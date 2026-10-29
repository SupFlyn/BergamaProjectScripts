# ================================================================ v10 the four proposal sections, true to the cut
# v10 (revision 29 Oct, WO-T3b-3; package C "Page 13", brief 02 §3-§6): the sketches are gone. Each section is drawn
# at 1:500 on the booklet page from the level table (common/levels.py: bed, bed width, bank and wall tops, bank type
# and angle, terraces, Q100, Q500) with the shared section parts (DSİ walls, embankments, loose earth, railings,
# stone / concrete / earth / gravel hatches, steps seated into the bank) and the plants module (every species at its
# true size and form; D6: no fig, citrus, iris, oleander, white poplar; D2: common reed only in lined basins the flood
# passes by). Figures through ONE helper, _p13_fig (figures.py paused: swap the new set in there). All four sections
# look downstream: the NE bank (left bank) on the left, the SW bank on the right, as the key map's triangles show.
# Drawn in booklet print mm (k = PS_K mm per m); build_sheet() places the block on the A0 sheet at 1 / BK_S.
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
PS_FIG = "5E5650"                     # figures
PS_TIMBER = "AA8148"                  # boardwalk timber (icons palette: timber)
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
PS_BREAK = {"W2": ("SW", 50.0)}       # W2's SW land (flat street level to the cut end 80 m out) drawn to 50 m, broken


def ps_lv(z):
    return u"+%.2f" % z


def ps_put(pg, shapes):
    """house shapes ("poly", ring, fill, stroke, lw) / ("line", pts, colour, lw) of the shared modules -> page items"""
    for s in shapes:
        if not s or len(s) < 3 or not s[1]:
            continue
        if s[0] == "poly":
            r = s[1]
            rings = r if isinstance(r[0][0], (list, tuple)) else [r]
            pg.poly(rings, fill=s[2], stroke=s[3] if len(s) > 3 else None, lw=(s[4] if len(s) > 4 and s[4] else 0.1))
        elif s[0] == "line":
            pg.line(s[1], s[2], s[3] if len(s) > 3 and s[3] else 0.1)


class PsSec(object):
    """One section: its own page in print mm, (0, 0) = (left end u0, PS_DEPTH under the bed); u = m across the stream
    from the axis (NE negative), z = m a.s.l."""

    def __init__(self, cid, u0, u1, d):
        self.cid, self.u0, self.u1, self.d = cid, float(u0), float(u1), d
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
            e = max(e, hw + h / math.tan(math.radians(level(cid, "angle_deg", side))) + 3.0)
        elif kind == "loose_earth":
            e = e + 4.0
        ext[side] = e
    br = PS_BREAK.get(cid)
    if br:
        ext[br[0]] = min(ext[br[0]], br[1])
    return -ext["NE"], ext["SW"], d


def _p13_fig(S, pose, u, z, height=1.75, facing=1):
    """page 13's ONE figure helper (figures.py paused: the new silhouette set goes in here): the legacy fig_polys
    at true height for the section's scale, feet at (u, z)"""
    for ring in fig_polys(pose, height, facing):
        S.pg.poly([[(S.X(u + px), S.Y(z + py)) for px, py in ring]], fill=PS_FIG)


def ps_name(key):
    sp = PLA_SPECIES[key]
    tr = sp.get("turkish")
    return sp["name"] if not tr or tr == "UNVERIFIED" else u"%s (%s)" % (sp["name"], tr)


def ps_plant(S, key, u, z, label=True, **kw):
    """a species at true size on the ground at (u, z); labelled at its top once per section"""
    S.put(pla_section(key, S.X(u), S.Y(z), S.k, **kw))
    if label:
        S.lab(ps_name(key), u, z + (kw.get("h_m") or PLA_SPECIES[key]["h_m"]))


def ps_land(S, pts, material="earth"):
    """cut ground under a surface [(u, z)] left to right, down to the drawing's bottom"""
    S.put(sct_ground(S.P(pts), 0.0, S.k, material))


def ps_bed(S, uL, uR):
    """the gravel bed from uL to uR with the summer strip channel (PS_STRIP) on the axis, water in it"""
    w, dp = PS_STRIP
    b = S.bed
    pts = [(uL, b), (-w / 2.0, b), (-w / 2.0 + 0.6, b - dp), (w / 2.0 - 0.6, b - dp), (w / 2.0, b), (uR, b)]
    S.put(sct_ground(S.P(pts), 0.0, S.k, "gravel"))
    S.put(sec_water(S.P(pts[1:5])))
    S.lab(u"summer strip", 0.0, b, True)


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


def ps_flood_lines(S):
    """Q500 dashed and Q100 dotted across every wet stretch; one label over the widest, at its left end"""
    q1, q5 = level(S.cid, "q100"), level(S.cid, "q500")
    for wl, dash in ((q5, [1.2, 0.6]), (q1, [0.3, 0.45])):
        for r in ps_wet(S.prof, wl):
            S.pg.line([(S.X(r[0][0]), S.Y(wl)), (S.X(r[-1][0]), S.Y(wl))], COL["river_mid"], 0.22, dash=dash)
    runs = [r_ for r_ in ps_wet(S.prof, q5) if r_[0][0] <= -S.hw + 0.01 <= r_[-1][0]]
    if runs:                                                    # in the channel, from its NE side: Q500 over its
        x = S.X(max(runs[0][0][0], -S.hw)) + 0.8                # line, Q100 under its own (clear of the strip)
        S.pg.text(u"Q500 %s" % ps_lv(q5), x, S.Y(q5) + 0.6, PS_LBL, COL["river_dark"])
        S.pg.text(u"Q100 %s" % ps_lv(q1), x, S.Y(q1) - 0.6 - PS_LBL * CAP, PS_LBL, COL["river_dark"])


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
    ps_bed(S, -hw, hw)
    ps_wall(S, -hw, -1, tN)
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
    # planting and people, each where it happens
    ps_plant(S, "plane", -21.5, tN, seed=1)
    ps_plant(S, "chaste", 20.2, tS, seed=2)
    for i, u in enumerate((-4.6, -3.7, 3.6, 4.5)):
        ps_plant(S, "soft_rush", u, b, label=(i == 0), seed=i)
    _p13_fig(S, "watch", -hw - 1.3, tN, facing=1)               # at the railing, looking into the channel
    _p13_fig(S, "walk", 18.6, tS, facing=1)                     # along the basins
    _p13_fig(S, "wade", 0.5, b - PS_STRIP[1], facing=-1)        # in the summer strip


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
    ps_flood_wash(S)
    ps_land(S, [(S.u0, tN), (-hw, tN)])
    ps_land(S, [(hw, plat), (u_st, plat)] + steps + [(S.u1, tS)])
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
    S.lab(u"hub square %s" % ps_lv(tS), u_sq + 3.0, tS + 0.1, True)
    xb = S.X(S.u1)                                              # break line: the land goes on to the cut end
    yb, yt = S.Y(S.z0), S.Y(tS)
    S.pg.line([(xb, yb - 0.6), (xb, yb + 0.35 * (yt - yb)), (xb - 0.7, yb + 0.45 * (yt - yb)),
               (xb + 0.7, yb + 0.6 * (yt - yb)), (xb, yb + 0.7 * (yt - yb)), (xb, yt + 0.8)], COL["ink"], 0.2)
    ps_plant(S, "plane", u_sq + 7.0, tS, seed=3)
    ps_plant(S, "plane", u_sq + 21.0, tS, label=False, seed=4)
    for i, u in enumerate((hw + 0.4, hw + 1.0)):
        ps_plant(S, "soft_rush", u, plat, label=(i == 0), seed=5 + i)
    _p13_fig(S, "watch", -hw - 1.3, tN, facing=1)
    _p13_fig(S, "bike", -22.0, tN, facing=1)
    _p13_fig(S, "touch", hw + 1.8, plat, facing=-1)            # at the strip's edge
    for i in (3, 7):                                           # sitting on the steps, facing the stream
        ua, ub, _, z1 = blocks[i]
        _p13_fig(S, "sit", (ua + ub) / 2.0, z1, facing=-1)
    _p13_fig(S, "stand", u_sq + 1.0, tS, facing=-1)            # at the top of the steps, the viewing edge
    _p13_fig(S, "walk", u_sq + 15.0, tS, facing=1)
    _p13_fig(S, "sit", u_sq + 9.0, tS, facing=1)               # in the plane's shade


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
    for i, u in enumerate((s0 - 3.2, s0 - 2.4, s0 - 1.6, s0 - 0.8)):
        ps_plant(S, "loosestrife" if i % 2 else "soft_rush", u, gy(u), label=(i < 2), seed=10 + i)
    for i in range(3):
        u = s1 + 0.9 + i * 0.6
        ps_plant(S, "lavender", u, gf, label=(i == 0), seed=20 + i)
    S.put(pla_crop_rows("tomato", S.X(s1 + 2.6), S.X(s1 + 7.0), S.Y(gf), k, spacing=1.0, h_m=1.0, crown_m=0.8))
    S.lab(u"Tomato (Domates)", s1 + 4.8, gf + 1.0)
    ps_plant(S, "plane", s1 + 14.5, gf, beyond=True, seed=30)  # café shade, a step behind the cut
    ps_plant(S, "olive", s1 + 10.0, gf, seed=31)
    ps_plant(S, "chaste", s1 + 8.0, gf, seed=32)
    S.lab(u"café beds", s1 + 13.0, gf + 2.1, True)
    _p13_fig(S, "watch", crest - 1.2, tN, facing=1)
    i = n // 2
    _p13_fig(S, "walk", -hw - tread * (i + 0.5), b + rise * (i + 1), facing=1)
    _p13_fig(S, "wade", -0.4, b - PS_STRIP[1], height=1.15, facing=1)
    _p13_fig(S, "sit", s0 + 5.0, shelf, facing=-1)
    _p13_fig(S, "walk", s0 + 10.5, shelf, facing=1)
    _p13_fig(S, "touch", s1 + 5.2, gf, facing=-1)             # picking tomatoes
    _p13_fig(S, "sit", s1 + 13.6, gf, facing=-1)              # café under the plane


# ---------------------------------------------------------------- W4 downstream reach
def ps_sec_w4(S):
    c, b, hw, k = S.cid, S.bed, S.hw, S.k
    tN, aN = level(c, "top", "NE"), level(c, "angle_deg", "NE")
    tS, aS = level(c, "top", "SW"), level(c, "angle_deg", "SW")
    q1, q5 = level(c, "q100"), level(c, "q500")
    gN, gS = math.tan(math.radians(aN)), math.tan(math.radians(aS))
    cN, cS = -hw - (tN - b) / gN, hw + (tS - b) / gS            # crests (u)
    S.prof = [(S.u0, tN), (cN, tN), (-hw, b), (hw, b), (cS, tS), (S.u1, tS)]
    ps_flood_wash(S)
    zN = lambda u: b + (-hw - u) * gN                           # the NE slope's level at u
    sh, _ = sct_bank("embankment", S.X(-hw), S.Y(tN), S.Y(b), -1, k, angle_deg=aN, reach_m=cN - S.u0,
                     depth_m=PS_DEPTH)
    S.put(sh)
    sh, _ = sct_bank("embankment", S.X(hw), S.Y(tS), S.Y(b), 1, k, angle_deg=aS, reach_m=S.u1 - cS,
                     depth_m=PS_DEPTH)
    S.put(sh)
    ps_bed(S, -hw, hw)
    # NE: planting in bands by flood level: wet edge under Q100, the boardwalk in the Q100 band, trees above Q500
    dk = round((q1 - 0.40) * 20.0) / 20.0                       # boardwalk deck: floods at Q100 (design rule)
    ub = -hw - (dk - b) / gN                                    # where the deck meets the slope
    ua = ub + 6.0
    S.pg.poly([S.P([(ua, dk - 0.20), (ua, dk), (ub, dk), (ub, dk - 0.20)])], fill=PS_TIMBER, stroke=SCT["cut"],
              lw=0.25)
    u = ua - 0.3
    while u > ub + 0.5:                                         # piles down into the bank
        S.pg.line(S.P([(u, dk - 0.20), (u, zN(u) - 0.6)]), PS_TIMBER, 0.35)
        u -= 2.0
    ps_rail(S, ua - 0.1, dk)
    S.lab(u"boardwalk %s" % ps_lv(dk), (ua + ub) / 2.0, dk + PS_RAIL_H, True)
    u_q1 = -hw - (q1 - b) / gN
    for i, u in enumerate([-hw - 0.6 - 0.9 * j for j in range(5)]):
        ps_plant(S, "soft_rush" if i % 2 else "loosestrife", u, zN(u), label=(i < 2), seed=40 + i)
    S.lab(u"floodable planting", (-hw + u_q1) / 2.0 - 1.0, zN(-hw - 2.0) + 1.6, True)
    u_q5 = -hw - (q5 - b) / gN
    ps_plant(S, "tamarisk", (u_q5 + ub) / 2.0, zN((u_q5 + ub) / 2.0), seed=46)
    ps_plant(S, "ash", u_q5 - 4.0, zN(u_q5 - 4.0), seed=47)
    ps_plant(S, "plane", cN + 1.5, zN(cN + 1.5), seed=48)
    # SW: grass slope, rush at the toe, the field behind the crest takes the surplus water
    for i, u in enumerate((hw + 0.6, hw + 1.5)):
        ps_plant(S, "soft_rush", u, b + (u - hw) * gS, label=False, seed=50 + i)
    S.put(pla_crop_rows("cotton", S.X(cS + 1.0), S.X(S.u1 - 0.4), S.Y(tS), k, spacing=0.9, h_m=1.0, crown_m=0.6))
    S.lab(u"Cotton (Pamuk) · surplus water", (cS + S.u1) / 2.0, tS + 1.0, True)
    _p13_fig(S, "bike", S.u0 + 1.4, tN, facing=1)
    _p13_fig(S, "walk", (ua + ub) / 2.0 + 1.0, dk, facing=1)
    _p13_fig(S, "wade", 0.3, b - PS_STRIP[1], height=1.15, facing=-1)
    _p13_fig(S, "stand", S.u1 - 1.2, tS, facing=-1)


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
    """0-5-10-20 m at k mm per m from (x, y), its numbers over it, the round scale after it"""
    h, col = 0.9, COL["ink"]
    marks = (0, 5, 10, 20)
    for i, (a, b_) in enumerate(zip(marks[:-1], marks[1:])):
        pg.poly([rect(x + a * k, y, x + b_ * k, y + h)], fill=(col if i % 2 == 0 else COL["white"]), stroke=col,
                lw=0.15)
    for m_ in marks:
        pg.text(str(m_), x + m_ * k, y + h + 0.6, PS_LBL, col, align="C")
    pg.text(u"m · 1:%d" % PS_SCALE, x + 20 * k + text_w(u"20", PS_LBL) / 2.0 + 1.2, y + h + 0.6, PS_LBL, col)


def ps_finish(S, log):
    """flood levels, the labels over the drawing, the bank / bed rows under it, the scale bar"""
    pg = S.pg
    ps_flood_lines(S)
    top = items_bbox(pg.items)[3]
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


def ps_section(cid, log):
    """one cut as a Page in print mm (see PsSec)"""
    u0, u1, d = ps_extent(cid)
    S = PsSec(cid, u0, u1, d)
    PS_DRAW[cid](S)
    ps_finish(S, log)
    return S.pg


# ---------------------------------------------------------------- the page block: key map strip + 2 x 2 sections
PS_GAP = 4.0                           # print mm between the panels


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


def ps_block(log):
    """page 13: the key map strip across the top (it serves all four sections), the four sections under it in
    reading order, all at 1:500, in print mm (0, 0)-(BK_W, BK_H). Returns (Page, {sheet key: panel box})."""
    pg = Page(BK_W, BK_H)
    yk = BK_H - PS_KEY_H
    ps_key_strip(pg, (0.0, yk, BK_W, BK_H), log)
    cw = (BK_W - PS_GAP) / 2.0
    ch = (yk - 2.0 * PS_GAP) / 2.0
    boxes = {}
    for i, (key, cid, n, name, take) in enumerate(PS_CUTS):
        x0 = (i % 2) * (cw + PS_GAP)
        y1 = yk - PS_GAP - (i // 2) * (ch + PS_GAP)
        box = (x0, y1 - ch, x0 + cw, y1)
        boxes[key] = box
        inner = ps_cell(pg, box, n, cid, name, take, ps_note(cid))
        sec = ps_section(cid, log)
        b = items_bbox(sec.items)
        if b[2] - b[0] > inner[2] - inner[0] + 0.01 or b[3] - b[1] > inner[3] - inner[1] + 0.01:
            log.append(u"NOTE section %s: %.0f x %.0f mm at 1:%d, room %.0f x %.0f mm (kept to scale)" % (
                cid, b[2] - b[0], b[3] - b[1], PS_SCALE, inner[2] - inner[0], inner[3] - inner[1]))
        dx = (inner[0] + inner[2]) / 2.0 - (b[0] + b[2]) / 2.0
        dy = inner[1] - b[1]
        pg.items += xform(sec.items, 1.0, dx, dy)
    log.append(u"sections (v10): W1-W4 at 1:%d on the booklet page, looking downstream" % PS_SCALE)
    return pg, boxes
