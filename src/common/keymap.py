# ---- Key maps, cut symbol, north arrow (round 4 S2, 1 Nov 2026; G-R4-9, R01, U02 U31 U50 U51 U55 U60; PLAN §4.5) -----
# ONE key-map module: every cut line drawn with the R01 symbol in red (an end bar with an open triangle standing on it
# pointing the way the section looks, a dash-dot line between), in front of a muted base, with ONLY the page's cuts,
# the main street and place names (so the reader knows where it is), never over its legend; ONE north arrow (the
# arrow and "N", no plate, U31 U51). Included by common/basemap.py (its last lines, after map_layers.py); do not
# include it again. The old basemap_cut_items / keymap_items are thin wrappers at the end of this file.
# ROUND 5 (S2, 1 Nov 2026; G-R5-3, D3, D6, A11, U33 U36 U45 U67-U69; PLAN §3 "Key map"): v2. Drawn like the p02 map
# (basemap mode "keymap": green ground, houses by urban fabric, the stream blue, bridges), never the grey blob; the
# frame cut to the map (fitted, fill logged, >= 0.85); turned so the corridor runs along the frame's long side, the
# north arrow showing true north in a free corner; names only through the names table (street_label, keymap_places);
# exported as items for the booklet (km_items: drawing + text labels with anchors + keymap item; G-R5-12, Aras's
# addendum 1 Nov 22:37 point 3). Every page's key map calls km_map (p04, p05, p09, p10 locator, p13-14, p15, p16,
# p18, p19-20, p24; their page sessions S6-S10 switch the callers to km_items); scale_den keeps the round 4 contract.
#   KM_CUT, KM_NAMES, KM_FRAME, KM_CUT_PLAN      the cut symbol, the names switches, the frame line, plan cuts (D6)
#   km_cut_items(cuts, scale_den, frame=None, style=None, text_mm=2.47)      R01 cut symbols as items (survey m)
#   km_map(ids, w_mm=None, h_mm=None, zooms=None, page=None, names=None, legend_box=None, log=None, looks=None,
#          box=None, scale_den=None, extra_names=None, D=None, margin=None, rotate=None, fit=None, pad_mm=None,
#          base_mode="keymap", north=True)                                  a whole key map (survey m + its T)
#   km_draw(km, X, fill_fn, line_fn, text_fn, water_opts=None, page=None, log=None, frame=True)   draws it
#   km_items(km, page=None, item_id=None, priority=5)                       round 5: the key map as booklet items
#   km_texts(km)                                 its texts in key-map mm, for the page's TextPage (.put)
#   north_items(x, y, ang_rad=0.0, size_mm=6.0, colour="2C2219")           the north arrow (page mm, y up)
# Items: the basemap format (common/basemap.py head). Key-map mm: origin at the key map's lower-left, y up.
# ROUND 6 (S1, 4 Nov 2026; G6-5, Q7; PLAN.md §2.5, §2.8): v3, THE only key-map drawer, built from the site board's
# p08 "Where each street is cut" key map (_t3_sec_key, Aras: "almost exceptional ... colourful and all"), so the
# target and the module are one drawing: the strong set (common/hues.py HUE_KEY: fabric, heritage browns, green, blue
# stream, roads kept); street names very subtle (A4A1A3, exactly 4 pt); the page's cuts bold red across with end
# marks and labels, gaps between neighbouring marks (km_cut_marks); the study area drawn WHOLE: the calisma_alan parts
# unioned where they meet (km_study_ring), the frame sized to hold every ring, each ring one closed dashed path, never
# clipped (the p08 outline broke where the frame cut it). The 2 Nov dist fixes (2eb070b: short cuts drawn without end
# names, margin per axis, north arrow along the edges at 5 / 4 / 3.2 mm, fill inside the pad) are in this source now.
#   km_keymap(page, cuts=None, cut_ids=None, zooms=None, w_mm=None, h_mm=None, box=None, scale_den=None,
#             rotate=None, names=("streets", "places"), log=None, **more)   THE call (more: km_map's other options)
#   km_draw_to(km, X, fill_fn, line_fn, text_fn)    draw on a board / page;  km_export_items(km, page, item_id)
#   km_log(page)                                     `keymap <page> module cuts=<ids> study_closed=1`
#   km_study_ring(D=None, rings=None)                the study outline: closed rings, overlapping parts unioned
#   km_cut_marks(cuts, den, frame=None, gap_mm=1.5, T=None, box_mm=None, page=None, log=None, per_cut=False)
#   km_street_names(D, T, obstacles, vb=..., ...)    the subtle street / place names, placed clear of obstacles
# Also includes the round 6 shared tables and marks (one include for every script that has basemap.py):
#@include hues.py
#@include annot.py
#@include cch_points.py
import math as _km_m

# R01 in red (G-R4-9): line 0.5 mm dash-dot; end bar 2.4 mm along the line at each end, the open triangle standing on
# it (base = the bar, height tri_h, apex the way the section looks), the end name beyond the bar. Sizes: drawing rules
# of PLAN §4.5 (the triangle's base is the bar so it never overhangs it).
KM_CUT = dict(colour="C0392B", lw=0.5, dash=(3.0, 0.8, 0.6, 0.8), end_bar=2.4, bar_lw=0.6, tri_h=2.1, tri_lw=0.35,
              text_mm=2.47, gap_mm=0.8)
KM_NAMES = dict(streets=("main",), n_streets=4, places=True, n_places=6, size_mm=4.0 * 0.352778, colour="A4A1A3",
                bold=False, pad_mm=0.6)     # round 6 (G6-5): very subtle, exactly the 4 pt floor ("squint a little")
KM_MIN_L = 1.0           # mm: round 6 (from the site board's T3_KEY_MIN_L): a cut's line between its end bars at least
#                          this long on the key map (a street is 10-20 m wide, under 2 mm at a key map's scale)
KM_GAP = 1.5             # mm: round 6 (G6-5 "gaps"): neighbouring cut marks keep at least this apart
KM_SHRINK = (1.0, 0.75, 0.55)      # round 6: symbol sizes tried when two marks would touch
KM_ZOOM = dict(colour="C0392B", lw=0.35)       # zoom / window frames on a key map: the cut red, solid
KM_FRAME = dict(colour="4A3F35", lw=0.25)      # round 5 (S2, D3): the key map's frame line (site board INK), hairline
# round 5 (S2, D6 a, U30): cut lines ON PLANS (not key maps): thin and muted, 0.25 pt 8E8F8A dashed (PLAN §3); pass
# as km_cut_items(..., style=KM_CUT_PLAN); key maps keep the red R01 KM_CUT. Dash, bar and triangle sizes: design values
KM_CUT_PLAN = dict(colour="8E8F8A", lw=0.0882, dash=(1.6, 0.8), end_bar=1.6, bar_lw=0.0882, tri_h=1.2, tri_lw=0.0882,
                   text_mm=1.59, gap_mm=0.6)
KM_LOG = []


def km_cut_items(cuts, scale_den, frame=None, style=None, text_mm=None):
    """R01 cut symbols (G-R4-9) as items in survey m. cuts = [(end1, end2, (name1, name2)[, look])] (as
    basemap_cut_ids gives them: end1 = the section's left end, look +1 = the viewer stands so end1 is on the left,
    -1 the other way); scale_den: the key map's 1:scale_den (mm sizes -> m); frame: a convex polygon the symbols stay
    inside (the line is cut to it and pulled in so bars and names fit). Per cut: the dash-dot line end to end, at each
    end the bar and the open triangle pointing the look direction, the end's name beyond the bar (bold)."""
    st = dict(KM_CUT)
    st.update(style or {})
    tm = text_mm or st["text_mm"]
    m = scale_den / 1000.0                               # survey m per key-map mm
    col = st["colour"]
    out = []
    for c in cuts:
        a, b, names = c[0], c[1], c[2]
        look = c[3] if len(c) > 3 and isinstance(c[3], (int, float)) else 1   # v32 (L1): a look given as text = +1
        L0 = _km_m.hypot(b[0] - a[0], b[1] - a[1])
        if L0 < 1e-6:
            continue
        ux, uy = (b[0] - a[0]) / L0, (b[1] - a[1]) / L0
        if frame:
            ab = _bm_clip_convex(a, b, frame)
            if ab is None:
                continue
            a, b = ab
            pull = (st["gap_mm"] + tm * 0.6 * max(len(names[0]), len(names[1]), 1)) * m
            L = _km_m.hypot(b[0] - a[0], b[1] - a[1])
            if L <= 2.0 * pull + 2.0 * st["end_bar"] * m:   # 2 Nov fix: too short for its end names: no longer
                n0 = names[0]                                 # dropped; drawn without them, its first name beside
                names = (u"", u"")                            # the middle (km_map's id label goes on the other side)
                pull = st["gap_mm"] * m
                mx_, my_ = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
                if L <= 2.0 * pull + 2.0 * st["end_bar"] * m:   # shorter than the symbol: its least length, centred
                    hl = pull + st["end_bar"] * m + 0.5 * m
                    a, b = (mx_ - ux * hl, my_ - uy * hl), (mx_ + ux * hl, my_ + uy * hl)
                if n0:
                    off_ = tm * 1.2 * m
                    out.append(("text", n0, (mx_ + uy * off_, my_ - ux * off_), tm, col, True, "MC"))
            a = (a[0] + ux * pull, a[1] + uy * pull)
            b = (b[0] - ux * pull, b[1] - uy * pull)
        fx, fy = -uy * look, ux * look                   # the way the section looks
        out.append(("line", [a, b], col, st["lw"], list(st["dash"]), 1.0))
        bar, th = st["end_bar"] * m, st["tri_h"] * m
        for p, nm, sgn in ((a, names[0], -1.0), (b, names[1], 1.0)):
            q = (p[0] - ux * sgn * bar, p[1] - uy * sgn * bar)          # the bar runs from the end inward
            out.append(("line", [p, q], col, st["bar_lw"], None, 1.0))
            mid = ((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0)
            tri = [p, q, (mid[0] + fx * th, mid[1] + fy * th), p]
            out.append(("line", tri, col, st["tri_lw"], None, 1.0))      # open triangle standing on the bar
            off = (st["gap_mm"] + tm * 0.3 * max(1, len(nm))) * m     # beyond the end, clear of the bar
            t = (p[0] + ux * sgn * off, p[1] + uy * sgn * off)
            if nm:
                out.append(("text", nm, t, tm, col, True, "MC"))
    return out


def _km_box_hit(b, boxes, pad=0.0):
    for o in boxes:
        if not (b[2] + pad <= o[0] or b[0] - pad >= o[2] or b[3] + pad <= o[1] or b[1] - pad >= o[3]):
            return True
    return False


def _km_seg_hit(b, segs, pad):
    x0, y0, x1, y1 = b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad
    for p, q in segs:
        L = _km_m.hypot(q[0] - p[0], q[1] - p[1])
        n = max(1, int(L / 0.4))
        for i in range(n + 1):
            x, y = p[0] + (q[0] - p[0]) * i / n, p[1] + (q[1] - p[1]) * i / n
            if x0 <= x <= x1 and y0 <= y <= y1:
                return True
    return False


def _km_axis_deg(P):
    """round 5 (S2): the direction (degrees, counter-clockwise from east) of the long axis of points P (principal
    axis of their spread); 0.0 when P has fewer than 3 points"""
    if len(P) < 3:
        return 0.0
    mx, my = sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P)
    sxx = sum((p[0] - mx) ** 2 for p in P)
    syy = sum((p[1] - my) ** 2 for p in P)
    sxy = sum((p[0] - mx) * (p[1] - my) for p in P)
    return _km_m.degrees(0.5 * _km_m.atan2(2.0 * sxy, sxx - syy))


def km_map(ids, w_mm=None, h_mm=None, zooms=None, page=None, names=None, legend_box=None, log=None, looks=None,
           box=None, scale_den=None, extra_names=None, D=None, margin=None, rotate=None, fit=None, pad_mm=None,
           base_mode="keymap", north=True, cuts=None, study=None, strong=True):
    """THE key map (round 5 S2 v2: G-R5-3, D3, D6, A11; round 4 G-R4-9). Key-map mm: origin at the frame's lower-left,
    y up. ids: this page's cut ids (cut registry, levels.py) and zoom / window ids (zooms {id: polygon survey m}, else
    level_window(id)); none + page = every cut the registry draws on that page.
    Size and frame (D3 "a frame sized to the map"): with scale_den None (the usual call) the map is FITTED: w_mm /
    h_mm are the most the page offers (either may be None; both None = 80 mm wide), the scale fills that space and the
    frame is cut to the map plus pad_mm (default 1.0) and a margin (default 2 % of the content), so the map fills its
    frame; fit=False keeps the caller's w x h (map centred, round 4). scale_den given: the round 4 contract (fixed
    scale, the caller's frame or box; no turn).
    Turn (U68): rotate=None turns a fitted map so the corridor (the study area's long axis) runs along the frame's
    long side (portrait space: upright), north never pointing down; a number = that turn in degrees
    (counter-clockwise); False = north up. The north arrow shows true north (north=True: arrow only, in the freest
    corner).
    Base (U69 "just draw it like page 2"): basemap mode base_mode ("keymap" = the p02 look: green ground, houses by
    urban fabric, the stream blue, bridges), cut to the frame. Content: the study line, ONLY these cuts (R01 red,
    look direction), zoom frames, names: main streets (OpenStreetMap names by the names table's spelling,
    street_label) and the names table's key-map places (keymap_places: "at" + "km"; never a raw survey name), then
    extra_names; each placed clear of the cuts, their labels, the north arrow, legend_box and each other, else left
    out and logged. Labels are hints: km_items exports them with their anchors for the booklet to place (G-R5-12).
    Logs `keymap <page> fill=<x> rotation=<deg> cuts=<ids>` (fill = the content's box / the frame; WARNING below
    0.85 on a fitted map). Returns dict(base, study, cuts, names, items (survey m, in order), box, scale_den, T, Tinv,
    drawn, missing, label_boxes, w_mm, h_mm, study_rings, rotation_deg, north_deg, fill, frame (survey ring),
    frame_items, north (key-map mm items), labels [dict(string, kind, anchor, box, size_mm, colour, bold)], fitted,
    looks, zoom_ids, page).
    Round 6 (S1, G6-5): cuts = explicit cuts [(end1, end2, (name1, name2), look[, id])] survey m (street cuts R1-R4,
    anything not in the registry), drawn with the registry ids; study = the study rings to draw (default
    km_study_ring(D): overlapping parts unioned, each ring whole); the content always holds every study ring, so the
    frame never cuts it (a caller's box is widened to it); strong=True = the key-map colours of hues.HUE_KEY (heritage
    in the fabric in browns); cuts by km_cut_marks (gaps between neighbours); names by km_street_names."""
    D = D if D is not None else basemap_load()
    log = log if log is not None else KM_LOG
    xcuts = cuts
    nm_st = dict(KM_NAMES)
    nm_st.update(names or {})
    pg = u"%s" % (page or u"")
    if not ids and page is not None and callable(globals().get("level_registry_all")):
        ids = [e["id"] for e in level_registry_all(str(page))]
    cuts, wins, drawn, missing, seen = [], [], [], [], set()
    win_fn = globals().get("level_window")
    for cid in ids or ():
        if zooms and cid in zooms:
            wins.append((cid, [tuple(p) for p in zooms[cid]]))
            drawn.append(cid)
            continue
        try:
            c = basemap_cut_ids([cid], looks)[0]
            ek = (round(c[0][0], 1), round(c[0][1], 1), round(c[1][0], 1), round(c[1][1], 1))
            if ek not in seen:                           # the crossings of one cut share one line
                seen.add(ek)
                cuts.append((cid, c))
            drawn.append(cid)
            continue
        except Exception:
            pass
        try:
            w = win_fn(cid) if callable(win_fn) else None
            if w:
                wins.append((cid, [tuple(p) for p in w]))
                drawn.append(cid)
                continue
        except Exception:
            pass
        missing.append(cid)
        log.append(u"WARNING %s keymap '%s' is neither a cut of the registry nor a zoom passed in: not drawn."
                   % (pg, cid))
    for c in xcuts or ():                                # round 6: explicit cuts (street cuts R1-R4 ...)
        cid = c[4] if len(c) > 4 and c[4] else c[2][0]
        cuts.append((cid, (tuple(c[0]), tuple(c[1]), tuple(c[2]), c[3] if len(c) > 3 else 1)))
        drawn.append(cid)
    study = km_study_ring(D) if study is None else [[tuple(p) for p in R] for R in study]
    auto = not scale_den
    fit = auto if fit is None else (bool(fit) and auto)
    if margin is None:
        margin = 0.02 if fit else 0.06
    pad = 1.0 if pad_mm is None else float(pad_mm)
    if box is None:
        cont = [p for R in study for p in R] + [p for _, c in cuts for p in c[:2]] + [p for _, w in wins for p in w]
        if not cont:
            cont = list(basemap_extent(D) or [])
        if not cont:
            raise ValueError(u"key map %s: nothing to frame (no basemap data, no cuts)" % pg)
    else:
        bx_ = _bm_bb([(box[0], box[1]), (box[2], box[3])] + [p for R in study for p in R])   # round 6: ring whole
        if tuple(bx_) != (box[0], box[1], box[2], box[3]):
            log.append(u"keymap %s: box widened to hold the whole study outline" % pg)
        cont = [(bx_[0], bx_[1]), (bx_[2], bx_[1]), (bx_[2], bx_[3]), (bx_[0], bx_[3])]
    # the turn: the corridor along the frame's long side (U68)
    if rotate is None:
        if auto:
            bx_ = _bm_bb(cont)
            ax_pts = [p for R in study for p in R if bx_[0] <= p[0] <= bx_[2] and bx_[1] <= p[1] <= bx_[3]]
            th = _km_axis_deg(ax_pts if len(ax_pts) >= 3 else cont)
            portrait = bool(w_mm and h_mm and h_mm > w_mm)
            phi = (90.0 - th) if portrait else -th
        else:
            phi = 0.0
    else:
        phi = float(rotate or 0.0)
    if _km_m.cos(_km_m.radians(phi)) < -1e-9:            # north never points down the page
        phi += 180.0
    phi = (phi + 180.0) % 360.0 - 180.0
    cph, sph = _km_m.cos(_km_m.radians(phi)), _km_m.sin(_km_m.radians(phi))
    bx0 = _bm_bb(cont)
    c0 = ((bx0[0] + bx0[2]) / 2.0, (bx0[1] + bx0[3]) / 2.0)

    def rot(p):
        dx, dy = p[0] - c0[0], p[1] - c0[1]
        return (dx * cph - dy * sph, dx * sph + dy * cph)

    def unrot(q):
        return (q[0] * cph + q[1] * sph + c0[0], -q[0] * sph + q[1] * cph + c0[1])
    rc = [rot(p) for p in cont]
    rx0, ry0, rx1, ry1 = _bm_bb(rc)
    cw, ch = max(rx1 - rx0, 1.0), max(ry1 - ry0, 1.0)  # the content, m
    d = margin * max(cw, ch)
    if fit:     # 2 Nov fix (fill warnings): margin per axis, so a long strip is not padded by its length across
        bw, bh = cw * (1.0 + 2.0 * margin), ch * (1.0 + 2.0 * margin)
    else:
        bw, bh = cw + 2.0 * d, ch + 2.0 * d
    if fit:
        if not w_mm and not h_mm:
            w_mm = 80.0
        dens = []
        if w_mm:
            dens.append(bw * 1000.0 / max(1.0, w_mm - 2.0 * pad))
        if h_mm:
            dens.append(bh * 1000.0 / max(1.0, h_mm - 2.0 * pad))
        den = max(dens)
        w_mm, h_mm = bw * 1000.0 / den + 2.0 * pad, bh * 1000.0 / den + 2.0 * pad
    elif scale_den and (w_mm is None or h_mm is None):   # a fixed scale: the key map is the box at that scale
        den = float(scale_den)
        w_mm, h_mm = bw * 1000.0 / den, bh * 1000.0 / den
    else:
        den = float(scale_den) if scale_den else max(bw * 1000.0 / w_mm, bh * 1000.0 / h_mm)
    s = 1000.0 / den
    rcx, rcy = (rx0 + rx1) / 2.0, (ry0 + ry1) / 2.0

    def T(p):
        r = rot(p)
        return ((r[0] - rcx) * s + w_mm / 2.0, (r[1] - rcy) * s + h_mm / 2.0)

    def Tinv(q):
        return unrot(((q[0] - w_mm / 2.0) / s + rcx, (q[1] - h_mm / 2.0) / s + rcy))
    frame = [Tinv((0.0, 0.0)), Tinv((w_mm, 0.0)), Tinv((w_mm, h_mm)), Tinv((0.0, h_mm))]
    vb = _bm_bb(frame)
    if base_mode == "muted":
        base = ml_base(vb, den, D=D, crop=False) if D else []
    else:
        base = basemap_items(base_mode, box=vb, D=D, scale_den=den) if D else []
    base = ml_crop(base, frame) if base else []
    if strong and base:
        base = _km_strong(base)
    if D and D.get("format") != BASEMAP_FORMAT:
        log.append(u"FLAG keymap %s: basemap format %s has no urban fabric per house: one house tone until the site "
                   u"board writes format %d" % (pg, D.get("format"), BASEMAP_FORMAT))
    st_items = ml_study_items(study)
    cut_items = []
    marks = km_cut_marks([c for _, c in cuts], den, frame=frame, T=T, box_mm=(w_mm, h_mm), page=pg, log=log,
                         per_cut=True)
    for (cid, c), its in zip(cuts, marks):
        nm_fn = globals().get("level_name")
        try:
            name = nm_fn(cid) if callable(nm_fn) else cid
        except Exception:
            name = cid
        name = u"%s" % name
        name = name.split("-")[0]                        # a crossing row (S5-2) is labelled by its cut (S5)
        if not its:
            log.append(u"WARNING %s keymap cut %s too short inside the frame: not drawn" % (pg, cid))
        elif name not in c[2][0] and name not in c[2][1]:   # end names that do not say the id: the id too
            a, b = c[0], c[1]
            L0 = _km_m.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
            nx, ny = -(b[1] - a[1]) / L0, (b[0] - a[0]) / L0
            q = ((a[0] + b[0]) / 2.0 + nx * KM_CUT["text_mm"] * 1.2 / s, (a[1] + b[1]) / 2.0 + ny * KM_CUT["text_mm"]
                 * 1.2 / s)
            its.append(("text", name, q, KM_CUT["text_mm"], KM_CUT["colour"], True, "MC"))
        cut_items += its
    for cid, w in wins:
        cut_items.append(("line", list(w) + [w[0]], KM_ZOOM["colour"], KM_ZOOM["lw"], None, 1.0))
        x0, y0, x1, y1 = _bm_bb([T(p) for p in w])
        cut_items.append(("text", cid, Tinv((x0 + KM_CUT["text_mm"] * 0.9, y1 + KM_CUT["text_mm"] * 0.8)),
                          KM_CUT["text_mm"], KM_CUT["colour"], True, "MC"))
    fmw = globals().get("fm_width")
    pt_of = lambda mm: mm / 0.352778
    segs, boxes, label_boxes, labels = [], [], [], []
    for it in cut_items + st_items:
        if it[0] == "line":
            P = [T(p) for p in it[1]]
            segs += list(zip(P, P[1:]))
    for it in cut_items:
        if it[0] == "text":
            x, y = T(it[2])
            w = fmw(it[1], pt_of(it[3]), bold=it[5]) if callable(fmw) else 0.6 * it[3] * len(it[1])
            b = (x - w / 2.0, y - it[3] / 2.0, x + w / 2.0, y + it[3] / 2.0)
            boxes.append(b)
            label_boxes.append((it[1], b))
            labels.append(dict(string=it[1], kind="cut", anchor=(x, y), box=b, size_mm=it[3], colour=it[4],
                               bold=it[5]))
    # the north arrow: arrow only (G-R4-9), in the first free corner (top right, top left, bottom right, bottom left)
    north_its, nsz = [], 5.0
    if north:
        best = None
        # 2 Nov fix (no free corner): the corners, then along the edges (2 mm steps), at 5 / 4 / 3.2 mm; first clear
        # of every line, then clear of the cuts and labels only (the study line may pass under the arrow)
        cut_segs = []
        for it in cut_items:
            if it[0] == "line":
                P = [T(p) for p in it[1]]
                cut_segs += list(zip(P, P[1:]))
        for sg_ in (segs, cut_segs):
            for nsz_ in (5.0, 4.0, 3.2):
                h_ = 0.9 * nsz_
                xr, xl, yt, yb = w_mm - pad - h_, pad + h_, h_mm - pad - h_, pad + h_
                if xr < xl or yt < yb:
                    continue
                nx_, ny_ = int((xr - xl) / 2.0), int((yt - yb) / 2.0)
                cands = [(xr, yt), (xl, yt), (xr, yb), (xl, yb)]
                cands += [(xr - 2.0 * k, yt) for k in range(1, nx_ + 1)] + [(xr - 2.0 * k, yb) for k in range(1, nx_ + 1)]
                cands += [(xr, yt - 2.0 * k) for k in range(1, ny_ + 1)] + [(xl, yt - 2.0 * k) for k in range(1, ny_ + 1)]
                for cxn, cyn in cands:
                    nb = (cxn - h_, cyn - h_, cxn + h_, cyn + h_)
                    if not _km_seg_hit(nb, sg_, 0.3) and not _km_box_hit(nb, boxes, 0.3):
                        best = (cxn, cyn, nb)
                        break
                if best is not None:
                    if nsz_ != nsz:
                        log.append(u"keymap %s north arrow at %.1f mm (no room at %.1f mm)" % (pg, nsz_, nsz))
                    nsz = nsz_
                    break
            if best is not None:
                break
        if best is None:
            cxn, cyn = w_mm - pad - 0.9 * nsz, h_mm - pad - 0.9 * nsz
            best = (cxn, cyn, (cxn - 0.9 * nsz, cyn - 0.9 * nsz, cxn + 0.9 * nsz, cyn + 0.9 * nsz))
            log.append(u"WARNING %s keymap north arrow: no free corner, set top right over the map" % pg)
        cxn, cyn, nb = best
        a = _km_m.radians(phi)
        foot = (cxn + _km_m.sin(a) * 0.5 * nsz, cyn - _km_m.cos(a) * 0.5 * nsz)    # the arrow centred on (cxn, cyn)
        north_its = north_items(foot[0], foot[1], ang_rad=a, size_mm=nsz * 0.75)
        boxes.append(nb)
    if legend_box:
        boxes.append(tuple(legend_box))
    nr = km_street_names(D, T, boxes, vb=vb, frame_mm=(w_mm, h_mm), segs=segs, Tinv=Tinv, names=nm_st,
                         extra_names=extra_names, page=pg, log=log)
    name_items = nr["items"]
    labels += nr["labels"]
    label_boxes += nr["label_boxes"]
    fill = (cw * s) * (ch * s) / max(1e-9, (w_mm - 2.0 * pad) * (h_mm - 2.0 * pad) if fit else w_mm * h_mm)
    fill = min(1.0, fill)
    rot_out = round(phi, 1)
    log.append(u"keymap %s fill=%.2f rotation=%.1f cuts=%s" % (pg, fill, rot_out,
                                                               u",".join(cid for cid, _ in cuts) or u"-"))
    if fit and fill < 0.85:
        log.append(u"WARNING %s keymap fill %.2f below 0.85 (frame %.0f x %.0f mm)" % (pg, fill, w_mm, h_mm))
    if log is not KM_LOG:
        KM_LOG.append(log[-1])
    frame_mm = [(0.0, 0.0), (w_mm, 0.0), (w_mm, h_mm), (0.0, h_mm)]
    frame_items = [("fill", [frame_mm], bm_key_col("paper"), 1.0, True),
                   ("line", frame_mm + [frame_mm[0]], KM_FRAME["colour"], KM_FRAME["lw"], None, 1.0)]
    return dict(base=base, study=st_items, cuts=cut_items, names=name_items,
                items=list(base) + st_items + cut_items + name_items, box=(vb[0], vb[1], vb[2], vb[3]), scale_den=den,
                T=T, Tinv=Tinv, drawn=drawn, missing=missing, label_boxes=label_boxes, w_mm=w_mm, h_mm=h_mm,
                study_rings=study, rotation_deg=rot_out, north_deg=rot_out, fill=fill, frame=frame,
                frame_items=frame_items, north=north_its, labels=labels, fitted=fit, looks=dict(looks or {}),
                zoom_ids=[cid for cid, _ in wins], cut_ids=[cid for cid, _ in cuts], page=page)


def km_street_names(D, T, obstacles, vb=None, frame_mm=None, segs=(), Tinv=None, names=None, extra_names=None,
                    page=None, log=None):
    """round 6 (S1, G6-5; moved out of km_map unchanged in its rule): the key map's names, very subtle (KM_NAMES:
    A4A1A3, 4 pt): the main streets (OpenStreetMap names by the names table's spelling, street_label), the names
    table's key-map places (keymap_places), then extra_names [(name, xy)]; each placed at its point or the nearest
    of six spots clear of obstacles (key-map mm boxes; the placed names are added to it), segs (key-map mm
    segments) and the frame (frame_mm = (w, h)); a name with no free place is left out and logged. T / Tinv: survey
    m <-> key-map mm; vb: the survey box the names are taken from. Returns dict(items (survey m text items), labels
    (dicts as km_map's), label_boxes)."""
    log = log if log is not None else KM_LOG
    nm_st = dict(KM_NAMES)
    nm_st.update(names or {})
    pg = page or u""
    w_mm, h_mm = frame_mm
    boxes = obstacles
    fmw = globals().get("fm_width")
    pt_of = lambda mm: mm / 0.352778
    label_boxes, labels = [], []
    cand = []
    stl = globals().get("street_label")
    if nm_st.get("streets"):
        for n, p, _a, _cl, _ln in basemap_street_names(vb, D, classes=tuple(nm_st["streets"]))[:4 * nm_st["n_streets"]]:
            cand.append((stl(n) if callable(stl) else n, p, "street"))
    if nm_st.get("places"):
        kp = globals().get("keymap_places")
        if callable(kp):
            for n, p, _k in kp(vb):
                cand.append((n, p, "place"))
        else:
            log.append(u"FLAG keymap %s: common/names.py not included: no place names (never a raw survey name)" % pg)
    for n, p in extra_names or ():
        cand.append((n, tuple(p), "extra"))
    if cand and not callable(fmw):
        raise RuntimeError(u"km_map needs common/font_metrics.py (round 4 S1: fm_width) included before it is "
                           u"called: text widths come from the real font only")
    sz = nm_st["size_mm"]
    pad_n = nm_st["pad_mm"]
    name_items, placed, seen_n = [], {"street": 0, "place": 0, "extra": 0}, set()
    lim = {"street": nm_st["n_streets"], "place": nm_st["n_places"], "extra": 10 ** 6}
    for n, p, kind in cand:
        if placed[kind] >= lim[kind] or n in seen_n:
            continue
        x, y = T(p)
        if not (0.0 <= x <= w_mm and 0.0 <= y <= h_mm):
            continue
        w = fmw(n, pt_of(sz), bold=nm_st["bold"])
        ok = None
        for dx, dy in ((0.0, 0.0), (0.0, sz * 1.1), (0.0, -sz * 1.1), (w / 2.0 + 1.0, 0.0), (-w / 2.0 - 1.0, 0.0),
                       (0.0, sz * 2.2), (0.0, -sz * 2.2)):
            b = (x + dx - w / 2.0, y + dy - sz / 2.0, x + dx + w / 2.0, y + dy + sz / 2.0)
            if b[0] < pad_n or b[1] < pad_n or b[2] > w_mm - pad_n or b[3] > h_mm - pad_n:
                continue
            if _km_box_hit(b, boxes, pad_n) or _km_seg_hit(b, segs, pad_n):
                continue
            ok = b
            break
        if ok is None:                                    # 4 Nov (Aras 19:17 "not drawing ... is not a solution"):
            ok = (x - w / 2.0, y - sz / 2.0, x + w / 2.0, y + sz / 2.0)   # set on its point, handed to the booklet,
            ok = (max(pad_n, min(ok[0], w_mm - pad_n - w)), max(pad_n, min(ok[1], h_mm - pad_n - sz)))   # which
            ok = (ok[0], ok[1], ok[0] + w, ok[1] + sz)                     # moves it off whatever it hits
            log.append(u"keymap %s: name '%s' set on its point (no free place here; the booklet places it)" % (pg, n))
        seen_n.add(n)
        boxes.append(ok)
        label_boxes.append((n, ok))
        placed[kind] += 1
        name_items.append(("text", n, Tinv(((ok[0] + ok[2]) / 2.0, (ok[1] + ok[3]) / 2.0)), sz, nm_st["colour"],
                           nm_st["bold"], "MC"))
        labels.append(dict(string=n, kind=kind, anchor=(x, y), box=ok, size_mm=sz, colour=nm_st["colour"],
                           bold=nm_st["bold"]))
    return dict(items=name_items, labels=labels, label_boxes=label_boxes)


def km_draw(km, X, fill_fn, line_fn, text_fn, water_opts=None, page=None, log=None, frame=True):
    """draws a km_map (PLAN §3 order: paper, base, WATER, structures, the study line, the red cuts, names, then the
    frame line and the north arrow): X(q) key-map mm -> page point (e.g. lambda q: (x0 + q[0], y0 + q[1]), or a
    y-down flip). frame=False leaves out the paper, the frame line and the arrow (a caller that draws its own).
    text_fn=None draws no text (the booklet places the labels from km_items). Returns map_draw's dict."""
    T = km["T"]
    if frame:
        basemap_draw(km["frame_items"][:1], X, fill_fn, line_fn, None)
    r = map_draw(page or u"key", lambda p: X(T(p)), fill_fn, line_fn, text_fn, km["base"],
                 {"proj_marks": [it for it in km["cuts"] if it[0] != "text"],
                  "proj_labels": [it for it in km["cuts"] if it[0] == "text"] + km["names"]},
                 study=km.get("study_rings"), clip=False, log=log, water_opts=water_opts)
    if frame:
        basemap_draw(km["frame_items"][1:] + km["north"], X, fill_fn, line_fn, text_fn)
    return r


def km_items(km, page=None, item_id=None, priority=5):
    """round 5 (S2, G-R5-12; PLAN §4 item schema v1, Aras's addendum 1 Nov 22:37 point 3): the key map as items for
    the booklet: one "drawing" (layers of shapes in key-map mm, y up, origin lower-left; texts left out), one "text"
    item per label (names and cut labels, role "label", with its anchor in the drawing and the module's placement as
    hint_box), one "keymap" item (cut ids, looks, zooms, names, fill, rotation). Shapes: {"type": "poly", "rings",
    "fill", "opacity", "nonzero"} and {"type": "line", "pts", "stroke", "width_pt", "dash_pt", "opacity"}."""
    pg = page if page is not None else km.get("page")
    did = item_id or (u"keymap_%s" % (pg or u"key"))
    layers, cur = [], {"name": None}

    def layer(name):
        cur["name"] = name
        layers.append(dict(z=len(layers), name=name, shapes=[]))

    def fill_fn(rings, col, alpha, nonzero):
        if cur["name"] is None:
            layer("base")
        layers[-1]["shapes"].append(dict(type="poly", rings=[[[round(p[0], 3), round(p[1], 3)] for p in R]
                                                             for R in rings], fill=col, opacity=alpha,
                                         nonzero=bool(nonzero)))

    def line_fn(pts, col, w_mm, dash_mm, alpha):
        if cur["name"] is None:
            layer("base")
        layers[-1]["shapes"].append(dict(type="line", pts=[[round(p[0], 3), round(p[1], 3)] for p in pts],
                                         stroke=col, width_pt=round(w_mm / 0.352778, 3),
                                         dash_pt=[round(d_ / 0.352778, 3) for d_ in dash_mm] if dash_mm else None,
                                         opacity=alpha))
    T = km["T"]
    layer("paper")
    basemap_draw(km["frame_items"][:1], lambda q: q, fill_fn, line_fn, None)
    map_draw(u"%s key map" % (pg or u""), T, fill_fn, line_fn, None, km["base"],
             {"proj_marks": [it for it in km["cuts"] if it[0] != "text"]}, study=km.get("study_rings"),
             clip=False, order_fn=layer)
    layer("frame")
    basemap_draw(km["frame_items"][1:] + [it for it in km["north"] if it[0] != "text"], lambda q: q, fill_fn,
                 line_fn, None)
    layers = [L_ for L_ in layers if L_["shapes"]]
    for i, L_ in enumerate(layers):
        L_["z"] = i
    w, h = km["w_mm"], km["h_mm"]
    out = [dict(id=did, page=pg, kind="drawing", role="keymap", priority=priority, group=did, units="mm",
                axes=u"key-map mm, origin lower-left, y up", size_mm=[round(w, 2), round(h, 2)], extent=[0.0, 0.0,
                                                                                                    round(w, 2),
                                                                                                    round(h, 2)],
                scale_pref=None, scale_den=round(km["scale_den"]), scale_bar=False, north_deg=km["north_deg"],
                layers=layers, keep_areas=[[0.0, 0.0, round(w, 2), round(h, 2)]], anchors={})]
    texts = [dict(string=t[1], kind="north", anchor=t[2], box=None, size_mm=t[3], colour=t[4], bold=t[5])
             for t in km["north"] if t[0] == "text"]
    for i, lb in enumerate(km["labels"] + texts):
        out.append(dict(id=u"%s.t%d" % (did, i), page=pg, kind="text", role="label", priority=priority, group=did,
                        string=lb["string"], label_kind=lb["kind"],
                        anchor=dict(drawing=did, point=[round(lb["anchor"][0], 2), round(lb["anchor"][1], 2)]),
                        hint_box=[round(v, 2) for v in lb["box"]] if lb["box"] else None,
                        size_pt=round(lb["size_mm"] / 0.352778, 2), min_pt=4.0, bold=bool(lb["bold"]),
                        colour=lb["colour"], short_forms=[], side_list_ok=False, justify=False))
    out.append(dict(id=u"%s.km" % did, page=pg, kind="keymap", role="keymap", priority=priority, group=did,
                    drawing=did, cuts=[dict(id=c, look=km["looks"].get(c, 1)) for c in km["cut_ids"]],
                    zooms=list(km["zoom_ids"]), names=[lb["string"] for lb in km["labels"] if lb["kind"] != "cut"],
                    fill=round(km["fill"], 3), rotation_deg=km["rotation_deg"], missing=list(km["missing"])))
    return out


def km_texts(km):
    """the key map's texts in key-map mm for the page's TextPage: [(text, (x, y) centre, size_mm, bold, box)]"""
    out = []
    for it in km["cuts"] + km["names"]:
        if it[0] == "text":
            x, y = km["T"](it[2])
            box = next((b for t, b in km["label_boxes"] if t == it[1]), None)
            out.append((it[1], (x, y), it[3], it[5], box))
    return out


def north_items(x, y, ang_rad=0.0, size_mm=6.0, colour="2C2219"):
    """THE north arrow (G-R4-9, U31 U51): only the arrow and "N", no plate or box behind it, as items in page mm
    (y up): a slim filled arrowhead on a short shaft, size_mm tall, "N" above its tip; (x, y) = the shaft's foot;
    ang_rad = north's turn from page-up, counter-clockwise. Draw with basemap_draw(items, lambda p: p, ...)."""
    c, s_ = _km_m.cos(ang_rad), _km_m.sin(ang_rad)

    def R(px, py):
        return (x + px * c - py * s_, y + px * s_ + py * c)
    h = size_mm
    hw = 0.22 * h
    head = [R(0.0, h), R(-hw, 0.55 * h), R(0.0, 0.66 * h), R(hw, 0.55 * h)]
    tm = max(2.12, 0.42 * h)                             # "N" at least 6 pt
    return [("line", [R(0.0, 0.0), R(0.0, 0.62 * h)], colour, max(0.18, 0.04 * h), None, 1.0),
            ("fill", [head], colour, 1.0, True),
            ("text", u"N", R(0.0, h + 0.75 * tm), tm, colour, True, "MC")]


# ---- round 6 (S1, 4 Nov 2026; G6-5): v3 ------------------------------------------------------------------------------
KM_STUDY_LOG = {}        # page -> (n rings, closed: 1/0) of its last key map


def km_study_ring(D=None, rings=None):
    """the study area (calisma_alan, "two closed parts worked as one") as the key map draws it: closed rings, survey
    m, the parts that overlap or cross unioned into one outline (study_clip._sc_gh union, perturbed and retried like
    _sc_poly_and when a vertex falls on an edge), holes of the union left out, parts that never meet kept as their
    own closed rings (the 25 Oct recorded copy's two parts are ~249 m apart: two rings; nothing is drawn between them
    that the survey does not hold). rings default = basemap_study(D)."""
    R0 = [[tuple(p[:2]) for p in _sc_open(R)] for R in (rings if rings is not None else basemap_study(D)) or ()
          if len(R) >= 3]
    out = []
    for R in R0:
        cur = R
        rest = []
        for Q in out:
            got = None
            S_ = list(cur)
            for k in range(6):
                got = _sc_gh(S_, Q, union=True)
                if got is not None:
                    break
                d = 1e-6 * (k + 1)
                S_ = [(p[0] + d * ((i * 7919) % 13 - 6) / 6.0, p[1] + d * ((i * 104729) % 11 - 5) / 5.0)
                      for i, p in enumerate(S_)]
            if got is None:
                rest.append(Q)                           # no clean union: both stay
                continue
            if len(got) == 2 and [tuple(p) for p in got[1]] == [tuple(p) for p in Q] and \
                    [tuple(p) for p in got[0]] == [tuple(p) for p in S_]:
                rest.append(Q)                           # apart: both stay, each closed
                continue
            cur = max(got, key=lambda G: abs(_sc_area(G)))      # the outer ring; holes left out
        out = rest + [cur]
    return out


def _km_strong(items):
    """round 6 (Q7, Q5): the base in the key-map strong set: houses of fabric monument / sacred (heritage in the
    fabric, no sourced per-building status = HER r3, plan_findings H3 last row) take HUE_KEY her3 (annexes paler by
    BM_KEY annex, the p02 rule); every other tone is already the strong set's (BM_KEY: fabric mixed 0.40, greens
    mixed 0.35, stream, roads)"""
    her3 = HUE_KEY["her3"]
    remap = {}
    for fab in ("monument", "sacred"):
        remap[bm_fabric_col({"fabric": fab})] = her3
        remap[bm_fabric_col({"fabric": fab, "annex": True})] = _bm_mix(her3, BM_KEY["paper"], BM_KEY["annex"])
    out = []
    for it in items:
        if it[0] in ("fill", "line") and isinstance(it[2], str) and it[2].upper() in remap:
            t = tuple(it[:2]) + (remap[it[2].upper()],) + tuple(it[3:])
            it = _bm_tag(t, it.layer) if hasattr(it, "layer") else t
        out.append(it)
    return out


def _km_seg_dist(p, q, r, t):
    """the least distance between segments pq and rt"""
    def pd(a, b, c):
        dx, dy = c[0] - b[0], c[1] - b[1]
        L = dx * dx + dy * dy
        u = 0.0 if L < 1e-18 else max(0.0, min(1.0, ((a[0] - b[0]) * dx + (a[1] - b[1]) * dy) / L))
        return _km_m.hypot(a[0] - b[0] - u * dx, a[1] - b[1] - u * dy)
    d1 = (q[0] - p[0], q[1] - p[1])
    d2 = (t[0] - r[0], t[1] - r[1])
    den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) > 1e-18:
        a = ((r[0] - p[0]) * d2[1] - (r[1] - p[1]) * d2[0]) / den
        b = ((r[0] - p[0]) * d1[1] - (r[1] - p[1]) * d1[0]) / den
        if 0.0 <= a <= 1.0 and 0.0 <= b <= 1.0:
            return 0.0
    return min(pd(p, r, t), pd(q, r, t), pd(r, p, q), pd(t, p, q))


def km_cut_marks(cuts, den, frame=None, gap_mm=None, T=None, box_mm=None, page=None, log=None, per_cut=False):
    """round 6 (S1, G6-5; from the site board's _t3_sec_key, the p08 target): the key map's cuts, bold red across
    (km_cut_items, R01), cuts = [(end1, end2, (name1, name2), look)] survey m, den = the key map's 1:den. Each cut
    lengthened about its middle to KM_MIN_L between its end bars where it is shorter on the map; neighbouring marks
    kept gap_mm (KM_GAP) apart: a mark that would touch an earlier one is drawn smaller (KM_SHRINK), else drawn
    with a WARNING line; end names that would touch another cut, a name or leave the map (T survey m -> key-map mm,
    box_mm = (w, h)) become ONE name beside the cut's middle (3.5-12 mm out, either side; none free = WARNING, set at
    the first spot). Returns the items (survey m), or per cut a list of items (per_cut=True)."""
    log = log if log is not None else KM_LOG
    gap = KM_GAP if gap_mm is None else float(gap_mm)
    m = den / 1000.0
    Tm = T or (lambda p: (p[0] / m, p[1] / m))
    fmw = globals().get("fm_width")
    pg = page or u""

    def tbox(it):
        x, y = Tm(it[2])
        w = fmw(it[1], it[3] / 0.352778, bold=it[5]) if callable(fmw) else 0.6 * it[3] * len(it[1])
        return (x - w / 2.0, y - it[3] / 2.0, x + w / 2.0, y + it[3] / 2.0)

    def segs_of(its):
        out_ = []
        for it in its:
            if it[0] == "line":
                P = [Tm(p) for p in it[1]]
                out_ += list(zip(P, P[1:]))
        return out_

    def inside(b):
        if not box_mm:
            return True
        return b[0] >= 0.6 and b[1] >= 0.6 and b[2] <= box_mm[0] - 0.6 and b[3] <= box_mm[1] - 0.6
    min_l = (2.0 * KM_CUT["end_bar"] + KM_MIN_L) * m
    done, done_segs, tboxes = [], [], []
    for c in cuts:
        a, b, nm = tuple(c[0]), tuple(c[1]), tuple(c[2])
        look = c[3] if len(c) > 3 and isinstance(c[3], (int, float)) else 1
        L0 = _km_m.hypot(b[0] - a[0], b[1] - a[1]) or 1e-6
        ux, uy = (b[0] - a[0]) / L0, (b[1] - a[1]) / L0
        if L0 < min_l:
            cx_, cy_ = 0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1])
            a, b = (cx_ - 0.5 * min_l * ux, cy_ - 0.5 * min_l * uy), (cx_ + 0.5 * min_l * ux, cy_ + 0.5 * min_l * uy)
        its, sg, crowd = None, None, False
        for k in KM_SHRINK:
            st = dict(end_bar=KM_CUT["end_bar"] * k, tri_h=KM_CUT["tri_h"] * k)
            its = km_cut_items([(a, b, nm, look)], den, frame=frame, style=st)
            sg = segs_of(its)
            if not any(_km_seg_dist(p, q, r, t) < gap for p, q in sg for r, t in done_segs):
                if k != 1.0:
                    log.append(u"keymap %s cut %s drawn at %.0f %% size (gap to its neighbour)" % (pg, nm[0], k * 100))
                break
        else:                                        # v32 (L1, LAYOUT_PLAN §3.2-5): marks closer than the gap keep
            crowd = True                             # their smallest size and their NAMES are pushed apart (no WARNING)
            log.append(u"keymap %s cut %s closer than %.1f mm to a neighbour: drawn at %.0f %% size, its name pushed "
                       u"clear of the neighbour" % (pg, nm[0], gap, KM_SHRINK[-1] * 100))
        others = list(done_segs)
        tx = [tbox(it) for it in its if it[0] == "text"]
        if tx and (crowd or not all(inside(bb) and not _km_box_hit(bb, tboxes, 0.6) and not _km_seg_hit(bb, others, 0.6)
                          for bb in tx)):
            its = [it for it in its if it[0] != "text"]
            nx, ny = -(b[1] - a[1]) / L0, (b[0] - a[0]) / L0
            mid = (0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1]))
            got = None
            for strict in (True, False):                 # clear of every cut line first, else of the texts only
                for off in (3.5, 5.0, 6.5, 8.0, 10.0, 12.0, 15.0, 18.0, 22.0):   # v32: further out before giving up
                    for sgn in (-1.0, 1.0):
                        it = ("text", nm[0], (mid[0] + sgn * nx * off * m, mid[1] + sgn * ny * off * m),
                              KM_CUT["text_mm"], KM_CUT["colour"], True, "MC")
                        bb = tbox(it)
                        if inside(bb) and not _km_box_hit(bb, tboxes, 0.6) and not (
                                strict and _km_seg_hit(bb, others + sg, 0.6)):
                            got = (it, bb)
                            break
                    if got:
                        break
                if got:
                    if not strict:
                        log.append(u"keymap %s: the name of cut %s crosses another cut's line (no clear place)"
                                   % (pg, nm[0]))
                    break
            if got is None:
                log.append(u"keymap %s: the name of cut %s set at its first spot (no free place here; the booklet "
                           u"places it)" % (pg, nm[0]))
                it = ("text", nm[0], (mid[0] - nx * 3.5 * m, mid[1] - ny * 3.5 * m), KM_CUT["text_mm"],
                      KM_CUT["colour"], True, "MC")
                got = (it, tbox(it))
            its.append(got[0])
            tx = [got[1]]
            log.append(u"keymap %s: cut %s named once beside its middle (its end names had no room)" % (pg, nm[0]))
        tboxes += tx
        done_segs += sg
        done.append(its)
    return done if per_cut else [it for its in done for it in its]


def km_keymap(page, cuts=None, cut_ids=None, zooms=None, w_mm=None, h_mm=None, box=None, scale_den=None,
              rotate=None, names=("streets", "places"), log=None, **more):
    """round 6 (S1, G6-5; PLAN §2.5, §2.8): THE key map of a page, the p08 "Where each street is cut" look. page:
    the booklet page id ("p08"); cuts: explicit cuts [(end1, end2, (name1, name2), look[, id])] survey m; cut_ids:
    cut registry ids (levels.py) and zoom / window ids; zooms {id: polygon survey m}; w_mm / h_mm: the most the page
    frame offers (fitted map, km_map's rule) or, with scale_den, a fixed scale; box: survey box to show (widened to
    hold the whole study outline); rotate: None = corridor along the long side, a number = degrees, False = north
    up; names: which name kinds ("streets", "places"; () = none). more: km_map's other options (legend_box,
    extra_names, looks, D, margin, fit, pad_mm, north). Returns km_map's dict plus study_ring (the closed rings),
    study_closed (1), rotation, page; logs `keymap <page> module cuts=<ids> study_closed=1`."""
    nm = dict(streets=("main",) if "streets" in (names or ()) else (), places="places" in (names or ()))
    D = more.pop("D", None)
    D = D if D is not None else basemap_load()
    ring = km_study_ring(D)
    km = km_map(list(cut_ids or ()), w_mm, h_mm, zooms=zooms, page=page, names=nm, log=log, box=box,
                scale_den=scale_den, rotate=rotate, D=D, cuts=cuts, study=ring, strong=True, **more)
    km["study_ring"] = ring
    km["study_closed"] = 1 if ring else 0
    km["rotation"] = km["rotation_deg"]
    km["cuts_all"] = list(km["cut_ids"])
    KM_STUDY_LOG[page] = (len(ring), km["study_closed"])
    km_log(page, km, log)
    return km


def km_draw_to(km, X, fill_fn, line_fn, text_fn, **kw):
    """round 6: draws a km_keymap on a board / page (km_draw: paper, base, water, study line whole and unclipped, red
    cuts, names, frame line, north arrow); X(q) key-map mm -> page point"""
    return km_draw(km, X, fill_fn, line_fn, text_fn, **kw)


def km_export_items(km, page=None, item_id=None, priority=5):
    """round 6: a km_keymap as booklet items (km_items: drawing, labels, keymap item)"""
    return km_items(km, page=page, item_id=item_id, priority=priority)


def km_log(page, km=None, log=None):
    """`keymap <page> module cuts=<ids> study_closed=<1|0> parts=<n>` (the G6-5 done-when line; study_closed=1 =
    every study ring drawn whole and closed). A page with no study data logs study_closed=0 with a WARNING."""
    n, closed = KM_STUDY_LOG.get(page, (0, 0))
    ids = u",".join((km or {}).get("cut_ids") or []) or u"-"
    ln = u"keymap %s module cuts=%s study_closed=%d parts=%d" % (page, ids, closed, n)
    lg = log if log is not None else KM_LOG
    lg.append(ln)
    if not closed:
        lg.append(u"WARNING %s keymap: no study outline (no basemap study layer and no recorded copy)" % page)
    if lg is not KM_LOG:
        KM_LOG.append(ln)
    return ln



# ---- old names (round 3 callers; page sessions move to km_map / km_cut_items) -------------------------------------
def basemap_cut_items(cuts, scale_den, frame=None, inset_mm=3.0, tri_mm=2.6, text_mm=2.4, col=None, D=None):
    """round 3 name, now the R01 red symbol (G-R4-9): km_cut_items(cuts, scale_den, frame or the analysis frame).
    inset_mm, tri_mm and col are ignored (one symbol, one colour everywhere)."""
    return km_cut_items(cuts, scale_den, frame=frame or basemap_frame(D), text_mm=max(text_mm, 2.12))


def keymap_items(ids=(), scale_den=10000.0, box=None, zooms=None, mode="key", override=None, looks=None, D=None,
                 margin=0.06, text_mm=2.4, col=None, log=None, page=None):
    """round 3 name, now km_map at the caller's scale and box (mode, override, text_mm and col are ignored: the base is
    the muted one, the cuts R01 red): dict(items (survey m, in order), box, drawn, missing) as before"""
    km = km_map(ids, None, None, zooms=zooms, page=page, log=log, looks=looks, box=box, scale_den=scale_den, D=D,
                margin=margin, names=dict(streets=(), places=False))     # round 3 key maps had no names
    return dict(items=km["items"], box=km["box"], drawn=km["drawn"], missing=km["missing"])
