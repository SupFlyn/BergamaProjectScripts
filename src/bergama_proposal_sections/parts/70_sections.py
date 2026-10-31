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
PS_SCALE = 500                       # 1:500 on the booklet page (standard scales, SCRIPT_STANDARD §8)
PS_K = 1000.0 / PS_SCALE              # print mm per m (k of section_parts and plants)
PS_DEPTH = 1.0                        # m of cut ground drawn under the bed (section_parts drawing rule)
PS_WALL_T = 0.60                      # m: DSİ wall thickness: no sourced value; the same 0.60 m as p.04-05 (site board P45_WALL_T_M, G2)
PS_RAIL_H = 1.10                      # m: railing height on the wall and bank tops: drawing value
PS_KERB_H = 0.15                      # m: basin kerb above the ground: drawing value
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
PS_CUTS = [("up", "W1", 1, u"Upstream entry", u"runoff cleaned in lined reed basins, given back in summer"),
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


def ps_zones(S, zones, seed, layer=0, density=1.0, max_n=None):
    """G10 people zone by zone (figures.py fig_place_zones): zones [(kind, ua, ub, ground)] with ground = a level
    (m) or a function of u (m) -> level; kinds walkway, bike_lane, viewing_terrace, sun_steps, stepping_stones, lawn
    take people, "water" none (counted in the G14 line). The average-flow water is passed, so nobody stands where
    the drawn water covers the ground; layer 1 / 2 = people further from the cut (smaller, paler)."""
    zz = []
    for kind, ua, ub, g in zones:
        zz.append((kind, S.X(min(ua, ub)), S.X(max(ua, ub)), S.zf(g) if callable(g) else S.Y(g)))
    sh, placed = fig_place_zones(zz, S.Y(S.bed), S.k, seed=seed, layer=layer, style=S.style, density=density,
                                 water=ps_water_y(S), max_per_zone=max_n)
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
    """the D8 sky and the depth behind the cut (R16): faded mixed tree groups in D9 layers 2 and 1, each layer on
    its own ground = the cut line with the bed (G14), none where that ground lies under the average-flow water"""
    pr = ps_gprof(S)
    ht = max(PLA_SPECIES[k_]["h_m"] for k_ in mix) * PLA_GROUP["size"][1]
    y_top = S.Y(max(z for _u, z in S.prof) + ht)
    wl = sf_atmosphere(0.0, S.w, pr, y_top, S.k, seed=seed, sky="d8", birds=False, mix=list(mix), style=S.style,
                       back_ground={2: pr, 1: pr}, groups=True, water=ps_water_y(S))
    wl.put(S.pg)


def ps_land(S, pts, material="earth"):
    """cut ground under a surface [(u, z)] left to right, down to the drawing's bottom"""
    S.put(sct_ground(S.P(pts), 0.0, S.k, material))


def ps_strip(S):
    """the summer strip channel (PS_STRIP) on the axis: its four points"""
    w, dp = PS_STRIP
    b = S.bed
    return [(-w / 2.0, b), (-w / 2.0 + 0.6, b - dp), (w / 2.0 - 0.6, b - dp), (w / 2.0, b)]


def ps_bed(S, uL, uR, call=u"Stepping stones: cross the summer strip dry-shod"):
    """the gravel bed from uL to uR with the summer strip, then the M5 water (G8): the average yearly flow over the
    wet bed (never dry), Q100 and Q500 wall to wall (lines only), their levels stacked from S.lab_u; stepping stones
    across the strip. Returns (u from, u to, level) of the stones' tops: the only place in the water people stand."""
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
def ps_sec_w1(S):
    c, b, hw = S.cid, S.bed, S.hw
    tN, tS = level(c, "top", "NE"), level(c, "top", "SW")
    S.prof = [(S.u0, tN), (-hw, tN), (-hw, b), (hw, b), (hw, tS), (S.u1, tS)]
    ps_back(S, 11)
    ps_land(S, [(S.u0, tN), (-hw, tN)])                         # NE: the street behind the wall
    # SW: three lined reed basins sunk into the land (D2 a: lined, root-contained, the flood passes by above Q500),
    # floors stepping down toward the stream: street runoff in at the far one, cleaned water out through the wall
    kt = 0.15                                                   # basin kerb / slab (plants module drawing rule)
    bas = [(23.0, 28.0, 1.10), (29.5, 34.5, 0.90), (36.0, 41.0, 0.70)]   # (u from, u to, floor under the ground m)
    surf = [(hw, tS)]
    for u0, u1, dp in bas:
        f = tS - dp - kt
        surf += [(u0 - kt, tS), (u0 - kt, f), (u1 + kt, f), (u1 + kt, tS)]
    surf.append((S.u1, tS))
    ps_land(S, surf)
    # NE street, from the wall: a walk along the edge, the bike lane behind it, shade trees at the street side
    ps_lane(S, -hw - 0.6, -hw - 3.6, tN, "walk", u"Edge walk: looks down into the bed")
    ps_lane(S, -hw - 4.0, -hw - 6.0, tN, "bike", u"Bike lane: street side, clear of the walk")
    ps_lane(S, hw + 0.8, hw + 3.8, tS, "walk", u"Basin walk: along the cleaning basins")
    # the way down: a stone stair from the NE wall top into the bed (it floods), its rail on the open side, and a
    # line of stepping stones from its foot across the bed and the summer strip: what people do down there
    n = int(math.ceil((tN - b) / PS_STAIR[1]))
    rise, tread = (tN - b) / n, PS_STAIR[0]
    u_bot = -hw + n * tread
    ua, ub, ztop = ps_bed(S, -hw, hw, call=u"Stepping stones: stair foot across the bed, dry-shod")
    S.put(sf_stepping_stones(S.X(u_bot + 0.1), S.X(ua - 0.3), S.Y(b), ps_water_y(S), S.k, above_m=PS_STONE_UP,
                             seed=5))
    ps_wall(S, -hw, -1, tN, rail=False)                         # the stair's head opens the NE wall
    ps_wall(S, hw, 1, tS)
    sh, _ = sf_stairs(S.X(u_bot), S.Y(b), n, rise, tread, S.k, side=-1, material="stone", rail=True)
    S.put(sh)
    S.call(u"Stair: the way down into the bed, %d × %d cm" % (n, round(rise * 100)), -hw + n * tread * 0.5,
           b + (tN - b) * 0.5 + 1.2)
    # planting (G9 groups): street trees behind the lanes (layer 1) and at the street side, an emergent edge in the
    # wet bed along the SW wall, shrubs between the SW walk and the basins
    ps_group(S, S.u0 + 0.3, -hw - 0.8, lambda u: tN, 0.45, 0.9, {"plane": 1.0, "ash": 0.5, "chaste": 0.9,
                                                                   "rosemary": 0.6}, 12, layers=(1,), call=False)
    ps_group(S, S.u0 + 0.3, -hw - 6.4, lambda u: tN, 0.45, 0.7, {"plane": 1.0, "chaste": 0.8, "rosemary": 0.6}, 13,
             why={"shade": u"shade the street walk"})
    ps_group(S, hw - 7.0, hw - 0.4, lambda u: b, 0.0, 0.16, ["soft_rush", "loosestrife", "rush"], 14,
             why={"cleaning": u"clean the released water"})
    ps_group(S, hw + 4.2, bas[0][0] - 0.6, lambda u: tS, 0.5, 0.92, ["chaste", "rosemary", "lavender", "olive"], 15,
             layers=(1, 0), why={"perception": u"seasonal colour by the walk"})
    for i, (u0, u1, dp) in enumerate(bas):
        f = tS - dp
        S.put(pla_reed_basin(S.X(u0), S.X(u1), S.Y(f), S.Y(tS), S.k, PS_KERB_H, media_m=0.50,
                             wl_y=S.Y(f + 0.65)))
    S.call(u"Lined reed basins: clean runoff, above Q500", 32.0, tS + 2.9)
    f_near, f_far = tS - bas[0][2], tS - bas[2][2]
    ps_arrow(S, [(S.u1 - 0.2, tS + 2.6), (41.4, tS + 1.4), (39.5, f_far + 0.85)], COL["river_mid"], 0.3)
    S.call(u"Runoff in: street and roof water to the basins", S.u1 - 0.6, tS + 2.6)
    ps_arrow(S, [(bas[0][0] - 0.3, f_near + 0.45), (hw + PS_WALL_T, f_near + 0.45), (hw - 0.1, f_near + 0.45),
                 (hw - 1.4, b + 0.25)], COL["river_dark"], 0.3, dash=[0.8, 0.4])
    S.call(u"Summer release: cleaned water back to the strip", hw - 0.7, f_near + 0.6)
    # people by zone: the edge walk and bike lane, down the stair's dry treads, across on the stones, along the
    # basins; nobody in the water itself; a few more further along the street (layer 1)
    stair = ps_stair_z(u_bot, b, n, rise, tread, -1)
    ps_zones(S, [("walkway", -hw - 3.6, -hw - 0.6, tN), ("bike_lane", -hw - 6.0, -hw - 4.0, tN)], 15)
    ps_zones(S, [("walkway", -hw + 0.3, u_bot - 0.3, stair)], 16, max_n=2)
    ps_zones(S, [("stepping_stones", u_bot + 0.1, ub, ztop), ("water", ub, hw, b),
                 ("walkway", hw + 0.8, hw + 3.8, tS)], 17)
    ps_zones(S, [("walkway", S.u0 + 0.5, -hw - 0.6, tN)], 18, layer=1, density=0.6)


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
                 ("lawn", hw + 0.3, u_st - 0.3, plat),
                 ("sun_steps", u_st + 0.2, u_sq - 0.2, ps_stair_z(u_st, plat, n, rise, tread, 1)),
                 ("walkway", u_sq + 0.5, S.u1 - 1.0, tS)], 24)
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
                 ("water", -hw, ua, b), ("stepping_stones", ua, ub, ztop), ("water", ub, s0, gy),
                 ("lawn", s0 + 1.0, s1 - 1.0, shelf)], 35)
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
                 ("viewing_terrace", uT + 0.3, uW - 0.3, tT), ("walkway", ub - 0.3, ua + 0.3, dk),
                 ("water", -hw, sa, b), ("stepping_stones", sa, sb, ztop), ("water", sb, hw, b)], 45)
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
