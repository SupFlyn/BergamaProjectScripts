# ---- M8 section framework (H-B 30 Oct 2026; R2-A 31 Oct: G14 grounding, triangle switch, D8 sky, back houses): scale, frame layers, standard elements, callouts, G6 assert ----------
# Needs section_parts.py, water.py (WaterLayers, shp_put), figures.py, plants.py, levels.py + data/LEVELS.py.
# Units: k = page mm per m of the drawing (1:500 printed at 100 % -> k = 2.0); levels in m a.s.l. through
# sf_y_of(); widths in m in, printed in cm (G6/G13). Shapes as in water.py. The cut registry is levels.py:
# level_registry(cid) / level_registry_all(page) (id, location, bed, avg_flow, q100, q500, walls, pages); no page
# types a level. Every element is drawn at true size; sizes the project has no source for are parameters, and the
# few defaults below are marked as drawing rules (never printed as data).

SF_SCALES = (200, 250, 500, 1000, 2000, 2500, 5000, 7500, 10000, 15000, 20000, 25000)    # D6 a: the only scales on any sheet (v15.2: + 7500, 15000, 25000 from the booklet list)
# round 4 (S2, D11, Aras 1 Nov 10:31): 1:100 is allowed for ZOOM INSETS ONLY (nothing on the list is >= 2 x 1:250)
SF_INSET_SCALES = (100,) + SF_SCALES
SF_INSET_MIN_ZOOM = 2.0             # G-R4-5.6: an inset is at least 2 x its parent's scale


def _sf_warn(page, kind, msg):
    """round 5 (S3, G-R5-1): a section-kit hit is a WARNING (common warn.py sink when included: orange + log line),
    never a stop; without warn.py the line goes to SF_LOG (sec_look_lines prints it)"""
    if globals().get("wn_warn"):
        return wn_warn(page, kind, msg)
    line = u"WARNING " + u" ".join(u"%s" % p_ for p_ in (page, kind) if p_) + u": %s" % msg
    SF_LOG.append(line)
    return line


def sf_scale_ok(den, inset=False):
    """den if it is a standard scale (D6 a; inset=True also allows 1:100, D11 zoom insets only). Round 5 (S3): an
    off-list scale is a WARNING and the next listed scale at or beyond it (smaller drawing, so it still fits) is
    returned; never a stop"""
    sc = SF_INSET_SCALES if inset else SF_SCALES
    d = int(round(float(den)))
    if d in sc:
        return d
    up = [v for v in sc if v >= d] or [sc[-1]]
    _sf_warn(None, "scale", u"1:%s is not on the scale list (D6%s): 1:%d used" % (den, ", D11 insets" if inset else "",
                                                                                 up[0]))
    return up[0]


def sf_k(den, print_k=1.0):
    """page mm per m at 1:den (print_k = the booklet's print reduction, 1.0 = drawn at print size)"""
    return 1000.0 / sf_scale_ok(den) * print_k


def sf_scale_pick(extent_m, box_mm, min_den=None):
    """the largest standard scale (smallest 1:den) at which extent_m (m) fits box_mm (page mm); min_den keeps it at
    or beyond a scale (e.g. 500 so sections of one page share 1:500). ValueError when even 1:20,000 is too big."""
    for den in SF_SCALES:
        if min_den and den < min_den:
            continue
        if extent_m * 1000.0 / den <= box_mm + 1e-6:
            return den
    raise ValueError("%.0f m does not fit %.0f mm at any standard scale" % (extent_m, box_mm))


def sf_scale_text(den):
    """"1:1,000" """
    return u"1:{:,}".format(sf_scale_ok(den))


def sf_y_of(datum, y0, k):
    """level (m a.s.l.) -> page y: datum level drawn at page y0"""
    return lambda lev: y0 + (float(lev) - datum) * k


def sf_cut(cid):
    """the cut registry entry (levels.py level_registry): the one place a section reads its levels"""
    return level_registry(cid)


# ---- frame layers: ground, background topography, atmosphere ------------------------------------------------------
def sf_ground(surface, k, bottom_y=None, material="earth", depth_m=1.5, into=None):
    """cut ground under a surface polyline (page mm, left to right) in its material hatch and the cut line, into the
    "ground" layer; bottom_y default = depth_m below the surface's lowest point (drawing rule)"""
    wl = into if into is not None else water_layers()
    b = bottom_y if bottom_y is not None else min(p[1] for p in surface) - depth_m * k
    wl.add("ground", sct_ground(list(surface), b, k, material))
    return wl


def sf_topo_back(profiles, bottom_y, into=None):
    """background topography: ground lines further from the cut (page mm, the farthest first), each a faded
    silhouette down to bottom_y with a fine edge, into "background" (pages take them from the survey)"""
    wl = into if into is not None else water_layers()
    n = len(profiles)
    for i, pr in enumerate(profiles):
        t = 0.75 - 0.35 * (i / float(max(1, n - 1)))   # far = paler
        ring = list(pr) + [(pr[-1][0], bottom_y), (pr[0][0], bottom_y)]
        wl.add("background", [("poly", ring, _sec_mix(SCT_SOIL["layers"][-1], "FFFFFF", t), None, 0.0),
                              ("line", list(pr), _sec_mix(SEC["ink2"], SEC["paper"], t), 0.12)])
    return wl


# ---- G14 grounding (R2-A 31 Oct 2026): every section item stands on its own ground; nothing floats ---------------
# gy anywhere below = a number (flat), a function x -> y, or a polyline [(x, y), ...] (page mm, y up).
SF_G14 = dict(seen=set(), moved=set(), max_mm=0.0, refused={})


def sf_gy(profile):
    """a ground function x -> y from a polyline [(x, y), ...] (page mm, any order; flat beyond its ends)"""
    import bisect as _b
    P = sorted((float(x), float(y)) for x, y in profile)
    xs = [p[0] for p in P]

    def f(x):
        if x <= xs[0]:
            return P[0][1]
        if x >= xs[-1]:
            return P[-1][1]
        i = _b.bisect_right(xs, x)
        (xa, ya), (xb, yb) = P[i - 1], P[i]
        return ya if xb - xa < 1e-12 else ya + (yb - ya) * (x - xa) / (xb - xa)
    f.sf_pts = P
    return f


def _sf_fn(gy):
    if callable(gy):
        return gy
    if isinstance(gy, (list, tuple)):
        return sf_gy(gy)
    return lambda _x, _v=float(gy): _v


def sf_ground_min(gy, xa, xb, n=8):
    """the lowest ground under [xa, xb] (page mm): G14 seats an item there, so no part of its base floats on a
    slope. Polylines: exact (their vertices inside); functions: n + 1 samples."""
    if xb < xa:
        xa, xb = xb, xa
    f = _sf_fn(gy)
    ys = [f(xa + (xb - xa) * i / float(n)) for i in range(n + 1)]
    ys += [y for x, y in (getattr(f, "sf_pts", None) or ()) if xa < x < xb]
    return min(ys)


def sf_seat_x(gy, x, half_w, tol=0.05):
    """G14: the y an item centred on x with a base half_w wide each side stands at = the lowest ground under its
    base; counted in the G14 log line (moved when it differs from the ground under its centre by more than tol mm)"""
    y = sf_ground_min(gy, x - abs(half_w), x + abs(half_w))
    key = (round(x, 2), round(y, 2))
    SF_G14["seen"].add(key)
    d = _sf_fn(gy)(x) - y
    if d > tol:
        SF_G14["moved"].add(key)
        SF_G14["max_mm"] = max(SF_G14["max_mm"], d)
    return y


def sf_ground_fn(gy, half_w):
    """gy as a function that already seats (sf_seat_x): pass it as the ground of fig_side, fig_activity,
    pla_section ... so every item they place stands on the lowest ground under its base"""
    return lambda x: sf_seat_x(gy, x, half_w)


# ---- people on the surface (round 5, S3, CHK-3 seat fix, G-R5-4.4 / PLAN §3 People) -------------------------------
# sf_seat_x seats on the LOWEST ground under a base: right for plants and houses (a trunk or wall foot may go into a
# slope), wrong for people (U11 "his feet is in the fucking floor", S09 feet sunk in a step). People stand on the
# HIGHER ground at their two feet: no foot is ever inside the ground or a step; on a step edge the person stands on
# the tread. Plants keep sf_seat_x.
SF_PEOPLE = dict(seen=0, grounded=0, tol_mm=0.15)


def sf_seat_feet(gy, x, half_w, n=6):
    """the y a person centred on x stands at: the HIGHER ground at the feet x - half_w and x + half_w (and between
    them, n samples, so a riser between the feet is stood on, never stepped into). half_w = the foot half span
    (figures.py FIG_FOOT_HALF_M x k). Counted in sf_people_line."""
    f = _sf_fn(gy)
    hw = abs(half_w)
    ys = [f(x - hw + 2.0 * hw * i / float(n)) for i in range(n + 1)]
    ys += [y for xx, y in (getattr(f, "sf_pts", None) or ()) if x - hw < xx < x + hw]
    y = max(ys)
    SF_PEOPLE["seen"] += 1
    SF_PEOPLE["grounded"] += 1
    return y


def sf_feet_fn(gy, half_w):
    """gy as a function that seats people by sf_seat_feet: pass it as the ground of fig_side / fig_activity /
    fig_place_zones (S4 figures.py) instead of sf_ground_fn"""
    return lambda x: sf_seat_feet(gy, x, half_w)


def sf_people_check(items, gy, half_w=None, page=None, tol=None):
    """G-R5-4.4 check by reasoning: items = [shapes of one person, ...] standing on ground gy; a person whose feet
    are more than tol mm above (floating) or below (sunk) the sf_seat_feet ground is a WARNING. Adds to the
    `people grounded n of n` count (sf_people_line). Returns the number grounded."""
    tol = SF_PEOPLE["tol_mm"] if tol is None else tol
    ok = 0
    for i, sh in enumerate(items or ()):
        b = _sf_base(sh)
        if b is None:
            continue
        hw = 0.5 * (b[2] - b[1]) if half_w is None else half_w
        g = max(_sf_fn(gy)(b[1]), _sf_fn(gy)(b[2]), _sf_fn(gy)(0.5 * (b[1] + b[2])))
        if half_w is not None:
            g = max(_sf_fn(gy)(0.5 * (b[1] + b[2]) - hw), _sf_fn(gy)(0.5 * (b[1] + b[2]) + hw), g)
        d = b[0] - g
        SF_PEOPLE["seen"] += 1
        if abs(d) <= tol:
            ok += 1
            SF_PEOPLE["grounded"] += 1
        else:
            _sf_warn(page, "people", u"person %d %s %.2f mm at x %.1f" % (i, u"floats" if d > 0 else u"sunk", abs(d),
                                                                         0.5 * (b[1] + b[2])))
    return ok


def sf_people_line():
    """the done-when log line `people grounded n of n` (G-R5-4.8); None when no person was seated or checked"""
    if not SF_PEOPLE["seen"]:
        return None
    return u"people grounded %d of %d" % (SF_PEOPLE["grounded"], SF_PEOPLE["seen"])


# ---- activity guards (round 5, S3; G-R5-4.4, PLAN §8 rule for all): fishing and wading only where water is drawn --
SF_DRY_MONTHS = (7, 8, 9)            # p10: the summer bed "dry or 3 cm Jul-Sep" -> no fishing, no wading Jul-Sep
SF_WADE_MAX_M = 0.50                 # PLAN §3 People: wading only in water <= 0.50 m (figures.py FIG_WADE_MAX_M)


def sf_activity_ok(kind, ground_y=None, water_y=None, k=None, month=None, strip=False, page=None, what=u"",
                   quiet=False):
    """(ok, reason): may a person do `kind` ("fish", "wade", anything else = True) at a spot whose ground is at page
    y ground_y with the drawn water surface at water_y (page y, None = no water drawn there), k mm per m, in month
    (1-12, None = no season shown)? Fishing: water drawn at the spot (the line ends in it) and not a dry month unless
    `strip` (the summer strip whose water is drawn). Wading: water drawn and its depth <= SF_WADE_MAX_M. A refusal is
    a WARNING (`<page> activity`) so the page draws a walker or watcher instead (P05.1). v15.2: quiet=True writes
    nothing (the caller logs the refusal itself)."""
    if kind not in ("fish", "fishing", "wade", "wading"):
        return True, u""
    why = None
    if water_y is None:
        why = u"no water drawn"
    elif month is not None and int(month) in SF_DRY_MONTHS and not strip:
        why = u"month %d: the bed is dry or 3 cm (p10)" % int(month)
    elif kind in ("wade", "wading") and ground_y is not None and k:
        dep = (water_y - ground_y) / float(k)
        if dep > SF_WADE_MAX_M + 1e-6:
            why = u"water %.2f m deep > %.2f m" % (dep, SF_WADE_MAX_M)
        elif dep <= 0.0:
            why = u"ground above the water"
    if why:
        if not quiet:
            _sf_warn(page, "activity", u"%s %s refused: %s" % (kind, what, why))
        return False, why
    return True, u""


# ---- trees at a middle level (round 5, S3, G-R5-4.5, U37 / U40 / U65) -------------------------------------------
# Where the drawing is not about plants or seasons, trees stand behind the people and lighter (depth layer 1, r3
# G15); where it is (p15, p18, p19-20) trees lead (layer 0). Never squeezed or thinned; shrubs in every section.
SF_TREE_LEAD_PAGES = ("p15", "p18", "p19", "p20")


def sf_tree_level(page):
    """dict(layer, lead) for the trees of a drawing on page (23-page id): layer 0 + lead True on the plant / season
    pages, else layer 1 (behind the people, paler: figures.py fig_fade / plants.py layer tones)"""
    lead = (u"%s" % page) in SF_TREE_LEAD_PAGES
    return dict(layer=0 if lead else 1, lead=lead)


def _sf_pts(s):
    t = s[0]
    if t in ("poly", "line"):
        return list(s[1])
    if t == "image":
        x0, y0, w, h = s[1:5]
        return [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
    return []


def _sf_move(s, dy):
    t = s[0]
    if t in ("poly", "line"):
        return (t, [(x, y + dy) for x, y in s[1]]) + tuple(s[2:])
    if t == "image":
        return tuple(s[:2]) + (s[2] + dy,) + tuple(s[3:])
    if t == "text":
        return tuple(s[:3]) + (s[3] + dy,) + tuple(s[4:])
    return s


def _sf_base(shapes, base_w=None):
    """(bottom y, x0, x1) of an item's base: images = their centre 40 % (trimmed cutouts: feet / trunk in the
    middle), drawings = the points within 4 % of the item's height above its bottom; base_w (mm) overrides"""
    pts = [p for s in shapes for p in _sf_pts(s)]
    if not pts:
        return None
    y0 = min(p[1] for p in pts)
    h = max(p[1] for p in pts) - y0
    if base_w is None:
        ims = [s for s in shapes if s[0] == "image"]
        if ims and len(ims) == len([s for s in shapes if _sf_pts(s)]):
            xa, xb = min(s[1] for s in ims), max(s[1] + s[3] for s in ims)
            c, hw = 0.5 * (xa + xb), 0.2 * (xb - xa)
            return y0, c - hw, c + hw
        low = [p[0] for p in pts if p[1] <= y0 + 0.04 * h + 1e-6]
        return y0, min(low), max(low)
    xs = [p[0] for p in pts]
    c = 0.5 * (min(xs) + max(xs))
    return y0, c - 0.5 * base_w, c + 0.5 * base_w


def sf_seat(shapes, gy, base_w=None, tol=0.05, sink=False):
    """G14 for any drawn item (cutout image, drawn figure, plant, stall, background house: one item's shapes): moves
    it down onto the lowest ground under its base (only down: a wading figure or a plinth set lower on purpose
    stays; sink=True also lifts an item buried below that ground). Counted in sf_g14_line. Returns the shapes."""
    b = _sf_base(shapes, base_w)
    if b is None:
        return shapes
    y0, xa, xb = b
    g = sf_ground_min(gy, xa, xb)
    key = (round(0.5 * (xa + xb), 2), round(g, 2))
    SF_G14["seen"].add(key)
    dy = g - y0
    if dy < -tol or (sink and dy > tol):
        SF_G14["moved"].add(key)
        SF_G14["max_mm"] = max(SF_G14["max_mm"], abs(dy))
        return [_sf_move(s, dy) for s in shapes]
    return shapes


def sf_seat_box(xa, xb, gy):
    """G14 for a house drawn by its base: the y its walls start at = the lowest ground of its own layer's profile
    under [xa, xb] (pass the profile of the house's depth layer, sf_back_profile, not the cut line)"""
    return sf_seat_x(gy, 0.5 * (xa + xb), 0.5 * abs(xb - xa))


def sf_back_profile(bases, x0, x1):
    """the ground line of one background depth layer through its items' own bases [(xa, xb, base_y)] (page mm:
    each house's ground from the survey): flat under each item, straight between neighbours, flat out to x0 / x1.
    Draw it with sf_topo_back so the houses visibly stand on it, and seat them with sf_seat_box on it."""
    pts = []
    for xa, xb, y in sorted(bases, key=lambda b: 0.5 * (b[0] + b[1])):
        pts += [(min(xa, xb), y), (max(xa, xb), y)]
    if not pts:
        return []
    pts.sort()
    return [(x0, pts[0][1])] + pts + [(x1, pts[-1][1])]


SF_BACK = dict(fill="E6E3DD", line="CFCBC2", roof="DAD6CE", lw=0.08)   # round 4 (S2, G-R4-5.3): background houses
SF_BACK_WIN_M = 30.0                # m behind the cut: farther houses get no windows (drawing rule, PLAN §4.7)


def sf_back_house(xa, xb, gy, h_m, k, layer=1, floors=None, roof="hip", fill=None, ink=None, d_m=None):
    """G14 + G7 + M8: a background house in elevation (not a rectangle): walls h_m (data height, m) high standing
    on the lowest ground of its layer's profile gy under it, a window per bay and storey (sill 0.90 m, head 2.10 m:
    the repo's bld_section_profile values; bay 3.0 m and window 1.20 m wide: drawing rules), a hipped roof at the
    repo's BLD_PITCH (M11 convention, not surveyed; "flat" = 0.60 m parapet), eaves 0.30 m; true size (an
    elevation: k is not reduced). Round 4 v2 (S2, G-R4-5.3): ONE pale tone at every depth (SF_BACK: no darker layer),
    windows only within SF_BACK_WIN_M behind the cut: d_m = the house's distance behind the cut (sf_back_buildings
    gives it); without d_m only depth layer 1 gets windows. fill / ink override the tones. Returns house shapes."""
    import math as _m
    wall = fill or SF_BACK["fill"]
    line = ink or SF_BACK["line"]
    rf = SF_BACK["roof"]
    win = (d_m <= SF_BACK_WIN_M) if d_m is not None else layer <= 1
    xa, xb = min(xa, xb), max(xa, xb)
    y0 = sf_seat_box(xa, xb, gy)
    yt = y0 + h_m * k
    sh = [("poly", [(xa, y0), (xb, y0), (xb, yt), (xa, yt)], wall, line, SF_BACK["lw"])]
    w_m = (xb - xa) / k
    nf = int(floors) if floors else max(1, int(round(h_m / globals().get("BLD_STOREY", 3.0))))
    st = h_m / float(nf)
    nb = max(1, int(w_m // 3.0))
    if win and st >= 2.4 and w_m >= 2.4:
        bw = (xb - xa) / nb
        for i in range(nf):
            for j in range(nb):
                cx = xa + (j + 0.5) * bw
                wy0, wy1 = y0 + (i * st + 0.9) * k, y0 + (i * st + 2.1) * k
                ww = min(1.2 * k, 0.6 * bw)
                sh.append(("poly", [(cx - ww / 2, wy0), (cx + ww / 2, wy0), (cx + ww / 2, wy1), (cx - ww / 2, wy1)],
                           line, None, 0.05))
    if roof == "flat":
        sh.append(("poly", [(xa, yt), (xb, yt), (xb, yt + 0.6 * k), (xa, yt + 0.6 * k)], wall, line, SF_BACK["lw"]))
    else:
        t = _m.tan(_m.radians(globals().get("BLD_PITCH", 30.0)))
        run = min(0.5 * (xb - xa) + 0.3 * k, 4.0 * k)
        rise = t * run
        e = 0.3 * k
        sh.append(("poly", [(xa - e, yt), (xb + e, yt), (xb + e - run, yt + rise), (xa - e + run, yt + rise)], rf, line,
                   SF_BACK["lw"]))
    return sh


SF_BACK_BAND = (8.0, 120.0)   # m behind a cut where background houses are taken from (drawing rule, R2-C)


def sf_back_buildings(cid, t0, t1, d0=None, d1=None, log=None, look=1):
    """R2-C (checklist 7, Aras 31 Oct 12:01 "no background houses"): the basemap buildings standing d0..d1 m behind
    the registry cut cid (the way the section looks: the normal (-u_y, u_x) of its ends, as the page key maps), each
    projected onto the cut: [(t_a, t_b m along the cut, h m, floors or None, d m behind)], farthest first, clipped to
    t0..t1. Height: the building's data height, else the repo's M11 convention floors x BLD_STOREY (buildings.py
    _bld_h, as every cut-through building). Draw with sf_back_house on the depth layer's ground (d < half the band:
    layer 1, else 2). look=-1: the drawing looks the other way (its first end on the right, as the p.12 W cuts and
    their key map, basemap_cut_ids looks=-1)."""
    import math as _m
    d0 = SF_BACK_BAND[0] if d0 is None else d0
    d1 = SF_BACK_BAND[1] if d1 is None else d1
    D = basemap_load(log=log) if globals().get("basemap_load") else None
    L = (D or {}).get("layers") or {}
    a, b = level_ends(cid)
    Lc = _m.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    u = ((b[0] - a[0]) / Lc, (b[1] - a[1]) / Lc)
    f = (-u[1] * look, u[0] * look)
    out = []
    for bl in L.get("buildings", []):
        h = _bld_h(bl) if globals().get("_bld_h") else float(bl.get("h") or 0.0)
        if h <= 0.0:
            continue
        P = [p_ for R_ in bl["rings"][:bl.get("np", len(bl["rings"]))] for p_ in R_]
        if len(P) < 3:
            continue
        ts = [(p_[0] - a[0]) * u[0] + (p_[1] - a[1]) * u[1] for p_ in P]
        ds = [(p_[0] - a[0]) * f[0] + (p_[1] - a[1]) * f[1] for p_ in P]
        dn = min(ds)
        if dn < d0 or dn > d1:
            continue
        ta, tb = max(t0, min(ts)), min(t1, max(ts))
        if tb - ta < 2.0:
            continue
        out.append((ta, tb, round(h, 2), int(bl.get("floors") or 0) or None, dn))
    out.sort(key=lambda r: -r[4])
    if log is not None:
        log.append(u"background houses {}: {} buildings {:.0f}-{:.0f} m behind the cut".format(cid, len(out), d0, d1))
    return out


def sf_assert_g14(items, gy, tol=0.2, strict=True):
    """G14 check by reasoning: items = [shapes of one item, ...] all on ground gy; an item whose base is more than
    tol mm above the lowest ground under it floats. strict: AssertionError listing them; else the messages."""
    bad = []
    for i, sh in enumerate(items):
        b = _sf_base(sh)
        if b is None:
            continue
        g = sf_ground_min(gy, b[1], b[2])
        if b[0] - g > tol:
            bad.append(u"G14: item %d floats %.2f mm over x %.1f-%.1f" % (i, b[0] - g, b[1], b[2]))
    if bad and strict:
        raise AssertionError(u"; ".join(bad))
    return bad


def sf_g14_line():
    """one log line: items seated by G14 and how many were moved onto the ground (None when nothing was seated)"""
    if not SF_G14["seen"]:
        return None
    s = u"G14 grounding: %d items seated, %d moved onto the ground (max %.1f mm)" % (
        len(SF_G14["seen"]), len(SF_G14["moved"]), SF_G14["max_mm"])
    if SF_G14["refused"]:
        s += u"; no people placed in: " + u", ".join(u"%s (%d)" % kv for kv in sorted(SF_G14["refused"].items()))
    return s


# ---- G14 / U22 meaningless triangles: switches (the cut-direction triangles of key maps are not touched) ---------
# walls: the small triangle that marks a surveyed wall (no height) on a section's ground (p4-5);
# aggregate: the open triangles of the concrete hatch (section_parts sct_hatch_fill; dots stay).
SF_TRI = dict(walls=True, aggregate=True)


def sf_triangles(walls=None, aggregate=None):
    """switch the section triangles on / off for what follows; returns the previous state (sf_triangles(**old)
    restores it). Pages switch them off (G14 round 2)."""
    old = dict(SF_TRI)
    if walls is not None:
        SF_TRI["walls"] = bool(walls)
    if aggregate is not None:
        SF_TRI["aggregate"] = bool(aggregate)
    return old


def sf_wall_mark(x, y, h, fill=None):
    """the surveyed-wall mark at (x, y): a triangle h high (its legend must say so); [] when SF_TRI walls is off"""
    if not SF_TRI["walls"]:
        return []
    return [("poly", [(x, y + h), (x - 0.6 * h, y), (x + 0.6 * h, y)], fill or SEC["ink2"], None, 0.1)]


# ---- sky v2 (round 4 S2, G-R4-5.3, U06 "background and sky looks weird"; PLAN §4.7) --------------------------------
# D8 answer (PLAN.md round 2): default a = every section and perspective. sky="d8" / True / "designed" in
# sf_atmosphere all draw this sky.
SF_SKY_DEFAULT = "designed"
# The sky sits back: the paper stays white; only the top SF_SKY["wash_h"] of the drawing's height above its lowest
# ground carries one very light vertical wash (wash_top at the top edge -> paper at the wash's foot); 2-3 OPEN cloud
# contours (a long low top line, no fill, no base line) in a pale cool grey; 2-4 birds in a pale grey. Nothing in the
# sky is darker than the muted base-map houses (map_layers / basemap BM_MUTED: bld EDEBE6, edge C9C5BC). Drawing rules,
# not data. Six fixed arrangements; a cut id keeps its arrangement and neighbouring cuts of a page never share one.
SF_SKY = dict(wash_h=0.30, bands=8, paper="FFFFFF", wash_top="F3F5F6", cloud="C9CFD3", cloud_lw=0.10, bird="C4CACE",
              cloud_w_max=45.0, cloud_h_max=3.0)
SF_SKY_VARIANTS = (                 # cloud centres (x as a fraction of the width, y as a fraction of the height above
    dict(x=(0.18, 0.66), y=(0.86, 0.74), w=(0.24, 0.20), birds=3),          # the lowest ground), widths (fraction of
    dict(x=(0.10, 0.45, 0.80), y=(0.78, 0.89, 0.72), w=(0.18, 0.22, 0.16), birds=2),   # the width), birds
    dict(x=(0.30, 0.80), y=(0.72, 0.86), w=(0.26, 0.18), birds=4),
    dict(x=(0.12, 0.40, 0.72), y=(0.84, 0.70, 0.80), w=(0.16, 0.20, 0.22), birds=3),
    dict(x=(0.55, 0.88), y=(0.82, 0.71), w=(0.28, 0.16), birds=2),
    dict(x=(0.14, 0.50), y=(0.70, 0.83), w=(0.22, 0.26), birds=3),
)
SF_SKY_USED = {}                    # cut id -> variant (a cut keeps its sky wherever it is drawn)
SF_SKY_RECENT = []                  # the last variants handed out: neighbours on a page never share one
SF_LOG = []                         # "sky variant <cid> v<n>", inset and level-mark lines (sec_look_lines)


def sf_sky_variant(cid=None):
    """the sky variant (0-5) of a section: a cut id keeps one variant for the run (hash of the id), moved on while it
    equals one of the last five handed out, so the sections of one page never share a sky; no cid -> the next in
    rotation. Logged once per cut as "sky variant <cid> v<n>"."""
    n = len(SF_SKY_VARIANTS)
    if cid is not None and cid in SF_SKY_USED:
        return SF_SKY_USED[cid]
    if cid is not None:
        v = sum((i + 1) * ord(ch) for i, ch in enumerate(u"%s" % cid)) % n
    else:
        v = (SF_SKY_RECENT[-1] + 1) % n if SF_SKY_RECENT else 0
    for _i in range(n):
        if v not in SF_SKY_RECENT[-(n - 1):]:
            break
        v = (v + 1) % n
    SF_SKY_RECENT.append(v)
    key = cid if cid is not None else u"section %d" % len(SF_SKY_RECENT)
    SF_SKY_USED[key] = v
    SF_LOG.append(u"sky variant %s v%d" % (key, v + 1))
    return v


def _sf_cloud(cx, cy, w, hb, rnd, col, lw):
    """sky v2: one OPEN cloud contour: a long low top line of 2-3 shallow swells, its ends easing down to the cloud's
    foot (no base line, no fill), and a short loose stroke under it"""
    import math as _m
    m = 2 + int(rnd() * 1.999)
    pts = []
    n = 40
    ph = [0.6 + 0.8 * rnd() for _i in range(m)]
    for j in range(n + 1):
        t = j / float(n)
        env = _m.sin(_m.pi * t) ** 0.6                       # ends ease down to the foot
        sw = sum(ph[i] * max(0.0, _m.sin(_m.pi * (t * m - i))) for i in range(m)) / max(ph)
        pts.append((cx - 0.5 * w + w * t, cy + hb * env * (0.45 + 0.55 * sw)))
    x0 = cx - 0.5 * w + w * (0.15 + 0.2 * rnd())
    return [("line", pts, col, lw), ("line", [(x0, cy - 0.35 * hb), (x0 + w * (0.35 + 0.2 * rnd()), cy - 0.35 * hb)],
                                     col, lw)]


def sf_sky(x0, x1, y0, y_top, seed=0, clouds=True, tone=None, cid=None, birds=True, variant=None):
    """sky v2 (round 4 S2, G-R4-5.3) behind a section or perspective: paper white, one very light vertical wash
    (SF_SKY wash_top -> paper) over the top SF_SKY["wash_h"] of y0 (page y, the lowest ground) .. y_top, 2-3 open
    cloud contours and 2-4 pale birds after one of SF_SKY_VARIANTS (variant, else sf_sky_variant(cid): no two
    sections of a page share one). tone: kept for old calls, no effect (the sky never takes a page colour). Draw it
    first (behind the ground). Returns shapes."""
    v = SF_SKY_VARIANTS[(variant if variant is not None else sf_sky_variant(cid)) % len(SF_SKY_VARIANTS)]
    H, W = y_top - y0, x1 - x0
    if W <= 1.0 or H <= 1.0:
        return []
    ys = y_top - SF_SKY["wash_h"] * H
    n = int(SF_SKY["bands"])
    sh = []
    for i in range(n):                                   # the wash: paper at its foot, wash_top at the top edge
        ya = ys + (y_top - ys) * i / float(n)
        yb = ys + (y_top - ys) * (i + 1) / float(n) + (0.05 if i < n - 1 else 0.0)
        sh.append(("poly", [(x0, ya), (x1, ya), (x1, yb), (x0, yb)],
                   _sec_mix(SF_SKY["paper"], SF_SKY["wash_top"], (i + 0.5) / n), None, 0.0))
    if clouds:
        rnd = _wat_rng(seed + 211)
        for fx, fy, fw in zip(v["x"], v["y"], v["w"]):
            w = min(fw * W, SF_SKY["cloud_w_max"])
            hb = min(0.08 * w, SF_SKY["cloud_h_max"], 0.10 * H)
            cx = min(max(x0 + fx * W, x0 + 0.55 * w), x1 - 0.55 * w)
            cy = min(y0 + fy * H, y_top - 1.2 * hb)
            sh += _sf_cloud(cx, cy, w, hb, rnd, SF_SKY["cloud"], SF_SKY["cloud_lw"])
    if birds and v["birds"]:
        sh += sf_birds(x0 + 0.08 * W, x1 - 0.08 * W, y0 + 0.55 * H, y0 + 0.92 * H, seed=seed, n=v["birds"])
    return sh


# ---- D3 birds (round 3 G15): a few architectural silhouettes, generic until research/fauna.md exists ------------
# Shapes in units of the bird's wingspan (drawing rules; page size SF_BIRD_MM, a symbol, not to scale): gliding,
# wings up, wings down; filled in a faded ink, opaque, like R05 / R07. Counted for the fauna FLAG (figures.py).
SF_BIRD_MM = (1.6, 3.0)             # page mm: wingspan range of the symbols
SF_BIRD_SHAPES = {
    "glide": [(-0.50, 0.04), (-0.22, 0.06), (-0.06, 0.02), (0.00, 0.05), (0.06, 0.02), (0.22, 0.06), (0.50, 0.04),
              (0.20, 0.00), (0.07, -0.03), (0.00, -0.07), (-0.07, -0.03), (-0.20, 0.00)],
    "up": [(-0.42, 0.30), (-0.20, 0.12), (-0.05, 0.02), (0.00, 0.05), (0.05, 0.02), (0.20, 0.12), (0.42, 0.30),
           (0.18, 0.02), (0.06, -0.04), (0.00, -0.09), (-0.06, -0.04), (-0.18, 0.02)],
    "down": [(-0.45, -0.18), (-0.22, -0.02), (-0.06, 0.04), (0.00, 0.07), (0.06, 0.04), (0.22, -0.02), (0.45, -0.18),
             (0.20, -0.08), (0.07, -0.03), (0.00, -0.06), (-0.07, -0.03), (-0.20, -0.08)],
}


def sf_birds(x0, x1, y0, y1, seed=0, n=None, ink=None, size=None):
    """2-5 generic bird silhouettes (D3) flying in the box x0..x1, y0..y1 (page mm): varied poses and sizes,
    loosely grouped (never a row); n fixes the count, size (mm) the wingspan. Fauna stays generic until
    research/fauna.md exists (figures.py fig_flag_lines logs "FLAG fauna pending research"). Returns shapes."""
    if x1 - x0 <= 1.0 or y1 - y0 <= 0.5:
        return []
    rnd = _wat_rng(seed + 77)
    ink = ink or SF_SKY["bird"]                          # round 4 sky v2: pale, never darker than the base houses
    cnt = n if n is not None else 2 + int(rnd() * 3.999)
    gx = x0 + (0.15 + 0.7 * rnd()) * (x1 - x0)                 # the flock's centre
    gy = y0 + (0.3 + 0.5 * rnd()) * (y1 - y0)
    keys = ("glide", "up", "down")
    sh = []
    for i in range(cnt):
        s = size or (SF_BIRD_MM[0] + (SF_BIRD_MM[1] - SF_BIRD_MM[0]) * rnd())
        bx = min(max(gx + (rnd() - 0.5) * 0.30 * (x1 - x0) + i * 0.9 * s * (1 if rnd() > 0.5 else -1), x0 + s), x1 - s)
        by = min(max(gy + (rnd() - 0.5) * 0.6 * (y1 - y0), y0), y1)
        tilt = (rnd() - 0.5) * 0.5
        shp = SF_BIRD_SHAPES[keys[(i + int(rnd() * 3)) % 3]]
        sh.append(("poly", [(bx + s * (px - tilt * py), by + s * (py + tilt * px)) for px, py in shp], ink, None, 0.0))
    if globals().get("FIG_FAUNA_DRAWN") is not None:
        FIG_FAUNA_DRAWN[0] += cnt
    return sh


def sec_look_lines():
    """the round 3 section-look log lines for a page's log: sky variants handed out, the plants line (no alpha, bare
    species), the fauna FLAG while research/fauna.md is missing"""
    out = []
    if SF_LOG:
        out.append(u"; ".join(SF_LOG))
    for ln in (globals().get("PLA_LOG") or ()):
        if ln.startswith(u"plants: no alpha"):
            out.append(ln)
    f = globals().get("pla_log_lines")      # round 4 (S3): willow v2 drawn, plants by species / season, colour FLAG
    if f:
        out += f()
    f = globals().get("fig_flag_lines")
    if f:
        out += f()
    out += sf_kit_lines()
    return out


def sf_kit_lines():
    """round 5 (S3) section kit v2 done-when lines (G-R5-4.8): materials solid, `widths 0`, `people grounded n of
    n`, the bridge lines (bridges.py), once per run (the counters are not reset: the last page's call has them all)"""
    out = []
    sl = globals().get("SCT_LOG")
    if sl:
        out.append(u"section materials solid: %d cut rings flat colour, %d with inset joints, hatches 0"
                   % (sl["solid"], sl["detail"]))
    out.append(sf_widths_line())
    pl = sf_people_line()
    if pl:
        out.append(pl)
    f = globals().get("br_log_lines")
    if f:
        out += f()
    return out


def sf_atmosphere(x0, x1, gy, y_top, k, seed=0, sky=True, trees=True, birds=True, mix=None, t0=0.45, t1=0.95,
                  density=0.7, style="b", into=None, back_ground=None, groups=True, water=None, cid=None, month=None):
    """the atmosphere behind a section (p17; R16, R19 idea): a sky from the ground line gy (number, function of x
    or polyline) up to y_top, faded depth trees in D9 layers 2 and 1 (band t0..t1), a few birds. Into "atmosphere"
    (sky, birds) and "background" (trees). sky: "designed" (D8: sf_sky, gradient + soft clouds), "d8" (the D8 answer,
    SF_SKY_DEFAULT), True (the older calm three bands), False (none). R2-A 31 Oct (G14, G9): back_ground = {layer:
    profile} gives each depth layer its own ground (drawn with sf_topo_back, farthest first) and the trees stand on
    it, else on gy; every tree is seated on the lowest ground under it (sf_seat_x); groups=True plants mixed groups
    (plants.py pla_group_section) instead of the single scatter; water (page y or function of x): no tree where the
    ground of its layer lies under it. Round 3 (G15): cid = the cut id that picks the sky variant (sf_sky_variant);
    birds = sf_birds (D3); month (1-12) draws the depth trees in that month's colours / bare (plants.py pla_colour).
    Returns the WaterLayers."""
    wl = into if into is not None else water_layers()
    gf = _sf_fn(gy)
    g0 = min(gf(x0), gf(x1), sf_ground_min(gf, x0, x1, 24))
    if sky is True or sky == "d8":                       # round 4 (S2): every sky is sky v2 (the old bands retired)
        sky = SF_SKY_DEFAULT
    if sky == "designed":
        wl.add("atmosphere", sf_sky(x0, x1, g0, y_top, seed=seed, cid=cid, birds=False))
    if back_ground:
        bot = min(min(p[1] for p in pr) for pr in back_ground.values()) - 1.0
        lays = sorted(back_ground, reverse=True)
        sf_topo_back([back_ground[l_] for l_ in lays], bot, into=wl)
    if trees:
        for layer in (2, 1):
            g_ = sf_gy(back_ground[layer]) if back_ground and layer in back_ground else gf
            if groups:
                sh, _pl, _gr = pla_group_section(x0, x1, g_, k, t0=t0, t1=t1, mix=mix, seed=seed + 31 * layer,
                                            layers=(layer,), style=style, density=density, hires=False, detail=False,
                                            water=water, month=month)
            else:
                sh, _pl = pla_scatter_section(x0, x1, sf_ground_fn(g_, 0.4 * k), k, t0=t0, t1=t1, mix=mix,
                                              seed=seed + 31 * layer, layer=layer, style=style, density=density,
                                              hires=False, detail=False, month=month)
            wl.add("background", sh)
    if birds:
        wl.add("atmosphere", sf_birds(x0, x1, g0 + 0.55 * (y_top - g0), g0 + 0.95 * (y_top - g0), seed=seed))
    return wl


# ---- numbered callouts (R07, R19 idea) ------------------------------------------------------------------------------
class SfCallouts(object):
    """numbered callouts of one drawing: add(x, y, text) -> its number; marks(size) = the numbered circles; key(x, y,
    size) = the numbered list beside the drawing (G1: every number explained)"""

    def __init__(self, start=1):
        self.items, self.n0 = [], start

    def add(self, x, y, text):
        for n, _x, _y, t in self.items:                # the same element twice keeps one number
            if t == text:
                self.items.append((n, x, y, t))
                return n
        n = self.n0 + len(set(t for _n, _x, _y, t in self.items))
        self.items.append((n, x, y, text))
        return n

    def marks(self, size=1.8, ink=None, fill="FFFFFF"):
        ink = ink or SEC["ink"]
        sh = []
        mk = globals().get("mk_marker")                  # round 4 (S2, G-R4-7): the one marker function (S1 marker.py)
        for n, x, y, _t in self.items:
            if callable(mk):
                sh += list(mk(x, y, u"%d" % n, ink, size_pt=max(7.0, size / 0.3528), style="ring")[0])
                continue
            r = 0.75 * size
            sh += [("poly", sec_ellipse(x, y, r, r, 20), fill, ink, 0.15),
                   ("text", u"%d" % n, x, y - 0.36 * size, 0.85 * size, ink, True, "C")]
        return sh

    def key(self, x, y, size=1.8, ink=None, gap=None):
        """the numbered list: one row per number from (x, y) down (y up), gap apart; ink = the caller's colour (else
        SEC ink). Round 4 closing (G-R4-7): each number is the shared marker (marker.py mk_marker, style "ring" as
        .marks: the glyph centred on its ink box, at least 7 pt), its disc centred 0.4 x size above the row's
        baseline and at least its radius in from x; the row's words start 2 x size in (further only when the disc
        is wider). Returns house shapes, as before."""
        ink = ink or SEC["ink"]
        gap = gap or 1.5 * size
        pt = max(7.0, size / 0.3528)
        seen, sh, yy = set(), [], y
        for n, _x, _y, t in sorted(self.items):
            if n in seen:
                continue
            seen.add(n)
            cy = yy - 0.4 * size
            shp, _box, r = mk_marker(x + 0.75 * size, cy, u"%d" % n, ink, size_pt=pt, style="ring")
            if r > 0.75 * size:                          # a wider disc (two digits) moves in to keep x its left edge
                shp, _box, r = mk_marker(x + r, cy, u"%d" % n, ink, size_pt=pt, style="ring")
            sh += list(shp)
            sh.append(("text", t, max(x + 2.0 * size, x + 2.0 * r + 0.4 * size), yy - 0.76 * size, size, ink, False,
                       "L"))
            yy -= gap
        return sh


def sf_width_label(x0, x1, y, width_m, size=2.47, ink=None, unit=True):
    """RETIRED in round 5 (S3, G-R5-4.6, U49 "remove the horizontal dimensions all together ... in all of the
    drawings"): draws nothing, returns []; every call is counted (sf_widths_line). Kept so old calls still run."""
    SF_WIDTHS["calls"] += 1
    return []


# ---- no widths anywhere (round 5, S3, G-R5-4.6): every text a section or its list prints goes through
# sf_strip_widths (item_export Ix.text calls it for every exported text, so page code needs no change): a width in
# cm ("Footway 456 cm", "bed 3,260 cm", "Bike · 300 cm"), a "W x H cm/m" size ("8 x 40 cm seats", "olives 500 x 700
# cm", "rows 7 x 5 m") and a lone "N cm" go with the separator before them; names, heights in m with 2 decimals
# ("+43.71", "2.50 m") and scale texts stay. A value in cm is never a height in this project (units rule: heights in m,
# 2 decimals), so every cm value is a width. Log `widths 0` (none left) or the strips counted.
SF_WIDTHS = dict(calls=0, stripped=0, examples=[])
_SF_W_RE = None


def _sf_w_re():
    global _SF_W_RE
    if _SF_W_RE is None:
        import re as _re
        num = r"\d[\d,.]*"
        _SF_W_RE = (
            # "8 x 40 cm seats", "500 × 700 cm", "rows 7 × 5 m", "400 x 30 cm" (a size pair: always a width)
            _re.compile(r"\s*(?:[·,:;\-–—]\s*)?(?:\(\s*)?" + num + r"\s*(?:cm|m)?\s*[x×]\s*" + num +
                        r"\s*(?:cm|m)\b\)?", _re.U),
            # "1,580 cm", "· 300 cm", "(456 cm)"
            _re.compile(r"\s*(?:[·,:;\-–—]\s*)?(?:\(\s*)?" + num + r"\s*cm\b\)?", _re.U),
        )
    return _SF_W_RE


def sf_strip_widths(s, page=None):
    """s without any horizontal dimension (see the notes above); counted in SF_WIDTHS. Non-strings pass through."""
    if not isinstance(s, str) or (u"cm" not in s and u"×" not in s and u" x " not in s):
        return s
    t = s
    for rx in _sf_w_re():
        t = rx.sub(u"", t)
    if t != s:
        import re as _re
        t = _re.sub(r"\s{2,}", u" ", t)
        t = _re.sub(r"\s*[·,:;\-–—]\s*$", u"", t).strip()
        t = _re.sub(r"^\s*[·,:;\-–—]\s*", u"", t)
        SF_WIDTHS["stripped"] += 1
        if len(SF_WIDTHS["examples"]) < 6:
            SF_WIDTHS["examples"].append(u"%s -> %s" % (s, t or u"(nothing)"))
    return t


def sf_widths_line():
    """the done-when log line: `widths 0` when no width was drawn or printed; else what was stripped (they are gone
    from the page; the line lets the page session find and delete the source strings)"""
    n = SF_WIDTHS["stripped"] + SF_WIDTHS["calls"]
    if not n:
        return u"widths 0"
    return u"widths 0 (removed this run: %d width texts, %d width chains; e.g. %s)" % (
        SF_WIDTHS["stripped"], SF_WIDTHS["calls"], u"; ".join(SF_WIDTHS["examples"]))


# ---- level markers beside the section (round 5, S3, G-R5-4.3, Aras's sketch refs/U04; replaces G-R4-5.4) ---------
# PLAN §3 "Level marker": a short horizontal mark beside the section, SF_LEVEL["gap"] >= 3 mm clear of the drawing's
# outer edge: long dash 3.5 mm, gap 0.8, short dash 0.8, gap 0.8, dash 3.1 mm ending under an open downward triangle
# (2.2 mm wide, 1.4 mm high, apex on the line at its outer end); the value "+43.71 Q100" (m, 2 decimals, 4.5 pt) beyond
# the triangle; stacked markers keep their lines at their levels and spread their labels >= 0.8 mm apart (a hairline
# joins a moved label). In the round 5 booklet the markers are drawn by the composer (pl_levels): a content script
# exports them with sf_level_items (Ix.levels) and draws nothing; sf_level_marks stays for pages still drawing
# themselves and draws the same marker.
SF_LEVEL = dict(gap=3.0, dashes=(3.5, 0.8, 0.8, 0.8, 3.1), tri_w=2.2, tri_h=1.4, size=4.5 * 25.4 / 72.0, lw=0.15,
                clear=0.8, label_gap=0.6)
SF_LEVEL_NAMES = dict(q500=u"Q500", q100=u"Q100", avg=u"mean flow", mean=u"mean flow", bed=u"bed")


def _sf_level_rows(levels, y_of, y0, y1, page):
    Pa = _wat_pal_sec() if globals().get("_wat_pal_sec") else {}
    rows = []
    for lv in levels or ():
        key, val = lv[0], float(lv[1])
        y = lv[2] if len(lv) > 2 and lv[2] is not None else (y_of(val) if y_of else None)
        if y is None:
            _sf_warn(page, "levels", u"level %r has no page y and no y_of: not marked" % (key,))
            continue
        if y0 is not None and (y < y0 - 1e-6 or y > y1 + 1e-6):
            _sf_warn(page, "levels", u"%s %+.2f lies outside the drawing's height: not marked" % (key, val))
            continue
        rows.append((y, key, val, Pa.get(key) or (SCT_WATER["surface"] if "SCT_WATER" in globals() else SEC["ink"])))
    rows.sort(key=lambda r: -r[0])
    return rows


def sf_level_marks(frame_box, levels, side="R", y_of=None, size=None, cols=None, page=None):
    """the level markers of one section beside its drawing (G-R5-4.3, U04). frame_box = (x0, y0, x1, y1) page mm
    (y up) of the drawing's outer edge; levels = [(key or name, level m[, page y])] (water_section's
    wl.anchors["levels"]); keys q500 / q100 / avg / mean / bed are named by SF_LEVEL_NAMES, any other key prints as
    given. side "R" (default) or "L" (mirrored). cols = {key: hex} overrides the water colours. Logs
    "levels <page> gap ok ..." in SF_LOG. Returns shapes (lines, open triangles, value texts)."""
    x0, y0, x1, y1 = frame_box
    size = size or SF_LEVEL["size"]
    rows = _sf_level_rows(levels, y_of, y0, y1, page)
    sgn = 1.0 if side == "R" else -1.0
    xs = (x1 if side == "R" else x0) + sgn * SF_LEVEL["gap"]           # the line starts gap mm off the drawing
    L = sum(SF_LEVEL["dashes"])
    tw, th, lw = SF_LEVEL["tri_w"], SF_LEVEL["tri_h"], SF_LEVEL["lw"]
    sh = []
    xt = xs + sgn * (L + 0.5 * tw + SF_LEVEL["label_gap"])           # labels start beyond the triangle
    last = None
    moved = 0
    for y, key, val, col in rows:
        col = (cols or {}).get(key) or col
        pos = 0.0
        for i, d in enumerate(SF_LEVEL["dashes"]):                    # dash, gap, dash, gap, dash
            if i % 2 == 0:
                sh.append(("line", [(xs + sgn * pos, y), (xs + sgn * (pos + d), y)], col, lw))
            pos += d
        ax = xs + sgn * L                                              # apex on the line at its outer end
        sh.append(("poly", [(ax, y), (ax - 0.5 * tw, y + th), (ax + 0.5 * tw, y + th)], None, col, lw))
        ty = y - 0.35 * size                                           # baseline: text centred on the line
        if last is not None and ty > last - (size + SF_LEVEL["clear"]):
            ty = last - (size + SF_LEVEL["clear"])
            moved += 1
            sh.append(("line", [(ax + sgn * 0.5 * tw, y), (xt - sgn * 0.2, ty + 0.35 * size)], col, 0.08))
        nm = SF_LEVEL_NAMES.get(key, u"%s" % key)
        sh.append(("text", u"%+.2f %s" % (val, nm), xt, ty, size, col, False, "L" if side == "R" else "R"))
        last = ty
    SF_LOG.append(u"levels %s gap ok: %d markers %.1f mm off the drawing (%s), %d labels spread" % (
        page or u"", len(rows), SF_LEVEL["gap"], side, moved))
    return sh


def sf_level_items(ix, page, drawing, levels, side="R"):
    """round 5 (G-R5-12): the level markers as an export item: ix.levels(page, drawing id, [(name, z m)], side); the
    booklet draws them (pl_levels, same U04 marker). levels as for sf_level_marks (keys named by SF_LEVEL_NAMES).
    Logs "levels <page> gap ok (exported n)". Returns the item id."""
    rows = []
    for lv in levels or ():
        rows.append((SF_LEVEL_NAMES.get(lv[0], u"%s" % lv[0]), float(lv[1])))
    SF_LOG.append(u"levels %s gap ok: %d markers exported to the booklet" % (page or u"", len(rows)))
    did = drawing["id"] if isinstance(drawing, dict) else drawing
    return ix.levels(page, did, rows, side=side)


# ---- standard elements (true size; page mm, y up; side +1 = builds to the right of x) ------------------------------
SF_LANE = dict(bike="C4AE9E", walk=SCT["concrete"], road="9C9890", gravel=SCT["gravel"], timber=SCT["timber"])
# round 5 (S3, PLAN §3): walk / gravel / timber = the section kit's solid material colours (section_parts SCT)
SF_RAIL_H = 1.10        # m, the repo's railing height (figures.py railing rail_h)
SF_SEAT_H = 0.45        # m, the repo's seat height (figures.py sit_step seat_h)


def sf_lane(x, y, width_m, k, kind="walk", side=1, t_m=0.15, callouts=None, label=None):
    """a lane on the ground at (x, y): bike (with its centre and edge lines), walk (paving joints), road, gravel or
    timber; t_m = its build-up drawn under the surface (drawing rule). label + callouts: a numbered callout.
    Returns shapes (surface at y)."""
    w, t = width_m * k * side, t_m * k
    xa, xb = min(x, x + w), max(x, x + w)
    sh = [("poly", [(xa, y - t), (xb, y - t), (xb, y), (xa, y)], SF_LANE.get(kind, SCT["concrete"]), SCT["cut"], 0.2)]
    if kind == "walk" and k >= SCT_DETAIL_K:          # round 5 (S3, G-R5-4.1): joints only at inset detail scales
        j = max(0.6 * k, 1.0)
        xx = xa + j
        while xx < xb - 0.2:
            sh.append(("line", [(xx, y - t), (xx, y)], SCT["line"], 0.06))
            xx += j
    elif kind == "bike":
        sh.append(("line", [(xa + 0.1 * k, y + 0.02), (xb - 0.1 * k, y + 0.02)], "FFFFFF", 0.12, [0.8, 0.6]))
    elif kind == "gravel":
        sh = sct_hatch_fill([(xa, y - t), (xb, y - t), (xb, y), (xa, y)], "gravel", k, SCT["cut"], 0.2)
    elif kind == "timber" and k >= SCT_DETAIL_K:
        xx = xa + 0.14 * k
        while xx < xb - 0.05:
            sh.append(("line", [(xx, y - t), (xx, y)], SCT["line"], 0.05))
            xx += 0.14 * k
    if callouts is not None and label:
        callouts.add((xa + xb) / 2.0, y + 1.2, label)
    return sh


def sf_stairs(x, y, n, rise_m, tread_m, k, side=1, material="concrete", t_m=0.15, rail=False):
    """a flight of n steps (rise_m, tread_m each; give them from the design) climbing from (x, y) toward side.
    Returns (shapes, (x_end, y_end))."""
    sh, cx, cy = [], x, y
    for _i in range(n):
        x2, y2 = cx + side * tread_m * k, cy + rise_m * k
        ring = [(cx, cy - t_m * k), (cx, y2), (x2, y2), (x2, cy - t_m * k)]
        sh += sct_hatch_fill(ring, material, k, SCT["cut"], 0.2)
        cx, cy = x2, y2
    if rail:
        sh.append(("line", [(x, y + SF_RAIL_H * k), (cx, cy + SF_RAIL_H * k)], SCT["cut"], 0.2))
        for px, py in ((x, y), (cx, cy)):
            sh.append(("line", [(px, py), (px, py + SF_RAIL_H * k)], SCT["cut"], 0.2))
    return sh, (cx, cy)


def sf_ramp(x, y, run_m, rise_m, k, side=1, t_m=0.20, material="concrete", rail=True):
    """a ramp slab from (x, y) rising rise_m over run_m toward side (slope = the design's; t_m drawing rule).
    Returns (shapes, (x_end, y_end), slope %)."""
    x2, y2 = x + side * run_m * k, y + rise_m * k
    ring = [(x, y - t_m * k), (x, y), (x2, y2), (x2, y2 - t_m * k)]
    sh = sct_hatch_fill(ring, material, k, SCT["cut"], 0.2)
    if rail:
        sh.append(("line", [(x, y + SF_RAIL_H * k), (x2, y2 + SF_RAIL_H * k)], SCT["cut"], 0.15))
    return sh, (x2, y2), (100.0 * rise_m / run_m if run_m else 0.0)


def sf_terrace(x, y, width_m, k, side=1, t_m=0.25, material="timber", rail=True):
    """a level viewing terrace / deck at (x, y) width_m wide toward side, slab t_m (drawing rule), railing SF_RAIL_H
    at its outer edge. Returns shapes."""
    x2 = x + side * width_m * k
    xa, xb = min(x, x2), max(x, x2)
    ring = [(xa, y - t_m * k), (xb, y - t_m * k), (xb, y), (xa, y)]
    sh = (sct_hatch_fill(ring, "concrete", k, SCT["cut"], 0.2) if material == "concrete" else
          [("poly", ring, SF_LANE["timber"], SCT["cut"], 0.2)])
    if rail:
        sh += sct_bank("railing", x2, y, y, side, k, h_m=SF_RAIL_H)[0]
    return sh


def sf_bridge(x0, x1, deck_y, k, deck_t_m=0.50, rail=True, material="concrete"):
    """a bridge deck over the stream from x0 to x1 (top at deck_y), deck_t_m thick (drawing rule unless the design
    gives one), railings at both edges; draw it in the "structures" layer (over the water). Returns shapes."""
    xa, xb = min(x0, x1), max(x0, x1)
    ring = [(xa, deck_y - deck_t_m * k), (xb, deck_y - deck_t_m * k), (xb, deck_y), (xa, deck_y)]
    sh = sct_hatch_fill(ring, material, k, SCT["cut"], 0.3)
    if rail:
        for xr in (xa + 0.1 * k, xb - 0.1 * k):
            sh.append(("line", [(xr, deck_y), (xr, deck_y + SF_RAIL_H * k)], SCT["cut"], 0.2))
        sh.append(("line", [(xa + 0.1 * k, deck_y + SF_RAIL_H * k), (xb - 0.1 * k, deck_y + SF_RAIL_H * k)], SCT["cut"],
                   0.2))
    return sh


def sf_stepping_stones(x0, x1, bed_y, wl_y, k, stone_w_m=0.60, gap_m=0.40, above_m=0.15, seed=0):
    """stepping stones across the water from x0 to x1, standing on the bed and above_m above the average-flow water
    wl_y; widths and gaps vary (no even rhythm). Sizes are drawing rules (a typical stride), not data. Returns
    shapes ("structures": over the water)."""
    rnd = _wat_rng(seed + 9)
    sh, x = [], x0 + 0.5 * gap_m * k
    top = wl_y + above_m * k
    while x + stone_w_m * 0.85 * k <= x1:
        w = stone_w_m * (0.85 + 0.3 * rnd()) * k
        r = 0.12 * w
        ring = [(x, bed_y), (x + w, bed_y), (x + w, top - r), (x + w - r, top), (x + r, top), (x, top - r)]
        sh += sct_hatch_fill(ring, "stone", k, SCT["cut"], 0.25)
        x += w + gap_m * (0.75 + 0.5 * rnd()) * k
    return sh


def sf_bench(x, y, k, side=1, seat_h=SF_SEAT_H, depth_m=0.45, t_m=0.08, back=False):
    """a bench in section at (x, y): seat seat_h (repo 0.45 m) high, depth_m deep (drawing rule), a leg, optional
    back. Returns shapes."""
    x2 = x + side * depth_m * k
    xa, xb = min(x, x2), max(x, x2)
    sy = y + seat_h * k
    sh = [("poly", [(xa, sy - t_m * k), (xb, sy - t_m * k), (xb, sy), (xa, sy)], SF_LANE["timber"], SCT["cut"], 0.2),
          ("line", [((xa + xb) / 2.0, y), ((xa + xb) / 2.0, sy - t_m * k)], SCT["cut"], 0.25)]
    if back:
        bx = xa if side > 0 else xb
        sh.append(("line", [(bx, sy), (bx - side * 0.05 * k, sy + 0.40 * k)], SCT["cut"], 0.25))
    return sh


# ---- street elements (round 3 G15; beside sf_bench). Sizes are DRAWING RULES for a typical element of its kind,
# not project data: never print them as measured. ----------------------------------------------------------------
SF_STREET = dict(lamp_h=4.00, lamp_arm=0.45, bollard_h=0.90, bollard_w=0.15, rack_h=0.75, rack_l=0.70)


def sf_lamp(x, y, k, side=1, h_m=None, layer=0, ink=None):
    """a pedestrian street lamp in section at (x, y): a slim mast h_m high (SF_STREET lamp_h 4.00 m, drawing rule),
    a short arm toward side and a lantern head; ink faded for depth layer (fig_fade). Returns shapes."""
    sc = fig_depth(layer)[0] if layer else 1.0
    K = k * sc
    ink = fig_fade(ink or SEC["ink"], layer) if layer else (ink or SEC["ink"])
    H, a = (h_m or SF_STREET["lamp_h"]) * K, SF_STREET["lamp_arm"] * K * side
    w = max(0.12, 0.06 * K)
    hx, hy = x + a, y + H - 0.05 * K
    return [("poly", [(x - w, y), (x + w, y), (x + 0.6 * w, y + H), (x - 0.6 * w, y + H)], ink, None, 0.0),
            ("line", [(x, y + H), (x + 0.6 * a, y + H + 0.06 * K), (hx, hy)], ink, max(0.1, 0.03 * K)),
            ("poly", [(hx - 0.14 * K, hy), (hx + 0.14 * K, hy), (hx + 0.07 * K, hy - 0.22 * K),
                      (hx - 0.07 * K, hy - 0.22 * K)], ink, None, 0.0)]


def sf_bollard(x, y, k, h_m=None, layer=0, ink=None):
    """a bollard in section at (x, y): SF_STREET bollard_h 0.90 m x bollard_w 0.15 m (drawing rule), rounded top,
    one light band. Returns shapes."""
    sc = fig_depth(layer)[0] if layer else 1.0
    K = k * sc
    ink = fig_fade(ink or SEC["ink"], layer) if layer else (ink or SEC["ink"])
    H, r = (h_m or SF_STREET["bollard_h"]) * K, 0.5 * SF_STREET["bollard_w"] * K
    ring = [(x - r, y), (x + r, y), (x + r, y + H - r)] + \
        [(x + r * __import__("math").cos(t), y + H - r + r * __import__("math").sin(t)) for t in
         [i * 3.14159265 / 8.0 for i in range(1, 8)]] + [(x - r, y + H - r)]
    return [("poly", ring, ink, None, 0.0),
            ("poly", [(x - r, y + 0.70 * H), (x + r, y + 0.70 * H), (x + r, y + 0.78 * H), (x - r, y + 0.78 * H)],
             "FFFFFF", None, 0.0)]


def sf_bike_rack(x, y, k, side=1, layer=0, ink=None):
    """a bike rack (an inverted-U stand) in section at (x, y), seen along its length: SF_STREET rack_l 0.70 m long,
    rack_h 0.75 m high (drawing rule), running toward side. Returns shapes."""
    import math as _m
    sc = fig_depth(layer)[0] if layer else 1.0
    K = k * sc
    ink = fig_fade(ink or SEC["ink"], layer) if layer else (ink or SEC["ink"])
    L, H = SF_STREET["rack_l"] * K * side, SF_STREET["rack_h"] * K
    r = 0.5 * abs(L)
    cx = x + 0.5 * L
    pts = [(x, y), (x, y + H - r)] + [(cx - r * _m.cos(t), y + H - r + r * _m.sin(t)) for t in
                                       [i * _m.pi / 10.0 for i in range(11)]] + [(x + L, y)]
    if side < 0:
        pts = [(x, y), (x, y + H - r)] + [(cx + r * _m.cos(t), y + H - r + r * _m.sin(t)) for t in
                                           [i * _m.pi / 10.0 for i in range(11)]] + [(x + L, y)]
    return [("line", pts, ink, max(0.12, 0.05 * K))]


# ---- zoom-in inset (round 3 G15, Aras's U29 sketch) --------------------------------------------------------------
# A use zone narrower than ~15 mm on the page gets an enlarged copy beside the section: a thin rectangle on the
# spot, the same drawing at the bigger scale in a box (white ground, 0.25 pt neatline like a map: the one frame
# G17 keeps), the label "ZOOMED IN · <what>" over it and ONE short connector from the spot's corner to the box's
# nearest corner (a frame link, not a label leader).
SF_ZOOM = dict(lw_spot=0.064, lw_box=0.088, label_mm=2.47, gap=1.0, bar_h=0.8, bar_lw=0.1)   # round 4: label 7 pt


def sf_scale_bar(x, y, k, den=None, max_mm=30.0, size=2.12, ink=None, segs=4):
    """round 4 (S2, G-R4-5.6): a small scale bar for an inset or section: segs alternating ink / white cells along a
    round length in m (1, 2, 5, 10, 20, 50, 100 ... the longest that fits max_mm at k page mm per m), left end at
    (x, y) (page mm, y up: the bar's top edge), "0" and "<L> m" under its ends and "1:<den>" after it when den is
    given; text 6 pt (minimum). Returns shapes."""
    ink = ink or SEC["ink"]
    Lm = 1.0
    for c in (1, 2, 5, 10, 20, 50, 100, 200, 500, 1000):
        if c * k <= max_mm:
            Lm = float(c)
    L = Lm * k
    h = SF_ZOOM["bar_h"]
    sh = []
    for i in range(segs):
        a, b = x + L * i / segs, x + L * (i + 1) / segs
        sh.append(("poly", [(a, y - h), (b, y - h), (b, y), (a, y)], ink if i % 2 == 0 else "FFFFFF", ink,
                   SF_ZOOM["bar_lw"]))
    ty = y - h - 0.9 * size
    sh.append(("text", u"0", x, ty, size, ink, False, "C"))
    sh.append(("text", u"%g m" % Lm, x + L, ty, size, ink, False, "C"))
    if den:
        sh.append(("text", u"1:{:,}".format(int(den)), x + L + 1.2 * size, y - h, size, ink, False, "L"))
    return sh


def _sf_clip_poly(ring, x0, y0, x1, y1):
    """Sutherland-Hodgman: ring clipped to the rectangle"""
    def cut(P, inside, inter):
        out = []
        for i in range(len(P)):
            a, b = P[i - 1], P[i]
            if inside(b):
                if not inside(a):
                    out.append(inter(a, b))
                out.append(b)
            elif inside(a):
                out.append(inter(a, b))
        return out

    def ix(xv):
        return lambda a, b: (xv, a[1] + (b[1] - a[1]) * (xv - a[0]) / ((b[0] - a[0]) or 1e-12))

    def iy(yv):
        return lambda a, b: (a[0] + (b[0] - a[0]) * (yv - a[1]) / ((b[1] - a[1]) or 1e-12), yv)
    P = list(ring)
    for inside, inter in ((lambda p: p[0] >= x0, ix(x0)), (lambda p: p[0] <= x1, ix(x1)),
                          (lambda p: p[1] >= y0, iy(y0)), (lambda p: p[1] <= y1, iy(y1))):
        if not P:
            break
        P = cut(P, inside, inter)
    return P


def _sf_clip_line(pts, x0, y0, x1, y1):
    """the pieces of a polyline inside the rectangle (Liang-Barsky per segment, joined where they touch)"""
    out, cur = [], []
    for a, b in zip(pts[:-1], pts[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        t0, t1, ok = 0.0, 1.0, True
        for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
            if abs(p) < 1e-12:
                if q < 0:
                    ok = False
                    break
                continue
            r = q / p
            if p < 0:
                t0 = max(t0, r)
            else:
                t1 = min(t1, r)
            if t0 > t1:
                ok = False
                break
        if not ok:
            if len(cur) >= 2:
                out.append(cur)
            cur = []
            continue
        pa = (a[0] + t0 * dx, a[1] + t0 * dy)
        pb = (a[0] + t1 * dx, a[1] + t1 * dy)
        if cur and abs(cur[-1][0] - pa[0]) < 1e-9 and abs(cur[-1][1] - pa[1]) < 1e-9:
            cur.append(pb)
        else:
            if len(cur) >= 2:
                out.append(cur)
            cur = [pa, pb]
        if t1 < 1.0:
            out.append(cur)
            cur = []
    if len(cur) >= 2:
        out.append(cur)
    return out


def sf_zoom_inset(src_box, dst_box, k_src, k_dst, draw_fn, label, size=None, ink=None, connector=True,
                  scale_den=None, parent_den=None, page=None):
    """G15 zoom-in inset. src_box = (x0, y0, x1, y1) page mm of the spot on the section; dst_box = the inset's box
    beside the section; k_src, k_dst = page mm per m of the section and of the inset (k_dst > k_src). draw_fn: the
    shapes of the section (a list, or a WaterLayers, or a callable returning one): every shape is re-drawn at the
    bigger scale (geometry x k_dst / k_src about the spot's centre -> the box's centre; pen widths and text sizes
    kept) and clipped to the box; images keep their pixels and get the box as clip. label: what is shown ("ZOOMED
    IN · <label>" over the box, left aligned). Returns shapes: the spot rectangle, the connector, the box ground,
    the enlarged copy, the neatline and the label. Size the box so the spot fits: (x1 - x0) x k_dst / k_src.
    Round 4 (S2, G-R4-5.6, D11): RAISES when the inset is less than SF_INSET_MIN_ZOOM (2) x its parent (k_dst / k_src,
    and parent_den / scale_den when both are given); scale_den = the inset's scale (checked against SF_INSET_SCALES:
    1:100 allowed for insets only) -> its own scale bar under the box and "1:<den>" in the caption; without it a
    FLAG line (no bar). page: the booklet page id for the log line "inset <page> parent 1:<a> inset 1:<b>". The
    caption sits above the box, outside the detail; the bar below it."""
    f_chk = float(k_dst) / float(k_src)
    if f_chk < SF_INSET_MIN_ZOOM - 1e-6:                   # round 5 (S3): a WARNING, never a stop
        _sf_warn(page, "inset", u"(%s): zoom %.2f x its parent; G-R4-5.6 needs >= %.0f x (D11: a 1:250 parent takes a "
                                u"1:100 inset)" % (label, f_chk, SF_INSET_MIN_ZOOM))
    if scale_den is not None:
        scale_den = sf_scale_ok(scale_den, inset=True)
        if parent_den is not None and float(parent_den) / float(scale_den) < SF_INSET_MIN_ZOOM - 1e-6:
            _sf_warn(page, "inset", u"(%s): 1:%s is less than 2 x its parent 1:%s (G-R4-5.6)"
                     % (label, scale_den, parent_den))
        SF_LOG.append(u"inset %s parent 1:%s inset 1:%s" % (page or u"", parent_den if parent_den else u"?",
                                                            int(scale_den)))
    else:
        SF_LOG.append(u"FLAG inset %s (%s): no scale_den passed: no scale bar (G-R4-5.6)" % (page or u"", label))
    sh_in = draw_fn() if callable(draw_fn) else draw_fn
    if hasattr(sh_in, "shapes"):
        sh_in = sh_in.shapes()
    ink = ink or SEC["ink"]
    size = size or SF_ZOOM["label_mm"]
    sx0, sy0, sx1, sy1 = src_box
    dx0, dy0, dx1, dy1 = dst_box
    f = float(k_dst) / float(k_src)
    scx, scy = 0.5 * (sx0 + sx1), 0.5 * (sy0 + sy1)
    dcx, dcy = 0.5 * (dx0 + dx1), 0.5 * (dy0 + dy1)

    def T(p):
        return (dcx + (p[0] - scx) * f, dcy + (p[1] - scy) * f)
    out = []
    for s_ in sh_in or ():
        t = s_[0]
        if t == "poly":
            r = _sf_clip_poly([T(p) for p in s_[1]], dx0, dy0, dx1, dy1)
            if len(r) >= 3:
                out.append(("poly", r) + tuple(s_[2:]))
        elif t == "line":
            for piece in _sf_clip_line([T(p) for p in s_[1]], dx0, dy0, dx1, dy1):
                out.append(("line", piece) + tuple(s_[2:]))
        elif t == "text":
            x, y = T((s_[2], s_[3]))
            if dx0 <= x <= dx1 and dy0 <= y <= dy1:
                out.append(("text", s_[1], x, y) + tuple(s_[4:]))
        elif t == "image":
            ax, ay = T((s_[1], s_[2]))
            w, h = s_[3] * f, s_[4] * f
            if ax < dx1 and ax + w > dx0 and ay < dy1 and ay + h > dy0:
                rest = tuple(s_[5:8]) + (None,) * (3 - len(s_[5:8]))
                out.append(("image", ax, ay, w, h) + rest[:3] + ((dx0, dy0, dx1, dy1),))
    box = [(dx0, dy0), (dx1, dy0), (dx1, dy1), (dx0, dy1)]
    sh = [("poly", [(sx0, sy0), (sx1, sy0), (sx1, sy1), (sx0, sy1)], None, ink, SF_ZOOM["lw_spot"])]
    if connector:                                    # spot corner -> the box's nearest corner
        cs = [(sx0, sy0), (sx1, sy0), (sx1, sy1), (sx0, sy1)]
        best = min(((a, b) for a in cs for b in box), key=lambda ab: (ab[0][0] - ab[1][0]) ** 2 + (ab[0][1] - ab[1][1]) ** 2)
        sh.append(("line", [best[0], best[1]], ink, SF_ZOOM["lw_spot"]))
    sh.append(("poly", box, "FFFFFF", None, 0.0))
    sh += out
    sh.append(("poly", box, None, ink, SF_ZOOM["lw_box"]))
    cap = u"ZOOMED IN · %s" % label + (u" · 1:{:,}".format(int(scale_den)) if scale_den else u"")
    sh.append(("text", cap, dx0, dy1 + 0.6 * size, size, ink, True, "L"))
    if scale_den:
        sh += sf_scale_bar(dx0, dy0 - SF_ZOOM["gap"], k_dst, None, max_mm=min(30.0, 0.45 * (dx1 - dx0)),
                           ink=ink)
    return sh


# ---- inset frame v2 (round 5, S3, G-R5-5: U12, U13, U14, U16; keep K2) --------------------------------------------
# Change of approach (round 4's insets were the parent's shapes scaled up: "page 14 zoom ins looks awful"): an inset
# is its OWN drawing, drawn again at its own scale k = sf_inset_k(den) so the kit's detail switches on (k >= 4, 1:250
# and larger: stone courses and deck boards at real size, section_parts SCT_DETAIL_K; treads and risers are drawn at
# true size anyway), and it is FRAMED ON THE ACTION: the window is computed from what the inset is about (the person,
# rod and line end, the water it shows, the seat or tread), never typed. Export: D_child = ix.drawing(...,
# scale_pref=[den]); ix.inset(page, parent id, window, child id, factor) (S1 schema); the booklet draws the frame, the
# link and the scale bar. sf_zoom_inset (scaled copy) stays only for pages not yet moved.
SF_INSET = dict(margin_m=0.6, min_w_m=3.0)          # clear margin round the action; smallest window (drawing rules)


def sf_inset_k(den):
    """page mm per m of an inset at 1:den (1:100 allowed, D11)"""
    return 1000.0 / sf_scale_ok(den, inset=True)


def sf_inset_frame(focus, parent_den, box_mm=None, margin_m=None, page=None, label=u""):
    """G-R5-5 framing: focus = the boxes (x0, y0, x1, y1, drawing m: chainage x, level y) of everything the inset is
    about (person, rod + line end, the water surface it shows, the seat); returns dict(window (m), den, factor, k)
    or None: the window = their union + margin_m on every side (centred on the action, so nothing it is about is
    cut), widened to box_mm's aspect (w, h mm) when given; den = the LARGEST scale on SF_INSET_SCALES that is >= 2 x
    the parent (den <= parent_den / 2) and fits box_mm (when given). WARNING when no listed scale fits."""
    m = SF_INSET["margin_m"] if margin_m is None else margin_m
    bx = [b for b in focus or () if b]
    if not bx:
        _sf_warn(page, "inset", u"(%s): nothing to frame (no focus boxes)" % label)
        return None
    x0 = min(b[0] for b in bx) - m
    y0 = min(b[1] for b in bx) - m
    x1 = max(b[2] for b in bx) + m
    y1 = max(b[3] for b in bx) + m
    if x1 - x0 < SF_INSET["min_w_m"]:
        c = 0.5 * (x0 + x1)
        x0, x1 = c - 0.5 * SF_INSET["min_w_m"], c + 0.5 * SF_INSET["min_w_m"]
    if box_mm:
        bw, bh = float(box_mm[0]), float(box_mm[1])
        w, h = x1 - x0, y1 - y0
        if w / h < bw / bh:                       # widen to the box's aspect, centred (the action stays centred)
            d = 0.5 * (h * bw / bh - w)
            x0, x1 = x0 - d, x1 + d
        else:
            d = 0.5 * (w * bh / bw - h)
            y0, y1 = y0 - d, y1 + d
    ok = [d_ for d_ in SF_INSET_SCALES if d_ <= float(parent_den) / SF_INSET_MIN_ZOOM + 1e-6]
    den = None
    for d_ in ok:                                 # largest scale first (smallest denominator)
        if not box_mm or ((x1 - x0) * 1000.0 / d_ <= box_mm[0] + 1e-6 and (y1 - y0) * 1000.0 / d_ <= box_mm[1] + 1e-6):
            den = d_
            break
    if den is None:
        den = ok[-1] if ok else SF_INSET_SCALES[0]
        _sf_warn(page, "inset", u"(%s): the action (%.1f x %.1f m) does not fit %s mm at any listed inset scale >= 2 x "
                                u"1:%s; 1:%d used" % (label, x1 - x0, y1 - y0, box_mm, parent_den, den))
    SF_LOG.append(u"inset %s %s: parent 1:%s inset 1:%d, window %.1f x %.1f m" % (
        page or u"", label, parent_den, den, x1 - x0, y1 - y0))
    return dict(window=(x0, y0, x1, y1), den=den, factor=float(parent_den) / den, k=1000.0 / den)


def sf_inset_cut_check(window, items, page=None, label=u""):
    """U16 "nothing cut by the inset frame": items = [(name, (x0, y0, x1, y1) m)] of the people, objects and plants
    drawn in the inset; one that the window's edge cuts (partly inside) is a WARNING. Returns the names cut."""
    wx0, wy0, wx1, wy1 = window
    cut = []
    for nm, b in items or ():
        inside = b[0] >= wx0 and b[2] <= wx1 and b[1] >= wy0 and b[3] <= wy1
        out = b[2] <= wx0 or b[0] >= wx1 or b[3] <= wy0 or b[1] >= wy1
        if not inside and not out:
            cut.append(nm)
    if cut:
        _sf_warn(page, "inset", u"(%s): cut by the frame: %s" % (label, u", ".join(u"%s" % c for c in cut)))
    return cut


# ---- G6: people 1.75 m vs tree heights vs buildings, at depth layer 0 ----------------------------------------------
def sf_assert_g6(k, trees=(), buildings=(), strict=False, layer=0, page=None):
    """the G6 scale check of one drawing at depth layer 0: figures print at their true height for k (figures.py
    fig_check_scale), every tree drawn (key, h_m) or placed (key, x, h_m, crown_m) inside its sourced height range
    (so the tree / person ratio is the real one), every building (name, drawn_h_m, data_h_m) at its data height
    (+-0.05 m). Round 5 (S3, A13): a true-scale miss is a WARNING line (never a stop); strict=True still raises for
    an old caller that asks. Returns the messages ([] when all is right)."""
    bad = []
    try:
        fig_check_scale(k, layer=layer)
    except AssertionError as ex:
        bad.append(u"%s" % ex)
    for t in trees or ():
        key, h = t[0], (t[1] if len(t) == 2 else t[2])
        sp = PLA_SPECIES.get(key)
        if sp is None:
            bad.append(u"G6: unknown species %r" % (key,))
            continue
        lo, hi = sp["h_range"]
        if (lo is not None and h < lo - 1e-6) or (hi is not None and h > hi + 1e-6):
            bad.append(u"G6: %s drawn %.2f m, sourced %s-%s m (tree / person %.1f)" % (key, h, lo or "", hi or "",
                                                                                    h / FIG_ADULT_H))
    for name, drawn, data in buildings or ():
        if data is not None and abs(float(drawn) - float(data)) > 0.05:
            bad.append(u"G6: building %s drawn %.2f m, data %.2f m" % (name, drawn, data))
    if bad and strict:
        raise AssertionError(u"; ".join(bad))
    for m_ in bad:
        _sf_warn(page, "scale", m_)
    return bad
