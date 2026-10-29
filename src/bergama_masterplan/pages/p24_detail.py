# p.24 the detail window panel: v28 (revision 29 Oct, WO-T4b-3) plan language + sections D1, D2 (split from parts/02_Design.py, parts/02b_detail.py, parts/02e_r28_detail.py, parts/03_make_board.py on 29 Oct 2026; moved unchanged)


# ================================================================ links between shapes (v2.3)
def link_shapes(L, shapes, near=30.0):
    """The shape (zone or strip) a link starts in and the one it ends in (holding the end, else nearest)."""
    def at(e, skip=None):
        for z in shapes:
            if z is not skip and pip(e[0], e[1], z["P"]):
                return z
        best, bd = None, near
        for z in shapes:
            if z is skip:
                continue
            d = min(seg_dist(e[0], e[1], a, b) for a, b in zip(thin(z["P"]), thin(z["P"])[1:] + thin(z["P"])[:1]))
            if d < bd:
                best, bd = z, d
        return best
    a = at(L["P"][0])
    return a, at(L["P"][-1], skip=a)


def inside_spots(TP, n=16):
    bx = bbox(TP)
    pole = inner_pt(TP)
    S = []
    for i in range(n):
        for j in range(n):
            x = bx[0] + (i + 0.5) / n * (bx[2] - bx[0])
            y = bx[1] + (j + 0.5) / n * (bx[3] - bx[1])
            if pip(x, y, TP):
                S.append((x, y))
    S.sort(key=lambda p: (p[0] - pole[0]) ** 2 + (p[1] - pole[1]) ** 2)
    return [pole] + S


def clip_ring(R, cb):
    """A ring cut to the rectangle cb = (x0, y0, x1, y1) (Sutherland-Hodgman on the four sides)."""
    P = list(R)
    for ax, lim, keep_lo in ((0, cb[0], False), (0, cb[2], True), (1, cb[1], False), (1, cb[3], True)):
        if not P:
            break
        out = []
        for i in range(len(P)):
            a, b = P[i - 1], P[i]
            ia = a[ax] <= lim if keep_lo else a[ax] >= lim
            ib = b[ax] <= lim if keep_lo else b[ax] >= lim
            if ib != ia:
                t = (lim - a[ax]) / ((b[ax] - a[ax]) or 1e-12)
                out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
            if ib:
                out.append(b)
        P = out
    return P


def north_arrow(pg, x, y, h=7.0):
    """v21: north arrow (survey grid +Y) with its tip at (x, y), page mm; 'N' beside it."""
    pg.poly([[(x, y), (x - 1.8, y - h), (x, y - h * 0.72)]], fill=COL["ink_dark"])
    pg.poly([[(x, y), (x, y - h * 0.72), (x + 1.8, y - h)]], fill=COL["white"], stroke=COL["ink_dark"], lw=0.15)
    pg.text(u"N", x + 2.6, y - 3.2, 2.6, COL["ink_dark"], bold=True)


def panel_marks(sh, x, y, scale, marks):
    """v21: north arrow and scale bar in a panel's bottom margin (x, y = its left end, page mm)."""
    north_arrow(sh, x + 2.0, y + 8.0)
    scale_bar(sh, x + 12.0, y + 1.0, scale, marks)


def store_m3(z):
    """(rough volume m3, words) of a water-route zone, or None: reed basins area x 0.46 m; retention terraces area x
    the Q100 depth over them at the nearest channel cut."""
    if z["code"] in STORE_DEPTH:
        return z["m2"] * STORE_DEPTH[z["code"]], u""
    if z["code"] == "WS" and z.get("P"):
        cx = sum(p[0] for p in z["P"]) / len(z["P"])
        cy = sum(p[1] for p in z["P"]) / len(z["P"])
        num, nm, c, span, bed, q100, q500 = min(CUT_AT, key=lambda r: (r[2][0] - cx) ** 2 + (r[2][1] - cy) ** 2)
        return z["m2"] * max(0.0, q100[0] - (bed + TERRACE_UP)), u" in Q100"
    return None


def _r28_base(pg, C, T, R, segs):
    """v27 (P24.1, P24.2): the survey as a faint grey underlay: the bed, contours, stream lines, buildings (heritage
    with a thin outline), street edges; the bridges crisp (the base's only dark lines, kept free of words)."""
    cl = _r28_base_cols()
    Rm = (R[0] - 5.0, R[1] - 5.0, R[2] + 5.0, R[3] + 5.0)
    near = lambda Ls: [[T(p) for p in L_] for L_ in Ls if len(L_) >= 2 and hit(bbox(L_), Rm)]
    Ps = near(C.bed_loops)
    if Ps:
        pg.poly(Ps, fill=cl["bed"])
        leg(("r28dt", "bed"))
    for Q in near(C.contours):
        pg.line(Q, COL["contour10"], 0.12)
        leg(("r28dt", "contour"))
    for Q in near(C.streams):
        pg.line(Q, COL["river_mid"], 0.12, alpha=0.5)
    for role in ("building", "housing", "shed"):
        Ps = near(C.bld.get(role, []))
        if Ps:
            pg.poly(Ps, fill=cl["bld"])
            leg(("r28dt", "bld"))
    Ps = near(C.bld.get("heritage", []))
    if Ps:
        pg.poly(Ps, fill=cl["bld"], stroke=COL["her_edge"], lw=0.15)
        leg(("r28dt", "her"))
    Ps = near(C.built_since)
    if Ps:
        pg.poly(Ps, fill=cl["bld"], stripes=(COL["ink2"], 0.8, 0.12, 45.0))
        leg(("r28dt", "since"))
    for Q in near(C.roads):
        pg.line(Q, COL["ink2"], 0.15, alpha=0.4)
        leg(("r28dt", "street"))
    for Q in near(C.bridges):
        pg.line(Q, COL["ink"], 0.4)
        segs += list(zip(Q, Q[1:]))
        leg(("r28dt", "bridge"))


def _r28_wh(lines):
    """lines [(text, size, bold, colour)] -> (w, h), mm"""
    return max(text_w(s, sz, bd) for s, sz, bd, _ in lines), sum(sz * 1.18 for s, sz, bd, _ in lines)


def _r28_text(pg, lines, b, centre=False):
    y = b[3]
    for s, sz, bd, col in lines:
        y -= sz
        if centre:
            pg.text(s, (b[0] + b[2]) / 2.0, y, sz, col, bold=bd, align="C")
        else:
            pg.text(s, b[0], y, sz, col, bold=bd)
        y -= sz * 0.18


def _r28_free(b, taken, segs, bounds, pad):
    if not (bounds[0] <= b[0] and b[2] <= bounds[2] and bounds[1] <= b[1] and b[3] <= bounds[3]):
        return False
    return not any(lp_hit(b, t, pad) for t in taken) and not any(_lp_seg_box(p, q, b) for p, q in segs)


def _r28_spot(w, h, anchor, taken, segs, bounds, rank=0):
    """G4 (common/label_place): a free w x h box by anchor, (box, leader) or None; rank 0 always finds one."""
    got = place_labels_all([{"x": anchor[0], "y": anchor[1], "wh": lambda f: (w, h), "rank": rank}], taken, bounds,
                           segs, sizes=(1.0,), pad=0.5)
    return got[0][:2] if 0 in got else None


def _r28_label(pg, lines, anchor, taken, segs, bounds, rank=0, leader=True):
    """A word block beside its anchor, on a thin leader when it had to move off; its box or None (dropped)."""
    w, h = _r28_wh(lines)
    got = _r28_spot(w, h, anchor, taken, segs, bounds, rank)
    if got is None:
        return None
    b, far = got
    _r28_text(pg, lines, b)
    if far and leader:
        pg.line([anchor, lp_leader_end(b, anchor)], COL["ink2"], 0.15)
    return b


def _r28_title(pg, ring_, variants, taken, segs, bounds):
    """v27 (P24.1, P24.2): a field's title block, centred on the first free spot inside the field (its pole first),
    else beside the pole on a leader; the variants are tried in order (with the grey line, then without)."""
    spots = inside_spots(ring_, 12)
    for lines in variants:
        w, h = _r28_wh(lines)
        for x, y in spots:
            b = (x - w / 2.0, y - h / 2.0, x + w / 2.0, y + h / 2.0)
            if _r28_free(b, taken, segs, bounds, 0.6):
                _r28_text(pg, lines, b, True)
                taken.append(b)
                return b
    for lines in variants:
        b = _r28_label(pg, lines, spots[0], taken, segs, bounds, rank=0 if lines is variants[-1] else 1)
        if b:
            return b
    return None


def _r28_route_runs(order, L, a, b):
    """v27 (P24.2, G5): one water route step as text runs [(text, bold)]: the move, the zone in bold, its area and
    rough volume (v22-v26's figures and wording, sentence case)."""
    if order < len(ROUTE):
        words, end = ROUTE[order][1].capitalize(), ROUTE[order][2]   # "Into {}", "Back to the stream"
        z = (a, b)[end] if end is not None else None
        if z is None:
            w0, _, rest = words.partition(u" ")
            return [(w0, True), (u" " + rest, False)]
        nm = name_of(z, z.get("own", ""))
        nm = ROUTE_SHORT.get(nm, nm).lower()
        pre, _, post = words.partition(u"{}")
        runs = [(pre + u"the ", False), (nm, True)] + ([(post, False)] if post else [])
        runs.append((u" · " + u_area(z["m2"]), False))
        sv = store_m3(z)                                 # v22: rough volume, area x depth
        if sv:
            runs.append((u" · ~" + u_volume(round(sv[0], -1)) + sv[1], False))
            leg(("dt", "vol"))
        return runs
    t_ = (L["label"] or u"water").lower().replace(u"river", u"stream").capitalize()
    head, _, last = t_.rpartition(u" ")
    return [(head + u" ", False), (last, True)] if head else [(t_, True)]


# ================================================================ v28 (revision 29 Oct, WO-T4b-3): plan language and sections
# Package H "Page 24". The plan: an architectural plan language (R15 idea, not its style), every element with its own
# symbol and texture, at true size from the masterplan's own design: lined reed cells (plants module), terrace edges
# with ticks, Demeter's Garden as an olive orchard at its sourced 7 x 5 m spacing, paved hub squares with their
# planes, forest crowns at their true crown width, the riverside walk with its bike lane, stepping stones, footbridge
# decks, the changed roads by their change, the wetland of the widened stream; no round vignettes. Under each plan its
# section at the same 1:1,000: D1 on the W1 line, D2 on the W3 line (the cut lines may repeat, D11; p.13 draws them
# at 1:500 within the banks looking downstream, these run across the whole window looking upstream, with the zones
# from the water to the edge). The section's channel comes from the level table (common/levels.py: bed, bed width,
# wall and bank tops, Q100, Q500), the land beyond the banks from the survey's heights (spot heights near the line,
# the contours it crosses); along it every proposal the plan draws where the cut crosses it, paler where it stands
# beyond the cut in the view direction; a vertical line names each zone (R18 idea); banks, materials, roots and
# people from section_parts, plants and figures (R16, R17 idea).
P24_CUTS = {"dt_upstream": ("W1", u"D1"), "dt_k5": ("W3", u"D2")}
P24_HALF_M = 97.0            # the section reaches this far either side of the stream axis, m (half the window width)
P24_WALL_T = 0.60            # DSİ wall thickness, m: no sourced value; the 0.60 m of p.04-05 and p.13 (G2)
P24_RAIL_H = 1.10            # railing on a wall top, m: drawing value (as p.13)
P24_KERB_H = 0.15            # reed cell kerb above the ground, m: drawing value (as p.13)
P24_BASIN = (5.0, 1.5, 0.90, 0.50, 0.65)   # reed cell: length, gap, floor under the rim, media, water over the floor,
#                              m: drawing values (p.13's middle basin)
P24_FREEBOARD = 0.30         # a dry proposed floor sits this far above Q500, rounded up to 5 cm (p.13's rule)
P24_WALL_DG = 0.40           # Demeter's Garden's stone edge wall, m thick (as p.13)
P24_PAVE_T = 0.25            # paving of hub squares and streets in section, m (drawing value, as p.13)
P24_SPOT_M = 5.0             # survey spot heights this far from the cut line make its ground, m
P24_BEYOND_M = 150.0         # proposals this far beyond the cut, in the view direction, show paler in the section, m
P24_BELOW_M = 3.0            # cut ground drawn this far under the lowest point, m
P24_STEP_M = 0.5             # the section's sampling step, m
P24_MIN_RUN = 4.0            # zone runs shorter than this get no zone line, m
P24_TREE_M = 6.0             # forest and street trees this far from the cut line stand in the section, m
P24_BIKE = True              # the riverside walk carries a bike lane (Aras 29 Oct 21:04, decision card)
P24_BIKE_W = 2.0             # bike lane beside the walk in plan, m: drawing value
P24_STONE = (0.40, 1.20)     # stepping stone radius and spacing, m: drawing values
P24_LAB_ROWS = 4             # rows of zone names above a section
P24_SEC_MAX = 222.0          # mm: a crop (plan + section) taller than this does not fit the booklet page with its legend
P24_FLOOD, P24_FLOOD_A = "C1D3DB", 0.55   # the reach of Q500 in section (as p.13)
P24_BIKE_COL = "A9673F"      # the bike lane (palette centre family, darker)
P24_KEY = {("WT", None): "reed", ("WD", None): "spill", ("WS", None): "terraces", ("DG", None): "demeter",
           ("GR", None): "forest", ("WA", "F"): "wetland", ("WP", None): "wetland", ("WA", "W"): "subhub"}
P24_NAME = {"reed": u"REED BASINS, LINED", "spill": u"SPILLWAY", "terraces": u"RAIN TERRACES",
            "demeter": u"DEMETER'S GARDEN", "forest": u"FOREST CORRIDOR", "trees": u"TREE-PLANTED AREA",
            "wetland": u"WIDENED STREAM · WETLAND", "subhub": u"SUB-HUB IN THE BED", "hub": u"HUB SQUARE",
            "walk": u"WALK + BIKE LANE" if P24_BIKE else u"RIVERSIDE WALK", "street": u"STREET", "bld": u"BUILDING",
            "bed": u"SELINOS", "foot": u"FOOTBRIDGE", "stones": u"STEPPING STONES", "view": u"VIEWING TERRACE"}
# species named under a plan field's title (plants module names, "English (Turkish)"; D2: reed only in lined cells,
# D6: no iris, oleander, white poplar; water mint left out of the open ground)
P24_SPECIES = {"reed": ("reed",), "terraces": ("lavender",), "hub": ("plane",), "demeter": ("olive", "lavender"),
               "wetland": ("willow", "tamarisk", "loosestrife"), "forest": ("ash", "plane")}


def _p24_put(pg, shapes, alpha=None):
    """house shapes ("poly", ring(s), fill, stroke, lw) / ("line", pts, colour, lw) of the shared modules -> pg"""
    for s in shapes:
        if not s or len(s) < 3 or not s[1]:
            continue
        if s[0] == "poly":
            r = s[1]
            rings = r if isinstance(r[0][0], (list, tuple)) else [r]
            pg.poly(rings, fill=s[2], stroke=s[3] if len(s) > 3 else None,
                    lw=(s[4] if len(s) > 4 and s[4] else 0.1), alpha=alpha)
        elif s[0] == "line":
            pg.line(s[1], s[2], s[3] if len(s) > 3 and s[3] else 0.1, alpha=alpha)


def _p24_top(shapes):
    """the highest page y of house shapes (or None)"""
    ys = []
    for s in shapes:
        if s and len(s) >= 2 and s[1]:
            r = s[1]
            rings = r if isinstance(r[0][0], (list, tuple)) else [r]
            ys += [p[1] for R in rings for p in R]
    return max(ys) if ys else None


def _p24_sp(key):
    """a species' printed name, 'English (Turkish)', English alone where the Turkish name is unverified"""
    sp = PLA_SPECIES[key]
    tr = sp.get("turkish") or u""
    return sp["name"] if (not tr or u"UNVERIFIED" in tr) else u"{} ({})".format(sp["name"], tr)


def _p24_cross(c0, cd, p, q):
    """t (m along c0 + t * cd) where segment p-q crosses that line, or None"""
    sx, sy = q[0] - p[0], q[1] - p[1]
    den = cd[0] * sy - cd[1] * sx
    if abs(den) < 1e-12:
        return None
    wx, wy = p[0] - c0[0], p[1] - c0[1]
    s = (wx * cd[1] - wy * cd[0]) / den
    return (wx * sy - wy * sx) / den if -1e-9 <= s <= 1.0 + 1e-9 else None


def _p24_crossings(c0, cd, P, ta, tb):
    """every t in ta..tb where polyline P crosses the cut line"""
    out = []
    for p, q in zip(P, P[1:]):
        t = _p24_cross(c0, cd, p, q)
        if t is not None and ta <= t <= tb:
            out.append(t)
    return out


def _p24_tz(c0, cd, f, p):
    """(t along the cut, depth in the view direction f) of a survey point"""
    dx, dy = p[0] - c0[0], p[1] - c0[1]
    return dx * cd[0] + dy * cd[1], dx * f[0] + dy * f[1]


def _p24_zat(prof, t):
    """the profile's height at t (on a vertical step: the value of the first segment that holds t)"""
    if t <= prof[0][0]:
        return prof[0][1]
    for (t0, z0), (t1, z1) in zip(prof, prof[1:]):
        if t1 > t0 and t0 <= t <= t1:
            return z0 + (z1 - z0) * (t - t0) / (t1 - t0)
    return prof[-1][1]


def p24_ground(C, c0, cd, ta, tb):
    """[(t, z)] survey heights along the cut c0 + t * cd: spot heights (NOKTA_TAKEOMETRI) within P24_SPOT_M of the
    line, and the survey contours it crosses at their own height (the shared basemap's contours when the survey's
    lie flat); points closer than 1 m along the cut are averaged."""
    nx_, ny_ = -cd[1], cd[0]
    pts = []
    for x, y, z in C.spots:
        dx, dy = x - c0[0], y - c0[1]
        t = dx * cd[0] + dy * cd[1]
        if ta - 5.0 <= t <= tb + 5.0 and abs(dx * nx_ + dy * ny_) <= P24_SPOT_M:
            pts.append((t, z))
    cz = [(P, z) for P, z in getattr(C, "contour_z", []) if abs(z) > 1.0]
    if not cz:
        cz = [(P, z) for major, z, P in ((basemap_load() or {}).get("contours") or []) if z is not None]
    for P, z in cz:
        pts += [(t, z) for t in _p24_crossings(c0, cd, P, ta - 5.0, tb + 5.0)]
    pts.sort()
    out = []
    for t, z in pts:
        if out and t - out[-1][2] < 1.0:
            g = out[-1]
            g[0].append(t)
            g[1].append(z)
        else:
            out.append([[t], [z], t])
    return [(sum(a) / len(a), sum(b) / len(b)) for a, b, _ in out]


def p24_profile(C, cid, c0, cd, ta, tb, warn):
    """the cut line's ground today, left (SW, t < 0) to right (NE), as [[t, z]]: the bed at its level and width;
    DSİ walls at the level table's top with the land behind them at the wall top for 2 m; the other banks and all land
    beyond from the survey heights (p24_ground); flat at the bank top where the survey has none (logged)."""
    bed, hw = level(cid, "bed"), level(cid, "bed_width_cm") / 200.0
    sv = p24_ground(C, c0, cd, ta, tb)
    land, kinds, tops = {}, {}, {}
    for side, sg in (("SW", -1.0), ("NE", 1.0)):
        kinds[side] = (level_cut(cid).get(side) or {}).get("type")
        tops[side] = level(cid, "top", side)
        if kinds[side] == "dsi_wall":
            e = hw + P24_WALL_T + 2.0
            pts = [(sg * e, tops[side])] + [(t, z) for t, z in sv if sg * t > e]
        else:
            pts = [(sg * hw, bed)] + [(t, z) for t, z in sv if sg * t > hw + 1.0]
        if len(pts) == 1:
            pts.append((sg * (hw + 4.0), tops[side] if tops[side] is not None else bed))
            warn.append(u"section {}: no survey heights on the {} side: its land is drawn flat".format(cid, side))
        land[side] = sorted(pts)
    n = int((tb - ta) / P24_STEP_M)
    ts = [ta + i * P24_STEP_M for i in range(n + 1)] + [tb]
    prof = [[t, _p24_zat(land["SW"], t) if kinds["SW"] != "dsi_wall" or t < -(hw + P24_WALL_T + 2.0)
             else tops["SW"]] for t in ts if t < -hw]
    prof += [[-hw, tops["SW"]], [-hw, bed]] if kinds["SW"] == "dsi_wall" else [[-hw, bed]]
    prof += [[hw, bed], [hw, tops["NE"]]] if kinds["NE"] == "dsi_wall" else [[hw, bed]]
    prof += [[t, _p24_zat(land["NE"], t) if kinds["NE"] != "dsi_wall" or t > hw + P24_WALL_T + 2.0
              else tops["NE"]] for t in ts if t > hw]
    return prof, kinds, tops


def p24_zone(C, p):
    """what the masterplan puts at survey point p (a P24_NAME key) or None: its zones first, then the widened stream,
    the hub squares, buildings and roads of the survey grid"""
    for z in C.D.zones:
        k_ = P24_KEY.get((z["code"], z.get("tier") if z["code"] == "WA" else None))
        if k_ and pip(p[0], p[1], z["P"]):
            return k_
    if any(pip(p[0], p[1], w["ring"]) for w in C.widen):
        return "wetland"
    for h in C.hubs:
        if any(len(L_) >= 3 and pip(p[0], p[1], L_) for L_ in h.get("square") or []):
            return "hub"
    n = C.cell(p)
    if n is not None and C.F[n] in (1, 2):
        return "bld" if C.F[n] == 1 else "street"
    return None


def p24_runs(C, c0, cd, ta, tb, hw):
    """[[key, t0, t1]] the zones along the cut (bed = the bed width), from P24_STEP_M samples"""
    runs = []
    t = ta
    while t < tb:
        tm = min(tb, t + P24_STEP_M)
        u = (t + tm) / 2.0
        key = "bed" if abs(u) <= hw else p24_zone(C, (c0[0] + cd[0] * u, c0[1] + cd[1] * u))
        if key == "subhub" and abs(u) > hw:
            key = "wetland"
        if runs and runs[-1][0] == key:
            runs[-1][2] = tm
        else:
            runs.append([key, t, tm])
        t = tm
    return [r_ for r_ in runs if r_[0] is not None]


def _p24_set(prof, t0, t1, fn, hw):
    """z = fn(t, z) for the profile points in t0..t1 outside the bed (the bed and its wall faces, |t| <= hw, keep
    theirs)"""
    for p in prof:
        if t0 <= p[0] <= t1 and abs(p[0]) > hw + 1e-6:
            p[1] = fn(p[0], p[1])


def _p24_cut_in(prof, a, b, pts):
    """the profile with the points between a and b replaced by pts (left to right)"""
    return [p for p in prof if p[0] < a] + [list(q) for q in pts] + [p for p in prof if p[0] > b]


class P24Sec(object):
    """One section in print mm at 1:1,000 (k = 1 mm per m): x = (t - ta) k, y = (z - z0) k."""

    def __init__(self, ta, tb, z0):
        self.ta, self.tb, self.z0, self.k = ta, tb, z0, 1000.0 / DT_SCALE
        self.w = (tb - ta) * self.k
        self.pg = Page(self.w, 0.0)
        self.shapes = []                                 # what the plants and figures added (for the top)
        self.zl = []                                     # zone lines: (name, t, z of the ground, beyond)
        self.lv = []                                     # level words: (text, t, z)

    def X(self, t):
        return (t - self.ta) * self.k

    def Y(self, z):
        return (z - self.z0) * self.k

    def put(self, shapes, alpha=None):
        _p24_put(self.pg, shapes, alpha)
        self.shapes += shapes

    def plant(self, key, t, z, beyond=False, seed=0, **kw):
        self.put(pla_section(key, self.X(t), self.Y(z), self.k, beyond=beyond, seed=seed, **kw))

    def fig(self, pose, t, z, facing=1, **kw):
        self.put(fig_side(pose, self.X(t), self.Y(z), self.k, facing=facing, mm_per_m=self.k, **kw))

    def block(self, t0, t1, z0, z1, material):
        a, b = sorted((t0, t1))
        self.put(sct_hatch_fill([(self.X(a), self.Y(z0)), (self.X(b), self.Y(z0)), (self.X(b), self.Y(z1)),
                                 (self.X(a), self.Y(z1))], material, self.k, SCT["cut"], 0.2))


def p24_section(C, w, warn):
    """v28 (WO-T4b-3): the section under window w (P24_CUTS), as (Page, w mm, h mm, legend keys, words not placed);
    None when the window has no cut. Looks upstream: the SW bank on the left, as the plan reads it."""
    cid, name = P24_CUTS.get(w["id"], (None, None))
    if not cid:
        return None
    R = w["R"]
    E = level_ends(cid)
    c0 = CUT_AT[{"W1": 0, "W3": 2}[cid]][2]
    L = math.hypot(E[1][0] - E[0][0], E[1][1] - E[0][1]) or 1.0
    cd = ((E[1][0] - E[0][0]) / L, (E[1][1] - E[0][1]) / L)            # SW end -> NE end
    if level_end_labels(cid)[0] != u"SW":
        cd = (-cd[0], -cd[1])
    f = (-cd[1], cd[0])                                                # the view: the SW end on its left
    tin = [-P24_HALF_M, P24_HALF_M]
    for ax, lo, hi in ((0, R[0], R[2]), (1, R[1], R[3])):             # the cut line inside the window
        if abs(cd[ax]) > 1e-9:
            ts_ = sorted(((lo - c0[ax]) / cd[ax], (hi - c0[ax]) / cd[ax]))
            tin = [max(tin[0], ts_[0]), min(tin[1], ts_[1])]
    ta, tb = tin
    bed, hw = level(cid, "bed"), level(cid, "bed_width_cm") / 200.0
    q100, q500 = level(cid, "q100"), level(cid, "q500")
    if tb - ta < 2 * hw + 10.0:
        warn.append(u"section {}: the cut line has only {:.0f} m inside the window: not drawn".format(name, tb - ta))
        return None
    prof, kinds, tops = p24_profile(C, cid, c0, cd, ta, tb, warn)
    runs = p24_runs(C, c0, cd, ta, tb, hw)
    keys = set()
    # ---- the proposal in the ground: wetland benches (the bank cut back), the garden raised above Q500, hub squares
    # and streets flat, reed cells under one rim, terraces at the plan's terrace edges, the walk flat
    bench = bed + TERRACE_UP
    gf = math.ceil((q500 + P24_FREEBOARD) * 20.0) / 20.0
    gone = set()
    for key, t0, t1 in runs:
        if key == "wetland":
            _p24_set(prof, t0, t1, lambda t, z: min(z, bench), hw)
            for side, sg in (("SW", -1.0), ("NE", 1.0)):
                if kinds[side] == "dsi_wall" and min(abs(t0 - sg * hw), abs(t1 - sg * hw)) <= P24_WALL_T + 2.5:
                    gone.add(side)
        elif key == "demeter":
            _p24_set(prof, t0, t1, lambda t, z: max(z, gf), hw)
        elif key in ("hub", "street", "reed"):
            zs = [p[1] for p in prof if t0 <= p[0] <= t1 and abs(p[0]) > hw]
            if zs:
                zf = min(zs) if key == "reed" else sum(zs) / len(zs)
                _p24_set(prof, t0, t1, lambda t, z, zf=zf: zf, hw)
    for side in gone:                                     # the DSİ wall gives way to the wetland's soft toe
        sg = -1.0 if side == "SW" else 1.0
        prof = [p for p in prof if not (abs(p[0] - sg * hw) < 1e-6 and abs(p[1] - tops[side]) < 1e-6)]
        _p24_set(prof, min(sg * hw, sg * (hw + 2.0)), max(sg * hw, sg * (hw + 2.0)),
                 lambda t, z: bed + (bench - bed) * min(1.0, (abs(t) - hw) / 2.0), hw)
    terr = []
    for P in C.terr:                                      # the plan's terrace edges: a bench 4 m uphill of each
        for t in _p24_crossings(c0, cd, P, ta + 4.0, tb - 4.0):
            if abs(t) <= hw + 2.0:
                continue
            z0_ = _p24_zat(prof, t)
            sg = 1.0 if _p24_zat(prof, t + 3.0) > _p24_zat(prof, t - 3.0) else -1.0
            te = t + sg * R28DT_TERR_M
            zt = _p24_zat(prof, te)
            _p24_set(prof, min(t, te), max(t, te), lambda t_, z, z0_=z0_: z0_, hw)
            terr.append((t, te, z0_, zt, sg))
    walks = []
    for P in C.canopy:
        for t in _p24_crossings(c0, cd, P, ta + 2.0, tb - 2.0):
            if abs(t) > hw + 1.0:
                zw = _p24_zat(prof, t)
                _p24_set(prof, t - WALK_W / 2.0, t + WALK_W / 2.0, lambda t_, z, zw=zw: zw, hw)
                walks.append((t, zw))
    cells = []
    kt = 0.15
    ln, gap, dep, media, wl = P24_BASIN
    for key, t0, t1 in runs:
        if key != "reed":
            continue
        a = t0 + 1.0
        while a + ln <= t1 - 1.0:
            rim = _p24_zat(prof, a)
            prof = _p24_cut_in(prof, a - kt, a + ln + kt, [(a - kt, rim), (a - kt, rim - dep - kt),
                                                          (a + ln + kt, rim - dep - kt), (a + ln + kt, rim)])
            cells.append((a, a + ln, rim))
            a += ln + gap
    z0 = min([p[1] for p in prof] + [bed]) - P24_BELOW_M
    S = P24Sec(ta, tb, z0)
    X, Y, k = S.X, S.Y, S.k
    # ---- the reach of Q500 (wash) where it joins the stream, the Q100 and Q500 lines over it
    lo_, hi_ = 0.0, 0.0
    while lo_ > ta and _p24_zat(prof, lo_ - P24_STEP_M) < q500:
        lo_ -= P24_STEP_M
    while hi_ < tb and _p24_zat(prof, hi_ + P24_STEP_M) < q500:
        hi_ += P24_STEP_M
    if hi_ > lo_:
        n_ = int((hi_ - lo_) / P24_STEP_M)
        ring_ = [(X(lo_), Y(q500))] + [(X(lo_ + i * P24_STEP_M), Y(_p24_zat(prof, lo_ + i * P24_STEP_M)))
                                       for i in range(n_ + 1)] + [(X(hi_), Y(q500))]
        S.pg.poly([ring_], fill=P24_FLOOD, alpha=P24_FLOOD_A)
        for lv_, dash in ((q100, [1.2, 0.6]), (q500, [0.4, 0.4])):
            S.pg.line([(X(lo_), Y(lv_)), (X(hi_), Y(lv_))], COL["river_dark"], 0.2, dash, cap=0)
        S.lv.append((u"Q100 {} · Q500 {}".format(u_level(q100), u_level(q500)), hi_, q500))
        keys.add("flood")
    # ---- the cut ground, the bed, the walls kept (railings) or given way (today's wall dashed)
    S.put(sct_ground([(X(p[0]), Y(p[1])) for p in prof], 0.0, k))
    S.put(sct_bed(X(-hw), X(hw), Y(bed), k, depth_m=1.0))
    S.lv.append((u"bed " + u_level(bed), 0.0, bed))
    for side, sg in (("SW", -1.0), ("NE", 1.0)):
        if kinds[side] != "dsi_wall":                     # an earth bank: the survey draws it (its crest has no
            continue                                      # place on the cut in the level table, so no level word)
        a, b = sg * hw, sg * (hw + P24_WALL_T)
        ring_ = [(X(a), Y(bed)), (X(b), Y(bed)), (X(b), Y(tops[side])), (X(a), Y(tops[side]))]
        if side in gone:
            S.pg.poly([ring_], stroke=COL["ink2"], lw=0.15, dash=[0.8, 0.5])
            continue
        S.put(sct_hatch_fill(ring_, "stone", k, SCT["cut"], 0.3))
        S.put(sct_bank("railing", X((a + b) / 2.0), Y(tops[side]), Y(bed), -sg, k, h_m=P24_RAIL_H)[0])
        S.lv.append((u_level(tops[side]), b, tops[side] + P24_RAIL_H))
        keys.add("wall")
    # ---- what each zone holds: planting, paving, cells, the garden, people placed by what they do there
    near = lambda pts, d: [(t, i) for i, p in enumerate(pts) for t, dd in [_p24_tz(c0, cd, f, p)]
                           if ta + 2.0 <= t <= tb - 2.0 and abs(dd) <= d and abs(t) > hw + 1.0]
    for t, i in near(C.forest, P24_TREE_M):
        S.plant("ash" if i % 2 else "plane", t, _p24_zat(prof, t), seed=i)
        keys.add("forest")
    for t, i in near(C.trees, P24_TREE_M):
        S.plant("plane" if i % 2 else "ash", t, _p24_zat(prof, t), seed=50 + i)
        keys.add("forest")
    railed = False
    for side, sg in (("SW", -1.0), ("NE", 1.0)):         # one figure at a railing, looking into the channel
        if kinds[side] == "dsi_wall" and side not in gone and not railed:
            fc = 1 if sg < 0 else -1
            m_ = fig_meta("railing", facing=fc, rail_h=P24_RAIL_H)
            S.fig("railing", sg * (hw + P24_WALL_T / 2.0) - m_.get("rail_x", 0.0), tops[side], facing=fc,
                  rail_h=P24_RAIL_H)
            railed = True
    for key, t0, t1 in runs:
        ln_, tm = t1 - t0, (t0 + t1) / 2.0
        fc = 1 if tm < 0 else -1                          # people face the stream
        if key == "hub":
            zf = _p24_zat(prof, tm)
            S.block(t0, t1, zf - P24_PAVE_T, zf, "stone")
            hub_t = [t for h in C.hubs for t, i in near(h.get("trees") or [], P24_TREE_M)]
            for j, t in enumerate(hub_t or [tm]):
                S.plant("plane", t, zf, seed=70 + j)
            S.fig("sit_chair", tm - 2.0, zf, facing=fc)
            S.fig("stand", tm + 2.5, zf, facing=-fc)
            S.lv.append((u_level(zf), tm, zf))
        elif key == "street":
            zf = _p24_zat(prof, tm)
            S.block(t0, t1, zf - P24_PAVE_T, zf, "concrete")
            if ln_ >= 6.0:
                S.fig("walk", tm, zf, facing=fc)
        elif key == "demeter":
            ts_ = sorted((t0, t1), key=abs)
            te = ts_[0]                                   # the garden's stream-side edge: a stone wall
            sg = 1.0 if te > tm else -1.0
            S.block(te, te - sg * P24_WALL_DG, gf - 1.0, gf + 0.15, "stone")
            x0_, x1_ = X(min(t0, t1) + 1.5), X(max(t0, t1) - 1.5)
            if x1_ > x0_:
                S.put(pla_crop_rows("olive", x0_, x1_, Y(gf), k))
                n_ = int((x1_ - x0_) / (PLA_CROPS["olive"]["row_m"] * k) + 1e-9)
                t_o = min(t0, t1) + 1.5 + ((x1_ - x0_) - n_ * PLA_CROPS["olive"]["row_m"] * k) / 2.0 / k
                S.fig("olive", t_o + 1.3, gf, facing=-1)
            S.plant("lavender", te - sg * 1.2, gf, seed=81)
            S.lv.append((u_level(gf), tm, gf))
        elif key == "wetland" and abs(tm) > hw:
            z_ = lambda t: _p24_zat(prof, t)
            if ln_ >= 12.0:
                S.plant("willow", tm, z_(tm), seed=90)
            if ln_ >= 20.0:
                S.plant("tamarisk", t0 + ln_ / 4.0, z_(t0 + ln_ / 4.0), seed=91)
                S.plant("tamarisk", t1 - ln_ / 4.0, z_(t1 - ln_ / 4.0), seed=92)
            te = min((t0, t1), key=abs)
            sg = 1.0 if tm > 0 else -1.0
            for j in range(int(min(6.0, ln_ - 1.0) / 1.5)):
                t = te + sg * (0.75 + j * 1.5)
                S.plant("loosestrife" if j % 2 else "soft_rush", t, z_(t), seed=95 + j)
            if ln_ >= 8.0:
                S.fig("watch", te + sg * 3.0, z_(te + sg * 3.0), facing=-1 if sg > 0 else 1)
        elif key == "terraces":
            t = t0 + 1.25
            j = 0
            while t < t1 - 1.0:
                S.plant("lavender", t, _p24_zat(prof, t), seed=100 + j)
                t += 2.5
                j += 1
            if ln_ >= 8.0:
                S.fig("walk", tm, _p24_zat(prof, tm), facing=fc)
        elif key == "bld":
            zf = _p24_zat(prof, tm)
            S.pg.line([(X(t0), Y(zf) + 0.4), (X(t1), Y(zf) + 0.4)], COL["bld"], 0.8, cap=0)
    for a, b, rim in cells:                               # the lined reed cells (D2 a), above Q500 by their rim
        fl = rim - P24_BASIN[2]
        S.put(pla_reed_basin(X(a), X(b), Y(fl), Y(rim), k, P24_KERB_H, media_m=P24_BASIN[3],
                             wl_y=Y(fl + P24_BASIN[4])))
        keys.add("reed")
    if cells:
        a, b, rim = cells[0]
        S.fig("touch", a - 0.7, rim, facing=1)            # the clean-water classroom: a hand into the cell
        S.lv.append((u_level(cells[0][2]), (cells[0][0] + cells[-1][1]) / 2.0, cells[0][2]))
    for t, te, z0_, zt, sg in terr:                       # each terrace's riser, where the old ground stood higher
        if zt > z0_ + 0.05:
            S.block(te, te + sg * 0.15, z0_ - 0.3, zt, "concrete")
        keys.add("terraces")
    for j, (t, zw) in enumerate(walks):                   # the riverside walk, its bike lane
        S.fig("walk", t - 0.6, zw, facing=1 if j % 2 else -1)
        if P24_BIKE:
            S.fig("bike", t + 0.4, zw, facing=-1 if j % 2 else 1)
        S.zl.append((P24_NAME["walk"], t, zw, False))
        keys.add("walk")
    # ---- zone lines: one per run (bed = the stream), then what stands beyond the cut, paler
    for key, t0, t1 in runs:
        if key in P24_NAME and (t1 - t0 >= P24_MIN_RUN or key == "bed") and key != "walk":
            tm = (t0 + t1) / 2.0
            S.zl.append((P24_NAME[key], tm, _p24_zat(prof, tm), False))
    crossed = set(r_[0] for r_ in runs)
    seen = set()
    for z in C.D.zones:
        key = P24_KEY.get((z["code"], z.get("tier") if z["code"] == "WA" else None))
        if not key or key in crossed or key in seen or not z.get("P"):
            continue
        q = inner_pt(z["P"])
        t, d = _p24_tz(c0, cd, f, q)
        if 0.0 < d <= P24_BEYOND_M and ta + 3.0 <= t <= tb - 3.0 and R[0] <= q[0] <= R[2] and R[1] <= q[1] <= R[3]:
            seen.add(key)
            zz = _p24_zat(prof, t)
            sp_ = {"hub": "plane", "demeter": "olive", "wetland": "willow", "forest": "ash", "terraces": "lavender"}
            if key in sp_:
                S.plant(sp_[key], t, zz, beyond=True, seed=120 + len(seen))
            S.zl.append((P24_NAME[key], t, zz, True))
    for h in C.hubs:                                      # a hub square beyond: its planes, paler
        if "hub" in crossed or "hub" in seen:
            break
        for t_, i in [(t, i) for i, p in enumerate(h.get("trees") or []) for t, d in [_p24_tz(c0, cd, f, p)]
                      if 0.0 < d <= P24_BEYOND_M and ta + 3.0 <= t <= tb - 3.0]:
            S.plant("plane", t_, _p24_zat(prof, t_), beyond=True, seed=130 + i)
            if "hub" not in seen:
                S.zl.append((P24_NAME["hub"], t_, _p24_zat(prof, t_), True))
                seen.add("hub")
    for c_ in C.cross:                                    # footbridges and stepping stones beyond
        ts_ = [_p24_tz(c0, cd, f, p) for p in c_["P"]]
        if not all(0.0 < d <= P24_BEYOND_M for _, d in ts_):
            continue
        t1_, t2_ = sorted(t for t, _ in ts_)
        if t2_ < ta or t1_ > tb:
            continue
        t1_, t2_ = max(ta, t1_), min(tb, t2_)
        if c_["kind"] == "footbridge":
            zd = max(_p24_zat(prof, t1_), _p24_zat(prof, t2_))
            S.pg.line([(X(t1_), Y(zd)), (X(t2_), Y(zd))], COL["ink2"], 0.6, cap=0, alpha=0.6)
            S.zl.append((P24_NAME["foot"], (t1_ + t2_) / 2.0, zd, True))
        elif c_["kind"] == "stepping stones":
            t = max(t1_, -hw) + P24_STONE[1] / 2.0
            while t < min(t2_, hw):
                S.pg.circle(X(t), Y(bed) + P24_STONE[0] * k, P24_STONE[0] * k, fill=COL["ink2"], alpha=0.5)
                t += P24_STONE[1]
            S.zl.append((P24_NAME["stones"], 0.0, bed, True))
    if C.terrace:
        t, d = _p24_tz(c0, cd, f, C.terrace["xy"])
        if 0.0 < d <= P24_BEYOND_M and ta + 3.0 <= t <= tb - 3.0:
            zz = _p24_zat(prof, t)
            S.pg.line([(X(t - 2.0), Y(zz + 0.3)), (X(t + 2.0), Y(zz + 0.3))], COL["ink2"], 0.5, cap=0, alpha=0.6)
            S.zl.append((P24_NAME["view"], t, zz, True))
    # ---- words: the zone lines and names in rows above everything (R18 idea), the levels by their points
    top = max([_p24_top(S.shapes) or 0.0] + [Y(p[1]) for p in prof]) + 2.0
    rows = [[] for _ in range(P24_LAB_ROWS)]
    ts_lab, missing = KEY_MIN, []
    pitch = ts_lab * 1.45
    for nm, t, zz, beyond in sorted(S.zl, key=lambda z_: z_[1]):
        s_ = nm + (u" · BEYOND" if beyond else u"")
        wd = text_w(s_, ts_lab)
        x = min(max(X(t), wd / 2.0), S.w - wd / 2.0)
        r_ = next((i for i, row in enumerate(rows) if all(x - wd / 2.0 > b + 1.0 or x + wd / 2.0 < a - 1.0
                                                         for a, b in row)), None)
        if r_ is None:
            missing.append(s_)
            continue
        rows[r_].append((x - wd / 2.0, x + wd / 2.0))
        yl = top + r_ * pitch
        col = COL["ink2"] if beyond else COL["ink_dark"]
        S.pg.line([(X(t), Y(zz) + 0.3), (X(t), yl - 0.4)], col, 0.12, [0.6, 0.4] if beyond else None, cap=0)
        S.pg.text(s_, x, yl, ts_lab, col, bold=not beyond, align="C")
    h = top + (max([i + 1 for i, row in enumerate(rows) if row] or [0]) + 0.4) * pitch
    used = [r for row in rows for r in row]
    taken = [(a, top - 0.5, b, h) for a, b in used]
    for s_, t, al in ((name, ta, "L"), (name + u"'", tb, "R")):   # the cut's names, as on the plan
        x, y = X(t) + (0.6 if al == "L" else -0.6), Y(_p24_zat(prof, t)) + 1.2
        S.pg.text(s_, x, y, 3.4, COL["ink_dark"], bold=True, align=al)
        wd = text_w(s_, 3.4, True)
        taken.append((x if al == "L" else x - wd, y - 0.3, x + wd if al == "L" else x, y + 3.4))
    for s_, t, zz in S.lv:
        wd = text_w(s_, ts_lab)
        got = label_spot(X(t), Y(zz) + 1.2, wd, ts_lab * 1.1, taken, (0.0, 0.5, S.w, top - 0.5), (), 0.3)
        if got is None:
            missing.append(s_)
            continue
        b = got[0]
        S.pg.text(s_, b[0], b[1] + ts_lab * 0.2, ts_lab, COL["ink"])
        taken.append(b)
    keys.add("section")
    return S.pg, S.w, h, keys, missing


def p24_cut_on_plan(pg, w, T, taken, segs, bounds):
    """the section's line on the plan (only this window's cut): dash-dot across the window, a triangle at each end
    pointing the way the section looks (upstream), its names at the ends (D1, D1')."""
    cid, name = P24_CUTS.get(w["id"], (None, None))
    if not cid:
        return False
    R = w["R"]
    E = level_ends(cid)
    c0 = CUT_AT[{"W1": 0, "W3": 2}[cid]][2]
    L = math.hypot(E[1][0] - E[0][0], E[1][1] - E[0][1]) or 1.0
    cd = ((E[1][0] - E[0][0]) / L, (E[1][1] - E[0][1]) / L)
    if level_end_labels(cid)[0] != u"SW":
        cd = (-cd[0], -cd[1])
    f = (-cd[1], cd[0])                                  # the view (as p24_section): the SW end on its left
    tin = [-P24_HALF_M, P24_HALF_M]
    for ax, lo, hi in ((0, R[0], R[2]), (1, R[1], R[3])):
        if abs(cd[ax]) > 1e-9:
            ts_ = sorted(((lo - c0[ax]) / cd[ax], (hi - c0[ax]) / cd[ax]))
            tin = [max(tin[0], ts_[0]), min(tin[1], ts_[1])]
    A = T((c0[0] + cd[0] * tin[0], c0[1] + cd[1] * tin[0]))
    B = T((c0[0] + cd[0] * tin[1], c0[1] + cd[1] * tin[1]))
    ink = COL["ink_dark"]
    pg.line([A, B], ink, 0.35, [2.4, 0.8, 0.4, 0.8], cap=0)
    segs.append((A, B))
    s = 2.2
    for (x, y), nm in ((A, name), (B, name + u"'")):
        tip = (x + f[0] * s, y + f[1] * s)
        pg.poly([[tip, (x - cd[0] * s * 0.55, y - cd[1] * s * 0.55), (x + cd[0] * s * 0.55, y + cd[1] * s * 0.55)]],
                fill=ink)
        taken.append((x - s, y - s, x + s, y + s))
        _r28_label(pg, [(nm, R28DT_TS["place"], True, ink)], (x - f[0] * 1.5, y - f[1] * 1.5), taken, segs, bounds)
    return True


def _p24_offset(P, d):
    """polyline P (survey m) moved d m to its left (per-vertex normals)"""
    out = []
    for i, p in enumerate(P):
        a, b = P[max(0, i - 1)], P[min(len(P) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        out.append((p[0] - dy / L * d, p[1] + dx / L * d))
    return out


def _p24_land_side(C, P):
    """+1 when the land (away from the water) lies to the left of walk P, else -1 (the corridor's distance from the
    water a few metres either side of its middle)"""
    s = arclen(P)
    (x, y), (ux, uy) = at_len(P, s, s[-1] / 2.0)
    d = []
    for sg in (1.0, -1.0):
        n = C.cell((x - uy * 4.0 * sg, y + ux * 4.0 * sg))
        d.append(C.Dst[n] if n is not None and C.Dst[n] < 1e8 else 0.0)
    return 1.0 if d[0] >= d[1] else -1.0


def p24_plan(pg, C, w, T, inP, on, k, taken, segs, dw, dh):
    """v28 (WO-T4b-3): the window's proposal in the architectural plan language, each element its own symbol and
    texture at true size; returns [(field key, page rings)] for the titles."""
    ink, ink2, white = COL["ink_dark"], COL["ink2"], COL["white"]
    TP = lambda P: [T(p) for p in P]
    fields = []
    # ---- fields: wetland (widened stream and flood terraces), terraces, spillway, sub-hub bed, forest walk
    for z in C.D.zones:
        key = P24_KEY.get((z["code"], z.get("tier") if z["code"] == "WA" else None))
        Q = TP(z["P"]) if key else None
        if not Q or not on(Q):
            continue
        if key == "wetland":
            pg.poly([Q], fill=WET_COL, alpha=0.55, stripes=(COL["river_dark"], 1.4, 0.1, 0.0, True))
        elif key == "terraces":
            pg.poly([Q], fill=R28_ZONE["terraces"][1], alpha=0.18)
        elif key == "spill":
            pg.poly([Q], fill=COL["river"], alpha=0.6, stripes=(COL["river_dark"], 0.8, 0.1, 90.0))
        elif key == "subhub":
            pg.poly([Q], fill=R28_ZONE["subhub"][1], alpha=0.25)
        elif key == "forest":
            pg.poly([Q], fill=R28_ZONE["forest"][1], alpha=0.15)
        elif key == "reed":
            _p24_put(pg, pla_cell_plan("reed", Q, k))         # lined, root-contained cells (D2 a)
        elif key == "demeter":
            _p24_put(pg, pla_crop_plan("olive", Q, k, ang_deg=principal_angle(z["P"])))   # 7 x 5 m (Kaya 2017)
        fields.append((key, Q))
        leg(("p24", key))
    for wd in C.widen:
        Q = TP(wd["ring"])
        if on(Q):
            pg.poly([Q], fill=WET_COL, alpha=0.55, stripes=(COL["river_dark"], 1.4, 0.1, 0.0, True))
            fields.append(("wetland", Q))
            leg(("p24", "wetland"))
    for a in C.arms:                                      # planted side arm (no reed in the open bed, D2 a)
        Q = TP(a["P"])
        if on(Q):
            pg.line(Q, COL["river"], max(1.0, 6.0 * k), alpha=0.8)
            pg.line(Q, COL["river_dark"], 0.15, [0.6, 0.6], cap=0)
            leg(("p24", "arm"))
    # ---- hub squares: paving grid, their planes
    for h in C.hubs:
        for L_ in h.get("square") or []:
            Q = TP(L_)
            if len(Q) >= 3 and on(Q):
                pg.poly([Q], fill=SQ_FILL, stroke=SQ_EDGE, lw=0.2)
                pg.poly([Q], stripes=(SQ_EDGE, 2.0, 0.06, 0.0), alpha=0.6)
                pg.poly([Q], stripes=(SQ_EDGE, 2.0, 0.06, 90.0), alpha=0.6)
                fields.append(("hub", Q))
                leg(("p24", "hub"))
        for i, p in enumerate(h.get("trees") or []):
            if inP(p):
                x, y = T(p)
                _p24_put(pg, pla_plan("plane", x, y, k, seed=i), alpha=0.85)
                leg(("p24", "tree"))
    # ---- terrace edges: a line with ticks down toward the stream
    for P in C.terr:
        Q = TP(P)
        if on(Q):
            ticks_line(pg, Q, R28_ZONE["terraces"][1], 0.3, 1.6, 0.8, 1.0, alpha=0.9)
            segs += list(zip(Q, Q[1:]))
            leg(("p24", "terr"))
    # ---- trees at their true crown width: the forest corridor (ash, plane), the tree-planted area (paler)
    for pts, bey, key in ((C.forest, False, "forest_tree"), (C.trees, True, "forest_tree")):
        for i, p in enumerate(pts):
            if inP(p):
                x, y = T(p)
                _p24_put(pg, pla_plan("ash" if i % 2 else "plane", x, y, k, beyond=bey, seed=i), alpha=0.8)
                leg(("p24", "tree"))
    # ---- the riverside walk with its bike lane on the land side
    for P in C.canopy:
        Q = TP(P)
        if not on(Q) or len(P) < 2:
            continue
        pg.line(Q, ink2, WALK_W * k + 0.3, cap=0)
        pg.line(Q, white, WALK_W * k, cap=0)
        segs += list(zip(Q, Q[1:]))
        leg(("p24", "walk"))
        if P24_BIKE:
            sg = _p24_land_side(C, P)
            B = TP(_p24_offset(P, sg * (WALK_W + P24_BIKE_W) / 2.0))
            pg.line(B, P24_BIKE_COL, P24_BIKE_W * k, cap=0, alpha=0.55)
            pg.line(B, white, 0.12, [1.0, 1.0], cap=0)
            s = arclen(B)
            t = min(25.0 * k, s[-1] / 2.0)
            while t < s[-1]:
                (x, y), _ = at_len(B, s, t)
                _p24_put(pg, ico_draw("bike", x, y, 2.6, ink=P24_BIKE_COL))
                taken.append((x - 1.3, y - 1.3, x + 1.3, y + 1.3))
                t += 60.0 * k
            leg(("p24", "bike"))
    # ---- crossings: stepping stones (true size), footbridge decks (the walk's width)
    for c_ in C.cross:
        A_, B_ = c_["P"][0], c_["P"][1]
        if c_["kind"] == "stepping stones" and (inP(A_) or inP(B_)):
            L = math.hypot(B_[0] - A_[0], B_[1] - A_[1]) or 1.0
            n = max(2, int(L / P24_STONE[1]))
            for i in range(n):
                fr = (i + 0.5) / n
                x, y = T((A_[0] + (B_[0] - A_[0]) * fr, A_[1] + (B_[1] - A_[1]) * fr))
                pg.circle(x, y, max(0.3, P24_STONE[0] * k), fill=ink2)
            taken += boxes_along([T(A_), T(B_)], 1.0)
            leg(("p24", "stones"))
        elif c_["kind"] == "footbridge" and (inP(A_) or inP(B_)):
            ring_ = TP(_p24_offset([A_, B_], WALK_W / 2.0)) + list(reversed(TP(_p24_offset([A_, B_], -WALK_W / 2.0))))
            pg.poly([ring_], fill=white, stroke=ink, lw=0.25)
            segs += list(zip(ring_, ring_[1:] + ring_[:1]))
            leg(("p24", "foot"))
    # ---- the roads changed: a band in the change's colour with its marking (calmed: dashes; pedestrian: dots;
    # shared: ticks)
    for rd in ROADS:
        if rd["change"] not in ("calmed", "pedestrian", "shared"):
            continue
        Q = TP(rd["xy"])
        if not on(Q):
            continue
        col = ROAD_CHANGE_COL[rd["change"]]
        pg.line(Q, col, 7.0 * k, cap=0, alpha=0.28)
        if rd["change"] == "calmed":
            pg.line(Q, col, 0.25, [1.6, 1.2], cap=0)
        elif rd["change"] == "pedestrian":
            s = arclen(Q)
            t = 0.0
            while t <= s[-1]:
                (x, y), _ = at_len(Q, s, t)
                pg.circle(x, y, 0.3, fill=col)
                t += 1.6
        else:
            ticks_line(pg, Q, col, 0.25, 2.0, 1.0, 1.0)
        leg(("p24", "road_" + rd["change"]))
    # ---- the hidden stream; the viewing terrace and its sightline; cafés
    for P in C.covered:
        Q = TP(P)
        if on(Q):
            pg.line(Q, COL["river_mid"], 1.2, [1.6, 0.9], cap=0, alpha=0.7)
            leg(("p24", "hidden"))
    if C.terrace and inP(C.terrace["xy"]):
        x, y = T(C.terrace["xy"])
        p2 = (C.terrace["xy"][0] + C.terrace["dir"][0] * 400.0, C.terrace["xy"][1] + C.terrace["dir"][1] * 400.0)
        pg.line([(x, y), T(p2)], COL["accent"], 0.3, [1.4, 0.8], cap=0, alpha=0.7)
        _p24_put(pg, ico_draw("viewpoint", x, y, 3.2))
        taken.append((x - 1.6, y - 1.6, x + 1.6, y + 1.6))
        leg(("p24", "view"))
    for z in C.D.zones:
        if z["code"] in ("GR", "DG") and inP(z["q"]):
            x, y = T(z["q"])
            _p24_put(pg, ico_draw("cafe", x, y, 3.0))
            taken.append((x - 1.5, y - 1.5, x + 1.5, y + 1.5))
            leg(("p24", "cafe"))
    return fields


def r28_window_panel(C, w, areas, missing, warn):
    """v28 (revision 29 Oct, WO-T4b-3; package H "Page 24"): a 1:1,000 window, north up: the faint survey, the
    proposal in the architectural plan language (p24_plan), the water route 1-4, the study area, the section line
    (this window's only); one title per field, place names, small words. Under it its section (p24_section, D1 or
    D2) at the same scale. One crop: the plan with its north arrow and scale bar, the section with its own."""
    R = w["R"]
    k = 1000.0 / DT_SCALE
    dw, dh = (R[2] - R[0]) * k, (R[3] - R[1]) * k
    T = lambda p: ((p[0] - R[0]) * k, (p[1] - R[1]) * k)
    inP = lambda p: R[0] <= p[0] <= R[2] and R[1] <= p[1] <= R[3]
    on = lambda Q: hit(bbox(Q), (0.0, 0.0, dw, dh))
    _PLEG[0] = {}
    pg = Page(dw, dh)
    taken, segs, ts = [], [], R28DT_TS
    ink, ink1, ink2, white = COL["ink_dark"], COL["ink"], COL["ink2"], COL["white"]
    bounds = (1.0, 1.0, dw - 1.0, dh - 1.0)
    _r28_base(pg, C, T, R, segs)
    fields = p24_plan(pg, C, w, T, inP, on, k, taken, segs, dw, dh)
    # ---- the water route (P24.2): the zone base's water links in the route's order, one line language on top
    rc = R28DT_ROUTE
    steps, shapes = [], C.D.zones + C.D.strips
    for L in C.D.links:
        if L["kind"] != "water" or len(L["P"]) < 2 or not any(inP(p) for p in L["P"]):
            continue
        a, b = link_shapes(L, shapes)
        ab = (a["code"] if a and a in C.D.zones else None, b["code"] if b and b in C.D.zones else None)
        steps.append((next((i for i, st in enumerate(ROUTE) if st[0] == ab), len(ROUTE)), L, a, b))
    steps.sort(key=lambda s_: s_[0])
    dots, key_lines = [], []
    for n_, (order, L, a, b) in enumerate(steps, 1):
        P = [T(p) for p in L["P"]]
        s = arclen(P)
        if s[-1] < 0.5:
            continue
        hl = min(1.8, s[-1] * 0.45)                      # arrowhead length, mm
        (tx, ty), (ux, uy) = at_len(P, s, s[-1])
        bx, by = tx - ux * hl, ty - uy * hl
        pg.line(sub_line(P, s, 0.0, s[-1] - hl * 0.8), rc, 0.6, cap=1)
        pg.poly([[(tx, ty), (bx - uy * hl * 0.42, by + ux * hl * 0.42), (bx + uy * hl * 0.42, by - ux * hl * 0.42)]],
                fill=rc)
        segs += list(zip(P, P[1:]))
        dots.append((n_, P[0]))
        key_lines.append((n_, _r28_route_runs(order, L, a, b)))
        leg(("r28dt", "route"))
    r_ = 1.9
    for n_, (x, y) in dots:                              # the step's number at its start, nudged off when taken
        b = (x - r_, y - r_, x + r_, y + r_)
        far = False
        if not _r28_free(b, taken, (), bounds, 0.2):
            got = label_spot(x, y, 2 * r_, 2 * r_, taken, bounds, (), 0.2)
            if got:
                b, far = got
        cx, cy = (b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0
        if far:
            pg.line([(x, y), lp_leader_end(b, (x, y))], rc, 0.2)
        pg.circle(cx, cy, r_ + 0.25, fill=white)
        pg.circle(cx, cy, r_, fill=rc)
        pg.text(str(n_), cx, cy - ts["small"] * 0.36, ts["small"], white, bold=True, align="C")
        taken.append(b)
    # ---- G8: the study area where it crosses the window; the section line (D11: this window's cut only)
    st = R28_STUDY_LINE
    for A in (areas or {}).values():
        Q = [T(p) for p in list(A) + [A[0]]]
        if on(Q):
            pg.line(Q, st["colour"], st["width_mm"], list(st["dash_mm"]), cap=0)
            segs += list(zip(Q, Q[1:]))
            leg(("r28dt", "study"))
    if p24_cut_on_plan(pg, w, T, taken, segs, bounds):
        leg(("p24", "cut"))
    # ---- words (G4): place names, one title per field inside it (its species in small grey), the route key, then
    # the small words (dropped where there is no room)
    names = [(HUB_NAME[h["id"]], h["xy"]) for h in C.hubs] + \
        [(nm, xy) for nm, xy in BRIDGES_K if nm in (u"K1", u"K2")] + PLACES
    for nm, xy in names:
        if inP(xy) and not _r28_label(pg, [(nm, ts["place"], True, ink1)], T(xy), taken, segs, bounds):
            missing.append(nm)
    best = {}
    for key, Q in fields:
        vis = clip_ring(Q, (0.0, 0.0, dw, dh))
        if len(vis) >= 3 and abs(area2(vis)) >= R28DT_TITLE_MM2 and abs(area2(vis)) > abs(area2(best.get(key, [(0, 0)] * 3))):
            best[key] = vis
    fpts = [T(p) for p in C.forest if inP(p)]
    for key in R28DT_ORDER + ("spill",):
        if key not in best and not (key == "forest" and fpts):
            continue
        nm = R28_ZONE[key][0] if key in R28_ZONE else P24_NAME[key].capitalize()
        title = [(nm, ts["zone"], True, ink)]
        sub = [(_p24_sp(s_) + (u" · lined cells" if s_ == "reed" else u""), ts["small"], False, ink2)
               for s_ in P24_SPECIES.get(key, ())]
        if key in best:
            ok = _r28_title(pg, best[key], ([title + sub] if sub else []) + [title], taken, segs, bounds)
        else:                                             # the forest corridor is trees, not a field: by its middle tree
            fp = sorted(fpts)[len(fpts) // 2]
            ok = _r28_label(pg, title + sub, fp, taken, segs, bounds, rank=1) or \
                _r28_label(pg, title, fp, taken, segs, bounds, rank=1)
        if not ok:
            missing.append(nm)
    if key_lines:                                        # the route key (P24.2, G5): numbered dot, the step's words
        pitch, rr = 3.6, 1.5
        w_ = max([2 * rr + 1.2 + sum(text_w(t_, ts["label"], bd) for t_, bd in runs) for _, runs in key_lines] +
                 [text_w(u"Water route", ts["label"], True)])
        h_ = ts["label"] * 1.18 + 0.4 + pitch * len(key_lines)
        anc = (sum(p[0] for _, p in dots) / len(dots), sum(p[1] for _, p in dots) / len(dots)) if dots else \
            (dw / 2.0, dh / 2.0)
        got = _r28_spot(w_, h_, anc, taken, segs, bounds)
        if got:
            b = got[0]
            taken.append(b)
            y = b[3] - ts["label"]
            pg.text(u"Water route", b[0], y, ts["label"], ink, bold=True)
            y -= ts["label"] * 0.18 + 0.4
            for n_, runs in key_lines:
                cy = y - pitch / 2.0
                pg.circle(b[0] + rr, cy, rr, fill=rc)
                pg.text(str(n_), b[0] + rr, cy - ts["small"] * 0.36, ts["small"], white, bold=True, align="C")
                x = b[0] + 2 * rr + 1.2
                for t_, bd in runs:
                    pg.text(t_, x, cy - ts["label"] * 0.36, ts["label"], ink1, bold=bd)
                    x += text_w(t_, ts["label"], bd)
                y -= pitch
        else:
            missing.append(u"water route key")
    words = []
    for z in C.D.zones:
        if z["code"] == "WT":
            words.append((u"clean-water classroom", z["q"]))   # v24's education mark: city link stop 7
    if C.canopy:
        cp = [p for P in C.canopy for p in P if inP(p)]
        if cp:
            words.append((u"walk + bike lane" if P24_BIKE else u"riverside walk",
                          min(cp, key=lambda p: (T(p)[0] - dw / 2) ** 2 + (T(p)[1] - dh / 2) ** 2)))
    words += [(u"footbridge", c_["xy"]) for c_ in C.cross if c_["kind"] == "footbridge"]
    words += [(u"stepping stones", c_["xy"]) for c_ in C.cross if c_["kind"] == "stepping stones"]
    if C.terrace:
        words.append((u"viewing terrace", C.terrace["xy"]))
    words += [(u"step to the water", PLACES[1][1]), (u"deck on the Roman bank wall", ROMAN_WALL),
              (u"workshops", CRAFT_XY)]
    for rd in ROADS:
        if rd["change"] in ("pedestrian", "calmed", "shared"):
            P = rd["xy"]
            words.append((rd["change"] + (u" bridge" if u"Köprü" in rd["name"] else u" street"),
                          at_len(P, arclen(P), arclen(P)[-1] / 2.0)[0]))
    for s_, xy in words:
        if inP(xy) and not _r28_label(pg, [(s_, ts["small"], False, ink2)], T(xy), taken, segs, bounds, rank=1):
            missing.append(s_ + u" (no room)")
    # ---- the panel, bottom up: the section's scale bar row, the section, the plan's north arrow and scale bar, the
    # plan, its title (sheet only)
    M = 12.0
    sec = p24_section(C, w, warn)
    W = M + dw + M
    if sec:
        spg, sw_, shh, skeys, smiss = sec
        missing += smiss
        for k_ in skeys:
            leg(("p24s", k_))
        y_sec = 11.0
        y_mk = y_sec + shh + 3.0
    else:
        y_mk = 1.5
    y_pl = y_mk + 10.5
    H = y_pl + dh + 14.0
    sh = Page(W, H)
    sh.poly([rect(0, 0, W, H)], fill=COL["paper"])
    if sec:
        blit(sh, spg, M + (dw - sw_) / 2.0, y_sec)
        scale_bar(sh, M, 1.5, DT_SCALE, (0.0, 10.0, 20.0, 50.0))
        cid, nm = P24_CUTS[w["id"]]
        sh.text(u"Section {} {}' · from the stream to the edge, every zone of the plan above, looking upstream".format(
            nm, nm), M + 72.0, 1.7, ts["label"], COL["ink_dark"], bold=True)
    panel_marks(sh, M, y_mk, DT_SCALE, (0.0, 10.0, 20.0, 50.0))
    sh.clip([rect(M, y_pl, M + dw, y_pl + dh)])
    blit(sh, pg, M, y_pl)
    sh.unclip()
    sh.text(w["title"] + u" · 1:1,000", M, y_pl + dh + 5.0, 5.0, COL["ink_dark"], bold=True)
    sh.crop = (M, 0.5, M + dw, y_pl + dh)
    if y_pl + dh - 0.5 > P24_SEC_MAX:
        warn.append(u"detail {}: plan and section are {:.0f} mm high, more than the {:.0f} mm the booklet page holds "
                    u"with its legend".format(w["id"], y_pl + dh - 0.5, P24_SEC_MAX))
    sh.key, sh.world, sh.scale = w["key"], R, DT_SCALE
    pl = dict(_PLEG[0])
    sh.pleg, _PLEG[0] = pl, None
    sh.r28_leg = r28_crop_legend(pl)
    sh.bid = (w["id"], w["old"], w["caption"])
    return sh


def r28_crop_legend(keys):
    """v28 (WO-T4b-3): a window's booklet legend, only what its plan and section draw: one sample per symbol."""
    cl = _r28_base_cols()
    rows = ((("p24", "reed"), "fill", PLA_WET, u"Reed basins in lined cells"),
            (("p24", "terraces"), "fill", R28_ZONE["terraces"][1], u"Rain terraces"),
            (("p24", "terr"), "line", R28_ZONE["terraces"][1], u"Terrace edge, ticks downhill"),
            (("p24", "spill"), "fill", COL["river"], u"Spillway"),
            (("p24", "wetland"), "fill", WET_COL, u"Widened stream · wetland"),
            (("p24", "arm"), "line", COL["river"], u"Planted side arm"),
            (("p24", "subhub"), "fill", R28_ZONE["subhub"][1], u"Sub-hub in the bed"),
            (("p24", "forest"), "fill", R28_ZONE["forest"][1], u"Forest corridor"),
            (("p24", "tree"), "dot", SEC["crown"], u"Tree at its crown width"),
            (("p24", "demeter"), "fill", PLA_FIELD, u"Demeter's Garden · olive rows 7 × 5 m"),
            (("p24", "hub"), "fill", SQ_FILL, u"Hub square, paved"),
            (("p24", "cafe"), "dot", R28_ZONE["cafe"][1], u"Café"),
            (("p24", "walk"), "line", COL["ink2"], u"Riverside walk"),
            (("p24", "bike"), "line", P24_BIKE_COL, u"Bike lane"),
            (("p24", "stones"), "dot", COL["ink2"], u"Stepping stones"),
            (("p24", "foot"), "line", COL["ink_dark"], u"Footbridge deck"),
            (("p24", "road_calmed"), "line", ROAD_CHANGE_COL["calmed"], u"Street calmed"),
            (("p24", "road_pedestrian"), "line", ROAD_CHANGE_COL["pedestrian"], u"Street or bridge for walking"),
            (("p24", "road_shared"), "line", ROAD_CHANGE_COL["shared"], u"Street shared"),
            (("p24", "hidden"), "dash", COL["river_mid"], u"Hidden stream line"),
            (("p24", "view"), "dot", COL["accent"], u"Viewing terrace, sightline"),
            (("r28dt", "route"), "line", R28DT_ROUTE, u"Water route · step"),
            (("p24", "cut"), "dashdot", COL["ink_dark"], u"Section line, triangles look upstream"),
            (("p24s", "flood"), "fill", P24_FLOOD, u"Reach of Q500 (lines: Q100, Q500)"),
            (("p24s", "wall"), "fill", SCT["stone"], u"DSİ stone wall"),
            (("r28dt", "bed"), "fill", cl["bed"], u"Stream bed (survey)"),
            (("r28dt", "bld"), "fill", cl["bld"], u"Building (survey)"),
            (("r28dt", "study"), "dashdot", R28_STUDY_LINE["colour"], R28_STUDY_NAME))
    return [{"kind": kind, "colour": colour, "label": label} for key, kind, colour, label in rows if key in keys]


def leg(key, val=True):
    LEG.setdefault(key, val)
    if _PLEG[0] is not None:
        _PLEG[0].setdefault(key, val)
