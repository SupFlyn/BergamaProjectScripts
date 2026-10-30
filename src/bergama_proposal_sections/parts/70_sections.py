# ================================================================ v10 the four proposal sections, true to the cut
# v10 (revision 29 Oct, WO-T3b-3; package C "Page 13", brief 02 §3-§6): the sketches are gone. Each section is drawn
# at 1:500 on the booklet page from the level table (common/levels.py: bed, bed width, bank and wall tops, bank type
# and angle, terraces, Q100, Q500) with the shared section parts (DSİ walls, embankments, loose earth, railings,
# stone / concrete / earth / gravel hatches, steps seated into the bank) and the plants module (every species at its
# true size and form; D6: no fig, citrus, iris, oleander, white poplar; D2: common reed only in lined basins the flood
# passes by). Figures through ps_fig / ps_people (M7, revision 30 Oct). All four sections
# look downstream: the NE bank (left bank) on the left, the SW bank on the right, as the key map's triangles show.
# Drawn in booklet print mm (k = PS_K mm per m); build_sheet() places the block on the A0 sheet at 1 / BK_S.
# Revision 30 Oct (T6, booklet p12): people are the M7 figures at 1.75 m (D9 layer 0 at the cut), plants the M6
# species at their sourced heights in mixed, wet-to-dry scatters (G9), checked by sf_assert_g6 (G6); the water is the
# M5 section (average yearly flow, never dry; Q100 / Q500 from the cut registry); every bank is a designed place with
# its reason (G10): walks, bike lanes, a stair down the W1 wall into the bed, life in the wet bed, the W4 ramp to a
# viewing terrace and the boardwalk; faded trees behind the cut (R16). Each section is drawn in style "b" (vector)
# and "a" (cutouts, D1) from the same geometry (PsSec.style).
PS_SCALE = 500                        # 1:500 on the booklet page (standard scales, SCRIPT_STANDARD §8)
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
PS_FLOOD = "C1D3DB"                   # the reach of Q500 (wash, see-through)
PS_FLOOD_A = 0.55
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
        self.labels = []                                      # (text, u, z of the thing's top, proposal?)
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

    def lab(self, text, u, z, prop=False):
        self.labels.append((text, u, z, prop))


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


def ps_fig(S, pose, u, z, facing=1, **p):
    """one person at the cut (M7: adult 1.75 m, cyclist 1.80 m, D9 layer 0), feet at (u, z), in the section's style"""
    S.put(fig_side(pose, S.X(u), S.Y(z), S.k, facing=facing, style=S.style, **p))


def ps_people(S, zone, ua, ub, zf, seed, water=None, **p):
    """people doing what the zone is for (M7 FIG_ACTIVITY) from ua to ub (m) on the ground zf(u) (m a.s.l.); water =
    the water level (m) for wading figures"""
    a, b = sorted((ua, ub))
    sh, placed = fig_activity(zone, S.X(a), S.X(b), S.zf(zf), S.k, seed=seed, style=S.style,
                              water=(S.Y(water) if water is not None else None), **p)
    S.put(sh)
    return placed


def ps_lane(S, ua, ub, z, kind, label=None):
    """an M8 lane (walk, bike, gravel, timber) from ua to ub on level z; label = the zone and its reason (G10)"""
    a, b = sorted((ua, ub))
    S.put(sf_lane(S.X(a), S.Y(z), b - a, S.k, kind=kind))
    if label:
        S.lab(label, (a + b) / 2.0, z, True)


def ps_scatter(S, ua, ub, zf, t0, t1, mix, seed, density=1.0, avoid=(), label=True):
    """mixed planting (M6) from ua to ub (m) on the ground zf(u): band t0 (wet) to t1 (dry), crowns overlapping, no
    rows or repeated clusters (G9); each species named once over the drawing"""
    a, b = sorted((ua, ub))
    if b - a < 0.3:
        return []
    av = [tuple(sorted((S.X(p), S.X(q)))) for p, q in avoid] or None
    sh, placed = pla_scatter_section(S.X(a), S.X(b), S.zf(zf), S.k, t0=t0, t1=t1, mix=mix, seed=seed,
                                     style=S.style, density=density, avoid=av)
    S.put(sh)
    for key, x, h, cr in placed:
        S.trees.append((key, x, h, cr))
        if label:
            u = S.U(x)
            S.lab(ps_name(key), u, zf(u) + h)
    return placed


def ps_back(S, seed):
    """depth behind the cut (R16): faded trees in D9 layers 2 and 1, standing at the bank tops (never in the bed)"""
    top = min(S.prof[0][1], S.prof[-1][1])
    wl = sf_atmosphere(0.0, S.w, lambda x: S.Y(max(top, ps_z_at(S.prof, S.U(x)))), 0.0, S.k, seed=seed, sky=False,
                       birds=False, mix=["plane", "ash", "chaste", "olive", "tamarisk"], style=S.style)
    wl.put(S.pg)


def ps_name(key):
    sp = PLA_SPECIES[key]
    tr = sp.get("turkish")
    return sp["name"] if not tr or tr == "UNVERIFIED" else u"%s (%s)" % (sp["name"], tr)


def ps_plant(S, key, u, z, label=True, **kw):
    """a species at its sourced height (M6) on the ground at (u, z); labelled at its top once per section"""
    S.put(pla_section(key, S.X(u), S.Y(z), S.k, style=S.style, **kw))
    h = pla_height_ok(key, kw.get("h_m") or PLA_SPECIES[key]["h_m"])
    if not kw.get("beyond"):
        S.trees.append((key, S.X(u), h, kw.get("crown_m") or PLA_SPECIES[key]["crown_m"]))
    if label:
        S.lab(ps_name(key), u, z + h)


def ps_land(S, pts, material="earth"):
    """cut ground under a surface [(u, z)] left to right, down to the drawing's bottom"""
    S.put(sct_ground(S.P(pts), 0.0, S.k, material))


def ps_strip(S):
    """the summer strip channel (PS_STRIP) on the axis: its four points"""
    w, dp = PS_STRIP
    b = S.bed
    return [(-w / 2.0, b), (-w / 2.0 + 0.6, b - dp), (w / 2.0 - 0.6, b - dp), (w / 2.0, b)]


def ps_bed(S, uL, uR):
    """the gravel bed from uL to uR with the summer strip, then the M5 water (G8): the average yearly flow over the
    wet bed (never dry), Q100 and Q500 wall to wall, their levels stacked from S.lab_u; stepping stones across the
    strip"""
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
    S.put(sf_stepping_stones(S.X(st[0][0] - 0.2), S.X(st[-1][0] + 0.2), S.Y(st[1][1]), S.Y(level_avg_flow(S.cid)),
                             S.k, seed=len(S.cid)))
    S.lab(u"summer strip · stepping stones", 0.0, b, True)


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


def ps_wet(prof, wl):
    """the stretches of the cut line prof [(u, z)] under the water level wl, each closed along the water line"""
    runs, cur = [], []
    for i, a in enumerate(prof):
        if a[1] < wl:
            if not cur:
                if i > 0:
                    p = prof[i - 1]
                    t = (wl - p[1]) / (a[1] - p[1])
                    cur.append((p[0] + (a[0] - p[0]) * t, wl))
                else:
                    cur.append((a[0], wl))
            cur.append(a)
        elif cur:
            p = prof[i - 1]
            t = (wl - p[1]) / (a[1] - p[1])
            cur.append((p[0] + (a[0] - p[0]) * t, wl))
            runs.append(cur)
            cur = []
    if cur:
        cur.append((cur[-1][0], wl))
        runs.append(cur)
    return runs


def ps_flood_wash(S):
    """the reach of Q500 as a see-through wash behind everything (call first)"""
    for r in ps_wet(S.prof, level(S.cid, "q500")):
        S.pg.poly([S.P(r)], fill=PS_FLOOD, alpha=PS_FLOOD_A)


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
    avg = level_avg_flow(c)
    S.prof = [(S.u0, tN), (-hw, tN), (-hw, b), (hw, b), (hw, tS), (S.u1, tS)]
    ps_back(S, 11)
    ps_flood_wash(S)
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
    ps_lane(S, -hw - 0.6, -hw - 3.6, tN, "walk", u"edge walk · looks down into the bed")
    ps_lane(S, -hw - 4.0, -hw - 6.0, tN, "bike", u"bike lane · street side, clear of the walk")
    ps_lane(S, hw + 0.8, hw + 3.8, tS, "walk")
    ps_bed(S, -hw, hw)
    ps_wall(S, -hw, -1, tN, rail=False)                         # the stair's head opens the NE wall
    ps_wall(S, hw, 1, tS)
    for i, (u0, u1, dp) in enumerate(bas):
        f = tS - dp
        S.put(pla_reed_basin(S.X(u0), S.X(u1), S.Y(f), S.Y(tS), S.k, PS_KERB_H, media_m=0.50,
                             wl_y=S.Y(f + 0.65)))
    S.lab(u"lined reed basins · above Q500", 32.0, tS + 2.9, True)
    S.lab(ps_name("reed"), 25.5, tS + 1.9)
    f_near, f_far = tS - bas[0][2], tS - bas[2][2]
    ps_arrow(S, [(S.u1 - 0.2, tS + 2.6), (41.4, tS + 1.4), (39.5, f_far + 0.85)], COL["river_mid"], 0.3)
    S.lab(u"street and roof runoff in", S.u1 - 0.6, tS + 2.6, True)
    ps_arrow(S, [(bas[0][0] - 0.3, f_near + 0.45), (hw + PS_WALL_T, f_near + 0.45), (hw - 0.1, f_near + 0.45),
                 (hw - 1.4, b + 0.25)], COL["river_dark"], 0.3, dash=[0.8, 0.4])
    S.lab(u"summer release to the strip", hw - 0.7, f_near + 0.6, True)
    # the way down: a stone stair from the NE wall top into the bed (it floods), its rail on the open side
    n = int(math.ceil((tN - b) / PS_STAIR[1]))
    rise, tread = (tN - b) / n, PS_STAIR[0]
    u_bot = -hw + n * tread
    sh, _ = sf_stairs(S.X(u_bot), S.Y(b), n, rise, tread, S.k, side=-1, material="stone", rail=True)
    S.put(sh)
    S.lab(u"stair down into the bed %d × %d cm" % (n, round(rise * 100)), -hw + n * tread * 0.5,
          b + (tN - b) * 0.5 + 1.2, True)
    # planting: shade trees at the street side, a mixed bed edge, shrubs between the SW walk and the basins
    ps_scatter(S, S.u0 + 0.3, -hw - 6.4, lambda u: tN, 0.48, 0.6, {"plane": 1.0, "chaste": 0.8}, 12)
    ps_scatter(S, -4.4, -2.0, lambda u: b, 0.0, 0.16, ["soft_rush", "loosestrife", "rush"], 13, density=0.9)
    ps_scatter(S, hw + 4.2, bas[0][0] - 0.6, lambda u: tS, 0.5, 0.92, ["chaste", "rosemary", "lavender"], 14)
    # people, each where it happens: on the edge walk and bike lane, down the stair, in the bed, along the basins
    ps_people(S, "walkway", -hw - 0.6, -hw - 3.6, lambda u: tN, 15)
    ps_people(S, "bike_lane", -hw - 4.0, -hw - 6.0, lambda u: tN, 16)
    ps_fig(S, "walk", -hw + 0.45 * n * tread, ps_stair_z(u_bot, b, n, rise, tread, -1)(-hw + 0.45 * n * tread),
           facing=1)
    ps_people(S, "bed", u_bot + 0.4, -4.6, lambda u: b, 17, water=avg)
    ps_people(S, "walkway", hw + 0.8, hw + 3.8, lambda u: tS, 18)


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
    S.lab_u = -hw + 0.6                                         # people wade on the SW side of the strip
    avg = level_avg_flow(c)
    ps_back(S, 21)
    ps_flood_wash(S)
    ps_land(S, [(S.u0, tN), (-hw, tN)])
    ps_land(S, [(hw, plat), (u_st, plat)] + steps + [(S.u1, tS)])
    ps_lane(S, -hw - 0.6, -hw - 4.1, tN, "walk", u"edge walk · looks across to the steps")
    ps_lane(S, -hw - 4.5, -hw - 6.5, tN, "bike", u"bike lane · street side, clear of the walk")
    ps_bed(S, -hw, hw)
    ps_wall(S, -hw, -1, tN)
    ps_block_ring(S, hw, u_st, plat - 0.25, plat, "concrete")   # sub-hub floor slab
    for ua, ub, z0, z1 in blocks:                               # steps seated into the cut-back bank
        ps_block_ring(S, ua, ub, z0, z1, "stone")
    ps_block_ring(S, u_sq, S.u1, tS - 0.25, tS, "stone")        # hub square paving
    S.pg.poly([S.P([(hw, b), (hw + PS_WALL_T, b), (hw + PS_WALL_T, tS), (hw, tS)])], stroke=COL["ink2"], lw=0.18,
              dash=[0.8, 0.5])                                  # today's DSİ wall, replaced by the steps
    S.lab(u"today's wall line", hw + PS_WALL_T / 2.0, tS)
    S.lab(u"sub-hub floor %s" % ps_lv(plat), (hw + u_st) / 2.0, plat, True)
    S.lab(u"seating steps %d × %d cm" % (n, round(rise * 100)), u_st + 0.5 * n * tread, plat + 0.5 * n * rise + 0.6,
          True)
    S.lab(u"hub square %s · dry above Q500, plane shade" % ps_lv(tS), u_sq + 3.0, tS + 0.1, True)
    xb = S.X(S.u1)                                              # break line: the land goes on to the cut end
    yb, yt = S.Y(S.z0), S.Y(tS)
    S.pg.line([(xb, yb - 0.6), (xb, yb + 0.35 * (yt - yb)), (xb - 0.7, yb + 0.45 * (yt - yb)),
               (xb + 0.7, yb + 0.6 * (yt - yb)), (xb, yb + 0.7 * (yt - yb)), (xb, yt + 0.8)], COL["ink"], 0.2)
    # planting: the square's planes (Ottoman squares with plane trees, ICOMOS 2014), a mixed tree band behind the NE
    # walk, rushes at the bed's SW edge
    ps_plant(S, "plane", u_sq + 7.0, tS, seed=3)
    ps_plant(S, "plane", u_sq + 19.5, tS, label=False, seed=4)
    ps_scatter(S, S.u0 + 0.3, -hw - 7.0, lambda u: tN, 0.48, 0.88,
               {"plane": 1.0, "ash": 0.5, "chaste": 0.9, "rosemary": 0.7}, 22)
    ps_scatter(S, hw - 2.2, hw - 0.3, lambda u: b, 0.0, 0.14, ["soft_rush", "loosestrife"], 23, density=0.9)
    # people: the NE walk and bike lane, wading in the bed, at the water on the sub-hub floor, sitting on the steps,
    # watching from the top of the steps, walking in the square's shade
    ps_people(S, "walkway", -hw - 0.6, -hw - 4.1, lambda u: tN, 24)
    ps_people(S, "bike_lane", -hw - 4.5, -hw - 6.5, lambda u: tN, 25)
    ps_people(S, "bed", 3.6, hw - 2.4, lambda u: b, 26, water=avg)
    ps_fig(S, "touch", hw + 0.9, plat, facing=-1)
    ps_fig(S, "child_play", hw + 2.6, plat, facing=-1)
    ps_people(S, "sun_steps", u_st + 0.2, u_sq - 0.2, ps_stair_z(u_st, plat, n, rise, tread, 1), 27)
    ps_fig(S, "watch", u_sq + 0.8, tS, facing=-1)
    S.put(fig_group(S.X(u_sq + 3.0), S.Y(tS), S.k, n=3, seed=28, style=S.style))
    ps_people(S, "walkway", u_sq + 9.5, S.u1 - 1.0, lambda u: tS, 29)


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
    avg = level_avg_flow(c)
    S.lab_u = -1.9                                              # level labels over the water, clear of the SW slope
    ps_back(S, 31)
    ps_flood_wash(S)
    # NE: today's loose earth bank (dashed) and the steps seated into it (section_parts earth bank with steps)
    sh, _ = sct_bank("earth", S.X(-hw), S.Y(tN), S.Y(b), -1, k, run_m=run, reach_m=crest - S.u0, depth_m=PS_DEPTH,
                     steps=[(rise, tread)] * n, steps_from_m=0.0, step_material="stone")
    ps_land(S, [(hw, b), (s0, shelf), (s1, shelf), (s1, gf), (S.u1, gf)])   # the garden: fill above the shelf
    S.put(sh)
    old = [(-hw - run * i / 12.0, b + (tN - b) * (3 * (i / 12.0) ** 2 - 2 * (i / 12.0) ** 3)) for i in range(13)]
    S.pg.line(S.P(old), COL["ink2"], 0.18, dash=[0.8, 0.5])
    ps_bed(S, -hw, hw)
    ps_rail(S, crest - 0.2, tN)
    # SW: the stream commons on the shelf (floods in winter), the garden raised above Q500 behind a stone wall
    ps_block_ring(S, s1, s1 + 0.40, shelf - 0.30, gf + 0.15, "stone")
    S.lab(u"steps down the bank %d × %d cm" % (n, round(rise * 100)), -hw - run * 0.45, b + (tN - b) * 0.45 + 2.0,
          True)
    S.lab(u"stream commons %s" % ps_lv(shelf), (s0 + s1) / 2.0, shelf, True)
    S.lab(u"Demeter's Garden %s" % ps_lv(gf), s1 + 1.5, gf + 0.3, True)
    gy = lambda u: shelf + (b - shelf) * max(0.0, min(1.0, (s0 - u) / (s0 - hw)))
    S.lab(u"wet edge · floods at Q100, holds the bank", (hw + s0) / 2.0, gy((hw + s0) / 2.0) + 0.4, True)
    # planting: a mixed wet edge on the slope up to the commons (wet to drier), herbs along the garden wall,
    # tomato rows, olive and chaste tree, the café's plane a step behind the cut
    ps_scatter(S, hw + 2.4, s0 - 0.3, gy, 0.0, 0.42, ["soft_rush", "loosestrife", "rush", "willow", "tamarisk"], 33)
    ps_scatter(S, s1 + 0.6, s1 + 2.4, lambda u: gf, 0.84, 1.0, ["lavender", "rosemary"], 34)
    S.put(pla_crop_rows("tomato", S.X(s1 + 2.6), S.X(s1 + 7.0), S.Y(gf), k, spacing=1.0, h_m=1.0, crown_m=0.8))
    S.lab(u"Tomato (Domates)", s1 + 4.8, gf + 1.0)
    ps_plant(S, "plane", s1 + 14.5, gf, beyond=True, seed=30)  # café shade, a step behind the cut
    ps_plant(S, "olive", s1 + 10.0, gf, seed=31)
    ps_plant(S, "chaste", s1 + 8.0, gf, seed=32)
    S.lab(u"café beds", s1 + 13.0, gf + 2.1, True)
    # people: watching from the crest, sitting and walking on the bank steps, wading in the bed, on the commons,
    # picking tomatoes, at the café under the plane
    ps_fig(S, "watch", crest + 0.5, tN, facing=1)
    ps_people(S, "sun_steps", crest + 1.6, -hw - 0.4, ps_stair_z(-hw, b, n, rise, tread, -1), 35)
    ps_people(S, "bed", -hw + 0.4, -2.6, lambda u: b, 36, water=avg)
    ps_people(S, "walkway", s0 + 1.0, s1 - 1.0, lambda u: shelf, 37)
    ps_fig(S, "touch", s1 + 5.2, gf, facing=-1)                # picking tomatoes
    ps_fig(S, "sit_step", s1 + 13.6, gf, facing=-1)            # café under the plane


# ---------------------------------------------------------------- W4 downstream reach
def ps_sec_w4(S):
    c, b, hw, k = S.cid, S.bed, S.hw, S.k
    tN, aN = level(c, "top", "NE"), level(c, "angle_deg", "NE")
    tS, aS = level(c, "top", "SW"), level(c, "angle_deg", "SW")
    q1, q5 = level(c, "q100"), level(c, "q500")
    avg = level_avg_flow(c)
    gN, gS = math.tan(math.radians(aN)), math.tan(math.radians(aS))
    cN, cS = -hw - (tN - b) / gN, hw + (tS - b) / gS            # crests (u)
    S.prof = [(S.u0, tN), (cN, tN), (-hw, b), (hw, b), (cS, tS), (S.u1, tS)]
    S.lab_u = 1.9
    ps_back(S, 41)
    ps_flood_wash(S)
    zN = lambda u: b + (-hw - u) * gN                           # the NE slope's level at u
    zS = lambda u: b + (u - hw) * gS
    sh, _ = sct_bank("embankment", S.X(-hw), S.Y(tN), S.Y(b), -1, k, angle_deg=aN, reach_m=cN - S.u0,
                     depth_m=PS_DEPTH)
    S.put(sh)
    sh, _ = sct_bank("embankment", S.X(hw), S.Y(tS), S.Y(b), 1, k, angle_deg=aS, reach_m=S.u1 - cS,
                     depth_m=PS_DEPTH)
    S.put(sh)
    # NE crest: the tree corridor, the bike lane, the crest walk (G10)
    ps_lane(S, cN - 0.3, cN - 2.8, tN, "walk", u"crest walk")
    ps_lane(S, cN - 3.2, cN - 5.2, tN, "bike", u"bike lane · along the crest, clear of the walk")
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
    ps_bed(S, -hw, hw)
    ring = [(cN, tN), (uT, tT - 0.20), (uT, zN(uT))]            # the berm under the ramp
    S.put(sct_hatch_fill(S.P(ring), "earth", k, SCT["cut"], 0.25))
    sh, _, _ = sf_ramp(S.X(uT), S.Y(tT), run, tN - tT, k, side=-1, material="concrete", rail=True)
    S.put(sh)
    S.lab(u"ramp · step-free from the crest", (cN + uT) / 2.0, (tN + tT) / 2.0 + PS_RAIL_H, True)
    S.put(sf_terrace(S.X(uT), S.Y(tT), PS_TERRACE_W, k, side=1, material="timber", rail=False))
    u = uT + 0.4
    while u < uW:                                               # the terrace's piles down into the bank
        S.pg.line(S.P([(u, tT - 0.25), (u, zN(u) - 0.6)]), PS_TIMBER, 0.35)
        u += 1.8
    S.lab(u"viewing terrace %s · above Q500" % ps_lv(tT), (uT + uW) / 2.0, tT + 1.8, True)
    sh, _ = sf_stairs(S.X(ub), S.Y(dk), ns, rs, PS_STAIR[0], k, side=-1, material="concrete", rail=True)
    S.put(sh)
    S.pg.poly([S.P([(ua, dk - 0.20), (ua, dk), (ub, dk), (ub, dk - 0.20)])], fill=PS_TIMBER, stroke=SCT["cut"],
              lw=0.25)
    u = ub + 0.3
    while u < ua - 0.3:                                         # piles down into the bank and the bed
        S.pg.line(S.P([(u, dk - 0.20), (u, min(zN(u), b) - 0.6)]), PS_TIMBER, 0.35)
        u += 2.0
    ps_rail(S, ua + 0.1, dk)
    S.lab(u"boardwalk %s · floods at Q100" % ps_lv(dk), (ua + ub) / 2.0, dk + PS_RAIL_H, True)
    # planting: the crest corridor (mixed trees and shrubs), a wet edge under the terrace and boardwalk, the SW slope
    # wet to dry; the field behind the SW crest takes the surplus water
    ps_scatter(S, S.u0 + 0.3, cN - 5.6, lambda u: tN, 0.48, 0.9,
               {"plane": 1.0, "ash": 0.5, "chaste": 1.0, "rosemary": 0.8, "olive": 0.6}, 42)
    S.lab(u"ecological corridor · trees and shrubs along the crest", (S.u0 + cN - 5.6) / 2.0, tN + 0.5, True)
    ps_scatter(S, uT + 0.3, -hw - 0.2, zN, 0.0, 0.16, ["soft_rush", "loosestrife", "rush"], 43)
    ps_scatter(S, hw + 0.3, cS - 0.6, zS, 0.0, 0.5, ["soft_rush", "loosestrife", "willow", "tamarisk", "chaste"], 44)
    S.put(pla_crop_rows("cotton", S.X(cS + 1.0), S.X(S.u1 - 0.4), S.Y(tS), k, spacing=0.9, h_m=1.0, crown_m=0.6))
    S.lab(u"Cotton (Pamuk) · surplus water", (cS + S.u1) / 2.0, tS + 1.0, True)
    # people: cycling and walking on the crest, down the ramp, gathered on the terrace, on the boardwalk, in the bed
    ps_people(S, "walkway", cN - 0.3, cN - 2.8, lambda u: tN, 45)
    ps_people(S, "bike_lane", cN - 3.2, cN - 5.2, lambda u: tN, 46)
    ps_people(S, "walkway", cN + 1.0, uT - 1.0, lambda u: tN - (u - cN) * PS_RAMP, 47)
    ps_fig(S, "sit_step", uT + 0.5, tT, facing=1)
    S.put(fig_group(S.X(uT + 1.9), S.Y(tT), k, n=3, seed=48, style=S.style))
    ps_fig(S, "watch", uW - 0.5, tT, facing=1)
    ps_fig(S, "walk", ub - 0.8, dk, facing=1)
    ps_fig(S, "watch", ua + 0.7, dk, facing=1)
    ps_people(S, "bed", -hw + 0.8, -2.0, lambda u: b, 49, water=avg)
    ps_fig(S, "stand", S.u1 - 1.2, tS, facing=-1)


PS_DRAW = {"W1": ps_sec_w1, "W2": ps_sec_w2, "W3": ps_sec_w3, "W4": ps_sec_w4}


# ---------------------------------------------------------------- labels over the section, data rows under it
def ps_pack(items, xmin, xmax, rows=3, gap=1.2):
    """items [(w, ax)]: each label set over its anchor x (the leader drops straight down), in the lowest row where it
    touches no other label and no leader of a higher row crosses it. Returns [(row, x0) or None]."""
    placed = [[] for _ in range(rows)]
    leaders, out = [], [None] * len(items)
    for i in sorted(range(len(items)), key=lambda j: items[j][1]):
        w, ax = items[i]
        cands = [ax - w * f for f in (0.5, 0.35, 0.65, 0.2, 0.8, 0.05, 0.95)]
        for r in range(rows):
            ok = None
            for x0 in cands:
                x0 = max(xmin, min(xmax - w, x0))
                if not (x0 - 0.05 <= ax <= x0 + w + 0.05):
                    continue
                if any(x0 < b_ + gap and a_ < x0 + w + gap for a_, b_ in placed[r]):
                    continue
                if any(rr > r and x0 - gap < lx < x0 + w + gap for lx, rr in leaders):
                    continue
                if any(a_ - gap < ax < b_ + gap for q in range(r) for a_, b_ in placed[q]):
                    continue
                ok = x0
                break
            if ok is not None:
                placed[r].append((ok, ok + w))
                leaders.append((ax, r))
                out[i] = (r, ok)
                break
    return out


def ps_scale_bar(pg, x, y, k):
    """0-5-10-20 m at k mm per m from (x, y), its numbers over it, the round scale after it: the A0 SHEET's scale
    (PS_SCALE x BK_S, standard), which the booklet re-sets to the scale it prints (1:500, D6)"""
    h, col = 0.9, COL["ink"]
    marks = (0, 5, 10, 20)
    for i, (a, b_) in enumerate(zip(marks[:-1], marks[1:])):
        pg.poly([rect(x + a * k, y, x + b_ * k, y + h)], fill=(col if i % 2 == 0 else COL["white"]), stroke=col,
                lw=0.15)
    for m_ in marks:
        pg.text(str(m_), x + m_ * k, y + h + 0.6, PS_LBL, col, align="C")
    pg.text(u"m · 1:%d" % sf_scale_ok(round(PS_SCALE * BK_S)), x + 20 * k + text_w(u"20", PS_LBL) / 2.0 + 1.2, y + h + 0.6, PS_LBL, col)


def ps_finish(S, log):
    """flood levels, the labels over the drawing, the bank / bed rows under it, the scale bar"""
    pg = S.pg
    for m_ in sf_assert_g6(S.k, trees=S.trees, strict=False):  # G6: people 1.75 m, trees in their sourced range
        log.append(u"G6 CHECK section %s (style %s): %s" % (S.cid, S.style, m_))
    top = ps_bbox(pg.items)[3]
    seen, labs = set(), []
    for t, u, z, prop in S.labels:
        if t not in seen:
            seen.add(t)
            labs.append((t, u, z, prop))
    got = ps_pack([(text_w(t, PS_LBL), S.X(u)) for t, u, z, prop in labs], -4.0, S.w + 4.0)
    base = top + 1.6 + PS_LBL * 0.25
    for (t, u, z, prop), g in zip(labs, got):
        if g is None:
            log.append(u"NOTE section %s: label '%s' left out (no free place over the drawing)" % (S.cid, t))
            continue
        r, x0 = g
        yb = base + r * PS_ROW
        ax, ay = S.X(u), S.Y(z) + 0.5
        if yb - 0.8 > ay + 0.4:
            pg.line([(ax, yb - 0.8), (ax, ay)], COL["ink2"], 0.12)
        pg.text(t, x0, yb, PS_LBL, COL["accent"] if prop else COL["ink"])
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
    ps_scale_bar(pg, 0.0, -1.6 - PS_LBL * CAP - last * PS_ROW - 4.8, S.k)


def ps_section(cid, log, style="b"):
    """one cut as a Page in print mm (see PsSec), in style b (vector) or a (cutouts, D1)"""
    u0, u1, d = ps_extent(cid)
    S = PsSec(cid, u0, u1, d, style)
    PS_DRAW[cid](S)
    ps_finish(S, log)
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
    rows = [("wash", u"reach of the 500-year flood (Q500)"), ("water", u"water at the average yearly flow"),
            ("q100", u"Q100 flood level"), ("q500", u"Q500 flood level"),
            (SCT["stone"], u"stone: DSİ walls, steps, garden wall"), (SCT["concrete"], u"concrete: stairs, ramp, basins"),
            (SCT["earth"], u"earth"), (SCT["gravel"], u"gravel bed"), (PS_TIMBER, u"timber: terrace, boardwalk"),
            (SF_LANE["walk"], u"walk paving"), (SF_LANE["bike"], u"bike lane"),
            ("accent", u"proposal (labels)")]
    sw, gap, x, y = 5.0, 4.0, x0, y1 - PS_ROW
    for kind, lab in rows:
        w = sw + 1.2 + text_w(lab, PS_LBL)
        if x + w > x1 and x > x0:
            x, y = x0, y - PS_ROW
        cy = y + PS_LBL * CAP / 2.0
        if kind in ("q100", "q500"):
            pg.line([(x, cy), (x + sw, cy)], P[kind], 0.3, dash=[1.2, 0.6] if kind == "q100" else [0.4, 0.5])
        else:
            fill = {"wash": PS_FLOOD, "water": P["sec"], "accent": COL["accent"]}.get(kind, kind)
            pg.poly([rect(x, cy - 1.0, x + sw, cy + 1.0)], fill=fill, stroke=COL["faint"], lw=0.1,
                    alpha=(PS_FLOOD_A if kind == "wash" else None))
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
        sec = ps_section(cid, log, style)
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
    log.append(u"sections (v10, revision 30 Oct style %s): W1-W4 at 1:%d on the booklet page, looking downstream"
               % (style, sf_scale_ok(PS_SCALE)))
    return pg, boxes
