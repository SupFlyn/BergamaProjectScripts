# p.06 the stream edge and where we can build (split from parts/15c_review_pages.py, parts/15e_v45_pages.py,
# parts/15k_r28_edge.py on 29 Oct 2026).
# Revision 29 Oct 2026 (WO-T3a-4, D1 a: p.22 merged into p.06): ONE drawing, crop drw_edge_build. The p.22 copy
# (draw_edge_build_e, crop drw_edge_build_e) and the filter sheet (r28e_draw_filter, crop drw_filter) are gone: their
# one idea (frame -> unbuilt -> open to change) is the bar in WHERE WE CAN BUILD. Where we can build is recounted
# here on ONE 2 m raster (p06_open: every cell counted once, buildings / streets / water first), bare open ground
# added, the largest pieces named as sites A-F with boxes (R10 / R11 idea: what it is, m², what it opens to); the
# base is the basemap module's detailed mode; hatches heavier. Every m² figure is a cell count, never typed.
# Revision 30 Oct 2026 (T4, PG1 p6, D5 BOTH): the strip on the faint M3 "base" (buildings as plan, streets, the
# stream, the study area; no green, contours, street / heritage / mahalle names), where we can build the strongest
# tone, sites as filled lettered squares repeated on their boxes, labels by M2 clear of the buildings, only the m²
# the boxes explain; the page drawn twice (P06_PAL a / b), crops drw_edge_build_a, _b and drw_edge_build (= b).
# v55 (Aras 31 Oct, critique p6): the beige palette b only, ONE copy, crop drw_edge_build; palette a removed.
# v58 (round 3, P06.1, P06.2, G1-G3, G8, G16, G17): the column beside the map re-laid on the map's grid (THE EDGE bars
# with the rings at their right, WHERE WE CAN BUILD under them at full width, the map's key under that), the map at a
# booklet scale only (p06_den: 1:10,000), the column wider; sites lettered left -> right on the map, their boxes in the
# same order under the map, no leader lines, no box frames; bridges by real name (bridge_name), a label with no free spot a
# number in the map's key; photo numbers beside their camera point without a line; one FLAG overlap p06.
# v61 (round 6, S3, 4 Nov 2026; BRIEF §6 row 6 "G6-1 only" + the global rules): every colour from the hue table
# (p06_pal: context CTX, heritage HER, the stream WAT, the bank edge one MOV ramp, where we can build one CTX ramp,
# annotations ANN), the key grouped by category (legend_group); photo viewpoints as G6-4 view marks (an_view, ANN
# ink, no red); north by an_north (sb_an_north); the SON page6 overlaps cleared (rings' words, the "[n]" under the
# column titles, photo numbers kept off the bridges' numbers); G6-9 kinds on every element.


def edge_shares(S):
    """v42: {edge type: % of the bank length}, and the % walled and embanked (the key question's measure)."""
    tot = sum(S.edge_len.values())
    if tot <= 0:
        return {}, 0.0, 0.0, 0.0
    return (dict((k, 100.0 * v / tot) for k, v in S.edge_len.items()), 100.0 * S.walled_len / tot,
            100.0 * getattr(S, "embanked_len", 0.0) / tot, tot)


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


def r28e_names(S, V, k):
    """revision 30 Oct (p6 change 1, G3: no label on the buildings): the strip's one context name is the stream's
    (rank 0, italic, the water's edge tone). The street, heritage and mahalle names sat on the buildings and are gone
    (r28e_streets, r28e_heritage, r28e_mahalle deleted)."""
    rl = getattr(S, "river_label", None)
    if not rl or not S.F.inside(rl[0], rl[1]):
        return []
    px, py = V.p(rl[0], rl[1])
    return [dict(x=px, y=py, lines=[(rl[3], False)], h=bk_hk(7.0, k), col=C(hue("WAT", 2)), rank=0, italic=True,
                 key=("box", C(hue("WAT", 3))))]          # v58 (P06.2): its key row if it becomes a number; v61 WAT


def r28e_place(B, items, taken, bounds, k, L, lines=(), order=66, n0=0):
    """M2 (common/label_place.py lp_place): the labels items [dict(x, y (board units), lines [(text, bold)], h
    (capital height), col, rank, r (the target's radius, board units), italic, key (kind, ref): its key swatch)]
    placed clear of each other, of the boxes in taken (symbols) and of the polylines lines (board units: the
    stream's centre line, the building outlines, the bank edge), inside bounds. Worked in booklet mm, 7 pt, never
    smaller. v58 (round 3, P06.2, G3): no leader lines: a label that finds no free spot next to its target becomes a
    number on the spot (n0 + n: after the photo numbers 1..n0), in reading order, listed in the map's key. Returns
    [(number, text, key)] in number order; taken grows by the placed boxes."""
    mm = 1.0 / k
    pad, lead = 0.3, 1.4
    labs = []
    for it in items:
        h = it["h"] * mm
        labs.append(dict(x=it["x"] * mm, y=it["y"] * mm, rank=it.get("rank", 1), r=it.get("r", 0.0) * mm,
                         w=max(r28mv_tw(t, h, b) for t, b in it["lines"]) + 2.0 * pad,
                         h=h * (1.0 + lead * (len(it["lines"]) - 1)) + 2.0 * pad))
    hn = max([it["h"] for it in items] or [0.0]) * mm     # a number: bold, the labels' height
    idx = LpSegIndex(polylines=[[(p[0] * mm, p[1] * mm) for p in P] for P in lines if len(P) >= 2])
    got = lp_place(labs, obstacles=[tuple(v * mm for v in b) for b in taken], lines=idx,
                   bounds=tuple(v * mm for v in bounds) if bounds else None, pad=0.3, sizes=(1.0,),
                   num_wh=lambda t: (r28mv_tw(str(int(t) + n0), hn, True) + 2.0 * pad, hn + 2.0 * pad))
    numbered = []
    for it, g in zip(items, got):
        if g is None:
            continue
        b = g["box"]
        if g.get("number"):                               # v58: the number on the spot, the label in the key
            n = n0 + g["number"]
            B.text(str(n), 0.5 * (b[0] + b[2]) * k, 0.5 * (b[1] + b[3]) * k, it["h"], it["col"], L, order=order,
                   font=FONT_TITLE, bold=True, align="MC")
            numbered.append((n, u" ".join(t for t, b_ in it["lines"]), it.get("key") or ("box", WHITE)))
        else:
            x0, y1 = b[0] * k, b[3] * k
            h = it["h"]
            yl = y1 - pad * k - h
            for t, bold in it["lines"]:
                B.text(t, x0 + pad * k, yl, h, it["col"], L, order=order, font=FONT_TITLE, bold=bold,
                       italic=it.get("italic", False))
                yl -= lead * h
        taken.append(tuple(v * k for v in b))
    return sorted(numbered, key=lambda t: t[0])


def r28e_strip(S, B, x, yt, k, L, photos=(), sites=(), pal=None, den=None):
    """v50 (G7, P06.1, P06.4), revision 30 Oct (p6, D5): the whole frame as ONE strip at 1:10,000, its top-left
    corner at (x, yt), in the palette pal (P06_PAL "a" / "b"): the faint M3 base (p06_base: buildings as plan, streets,
    the stream, the study area), where we can build in p06_open's four classes (p06_hatched: the strongest tone on
    the map), the sites outlined with a filled lettered square each (s["px"], s["py"] = its page point), the edge
    every 4 m on both banks (walled and embanked marked), the six bridges as bars with their names, the photo
    viewpoints (numbered discs, view cones), the stream's name, the frame's line. Labels by M2 (r28e_place), clear of
    the buildings. v58 (round 3): at 1:den (p06_den; default R28E_DEN), bridges by their real
    name (G16), no leader lines (G3), the frame's 0.25 pt neatline kept (G17). Returns (View, board units per metre,
    the strip's rectangle, the numbered labels [(n, text, key)], the bridge bars' boxes for the overlap test)."""
    pal = pal or p06_pal()
    F = S.F
    ss = 1000.0 * k / (den or R28E_DEN)
    V = View(F, ss, x, yt)
    r = (x, yt - F.h * ss, x + F.w * ss, yt)
    CB = ClipB(B, r)
    with B.kind("frame", u"map ground"):
        B.fill([rect(*r)], WHITE, L, 1)
    if not p06_base(S, CB, V, k, L, den or R28E_DEN):
        with B.kind("annotations", u"study area"):
            draw_r28_study(S, CB, V, k, L)
    O = p06_open(S)
    for part, hk in P06_CLASSES:                          # where we can build: the map's one strong tone
        with B.kind("ground", u"where we can build " + part):     # v61 (G6-9)
            p06_hatched(CB, V, O["draw"][part], hk, k, L, 6, pal)
    ctx1 = C(hue("CTX", 1))                               # v61 (G6-6): bridges, sites, marks in CTX r1
    for i_, P in enumerate(getattr(S, "bridges", []) or []):
        with B.kind("roads", u"bridge %d" % (i_ + 1)):
            CB.line(V.P(P), ctx1, L, 25, bk_lw(0.3, k))
    lines_ = []                                           # what no label may sit on
    for i_, (typ, pts) in enumerate(getattr(S, "edge_runs", [])):    # the edge every 4 m, both banks
        Q = V.P(pts)
        with B.kind("water", u"bank edge %s %d" % (typ, i_ + 1)):
            CB.line(Q, pal["edge"][typ], L, 40, bk_lw(P06_EDGE_LINE_MM, k))
        lines_.append(Q)
    with B.kind("water", u"walled bank"):
        for pts in getattr(S, "wall_runs", []):
            for d in dashes(V.P(pts), 1.0 * k, 0.8 * k):
                CB.line(d, WHITE, L, 41, bk_lw(0.3, k))
    with B.kind("water", u"embanked bank"):
        for pts in getattr(S, "bank_runs", []):
            for d in dashes(V.P(pts), 0.2 * k, 1.0 * k):
                CB.line(d, WHITE, L, 41, bk_lw(0.3, k))
    h7 = bk_hk(7.0, k)
    taken, items, syms = [], [], []
    resv = []                                             # v61 (G6-8): room kept for a bridge's number on its spot
    for kk, nm, bx, by in BRIDGES_K:                      # the six crossings: a bar across the stream, its name
        if not F.inside(bx, by):
            continue
        px, py = V.p(bx, by)
        nrm = stream_normal(S, bx, by) or (0.0, 1.0)
        a_ = V.p(bx + nrm[0], by + nrm[1])
        ln = math.hypot(a_[0] - px, a_[1] - py) or 1.0
        e = ((a_[0] - px) / ln * 1.6 * k, (a_[1] - py) / ln * 1.6 * k)
        with B.kind("roads", u"bridge " + bridge_name(kk)):
            CB.line([(px - e[0], py - e[1]), (px + e[0], py + e[1])], ctx1, L, 45, bk_lw(0.6, k))
        taken.append((px - 1.6 * k, py - 1.6 * k, px + 1.6 * k, py + 1.6 * k))
        syms.append(taken[-1])
        resv.append((px - P06_BR_RESV * k, py - P06_BR_RESV * k, px + P06_BR_RESV * k, py + P06_BR_RESV * k))
        items.append(dict(x=px, y=py, lines=[(bridge_name(kk), True)], h=h7, col=INK, rank=0, r=1.6 * k,
                          key=("bridge", None)))      # v58 (round 3, G16): the real name, never the K code
    sq = P06_MARK_MM * k                                  # a site: its outline and a filled lettered square
    for st in sites:
        with B.kind("ground", u"site " + st["id"]):
            for g in st["rings"]:
                for P in g:
                    CB.line(V.P(list(P) + [P[0]]), pal["site"], L, 44, bk_lw(P06_SITE_MM, k))
        px, py = V.p(st["x"], st["y"])
        st["px"], st["py"] = px, py
        q = rect(px - sq, py - sq, px + sq, py + sq)
        with B.kind("annotations", u"site mark " + st["id"]):
            B.fill([q], pal["mark"], L, 62)
            B.line(q + [q[0]], WHITE, L, 63, bk_lw(0.25, k))
            B.text(st["id"], px, py, bk_hk(8.0, k), WHITE, L, order=64, font=FONT_TITLE, bold=True, align="MC")
        taken.append((px - sq - 0.3 * k, py - sq - 0.3 * k, px + sq + 0.3 * k, py + sq + 0.3 * k))
    # v61 (round 6, G6-4, PLAN P-5, frames p06 §4-5): each photo viewpoint is a G6-4 view mark (annot.py an_view: a
    # small open triangle at the camera pointing the photo's bearing, its number at 5 pt, ANN ink; no red cone, no
    # disc: red is for key-map cuts only). The number sits behind the triangle (an_view's spot) or, when that spot is
    # taken (a bridge's number, a site, another mark), at the first free spot round the camera, never on the view.
    xv = SbX(B, L, 60, k, kind="annotations")
    xcb = xv.cb()
    for j, (p, it) in enumerate(photos):
        if not F.inside(it["x"], it["y"]):
            continue
        px, py = V.p(it["x"], it["y"])
        brg = PHOTO_VIEW.get(it.get("file", "").split(".")[0], (None, None))[0]
        dir_ = 90.0                                       # no bearing: the mark points up the page
        if brg is not None:                               # bearing from true north, clockwise; survey y = north
            tip = V.p(it["x"] + math.sin(math.radians(brg)) * EB_CONE_M,
                      it["y"] + math.cos(math.radians(brg)) * EB_CONE_M)
            dir_ = math.degrees(math.atan2(tip[1] - py, tip[0] - px))
        its = list(an_view(None, (px / k, py / k), dir_, str(j + 1), None, None, page="p06"))
        tri = 0.5 * AN_VIEW["tri_mm"] * k + 0.2 * k
        tbox = (px - tri, py - tri, px + tri, py + tri)
        ti = [i_ for i_, t_ in enumerate(its) if t_[0] == "text"]
        nbox = None
        if ti:
            t_ = its[ti[0]]
            hc = t_[3] * _PDF_CAP["sans"] * k             # the number's capital height (board units)
            hw, hh = 0.5 * tw(t_[1], hc, "sans", False) + 0.3 * k, 0.5 * hc + 0.3 * k
            far = 0.5 * AN_VIEW["tri_mm"] + AN_VIEW["gap_mm"]
            cands = [(t_[2][0] * k, t_[2][1] * k)]
            for a in range(12):                           # round the camera, the view's own side left out
                ang = math.radians(dir_ + 180.0 + (a + 1) // 2 * (1 if a % 2 else -1) * 30.0)
                if abs((math.degrees(ang) - dir_ + 180.0) % 360.0 - 180.0) < 50.0:
                    continue
                d_ = far * k + max(hw, hh)
                cands.append((px + d_ * math.cos(ang), py + d_ * math.sin(ang)))
            obst = taken + resv + [tbox]
            for cx_, cy_ in cands:
                b = (cx_ - hw, cy_ - hh, cx_ + hw, cy_ + hh)
                if r[0] <= b[0] and b[2] <= r[2] and r[1] <= b[1] and b[3] <= r[3] and not _hit(b, obst):
                    nbox = b
                    break
            if nbox is None:
                cx_, cy_ = cands[0]
                nbox = (cx_ - hw, cy_ - hh, cx_ + hw, cy_ + hh)
                LOG.append(u"photo viewpoint {}: number exported behind its mark (no free spot round the camera; "
                           u"the booklet places it)".format(j + 1))     # v62 (L2): no producer-side warning
            its[ti[0]] = (t_[0], t_[1], (0.5 * (nbox[0] + nbox[2]) / k, 0.5 * (nbox[1] + nbox[3]) / k)) + tuple(t_[3:])
        basemap_draw(its, lambda q: q, xcb[0], xcb[1], xcb[2])
        taken.append(tbox)
        syms.append(tbox)
        if nbox:
            taken.append(nbox)
    items += r28e_names(S, V, k)
    for P_ in getattr(S, "selinus", None) or []:          # labels never sit on the stream's centre line ...
        lines_.append(V.P(dp_simplify(P_, 15.0)))
    for u in S.bld:                                       # ... nor on a building (G3)
        for P_ in u["parts"]:
            if P_ and len(P_) >= 3 and F.inside(P_[0][0], P_[0][1]):
                lines_.append(V.P(list(P_) + [P_[0]]))
    with B.kind("labels"):
        numbered = r28e_place(B, items, taken, (r[0] + 0.5 * k, r[1] + 0.5 * k, r[2] - 0.5 * k, r[3] - 0.5 * k), k,
                              L, lines_, n0=len(photos))
    with B.kind("frame", u"neatline"):
        B.line(rect(*r) + [(r[0], r[1])], INK, L, 70, bk_lw(0.25, k))     # G17: the map's thin neatline
    return V, ss, r, numbered, syms


# ------------------------------------------------------------ the key and the panels beside the strip
def r28e_swatch(B, kind, ref, x, y, k, L, w=6.0, h=2.4, order=20, pal=None):
    """a key sample w x h booklet mm, its top-left corner at (x, y), in the palette pal (p06_pal): box (fill ref),
    bld / her (a building / heritage building as the base draws them: fill, outline, roof ridge and hips),
    hatch / hatchline (P06_CLASSES hatch key ref: tint, hatch and edge as the strip / the hatch alone), line (ref =
    (colour, mm)), dash (ref = colour: the covered course), study (G8), bridge (a bar across the stream), edge (the
    six edge shades), walled / embanked (the bank marks), view (a G6-4 view mark), frame (the analysis frame's line),
    site (an outline and its filled square). v61 (round 6, G6-6): every colour from the hue table (p06_pal)."""
    pal = pal or p06_pal()
    w, h = w * k, h * k
    sw_ = rect(x, y - h, x + w, y)
    ym = y - 0.5 * h
    if kind == "box":
        B.fill([sw_], ref, L, order)
    elif kind in ("bld", "her"):                          # the base's buildings "plan_faint", in the table's tones
        fc, rc, ec = (pal["bld"] if kind == "bld" else pal["her"])
        B.fill([sw_], fc, L, order)
        e_ = 0.5 * h
        for P in ([(x + e_, ym), (x + w - e_, ym)], [(x, y), (x + e_, ym), (x, y - h)],
                  [(x + w, y), (x + w - e_, ym), (x + w, y - h)]):
            B.line(P, rc, L, order + 1, bk_lw(0.08, k))
        B.line(sw_ + [sw_[0]], ec, L, order + 2, bk_lw(0.1, k))
    elif kind in ("hatch", "hatchline"):
        lab, col, ang = p06_hatch_spec(ref, pal)
        if kind == "hatch":
            B.fill([sw_], mix(col, WHITE, pal["tint"]), L, order)
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
    elif kind == "bridge":
        B.fill([rect(x, ym - 0.7 * k, x + w, ym + 0.7 * k)], pal["water"], L, order)
        B.line([(x + 0.5 * w, y), (x + 0.5 * w, y - h)], pal["ctx1"], L, order + 1, bk_lw(0.6, k))
    elif kind == "edge":
        n_ = len(EDGE_ORDER)
        for i, k_ in enumerate(EDGE_ORDER):
            B.line([(x + i * w / n_, ym), (x + (i + 1) * w / n_, ym)], pal["edge"][k_], L, order,
                   bk_lw(P06_EDGE_LINE_MM, k))
    elif kind in ("walled", "embanked"):
        B.line([(x, ym), (x + w, ym)], pal["ctx1"], L, order, bk_lw(0.7, k))
        dd = (1.0, 0.8) if kind == "walled" else (0.2, 1.0)
        for d in dashes([(x, ym), (x + w, ym)], dd[0] * k, dd[1] * k):
            B.line(d, WHITE, L, order + 1, bk_lw(0.3, k))
    elif kind == "view":                                  # v61 (G6-4): the view mark as an_view draws it
        c_, hh = (x + 0.5 * w, ym), 0.5 * AN_VIEW["tri_mm"] * k
        tip, bl, br = (c_[0] + hh, c_[1]), (c_[0] - hh, c_[1] + hh), (c_[0] - hh, c_[1] - hh)
        B.line([tip, bl, br, tip], pal["ann"], L, order, bk_lw(AN_VIEW["lw"], k))
    elif kind == "frame":
        B.line(sw_ + [sw_[0]], pal["ctx1"], L, order, bk_lw(0.25, k))
    elif kind == "site":                                  # a site's outline and its filled lettered square
        B.line(sw_ + [sw_[0]], pal["site"], L, order, bk_lw(P06_SITE_MM, k))
        q = rect(x + 0.5 * w - 0.9 * k, ym - 0.9 * k, x + 0.5 * w + 0.9 * k, ym + 0.9 * k)
        B.fill([q], pal["mark"], L, order + 1)


def r28e_key(B, rows, x, y, ncol, colw, k, L, pal=None):
    """the map's key (P06.2, P06.3: it draws the hatches and outlined fills the booklet's legend cannot), rows
    [(kind, ref, label)] in ncol columns colw wide, filled column by column from (x, y) (top), 7 pt, in the palette
    pal. Returns the y under it. v61 (G6-9): each row one legend element."""
    pitch = 3.3 * k
    nrow = max(1, (len(rows) + ncol - 1) // ncol)
    h7 = bk_hk(7.0, k)
    for i, (kind, ref, lab) in enumerate(rows):
        lx, ly = x + (i // nrow) * colw, y - (i % nrow) * pitch
        with B.kind("legend", u"key %d" % (i + 1)):
            r28e_swatch(B, kind, ref, lx, ly, k, L, pal=pal)
            # v59.1: a label wider than its column is set smaller (down to 6 pt) to fit it; "15  Adnan Menderes
            # Bulvarı road bridge" ran 3 mm past the crop's right edge
            h_ = h7
            av_ = colw - 7.5 * k
            tw_ = site28_tw(lab, h7)
            if tw_ > av_ > 0:
                h_ = max(bk_hk(6.0, k), h7 * av_ / tw_)
            B.text(lab, lx + 7.0 * k, ly - 2.4 * k + 0.4 * k, h_, INK, L, font=FONT_TITLE)
    return y - nrow * pitch


def r28e_key_rows(photos=True, numbered=(), pal=None):
    """the stream edge plan's key: every layer the strip draws (revision 30 Oct: the M3 base's layers only; the
    hatches of where we can build are in their own panel, with their areas). v58 (round 3, G3, G16): no K codes; the
    labels the map shows as numbers (r28e_place: [(n, text, (kind, ref))]) one row each, in number order.
    v61 (round 6, G6-6): grouped by category in the hue table's order (legend_group: existing context CTX, heritage
    HER, the stream WAT, the bank edge as one ramp of MOV shades, then the annotations ANN), every colour from the
    table; the photo viewpoint is a G6-4 view mark (ANN ink)."""
    pal = pal or p06_pal()
    ent = [dict(cat="CTX", rank=3, row=("bld", None, u"Building")),
           dict(cat="CTX", rank=4, row=("box", pal["street"], u"Street")),
           dict(cat="CTX", rank=1, row=("bridge", None, u"Bridge")),
           dict(cat="CTX", rank=1, row=("walled", None, u"Walled bank")),
           dict(cat="CTX", rank=1, row=("embanked", None, u"Embanked bank (slope line)")),
           dict(cat="CTX", rank=1, row=("frame", None, R28_FRAME_NAME + u" (the map's edge)")),
           dict(cat="CTX", rank=1, row=("site", None, u"Site A-F: open ground in one piece")),
           dict(cat="HER", rank=4, row=("her", None, u"Heritage building")),
           dict(cat="WAT", rank=3, row=("box", pal["water"], u"Stream")),
           dict(cat="WAT", rank=2, row=("dash", pal["water_edge"], u"Covered course")),
           dict(cat="MOV", rank=1, row=("edge", None, u"Bank edge, every 4 m (THE EDGE)")),
           dict(cat="ANN", rank=1, row=("study", None, R28_STUDY_NAME))]
    if photos:
        ent.append(dict(cat="ANN", rank=2, row=("view", None, u"Photo viewpoint: its number, looking that way")))
    rows = [e_["row"] for e_ in legend_group(ent)]
    rows += [(kr[0], kr[1], u"{}  {}".format(n, t)) for n, t, kr in numbered]     # v58: the numbers on the map
    return rows


def r28e_edge_panel(S, B, x, y, w, k, L, pal=None, right=0.0):
    """THE EDGE: what meets the water, % of the bank length on both sides, six bars in the strip's edge colours
    (palette pal), from (x, y) (top), w wide; v58 (round 3, P06.1): the bars end right (board units) short of w (the
    rings sit there), the label column as wide as its longest label. Returns (the y under it, % walled, % embanked,
    the y of the bars' top)."""
    pal = pal or p06_pal()
    sh_, wl_, em_, tot = edge_shares(S)
    if tot <= 0:
        return y, wl_, em_, y
    h7, h75 = bk_hk(7.0, k), bk_hk(7.5, k)
    B.text(u"THE EDGE " + bcite(EDGE_SRC), x, y - h75, h75, INK, L, font=FONT_TITLE, bold=True)
    y -= h75 + P06_HEAD_GAP_MM * k                       # v61 (G6-8): the title's "[n]" clear of the line under it
    r28e_rich(B, u"% of **{}** of bank · both sides, **every 4 m**".format(u_dim(tot, "km")), x, y - h7, h7, INK2, L)
    y -= h7 + 2.6 * k
    lw_ = p06_edge_lw(k)                                  # v58: was 40 mm
    bw0 = max(1.0 * k, w - right - lw_ - 9.0 * k)
    vmax = max(sh_.values() or [1.0]) or 1.0
    ybars = y
    for k_ in EDGE_ORDER:
        v_ = sh_.get(k_, 0.0)
        with B.kind("legend", u"edge bar " + k_):        # v62 (L2, G6-9): a chart bar = legend (was untagged)
            B.text(EB_EDGE_LAB[k_], x, y - h7, h7, INK, L, font=FONT_TITLE)
            bx_ = x + lw_
            if v_ > 0:
                B.fill([rect(bx_, y - h7 - 0.3 * k, bx_ + bw0 * v_ / vmax, y + 0.2 * k)], pal["edge"][k_], L, 20)
            B.text(u"{:.0f}%".format(v_), bx_ + bw0 * v_ / vmax + 1.2 * k, y - h7, h7, INK, L, font=FONT_TITLE,
                   bold=True)
        y -= 3.5 * k
    return y, wl_, em_, ybars


def p06_edge_lw(k):
    """v58 (round 3, P06.1): THE EDGE's label column: its longest label at 7 pt and 2 mm"""
    return max(r28mv_tw(EB_EDGE_LAB[k_], bk_hk(7.0, k)) for k_ in EDGE_ORDER) + 2.0 * k


def p06_rings_pitch(k):
    """v58 (round 3, P06.1): the rings' spacing: the first ring's mark and word clear of the second ring"""
    return max(12.0 * k, 5.5 * k + r28mv_tw(u"walled", bk_hk(7.0, k)) + 4.0 * k)   # v61 (G6-8): was + 2.5 mm


def p06_rings_w(k):
    """v58 (round 3, P06.1): the width the two rings and their words take"""
    h7 = bk_hk(7.0, k)
    return max(p06_rings_pitch(k) + 5.5 * k + r28mv_tw(u"embanked", h7), r28mv_tw(u"disconnected", h7))


def r28e_rings(B, x, y, wl_, em_, k, L):
    """walled and embanked: two rings, each with the mark the strip draws, "disconnected" under them; top at y.
    Returns the y under them. v58 (round 3, P06.1): spaced by p06_rings_pitch (was 21 mm), p06_rings_w wide.
    v61 (round 6, G6-8, SON page6 "walled" x "embanked / disconnected"): "disconnected" a text height and 1 mm under
    the marks' words (it touched "walled"), the rings in CTX r2 on CTX r4 (G6-6)."""
    h7, h8 = bk_hk(7.0, k), bk_hk(8.0, k)
    rr = 5.0 * k
    pitch = p06_rings_pitch(k)
    yw = y
    for j, (pct, kind) in enumerate(((wl_, "walled"), (em_, "embanked"))):
        rx, ry = x + rr + j * pitch, y - rr
        with B.kind("legend", u"ring " + kind):
            vis_ring(B, rx, ry, rr, pct, C(hue("CTX", 2)), C(hue("CTX", 4)), L)
            B.text(u"{:.0f}%".format(pct), rx, ry, h8, INK, L, order=40, font=FONT_TITLE, bold=True, align="MC")
            sx, sy = rx - rr, ry - rr - 2.8 * k
            r28e_swatch(B, kind, None, sx, sy + 1.2 * k, k, L, w=4.5)
            yw = sy - 0.5 * h7
            B.text(kind, sx + 5.5 * k, yw, h7, INK, L, font=FONT_TITLE)
    yd = yw - 1.0 * k - h7                                # the words' baseline - 1 mm - a text height
    B.text(u"disconnected", x, yd, h7, INK2, L, font=FONT_TITLE)
    return yd - 1.0 * k


# ------------------------------------------------------------ v51 (WO-T3a-4): where we can build, recounted
# ONE raster of the analysis frame (REST_CELL, the cells frame_rest splits the unmapped ground on); every cell is
# counted once, in this order: buildings, street surfaces (and the centre line of every street without a measured
# width), the stream's water: never open; then vacant lots, parking & yards (OpenStreetMap / survey zones), loose
# ground (the satellite's grass or scrub on unmapped ground, and OpenStreetMap grass lots), bare ground (unmapped
# ground with no satellite class, wide enough for a P06_BARE_R opening and P06_BARE_MIN or more in one piece). Every
# m² printed is (cells) x REST_CELL²: the drawing traces the same cells, so figure and hatch agree.
P06_CLASSES = (("vacant", "open"), ("parking", "parking"), ("loose", "loose"), ("bare", "bare"))  # count -> hatch key
P06_ANG = {"open": 45.0, "parking": -45.0, "loose": 0.0, "bare": 90.0}   # hatch angles: R28_BUILD_HATCH, bare vertical
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
# revision 30 Oct (p6, D5): the palette (v55: b only, Aras 31 Oct). The base (M3 "base"), where we can build the
# strongest tone. v61 (round 6, G6-6, PLAN §2.6, Q5): every colour from the hue table (common/hues.py), built at run
# time by p06_pal (never at import: hues.py comes in with basemap.py):
#   base and context CTX (buildings r3, streets r4, bridges / walls / frame / sites r1); heritage buildings HER r4
#   fill, r3 edge; the stream WAT r3, its edge and the covered course WAT r2; annotations ANN (photo view marks ink).
#   Where we can build = ONE category, CTX shades (the table puts vacant ground under existing context; these are
#   readings of ground as it is, not proposals): mapped ground (vacant lots, parking & yards) r1, ground read from the
#   satellite (loose, bare) r2, told apart inside a rank by the hatch angle (P06_ANG); tints 0.82 to white so the
#   CTX r3 buildings stay the darker flat tone.
#   The bank edge (THE EDGE, six types) = ONE category, MOV shades (access to the water from the town's side), most
#   closed darkest: built r1, street r1-r2, walkable r2, planted r2-r3, parking r3, loose r4 (the two in-between
#   steps are the halfway mix of neighbouring ranks of the same hue: six types on a four-step ramp; no new hue).
# tint: a hatch's ground = its line colour this far to white; mark: the sites' squares; site: their outlines; head
# "class": a site box's head in its main class's colour
P06_PAL = {}                    # v61: filled once a run by p06_pal()
P06_EDGE_RANK = {"building": (1, 1), "street": (1, 2), "pedestrian": (2, 2), "green": (2, 3), "parking": (3, 3),
                 "open": (4, 4)}  # v61: MOV ranks (a, b): the halfway mix of r_a and r_b (a = b: the rank itself)
P06_CLS_RANK = {"open": 1, "parking": 1, "loose": 2, "bare": 2}     # v61: CTX rank of each where-we-can-build class
P06_HEAD_GAP_MM = 2.6           # v61 (G6-8): mm under a column title (was 1.6: its "[n]" touched the line under it)
P06_BR_RESV = 2.6               # v61 (G6-8): mm, half the room kept round a bridge for its number (photo numbers 6-8
                                # sat on bridge numbers 11-13 in SUBMISSION_SON page6)


def p06_pal():
    """v61 (round 6, G6-6): the page's palette from the hue table (hue(), common/hues.py), built once a run"""
    if "b" in P06_PAL:
        return P06_PAL["b"]
    h_ = lambda c_, r_: C(hue(c_, r_))
    edge = {}
    for k_ in EDGE_ORDER:
        ra, rb = P06_EDGE_RANK.get(k_, (4, 4))
        edge[k_] = h_("MOV", ra) if ra == rb else mix(h_("MOV", ra), h_("MOV", rb), 0.5)
    P06_PAL["b"] = dict(name="b", tint=0.82, mark=h_("CTX", 1), site=h_("CTX", 1), head="class", ctx1=h_("CTX", 1),
                        cls=dict((k_, h_("CTX", r_)) for k_, r_ in P06_CLS_RANK.items()), edge=edge,
                        bld=(h_("CTX", 3), h_("CTX", 4), h_("CTX", 3)),        # fill, roof marks, outline
                        her=(h_("HER", 4), h_("HER", 3), h_("HER", 3)),
                        street=h_("CTX", 4), other=h_("CTX", 5), water=h_("WAT", 3), water_edge=h_("WAT", 2),
                        ring=(h_("CTX", 2), h_("CTX", 4)), ann=C(hue("ANN", "ink")),
                        # the M3 base's own tones (basemap.py BM_FAINT, plan_faint heritage) -> the table's
                        base={crop_hex(C(BM_FAINT["bld_veryfaint"])): hue("CTX", 3),
                              crop_hex(C(BM_FAINT["bld"])): hue("CTX", 4),
                              crop_hex(C(BM_FAINT["road"])): hue("CTX", 4),
                              crop_hex(C(BM_FAINT["road_line"])): hue("CTX", 3),
                              P06_BASE_HER[0]: hue("HER", 4), P06_BASE_HER[1]: hue("HER", 3)})
    return P06_PAL["b"]


P06_BASE_LAYERS = ("buildings", "streets", "water", "study_area")   # the M3 "base" layers p.06 needs (no green, contours)
P06_BASE_KIND = (("streets", "roads"), ("water", "water"), ("buildings", "buildings"), ("study_area", "annotations"))
#                 v61 (G6-9): the base layers in basemap_items' own draw sequence, each with its kind
P06_BASE_HER = ("F1E6E5", "CDAAAA")   # the M3 base's heritage fill / edge (basemap.py plan_faint): kind heritage
P06_EDGE_LINE_MM = 0.5          # mm: the bank edge line on the booklet page (was 0.7: it crowded the areas)
P06_MARK_MM = 1.9               # mm: half a site's square
P06_HATCH_MM = (0.8, 0.2)       # mm: hatch spacing and line weight on the booklet page (were 1.0, 0.12)
P06_EDGE_MM = 0.15              # mm: each open piece's edge in its hatch colour
P06_SITE_MM = 0.35              # mm: a site's outline
P06_SCALES = (200, 250, 500, 1000, 2000, 2500, 5000, 10000, 20000)   # v58: the only booklet scales (Aras 26 Oct)
P06_BAR_MIN_MM = 22.0           # mm: v58 (round 3, P06.1) the longest of THE EDGE's bars at least (the 62% one)
P06_SRC = (u"Land cover: ESA WorldCover 10 m 2021 v200 (CC BY 4.0, contains modified Copernicus Sentinel data "
           u"2021). Lots, parking, grass and streets: © OpenStreetMap contributors (ODbL).")


def p06_hatch_spec(key, pal=None):
    """(legend name, colour, hatch angle) of a P06_CLASSES hatch key in the palette pal (P06_PAL, default "b")"""
    pal = pal or p06_pal()
    return P06_LABEL[key], pal["cls"][key], P06_ANG[key]


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
    """a site's place in words: (side of the stream, "by Üç Kemer Köprüsü" / "between Ulucami Önü Köprüsü and
    Tabak Köprüsü" / "beyond ... road bridge"). v58 (round 3, G16): bridges by bridge_name (the full name: the site boxes
    have no bridge key), never a K code."""
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
            pos = u"by " + bridge_name(kk)
        else:
            u_ = F.local(x, y)[0]
            lo = [b_ for b_ in br if b_[1] <= u_]
            hi = [b_ for b_ in br if b_[1] > u_]
            if lo and hi:
                pos = u"between {} and {}".format(bridge_name(max(lo, key=lambda b_: b_[1])[0]),
                                                  bridge_name(min(hi, key=lambda b_: b_[1])[0]))
            else:
                pos = u"beyond " + bridge_name((max(lo, key=lambda b_: b_[1]) if lo else
                                                min(hi, key=lambda b_: b_[1]))[0])
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
    # v58 (round 3, P06.2, G3): lettered in reading order on the map: left -> right (the frame's u = page x), ties
    # top -> bottom (v = page y, up); the boxes under the map follow the letters
    sites.sort(key=lambda s_: (F.local(s_["x"], s_["y"])[0], -F.local(s_["x"], s_["y"])[1]))
    for i, s_ in enumerate(sites):
        s_["id"] = P06_LETTERS[i]
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


def p06_base(S, CB, V, k, L, den=None):
    """revision 30 Oct (p6 change 1, M3): the strip's base = the basemap module's faint "base" mode inside the frame,
    only the layers the page needs (buildings as plan, M11; streets; the stream, M5; the study area, ONE outline):
    its fills at order 3 (under the hatches), its lines at 9 (over them), no texts. Drawn in booklet mm (so M5's
    water reads its own mm sizes) and scaled to the board. Returns True; without the basemap file False after the
    board's own base (r28e_base) without its open-ground layers. v58 (round 3): den = the map's scale (p06_den).
    The stream: M5 water_plan via basemap_draw (G8: no squiggle, no low-flow or centre line)."""
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
        return False
    xs, ys = [p[0] for p in S.F.P], [p[1] for p in S.F.P]
    # v59 (round 4, G-R4-4, P06): the faint base kept (K1: its tones match the WHERE WE CAN BUILD bar and the key);
    # its fills at 3 and now its lines at 5, both under the hatches (6): base back, project front; only the study
    # line (one style, R28_STUDY_LINE) above the project's lines (43), under the marks
    # v61 (round 6): one layer at a time in the basemap's own sequence (streets, the stream, buildings, the study
    # area), each its G6-9 kind; the base's faint tones mapped to the hue table's (p06_pal()["base"], G6-6)
    bmap = p06_pal()["base"]
    st_c = crop_hex(R28_STUDY_LINE["colour"])

    def col_(hx, alpha):
        if isinstance(hx, str):
            hx = bmap.get(crop_hex(hx), hx)
        c_ = C(hx) if isinstance(hx, str) else tuple(int(v) for v in hx[:3])
        return mix(c_, WHITE, 1.0 - alpha) if alpha is not None and alpha < 1.0 else c_

    def up(P):
        return [(p[0] * k, p[1] * k) for p in P]

    def her_(hx):                                         # v61 (G6-9): a heritage building's fill / edge
        return CB.kind("heritage") if isinstance(hx, str) and crop_hex(hx) in P06_BASE_HER else _SbNoKind()

    def fill_fn(rings, hx, alpha, nonzero):
        col = col_(hx, alpha)
        with her_(hx):
            CB.fill([up(R) for R in rings], r28_nz(col) if nonzero else col, L, 3)

    def line_fn(pts, hx, width_mm, dash_mm, alpha):
        col, lw, P = col_(hx, alpha), bk_lw(width_mm or 0.1, k), up(pts)
        od = 43 if dash_mm and isinstance(hx, str) and crop_hex(hx) == st_c else 5     # v59 (G-R4-4)
        with her_(hx):
            if dash_mm:
                pat = list(dash_mm) if isinstance(dash_mm, (tuple, list)) else [dash_mm, dash_mm]
                for d in r28_pattern(P, [m_ * k for m_ in (pat if len(pat) >= 2 else pat * 2)]):
                    CB.line(d, col, L, od, lw)
            else:
                CB.line(P, col, L, od, lw)
    for lay_, kd_ in P06_BASE_KIND:
        if lay_ not in P06_BASE_LAYERS:
            continue
        items = basemap_items("base", override=[lay_], box=(min(xs), min(ys), max(xs), max(ys)), D=D,
                              scale_den=den or R28E_DEN)
        with CB.kind(kd_, None if kd_ in ("buildings", "roads") else lay_):   # buildings / streets: each its own
            basemap_draw(items, lambda p: tuple(v / k for v in V.p(p[0], p[1])), fill_fn, line_fn, None)
    LOG.extend(basemap_warnings())
    return True


def p06_hatched(CB, V, groups, key, k, L, order, pal=None):
    """one class of where we can build in the palette pal: tint (pal["tint"]), hatch (P06_HATCH_MM) and a thin edge
    in its colour"""
    pal = pal or p06_pal()
    lab, col, ang = p06_hatch_spec(key, pal)
    chunk = []
    for i, g in enumerate(groups):
        chunk.extend(g)
        if len(chunk) >= 400 or i == len(groups) - 1:
            Ps = V.Ps(chunk)
            CB.fill(Ps, mix(col, WHITE, pal["tint"]), L, order)
            CB.hatch(Ps, col, L, order + 1, P06_HATCH_MM[0] * k, math.radians(ang), bk_lw(P06_HATCH_MM[1], k))
            for P in Ps:
                CB.line(P + [P[0]], col, L, order + 1, bk_lw(P06_EDGE_MM, k))
            chunk = []


def p06_build_panel(S, B, x, y, w, k, L, pal=None):
    """WHERE WE CAN BUILD beside the strip (p.22's filter folded in as one bar): the figure, the analysis frame as one
    bar (open to change by class in the palette pal, other unbuilt ground, streets, buildings, the stream: p06_open's
    counts), the four classes with their m². Top at y. Returns the y under it. v58 (round 3, P06.1): the four classes
    two to a row, left -> right then top -> bottom (the column's height matches the map's)."""
    pal = pal or p06_pal()
    O = p06_open(S)
    h65, h7, h75 = bk_hk(6.5, k), bk_hk(7.0, k), bk_hk(7.5, k)
    B.text(u"WHERE WE CAN BUILD " + bcite(P06_SRC), x, y - h75, h75, INK, L, font=FONT_TITLE, bold=True)
    y -= h75 + P06_HEAD_GAP_MM * k                       # v61 (G6-8, SON page6 "WHERE WE CAN BUILD" x "[6]")
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
            lab, col, ang = p06_hatch_spec(hk, pal)
            with B.kind("legend", u"build bar " + part):  # v62 (L2, G6-9): the bar's parts, one element each
                B.fill([q], mix(col, WHITE, pal["tint"]), L, 20)
                B.hatch([q], col, L, 21, P06_HATCH_MM[0] * k, math.radians(ang), bk_lw(P06_HATCH_MM[1], k))
            cx_ += sw
    x_open = cx_
    # v61 (G6-6): the frame's other parts in the map's tones from the hue table (other unbuilt CTX r5, streets
    # CTX r4, buildings CTX r3, the stream WAT r3; SON had streets and buildings in each other's base tone)
    for nm_, key, col, tc in ((u"other unbuilt", "other", pal["other"], INK),
                              (u"streets", "streets", pal["street"], INK),
                              (u"buildings", "buildings", pal["bld"][0], INK),
                              (u"stream", "stream", pal["water"], INK)):
        sw = w * O["bar"][key] / fr
        if sw <= 0.0:
            continue
        with B.kind("legend", u"build bar " + key):
            B.fill([rect(cx_, y - bh, cx_ + sw, y)], col, L, 20)
            # v62 (L2): the name always (was: only where it fitted the bar); the booklet moves it off a narrow bar
            B.text(nm_, cx_ + 0.6 * k, y - 0.5 * (bh + h65), h65, tc, L, order=24, font=FONT_TITLE)
        cx_ += sw
    with B.kind("legend", u"build bar outline"):
        B.line(rect(x, y - bh, x + w, y) + [(x, y - bh)], INK, L, 22, bk_lw(0.15, k))
    yb = y - bh - 1.0 * k                                 # a bracket under the open part
    if x_open - x > 1.0 * k:
        B.line([(x, yb + 0.6 * k), (x, yb), (x_open, yb), (x_open, yb + 0.6 * k)], INK, L, 22, bk_lw(0.15, k))
    yt_ = yb - 0.8 * k - h65                              # under the bracket its name; at the bar's end the frame
    B.text(u"open to change", x, yt_, h65, INK, L, font=FONT_TITLE, bold=True)
    t_ = p06_bar_text(O)
    B.text(t_, x + w - r28mv_tw(t_, h65), yt_, h65, INK2, L, font=FONT_TITLE)
    y = yt_ - 2.4 * k
    for i, (part, hk) in enumerate(P06_CLASSES):         # v58: two to a row
        cx_ = x + (i % 2) * 0.5 * w
        cy_ = y - (i // 2) * 4.2 * k
        with B.kind("legend", u"class " + part):
            r28e_swatch(B, "hatch", hk, cx_, cy_, k, L, h=3.0, pal=pal)
            r28e_rich(B, p06_class_text(O, part, hk, pal), cx_ + 7.5 * k, cy_ - 2.5 * k, h7, INK, L)
    return y - ((len(P06_CLASSES) + 1) // 2) * 4.2 * k


def p06_bar_text(O):
    """v58 (round 3, P06.1): the words at the frame bar's end (shared by the panel and its width, p06_den)"""
    return u"whole bar: {} {}".format(R28_FRAME_NAME.lower(), u_area(max(1.0, O["frame"])))


def p06_class_text(O, part, hk, pal=None):
    """v58 (round 3, P06.1): a class row of WHERE WE CAN BUILD, with **bold**"""
    return u"**{}** · {}".format(p06_hatch_spec(hk, pal)[0], u_area(O["area"][part]))


def p06_rich_w(s_, h):
    """v58 (round 3, P06.1): the width of a one-line text with **bold** runs at capital height h"""
    return sum(r28mv_tw(t_, h, i % 2 == 1) for i, t_ in enumerate(s_.split(u"**")))


def p06_den(S, x_w, k, pal=None):
    """v58 (round 3, P06.1, G2): the map's scale denominator. The column beside the map needs a least width (THE
    EDGE bars at least P06_BAR_MIN_MM with the rings at their right; the frame bar's words; two class rows side by
    side); the map takes the largest booklet scale (P06_SCALES, Aras 26 Oct: only these, never a rounded value) whose
    width fits the rest of the panel width x_w (board units) less the gap; the column takes the remainder (1:10,000
    on p.06)."""
    O = p06_open(S)
    h65, h7 = bk_hk(6.5, k), bk_hk(7.0, k)
    cw_a = p06_edge_lw(k) + P06_BAR_MIN_MM * k + 9.0 * k + 3.0 * k + p06_rings_w(k)
    cw_b = r28mv_tw(u"open to change", h65, True) + 3.0 * k + r28mv_tw(p06_bar_text(O), h65)
    cw_c = 2.0 * (7.5 * k + max(p06_rich_w(p06_class_text(O, part, hk, pal), h7) for part, hk in P06_CLASSES)
                  + 2.0 * k)
    room = x_w - R28E_GAP * k - max(cw_a, cw_b, cw_c)
    fit = [d_ for d_ in P06_SCALES if 1000.0 * S.F.w * k / d_ <= room]
    if not fit:
        LOG.append(u"WARNING: p.06: no booklet scale fits the map's room ({:.1f} mm); drawn at 1:{:,}.".format(
            room / k, R28E_DEN))
        return R28E_DEN
    return min(fit)


def p06_site_lines(st):
    """a site box's text (G4: one headline value plus a line): (the m², [what it is and where; what it opens to and
    the study area], with **bold**)"""
    where = u", ".join(v for v in (st["side"], st["pos"]) if v)
    what = u" + ".join(P06_WHAT[hk] for part, hk in P06_CLASSES if st["shares"][part] >= 0.2) or P06_WHAT[st["key"]]
    what = what[:1].upper() + what[1:]
    l1 = u"**{}**, {}".format(what, where[:1].lower() + where[1:]) if where else u"**{}**".format(what)
    opens = (u"opens to " + u", ".join(P06_OPEN_TO[o] for o in st["opens"])) if st["opens"] else \
        u"closed in by buildings"
    stdy = (u"inside the study area" if st["study"] >= 0.5 else
            u"partly in the study area" if st["study"] > 0.0 else u"outside the study area")
    return u_area(st["a"]), [l1, opens[:1].upper() + opens[1:] + u" · " + stdy]


def p06_site_boxes(B, sites, x0, x1, ytop, k, L, pal=None):
    """R10 / R11, revision 30 Oct (p6 change 3): one box a site, side by side under the map from (x0, ytop) to x1.
    Its head bar repeats the map's marker (the letter in the same square, the head in the site's main class's colour)
    with the m² as the headline; under it what it is and where, what it opens to and the study area. v58 (round 3,
    P06.2, G3, G17): in letter order (= left -> right on the map, p06_open), under the map at its width, no leader lines,
    no frame stroke (whitespace and the grid separate them). Returns the y under them."""
    if not sites:
        return ytop
    pal = pal or p06_pal()
    h7, h9 = bk_hk(7.0, k), bk_hk(9.0, k)
    order_ = sorted(sites, key=lambda s_: s_["id"])
    n, g = len(order_), 3.0 * k
    bw = (x1 - x0 - (n - 1) * g) / n
    tw_ = bw - 2.4 * k
    hb = h9 + 2.6 * k
    sq = hb - 1.4 * k
    body = []
    for st in order_:
        head, lines_ = p06_site_lines(st)
        body.append((head, [(s_, len(r28mv_lines(s_, tw_, h7))) for s_ in lines_]))
    hmax = max(sum(n_ for s_, n_ in wr) for t, wr in body)
    bh = hb + 1.6 * k + h7 + (hmax - 1) * R28MV_LEAD * h7 + 1.6 * k
    for i, (st, (head, wr)) in enumerate(zip(order_, body)):
        bx = x0 + i * (bw + g)
        # v61 (G6-6): the head in its main class's colour as the table gives it (CTX r1 / r2), no darkening
        with B.kind("labels", u"site box " + st["id"]):      # v61 (G6-9)
            col = pal["mark"] if pal.get("head") != "class" else p06_hatch_spec(st["key"], pal)[1]
            B.fill([rect(bx, ytop - hb, bx + bw, ytop)], col, L, 31)
            mx0, my = bx + 0.7 * k, ytop - 0.5 * hb           # the marker again: a white square, the letter in col
            B.fill([rect(mx0, my - 0.5 * sq, mx0 + sq, my + 0.5 * sq)], WHITE, L, 33)
            B.text(st["id"], mx0 + 0.5 * sq, my, bk_hk(8.0, k), col, L, order=34, font=FONT_TITLE, bold=True,
                   align="MC")
            B.text(head, mx0 + sq + 1.4 * k, my - 0.5 * h9, h9, WHITE, L, order=34, font=FONT_TITLE, bold=True)
            yl = ytop - hb - 1.6 * k - h7
            for s_, n_ in wr:
                r28mv_para(B, s_, bx + 1.2 * k, yl, tw_, h7, INK, L, order=40)
                yl -= n_ * R28MV_LEAD * h7
    return ytop - bh


class _P06Rec(object):
    """v58 (round 3, G3): a Board as p.06 sees it: every call goes on to B (B None: a dry run that draws nothing, to
    measure a block's height), and the box of each text it sets (txt) and each image (img) is kept for the page's
    overlap test (lp_overlap_flag). rec False: texts not kept (a photo's own number tag, part of the photo)."""

    def __init__(self, B):
        self.B, self.txt, self.img, self.rec = B, [], [], True

    def __getattr__(self, k_):
        if self.B is None:
            return lambda *a, **kw: None
        return getattr(self.B, k_)

    def kind(self, kind, eid=None):
        """v61 (G6-9): the Board's element tag (a dry run: nothing to tag)"""
        return self.B.kind(kind, eid) if self.B is not None else _SbNoKind()

    def text(self, txt, x, y, h, *a, **kw):
        if self.rec and txt:
            bold = kw.get("bold", a[4] if len(a) > 4 else False)
            al = (kw.get("align", a[5] if len(a) > 5 else "L") or "L").upper()
            tw_ = r28mv_tw(u"{}".format(txt), h, bold)
            x0 = x - tw_ if al[-1] == "R" else x - 0.5 * tw_ if al[-1] == "C" else x
            y0 = y - 0.5 * h if len(al) == 2 and al[0] == "M" else y
            self.txt.append((x0, y0, x0 + tw_, y0 + h))
        if self.B is not None:
            self.B.text(txt, x, y, h, *a, **kw)

    def image(self, path, x0, y0, x1, y1, *a, **kw):
        self.img.append((min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)))
        if self.B is not None:
            self.B.image(path, x0, y0, x1, y1, *a, **kw)


def p06_column(S, B, x, y, w, ybot, k, L, pal=None):
    """v58 (round 3, P06.1, G2): the column beside the map on its grid, top at y (the map's top), w wide: row 1 THE
    EDGE (title, line, the six bars) with the walled / embanked rings at the bars' right; row 2 WHERE WE CAN BUILD at
    the full width, its bottom on the map's bottom ybot when the rows leave room (else right under row 1). No gap
    beside the map. Returns the y under it."""
    rw = p06_rings_w(k)
    ya, wl_, em_, ybars = r28e_edge_panel(S, B, x, y, w, k, L, pal, right=rw + 3.0 * k)
    yr = r28e_rings(B, x + w - rw, ybars, wl_, em_, k, L)
    ya = min(ya, yr) - 2.5 * k
    hb = ya - p06_build_panel(S, _P06Rec(None), x, ya, w, k, L, pal)     # dry run: the panel's height
    return p06_build_panel(S, B, x, min(ya, ybot + hb), w, k, L, pal)


# ------------------------------------------------------------ p.06
def p06_page(S, B, x, top, w, k, L, photos, O, pal):
    """one copy of p.06 in the palette pal (D5), top-left at (x, top), w wide (the full booklet panel): the strip
    (r28e_strip), its scale bar and north arrow under it, a box a site under them (p06_site_boxes, the map's width);
    beside them the column (p06_column: THE EDGE, the walled / embanked rings, WHERE WE CAN BUILD; then the map's key
    in two columns, G1); the photos four to a row in the height left (the page's BK_AH). v58 (round 3, P06.1): the
    map's scale from p06_den (a booklet scale only: 1:10,000); one FLAG overlap p06. Returns (the y below, board
    units per metre, the numbered map labels [(n, text, key)])."""
    F = S.F
    B = _P06Rec(B)                                        # v58 (G3): keeps every text box for the overlap test
    h7, h75, h9 = bk_hk(7.0, k), bk_hk(7.5, k), bk_hk(9.0, k)
    den = p06_den(S, w, k, pal)
    i0_map = sb_mark(B)                                   # v59 closing (G-R4-1): the map's own texts from here
    V, ss, r, numbered, syms = r28e_strip(S, B, x, top, k, L, photos, O["sites"], pal, den)
    sb_keep(B, r, u"p06 edge map", "map", i0_map)         # its names and numbers may sit on it, no other text
    # v58: no site leaders any more: always at the left. v59 (round 4, G-R4-9): b_foot's scale bar, and THE north
    # arrow (_sb_north: keymap.north_items, no white half) in its place
    # v61 (round 6, G6-4): the plain north arrow of annot.py (an_north) outside the map, by sb_an_north
    sbx = x + 1.0 * k
    with B.kind("annotations", u"scale bar"):
        low_sb = draw_scalebar_bk(B, sbx, r[1] - 2.5 * k, ss, R28E_SB_M, k, L)
    nb_ = sb_an_north(B, math.atan2(math.cos(F.ang), math.sin(F.ang)), sbx + R28E_SB_M * ss + 10.0 * k,
                      r[1] - 5.5 * k, 5.0, k, L)
    foot = min(low_sb, nb_[1])
    cx0 = r[2] + R28E_GAP * k                             # the column beside the strip
    ycol = p06_column(S, B, cx0, top, x + w - cx0, r[1], k, L, pal)
    # v58 (lead, G1): the boxes under the map at its width; the map's key in the column under WHERE WE CAN BUILD,
    # two columns, beside the map and the boxes
    ys = p06_site_boxes(B, O["sites"], x, r[2], foot - 3.0 * k, k, L, pal)
    i0_key = sb_mark(B)                                   # v59 closing (G-R4-1): the key's own texts from here
    yk = r28e_key(B, r28e_key_rows(bool(photos), numbered, pal), cx0, ycol - 3.0 * k, 2, 0.5 * (x + w - cx0), k, L,
                  pal)
    hue_log("p06", log=LOG)                               # v61 (G6-6): `legend p06 hues=table`
    sb_keep(B, (cx0, yk, x + w, ycol - 3.0 * k), u"p06 map key", "legend", i0_key)
    low = min(ys, yk)
    bot = top - BK_AH * k
    n_ph = len(photos)
    if n_ph:                                              # P06.4: the photos in the height left (D13: no credit line)
        hb = low - 3.0 * k - h75
        B.text(u"SITE PHOTOS · 1 OCT 2026 · NUMBERS AND CONES ON THE PLAN", x, hb, h75, INK, L, font=FONT_TITLE,
               bold=True)
        py0 = hb - 3.0 * k
        cols, g = 4, 3.0 * k
        rows_ = (n_ph + cols - 1) // cols
        cap_h = 1.2 * k + h7 + 2.2 * k                    # caption under each photo and the row gap
        # v59 (round 4, P06.2, G-R4-3; Aras U60 "the bottom images do not line up with the top-right description"):
        # the photos share the edges of the blocks above: n_l of each row under the map (from its left edge x to its
        # right edge r[2]) and n_r under the column (from its left edge cx0 to the page's right edge x + w), each
        # group justified edge to edge (first photo on the left edge, last on the right edge); one height for all,
        # 4:3 as taken, as large as the narrower group and the height left allow
        W_l, W_r = r[2] - x, x + w - cx0
        n_r = max(1, min(cols - 1, int(round(cols * W_r / max(1e-9, W_l + W_r)))))
        n_l = cols - n_r
        pw_max = min((W_l - (n_l - 1) * g) / n_l, (W_r - (n_r - 1) * g) / n_r)
        ph = max(10.0 * k, min(pw_max * 0.75, (py0 - bot - 1.0 * k + 2.2 * k) / rows_ - cap_h))
        pw = ph / 0.75                                    # never stretched: 4:3 as taken
        g_l = (W_l - n_l * pw) / (n_l - 1) if n_l > 1 else 0.0
        g_r = (W_r - n_r * pw) / (n_r - 1) if n_r > 1 else 0.0
        bn = 4.2 * k
        for j, (p, it) in enumerate(photos):
            c_ = j % cols
            if c_ < n_l:                                  # under the map
                px = x + c_ * (pw + g_l) if n_l > 1 else x
            else:                                         # under the column (a lone photo on its left edge,
                px = cx0 + (c_ - n_l) * (pw + g_r)        # where the column's words start)
            py = py0 - (j // cols) * (ph + cap_h)
            i0_ph = sb_mark(B)                            # v59 closing (G-R4-1): the photo's tag and caption
            with B.kind("annotations", u"photo %d" % (j + 1)):   # v62 (L2): was "other"
                B.image(p, px, py - ph, px + pw, py, L, order=5)
            with B.kind("labels", u"photo tag %d" % (j + 1)):    # v61 (P-5): the tag in ANN ink, not red
                B.fill([rect(px, py - bn, px + bn, py)], pal["ann"], L, 64)
                B.rec = False                             # the photo's number tag sits on the photo by design
                B.text(str(j + 1), px + 0.5 * bn, py - 0.5 * bn, h9, WHITE, L, order=65, font=FONT_TITLE, bold=True,
                       align="MC")
                B.rec = True
            B.text(eb_caption(it, pw, h7), px, py - ph - 1.2 * k - h7, h7, INK, L, font=FONT_TITLE)
            sb_keep(B, (px, py - ph, px + pw, py), u"p06 photo %d" % (j + 1), "photo", i0_ph)   # no other text on it
        low = py0 - rows_ * (ph + cap_h) + 2.2 * k
        if low < bot + 0.5 * k:
            LOG.append(u"WARNING: the stream edge plan's photos end {:.1f} mm below the booklet page's area "
                       u"(palette {}).".format((bot + 0.5 * k - low) / k, pal["name"]))
    # v58 (round 3, G3): the page's overlap test: every text set here vs each other, vs the bridge bars and the
    # photos, and vs the page's panel
    lp_overlap_flag("p06", B.txt, list(syms) + B.img, bounds=(x, bot, x + w, top))
    an_log("p06", log=LOG)                                # v61 (G6-4): `annot p06 cuts=0 levels=0` (view marks only)
    LOG.append(sb_tree_log("p06"))                        # v61 (G6-10): the M3 base draws no trees on p.06
    LOG.append(u"p.06 layout (v58, P06.1): map {:.1f} x {:.1f} mm at 1:{:,}; column {:.1f} mm wide; key in the column "
               u"ends {:.1f} mm {} the site boxes.".format(
                   (r[2] - r[0]) / k, (r[3] - r[1]) / k, den, (x + w - cx0) / k, abs(yk - ys) / k,
                   u"above" if yk > ys else u"below"))
    return low, ss, numbered


def draw_edge_build(S, B, x, y, w, U, with_photos=True):
    """v51, revision 30 Oct (p6, D5 BOTH): THE STREAM EDGE AND WHERE WE CAN BUILD (p.06). The page (p06_page) drawn
    once in the beige palette b (v55, Aras 31 Oct), crop drw_edge_build. with_photos=False (the retired p.22 copy, drw_edge_build_e)
    draws nothing. Drawn for the full booklet panel width (BK_AW). Returns the y below."""
    L = "LU_BOARD::EdgeBuild"
    if not with_photos:
        LOG.append(u"The p.22 copy of the stream edge plan (drw_edge_build_e) is retired (D1 a): nothing drawn.")
        return y
    F = S.F
    k = w / BK_AW
    photos = []
    try:
        photos = photo_files(os.path.join(SELINUS_RES_DIR, "_site_photos"))
    except Exception:
        LOG.append("WARNING: the site photos could not be read for the stream edge plan:\n" + traceback.format_exc())
    O = p06_open(S)
    n_ph = len(photos)
    cap = (u"Where we can build: {} open to change, {:.0f}% of the analysis frame · sites {} · photo viewpoints "
           u"1-{}".format(u_area(O["open"]), 100.0 * O["open"] / max(1.0, O["frame"]),
                          u"A-" + O["sites"][-1]["id"] if O["sites"] else u"none", n_ph or 8))
    top = y                                               # v55 (Aras 31 Oct): the beige palette b only
    low, ss, numbered = p06_page(S, B, x, top, w, k, L, photos, O, p06_pal())
    # v59.1: 1.0 mm under the last row of photo captions (was 0.5 mm: their descenders, "(", "g", "y", reached the edge)
    crop_panel("edge_build", x, low - 1.0 * k, x + w, top + 0.5 * k, cap, crop_scale(ss), [])
    CROP_PANELS[-1]["bk_w"] = BK_AW                       # drawn for the full booklet panel width
    LOG.append(u"Stream edge plan (p.06): ONE strip at 1:{:,}, {:.1f} x {:.1f} mm, palette b; {} open to "
               u"change; {} sites (lettered left -> right); {} photos; map labels as numbers in the key (G3, v58): "
               u"{}.".format(int(round(1000.0 * k / ss)), F.w * ss / k, F.h * ss / k, u_area(O["open"]),
                             len(O["sites"]), n_ph, u", ".join(u"{} {}".format(n, t) for n, t, kr in numbered) or
                             u"none"))
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
