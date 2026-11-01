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
    """v27 (P24.1, P24.2): the stream drawn by M5 (water_plan: surface tone, bank line, flow streaks deeper to the
    middle; the site board's stream polygon, as p.21), its banks kept free of words; the bridges crisp. v38 (round 4,
    G-R4-4): the houses, streets and contours come from the shared muted base (ml_base, drawn first by mp_map_draw in
    r28_window_panel); this is the page's "proj_water" step. R = the window's bounding box (survey m)."""
    Rm = (R[0] - 5.0, R[1] - 5.0, R[2] + 5.0, R[3] + 5.0)
    near = lambda Ls: [[T(p) for p in L_] for L_ in Ls if len(L_) >= 2 and hit(bbox(L_), Rm)]
    box = (-2.0, -2.0, pg.W + 2.0, pg.H + 2.0)
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
    pg.tgroup()                                           # v38: one block = one text group
    for s, sz, bd, col in lines:
        y -= sz
        if centre:
            pg.text(s, (b[0] + b[2]) / 2.0, y, sz, col, bold=bd, align="C")
        else:
            pg.text(s, b[0], y, sz, col, bold=bd)
        y -= sz * 0.18
    pg.tgroup(False)


def _r28_free(b, taken, segs, bounds, pad):
    if not (bounds[0] <= b[0] and b[2] <= bounds[2] and bounds[1] <= b[1] and b[3] <= bounds[3]):
        return False
    return not any(lp_hit(b, t, pad) for t in taken) and not any(_lp_seg_box(p, q, b) for p, q in segs)


def _r28_spot(w, h, anchor, taken, segs, bounds, rank=0):
    """G4 (common/label_place): a free w x h box by anchor, (box, leader) or None; rank 0 always finds one."""
    got = place_labels_all([{"x": anchor[0], "y": anchor[1], "wh": lambda f: (w, h), "rank": rank}], taken, bounds,
                           segs, sizes=(1.0,), pad=0.5)
    return got[0][:2] if 0 in got else None


def _r28_label(pg, lines, anchor, taken, segs, bounds, rank=0):
    """A word block on or right next to its anchor (v37, round 3 G3: no leader lines; a block that would have to
    move off its anchor is not drawn: None, the caller logs it); its box or None."""
    w, h = _r28_wh(lines)
    got = label_spot(anchor[0], anchor[1], w, h, taken, bounds, LpSegIndex(segs=segs) if segs else (), 0.5,
                     rings=LP_NEAR_RINGS)
    if not got:
        return None
    b = got[0]
    _r28_text(pg, lines, b)
    taken.append(b)
    _P24_LAB.append(b)
    return b


_P24_LAB = []                # v37: the word boxes of the window being drawn (FLAG overlap p22)


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
                _P24_LAB.append(b)
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
P24_BELOW_M = 6.0            # cut ground drawn this far under the lowest point, m (v36: 3.0 -> 6.0, room for the
#                              callout circles in the cut ground under the bed)
P24_STEP_M = 0.5             # the section's sampling step, m
P24_MIN_RUN = 4.0            # zone runs shorter than this get no zone line, m
P24_TREE_M = 6.0             # forest and street trees this far from the cut line stand in the section, m
P24_BIKE = True              # the riverside walk carries a bike lane (Aras 29 Oct 21:04, decision card)
P24_BIKE_W = 2.0             # bike lane beside the walk in plan, m: drawing value
P24_STONE = (0.40, 1.20)     # stepping stone radius and spacing, m: drawing values
P24_LAB_ROWS = 4             # rows of zone names above a section
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
# v36 (R2-M left items, checklist 5 + 8; the water board's callout style, R2-C SfCallouts): numbered circles in the
# cut ground under each element, a numbered key under the section, each line "Element: reason" (<= 55 letters)
P24_CO = 2.65                # callout circle and key size, mm (= the water board's FS_MIN, 7.5 pt; R28DT_TS label)
P24_GROUP_DO = {"shade": u"shade", "wind": u"break the wind", "noise": u"soften the noise",
                "corridor": u"green corridor", "cleaning": u"clean the water", "perception": u"colour and scent"}
#                              what a planting group does (water board P12_GROUP_DO; plants.py purpose tags, sure only)
# the reasons: p24_reason's words, the corridor's notes (crossings, H5 sightline) and the section's own drawing rules
P24_WHY = {"walk": (u"Walk + bike lane" if P24_BIKE else u"Riverside walk") + u": in the shade, between the hubs",
           "reed": u"Reed cells: clean the water once before it goes back",
           "touch": u"Cell edge: a clean-water classroom",
           "terraces": u"Rain terraces: hold the rain, overflow to the reeds",
           "spill": u"Spillway: gives the cleaned water back to the stream",
           "wetland": u"Wetland bench: floods first, {:.2f} m over the bed",
           "demeter": u"Demeter's Garden: raised over Q500, stays dry",
           "dg_wall": u"Stone wall: holds the raised garden's edge",
           "hub": u"Hub square: a dry square at the bridge, plane shade",
           "wall": u"DSİ wall: kept, a railing to look into the channel",
           "wall_gone": u"DSİ wall: gives way to the wetland's soft toe",
           "subhub": u"Sub-hub: a place in the bed for the dry months",
           "stones": u"Stepping stones: sub-hub crossing, closes in floods",
           "foot": u"Footbridge: {:.0f} m reach without a crossing",
           "view": u"Viewing terrace: sightline to " + landmark_name("trajan_tapinagi")}   # G-R4-11: names table


def _p24_group_text(keys):
    """v36 (G9, as the water board's _p12_group_text): one planting group's callout, "Element: reason" (<= 55
    letters): its species, what it does (plants.py purpose tags, sure only); None when no sourced purpose is known"""
    keys = [q for q in dict.fromkeys(keys) if q in PLA_SPECIES]
    tags = set(t_ for q in keys for t_ in pla_purpose(q, sure_only=True))
    does = [P24_GROUP_DO[t_] for t_ in PLA_TAGS if t_ in tags and t_ in P24_GROUP_DO][:2]
    if not does:
        return None
    keys.sort(key=lambda q: -PLA_SPECIES[q]["h_m"])        # the tallest first
    nm = []
    for q in keys:
        w_ = PLA_SPECIES[q]["name"]
        nm.append(w_.lower() if w_.split()[-1].lower() == "tree" else w_.split()[-1].lower())
    tail = u": " + u", ".join(does)
    n = min(3, len(nm))
    while n > 1 and len(u" + ".join(nm[:n]) + tail) > 55:
        n -= 1
    s_ = u" + ".join(nm[:n]) + tail
    return s_[:1].upper() + s_[1:]


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
        elif s[0] == "image":                             # round 5 (S4 plant module v3, D4 interface): image plants
            it_ = tuple(s) + (None,) * (9 - len(s))       # pass through as Page image items ("image", x, y, w, h,
            pg.items.append(it_[:9])                      # path, alpha, flip, clip); the item export carries them
        elif s[0] == "circle" and len(s) >= 4:
            pg.circle(s[1], s[2], s[3], fill=s[4] if len(s) > 4 else None, stroke=s[5] if len(s) > 5 else None,
                      lw=(s[6] if len(s) > 6 and s[6] else 0.1), alpha=alpha)


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
        cz = [(P, z) for major, z, P in (((basemap_load() or {}).get("layers") or {}).get("contours") or []) if z is not None]
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
    the hub squares, buildings and roads of the survey grid. Round 5 (P24.7): Demeter's Garden = its design (02g
    dg_design: the zone outlines + the stream terrace that reaches the D2 cut)"""
    if any(pip(p[0], p[1], R_) for R_ in dg_design(C)["rings"]):
        return "demeter"
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

    def __init__(self, ta, tb, z0, style="b", den=None):
        self.ta, self.tb, self.z0, self.k = ta, tb, z0, 1000.0 / (den or DT_SCALE)   # round 5: den = an inset's scale
        self.w = (tb - ta) * self.k
        self.pg = Page(self.w, 0.0)
        self.pg.text_page(u"p22 section", bounds=(-60.0, -150.0, self.w + 60.0, 300.0), pad=P24_TP_PAD)   # v38
        self.wl = water_layers()
        self.style = style
        self.shapes = []                                 # every shape added (for the top)
        self.trees = []                                  # (key, h_m) drawn at layer 0 (G6 check)
        self.zl = []                                     # zone lines: (name, t, z of the ground, beyond)
        self.lv = []                                     # level words: (text, t, z)
        self.gnd = None                                  # v35 G14: z of the finished ground at t (set by p24_section)
        self.seated = 0                                  # v35 G14: items lowered onto the ground
        self.co = []                                     # v36: callouts (t, z of the ground, "Element: reason", row)

    def callout(self, t, z, text, row=0):
        """v36: a numbered callout under the element at t (row 0) or its planting group (row 1); placed by
        _p24_marks"""
        if text:
            self.co.append((t, z, text, row))

    def seat(self, t, z, half=None, count=True):
        """v35 (G14, nothing floats): z lowered to the lowest finished ground under the item's base (t +- half m)
        when it stands up to P24_SEAT_MAX above it (a slope); a bigger drop is a wall edge or a deliberate level
        (wall top, raised garden, water): z kept"""
        if self.gnd is None:
            return z
        half = P24_SEAT_HALF if half is None else half
        zm = min(self.gnd(t + d) for d in (-half, -half / 2.0, 0.0, half / 2.0, half))
        if 0.005 < z - zm <= P24_SEAT_MAX:
            self.seated += 1 if count else 0
            return zm
        return z

    def X(self, t):
        return (t - self.ta) * self.k

    def Y(self, z):
        return (z - self.z0) * self.k

    def put(self, shapes, layer="structures"):
        self.wl.add(layer, shapes)
        self.shapes += list(shapes or [])

    def plant(self, key, t, z, layer=0, seed=0, into="vegetation", **kw):
        z = self.seat(t, z) if not layer else z           # v35 G14 (behind the cut: on the cut ground as before)
        self.put(pla_section(key, self.X(t), self.Y(z), self.k, seed=seed, style=self.style, layer=layer, **kw), into)
        if not layer:
            self.trees.append((key, kw.get("h_m") or PLA_SPECIES[key]["h_m"]))

    def scatter(self, t0, t1, prof, b0, b1, mix, seed, density=1.0):
        """a mixed planting from t0 to t1 on the ground, band position b0 at t0 to b1 at t1 (M6, no rows)"""
        sh, placed = pla_scatter_section(self.X(t0), self.X(t1), lambda x: self.Y(_p24_zat(prof, x / self.k + self.ta)),
                                         self.k, t0=b0, t1=b1, mix=mix, seed=seed, style=self.style, density=density)
        self.put(sh, "vegetation")
        self.trees += [(key, h) for key, x, h, cr in placed]
        return [key for key, x, h, cr in placed]          # v36: the group's species (its callout)

    def _gy(self, z):
        """round 5 (S3, G-R5-4.4): the page-y ground under a figure: the finished ground where it lies within
        P24_SEAT_MAX of z (a slope, a step), else z (a wall top, the raised garden, a set level)"""
        def gy(x, z=z):
            if self.gnd is None:
                return self.Y(z)
            zg = self.gnd(x / self.k + self.ta)
            return self.Y(zg if abs(zg - z) <= P24_SEAT_MAX else z)
        return gy

    def fig(self, pose, t, z, facing=1, **kw):
        # round 5 (S3 sf_seat_feet): the feet on the HIGHER ground across the foot span (never sunk in a step)
        y = sf_seat_feet(self._gy(z), self.X(t), FIG_FOOT_HALF_M * self.k) if "sf_seat_feet" in globals() and \
            "FIG_FOOT_HALF_M" in globals() else self.Y(self.seat(t, z))
        self.put(fig_side(pose, self.X(t), y, self.k, facing=facing, mm_per_m=self.k, style=self.style, **kw),
                 "figures")

    def people(self, zone, t0, t1, z, seed=0, **kw):
        """people doing what the zone is for (M7 fig_activity) from t0 to t1, standing at z; v35 (G14): on dry ground
        each figure stands on the lowest finished ground under its feet (seat), so none floats on a slope or a terrace
        step; in the bed ("bed": wading) at z"""
        if t1 - t0 < 1.0:
            return
        gy = self.Y(z)
        kw.setdefault("focus", self.X(0.0))              # v36 (Aras 31 Oct 12:01): who stays looks at the stream
        if zone != "bed" and self.gnd is not None:       # round 5 (S3): feet on the higher ground (sf_feet_fn)
            gy = sf_feet_fn(self._gy(z), FIG_FOOT_HALF_M * self.k) if "sf_feet_fn" in globals() and \
                "FIG_FOOT_HALF_M" in globals() else \
                (lambda x, z=z: self.Y(self.seat(x / self.k + self.ta, z, 0.25, count=False)))
        sh, _ = fig_activity(zone, self.X(t0), self.X(t1), gy, self.k, seed=seed, style=self.style, **kw)
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


P24_SEAT_HALF = 0.3         # v35 G14: half the base of a plant or person, m (the lowest ground under it carries it)
P24_SEAT_MAX = 0.6          # v35 G14: lowered at most this much, m (more = a wall edge or a set level: kept)
P24_BACK_M = (140.0, 60.0)   # T7: ground lines this far behind the cut (view direction), from the survey: the context
P24_ARM_M = 60.0             # T7: trees of the corridor this far behind the cut stand in depth layer 1, farther in 2
P24_BACK_GAP = 6.0           # T7: trees behind the cut at least this far apart along it per depth layer, m (legible)


def p24_section(C, w, warn, style="b", den=None, ex=None):
    """v28 (WO-T4b-3): the section under window w (P24_CUTS), as (Page, w mm, h mm, legend keys, words not placed);
    None when the window has no cut. Looks upstream: the SW bank on the left, as the plan reads it. T7 (30 Oct,
    booklet p22, G8 / G10 / D1 / D9): one geometry, two styles ("b" vector, "a" cutouts); the levels from the cut
    registry (W1, W3: bed, average flow, Q100, Q500, wall tops; never typed); the water in the bed at the average
    yearly flow with Q100 / Q500 (M5 water_section); the ground behind the cut from the survey (context); the
    corridor's trees from the plan's tree set (layer 0 at the cut, 1 and 2 behind, D9); every zone with its paths
    (walk, bike lane, street: M8 sf_lane), its planting (M6, mixed, no rows) and people doing what it is for (M7,
    adults 1.75 m); the G6 check logged.
    Round 5 (S6, G-R5-12): with ex (a dict) the section is drawn for the item export: no zone band, no callout key,
    no level marks and no zoom inset are drawn (the booklet places them); ex gets the levels, callouts, zone names,
    walks and frame (ta, tb, z0, k, top) and the function returns ex. den = draw at 1:den (an inset: the SAME
    geometry drawn again at its own scale, G-R5-5). D8: the bridges (S3 br_section) in the background / cut.
    D2 (P24.7): Demeter's Garden in the cut (its stream terrace, 02g) with its tomato rows."""
    sp_ = p24_cut_span(w)
    if sp_ is None:
        return None
    cid, name, c0, cd, f, ta, tb = sp_
    R = w["R"]
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
    S = P24Sec(ta, tb, z0, style, den)
    S.cid = name                                          # v37: for the zoom inset's log line
    S.pg.tp.name = u"p22 {} section {}".format(name, style)   # v38 (G-R4-1)
    X, Y, k = S.X, S.Y, S.k
    zat = lambda t: _p24_zat(prof, t)
    S.gnd = zat                                           # v35 G14: the finished ground (after cuts, terraces, walks)
    # ---- context: the ground behind the cut (survey heights on lines parallel to it, farthest first), the corridor's
    # trees behind the cut in depth layers 1 and 2 (D9), on the background behind the cut ground
    backs, back_d = [], []
    for d in P24_BACK_M:
        g = [(t, z) for t, z in p24_ground(C, (c0[0] + f[0] * d, c0[1] + f[1] * d), cd, ta, tb) if ta <= t <= tb]
        if len(g) >= 2:
            backs.append([(X(t), Y(z)) for t, z in g])
            back_d.append(d)
    # v36 (Aras 31 Oct 12:01 "no background houses", checklist 7; R2-C sf_back_buildings): the basemap houses
    # SF_BACK_BAND m behind the cut (data height, else floors x BLD_STOREY), projected onto this cut (registry t, d ->
    # this section's t from c0 and d behind it); up to P24_ARM_M behind on the near ground line (layer 1, as the trees),
    # farther on the far one (layer 2); each layer's houses after its ground, so a nearer ground hides their feet;
    # none over the channel (it runs on behind the cut)
    houses, hspan, nh, nx = [], [], 0, 0
    try:
        ea, eb = level_ends(cid)
        sgn = 1.0 if (eb[0] - ea[0]) * cd[0] + (eb[1] - ea[1]) * cd[1] > 0 else -1.0   # this cut runs as the registry's
        off = (ea[0] - c0[0]) * cd[0] + (ea[1] - c0[1]) * cd[1]
        dsh = (ea[0] - c0[0]) * f[0] + (ea[1] - c0[1]) * f[1]
        s0, s1 = sorted(((ta - off) * sgn, (tb - off) * sgn))
        hlog = []
        for sa, sb, h_m, fl, dd in sf_back_buildings(cid, s0, s1, SF_BACK_BAND[0] - dsh, SF_BACK_BAND[1] - dsh,
                                                     log=hlog, look=int(sgn)):
            ha, hb = sorted((off + sgn * sa, off + sgn * sb))
            houses.append((ha, hb, h_m, fl, dd + dsh))
    except Exception as ex:
        warn.append(u"section {}: background houses not drawn ({}: {})".format(name, type(ex).__name__, ex))
    if backs:
        bsh = sf_topo_back(backs, Y(z0)).L["background"]  # two shapes per ground line, the farthest first
        for i, d in enumerate(back_d):
            S.wl.add("background", bsh[2 * i:2 * i + 2])
            ly = 1 if d <= P24_ARM_M else 2
            for ha, hb, h_m, fl, dd in houses:
                if (1 if dd <= P24_ARM_M else 2) != ly:
                    continue
                if hb - ha < 3.0 or (hb > -hw - P24_WALL_T - 1.0 and ha < hw + P24_WALL_T + 1.0):
                    nx += 1                               # under one bay (sf_back_house's 3.0 m) or over the channel
                    continue
                S.put(sf_back_house(X(ha), X(hb), sf_gy(backs[i]), h_m, k, layer=ly, floors=fl, d_m=dd),   # v38 (G-R4-5.3)
                      "background")
                hspan.append((ha, hb, dd))
                nh += 1
        keys.add("back")
        if nh:
            keys.add("bhouse")
    if style == "b":
        warn.append(u"section {}: {} background houses drawn ({} left out: narrow or over the channel)".format(
            name, nh, nx + max(0, len(houses) - nh - nx)))
    near0, back = [], []
    for i, (key, x_, y_, cr, I_) in enumerate(p24_tree_set(C, w)):   # round 5: the plan's placer trees (P24.4)
        p = (x_, y_)
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
        if any(ha <= t <= hb and dd < d for ha, hb, dd in hspan):
            continue                                      # v36: behind a nearer house (nothing see-through)
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
    S.lv.append((u"bed", 0.0, bed))                       # v38: (level mark name, t, level m)
    for side, sg in (("SW", -1.0), ("NE", 1.0)):         # DSİ walls kept (stone, railing) or given way (dashed)
        if kinds[side] != "dsi_wall":
            continue
        a, b = sg * hw, sg * (hw + P24_WALL_T)
        ring_ = [(X(a), Y(bed)), (X(b), Y(bed)), (X(b), Y(tops[side])), (X(a), Y(tops[side]))]
        S.callout((a + b) / 2.0, tops[side], P24_WHY["wall_gone" if side in gone else "wall"])   # v36
        if side in gone:
            S.put([("line", ring_ + ring_[:1], COL["ink2"], 0.15, [0.8, 0.5])])
            continue
        S.block(a, b, bed, tops[side], "stone")
        S.put(sct_bank("railing", X((a + b) / 2.0), Y(tops[side]), Y(bed), -sg, k, h_m=P24_RAIL_H)[0])
        S.lv.append((u"railing", b, tops[side] + P24_RAIL_H))
        keys.add("wall")
    railed = False
    for side, sg in (("SW", -1.0), ("NE", 1.0)):         # one figure at a railing, looking into the channel
        if kinds[side] == "dsi_wall" and side not in gone and not railed:
            fc = 1 if sg < 0 else -1
            m_ = fig_meta("railing", facing=fc, rail_h=P24_RAIL_H)
            S.fig("railing", sg * (hw + P24_WALL_T / 2.0) - m_.get("rail_x", 0.0), tops[side], facing=fc,
                  rail_h=P24_RAIL_H)
            railed = True
    # ---- the sub-hub in the bed (zone WA, bed tier) where the cut crosses it (v36: no people in its water)
    sub = any(p24_zone(C, (c0[0] + cd[0] * u, c0[1] + cd[1] * u)) == "subhub"
              for u in [-hw + (i + 0.5) * (2.0 * hw) / 8.0 for i in range(8)])
    if sub:                                               # v36 (Aras 31 Oct 11:28, checklist 11): nobody in the
        #                                                   water-filled channel: the sub-hub keeps its name and callout
        S.zl.append((P24_NAME["subhub"], 0.0, bed, False))
        S.callout(0.0, bed, P24_WHY["subhub"])           # v36
    # ---- the corridor's trees at the cut (the plan's tree set, layer 0)
    for t, key, cr, i in near0:
        S.plant(key, t, zat(t), seed=i, crown_m=cr)
        keys.add("forest")
    grp = []                                              # v36 (G9): one callout per group of them (a gap > 10 m or
    for t, key, cr, i in sorted(near0):                   # the stream between splits a group)
        if grp and (t - grp[-1][-1][0] > 10.0 or (t > 0.0) != (grp[-1][-1][0] > 0.0)):
            grp.append([])
        if not grp:
            grp.append([])
        grp[-1].append((t, key))
    for g_ in grp:
        tm_ = (g_[0][0] + g_[-1][0]) / 2.0
        S.callout(tm_, zat(tm_), _p24_group_text([q for _t, q in g_]), row=1)
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
            S.lv.append((u"square", tm, zf))
            S.callout(tm, zf, P24_WHY["hub"])             # v36
            if hub_t:
                S.callout(sum(hub_t) / len(hub_t), zf, _p24_group_text(["plane"]), row=1)
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
            if x1_ > x0_:                                 # round 5 (P24.7, U64): the garden's crop in the cut,
                S.put(pla_crop_rows("tomato", x0_, x1_, Y(gf), k, spacing=DG_ROW_M,
                                    h_m=DG_TOMATO_H_M, crown_m=DG_TOMATO_W_M), "vegetation")   # tomato rows
                keys.add("dg_rows")                       # (row spacing a drawing rule, 02g DG_ROW_M)
                S.fig("stand", (min(t0, t1) + max(t0, t1)) / 2.0 + sg * 2.0, gf, facing=-1 if sg > 0 else 1)
            S.plant("lavender", te - sg * 1.2, gf, seed=81)
            S.lv.append((u"garden", tm, gf))
            S.callout(tm, gf, P24_WHY["demeter"])         # v36
            S.callout(te - sg * P24_WALL_DG / 2.0, gf, P24_WHY["dg_wall"])
            S.callout(tm + sg * 3.0, gf, u"Tomato rows: the garden's crop, above the flood", row=1)
        elif key == "wetland" and abs(tm) > hw:
            te = min((t0, t1), key=abs)                   # the water's side of the bench
            b0, b1 = (0.0, 0.45) if te == t0 else (0.45, 0.0)
            got = S.scatter(t0, t1, prof, b0, b1, ("soft_rush", "loosestrife", "willow", "tamarisk"), seed=90,
                            density=0.9)
            S.callout(tm, zat(tm), P24_WHY["wetland"].format(TERRACE_UP))   # v36
            if got:
                S.callout(tm, zat(tm), _p24_group_text(got), row=1)
            sg = 1.0 if tm > 0 else -1.0
            if ln_ >= 8.0:
                S.fig("watch", te + sg * 3.0, zat(te + sg * 3.0), facing=-1 if sg > 0 else 1)
        elif key == "terraces":
            got = S.scatter(t0, t1, prof, 0.86, 0.94, ("lavender",), seed=100, density=0.8)
            S.people("walkway", t0 + 1.0, t1 - 1.0, zat(tm), seed=31, density=0.5, max_n=2)
            S.callout(tm, zat(tm), P24_WHY["terraces"])   # v36
            if got:
                S.callout(tm, zat(tm), _p24_group_text(got), row=1)
        elif key == "spill" and ln_ >= P24_MIN_RUN:
            S.callout(tm, zat(tm), P24_WHY["spill"])      # v36
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
        S.lv.append((u"reed cells", (cells[0][0] + cells[-1][1]) / 2.0, cells[0][2]))
        S.callout(a - 0.7, rim, P24_WHY["touch"])         # v36
        tc = (cells[0][0] + cells[-1][1]) / 2.0
        S.callout(tc, zat(tc), P24_WHY["reed"])
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
        S.callout(t, zw, P24_WHY["walk"])                 # v36
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
        d_lo = P24_STREET_D[0] if c_["kind"] == "stepping stones" else 0.0   # v38 closing: stones at the cut too
        if not all(d_lo < d <= P24_BEYOND_M for _, d in ts_):
            continue
        t1_, t2_ = sorted(t for t, _ in ts_)
        if t2_ < ta or t1_ > tb:
            continue
        t1_, t2_ = max(ta, t1_), min(tb, t2_)
        ly_ = 0 if all(abs(d) <= 3.0 for _, d in ts_) else 1   # within 3 m of the cut: layer 0 (as the street kit)
        pale = fig_fade(COL["ink2"], 1 if c_["kind"] == "footbridge" else ly_)
        if c_["kind"] == "footbridge":
            zd = max(zat(t1_), zat(t2_))
            S.put([("line", [(X(t1_), Y(zd)), (X(t2_), Y(zd))], pale, 0.6)], "background")
            S.zl.append((P24_NAME["foot"], (t1_ + t2_) / 2.0, zd, True))
            if c_.get("gap"):                             # v36: the corridor's reason (its crossings note)
                S.callout((t1_ + t2_) / 2.0, zat((t1_ + t2_) / 2.0), P24_WHY["foot"].format(c_["gap"]))
        elif c_["kind"] == "stepping stones":
            t = max(t1_, -hw) + P24_STONE[1] / 2.0
            st_t = []
            while t < min(t2_, hw):
                S.put([("poly", sec_ellipse(X(t), Y(bed) + P24_STONE[0] * k, P24_STONE[0] * k, P24_STONE[0] * k, 12),
                        pale, None, 0.1)], "structures")
                st_t.append(t)
                t += P24_STONE[1]
            S.zl.append((P24_NAME["stones"], 0.0, bed, ly_ > 0))
            S.callout(0.0, bed, P24_WHY["stones"])        # v36
            p24_stones_people(S, st_t, bed, avg, ly_, warn if style == "b" else [], name)   # v38 closing G-R4-5.7
    # v38 (round 4, P22.8): the street elements the plan places, where they stand near the cut (P24_STREET_D): on the
    # cut ground, layer 0 within 3 m, else faded one layer behind
    for kind, fn in (("lamp", lambda x, y, ly: sf_lamp(x, y, k, side=1, layer=ly)),
                     ("bollard", lambda x, y, ly: sf_bollard(x, y, k, layer=ly)),
                     ("rack", lambda x, y, ly: sf_bike_rack(x, y, k, side=1, layer=ly))):
        n_ = 0
        for q in _P24_STREET[kind]:
            t, d = _p24_tz(c0, cd, f, q)
            if P24_STREET_D[0] <= d <= P24_STREET_D[1] and ta + 1.0 <= t <= tb - 1.0 and abs(t) > hw + 1.0:
                S.put(fn(X(t), Y(zat(t)), 0 if abs(d) <= 3.0 else 1), "structures")
                n_ += 1
        if n_:
            keys.add(kind)
    # v38 (G-R4-5.2, S3 handover): the shrub and flower layer on every planted run (no rows; sourced species only)
    paths = [(X(min(t - sg * WALK_W / 2.0, t - sg * WALK_W / 2.0 + sg * lane_w)),
              X(max(t - sg * WALK_W / 2.0, t - sg * WALK_W / 2.0 + sg * lane_w))) for t, zw, sg in walks]
    for j, (key, t0, t1) in enumerate(runs):
        if key in P24_LOW_IN and t1 - t0 >= 4.0:
            sh_, _pl = pla_low_section(X(t0), X(t1), lambda x: Y(zat(x / k + ta)), k, t0=P24_LOW_IN[key][0],
                                       t1=P24_LOW_IN[key][1], seed=60 + j, avoid=paths, water=Y(avg),
                                       mix=P24_LOW_MIX.get(key))
            S.put(sh_, "vegetation")
            keys.add("low")
    for xy in ([C.terrace["xy"]] if C.terrace else []) + list(_P24_DECK):   # v38: the window's own deck too
        t, d = _p24_tz(c0, cd, f, xy)
        if 0.0 < d <= P24_BEYOND_M and ta + 3.0 <= t <= tb - 3.0:
            zz = zat(t)
            S.put([("line", [(X(t - 2.0), Y(zz + 0.3)), (X(t + 2.0), Y(zz + 0.3))], fig_fade(COL["ink2"], 1), 0.5)],
                  "background")
            S.zl.append((P24_NAME["view"], t, zz, True))
            S.callout(t, zz, P24_WHY["view"])             # v36
    try:                                                  # round 5 (D8, G-R5-4.7, S3): the bridges this cut sees
        lk = 1 if (f[0] * -cd[1] + f[1] * cd[0]) > 0 else -1   # br's "beyond" = cd turned left x look; p24's f
        ends_ = ((c0[0] + cd[0] * ta, c0[1] + cd[1] * ta), (c0[0] + cd[0] * tb, c0[1] + cd[1] * tb))
        tops_ = [v for v in (tops or {}).values() if v is not None]
        br_section(name, X=lambda t_: X(ta + t_), Y=Y, look=lk, t0=0.0, t1=tb - ta, top=max(tops_) if tops_ else None,
                   page=u"p22 " + name, into=S.wl, ends=ends_, bed=bed)
    except Exception as ex_:
        warn.append(u"section {}: bridges not drawn ({}: {})".format(name, type(ex_).__name__, ex_))
    if SF_SKY_DEFAULT == "designed":                     # v36 (D8, default a: every section): the designed sky, behind all
        g0_ = min(Y(p[1]) for p in prof)
        S.wl.add("atmosphere", sf_sky(0.0, S.w, g0_, max(_p24_top(S.shapes) or 0.0, g0_ + 10.0) + 3.0,
                                      seed={"W1": 5, "W3": 7}.get(cid, 5), cid=u"p22 " + name))   # v37 (G15)
    S.draw()
    bad = sf_assert_g6(k, trees=S.trees, strict=False)   # G6: people 1.75 m, every tree in its sourced height range
    if bad and style == "b":
        warn.append(u"section {}: {}".format(name, u"; ".join(bad)))
    if style == "a" and S.seated:                         # v35 G14 log (style a = the booklet's)
        warn.append(u"section {}: G14 {} plants / single figures lowered onto the ground (groups follow the ground per figure)".format(name, S.seated))
    # ---- words (v37, round 3, P22.4 / G3 / G15): no name lines over the drawing; the zones named in a band UNDER the
    # cut (R07 idea, p24_band), the ZOOMED IN inset of the walk above the drawing (p24_zoom), the levels by their points
    top = max([_p24_top(S.shapes) or 0.0] + [Y(p[1]) for p in prof] + [Y(q500) + 2.0 * KEY_MIN]) + 2.0
    ts_lab, missing = KEY_MIN, []
    taken = []
    h = top
    if ex is not None:                                    # round 5 (G-R5-12): the words are the booklet's
        lvs, seen_ = [], set()
        for lv in list(S.wl.anchors.get("levels") or []) + [(nm_, zz) for nm_, t, zz in S.lv]:
            if lv[0] not in seen_:
                seen_.add(lv[0])
                lvs.append((lv[0], lv[1]))
        for s_, t, al in ((name, ta, "L"), (name + u"\u2032", tb, "R")):   # the cut's names at its ends (labels)
            S.pg.text(s_, X(t) + (0.6 if al == "L" else -0.6), Y(zat(t)) + 1.2, 3.4, COL["ink_dark"], bold=True,
                      align=al)
        co = _p24_marks(S, zat, taken, missing)
        n0 = len(S.pg.items)
        shp_put(S.pg, co.marks(size=P24_CO))
        S.pg.items[n0:] = [it_[:9] + ("marker",) if it_[0] == "text" else it_ for it_ in S.pg.items[n0:]]
        zones, seen_ = [], set()
        for key, t0, t1 in runs:                          # the zone names (was the band under the section)
            if key in P24_BAND and (t1 - t0 >= P24_MIN_RUN or key == "bed"):
                tm = (t0 + t1) / 2.0
                nm = P24_BAND["subhub"] if (key == "bed" and sub) else P24_BAND[key]
                zones.append((nm, tm, zat(tm), False))
        for nm, t, zz, beyond in S.zl:
            if beyond:
                zones.append((nm[:1] + nm[1:].lower() + u" (beyond)", t, zz, True))
        ex.update(pg=S.pg, w=S.w, top=top, ta=ta, tb=tb, z0=z0, k=k, levels=lvs, keys=keys, missing=missing,
                  callouts=[(n_, ta + x_ / k, z0 + y_ / k, t_) for n_, x_, y_, t_ in co.items], zones=zones,
                  walks=walks, runs=runs, cid=cid, name=name, hw=hw, gf=gf, bed=bed, avg=avg, S=S)
        return ex
    zb = p24_zoom(S, walks, runs, top, missing)
    if zb:
        taken.append(zb)
        h = max(h, zb[3] + 0.5)
    band_h, bboxes = p24_band(S, runs, walks, sub, hw, missing)
    taken += bboxes
    for s_, t, al in ((name, ta, "L"), (name + u"'", tb, "R")):   # the cut's names, as on the plan
        x, y = X(t) + (0.6 if al == "L" else -0.6), Y(zat(t)) + 1.2
        S.pg.text(s_, x, y, 3.4, COL["ink_dark"], bold=True, align=al)
        wd = text_w(s_, 3.4, True)
        taken.append((x if al == "L" else x - wd, y - 0.3, x + wd if al == "L" else x, y + 3.4))
    co = _p24_marks(S, zat, taken, missing)               # v36: the numbered circles in the cut ground
    shp_put(S.pg, co.marks(size=P24_CO))
    # v38 (round 4, G-R4-5.4, U43/U44, S2 handover): every level in the margin right of the section frame (open
    # triangle on a tick at the level's height, value outside), the water's levels (water_section anchors) first,
    # then the section's own (bed, railing, square, garden, reed cells), one mark per name; nothing in the picture
    lvs, seen_ = [], set()
    for lv in list(S.wl.anchors.get("levels") or []) + [(nm_, zz) for nm_, t, zz in S.lv]:
        if lv[0] not in seen_:
            seen_.add(lv[0])
            lvs.append(lv)
    shp_put(S.pg, sf_level_marks((0.0, 0.0, S.w, top), lvs, side="R", y_of=Y, size=ts_lab, page=u"p22 " + name))
    keys.add("section")
    # v36: the numbered key under the section (as p.17's: columns across the section's width); kh = its depth under
    # the drawing (y < 0), which the panel adds to the section's block, so the booklet crop reaches down to it
    items = sorted(dict((n_, t_) for n_, _x, _y, t_ in co.items).items())
    kh = 0.0
    if items:
        cw = max(text_w(t_, P24_CO) for _n, t_ in items) + 2.0 * P24_CO + 4.0
        nc = max(1, min(len(items), int((S.w + 4.0) // cw)))
        per = (len(items) + nc - 1) // nc
        yk = -(band_h + 1.5 + 0.35 * P24_CO)              # v37: under the zone band
        for c_ in range(nc):
            part = items[c_ * per:(c_ + 1) * per]
            if part:
                kc = SfCallouts()
                kc.items = [(n_, 0.0, 0.0, t_) for n_, t_ in part]
                shp_put(S.pg, kc.key(c_ * cw, yk, size=P24_CO))
        kh = -(yk - (per - 1) * 1.5 * P24_CO - 1.15 * P24_CO) + 0.5
        if nc * cw - 4.0 > S.w + 0.1:
            warn.append(u"section {}: the callout key ({:.0f} mm) is wider than the section ({:.0f} mm)".format(
                name, nc * cw - 4.0, S.w))
    kh = max(kh, band_h)
    TP_LOG.append(S.pg.check_text())                     # v38 (G-R4-1): the section's collision test (raises)
    return S.pg, S.w, h, keys, missing, kh


def p24_stones_people(S, st_t, bed, avg, ly, warn, name):
    """v38 closing (G-R4-5.7, S8 "stepping stones + wading"): the way into the bed that the masterplan designs is the
    sub-hub's stepping stones (Corridor.crossings, P24_STONE); the section's people use them by the figures module's
    rules (U26: in the water only on stepping stones or wading; FIG_WADE_MAX_M knee deep at most): when a stone's
    top (bed + its 2 x P24_STONE[0] height) stands above the average yearly flow, two people cross on the stones
    (poses from FIG_ACTIVITY["stepping_stones"], each on a stone's top); else, when the average flow is no deeper
    than FIG_WADE_MAX_M, one person wades beside the stones; else nobody (logged). st_t = the stones' t (m),
    ly = their depth layer (0 at the cut, 1 beyond). Returns the number of people drawn."""
    if not st_t:
        return 0
    X, Y, k = S.X, S.Y, S.k
    top = bed + 2.0 * P24_STONE[0]
    if top >= avg:
        poses = [a[0] for a in FIG_ACTIVITY["stepping_stones"]][:2]
        at = sorted(set([st_t[len(st_t) // 3], st_t[(2 * len(st_t)) // 3]]))
        for i, t in enumerate(at):
            S.put(fig_side(poses[i % len(poses)], X(t), Y(top), k, facing=1 if i % 2 == 0 else -1, mm_per_m=k,
                           layer=ly, style=S.style), "figures")
        return len(at)
    if avg - bed <= FIG_WADE_MAX_M:
        t = st_t[0] + P24_STONE[1] / 2.0                  # between the first two stones, in the water
        S.put(fig_side("wade", X(t), Y(bed), k, facing=1, mm_per_m=k, layer=ly, style=S.style, depth_m=avg - bed),
              "figures")
        return 1
    warn.append(u"section {}: nobody on the stepping stones: the average flow ({:.2f} m deep) covers the stones' tops "
                u"({:.2f} m) and is deeper than knee ({:.2f} m)".format(name, avg - bed, top - bed, FIG_WADE_MAX_M))
    return 0


# v37 (round 3, P22.4, R07 idea): the zones' names in a band under the section, sentence case
P24_BAND = {"reed": u"Reed basins", "spill": u"Spillway", "terraces": u"Rain terraces", "demeter": u"Demeter's Garden",
            "forest": u"Forest corridor", "trees": u"Trees", "wetland": u"Wetland bench", "subhub": u"Sub-hub in the bed",
            "hub": u"Hub square", "walk": u"Walk + bike lane" if P24_BIKE else u"Riverside walk", "street": u"Street",
            "bld": u"Building", "bed": u"Selinos stream", "foot": u"Footbridge", "stones": u"Stepping stones",
            "view": u"Viewing terrace"}
P24_BAND_SHORT = {"demeter": u"Garden", "terraces": u"Terraces", "wetland": u"Wetland", "walk": u"Walk",
                  "subhub": u"Sub-hub", "bed": u"Stream", "forest": u"Forest", "reed": u"Reeds", "hub": u"Square"}
P24_ZOOM_DEN = 250.0         # v38 (round 4, P22.6, G-R4-5.6): the zoom inset at 1:250 = 4 x its 1:1,000 parent
#                              (was a 1.75 m person 6 mm tall = 1:292)
P24_LOW_IN = {"terraces": (0.65, 0.8), "forest": (0.5, 0.7), "wetland": (0.1, 0.3), "demeter": (0.85, 0.9),
              "trees": (0.4, 0.7)}   # v38: runs with the low layer: band positions wet (0) -> dry (1), drawing rule
P24_LOW_MIX = {"demeter": ("lavender", "rosemary", "chaste")}   # the garden's beds (as its plan)
P24_ZOOM_SPOT = (10.0, 4.5, 1.0)   # the inset's spot: m wide, m high, m of it under the walk's surface


def p24_band(S, runs, walks, sub, hw, missing):
    """v37 (P22.4, R07): the zones along the cut named in a band under the section (y < 0): a tick at each zone's
    ends and its name centred under it (the short name, else left out and logged, when it does not fit); the walk
    with its bike lane spliced in where the cut crosses it; the bed named "Sub-hub in the bed" where the cut crosses
    the sub-hub; a second, grey row names what stands beyond the cut (S.zl beyond entries) at its place. Returns
    (band depth mm, text boxes)."""
    segs = [[k_, t0, t1] for k_, t0, t1 in runs if k_ in P24_BAND]
    for t, zw, sg in walks:                               # the walk + bike lane over whatever zone it lies in
        lw_ = WALK_W + (P24_BIKE_W if P24_BIKE else 0.0)
        a_, b_ = sorted((t - sg * WALK_W / 2.0, t - sg * WALK_W / 2.0 + sg * lw_))
        out = []
        for k_, t0, t1 in segs:
            if t1 <= a_ or t0 >= b_:
                out.append([k_, t0, t1])
                continue
            if t0 < a_:
                out.append([k_, t0, a_])
            if t1 > b_:
                out.append([k_, b_, t1])
        out.append(["walk", a_, b_])
        segs = sorted(out, key=lambda r_: r_[1])
    ts_ = KEY_MIN
    yb1 = -0.3 - ts_ * 1.05
    ink, ink2 = COL["ink_dark"], COL["ink2"]
    boxes = []
    for k_, t0, t1 in segs:
        x0, x1 = S.X(max(t0, S.ta)), S.X(min(t1, S.tb))
        if x1 - x0 < 0.3:
            continue
        for x in (x0, x1):
            S.pg.line([(x, -0.3), (x, yb1 - 0.3)], ink2, 0.12)
        nm = P24_BAND["subhub"] if (k_ == "bed" and sub) else P24_BAND[k_]
        sh_ = P24_BAND_SHORT.get("subhub" if (k_ == "bed" and sub) else k_)
        for s_ in (nm, sh_):
            if s_ and text_w(s_, ts_, True) <= x1 - x0 - 0.8:
                xm = (x0 + x1) / 2.0
                S.pg.text(s_, xm, yb1, ts_, ink, bold=True, align="C")
                wd = text_w(s_, ts_, True)
                boxes.append((xm - wd / 2.0, yb1 - 0.2 * ts_, xm + wd / 2.0, yb1 + 0.8 * ts_))
                break
        else:
            missing.append(u"zone band: " + nm + u" (narrower than its name)")
    yb2 = yb1 - ts_ * 1.4
    used, row2 = [], False
    for nm, t, zz, beyond in sorted(S.zl, key=lambda z_: z_[1]):
        if not beyond:
            continue
        s_ = nm[:1] + nm[1:].lower() + u" (beyond)"
        wd = text_w(s_, ts_)
        x = min(max(S.X(t), wd / 2.0), S.w - wd / 2.0)
        if any(not (x - wd / 2.0 > b_ + 1.0 or x + wd / 2.0 < a_ - 1.0) for a_, b_ in used):
            missing.append(s_)
            continue
        used.append((x - wd / 2.0, x + wd / 2.0))
        S.pg.text(s_, x, yb2, ts_, ink2, align="C")
        boxes.append((x - wd / 2.0, yb2 - 0.2 * ts_, x + wd / 2.0, yb2 + 0.8 * ts_))
        row2 = True
    return -((yb2 if row2 else yb1) - 0.3 * ts_) + 0.5, boxes


def p24_zoom(S, walks, runs, top, missing):
    """v37 (G15, PLAN §2 Zoom inset): the walk nearest the stream re-drawn in a box above the section at the scale
    P24_ZOOM_DEN (v38: 1:250, 4 x the parent, with its own scale bar; sf_zoom_inset: spot frame on the cut, one connector, "ZOOMED IN · walk
    + bike lane"); no walk on the cut: the hub square; neither: nothing, "FLAG zoom inset <cut> skipped" logged.
    Images only where they lie wholly in the box. Returns the inset's box (with its label) or None."""
    k_dst = 1000.0 / P24_ZOOM_DEN
    wm, hm_, dn = P24_ZOOM_SPOT
    if walks:
        t, zw, sg = min(walks, key=lambda w_: abs(w_[0]))
        t += sg * (P24_BIKE_W / 2.0 if P24_BIKE else 0.0)
        what = P24_BAND["walk"].lower()
    else:
        hub = [r_ for r_ in runs if r_[0] == "hub"]
        if not hub:
            WAT_LOG.append(u"FLAG zoom inset p22 {}: skipped: no walk or hub square on the cut".format(S.cid))
            return None
        t = (hub[0][1] + hub[0][2]) / 2.0
        zw = S.gnd(t)
        what = u"hub square"
    src = (S.X(t - wm / 2.0), S.Y(zw - dn), S.X(t + wm / 2.0), S.Y(zw - dn + hm_))
    bw, bh = wm * k_dst, hm_ * k_dst
    lab = SF_ZOOM["label_mm"] * 1.6
    if bw > S.w:
        WAT_LOG.append(u"FLAG zoom inset p22 {}: skipped: no room".format(S.cid))
        return None
    cx = min(max((src[0] + src[2]) / 2.0, bw / 2.0), S.w - bw / 2.0)
    dst = (cx - bw / 2.0, top + 1.0, cx + bw / 2.0, top + 1.0 + bh)
    k_src = S.k
    for sh in sf_zoom_inset(src, dst, k_src, k_dst, S.wl, what, scale_den=P24_ZOOM_DEN, parent_den=DT_SCALE,
                            page=u"p22 " + S.cid):
        if sh[0] == "image" and not (dst[0] <= sh[1] and sh[1] + sh[3] <= dst[2] and dst[1] <= sh[2] and
                                     sh[2] + sh[4] <= dst[3]):
            continue
        shp_put(S.pg, [sh])
    return (dst[0], dst[1], dst[2], dst[3] + lab)


def _p24_marks(S, zat, taken, missing):
    """v36 (the water board's callout style, R2-C): each callout of S.co as a numbered circle (SfCallouts, P24_CO) in
    the cut ground under its element (row 0) or a circle lower under its planting group (row 1); a circle that would
    touch another circle, a word box (taken) or leave the drawing moves sideways by one circle, then deeper; the same
    text keeps one number. Its boxes join taken (the level words keep clear). Returns the SfCallouts."""
    co = SfCallouts()
    r = 0.75 * P24_CO
    step = 2.0 * r + 0.4
    done = []
    for t, z, txt, row in sorted(S.co, key=lambda c_: (c_[3], c_[0])):
        got = None
        for dx in (0, 1, -1, 2, -2, 3, -3):
            x = min(max(S.X(t) + dx * step, r + 0.3), S.w - r - 0.3)
            gyx = min(S.Y(zat(min(max(x_ / S.k + S.ta, S.ta), S.tb))) for x_ in (x - r, x, x + r))
            for j in ((0, 1, 2) if row == 0 else (1, 2, 0)):
                y = gyx - 0.4 - r - j * step
                b = (x - r, y - r, x + r, y + r)
                if b[1] < 0.4 or any(math.hypot(x - px, y - py) < step for px, py in done) or \
                        any(b[0] < q[2] and q[0] < b[2] and b[1] < q[3] and q[1] < b[3] for q in taken):
                    continue
                got = (x, y, b)
                break
            if got:
                break
        if got is None:
            missing.append(u"callout: " + txt)
            continue
        co.add(got[0], got[1], txt)
        done.append((got[0], got[1]))
        taken.append(got[2])
    return co


def p24_cut_on_plan(pg, w, T, taken, segs, bounds):
    """the section's line on the plan (only this window's cut): v38 (round 4, P22.8, G-R4-9): the red R01 dash-dot
    (KM_CUT) on a white casing, running left -> right in the turned window, its names D1 / D1' just beyond its ends;
    no triangles (the look direction is shown on the key map only)."""
    sp_ = p24_cut_span(w)
    if sp_ is None:
        return False
    cid, name, c0, cd, f, ta, tb = sp_
    A = T((c0[0] + cd[0] * ta, c0[1] + cd[1] * ta))
    B = T((c0[0] + cd[0] * tb, c0[1] + cd[1] * tb))
    col = KM_CUT["colour"]
    pg.line([A, B], COL["white"], 1.0, cap=0)            # v37 (P22.2): a white casing, the line reads over the trees
    pg.line([A, B], col, KM_CUT["lw"], list(KM_CUT["dash"]), cap=0)
    segs.append((A, B))
    ts_ = R28DT_TS["place"]
    for (x, y), nm, al in ((A, name, "R"), (B, name + u"'", "L")):
        wd = text_w(nm, ts_, True)
        x0 = x - 0.8 - wd if al == "R" else x + 0.8
        cands = [(x0, y - ts_ * 0.5), (x - wd / 2.0, y + 1.0), (x - wd / 2.0, y - 1.0 - ts_)]   # beside, above, under
        cands = [(min(max(cx, bounds[0]), bounds[2] - wd), min(max(cy, bounds[1]), bounds[3] - ts_)) for cx, cy in cands]
        bx, by = next(((cx, cy) for cx, cy in cands if _r28_free((cx, cy, cx + wd, cy + ts_), taken, (), bounds, 0.3)),
                      cands[0])
        b = (bx, by, bx + wd, by + ts_)
        pg.text(nm, b[0], b[1] + ts_ * 0.14, ts_, col, bold=True, halo=COL["white"])
        taken.append(b)
        _P24_LAB.append(b)
    return True


P24_CUT_INSET_M = 8.0        # v37 (round 3, P22.2): the cut line (and its section) starts this far inside the window, m
#                              (8 mm at 1:1,000: room for its name inside the frame)
P24_LEVEL_MM = 24.0          # v38 (G-R4-5.4): the cut stops this far (m = mm at 1:1,000) short of the window's right
#                              edge: the section's level marks stand in that margin, inside the column
P24_CUT_BAND = (0.30, 0.70)  # v38 (P22.1): the cut line's height in the turned plan, fraction of its height (design)


def _p24_cut_dir(cid):
    """v38: (cd, f) of a registry cut: cd the unit direction SW end -> NE end, f the view (upstream: the SW end on
    its left), f = cd turned 90 degrees counter-clockwise"""
    E = level_ends(cid)
    L = math.hypot(E[1][0] - E[0][0], E[1][1] - E[0][1]) or 1.0
    cd = ((E[1][0] - E[0][0]) / L, (E[1][1] - E[0][1]) / L)
    if level_end_labels(cid)[0] != u"SW":
        cd = (-cd[0], -cd[1])
    return cd, (-cd[1], cd[0])


def p24_frame(w):
    """v38 (round 4, P22.1, U46): window w turned so its cut runs left -> right on the page (u = the cut's direction)
    and the section's view (upstream, v) points up the page: plan and section read the same way and share the cut
    axis. Same size and centre as detail_windows' north-up window, moved along v only as far as needed to hold the
    cut between P24_CUT_BAND of its height. Returns dict(o origin (survey m, the page's lower-left), u, v, W, H (m),
    R (bounding box, survey m), ring (the four corners), north (north's turn from page-up, rad, counter-clockwise))."""
    R = w["R"]
    Wm, Hm = R[2] - R[0], R[3] - R[1]
    c = ((R[0] + R[2]) / 2.0, (R[1] + R[3]) / 2.0)
    u, v = (1.0, 0.0), (0.0, 1.0)
    cid = P24_CUTS.get(w["id"], (None, None))[0]
    if cid:
        u, v = _p24_cut_dir(cid)
        c0 = CUT_AT[{"W1": 0, "W3": 2}[cid]][2]
        dv = (c0[0] - c[0]) * v[0] + (c0[1] - c[1]) * v[1]
        lo, hi = (P24_CUT_BAND[0] - 0.5) * Hm, (P24_CUT_BAND[1] - 0.5) * Hm
        sh_ = dv - lo if dv < lo else (dv - hi if dv > hi else 0.0)
        c = (c[0] + v[0] * sh_, c[1] + v[1] * sh_)
    o = (c[0] - u[0] * Wm / 2.0 - v[0] * Hm / 2.0, c[1] - u[1] * Wm / 2.0 - v[1] * Hm / 2.0)
    ring = [(o[0] + u[0] * a + v[0] * b, o[1] + u[1] * a + v[1] * b) for a, b in ((0, 0), (Wm, 0), (Wm, Hm), (0, Hm))]
    return dict(o=o, u=u, v=v, W=Wm, H=Hm, R=bbox(ring), ring=ring, north=math.atan2(-u[1], v[1]))


def p24_cut_span(w):
    """v37: (cid, name, c0, cd, f, ta, tb) of window w's cut, or None: c0 the registry cut's centre (survey m), cd the
    unit direction SW end -> NE end, f the view (upstream: the SW end on its left), ta..tb the part of the line drawn.
    One span for the plan's cut line and the section, so they always match. v38 (P22.1): in the turned window
    (p24_frame) the cut runs left -> right: from P24_CUT_INSET_M inside its left edge to P24_LEVEL_MM short of its
    right edge (the section's level marks stand in that margin, G-R4-5.4)."""
    cid, name = P24_CUTS.get(w["id"], (None, None))
    if not cid:
        return None
    F = p24_frame(w)
    cd, f, o = F["u"], F["v"], F["o"]
    c0 = CUT_AT[{"W1": 0, "W3": 2}[cid]][2]
    u0 = (c0[0] - o[0]) * cd[0] + (c0[1] - o[1]) * cd[1]  # the cut centre's distance from the window's left edge, m
    return cid, name, c0, cd, f, P24_CUT_INSET_M - u0, F["W"] - P24_LEVEL_MM - u0


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


P24_OVER_WATER = ("subhub", "spill")   # round 5 (G-R5-8): fields IN the water by design, drawn above the stream


def p24_plan(pg, C, w, T, inP, on, k, taken, segs, dw, dh, part="all"):
    """v28 (WO-T4b-3): the window's proposal in the architectural plan language, each element its own symbol and
    texture at true size; returns [(field key, page rings)] for the titles. T7 (30 Oct, M5): ground fields, then the
    paths and crossings, then the trees over them.
    Round 5 (S6): part "fields" = the zone fields, the widened stream and Demeter's Garden, drawn at proj_tint UNDER
    the stream (G-R5-8: water above every tint; widened stream / wetland join the stream's water under it); part
    "rest" = the fields in the water by design (P24_OVER_WATER: sub-hub, spillway), the side arms and everything
    else, above the stream. Every designed outline Chaikin-smoothed (G-R5-9, P24.5); no stripes (G-R5-4.1); the
    trees by the planting placer (G-R5-7, P24.4: p24_tree_set)."""
    ink, ink2, white = COL["ink_dark"], COL["ink2"], COL["white"]
    TP = lambda P: [T(p) for p in P]
    sm = lambda P: chaikin([tuple(p[:2]) for p in P], 3, closed=True) if len(P) >= 3 else list(P)   # G-R5-9
    fields = []
    # ---- fields: wetland (widened stream and flood terraces), terraces, spillway, sub-hub bed, forest walk.
    # v38 closing (G-R4-4, CHK-7): the zone-base zones are clipped to the study area here, at their source, as p21's
    # pl23_prep does (sc_rings_clip, page "p22", the id mp_map_draw counts under); each part is its own field
    st = getattr(C, "study", None) or sc_rings()
    parts_ = []
    for z in C.D.zones:
        key = P24_KEY.get((z["code"], z.get("tier") if z["code"] == "WA" else None))
        if key and len(z["P"]) >= 3:
            parts_ += [(key, dict(z, P=P_)) for P_ in (sc_rings_clip(z["P"], st, u"p22") if st else [list(z["P"])])
                       if len(P_) >= 3]
    for key, z in parts_:
        under = key not in P24_OVER_WATER                 # drawn under the stream (part "fields") or above ("rest")
        if part != "all" and under != (part == "fields"):
            continue
        Q = TP(sm(z["P"]))
        if not on(Q):
            continue
        if key == "wetland":                              # v37 (D2, G8): flat wetland tone, firm edge, no waves
            pg.poly([Q], fill=WET_COL)
            pg.line(Q + Q[:1], _wat_pal()["edge"], 0.25)
        elif key == "terraces":                           # v37 (P22.3): the fields fade into each other (soft
            soft_fill(pg, [Q], R28_ZONE["terraces"][1], 0.18, P24_SOFT_MM)   # edge, no outline)
        elif key == "spill":                              # round 5: solid, no stripes (G-R5-4.1)
            pg.poly([Q], fill=COL["river"], alpha=0.6)
            pg.line(Q + Q[:1], COL["river_dark"], 0.2)
        elif key == "subhub":
            soft_fill(pg, [Q], R28_ZONE["subhub"][1], 0.25, P24_SOFT_MM)
        elif key == "forest":
            soft_fill(pg, [Q], R28_ZONE["forest"][1], 0.15, P24_SOFT_MM)
        elif key == "reed":
            _p24_put(pg, pla_cell_plan("reed", Q, k))         # lined, root-contained cells (D2 a)
        elif key == "demeter":                            # round 5 (P24.7): the designed garden (02g), drawn once
            if not _P24_DG_DONE:
                _P24_DG_DONE.append(1)
                p24_garden(pg, C, k, T, segs, on)
                fields += [("demeter", TP(R_)) for R_ in dg_design(C)["rings"] if on(TP(R_))]
                leg(("p24", "demeter"))
            continue
        if key != "demeter":
            _P24_SP.update(P24_SPECIES.get(key, ()))
        fields.append((key, Q))
        leg(("p24", key))
    if part != "rest":
        for wd in C.widen:
            Q = TP(sm(wd["ring"]))
            if on(Q):
                pg.poly([Q], fill=WET_COL)                # the new bank: under the stream (G-R5-8)
                pg.line(Q + Q[:1], _wat_pal()["edge"], 0.3)
                fields.append(("wetland", Q))
                leg(("p24", "wetland"))
    if part == "fields":
        return fields
    for a in C.arms:                                      # planted side arm (no reed in the open bed, D2 a)
        Q = TP(a["P"])
        if on(Q):
            pg.line(Q, COL["river"], max(1.0, 6.0 * k), alpha=0.8)
            pg.line(Q, COL["river_dark"], 0.15, [0.6, 0.6], cap=0)
            leg(("p24", "arm"))
    # ---- hub squares: paving grid, their planes
    for h in C.hubs:
        for L_ in h.get("square") or []:
            Q = TP(sm(L_))
            if len(Q) >= 3 and on(Q):                     # round 5: solid paving, organic outline (G-R5-4.1, 4.9)
                pg.poly([Q], fill=SQ_FILL, stroke=SQ_EDGE, lw=0.2)
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
            p24_lane_ends(pg, C, _p24_offset(P, sg * (WALK_W + P24_BIKE_W) / 2.0), T, inP, k, taken, segs)
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
    # ---- vegetation over the ground, water and paths (M5 order; G9): the corridor's tree set as on p.21 (v33: rows
    # along the water's edge, one species per row from wet to dry, each at its crown width with its own plan mark),
    # the hub squares' planes
    p24_kit(pg, C, T, inP, k, taken, people=False)        # v37 (P22.3): benches and planters under the crowns
    n_t = 0                                               # round 5 (G-R5-7, P24.4): the planting placer's trees
    for i, (key, x_, y_, cr, I_) in enumerate(p24_tree_set(C, w)):
        if inP((x_, y_)):
            x, y = T((x_, y_))
            _p24_put(pg, pla_plan(key, x, y, k, crown_m=cr, seed=i))
            _P24_SP.add(key)
            n_t += 1
    if n_t:
        leg(("p24", "tree"))
    for p, i in pl23_hub_trees(C):                       # v37 (G8, D7): on land, opaque
        if inP(p):
            x, y = T(p)
            _p24_put(pg, pla_plan("plane", x, y, k, seed=i))
            leg(("p24", "tree"))
            _P24_SP.add("plane")
    p24_kit(pg, C, T, inP, k, taken, people=True)         # v37 (P22.3, G15): the people over everything
    if C.terrace and inP(C.terrace["xy"]):
        x, y = T(C.terrace["xy"])
        p2 = (C.terrace["xy"][0] + C.terrace["dir"][0] * 400.0, C.terrace["xy"][1] + C.terrace["dir"][1] * 400.0)
        pg.line([(x, y), T(p2)], COL["accent"], 0.3, [1.4, 0.8], cap=0, alpha=0.7)
        _p24_put(pg, ico_draw("viewpoint", x, y, 3.2))
        taken.append((x - 1.6, y - 1.6, x + 1.6, y + 1.6))
        leg(("p24", "view"))
    else:                                                 # v38 (P22.4, U64): this window's own viewing terrace
        p24_deck(pg, C, T, inP, k, taken, segs)
    for z in C.D.zones:                                   # round 5: Demeter's Garden draws its own café (02g)
        if z["code"] == "GR" and inP(z["q"]):
            x, y = T(z["q"])
            _p24_put(pg, ico_draw("cafe", x, y, 3.0))
            taken.append((x - 1.5, y - 1.5, x + 1.5, y + 1.5))
            leg(("p24", "cafe"))
    return fields


# ---- v38 (round 4, P22.4, P22.5, P22.8): the garden, the lane's ends, the viewing terrace (design rules, stated)
P24_LEG_SP = ("willow", "tamarisk", "loosestrife", "reed", "ash", "plane", "olive", "chaste", "rosemary", "lavender")
P24_TREE_SET = ("willow", "tamarisk", "ash", "plane")   # the corridor's tree set (pl23_trees_draw, as p.21)
P24_DG_TOL = 2.0             # m: Demeter's Garden's outline simplified to straight edges (FORM: no curves off the water)
P24_DG_HEDGE = 1.5           # m: the rosemary hedge on its border (design value)
P24_DG_PATH = 2.5            # m: the gravel path from the café to the walk (design value)
P24_DG_PLANE = 8.0           # m: the café's two shade planes stand this far either side of it along the garden's axis
P24_LAMP_M = 25.0            # m: a lamp every this many m on the lane's land edge (design rule, as the benches)
P24_BIKE_JOIN_M = 40.0       # m: a lane end joins the nearest street this near (inside the study area), else a rack
P24_RACK = (4, 1.0, 1.6)     # bike rack: stands, spacing m, length m (design values; sf_bike_rack in section)
P24_DECK = (8.0, 4.0)        # m: the viewing terrace's timber deck, along x across (design value)
P24_STREET_D = (-3.0, 25.0)  # m: street elements this far behind / beyond the cut show in its section
_P24_DECK = []               # survey points of the decks the window draws (its section)


def _p24_pin(p, R_):
    """point p inside ring R_ (even-odd)"""
    x, y, ins = p[0], p[1], False
    for (x1, y1), (x2, y2) in zip(R_, R_[1:] + R_[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            ins = not ins
    return ins


def _p24_simplify(R_, tol):
    """ring R_ simplified to straight edges (Douglas-Peucker, tolerance tol in its units)"""
    def dp(P):
        if len(P) < 3:
            return P
        (x1, y1), (x2, y2) = P[0], P[-1]
        L = math.hypot(x2 - x1, y2 - y1) or 1e-9
        ds = [abs((x2 - x1) * (y1 - p[1]) - (x1 - p[0]) * (y2 - y1)) / L for p in P[1:-1]]
        i = max(range(len(ds)), key=lambda j: ds[j]) + 1
        return dp(P[:i + 1])[:-1] + dp(P[i:]) if ds[i - 1] > tol else [P[0], P[-1]]
    if len(R_) < 4:
        return list(R_)
    far = max(range(len(R_)), key=lambda j: (R_[j][0] - R_[0][0]) ** 2 + (R_[j][1] - R_[0][1]) ** 2)
    out = dp(list(R_[:far + 1]))[:-1] + dp(list(R_[far:]) + [R_[0]])[:-1]
    return out if len(out) >= 3 else list(R_)


def _p24_half(R_, a, n):
    """the part of ring R_ on the side n of the line through a (Sutherland-Hodgman)"""
    side = lambda p: (p[0] - a[0]) * n[0] + (p[1] - a[1]) * n[1]
    out = []
    for p, q in zip(R_, R_[1:] + R_[:1]):
        sp, sq = side(p), side(q)
        if sp >= 0.0:
            out.append(p)
        if (sp >= 0.0) != (sq >= 0.0):
            f_ = sp / (sp - sq)
            out.append((p[0] + (q[0] - p[0]) * f_, p[1] + (q[1] - p[1]) * f_))
    return out


def _p24_near(p, lines):
    """(distance, point) of the nearest point on polylines lines to p, or (inf, None)"""
    best = (float("inf"), None)
    for L_ in lines:
        for a, b in zip(L_, L_[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            l2 = dx * dx + dy * dy
            t = 0.0 if l2 < 1e-12 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / l2))
            q = (a[0] + dx * t, a[1] + dy * t)
            d = math.hypot(p[0] - q[0], p[1] - q[1])
            if d < best[0]:
                best = (d, q)
    return best


def _p24_wet(C, p):
    """the masterplan's distance from p to the water, m (None off its grid)"""
    n = C.cell(p)
    return C.Dst[n] if n is not None and C.Dst[n] < 1e8 else None


_P24_DG_DONE = []            # round 5: the garden is drawn once per window (reset in p24_window)
_P24_TREES = {}              # round 5: window id -> the planting placer's trees (survey m), plan and section share them
P24_DG_SEAT = (2.0, 0.6)     # m: a garden seat, length x depth (drawing value, as P24_BENCH)


def p24_garden(pg, C, k, T, segs, on):
    """round 5 (P24.7, P23.7, U64): Demeter's Garden from its ONE design (02g dg_design): the organic outlines
    (garden + the stream terrace that reaches the D2 cut) in the garden tone with a rosemary hedge band inside the
    edge, the olive grove in each garden's landward half (plants module crop, sourced default spacing), the tomato
    rows (the garden's crop; spacing a drawing rule, 02g DG_ROW_M), the café disc with its planes, the gathering
    place on the terrace, seats, the gravel paths (café -> walk, garden -> Üç Kemer Köprüsü), the terrace's edge
    down to the stream. Species only through the plant module (D4 interface)."""
    dg = dg_design(C)
    TP = lambda P: [T(p) for p in P]
    Rs = [TP(R_) for R_ in dg["rings"] if on(TP(R_))]
    if not Rs:
        return False
    for Q in Rs:
        pg.poly([Q], fill=PLA_FIELD, alpha=0.35)
    for R_ in dg["olive"]:
        Q = TP(R_)
        if on(Q):
            _p24_put(pg, pla_crop_plan("olive", Q, k, ang_deg=principal_angle(Q)))
            leg(("p24", "dg_olive"))
            _P24_SP.add("olive")
    n_r = 0
    for P in dg["rows"]:
        Q = TP(P)
        if on(Q):
            pg.line(Q, pla_green("crop"), max(0.25, 0.6 * k), cap=1)   # tomato leaves (plants module crop tone)
            n_r += 1
    if n_r:
        leg(("p24", "dg_rows"))
    for P in dg["paths"]:
        Q = TP(P)
        if on(Q):
            pg.line(Q, COL["ink2"], P24_DG_PATH * k + 0.2, cap=1)
            pg.line(Q, SF_LANE["gravel"], P24_DG_PATH * k, cap=1)
            segs += list(zip(Q, Q[1:]))
            leg(("p24", "dg_path"))
    for P in dg["edge"]:
        Q = TP(P)
        if on(Q):
            pg.line(Q, SCT["stone"], 0.6, cap=1)
            leg(("p24", "dg_edge"))
    for R_ in dg["gather"]:
        Q = TP(R_)
        if on(Q):
            pg.poly([Q], fill=SF_LANE["gravel"], stroke=COL["ink2"], lw=0.15)
            leg(("p24", "dg_gather"))
    for R_ in dg["cafe"]:
        Q = TP(R_)
        if on(Q):
            pg.poly([Q], fill=SF_LANE["walk"], stroke=COL["ink2"], lw=0.15)
            c_ = (sum(p[0] for p in Q) / len(Q), sum(p[1] for p in Q) / len(Q))
            _p24_put(pg, ico_draw("cafe", c_[0], c_[1], 3.0))
            leg(("p24", "cafe"))
    for x_, y_, ang in dg["seats"]:
        u = (math.cos(ang), math.sin(ang))
        Q = TP(_p24_box_along((x_, y_), u, P24_DG_SEAT[0], P24_DG_SEAT[1]))
        if on(Q):
            pg.poly([Q], fill=COL["ink2"])
            leg(("p24", "bench"))
    for i, (key, x_, y_) in enumerate(dg["shade_trees"]):
        x, y = T((x_, y_))
        _p24_put(pg, pla_plan(key, x, y, k, seed=40 + i))
        _P24_SP.add(key)
    for Q in Rs:                                          # the hedge: a band inside the outline, then its edge line
        pg.clip([Q])
        pg.line(Q + Q[:1], pla_colours("rosemary")["fill"], 2.0 * P24_DG_HEDGE * k, cap=1)
        pg.unclip()
        pg.line(Q + Q[:1], COL["ink2"], 0.25)
        segs += list(zip(Q, Q[1:] + Q[:1]))
    leg(("p24", "dg_hedge"))
    _P24_SP.add("rosemary")
    return True


def p24_tree_set(C, w):
    """round 5 (G-R5-7, P24.4, U61 "trees by the plan"): the window's trees from the ONE planting placer (S4
    common/planting.py pln_place), survey m: project = the study area inside the turned window; cores = the designed
    fields there (forest corridor, rain terraces, Demeter's Garden, wetland, hub squares; dense, mixed, fading
    outward, no grid, no alternation, nothing outside the project); water = the plans' water rings (no tree on
    water); avoided: the hub squares' paving, the walk + bike lane; kept only on open ground of the masterplan's grid
    (no tree on a building or a road). Cached per window: the plan and its section show the same trees.
    Returns [(key, x, y, crown_m, I)]."""
    got = _P24_TREES.get(w["id"])
    if got is not None:
        return got
    F = p24_frame(w)
    st = getattr(C, "study", None) or sc_rings()
    proj = []
    for S_ in st or ():
        proj += [r_ for r_ in sc_rings_clip(F["ring"], [S_]) if len(r_) >= 3]
    if not proj:
        proj = [list(F["ring"])]
    inR = lambda P: any(F["R"][0] - 50 <= p[0] <= F["R"][2] + 50 and F["R"][1] - 50 <= p[1] <= F["R"][3] + 50
                        for p in P)
    cores = [list(z["P"]) for z in C.D.zones if P24_KEY.get((z["code"], z.get("tier") if z["code"] == "WA" else None))
             in ("forest", "terraces", "wetland") and len(z["P"]) >= 3 and inR(z["P"])]
    cores += [R_ for R_ in dg_design(C)["rings"] if inR(R_)]
    sq = [list(L_) for h in C.hubs for L_ in (h.get("square") or []) if len(L_) >= 3 and inR(L_)]
    avoid = list(sq)
    lw_ = WALK_W + (P24_BIKE_W if P24_BIKE else 0.0)
    for P in C.canopy:
        if len(P) >= 2 and inR(P):
            avoid.append(_p24_offset(P, lw_ / 2.0 + 0.5) + list(reversed(_p24_offset(P, -lw_ / 2.0 - 0.5))))
    avoid += [list(R_) for R_ in dg_design(C)["cafe"] + dg_design(C)["gather"]]
    placed = pln_place(proj, cores=cores + sq, outer=(), water=pl23_wet_rings(C), k=1.0, seed=P24_SEED,
                       avoid=avoid, page=u"p22 " + w["id"], shrubs=False)
    out = []
    for key, x, y, cr, I_ in placed.get("trees") or []:
        n = C.cell((x, y))
        if n is not None and C.F[n] != 0:
            continue                                      # a building or a road cell of the masterplan grid
        out.append((key, x, y, cr, I_))
    _P24_TREES[w["id"]] = out
    return out


def p24_lane_ends(pg, C, B, T, inP, k, taken, segs):
    """v38 (round 4, P22.4, U47(3) "bisiklet yolu neden bir anda kesiliyor"): the bike lane B (survey m) never stops in
    the open: each end inside the window joins the nearest street within P24_BIKE_JOIN_M inside the study area (the
    lane drawn on to it, bollards across the join), else ends at a bike rack (P24_RACK) drawn at true size."""
    streets = [L_ for L_ in list(C.roads) + [rd["xy"] for rd in ROADS] if len(L_) >= 2]
    ins = getattr(C, "in_study", None)
    white = COL["white"]
    for e, nb in ((B[0], B[1]), (B[-1], B[-2])):
        if not inP(e):
            continue                                      # it runs on beyond the window
        d, q = _p24_near(e, streets)
        if q is not None and d <= P24_BIKE_JOIN_M and (ins is None or ins(q, 0.0)):
            if d > 0.5:
                J = [T(e), T(q)]
                pg.line(J, P24_BIKE_COL, P24_BIKE_W * k, cap=0, alpha=0.55)
                pg.line(J, white, 0.12, [1.0, 1.0], cap=0)
                segs.append((J[0], J[1]))
            ux, uy = (q[0] - e[0]) / (d or 1.0), (q[1] - e[1]) / (d or 1.0)
            if d <= 0.5:
                L = math.hypot(e[0] - nb[0], e[1] - nb[1]) or 1.0
                ux, uy = (e[0] - nb[0]) / L, (e[1] - nb[1]) / L
            for i in (-1, 0, 1):                          # three bollards across the lane at the street
                b_ = (q[0] - uy * i * 0.8, q[1] + ux * i * 0.8)
                x, y = T(b_)
                pg.circle(x, y, 0.3, fill=COL["ink2"])
                taken.append((x - 0.4, y - 0.4, x + 0.4, y + 0.4))
            _P24_STREET["bollard"].append(q)
            leg(("p24", "bollard"))
        else:
            L = math.hypot(e[0] - nb[0], e[1] - nb[1]) or 1.0
            ux, uy = (e[0] - nb[0]) / L, (e[1] - nb[1]) / L
            n_, sp, ln = P24_RACK
            for i in range(n_):
                c_ = (e[0] - ux * i * sp, e[1] - uy * i * sp)
                A_ = T((c_[0] - uy * ln / 2.0, c_[1] + ux * ln / 2.0))
                B_ = T((c_[0] + uy * ln / 2.0, c_[1] - ux * ln / 2.0))
                pg.line([A_, B_], COL["ink_dark"], 0.25, cap=1)
                taken.append(bbox([A_, B_]))
            _P24_STREET["rack"].append(e)
            leg(("p24", "rack"))


def p24_deck(pg, C, T, inP, k, taken, segs):
    """v38 (round 4, P22.4, U64 "izleme terası"): the window's own viewing terrace when the corridor's (C.terrace)
    lies outside it: a P24_DECK timber deck on the walk's water side where the walk inside the window (and the study
    area) comes closest to the water, with its viewpoint and a sightline across the water."""
    ins = getattr(C, "in_study", None)
    best = None
    for P in C.canopy:
        if len(P) < 2:
            continue
        s = arclen(P)
        sg = _p24_land_side(C, P)
        t = 4.0
        while t < s[-1] - 4.0:
            p, u = at_len(P, s, t)
            dw_ = _p24_wet(C, p)
            if inP(p) and dw_ is not None and (best is None or dw_ < best[0]):
                off = -sg * (WALK_W / 2.0 + P24_DECK[1] / 2.0)
                c_ = (p[0] - u[1] * off, p[1] + u[0] * off)
                if inP(c_) and (ins is None or ins(c_, 0.0)):
                    best = (dw_, c_, u, (-u[1] * -sg, u[0] * -sg))
            t += 5.0
    if best is None:
        return False
    _d, c_, u, wdir = best
    Q = [T(q) for q in _p24_box_along(c_, u, P24_DECK[0], P24_DECK[1])]
    pg.poly([Q], fill=SF_LANE["timber"], stroke=COL["ink"], lw=0.2)
    x, y = T(c_)
    p2 = (c_[0] + wdir[0] * 30.0, c_[1] + wdir[1] * 30.0)
    pg.line([(x, y), T(p2)], COL["accent"], 0.3, [1.4, 0.8], cap=0, alpha=0.7)
    _p24_put(pg, ico_draw("viewpoint", x, y, 3.2))
    taken.append(bbox(Q))
    taken.append((x - 1.6, y - 1.6, x + 1.6, y + 1.6))
    segs += list(zip(Q, Q[1:] + Q[:1]))
    _P24_DECK.append(c_)
    leg(("p24", "deck"))
    leg(("p24", "view"))
    return True


P24_SOFT_MM = 1.2            # v37 (P22.3): the soft edge of a field at 1:1,000, mm (fields fade into each other)
P24_BENCH_M = 25.0           # v37 (P22.3, G10): a bench on the walk's water side every this many m (design rule: a
#                              seat in the shade between the hubs), a lavender planter half way between two benches
P24_BENCH = (2.0, 0.6)       # bench length x depth, m (drawing value, as sf_bench's seat)
P24_PLANTER = (4.0, 1.2)     # planter length x depth, m (drawing value)
P24_WALKER_M = 18.0          # v37 (G15): a walker about every this many m of walk, a cyclist every P24_RIDER_M
P24_RIDER_M = 45.0
P24_PEOPLE_IN = {"hub": (("stand", "sit", "watch", "adult_child"), 5), "terraces": (("sit_step", "watch"), 3),
                 "demeter": (("walk", "stand"), 2)}   # poses, how many per field; none on the sub-hub: the plan
#                              shows the stream at average flow there (checklist 11: nobody in a water-filled channel)
P24_SEED = 2410


def _p24_dry(C, p):
    """v37: survey point p lies on land (in no water ring the plans draw: pl23_wet_rings)"""
    return not any(pip(p[0], p[1], R_) for R_ in pl23_wet_rings(C))


def _p24_box_along(p, u, L, D):
    """a ring L x D m centred on survey point p, its length along the unit vector u"""
    nx_, ny_ = -u[1], u[0]
    hl, hd = L / 2.0, D / 2.0
    return [(p[0] + u[0] * a + nx_ * b, p[1] + u[1] * a + ny_ * b) for a, b in ((-hl, -hd), (hl, -hd), (hl, hd), (-hl, hd))]


def p24_kit(pg, C, T, inP, k, taken, people=False):
    """v37 (round 3, P22.3 "real detail at 1:1,000", G10, G15): on the window's plan, people=False: a bench on the
    walk's water side every P24_BENCH_M and a lavender planter half way between two (the walk's own line, C.canopy);
    people=True: people seen from above doing what each place is for: walkers along the walk, cyclists on the bike
    lane, people standing and sitting on the hub squares, sitting on the terrace steps, walking in Demeter's Garden. Nothing on water (_p24_dry). Seeded: the same every press."""
    rnd = random.Random(P24_SEED + (7 if people else 0))
    ink2 = COL["ink2"]
    lav = pla_colour("lavender")["fill"]
    n_b = n_p = n_f = 0
    for j, P in enumerate(C.canopy):
        if len(P) < 2:
            continue
        sg = _p24_land_side(C, P)
        s = arclen(P)
        if not people:
            wat = _p24_offset(P, -sg * (WALK_W / 2.0 + 0.2 + P24_BENCH[1] / 2.0))
            sw_ = arclen(wat)
            t = P24_BENCH_M / 2.0
            while t < sw_[-1]:
                for tt, (Lm, Dm), kind in ((t, P24_BENCH, "bench"), (t + P24_BENCH_M / 2.0, P24_PLANTER, "planter")):
                    if tt >= sw_[-1]:
                        continue
                    p, u = at_len(wat, sw_, tt)
                    if not inP(p) or not _p24_dry(C, p):
                        continue
                    Q = [T(q) for q in _p24_box_along(p, u, Lm, Dm)]
                    if kind == "bench":
                        pg.poly([Q], fill=COL["ink2"], stroke=None)
                        n_b += 1
                    else:
                        pg.poly([Q], fill=lav, stroke=ink2, lw=0.12)
                        n_p += 1
                    taken.append(bbox(Q))
                t += P24_BENCH_M
            lamp = _p24_offset(P, sg * (WALK_W / 2.0 + (P24_BIKE_W if P24_BIKE else 0.0) + 0.6))   # v38 (P22.8):
            sl_ = arclen(lamp)                            # lamps on the lane's land edge every P24_LAMP_M
            t = P24_LAMP_M / 4.0
            while t < sl_[-1]:
                p, u = at_len(lamp, sl_, t)
                if inP(p) and _p24_dry(C, p):
                    x, y = T(p)
                    pg.circle(x, y, 1.0, stroke=COL["ink2"], lw=0.08)
                    pg.circle(x, y, 0.45, fill=COL["ink_dark"])
                    _P24_STREET["lamp"].append(p)
                    taken.append((x - 1.0, y - 1.0, x + 1.0, y + 1.0))
                t += P24_LAMP_M
            continue
        t = rnd.uniform(2.0, P24_WALKER_M)               # walkers on the walk, both ways, a little off its middle
        while t < s[-1]:
            p, u = at_len(P, s, t)
            q = (p[0] - u[1] * rnd.uniform(-0.7, 0.7), p[1] + u[0] * rnd.uniform(-0.7, 0.7))
            if inP(q) and _p24_dry(C, q):
                ang = math.atan2(u[1], u[0]) - _P24_ROT[0] + (math.pi if rnd.random() < 0.5 else 0.0)
                x, y = T(q)
                _p24_put(pg, fig_top("walk" if rnd.random() < 0.8 else "adult_child", x, y, k, ang=ang, mm_per_m=k,
                                     pick=rnd.randint(0, 3)))
                n_f += 1
            t += P24_WALKER_M * rnd.uniform(0.7, 1.3)
        if P24_BIKE:                                     # cyclists on the bike lane (its land side)
            B = _p24_offset(P, sg * (WALK_W + P24_BIKE_W) / 2.0)
            sb = arclen(B)
            t = rnd.uniform(5.0, P24_RIDER_M)
            while t < sb[-1]:
                p, u = at_len(B, sb, t)
                if inP(p) and _p24_dry(C, p):
                    x, y = T(p)
                    ang = math.atan2(u[1], u[0]) - _P24_ROT[0] + (math.pi if rnd.random() < 0.5 else 0.0)
                    _p24_put(pg, fig_top("bike", x, y, k, ang=ang, mm_per_m=k))
                    n_f += 1
                t += P24_RIDER_M * rnd.uniform(0.7, 1.3)
    if people:                                           # the places: hub squares, terraces, garden, sub-hub
        rings = [("hub", L_) for h in C.hubs for L_ in (h.get("square") or []) if len(L_) >= 3]
        for z in C.D.zones:
            key = P24_KEY.get((z["code"], z.get("tier") if z["code"] == "WA" else None))
            if key in P24_PEOPLE_IN and key != "hub" and len(z["P"]) >= 3:
                rings.append((key, z["P"]))
        for key, Rg in rings:
            if not any(inP(p) for p in Rg):
                continue
            poses, n = P24_PEOPLE_IN[key]
            Q = [T(p) for p in Rg]
            spots = inside_spots(Q, 10)[1:]
            rnd.shuffle(spots)
            got = 0
            for x, y in spots:
                if got >= n:
                    break
                wp = (Rg[0][0] + (x - Q[0][0]) / k, Rg[0][1] + (y - Q[0][1]) / k)   # back to survey m (T: shift + k)
                if not inP(wp) or not _p24_dry(C, wp):
                    continue
                _p24_put(pg, fig_top(poses[got % len(poses)], x, y, k, ang=rnd.uniform(0.0, 2.0 * math.pi),
                                     mm_per_m=k, pick=rnd.randint(0, 3)))
                got += 1
                n_f += 1
    if _P24_STREET["lamp"] and not people:
        leg(("p24", "lamp"))
    if n_b:
        leg(("p24", "bench"))
    if n_p:
        leg(("p24", "planter"))
    if n_f:
        leg(("p24", "people"))
    return n_b, n_p, n_f


# ---- T7 (30 Oct, booklet p22): a reason for every element (G10) and the page's key map (M4) ---------------------
P24_KEYMAP_IN = "dt_k5"      # the window whose plan carries the page's key map (drawn last: it knows both windows)
P24_KM_W, P24_KM_HMAX = 62.0, 40.0   # mm: the key map inset (v38, P22.3: bigger, 58 x 36 -> 62 x 40)
_P24_WINS = {}               # window id -> (section name, the turned window's corners, survey m), filled as drawn
# v38 (round 4, P22.1, G-R4-3): one column per window and style on the booklet page (design values, mm)
P24_PANEL_H = 236.0          # the column (= the booklet crop): both columns share top and bottom (booklet body 243 mm)
P24_TITLE_H = 7.0            # its title strip: the window's title, the scale bar, the north arrow
P24_GAP = 3.0                # between plan and section, and above the legend
P24_SCALE_ROW = 6.0          # the section's scale bar and title row under its key
P24_UNIT_GAP = 8.0           # between the style b and style a columns on the sheet (not on the booklet page)
P24_LEG_PITCH = 3.3          # legend row pitch (7 pt text)
P24_LEG_COLS = 3
P24_TP_PAD = 0.2             # the p22 TextPages' clearance between words, mm (below the placers' 0.3-0.6 mm)
_P24_ROT = [0.0]             # the turned window's page x axis as a survey angle, rad (survey angle - this = page angle)
_P24_SP = set()              # the plant species the window draws (its planting legend)
_P24_STREET = {"lamp": [], "rack": [], "bollard": []}   # survey points of the window's street elements (its section)


def p24_north(sh, x, y, ang):
    """v38 (G-R4-9): the shared north arrow (no plate) with its foot at (x, y), turned by ang (rad, CCW from up)"""
    def fill_fn(rings, hx, al, nonzero=False):
        sh.poly([R_ for R_ in rings if len(R_) >= 3], fill=hx)

    def line_fn(pts, hx, lw, dash, al):
        sh.line(pts, hx, lw, list(dash) if dash else None)

    def text_fn(t_, xy, size, hx, bold, align):
        al = align[-1] if align and align[-1] in "LCR" else "C"
        dy = -0.36 * size if align and align[0] == "M" else (-size if align and align[0] == "T" else 0.0)
        sh.text(t_, xy[0], xy[1] + dy, size, hx, bold=bold, align=al)
    basemap_draw(north_items(x, y, ang, size_mm=3.8, colour=COL["ink_dark"]), lambda p: p, fill_fn, line_fn, text_fn)


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
             if cid else u"Q500 stays in the banks at the {} cut".format(bridge_name("K5", short=True)))
        return q + u" · café"
    if key == "subhub":
        return u"a place in the bed for the dry months · shut in floods"
    if key == "hub":
        return u"a dry square at the bridge · plane shade"
    return None


def p24_window(ix, page, C, w, missing, warn):
    """round 5 (S6, G-R5-12; replaces r28_window_panel's sheet): window w as items: its 1:1,000 plan (turned so its
    cut runs left -> right, p24_frame; drawing units = the turned frame's metres, north_deg), its section D1-D1′ /
    D2-D2′ (x = m along the cut, t = 0 at the stream's centre; y = m a.s.l.), the section's walk inset (the same
    geometry drawn again at its own scale, G-R5-5), level markers (S3 sf_level_items), zone names and field titles
    as anchored labels, the water route and the callouts as numbered lists with anchors, the legend by group. Draw
    order (G-R5-8): base -> D9 tint + the zone fields (proj_tint) -> the stream (proj_water) -> the fields in the
    water by design + everything else (proj_lines) -> study -> marks. Returns log lines."""
    out = []
    F = p24_frame(w)
    R, o_, u_, v_ = F["R"], F["o"], F["u"], F["v"]
    k = 1000.0 / DT_SCALE
    dw, dh = F["W"] * k, F["H"] * k
    _P24_ROT[0] = math.atan2(u_[1], u_[0])

    def T(p):
        x, y = p[0] - o_[0], p[1] - o_[1]
        return ((x * u_[0] + y * u_[1]) * k, (x * v_[0] + y * v_[1]) * k)

    def inP(p):
        x, y = p[0] - o_[0], p[1] - o_[1]
        a, b = x * u_[0] + y * u_[1], x * v_[0] + y * v_[1]
        return 0.0 <= a <= F["W"] and 0.0 <= b <= F["H"]
    on = lambda Q: hit(bbox(Q), (0.0, 0.0, dw, dh))
    _PLEG[0] = {}
    del _P24_LAB[:]
    _P24_SP.clear()
    del _P24_DECK[:]
    del _P24_DG_DONE[:]
    for k_ in _P24_STREET:
        del _P24_STREET[k_][:]
    cname = P24_CUTS.get(w["id"], (None, w["id"]))[1] or w["id"]
    _P24_WINS[w["id"]] = (cname, F["ring"])
    pg = Page(dw, dh)
    pg.text_page(u"p22 " + cname + u" plan", pad=P24_TP_PAD)
    taken, segs, ts = [], [], R28DT_TS
    ink, ink1, ink2 = COL["ink_dark"], COL["ink"], COL["ink2"]
    study = getattr(C, "study", None) or sc_rings()
    fields = []
    foot = [z["P"] for z in C.D.zones if P24_KEY.get((z["code"], z.get("tier") if z["code"] == "WA" else None))
            and len(z["P"]) >= 3] + [wd["ring"] for wd in C.widen] + \
        [L_ for h in C.hubs for L_ in (h.get("square") or []) if len(L_) >= 3]
    base = ml_base(R, DT_SCALE, contours=True, override={"stream": False})   # the masterplan draws its own stream
    if base:
        for k_ in ("bld", "street", "contour"):
            leg(("r28dt", k_))
    mp_map_draw(pg, page, T, base, steps={
        "proj_tint": lambda: fields.extend(p24_plan(pg, C, w, T, inP, on, k, taken, segs, dw, dh, part="fields")),
        "proj_water": lambda: _r28_base(pg, C, T, R, segs, k),
        "proj_lines": lambda: fields.extend(p24_plan(pg, C, w, T, inP, on, k, taken, segs, dw, dh, part="rest"))},
        tint=ml_tint(foot, study=study, page=page), study=study)
    if foot:
        leg(("p24", "tint"))
    # ---- the water route (P24.2): the zone base's water links in the route's order; numbers on the map, the words
    # in a numbered list (G-R5-12)
    rc = R28DT_ROUTE
    steps, shapes = [], C.D.zones + C.D.strips
    for L in C.D.links:
        if L["kind"] != "water" or len(L["P"]) < 2 or not any(inP(p) for p in L["P"]):
            continue
        a, b = link_shapes(L, shapes)
        ab = (a["code"] if a and a in C.D.zones else None, b["code"] if b and b in C.D.zones else None)
        steps.append((next((i for i, st in enumerate(ROUTE) if st[0] == ab), len(ROUTE)), L, a, b))
    steps.sort(key=lambda s_: s_[0])
    route_rows = []
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
        mp_marker(pg, P[0][0], P[0][1], str(n_), rc, size_pt=ts["small"] / PT, r_min=1.9, name=u"route %d" % n_)
        route_rows.append((u"".join(t_ for t_, _bd in _r28_route_runs(order, L, a, b)), P[0]))
        leg(("r28dt", "route"))
    for A in study or ():
        if on([T(p) for p in A]):
            leg(("r28dt", "study"))
    sp_ = p24_cut_span(w)                                  # ---- the section's line: thin and muted (D6, P24.2)
    if sp_ is not None:
        cid, name, c0, cd, f, ta, tb = sp_
        A_ = T((c0[0] + cd[0] * ta, c0[1] + cd[1] * ta))
        B_ = T((c0[0] + cd[0] * tb, c0[1] + cd[1] * tb))
        pg.line([A_, B_], KM_CUT_PLAN["colour"], KM_CUT_PLAN["lw"], list(KM_CUT_PLAN["dash"]), cap=0)
        for (x, y), nm, al in ((A_, name, "R"), (B_, name + u"′", "L")):
            pg.text(nm, x + (-0.6 if al == "R" else 0.6), y - KM_CUT_PLAN["text_mm"] * 0.36, KM_CUT_PLAN["text_mm"],
                    KM_CUT_PLAN["colour"], bold=True, align=al)
        leg(("p24", "cut"))
    # ---- words as anchored labels (the booklet places them, G-R5-12): place names, one title per field (its reason
    # goes to the "why" list), small words
    names = [(HUB_NAME[h["id"]], h["xy"]) for h in C.hubs] + \
        [(bridge_name(nm), xy) for nm, xy in BRIDGES_K if nm in (u"K1", u"K2")] + PLACES
    for nm, xy in names:
        if inP(xy):
            x, y = T(xy)
            pg.text(nm, x, y, ts["place"], ink1, bold=True, align="C")
    best = {}
    for key, Q in fields:
        vis = clip_ring(Q, (0.0, 0.0, dw, dh))
        if len(vis) >= 3 and abs(area2(vis)) >= R28DT_TITLE_MM2 and abs(area2(vis)) > abs(area2(best.get(key, [(0, 0)] * 3))):
            best[key] = vis
    fpts = [T(p) for p in C.forest if inP(p)]
    why_rows = []
    for key in R28DT_ORDER + ("spill",):
        if key not in best and not (key == "forest" and fpts):
            continue
        nm = R28_ZONE[key][0] if key in R28_ZONE else P24_NAME[key].capitalize()
        at = inner_pt(best[key]) if key in best else sorted(fpts)[len(fpts) // 2]
        pg.text(nm, at[0], at[1], ts["zone"], ink, bold=True, align="C")
        rs = p24_reason(C, key, w)
        if rs:
            why_rows.append((nm[:1].upper() + nm[1:].lower() + u": " + rs, at))
    words = []
    for z in C.D.zones:
        if z["code"] == "WT":
            words.append((u"clean-water classroom", z["q"]))
    words += [(u"footbridge", c_["xy"]) for c_ in C.cross if c_["kind"] == "footbridge"]
    words += [(u"stepping stones", c_["xy"]) for c_ in C.cross if c_["kind"] == "stepping stones"]
    if C.terrace:
        words.append((u"viewing terrace", C.terrace["xy"]))
    words += [(u"step to the water", PLACES[1][1]), (u"deck on the Roman bank wall", ROMAN_WALL),
              (u"workshops", CRAFT_XY)]
    dg = dg_design(C)
    for nm_, Rl in ((u"café", dg["cafe"]), (u"gathering place", dg["gather"])):
        words += [(nm_, (sum(p[0] for p in R_) / len(R_), sum(p[1] for p in R_) / len(R_))) for R_ in Rl]
    words += [(u"tomato rows", R_[len(R_) // 2]) for R_ in dg["terrace"]]
    for rd in ROADS:
        if rd["change"] in ("pedestrian", "calmed", "shared"):
            P = rd["xy"]
            words.append((rd["change"] + (u" bridge" if u"Köprü" in rd["name"] else u" street"),
                          at_len(P, arclen(P), arclen(P)[-1] / 2.0)[0]))
    for s_, xy in words:
        if inP(xy):
            x, y = T(xy)
            pg.text(s_, x, y, ts["small"], ink2, align="C")
    # ---- the plan as a drawing (turned frame m; north_deg = north's turn from page-up, counter-clockwise)
    did = u"mp_dt_" + w["id"]
    D = mpx_drawing(ix, did, page, pg, (0.0, 0.0, dw, dh), DT_SCALE, origin_m=(0.0, 0.0), dkind="plan",
                    north_deg=round(math.degrees(F["north"]), 2), scale_pref=[int(DT_SCALE)], priority=1, group=did,
                    title=w["title"])
    MPX_PAGES.append(("A", u"p24 " + w["id"], pg))
    ix.text(page, w["title"], "heading", priority=3, group=did)
    if sp_ is not None:
        ix.anchor(D, name, (A_[0] / k, A_[1] / k))
        ix.anchor(D, name + u"′", (B_[0] / k, B_[1] / k))
    if route_rows:
        ix.list(page, did, [t_ for t_, _p in route_rows], numbered=True, anchors=[(p_[0] / k, p_[1] / k)
                                                                                  for _t, p_ in route_rows],
                id=did + u"_route", group=did)
        ix.text(page, u"Water route · collect, clean, give back", "heading", priority=4, group=did)
    if why_rows:
        ix.list(page, did, [t_ for t_, _p in why_rows], numbered=False, anchors=[(p_[0] / k, p_[1] / k)
                                                                                 for _t, p_ in why_rows],
                id=did + u"_why", group=did)
    # ---- the section, its levels, zone names, callouts and walk inset
    sec = p24_section(C, w, warn, "b", ex={})
    if sec is not None:
        for k_ in sec["keys"]:
            leg(("p24s", k_))
        missing += sec["missing"]
        sid = did + u"_sec"
        Ds = mpx_drawing(ix, sid, page, sec["pg"], (0.0, 0.0, sec["w"], sec["top"]), DT_SCALE,
                         origin_m=(sec["ta"], sec["z0"]), dkind="section", scale_pref=[int(DT_SCALE)], priority=1,
                         group=did, title=u"Section {0}-{0}′".format(sec["name"]))
        MPX_PAGES.append(("A", u"p24 " + w["id"] + u" section", sec["pg"]))
        ix.text(page, u"Section {0}-{0}′ · looking upstream".format(sec["name"]), "heading", priority=3,
                group=did)
        sf_level_items(ix, page, Ds, sec["levels"])
        for nm, t, zz, beyond in sec["zones"]:
            ix.text(page, nm, "label", drawing=sid, at=(t, zz), colour=COL["ink2"] if beyond else COL["ink_dark"],
                    bold=not beyond, group=did, priority=4)
        rows, seen_ = [], set()
        for n_, t, zz, t_ in sorted(sec["callouts"]):
            if n_ not in seen_:
                seen_.add(n_)
                rows.append((t_, (t, zz)))
        if rows:
            ix.list(page, sid, [t_ for t_, _a in rows], numbered=True, anchors=[a_ for _t, a_ in rows],
                    id=sid + u"_key", group=did)
        out += p24_inset(ix, page, C, w, sec, sid, did)
    # ---- the legend, by group (only what this window's plan and section draw)
    grp, cur = [], None
    for r_ in p24_legend(dict(_PLEG[0])):
        if r_[0] == "head":
            cur = [r_[1], []]
            grp.append(cur)
        elif cur is not None:
            cur[1].append((dict(kind=P24_LEG_KIND.get(r_[0], "fill"), colour=r_[1]), r_[2]))
    for i, (head, ents) in enumerate(grp):
        if ents:
            ix.legend(page, did, ents, title=head, id=u"%s_leg%d" % (did, i + 1), group=did)
    _PLEG[0] = None
    out.append(u"p24 {}: plan {}, section {}, fields {}, route steps {}, trees {}".format(
        w["id"], did, (did + u"_sec") if sec is not None else u"none", len(fields), len(route_rows),
        len(_P24_TREES.get(w["id"]) or ())))
    return out


def p24_inset(ix, page, C, w, sec, sid, did):
    """round 5 (G-R5-5, S3 sf_inset_frame): the walk (or the hub square) nearest the stream as its OWN drawing at
    its own scale: the section drawn again at the inset's 1:den (same geometry, details on at 1:250 and larger),
    framed on the walk's people and surface (P24_ZOOM_SPOT); an inset never skipped silently (WARNING)."""
    walks, runs = sec["walks"], sec["runs"]
    wm, hm_, dn = P24_ZOOM_SPOT
    if walks:
        t, zw, sg = min(walks, key=lambda w_: abs(w_[0]))
        t += sg * (P24_BIKE_W / 2.0 if P24_BIKE else 0.0)
    else:
        hub = [r_ for r_ in runs if r_[0] == "hub"]
        if not hub:
            ix.warn(page, "inset", u"%s: no walk or hub square on the cut: no inset" % sec["name"])
            return []
        t = (hub[0][1] + hub[0][2]) / 2.0
        zw = sec["S"].gnd(t)
    focus = [(t - wm / 2.0, zw - dn, t + wm / 2.0, zw - dn + hm_)]
    fr = sf_inset_frame(focus, DT_SCALE, page=page, label=sec["name"] + u" walk")
    if not fr:
        return []
    ex2 = p24_section(C, w, [], "b", den=fr["den"], ex={})
    if ex2 is None:
        return []
    k2, wx0, wy0, wx1, wy1 = ex2["k"], fr["window"][0], fr["window"][1], fr["window"][2], fr["window"][3]
    cid_ = sid + u"_zoom"
    box = ((wx0 - ex2["ta"]) * k2, (wy0 - ex2["z0"]) * k2, (wx1 - ex2["ta"]) * k2, (wy1 - ex2["z0"]) * k2)
    mpx_drawing(ix, cid_, page, ex2["pg"], box, fr["den"], origin_m=(wx0, wy0), dkind="section",
                scale_pref=[int(fr["den"])], priority=2, group=did, labels=False)
    ix.inset(page, sid, list(fr["window"]), cid_, DT_SCALE / float(fr["den"]), id=cid_ + u"_inset")
    return [u"p24 {} inset 1:{:.0f} of 1:{:.0f} (x {:.0f}), window {:.1f} x {:.1f} m".format(
        sec["name"], fr["den"], DT_SCALE, DT_SCALE / float(fr["den"]), wx1 - wx0, wy1 - wy0)]


def p24_items(ix, C, wins, areas, missing, warn):
    """round 5 (S6, G-R5-12): booklet p24 (item page MPX_PAGE["p24"]) = both 1:1,000 windows (plan + section +
    inset + lists + legend each) and ONE key map of both windows and their cuts (S2 km_map, placed by the booklet in
    the right column, never on a plan: P24.1). missing = {window id: [words not placed]}. Returns log lines."""
    page = MPX_PAGE["p24"]
    out = []
    _P24_WINS.clear()
    _P24_TREES.clear()
    for w in wins:
        out += p24_window(ix, page, C, w, missing.setdefault(w["id"], []), warn)
    zooms = dict((nm, ring) for nm, ring in _P24_WINS.values())
    ids = [P24_CUTS[b][0] for b in sorted(_P24_WINS) if b in P24_CUTS] + sorted(zooms)
    try:
        km = km_map(ids, P24_KM_BOX[0], P24_KM_BOX[1], zooms=zooms, page=page)
        if km.get("items"):
            mpx_keymap(ix, page, km, item_id=u"mp_dt_keymap")
            out.append(u"p24 key map: cuts {}, windows {}".format(u", ".join(ids[:2]), len(zooms)))
        else:
            ix.warn(page, "keymap", u"no base map data (run the site board first): key map not exported")
    except Exception as ex_:
        ix.warn(page, "keymap", u"key map not exported (%s: %s)" % (type(ex_).__name__, ex_))
    ix.text(page, u"The water edge at 1:1,000", "title", priority=1, group=u"mp_dt")
    out += pln_log_lines(page) if "pln_log_lines" in globals() else []
    return out


def _p24_sp_label(key):
    sp = PLA_SPECIES.get(key) or {}
    nm = sp.get("name") or key
    return nm + (u" · " + sp["turkish"] if sp.get("turkish") else u"")   # D5: the Turkish name beside the species


def p24_legend(keys):
    """v38 (round 4, P22.5, P22.7; replaces r28_crop_legend): the column's legend, only what its plan and section
    draw, in three groups: Planting (one sample per species in its own colour, D5 Turkish name beside it), Design,
    Section. Rows: ("head", text) or (kind, colour, label)."""
    cl = _r28_base_cols()
    out = []
    sp = [k_ for k_ in P24_LEG_SP if k_ in _P24_SP]
    if sp:
        out.append(("head", u"Planting"))
        out += [("tree" if PLA_SPECIES.get(k_, {}).get("layer") == "tree" else "dot", pla_colours(k_)["fill"],
                 _p24_sp_label(k_)) for k_ in sp]
        if ("p24", "dg_olive") in keys:
            out.append(("fill", PLA_FIELD, u"Olive grove"))
    design = ((("p24", "tint"), "fill", ML_TINT, u"What we change (light tint)"),
              (("p24", "reed"), "fill", PLA_WET, u"Reed basins in lined cells"),
              (("p24", "terraces"), "fill", R28_ZONE["terraces"][1], u"Rain terraces"),
              (("p24", "terr"), "line", R28_ZONE["terraces"][1], u"Terrace edge, ticks downhill"),
              (("p24", "spill"), "fill", COL["river"], u"Spillway"),
              (("p24", "wetland"), "fill", WET_COL, u"Widened stream · wetland"),
              (("p24", "arm"), "line", COL["river"], u"Planted side arm"),
              (("p24", "subhub"), "fill", R28_ZONE["subhub"][1], u"Sub-hub in the bed"),
              (("p24", "forest"), "fill", R28_ZONE["forest"][1], u"Forest corridor"),
              (("p24", "dg_hedge"), "line", pla_colours("rosemary")["fill"], u"Garden hedge, rosemary"),
              (("p24", "dg_beds"), "fill", pla_colours("lavender")["fill"], u"Garden beds, mixed shrubs"),
              (("p24", "demeter"), "fill", PLA_FIELD, u"Demeter's Garden"),
              (("p24", "dg_rows"), "line", pla_green("crop"), u"Tomato rows"),
              (("p24", "dg_edge"), "line", SCT["stone"], u"Garden edge to the stream, stone"),
              (("p24", "dg_gather"), "fill", SF_LANE["gravel"], u"Gathering place"),
              (("p24", "dg_path"), "line", SF_LANE["gravel"], u"Gravel path"),
              (("p24", "hub"), "fill", SQ_FILL, u"Hub square, paved"),
              (("p24", "cafe"), "dot", R28_ZONE["cafe"][1], u"Café"),
              (("p24", "walk"), "line", COL["ink2"], u"Riverside walk"),
              (("p24", "bike"), "line", P24_BIKE_COL, u"Bike lane"),
              (("p24", "rack"), "line", COL["ink_dark"], u"Bike racks at the lane's end"),
              (("p24", "lamp"), "dot", COL["ink_dark"], u"Lamp"),
              (("p24", "bollard"), "dot", COL["ink2"], u"Bollards where the lane meets a street"),
              (("p24", "deck"), "fill", SF_LANE["timber"], u"Viewing terrace, timber deck"),
              (("p24", "stones"), "dot", COL["ink2"], u"Stepping stones"),
              (("p24", "bench"), "fill", COL["ink2"], u"Bench"),
              (("p24", "planter"), "fill", pla_colours("lavender")["fill"], u"Planter, lavender"),
              (("p24", "people"), "dot", FIG_A1_INK, u"People"),
              (("p24", "foot"), "line", COL["ink_dark"], u"Footbridge deck"),
              (("p24", "road_calmed"), "line", ROAD_CHANGE_COL["calmed"], u"Street calmed"),
              (("p24", "road_pedestrian"), "line", ROAD_CHANGE_COL["pedestrian"], u"Street or bridge for walking"),
              (("p24", "road_shared"), "line", ROAD_CHANGE_COL["shared"], u"Street shared"),
              (("p24", "hidden"), "dash", COL["river_mid"], u"Hidden stream line"),
              (("p24", "view"), "dot", COL["accent"], u"Viewpoint, sightline"),
              (("r28dt", "route"), "line", R28DT_ROUTE, u"Water route · step"),
              (("p24", "cut"), "dashdot", KM_CUT["colour"], u"Section line"),
              (("r28dt", "study"), "dashdot", R28_STUDY_LINE["colour"], R28_STUDY_NAME),
              (("r28dt", "bed"), "fill", _wat_pal()["surface"], u"Selinos stream"),
              (("r28dt", "bld"), "fill", cl["bld"], u"Building (survey)"))
    rows = [(kind, colour, label) for key, kind, colour, label in design if key in keys]
    if rows:
        out.append(("head", u"Design"))
        out += rows
    section = ((("p24s", "avg"), "fill", _wat_pal()["sec"], u"Water at the average yearly flow"),
               (("p24s", "flood"), "fill", P24_FLOOD, u"Reach of Q500 (lines: Q100, Q500)"),
               (("p24s", "dg_rows"), "line", pla_green("crop"), u"Tomato rows (garden crop)"),
               (("p24s", "lane"), "fill", SF_LANE["walk"], u"Walk, bike lane, street"),
               (("p24s", "back"), "fill", _sec_mix(SEC["soil"], SEC["paper"], 0.6), u"Ground behind the cut"),
               (("p24s", "bhouse"), "fill", BLD_COL["fill"], u"Buildings behind the cut"),
               (("p24s", "wall"), "fill", SCT["stone"], u"DSİ stone wall"))
    rows = [(kind, colour, label) for key, kind, colour, label in section if key in keys]
    if rows:
        out.append(("head", u"Section"))
        out += rows
    return out


def leg(key, val=True):
    LEG.setdefault(key, val)
    if _PLEG[0] is not None:
        _PLEG[0].setdefault(key, val)
