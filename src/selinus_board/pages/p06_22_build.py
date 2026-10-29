# p.06 / p.22 the edge build and its filter (split from parts/15c_review_pages.py, parts/15e_v45_pages.py, parts/15k_r28_edge.py on 29 Oct 2026; moved unchanged)


def edge_shares(S):
    """v42: {edge type: % of the bank length}, and the % walled and embanked (the key question's measure)."""
    tot = sum(S.edge_len.values())
    if tot <= 0:
        return {}, 0.0, 0.0, 0.0
    return (dict((k, 100.0 * v / tot) for k, v in S.edge_len.items()), 100.0 * S.walled_len / tot,
            100.0 * getattr(S, "embanked_len", 0.0) / tot, tot)


def photo_fov(f35):
    """v45: a photo's horizontal angle of view (radians) at 35 mm-equivalent focal length f35: the 4:3 frame's width
    is 34.6 mm of the 43.27 mm reference diagonal (the data pack's photos keep the full 4:3 frame)."""
    return 2.0 * math.atan(34.6 / (2.0 * f35))


def eb_caption(it, width, h):
    """v45: a photo's keyword caption on ONE line at height h: middle keywords left out until it fits width (real
    Helvetica runs about 0.72 x the capital height per character)."""
    parts = photo_caption(it).split(u" · ")
    est = (lambda t: len(t) * 0.72 * h)
    while len(parts) > 2 and est(u" · ".join(parts)) > width:
        del parts[-2]
    t = u" · ".join(parts)
    while len(t) > 6 and est(t) > width:
        t = t[:-2].rstrip(u" ·") + u"…"
    return t


def r28e_rich(B, s, x, y, h, col, L, order=40):
    """G5: one line with **bold** runs from baseline y; returns its width"""
    ln = r28mv_lines(s, 1e12, h)
    return r28mv_draw_line(B, ln[0], x, y, h, col, L, order) if ln else 0.0


def r28e_streets(S):
    """P06.1: the named streets of the strip (OpenStreetMap names of S.roads): those with a main-road class
    (MAIN_ROADS) first, then the longest, each R28E_STREET_MIN or more inside the frame, at most R28E_N_STREET:
    [(name, x, y)] at the middle of its longest piece"""
    by = {}
    for r_ in S.roads:
        t = r_.get("tags") or {}
        nm = u" ".join((t.get("name") or u"").split())
        if not nm or r_.get("L", 0.0) <= 0.0 or len(r_["P"]) < 2:
            continue
        e = by.setdefault(nm, dict(L=0.0, main=False, best=None))
        e["L"] += r_["L"]
        e["main"] = e["main"] or t.get("highway") in MAIN_ROADS
        if e["best"] is None or r_["L"] > e["best"]["L"]:
            e["best"] = r_
    names = sorted((nm for nm, e in by.items() if e["L"] >= R28E_STREET_MIN),
                   key=lambda nm: (not by[nm]["main"], -by[nm]["L"]))
    out = []
    for nm in names[:R28E_N_STREET]:
        P = by[nm]["best"]["P"]
        q = pl_point_at(P, 0.5 * pl_length(P))[0]
        out.append((nm, q[0], q[1]))
    return out


def r28e_heritage(S):
    """P06.1: the heritage names of the strip: the monuments' and sacred buildings' own names (u["proper"]: survey or
    OpenStreetMap), the largest first, then named heritage points (OpenStreetMap, places) standing free; one label a
    place (a name, or the same first word within 60 m, once), at most R28E_N_HER: [(name, x, y)]"""
    F = S.F
    cand = sorted([(u["A"], u["proper"], interior_point(u["parts"][0])) for u in S.bld
                   if u.get("fabric") in ("monument", "sacred") and u.get("proper")], key=lambda c_: -c_[0])
    cand += [(0.0, p_["name"], (p_["x"], p_["y"])) for p_ in getattr(S, "pois", None) or []
             if p_.get("her") and not p_.get("in_bld") and proper_name(p_.get("name") or u"")]
    out = []
    for a_, nm, (x_, y_) in cand:
        nm = u" ".join(nm.split())
        w0 = nm.split()[0].lower()
        if not F.inside(x_, y_) or any(nm == o[0] or (o[0].split()[0].lower() == w0 and
                                                      math.hypot(o[1] - x_, o[2] - y_) < 60.0) for o in out):
            continue
        out.append((nm, x_, y_))
        if len(out) >= R28E_N_HER:
            break
    return out


def r28e_mahalle(S):
    """P06.1: the mahalle names of the strip: OpenStreetMap boundary=administrative, admin_level 8 relations (their
    outer ways joined into closed rings, cut to the frame), each named at an inside point of its largest piece in the
    frame when that holds R28E_MAH_MIN or more: [(name without "Mahallesi", x, y)]"""
    m = r28e_memo(S)
    if "mahalle" in m:
        return m["mahalle"]
    out, F = [], S.F
    osm = getattr(S, "osm", None) or {}
    ways, Pj = osm.get("ways") or {}, osm.get("P")
    for mem, tags in osm.get("rels") or []:
        nm = u" ".join((tags.get("name") or u"").split())
        if tags.get("boundary") != "administrative" or str(tags.get("admin_level")) != "8" or not nm or Pj is None:
            continue
        lines_ = []
        for ref, role in mem:
            if role in ("outer", "", None) and ref in ways:
                pts = [q for q in (Pj(n_) for n_ in ways[ref][0]) if q]
                if len(pts) >= 2:
                    lines_.append(pts)
        best = None
        for R_ in chain_segments(lines_, 0.05):
            if len(R_) < 4 or math.hypot(R_[0][0] - R_[-1][0], R_[0][1] - R_[-1][1]) > 1.0:
                continue
            Q = F.clip_poly(R_[:-1])
            a_ = shoelace(Q)[0] if Q else 0.0
            if a_ >= R28E_MAH_MIN and (best is None or a_ > best[0]):
                best = (a_, Q)
        if best is not None:
            for suf in (u" Mahallesi", u" Mahalle"):
                if nm.endswith(suf):
                    nm = nm[:-len(suf)].strip()
            x_, y_ = interior_point(best[1])
            out.append((nm, x_, y_))
    m["mahalle"] = out
    LOG.append(u"Mahalle names on the stream edge plan (OpenStreetMap, admin_level 8): {}.".format(
        u", ".join(nm for nm, x_, y_ in out) or u"none (no closed boundary with 2 ha or more in the frame)"))
    return out


def r28e_names(S, V, k):
    """P06.1: the strip's context names as r28e_place items, 7 pt: the stream (always shown), heritage, main
    streets, mahalle (each may be dropped where nothing is free)"""
    F = S.F
    h = bk_hk(7.0, k)
    out = []
    rl = getattr(S, "river_label", None)
    if rl and F.inside(rl[0], rl[1]):
        px, py = V.p(rl[0], rl[1])
        out.append(dict(x=px, y=py, lines=[(rl[3], False)], h=h, col=MPL["water_edge"], rank=0, italic=True))
    for nm, x_, y_ in r28e_heritage(S):
        px, py = V.p(x_, y_)
        out.append(dict(x=px, y=py, lines=[(nm, False)], h=h, col=R28E_HER_TXT, rank=1))
    for nm, x_, y_ in r28e_streets(S):
        px, py = V.p(x_, y_)
        out.append(dict(x=px, y=py, lines=[(nm, False)], h=h, col=INK, rank=1))
    for nm, x_, y_ in r28e_mahalle(S):
        px, py = V.p(x_, y_)
        out.append(dict(x=px, y=py, lines=[(tr_upper(nm), False)], h=h, col=INK2, rank=1, centre=True))
    return out


def r28e_place(B, items, taken, bounds, k, L, segs=(), order=66):
    """G4 (common/label_place.py): the labels items [dict(x, y (board units), lines [(text, bold)], h (capital
    height), col, rank (0 always shown, 1 may be dropped), centre (an area's name: on its point when that is free),
    italic)] placed clear of each other, of the boxes in taken (symbols) and of the lines segs [(p, q)], inside
    bounds; a label set off its point gets a thin leader. Worked in booklet mm; never smaller than drawn (7 pt).
    Returns the texts of the labels dropped; taken grows."""
    mm = 1.0 / k
    pad, lead = 0.3, 1.4
    tk = [tuple(v * mm for v in b) for b in taken]
    bd = tuple(v * mm for v in bounds) if bounds else None
    sg = [((p[0] * mm, p[1] * mm), (q[0] * mm, q[1] * mm)) for p, q in segs]

    def size(it):
        h = it["h"] * mm
        return (max(r28mv_tw(t, h, b) for t, b in it["lines"]) + 2.0 * pad,
                h * (1.0 + lead * (len(it["lines"]) - 1)) + 2.0 * pad)

    def free(b):
        return ((bd is None or (bd[0] <= b[0] and b[2] <= bd[2] and bd[1] <= b[1] and b[3] <= bd[3])) and
                not any(lp_hit(b, t) for t in tk) and not any(_lp_seg_box(p, q, b) for p, q in sg))

    placed = {}

    def run(idx):
        sub = []
        for i in idx:
            wh_ = size(items[i])
            sub.append(dict(x=items[i]["x"] * mm, y=items[i]["y"] * mm, wh=(lambda f, s_=wh_: s_),
                            rank=items[i].get("rank", 1)))
        for j, got in place_labels_all(sub, tk, bd, sg, sizes=(1.0,), pad=0.2).items():
            placed[idx[j]] = (got[0], got[1])

    run([i for i, it in enumerate(items) if it.get("rank", 1) == 0])
    rest = []
    for i, it in enumerate(items):
        if it.get("rank", 1) == 0:
            continue
        if it.get("centre"):
            w_, h_ = size(it)
            ax, ay = it["x"] * mm, it["y"] * mm
            b = (ax - 0.5 * w_, ay - 0.5 * h_, ax + 0.5 * w_, ay + 0.5 * h_)
            if free(b):
                tk.append(b)
                placed[i] = (b, False)
                continue
        rest.append(i)
    run(rest)
    dropped = []
    for i, it in enumerate(items):
        if i not in placed:
            dropped.append(u" ".join(t for t, b_ in it["lines"]))
            continue
        b, far = placed[i]
        x0, y1 = b[0] * k, b[3] * k
        if far:
            e = lp_leader_end(b, (it["x"] * mm, it["y"] * mm))
            B.line([(it["x"], it["y"]), (e[0] * k, e[1] * k)], it["col"], L, order - 1, bk_lw(0.1, k))
        h = it["h"]
        yl = y1 - pad * k - h
        for t, bold in it["lines"]:
            B.text(t, x0 + pad * k, yl, h, it["col"], L, order=order, font=FONT_TITLE, bold=bold,
                   italic=it.get("italic", False))
            yl -= lead * h
    taken[:] = [tuple(v * k for v in b) for b in tk]
    return dropped


def r28e_strip(S, B, x, yt, k, L, photos=()):
    """v50 (G7, P06.1, P06.4): the whole frame as ONE strip at 1:10,000, its top-left corner at (x, yt): the base,
    the edge every 4 m on both banks (walled and embanked marked), bridges K1-K6 as bars with their names, the photo
    viewpoints (numbered discs, view cones), the context names (G4), the frame's line. Returns (View, board units
    per metre, the strip's rectangle, the labels dropped)."""
    F = S.F
    ss = 1000.0 * k / R28E_DEN
    V = View(F, ss, x, yt)
    r = (x, yt - F.h * ss, x + F.w * ss, yt)
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 1)
    r28e_base(S, CB, V, k, L)
    for typ, pts in getattr(S, "edge_runs", []):          # the edge every 4 m, both banks
        CB.line(V.P(pts), EDGE[typ][1], L, 40, bk_lw(0.7, k))
    for pts in getattr(S, "wall_runs", []):
        for d in dashes(V.P(pts), 1.0 * k, 0.8 * k):
            CB.line(d, WHITE, L, 41, bk_lw(0.3, k))
    for pts in getattr(S, "bank_runs", []):
        for d in dashes(V.P(pts), 0.2 * k, 1.0 * k):
            CB.line(d, WHITE, L, 41, bk_lw(0.3, k))
    h7 = bk_hk(7.0, k)
    taken, items = [], []
    for kk, nm, bx, by in BRIDGES_K:                      # the six crossings: a bar across the stream, K and name
        if not F.inside(bx, by):
            continue
        px, py = V.p(bx, by)
        nrm = stream_normal(S, bx, by) or (0.0, 1.0)
        a_ = V.p(bx + nrm[0], by + nrm[1])
        ln = math.hypot(a_[0] - px, a_[1] - py) or 1.0
        e = ((a_[0] - px) / ln * 1.6 * k, (a_[1] - py) / ln * 1.6 * k)
        CB.line([(px - e[0], py - e[1]), (px + e[0], py + e[1])], MPL["ink_dark"], L, 45, bk_lw(0.6, k))
        taken.append((px - 1.6 * k, py - 1.6 * k, px + 1.6 * k, py + 1.6 * k))
        items.append(dict(x=px, y=py, lines=[(kk, True), (nm, False)], h=h7, col=INK, rank=0))
    rd = 1.6 * k                                          # a viewpoint's disc; its number 7 pt
    for j, (p, it) in enumerate(photos):                  # viewpoints: cone from the camera, disc behind it
        if not F.inside(it["x"], it["y"]):
            continue
        px, py = V.p(it["x"], it["y"])
        brg, f35 = PHOTO_VIEW.get(it.get("file", "").split(".")[0], (None, None))
        dx, dy, fov = 0.0, 0.0, 0.0
        if brg is not None:                               # bearing from true north, clockwise; survey y = north
            fov = photo_fov(f35)
            tip = V.p(it["x"] + math.sin(math.radians(brg)) * EB_CONE_M,
                      it["y"] + math.cos(math.radians(brg)) * EB_CONE_M)
            ln = math.hypot(tip[0] - px, tip[1] - py) or 1.0
            dx, dy = (tip[0] - px) / ln, (tip[1] - py) / ln
            ac, R_ = math.atan2(dy, dx), EB_CONE_M * ss
            arc = [(px + R_ * math.cos(ac + fov * (t_ / 12.0 - 0.5)), py + R_ * math.sin(ac + fov * (t_ / 12.0 - 0.5)))
                   for t_ in range(13)]
            CB.line([arc[-1], (px, py), arc[0]] + arc[1:], INK, L, 50, bk_lw(0.2, k))
            cq = arc + [(px, py)]
            taken.append((min(q[0] for q in cq), min(q[1] for q in cq), max(q[0] for q in cq), max(q[1] for q in cq)))
        B.fill([circle_pts(px, py, 0.4 * k, 10)], INK, L, 51)
        spot = None
        back = math.atan2(-dy, -dx) if brg is not None else 0.0
        for far in (1.0, 1.8, 2.6):
            for a in range(12):
                ang = back + (a + 1) // 2 * (1 if a % 2 else -1) * math.pi / 6.0
                dd = far * (rd + 0.8 * k)
                if brg is not None and dd <= EB_CONE_M * ss + rd:
                    off = abs((ang - math.atan2(dy, dx) + math.pi) % (2.0 * math.pi) - math.pi)
                    if off < 0.5 * fov + math.radians(12.0):
                        continue                          # never on its own cone
                cx_, cy_ = px + dd * math.cos(ang), py + dd * math.sin(ang)
                b = (cx_ - rd, cy_ - rd, cx_ + rd, cy_ + rd)
                own = [t_ for t_ in taken if not (t_[0] <= px <= t_[2] and t_[1] <= py <= t_[3])]   # not its own cone
                if r[0] <= b[0] and b[2] <= r[2] and r[1] <= b[1] and b[3] <= r[3] and not _hit(b, own):
                    spot = (cx_, cy_, b)
                    break
            if spot:
                break
        if spot is None:
            spot = (px - (rd + 0.8 * k), py, (px - 2 * rd - 0.8 * k, py - rd, px - 0.8 * k, py + rd))
            LOG.append("Stream edge plan: photo {} has no free place for its number; drawn beside it.".format(j + 1))
        cx_, cy_, b = spot
        B.line([(px, py), (cx_, cy_)], INK, L, 59, bk_lw(0.15, k))
        B.fill([circle_pts(cx_, cy_, rd, 24)], INK, L, 60)
        B.text(str(j + 1), cx_, cy_, h7, WHITE, L, order=61, font=FONT_TITLE, bold=True, align="MC")
        taken.append(b)
    items += r28e_names(S, V, k)
    segs = []                                             # labels never sit on the stream's centre line
    for P in getattr(S, "selinus", None) or []:
        Q = V.P(dp_simplify(P, 15.0))
        segs += list(zip(Q[:-1], Q[1:]))
    dropped = r28e_place(B, items, taken, (r[0] + 0.5 * k, r[1] + 0.5 * k, r[2] - 0.5 * k, r[3] - 0.5 * k), k, L,
                         segs)
    B.line(rect(*r) + [(r[0], r[1])], INK, L, 70, bk_lw(0.25, k))
    return V, ss, r, dropped


# ------------------------------------------------------------ the key and the panels beside the strip
def r28e_swatch(B, kind, ref, x, y, k, L, w=6.0, h=2.4, order=20):
    """a key sample w x h booklet mm, its top-left corner at (x, y): box (fill ref), osm (a building with the
    OpenStreetMap footprint's thin outline), her (heritage building), hatch / hatchline (R28_BUILD_HATCH key ref: tint
    and hatch as the strip / the hatch alone), line (ref = (colour, mm)), dash (ref = colour: the covered course),
    study (G8), contour (a 10 m and a 5 m line), bridge (a bar across the stream), edge (the six edge colours),
    walled / embanked (the bank marks), cone (a viewpoint), frame (the analysis frame's line), note (results needed)"""
    w, h = w * k, h * k
    sw_ = rect(x, y - h, x + w, y)
    ym = y - 0.5 * h
    if kind == "box":
        B.fill([sw_], ref, L, order)
    elif kind == "osm":
        B.fill([sw_], R28E_BLD, L, order)
        B.line(sw_ + [sw_[0]], R28E_OSM_EDGE, L, order + 1, bk_lw(0.08, k))
    elif kind == "her":
        B.fill([sw_], MPL["her"], L, order)
        B.line(sw_ + [sw_[0]], MPL["her_edge"], L, order + 1, bk_lw(0.12, k))
    elif kind in ("hatch", "hatchline"):
        lab, col, ang = R28E_HATCH[ref]
        if kind == "hatch":
            B.fill([sw_], mix(col, WHITE, R28E_TINT), L, order)
        B.hatch([sw_], col, L, order + 1, R28E_HATCH_MM[0] * k, math.radians(ang), bk_lw(R28E_HATCH_MM[1], k))
        B.line(sw_ + [sw_[0]], col, L, order + 2, bk_lw(0.1, k))
    elif kind == "line":
        B.line([(x, ym), (x + w, ym)], ref[0], L, order, bk_lw(ref[1], k))
    elif kind == "dash":
        for d in dashes([(x, ym), (x + w, ym)], 1.6 * k, 0.9 * k):
            B.line(d, ref, L, order, bk_lw(0.3, k))
    elif kind == "study":
        st = R28_STUDY_LINE
        for d in r28_pattern([(x, ym), (x + w, ym)], [m_ * k for m_ in st["dash_mm"]]):
            B.line(d, C(st["colour"]), L, order, bk_lw(st["width_mm"], k))
    elif kind == "contour":
        B.line([(x, ym + 0.6 * k), (x + w, ym + 0.6 * k)], R28E_CONTOUR, L, order, bk_lw(R28E_CONTOUR_W[1], k))
        B.line([(x, ym - 0.6 * k), (x + w, ym - 0.6 * k)], R28E_CONTOUR, L, order, bk_lw(R28E_CONTOUR_W[0], k))
    elif kind == "bridge":
        B.fill([rect(x, ym - 0.7 * k, x + w, ym + 0.7 * k)], MPL["water"], L, order)
        B.line([(x + 0.5 * w, y), (x + 0.5 * w, y - h)], MPL["ink_dark"], L, order + 1, bk_lw(0.6, k))
    elif kind == "edge":
        n_ = len(EDGE_ORDER)
        for i, k_ in enumerate(EDGE_ORDER):
            B.line([(x + i * w / n_, ym), (x + (i + 1) * w / n_, ym)], EDGE[k_][1], L, order, bk_lw(0.7, k))
    elif kind in ("walled", "embanked"):
        B.line([(x, ym), (x + w, ym)], INK2, L, order, bk_lw(0.7, k))
        dd = (1.0, 0.8) if kind == "walled" else (0.2, 1.0)
        for d in dashes([(x, ym), (x + w, ym)], dd[0] * k, dd[1] * k):
            B.line(d, WHITE, L, order + 1, bk_lw(0.3, k))
    elif kind == "cone":
        B.line([(x + w, y), (x + 0.8 * k, ym), (x + w, y - h)], INK, L, order, bk_lw(0.2, k))
        B.fill([circle_pts(x + 0.8 * k, ym, 0.4 * k, 10)], INK, L, order + 1)
    elif kind == "frame":
        B.line(sw_ + [sw_[0]], INK, L, order, bk_lw(0.25, k))
    elif kind == "note":
        B.line(sw_ + [sw_[0]], MARK_C, L, order, bk_lw(0.2, k))


def r28e_key(B, rows, x, y, ncol, colw, k, L):
    """the map's key (P06.2, P06.3: it draws the hatches and outlined fills the booklet's legend cannot), rows
    [(kind, ref, label)] in ncol columns colw wide, filled column by column from (x, y) (top), 7 pt. Returns the y
    under it."""
    pitch = 3.3 * k
    nrow = max(1, (len(rows) + ncol - 1) // ncol)
    h7 = bk_hk(7.0, k)
    for i, (kind, ref, lab) in enumerate(rows):
        lx, ly = x + (i // nrow) * colw, y - (i % nrow) * pitch
        r28e_swatch(B, kind, ref, lx, ly, k, L)
        B.text(lab, lx + 7.0 * k, ly - 2.4 * k + 0.4 * k, h7, INK, L, font=FONT_TITLE)
    return y - nrow * pitch


def r28e_key_rows(photos=True):
    """the stream edge plan's key (the hatches of where we can build are in its own panel, with their areas)"""
    rows = [("box", R28E_BLD, u"Building (survey)"), ("osm", None, u"Building, OpenStreetMap footprint"),
            ("her", None, u"Heritage building"), ("box", MPL["road"], u"Street"),
            ("box", MPL["water"], u"Stream"), ("dash", MPL["water_edge"], u"Covered course"),
            ("box", MPL["tree"], u"Woods, tree cover"), ("box", MPL["park"], u"Parks, grass"),
            ("box", MPL["field"], u"Fields, orchards"), ("contour", None, u"Contours, 5 m (10 m bolder)"),
            ("bridge", None, u"Bridge K1-K6 and its name"), ("edge", None, u"Bank edge, every 4 m (THE EDGE)"),
            ("walled", None, u"Walled bank"), ("embanked", None, u"Embanked bank (slope line)"),
            ("study", None, R28_STUDY_NAME), ("frame", None, R28_FRAME_NAME + u" (the map's edge)")]
    if photos:
        rows.append(("cone", None, u"Photo viewpoint and view cone"))
    return rows


def r28e_edge_panel(S, B, x, y, w, k, L):
    """THE EDGE: what meets the water, % of the bank length on both sides, six bars in the strip's edge colours,
    from (x, y) (top), w wide. Returns (the y under it, % walled, % embanked)."""
    sh_, wl_, em_, tot = edge_shares(S)
    if tot <= 0:
        return y, wl_, em_
    h7, h75 = bk_hk(7.0, k), bk_hk(7.5, k)
    B.text(u"THE EDGE " + bcite(EDGE_SRC), x, y - h75, h75, INK, L, font=FONT_TITLE, bold=True)
    y -= h75 + 1.6 * k
    r28e_rich(B, u"% of **{}** of bank · both sides, **every 4 m**".format(u_dim(tot, "km")), x, y - h7, h7, INK2, L)
    y -= h7 + 2.6 * k
    lw_ = 40.0 * k
    bw0 = w - lw_ - 9.0 * k
    vmax = max(sh_.values() or [1.0]) or 1.0
    for k_ in EDGE_ORDER:
        v_ = sh_.get(k_, 0.0)
        B.text(EB_EDGE_LAB[k_], x, y - h7, h7, INK, L, font=FONT_TITLE)
        bx_ = x + lw_
        if v_ > 0:
            B.fill([rect(bx_, y - h7 - 0.3 * k, bx_ + bw0 * v_ / vmax, y + 0.2 * k)], EDGE[k_][1], L, 20)
        B.text(u"{:.0f}%".format(v_), bx_ + bw0 * v_ / vmax + 1.2 * k, y - h7, h7, INK, L, font=FONT_TITLE, bold=True)
        y -= 3.5 * k
    return y, wl_, em_


def r28e_rings(B, x, y, wl_, em_, k, L):
    """walled and embanked: two rings, each with the mark the strip draws, "disconnected" under them; top at y.
    Returns the y under them."""
    h7, h8 = bk_hk(7.0, k), bk_hk(8.0, k)
    rr = 5.0 * k
    for j, (pct, kind) in enumerate(((wl_, "walled"), (em_, "embanked"))):
        rx, ry = x + rr + j * 21.0 * k, y - rr
        vis_ring(B, rx, ry, rr, pct, INK2, FAINT, L)
        B.text(u"{:.0f}%".format(pct), rx, ry, h8, INK, L, order=40, font=FONT_TITLE, bold=True, align="MC")
        sx, sy = rx - rr, ry - rr - 2.8 * k
        r28e_swatch(B, kind, None, sx, sy + 1.2 * k, k, L, w=4.5)
        B.text(kind, sx + 5.5 * k, sy - 0.5 * h7, h7, INK, L, font=FONT_TITLE)
    B.text(u"disconnected", x, y - 2.0 * rr - 6.2 * k, h7, INK2, L, font=FONT_TITLE)
    return y - 2.0 * rr - 7.2 * k


def r28e_build_key(S, B, x, y, w, k, L, fill=True):
    """WHERE WE CAN BUILD (P06.2: the legend beside the strip): the ground open to change, its three parts as the
    strip draws them (tint and vector hatch) with their areas; every figure is ground_open's count. Top at y.
    Returns the y under it."""
    h7, h75 = bk_hk(7.0, k), bk_hk(7.5, k)
    vac, park, loose, opn = ground_open(S)
    B.text(u"WHERE WE CAN BUILD " + bcite(OPEN_SRC), x, y - h75, h75, INK, L, font=FONT_TITLE, bold=True)
    y -= h75 + 1.6 * k
    r28e_rich(B, u"**{}** · {:.0f}% of the frame, **open to change**".format(
        u_area(opn, "ha"), 100.0 * opn / max(1.0, S.frame_area)), x, y - h7, h7, INK2, L)
    y -= h7 + 2.0 * k
    for (part, hk), a in zip(R28E_KEYS, (vac, park, loose)):
        r28e_swatch(B, "hatch" if fill else "hatchline", hk, x, y, k, L, h=3.0)
        r28e_rich(B, u"**{}** · {}".format(R28E_HATCH[hk][0], u_area(a, "ha")), x + 7.5 * k, y - 2.5 * k, h7, INK, L)
        y -= 4.4 * k
    return y


# ------------------------------------------------------------ p.06 and p.22
def draw_edge_build(S, B, x, y, w, U, with_photos=True):
    """v50 (MIRAQUA 28 Oct, P06.1-P06.4, G7, G8; replaces v45's two strips at 1:5,000): THE STREAM EDGE AND WHERE
    WE CAN BUILD (p.06, crop drw_edge_build). The whole frame as ONE strip at 1:10,000 on the booklet page
    (r28e_strip: the edge every 4 m on both banks, walls and embankments, where we can build hatched, bridges K1-K6
    with their names, street, mahalle and heritage names, contours, the study area, the photo viewpoints), its scale
    bar and north arrow under it; beside it THE EDGE, the walled / embanked rings and WHERE WE CAN BUILD; the map's
    key under them; the photos, four to a row, in the height left (the page's BK_AH). with_photos=False: p.22's copy
    (draw_edge_build_e). Drawn for the full booklet panel width (BK_AW). Returns the y below."""
    L = "LU_BOARD::EdgeBuild"
    F = S.F
    k = w / BK_AW
    top = y
    if not with_photos:
        return draw_edge_build_e(S, B, x, top, w, U, k, L)
    h7, h75, h9 = bk_hk(7.0, k), bk_hk(7.5, k), bk_hk(9.0, k)
    photos = []
    try:
        photos = photo_files(os.path.join(SELINUS_RES_DIR, "_site_photos"))
    except Exception:
        LOG.append("WARNING: the site photos could not be read for the stream edge plan:\n" + traceback.format_exc())
    V, ss, r, dropped = r28e_strip(S, B, x, top, k, L, photos)
    foot = b_foot(B, F, x, r[1], ss, k, L, R28E_SB_M)
    cx0 = r[2] + R28E_GAP * k                             # the column beside the strip
    cw = x + w - cx0
    yy, wl_, em_ = r28e_edge_panel(S, B, cx0, top, cw, k, L)
    yy -= 2.5 * k
    y1 = r28e_rings(B, cx0, yy, wl_, em_, k, L)
    y2 = r28e_build_key(S, B, cx0 + 44.0 * k, yy, cw - 44.0 * k, k, L)
    low = r28e_key(B, r28e_key_rows(bool(photos)), x, min(foot, y1, y2) - 3.0 * k, 6, w / 6.0, k, L)
    bot = top - BK_AH * k
    n_ph = len(photos)
    if n_ph:                                              # P06.4: the photos in the height the second strip left
        hb = low - 3.0 * k - h75
        B.text(u"SITE PHOTOS · 1 OCT 2026 · NUMBERS AND CONES ON THE PLAN " + bcite(
            u"Photos: site visit 2026-10-01 (group photos, GPS within {:.0f} m). On the plan: the dot is where each was "
            u"taken, the cone its direction (compass, true north) and angle of view (35 mm-equivalent focal length), "
            u"both from the photo's own record (EXIF), {:.0f} m long. Captions: keywords of the photo index (a visual "
            u"reading); Roman bridges after h01 §5.".format(max(it.get("gps_err_m", 0.0) for p, it in photos),
                                                             EB_CONE_M)), x, hb, h75, INK, L, font=FONT_TITLE, bold=True)
        py0 = hb - 3.0 * k
        cols, g = 4, 3.0 * k
        cell = (w - (cols - 1) * g) / cols
        rows_ = (n_ph + cols - 1) // cols
        cap_h = 1.2 * k + h7 + 2.2 * k                    # caption under each photo and the row gap
        ph = max(10.0 * k, min(cell * 0.75, (py0 - bot - 1.0 * k + 2.2 * k) / rows_ - cap_h))
        pw = ph / 0.75                                    # never stretched: 4:3 as taken
        bn = 4.2 * k
        for j, (p, it) in enumerate(photos):
            px = x + (j % cols) * (cell + g)
            py = py0 - (j // cols) * (ph + cap_h)
            B.image(p, px, py - ph, px + pw, py, L, order=5)
            B.fill([rect(px, py - bn, px + bn, py)], INK, L, 64)
            B.text(str(j + 1), px + 0.5 * bn, py - 0.5 * bn, h9, WHITE, L, order=65, font=FONT_TITLE, bold=True,
                   align="MC")
            B.text(eb_caption(it, pw, h7), px, py - ph - 1.2 * k - h7, h7, INK, L, font=FONT_TITLE)
        low = py0 - rows_ * (ph + cap_h) + 2.2 * k
        if low < bot + 0.5 * k:
            LOG.append(u"WARNING: the stream edge plan's photos end {:.1f} mm below the booklet page's area.".format(
                (bot + 0.5 * k - low) / k))
    crop_panel("edge_build", x, low - 0.5 * k, x + w, top + 0.5 * k,
               u"Both banks, the edge every 4 m · ground open to change · photo viewpoints 1-{}".format(n_ph or 8),
               crop_scale(ss), [])
    CROP_PANELS[-1]["bk_w"] = BK_AW                       # drawn for the full booklet panel width
    vac, park, loose, opn = ground_open(S)
    LOG.append(u"Stream edge plan (p.06): ONE strip at 1:{:,}, {:.1f} x {:.1f} mm; ground open to change {} ({:.1f}% "
               u"of the frame): open ground {}, parking & yards {}, loose ground {}; {} photos; labels left out (G4): "
               u"{}.".format(R28E_DEN, F.w * ss / k, F.h * ss / k, u_area(opn, "ha"), 100.0 * opn / max(1.0, S.frame_area),
                             u_area(vac, "ha"), u_area(park, "ha"), u_area(loose, "ha"), n_ph,
                             u", ".join(dropped) or u"none"))
    r28e_export_open(S)
    return low - 1.0 * U


def draw_edge_build_e(S, B, x, top, w, U, k, L):
    """v50 (P22.1, G7, G8; p.22 "Before the masterplan", cut when the booklet merges pp.21 + 22, D1): the strip of
    draw_edge_build without photos or viewpoints, ONE strip at 1:10,000; the column from EB_COL_X as before (THE
    EDGE, the walled / embanked rings, WHERE WE CAN BUILD, stacked), the key where the legend was (under the strip),
    scale bar and north arrow under the strip. Crop drw_edge_build_e, drawn for the full booklet panel width. Returns
    the y below."""
    V, ss, r, dropped = r28e_strip(S, B, x, top, k, L)
    foot = b_foot(B, S.F, x, r[1], ss, k, L, R28E_SB_M)
    cx0 = x + EB_COL_X * k
    cw = x + w - cx0
    yy, wl_, em_ = r28e_edge_panel(S, B, cx0, top, cw, k, L)
    yy = r28e_rings(B, cx0, yy - 2.5 * k, wl_, em_, k, L)
    yy = r28e_build_key(S, B, cx0, yy - 3.0 * k, cw, k, L)
    low = min(yy, r28e_key(B, r28e_key_rows(False), x, foot - 3.0 * k, 4, (r[2] - x) / 4.0, k, L))
    crop_panel("edge_build_e", x, low - 0.5 * k, x + w, top + 0.5 * k,
               u"Before the masterplan: both banks, the edge every 4 m · ground open to change", crop_scale(ss), [])
    CROP_PANELS[-1]["bk_w"] = BK_AW                       # drawn for the full booklet panel width
    LOG.append(u"Stream edge plan, p.22 copy: ONE strip at 1:{:,}; {:.0f} mm high; labels left out (G4): {}.".format(
        R28E_DEN, (top - low) / k, u", ".join(dropped) or u"none"))
    r28e_export_open(S)
    return low - 1.0 * U


# ------------------------------------------------------------ D1: the export and the filter sheet
def r28e_export_open(S):
    """D1: r28_open_to_change.json in SELINUS_RES_DIR, once a run: the ground open to change as p.06 counts and
    draws it, {frame_ha, total_ha, classes {vacant, parking, loose: {ha (ground_open's count, the figures p.06
    prints), rings (survey m, as drawn: the mapped outlines with their holes; the loose ground traced from the
    counted cells and smoothed)}}, definition, rings, source}"""
    m = r28e_memo(S)
    if m.get("exported"):
        return
    m["exported"] = True
    try:
        vac, park, loose, opn = ground_open(S)
        og = r28e_open_groups(S)
        cls = {}
        for (part, hk), a in zip(R28E_KEYS, (vac, park, loose)):
            cls[part] = {"ha": round(a / 1e4, 2),
                         "rings": [[[round(p[0], 2), round(p[1], 2)] for p in P] for g in og[part] for P in g
                                   if len(P) >= 3]}
        out = {"frame_ha": round(S.frame_area / 1e4, 2), "total_ha": round(opn / 1e4, 2), "classes": cls,
               "definition": u"Open to change (site board, p.06) = the analysis frame's vacant lots and parking & "
                             u"yards as mapped (survey, OpenStreetMap) and its loose ground: unmapped ground that ESA "
                             u"WorldCover 2021 classes as grassland or shrubland, counted on a {:.0f} m raster. A "
                             u"reading of what could change, not a check of ownership or zoning".format(REST_CELL),
               "rings": u"survey m; each class's outlines as p.06 draws them (the loose ground traced from the counted "
                        u"cells, simplified and smoothed); the areas are the count; fill even-odd",
               "source": u"{} · {}".format(SCRIPT_VERSION, time.strftime("%Y-%m-%d %H:%M"))}
        os.makedirs(SELINUS_RES_DIR, exist_ok=True)
        with open(R28E_OPEN_JSON, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, separators=(",", ":"))
        LOG.append(u"r28_open_to_change.json (D1): {} open to change of {} ({}: vacant {}, parking & yards {}, loose "
                   u"{} rings).".format(u_area(opn, "ha"), u_area(S.frame_area, "ha"), R28E_OPEN_JSON,
                                        len(cls["vacant"]["rings"]), len(cls["parking"]["rings"]),
                                        len(cls["loose"]["rings"])))
    except Exception:
        LOG.append("WARNING: r28_open_to_change.json not written:\n" + traceback.format_exc())


def r28e_mp_open():
    """D1: the masterplan's open ground (r28_open_ground.json beside its masterplan_results.json: the masterplan runs
    before the site board), or None (logged) when it is missing or not complete; and the path looked at"""
    p = bg_first([os.path.join(bg_cache("bergama_masterplan"), R28E_MP_JSON),
                  os.path.join(os.path.dirname(MP_RESULTS_FILE), R28E_MP_JSON)])
    try:
        with open(p, "r", encoding="utf-8") as fh:
            d = json.load(fh)
        if isinstance(d, dict) and isinstance(d.get("classes"), dict) and d.get("open_ha") is not None and \
                d.get("frame_ha") is not None:
            return d, p
        LOG.append(u"WARNING: {} has no open_ha, frame_ha or classes: the filter sheet says \"masterplan results "
                   u"needed\".".format(p))
    except Exception as ex:
        LOG.append(u"Filter sheet: the masterplan's open ground ({}) could not be read ({}): it says \"masterplan "
                   u"results needed\" and prints no open-ground figure.".format(p, ex))
    return None, p


def r28e_draw_filter(S, B, x, y, w, U):
    """v50 (MIRAQUA 28 Oct, D1; crop drw_filter, the booklet's one page for pp.21 + 22 when it merges them): THE
    FILTER. One strip of the analysis frame at 1:10,000 (G7, G8): the masterplan's open ground and what it leaves out
    (buildings, streets, the stream bed: its own cells, read from r28_open_ground.json) in R28_OPEN's colours, the
    ground open to change hatched as on p.06; under it the filter as three bars to one scale, analysis frame -> open
    ground (the masterplan's count, printed as it is: G10) -> of which open to change (ground_open, the figure p.06
    prints), one short reason a step (G5), and the two definitions named side by side. Without the masterplan's file
    the strip and the second bar say "masterplan results needed" and no open-ground figure is printed. Drawn for the
    full booklet panel width (BK_AW). Returns the y below."""
    L = "LU_BOARD::Filter"
    F = S.F
    k = w / BK_AW
    top = y
    h7, h75, h8, h9, h10 = (bk_hk(p_, k) for p_ in (7.0, 7.5, 8.0, 9.0, 10.0))
    mp, mp_path = r28e_mp_open()
    oc = dict((k_, C(R28_OPEN[k_])) for k_ in ("open_fill", "building", "road", "stream", "bridge"))
    cls = (mp or {}).get("classes") or {}

    def ha(key):                                          # a class of the masterplan's count, m2
        return float((cls.get(key) or {}).get("ha") or 0.0) * 1e4
    # ---- the strip
    ss = 1000.0 * k / R28E_DEN
    V = View(F, ss, x, top)
    r = (x, top - F.h * ss, x + F.w * ss, top)
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 1)
    if mp:
        for key, ck, o_ in (("open", "open_fill", 3), ("road", "road", 4), ("bed", "stream", 5),
                            ("building", "building", 6)):
            rings = [[(float(q[0]), float(q[1])) for q in P] for P in (cls.get(key) or {}).get("rings") or []
                     if len(P) >= 3]
            if rings:
                CB.fill(V.Ps(rings), oc[ck], L, o_)
    else:                                                 # the board's own streets, stream and buildings
        for rg_ in getattr(S, "road_net", None) or []:
            CB.fill(V.Ps([rg_["P"]] + rg_["H"]), oc["road"], L, 4)
        for wt in S.water:
            CB.fill(V.Ps([wt["P"]] + wt.get("H", [])), oc["stream"], L, 5)
        mini_buildings(S, CB, V, L, lambda u: oc["building"], order=6)
    og = r28e_open_groups(S)
    for part, hk in R28E_KEYS:
        r28e_hatched(CB, V, og[part], hk, k, L, 8, fill=False)
    for P in getattr(S, "bridges", []) or []:
        CB.line(V.P(P), oc["bridge"], L, 12, bk_lw(0.3, k))
    draw_r28_study(S, CB, V, k, L)
    if not mp:
        t_ = u"Open ground: masterplan results needed (r28_open_ground.json)"
        tl = r28mv_tw(t_, h8, True)
        cx_, cy_ = 0.5 * (r[0] + r[2]), 0.5 * (r[1] + r[3])
        bx = rect(cx_ - 0.5 * tl - 1.5 * k, cy_ - 0.5 * h8 - 1.5 * k, cx_ + 0.5 * tl + 1.5 * k, cy_ + 0.5 * h8 + 1.5 * k)
        B.fill([bx], WHITE, L, 60)
        B.line(bx + [bx[0]], MARK_C, L, 61, bk_lw(0.2, k))
        B.text(t_, cx_ - 0.5 * tl, cy_ - 0.5 * h8, h8, MARK_C, L, order=62, font=FONT_TITLE, bold=True)
    B.line(rect(*r) + [(r[0], r[1])], INK, L, 70, bk_lw(0.25, k))
    foot = b_foot(B, F, x, r[1], ss, k, L, R28E_SB_M)
    # ---- the key beside the strip
    kx = r[2] + R28E_GAP * k
    tw_ = x + w - kx
    vac, park, loose, opn = ground_open(S)
    rows = [("frame", None, R28_FRAME_NAME), ("study", None, R28_STUDY_NAME),
            ("box", oc["open_fill"], u"Open ground (masterplan)") if mp else
            ("note", None, u"Open ground: masterplan results needed"),
            ("box", oc["building"], u"Building"), ("box", oc["road"], u"Street"), ("box", oc["stream"], u"Stream bed"),
            ("line", (oc["bridge"], 0.3), u"Bridge")]
    rows += [("hatchline", hk, u"Open to change: " + nm_) for (part, hk), nm_ in
             zip(R28E_KEYS, (u"vacant lots", u"parking & yards", u"loose ground"))]
    kl = r28e_key(B, rows, kx, top, 1, tw_, k, L)
    # ---- the filter: three bars to one scale (the frame = the strip's length), a reason each
    fr = S.frame_area
    mfr = float(mp["frame_ha"]) * 1e4 if mp else fr
    if mp and abs(mfr - fr) > 500.0:
        LOG.append(u"Filter sheet: the masterplan's frame is {}, the board's {} (G10: the first bar prints the "
                   u"board's).".format(u_area(mfr, "ha"), u_area(fr, "ha")))
    oa = float(mp["open_ha"]) * 1e4 if mp else 0.0
    bars_w = r[2] - x
    pct = lambda a, b: u"{:.0f}%".format(100.0 * a / max(1.0, b))
    steps = [dict(label=u"1 · " + R28_FRAME_NAME, fig=u"{} · 100%".format(u_area(fr, "ha")), w=bars_w,
                  why=u"**{}**: the strip's rectangle, {} × {}; every figure on this page is counted over "
                      u"it.".format(R28_FRAME_NAME, u_num(F.w), u_dim(F.h, "m", 0)),
                  segs=[(u"Open ground", ha("open"), oc["open_fill"], INK),
                        (u"Buildings", ha("building"), oc["building"], WHITE),
                        (u"Streets", ha("road"), oc["road"], INK), (u"Stream bed", ha("bed"), oc["stream"], INK)]
                  if mp else [])]
    if mp:
        steps.append(dict(label=u"2 · Open ground (masterplan)", fig=u"{} · {} of the frame".format(
            u_area(oa, "ha"), pct(oa, mfr)), w=bars_w * oa / max(1.0, mfr),
            why=u"**Open ground**: no building, no street, not the stream bed: all the masterplan may draw on. "
                u"**Left out**: buildings {}, streets {}, the stream bed {}.".format(
                    u_area(ha("building"), "ha"), u_area(ha("road"), "ha"), u_area(ha("bed"), "ha")),
            segs=[(u"", oa, oc["open_fill"], INK)]))
    else:
        steps.append(dict(label=u"2 · Open ground (masterplan)", fig=None, w=None, note=True,
                          why=u"**Masterplan results needed**: the open ground is the masterplan's own count "
                              u"(r28_open_ground.json, written when the masterplan runs); no figure is printed "
                              u"without it."))
    steps.append(dict(label=u"3 · Of which open to change (site board, as p.06)", fig=u"{} · {} of the frame".format(
        u_area(opn, "ha"), pct(opn, fr)), w=bars_w * opn / max(1.0, fr), hatch=True,
        why=u"**No use recorded**: vacant lots {}, parking & yards {}, loose ground {} (grass or scrub where nothing is "
            u"mapped). **Not counted**: planted or farmed ground (parks, woods, fields, orchards) and unmapped ground "
            u"the satellite does not see as grass or scrub.".format(
                u_area(vac, "ha"), u_area(park, "ha"), u_area(loose, "ha"))))
    close_s = (u"**Two readings, not two answers.** Open ground is what is not built, paved or water: all the "
               u"masterplan may draw on. Open to change is only the ground with no use recorded, counted on the site "
               u"board's own map (p.06). Both read what could change, **not a check of ownership or zoning**.")
    src = bcite(OPEN_SRC)
    if mp:
        src += bcite(u"Open ground: the masterplan's count, read from its r28_open_ground.json ({}). {}.".format(
            mp.get("source", u""), mp.get("definition", u"")))
    yy = min(foot, kl) - 4.0 * k
    B.text(u"THE FILTER · ANALYSIS FRAME, OPEN GROUND, OPEN TO CHANGE " + src, x, yy - h9, h9, INK, L,
           font=FONT_TITLE, bold=True)
    yy -= h9 + 4.0 * k
    bh = 10.0 * k
    heights = []
    for st_ in steps:
        n_ = len(r28mv_lines(st_["why"], tw_, h8))
        th = (h10 + 2.2 * k if st_.get("fig") else 0.0) + h8 + (n_ - 1) * R28MV_LEAD * h8 + 0.6 * k
        heights.append(max(h75 + 1.6 * k + bh, th))
    n_c = len(r28mv_lines(close_s, w, h8))
    close_h = 5.0 * k + h8 + (n_c - 1) * R28MV_LEAD * h8 + 0.6 * k
    bot = top - BK_AH * k + 1.0 * k
    spare = (yy - bot) - sum(heights) - close_h
    gap = max(8.0 * k, min(24.0 * k, 0.5 * spare))        # the funnels take the height the page has
    funnel = mix(oc["open_fill"], WHITE, 0.55)
    prev = None
    ty = yy
    for st_, hgt in zip(steps, heights):
        lb = ty - h75
        bt = lb - 1.6 * k
        bb_ = bt - bh
        if mp and prev is not None and st_.get("w"):      # the funnel from the bar above
            B.fill([[(x, prev[1]), (x + prev[0], prev[1]), (x + st_["w"], bt), (x, bt)]], funnel, L, 2)
        B.text(st_["label"], x, lb, h75, INK, L, font=FONT_TITLE, bold=True)
        if st_.get("hatch"):
            cx_ = x
            for (part, hk), a in zip(R28E_KEYS, (vac, park, loose)):
                sw = bars_w * a / max(1.0, fr)
                if sw > 0.0:
                    q = rect(cx_, bb_, cx_ + sw, bt)
                    lab_, col_, ang_ = R28E_HATCH[hk]
                    B.fill([q], mix(col_, WHITE, R28E_TINT), L, 20)
                    B.hatch([q], col_, L, 21, R28E_HATCH_MM[0] * k, math.radians(ang_), bk_lw(R28E_HATCH_MM[1], k))
                    cx_ += sw
            B.line(rect(x, bb_, cx_, bt) + [(x, bb_)], INK, L, 22, bk_lw(0.15, k))
        elif st_.get("note"):
            q = rect(x, bb_, x + 0.5 * bars_w, bt)
            B.line(q + [q[0]], MARK_C, L, 22, bk_lw(0.2, k))
            B.text(u"masterplan results needed", x + 1.5 * k, bb_ + 0.5 * (bh - h75), h75, MARK_C, L, order=24,
                   font=FONT_TITLE, bold=True)
        else:
            cx_ = x
            tot_ = sum(s_[1] for s_ in st_.get("segs") or []) or 0.0
            for nm_, a, col_, tc_ in (st_.get("segs") or []) if tot_ > 0.0 else []:
                sw = st_["w"] * a / tot_
                B.fill([rect(cx_, bb_, cx_ + sw, bt)], col_, L, 20)
                t_ = u"{} {}".format(nm_, u_area(a, "ha")) if nm_ else u""
                if t_ and r28mv_tw(t_, h7) + 2.4 * k <= sw:
                    B.text(t_, cx_ + 1.2 * k, bb_ + 0.5 * (bh - h7), h7, tc_, L, order=24, font=FONT_TITLE)
                cx_ += sw
            if tot_ <= 0.0:                               # the frame alone (without the masterplan's classes)
                B.fill([rect(x, bb_, x + st_["w"], bt)], WHITE, L, 20)
            B.line(rect(x, bb_, x + st_["w"], bt) + [(x, bb_)], INK, L, 22, bk_lw(0.15, k))
        yb = ty
        if st_.get("fig"):
            B.text(st_["fig"], kx, ty - h10, h10, INK, L, font=FONT_TITLE, bold=True)
            yb = ty - h10 - 2.2 * k
        r28mv_para(B, st_["why"], kx, yb - h8, tw_, h8, INK, L, order=40)
        prev = (st_.get("w") or 0.0, bb_)
        y_end = ty - hgt
        ty = y_end - gap
    yc = r28mv_para(B, close_s, x, y_end - 5.0 * k - h8, w, h8, INK, L, order=40)
    low = yc + R28MV_LEAD * h8 - 0.6 * k - h8 * 0.3
    if low < bot - 0.5 * k:
        LOG.append(u"WARNING: the filter sheet ends {:.1f} mm below the booklet page's area.".format((bot - low) / k))
    crop_panel("filter", x, low - 0.5 * k, x + w, top + 0.5 * k,
               u"The filter · analysis frame, open ground, open to change", crop_scale(ss), [])
    CROP_PANELS[-1]["bk_w"] = BK_AW                       # drawn for the full booklet panel width
    LOG.append(u"Filter sheet (D1, crop drw_filter): {} frame -> open ground {} -> open to change {} (vacant {}, "
               u"parking & yards {}, loose {}); one strip at 1:{:,}; {:.0f} mm high.".format(
                   u_area(fr, "ha"), u_area(oa, "ha") if mp else u"(masterplan results needed: " + mp_path + u")",
                   u_area(opn, "ha"), u_area(vac, "ha"), u_area(park, "ha"), u_area(loose, "ha"), R28E_DEN,
                   (top - low) / k))
    r28e_export_open(S)
    return low - 1.0 * U
