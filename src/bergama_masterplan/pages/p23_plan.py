# p.23 the plan (booklet p21): plan_page, the pl28_* / pl23_* functions and draw_corridor (split from parts/02_Design.py, parts/02b_detail.py, parts/02c_corridor.py, parts/02d_r28_ground.py on 29 Oct 2026; T7 30 Oct: layer order, trees, stream, labels)
# v28 (revision 29 Oct, WO-T4b-2, package H "Page 23"): the map is the page. The analysis frame at 1:5,000 in two rows
# (upstream half on top, downstream half below; PL23_OVL m either side of the match line drawn in both), every layer
# of the corridor on both, the riverside walk as one route with the bike lane beside it (PL23_BIKE); each numbered
# move a short boxed text on the map by its place, on an arrow (R13 callouts, R14 numbered boxes); a side column
# holds the small legend, the moves with no room on the map and the areas left as they are. One strip at 1:10,000
# when two rows do not fit the crop. The perspective collage of R12 is left out (a script draws no photo collage).
# v38 (round 4, S8, booklet p21 "Masterplan: an ecological corridor"; BRIEF P21.1-P21.7, P22.8, G-R4-1/2/4/7/9/11):
#   * ONE draw order (mp_map_draw = common/map_layers.map_draw): the shared MUTED base (ml_base: light houses with one
#     closed outline per block, light streets, the stream) at the bottom, the D9 footprint tint on what we change
#     (pl23_tint), then the page's own water, lines, planting and pictograms as steps AT their layers, the study
#     line (map_draw's, violet) above them; the masterplan's own survey base (C.bld faces, C.roads, built_since) is
#     no longer drawn here (P21.3; C.bld / F stay for the grid analysis).
#   * the round 3 lines redrawn as crisp single lines (PL23_LW), no stacked soft bands (P21.1).
#   * nothing outside the study area: the corridor generates inside it (02c, v38); here a second filter on the zones
#     (sc_rings_clip), roads, hidden stream, walk, sightline (sc_lines), trees (sc_points) and icons (C.in_study);
#     a hub outside it gets no symbol, only its name in the base tone (P21.5).
#   * every text through the page's TextPage (Page.text_page "p21"; check_text RAISES on a collision); markers by
#     mp_marker in the colour of what they name (mk_register tables, P21.2); hub names by TextPage.place with real
#     fallbacks (further rings, a smaller size, then a number + side-list row, P21.6); the voids drawn as designed
#     places (P21.7); the move reasons printed in the side list (P22.8); north arrow = keymap.north_items (G-R4-9).
PL23_SCALE = 5000.0          # the two rows
PL23_FALLBACK = 10000.0      # one strip when the two rows do not fit BK_W x BK_H
PL23_OVL = 25.0              # m either side of the match line drawn in both rows
PL23_MARK_H = 9.0            # mm: north arrow, scale bar and flow note under each row
PL23_GAP = 3.0               # mm between the first row's marks and the second row
PL23_SIDE_MIN = 80.0         # mm: the side column at least this wide
PL23_SIDE_GAP = 5.0          # mm between the map and the side column
PL23_MARKS = {5000.0: (0.0, 50.0, 100.0, 250.0), 10000.0: (0.0, 100.0, 200.0, 500.0)}   # scale bar, m (50 mm)
PL23_REPEAT_MM = 45.0        # v35 (round 2 "upper map still crowded"): a move's badge again only this far (row mm) from its others
# v38 (round 4, S8): the round 4 page's sizes and drawing rules (design values unless a comment names a source)
PL23_NAME_PT = (8.0, 7.0)    # hub names (bold, white halo): first size, then the smaller try, pt (design value; P21.4
#                              "text a little smaller": was 9 pt)
PL23_BASE_NAME_PT = 6.5      # a hub outside the study area: its name as a plain base place name, pt (design value)
PL23_NAME_RINGS = (0.0, 2.5, 5.0)    # mm beyond the hub symbol where its name is tried, ring by ring (design value)
PL23_MK_PT = 7.0             # marker glyphs on the map and in the lists, pt (booklet label size, KEY_MIN)
PL23_MK_SHIFTS = (0.0, 2.2, 3.6, 5.0)   # mm: a marker on its place, else on rings this far round it (design value)
PL23_ROW_PAD = 0.8           # mm: labels and markers stay this far inside their map row (design value)
PL23_LW = dict(arm=0.7, road=0.6, later=0.4, hidden=0.45, walk=0.5, bike=0.22, bike_off=0.7, foot=0.45, stones=0.35,
               canopy=0.35, sight=0.3, terrace=0.3, bank=0.25, outline=0.15, square=0.25)
#                              mm: P21.1 crisp single lines at 1:5,000 (design values)
PL23_TERR_TINT_M = 4.0       # m either side of a rain terrace line: its D9 footprint band (design value)
PL23_VOID_COL = {"meadow": "89986A", "garden": "70754C", "grove": "3C4733", "lanes": "8E8F8A", "heritage": "8B2D2D"}
#                              P21.7 the designed voids' outline and marker colour (palette v1.4 references; design value)
PL23_VOID_LETTERS = u"ABCDEFGHIJKLMNOPQRSTUVWXYZ"   # one letter per kind of designed place, in reading order
PL23_LANE_CROWN_K = 0.6      # lane trees of the "Shaded lanes" voids: this x the species' sourced crown (design value)
PL23_SHRUB_GROUP_M = 6.0     # a rosemary / lavender group of a pocket garden drawn as ONE mound this wide, m (design
#                              value: one plant, 0.66-0.75 m, would print 0.15 mm at 1:5,000)
PL23_ENTRY_GAP = 0.9         # mm between two entries of the side lists (more than the placer's 0.6 mm pad; design value)
PL23_CONTOURS = False        # G-R4-4: the base's contours (green relief ramp) off on p21: the planting gradient and
#                              the terraces already read the slope at 1:5,000 (design value; True draws them)
PL23_TP_MARGINS = (0.0, 0.0, 0.0, 0.0)   # the crop is the booklet panel: no margin inside it (the booklet keeps its own)
PL23_EDGE_MM = 0.5           # mm the side column's text keeps from the crop's right edge (a glyph's ink may pass its
#                              advance width; design value)
PL23_WALK_COL, PL23_BIKE_COL = "4C2528", "5C7A86"         # palette references (library/examples/palettes)
PL23_BIKE = True             # the riverside walk carries a bike lane on its land side (Aras 29 Oct 21:04, decision card)


# T7 (revision 30 Oct, PG4 p21): the plan language. G8 / M5: the stream textured with a defined bank (water_plan),
# the site board's stream polygon (basemap "water") where there is one, else the corridor's bed; no mid-stream line.
# v35 (round 2, Aras 31 Oct p21: rows read "incredibly patterned and regular"; wanted scattered, never one tree type,
# natural but in a planned, architectural order, G9): the order is the ecology, not a pattern. Two bands from the
# water: the FOREST band (6-32 m) is one continuous riparian belt, mixed species whose crowns interpenetrate (trees
# at least PL23_BELT_GAP x their mean crown apart, dart thrown, row-like picks thrown away); the TREES band (32-60 m)
# is open ground with copses of 2-4 mixed trees (centres PL23_COPSE_M apart), lawns between. Species per tree:
# weighted by PLA_NICHE at t = distance / TREES[1] (wet to dry: willow, tamarisk, ash, plane), so neighbours mix where
# niches overlap; t is held inside the four trees' niche centres (0.24-0.52: past 0.52 = the driest of them).
# Crowns 0.88-1.08 x the sourced crown (_pla_size_var). Off the hubs (FOREST[2] / TREES[2]), only on open cells (no
# building, road or bed). Seeded: the same set every press. The same set draws p.21 and p.22 (plans and sections).
PL23_TREE_KEYS = ("willow", "tamarisk", "ash", "plane")   # the corridor's trees (P24_SPECIES wetland + forest)
PL23_BELT_GAP = 0.85         # forest belt: at least this x the two crowns' mean apart (crowns overlap a little)
PL23_COPSE_M = 42.0          # trees band: copse centres at least this far apart, m (design value)
PL23_COPSE_N = (2, 4)        # trees per copse
PL23_SEED = 2310
PL23_DG_ICON_MM = 4.0        # v37 (round 3, G9): Demeter's Garden's one olive symbol on the 1:5,000 plan, mm across


def _pl23_pick(t, rnd):
    """a corridor tree species for band position t, weighted by its niche (PLA_NICHE), t held inside the centres"""
    cs = [PLA_NICHE[k_][0] for k_ in PL23_TREE_KEYS]
    t = min(max(t, min(cs)), max(cs))
    ws = [(k_, PLA_NICHE[k_][2] * math.exp(-((t - PLA_NICHE[k_][0]) / PLA_NICHE[k_][1]) ** 2)) for k_ in PL23_TREE_KEYS]
    r = rnd.random() * sum(w for _k, w in ws)
    for k_, w in ws:
        r -= w
        if r <= 0.0:
            return k_
    return ws[-1][0]


def pl23_tree_set(C):
    """[(xy survey m, species key, crown m)] of the corridor's trees, once per corridor (C.pl23_trees), v35: a mixed
    riparian belt (FOREST band) and mixed copses (TREES band), see the note above"""
    got = getattr(C, "pl23_trees", None)
    if got is not None:
        return got
    rnd = random.Random(PL23_SEED)
    c, B = C.G.c, 12.0
    hsh, out = {}, []

    def near(q, r):
        i0, j0, m = int(math.floor(q[0] / B)), int(math.floor(q[1] / B)), int(math.ceil(r / B))
        return [e for i in range(i0 - m, i0 + m + 1) for j in range(j0 - m, j0 + m + 1) for e in hsh.get((i, j), ())]

    def free(q, cr, f):
        return all(math.hypot(q[0] - e[0][0], q[1] - e[0][1]) >= f * (cr + e[2]) / 2.0 for e in near(q, 16.0))

    def at(q, d0, d1, hmin):
        n = C.cell(q)
        if n is None or C.F[n] != 0 or not (d0 <= C.Dst[n] <= d1) or C.dhub(q) < hmin:
            return None
        return C.Dst[n]

    def put(q, key):
        cr = PLA_SPECIES[key]["crown_m"] * (0.88 + 0.20 * rnd.random())
        return q, key, cr

    def jit(n):
        u, v = C.G.xy(n)
        return C.V.xy(u + (rnd.random() - 0.5) * c, v + (rnd.random() - 0.5) * c)

    def add(e):
        out.append(e)
        hsh.setdefault((int(math.floor(e[0][0] / B)), int(math.floor(e[0][1] / B))), []).append(e)
    belt = [n for n in range(C.N) if C.F[n] == 0 and FOREST[0] <= C.Dst[n] < FOREST[1]]
    rnd.shuffle(belt)
    for n in belt:                                       # the riparian belt: dart throwing, no rows
        q = jit(n)
        d = at(q, FOREST[0], FOREST[1], FOREST[2])
        if d is None:
            continue
        e = put(q, _pl23_pick(d / TREES[1], rnd))
        if not free(q, e[2], PL23_BELT_GAP):
            continue
        if _pla_rowlike(q, [x[0] for x in near(q, 3.0 * e[2])], 3.0 * e[2]):
            continue
        add(e)
    outer = [n for n in range(C.N) if C.F[n] == 0 and FOREST[1] <= C.Dst[n] <= TREES[1]]
    rnd.shuffle(outer)
    cen, CB = {}, PL23_COPSE_M                           # copse centres by 42 m bucket (fast on the laptop)
    for n in outer:                                      # the open band: copses of mixed trees, lawns between
        q = jit(n)
        if at(q, FOREST[1], TREES[1], TREES[2]) is None:
            continue
        ci, cj = int(math.floor(q[0] / CB)), int(math.floor(q[1] / CB))
        if any(math.hypot(q[0] - p[0], q[1] - p[1]) < PL23_COPSE_M
               for i in (ci - 1, ci, ci + 1) for j in (cj - 1, cj, cj + 1) for p in cen.get((i, j), ())):
            continue
        cen.setdefault((ci, cj), []).append(q)
        want, got_ = rnd.randint(*PL23_COPSE_N), 0
        for _ in range(12 * PL23_COPSE_N[1]):
            if got_ >= want:
                break
            a, r = rnd.uniform(0.0, 2.0 * math.pi), 9.0 * math.sqrt(rnd.random())
            q2 = (q[0] + r * math.cos(a), q[1] + r * math.sin(a))
            d = at(q2, FOREST[1], TREES[1], TREES[2])
            if d is None:
                continue
            e = put(q2, _pl23_pick(d / TREES[1], rnd))
            if free(q2, e[2], 0.75):
                add(e)
                got_ += 1
    out.sort(key=lambda e: PLA_SPECIES[e[1]]["h_m"])      # the lower crowns first, the taller over them
    # v37 (round 3, P21.2 / G8): clipped to land at the source, so p.21 and p.22 (plans and sections) inherit it
    out = water_clip_points(out, [], pl23_wet_rings(C), crown_frac=0.5, get=lambda e: (e[0][0], e[0][1], e[2] / 2.0),
                            page=u"p21 + p22 tree set")
    if getattr(C, "study", None):                        # v38 (round 4, P21.5, CHK-7 site 9): a second filter, the
        out = sc_points(out, C.study, get=lambda e: (e[0][0], e[0][1]), page=u"p21")   # study area (crown centre)
    C.pl23_trees = out
    return out


PL23_ARM_HALF_M = 3.0        # v37: half the drawn width of a side arm (draw_corridor: 6 m), m, for the tree clip


def pl23_wet_rings(C):
    """v37 (round 3, G8): every water ring the plans draw, survey m, once per corridor (C.pl23_wet): the stream's
    outer rings (its islands count as water: no tree on a gravel bar in the channel), the widened reaches, the side
    arms (PL23_ARM_HALF_M either side of their line) and the reed basins (zone WT)"""
    got = getattr(C, "pl23_wet", None)
    if got is not None:
        return got
    out = [list(R) for R, _Hs in pl23_water_groups(C)]
    out += [list(w["ring"]) for w in C.widen if len(w["ring"]) >= 3]
    for a in C.arms:
        P = [tuple(p) for p in a["P"]]
        if len(P) >= 2:
            out.append(pl23_offset(P, PL23_ARM_HALF_M) + list(reversed(pl23_offset(P, -PL23_ARM_HALF_M))))
    out += [list(z["P"]) for z in C.D.zones if z["code"] == "WT" and len(z["P"]) >= 3]
    C.pl23_wet = out
    return out


def pl23_hub_trees(C):
    """v37 (G8): [(xy survey m, i)] of the hub squares' plane trees kept on land, once per corridor"""
    got = getattr(C, "pl23_hub_trees_", None)
    if got is not None:
        return got
    cr = PLA_SPECIES["plane"]["crown_m"] * 0.8
    pts = [(p, i) for h in C.hubs for i, p in enumerate(h.get("trees") or [])]
    C.pl23_hub_trees_ = water_clip_points(pts, [], pl23_wet_rings(C), crown_frac=0.5,
                                          get=lambda e: (e[0][0], e[0][1], cr / 2.0), page=u"p21 + p22 hub squares")
    if getattr(C, "study", None):                        # v38 (round 4, P21.5): and inside the study area
        C.pl23_hub_trees_ = sc_points(C.pl23_hub_trees_, C.study, get=lambda e: (e[0][0], e[0][1]), page=u"p21")
    return C.pl23_hub_trees_


def pl23_put(pg, shapes, alpha=None):
    """house shapes ("poly", ring, fill, stroke, lw[, alpha]) / ("line", pts, colour, lw[, dash]) -> pg, the
    fills at alpha when given"""
    for s_ in shapes or []:
        if s_[0] == "poly" and len(s_[1]) >= 3:
            a = s_[5] if len(s_) > 5 and s_[5] is not None else (alpha if s_[2] else None)
            pg.poly([list(s_[1])], fill=s_[2] or None, stroke=s_[3] if len(s_) > 3 else None,
                    lw=(s_[4] if len(s_) > 4 and s_[4] else 0.1), alpha=a)
        elif s_[0] == "line" and len(s_[1]) >= 2:
            pg.line(list(s_[1]), s_[2], s_[3] if len(s_) > 3 and s_[3] else 0.1, s_[4] if len(s_) > 4 else None)


def pl23_trees_draw(pg, C, T, k, box):
    """the tree set (pl23_tree_set) inside box (page mm) at its crown width; the species' own plan mark only at
    1:1,000 and larger (at 1:5,000 the crown forms tell them apart, M6: fewer symbols). Returns the legend keys
    (v38: "tree_<species>", one legend row per species with its Turkish name, D5)."""
    used = set()
    for i, (p, key, cr) in enumerate(pl23_tree_set(C)):
        x, y = T(p)
        r = cr * k / 2.0
        if x + r < box[0] or x - r > box[2] or y + r < box[1] or y - r > box[3]:
            continue
        pl23_put(pg, pla_plan(key, x, y, k, crown_m=cr, seed=i, distinct=k >= 0.5))   # v37 (D7): opaque
        used.add("tree_" + key)
    return used


def pl23_water_groups(C, warn=None):
    """[(outer ring, [holes])] survey m of the stream in plan, once per corridor (C.pl23_water): the site board's
    stream polygon (basemap "water", M3 / M5) where the base map has it, else the corridor's bed loops"""
    got = getattr(C, "pl23_water", None)
    if got is not None:
        return got
    out = []
    try:
        for it in basemap_items("base", ["water"], box=bbox(C.V.P)):
            if it[0] == "water":
                out += [(list(g[0]), [list(H) for H in g[1:] if len(H) >= 3]) for g in it[1] if len(g[0]) >= 3]
    except Exception as ex:
        if warn is not None:
            warn.append(u"masterplan: the base map's stream not read ({}): the corridor's bed is drawn".format(
                type(ex).__name__))
        out = []
    if not out:
        out = [(list(L), []) for L in C.bed_loops]
    C.pl23_water = out
    return out


def pl23_water_draw(pg, C, T, k, on, spacing):
    """the stream (M5 water_plan: surface tone, bank line, flow streaks deeper to the middle); islands in paper.
    Returns the page rings drawn (for the labels' linework)."""
    rings = []
    for i, (R, Hs) in enumerate(pl23_water_groups(C)):
        Q = [T(p) for p in R]
        if not on(Q):
            continue
        QHs = [[T(p) for p in H] for H in Hs]            # v37 (P21.2 glitch): islands left open by water_plan (the
        shp_put(pg, water_plan(Q, k, seed=i, spacing=spacing, holes=QHs).shapes())   # ground shows), no paper patch
        rings.append(Q)
        rings += QHs
    return rings


def pl23_prep(C):
    """v38 (round 4, P21.5, CHK-7 site 10): the corridor's drawn geometry clipped to the study area ONCE per corridor
    (C.pl23_clip; both rows read it, so each clip is counted once for "p21"): the zone-base zones (DG Demeter's
    Garden, WT reed basins) through sc_rings_clip; the changed roads and the later town line, the hidden-stream
    line, the riverside walk runs and the sightline through sc_lines. Survey m."""
    got = getattr(C, "pl23_clip", None)
    if got is not None:
        return got
    st = C.study or None
    out = dict(zones={}, roads=[], cov=[], walk=[], sight=[])
    for z in C.D.zones:
        if z["code"] in ("DG", "WT") and len(z["P"]) >= 3:
            out["zones"].setdefault(z["code"], []).extend(sc_rings_clip(z["P"], st, u"p21") if st else [list(z["P"])])
    for rd in ROADS + [TOWN_LINE]:
        ch = rd["change"] if rd["change"] in ROAD_CHANGE_COL else "later"
        runs = sc_lines(rd["xy"], st, u"p21") if st else [list(rd["xy"])]
        if runs:
            out["roads"].append((rd, ch, runs))
    for P in C.covered:
        out["cov"] += sc_lines(P, st, u"p21") if st else [list(P)]
    for x in (C.CL.get("W") or {}).get("runs") or []:
        P = x.get("P") or []
        if len(P) >= 2:
            for run in (sc_lines(P, st, u"p21") if st else [list(P)]):
                out["walk"].append((run, x.get("cls") == "bed", x.get("bank")))
    if C.terrace:                                         # the sightline toward the Trajaneum (off the plan)
        p2 = (C.terrace["xy"][0] + C.terrace["dir"][0] * 400.0, C.terrace["xy"][1] + C.terrace["dir"][1] * 400.0)
        out["sight"] = sc_lines([C.terrace["xy"], p2], st, u"p21") if st else [[C.terrace["xy"], p2]]
    C.pl23_clip = out
    return out


def pl23_tint(C):
    """v38 (round 4, G-R4-4, D9): the light transparent footprint of what we change, as ml_tint items (clipped to the
    study area): the widened stream, the reed basins (zone WT), a band PL23_TERR_TINT_M either side of each rain
    terrace, the hub squares and the designed voids (not the heritage settings: they are kept as they are)."""
    cl = pl23_prep(C)
    rings = [list(w["ring"]) for w in C.widen if len(w["ring"]) >= 3]
    rings += [list(R) for R in cl["zones"].get("WT", [])]
    for P in C.terr:
        P = [tuple(p[:2]) for p in P]
        if len(P) >= 2:
            rings.append(pl23_offset(P, PL23_TERR_TINT_M) + list(reversed(pl23_offset(P, -PL23_TERR_TINT_M))))
    for h in C.hubs:
        rings += [list(L_) for L_ in (h.get("square") or []) if len(L_) >= 3]
    for r_ in C.nogo:
        if r_.get("design") != "heritage":
            rings += [list(L_) for L_ in (r_.get("rings") or []) if len(L_) >= 3]
    return ml_tint(rings, study=C.study or None, page=u"p21")


def pl23_row_box(C, row, pad=30.0):
    """v38: the survey box (x0, y0, x1, y1) m of a map row (its four corners, pad m round), for the base map"""
    V = C.V
    b = bbox([V.xy(V.u0 + row[a_], v) for a_ in ("a", "b") for v in (V.v0, V.v1)])
    return (b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad)


def draw_corridor(pg, T, k, C, inP, dw, dh, base, tint):
    """Every layer of the corridor on plan page pg (T: world -> page mm, k: mm per m; inP: world point on this
    plan's own part). v38 (round 4, S8, G-R4-4): ONE draw order, map_layers' (mp_map_draw): base (the shared muted
    base, ml_base items) -> proj_tint (planting gradient, programme rings, then the D9 footprint tint) -> proj_water
    (the stream only when the base has none, the widened stream as a wetland inside its new bank, reed basins, side
    arms, the hidden-stream line) -> proj_lines (hub squares, Demeter's Garden, rain terraces, changed roads, bridges
    only without a base, crossings, the walk and its bike lane, the canopy, the sightline, the designed voids'
    outlines) -> proj_vegetation (trees, hub planes, the voids' copses, lane trees and shrub groups, Demeter's
    Garden's olive) -> study (map_draw's violet line) -> proj_marks (pictograms). Crisp single lines (P21.1), only
    inside the study area (P21.5). No text is drawn here (the page's TextPage places every word). Returns (legend
    keys used, name specs [dict(id, text, xy page mm, r, study)], pictogram boxes [(box page mm, keep name)])."""
    used, specs, icons = set(), [], []
    ink, ink2 = COL["ink_dark"], COL["ink2"]
    on = lambda Q: len(Q) >= 2 and hit(bbox(Q), (-2.0, -2.0, dw + 2.0, dh + 2.0))
    TL = lambda Ls: [Q for Q in ([T(p) for p in L_] for L_ in Ls) if len(Q) >= 3 and on(Q)]
    inside = lambda x, y, m=0.0: -m <= x <= dw + m and -m <= y <= dh + m
    big = k >= 0.5                                       # a 1:1,000 window
    fine = k < 0.15                                      # the 1:10,000 strip (fallback)
    lw = PL23_LW
    cl = pl23_prep(C)
    ins = C.in_study
    base_water = bool(basemap_water_rings(base)) if base else False
    if base:
        used.add("houses")
    if base_water:
        used.add("bed")

    def s_tint():                                        # the gradients under the D9 tint (map_draw draws it next)
        for t, Ls in reversed(C.eco):
            Ps = TL(Ls)
            if Ps:
                pg.poly(Ps, fill=ECO_COL, alpha=ECO_A)
                used.add("eco")
        for r_, Ls in reversed(C.rings):
            Ps = TL(Ls)
            if Ps:
                pg.poly(Ps, fill=HUB_COL, alpha=HUB_A)
                used.add("ring")
        if tint:
            used.add("tint")

    def s_water():
        if not base_water and pl23_water_draw(pg, C, T, k, on, 1.0 if big else 0.8):
            used.add("bed")                              # no base map: the corridor's own stream
        for w in C.widen:
            Q = [T(p) for p in w["ring"]]
            if len(Q) >= 3 and on(Q):
                pg.poly([Q], fill=WET_COL)               # v37 (D2, G8): flat wetland tone
                pg.line(Q + Q[:1], _wat_pal()["edge"], lw["bank"])   # the new bank, firm
                used.add("widen")
        for Q in TL(cl["zones"].get("WT", [])):
            pg.poly([Q], fill=WET_COL)
            pg.poly([Q], stripes=(COL["river_dark"], 0.9, 0.12, 90.0))
            pg.line(Q + Q[:1], COL["river_dark"], lw["outline"])
            used.add("reed")
        for a in C.arms:
            Q = [T(p) for p in a["P"]]
            if on(Q):
                pg.line(Q, COL["river_mid"], lw["arm"])   # v38 (P21.1): one crisp line, no soft band
                used.add("arm")
        for P in cl["cov"]:
            Q = [T(p) for p in P]
            if on(Q):
                pg.line(Q, COL["river_mid"], lw["hidden"], [1.6, 0.9], cap=0)
                used.add("hidden")

    def s_lines():
        for h in C.hubs:                                 # the hub squares: their D9 tint + a firm edge
            for Q in TL(h.get("square") or []):
                pg.line(Q + Q[:1], SQ_EDGE, lw["square"])
                used.add("square")
        for Q in TL(cl["zones"].get("DG", [])):
            pg.poly([Q], fill=MP["agriculture"][2], alpha=0.16)
            pg.line(Q + Q[:1], MP["agriculture"][2], lw["outline"])
            used.add("dg")
        for P in C.terr:                                 # rain terraces: ticks toward the stream
            Q = [T(p) for p in P]
            if not on(Q):
                continue
            mid = P[len(P) // 2]
            c_, _ = chain_at(C.ref, mid)
            q, _ = at_len(C.ref, arclen(C.ref), c_)
            s = arclen(Q)
            (x, y), (ux, uy) = at_len(Q, s, s[-1] / 2.0)
            qx, qy = T(q)
            side = 1.0 if (-uy) * (qx - x) + ux * (qy - y) > 0 else -1.0
            ticks_line(pg, Q, MP["storage"][2], lw["terrace"], 2.4 if big else 1.6, 0.9 if big else 0.6, side)
            used.add("terrace")
        for rd, ch, runs in cl["roads"]:                 # v38 (P21.1): one crisp line per changed road
            for P in runs:
                Q = [T(p) for p in P]
                if not on(Q):
                    continue
                if ch == "later":
                    pg.line(Q, ROAD_CHANGE_COL["later"], lw["later"], [2.0, 1.0], cap=0)
                else:
                    pg.line(Q, ROAD_CHANGE_COL[ch], lw["road"])
                used.add("road_" + ch)
        if not base:                                     # the base map draws the bridges (muted); without it, these
            for P in C.bridges:
                Q = [T(p) for p in P]
                if on(Q):
                    pg.line(Q, ink, 0.5 if big else 0.3)
                    used.add("bridge")
        for c_ in C.cross:
            if not c_.get("P"):                          # v30.1: kept bridges have only "xy"
                continue
            A_, B_ = T(c_["P"][0]), T(c_["P"][1])
            if c_["kind"] == "footbridge":
                pg.line([A_, B_], ink, lw["foot"])
                used.add("foot")
            elif c_["kind"] == "stepping stones":
                for i in range(5):
                    f = (i + 0.5) / 5.0
                    pg.circle(A_[0] + (B_[0] - A_[0]) * f, A_[1] + (B_[1] - A_[1]) * f, 0.9 if big else lw["stones"],
                              fill=ink2)
                used.add("stones")
        for P, bed, bank in cl["walk"]:                  # the riverside walk, its bike lane one thin line beside it
            Q = [T(p) for p in P]
            if len(Q) < 2 or not on(Q):
                continue
            pg.line(Q, PL23_WALK_COL, lw["walk"], [1.6, 0.6] if bed else None, cap=0 if bed else 1)
            used.add("walk_bed" if bed else "walk")
            if PL23_BIKE and not bed:
                pg.line(pl23_offset(Q, lw["bike_off"] * (1.0 if bank == "NE" else -1.0)), PL23_BIKE_COL, lw["bike"])
                used.add("bike")
        for P in C.canopy:
            Q = [T(p) for p in P]
            if on(Q):
                pg.line(Q, MP["centre"][2], lw["canopy"], [0.8, 0.5], cap=0)
                used.add("canopy")
        for P in cl["sight"]:
            Q = [T(p) for p in P]
            if on(Q):
                pg.line(Q, COL["accent"], lw["sight"], [1.4, 0.8], cap=0)
                used.add("sight")
        for r_ in C.nogo:                                # P21.7: the designed voids, a hairline round their tint
            col = PL23_VOID_COL.get(r_.get("design"), ink2)
            for Q in TL(r_.get("rings") or []):
                pg.line(Q + Q[:1], col, lw["outline"])
                r_["placed"] = True
                used.add("void")

    def s_veg():
        used.update(pl23_trees_draw(pg, C, T, k, (-2.0, -2.0, dw + 2.0, dh + 2.0)))
        for p, i in pl23_hub_trees(C):                   # v37 (G8, D7): kept on land, opaque
            x, y = T(p)
            if inside(x, y, 2.0):
                pl23_put(pg, pla_plan("plane", x, y, k, crown_m=PLA_SPECIES["plane"]["crown_m"] * 0.8, seed=200 + i,
                                      distinct=k >= 0.5))
                used.add("tree_plane")
        for j, r_ in enumerate(C.nogo):                  # P21.7: copses (plane / ash), lane trees, shrub groups
            lane = r_.get("design") == "lanes"
            for i, p in enumerate(r_.get("trees") or []):
                x, y = T(p)
                if not inside(x, y, 2.0):
                    continue
                key = ("plane", "ash")[i % 2]
                cr = PLA_SPECIES[key]["crown_m"] * (PL23_LANE_CROWN_K if lane else 1.0)
                pl23_put(pg, pla_plan(key, x, y, k, crown_m=cr, seed=400 + 37 * j + i, distinct=k >= 0.5))
                used.add("tree_" + key)
            for i, p in enumerate(r_.get("shrubs") or []):
                x, y = T(p)
                if not inside(x, y, 1.0):
                    continue
                key = ("rosemary", "lavender")[i % 2]
                pl23_put(pg, pla_plan(key, x, y, k, crown_m=PL23_SHRUB_GROUP_M, seed=700 + 37 * j + i,
                                      distinct=k >= 0.5))
                used.add("shrub_" + key)
        for j, z in enumerate(z_ for z_ in C.D.zones if z_["code"] == "DG" and ins(z_["q"])):
            x, y = T(z["q"])                             # v37 (G9): Demeter's Garden = its field + ONE olive
            if inside(x, y):
                d_ = PL23_DG_ICON_MM if not big else max(PL23_DG_ICON_MM, PLA_SPECIES["olive"]["crown_m"] * k)
                pl23_put(pg, pla_plan("olive", x, y, k, crown_m=d_ / k, seed=300 + j, distinct=True))
                icons.append(((x - d_ / 2.0, y - d_ / 2.0, x + d_ / 2.0, y + d_ / 2.0), u"olive %d" % j))

    s_ic = 3.0 if big else (1.8 if fine else 2.2)

    def s_marks():                                       # pictograms, only inside the study area (P21.5)
        for p in C.seats:
            x, y = T(p)
            if inside(x, y) and ins(p):
                icon(pg, "seat", x, y, s_ic * 0.8)
                used.add("seat")
        ic = []
        for h in C.hubs:
            if not h.get("in_study"):                    # v38 (U40): a hub outside designs nothing: no symbol
                continue
            ic.append(("transit" if h["role"] == "transit" else ("gate" if h["id"] == u"K6" else "walkhub"), h["xy"],
                       u"hub_icon " + h["id"]))
            if h.get("sub_xy"):
                ic.append(("sub", h["sub_xy"]["c"], u"icon"))
        for z in C.D.zones:
            if z["code"] in ("GR", "DG"):
                ic.append(("cafe", z["q"], u"icon"))
            if z["code"] == "WT":
                ic.append(("edu", z["q"], u"icon"))
            if z["code"] == "WS" or (z["code"] == "WA" and z["tier"] == "F"):
                ic.append(("seat", z["q"], u"icon"))
        ic += [("edu", CRAFT_XY, u"icon"), ("deck", ROMAN_WALL, u"icon")]
        if C.terrace:
            ic.append(("view", C.terrace["xy"], u"icon"))
        for kind, p, nm in ic:
            if not ins(p):
                continue
            x, y = T(p)
            if inside(x, y):
                big_ = kind in ("transit", "walkhub", "gate")
                s_ = s_ic * (1.25 if big_ else 1.0)
                icon(pg, kind, x, y, s_)
                icons.append(((x - s_ * 0.55, y - s_ * 0.55, x + s_ * 0.55, y + s_ * 0.55), nm))
                used.add(kind)

    mp_map_draw(pg, u"p21", T, base, steps={"proj_tint": s_tint, "proj_water": s_water, "proj_lines": s_lines,
                                            "proj_vegetation": s_veg, "proj_marks": s_marks},
                tint=tint, study=C.study or None)
    if C.study:
        used.add("study")
    for h in C.hubs:                                     # the hub names for the page's TextPage (Turkish, G-R4-11)
        if inP(h["xy"]):
            specs.append(dict(id=h["id"], text=HUB_NAME[h["id"]], xy=T(h["xy"]), study=bool(h.get("in_study")),
                              r=s_ic * 1.25 * 0.55 if h.get("in_study") else 0.0))
    return used, specs, icons


# ---------------------------------------------------------------- G10: one frame figure
def pl28_frame_stats(C):
    """v27 (MIRAQUA 28 Oct, G10): C.frame_m2 = the frame polygon's area (shoelace: 150.52 ha for site_alan, the figure
    the site board prints on p.02); C.inF = 1 for each grid cell whose centre lies inside the frame (the grid
    overshoots it by up to one cell on each axis, which made 151 ha); each such cell stands for frame area / cells
    inside (C.cell_m2, within 0.3 % of c x c), so C.stats {0 open, 1 building, 2 road, 3 bed: m2} adds up to the
    frame exactly. One pass over the grid (was four)."""
    G, V, F = C.G, C.V, C.F
    P = list(getattr(V, "frame_P", None) or V.P)          # build_all sets V.frame_P = site_alan
    inF = bytearray(C.N)
    for n in G.poly_cells([V.uv(p) for p in P]):
        inF[n] = 1
    C.frame_m2 = abs(area2(P))
    C.inF = inF
    C.cell_m2 = C.frame_m2 / float(inF.count(1) or 1)
    Fin = bytes(v if i else 9 for v, i in zip(F, inF))
    C.stats = dict((k_, Fin.count(k_) * C.cell_m2) for k_ in (0, 1, 2, 3))


# ---------------------------------------------------------------- v38 (round 4, G-R4-1 / G-R4-2): text on the page
# v38 (round 4, S8): pl28_study / pl28_draw_study (G8, own study line) are gone: map_draw draws the one study line
# (BM_STUDY_LINE) in its own layer; pl28_runs and pl28_legend are replaced by pl23_runs and pl23_legend (every text
# registered in the page's TextPage, lines of one entry in one group).
def pl23_text(sh, s, x, y, size, colour, bold=False, align="L", group=None, name=None, allow=(), role="label",
              halo=None):
    """v38 (G-R4-1): one text on the page sh (size mm, baseline point at align), registered in sh's TextPage with
    its real box first (group: the lines of one entry, the runs of one line, may touch each other) and then drawn.
    Returns its box. (v38 closing: ² / ³ are the font's own glyphs, so they need no split any more.)"""
    if not s or not s.strip():
        return None
    if sh.tp is None:
        sh.text(s, x, y, size, colour, bold=bold, align=align, halo=halo, name=name, allow=allow, role=role)
        return None
    b = sh.tp.put(s, x, y, size / PT, bold, align, 0.0, name, role, colour, allow, group, emit=False)
    sh.items.append(("text", s, x, y, size, colour, bold, align, halo))
    return b


def pl23_wrap(s, w, size, bold=False, warn=None, page=u"p21"):
    """v38 (G-R4-2): s wrapped to w mm at size mm with real widths (tp_wrap), never one word alone on the last line
    (min_last_words=2); when the words do not allow it at w, a slightly narrower column is tried. Returns the lines
    (strings, as the old common/wrap.py wrap did). v38 closing: p16 and p22 use it too (page = the warning's page)."""
    for f in (1.0, 0.94, 0.88, 0.82):
        try:
            L = tp_wrap(s, w * f, size / PT, bold, min_last_words=2, bold_marks=False)
            return [u" ".join(r_[0] for r_ in ln) for ln in L if ln]
        except TpWidow:
            continue
    if warn is not None:
        warn.append(u"masterplan %s: one word alone on the last line of: %s" % (page, s))
    L = tp_wrap(s, w, size / PT, bold, min_last_words=1, bold_marks=False)
    return [u" ".join(r_[0] for r_ in ln) for ln in L if ln]


def pl23_asc_desc(size):
    """(ascender, descender) mm at size mm over both weights (descender negative): the line box every entry keeps"""
    a = [fm_asc_desc(size / PT, b) for b in (False, True)]
    return max(v[0] for v in a), min(v[1] for v in a)


def pl23_runs(sh, x, y, runs, size, colour):
    """v38: one line of text in runs [(text, bold)] (the bold keyword inside a line, G5), one group; returns its end x"""
    g = sh.tp._group() if sh.tp is not None else None
    for t, bd in runs:
        if t:
            pl23_text(sh, t, x, y, size, colour, bold=bd, group=g)
            x += text_w(t, size, bd)
    return x


def pl23_legend(sh, groups, x0, x1, y_top, ncols, warn):
    """v38 (G-R4-1, P21.4): the legend in ncols columns from x0 to x1, top down from y_top: each group a bold head,
    then its drawn samples with plain names (only what the page draws, 7 pt); a name too long for its column wraps
    onto a second row (no widow); a head never ends a column. Row pitch = the font's line box + the placer's pad, so
    no two rows touch. The block is kept (kind "legend") so no label of the page may enter it. Returns the y under it."""
    sz = KEY_MIN
    asc, desc = pl23_asc_desc(sz)
    pitch = asc - desc + 0.75
    cw = (x1 - x0) / float(ncols)
    tw = cw - 7.5 - 0.8
    rows = []                                             # (lines, sample or None for a head)
    for head, items in groups:
        if items:
            rows.append(([head], None))
            rows += [(pl23_wrap(nm, tw, sz, False, warn), f) for nm, f in items]
    if not rows:
        return y_top
    slots = sum(len(L) for L, _f in rows)
    cols = []
    for R in range(int(math.ceil(slots / float(ncols))), slots + 2):
        cols, cur, n = [], [], 0
        for r_ in rows:
            h = len(r_[0])
            if cur and (n + h > R or (r_[1] is None and n + h >= R)):
                cols.append(cur)
                cur, n = [], 0
            cur.append(r_)
            n += h
        cols.append(cur)
        if len(cols) <= ncols:
            break
    y_low = y_top
    for c, col in enumerate(cols):
        cx = x0 + c * cw
        j = 0
        for L, f in col:
            base = y_top - asc - j * pitch
            g_ = sh.tp._group()
            if f is None:
                pl23_text(sh, L[0], cx, base, sz, COL["ink_dark"], bold=True, group=g_, allow=("legend",))
            else:
                f(sh, cx, base - 0.3, 6.0, 2.2)
                for i_, t_ in enumerate(L):
                    pl23_text(sh, t_, cx + 7.5, base - i_ * pitch, sz, COL["ink"], group=g_, allow=("legend",))
            j += len(L)
        y_low = min(y_low, y_top - asc - (j - 1) * pitch + desc)
    sh.keep((x0, y_low, x1, y_top), "legend", u"legend")
    return y_low


# ---------------------------------------------------------------- P23: markers, list, sources
def pl28_note_group(nt):
    """P23.1: the R28_MARKERS group of a numbered note: roads; hubs and transit (the later town bus line too); water
    and ecology (reed basins, terraces, hidden stream, widened stream, side arm, the edges kept); crossings
    (footbridges); heritage and views."""
    k = nt["key"]
    if k[0] == "road":
        return "hubs" if k[1] == TOWN_LINE["name"] else "roads"
    return {"hub": "hubs", "foot": "crossings", "h4": "heritage", "h6": "heritage", "view": "heritage"}.get(k[0], "water")


def pl28_note_entry(C, nt):
    """P23.2: (name, one short line) of a numbered note for the list, in plain words from the note's own data. No
    source codes: they go to the sources page with every reason, whole (pl28_plan_sources)."""
    k = nt["key"]
    less = u"less than {:.0f} m open".format(KEPT_MAX)
    if k[0] == "hub":
        h = next((h_ for h_ in C.hubs if h_["id"] == k[1]), {})
        nm = PL28_HUB.get(k[1], k[1])
        if h.get("role") == "transit":
            return nm + u" · transit hub", u"town bus lines stop here · " + (
                u"square over the culvert" if k[1] == u"İstiklal" else u"by the " + landmark_name("kizil_avlu") + u" tunnels")
        if k[1] == u"K6":
            return nm + u" · gateway out", u"the primary road is kept · bus stop {} {:.0f} m".format(
                h.get("stop", u""), h.get("stop_m", 0.0))
        extra = {u"K3": u" · workshops, education", u"K5": u" · Demeter's Garden"}.get(k[1], u"")
        sub = u", sub-hub in the bed" if h.get("sub_xy") else u""
        return nm + u" · walking hub", (u"dry square" if extra else u"dry square at the Roman bridge") + sub + extra
    if k[0] == "road":
        if k[1] == TOWN_LINE["name"]:
            return u"Town bus line to {} · later step".format(bridge_name("K4", short=True)), \
                u"on the existing streets from İstiklal to the {} stop".format(bridge_name("K4", short=True))
        rd = next((r_ for r_ in ROADS if r_["name"] == k[1]), None)
        if rd is not None:
            ch, _, rest = rd["note"].partition(u": ")
            return u"{}{} · {}".format(rd["name"][:1].upper(), rd["name"][1:], ch), rest
    if k[0] == "kept":
        return {"building": (u"Edge kept · buildings", u"buildings stand at the bank, " + less),
                "road": (u"Edge kept · road", u"a road runs at the bank, " + less),
                "frame": (u"Nothing placed", u"the edge of the analysis frame, " + less)}.get(
            k[1], (nt["text"][:1] + nt["text"][1:].lower(), less))
    if k[0] == "view" and C.terrace:
        return u"Viewing terrace", u"a clear sightline to {}, {:,.0f} m away".format(   # closing G-R4-11: names table
            landmark_name("trajan_tapinagi"), C.terrace["d"])
    if k[0] == "widen" and C.widen:
        lo, hi = min(w["fw"][0] for w in C.widen), max(w["fw"][1] for w in C.widen)
        return u"Stream widened", u"room for water and a wetland · {:.0f}-{:.0f} m open beside the bank".format(lo, hi)
    if k[0] == "foot":
        return u"Footbridge" + (u"s" if len(nt["at"]) > 1 else u""), \
            u"{:.0f}+ m of stream without a crossing".format(FOOT_GAP_M)   # v38 (P21.4): shorter
    fixed = {"h4": (u"Step to the water", u"facing Tabaklar Hamamı, a bath ruin 1.5 m from the stream"),
             "h6": (u"Deck over the Roman bank wall", u"a Roman bank wall of about 120 m"),   # v38 (G-R4-11, §4.6)
             "wt": (u"Reed basins", u"the water is cleaned once · clean-water classroom"),
             "terr": (u"Rain terraces on the contours", u"they hold the rain · overflow to the reed basins"),
             "cov": (u"Hidden stream", u"nothing opened: the water line drawn in the paving"),
             "arm": (u"Side arm", u"a planted channel cleans the return water")}   # v28 (D2 a): reed only in lined basins
    return fixed.get(k[0], (nt["text"][:1] + nt["text"][1:].lower(), u""))


def pl28_src_kind(s):
    """N2 / F5 hint for the booklet's sources page: "public online" (OSM, its bus stops, ESA WorldCover, DSI, EPA),
    "project note" (history cards h01-h03, decisions D/H, register codes P/E), else "booklet analysis" (survey, open
    ground, edge plan, water board cuts, city link)."""
    if re.search(u"\\bOSM\\b|WorldCover|satellite 2021|\\bDSI\\b|\\bEPA\\b|bus stop", s):
        return u"public online"
    if re.search(u"\\b(h0\\d|H\\d|D\\d{1,2}|P\\d{2}|E\\d{2})\\b", s):
        return u"project note"
    return u"booklet analysis"


def pl28_plan_sources(ents, vl):
    """P23.2 / N2: what the page does not print, for the booklet's sources page, keyed by the marker numbers (and
    letters) on the masterplan page. v28 (revision 29 Oct, WO-T4b-2, D13): only the public sources (pl28_src_kind
    "public online"); a move or area with none keeps an empty list. v38 (round 4, P21.7): "left_as_is" now holds the
    designed places, one entry per letter (vl, pl23_markers: a letter per kind of place), with its place name, its
    reason, the regions' total ha, their data reasons and the sources those name (the key name is kept: the booklet
    reads it)."""
    pub = lambda s_: pl28_src_kind(s_) == u"public online"
    out = []
    for v in vl:
        whys, srcs = [], []
        for r_ in v["regions"]:
            w_ = PL28_SRC_TAG.sub(u"", r_["why"]).strip()
            if w_ not in whys:
                whys.append(w_)
            for m_ in PL28_SRC_TAG.findall(r_["why"]):
                n_ = PL28_SRC_NAME.get(m_, m_)
                if pub(n_) and n_ not in srcs:
                    srcs.append(n_)
        out.append({"id": v["letter"], "place": v["place"], "reason": v["reason"],
                    "ha": round(sum(r_["ha"] for r_ in v["regions"]), 2), "why": u"; ".join(whys), "sources": srcs})
    return {"crop": "mp_plan", "heading": u"Masterplan: what each numbered move stands on",
            "markers": [{"n": nt["n"], "group": grp, "name": nm, "line": line,
                         "sources": [{"text": s_, "kind": u"public online"} for s_ in nt["why"] if pub(s_)]}
                        for nt, grp, nm, line, ok in ents],
            "left_as_is": out}


# ---------------------------------------------------------------- v28 (WO-T4b-2): rows, route, callouts, side column
def pl23_offset(Q, d):
    """the polyline Q (page mm) moved d mm to its left (negative: to its right), each vertex along the normal of its
    neighbours' chord"""
    out, n = [], len(Q)
    for i in range(n):
        a, b = Q[max(0, i - 1)], Q[min(n - 1, i + 1)]
        ux, uy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(ux, uy) or 1.0
        out.append((Q[i][0] - uy / L * d, Q[i][1] + ux / L * d))
    return out


def pl23_rows(C, warn):
    """(scale, rows): two rows at PL23_SCALE when they fit the crop beside a PL23_SIDE_MIN side column, else one strip
    at PL23_FALLBACK. A row = {a, b: m from the frame's upstream end drawn; ea, eb: its own part (names, markers)}."""
    V = C.V
    L, Hm = V.u1 - V.u0, V.v1 - V.v0
    k = 1000.0 / PL23_SCALE
    w2, h2 = (L / 2.0 + PL23_OVL) * k, Hm * k
    if w2 <= BK_W - PL23_SIDE_MIN - PL23_SIDE_GAP and 2.0 * (h2 + PL23_MARK_H) + PL23_GAP <= BK_H:
        m = L / 2.0
        return PL23_SCALE, [dict(a=0.0, b=m + PL23_OVL, ea=0.0, eb=m), dict(a=m - PL23_OVL, b=L, ea=m, eb=L)]
    warn.append(u"masterplan page: two rows at 1:{:,.0f} ({:.0f} x {:.0f} mm each) do not fit the page: one strip at "
                u"1:{:,.0f}".format(PL23_SCALE, w2, h2, PL23_FALLBACK))
    return PL23_FALLBACK, [dict(a=0.0, b=L, ea=0.0, eb=L)]


def pl23_row_T(C, row, k, x0=0.0, y0=0.0):
    """(T, mine) of a row: T world -> page mm with the row's upstream end at x0 and the frame's foot at y0; mine(p) =
    the point lies in the row's own part of the frame"""
    V = C.V

    def T(p):
        u, v = V.uv(p)
        return (u - V.u0 - row["a"]) * k + x0, (v - V.v0) * k + y0

    def mine(p):
        u, v = V.uv(p)
        return V.u0 + row["ea"] <= u <= V.u0 + row["eb"] and V.v0 <= v <= V.v1
    return T, mine


def pl23_marks(sh, C, x0, y0, scale, runs):
    """the row under a map row, from (x0, y0) up: v38 (G-R4-9) the north arrow of keymap.north_items (only the arrow
    and "N", no plate; survey +Y turned with the plan) drawn with basemap_draw and kept as an obstacle, the scale bar
    beside it (SCRIPT_STANDARD §8) and a short note in runs [(text, bold)]"""
    V = C.V
    nu, nv = V.uv((V.cx, V.cy + 1.0))
    L = math.hypot(nu, nv) or 1.0
    ang = math.atan2(-nu / L, nv / L)                    # north's turn from page-up, counter-clockwise

    def fill(rings, hx, a, nz):
        sh.poly(rings, fill=hx)
        for R in rings:
            sh.keep(R, "north", u"north arrow")

    def line(pts, hx, w, dash, a):
        sh.line(pts, hx, w, list(dash) if dash else None)
        sh.keep(pts, "north", u"north arrow", line=True)

    def text(s_, xy, size, hx, bold, align):            # "MC" = (x, y) the middle of the ink: to a baseline point
        ix0, iy0, ix1, iy1 = fm_ink_box(s_, size / PT, bool(bold))
        pl23_text(sh, s_, xy[0] - (ix0 + ix1) / 2.0, xy[1] - (iy0 + iy1) / 2.0, size, hx, bold=bool(bold),
                  allow=("north",), name=u"north arrow")
    basemap_draw(north_items(x0 + 8.0, y0 + 0.4, ang, 6.0, COL["ink_dark"]), lambda p: p, fill, line, text)
    mk = PL23_MARKS.get(scale, PL28_MARKS)
    xb = x0 + 17.0
    scale_bar(sh, xb, y0 + 2.0, scale, mk)
    xs = xb + mk[-1] * 1000.0 / scale + 6.0 + text_w(u"1:{:,.0f}".format(scale), 3.4, True) + 6.0
    pl23_runs(sh, xs, y0 + 2.0, runs, KEY_MIN, COL["ink2"])


# ---------------------------------------------------------------- v38 (round 4, G-R4-7, P21.2): markers
def pl23_mk_tables(C):
    """v38 (P21.2): the element colours the markers read (mk_register), from the colours the page draws them with:
    roads (ROAD_CHANGE_COL, as drawn), hubs (their pictogram), the other moves (the line / fill that draws them),
    the edges kept (the base tones of what stands at the bank), the designed voids (their outline)."""
    mk_register("road", ROAD_CHANGE_COL)
    mk_register("hub", dict((h["id"], COL["accent_dark"] if h["role"] == "transit" else
                             (COL["ink_dark"] if h["id"] == u"K6" else SQ_EDGE)) for h in C.hubs))
    mk_register("move", {"widen": _wat_pal()["edge"], "arm": COL["river_mid"], "wt": COL["river_dark"],
                         "cov": COL["river_mid"], "terr": MP["storage"][2], "foot": COL["ink_dark"],
                         "view": COL["accent"], "h4": COL["histwall"], "h6": COL["histwall"]})
    mk_register("kept", {"building": BM_MUTED["bld_edge"], "road": BM_MUTED["road_edge"], "frame": COL["ink2"]})
    mk_register("void", PL23_VOID_COL)


def pl23_note_colour(nt):
    """v38 (P21.2): the colour of the element a numbered note names (mk_colour raises on an unknown one)"""
    k = nt["key"]
    if k[0] == "hub":
        return mk_colour("hub", k[1])
    if k[0] == "road":
        rd = TOWN_LINE if k[1] == TOWN_LINE["name"] else next((r_ for r_ in ROADS if r_["name"] == k[1]), None)
        ch = rd["change"] if rd is not None and rd["change"] in ROAD_CHANGE_COL else "later"
        return mk_colour("road", ch)
    if k[0] == "kept":
        return mk_colour("kept", k[1])
    return mk_colour("move", k[0])


def pl23_mk_r(s):
    """the outer radius (rim included) mp_marker gives the glyph s, mm"""
    return mk_marker(0.0, 0.0, s, "FFFFFF", PL23_MK_PT)[2] + 0.125


def pl23_mk_spot(tp, x, y, r, bounds):
    """v38: the first free spot (TextPage: no text, no kept area within its pad) for a marker of radius r: on its
    place (x, y), else on rings PL23_MK_SHIFTS round it, inside bounds; None when there is none"""
    for d in PL23_MK_SHIFTS:
        for j in range(8 if d > 0.0 else 1):
            a = j * math.pi / 4.0
            cx, cy = x + d * math.cos(a), y + d * math.sin(a)
            b = (cx - r, cy - r, cx + r, cy + r)
            if b[0] < bounds[0] or b[1] < bounds[1] or b[2] > bounds[2] or b[3] > bounds[3]:
                continue
            if tp._free(b):
                return cx, cy
    return None


def pl23_markers(sh, C, rws, warn):
    """v38 (round 4, P21.2, P21.7, G-R4-5.5): the map's markers, each through mp_marker (glyph centred on its ink,
    circle grown for two digits, disc kept as an obstacle) in the colour of what it names: every numbered move on
    each of its places (a repeat only PL23_REPEAT_MM from the others; an edge kept once), on its place or the
    nearest free spot round it; every designed void a letter on its first label spot (one letter per kind of place,
    in reading order: the list explains each kind once, G-R4-2). A move with no free spot is only in the side list
    (warned). rws = [(T sheet, mine, bounds, name specs)]. Returns (ents [nt, group, name, line, on the map],
    letter groups [dict(letter, design, place, reason, colour, regions, n_map)])."""
    tp = sh.tp
    ents, vl = [], []
    row_of = lambda p: next((i for i, r_ in enumerate(rws) if r_[1](p)), None)
    for nt in sorted(C.notes, key=lambda nt_: nt_["n"]):
        nm, line = pl28_note_entry(C, nt)
        ent = [nt, pl28_note_group(nt), nm, line, False]
        ents.append(ent)
        col, s = pl23_note_colour(nt), u"%d" % nt["n"]
        r = pl23_mk_r(s)
        seen = []
        for p in nt["at"]:
            i = row_of(p)
            if i is None:
                continue
            x, y = rws[i][0](p)
            if any(j == i and math.hypot(x - a, y - b) < PL23_REPEAT_MM for j, a, b in seen):
                continue                                  # v35: no repeat badge near one of the same move
            spot = pl23_mk_spot(tp, x, y, r, rws[i][2])
            if spot is None:
                continue
            mp_marker(sh, spot[0], spot[1], s, col, PL23_MK_PT)
            seen.append((i, x, y))
            ent[4] = True
            if nt["key"][0] == "kept":                    # an edge kept: one badge
                break
    by = {}
    V = C.V
    order = sorted(C.nogo, key=lambda r_: min([V.uv(q)[0] for q in r_["at"]] or [0.0]))
    for r_ in order:                                      # P21.7: the designed places, a letter per kind
        dz = r_.get("design") or u"place"
        if dz not in by:
            if len(by) >= len(PL23_VOID_LETTERS):
                raise ValueError(u"masterplan p21: more kinds of designed place than letters")
            by[dz] = dict(letter=PL23_VOID_LETTERS[len(by)], design=dz, place=r_.get("place") or dz,
                          reason=r_.get("reason") or u"", colour=mk_colour("void", dz), regions=[], n_map=0)
            vl.append(by[dz])
        v = by[dz]
        v["regions"].append(r_)
        p = next((q for q in r_["at"] if row_of(q) is not None), None)
        if p is None:
            continue
        i = row_of(p)
        x, y = rws[i][0](p)
        spot = pl23_mk_spot(tp, x, y, pl23_mk_r(v["letter"]), rws[i][2])
        if spot is None:
            warn.append(u"masterplan p21: designed place {} ({:.1f} ha) has no free spot for its letter {}: its "
                        u"outline is drawn, the side list names the kind".format(v["place"], r_["ha"], v["letter"]))
            continue
        mp_marker(sh, spot[0], spot[1], v["letter"], v["colour"], PL23_MK_PT)
        v["n_map"] += 1
    return ents, vl


# ---------------------------------------------------------------- v38 (round 4, P21.6): hub names
def pl23_fit(tp, text, anchor, pt, bold, d, bounds):
    """the TextPage positions (E, NE, N … in reading order) of text round anchor at distance d whose box stays
    inside bounds, as (dx, dy, align) for TextPage.place"""
    out = []
    for c in TP_POSITIONS:
        x, y, al = tp._at(c, text, anchor, pt, bold, d)
        b = tp._box(text, x, y, pt, bold, al, 0.0)
        if bounds[0] <= b[0] and b[2] <= bounds[2] and bounds[1] <= b[1] and b[3] <= bounds[3]:
            out.append((x - anchor[0], y - anchor[1], al))
    return out


def pl23_names(sh, C, rws, warn):
    """v38 (round 4, P21.6, D10): the hub names placed by the page's TextPage (TextPage.place), never "not placed":
    each in its row, beside its pictogram (bold, white halo), tried at PL23_NAME_PT[0] on rings PL23_NAME_RINGS
    further and further out, then at the smaller PL23_NAME_PT[1] on the same rings, then as a number on the hub
    (ring marker in the hub's colour) with a row in the side list (TpSideList, numbered in reading order). A hub
    outside the study area has no symbol: its name only as a plain base place name (PL23_BASE_NAME_PT, base tone);
    with no room it is left out WITH a warning (base names are context). Returns the side-list rows [(n, text,
    colour)]."""
    tp = sh.tp
    sl = TpSideList(u"p21 hub names")
    drawn, n_alt, n_base = [], 0, 0
    cols = {}
    for i, r_ in enumerate(rws):
        bounds = r_[2]
        for s in r_[3]:
            anchor = tuple(s["xy"])
            if not s["study"]:                            # P21.5: a base place name, no hub
                it = None
                for ring in PL23_NAME_RINGS:
                    pos = pl23_fit(tp, s["text"], anchor, PL23_BASE_NAME_PT, False, ring + 0.8, bounds)
                    if not pos:
                        continue
                    try:
                        it = tp.place(s["text"], anchor, positions=pos, pt=PL23_BASE_NAME_PT, colour=BM_MUTED["name"],
                                      name=u"base name " + s["id"], role="base_name")
                        break
                    except TextCollision:
                        continue
                if it is None:
                    warn.append(u"masterplan p21: {} lies outside the study area (no hub drawn) and its base name has "
                                u"no free spot: left out".format(s["text"]))
                else:
                    drawn.append((it, BM_MUTED["name"], None))
                    n_base += 1
                continue
            col = mk_colour("hub", s["id"])
            it = None
            for j, pt in enumerate(PL23_NAME_PT):
                for ring in PL23_NAME_RINGS:
                    pos = pl23_fit(tp, s["text"], anchor, pt, True, s["r"] + ring + 0.8, bounds)
                    if not pos:
                        continue
                    try:
                        it = tp.place(s["text"], anchor, positions=pos, pt=pt, bold=True, colour=COL["ink_dark"],
                                      name=u"hub name " + s["id"])
                        break
                    except TextCollision:
                        continue
                if it is not None:
                    n_alt += 1 if j else 0
                    break
            if it is None:                                # the number + side-list row (TextPage's own fallback), on
                at = pl23_mk_spot(tp, anchor[0], anchor[1], pl23_mk_r(u"88") + 0.4, bounds) or anchor   # a free spot
                it = tp.place(s["text"], at, positions=(), pt=PL23_NAME_PT[-1], bold=True, side_list=sl,   # by the hub
                              colour=col, name=u"hub name " + s["id"], allow=(u"hub_icon " + s["id"],))
                cols[id(it)] = col
            drawn.append((it, COL["ink_dark"], COL["white"]))
    rows = sl.close(tp) if sl.entries else []
    for it, col, halo in drawn:
        if it.get("role") == "number":                   # a ring marker round the number, kept, in the hub's colour
            col = cols.get(id(it), col)
            b = it["box"]
            cx, cy = (b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0
            r = 0.5 * math.hypot(b[2] - b[0], b[3] - b[1]) + MK_MARGIN_MM
            R = [(cx + r * math.cos(math.pi * q / 16.0), cy + r * math.sin(math.pi * q / 16.0)) for q in range(32)]
            sh.poly([R], fill=COL["white"], stroke=col, lw=0.3)
            sh.keep(R, "marker", u"hub number " + it["text"])
            halo = None
        sh.items.append(("text", it["text"], it["x"], it["y"], it["size_mm"], col, it["bold"], it["align"], halo))
    TP_LOG.append(u"p21 hub names: {} placed ({} at {:.0f} pt), {} numbered in the side list, {} base names".format(
        len(drawn) - len(rows) - n_base, n_alt, PL23_NAME_PT[-1], len(rows), n_base))
    out = []
    for n, t in rows:
        e = next(e_ for e_ in sl.entries if e_["n"] == n)
        out.append((n, t, cols.get(id(e["item"]), COL["ink_dark"])))
    return out


# ---------------------------------------------------------------- v38 (round 4, P21.4, P21.7, P22.8): side column
PL23_LIST_COLS = 2           # v37: the side lists (moves, designed places) in this many columns
PL23_LIST_GAP = 3.0          # mm between the list columns
PL23_LIST_TS = KEY_MIN       # v38 (P21.4): the lists' names and reasons at 7 pt (names were 7.5 pt)


def pl23_head(sh, s, x, y_top, w):
    """a list's head (bold, ink2) over a hairline, from y_top down; returns the y under it"""
    asc, desc = pl23_asc_desc(PL28_HEAD_TS)
    b = y_top - asc
    pl23_text(sh, s, x, b, PL28_HEAD_TS, COL["ink2"], bold=True)
    yl = b + desc - 0.5
    sh.line([(x, yl), (x + w, yl)], COL["ink2"], 0.2, alpha=0.5)
    return yl - 0.8


def pl23_list(sh, x0, x1, y_top, head, es, ncol, warn):
    """v38 (G-R4-1, G-R4-2, P22.8): a list under its head, flowed column by column into ncol columns: each entry its
    marker (mp_marker, the colour of what it names; "ring" style for the hub numbers) and its rows [(text, bold,
    colour)] wrapped with no widow, all lines of one entry in one text group; entries PL23_ENTRY_GAP apart beyond the
    font's line box, so no two entries touch. es = [dict(mk=(glyph, colour[, style]), rows=[...])]. Returns the y
    under the lowest column."""
    y = pl23_head(sh, head, x0, y_top, x1 - x0)
    colw = (x1 - x0 - PL23_LIST_GAP * (ncol - 1)) / float(ncol)
    R = max(pl23_mk_r(e["mk"][0]) for e in es)
    tx = 2.0 * R + 1.2
    sz = PL23_LIST_TS
    asc, desc = pl23_asc_desc(sz)
    lead = sz * 1.18
    items = []
    for e in es:
        lines = []
        for t, bd, cl in e["rows"]:
            if t:
                lines += [(s_, bd, cl) for s_ in pl23_wrap(t, colw - tx, sz, bd, warn)]
        h = max(asc + (len(lines) - 1) * lead - desc, 2.0 * R) + PL23_ENTRY_GAP
        items.append((e, lines, h))
    goal = sum(h for _e, _l, h in items) / float(ncol)
    c, cur, yy, y_low = 0, 0.0, y, y
    for e, lines, h in items:
        if cur + h > goal + 0.01 and cur > 0.0 and c < ncol - 1:
            c, cur, yy = c + 1, 0.0, y
        x = x0 + c * (colw + PL23_LIST_GAP)
        mp_marker(sh, x + R, yy - R, e["mk"][0], e["mk"][1], PL23_MK_PT, style=e["mk"][2] if len(e["mk"]) > 2 else
                  "solid")
        g = sh.tp._group()
        by = yy - asc
        for t, bd, cl in lines:
            pl23_text(sh, t, x + tx, by, sz, cl, bold=bd, group=g)
            by -= lead
        yy -= h
        cur += h
        y_low = min(y_low, yy)
    return y_low


def pl23_side(sh, x0, x1, H, used, ents, vl, warn):
    """v38 (round 4, P21.4, P21.7, P22.8): the side column from x0 to x1, top down: the legend (two columns, only
    what the page draws, PL23_LEGEND), the moves by number (marker, name, and its reason line under it: P22.8, CHK3_7
    §7.6), the designed places by letter (marker, place and total ha, its reason once per kind: P21.7). Keywords and
    short lines, a fact once (G-R4-2). Returns the y under the column (the hub-name side list may follow)."""
    groups = [(u"BASE MAP", [(nm, f) for key, nm, f in PL23_LEGEND if key in used and key in PL23_BASE_KEYS]),
              (u"PROPOSED", [(nm, f) for key, nm, f in PL23_LEGEND if key in used and key not in PL23_BASE_KEYS])]
    y = pl23_legend(sh, groups, x0, x1, H, 2, warn)
    if ents:
        es = [dict(mk=(u"%d" % nt["n"], pl23_note_colour(nt)),
                   rows=[(nm, True, COL["ink"]), (line, False, COL["ink2"])]) for nt, grp, nm, line, ok in ents]
        y = pl23_list(sh, x0, x1, y - 1.6, u"The moves, by number", es, PL23_LIST_COLS, warn)
    if vl:
        es = []
        for v in vl:
            ha = u_area(sum(r_["ha"] for r_ in v["regions"]) * 1e4, "ha")
            es.append(dict(mk=(v["letter"], v["colour"]),
                           rows=[(u"{} · {}".format(v["place"], ha), True, COL["ink"]), (v["reason"], False, COL["ink2"])]))
        y = pl23_list(sh, x0, x1, y - 1.6, u"Designed places, by letter", es, PL23_LIST_COLS, warn)
    if y < 0.0:
        warn.append(u"masterplan page: the side column runs {:.1f} mm over the crop (legend, moves, designed "
                    u"places): the text check will name the first text outside".format(-y))
    return y


# v28: the route's legend samples; T7: the stream, the wetland and the trees as the plan draws them (M5 water_plan,
# M6 pla_plan: no green dots). v38 (round 4): the samples of the crisp lines, the muted base, the D9 tint, the
# designed places, one row per species with its Turkish name (D5).
def _pl23_sw_bike():
    def f(pg, x, y, w, h):
        pg.line([(x, y + h * 0.35), (x + w, y + h * 0.35)], PL23_WALK_COL, PL23_LW["walk"])
        pg.line([(x, y + h * 0.35 + PL23_LW["bike_off"]), (x + w, y + h * 0.35 + PL23_LW["bike_off"])], PL23_BIKE_COL,
                PL23_LW["bike"])
    return f


def _pl23_sw_water():
    def f(pg, x, y, w, h):
        shp_put(pg, water_plan(rect(x, y, x + w, y + h), 1.0, spacing=0.5).shapes())
    return f


def _pl23_sw_wet():
    def f(pg, x, y, w, h):
        R = rect(x, y, x + w, y + h)
        pg.poly([R], fill=WET_COL)                       # v37: as the plan draws it (flat, firm bank, no waves)
        pg.line(R + R[:1], _wat_pal()["edge"], PL23_LW["bank"])
    return f


def _pl23_sw_reed():
    def f(pg, x, y, w, h):
        R = rect(x, y, x + w, y + h)
        pg.poly([R], fill=WET_COL)
        pg.poly([R], stripes=(COL["river_dark"], 0.9, 0.12, 90.0))
        pg.line(R + R[:1], COL["river_dark"], PL23_LW["outline"])
    return f


def _pl23_sw_house():
    def f(pg, x, y, w, h):
        R = rect(x + 0.4, y, x + w - 0.4, y + h)
        pg.poly([R], fill=BM_MUTED["bld"], stroke=BM_MUTED["bld_edge"], lw=BM_MUTED["lw"])
    return f


def _pl23_sw_outline(col, lw, fill=None, alpha=None):
    def f(pg, x, y, w, h):
        R = rect(x + 0.3, y, x + w - 0.3, y + h)
        if fill:
            pg.poly([R], fill=fill, alpha=alpha)
        pg.line(R + R[:1], col, lw)
    return f


def _pl23_sw_terr():
    def f(pg, x, y, w, h):
        ticks_line(pg, [(x, y + h * 0.6), (x + w, y + h * 0.6)], MP["storage"][2], PL23_LW["terrace"], 1.6, 0.6, -1.0)
    return f


def _pl23_sw_plant(key, d_mm=2.2):
    def f(pg, x, y, w, h):
        cr = PLA_SPECIES[key]["crown_m"]
        pl23_put(pg, pla_plan(key, x + w / 2.0, y + h / 2.0, d_mm / cr, crown_m=cr, seed=1, distinct=False))
    return f


_PL23_SP = lambda key: u"{} ({})".format(PLA_SPECIES[key]["name"], PLA_SPECIES[key]["turkish"])
PL23_BASE_KEYS = ("houses", "bed", "bridge", "study")
PL23_LEGEND = [
    ("houses", u"Houses and streets, survey", _pl23_sw_house()),
    ("bed", u"Selinos, darker = deeper", _pl23_sw_water()),
    ("bridge", u"Bridge", _sw_line(COL["ink_dark"], 0.3)),
    ("study", R28_STUDY_NAME, _sw_line(BM_STUDY_LINE["colour"], BM_STUDY_LINE["width_mm"],
                                       list(BM_STUDY_LINE["dash_mm"]))),
    ("tint", u"What we change, footprint", _sw_fill(ML_TINT, alpha=ML_TINT_ALPHA)),
    ("eco", u"Planting gradient", _sw_grad(ECO_COL)),
    ("ring", u"Programme at hubs", _sw_grad(HUB_COL)),
    ("widen", u"Widened · wetland, new bank", _pl23_sw_wet()),
    ("reed", u"Reed basins", _pl23_sw_reed()),
    ("arm", u"Planted side arm", _sw_line(COL["river_mid"], PL23_LW["arm"])),   # D2 a: not "reed"
    ("hidden", u"Hidden stream line", _sw_line(COL["river_mid"], PL23_LW["hidden"], [1.6, 0.9])),
    ("terrace", u"Rain terrace", _pl23_sw_terr()),
    ("square", u"Hub square", _pl23_sw_outline(SQ_EDGE, PL23_LW["square"], ML_TINT, ML_TINT_ALPHA)),
    ("dg", u"Demeter's Garden", _pl23_sw_outline(MP["agriculture"][2], PL23_LW["outline"], MP["agriculture"][2], 0.16)),
    ("void", u"Designed place, by letter", _pl23_sw_outline(PL23_VOID_COL["meadow"], PL23_LW["outline"], ML_TINT,
                                                            ML_TINT_ALPHA)),
    ("walk", u"Riverside walk", _sw_line(PL23_WALK_COL, PL23_LW["walk"])),
    ("walk_bed", u"Bed walk, shut in floods", _sw_line(PL23_WALK_COL, PL23_LW["walk"], [1.6, 0.6])),
    ("bike", u"Bike lane beside the walk", _pl23_sw_bike()),
    ("foot", u"New footbridge", _sw_line(COL["ink_dark"], PL23_LW["foot"])),
    ("stones", u"Stepping stones", _sw_dots(COL["ink2"], PL23_LW["stones"], None)),
    ("canopy", u"Canopied walkway", _sw_line(MP["centre"][2], PL23_LW["canopy"], [0.8, 0.5])),
    ("sight", u"Sightline", _sw_line(COL["accent"], PL23_LW["sight"], [1.4, 0.8])),
    ("road_calmed", u"Road calmed", _sw_line(ROAD_CHANGE_COL["calmed"], PL23_LW["road"])),
    ("road_pedestrian", u"Road pedestrian", _sw_line(ROAD_CHANGE_COL["pedestrian"], PL23_LW["road"])),
    ("road_shared", u"Road shared", _sw_line(ROAD_CHANGE_COL["shared"], PL23_LW["road"])),
    ("road_kept", u"Road kept", _sw_line(ROAD_CHANGE_COL["kept"], PL23_LW["road"])),
    ("road_relocated", u"Road relocated", _sw_line(ROAD_CHANGE_COL["relocated"], PL23_LW["road"])),
    ("road_later", u"Bus line, later", _sw_line(ROAD_CHANGE_COL["later"], PL23_LW["later"], [2.0, 1.0]))] + \
    [("tree_" + k_, _PL23_SP(k_), _pl23_sw_plant(k_)) for k_ in PL23_TREE_KEYS] + \
    [("shrub_" + k_, _PL23_SP(k_), _pl23_sw_plant(k_, 1.6)) for k_ in ("rosemary", "lavender")] + \
    [(k_, nm, _sw_icon(k_)) for k_, nm in (("walkhub", u"Walking hub"), ("transit", u"Transit hub"),
                                           ("gate", u"Gateway out"), ("sub", u"Sub-hub in the bed"),
                                           ("seat", u"Seats"), ("cafe", u"Cafe"), ("edu", u"Education"),
                                           ("view", u"Viewing terrace"), ("deck", u"Deck, archaeology"))]


# ---------------------------------------------------------------- the page
def plan_page(C, warn):
    """v28 (revision 29 Oct, WO-T4b-2, package H "Page 23"): the masterplan page (crop mp_plan, 392 x 238 mm). The
    analysis frame in two rows at 1:5,000 (pl23_rows; one 1:10,000 strip when they do not fit), upstream half on top,
    a dashed match line where the halves meet and its marks row (north arrow, scale bar, flow note). v38 (round 4,
    S8): one TextPage "p21" for the whole crop (every word registered with its real box; check_text RAISES on any
    collision, so a page with overlapping text is not written); each row drawn in ONE draw order (draw_corridor ->
    mp_map_draw: the shared muted base, the D9 tint, the project, the study line); then the markers (pl23_markers),
    the side column (pl23_side: legend, moves with their reasons, designed places), the hub names (pl23_names, with
    their numbered side-list rows when a name has no room). Public sources go to the sources page (sh.plan_sources)."""
    scale, rows = pl23_rows(C, warn)
    k = 1000.0 / scale
    V = C.V
    W, H = BK_W, BK_H
    dh = (V.v1 - V.v0) * k
    sh = Page(W, H)
    sh.poly([rect(0, 0, W, H)], fill=COL["paper"])
    sh.text_page(u"p21", (0.0, 0.0, W, H), margins=PL23_TP_MARGINS)
    pl23_mk_tables(C)
    pl23_water_groups(C, warn)
    D = basemap_load()
    if not D:
        warn.append(u"masterplan p21: no base map data (basemap.json of the site board): the plan has no base map "
                    u"(run the site board once)")
    tint = pl23_tint(C)
    used, rws, x_side = set(), [], 0.0
    y_top = H
    for i, row in enumerate(rows):
        dw = (row["b"] - row["a"]) * k
        x0, y0 = 0.0, y_top - dh
        T, mine = pl23_row_T(C, row, k)
        base = ml_base(pl23_row_box(C, row), scale, D=D, contours=PL23_CONTOURS) if D else []
        pg = Page(dw, dh)
        u_, specs, icons = draw_corridor(pg, T, k, C, mine, dw, dh, base, tint)
        used |= u_
        sh.clip([rect(x0, y0, x0 + dw, y0 + dh)])
        blit(sh, pg, x0, y0)
        sh.unclip()
        sh.poly([rect(x0, y0, x0 + dw, y0 + dh)], stroke=COL["ink2"], lw=0.25, alpha=0.45)   # the row's edge = the frame
        sh.tp.block((x0, y0, x0 + dw, y0 + dh), u"map row %d" % (i + 1))
        for b, nm in icons:                               # the pictograms: no label or marker on them
            sh.keep((b[0] + x0, b[1] + y0, b[2] + x0, b[3] + y0), "icon", nm)
        Ts, _ = pl23_row_T(C, row, k, x0, y0)
        if len(rows) > 1:                                 # the match line where the halves meet
            xm = x0 + ((row["eb"] if i == 0 else row["ea"]) - row["a"]) * k
            sh.line([(xm, y0), (xm, y0 + dh)], COL["ink2"], 0.3, [1.6, 0.8], cap=0)
            t_ = u"match line · continues below" if i == 0 else u"match line · from above"
            tw = text_w(t_, KEY_MIN)
            tx = xm - 1.2 - tw if i == 0 else xm + 1.2
            pl23_text(sh, t_, tx, y0 + dh - 3.0, KEY_MIN, COL["ink2"], halo=COL["white"])
        specs = [dict(s, xy=(s["xy"][0] + x0, s["xy"][1] + y0)) for s in specs]
        rws.append((Ts, mine, (x0 + PL23_ROW_PAD, y0 + PL23_ROW_PAD, x0 + dw - PL23_ROW_PAD, y0 + dh - PL23_ROW_PAD),
                    specs))
        if len(rows) > 1:                                 # P21.4: the flow said once
            runs = [(u"upstream half · flow ", False), (u"left to right", True)] if i == 0 else \
                [(u"downstream half", True)]
        else:
            runs = [(u"flow ", False), (u"left to right", True)]
        pl23_marks(sh, C, x0, y0 - PL23_MARK_H, scale, runs)
        x_side = max(x_side, dw)
        y_top = y0 - PL23_MARK_H - PL23_GAP
    if y_top + PL23_GAP < -0.5 or x_side > W - PL23_SIDE_MIN:
        warn.append(u"masterplan page: the map ({:.0f} x {:.0f} mm) runs over the {:.0f} x {:.0f} mm crop".format(
            x_side, H - y_top - PL23_GAP, W, H))
    sh.tp.block((x_side + PL23_SIDE_GAP, 0.0, W, H), u"side column")
    ents, vl = pl23_markers(sh, C, rws, warn)
    for nt, grp, nm, line, ok in ents:
        if not ok:
            warn.append(u"masterplan move {} has no marker on the map (no free spot on or round its places in the "
                        u"rows): only in the side list ({})".format(nt["n"], nm))
    y = pl23_side(sh, x_side + PL23_SIDE_GAP, W - PL23_EDGE_MM, H, used, ents, vl, warn)
    nrows = pl23_names(sh, C, rws, warn)
    if nrows:                                             # P21.6: the hub names with no room, by number
        pl23_list(sh, x_side + PL23_SIDE_GAP, W - PL23_EDGE_MM, y - 1.6, u"Hub names, by number",
                  [dict(mk=(u"%d" % n, col, "ring"), rows=[(t, True, COL["ink"])]) for n, t, col in nrows],
                  PL23_LIST_COLS, warn)
    TP_LOG.append(sh.check_text())                        # G-R4-1: RAISES; v38 closing: logs "overlap p21 ..."
    sh.crop = (0.0, 0.0, W, H)
    sh.key, sh.world, sh.scale, sh.pleg = "plan", bbox(C.V.P), scale, None
    sh.bid = ("mp_plan", "c1_s1", u"Masterplan: the ecological corridor of the whole {}".format(R28_FRAME_NAME.lower()))
    sh.plan_sources = pl28_plan_sources(ents, vl)
    C.ni_placed = sum(1 for r_ in C.nogo if r_.get("placed"))
    return sh
