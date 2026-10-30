# p.14-15 the S4 pair (v5, revision 29 Oct 2026, T3b WO-T3b-4, package D; split from code.py and
# parts/r28_occupancy.py on 29 Oct 2026, rebuilt). ONE S4 for both pages: the existing levels from the level module
# (D4 b: bed +42.48; bed width, bank tops, the two level shelves, Q100, Q500) with our proposal on them; planting by the
# rule (D6: purple loosestrife + soft rush, no iris; D2: no reed in the open bed), each plant from plants.py in that
# month's state; the p.20 planting bands with their days under water folded into p.15 (D9 a).
#   p.14 (p14_page): four rows, a season each: rain and water as a small graphic, the cut at 1:500 with its plants in
#        the season's state, a line a month of plant states under it, the type of space it becomes named on it, one
#        rectangular view from the same viewpoint in every season, the animals on record that season.
#   p.15 (p15_page): the north-east bank at 1:250 with widths, levels and planting bands (days under water), and the
#        year on one month axis (R31: a row of pictograms per user group, bars on one time axis; plants in leaf and
#        flower).
# Revision 30 Oct 2026 (T6, booklet p13 + p14): planting from plants.py's mixed scatter by zone (G9), true-size
# people and stalls from figures.py by the season's programme (G10, P14_USE), trees beyond the cut (R16), p.15's water
# at the registry's average flow (M5), numbered zone reasons (R19), the year read through figures a month (R03, R05);
# every panel drawn twice (D1): style b (vector) in its cell, style a (cutouts) in a copy right of the board.
# build_board calls P14_TITLE, P15_TITLE, p14_page(pg, box, opt, log), p15_page(pg, box, opt, log).

P14_TITLE = u"S4 THROUGH THE SEASONS · the water level decides what the place becomes"
P15_TITLE = u"S4 NORTH-EAST BANK · the terraces stay, their use follows the months"

# ---------------------------------------------------------------- the cut: levels from the level module, our proposal
# m across S4 from the bed's low point (north-east +, as the level table's shelves), levels m a.s.l. The bed starts where
# the north-east shelf starts and is the table's width wide; where the table gives no bank angle a loose earth bank is
# drawn at P14_EARTH_RUN. The proposal: a lined summer strip in the bed, the north-east shelf as a gravel flood terrace
# with a floodable lower walk, seat steps up to a raised promenade over Q500, its earth fill down to today's bank top.
P14_EARTH_RUN = 2.0                  # loose earth bank, m run per m rise (drawing rule)
P14_STRIP = (-3.5, 0.5)              # the summer strip (400 cm wide, STRIP_DEPTH deep) beside the north-east bank
P14_LINER = 0.15                     # its concrete liner, m
P14_PROM_OVER = 1.41                 # the raised promenade over the registry's Q500, m (design: +47.60 on Q500 +46.19)
_P14_Q500 = level("S4", "q500")
P14_PROM = round(_P14_Q500 + P14_PROM_OVER, 2) if _P14_Q500 is not None else None   # the promenade, m a.s.l.
P14_STEPS = (8, 0.80)                # seat steps from the flood terrace up to the promenade: number, tread m
P14_PROM_W = (7.0, 3.0)              # promenade and bike lane, m
P14_FILL_RUN = 3.0                   # the promenade's earth fill down to today's bank top, m run per m rise
P14_WALK = (21.0, 24.0)              # the floodable lower walk on the flood terrace, m across
P14_SLAB = 0.25                      # paving and step slabs, m
P14_GRAVEL = 0.50                    # gravel under the bed, m
P14_POCHE = 1.00                     # cut ground drawn under the strip floor, m
P14_RANGE = (-46.0, 52.0)            # p.14: the whole cut, street to street
P15_RANGE = (-5.0, 52.0)             # p.15: the north-east bank from the strip
P14_DEN, P15_DEN = 500.0, 250.0      # standard scales of the two cuts
P14_SHEET_M = 0.10                   # a mean depth over this covers the gravel bed as one sheet of water; under it the
#                                      bed lies open and only the lined strip holds water (DEPTH, flat reach)
P14_SEA_MONTH = {"winter": 1, "spring": 4, "summer": 7, "autumn": 10}   # the month each cut and view shows (1-12)
P14_TREE_MAX = 15.0                  # m: no tree drawn taller (drawing rule: young trees, inside every species' sourced
#                                      range; p.14's rows hold 15 m over the promenade at 1:500)
P14_PLANT_ZONES = [  # where S4 is planted (D6, D2; G9: mixed species interpenetrating wet to dry, plants.py's niches;
    # G10: paths, the market ground, the steps and the wading strip stay open): (zone of _p14_geo, band t at its start,
    # at its end (0 = the water's edge ... 1 = dry upper ground), species, density, seed)
    ("sw_path", 0.58, 0.62, ("plane", "ash"), 0.8, 11),
    ("sw_slope", 0.50, 0.04, ("ash", "tamarisk", "willow", "chaste", "loosestrife", "soft_rush"), 1.2, 12),
    ("bed_sw", 0.02, 0.06, ("soft_rush", "loosestrife"), 1.4, 13),
    ("toe", 0.06, 0.26, ("willow", "tamarisk", "loosestrife", "soft_rush"), 1.3, 15),
    ("terr_a", 0.28, 0.34, ("willow", "tamarisk", "chaste", "loosestrife"), 1.2, 16),
    ("terr_b", 0.36, 0.38, ("tamarisk", "chaste"), 1.2, 17),
    ("terr_c", 0.38, 0.46, ("tamarisk", "chaste", "ash"), 1.2, 18),
    ("prom", 0.52, 0.52, ("plane",), 0.8, 19),
    ("fill", 0.60, 0.70, ("ash", "plane", "tamarisk", "chaste"), 1.1, 20),
]
P14_PLANTS = []                      # (species, m across, height m, crown m), filled once a run by _p14_planting (p.17
#                                      reads it for F3 after _p14_geo())
P14_SPACES = {  # what the place becomes that season, named on the cut: (zone of _p14_geo, name)
    "winter": [("bed", u"FLOOD CHANNEL"), ("terrace", u"FLOOD TERRACE")],
    "spring": [("bed", u"SHALLOW STREAM"), ("terrace", u"WET MEADOW")],
    "summer": [("strip", u"WADING STRIP"), ("market", u"MARKET GROUND"), ("prom", u"SHADED TERRACE")],
    "autumn": [("gravel", u"OPEN GRAVEL BED"), ("steps", u"SUN STEPS")],
}
P14_SPACE_COL = {"bed": "1B535E", "strip": "1B535E", "gravel": "6B5B2E", "terrace": "6B5B2E", "market": "5E4B8B",
                 "steps": "6B5B2E", "prom": "2D564E"}
P14_USE = {  # who is where, doing what, each season (G10; our programme, as the rows of P15_USE): (zone of _p14_geo,
    # FIG_ACTIVITY zone type, density, seed); figures.py places the people (poses that fit the zone, irregular gaps)
    "winter": [("sw_path", "walkway", 0.4, 1), ("prom", "walkway", 0.9, 2), ("bike", "bike_lane", 0.5, 3),
               ("walk", "walkway", 0.3, 4)],
    "spring": [("sw_path", "walkway", 0.6, 5), ("open", "bed", 0.5, 6), ("walk", "walkway", 0.8, 7),
               ("steps", "sun_steps", 0.6, 8), ("prom", "walkway", 0.7, 9), ("bike", "bike_lane", 0.6, 10)],
    "summer": [("sw_path", "walkway", 0.8, 11), ("strip", "wading_strip", 1.4, 12), ("open", "walkway", 0.7, 13),
               ("market", "market_ground", 1.2, 14), ("walk", "walkway", 1.0, 15), ("steps", "sun_steps", 1.0, 16),
               ("prom", "walkway", 1.0, 17), ("bike", "bike_lane", 1.0, 18)],
    "autumn": [("sw_path", "walkway", 0.6, 19), ("open", "walkway", 1.0, 20), ("strip", "wading_strip", 0.4, 21),
               ("steps", "sun_steps", 1.6, 22), ("prom", "walkway", 0.8, 23), ("bike", "bike_lane", 0.7, 24)],
}
P14_STALL_CANOPY = "CDBFDB"          # the Kermes stalls' canopy: the Kermes visitors' purple, light
_P14_GEO = []
_P14_PEOPLE = {}


def _p14_lv(key, side=None):
    v = level("S4", key, side)
    if v is None:
        raise RuntimeError(u"S4: '{}' {} is missing in the level module (common/data/LEVELS.py)".format(key, side or u""))
    return v


def _p14_terrace(side):
    """(from m, to m, level) of S4's level shelf on side, from the level module"""
    for t in level_cut("S4").get("terraces") or []:
        if t.get("side") == side:
            lv = t.get("level")
            return float(t["from_m"]), float(t["to_m"]), round(float(lv["value"] if isinstance(lv, dict) else lv), 2)
    raise RuntimeError(u"S4: no {} shelf in the level module".format(side))


def _p14_geo():
    """The S4 cut, once a run: the levels (bed, q100, q500, ne_top, sw_top, shelf, sfl = strip floor, base), the profile
    "prof" [(s, z)] street to street, its segments "segs" [((s, z), (s, z), surface)], today's north-east bank "today",
    the zones {name: (s0, s1)}, the step rise."""
    if _P14_GEO:
        return _P14_GEO[0]
    if P14_PROM is None:
        raise RuntimeError(u"S4: 'q500' is missing in the level module (common/data/LEVELS.py): no promenade level")
    bed, q100, q500 = _p14_lv("bed"), _p14_lv("q100"), _p14_lv("q500")
    width = _p14_lv("bed_width_cm") / 100.0
    ne_top, sw_top = _p14_lv("top", "NE"), _p14_lv("top", "SW")
    ne0, ne1, shelf = _p14_terrace("NE")
    sw0, sw1, sw_z = _p14_terrace("SW")
    b1 = ne0
    b0 = b1 - width
    st0, st1 = P14_STRIP
    sfl = bed - STRIP_DEPTH
    t0 = b1 + (shelf - bed) * P14_EARTH_RUN
    n, tread = P14_STEPS
    rise = (P14_PROM - shelf) / n
    p0 = ne1 + (n - 1) * tread
    p1 = p0 + P14_PROM_W[0]
    p2 = p1 + P14_PROM_W[1]
    p3 = p2 + (P14_PROM - ne_top) * P14_FILL_RUN
    pts, segs = [], []

    def add(s, z, tag=None):
        if pts and tag:
            segs.append((pts[-1], (s, z), tag))
        pts.append((s, z))
    add(P14_RANGE[0], sw_z)
    add(-sw1, sw_z, "road")
    add(-sw0 - 0.6, sw_z, "path")
    add(-sw0, sw_top, "crest")
    add(b0, bed, "slope_sw")
    add(st0, bed, "gravel")
    add(st0, sfl, "strip_side")
    add(st1, sfl, "strip")
    add(st1, bed, "strip_side")
    add(b1, bed, "gravel")
    add(t0, shelf, "slope_ne")
    add(P14_WALK[0], shelf, "terrace")
    add(P14_WALK[1], shelf, "walk")
    add(ne1, shelf, "terrace")
    for j in range(n):
        add(ne1 + j * tread, shelf + (j + 1) * rise, "riser")
        if j < n - 1:
            add(ne1 + (j + 1) * tread, shelf + (j + 1) * rise, "tread")
    add(p1, P14_PROM, "prom")
    add(p2, P14_PROM, "bike")
    add(p3, ne_top, "fill")
    add(P14_RANGE[1], ne_top, "street")
    ss = [p[0] for p in pts]
    if any(b < a - 1e-9 for a, b in zip(ss[:-1], ss[1:])):
        raise RuntimeError(u"S4: the levels give a cut that runs backwards ({}); check P14_* against levels.py".format(
            u", ".join(u"{:.2f}".format(s) for s in ss)))
    G = dict(bed=bed, q100=q100, q500=q500, ne_top=ne_top, sw_top=sw_top, shelf=shelf, sfl=sfl, rise=rise,
             width=width, base=sfl - P14_POCHE, prof=pts, segs=segs, b0=b0, b1=b1,
             dmax=max(_p14_depth(m) for m in range(12)),
             today=[(ne1, shelf), (ne1 + (ne_top - shelf) * P14_EARTH_RUN, ne_top), (P14_RANGE[1], ne_top)],
             zones=dict(bed=(b0, b1), gravel=(b0, st0), strip=(st0, st1), toe=(b1, t0), terrace=(t0, ne1),
                        market=(t0 + 2.0, P14_WALK[0] - 1.0), walk=P14_WALK, steps=(ne1, p0), prom=(p0, p1),
                        bike=(p1, p2), fill=(p2, p3), sw_slope=(-sw0, b0), sw_path=(-sw1, -sw0),
                        bed_sw=(b0, b0 + 2.5), open=(b0 + 3.0, st0 - 0.5), terr_a=(t0, t0 + 2.0),
                        terr_b=(P14_WALK[0] - 1.0, P14_WALK[0]), terr_c=(P14_WALK[1], ne1)))
    _P14_GEO.append(G)
    _p14_planting()
    return G


def _p14_planting():
    """S4's planting, once a run, in m across the cut: P14_PLANT_ZONES through plants.py's mixed scatter (G9; k 1, so
    positions and sizes come out in m), trees no taller than P14_TREE_MAX (crown scaled with them). Fills P14_PLANTS."""
    if P14_PLANTS:
        return P14_PLANTS
    zn = _p14_geo()["zones"]
    out = []
    for zone, ta, tb, mix, dens, seed in P14_PLANT_ZONES:
        a, b = zn[zone]
        if b - a < 0.5:
            continue
        _sh, placed = pla_scatter_section(a, b, 0.0, 1.0, t0=ta, t1=tb, mix=list(mix), seed=seed, density=dens,
                                          hires=False, detail=False)
        for key, s, h, w in placed:
            if h > P14_TREE_MAX:
                w, h = w * P14_TREE_MAX / h, P14_TREE_MAX
            out.append((key, round(s, 2), round(h, 2), round(w, 2)))
    out.sort(key=lambda p: p[1])
    P14_PLANTS[:] = out
    return P14_PLANTS


def _p14_size(key):
    """(height, crown) m a species is drawn at on its own (keys, the year): plants.py's drawing size, trees capped"""
    sp = PLA_SPECIES[key]
    h, w = sp["h_m"], sp["crown_m"]
    if h > P14_TREE_MAX:
        w, h = w * P14_TREE_MAX / h, P14_TREE_MAX
    return h, w


def _p14_people(sea):
    """the season's people in m across S4, once a run: [(pose, m across, facing, seed)] from P14_USE through
    figures.py's fig_activity (k 1: positions in m); pose "market" = a stall with its vendor and buyer, "group" = three
    people together"""
    if sea in _P14_PEOPLE:
        return _P14_PEOPLE[sea]
    zn = _p14_geo()["zones"]
    out = []
    for zone, kind, dens, seed in P14_USE.get(sea, []):
        a, b = zn[zone]
        _sh, placed = fig_activity(kind, a, b, 0.0, 1.0, seed=seed, density=dens)
        for i, (pose, s) in enumerate(placed):
            out.append((pose, s, 1 if (seed + i) % 2 else -1, seed * 10 + i))
    _P14_PEOPLE[sea] = out
    return out


def _p14_person(pose, x, gy, k, facing, seed, style="b", layer=0, wl=None, ink=None):
    """one entry of _p14_people at page x on the ground gy (page y), k mm per m as printed (a view passes its
    perspective k), layer = the D9 fade only; wl = the water level (page y) where the ground is under water: a
    standing pose there wades. Returns house shapes."""
    K = k / fig_depth(layer)[0]
    if pose == "market":
        return fig_stall(x, gy, K, facing=facing, layer=layer, seed=seed, ink=ink, canopy=P14_STALL_CANOPY,
                         style=style)
    wet = wl is not None and wl > gy + 0.02 * k
    if pose == "group" and not wet:
        return fig_group(x, gy, K, n=3, seed=seed, layer=layer, ink=ink, style=style)
    q = {}
    if wet:
        pose = "wade" if pose in ("walk", "stand", "watch", "adult_child", "group", "wade") else pose
        if pose == "wade":
            q["depth_m"] = max(0.05, min(0.60, (wl - gy) / k))
    return fig_side(pose, x, gy, K, facing=facing, ink=ink, layer=layer, style=style, pick=seed, **q)


def _p14_surf(s):
    """the ground of the cut at s (at a riser the upper one)"""
    pts = _p14_geo()["prof"]
    best = None
    for (a, za), (b, zb) in zip(pts[:-1], pts[1:]):
        if b > a and a - 1e-9 <= s <= b + 1e-9:
            z = za + (zb - za) * (s - a) / (b - a)
            best = z if best is None else max(best, z)
    if best is None:
        return pts[0][1] if s < pts[0][0] else pts[-1][1]
    return best


def _p14_wet(z, s0, s1, step=0.05):
    """the stretches from s0 to s1 whose ground lies under the level z: [(a, b)]"""
    out, a, s = [], None, s0
    n = int((s1 - s0) / step) + 1
    for i in range(n + 1):
        s = min(s1, s0 + i * step)
        if _p14_surf(s) < z - 1e-6:
            if a is None:
                a = s
        elif a is not None:
            out.append((a, s))
            a = None
    if a is not None:
        out.append((a, s1))
    return out


def _p14_depth(m):
    """the mean depth in the bed in month m (0 = Jan) on the flat reach (DEPTH): the higher of the two gauge routes"""
    return max(DEPTH["flat"][0][m], DEPTH["flat"][1][m])


def _p14_sea_depth(sea):
    ms = S4_MONTH_IDX[sea]
    return sum(_p14_depth(m) for m in ms) / float(len(ms))


def _p14_band_code(s, z):
    """the planting band (PLANT_BANDS code) of the ground at s, z by how often water reaches it: A the strip, B under
    the highest monthly mean water, C up to the flood terrace, D up to Q100, E up to Q500, F above"""
    G = _p14_geo()
    if G["zones"]["strip"][0] <= s <= G["zones"]["strip"][1]:
        return "A"
    if z <= G["bed"] + G["dmax"] + 1e-6:
        return "B"
    if z < G["shelf"] - 1e-6:
        return "C"
    if z <= G["q100"]:
        return "D"
    if z <= G["q500"]:
        return "E"
    return "F"


# ---------------------------------------------------------------- page helpers: clipping, shapes, plants, people
def _p14_clip_ring(ring, r):
    """ring clipped to the rectangle r = (x0, y0, x1, y1) (Sutherland-Hodgman), or None"""
    out = list(ring)
    for i in range(4):
        if len(out) < 3:
            return None

        def ins(p, i=i):
            return (p[0] >= r[0], p[1] >= r[1], p[0] <= r[2], p[1] <= r[3])[i]

        def cut(p, q, i=i):
            if i in (0, 2):
                t = (r[i] - p[0]) / (q[0] - p[0])
                return (r[i], p[1] + t * (q[1] - p[1]))
            t = (r[i] - p[1]) / (q[1] - p[1])
            return (p[0] + t * (q[0] - p[0]), r[i])
        inp, out = out, []
        prev = inp[-1]
        for cur in inp:
            if ins(cur):
                if not ins(prev):
                    out.append(cut(prev, cur))
                out.append(cur)
            elif ins(prev):
                out.append(cut(prev, cur))
            prev = cur
    return out if len(out) >= 3 else None


def _p14_clip_line(pts, r):
    """the runs of the polyline pts inside the rectangle r (Liang-Barsky)"""
    runs, cur = [], []
    for p, q in zip(pts[:-1], pts[1:]):
        t0, t1, ok = 0.0, 1.0, True
        dx, dy = q[0] - p[0], q[1] - p[1]
        for pp, qq in ((-dx, p[0] - r[0]), (dx, r[2] - p[0]), (-dy, p[1] - r[1]), (dy, r[3] - p[1])):
            if abs(pp) < 1e-12:
                if qq < 0:
                    ok = False
                    break
            elif pp < 0:
                t0 = max(t0, qq / pp)
            else:
                t1 = min(t1, qq / pp)
        if not ok or t0 > t1:
            if cur:
                runs.append(cur)
                cur = []
            continue
        a, b = (p[0] + t0 * dx, p[1] + t0 * dy), (p[0] + t1 * dx, p[1] + t1 * dy)
        if cur and abs(cur[-1][0] - a[0]) < 1e-9 and abs(cur[-1][1] - a[1]) < 1e-9:
            cur.append(b)
        else:
            if cur:
                runs.append(cur)
            cur = [a, b]
    if cur:
        runs.append(cur)
    return runs


def _p14_clip_items(items, r):
    """this board's page items cut to the rectangle r (a view or a key map stays inside its frame)"""
    out = []
    for it in items:
        if it[0] == "poly":
            rings = [c for c in (_p14_clip_ring(rg, r) for rg in it[1]) if c]
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
        elif it[0] == "image":                             # D1 a: a cutout keeps its whole picture, clipped at r
            x_, y_, w_, h_ = it[1:5]
            if x_ < r[2] and x_ + w_ > r[0] and y_ < r[3] and y_ + h_ > r[1]:
                out.append(tuple(it[:8]) + (r,))
    return out


def _p14_bb(items):
    """items_bbox with the D1 a images (cut to their clip)"""
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


def _p14_ell(cx, cy, rx, ry, rot=0.0, n=22):
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    out = []
    for i in range(n):
        t = 2.0 * math.pi * i / n
        u, v = rx * math.cos(t), ry * math.sin(t)
        out.append((cx + u * c - v * s, cy + u * s + v * c))
    return out


def _p14_band(pts, w):
    """a band w wide along the polyline pts, as one ring"""
    left, right = [], []
    for i, p in enumerate(pts):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L * w / 2.0, dx / L * w / 2.0
        left.append((p[0] + nx, p[1] + ny))
        right.append((p[0] - nx, p[1] - ny))
    return left + right[::-1]


P14_BARE = "DCD6C8"                  # a bare crown
P14_BARE_EDGE = "B0AC9C"
P14_BLOOM = "C97FA0"                 # in flower: one colour for every species, as in the calendars
P14_LEAF = "9DB46F"                  # in leaf, on the key


def _p14_state(key, month):
    """a species in month (1-12), from plants.py's sourced months: "cut" (loosestrife heads), "bloom", "leaf", "bare",
    or None when no leaf months are sourced and it is not in flower"""
    m = pla_months(key)
    if month in m["cut"]:
        return "cut"
    if month in m["bloom"]:
        return "bloom"
    if m["leaf"]:
        return "leaf" if month in m["leaf"] else "bare"
    return None


def _p14_cell(pg, x0, y0, x1, y1, st, leaf=None):
    """one calendar cell of a plant state"""
    r = rect(x0, y0, x1, y1)
    if st == "leaf":
        pg.poly([r], fill=leaf or P14_LEAF)
    elif st == "bloom":
        pg.poly([r], fill=P14_BLOOM)
    elif st == "bare":
        pg.poly([r], fill=COL["white"], stroke=P14_BARE_EDGE, lw=0.1)
    elif st == "cut":
        pg.poly([r], fill=COL["white"], stroke=P14_BLOOM, lw=0.1, stripes=(P14_BLOOM, 0.55, 0.1, 45.0))


P14_HR_BARE = {"plane": "plane_bare"}   # bare-month silhouettes of the high-res library (hires.py)


def _p14_plant(key, x, gy, k, month, h=None, cw=None, seed=0, style="b", layer=0, detail=True):
    """a species in section (plants.py) as it is that month (1-12), ground at (x, gy) page mm, k mm per m as printed
    (true size; a view passes its perspective k): a bare crown see-through, flowers only in its flowering months,
    loosestrife without its heads once they are cut. style "a": the species' cutout while it is in leaf (bare months
    and missing cutouts stay drawn). layer: the D9 fade only. Returns house shapes."""
    c = PLA_SPECIES[key]["colours"]
    st = _p14_state(key, month)
    if style == "a" and st != "bare":
        im = cut_image(key, x, gy, k / fig_depth(layer)[0], h_m=h or PLA_SPECIES[key]["h_m"], layer=layer,
                       facing=-1 if seed % 2 else 1, pick=seed)
        if im:
            return im
    fol = (c.get("fill"), c.get("lt"))
    acc = c.get("accent")
    out = []
    if st == "bare" and key in P14_HR_BARE and detail:  # assets_2: the high-res bare crown, branches in the stem colour
        sp = PLA_SPECIES[key]
        bare = hr_side(P14_HR_BARE[key], x, gy, k, h or sp["h_m"], cw or sp["crown_m"], c.get("stem"),
                       facing=-1 if seed % 2 else 1)
        out = [("poly", sh[1], sh[2], None, 0.1) for sh in bare or [] if sh[0] == "poly"]
    if not out:
        for sh in pla_section(key, x, gy, k, h, cw, False, seed, hires=detail, detail=detail):
            if sh[0] == "poly":
                fill = sh[2]
                if st == "bare" and fill in fol:      # a high-res fill (lw 0.0) takes no edge: its keyhole would show
                    out.append(("poly", sh[1], P14_BARE, c.get("stem") if sh[4] else None, 0.06, 0.6))
                    continue
                if acc and fill == acc and st != "bloom":
                    if st in ("cut", "bare"):
                        continue
                    fill = c.get("fill")
                out.append(("poly", sh[1], fill, sh[3], sh[4]))
            elif not (acc and sh[2] == acc and st != "bloom"):
                out.append(("line", sh[1], sh[2], sh[3]))
    if layer:
        out = [(s_[0], s_[1], fig_fade(s_[2], layer), fig_fade(s_[3], layer)) + tuple(s_[4:]) if s_[0] == "poly" else
               (s_[0], s_[1], fig_fade(s_[2], layer)) + tuple(s_[3:]) for s_ in out]
    return out


# ---------------------------------------------------------------- the animals on record (T1 ecology, GBIF)
# fauna.json (T1/ecology, H-ecology 29 Oct): species recorded near Bergama with the months that have records, from the
# GBIF occurrence search (eBird, iNaturalist, the Odonata atlas) in the town and basin boxes; reptiles under Squamata /
# Testudines. Fish: none on record in GBIF, so none are drawn. Order = the order shown; colours body, wing, light,
# bill, legs; h = size m.
P14_FAUNA = [
    dict(key="grey_heron", name=u"Grey heron", kind="heron", m=set(range(1, 13)), h=0.95,
         c=("9AA0A4", "5E676D", "F2F0EA", "D4A93C", "8A7D5A")),
    dict(key="white_stork", name=u"White stork", kind="stork", m={3, 4, 5, 6, 7, 8, 9}, h=1.0,
         c=("FFFFFF", "2C2219", "FFFFFF", "C8432F", "C8432F")),
    dict(key="kingfisher", name=u"Common kingfisher", kind="kingfisher", m={7, 8, 10, 11, 12}, h=0.17,
         c=("2A86B8", "1F5E86", "D9792B", "2C2219", "C8432F")),
    dict(key="barn_swallow", name=u"Barn swallow", kind="swallow", m={4, 5, 6, 7, 8, 9, 10}, h=0.2,
         c=("22304D", "22304D", "F1E7D8", "A33A2A", "22304D")),
    dict(key="little_egret", name=u"Little egret", kind="heron", m=set(range(1, 13)), h=0.6,
         c=("FFFFFF", "E9E6DE", "FFFFFF", "2C2219", "2C2219")),
    dict(key="black_stork", name=u"Black stork", kind="stork", m={1, 3, 4, 5, 6, 7, 9, 10, 11, 12}, h=1.0,
         c=("2F2A26", "2F2A26", "FFFFFF", "C8432F", "C8432F")),
    dict(key="white_wagtail", name=u"White wagtail", kind="songbird", m={1, 2, 3, 4, 5, 8, 10, 11, 12}, h=0.18,
         c=("8E9296", "2C2219", "FFFFFF", "2C2219", "2C2219")),
    dict(key="grey_wagtail", name=u"Grey wagtail", kind="songbird", m={8, 9, 10, 11}, h=0.18,
         c=("7D858C", "2C2219", "E8C94A", "2C2219", "C9B9A0")),
    dict(key="caspian_turtle", name=u"Western Caspian turtle", kind="turtle", m={2, 4, 5, 6, 8, 10}, h=0.2,
         c=("5B6236", "3A3F23", "D2C98E", "7E8450", "7E8450")),
    dict(key="marsh_frog", name=u"Marsh frog", kind="frog", m={2, 5, 7}, h=0.1,
         c=("7E9A4A", "4E6230", "DDD8A8", "2C2219", "4E6230")),
    dict(key="red_veined_darter", name=u"Red-veined darter", kind="dragonfly", m={8, 9}, h=0.07,
         c=("C2412D", "7A2418", "E8EEF0", "2C2219", "2C2219")),
    dict(key="banded_demoiselle", name=u"Banded demoiselle", kind="damselfly", m={8}, h=0.07,
         c=("2E6F8E", "1F3A4A", "C8D6DC", "1F3A4A", "1F3A4A")),
    dict(key="green_toad", name=u"European green toad", kind="toad", m={4, 8, 11}, h=0.1,
         c=("A7A47E", "5F7A45", "E4DFC8", "2C2219", "5F7A45")),
    dict(key="dice_snake", name=u"Dice snake", kind="snake", m={7}, h=0.08,
         c=("7D7A5C", "3F3C2C", "C9C3A0", "2C2219", "3F3C2C")),
    dict(key="tree_frog", name=u"Eastern tree frog", kind="frog", m={4}, h=0.05,
         c=("7DBA4A", "4F8A2E", "EAF0C8", "2C2219", "4F8A2E")),
]
# P14_FAUNA key -> high-res silhouette (hires.py; stand-ins of the same genus or family per GAPS.md D). Wagtails and
# the green toad have no vector in the pack: their pictograms stay.
P14_HR = dict(grey_heron="heron", white_stork="stork", kingfisher="kingfisher", barn_swallow="swallow",
              little_egret="egret", black_stork="stork", caspian_turtle="turtle", marsh_frog="frog",
              red_veined_darter="dragonfly", banded_demoiselle="damselfly", dice_snake="snake", tree_frog="frog")
P14_BIRDS = ("heron", "stork", "kingfisher", "swallow", "songbird")
P14_FAUNA_N = (7, 3)                 # animals shown a season at most, of them not birds at most
P14_FOOT = {"heron": 0.44, "stork": 0.46, "kingfisher": 0.27, "songbird": 0.2, "turtle": 0.1, "frog": 0.17,
            "toad": 0.17, "snake": 0.1}  # the pictogram's feet under its centre, x its size
P14_FAUNA_SRC = [u"Imani J et al. (2026). EOD – eBird Observation Dataset. Cornell Lab of Ornithology. "
                 u"https://doi.org/10.15468/aomfnb, accessed via GBIF.org 2026-10-29",
                 u"iNaturalist contributors (2026). iNaturalist Research-grade Observations. "
                 u"https://doi.org/10.15468/ab3s5x, accessed via GBIF.org 2026-10-29",
                 u"Boudot J, van Grunsven R (2021). Atlas of the dragonflies and damselflies of West and Central Asia. "
                 u"Version 1.4. https://doi.org/10.15468/gt3j2u, accessed via GBIF.org 2026-10-29"]


def _p14_fauna_for(sea):
    """the animals with records in the season's months: birds first, at most P14_FAUNA_N"""
    ms = set(m + 1 for m in S4_MONTH_IDX[sea])
    on = [f for f in P14_FAUNA if f["m"] & ms]
    rest = [f for f in on if f["kind"] not in P14_BIRDS][:P14_FAUNA_N[1]]
    return [f for f in on if f["kind"] in P14_BIRDS][:P14_FAUNA_N[0] - len(rest)] + rest


def _p14_fauna(pg, key, x, y, size, facing=1):
    """ONE place for the animal pictograms of pp.14-15 (figures.py, which will hold them, is paused): the P14_FAUNA
    animal key drawn in a size-mm square centred on (x, y), head to the left (facing -1: to the right), simple flat
    shapes in its own colours. 30 Oct: the high-res set (P14_HR) first, the pictograms where it has none."""
    fa = [f for f in P14_FAUNA if f["key"] == key][0]
    body, wing, light, bill, legs = fa["c"]
    kind = fa["kind"]
    lw = max(0.05, size / 70.0)
    white = body.upper() == "FFFFFF"
    hr = hr_fauna(P14_HR.get(key), x, y, size, fill=body, edge=COL["ink2"] if white else None, lw=lw,
                  facing=facing, foot=P14_FOOT.get(kind))   # assets_2: the high-res silhouette in its own body colour
    if hr:
        for sh in hr:
            if sh[0] == "poly":
                pg.poly([sh[1]], fill=sh[2])
            else:
                pg.line(sh[1], sh[2], sh[3])
        return
    dark = "2C2219"

    def T(u, v):
        return (x + u * size * facing, y + v * size)

    def P(pts, fill, edge=False, alpha=None):
        pg.poly([[T(u, v) for u, v in pts]], fill=fill, stroke=COL["ink2"] if edge else None, lw=lw, alpha=alpha)

    def E(cx, cy, rx, ry, rot, fill, edge=False, alpha=None):
        P(_p14_ell(cx, cy, rx, ry, rot), fill, edge, alpha)

    def B(pts, w, fill, edge=False):
        P(_p14_band(pts, w), fill, edge)

    def L(pts, colour, w):
        pg.line([T(u, v) for u, v in pts], colour, max(0.05, w * size))
    if kind == "heron":
        L([(0.04, -0.06), (0.02, -0.44)], legs, 0.022)
        L([(0.1, -0.06), (0.13, -0.44)], legs, 0.022)
        E(0.1, 0.0, 0.21, 0.1, -18, body, white)
        E(0.15, 0.02, 0.15, 0.065, -18, wing, white)
        P([(0.27, -0.05), (0.38, -0.13), (0.25, -0.1)], wing, white)
        B([(-0.06, 0.04), (-0.13, 0.14), (-0.08, 0.24), (-0.14, 0.33)], 0.05, light, True)
        E(-0.16, 0.36, 0.055, 0.04, 0, light, True)
        if not white:
            L([(-0.15, 0.38), (-0.03, 0.42)], dark, 0.015)
        P([(-0.2, 0.37), (-0.43, 0.34), (-0.2, 0.34)], bill)
    elif kind == "stork":
        L([(0.0, -0.06), (-0.02, -0.46)], legs, 0.024)
        L([(0.08, -0.06), (0.11, -0.46)], legs, 0.024)
        E(0.06, 0.02, 0.23, 0.11, -10, body, white)
        E(0.15, 0.0, 0.17, 0.075, -10, wing, white)
        if not white:
            E(0.0, -0.05, 0.12, 0.04, -10, light)
        B([(-0.1, 0.07), (-0.17, 0.27)], 0.07, body, white)
        E(-0.18, 0.3, 0.055, 0.045, 0, body, white)
        P([(-0.21, 0.32), (-0.46, 0.21), (-0.2, 0.28)], bill)
    elif kind == "kingfisher":
        L([(-0.4, -0.27), (0.42, -0.27)], "8B6B4A", 0.03)
        L([(0.0, -0.13), (0.0, -0.27)], legs, 0.02)
        B([(0.2, -0.05), (0.33, -0.22)], 0.06, wing)
        E(0.04, -0.04, 0.17, 0.12, 35, light)
        E(0.1, 0.02, 0.15, 0.09, 35, body)
        E(-0.1, 0.14, 0.1, 0.095, 0, body)
        E(-0.12, 0.1, 0.05, 0.035, 0, light)
        P([(-0.18, 0.17), (-0.46, 0.12), (-0.18, 0.11)], bill)
    elif kind == "swallow":
        P([(0.0, 0.03), (0.14, 0.36), (0.3, 0.4), (0.12, 0.0)], body)
        P([(0.0, -0.03), (0.12, -0.34), (0.27, -0.38), (0.12, 0.0)], wing)
        P([(0.18, 0.03), (0.47, 0.11), (0.26, 0.0), (0.47, -0.11), (0.18, -0.03)], body)
        E(0.0, 0.0, 0.21, 0.06, 0, body)
        E(0.02, -0.025, 0.13, 0.03, 0, light)
        E(-0.2, 0.0, 0.065, 0.055, 0, body)
        E(-0.23, -0.025, 0.035, 0.025, 0, bill)
    elif kind == "songbird":
        L([(0.0, -0.07), (-0.02, -0.2)], legs, 0.015)
        L([(0.05, -0.07), (0.05, -0.2)], legs, 0.015)
        B([(0.14, 0.0), (0.46, 0.09)], 0.05, wing)
        E(0.02, -0.01, 0.18, 0.09, 8, light, True)
        E(0.06, 0.03, 0.15, 0.065, 8, body)
        E(-0.15, 0.1, 0.075, 0.07, 0, body)
        E(-0.15, 0.04, 0.05, 0.04, 0, wing)
        P([(-0.21, 0.11), (-0.3, 0.1), (-0.21, 0.08)], bill)
    elif kind == "turtle":
        E(0.2, -0.08, 0.07, 0.04, 20, legs)
        E(-0.17, -0.08, 0.07, 0.04, -20, legs)
        B([(0.3, -0.03), (0.4, -0.08)], 0.04, legs)
        B([(-0.26, 0.0), (-0.36, 0.03)], 0.08, legs)
        E(-0.4, 0.03, 0.07, 0.05, 10, legs)
        L([(-0.45, 0.045), (-0.33, 0.02)], light, 0.012)
        P([(0.3 * math.cos(math.pi * i / 16.0), -0.04 + 0.24 * math.sin(math.pi * i / 16.0)) for i in range(17)],
          body, True)
        P(rect(-0.31, -0.08, 0.31, -0.04), light)
        for u_ in (-0.12, 0.0, 0.12):
            L([(u_, -0.04), (u_ * 1.2, 0.17 - abs(u_) * 0.5)], wing, 0.012)
        L([(-0.25, 0.08), (0.25, 0.08)], wing, 0.012)
    elif kind in ("frog", "toad"):
        E(0.12, -0.07, 0.17, 0.07, -8, wing)
        B([(0.04, -0.14), (0.34, -0.15)], 0.04, wing)
        E(0.0, 0.0, 0.26, 0.13, 12, body)
        E(-0.02, -0.06, 0.2, 0.05, 8, light)
        E(-0.2, 0.06, 0.1, 0.08, 0, body)
        B([(-0.12, -0.04), (-0.17, -0.16)], 0.04, body)
        spots = ((0.04, 0.07), (0.13, 0.03), (-0.05, 0.04))
        if kind == "toad":
            spots += ((0.0, 0.11), (0.17, 0.08), (-0.1, 0.1), (0.09, -0.01))
        for u_, v_ in spots:
            E(u_, v_, 0.025, 0.02, 0, wing)
        E(-0.2, 0.14, 0.045, 0.045, 0, light, True)
        E(-0.21, 0.14, 0.02, 0.02, 0, dark)
    elif kind == "dragonfly":
        for cy_, rot in ((0.17, 10), (-0.17, -10)):
            E(-0.2, cy_, 0.06, 0.2, rot, light, True, 0.8)
        for cy_, rot in ((0.18, -12), (-0.18, 12)):
            E(-0.08, cy_, 0.07, 0.21, rot, light, True, 0.8)
        B([(-0.12, 0.0), (0.46, 0.0)], 0.05, body)
        E(-0.2, 0.0, 0.08, 0.05, 0, wing)
        E(-0.32, 0.0, 0.05, 0.055, 0, body)
    elif kind == "damselfly":
        E(0.12, 0.07, 0.26, 0.045, 3, light, True, 0.8)
        E(0.16, 0.07, 0.1, 0.04, 3, wing, False, 0.85)
        B([(-0.1, 0.0), (0.48, 0.03)], 0.03, body)
        E(-0.17, 0.0, 0.07, 0.04, 0, body)
        E(-0.27, 0.01, 0.04, 0.04, 0, wing)
    else:                                                  # snake
        pts = [(-0.38, 0.02), (-0.25, 0.12), (-0.07, -0.04), (0.12, 0.1), (0.3, -0.04), (0.46, 0.0)]
        B(pts, 0.07, body)
        for u_, v_ in pts[1:-1]:
            E(u_, v_, 0.025, 0.02, 0, wing)
        E(-0.42, 0.02, 0.06, 0.04, 0, body)


def skyline(items, x0, x1, step=1.0):
    """Highest drawn point (page y) in every step-wide column from x0 to x1 (lines sampled along their length)."""
    n = int((x1 - x0) / step) + 2
    top = [-1e9] * n

    def put(x, y):
        i = int((x - x0) / step)
        if 0 <= i < n and y > top[i]:
            top[i] = y

    def seg(p, q):
        m = max(1, int(abs(q[0] - p[0]) / step) + 1)
        for j in range(m + 1):
            t = j / float(m)
            put(p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    for it in items:
        if it[0] == "poly":
            for r in it[1]:
                for i in range(len(r)):
                    seg(r[i], r[(i + 1) % len(r)])
        elif it[0] == "line":
            for i in range(len(it[1]) - 1):
                seg(it[1][i], it[1][i + 1])
        elif it[0] == "circle":
            put(it[1], it[2] + it[3])
        elif it[0] == "image":                             # a cutout: its picture's top edge
            seg((it[1], it[2] + it[4]), (it[1] + it[3], it[2] + it[4]))
    return lambda a, b: max(top[max(0, int((a - x0) / step)):max(1, int((b - x0) / step) + 1)] or [-1e9])


def sky_labels(pg, labs, items, x_lo, x_hi, y_cap, fs, boxes=None):
    """Short labels set in the open sky over a section, each as low as it fits above everything drawn under it and
    clear of the other labels, with a thin leader to its anchor. labs = [(ax, ay, [lines], colour, bold)]."""
    sky = skyline(items, x_lo - 60.0, x_hi + 60.0)
    boxes = boxes if boxes is not None else []
    lead = fs * 1.25
    for ax, ay, lines, colour, bold in sorted(labs, key=lambda t: t[0]):
        w = max(text_w(t, fs, bold) for t in lines) * BK_GROW + 0.8
        h = lead * len(lines) * BK_GROW
        best = None
        for x0 in (ax - 1.0, ax - w + 1.0, ax - w / 2.0):
            x0 = max(x_lo, min(x0, x_hi - w))
            y = max(sky(x0, x0 + w) + 1.2, ay + 1.5)
            while y + h < y_cap + 30.0:
                if not any(x0 < b[2] and b[0] < x0 + w and y < b[3] and b[1] < y + h for b in boxes):
                    break
                y += 0.5
            if best is None or y < best[1]:
                best = (x0, y)
        x0, y = best
        boxes.append((x0, y, x0 + w, y + h))
        for i, t in enumerate(lines):
            pg.text(t, x0 + 0.4, y + h - BK_GROW * lead * (i + 0.8), fs, colour, bold=bold)
        lx = min(max(ax, x0 + 0.6), x0 + w - 0.6)
        pg.line([(ax, ay), (lx, y - 0.3)], COL["ink2"], 0.1)
        pg.circle(ax, ay, 0.35, fill=COL["ink"])
    return boxes


def r28_mix(a, b, t):
    """hex colour a taken t of the way to b"""
    return u"".join(u"%02X" % int(round(int(a[i:i + 2], 16) * (1.0 - t) + int(b[i:i + 2], 16) * t)) for i in (0, 2, 4))


def occ_spans(ms):
    """the months ms (0 = Jan) as spans [(first, end)] along the year: Dec-Feb gives (0, 2) and (11, 12)"""
    out, m = [], 0
    while m < 12:
        if m in ms:
            n = m
            while n + 1 < 12 and (n + 1) in ms:
                n += 1
            out.append((m, n + 1))
            m = n + 1
        else:
            m += 1
    return out


# ---------------------------------------------------------------- the key map: S4 only, basemap "topographic"
P14_KEY = (130.0, 22.0)              # p.14: the key map's room (top right), mm; a key map states no scale, so it fills it


def _p14_keymap(pg, box, log=None):
    """the S4 key map at the top right of box (x0, y0, x1, y1): the analysis frame turned along its long side, upstream
    at the left, the shared basemap in its topographic mode (02 §1), ONLY the S4 cut with its look triangles and end
    names (D11), a north arrow at its left. Returns the box it took (the box's top edge when there is no basemap)."""
    x0, y0, x1, y1 = box
    fr = basemap_frame()
    if not fr:
        if log is not None:
            log.append(u"pp.14-15 key map: no basemap data (run the site board v51+ once); pages drawn without it")
        return (x1, y1, x1, y1)
    cx, cy = sum(p[0] for p in fr) / len(fr), sum(p[1] for p in fr) / len(fr)
    e1 = (fr[1][0] - fr[0][0], fr[1][1] - fr[0][1])
    e2 = (fr[2][0] - fr[1][0], fr[2][1] - fr[1][1])
    u = e1 if math.hypot(*e1) >= math.hypot(*e2) else e2
    L = math.hypot(*u)
    u = (u[0] / L, u[1] / L)
    if (fr[0][0] - cx) * u[0] + (fr[0][1] - cy) * u[1] > 0:      # the upstream end at the left
        u = (-u[0], -u[1])
    v = (-u[1], u[0])
    us = [(p[0] - cx) * u[0] + (p[1] - cy) * u[1] for p in fr]
    vs = [(p[0] - cx) * v[0] + (p[1] - cy) * v[1] for p in fr]
    na = 9.0                                                      # room for the north arrow
    den = max((max(us) - min(us)) * 1000.0 / (x1 - x0 - na), (max(vs) - min(vs)) * 1000.0 / (y1 - y0))
    k = 1000.0 / den
    ox, oy = x1 - max(us) * k, y1 - max(vs) * k

    def T(p):
        return (ox + ((p[0] - cx) * u[0] + (p[1] - cy) * u[1]) * k, oy + ((p[0] - cx) * v[0] + (p[1] - cy) * v[1]) * k)
    R = (ox + min(us) * k, oy + min(vs) * k, ox + max(us) * k, oy + max(vs) * k)
    sbox = (min(p[0] for p in fr), min(p[1] for p in fr), max(p[0] for p in fr), max(p[1] for p in fr))
    sp = Page(0, 0)

    def fade(hx, alpha):
        return hx if alpha is None or alpha >= 0.999 else r28_mix(hx, "FFFFFF", 1.0 - max(0.0, float(alpha)))

    def fill_fn(rings, hx, alpha, nonzero):
        sp.poly([r_ for r_ in rings if len(r_) >= 3], fill=fade(hx, alpha))

    def line_fn(pts, hx, w_mm, dash_mm, alpha):
        d_ = None
        if dash_mm:
            d_ = list(dash_mm) if isinstance(dash_mm, (list, tuple)) else [dash_mm, dash_mm]
        sp.line(pts, fade(hx, alpha), w_mm, dash=d_)

    def text_fn(s, xy, size_mm, hx, bold=False, align="L"):
        sp.text(s, xy[0], xy[1], max(size_mm, FS_MIN), hx, bold=bold, align=(str(align or u"L")[-1:]).upper())   # v7.1: "MC" -> "C"
    try:
        items = basemap_items("topographic", box=sbox, split_buildings=True)
        cut = basemap_cut_items(basemap_cut_ids(["S4"]), den, text_mm=FS_MIN)
        pg.poly([rect(*R)], fill=COL["white"])
        basemap_draw(list(items) + list(cut), T, fill_fn, line_fn, text_fn)
    except Exception as ex:
        if log is not None:
            log.append(u"pp.14-15 key map not drawn: {}: {}".format(type(ex).__name__, ex))
        return (x1, y1, x1, y1)
    pg.items += _p14_clip_items(sp.items, R)
    pg.poly([rect(*R)], fill=None, stroke=COL["ink2"], lw=0.2)
    nx, ny = u[1], v[1]                                           # survey north in the page
    n_ = math.hypot(nx, ny) or 1.0
    nx, ny = nx / n_, ny / n_
    ax, ay = R[0] - na / 2.0, R[3] - 6.0
    px, py = -ny, nx
    tip, tail = (ax + nx * 3.0, ay + ny * 3.0), (ax - nx * 3.0, ay - ny * 3.0)
    pg.poly([[tip, (tail[0] + px * 1.4, tail[1] + py * 1.4), (ax - nx * 1.4, ay - ny * 1.4),
              (tail[0] - px * 1.4, tail[1] - py * 1.4)]], fill=COL["ink_dark"])
    pg.text(u"N", tip[0] + nx * 2.2, tip[1] + ny * 2.2 - FS_MIN * 0.35, FS_MIN, COL["ink_dark"], bold=True, align="C")
    return (R[0] - na, R[1], R[2], R[3])


# ---------------------------------------------------------------- the cut, drawn (pp.14 and 15)
P14_LOOK = {  # each season's colours in the views, and its water on the cuts
    "winter": dict(sky="DCE3E6", far="B3B8AA", grass="A3A98A", gravel="BBB4A2", water="86AEBC"),
    "spring": dict(sky="E3EDF0", far="B4C497", grass="98B46C", gravel="CEC6B3", water="96BCC8"),
    "summer": dict(sky="F3EFE2", far="CCC198", grass="CBBD84", gravel="DDD4BE", water="8CBBC8"),
    "autumn": dict(sky="ECE5D7", far="BFB18A", grass="B7A676", gravel="D5CCB6", water="90B5C1"),
}
P14_FIG = "4F453C"                   # the people in the views


def _p14_back(X, Y, k, rng, month, style="b"):
    """the trees beyond the cut (R16: depth through faded background trees): plants.py's mixed scatter of S4's own
    tree species in D9 layers 2 and 1 on the cut's ground line, never over the bed, each in the month's state.
    Returns house shapes."""
    G = _p14_geo()
    xa, xb = X(rng[0]), X(rng[1])

    def gy(x):
        return Y(_p14_surf(rng[0] + (x - xa) / k))
    mix = sorted(set(p[0] for p in P14_PLANTS if PLA_SPECIES[p[0]]["layer"] == "tree"))
    out = []
    if not mix:
        return out
    for layer in (2, 1):
        sc = fig_depth(layer)[0]
        _sh, placed = pla_scatter_section(xa, xb, gy, k, t0=0.40, t1=0.70, mix=mix, seed=40 + layer, layer=layer,
                                          density=0.6, hires=False, detail=False, avoid=[(X(G["b0"]), X(G["b1"]))])
        for i, (key, x, h, w) in enumerate(placed):
            if h > P14_TREE_MAX:
                w, h = w * P14_TREE_MAX / h, P14_TREE_MAX
            out += _p14_plant(key, x, gy(x), k * sc, month, h, w, 50 * layer + i, style, layer, detail=False)
    return out


def _p14_cut(pg, x0, yb, k, rng, sea, month, people=True, style="b", water="season", back=True):
    """the S4 cut from rng[0] to rng[1] (m across) at k mm per m, rng[0] at x0 and its base (G["base"]) at yb, as it is
    in sea, layered as M5 sets it: the trees beyond (R16), the cut ground (earth, the gravel bed, the concrete strip
    liner, walk, steps and promenade), the water (water "season": the season's mean depth as a sheet over the bed, else
    the strip full, Q100 / Q500 in winter; "avg": the registry's average yearly flow and Q100 / Q500 through water.py),
    S4's planting in month's state, the season's people and stalls (P14_USE, true size). style "a": cutouts (D1).
    Returns (X, Y): m across -> page x, level -> page y."""
    G = _p14_geo()
    s0, s1 = rng
    zb = G["base"]

    def X(s):
        return x0 + (s - s0) * k

    def Y(z):
        return yb + (z - zb) * k
    clip = (X(s0), -1e9, X(s1), 1e9)
    if back:
        shp_put(pg, _p14_back(X, Y, k, rng, month, style))

    def put(ring_m, mat):
        r_ = _p14_clip_ring([(X(s), Y(z)) for s, z in ring_m], clip)
        if r_:
            sec_put(pg, sct_hatch_fill(r_, mat, k, None, 0.1))
    bed, sfl, shelf, zn = G["bed"], G["sfl"], G["shelf"], G["zones"]
    st0, st1 = zn["strip"]
    lt = P14_LINER
    pts = [(s0, _p14_surf(s0))] + [p for p in G["prof"] if s0 < p[0] < s1] + [(s1, _p14_surf(s1))]
    put(pts + [(s1, zb), (s0, zb)], "earth")
    for a, b in ((G["b0"], st0 - lt), (st1 + lt, G["b1"])):
        put([(a, bed), (b, bed), (b, bed - P14_GRAVEL), (a, bed - P14_GRAVEL)], "gravel")
    t0, t1 = zn["terrace"]
    put([(t0, shelf), (t1, shelf), (t1, shelf - 0.3), (t0, shelf - 0.3)], "gravel")
    put([(st0 - lt, bed), (st0 - lt, sfl - lt), (st1 + lt, sfl - lt), (st1 + lt, bed), (st1, bed), (st1, sfl),
         (st0, sfl), (st0, bed)], "concrete")
    w0, w1 = P14_WALK
    put([(w0, shelf), (w1, shelf), (w1, shelf - 0.2), (w0, shelf - 0.2)], "concrete")
    e0, p0 = zn["steps"]
    put([p for p in G["prof"] if e0 - 1e-9 <= p[0] <= p0 + 1e-9 and p[1] >= shelf - 1e-9] +
        [(p0, P14_PROM - 0.35), (e0, shelf - 0.35)], "concrete")
    p2 = zn["bike"][1]
    put([(p0, P14_PROM), (p2, P14_PROM), (p2, P14_PROM - P14_SLAB), (p0, P14_PROM - P14_SLAB)], "concrete")
    pg.line([(X(s), Y(z)) for s, z in pts], COL["ink_dark"], 0.3)
    b0_, b1_ = max(zn["bike"][0], s0), min(zn["bike"][1], s1)
    if b1_ > b0_:
        pg.line([(X(b0_), Y(P14_PROM) + 0.25), (X(b1_), Y(P14_PROM) + 0.25)], "B98A74", 0.5)
    # the water, before the plants and people (M5 layer order)
    if water == "avg":
        zw = level_avg_flow("S4")
        wl = water_section([(X(s), Y(z)) for s, z in pts], k, Y, cid="S4", labels=False)
        shp_put(pg, wl.shapes(("water",)))
        wet = _p14_wet(zw, s0, s1)
    else:
        depth = _p14_sea_depth(sea)
        if depth >= P14_SHEET_M:
            zw = bed + depth
            wet = _p14_wet(zw, s0, s1)
        else:
            zw = bed
            wet = [(max(st0, s0), min(st1, s1))] if st1 > s0 and st0 < s1 else []
        for a, b in wet:
            ring = [(X(a), Y(zw))] + [(X(s), Y(z)) for s, z in G["prof"] if a < s < b] + [(X(b), Y(zw))]
            pg.poly([ring], fill=P14_LOOK[sea]["water"], alpha=0.85)
            pg.line([(X(a), Y(zw)), (X(b), Y(zw))], C["w3"], 0.2)
        if sea == "winter":
            for zq in (G["q100"], G["q500"]):
                for a, b in _p14_wet(zq, s0, s1):
                    pg.line([(X(a), Y(zq)), (X(b), Y(zq))], C["w4"], 0.18, dash=[1.2, 0.7])
    # the planting in the month's state, tall first so the low layer reads in front
    for i, (key, s, h, cw) in sorted(enumerate(P14_PLANTS), key=lambda t: -t[1][2]):
        if s0 + 0.3 <= s <= s1 - 0.3:
            shp_put(pg, _p14_plant(key, X(s), Y(_p14_surf(s)), k, month, h, cw, i, style))
    if people:
        for pose, s, face, seed in _p14_people(sea):
            if s0 + 1.0 <= s <= s1 - 1.0:
                z = _p14_surf(s)
                under = any(a <= s <= b for a, b in wet) and z < zw
                shp_put(pg, _p14_person(pose, X(s), Y(z), k, face, seed, style, wl=Y(zw) if under else None))
    return X, Y


def _p14_cal_band(pg, X, ytop, sea, rng):
    """under a season's cut: a line a month of the season (the first month on top), a cell under the plants in their
    state that month (plants.py's sourced months; one cell where plants stand closer than a cell), the months named
    at the left"""
    ms = [m + 1 for m in S4_MONTH_IDX[sea]]
    hh, cw = 1.15, 1.2
    for i in range(len(ms) + 1):
        pg.line([(X(rng[0]), ytop - i * hh), (X(rng[1]), ytop - i * hh)], COL["faint"], 0.08)
    pg.text(S4_MONTHS[sea], X(rng[0]) + 0.4, ytop - hh * len(ms) / 2.0 - FS_MIN * 0.35, FS_MIN, COL["ink2"])
    last = X(rng[0]) + text_w(S4_MONTHS[sea], FS_MIN) + 1.0
    for key, s, h, cw_ in P14_PLANTS:
        if rng[0] <= s <= rng[1] and X(s) - cw / 2.0 > last + 0.15:
            last = X(s) + cw / 2.0
            for i, m in enumerate(ms):
                st = _p14_state(key, m)
                if st:
                    _p14_cell(pg, X(s) - cw / 2.0, ytop - (i + 1) * hh + 0.12, X(s) + cw / 2.0, ytop - i * hh - 0.12,
                              st, PLA_SPECIES[key]["colours"].get("fill"))


# ---------------------------------------------------------------- the view: the same spot in every season (p.14)
P14_EYE = (22.5, 1.60)               # the viewpoint of every view: on the lower walk (m across S4), eye height m
P14_VIEW = (0.26, 0.62, 0.55)        # focal length x the view's width; the vanishing point's x, y as shares of the view
P14_SURF = {"road": "B4AFA2", "street": "B4AFA2", "path": "CEC7B5", "crest": "A7A08F", "strip_side": "B8B2A4",
            "walk": "D9D4C7", "riser": "A9A394", "tread": "DCD7CA", "prom": "E4DFD2", "bike": "B98A74"}


def _p14_surf_col(tag, look):
    if tag in P14_SURF:
        return P14_SURF[tag]
    if tag in ("slope_sw", "slope_ne", "fill"):
        return look["grass"]
    if tag == "terrace":
        return r28_mix(look["gravel"], look["grass"], 0.45)
    if tag == "strip":
        return r28_mix(look["gravel"], "6F6A5E", 0.25)
    return look["gravel"]


P14_VIEW_PEOPLE = (7.0, 22.0, 17.0)  # people in the view: nearest depth m, depth spread m, a second walker this far behind
P14_FAR = (130.0, 170.0, 230.0, 320.0)   # depths m of the far tree line along both banks (simple crowns, the far tone)


def _p14_rng(seed):
    """a small repeatable random generator: rnd() -> 0..1"""
    st = [(int(seed) * 2654435761 + 12345) % 2147483647 or 1]

    def rnd():
        st[0] = (st[0] * 48271) % 2147483647
        return st[0] / 2147483647.0
    return rnd


def _p14_view(pg, box, sea, style="b"):
    """one rectangular view, the same in every season: a one-point perspective up the Selinos stream from the lower
    walk (P14_EYE), the S4 cut carried along the stream, the water at the season's level, S4's planting as it is that
    month repeated along both banks to a far tree line, the season's people at their zones (P14_USE) and stalls, up to
    three of its animals. Ground textured (gravel, grass, paving), sky graded; far things fade by D9 layer (style b
    tones, style a cutout opacity). Faces turned away are left out, the rest is laid far to near; everything is cut to
    the rectangle. style "a": cutouts for the planting and the people, soft shadows, a light vignette (D1)."""
    x0, y0, x1, y1 = box
    G = _p14_geo()
    month = P14_SEA_MONTH[sea]
    look = P14_LOOK[sea]
    W, H = x1 - x0, y1 - y0
    f = P14_VIEW[0] * W
    vx, vy = x0 + P14_VIEW[1] * W, y0 + P14_VIEW[2] * H
    sc = P14_EYE[0]
    zc = _p14_surf(sc) + P14_EYE[1]
    rnd = _p14_rng(SEAS.index(sea) + 7)

    def pr(s, z, d):
        return (vx + f * (s - sc) / d, vy + f * (z - zc) / d)

    def lay(d):
        return 0 if d < 18.0 else (1 if d < 45.0 else 2)
    sp = Page(0, 0)
    for i in range(4):                                            # the sky, lighter toward the horizon
        ya, yb_ = vy + (y1 - vy) * i / 4.0, vy + (y1 - vy) * (i + 1) / 4.0
        sp.poly([rect(x0, ya, x1, yb_)], fill=r28_mix(look["sky"], COL["white"], 0.45 - 0.15 * i))
    sp.poly([rect(x0, y0, x1, vy)], fill=look["far"])
    dn, df = 0.6, 4000.0
    pts = G["prof"]
    segs = ([((pts[0][0] - 800.0, pts[0][1]), pts[0], "road")] + list(G["segs"]) +
            [(pts[-1], (pts[-1][0] + 800.0, pts[-1][1]), "street")])
    draws = []
    for a, b, tag in segs:
        if -(b[1] - a[1]) * (sc - a[0]) + (b[0] - a[0]) * (zc - a[1]) <= 1e-9:
            continue                                              # turned away from the eye
        key = 0.0 if a[0] <= sc <= b[0] else min(abs(a[0] - sc), abs(b[0] - sc))
        draws.append((key, a, b, tag))
    depth = _p14_sea_depth(sea)
    if depth >= P14_SHEET_M:
        zw = G["bed"] + depth
        wet = _p14_wet(zw, G["b0"] - 2.0, G["b1"] + 6.0)
    else:
        zw = G["bed"]
        wet = [G["zones"]["strip"]]
    for a, b in wet:
        key = 0.0 if a <= sc <= b else min(abs(a - sc), abs(b - sc))
        draws.append((key - 1e-3, (a, zw), (b, zw), "water"))
    draws.sort(key=lambda t: -t[0])
    edge = r28_mix(look["far"], COL["ink_dark"], 0.35)
    for key, a, b, tag in draws:
        colr = look["water"] if tag == "water" else _p14_surf_col(tag, look)
        sp.poly([[pr(a[0], a[1], dn), pr(b[0], b[1], dn), pr(b[0], b[1], df), pr(a[0], a[1], df)]], fill=colr,
                stroke=colr, lw=0.05)
        if tag == "water":
            for i, d in enumerate((5.0, 7.5, 11.0, 16.0, 23.0, 33.0, 48.0)):
                m_ = a[0] + (b[0] - a[0]) * (0.25 + 0.5 * ((i * 0.37) % 1.0))
                hw = (b[0] - a[0]) * 0.1
                sp.line([pr(m_ - hw, zw, d), pr(m_ + hw, zw, d)], COL["white"], 0.12)
            if style == "a":                                      # the sky caught on the water, far half
                sp.poly([[pr(a[0], zw, 14.0), pr(b[0], zw, 14.0), pr(b[0], zw, df), pr(a[0], zw, df)]],
                        fill=look["sky"], alpha=0.35)
            continue
        if tag in ("tread", "riser", "walk", "prom", "crest", "strip_side", "bike"):
            for p_ in (a, b):
                sp.line([pr(p_[0], p_[1], dn), pr(p_[0], p_[1], 400.0)], edge, 0.07)
            if tag in ("prom", "walk"):                          # paving joints
                for d in range(3, 90, 3):
                    sp.line([pr(a[0], a[1], float(d)), pr(b[0], b[1], float(d))], edge, 0.04)
        tex = r28_mix(colr, COL["ink_dark"], 0.22)
        if tag in ("gravel", "strip", "terrace", "path", "crest"):   # gravel: stones, larger near
            for _i in range(int(14 + 6 * abs(b[0] - a[0]) ** 0.5)):
                d = 1.5 + 34.0 * rnd() ** 1.6
                s_ = a[0] + (b[0] - a[0]) * rnd()
                z_ = a[1] + (b[1] - a[1]) * (s_ - a[0]) / ((b[0] - a[0]) or 1.0)
                x_, y_ = pr(s_, z_, d)
                r_ = 0.05 * f / d
                if r_ > 0.04:
                    sp.poly([_p14_ell(x_, y_, r_, r_ * 0.45, 0.0, 8)], fill=tex)
        elif tag in ("slope_sw", "slope_ne", "fill"):             # grass: short blades, longer near
            for _i in range(int(20 + 8 * abs(b[0] - a[0]) ** 0.5)):
                d = 1.5 + 30.0 * rnd() ** 1.6
                s_ = a[0] + (b[0] - a[0]) * rnd()
                z_ = a[1] + (b[1] - a[1]) * (s_ - a[0]) / ((b[0] - a[0]) or 1.0)
                p_, q_ = pr(s_, z_, d), pr(s_ + 0.03, z_ + 0.18, d)
                if q_[1] - p_[1] > 0.12:
                    sp.line([p_, q_], tex, 0.06)
    spr = []
    for d in P14_FAR:                                             # the far tree line, both banks
        for s_ in [G["b0"] - 9.0 + 4.5 * j for j in range(3)] + [G["b1"] + 6.0 + 7.0 * j for j in range(6)]:
            spr.append((d + 9.0 * rnd(), "far", (s_ + 2.0 * rnd(), 9.0 + 5.0 * rnd())))
    for i, (key, s, h, cw) in enumerate(P14_PLANTS):
        tall = h >= 6.0
        step = 13.0 if tall else (7.0 if h >= 2.0 else 3.5)
        dvis = (sc - s) * P14_VIEW[0] / P14_VIEW[1] if s < sc else (s - sc) * P14_VIEW[0] / (1.0 - P14_VIEW[1])
        d = max(dvis * 0.9, 9.0 if tall else 2.5) + (i % 3) * step / 3.0
        j = 0
        while d < (110.0 if tall else (60.0 if h >= 2.0 else 35.0)):
            spr.append((d, "plant", (key, s + ((j * 7 + i) % 5 - 2) * 0.15, h, cw, i * 31 + j)))
            d += step
            j += 1
    for i, (pose, s, face, seed) in enumerate(_p14_people(sea)):
        d = P14_VIEW_PEOPLE[0] + P14_VIEW_PEOPLE[1] * ((seed * 53 + i * 29) % 97) / 97.0
        spr.append((d, "fig", (pose, s, face, seed)))
        if pose in ("walk", "adult_child", "group", "bike") and i % 2 == 0:
            spr.append((d + P14_VIEW_PEOPLE[2], "fig", (pose, s + 0.6, -face, seed + 5)))
    fa = _p14_fauna_for(sea)                                      # a wading bird, a flying or perched one, one more
    wad = [a for a in fa if a["kind"] in ("heron", "stork")]
    fly = [a for a in fa if a["kind"] in ("swallow", "kingfisher", "songbird")]
    oth = [a for a in fa if a["kind"] not in P14_BIRDS]
    if wad:
        spr.append((17.0, "animal", (wad[0], -8.0, None)))
    if fly:
        spr.append((10.0, "animal", (fly[0], 12.0, zc + 2.2) if fly[0]["kind"] == "swallow" else (fly[0], 0.9, None)))
    if oth:
        at = {"turtle": (0.7, None, 11.0), "frog": (1.2, None, 10.0), "toad": (3.0, None, 9.0),
              "snake": (2.0, None, 10.0), "dragonfly": (-1.5, G["bed"] + 0.8, 9.0),
              "damselfly": (-0.8, G["bed"] + 0.6, 9.0)}.get(oth[0]["kind"], (1.2, None, 10.0))
        spr.append((at[2], "animal", (oth[0], at[0], at[1])))
    spr.sort(key=lambda t: -t[0])
    farc = r28_mix(look["far"], COL["ink_dark"], 0.12)
    shade = "2E2A22"
    for d, kind, data in spr:
        k = f / d
        if kind == "far":
            s_, h_ = data
            x, y = pr(s_, _p14_surf(s_), d)
            sp.poly([_p14_ell(x, y + h_ * k * 0.62, h_ * k * 0.42, h_ * k * 0.4, 0.0, 12)], fill=farc)
        elif kind == "plant":
            key, s, h, cw, seed = data
            x, y = pr(s, _p14_surf(s), d)
            if style == "a" and d < 30.0:
                sp.poly([_p14_ell(x, y, cw * k * 0.35, cw * k * 0.05, 0.0, 14)], fill=shade, alpha=0.15)
            shp_put(sp, _p14_plant(key, x, y, k, month, h, cw, seed, style, lay(d), detail=d < 20.0))
        elif kind == "fig":
            pose, s, face, seed = data
            z = _p14_surf(s)
            x, y = pr(s, z, d)
            under = any(a <= s <= b for a, b in wet) and z < zw
            if style == "a" and pose != "market":
                sp.poly([_p14_ell(x, y, 0.35 * k, 0.07 * k, 0.0, 12)], fill=shade, alpha=0.2)
            shp_put(sp, _p14_person(pose, x, y, k, face, seed, style, lay(d), pr(s, zw, d)[1] if under else None,
                                    P14_FIG))
        else:
            a_, s, z = data
            sz = max(a_["h"] * k * 1.3, 3.2)
            if z is None:
                x, y = pr(s, _p14_surf(s), d)
                y += P14_FOOT.get(a_["kind"], 0.0) * sz
            else:
                x, y = pr(s, z, d)
            _p14_fauna(sp, a_["key"], x, y, sz, 1)
    if style == "a":                                              # a light vignette: the near ground darker
        sp.poly([rect(x0, y0, x1, y0 + 0.16 * H)], fill=shade, alpha=0.1)
        sp.poly([rect(x0, y0, x1, y0 + 0.07 * H)], fill=shade, alpha=0.1)
    pg.items += _p14_clip_items(sp.items, box)
    pg.poly([rect(x0, y0, x1, y1)], fill=None, stroke=COL["ink2"], lw=0.2)


# ---------------------------------------------------------------- p.14
P14_COLS = (36.0, 21.0, 46.0, 3.0)   # the season column, the level ladder, the animals column, the gap, mm
P14_RAIN_MAX = 110.0                 # rain, mm a month, at the top of the small bars
P14_DEPTH_MAX = 0.25                 # water, m, that fills the small channel


def _p14_season_tag(pg, x, ytop, w, h, sea):
    """the season's name and months, then a month each: its rain (MGM normals, RAIN) as a bar and the mean water depth
    in the bed (DEPTH) in a small channel, the values on them"""
    fs = FS_MIN
    w -= 2.0
    pg.poly([rect(x, ytop - 0.9, x + w, ytop)], fill=BAND_BLUE[SEAS.index(sea)])
    pg.text(sea.upper(), x, ytop - 5.6, 4.2, COL["ink_dark"], bold=True)
    pg.text(S4_MONTHS[sea], x, ytop - 5.6 - fs * 1.4, fs, COL["ink2"], bold=True)
    cw = w / 3.0
    rh = max(5.0, min(12.0, h - 30.0))
    yr = ytop - 5.6 - fs * 1.4 - 1.6 - fs - 0.6 - rh
    pg.line([(x, yr), (x + w, yr)], COL["ink2"], 0.1)
    for i, m in enumerate(S4_MONTH_IDX[sea]):
        cx = x + (i + 0.5) * cw
        bh = rh * min(1.0, RAIN[m] / P14_RAIN_MAX)
        pg.poly([rect(cx - cw * 0.22, yr, cx + cw * 0.22, yr + bh)], fill=C["w3"])
        pg.text(u"{:.0f}".format(RAIN[m]), cx, yr + bh + 0.6, fs, C["w4"], align="C")
        pg.text(MONTHS[m], cx, yr - fs * 1.1, fs, COL["ink2"], align="C")
        gh, gw = 3.6, cw * 0.36
        yc = yr - fs * 1.1 - 1.4
        t = min(1.0, _p14_depth(m) / P14_DEPTH_MAX)
        ww = gw * 0.55 + gw * 0.45 * t
        pg.poly([[(cx - gw * 0.55, yc - gh), (cx + gw * 0.55, yc - gh), (cx + ww, yc - gh + gh * t),
                  (cx - ww, yc - gh + gh * t)]], fill=C["w2"])
        pg.line([(cx - gw, yc), (cx - gw * 0.55, yc - gh), (cx + gw * 0.55, yc - gh), (cx + gw, yc)], COL["ink"], 0.2)
        pg.text(u"{:.2f}".format(_p14_depth(m)), cx, yc - gh - fs * 1.05, fs, C["w4"], align="C")


def _p14_animals(pg, x, ytop, w, h, sea):
    """the animals on record that season: pictogram and name, one under the other"""
    sel = _p14_fauna_for(sea)
    if not sel:
        return
    pitch = min(6.6, h / float(len(sel)))
    sz = min(6.0, pitch - 0.5)
    for i, fa in enumerate(sel):
        cy = ytop - pitch * (i + 0.5)
        _p14_fauna(pg, fa["key"], x + sz / 2.0, cy, sz)
        pg.text(fa["name"], x + sz + 1.5, cy - FS_MIN * 0.35, FS_MIN, COL["ink_dark"])


def _p14_state_key(pg, x, y):
    """the plant states as drawn samples, one line from the top y; returns its bottom y"""
    fs = FS_MIN
    yy = y - fs * 1.1
    t = u"plants, under each cut a line a month:"
    pg.text(t, x, yy, fs, COL["ink2"])
    xx = x + text_w(t, fs) + 2.0
    for st, word in (("leaf", u"in leaf"), ("bloom", u"in flower"), ("bare", u"bare"), ("cut", u"heads cut")):
        _p14_cell(pg, xx, yy - 0.2, xx + 3.2, yy + fs * 0.75, st)
        pg.text(word, xx + 4.2, yy, fs, COL["ink"])
        xx += 4.2 + text_w(word, fs) + 3.5
    return yy - fs * 0.5


def _p14_plant_key(pg, x, ytop, w, h, style="b"):
    """the species on the cuts, a small drawing (May) and the name each, in one row w wide from x; returns the
    bottom y"""
    cw = w / float(len(P15_PLANT_ROWS))
    for i, key in enumerate(P15_PLANT_ROWS):
        hh, cr = _p14_size(key)
        kk = (h - 1.0) / max(hh, cr)
        xx = x + i * cw
        shp_put(pg, _p14_plant(key, xx + cr * kk / 2.0 + 0.3, ytop - h + 0.5, kk, 5, hh, cr, 0, style))
        pg.text(PLA_SPECIES[key]["name"], xx + cr * kk + 1.6, ytop - h / 2.0 - FS_MIN * 0.35, FS_MIN, COL["ink"])
    return ytop - h


# ---------------------------------------------------------------- D1: both styles, the style a copy right of the board
P14_EXT_GAP = 6.0                    # mm between the board and a style a copy (the board's cell gap)


def _p14_ext_box(pg, box, title):
    """D1 (revision 30 Oct): room for a panel's style a copy right of everything on the board, at the same height and
    size as box: the board grows to the right (pg.W and BOARD_W, which booklet_export reads for its crops), a white
    panel with its title. Returns the copy's box."""
    global BOARD_W
    w = box[2] - box[0]
    x0 = pg.W + P14_EXT_GAP
    pg.poly([rect(pg.W, 0.0, x0 + w + M, pg.H)], fill=COL["sheet"])
    pg.poly([rect(x0 - 4.0, box[1] - 3.0, x0 + w + 4.0, box[3] + 11.5)], fill=COL["white"], stroke=COL["faint"],
            lw=0.25)
    pg.text(title + u" · style a", x0, box[3] + 4.0, 4.0, COL["ink_dark"], bold=True)
    pg.W = x0 + w + M
    BOARD_W = pg.W
    return (x0, box[1], x0 + w, box[3])


def _p14_crop_ids(cid):
    """the D1 crop ids cid_a / cid_b laid out like cid (BK_FIXED: printed 1:1) with cid's caption"""
    global BK_FIXED
    BK_FIXED = tuple(BK_FIXED) + tuple(i for i in (cid + "_a", cid + "_b") if i not in BK_FIXED)
    for s_ in ("_a", "_b"):
        BK_CAPTIONS.setdefault(cid + s_, BK_CAPTIONS.get(cid, u""))
    return [cid, cid + "_b", cid + "_a"]


def _p14_g6(k, keys, log, what):
    """the G6 check of a drawing (section_frame.py): people true size at k, every plant inside its sourced range; one
    log line when something is off"""
    bad = sf_assert_g6(k, trees=[(p[0], p[2]) for p in keys], strict=False)
    if bad and log is not None:
        log.append(u"WARNING (G6) {}: {}".format(what, u"; ".join(bad)))


def _p14_panel(pg, box, log, style):
    """p.14 in one style, drawn whole into box: the context line and the plant-state key, the S4 key map at the top
    right, the column heads, then a row a season (rain and water, the cut at 1:500 with its levels at the right and
    the trees beyond it, the view, the animals), the scale bar flush with the cuts' column. Returns its bbox."""
    x0, y0, x1, y1 = box
    n0 = len(pg.items)
    fs = FS_MIN
    G = _p14_geo()
    k = 1000.0 / P14_DEN
    wa, wl, wd, gap = P14_COLS
    kb = _p14_keymap(pg, (x1 - P14_KEY[0], y1 - P14_KEY[1], x1, y1), log)
    cb = context(pg, x0, y1, kb[0] - x0 - 8.0, "seasons")
    yk = _p14_state_key(pg, x0, cb[1] - 1.0)
    yk = _p14_plant_key(pg, x0, yk - 1.0, kb[0] - x0 - 8.0, 9.0, style)
    yh = min(kb[1], yk) - 2.5
    wb = (P14_RANGE[1] - P14_RANGE[0]) * k
    xa, xb = x0, x0 + wa + gap
    xl = xb + wb + 0.5
    xv = xl + wl + gap
    xd = x1 - wd
    wv = xd - gap - xv
    if wv < 50.0 and log is not None:
        log.append(u"WARNING: p.14 views only {:.0f} mm wide (panel {:.0f} mm)".format(wv, x1 - x0))
    heads = [(xa, u"RAIN · WATER", u"mm a month " + cite(YEAR_SRC[0][1]) + u" · m deep"),
             (xb, u"THE CUT S4–S4', SOUTH-WEST TO NORTH-EAST · 1:500",
              u"what the place becomes, who uses it · its plants, a line a month under it"),
             (xv, u"VIEW UPSTREAM FROM THE LOWER WALK", u"the same spot in every season"),
             (xd, u"ANIMALS ON RECORD", u"GBIF " + u"".join(cite(s_) for s_ in P14_FAUNA_SRC))]
    for hx, t1, t2 in heads:
        pg.text(t1, hx, yh - fs, fs, COL["ink_dark"], bold=True)
        pg.text(t2, hx, yh - fs * 2.3, fs, COL["ink2"])
    yt = yh - fs * 2.3 - 2.0
    rh = (yt - y0 - (fs * 1.3 + 2.4 + fs * CAP) - 1.5) / 4.0
    for i, sea in enumerate(SEAS):
        rt = yt - i * rh
        rbot = rt - rh
        pg.line([(x0, rt), (x1, rt)], COL["faint"], 0.25)
        _p14_season_tag(pg, xa, rt - 1.0, wa, rh - 2.0, sea)
        yb = rbot + 5.0
        sp = Page(0, 0)
        X, Y = _p14_cut(sp, xb, yb, k, P14_RANGE, sea, P14_SEA_MONTH[sea], style=style)
        pg.items += sp.items
        _p14_cal_band(pg, X, yb - 0.8, sea, P14_RANGE)
        d = _p14_sea_depth(sea)
        lv = [(Y(G["bed"]), u"{:+.2f} bed".format(G["bed"]), COL["ink"], False)]
        if d >= P14_SHEET_M:
            lv.append((Y(G["bed"] + d), u"{:+.2f} water".format(G["bed"] + d), C["w4"], True))
        else:
            lv.append((Y(G["sfl"]), u"{:+.2f} strip".format(G["sfl"]), C["w4"], True))
        if sea == "winter":
            lv += [(Y(G["q100"]), u"{:+.2f} Q100".format(G["q100"]), C["w4"], True),
                   (Y(G["q500"]), u"{:+.2f} Q500".format(G["q500"]), C["w4"], True)]
        level_ladder(pg, lv, xl, xl + 3.5, fs, None, lo=yb)
        labs = []
        for zone, name in P14_SPACES[sea]:
            a, b = G["zones"][zone]
            sm = (a + b) / 2.0
            zz = _p14_surf(sm)
            if zone in ("bed", "gravel", "strip") and d >= P14_SHEET_M:
                zz = max(zz, G["bed"] + d)
            labs.append((X(sm), Y(zz) + 0.3, [name], P14_SPACE_COL[zone], True))
        sky_labels(pg, labs, sp.items, xb, xb + wb, rt - 1.5, fs)
        _p14_view(pg, (xv, rbot + 1.2, xv + wv, rt - 1.2), sea, style)
        _p14_animals(pg, xd, rt - 1.2, wd, rh - 2.4, sea)
    pg.line([(x0, yt - 4 * rh), (x1, yt - 4 * rh)], COL["faint"], 0.25)
    r28_scale_bar(pg, xb, y0 + fs * 1.3 + 0.4, P14_DEN)
    bb = _p14_bb(pg.items[n0:])
    if log is not None:
        _p14_g6(k, P14_PLANTS, log, u"p.14 cuts")
        log.append(u"p.14 S4 seasons, style {}: cuts 1:{:,.0f}, rows {:.1f} mm, views {:.0f} mm wide, panel {:.0f} x "
                   u"{:.0f} mm; S4 bed {:+.2f}, width {:,.0f} cm (level module); {} plants, people {}".format(
                       style, P14_DEN, rh, wv, bb[2] - bb[0], bb[3] - bb[1], G["bed"], G["width"] * 100.0,
                       len(P14_PLANTS), u", ".join(u"{} {}".format(s_, len(_p14_people(s_))) for s_ in SEAS)))
    return bb


def p14_page(pg, box, opt, log):
    """p.14, the four seasons of S4 (package D), drawn whole into box (x0, y0, x1, y1), page mm, in style b, and its
    style a copy right of the board (D1). Returns its crops [(crop id, bbox, scale denominator)]: the unsuffixed id and
    _b = style b, _a = style a."""
    bb_b = _p14_panel(pg, box, log, "b")
    bb_a = _p14_panel(pg, _p14_ext_box(pg, box, P14_TITLE), log, "a")
    ids = _p14_crop_ids("wb_s4_seasons")
    return [(ids[0], bb_b, P14_DEN), (ids[1], bb_b, P14_DEN), (ids[2], bb_a, P14_DEN)]


# ---------------------------------------------------------------- p.15
P15_KEY = (120.0, 30.0)
P15_GROUPS = [("locals", u"locals", "CC9A52"), ("tourists", u"tourists", "8B3A3F"), ("students", u"students", "5C7A86"),
              ("kermes", u"Kermes visitors", "5E4B8B")]   # the city link's groups (pp.08, 10) + the Kermes
P15_GROUP_COL = dict((g_, c_) for g_, _, c_ in P15_GROUPS)
P15_KERMES = (5 + 28.5 / 30.0, 6 + 5.0 / 31.0)            # 29 Jun-5 Jul in months from 1 Jan (the 90th Kermes, 2026)
P15_USE = [  # who uses the north-east bank, doing what, how much each month Jan-Dec (0 none - 3 busy: our programme,
    # from the season cuts, drawn as that many figures in the month); None = the Kermes week only: (group, pose,
    # keywords, months)
    ("locals", "walk", u"walk the promenade", (2, 2, 2, 2, 3, 3, 3, 3, 3, 2, 2, 2)),
    ("locals", "watch", u"watch the floods", (3, 3, 1, 1, 0, 0, 0, 0, 0, 0, 1, 3)),
    ("locals", "sit", u"sit on the seat steps", (1, 1, 1, 2, 2, 2, 3, 3, 2, 2, 1, 1)),
    ("locals", "child_play", u"children at the water's edge", (0, 0, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0)),
    ("locals", "wade", u"wade in the summer strip", (0, 0, 0, 1, 1, 2, 3, 3, 1, 0, 0, 0)),
    ("locals", "walk", u"walk the open gravel bed", (0, 0, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0)),
    ("tourists", "walk", u"walk the promenade", (0, 0, 1, 1, 2, 2, 2, 2, 2, 1, 0, 0)),
    ("tourists", "wade", u"cool their feet in the strip", (0, 0, 0, 0, 0, 1, 2, 2, 0, 0, 0, 0)),
    ("students", "sit", u"meet on the seat steps", (1, 1, 2, 2, 2, 1, 0, 0, 1, 2, 2, 1)),
    ("kermes", "stall", u"Kermes stalls on the terrace", None),
]
P15_PLANT_ROWS = ("plane", "ash", "willow", "tamarisk", "chaste", "loosestrife", "soft_rush")
P15_SAY = (u"**Winter and spring** give the bed to the stream; **summer and autumn** give it to people: wading, the "
           u"Kermes market, walking the gravel. The seat steps and the raised promenade are used **all year**.")
P15_BAND_SRC = (u"Rijkswaterstaat (2023). Hydrologische randvoorwaarden van de ecotopen in PAGW rivieren, memo, "
                u"pp. 8-16")
P15_LABEL_W = 78.0                   # the chart's label column, mm


def _p15_days(code):
    if code == "A":
        return u"under water all year"
    lo, hi = BAND_DAYS[code]
    if lo <= 0.0:
        return u"under {:g} days a year".format(hi)
    return u"{:g}–{:g} days a year".format(lo, hi)


def _p15_year(pg, x0, ytop, x1, ybot, log=None, style="b"):
    """THE YEAR ON ONE MONTH AXIS (R31's idea: a row of pictograms a user group, everyone's activities on one time
    axis; R03 / R05: intensity read from figures): the seasons as p.14 names them, the water (when the stream covers
    the bed, when the strip runs on stored water, when the gravel bed is open), who and when (one to three figures in
    each month = how busy, the group's tint behind; the Kermes week as a stall), the plants (each month a small drawing
    of the species in that month's state over its leaf and flower bars, plants.py), one short conclusion. Fills x0..x1
    from ytop down to ybot."""
    fs = FS_MIN
    xa = x0 + P15_LABEL_W
    mw = (x1 - xa) / 12.0
    tx = x0 + 24.0

    def X(t):
        return xa + t * mw
    wet = [m for m in range(12) if _p14_depth(m) >= P14_SHEET_M]
    water = [(u"stream covers the bed", "flood", wet, C["w2"]),
             (u"strip runs on stored water", "strip", [m for m in range(12) if m not in wet], "7FAFC0"),
             (u"gravel bed open to people", "hub_open", list(SUBHUB_OPEN), "D9C79A")]
    say_h = 3.2 * 1.28 * 2 + 2.5
    head_h = fs * 2.6 + 1.2
    blk = fs * 1.6
    nrow = len(water) + len(P15_USE) + len(P15_PLANT_ROWS)
    rh = (ytop - ybot - head_h - say_h - 3 * blk) / nrow
    if rh < 3.4 and log is not None:
        log.append(u"WARNING (D9): p.15 THE YEAR has {:.1f} mm a row, under 3.4: the pair needs more room".format(rh))
    rh = max(3.0, min(6.5, rh))
    yend = ytop - head_h - 3 * blk - nrow * rh
    tint = {"winter": "EDF1F2", "spring": "F0F3E8", "summer": "F7F3E5", "autumn": "F4EEE5"}
    for sea in SEAS:
        for m in S4_MONTH_IDX[sea]:
            pg.poly([rect(X(m), yend, X(m + 1), ytop - fs * 1.3)], fill=tint[sea])
        for a_, b_ in occ_spans(list(S4_MONTH_IDX[sea])):
            pg.text(sea, X((a_ + b_) / 2.0), ytop - fs, fs, COL["ink2"], bold=True, align="C")
    for m in range(12):
        pg.text(MONTHS[m], X(m + 0.5), ytop - fs * 2.3, fs, COL["ink_dark"], align="C")
    for m in range(13):
        pg.line([(X(m), ytop - fs * 1.3), (X(m), yend)], COL["white"], 0.35)
    y = [ytop - head_h]

    def title(t):
        pg.text(t, x0, y[0] - fs * 1.15, fs, COL["ink_dark"], bold=True)
        pg.line([(x0, y[0] - blk + 0.2), (x1, y[0] - blk + 0.2)], COL["faint"], 0.15)
        y[0] -= blk

    def label(words):
        pg.text(words, tx + rh + 0.4, y[0] - rh / 2.0 - fs * 0.35, fs, COL["ink"])

    def bar(a_, b_, colour, frac, alpha=None):
        c_ = y[0] - rh / 2.0
        pg.poly([rect(X(a_) + 0.25, c_ - rh * frac / 2.0, X(b_) - 0.25, c_ + rh * frac / 2.0)], fill=colour,
                alpha=alpha)
    title(u"WATER")
    for words, ic, ms, colour in water:
        icon(pg, ic, tx, y[0] - 0.3, rh - 0.6)
        label(words)
        for a_, b_ in occ_spans(ms):
            bar(a_, b_, colour, 0.55)
        y[0] -= rh
    title(u"WHO, AND WHEN · one figure = a few people, three = busy")
    names = dict((g_, n_) for g_, n_, _ in P15_GROUPS)
    kf = (rh - 0.9) / FIG_ADULT_H                                 # figures in the months, true proportions
    last = None
    for g_, pose, words, vals in P15_USE:
        col = P15_GROUP_COL[g_]
        if g_ != last:
            pg.text(names[g_], x0, y[0] - rh / 2.0 - fs * 0.35, fs, col, bold=True)
            last = g_
        pg.poly([rect(tx, y[0] - rh + 0.3, tx + rh - 0.6, y[0] - 0.3)], fill=col)
        yf = y[0] - rh + 0.45
        if pose == "stall":
            shp_put(pg, fig_stall(tx + (rh - 0.6) / 2.0 + 0.4, y[0] - rh + 0.6, (rh - 1.4) / FIG_STALL["canopy_top"],
                                  vendor=False, buyer=False, ink=COL["white"], fill=col, canopy=COL["white"]))
        else:
            shp_put(pg, fig_side(pose, tx + (rh - 0.6) / 2.0, y[0] - rh + 0.6, (rh - 1.4) / FIG_ADULT_H,
                                 ink=COL["white"], pen_min_mm=0.0))
        label(words)
        if vals is None:
            bar(P15_KERMES[0], P15_KERMES[1], col, 0.9, 0.25)
            shp_put(pg, fig_stall((X(P15_KERMES[0]) + X(P15_KERMES[1])) / 2.0 + 0.5, yf, kf, vendor=True, buyer=False,
                                  ink=col, canopy=P14_STALL_CANOPY, style=style))
            pg.text(u"29 Jun–5 Jul", X(P15_KERMES[1]) + 0.8, y[0] - rh / 2.0 - fs * 0.35, fs, col, bold=True)
        else:
            for m in range(12):
                v = vals[m]
                if v <= 0:
                    continue
                bar(m, m + 1, col, 0.92, 0.12 + 0.06 * v)
                for j in range(v):
                    xx = X(m + 0.5) + (j - (v - 1) / 2.0) * max(1.4, 0.75 * FIG_ADULT_H * kf)
                    q = {"depth_m": 0.30} if pose == "wade" else {}
                    shp_put(pg, fig_side(pose, xx, yf, kf, facing=1 if (m + j) % 2 else -1, ink=col, style=style,
                                         pick=m * 3 + j, **q))
        y[0] -= rh
    pg.text(u"PLANTS", x0, y[0] - fs * 1.15, fs, COL["ink_dark"], bold=True)
    xx = x0 + text_w(u"PLANTS", fs, True) + 3.0
    for st, word in (("leaf", u"in leaf"), ("bloom", u"in flower"), ("cut", u"heads cut")):
        _p14_cell(pg, xx, y[0] - fs * 1.15 - 0.2, xx + 3.2, y[0] - fs * 1.15 + fs * 0.75, st)
        pg.text(word, xx + 4.0, y[0] - fs * 1.15, fs, COL["ink"])
        xx += 4.0 + text_w(word, fs) + 3.0
    pg.text(u"each month: the plant as it is then", xx + 2.0, y[0] - fs * 1.15, fs, COL["ink2"])
    pg.line([(x0, y[0] - blk + 0.2), (x1, y[0] - blk + 0.2)], COL["faint"], 0.15)
    y[0] -= blk
    for key in P15_PLANT_ROWS:
        sp_ = PLA_SPECIES[key]
        h, cw = _p14_size(key)
        kk = (rh - 0.8) / max(h, cw)
        shp_put(pg, _p14_plant(key, tx + (rh - 0.6) / 2.0, y[0] - rh + 0.4, kk, 5, h, cw, 0, style))
        label(sp_["name"])
        mo = pla_months(key)
        for a_, b_ in occ_spans([m - 1 for m in mo["leaf"]]):
            bar(a_, b_, sp_["colours"].get("fill") or P14_LEAF, 0.3, 0.45)
        for a_, b_ in occ_spans([m - 1 for m in mo["bloom"] if m not in mo["cut"]]):
            bar(a_, b_, P14_BLOOM, 0.62, 0.45)
        for m in mo["cut"]:
            c_ = y[0] - rh / 2.0
            _p14_cell(pg, X(m - 1) + 0.25, c_ - rh * 0.31, X(m) - 0.25, c_ + rh * 0.31, "cut")
        km = (rh - 0.9) / max(h, cw)
        for m in range(12):
            if _p14_state(key, m + 1):
                shp_put(pg, _p14_plant(key, X(m + 0.5), y[0] - rh + 0.45, km, m + 1, h, cw, m, style))
        y[0] -= rh
    r28_para(pg, x0, y[0] - 1.5, x1 - x0, P15_SAY, 3.2, COL["ink_dark"])


P15_WHY = [  # the north-east bank's parts and why each is there (G10; our design), numbered on the cut (R19):
    # (zone of _p14_geo, words; {open} = the months the gravel bed is open, from SUBHUB_OPEN)
    ("strip", u"summer strip: holds stored water, wading when the stream is low"),
    ("gravel", u"gravel bed: the stream's, open to walk {open}"),
    ("market", u"flood terrace: the Kermes market ground, under water only in a flood"),
    ("walk", u"lower walk: floodable, closed in a flood"),
    ("steps", u"seat steps: sit and watch the water; a flood rises up them"),
    ("prom", u"promenade: over Q500, dry in every flood"),
    ("bike", u"bike lane: over Q500, apart from the walkers"),
]


def _p15_open():
    """the months the gravel bed is open (SUBHUB_OPEN) as "Jun-Oct", or the months listed"""
    ms = sorted(SUBHUB_OPEN)
    if not ms:
        return u""
    if ms == list(range(ms[0], ms[-1] + 1)):
        return u"{}–{}".format(MONTHS[ms[0]], MONTHS[ms[-1]]) if len(ms) > 1 else MONTHS[ms[0]]
    return u", ".join(MONTHS[m] for m in ms)


def _p15_panel(pg, box, log, style):
    """p.15 in one style, drawn whole into box: the context line, the S4 key map at the top right, the bank at 1:250
    in summer with the trees beyond (R16), the stream at the registry's average flow with Q100 / Q500 (M5), the
    planting (plants named with what they do, sourced purposes), the summer's people and Kermes stalls at true size,
    today's bank dashed, the parts numbered with their reason (R19, G10), its widths in cm and planting bands under it,
    the levels and the bands' days under water at its right (the p.20 ladder, D9 a), the scale bar flush left under
    it, then the year on one month axis. Returns its bbox."""
    x0, y0, x1, y1 = box
    n0 = len(pg.items)
    fs = FS_MIN
    G = _p14_geo()
    k = 1000.0 / P15_DEN
    s0, s1 = P15_RANGE
    ws = (s1 - s0) * k
    kb = _p14_keymap(pg, (x1 - P15_KEY[0], y1 - P15_KEY[1], x1, y1), log)
    cb = context(pg, x0, y1, min(ws, kb[0] - x0 - 6.0), "ne")
    ztop = max(_p14_surf(s) + h for _, s, h, _ in P14_PLANTS if s0 <= s <= s1)
    yb = cb[1] - 10.0 - (ztop - G["base"]) * k
    sp = Page(0, 0)
    X, Y = _p14_cut(sp, x0, yb, k, P15_RANGE, "summer", P14_SEA_MONTH["summer"], style=style, water="avg")
    pg.items += sp.items
    pg.line([(X(s), Y(z)) for s, z in G["today"] if s <= s1], COL["ink2"], 0.2, dash=[1.0, 0.6])
    labs, done = [], set()
    for key, s, h, cw in P14_PLANTS:
        if s0 + 0.5 <= s <= s1 and key not in done:
            done.add(key)
            what = pla_purpose(key, sure_only=True)
            t = PLA_SPECIES[key]["name"] + (u", heads cut in Sep" if key == "loosestrife" else u"") + \
                (u" · " + u", ".join(what) if what else u"")
            labs.append((X(s), Y(_p14_surf(s) + h * 0.75), [t], COL["ink_dark"], False))
    st_ = [s for pose, s, _f, _sd in _p14_people("summer") if pose == "market" and s0 + 1.0 <= s <= s1 - 1.0]
    if st_:
        labs.append((X(st_[0]), Y(_p14_surf(st_[0]) + FIG_STALL["canopy_top"]),
                     [u"Kermes stall · counter {:,.0f} cm".format(FIG_STALL["counter_h"] * 100.0)],
                     P15_GROUP_COL["kermes"], True))
    sky_labels(pg, labs, sp.items, x0, x0 + ws, cb[1] - 1.0, fs)
    # the parts, numbered with their reason (R19, G10)
    co = SfCallouts()
    for zone, words in P15_WHY:
        a, b = max(G["zones"][zone][0], s0), min(G["zones"][zone][1], s1)
        if b - a >= 1.4:
            sm = (a + b) / 2.0
            co.add(X(sm), Y(_p14_surf(sm)) - 2.4, words.format(open=_p15_open()))
    shp_put(pg, co.marks(fs * 1.1))
    # widths, cm, with the parts' names
    zn = G["zones"]
    dims = [(zn["strip"], u"strip"), ((zn["strip"][1], G["b1"]), u""), (zn["toe"], u"bank"),
            ((zn["terrace"][0], P14_WALK[0]), u"flood terrace"), (zn["walk"], u"lower walk"),
            ((P14_WALK[1], zn["terrace"][1]), u""), (zn["steps"], u"seat steps"), (zn["prom"], u"promenade"),
            (zn["bike"], u"bike lane"), (zn["fill"], u"fill")]
    yd = yb - 3.2
    xs_ = [X(a) for (a, b), _ in dims] + [X(dims[-1][0][1])]
    pg.line([(xs_[0], yd), (xs_[-1], yd)], C["acc"], 0.15)
    for x_ in xs_:
        pg.line([(x_ - 0.6, yd - 0.6), (x_ + 0.6, yd + 0.6)], C["acc"], 0.2)
    for (a, b), name in dims:
        w_ = X(b) - X(a)
        t = u"{:,.0f}".format(round((b - a) * 100.0))
        if text_w(t, fs) < w_ - 0.8:
            pg.text(t, (X(a) + X(b)) / 2.0, yd + 0.7, fs, C["acc"], align="C")
        if name and text_w(name, fs) < w_ + 2.0:
            pg.text(name, (X(a) + X(b)) / 2.0, yd - fs * 1.15, fs, COL["ink"], align="C")
    pg.text(u"cm", xs_[-1] + 1.2, yd - fs * 0.35, fs, C["acc"])
    # the planting bands along the cut (where water reaches the ground how often)
    yt_b, hb = yd - fs * 1.15 - 1.6, 3.0
    runs, s, step = [], s0, 0.1
    while s < s1 - 1e-9:
        c_ = _p14_band_code(s + step / 2.0, _p14_surf(s + step / 2.0))
        if runs and runs[-1][0] == c_:
            runs[-1][2] = s + step
        else:
            runs.append([c_, s, s + step])
        s += step
    for c_, a, b in runs:
        pg.poly([rect(X(a), yt_b - hb, X(min(b, s1)), yt_b)], fill=BAND_COL[c_])
        if X(b) - X(a) > 3.0:
            pg.text(c_, (X(a) + X(b)) / 2.0, yt_b - hb + 0.55, fs, COL["ink_dark"], bold=True, align="C")
    bar = r28_scale_bar(pg, x0, yt_b - hb - 1.6 - (2.0 + fs * CAP + 0.2), P15_DEN)
    # at the right: the levels, and the bands with their days under water (the p.20 ladder, D9 a)
    xr = x0 + ws + 4.0
    avg = level_avg_flow("S4")
    bands = [("A", G["sfl"], G["bed"]), ("B", G["bed"], G["bed"] + G["dmax"]),
             ("C", G["bed"] + G["dmax"], G["shelf"]), ("D", G["shelf"], G["q100"]), ("E", G["q100"], G["q500"]),
             ("F", G["q500"], P14_PROM)]
    for c_, lo, hi in bands:
        pg.poly([rect(xr, Y(lo), xr + 3.0, Y(hi))], fill=BAND_COL[c_], stroke=COL["white"], lw=0.1)
    levels = sorted([(G["sfl"], u"strip floor"), (G["bed"], u"bed"), (avg, u"average flow"),
                     (G["shelf"], u"flood terrace"), (G["ne_top"], u"bank today"), (G["q100"], u"Q100"),
                     (G["q500"], u"Q500"), (P14_PROM, u"promenade")])
    ys = spread([Y(z) - fs * 0.35 for z, _ in levels], fs * 1.25)
    for (z, name), yl in zip(levels, ys):
        pg.line([(xr - 1.0, Y(z)), (xr + 4.0, Y(z)), (xr + 5.5, yl + fs * 0.35), (xr + 6.2, yl + fs * 0.35)],
                COL["ink2"], 0.1)
        pg.text(u"{:+.2f} {}".format(z, name), xr + 6.6, yl, fs,
                C["w4"] if name[0] == u"Q" or name.startswith(u"average") else COL["ink"])
    xc2 = xr + 6.6 + max(text_w(u"{:+.2f} {}".format(z, n_), fs) for z, n_ in levels) + 4.0
    bn = dict((b_[0], b_[1]) for b_ in PLANT_BANDS)
    bn["A"] = u"summer strip"
    ys2 = spread([(Y(lo) + Y(hi)) / 2.0 - fs * 0.35 for _, lo, hi in bands], fs * 1.3)
    for (c_, lo, hi), yl in zip(bands, ys2):
        pg.poly([rect(xc2, yl - 0.4, xc2 + 3.2, yl + fs * 0.85)], fill=BAND_COL[c_])
        pg.text(c_, xc2 + 1.6, yl, fs, COL["ink_dark"], bold=True, align="C")
        pg.text(u"{} · {}".format(bn[c_], _p15_days(c_)), xc2 + 4.2, yl, fs, COL["ink"])
    yl_t = max(ys[-1], ys2[-1]) + fs * 2.2
    pg.text(u"LEVELS · PLANTING BANDS, days under water " + cite(P15_BAND_SRC), xr, yl_t, fs, COL["ink_dark"],
            bold=True)
    # the numbered parts' key above the ladder, clear of the key map
    nk = len(set(n for n, _x, _y, _t in co.items))
    gap = fs * 1.5
    ky = yl_t + 3.0 + fs * 1.3 + nk * gap
    pg.text(u"THE BANK, PART BY PART · why each is there", xr, ky, fs, COL["ink_dark"], bold=True)
    shp_put(pg, co.key(xr, ky - fs * 0.6, fs, gap=gap))
    if ky + fs > kb[1] - 1.0 and log is not None:
        log.append(u"WARNING: p.15 the parts' key reaches the key map ({:.1f} mm)".format(ky + fs - kb[1] + 1.0))
    _p15_year(pg, x0, bar[1] - 3.0, x1, y0, log, style)
    bb = _p14_bb(pg.items[n0:])
    if log is not None:
        _p14_g6(k, [p for p in P14_PLANTS if s0 <= p[1] <= s1], log, u"p.15 cut")
        log.append(u"p.15 S4 north-east bank 1:{:,.0f} and the year, style {}: panel {:.0f} x {:.0f} mm{}".format(
            P15_DEN, style, bb[2] - bb[0], bb[3] - bb[1], u"" if bb[1] >= y0 - 0.5 else
            u" (WARNING D9: {:.1f} mm below the cell: the pair does not fit two pages)".format(y0 - bb[1])))
    return bb


def p15_page(pg, box, opt, log):
    """p.15, the north-east bank of S4 (package D), drawn whole into box (x0, y0, x1, y1), page mm, in style b, and
    its style a copy right of the board (D1). Returns its crops: the unsuffixed id and _b = style b, _a = style a."""
    bb_b = _p15_panel(pg, box, log, "b")
    bb_a = _p15_panel(pg, _p14_ext_box(pg, box, P15_TITLE), log, "a")
    if log is not None:
        for ln in (cut_log_line(),) + tuple(PLA_LOG):
            if ln and ln not in log:
                log.append(ln)
    ids = _p14_crop_ids("wb_s4_ne")
    return [(ids[0], bb_b, P15_DEN), (ids[1], bb_b, P15_DEN), (ids[2], bb_a, P15_DEN)]
