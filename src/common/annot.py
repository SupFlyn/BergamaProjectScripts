# ---- Plan annotations (round 6 S1, 4 Nov 2026; G6-4; PLAN.md §2.4, §2.8) -------------------------------------------
# The marks on every PLAN except key maps (Aras 4 Nov 09:32, refs/targets/r06_R01 poster: "much cleaner and keeps the
# drawings clean"): a section cut = a small filled triangle (2.0 mm) + its letter at each end, just outside the
# drawing's frame, with a short dashed stub (4 mm) on the cut's line and NO line across the plan; a level = a tiny
# crosshair 1.6 mm + "+0.00" at 5 pt (round 7); a view mark = a small open triangle + a short name; the north arrow plain and
# solid, no box. Replaces the red / grey cut lines across plans of rounds 3-5 (KM_CUT_PLAN, km_cut_items on plans).
# Included by common/keymap.py (every script that includes basemap.py has it). Page mm, y up. Every function returns
# its items (the basemap format: "fill" / "line" / "text") and, when X is given, draws them through it:
#   X = (fill_fn, line_fn, text_fn) as basemap_draw takes them, in page mm; T = survey m -> page mm (None: the
#   points are page mm already); frame = the drawing's frame (x0, y0, x1, y1) page mm.
#   an_cut(X, a_xy, b_xy, letter, frame, T, look=1, names=None)   the two end marks of one cut
#   an_level(X, xy, value_m, T)                                    one level mark (value in m, 2 decimals)
#   an_view(X, xy, dir_deg, name, frame, T)                        one view mark
#   an_north(X, xy, north_deg, size_mm=6)                          the north arrow
#   an_name(X, xy, text, T=None, page=None)                        a small name inside its area (round 7)
#   an_list(X, frame, rows, page=None)                             a list in the side column (round 7)
#   an_log(page, n_cuts=None, n_levels=None, log=None)             `annot <page> <kind> <n>` per kind
# ROUND 7 (S1, 5 Nov 2026; G7-2, PLAN §4.4; target refs/targets/r06_R01 poster): an_level is now a tiny crosshair +
# "+0.00" (was a quartered circle); an_name and an_list added (names small inside their area, lists in the side
# column); an_cut, an_view, an_north unchanged. Every plan except key maps and the masterplan page uses these only.
import math as _an_m

AN_CUT = dict(tri_mm=2.0, stub_mm=4.0, gap_mm=1.0, stub_lw=0.18, dash=(0.8, 0.5), text_mm=2.12)   # 6 pt letters
AN_LEVEL = dict(d_mm=1.6, lw=0.12, text_mm=1.764, gap_mm=0.6)          # round 7: crosshair 1.6 mm, "+0.00" 5 pt
AN_NAME = dict(text_mm=1.764, colour="2C2219")                         # round 7: names inside their area, 5 pt
AN_LIST = dict(text_mm=1.764, lead=1.35, key_gap_mm=1.0, colour="2C2219")   # round 7: side-column list, 5 pt
AN_VIEW = dict(tri_mm=2.0, lw=0.18, text_mm=1.764, gap_mm=0.8)
AN_COUNT = {}                          # page -> {"cuts": n, "levels": n, "views": n, "names": n, "lists": n}
AN_LOG = []


def _an_col(name):
    t = globals().get("HUE_ANN")
    return (t or {}).get(name) or {"cut": "8E8F8A", "ink": "2C2219"}[name]


def _an_out(items, X):
    if X:
        fill_fn, line_fn, text_fn = (tuple(X) + (None, None, None))[:3]
        basemap_draw(items, lambda p: p, fill_fn, line_fn, text_fn)
    return items


def _an_add(page, kind):
    if page is not None:
        c = AN_COUNT.setdefault(page, {"cuts": 0, "levels": 0, "views": 0, "names": 0, "lists": 0})
        c[kind] += 1


def _an_frame_hits(a, b, frame):
    """where the endless line through a, b crosses the frame rectangle: the two points (lowest t first) or None"""
    x0, y0, x1, y1 = frame
    ux, uy = b[0] - a[0], b[1] - a[1]
    ts = []
    for v, p0, d in ((x0, a[0], ux), (x1, a[0], ux)):
        if abs(d) > 1e-12:
            t = (v - p0) / d
            y = a[1] + uy * t
            if y0 - 1e-9 <= y <= y1 + 1e-9:
                ts.append(t)
    for v, p0, d in ((y0, a[1], uy), (y1, a[1], uy)):
        if abs(d) > 1e-12:
            t = (v - p0) / d
            x = a[0] + ux * t
            if x0 - 1e-9 <= x <= x1 + 1e-9:
                ts.append(t)
    if len(ts) < 2:
        return None
    t0, t1 = min(ts), max(ts)
    if t1 - t0 < 1e-9:
        return None
    return (a[0] + ux * t0, a[1] + uy * t0), (a[0] + ux * t1, a[1] + uy * t1)


def an_cut(X, a_xy, b_xy, letter, frame, T=None, look=1, names=None, page=None):
    """the G6-4 cut mark of one section: a_xy, b_xy = the cut's ends (end1 = the section's left end, look +1 = the
    viewer stands so end1 is on the left, as km_cut_items); letter "A" -> ends "A" and "A'" (names = (n1, n2) to give
    both). At each place where the cut's line leaves the frame: a dashed stub stub_mm long outward (gap_mm off the
    frame), at its outer end a filled triangle tri_mm pointing the way the section looks, the letter beyond it along
    the line. Nothing is drawn across the plan. Returns the items (page mm); a cut whose line misses the frame
    returns [] with a WARNING in AN_LOG."""
    a = T(a_xy) if T else tuple(a_xy)
    b = T(b_xy) if T else tuple(b_xy)
    hit = _an_frame_hits(a, b, frame)
    n1, n2 = names or (letter, letter + u"'")
    if hit is None:
        AN_LOG.append(u"WARNING %s annot cut %s: its line misses the drawing frame, no mark drawn" % (page or u"", n1))
        return []
    p1, p2 = hit
    if (p1[0] - a[0]) * (b[0] - a[0]) + (p1[1] - a[1]) * (b[1] - a[1]) > (p2[0] - a[0]) * (b[0] - a[0]) + \
            (p2[1] - a[1]) * (b[1] - a[1]):
        p1, p2 = p2, p1                                  # p1 on end1's side
    L = _an_m.hypot(p2[0] - p1[0], p2[1] - p1[1])
    ux, uy = (p2[0] - p1[0]) / L, (p2[1] - p1[1]) / L
    fx, fy = -uy * look, ux * look                       # the way the section looks (as km_cut_items)
    st, ink, grey = AN_CUT, _an_col("ink"), _an_col("cut")
    out = []
    for p, nm, sg in ((p1, n1, -1.0), (p2, n2, 1.0)):
        s0 = (p[0] + ux * sg * st["gap_mm"], p[1] + uy * sg * st["gap_mm"])
        s1 = (p[0] + ux * sg * (st["gap_mm"] + st["stub_mm"]), p[1] + uy * sg * (st["gap_mm"] + st["stub_mm"]))
        out.append(("line", [s0, s1], grey, st["stub_lw"], list(st["dash"]), 1.0))
        h = st["tri_mm"]
        tri = [(s1[0] + ux * h * 0.5, s1[1] + uy * h * 0.5), (s1[0] - ux * h * 0.5, s1[1] - uy * h * 0.5),
               (s1[0] + fx * h * 0.87, s1[1] + fy * h * 0.87)]
        out.append(("fill", [tri], ink, 1.0, True))
        off = h * 0.5 + 0.6 + st["text_mm"] * 0.45 * max(1, len(nm))
        out.append(("text", nm, (s1[0] + ux * sg * off, s1[1] + uy * sg * off), st["text_mm"], ink, True, "MC"))
    _an_add(page, "cuts")
    return _an_out(out, X)


def an_level(X, xy, value_m, T=None, page=None):
    """the G7-2 level mark (round 7; poster r06_R01): a tiny crosshair AN_LEVEL d_mm across at xy (two hairlines,
    no circle, no fill), its value "+0.00" (m, 2 decimals, signed) at 5 pt to the right. Returns the items (page
    mm)."""
    c = T(xy) if T else tuple(xy)
    st, ink = AN_LEVEL, _an_col("ink")
    r = st["d_mm"] / 2.0
    out = [("line", [(c[0] - r, c[1]), (c[0] + r, c[1])], ink, st["lw"], None, 1.0),
           ("line", [(c[0], c[1] - r), (c[0], c[1] + r)], ink, st["lw"], None, 1.0)]
    v = u"%+.2f" % float(value_m)
    out.append(("text", v, (c[0] + r + st["gap_mm"], c[1]), st["text_mm"], ink, False, "ML"))
    _an_add(page, "levels")
    return _an_out(out, X)


def an_view(X, xy, dir_deg, name, frame=None, T=None, page=None):
    """the G6-4 view mark: a small open triangle at xy pointing dir_deg (degrees, counter-clockwise from page east),
    the short name behind it (away from where it looks). A mark inside the frame is moved onto the frame's edge
    behind it, so the mark stays outside the drawing. Returns the items (page mm)."""
    c = T(xy) if T else tuple(xy)
    st, ink = AN_VIEW, _an_col("ink")
    ux, uy = _an_m.cos(_an_m.radians(dir_deg)), _an_m.sin(_an_m.radians(dir_deg))
    if frame and frame[0] < c[0] < frame[2] and frame[1] < c[1] < frame[3]:
        hit = _an_frame_hits(c, (c[0] + ux, c[1] + uy), frame)
        if hit:
            c = hit[0]                                   # the edge behind the mark
            c = (c[0] - ux * (st["gap_mm"] + st["tri_mm"]), c[1] - uy * (st["gap_mm"] + st["tri_mm"]))
    h = st["tri_mm"]
    tip = (c[0] + ux * h * 0.5, c[1] + uy * h * 0.5)
    bl = (c[0] - ux * h * 0.5 - uy * h * 0.5, c[1] - uy * h * 0.5 + ux * h * 0.5)
    br = (c[0] - ux * h * 0.5 + uy * h * 0.5, c[1] - uy * h * 0.5 - ux * h * 0.5)
    out = [("line", [tip, bl, br, tip], ink, st["lw"], None, 1.0)]
    off = h * 0.5 + st["gap_mm"] + st["text_mm"] * 0.3 * max(1, len(name))
    out.append(("text", name, (c[0] - ux * off, c[1] - uy * off), st["text_mm"], ink, False, "MC"))
    _an_add(page, "views")
    return _an_out(out, X)


def an_north(X, xy, north_deg, size_mm=6.0):
    """the G6-4 north arrow: keymap.north_items (a plain solid arrowhead on a shaft and "N", no plate or box) with its
    foot at xy, north turned north_deg (degrees, counter-clockwise from page-up). Placed by the caller outside the
    drawing. Returns the items (page mm)."""
    return _an_out(north_items(xy[0], xy[1], ang_rad=_an_m.radians(north_deg), size_mm=size_mm,
                               colour=_an_col("ink")), X)


def an_name(X, xy, text, T=None, page=None):
    """the G7-2 name (round 7): a small name (AN_NAME, 5 pt, regular) centred at xy inside its area (the caller
    gives a point inside the area it names). Returns the items (page mm); the booklet moves it if it hits."""
    c = T(xy) if T else tuple(xy)
    out = [("text", u"%s" % text, c, AN_NAME["text_mm"], AN_NAME["colour"], False, "MC")]
    _an_add(page, "names")
    return _an_out(out, X)


def an_list(X, frame, rows, page=None):
    """the G7-2 side-column list (round 7): rows top-down from the top-left of frame (x0, y0, x1, y1) page mm, y up;
    a row = "text" or (key, text): the key bold (a number or letter matching a mark on the plan), the text after it
    (AN_LIST, 5 pt, line pitch 1.35). Every row is drawn: rows below the frame's bottom stay (never dropped) with a
    WARNING in AN_LOG. Returns the items (page mm)."""
    st = AN_LIST
    x0, y0, x1, y1 = frame
    pitch = st["text_mm"] * st["lead"]
    fmw = globals().get("fm_width")
    out = []
    y = y1 - 0.5 * st["text_mm"]
    for r in rows:
        key, txt = (r[0], r[1]) if isinstance(r, (tuple, list)) else (None, r)
        x = x0
        if key is not None and u"%s" % key:
            k = u"%s" % key
            out.append(("text", k, (x, y), st["text_mm"], st["colour"], True, "ML"))
            kw = fmw(k, st["text_mm"] / 0.352778, bold=True) if callable(fmw) else 0.6 * st["text_mm"] * len(k)
            x += kw + st["key_gap_mm"]
        out.append(("text", u"%s" % txt, (x, y), st["text_mm"], st["colour"], False, "ML"))
        y -= pitch
    if y + pitch - 0.5 * st["text_mm"] < y0:
        AN_LOG.append(u"WARNING %s annot list: %d rows reach %.1f mm below the frame bottom (all drawn)"
                      % (page or u"", len(rows), y0 - (y + pitch - 0.5 * st["text_mm"])))
    _an_add(page, "lists")
    return _an_out(out, X)


def an_log(page, n_cuts=None, n_levels=None, log=None):
    """round 7: one line per kind, `annot <page> <kind> <n>` (cut, level, view, name, list); counts default to what
    the an_* functions drew for page this run (n_cuts / n_levels override). Returns the lines joined by newlines."""
    c = dict(AN_COUNT.get(page) or {})
    if n_cuts is not None:
        c["cuts"] = n_cuts
    if n_levels is not None:
        c["levels"] = n_levels
    lns = [u"annot %s %s %d" % (page, k[:-1], c.get(k, 0)) for k in ("cuts", "levels", "views", "names", "lists")]
    lg = log if log is not None else AN_LOG
    lg.extend(lns)
    return u"\n".join(lns)
