# p.14-15 the S4 pair (v5, revision 29 Oct 2026, T3b WO-T3b-4, package D; split from code.py and
# parts/r28_occupancy.py on 29 Oct 2026, rebuilt). ONE S4 for both pages: the existing levels from the level module
# (N1 a, round 3: survey datum, bed +43.59 = the low point of the surveyed profile; bank tops, the two level shelves,
# Q100, Q500) and the surveyed ground (s4_profile) with our proposal on them; planting by the
# rule (D6: purple loosestrife + soft rush, no iris; D2: no reed in the open bed), each plant from plants.py in that
# month's state; the p.20 planting bands with their days under water folded into p.15 (D9 a).
#   p.14 (p14_page): four rows, a season each: rain and water as a small graphic, the cut at 1:500 with its plants in
#        the season's state, its zones numbered and what they become named under it (round 3), one
#        rectangular view from the same viewpoint in every season, the animals on record that season (a list).
#   p.15 (p15_page): the north-east bank at 1:250 with widths, levels and planting bands (days under water), and the
#        year on one month axis (R31: a row of pictograms per user group, bars on one time axis; plants in leaf and
#        flower).
# Revision 30 Oct 2026 (T6, booklet p13 + p14): planting from plants.py's mixed scatter by zone (G9), true-size
# people and stalls from figures.py by the season's programme (G10, P14_USE), trees beyond the cut (R16), p.15's water
# at the registry's average flow (M5), numbered zone reasons (R19), the year read through figures a month (R03, R05);
# every panel drawn twice (D1): style b (vector) in its cell, style a (cutouts) in a copy right of the board.
# Round 2 (31 Oct 2026, R2-C; booklet p13 + p14): planting as mixed groups (pla_group_section, P14_PLANT_RUNS, G9),
# people by zone through fig_place_zones (G10; depth layers 0 / 1, one cutout style, nobody in water over knee), every
# item seated (G14), the D8 designed sky, no hatch triangles; p13's views denser and render-like (layered planting,
# aerial veil, the season's activity repeated up the stream); p14's cut clipped to its frame so no crown reaches the
# levels and the lists beside it (G3), its planting labelled by group with what each does.
# Round 3 (31 Oct 2026, B2; booklet p13 + p14): the bed is the surveyed profile, filled, the water fills it only below
# each level (level_season_depth, N2 a: the summer strip full of clean water + the natural level printed), Q100/Q500
# on every cut; plants seasonal and opaque through plants.py (pla_section month=, bare winter trees, species colours,
# the new willow), the cut's trees a depth layer back (G15); people in front in one drawn style with street elements;
# zones numbered under each cut with their reasons (R07, G10); zoom insets at 1:200 (U29); no leader labels (G3).
# Round 4 (1 Nov 2026, S6a; handover/S6a_p14_design_spec.md): every text in the page's TextPage (G-R4-1, a collision
# raises; word blocks grouped, key maps and markers kept clear); p.14: plant key English · Turkish (D5), the zones
# as a numbered colour strip under each cut (P14.1, mk_marker), the shared key map (km_map, red R01) and north arrow,
# level marks outside each cut's frame (sf_level_marks), the low planting layer (pla_low_section), plants in the
# season's state (plants.py season=), greenery colours from pla_colours (G-R4-6), the one people set (pen_black),
# the views' trees whole inside their frames (P14.2), insets with their scale (1:200); p.15: one LEFT section block
# (blk_section), its parts numbered on the surface, its level marks outside the frame, the inset at 1:100 (D11), one
# subtitle (P15.5), the year's PLANTS rows clear of each other (P15.3).
# Round 5 (S8, 2 Nov 2026; G-R5-12): the board only RECORDS; every drawing goes to the booklet as its own item
# (parts/wb_items.py). The code's p14 = booklet p15 "Four seasons on one cut" (WBX_PG_SEASONS, old crop
# wb_s4_seasons), p15 = booklet p16 "The S4 cut, north-east bank" (WBX_PG_NE, old crop wb_s4_ne). p15: each row's
# rain diagram, cut (1:500, x = m across S4 from the bed's low point, y = m a.s.l.), inset and view are drawings of
# their own; the plant, zone and animal keys are booklet legends (wbx_legend), the level markers booklet levels
# (wbx_levels, U04), the key map km_map v2 handed over whole (wbx_keymap, G-R5-3); insets v2 (sf_inset_frame: their
# own drawing at their own k, framed on the action, cut check); trees lead (sf_tree_level), people stand on the higher
# ground at their feet (sf_seat_feet), fishing / wading gated (sf_activity_ok, PLAN §8); the season's scenario per
# PLAN §8 (spring waders, summer shade seating, autumn loosestrife heads cut + walkers, winter few walkers). p16: the
# width row is gone (G-R5-4.6), its lists and band key are booklet lists / legends, the year chart its own diagram.
# v16 (round 6, S5, 4 Nov 2026): booklet p13 "Four seasons on one cut" moved to pages/p13_seasons.py (r06_S03, the
# 28 Oct four seasons restored on this file's ACCURATE cut, P-11); the old p14 panel (p14_page, _p14_panel, rain bars,
# zone strips and keys, the upstream views, the 1:200 insets) is deleted; this file keeps the shared S4 cut (_p14_geo,
# _p14_cut: G6-9 groups, qlines), the S4 key map on keymap.py v3 (_p14_keymap -> km_keymap), the zones on the hue
# table, the inset v2 with the dist v15.2 window shift ported, and booklet p14 (p15_page) in ACCURATE language
# (section log, ▽ spread check, bands A-F on the hue table, key map km_keymap; year chart as is).
# build_board calls P14_TITLE, P15_TITLE, p13_page(pg, box, opt, log) (p13_seasons.py), p15_page(pg, box, opt, log).

P14_TITLE = u"S4 THROUGH THE SEASONS · the water level decides what the place becomes"
P15_TITLE = u"S4 NORTH-EAST BANK · the terraces stay, their use follows the months"

# ---------------------------------------------------------------- the cut: levels from the level module, our proposal
# m across S4 from the bed's low point (north-east +, as the level table's shelves), levels m a.s.l. Round 3 (N1 a):
# the ground is the surveyed profile (s4_profile) up to where it rises through the north-east shelf level (t0); the
# proposal: a lined summer strip cut into the bed, the north-east shelf from t0 as a gravel flood terrace graded at the
# shelf level with a floodable lower walk, seat steps up to a raised promenade over Q500, its earth fill down to the
# surveyed ground (the street).
P14_BED_BAND = 0.50                  # the bed floor: surveyed ground within this of the bed, m (LEVELS bed_width rule)
P14_COVER = 0.5                      # "the stream covers the bed": the month's level wets this share of the bed floor
#                                      (drawing rule)
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
P14_ZOOM_DEN = 200.0                 # the zoom insets (U29, G15): an allowed booklet scale
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
    ("terr_b", 0.36, 0.38, ("tamarisk", "chaste"), 1.2, 17),
    ("terr_c", 0.38, 0.46, ("tamarisk", "chaste", "ash"), 1.2, 18),
    ("prom", 0.52, 0.52, ("plane", "ash"), 0.8, 19),
    ("fill", 0.60, 0.70, ("ash", "plane", "tamarisk", "chaste"), 1.1, 20),
]
P14_PLANT_RUNS = [("sw_path", "sw_slope", "bed_sw"), ("toe", "terr_b", "terr_c"), ("prom", "fill")]   # G9:
#                                      the zones planted as one stretch of mixed groups (the open ground between them:
#                                      the market ground, the lower walk, the bike lane, kept free)
P14_LOW_ZONES = ("sw_slope", "toe", "terr_b", "terr_c", "fill")   # round 4 (G-R4-5.3): the zones whose ground gets
#                                      plants.py's low layer (pla_low_section) under the groups: only their own low
#                                      species of P14_PLANT_ZONES (no species added)
P14_LOW_DENS = 0.9                   # its density, x the zone's own (drawing rule)
P14_PLANTS = []                      # (species, m across, height m, crown m), filled once a run by _p14_planting (p.17
#                                      reads it for F3 after _p14_geo())
P14_GROUPS = []                      # the mixed groups (m from, m to, species, purpose tags), filled with P14_PLANTS
P14_USE = {  # who is where, doing what, each season (G10; our programme, as the rows of P15_USE; Aras 31 Oct: summer on
    # the wading strip and the market ground, autumn on the sun steps, winter few people on the high walk, spring
    # walkers and children): (zone of _p14_geo, FIG_ACTIVITY zone kind, density, seed, D9 layer: 0 at the cut, 1 just
    # beyond it, smaller and paler, focus, cast, at most); figures.py's fig_place_zones places the people (walkable
    # zones only, nobody where the season's water is deeper than knee, poses that fit the zone, irregular gaps).
    # R2-C scenes (Aras 31 Oct 12:01 "they look like they are just put in there"): focus "water" = people who stay
    # look at the season's water, children play in pairs turned to each other; "stall" = on the market ground everyone
    # turns to the nearest stall, each stall to its nearest buyer (its vendor behind the counter: fig_stall); cast =
    # the poses of that zone's people in turn (a small story; markets, groups and bikes stay as placed)
    # Round 3 (G15, P13.2): each season's own scenario, zone by zone, with the new poses (running, dog walk, fishing,
    # lying) and one drawn people style (PLAN §2: fig_side's pen language; cutouts would mix two styles).
    "winter": [("sw_path", "walkway", 0.3, 1, 0, None, ("walk", "dog_walk"), None),   # few people: the high water is
               ("prom_edge", "viewing_terrace", 0.8, 2, 0, "water", ("watch", "stand", "watch"), 3),   # watched from
               ("prom_in", "walkway", 0.4, 32, 0, None, ("dog_walk", "running", "walk"), 3),   # the promenade's edge
               ("steps", "sun_steps", 0.3, 34, 0, "water", ("watch", "sit_step"), 2),
               ("bike", "bike_lane", 0.4, 3, 0, None, None, None)],
    "spring": [("sw_path", "walkway", 0.6, 5, 0, None, ("walk", "dog_walk"), None),
               ("wedge", "water_edge", 0.8, 35, 0, "water", ("fishing", "watch"), 2),   # a fisher at the spring water
               ("wade_s", "wading_strip", 0.9, 37, 0, "water", ("wade", "wade", "touch_water"), 3),   # round 5 (PLAN
               #                                       §8: spring walkers + wading): waders at the spring stream's
               #                                       shallow north-east margin, knee deep at most (fig_place_zones)
               ("walk", "walkway", 0.8, 7, 0, "water", ("adult_child", "walk"), None),   # walkers on the lower walk
               ("steps", "sun_steps", 0.7, 8, 0, "water", ("sit_step", "adult_child", "sit_step"), None),   # families
               ("prom", "walkway", 0.8, 9, 0, "water", ("walk", "running", "adult_child"), None),
               ("bike", "bike_lane", 0.6, 10, 0, None, None, None),
               ("walk", "walkway", 0.5, 25, 1, "water", ("watch", "watch", "adult_child"), 2),   # looking at the wet
               ("prom", "walkway", 0.5, 26, 1, None, None, None)],   # meadow (round 4, PLAN §5: zone 6 is walked
               #                                       around in spring, nobody on it)
    "summer": [("sw_path", "walkway", 0.8, 11, 0, None, ("walk", "dog_walk", "walk"), None),
               ("edge", "walkway", 1.5, 33, 0, "water", ("adult_child", "watch", "adult_child"), 3),   # a family at
               ("strip", "wading_strip", 1.4, 12, 0, "water", ("child_play", "child_play", "wade", "touch_water"),
                None),                                                   # the strip's edge, children playing in pairs
               ("open_w", "lawn", 0.7, 13, 0, "water", ("lying", "child_play", "walk"), 3),   # sunbathing on the gravel
               ("market", "market_ground", 1.2, 14, 0, "stall", None, None),   # buyers at the Kermes stalls
               ("walk", "walkway", 1.0, 15, 0, "water", None, None),
               ("steps", "sun_steps", 1.0, 16, 0, "water", None, None),
               ("prom", "walkway", 1.0, 17, 0, "water", ("walk", "dog_walk", "walk"), None),
               ("bike", "bike_lane", 1.0, 18, 0, None, None, None),
               ("market", "walkway", 0.7, 27, 1, "stall", None, None),
               ("open", "walkway", 0.5, 28, 1, "water", None, None),
               ("prom", "walkway", 0.6, 29, 1, "water", None, None)],
    "autumn": [("sw_path", "walkway", 0.6, 19, 0, None, ("walk", "running"), None),
               ("open_w", "walkway", 1.0, 20, 0, "water", ("walk", "adult_child"), None),   # walking the open bed
               ("edge", "water_edge", 0.6, 36, 0, "water", ("fishing", "watch"), 2),         # fishing at the low water
               ("toe", "water_edge", 0.5, 39, 0, "water", ("touch", "touch", "watch"), 2),   # round 5 (PLAN §8 autumn
               #                                       harvest): the loosestrife flower heads cut at the riparian edge
               #                                       (plants.py pla_months: cut month 9; pose "touch" = reaching down)
               ("strip", "wading_strip", 0.4, 21, 0, "water", ("touch_water", "wade"), None),
               ("steps", "sun_steps", 1.6, 22, 0, "water", ("sit_step", "sit_step", "sit_step", "stand"),
                None),                                                   # friends on the sun steps, facing the water
               ("prom", "walkway", 0.8, 23, 0, "water", ("walk", "running", "dog_walk"), None),
               ("bike", "bike_lane", 0.7, 24, 0, None, None, None),
               ("steps", "sun_steps", 0.9, 30, 1, "water", None, None),
               ("open", "walkway", 0.5, 31, 1, "water", None, None)],
}
P14_WADE_S = (2.5, 0.2)              # m inside the spring water's north-east edge (wl_s): the waders' margin, from, to
#                                      (drawing rule; fig_place_zones keeps them where it is at most knee deep)
P14_FISH_REACH = 4.0                 # m: the farthest water a fisher's line reaches ahead (figures.py's dry-bank guard)
P14_STALL_CANOPY = "CDBFDB"          # the Kermes stalls' canopy: the Kermes visitors' purple, light
_P14_GEO = []
_P14_PEOPLE = {}
_P14_TREES = {}                      # v16 (G6-10): trees drawn on each page's cuts this run (designed species)


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


def _p14_profile(log=None):
    """the surveyed S4 ground (N1 a, DATA-1): code.py's s4_profile (the open file's re-cut, else DETAIL_SRC's embedded
    survey profile, every PROFILE_DS m along S4_A -> S4_B, north-east to larger s). Returns (z, ds, (s_low, z_low)):
    z(s) the ground level at s m across from the profile's low point (north-east +), its step, the low point"""
    s0, ds, Z = s4_profile(detail_engine(), log)
    s0, ds, Z = float(s0), float(ds), [float(z_) for z_ in Z]
    i = min(range(len(Z)), key=lambda j_: Z[j_])
    sl = s0 + i * ds

    def z(s):
        u = (sl + s - s0) / ds
        if u <= 0.0:
            return Z[0]
        if u >= len(Z) - 1:
            return Z[-1]
        j_ = int(u)
        t = u - j_
        return Z[j_] * (1.0 - t) + Z[j_ + 1] * t
    return z, ds, (sl, Z[i])


def _p14_cross(zf, z, side, ds, lim):
    """m across where the surveyed ground zf, going out from the low point to side (+1 north-east, -1 south-west),
    first rises to the level z; side * lim if it never does"""
    s = 0.0
    while abs(s) < lim:
        s2 = s + side * ds
        za, zb = zf(s), zf(s2)
        if zb >= z:
            t = (z - za) / (zb - za) if zb > za + 1e-9 else 1.0
            return s + side * ds * min(1.0, max(0.0, t))
        s = s2
    return side * lim


def _p14_geo(log=None):
    """The S4 cut, once a run (round 3, N1 a: the survey datum): the levels (bed = the level module's +43.59, the
    surveyed low point; q100, q500, ne_top, sw_top, shelf, sfl = strip floor, base; levels = each season's water and
    the average flow), the profile "prof" [(s, z)] street to street (the surveyed ground up to t0, where it rises
    through the north-east shelf level, the strip cut into it; then our terrace, walk, seat steps, promenade, bike lane
    and fill down to the surveyed street), its segments "segs" [((s, z), (s, z), surface)], the surveyed north-east bank
    "today", the zones {name: (s0, s1)}, the step rise; "src" = the levels' log line. The interface p.17 reads:
    handover/B2_work/p14_geo_interface.md."""
    if _P14_GEO:
        return _P14_GEO[0]
    if P14_PROM is None:
        raise RuntimeError(u"S4: 'q500' is missing in the level module (common/data/LEVELS.py): no promenade level")
    bed, q100, q500 = _p14_lv("bed"), _p14_lv("q100"), _p14_lv("q500")
    ne_top, sw_top = _p14_lv("top", "NE"), _p14_lv("top", "SW")
    _ne0, ne1, shelf = _p14_terrace("NE")
    sw0, sw1, _sw_z = _p14_terrace("SW")
    zf, ds, low = _p14_profile(log)
    r0, r1 = P14_RANGE
    lim = max(-r0, r1)
    b0 = _p14_cross(zf, bed + P14_BED_BAND, -1, ds, lim)
    b1 = _p14_cross(zf, bed + P14_BED_BAND, 1, ds, lim)
    t0 = _p14_cross(zf, shelf, 1, ds, lim)
    st0, st1 = P14_STRIP
    sfl = bed - STRIP_DEPTH
    lv = dict((sea, round(bed + level_season_depth("S4", [m + 1 for m in S4_MONTH_IDX[sea]]), 2)) for sea in SEAS)
    lv["avg"] = level_avg_flow("S4")
    wl_w = _p14_cross(zf, lv["winter"], 1, ds, lim)
    wl_s = _p14_cross(zf, lv["spring"], 1, ds, lim)
    n, tread = P14_STEPS
    rise = (P14_PROM - shelf) / n
    p0 = ne1 + (n - 1) * tread
    p1 = p0 + P14_PROM_W[0]
    p2 = p1 + P14_PROM_W[1]
    p3, s = None, p2                                  # the fill, down at P14_FILL_RUN until it meets the street
    while s < r1 - 1e-9:
        s = min(r1, s + ds / 2.0)
        if P14_PROM - (s - p2) / P14_FILL_RUN <= zf(s):
            p3 = s
            break
    if p3 is None:
        p3 = r1
    zp3 = max(zf(p3), P14_PROM - (p3 - p2) / P14_FILL_RUN)
    grid = [j_ * ds for j_ in range(int(math.ceil(r0 / ds)), int(math.floor(r1 / ds)) + 1)]
    pts, segs = [], []

    def add(s_, z_, tag=None):
        if pts and tag:
            segs.append((pts[-1], (s_, z_), tag))
        pts.append((s_, z_))

    def sw_tag(s_):
        sm = (pts[-1][0] + s_) / 2.0
        if sm < -sw1:
            return "road"
        if sm < -sw0 - 0.6:
            return "path"
        if sm < -sw0:
            return "crest"
        return "slope_sw" if sm < b0 else "gravel"
    add(r0, zf(r0))
    for s_ in grid:
        if r0 + 1e-9 < s_ < st0 - 1e-9:
            add(s_, zf(s_), sw_tag(s_))
    add(st0, zf(st0), sw_tag(st0))
    add(st0, sfl, "strip_side")
    add(st1, sfl, "strip")
    add(st1, zf(st1), "strip_side")
    for s_ in grid:
        if st1 + 1e-9 < s_ < t0 - 1e-9:
            add(s_, zf(s_), "gravel" if (pts[-1][0] + s_) / 2.0 < b1 else "slope_ne")
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
    add(p3, zp3, "fill")
    if p3 < r1 - 1e-9:
        for s_ in grid:
            if p3 + 1e-9 < s_ < r1 - 1e-9:
                add(s_, zf(s_), "street")
        add(r1, zf(r1), "street")
    ss = [p[0] for p in pts]
    if any(b < a - 1e-9 for a, b in zip(ss[:-1], ss[1:])):
        raise RuntimeError(u"S4: the levels give a cut that runs backwards ({}); check P14_* against levels.py".format(
            u", ".join(u"{:.2f}".format(s_) for s_ in ss)))
    toe = (min(wl_w + 0.5, b1 - 0.5), b1)
    wedge = (wl_s + 0.2, max(wl_s + 1.5, min(wl_s + 2.5, toe[0])))
    width = b1 - b0
    tw = level("S4", "bed_width_cm")
    src = (u"S4 levels: datum survey (bed {:+.2f}, the surveyed low point at {:.2f} m along S4_A-S4_B, profile {:+.2f}; "
           u"average flow {:+.2f}, Q100 {:+.2f}, Q500 {:+.2f}; season water winter {:+.2f}, spring {:+.2f}, summer {:+.2f}, "
           u"autumn {:+.2f} (level_season_depth); strip floor {:+.2f}, strip full {:+.2f}; bed floor {:,.0f} cm wide "
           u"(table {})){}").format(bed, low[0], low[1], lv["avg"], q100, q500, lv["winter"], lv["spring"],
                                    lv["summer"], lv["autumn"], sfl, sfl + STRIP_DEPTH, width * 100.0,
                                    u"{:,.0f} cm".format(tw) if tw is not None else u"none",
                                    u"; FLAG S4 profile low point {:+.2f} is not the level module's bed {:+.2f}".format(
                                        low[1], bed) if abs(low[1] - bed) > 0.02 else u"")
    G = dict(bed=bed, q100=q100, q500=q500, ne_top=ne_top, sw_top=sw_top, shelf=shelf, sfl=sfl, rise=rise,
             strip_full=sfl + STRIP_DEPTH, strip_lip=(zf(st0), zf(st1)), levels=lv, wl_w=wl_w, t0=t0, low=low,
             width=width, base=sfl - P14_POCHE, prof=pts, segs=segs, b0=b0, b1=b1, src=src, _ss=ss,
             dmax=max(level_month_depth("S4", m) for m in range(1, 13)),
             today=[(ne1, zf(ne1))] + [(s_, zf(s_)) for s_ in grid if ne1 < s_ < r1] + [(r1, zf(r1))],
             zones=dict(bed=(b0, b1), gravel=(b0, st0), strip=(st0, st1), toe=toe, terrace=(t0, ne1),
                        market=(b1 + 0.5, P14_WALK[0] - 1.0), walk=P14_WALK, steps=(ne1, p0), prom=(p0, p1),
                        bike=(p1, p2), fill=(p2, p3), sw_slope=(-sw0, b0), sw_path=(-sw1, -sw0),
                        bed_sw=(b0, b0 + 2.5), open=(b0 + 3.0, st0 - 0.5),
                        terr_b=(P14_WALK[0] - 1.0, P14_WALK[0]), terr_c=(P14_WALK[1], ne1),
                        edge=(st0 - 4.0, st0 - 0.2), open_w=(b0 + 3.0, st0 - 4.5), prom_edge=(p0, p0 + 3.0),
                        prom_in=(p0 + 3.0, p1), wedge=wedge,    # R2-C scenes: the strip's edge, the promenade's edge
                        wade_s=(max(st1, wl_s - P14_WADE_S[0]), max(st1, wl_s - P14_WADE_S[1]))))   # round 5: the
    #                                                  spring waders' margin (P14_USE spring, PLAN §8)
    _P14_GEO.append(G)
    _p14_planting()
    return G


def _p14_planting():
    """S4's planting, once a run, in m across the cut (k 1): each run of P14_PLANT_RUNS through plants.py's
    pla_group_section (G9: mixed groups, crowns overlapping, the low layer under and around them, never rows), its
    band t running through the zones' own (P14_PLANT_ZONES, t at each zone's start and end), its species the zones'
    together, the ground between its zones kept free; trees no taller than P14_TREE_MAX (crown scaled with them).
    Fills P14_PLANTS and P14_GROUPS (what each group does: pla_purpose tags)."""
    if P14_PLANTS:
        return P14_PLANTS
    zn = _p14_geo()["zones"]
    pz = dict((z_[0], z_[1:]) for z_ in P14_PLANT_ZONES)
    out, grp = [], []
    for run in P14_PLANT_RUNS:
        zs = sorted([z_ for z_ in run if z_ in pz and zn[z_][1] - zn[z_][0] >= 0.5], key=lambda z_: zn[z_][0])
        if not zs:
            continue
        knots = []
        for z_ in zs:
            knots += [(zn[z_][0], pz[z_][0]), (zn[z_][1], pz[z_][1])]

        def tf(x, kn=knots):
            if x <= kn[0][0]:
                return kn[0][1]
            for (xa, ta), (xb, tb) in zip(kn[:-1], kn[1:]):
                if xa <= x <= xb:
                    return ta if xb - xa < 1e-9 else ta + (tb - ta) * (x - xa) / (xb - xa)
            return kn[-1][1]
        mix = []
        for z_ in zs:
            mix += [k_ for k_ in pz[z_][2] if k_ not in mix]
        avoid = [(zn[p_][1], zn[q_][0]) for p_, q_ in zip(zs[:-1], zs[1:]) if zn[q_][0] > zn[p_][1] + 1e-6]
        _sh, placed, groups = pla_group_section(zn[zs[0]][0], zn[zs[-1]][1], 0.0, 1.0, t0=tf, mix=mix,
                                                seed=pz[zs[0]][4], layers=(0,), style="b",
                                                density=sum(pz[z_][3] for z_ in zs) / float(len(zs)), avoid=avoid,
                                                hires=False, detail=False)
        for key, s, h, w, _l in placed:
            if h > P14_TREE_MAX:
                w, h = w * P14_TREE_MAX / h, P14_TREE_MAX
            out.append((key, round(s, 2), round(h, 2), round(w, 2)))
        grp += [(round(xa, 2), round(xb, 2), list(ks), list(tags)) for _l, xa, xb, ks, tags in groups]
    out.sort(key=lambda p: p[1])
    P14_PLANTS[:] = out
    P14_GROUPS[:] = sorted(grp)
    return P14_PLANTS


def _p14_size(key):
    """(height, crown) m a species is drawn at on its own (keys, the year): plants.py's drawing size, trees capped"""
    sp = PLA_SPECIES[key]
    h, w = sp["h_m"], sp["crown_m"]
    if h > P14_TREE_MAX:
        w, h = w * P14_TREE_MAX / h, P14_TREE_MAX
    return h, w


_P14_WATER = {}


def _p14_water(sea, mode="season"):
    """the water drawn on S4: (level m, wet stretches [(a, b)] m across, level as a function of m across for
    fig_place_zones). Round 3 (DATA-1, N2 a): the water fills the surveyed profile below the level, in the stream's
    run only. mode "season": the season's mean level (G["levels"], level_season_depth; in summer and autumn the natural
    level, the strip drawn full of clean water under it by _p14_cut); "avg": the registry's average yearly flow (M5)"""
    if (sea, mode) in _P14_WATER:
        return _P14_WATER[(sea, mode)]
    G = _p14_geo()
    s0, s1 = P14_RANGE
    zw = G["levels"]["avg"] if mode == "avg" else G["levels"][sea]
    out = (zw, _p14_wet(zw, s0, s1), (lambda s, _z=zw: _z))
    _P14_WATER[(sea, mode)] = out
    return out


def _p14_people(sea, mode="season"):
    """the season's people in m across S4, once a run: [(pose, m across, facing, seed, layer, zone kind)] from P14_USE
    through figures.py's fig_place_zones on the cut's own ground (k 1: positions and levels in m; walkable zones only,
    nobody where the water drawn in mode (_p14_water) is deeper than knee, G10 + Aras 31 Oct); one drawn people style
    (round 3, PLAN §2: fig_side's pen language, every pose drawn); pose "market" = a stall with its vendor and buyer, "group" = three people
    together (_p14_person). R2-C scenes: each zone's cast and focus (P14_USE) turn the people to what they are there
    for (the water, a stall: _p14_face)"""
    if (sea, mode) in _P14_PEOPLE:
        return _P14_PEOPLE[(sea, mode)]
    zn = _p14_geo()["zones"]
    zw, wet, wfn = _p14_water(sea, mode)
    out, stalls = [], []
    for u_ in P14_USE.get(sea, []):
        zone, kind, dens, seed, layer, fo, cast, mx = (tuple(u_) + (None,) * 3)[:8]
        a, b = zn[zone]
        fs = _p14_focus(wet, a, b) if fo == "water" else None
        _sh, placed = fig_place_zones([(kind, a, b)], _p14_surf, 1.0, seed=seed, layer=layer, style="b",
                                      density=dens, water=wfn, max_per_zone=mx, focus=fs)
        poses = []
        for i, (kd, pose, s) in enumerate(placed):
            if cast and pose not in ("market", "group", "bike"):
                pose = cast[i % len(cast)]
            poses.append(pose)
        faces = _p14_face(poses, [s for _kd, _p, s in placed], seed, fs, stalls if fo == "stall" else None)
        for i, ((kd, _p, s), pose, face) in enumerate(zip(placed, poses, faces)):
            if pose == "market":
                stalls.append(s)
            pose = _p14_act(pose, s, face, sea, mode, zw, wet)
            out.append((pose, s, face, seed * 10 + i, layer, kd))
    _P14_PEOPLE[(sea, mode)] = out
    return out


def _p14_act(pose, s, face, sea, mode, zw, wet):
    """round 5 (S3 sf_activity_ok, PLAN §8, G-R5-4.4): a fisher only where the drawn water lies ahead within
    P14_FISH_REACH, a wader only in drawn water at most 0.50 m deep; neither in Jul-Sep (the row's month) but in the
    summer strip whose water is drawn (summer, autumn, the average flow). A refused fisher watches, a refused wader
    stands (sf_activity_ok writes the WARNING). Returns the pose drawn."""
    kind = "fish" if pose == "fishing" else ("wade" if pose == "wade" else None)
    if kind is None:
        return pose
    G = _p14_geo()
    st0, st1 = G["zones"]["strip"]
    strip_on = mode == "avg" or sea in ("summer", "autumn")           # _p14_cut draws the strip full of water then
    if kind == "fish":
        ahead = [q for q in (min(max(s, a), b) for a, b in wet)
                 if (q - s) * face >= -0.05 and abs(q - s) <= P14_FISH_REACH]
        wy = zw if ahead else None
        strip = strip_on and any(st0 <= q <= st1 for q in ahead)
    else:
        wy = zw if any(a <= s <= b for a, b in wet) else None
        strip = strip_on and st0 <= s <= st1
    ok, _why = sf_activity_ok(kind, _p14_surf(s), wy, 1.0, P14_SEA_MONTH.get(sea), strip=strip,
                              page=WBX_PG_NE if mode == "avg" else WBX_PG_SEASONS,
                              what=u"S4 %s at %.1f m" % (sea, s))
    return pose if ok else ("watch" if kind == "fish" else "stand")


def _p14_focus(wet, a, b):
    """the m across people in the zone a..b look at: the nearest point of the season's water (wet stretches), the
    zone's middle where it lies in the water; None without water"""
    m = (a + b) / 2.0
    pts = [min(max(m, wa), wb) for wa, wb in wet]
    return min(pts, key=lambda q: abs(q - m)) if pts else None


def _p14_face(poses, xs, seed, focus=None, stalls=None):
    """R2-C scenes (figures.py's fig_activity rule): the facing (1 = to the north-east) of each of a zone's people.
    focus (m): people who stay (FIG_FOCUS_POSES, sitters, groups) look at it, children playing turn to each other in
    pairs (the left one looks right). stalls (a list, the market ground's): each stall faces its nearest person (its
    buyers' side), every person faces the nearest stall (this zone's or one drawn before); walkers and riders keep
    their own way."""
    face = [1 if (seed + i) % 2 else -1 for i in range(len(poses))]
    if stalls is not None:
        own = [x for p_, x in zip(poses, xs) if p_ == "market"]
        folk = [x for p_, x in zip(poses, xs) if p_ != "market"]
        for i, (p_, x) in enumerate(zip(poses, xs)):
            if p_ == "market":
                to = min(folk, key=lambda q: abs(q - x)) if folk else (min(xs) + max(xs)) / 2.0
                face[i] = 1 if to >= x else -1
            elif own or stalls:
                to = min(own + list(stalls), key=lambda q: abs(q - x))
                face[i] = 1 if to >= x else -1
        return face
    run = 0
    for i, (p_, x) in enumerate(zip(poses, xs)):
        if p_ in FIG_PAIR_POSES:
            face[i] = 1 if run % 2 == 0 else -1
            run += 1
            continue
        run = 0
        if focus is not None and (p_ in FIG_FOCUS_POSES or p_ in ("sit_step", "group")):
            face[i] = 1 if focus >= x else -1
    return face


def _p14_person(pose, x, gy, k, facing, seed, style="b", layer=0, wl=None, ink=None, wcol=None):
    """one entry of _p14_people at page x on the ground gy (page y), k mm per m as printed (a view passes its
    perspective k), layer = the D9 fade only; wl = the water level (page y) where the ground is under water (the
    strip, at most knee deep: fig_place_zones keeps people out of deeper water): the figure stands on the floor and
    the water (wcol) is drawn over its shins, the rest of it above the water line. "group": three people together,
    standing cutouts (no drawn pose). Returns house shapes."""
    K = k / fig_depth(layer)[0]
    if pose == "market":
        return fig_stall(x, gy, K, facing=facing, layer=layer, seed=seed, ink=ink, canopy=P14_STALL_CANOPY,
                         style=style)
    wet = wl is not None and wl > gy + 0.02 * k
    if pose == "group" and not wet:
        sh = []
        for j, (p_, dx) in enumerate((("stand", -0.55), ("walk", 0.05), ("adult_child", 0.7))):
            sh += fig_side(p_, x + dx * k, gy, K, facing=facing if j else -facing, ink=ink, layer=layer, style=style,
                           pick=seed + j)
        return sh
    if wet and pose not in ("walk", "stand", "child_play", "adult_child", "touch_water", "wade"):
        pose = "stand"
    sh = fig_side(pose, x, gy, K, facing=facing, ink=ink, layer=layer, style=style, pick=seed)
    if wet:
        sh = list(sh) + [("poly", rect(x - 0.45 * k, gy - 0.05 * k, x + 0.45 * k, wl), wcol or C["w2"], None, 0.0),
                         ("line", [(x - 0.45 * k, wl), (x + 0.45 * k, wl)], C["w3"], 0.1)]
    return sh


def _p14_surf(s):
    """the ground of the cut at s (at a riser or a strip side the upper one); a binary search on the profile"""
    G = _p14_geo()
    pts, ss = G["prof"], G["_ss"]
    if s <= ss[0]:
        return pts[0][1]
    if s >= ss[-1]:
        return pts[-1][1]
    lo, hi = 0, len(ss) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ss[mid] <= s:
            lo = mid
        else:
            hi = mid
    best = None
    for i in range(max(0, lo - 3), min(len(pts) - 1, lo + 3)):
        (a, za), (b, zb) = pts[i], pts[i + 1]
        if b > a and a - 1e-9 <= s <= b + 1e-9:
            z = za + (zb - za) * (s - a) / (b - a)
            best = z if best is None else max(best, z)
    return pts[lo][1] if best is None else best


def _p14_wet(z, s0, s1, step=0.05, main=True):
    """the stretches from s0 to s1 whose ground lies under the level z: [(a, b)]; main: only the one the stream runs
    in (holding 0 m across; a low pocket elsewhere, e.g. a street under Q500 behind the fill, is not the stream's)"""
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
    if main:
        out = [(a_, b_) for a_, b_ in out if a_ - step <= 0.0 <= b_ + step]
    return out


def _p14_depth(m):
    """the mean water depth over the bed's low point in month m (0 = Jan) at S4 (round 3, DATA-1): the level module's
    S4 row, the higher of the two gauge routes (level_month_depth)"""
    return level_month_depth("S4", m + 1)


_P14_COVER = []


def _p14_cover_months():
    """the months (0 = Jan) whose mean level wets at least P14_COVER of the bed floor (b0..b1): "the stream covers the
    bed" (round 3: the surveyed bed is no flat sheet; drawing rule P14_COVER), once a run"""
    if not _P14_COVER:
        G = _p14_geo()
        w = G["b1"] - G["b0"]
        _P14_COVER.append([m for m in range(12) if sum(
            b - a for a, b in _p14_wet(G["bed"] + _p14_depth(m), G["b0"], G["b1"], 0.1)) >= P14_COVER * w])
    return _P14_COVER[0]


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
                _p14_keep_grp(out[-1], it)            # v16 (G6-9): the copy keeps its group
        elif it[0] == "line":
            for run in _p14_clip_line(it[1], r):
                out.append(("line", run) + tuple(it[2:]))
                _p14_keep_grp(out[-1], it)
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


P14_BARE_EDGE = "B0AC9C"
P14_KEY_GREY = ("B7B2A6", "8E887C")  # the calendar legend's samples (in leaf, in flower): neutral, each row's bars
#                                      carry the species' own colours (round 4, G-R4-6: no page-wide greenery colour)


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


def _p14_cell(pg, x0, y0, x1, y1, st, col=None):
    """one calendar cell of a plant state; col = its colour (the species' own from pla_colours, or a legend grey)"""
    r = rect(x0, y0, x1, y1)
    if st == "leaf":
        pg.poly([r], fill=col or P14_KEY_GREY[0])
    elif st == "bloom":
        pg.poly([r], fill=col or P14_KEY_GREY[1])
    elif st == "bare":
        pg.poly([r], fill=COL["white"], stroke=P14_BARE_EDGE, lw=0.1)
    elif st == "cut":
        c_ = col or P14_KEY_GREY[1]
        pg.poly([r], fill=COL["white"], stroke=c_, lw=0.1, stripes=(c_, 0.55, 0.1, 45.0))


def _p14_bloom_col(key):
    """the flower colour of a species for the calendar bars (G-R4-6): pla_colours' accent in its bloom season, else
    its light fleck"""
    for sea in SEAS:
        c = pla_colours(key, sea)
        if c.get("accent"):
            return c["accent"]
    return pla_colours(key)["lt"]


def _p14_plant(key, x, gy, k, month, h=None, cw=None, seed=0, style="b", layer=0, detail=True, season=None):
    """a species in section (plants.py) as it is that month (1-12), ground at (x, gy) page mm, k mm per m AS PRINTED
    (the caller's true scale times its layer's scale; a view passes its perspective k): round 3 (D7, G9, G15) through
    pla_section(month=): the season's species colour, deciduous species out of leaf drawn bare (branches with the open
    gaps between them, pla_bare), flowers only in the bloom months, always vector and opaque, the new willow; layer =
    the D9 depth tone (pla_section scales by it, so k is handed on without that scale). style: kept for the callers
    (a seasonal plant is vector in every style). Round 4: season (the cuts and views) = plants.py's season state;
    month (the calendar) its month alias. Returns house shapes."""
    sc = fig_depth(layer)[0] if layer else 1.0
    if season is not None:
        return pla_section(key, x, gy, k / sc, h, cw, False, seed, hires=detail, style="b", layer=layer,
                           detail=detail, season=season)
    return pla_section(key, x, gy, k / sc, h, cw, False, seed, hires=detail, style="b", layer=layer, detail=detail,
                       month=month)


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
    """round 3 (G15): only in the season's sourced list beside the drawings (the sections and views draw generic birds
    until research/fauna.md exists); opaque. ONE place for the animal pictograms of pp.14-15 (figures.py, which will hold them, is paused): the P14_FAUNA
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
            E(-0.2, cy_, 0.06, 0.2, rot, light, True)
        for cy_, rot in ((0.18, -12), (-0.18, 12)):
            E(-0.08, cy_, 0.07, 0.21, rot, light, True)
        B([(-0.12, 0.0), (0.46, 0.0)], 0.05, body)
        E(-0.2, 0.0, 0.08, 0.05, 0, wing)
        E(-0.32, 0.0, 0.05, 0.055, 0, body)
    elif kind == "damselfly":
        E(0.12, 0.07, 0.26, 0.045, 3, light, True)
        E(0.16, 0.07, 0.1, 0.04, 3, wing, False)
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


# ---------------------------------------------------------------- the key map: S4 only (v16: keymap.py v3 km_keymap)


def _p14_keymap(page, size, item_id, log=None):
    """v16 (round 6, S5, G6-5): the key map of S4 from the one module (common/keymap.py v3 km_keymap: S4 as a bold red
    cut with its end triangles, the study area closed, street names subtle), size = (w, h) mm the most room the page
    frame offers (fitted inside), handed to the booklet whole (wbx_keymap); nothing drawn on the board. page = the
    board page id (WBX_PG_SEASONS / WBX_PG_NE); km_keymap takes the round 6 id (wbx_p) and writes its own
    `keymap <page> module ...` log line. Returns the key map dict, or None (a WARNING, never a stop)."""
    w, h = size
    try:
        km = km_keymap(wbx_p(page), cut_ids=["S4"], w_mm=w, h_mm=h, log=log)
    except Exception as ex:
        if log is not None:
            log.append(u"FLAG {} key map not made: {}: {}".format(page, type(ex).__name__, ex))
        wbx_warn(page, "keymap", u"S4 key map not made: {}: {}".format(type(ex).__name__, ex))
        return None
    if not km or (isinstance(km, dict) and "items" in km and not km["items"]):
        wbx_warn(page, "keymap", u"S4 key map not made: no basemap data (run the site board once)")
        return None
    wbx_keymap(page, km, item_id=item_id)
    return km


def _p14_grp(pg, kind=None, eid=None):
    """v16 (round 6, S5, G6-9): the items drawn on pg from now on are one element "<kind>/<eid>" (Page.g's tag set
    without a with-block, so long drawing runs keep their indentation); no kind ends it. A Page without groups
    ignores it."""
    if hasattr(pg, "cur_grp"):
        pg.cur_grp = u"%s/%s" % (kind, eid) if kind else None


def _p14_keep_grp(new, old):
    """v16 (G6-9): a clipped copy of a page item keeps the item's group tag (code.py wb_grp_of / _GRP)"""
    f_ = globals().get("wb_grp_of")
    g_ = f_(old) if f_ else None
    if g_:
        _GRP[id(new)] = (new, g_)


def _p14_level_spread(page, did, rows, Y, ytop, log=None, fs=None):
    """v16 (round 6, S5, PLAN §2.3): the ▽ values at a section's right edge never stacked: spread upward from their
    lines with a gap of at least the text height (1.3 x fs, mm on the board = print at the drawing's scale); a value
    that would rise over the drawing's top (ytop, board mm) is a WARNING (never a stop). rows = [(key, m)];
    Y = m a.s.l. -> board y. Returns the number of values moved off their own line."""
    fs = fs or FS_MIN
    gap = 1.3 * fs
    prev, moved, top = None, 0, None
    for key, z in sorted(rows, key=lambda r_: r_[1]):
        y = Y(z)
        yy = y if prev is None else max(y, prev + gap)
        if yy > y + 1e-6:
            moved += 1
        prev = yy
        top = (key, z, yy)
    if top is not None and top[2] + fs > ytop + 1e-6 and log is not None:   # v17 (L4): info only; the values
        log.append(u"levels {} {}: the spread reaches {:.1f} mm over the top (the booklet staggers them)".format(
            wbx_p(page), did, top[2] + fs - ytop))  # are wbx_levels items, the booklet staggers (LAYOUT_PLAN 3.2-4)
    if log is not None:
        log.append(u"levels {} {}: {} values at the right edge, {} spread off their line (gap {:.1f} mm)".format(
            wbx_p(page), did, len(rows), moved, gap))
    return moved


def _p14_hue_log(page, log):
    """v16 (G6-6): `legend <page> hues=table` once (common/hues.py hue_log; it may write the line itself)"""
    if log is None:
        return
    n_ = len(log)
    try:
        r_ = hue_log(wbx_p(page), log=log)
    except Exception as ex:
        r_ = None
        log.append(u"FLAG {} hue_log: {}: {}".format(page, type(ex).__name__, ex))
    if len(log) == n_:
        ln = r_ if isinstance(r_, str) and r_ else u"legend {} hues=table".format(wbx_p(page))
        if ln not in log:
            log.append(ln)


# ---------------------------------------------------------------- the cut, drawn (pp.14 and 15)
P14_LOOK = {  # each season's water on the cuts (v16: the views are gone, P-11; sky and gravel kept as data)
    "winter": dict(sky="DCE3E6", gravel="BBB4A2", water="86AEBC"),
    "spring": dict(sky="E3EDF0", gravel="CEC6B3", water="96BCC8"),
    "summer": dict(sky="F3EFE2", gravel="DDD4BE", water="8CBBC8"),
    "autumn": dict(sky="ECE5D7", gravel="D5CCB6", water="90B5C1"),
}
P14_HOUSE_ON = 0.50                  # m: a background house stands only where the cut's ground under all of it lies
#                                      no lower than this under the lower bank top (drawing rule: no house in the
#                                      stream's valley, where the bed and its terraces run on behind the cut)
_P14_HOUSES = {}


def _p14_t0():
    """m along the registry cut S4 (from its end S4) where it crosses the Selinos line (p.12's P12_SELINOS): the
    page's 0 m across, north-east + (as p.17's _p17_s4_pt); None where it does not cross"""
    a, b = level_ends("S4")
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    d1 = (b[0] - a[0], b[1] - a[1])
    P = globals().get("P12_SELINOS") or []
    for p, q in zip(P[:-1], P[1:]):
        d2 = (q[0] - p[0], q[1] - p[1])
        den = d1[0] * d2[1] - d1[1] * d2[0]
        if abs(den) > 1e-12:
            w = (p[0] - a[0], p[1] - a[1])
            t = (w[0] * d2[1] - w[1] * d2[0]) / den
            u = (w[0] * d1[1] - w[1] * d1[0]) / den
            if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
                return t * L
    return None


def _p14_houses(rng, log=None):
    """the basemap houses behind S4 over rng (m across), once a run (section_frame.py's sf_back_buildings: SF_BACK_BAND
    m behind the cut, data height else floors x BLD_STOREY): [(m from, m to, h m, floors, m behind)] farthest first,
    only those on the high ground beside the stream (P14_HOUSE_ON)"""
    if rng in _P14_HOUSES:
        return _P14_HOUSES[rng]
    t0 = _p14_t0()
    if t0 is None:
        if log is not None:
            log.append(u"pp.14-15 background houses: S4 does not cross the Selinos line (P12_SELINOS); none drawn")
        _P14_HOUSES[rng] = []
        return []
    G = _p14_geo()
    z_on = min(G["sw_top"], G["ne_top"]) - P14_HOUSE_ON
    out, low = [], 0
    for ta, tb, h, fl, d in sf_back_buildings("S4", t0 + rng[0], t0 + rng[1], log=log):
        sa, sb = ta - t0, tb - t0
        zs = [_p14_surf(sa + (sb - sa) * i / 8.0) for i in range(9)] + [z for s_, z in G["prof"] if sa < s_ < sb]
        if min(zs) < z_on:
            low += 1
            continue
        out.append((sa, sb, h, fl, d))
    if log is not None:
        log.append(u"pp.14-15 background houses {:.0f} to {:+.0f} m across: {} drawn, {} over the stream's valley left "
                   u"out".format(rng[0], rng[1], len(out), low))
    _P14_HOUSES[rng] = out
    return out


def _p14_back(X, Y, k, rng, month, style="b", zw=None, ytop=None, season=None):
    """the houses and trees beyond the cut (R16: depth through faded background houses and trees): the basemap's
    houses behind S4 (_p14_houses; sf_back_house, D9 layer 1 nearer than the band's middle, else 2), farthest first,
    left out where the roof would leave the drawing (above ytop, page y); then plants.py's pla_group_section of S4's
    own trees and shrubs in D9 layers 2 and 1 (G9 mixed groups; depth tone by layer) in front of them; all seated on
    the lowest ground of the cut's line under them (G14), no tree over the bed nor where the ground lies under the
    water zw (m), each in the month's state (round 4: in season's, plants.py; houses with d_m, windows only near the
    cut, sf_back_house v2). Returns house shapes."""
    G = _p14_geo()
    xa, xb = X(rng[0]), X(rng[1])

    def gy(x):
        return Y(_p14_surf(rng[0] + (x - xa) / k))
    out = []
    pitch = math.tan(math.radians(globals().get("BLD_PITCH", 30.0)))
    mix = sorted(set(p[0] for p in P14_PLANTS if PLA_SPECIES[p[0]]["layer"] in ("tree", "shrub")))
    for lay in (2, 1):                                  # layer by layer, farthest first: its houses, then its trees
        for sa, sb, h, fl, d in _p14_houses(rng):
            if (1 if d < 0.5 * sum(SF_BACK_BAND) else 2) != lay:
                continue
            x_a, x_b = X(sa), X(sb)
            if ytop is not None and sf_ground_min(gy, x_a, x_b) + (h + pitch * min(0.5 * (sb - sa) + 0.3, 4.0)) * k > ytop:
                continue
            out += sf_back_house(x_a, x_b, gy, h, k, layer=lay, floors=fl, d_m=d)
        if len(mix) < 2:
            continue
        _sh, placed, _gr = pla_group_section(xa, xb, gy, k, t0=0.40, t1=0.70, mix=mix, seed=40, layers=(lay,), style="b",
                                             density=0.6, avoid=[(X(G["b0"]), X(G["b1"]))], hires=False, detail=False,
                                             water=None if zw is None else Y(zw))
        for i, (key, x, h, w, layer) in enumerate(placed):
            if h > P14_TREE_MAX:
                w, h = w * P14_TREE_MAX / h, P14_TREE_MAX
            sc = fig_depth(layer)[0]
            y = sf_seat_x(gy, x, (0.12 if PLA_SPECIES[key]["layer"] == "tree" else 0.35) * w * k * sc)
            out += _p14_plant(key, x, y, k * sc, month, h, w, 50 * layer + i, style, layer, detail=False,
                              season=season)
    return out


P14_STEPS_LOG = ["atmosphere", "background", "ground", "bed", "water", "vegetation", "figures", "labels"]   # G8: the
#                                      order _p14_cut and its page draw in (wat_draw_order_lines)


P14_STREET_AT = (1.2, 0.6, 1.8, 0.4)   # m: the bench past the promenade's edge, the lamp and the rack before its
#                                      end, the bollard past the lower walk's start (drawing rules, round 3)


def _p14_street_pos():
    """[(m across, kind)] of S4's street elements (P14_STREET_AT)"""
    zn = _p14_geo()["zones"]
    p0, p1 = zn["prom"]
    b, l_, r_, o_ = P14_STREET_AT
    return [(p0 + b, "bench"), (p1 - l_, "lamp"), (p1 - r_, "rack"), (P14_WALK[0] + o_, "bollard")]


def _p14_street(X, k, rng, gy, sitter=False):
    """the street elements of S4's proposal at the cut (G15; sizes are section_frame.py's drawing rules, never printed):
    a bench at the promenade's water edge facing the stream, a lamp and a bike rack on its land side by the bike lane,
    a bollard where the floodable lower walk starts (it is closed in a flood). gy(x) = the ground's page y. Round 5
    (PLAN §8 p15 summer "shade seating"): sitter = someone seated on the bench under the promenade's trees (the
    shaded terrace), p12's bench-sitter pattern (fig_meta seat_x, SF_SEAT_H). Returns house shapes."""
    out = []
    for s, kind in _p14_street_pos():
        if not rng[0] + 0.5 <= s <= rng[1] - 0.5:
            continue
        x = X(s)
        y = gy(x)
        if kind == "bench":
            out += sf_bench(x, y, k, side=-1, back=True)
            if sitter:
                an = fig_meta("sit_step", facing=-1, seat_h=SF_SEAT_H)
                out += fig_side("sit_step", x - 0.225 * k - an.get("seat_x", 0.0) * k, y, k, facing=-1,
                                seat_h=SF_SEAT_H)
        elif kind == "lamp":
            out += sf_lamp(x, y, k, side=-1)
        elif kind == "rack":
            out += sf_bike_rack(x, y, k, side=1)
        else:
            out += sf_bollard(x, y, k)
    return out


def _p14_cut(pg, x0, yb, k, rng, sea, month, people=True, style="b", water="season", back=True, ytop=None,
             trees_back=True, street=True, page=None, qlines=True):
    """the S4 cut from rng[0] to rng[1] (m across) at k mm per m, rng[0] at x0 and its base (G["base"]) at yb, as it is
    in sea, drawn in the G8 order (P14_STEPS_LOG): the houses and trees beyond (R16), the cut ground (round 3: the
    surveyed profile, the G15 soil gradient under the earth hatch, the gravel bed following the profile, the strip's
    concrete liner, walk, steps and promenade), the water (_p14_water, filling the profile only below its level, opaque:
    water "season" = the season's mean level, "avg" = the registry's average yearly flow through water.py; the summer
    strip full of clean water in summer, autumn and at the average flow, N2 a; the Q100 / Q500 lines on every cut), the
    cut's trees one depth layer back (trees_back, G15: paler, behind the use zones), the people just beyond the cut
    (D9 layer 1), the street elements (_p14_street), the low planting in month's state (only emergent species where
    the ground lies under the water), the season's people and stalls in front (P14_USE, true size). Every plant,
    person and stall seated on the lowest ground under its base (G14). Returns (X, Y): m across -> page x, level ->
    page y. Round 5: page (booklet id) sets the cut's tree layer by sf_tree_level (p15 trees lead at layer 0, p16
    behind the people at 1; trees_back only when no page is given); people stand on the higher ground at their feet
    (sf_seat_feet); a wader approved by _p14_act stands knee deep in the stream too; summer's bench gets a sitter.
    v16 (round 6, S5): ACCURATE language (r06_S03: true scale, library people and seasonal plant images, light soil,
    no hatch); qlines False leaves the Q100 / Q500 lines out (booklet p13: only the winter cut carries them, as
    r06_S03); every element tagged for G6-9 (_p14_grp: buildings, ground, water, levels, trees, plants, people,
    other), the trees counted per page for the G6-10 log (_P14_TREES)."""
    G = _p14_geo()
    s0, s1 = rng
    zb = G["base"]

    def X(s):
        return x0 + (s - s0) * k

    def Y(z):
        return yb + (z - zb) * k

    def gpy(x):
        return Y(_p14_surf(s0 + (x - x0) / k))
    mode = "avg" if water == "avg" else "season"
    zw, wet, _wf = _p14_water(sea, mode)
    clip = (X(s0), -1e9, X(s1), 1e9)
    if back:
        _p14_grp(pg, "buildings", u"S4 houses and trees beyond")
        shp_put(pg, _p14_back(X, Y, k, rng, month, style, zw, ytop, season=sea))
    _p14_grp(pg, "ground", u"S4 cut ground")

    def put(ring_m, mat):
        r_ = _p14_clip_ring([(X(s), Y(z)) for s, z in ring_m], clip)
        if r_:
            if mat == "earth":                         # G15: the hatch only, over the soil gradient
                sec_put(pg, sct_hatch_fill(r_, mat, k, None, 0.1, fill=False, hatch_lw=SCT_SOIL["hatch_lw"]))
            else:
                sec_put(pg, sct_hatch_fill(r_, mat, k, None, 0.1))
    bed, sfl, shelf, zn = G["bed"], G["sfl"], G["shelf"], G["zones"]
    st0, st1 = zn["strip"]
    lt = P14_LINER
    pts = [(s0, _p14_surf(s0))] + [p for p in G["prof"] if s0 < p[0] < s1] + [(s1, _p14_surf(s1))]
    shp_put(pg, sct_soil_gradient([(X(s), Y(z)) for s, z in pts], Y(zb), k))
    put(pts + [(s1, zb), (s0, zb)], "earth")
    for a, b in ((G["b0"], st0 - lt), (st1 + lt, G["b1"])):   # the gravel bed, under the surveyed ground
        a, b = max(a, s0), min(b, s1)
        if b - a < 0.05:
            continue
        top = [(a, _p14_surf(a))] + [p for p in G["prof"] if a < p[0] < b] + [(b, _p14_surf(b))]
        put(top + [(s_, z_ - P14_GRAVEL) for s_, z_ in reversed(top)], "gravel")
    t0, t1 = zn["terrace"]
    put([(t0, shelf), (t1, shelf), (t1, shelf - 0.3), (t0, shelf - 0.3)], "gravel")
    zl0, zl1 = G["strip_lip"]
    put([(st0 - lt, zl0), (st0 - lt, sfl - lt), (st1 + lt, sfl - lt), (st1 + lt, zl1), (st1, zl1), (st1, sfl),
         (st0, sfl), (st0, zl0)], "concrete")
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
    # the water, before the plants and people (G8), opaque
    _p14_grp(pg, "water", u"Selinos " + (u"average flow" if water == "avg" else sea))
    pal = _wat_pal()
    wcol = P14_LOOK[sea]["water"]
    if water == "avg":
        wl = water_section([(X(s), Y(z)) for s, z in pts], k, Y, cid="S4", labels=False)
        shp_put(pg, wl.shapes(("water",)))
        wcol = C["w2"]
    else:
        for a, b in wet:
            a, b = max(a, s0), min(b, s1)
            if b <= a:
                continue
            ring = [(X(a), Y(zw))] + [(X(s), Y(z)) for s, z in G["prof"] if a < s < b] + [(X(b), Y(zw))]
            pg.poly([ring], fill=wcol)
            pg.line([(X(a), Y(zw)), (X(b), Y(zw))], C["w3"], 0.2)
        for zq, key in (((G["q100"], "q100"), (G["q500"], "q500")) if qlines else ()):
            _p14_grp(pg, "levels", u"%s %+.2f" % (P14_LEVEL_NAMES.get(key, key), zq))
            for a, b in _p14_wet(zq, s0, s1):
                pg.line([(X(a), Y(zq)), (X(b), Y(zq))], pal[key], 0.18, dash=[1.2, 0.7] if key == "q100" else [0.4, 0.5])
    if water == "avg" or sea in ("summer", "autumn"):     # N2 a: the summer strip full of clean water
        a_, b_ = max(st0, s0), min(st1, s1)
        top = min(G["strip_full"], zw)
        if b_ > a_ and top > sfl:
            _p14_grp(pg, "water", u"summer strip")
            pg.poly([rect(X(a_), Y(sfl), X(b_), Y(top))], fill=pal["low"])
            pg.line([(X(a_), Y(top)), (X(b_), Y(top))], C["w3"], 0.12)

    def folk(lay_):
        for pose, s, face, seed, layer, _kd in _p14_people(sea, mode):
            if layer != lay_ or not s0 + 1.0 <= s <= s1 - 1.0:
                continue
            sc = fig_depth(layer)[0]
            half = (0.8 if pose == "market" else (0.9 if pose == "group" else FIG_FOOT_HALF_M)) * k * sc
            y = sf_seat_feet(gpy, X(s), half)             # round 5 (S3): the higher ground at the feet
            under = any(a <= s <= b for a, b in wet) and y < Y(zw) - 0.02 * k
            if under and not (st0 <= s <= st1 or (pose == "wade" and (Y(zw) - y) / k <= FIG_WADE_MAX_M + 1e-6)):
                continue                                  # round 4 (G-R4-5.2): nobody in the water but the strip's
                #                                           (round 5: and the spring waders, knee deep, _p14_act)
            _p14_grp(pg, "people", u"person %d · %s" % (seed, pose))
            shp_put(pg, _p14_person(pose, X(s), y, k * sc, face, seed, style, layer, Y(zw) if under else None,
                                    wcol=wcol))

    def plants(trees):
        for i, (key, s, h, cw) in sorted(enumerate(P14_PLANTS), key=lambda t: -t[1][2]):
            tree = PLA_SPECIES[key]["layer"] == "tree"
            if tree != trees or not s0 + 0.3 <= s <= s1 - 0.3:
                continue
            if page is not None:                          # round 5 (S3 G-R5-4.5): the page's tree level
                layer = sf_tree_level(page)["layer"] if tree else 0
            else:
                layer = 1 if tree and trees_back else 0
            sc = fig_depth(layer)[0] if layer else 1.0
            y = sf_seat_x(gpy, X(s), (0.12 if tree else 0.35) * cw * k * sc)
            if y < Y(zw) - 0.02 * k and any(a <= s <= b for a, b in wet) and PLA_SPECIES[key]["layer"] != "emergent":
                continue                                  # G14: no plant in the water unless it grows there
            nm_ = PLA_SPECIES[key].get("name") or key
            _p14_grp(pg, "trees" if tree else "plants", u"%s %d · %s" % (u"tree" if tree else u"plant", i, nm_))
            if tree:
                _P14_TREES[page] = _P14_TREES.get(page, 0) + 1
            shp_put(pg, _p14_plant(key, X(s), y, k * sc, month, h, cw, i, style, layer, season=sea))

    def low():                                            # round 4 (G-R4-5.3): the shrub and flower layer
        for zone, ta, tb, mix, dens, seed in P14_PLANT_ZONES:
            low_mix = [k_ for k_ in mix if k_ in PLA_LOW]
            if zone not in P14_LOW_ZONES or not low_mix:
                continue
            a, b = max(zn[zone][0], s0), min(zn[zone][1], s1)
            if b - a < 0.5:
                continue
            _p14_grp(pg, "plants", u"low planting · " + zone)
            sh, _pl = pla_low_section(X(a), X(b), gpy, k, ta, tb, seed=seed + 60, density=P14_LOW_DENS * dens,
                                      water=Y(zw), season=sea, mix=low_mix, detail=k >= 3.0)
            shp_put(pg, sh)
    plants(True)                                          # G15: the cut's trees step back, behind the use zones
    if people:
        folk(1)
    if street:
        _p14_grp(pg, "other", u"street elements · bench, lamp, bike rack, bollard")
        shp_put(pg, _p14_street(X, k, rng, gpy, sitter=people and sea == "summer"))
    plants(False)
    low()
    if people:
        folk(0)
    _p14_grp(pg)
    return X, Y


# ---------------------------------------------------------------- the zones (booklet p14's parts list numbers them)
# v16 (round 6, S5): the old p14 four-seasons panel (rain bars, zone strips, PLANTS / ZONES keys, the views, the
# 1:200 insets) is gone (P-11); booklet p13 is pages/p13_seasons.py now. The zones' numbers stay for p14's parts list.
P14_MARK_PT, P14_MARK_R = 6.0, 1.7   # the zone numbers: pt (the G-R4-1 minimum), disc radius mm (one size for 1-11)
P14_ZONE_KEY = [  # the zones under each cut, numbered left to right (G10; our design); the reasons (third entry) are
    # printed on p.15 for the north-east bank (P15_WHY), on p.14 only the names (round 4, P14.1: the strip replaces the
    # paragraph)
    ("sw_path", u"shaded path", u"a walk under the planes, dry in every flood"),
    ("sw_slope", u"planted bank", u"roots hold the steep south-west bank"),
    ("open", u"gravel bed", u"the stream's in winter, open to walk {open}"),
    ("strip", u"summer strip", u"clean water to wade in when the stream is low"),
    ("toe", u"riparian edge", u"willow, tamarisk and rushes clean the water and hold the bank"),
    ("market", u"flood terrace", u"the Kermes market ground, dry except in floods"),
    ("walk", u"lower walk", u"floodable, closed by a bollard in a flood"),
    ("steps", u"sun steps", u"sit and watch the water; a flood rises up them"),
    ("prom", u"promenade", u"over Q500, dry in every flood; benches and lamps"),
    ("bike", u"bike lane", u"over Q500, apart from the walkers; bike racks beside it"),
    ("fill", u"planted fill", u"shade between the promenade and the street"),
]
# v16 (round 6, S5, G6-6): the zones' colours from the one hue table (common/hues.py hue(code, rank)), as
# plan_findings/hues_and_proposals.md H1 "The S4 cut, north-east bank" maps them: paths and walks MOV, the strip WAT r2,
# the planted slope / edge / fill GRN r1-r3, the gravel bed CTX r2, the market ground PUB r2
P14_ZONE_HUE = {"sw_path": ("MOV", 3), "sw_slope": ("GRN", 2), "open": ("CTX", 2), "strip": ("WAT", 2),
                "toe": ("GRN", 1), "market": ("PUB", 2), "walk": ("MOV", 3), "steps": ("MOV", 2), "prom": ("MOV", 1),
                "bike": ("MOV", 4), "fill": ("GRN", 3)}
P14_ZONE_COL = dict((z_, hue(c_, r_)) for z_, (c_, r_) in P14_ZONE_HUE.items())   # the zones' marker colours


def _p14_name(key, log=None):
    """a species' name as printed (D5): "English · Turkish" (plants.py), English alone where the Turkish name is not
    verified (FLAG once)"""
    sp = PLA_SPECIES[key]
    tr = (sp.get("turkish") or u"").strip()
    if not tr or tr.upper() == u"UNVERIFIED":
        ln = u"FLAG p14-15 plant names: {} has no verified Turkish name (plants.py): English only".format(key)
        if log is not None and ln not in log:
            log.append(ln)
        return sp["name"]
    return u"{} · {}".format(sp["name"], tr)


def _p14_mark(pg, cx, cy, s, colour, style="solid", size_pt=None, r_min=None):
    """one marker (marker.py mk_marker, G-R4-7) on pg: its disc a keep of the page's TextPage, its glyph a text that may
    sit on that disc only. Returns its box"""
    sh, box, _r = mk_marker(cx, cy, s, colour, size_pt=size_pt or P14_MARK_PT,
                            r_min=P14_MARK_R if r_min is None else r_min, style=style)
    MK_N[0] += 1
    nm = u"marker p14-15 %d" % MK_N[0]
    for s_ in sh:
        if s_[0] == "poly":
            pg.poly([s_[1]], fill=s_[2], stroke=s_[3], lw=s_[4] or 0.1)
            pg.keep(s_[1], "marker", nm)
        elif s_[0] == "text":
            pg.text(s_[1], s_[2], s_[3], s_[4], s_[5], bold=True, align="L", allow=(nm,))
    return box


def _p14_level_rows(sea, avg=False):
    """the levels a cut marks outside its frame (DATA-1, G-R4-5.4): [(key, m)]: Q500, Q100, the season's mean (avg:
    the registry's average flow), the bed; with the summer strip full (summer, autumn, avg) its full level and floor"""
    G = _p14_geo()
    zw = level_avg_flow("S4") if avg else G["levels"][sea]
    rows = [("q500", G["q500"]), ("q100", G["q100"]), (u"average flow" if avg else "mean", zw)]
    if avg or sea in ("summer", "autumn"):
        if abs(G["strip_full"] - G["bed"]) < 0.005:
            rows.append((u"bed, strip full", G["bed"]))
        else:
            rows += [(u"strip full", G["strip_full"]), ("bed", G["bed"])]
        rows.append((u"strip floor", G["sfl"]))
    else:
        rows.append(("bed", G["bed"]))
    return rows


P14_LEVEL_NAMES = dict(q500=u"Q500", q100=u"Q100")   # the other keys print as they are (round 4's marks)


def _p14_levels_out(page, did, rows, sea=None):
    """round 5 (G-R5-4.3 / U04, S8): a cut's levels handed to the booklet (wbx_levels: the booklet draws the U04
    markers beside the drawing, on its y = m a.s.l.; the board draws none). rows = _p14_level_rows' [(key, m)];
    "mean" = the season's mean level, named with its season. Returns the [(name, m)] exported."""
    out = []
    for key, z in rows:
        nm = (u"%s mean" % sea if sea else u"mean") if key == "mean" else P14_LEVEL_NAMES.get(key, key)
        out.append((nm, round(float(z), 2)))
    wbx_levels(page, did, out, side="R")
    return out


# ---------------------------------------------------------------- insets v2 (round 5, S3 G-R5-5, C6, U16)
P14_INSET_BOX = (80.0, 60.0)         # mm: the most room an inset drawing takes on the board (design value):
#                                      sf_inset_frame picks the largest listed scale >= 2 x its cut that fits it
P14_INSET_SPAN = 3.0                 # m either side of the spot: the people and street elements the inset is about
P14_INSET_N = 3                      # people an inset is about at most, the nearest to its spot (design value)
P14_INSET_RUN = 2.0                  # m drawn past the window on each side before the window cuts the drawing


def _p14_street_boxes():
    """[(kind, (m from, z, m to, z top))] of S4's street elements (sizes: section_frame's drawing rules SF_SEAT_H,
    SF_STREET; the bench's back 0.40 m, sf_bench)"""
    out = []
    for s, kind in _p14_street_pos():
        z = _p14_surf(s)
        if kind == "bench":
            b = (s - 0.50, z, s + 0.05, z + SF_SEAT_H + 0.45)
        elif kind == "lamp":
            b = (s - SF_STREET["lamp_arm"] - 0.20, z, s + 0.10, z + SF_STREET["lamp_h"] + 0.30)
        elif kind == "rack":
            b = (s - 0.05, z, s + SF_STREET["rack_l"] + 0.05, z + SF_STREET["rack_h"])
        else:
            b = (s - 0.10, z, s + 0.10, z + SF_STREET["bollard_h"])
        out.append((kind, b))
    return out


def _p14_person_box(pose, s, face):
    """the box (m from, z, m to, z top) one entry of _p14_people takes in the cut (drawing rules: a stall's canopy, a
    group or a bike 0.9 m either side, a person 0.45 m; a wader's feet 0.6 m under the water; a fisher's line
    P14_FISH_REACH ahead)"""
    z = _p14_surf(s)
    if pose == "market":
        return (s - 1.6, z, s + 1.6, z + FIG_STALL["canopy_top"] + 0.1)
    hw = 0.9 if pose in ("group", "bike", "dog_walk", "lying") else 0.45
    a, b = s - hw, s + hw
    if pose == "fishing":
        a, b = min(a, s + face * P14_FISH_REACH), max(b, s + face * P14_FISH_REACH)
    return (a, z - (0.6 if pose == "wade" else 0.0), b, z + FIG_ADULT_H + 0.1)


def _p14_inset2(pg, page, parent, X, Y, parent_den, sea, zone, words, at, water="season", sm=None, style="b",
                log=None, crop=None, group=None):
    """G-R5-5 / C6 / U16 (S3 inset v2): the use spot of zone (sm m across, its middle by default) as its OWN drawing,
    drawn again by _p14_cut at its own k (sf_inset_k: the kit's detail on), framed on the action by sf_inset_frame:
    the nearest P14_INSET_N people within P14_INSET_SPAN of the spot, the street elements there, and the water where
    the scene meets it; den = the largest listed inset scale >= 2 x parent_den that fits P14_INSET_BOX. The people,
    street elements and plants no taller than the window go through sf_inset_cut_check (trees are left out of the
    check: a crown always passes a window a few m high). at = (x, top, "L" | "R"): where the child sits on the
    board (its own item span, cut to its box, so nothing leaks into the parent). Registers the child (wbx_drawing,
    den, origin = (m across, m a.s.l.) at its lower left) and the inset link (wbx_inset; window in the parent's
    board mm by X, Y). Returns the child's id, or None."""
    G = _p14_geo()
    a, b = G["zones"][zone]
    sm = (a + b) / 2.0 if sm is None else sm
    mode = "avg" if water == "avg" else "season"
    zw, wet, _wf = _p14_water(sea, mode)
    folk = _p14_people(sea, mode)
    near = sorted([p_ for p_ in folk if p_[4] == 0 and abs(p_[1] - sm) <= P14_INSET_SPAN],
                  key=lambda p_: abs(p_[1] - sm))
    focus = [_p14_person_box(p_[0], p_[1], p_[2]) for p_ in near[:P14_INSET_N]]
    focus += [b_ for _n, b_ in _p14_street_boxes() if abs(0.5 * (b_[0] + b_[2]) - sm) <= P14_INSET_SPAN]
    if not focus:
        z = _p14_surf(sm)
        focus = [(sm - 1.5, z, sm + 1.5, z + FIG_ADULT_H)]
    fx0, fx1 = min(f_[0] for f_ in focus), max(f_[2] for f_ in focus)
    for wa, wb in wet:                                   # the water shown where the scene meets it (G-R5-5)
        if wa < fx1 + 1.0 and wb > fx0 - 1.0:
            focus.append((max(wa, fx0 - 1.0), zw - 0.3, min(wb, fx1 + 1.0), zw))
    fr = sf_inset_frame(focus, parent_den, box_mm=P14_INSET_BOX, page=page, label=words)
    if not fr:
        return None
    den, kc = fr["den"], fr["k"]
    stb = _p14_street_boxes()

    def _chk(w0, z0, w1, z1):
        c_ = [(u"%s at %.1f m" % (p_[0], p_[1]), _p14_person_box(p_[0], p_[1], p_[2])) for p_ in folk
              if w0 - P14_INSET_RUN <= p_[1] <= w1 + P14_INSET_RUN]
        c_ += stb
        for key, s, h, cw in P14_PLANTS:
            if h <= z1 - z0 and w0 - cw <= s <= w1 + cw:
                z = _p14_surf(s)
                c_.append((u"%s at %.1f m" % (key, s), (s - cw / 2.0, z, s + cw / 2.0, z + h)))
        return c_

    def _ncut(w_):
        n_ = 0
        for _nm, b_ in _chk(*w_):
            if not (b_[0] >= w_[0] and b_[2] <= w_[2] and b_[1] >= w_[1] and b_[3] <= w_[3]) and \
                    not (b_[2] <= w_[0] or b_[0] >= w_[2] or b_[3] <= w_[1] or b_[1] >= w_[3]):
                n_ += 1
        return n_

    # v15.2 (2 Nov run, U16 "cut by the frame"; v16: ported from dist to src, wb_drift.diff): when the frame cuts a
    # person, street element or plant, the window is shifted along the section (and in level) at its own size, then
    # at the most P14_INSET_BOX allows at the SAME den, to the nearest place where nothing is cut and every focus box
    # stays inside; else the least cut place
    wn = fr["window"]
    n_best = _ncut(wn)
    if n_best:
        ux0, uz0 = min(f_[0] for f_ in focus), min(f_[1] for f_ in focus)
        ux1, uz1 = max(f_[2] for f_ in focus), max(f_[3] for f_ in focus)
        cx, cz = 0.5 * (wn[0] + wn[2]), 0.5 * (wn[1] + wn[3])
        best = None
        for ww, wh in ((wn[2] - wn[0], wn[3] - wn[1]),
                       (P14_INSET_BOX[0] * den / 1000.0, P14_INSET_BOX[1] * den / 1000.0)):
            if ww < ux1 - ux0 - 1e-6 or wh < uz1 - uz0 - 1e-6:
                continue
            nx, nz = int((ww - (ux1 - ux0)) / 0.1), int((wh - (uz1 - uz0)) / 0.1)
            for ix in range(nx + 1):
                for iz in range(nz + 1):
                    x0_, z0_ = ux1 - ww + 0.1 * ix, uz1 - wh + 0.1 * iz
                    w_ = (x0_, z0_, x0_ + ww, z0_ + wh)
                    n_ = _ncut(w_)
                    d_ = abs(x0_ + 0.5 * ww - cx) + abs(z0_ + 0.5 * wh - cz)
                    if best is None or (n_, d_) < best[:2]:
                        best = (n_, d_, w_)
            if best and best[0] == 0:
                break
        if best and best[0] < n_best:
            if log is not None:
                log.append(u"inset {} {}: window moved {:.1f}-{:.1f} m -> {:.1f}-{:.1f} m (1:{:,.0f} kept): {} cut "
                           u"-> {}".format(page, words, wn[0], wn[2], best[2][0], best[2][2], den, n_best, best[0]))
            fr["window"] = best[2]
    w0, z0, w1, z1 = fr["window"]
    chk = _chk(w0, z0, w1, z1)
    cut = sf_inset_cut_check(fr["window"], chk, page=page, label=words)
    wc, hc = (w1 - w0) * kc, (z1 - z0) * kc
    xa = at[0] - wc if (at[2:] or ("L",))[0] == "R" else at[0]
    bbc = (xa, at[1] - hc, xa + wc, at[1])
    r0, r1 = w0 - P14_INSET_RUN, w1 + P14_INSET_RUN
    sp = Page(0, 0)
    _p14_cut(sp, xa - (w0 - r0) * kc, bbc[1] - (z0 - G["base"]) * kc, kc, (r0, r1), sea, P14_SEA_MONTH[sea],
             style=style, water=water, back=False, page=page)
    n0 = wbx_mark(pg)
    pg.items += _p14_clip_items(sp.items, bbc)
    did = u"%s_inset" % parent
    wbx_drawing(did, page, pg, bbc, n0=n0, den=den, origin=(w0, z0), dkind="section", scale_pref=[int(den)],
                title=u"Zoomed in · " + words, group=group or parent, crop=crop)
    wbx_inset(page, parent, (X(w0), Y(z0), X(w1), Y(z1)), did)
    if log is not None:
        log.append(u"inset {} {}: {} -> {} at 1:{:,.0f} (cut 1:{:,.0f}), window {:.1f}-{:.1f} m x {:+.2f}-{:+.2f}, "
                   u"about {} people + {} street elements, cut by the frame: {}".format(
                       page, words, parent, did, den, parent_den, w0, w1, z0, z1, len(near[:P14_INSET_N]),
                       len(focus) - len(near[:P14_INSET_N]), u", ".join(cut) if cut else u"none"))
    return did


def _p14_sf_log(log, *heads):
    """section_frame.py's log lines that start with one of heads, once each"""
    if log is None:
        return
    for ln in SF_LOG:
        if any(ln.startswith(h_) or ln.startswith(u"FLAG " + h_) for h_ in heads) and ln not in log:
            log.append(ln)


def _p14_g6(k, keys, log, what):
    """the G6 check of a drawing (section_frame.py): people true size at k, every plant inside its sourced range; one
    FLAG log line when something is off (M2.7)"""
    bad = sf_assert_g6(k, trees=[(p[0], p[2]) for p in keys], strict=False)
    if bad and log is not None:
        log.append(u"FLAG G6 {}: {}".format(what, u"; ".join(bad)))


def _p14_bridge_log(page, log):
    """S3 §4 (A15): the S4 cut sees no bridge within 500 m; br_section logs `bridge S4 <name|none>` (shapes not
    drawn: the cut's chainage here is m across from the bed's low point, not br_section's; a found bridge is a
    WARNING to draw it)"""
    try:
        out = br_section("S4", look=1, page=page)
    except Exception as ex:
        if log is not None:
            log.append(u"FLAG bridge S4 ({}): br_section failed: {}: {}".format(page, type(ex).__name__, ex))
        return
    if out.get("found"):
        wbx_warn(page, "bridge", u"S4 sees %s: not drawn on this page" % u", ".join(
            u"%s" % f_.get("name") for f_ in out["found"]))
    if log is not None:
        for ln in BR_LOG[-1:]:
            if ln not in log:
                log.append(ln)


# ---------------------------------------------------------------- p.15
P15_KEY = (126.0, 36.0)              # v16 (G6-5, frames_p14-22 "SON page16 -> new page 14": key map x1.25 at
#                                      [3,11 30x12]): the most room km_keymap is offered, mm; nothing drawn on the board
P15_BAND_HUE = {"A": ("WAT", 3), "B": ("GRN", 1), "C": ("GRN", 2), "D": ("GRN", 3), "E": ("GRN", 4),
                "F": ("CTX", 4)}     # v16 (G6-6, hues H1 "The S4 cut, north-east bank"): the planting bands A-F from
#                                      the hue table (A the summer strip WAT r3; B-E wet -> dry GRN r1-r4; F CTX r4),
#                                      replacing code.py BAND_COL on this page


def _p15_band_col(c_):
    """v16 (G6-6): a planting band's fill (P15_BAND_HUE) and the ink of its letter on it (white on GRN r1 / r2)"""
    code, rank = P15_BAND_HUE[c_]
    return hue(code, rank), (COL["white"] if code == "GRN" and rank <= 2 else COL["ink_dark"])
P15_ZOOM_DEN = 100.0                 # round 4 (G-R4-5.7, D11): p.15's inset at 1:100 (round 5: sf_inset_frame picks it)
P15_INSET_M = (5.0, 2.2)             # its spot over the bike lane, m across x m high (drawing rule): 50 x 22 mm
P15_BAND_H = 33.0                    # mm over the cut for its inset and key map (the inset 22 mm + caption + bar)
P15_LEVEL_W = 33.0                   # mm right of the cut for its level marks (inside the block's drawing column)
P15_SIDE_W = 104.0                   # mm, the block's side column (key lists)
P15_TITLE_BLK = u"THE BANK · summer, the stream at its average flow"   # round 5: the booklet prints the scale
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
P15_BAND_SRC = (u"Rijkswaterstaat (2023). Hydrologische randvoorwaarden van de ecotopen in PAGW rivieren, memo, "
                u"pp. 8-16")
P15_LABEL_W = 78.0                   # the chart's label column, mm
P15_ROW_MIN = 3.4                    # mm, the least row of THE YEAR: two 7.5 pt labels one over the other stay 0.6 mm
#                                      apart (G-R4-1)


def _p15_days(code):
    if code == "A":
        return u"under water all year"
    lo, hi = BAND_DAYS[code]
    if lo <= 0.0:
        return u"under {:g} days a year".format(hi)
    return u"{:g}–{:g} days a year".format(lo, hi)


def _p15_year(pg, x0, ytop, x1, ybot, log=None, style="b", page=None, did=None):
    """THE YEAR ON ONE MONTH AXIS (R31's idea: a row of pictograms a user group, everyone's activities on one time
    axis; R03 / R05: intensity read from figures): the seasons as p.14 names them, the water (when the stream covers
    the bed, when the strip runs on stored water, when the gravel bed is open), who and when (one to three figures in
    each month = how busy, the group's tint behind; the Kermes week as a stall), the plants (each month a small drawing
    of the species in that month's state over its leaf and flower bars in its own colours, plants.py pla_colours,
    G-R4-6). Round 4 (P15.3): PLANTS is a title row of its own with its legend (neutral samples) in one text group;
    rows never under P15_ROW_MIN; no closing paragraph (G-R4-2). Fills x0..x1 from ytop down to ybot. Round 5 (S8):
    the PLANTS legend (in leaf, in flower, heads cut) and its note are booklet items of the drawing did on page
    (wbx_legend, wbx_text), not drawn on the board. Returns the bottom y."""
    fs = FS_MIN
    xa = x0 + P15_LABEL_W
    mw = (x1 - xa) / 12.0
    tx = x0 + 24.0

    def X(t):
        return xa + t * mw
    wet = _p14_cover_months()                 # round 3: the level wets at least P14_COVER of the surveyed bed floor
    water = [(u"stream covers the bed", "flood", wet, C["w2"]),
             (u"strip runs on stored water", "strip", [m for m in range(12) if m not in wet], "7FAFC0"),
             (u"gravel bed open to people", "hub_open", list(SUBHUB_OPEN), "D9C79A")]
    head_h = fs * 2.6 + 1.2
    blk = fs * 1.6
    nrow = len(water) + len(P15_USE) + len(P15_PLANT_ROWS)
    rh = (ytop - ybot - head_h - 3 * blk) / nrow
    if rh < P15_ROW_MIN and log is not None:
        log.append(u"WARNING (D9): p.15 THE YEAR has {:.1f} mm a row, under {:.1f}: the pair needs more room".format(
            rh, P15_ROW_MIN))
        wn_orange(log[-1][8:])  # v15.1 (closing): this WARNING line also orange (one sink)
    rh = max(P15_ROW_MIN, min(6.5, rh))
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

    def bar(a_, b_, colour, frac, alpha=None):          # round 3: opaque, a lighter tone instead of see-through
        c_ = y[0] - rh / 2.0
        if alpha is not None:
            colour = r28_mix(colour, COL["white"], 1.0 - alpha)
        pg.poly([rect(X(a_) + 0.25, c_ - rh * frac / 2.0, X(b_) - 0.25, c_ + rh * frac / 2.0)], fill=colour)
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
                                 pen_min_mm=0.0))
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
                    shp_put(pg, fig_side(pose, xx, yf, kf, facing=1 if (m + j) % 2 else -1, style=style,
                                         pick=m * 3 + j))   # round 4: the one people set (pen_black)
        y[0] -= rh
    title(u"PLANTS")                                              # P15.3: PLANTS, its own title row
    if page is not None and did is not None:                      # round 5: its legend and note go to the booklet
        def cell_sw(st_):
            return lambda pg_, x_, y_, w_, h_: _p14_cell(pg_, x_, y_, x_ + w_, y_ + h_, st_)
        wbx_legend(page, did, [(cell_sw(st), word) for st, word in (("leaf", u"in leaf"), ("bloom", u"in flower"),
                                                                     ("cut", u"heads cut"))],
                   title=u"PLANTS", id=u"%s_plants" % did)
        wbx_text(page, u"bars in each species' own colours · each month: the plant as it is then", "note", did=did,
                 group=did)
    for key in P15_PLANT_ROWS:
        h, cw = _p14_size(key)
        kk = (rh - 0.8) / max(h, cw)
        shp_put(pg, _p14_plant(key, tx + (rh - 0.6) / 2.0, y[0] - rh + 0.4, kk, None, h, cw, 0, style))
        label(_p14_name(key, log))
        mo = pla_months(key)
        bcol = _p14_bloom_col(key)
        for a_, b_ in occ_spans([m - 1 for m in mo["leaf"]]):
            bar(a_, b_, pla_colours(key)["fill"], 0.3, 0.45)
        for a_, b_ in occ_spans([m - 1 for m in mo["bloom"] if m not in mo["cut"]]):
            bar(a_, b_, bcol, 0.62, 0.45)
        for m in mo["cut"]:
            c_ = y[0] - rh / 2.0
            _p14_cell(pg, X(m - 1) + 0.25, c_ - rh * 0.31, X(m) - 0.25, c_ + rh * 0.31, "cut", bcol)
        km = (rh - 0.9) / max(h, cw)
        for m in range(12):
            if _p14_state(key, m + 1):
                shp_put(pg, _p14_plant(key, X(m + 0.5), y[0] - rh + 0.45, km, m + 1, h, cw, m, style))
        y[0] -= rh
    return y[0]


P15_WHY = [  # the north-east bank's parts and why each is there (G10; our design), numbered on the cut as p.14's zones
    # (round 4: the same number and colour, P15_ZONE): (zone of _p14_geo, words; {open} = the months the gravel bed is
    # open, from SUBHUB_OPEN)
    ("gravel", u"gravel bed: the stream's, open to walk {open}"),
    ("strip", u"summer strip: holds stored water, wading when the stream is low"),
    ("toe", u"riparian edge: willow, tamarisk and rushes clean the water and hold the bank"),
    ("market", u"flood terrace: the Kermes market ground, under water only in a flood"),
    ("walk", u"lower walk: floodable, closed by a bollard in a flood"),
    ("steps", u"seat steps: sit and watch the water; a flood rises up them"),
    ("prom", u"promenade: over Q500, dry in every flood; a bench and lamps"),
    ("bike", u"bike lane: over Q500, apart from the walkers; a bike rack"),
]
P15_ZONE = {"gravel": "open"}        # a p.15 part shown with the p.14 zone it belongs to (number and colour)
P15_GROUP_MARK = "3C4733"            # the planting groups' letters: rings in the planting's dark green (drawing rule)


def _p15_open():
    """the months the gravel bed is open (SUBHUB_OPEN) as "Jun-Oct", or the months listed"""
    ms = sorted(SUBHUB_OPEN)
    if not ms:
        return u""
    if ms == list(range(ms[0], ms[-1] + 1)):
        return u"{}–{}".format(MONTHS[ms[0]], MONTHS[ms[-1]]) if len(ms) > 1 else MONTHS[ms[0]]
    return u", ".join(MONTHS[m] for m in ms)


def _p15_num(zone):
    """the p.14 number (1-11) and colour of a p.15 part"""
    z_ = P15_ZONE.get(zone, zone)
    n = [q[0] for q in P14_ZONE_KEY].index(z_) + 1
    return n, P14_ZONE_COL[z_]


def _p15_list(pg, x, y, w, head, rows, style="solid"):
    """a numbered or lettered key in the side column from y down: the bold head, then each row's marker (mk_marker,
    its own colour) and its words wrapped beside it (one text group a row). rows = [(glyph, colour, words)].
    Returns the bottom y"""
    fs = FS_MIN
    old = pg.tg
    pg.text(head, x, y - fs, fs, COL["ink_dark"], bold=True)
    y -= fs * 1.6
    rr = P14_MARK_R + 0.15
    tx = x + 2.0 * rr + 1.0
    for g_, col, words in rows:
        lines = wrap(words, fs, w - (tx - x))
        cy = y - rr
        _p14_mark(pg, x + rr, cy, g_, col, style=style)
        pg.tgroup()
        for j, ln in enumerate(lines):
            pg.text(ln, tx, cy - fs * 0.35 - j * fs * 1.25, fs, COL["ink"])
        pg.tg = old
        y -= max(2.0 * rr + 0.8, (len(lines) - 1) * fs * 1.25 + rr + fs * 0.35 + fs * 0.3 + 0.8)
    return y


def _p15_bands_key(pg, x, y, w):
    """the planting bands A-F with their days under water (the p.20 ladder, D9 a), from y down; returns the bottom"""
    fs = FS_MIN
    pg.text(u"PLANTING BANDS UNDER THE CUT · days under water " + cite(P15_BAND_SRC), x, y - fs, fs, COL["ink_dark"],
            bold=True)
    y -= fs * 1.6
    bn = dict((b_[0], b_[1]) for b_ in PLANT_BANDS)
    bn["A"] = u"summer strip"
    for c_ in ("A", "B", "C", "D", "E", "F"):
        yl = y - fs
        pg.poly([rect(x, yl - 0.4, x + 3.2, yl + fs * 0.85)], fill=_p15_band_col(c_)[0])
        old = pg.tg
        pg.tgroup()
        pg.text(c_, x + 1.6, yl, fs, COL["ink_dark"], bold=True, align="C")
        pg.text(u"{} · {}".format(bn[c_], _p15_days(c_)), x + 4.2, yl, fs, COL["ink"])
        pg.tg = old
        y -= fs * 1.45
    return y


def _p15_side(pg, x, ytop, w, parts, groups):
    """the block's side column (G-R4-3 LEFT, G-R4-5.5): the parts in number order, the planting groups by letter, the
    planting bands; returns the bottom y"""
    y = _p15_list(pg, x, ytop, w, u"THE BANK, PART BY PART · why each is there", parts)
    if groups:
        y = _p15_list(pg, x, y - 3.0, w, u"PLANTING, GROUP BY GROUP · what each does", groups, style="ring")
    return _p15_bands_key(pg, x, y - 3.0, w)


def _p15_panel(pg, box, log, style):
    """booklet p16 (the code's p.15; round 5, S8): drawn into box on the board as a recorder and handed to the
    booklet as items (WBX_PG_NE, every drawing crop="wb_s4_ne"): the bank in summer at 1:250 ("p16_section": x = m
    across S4 from the bed's low point, y = m a.s.l.; scale_pref = the Bergama list from 1:200 to 1:500, so the
    booklet takes the scale that fills the block, P16.1): the surveyed bed, the stream at the registry's average flow
    with Q100 / Q500 (M5), the summer strip full (N2 a), the trees beyond (R16) and the cut's trees at the page's level
    (sf_tree_level), the planting and its low layer in summer, the people and Kermes stalls at true size, the street
    elements, the surveyed bank today dashed, its parts numbered on their surface as p15's zones, its planting groups
    lettered on their crowns, the lettered planting-band strip under it (P16.4: the zone-width row is gone); its
    levels as booklet levels (P16.3); its inset v2 over the promenade and bike lane ("p16_section_inset", P16.2); the
    parts and groups as booklet lists anchored on their marks, the bands as a legend, the title a heading; the key map
    km_keymap v3 (wbx_keymap, G6-5); then the year on one month axis ("p16_year", a diagram). Returns its bbox."""
    x0, y0, x1, y1 = box
    n0 = len(pg.items)
    page = WBX_PG_NE
    crop = "wb_s4_ne"
    G = _p14_geo(log)
    k = 1000.0 / P15_DEN
    s0, s1 = P15_RANGE
    ws = (s1 - s0) * k
    zn = G["zones"]
    tl = sf_tree_level(page)
    sc_t = fig_depth(tl["layer"])[0] if tl["layer"] else 1.0     # the cut's trees at the page's level
    # what the lists name (numbers as p15's zones, groups lettered on their tallest plant)
    parts = []
    for zone, words in P15_WHY:
        a, b = max(zn[zone][0], s0), min(zn[zone][1], s1)
        if b - a >= 1.4:
            n, col = _p15_num(zone)
            parts.append((n, col, words.format(open=_p15_open()), (a + b) / 2.0))
    parts.sort(key=lambda p_: p_[0])
    groups = []
    for a, b, ks, tags in P14_GROUPS:
        inside = [p_ for p_ in P14_PLANTS if a - 0.01 <= p_[1] <= b + 0.01 and s0 + 0.5 <= p_[1] <= s1 - 0.5]
        if not inside:
            continue
        key, s, h, _cw = max(inside, key=lambda p_: p_[2])
        sc_ = sc_t if PLA_SPECIES[key]["layer"] == "tree" else 1.0
        do = globals().get("P12_GROUP_DO") or {}
        groups.append([s, _p14_surf(s) + h * sc_ * 0.6, u" + ".join(_p14_name(k_, log) for k_ in ks) +
                       (u": " + u", ".join(do.get(t_, t_) for t_ in tags) if tags else u"")])
    groups.sort(key=lambda g_: (-round(g_[1] / 2.0), g_[0]))    # reading order: top row first, left to right
    letters = u"abcdefghijklmn"
    grows = [(letters[j % len(letters)], P15_GROUP_MARK, g_[2]) for j, g_ in enumerate(groups)]
    # the block: its height = the taller of the drawing column and the side column (board layout only)
    ztop = max([_p14_surf(s) + h * (sc_t if PLA_SPECIES[key_]["layer"] == "tree" else 1.0)
                for key_, s, h, _ in P14_PLANTS if s0 <= s <= s1] + [P14_PROM + 2.0])
    h_cut = (ztop - G["base"]) * k + 2.0
    under = 1.4 + 3.0 + 1.0                       # the band strip under the cut (round 5: no width row, no bar)
    h_draw = BLK_TITLE_H + P15_BAND_H + h_cut + under
    probe = Page(0, 0)
    h_side = BLK_TITLE_H + (y1 - _p15_side(probe, 0.0, y1, P15_SIDE_W, [(n, c, t) for n, c, t, _s in parts], grows))
    blk = blk_section(x0, y1, x1 - x0, max(h_draw, h_side), P15_TITLE_BLK, side_w=P15_SIDE_W, mode="LEFT",
                      y_down=False)
    d = blk["drawing"]
    _p14_keymap(page, P15_KEY, u"p16_keymap", log)       # v16 (G6-5): km_keymap, S4 only
    _P14_TREES.pop(page, None)
    ytc = d[3] - P15_BAND_H
    yb = ytc - h_cut
    nc = wbx_mark(pg)
    # v16 (round 6, S5): booklet p14's S4 cut, north-east bank, 1:250 + its zoom: ACCURATE language (BRIEF §3, PLAN
    # §2.3, r06_S03 traits: true scale, library people and seasonal plant images, light soil, no hatch, ▽ levels at the
    # right edge spread, no horizontal dimension row: none is drawn since round 5, G-R5-4.6); content as before
    _p14_grp(pg, "other", u"sky")
    shp_put(pg, sf_sky(x0, x0 + ws, yb, ytc, seed=7, cid=u"S4-ne"))   # D8 / G15: its own sky
    _p14_grp(pg)
    sp = Page(0, 0)
    _p14_houses(P15_RANGE, log)                  # checklist 7: the houses behind the cut, logged once
    X, Y = _p14_cut(sp, x0, yb, k, P15_RANGE, "summer", P14_SEA_MONTH["summer"], style=style, water="avg", ytop=ytc,
                    page=page)
    fr = (x0, yb, x0 + ws, ytc)
    top = max(_p14_bb(sp.items)[3], fr[3])       # v17 (L4, Aras 4 Nov 19:17): a crown over the frame is drawn
    pg.items += _p14_clip_items(sp.items, (fr[0], fr[1], fr[2], top + 0.05))   # whole; the drawing's box grows
    _p14_grp(pg, "ground", u"S4 bank today (surveyed)")
    pg.line([(X(s), Y(z)) for s, z in G["today"] if s <= s1], COL["ink2"], 0.2, dash=[1.0, 0.6])
    _p14_grp(pg, "annotations", u"parts and planting groups")
    # the parts' numbers on their surface (G-R4-5.6), the groups' letters on their crowns (G-R4-7)
    rr = P14_MARK_R + 0.15
    taken, part_at, group_at = [], [], []
    for n, col, _t, sm in parts:
        cx, cy = X(sm), Y(_p14_surf(sm))
        taken.append((cx, cy))
        part_at.append((cx, cy))
        _p14_mark(pg, cx, cy, n, col)
    for g_, (gl, gc, _t) in zip(groups, grows):
        cx, cy = X(g_[0]), Y(g_[1])
        for _i in range(4):
            if all(math.hypot(cx - qx, cy - qy) >= 2.0 * rr + 0.7 for qx, qy in taken):
                break
            cy += 2.0 * rr + 0.7
        taken.append((cx, cy))
        group_at.append((cx, cy))
        _p14_mark(pg, cx, cy, gl, gc, style="ring")
    # the planting bands along the cut (where water reaches the ground how often): the lettered strip stays (P16.4)
    fs = FS_MIN
    yt_b, hb = yb - 1.4, 3.0
    runs, s, step = [], s0, 0.1
    while s < s1 - 1e-9:
        c_ = _p14_band_code(s + step / 2.0, _p14_surf(s + step / 2.0))
        if runs and runs[-1][0] == c_:
            runs[-1][2] = s + step
        else:
            runs.append([c_, s, s + step])
        s += step
    for c_, a, b in runs:
        fc_, ic_ = _p15_band_col(c_)
        _p14_grp(pg, "annotations", u"planting band %s" % c_)
        pg.poly([rect(X(a), yt_b - hb, X(min(b, s1)), yt_b)], fill=fc_)
        if X(b) - X(a) > 3.0:
            pg.text(c_, (X(a) + X(b)) / 2.0, yt_b - hb + 0.55, fs, ic_, bold=True, align="C")
    _p14_grp(pg)
    did = u"p16_section"
    bbs = (x0, yt_b - hb - 0.5, x0 + ws, max(ytc, top + 0.3))   # v17 (L4): holds the whole cut
    wbx_drawing(did, page, pg, bbs, n0=nc, den=P15_DEN, origin=(s0, G["base"] + (bbs[1] - yb) / k),
                dkind="section", scale_pref=[d_ for d_ in SF_SCALES if d_ <= P14_DEN], group=did, crop=crop)
    wbx_text(page, P15_TITLE_BLK, "heading", did=did, group=did)
    _p14_levels_out(page, did, _p15_level_rows())
    _p14_level_spread(page, did, _p15_level_rows(), Y, ytc, log)
    if log is not None:
        log.append(u"section {} S4 ACCURATE (north-east bank, 1:{:,.0f}, zoom {})".format(wbx_p(page), P15_DEN,
                                                                                         did + u"_inset"))
    # the lists beside it: booklet lists anchored on their marks, the bands a legend (nothing drawn on the board)
    wbx_text(page, u"THE BANK, PART BY PART · why each is there", "heading", did=did, group=did)
    wbx_list(page, did, [u"{} {}".format(n, t) for n, _c, t, _s in parts], numbered=False, anchors_board=part_at,
             id=u"p16_parts")
    if grows:
        wbx_text(page, u"PLANTING, GROUP BY GROUP · what each does", "heading", did=did, group=did)
        wbx_list(page, did, [u"{} {}".format(gl, t) for gl, _c, t in grows], numbered=False,
                 anchors_board=group_at, id=u"p16_groups")
    bn = dict((b_[0], b_[1]) for b_ in PLANT_BANDS)
    bn["A"] = u"summer strip"
    wbx_legend(page, did, [(wbx_sw("fill", _p15_band_col(c_)[0]), u"{} · {} · {}".format(c_, bn[c_], _p15_days(c_)))
                           for c_ in ("A", "B", "C", "D", "E", "F")],
               title=u"PLANTING BANDS UNDER THE CUT · days under water " + cite(P15_BAND_SRC), id=u"p16_bands")
    # the inset v2 (P16.2): the promenade and bike lane, framed on its people and street elements, at its own k
    ins = _p14_inset2(pg, page, did, X, Y, P15_DEN, "summer", "bike", u"promenade and bike lane",
                      (x1 - 2.0, y1 - 2.0, "R"), water="avg", sm=zn["bike"][0], style=style, log=log, crop=crop,
                      group=did)
    # the year on one month axis: a diagram of its own
    yid = u"p16_year"
    ny = wbx_mark(pg)
    ytop = d[1] - 4.0
    ybot = _p15_year(pg, x0, ytop, x1, y0, log, style, page=page, did=yid)
    wbx_drawing(yid, page, pg, (x0, min(ybot, ytop - 1.0), x1, ytop), n0=ny, dkind="diagram",
                title=u"THE YEAR ON ONE MONTH AXIS", group=yid, crop=crop)
    bb = _p14_bb(pg.items[n0:])
    if log is not None:
        if G["src"] not in log:
            log.append(G["src"])
        for ln in wat_draw_order_lines(page=u"p16", steps=P14_STEPS_LOG):
            if ln not in log:
                log.append(ln)
        _p14_sf_log(log, u"inset " + page, u"levels " + page)
        _p14_g6(k, [p for p in P14_PLANTS if s0 <= p[1] <= s1], log, u"p16 cut")
        _p14_hue_log(page, log)
        log.append(u"trees {} species={} generic=0 (proposed planting, designed species; no survey tree on the "
                   u"cut)".format(wbx_p(page), _P14_TREES.get(page, 0)))
        log.append(u"p16 S4 north-east bank board 1:{:,.0f} (booklet picks 1:200-1:500), inset {}, trees layer {}, "
                   u"panel {:.0f} x {:.0f} mm{}".format(
                       P15_DEN, ins or u"not drawn", tl["layer"], bb[2] - bb[0], bb[3] - bb[1],
                       u"" if bb[1] >= y0 - 0.5 else u" (FLAG: {:.1f} mm below the cell)".format(y0 - bb[1])))
    return bb


def _p15_level_rows():
    """p.15's levels (DATA-1, G-R4-5.4), marked outside the cut's frame: the strip floor, the bed (strip full), the
    average flow, the flood terrace, the bank today, Q100, Q500, the promenade"""
    G = _p14_geo()
    rows = _p14_level_rows("summer", avg=True)
    return rows + [(u"flood terrace", G["shelf"]), (u"bank today", G["ne_top"]), (u"promenade", P14_PROM)]


def p15_page(pg, box, opt, log):
    """the code's p.15 = booklet p16, the north-east bank of S4, drawn into box (x0, y0, x1, y1), page mm, and handed
    to the booklet as items (WBX_PG_NE). Returns its crop as before (the drawings registered with crop="wb_s4_ne"
    replace it in the export)."""
    tri = sf_triangles(walls=False, aggregate=False)          # G14 / U22: no meaningless triangles in the cut
    try:
        bb = _p15_panel(pg, box, log, "a")   # lead: style a, as p11, p12, p17 (Aras 31 Oct 08:46)
    finally:
        sf_triangles(**tri)
    _p14_bridge_log(WBX_PG_NE, log)
    if log is not None:
        extra = []                                            # round 5 done-when lines (S3 / S4), once each
        for fn_ in ("sf_people_line", "pla_log_lines", "fig_set_line"):
            f_ = globals().get(fn_)
            try:
                r_ = f_(False) if fn_ == "fig_set_line" else (f_() if f_ else None)
            except Exception:
                r_ = None
            extra += list(r_) if isinstance(r_, (list, tuple)) else ([r_] if r_ else [])
        for ln in (cut_log_line(), sf_g14_line()) + tuple(PLA_LOG) + tuple(extra):
            if ln and ln not in log:
                log.append(ln)
    return [("wb_s4_ne", bb, P15_DEN)]
