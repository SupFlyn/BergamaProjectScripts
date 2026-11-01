# ================================================================ v10 the four proposal sections, true to the cut
# v10 (revision 29 Oct, WO-T3b-3; package C "Page 13", brief 02 §3-§6): the sketches are gone. Each section is drawn
# at 1:500 on the booklet page from the level table (common/levels.py: bed, bed width, bank and wall tops, bank type
# and angle, terraces, Q100, Q500) with the shared section parts (DSİ walls, embankments, loose earth, railings,
# stone / concrete / earth / gravel hatches, steps seated into the bank) and the plants module (every species at its
# true size and form; D6: no fig, citrus, iris, oleander, white poplar; D2: common reed only in lined basins the flood
# passes by). Figures through ps_fig / ps_zones (M7, revision 30 Oct; R2-C). All four sections
# look downstream: the NE bank (left bank) on the left, the SW bank on the right, as the key map's triangles show.
# Drawn in booklet print mm (k = PS_K mm per m); build_sheet() places the block on the A0 sheet at 1 / BK_S.
# Revision 30 Oct (T6, booklet p12): people are the M7 figures at 1.75 m (D9 layer 0 at the cut), plants the M6
# species at their sourced heights in mixed, wet-to-dry scatters (G9), checked by sf_assert_g6 (G6); the water is the
# M5 section (average yearly flow, never dry; Q100 / Q500 from the cut registry); every bank is a designed place with
# its reason (G10): walks, bike lanes, a stair down the W1 wall into the bed, life in the wet bed, the W4 ramp to a
# viewing terrace and the boardwalk; faded trees behind the cut (R16). Each section is drawn in style "b" (vector)
# and "a" (cutouts, D1) from the same geometry (PsSec.style).
# Round 2 (R2-C, 31 Oct, PG3 p12 #6-#7): people only by zone (fig_place_zones, R2-A): in the water only on stepping
# stones (no wading figures: they are the one drawn pose left), passing the average-flow water so nobody stands in a
# water-filled channel; far people and plants on depth layers 1 / 2; planting in mixed groups (pla_group_section),
# emergent species only where the ground is under water; the trees behind the cut stand on their own layer's ground
# (the cut line incl. the bed, none on the water) under the D8 sky; every item seated (G14, log line); the Q500 wash
# around people is gone (Q100 / Q500 stay lines); every label is a numbered callout "Element: reason" (SfCallouts)
# with its key under the drawing; the section triangles are switched off (U22).
# R2-C pass 2 (Aras 31 Oct 12:01): W1 redrawn to p.17's F1 layout (path and bike lane under the SW trees, view
# terrace on the NE wall top, reed basins beyond) with sitting steps, landings and planted pockets as the way down (no
# straight stair, no blocks in the bed); background houses from the basemap on every depth layer (ps_back); people
# as scenes looking at the water (ps_zones focus).
# v16 (round 3, booklet p12: P12.3-P12.5, G15, G16, DATA-1): each cut tells its scenario (title) and names its use
# zones under the drawing with a reason (R07, ps_zone_strip); people in front (new poses through FIG_ACTIVITY and
# water_edge zones), big trees on depth layer 1 (behind, paler: R05 / R06), street elements with a reason, a quiet sky
# per cut id with a few birds (D3), none of the back trees in the channel, one 1:200 zoom inset in the cut's own free
# sky (U29); cut ends W1 / W1' and the banks by place under the drawing (D6); the walled beds from the surveyed
# sections (water board data/CUTS.py), the summer strip on the survey low point (B2 finding, Aras ask 1 a).
# v17 (round 4, S7, P13.1 / D2): 1:250 on the booklet page, two cuts per page, one cut per full row (CHK-8); numbers
# (mk_marker) instead of callout circles, the words in a side column / strip, level marks outside, insets 1:100.
PS_SCALE = 250                      # 1:250 on the booklet page (standard scales, SCRIPT_STANDARD §8)
PS_K = 1000.0 / PS_SCALE              # print mm per m (k of section_parts and plants)
PS_DEPTH = 1.0                        # m of cut ground drawn under the bed (section_parts drawing rule)
PS_WALL_T = 0.60                      # m: DSİ wall thickness: no sourced value; the same 0.60 m as p.04-05 (site board P45_WALL_T_M, G2)
PS_RAIL_H = 1.10                      # m: railing height on the wall and bank tops: drawing value
PS_BASIN = dict(kerb_h=0.30, depth=1.10, media=0.80, kerb_t=0.15)   # W1 reed basin cell beyond the NE wall: the
#                                     same drawing values as p.17's F1 (water board P17_BASIN; no source)
PS_STRIP = (3.00, 0.40)               # m: the summer strip channel in the bed (proposal): width, depth
PS_FREEBOARD = 0.30                   # m: a dry proposed floor sits at least this far above Q500 (design rule)
PS_LBL = 7.0 * PT                     # print mm: labels, list, level marks (GRID_TYPE label 7 pt; v17)
PS_TTL = 10.0 * PT                    # section titles (GRID_TYPE heading 10 pt bold; v17)
PS_NOTE = 8.0 * PT                    # the scenario after a title
PS_TIMBER = SF_LANE["timber"]         # boardwalk timber: the same tone as the M8 terraces and lanes
PS_STAIR = (0.30, 0.18)               # m: tread, largest rise of the stairs drawn here (design rule)
PS_RAMP = 1.0 / 12.0                  # rise per run of the W4 ramp (design rule)
PS_TERRACE_W = 4.0                    # m: the W4 viewing terrace's width across the cut (design rule)
# W1 = p.17's F1 (Aras 31 Oct 12:01): the SW path and bike lane widths of p.17 (water board P14_PROM_W, same cut)
# and the way down into the walled bed as sitting steps with landings (design rules, not data)
PS_W1_LANES = (7.0, 3.0)              # m: SW path, SW bike lane (p.17 F1)
PS_W1_SIT = (0.80, 0.45)              # m: sitting step tread (sit, feet on the step below), largest riser (seat high)
PS_W1_FLIGHTS = 3                     # flights of sitting steps, a landing between two flights
PS_W1_LAND = 2.40                     # m: a landing: the way on at its front, a planted pocket at its back
PS_W1_POCKET = (1.20, 0.60)           # m: the planted pocket on a landing: width, soil depth
PS_W1_FLOOR_W = 1.60                  # m: the floor at the water's edge (on the DSİ wall foot, cut down to it)
PS_W1_FLOOR_UP = 0.25                 # m: that floor at least this far over the average-flow water (stays dry)
PS_RAIL_DROP = 0.50                   # m: a drop deeper than this gets a railing (design rule)
PS_STONE_UP = 0.15                    # m: stepping stone tops over the average-flow water (sf_stepping_stones default)
PS_WHY = {"shade": u"shade", "cleaning": u"clean the water", "perception": u"seasonal colour",
          "wind": u"cut the wind", "noise": u"cut street noise", "corridor": u"ecological corridor"}
PS_SHORT = {"plane": u"Plane", "ash": u"Ash", "willow": u"Willow", "olive": u"Olive", "tamarisk": u"Tamarisk",
            "chaste": u"Chaste tree", "rosemary": u"Rosemary", "lavender": u"Lavender", "loosestrife": u"Loosestrife",
            "soft_rush": u"Soft rush", "rush": u"Sharp rush", "stone_pine": u"Stone pine"}
# where each cut crosses the stream axis (survey m; the cut centres of the level table's W rows): the drawn span runs
# from it to the cut's two ends (level_ends), NE end on the left
PS_AXIS = {"W1": (29693.022, 32569.176), "W2": (29959.774, 32264.566), "W3": (30354.663, 31689.671),
           "W4": (30991.856, 31039.404)}
# (sheet key = the surveyed section's key in data/CUTS.py, cut id, number on the page, name, scenario in the title)
# v16 (G15): the scenario says what we offer at that spot and how it differs from the next cut; (G16) bridges by name
PS_CUTS = [("up", "W1", 1, u"Upstream entry",
            u"the quiet entry: sitting steps down into the walled bed, reed basins beyond the Kale side wall clean "
            u"stream water"),
           ("k4", "W2", 2, u"%s walking hub" % bridge_name("K4", short=True),
            u"the busy hub: a dry square in the planes' shade above Q500, seating steps down to the summer strip"),
           ("k5", "W3", 3, u"%s · Demeter's Garden" % bridge_name("K5", short=True),
            u"room for the stream: an open commons the floods may cover, the garden raised above Q500 behind it"),
           ("down", "W4", 4, u"Downstream reach",
            u"the wild edge: planting bands and a boardwalk by flood level, a step-free ramp to a viewing terrace")]
PS_SKY_OVER = 2.0                     # m of sky over the tallest back crown (drawing rule: room for the birds)
PS_INSET_SCALE = 100                  # v17 (G-R4-5.6, D11): the zoom inset's scale, 2.5 x the 1:250 parent
PS_INSET_K = 1000.0 / PS_INSET_SCALE  # its print mm per m
PS_FLAT_TOL = 0.20                    # m: a surveyed floor this level or better is drawn flat (drawing rule)
# v17 (CHK-8, design spec S7): at 1:250 W3 and W4 are cut on their SW side with a break mark like W2 (W3 keeps 10 m of
# Demeter's Garden with its tomato rows and café; W4 keeps 6 m of the cotton field behind the crest)
PS_BREAK = {"W2": ("SW", 50.0), "W3": ("SW", 50.0), "W4": ("SW", 38.0)}
# m of level ground drawn behind an embankment crest (default 3.0): W4 NE 8.0 for the crest walk, bike lane and tree
# corridor (the level table's survey source reads that crest "50.0 m out", about 8 m behind the angled crest)
PS_CREST_FLAT = {("W4", "NE"): 8.0}       # W2's SW land (flat street level to the cut end 80 m out) drawn to 50 m, broken


def ps_lv(z):
    return u"+%.2f" % z


def ps_put(pg, shapes):
    """house shapes of the shared modules -> page items: multi-ring polys here, everything else (poly, line, text,
    image) through M5 shp_put"""
    for s in shapes or []:
        if not s:
            continue
        if s[0] == "poly" and s[1] and isinstance(s[1][0][0], (list, tuple)):
            pg.poly(s[1], fill=s[2], stroke=s[3] if len(s) > 3 else None, lw=(s[4] if len(s) > 4 and s[4] else 0.1),
                    alpha=s[5] if len(s) > 5 else None)
        else:
            shp_put(pg, [s])


def ps_xform(items, s, dx, dy):
    """xform with the D1 a "image" items kept in their place in the drawing order"""
    out = []
    for it in items:
        if it[0] == "image":
            _, x, y, w, h, path, a, flip, clip = (tuple(it) + (None,) * 9)[:9]
            out.append(("image", dx + s * x, dy + s * y, w * s, h * s, path, a, flip,
                        (dx + s * clip[0], dy + s * clip[1], dx + s * clip[2], dy + s * clip[3]) if clip else None))
        else:
            out += xform([it], s, dx, dy)
    return out


def ps_bbox(items):
    """items_bbox with the image items' extents"""
    b = items_bbox([it for it in items if it[0] != "image"])
    ims = [it for it in items if it[0] == "image"]
    if not ims:
        return b
    xs = [it[1] for it in ims] + [it[1] + it[3] for it in ims]
    ys = [it[2] for it in ims] + [it[2] + it[4] for it in ims]
    if b == (0.0, 0.0, 0.0, 0.0) and len(ims) == len(items):
        return (min(xs), min(ys), max(xs), max(ys))
    return (min([b[0]] + xs), min([b[1]] + ys), max([b[2]] + xs), max([b[3]] + ys))


def ps_z_at(prof, u):
    """the level (m) of the cut line prof [(u, z)] at u (its highest where it is vertical)"""
    if u <= prof[0][0]:
        return prof[0][1]
    best = None
    for (ua, za), (ub, zb) in zip(prof[:-1], prof[1:]):
        if ua <= u <= ub:
            z = za if ub - ua < 1e-9 else za + (zb - za) * (u - ua) / (ub - ua)
            best = z if best is None else max(best, z)
    return best if best is not None else prof[-1][1]


class PsSec(object):
    """One section: its own page in print mm, (0, 0) = (left end u0, PS_DEPTH under the bed); u = m across the stream
    from the axis (NE negative), z = m a.s.l."""

    def __init__(self, cid, u0, u1, d, style="b"):
        self.cid, self.u0, self.u1, self.d = cid, float(u0), float(u1), d
        self.style = style                                    # D1: "b" vector, "a" cutouts, one geometry
        self.trees = []                                       # (key, x, h_m, crown_m) at the cut, for the G6 check
        self.bed = level(cid, "bed")
        self.z0 = self.bed - PS_DEPTH
        self.k = PS_K
        self.hw = level(cid, "bed_width_cm") / 200.0          # half the bed width (m), the bed centred on the axis
        self.pg = Page(0, 0)
        self.calls = []                                       # (text "Element: reason", u, z where its circle sits)
        self.notes = []                                       # log notes of this section (planting that did not fit)
        self.info = []                                        # other log lines of this section (background houses)
        self.prof = []                                        # the cut line (u, z), left to right, for the flood
        self.w = (self.u1 - self.u0) * self.k
        # v16: the bed from the survey (gb = level function of u between the walls, None = flat at the registry
        # bed), the summer strip's centre (u), the use zones named under the drawing (name, reason, ua, ub), the
        # boxes (page mm) of tall things the zoom inset keeps clear of, the inset's spot (ua, ub, za, zb, what)
        self.gb, self.st_c = None, 0.0
        self.zones, self.obst, self.inset = [], [], None
        self.y_top = None                                     # page y of the sky's top (ps_back)
        self.boxes = []                                       # drawn inset boxes (page mm), for the overlap test
        self.inset_busy = None                                # the inset with its label (page mm): callouts keep off
        self.page = None                                      # v17: the booklet page id ("p13a" / "p13b")
        self.marks, self.list = [], []                        # v17: numbers (x, y, n, colour), list (n, text, colour)

    def gbed(self, u):
        """the bed's level (m) at u: the survey profile, else the registry bed"""
        return self.gb(u) if self.gb else self.bed

    def zone(self, name, reason, ua, ub, kind="zone"):
        """a use zone over its span ua..ub (m); v17: numbered on its ground (ps_marks) and named in the side list,
        "Name · reason"; kind "zone" (designed) or "water" (bed, stones, wet edge) sets the number's colour"""
        self.zones.append((name, reason, min(ua, ub), max(ua, ub), kind))

    def X(self, u):
        return (u - self.u0) * self.k

    def Y(self, z):
        return (z - self.z0) * self.k

    def P(self, pts):
        return [(self.X(u), self.Y(z)) for u, z in pts]

    def U(self, x):
        return self.u0 + x / self.k

    def zf(self, f):
        """a level function of u (m) -> a page-y function of page x"""
        return lambda x: self.Y(f(self.U(x)))

    def put(self, shapes):
        ps_put(self.pg, shapes)

    def call(self, text, u, z, kind="built", key=None):
        """a numbered element "Element: reason": its number at (u, z) m (v17: mk_marker, ps_marks); kind "built"
        (street elements, today's wall: ink), "zone" (accent) or "plant" (key = its tallest species: that colour)"""
        self.calls.append((text, u, z, kind, key))


def ps_kind(cid, side):
    return (level_cut(cid).get(side) or {}).get("type")


def ps_extent(cid):
    """(u0, u1, {"NE": m, "SW": m} from the axis to each cut end): the cut's span, widened to show a whole bank
    (embankment crest + 3 m, wall + 4 m, loose earth crest + 4 m), W2's SW cut short (PS_BREAK)"""
    c = PS_AXIS[cid]
    d = dict((nm, math.hypot(p[0] - c[0], p[1] - c[1])) for p, nm in zip(level_ends(cid), level_end_labels(cid)))
    hw = level(cid, "bed_width_cm") / 200.0
    ext = {}
    for side in ("NE", "SW"):
        kind, e = ps_kind(cid, side), d[side]
        if kind == "dsi_wall":
            e = max(e, hw + PS_WALL_T + 4.0)
        elif kind == "embankment":
            h = level(cid, "top", side) - level(cid, "bed")
            e = max(e, hw + h / math.tan(math.radians(level(cid, "angle_deg", side))) + PS_CREST_FLAT.get((cid, side), 3.0))
        elif kind == "loose_earth":
            e = e + 4.0
        ext[side] = e
    br = PS_BREAK.get(cid)
    if br:
        ext[br[0]] = min(ext[br[0]], br[1])
    return -ext["NE"], ext["SW"], d


def ps_water_y(S):
    """the page y of the water at the average yearly flow (G8): wet ground under it takes only emergent plants and
    no people (fig_place_zones water=)"""
    return S.Y(level_avg_flow(S.cid))


def ps_gprof(S):
    """the cut line S.prof as a page polyline whose x only grows (a wall's two points 0.05 mm apart), so the G14
    seat helpers read it as a ground function: the bed included, the walls nearly vertical"""
    out = []
    for x, y in S.P(S.prof):
        if out and x <= out[-1][0]:
            x = out[-1][0] + 0.05
        out.append((x, y))
    return out


def ps_obst(S, x, gy, h_m, crown_m, layer=0):
    """v16: the box (page mm) of one drawn plant (x, seated on page y gy, its depth layer's size) for the zoom inset's
    free-sky search"""
    sc = fig_depth(layer)[0] if layer else 1.0
    hw_ = 0.55 * crown_m * S.k * sc
    S.obst.append((x - hw_, gy, x + hw_, gy + h_m * S.k * sc * 1.02, int(layer or 0)))   # v17: + its depth layer


def ps_survey(S, key, log):
    """v16 DATA-1 (B2 finding: the W1 surveyed bed slopes; Aras ask 1 a: survey bed, the summer strip on the survey
    low point): the cut's surveyed section from the water board's data/CUTS.py row `key` (ground every 1 m over the
    bed low point, u0 = its SW end, + toward the NE bank), used only when its bed and length match the level module
    (else FLAG, flat). Walled cuts: the bed between the DSİ walls follows the survey, the profile placed so both wall
    feet stand level (drawing rule: the survey predates the walls and the cut's axis is not the survey's stream
    lines; for W1 this lands within ~2 m of p.17's stream-line walls). Unwalled cuts: the banks stay the level table's,
    the bed flat at the registry bed (the survey floor's relief logged). In both, the strip moves onto the survey's
    lowest point inside the drawn bed. Sets S.gb, S.st_c."""
    c, hw = S.cid, S.hw
    row = next((r for r in CUTS if r.get("key") == key), None) if "CUTS" in globals() else None
    ln = level(c, "length_m")
    if not row or not row.get("ground") or row.get("bed") is None:
        log.append(u"FLAG p12 %s: no surveyed section (data/CUTS.py \"%s\"): bed flat at %s, strip on the axis" % (
            c, key, ps_lv(S.bed)))
        return
    g = [float(v) for v in row["ground"]]
    if abs(float(row["bed"]) - S.bed) > 0.005 or (ln and abs(len(g) - 1 - ln) > 1.0):
        log.append(u"FLAG p12 %s: data/CUTS.py \"%s\" (bed %s, %d m) does not match the level module (bed %s, %s m): "
                   u"bed flat, strip on the axis" % (c, key, row["bed"], len(g) - 1, ps_lv(S.bed), ln))
        return
    u0 = float(row["u0"])

    def gz(uc):                                                # m over the bed at survey u (+ toward NE)
        t = max(0.0, min(len(g) - 1.0, uc - u0))
        i = min(len(g) - 2, int(t))
        return g[i] + (g[i + 1] - g[i]) * (t - i)
    walled = ps_kind(c, "NE") == "dsi_wall" and ps_kind(c, "SW") == "dsi_wall"
    cc = 0.0                                                   # survey u that sits on the drawn axis
    if walled:
        cand = [u0 + hw + 0.1 * i for i in range(int(max(0.0, (len(g) - 1) - 2.0 * hw) / 0.1) + 1)]
        if cand:
            cc = min(cand, key=lambda q: (round(abs(gz(q + hw) - gz(q - hw)), 2), abs(q)))
        S.gb = lambda u, _c=cc: S.bed + gz(_c - u)             # drawn u (NE negative) -> survey u (NE positive)
    us = [-hw + 0.25 * i for i in range(int(2.0 * hw / 0.25) + 1)]
    zs = [gz(cc - u) for u in us]
    low = us[zs.index(min(zs))]
    half = PS_STRIP[0] / 2.0
    S.st_c = max(-hw + 0.3 + half, min(hw - 0.3 - half, low))
    if walled:
        log.append(u"p12 %s: bed between the DSİ walls from the surveyed section (data/CUTS.py \"%s\", bed %s, every "
                   u"1 m), placed with both wall feet at +%.2f m over the low point (%.1f m off the cut axis); "
                   u"summer strip moved onto the survey low point at u %.1f m" % (
                       c, key, ps_lv(S.bed), gz(cc + hw), cc, S.st_c))
    else:
        fl = [z for z in zs if z <= 0.5]                       # the survey floor (the TIN floor rule: within 0.5 m)
        rel = (max(fl) - min(fl)) if fl else max(zs) - min(zs)
        log.append(u"%sp12 %s: survey floor level within %.2f m (data/CUTS.py \"%s\"): bed drawn flat at %s; summer "
                   u"strip moved onto the survey low point at u %.1f m" % (
                       u"FLAG " if rel > PS_FLAT_TOL else u"", c, rel, key, ps_lv(S.bed), S.st_c))


def ps_fig(S, pose, u, z, facing=1, **p):
    """one person at the cut on dry land only (M7: adult 1.75 m, D9 layer 0), feet at (u, z) seated on the ground
    (G14 sf_seat_x); people near the channel go through ps_zones, never here"""
    x = S.X(u)
    y = sf_seat_x(S.Y(z), x, FIG_FOOT_HALF_M * S.k)
    S.put(fig_side(pose, x, y, S.k, facing=facing, style=S.style, **p))


def ps_zones(S, zones, seed, layer=0, density=1.0, max_n=None, focus=0.0, **p):
    """G10 people zone by zone (figures.py fig_place_zones): zones [(kind, ua, ub, ground)] with ground = a level
    (m) or a function of u (m) -> level; kinds walkway, bike_lane, viewing_terrace, sun_steps, stepping_stones, lawn
    take people, "water" none (counted in the G14 line). The average-flow water is passed, so nobody stands where
    the drawn water covers the ground; layer 1 / 2 = people further from the cut (smaller, paler). Scenes (R2-C pass
    2, Aras 31 Oct 12:01 "they look like they are just put there"): focus = u (m) that everyone who stays looks at
    (default 0.0 = the water's middle on the axis; a stall or a view where the section has one), children playing
    turn to each other, walkers and riders keep their way; p goes to every figure (seat_h ...)."""
    zz = []
    for kind, ua, ub, g in zones:
        zz.append((kind, S.X(min(ua, ub)), S.X(max(ua, ub)), S.zf(g) if callable(g) else S.Y(g)))
    sh, placed = fig_place_zones(zz, S.Y(S.bed), S.k, seed=seed, layer=layer, style=S.style, density=density,
                                 water=ps_water_y(S), max_per_zone=max_n,
                                 focus=None if focus is None else S.X(focus), **p)
    S.put(sh)
    return placed


def ps_lane(S, ua, ub, z, kind, zone=None):
    """an M8 lane (walk, bike, gravel, timber) from ua to ub on level z; zone = (name, reason): v16 (G15, R07) named
    under the drawing over its span (G10)"""
    a, b = sorted((ua, ub))
    S.put(sf_lane(S.X(a), S.Y(z), b - a, S.k, kind=kind))
    if zone:
        S.zone(zone[0], zone[1], a, b)


def ps_street(S, kind, u, z, call, side=1):
    """v16 (G15, U11): a street element where the design has one, at u on level z, seated (G14), with its reason as
    a numbered callout: "lamp" (sf_lamp), "bollard" (sf_bollard), "rack" (sf_bike_rack); sizes are SF_STREET drawing
    rules, never printed"""
    x = S.X(u)
    y = sf_seat_x(S.Y(z), x, 0.1 * S.k)
    if kind == "lamp":
        sh, h = sf_lamp(x, y, S.k, side=side), SF_STREET["lamp_h"]
    elif kind == "bollard":
        sh, h = sf_bollard(x, y, S.k), SF_STREET["bollard_h"]
    else:
        sh, h = sf_bike_rack(x, y, S.k, side=side), SF_STREET["rack_h"]
    S.put(sh)
    S.obst.append((x - 0.6 * S.k, y, x + 0.6 * S.k, y + (h + 0.3) * S.k, 0))
    if call:
        S.call(call, u, z + h + 0.6)                          # v17: the number at the element's top


def ps_group_text(keys, tags, why=None):
    """the callout of one planting group: "Plane + chaste tree: shade the walk" from the species (tallest first) and
    the group's sourced purpose tags (pla_group_section); why = {tag: words} says it for this place; None when the
    group has no sourced purpose"""
    why = why or {}
    order = [t for t in why if t in tags] + [t for t in ("shade", "cleaning", "wind", "noise", "corridor",
                                                         "perception") if t in tags and t not in why]
    if not order:
        return None
    reason = u", ".join(why.get(t, PS_WHY[t]) for t in order[:2])
    ks = sorted(keys, key=lambda k_: -(PLA_SPECIES[k_].get("h_m") or 0.0))
    for n in (3, 2, 1):
        names = [PS_SHORT.get(k_, PLA_SPECIES[k_]["name"]) for k_ in ks[:n]]
        t = u" + ".join([names[0]] + [m_[0].lower() + m_[1:] for m_ in names[1:]]) + u": " + reason
        if len(t) <= 55 or n == 1:
            return t
    return None


def ps_group(S, ua, ub, zf, t0, t1, mix, seed, layers=(0,), why=None, avoid=(), density=1.0, call=True):
    """G9 planting from ua to ub (m) on the ground zf(u): mixed groups (plants.py pla_group_section: two or more
    species, overlapping crowns, the low layer under and around, depth layers back to front), band t0 (wet) to t1
    (dry); where the ground lies under the average-flow water only emergent species; every plant seated (G14).
    One callout per group saying what it does there (call=False: none). Returns the groups."""
    a, b = sorted((ua, ub))
    av = [tuple(sorted((S.X(p), S.X(q)))) for p, q in avoid] or None
    sh, placed, groups = pla_group_section(S.X(a), S.X(b), S.zf(zf), S.k, t0=t0, t1=t1, mix=mix, seed=seed,
                                           layers=layers, style=S.style, density=density, avoid=av,
                                           water=ps_water_y(S))
    S.put(sh)
    for key, x, h, cr, layer in placed:
        S.trees.append((key, x, h, cr))                       # G6: every plant inside its sourced height range
        ps_obst(S, x, S.Y(zf(S.U(x))), h, cr, layer)
    if not groups:
        S.notes.append(u"no mixed group fits %.1f-%.1f m (%s)" % (a, b, u", ".join(sorted(mix))))
    for layer, xa, xb, ks, tags in groups:
        t = ps_group_text(ks, tags, why) if call else None
        if not t:
            continue
        top = max([h for k_, x, h, cr, l_ in placed if l_ == layer and xa - 0.5 * cr * S.k <= x <= xb] or [2.0])
        u = S.U(0.5 * (xa + xb))
        tall = max(ks, key=lambda k_: PLA_SPECIES[k_].get("h_m") or 0.0)
        S.call(t, u, zf(u) + top * (fig_depth(layer)[0] if layer else 1.0) * 0.8, "plant", tall)   # v17: in the crown
    return groups


def ps_back(S, seed, mix=("plane", "chaste", "olive", "tamarisk")):
    """the D8 sky and the depth behind the cut (R16): D9 layers 2 and 1, each on its own ground = the cut line with
    the bed (G14), the farthest first: R2-C pass 2 (Aras 31 Oct 12:01 "no background houses"; checklist 7) the
    basemap houses SF_BACK_BAND m behind the registry cut (sf_back_buildings: data height, else floors x
    BLD_STOREY; nearer than the band's middle on layer 1, the rest on layer 2) standing on the layer's ground
    (sf_back_house: real profiles, faded by layer, seated), then that layer's faded mixed tree groups round them;
    no house over the channel (it runs on behind the cut) or whose roof leaves the sky, no tree where the ground
    lies under the average-flow water"""
    pr = ps_gprof(S)
    gf = sf_gy(pr)
    wy = ps_water_y(S)
    # v16 (G15, P12.3): the sky reaches PS_SKY_OVER over the tallest back crown (layer 1, the nearest back layer), so
    # it never dominates and the section stays low enough for its cell; a sky of its own per cut id, birds on (D3)
    # v17 (1:250, design spec S7): ash left the BACK mix (front groups keep it), so the sky ends 15 m over the
    # highest ground and two cuts fit one page
    ht = max(PLA_SPECIES[k_]["h_m"] for k_ in mix) * PLA_GROUP["size"][1] * fig_depth(1)[0] + PS_SKY_OVER
    y_top = S.Y(max(z for _u, z in S.prof) + ht)
    S.y_top = y_top
    wl = sf_atmosphere(0.0, S.w, pr, y_top, S.k, seed=seed, sky="d8", trees=False, birds=True, style=S.style,
                       back_ground={2: pr, 1: pr}, cid=S.cid)
    lab = level_end_labels(S.cid)                               # registry m along the cut (t) -> u: the first end's
    d0, sg = S.d[lab[0]], (-1.0 if lab[0] == "SW" else 1.0)    # distance to the axis; SW positive, NE negative
    lo = min(S.prof[0][1], S.prof[-1][1]) - 0.5                 # the channel: the cut line under both land levels
    cu = [u for u, z in S.prof if z < lo]
    ch = (min(cu), max(cu)) if cu else None
    chx = [(S.X(ch[0]), S.X(ch[1]))] if ch else []              # v16 (G8): no back tree in the channel, wet or dry
    blds = sf_back_buildings(S.cid, *sorted((d0 + sg * S.u0, d0 + sg * S.u1)), log=S.info, look=-1)   # the key map's view (SW right)
    dmid = 0.5 * (SF_BACK_BAND[0] + SF_BACK_BAND[1])
    nh, nx = 0, 0
    for layer in (2, 1):
        hs = []
        for ta, tb, h_m, fl, db in blds:                       # this layer's houses, before its trees
            if (1 if db < dmid else 2) != layer or tb - ta < 3.0:   # a sliver under one bay (sf_back_house's 3.0 m)
                continue
            ua, ub = sorted((sg * (ta - d0), sg * (tb - d0)))
            if ch and ub > ch[0] and ua < ch[1]:
                nx += 1
                continue
            hh = sf_back_house(S.X(ua), S.X(ub), pr, h_m, S.k, layer=layer, floors=fl, d_m=db)   # v17: windows <= 30 m
            if not hh or max(p_[1] for s_ in hh for p_ in s_[1]) > y_top:
                nx += 1
                continue
            wl.add("background", hh)
            hs.append((S.X(ua), S.X(ub)))
            S.obst.append((S.X(ua), min(p_[1] for s_ in hh for p_ in s_[1]), S.X(ub),
                           max(p_[1] for s_ in hh for p_ in s_[1]), layer))
            nh += 1
        sh, pl_, _gr = pla_group_section(0.0, S.w, gf, S.k, t0=0.45, t1=0.95, mix=list(mix), seed=seed + 31 * layer,
                                         layers=(layer,), style=S.style, density=0.7, avoid=(hs + chx) or None,
                                         hires=False, detail=False, water=wy)
        wl.add("background", sh)
        for key, x, h, cr, l_ in pl_:
            ps_obst(S, x, gf(x), h, cr, l_)
    wl.put(S.pg)
    S.info.append(u"%d background houses drawn (%d left out: over the channel or above the sky)" % (nh, nx))


def ps_land(S, pts, material="earth"):
    """cut ground under a surface [(u, z)] left to right, down to the drawing's bottom"""
    S.put(sct_ground(S.P(pts), 0.0, S.k, material))


def ps_strip(S):
    """the summer strip channel (PS_STRIP) at S.st_c (v16: the survey low point, ps_survey), cut PS_STRIP depth
    under the lowest bed point it spans: its four points"""
    w, dp = PS_STRIP
    a, e = S.st_c - w / 2.0, S.st_c + w / 2.0
    fl = min(S.gbed(a + (e - a) * i / 8.0) for i in range(9)) - dp
    return [(a, S.gbed(a)), (a + 0.6, fl), (e - 0.6, fl), (e, S.gbed(e))]


def ps_bed_pts(S, uL, uR):
    """v16: the bed surface from uL to uR (m) with the summer strip cut in: the survey every 1 m where S.gb, else
    flat at the registry bed. Put it into S.prof between the banks."""
    st = ps_strip(S)
    pts = [(uL, S.gbed(uL))]
    if S.gb:
        u = math.floor(uL) + 1.0
        while u < st[0][0] - 0.3:
            pts.append((u, S.gbed(u)))
            u += 1.0
    pts += st
    if S.gb:
        u = math.ceil(st[-1][0] + 0.3)
        while u < uR - 0.3:
            pts.append((u, S.gbed(u)))
            u += 1.0
    return pts + [(uR, S.gbed(uR))]


def ps_bed(S, uL, uR, call=(u"Stepping stones", u"cross the summer strip dry-shod"), stones=True):
    """the gravel bed from uL to uR with the summer strip (v16: the surveyed bed and the strip on its low point are
    in S.prof already, ps_bed_pts), then the M5 water (G8): the average yearly flow filling the bed below it (never
    dry), Q100 and Q500 wall to wall (lines only; v17: their levels are marked outside the drawing, ps_page);
    stepping stones across the strip (stones=False: none, W1), named as a zone (call = (name, reason)).
    Returns (u from, u to, level) of the stones' tops: the only place in the water people stand."""
    st = ps_strip(S)
    S.put(sct_ground(S.P(ps_bed_pts(S, uL, uR)), 0.0, S.k, "gravel"))
    # v17 (G-R4-5.4): no level labels in the picture; the levels are marked outside the frame (ps_page)
    wl = water_section(S.P(S.prof), S.k, S.Y, cid=S.cid, fill_ground=False, labels=False)
    wl.put(S.pg)
    ua, ub, ztop = st[0][0] - 0.2, st[-1][0] + 0.2, level_avg_flow(S.cid) + PS_STONE_UP
    if not stones:
        return ua, ub, ztop
    S.put(sf_stepping_stones(S.X(ua), S.X(ub), S.Y(st[1][1]), ps_water_y(S), S.k, above_m=PS_STONE_UP,
                             seed=len(S.cid)))
    if call:
        S.zone(call[0], call[1], ua, ub, "water")
    return ua, ub, ztop


def ps_stair_z(u_bot, z_bot, n, rise, tread, side):
    """the tread level (m) at u of a flight climbing from (u_bot, z_bot) toward side"""
    def f(u):
        i = int(math.ceil((u - u_bot) * side / tread - 1e-9))
        return z_bot + rise * max(0, min(n, i))
    return f


def ps_wall(S, u_face, side, top, rail=True):
    """the DSİ stone wall with its water face at u_face (side -1: land to the left), bed to top; a railing on it"""
    sh, _ = sct_bank("dsi_wall", S.X(u_face), S.Y(top), S.Y(S.bed), side, S.k, t_m=PS_WALL_T, reach_m=0.05,
                     depth_m=PS_DEPTH)
    S.put(sh)
    if rail:
        ps_rail(S, u_face + side * 0.15, top)


def ps_rail(S, u, z):
    sh, _ = sct_bank("railing", S.X(u), S.Y(z), S.Y(S.bed), 1, S.k, h_m=PS_RAIL_H)
    S.put(sh)


def ps_block_ring(S, u0, u1, z0, z1, material):
    S.put(sct_hatch_fill(S.P([(u0, z0), (u1, z0), (u1, z1), (u0, z1)]), material, S.k, SCT["cut"], 0.25))


def ps_steps(u, z, n, rise, tread, side):
    """a flight of n steps from (u, z) climbing landward (side +1 = to the right): (surface points after the
    start, [(ua, ub, z_under, z_top)] one block per step, its slab 0.15 m under the step below)"""
    pts, blocks = [], []
    for _ in range(n):
        z2, u2 = z + rise, u + side * tread
        pts += [(u, z2), (u2, z2)]
        blocks.append((min(u, u2), max(u, u2), z - 0.15, z2))
        u, z = u2, z2
    return pts, blocks


def ps_arrow(S, pts, col, lw=0.3, dash=None):
    P = S.P(pts)
    S.pg.line(P, col, lw, dash=dash)
    (ax, ay), (bx, by) = P[-2], P[-1]
    L = math.hypot(bx - ax, by - ay) or 1e-9
    ux, uy, h = (bx - ax) / L, (by - ay) / L, 1.1
    S.pg.poly([[(bx, by), (bx - ux * h - uy * h * 0.45, by - uy * h + ux * h * 0.45),
                (bx - ux * h + uy * h * 0.45, by - uy * h - ux * h * 0.45)]], fill=col)


def ps_low(S, ua, ub, zf, seed, t0=0.55, t1=0.95, avoid=(), density=1.2):
    """v17 (G-R4-5.2, D7): the low layer of sourced shrubs and flowers (plants.py pla_low_section: chaste tree,
    rosemary, French lavender, purple loosestrife, soft rush, mixed by wetness, never in rows) on a soft bank from ua
    to ub (m) on the ground zf(u), seated (G14); avoid = [(u, u)] spans kept free (lanes, benches)"""
    a, b = sorted((ua, ub))
    if b - a < 1.0:
        return
    av = [tuple(sorted((S.X(p), S.X(q)))) for p, q in avoid] or None
    sh, placed = pla_low_section(S.X(a), S.X(b), S.zf(zf), S.k, t0=t0, t1=t1, seed=seed, density=density, avoid=av,
                                 water=ps_water_y(S))
    S.put(sh)
    for key, x, h, cr in placed:
        S.trees.append((key, x, h, cr))
        ps_obst(S, x, S.Y(zf(S.U(x))), h, cr, 0)


def ps_break(S, z_top):
    """the break line at the drawing's right end (the land goes on to the cut end; PS_BREAK), from the drawing's
    bottom to just over the ground at z_top"""
    xb = S.X(S.u1)
    yb, yt = S.Y(S.z0), S.Y(z_top)
    S.pg.line([(xb, yb - 0.6), (xb, yb + 0.35 * (yt - yb)), (xb - 0.7, yb + 0.45 * (yt - yb)),
               (xb + 0.7, yb + 0.6 * (yt - yb)), (xb, yb + 0.7 * (yt - yb)), (xb, yt + 0.8)], COL["ink"], 0.2)


# ---------------------------------------------------------------- W1 upstream entry
def ps_pocket(S, ua, ub, z, seed):
    """a planted pocket on a W1 landing (ua..ub m, soil at z, PS_W1_POCKET deep): a chaste tree with rosemary and
    lavender round it (G9: mixed, overlapping, sourced sizes PLA_SPECIES), each seated (G14); one callout (the same
    words on every landing: one number)"""
    ps_block_ring(S, ua, ub, z - PS_W1_POCKET[1], z, "earth")
    for i, (key, f) in enumerate((("chaste", 0.62), ("rosemary", 0.28), ("lavender", 0.82))):   # tall one first
        sp = PLA_SPECIES[key]
        x = S.X(ua + f * (ub - ua))
        S.put(pla_section(key, x, sf_seat_x(S.Y(z), x, 0.35 * sp["crown_m"] * S.k), S.k, h_m=sp["h_m"],
                          crown_m=sp["crown_m"], seed=seed + i, style=S.style))
        S.trees.append((key, x, sp["h_m"], sp["crown_m"]))
    t = ps_group_text(["chaste", "rosemary", "lavender"], ("perception",),
                      {"perception": u"colour and scent by the seats"})
    S.call(t, (ua + ub) / 2.0, z + 0.8 * PLA_SPECIES["chaste"]["h_m"], "plant", "chaste")


def ps_sec_w1(S):
    """W1 = p.17's F1 (same registry cut; Aras 31 Oct 12:01 "f1 has better surrounding"): the SW bank's path and
    bike lane under the trees with a bench, the viewing terrace on the NE wall top, the lined reed basins beyond it
    on the NE side, the walled bed at the registry levels. The way into the bed is no straight stair: sitting steps
    cut back into the SW bank in PS_W1_FLIGHTS flights (seat-high risers, treads to sit on), landings with a planted
    pocket between them, a floor at the water's edge on the DSİ wall foot (railed: deeper than PS_RAIL_DROP to the
    bed). No blocks in the bed and nobody in its water. v16: the bed from the survey (ps_survey), the edge floor on
    it at the SW wall foot; zones named under the drawing; a lamp at the path; the inset on the floor and steps."""
    c, b, hw, k = S.cid, S.bed, S.hw, S.k
    tN, tS = level(c, "top", "NE"), level(c, "top", "SW")
    # the edge floor: dry at the average flow and (v16, DATA-1) never under the surveyed bed at the SW wall foot
    fl = math.ceil(max(level_avg_flow(c) + PS_W1_FLOOR_UP, S.gbed(hw)) * 20.0) / 20.0
    n = int(math.ceil((tS - fl) / PS_W1_SIT[1] - 1e-9))
    rise = (tS - fl) / n
    nf = max(1, min(PS_W1_FLIGHTS, n))
    fls = [n // nf + (1 if i < n % nf else 0) for i in range(nf)]
    u, z = hw + PS_W1_FLOOR_W, fl
    steps, blocks, flights, lands = [(hw, fl), (u, fl)], [], [], []
    for i, m in enumerate(fls):                                 # flight by flight, climbing to the SW (right)
        uf = u
        for j in range(m):
            z += rise
            steps.append((u, z))
            if i == nf - 1 and j == m - 1:
                break
            w = PS_W1_LAND if j == m - 1 else PS_W1_SIT[0]
            blocks.append((u, u + (w - PS_W1_POCKET[0] if j == m - 1 else w), z - rise - 0.15, z))
            if j == m - 1:
                flights.append((uf, u))
                lands.append((u, u + w, z))
            u += w
            steps.append((u, z))
    flights.append((uf, u))
    u_top = u
    S.prof = [(S.u0, tN), (-hw, tN)] + ps_bed_pts(S, -hw, hw) + steps + [(S.u1, tS)]
    gstep = lambda u_: ps_z_at(steps + [(S.u1, tS)], u_)
    # SW bank top (p.17 F1): the path next to the steps' head, a tree strip with the bench, the bike lane outside
    pa = (u_top + 0.3, u_top + 0.3 + PS_W1_LANES[0])
    bk = (S.u1 - 0.4 - PS_W1_LANES[1], S.u1 - 0.4)
    if bk[0] < pa[1] + 1.0:
        S.notes.append(u"the SW path and bike lane overlap the drawn bank (%.1f m left)" % (bk[0] - pa[1]))
    bn = pa[1] + 0.6                                            # the bench, its back to the bike lane
    # NE (p.17 F1): the viewing terrace on the wall top, the reed basins beyond it (behind the cut, faded)
    vt = (-hw - PS_WALL_T - PS_TERRACE_W, -hw - PS_WALL_T)
    bx = (S.u0 + 0.3, vt[0] - 0.6)
    ps_back(S, 11)
    bp = pla_reed_basin(S.X(bx[0]), S.X(bx[1]), S.Y(tN - PS_BASIN["depth"]), S.Y(tN), k, PS_BASIN["kerb_h"],
                        PS_BASIN["kerb_t"], PS_BASIN["media"])
    S.put(bp)
    ps_land(S, [(S.u0, tN), (-hw, tN)])                         # v16 (D7): no white veil over the basins; the
    ps_land(S, steps + [(S.u1, tS)])                            # cut land drawn after them hides what is behind
    ps_lane(S, pa[0], pa[1], tS, "walk", (u"Path", u"in the shade of the bazaar side trees"))
    ps_lane(S, bk[0], bk[1], tS, "bike", (u"Bike lane", u"through route under the trees"))
    S.put(sf_bench(S.X(bn), sf_seat_x(S.Y(tS), S.X(bn), 0.25 * k), k, side=-1, back=True))
    S.call(u"Bench: in the trees' shade, facing the water", bn - 0.2, tS + 1.4)
    ps_street(S, "lamp", u_top + 0.15, tS, u"Lamp: lights the path and the steps' head after dark", side=1)
    ps_bed(S, -hw, hw, call=None, stones=False)                 # no stones, no blocks in the bed (Aras 12:01)
    S.zone(u"Walled bed", u"left to the stream, summer strip on its low point", -hw, hw, "water")
    ps_wall(S, -hw, -1, tN)
    S.put(sf_terrace(S.X(vt[1]), S.Y(tN), PS_TERRACE_W, k, side=-1, material="timber", rail=False))
    S.zone(u"View terrace", u"on the Kale side wall top, over the water", vt[0], vt[1])
    # SW: today's wall (dashed) cut down to the edge floor, the sitting steps seated into the bank behind it
    S.pg.poly([S.P([(hw, S.gbed(hw)), (hw + PS_WALL_T, S.gbed(hw)), (hw + PS_WALL_T, tS), (hw, tS)])],
              stroke=COL["ink2"], lw=0.18, dash=[0.8, 0.5])
    ps_block_ring(S, hw, hw + PS_WALL_T, S.z0, fl, "stone")    # the wall foot, kept under the floor
    ps_block_ring(S, hw + PS_WALL_T, hw + PS_W1_FLOOR_W, fl - 0.25, fl, "concrete")
    for ua_, ub_, z0, z1 in blocks:
        ps_block_ring(S, ua_, ub_, z0, z1, "stone")
    if fl - S.gbed(hw - 0.5) > PS_RAIL_DROP:
        ps_rail(S, hw + 0.15, fl)
    for i, (ua_, ub_, z_) in enumerate(lands):
        ps_pocket(S, ub_ - PS_W1_POCKET[0], ub_, z_, 50 + 3 * i)
    S.call(u"Dashed line: today's DSİ wall, cut back into steps", hw + PS_WALL_T / 2.0, tS + 0.6)
    S.zone(u"Edge floor", u"on the dry bed edge at the foot of the steps", hw, hw + PS_W1_FLOOR_W)
    S.zone(u"Sitting steps", u"%d × %d cm seats, %d flights, planted landings" % (n, round(rise * 100), nf),
           hw + PS_W1_FLOOR_W, u_top)
    ps_arrow(S, [(S.st_c, level_avg_flow(c) + 0.3), (-hw + 1.2, tN + 2.4), (bx[1] - 0.8, tN + 1.8)],
             COL["river_mid"], 0.3, dash=[0.9, 0.6])            # over the terrace's rail and heads to the basins
    S.zone(u"Reed basins", u"stream water cleaned beyond the wall", bx[0], bx[1])
    # planting (G9 groups, p.17 F1): the trees of the SW bank round the path and bike lane (their crowns over both;
    # v16 G15: on depth layer 1, behind the people and paler), an emergent edge at each wall foot on the surveyed bed
    ps_group(S, u_top + 0.2, S.u1 - 0.2, lambda u_: tS, 0.50, 0.56, {"plane": 1.0, "ash": 0.6, "chaste": 0.8}, 11,
             layers=(1,), avoid=[pa, bk, (bn - 0.6, bn + 0.2)], why={"shade": u"shade the path and bike lane"})
    ps_group(S, -hw + 0.2, -hw + 5.0, S.gbed, 0.02, 0.05, ["soft_rush", "loosestrife"], 18, density=1.2,
             why={"cleaning": u"clean the water by the wall"})
    ps_group(S, hw - 5.0, hw - 0.2, S.gbed, 0.05, 0.02, ["soft_rush", "loosestrife"], 22, density=1.2,
             why={"cleaning": u"clean the water by the steps"})
    ps_low(S, pa[1] + 0.3, bk[0] - 0.3, lambda u_: tS, 12, avoid=[(bn - 0.8, bn + 0.4)])   # v17: shrubs + flowers
    # people as scenes, all looking at the water (focus: the strip): at the floor's railing and sitting on the steps
    # together, one on each landing's way down, on the view terrace; walking, running, walking a dog on the path
    # (FIG_ACTIVITY walkway) and riding the bike lane; more further along the path and the terrace (layer 1); nobody
    # in the bed ("water": counted)
    ps_zones(S, [("water", -hw, hw, b), ("viewing_terrace", hw + 0.3, hw + PS_W1_FLOOR_W - 0.1, fl)] +
             [("sun_steps", fa + 0.05, fb - 0.05, gstep) for fa, fb in flights], 15, density=1.5, seat_h=rise,
             focus=S.st_c)
    ps_zones(S, [("walkway", ua_ + 0.1, ub_ - PS_W1_POCKET[0] - 0.1, z_) for ua_, ub_, z_ in lands], 16, max_n=1,
             focus=S.st_c)
    ps_zones(S, [("viewing_terrace", vt[0] + 0.2, vt[1] - 0.2, tN)], 17, density=1.4, max_n=3, focus=S.st_c)
    ps_zones(S, [("walkway", pa[0], pa[1], tS), ("bike_lane", bk[0], bk[1], tS)], 18)
    ps_zones(S, [("viewing_terrace", vt[0] + 0.2, vt[1] - 0.2, tN), ("walkway", pa[0], pa[1], tS)], 19, layer=1,
             density=0.6, max_n=2)
    S.inset = (hw - 0.5, hw + PS_W1_FLOOR_W + 2.5, fl - 0.6, fl + 2.4, u"edge floor and sitting steps")   # v17: 1:100


# ---------------------------------------------------------------- W2 walking hub (Ulucami Önü)
def ps_sec_w2(S):
    """W2 at the Ulucami Önü bridge: the SW wall opened into a sub-hub floor at the water and seating steps up to a
    dry hub square above Q500 with planes; the NE edge walk and bike lane. v16: the bed between the walls from the
    survey with the strip and the stones on its low point, zones named under the drawing, fishing at the floor's
    water edge, a lamp on the edge walk, bike racks and bollards on the square, the inset on the floor."""
    c, b, hw = S.cid, S.bed, S.hw
    tN, tS = level(c, "top", "NE"), level(c, "top", "SW")
    plat = max(b + 0.30, math.ceil(S.gbed(hw) * 20.0) / 20.0)  # sub-hub floor: just above the summer strip, never
    n, tread = 10, 0.80                                         # under the surveyed bed at the wall line
    rise = (tS - plat) / n
    u_st = hw + 4.0                                             # the steps start 4.00 m behind today's wall line
    steps, blocks = ps_steps(u_st, plat, n, rise, tread, 1)
    u_sq = u_st + n * tread                                     # the hub square from here, at the wall top level
    S.prof = [(S.u0, tN), (-hw, tN)] + ps_bed_pts(S, -hw, hw) + [(hw, plat), (u_st, plat)] + steps + [(S.u1, tS)]
    ps_back(S, 21)
    ps_land(S, [(S.u0, tN), (-hw, tN)])
    ps_land(S, [(hw, plat), (u_st, plat)] + steps + [(S.u1, tS)])
    ps_lane(S, -hw - 0.6, -hw - 4.1, tN, "walk", (u"Edge walk", u"looks across to the seating steps"))
    ps_lane(S, -hw - 4.5, -hw - 6.5, tN, "bike", (u"Bike lane", u"street side, clear of the walk"))
    ps_street(S, "lamp", -hw - 4.3, tN, u"Lamp: lights the edge walk and the bike lane", side=1)
    ua, ub, ztop = ps_bed(S, -hw, hw)
    ps_wall(S, -hw, -1, tN)
    ps_block_ring(S, hw, u_st, plat - 0.25, plat, "concrete")   # sub-hub floor slab
    for ua_, ub_, z0, z1 in blocks:                             # steps seated into the cut-back bank
        ps_block_ring(S, ua_, ub_, z0, z1, "stone")
    ps_block_ring(S, u_sq, S.u1, tS - 0.25, tS, "stone")        # hub square paving
    S.pg.poly([S.P([(hw, S.gbed(hw)), (hw + PS_WALL_T, S.gbed(hw)), (hw + PS_WALL_T, tS), (hw, tS)])],
              stroke=COL["ink2"], lw=0.18, dash=[0.8, 0.5])     # today's DSİ wall, replaced by the steps
    S.call(u"Dashed line: today's DSİ wall, opened into steps", hw + PS_WALL_T / 2.0, tS + 0.6)
    S.zone(u"Sub-hub floor", u"at the water, just above the flow", hw, u_st)
    S.zone(u"Seating steps", u"%d × %d cm, sun and a view of the water" % (n, round(rise * 100)), u_st, u_sq)
    S.zone(u"Hub square", u"dry above Q500, in the planes' shade", u_sq, S.u1)
    ps_street(S, "rack", u_sq + 1.0, tS, u"Bike racks: leave the bike, walk down to the water", side=1)
    ps_street(S, "bollard", S.u1 - 1.0, tS, u"Bollards: the square's street edge, no cars")
    ps_break(S, tS)                                             # break line: the land goes on to the cut end
    # planting (G9 groups; v16 G15: the trees on depth layer 1, behind the people): the square's planes with an
    # understorey (Ottoman squares with plane trees, ICOMOS 2014), the street trees behind the NE lanes, an emergent
    # edge in the bed by the sub-hub floor
    ps_group(S, u_sq + 4.0, S.u1 - 0.5, lambda u: tS, 0.48, 0.8, {"plane": 1.0, "chaste": 0.6, "rosemary": 0.5,
                                                                  "lavender": 0.4}, 20, layers=(1,),
             why={"shade": u"shade the hub square"})
    ps_group(S, S.u0 + 0.3, -hw - 0.8, lambda u: tN, 0.45, 0.9, {"plane": 1.0, "ash": 0.5, "chaste": 0.9,
                                                                   "rosemary": 0.7}, 21, layers=(1,),
             why={"shade": u"shade the street walk"})
    ps_group(S, max(ub + 1.0, hw - 5.0), hw - 0.3, S.gbed, 0.0, 0.14, ["soft_rush", "loosestrife", "rush"], 23,
             why={"cleaning": u"clean the water at the steps"})
    ps_low(S, S.u0 + 0.3, -hw - 6.9, lambda u: tN, 28)          # v17: shrubs + flowers behind the NE lanes
    # people by zone: the NE walk and bike lane (walking, running, a dog), across on the stones, fishing at the
    # floor's water edge, children playing on the dry sub-hub floor, sitting on the steps, walking and standing
    # together in the square; more behind (layer 1)
    ps_zones(S, [("walkway", -hw - 4.1, -hw - 0.6, tN), ("bike_lane", -hw - 6.5, -hw - 4.5, tN),
                 ("water", -hw, ua, b), ("stepping_stones", ua, ub, ztop), ("water", ub, hw, b),
                 ("walkway", u_sq + 2.0, S.u1 - 1.6, tS)], 24, focus=S.st_c)
    ps_zones(S, [("water_edge", hw + 0.3, hw + 1.6, plat), ("lawn", hw + 1.8, u_st - 0.3, plat)], 26, density=1.4,
             focus=S.st_c)                                      # fishing at the edge, children playing together
    ps_zones(S, [("sun_steps", u_st + 0.2, u_sq - 0.2, ps_stair_z(u_st, plat, n, rise, tread, 1))], 27, density=1.6,
             seat_h=rise, focus=S.st_c)                         # sitting together on the steps, facing the water
    ps_zones(S, [("walkway", S.u0 + 0.5, -hw - 0.6, tN), ("walkway", u_sq + 2.0, S.u1 - 1.6, tS)], 25, layer=1,
             density=0.6)
    S.inset = (hw + 0.5, u_st + 1.5, plat - 0.6, plat + 2.4, u"sub-hub floor at the water")      # v17: 1:100


# ---------------------------------------------------------------- W3 K5 Demeter's Garden
def ps_sec_w3(S):
    """W3 at Üç Kemer: bank steps seated into the NE loose earth bank, the stream commons on the SW shelf, Demeter's
    Garden raised above Q500 behind its wall. v16: zones named under the drawing, a lamp on the crest walk, families
    lying and playing on the commons, the strip on the survey low point, the inset on the stones."""
    c, b, hw, k = S.cid, S.bed, S.hw, S.k
    tN, q5 = level(c, "top", "NE"), level(c, "q500")
    sh_ = [t for t in (level_cut(c).get("terraces") or []) if t.get("side") == "SW"]
    if not sh_:
        raise RuntimeError("W3: the SW shelf (terraces) is missing in ../common/data/LEVELS.py")
    lv = sh_[0]["level"]
    shelf = float(lv["value"] if isinstance(lv, dict) else lv)
    s0, s1 = float(sh_[0]["from_m"]), float(sh_[0]["to_m"])
    gf = math.ceil((q5 + PS_FREEBOARD) * 20.0) / 20.0          # garden floor: dry above Q500
    run = S.d["NE"] - hw                                        # NE loose earth: toe to the crest at the cut end
    n = max(1, int(round((tN - b) / 0.45)))
    rise, tread = (tN - b) / n, run / n
    crest = -hw - run
    steps, _ = ps_steps(-hw, b, n, rise, tread, -1)
    S.prof = [(S.u0, tN)] + list(reversed(steps)) + ps_bed_pts(S, -hw, hw) + [(s0, shelf), (s1, shelf), (s1, gf),
                                                                             (S.u1, gf)]
    ps_back(S, 31)
    # NE: today's loose earth bank (dashed) and the steps seated into it (section_parts earth bank with steps)
    sh, _ = sct_bank("earth", S.X(-hw), S.Y(tN), S.Y(b), -1, k, run_m=run, reach_m=crest - S.u0, depth_m=PS_DEPTH,
                     steps=[(rise, tread)] * n, steps_from_m=0.0, step_material="stone")
    ps_land(S, [(hw, b), (s0, shelf), (s1, shelf), (s1, gf), (S.u1, gf)])   # the garden: fill above the shelf
    S.put(sh)
    old = [(-hw - run * i / 12.0, b + (tN - b) * (3 * (i / 12.0) ** 2 - 2 * (i / 12.0) ** 3)) for i in range(13)]
    S.pg.line(S.P(old), COL["ink2"], 0.18, dash=[0.8, 0.5])
    ua, ub, ztop = ps_bed(S, -hw, hw)
    ps_rail(S, crest - 0.2, tN)
    ps_lane(S, crest - 3.6, crest - 0.3, tN, "walk", (u"Crest walk", u"looks down the steps to the water"))
    ps_street(S, "lamp", crest - 3.8, tN, u"Lamp: lights the crest walk and the steps' head", side=1)
    # SW: the stream commons on the shelf, the garden raised above Q500 behind a stone wall
    ps_block_ring(S, s1, s1 + 0.40, shelf - 0.30, gf + 0.15, "stone")
    S.zone(u"Bank steps", u"%d × %d cm, sit or walk down to the bed" % (n, round(rise * 100)), crest, -hw)
    S.zone(u"Stream commons", u"open ground the floods may cover", s0, s1)
    S.zone(u"Demeter's Garden", u"raised above Q500, stays dry", s1, S.u1)
    gy = lambda u: shelf + (b - shelf) * max(0.0, min(1.0, (s0 - u) / (s0 - hw)))
    S.zone(u"Wet edge", u"floods at Q100, holds the bank", hw, s0, "water")
    # planting (G9 groups): a mixed wet edge on the slope up to the commons (wet to drier, emergent only under the
    # water), the garden's trees, shrubs and herbs around the tomato rows, the café's plane a step behind (layer 1)
    ps_group(S, hw + 0.4, s0 - 0.3, gy, 0.0, 0.42, ["soft_rush", "loosestrife", "rush", "willow", "tamarisk"], 33,
             layers=(1, 0), why={"cleaning": u"clean the water", "shade": u"shade the edge"})
    rows = (s1 + 2.6, s1 + 7.0)
    S.put(sf_seat(pla_crop_rows("tomato", S.X(rows[0]), S.X(rows[1]), S.Y(gf), k, spacing=1.0, h_m=1.0,
                                crown_m=0.8), S.Y(gf)))
    S.call(u"Tomato rows: the garden's crop, above the flood", sum(rows) / 2.0, gf + 1.4, "zone")
    ps_group(S, s1 + 0.6, S.u1 - 0.3, lambda u: gf, 0.5, 0.95, {"plane": 0.6, "olive": 1.0, "chaste": 0.8,
                                                                "rosemary": 0.7, "lavender": 0.7}, 34,
             layers=(1, 0), avoid=[(rows[0] - 0.2, rows[1] + 0.2)],
             why={"shade": u"shade the café", "perception": u"seasonal colour"})
    ps_low(S, s1 + 0.6, rows[0] - 0.3, lambda u: gf, 38)       # v17: shrubs + flowers round the tomato rows
    ps_break(S, gf)                                             # v17 (1:250): the garden goes on to the cut end
    # people by zone: on the crest walk, sitting and walking on the bank steps, across on the stones, children and
    # families on the commons; a gardener at the tomato rows and a café guest (dry garden floor, hand-placed)
    ps_zones(S, [("walkway", crest - 3.6, crest - 0.3, tN),
                 ("sun_steps", crest + 1.6, -hw - 0.4, ps_stair_z(-hw, b, n, rise, tread, -1)),
                 ("water", -hw, ua, b), ("stepping_stones", ua, ub, ztop), ("water", ub, s0, gy)], 35, seat_h=rise,
             focus=S.st_c)
    ps_zones(S, [("lawn", s0 + 1.0, s1 - 1.0, shelf)], 37, density=1.4,
             focus=S.st_c)                                      # families playing, lying in the sun on the commons
    ps_zones(S, [("lawn", s0 + 1.0, s1 - 1.0, shelf)], 36, layer=1, density=0.6)
    ps_fig(S, "stand", s1 + 5.2, gf, facing=-1)                # at the tomato rows
    ps_fig(S, "sit_step", s1 + 8.6, gf, facing=-1)             # café in the garden (v17: inside the 50 m break)
    S.call(u"Café: guests in the garden's shade", s1 + 8.6, gf + 2.2, "zone")
    S.inset = (ua - 0.5, ub + 0.5, b - 0.5, b + 2.5, u"stepping stones over the summer strip")    # v17: 1:100


# ---------------------------------------------------------------- W4 downstream reach
def ps_sec_w4(S):
    """W4 downstream: the crest walk, bike lane and tree corridor on the NE embankment, a ramp on a berm to a viewing
    terrace above Q500, steps to a boardwalk that floods at Q100, the SW slope planted wet to dry, the field behind.
    v16: zones named under the drawing, the corridor on depth layers 2-1, a lamp and a bollard on the crest, fishing
    at the boardwalk's end, the strip on the survey low point, the inset on the boardwalk end."""
    c, b, hw, k = S.cid, S.bed, S.hw, S.k
    tN, aN = level(c, "top", "NE"), level(c, "angle_deg", "NE")
    tS, aS = level(c, "top", "SW"), level(c, "angle_deg", "SW")
    q1, q5 = level(c, "q100"), level(c, "q500")
    gN, gS = math.tan(math.radians(aN)), math.tan(math.radians(aS))
    cN, cS = -hw - (tN - b) / gN, hw + (tS - b) / gS            # crests (u)
    S.prof = [(S.u0, tN), (cN, tN)] + ps_bed_pts(S, -hw, hw) + [(cS, tS), (S.u1, tS)]
    ps_back(S, 41)
    zN = lambda u: b + (-hw - u) * gN                           # the NE slope's level at u
    zS = lambda u: b + (u - hw) * gS
    sh, _ = sct_bank("embankment", S.X(-hw), S.Y(tN), S.Y(b), -1, k, angle_deg=aN, reach_m=cN - S.u0,
                     depth_m=PS_DEPTH)
    S.put(sh)
    sh, _ = sct_bank("embankment", S.X(hw), S.Y(tS), S.Y(b), 1, k, angle_deg=aS, reach_m=S.u1 - cS,
                     depth_m=PS_DEPTH)
    S.put(sh)
    # NE crest: the tree corridor, the bike lane, the crest walk (G10)
    ps_lane(S, cN - 0.3, cN - 2.8, tN, "walk", (u"Crest walk", u"above Q500, beside the corridor"))
    ps_lane(S, cN - 3.2, cN - 5.2, tN, "bike", (u"Bike lane", u"along the crest, clear of the walk"))
    ps_street(S, "lamp", cN - 3.0, tN, u"Lamp: lights the crest walk and the bike lane", side=1)
    ps_street(S, "bollard", cN - 0.1, tN, u"Bollard: no vehicles on the ramp")
    # the ramp down the embankment on an earth berm to a viewing terrace above Q500, steps to the boardwalk
    tT = math.ceil((q5 + PS_FREEBOARD) * 20.0) / 20.0           # terrace floor: dry above Q500
    run = (tN - tT) / PS_RAMP
    uT = cN + run                                               # the ramp's foot = the terrace's landward edge
    uW = uT + PS_TERRACE_W                                      # the terrace's water edge
    dk = round((q1 - 0.40) * 20.0) / 20.0                       # boardwalk deck: floods at Q100 (design rule)
    ns = int(math.ceil((tT - dk) / PS_STAIR[1]))
    rs = (tT - dk) / ns
    ub = uW + ns * PS_STAIR[0]                                  # the boardwalk's landward edge
    ua = -hw + 1.6                                              # ... its end, over the bed's edge
    sa, sb, ztop = ps_bed(S, -hw, hw)
    ring = [(cN, tN), (uT, tT - 0.20), (uT, zN(uT))]            # the berm under the ramp
    S.put(sct_hatch_fill(S.P(ring), "earth", k, SCT["cut"], 0.25))
    sh, _, _ = sf_ramp(S.X(uT), S.Y(tT), run, tN - tT, k, side=-1, material="concrete", rail=True)
    S.put(sh)
    S.zone(u"Ramp", u"step-free from the crest to the terrace", cN, uT)
    S.put(sf_terrace(S.X(uT), S.Y(tT), PS_TERRACE_W, k, side=1, material="timber", rail=False))
    u = uT + 0.4
    while u < uW:                                               # the terrace's piles down into the bank
        S.pg.line(S.P([(u, tT - 0.25), (u, zN(u) - 0.6)]), PS_TIMBER, 0.35)
        u += 1.8
    S.zone(u"Viewing terrace", u"above Q500, looks over the water", uT, uW)
    sh, _ = sf_stairs(S.X(ub), S.Y(dk), ns, rs, PS_STAIR[0], k, side=-1, material="concrete", rail=True)
    S.put(sh)
    S.pg.poly([S.P([(ua, dk - 0.20), (ua, dk), (ub, dk), (ub, dk - 0.20)])], fill=PS_TIMBER, stroke=SCT["cut"],
              lw=0.25)
    u = ub + 0.3
    while u < ua - 0.3:                                         # piles down into the bank and the bed
        S.pg.line(S.P([(u, dk - 0.20), (u, min(zN(u), b) - 0.6)]), PS_TIMBER, 0.35)
        u += 2.0
    ps_rail(S, ua + 0.1, dk)
    S.zone(u"Boardwalk", u"steps down, floods at Q100, out over the wet edge", uW, ua)
    # planting (G9 groups): the crest corridor (trees and shrubs; v16 G15: layers 2-1, behind the people), a wet edge
    # under the terrace and boardwalk, the SW slope wet to dry; the field behind the SW crest takes the surplus water
    ps_group(S, S.u0 + 0.3, cN - 5.6, lambda u: tN, 0.45, 0.9,
             {"plane": 1.0, "ash": 0.5, "chaste": 1.0, "rosemary": 0.8, "olive": 0.6}, 42, layers=(2, 1),
             why={"shade": u"shade the crest"})
    S.call(u"Ecological corridor: trees and shrubs along the crest", (S.u0 + cN - 5.6) / 2.0, tN + 4.0, "plant",
           "plane")
    ps_group(S, uT + 0.3, -hw - 0.2, zN, 0.0, 0.16, ["soft_rush", "loosestrife", "rush"], 43,
             why={"cleaning": u"clean the water under the deck"})
    ps_group(S, hw + 0.3, cS - 0.6, zS, 0.0, 0.5, ["soft_rush", "loosestrife", "willow", "tamarisk", "chaste"], 44,
             layers=(1, 0), why={"shade": u"shade the slope", "cleaning": u"clean the water"})
    ps_low(S, S.u0 + 0.3, cN - 5.6, lambda u: tN, 48)            # v17: shrubs + flowers in front of the corridor
    ps_low(S, hw + 1.0, cS - 0.6, zS, 49, t0=0.3)               # v17: and on the bazaar side slope, wet to dry
    S.put(sf_seat(pla_crop_rows("cotton", S.X(cS + 1.0), S.X(S.u1 - 0.4), S.Y(tS), k, spacing=0.9, h_m=1.0,
                                crown_m=0.6), S.Y(tS)))
    S.zone(u"Cotton field", u"takes the surplus water", cS, S.u1)
    ps_break(S, tS)                                             # v17 (1:250): the field goes on to the cut end
    # people by zone: cycling, walking, running, a dog on the crest, down the ramp, sitting and standing on the
    # terrace, on the boardwalk and fishing at its end (water_edge: the line drops to the average-flow water), across
    # on the stones; more along the crest behind the cut (layer 1); a farmer in the field
    ps_zones(S, [("walkway", cN - 2.8, cN - 0.3, tN), ("bike_lane", cN - 5.2, cN - 3.2, tN),
                 ("walkway", cN + 1.0, uT - 1.0, lambda u: tN - (u - cN) * PS_RAMP),
                 ("walkway", ub - 0.3, ua - 2.2, dk), ("water_edge", ua - 2.0, ua - 0.1, dk),
                 ("water", -hw, sa, b), ("stepping_stones", sa, sb, ztop), ("water", sb, hw, b)], 45, focus=S.st_c)
    ps_zones(S, [("viewing_terrace", uT + 0.3, uW - 0.3, tT)], 47, density=1.5,
             focus=S.st_c)                                      # together at the view over the water
    ps_zones(S, [("walkway", cN - 2.8, cN - 0.3, tN)], 46, layer=1, density=0.6)
    ps_fig(S, "stand", S.u1 - 1.2, tS, facing=-1)
    S.inset = (ua - 3.5, ua + 0.6, dk - 1.0, dk + 2.2, u"fishing from the boardwalk's end")       # v17: 1:100


PS_DRAW = {"W1": ps_sec_w1, "W2": ps_sec_w2, "W3": ps_sec_w3, "W4": ps_sec_w4}


# ---------------------------------------------------------------- v17: numbers on the section, the zoom inset
# v17 (round 4, G-R4-5.5, G-R4-7, G-R4-2): every zone and element is ONE marker (marker.py mk_marker) on what it
# names, numbered in reading order; the side list (or W4's strip) repeats the numbers "*Name* · reason". The old
# callout key, zone strip, bank rows and bed dimension line under the drawing are gone (the "today" line says it).
PS_MK_R = 2.2                          # print mm: the room one marker takes (two digits at 7 pt + its rim, marker.py)
PS_MK_COL = {"zone": "8B3A3F", "water": "5D7F8D", "built": "4A3F35"}   # designed zone, water / bed, street element


def ps_mk_col(kind, key=None):
    """the marker colour = the colour of what it names (G-R4-7): a planting group takes its tallest species' fill"""
    if kind == "plant" and key:
        return pla_colours(key)["fill"]
    return PS_MK_COL.get(kind, PS_MK_COL["zone"])


def ps_marks(S):
    """the numbers of one section (section mm): a zone on its ground at its middle, an element (call) at its point;
    a number that touches another or the zoom inset moves up (then sideways) until it is clear and stays inside the
    section's width and height; numbered in reading order (tp_reading_order), one number per distinct text. Fills
    S.marks [(x, y, n, colour)] and S.list [(n, text, colour)]."""
    r = PS_MK_R
    bb = ps_bbox(S.pg.items)
    top = bb[3] - r
    busy = [S.inset_busy] if S.inset_busy else []
    ents = []
    for name, why, ua, ub, kind in S.zones:
        a, b = max(ua, S.u0), min(ub, S.u1)
        u = 0.5 * (a + b)
        ents.append((u"*%s* · %s" % (name, why), S.X(u), S.Y(ps_z_at(S.prof, u)) + r + 0.3, ps_mk_col(kind)))
    for t, u, z, kind, key in S.calls:
        nm, _s, why = t.partition(u": ")
        ents.append((u"*%s* · %s" % (nm, why) if why else u"*%s*" % nm, S.X(u), S.Y(z) + r, ps_mk_col(kind, key)))
    done, at = [], []
    step = 2.0 * r + 0.6

    def free(x, y):
        if any(math.hypot(p[0] - x, p[1] - y) < step for p in done):
            return False
        return not any(q[0] - r - 0.6 < x < q[2] + r + 0.6 and q[1] - r - 0.6 < y < q[3] + r + 0.6 for q in busy)
    for txt, x0, y0, col in ents:
        x0 = max(r, min(S.w - r, x0))
        spot = None
        for sx in (0, 1, -1, 2, -2, 3, -3, 4, -4):
            x = max(r, min(S.w - r, x0 + sx * step))
            y = y0
            while y <= top and not free(x, y):
                y += 0.5
            if y <= top:
                spot = (x, y)
                break
        if spot is None:
            raise ValueError(u"p13 %s: no free spot for the number of %r inside the section" % (S.cid, txt))
        done.append(spot)
        at.append((spot[0], spot[1], txt, col))
    num = {}
    S.marks, S.list = [], []
    for j in tp_reading_order([(x, y) for x, y, _t, _c in at], y_down=False, row_mm=3.0 * r):
        x, y, txt, col = at[j]
        if txt not in num:
            num[txt] = len(num) + 1
            S.list.append((num[txt], txt, col))
        S.marks.append((x, y, num[txt], col))


def ps_inset_shapes(items):
    """v16: the section's page items as house shapes for sf_zoom_inset (one ring per poly, circles as rings,
    images kept; no text: the inset shows the drawing, its words stay on the section)"""
    out = []
    for it in items:
        if it[0] == "poly":
            for R in it[1]:
                if len(R) >= 3:
                    out.append(("poly", R, it[2], it[3], it[4], it[7]))
        elif it[0] == "line":
            out.append(("line", it[1], it[2], it[3], it[4]))
        elif it[0] == "circle":
            out.append(("poly", sec_ellipse(it[1], it[2], it[3], it[3], 16), it[4], it[5], it[6]))
        elif it[0] == "image":
            out.append(tuple(it[:8]))
    return out


def ps_inset(S, log):
    """v17 (G-R4-5.6, D11): the cut's main use spot S.inset (ua, ub, za, zb m, what) drawn again at 1:100
    (PS_INSET_SCALE, 2.5 x the 1:250 parent) in a box in the section's own free sky: over the highest ground and its
    people, clear of every drawn thing of the front layer (S.obst layer 0: plants, street elements; the back layers
    may go under its white ground) and of the spot, inside the drawing, as near the spot as it can be; sf_zoom_inset
    draws the spot frame, one frame link, the box, "ZOOMED IN · what · 1:100" above it and its own scale bar under
    it. No room: FLAG, no inset."""
    if not S.inset:
        return
    ua, ub, za, zb, what = S.inset
    src = (S.X(ua), S.Y(za), S.X(ub), S.Y(zb))
    f = PS_INSET_K / S.k
    dw, dh = (src[2] - src[0]) * f, (src[3] - src[1]) * f
    lab_w = fm_width(u"ZOOMED IN · %s · 1:%d" % (what, PS_INSET_SCALE), PS_LBL / PT, True)
    lab_h = 0.6 * PS_LBL + PS_LBL * CAP + 0.6                  # the caption over the box
    bar_h = SF_ZOOM["gap"] + SF_ZOOM["bar_h"] + 0.9 * 2.12 + 0.6   # its scale bar and figures under the box
    ww = max(dw, lab_w)
    bb = ps_bbox(S.pg.items)
    lo = S.Y(max(z for _u, z in S.prof) + 2.4) + bar_h          # over the highest ground and its people
    hi = max(S.y_top if S.y_top is not None else bb[3], bb[3]) - lab_h
    keep = [tuple(o[:4]) for o in S.obst if (o[4] if len(o) > 4 else 0) == 0] + \
        [(src[0] - 1.0, src[1] - 1.0, src[2] + 1.0, src[3] + 1.0)]
    cx, cy = 0.5 * (src[0] + src[2]), 0.5 * (src[1] + src[3])
    best = None
    y = lo
    while y + dh <= hi:
        x = 0.5
        while x + ww <= S.w - 0.5:
            b_ = (x - 0.6, y - bar_h, x + ww + 0.6, y + dh + lab_h)
            if not any(b_[0] < o[2] and o[0] < b_[2] and b_[1] < o[3] and o[1] < b_[3] for o in keep):
                d = math.hypot(x + 0.5 * dw - cx, y + 0.5 * dh - cy)
                if best is None or d < best[0]:
                    best = (d, x, y)
            x += 1.5
        y += 1.5
    if best is None:
        log.append(u"FLAG %s %s: no free sky for the zoom inset (%.0f x %.0f mm at 1:%d): not drawn" % (
            S.page, S.cid, dw, dh, PS_INSET_SCALE))
        return
    _d, x, y = best
    dst = (x, y, x + dw, y + dh)
    S.put(sf_zoom_inset(src, dst, S.k, PS_INSET_K, ps_inset_shapes(S.pg.items), what, size=PS_LBL,
                        scale_den=PS_INSET_SCALE, parent_den=PS_SCALE, page=S.page))
    S.boxes.append(dst)
    S.inset_busy = (x - 0.3, y - bar_h, x + ww + 0.3, y + dh + lab_h)
    log.append(u"%s %s: zoom inset at 1:%d (%s), %.0f x %.0f mm, people %.1f mm tall" % (
        S.page, S.cid, PS_INSET_SCALE, what, dw, dh, FIG_ADULT_H * PS_INSET_K))


def ps_finish(S, log):
    """the G6 check, the notes, (v17) the 1:100 zoom inset, then the numbers (ps_marks)"""
    for m_ in sf_assert_g6(S.k, trees=S.trees, strict=False):  # G6: people 1.75 m, trees in their sourced range
        log.append(u"G6 CHECK section %s (style %s): %s" % (S.cid, S.style, m_))
    for m_ in S.notes:
        log.append(u"NOTE section %s planting: %s" % (S.cid, m_))
    for m_ in S.info:
        log.append(u"section %s: %s" % (S.cid, m_))
    ps_inset(S, log)
    ps_marks(S)


def ps_section(cid, log, page, style="a"):
    """one cut as a PsSec (its drawing in S.pg, print mm at 1:250; see PsSec), in style a (D1, the only style);
    v16: the surveyed bed first (ps_survey, DATA-1); v17: page = the booklet page id (log lines, inset)"""
    u0, u1, d = ps_extent(cid)
    S = PsSec(cid, u0, u1, d, style)
    S.page = page
    ps_survey(S, next(k_ for k_, c_, _n, _m, _t in PS_CUTS if c_ == cid), log)
    PS_DRAW[cid](S)
    ps_finish(S, log)
    return S


# ---------------------------------------------------------------- v17: the words beside a section
PS_LIST_PT, PS_TODAY_PT, PS_TITLE_PT, PS_SCEN_PT = 7.0, 6.5, 10.0, 8.0   # pt: list, "today" line, title, scenario
PS_LEAD = 1.3                          # line spacing / size
PS_LIST_ROW = 3.7                      # print mm: least step between two list entries (a two-digit marker + 0.6 mm)


def ps_lead(pt):
    return pt * PT * PS_LEAD


def ps_bank_short(c, side):
    """a bank as the level table has it, short"""
    kind = ps_kind(c, side)
    h = level(c, "height", side) or level_depth(c, side)
    if kind == "dsi_wall":
        return u"DSİ stone wall %.2f m" % h
    if kind == "embankment":
        return u"embankment %.1f° · %.2f m" % (level(c, "angle_deg", side), h)
    if kind == "loose_earth":
        return u"loose earth bank %.2f m" % h
    return u"no crest, the ground keeps rising"


def ps_today(S):
    """v17 (G-R4-2): the one "today" line: both banks and the bed width from the level table, by place name"""
    c = S.cid
    return u"*Today* · %s: %s · bed {:,.0f} cm · %s: %s".format(level(c, "bed_width_cm")) % (
        place_name("side_NE"), ps_bank_short(c, "NE"), place_name("side_SW"), ps_bank_short(c, "SW"))


def ps_note(cid):
    """the key line of a section, from the level table"""
    q5 = level(cid, "q500")
    if cid == "W1":
        return u"Q500 %s stays *%.2f m* under the DSİ walls · reeds only in lined basins the flood passes by" % (
            ps_lv(q5), level(cid, "top", "SW") - q5)
    if cid == "W2":
        return u"Q500 %s stays *%.2f m* under the hub square · the steps flood, the square stays dry" % (
            ps_lv(q5), level(cid, "top", "SW") - q5)
    if cid == "W3":
        return u"Q500 %s · garden floor *%s* stays dry: olive and lavender need soil that never waterlogs" % (
            ps_lv(q5), ps_lv(math.ceil((q5 + PS_FREEBOARD) * 20.0) / 20.0))
    return u"Q500 %s stays *%.2f m* under the %s bank top · wet edge, boardwalk and trees by flood level" % (
        ps_lv(q5), level(cid, "top", "NE") - q5, place_name("side_NE"))


def ps_para(tp, text, x, y, w, pt, colour, name):
    """a wrapped paragraph from its first baseline y (tp = None: measured only); returns the next baseline"""
    lead = ps_lead(pt)
    if tp is not None:
        return tp.para(text, x, y, w, pt, lead, name=name, colour=colour, min_last_words=1)
    return y - len(tp_wrap(text, w, pt, False, 1, True)) * lead


def ps_list_col(S, ents, x0, w, y, tp=None, pg=None):
    """numbered list entries [(n, text, colour)] in a column from x0, w wide, first baseline y: the marker
    (mk_marker, the same colour as on the drawing), "*Name* · reason" beside it; returns the last baseline"""
    tx = x0 + 2.0 * PS_MK_R + 1.2
    last = y + PS_LIST_ROW
    for n, t, col in ents:
        if tp is not None:
            sh, _b, _r = mk_marker(x0 + PS_MK_R, y + 0.5 * PS_LIST_PT * PT * CAP, n, col, PS_LIST_PT)
            ps_put(pg, mk_put(tp, sh, name=u"%s list %d" % (S.cid, n)))
        yn = ps_para(tp, t, tx, y, x0 + w - tx, PS_LIST_PT, COL["ink"], u"%s list" % S.cid)
        last = yn + ps_lead(PS_LIST_PT)
        y = last - PS_LIST_ROW
    return last


def ps_side(S, x0, w, ytop, tp=None, pg=None):
    """the side column's words from ytop down (LEFT blocks): the "today" line and the key line (6.5 pt, ink2), then
    the numbered list; tp = None: measured only. Returns the y under the last line."""
    y = ytop - PS_TODAY_PT * PT * CAP
    yn = ps_para(tp, ps_today(S) + u"\n" + ps_note(S.cid), x0, y, w, PS_TODAY_PT, COL["ink2"], u"%s today" % S.cid)
    yl = yn + ps_lead(PS_TODAY_PT) - PS_LIST_ROW - 1.0
    return ps_list_col(S, S.list, x0, w, yl, tp, pg) - 1.0


def ps_strip_words(S, x0, w, ytop, legend, tp=None, pg=None, ncol=3):
    """W4's strip (RIGHT block) from ytop down: the "today" and key line across, the list in ncol columns, (legend)
    the material legend across under it; returns the y under it"""
    y = ytop - PS_TODAY_PT * PT * CAP
    yn = ps_para(tp, ps_today(S) + u" · " + ps_note(S.cid), x0, y, w, PS_TODAY_PT, COL["ink2"], u"%s today" % S.cid)
    yl = yn + ps_lead(PS_TODAY_PT) - PS_LIST_ROW - 1.0
    gap = 6.0
    cw = (w - (ncol - 1) * gap) / float(ncol)
    nrow = int(math.ceil(len(S.list) / float(ncol))) if S.list else 0
    low = yl + ps_lead(PS_LIST_PT)
    for c_ in range(ncol):
        part = S.list[c_ * nrow:(c_ + 1) * nrow]
        if part:
            low = min(low, ps_list_col(S, part, x0 + c_ * (cw + gap), cw, yl, tp, pg))
    low -= 1.0
    if legend:
        low = ps_legend(x0, x0 + w, low - 1.5, tp, pg)
    return low


def ps_legend(x0, x1, ytop, tp=None, pg=None):
    """G1: samples of everything the sections draw, in rows from ytop across x0-x1 (print mm), 7 pt, through the
    page's TextPage; tp = None: measured only. Returns the band's bottom y."""
    P = _wat_pal()
    rows = [("water", u"water at the average yearly flow"),
            ("q100", u"Q100 flood level"), ("q500", u"Q500 flood level"),
            (SCT["stone"], u"stone: DSİ walls, steps, garden wall"), (SCT["concrete"], u"concrete: stairs, ramp, basins"),
            (SCT["earth"], u"earth"), (SCT["gravel"], u"gravel bed"), (PS_TIMBER, u"timber: terrace, boardwalk"),
            (SF_LANE["walk"], u"walk paving"), (SF_LANE["bike"], u"bike lane")]
    sw, gap = 5.0, 4.0
    x, y = x0, ytop - PS_LIST_PT * PT * CAP
    for kind, lab in rows:
        w = sw + 1.2 + fm_width(lab, PS_LIST_PT)
        if x + w > x1 and x > x0:
            x, y = x0, y - PS_LIST_ROW
        if tp is not None:
            cy = y + 0.5 * PS_LIST_PT * PT * CAP
            if kind in ("q100", "q500"):
                pg.line([(x, cy), (x + sw, cy)], P[kind], 0.3, dash=[1.2, 0.6] if kind == "q100" else [0.4, 0.5])
            else:
                pg.poly([rect(x, cy - 1.0, x + sw, cy + 1.0)], fill={"water": P["sec"]}.get(kind, kind),
                        stroke=COL["faint"], lw=0.1)
                if kind == "water":
                    pg.line([(x, cy + 1.0), (x + sw, cy + 1.0)], SEC["hatch"], 0.3)
            tp.put(lab, x + sw + 1.2, y, PS_LIST_PT, name=u"legend", role="legend", colour=COL["ink"])
        x += w + gap
    bottom = y - 0.8
    if tp is not None:
        tp.block((x0, bottom, x1, ytop), u"legend")
    return bottom


# ---------------------------------------------------------------- v17: the two booklet pages p13a / p13b
# Design spec: revision_2026-11-01_round4/handover/S7_design_spec.md. Each page = one crop BK_W x BK_H (print mm,
# y up) drawn at the booklet scale itself (BK_S 1): two cuts, one full row each, at 1:250 (D2), insets 1:100 (D11).
# W1-W3: blk_section LEFT (title strip, drawing, side column of words); W4: RIGHT (its 353 mm drawing and its level
# marks leave no room for a column: the words go into a strip under it). One TextPage per page: every text of the
# crop goes through it and check() RAISES on any collision (G-R4-1); it then draws them (emit).
PS_PAGES = [("p13a", "p1", ("W1", "W2")), ("p13b", "p2", ("W3", "W4"))]
PS_RIGHT_WHY = {"W4": u"its 353 mm drawing and the level marks leave no room for a side column"}
PS_ROW_GAP = 4.0                       # print mm: least gap between two rows (spare height goes into the gaps)
PS_SIDE_MIN = 60.0                     # print mm: the narrowest side column
PS_KM_H = (22.0, 40.0)                 # print mm: the key map's least and largest height (in a side column)
PS_KM_GAP = 3.0                        # print mm under the key map


def ps_tp_draw(pg):
    """the TextPage's drawer: each registered text as a Page text item (sizes back to mm, "MC" to a baseline)"""
    def draw(it):
        x, y, al = it["x"], it["y"], it["align"]
        if str(al).upper() in ("MC", "CM"):
            ix0, iy0, ix1, iy1 = fm_ink_box(it["text"], it["pt"], it["bold"])
            y -= 0.5 * (iy0 + iy1)
            al = "C"
        ex = it.get("extra") or {}
        pg.text(it["text"], x, y, it["size_mm"], it["colour"] or COL["ink"], bold=it["bold"], align=al,
                mat=ex.get("mat"), halo=ex.get("halo"))
    return draw


def ps_place_items(pg, tp, items, dx, dy, name):
    """a section's items moved by (dx, dy) onto the page; its texts (inset caption, scale figures) registered in tp"""
    for it in ps_xform(items, 1.0, dx, dy):
        if it[0] == "text":
            _, s_, x, y, size, col, bold, al, mat, halo = it
            ex = dict((k_, v_) for k_, v_ in (("mat", mat), ("halo", halo)) if v_ is not None)
            tp.put(s_, x, y, size / PT, bold, al or "L", 0.0, name, "drawing", col, **ex)
        else:
            pg.items.append(it)


def ps_title(tp, b, S):
    """the title strip: "W1 · Upstream entry" (10 pt bold), the scenario after it (8 pt), the look direction at the
    page's right edge (8 pt, by place name)"""
    _key, cid, _n, name, take = next(r_ for r_ in PS_CUTS if r_[1] == S.cid)
    x, y = b["title_base"]
    t = u"%s · %s" % (cid, name)
    tp.put(t, x, y, PS_TITLE_PT, True, name=u"%s title" % cid, role="title", colour=COL["ink_dark"])
    tp.put(take, x + fm_width(t, PS_TITLE_PT, True) + 2.5, y, PS_SCEN_PT, name=u"%s title" % cid, role="title",
           colour=COL["ink"])
    tp.put(u"looking downstream · %s left, %s right" % (place_name("side_NE"), place_name("side_SW")), BK_W, y,
           PS_SCEN_PT, align="R", name=u"%s title" % cid, role="title", colour=COL["ink2"])


def ps_page(page, cids, log, style="a"):
    """one booklet page (p13a / p13b) in print mm (0, 0)-(BK_W, BK_H), y up: the two cuts drawn and measured first,
    the key map put in the first side column with room (else the first row grows), the rows sized to what they hold
    and top-aligned, spare height into the gaps; a page that cannot hold its rows at 1:250 RAISES with the numbers
    (no shrinking). Returns (Page, {sheet key: block box})."""
    pg = Page(BK_W, BK_H)
    tp = TextPage(page, (0.0, 0.0, BK_W, BK_H), y_down=False, pad=0.6)
    L = []
    for cid in cids:
        S = ps_section(cid, log, page, style)
        bb = ps_bbox(S.pg.items)
        by0 = min(0.0, bb[1])
        e = dict(S=S, bb=bb, by0=by0, dx=-min(0.0, bb[0]), sh=bb[3] - by0, km=0.0,
                 mode="RIGHT" if cid in PS_RIGHT_WHY else "LEFT",
                 q5=S.Y(level(cid, "q500")) - by0 + 1.8)                 # the level marks' top over the bottom
        e["dw"] = max(S.w, bb[2]) + e["dx"]
        if e["mode"] == "LEFT":
            e["sw"] = BK_W - e["dw"] - GRID_GUT
            if e["sw"] < PS_SIDE_MIN:
                raise ValueError(u"%s %s: the drawing is %.1f mm wide at 1:%d: its side column would be %.1f mm "
                                 u"(at least %.0f)" % (page, cid, e["dw"], PS_SCALE, e["sw"], PS_SIDE_MIN))
            e["side0"] = -ps_side(S, 0.0, e["sw"], 0.0)
        L.append(e)
    lefts = [e for e in L if e["mode"] == "LEFT"]

    def spare(e):
        return e["sh"] - (e["side0"] + 1.5 + e["q5"]) - PS_KM_GAP
    pick = next((e for e in lefts if spare(e) >= PS_KM_H[0]), lefts[0])
    pick["km"] = max(PS_KM_H[0], min(PS_KM_H[1], spare(pick)))
    rights = [e for e in L if e["mode"] == "RIGHT"]
    foot = not rights                                            # p13a: the legend under row 2; p13b: in W4's strip

    def heights(leg):
        tot = 0.0
        for e in L:
            if e["mode"] == "LEFT":
                e["dh"] = max(e["sh"], (e["km"] + PS_KM_GAP if e["km"] else 0.0) + e["side0"] + 1.5 + e["q5"])
                e["h"] = BLK_TITLE_H + e["dh"]
            else:
                e["dh"] = e["sh"]
                e["st"] = -ps_strip_words(e["S"], 0.0, BK_W, 0.0, leg)
                e["h"] = BLK_TITLE_H + e["dh"] + GRID_GUT + e["st"]
            tot += e["h"]
        lh = -ps_legend(0.0, BK_W, 0.0) if (leg and foot) else 0.0
        return tot + PS_ROW_GAP * (len(L) - 1) + ((PS_ROW_GAP + lh) if lh else 0.0), lh
    legend = True
    tot, lh = heights(True)
    if tot > BK_H and rights:
        legend = False
        tot, lh = heights(False)
        log.append(u"NOTE %s: no room for the material legend at 1:%d: it is on p13a only" % (page, PS_SCALE))
    if tot > BK_H:
        raise ValueError(u"%s: the rows need %.1f mm at 1:%d, the page has %.1f mm (%s): no shrinking (D2)" % (
            page, tot, PS_SCALE, BK_H, u", ".join(u"%s %.1f" % (e["S"].cid, e["h"]) for e in L)))
    ngap = len(L) - 1 + (1 if lh else 0)
    gap = PS_ROW_GAP + (BK_H - tot) / float(max(1, ngap))
    tri = sf_triangles(walls=False, aggregate=False)            # U22: no meaningless triangles in the sections
    boxes = {}
    y = BK_H
    for e in L:
        S, c = e["S"], e["S"].cid
        b = blk_section(0.0, y, BK_W, e["h"], c, side_w=e.get("sw"), mode=e["mode"],
                        why=PS_RIGHT_WHY.get(c), strip_h=e.get("st"), y_down=False)
        ps_title(tp, b, S)
        d = b["drawing"]
        dxp, dyp = d[0] + e["dx"], d[1] - e["by0"]
        ps_place_items(pg, tp, S.pg.items, dxp, dyp, u"%s drawing" % c)
        tp.block(d, u"%s drawing" % c)
        for i, (x, y_, n, col) in enumerate(S.marks):
            sh_, _b, _r = mk_marker(dxp + x, dyp + y_, n, col, PS_LIST_PT)
            ps_put(pg, mk_put(tp, sh_, name=u"%s mark %d" % (c, i)))
        # the level marks outside the drawing's right edge (G-R4-5.4), the 1:250 scale bar beside (or over) them
        fr = (dxp, dyp + e["by0"], dxp + max(S.w, e["bb"][2]), dyp + e["bb"][3])
        lv = [("q500", level(c, "q500")), ("q100", level(c, "q100")), ("avg", level_avg_flow(c)), ("bed", S.bed)]
        ps_put(pg, tp_shapes(sf_level_marks(fr, lv, side="R", y_of=lambda v, _S=S, _d=dyp: _d + _S.Y(v),
                                            size=PS_LBL, page=u"%s %s" % (page, c)), tp, name=u"%s levels" % c))
        lb = [it["box"] for it in tp.items if it["name"] == u"%s levels" % c] or [(fr[2], fr[1], fr[2] + 8.0, fr[1])]
        if e["mode"] == "LEFT":
            xb, yb = max(q[2] for q in lb) + 3.0, fr[1] + 3.5
        else:
            xb, yb = fr[2] + 2.0, max(q[3] for q in lb) + 4.0
        ps_put(pg, tp_shapes(sf_scale_bar(xb, yb, S.k, den=PS_SCALE, max_mm=min(24.0, BK_W - xb - 10.0)), tp,
                             name=u"%s bar" % c))
        if e["mode"] == "LEFT":
            sx0, _sy0, sx1, sy1 = b["side"]
            yt = sy1
            if e["km"]:
                ps_key_map(pg, tp, (sx0, sy1 - e["km"], sx1, sy1), cids, page, log)
                yt = sy1 - e["km"] - PS_KM_GAP
            ps_side(S, sx0, sx1 - sx0, yt, tp, pg)
        else:
            st = b["strip"]
            ps_strip_words(S, st[0], st[2] - st[0], st[3], legend, tp, pg)
        key = next(k_ for k_, c_, _n, _m, _t in PS_CUTS if c_ == c)
        boxes[key] = (0.0, y - e["h"], BK_W, y)
        log.append(u"%s %s: block %s %.0f x %.0f mm, drawing %.0f x %.0f mm at 1:%d, %d numbers" % (
            page, c, e["mode"], BK_W, e["h"], e["dw"], e["sh"], PS_SCALE, len(S.list)))
        y -= e["h"] + gap
    if lh:
        ps_legend(0.0, BK_W, lh, tp, pg)
    sf_triangles(**tri)
    tp.check(True, log)                                        # G-R4-1: RAISES TextCollision on any collision
    tp.emit(ps_tp_draw(pg))
    return pg, boxes
