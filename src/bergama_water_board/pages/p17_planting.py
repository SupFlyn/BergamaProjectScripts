# p.17 planting and water (water board v6; revision 30 Oct 2026, T7: booklet p16 and p17). Two booklet pages:
#   page A (p17_page, crop wb_plants, booklet p16 "Which plant goes where"): two plan windows at one standard scale on
#        the shared basemap (M3 "detailed": streets, M11 buildings with roof ridges, M5 water), farms and orchards as one
#        field texture and one symbol per area (D7), the water spaces of the zone base, the planting as species
#        areas in wet-to-dry bands (R2-C _p17_drift_plan, R12-R14: drifts, overlapping crowns, no rows), July shade, the
#        four section lines of page B from the cut registry (W1, F2, S4, F4), the hubs and the numbered water spaces;
#        beside them the key map (M4: study-area outline + both windows) and the legend; under them the numbered list
#        and the species catalogue (photo, detailed section and plan from M6, foliage, height, water, role).
#   page B (p17b_page, crops wb_plants_b = wb_plants_b_a, booklet p17): the four cuts W1, F2, S4, F4
#        at 1:500 (D6), each with its programmes (bike lane, walking path, viewing terrace, bridge crossing, walking in
#        the water), people doing them (M7: 1.75 m at the cut plane, D9 layers behind), the planting groups as mixed
#        groups with what each does (G9), the background ground, houses and trees per depth layer under the D8 sky
#        (M8), the bed filled with water at the average yearly flow and the Q100 / Q500 lines (M5), every level from
#        the cut registry (M8); key map (M4: all four cuts + outline), giant reed: remove, the year of each species,
#        the materials. D1 a (round 2): style a only, in its cell; callouts "Element: reason" per zone and group.
# build_board calls P17_TITLE, P17B_TITLE, p17_page(pg, box, opt, log), p17b_page(pg, box, opt, log); each returns
# [(crop id, bbox, scale denominator)].

P17_TITLE = u"PLANTING AND WATER · where each plant goes around the water spaces"
P17B_TITLE = u"PLANTING AND WATER IN SECTION · four cuts, the species and their year"
P17_W = 377.0                        # the most a page takes, mm (the booklet's A3 panel at 1:1)
P17_CAT = ("reed", "mint", "soft_rush", "loosestrife", "willow", "tamarisk", "chaste", "ash", "plane", "olive",
           "rosemary", "lavender")   # the catalogue, wet to dry: every species the two pages draw
P17_DENS = (1000.0, 2000.0, 2500.0, 5000.0)   # the plan windows: the first standard scale at which both fit
P17_WIN_GAP = 12.0                   # mm at least between the plan windows A and B (Aras 31 Oct: a clear gap)
P17_BAR = {1000.0: (0, 10, 20, 50), 2000.0: (0, 20, 50, 100), 2500.0: (0, 20, 50, 100), 5000.0: (0, 50, 100, 200)}
P17_SEC_DEN = 500.0                  # every section
P17_FS, P17_HEAD = FS_MIN, 3.4       # label and heading sizes, mm
P17_WATER = "8CBBC8"                 # the summer strip (the low-flow channel) in plan
P17_ZONE = {"WT": ("CBEDE5", "8DB8AF"), "WD": ("C1D3DB", "889EA8"), "GR": ("EEEADD", "C9C3B0"),
            "WS": ("EEE8D6", "C9BFA6"), "WP": ("E6EEDD", "B9C6A2"), "ARM": ("B9D7DE", "5D7F8D"),
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
# plan planting (G9, M6 niches): the species of each water space and of the stream banks, wet to dry; the band
# position t (0 = the water's edge, 1 = dry upper ground) of the spaces planted as one band; the bank band's width
P17_MIX = {"WD": ("soft_rush", "loosestrife"), "GR": ("plane", "ash", "chaste"), "WS": ("olive", "rosemary", "lavender"),
           "WP": ("soft_rush", "loosestrife", "willow", "tamarisk", "chaste", "ash"),
           "ARM": ("soft_rush", "loosestrife", "willow"),
           "BANK": ("soft_rush", "loosestrife", "willow", "tamarisk", "chaste", "ash", "plane", "olive", "rosemary",
                    "lavender")}
P17_MIX_T = {"WD": 0.06, "GR": 0.50, "WS": 0.86}
P17_BAND_M = 35.0                    # the stream-bank planting reaches this far from the water, m (design: the corridor)
P17_WP_M = 60.0                      # the wetland's wet-to-dry band, m from the water (its depth across, zone base WP)
P17_ARM_BAND = 10.0                  # the side arm's planting either side of its water, m (drawing value)
P17_KEYCOL = "8B3A3F"                # key maps: cut lines and windows (COL accent)
P17_WHY = {"wind": u"cuts the wind", "noise": u"cuts street noise", "shade": u"gives shade",
           "corridor": u"ecological corridor", "cleaning": u"cleans the water", "perception": u"helps perception"}
P17_WHY_PLACE = ("wind", "noise")    # purposes the design gives a group by where it stands (street edge, open top),
#                                      not a species property: printed without a species tag (handover: unverified)
# R2-C (31 Oct, R12-R14): the plans draw the planting as species AREAS in four wet-to-dry bands along the water; a
# band's edges lie halfway between the niche centres (plants.py PLA_NICHE) of neighbouring bands (_p17_band_t)
P17_BANDS = (("soft_rush", "loosestrife", "rush"), ("willow", "tamarisk"), ("ash", "plane", "chaste"),
             ("olive", "rosemary", "lavender", "stone_pine"))
P17_SHORT = {"plane": u"plane", "ash": u"ash", "willow": u"willow", "tamarisk": u"tamarisk", "chaste": u"chaste tree",
             "olive": u"olive", "rosemary": u"rosemary", "lavender": u"lavender", "loosestrife": u"loosestrife",
             "soft_rush": u"soft rush", "rush": u"sharp rush", "stone_pine": u"stone pine"}
P17_CO = FS_MIN                       # section callouts: circle and key size (shared callout style, p11 / p12 / p17)


# ---------------------------------------------------------------- small helpers
def _p17_put(pg, shapes):
    """house shapes (alpha, text and the style a cutout images) on a Page (water.py shp_put)"""
    shp_put(pg, shapes)


def _p17_size(key):
    """(height, crown) m a species is drawn at on its own: plants.py's sourced drawing size, the same in the plans and
    the catalogue"""
    sp = PLA_SPECIES[key]
    return sp["h_m"], sp["crown_m"]


def _p17_area(R):
    return abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(R, R[1:] + R[:1]))) / 2.0


def _p17_hit(R, box):
    xs, ys = [p[0] for p in R], [p[1] for p in R]
    return not (max(xs) < box[0] or min(xs) > box[2] or max(ys) < box[1] or min(ys) > box[3])


def _p17_move(items, dx, dy):
    """page items moved by (dx, dy) at 1:1, the cutout images too (xform leaves "image" items out)"""
    out = []
    for it in items:
        if it[0] == "image":
            c = it[8] if len(it) > 8 else None
            out.append(("image", it[1] + dx, it[2] + dy, it[3], it[4], it[5], it[6], it[7],
                        (c[0] + dx, c[1] + dy, c[2] + dx, c[3] + dy) if c else None))
        else:
            out += xform([it], 1.0, dx, dy)
    return out


def _p17_bb(items):
    """items_bbox with the cutout images (cut to their clip)"""
    b = items_bbox([it for it in items if it[0] != "image"])
    bs = [b] if b != (0.0, 0.0, 0.0, 0.0) else []
    for it in items:
        if it[0] == "image":
            r = (it[1], it[2], it[1] + it[3], it[2] + it[4])
            c = it[8] if len(it) > 8 and it[8] else r
            bs.append((max(r[0], c[0]), max(r[1], c[1]), min(r[2], c[2]), min(r[3], c[3])))
    if not bs:
        return b
    return (min(q[0] for q in bs), min(q[1] for q in bs), max(q[2] for q in bs), max(q[3] for q in bs))


def _p17_clip(shapes, r):
    """house shapes cut to the rectangle r = (x0, y0, x1, y1); a cutout image keeps its picture, clipped at r"""
    out = []
    for s_ in shapes:
        t = s_[0]
        if t == "poly":
            c = _p14_clip_ring(list(s_[1]), r)
            if c:
                out.append(("poly", c) + tuple(s_[2:]))
        elif t == "line":
            for run in _p14_clip_line(list(s_[1]), r):
                out.append(("line", run) + tuple(s_[2:]))
        elif t == "text":
            if r[0] <= s_[2] <= r[2] and r[1] <= s_[3] <= r[3]:
                out.append(s_)
        elif t == "image":
            x_, y_, w_, h_ = s_[1:5]
            if x_ < r[2] and x_ + w_ > r[0] and y_ < r[3] and y_ + h_ > r[1]:
                out.append(tuple(s_[:8]) + ((max(r[0], x_), max(r[1], y_), min(r[2], x_ + w_), min(r[3], y_ + h_)),))
    return out


def _p17_shp_bb(shapes):
    xs, ys = [], []
    for s_ in shapes:
        if s_[0] in ("poly", "line"):
            xs += [p[0] for p in s_[1]]
            ys += [p[1] for p in s_[1]]
        elif s_[0] == "image":
            c = s_[8] if len(s_) > 8 and s_[8] else (s_[1], s_[2], s_[1] + s_[3], s_[2] + s_[4])
            xs += [c[0], c[2]]
            ys += [c[1], c[3]]
    return (min(xs), min(ys), max(xs), max(ys)) if xs else (0.0, 0.0, 0.0, 0.0)


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


def _p17_ring_index(rings, cell):
    """rings (page mm) bucketed by the grid cells their boxes touch, so a point-in-any-ring test stays local"""
    idx = {}
    for R_ in rings:
        if len(R_) < 3:
            continue
        xs, ys = [p[0] for p in R_], [p[1] for p in R_]
        bb = (min(xs), min(ys), max(xs), max(ys))
        for i in range(int(math.floor(bb[0] / cell)), int(math.floor(bb[2] / cell)) + 1):
            for j in range(int(math.floor(bb[1] / cell)), int(math.floor(bb[3] / cell)) + 1):
                idx.setdefault((i, j), []).append((bb, R_))
    return idx


def _p17_in(idx, cell, p):
    for bb, R_ in idx.get((int(math.floor(p[0] / cell)), int(math.floor(p[1] / cell))), ()):
        if bb[0] <= p[0] <= bb[2] and bb[1] <= p[1] <= bb[3] and _p17_pip(p, R_):
            return True
    return False


def _p17_edge_index(rings, cell):
    """the edges of several rings (page mm) bucketed by grid cell, for water.py _wat_near_edge"""
    idx = {}
    for R_ in rings:
        if len(R_) >= 3:
            for key_, segs in _wat_edge_index(list(R_), cell).items():
                idx.setdefault(key_, []).extend(segs)
    return idx


def _p17_band_t():
    """the band edges on the wet-to-dry scale t (0 the water's edge .. 1 dry ground): halfway between the last niche
    centre of one P17_BANDS band and the first of the next (plants.py PLA_NICHE), so no new number"""
    out = []
    for a, b in zip(P17_BANDS[:-1], P17_BANDS[1:]):
        out.append(0.5 * (max(PLA_NICHE[k_][0] for k_ in a if k_ in PLA_NICHE) +
                          min(PLA_NICHE[k_][0] for k_ in b if k_ in PLA_NICHE)))
    return out


def _p17_drift_plan(ring, k, tf, mix, seed, density=1.0, avoid=None, max_n=3000):
    """G9 planting in plan as R12-R14 draw it: species AREAS in wet-to-dry bands along the water. t = tf(x, y) (0 the
    water's edge .. 1 dry ground, > 1 nothing) puts a point in its band (P17_BANDS, edges _p17_band_t); each band is
    cut into drifts around irregular centres (5-16 m plus two crowns of the lead species across: plants.py PLA_GROUP
    group_m, a drawing rule), each drift led by one species with a second mixed in and, at its edges, the species of
    the neighbouring band whose niche reaches there (plants.py _pla_pick): interpenetrating, never rows. Crowns
    overlap (trunks 35-75 % of the two crowns apart: PLA_GROUP step), sizes vary (PLA_GROUP size inside the sourced
    range), no straight evenly spaced line (plants.py _pla_rowlike). Each drift is drawn as its area first (the lead
    species' tone, a fine edge: the band edges follow the water), then the low layer, then the crowns, tall on top.
    ring and avoid: page mm. Returns (shapes, placed [(key, x, y, crown_m)])."""
    keys = [k_ for k_ in mix if k_ in PLA_NICHE]
    if not keys or len(ring) < 3:
        return [], []
    edges = _p17_band_t()
    rnd = _pla_rng(seed * 13 + 3)
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    bx0, by0, bw, bh = min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)
    area = _p17_area(ring)
    pools = [[k_ for k_ in keys if k_ in b_] for b_ in P17_BANDS]

    def band(t):
        return sum(1 for e in edges if t > e)

    def free(x, y):
        return _p17_pip((x, y), ring) and not any(_p17_pip((x, y), a) for a in (avoid or ()))

    def crown(key):
        return PLA_SPECIES[key]["crown_m"]
    g0, g1 = PLA_GROUP["group_m"]
    drifts = dict((b, []) for b in range(len(P17_BANDS)))      # band -> [(x, y, r mm, lead, second)]

    def nearest(b, x, y):
        best, bd = None, None
        for d_ in drifts[b]:
            q = math.hypot(x - d_[0], y - d_[1]) / d_[2]
            if bd is None or q < bd:
                best, bd = d_, q
        return best, bd
    r_small = (0.5 * g0 + min(crown(k_) for k_ in keys)) * k
    for _i in range(int(min(6000, 12.0 * area / (math.pi * r_small * r_small) + 40))):
        x, y = bx0 + rnd() * bw, by0 + rnd() * bh
        if not free(x, y):
            continue
        t = tf(x, y)
        if t > 1.0:
            continue
        b = band(t)
        if not pools[b]:
            continue
        nb, q = nearest(b, x, y)
        if nb is not None and q < 0.9:
            continue
        cand = [k_ for k_ in pools[b] if nb is None or k_ != nb[3] or len(pools[b]) == 1]
        lead = cand[int(rnd() * len(cand)) % len(cand)]
        other = [k_ for k_ in pools[b] if k_ != lead] or \
            [k_ for bb in (b - 1, b + 1) if 0 <= bb < len(pools) for k_ in pools[bb]]
        second = other[int(rnd() * len(other)) % len(other)] if other else None
        r = (0.5 * (g0 + (g1 - g0) * rnd()) + crown(lead)) * k
        drifts[b].append((x, y, r, lead, second))
    sh = []
    # the areas: each drift's ground, ray by ray out to its band edge, its neighbour drift or the planted ring
    for b, ds in drifts.items():
        for d_ in ds:
            def inside(p, d_=d_, b=b):
                if not free(p[0], p[1]):
                    return False
                t = tf(p[0], p[1])
                return t <= 1.0 and band(t) == b and nearest(b, p[0], p[1])[0] is d_
            pts = []
            for i in range(40):
                a = 2.0 * math.pi * i / 40.0
                u = (math.cos(a), math.sin(a))
                lo, hi = 0.0, d_[2]
                if inside((d_[0] + u[0] * hi, d_[1] + u[1] * hi)):
                    lo = hi
                else:
                    for _j in range(6):
                        m = 0.5 * (lo + hi)
                        if inside((d_[0] + u[0] * m, d_[1] + u[1] * m)):
                            lo = m
                        else:
                            hi = m
                pts.append((d_[0] + u[0] * lo, d_[1] + u[1] * lo))
            if _p17_area(pts) > 0.5:
                fc = PLA_SPECIES[d_[3]]["colours"]["fill"]
                sh.append(("poly", pts, _sec_mix(fc, SEC["paper"], 0.72), _sec_mix(fc, SEC["paper"], 0.35), 0.1))
    # the plants: dart throwing per layer, each species from its drift (lead 62 %, second 24 %, the band's niche rest)
    lo_s, hi_s = PLA_GROUP["step"]
    placed = {True: [], False: []}
    total = 0
    for canopy in (True, False):
        ks_c = [k_ for k_ in keys if _pla_canopy(k_) == canopy]
        if not ks_c:
            continue
        cs = max(crown(k_) for k_ in ks_c) * k * PLA_GROUP["size"][1]
        grid = {}
        r_typ = sum(crown(k_) for k_ in ks_c) / len(ks_c) / 2.0 * k
        for _i in range(int(min(40000, 8.0 * density * area / (math.pi * r_typ * r_typ) + 50))):
            if total >= max_n:
                break
            x, y = bx0 + rnd() * bw, by0 + rnd() * bh
            if not free(x, y):
                continue
            t = tf(x, y)
            if t > 1.0:
                continue
            d_ = nearest(band(t), x, y)[0]
            u = rnd()
            key = None
            if d_ is not None and u < 0.62:
                key = d_[3]
            elif d_ is not None and u < 0.86:
                key = d_[4]
            else:
                key = _pla_pick(t, rnd, keys, None, canopy)
            if key is None or _pla_canopy(key) != canopy:
                alt = [q for q in ((d_[3], d_[4]) if d_ is not None else ()) if q and _pla_canopy(q) == canopy]
                key = alt[0] if alt else None
            if key is None:
                continue
            h, w = _pla_group_size(key, rnd)
            r = w / 2.0 * k
            s_ = lo_s + (hi_s - lo_s) * rnd()
            ci, cj = int(math.floor(x / cs)), int(math.floor(y / cs))
            near = [e for i in (ci - 1, ci, ci + 1) for j in (cj - 1, cj, cj + 1) for e in grid.get((i, j), ())]
            if any(math.hypot(e[0] - x, e[1] - y) < s_ * (r + e[2]) for e in near):
                continue
            if _pla_rowlike((x, y), [(e[0], e[1]) for e in near], 3.0 * cs):
                continue
            e = (x, y, r, key, h)
            placed[canopy].append(e)
            grid.setdefault((ci, cj), []).append(e)
            total += 1
    out = []
    for canopy in (False, True):
        for i, (x, y, r, key, h) in enumerate(sorted(placed[canopy], key=lambda e: e[4])):   # tall crowns on top
            part = pla_plan(key, x, y, k, crown_m=2.0 * r / k, seed=seed + i * 3 + (7 if canopy else 0))
            if canopy:
                part = [(s_[0], s_[1], s_[2], s_[3], s_[4], 1.0) if s_[0] == "poly" and s_[2] else s_ for s_ in part]
            sh += part
            out.append((key, x, y, 2.0 * r / k))
    return sh, out


def _p17_window(pg, x0, ytop, key, den, fit, log):
    """one plan window, its top-left at (x0, ytop): farms and orchards (D7), the basemap (M11 buildings, M5 water),
    the water spaces, July shade, the planting as mixed scatters wet to dry (G9), the four section lines, the hubs and
    the numbered badges; frame, scale bar, name and north arrow under it. Returns (bbox, numbers, {code: species})."""
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
    Rr = [(R[0], R[1]), (R[2], R[1]), (R[2], R[3]), (R[0], R[3])]
    sp = Page(0, 0)
    sp.poly([rect(*R)], fill=COL["white"])
    D = basemap_load(log=log)
    L = (D or {}).get("layers") or {}
    # farms and orchards (D7 a): one field texture and one representative symbol in the middle of each area
    fields = []
    lc = L.get("lc") or {}
    farm = list(lc.get("farmland", [])) + [z_["rings"] for z_ in L.get("zones", []) if z_.get("kind") == "agri"]
    for crop, groups in (("olive", lc.get("orchard", [])), ("maize", farm)):
        for g in groups:
            if not g or len(g[0]) < 3 or not _p17_hit(g[0], sb):
                continue
            Pc = _p14_clip_ring([T(p) for p in g[0]], R)
            if not Pc or _p17_area(Pc) < 4.0:
                continue
            fields.append(Pc)
            sh = pla_field_tile(Pc, k, crop=crop, seed=len(fields))
            if _p17_area(Pc) < 140.0:                    # too small for its symbol: the texture alone
                sh = [sh[0]] + [s_ for s_ in sh[1:] if s_[0] == "line" and s_[2] == PLA_ROW]
            _p17_put(sp, sh)
    items = []
    if D:
        try:
            items = basemap_items("detailed", {"trees": False, "green": False, "contours": False, "fields": False,
                                               "buildings": "plan"}, box=sb, D=D, split_buildings=True, scale_den=den)
            _p17_basemap_into(sp, items, T)
        except Exception as ex:
            log.append(u"p.17 plan {}: basemap not drawn: {}: {}".format(key, type(ex).__name__, ex))
    water = [[T(p) for p in r_] for r_ in basemap_water_rings(items)]
    bld = [[T(p) for p in R_] for b in L.get("buildings", []) for R_ in b["rings"][:b.get("np", len(b["rings"]))]
           if len(R_) >= 3 and _p17_hit(R_, sb)]
    streets = [[T(p) for p in g[0]] for g in L.get("street_areas", []) if g and len(g[0]) >= 3 and _p17_hit(g[0], sb)]
    zs = [z for z in _p17_zones() if any(inR(p) for p in z["ring"])]
    arms = [a for a in _p17_arms(log) if any(inR(p) for p in a)]
    widen = [r for r in _p17_widen(log) if any(inR(p) for p in r)]
    for r in widen:
        sp.poly([[T(p) for p in r]], fill=P17_ZONE["WIDEN"][0], stroke=P17_ZONE["WIDEN"][1], lw=0.1)
    for z in zs:                                         # the water spaces, flat (planting comes after the shade)
        if z["code"] == "STRIP":                         # the low-flow channel: deeper water, no outline (G8)
            sp.poly([[T(p) for p in z["ring"]]], fill=P17_ZONE["STRIP"][0], alpha=0.55)
        elif z["code"] in P17_ZONE and z["code"] != "WT":
            f_, s_ = P17_ZONE[z["code"]]
            sp.poly([[T(p) for p in z["ring"]]], fill=f_, stroke=s_, lw=0.12)
    arm_bands = []
    for a in arms:
        P = [T(p) for p in a]
        arm_bands.append(_p14_band(P, 2.0 * P17_ARM_W * k))
        sp.poly([arm_bands[-1]], fill=P17_ZONE["ARM"][0], stroke=P17_ZONE["ARM"][1], lw=0.12)
    # July shade on the bed and the water spaces (5 m cells, three classes)
    sh = _p17_shade(log)
    spaces = [[Ti(*p) for p in r_] for r_ in water] + [z["ring"] for z in zs] + widen
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
    # the planting (G9, M6): lined basin cells; each space a mixed scatter at its band; the side arms and the stream
    # banks wet to dry by the distance to the water. Plants never stand in water, buildings, streets or fields.
    cell = 6.0
    wet = water + [[T(p) for p in z["ring"]] for z in zs if z["code"] in ("STRIP", "WD")] + arm_bands
    widx = _p17_edge_index(wet, cell)
    wet_in = _p17_ring_index(wet, cell)
    bld_in = _p17_ring_index(bld, cell)
    placed, taken = {}, []

    def note(code, pl):
        s_ = placed.setdefault(code, [])
        for q in pl:
            if q[0] not in s_:
                s_.append(q[0])
    for i, z in enumerate(zs):
        Rp = [T(p) for p in z["ring"]]
        code = z["code"]
        try:
            if code == "WT":
                cz, au, av, (a0, a1), _ = _p17_axis(Rp)
                cuts = [a0 + (a1 - a0) * f for f in (1.0 / 3.0, 2.0 / 3.0)]
                cl_ = []
                for j, kind in enumerate(("reed", "reed", "mint")):
                    rr = Rp
                    if j > 0:
                        rr = _p17_half(rr, (cz[0] + au[0] * cuts[j - 1], cz[1] + au[1] * cuts[j - 1]), au)
                    if rr and j < 2:
                        rr = _p17_half(rr, (cz[0] + au[0] * cuts[j], cz[1] + au[1] * cuts[j]), (-au[0], -au[1]))
                    if rr:
                        cl_.append((kind, rr))
                for kind, rr in cl_:
                    _p17_put(sp, pla_cell_plan(kind, rr, k, P17_BASIN["kerb_t"]))
                note("WT", [("reed",), ("mint",)])
            elif code in P17_MIX_T:
                if code == "WS":                         # the terrace edges along the contours, 7 m apart
                    cz, au, av, (a0, a1), (b0, b1) = _p17_axis(Rp)
                    bb = b0 + 7.0 * k
                    while bb < b1 - 1e-6:
                        seg = [(cz[0] + au[0] * a0 * 1.2 + av[0] * bb, cz[1] + au[1] * a0 * 1.2 + av[1] * bb),
                               (cz[0] + au[0] * a1 * 1.2 + av[0] * bb, cz[1] + au[1] * a1 * 1.2 + av[1] * bb)]
                        for run in _p17_clip_seg(seg, Rp):
                            sp.line(run, "8C8170", 0.3)
                        bb += 7.0 * k
                t_ = P17_MIX_T[code]
                shp, pl = _p17_drift_plan(Rp, k, lambda x_, y_, t_=t_: t_, list(P17_MIX[code]), 40 + 7 * i, density=0.9)
                _p17_put(sp, shp)
                note(code, pl)
            elif code == "WP":
                band = P17_WP_M * k

                def t_wp(x_, y_):
                    p_ = (x_, y_)
                    if _p17_in(wet_in, cell, p_) or _p17_in(bld_in, cell, p_):
                        return 9.0
                    return min(1.0, _wat_near_edge(widx, cell, p_, band)[0] / band)
                shp, pl = _p17_drift_plan(Rp, k, t_wp, list(P17_MIX["WP"]), 60 + 7 * i, density=0.9)
                _p17_put(sp, shp)
                note(code, pl)
            if code != "STRIP":
                taken.append(Rp)
        except Exception as ex:
            log.append(u"p.17 plan {}: {} not planted: {}: {}".format(key, code, type(ex).__name__, ex))
    for i, a in enumerate(arms):                         # the side arm: rushes and loosestrife at its water, willow out
        P = [T(p) for p in a]
        ring = _p14_band(P, 2.0 * (P17_ARM_W + P17_ARM_BAND) * k)

        def t_arm(x_, y_, P=P):
            p_ = (x_, y_)
            if _p17_in(bld_in, cell, p_):
                return 9.0
            return 0.45 * max(0.0, _p17_line_d(p_, P) - P17_ARM_W * k) / (P17_ARM_BAND * k)
        try:
            shp, pl = _p17_drift_plan(ring, k, t_arm, list(P17_MIX["ARM"]), 90 + i, density=0.9,
                                      avoid=[arm_bands[i]])
            _p17_put(sp, shp)
            note("ARM", pl)
            taken.append(ring)
        except Exception as ex:
            log.append(u"p.17 plan {}: side arm not planted: {}: {}".format(key, type(ex).__name__, ex))
    # the stream banks: P17_BAND_M wide, wet to dry, wherever the ground is open
    blk = _p17_ring_index(bld + streets + fields + taken, cell)
    band = P17_BAND_M * k

    def t_bank(x_, y_):
        p_ = (x_, y_)
        if _p17_in(wet_in, cell, p_) or _p17_in(blk, cell, p_):
            return 9.0
        d_ = _wat_near_edge(widx, cell, p_, band)[0]
        return d_ / band if d_ < band - 1e-9 else 9.0
    try:
        shp, pl = _p17_drift_plan(Rr, k, t_bank, list(P17_MIX["BANK"]), 7 if key == "A" else 8, density=0.8)
        _p17_put(sp, shp)
        note("BANK", pl)
    except Exception as ex:
        log.append(u"p.17 plan {}: stream banks not planted: {}: {}".format(key, type(ex).__name__, ex))
    # the section lines of page B (cut registry: W1, F2, S4, F4), dash-dot, a view-direction triangle at each end (the
    # way page B looks: toward the ground _p17_topo draws behind the cut), the names on the other side
    taken_l = []
    for cid in P17_CUTS:
        nm = level_name(cid)
        a, b = level_ends(cid)
        La = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
        O, V = T(a), T((a[0] - (b[1] - a[1]) / La, a[1] + (b[0] - a[0]) / La))
        vl = math.hypot(V[0] - O[0], V[1] - O[1]) or 1.0
        vd = ((V[0] - O[0]) / vl, (V[1] - O[1]) / vl)
        for run in _p14_clip_line([T(a), T(b)], (R[0] + 3.0, R[1] + 3.0, R[2] - 3.0, R[3] - 3.0)):
            sp.line(run, COL["ink_dark"], 0.3, dash=[2.4, 0.7, 0.4, 0.7])
            for (px, py), lab in ((run[0], nm), (run[-1], nm + u"'")):
                tri = [(px + vd[0] * 2.2, py + vd[1] * 2.2), (px - vd[1] * 0.9, py + vd[0] * 0.9),
                       (px + vd[1] * 0.9, py - vd[0] * 0.9)]
                sp.poly([tri], fill=COL["ink_dark"])
                lx, ly = px - vd[0] * 2.2, py - vd[1] * 2.2 - P17_FS * CAP / 2.0
                sp.text(lab, lx, ly, P17_FS, COL["ink_dark"], bold=True, align="C")
                taken_l += [_p17_text_box(lab, lx, ly, P17_FS, True, "C"),
                            (min(q[0] for q in tri), min(q[1] for q in tri), max(q[0] for q in tri),
                             max(q[1] for q in tri))]
    # hubs: the icon and the name
    for name, xy in _p17_hubs(log):
        if inR(xy):
            X, Y = T(xy)
            _p17_put(sp, ico_badge("hub", X, Y, 4.0))
            sp.text(name, X + 2.8, Y - P17_FS * 0.35, P17_FS, COL["ink_dark"], bold=True)
            taken_l.append((X - 2.0, Y - 2.0, X + 2.8 + text_w(name, P17_FS, True), Y + 2.0))
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
            b_ = label_spot(at[0], at[1], 3.8, 3.8, taken_l, (R[0] + 1.0, R[1] + 1.0, R[2] - 1.0, R[3] - 1.0), (), 0.3,
                            rings=(0.0, 1.5, 3.0, 5.0, 8.0))
            if b_:
                (bx0, by0, bx1, by1), far = b_
                if far:
                    sp.line([at, lp_leader_end(b_[0], at)], COL["ink_dark"], 0.12)
                _p17_badge(sp, n, (bx0 + bx1) / 2.0, (by0 + by1) / 2.0)
                taken_l.append(b_[0])
                nums.append(n)
    pg.items += _p17_clip_items(sp.items, R)
    pg.poly([rect(*R)], fill=None, stroke=COL["ink2"], lw=0.2)
    # under it: the scale bar, the window's name and scale, the north arrow
    yb = R[1] - 4.0
    bb = _p12_bar(pg, R[0], yb, den, P17_BAR.get(den, (0, 20, 50, 100)))
    lab = u"{} · plan · 1:{:,.0f}".format(P17_WIN_NAME[key], den)
    pg.text(lab, bb[2] + 3.0, yb, P17_FS, COL["ink"], bold=True)
    nd = (T((0.0, 100.0))[0] - T((0.0, 0.0))[0], T((0.0, 100.0))[1] - T((0.0, 0.0))[1])
    nl = math.hypot(*nd) or 1.0
    nx, ny = R[2] - 4.0, yb - 1.0
    if bb[2] + 3.0 + text_w(lab, P17_FS, True) + 1.5 > nx - 5.0:    # the label reaches it (G3): top right, inside
        nx, ny = R[2] - 4.5, R[3] - 10.0
        pg.poly([rect(nx - 3.5, ny - 3.5, nx + 3.5, ny + 8.5)], fill=COL["white"], stroke=COL["ink2"], lw=0.1)
    nb = _p17_north(pg, nx, ny, (nd[0] / nl, nd[1] / nl), 4.0)
    return (min(R[0], bb[0]), min(bb[1], nb[1], yb - 1.5), R[2], R[3]), nums, placed


def _p17_clip_items(items, r):
    """page items cut to the rectangle r (polys, lines, circles, texts)"""
    out = []
    for it in items:
        if it[0] == "poly":
            rings = [c_ for c_ in (_p14_clip_ring(rg, r) for rg in it[1]) if c_]
            if rings:
                out.append(("poly", rings) + tuple(it[2:]))
        elif it[0] == "line":
            for run in _p14_clip_line(it[1], r):
                out.append(("line", run) + tuple(it[2:]))
        elif it[0] == "circle":
            if r[0] <= it[1] <= r[2] and r[1] <= it[2] <= r[3]:
                out.append(it)
        elif it[0] == "text":
            if r[0] <= it[2] <= r[2] and r[1] <= it[3] <= r[3]:
                out.append(it)
    return out


P17_WIN_NAME = {"A": u"Upstream entry", "B": u"Lower reach"}
P17_CUTS = ("W1", "F2", "S4", "F4")    # the sections of page B: cut registry ids, printed as level_name gives them


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


def _p17_win_corners(fit):
    """the four survey corners of a window fitted by _p17_win_fit"""
    w, h, u, v, c, den = fit
    hw, hh = w / 2.0 * den / 1000.0, h / 2.0 * den / 1000.0
    return [((c[0] + a) * u[0] + (c[1] + b) * v[0], (c[0] + a) * u[1] + (c[1] + b) * v[1])
            for a, b in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))]


# ---------------------------------------------------------------- key maps (M4 keymap_items: the study-area outline)
def _p17_key(pg, x0, ytop, w, hmax, ids, zooms, log):
    """the key map of a page, north up, its top-left at (x0, ytop), at most w x hmax mm: M4 keymap_items (the basemap's
    key mode, the study-area outline, every id). zooms {name: survey ring}: the plan windows, drawn and named by M4.
    Cut ids (no zooms): each cut a short bold mark at its registry place, named by lp_place (the cuts W1 and F2 lie 50 m
    apart, too close for M4's end markers at this size). Returns its box, or None without basemap data."""
    D = basemap_load(log=log)
    if not D:
        log.append(u"p.17 key map: no basemap data (run the site board v51+ once)")
        return None
    try:
        r = keymap_items(ids=list(ids), zooms=zooms, D=D, log=log, col=P17_KEYCOL)
        bx = r["box"]
        na = 6.0                                         # the north arrow's column
        bw, bh = bx[2] - bx[0], bx[3] - bx[1]
        den = max(bw * 1000.0 / (w - na), bh * 1000.0 / hmax)
        r = keymap_items(ids=list(ids), zooms=zooms, D=D, log=log, col=P17_KEYCOL, box=bx, scale_den=den,
                         text_mm=FS_MIN)
    except Exception as ex:
        log.append(u"p.17 key map not drawn: {}: {}".format(type(ex).__name__, ex))
        return None
    k = 1000.0 / den
    X0 = x0 + na
    Rk = (X0, ytop - bh * k, X0 + bw * k, ytop)

    def T(p):
        return (X0 + (p[0] - bx[0]) * k, Rk[1] + (p[1] - bx[1]) * k)
    own = not zooms
    items = [it for it in r["items"] if not (own and ((it[0] in ("fill", "line") and it[2] == P17_KEYCOL) or
                                                       (it[0] == "text" and it[4] == P17_KEYCOL)))]
    sp = Page(0, 0)
    sp.poly([rect(*Rk)], fill=COL["white"])

    def fill_fn(rings, hx, alpha, nonzero):
        sp.poly([r_ for r_ in rings if len(r_) >= 3], fill=hx if alpha is None or alpha >= 0.999 else
                _sec_mix(hx, "FFFFFF", 1.0 - max(0.0, float(alpha))))

    def line_fn(pts, hx, w_mm, dash_mm, alpha):
        d_ = (list(dash_mm) if isinstance(dash_mm, (list, tuple)) else [dash_mm, dash_mm]) if dash_mm else None
        sp.line(pts, hx if alpha is None or alpha >= 0.999 else _sec_mix(hx, "FFFFFF", 1.0 - max(0.0, float(alpha))),
                w_mm, dash=d_)

    def text_fn(s, xy, size_mm, hx, bold=False, align="L"):
        sp.text(s, xy[0], xy[1] - max(size_mm, FS_MIN) * 0.35, max(size_mm, FS_MIN), hx, bold=bold,
                align=(str(align or u"L")[-1:]).upper())
    basemap_draw(items, T, fill_fn, line_fn, text_fn)
    labs, marks = [], []
    if own:
        for cid in ids:
            try:
                a, b = level_ends(cid)
            except Exception:
                continue
            A, B = T(a), T(b)
            L = math.hypot(B[0] - A[0], B[1] - A[1]) or 1.0
            if L < 3.0:                                  # a cut shorter than 3 mm on the map: a 3 mm mark across it
                m_, d_ = ((A[0] + B[0]) / 2.0, (A[1] + B[1]) / 2.0), ((B[0] - A[0]) / L, (B[1] - A[1]) / L)
                A, B = (m_[0] - d_[0] * 1.5, m_[1] - d_[1] * 1.5), (m_[0] + d_[0] * 1.5, m_[1] + d_[1] * 1.5)
            sp.line([A, B], P17_KEYCOL, 0.5)
            marks.append((min(A[0], B[0]) - 0.4, min(A[1], B[1]) - 0.4, max(A[0], B[0]) + 0.4, max(A[1], B[1]) + 0.4))
            nm = level_name(cid)
            labs.append((nm, ((A[0] + B[0]) / 2.0, (A[1] + B[1]) / 2.0)))
    out = _p17_clip_items(sp.items, Rk)
    if labs:
        got = lp_place([dict(x=p[0], y=p[1], w=text_w(nm, FS_MIN, True) + 0.6, h=FS_MIN * 1.05, rank=0, r=0.8)
                        for nm, p in labs], obstacles=marks, bounds=Rk, max_leader=12.0)
        placed_ = [g["box"] for g in got if g]
        for (nm, p), g in zip(labs, got):
            if not g:                                    # M4: every cut named; the nearest free spot with a leader
                w_ = text_w(nm, FS_MIN, True) + 0.6
                b_ = label_spot(p[0], p[1], w_, FS_MIN * 1.05, marks + placed_, Rk, (), 0.3,
                                rings=(1.0, 2.5, 4.0, 6.0, 9.0, 13.0))
                if not b_:
                    log.append(u"WARNING p.17 key map: no room for the name {}".format(nm))
                    continue
                g = dict(box=b_[0], leader=(p, lp_leader_end(b_[0], p)) if b_[1] else None)
                placed_.append(b_[0])
            bxl = g["box"]
            if g["leader"]:
                out.append(("line", [g["leader"][0], g["leader"][1]], P17_KEYCOL, 0.12, None, 1))
            out.append(("text", nm, bxl[0] + 0.3, bxl[1] + FS_MIN * 0.25, FS_MIN, P17_KEYCOL, True, "L", None, None))
    pg.items += out
    pg.poly([rect(*Rk)], fill=None, stroke=COL["ink2"], lw=0.2)
    nb = _p17_north(pg, x0 + na / 2.0, Rk[3] - 6.0, (0.0, 1.0), 3.5)
    return (x0, min(Rk[1], nb[1]), Rk[2], Rk[3])


# ---------------------------------------------------------------- page A: legend, numbered list, catalogue
def _p17_legend(pg, x, ytop, w, log):
    """a drawn sample and a plain name for every symbol the plans draw (G1); returns the bottom y"""
    fs = P17_FS
    y = ytop
    pg.text(u"ON THE PLANS", x, y - fs, fs, COL["ink_dark"], bold=True)
    y -= fs * 1.9
    rows = [("water", u"Selinos stream, darker = deeper"), ("STRIP", u"summer strip: the low-flow channel"),
            ("cell", u"lined basin cell: reed, water mint"), ("WD", u"spillway"), ("GR", u"shaded walk"),
            ("WS", u"rain terraces"), ("WP", u"wetland"), ("ARM", u"side arm"),
            ("plant", u"planting areas, wet to dry: each tint led by one species, each crown its species"),
            ("maize", u"farmland: field texture, one crop symbol"), ("olive", u"orchard: one olive symbol"),
            ("bld", u"building, roof ridges"), ("cut", u"section line, triangle: the way the section looks"),
            ("hub", u"hub")]
    if _p17_shade(log):
        rows += [("shade", lab) for _, _, lab in P17_SHADE]
    pa = _wat_pal()
    for kind, lab in rows:
        yy = y - fs * 0.15
        sm = (x, yy - 1.0, x + 6.0, yy + 2.2)
        if kind == "water":
            pg.poly([rect(*sm)], fill=pa["surface"], stroke=pa["edge"], lw=0.25)
            pg.line([(x + 1.2, yy + 0.6), (x + 4.8, yy + 0.6)], pa["deep"], 0.2)
        elif kind == "cell":
            _p17_put(pg, pla_cell_plan("reed", sm, 2.0, 0.15))
        elif kind == "plant":
            fc = PLA_SPECIES["willow"]["colours"]["fill"]
            pg.poly([rect(*sm)], fill=_sec_mix(fc, SEC["paper"], 0.72), stroke=_sec_mix(fc, SEC["paper"], 0.35), lw=0.1)
            _p17_put(pg, pla_plan("willow", x + 1.7, yy + 0.6, 0.45, crown_m=7.0))
            _p17_put(pg, pla_plan("soft_rush", x + 4.6, yy + 0.3, 2.0))
        elif kind in ("maize", "olive"):
            _p17_put(pg, pla_field_tile(sm, 1.0, crop=kind, symbol_mm=2.6))
        elif kind == "bld":
            pg.poly([rect(*sm)], fill=BLD_COL["fill"], stroke=BLD_COL["edge"], lw=BLD_LW["block"])
            pg.line([(x + 1.6, yy + 0.6), (x + 4.4, yy + 0.6)], BLD_COL["roof"], BLD_LW["roof"])
            for xa, xb in ((x, x + 1.6), (x + 6.0, x + 4.4)):
                pg.line([(xa, yy - 1.0), (xb, yy + 0.6), (xa, yy + 2.2)], BLD_COL["roof"], BLD_LW["roof"])
        elif kind == "cut":
            pg.line([(x, yy + 0.6), (x + 6.0, yy + 0.6)], COL["ink_dark"], 0.3, dash=[2.4, 0.7, 0.4, 0.7])
            pg.poly([[(x + 0.3, yy + 0.6), (x + 1.2, yy + 0.6), (x + 0.75, yy + 2.4)]], fill=COL["ink_dark"])
        elif kind == "hub":
            _p17_put(pg, ico_badge("hub", x + 3.0, yy + 0.6, 3.6))
        elif kind == "STRIP":
            pg.poly([rect(*sm)], fill=pa["surface"], stroke=pa["edge"], lw=0.25)
            pg.poly([rect(x + 0.8, yy - 0.1, x + 5.2, yy + 1.3)], fill=P17_ZONE["STRIP"][0], alpha=0.55)
        elif kind == "shade":
            col = [c_ for _, c_, l_ in P17_SHADE if l_ == lab][0]
            pg.poly([rect(*sm)], fill=col, alpha=0.6)
        else:
            f_, s_ = P17_ZONE[kind]
            pg.poly([rect(*sm)], fill=f_, stroke=s_, lw=0.12)
        t = lab if kind != "shade" else u"July shade " + lab
        ly = r28_para(pg, x + 7.5, y + fs * 1.28, w - 7.5, t, fs, COL["ink"])
        y = min(y, ly) - fs * 1.55
    return y


def _p17_list(pg, x, ytop, w, nums, placed):
    """the numbered water spaces with the species drawn there (R35), in two columns; returns the bottom y"""
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
            got = [k_ for k_ in P17_CAT if k_ in (placed.get(code) or ())]
            if code == "STRIP":
                s_ = u"**{}**: the low-flow channel".format(name)
            elif got:
                s_ = u"**{}**: {}".format(name, u", ".join(PLA_SPECIES[k_]["name"].lower() if i_ else
                                                           PLA_SPECIES[k_]["name"] for i_, k_ in enumerate(got)))
            else:
                s_ = u"**{}**".format(name)
            y = min(y - 3.8, r28_para(pg, xx + 4.6, y + fs * 0.2, cw - 4.6, s_, fs, COL["ink"]) - 0.6)
        low = min(low, y)
    return low


def _p17_foliage(key):
    t = PLA_SPECIES[key].get("foliage") or u""
    if not t or u"not found" in t or u"UNVERIFIED" in t:
        return None
    return t.split(u" (")[0]


def _p17_height(key):
    """the sourced height range, m with 2 decimals (project rule for heights)"""
    lo, hi = PLA_SPECIES[key].get("h_range") or (None, None)
    if hi is None:
        return None
    if lo is None:
        return u"up to {:.2f} m".format(hi)
    return u"{:.2f}-{:.2f} m".format(lo, hi)


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
    """page A (wb_plants): the two plan windows with the key map and the legend at their right, the numbered water
    spaces under them, the species catalogue under the list (no empty band: the crop ends with the catalogue).
    Returns [(crop id, bbox, den)]."""
    if _P17_MEMO.get("run") != id(pg):                  # a new run reads its data afresh
        _P17_MEMO.clear()
        _P17_MEMO["run"] = id(pg)
    x0, y0, x1, y1 = box
    W = min(x1 - x0, P17_W)
    x1 = x0 + W
    n0 = len(pg.items)
    G = 5.0
    LG = 56.0                                           # the key map and legend column, mm
    cb = _p17_catalogue(pg, x0, y0, x1, log, measure=True)
    ch = cb[3] - cb[1]
    ytop = y1 - P17_HEAD - 2.0                          # room for the window letters
    hmax = ytop - y0 - ch - 4 * 4.4 - 3 * G - 9.0       # the list (four lines), the gaps, the scale bar row
    # the plan windows: one standard scale for both, the first at which they fit beside the column
    pa, pb = _p17_win_pts("A", log), _p17_win_pts("B", log)
    pick = None
    for den in P17_DENS:
        fa, fb = _p17_win_fit(pa, den), _p17_win_fit(pb, den)
        if fa[0] + fb[0] + P17_WIN_GAP + G + LG <= W and max(fa[1], fb[1]) <= hmax:
            pick = (den, fa, fb)
            break
    if pick is None:
        den = P17_DENS[-1]
        pick = (den, _p17_win_fit(pa, den), _p17_win_fit(pb, den))
        log.append(u"WARNING p.17: the plan windows do not fit at any standard scale; drawn at 1:{:,.0f}".format(den))
    den, fa, fb = pick
    pg.text(u"A", x0, ytop + 1.2, P17_HEAD, COL["accent"], bold=True)
    ba, na, sa = _p17_window(pg, x0, ytop, "A", den, fa, log)
    gap = max(P17_WIN_GAP, 0.5 * (W - LG - G - fa[0] - fb[0]))   # the room left shared: a clear gap, A and B
    gap = min(gap, max(G, W - LG - G - fa[0] - fb[0]))             # never pushing B into the column
    pg.text(u"B", ba[2] + gap, ytop + 1.2, P17_HEAD, COL["accent"], bold=True)
    bb_, nb, sb_ = _p17_window(pg, ba[2] + gap, ytop, "B", den, fb, log)
    # the column: key map (outline + both windows), the legend
    kb = _p17_key(pg, x1 - LG, y1, LG, 30.0, (u"A", u"B"),
                  {u"A": _p17_win_corners(fa), u"B": _p17_win_corners(fb)}, log)
    ly = _p17_legend(pg, x1 - LG, (kb[1] if kb else y1) - 4.0, LG, log)
    placed = dict(sa)
    for c_, ks in sb_.items():
        placed[c_] = list(placed.get(c_, [])) + [k_ for k_ in ks if k_ not in placed.get(c_, [])]
    yl = _p17_list(pg, x0, min(ba[1], bb_[1]) - 4.0, bb_[2] - x0, set(na) | set(nb), placed)
    ycat = min(yl, ly) - G
    _p17_catalogue(pg, x0, ycat - ch, x1, log)
    if ycat - ch < y0 - 0.5:
        log.append(u"WARNING p.17 page A: {:.0f} mm taller than its box".format(y0 - (ycat - ch)))
    drawn_ = set(k_ for ks in placed.values() for k_ in ks)
    if drawn_ - set(P17_CAT):
        log.append(u"WARNING p.17: drawn but not in the catalogue: {}".format(u", ".join(sorted(drawn_ - set(P17_CAT)))))
    log.append(u"p.17 page A: plans 1:{:,.0f}, species planted {}, catalogue {} species, photos {}".format(
        den, len(drawn_), len(P17_CAT), sum(1 for p_ in _P17_MEMO.get("photos", []) if p_[0])))
    return [("wb_plants", items_bbox(pg.items[n0:]), den)]


# ---------------------------------------------------------------- page B: the sections at 1:500
P17_WALL_T = 0.60                    # DSİ wall thickness drawn (no source; as p.04-05 and p.13 draw it)
P17_F1_RNG = (4.0, 69.0)             # W1: the part drawn, m from the SW end (the walk, the walls, the basins beyond)
P17_F1_BED = (22.1, 54.7)            # W1: the bed between the walls, m from the SW end (the W1 width, placed so the
P17_F1_STRIP = (24.1, 28.9)          #     zone base's strip, 24.1-28.9 m on the line, lies in it)
P17_F2_RANGE = (36.0, 178.0)         # the part of F2 drawn, m along it
P17_F2_WALLS = (44.6, 67.7)          # F2: the bed between the DSİ walls (sample_cut.py: the survey's stream lines)
P17_F2_CELLS = [("reed", 77.9, 83.9), ("reed", 84.4, 90.4), ("mint", 90.9, 96.9)]   # basin cells in the zone WT
P17_F2_TERR = 7.0                    # rain terrace tread, m (the olive row spacing, plants.py PLA_CROPS)
P17_F4_RANGE = (12.0, 140.0)
P17_F4_BED = (73.7, 113.9)           # F4: the bed between the survey's two stream lines, m along the cut
P17_F4_STRIP = (86.7, 90.9)          # the zone base's strip on F4 (ZONE_COPY A-NIL-STRIP-2)
P17_F3_RANGE = (-40.0, 46.0)         # S4: m across from the bed's low point (p.14's coordinates), path to bike lane
P17_GRAVEL = 0.50
P17_ARM_D, P17_ARM_WL = 0.80, 0.30   # the side arm: channel depth and its water, m (drawing values)
P17_DECK_UP = 0.45                   # the F4 viewing deck over the bank top, m (drawing value: a seat height)
P17_RAMP = 12.0                      # ramp run per m rise (1:12, drawing rule)
P17_TERRACE_W = 4.0                  # the viewing terraces, m (drawing value)
P17_TOPO_D = (160.0, 60.0)           # background topography: survey contours on lines this far behind the cut, m
P17_STONE_UP = 0.15                  # stepping stones' tops over the average-flow water, m (= section_frame.py
#                                      sf_stepping_stones' own drawing rule, passed so the people stand on them)


def _p17_reg(cid):
    """the cut registry entry (M8) with the levels a section needs; a clear stop when one is missing"""
    r = level_registry(cid)
    for key in ("bed", "avg_flow", "q100", "q500"):
        if r.get(key) is None:
            raise RuntimeError(u"{}: '{}' is missing in the cut registry (common/data/LEVELS.py)".format(cid, key))
    return r


def _p17_wall(r):
    """the DSİ wall tops (SW, NE) of a walled cut from the registry"""
    sw, ne = r["walls"]["SW"][1], r["walls"]["NE"][1]
    if sw is None and ne is None:
        raise RuntimeError(u"{}: no wall top in the cut registry".format(r["id"]))
    return (sw if sw is not None else ne), (ne if ne is not None else sw)


def _p17_prof(gz, t0, t1, pieces, step=2.0):
    """the cut's ground [(t, z)] from t0 to t1: the survey (gz) every step m, replaced inside each piece (a, b, pts)
    by the piece's own points (a lane levelled, a channel dug)"""
    out = [(t0, gz(t0))]
    last = t0
    for a, b, pts in sorted(pieces, key=lambda q: q[0]) + [(t1, t1, [(t1, gz(t1))])]:
        s = math.floor(last / step) * step + step
        while s < a - 0.3:
            if s > last + 0.3:
                out.append((s, gz(s)))
            s += step
        out += [p for p in pts if p[0] >= last - 1e-9]
        last = max(last, b)
    return out


def _p17_flat(gz, a, b):
    """a levelled stretch a-b at the mean survey ground (2 decimals): its profile points"""
    n = max(1, int(b - a))
    z = round(sum(gz(a + (b - a) * i / float(n)) for i in range(n + 1)) / (n + 1), 2)
    return (a, b, [(a, gz(a)), (a, z), (b, z), (b, gz(b))]), z


def _p17_lane_txt(name, w_m):
    return u"{} · {:,.0f} cm".format(name, w_m * 100.0)


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


def _p17_seg_t(A, B, p, q):
    """where the segment p-q crosses A-B: the parameter 0-1 along A-B, or None"""
    d1 = (B[0] - A[0], B[1] - A[1])
    d2 = (q[0] - p[0], q[1] - p[1])
    den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-12:
        return None
    w_ = (p[0] - A[0], p[1] - A[1])
    t = (w_[0] * d2[1] - w_[1] * d2[0]) / den
    s = (w_[0] * d1[1] - w_[1] * d1[0]) / den
    return t if 0.0 <= t <= 1.0 and 0.0 <= s <= 1.0 else None


def _p17_topo(cid, t0, t1, log):
    """the background topography of a cut (M8, R16 idea): the survey contours (basemap) met by lines parallel to the cut
    P17_TOPO_D m behind it (the way the section looks, M4 end markers), as ground lines [(t m along, m a.s.l.)], the
    farthest first, each with its distance: [(d, profile)]; [] without contours (one log line)"""
    if "cbb" not in _P17_MEMO:
        D = basemap_load(log=log)
        cs = ((D or {}).get("layers") or {}).get("contours") or []
        _P17_MEMO["cbb"] = [(min(p[0] for p in P), min(p[1] for p in P), max(p[0] for p in P), max(p[1] for p in P),
                             float(z), P) for _mj, z, P in cs if z is not None and len(P) >= 2]
        if not _P17_MEMO["cbb"]:
            log.append(u"p.17 sections: no survey contours in the basemap: drawn without background topography")
    a, b = level_ends(cid)
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
    f = (-u[1], u[0])
    out = []
    for d in P17_TOPO_D:
        A = (a[0] + u[0] * t0 + f[0] * d, a[1] + u[1] * t0 + f[1] * d)
        B = (a[0] + u[0] * t1 + f[0] * d, a[1] + u[1] * t1 + f[1] * d)
        bb = (min(A[0], B[0]), min(A[1], B[1]), max(A[0], B[0]), max(A[1], B[1]))
        pts = []
        for x0_, y0_, x1_, y1_, z, P in _P17_MEMO["cbb"]:
            if x1_ < bb[0] or x0_ > bb[2] or y1_ < bb[1] or y0_ > bb[3]:
                continue
            for p, q in zip(P[:-1], P[1:]):
                s = _p17_seg_t(A, B, p, q)
                if s is not None:
                    pts.append((t0 + s * (t1 - t0), z))
        pts.sort()
        if len(pts) >= 2:
            out.append((d, [(t0, pts[0][1])] + pts + [(t1, pts[-1][1])]))
    return out


def _p17_gaps(a, b, cuts):
    """the parts of the interval a-b (a < b) outside every interval in cuts"""
    out = [(a, b)]
    for c0, c1 in cuts:
        nxt = []
        for p, q in out:
            if c1 <= p or c0 >= q:
                nxt.append((p, q))
                continue
            if c0 > p:
                nxt.append((p, c0))
            if c1 < q:
                nxt.append((c1, q))
        out = nxt
    return [(p, q) for p, q in out if q - p > 0.2]


def _p17_rows(items, W, fs, ends=None, size=None):
    """labels [(xa, xb, text, chip)] centred over their spans on up to three rows, none overlapping (G3): [(xa, xb,
    text, chip, lx, row, tw)]; ends = (left width, right width) kept free on row 0 (the cut's end names)"""
    size = size or fs
    lim = [[(ends[0] + 1.5) if ends else 0.0, W - ((ends[1] + 1.5) if ends else 0.0)], [0.0, W], [0.0, W]]
    last = [lim[r][0] - 1.5 for r in range(3)]
    out = []
    for xa, xb, text, chip in sorted(items, key=lambda q: (q[0] + q[1]) / 2.0):
        tw = text_w(text, size, True) + ((size * 1.7 + 0.8) if chip else 0.0)
        xm = (xa + xb) / 2.0
        got = None
        for r in range(3):
            lx = min(max(xm - tw / 2.0, lim[r][0]), lim[r][1] - tw)
            if lx >= last[r] + 1.5:
                got = (r, lx)
                break
        if got is None:                                  # no row has it centred: the row with the most room, moved on
            r = min(range(3), key=lambda r_: last[r_])
            got = (r, min(last[r] + 1.5, max(lim[r][0], lim[r][1] - tw)))
        r, lx = got
        last[r] = lx + tw
        out.append((xa, xb, text, chip, lx, r, tw))
    return out


def _p17_houses(cid, t0, t1, d, log):
    """the buildings of the basemap (M11, with their data height) that the line d m behind a cut crosses: [(t_a, t_b m
    along the cut, h m, floors or None)]; a building without a data height is left out (never a guessed height)"""
    L = (basemap_load(log=log) or {}).get("layers") or {}
    a, b = level_ends(cid)
    Lc = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    u = ((b[0] - a[0]) / Lc, (b[1] - a[1]) / Lc)
    f = (-u[1], u[0])
    A = (a[0] + u[0] * t0 + f[0] * d, a[1] + u[1] * t0 + f[1] * d)
    B = (a[0] + u[0] * t1 + f[0] * d, a[1] + u[1] * t1 + f[1] * d)
    bb = (min(A[0], B[0]), min(A[1], B[1]), max(A[0], B[0]), max(A[1], B[1]))
    out = []
    for bl in L.get("buildings", []):
        h = float(bl.get("h") or 0.0)
        if h <= 0.0:
            continue
        for R_ in bl["rings"][:bl.get("np", len(bl["rings"]))]:
            if len(R_) < 3 or not _p17_hit(R_, bb):
                continue
            ss = [s for s in (_p17_seg_t(A, B, p, q) for p, q in zip(R_, list(R_[1:]) + [R_[0]])) if s is not None]
            if len(ss) >= 2:
                out.append((t0 + min(ss) * (t1 - t0), t0 + max(ss) * (t1 - t0), h, int(bl.get("floors") or 0) or None))
    return sorted(out)


def _p17_depth(spec, reg, X, P, gyx, zb, top, k, wl_y, style, log):
    """behind the cut (M8, D9; R16, R19 idea), the farthest layer first: its own ground from the survey contours
    (_p17_topo: layer 2 on the line P17_TOPO_D[0] m behind, layer 1 on P17_TOPO_D[1] m), the houses that line crosses
    standing on it at their data height (sf_back_house: real profiles, faded by layer, G14 seated), then mixed tree
    groups on it (pla_group_section: wet species toward the stream, dry ones outward, none on water, none in a house).
    Layer by layer, so a nearer ground hides what stands behind it. Without contours the trees stand on the cut ground
    (one log line). Returns shapes (page mm of the section)."""
    t0, t1 = spec["rng"]
    W = X(t1)
    xb = X(min(spec["prof"], key=lambda p: p[1])[0])           # the bed's low point
    half = max(xb, W - xb) or 1.0

    def tfun(x):                                               # band 0.25 at the stream to 0.85 at the ends
        return 0.25 + 0.60 * min(1.0, abs(x - xb) / half)
    prs = dict(_p17_topo(reg["id"], t0, t1, log)) if spec.get("topo", True) else {}
    sh, nh = [], 0
    for layer, d in zip((2, 1), P17_TOPO_D):
        g_, hs = gyx, []
        pr = prs.get(d)
        if pr:
            pts = P([(t, min(z, zb + top / k)) for t, z in pr])
            sh += sf_topo_back([pts], 0.0).shapes()
            g_ = sf_gy(pts)
            for ta, tb, h, fl in _p17_houses(reg["id"], t0, t1, d, log):
                if tb - ta < 3.0:                              # a sliver under one bay (sf_back_house's 3.0 m bay)
                    continue
                sh += sf_back_house(X(max(ta, t0)), X(min(tb, t1)), g_, h, k, layer=layer, floors=fl)
                hs.append((X(ta), X(tb)))
                nh += 1
        tr, _pl, _gr = pla_group_section(0.0, W, g_, k, t0=tfun, mix=["plane", "ash", "willow", "tamarisk", "olive"],
                                         seed=spec.get("seed", 3) * 7 + layer, layers=(layer,), style=style,
                                         density=0.6, avoid=hs, hires=False, detail=False, water=wl_y)
        sh += tr
    spec["n_houses"] = nh
    return sh


def _p17_group_sec(g, X, gyx, k, wl_y, avoid, style):
    """one planting group of a cut (G9): plants.py pla_group_section over the group's stretch, its band g["t"] from
    one end to the other, mixed species with overlapping crowns, a mid layer (D9 1) behind the cut plane (0), only
    emergent species where the ground lies under the average-flow water. The helper starts its first group up to
    half its widest gap in (PLA_GROUP gap_m): the run starts that far before the stretch and that lead-in is kept
    free, so a narrow stretch still gets its group. Returns (back shapes, front shapes, placed [(key, x mm, h, crown,
    layer)])."""
    x0, x1 = X(g["a"]), X(g["b"])
    lead = 0.5 * PLA_GROUP["gap_m"][1] * k
    ta, tb = g["t"]

    def tf(x):
        return ta + (tb - ta) * min(1.0, max(0.0, (x - x0) / max(1e-9, x1 - x0)))
    out = []
    for layer in (1, 0):
        sh_, pl_, _gr = pla_group_section(x0 - lead, x1, gyx, k, t0=tf, mix=list(g["mix"]), seed=g["seed"] * 3 + layer,
                                          layers=(layer,), style=style, density=g.get("dens", 1.0),
                                          avoid=list(avoid) + [(x0 - lead - 1.0, x0)], water=wl_y)
        out.append((sh_, pl_))
    return out[0][0], out[1][0], out[0][1] + out[1][1]


def _p17_co_text(keys, tags):
    """a planting group's callout, "Plane + ash: gives shade, ecological corridor", at most ~55 characters: species
    tallest first (up to three), what the group does (up to two)"""
    for nk, nt in ((3, 2), (2, 2), (2, 1), (1, 1)):
        nm = u" + ".join(P17_SHORT.get(k_, PLA_SPECIES[k_]["name"].lower()) for k_ in keys[:nk])
        s = (nm[:1].upper() + nm[1:]) + u": " + u", ".join(P17_WHY[t] for t in tags[:nt])
        if len(s) <= 55:
            return s
    return s


def _p17_marks(cos, top, r):
    """the callout circles [(x, y, text)] moved up in steps until none overlaps another (G3), never above top - r"""
    out = []
    for x, y, t in cos:
        yy = y
        for _i in range(12):
            if all(math.hypot(x - q[0], yy - q[1]) >= 2.0 * r + 0.4 for q in out):
                break
            yy += 2.0 * r + 0.4
        if yy > top - r:                                       # no room above: beside it instead
            yy = y
            x += 2.0 * r + 0.4
        out.append((x, min(yy, top - r), t))
    return out


def _p17_section(spec, style, log):
    """one cut at 1:500 on its own Page (origin: x 0 = the start of the drawn part, y 0 = 1 m under its lowest ground)
    in style a (D1 a: cutouts over the drawn ground). Layers in M5's order: the D8 sky (sf_atmosphere sky="d8") and
    behind the cut, layer by layer, the survey ground, the houses on it and tree groups (_p17_depth); the cut ground in
    its hatch, the bed filled, the water at the average yearly flow, the Q100 / Q500 lines (M5 water_section);
    structures (lanes, terraces, ramp, bridge, stepping stones, benches, basins); the planting groups (G9 mixed, two
    depth layers, _p17_group_sec); the people of each zone (G10 fig_place_zones, nobody in water deeper than wading,
    a mid layer behind); then the programme row on top, numbered callouts on the drawing (an "Element: reason" for every
    zone and one for every planting group) with their key under it, the caption and the scale bar, the levels at the
    right. G14: every item seated on its own ground (log line sf_g14_line, once per run, by p17b_page)."""
    k = sf_k(P17_SEC_DEN)
    fs = P17_FS
    t0, t1 = spec["rng"]
    prof = spec["prof"]
    reg = _p17_reg(spec["cid"])
    name = level_name(spec["cid"])
    zb = min(z for _t, z in prof) - 1.0
    Y = sf_y_of(zb, 0.0, k)

    def X(t):
        return (t - t0) * k

    def gz(t):
        return _p17_gz(prof, t)

    def gyx(x):
        return Y(gz(x / k + t0))

    def P(pts):
        return [(X(t), Y(z)) for t, z in pts]
    W = X(t1)
    wl_y = Y(reg["avg_flow"])
    stone_y = wl_y + P17_STONE_UP * k
    wl = water_layers()
    water_section(P(prof), k, Y, cid=reg["id"], banks=spec.get("banks", ("earth", "earth")), labels=False, style=style,
                  into=wl)
    for ring, mat in spec.get("fills", []):
        wl.add("bed", sct_hatch_fill(P(ring), mat, k, None, 0.1))
    for ring in spec.get("water", []):
        wl.add("water", _wat_sec_body(P(ring), 0.6))
    for kind, a, b, fl, rim in spec.get("cells", []):
        fn = pla_reed_basin if kind == "reed" else pla_mint_cell
        wl.add("structures", fn(X(a), X(b), Y(fl), Y(rim), k, P17_BASIN["kerb_h"], P17_BASIN["kerb_t"],
                                P17_BASIN["media"]))
    for st in spec.get("structures", []):
        kind = st[0]
        if kind == "lane":
            _, a, b, lk = st
            wl.add("structures", sf_lane(X(a), Y(gz((a + b) / 2.0)), b - a, k, kind=lk))
        elif kind == "terrace":                          # rail at the end named ("a" / "b"); z: a raised deck
            _, a, b, rail_at, z = st
            zz = z if z is not None else gz((a + b) / 2.0)
            wl.add("structures", sf_terrace(X(b) if rail_at == "a" else X(a), Y(zz), b - a, k,
                                            side=-1 if rail_at == "a" else 1))
            if z is not None:
                for t_ in (a + 0.15, b - 0.15):
                    wl.add("structures", [("line", [(X(t_), Y(gz(t_))), (X(t_), Y(zz) - 0.25 * k)], SCT["cut"], 0.25)])
        elif kind == "ramp":
            _, a, b, z0, z1 = st
            wl.add("structures", sf_ramp(X(a), Y(z0), b - a, z1 - z0, k)[0])
        elif kind == "bridge":
            _, a, b, z = st
            wl.add("structures", sf_bridge(X(a), X(b), Y(z), k))
        elif kind == "bench":
            _, t_, side = st
            wl.add("structures", sf_bench(X(t_), sf_seat_x(gyx, X(t_), 0.25 * k), k, side=side, back=True))
        elif kind == "stones":                           # across the summer strip, on its floor, above the water
            _, a, b = st
            wl.add("structures", sf_stepping_stones(X(a), X(b), sf_ground_min(gyx, X(a), X(b)), wl_y, k,
                                                    above_m=P17_STONE_UP, seed=spec.get("seed", 3)))
    # the planting groups (G9): mixed groups in two depth layers, each group says what it does (one callout)
    av = [(X(a), X(b)) for a, b in spec.get("avoid", [])]
    back, front, trees, cos = [], [], [], []
    for g in spec.get("groups", []):
        if g.get("fixed"):
            pl_ = [(key, X(s), h, w, 0) for key, s, h, w in spec.get("fixed", []) if g["a"] <= s <= g["b"]]
        else:
            b_, f_, pl_ = _p17_group_sec(g, X, gyx, k, wl_y, av, style)
            back += b_
            front += f_
        keys = sorted(set(p[0] for p in pl_), key=lambda k_: -PLA_SPECIES[k_]["h_m"])
        tags = [t for t in g.get("why", ()) if t in P17_WHY_PLACE or any(t in pla_purpose(k_) for k_ in keys)]
        trees += [p for p in pl_ if p[4] == 0]
        f0 = [p for p in pl_ if p[4] == 0] or pl_
        if len(keys) >= 2 and tags and f0:
            xm = sum(p[1] for p in f0) / len(f0)
            hm = max(p[2] for p in f0)
            cos.append((xm, gyx(xm) + 0.55 * hm * k, _p17_co_text(keys, tags)))
    fx = [(key, X(s), h, w, 0) for key, s, h, w in spec.get("fixed", []) if t0 + 0.2 <= s <= t1 - 0.2]
    for i, (key, x, h, w, _l) in enumerate(sorted(fx, key=lambda q: -q[2])):   # S4: p.14's own plants, seated
        front += pla_section(key, x, sf_seat_x(gyx, x, 0.12 * w * k), k, h_m=h, crown_m=w, seed=i + 7, style=style,
                             layer=0)
    trees += [p for p in fx if p not in trees]
    wl.add("vegetation", back + front)
    bad = sf_assert_g6(k, trees=[(p[0], p[1], p[2], p[3]) for p in trees], strict=False)
    if bad:
        log.append(u"WARNING (G6) p.17 {}: {}".format(name, u"; ".join(bad[:3])))
    # people doing what each zone is for (G10): fig_place_zones, nobody where the water is deeper than wading
    figs = []
    for j, (zone, a, b, o) in enumerate(spec.get("people", [])):
        o = o or {}
        gr = stone_y if zone == "stepping_stones" else (Y(o["z"]) if o.get("z") is not None else None)
        sh_, _pl = fig_place_zones([(zone, X(a), X(b), gr)], gyx, k, seed=31 * j + 5 + 7 * spec.get("seed", 3),
                                   layer=0, style=style, density=o.get("dens", 1.0), water=wl_y,
                                   max_per_zone=o.get("n"))
        figs += sh_
    wl.add("figures", figs)
    for t_, z_, txt in spec.get("callouts", []):
        cos.append((X(t_), (Y(z_) if z_ is not None else gyx(X(t_))) + 2.5 * k, txt))
    top = _p17_shp_bb(wl.shapes())[3] + 1.5
    # behind the cut (D9): the sky, the depth layers, people further along the walks (layer 1), basins beyond
    clipr = (0.0, 0.0, W, top)
    atm = water_layers()
    sf_atmosphere(0.0, W, gyx, top, k, seed=spec.get("seed", 3), sky="d8", trees=False, into=atm)
    wl.add("atmosphere", _p17_clip(atm.L["atmosphere"], clipr))
    wl.add("background", _p17_clip(_p17_depth(spec, reg, X, P, gyx, zb, top, k, wl_y, style, log), clipr))
    bp = []
    for kind, a, b, fl, rim in spec.get("beyond", []):
        fn = pla_reed_basin if kind == "reed" else pla_mint_cell
        bp += fn(X(a), X(b), Y(fl), Y(rim), k, P17_BASIN["kerb_h"], P17_BASIN["kerb_t"], P17_BASIN["media"])
    if bp:
        b_ = _p17_shp_bb(bp)
        bp.append(("poly", [(b_[0], b_[1]), (b_[2], b_[1]), (b_[2], b_[3]), (b_[0], b_[3])], "FFFFFF", None, 0.1, 0.5))
        wl.add("background", bp)
    for j, (zone, a, b) in enumerate(spec.get("back", [])):
        sh_, _pl = fig_place_zones([(zone, X(a), X(b))], gyx, k, seed=77 + j + spec.get("seed", 3), layer=1,
                                   style=style, density=0.6, water=wl_y, max_per_zone=2)
        wl.add("background", sh_)
    pg = Page(0, 0)
    _p17_put(pg, _p17_clip(wl.shapes(), (0.0, -1e4, W, 1e4)))
    for pts, colour in spec.get("arrows", []):
        arrow(pg, P(pts), colour, 0.3, 1.6, [0.9, 0.6])
    # the numbered callouts on the drawing (shared style: SfCallouts, P17_CO)
    co = SfCallouts()
    for x, y, txt in _p17_marks(sorted(cos, key=lambda q: q[0]), top - 0.5, 0.75 * P17_CO):
        co.add(x, y, txt)
    _p17_put(pg, co.marks(size=P17_CO))
    # on top: the cut's end names and its programmes on vertical lines (R18 lane widths), never crossing a label
    top += 2.5
    rh = fs * 1.6
    ends = (name, name + u"'")
    ew = (text_w(ends[0], P17_HEAD, True), text_w(ends[1], P17_HEAD, True))
    zl = _p17_rows([(X(max(a, t0)), X(min(b, t1)), txt, None) for a, b, txt in spec.get("zones", [])
                    if min(b, t1) - max(a, t0) >= 0.5], W, fs, ew)
    boxes = [(-0.4, top - 1.2, ew[0] + 0.4, top + P17_HEAD * CAP + 0.3, -1, -1),
             (W - ew[1] - 0.4, top - 1.2, W + 0.4, top + P17_HEAD * CAP + 0.3, -1, -2)]
    pg.text(ends[0], 0.0, top, P17_HEAD, COL["ink_dark"], bold=True)
    pg.text(ends[1], W, top, P17_HEAD, COL["ink_dark"], bold=True, align="R")
    for i, (xa, xb, txt, chip, lx, r_, tw) in enumerate(zl):
        yl = top + r_ * rh
        pg.text(txt, lx, yl, fs, COL["ink_dark"], bold=True)
        boxes.append((lx - 0.4, yl - fs * 0.3 - 0.3, lx + tw + 0.4, yl + fs * CAP + 0.3, r_, i))
    for i, (xa, xb, txt, chip, lx, r_, tw) in enumerate(zl):
        yl = top + r_ * rh - 0.6
        for p_, q_ in _p17_gaps(xa, xb, [(b_[0], b_[2]) for b_ in boxes
                                         if b_[4] in (r_, -1) and b_[5] != i and b_[1] <= yl <= b_[3]]):
            pg.line([(p_, yl), (q_, yl)], COL["ink2"], 0.12)
        for xv in (xa, xb):
            y0_ = gyx(min(max(xv, 0.01), W - 0.01)) + 0.4
            cuts = [(b_[1], b_[3]) for b_ in boxes if b_[4] < r_ and b_[0] <= xv <= b_[2]]
            cuts += [(y_ - 0.75 * P17_CO, y_ + 0.75 * P17_CO) for _n, x_, y_, _t in co.items
                     if abs(x_ - xv) < 0.75 * P17_CO]
            for p_, q_ in _p17_gaps(y0_, yl, cuts):
                pg.line([(xv, p_), (xv, q_)], COL["ink2"], 0.1, dash=[0.5, 0.5])
    # under it: the planting bands (S4), the callout key in columns, the caption and the scale bar
    low = -1.2
    if spec.get("bands"):
        yb_ = low - 1.0 - fs
        br = _p17_rows([(X(max(a, t0)), X(min(b, t1)), lab, c_) for a, b, lab, c_ in spec["bands"]], W, fs)
        for xa, xb, txt, chip, lx, r_, tw in br:
            yl = yb_ - r_ * fs * 1.5
            pg.poly([rect(lx, yl - 0.2, lx + fs * 1.7, yl + fs * 0.95)], fill=BAND_COL.get(chip, chip))
            pg.text(chip, lx + fs * 0.85, yl + 0.1, fs, "FFFFFF", bold=True, align="C")
            pg.text(txt, lx + fs * 1.7 + 0.8, yl, fs, COL["ink_dark"], bold=True)
            low = min(low, yl - fs * 0.3)
    items = sorted(dict((n, t) for n, _x, _y, t in co.items).items())
    if items:
        cw = max(text_w(t, P17_CO) for _n, t in items) + 2.0 * P17_CO + 4.0
        nc = max(1, min(len(items), int((W + 4.0) // cw)))
        per = (len(items) + nc - 1) // nc
        yk = low - 1.5
        for c_ in range(nc):
            part = items[c_ * per:(c_ + 1) * per]
            if part:
                kc = SfCallouts()
                kc.items = [(n, 0.0, 0.0, t) for n, t in part]
                _p17_put(pg, kc.key(c_ * cw, yk, size=P17_CO))
        low = yk - per * 1.5 * P17_CO
    yc = low - fs * 1.5
    pg.text(spec["caption"], 0.0, yc, fs, COL["ink_dark"], bold=True)
    r28_scale_bar(pg, text_w(spec["caption"], fs, True) + 5.0, yc - 0.3, P17_SEC_DEN, fs, False)
    # the levels at the right, every one from the cut registry (M8), or the design's own named level
    ent = [(Y(reg["bed"]), u_level(reg["bed"]) + u" bed", C["w4"], False),
           (Y(reg["avg_flow"]), u_level(reg["avg_flow"]) + u" average flow", C["w4"], True),
           (Y(reg["q100"]), u_level(reg["q100"]) + u" Q100", C["w4"], False),
           (Y(reg["q500"]), u_level(reg["q500"]) + u" Q500", C["w4"], False)]
    ent += [(Y(z), u_level(z) + u" " + t, COL["ink"], False) for z, t in spec.get("levels", [])]
    level_ladder(pg, ent, W + 0.8, W + 4.0, fs, lo=0.0)
    log.append(u"p.17 {}: {} planting groups, {} callouts, {} background houses (data heights)".format(
        name, len(spec.get("groups", [])), len(items), spec.get("n_houses", 0)))
    return pg


def _p17_f2(log):
    """F2 across the stream at the upstream entry (cut registry F2): the walk on the SW wall top, stepping stones across the bed (v10: nobody in the walled channel's water),
    the spillway, the lined reed basins, the dry bank, the shaded walk with its bike lane, the rain terraces and the
    viewing terrace on the top one"""
    r = _p17_reg("F2")
    bed = r["bed"]
    wsw, wne = _p17_wall(r)
    g = _p17_ground("F2")

    def gz(t):
        return _p17_interp(g, t)
    t0, t1 = P17_F2_RANGE
    ws, wn = P17_F2_WALLS
    wtk = P17_WALL_T
    wk, bk = P14_PROM_W
    zone = dict((c_, (a_, b_)) for c_, a_, b_ in level_cut("F2").get("zones") or [])
    for c_ in ("STRIP", "WD", "WT", "GR", "WS"):
        if c_ not in zone:
            raise RuntimeError(u"F2: zone {} is missing in the cut registry (common/data/LEVELS.py)".format(c_))
    st0, st1 = zone["STRIP"]
    sp0, sp1 = wn + wtk, zone["WD"][1]
    bt0, bt1 = zone["WT"]
    gr0, gr1 = zone["GR"]
    te0, te1 = zone["WS"]
    zp = round(max(gz(bt0 + i) for i in range(int(bt1 - bt0) + 1)), 2)     # the basin platform: the ground's top there
    floor = zp - P17_BASIN["depth"]
    prof = []
    # south-west: the ground held up to the wall top behind the DSİ wall, the survey further out
    t, side = ws - wtk, []
    while t >= t0 - 1e-9:
        side.append((t, wsw if gz(t) < wsw and all(p[1] == wsw for p in side) else gz(t)))
        t -= 2.0
    if side[-1][0] > t0:
        side.append((t0, wsw if gz(t0) < wsw and all(p[1] == wsw for p in side) else gz(t0)))
    prof += side[::-1]
    prof += [(ws - wtk, wsw), (ws, wsw), (ws, bed), (st0, bed), (st0, bed - STRIP_DEPTH), (st1, bed - STRIP_DEPTH),
             (st1, bed), (wn, bed), (wn, wne), (sp0, wne)]
    # the spillway trough from the basins down to the wall top, then the basin platform and the cells
    prof += [(sp0 + 0.3, wne), (sp0 + 0.3, wne - 0.45), (sp1 - 0.3, wne - 0.30), (sp1 - 0.3, wne), (sp1, wne),
             (bt0 - 0.3, zp), (bt0, zp)]
    cells = []
    for kind, a, b in P17_F2_CELLS:
        prof += [(a, zp), (a, floor + P17_BASIN["media"]), (b, floor + P17_BASIN["media"]), (b, zp)]
        cells.append((kind, a, b, floor, zp))
    prof += [(bt1, zp)]
    t = math.ceil(bt1 + 1.0)
    while t < gr0 - 0.3:
        prof.append((t, gz(t)))
        t += 2.0
    pc, zg = _p17_flat(gz, gr0, gr1)                    # the shaded walk, levelled
    prof += pc[2][:3]
    # the rain terraces: level treads P17_F2_TERR wide at the mean ground of each, stone retaining walls
    fills, treads = [], []
    prev, s = zg, te0
    while s + P17_F2_TERR <= te1 + 0.1:
        lv = round(sum(gz(s + j * 0.5) for j in range(int(P17_F2_TERR * 2) + 1)) / (int(P17_F2_TERR * 2) + 1), 2)
        prof += [(s, lv), (s + P17_F2_TERR, lv)]
        fills.append(([(s - 0.4, min(prev, lv) - 0.4), (s, min(prev, lv) - 0.4), (s, max(prev, lv)),
                       (s - 0.4, max(prev, lv))], "stone"))
        treads.append((s, s + P17_F2_TERR, lv))
        prev, s = lv, s + P17_F2_TERR
    prof.append((min(t1, s + 0.6), gz(min(t1, s + 0.6))))
    if prof[-1][0] < t1:
        prof.append((t1, gz(t1)))
    fills += [([(ws - wtk, wsw), (ws, wsw), (ws, bed - P17_GRAVEL), (ws - wtk, bed - P17_GRAVEL)], "stone"),
              ([(wn, wne), (wn + wtk, wne), (wn + wtk, bed - P17_GRAVEL), (wn, bed - P17_GRAVEL)], "stone"),
              ([(st0 - 0.15, bed), (st0 - 0.15, bed - STRIP_DEPTH - 0.15), (st1 + 0.15, bed - STRIP_DEPTH - 0.15),
                (st1 + 0.15, bed), (st1, bed), (st1, bed - STRIP_DEPTH), (st0, bed - STRIP_DEPTH), (st0, bed)],
               "concrete"),
              ([(sp0, wne), (sp0 + 0.3, wne), (sp0 + 0.3, wne - 0.45), (sp1 - 0.3, wne - 0.30), (sp1 - 0.3, wne),
                (sp1, wne), (sp1, wne - 0.5), (sp0, wne - 0.65)], "concrete")]
    water = [[(sp0 + 0.3, wne - 0.45), (sp1 - 0.3, wne - 0.30), (sp1 - 0.3, wne - 0.15), (sp0 + 0.3, wne - 0.25)]]
    wa = (ws - wtk - wk, ws - wtk)                      # the walk on the wall top
    bl = (gr0 + 2.5, gr0 + 2.5 + bk)                    # the shaded walk: bike lane, then the walk
    wl_ = (bl[1] + 2.0, bl[1] + 2.0 + wk)
    ta = treads[-1][0] if treads else te1 - P17_TERRACE_W
    vt = (ta, ta + P17_TERRACE_W)                       # the viewing terrace on the top tread, its rail to the stream
    rush = ("soft_rush", "loosestrife")
    groups = [dict(a=ws + 0.2, b=ws + 2.6, t=(0.02, 0.06), mix=rush, dens=1.2, why=("cleaning",), seed=21),
              dict(a=wn - 2.6, b=wn - 0.2, t=(0.06, 0.02), mix=rush, dens=1.2, why=("cleaning",), seed=22),
              dict(a=sp0 + 0.5, b=sp1 - 0.5, t=(0.04, 0.08), mix=rush, dens=0.8, why=("cleaning",), seed=23),
              dict(a=bt1 + 0.5, b=gr0 - 0.3, t=(0.55, 0.85), mix=("chaste", "tamarisk", "olive", "rosemary", "lavender"),
                   why=("perception", "corridor"), seed=24),
              dict(a=gr0 + 0.3, b=gr1 - 0.3, t=(0.48, 0.55), mix=("plane", "ash", "chaste"), why=("shade", "corridor"),
                   seed=25),
              dict(a=te0 + 0.5, b=vt[0] - 0.3, t=(0.78, 0.95), mix=("olive", "rosemary", "lavender"),
                   why=("shade", "perception"), seed=26)]
    bn = bl[1] + 0.7                                    # a bench between the bike lane and the walk
    avg = r["avg_flow"]
    return dict(cid="F2", seed=2, rng=(t0, t1), prof=prof, fills=fills, water=water, cells=cells, groups=groups,
                avoid=[wa, bl, wl_, vt, (bn - 0.3, bn + 0.8)],
                structures=[("lane", wa[0], wa[1], "walk"), ("lane", bl[0], bl[1], "bike"),
                            ("lane", wl_[0], wl_[1], "walk"), ("terrace", vt[0], vt[1], "a", None),
                            ("stones", st0, st1), ("bench", bn, 1)],
                people=[("walkway", wa[0], wa[1], None), ("stepping_stones", st0, st1, {"n": 2}),
                        ("bike_lane", bl[0], bl[1], {"n": 1}), ("walkway", wl_[0], wl_[1], None),
                        ("viewing_terrace", vt[0], vt[1], {"n": 3})],   # v10: nobody in the walled channel's water (Aras 11:28)
                callouts=[((wa[0] + wa[1]) / 2.0, None, u"Wall-top path: walk along the stream, above the bed"),
                          ((st0 + st1) / 2.0, avg, u"Stepping stones: cross the summer strip dry-shod"),
                          ((sp0 + sp1) / 2.0, wne, u"Spillway: basin overflow runs back to the stream"),
                          ((bt0 + bt1) / 2.0, zp, u"Reed basins: clean run-off before the stream"),
                          ((bl[0] + bl[1]) / 2.0, None, u"Bike lane: through route, apart from walkers"),
                          (bn, None, u"Bench: in the trees' shade, facing the water"),
                          ((wl_[0] + wl_[1]) / 2.0, None, u"Shaded walk: under the trees, out of the sun"),
                          ((te0 + vt[0]) / 2.0, None, u"Rain terraces: level treads hold the rain"),
                          ((vt[0] + vt[1]) / 2.0, None, u"View terrace: over the basins to the stream")],
                back=[("walkway", wa[0], wa[1]), ("walkway", wl_[0], wl_[1])],
                arrows=[([(sp0 + 0.2, wne - 0.2), (sp0 - 0.8, wne - 1.6), (sp0 - 1.2, bed + 0.4)], C["w3"])],
                zones=[(wa[0], wa[1], _p17_lane_txt(u"PATH", wk)), (ws, wn, u"SUMMER STRIP"), (sp0, sp1, u"SPILLWAY"),
                       (bt0, bt1, u"REED BASINS"), (bt1, gr0, u"DRY BANK"), (bl[0], bl[1], _p17_lane_txt(u"BIKE", bk)),
                       (wl_[0], wl_[1], _p17_lane_txt(u"PATH", wk)), (te0, vt[0], u"RAIN TERRACES"),
                       (vt[0], vt[1], u"VIEW TERRACE")],
                levels=[(wne, u"DSİ wall")],
                caption=u"F2 · the upstream entry: rain terraces, reed basins and the walled stream")


def _p17_f4(log):
    """F4 across the lower reach (cut registry F4): the path and its bridge over the side arm, the bank top, the
    viewing deck with its ramp, the widened bed with its strip (wading), the NE bank, the bike lane and the walk"""
    r = _p17_reg("F4")
    g = _p17_ground("F4")

    def gz(t):
        return _p17_interp(g, t)
    t0, t1 = P17_F4_RANGE
    zone = dict((c_, (a_, b_)) for c_, a_, b_ in level_cut("F4").get("zones") or [])
    if "ARM" not in zone:
        raise RuntimeError(u"F4: zone ARM is missing in the cut registry (common/data/LEVELS.py)")
    a0, a1 = zone["ARM"]
    b0, b1 = P17_F4_BED
    st0, st1 = P17_F4_STRIP
    wk, bk = P14_PROM_W
    zf = gz((a0 + a1) / 2.0) - P17_ARM_D               # the side arm's floor
    zs = gz((st0 + st1) / 2.0)
    pw = (a0 - 1.0 - wk, a0 - 1.0)                      # the path to the bridge
    br = (a0 - 1.0, a1 + 1.0)                           # the footbridge over the side arm
    zbr = round(max(gz(br[0]), gz(br[1])) + 0.10, 2)
    dk = (62.0 - P17_TERRACE_W, 62.0)                   # the viewing deck at the SW bank's edge (survey: it drops at 62 m)
    rp = (dk[0] - P17_DECK_UP * P17_RAMP, dk[0])        # its ramp, 1:12
    zr0 = gz(rp[0])
    zdk = round(zr0 + P17_DECK_UP, 2)
    bl = (127.0, 127.0 + bk)                            # the street side: bike lane, then the walk
    wl_ = (bl[1] + 1.0, bl[1] + 1.0 + wk)
    pieces = [_p17_flat(gz, pw[0], pw[1])[0], _p17_flat(gz, bl[0], wl_[1])[0],
              (a0, a1, [(a0, gz(a0)), (a0 + 0.8, zf), (a1 - 0.8, zf), (a1, gz(a1))]),
              (st0, st1, [(st0, zs), (st0, zs - STRIP_DEPTH), (st1, zs - STRIP_DEPTH), (st1, zs)])]
    prof = _p17_prof(gz, t0, t1, pieces)
    fills = [([(st0 - 0.15, zs), (st0 - 0.15, zs - STRIP_DEPTH - 0.15), (st1 + 0.15, zs - STRIP_DEPTH - 0.15),
               (st1 + 0.15, zs), (st1, zs), (st1, zs - STRIP_DEPTH), (st0, zs - STRIP_DEPTH), (st0, zs)], "concrete")]
    f = 1.0 - P17_ARM_WL / P17_ARM_D
    water = [[(a0 + 0.8 * f, zf + P17_ARM_WL), (a0 + 0.8, zf), (a1 - 0.8, zf), (a1 - 0.8 * f, zf + P17_ARM_WL)]]
    rush = ("soft_rush", "loosestrife")
    groups = [dict(a=t0 + 0.3, b=pw[0] - 0.3, t=(0.50, 0.56), mix=("plane", "ash", "chaste"), why=("shade",), seed=41),
              dict(a=br[1] + 0.3, b=rp[0] - 0.3, t=(0.50, 0.62), mix=("plane", "ash", "tamarisk", "chaste"),
                   why=("shade", "wind", "corridor"), seed=42),
              dict(a=dk[1] + 0.3, b=b0, t=(0.42, 0.10), mix=("ash", "tamarisk", "willow", "chaste", "loosestrife"),
                   why=("corridor", "shade"), seed=43),
              dict(a=b0 + 0.3, b=st0 - 0.3, t=(0.14, 0.02), mix=rush, dens=0.8, why=("cleaning", "corridor"), seed=44),
              dict(a=st1 + 0.3, b=93.5, t=(0.02, 0.04), mix=rush, dens=0.8, why=("cleaning", "corridor"), seed=45),
              dict(a=b1 + 0.3, b=121.0, t=(0.10, 0.45), mix=("loosestrife", "willow", "tamarisk", "chaste", "ash"),
                   why=("corridor", "shade"), seed=46),
              dict(a=121.0, b=bl[0] - 0.3, t=(0.50, 0.55), mix=("plane", "ash"), why=("shade", "noise"), seed=47)]
    bn = br[1] + 1.0                                    # a bench on the bank top, in the trees' shade
    avg = r["avg_flow"]
    return dict(cid="F4", seed=4, rng=(t0, t1), prof=prof, fills=fills, water=water, groups=groups,
                avoid=[pw, br, (rp[0], dk[1]), bl, wl_, (bn - 0.3, bn + 0.8)],
                structures=[("lane", pw[0], pw[1], "walk"), ("bridge", br[0], br[1], zbr),
                            ("ramp", rp[0], rp[1], zr0, zdk), ("terrace", dk[0], dk[1], "b", zdk),
                            ("lane", bl[0], bl[1], "bike"), ("lane", wl_[0], wl_[1], "walk"),
                            ("stones", st0, st1), ("bench", bn, 1)],
                people=[("walkway", pw[0], pw[1], None), ("bridge_crossing", br[0] + 0.5, br[1] - 0.5, {"z": zbr}),
                        ("viewing_terrace", dk[0], dk[1], {"z": zdk, "n": 3}),
                        ("stepping_stones", st0, st1, {"n": 2}), ("wading_strip", 94.0, 109.5, {"n": 3}),
                        ("bike_lane", bl[0], bl[1], {"n": 1}), ("walkway", wl_[0], wl_[1], None)],
                callouts=[((pw[0] + pw[1]) / 2.0, None, u"Path: walk the SW bank to the footbridge"),
                          ((br[0] + br[1]) / 2.0, zbr, u"Footbridge: cross the side arm dry-shod"),
                          (bn, None, u"Bench: in the trees' shade on the bank top"),
                          ((rp[0] + dk[1]) / 2.0, zdk, u"View terrace: up a ramp, a step-free view"),
                          ((st0 + st1) / 2.0, avg, u"Stepping stones: cross the summer strip dry-shod"),
                          ((94.0 + 109.5) / 2.0, avg, u"Wading strip: shallow water in the widened bed"),
                          ((bl[0] + bl[1]) / 2.0, None, u"Bike lane: street side, apart from walkers"),
                          ((wl_[0] + wl_[1]) / 2.0, None, u"Street walk: behind the trees, off the traffic")],
                back=[("walkway", pw[0], pw[1]), ("walkway", wl_[0], wl_[1])],
                zones=[(pw[0], pw[1], _p17_lane_txt(u"PATH", wk)), (br[0], br[1], u"BRIDGE"),
                       (br[1], rp[0], u"BANK TOP"), (rp[0], dk[1], u"VIEW TERRACE"), (dk[1], b0, u"SW BANK"),
                       (b0, b1, u"WADING"), (b1, bl[0], u"NE BANK"), (bl[0], bl[1], _p17_lane_txt(u"BIKE", bk)),
                       (wl_[0], wl_[1], _p17_lane_txt(u"PATH", wk))],
                caption=u"F4 · the lower reach: the side arm, the bank top and the widened stream")


def _p17_f1(log):
    """W1 at the inflow (cut registry W1, = F1): the bike lane and the walk under the planes on the SW bank, stepping
    stones in the walled bed (v10: nobody in its water), the viewing terrace on the NE wall top, the reed basins beyond"""
    r = _p17_reg("W1")
    bed = r["bed"]
    wsw, wne = _p17_wall(r)
    t0, t1 = P17_F1_RNG
    ws, wn = P17_F1_BED
    st0, st1 = P17_F1_STRIP
    wtk = P17_WALL_T
    wk, bk = P14_PROM_W
    prof = [(t0, wsw), (ws - wtk, wsw), (ws, wsw), (ws, bed), (st0, bed), (st0, bed - STRIP_DEPTH),
            (st1, bed - STRIP_DEPTH), (st1, bed), (wn, bed), (wn, wne), (wn + wtk, wne), (t1, wne)]
    fills = [([(ws - wtk, wsw), (ws, wsw), (ws, bed - P17_GRAVEL), (ws - wtk, bed - P17_GRAVEL)], "stone"),
             ([(wn, wne), (wn + wtk, wne), (wn + wtk, bed - P17_GRAVEL), (wn, bed - P17_GRAVEL)], "stone"),
             ([(st0 - 0.15, bed), (st0 - 0.15, bed - STRIP_DEPTH - 0.15), (st1 + 0.15, bed - STRIP_DEPTH - 0.15),
               (st1 + 0.15, bed), (st1, bed), (st1, bed - STRIP_DEPTH), (st0, bed - STRIP_DEPTH), (st0, bed)],
              "concrete")]
    bl = (t0 + 0.6, t0 + 0.6 + bk)
    wl_ = (bl[1] + 1.4, bl[1] + 1.4 + wk)
    vt = (wn + wtk, wn + wtk + P17_TERRACE_W)
    bx0 = vt[1] + 0.6
    beyond = [("reed", bx0, bx0 + 5.6, wne - P17_BASIN["depth"], wne),
              ("mint", bx0 + 6.2, min(t1 - 0.5, bx0 + 11.0), wne - P17_BASIN["depth"], wne)]
    rush = ("soft_rush", "loosestrife")
    groups = [dict(a=t0 + 0.2, b=ws - wtk - 0.3, t=(0.50, 0.56), mix=("plane", "ash", "chaste"),
                   why=("shade", "corridor"), seed=61),
              dict(a=ws + 0.2, b=ws + 2.0, t=(0.02, 0.05), mix=rush, dens=1.2, why=("cleaning",), seed=62),
              dict(a=wn - 2.0, b=wn - 0.2, t=(0.05, 0.02), mix=rush, dens=1.2, why=("cleaning",), seed=63)]
    bn = bl[1] + 0.5                                    # a bench between the bike lane and the path
    avg = r["avg_flow"]
    return dict(cid="W1", seed=1, rng=(t0, t1), prof=prof, fills=fills, groups=groups, beyond=beyond,
                avoid=[bl, wl_, (bn - 0.3, bn + 0.8)],
                structures=[("lane", bl[0], bl[1], "bike"), ("lane", wl_[0], wl_[1], "walk"),
                            ("terrace", vt[0], vt[1], "a", None), ("stones", st0, st1), ("bench", bn, 1)],
                people=[("bike_lane", bl[0], bl[1], {"n": 1}), ("walkway", wl_[0], wl_[1], None),
                        ("stepping_stones", st0, st1, {"n": 2}), ("viewing_terrace", vt[0], vt[1], {"n": 2})],
                callouts=[((bl[0] + bl[1]) / 2.0, None, u"Bike lane: through route under the trees"),
                          (bn, None, u"Bench: in the trees' shade, facing the water"),
                          ((wl_[0] + wl_[1]) / 2.0, None, u"Path: shaded by the trees of the SW bank"),
                          ((st0 + st1) / 2.0, avg, u"Stepping stones: cross the summer strip dry-shod"),
                          ((vt[0] + vt[1]) / 2.0, None, u"View terrace: on the NE wall top, over the bed"),
                          ((bx0 + t1) / 2.0, wne, u"Reed basins beyond: stream water cleaned there")],
                back=[("walkway", wl_[0], wl_[1])],
                arrows=[([((ws + wn) / 2.0 + 6.0, bed + 0.5), (wn - 1.0, wne - 0.6), (bx0 + 1.0, wne + 0.9)], C["w3"])],
                zones=[(bl[0], bl[1], _p17_lane_txt(u"BIKE", bk)), (wl_[0], wl_[1], _p17_lane_txt(u"PATH", wk)),
                       (ws, wn, u"SUMMER STRIP"), (vt[0], vt[1], u"VIEW TERRACE"), (bx0, t1, u"REED BASINS beyond")],
                levels=[(wne, u"DSİ wall")],
                caption=u"W1 · the walled stream at the inflow, the reed basins beyond")


P17_S4_WHY = {"sw_path": ("shade", "noise"), "sw_slope": ("corridor", "shade"), "bed_sw": ("cleaning",),
              "open": ("cleaning",), "toe": ("cleaning", "corridor"), "terr_a": ("corridor", "shade"),
              "terr_b": ("corridor", "perception"), "terr_c": ("shade", "corridor"), "prom": ("shade",),
              "fill": ("shade", "noise")}   # what each of p.14's planting zones does on S4 (G9)


def _p17_f3(log):
    """S4 (cut registry S4, = F3): p.14's own cut and planting (_p14_geo, _p14_planting), so the cut is the same
    everywhere: the path, the planting bands of the widened stream by the days water covers the ground (PLANT_BANDS,
    RWS), wading in the strip, the lower walk, the sun steps, the promenade and the bike lane"""
    G = _p14_geo()
    t0, t1 = P17_F3_RANGE
    prof = [(t0, _p14_surf(t0))] + [p for p in G["prof"] if t0 < p[0] < t1] + [(t1, _p14_surf(t1))]
    bed, sfl, shelf, zn = G["bed"], G["sfl"], G["shelf"], G["zones"]
    st0, st1 = zn["strip"]
    lt = P14_LINER
    e0, p0 = zn["steps"]
    p1 = zn["prom"][1]
    p2 = zn["bike"][1]
    w0, w1 = P14_WALK
    tt0, tt1 = zn["terrace"]
    wk, bk = P14_PROM_W
    fills = [([(tt0, shelf), (tt1, shelf), (tt1, shelf - 0.3), (tt0, shelf - 0.3)], "gravel"),
             ([(st0 - lt, bed), (st0 - lt, sfl - lt), (st1 + lt, sfl - lt), (st1 + lt, bed), (st1, bed), (st1, sfl),
               (st0, sfl), (st0, bed)], "concrete"),
             ([(w0, shelf), (w1, shelf), (w1, shelf - 0.2), (w0, shelf - 0.2)], "concrete"),
             ([p for p in G["prof"] if e0 - 1e-9 <= p[0] <= p0 + 1e-9 and p[1] >= shelf - 1e-9] +
              [(p0, P14_PROM - 0.35), (e0, shelf - 0.35)], "concrete"),
             ([(p0, P14_PROM), (p2, P14_PROM), (p2, P14_PROM - P14_SLAB), (p0, P14_PROM - P14_SLAB)], "concrete")]
    fn = globals().get("_p14_planting")
    fixed = [tuple(p)[:4] for p in (fn() if callable(fn) else P14_PLANTS)]
    groups = [dict(a=zn[z_][0], b=zn[z_][1], fixed=True, why=P17_S4_WHY.get(z_, ()))
              for z_ in [q[0] for q in globals().get("P14_PLANT_ZONES", [])] if z_ in zn]
    # the bands: the ground's band code every 0.25 m, merged into runs; each run named once
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
    bands, seen = [], set()
    for c_, a, b in runs:
        if b - a < 3.0 or c_ in seen:
            continue
        nm, days = bn.get(c_, (u"", u""))
        lab = (nm.split(u" (")[0].split(u" / ")[0].lower() + u" · " +
               days.replace(u" d/yr", u" d").replace(u"–", u"-").split(u";")[0]).strip(u" ·")
        bands.append((a, b + 0.25, lab, c_))
        seen.add(c_)
    sw = zn["sw_path"]
    return dict(cid="S4", seed=3, rng=(t0, t1), prof=prof, fills=fills, fixed=fixed, groups=groups,
                structures=[("stones", st0, st1)],
                people=[("walkway", max(t0 + 0.5, sw[0]), sw[1], {"n": 2}), ("stepping_stones", st0, st1, {"n": 2}),
                        ("walkway", w0, w1, {"n": 2}), ("sun_steps", e0, p0, {"n": 3}), ("walkway", p0, p1, None),
                        ("bike_lane", p1, p2, {"n": 1})],
                callouts=[((max(t0 + 0.5, sw[0]) + sw[1]) / 2.0, None, u"Path: SW bank walk under the trees"),
                          ((st0 + st1) / 2.0, _p17_reg("S4")["avg_flow"],
                           u"Stepping stones: cross the summer strip dry-shod"),
                          ((w0 + w1) / 2.0, None, u"Lower walk: along the water, between the bands"),
                          ((e0 + p0) / 2.0, None, u"Sun steps: sit in the sun, facing the water"),
                          ((p0 + p1) / 2.0, None, u"Promenade: top-of-bank walk under shade trees"),
                          ((p1 + p2) / 2.0, None, u"Bike lane: on the bank top, apart from walkers")],
                back=[("walkway", p0, p1)],
                zones=[(sw[0], sw[1], u"PATH"), (st0, st1, u"STONES"), (w0, w1, u"LOWER WALK"),
                       (e0, p0, u"SUN STEPS"), (p0, p1, _p17_lane_txt(u"PROMENADE", wk)),
                       (p1, p2, _p17_lane_txt(u"BIKE", bk))],
                bands=bands, levels=[(P14_PROM, u"promenade")],
                caption=u"S4 · the planting bands of the widened stream " + cite(P15_BAND_SRC))


# ---------------------------------------------------------------- page B: the calendar, giant reed, the page
P17_LEAF = "DCE3C8"                  # in leaf (calm, G5)
P17_BLOOM = "C4A9B8"                 # in flower: one muted colour for every species
P17_MONTHS = u"JFMAMJJASOND"


def _p17_calendar(pg, x, ytop, w, log):
    """the species of the catalogue on ONE month axis (R36), calm (G5): a pale bar where it is in leaf, a muted one
    where it flowers, a fine cross where its flower heads are cut; sourced months only (plants.py pla_months).
    Returns the bottom y."""
    fs = P17_FS
    lw_ = max(text_w(PLA_SPECIES[k_]["name"], fs) for k_ in P17_CAT) + 1.5
    cw = (w - lw_) / 12.0
    rh = fs * 1.3
    pg.text(u"THE YEAR OF EACH SPECIES", x, ytop - P17_HEAD, P17_HEAD, COL["ink_dark"], bold=True)
    y = ytop - P17_HEAD - 2.0
    for m in range(12):
        pg.text(P17_MONTHS[m], x + lw_ + (m + 0.5) * cw, y - fs, fs, COL["ink2"], align="C")
    y -= fs * 1.5
    y0 = y
    yb = y - len(P17_CAT) * rh
    for m in range(13):
        pg.line([(x + lw_ + m * cw, y0 + 0.4), (x + lw_ + m * cw, yb)], COL["faint"], 0.06)
    for i, key in enumerate(P17_CAT):
        mo = pla_months(key)
        yy = y - i * rh
        pg.text(PLA_SPECIES[key]["name"], x, yy - rh + fs * 0.35, fs, COL["ink"])
        for m in mo.get("leaf") or []:
            pg.poly([rect(x + lw_ + (m - 1) * cw, yy - rh + 0.45, x + lw_ + m * cw, yy - 0.45)], fill=P17_LEAF)
        for m in mo.get("bloom") or []:
            pg.poly([rect(x + lw_ + (m - 1) * cw + 0.3, yy - rh * 0.64, x + lw_ + m * cw - 0.3, yy - rh * 0.36)],
                    fill=P17_BLOOM)
        for m in mo.get("cut") or []:
            xm = x + lw_ + (m - 0.5) * cw
            pg.line([(xm - 0.7, yy - rh + 0.5), (xm + 0.7, yy - 0.5)], COL["ink"], 0.2)
            pg.line([(xm - 0.7, yy - 0.5), (xm + 0.7, yy - rh + 0.5)], COL["ink"], 0.2)
    y = yb - fs * 1.5
    xx = x
    for kind, lab in (("leaf", u"in leaf"), ("bloom", u"in flower"), ("cut", u"flower heads cut")):
        if kind == "leaf":
            pg.poly([rect(xx, y - 0.1, xx + 4.0, y + fs * 0.7)], fill=P17_LEAF)
        elif kind == "bloom":
            pg.poly([rect(xx, y + 0.15, xx + 4.0, y + fs * 0.45)], fill=P17_BLOOM)
        else:
            pg.line([(xx + 1.3, y), (xx + 2.7, y + fs * 0.7)], COL["ink"], 0.2)
            pg.line([(xx + 1.3, y + fs * 0.7), (xx + 2.7, y)], COL["ink"], 0.2)
        pg.text(lab, xx + 5.0, y, fs, COL["ink"])
        xx += 5.0 + text_w(lab, fs) + 4.0
    return y - fs * 0.6


def _p17_materials(pg, x, ytop, w):
    """what the sections draw (G1): the cut materials and the water lines, two columns; returns the bottom y"""
    fs = P17_FS
    pa = _wat_pal()
    rows = [("earth", u"ground"), ("stone", u"stone wall"), ("gravel", u"gravel bed"), ("concrete", u"concrete"),
            ("avg", u"average flow"), ("q100", u"Q100 level"), ("q500", u"Q500 level"), ("co", u"callout: key under each cut")]
    half = (len(rows) + 1) // 2
    cw = w / 2.0
    low = ytop
    for i, (kind, lab) in enumerate(rows):
        xx = x + (i // half) * cw
        y = ytop - (i % half) * fs * 1.45 - fs
        sm = [(xx, y - 0.4), (xx + 4.0, y - 0.4), (xx + 4.0, y + fs * 0.8), (xx, y + fs * 0.8)]
        if kind in ("earth", "stone", "gravel", "concrete"):
            _p17_put(pg, sct_hatch_fill(sm, kind, 2.0, SCT["cut"], 0.15))
        elif kind == "avg":
            _p17_put(pg, [("poly", sm, pa["sec"], None, 0.1), ("line", [sm[3], sm[2]], SEC["hatch"], 0.3)])
        elif kind == "co":
            r_ = 0.75 * P17_CO
            _p17_put(pg, [("poly", sec_ellipse(xx + 2.0, y + fs * 0.35, r_, r_, 20), "FFFFFF", SEC["ink"], 0.15),
                          ("text", u"1", xx + 2.0, y + fs * 0.35 - 0.36 * P17_CO, 0.85 * P17_CO, SEC["ink"], True, "C")])
        else:
            pg.line([(xx, y + fs * 0.3), (xx + 4.0, y + fs * 0.3)], pa[kind], 0.25,
                    dash=[1.2, 0.6] if kind == "q100" else [0.4, 0.5])
        pg.text(lab, xx + 5.0, y, fs, COL["ink"])
        low = min(low, y - fs * 0.4)
    return low


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
    """a section Page put with its top-left at (x, ytop), at 1:1 (its scale is its own), cutouts included; its box"""
    b = _p17_bb(part.items)
    pg.items += _p17_move(part.items, x - b[0], ytop - b[3])
    return (x, ytop - (b[3] - b[1]), x + b[2] - b[0], ytop)


def _p17b_draw(pg, box, specs, style, log):
    """page B in box, in style "b" or "a": row 1 F2 with the key map (all four cuts + outline), giant reed and the
    materials at its right; row 2 F4 with the year of each species; row 3 W1 and S4 side by side. Every section at
    1:500 (D6), its own scale bar. Returns the bbox of what it drew."""
    x0, y0, x1, y1 = box
    n0 = len(pg.items)
    G = 5.0
    parts = {}
    for nm in ("F2", "F4", "W1", "S4"):
        if nm in specs:
            try:
                parts[nm] = _p17_section(specs[nm], style, log)
            except Exception as ex:
                log.append(u"WARNING p.17 section {} ({}) not drawn: {}: {}".format(nm, style, type(ex).__name__, ex))
                import traceback as _tb
                log.append(_tb.format_exc()[-600:])
    wd = dict((nm, _p17_bb(p_.items)) for nm, p_ in parts.items())
    wd = dict((nm, b[2] - b[0]) for nm, b in wd.items())
    y = y1
    # row 1: F2 | key map, giant reed, the materials
    low, xr = y, x0
    if "F2" in parts:
        b2 = _p17_place(pg, parts["F2"], x0, y)
        low, xr = b2[1], b2[2] + G
    cw = x1 - xr
    kb = _p17_key(pg, xr, y, cw, 26.0, P17_CUTS, None, log)
    yy = _p17_remove(pg, xr, (kb[1] if kb else y) - 4.0, cw, log) - 4.0
    yy = _p17_materials(pg, xr, yy, cw)
    y = min(low, yy) - G
    # row 2: F4 | the year of each species
    if "F4" in parts:
        b4 = _p17_place(pg, parts["F4"], x0, y)
        xcal = b4[2] + G
    else:
        b4, xcal = (x0, y, x0, y), x0
    yk = _p17_calendar(pg, xcal, y, x1 - xcal, log)
    y = min(b4[1], yk) - G
    # row 3: W1 and S4 side by side, the room between them shared
    w1, w3 = wd.get("W1", 0.0), wd.get("S4", 0.0)
    gap = max(G, (x1 - x0) - w1 - w3)
    low = y
    if "W1" in parts:
        low = min(low, _p17_place(pg, parts["W1"], x0, y)[1])
    if "S4" in parts:
        low = min(low, _p17_place(pg, parts["S4"], x0 + w1 + gap if w1 else x0, y)[1])
    wide = max([wd.get("F2", 0.0) + G + 50.0, wd.get("F4", 0.0) + G + 75.0, w1 + w3 + G])
    if low < y0 - 0.5 or wide > x1 - x0 + 0.5:
        log.append(u"WARNING p.17 page B ({}): {:.0f} x {:.0f} mm, more than the {:.0f} x {:.0f} mm of the box".format(
            style, wide, y1 - low, x1 - x0, y1 - y0))
    return _p17_bb(pg.items[n0:])


def p17b_page(pg, box, opt, log):
    """page B (wb_plants_b): the four cuts at 1:500 from the cut registry, in style a only (D1 a, Aras 31 Oct: one
    style), drawn in box; crops wb_plants_b and its style a alias wb_plants_b_a (the same drawing). The meaningless
    triangles are off (G14 / U22); the G14 grounding line goes to the log once. Returns [(crop id, bbox, den)]."""
    if _P17_MEMO.get("run") != id(pg):                  # a new run reads its data afresh
        _P17_MEMO.clear()
        _P17_MEMO["run"] = id(pg)
    tri = sf_triangles(walls=False, aggregate=False)
    specs = {}
    for nm, fn in (("F2", _p17_f2), ("F4", _p17_f4), ("W1", _p17_f1), ("S4", _p17_f3)):
        try:
            specs[nm] = fn(log)
        except Exception as ex:
            log.append(u"WARNING p.17 section {} not built: {}: {}".format(nm, type(ex).__name__, ex))
    bb_a = _p17b_draw(pg, box, specs, "a", log)
    sf_triangles(**tri)
    ids = _p14_crop_ids("wb_plants_b") if callable(globals().get("_p14_crop_ids")) else \
        ["wb_plants_b", "wb_plants_b_b", "wb_plants_b_a"]
    out = [(ids[0], bb_a, P17_SEC_DEN), (ids[2], bb_a, P17_SEC_DEN)]
    cl = cut_log_line()
    if cl:
        log.append(u"p.17 " + cl)
    gl = sf_g14_line()
    if gl:
        log.append(gl)
    log.append(u"p.17 page B: sections {} at 1:{:,.0f}, style a".format(u", ".join(level_name(c_) for c_ in specs),
                                                                        P17_SEC_DEN))
    return out
