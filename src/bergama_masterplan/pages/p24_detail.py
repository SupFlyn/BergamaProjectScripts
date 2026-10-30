# p.24 the detail window panel (booklet p22; T7 30 Oct: reasons, key map, trees, M5 water, sections in two styles): v28 (revision 29 Oct, WO-T4b-3) plan language + sections D1, D2 (split from parts/02_Design.py, parts/02b_detail.py, parts/02e_r28_detail.py, parts/03_make_board.py on 29 Oct 2026; moved unchanged)


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


def _r28_base(pg, C, T, R, segs, k):
    """v27 (P24.1, P24.2): the survey as a faint grey underlay: contours, buildings (heritage with a thin outline),
    street edges; the bridges crisp (the base's only dark lines, kept free of words). T7 (30 Oct, M5 / G8): the
    stream drawn by M5 over the context (water_plan: surface tone, bank line, flow streaks deeper to the middle; the
    site board's stream polygon, as p.21), its banks kept free of words; no mid-stream line."""
    cl = _r28_base_cols()
    Rm = (R[0] - 5.0, R[1] - 5.0, R[2] + 5.0, R[3] + 5.0)
    near = lambda Ls: [[T(p) for p in L_] for L_ in Ls if len(L_) >= 2 and hit(bbox(L_), Rm)]
    dw, dh = (R[2] - R[0]) * k, (R[3] - R[1]) * k
    for Q in near(C.contours):
        pg.line(Q, COL["contour10"], 0.12)
        leg(("r28dt", "contour"))
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
    box = (-2.0, -2.0, dw + 2.0, dh + 2.0)
    rings = pl23_water_draw(pg, C, T, k, lambda Q: hit(bbox(Q), box), 1.3)
    for Q in rings:
        segs += [(a, b) for a, b in zip(Q, Q[1:] + Q[:1]) if hit(bbox([a, b]), box)]
    if rings:
        leg(("r28dt", "bed"))
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
        if s and s[0] == "image":                         # T7: a cutout ("image", x, y, w, h, ...)
            ys.append(s[2] + s[4])
            continue
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
    """One section in print mm at 1:1,000 (k = 1 mm per m): x = (t - ta) k, y = (z - z0) k. T7 (30 Oct, M5 / G8):
    everything goes into ONE WaterLayers draw list (atmosphere, background, ground, bed, water, structures,
    vegetation, figures, labels) and is put on the page once (draw), so the layer order is fixed; style "a" / "b"
    (D1) draws the plants and people as cutouts or vectors from the same geometry."""

    def __init__(self, ta, tb, z0, style="b"):
        self.ta, self.tb, self.z0, self.k = ta, tb, z0, 1000.0 / DT_SCALE
        self.w = (tb - ta) * self.k
        self.pg = Page(self.w, 0.0)
        self.wl = water_layers()
        self.style = style
        self.shapes = []                                 # every shape added (for the top)
        self.trees = []                                  # (key, h_m) drawn at layer 0 (G6 check)
        self.zl = []                                     # zone lines: (name, t, z of the ground, beyond)
        self.lv = []                                     # level words: (text, t, z)

    def X(self, t):
        return (t - self.ta) * self.k

    def Y(self, z):
        return (z - self.z0) * self.k

    def put(self, shapes, layer="structures"):
        self.wl.add(layer, shapes)
        self.shapes += list(shapes or [])

    def plant(self, key, t, z, layer=0, seed=0, into="vegetation", **kw):
        self.put(pla_section(key, self.X(t), self.Y(z), self.k, seed=seed, style=self.style, layer=layer, **kw), into)
        if not layer:
            self.trees.append((key, kw.get("h_m") or PLA_SPECIES[key]["h_m"]))

    def scatter(self, t0, t1, prof, b0, b1, mix, seed, density=1.0):
        """a mixed planting from t0 to t1 on the ground, band position b0 at t0 to b1 at t1 (M6, no rows)"""
        sh, placed = pla_scatter_section(self.X(t0), self.X(t1), lambda x: self.Y(_p24_zat(prof, x / self.k + self.ta)),
                                         self.k, t0=b0, t1=b1, mix=mix, seed=seed, style=self.style, density=density)
        self.put(sh, "vegetation")
        self.trees += [(key, h) for key, x, h, cr in placed]

    def fig(self, pose, t, z, facing=1, **kw):
        self.put(fig_side(pose, self.X(t), self.Y(z), self.k, facing=facing, mm_per_m=self.k, style=self.style, **kw),
                 "figures")

    def people(self, zone, t0, t1, z, seed=0, **kw):
        """people doing what the zone is for (M7 fig_activity), on flat ground z from t0 to t1"""
        if t1 - t0 < 1.0:
            return
        sh, _ = fig_activity(zone, self.X(t0), self.X(t1), self.Y(z), self.k, seed=seed, style=self.style, **kw)
        self.put(sh, "figures")

    def block(self, t0, t1, z0, z1, material):
        a, b = sorted((t0, t1))
        self.put(sct_hatch_fill([(self.X(a), self.Y(z0)), (self.X(b), self.Y(z0)), (self.X(b), self.Y(z1)),
                                 (self.X(a), self.Y(z1))], material, self.k, SCT["cut"], 0.2))

    def lane(self, t0, t1, z, kind):
        """M8 sf_lane: a path's surface and build-up from t0 to t1 at level z (walk, bike, road, gravel)"""
        a, b = sorted((t0, t1))
        self.put(sf_lane(self.X(a), self.Y(z), b - a, self.k, kind=kind))

    def draw(self):
        self.wl.put(self.pg)


P24_BACK_M = (140.0, 60.0)   # T7: ground lines this far behind the cut (view direction), from the survey: the context
P24_ARM_M = 60.0             # T7: trees of the corridor this far behind the cut stand in depth layer 1, farther in 2
P24_BACK_GAP = 6.0           # T7: trees behind the cut at least this far apart along it per depth layer, m (legible)


def p24_section(C, w, warn, style="b"):
    """v28 (WO-T4b-3): the section under window w (P24_CUTS), as (Page, w mm, h mm, legend keys, words not placed);
    None when the window has no cut. Looks upstream: the SW bank on the left, as the plan reads it. T7 (30 Oct,
    booklet p22, G8 / G10 / D1 / D9): one geometry, two styles ("b" vector, "a" cutouts); the levels from the cut
    registry (W1, W3: bed, average flow, Q100, Q500, wall tops; never typed); the water in the bed at the average
    yearly flow with Q100 / Q500 (M5 water_section); the ground behind the cut from the survey (context); the
    corridor's trees from the plan's tree set (layer 0 at the cut, 1 and 2 behind, D9); every zone with its paths
    (walk, bike lane, street: M8 sf_lane), its planting (M6, mixed, no rows) and people doing what it is for (M7,
    adults 1.75 m); the G6 check logged."""
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
    reg = level_registry(cid)
    bed, hw = reg["bed"], reg["bed_width_cm"] / 200.0
    q100, q500, avg = reg["q100"], reg["q500"], reg["avg_flow"]
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
    lane_w = WALK_W + (P24_BIKE_W if P24_BIKE else 0.0)
    for P in C.canopy:
        for t in _p24_crossings(c0, cd, P, ta + 2.0, tb - 2.0):
            if abs(t) > hw + 1.0:
                sg = 1.0 if t > 0 else -1.0               # the bike lane on the land side of the walk
                zw = _p24_zat(prof, t)
                a_, b_ = sorted((t - sg * WALK_W / 2.0, t - sg * WALK_W / 2.0 + sg * lane_w))
                _p24_set(prof, a_, b_, lambda t_, z, zw=zw: zw, hw)
                walks.append((t, zw, sg))
    cells = []
    kt = 0.15
    ln, gap, dep, media, wl_ = P24_BASIN
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
    S = P24Sec(ta, tb, z0, style)
    X, Y, k = S.X, S.Y, S.k
    zat = lambda t: _p24_zat(prof, t)
    # ---- context: the ground behind the cut (survey heights on lines parallel to it, farthest first), the corridor's
    # trees behind the cut in depth layers 1 and 2 (D9), on the background behind the cut ground
    backs = []
    for d in P24_BACK_M:
        g = [(t, z) for t, z in p24_ground(C, (c0[0] + f[0] * d, c0[1] + f[1] * d), cd, ta, tb) if ta <= t <= tb]
        if len(g) >= 2:
            backs.append([(X(t), Y(z)) for t, z in g])
    if backs:
        sf_topo_back(backs, Y(z0), into=S.wl)
        keys.add("back")
    near0, back = [], []
    for i, (p, key, cr) in enumerate(pl23_tree_set(C)):
        t, d = _p24_tz(c0, cd, f, p)
        if not (ta + 2.0 <= t <= tb - 2.0) or abs(t) <= hw + 1.0:
            continue
        if abs(d) <= P24_TREE_M:
            near0.append((t, key, cr, i))
        elif 0.0 < d <= P24_BEYOND_M:
            back.append((d, t, key, cr, i))
    shown = {1: [], 2: []}
    for d, t, key, cr, i in sorted(back):                 # behind the cut: the nearest first, one per P24_BACK_GAP m
        ly = 1 if d <= P24_ARM_M else 2
        if all(abs(t - t_) >= P24_BACK_GAP for t_ in shown[ly]):
            shown[ly].append(t)
            S.plant(key, t, zat(t), layer=ly, seed=300 + i, into="background", crown_m=cr, detail=False)
            keys.add("forest")
    # ---- the cut ground (survey, one hatch), then the channel by M5: the bed, the water at the average yearly flow,
    # Q100 and Q500 with their level words; where a flood level overtops the channel its line runs on over the land it
    # reaches (filled for Q500: the reach of Q500 where it joins the stream)
    S.put(sct_ground([(X(p[0]), Y(p[1])) for p in prof], 0.0, k), "ground")

    def reach(lev):
        lo_, hi_ = 0.0, 0.0
        while lo_ > ta and zat(lo_ - P24_STEP_M) < lev:
            lo_ -= P24_STEP_M
        while hi_ < tb and zat(hi_ + P24_STEP_M) < lev:
            hi_ += P24_STEP_M
        return lo_, hi_
    lo_, hi_ = reach(q500)
    if hi_ > lo_:
        n_ = int((hi_ - lo_) / P24_STEP_M)
        ring_ = [(X(lo_), Y(q500))] + [(X(lo_ + i * P24_STEP_M), Y(zat(lo_ + i * P24_STEP_M))) for i in range(n_ + 1)] + \
            [(X(hi_), Y(q500))]
        S.put([("poly", ring_, P24_FLOOD, None, 0.1, P24_FLOOD_A)], "bed")
        keys.add("flood")
    ch = [p for p in prof if abs(p[0]) <= hw + P24_WALL_T + 2.0]
    water_section([(X(p[0]), Y(p[1])) for p in ch], k, Y, cid=cid, fill_ground=False, labels=True,
                  label_size=KEY_MIN, style=style, into=S.wl)
    pal = _wat_pal()
    for lev, key, dash in ((q100, "q100", [1.2, 0.6]), (q500, "q500", [0.4, 0.5])):
        lo_, hi_ = reach(lev)
        for a_, b_ in ((lo_, ch[0][0]), (ch[-1][0], hi_)):
            if b_ - a_ > 0.2:
                S.put([("line", [(X(a_), Y(lev)), (X(b_), Y(lev))], pal[key], 0.25, dash)], "water")
    keys.add("avg")
    S.lv.append((u"bed " + u_level(bed), 0.0, bed))
    for side, sg in (("SW", -1.0), ("NE", 1.0)):         # DSİ walls kept (stone, railing) or given way (dashed)
        if kinds[side] != "dsi_wall":
            continue
        a, b = sg * hw, sg * (hw + P24_WALL_T)
        ring_ = [(X(a), Y(bed)), (X(b), Y(bed)), (X(b), Y(tops[side])), (X(a), Y(tops[side]))]
        if side in gone:
            S.put([("line", ring_ + ring_[:1], COL["ink2"], 0.15, [0.8, 0.5])])
            continue
        S.block(a, b, bed, tops[side], "stone")
        S.put(sct_bank("railing", X((a + b) / 2.0), Y(tops[side]), Y(bed), -sg, k, h_m=P24_RAIL_H)[0])
        S.lv.append((u_level(tops[side]), b, tops[side] + P24_RAIL_H))
        keys.add("wall")
    railed = False
    for side, sg in (("SW", -1.0), ("NE", 1.0)):         # one figure at a railing, looking into the channel
        if kinds[side] == "dsi_wall" and side not in gone and not railed:
            fc = 1 if sg < 0 else -1
            m_ = fig_meta("railing", facing=fc, rail_h=P24_RAIL_H)
            S.fig("railing", sg * (hw + P24_WALL_T / 2.0) - m_.get("rail_x", 0.0), tops[side], facing=fc,
                  rail_h=P24_RAIL_H)
            railed = True
    # ---- the sub-hub in the bed (zone WA, bed tier) where the cut crosses it: people in the water at average flow
    sub = any(p24_zone(C, (c0[0] + cd[0] * u, c0[1] + cd[1] * u)) == "subhub"
              for u in [-hw + (i + 0.5) * (2.0 * hw) / 8.0 for i in range(8)])
    if sub:
        S.people("bed", -hw + 0.6, hw - 0.6, bed, seed=11, water=Y(avg))
        S.zl.append((P24_NAME["subhub"], 0.0, bed, False))
    # ---- the corridor's trees at the cut (the plan's tree set, layer 0)
    for t, key, cr, i in near0:
        S.plant(key, t, zat(t), seed=i, crown_m=cr)
        keys.add("forest")
    # ---- what each zone holds: its ground, paths, planting and people (G10)
    for key, t0, t1 in runs:
        ln_, tm = t1 - t0, (t0 + t1) / 2.0
        fc = 1 if tm < 0 else -1                          # people face the stream
        if key == "hub":
            zf = zat(tm)
            S.block(t0, t1, zf - P24_PAVE_T, zf, "stone")
            hub_t = [t for h in C.hubs for t, d in [_p24_tz(c0, cd, f, p) for p in h.get("trees") or []]
                     if abs(d) <= P24_TREE_M and t0 <= t <= t1]
            for j, t in enumerate(hub_t):
                S.plant("plane", t, zf, seed=70 + j)
            S.people("walkway", t0 + 0.5, t1 - 0.5, zf, seed=21)
            S.lv.append((u_level(zf), tm, zf))
        elif key == "street":
            zf = zat(tm)
            S.lane(t0, t1, zf, "road")
            keys.add("lane")
        elif key == "demeter":
            ts_ = sorted((t0, t1), key=abs)
            te = ts_[0]                                   # the garden's stream-side edge: a stone wall
            sg = 1.0 if te > tm else -1.0
            S.block(te, te - sg * P24_WALL_DG, gf - 1.0, gf + 0.15, "stone")
            x0_, x1_ = X(min(t0, t1) + 1.5), X(max(t0, t1) - 1.5)
            if x1_ > x0_:
                S.put(pla_crop_rows("olive", x0_, x1_, Y(gf), k), "vegetation")
                n_ = int((x1_ - x0_) / (PLA_CROPS["olive"]["row_m"] * k) + 1e-9)
                t_o = min(t0, t1) + 1.5 + ((x1_ - x0_) - n_ * PLA_CROPS["olive"]["row_m"] * k) / 2.0 / k
                S.fig("olive", t_o + 1.3, gf, facing=-1)
            S.plant("lavender", te - sg * 1.2, gf, seed=81)
            S.lv.append((u_level(gf), tm, gf))
        elif key == "wetland" and abs(tm) > hw:
            te = min((t0, t1), key=abs)                   # the water's side of the bench
            b0, b1 = (0.0, 0.45) if te == t0 else (0.45, 0.0)
            S.scatter(t0, t1, prof, b0, b1, ("soft_rush", "loosestrife", "willow", "tamarisk"), seed=90, density=0.9)
            sg = 1.0 if tm > 0 else -1.0
            if ln_ >= 8.0:
                S.fig("watch", te + sg * 3.0, zat(te + sg * 3.0), facing=-1 if sg > 0 else 1)
        elif key == "terraces":
            S.scatter(t0, t1, prof, 0.86, 0.94, ("lavender",), seed=100, density=0.8)
            S.people("walkway", t0 + 1.0, t1 - 1.0, zat(tm), seed=31, density=0.5, max_n=2)
        elif key == "bld":
            zf = zat(tm)
            S.put([("line", [(X(t0), Y(zf) + 0.4), (X(t1), Y(zf) + 0.4)], COL["bld"], 0.8)])
    for a, b, rim in cells:                               # the lined reed cells (D2 a), above Q500 by their rim
        fl = rim - P24_BASIN[2]
        S.put(pla_reed_basin(X(a), X(b), Y(fl), Y(rim), k, P24_KERB_H, media_m=P24_BASIN[3],
                             wl_y=Y(fl + P24_BASIN[4])), "vegetation")
        keys.add("reed")
    if cells:
        a, b, rim = cells[0]
        S.fig("touch", a - 0.7, rim, facing=1)            # the clean-water classroom: a hand into the cell
        S.lv.append((u_level(cells[0][2]), (cells[0][0] + cells[-1][1]) / 2.0, cells[0][2]))
    for t, te, z0_, zt, sg in terr:                       # each terrace's riser, where the old ground stood higher
        if zt > z0_ + 0.05:
            S.block(te, te + sg * 0.15, z0_ - 0.3, zt, "concrete")
        keys.add("terraces")
    for j, (t, zw, sg) in enumerate(walks):               # the riverside walk, its bike lane on the land side
        wa, wb = t - sg * WALK_W / 2.0, t + sg * WALK_W / 2.0
        S.lane(wa, wb, zw, "walk")
        S.people("walkway", min(wa, wb) + 0.2, max(wa, wb) - 0.2, zw, seed=41 + j, max_n=2)
        if P24_BIKE:
            S.lane(wb, wb + sg * P24_BIKE_W, zw, "bike")
            S.people("bike_lane", min(wb, wb + sg * P24_BIKE_W), max(wb, wb + sg * P24_BIKE_W), zw, seed=51 + j,
                     max_n=1)
        S.zl.append((P24_NAME["walk"], t, zw, False))
        keys.add("walk")
        keys.add("lane")
    # ---- zone lines: one per run (bed = the stream), then what stands beyond the cut, paler (D9 layer 1)
    for key, t0, t1 in runs:
        if key in P24_NAME and (t1 - t0 >= P24_MIN_RUN or key == "bed") and key != "walk":
            tm = (t0 + t1) / 2.0
            S.zl.append((P24_NAME[key], tm, zat(tm), False))
    crossed = set(r_[0] for r_ in runs)
    seen = set()
    for z in C.D.zones:
        key = P24_KEY.get((z["code"], z.get("tier") if z["code"] == "WA" else None))
        if not key or key in crossed or key in seen or not z.get("P") or (key == "subhub" and sub):
            continue
        q = inner_pt(z["P"])
        t, d = _p24_tz(c0, cd, f, q)
        if 0.0 < d <= P24_BEYOND_M and ta + 3.0 <= t <= tb - 3.0 and R[0] <= q[0] <= R[2] and R[1] <= q[1] <= R[3]:
            seen.add(key)
            zz = zat(t)
            sp_ = {"demeter": "olive", "terraces": "lavender"}
            if key in sp_:
                S.plant(sp_[key], t, zz, layer=1, seed=120 + len(seen), into="background")
            S.zl.append((P24_NAME[key], t, zz, True))
    for c_ in C.cross:                                    # footbridges and stepping stones beyond
        if not c_.get("P"):                               # v30.1: kept bridges have only "xy"
            continue
        ts_ = [_p24_tz(c0, cd, f, p) for p in c_["P"]]
        if not all(0.0 < d <= P24_BEYOND_M for _, d in ts_):
            continue
        t1_, t2_ = sorted(t for t, _ in ts_)
        if t2_ < ta or t1_ > tb:
            continue
        t1_, t2_ = max(ta, t1_), min(tb, t2_)
        pale = fig_fade(COL["ink2"], 1)
        if c_["kind"] == "footbridge":
            zd = max(zat(t1_), zat(t2_))
            S.put([("line", [(X(t1_), Y(zd)), (X(t2_), Y(zd))], pale, 0.6)], "background")
            S.zl.append((P24_NAME["foot"], (t1_ + t2_) / 2.0, zd, True))
        elif c_["kind"] == "stepping stones":
            t = max(t1_, -hw) + P24_STONE[1] / 2.0
            while t < min(t2_, hw):
                S.put([("poly", sec_ellipse(X(t), Y(bed) + P24_STONE[0] * k, P24_STONE[0] * k, P24_STONE[0] * k, 12),
                        pale, None, 0.1)], "structures")
                t += P24_STONE[1]
            S.zl.append((P24_NAME["stones"], 0.0, bed, True))
    if C.terrace:
        t, d = _p24_tz(c0, cd, f, C.terrace["xy"])
        if 0.0 < d <= P24_BEYOND_M and ta + 3.0 <= t <= tb - 3.0:
            zz = zat(t)
            S.put([("line", [(X(t - 2.0), Y(zz + 0.3)), (X(t + 2.0), Y(zz + 0.3))], fig_fade(COL["ink2"], 1), 0.5)],
                  "background")
            S.zl.append((P24_NAME["view"], t, zz, True))
    S.draw()
    bad = sf_assert_g6(k, trees=S.trees, strict=False)   # G6: people 1.75 m, every tree in its sourced height range
    if bad and style == "b":
        warn.append(u"section {}: {}".format(name, u"; ".join(bad)))
    # ---- words: the zone lines and names in rows above everything (R18 idea), the levels by their points
    top = max([_p24_top(S.shapes) or 0.0] + [Y(p[1]) for p in prof] + [Y(q500) + 2.0 * KEY_MIN]) + 2.0
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
    an = S.wl.anchors                                     # M5's level words at the right end of Q500 / Q100 / avg
    if an:
        xs_, ys_ = [p[0] for p in an.values()], [p[1] for p in an.values()]
        taken.append((min(xs_), min(ys_) - 3.5 * KEY_MIN, max(xs_) + 1.2 * KEY_MIN + text_w(u"average flow +00.00",
                                                                                               KEY_MIN) + 1.0,
                      max(ys_) + 1.2 * KEY_MIN))
    for s_, t, al in ((name, ta, "L"), (name + u"'", tb, "R")):   # the cut's names, as on the plan
        x, y = X(t) + (0.6 if al == "L" else -0.6), Y(zat(t)) + 1.2
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
    texture at true size; returns [(field key, page rings)] for the titles. T7 (30 Oct, M5): ground fields, then the
    paths and crossings, then the trees over them (one tree set with p.21, pl23_tree_set)."""
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
    # ---- terrace edges: a line with ticks down toward the stream
    for P in C.terr:
        Q = TP(P)
        if on(Q):
            ticks_line(pg, Q, R28_ZONE["terraces"][1], 0.3, 1.6, 0.8, 1.0, alpha=0.9)
            segs += list(zip(Q, Q[1:]))
            leg(("p24", "terr"))
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
        if not c_.get("P"):                               # v30.1: kept bridges have only "xy"
            continue
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
    # ---- vegetation over the ground, water and paths (M5 order; G9): the corridor's tree set as on p.21 (groves
    # and clearings, species by their band from the water, each at its crown width with its own plan mark; no
    # identical clusters), the hub squares' planes
    if pl23_trees_draw(pg, C, T, k, (-8.0, -8.0, dw + 8.0, dh + 8.0)):
        leg(("p24", "tree"))
    for h in C.hubs:
        for i, p in enumerate(h.get("trees") or []):
            if inP(p):
                x, y = T(p)
                _p24_put(pg, pla_plan("plane", x, y, k, seed=i), alpha=0.85)
                leg(("p24", "tree"))
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


# ---- T7 (30 Oct, booklet p22): a reason for every element (G10) and the page's key map (M4) ---------------------
P24_KEYMAP_IN = "dt_k5"      # the window whose plan carries the page's key map (drawn last: it knows both windows)
P24_KM_W, P24_KM_HMAX = 58.0, 36.0   # mm: the key map inset at most this wide / high
_P24_WINS = {}               # window id -> (section name, window R survey m), filled as the windows are drawn


def p24_reason(C, key, w):
    """T7 (G10): why this element is where it is, one line, from the masterplan's own data: the moves' reasons
    (Corridor.notes), the zone base's purposes (LEG_ZONE), the corridor's rules (FOREST, TERRACE_UP, open ground beside
    the bank) and the cut registry; None where the data gives no reason (left out, never invented)."""
    R = w["R"]
    inR = lambda p: R[0] <= p[0] <= R[2] and R[1] <= p[1] <= R[3]
    cid = P24_CUTS.get(w["id"], (None,))[0]
    if key == "reed":
        return u"the water is cleaned once before it goes back · a clean-water classroom"
    if key == "terraces":
        return u"they hold the rain on the slope · overflow to the reed basins"
    if key == "spill":
        return u"gives the cleaned water back to the stream"
    if key == "forest":
        return u"shade on the walk between the hubs · {:.0f}-{:.0f} m from the water".format(FOREST[0], FOREST[1])
    if key == "wetland":
        ws = [x for x in C.widen if any(inR(p) for p in x["ring"])]
        if ws:
            lo, hi = min(x["fw"][0] for x in ws), max(x["fw"][1] for x in ws)
            return u"{:.0f}-{:.0f} m open beside the bank: room for the water, a wetland".format(lo, hi)
        return u"it floods first: a terrace {:.2f} m over the bed".format(TERRACE_UP)
    if key == "demeter":
        q = (u"raised over Q500 {}: Q500 stays in the banks here".format(u_level(level_registry(cid)["q500"]))
             if cid else u"Q500 stays in the banks at the K5 cut")
        return q + u" · café"
    if key == "subhub":
        return u"a place in the bed for the dry months · shut in floods"
    if key == "hub":
        return u"a dry square at the bridge · plane shade"
    return None


def p24_keymap(pg, dw, dh, fields, taken, warn):
    """T7 (M4): the key map inset in the plan's emptiest corner: the study-area outline, both windows (D1, D2) and
    their registry cuts (W1, W3), labelled; its box joins taken. Returns True when drawn."""
    zooms = dict((nm, rect(R_[0], R_[1], R_[2], R_[3])) for nm, R_ in _P24_WINS.values())
    ids = [P24_CUTS[b][0] for b in sorted(_P24_WINS) if b in P24_CUTS]
    try:
        km = keymap_items(ids=ids, zooms=zooms, mode="key", text_mm=KEY_MIN)
    except Exception as ex:
        warn.append(u"p.22 key map not drawn ({}: {})".format(type(ex).__name__, ex))
        return False
    box = km.get("box")
    if not box or not km.get("items"):
        warn.append(u"p.22 key map not drawn: no base map data (run the site board first)")
        return False
    for m_ in km.get("missing") or []:
        warn.append(u"p.22 key map: {} not drawn".format(m_))
    bw, bh = max(1.0, box[2] - box[0]), max(1.0, box[3] - box[1])
    s = min((P24_KM_W - 2.0) / bw, (P24_KM_HMAX - 2.0 - KEY_MIN * 1.6) / bh)
    try:                                                  # again at the inset's own scale (its labels' offsets)
        km = keymap_items(ids=ids, zooms=zooms, mode="key", text_mm=KEY_MIN, box=box, scale_den=1000.0 / s)
    except Exception:
        pass
    iw, ih = bw * s + 2.0, bh * s + 2.0 + KEY_MIN * 1.6
    cands = [(dw - iw - 1.0, dh - ih - 1.0), (1.0, dh - ih - 1.0), (dw - iw - 1.0, 1.0), (1.0, 1.0)]
    score = lambda c: sum(1 for _, Q in fields for p in Q if c[0] <= p[0] <= c[0] + iw and c[1] <= p[1] <= c[1] + ih)
    x0, y0 = min(cands, key=score)
    pg.poly([rect(x0, y0, x0 + iw, y0 + ih)], fill=COL["white"], stroke=COL["ink2"], lw=0.2)
    pg.text(u"Key map · D1, D2 in the study area", x0 + 1.0, y0 + ih - KEY_MIN * 1.25, KEY_MIN, COL["ink_dark"],
            bold=True)
    ox, oy = x0 + 1.0, y0 + 1.0
    Tk = lambda p: (ox + (p[0] - box[0]) * s, oy + (p[1] - box[1]) * s)
    op = lambda a: a if a is not None and a < 0.995 else None

    def fill_fn(rings, hx, al, nonzero=False):
        pg.poly([R_ for R_ in rings if len(R_) >= 3], fill=hx, alpha=op(al))

    def line_fn(pts, hx, lw, dash, al):
        pg.line(pts, hx, lw, list(dash) if dash else None, cap=0 if dash else 1, alpha=op(al))

    def text_fn(t_, xy, size, hx, bold, align):
        al = align[-1] if align and align[-1] in "LCR" else "L"
        dy = -0.36 * size if align and align[0] == "M" else (-size if align and align[0] == "T" else 0.0)
        pg.text(t_, xy[0], xy[1] + dy, size, hx, bold=bold, align=al, halo=COL["white"])
    pg.clip([rect(ox, oy, ox + bw * s, oy + bh * s)])
    basemap_draw(km["items"], Tk, fill_fn, line_fn, text_fn)
    pg.unclip()
    taken.append((x0, y0, x0 + iw, y0 + ih))
    return True


def r28_window_panel(C, w, areas, missing, warn):
    """v28 (revision 29 Oct, WO-T4b-3; package H "Page 24"): a 1:1,000 window, north up: the faint survey, the
    proposal in the architectural plan language (p24_plan), the water route 1-4, the study area, the section line
    (this window's only); one title per field, place names, small words. Under it its section (p24_section, D1 or
    D2) at the same scale. One crop: the plan with its north arrow and scale bar, the section with its own.
    T7 (30 Oct, booklet p22): each field title carries its reason (p24_reason, G10); the K5 window carries the key
    map of both windows (p24_keymap, M4); the section is drawn in both D1 styles and the panel holds both crops
    (sh.crops_more: <id>_b, <id>_a; <id> itself = style b), on the 4 mm baseline grid (M1)."""
    R = w["R"]
    k = 1000.0 / DT_SCALE
    dw, dh = (R[2] - R[0]) * k, (R[3] - R[1]) * k
    T = lambda p: ((p[0] - R[0]) * k, (p[1] - R[1]) * k)
    inP = lambda p: R[0] <= p[0] <= R[2] and R[1] <= p[1] <= R[3]
    on = lambda Q: hit(bbox(Q), (0.0, 0.0, dw, dh))
    _PLEG[0] = {}
    if w["id"] == DT_WINDOWS[0][0]:                       # a new run: the first window starts the key map's list
        _P24_WINS.clear()
    _P24_WINS[w["id"]] = (P24_CUTS.get(w["id"], (None, w["id"]))[1], R)
    pg = Page(dw, dh)
    taken, segs, ts = [], [], R28DT_TS
    ink, ink1, ink2, white = COL["ink_dark"], COL["ink"], COL["ink2"], COL["white"]
    bounds = (1.0, 1.0, dw - 1.0, dh - 1.0)
    _r28_base(pg, C, T, R, segs, k)
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
    if w["id"] == P24_KEYMAP_IN and p24_keymap(pg, dw, dh, fields, taken, warn):   # T7 (M4): before the words
        leg(("p24", "keymap"))
    # ---- words (G4): place names, one title per field inside it (T7, G10: its reason, then its species in small
    # grey), the route key, then the small words (dropped where there is no room)
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
        rs = p24_reason(C, key, w)
        why = [(s_, ts["small"], False, ink1) for s_ in wrap(rs, ts["small"], 56.0)] if rs else []
        sub = [(_p24_sp(s_) + (u" · lined cells" if s_ == "reed" else u""), ts["small"], False, ink2)
               for s_ in P24_SPECIES.get(key, ())]
        vs = ([title + why + sub] if sub else []) + ([title + why] if why else []) + [title]
        if key in best:
            ok = _r28_title(pg, best[key], vs, taken, segs, bounds)
        else:                                             # the forest corridor is trees, not a field: by its middle tree
            fp = sorted(fpts)[len(fpts) // 2]
            ok = None
            for v_ in vs:
                ok = _r28_label(pg, v_, fp, taken, segs, bounds, rank=1)
                if ok:
                    break
        if not ok:
            missing.append(nm)
        elif why and ok[3] - ok[1] < _r28_wh(title + why)[1] - 1e-6:
            missing.append(nm + u" · its reason (no room)")
    if key_lines:                                        # the route key (P24.2, G5): numbered dot, the step's words
        pitch, rr = 3.6, 1.5
        w_ = max([2 * rr + 1.2 + sum(text_w(t_, ts["label"], bd) for t_, bd in runs) for _, runs in key_lines] +
                 [text_w(u"Water route · collect, clean, give back", ts["label"], True)])
        h_ = ts["label"] * 1.18 + 0.4 + pitch * len(key_lines)
        anc = (sum(p[0] for _, p in dots) / len(dots), sum(p[1] for _, p in dots) / len(dots)) if dots else \
            (dw / 2.0, dh / 2.0)
        got = _r28_spot(w_, h_, anc, taken, segs, bounds)
        if got:
            b = got[0]
            taken.append(b)
            y = b[3] - ts["label"]
            pg.text(u"Water route · collect, clean, give back", b[0], y, ts["label"], ink, bold=True)
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
    # ---- the panel (T7, M1): every block a whole number of 4 mm baseline rows, the section left-aligned with its
    # plan. One unit per style (D1): the plan with its north arrow and scale bar, under it its section with its own
    # scale bar row; style b on top (crop <id> and <id>_b), style a under it (crop <id>_a: the same geometry with
    # cutouts). The plan (and its key map) is the same drawing in both.
    M = 12.0
    units = []
    for st in ("b", "a"):
        sec = p24_section(C, w, warn if st == "b" else [], st)
        if sec is None:
            break
        units.append((st, sec))
        if st == "b":
            missing += sec[4]
        for k_ in sec[3]:
            leg(("p24s", k_))
    units = units or [("b", None)]
    SCALE_ROW, MARK_ROW, TITLE_ROW, GAP = 2 * GRID_BASE, 3 * GRID_BASE, 3 * GRID_BASE, 4 * GRID_BASE
    hs = [((SCALE_ROW + grid_snap_h(sec[2])) if sec else 0.0) + MARK_ROW + dh for st, sec in units]
    W = M + dw + M
    H = 1.0 + sum(hs) + TITLE_ROW * len(units) + GAP * (len(units) - 1)
    sh = Page(W, H)
    sh.poly([rect(0, 0, W, H)], fill=COL["paper"])
    cid, nm = P24_CUTS.get(w["id"], (None, None))
    crops, y = {}, 1.0
    for st, sec in reversed(units):                       # style a at the bottom, style b on top
        y0 = y
        if sec:
            spg, sw_, shh = sec[0], sec[1], sec[2]
            scale_bar(sh, M, y + 1.5, DT_SCALE, (0.0, 10.0, 20.0, 50.0))
            sh.text(u"Section {0} {0}' on cut {1} · every zone of the plan above, looking upstream".format(
                nm, level_name(cid)), M + 72.0, y + 1.7, ts["label"], COL["ink_dark"], bold=True)
            y += SCALE_ROW
            blit(sh, spg, M, y)                           # images (style a) stay outside every clip
            y += grid_snap_h(shh)
        panel_marks(sh, M, y, DT_SCALE, (0.0, 10.0, 20.0, 50.0))
        y += MARK_ROW
        sh.clip([rect(M, y, M + dw, y + dh)])
        blit(sh, pg, M, y)
        sh.unclip()
        y += dh
        sh.text(w["title"] + u" · 1:1,000" + (u" · style a (cutouts)" if st == "a" else u""), M, y + 5.0, 5.0,
                COL["ink_dark"], bold=True)
        crops[st] = (M, y0 - 0.5 if y0 > 1.0 else 0.5, M + dw, y)
        y += TITLE_ROW + GAP
    sh.crop = crops["b"]
    sh.crops_more = [(w["id"] + u"_" + st, crops[st]) for st in ("b", "a") if st in crops]   # request: the lead's
    # make_board / booklet_crops write these as extra crops (the crop itself = style b, for older readers)
    hb = crops["b"][3] - crops["b"][1]
    if hb > P24_SEC_MAX:
        warn.append(u"detail {}: plan and section are {:.0f} mm high, more than the {:.0f} mm the booklet page holds "
                    u"with its legend".format(w["id"], hb, P24_SEC_MAX))
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
            (("p24", "tree"), "dot", SEC["crown"], u"Trees at crown width: willow, tamarisk by the water; ash, plane above"),
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
            (("p24s", "avg"), "fill", _wat_pal()["sec"], u"Water at the average yearly flow"),
            (("p24s", "flood"), "fill", P24_FLOOD, u"Reach of Q500 (lines: Q100, Q500)"),
            (("p24s", "lane"), "fill", SF_LANE["walk"], u"Walk, bike lane, street in section"),
            (("p24s", "back"), "fill", _sec_mix(SEC["soil"], SEC["paper"], 0.6), u"Ground behind the cut (survey)"),
            (("p24s", "wall"), "fill", SCT["stone"], u"DSİ stone wall"),
            (("r28dt", "bed"), "fill", _wat_pal()["surface"], u"Selinos stream (darker = deeper)"),
            (("r28dt", "bld"), "fill", cl["bld"], u"Building (survey)"),
            (("r28dt", "study"), "dashdot", R28_STUDY_LINE["colour"], R28_STUDY_NAME))
    return [{"kind": kind, "colour": colour, "label": label} for key, kind, colour, label in rows if key in keys]


def leg(key, val=True):
    LEG.setdefault(key, val)
    if _PLEG[0] is not None:
        _PLEG[0].setdefault(key, val)
