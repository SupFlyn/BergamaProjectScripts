# p.17 planting and water (water board v6, revision 29 Oct 2026, T4a WO-T4a-2, package F "Page 17"; D2, D6, D9 a: the
# p.20 ladder folds into this page and pp.14-15). Two booklet pages, built from project data only:
#   page A (p17_page, crop wb_plants): the PLAN. A key strip of the analysis frame (basemap "topographic", the two plan
#        windows, the hubs; no cut lines: page A draws no section) and two plan windows at one standard scale on the
#        shared basemap (streets, buildings, fields): the upstream entry (reed basins, spillway, shaded walk, rain
#        terraces, summer strip) and the lower reach (widened stream and wetland, side arm, summer strip). Every
#        species as its top-view crown at true size (plants.py pla_plan, the same size as in the sections), every
#        water space numbered (R35), July shade hours on the bed and the water spaces (site board shade_july.json),
#        the cut lines F1-F4 of page B. Under them the numbered list and the species catalogue (R36: photo, silhouette
#        and crown from the primitives, foliage, height, water, role; sourced values only, species.json + plants.py).
#   page B (p17b_page, crop wb_plants_b): the SECTIONS at 1:500, each with its zone labels on vertical lines, levels
#        from the level module, people by activity (_p17_fig), a scale bar: F2 rain terraces + reed basins (new line,
#        LEVELS "F2"), F4 side arm (new line, LEVELS "F4"), F1 the stream at the inflow on the W1 line with the reed
#        basins beyond, F3 the widened stream on the S4 line with the planting bands and their days under water (the
#        S4 band section folded in; the S4 geometry and plants are p.14's own, _p14_geo / P14_PLANTS, so the cut is the
#        same everywhere). A key map with ONLY F1-F4, the bloom / leaf calendar (one month axis), giant reed: remove.
# build_board calls P17_TITLE, P17B_TITLE, p17_page(pg, box, opt, log), p17b_page(pg, box, opt, log); each returns
# [(crop id, bbox, scale denominator)].

P17_TITLE = u"PLANTING AND WATER · where each plant goes around the water spaces"
P17B_TITLE = u"PLANTING AND WATER IN SECTION · four cuts, the species and their year"
P17_W = 377.0                        # the most a page takes, mm (the booklet's A3 panel at 1:1)
P17_SAY = (u"**Wet to dry, low to high**: rushes and loosestrife at the water, willow and tamarisk on the banks that "
           u"flood, shade trees and olives on the dry tops. **Common reed and water mint** only in lined basins the "
           u"flood bypasses.")
P17B_SAY = (u"Each cut shows the **water**, the **planting band** each species needs, and **what surrounds it**: "
            u"streets, walks, terraces.")
# sizes drawn (m): (height, crown) as p.14 draws S4 (trees at about ten years, inside plants.py's sourced ranges); the
# others plants.py's own (None). The plan, the sections and the catalogue use these, so a crown and its tree agree.
P17_SIZE = {"plane": (12.0, 12.0), "ash": (12.0, 8.4), "willow": (10.0, 7.0), "tamarisk": (5.0, 4.5),
            "chaste": (3.0, 2.5), "loosestrife": (1.5, 1.0), "soft_rush": (1.0, 0.6), "olive": (5.0, 5.0),
            "lavender": (None, None), "rosemary": (None, None)}
P17_CAT = ("reed", "mint", "soft_rush", "loosestrife", "willow", "tamarisk", "chaste", "ash", "plane", "olive",
           "rosemary", "lavender")   # the catalogue, wet to dry
P17_DENS = (1000.0, 2000.0, 2500.0, 5000.0)   # the plan windows: the first standard scale at which both fit
P17_BAR = {1000.0: (0, 10, 20, 50), 2000.0: (0, 20, 50, 100), 2500.0: (0, 20, 50, 100), 5000.0: (0, 50, 100, 200)}
P17_SEC_DEN = 500.0                  # every section
P17_FS, P17_HEAD = FS_MIN, 3.4       # label and heading sizes, mm
P17_FIG = "4F453C"                   # people
P17_WATER = "8CBBC8"                 # summer water in the sections and the strip in plan
P17_ZONE = {"WT": ("CBEDE5", "8DB8AF"), "WD": ("C1D3DB", "889EA8"), "GR": ("E9E3D2", "B0AC9C"),
            "WS": ("E6DFC6", "B5AA93"), "WP": ("DCE9D2", "A7B67F"), "ARM": ("B9D7DE", "5D7F8D"),
            "STRIP": (P17_WATER, "4B92A3"), "WIDEN": ("D3E4E8", "889EA8")}
P17_SHADE = ((2.0, "E6DCC6", u"under 2 h"), (5.0, "CDBF9F", u"2-5 h"), (99.0, "A99A78", u"over 5 h"))
P17_BASIN = dict(kerb_h=0.30, depth=1.10, media=0.80, kerb_t=0.15)   # lined basin cell: drawing values (no source)
P17_ARM_W = 3.0                      # the side arm, m either side of its line (masterplan R28DT_ARM_M)
# the side arm the F4 cut crosses, survey m, while the masterplan writes no corridor geometry: its middle part read off
# the masterplan plan (p.23, georeferenced on the analysis frame, +-5 m); masterplan_results.json "corridor" "arms"
# replaces it when present (log line otherwise)
P17_ARM_FALLBACK = [(30666.1, 31215.0), (30680.9, 31177.7), (30722.8, 31141.0), (30768.4, 31113.1),
                    (30804.0, 31090.5), (30834.3, 31057.9), (30869.1, 31026.4), (30894.6, 31025.7),
                    (30918.6, 31043.1)]
P17_ROWS_L = 45.0                    # plan: the planting bands of a cut repeat this far up and down the stream, m


# ---------------------------------------------------------------- small helpers
def _p17_put(pg, shapes):
    sec_put(pg, shapes)


def _p17_fig(pg, pose, x, y, k, facing=1, view="side", h_m=1.70, col=None, **p):
    """ONE place for the people of p.17 (common/figures.py): side view feet at (x, y) or top view centred there, k mm
    per m. "sit" = the library's sit_chair."""
    ink = col or P17_FIG
    if view == "top":
        sh = fig_top(pose, x, y, k, ink=ink)
    else:
        sh = fig_side("sit_chair" if pose == "sit" else pose, x, y, k, facing, ink=ink, h_m=h_m, **p)
    _p17_put(pg, sh)


def _p17_size(key):
    h, w = P17_SIZE.get(key, (None, None))
    sp = PLA_SPECIES[key]
    return (h or sp["h_m"]), (w or sp["crown_m"])


def _p17_sec_plant(pg, key, x, gy, k, seed=0, beyond=False):
    h, w = _p17_size(key)
    _p17_put(pg, pla_section(key, x, gy, k, h_m=h, crown_m=w, beyond=beyond, seed=seed))


def _p17_plan_plant(pg, key, x, y, k, seed=0):
    _p17_put(pg, pla_plan(key, x, y, k, crown_m=_p17_size(key)[1], seed=seed))


def _p17_rnd(i, s=0):
    """a fixed jitter 0-1 (the same every run)"""
    v = math.sin(i * 12.9898 + s * 78.233) * 43758.5453
    return v - math.floor(v)


def _p17_pip(p, ring):
    x, y, ins = p[0], p[1], False
    n = len(ring)
    for i in range(n):
        (xa, ya), (xb, yb) = ring[i], ring[(i + 1) % n]
        if (ya > y) != (yb > y) and x < xa + (y - ya) * (xb - xa) / (yb - ya):
            ins = not ins
    return ins


def _p17_cen(R):
    return (sum(p[0] for p in R) / len(R), sum(p[1] for p in R) / len(R))


def _p17_half(ring, a, n):
    """ring clipped to the half plane (p - a) . n >= 0 (Sutherland-Hodgman, one edge)"""
    def f(p):
        return (p[0] - a[0]) * n[0] + (p[1] - a[1]) * n[1]
    out = []
    for i in range(len(ring)):
        p, q = ring[i - 1], ring[i]
        fp, fq = f(p), f(q)
        if fq >= 0:
            if fp < 0:
                t = fp / (fp - fq)
                out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
            out.append(q)
        elif fp >= 0:
            t = fp / (fp - fq)
            out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
    return out if len(out) >= 3 else None


def _p17_seg_d(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 < 1e-12 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def _p17_line_d(p, P):
    return min(_p17_seg_d(p, a, b) for a, b in zip(P[:-1], P[1:])) if len(P) > 1 else 1e9


def _p17_along(P, d):
    """point and unit direction at arc length d along the polyline P (clamped)"""
    acc = 0.0
    for a, b in zip(P[:-1], P[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L < 1e-9:
            continue
        if acc + L >= d or b is P[-1]:
            t = max(0.0, min(1.0, (d - acc) / L))
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        acc += L
    a, b = P[-2], P[-1]
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    return b, ((b[0] - a[0]) / L, (b[1] - a[1]) / L)


def _p17_cross(a, b, P):
    """where the segment a-b crosses the polyline P first: (point, arc length along P) or None"""
    acc = 0.0
    for p, q in zip(P[:-1], P[1:]):
        L = math.hypot(q[0] - p[0], q[1] - p[1])
        d1 = (b[0] - a[0], b[1] - a[1])
        d2 = (q[0] - p[0], q[1] - p[1])
        den = d1[0] * d2[1] - d1[1] * d2[0]
        if abs(den) > 1e-12:
            w = (p[0] - a[0], p[1] - a[1])
            t = (w[0] * d2[1] - w[1] * d2[0]) / den
            s = (w[0] * d1[1] - w[1] * d1[0]) / den
            if 0.0 <= t <= 1.0 and 0.0 <= s <= 1.0:
                return (a[0] + d1[0] * t, a[1] + d1[1] * t), acc + s * L
        acc += L
    return None


def _p17_text_box(s, x, y, fs, bold=False, align="L"):
    w = text_w(s, fs, bold)
    x0 = x - {"L": 0.0, "C": w / 2.0, "R": w}[align]
    return (x0, y - fs * 0.3, x0 + w, y + fs * CAP)


def _p17_badge(pg, n, x, y, size=3.6, colour=None):
    """a numbered water-space badge (icons.py ico_step) centred on (x, y); its box"""
    sh, (ax, ay), th, cap = ico_step(x, y, size, "solid", colour or MP["discharge"][2])
    _p17_put(pg, sh)
    pg.text(str(n), ax, ay - cap / 2.0, cap / CAP, th, bold=True, align="C")
    return (x - size / 2.0, y - size / 2.0, x + size / 2.0, y + size / 2.0)


def _p17_north(pg, x, y, d, L=6.0):
    """north arrow at (x, y) along the unit page direction d; its box"""
    tip = (x + d[0] * L, y + d[1] * L)
    arrow(pg, [(x, y), tip], COL["ink"], 0.3, 1.8)
    pg.text(u"N", tip[0] + d[0] * 1.8, tip[1] + d[1] * 1.8 - P17_FS * CAP / 2.0, P17_FS, COL["ink"], bold=True,
            align="C")
    return (min(x, tip[0]) - 3.0, min(y, tip[1]) - 3.0, max(x, tip[0]) + 3.0, max(y, tip[1]) + 3.5)


# ---------------------------------------------------------------- data, read once a run
_P17_MEMO = {}


def _p17_zones():
    """the Option A zones (survey m) from the water balance results "zones": [dict(code, label, ring, ...)]"""
    if "zones" not in _P17_MEMO:
        z = _p12_get("zones") or {}
        _P17_MEMO["zones"] = [dict(q, ring=[tuple(p) for p in q["ring"]]) for q in z.get("zones") or []
                              if len(q.get("ring") or []) >= 3]
    return _P17_MEMO["zones"]


def _p17_mp(log):
    """masterplan_results.json (the masterplan's cache folder), read once; {} when missing (logged)"""
    if "mp" not in _P17_MEMO:
        d = {}
        for fn in (os.path.join(bg_cache("bergama_masterplan"), "masterplan_results.json"),
                   os.path.join(bg_output("bergama_masterplan"), "masterplan_results.json")):
            try:
                with open(fn, "r", encoding="utf-8") as f:
                    d = json.load(f)
                break
            except Exception:
                continue
        if not d:
            log.append(u"p.17: no masterplan_results.json: hubs from the four chain places, side arm from its p.23 line")
        _P17_MEMO["mp"] = d
    return _P17_MEMO["mp"]


def _p17_hubs(log):
    """[(name, (x, y))] the hubs of the masterplan's movement, else K4 and K5 of the chain"""
    hs = ((_p17_mp(log).get("movement") or {}).get("hubs")) or []
    out = [(h.get("name") or u"", tuple(h["xy"])) for h in hs if h.get("xy")]
    return out or [(n, p) for n, p in P12_PLACES if n.startswith(u"K")]


def _p17_arms(log):
    """the side arms (survey m polylines): masterplan_results.json "corridor" "arms" (a later masterplan writes it),
    else the one read off p.23 that F4 crosses"""
    co = _p17_mp(log).get("corridor") or {}
    arms = [[tuple(p) for p in (a.get("P") if isinstance(a, dict) else a)] for a in co.get("arms") or []]
    if arms:
        return arms
    if "arm_log" not in _P17_MEMO:
        _P17_MEMO["arm_log"] = 1
        log.append(u"p.17: the masterplan writes no corridor geometry: the side arm is the one read off p.23 (+-5 m)")
    return [list(P17_ARM_FALLBACK)]


def _p17_widen(log):
    co = _p17_mp(log).get("corridor") or {}
    return [[tuple(p) for p in (w.get("ring") if isinstance(w, dict) else w)] for w in co.get("widen") or []]


def _p17_shade(log):
    """(cells [(x, y, hours)], daylight h, cell m) from the site board's shade_july.json, read once; None (one log
    line)"""
    if "shade" not in _P17_MEMO:
        r = None
        fn = os.path.join(bg_output("selinus_board"), "shade_july.json")
        try:
            with open(fn, "r", encoding="utf-8") as f:
                d = json.load(f)
            cells = [(float(c[0]), float(c[1]), float(c[2])) for c in (d.get("map") or {}).get("cells") or []]
            if cells:
                r = (cells, float(d.get("daylight_h") or 0.0), float((d.get("map") or {}).get("cell_m") or 5.0))
        except Exception:
            r = None
        if r is None:
            log.append(u"p.17: no shade_july.json ({}): the plans are drawn without July shade (run the site board v51+ "
                       u"with its environment analyses)".format(fn))
        _P17_MEMO["shade"] = r
    return _P17_MEMO["shade"]


def _p17_s4_pt(s):
    """the S4 point s m across the stream from where S4 crosses the Selinos line (north-east +), survey m"""
    if "s4" not in _P17_MEMO:
        a, b = level_ends("S4")
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        c = _p17_cross(a, b, P12_SELINOS)
        _P17_MEMO["s4"] = ((c[0] if c else ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)), u)
    o, u = _P17_MEMO["s4"]
    return (o[0] + u[0] * s, o[1] + u[1] * s)


def _p17_cut_pt(cid, t):
    """the point t m along a level cut from its first end, survey m"""
    a, b = level_ends(cid)
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    return (a[0] + (b[0] - a[0]) * t / L, a[1] + (b[1] - a[1]) * t / L)


def _p17_lv(cid, key, side=None):
    v = level(cid, key, side)
    if v is None:
        raise RuntimeError(u"{}: '{}' {} is missing in the level module (common/data/LEVELS.py)".format(
            cid, key, side or u""))
    return v


def _p17_ground(cid):
    """the surveyed ground of a T4a cut [(m along, m a.s.l.)] (LEVELS row field "ground")"""
    g = (level_cut(cid).get("ground") or {}).get("value") or []
    if len(g) < 2:
        raise RuntimeError(u"{}: no ground profile in the level module".format(cid))
    return [(float(t), float(z)) for t, z in g]


def _p17_interp(P, t):
    if t <= P[0][0]:
        return P[0][1]
    for (a, za), (b, zb) in zip(P[:-1], P[1:]):
        if a <= t <= b:
            return za + (zb - za) * (t - a) / ((b - a) or 1.0)
    return P[-1][1]


# ---------------------------------------------------------------- page A: the plan windows
# the plants of each cut (m along the cut from its first end; S4: p.14's own list, m across from the bed), repeated in
# plan as rows along the stream P17_ROWS_L either side of the cut, at the same offset from the Selinos line
P17_F1_PLANTS = [("plane", 6.0), ("plane", 16.0), ("loosestrife", 23.4), ("soft_rush", 29.6), ("loosestrife", 30.4),
                 ("soft_rush", 53.9), ("ash", 63.0)]
P17_F4_PLANTS = [("ash", 16.0), ("plane", 22.0), ("loosestrife", 25.8), ("soft_rush", 34.2), ("ash", 41.0),
                 ("tamarisk", 50.0), ("chaste", 55.5), ("willow", 64.0), ("chaste", 69.5), ("soft_rush", 75.0),
                 ("soft_rush", 85.6), ("loosestrife", 92.0), ("soft_rush", 112.8), ("chaste", 117.5),
                 ("tamarisk", 122.5), ("plane", 137.0)]


def _p17_axis(R):
    """centre, long axis u, its normal v and the half extents along u and v of a ring (principal axes)"""
    c = _p17_cen(R)
    sxx = sum((p[0] - c[0]) ** 2 for p in R)
    syy = sum((p[1] - c[1]) ** 2 for p in R)
    sxy = sum((p[0] - c[0]) * (p[1] - c[1]) for p in R)
    a = 0.5 * math.atan2(2.0 * sxy, sxx - syy)
    u, v = (math.cos(a), math.sin(a)), (-math.sin(a), math.cos(a))
    us = [(p[0] - c[0]) * u[0] + (p[1] - c[1]) * u[1] for p in R]
    vs = [(p[0] - c[0]) * v[0] + (p[1] - c[1]) * v[1] for p in R]
    return c, u, v, (min(us), max(us)), (min(vs), max(vs))


def _p17_frame_uv():
    """the analysis frame's long axis (upstream end at the left) and its normal, or None"""
    fr = basemap_frame()
    if not fr:
        return None
    cx, cy = _p17_cen(fr)
    e1 = (fr[1][0] - fr[0][0], fr[1][1] - fr[0][1])
    e2 = (fr[2][0] - fr[1][0], fr[2][1] - fr[1][1])
    u = e1 if math.hypot(*e1) >= math.hypot(*e2) else e2
    L = math.hypot(*u)
    u = (u[0] / L, u[1] / L)
    if (fr[0][0] - cx) * u[0] + (fr[0][1] - cy) * u[1] > 0:
        u = (-u[0], -u[1])
    return u, (-u[1], u[0])


def _p17_win_pts(key, log):
    """the survey points a plan window must hold"""
    pts = []
    zs = _p17_zones()
    if key == "A":
        for cid in ("F2", "W1"):
            pts += list(level_ends(cid))
        pts += [p for z in zs if z.get("study_area") == "aras_alan" and z["code"] != "STRIP" for p in z["ring"]]
    else:
        pts += list(level_ends("F4"))
        pts += [_p17_s4_pt(s) for s in P14_RANGE]
        pts += [p for z in zs if z["code"] == "WP" for p in z["ring"]]
        mid = _p17_cut_pt("F4", 0.5 * level("F4", "length_m"))
        pts += [p for a in _p17_arms(log) for p in a if math.hypot(p[0] - mid[0], p[1] - mid[1]) < 150.0]
    return pts


def _p17_win_fit(pts, den, pad=8.0):
    """the best turn for a window at 1:den: (w mm, h mm, u, v, centre, den) of north-up or along the frame, the smaller"""
    best = None
    k = 1000.0 / den
    turns = [((1.0, 0.0), (0.0, 1.0))]
    fu = _p17_frame_uv()
    if fu:
        turns.append(fu)
    for u, v in turns:
        us = [p[0] * u[0] + p[1] * u[1] for p in pts]
        vs = [p[0] * v[0] + p[1] * v[1] for p in pts]
        w, h = (max(us) - min(us) + 2 * pad) * k, (max(vs) - min(vs) + 2 * pad) * k
        c = ((min(us) + max(us)) / 2.0, (min(vs) + max(vs)) / 2.0)
        if best is None or w * h < best[0] * best[1] - 1e-6:
            best = (w, h, u, v, c, den)
    return best


def _p17_basemap_into(sp, items, T):
    def fill_fn(rings, hx, alpha, nonzero):
        sp.poly([r_ for r_ in rings if len(r_) >= 3], fill=hx, alpha=alpha if alpha is not None and alpha < 0.999 else None)

    def line_fn(pts, hx, w_mm, dash_mm, alpha):
        d_ = None
        if dash_mm:
            d_ = list(dash_mm) if isinstance(dash_mm, (list, tuple)) else [dash_mm, dash_mm]
        sp.line(pts, hx, w_mm, dash=d_)
    basemap_draw(items, T, fill_fn, line_fn)


def _p17_fill_rings(items):
    """the rings of the fill items of a basemap item list (survey m)"""
    out = []
    for it in items:
        if it[0] == "fill":
            out += [r for r in it[1] if len(r) >= 3]
    return out


def _p17_rows(sp, cid, plants, T, k, skip, n0=0):
    """the planting of a cut repeated in plan as rows along the Selinos line, P17_ROWS_L either side of the cut, at
    each plant's offset from the line; skip(p_survey, key) leaves a spot out"""
    a, b = level_ends(cid)
    c = _p17_cross(a, b, P12_SELINOS)
    if not c:
        return 0
    (cx, cy), d0 = c
    t0 = math.hypot(cx - a[0], cy - a[1])
    ux, uy = b[0] - a[0], b[1] - a[1]
    n = 0
    for i, (key, t) in enumerate(plants):
        off = t - t0
        cw = _p17_size(key)[1]
        step = max(1.3 * cw, 2.0)
        d = d0 - P17_ROWS_L
        j = 0
        while d <= d0 + P17_ROWS_L:
            (px, py), (dx, dy) = _p17_along(P12_SELINOS, d)
            nx, ny = -dy, dx
            if nx * ux + ny * uy < 0:
                nx, ny = -nx, -ny
            jit = (_p17_rnd(i * 97 + j, 3) - 0.5) * 0.3 * step
            q = (px + nx * (off + jit * 0.3), py + ny * (off + jit * 0.3))
            if not skip(q, key):
                X, Y = T(q)
                _p17_plan_plant(sp, key, X, Y, k, n0 + i * 31 + j)
                n += 1
            d += step + jit
            j += 1
    return n


def _p17_window(pg, x0, ytop, key, den, fit, log):
    """one plan window, its top-left at (x0, ytop): the basemap, the water spaces with their planting, July shade, the
    cut lines, the hubs and the numbered badges, frame, north arrow and scale bar under it. Returns (bbox, numbers)."""
    w, h, u, v, c = fit[:5]
    k = 1000.0 / den
    R = (x0, ytop - h, x0 + w, ytop)
    ox, oy = (R[0] + R[2]) / 2.0, (R[1] + R[3]) / 2.0

    def T(p):
        return (ox + ((p[0] * u[0] + p[1] * u[1]) - c[0]) * k, oy + ((p[0] * v[0] + p[1] * v[1]) - c[1]) * k)

    def Ti(X, Y):
        a_, b_ = (X - ox) / k + c[0], (Y - oy) / k + c[1]
        return (a_ * u[0] + b_ * v[0], a_ * u[1] + b_ * v[1])
    corners = [Ti(R[0], R[1]), Ti(R[2], R[1]), Ti(R[2], R[3]), Ti(R[0], R[3])]
    sb = (min(p[0] for p in corners), min(p[1] for p in corners), max(p[0] for p in corners),
          max(p[1] for p in corners))

    def inR(p):
        X, Y = T(p)
        return R[0] <= X <= R[2] and R[1] <= Y <= R[3]
    sp = Page(0, 0)
    sp.poly([rect(*R)], fill=COL["white"])
    D = basemap_load(log=log)
    bld, water = [], []
    if D:
        try:
            _p17_basemap_into(sp, basemap_items("detailed", {"trees": False, "green": False, "contours": False},
                                                box=sb, D=D, split_buildings=True), T)
            off = {"stream": False, "streets": False, "buildings": False, "green": False, "trees": False,
                   "fields": False, "contours": False}
            bld = _p17_fill_rings(basemap_items("detailed", dict(off, buildings=True), box=sb, D=D, split_buildings=True))
            water = _p17_fill_rings(basemap_items("detailed", dict(off, stream=True), box=sb, D=D))
        except Exception as ex:
            log.append(u"p.17 plan {}: basemap not drawn: {}: {}".format(key, type(ex).__name__, ex))
    zs = [z for z in _p17_zones() if any(inR(p) for p in z["ring"])]
    arms = [a for a in _p17_arms(log) if any(inR(p) for p in a)]
    widen = [r for r in _p17_widen(log) if any(inR(p) for p in r)]
    for r in widen:
        sp.poly([[T(p) for p in r]], fill=P17_ZONE["WIDEN"][0], stroke=P17_ZONE["WIDEN"][1], lw=0.1)
    for z in zs:                                         # the water spaces, flat (planting comes after the shade)
        if z["code"] in P17_ZONE and z["code"] != "WT":
            f_, s_ = P17_ZONE[z["code"]]
            sp.poly([[T(p) for p in z["ring"]]], fill=f_, stroke=s_, lw=0.12)
    for a in arms:
        P = [T(p) for p in a]
        sp.poly([_p14_band(P, 2.0 * P17_ARM_W * k)], fill=P17_ZONE["ARM"][0], stroke=P17_ZONE["ARM"][1], lw=0.12)
    # July shade on the bed and the water spaces (5 m cells, three classes)
    sh = _p17_shade(log)
    spaces = water + [z["ring"] for z in zs] + widen
    if sh:
        cells, day, cm = sh
        hc = cm / 2.0
        for x, y, hrs in cells:
            if not (sb[0] - cm <= x <= sb[2] + cm and sb[1] - cm <= y <= sb[3] + cm):
                continue
            q = (x, y)
            if not (any(_p17_pip(q, r) for r in spaces) or any(_p17_line_d(q, a) <= P17_ARM_W for a in arms)):
                continue
            col = next(cl for lim, cl, _ in P17_SHADE if hrs < lim)
            sp.poly([[T((x - hc, y - hc)), T((x + hc, y - hc)), T((x + hc, y + hc)), T((x - hc, y + hc))]], fill=col,
                    alpha=0.6)
    # the planting: lined basin cells, spillway rushes, shaded walk planes, rain terraces, the strip's edges,
    # the wetland, the side arm, the rows of the cuts
    taken_rings = []
    for z in zs:
        Rp = [T(p) for p in z["ring"]]
        code = z["code"]
        try:
            if code == "WT":
                cz, au, av, (a0, a1), _ = _p17_axis(Rp)
                cuts = [a0 + (a1 - a0) * f for f in (1.0 / 3.0, 2.0 / 3.0)]
                cells = []
                for i, kind in enumerate(("reed", "reed", "mint")):
                    rr = Rp
                    if i > 0:
                        rr = _p17_half(rr, (cz[0] + au[0] * cuts[i - 1], cz[1] + au[1] * cuts[i - 1]), au)
                    if rr and i < 2:
                        rr = _p17_half(rr, (cz[0] + au[0] * cuts[i], cz[1] + au[1] * cuts[i]), (-au[0], -au[1]))
                    if rr:
                        cells.append((kind, rr))
                for kind, rr in cells:
                    _p17_put(sp, pla_cell_plan(kind, rr, k, P17_BASIN["kerb_t"]))
                taken_rings.append(z["ring"])
            elif code == "WD":
                _p17_scatter(sp, Rp, ("soft_rush",), 1.6 * k, k, 11)
                taken_rings.append(z["ring"])
            elif code == "GR":
                cz, au, av, (a0, a1), _ = _p17_axis(Rp)
                cw = _p17_size("plane")[1] * k
                n = max(1, int((a1 - a0) / cw))
                for i in range(n):
                    s = a0 + (a1 - a0) * (i + 0.5) / n
                    p = (cz[0] + au[0] * s, cz[1] + au[1] * s)
                    if _p17_pip(p, Rp):
                        _p17_plan_plant(sp, "plane", p[0], p[1], k, 50 + i)
                taken_rings.append(z["ring"])
            elif code == "WS":
                cz, au, av, (a0, a1), (b0, b1) = _p17_axis(Rp)
                ang = math.degrees(math.atan2(au[1], au[0]))
                bb = b0 + 7.0 * k
                while bb < b1 - 1e-6:                        # terrace edges along the contours, 7 m apart
                    seg = [(cz[0] + au[0] * a0 * 1.2 + av[0] * bb, cz[1] + au[1] * a0 * 1.2 + av[1] * bb),
                           (cz[0] + au[0] * a1 * 1.2 + av[0] * bb, cz[1] + au[1] * a1 * 1.2 + av[1] * bb)]
                    for run in _p17_clip_seg(seg, Rp):
                        sp.line(run, "8C8170", 0.3)
                        L = math.hypot(run[1][0] - run[0][0], run[1][1] - run[0][1])
                        m = int(L / (1.5 * k))
                        for j in range(m):
                            t = (j + 0.5) / max(m, 1)
                            q = (run[0][0] + (run[1][0] - run[0][0]) * t + av[0] * 0.8 * k,
                                 run[0][1] + (run[1][1] - run[0][1]) * t + av[1] * 0.8 * k)
                            _p17_plan_plant(sp, "rosemary" if j % 2 else "lavender", q[0], q[1], k, 70 + j)
                    bb += 7.0 * k
                _p17_put(sp, pla_crop_plan("olive", Rp, k, row_spacing=7.0, plant_spacing=5.0, ang_deg=ang,
                                           crown_m=_p17_size("olive")[1], field=False))
                taken_rings.append(z["ring"])
            elif code == "STRIP":
                _p17_edge(sp, Rp, ("soft_rush", "loosestrife"), 2.5 * k, k, 90)
            elif code == "WP":
                _p17_wetland(sp, z["ring"], T, k, bld)
                taken_rings.append(z["ring"])
        except Exception as ex:
            log.append(u"p.17 plan {}: {} not planted: {}: {}".format(key, code, type(ex).__name__, ex))
    for a in arms:
        P = [T(p) for p in a]
        for side in (-1.0, 1.0):
            _p17_edge(sp, _p17_offset(P, side * (P17_ARM_W + 1.0) * k), ("soft_rush", "loosestrife"), 2.2 * k, k,
                      120 if side > 0 else 140, closed=False)

    def skip(q, key_):
        if any(_p17_pip(q, r) for r in bld) or any(_p17_pip(q, r) for r in taken_rings):
            return True
        if key_ not in ("soft_rush", "loosestrife") and any(_p17_line_d(q, a) <= P17_ARM_W + 0.5 for a in arms):
            return True
        return not inR(q)
    for cid, plants in (("W1", P17_F1_PLANTS), ("F4", P17_F4_PLANTS)):
        if inR(_p17_cut_pt(cid, 0.5 * level(cid, "length_m"))):
            _p17_rows(sp, cid, plants, T, k, skip, 200)
    if key == "B":
        a_, _b = level_ends("S4")
        t0 = math.hypot(_p17_s4_pt(0.0)[0] - a_[0], _p17_s4_pt(0.0)[1] - a_[1])
        _p17_rows(sp, "S4", [(key_, t0 + s) for key_, s, _h, _w in P14_PLANTS], T, k, skip, 400)
    # the cut lines of page B (F1 on W1, F3 on S4), dash-dot, their names at the ends
    taken = []
    for cid, nm in P17_CUTS:
        a, b = level_ends(cid)
        A, B = T(a), T(b)
        runs = _p14_clip_line([A, B], (R[0] + 1.0, R[1] + 1.0, R[2] - 1.0, R[3] - 1.0))
        for run in runs:
            sp.line(run, COL["ink_dark"], 0.3, dash=[2.4, 0.7, 0.4, 0.7])
            for (px, py), lab in ((run[0], nm), (run[-1], nm + u"'")):
                bx = _p17_text_box(lab, px, py + 0.8, P17_FS, True, "C")
                sp.text(lab, px, py + 0.8, P17_FS, COL["ink_dark"], bold=True, align="C")
                taken.append(bx)
    # hubs: the icon and the name
    for name, xy in _p17_hubs(log):
        if inR(xy):
            X, Y = T(xy)
            _p17_put(sp, ico_badge("hub", X, Y, 4.0))
            sp.text(name, X + 2.8, Y - P17_FS * 0.35, P17_FS, COL["ink_dark"], bold=True)
            taken.append((X - 2.0, Y - 2.0, X + 2.8 + text_w(name, P17_FS, True), Y + 2.0))
    # numbered badges, one per water space in the window
    nums = []
    for n, code, name, keys in PLANT_SITES:
        at = None
        if code == "ARM":
            if arms:
                at = T(_p17_along(arms[0], 0.5 * sum(math.hypot(q[0] - p[0], q[1] - p[1])
                                                     for p, q in zip(arms[0][:-1], arms[0][1:])))[0])
        else:
            cand = [z for z in zs if z["code"] == code]
            if cand:
                z = max(cand, key=lambda z_: len(z_["ring"]))
                if code == "STRIP":
                    inside = [T(p) for p in z["ring"] if inR(p)]
                    at = inside[len(inside) // 2] if inside else None
                else:
                    at = T(_p17_cen(z["ring"]))
        if at and R[0] + 3.0 <= at[0] <= R[2] - 3.0 and R[1] + 3.0 <= at[1] <= R[3] - 3.0:
            b_ = label_spot(at[0], at[1], 3.8, 3.8, taken, (R[0] + 1.0, R[1] + 1.0, R[2] - 1.0, R[3] - 1.0), (), 0.3,
                            rings=(0.0, 1.5, 3.0, 5.0, 8.0))
            if b_:
                (bx0, by0, bx1, by1), far = b_
                if far:
                    sp.line([at, lp_leader_end(b_[0], at)], COL["ink_dark"], 0.12)
                _p17_badge(sp, n, (bx0 + bx1) / 2.0, (by0 + by1) / 2.0)
                taken.append(b_[0])
                nums.append(n)
    pg.items += _p14_clip_items(sp.items, R)
    pg.poly([rect(*R)], fill=None, stroke=COL["ink2"], lw=0.2)
    # under it: the window's name, the scale bar, "1:den", the north arrow
    yb = R[1] - 4.0
    bb = _p12_bar(pg, R[0], yb, den, P17_BAR.get(den, (0, 20, 50, 100)))
    lab = u"{} · plan · 1:{:,.0f}".format(P17_WIN_NAME[key], den)
    xl = bb[2] + 3.0
    pg.text(lab, xl, yb, P17_FS, COL["ink"], bold=True)
    nd = (T((0.0, 100.0))[0] - T((0.0, 0.0))[0], T((0.0, 100.0))[1] - T((0.0, 0.0))[1])
    nl = math.hypot(*nd) or 1.0
    nb = _p17_north(pg, R[2] - 4.0, yb - 1.0, (nd[0] / nl, nd[1] / nl), 4.0)
    return (min(R[0], bb[0]), min(bb[1], nb[1], yb - 1.5), R[2], R[3]), nums


P17_WIN_NAME = {"A": u"Upstream entry", "B": u"Lower reach"}
P17_CUTS = [("W1", u"F1"), ("F2", u"F2"), ("S4", u"F3"), ("F4", u"F4")]   # the sections of page B: (level cut, name)


def _p17_clip_seg(seg, ring):
    """the parts of the segment seg inside ring (sampled every 1/200 of its length)"""
    (ax, ay), (bx, by) = seg
    out, cur = [], None
    n = 200
    for i in range(n + 1):
        t = i / float(n)
        p = (ax + (bx - ax) * t, ay + (by - ay) * t)
        if _p17_pip(p, ring):
            if cur is None:
                cur = [p, p]
            cur[1] = p
        elif cur is not None:
            out.append(cur)
            cur = None
    if cur is not None:
        out.append(cur)
    return [r for r in out if math.hypot(r[1][0] - r[0][0], r[1][1] - r[0][1]) > 0.5]


def _p17_scatter(sp, Rp, keys, step, k, seed):
    """plants of keys on a jittered grid step mm apart inside the page ring Rp"""
    xs, ys = [p[0] for p in Rp], [p[1] for p in Rp]
    i = 0
    y = min(ys) + step / 2.0
    while y < max(ys):
        x = min(xs) + step / 2.0 * (1 + (i % 2))
        while x < max(xs):
            q = (x + (_p17_rnd(i, seed) - 0.5) * step * 0.4, y + (_p17_rnd(i, seed + 1) - 0.5) * step * 0.4)
            if _p17_pip(q, Rp):
                _p17_plan_plant(sp, keys[i % len(keys)], q[0], q[1], k, seed + i)
            x += step
            i += 1
        y += step


def _p17_offset(P, d):
    """the polyline P (page) moved d mm to its left"""
    out = []
    for i, p in enumerate(P):
        a, b = P[max(i - 1, 0)], P[min(i + 1, len(P) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        out.append((p[0] - dy / L * d, p[1] + dx / L * d))
    return out


def _p17_edge(sp, P, keys, step, k, seed, closed=True):
    """plants of keys every step mm along the page polyline / ring P"""
    pts = list(P) + ([P[0]] if closed else [])
    L = sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(pts[:-1], pts[1:]))
    n = int(L / step)
    for i in range(n):
        (x, y), _ = _p17_along(pts, (i + 0.5) * step)
        _p17_plan_plant(sp, keys[i % len(keys)], x, y, k, seed + i)


def _p17_wetland(sp, ring, T, k, bld):
    """the floodable riverside planting (zone base WP) as bands by distance from the Selinos line: rush and loosestrife
    at the water, willow, tamarisk and chaste tree further out, ash on the dry edge (the section rule of F4)"""
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    i, step = 0, 4.5
    y = min(ys) + step / 2.0
    while y < max(ys):
        x = min(xs) + step / 2.0 * (1 + (i % 2))
        while x < max(xs):
            q = (x + (_p17_rnd(i, 21) - 0.5) * 1.8, y + (_p17_rnd(i, 22) - 0.5) * 1.8)
            if _p17_pip(q, ring) and not any(_p17_pip(q, r) for r in bld):
                d = _p17_line_d(q, P12_SELINOS)
                key = (("soft_rush", "loosestrife")[i % 2] if d < 30.0 else
                       (("willow", "tamarisk", "chaste")[i % 3] if d < 55.0 else "ash"))
                if key in ("willow", "tamarisk", "ash") and i % 2:
                    key = "chaste"
                X, Y = T(q)
                _p17_plan_plant(sp, key, X, Y, k, 300 + i)
            x += step
            i += 1
        y += step


def _p17_win_corners(fit):
    """the four survey corners of a window fitted by _p17_win_fit"""
    w, h, u, v, c, den = fit
    hw, hh = w / 2.0 * den / 1000.0, h / 2.0 * den / 1000.0
    return [((c[0] + a) * u[0] + (c[1] + b) * v[0], (c[0] + a) * u[1] + (c[1] + b) * v[1])
            for a, b in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))]


# ---------------------------------------------------------------- key maps (basemap "topographic", 02 §1)
def _p17_keymap(pg, box, cuts, wins, log):
    """the analysis frame along its long side in box (x0, y0, x1, y1), upstream at the left, the shared basemap in its
    topographic mode, the hubs, and either this page's cut lines ONLY (cuts: [(level cut, name)]) or the plan windows
    (wins: [(name, survey ring)]); a north arrow at its left. Returns its box, or None without basemap data."""
    x0, y0, x1, y1 = box
    fr = basemap_frame()
    fu = _p17_frame_uv()
    if not fr or not fu:
        log.append(u"p.17 key map: no basemap data (run the site board v51+ once)")
        return None
    u, v = fu
    cx, cy = _p17_cen(fr)
    us = [(p[0] - cx) * u[0] + (p[1] - cy) * u[1] for p in fr]
    vs = [(p[0] - cx) * v[0] + (p[1] - cy) * v[1] for p in fr]
    na = 8.0
    den = max((max(us) - min(us)) * 1000.0 / (x1 - x0 - na), (max(vs) - min(vs)) * 1000.0 / (y1 - y0))
    k = 1000.0 / den
    ox, oy = x0 + na - min(us) * k, y1 - max(vs) * k

    def T(p):
        return (ox + ((p[0] - cx) * u[0] + (p[1] - cy) * u[1]) * k, oy + ((p[0] - cx) * v[0] + (p[1] - cy) * v[1]) * k)
    R = (ox + min(us) * k, oy + min(vs) * k, ox + max(us) * k, oy + max(vs) * k)
    sbox = (min(p[0] for p in fr), min(p[1] for p in fr), max(p[0] for p in fr), max(p[1] for p in fr))
    sp = Page(0, 0)

    def text_fn(s, xy, size_mm, hx, bold=False, align="L"):
        sp.text(s, xy[0], xy[1], max(size_mm, FS_MIN), hx, bold=bold, align=(str(align or u"L")[-1:]).upper())   # v7.1: "MC" -> "C"
    try:
        items = list(basemap_items("topographic", box=sbox, split_buildings=True))
        if cuts:
            items += list(basemap_cut_items([(level_ends(cid)[0], level_ends(cid)[1], (nm, nm + u"'"))
                                             for cid, nm in cuts], den, text_mm=FS_MIN))
        sp.poly([rect(*R)], fill=COL["white"])

        def fill_fn(rings, hx, alpha, nonzero):
            sp.poly([r_ for r_ in rings if len(r_) >= 3], fill=hx if alpha is None or alpha >= 0.999 else
                    r28_mix(hx, "FFFFFF", 1.0 - max(0.0, float(alpha))))

        def line_fn(pts, hx, w_mm, dash_mm, alpha):
            d_ = (list(dash_mm) if isinstance(dash_mm, (list, tuple)) else [dash_mm, dash_mm]) if dash_mm else None
            sp.line(pts, hx if alpha is None or alpha >= 0.999 else r28_mix(hx, "FFFFFF", 1.0 - max(0.0, float(alpha))),
                    w_mm, dash=d_)
        basemap_draw(items, T, fill_fn, line_fn, text_fn)
    except Exception as ex:
        log.append(u"p.17 key map not drawn: {}: {}".format(type(ex).__name__, ex))
        return None
    for name, ring in wins or []:
        P = [T(p) for p in ring]
        sp.poly([P], fill=None, stroke=COL["accent"], lw=0.35)
        xs, ys = [p[0] for p in P], [p[1] for p in P]
        sp.text(name, max(xs) + 0.8, max(ys) - FS_MIN, FS_MIN, COL["accent"], bold=True)
    for name, xy in _p17_hubs(log):
        X, Y = T(xy)
        sp.circle(X, Y, 0.7, fill=COL["ink_dark"])
    pg.items += _p14_clip_items(sp.items, R)
    pg.poly([rect(*R)], fill=None, stroke=COL["ink2"], lw=0.2)
    n_ = (u[1], v[1])
    nl = math.hypot(*n_) or 1.0
    nb = _p17_north(pg, R[0] - na / 2.0, R[3] - 7.0, (n_[0] / nl, n_[1] / nl), 3.5)
    return (min(R[0] - na, nb[0]), R[1], R[2], R[3])


# ---------------------------------------------------------------- page A: legend, numbered list, catalogue
def _p17_legend(pg, x, ytop, w, log):
    """drawn samples with plain names, only what the plans draw; returns the bottom y"""
    fs = P17_FS
    y = ytop
    pg.text(u"ON THE PLANS", x, y - fs, fs, COL["ink_dark"], bold=True)
    y -= fs * 1.9
    rows = [("cell", u"lined basin cell: reed, water mint"), ("WD", u"spillway"), ("GR", u"shaded walk"),
            ("WS", u"rain terraces, olive rows"), ("STRIP", u"summer strip"), ("WP", u"wetland planting"),
            ("ARM", u"side arm"), ("cut", u"section line (p.17 sections)"), ("hub", u"hub")]
    if _p17_shade(log):
        rows += [("shade", lab) for _, _, lab in P17_SHADE]
    for i, (kind, lab) in enumerate(rows):
        yy = y - fs * 0.15
        if kind == "cell":
            _p17_put(pg, pla_cell_plan("reed", (x, yy - 1.0, x + 6.0, yy + 2.2), 2.0, 0.15))
        elif kind == "cut":
            pg.line([(x, yy + 0.6), (x + 6.0, yy + 0.6)], COL["ink_dark"], 0.3, dash=[2.4, 0.7, 0.4, 0.7])
        elif kind == "hub":
            _p17_put(pg, ico_badge("hub", x + 3.0, yy + 0.6, 3.6))
        elif kind == "shade":
            col = [c_ for _, c_, l_ in P17_SHADE if l_ == lab][0]
            pg.poly([rect(x, yy - 1.0, x + 6.0, yy + 2.2)], fill=col, alpha=0.6)
        else:
            f_, s_ = P17_ZONE[kind]
            pg.poly([rect(x, yy - 1.0, x + 6.0, yy + 2.2)], fill=f_, stroke=s_, lw=0.12)
        t = lab if kind != "shade" else u"July shade " + lab
        pg.text(t, x + 7.5, y, fs, COL["ink"])
        y -= fs * 1.55
    y -= 0.6
    y = r28_para(pg, x, y + fs * 0.4, w, u"crowns at **true size** for each species", fs, COL["ink2"])
    return y


def _p17_list(pg, x, ytop, w, nums):
    """the numbered water spaces with what grows there (R35), in two columns; returns the bottom y"""
    fs = P17_FS
    items = [s for s in PLANT_SITES if s[0] in nums]
    cw = (w - 6.0) / 2.0
    half = (len(items) + 1) // 2
    low = ytop
    for col, part in enumerate((items[:half], items[half:])):
        y = ytop
        xx = x + col * (cw + 6.0)
        for n, code, name, keys in part:
            _p17_badge(pg, n, xx + 1.8, y - 1.8)
            s_ = u"**{}**: {}".format(name, u", ".join(PLA_SPECIES[k_]["name"].lower() if i_ else PLA_SPECIES[k_]["name"]
                                                       for i_, k_ in enumerate(keys)))
            y = min(y - 3.8, r28_para(pg, xx + 4.6, y + fs * 0.2, cw - 4.6, s_, fs, COL["ink"]) - 0.6)
        low = min(low, y)
    return low


def _p17_foliage(key):
    t = PLA_SPECIES[key].get("foliage") or u""
    if not t or u"not found" in t or u"UNVERIFIED" in t:
        return None
    return t.split(u" (")[0]


def _p17_height(key):
    lo, hi = PLA_SPECIES[key].get("h_range") or (None, None)
    if hi is None:
        return None
    f = lambda v: (u"{:.0f}".format(v) if abs(v - round(v)) < 1e-9 else u"{:.1f}".format(v))
    if lo is None:
        return u"up to {} m".format(f(hi))
    return u"{}-{} m".format(f(lo), f(hi))


P17_WATER_ICON = {"wet": "water", "moist": "drip", "dry": "drought"}
P17_ROLE_ICON = {"clean": "nutrients", "shade": "shade", "hold the bank": "high_water", "scent": "plants",
                 "flower": "plants", "harvest": "olive"}


def _p17_name(key):
    return plant_name(key) if key in PLANTS else u"{} ({})".format(PLA_SPECIES[key]["name"], PLA_SPECIES[key]["turkish"]) \
        if u"UNVERIFIED" not in PLA_SPECIES[key]["turkish"] else PLA_SPECIES[key]["name"]


def _p17_views(pg, key, x, y, w, h):
    """the species' section silhouette (left) and its top-view crown (right) at ONE size factor, in the box (x, y) -
    (x + w, y + h): the two views of one primitive"""
    half = (w - 1.0) / 2.0
    if key in ("reed", "mint"):
        tall = (PLA_SPECIES[key]["h_m"] or 1.0) + P17_BASIN["depth"] + P17_BASIN["kerb_h"]
        kk = min(h / tall, half / 2.4)
        fl = y + 0.2
        rim = fl + (P17_BASIN["depth"]) * kk
        fn = pla_reed_basin if key == "reed" else pla_mint_cell
        _p17_put(pg, fn(x + 0.4, x + half - 0.4, fl, rim, kk, P17_BASIN["kerb_h"], P17_BASIN["kerb_t"],
                        P17_BASIN["media"]))
        _p17_put(pg, pla_cell_plan(key, (x + half + 1.0, y + h / 2.0 - half / 2.0, x + w, y + h / 2.0 + half / 2.0),
                                   kk, P17_BASIN["kerb_t"]))
        return
    hh, cw = _p17_size(key)
    kk = min(h / hh, half / max(cw, 0.1))
    _p17_put(pg, pla_section(key, x + half / 2.0, y, kk, h_m=hh, crown_m=cw))
    _p17_put(pg, pla_plan(key, x + half + 1.0 + half / 2.0, y + h / 2.0, kk, crown_m=cw))


def _p17_card(pg, x, ytop, w, sp_, photo, photos):
    """one catalogue column (R36): photo, the two views, name with its sources, foliage and height, water, role.
    Returns the bottom y."""
    fs = P17_FS
    key = sp_["key"]
    path, credit = photo
    y = ytop
    pg.poly([rect(x, y - PHOTO_H, x + PHOTO_W, y)], fill=C["paper"], stroke=C["faint"], lw=0.2)
    if path:
        photos.append((x, y - PHOTO_H, x + PHOTO_W, y, path))
    y -= PHOTO_H + 1.2
    _p17_views(pg, key, x, y - 15.0, w, 15.0)
    y -= 16.5
    name = _p17_name(key) + u" " + cite(sp_["src"]) + (cite(credit) if credit else u"")
    y = para(pg, x, y, w, name, fs, COL["ink_dark"], bold=True) - 0.4
    fo, ht = _p17_foliage(key), _p17_height(key)
    t = u" · ".join(s_ for s_ in (fo, ht) if s_)
    if t:
        y = para(pg, x, y, w, t, fs, COL["ink"]) - 0.4
    wc, wt = sp_["water"]
    _p17_put(pg, ico_draw(P17_WATER_ICON[wc], x + 1.5, y - 2.45, 3.0))
    y = min(y - 3.3, para(pg, x + 3.6, y, w - 3.6, wt, fs, COL["ink"]) - 0.4)
    ix = x
    for r_ in sp_["role"]:
        _p17_put(pg, ico_draw(P17_ROLE_ICON.get(r_, "plants"), ix + 1.5, y - 2.45, 3.0))
        ix += 3.4
    y = min(y - 3.3, para(pg, ix + 0.4, y, w - (ix - x) - 0.4, u", ".join(sp_["role"]), fs, COL["river_dark"],
                          bold=True) - 0.4)
    return y


def _p17_catalogue(pg, x0, ybot, x1, log, measure=False):
    """the species, wet to dry, one column each, along the foot of page A; bottom-aligned at ybot. Returns its box."""
    sps = [s_ for k_ in P17_CAT for s_ in SPECIES if s_["key"] == k_]
    n = len(sps)
    gap = max(0.6, min(3.0, (x1 - x0 - n * PHOTO_W) / max(n - 1, 1)))
    w = PHOTO_W
    if "photos" not in _P17_MEMO:
        state = {}
        out = []
        for s_ in sps:
            p_ = (None, None)
            if PHOTO_ON[0] and s_["key"] in PLANTS:
                path, credit, why = plant_photo_of(s_["key"], log, state)
                p_ = (path, credit)
                if not path:
                    log.append(u"p.17 catalogue: no photo of {} ({})".format(s_["key"], why or u"not loaded"))
            elif s_["key"] not in PLANTS:
                log.append(u"p.17 catalogue: {} has no photo entry in common/plant_photos.py PLANTS".format(s_["key"]))
            out.append(p_)
        _P17_MEMO["photos"] = out
    photos = _P17_MEMO["photos"]
    hmax = max(-_p17_card(Page(0, 0), 0.0, 0.0, w, s_, (None, None), []) for s_ in sps)
    if measure:
        return (x0, ybot, x0 + n * w + (n - 1) * gap, ybot + hmax)
    ytop = ybot + hmax
    for i, (s_, p_) in enumerate(zip(sps, photos)):
        _p17_card(pg, x0 + i * (w + gap), ytop, w, s_, p_, PHOTOS)
    return (x0, ybot, x0 + n * w + (n - 1) * gap, ytop)


def p17_page(pg, box, opt, log):
    """page A (wb_plants): the conclusion and the key strip on top, the two plan windows with their legend, the
    numbered water spaces, the species catalogue along the foot. Returns [(crop id, bbox, den)]."""
    if _P17_MEMO.get("run") != id(pg):                  # a new run reads its data afresh
        _P17_MEMO.clear()
        _P17_MEMO["run"] = id(pg)
    x0, y0, x1, y1 = box
    W = min(x1 - x0, P17_W)
    x1 = x0 + W
    n0 = len(pg.items)
    G = 5.0
    LG = 56.0                                           # the legend column, mm
    # the plan windows: one standard scale for both, the first at which they fit beside the legend
    pa, pb = _p17_win_pts("A", log), _p17_win_pts("B", log)
    pick = None
    for den in P17_DENS:
        fa, fb = _p17_win_fit(pa, den), _p17_win_fit(pb, den)
        if fa[0] + fb[0] + 2 * G + LG <= W and max(fa[1], fb[1]) <= 104.0:
            pick = (den, fa, fb)
            break
    if pick is None:
        den = P17_DENS[-1]
        pick = (den, _p17_win_fit(pa, den), _p17_win_fit(pb, den))
        log.append(u"WARNING p.17: the plan windows do not fit at any standard scale; drawn at 1:{:,.0f}".format(den))
    den, fa, fb = pick
    # top row: the key strip (the frame, the two windows, the hubs) and the conclusion
    KH = 22.0
    kb = _p17_keymap(pg, (x0, y1 - KH, x0 + 5.38 * KH + 8.0, y1), None,
                     [(u"A", _p17_win_corners(fa)), (u"B", _p17_win_corners(fb))], log)
    xs = (kb[2] if kb else x0) + 6.0
    yc = r28_para(pg, xs, y1, x1 - xs, P17_SAY, P17_HEAD, COL["ink_dark"])
    ytop = min(y1 - KH, yc) - 6.0
    # the windows, side by side, the legend at the right
    pg.text(u"A", x0, ytop + 1.2, P17_HEAD, COL["accent"], bold=True)
    ba, na = _p17_window(pg, x0, ytop, "A", den, fa, log)
    pg.text(u"B", ba[2] + G, ytop + 1.2, P17_HEAD, COL["accent"], bold=True)
    bb_, nb = _p17_window(pg, ba[2] + G, ytop, "B", den, fb, log)
    ly = _p17_legend(pg, x1 - LG, ytop, LG, log)
    ybot = min(ba[1], bb_[1], ly) - 4.0
    # the numbered water spaces under the windows, the catalogue at the foot
    cb = _p17_catalogue(pg, x0, y0, x1, log, measure=True)
    yl = _p17_list(pg, x0, ybot, x1 - x0, set(na) | set(nb))
    if yl - 4.0 < cb[3]:
        log.append(u"WARNING p.17: the catalogue runs into the list by {:.0f} mm".format(cb[3] - yl + 4.0))
    _p17_catalogue(pg, x0, y0, x1, log)
    log.append(u"p.17 page A: plans 1:{:,.0f} ({} and {}), catalogue {} species, photos {}".format(
        den, u"north up" if fa[2] == (1.0, 0.0) else u"along the frame", u"north up" if fb[2] == (1.0, 0.0) else
        u"along the frame", len(P17_CAT), sum(1 for p_ in _P17_MEMO.get("photos", []) if p_[0])))
    return [("wb_plants", items_bbox(pg.items[n0:]), den)]


# ---------------------------------------------------------------- page B: the sections at 1:500
P17_WALL_T = 0.60                    # DSİ wall thickness drawn (no source; as p.04-05 and p.13 draw it)
P17_F1_BED = (22.1, 54.7)            # F1 on the W1 line: the bed between the walls, m from the SW end (the W1 width,
#                                      placed so the zone base's strip, 24.1-28.9 m on the line, lies in it)
P17_F1_STRIP = (24.1, 28.9)
P17_F2_RANGE = (36.0, 178.0)         # the part of F2 drawn, m along it
P17_F2_WALLS = (44.6, 67.7)          # F2: the bed between the DSİ walls (sample_cut.py: the survey's stream lines)
P17_F2_CELLS = [("reed", 77.9, 83.9), ("reed", 84.4, 90.4), ("mint", 90.9, 96.9)]   # basin cells in the zone WT
P17_F2_TERR = 7.0                    # rain terrace tread, m (the olive row spacing, plants.py PLA_CROPS)
P17_F4_RANGE = (12.0, 140.0)
P17_F4_BED = (73.7, 113.9)           # F4: the bed between the survey's two stream lines, m along the cut
P17_F3_RANGE = (-42.0, 48.0)         # F3 on S4: m across from the bed's low point (p.14's coordinates)
P17_GRAVEL = 0.50


def _p17_gz(prof, t):
    """the ground of a profile [(t, z)] at t (at a vertical step the upper one)"""
    best = None
    for (a, za), (b, zb) in zip(prof[:-1], prof[1:]):
        if b > a and a - 1e-9 <= t <= b + 1e-9:
            z = za + (zb - za) * (t - a) / (b - a)
            best = z if best is None else max(best, z)
    if best is None:
        return prof[0][1] if t < prof[0][0] else prof[-1][1]
    return best


def _p17_wet(prof, z, t0, t1, step=0.25):
    out, a = [], None
    n = int((t1 - t0) / step)
    for i in range(n + 1):
        t = t0 + i * step
        if _p17_gz(prof, t) < z - 1e-6:
            if a is None:
                a = t
        elif a is not None:
            out.append((a, t))
            a = None
    if a is not None:
        out.append((a, t1))
    return out


def _p17_section(spec, log):
    """one section at 1:500 from spec (see the builders), on its own Page: origin = (t0, zb); returns the Page.
    spec: rng, zb, prof [(t, z)], fills [(ring, material)], water [ring], plants [(key, t, seed)], cells [(kind, t0, t1,
    floor, rim)], beyond [(kind, t0, t1, floor, rim)], beyond_plants, people [(pose, t, facing, params)], zones
    [(t0, t1, text, chip colour or None)], levels [(z, text, colour, bold)], qlines [z], arrows [(pts, colour)],
    ends (left, right), caption."""
    k = 1000.0 / P17_SEC_DEN
    t0, t1 = spec["rng"]
    zb = spec["zb"]
    prof = spec["prof"]
    fs = P17_FS

    def X(t):
        return (t - t0) * k

    def Y(z):
        return (z - zb) * k

    def P(pts):
        return [(X(t), Y(z)) for t, z in pts]
    pg = Page(0, 0)
    W = X(t1)
    clip = (0.0, -1e9, W, 1e9)

    def put(ring_tz, mat):
        r_ = _p14_clip_ring(P(ring_tz), clip)
        if r_:
            _p17_put(pg, sct_hatch_fill(r_, mat, k, None, 0.1))
    # what stands beyond the cut, pushed back behind a veil
    if spec.get("beyond") or spec.get("beyond_plants"):
        bp = Page(0, 0)
        for kind, a, b, fl, rim in spec.get("beyond", []):
            fn = pla_reed_basin if kind == "reed" else pla_mint_cell
            _p17_put(bp, fn(X(a), X(b), Y(fl), Y(rim), k, P17_BASIN["kerb_h"], P17_BASIN["kerb_t"], P17_BASIN["media"]))
        for key, t, seed in spec.get("beyond_plants", []):
            _p17_sec_plant(bp, key, X(t), Y(_p17_gz(prof, t)), k, seed, beyond=True)
        pg.items += _p14_clip_items(bp.items, (0.0, Y(spec.get("beyond_z", zb)), W, 1e9))
        bb = items_bbox(bp.items) if bp.items else None
        if bb:
            pg.poly([rect(bb[0], bb[1], bb[2], bb[3])], fill=COL["white"], alpha=0.5)
    put(prof + [(t1, zb), (t0, zb)], "earth")
    for ring, mat in spec.get("fills", []):
        put(ring, mat)
    for ring in spec.get("water", []):
        r_ = _p14_clip_ring(P(ring), clip)
        if r_:
            pg.poly([r_], fill=P17_WATER, alpha=0.85)
            top = max(p[1] for p in r_)
            xs = [p[0] for p in r_ if abs(p[1] - top) < 1e-6]
            if len(xs) >= 2:
                pg.line([(min(xs), top), (max(xs), top)], C["w3"], 0.2)
    pg.line(P(prof), COL["ink_dark"], 0.3)
    for kind, a, b, fl, rim in spec.get("cells", []):
        fn = pla_reed_basin if kind == "reed" else pla_mint_cell
        _p17_put(pg, fn(X(a), X(b), Y(fl), Y(rim), k, P17_BASIN["kerb_h"], P17_BASIN["kerb_t"], P17_BASIN["media"]))
    for pts, colour in spec.get("arrows", []):
        arrow(pg, P(pts), colour, 0.3, 1.6, [0.9, 0.6])
    for key, t, seed in spec.get("plants", []):
        if t0 + 0.3 <= t <= t1 - 0.3:
            _p17_sec_plant(pg, key, X(t), Y(_p17_gz(prof, t)), k, seed)
    for pose, t, face, par in spec.get("people", []):
        if t0 + 0.8 <= t <= t1 - 0.8:
            par = dict(par or {})
            zf = par.pop("z", None)
            _p17_fig(pg, pose, X(t), Y(zf if zf is not None else _p17_gz(prof, t)), k, face, **par)
    for z in spec.get("qlines", []):
        for a, b in _p17_wet(prof, z, t0, t1):
            pg.line([(X(a), Y(z)), (X(b), Y(z))], C["w4"], 0.18, dash=[1.2, 0.7])
    # the zones on vertical lines over the drawing (R34), staggered on two rows where they meet
    top = items_bbox(pg.items)[3] + 3.0
    rows_end = [-1e9, -1e9]
    for a, b, text, chip in spec.get("zones", []):
        a, b = max(a, t0), min(b, t1)
        if b - a < 0.5:
            continue
        xa, xb = X(a), X(b)
        xm = (xa + xb) / 2.0
        cw = (fs * 1.7 + 0.8) if chip else 0.0
        tw = text_w(text, fs, True) + cw
        lx = min(max(xm - tw / 2.0, 0.0), W - tw)
        row = 0 if lx > rows_end[0] + 1.5 else 1
        if row == 1 and lx <= rows_end[1] + 1.5:
            lx = rows_end[1] + 1.5
        rows_end[row] = lx + tw
        yl = top + row * fs * 1.6
        for xv in (xa, xb):
            pg.line([(xv, yl - 0.6), (xv, Y(_p17_gz(prof, (xv / k) + t0)) + 0.4)], COL["ink2"], 0.1, dash=[0.5, 0.5])
        pg.line([(xa, yl - 0.6), (xb, yl - 0.6)], COL["ink2"], 0.12)
        if chip:
            pg.poly([rect(lx, yl - 0.2, lx + fs * 1.7, yl + fs * 0.95)], fill=BAND_COL.get(chip, chip))
            pg.text(chip, lx + fs * 0.85, yl + 0.1, fs, "FFFFFF", bold=True, align="C")
        pg.text(text, lx + cw, yl, fs, COL["ink_dark"], bold=True)
    ytop = top + (2 if rows_end[1] > -1e8 else 1) * fs * 1.6
    l_, r_ = spec.get("ends", (u"", u""))
    pg.text(l_, 0.0, ytop + 0.8, P17_HEAD, COL["ink_dark"], bold=True)
    pg.text(r_, W, ytop + 0.8, P17_HEAD, COL["ink_dark"], bold=True, align="R")
    # the levels at the right
    ent = [(Y(z), t, colr, bold) for z, t, colr, bold in spec.get("levels", [])]
    if ent:
        level_ladder(pg, ent, W + 0.8, W + 4.0, fs, lo=Y(zb))
    # under it: the caption and the scale bar
    yc = -fs * 1.6
    pg.text(spec["caption"], 0.0, yc, fs, COL["ink_dark"], bold=True)
    r28_scale_bar(pg, text_w(spec["caption"], fs, True) + 5.0, yc - 0.3, P17_SEC_DEN, fs, False)
    return pg


def _p17_lv_text(z, what):
    return u"{} {}".format(u_level(z), what)


def _p17_f2(log):
    """F2 across the stream, the spillway, the lined reed basins, the shaded walk and the rain terraces (LEVELS F2)"""
    bed, wt = _p17_lv("F2", "bed"), _p17_lv("F2", "top", "NE")
    q100, q500 = _p17_lv("F2", "q100"), _p17_lv("F2", "q500")
    g = _p17_ground("F2")
    t0, t1 = P17_F2_RANGE
    ws, wn = P17_F2_WALLS
    wtk = P17_WALL_T
    zone = dict((c_, (a_, b_)) for c_, a_, b_ in level_cut("F2").get("zones") or [])
    st0, st1 = zone.get("STRIP", (49.2, 54.0))
    sp0, sp1 = 68.3, zone.get("WD", (54.1, 75.4))[1]
    bt0, bt1 = zone.get("WT", (77.7, 97.1))
    gr0, gr1 = zone.get("GR", (115.6, 135.6))
    te0, te1 = zone.get("WS", (135.6, 177.6))
    gz = lambda t: _p17_interp(g, t)
    zp = round(max(gz(bt0 + i) for i in range(int(bt1 - bt0) + 1)), 2)     # the basin platform
    floor = zp - P17_BASIN["depth"]
    prof = []
    # south-west: the ground held up to the wall top behind the DSİ wall, the survey further out
    t, side = ws - wtk, []
    while t >= t0 - 1e-9:
        side.append((t, wt if gz(t) < wt and all(p[1] == wt for p in side) else gz(t)))
        t -= 2.0
    if side[-1][0] > t0:
        side.append((t0, wt if gz(t0) < wt and all(p[1] == wt for p in side) else gz(t0)))
    prof += side[::-1]
    prof += [(ws - wtk, wt), (ws, wt), (ws, bed), (st0, bed), (st0, bed - STRIP_DEPTH), (st1, bed - STRIP_DEPTH),
             (st1, bed), (wn, bed), (wn, wt), (wn + wtk, wt)]
    # the spillway trough from the basins down to the wall top, then the basin platform and the cells
    prof += [(sp0 + 0.3, wt), (sp0 + 0.3, wt - 0.45), (sp1 - 0.3, wt - 0.30), (sp1 - 0.3, wt), (sp1, wt),
             (bt0 - 0.3, zp), (bt0, zp)]
    cells = []
    for kind, a, b in P17_F2_CELLS:
        prof += [(a, zp), (a, floor + P17_BASIN["media"]), (b, floor + P17_BASIN["media"]), (b, zp)]
        cells.append((kind, a, b, floor, zp))
    prof += [(bt1, zp)]
    t = math.ceil(bt1 + 1.0)
    while t < te0:
        prof.append((t, gz(t)))
        t += 2.0
    # the rain terraces: level treads P17_F2_TERR wide at the mean ground of each, stone retaining walls
    fills, plants, people = [], [], []
    prev = gz(te0)
    prof.append((te0, prev))
    s, i = te0, 0
    while s + P17_F2_TERR <= te1 + 0.1:
        lv = round(sum(gz(s + j * 0.5) for j in range(int(P17_F2_TERR * 2) + 1)) / (int(P17_F2_TERR * 2) + 1), 2)
        prof += [(s, lv), (s + P17_F2_TERR, lv)]
        fills.append(([(s - 0.4, min(prev, lv) - 0.4), (s, min(prev, lv) - 0.4), (s, max(prev, lv)),
                       (s - 0.4, max(prev, lv))], "stone"))
        plants += [("rosemary", s + 0.8, 70 + i), ("lavender", s + 1.7, 80 + i), ("olive", s + 4.2, 90 + i)]
        prev, s, i = lv, s + P17_F2_TERR, i + 1
    prof.append((min(t1, s + 0.6), gz(min(t1, s + 0.6))))
    if prof[-1][0] < t1:
        prof.append((t1, gz(t1)))
    fills += [([(ws - wtk, wt), (ws, wt), (ws, bed - P17_GRAVEL), (ws - wtk, bed - P17_GRAVEL)], "stone"),
              ([(wn, wt), (wn + wtk, wt), (wn + wtk, bed - P17_GRAVEL), (wn, bed - P17_GRAVEL)], "stone"),
              ([(ws, bed), (st0 - 0.15, bed), (st0 - 0.15, bed - P17_GRAVEL), (ws, bed - P17_GRAVEL)], "gravel"),
              ([(st1 + 0.15, bed), (wn, bed), (wn, bed - P17_GRAVEL), (st1 + 0.15, bed - P17_GRAVEL)], "gravel"),
              ([(st0 - 0.15, bed), (st0 - 0.15, bed - STRIP_DEPTH - 0.15), (st1 + 0.15, bed - STRIP_DEPTH - 0.15),
                (st1 + 0.15, bed), (st1, bed), (st1, bed - STRIP_DEPTH), (st0, bed - STRIP_DEPTH), (st0, bed)],
               "concrete"),
              ([(sp0, wt), (sp0 + 0.3, wt), (sp0 + 0.3, wt - 0.45), (sp1 - 0.3, wt - 0.30), (sp1 - 0.3, wt),
                (sp1, wt), (sp1, wt - 0.5), (sp0, wt - 0.65)], "concrete"),
              ([(gr0 + 6.0, gz(gr0 + 6.0)), (gr1 - 6.0, gz(gr1 - 6.0)), (gr1 - 6.0, gz(gr1 - 6.0) - 0.2),
                (gr0 + 6.0, gz(gr0 + 6.0) - 0.2)], "concrete")]
    water = [[(st0, bed - STRIP_DEPTH), (st1, bed - STRIP_DEPTH), (st1, bed), (st0, bed)],
             [(sp0 + 0.3, wt - 0.45), (sp1 - 0.3, wt - 0.30), (sp1 - 0.3, wt - 0.15), (sp0 + 0.3, wt - 0.25)]]
    plants += [("loosestrife", st0 - 0.9, 1), ("soft_rush", st1 + 0.7, 2), ("soft_rush", wn - 0.8, 3)]
    t = bt1 + 2.0
    j = 0
    while t < gr0 - 1.0:
        plants.append(("lavender", t, 30 + j))
        t += 1.2
        j += 1
    plants += [("plane", gr0 + 3.0, 40), ("plane", gr1 - 3.0, 41)]
    people += [("walk", ws - 4.0, 1, None), ("wade", (st0 + st1) / 2.0, -1, {"depth_m": STRIP_DEPTH, "z": bed - STRIP_DEPTH}),
               ("adult_child", (gr0 + gr1) / 2.0 + 1.0, -1, {"child_h": 1.15}),
               ("olive", te0 + P17_F2_TERR * 2 + 5.4, -1, {"branch_h": 1.9})]
    # the spillway falls over the wall into the bed
    arrows = [([(sp0 + 0.2, wt - 0.2), (sp0 - 0.8, wt - 1.6), (sp0 - 1.2, bed + 0.4)], C["w3"])]
    zones = [(t0, ws - wtk, u"SW BANK", None), (ws, wn, u"STREAM BED · summer strip", None),
             (sp0, sp1, u"SPILLWAY", None), (bt0, bt1, u"REED BASINS · lined", None),
             (bt1, gr0, u"DRY BANK", None), (gr0, gr1, u"SHADED WALK", None), (te0, te1, u"RAIN TERRACES", None)]
    levels = [(bed, _p17_lv_text(bed, u"bed"), C["w4"], False), (q100, _p17_lv_text(q100, u"Q100"), C["w4"], False),
              (q500, _p17_lv_text(q500, u"Q500"), C["w4"], True), (wt, _p17_lv_text(wt, u"DSİ wall"), COL["ink"], False),
              (zp, _p17_lv_text(zp, u"basin rim"), COL["ink"], False)]
    return dict(rng=(t0, t1), zb=bed - P17_GRAVEL - 1.0, prof=prof, fills=fills, water=water, plants=plants,
                cells=cells, people=people, qlines=[q100, q500], arrows=arrows, zones=zones, levels=levels,
                ends=(u"F2", u"F2'"), caption=u"F2 · rain terraces, reed basins and the stream at the upstream entry")


def _p17_f4(log):
    """F4 across the side arm, the bank top, the widened bed with its strip and the street (LEVELS F4)"""
    bed = _p17_lv("F4", "bed")
    q100, q500 = _p17_lv("F4", "q100"), _p17_lv("F4", "q500")
    g = _p17_ground("F4")
    gz = lambda t: _p17_interp(g, t)
    t0, t1 = P17_F4_RANGE
    zone = dict((c_, (a_, b_)) for c_, a_, b_ in level_cut("F4").get("zones") or [])
    a0, a1 = zone.get("ARM", (27.0, 33.0))
    b0, b1 = P17_F4_BED
    st0, st1 = 86.7, 90.9                                # the zone base's strip on F4 (ZONE_COPY A-NIL-STRIP-2)
    zf = gz((a0 + a1) / 2.0) - 0.80                      # the side arm's floor: a 0.80 m channel (drawing value)
    zs = gz((st0 + st1) / 2.0)
    prof = []
    t = t0
    while t < a0:
        prof.append((t, gz(t)))
        t += 2.0
    prof += [(a0, gz(a0)), (a0 + 0.8, zf), (a1 - 0.8, zf), (a1, gz(a1))]
    t = math.ceil(a1 + 1.0)
    while t < st0:
        prof.append((t, gz(t)))
        t += 2.0
    prof += [(st0, zs), (st0, zs - STRIP_DEPTH), (st1, zs - STRIP_DEPTH), (st1, zs)]
    t = math.ceil(st1 + 1.0)
    while t < t1:
        prof.append((t, gz(t)))
        t += 2.0
    prof.append((t1, gz(t1)))
    fills = [([(b0, gz(b0)), (st0 - 0.15, zs), (st0 - 0.15, zs - P17_GRAVEL), (b0, gz(b0) - P17_GRAVEL)], "gravel"),
             ([(st1 + 0.15, zs), (b1, gz(b1)), (b1, gz(b1) - P17_GRAVEL), (st1 + 0.15, zs - P17_GRAVEL)], "gravel"),
             ([(st0 - 0.15, zs), (st0 - 0.15, zs - STRIP_DEPTH - 0.15), (st1 + 0.15, zs - STRIP_DEPTH - 0.15),
               (st1 + 0.15, zs), (st1, zs), (st1, zs - STRIP_DEPTH), (st0, zs - STRIP_DEPTH), (st0, zs)], "concrete"),
             ([(126.6, gz(126.6)), (132.0, gz(132.0)), (132.0, gz(132.0) - 0.3), (126.6, gz(126.6) - 0.3)], "concrete")]
    water = [[(st0, zs - STRIP_DEPTH), (st1, zs - STRIP_DEPTH), (st1, zs), (st0, zs)],
             [(a0 + 0.8 * 0.6, zf + 0.3), (a0 + 0.8, zf), (a1 - 0.8, zf), (a1 - 0.8 * 0.6, zf + 0.3)]]
    plants = [(key, t, 500 + i) for i, (key, t) in enumerate(P17_F4_PLANTS)]
    people = [("walk", 19.0, 1, None), ("watch", a1 + 1.6, -1, None),
              ("wade", (st0 + st1) / 2.0, 1, {"depth_m": STRIP_DEPTH, "z": zs - STRIP_DEPTH}),
              ("bike", 129.0, -1, None)]
    zones = [(t0, a0 - 1.0, u"OPEN GROUND", None), (a0 - 1.0, a1 + 1.0, u"SIDE ARM", None),
             (a1 + 1.0, 59.0, u"BANK TOP", None), (59.0, b0, u"SW BANK", None), (b0, b1, u"WIDENED BED · strip", None),
             (b1, 126.6, u"NE BANK", None), (126.6, t1, u"STREET", None)]
    levels = [(bed, _p17_lv_text(bed, u"bed"), C["w4"], False), (q100, _p17_lv_text(q100, u"Q100"), C["w4"], False),
              (q500, _p17_lv_text(q500, u"Q500"), C["w4"], True)]
    return dict(rng=(t0, t1), zb=bed - P17_GRAVEL - 1.0, prof=prof, fills=fills, water=water, plants=plants,
                people=people, qlines=[q100, q500], zones=zones, levels=levels, ends=(u"F4", u"F4'"),
                caption=u"F4 · the side arm and the widened stream, lower reach")


def _p17_f1(log):
    """F1 on the W1 line: the walled stream at the inflow, its strip with rush edges, the reed basins beyond"""
    bed, wt = _p17_lv("W1", "bed"), _p17_lv("W1", "top", "NE")
    q100, q500 = _p17_lv("W1", "q100"), _p17_lv("W1", "q500")
    L = _p17_lv("W1", "length_m")
    t0, t1 = 0.0, L
    ws, wn = P17_F1_BED
    st0, st1 = P17_F1_STRIP
    wtk = P17_WALL_T
    prof = [(t0, wt), (ws - wtk, wt), (ws, wt), (ws, bed), (st0, bed), (st0, bed - STRIP_DEPTH),
            (st1, bed - STRIP_DEPTH), (st1, bed), (wn, bed), (wn, wt), (wn + wtk, wt), (t1, wt)]
    fills = [([(ws - wtk, wt), (ws, wt), (ws, bed - P17_GRAVEL), (ws - wtk, bed - P17_GRAVEL)], "stone"),
             ([(wn, wt), (wn + wtk, wt), (wn + wtk, bed - P17_GRAVEL), (wn, bed - P17_GRAVEL)], "stone"),
             ([(st1 + 0.15, bed), (wn, bed), (wn, bed - P17_GRAVEL), (st1 + 0.15, bed - P17_GRAVEL)], "gravel"),
             ([(ws, bed), (st0 - 0.15, bed), (st0 - 0.15, bed - P17_GRAVEL), (ws, bed - P17_GRAVEL)], "gravel"),
             ([(st0 - 0.15, bed), (st0 - 0.15, bed - STRIP_DEPTH - 0.15), (st1 + 0.15, bed - STRIP_DEPTH - 0.15),
               (st1 + 0.15, bed), (st1, bed), (st1, bed - STRIP_DEPTH), (st0, bed - STRIP_DEPTH), (st0, bed)],
              "concrete")]
    water = [[(st0, bed - STRIP_DEPTH), (st1, bed - STRIP_DEPTH), (st1, bed), (st0, bed)]]
    plants = [(key, t, 600 + i) for i, (key, t) in enumerate(P17_F1_PLANTS)]
    bx0 = wn + wtk + 1.2
    beyond = [("reed", bx0, bx0 + 5.6, wt - P17_BASIN["depth"], wt),
              ("mint", bx0 + 6.2, min(t1 - 0.5, bx0 + 11.0), wt - P17_BASIN["depth"], wt)]
    people = [("walk", 11.0, 1, None), ("watch", wn + wtk + 0.6, -1, None)]
    arrows = [([((ws + wn) / 2.0 + 6.0, bed + 0.5), (wn - 1.0, wt - 0.6), (bx0 + 1.0, wt + 0.9)], C["w3"])]
    zones = [(t0, ws - wtk, u"SW BANK · plane shade", None), (ws, wn, u"STREAM BED · strip", None),
             (wn + wtk, t1, u"REED BASINS beyond", None)]
    levels = [(bed, _p17_lv_text(bed, u"bed"), C["w4"], False), (q100, _p17_lv_text(q100, u"Q100"), C["w4"], False),
              (q500, _p17_lv_text(q500, u"Q500"), C["w4"], True), (wt, _p17_lv_text(wt, u"DSİ wall"), COL["ink"], False)]
    return dict(rng=(t0, t1), zb=bed - P17_GRAVEL - 1.0, prof=prof, fills=fills, water=water, plants=plants,
                beyond=beyond, beyond_z=wt, people=people, qlines=[q100, q500], arrows=arrows, zones=zones, levels=levels,
                ends=(u"F1", u"F1'"), caption=u"F1 · the stream at the inflow, the reed basins beyond")


def _p17_f3(log):
    """F3 on the S4 line (p.14's own cut and planting, _p14_geo / P14_PLANTS): the planting bands by the days water
    covers the ground (PLANT_BANDS, RWS), both banks, in full leaf"""
    G = _p14_geo()
    t0, t1 = P17_F3_RANGE
    prof = [(t0, _p14_surf(t0))] + [p for p in G["prof"] if t0 < p[0] < t1] + [(t1, _p14_surf(t1))]
    bed, sfl, shelf, zn = G["bed"], G["sfl"], G["shelf"], G["zones"]
    st0, st1 = zn["strip"]
    lt = P14_LINER
    e0, p0 = zn["steps"]
    p2 = zn["bike"][1]
    w0, w1 = P14_WALK
    tt0, tt1 = zn["terrace"]
    fills = [([(G["b0"], bed), (st0 - lt, bed), (st0 - lt, bed - P14_GRAVEL), (G["b0"], bed - P14_GRAVEL)], "gravel"),
             ([(st1 + lt, bed), (G["b1"], bed), (G["b1"], bed - P14_GRAVEL), (st1 + lt, bed - P14_GRAVEL)], "gravel"),
             ([(tt0, shelf), (tt1, shelf), (tt1, shelf - 0.3), (tt0, shelf - 0.3)], "gravel"),
             ([(st0 - lt, bed), (st0 - lt, sfl - lt), (st1 + lt, sfl - lt), (st1 + lt, bed), (st1, bed), (st1, sfl),
               (st0, sfl), (st0, bed)], "concrete"),
             ([(w0, shelf), (w1, shelf), (w1, shelf - 0.2), (w0, shelf - 0.2)], "concrete"),
             ([p for p in G["prof"] if e0 - 1e-9 <= p[0] <= p0 + 1e-9 and p[1] >= shelf - 1e-9] +
              [(p0, P14_PROM - 0.35), (e0, shelf - 0.35)], "concrete"),
             ([(p0, P14_PROM), (p2, P14_PROM), (p2, P14_PROM - P14_SLAB), (p0, P14_PROM - P14_SLAB)], "concrete")]
    water = [[(st0, sfl), (st1, sfl), (st1, bed), (st0, bed)]]
    plants = [(key, s, 700 + i) for i, (key, s, h, cw) in enumerate(P14_PLANTS)]
    people = [("wade", (st0 + st1) / 2.0, 1, {"depth_m": bed - sfl, "z": sfl}),
              ("sit_step", e0 + 3 * P14_STEPS[1] + 0.3, -1, {"seat_h": G["rise"]}), ("walk", (p0 + zn["prom"][1]) / 2.0,
                                                                                    1, None)]
    # the bands: the ground's band code every 0.25 m, merged into runs; each run named on the vertical lines
    runs = []
    s = t0
    while s <= t1 + 1e-9:
        c_ = _p14_band_code(s, _p14_surf(s))
        if runs and runs[-1][0] == c_:
            runs[-1][2] = s
        else:
            runs.append([c_, s, s])
        s += 0.25
    bn = dict((b_[0], (b_[1], b_[3])) for b_ in PLANT_BANDS)
    zones, seen = [], set()
    for c_, a, b in runs:
        if b - a < 3.0:
            continue
        name, days = bn.get(c_, (u"", u""))
        lab = (name.split(u" (")[0].split(u" / ")[0].lower() if c_ not in seen else u"") + \
            (u" · " + days.replace(u" d/yr", u" d").replace(u"–", u"-").split(u";")[0] if c_ not in seen else u"")
        zones.append((a, b + 0.25, lab.strip(u" ·"), c_))
        seen.add(c_)
    levels = [(bed, _p17_lv_text(bed, u"bed"), C["w4"], False),
              (G["q100"], _p17_lv_text(G["q100"], u"Q100"), C["w4"], False),
              (G["q500"], _p17_lv_text(G["q500"], u"Q500"), C["w4"], True),
              (P14_PROM, _p17_lv_text(P14_PROM, u"promenade"), COL["ink"], False)]
    return dict(rng=(t0, t1), zb=G["base"], prof=prof, fills=fills, water=water, plants=plants, people=people,
                qlines=[G["q100"], G["q500"]], zones=zones, levels=levels, ends=(u"F3", u"F3'"),
                caption=u"F3 · the planting bands of the widened stream " + cite(P15_BAND_SRC))


# ---------------------------------------------------------------- page B: the calendar, giant reed, the page
P17_LEAF = "C9D7A6"                  # in leaf
P17_MONTHS = u"JFMAMJJASOND"


def _p17_calendar(pg, x, ytop, w, log):
    """the species of the catalogue on ONE month axis (R36): a bar where it is in leaf, a darker one where it flowers,
    a tick where its flower heads are cut; sourced months only (plants.py pla_months). Returns the bottom y."""
    fs = P17_FS
    lw_ = max(text_w(PLA_SPECIES[k_]["name"], fs) for k_ in P17_CAT) + 1.5
    cw = (w - lw_) / 12.0
    rh = fs * 1.3
    pg.text(u"THE YEAR OF EACH SPECIES", x, ytop - P17_HEAD, P17_HEAD, COL["ink_dark"], bold=True)
    y = ytop - P17_HEAD - 2.0
    for m in range(12):
        pg.text(P17_MONTHS[m], x + lw_ + (m + 0.5) * cw, y - fs, fs, COL["ink2"], bold=True, align="C")
    y -= fs * 1.5
    y0 = y
    for i, key in enumerate(P17_CAT):
        mo = pla_months(key)
        yy = y - i * rh
        pg.text(PLA_SPECIES[key]["name"], x, yy - rh + fs * 0.35, fs, COL["ink"])
        for m in mo.get("leaf") or []:
            pg.poly([rect(x + lw_ + (m - 1) * cw, yy - rh + 0.25, x + lw_ + m * cw, yy - 0.25)], fill=P17_LEAF)
        for m in mo.get("bloom") or []:
            pg.poly([rect(x + lw_ + (m - 1) * cw + 0.2, yy - rh * 0.72, x + lw_ + m * cw - 0.2, yy - rh * 0.28)],
                    fill=P14_BLOOM)
        for m in mo.get("cut") or []:
            xm = x + lw_ + (m - 0.5) * cw
            pg.line([(xm - 0.9, yy - rh + 0.4), (xm + 0.9, yy - 0.4)], COL["accent"], 0.3)
            pg.line([(xm - 0.9, yy - 0.4), (xm + 0.9, yy - rh + 0.4)], COL["accent"], 0.3)
    yb = y - len(P17_CAT) * rh
    for m in range(13):
        pg.line([(x + lw_ + m * cw, y0 + 0.4), (x + lw_ + m * cw, yb)], COL["faint"], 0.08)
    y = yb - fs * 1.5
    xx = x
    for kind, lab in (("leaf", u"in leaf"), ("bloom", u"in flower"), ("cut", u"flower heads cut")):
        if kind == "leaf":
            pg.poly([rect(xx, y - 0.3, xx + 4.0, y + fs * 0.8)], fill=P17_LEAF)
        elif kind == "bloom":
            pg.poly([rect(xx, y + 0.1, xx + 4.0, y + fs * 0.5)], fill=P14_BLOOM)
        else:
            pg.line([(xx + 1.1, y - 0.2), (xx + 2.9, y + fs * 0.8)], COL["accent"], 0.3)
            pg.line([(xx + 1.1, y + fs * 0.8), (xx + 2.9, y - 0.2)], COL["accent"], 0.3)
        pg.text(lab, xx + 5.0, y, fs, COL["ink"])
        xx += 5.0 + text_w(lab, fs) + 4.0
    return y - fs * 0.6


def _p17_remove(pg, x, ytop, w, log):
    """giant reed: its photo crossed, take it out and why (02 §5: only marked remove). Returns the bottom y."""
    fs = P17_FS
    key, words, src = SPECIES_REMOVE
    path, credit = None, None
    if PHOTO_ON[0] and key in PLANTS:
        path, credit, why = plant_photo_of(key, log, {})
    pg.poly([rect(x, ytop - PHOTO_H, x + PHOTO_W, ytop)], fill=C["paper"], stroke=C["faint"], lw=0.2)
    if path:
        PHOTOS.append((x, ytop - PHOTO_H, x + PHOTO_W, ytop, path))
    _p17_put(pg, ico_cross(x + PHOTO_W - 3.5, ytop - 3.5, 5.0, COL["accent"]))
    tx = x + PHOTO_W + 2.0
    y = para(pg, tx, ytop, w - PHOTO_W - 2.0, _p17_name(key) + u" " + cite(src) + (cite(credit) if credit else u""),
             fs, COL["ink_dark"], bold=True)
    y = r28_para(pg, tx, y - 0.4, w - PHOTO_W - 2.0, words, fs, COL["accent"])
    return min(y, ytop - PHOTO_H)


def _p17_place(pg, part, x, ytop):
    """a section Page put with its top-left at (x, ytop), at 1:1 (its scale is its own); returns its box"""
    b = items_bbox(part.items)
    dx, dy = x - b[0], ytop - b[3]
    pg.items += xform(part.items, 1.0, dx, dy)
    return (x, ytop - (b[3] - b[1]), x + b[2] - b[0], ytop)


def p17b_page(pg, box, opt, log):
    """page B (wb_plants_b): the conclusion and the key map (F1-F4 only) on top; F2 with giant reed beside it; F4 with
    the calendar beside it; F1 and F3 side by side. Every section at 1:500. Returns [(crop id, bbox, den)]."""
    if _P17_MEMO.get("run") != id(pg):                  # a new run reads its data afresh
        _P17_MEMO.clear()
        _P17_MEMO["run"] = id(pg)
    x0, y0, x1, y1 = box
    W = min(x1 - x0, P17_W)
    x1 = x0 + W
    n0 = len(pg.items)
    G = 5.0
    parts = {}
    for nm, fn in (("F2", _p17_f2), ("F4", _p17_f4), ("F1", _p17_f1), ("F3", _p17_f3)):
        try:
            parts[nm] = _p17_section(fn(log), log)
        except Exception as ex:
            log.append(u"WARNING p.17 section {} not drawn: {}: {}".format(nm, type(ex).__name__, ex))
            import traceback as _tb
            log.append(_tb.format_exc()[-600:])
    size = dict((nm, items_bbox(p_.items)) for nm, p_ in parts.items())
    wh = dict((nm, (b[2] - b[0], b[3] - b[1])) for nm, b in size.items())
    # top: the conclusion, the key map with this page's cuts only
    KW = 120.0
    kb = _p17_keymap(pg, (x1 - KW, y1 - KW / 5.38, x1, y1), P17_CUTS, None, log)
    yc = r28_para(pg, x0, y1, (kb[0] if kb else x1) - x0 - G, P17B_SAY, P17_HEAD, COL["ink_dark"])
    y = min(yc, kb[1] if kb else y1) - 5.0
    # row 1: F2, giant reed at its right
    if "F2" in parts:
        b2 = _p17_place(pg, parts["F2"], x0, y)
        yr = _p17_remove(pg, b2[2] + G, y, x1 - b2[2] - G, log)
        y = min(b2[1], yr) - 5.0
    # row 2: F4, the calendar at its right
    if "F4" in parts:
        b4 = _p17_place(pg, parts["F4"], x0, y)
        xcal = b4[2] + G
    else:
        b4, xcal = (x0, y, x0, y), x0
    yk = _p17_calendar(pg, xcal, y, x1 - xcal, log)
    y = min(b4[1], yk) - 5.0
    # row 3: F1 and F3 side by side, the room between them shared
    w1 = wh.get("F1", (0.0, 0.0))[0]
    w3 = wh.get("F3", (0.0, 0.0))[0]
    gap = max(G, W - w1 - w3)
    low = y
    if "F1" in parts:
        low = min(low, _p17_place(pg, parts["F1"], x0, y)[1])
    if "F3" in parts:
        low = min(low, _p17_place(pg, parts["F3"], x0 + w1 + gap if w1 else x0, y)[1])
    if low < y0 or w1 + w3 + G > W:
        log.append(u"WARNING p.17 page B: {:.0f} x {:.0f} mm, more than the {:.0f} x {:.0f} mm of the box".format(
            max(W, w1 + w3 + G), y1 - low, W, y1 - y0))
    log.append(u"p.17 page B: sections {} at 1:{:,.0f}".format(u", ".join(sorted(parts)), P17_SEC_DEN))
    return [("wb_plants_b", items_bbox(pg.items[n0:]), P17_SEC_DEN)]
