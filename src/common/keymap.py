# ---- Key maps, cut symbol, north arrow (round 4 S2, 1 Nov 2026; G-R4-9, R01, U02 U31 U50 U51 U55 U60; PLAN §4.5) -----
# ONE key-map module: every cut line drawn with the R01 symbol in red (an end bar with an open triangle standing on it
# pointing the way the section looks, a dash-dot line between), in front of a muted base, with ONLY the page's cuts,
# the main street and place names (so the reader knows where it is), never over its legend; ONE north arrow (the
# arrow and "N", no plate, U31 U51). Included by common/basemap.py (its last lines, after map_layers.py); do not
# include it again. The old basemap_cut_items / keymap_items are thin wrappers at the end of this file.
#   KM_CUT, KM_NAMES                             the cut symbol and the names switches
#   km_cut_items(cuts, scale_den, frame=None, style=None, text_mm=2.47)      R01 cut symbols as items (survey m)
#   km_map(ids, w_mm, h_mm, zooms=None, page=None, names=None, legend_box=None, log=None, looks=None, box=None,
#          scale_den=None, extra_names=None, D=None, margin=0.06)           a whole key map (survey m + its T)
#   km_draw(km, X, fill_fn, line_fn, text_fn, water_opts=None, page=None)   draws it through map_draw
#   km_texts(km)                                 its texts in key-map mm, for the page's TextPage (.put)
#   north_items(x, y, ang_rad=0.0, size_mm=6.0, colour="2C2219")           the north arrow (page mm, y up)
# Items: the basemap format (common/basemap.py head). Key-map mm: origin at the key map's lower-left, y up.
import math as _km_m

# R01 in red (G-R4-9): line 0.5 mm dash-dot; end bar 2.4 mm along the line at each end, the open triangle standing on
# it (base = the bar, height tri_h, apex the way the section looks), the end name beyond the bar. Sizes: drawing rules
# of PLAN §4.5 (the triangle's base is the bar so it never overhangs it).
KM_CUT = dict(colour="C0392B", lw=0.5, dash=(3.0, 0.8, 0.6, 0.8), end_bar=2.4, bar_lw=0.6, tri_h=2.1, tri_lw=0.35,
              text_mm=2.47, gap_mm=0.8)
KM_NAMES = dict(streets=("main",), n_streets=4, places=True, n_places=6, size_mm=2.12, colour="6B645B", bold=False,
                pad_mm=0.6)
KM_ZOOM = dict(colour="C0392B", lw=0.35)       # zoom / window frames on a key map: the cut red, solid
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
        look = c[3] if len(c) > 3 else 1
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
            if L <= 2.0 * pull + 2.0 * st["end_bar"] * m:
                continue
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


def km_map(ids, w_mm, h_mm, zooms=None, page=None, names=None, legend_box=None, log=None, looks=None, box=None,
           scale_den=None, extra_names=None, D=None, margin=0.06):
    """a whole key map (G-R4-9) fitted to w_mm x h_mm (key-map mm, origin lower-left, y up; north up). ids: the
    page's cut ids (the cut registry, levels.py) and zoom ids (zooms {id: polygon survey m}, else level_window(id));
    with no ids and page given, every cut the registry draws on that page. box: survey m (default the study area +
    every cut and zoom, widened by margin); scale_den: fixed scale (default: the scale that fills w x h; a key map is
    a diagram, no scale bar); w_mm / h_mm None with scale_den: the box at that scale. Layers: muted base (ml_base) -> study line -> zoom frames -> R01 cuts in red -> names.
    Names (names = KM_NAMES overrides): the main streets' OpenStreetMap names (basemap_street_names, longest first),
    the place names of the basemap and extra_names [(name, (x, y))], each placed (font_metrics fm_width, S1) clear
    of the cuts, their labels, the legend_box (key-map mm) and each other; a name that finds no place is left out
    and logged (a key map is never crowded). Returns dict(base, study, cuts, names (items, survey m), items (all, in
    order), box, scale_den, T (survey -> key-map mm), Tinv, drawn, missing, label_boxes (key-map mm), w_mm, h_mm)."""
    D = D if D is not None else basemap_load()
    log = log if log is not None else KM_LOG
    nm_st = dict(KM_NAMES)
    nm_st.update(names or {})
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
        log.append(u"WARNING: key map %s: '%s' is neither a cut of the registry nor a zoom passed in: not drawn."
                   % (page or u"", cid))
    study = basemap_study(D)
    if box is None:
        pts = [p for R in study for p in R] + [p for _, c in cuts for p in c[:2]] + [p for _, w in wins for p in w]
        if not pts:
            pts = list(basemap_extent(D) or [])
        if not pts:
            raise ValueError(u"key map %s: nothing to frame (no basemap data, no cuts)" % (page or u""))
        x0, y0, x1, y1 = _bm_bb(pts)
        d = margin * max(x1 - x0, y1 - y0, 1.0)
        box = (x0 - d, y0 - d, x1 + d, y1 + d)
    bw, bh = box[2] - box[0], box[3] - box[1]
    if scale_den and (w_mm is None or h_mm is None):     # a fixed scale: the key map is the box at that scale
        w_mm, h_mm = bw * 1000.0 / scale_den, bh * 1000.0 / scale_den
    den = float(scale_den) if scale_den else max(bw * 1000.0 / w_mm, bh * 1000.0 / h_mm)
    s = 1000.0 / den
    cx, cy = (box[0] + box[2]) / 2.0, (box[1] + box[3]) / 2.0

    def T(p):
        return ((p[0] - cx) * s + w_mm / 2.0, (p[1] - cy) * s + h_mm / 2.0)

    def Tinv(q):
        return ((q[0] - w_mm / 2.0) / s + cx, (q[1] - h_mm / 2.0) / s + cy)
    # the visible box (the key map's own rectangle, survey m) frames the cut symbols
    vb = (Tinv((0.0, 0.0)), Tinv((w_mm, h_mm)))
    frame = [(vb[0][0], vb[0][1]), (vb[1][0], vb[0][1]), (vb[1][0], vb[1][1]), (vb[0][0], vb[1][1])]
    base = ml_base((vb[0][0], vb[0][1], vb[1][0], vb[1][1]), den, D=D) if D else []
    st_items = ml_study_items(study)
    cut_items = []
    for cid, c in cuts:
        its = km_cut_items([c], den, frame=frame)
        nm_fn = globals().get("level_name")
        try:
            name = nm_fn(cid) if callable(nm_fn) else cid
        except Exception:
            name = cid
        name = u"%s" % name
        name = name.split("-")[0]                        # a crossing row (S5-2) is labelled by its cut (S5)
        if name not in c[2][0] and name not in c[2][1]:  # end names that do not say the id ("SW" / "NE"): the id too
            a, b = c[0], c[1]
            L0 = _km_m.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
            nx, ny = -(b[1] - a[1]) / L0, (b[0] - a[0]) / L0
            q = ((a[0] + b[0]) / 2.0 + nx * KM_CUT["text_mm"] * 1.2 / s, (a[1] + b[1]) / 2.0 + ny * KM_CUT["text_mm"]
                 * 1.2 / s)
            its.append(("text", name, q, KM_CUT["text_mm"], KM_CUT["colour"], True, "MC"))
        cut_items += its
    for cid, w in wins:
        cut_items.append(("line", list(w) + [w[0]], KM_ZOOM["colour"], KM_ZOOM["lw"], None, 1.0))
        x0, y0, x1, y1 = _bm_bb(w)
        cut_items.append(("text", cid, (x0 + KM_CUT["text_mm"] * 0.9 / s, y1 + KM_CUT["text_mm"] * 0.8 / s),
                          KM_CUT["text_mm"], KM_CUT["colour"], True, "MC"))
    cand = []
    if nm_st.get("streets"):
        for n, p, _a, _cl, _ln in basemap_street_names(None, D, classes=tuple(nm_st["streets"]))[:4 * nm_st["n_streets"]]:
            cand.append((n, p, "street"))
    if nm_st.get("places"):
        for n, p in basemap_names(None, D):
            cand.append((n, p, "place"))
    for n, p in extra_names or ():
        cand.append((n, tuple(p), "extra"))
    # obstacles in key-map mm: cut lines / bars / triangles, cut and zoom labels, the legend
    fmw = globals().get("fm_width")
    if cand and not callable(fmw):
        raise RuntimeError(u"km_map needs common/font_metrics.py (round 4 S1: fm_width) included before it is "
                           u"called: text widths come from the real font only")
    pt_of = lambda mm: mm / 0.352778
    segs, boxes, label_boxes = [], [], []
    for it in cut_items:
        if it[0] == "line":
            P = [T(p) for p in it[1]]
            segs += list(zip(P, P[1:]))
        elif it[0] == "text" and callable(fmw):
            x, y = T(it[2])
            w = fmw(it[1], pt_of(it[3]), bold=it[5])
            b = (x - w / 2.0, y - it[3] / 2.0, x + w / 2.0, y + it[3] / 2.0)
            boxes.append(b)
            label_boxes.append((it[1], b))
    if legend_box:
        boxes.append(tuple(legend_box))
    sz = nm_st["size_mm"]
    pad = nm_st["pad_mm"]
    name_items, placed = [], {"street": 0, "place": 0, "extra": 0}
    lim = {"street": nm_st["n_streets"], "place": nm_st["n_places"], "extra": 10 ** 6}
    for n, p, kind in cand:
        if placed[kind] >= lim[kind]:
            continue
        x, y = T(p)
        if not (0.0 <= x <= w_mm and 0.0 <= y <= h_mm):
            continue
        w = fmw(n, pt_of(sz), bold=nm_st["bold"])
        ok = None
        for dx, dy in ((0.0, 0.0), (0.0, sz * 1.1), (0.0, -sz * 1.1), (w / 2.0 + 1.0, 0.0), (-w / 2.0 - 1.0, 0.0),
                       (0.0, sz * 2.2), (0.0, -sz * 2.2)):
            b = (x + dx - w / 2.0, y + dy - sz / 2.0, x + dx + w / 2.0, y + dy + sz / 2.0)
            if b[0] < pad or b[1] < pad or b[2] > w_mm - pad or b[3] > h_mm - pad:
                continue
            if _km_box_hit(b, boxes, pad) or _km_seg_hit(b, segs, pad):
                continue
            ok = b
            break
        if ok is None:
            log.append(u"key map %s: name '%s' left out (no free place)" % (page or u"", n))
            continue
        boxes.append(ok)
        label_boxes.append((n, ok))
        placed[kind] += 1
        name_items.append(("text", n, Tinv(((ok[0] + ok[2]) / 2.0, (ok[1] + ok[3]) / 2.0)), sz, nm_st["colour"],
                           nm_st["bold"], "MC"))
    KM_LOG.append(u"key map %s: cuts %s, zooms %d, names %d, 1:%d (diagram, no bar)"
                  % (page or u"", u", ".join(cid for cid, _ in cuts) or u"-", len(wins), len(name_items), int(den)))
    return dict(base=base, study=st_items, cuts=cut_items, names=name_items,
                items=list(base) + st_items + cut_items + name_items, box=box, scale_den=den, T=T, Tinv=Tinv,
                drawn=drawn, missing=missing, label_boxes=label_boxes, w_mm=w_mm, h_mm=h_mm,
                study_rings=study)


def km_draw(km, X, fill_fn, line_fn, text_fn, water_opts=None, page=None, log=None):
    """draws a km_map through map_draw (G-R4-4 order: muted base, then the study line, then the red cuts, then the
    names): X(q) key-map mm -> page point (e.g. lambda q: (x0 + q[0], y0 + q[1]), or a y-down flip). Returns
    map_draw's dict."""
    T = km["T"]
    return map_draw(page or u"key", lambda p: X(T(p)), fill_fn, line_fn, text_fn, km["base"],
                    {"proj_marks": [it for it in km["cuts"] if it[0] != "text"],
                     "proj_labels": [it for it in km["cuts"] if it[0] == "text"] + km["names"]},
                    study=km.get("study_rings"), clip=False, log=log, water_opts=water_opts)


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
