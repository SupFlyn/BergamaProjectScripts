# p.07-09 movement: how people use it, today and the proposal (split from parts/15_ndvi_col.py, parts/15d_v44_pages.py, parts/15f_v46_pages.py, parts/15i_r28_movement.py, parts/16_write_city_link_movement.py on 29 Oct 2026; moved unchanged)


def div_t(d, dmax):
    if dmax <= 0:
        return 0.5
    s = math.sqrt(min(1.0, abs(d) / dmax))
    return 0.5 + 0.5 * s if d > 0 else 0.5 - 0.5 * s


# ============================================================ drawing (survey coordinates; baked via selinus_board helpers)
def _runs(chains, pieces, xy, value_of, inside_frame, F):
    """Polylines of equal value along every chain: [(points, value)], clipped to the frame."""
    out = []
    for ch in chains:
        run, cur = [], None
        for (pi, fw), n0, n1 in zip(ch["seq"], ch["nodes"][:-1], ch["nodes"][1:]):
            v = value_of(pi) if pi in inside_frame else None
            if v != cur or not run:
                if run and cur is not None:
                    out.append((run, cur))
                run, cur = [xy[n0]], v
            run.append(xy[n1])
        if run and cur is not None:
            out.append((run, cur))
    clipped = []
    for P, v in out:
        for q in F.clip_line(P):
            if len(q) >= 2:
                clipped.append((q, v))
    return clipped


# ------------------------------------------------------------ p.6 walking / driving today: the key streets only
def mv_key_rows(MV, key, n=MV_KEY_N):
    """v44: the n named streets (50 m+ in the frame) with the highest potential `key` today (the engine's own street
    table), highest first."""
    return [r for r in sorted(MV.get("big") or [], key=lambda r: -r[key]) if r[key] > 0][:n]


def mv_with_masterplan(S, M):
    """v44: the movement engine run with the masterplan's proposal (once per run, S.mv_mp): cars off the roads it makes
    pedestrian or relocates, each crossing joined to the walking network across the stream, the hub squares as new
    everyday destinations (as the city link stops are in the board's own proposal run). None without OSM."""
    if getattr(S, "mv_mp", None) is not None:
        return S.mv_mp or None
    S.mv_mp = {}
    osm = getattr(S, "osm", None)
    if not osm:
        return None
    closed = [_xy_list(r.get("xy")) for r in M.get("roads") or [] if r.get("change") in ("pedestrian", "relocated")]
    closed = [P for P in closed if len(P) >= 2]
    props = []
    for c in M.get("crossings") or []:
        p = _xy1(c.get("xy"))
        nrm = stream_normal(S, p[0], p[1]) if p else None
        if p and nrm:
            props.append(("bridge", [(p[0] - nrm[0] * CROSS_HALF, p[1] - nrm[1] * CROSS_HALF),
                                     (p[0] + nrm[0] * CROSS_HALF, p[1] + nrm[1] * CROSS_HALF)], False))
    attr = [p for p in (_xy1(h.get("xy")) for h in M.get("hubs") or []) if p]
    t0, log = time.time(), []
    try:
        ns = dict(globals())
        ns["build_corridors"] = lambda S_: None              # the board has built its spines already
        S.mv_mp = dict(R=analyse(ns, S, osm, PLACES_PATH or None, props, closed, attr, MV_OPT, log))
    except Exception:
        LOG.append("WARNING: movement with the masterplan's proposal failed:\n" + traceback.format_exc())
        return None
    LOG.append("Movement with the masterplan's proposal ({:.0f} s; {} roads closed to cars, {} crossings, {} hubs): "
               .format(time.time() - t0, len(closed), len(props), len(attr)) + " ".join(l_ for l_ in log if l_))
    return S.mv_mp


def b_view(F, x, ytop, U):
    """v46: a theme-B map: the whole frame F at 1:10,000 on the booklet page, its top-left corner at (x, ytop); k =
    board units per booklet mm of a drawing 120 U wide (as draw_edge_build). Returns (View, k, board units per metre,
    the map's rectangle)."""
    k = 120.0 * U / BK_AW
    ss = 1000.0 * k / B_DEN
    return View(F, ss, x, ytop), k, ss, (x, ytop - F.h * ss, x + F.w * ss, ytop)


def mv_reach(R, starts, rmax):
    """v46: walkable reach: the walking cost (flat-ground metres; Tobler slope on the survey terrain where the network
    has heights) from the nearest start point to every node of the walking network WITH the proposal (walk_a: today's
    streets and footways and the masterplan's crossings), out to rmax; each start joins the network at its nearest
    node within MV_OPT["snap"], that distance counted. Returns {node: cost}."""
    pieces, xy = R["pieces"], R["xy"]
    z = getattr(pieces, "z", None) or {}
    adj = {}
    for p in pieces:
        if not p["walk"] or p["L"] <= 0:
            continue
        a, b = p["a"], p["b"]
        za, zb = z.get(a), z.get(b)
        g = (zb - za) / p["L"] if za is not None and zb is not None else 0.0
        adj.setdefault(a, []).append((b, p["L"] * tobler_factor(g)))
        adj.setdefault(b, []).append((a, p["L"] * tobler_factor(-g)))
    hq, cost = [], {}
    for sx, sy in starts:
        best = min(((xy[n][0] - sx) ** 2 + (xy[n][1] - sy) ** 2, n) for n in adj) if adj else None
        if best and best[0] <= MV_OPT["snap"] ** 2:
            heapq.heappush(hq, (math.sqrt(best[0]), best[1]))
    while hq:
        d, n = heapq.heappop(hq)
        if n in cost:
            continue
        cost[n] = d
        for m, c in adj[n]:
            if m not in cost and d + c <= rmax:
                heapq.heappush(hq, (d + c, m))
    return cost


def r28mv_line_w(line, h):
    """the width of one line of r28mv_lines"""
    sw_ = r28mv_tw(u" ", h)
    return sum((sw_ if sp else 0.0) + sum(r28mv_tw(t_, h, b_) for t_, b_ in word) for sp, word in line)


def r28mv_title(s):
    """an upper-case name in title case with its Turkish letters (K4 · ULUCAMİ ÖNÜ -> K4 · Ulucami Önü, İSTİKLAL
    MEYDANI -> İstiklal Meydanı); words with digits and words not in capitals stay as written"""
    out = []
    for w_ in (s or u"").split(u" "):
        if not w_ or any(c_.isdigit() for c_ in w_) or not w_.isupper():
            out.append(w_)
            continue
        lo = w_.replace(u"I", u"ı").replace(u"İ", u"i").lower()
        out.append({u"i": u"İ", u"ı": u"I"}.get(lo[0], lo[0].upper()) + lo[1:])
    return u" ".join(out)


def r28mv_cap(s):
    return (s or u"")[:1].upper() + (s or u"")[1:]


def r28mv_note_text(note, heads):
    """the masterplan's note without its leading "change: " (the change is printed in bold before it)"""
    n_ = (note or u"").strip()
    if u": " in n_ and n_.split(u": ", 1)[0].strip().lower() in heads:
        n_ = n_.split(u": ", 1)[1].strip()
    return n_


def r28mv_entry(name, change, note):
    """a list entry: **name · change** · note"""
    return u"**{}{}**{}".format(name, u" · " + change if change else u"", u" · " + note if note else u"")


def r28mv_src_mv():
    """the movement method's source (the same words as the top map's, so the same [n])"""
    return ("Movement potential = the number of shortest routes between every building and every everyday "
            "destination within {:.0f} m on foot or {:.0f} min by car that use the street (OSM network, Overture "
            "places, the method of bergama_movement v1); index 100 = the busiest street piece in the frame. A count "
            "of routes, not of people or vehicles: no count exists for these streets.".format(
                MV_OPT["r_walk"], MV_OPT["t_car"] / 60.0))


def _r28mv_wh(w_, h_):
    return lambda f: (w_ * f, h_ * f)


def r28mv_base_leg():
    """the pale base's legend rows (b_base's tones as R28Pale draws them) and the study area"""
    return [("box", r28mv_pale(MPL["water"], 0.3), u"Selinos stream"), ("box", r28mv_pale(MPL["bld"], 0.5), u"Building"),
            ("box", r28mv_pale(MPL["her"], 0.5), u"Heritage building"), R28_STUDY_LEG]


# ------------------------------------------------------------ p.07 walking / driving today: every piece graded
def r28mv_class(v):
    """the index class (0-4) of value v"""
    for i, up in enumerate(R28MV_CLS):
        if v < up:
            return i
    return len(R28MV_CLS) - 1


def r28mv_class_streets(B, V, runs, k, L, order):
    """v50 (MIRAQUA 28 Oct, P07.3): every street piece of runs [(points, (OSM class, index))] (mv_runs) in its index
    class: colour (the top map's SEQ ramp at the class's upper step) and line weight (R28MV_CLS_W) by class, the
    busiest drawn last. Returns the length (m) in each class."""
    lens = [0.0] * len(R28MV_CLS)
    for P, (cls, v) in sorted(runs, key=lambda r_: r_[1][1]):
        c_ = r28mv_class(v)
        lens[c_] += pl_length(P)
        B.line(V.P(P), R28MV_CLS_COL[c_], L, order + c_, bk_lw(R28MV_CLS_W[c_], k))
    return lens


def r28mv_class_legend():
    """the five classes as booklet legend rows: sample in the class's colour and line weight (pt)"""
    labs = [u"{:.0f}-{:.0f}".format(a_, b_) for a_, b_ in zip((0.0,) + R28MV_CLS[:-1], R28MV_CLS)]
    return [dict(kind="line", colour=crop_hex(c_), label=u"Walk / car index " + lab, width=round(w_ * 72.0 / 25.4, 2))
            for c_, lab, w_ in zip(R28MV_CLS_COL, labs, R28MV_CLS_W)]


def draw_mv_key(S, B, V, R, MV, key, F, L, h, bounds):
    """v44: the key streets of the walking / driving map, named. v50 (MIRAQUA 28 Oct, P07.3, P07.4): every street
    piece is drawn graded (r28mv_class_streets), so this names the 5 busiest named streets (mv_key_rows) at h (7 pt),
    "name · index" on its longest run, placed without overlaps (place_labels). Returns (their rows, the key of the
    labels that found no place, {name: every point of its runs})."""
    rows = mv_key_rows(MV, key)
    names = set(r_["name"] for r_ in rows)
    pieces = R["pieces"]
    net = "car_b" if key.startswith("car") else "walk_b"

    def val(pi):
        nm = (pieces[pi]["tags"].get("name") or "").strip()
        return nm if nm in names else None
    best, pts = {}, {}
    for P, nm in _runs(R["chains"][net], pieces, R["xy"], val, set(R["inside"]), F):
        pts.setdefault(nm, []).extend(P)
        if nm not in best or pl_length(P) > pl_length(best[nm]):
            best[nm] = P
    labels = []
    for r_ in rows:
        P = best.get(r_["name"])
        if P:
            q, t = pl_point_at(P, pl_length(P) / 2.0)
            px, py = V.p(q[0], q[1])
            labels.append(([u"{} · {:.0f}".format(r_["name"], r_[key])], px, py, h, INK))
    return rows, place_labels(B, labels, [], L, bounds=bounds), pts


def r28mv_main_stream(S):
    streams = [P for P in (getattr(S, "selinus", None) or []) if len(P) >= 2]
    return max(streams, key=pl_length) if streams else None


def r28mv_edge_means(S, R):
    """v50 (P07.2): today's walking and driving index, length-weighted, on the street pieces whose middle lies within
    R28MV_EDGE_M of the main Selinos line (as city_link_movement.json "edge") and on every piece on the map:
    {"walk_b" | "car_b": (along the stream, all, m along the stream)}; once per run (S._r28mv_edge)."""
    got = getattr(S, "_r28mv_edge", None)
    if got is not None:
        return got
    out, main = {}, r28mv_main_stream(S)
    if main:
        d = R28MV_EDGE_M
        segs = list(zip(main[:-1], main[1:]))
        g = Grid(d)
        for i, (a, b) in enumerate(segs):
            g.add(i, (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])))
        pieces, xy, IDX = R["pieces"], R["xy"], R["IDX"]
        acc = {"walk_b": [0.0, 0.0, 0.0, 0.0], "car_b": [0.0, 0.0, 0.0, 0.0]}
        for i in R["inside"]:
            p = pieces[i]
            if p["prop"] or p["L"] <= 0:
                continue
            m = ((xy[p["a"]][0] + xy[p["b"]][0]) / 2.0, (xy[p["a"]][1] + xy[p["b"]][1]) / 2.0)
            near = any(seg_dist(m[0], m[1], segs[j][0][0], segs[j][0][1], segs[j][1][0], segs[j][1][1]) <= d
                       for j in g.query((m[0] - d, m[1] - d, m[0] + d, m[1] + d)))
            for key, ok in (("walk_b", p["walk"]), ("car_b", p["cf"] or p["cb"])):
                if not ok:
                    continue
                v = IDX[key].get(i, 0.0) * p["L"]
                a_ = acc[key]
                a_[0] += v
                a_[1] += p["L"]
                if near:
                    a_[2] += v
                    a_[3] += p["L"]
        out = dict((key, (a_[2] / a_[3] if a_[3] else None, a_[0] / a_[1] if a_[1] else None, a_[3]))
                   for key, a_ in acc.items())
    S._r28mv_edge = out
    return out


# ------------------------------------------------------------ p.07 the notes beside the maps (P07.2)
def r28mv_note(B, crop, k, L, num, items, head=u"Why these streets matter"):
    """v50 (MIRAQUA 28 Oct, P07.2): a short note in the empty width right of a p.07 map whose crop is `crop` (board
    units): its heading, then items (lines with one or two **bold** keywords, G5), 9 pt (8.5, 8 where the map's
    height asks for it; the last items left out, logged, where even that does not fit). Crop drw_mv_note_<num>, as
    tall as its text, its top on the map's, drawn for its width on the booklet page (bk_w): the row map + 4 mm +
    note stays within BK_AW, so the map keeps 1:10,000."""
    wmax = BK_AW - R28MV_GUT - (crop[2] - crop[0]) / k - 0.5     # mm the row leaves for the note's crop
    nw = min(R28MV_NOTE_W, wmax - 1.0)                            # mm of text
    if nw < 30.0 or not items:
        LOG.append("Note {} beside the p.07 map not drawn (no width or nothing to say).".format(num))
        return
    hmax = crop[3] - crop[1] - 1.0 * k                            # no taller than its map's crop
    x0 = crop[2] + R28MV_GUT * k
    tx, items, fit = x0 + 0.5 * k, list(items), None
    while items and fit is None:
        for pt in (9.0, 8.5, 8.0):
            h, hh = bk_hk(pt, k), bk_hk(pt + 0.5, k)
            lines = [r28mv_lines(it, nw * k, h) for it in items]
            need = 0.5 * k + hh + (R28MV_LEAD + 0.6) * h + (sum(len(l_) for l_ in lines) - 1) * R28MV_LEAD * h + \
                (len(lines) - 1) * 0.5 * h + 0.4 * h + 0.5 * k
            if need <= hmax:
                fit = (h, hh, lines)
                break
        if fit is None:
            LOG.append(u"Note {} beside the p.07 map: \"{}\" left out (no room).".format(num, items[-1]))
            items = items[:-1]
    if fit is None:
        return
    h, hh, lines = fit
    y = crop[3] - 0.5 * k - hh
    B.text(head, tx, y, hh, INK, L, order=66, font=FONT_TITLE, bold=True)
    y -= (R28MV_LEAD + 0.6) * h
    for j, item in enumerate(lines):
        for ln in item:
            r28mv_draw_line(B, ln, tx, y, h, INK, L)
            y -= R28MV_LEAD * h
        y -= 0.5 * h
    bot = y + R28MV_LEAD * h + 0.5 * h - 0.4 * h
    crop_panel("mv_note_{}".format(num), x0, bot - 0.5 * k, x0 + (nw + 1.0) * k, crop[3], u"")
    CROP_PANELS[-1]["bk_w"] = nw + 1.0


def r28mv_note_top(S, B, crop, k, L, MV, n_pl):
    """v50 (P07.2): drw_mv_note_1, beside the top map: the shops' streets, the busiest street, shops against walking,
    the civic constellations and the services, all as the board computes and prints them on the page."""
    out = []
    prim = [g for g in getattr(S, "corr_primary", None) or [] if g["label"] != "an unnamed street"]
    if prim:
        out.append(u"**Shops** line up on {}: the primary commercial spines {}.".format(
            join_names([u"{} ({} shops)".format(g["label"], g["n"]) for g in prim]), bcite(R28MV_SRC_COM)))
    sec = getattr(S, "corr_secondary", None) or []
    if sec:
        out.append(u"**{} more street{}** with 3 or more shops: the secondary spines.".format(
            len(sec), u"" if len(sec) == 1 else u"s"))
    rows = MV.get("rows") or []
    if rows:
        out.append(u"**Busiest street** on foot and by car together: {}, index {:.0f} (100 = the busiest street "
                   u"piece) {}.".format(rows[0]["name"], rows[0]["comb_b"], bcite(r28mv_src_mv())))
    rho, big = (MV.get("rho") or {}).get("walk_b"), MV.get("big") or []
    if rho is not None and big:
        out.append(u"**Shops and walking**: Spearman {:.2f} over the {} named streets of 50 m or more (1 = the same "
                   u"order).".format(rho, len(big)))
    cl = [c_ for c_ in getattr(S, "clusters", None) or [] if any(S.F.inside(p[0], p[1]) for p in c_["P"])]
    if cl:
        out.append(u"**{} civic constellation{}** on the map: 3 or more civic or sacred places, each within 100 m of "
                   u"the next.".format(len(cl), u"" if len(cl) == 1 else u"s"))
    tot = sum((n_pl or {}).values())
    if tot:
        f, n = max(n_pl.items(), key=lambda kv: kv[1])
        lab = dict((f_, lab_) for f_, let_, c_, lab_ in WALK_FUN).get(f, f)
        out.append(u"**{} services** on the map (Overture places); the most are {} ({}).".format(tot, lab.lower(), n))
    r28mv_note(B, crop, k, L, 1, out)


def r28mv_note_today(S, R, MV, key, rows, pts, lens):
    """v50 (P07.2): the lines of drw_mv_note_2 / _3: the busiest named streets, how many of them come close to the
    stream, the index along the stream against all streets, how the network length spreads over the classes, what
    the index counts"""
    walk = key.startswith("walk")
    out = []
    if rows:
        out.append(u"**Busiest**: " + u", ".join(u"{} {:.0f}".format(r_["name"], r_[key]) for r_ in rows) + u".")
    main = r28mv_main_stream(S)
    if main and rows:
        near = [r_ for r_ in rows if pts.get(r_["name"]) and
                min(pl_dist(p[0], p[1], main, False) for p in pts[r_["name"]]) <= R28MV_NEAR_M]
        out.append(u"**{} of the {}** busiest come within {:.0f} m of the stream.".format(len(near), len(rows),
                                                                                         R28MV_NEAR_M))
    em = r28mv_edge_means(S, R).get(key)
    if em and em[0] is not None and em[1] is not None:
        out.append(u"**Along the stream** (streets within {:.0f} m of it): index {:.0f} on average, all streets on the "
                   u"map {:.0f}.".format(R28MV_EDGE_M, em[0], em[1]))
    tot = sum(lens)
    if tot > 0:
        out.append(u"**{:.0f}%** of the {} street length carries index 25 or more, {:.0f}% stays under 2.".format(
            100.0 * (lens[3] + lens[4]) / tot, u"walkable" if walk else u"drivable", 100.0 * lens[0] / tot))
    if walk:
        out.append(u"**On foot**: the shortest routes up to {:.0f} m between every building and the everyday "
                   u"destinations; 100 = the busiest piece today {}.".format(MV_OPT["r_walk"], bcite(r28mv_src_mv())))
    else:
        out.append(u"**By car**: the shortest routes up to {:.0f} min; footways and steps are not on this map "
                   u"{}.".format(MV_OPT["t_car"] / 60.0, bcite(r28mv_src_mv())))
    return out


def draw_mv_today(S, B, x, y, U, R, MV, key, title, cap):
    """v46 (Prompt 3, p.8): walking or driving today as its own map at the theme's one scale: the whole site frame at
    1:10,000, the masterplan base, the scale bar and north arrow under it. v50 (MIRAQUA 28 Oct, P07.3): the index on
    EVERY street piece of its network (mv_runs walk_b / car_b; walking-only pieces stay base street on the driving
    map), graded in five classes by colour and line weight (r28mv_class_streets), the classes in the crop's legend;
    the 5 busiest named streets named at 7 pt (draw_mv_key, P07.4); P07.2: its note beside it (drw_mv_note_2 / _3).
    Returns the y below its crop."""
    L = "LU_BOARD::HowPeopleUseIt"
    F = S.F
    B.text(title, x, y, 0.5 * U, INK, L, font=FONT_TITLE, bold=True)
    V, k, ss, r = b_view(F, x, y - 0.8 * U, U)
    h = bk_hk(R28MV_LABEL_PT, k)
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 1)
    b_base(S, CB, V, k, L)
    lens = r28mv_class_streets(CB, V, mv_runs(S, R, key, F), k, L, 14)
    rows, key_, pts = draw_mv_key(S, CB, V, R, MV, key, F, L, h, r)
    b_frame(B, r, k, L)
    low = b_foot(B, F, x, r[1], ss, k, L)
    if key_:
        low = draw_label_key(B, key_, x, low - 0.8 * k, r[2] - x, h, L)
    crop = (x - 0.5 * k, low - 0.5 * k, r[2] + 0.5 * k, r[3] + 0.5 * k)
    crop_panel(CROP_MV.get(key, key), crop[0], crop[1], crop[2], crop[3], cap.format(len(rows)), crop_scale(ss),
               r28mv_class_legend())
    if key in R28MV_NOTE_OF:
        r28mv_note(B, crop, k, L, R28MV_NOTE_OF[key], r28mv_note_today(S, R, MV, key, rows, pts, lens))
    return low - 0.5 * k


# ------------------------------------------------------------ p.09 the proposal: symbols
def r28mv_offset(Q, d):
    """the polyline Q moved d (board units) to its left"""
    out, n = [], len(Q)
    for i in range(n):
        a, b = Q[max(0, i - 1)], Q[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1.0
        out.append((Q[i][0] - dy / ln * d, Q[i][1] + dx / ln * d))
    return out


def r28mv_road_line(B, Q, st, k, L, order):
    """a road of category style st (R28MV_ROAD) along the page polyline Q: a white casing, the line (dashed where the
    style says), the calmed road's short cross ticks"""
    nm, col, w, dash, ticks = st
    B.line(Q, WHITE, L, order, bk_lw(w + 0.5, k))
    for d in (dashes(Q, dash[0] * k, dash[1] * k) if dash else [Q]):
        B.line(d, col, L, order + 1, bk_lw(w, k))
    if ticks:
        lq, s = pl_length(Q), 0.7 * k
        while s < lq:
            p, t = pl_point_at(Q, s)
            B.line([(p[0] - t[1] * 0.85 * k, p[1] + t[0] * 0.85 * k), (p[0] + t[1] * 0.85 * k, p[1] - t[0] * 0.85 * k)],
                   col, L, order + 2, bk_lw(0.22, k))
            s += 1.4 * k


def r28mv_bus_line(B, Q, k, L, order, dashed=True, side=1.05):
    """the bus line along the page polyline Q, side mm to its left (beside the road it runs on), dashed when later"""
    nm, col, w, dash = R28MV_BUS
    Qo = r28mv_offset(Q, side * k) if side else Q
    for d in (dashes(Qo, dash[0] * k, dash[1] * k) if dashed else [Qo]):
        B.line(d, col, L, order, bk_lw(w, k))


def r28mv_cross(B, px, py, e, kind, k, L, order, s=1.0):
    """a crossing at (px, py), e = the page direction across the stream: bridge kept = two decks with flared ends
    (R28_OPEN bridge), footbridge = one bar with end ticks, stepping stones = four stones (both R28_MARKERS
    crossings), each on a white casing"""
    t = (-e[1], e[0])
    a = R28MV_SYM * k * s

    def pt(fe, ft):
        return (px + e[0] * fe + t[0] * ft, py + e[1] * fe + t[1] * ft)
    col = R28MV_MK["crossings"]
    if kind == "bridge kept":
        for sd in (-0.55, 0.55):
            B.line([pt(-a, sd * k * s), pt(a, sd * k * s)], WHITE, L, order, bk_lw(0.8, k))
        for sd in (-0.55, 0.55):
            fl = math.copysign(0.45, sd) * k * s
            B.line([pt(-a - 0.45 * k * s, sd * k * s + fl), pt(-a, sd * k * s), pt(a, sd * k * s),
                    pt(a + 0.45 * k * s, sd * k * s + fl)], R28MV_BRIDGE, L, order + 1, bk_lw(0.3, k))
    elif kind == "stepping stones":
        for f in (-0.75, -0.25, 0.25, 0.75):
            c_ = pt(f * a, 0.0)
            B.fill([circle_pts(c_[0], c_[1], 0.55 * k * s, 12)], WHITE, L, order)
            B.fill([circle_pts(c_[0], c_[1], 0.36 * k * s, 12)], col, L, order + 1)
    else:                                                 # a footbridge (any other new crossing alike)
        B.line([pt(-a, 0.0), pt(a, 0.0)], WHITE, L, order, bk_lw(1.0, k))
        B.line([pt(-a, 0.0), pt(a, 0.0)], col, L, order + 1, bk_lw(0.55, k))
        for f in (-a, a):
            B.line([pt(f, -0.6 * k * s), pt(f, 0.6 * k * s)], col, L, order + 1, bk_lw(0.3, k))


def r28mv_hub(B, px, py, role, k, L, order, s=1.0):
    """a hub at (px, py): a ring (R28_MARKERS hubs) round its place, which stays visible inside (the bridge it sits
    at); a transit hub with a filled centre"""
    rr = R28MV_HUB_R * k * s
    ring = circle_pts(px, py, rr, 36)
    ring = ring + [ring[0]]
    col = R28MV_MK["hubs"]
    B.line(ring, WHITE, L, order, bk_lw(1.0 * s, k))
    B.line(ring, col, L, order + 1, bk_lw(0.5 * s, k))
    if role == "transit":
        B.fill([circle_pts(px, py, 1.0 * k * s, 20)], col, L, order + 1)


def r28mv_disc(B, cx, cy, n, col, k, L, order, r_mm=R28MV_DISC, pt=7.0):
    """a numbered callout: a disc in its group's colour, the number white, bold, centred by its measured width"""
    B.fill([circle_pts(cx, cy, r_mm * k, 24)], col, L, order)
    h = bk_hk(pt, k)
    t_ = str(n)
    B.text(t_, cx - 0.5 * r28mv_tw(t_, h, True), cy - 0.5 * h, h, WHITE, L, order=order + 1, font=FONT_TITLE,
           bold=True)


def r28mv_dot(B, px, py, col, k, L, order, hollow=False):
    """the index chart's mark: today a ring, with the proposal a dot"""
    rr = 0.85 * k
    if hollow:
        ring = circle_pts(px, py, rr, 16)
        B.fill([ring], WHITE, L, order)
        B.line(ring + [ring[0]], INK2, L, order + 1, bk_lw(0.3, k))
    else:
        B.fill([circle_pts(px, py, rr, 16)], col, L, order + 2)


def r28mv_sample(B, kind, arg, x0, yc, k, L, order=67):
    """a 5 mm key sample of a map symbol, drawn as on the map: road (arg = its style), bus (arg = dashed), truck,
    cross (arg = the crossing's kind, across a short piece of stream), hub (arg = role)"""
    x1 = x0 + 5.0 * k
    if kind == "road":
        r28mv_road_line(B, [(x0, yc), (x1, yc)], arg, k, L, order)
    elif kind == "bus":
        r28mv_bus_line(B, [(x0, yc), (x1, yc)], k, L, order, dashed=arg, side=0.0)
    elif kind == "truck":
        for d in dashes([(x0, yc), (x1, yc)], 2.4 * k, 1.2 * k):
            B.line(d, INK, L, order, bk_lw(0.6, k))
    elif kind == "cross":
        B.fill([rect(x0, yc - 0.9 * k, x1, yc + 0.9 * k)], r28mv_pale(MPL["water"], 0.3), L, order)
        r28mv_cross(B, x0 + 2.5 * k, yc, (0.0, 1.0), arg, k, L, order + 1, s=0.6)
    elif kind == "hub":
        r28mv_hub(B, x0 + 2.5 * k, yc, arg, k, L, order, s=0.7)


def r28mv_list(B, head, keyrow, entries, x0, y, cw, k, L):
    """v50 (MIRAQUA 28 Oct, P09.2): one group of the proposal's list in a column cw wide from y down: its name, the
    key of its symbols as the map draws them (keyrow [(kind, arg, label)]), then each entry [(number or None, colour,
    text)]: the number disc in the group's colour, **name · change** · note, wrapped, 7.5 pt. Returns the y under it."""
    h8, h75, h7 = bk_hk(8.0, k), bk_hk(7.5, k), bk_hk(7.0, k)
    yb = y - h8
    B.text(head.upper(), x0, yb, h8, INK, L, order=66, font=FONT_TITLE, bold=True)
    yb -= 2.1 * h8
    cx = x0
    for kind, arg, lab in keyrow:
        wl = 6.2 * k + r28mv_tw(lab, h7) + 3.0 * k
        if cx > x0 and cx + wl > x0 + cw:
            cx, yb = x0, yb - 2.0 * h7
        r28mv_sample(B, kind, arg, cx, yb + 0.5 * h7, k, L)
        B.text(lab, cx + 6.2 * k, yb, h7, INK, L, order=66, font=FONT_TITLE)
        cx += wl
    yb -= (2.7 if keyrow else 0.6) * h75
    tx, tw_ = x0 + 4.1 * k, cw - 4.1 * k
    last = yb
    for n_, col, txt in entries:
        if n_ is not None:
            r28mv_disc(B, x0 + 1.55 * k, yb + 0.5 * h75, n_, col, k, L, 66, r_mm=1.55)
        for ln in r28mv_lines(txt, tw_, h75):
            r28mv_draw_line(B, ln, tx, yb, h75, INK, L)
            last = yb
            yb -= R28MV_LEAD * h75
        yb -= 0.55 * h75
    return min(last - 0.5 * h75, yb + R28MV_LEAD * h75)


# ------------------------------------------------------------ p.09 the proposal map (P09.1, P09.2)
def draw_mv_proposal(S, B, x, y, w, U, M):
    """v46 (Prompt 3, p.10): THE PROPOSAL, the whole site frame at 1:10,000 on the frame's axes (one strip, G7).
    v50 (MIRAQUA 28 Oct, P09.1, redrawn from scratch: the multiplied green glow buried the streets, the names
    overlapped): one line on what the map shows; a pale base (b_base through R28Pale, G6); reach on foot from the
    masterplan's hubs (mv_reach on the network with the proposal) as thin streets in the three crisp classes of
    R28_REACH, never a glow, never multiplied; the roads by category as line types on a white casing (kept thin,
    calmed with ticks, pedestrian heavy, shared dashed; the bus line dashed beside its streets); the crossings as
    symbols across the stream (bridge kept: two decks, named K1-K6; footbridge: one bar; stepping stones: four
    stones), the hubs as rings (transit: a filled centre); every road, new crossing and hub a numbered disc in its
    group's colour (R28_MARKERS), on a leader where it sits off its point, placed without overlaps (label_place, G4).
    Under the map the scale bar, north arrow and the reach key, then (P09.2) the list in three groups (roads;
    bridges and crossings; hubs), each with the key of its symbols and its entries **name · change** · note, numbered
    upstream to downstream; then (P09.3) the index change chart (r28mv_index_change). Crops drw_proposal and
    drw_index_change. Returns the y below."""
    L = "LU_BOARD::Proposal"
    F = S.F
    B.text(u"THE PROPOSAL · HOW PEOPLE WILL MOVE", x, y, 1.05 * U, INK, L, font=FONT_TITLE, bold=True)
    k = 120.0 * U / BK_AW
    h9, h75, h7 = bk_hk(9.0, k), bk_hk(7.5, k), bk_hk(7.0, k)
    MR = mv_with_masterplan(S, M)
    R2 = MR.get("R") if MR else None
    hubs = [hb for hb in M.get("hubs") or [] if _xy1(hb.get("xy"))]
    hub_xy = [_xy1(hb["xy"]) for hb in hubs]
    rw = R28_REACH[-1][0]
    top = y - 1.2 * U                                     # the crop's top
    mw = F.w * 1000.0 * k / B_DEN
    what = (u"What it shows: **reach on foot** from the {} hubs along today's streets (green), and **the roads, "
            u"crossings and hubs** of the masterplan, numbered as in the list below.").format(len(hub_xy))
    yb = top - 0.5 * k - h9
    for ln in r28mv_lines(what, mw, h9):
        r28mv_draw_line(B, ln, x, yb, h9, INK, L)
        yb -= R28MV_LEAD * h9
    V, k, ss, r = b_view(F, x, yb + R28MV_LEAD * h9 - 2.5 * k, U)
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 1)
    b_base(S, R28Pale(CB), V, k, L)
    # reach on foot: thin streets, three crisp classes (R28_REACH), normal blend
    km = [0.0] * len(R28_REACH)
    src = None
    if R2 and hub_xy:
        cost = mv_reach(R2, hub_xy, rw)
        pieces = R2["pieces"]

        def reach_cls(pi):
            p = pieces[pi]
            if p["prop"]:                                 # the crossings' network joins: drawn as crossings
                return None
            c_ = min(cost.get(p["a"], 1e12), cost.get(p["b"], 1e12))
            return next((j for j, rc in enumerate(R28_REACH) if c_ <= rc[0]), None)
        for P, c_ in sorted(_runs(R2["chains"]["walk_a"], pieces, R2["xy"], reach_cls, set(R2["inside"]), F),
                            key=lambda rr_: -rr_[1]):
            CB.line(V.P(P), C(R28_REACH[c_][2]), L, 20 + len(R28_REACH) - c_, bk_lw(R28MV_REACH_W[c_], k))
            km[c_] += pl_length(P) / 1000.0
        LOG.append(u"Proposal map: reach on foot from {} hubs (Tobler, with the masterplan's crossings): {} km of "
                   u"street and footway in the frame.".format(len(hub_xy), u" / ".join(
                       u"{} {:.1f}".format(lab_, km_) for (lim_, lab_, hx_), km_ in zip(R28_REACH, km))))
        src = bcite("Reach on foot: the shortest walking cost from the nearest masterplan hub along the OSM streets "
                    "and footways and the masterplan's crossings (the board's movement network with the proposal), "
                    "each street piece timed by Tobler (1993) on the survey terrain and given as flat-ground metres, "
                    "in three classes (0-100, 100-400, 400-800 m) to {:.0f} m, the walking radius of the movement "
                    "method (bergama_movement v1). Computed; weakest assumption: every crossing open and every "
                    "footway walkable all year.".format(rw))
    else:
        LOG.append("Proposal map: no street network with the masterplan (OSM) or no hubs, so no reach on foot drawn.")

    def mm(p):                                            # board -> booklet mm from the map's lower-left corner
        return ((p[0] - r[0]) / k, (p[1] - r[1]) / k)
    segs, taken, roads, cross, kept, hubl = [], [], [], [], [], []
    for rd in M.get("roads") or []:                       # the roads by category
        P = _xy_list(rd.get("xy"))
        runs = F.clip_line(P) if len(P) >= 2 else []
        if not runs:
            continue
        ch = rd.get("change", "kept")
        st = R28MV_ROAD.get(ch, R28MV_ROAD["kept"])
        for run in runs:
            Q = V.P(run)
            r28mv_road_line(CB, Q, st, k, L, 30)
            segs += [(mm(a), mm(b)) for a, b in zip(Q[:-1], Q[1:])]
        run = max(runs, key=pl_length)
        q, t = pl_point_at(run, pl_length(run) / 2.0)
        chl = st[0] if ch in R28MV_ROAD else ch
        roads.append(dict(grp="roads", ch=ch, chlab=chl, name=rd.get("name", u""), P=P, at=V.p(q[0], q[1]), col=st[1],
                          text=r28mv_entry(rd.get("name", u""), chl, r28mv_note_text(rd.get("note"), (ch, chl)))))
    tr = M.get("truck_route")
    if tr and len(_xy_list(tr.get("xy"))) >= 2:
        P = _xy_list(tr["xy"])
        runs = F.clip_line(P)
        for run in runs:
            Q = V.P(run)
            for d in dashes(Q, 2.4 * k, 1.2 * k):
                CB.line(d, INK, L, 35, bk_lw(0.6, k))
            segs += [(mm(a), mm(b)) for a, b in zip(Q[:-1], Q[1:])]
        if runs:
            run = max(runs, key=pl_length)
            q, t = pl_point_at(run, pl_length(run) * 0.35)
            roads.append(dict(grp="roads", ch="truck", chlab=u"rerouted", name=tr.get("name", u"truck route"), P=P,
                              at=V.p(q[0], q[1]), col=INK, text=r28mv_entry(r28mv_cap(tr.get("name", u"truck route")),
                                                                            u"rerouted", tr.get("note", u""))))
    else:
        LOG.append("Proposal map: truck route pending in the masterplan (movement.truck_route is null).")
    bus_dash = set()
    for rt in M.get("routes") or []:                      # the town bus line extended to K4, a later step
        P = _xy_list(rt.get("xy"))
        runs = F.clip_line(P) if len(P) >= 2 else []
        if not runs:
            continue
        later = bool(rt.get("later")) or str(rt.get("status", "")).lower() in ("later", "proposed", "future")
        bus_dash.add(later)
        for run in runs:
            Q = V.P(run)
            r28mv_bus_line(CB, Q, k, L, 36, dashed=later)
            segs += [(mm(a), mm(b)) for a, b in zip(Q[:-1], Q[1:])]
        run = max(runs, key=pl_length)
        q, t = pl_point_at(run, pl_length(run) * 0.35)
        chl = u"later step" if later else u"bus line"
        roads.append(dict(grp="roads", ch="bus", chlab=chl, name=r28mv_cap(rt.get("name", u"")), P=P,
                          at=V.p(q[0], q[1]), col=R28MV_BUS[1], text=r28mv_entry(
                              r28mv_cap(rt.get("name", u"")), chl, r28mv_note_text(rt.get("note"), ("later step", "later")))))
    for c in M.get("crossings") or []:                    # crossings, symbols across the stream
        p = _xy1(c.get("xy"))
        if not p or not F.inside(p[0], p[1]):
            continue
        px, py = V.p(p[0], p[1])
        nrm = stream_normal(S, p[0], p[1]) or (0.0, 1.0)
        a_ = V.p(p[0] + nrm[0], p[1] + nrm[1])
        ln_ = math.hypot(a_[0] - px, a_[1] - py) or 1.0
        kind = c.get("kind", "footbridge")
        r28mv_cross(CB, px, py, ((a_[0] - px) / ln_, (a_[1] - py) / ln_), kind, k, L, 40)
        q_ = mm((px, py))
        taken.append((q_[0] - R28MV_SYM - 0.3, q_[1] - R28MV_SYM - 0.3, q_[0] + R28MV_SYM + 0.3, q_[1] + R28MV_SYM + 0.3))
        nm = c.get("name", u"") or u""
        if kind == "bridge kept":
            kept.append((nm.replace(u" bridge", u""), px, py))
        else:
            cross.append(dict(grp="crossings", ch=kind, at=(px, py), text=r28mv_entry(r28mv_cap(nm), u"",
                                                                                     c.get("note", u""))))
    for hb in hubs:                                       # hubs, rings
        p = _xy1(hb["xy"])
        if not F.inside(p[0], p[1]):
            continue
        px, py = V.p(p[0], p[1])
        role = str(hb.get("role", "") or "")
        r28mv_hub(CB, px, py, role, k, L, 50)
        q_ = mm((px, py))
        rr = R28MV_HUB_R + 0.4
        taken.append((q_[0] - rr, q_[1] - rr, q_[0] + rr, q_[1] + rr))
        bits = [u"sub-hub in the bed"] if hb.get("sub_hub") else []
        if hb.get("bus_stop"):
            try:
                bits.append(u"bus stop {}, {:.0f} m".format(hb["bus_stop"], float(hb.get("bus_stop_m"))))
            except Exception:
                bits.append(u"bus stop {}".format(hb["bus_stop"]))
        hubl.append(dict(grp="hubs", ch=role, at=(px, py), text=r28mv_entry(
            r28mv_title(hb.get("name", u"")), (role + u" hub") if role else u"hub", u" · ".join(bits))))
    # numbers: roads (the bus line last), new crossings, hubs, each upstream (left) to downstream
    roads.sort(key=lambda d_: (d_["ch"] in ("bus", "truck"), d_["at"][0]))
    cross.sort(key=lambda d_: d_["at"][0])
    hubl.sort(key=lambda d_: d_["at"][0])
    for n_, d_ in enumerate(roads + cross + hubl):
        d_["n"] = n_ + 1
    # G4: the kept bridges' names, then the numbered discs, each clear of the symbols, the roads and each other
    bounds = (0.3, 0.3, (r[2] - r[0]) / k - 0.3, (r[3] - r[1]) / k - 0.3)
    its = [dict(x=mm((px, py))[0], y=mm((px, py))[1], wh=_r28mv_wh(r28mv_tw(nm, h7, True) / k, h7 / k), rank=0)
           for nm, px, py in kept]
    for i_, (bx, lead, f_) in place_labels_all(its, taken, bounds, segs, sizes=(1.0,), pad=0.3).items():
        nm, px, py = kept[i_]
        B.text(nm, r[0] + bx[0] * k, r[1] + bx[1] * k, h7, INK, L, order=64, font=FONT_TITLE, bold=True)
        if lead:
            e_ = lp_leader_end(bx, mm((px, py)))
            B.line([(px, py), (r[0] + e_[0] * k, r[1] + e_[1] * k)], INK2, L, 63, bk_lw(0.12, k))
    calls = hubl + cross + roads                          # placed in this order: hubs, crossings, roads
    dd = 2.0 * R28MV_DISC
    its = [dict(x=mm(c_["at"])[0], y=mm(c_["at"])[1], wh=_r28mv_wh(dd, dd), rank=0) for c_ in calls]
    got = place_labels_all(its, taken, bounds, segs, sizes=(1.0,), pad=0.35)
    for i_, c_ in enumerate(calls):
        if i_ not in got:
            LOG.append(u"Proposal map: no room for callout {} ({}).".format(c_["n"], r28mv_parse(c_["text"])[0][0]))
            continue
        bx = got[i_][0]
        col = R28MV_MK[c_["grp"]]
        cx, cy = r[0] + 0.5 * (bx[0] + bx[2]) * k, r[1] + 0.5 * (bx[1] + bx[3]) * k
        ax, ay = c_["at"]
        dl = math.hypot(cx - ax, cy - ay)
        if dl > (R28MV_DISC + 0.9) * k:                   # off its point: a leader, from the symbol's edge
            ux, uy = (cx - ax) / dl, (cy - ay) / dl
            s0 = {"hubs": R28MV_HUB_R, "crossings": 0.8}.get(c_["grp"], 0.0) * k
            B.line([(ax + ux * s0, ay + uy * s0), (cx - ux * R28MV_DISC * k, cy - uy * R28MV_DISC * k)], col, L, 62,
                   bk_lw(0.15, k))
            if c_["grp"] == "roads":
                B.fill([circle_pts(ax, ay, 0.4 * k, 12)], col, L, 63)
        r28mv_disc(B, cx, cy, c_["n"], col, k, L, 64)
    b_frame(B, r, k, L)
    low = b_foot(B, F, x, r[1], ss, k, L)
    if src:                                               # the reach key, right of the scale bar and north arrow
        kx, yc = x + B_SB_M * ss + 20.0 * k, r[1] - 3.1 * k
        cx = kx + r28mv_draw_line(B, r28mv_lines(u"**Reach on foot** from the nearest hub, slope counted {}:".format(
            src), 1e9, h75)[0], kx, yc - 0.5 * h75, h75, INK, L) + 2.5 * k
        for (lim_, lab_, hx_), wl in zip(R28_REACH, R28MV_REACH_W):
            B.line([(cx, yc), (cx + 6.0 * k, yc)], C(hx_), L, 66, bk_lw(wl, k))
            B.text(lab_, cx + 7.2 * k, yc - 0.5 * h7, h7, INK, L, order=66, font=FONT_TITLE)
            cx += 7.2 * k + r28mv_tw(lab_, h7) + 4.0 * k
    # P09.2: the list in three groups, each with the key of its symbols
    gap = 6.0 * k
    cw = (mw - 2.0 * gap) / 3.0
    have = set(d_["ch"] for d_ in roads)
    keys = {"roads": [("road", R28MV_ROAD[c_], R28MV_ROAD[c_][0]) for c_ in ("kept", "calmed", "pedestrian", "shared",
                                                                             "relocated") if c_ in have] +
            ([("truck", None, u"truck route, rerouted")] if "truck" in have else []) +
            [("bus", d_, R28MV_BUS[0] if d_ else u"bus line") for d_ in sorted(bus_dash)],
            "crossings": ([("cross", "bridge kept", u"bridge kept")] if kept else []) +
            [("cross", kd, kd) for kd in ("footbridge", "stepping stones") if kd in set(d_["ch"] for d_ in cross)],
            "hubs": [("hub", ro, (ro + u" hub") if ro else u"hub") for ro in ("walking", "transit", "")
                     if ro in set(d_["ch"] for d_ in hubl)]}
    ents = {"roads": [(d_["n"], R28MV_MK["roads"], d_["text"]) for d_ in roads],
            "crossings": ([(None, None, u"**{} · bridges kept** · named on the map".format(u", ".join(
                nm for nm, px, py in sorted(kept, key=lambda q__: q__[1]))))] if kept else []) +
            [(d_["n"], R28MV_MK["crossings"], d_["text"]) for d_ in cross],
            "hubs": [(d_["n"], R28MV_MK["hubs"], d_["text"]) for d_ in hubl]}
    ly = low - 3.0 * k
    lb = ly
    for j, (g_, head) in enumerate(R28MV_GROUPS):
        if keys[g_] or ents[g_]:
            lb = min(lb, r28mv_list(B, head, keys[g_], ents[g_], x + j * (cw + gap), ly, cw, k, L))
    crop_panel("proposal", x - 0.5 * k, lb - 0.5 * k, r[2] + 0.5 * k, top,
               u"How people will move · reach on foot, roads, crossings and hubs of the masterplan", crop_scale(ss),
               crop_legend(r28mv_base_leg()))
    low = lb - 0.5 * k
    if R2 and roads:                                      # P09.3: the index today and with the proposal
        low = r28mv_index_change(S, B, x, low - 8.0 * k, k, L, R2, roads)
    else:
        LOG.append("Index change: no street network with the masterplan (OSM) or no road, so no chart.")
    return low - 0.4 * U


# ------------------------------------------------------------ p.09 walk and car index, today and with the proposal (P09.3)
def r28mv_index_change(S, B, x, ytop, k, L, R2, roads):
    """v50 (MIRAQUA 28 Oct, P09.3; replaces the commercial spines map, which repeated p.07): the walk and car index
    today and with the proposal on each road of the masterplan and on the bus line (mv_line_index on the run with the
    proposal, R2: the length-weighted mean of the street pieces within MV_LINE_D of the line; 100 = the busiest piece
    today, per mode), as two small charts with one 0-100 axis each (today a ring, with the proposal a dot in the
    road's colour), the roads grouped by change and numbered as on the map; under them what the model leaves out:
    calmed and shared roads keep their cars and the bus line is not modelled, so their change comes only through the
    network. Crop drw_index_change, drawn for its width on the booklet page (bk_w). Returns the y below."""
    keys = ("walk_b", "walk_a", "car_b", "car_a")
    rows = [(d_, mv_line_index(R2, d_["P"], keys)) for d_ in roads]
    rank = dict((c_, j) for j, c_ in enumerate(R28MV_CHANGE_ORDER))
    rows.sort(key=lambda rv: (rank.get(rv[0]["ch"], len(rank)), rv[0]["n"]))
    LOG.append(u"Index change (walk today -> with, car today -> with): " + u"; ".join(
        u"{} {} -> {}, {} -> {}".format(d_["name"], *[u"n/a" if v.get(k_) is None else u"{:.0f}".format(v[k_])
                                                      for k_ in keys]) for d_, v in rows))
    h9, h75, h7 = bk_hk(9.0, k), bk_hk(7.5, k), bk_hk(7.0, k)
    W = S.F.w * 1000.0 / B_DEN                            # mm: as wide as the map
    PW, VW, PG = 70.0, 15.0, 6.0                          # mm: a chart's plot, its values, the gap between the two
    X2 = W - PW - VW
    X1 = X2 - PG - PW - VW
    vals = [v_ for d_, v in rows for v_ in v.values() if v_ is not None]
    vmax = max(100.0, 25.0 * math.ceil(max(vals or [0.0]) / 25.0))
    yb = ytop - 0.5 * k - h9
    wt = r28mv_draw_line(B, r28mv_lines(u"**Walk and car index**, today and with the proposal, on the masterplan's roads "
                                        u"{}".format(bcite(r28mv_src_mv())), 1e9, h9)[0], x, yb, h9, INK, L)
    sx = x + wt + 8.0 * k                                 # what the marks are
    r28mv_dot(B, sx, yb + 0.5 * h7, None, k, L, 62, True)
    B.text(u"today", sx + 1.6 * k, yb, h7, INK2, L, order=66, font=FONT_TITLE)
    sx += 1.6 * k + r28mv_tw(u"today", h7) + 4.0 * k
    r28mv_dot(B, sx, yb + 0.5 * h7, INK2, k, L, 62)
    B.text(u"with the proposal, in the road's colour", sx + 1.6 * k, yb, h7, INK2, L, order=66, font=FONT_TITLE)
    yh = yb - 5.5 * k
    B.text(u"Road · change", x + 4.2 * k, yh, h7, INK2, L, order=66, font=FONT_TITLE, bold=True)
    for X, lab in ((X1, u"Walking index"), (X2, u"Driving index")):
        B.text(lab, x + X * k, yh, h75, INK, L, order=66, font=FONT_TITLE, bold=True)
        B.text(u"today / with", x + (X + PW + 2.0) * k, yh, h7, INK2, L, order=66, font=FONT_TITLE)
    y0, rh = yh - 2.0 * k, 5.0 * k
    yend = y0 - len(rows) * rh
    for X in (X1, X2):                                    # the axis: light lines every 25, numbers under the rows
        for g_ in range(0, int(vmax) + 1, 25):
            gx = x + (X + PW * g_ / vmax) * k
            B.line([(gx, y0), (gx, yend)], mix(INK2, WHITE, 0.7), L, 60, bk_lw(0.12, k))
            t_ = u"{}".format(g_)
            B.text(t_, gx - 0.5 * r28mv_tw(t_, h7), yend - 1.2 * k - h7, h7, INK2, L, order=66, font=FONT_TITLE)
    na = False
    nmax = (X1 - 7.0) * k                                 # the name column's width
    for i, (d_, v) in enumerate(rows):
        yc = y0 - (i + 0.5) * rh
        r28mv_disc(B, x + 1.55 * k, yc, d_["n"], R28MV_MK["roads"], k, L, 64, r_mm=1.55)
        ln = r28mv_lines(u"**{}** · {}".format(d_["name"], d_["chlab"]), 1e9, h75)[0]
        hh = max(h7, min(h75, h75 * nmax / max(1e-9, r28mv_line_w(ln, h75))))
        r28mv_draw_line(B, r28mv_lines(u"**{}** · {}".format(d_["name"], d_["chlab"]), 1e9, hh)[0], x + 4.2 * k,
                        yc - 0.5 * hh, hh, INK, L)
        for X, kb, ka in ((X1, "walk_b", "walk_a"), (X2, "car_b", "car_a")):
            b_, a_ = v.get(kb), v.get(ka)
            if b_ is None or a_ is None:
                B.text(u"n/a", x + (X + PW + 2.0) * k, yc - 0.5 * h7, h7, INK2, L, order=66, font=FONT_TITLE)
                na = True
                continue
            xb, xa = x + (X + PW * min(b_, vmax) / vmax) * k, x + (X + PW * min(a_, vmax) / vmax) * k
            B.line([(xb, yc), (xa, yc)], mix(INK2, WHITE, 0.4), L, 61, bk_lw(0.45, k))
            r28mv_dot(B, xb, yc, None, k, L, 62, True)
            r28mv_dot(B, xa, yc, d_["col"], k, L, 62)
            vt = u"{:.0f} / ".format(b_) + (u"**{:.0f}**" if round(a_) != round(b_) else u"{:.0f}").format(a_)
            r28mv_draw_line(B, r28mv_lines(vt, 1e9, h75)[0], x + (X + PW + 2.0) * k, yc - 0.5 * h75, h75, INK, L)
    yn = yend - 1.2 * k - h7 - 4.0 * k - h75
    yn = r28mv_para(B, u"**Not modelled**: calmed and shared roads keep their cars and the bus line is not in the "
                       u"model, so their index moves only through the **network** (cars off the pedestrian roads, the "
                       u"crossings as walking links, the hubs as destinations).", x, yn, W * k, h75, INK2, L)
    yn = r28mv_para(B, u"**Index 100** = the busiest street piece today, per mode; a road = the mean of the street "
                       u"pieces within {:.0f} m of its line, by length{}".format(
                           MV_LINE_D, u"; n/a = none that close." if na else u"."), x, yn - 0.3 * h75, W * k, h75,
                    INK2, L)
    bot = yn + R28MV_LEAD * h75 - 0.5 * h75
    crop_panel("index_change", x - 0.5 * k, bot - 0.5 * k, x + (W + 0.5) * k, ytop,
               u"Walk and car index · today and with the proposal · roads of the masterplan")
    CROP_PANELS[-1]["bk_w"] = W + 1.0
    return bot - 0.5 * k


def mv_runs(S, R, key, F):
    """[(points, (class, value))] of map `key` along the walking (or driving) network, clipped to F."""
    pieces, IDX = R["pieces"], R["IDX"]
    if key.endswith("_d"):
        a_, b_ = IDX[key[:-2] + "_a"], IDX[key[:-2] + "_b"]
        vals = dict((i, a_.get(i, 0.0) - b_.get(i, 0.0)) for i in R["inside"])
    else:
        vals = IDX[key]
    net = ("car" if key.startswith("car") else "walk") + ("_a" if key.endswith(("_a", "_d")) else "_b")

    def val(pi):
        return (MV_CLASS.get(pieces[pi]["tags"].get("highway"), "lane"), round(vals.get(pi, 0.0), 1))
    return _runs(R["chains"][net], pieces, R["xy"], val, set(R["inside"]), F)


def draw_mv_streets(B, V, runs, L, order, scale=1.0, div=False, dmax=1.0):
    for P, (cls, v) in sorted(runs, key=lambda r: abs(r[1][1])):
        if div:
            if abs(v) < 0.05:
                continue
            col = mv_ramp(DIV, div_t(v, dmax))
        else:
            col = mv_ramp(SEQ, seq_t(v, 100.0))
        B.line(V.P(P), col, L, order, MV_W[cls] * scale)


def draw_how_people_use_it(S, B, x, y, w, U):
    """S2: how people move and what they reach (was 07 commercial spines, 09 civic constellations, diagrams D3, D5, D7
    and the movement script's panels). v46 (Prompt 3, p.8, analysis): the whole site frame at 1:10,000 on the frame's
    axes in the masterplan's base, the scale bar and north arrow under it; no proposed spine or stops (analysis
    only); walking and driving today as their own maps at the same scale under it (draw_mv_today). Returns the y below."""
    L = "LU_BOARD::HowPeopleUseIt"
    F = S.F
    B.text("HOW PEOPLE USE IT · STREETS · SHOPS · SERVICES · WALKS", x, y, 1.05 * U, INK, L,
           font=FONT_TITLE, bold=True)                    # v38: keywords
    V, k, ss, r = b_view(F, x, y - 1.2 * U, U)            # v46: the site frame at 1:10,000, as every theme-B map
    mw = F.w * ss
    CB = ClipB(B, r)
    MV = movement(S)
    R = MV.get("R")
    try:
        DG, ctx = diagram_ctx(S)
        D7 = DG["d7_links"](ctx) if ctx.areas else None
    except Exception:
        LOG.append("WARNING: services and walks not drawn:\n" + traceback.format_exc())
        DG, ctx, D7 = None, None, None
    # the masterplan base, crisp; uses in colour (v46)
    B.fill([rect(*r)], WHITE, L, 1)
    use_cats = ("commercial", "mixed", "institutional", "religious")
    b_base(S, CB, V, k, L, lambda u: CAT[u["cat"]][1] if u["cat"] in use_cats else MPL["bld"])
    # commerce spines: a broad pale band in the street, under the buildings
    cc = CAT["commercial"][1]
    for g in S.corr_primary:
        for P in g["Ps"]:
            CB.line(V.P(P), mix(cc, WHITE, 0.45), L, 9, bk_lw(1.8, k))
    for g in S.corr_secondary:
        for P in g["Ps"]:
            for d in dashes(V.P(P), 3.0 * k, 1.8 * k):
                CB.line(d, mix(cc, WHITE, 0.45), L, 9, bk_lw(1.1, k))
    # streets: line width = OSM class, colour = combined movement potential today
    if R:
        draw_mv_streets(CB, V, mv_runs(S, R, "comb_b", F), L, 14)
    # v46 (Prompt 3): the proposed streamside spine and its stops are no longer drawn here (an analysis map)
    # civic constellations
    hc = mix(CAT["institutional"][1], INK, 0.2)
    for cl in S.clusters:
        for run in F.clip_line(cl["P"] + [cl["P"][0]]):
            for d in dashes(V.P(run), 2.0 * k, 1.4 * k):
                CB.line(d, hc, L, 16, bk_lw(0.18, k))
    # services (Overture places, as D5) and the walks to the nearest of each function (as D7)
    fcol = dict((f, hexrgb(c)) for f, let, c, lab in WALK_FUN)
    n_pl = {}
    if ctx is not None:
        for px_, py_, f, nm, conf, cat in [p[:6] for p in ctx.places]:
            if F.inside(px_, py_):
                n_pl[f] = n_pl.get(f, 0) + 1
                cx, cy = V.p(px_, py_)
                CB.fill([circle_pts(cx, cy, 0.45 * k, 8)], fcol.get(f, INK2), L, 30)
    walk_c = mix(INK, PAPER, 0.15)
    dest = {}
    if D7:
        for k_, best in D7["res"].items():
            for f, r_ in best.items():
                if r_["pts"]:
                    for run in F.clip_line(r_["pts"]):
                        for d in dashes(V.P(run), 0.6 * k, 0.6 * k):
                            CB.line(d, walk_c, L, 32, bk_lw(0.16, k))
                dest[(f, round(r_["x"]), round(r_["y"]))] = r_
        rr = 1.9 * k
        let_of = dict((f, let) for f, let, c, lab in WALK_FUN)
        for (f, _, _), r_ in dest.items():
            if F.inside(r_["x"], r_["y"]):
                px, py = V.p(r_["x"], r_["y"])
                roundel(B, px, py, rr, let_of.get(f, "?"), fcol.get(f, INK), (255, 255, 255), L, order=62)
        for nm, sh, a in stage_areas(S):                    # where each walk starts: a name, never an outline
            cx, cy = shoelace(a["P"])[1:]
            px, py = V.p(cx, cy)                          # v40: plain text, no white box (Aras 25 Oct 21:41)
            CB.text(nm, px, py, bk_hk(8.0, k), INK, L, order=64, font=FONT_TITLE, bold=True, align="C")
    draw_map_annotations(S, B, V, U, rh=bk_hk(8.0, k))
    b_frame(B, r, k, L)
    foot = b_foot(B, F, x, r[1], ss, k, L)                # v46: under the map, never on it
    crop_r = (x - 0.5 * k, foot - 0.5 * k, r[2] + 0.5 * k, r[3] + 0.5 * k)    # the booklet crop of the plan
    r28mv_note_top(S, B, crop_r, k, L, MV, n_pl)          # v50 (MIRAQUA 28 Oct, P07.2): drw_mv_note_1 beside the plan
    yy = foot - 3.0 * U
    # walking and driving today, only the key streets in colour and named (v44, Aras 27 Oct: "highlight only the key
    # axes and roads"); v46: each its own map at the theme's one scale, stacked under the plan
    if R:
        # v50 (MIRAQUA 28 Oct, P07.3): the index on every street piece, the busiest named (draw_mv_today, 15i)
        for key_, title, cap in (("walk_b", "WALKING TODAY", u"Walking today · index on every street piece · the {} "
                                                             u"busiest named"),
                                 ("car_b", "DRIVING TODAY", u"Driving today · index on every street piece · the {} "
                                                            u"busiest named")):
            yy = draw_mv_today(S, B, x, yy, U, R, MV, key_, title, cap) - 2.0 * U
    # walking lengths from each working area (D7), as a small table
    if D7:
        st = [(nm, sh) for nm, sh, a in stage_areas(S) if nm in D7["res"]]
        cw0, cw = 9.0 * U, (mw - 9.0 * U) / max(1, len(st))
        h = 0.36 * U
        r_walk = bcite("Commerce: shopfronts within 30 m of a street (survey, OSM, Overture). Services: Overture/Meta "
                       "places. Walks: the shortest along OSM streets and footways from the edge of each working area, "
                       "rounded to 10 m.")
        B.text("WALK TO THE NEAREST · m along OSM streets and footways " + r_walk, V.X0, yy, 0.42 * U, INK, L,
               font=FONT_TITLE, bold=True)
        yy -= 1.0 * U
        for j, (nm, sh) in enumerate(st):
            B.text("from the " + nm, V.X0 + cw0 + j * cw, yy, h, INK2, L, bold=True)
        yy -= 0.85 * U
        # v33 (Step 4): the climb of every walk on the survey terrain, instead of an axonometric of S2
        walks = [D7["res"].get(nm, {}).get(f) for f, let, c, lab in WALK_FUN for nm, sh in st]
        lines_ = [r["pts"] if r and r["pts"] and not r["inside"] else [] for r in walks]
        ups = DG["walk_climbs"](ctx, lines_ + [p["pts"] for p in D7["pairs"]])
        climb = dict((id(r), u_) for r, u_ in zip(walks, ups) if r)
        for f, let, c, lab in WALK_FUN:
            roundel(B, V.X0 + 0.3 * U, yy + 0.15 * U, 0.3 * U, let, fcol[f], (255, 255, 255), L, order=62)
            B.text(lab, V.X0 + 0.9 * U, yy, h, INK, L)
            for j, (nm, sh) in enumerate(st):
                r = D7["res"].get(nm, {}).get(f)
                up = climb.get(id(r)) if r else None
                t_ = "none in reach" if not r else ("inside" if r["inside"] else DG["m10"](r["L"]) + (
                    ", {} m up".format(up) if up and up >= 5 else ""))
                B.text(t_, V.X0 + cw0 + j * cw, yy, h, INK, L)
            yy -= 0.75 * U
        ups = [u_ for u_, ln in zip(ups, lines_ + [p["pts"] for p in D7["pairs"]]) if u_ is not None and ln]
        yy -= 0.4 * U
    # legend (v38: short names; the method sentences are entries of the Sources key, cited [n])
    r_mv = bcite("Movement potential = the number of shortest routes between every building and every everyday "
                 "destination within {:.0f} m on foot or {:.0f} min by car that use the street (OSM network, Overture "
                 "places, the method of bergama_movement v1); index 100 = the busiest street piece in the frame. A count "
                 "of routes, not of people or vehicles: no count exists for these streets.".format(
                     MV_OPT["r_walk"], MV_OPT["t_car"] / 60.0)) if R else ""
    r_com = bcite("Commerce: shopfronts within 30 m of a street (survey, OSM, Overture). Services: Overture/Meta "
                  "places. Walks: the shortest along OSM streets and footways from the edge of each working area, "
                  "rounded to 10 m.")
    leg = [("hdr", None, "STREETS · COLOUR = MOVEMENT POTENTIAL · WIDTH = OSM CLASS " + r_mv)]
    if R:
        for v in (2, 10, 25, 50, 100):
            leg.append(("thick", mv_ramp(SEQ, seq_t(v, 100.0)), "Index {}".format(v)))
    leg += [("hdr", None, "SHOPS AND CIVIC LIFE " + r_com),
            ("thick", mix(cc, WHITE, 0.45), "Primary commercial spine"),
            ("dash", mix(cc, WHITE, 0.45), "Secondary commercial spine")]
    leg += [("box", CAT["commercial"][1], "Commerce"), ("box", CAT["mixed"][1], "Mixed use"),
            ("box", CAT["institutional"][1], "Civic"), ("box", CAT["religious"][1], "Sacred"),
            ("dash", hc, "Constellation · 3+ in 100 m")]
    if ctx is not None:
        leg += [("hdr", None, "SERVICES AND WALKS " + r_com)]
        for f, let, c, lab in WALK_FUN:
            if n_pl.get(f):
                leg.append(("dot", fcol[f], "{} · {} places".format(lab, n_pl[f])))
        leg.append(("dash", walk_c, "Walk to the nearest (letter at the place)"))
    ly = draw_legend_items(B, leg, x, yy - 0.4 * U, mw, U, L, h=0.4)
    crop_panel("movement", crop_r[0], crop_r[1], crop_r[2], crop_r[3], u"How people use it · streets, shops, services",
               crop_scale(ss), crop_legend(leg + B_BASE_LEG))    # v40: the booklet crop of the plan (v46: 1:10,000);
    #                                                       v49.1 (Prompt 8): + the base's tones, as on p.10
    # v38 (visual first): what the numbers say as a tile and two mini-charts (were caption sentences); computed above,
    # nothing measured on the street
    cy0 = ly - 0.4 * U
    low = cy0
    cx = x
    gw, gh = min(30.0 * U, (mw - 4.0 * U) / 3.0), 7.0 * U
    tfill = mix(PAPER, (255, 255, 255), 0.5)
    if R and MV.get("rows"):
        top = MV["rows"][0]
        low = min(low, vis_tiles(B, cx, cy0, gw, [
            ("road", "BUSIEST STREET · WALK + DRIVE", "{} · index {:.0f}".format(top["name"], top["comb_b"]), r_mv)],
            U, L, h=1.3, ink=INK, grey=INK2, fill=tfill, rule=FAINT))
        cx += gw + 2.0 * U
        rw = MV["rho"].get("walk_b")
        big = [r_ for r_ in (MV.get("big") or []) if r_.get("walk_b") is not None]
        if rw is not None and big:                        # scatter: shops per street against walking potential
            B.text("SHOPS vs WALKING POTENTIAL · Spearman {:.2f} {}".format(rw, r_com), cx, cy0 - 0.4 * U, 0.4 * U,
                   INK, L, font=FONT_TITLE, bold=True)
            px0, py0 = cx + 1.4 * U, cy0 - 1.0 * U - gh
            pw_ = gw - 1.4 * U
            xm = max(100.0, max(r_["walk_b"] for r_ in big))
            ym = max(1.0, max(r_["shops"] for r_ in big))
            B.fill([rect(px0, py0, px0 + pw_, py0 + gh)], tfill, L, 20)
            B.line(rect(px0, py0, px0 + pw_, py0 + gh) + [(px0, py0)], FAINT, L, 21, 0.04)
            for r_ in big:
                B.fill([circle_pts(px0 + pw_ * r_["walk_b"] / xm, py0 + gh * r_["shops"] / ym, 0.12 * U, 8)],
                       mix(CAT["commercial"][1], INK, 0.2), L, 22)
            B.text("0", px0, py0 - 0.45 * U, 0.28 * U, INK2, L, align="C")
            B.text("{:.0f}".format(xm), px0 + pw_, py0 - 0.45 * U, 0.28 * U, INK2, L, align="C")
            B.text("{:.0f}".format(ym), px0 - 0.2 * U, py0 + gh - 0.28 * U, 0.28 * U, INK2, L, align="R")
            B.text("walking index · {} streets of 50 m+".format(len(MV["big"])), px0 + pw_ / 2.0, py0 - 0.95 * U,
                   0.28 * U, INK2, L, align="C")
            B.text("shops", px0 - 0.2 * U, py0 + 0.1 * U, 0.28 * U, INK2, L, align="R")
            crop_panel("shops_vs_walking", cx - 0.6 * U, py0 - 1.3 * U, cx + gw, py0 + gh + 0.1 * U,
                       u"More walkers, more shops · Spearman {:.2f}".format(rw))    # v40
            low = min(low, py0 - 1.4 * U)
            cx += gw + 2.0 * U
    if D7 and ups:                                        # the climb of every walk, as bars
        mx = max(ups)
        r_cl = bcite("Climb on the survey terrain: rises summed every {:.0f} m, rounded to 5 m; calculated. The table "
                     "carries the heights that matter for these walks, so S2 has no axonometric.".format(DG["CLIMB_STEP"]))
        B.text("CLIMB OF THE WALKS · " + ("none 5 m or more" if mx < 5 else "most {} m up".format(mx)) + " " + r_cl,
               cx, cy0 - 0.4 * U, 0.4 * U, INK, L, font=FONT_TITLE, bold=True)
        vv = sorted(ups, reverse=True)
        bx0, by0 = cx + 1.4 * U, cy0 - 1.0 * U - gh
        bw_ = (gw - 1.4 * U) / float(len(vv))
        ym = max(5.0, float(mx))
        for i, u_ in enumerate(vv):
            B.fill([rect(bx0 + i * bw_ + 0.1 * bw_, by0, bx0 + (i + 0.9) * bw_, by0 + gh * u_ / ym)],
                   INK2 if u_ >= 5 else FAINT, L, 21)
        for dd in dashes([(bx0, by0 + gh * 5.0 / ym), (bx0 + gw - 1.4 * U, by0 + gh * 5.0 / ym)], 0.3 * U, 0.2 * U):
            B.line(dd, MARK_C, L, 22, 0.06)
        B.text("5 m", bx0 - 0.2 * U, by0 + gh * 5.0 / ym - 0.12 * U, 0.28 * U, MARK_C, L, align="R")
        B.line([(bx0, by0), (bx0 + gw - 1.4 * U, by0)], INK2, L, 22, 0.05)
        B.text("walks, steepest first · m up", bx0 + (gw - 1.4 * U) / 2.0, by0 - 0.55 * U, 0.28 * U, INK2, L, align="C")
        crop_panel("walk_climb", cx, by0 - 0.9 * U, cx + gw, by0 + gh + 0.1 * U, u"Climb of the walks")     # v40
        low = min(low, by0 - 1.0 * U)
    return low - 0.4 * U
