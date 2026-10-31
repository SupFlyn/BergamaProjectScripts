# p.17 planting and water (water board v6; revision 30 Oct 2026, T7: booklet p16 and p17). Two booklet pages:
#   page A (p17_page, crop wb_plants, booklet p16 "Which plant goes where"): two plan windows at one standard scale on
#        the shared basemap (M3 "detailed": streets, M11 buildings with roof ridges, M5 water), farms and orchards as one
#        field texture and one symbol per area (D7), the water spaces of the zone base, the planting as species
#        areas in wet-to-dry bands (R2-C _p17_drift_plan, R12-R14: drifts, overlapping crowns, no rows), July shade, the
#        four section lines of page B from the cut registry (W1, F2, S4, F4), the hubs and the numbered water spaces;
#        beside them the key map (M4: study-area outline + both windows) and the legend; under them the numbered list,
#        the planting logic (round 3, P16.3: band map, shares, height ranking) and the species catalogue (photo,
#        detailed section and plan from M6, foliage, water, role) with the giant reed "remove" card.
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
# round 3 (D2, P16.4): the summer strip is no longer drawn in plan (no squiggle); it is shown in the sections only
P17_ZONE = {"WT": ("CBEDE5", "8DB8AF"), "WD": ("C1D3DB", "889EA8"), "GR": ("EEEADD", "C9C3B0"),
            "WS": ("EEE8D6", "C9BFA6"), "WP": ("E6EEDD", "B9C6A2"), "ARM": ("B9D7DE", "5D7F8D"),
            "WIDEN": ("D3E4E8", "889EA8")}
# July shade: (hours under, colour, label, hatch spacing mm): drawn as an opaque fine hatch (G9: no alpha), so the
# water texture under it stays visible
P17_SHADE = ((2.0, "E6DCC6", u"under 2 h", 2.0), (5.0, "CDBF9F", u"2-5 h", 1.2), (99.0, "A99A78", u"over 5 h", 0.7))
P17_NEAT = 0.09                      # a map's neatline, mm (0.25 pt; D4: the only frame kept)
P17_DENS_PLAN = {"space": 0.65, "bank": 0.5}   # P16.2 (U14 "çok dolu"): plan planting density (drawing rule)
P17_CLEAR_M = 10.0                   # P16.2: an open clearing this far round each place people use (drawing rule)
# the four wet-to-dry bands (P17_BANDS) by the words of the page intro; one colour each (PLAN §2 palette), the same on
# p16 (plans, shares) and p17 (the band row under each section)
P17_BAND_NAME = (u"at the water", u"banks that flood", u"moist ground", u"dry tops")
P17_BAND_COL = ("5C7A86", "A2B6B5", "89986A", "8E8F8A")
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
_P17_LABS = []                       # the text boxes of the booklet page being drawn (lp_overlap_flag, G3)


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
    out = [(_p17_place_nm(h.get("name") or u""), tuple(h["xy"])) for h in hs if h.get("xy")]
    if out:
        return out
    known = [bridge_name(c_) for c_ in bridges_in_order()]
    return [(_p17_place_nm(n), p) for n, p in P12_PLACES if re.search(u"\\bK[1-6]\\b", n) or n in known]


def _p17_place_nm(n):
    """G16: a hub or place name with any K-code (K1-K6) as its real bridge name (names module)"""
    m = re.search(u"\\bK([1-6])\\b", n or u"")
    return bridge_name(u"K" + m.group(1)) if m else (n or u"")


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
    def opaque(hx, alpha):                               # G9 (round 3): no alpha; the tone mixed toward white instead
        return hx if not hx or alpha is None or alpha >= 0.999 else _sec_mix(hx, "FFFFFF", 1.0 - max(0.0, float(alpha)))

    def fill_fn(rings, hx, alpha, nonzero):
        sp.poly([r_ for r_ in rings if len(r_) >= 3], fill=opaque(hx, alpha))

    def line_fn(pts, hx, w_mm, dash_mm, alpha):
        d_ = None
        if dash_mm:
            d_ = list(dash_mm) if isinstance(dash_mm, (list, tuple)) else [dash_mm, dash_mm]
        sp.line(pts, opaque(hx, alpha), w_mm, dash=d_)
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


def _p17_drift_plan(ring, k, tf, mix, seed, density=1.0, avoid=None, max_n=3000, water=None, clear=None, page="p16"):
    """G9 planting in plan as R12-R14 draw it: species AREAS in wet-to-dry bands along the water. t = tf(x, y) (0 the
    water's edge .. 1 dry ground, > 1 nothing) puts a point in its band (P17_BANDS, edges _p17_band_t); each band is
    cut into drifts around irregular centres (5-16 m plus two crowns of the lead species across: plants.py PLA_GROUP
    group_m, a drawing rule), each drift led by one species with a second mixed in and, at its edges, the species of
    the neighbouring band whose niche reaches there (plants.py _pla_pick): interpenetrating, never rows. Crowns
    overlap (trunks 35-75 % of the two crowns apart: PLA_GROUP step), sizes vary (PLA_GROUP size inside the sourced
    range), no straight evenly spaced line (plants.py _pla_rowlike). Each drift is drawn as its area first (the lead
    species' tone, a fine edge: the band edges follow the water), then the low layer, then the crowns, tall on top.
    ring and avoid: page mm. Round 3: water = the water rings (page mm): no area and no plant in them, and every
    placed plant goes through water.py water_clip_points (G8, logged for page); clear = [(x, y, r mm)] open
    clearings round the places people use (P16.2): crowns are left out there, the drift's ground tint stays.
    Returns (shapes, placed [(key, x, y, crown_m)], drifts [(band, lead key, area ring, area mm²)])."""
    keys = [k_ for k_ in mix if k_ in PLA_NICHE]
    if not keys or len(ring) < 3:
        return [], [], []
    edges = _p17_band_t()
    rnd = _pla_rng(seed * 13 + 3)
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    bx0, by0, bw, bh = min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)
    area = _p17_area(ring)
    pools = [[k_ for k_ in keys if k_ in b_] for b_ in P17_BANDS]
    wet_r = [list(r_) for r_ in (water or ()) if len(r_) >= 3]
    wet_ix = _p17_ring_index(wet_r, 6.0) if wet_r else {}   # bucketed: the stream's rings are long

    def band(t):
        return sum(1 for e in edges if t > e)

    def free(x, y):
        return (_p17_pip((x, y), ring) and not any(_p17_pip((x, y), a) for a in (avoid or ())) and
                not (wet_ix and _p17_in(wet_ix, 6.0, (x, y))))

    def in_clear(x, y):
        return any(math.hypot(x - c_[0], y - c_[1]) < c_[2] for c_ in (clear or ()))

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
    sh, info = [], []
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
                info.append((b, d_[3], pts, _p17_area(pts)))
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
            if key is None or (canopy and in_clear(x, y)):
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
    if wet_r:                                            # G8: no crown over the water (one line logged by water.py)
        ok = set(id(e) for e in water_clip_points(placed[False] + placed[True], wet_r, page=page))
        placed = dict((c_, [e for e in placed[c_] if id(e) in ok]) for c_ in (False, True))
    for canopy in (False, True):
        for i, (x, y, r, key, h) in enumerate(sorted(placed[canopy], key=lambda e: e[4])):   # tall crowns on top
            sh += pla_plan(key, x, y, k, crown_m=2.0 * r / k, seed=seed + i * 3 + (7 if canopy else 0))
            out.append((key, x, y, 2.0 * r / k))
    return sh, out, info


def _p17_window(pg, x0, ytop, key, den, fit, log, start=1, seen=None):
    """one plan window, its top-left at (x0, ytop): farms and orchards (D7), the basemap (M11 buildings, M5 water),
    the water spaces, July shade, the planting as mixed scatters wet to dry (G9), the four section lines, the hubs and
    the numbered badges; frame, scale bar, name and north arrow under it. Round 3: no summer strip (D2), the places
    people use drawn at their section spots (G10), lighter planting with clearings (P16.2), plants clipped to land
    (G8), badges without leaders numbered in reading order from start (G3). Returns (bbox, badges [(n, code, name)],
    {code: species}, drift areas [(band, lead key, ring mm, area mm²)], text boxes)."""
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
    zs = [z for z in _p17_zones() if z["code"] != "STRIP" and any(inR(p) for p in z["ring"])]   # D2: no strip in plan
    arms = [a for a in _p17_arms(log) if any(inR(p) for p in a)]
    widen = [r for r in _p17_widen(log) if any(inR(p) for p in r)]
    for r in widen:
        sp.poly([[T(p) for p in r]], fill=P17_ZONE["WIDEN"][0], stroke=P17_ZONE["WIDEN"][1], lw=0.1)
    for z in zs:                                         # the water spaces, flat (planting comes after the shade)
        if z["code"] in P17_ZONE and z["code"] != "WT":
            f_, s_ = P17_ZONE[z["code"]]
            sp.poly([[T(p) for p in z["ring"]]], fill=f_, stroke=s_, lw=0.12)
    arm_bands = []
    for a in arms:
        P = [T(p) for p in a]
        arm_bands.append(_p14_band(P, 2.0 * P17_ARM_W * k))
        sp.poly([arm_bands[-1]], fill=P17_ZONE["ARM"][0], stroke=P17_ZONE["ARM"][1], lw=0.12)
    # July shade on the bed and the water spaces (5 m cells, three classes): an opaque fine hatch (G9: no alpha)
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
            col, hs_ = next((cl, hs) for lim, cl, _l, hs in P17_SHADE if hrs < lim)
            for p_, q_ in sec_hatch([T((x - hc, y - hc)), T((x + hc, y - hc)), T((x + hc, y + hc)),
                                     T((x - hc, y + hc))], hs_, 45.0):
                sp.line([p_, q_], col, 0.12)
    # P16.2 / G10: what is at each point, from the sections' own programme (the same place in plan and in section):
    # stepping stones, footbridge, viewing terraces, sun steps; their footprints stay unplanted, an open clearing
    # round each (no crowns), so the places read
    foot, clear, st_n = [], [], 0
    for kind, cid, ta, tb, rail in _p17_plan_structs(log):
        pa, pb = _p17_spec_pt(cid, ta), _p17_spec_pt(cid, tb)
        if not inR(((pa[0] + pb[0]) / 2.0, (pa[1] + pb[1]) / 2.0)):
            continue
        shp, fr = _p17_struct_plan(kind, T(pa), T(pb), rail)
        _p17_put(sp, shp)
        foot.append(fr)
        C = _p17_cen(fr)
        clear.append((C[0], C[1], P17_CLEAR_M * k))
        st_n += 1
    for name, xy in _p17_hubs(log):
        if inR(xy):
            X, Y = T(xy)
            clear.append((X, Y, P17_CLEAR_M * k))
    # the planting (G9, M6): lined basin cells; each space a mixed scatter at its band; the side arms and the stream
    # banks wet to dry by the distance to the water. Plants never stand in water (water_clip_points, G8), buildings,
    # streets, fields or on the places people use.
    cell = 6.0
    wet = water + [[T(p) for p in z["ring"]] for z in zs if z["code"] == "WD"] + arm_bands
    widx = _p17_edge_index(wet, cell)
    wet_in = _p17_ring_index(wet, cell)
    bld_in = _p17_ring_index(bld, cell)
    placed, taken, geo = {}, [], []
    ds_, db_ = P17_DENS_PLAN["space"], P17_DENS_PLAN["bank"]

    def note(code, pl, info=()):
        s_ = placed.setdefault(code, [])
        for q in pl:
            if q[0] not in s_:
                s_.append(q[0])
        geo.extend(info)
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
                note("WT", [("reed",), ("mint",)], [(0, kind, rr, _p17_area(rr)) for kind, rr in cl_])
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
                shp, pl, inf = _p17_drift_plan(Rp, k, lambda x_, y_, t_=t_: t_, list(P17_MIX[code]), 40 + 7 * i,
                                               density=ds_, avoid=foot, water=wet, clear=clear)
                _p17_put(sp, shp)
                note(code, pl, inf)
            elif code == "WP":
                band = P17_WP_M * k

                def t_wp(x_, y_):
                    p_ = (x_, y_)
                    if _p17_in(wet_in, cell, p_) or _p17_in(bld_in, cell, p_):
                        return 9.0
                    return min(1.0, _wat_near_edge(widx, cell, p_, band)[0] / band)
                shp, pl, inf = _p17_drift_plan(Rp, k, t_wp, list(P17_MIX["WP"]), 60 + 7 * i, density=ds_,
                                               avoid=foot, water=wet, clear=clear)
                _p17_put(sp, shp)
                note(code, pl, inf)
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
            shp, pl, inf = _p17_drift_plan(ring, k, t_arm, list(P17_MIX["ARM"]), 90 + i, density=ds_,
                                           avoid=foot, water=wet, clear=clear)
            _p17_put(sp, shp)
            note("ARM", pl, inf)
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
        shp, pl, inf = _p17_drift_plan(Rr, k, t_bank, list(P17_MIX["BANK"]), 7 if key == "A" else 8, density=db_,
                                       avoid=foot, water=wet, clear=clear)
        _p17_put(sp, shp)
        note("BANK", pl, inf)
    except Exception as ex:
        log.append(u"p.17 plan {}: stream banks not planted: {}: {}".format(key, type(ex).__name__, ex))
    # the section lines of page B (cut registry: W1, F2, S4, F4), dash-dot, a view-direction triangle at each end (the
    # way page B looks: toward the ground _p17_topo draws behind the cut), the cut-end names (D6) on the other side
    taken_l, labs_ = [], []
    for cid in P17_CUTS:
        ends_ = cut_end_labels(level_name(cid))
        a, b = level_ends(cid)
        La = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
        O, V = T(a), T((a[0] - (b[1] - a[1]) / La, a[1] + (b[0] - a[0]) / La))
        vl = math.hypot(V[0] - O[0], V[1] - O[1]) or 1.0
        vd = ((V[0] - O[0]) / vl, (V[1] - O[1]) / vl)
        for run in _p14_clip_line([T(a), T(b)], (R[0] + 3.0, R[1] + 3.0, R[2] - 3.0, R[3] - 3.0)):
            sp.line(run, COL["ink_dark"], 0.3, dash=[2.4, 0.7, 0.4, 0.7])
            for (px, py), lab in ((run[0], ends_[0]), (run[-1], ends_[1])):
                tri = [(px + vd[0] * 2.2, py + vd[1] * 2.2), (px - vd[1] * 0.9, py + vd[0] * 0.9),
                       (px + vd[1] * 0.9, py - vd[0] * 0.9)]
                sp.poly([tri], fill=COL["ink_dark"])
                lx, ly = px - vd[0] * 2.2, py - vd[1] * 2.2 - P17_FS * CAP / 2.0
                sp.text(lab, lx, ly, P17_FS, COL["ink_dark"], bold=True, align="C")
                tb_ = _p17_text_box(lab, lx, ly, P17_FS, True, "C")
                taken_l += [tb_, (min(q[0] for q in tri), min(q[1] for q in tri), max(q[0] for q in tri),
                                  max(q[1] for q in tri))]
                labs_.append(tb_)
    # hubs: the icon and the place name (G16: real names, no K-codes)
    for name, xy in _p17_hubs(log):
        if inR(xy):
            X, Y = T(xy)
            _p17_put(sp, ico_badge("hub", X, Y, 4.0))
            sp.text(name, X + 2.8, Y - P17_FS * 0.35, P17_FS, COL["ink_dark"], bold=True)
            tb_ = (X + 2.6, Y - P17_FS * 0.35 - P17_FS * 0.3, X + 2.8 + text_w(name, P17_FS, True), Y + P17_FS * 0.5)
            taken_l += [(X - 2.0, Y - 2.0, X + 2.0, Y + 2.0), tb_]
            labs_.append(tb_)
    # numbered badges, one per water space (G3): on the spot or right beside it, never a leader; numbered in reading
    # order from start (window A, then B); a space already numbered in A keeps its number (seen)
    seen = seen if seen is not None else {}
    want = []
    for _n, code, name, _keys in PLANT_SITES:
        if code == "STRIP":
            continue
        at = None
        if code == "ARM":
            if arms:
                at = T(_p17_along(arms[0], 0.5 * sum(math.hypot(q[0] - p[0], q[1] - p[1])
                                                     for p, q in zip(arms[0][:-1], arms[0][1:])))[0])
        else:
            cand = [z for z in zs if z["code"] == code]
            if cand:
                at = T(_p17_cen(max(cand, key=lambda z_: len(z_["ring"]))["ring"]))
        if at and R[0] + 3.0 <= at[0] <= R[2] - 3.0 and R[1] + 3.0 <= at[1] <= R[3] - 3.0:
            want.append((code, name, at))
    got = lp_place([dict(x=at[0], y=at[1], w=3.8, h=3.8, r=0.8) for _c, _nm, at in want], obstacles=taken_l,
                   bounds=(R[0] + 1.0, R[1] + 1.0, R[2] - 1.0, R[3] - 1.0), pad=0.3, sizes=(1.0,))
    badges, n = [], start
    for j in lp_reading_order([at for _c, _nm, at in want]):
        code, name, at = want[j]
        g = got[j]
        bx_ = g["box"] if g else (at[0] - 1.9, at[1] - 1.9, at[0] + 1.9, at[1] + 1.9)
        if code in seen:
            num = seen[code]
        else:
            num, n = n, n + 1
            seen[code] = num
            badges.append((num, code, name))
        _p17_badge(sp, num, (bx_[0] + bx_[2]) / 2.0, (bx_[1] + bx_[3]) / 2.0)
        taken_l.append(bx_)
        labs_.append(bx_)
    pg.items += _p17_clip_items(sp.items, R)
    pg.poly([rect(*R)], fill=None, stroke=COL["ink2"], lw=P17_NEAT)      # a map keeps a thin neatline (D4)
    # under it: the scale bar, the window's name and scale, the north arrow
    yb = R[1] - 4.0
    bb = _p12_bar(pg, R[0], yb, den, P17_BAR.get(den, (0, 20, 50, 100)))
    lab = u"{} · plan · 1:{:,.0f}".format(P17_WIN_NAME[key], den)
    pg.text(lab, bb[2] + 3.0, yb, P17_FS, COL["ink"], bold=True)
    labs_.append(_p17_text_box(lab, bb[2] + 3.0, yb, P17_FS, True))
    nd = (T((0.0, 100.0))[0] - T((0.0, 0.0))[0], T((0.0, 100.0))[1] - T((0.0, 0.0))[1])
    nl = math.hypot(*nd) or 1.0
    nx, ny = R[2] - 4.0, yb - 1.0
    if bb[2] + 3.0 + text_w(lab, P17_FS, True) + 1.5 > nx - 5.0:    # the label reaches it (G3): top right, inside
        nx, ny = R[2] - 4.5, R[3] - 10.0
        pg.poly([rect(nx - 3.5, ny - 3.5, nx + 3.5, ny + 8.5)], fill=COL["white"])   # G17: no stroke
    nb = _p17_north(pg, nx, ny, (nd[0] / nl, nd[1] / nl), 4.0)
    wat_draw_order_lines(page=u"p16 plan " + key, steps=["ground", "water", "structures", "vegetation", "labels"])
    log.append(u"p.16 plan {}: {} places drawn in plan (stones, bridge, terraces, sun steps), {} badges".format(
        key, st_n, len(want)))
    return (min(R[0], bb[0]), min(bb[1], nb[1], yb - 1.5), R[2], R[3]), badges, placed, \
        dict(drifts=geo, water=wet, R=R, den=den, nd=(nd[0] / nl, nd[1] / nl)), labs_


def _p17_specs(log):
    """the four section specs of page B (W1, F2, S4, F4), built once a run: page A draws their places in plan from
    them, so plan and section show the same thing at the same spot"""
    if "specs" not in _P17_MEMO:
        out = {}
        for nm, fn in (("F2", _p17_f2), ("F4", _p17_f4), ("W1", _p17_f1), ("S4", _p17_f3)):
            try:
                out[nm] = fn(log)
            except Exception as ex:
                log.append(u"WARNING p.17 section {} not built: {}: {}".format(nm, type(ex).__name__, ex))
        _P17_MEMO["specs"] = out
    return _P17_MEMO["specs"]


def _p17_spec_pt(cid, t):
    """the survey point of a section spec's coordinate t: S4 m across from the bed's low point (p.14's), the other
    cuts m along from their first end"""
    return _p17_s4_pt(t) if cid == "S4" else _p17_cut_pt(cid, t)


def _p17_plan_structs(log):
    """G10 in plan: [(kind, cut id, t from, t to, rail end)] the stepping stones, footbridges and viewing terraces of
    the section specs, and S4's sun steps (kind "steps")"""
    out = []
    for cid, sp_ in sorted(_p17_specs(log).items()):
        for st in sp_.get("structures", []):
            if st[0] in ("stones", "bridge", "terrace"):
                out.append((st[0], cid, st[1], st[2], st[3] if st[0] == "terrace" else None))
        for pe in sp_.get("people", []):
            if pe[0] == "sun_steps":
                out.append(("steps", cid, pe[1], pe[2], None))
    return out


def _p17_struct_plan(kind, A, B, rail=None):
    """a place people use as a plan symbol from A to B (page mm, along the cut): stones a staggered row of stones,
    bridge a deck with two rails, terrace a deck with its rail at the rail end ("a" = A), steps parallel treads. Sizes
    at least legible at the plan's scale (symbols, explained in the legend; drawing rules, never printed). Returns
    (shapes, footprint ring)."""
    L = math.hypot(B[0] - A[0], B[1] - A[1]) or 1e-6
    d = ((B[0] - A[0]) / L, (B[1] - A[1]) / L)
    n_ = (-d[1], d[0])
    C = ((A[0] + B[0]) / 2.0, (A[1] + B[1]) / 2.0)
    Lp = max(L, {"stones": 3.0, "bridge": 2.6, "terrace": 2.2, "steps": 1.6}[kind])
    half = {"stones": 0.6, "bridge": 0.55, "terrace": 0.75, "steps": 0.9}[kind]

    def at(s, o):
        return (C[0] + d[0] * s + n_[0] * o, C[1] + d[1] * s + n_[1] * o)
    sh = []
    ink = COL["ink_dark"]
    if kind == "stones":
        for i in range(4):
            s = -Lp / 2.0 + Lp * (i + 0.5) / 4.0
            p = at(s, 0.22 if i % 2 else -0.22)
            sh.append(("poly", sec_ellipse(p[0], p[1], 0.36, 0.3, 10), "C9BBA2", COL["ink2"], 0.08))
    elif kind in ("bridge", "terrace"):
        ring = [at(-Lp / 2.0, -half), at(Lp / 2.0, -half), at(Lp / 2.0, half), at(-Lp / 2.0, half)]
        sh.append(("poly", ring, "FFFFFF" if kind == "bridge" else "E7E1D3", ink, 0.12))
        if kind == "bridge":
            for o in (-half, half):
                sh.append(("line", [at(-Lp / 2.0, o), at(Lp / 2.0, o)], ink, 0.22))
        else:
            s = -Lp / 2.0 if rail == "a" else Lp / 2.0
            sh.append(("line", [at(s, -half), at(s, half)], ink, 0.3))
    else:
        for i in range(4):
            s = -Lp / 2.0 + Lp * i / 3.0
            sh.append(("line", [at(s, -half), at(s, half)], ink, 0.14))
    m = 0.4
    foot = [at(-Lp / 2.0 - m, -half - m), at(Lp / 2.0 + m, -half - m), at(Lp / 2.0 + m, half + m),
            at(-Lp / 2.0 - m, half + m)]
    return sh, foot


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
    low = Rk[1]
    if labs:                                             # G3: names on or beside their cut, else numbers + key row
        L_ = [dict(x=p[0], y=p[1], w=text_w(nm, FS_MIN, True) + 0.6, h=FS_MIN * 1.05, rank=0, r=0.8, text=nm)
              for nm, p in labs]
        got = lp_place(L_, obstacles=marks, bounds=Rk)
        for (nm, p), g in zip(labs, got):
            bxl = g["box"]
            out.append(("text", str(g["number"]) if g.get("number") else nm, bxl[0] + 0.3, bxl[1] + FS_MIN * 0.25,
                        FS_MIN, P17_KEYCOL, True, "L", None, None))
            _P17_LABS.append(bxl)
        rows = u"   ".join(u"{} {}".format(n_, L__["text"]) for n_, L__ in lp_key(L_, got))
        if rows:                                         # the key of the numbered cuts, under the map
            low = Rk[1] - 1.2 - FS_MIN
            out.append(("text", rows, Rk[0], low, FS_MIN, P17_KEYCOL, True, "L", None, None))
            _P17_LABS.append(_p17_text_box(rows, Rk[0], low, FS_MIN, True))
            low -= FS_MIN * 0.4
    pg.items += out
    pg.poly([rect(*Rk)], fill=None, stroke=COL["ink2"], lw=P17_NEAT)   # a map keeps a thin neatline (D4)
    nb = _p17_north(pg, x0 + na / 2.0, Rk[3] - 6.0, (0.0, 1.0), 3.5)
    return (x0, min(low, nb[1]), Rk[2], Rk[3])


# ---------------------------------------------------------------- page A: legend, numbered list, catalogue
def _p17_legend(pg, x, ytop, w, log):
    """a drawn sample and a plain name for every symbol the plans draw (G1); returns the bottom y"""
    fs = P17_FS
    y = ytop
    pg.text(u"ON THE PLANS", x, y - fs, fs, COL["ink_dark"], bold=True)
    y -= fs * 1.9
    rows = [("water", place_name("stream") + u", darker = deeper"),
            ("stones", u"stepping stones: cross the summer strip dry-shod"),
            ("bridge", u"footbridge: cross the side arm dry-shod"),
            ("terrace", u"viewing terrace: a step-free view over the water"),
            ("steps", u"sun steps: sit in the sun, facing the water"),
            ("cell", u"lined basin cell: reed, water mint"),
            ("space", u"water space: named by its number (list under the plans)"),
            ("plant", u"planting areas, wet to dry: each tint led by one species, each crown its species"),
            ("maize", u"farmland: field texture, one crop symbol"), ("olive", u"orchard: one olive symbol"),
            ("bld", u"building, roof ridges"), ("cut", u"section line, triangle: the way the section looks"),
            ("hub", u"hub")]
    if _p17_shade(log):
        rows += [("shade", u"July shade on the water: " + u", ".join(l_ for _, _, l_, _h in P17_SHADE))]
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
        elif kind in ("stones", "bridge", "terrace", "steps"):
            if kind in ("stones", "bridge"):
                pg.poly([rect(*sm)], fill=pa["surface"], stroke=pa["edge"], lw=0.25)
            _p17_put(pg, _p17_struct_plan(kind, (x + 1.2, yy + 0.6), (x + 4.8, yy + 0.6), "a")[0])
        elif kind == "shade":                            # G9: the opaque hatch the plans draw, light to dense
            pg.poly([rect(*sm)], fill=pa["surface"], stroke=pa["edge"], lw=0.25)
            for j_, (_l, col, _t, hs_) in enumerate(P17_SHADE):
                xa_ = sm[0] + j_ * 2.0
                for p_, q_ in sec_hatch([(xa_, sm[1]), (xa_ + 2.0, sm[1]), (xa_ + 2.0, sm[3]), (xa_, sm[3])],
                                        hs_ * 0.5, 45.0):
                    pg.line([p_, q_], col, 0.12)
        elif kind == "space":
            f_, s_ = P17_ZONE["WP"]
            pg.poly([rect(*sm)], fill=f_, stroke=s_, lw=0.12)
            _p17_badge(pg, 1, x + 3.0, yy + 0.6, 2.6)
        else:
            f_, s_ = P17_ZONE[kind]
            pg.poly([rect(*sm)], fill=f_, stroke=s_, lw=0.12)
        t = lab
        ly = r28_para(pg, x + 7.5, y + fs * 1.28, w - 7.5, t, fs, COL["ink"])
        y = min(y, ly) - fs * 1.55
    return y


def _p17_list(pg, x, ytop, w, badges, placed):
    """the numbered water spaces with the species drawn there (R35), in two columns, in the badges' reading order
    (G3: badges [(n, code, name)] from the plans); returns the bottom y"""
    fs = P17_FS
    items = sorted(badges)
    cw = (w - 6.0) / 2.0
    half = (len(items) + 1) // 2
    low = ytop
    for col, part in enumerate((items[:half], items[half:])):
        y = ytop
        xx = x + col * (cw + 6.0)
        for n, code, name in part:
            _p17_badge(pg, n, xx + 1.8, y - 1.8)
            got = [k_ for k_ in P17_CAT if k_ in (placed.get(code) or ())]
            if got:
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
    """one catalogue column (R36): photo, the two views, name with its sources, foliage, water, role (round 3, G4:
    the height is printed once, in the height ranking of the logic diagram). Returns the bottom y."""
    fs = P17_FS
    key = sp_["key"]
    path, credit = photo
    y = ytop
    pg.poly([rect(x, y - PHOTO_H, x + PHOTO_W, y)], fill=C["paper"])     # G17: no frame
    if path:
        photos.append((x, y - PHOTO_H, x + PHOTO_W, y, path))
    y -= PHOTO_H + 1.2
    _p17_views(pg, key, x, y - 15.0, w, 15.0)
    y -= 16.5
    name = _p17_name(key) + u" " + cite(sp_["src"]) + (cite(credit) if credit else u"")
    y = para(pg, x, y, w, name, fs, COL["ink_dark"], bold=True) - 0.4
    fo = _p17_foliage(key)
    if fo:
        y = para(pg, x, y, w, fo, fs, COL["ink"]) - 0.4
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
    """the species, wet to dry, one column each, along the foot of page A, then (P16.5, D5) the giant reed card: take
    it out; bottom-aligned at ybot. Returns its box."""
    sps = [s_ for k_ in P17_CAT for s_ in SPECIES if s_["key"] == k_]
    n = len(sps)
    gr = 4.0                                             # the gap before the giant reed card
    gap = max(0.6, min(3.0, (x1 - x0 - (n + 1) * PHOTO_W - gr) / max(n - 1, 1)))
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
    hmax = max([-_p17_card(Page(0, 0), 0.0, 0.0, w, s_, (None, None), []) for s_ in sps] +
               [-_p17_card_remove(Page(0, 0), 0.0, 0.0, w, log, measure=True)])
    xr = x0 + n * w + (n - 1) * gap + gr
    if measure:
        return (x0, ybot, xr + w, ybot + hmax)
    ytop = ybot + hmax
    for i, (s_, p_) in enumerate(zip(sps, photos)):
        _p17_card(pg, x0 + i * (w + gap), ytop, w, s_, p_, PHOTOS)
    _p17_card_remove(pg, xr, ytop, w, log)
    return (x0, ybot, xr + w, ytop)


def _p17_card_remove(pg, x, ytop, w, log, measure=False):
    """P16.5 (D5): the giant reed (Kargı) as the last card of the species strip: its photo crossed out, its name and
    sources, take it out and why (02 §5: only marked remove). Returns the bottom y."""
    fs = P17_FS
    key, words, src = SPECIES_REMOVE
    path, credit = None, None
    if not measure and PHOTO_ON[0] and key in PLANTS:
        if "photo_remove" not in _P17_MEMO:
            _P17_MEMO["photo_remove"] = plant_photo_of(key, log, {})[:2]
        path, credit = _P17_MEMO["photo_remove"]
    pg.poly([rect(x, ytop - PHOTO_H, x + PHOTO_W, ytop)], fill=C["paper"])   # G17: no frame
    if path:
        PHOTOS.append((x, ytop - PHOTO_H, x + PHOTO_W, ytop, path))
    _p17_put(pg, ico_cross(x + PHOTO_W - 3.5, ytop - 3.5, 5.0, COL["accent"]))
    y = ytop - PHOTO_H - 1.2
    y = para(pg, x, y, w, _p17_name(key) + u" " + cite(src) + (cite(credit) if credit else u""), fs,
             COL["ink_dark"], bold=True) - 0.4
    return r28_para(pg, x, y, w, words, fs, COL["accent"])


P17_FOL_COL = (("evergreen", "3C4733"), ("deciduous", "89986A"), ("herbaceous", "A2B6B5"), (u"not sourced", "DCD9D2"))


def _p17_fol_class(key):
    """evergreen / deciduous / herbaceous from the species' sourced foliage (plants.py), else: not sourced"""
    fo = (_p17_foliage(key) or u"").lower()
    for c_, _col in P17_FOL_COL[:3]:
        if fo.startswith(c_):
            return c_
    return u"not sourced"


def _p17_logic(pg, x0, ytop, w, h, geos, log):
    """P16.3 (idea R04: zones on plan, share bars, height ranking): why each plant goes where, from the plans' own
    planting and the species' sourced data only. (a) plan B's planting areas by wet-to-dry band at half the plans'
    scale; (b) two share bars over plans A and B: the bands' areas, and evergreen / deciduous / herbaceous by the area
    each drift's lead species covers (lined basin cells counted with reed and water mint); (c) the species ranked by
    their sourced maximum height (plants.py h_range), drawn at one true scale on one ground line, with the range and
    the sources. geos: the windows' geo dicts (drifts, water, R, den, nd). Returns its box."""
    fs = P17_FS
    yb = ytop - h
    # (a) the band map of plan B
    gB = geos.get("B") or {}
    wa = 95.0
    if gB.get("drifts"):
        R = gB["R"]
        th = ytop - fs * 1.3
        mh = th - 2.0 - (yb + 6.0)                       # room under the title, over the scale bar
        den_m = next((d_ for d_ in (2.0 * gB["den"], 4.0 * gB["den"]) if (R[2] - R[0]) * gB["den"] / d_ <= wa and
                      (R[3] - R[1]) * gB["den"] / d_ <= mh), 4.0 * gB["den"])
        f = gB["den"] / den_m
        Rm = (x0, th - 2.0 - (R[3] - R[1]) * f, x0 + (R[2] - R[0]) * f, th - 2.0)

        def M(p):
            return (Rm[0] + (p[0] - R[0]) * f, Rm[1] + (p[1] - R[1]) * f)
        pg.text(u"PLANTING BANDS · plan B · 1:{:,.0f}".format(den_m), x0, th, fs, COL["ink_dark"], bold=True)
        _P17_LABS.append(_p17_text_box(u"PLANTING BANDS · plan B · 1:{:,.0f}".format(den_m), x0, th, fs, True))
        pg.poly([rect(*Rm)], fill=COL["white"])
        pa = _wat_pal()
        for r_ in gB.get("water") or []:
            c_ = _p14_clip_ring(list(r_), R)
            if c_:
                pg.poly([[M(p) for p in c_]], fill=pa["surface"])
        for b, _lead, ring, _a in gB["drifts"]:
            c_ = _p14_clip_ring(list(ring), R)
            if c_:
                pg.poly([[M(p) for p in c_]], fill=_sec_mix(P17_BAND_COL[b], SEC["paper"], 0.25))
        pg.poly([rect(*Rm)], fill=None, stroke=COL["ink2"], lw=P17_NEAT)
        bb = _p12_bar(pg, Rm[0], Rm[1] - 4.0, den_m, P17_BAR.get(den_m, (0, 50, 100, 200)))
        nd = gB.get("nd") or (0.0, 1.0)
        _p17_north(pg, Rm[2] - 3.0, Rm[1] - 5.5, nd, 3.0)
    # (b) the shares, plans A and B together (one standard scale, so page mm² / k² = m²)
    xb, wb = x0 + 100.0, 85.0
    bands, fol = [0.0] * len(P17_BANDS), dict((c_, 0.0) for c_, _ in P17_FOL_COL)
    for g_ in geos.values():
        kk = 1000.0 / g_["den"]
        for b, lead, _ring, a in g_.get("drifts") or []:
            bands[b] += a / (kk * kk)
            fol[_p17_fol_class(lead)] += a / (kk * kk)
    y = ytop
    for title, rows in ((u"WET TO DRY · planted area, plans A and B",
                         [(P17_BAND_NAME[i], P17_BAND_COL[i], bands[i]) for i in range(len(P17_BANDS))]),
                        (u"FOLIAGE · by the lead species' area",
                         [(c_, col, fol[c_]) for c_, col in P17_FOL_COL])):
        tot = sum(r_[2] for r_ in rows)
        pg.text(title, xb, y - fs, fs, COL["ink_dark"], bold=True)
        _P17_LABS.append(_p17_text_box(title, xb, y - fs, fs, True))
        y -= fs * 1.5 + 4.0
        xx = xb
        for nm, col, a in rows:                          # the 100 % bar
            if tot > 0 and a > 0:
                ww = wb * a / tot
                pg.poly([rect(xx, y, xx + ww, y + 3.6)], fill=col)
                xx += ww
        y -= 1.0
        for nm, col, a in rows:                          # its key: chip, name, m², %
            if a <= 0 or tot <= 0:
                continue
            y -= fs * 1.3
            pg.poly([rect(xb, y - 0.1, xb + 2.4, y + fs * 0.75)], fill=col)
            t = u"{} · {:,.0f} m² · {:.0f} %".format(nm, a, 100.0 * a / tot)
            pg.text(t, xb + 3.2, y, fs, COL["ink"])
            _P17_LABS.append(_p17_text_box(t, xb + 3.2, y, fs))
        y -= fs * 1.0
    log.append(u"p.16 logic: bands {} m², foliage {}".format(
        u" / ".join(u"{:,.0f}".format(a) for a in bands),
        u", ".join(u"{} {:,.0f} m²".format(c_, a) for c_, a in sorted(fol.items()) if a > 0)))
    # (c) the height ranking: sourced maximum heights, one true scale
    xc = x0 + 190.0
    wc = x0 + w - xc
    sps = sorted([k_ for k_ in P17_CAT if (PLA_SPECIES[k_].get("h_range") or (None, None))[1]],
                 key=lambda k_: -PLA_SPECIES[k_]["h_range"][1])
    title = u"HEIGHT · each species' sourced maximum, one scale"
    pg.text(title, xc, ytop - fs, fs, COL["ink_dark"], bold=True)
    _P17_LABS.append(_p17_text_box(title, xc, ytop - fs, fs, True))
    ax = 9.0                                             # the axis labels' column
    cw = (wc - ax) / max(1, len(sps))
    src_of = dict((s_["key"], s_["src"]) for s_ in SPECIES)

    def words(pg_, key, xx, yy):
        y_ = para(pg_, xx, yy, cw - 0.6, P17_SHORT.get(key, PLA_SPECIES[key]["name"].lower()), fs, COL["ink_dark"],
                  bold=True)
        y_ = para(pg_, xx, y_ - 0.3, cw - 0.6, (_p17_height(key) or u"") + u" " + cite(src_of.get(key, u"")), fs,
                  COL["ink"])
        return y_ - fs * 0.3
    tdeep = max(-words(Page(0, 0), k_, 0.0, 0.0) for k_ in sps) if sps else 0.0
    gy = yb + tdeep + 1.0                                # the ground line
    top = ytop - fs * 1.5 - 1.0
    hmax = max(PLA_SPECIES[k_]["h_range"][1] for k_ in sps) if sps else 1.0
    step = 10.0 if hmax > 20.0 else 5.0
    hgrid = step * math.ceil(hmax / step)
    ks = (top - gy) / hgrid                              # mm per m, the same for every species
    for v_ in [0.0, 5.0] + [step * i for i in range(1, int(hgrid / step) + 1) if step * i > 5.0]:
        yy = gy + v_ * ks
        pg.line([(xc + ax, yy), (xc + wc, yy)], COL["faint"] if v_ else COL["ink2"], 0.06 if v_ else 0.15)
        lab = u"{:.0f} m".format(v_)
        pg.text(lab, xc + ax - 1.0, yy - fs * 0.35, fs, COL["ink2"], align="R")
        _P17_LABS.append(_p17_text_box(lab, xc + ax - 1.0, yy - fs * 0.35, fs, False, "R"))
    for i, key in enumerate(sps):
        xm = xc + ax + (i + 0.5) * cw
        hi = PLA_SPECIES[key]["h_range"][1]
        crown = min(PLA_SPECIES[key]["crown_m"] or 1.0, 0.95 * cw / ks)   # a crown never wider than its column
        _p17_put(pg, pla_section(key, xm, gy, ks, h_m=hi, crown_m=crown, seed=i + 3))
        words(pg, key, xc + ax + i * cw + 0.3, gy - 1.0)
    return (x0, yb, x0 + w, ytop)


def p17_page(pg, box, opt, log):
    """page A (wb_plants, booklet p16): the two plan windows with the key map and the legend at their right, the
    numbered water spaces under them, the planting-logic diagram (P16.3) in the band that was empty (P16.1), the
    species strip with the giant reed card (P16.5) along the foot. Everything measured first so the page fits its box
    (G2). Returns [(crop id, bbox, den)]."""
    if _P17_MEMO.get("run") != id(pg):                  # a new run reads its data afresh
        _P17_MEMO.clear()
        _P17_MEMO["run"] = id(pg)
    del _P17_LABS[:]
    x0, y0, x1, y1 = box
    W = min(x1 - x0, P17_W)
    x1 = x0 + W
    n0 = len(pg.items)
    G = 5.0
    LG = 56.0                                           # the key map and legend column, mm
    LOGIC = (40.0, 58.0)                                # the logic diagram's height, least and most, mm
    cb = _p17_catalogue(pg, x0, y0, x1, log, measure=True)
    ch = cb[3] - cb[1]
    ytop = y1 - P17_HEAD - 2.0                          # room for the window letters
    hmax = ytop - y0 - ch - LOGIC[0] - 4 * 4.4 - 4 * G - 9.0   # the list (four lines), the gaps, the scale bar row
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
    seen = {}
    ba, na, sa, ga, la = _p17_window(pg, x0, ytop, "A", den, fa, log, start=1, seen=seen)
    gap = max(P17_WIN_GAP, 0.5 * (W - LG - G - fa[0] - fb[0]))   # the room left shared: a clear gap, A and B
    gap = min(gap, max(G, W - LG - G - fa[0] - fb[0]))             # never pushing B into the column
    pg.text(u"B", ba[2] + gap, ytop + 1.2, P17_HEAD, COL["accent"], bold=True)
    bb_, nb, sb_, gb, lb = _p17_window(pg, ba[2] + gap, ytop, "B", den, fb, log, start=1 + len(na), seen=seen)
    _P17_LABS.extend(la + lb)
    # the column: key map (outline + both windows), the legend
    kb = _p17_key(pg, x1 - LG, y1, LG, 30.0, (u"A", u"B"),
                  {u"A": _p17_win_corners(fa), u"B": _p17_win_corners(fb)}, log)
    ly = _p17_legend(pg, x1 - LG, (kb[1] if kb else y1) - 4.0, LG, log)
    placed = dict(sa)
    for c_, ks in sb_.items():
        placed[c_] = list(placed.get(c_, [])) + [k_ for k_ in ks if k_ not in placed.get(c_, [])]
    yl = _p17_list(pg, x0, min(ba[1], bb_[1]) - 4.0, bb_[2] - x0, na + nb, placed)
    # the logic diagram takes the room between the list / legend and the species strip (no dead band, P16.1)
    ylog = min(yl, ly) - G
    hl = ylog - (y0 + ch + G)
    if hl < LOGIC[0]:
        log.append(u"FLAG p.16: the logic diagram gets {:.0f} mm, under its {:.0f} mm".format(hl, LOGIC[0]))
    hl = min(LOGIC[1], max(LOGIC[0], hl))
    lgb = _p17_logic(pg, x0, ylog, W, hl, {"A": ga, "B": gb}, log)
    cat = _p17_catalogue(pg, x0, y0, x1, log)       # the species strip at the foot of the box
    if lgb[1] < cat[3] + 1.0:
        log.append(u"WARNING p.17 page A: {:.0f} mm taller than its box".format(cat[3] + 1.0 - lgb[1]))
    drawn_ = set(k_ for ks in placed.values() for k_ in ks)
    if drawn_ - set(P17_CAT):
        log.append(u"WARNING p.17: drawn but not in the catalogue: {}".format(u", ".join(sorted(drawn_ - set(P17_CAT)))))
    log.append(u"p.17 page A: plans 1:{:,.0f}, species planted {}, catalogue {} species, photos {}".format(
        den, len(drawn_), len(P17_CAT), sum(1 for p_ in _P17_MEMO.get("photos", []) if p_[0])))
    bbox = items_bbox(pg.items[n0:])
    # G3 done-when: the page's text against its other blocks and its box (the plans carry their own labels)
    lp_overlap_flag("p16", _P17_LABS, [(x1 - LG, ly, x1, (kb[1] if kb else y1) - 4.0), cat], bbox)
    return [("wb_plants", bbox, den)]


# ---------------------------------------------------------------- page B: the sections at 1:500
P17_WALL_T = 0.60                    # DSİ wall thickness drawn (no source; as p.04-05 and p.13 draw it)
P17_F1_RNG = (4.0, 69.0)             # W1: the part drawn, m from the SW end (the walk, the walls, the basins beyond)
P17_F1_BED = (22.1, 54.7)            # W1: the bed between the walls, m from the SW end (the survey's stream lines)
P17_F1_STRIP = (24.1, 28.9)          # W1: the zone base's strip; round 3 (DATA-1, ask 1 a) only its width is used: the
#                                      strip sits on the surveyed bed's low point (_p17_walled_bed)
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


def _p17_depth(spec, reg, X, P, gyx, zb, top, k, wl_y, style, log):
    """behind the cut (M8, D9; R16, R19 idea), the farthest layer first: its own ground from the survey contours
    (_p17_topo: layer 2 on the line P17_TOPO_D[0] m behind, layer 1 on P17_TOPO_D[1] m), the basemap houses of the
    band behind the cut (sf_back_buildings, SF_BACK_BAND: data height, else floors x BLD_STOREY; those nearer than the
    band's middle on layer 1, the rest on layer 2) standing on that layer's ground (sf_back_house: real profiles, faded
    by layer, G14 seated; a house whose roof would leave the drawing is left out), then mixed tree
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
    blds = sf_back_buildings(reg["id"], t0, t1, log=log)      # farthest first: [(t_a, t_b, h m, floors, d m behind)]
    dmid = 0.5 * (SF_BACK_BAND[0] + SF_BACK_BAND[1])
    sh, nh = [], 0
    for layer, d in zip((2, 1), P17_TOPO_D):
        g_, hs = gyx, []
        pr = prs.get(d)
        if pr:
            pts = P([(t, min(z, zb + top / k)) for t, z in pr])
            sh += sf_topo_back([pts], 0.0).shapes()
            g_ = sf_gy(pts)
        for ta, tb, h, fl, db in blds:                         # this layer's houses, before its trees
            if (1 if db < dmid else 2) != layer or tb - ta < 3.0:   # a sliver under one bay (sf_back_house's 3.0 m)
                continue
            hh = sf_back_house(X(ta), X(tb), g_, h, k, layer=layer, floors=fl)
            if not hh or _p17_shp_bb(hh)[3] > top:             # the roof would leave the drawing
                continue
            sh += hh
            hs.append((X(ta), X(tb)))
            nh += 1
        tr, _pl, _gr = pla_group_section(0.0, W, g_, k, t0=tfun, mix=["plane", "ash", "willow", "tamarisk", "olive"],
                                         seed=spec.get("seed", 3) * 7 + layer, layers=(layer,), style=style,
                                         density=0.6, avoid=hs, hires=False, detail=False, water=wl_y)
        sh += tr
    spec["n_houses"] = nh
    return sh


def _p17_group_sec(g, X, gyx, k, wl_y, avoid, style, use=()):
    """one planting group of a cut (G9): plants.py pla_group_section over the group's stretch, its band g["t"] from
    one end to the other, mixed species with overlapping crowns, a mid layer (D9 1) behind the cut plane (0), only
    emergent species where the ground lies under the average-flow water. The helper starts its first group up to
    half its widest gap in (PLA_GROUP gap_m): the run starts that far before the stretch and that lead-in is kept
    free, so a narrow stretch still gets its group. Round 3 (G15, K2): where the group reaches a use zone (use, page
    mm, +-2 m) the trees step back: the cut plane keeps the low planting only, the trees stand in layer 1 behind the
    people, paler by the module's layer tone. Returns (back shapes, front shapes, placed [(key, x mm, h, crown,
    layer)])."""
    x0, x1 = X(g["a"]), X(g["b"])
    lead = 0.5 * PLA_GROUP["gap_m"][1] * k
    ta, tb = g["t"]
    near = any(ua - 2.0 * k < x1 and ub + 2.0 * k > x0 for ua, ub in use)

    def tf(x):
        return ta + (tb - ta) * min(1.0, max(0.0, (x - x0) / max(1e-9, x1 - x0)))
    out = []
    for layer in (1, 0):
        mix = list(g["mix"])
        if layer == 0 and near:
            mix = [k_ for k_ in mix if not _pla_canopy(k_)]
        if not mix:
            out.append(([], []))
            continue
        sh_, pl_, _gr = pla_group_section(x0 - lead, x1, gyx, k, t0=tf, mix=mix, seed=g["seed"] * 3 + layer,
                                          layers=(layer,), style=style, density=g.get("dens", 1.0),
                                          avoid=list(avoid) + [(x0 - lead - 1.0, x0)], water=wl_y)
        out.append((sh_, pl_))
    return out[0][0], out[1][0], out[0][1] + out[1][1]


def _p17_co_text(keys, tags):
    """what a planting group is and does, "plane + ash: gives shade, ecological corridor", at most ~55 characters:
    species tallest first (up to three), what the group does (up to two)"""
    s = u""
    for nk, nt in ((3, 2), (2, 2), (2, 1), (1, 1)):
        nm = u" + ".join(P17_SHORT.get(k_, PLA_SPECIES[k_]["name"].lower()) for k_ in keys[:nk])
        s = nm + (u": " + u", ".join(P17_WHY[t] for t in tags[:nt]) if tags else u"")
        if len(s) <= 55:
            return s
    return s


def _p17_rows_w(items, W, nrows=2, gap=1.5):
    """labels [(xa, xb, tw, payload)] each centred over its span (page mm) on up to nrows rows, none overlapping
    (G3); a label that cannot sit within reach of its span gets None (it becomes a number). Returns [(payload, lx,
    row or None)] in the items' x order"""
    last = [-1e9] * nrows
    out = []
    for xa, xb, tw, pay in sorted(items, key=lambda q: (q[0] + q[1]) / 2.0):
        xm = (xa + xb) / 2.0
        reach = max(6.0, 0.5 * (xb - xa) + 4.0)
        got = None
        for r in range(nrows):
            lx = min(max(xm - tw / 2.0, 0.0), W - tw)
            lx = max(lx, last[r] + gap)
            if lx + tw <= W + 0.01 and abs(lx + tw / 2.0 - xm) <= reach:
                got = (r, lx)
                break
        if got is None:
            out.append((pay, xm, None))
            continue
        last[got[0]] = got[1] + tw
        out.append((pay, got[1], got[0]))
    return out


def _p17_tone(shapes, f):
    """shapes toned toward the paper by f (0..1): the depth tone of what lies beyond the cut, opaque (G9: no alpha)"""
    out = []
    for s_ in shapes:
        if s_[0] == "poly":
            out.append((s_[0], s_[1], _sec_mix(s_[2], SEC["paper"], f) if s_[2] else s_[2],
                        _sec_mix(s_[3], SEC["paper"], f) if s_[3] else s_[3], s_[4] if len(s_) > 4 else 0.1))
        elif s_[0] == "line" and s_[2]:
            out.append((s_[0], s_[1], _sec_mix(s_[2], SEC["paper"], f)) + tuple(s_[3:]))
        else:
            out.append(s_)
    return out


def _p17_spot_box(gyx, xa, xb, k, up_m=2.6):
    """the spot a zoom inset enlarges: xa..xb on the section, from 0.4 m under its lowest ground to up_m over its
    highest (people 1.75 m + room)"""
    ys = [gyx(xa + (xb - xa) * i / 10.0) for i in range(11)]
    return (xa, min(ys) - 0.4 * k, xb, max(ys) + up_m * k)


def _p17_inset_at(src, dw, dh, boxes, W, top):
    """a free place for a zoom inset dw x dh in the section's own sky: over everything drawn there (boxes, the spot),
    under the drawing's top, nearest the spot; None when there is none"""
    best = None
    cx = 0.5 * (src[0] + src[2])
    x = 0.5
    while x + dw <= W - 0.5:
        sky = max([b_[3] for b_ in boxes if b_[0] < x + dw + 1.0 and b_[2] > x - 1.0] + [src[3]])
        y0 = sky + 1.5
        if y0 + dh + P17_FS * 1.4 <= top:
            d = abs(x + dw / 2.0 - cx) + 0.2 * (y0 - src[3])
            if best is None or d < best[0]:
                best = (d, (x, y0, x + dw, y0 + dh))
        x += 2.0
    return best[1] if best else None


def _p17_section(spec, style, log, den=P17_SEC_DEN):
    """one cut at 1:den on its own Page (origin: x 0 = the start of the drawn part, y 0 = 1 m under its lowest
    ground) in style a (D1 a: cutouts over the drawn ground). Layers in M5's order: the sky (sf_atmosphere, its own
    variant by cut id, birds) and behind the cut, layer by layer, the survey ground, the houses on it and tree groups
    (_p17_depth: paler with distance, K2); the cut ground with the module's soil gradient (G15), the bed from the
    surveyed profile filled, the water at the average yearly flow, the Q100 / Q500 lines (M5 water_section);
    structures (lanes, terraces, ramp, bridge, stepping stones, benches, lamps, basins); the planting groups (G9 mixed,
    trees stepping back where people are, _p17_group_sec); the people of each zone in front (G10 / G15
    fig_place_zones, nobody in water deeper than wading); one zoom inset x2.5 on the cut's main use (people legible);
    the cut's end names and banks on top (D6); under it, like R07, the zones named with their reason and the
    planting band of every group with its species and what it does (numbers + key where a name does not fit its
    span, G3); caption and scale bar; the levels at the right. Text boxes in spec["labs"], the drawing's box in
    spec["dbox"] (section page mm)."""
    k = sf_k(den)
    fs = P17_FS
    t0, t1 = spec["rng"]
    prof = spec["prof"]
    reg = _p17_reg(spec["cid"])
    name = level_name(spec["cid"])
    zb = min(z for _t, z in prof) - 1.0
    Y = sf_y_of(zb, 0.0, k)
    labs = []

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
    # G15 soil: the module's gradient under the cut ground; water_section's flat earth fill is cleared (its hatch and
    # the stone / gravel fills stay)
    surf = P(prof)
    wl.add("ground", sct_soil_gradient(surf, min(p[1] for p in surf) - 1.0 * k, k))
    water_section(surf, k, Y, cid=reg["id"], banks=spec.get("banks", ("earth", "earth")), labels=False, style=style,
                  into=wl)
    wl.L["ground"] = [s_ for s_ in wl.L["ground"] if not (s_[0] == "poly" and s_[2] == SCT["earth"])]
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
        elif kind == "lamp":                             # street elements (G15), sizes are drawing rules
            _, t_, side = st
            wl.add("structures", sf_lamp(X(t_), gyx(X(t_)), k, side=side))
        elif kind == "bollard":
            wl.add("structures", sf_bollard(X(st[1]), gyx(X(st[1])), k))
        elif kind == "stones":                           # across the summer strip, on its floor, above the water
            _, a, b = st
            wl.add("structures", sf_stepping_stones(X(a), X(b), sf_ground_min(gyx, X(a), X(b)), wl_y, k,
                                                    above_m=P17_STONE_UP, seed=spec.get("seed", 3)))
    # the planting groups (G9): mixed groups in two depth layers; the trees step back where people are (G15)
    av = [(X(a), X(b)) for a, b in spec.get("avoid", [])]
    use = [(X(a), X(b)) for _z, a, b, _o in spec.get("people", [])]
    back, front, trees, grp = [], [], [], []
    for g in spec.get("groups", []):
        if g.get("fixed"):
            pl_ = [(key, X(s), h, w, 0) for key, s, h, w in spec.get("fixed", []) if g["a"] <= s <= g["b"]]
        else:
            b_, f_, pl_ = _p17_group_sec(g, X, gyx, k, wl_y, av, style, use)
            back += b_
            front += f_
        keys = sorted(set(p[0] for p in pl_), key=lambda k_: -PLA_SPECIES[k_]["h_m"])
        tags = [t for t in g.get("why", ()) if t in P17_WHY_PLACE or any(t in pla_purpose(k_) for k_ in keys)]
        trees += [p for p in pl_ if p[4] == 0]
        if keys:
            grp.append((g, keys, tags))
    fx = [(key, X(s), h, w, 0) for key, s, h, w in spec.get("fixed", []) if t0 + 0.2 <= s <= t1 - 0.2]
    for i, (key, x, h, w, _l) in enumerate(sorted(fx, key=lambda q: -q[2])):   # S4: p.14's own plants, seated
        ly_ = 1 if _pla_canopy(key) and any(ua - 2.0 * k < x < ub + 2.0 * k for ua, ub in use) else 0
        (back if ly_ else front).extend(pla_section(key, x, sf_seat_x(gyx, x, 0.12 * w * k), k, h_m=h, crown_m=w,
                                                    seed=i + 7, style=style, layer=ly_))
    trees += [p for p in fx if p not in trees]
    wl.add("vegetation", back + front)
    bad = sf_assert_g6(k, trees=[(p[0], p[1], p[2], p[3]) for p in trees], strict=False)
    if bad:
        log.append(u"WARNING (G6) p.17 {}: {}".format(name, u"; ".join(bad[:3])))
    # people doing what each zone is for (G10, G15), in front of the planting: who stays looks at the zone's focus
    # (the spec's water, or the zone's own), people in the water play in pairs, walkers keep their way
    fx0 = X(spec["focus"]) if spec.get("focus") is not None else X(min(prof, key=lambda q: q[1])[0])
    figs = []
    for j, (zone, a, b, o) in enumerate(spec.get("people", [])):
        o = o or {}
        gr = stone_y if zone == "stepping_stones" else (Y(o["z"]) if o.get("z") is not None else None)
        sh_, _pl = fig_place_zones([(zone, X(a), X(b), gr)], gyx, k, seed=31 * j + 5 + 7 * spec.get("seed", 3),
                                   layer=0, style=style, density=o.get("dens", 1.0), water=wl_y,
                                   max_per_zone=o.get("n"), focus=X(o["focus"]) if o.get("focus") is not None else fx0)
        figs += sh_
    wl.add("figures", figs)
    top = _p17_shp_bb(wl.shapes())[3] + 1.5
    # behind the cut (D9): the sky (its own variant, birds), the depth layers, people further along, basins beyond
    clipr = (0.0, 0.0, W, top)
    atm = water_layers()
    sf_atmosphere(0.0, W, gyx, top, k, seed=spec.get("seed", 3), sky="d8", trees=False, into=atm, cid=reg["id"])
    wl.add("atmosphere", _p17_clip(atm.L["atmosphere"], clipr))
    wl.add("background", _p17_clip(_p17_depth(spec, reg, X, P, gyx, zb, top, k, wl_y, style, log), clipr))
    bp = []
    for kind, a, b, fl, rim in spec.get("beyond", []):   # beyond the cut: the layer-1 tone (no alpha veil, G9)
        fn = pla_reed_basin if kind == "reed" else pla_mint_cell
        bp += fn(X(a), X(b), Y(fl), Y(rim), k, P17_BASIN["kerb_h"], P17_BASIN["kerb_t"], P17_BASIN["media"])
    if bp:
        wl.add("background", _p17_tone(bp, 0.5))
    for j, (zone, a, b) in enumerate(spec.get("back", [])):
        sh_, _pl = fig_place_zones([(zone, X(a), X(b))], gyx, k, seed=77 + j + spec.get("seed", 3), layer=1,
                                   style=style, density=0.6, water=wl_y, max_per_zone=2, focus=fx0)
        wl.add("background", sh_)
    # the zoom inset (G15): the cut's main use x2.5 (1:200 at 1:500), in the cut's own free sky
    ins = spec.get("inset")
    if ins:
        f_ = 2.5
        src = _p17_spot_box(gyx, X(max(ins[0], t0)), X(min(ins[1], t1)), k)
        dw, dh = (src[2] - src[0]) * f_, (src[3] - src[1]) * f_
        boxes = [_p17_shp_bb([s_]) for n_ in ("structures", "vegetation", "figures") for s_ in wl.L[n_]]
        boxes += [(x_ - 1.0, 0.0, x_ + 1.0, gyx(min(max(x_, 0.0), W))) for x_ in [i * 2.0 for i in range(int(W / 2.0) + 1)]]
        dst = _p17_inset_at(src, dw, dh, [b_ for b_ in boxes if b_ != (0.0, 0.0, 0.0, 0.0)], W, top)
        if dst:
            body = [s_ for n_ in WAT_LAYERS if n_ != "atmosphere" for s_ in wl.L[n_]]
            wl.add("labels", sf_zoom_inset(src, dst, k, k * f_, body, ins[2], size=fs))
            spec["inset_box"] = dst
        else:
            log.append(u"p.17 {}: no free sky for the zoom inset ({}): none drawn".format(name, ins[2]))
    pg = Page(0, 0)
    _p17_put(pg, _p17_clip(wl.shapes(), (0.0, -1e4, W, 1e4)))
    for pts, colour in spec.get("arrows", []):
        arrow(pg, P(pts), colour, 0.3, 1.6, [0.9, 0.6])
    spec["dbox"] = (0.0, 0.0, W, top)
    # on top: the cut's end names (D6) and the banks by place
    top += 2.5
    ends = cut_end_labels(name)
    try:
        sides = [place_name(u"bank_{}_short".format(s_)) for s_ in level_end_labels(reg["id"])]
    except Exception:
        sides = [u"", u""]
    pg.text(ends[0], 0.0, top, P17_HEAD, COL["ink_dark"], bold=True)
    w0 = text_w(ends[0], P17_HEAD, True)
    labs.append((0.0, top - 0.6, w0, top + P17_HEAD * CAP))
    if sides[0]:
        pg.text(sides[0], w0 + 1.5, top, fs, COL["ink"])
        labs.append(_p17_text_box(sides[0], w0 + 1.5, top, fs))
    pg.text(ends[1], W, top, P17_HEAD, COL["ink_dark"], bold=True, align="R")
    w1 = text_w(ends[1], P17_HEAD, True)
    labs.append((W - w1, top - 0.6, W, top + P17_HEAD * CAP))
    if sides[1]:
        pg.text(sides[1], W - w1 - 1.5, top, fs, COL["ink"], align="R")
        labs.append(_p17_text_box(sides[1], W - w1 - 1.5, top, fs, False, "R"))
    # under it (R07): the zones named with their reason, then the planting band of every group
    low = _p17_zone_strip(pg, spec, grp, X, W, -1.2, k, labs)
    yc = low - fs * 1.5
    pg.text(spec["caption"], 0.0, yc, fs, COL["ink_dark"], bold=True)
    labs.append(_p17_text_box(spec["caption"], 0.0, yc, fs, True))
    r28_scale_bar(pg, text_w(spec["caption"], fs, True) + 5.0, yc - 0.3, den, fs, False)
    # the levels at the right, every one from the cut registry (M8), or the design's own named level
    ent = [(Y(reg["bed"]), u_level(reg["bed"]) + u" bed", C["w4"], False),
           (Y(reg["avg_flow"]), u_level(reg["avg_flow"]) + u" average flow", C["w4"], True),
           (Y(reg["q100"]), u_level(reg["q100"]) + u" Q100", C["w4"], False),
           (Y(reg["q500"]), u_level(reg["q500"]) + u" Q500", C["w4"], False)]
    ent += [(Y(z), u_level(z) + u" " + t, COL["ink"], False) for z, t in spec.get("levels", [])]
    level_ladder(pg, ent, W + 0.8, W + 4.0, fs, lo=0.0)
    spec["labs"] = labs
    log.append(u"p.17 {}: {} planting groups, {} zones named, {} background houses, levels bed {} / avg flow {} / "
               u"Q100 {} / Q500 {} (registry), inset {}".format(
                   name, len(spec.get("groups", [])), len(spec.get("zones", [])), spec.get("n_houses", 0),
                   u_level(reg["bed"]), u_level(reg["avg_flow"]), u_level(reg["q100"]), u_level(reg["q500"]),
                   u"yes" if spec.get("inset_box") else u"no"))
    return pg


def _p17_zone_strip(pg, spec, grp, X, W, ytop, k, labs):
    """under a section, like R07 (G15): row 1 the use zones, a fine span rule with end ticks and "NAME · reason";
    row 2 every planting group, its band chip (the four P17_BAND_NAME bands by the group's wet-to-dry t; on S4 the
    sourced band letter of p.14's bands, BAND_COL, explained in the line under it) and "species + species: what it
    does", a colour swatch per species (its pla_colour). A label that cannot sit at its span becomes a number there
    (a row of its own above that tier's labels), explained in the key under the strip (G3: numbered left to right,
    row 1 first; the key in the same order). Returns the bottom y."""
    fs = P17_FS
    rh = fs * 1.45
    edges = _p17_band_t()
    ta, tb = spec["rng"]
    bands = spec.get("bands") or []
    keyl = []

    def numbers(rows, y0_):
        """the numbers of a tier's labels that did not fit, on their spans in the row y0_"""
        for pay, xm, r in rows:
            if r is None:
                n_ = len(keyl) + 1
                keyl.append((n_, pay[-1]))
                pg.text(str(n_), xm, y0_, fs, COL["ink_dark"], bold=True, align="C")
                labs.append(_p17_text_box(str(n_), xm, y0_, fs, True, "C"))
    # row 1: the zones
    z_it = []
    for z in spec.get("zones", []):
        a, b, nm = z[0], z[1], z[2]
        why = z[3] if len(z) > 3 else u""
        xa, xb = X(max(a, ta)), X(min(b, tb))
        if xb - xa < 0.5:
            continue
        tw = text_w(nm, fs, True) + (text_w(u" · " + why, fs) if why else 0.0)
        z_it.append((xa, xb, tw, (nm, why, nm + (u" · " + why if why else u""))))
    yr = ytop - 0.6
    for xa, xb, _tw, _p in z_it:                         # the span rules with their end ticks
        pg.line([(xa + 0.3, yr), (xb - 0.3, yr)], COL["ink2"], 0.12)
        for xv in (xa + 0.3, xb - 0.3):
            pg.line([(xv, yr - 0.6), (xv, yr + 0.6)], COL["ink2"], 0.12)
    rows = _p17_rows_w(z_it, W, nrows=2)
    off = 1 if any(r is None for _p, _x, r in rows) else 0
    y = yr - 1.0 - fs
    numbers(rows, y)
    nr = 0
    for (nm, why, _t), lx, r in rows:
        if r is None:
            continue
        yl = y - (r + off) * rh
        pg.text(nm, lx, yl, fs, COL["ink_dark"], bold=True)
        labs.append(_p17_text_box(nm, lx, yl, fs, True))
        if why:
            tw = text_w(nm, fs, True)
            pg.text(u" · " + why, lx + tw, yl, fs, COL["ink"])
            labs.append(_p17_text_box(u" · " + why, lx + tw, yl, fs))
        nr = max(nr, r + 1)
    y -= max(nr + off, 1) * rh + 0.6
    # row 2: the planting band of every group, its species and what it does
    g_it = []
    for g, keys, tags in grp:
        xa, xb = X(max(g["a"], ta)), X(min(g["b"], tb))
        if xb - xa < 0.3:
            continue
        if bands:                                        # S4: the sourced band letter at the group's middle
            xm_t = 0.5 * (g["a"] + g["b"])
            code = next((c_ for a_, b_, _l, c_ in bands if a_ <= xm_t <= b_), None)
            chip, bname = (BAND_COL.get(code, code), code) if code else (None, None)
        else:
            tm = 0.5 * (g["t"][0] + g["t"][1]) if g.get("t") else 0.5
            bi = sum(1 for e in edges if tm > e)
            chip, bname = P17_BAND_COL[bi], P17_BAND_NAME[bi]
        txt = _p17_co_text(keys, tags)
        lead = (bname + u": ") if bname and not bands else u""
        tw = (fs * 1.7 + 0.8 if chip else 0.0) + (text_w(lead, fs, True) if lead else 0.0) + \
            len(keys[:3]) * 2.0 + text_w(txt, fs)
        g_it.append((xa, xb, tw, (chip, bname, lead, keys, txt, lead + txt)))
    rows = _p17_rows_w(g_it, W, nrows=2)
    off = 1 if any(r is None for _p, _x, r in rows) else 0
    y0 = y - fs
    numbers(rows, y0)
    nr = 0
    for (chip, bname, lead, keys, txt, _t), lx, r in rows:
        if r is None:
            continue
        yl = y0 - (r + off) * rh
        xx = lx
        if chip:
            pg.poly([rect(xx, yl - 0.2, xx + fs * 1.7, yl + fs * 0.95)], fill=chip)
            if bands and bname:
                pg.text(bname, xx + fs * 0.85, yl + 0.1, fs, "FFFFFF", bold=True, align="C")
            xx += fs * 1.7 + 0.8
        if lead:
            pg.text(lead, xx, yl, fs, COL["ink_dark"], bold=True)
            xx += text_w(lead, fs, True)
        for k_ in keys[:3]:                              # each species its own colour (G9)
            pg.poly([rect(xx, yl, xx + 1.5, yl + 1.5)], fill=pla_colour(k_)["fill"])
            xx += 2.0
        pg.text(txt, xx, yl, fs, COL["ink"])
        labs.append((lx, yl - fs * 0.3, xx + text_w(txt, fs), yl + fs * CAP))
        nr = max(nr, r + 1)
    if g_it:
        y -= max(nr + off, 1) * rh + 0.4
    # S4: the sourced bands' key (letter, name, days a year), left to right
    if bands:
        xx, yl = 0.0, y - fs
        for a, b, lab, c_ in sorted(bands, key=lambda q: q[0]):
            tw = fs * 1.7 + 0.8 + text_w(lab, fs, True)
            if xx > 0.0 and xx + tw > W:
                xx, yl = 0.0, yl - rh
            pg.poly([rect(xx, yl - 0.2, xx + fs * 1.7, yl + fs * 0.95)], fill=BAND_COL.get(c_, c_))
            pg.text(c_, xx + fs * 0.85, yl + 0.1, fs, "FFFFFF", bold=True, align="C")
            pg.text(lab, xx + fs * 1.7 + 0.8, yl, fs, COL["ink_dark"], bold=True)
            labs.append((xx, yl - fs * 0.3, xx + tw, yl + fs * CAP))
            xx += tw + 4.0
        y = yl - fs * 0.3 - 0.6
    # the key of the numbers, in their order
    if keyl:
        xx, yl = 0.0, y - fs
        for n_, t in keyl:
            s_ = u"{} {}".format(n_, t)
            tw = text_w(s_, fs) + 4.0
            if xx > 0.0 and xx + tw > W:
                xx, yl = 0.0, yl - rh
            pg.text(s_, xx, yl, fs, COL["ink"])
            labs.append(_p17_text_box(s_, xx, yl, fs))
            xx += tw
        y = yl - fs * 0.3
    return y


def _p17_walled_bed(gz, ws, wn, width, log, cid):
    """DATA-1 (Aras 31 Oct, ask 1 a): the bed between a walled cut's DSİ walls from the survey ground gz (not flat),
    the summer strip (the low-flow channel, its zone-base width) moved onto the survey's lowest point, where the low
    water runs, cut STRIP_DEPTH under that point. Returns (profile points ws..wn, (st0, st1), strip floor, fills: the
    gravel bed following the floor, the strip's concrete liner)."""
    ts = [ws + 0.25 * i for i in range(int((wn - ws) / 0.25) + 1)]
    tlow = min(ts, key=gz)
    st0 = min(max(tlow - width / 2.0, ws + 0.3), wn - 0.3 - width)
    st1 = st0 + width
    fl = round(min(gz(st0 + (st1 - st0) * i / 8.0) for i in range(9)) - STRIP_DEPTH, 2)
    pts = [(ws, gz(ws))]
    t = math.floor(ws) + 1.0
    while t < st0 - 0.3:
        pts.append((t, gz(t)))
        t += 1.0
    pts += [(st0, gz(st0)), (st0, fl), (st1, fl), (st1, gz(st1))]
    t = math.ceil(st1 + 0.3)
    while t < wn - 0.3:
        pts.append((t, gz(t)))
        t += 1.0
    pts.append((wn, gz(wn)))
    lt = 0.15
    fills = [(pts + [(p[0], p[1] - P17_GRAVEL) for p in reversed(pts)], "gravel"),
             ([(st0 - lt, gz(st0)), (st0 - lt, fl - lt), (st1 + lt, fl - lt), (st1 + lt, gz(st1)), (st1, gz(st1)),
               (st1, fl), (st0, fl), (st0, gz(st0))], "concrete")]
    log.append(u"p.17 {}: bed between the DSİ walls from the survey profile; summer strip ({:.0f} cm) moved onto the "
               u"survey's low point at {:.1f}-{:.1f} m (DATA-1, Aras ask 1 a), floor {}".format(
                   cid, width * 100.0, st0, st1, u_level(fl)))
    return pts, (st0, st1), fl, fills


def _p17_f2(log):
    """F2 across the stream at the upstream entry (cut registry F2), scenario "step across, clean, look out": the
    walk on the SW wall top, stepping stones across the summer strip (nobody in the walled channel's water), the
    spillway, the lined reed basins, the dry bank, the shaded walk with its bike lane and bench, the rain terraces and
    the viewing terrace on the top one. Round 3 (DATA-1): the bed between the walls from the survey, the strip on its
    low point."""
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
    floor_pts, (st0, st1), sfl, bed_fills = _p17_walled_bed(gz, ws, wn, zone["STRIP"][1] - zone["STRIP"][0], log,
                                                            u"F2")
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
    prof += [(ws - wtk, wsw), (ws, wsw)] + floor_pts + [(wn, wne), (sp0, wne)]
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
    fills = bed_fills + fills
    fills += [([(ws - wtk, wsw), (ws, wsw), (ws, bed - P17_GRAVEL), (ws - wtk, bed - P17_GRAVEL)], "stone"),
              ([(wn, wne), (wn + wtk, wne), (wn + wtk, bed - P17_GRAVEL), (wn, bed - P17_GRAVEL)], "stone"),
              ([(sp0, wne), (sp0 + 0.3, wne), (sp0 + 0.3, wne - 0.45), (sp1 - 0.3, wne - 0.30), (sp1 - 0.3, wne),
                (sp1, wne), (sp1, wne - 0.5), (sp0, wne - 0.65)], "concrete")]
    water = [[(sp0 + 0.3, wne - 0.45), (sp1 - 0.3, wne - 0.30), (sp1 - 0.3, wne - 0.15), (sp0 + 0.3, wne - 0.25)]]
    wa = (ws - wtk - wk, ws - wtk)                      # the walk on the wall top
    bl = (gr0 + 2.5, gr0 + 2.5 + bk)                    # the shaded walk: bike lane, then the walk
    wl_ = (bl[1] + 2.0, bl[1] + 2.0 + wk)
    ta = treads[-1][0] if treads else te1 - P17_TERRACE_W
    vt = (ta, ta + P17_TERRACE_W)                       # the viewing terrace on the top tread, its rail to the stream
    rush = ("soft_rush", "loosestrife")
    groups = [dict(a=ws + 0.2, b=st0 - 0.3, t=(0.02, 0.06), mix=rush, dens=1.2, why=("cleaning",), seed=21),
              dict(a=st1 + 0.3, b=wn - 0.2, t=(0.06, 0.02), mix=rush, dens=1.2, why=("cleaning",), seed=22),
              dict(a=sp0 + 0.5, b=sp1 - 0.5, t=(0.04, 0.08), mix=rush, dens=0.8, why=("cleaning",), seed=23),
              dict(a=bt1 + 0.5, b=gr0 - 0.3, t=(0.55, 0.85), mix=("chaste", "tamarisk", "olive", "rosemary", "lavender"),
                   why=("perception", "corridor"), seed=24),
              dict(a=gr0 + 0.3, b=gr1 - 0.3, t=(0.48, 0.55), mix=("plane", "ash", "chaste"), why=("shade", "corridor"),
                   seed=25),
              dict(a=te0 + 0.5, b=vt[0] - 0.3, t=(0.78, 0.95), mix=("olive", "rosemary", "lavender"),
                   why=("shade", "perception"), seed=26)]
    groups = [g_ for g_ in groups if g_["b"] - g_["a"] > 0.5]
    bn = bl[1] + 0.7                                    # a bench between the bike lane and the walk
    lp_ = wl_[1] + 0.4                                  # a lamp on the walk's far edge (G15 street element)
    return dict(cid="F2", seed=2, rng=(t0, t1), prof=prof, fills=fills, water=water, cells=cells, groups=groups,
                focus=(st0 + st1) / 2.0,
                avoid=[wa, bl, wl_, vt, (bn - 0.3, bn + 0.8), (lp_ - 0.3, lp_ + 0.3)],
                structures=[("lane", wa[0], wa[1], "walk"), ("lane", bl[0], bl[1], "bike"),
                            ("lane", wl_[0], wl_[1], "walk"), ("terrace", vt[0], vt[1], "a", None),
                            ("stones", st0, st1), ("bench", bn, 1), ("lamp", lp_, -1)],
                people=[("walkway", wa[0], wa[1], None), ("stepping_stones", st0, st1, {"n": 2}),
                        ("bike_lane", bl[0], bl[1], {"n": 1}), ("walkway", wl_[0], wl_[1], None),
                        ("viewing_terrace", vt[0], vt[1], {"n": 3})],   # v10: nobody in the walled channel's water (Aras 11:28)
                back=[("walkway", wa[0], wa[1]), ("walkway", wl_[0], wl_[1])],
                arrows=[([(sp0 + 0.2, wne - 0.2), (sp0 - 0.8, wne - 1.6), (sp0 - 1.2, bed + 0.4)], C["w3"])],
                zones=[(wa[0], wa[1], _p17_lane_txt(u"PATH", wk), u"wall top, above the bed"),
                       (st0, st1, u"STONES", u"cross the summer strip dry-shod"),
                       (sp0, sp1, u"SPILLWAY", u"basin overflow back to the stream"),
                       (bt0, bt1, u"REED BASINS", u"clean run-off before the stream"),
                       (bt1, gr0, u"DRY BANK", u"shrubs hold the slope"),
                       (bl[0], bl[1], _p17_lane_txt(u"BIKE", bk), u"through route, apart from walkers"),
                       (wl_[0], wl_[1], _p17_lane_txt(u"PATH", wk), u"under the trees, out of the sun"),
                       (te0, vt[0], u"RAIN TERRACES", u"level treads hold the rain"),
                       (vt[0], vt[1], u"VIEW TERRACE", u"over the basins to the stream")],
                inset=(st0 - 1.5, st1 + 1.5, u"stepping stones over the summer strip"),
                levels=[(wne, u"DSİ wall")],
                caption=u"F2 · the upstream entry: rain terraces, reed basins and the walled stream")


def _p17_f4(log):
    """F4 across the lower reach (cut registry F4), scenario "play in the water": the path and its bridge over the
    side arm, the bank top, the viewing deck with its ramp, the widened bed with its strip (stones, wading), fishing
    and watching at the water's edge, the north bank, the street-side bike lane and walk with a lamp"""
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
    wd = (94.0, 109.5)                                  # the shallow strip people wade and play in
    # the water's edge NE of it: the first ground above the average flow, and a sitting group there facing the water
    # if 3.5 m of dry bank fit before the NE bank's trees (else none, one log line)
    wm = (wd[0] + wd[1]) / 2.0
    e = next((wm + 0.25 * i for i in range(int((121.0 - wm) / 0.25)) if gz(wm + 0.25 * i) > avg), None)
    sit = None
    if e is not None:
        sit = (max(e, wd[1]) + 0.3, max(e, wd[1]) + 3.8)
        if sit[1] > 119.0 or any(gz(sit[0] + 0.25 * i) <= avg for i in range(int((sit[1] - sit[0]) / 0.25) + 1)):
            sit = None
    if sit is None:
        log.append(u"p.17 F4: no dry bank by the shallow strip for the water's edge (none drawn)")
    else:
        groups[5]["a"] = max(groups[5]["a"], sit[1] + 0.3)
    lp_ = wl_[1] + 0.4                                  # a lamp at the street walk, a bollard where the path starts
    bo_ = pw[0] + 0.4
    sw_, ne_ = place_name("bank_SW_short").upper(), place_name("bank_NE_short").upper()
    return dict(cid="F4", seed=4, rng=(t0, t1), prof=prof, fills=fills, water=water, groups=groups,
                focus=(wd[0] + wd[1]) / 2.0,
                avoid=[pw, br, (rp[0], dk[1]), bl, wl_, (bn - 0.3, bn + 0.8), (lp_ - 0.3, lp_ + 0.3)] +
                      ([sit] if sit else []),
                structures=[("lane", pw[0], pw[1], "walk"), ("bridge", br[0], br[1], zbr),
                            ("ramp", rp[0], rp[1], zr0, zdk), ("terrace", dk[0], dk[1], "b", zdk),
                            ("lane", bl[0], bl[1], "bike"), ("lane", wl_[0], wl_[1], "walk"),
                            ("stones", st0, st1), ("bench", bn, 1), ("lamp", lp_, -1), ("bollard", bo_)],
                people=[("walkway", pw[0], pw[1], None),
                        ("bridge_crossing", br[0] + 0.5, br[1] - 0.5, {"z": zbr, "focus": (a0 + a1) / 2.0}),
                        ("viewing_terrace", dk[0], dk[1], {"z": zdk, "n": 3}),
                        ("stepping_stones", st0, st1, {"n": 2}), ("wading_strip", wd[0], wd[1], {"n": 4})] +
                       ([("water_edge", sit[0], sit[1], {"n": 3, "dens": 1.6})] if sit else []) +   # fishing, watching
                       [("bike_lane", bl[0], bl[1], {"n": 1}), ("walkway", wl_[0], wl_[1], None)],
                back=[("walkway", pw[0], pw[1]), ("walkway", wl_[0], wl_[1])],
                zones=[(pw[0], pw[1], _p17_lane_txt(u"PATH", wk), u"along the bank to the footbridge"),
                       (br[0], br[1], u"BRIDGE", u"cross the side arm dry-shod"),
                       (br[1], rp[0], u"BANK TOP", u"a bench in the trees' shade"),
                       (rp[0], dk[1], u"VIEW TERRACE", u"up a ramp, a step-free view"),
                       (dk[1], b0, sw_, u"willows hold the flood bank"),
                       (st0, st1, u"STONES", u"cross the summer strip dry-shod"),
                       (wd[0], wd[1], u"WADING", u"wade, play, cool your feet")] +
                      ([(sit[0], sit[1], u"WATER'S EDGE", u"fish, watch the play")] if sit else []) +
                      [(b1, bl[0], ne_, u"trees between the water and the street"),
                       (bl[0], bl[1], _p17_lane_txt(u"BIKE", bk), u"street side, apart from walkers"),
                       (wl_[0], wl_[1], _p17_lane_txt(u"PATH", wk), u"behind the trees, off the traffic")],
                inset=(wd[0] + 3.0, wd[0] + 11.0, u"wading in the shallow strip"),
                caption=u"F4 · the lower reach: the side arm, the bank top and the widened stream")


def _p17_w1_ground(log):
    """DATA-1: W1's surveyed ground [(m from the SW end, m a.s.l.)] from the board's CUTS row "up" (the surveyed
    section ARAS = the W1 cut, research levels2_out.json: heights over the bed every 1 m from u0 = the SW end), checked
    against the level module (bed, length); None (FLAG line) when missing or not matching"""
    row = next((c_ for c_ in CUTS if c_.get("key") == "up"), None)
    bed = level("W1", "bed")
    ln = level("W1", "length_m")
    if not row or not row.get("ground"):
        log.append(u"FLAG p.17 W1: no surveyed profile (data/CUTS.py \"up\"): the bed is drawn flat at {}".format(
            u_level(bed)))
        return None
    if abs(float(row.get("bed") or 0.0) - bed) > 0.005 or (ln and abs(len(row["ground"]) - 1 - ln) > 1.0):
        log.append(u"FLAG p.17 W1: CUTS \"up\" (bed {}, {} m) does not match the level module (bed {}, {} m): the bed "
                   u"is drawn flat".format(row.get("bed"), len(row["ground"]) - 1, u_level(bed), ln))
        return None
    log.append(u"p.17 W1: ground from the surveyed section (data/CUTS.py \"up\", bed {}, every 1 m)".format(
        u_level(bed)))
    return [(float(i), round(bed + float(v), 2)) for i, v in enumerate(row["ground"])]


def _p17_f1(log):
    """W1 at the inflow (cut registry W1, = F1), scenario "a shaded street-side route, a look over the wall": the
    bike lane and the walk under the planes on the south bank with a lamp, the walled bed from the survey (DATA-1;
    nobody in its water, no blocks in it), the summer strip on its low point, the viewing terrace on the north wall
    top, the reed basins beyond"""
    r = _p17_reg("W1")
    bed = r["bed"]
    wsw, wne = _p17_wall(r)
    t0, t1 = P17_F1_RNG
    ws, wn = P17_F1_BED
    wtk = P17_WALL_T
    wk, bk = P14_PROM_W
    g = _p17_w1_ground(log)
    sw0, sw1 = P17_F1_STRIP
    if g:
        floor_pts, (st0, st1), sfl, fills = _p17_walled_bed(lambda t: _p17_interp(g, t), ws, wn, sw1 - sw0, log,
                                                            u"W1")
    else:                                               # the flat bed (FLAG logged), the zone base's strip
        st0, st1 = sw0, sw1
        floor_pts = [(ws, bed), (st0, bed), (st0, bed - STRIP_DEPTH), (st1, bed - STRIP_DEPTH), (st1, bed), (wn, bed)]
        fills = [([(st0 - 0.15, bed), (st0 - 0.15, bed - STRIP_DEPTH - 0.15), (st1 + 0.15, bed - STRIP_DEPTH - 0.15),
                   (st1 + 0.15, bed), (st1, bed), (st1, bed - STRIP_DEPTH), (st0, bed - STRIP_DEPTH), (st0, bed)],
                  "concrete")]
    prof = [(t0, wsw), (ws - wtk, wsw), (ws, wsw)] + floor_pts + [(wn, wne), (wn + wtk, wne), (t1, wne)]
    fills += [([(ws - wtk, wsw), (ws, wsw), (ws, bed - P17_GRAVEL), (ws - wtk, bed - P17_GRAVEL)], "stone"),
              ([(wn, wne), (wn + wtk, wne), (wn + wtk, bed - P17_GRAVEL), (wn, bed - P17_GRAVEL)], "stone")]
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
    lp_ = wl_[1] + 0.3                                  # a lamp at the path's water side
    return dict(cid="W1", seed=1, rng=(t0, t1), prof=prof, fills=fills, groups=groups, beyond=beyond,
                focus=(st0 + st1) / 2.0,
                avoid=[bl, wl_, (bn - 0.3, bn + 0.8), (lp_ - 0.3, lp_ + 0.3)],
                structures=[("lane", bl[0], bl[1], "bike"), ("lane", wl_[0], wl_[1], "walk"),
                            ("terrace", vt[0], vt[1], "a", None), ("bench", bn, 1), ("lamp", lp_, 1)],
                people=[("bike_lane", bl[0], bl[1], {"n": 1}), ("walkway", wl_[0], wl_[1], None),
                        ("viewing_terrace", vt[0], vt[1], {"n": 2})],
                back=[("walkway", wl_[0], wl_[1])],
                arrows=[([((ws + wn) / 2.0 + 6.0, bed + 0.5), (wn - 1.0, wne - 0.6), (bx0 + 1.0, wne + 0.9)], C["w3"])],
                zones=[(bl[0], bl[1], _p17_lane_txt(u"BIKE", bk), u"through route under the trees"),
                       (wl_[0], wl_[1], _p17_lane_txt(u"PATH", wk), u"shaded by the south bank's trees"),
                       (st0, st1, u"SUMMER STRIP", u"the low flow, on the bed's lowest line"),
                       (vt[0], vt[1], u"VIEW TERRACE", u"on the wall top, over the bed"),
                       (bx0, t1, u"REED BASINS beyond", u"stream water cleaned there")],
                inset=(vt[0] - 1.0, vt[1] + 1.5, u"the viewing terrace on the wall top"),
                levels=[(wne, u"DSİ wall")],
                caption=u"W1 · the walled stream at the inflow, the reed basins beyond")


P17_S4_WHY = {"sw_path": ("shade", "noise"), "sw_slope": ("corridor", "shade"), "bed_sw": ("cleaning",),
              "open": ("cleaning",), "toe": ("cleaning", "corridor"),
              "terr_b": ("corridor", "perception"), "terr_c": ("shade", "corridor"), "prom": ("shade",),
              "fill": ("shade", "noise")}   # what each of p.14's planting zones does on S4 (G9)


def _p17_f3(log):
    """S4 (cut registry S4, = F3), scenario "sit in the sun between the bands": p.14's own cut and planting
    (_p14_geo, _p14_planting; round 3: on the survey datum, the bed from the surveyed profile, N1 a), so the cut is
    the same everywhere: the path, the planting bands of the widened stream by the days water covers the ground
    (PLANT_BANDS, RWS), the stones over the strip, the lower walk, the sun steps, the promenade with its lamp and the
    bike lane. Fills follow the survey: the gravel bed offset under the profile, the strip liner from G["strip_lip"]
    (p14_geo_interface.md)."""
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
    la, lb = G.get("strip_lip") or (bed, bed)           # the survey ground at the strip's two edges
    b0, b1 = G.get("b0", st0), G.get("b1", st1)
    bedp = [(b0, _p14_surf(b0))] + [p for p in G["prof"] if b0 < p[0] < b1] + [(b1, _p14_surf(b1))]
    fills = [(bedp + [(p[0], p[1] - P17_GRAVEL) for p in reversed(bedp)], "gravel"),   # the bed, under the survey
             ([(tt0, shelf), (tt1, shelf), (tt1, shelf - 0.3), (tt0, shelf - 0.3)], "gravel"),
             ([(st0 - lt, la), (st0 - lt, sfl - lt), (st1 + lt, sfl - lt), (st1 + lt, lb), (st1, lb), (st1, sfl),
               (st0, sfl), (st0, la)], "concrete"),
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
                focus=(st0 + st1) / 2.0,
                structures=[("stones", st0, st1), ("lamp", p0 + 0.6, -1), ("lamp", sw[1] - 0.3, 1)],
                people=[("walkway", max(t0 + 0.5, sw[0]), sw[1], {"n": 2}), ("stepping_stones", st0, st1, {"n": 2}),
                        ("walkway", w0, w1, {"n": 2}), ("sun_steps", e0, p0, {"n": 3}), ("walkway", p0, p1, None),
                        ("bike_lane", p1, p2, {"n": 1})],
                back=[("walkway", p0, p1)],
                zones=[(max(t0, sw[0]), sw[1], u"PATH", u"the south bank walk under the trees"),
                       (st0, st1, u"STONES", u"cross the summer strip dry-shod"),
                       (w0, w1, u"LOWER WALK", u"along the water, between the bands"),
                       (e0, p0, u"SUN STEPS", u"sit in the sun, facing the water"),
                       (p0, p1, _p17_lane_txt(u"PROMENADE", wk), u"top-of-bank walk, shade trees"),
                       (p1, p2, _p17_lane_txt(u"BIKE", bk), u"on the bank top, apart from walkers")],
                inset=(e0 - 0.5, min(p0, e0 + 6.0), u"the sun steps"),
                bands=bands, levels=[(P14_PROM, u"promenade")],
                caption=u"S4 · the planting bands of the widened stream " + cite(P15_BAND_SRC))


# ---------------------------------------------------------------- page B: the keys, the page
def _p17_materials(pg, x, ytop, w):
    """what the sections draw (G1): the cut materials and the water lines, two columns; returns the bottom y"""
    fs = P17_FS
    pa = _wat_pal()
    rows = [("earth", u"ground"), ("stone", u"stone wall"), ("gravel", u"gravel bed"), ("concrete", u"concrete"),
            ("avg", u"average flow"), ("q100", u"Q100 level"), ("q500", u"Q500 level")]
    half = (len(rows) + 1) // 2
    cw = w / 2.0
    low = ytop
    for i, (kind, lab) in enumerate(rows):
        xx = x + (i // half) * cw
        y = ytop - (i % half) * fs * 1.45 - fs
        sm = [(xx, y - 0.4), (xx + 4.0, y - 0.4), (xx + 4.0, y + fs * 0.8), (xx, y + fs * 0.8)]
        if kind == "earth":                              # G15: the soil gradient under the hatch, as the cuts
            _p17_put(pg, sct_ground([sm[3], sm[2]], sm[0][1], 2.0, "earth", 0.15))
        elif kind in ("stone", "gravel", "concrete"):
            _p17_put(pg, sct_hatch_fill(sm, kind, 2.0, SCT["cut"], 0.15))
        elif kind == "avg":
            _p17_put(pg, [("poly", sm, pa["sec"], None, 0.1), ("line", [sm[3], sm[2]], SEC["hatch"], 0.3)])
        else:
            pg.line([(xx, y + fs * 0.3), (xx + 4.0, y + fs * 0.3)], pa[kind], 0.25,
                    dash=[1.2, 0.6] if kind == "q100" else [0.4, 0.5])
        pg.text(lab, xx + 5.0, y, fs, COL["ink"])
        low = min(low, y - fs * 0.4)
    return low


def _p17_place(pg, part, x, ytop):
    """a section Page put with its top-left at (x, ytop), at 1:1 (its scale is its own), cutouts included; (its box,
    the move (dx, dy))"""
    b = _p17_bb(part.items)
    dx, dy = x - b[0], ytop - b[3]
    pg.items += _p17_move(part.items, dx, dy)
    return (x, ytop - (b[3] - b[1]), x + b[2] - b[0], ytop), (dx, dy)


def _p17_band_key(pg, x, ytop, w):
    """the four planting bands, wet to dry (G1: the chips under the sections): chip, name and the species of the
    catalogue that belong there, each with its colour swatch; returns the bottom y"""
    fs = P17_FS
    rh = fs * 1.45
    t = u"THE PLANTING BANDS · wet to dry"
    pg.text(t, x, ytop - fs, fs, COL["ink_dark"], bold=True)
    _P17_LABS.append(_p17_text_box(t, x, ytop - fs, fs, True))
    y = ytop - fs - rh
    for i, keys in enumerate(P17_BANDS):
        pg.poly([rect(x, y - 0.2, x + fs * 1.7, y + fs * 0.95)], fill=P17_BAND_COL[i])
        xx = x + fs * 1.7 + 0.8
        nm = P17_BAND_NAME[i] + u":"
        pg.text(nm, xx, y, fs, COL["ink_dark"], bold=True)
        _P17_LABS.append(_p17_text_box(nm, xx, y, fs, True))
        xx += text_w(nm, fs, True) + 1.2
        for k_ in [q for q in keys if q in P17_CAT]:
            s_ = P17_SHORT.get(k_, PLA_SPECIES[k_]["name"].lower())
            tw = 2.0 + text_w(s_, fs) + 1.6
            if xx + tw > x + w:
                xx, y = x + fs * 1.7 + 0.8, y - rh
            pg.poly([rect(xx, y, xx + 1.5, y + 1.5)], fill=pla_colour(k_)["fill"])
            pg.text(s_, xx + 2.0, y, fs, COL["ink"])
            _P17_LABS.append(_p17_text_box(s_, xx + 2.0, y, fs))
            xx += tw
        y -= rh
    return y + rh - fs * 0.4


def _p17b_draw(pg, box, specs, style, log):
    """page B in box (booklet p17, D5: each cut shows the water, the planting band each species needs and what
    surrounds it): row 1 F2 with the key map (all four cuts) and the line / material key at its right; row 2 F4 with
    the planting bands' key; row 3 W1 and S4 side by side. Every section at 1:500 (the booklet's one scale for its
    orthographic drawings), full extent, its own scale bar. Hard fit (P17.1, G2): every part is drawn on its own Page
    and measured first; the rows share the height left over (no dead band) and nothing leaves the box (a FLAG when the
    parts are bigger than it). Returns the bbox of what it drew."""
    x0, y0, x1, y1 = box
    n0 = len(pg.items)
    G = 5.0
    parts = {}
    for nm in ("F2", "F4", "W1", "S4"):
        if nm in specs:
            try:
                parts[nm] = _p17_section(specs[nm], style, log, P17_SEC_DEN)
            except Exception as ex:
                log.append(u"WARNING p.17 section {} ({}) not drawn: {}: {}".format(nm, style, type(ex).__name__, ex))
                import traceback as _tb
                log.append(_tb.format_exc()[-600:])
    bbs = dict((nm, _p17_bb(p_.items)) for nm, p_ in parts.items())
    wd = dict((nm, b[2] - b[0]) for nm, b in bbs.items())
    ht = dict((nm, b[3] - b[1]) for nm, b in bbs.items())
    # the side columns, measured on scratch pages
    cw1 = x1 - x0 - wd.get("F2", 0.0) - G
    cw2 = x1 - x0 - wd.get("F4", 0.0) - G
    sp_ = Page(0, 0)
    n_lab = len(_P17_LABS)
    kb_ = _p17_key(sp_, 0.0, 0.0, max(cw1, 30.0), 26.0, P17_CUTS, None, log)
    hk1 = -(_p17_materials(sp_, 0.0, (kb_[1] if kb_ else 0.0) - 4.0, max(cw1, 30.0)))
    hk2 = -_p17_band_key(Page(0, 0), 0.0, 0.0, max(cw2, 40.0))
    del _P17_LABS[n_lab:]
    rows = [max(ht.get("F2", 0.0), hk1), max(ht.get("F4", 0.0), hk2), max(ht.get("W1", 0.0), ht.get("S4", 0.0))]
    need = sum(rows) + 2 * G
    spare = (y1 - y0) - need
    if spare < -0.5:
        log.append(u"FLAG p.17 page B: the four cuts need {:.0f} mm, {:.0f} mm more than the box".format(need, -spare))
    gap = G + max(0.0, spare) / 2.0                    # the rows share the room left: no dead band at the foot
    if wd.get("W1", 0.0) + wd.get("S4", 0.0) + G > x1 - x0 + 0.5 or min(cw1, cw2) < 30.0:
        log.append(u"FLAG p.17 page B: a row is wider than the box ({:.0f} mm)".format(x1 - x0))
    labs, dboxes = [], []

    def put(nm, x, ytop):
        b, (dx, dy) = _p17_place(pg, parts[nm], x, ytop)
        sp = specs[nm]
        labs.extend((q[0] + dx, q[1] + dy, q[2] + dx, q[3] + dy) for q in sp.get("labs", []))
        d_ = sp.get("dbox")
        if d_:
            dboxes.append((d_[0] + dx, d_[1] + dy, d_[2] + dx, d_[3] + dy))
        return b
    y = y1
    # row 1: F2 | key map, the lines and materials
    xr = x0
    if "F2" in parts:
        xr = put("F2", x0, y)[2] + G
    kb = _p17_key(pg, xr, y, x1 - xr, 26.0, P17_CUTS, None, log)
    _p17_materials(pg, xr, (kb[1] if kb else y) - 4.0, x1 - xr)
    y -= rows[0] + gap
    # row 2: F4 | the planting bands
    xr = x0
    if "F4" in parts:
        xr = put("F4", x0, y)[2] + G
    _p17_band_key(pg, xr, y, x1 - xr)
    y -= rows[1] + gap
    # row 3: W1 and S4 side by side, the room between them shared
    w1, w3 = wd.get("W1", 0.0), wd.get("S4", 0.0)
    if "W1" in parts:
        put("W1", x0, y)
    if "S4" in parts:
        put("S4", x1 - w3 if w1 else x0, y)
    _P17_LABS.extend(labs)
    _P17_MEMO["p17_dboxes"] = dboxes
    log.append(u"p.17 page B ({}): rows {} mm, {:.0f} mm spare shared between them; sections at 1:{:,.0f}".format(
        style, u" / ".join(u"{:.0f}".format(r_) for r_ in rows), max(0.0, spare), P17_SEC_DEN))
    return _p17_bb(pg.items[n0:])


def p17b_page(pg, box, opt, log):
    """page B (wb_plants_b, booklet p17): the four cuts at 1:500 from the cut registry, in style a only (D1 a, Aras
    31 Oct: one style), drawn in box; crops wb_plants_b and its style a alias wb_plants_b_a (the same drawing). The
    meaningless triangles are off (G14 / U22); the G14 grounding line goes to the log once. Returns [(crop id, bbox,
    den)]."""
    if _P17_MEMO.get("run") != id(pg):                  # a new run reads its data afresh
        _P17_MEMO.clear()
        _P17_MEMO["run"] = id(pg)
    del _P17_LABS[:]
    tri = sf_triangles(walls=False, aggregate=False)
    specs = _p17_specs(log)
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
    log.append(u"p.17 S4 levels: datum survey (N1 a): bed {}, average flow {}, Q100 {}, Q500 {} (level module)".format(
        u_level(level("S4", "bed")), u_level(level_avg_flow("S4")), u_level(level("S4", "q100")),
        u_level(level("S4", "q500"))))
    lp_overlap_flag("p17", _P17_LABS, _P17_MEMO.get("p17_dboxes", []), bb_a)
    log.append(u"p.17 page B: sections {} at 1:{:,.0f}, style a".format(u", ".join(level_name(c_) for c_ in specs),
                                                                        P17_SEC_DEN))
    return out
