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
PS_SCALE = 500                       # 1:500 on the booklet page (standard scales, SCRIPT_STANDARD §8)
PS_K = 1000.0 / PS_SCALE              # print mm per m (k of section_parts and plants)
PS_DEPTH = 1.0                        # m of cut ground drawn under the bed (section_parts drawing rule)
PS_WALL_T = 0.60                      # m: DSİ wall thickness: no sourced value; the same 0.60 m as p.04-05 (site board P45_WALL_T_M, G2)
PS_RAIL_H = 1.10                      # m: railing height on the wall and bank tops: drawing value
PS_BASIN = dict(kerb_h=0.30, depth=1.10, media=0.80, kerb_t=0.15)   # W1 reed basin cell beyond the NE wall: the
#                                     same drawing values as p.17's F1 (water board P17_BASIN; no source)
PS_STRIP = (3.00, 0.40)               # m: the summer strip channel in the bed (proposal): width, depth
PS_FREEBOARD = 0.30                   # m: a dry proposed floor sits at least this far above Q500 (design rule)
PS_LBL = BK_MIN_PT * PT               # print mm: the smallest word on the page (7.5 pt)
PS_TTL = 9.5 * PT                     # section titles
PS_NOTE = 8.0 * PT                    # the key line under a title, the key map title
PS_ROW = PS_LBL * 1.35                # one label row
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
PS_CALL_UP = 2.6                      # m over a zone's ground where its callout circle sits (over the heads)
PS_CO = PS_LBL                        # callout circles and key: the page's smallest word size (BK_MIN_PT)
PS_WHY = {"shade": u"shade", "cleaning": u"clean the water", "perception": u"seasonal colour",
          "wind": u"cut the wind", "noise": u"cut street noise", "corridor": u"ecological corridor"}
PS_SHORT = {"plane": u"Plane", "ash": u"Ash", "willow": u"Willow", "olive": u"Olive", "tamarisk": u"Tamarisk",
            "chaste": u"Chaste tree", "rosemary": u"Rosemary", "lavender": u"Lavender", "loosestrife": u"Loosestrife",
            "soft_rush": u"Soft rush", "rush": u"Sharp rush", "stone_pine": u"Stone pine"}
# where each cut crosses the stream axis (survey m; the cut centres of the level table's W rows): the drawn span runs
# from it to the cut's two ends (level_ends), NE end on the left
PS_AXIS = {"W1": (29693.022, 32569.176), "W2": (29959.774, 32264.566), "W3": (30354.663, 31689.671),
           "W4": (30991.856, 31039.404)}
# (sheet key, cut id, number on the page, name, takeaway in the title)
PS_CUTS = [("up", "W1", 1, u"Upstream entry", u"sitting steps down to the water, reed basins beyond the NE wall"),
           ("k4", "W2", 2, u"K4 walking hub", u"seating steps down to the summer strip, the hub square stays dry"),
           ("k5", "W3", 3, u"K5 Demeter's Garden", u"garden above Q500, stream commons below it"),
           ("down", "W4", 4, u"Downstream reach", u"planting bands and a boardwalk that follow the flood levels")]
PS_BREAK = {"W2": ("SW", 50.0)}
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
        self.lab_u = 2.5                                      # m: where the water level labels start (clear of people)
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

    def call(self, text, u, z):
        """a numbered callout (R2-C shared style): its circle near (u, z) m, "Element: reason" in the key"""
        self.calls.append((text, u, z))


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


def ps_lane(S, ua, ub, z, kind, label=None):
    """an M8 lane (walk, bike, gravel, timber) from ua to ub on level z; label = its callout "Lane: reason" (G10)"""
    a, b = sorted((ua, ub))
    S.put(sf_lane(S.X(a), S.Y(z), b - a, S.k, kind=kind))
    if label:
        S.call(label, (a + b) / 2.0, z + PS_CALL_UP)


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
    if not groups:
        S.notes.append(u"no mixed group fits %.1f-%.1f m (%s)" % (a, b, u", ".join(sorted(mix))))
    for layer, xa, xb, ks, tags in groups:
        t = ps_group_text(ks, tags, why) if call else None
        if not t:
            continue
        top = max([h for k_, x, h, cr, l_ in placed if l_ == layer and xa - 0.5 * cr * S.k <= x <= xb] or [2.0])
        u = S.U(0.5 * (xa + xb))
        S.call(t, u, zf(u) + top * (fig_depth(layer)[0] if layer else 1.0) + 0.6)
    return groups


def ps_back(S, seed, mix=("plane", "ash", "chaste", "olive", "tamarisk")):
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
    ht = max(PLA_SPECIES[k_]["h_m"] for k_ in mix) * PLA_GROUP["size"][1]
    y_top = S.Y(max(z for _u, z in S.prof) + ht)
    wl = sf_atmosphere(0.0, S.w, pr, y_top, S.k, seed=seed, sky="d8", trees=False, birds=False, style=S.style,
                       back_ground={2: pr, 1: pr})
    lab = level_end_labels(S.cid)                               # registry m along the cut (t) -> u: the first end's
    d0, sg = S.d[lab[0]], (-1.0 if lab[0] == "SW" else 1.0)    # distance to the axis; SW positive, NE negative
    lo = min(S.prof[0][1], S.prof[-1][1]) - 0.5                 # the channel: the cut line under both land levels
    cu = [u for u, z in S.prof if z < lo]
    ch = (min(cu), max(cu)) if cu else None
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
            hh = sf_back_house(S.X(ua), S.X(ub), pr, h_m, S.k, layer=layer, floors=fl)
            if not hh or max(p_[1] for s_ in hh for p_ in s_[1]) > y_top:
                nx += 1
                continue
            wl.add("background", hh)
            hs.append((S.X(ua), S.X(ub)))
            nh += 1
        sh, _pl, _gr = pla_group_section(0.0, S.w, gf, S.k, t0=0.45, t1=0.95, mix=list(mix), seed=seed + 31 * layer,
                                         layers=(layer,), style=S.style, density=0.7, avoid=hs or None, hires=False,
                                         detail=False, water=wy)
        wl.add("background", sh)
    wl.put(S.pg)
    S.info.append(u"%d background houses drawn (%d left out: over the channel or above the sky)" % (nh, nx))


def ps_land(S, pts, material="earth"):
    """cut ground under a surface [(u, z)] left to right, down to the drawing's bottom"""
    S.put(sct_ground(S.P(pts), 0.0, S.k, material))


def ps_strip(S):
    """the summer strip channel (PS_STRIP) on the axis: its four points"""
    w, dp = PS_STRIP
    b = S.bed
    return [(-w / 2.0, b), (-w / 2.0 + 0.6, b - dp), (w / 2.0 - 0.6, b - dp), (w / 2.0, b)]


def ps_bed(S, uL, uR, call=u"Stepping stones: cross the summer strip dry-shod", stones=True):
    """the gravel bed from uL to uR with the summer strip, then the M5 water (G8): the average yearly flow over the
    wet bed (never dry), Q100 and Q500 wall to wall (lines only), their levels stacked from S.lab_u; stepping stones
    across the strip (stones=False: none, W1). Returns (u from, u to, level) of the stones' tops: the only place in
    the water people stand."""
    b = S.bed
    st = ps_strip(S)
    S.put(sct_ground(S.P([(uL, b)] + st + [(uR, b)]), 0.0, S.k, "gravel"))
    prof = []
    for i, p in enumerate(S.prof):                              # the cut line with the strip in its bed
        prof.append(p)
        q = S.prof[i + 1] if i + 1 < len(S.prof) else None
        if q and abs(p[1] - b) < 1e-6 and abs(q[1] - b) < 1e-6 and p[0] < st[0][0] and q[0] > st[-1][0]:
            prof += st
    wl = water_section(S.P(prof), S.k, S.Y, cid=S.cid, fill_ground=False, label_size=PS_LBL,
                       label_x=S.X(S.lab_u))
    wl.put(S.pg)
    ua, ub, ztop = st[0][0] - 0.2, st[-1][0] + 0.2, level_avg_flow(S.cid) + PS_STONE_UP
    if not stones:
        return ua, ub, ztop
    S.put(sf_stepping_stones(S.X(ua), S.X(ub), S.Y(st[1][1]), ps_water_y(S), S.k, above_m=PS_STONE_UP,
                             seed=len(S.cid)))
    if call:
        S.call(call, 0.0, ztop + PS_CALL_UP)
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


def ps_bank_text(S, side):
    """what the level table says about a bank, as printed under the section"""
    c = S.cid
    kind, top = ps_kind(c, side), level(c, "top", side)
    h = level(c, "height", side) or level_depth(c, side)
    if kind == "dsi_wall":
        s = u"DSİ stone wall %.2f m · top %s" % (h, ps_lv(top))
    elif kind == "embankment":
        s = u"embankment %.1f° · %.2f m · top %s" % (level(c, "angle_deg", side), h, ps_lv(top))
    elif kind == "loose_earth":
        s = u"loose earth bank %.2f m · top %s" % (h, ps_lv(top))
    else:
        s = u"no crest: the ground keeps rising"
    return u"%s today: %s" % (side, s)


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
    S.call(t, (ua + ub) / 2.0, z + PLA_SPECIES["chaste"]["h_m"] + 0.6)


def ps_sec_w1(S):
    """W1 = p.17's F1 (same registry cut; Aras 31 Oct 12:01 "f1 has better surrounding"): the SW bank's path and
    bike lane under the trees with a bench, the viewing terrace on the NE wall top, the lined reed basins beyond it
    on the NE side, the walled bed at the registry levels. The way into the bed is no straight stair: sitting steps
    cut back into the SW bank in PS_W1_FLIGHTS flights (seat-high risers, treads to sit on), landings with a planted
    pocket between them, a floor at the water's edge on the DSİ wall foot (railed: deeper than PS_RAIL_DROP to the
    bed). No blocks in the bed and nobody in its water."""
    c, b, hw, k = S.cid, S.bed, S.hw, S.k
    tN, tS = level(c, "top", "NE"), level(c, "top", "SW")
    fl = math.ceil((level_avg_flow(c) + PS_W1_FLOOR_UP) * 20.0) / 20.0   # the edge floor, dry at the average flow
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
    S.prof = [(S.u0, tN), (-hw, tN), (-hw, b), (hw, b)] + steps + [(S.u1, tS)]
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
    ys = [p_[1] for s_ in bp if s_[0] in ("poly", "line") for p_ in s_[1]]
    if ys:                                                      # beyond the cut: veiled like p.17 above the ground
        xa_, xb_, ya_, yb_ = S.X(bx[0] - 0.2), S.X(bx[1] + 0.2), S.Y(tN), max(ys) + 0.2   # (the cut land drawn next
        S.put([("poly", [(xa_, ya_), (xb_, ya_), (xb_, yb_), (xa_, yb_)], "FFFFFF", None, 0.1, 0.5)])   # hides the rest)
    ps_land(S, [(S.u0, tN), (-hw, tN)])
    ps_land(S, steps + [(S.u1, tS)])
    ps_lane(S, pa[0], pa[1], tS, "walk", u"Path: shaded by the trees of the SW bank")
    ps_lane(S, bk[0], bk[1], tS, "bike", u"Bike lane: through route under the trees")
    S.put(sf_bench(S.X(bn), sf_seat_x(S.Y(tS), S.X(bn), 0.25 * k), k, side=-1, back=True))
    S.call(u"Bench: in the trees' shade, facing the water", bn - 0.2, tS + PS_CALL_UP)
    ps_bed(S, -hw, hw, call=None, stones=False)                 # no stones, no blocks in the bed (Aras 12:01)
    ps_wall(S, -hw, -1, tN)
    S.put(sf_terrace(S.X(vt[1]), S.Y(tN), PS_TERRACE_W, k, side=-1, material="timber", rail=False))
    S.call(u"View terrace: on the NE wall top, over the bed", sum(vt) / 2.0, tN + PS_CALL_UP)
    # SW: today's wall (dashed) cut down to the edge floor, the sitting steps seated into the bank behind it
    S.pg.poly([S.P([(hw, b), (hw + PS_WALL_T, b), (hw + PS_WALL_T, tS), (hw, tS)])], stroke=COL["ink2"], lw=0.18,
              dash=[0.8, 0.5])
    ps_block_ring(S, hw, hw + PS_WALL_T, S.z0, fl, "stone")    # the wall foot, kept under the floor
    ps_block_ring(S, hw + PS_WALL_T, hw + PS_W1_FLOOR_W, fl - 0.25, fl, "concrete")
    for ua_, ub_, z0, z1 in blocks:
        ps_block_ring(S, ua_, ub_, z0, z1, "stone")
    if fl - b > PS_RAIL_DROP:
        ps_rail(S, hw + 0.15, fl)
    for i, (ua_, ub_, z_) in enumerate(lands):
        ps_pocket(S, ub_ - PS_W1_POCKET[0], ub_, z_, 50 + 3 * i)
    S.call(u"Dashed line: today's DSİ wall, cut back into steps", hw + PS_WALL_T / 2.0, tS + 0.6)
    S.call(u"Edge floor: at the water, dry at the average flow", hw + 0.9, fl + PS_CALL_UP)
    S.call(u"Sitting steps: %d × %d cm seats down to the water" % (n, round(rise * 100)), (hw + u_top) / 2.0,
           (fl + tS) / 2.0 + PS_CALL_UP)
    if lands:
        S.call(u"Landings: a rest between the flights", lands[0][0] + 0.6, lands[0][2] + PS_CALL_UP)
    ps_arrow(S, [(-6.0, b + 0.5), (-hw + 1.2, tN + 2.4), (bx[1] - 0.8, tN + 1.8)], COL["river_mid"], 0.3,
             dash=[0.9, 0.6])                                   # over the terrace's rail and heads to the basins
    S.call(u"Reed basins beyond: stream water cleaned there", sum(bx) / 2.0, tN + 4.0)
    # planting (G9 groups, p.17 F1): the trees of the SW bank round the path and bike lane (their crowns over both),
    # an emergent edge in the wet bed at each wall foot
    ps_group(S, u_top + 0.2, S.u1 - 0.2, lambda u_: tS, 0.50, 0.56, {"plane": 1.0, "ash": 0.6, "chaste": 0.8}, 11,
             layers=(1, 0), avoid=[pa, bk, (bn - 0.6, bn + 0.2)], why={"shade": u"shade the path and bike lane"})
    ps_group(S, -hw + 0.2, -hw + 5.0, lambda u_: b, 0.02, 0.05, ["soft_rush", "loosestrife"], 18, density=1.2,
             why={"cleaning": u"clean the water by the wall"})
    ps_group(S, hw - 5.0, hw - 0.2, lambda u_: b, 0.05, 0.02, ["soft_rush", "loosestrife"], 22, density=1.2,
             why={"cleaning": u"clean the water by the steps"})
    # people as scenes, all looking at the water (focus: the bed's middle): at the floor's railing and sitting on
    # the steps together, one on each landing's way down, on the view terrace; walking the path and riding the bike
    # lane; more further along the path and the terrace (layer 1); nobody in the bed's water ("water": counted)
    ps_zones(S, [("water", -hw, hw, b), ("viewing_terrace", hw + 0.3, hw + PS_W1_FLOOR_W - 0.1, fl)] +
             [("sun_steps", fa + 0.05, fb - 0.05, gstep) for fa, fb in flights], 15, density=1.5, seat_h=rise)
    ps_zones(S, [("walkway", ua_ + 0.1, ub_ - PS_W1_POCKET[0] - 0.1, z_) for ua_, ub_, z_ in lands], 16, max_n=1)
    ps_zones(S, [("viewing_terrace", vt[0] + 0.2, vt[1] - 0.2, tN)], 17, density=1.4, max_n=3)
    ps_zones(S, [("walkway", pa[0], pa[1], tS), ("bike_lane", bk[0], bk[1], tS)], 18)
    ps_zones(S, [("viewing_terrace", vt[0] + 0.2, vt[1] - 0.2, tN), ("walkway", pa[0], pa[1], tS)], 19, layer=1,
             density=0.6, max_n=2)


# ---------------------------------------------------------------- W2 K4 walking hub
def ps_sec_w2(S):
    c, b, hw = S.cid, S.bed, S.hw
    tN, tS = level(c, "top", "NE"), level(c, "top", "SW")
    plat = b + 0.30                                             # sub-hub floor: just above the summer strip
    n, tread = 10, 0.80
    rise = (tS - plat) / n
    u_st = hw + 4.0                                             # the steps start 4.00 m behind today's wall line
    steps, blocks = ps_steps(u_st, plat, n, rise, tread, 1)
    u_sq = u_st + n * tread                                     # the hub square from here, at the wall top level
    S.prof = [(S.u0, tN), (-hw, tN), (-hw, b), (hw, b), (hw, plat), (u_st, plat)] + steps + [(S.u1, tS)]
    S.lab_u = -hw + 0.6                                         # the level labels on the NE side of the strip
    ps_back(S, 21)
    ps_land(S, [(S.u0, tN), (-hw, tN)])
    ps_land(S, [(hw, plat), (u_st, plat)] + steps + [(S.u1, tS)])
    ps_lane(S, -hw - 0.6, -hw - 4.1, tN, "walk", u"Edge walk: looks across to the seating steps")
    ps_lane(S, -hw - 4.5, -hw - 6.5, tN, "bike", u"Bike lane: street side, clear of the walk")
    ua, ub, ztop = ps_bed(S, -hw, hw)
    ps_wall(S, -hw, -1, tN)
    ps_block_ring(S, hw, u_st, plat - 0.25, plat, "concrete")   # sub-hub floor slab
    for ua_, ub_, z0, z1 in blocks:                             # steps seated into the cut-back bank
        ps_block_ring(S, ua_, ub_, z0, z1, "stone")
    ps_block_ring(S, u_sq, S.u1, tS - 0.25, tS, "stone")        # hub square paving
    S.pg.poly([S.P([(hw, b), (hw + PS_WALL_T, b), (hw + PS_WALL_T, tS), (hw, tS)])], stroke=COL["ink2"], lw=0.18,
              dash=[0.8, 0.5])                                  # today's DSİ wall, replaced by the steps
    S.call(u"Dashed line: today's DSİ wall, opened into steps", hw + PS_WALL_T / 2.0, tS + 0.6)
    S.call(u"Sub-hub floor: at the water, just above the flow", (hw + u_st) / 2.0, plat + PS_CALL_UP)
    S.call(u"Seating steps: %d × %d cm, sun and a view of the water" % (n, round(rise * 100)),
           u_st + 0.5 * n * tread, plat + 0.5 * n * rise + PS_CALL_UP)
    S.call(u"Hub square: dry above Q500, in the planes' shade", u_sq + 3.0, tS + PS_CALL_UP)
    xb = S.X(S.u1)                                              # break line: the land goes on to the cut end
    yb, yt = S.Y(S.z0), S.Y(tS)
    S.pg.line([(xb, yb - 0.6), (xb, yb + 0.35 * (yt - yb)), (xb - 0.7, yb + 0.45 * (yt - yb)),
               (xb + 0.7, yb + 0.6 * (yt - yb)), (xb, yb + 0.7 * (yt - yb)), (xb, yt + 0.8)], COL["ink"], 0.2)
    # planting (G9 groups): the square's planes with an understorey (Ottoman squares with plane trees, ICOMOS 2014),
    # street trees behind the NE lanes (layer 1) and at the street side, an emergent edge at the bed's SW side
    ps_group(S, u_sq + 4.0, S.u1 - 0.5, lambda u: tS, 0.48, 0.8, {"plane": 1.0, "chaste": 0.6, "rosemary": 0.5,
                                                                  "lavender": 0.4}, 20, layers=(1, 0),
             why={"shade": u"shade the hub square"})
    ps_group(S, S.u0 + 0.3, -hw - 0.8, lambda u: tN, 0.45, 0.9, {"plane": 1.0, "ash": 0.5, "chaste": 0.9,
                                                                   "rosemary": 0.7}, 21, layers=(1,), call=False)
    ps_group(S, S.u0 + 0.3, -hw - 7.0, lambda u: tN, 0.48, 0.88, {"plane": 1.0, "ash": 0.5, "chaste": 0.9,
                                                                    "rosemary": 0.7}, 22,
             why={"shade": u"shade the street walk"})
    ps_group(S, ub + 1.0, hw - 0.3, lambda u: b, 0.0, 0.14, ["soft_rush", "loosestrife", "rush"], 23,
             why={"cleaning": u"clean the water at the steps"})
    # people by zone: the NE walk and bike lane, across on the stones, children at the water's edge on the dry
    # sub-hub floor, sitting on the steps, walking and standing together in the square; more behind (layer 1)
    ps_zones(S, [("walkway", -hw - 4.1, -hw - 0.6, tN), ("bike_lane", -hw - 6.5, -hw - 4.5, tN),
                 ("water", -hw, ua, b), ("stepping_stones", ua, ub, ztop), ("water", ub, hw, b),
                 ("walkway", u_sq + 0.5, S.u1 - 1.0, tS)], 24)
    ps_zones(S, [("lawn", hw + 0.3, u_st - 0.3, plat)], 26, density=1.4)   # children playing together at the water
    ps_zones(S, [("sun_steps", u_st + 0.2, u_sq - 0.2, ps_stair_z(u_st, plat, n, rise, tread, 1))], 27, density=1.6,
             seat_h=rise)                                       # sitting together on the steps, facing the water
    ps_zones(S, [("walkway", S.u0 + 0.5, -hw - 0.6, tN), ("walkway", u_sq + 0.5, S.u1 - 1.0, tS)], 25, layer=1,
             density=0.6)


# ---------------------------------------------------------------- W3 K5 Demeter's Garden
def ps_sec_w3(S):
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
    S.prof = list(reversed([(-hw, b)] + steps)) + [(hw, b), (s0, shelf), (s1, shelf), (s1, gf), (S.u1, gf)]
    S.prof = [(S.u0, tN)] + S.prof
    S.lab_u = -1.9                                              # level labels over the water, clear of the SW slope
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
    ps_lane(S, crest - 3.6, crest - 0.3, tN, "walk", u"Crest walk: looks down the steps to the water")
    # SW: the stream commons on the shelf, the garden raised above Q500 behind a stone wall
    ps_block_ring(S, s1, s1 + 0.40, shelf - 0.30, gf + 0.15, "stone")
    S.call(u"Bank steps: %d × %d cm, sit or walk down to the bed" % (n, round(rise * 100)), -hw - run * 0.45,
           b + (tN - b) * 0.45 + PS_CALL_UP)
    S.call(u"Stream commons: open ground the floods may cover", (s0 + s1) / 2.0, shelf + PS_CALL_UP)
    S.call(u"Demeter's Garden: raised above Q500, stays dry", s1 + 1.5, gf + PS_CALL_UP)
    gy = lambda u: shelf + (b - shelf) * max(0.0, min(1.0, (s0 - u) / (s0 - hw)))
    S.call(u"Wet edge: floods at Q100, holds the bank", (hw + s0) / 2.0, gy((hw + s0) / 2.0) + PS_CALL_UP)
    # planting (G9 groups): a mixed wet edge on the slope up to the commons (wet to drier, emergent only under the
    # water), the garden's trees, shrubs and herbs around the tomato rows, the café's plane a step behind (layer 1)
    ps_group(S, hw + 0.4, s0 - 0.3, gy, 0.0, 0.42, ["soft_rush", "loosestrife", "rush", "willow", "tamarisk"], 33,
             layers=(1, 0), why={"cleaning": u"clean the water", "shade": u"shade the edge"})
    rows = (s1 + 2.6, s1 + 7.0)
    S.put(sf_seat(pla_crop_rows("tomato", S.X(rows[0]), S.X(rows[1]), S.Y(gf), k, spacing=1.0, h_m=1.0,
                                crown_m=0.8), S.Y(gf)))
    S.call(u"Tomato rows: the garden's crop, above the flood", sum(rows) / 2.0, gf + PS_CALL_UP)
    ps_group(S, s1 + 0.6, S.u1 - 0.3, lambda u: gf, 0.5, 0.95, {"plane": 0.6, "olive": 1.0, "chaste": 0.8,
                                                                "rosemary": 0.7, "lavender": 0.7}, 34,
             layers=(1, 0), avoid=[(rows[0] - 0.2, rows[1] + 0.2)],
             why={"shade": u"shade the café", "perception": u"seasonal colour"})
    # people by zone: on the crest walk, sitting and walking on the bank steps, across on the stones, children and
    # families on the commons; a gardener at the tomato rows and a café guest (dry garden floor, hand-placed)
    ps_zones(S, [("walkway", crest - 3.6, crest - 0.3, tN),
                 ("sun_steps", crest + 1.6, -hw - 0.4, ps_stair_z(-hw, b, n, rise, tread, -1)),
                 ("water", -hw, ua, b), ("stepping_stones", ua, ub, ztop), ("water", ub, s0, gy)], 35, seat_h=rise)
    ps_zones(S, [("lawn", s0 + 1.0, s1 - 1.0, shelf)], 37, density=1.4)    # families on the commons by the water
    ps_zones(S, [("lawn", s0 + 1.0, s1 - 1.0, shelf)], 36, layer=1, density=0.6)
    ps_fig(S, "stand", s1 + 5.2, gf, facing=-1)                # at the tomato rows
    ps_fig(S, "sit_step", s1 + 13.6, gf, facing=-1)            # café under the plane
    S.call(u"Café: guests under the plane by the garden", s1 + 13.6, gf + PS_CALL_UP)


# ---------------------------------------------------------------- W4 downstream reach
def ps_sec_w4(S):
    c, b, hw, k = S.cid, S.bed, S.hw, S.k
    tN, aN = level(c, "top", "NE"), level(c, "angle_deg", "NE")
    tS, aS = level(c, "top", "SW"), level(c, "angle_deg", "SW")
    q1, q5 = level(c, "q100"), level(c, "q500")
    gN, gS = math.tan(math.radians(aN)), math.tan(math.radians(aS))
    cN, cS = -hw - (tN - b) / gN, hw + (tS - b) / gS            # crests (u)
    S.prof = [(S.u0, tN), (cN, tN), (-hw, b), (hw, b), (cS, tS), (S.u1, tS)]
    S.lab_u = 1.9
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
    ps_lane(S, cN - 0.3, cN - 2.8, tN, "walk", u"Crest walk: above Q500, beside the corridor")
    ps_lane(S, cN - 3.2, cN - 5.2, tN, "bike", u"Bike lane: along the crest, clear of the walk")
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
    S.call(u"Ramp: step-free from the crest to the terrace", (cN + uT) / 2.0, (tN + tT) / 2.0 + PS_CALL_UP)
    S.put(sf_terrace(S.X(uT), S.Y(tT), PS_TERRACE_W, k, side=1, material="timber", rail=False))
    u = uT + 0.4
    while u < uW:                                               # the terrace's piles down into the bank
        S.pg.line(S.P([(u, tT - 0.25), (u, zN(u) - 0.6)]), PS_TIMBER, 0.35)
        u += 1.8
    S.call(u"Viewing terrace: above Q500, looks over the water", (uT + uW) / 2.0, tT + PS_CALL_UP)
    sh, _ = sf_stairs(S.X(ub), S.Y(dk), ns, rs, PS_STAIR[0], k, side=-1, material="concrete", rail=True)
    S.put(sh)
    S.pg.poly([S.P([(ua, dk - 0.20), (ua, dk), (ub, dk), (ub, dk - 0.20)])], fill=PS_TIMBER, stroke=SCT["cut"],
              lw=0.25)
    u = ub + 0.3
    while u < ua - 0.3:                                         # piles down into the bank and the bed
        S.pg.line(S.P([(u, dk - 0.20), (u, min(zN(u), b) - 0.6)]), PS_TIMBER, 0.35)
        u += 2.0
    ps_rail(S, ua + 0.1, dk)
    S.call(u"Boardwalk: floods at Q100, out over the wet edge", (ua + ub) / 2.0, dk + PS_CALL_UP)
    # planting (G9 groups): the crest corridor (trees and shrubs, layers 2-0), a wet edge under the terrace and
    # boardwalk, the SW slope wet to dry; the field behind the SW crest takes the surplus water
    ps_group(S, S.u0 + 0.3, cN - 5.6, lambda u: tN, 0.45, 0.9,
             {"plane": 1.0, "ash": 0.5, "chaste": 1.0, "rosemary": 0.8, "olive": 0.6}, 42, layers=(2, 1, 0),
             why={"shade": u"shade the crest"})
    S.call(u"Ecological corridor: trees and shrubs along the crest", (S.u0 + cN - 5.6) / 2.0, tN + 0.5)
    ps_group(S, uT + 0.3, -hw - 0.2, zN, 0.0, 0.16, ["soft_rush", "loosestrife", "rush"], 43,
             why={"cleaning": u"clean the water under the deck"})
    ps_group(S, hw + 0.3, cS - 0.6, zS, 0.0, 0.5, ["soft_rush", "loosestrife", "willow", "tamarisk", "chaste"], 44,
             layers=(1, 0), why={"shade": u"shade the slope", "cleaning": u"clean the water"})
    S.put(sf_seat(pla_crop_rows("cotton", S.X(cS + 1.0), S.X(S.u1 - 0.4), S.Y(tS), k, spacing=0.9, h_m=1.0,
                                crown_m=0.6), S.Y(tS)))
    S.call(u"Cotton field: takes the surplus water", (cS + S.u1) / 2.0, tS + PS_CALL_UP)
    # people by zone: cycling and walking on the crest, down the ramp, sitting and standing on the terrace, on the
    # boardwalk, across on the stones; more along the crest behind the cut (layer 1); a farmer in the field
    ps_zones(S, [("walkway", cN - 2.8, cN - 0.3, tN), ("bike_lane", cN - 5.2, cN - 3.2, tN),
                 ("walkway", cN + 1.0, uT - 1.0, lambda u: tN - (u - cN) * PS_RAMP),
                 ("walkway", ub - 0.3, ua + 0.3, dk),
                 ("water", -hw, sa, b), ("stepping_stones", sa, sb, ztop), ("water", sb, hw, b)], 45)
    ps_zones(S, [("viewing_terrace", uT + 0.3, uW - 0.3, tT)], 47, density=1.5)   # together at the view over the water
    ps_zones(S, [("walkway", cN - 2.8, cN - 0.3, tN)], 46, layer=1, density=0.6)
    ps_fig(S, "stand", S.u1 - 1.2, tS, facing=-1)


PS_DRAW = {"W1": ps_sec_w1, "W2": ps_sec_w2, "W3": ps_sec_w3, "W4": ps_sec_w4}


# ---------------------------------------------------------------- callouts on the section, data rows and key under it
def ps_scale_bar(pg, x, y, k):
    """0-5-10-20 m at k mm per m from (x, y), its numbers over it, the round scale after it: the A0 SHEET's scale
    (PS_SCALE x BK_S, standard), which the booklet re-sets to the scale it prints (1:500, D6); the scale text only
    from sf_scale_text"""
    h, col = 0.9, COL["ink"]
    marks = (0, 5, 10, 20)
    for i, (a, b_) in enumerate(zip(marks[:-1], marks[1:])):
        pg.poly([rect(x + a * k, y, x + b_ * k, y + h)], fill=(col if i % 2 == 0 else COL["white"]), stroke=col,
                lw=0.15)
    for m_ in marks:
        pg.text(str(m_), x + m_ * k, y + h + 0.6, PS_LBL, col, align="C")
    pg.text(u"m · " + sf_scale_text(round(PS_SCALE * BK_S)), x + 20 * k + text_w(u"20", PS_LBL) / 2.0 + 1.2,
            y + h + 0.6, PS_LBL, col)


def ps_marks(S):
    """the callout circles (SfCallouts): each near its element, moved up until it touches no other circle and none
    of the water level labels (the box from S.lab_u over the average flow to Q500)"""
    r = 0.75 * PS_CO
    lx = S.X(S.lab_u)
    busy = [(lx - r, S.Y(level_avg_flow(S.cid)) - 2.5 * PS_LBL, lx + text_w(u"average flow +00.00", PS_LBL) + r,
             S.Y(level(S.cid, "q500")) + 1.5 * PS_LBL)]
    done = []
    for t, u, z in S.calls:
        x = max(r, min(S.w - r, S.X(u)))
        y = S.Y(z) + r
        for _i in range(40):
            hit = [p for p in done if math.hypot(p[0] - x, p[1] - y) < 2.0 * r + 0.4]
            box = [q for q in busy if q[0] - r < x < q[2] + r and q[1] - r < y < q[3] + r]
            if not hit and not box:
                break
            y = max([p[1] + 2.0 * r + 0.4 for p in hit] + [q[3] + r + 0.2 for q in box])
        done.append((x, y))
        S.co.add(x, y, t)
    S.put(S.co.marks(size=PS_CO))


def ps_finish(S, log, room_w=None):
    """G6 check, the callout circles, the bank / bed rows under the drawing, the callout key under them (in as many
    columns as room_w allows: every number explained), the scale bar"""
    pg = S.pg
    for m_ in sf_assert_g6(S.k, trees=S.trees, strict=False):  # G6: people 1.75 m, trees in their sourced range
        log.append(u"G6 CHECK section %s (style %s): %s" % (S.cid, S.style, m_))
    for m_ in S.notes:
        log.append(u"NOTE section %s planting: %s" % (S.cid, m_))
    for m_ in S.info:
        log.append(u"section %s: %s" % (S.cid, m_))
    S.co = SfCallouts()
    ps_marks(S)
    # under the drawing: the bed width as a dimension, each bank as the level table has it
    hw = S.hw
    y = -1.0
    xa, xb = S.X(-hw), S.X(hw)
    pg.line([(xa, y), (xb, y)], COL["ink"], 0.15)
    for x_ in (xa, xb):
        pg.line([(x_, y - 0.5), (x_, y + 0.6)], COL["ink"], 0.15)
    rows = []
    under = [(u"bed {:,.0f} cm · {}".format(level(S.cid, "bed_width_cm"), ps_lv(S.bed)), "C", (xa + xb) / 2.0),
             (ps_bank_text(S, "NE"), "L", 0.0), (ps_bank_text(S, "SW"), "R", S.w)]
    last = 0
    for t, al, x_ in under:
        w = text_w(t, PS_LBL)
        x0 = x_ - (w / 2.0 if al == "C" else (w if al == "R" else 0.0))
        r = 0
        while any(x0 < b_ + 2.0 and a_ < x0 + w + 2.0 for rr, a_, b_ in rows if rr == r):
            r += 1
        rows.append((r, x0, x0 + w))
        last = max(last, r)
        pg.text(t, x0, -1.6 - PS_LBL * CAP - r * PS_ROW, PS_LBL, COL["ink"])
    # the key: one line per number, "Element: reason", in columns under the rows
    yk = -1.6 - PS_LBL * CAP - last * PS_ROW - 2.0
    items = sorted(set((n, t) for n, _x, _y, t in S.co.items))
    if items:
        colw = max(text_w(t, PS_CO) for _n, t in items) + 2.0 * PS_CO + 3.0
        ncol = max(1, min(len(items), int(((room_w or S.w) + 3.0) // colw)))
        nrow = int(math.ceil(len(items) / float(ncol)))
        for c_ in range(ncol):
            part = items[c_ * nrow:(c_ + 1) * nrow]
            if not part:
                continue
            co = SfCallouts(start=part[0][0])
            for _n, t in part:
                co.add(0.0, 0.0, t)
            S.put(co.key(c_ * colw, yk, size=PS_CO))
        yk -= nrow * 1.5 * PS_CO
    ps_scale_bar(pg, 0.0, yk - 3.6, S.k)


def ps_section(cid, log, style="b", room_w=None):
    """one cut as a Page in print mm (see PsSec), in style b (vector) or a (cutouts, D1); room_w = the panel's
    width for the callout key (print mm)"""
    u0, u1, d = ps_extent(cid)
    S = PsSec(cid, u0, u1, d, style)
    PS_DRAW[cid](S)
    ps_finish(S, log, room_w)
    return S.pg


# ---------------------------------------------------------------- the page block: key map strip + 2 x 2 sections
PS_GAP = 4.0                           # print mm between the panels
PS_LEG_H = 9.0                         # print mm: the legend band at the block's bottom (two rows)


def ps_badge(pg, x, y, n, r=2.0):
    """the cut's number on the page (section titles and key map alike)"""
    pg.circle(x, y, r, fill=COL["accent"])
    fs = r * 1.15
    pg.text(str(n), x, y - fs * CAP / 2.0, fs, COL["white"], bold=True, align="C")


def ps_cell(pg, box, n, cid, name, take, note):
    """one section's panel: white ground, a coloured rule, the badge, the title (cut and name bold, the takeaway) and
    the key line under it. Returns the box left for the drawing (print mm)."""
    x0, y0, x1, y1 = box
    pg.poly([rect(x0, y0, x1, y1)], fill=COL["white"], stroke=COL["faint"], lw=0.25)
    pg.poly([rect(x0, y1 - 0.8, x1, y1)], fill=MP["discharge"][1])
    yt = y1 - 0.8 - 2.0 - PS_TTL * CAP                         # the title's baseline
    ps_badge(pg, x0 + 4.5, yt + PS_TTL * CAP / 2.0, n)
    yb, _ = ps_rich_para(pg, x0 + 8.0, yt + PS_TTL * 1.28, x1 - x0 - 11.0, u"**%s · %s** %s" % (cid, name, take),
                         PS_TTL, COL["ink_dark"])
    yb, _ = ps_rich_para(pg, x0 + 8.0, yb - 0.6, x1 - x0 - 11.0, note, PS_NOTE, COL["ink"])
    return (x0 + 3.0, y0 + 2.5, x1 - 3.0, yb - PS_NOTE * 0.25 - 2.0)


def ps_note(cid):
    """the key line of a section, from the level table"""
    q5 = level(cid, "q500")
    if cid == "W1":
        return u"Q500 %s stays **%.2f m** under the DSİ walls · reeds only in lined basins the flood passes by" % (
            ps_lv(q5), level(cid, "top", "SW") - q5)
    if cid == "W2":
        return u"Q500 %s stays **%.2f m** under the hub square · the steps flood, the square stays dry" % (
            ps_lv(q5), level(cid, "top", "SW") - q5)
    if cid == "W3":
        return u"Q500 %s · garden floor **%s** stays dry: olive and lavender need soil that never waterlogs" % (
            ps_lv(q5), ps_lv(math.ceil((q5 + PS_FREEBOARD) * 20.0) / 20.0))
    return u"Q500 %s stays **%.2f m** under the NE bank top · wet edge, boardwalk and trees by flood level" % (
        ps_lv(q5), level(cid, "top", "NE") - q5)


def ps_legend(pg, x0, x1, y1):
    """G1: the samples of everything the sections draw, in rows from the top y1 across x0-x1 (print mm), next to the
    drawings inside the block. Returns the band's bottom y."""
    P = _wat_pal()
    rows = [("water", u"water at the average yearly flow"),
            ("q100", u"Q100 flood level"), ("q500", u"Q500 flood level"),
            (SCT["stone"], u"stone: DSİ walls, steps, garden wall"), (SCT["concrete"], u"concrete: stairs, ramp, basins"),
            (SCT["earth"], u"earth"), (SCT["gravel"], u"gravel bed"), (PS_TIMBER, u"timber: terrace, boardwalk"),
            (SF_LANE["walk"], u"walk paving"), (SF_LANE["bike"], u"bike lane")]
    sw, gap, x, y = 5.0, 4.0, x0, y1 - PS_ROW
    for kind, lab in rows:
        w = sw + 1.2 + text_w(lab, PS_LBL)
        if x + w > x1 and x > x0:
            x, y = x0, y - PS_ROW
        cy = y + PS_LBL * CAP / 2.0
        if kind in ("q100", "q500"):
            pg.line([(x, cy), (x + sw, cy)], P[kind], 0.3, dash=[1.2, 0.6] if kind == "q100" else [0.4, 0.5])
        else:
            fill = {"water": P["sec"]}.get(kind, kind)
            pg.poly([rect(x, cy - 1.0, x + sw, cy + 1.0)], fill=fill, stroke=COL["faint"], lw=0.1)
            if kind == "water":
                pg.line([(x, cy + 1.0), (x + sw, cy + 1.0)], SEC["hatch"], 0.3)
        pg.text(lab, x + sw + 1.2, y, PS_LBL, COL["ink"])
        x += w + gap
    return y - 0.25 * PS_LBL


def ps_block(log, style="b"):
    """page 12 (p13 before): the key map strip across the top (it serves all four sections), the four sections under
    it in reading order, all at 1:500, the legend band at the bottom, in print mm (0, 0)-(BK_W, BK_H), in style b or
    a (D1). Returns (Page, {sheet key: panel box})."""
    pg = Page(BK_W, BK_H)
    tri = sf_triangles(walls=False, aggregate=False)            # U22: no meaningless triangles in the sections
    yk = BK_H - PS_KEY_H
    ps_key_strip(pg, (0.0, yk, BK_W, BK_H), log)
    yl = PS_LEG_H
    ps_legend(pg, 0.0, BK_W, yl)
    cw = (BK_W - PS_GAP) / 2.0
    ch = (yk - yl - 2.0 * PS_GAP) / 2.0
    boxes = {}
    for i, (key, cid, n, name, take) in enumerate(PS_CUTS):
        x0 = (i % 2) * (cw + PS_GAP)
        y1 = yk - PS_GAP - (i // 2) * (ch + PS_GAP)
        box = (x0, y1 - ch, x0 + cw, y1)
        boxes[key] = box
        inner = ps_cell(pg, box, n, cid, name, take, ps_note(cid))
        sec = ps_section(cid, log, style, room_w=inner[2] - inner[0])
        b = ps_bbox(sec.items)
        if b[2] - b[0] > inner[2] - inner[0] + 0.01 or b[3] - b[1] > inner[3] - inner[1] + 0.01:
            log.append(u"NOTE section %s: %.0f x %.0f mm at 1:%d, room %.0f x %.0f mm (kept to scale)" % (
                cid, b[2] - b[0], b[3] - b[1], PS_SCALE, inner[2] - inner[0], inner[3] - inner[1]))
        else:                                                  # D6: 1:500 is the largest standard scale that fits
            den = sf_scale_pick((b[2] - b[0]) / PS_K, inner[2] - inner[0], min_den=PS_SCALE)
            if den != PS_SCALE:
                log.append(u"NOTE section %s: fits only at 1:%d" % (cid, den))
        dx = (inner[0] + inner[2]) / 2.0 - (b[0] + b[2]) / 2.0
        dy = inner[1] - b[1]
        pg.items += ps_xform(sec.items, 1.0, dx, dy)
    sf_triangles(**tri)
    log.append(u"sections (v10, revision 30 Oct style %s): W1-W4 at 1:%d on the booklet page, looking downstream"
               % (style, sf_scale_ok(PS_SCALE)))
    log.append(sf_g14_line())                                   # G14: items seated, people refused in the water
    return pg, boxes
