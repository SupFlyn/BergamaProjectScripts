# ---- Map layers (round 4 S2, 1 Nov 2026; G-R4-4 "base map back, our drawings in front", D9 tint; PLAN §4.3) ---------
# ONE draw-order function for every map, plan and axo (p02, p06, p08, p10, p12, p16, p17, p20, p21, p22 and every key
# map): the base map muted, light and at the bottom; our drawings saturated and on top; the study line in its own
# layer above the project fills; proposals clipped to the study area at draw time too (study_clip.py) and counted.
# Included by common/basemap.py (its last lines, after study_clip.py); do not include it again.
# Items: the basemap format (common/basemap.py head), survey m (or already projected, e.g. an axo: then T = identity).
# Round 5 (S2, 1 Nov 2026; G-R5-8 "water drawn above every zone tint", G-R5-10 "base muted and cropped"): two layers
# after the project tints, "water" (the base stream) and "structures" (decks, covered course, bridges over it); a flat
# base list is filed by each item's layer (basemap _BmIt) so the stream lands in "water"; a base dict's "base_water"
# is drawn as "water" too; map_draw logs `zones <page> over_water_area <m2>, unlabeled_fields <n>`; ml_base crops.
#   ML_LAYERS                                   the 15 layers, bottom first
#   ml_base(box, scale_den, D=None, contours=False, names=False, override=None, crop=True)  the muted base (basemap
#                                               "muted"), cut to box (round 5, G-R5-10)
#   ml_crop(items, ring)                        round 5: items cut to a convex ring (survey m): fills, lines, water
#   ml_layer_of(item)                           round 5: the ML layer a base item belongs to
#   ml_tint(rings, colour=None, alpha=None, study=None, page=None)    D9 footprint tint items (clipped to the study)
#   ml_study_items(rings=None, D=None)          the study-area line items (BM_STUDY_LINE, one style everywhere)
#   map_draw(page, T, fill_fn, line_fn, text_fn, base, project, study=None, clip=True, order_fn=None, log=None,
#            water_opts=None, study_line=True, legend_cols=None, water_ok=None)
#                                               draws base -> project strictly in ML_LAYERS order; logs the done-when
#                                               line "layers base→project ok, n_outside_clipped <n> (<page>)" and
#                                               round 5 "zones <page> over_water_area <m2>, unlabeled_fields <n>"
# round 5 (S2, G-R5-8; PLAN §3 draw order: base fills -> tints / zone fields -> WATER -> structures over water ->
# planting -> people -> labels): "water" and "structures" follow "proj_tint"; the old names keep their places so
# stage lists that check the order (water board p12) still pass
ML_LAYERS = ("base_ground", "base_contours", "base_fills", "base_water", "base_outlines", "base_names",
             "proj_tint", "water", "structures", "proj_water", "proj_lines", "proj_vegetation", "study", "proj_marks",
             "proj_labels")
ML_BASE_LAYERS = ("base_ground", "base_contours", "base_fills", "base_water", "base_outlines", "base_names", "water",
                  "structures")
ML_PROJ_LAYERS = ("proj_tint", "proj_water", "proj_lines", "proj_vegetation", "study", "proj_marks", "proj_labels")
ML_FIELD_LAYERS = ("proj_lines", "proj_vegetation", "proj_marks")   # fills here are drawn above the stream
# D9 (Aras 1 Nov, U52 "çok hafif izdüşüm ... transparan çok hafif bir renkle"): the proposal footprint tint, very
# light and transparent, on every plan that shows proposals (p08, p10 plans, p12, p16, p17, p21, p22)
ML_TINT = "5C7A86"                  # palette reference slate (library/examples/palettes)
ML_TINT_ALPHA = 0.16
ML_NAME_MM = 2.12                   # base names 6 pt (the booklet minimum, G-R4-1), BM_MUTED["name"] tone
ML_NO_CLIP = ("proj_labels",)       # labels are placed by the text placer and may sit just outside the line
ML_LOG = []                         # this run's map_draw lines (a page script appends them to its log)


def ml_base(box, scale_den, D=None, contours=False, names=False, override=None, crop=True):
    """the muted base of a map (G-R4-4): basemap mode "muted" = the stream (M5 water), light streets with closed
    edges, light houses with ONE closed outline per block, every outline after every fill; contours=True adds the
    contours coloured to the relief (green ramp, lighter = lower, U48); names=True the place names (6 pt, pale).
    The study line is NOT in it (map_draw draws it in its own layer). box = (x0, y0, x1, y1) survey m; scale_den =
    the map's 1:scale_den. Returns basemap items (bottom first), [] without basemap data. Round 5 (G-R5-10):
    crop=True cuts every item to box, so nothing of the base runs past the drawing's window."""
    ov = dict(contours="height" if contours else False, names=bool(names))
    ov.update(override or {})
    its = basemap_items("muted", ov, box=box, D=D, scale_den=scale_den)
    its = [_bm_tag(("text", it[1], it[2], ML_NAME_MM, BM_MUTED["name"], False, it[6]), "base_names")
           if it[0] == "text" else it for it in its]
    if crop and box:
        its = ml_crop(its, [(box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])])
    return its


def _ml_clip_poly(R, ring):
    """ring R cut to the convex ring (Sutherland-Hodgman, any turn); [] when nothing is left"""
    n = len(ring)
    ccw = sum((ring[(i + 1) % n][0] - ring[i][0]) * (ring[(i + 1) % n][1] + ring[i][1]) for i in range(n)) < 0
    out = list(R)
    for i in range(n):
        a, b = ring[i], ring[(i + 1) % n]
        ex, ey = b[0] - a[0], b[1] - a[1]

        def side(p):
            c = ex * (p[1] - a[1]) - ey * (p[0] - a[0])
            return c if ccw else -c
        if not out:
            return []
        nxt = []
        for j in range(len(out)):
            p, q = out[j - 1], out[j]
            sp, sq = side(p), side(q)
            if sq >= 0:
                if sp < 0:
                    t = sp / (sp - sq)
                    nxt.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
                nxt.append(q)
            elif sp >= 0:
                t = sp / (sp - sq)
                nxt.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
        out = nxt
    return out if len(out) >= 3 else []


def _ml_inside_convex(P, ring):
    n = len(ring)
    ccw = sum((ring[(i + 1) % n][0] - ring[i][0]) * (ring[(i + 1) % n][1] + ring[i][1]) for i in range(n)) < 0
    for i in range(n):
        a, b = ring[i], ring[(i + 1) % n]
        for p in P:
            c = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
            if (c if ccw else -c) < 0:
                return False
    return True


def _ml_retag(src, t):
    lay = getattr(src, "layer", None)
    return _bm_tag(t, lay) if lay else t


def ml_crop(items, ring):
    """round 5 (S2, G-R5-10): basemap items cut to the convex ring (survey m, e.g. a key map's turned frame):
    fills ring by ring (a ring wholly inside is kept as it is), lines run by run, the "water" item ring by ring,
    texts kept when their point is inside. Each item keeps its map layer."""
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    bb = (min(xs), min(ys), max(xs), max(ys))

    def rings_cut(Rs):
        out = []
        for R in Rs:
            if len(R) < 3:
                continue
            if _ml_inside_convex(R, ring):
                out.append(R)
                continue
            rx, ry = [p[0] for p in R], [p[1] for p in R]
            if max(rx) < bb[0] or min(rx) > bb[2] or max(ry) < bb[1] or min(ry) > bb[3]:
                continue
            c = _ml_clip_poly(R, ring)
            if c:
                out.append(c)
        return out
    out = []
    for it in items:
        if it[0] == "fill":
            rs = rings_cut(it[1])
            if rs:
                out.append(_ml_retag(it, ("fill", rs) + tuple(it[2:])))
        elif it[0] == "line":
            P = it[1]
            if _ml_inside_convex(P, ring):
                out.append(it)
                continue
            for a, b in zip(P, P[1:]):
                ab = _bm_clip_convex(a, b, ring)
                if ab:
                    out.append(_ml_retag(it, ("line", [ab[0], ab[1]]) + tuple(it[2:])))
        elif it[0] == "water":
            gs = []
            for g in it[1]:
                c = rings_cut([g[0]])
                if c:
                    gs.append(c + rings_cut(g[1:]))
            if gs:
                es = []
                for P in it[2]:
                    for a, b in zip(P, P[1:]):
                        ab = _bm_clip_convex(a, b, ring)
                        if ab:
                            es.append([ab[0], ab[1]])
                out.append(_ml_retag(it, ("water", gs, es) + tuple(it[3:])))
        elif it[0] == "text":
            if _ml_inside_convex([it[2]], ring):
                out.append(it)
        else:
            out.append(it)
    return out


def ml_layer_of(it):
    """round 5 (S2, G-R5-8): the map layer of a base item: its own (basemap _BmIt.layer), else by kind (the stream
    item and the base water tones -> "water", texts -> "base_names", the rest "base_fills")"""
    lay = getattr(it, "layer", None)
    if lay in ML_BASE_LAYERS:
        return "water" if lay == "base_water" else lay
    if it[0] == "water":
        return "water"
    if it[0] == "text":
        return "base_names"
    wc = (BM_COL["water"], BM_COL["water_edge"], BM_KEY["water"], BM_KEY["water_edge"])
    if it[0] in ("fill", "line") and it[2] in wc:
        return "water"
    return "base_fills"


def _ml_pip(x, y, R):
    ins = False
    j = len(R) - 1
    for i in range(len(R)):
        xi, yi = R[i]
        xj, yj = R[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi:
            ins = not ins
        j = i
    return ins


def _ml_over_water(fills, water, T=None, n=12):
    """round 5 (S2, G-R5-8): the area (m², or page mm² when the items are already projected) of fills that lie
    over the water rings, estimated on an n x n grid per fill ring (even-odd inside both)"""
    if not fills or not water:
        return 0.0
    wb = [(R, (min(p[0] for p in R), min(p[1] for p in R), max(p[0] for p in R), max(p[1] for p in R)))
          for R in water if len(R) >= 3]
    area = 0.0
    for it in fills:
        for R in it[1]:
            if len(R) < 3:
                continue
            x0, y0 = min(p[0] for p in R), min(p[1] for p in R)
            x1, y1 = max(p[0] for p in R), max(p[1] for p in R)
            if not any(not (b[2] < x0 or b[0] > x1 or b[3] < y0 or b[1] > y1) for _, b in wb):
                continue
            dx, dy = (x1 - x0) / n, (y1 - y0) / n
            hit = 0
            for i in range(n):
                for j in range(n):
                    x, y = x0 + (i + 0.5) * dx, y0 + (j + 0.5) * dy
                    if _ml_pip(x, y, R) and any(b[0] <= x <= b[2] and b[1] <= y <= b[3] and _ml_pip(x, y, W)
                                                for W, b in wb):
                        hit += 1
            area += hit * dx * dy
    return area


def ml_tint(rings, colour=None, alpha=None, study=None, page=None):
    """D9: the light transparent footprint of what we change (channel setbacks, ponds, basins, terraces, store, new
    paths) as fill items, one per ring, clipped to the study rings (study_clip sc_rings_clip) when study is given.
    rings: [ring, ...] survey m (or page mm with study=None). Put them in map_draw's "proj_tint" layer."""
    col, a = colour or ML_TINT, ML_TINT_ALPHA if alpha is None else alpha
    out = []
    for R in rings or ():
        if len(R) < 3:
            continue
        for r in (sc_rings_clip(R, study, page) if study else [R]):
            out.append(("fill", [r], col, a, True))
    return out


def ml_study_items(rings=None, D=None):
    """the study-area outline as line items, ONE style everywhere (BM_STUDY_LINE: violet long-dash-dot, U18/U19);
    rings default = the basemap's study area"""
    st = BM_STUDY_LINE
    rings = rings if rings is not None else basemap_study(D)
    return [("line", list(R) + [R[0]], st["colour"], st["width_mm"], list(st["dash_mm"]), 1.0)
            for R in rings or () if len(R) >= 3]


def map_draw(page, T, fill_fn, line_fn, text_fn, base, project, study=None, clip=True, order_fn=None, log=None,
             water_opts=None, study_line=True, legend_cols=None, water_ok=None):
    """THE draw order of every map (G-R4-4 done-when). page: the booklet page id ("p21"); T(p) survey m -> page
    point (identity for items already projected); fill_fn / line_fn / text_fn as basemap_draw. base: the base items
    (ml_base, in their own order) or {base layer: items}; project: {layer: items} or [(layer, items)] with layers
    from ML_PROJ_LAYERS ("proj_tint", "proj_water", "proj_lines", "proj_vegetation", "proj_marks", "proj_labels");
    study: the study rings (sc_rings): with clip=True every project item except labels is clipped to them
    (sc_items) and counted; the study line goes in the "study" layer (study_line=False leaves it out, e.g. a key map
    that draws its own). order_fn(layer): called before each layer is drawn (the site board's page order numbers:
    base 2-28, tint 30-39, project 40-59, marks 60-69). Draws strictly in ML_LAYERS order, whatever order the
    caller listed. Returns dict(n_base, n_project, n_outside_clipped, layers) and logs (ML_LOG and log) "layers
    base→project ok, n_outside_clipped <n> (<page>)".
    Round 5 (S2, G-R5-8): the base stream is drawn in "water", above "proj_tint" (a flat base list is filed by
    ml_layer_of; a base dict's "base_water" goes to "water"), decks / covered course / bridges in "structures". Logs
    `zones <page> over_water_area <m2>, unlabeled_fields <n>`: over_water_area = fills in proj_lines /
    proj_vegetation / proj_marks (drawn above the stream) over the base water, minus fills whose colour is in
    water_ok (fields in the water by design: widened stream, wetland, sub-hub, spillway, reed arms); unlabeled_fields
    = tint and field fills whose colour is not in legend_cols (the legend's swatch colours; "n/a" + a FLAG when the
    page passes none). A count above 0 is a WARNING line (the run goes on)."""
    if isinstance(base, dict):
        bad = [k for k in base if k not in ML_BASE_LAYERS]
        if bad:
            raise ValueError(u"map_draw %s: base layer(s) %s unknown: use %s" % (page, bad, ", ".join(ML_BASE_LAYERS)))
        bd = {}
        for k in ML_BASE_LAYERS:
            if base.get(k):
                bd.setdefault("water" if k == "base_water" else k, []).extend(base[k])
        base_l = [(k, bd[k]) for k in ML_BASE_LAYERS if bd.get(k)]
    else:
        bd = {}
        for it in base or []:
            bd.setdefault(ml_layer_of(it), []).append(it)
        base_l = [(k, bd[k]) for k in ML_BASE_LAYERS if bd.get(k)]
    proj = {}
    for k, its in (project.items() if isinstance(project, dict) else (project or [])):
        if k not in ML_PROJ_LAYERS or k == "study":
            raise ValueError(u"map_draw %s: project layer %r unknown: use %s" % (page, k, ", ".join(
                l_ for l_ in ML_PROJ_LAYERS if l_ != "study")))
        proj.setdefault(k, []).extend(its or [])
    if study and clip:
        for k in list(proj):
            if k not in ML_NO_CLIP:
                proj[k] = sc_items(proj[k], study, page)
    if study and study_line:
        proj["study"] = ml_study_items(study)
    n_out = sc_count(page)                               # this page's clips this run: at the source + here
    nb = npj = 0
    drawn = []
    for layer in ML_LAYERS:
        its = dict(base_l).get(layer) if layer in ML_BASE_LAYERS else proj.get(layer)
        if not its:
            continue
        if order_fn is not None:
            order_fn(layer)
        n = basemap_draw(its, T, fill_fn, line_fn, text_fn, water_opts)
        drawn.append(layer)
        if layer in ML_BASE_LAYERS:
            nb += n
        else:
            npj += n
    ok = all(ML_LAYERS.index(a) < ML_LAYERS.index(b) for a, b in zip(drawn, drawn[1:]))
    line = (u"layers base→project %s, n_outside_clipped %d (%s: %s)"
            % (u"ok" if ok else u"FLAG out of order", n_out, page, u", ".join(drawn)))
    ML_LOG.append(line)
    if log is not None:
        log.append(line)
    # round 5 (S2, G-R5-8): the zones done-when line
    wrings = basemap_water_rings(dict(base_l).get("water") or [])
    wrings += [R for it in dict(base_l).get("water") or [] if it[0] == "fill" and it[2] not in
               (BM_COL["water"],) for R in it[1] if len(R) >= 3]
    ok_c = set(str(c).upper() for c in (water_ok or ()))
    above = [it for k in ML_FIELD_LAYERS for it in proj.get(k) or []
             if it[0] == "fill" and str(it[2]).upper() not in ok_c]
    ow = _ml_over_water(above, wrings)
    tints = [it for k in ("proj_tint",) + ML_FIELD_LAYERS for it in proj.get(k) or [] if it[0] == "fill"]
    if legend_cols is None:
        nu = u"n/a"
    else:
        lc = set(str(c).upper() for c in legend_cols)
        nu = sum(1 for it in tints if str(it[2]).upper() not in lc)
    zl = u"zones %s over_water_area %d, unlabeled_fields %s" % (page, int(round(ow)), nu)
    extra = []
    if ow > 0.5 or (nu != u"n/a" and nu > 0):
        extra.append(u"WARNING %s zones over_water_area %d, unlabeled_fields %s" % (page, int(round(ow)), nu))
    if nu == u"n/a" and tints:
        extra.append(u"FLAG zones %s: no legend colours passed, unlabeled fields not counted" % page)
    for l_ in [zl] + extra:
        ML_LOG.append(l_)
        if log is not None:
            log.append(l_)
    return dict(n_base=nb, n_project=npj, n_outside_clipped=n_out, layers=drawn, over_water_area=ow,
                unlabeled_fields=nu)


def ml_lines_log():
    """this run's map_draw lines, then emptied"""
    out = list(ML_LOG)
    del ML_LOG[:]
    return out
