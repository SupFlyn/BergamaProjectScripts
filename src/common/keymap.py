# ---- Key maps, cut symbol, north arrow (round 4 S2, 1 Nov 2026; G-R4-9, R01, U02 U31 U50 U51 U55 U60) -----------------
# ONE key-map module: the page's cuts in the R01 symbol in red (an end bar with an open triangle standing on it
# pointing the way the section looks, a dash-dot line between), the main street and place names, ONE north arrow (the
# arrow and "N", no plate, U31 U51). Included by common/basemap.py (its last lines, after map_layers.py); do not
# include it again. History: round 4 v1 (R01 red), round 5 v2 (base mode "keymap", items for the booklet), round 6 v3
# (closed study rings, gaps between cut marks), round 7 v4 below. Items: the basemap format (common/basemap.py head).
# Key-map mm: origin at the key map's lower-left, y up.
# ROUND 7 (S1, 5 Nov 2026; G7-3, BRIEF D2 exception; PLAN §4.3): v4 = SON page8's key map REUSED (Aras 08:59 "AND
# REPLACE THE KEYMAPS", 09:00 "no reuse the old keymap"): _t3_sec_key (1d6f866 p07_09_movement.py:1556-1727) on keymap
# v2, made callable with (page, cuts, frame w x h). Where round 6's v3 differed, SON page8 wins: the map on the site
# frame's own axes (no turn to the corridor), names 6B645B 6 pt (4 pt floor), frame line INK2 0.15 mm on white, the
# north arrow 4 mm OUTSIDE the frame in a 9 mm column, a heading above, base "keymap" as is (round 6's strong recolour
# gone). Its only fix: the study outline = closed rings, never clipped (the frame's content holds every ring).
# The frame is the page's SON key-map frame EXACTLY (no fitting of the frame; one uniform scale fills it). Removed:
# km_map, km_texts, _km_strong, _km_axis_deg, KM_CUT_PLAN, the round 3 wrappers basemap_cut_items / keymap_items.
#   km_keymap(page, cuts=None, w_mm=None, h_mm=None, heading=None, zooms=None, log=None, cut_ids=None, looks=None,
#             north_side="right", extra_names=None, D=None)       THE call (cuts: registry ids and / or explicit cuts)
#   km_draw_to(km, X, fill_fn, line_fn, text_fn)    draw on a board / page;  km_export_items(km, page, item_id)
#   km_log(page)                                     `keymap <page> module cuts=<ids> study_closed=1 parts=<n>`
#   km_cut_items(cuts, scale_den, frame=None, style=None, text_mm=None)    R01 cut symbols as items (survey m)
#   km_cut_marks(cuts, den, frame=None, gap_mm=1.5, T=None, box_mm=None, page=None, log=None, per_cut=False)
#   km_study_ring(D=None, rings=None)                the study outline: closed rings, overlapping parts unioned
#   km_street_names(D, T, obstacles, vb=..., ...)    the street / place names, placed clear of obstacles
#   km_draw(km, X, ...) / km_items(km, page, item_id, priority)   the drawing and export behind km_draw_to /
#                                                    km_export_items
#   north_items(x, y, ang_rad=0.0, size_mm=6.0, colour="2C2219")   THE north arrow (page mm, y up)
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
KM_NAMES = dict(streets=("main",), n_streets=4, places=True, n_places=6, size_mm=2.12, colour="6B645B",
                bold=False, pad_mm=0.6)     # round 7 (G7-3): SON page8's names (keymap v2 KM_NAMES: 6 pt, 6B645B)
KM_NAMES_MIN = 4.0 * 0.352778    # round 7: a name with no room at 6 pt tries 4 pt (the floor), never smaller
KM_MIN_L = 1.0           # mm: round 6 (from the site board's T3_KEY_MIN_L): a cut's line between its end bars at least
#                          this long on the key map (a street is 10-20 m wide, under 2 mm at a key map's scale)
KM_GAP = 1.5             # mm: round 6 (G6-5 "gaps"): neighbouring cut marks keep at least this apart
KM_SHRINK = (1.0, 0.75, 0.55)      # round 6: symbol sizes tried when two marks would touch
KM_ZOOM = dict(colour="C0392B", lw=0.35)       # zoom / window frames on a key map: the cut red, solid
KM_FRAME = dict(colour="7A6E60", lw=0.15)      # round 7 (G7-3): SON page8's frame line (site board INK2 0.15 mm)
KM_PAPER = "FFFFFF"      # round 7: SON page8 fills the map's rectangle white under the base
KM_NA = 9.0              # mm: round 7: SON page8's north column beside the map (T3_KEY_NA), outside the frame
KM_NORTH_MM = 4.0        # mm: SON page8's north arrow height (na_h)
KM_HEAD = dict(size_mm=7.5 * 0.352778, colour="4A3F35", gap_mm=1.5)   # SON page8 heading: 7.5 pt bold INK, 1.5 mm gap
KM_PAD = 1.0             # mm: inner pad between the frame and the content (round 6 fitted map's pad)
KM_MARGIN = 0.02         # share of the content added on each side (round 6 fitted map's margin)
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
                names = (u"", u"")                            # the middle (km_keymap's id label goes on the other side)
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


def km_street_names(D, T, obstacles, vb=None, frame_mm=None, segs=(), Tinv=None, names=None, extra_names=None,
                    page=None, log=None):
    """round 6 (S1, G6-5), round 7 (G7-3: SON page8's names, KM_NAMES 6B645B 6 pt, else KM_NAMES_MIN 4 pt): the
    key map's names: the main streets (OpenStreetMap names by the names table's spelling, street_label), the names
    table's key-map places (keymap_places), then extra_names [(name, xy)]; each placed at its point or the nearest
    of six spots clear of obstacles (key-map mm boxes; the placed names are added to it), segs (key-map mm
    segments) and the frame (frame_mm = (w, h)); a name with no free place is set on its point at 4 pt and logged
    (the booklet moves it; never left out). T / Tinv: survey
    m <-> key-map mm; vb: the survey box the names are taken from. Returns dict(items (survey m text items), labels
    (dicts as km_keymap's), label_boxes)."""
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
        raise RuntimeError(u"km_keymap needs common/font_metrics.py (round 4 S1: fm_width) included before it is "
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
        ok = None
        for sz_ in [sz] + ([KM_NAMES_MIN] if sz > KM_NAMES_MIN + 1e-6 else []):   # round 7: 6 pt, else the 4 pt floor
            w = fmw(n, pt_of(sz_), bold=nm_st["bold"])
            for dx, dy in ((0.0, 0.0), (0.0, sz_ * 1.1), (0.0, -sz_ * 1.1), (w / 2.0 + 1.0, 0.0),
                           (-w / 2.0 - 1.0, 0.0), (0.0, sz_ * 2.2), (0.0, -sz_ * 2.2)):
                b = (x + dx - w / 2.0, y + dy - sz_ / 2.0, x + dx + w / 2.0, y + dy + sz_ / 2.0)
                if b[0] < pad_n or b[1] < pad_n or b[2] > w_mm - pad_n or b[3] > h_mm - pad_n:
                    continue
                if _km_box_hit(b, boxes, pad_n) or _km_seg_hit(b, segs, pad_n):
                    continue
                ok = b
                break
            if ok is not None:
                break
        if ok is None:                                    # 4 Nov (Aras 19:17 "not drawing ... is not a solution"):
            ok = (x - w / 2.0, y - sz_ / 2.0, x + w / 2.0, y + sz_ / 2.0)   # set on its point (4 pt), handed to the
            ok = (max(pad_n, min(ok[0], w_mm - pad_n - w)), max(pad_n, min(ok[1], h_mm - pad_n - sz_)))   # booklet,
            ok = (ok[0], ok[1], ok[0] + w, ok[1] + sz_)                     # which moves it off whatever it hits
            log.append(u"keymap %s: name '%s' set on its point (no free place here; the booklet places it)" % (pg, n))
        seen_n.add(n)
        boxes.append(ok)
        label_boxes.append((n, ok))
        placed[kind] += 1
        name_items.append(("text", n, Tinv(((ok[0] + ok[2]) / 2.0, (ok[1] + ok[3]) / 2.0)), sz_, nm_st["colour"],
                           nm_st["bold"], "MC"))
        labels.append(dict(string=n, kind=kind, anchor=(x, y), box=ok, size_mm=sz_, colour=nm_st["colour"],
                           bold=nm_st["bold"]))
    return dict(items=name_items, labels=labels, label_boxes=label_boxes)


def km_draw(km, X, fill_fn, line_fn, text_fn, water_opts=None, page=None, log=None, frame=True):
    """draws a km_keymap (PLAN §3 order: paper, base, WATER, structures, the study line, the red cuts, names, then the
    frame line, the north arrow and the heading, both outside the frame): X(q) key-map mm -> page point (e.g. lambda q: (x0 + q[0], y0 + q[1]), or a
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
        basemap_draw(km["frame_items"][1:] + km["north"] + list(km.get("heading_items") or ()), X, fill_fn, line_fn,
                     text_fn)
    return r


def km_items(km, page=None, item_id=None, priority=5):
    """round 5 (S2, G-R5-12; PLAN §4 item schema v1, Aras's addendum 1 Nov 22:37 point 3): the key map as items for
    the booklet: one "drawing" (layers of shapes in key-map mm, y up, origin lower-left; texts left out), one "text"
    item per label (names and cut labels, role "label", with its anchor in the drawing and the module's placement as
    hint_box), one "keymap" item (cut ids, looks, zooms, names, fill, rotation). Round 7 (G7-3): the drawing is the
    frame EXACTLY (w_mm x h_mm); the north arrow is its own "drawing" item "<id>.north" (role "north", outside=True,
    anchor = its lower-left in the key map's mm, outside the frame) and the heading a "text" item "<id>.head" (role
    "heading", anchor = its left middle above the frame); the "N" is a label of kind "north" anchored outside too. Shapes: {"type": "poly", "rings",
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
    basemap_draw(km["frame_items"][1:], lambda q: q, fill_fn, line_fn, None)
    nb = km.get("north_box") or (km["w_mm"], 0.0, km["w_mm"] + KM_NA, KM_NA)
    layer("north")                                       # round 7: the north arrow outside the frame, its own item
    basemap_draw([it for it in km["north"] if it[0] != "text"], lambda q: (q[0] - nb[0], q[1] - nb[1]), fill_fn,
                 line_fn, None)
    nlay = layers.pop()
    nlay["z"] = 0
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
    nw, nh = nb[2] - nb[0], nb[3] - nb[1]
    out.append(dict(id=u"%s.north" % did, page=pg, kind="drawing", role="north", priority=priority, group=did,
                    units="mm", axes=u"mm, origin lower-left, y up", size_mm=[round(nw, 2), round(nh, 2)],
                    extent=[0.0, 0.0, round(nw, 2), round(nh, 2)], scale_pref=None, scale_den=None, scale_bar=False,
                    north_deg=None, layers=[nlay], keep_areas=[[0.0, 0.0, round(nw, 2), round(nh, 2)]], anchors={},
                    anchor=dict(drawing=did, point=[round(nb[0], 2), round(nb[1], 2)]), outside=True))
    for t in km.get("heading_items") or ():               # round 7: the heading above the frame (SON page8)
        hb = km.get("heading_box")
        out.append(dict(id=u"%s.head" % did, page=pg, kind="text", role="heading", priority=priority, group=did,
                        string=t[1], label_kind="heading",
                        anchor=dict(drawing=did, point=[round(t[2][0], 2), round(t[2][1], 2)]),
                        hint_box=[round(v, 2) for v in hb] if hb else None, size_pt=round(t[3] / 0.352778, 2),
                        min_pt=4.0, bold=True, colour=t[4], short_forms=[], side_list_ok=False, justify=False))
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


def _km_frame_deg(P):
    """round 7 (S1, G7-3): the site frame's own axis as SON page8 drew it (selinus_board Frame: the direction of the
    frame polygon's longest edge, degrees counter-clockwise from east, turned into (-90, 90]); 0.0 without a frame"""
    if not P or len(P) < 2:
        return 0.0
    best, ang = -1.0, 0.0
    for i in range(len(P)):
        q0, q1 = P[i], P[(i + 1) % len(P)]
        L = _km_m.hypot(q1[0] - q0[0], q1[1] - q0[1])
        if L > best:
            best, ang = L, _km_m.atan2(q1[1] - q0[1], q1[0] - q0[0])
    while ang > _km_m.pi / 2:
        ang -= _km_m.pi
    while ang <= -_km_m.pi / 2:
        ang += _km_m.pi
    return _km_m.degrees(ang)


def km_keymap(page, cuts=None, w_mm=None, h_mm=None, heading=None, zooms=None, log=None, cut_ids=None, looks=None,
              north_side="right", extra_names=None, D=None, **legacy):
    """round 7 (S1, G7-3; PLAN §4.3): THE key map of every page = SON page8's "Where each street is cut" (_t3_sec_key,
    1d6f866 src/selinus_board/pages/p07_09_movement.py:1556-1727, on keymap v2 89097ee), callable with a page's cuts
    and its SON key-map frame. As SON page8: the map on the site frame's own axes (basemap_frame = site_alan, the
    longest edge along the page, no other turn); base mode "keymap" (green ground, houses by urban fabric, the stream
    blue, roads); the cuts in red R01 (km_cut_marks: end bars, triangles, end names or one name beside the middle,
    gaps between neighbours); main street and place names in 6B645B at SON's 6 pt, 4 pt where 6 pt finds no room
    (never smaller, never left out: a name with no free place is set on its point for the booklet); frame line INK2
    0.15 mm on white; the north arrow (4 mm, no plate) OUTSIDE the frame in a KM_NA column at the right (north_side
    "left": at the left); the heading 7.5 pt bold above the frame. Only fix (G7-3): the study area = closed rings
    (km_study_ring), never clipped: the map's content is every study ring plus the cuts and zooms, one uniform scale
    so that content fills w_mm x h_mm (pad KM_PAD, margin 2 %), the base cut to the frame.
    page: booklet page id ("p08"); cuts: a list of cut registry ids / zoom ids (strings, levels.py) and explicit cuts
    [(end1, end2, (name1, name2), look[, id])] survey m, mixed as needed (cut_ids: the same ids, round 6 name);
    w_mm x h_mm: the SON key-map frame of the page (PLAN §3, H4 §3) = the map's frame EXACTLY (one missing: from the
    content's aspect; both missing: 80 mm wide, WARNING); heading: the text above the frame (None = none); zooms {id:
    polygon survey m}: window frames in red; looks {id: +1/-1} for registry cuts; extra_names [(name, xy)].
    legacy options of round 6 (box, scale_den, rotate, names, fit, margin, pad_mm, legend_box, north ...) are ignored
    with a log line. Returns dict(base, study, cuts, names, items, box, scale_den, T, Tinv (survey m <-> key-map mm,
    origin lower-left, y up), drawn, missing, label_boxes, labels, w_mm, h_mm, study_rings, study_ring,
    study_closed, rotation_deg, rotation, north_deg, fill, frame, frame_items, north (key-map mm items, outside the
    frame), north_box, heading_items, heading_box, looks, zoom_ids, cut_ids, cuts_all, page). Logs
    `keymap <page> 1:<den> axes=<deg> frame=<w>x<h> fill=<f> cuts=<ids>` and km_log's `keymap <page> module ...`."""
    log = log if log is not None else KM_LOG
    pg = u"%s" % (page or u"")
    for k in sorted(legacy):
        log.append(u"keymap %s: option %s ignored (round 7: SON page8 look, frame = w x h)" % (pg, k))
    D = D if D is not None else basemap_load()
    ids, xcuts = list(cut_ids or ()), []
    for c in cuts or ():
        (ids if isinstance(c, str) else xcuts).append(c)
    if not ids and not xcuts and page is not None and callable(globals().get("level_registry_all")):
        ids = [e["id"] for e in level_registry_all(str(page))]
    cut_l, wins, drawn, missing, seen = [], [], [], [], set()
    win_fn = globals().get("level_window")
    for cid in ids:
        if zooms and cid in zooms:
            wins.append((cid, [tuple(p) for p in zooms[cid]]))
            drawn.append(cid)
            continue
        try:
            c = basemap_cut_ids([cid], looks)[0]
            ek = (round(c[0][0], 1), round(c[0][1], 1), round(c[1][0], 1), round(c[1][1], 1))
            if ek not in seen:                           # the crossings of one cut share one line
                seen.add(ek)
                cut_l.append((cid, c))
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
    for zid, w in (zooms or {}).items():                 # zooms passed in but not named in cuts: drawn too
        if zid not in drawn:
            wins.append((zid, [tuple(p) for p in w]))
            drawn.append(zid)
    for c in xcuts:                                      # explicit cuts (street cuts R1-R4 ...)
        cid = c[4] if len(c) > 4 and c[4] else c[2][0]
        cut_l.append((cid, (tuple(c[0]), tuple(c[1]), tuple(c[2]), c[3] if len(c) > 3 else 1)))
        drawn.append(cid)
    study = km_study_ring(D)
    cont = [p for R in study for p in R] + [p for _, c in cut_l for p in c[:2]] + [p for _, w in wins for p in w]
    if not cont:
        cont = list(basemap_extent(D) or [])
    if not cont:
        raise ValueError(u"key map %s: nothing to frame (no basemap data, no cuts)" % pg)
    # SON page8: the site frame's own axes (the p07 maps' View), north turned to match
    fr = basemap_frame(D) if D else None
    if not fr:
        log.append(u"WARNING %s keymap: no site frame in the basemap data: drawn north up" % pg)
    phi = -_km_frame_deg(fr)
    cph, sph = _km_m.cos(_km_m.radians(phi)), _km_m.sin(_km_m.radians(phi))
    bx0 = _bm_bb(cont)
    c0 = ((bx0[0] + bx0[2]) / 2.0, (bx0[1] + bx0[3]) / 2.0)

    def rot(p):
        dx, dy = p[0] - c0[0], p[1] - c0[1]
        return (dx * cph - dy * sph, dx * sph + dy * cph)

    def unrot(q):
        return (q[0] * cph + q[1] * sph + c0[0], -q[0] * sph + q[1] * cph + c0[1])
    rx0, ry0, rx1, ry1 = _bm_bb([rot(p) for p in cont])
    cw, ch = max(rx1 - rx0, 1.0), max(ry1 - ry0, 1.0)  # the content, m
    bw, bh = cw * (1.0 + 2.0 * KM_MARGIN), ch * (1.0 + 2.0 * KM_MARGIN)
    pad = KM_PAD
    if not w_mm and not h_mm:
        w_mm = 80.0
        log.append(u"WARNING %s keymap frame: no w x h given, drawn 80 mm wide" % pg)
    if not h_mm:
        h_mm = bh * (w_mm - 2.0 * pad) / bw + 2.0 * pad
    if not w_mm:
        w_mm = bw * (h_mm - 2.0 * pad) / bh + 2.0 * pad
    w_mm, h_mm = float(w_mm), float(h_mm)
    den = max(bw * 1000.0 / max(1.0, w_mm - 2.0 * pad), bh * 1000.0 / max(1.0, h_mm - 2.0 * pad))
    s = 1000.0 / den
    rcx, rcy = (rx0 + rx1) / 2.0, (ry0 + ry1) / 2.0

    def T(p):
        r = rot(p)
        return ((r[0] - rcx) * s + w_mm / 2.0, (r[1] - rcy) * s + h_mm / 2.0)

    def Tinv(q):
        return unrot(((q[0] - w_mm / 2.0) / s + rcx, (q[1] - h_mm / 2.0) / s + rcy))
    frame = [Tinv((0.0, 0.0)), Tinv((w_mm, 0.0)), Tinv((w_mm, h_mm)), Tinv((0.0, h_mm))]
    vb = _bm_bb(frame)
    base = basemap_items("keymap", box=vb, D=D, scale_den=den) if D else []
    base = ml_crop(base, frame) if base else []
    if D and D.get("format") != BASEMAP_FORMAT:
        log.append(u"FLAG keymap %s: basemap format %s has no urban fabric per house: one house tone until the site "
                   u"board writes format %d" % (pg, D.get("format"), BASEMAP_FORMAT))
    st_items = ml_study_items(study)
    cut_items = []
    marks = km_cut_marks([c for _, c in cut_l], den, frame=frame, T=T, box_mm=(w_mm, h_mm), page=pg, log=log,
                         per_cut=True)
    nm_fn = globals().get("level_name")
    for (cid, c), its in zip(cut_l, marks):
        try:
            name = nm_fn(cid) if callable(nm_fn) else cid
        except Exception:
            name = cid
        name = (u"%s" % name).split("-")[0]              # a crossing row (S5-2) is labelled by its cut (S5)
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
    # SON page8: the north arrow beside the map in its own column, turned to north on these axes, no plate
    a = _km_m.radians(phi)
    ncx = -0.5 * KM_NA if north_side == "left" else w_mm + 0.5 * KM_NA
    ncy = h_mm - 0.5 * KM_NA if h_mm >= KM_NA else 0.5 * h_mm
    half = 0.5 * (KM_NORTH_MM + 0.75 * max(2.12, 0.42 * KM_NORTH_MM))
    north_its = north_items(ncx + half * _km_m.sin(a), ncy - half * _km_m.cos(a), ang_rad=a, size_mm=KM_NORTH_MM,
                            colour=KM_HEAD["colour"])
    north_box = (ncx - 0.5 * KM_NA, ncy - 0.5 * KM_NA, ncx + 0.5 * KM_NA, ncy + 0.5 * KM_NA)
    heading_items, heading_box = [], None
    if heading:
        hs = KM_HEAD["size_mm"]
        yh = h_mm + KM_HEAD["gap_mm"] + 0.5 * hs
        heading_items = [("text", u"%s" % heading, (0.0, yh), hs, KM_HEAD["colour"], True, "ML")]
        hw = fmw(u"%s" % heading, pt_of(hs), bold=True) if callable(fmw) else 0.6 * hs * len(heading)
        heading_box = (0.0, yh - 0.5 * hs, hw, yh + 0.5 * hs)
    nr = km_street_names(D, T, boxes, vb=vb, frame_mm=(w_mm, h_mm), segs=segs, Tinv=Tinv, names=None,
                         extra_names=extra_names, page=pg, log=log)
    labels += nr["labels"]
    label_boxes += nr["label_boxes"]
    fill = min(1.0, (cw * s) * (ch * s) / max(1e-9, (w_mm - 2.0 * pad) * (h_mm - 2.0 * pad)))
    rot_out = round(phi, 1)
    log.append(u"keymap %s 1:%.0f axes=%.1f frame=%.1fx%.1f fill=%.2f cuts=%s"
               % (pg, den, rot_out, w_mm, h_mm, fill, u",".join(cid for cid, _ in cut_l) or u"-"))
    if log is not KM_LOG:
        KM_LOG.append(log[-1])
    frame_mm = [(0.0, 0.0), (w_mm, 0.0), (w_mm, h_mm), (0.0, h_mm)]
    frame_items = [("fill", [frame_mm], KM_PAPER, 1.0, True),
                   ("line", frame_mm + [frame_mm[0]], KM_FRAME["colour"], KM_FRAME["lw"], None, 1.0)]
    KM_STUDY_LOG[page] = (len(study), 1 if study else 0)
    km = dict(base=base, study=st_items, cuts=cut_items, names=nr["items"],
              items=list(base) + st_items + cut_items + nr["items"], box=(vb[0], vb[1], vb[2], vb[3]),
              scale_den=den, T=T, Tinv=Tinv, drawn=drawn, missing=missing, label_boxes=label_boxes, labels=labels,
              w_mm=w_mm, h_mm=h_mm, study_rings=study, study_ring=study, study_closed=1 if study else 0,
              rotation_deg=rot_out, rotation=rot_out, north_deg=rot_out, fill=fill, frame=frame,
              frame_items=frame_items, north=north_its, north_box=north_box, heading_items=heading_items,
              heading_box=heading_box, looks=dict(looks or {}), zoom_ids=[cid for cid, _ in wins],
              cut_ids=[cid for cid, _ in cut_l], page=page)
    km["cuts_all"] = list(km["cut_ids"])
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

