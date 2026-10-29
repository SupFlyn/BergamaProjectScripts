# p.06 the stream edge and where we can build (split from parts/15c_review_pages.py, parts/15e_v45_pages.py,
# parts/15k_r28_edge.py on 29 Oct 2026).
# Revision 29 Oct 2026 (WO-T3a-4, D1 a: p.22 merged into p.06): ONE drawing, crop drw_edge_build. The p.22 copy
# (draw_edge_build_e, crop drw_edge_build_e) and the filter sheet (r28e_draw_filter, crop drw_filter) are gone: their
# one idea (frame -> unbuilt -> open to change) is the bar in WHERE WE CAN BUILD. Where we can build is recounted
# here on ONE 2 m raster (p06_open: every cell counted once, buildings / streets / water first), bare open ground
# added, the largest pieces named as sites A-F with boxes (R10 / R11 idea: what it is, m², what it opens to); the
# base is the basemap module's detailed mode; hatches heavier. Every m² figure is a cell count, never typed.


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


def r28e_strip(S, B, x, yt, k, L, photos=(), sites=()):
    """v50 (G7, P06.1, P06.4): the whole frame as ONE strip at 1:10,000, its top-left corner at (x, yt): the base,
    the edge every 4 m on both banks (walled and embanked marked), bridges K1-K6 as bars with their names, the photo
    viewpoints (numbered discs, view cones), the context names (G4), the frame's line. v51 (WO-T3a-4): the base is the
    basemap's detailed mode (p06_base), where we can build is p06_open's four classes (p06_hatched), the sites
    (p06_open's largest pieces) outlined with a lettered square each; every site gets its badge's page point as
    s["px"], s["py"]. Returns (View, board units per metre, the strip's rectangle, the labels dropped)."""
    F = S.F
    ss = 1000.0 * k / R28E_DEN
    V = View(F, ss, x, yt)
    r = (x, yt - F.h * ss, x + F.w * ss, yt)
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 1)
    p06_base(S, CB, V, k, L)
    O = p06_open(S)
    for part, hk in P06_CLASSES:                          # where we can build: tint, hatch and edge, legible
        p06_hatched(CB, V, O["draw"][part], hk, k, L, 6)
    for P in getattr(S, "bridges", []) or []:
        CB.line(V.P(P), MPL["ink_dark"], L, 25, bk_lw(0.3, k))
    draw_r28_study(S, CB, V, k, L)
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
    sq = 1.7 * k                                          # a site: its outline and a lettered square (photos: discs)
    for st in sites:
        for g in st["rings"]:
            for P in g:
                CB.line(V.P(list(P) + [P[0]]), MPL["ink_dark"], L, 44, bk_lw(P06_SITE_MM, k))
        px, py = V.p(st["x"], st["y"])
        st["px"], st["py"] = px, py
        q = rect(px - sq, py - sq, px + sq, py + sq)
        B.fill([q], WHITE, L, 62)
        B.line(q + [q[0]], MPL["ink_dark"], L, 63, bk_lw(0.3, k))
        B.text(st["id"], px, py, h7, MPL["ink_dark"], L, order=64, font=FONT_TITLE, bold=True, align="MC")
        taken.append((px - sq - 0.3 * k, py - sq - 0.3 * k, px + sq + 0.3 * k, py + sq + 0.3 * k))
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
    OpenStreetMap footprint's thin outline), her (heritage building), hatch / hatchline (P06_CLASSES hatch key ref:
    tint, hatch and edge as the strip / the hatch alone), line (ref = (colour, mm)), dash (ref = colour: the covered
    course), study (G8), contour (a 10 m and a 5 m line), bridge (a bar across the stream), edge (the six edge
    colours), walled / embanked (the bank marks), cone (a viewpoint), frame (the analysis frame's line), site (v51)"""
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
        lab, col, ang = p06_hatch_spec(ref)
        if kind == "hatch":
            B.fill([sw_], mix(col, WHITE, P06_TINT), L, order)
        B.hatch([sw_], col, L, order + 1, P06_HATCH_MM[0] * k, math.radians(ang), bk_lw(P06_HATCH_MM[1], k))
        B.line(sw_ + [sw_[0]], col, L, order + 2, bk_lw(P06_EDGE_MM, k))
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
    elif kind == "site":                                  # v51: a site's outline and its lettered square
        B.line(sw_ + [sw_[0]], MPL["ink_dark"], L, order, bk_lw(P06_SITE_MM, k))
        q = rect(x + 0.5 * w - 0.9 * k, ym - 0.9 * k, x + 0.5 * w + 0.9 * k, ym + 0.9 * k)
        B.fill([q], WHITE, L, order + 1)
        B.line(q + [q[0]], MPL["ink_dark"], L, order + 2, bk_lw(0.2, k))


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
            ("study", None, R28_STUDY_NAME), ("frame", None, R28_FRAME_NAME + u" (the map's edge)"),
            ("site", None, u"Site: open ground in one piece (boxes under the map)")]
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


# ------------------------------------------------------------ v51 (WO-T3a-4): where we can build, recounted
# ONE raster of the analysis frame (REST_CELL, the cells frame_rest splits the unmapped ground on); every cell is
# counted once, in this order: buildings, street surfaces (and the centre line of every street without a measured
# width), the stream's water: never open; then vacant lots, parking & yards (OpenStreetMap / survey zones), loose
# ground (the satellite's grass or scrub on unmapped ground, and OpenStreetMap grass lots), bare ground (unmapped
# ground with no satellite class, wide enough for a P06_BARE_R opening and P06_BARE_MIN or more in one piece). Every
# m² printed is (cells) x REST_CELL²: the drawing traces the same cells, so figure and hatch agree.
P06_CLASSES = (("vacant", "open"), ("parking", "parking"), ("loose", "loose"), ("bare", "bare"))  # count -> hatch key
P06_BARE_HATCH = (u"Bare ground", "847E75", 90.0)   # palette v1.4 ink2; vertical, apart from the other three angles
P06_LABEL = {"open": u"Vacant ground", "parking": u"Parking & yards", "loose": u"Loose ground", "bare": u"Bare ground"}
P06_WHAT = {"open": u"vacant lot", "parking": u"parking, yards", "loose": u"grass, scrub", "bare": u"bare ground"}
P06_GRASS_LU = ("grass", "greenery")                # OpenStreetMap grass lots: no use recorded, counted as loose
P06_GRASS_NAT = ("grassland", "heath")
P06_BARE_R = 5                  # cells: bare ground holds a square of 2 x 5 + 1 cells (22 m), so yards and street
P06_BARE_MIN = 1000.0           # m2: ... gaps between buildings drop out; one piece at least this large
P06_NEAR = (("stream", 10.0), ("street", 4.0), ("green", 4.0))   # m: a site opens to it within this distance
P06_OPEN_TO = {"stream": u"the stream", "street": u"a street", "green": u"parks, woods or fields"}
P06_N_SITES = 6                 # the largest pieces of open ground, lettered A-F on the map and boxed under it
P06_LETTERS = u"ABCDEFGH"
P06_BY_M = 150.0                # m: a site this close to a bridge is "by K.."
P06_BANK_M = 40.0               # m: a site this close to the stream's centre line is on its bank
P06_TINT = 0.72                 # a hatch's ground: its line colour this far to white (was 0.86: too faint)
P06_HATCH_MM = (0.8, 0.2)       # mm: hatch spacing and line weight on the booklet page (were 1.0, 0.12)
P06_EDGE_MM = 0.15              # mm: each open piece's edge in its hatch colour
P06_SITE_MM = 0.35              # mm: a site's outline
P06_OTHER = C("EFEDE6")         # palette v1.4 paper: the frame's other unbuilt ground in the bar
P06_SRC = (u"Land cover: ESA WorldCover 10 m 2021 v200 (CC BY 4.0, contains modified Copernicus Sentinel data "
           u"2021). Lots, parking, grass and streets: © OpenStreetMap contributors (ODbL).")


def p06_hatch_spec(key):
    """(legend name, colour, hatch angle) of a P06_CLASSES hatch key"""
    if key == "bare":
        return P06_LABEL["bare"], C(P06_BARE_HATCH[1]), P06_BARE_HATCH[2]
    lab, col, ang = R28E_HATCH[key]
    return P06_LABEL.get(key, lab), col, ang


def p06_grass_zone(z):
    """an OpenStreetMap grass lot (landuse grass / greenery, natural grassland / heath): open ground, no use recorded"""
    t = z.get("tags") or {}
    return z["kind"] == "green" and (t.get("landuse") in P06_GRASS_LU or t.get("natural") in P06_GRASS_NAT)


def _p06_cnt(rows):
    return sum(bin(r_).count("1") for r_ in rows)


def _p06_or(*masks):
    out = list(masks[0])
    for msk in masks[1:]:
        out = [a | b for a, b in zip(out, msk)]
    return out


def _p06_and(a, b):
    return [x & y for x, y in zip(a, b)]


def _p06_less(a, b):
    return [x & ~y for x, y in zip(a, b)]


def _p06_morph(rows, r, nx, grow):
    """a raster dilated (grow) or eroded by a square of 2r + 1 cells"""
    full = (1 << nx) - 1
    h = []
    for m in rows:
        e = m
        for i in range(1, r + 1):
            e = (e | (m << i) | (m >> i)) if grow else (e & (m << i) & (m >> i))
        h.append(e & full)
    ny, out = len(h), []
    for j in range(ny):
        e = h[j]
        for i in range(1, r + 1):
            a = h[j - i] if j - i >= 0 else 0
            b = h[j + i] if j + i < ny else 0
            e = (e | a | b) if grow else (e & a & b)
        out.append(e)
    return out


def _p06_burn(F, lines, c, nx, ny):
    """the cells a set of polylines (survey m) passes through"""
    rows = [0] * ny
    for P in lines:
        Q = [F.local(p[0], p[1]) for p in P]
        for (u0, v0), (u1, v1) in zip(Q[:-1], Q[1:]):
            n = max(1, int(math.hypot(u1 - u0, v1 - v0) / (0.5 * c)) + 1)
            for i in range(n + 1):
                a = int(math.floor((u0 + (u1 - u0) * i / n - F.u0) / c))
                j = int(math.floor((v0 + (v1 - v0) * i / n - F.v0) / c))
                if 0 <= a < nx and 0 <= j < ny:
                    rows[j] |= 1 << a
    return rows


def _p06_rings(F, rows, c):
    """a raster's outlines in survey m (cell corners; outer rings anticlockwise, holes clockwise)"""
    return [[F.world(F.u0 + a * c, F.v0 + j * c) for a, j in R_] for R_ in r28e_trace(rows)]


def p06_where(S, x, y):
    """a site's place in words: (side of the stream, "by K5" / "K4-K5" / "beyond K6")"""
    F = S.F
    best = None
    for P in getattr(S, "selinus", None) or []:
        for (ax, ay), (bx, by) in zip(P[:-1], P[1:]):
            dx, dy = bx - ax, by - ay
            t = max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / (dx * dx + dy * dy or 1e-9)))
            qx, qy = ax + t * dx, ay + t * dy
            d = math.hypot(x - qx, y - qy)
            if best is None or d < best[0]:
                best = (d, qx, qy)
    side = u""
    if best is not None and best[0] > 1.0:                # survey y = north
        ang = math.degrees(math.atan2(y - best[2], x - best[1]))
        side = (u"East", u"North", u"West", u"South")[int(((ang + 45.0) % 360.0) // 90.0)]
        side += u" bank" if best[0] <= P06_BANK_M else u" of the stream"
    br = [(kk, F.local(bx, by)[0], math.hypot(bx - x, by - y)) for kk, nm, bx, by in BRIDGES_K if F.inside(bx, by)]
    pos = u""
    if br:
        kk, bu, d = min(br, key=lambda b_: b_[2])
        if d <= P06_BY_M:
            pos = u"by " + kk
        else:
            u_ = F.local(x, y)[0]
            lo = [b_ for b_ in br if b_[1] <= u_]
            hi = [b_ for b_ in br if b_[1] > u_]
            if lo and hi:
                pos = u"{}–{}".format(max(lo, key=lambda b_: b_[1])[0], min(hi, key=lambda b_: b_[1])[0])
            else:
                pos = u"beyond " + (max(lo, key=lambda b_: b_[1]) if lo else min(hi, key=lambda b_: b_[1]))[0]
    return side, pos


def p06_open(S):
    """v51 (WO-T3a-4): where we can build, counted once a run (memo; every p.06 drawing and the export reuse it):
    {area {vacant, parking, loose, bare: m2}, open (their sum), frame, bar {buildings, streets, stream, other: m2},
    draw {class: smooth outline groups}, sites [{id, a, shares, opens, study, x, y, rings, side, pos, key}]}.
    Method in the comment above P06_CLASSES; all figures are cell counts."""
    m = r28e_memo(S)
    if "p06" in m:
        return m["p06"]
    F, c = S.F, REST_CELL
    nx, ny = int(math.ceil(F.w / c)), int(math.ceil(F.h / c))
    zero = [0] * ny

    def mk(polys):
        P_ = [P for P in polys if P and len(P) >= 3]
        return mask_of(F, P_, c, nx, ny) if P_ else list(zero)

    zmask = [mask_of(F, z["Ps"], c, nx, ny, holes=z.get("Hs") or None) for z in S.zones]   # each zone once

    def zm(pred):
        out = list(zero)
        for z, msk in zip(S.zones, zmask):
            if pred(z):
                out = _p06_or(out, msk)
        return out
    rr = getattr(S, "rest_rows", None) or {}

    def rr_(key):
        r_ = rr.get(key) or []
        return [r_[j] if j < len(r_) else 0 for j in range(ny)]
    fr = _loop_rows(F, [F.P], c, nx, ny)
    bld = mk([P for u in S.bld for P in u["parts"]])
    road = _p06_or(mk(getattr(S, "road_polys", None) or []),
                   _p06_burn(F, [r_["P"] for r_ in S.roads if not r_.get("w") and len(r_["P"]) >= 2], c, nx, ny))
    wat = list(zero)
    for w_ in getattr(S, "water", None) or []:
        if len(w_["P"]) >= 3:
            wat = _p06_or(wat, mask_of(F, [w_["P"]], c, nx, ny, holes=w_.get("H") or None))
    hard = _p06_or(bld, road, wat)
    free = _p06_less(fr, hard)
    vac = _p06_and(zm(lambda z: z["kind"] == "vacant"), free)
    park = _p06_less(_p06_and(zm(lambda z: z["kind"] == "transport"), free), vac)
    loose = _p06_less(_p06_and(_p06_or(rr_("grass"), rr_("shrub"), zm(p06_grass_zone)), free), _p06_or(vac, park))
    if rr:                                                # bare: unmapped, no satellite class, wide and large
        rest = _p06_less(_p06_less(free, zm(lambda z: True)), _p06_or(*[rr_(k_) for k_ in rr]))
        opened = _p06_and(_p06_morph(_p06_morph(rest, P06_BARE_R, nx, False), P06_BARE_R, nx, True), rest)
        keep = [g for g in r28e_groups(_p06_rings(F, opened, c)) if sum(signed_area(P) for P in g) >= P06_BARE_MIN]
        bare = _p06_and(_loop_rows(F, [P for g in keep for P in g], c, nx, ny), opened) if keep else list(zero)
    else:
        bare = list(zero)
        LOG.append(u"WARNING: where we can build (p.06): the frame's unmapped ground was not split by the satellite "
                   u"classes (frame_rest): no loose ground from the satellite and no bare ground counted.")
    a2 = c * c
    cls = {"vacant": vac, "parking": park, "loose": loose, "bare": bare}
    area = dict((k_, _p06_cnt(v) * a2) for k_, v in cls.items())
    opn = sum(area.values())
    frame = _p06_cnt(fr) * a2
    bar = {"buildings": _p06_cnt(_p06_and(bld, fr)) * a2,
           "streets": _p06_cnt(_p06_and(_p06_less(road, bld), fr)) * a2,
           "stream": _p06_cnt(_p06_and(_p06_less(wat, _p06_or(bld, road)), fr)) * a2}
    bar["other"] = max(0.0, frame - sum(bar.values()) - opn)
    draw = dict((k_, r28e_groups([r28e_smooth(P) for P in _p06_rings(F, v, c)])) for k_, v in cls.items())
    # ---- the sites: the largest pieces of open ground (all four classes together)
    union = _p06_or(vac, park, loose, bare)
    comps = sorted(r28e_groups(_p06_rings(F, union, c)), key=lambda g: -sum(signed_area(P) for P in g))
    green = _p06_or(zm(lambda z: z["kind"] in ("green", "agri") and not p06_grass_zone(z)),
                    rr_("trees"), rr_("farmland"), rr_("orchard"))
    near = dict((nm_, _p06_morph(msk, max(1, int(math.ceil(d_ / c))), nx, True)) for (nm_, d_), msk in
                zip(P06_NEAR, (wat, road, green)))
    study = mk(getattr(S, "r28_study", None) or [])
    sites = []
    for g in comps[:P06_N_SITES]:
        gm = _p06_and(_loop_rows(F, g, c, nx, ny), union)
        n_ = _p06_cnt(gm)
        if n_ <= 0:
            continue
        shares = dict((k_, _p06_cnt(_p06_and(gm, v)) / float(n_)) for k_, v in cls.items())
        x_, y_ = interior_point(g[0])
        side, pos = p06_where(S, x_, y_)
        key = max(P06_CLASSES, key=lambda pk: shares[pk[0]])[1]
        sites.append(dict(id=P06_LETTERS[len(sites)], a=n_ * a2, shares=shares, x=x_, y=y_, side=side, pos=pos,
                          key=key, rings=[[r28e_smooth(P) for P in g]],
                          opens=[nm_ for nm_, d_ in P06_NEAR if _p06_cnt(_p06_and(gm, near[nm_])) > 0],
                          study=_p06_cnt(_p06_and(gm, study)) / float(n_)))
    O = dict(area=area, open=opn, frame=frame, bar=bar, draw=draw, sites=sites)
    m["p06"] = O
    LOG.append(u"Where we can build (p.06, one {:.0f} m raster, each cell once): frame {}; open to change {} ({:.1f}%): "
               u"vacant {}, parking & yards {}, loose {}, bare {}; buildings {}, streets {}, stream {}, other unbuilt "
               u"{}. Before (ground_open): {} (vacant and parking as whole zones, loose scaled by frame_rest). Sites: "
               u"{}.".format(c, u_area(frame), u_area(opn), 100.0 * opn / max(1.0, frame), u_area(area["vacant"]),
                             u_area(area["parking"]), u_area(area["loose"]), u_area(area["bare"]),
                             u_area(bar["buildings"]), u_area(bar["streets"]), u_area(bar["stream"]),
                             u_area(bar["other"]), u_area(ground_open(S)[3]),
                             u"; ".join(u"{} {} {} {}".format(s_["id"], u_area(s_["a"]), s_["side"], s_["pos"])
                                        for s_ in sites) or u"none"))
    return O


# ------------------------------------------------------------ v51: the base, the hatches, the panel, the boxes
class _P06NoOpen(object):
    """r28e_base seen without its own open-ground layers (fills at 6, hatches at 7): the fallback base when the
    basemap file is missing (p.06 draws p06_open's classes itself)"""

    def __init__(self, B):
        self.B = B

    def __getattr__(self, k_):
        return getattr(self.B, k_)

    def fill(self, polys, color, layer, order):
        if order != 6:
            self.B.fill(polys, color, layer, order)

    def hatch(self, polys, color, layer, order, *a, **kw):
        if order != 7:
            self.B.hatch(polys, color, layer, order, *a, **kw)


def p06_base(S, CB, V, k, L):
    """v51 (02 §1): the strip's base = the basemap module's detailed mode inside the frame (memoised by the module):
    its fills at order 3 (under the hatches), its lines at 9 (over them), no texts (the strip names its own); without
    the basemap file, the board's own base (r28e_base) without its open-ground layers"""
    D = None
    try:
        lg = []
        D = basemap_load(log=lg)
        LOG.extend(lg)
    except Exception:
        LOG.append(u"WARNING: p.06 basemap not read:\n" + traceback.format_exc())
    if not D:
        LOG.append(u"p.06: no basemap file: the board's own base is drawn.")
        r28e_base(S, _P06NoOpen(CB), V, k, L)
        return
    xs, ys = [p[0] for p in S.F.P], [p[1] for p in S.F.P]
    items = basemap_items("detailed", box=(min(xs), min(ys), max(xs), max(ys)), D=D)

    def fill_fn(rings, hx, alpha, nonzero):
        col = C(hx)
        if alpha is not None and alpha < 1.0:
            col = mix(col, WHITE, 1.0 - alpha)
        CB.fill(rings, r28_nz(col) if nonzero else col, L, 3)

    def line_fn(pts, hx, width_mm, dash_mm, alpha):
        col = C(hx)
        if alpha is not None and alpha < 1.0:
            col = mix(col, WHITE, 1.0 - alpha)
        lw = bk_lw(width_mm or 0.1, k)
        if dash_mm:
            on, off = (dash_mm[0], dash_mm[1]) if isinstance(dash_mm, (tuple, list)) else (dash_mm, dash_mm)
            for d in dashes(pts, on * k, off * k):
                CB.line(d, col, L, 9, lw)
        else:
            CB.line(pts, col, L, 9, lw)
    basemap_draw(items, lambda p: V.p(p[0], p[1]), fill_fn, line_fn, None)


def p06_hatched(CB, V, groups, key, k, L, order):
    """one class of where we can build: light tint (P06_TINT), hatch (P06_HATCH_MM) and a thin edge in its colour"""
    lab, col, ang = p06_hatch_spec(key)
    chunk = []
    for i, g in enumerate(groups):
        chunk.extend(g)
        if len(chunk) >= 400 or i == len(groups) - 1:
            Ps = V.Ps(chunk)
            CB.fill(Ps, mix(col, WHITE, P06_TINT), L, order)
            CB.hatch(Ps, col, L, order + 1, P06_HATCH_MM[0] * k, math.radians(ang), bk_lw(P06_HATCH_MM[1], k))
            for P in Ps:
                CB.line(P + [P[0]], col, L, order + 1, bk_lw(P06_EDGE_MM, k))
            chunk = []


def p06_build_panel(S, B, x, y, w, k, L):
    """WHERE WE CAN BUILD beside the strip (p.22's filter folded in as one bar): the figure, the analysis frame as one
    bar (open to change by class, other unbuilt ground, streets, buildings, the stream: p06_open's counts), the four
    classes with their m². Top at y. Returns the y under it."""
    O = p06_open(S)
    h65, h7, h75 = bk_hk(6.5, k), bk_hk(7.0, k), bk_hk(7.5, k)
    B.text(u"WHERE WE CAN BUILD " + bcite(P06_SRC), x, y - h75, h75, INK, L, font=FONT_TITLE, bold=True)
    y -= h75 + 1.6 * k
    fr = max(1.0, O["frame"])
    s_ = u"**{}** · {:.0f}% of the frame, **open to change**".format(u_area(O["open"]), 100.0 * O["open"] / fr)
    r28mv_para(B, s_, x, y - h7, w, h7, INK2, L, order=40)
    y -= h7 + (len(r28mv_lines(s_, w, h7)) - 1) * R28MV_LEAD * h7 + 2.0 * k
    bh = 4.6 * k                                          # the frame as one bar
    cx_ = x
    for part, hk in P06_CLASSES:
        sw = w * O["area"][part] / fr
        if sw > 0.0:
            q = rect(cx_, y - bh, cx_ + sw, y)
            lab, col, ang = p06_hatch_spec(hk)
            B.fill([q], mix(col, WHITE, P06_TINT), L, 20)
            B.hatch([q], col, L, 21, P06_HATCH_MM[0] * k, math.radians(ang), bk_lw(P06_HATCH_MM[1], k))
            cx_ += sw
    x_open = cx_
    for nm_, key, col, tc in ((u"other unbuilt", "other", P06_OTHER, INK), (u"streets", "streets", MPL["road"], INK),
                              (u"buildings", "buildings", R28E_BLD, INK), (u"stream", "stream", MPL["water"], INK)):
        sw = w * O["bar"][key] / fr
        if sw <= 0.0:
            continue
        B.fill([rect(cx_, y - bh, cx_ + sw, y)], col, L, 20)
        if r28mv_tw(nm_, h65) + 1.2 * k <= sw:
            B.text(nm_, cx_ + 0.6 * k, y - 0.5 * (bh + h65), h65, tc, L, order=24, font=FONT_TITLE)
        cx_ += sw
    B.line(rect(x, y - bh, x + w, y) + [(x, y - bh)], INK, L, 22, bk_lw(0.15, k))
    yb = y - bh - 1.0 * k                                 # a bracket under the open part
    if x_open - x > 1.0 * k:
        B.line([(x, yb + 0.6 * k), (x, yb), (x_open, yb), (x_open, yb + 0.6 * k)], INK, L, 22, bk_lw(0.15, k))
    yt_ = yb - 0.8 * k - h65                              # under the bracket its name; at the bar's end the frame
    B.text(u"open to change", x, yt_, h65, INK, L, font=FONT_TITLE, bold=True)
    t_ = u"whole bar: {} {}".format(R28_FRAME_NAME.lower(), u_area(fr))
    B.text(t_, x + w - r28mv_tw(t_, h65), yt_, h65, INK2, L, font=FONT_TITLE)
    y = yt_ - 2.4 * k
    for part, hk in P06_CLASSES:
        r28e_swatch(B, "hatch", hk, x, y, k, L, h=3.0)
        r28e_rich(B, u"**{}** · {}".format(p06_hatch_spec(hk)[0], u_area(O["area"][part])), x + 7.5 * k, y - 2.5 * k,
                  h7, INK, L)
        y -= 4.2 * k
    return y


def p06_site_lines(st):
    """a site box's lines: (title, [body lines with **bold**])"""
    t = u"{} · {}".format(st["id"], u", ".join(v for v in (st["side"], st["pos"]) if v) or u"open ground")
    what = u" + ".join(P06_WHAT[hk] for part, hk in P06_CLASSES if st["shares"][part] >= 0.2)
    what = what[:1].upper() + what[1:]
    opens = (u"Opens to " + u", ".join(P06_OPEN_TO[o] for o in st["opens"])) if st["opens"] else \
        u"Closed in by buildings"
    stdy = (u"Inside the study area" if st["study"] >= 0.5 else
            u"Partly in the study area" if st["study"] > 0.0 else u"Outside the study area")
    return t, [u"**{}**".format(u_area(st["a"])), what or P06_WHAT[st["key"]].capitalize(), opens, stdy]


def p06_site_boxes(B, sites, x0, x1, ytop, ystrip, k, L):
    """R10 / R11: one box a site, side by side under the strip from (x0, ytop) to x1, in the order of their squares
    on the map (so no two leaders cross): a title bar in the colour of its main class, the m², what it is, what it
    opens to, the study area; a thin leader from the box up to its square. Returns the y under them."""
    if not sites:
        return ytop
    h7, h75 = bk_hk(7.0, k), bk_hk(7.5, k)
    order_ = sorted(sites, key=lambda s_: s_.get("px", 0.0))
    n, g = len(order_), 3.0 * k
    bw = (x1 - x0 - (n - 1) * g) / n
    tw_ = bw - 2.4 * k
    hb = h75 + 2.2 * k
    body = []
    for st in order_:
        t, lines_ = p06_site_lines(st)
        while len(t) > 3 and r28mv_tw(t, h75, True) > tw_:
            t = t[:-2].rstrip(u" ,·–") + u"…"
        wrapped = []
        for s_ in lines_:
            wrapped.append((s_, len(r28mv_lines(s_, tw_, h7))))
        body.append((t, wrapped))
    hmax = max(sum(n_ for s_, n_ in wr) for t, wr in body)
    bh = hb + 1.6 * k + h7 + (hmax - 1) * R28MV_LEAD * h7 + 1.6 * k
    for i, (st, (t, wr)) in enumerate(zip(order_, body)):
        bx = x0 + i * (bw + g)
        lab, col, ang = p06_hatch_spec(st["key"])
        cx_ = bx + 0.5 * bw
        if "px" in st:                                    # leader: down from the square, then to the box
            B.line([(st["px"], st["py"] - 1.7 * k), (st["px"], ystrip), (cx_, ytop)], MPL["ink_dark"], L, 58,
                   bk_lw(0.15, k))
        q = rect(bx, ytop - bh, bx + bw, ytop)
        B.fill([q], WHITE, L, 30)
        B.fill([rect(bx, ytop - hb, bx + bw, ytop)], col, L, 31)
        B.line(q + [q[0]], col, L, 32, bk_lw(0.2, k))
        B.text(t, bx + 1.2 * k, ytop - 0.5 * (hb + h75), h75, WHITE, L, order=33, font=FONT_TITLE, bold=True)
        yl = ytop - hb - 1.6 * k - h7
        for s_, n_ in wr:
            r28mv_para(B, s_, bx + 1.2 * k, yl, tw_, h7, INK, L, order=40)
            yl -= n_ * R28MV_LEAD * h7
    return ytop - bh


# ------------------------------------------------------------ p.06
def draw_edge_build(S, B, x, y, w, U, with_photos=True):
    """v51 (revision 29 Oct, WO-T3a-4; D1 a: p.22 merged into p.06): THE STREAM EDGE AND WHERE WE CAN BUILD (p.06,
    crop drw_edge_build). The whole frame as ONE strip at 1:10,000 on the booklet page (r28e_strip on the basemap's
    detailed mode: the edge every 4 m on both banks, walls and embankments, where we can build hatched in four
    classes, the six largest pieces outlined and lettered, bridges K1-K6, street, mahalle and heritage names,
    contours, the study area, the photo viewpoints), its scale bar and north arrow under it on the side with fewer
    sites; beside it THE EDGE, the walled / embanked rings and WHERE WE CAN BUILD (p06_build_panel); under them a box
    a site (p06_site_boxes), the map's key, the photos four to a row in the height left (the page's BK_AH).
    with_photos=False (the retired p.22 copy, drw_edge_build_e) draws nothing. Drawn for the full booklet panel
    width (BK_AW). Returns the y below."""
    L = "LU_BOARD::EdgeBuild"
    if not with_photos:
        LOG.append(u"The p.22 copy of the stream edge plan (drw_edge_build_e) is retired (D1 a): nothing drawn.")
        return y
    F = S.F
    k = w / BK_AW
    top = y
    h7, h75, h9 = bk_hk(7.0, k), bk_hk(7.5, k), bk_hk(9.0, k)
    photos = []
    try:
        photos = photo_files(os.path.join(SELINUS_RES_DIR, "_site_photos"))
    except Exception:
        LOG.append("WARNING: the site photos could not be read for the stream edge plan:\n" + traceback.format_exc())
    O = p06_open(S)
    V, ss, r, dropped = r28e_strip(S, B, x, top, k, L, photos, O["sites"])
    span = R28E_SB_M * ss + 18.0 * k                      # the scale bar on the side with fewer site leaders
    n_l = len([s_ for s_ in O["sites"] if s_.get("px", 0.0) < r[0] + span])
    n_r = len([s_ for s_ in O["sites"] if s_.get("px", 0.0) > r[2] - span])
    foot = b_foot(B, F, x if n_l <= n_r else r[2] - span, r[1], ss, k, L, R28E_SB_M)
    cx0 = r[2] + R28E_GAP * k                             # the column beside the strip
    cw = x + w - cx0
    yy, wl_, em_ = r28e_edge_panel(S, B, cx0, top, cw, k, L)
    yy -= 2.5 * k
    y1 = r28e_rings(B, cx0, yy, wl_, em_, k, L)
    y2 = p06_build_panel(S, B, cx0 + 44.0 * k, yy, cw - 44.0 * k, k, L)
    ys = p06_site_boxes(B, O["sites"], x, r[2], min(foot, y1, y2) - 3.0 * k, r[1], k, L)
    low = r28e_key(B, r28e_key_rows(bool(photos)), x, min(ys, y1, y2) - 3.0 * k, 6, w / 6.0, k, L)
    bot = top - BK_AH * k
    n_ph = len(photos)
    if n_ph:                                              # P06.4: the photos in the height left (D13: no credit line)
        hb = low - 3.0 * k - h75
        B.text(u"SITE PHOTOS · 1 OCT 2026 · NUMBERS AND CONES ON THE PLAN", x, hb, h75, INK, L, font=FONT_TITLE,
               bold=True)
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
               u"Where we can build: {} open to change, {:.0f}% of the analysis frame · sites {} · photo viewpoints "
               u"1-{}".format(u_area(O["open"]), 100.0 * O["open"] / max(1.0, O["frame"]),
                              u"A-" + O["sites"][-1]["id"] if O["sites"] else u"none", n_ph or 8),
               crop_scale(ss), [])
    CROP_PANELS[-1]["bk_w"] = BK_AW                       # drawn for the full booklet panel width
    LOG.append(u"Stream edge plan (p.06): ONE strip at 1:{:,}, {:.1f} x {:.1f} mm; {} open to change; {} sites; {} "
               u"photos; labels left out (G4): {}.".format(R28E_DEN, F.w * ss / k, F.h * ss / k, u_area(O["open"]),
                                                          len(O["sites"]), n_ph, u", ".join(dropped) or u"none"))
    r28e_export_open(S)
    return low - 1.0 * U


# ------------------------------------------------------------ D1: the export
def r28e_export_open(S):
    """D1: r28_open_to_change.json in SELINUS_RES_DIR, once a run: where we can build as p.06 counts and draws it
    (p06_open), {frame_ha, frame_m2, total_ha, total_m2, classes {vacant, parking, loose, bare: {ha, m2, rings
    (survey m, as drawn: traced from the counted cells and smoothed)}}, sites [{id, m2, x, y, opens_to, study,
    shares}], definition, rings, source}"""
    m = r28e_memo(S)
    if m.get("exported"):
        return
    m["exported"] = True
    try:
        O = p06_open(S)
        cls = {}
        for part, hk in P06_CLASSES:
            a = O["area"][part]
            cls[part] = {"ha": round(a / 1e4, 2), "m2": int(round(a)),
                         "rings": [[[round(p[0], 2), round(p[1], 2)] for p in P] for g in O["draw"][part] for P in g
                                   if len(P) >= 3]}
        sites = [{"id": s_["id"], "m2": int(round(s_["a"])), "x": round(s_["x"], 2), "y": round(s_["y"], 2),
                  "where": u", ".join(v for v in (s_["side"], s_["pos"]) if v), "opens_to": s_["opens"],
                  "study": round(s_["study"], 2), "shares": dict((k_, round(v, 2)) for k_, v in s_["shares"].items())}
                 for s_ in O["sites"]]
        out = {"frame_ha": round(O["frame"] / 1e4, 2), "frame_m2": int(round(O["frame"])),
               "total_ha": round(O["open"] / 1e4, 2), "total_m2": int(round(O["open"])), "classes": cls,
               "sites": sites,
               "definition": u"Open to change (site board, p.06) = the analysis frame's ground counted once on a {:.0f} "
                             u"m raster after buildings, street surfaces (and unmeasured street centre lines) and the "
                             u"stream: vacant lots and parking & yards as mapped (survey, OpenStreetMap), loose ground "
                             u"(unmapped ground ESA WorldCover 2021 classes as grassland or shrubland, and OpenStreetMap "
                             u"grass lots), bare ground (unmapped ground with no satellite class, holding a {:.0f} m "
                             u"square, {:.0f} m2 or more in one piece). A reading of what could change, not a check of "
                             u"ownership or zoning".format(REST_CELL, (2 * P06_BARE_R + 1) * REST_CELL, P06_BARE_MIN),
               "rings": u"survey m; each class's outlines as p.06 draws them (traced from the counted cells, "
                        u"simplified and smoothed); the areas are the count; fill even-odd",
               "source": u"{} · {}".format(SCRIPT_VERSION, time.strftime("%Y-%m-%d %H:%M"))}
        os.makedirs(SELINUS_RES_DIR, exist_ok=True)
        with open(R28E_OPEN_JSON, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, separators=(",", ":"))
        LOG.append(u"r28_open_to_change.json (D1): {} open to change of {} ({}; {} sites).".format(
            u_area(O["open"]), u_area(O["frame"]), R28E_OPEN_JSON, len(sites)))
    except Exception:
        LOG.append("WARNING: r28_open_to_change.json not written:\n" + traceback.format_exc())
