# Round 6 (S8, 4 Nov 2026; BRIEF §6 row 20, PLAN §4-§5): booklet page 20. The SUBMISSION_SON page 21 drawing is
# restored (round 3 ee52805 draw_corridor layers: own survey base, planting gradient, programme at the hubs), then
# the legend recoloured by category (PL23_HUE -> common/hues.py, G6-6), the proposals of the other pages added with
# transparent fills (dry-top terraces, spillway, floodable planting, collect-clean-hold 1-11, R1-R4, market), the
# areas left as they are lettered a-z as SON, every element in its G6-9 group. Older notes below.
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
PL23_LEFT_LETTERS = u"abcdefghijklmnopqrstuvwxyz"   # round 6: one letter per area left as it is (SON page 21 a-q)
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
                            page=u"p20 + p22 tree set")
    if getattr(C, "study", None):                        # v38 (round 4, P21.5, CHK-7 site 9): a second filter, the
        out = sc_points(out, C.study, get=lambda e: (e[0][0], e[0][1]), page=u"p20")   # study area (crown centre)
    C.pl23_trees = out
    return out


# round 5 (S6, P23.7): Demeter's Garden from the shared design (parts/02g_demeter.py dg_design, p24 helper), drawn
# in solid colours: the gathering place / café in a paving tone, the tomato rows a thin row line (design values)
PL23_DG_GATHER = "E6DCC8"
PL23_REED_TONE, PL23_REED_A = pla_green("reed"), 0.35   # round 5: the reed basins' solid tone over the wetland
PL23_DG_ROW = pla_green("row")
PL23_DG_ROW_LW = 0.12
def pl23_dg(C):
    """the designed Demeter's Garden (dg_design, parts/02g_demeter.py) clipped to the study area, once per
    corridor; None when the design module is not there or gives nothing (the zone-base DG field is drawn then)"""
    got = getattr(C, "pl23_dg_", 0)
    if got != 0:
        return got
    out = None
    if "dg_design" in globals():
        try:
            d = dg_design(C)                                                               # noqa: F821
        except Exception as ex:                          # p23_items warns (no warn list here)
            d = None
            C.pl23_dg_err = u"{}: {}".format(type(ex).__name__, ex)
        if d and d.get("rings"):
            st = C.study or None
            out = dict(d)
            out["rings"] = [Q for R in d["rings"] for Q in (sc_rings_clip(R, st, u"p20") if st else [list(R)])]
            for key in ("cafe", "gather"):
                out[key] = [Q for R in d.get(key) or [] for Q in (sc_rings_clip(R, st, u"p20") if st else [list(R)])]
            for key in ("rows", "paths", "edge"):
                out[key] = [Q for P in d.get(key) or [] for Q in (sc_lines(P, st, u"p20") if st else [list(P)])]
    C.pl23_dg_ = out
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
                                          get=lambda e: (e[0][0], e[0][1], cr / 2.0), page=u"p20 + p22 hub squares")
    if getattr(C, "study", None):                        # v38 (round 4, P21.5): and inside the study area
        C.pl23_hub_trees_ = sc_points(C.pl23_hub_trees_, C.study, get=lambda e: (e[0][0], e[0][1]), page=u"p20")
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
        elif s_[0] == "image":                           # round 5 (S4 plant module v3): image plants pass through as
            it_ = tuple(s_) + (None,) * (9 - len(s_))     # Page image items ("image", x, y, w, h, path, alpha, flip,
            pg.items.append(it_[:9])                     # clip); blit and the item export (04_items) carry them


PL23_TREE_N = {}            # round 6: trees drawn per species this run (trees log line)


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
        with mpx_grp(pg, "trees", u"%s %d" % (PLA_SPECIES[key]["name"], i + 1)):   # round 6 (G6-9, G6-10)
            pl23_put(pg, pla_plan(key, x, y, k, crown_m=cr, seed=i, distinct=k >= 0.5))   # v37 (D7): opaque
        used.add("tree_" + key)
        PL23_TREE_N[key] = PL23_TREE_N.get(key, 0) + 1
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
            out["zones"].setdefault(z["code"], []).extend(sc_rings_clip(z["P"], st, u"p20") if st else [list(z["P"])])
    for rd in ROADS + [TOWN_LINE]:
        ch = rd["change"] if rd["change"] in ROAD_CHANGE_COL else "later"
        runs = sc_lines(rd["xy"], st, u"p20") if st else [list(rd["xy"])]
        if runs:
            out["roads"].append((rd, ch, runs))
    for P in C.covered:
        out["cov"] += sc_lines(P, st, u"p20") if st else [list(P)]
    for x in (C.CL.get("W") or {}).get("runs") or []:
        P = x.get("P") or []
        if len(P) >= 2:
            for run in (sc_lines(P, st, u"p20") if st else [list(P)]):
                out["walk"].append((run, x.get("cls") == "bed", x.get("bank")))
    if C.terrace:                                         # the sightline toward the Trajaneum (off the plan)
        p2 = (C.terrace["xy"][0] + C.terrace["dir"][0] * 400.0, C.terrace["xy"][1] + C.terrace["dir"][1] * 400.0)
        out["sight"] = sc_lines([C.terrace["xy"], p2], st, u"p20") if st else [[C.terrace["xy"], p2]]
    C.pl23_clip = out
    return out


def pl23_row_box(C, row, pad=30.0):
    """v38: the survey box (x0, y0, x1, y1) m of a map row (its four corners, pad m round), for the base map"""
    V = C.V
    b = bbox([V.xy(V.u0 + row[a_], v) for a_ in ("a", "b") for v in (V.v0, V.v1)])
    return (b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad)


# round 6 (S8, BRIEF §6 row 20, G6-6, PLAN §2.6 / §5): every colour of the masterplan page from the category -> hue
# table (common/hues.py; r1 darkest = most important); the drawn item and its legend row read the same entry.
# Proposal fills transparent (alpha <= PL23_FILL_A, U28) so streets and buildings stay visible under them.
PL23_FILL_A = 0.35
PL23_HUE = {                 # legend key -> (category, rank) of PLAN §2.6
    "bld": ("CTX", 4), "bld_edge": ("CTX", 3), "her": ("HER", 4), "her_edge": ("HER", 3), "since": ("CTX", 3),
    "street": ("CTX", 3), "bridge": ("CTX", 1), "road_kept": ("CTX", 2),
    "eco": ("GRN", 3), "ring": ("PUB", 3), "flood_plant": ("GRN", 3),
    "widen": ("WW", 4), "widen_edge": ("WW", 2), "reed": ("WW", 2), "reed_edge": ("WW", 1), "arm": ("WW", 2),
    "terrace": ("WW", 1), "drytop": ("WW", 3), "drytop_edge": ("WW", 2), "spill": ("WW", 2), "spill_edge": ("WW", 1),
    "store": ("WW", 1), "cch": ("WW", 1), "hidden": ("WAT", 2),
    "dg": ("AGR", 2), "dg_edge": ("AGR", 1), "dg_gather": ("AGR", 4), "dg_row": ("AGR", 3),
    "walk": ("MOV", 1), "walk_bed": ("MOV", 1), "bike": ("MOV", 3), "foot": ("MOV", 1), "stones": ("MOV", 2),
    "canopy": ("MOV", 2), "road_pedestrian": ("MOV", 1), "road_calmed": ("MOV", 2), "road_shared": ("MOV", 3),
    "road_relocated": ("MOV", 2), "road_later": ("MOV", 1), "street_cut": ("MOV", 1),
    "square": ("PUB", 4), "square_edge": ("PUB", 2), "market": ("PUB", 1),
    "walkhub": ("PUB", 1), "transit": ("PUB", 1), "gate": ("PUB", 2), "sub": ("PUB", 2), "seat": ("PUB", 3),
    "cafe": ("PUB", 2), "edu": ("PUB", 2), "view": ("PUB", 2), "deck": ("HER", 2), "sight": ("HER", 2),
    "left": ("CTX", 2)}


def pl23_h(key):
    """the hue of a masterplan legend key (PL23_HUE -> hue(code, rank))"""
    c_, r_ = PL23_HUE[key]
    return hue(c_, r_)                                                                    # noqa: F821 (hues.py)


def pl23_cch(C):
    """round 6 (PLAN §5): the collect-clean-hold chain on the plan, once per corridor (C.pl23_cch_): the numbers 1-11
    of pages 11 and 12 (CCH_STEPS) at the places cch_points gives them (common/cch_points.py, S1: zone centroids of
    Aras's zones, 4 = the winter store, 1 / 10 the chain's entry and exit); a number with no place (6 summer strip,
    11 farmland outside, a missing zone) is left out and named in the log. dict(nums=[(n, name, xy)],
    missing=[(n, name)], store=xy|None, err=str|None)"""
    got = getattr(C, "pl23_cch_", None)
    if got is not None:
        return got
    out = dict(nums=[], missing=[], store=None, err=None)
    try:
        zs = [dict(code=z["code"], ring=list(z["P"]), study_area=z.get("own") or u"") for z in C.D.zones
              if len(z["P"]) >= 3]
        pts = cch_points(zs, log=C.pl23_log if hasattr(C, "pl23_log") else None)          # noqa: F821
        for n_ in sorted(CCH_STEPS):                                                       # noqa: F821
            xy = pts.get(n_)
            if xy is not None and C.in_study(xy):
                out["nums"].append((n_, cch_name(n_), tuple(xy[:2])))                     # noqa: F821
            else:
                out["missing"].append((n_, cch_name(n_)))                                 # noqa: F821
        out["store"] = tuple(pts["store"][:2]) if pts.get("store") else None
    except Exception as ex:                              # S1 module missing or another zone format: p23_items warns
        out["err"] = u"cch_points: {}: {}".format(type(ex).__name__, ex)
    C.pl23_cch_ = out
    return out


def pl23_street_cuts():
    """round 6 (PLAN §5): the street cuts R1-R4 of page 8, as the site board wrote them
    (cached/selinus_board/street_cuts.json {"R1": {"a": [x, y], "b": [x, y], "change": ..., "street": ...}}, survey
    m). Returns (dict, error text or None); never invented: a missing file leaves the marks out (WARNING)."""
    p_ = os.path.join(bg_cache("selinus_board"), "street_cuts.json")
    if not os.path.isfile(p_):
        return {}, u"no {} (run the site board first)".format(p_)
    try:
        with open(p_, encoding="utf-8") as f_:
            d = json.load(f_)
        return dict((k_, v) for k_, v in d.items() if isinstance(v, dict) and v.get("a") and v.get("b")), None
    except Exception as ex:
        return {}, u"{} unreadable ({}: {})".format(p_, type(ex).__name__, ex)


def pl23_bld_groups(Qs):
    """round 6 (G6-9): survey building faces (page mm) -> [[outer, courtyard, ...]] one list per building: a face
    lying inside a bigger face is its courtyard (the even-odd fill cuts it out, as round 3's one poly did)"""
    Qs = sorted(Qs, key=lambda Q: -abs(area2(Q)))
    bbs = [bbox(Q) for Q in Qs]
    out, slot = [], {}                                   # slot: index of an outer face -> its list in out
    for i, Q in enumerate(Qs):
        b = bbs[i]
        x0, y0 = inner_pt(Q)[:2]
        host = next((j for j in slot if bbs[j][0] <= b[0] and bbs[j][1] <= b[1] and bbs[j][2] >= b[2] and
                     bbs[j][3] >= b[3] and pip(x0, y0, Qs[j])), None)
        if host is None:
            slot[i] = len(out)
            out.append([Q])
        else:
            out[slot[host]].append(Q)
    return out


def draw_corridor(pg, T, k, C, inP, dw, dh, base, tint):
    """Every layer of the corridor on plan page pg (T: world -> page mm, k: mm per m; inP: world point on this
    plan's own part). Round 6 (S8, BRIEF row 20, PLAN §4): the SUBMISSION_SON page 21 drawing restored (ee52805
    draw_corridor, round 3): the masterplan's OWN survey base (buildings with heritage marked, street edges, built
    since the survey) over the soft ground tints (planting gradient C.eco, programme round the hubs C.rings), then the
    ground proposals, the water, the structures, the trees, the pictograms; base / tint (the shared muted base and
    the D9 footprint tint of round 4-5) are no longer drawn (kept as parameters for the callers). Every colour from
    the hue table (PL23_HUE, G6-6), proposal fills transparent (U28), the designed voids of round 4-5 not drawn (the
    page lists them "left as it is", as SON). Added (row 20 (c), PLAN §5): dry-top terraces (WS), spillway (WD),
    floodable planting (WP), the winter store and the card numbers 1-11 of Collect, clean, hold (pl23_cch), the
    street cuts R1-R4 (pl23_street_cuts), the producers' market at K5. Every element in its G6-9 group. Returns
    (legend keys used, name specs [dict(id, text, xy, r, study)], pictogram boxes [(box, keep name)])."""
    used, specs, icons = set(), [], []
    on = lambda Q: len(Q) >= 2 and hit(bbox(Q), (-2.0, -2.0, dw + 2.0, dh + 2.0))
    TL = lambda Ls: [Q for Q in ([T(p) for p in L_] for L_ in Ls) if len(Q) >= 3 and on(Q)]
    inside = lambda x, y, m=0.0: -m <= x <= dw + m and -m <= y <= dh + m
    big = k >= 0.5                                       # a 1:1,000 window
    fine = k < 0.15                                      # the 1:10,000 strip (fallback)
    lw = PL23_LW
    cl = pl23_prep(C)
    ins = C.in_study
    H = pl23_h
    st = C.study or None
    zc = lambda code: [Q for z in C.D.zones if z["code"] == code and len(z["P"]) >= 3
                       for Q in (sc_rings_clip(z["P"], st, u"p20") if st else [list(z["P"])])]

    def s_tint():
        with mpx_grp(pg, "ground", u"planting gradient"):  # the soft tints first (SON): planting from the water,
            for t, Ls in reversed(C.eco):                 # programme round the hubs; steps add up, each faint
                Ps = TL(Ls)
                if Ps:
                    pg.poly(Ps, fill=H("eco"), alpha=ECO_A)
                    used.add("eco")
        with mpx_grp(pg, "hubs", u"programme at the hubs"):
            for r_, Ls in reversed(C.rings):
                Ps = TL(Ls)
                if Ps:
                    pg.poly(Ps, fill=H("ring"), alpha=HUB_A)
                    used.add("ring")
        n_b = 0                                           # the survey base over the tints: every building readable,
        for role in ("building", "housing", "shed", "heritage"):   # one group each, its courtyards cut out
            her = role == "heritage"
            for Rs in pl23_bld_groups(TL(C.bld.get(role, []))):
                n_b += 1
                with mpx_grp(pg, "heritage" if her else "buildings", u"%s %d" % (role, n_b)):
                    pg.poly(Rs, fill=H("her" if her else "bld"), stroke=H("her_edge" if her else "bld_edge"),
                            lw=0.1)
                used.add("her" if her else "bld")
        for i, Q in enumerate(TL(C.built_since)):
            with mpx_grp(pg, "buildings", u"built since the survey %d" % (i + 1)):
                pg.poly([Q], fill=H("since"))
            used.add("since")
        with mpx_grp(pg, "roads", u"street edges"):
            for P in C.roads:
                Q = [T(p) for p in P]
                if on(Q):
                    pg.line(Q, H("street"), 0.3 if big else (0.1 if fine else 0.18))
                    used.add("street")
        for i, Q in enumerate(TL([R_ for R_ in zc("WP")])):   # floodable planting (WP: banks that flood)
            with mpx_grp(pg, "plants", u"floodable planting %d" % (i + 1)):
                pg.poly([Q], fill=H("flood_plant"), alpha=0.3)
            used.add("flood_plant")
        for i, Q in enumerate(TL(zc("WS"))):              # dry-top terraces (WS, P-15 name as on page 11)
            with mpx_grp(pg, "fields", u"dry-top terraces %d" % (i + 1)):
                pg.poly([Q], fill=H("drytop"), alpha=PL23_FILL_A)
                pg.line(Q + Q[:1], H("drytop_edge"), lw["outline"])
            used.add("drytop")
        for h in C.hubs:                                 # hub squares: light fill, firm edge
            for j, Q in enumerate(TL(h.get("square") or [])):
                with mpx_grp(pg, "hubs", u"hub square %s %d" % (h["id"], j + 1)):
                    pg.poly([Q], fill=H("square"), alpha=PL23_FILL_A)
                    pg.line(Q + Q[:1], H("square_edge"), lw["square"])
                used.add("square")
        dgd = pl23_dg(C)
        with mpx_grp(pg, "fields", u"Demeter's Garden"):
            for Q in TL(dgd["rings"] if dgd else cl["zones"].get("DG", [])):
                pg.poly([Q], fill=H("dg"), alpha=0.25)
                pg.line(Q + Q[:1], H("dg_edge"), lw["outline"])
                used.add("dg")
            if dgd:
                for Q in TL((dgd.get("gather") or []) + (dgd.get("cafe") or [])):
                    pg.poly([Q], fill=H("dg_gather"), alpha=0.6)
                for P in dgd.get("rows") or []:
                    Q = [T(p) for p in P]
                    if on(Q):
                        pg.line(Q, H("dg_row"), PL23_DG_ROW_LW)
                for P in (dgd.get("paths") or []) + (dgd.get("edge") or []):
                    Q = [T(p) for p in P]
                    if on(Q):
                        pg.line(Q, H("walk"), lw["walk"] * 0.7)
        for i, P in enumerate(C.terr):                   # rain terraces on the contours: ticks toward the stream
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
            with mpx_grp(pg, "fields", u"rain terrace %d" % (i + 1)):
                ticks_line(pg, Q, H("terrace"), lw["terrace"], 2.4 if big else 1.6, 0.9 if big else 0.6, side)
            used.add("terrace")

    def s_water():
        with mpx_grp(pg, "water", u"Selinos"):
            if pl23_water_draw(pg, C, T, k, on, 1.0 if big else 0.8):
                used.add("bed")
        for i, w in enumerate(C.widen):
            Q = [T(p) for p in w["ring"]]
            if len(Q) >= 3 and on(Q):
                with mpx_grp(pg, "water", u"widened stream %d" % (i + 1)):
                    pg.poly([Q], fill=H("widen"))
                    pg.line(Q + Q[:1], H("widen_edge"), lw["bank"])
                used.add("widen")
        for i, Q in enumerate(TL(cl["zones"].get("WT", []))):
            with mpx_grp(pg, "water", u"reed basins %d" % (i + 1)):
                pg.poly([Q], fill=H("reed"), alpha=PL23_FILL_A)
                pg.line(Q + Q[:1], H("reed_edge"), lw["outline"])
            used.add("reed")
        for i, Q in enumerate(TL(zc("WD"))):              # spillway: clean water back to the stream (page 11)
            with mpx_grp(pg, "water", u"spillway %d" % (i + 1)):
                pg.poly([Q], fill=H("spill"), alpha=PL23_FILL_A)
                pg.line(Q + Q[:1], H("spill_edge"), lw["outline"])
            used.add("spill")
        for i, a in enumerate(C.arms):
            Q = [T(p) for p in a["P"]]
            if on(Q):
                with mpx_grp(pg, "water", u"side arm %d" % (i + 1)):
                    pg.line(Q, H("arm"), lw["arm"])
                used.add("arm")
        for i, P in enumerate(cl["cov"]):
            Q = [T(p) for p in P]
            if on(Q):
                with mpx_grp(pg, "water", u"hidden stream %d" % (i + 1)):
                    pg.line(Q, H("hidden"), lw["hidden"], [1.6, 0.9], cap=0)
                used.add("hidden")

    def s_lines():
        for rd, ch, runs in cl["roads"]:                 # changed roads, one crisp line each (kept = context tone)
            for P in runs:
                Q = [T(p) for p in P]
                if not on(Q):
                    continue
                with mpx_grp(pg, "roads", u"%s · %s" % (rd.get("name", u"road"), ch)):
                    if ch == "later":
                        pg.line(Q, H("road_later"), lw["later"], [2.0, 1.0], cap=0)
                    elif ch == "relocated":
                        pg.line(Q, H("road_relocated"), lw["road"], [1.6, 0.6], cap=0)
                    else:
                        pg.line(Q, H("road_" + ch) if ("road_" + ch) in PL23_HUE else H("road_kept"), lw["road"])
                used.add("road_" + ch)
        for i, P in enumerate(C.bridges):
            Q = [T(p) for p in P]
            if on(Q):
                with mpx_grp(pg, "roads", u"bridge %d" % (i + 1)):
                    pg.line(Q, H("bridge"), 0.5 if big else 0.3)
                used.add("bridge")
        for c_ in C.cross:
            if not c_.get("P"):                          # v30.1: kept bridges have only "xy"
                continue
            A_, B_ = T(c_["P"][0]), T(c_["P"][1])
            if c_["kind"] == "footbridge":
                with mpx_grp(pg, "paths", u"footbridge"):
                    pg.line([A_, B_], H("foot"), lw["foot"])
                used.add("foot")
            elif c_["kind"] == "stepping stones":
                with mpx_grp(pg, "paths", u"stepping stones"):
                    for i in range(5):
                        f = (i + 0.5) / 5.0
                        pg.circle(A_[0] + (B_[0] - A_[0]) * f, A_[1] + (B_[1] - A_[1]) * f,
                                  0.9 if big else lw["stones"], fill=H("stones"))
                used.add("stones")
        for i, (P, bed, bank) in enumerate(cl["walk"]):  # the riverside walk, its bike lane one thin line beside it
            Q = [T(p) for p in P]
            if len(Q) < 2 or not on(Q):
                continue
            with mpx_grp(pg, "paths", u"%s %d" % (u"bed walk" if bed else u"riverside walk", i + 1)):
                pg.line(Q, H("walk"), lw["walk"], [1.6, 0.6] if bed else None, cap=0 if bed else 1)
                if PL23_BIKE and not bed:
                    pg.line(pl23_offset(Q, lw["bike_off"] * (1.0 if bank == "NE" else -1.0)), H("bike"), lw["bike"])
                    used.add("bike")
            used.add("walk_bed" if bed else "walk")
        for i, P in enumerate(C.canopy):
            Q = [T(p) for p in P]
            if on(Q):
                with mpx_grp(pg, "paths", u"canopied walkway %d" % (i + 1)):
                    pg.line(Q, H("canopy"), lw["canopy"], [0.8, 0.5], cap=0)
                used.add("canopy")
        for P in cl["sight"]:
            Q = [T(p) for p in P]
            if on(Q):
                with mpx_grp(pg, "annotations", u"sightline"):
                    pg.line(Q, H("sight"), lw["sight"], [1.4, 0.8], cap=0)
                used.add("sight")

    def s_veg():
        used.update(pl23_trees_draw(pg, C, T, k, (-2.0, -2.0, dw + 2.0, dh + 2.0)))
        for p, i in pl23_hub_trees(C):                   # v37 (G8, D7): kept on land, opaque
            x, y = T(p)
            if inside(x, y, 2.0):
                with mpx_grp(pg, "trees", u"Oriental plane %d" % (200 + i)):
                    pl23_put(pg, pla_plan("plane", x, y, k, crown_m=PLA_SPECIES["plane"]["crown_m"] * 0.8,
                                          seed=200 + i, distinct=k >= 0.5))
                used.add("tree_plane")
        dgd = pl23_dg(C)
        for i, (key, xs, ys) in enumerate((dgd or {}).get("shade_trees") or []):   # P23.7: the garden's shade
            x, y = T((xs, ys))
            if inside(x, y, 2.0) and key in PLA_SPECIES:
                with mpx_grp(pg, "trees", u"%s %d" % (PLA_SPECIES[key]["name"], 300 + i)):
                    pl23_put(pg, pla_plan(key, x, y, k, crown_m=PLA_SPECIES[key]["crown_m"], seed=300 + i,
                                          distinct=k >= 0.5))
                used.add(("tree_" if key in PL23_TREE_KEYS else "dg_tree_") + key)

    s_ic = 3.0 if big else (1.8 if fine else 2.2)

    def put_icon(kind, p, nm, f=1.0):
        x, y = T(p)
        if not (inside(x, y) and ins(p)):
            return False
        s_ = s_ic * f
        with mpx_grp(pg, "hubs" if kind in ("walkhub", "transit", "gate", "sub") else "annotations",
                     u"%s %s" % (kind, nm)):
            icon(pg, kind, x, y, s_)
        icons.append(((x - s_ * 0.55, y - s_ * 0.55, x + s_ * 0.55, y + s_ * 0.55), nm))
        used.add(kind)
        return True

    def s_marks():                                       # pictograms, only inside the study area (P21.5)
        for i, p in enumerate(C.seats):
            put_icon("seat", p, u"seat %d" % (i + 1), 0.8)
        for h in C.hubs:
            if not h.get("in_study"):                    # v38 (U40): a hub outside designs nothing: no symbol
                continue
            put_icon("transit" if h["role"] == "transit" else ("gate" if h["id"] == u"K6" else "walkhub"), h["xy"],
                     u"hub_icon " + h["id"], 1.25)
            if h.get("sub_xy"):
                put_icon("sub", h["sub_xy"]["c"], u"icon sub-hub " + h["id"])
        for z in C.D.zones:
            if z["code"] in ("GR", "DG"):
                put_icon("cafe", z["q"], u"icon")
            if z["code"] == "WT":
                put_icon("edu", z["q"], u"icon")
            if z["code"] == "WS" or (z["code"] == "WA" and z["tier"] == "F"):
                put_icon("seat", z["q"], u"icon")
        put_icon("edu", CRAFT_XY, u"icon")
        put_icon("deck", ROMAN_WALL, u"icon")
        if C.terrace:
            put_icon("view", C.terrace["xy"], u"icon")

    kw_ = {}                                             # round 5 (G-R5-8): the zones log line reads the legend's
    if "legend_cols" in mp_map_draw.__code__.co_varnames:   # colours and the fields in the water by design
        kw_ = dict(legend_cols=[H(k_) for k_ in ("widen", "reed", "spill", "drytop", "dg", "dg_gather", "square",
                                                  "flood_plant", "eco", "ring")],
                   water_ok=[H("widen"), H("reed"), H("spill")])
    mp_map_draw(pg, u"p20", T, [], steps={"proj_tint": s_tint, "proj_water": s_water, "proj_lines": s_lines,
                                          "proj_vegetation": s_veg, "proj_marks": s_marks},
                tint=[], study=C.study or None, **kw_)
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
    sh.items.append(("text", s, x, y, size, colour, bold, align, halo, role))   # round 5: role kept (04_items)
    return b


def pl23_wrap(s, w, size, bold=False, warn=None, page=u"p20"):
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
    less = u"no room to open it"                            # v40.2 (G-R5-4.6): no width in any list
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
        return u"Stream widened", u"room for water and a wetland beside the bank"   # v40.2: width dropped
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


# ---------------------------------------------------------------- v38 (round 4, G-R4-7, P21.2): markers
def pl23_mk_tables(C):
    """round 6 (G6-6): the marker colours = the category of what a move names, r1 (PLAN §2.6): changed roads in
    their movement shade (a kept road in the context tone), hubs public life, the water works, the hidden stream
    water, crossings movement, heritage and views heritage, the edges kept context (mk_register tables, P21.2)"""
    mk_register("road", dict((ch, pl23_h("road_" + ch)) for ch in ("calmed", "pedestrian", "shared", "kept",
                                                                    "relocated", "later")))
    mk_register("hub", dict((h["id"], hue("PUB", 1)) for h in C.hubs))                # noqa: F821
    mk_register("move", {"widen": hue("WW", 1), "arm": hue("WW", 1), "wt": hue("WW", 1), "terr": hue("WW", 1),
                         "cov": hue("WAT", 1), "foot": hue("MOV", 2), "view": hue("HER", 2), "h4": hue("HER", 2),
                         "h6": hue("HER", 2)})                                         # noqa: F821
    mk_register("kept", {"building": hue("CTX", 2), "road": hue("CTX", 2), "frame": hue("CTX", 2)})   # noqa: F821


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
    C.pl23_mk_at = {}                                     # glyph -> [(row, x, y page mm)] of its markers
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
            if spot is None:                              # v42 (L3): a move is never only in the list: its first
                if ent[4]:                                # place gets the marker on the place itself (the booklet's
                    continue                              # collision test sees it); repeats still need a free spot
                spot = (x, y)
                MPX_LOG.append(u"info p20 move %s: marker on its place (no free spot round it)" % s)
            mp_marker(sh, spot[0], spot[1], s, col, PL23_MK_PT)
            C.pl23_mk_at.setdefault(s, []).append((i, spot[0], spot[1]))   # round 5: the lists' anchors
            seen.append((i, x, y))
            ent[4] = True
            if nt["key"][0] == "kept":                    # an edge kept: one badge
                break
    V = C.V                                               # round 6 (S8, SON page 21): every area left as it is,
    order = sorted(C.nogo, key=lambda r_: -r_["ha"])      # one lowercase letter each (largest first, as SON a-q),
    for i_, r_ in enumerate(order):                       # a grey ring on its first free spot
        lt = PL23_LEFT_LETTERS[i_] if i_ < len(PL23_LEFT_LETTERS) else None
        if lt is None:
            warn.append(u"masterplan p20: more areas left as they are than letters: {:.1f} ha not lettered".format(
                r_["ha"]))
            continue
        v = dict(letter=lt, design=u"left", place=u"left as it is", reason=PL28_SRC_TAG.sub(u"", r_["why"]).strip(),
                 colour=pl23_h("left"), regions=[r_], n_map=0)
        vl.append(v)
        p = next((q for q in r_["at"] if row_of(q) is not None), None)
        if p is None:
            continue
        i = row_of(p)
        x, y = rws[i][0](p)
        spot = pl23_mk_spot(tp, x, y, pl23_mk_r(lt), rws[i][2])
        if spot is None:                                  # v42 (L3): on its place, never only in the list
            spot = (x, y)
            MPX_LOG.append(u"info p20 left-as-it-is %s: letter on its place (no free spot round it)" % lt)
        mp_marker(sh, spot[0], spot[1], lt, v["colour"], PL23_MK_PT, style="ring", name=u"left " + lt)
        C.pl23_mk_at.setdefault(lt, []).append((i, spot[0], spot[1]))
        v["n_map"] += 1
    cc = pl23_cch(C)                                      # the collect-clean-hold numbers 1-11 (pages 11, 12): a ring
    C.pl23_cch_on = []                                    # in the water works hue, apart from the solid move discs
    for n_, nm, xy in cc["nums"]:
        i = row_of(xy)
        if i is None:
            continue
        x, y = rws[i][0](xy)
        s_ = u"%d" % n_
        spot = pl23_mk_spot(tp, x, y, pl23_mk_r(s_), rws[i][2])
        if spot is None:                                  # v42 (L3): on its place, never left off the map
            spot = (x, y)
            MPX_LOG.append(u"info p20 collect-clean-hold %d: number on its place (no free spot round it)" % n_)
        mp_marker(sh, spot[0], spot[1], s_, pl23_h("cch"), PL23_MK_PT, style="ring", name=u"cch %d" % n_)
        C.pl23_cch_on.append((n_, nm, i, spot))
    return ents, vl


# v28: the route's legend samples; T7: the stream, the wetland and the trees as the plan draws them (M5 water_plan,
# M6 pla_plan: no green dots). v38 (round 4): the samples of the crisp lines, the muted base, the D9 tint, the
# designed places, one row per species with its Turkish name (D5).
def _pl23_sw_bike():
    def f(pg, x, y, w, h):
        pg.line([(x, y + h * 0.35), (x + w, y + h * 0.35)], pl23_h("walk"), PL23_LW["walk"])
        pg.line([(x, y + h * 0.35 + PL23_LW["bike_off"]), (x + w, y + h * 0.35 + PL23_LW["bike_off"])], pl23_h("bike"),
                PL23_LW["bike"])
    return f


def _pl23_sw_water():
    def f(pg, x, y, w, h):
        shp_put(pg, water_plan(rect(x, y, x + w, y + h), 1.0, spacing=0.5).shapes())
    return f


def _pl23_sw_box(fill_key, edge_key=None, alpha=None, lw=None):
    """round 6: a fill swatch exactly as the plan draws the key (fill hue, alpha, edge hue)"""
    def f(pg, x, y, w, h):
        R = rect(x + 0.3, y, x + w - 0.3, y + h)
        pg.poly([R], fill=pl23_h(fill_key), alpha=alpha)
        if edge_key:
            pg.line(R + R[:1], pl23_h(edge_key), lw or PL23_LW["outline"])
    return f


def _pl23_sw_ln(key, lw, dash=None):
    def f(pg, x, y, w, h):
        pg.line([(x, y + h / 2), (x + w, y + h / 2)], pl23_h(key), lw, dash, cap=0 if dash else 1)
    return f


def _pl23_sw_terr():
    def f(pg, x, y, w, h):
        ticks_line(pg, [(x, y + h * 0.6), (x + w, y + h * 0.6)], pl23_h("terrace"), PL23_LW["terrace"], 1.6, 0.6, -1.0)
    return f


def _pl23_sw_ring(key, glyph):
    def f(pg, x, y, w, h):
        mp_marker(pg, x + w / 2.0, y + h / 2.0, glyph, pl23_h(key), PL23_MK_PT * 0.8, style="ring")
    return f


def _pl23_sw_plant(key, d_mm=2.2):
    def f(pg, x, y, w, h):
        cr = PLA_SPECIES[key]["crown_m"]
        pl23_put(pg, pla_plan(key, x + w / 2.0, y + h / 2.0, d_mm / cr, crown_m=cr, seed=1, distinct=False))
    return f


_PL23_SP = lambda key: u"{} ({})".format(PLA_SPECIES[key]["name"], PLA_SPECIES[key]["turkish"])
# round 6 (G6-6): the legend by category (PLAN §2.6, HUE_CATS order, darker = more important inside a category);
# rows (key, category, rank, name, swatch); only what the rows draw appears. Planting species keep their own seasonal
# colours (P-3) under "Planting". Study area and the moves' / letters' markers are annotations (ANN, last).
PL23_LEGEND = [
    ("bld", "CTX", 4, u"Building (survey)", _pl23_sw_box("bld", "bld_edge")),
    ("street", "CTX", 3, u"Street edge (survey)", _pl23_sw_ln("street", 0.18)),
    ("since", "CTX", 3, u"Built since the survey", _pl23_sw_box("since")),
    ("bridge", "CTX", 1, u"Bridge", _pl23_sw_ln("bridge", 0.3)),
    ("road_kept", "CTX", 2, u"Road kept", _pl23_sw_ln("road_kept", PL23_LW["road"])),
    ("her", "HER", 4, u"Heritage building (survey)", _pl23_sw_box("her", "her_edge")),
    ("deck", "HER", 2, u"Deck, archaeology", _sw_icon("deck")),
    ("sight", "HER", 2, u"Sightline", _pl23_sw_ln("sight", PL23_LW["sight"], [1.4, 0.8])),
    ("bed", "WAT", 3, u"Selinos stream, darker = deeper", _pl23_sw_water()),
    ("hidden", "WAT", 2, u"Hidden stream line", _pl23_sw_ln("hidden", PL23_LW["hidden"], [1.6, 0.9])),
    ("terrace", "WW", 1, u"Rain terraces on the contours", _pl23_sw_terr()),
    ("reed", "WW", 2, u"Reed basins", _pl23_sw_box("reed", "reed_edge", PL23_FILL_A)),
    ("spill", "WW", 2, u"Spillway: clean water back to the stream", _pl23_sw_box("spill", "spill_edge", PL23_FILL_A)),
    ("arm", "WW", 2, u"Planted side arm", _pl23_sw_ln("arm", PL23_LW["arm"])),
    ("drytop", "WW", 3, u"Dry-top terraces", _pl23_sw_box("drytop", "drytop_edge", PL23_FILL_A)),
    ("widen", "WW", 4, u"Widened · wetland, new bank", _pl23_sw_box("widen", "widen_edge", None, PL23_LW["bank"])),
    ("cch", "WW", 1, u"1-11 Collect, clean, hold (as on page 11)", _pl23_sw_ring("cch", u"4")),
    ("eco", "GRN", 3, u"Planting gradient from the water", _pl23_sw_box("eco", None, 0.3)),
    ("flood_plant", "GRN", 3, u"Floodable planting, banks that flood", _pl23_sw_box("flood_plant", None, 0.3)),
    ("dg", "AGR", 2, u"Demeter's Garden", _pl23_sw_box("dg", "dg_edge", 0.25)),
    ("walk", "MOV", 1, u"Riverside walk", _pl23_sw_ln("walk", PL23_LW["walk"])),
    ("walk_bed", "MOV", 1, u"Bed walk, shut in floods", _pl23_sw_ln("walk_bed", PL23_LW["walk"], [1.6, 0.6])),
    ("road_pedestrian", "MOV", 1, u"Road pedestrian", _pl23_sw_ln("road_pedestrian", PL23_LW["road"])),
    ("road_later", "MOV", 1, u"Bus line, later", _pl23_sw_ln("road_later", PL23_LW["later"], [2.0, 1.0])),
    ("foot", "MOV", 1, u"New footbridge", _pl23_sw_ln("foot", PL23_LW["foot"])),
    ("street_cut", "MOV", 1, u"R1-R4 street cut (page 8)", _pl23_sw_ln("street_cut", 0.5)),
    ("road_calmed", "MOV", 2, u"Road calmed", _pl23_sw_ln("road_calmed", PL23_LW["road"])),
    ("road_relocated", "MOV", 2, u"Road relocated", _pl23_sw_ln("road_relocated", PL23_LW["road"], [1.6, 0.6])),
    ("stones", "MOV", 2, u"Stepping stones", _sw_dots(pl23_h("stones"), PL23_LW["stones"], None)),
    ("canopy", "MOV", 2, u"Canopied walkway", _pl23_sw_ln("canopy", PL23_LW["canopy"], [0.8, 0.5])),
    ("bike", "MOV", 3, u"Bike lane beside the walk", _pl23_sw_bike()),
    ("road_shared", "MOV", 3, u"Road shared", _pl23_sw_ln("road_shared", PL23_LW["road"])),
    ("walkhub", "PUB", 1, u"Walking hub", _sw_icon("walkhub")),
    ("transit", "PUB", 1, u"Transit hub", _sw_icon("transit")),
    ("market", "PUB", 1, u"Producers' market", _sw_dots(pl23_h("market"), 0.5, None)),
    ("gate", "PUB", 2, u"Gateway out", _sw_icon("gate")),
    ("sub", "PUB", 2, u"Sub-hub in the bed", _sw_icon("sub")),
    ("cafe", "PUB", 2, u"Café", _sw_icon("cafe")),
    ("edu", "PUB", 2, u"Education", _sw_icon("edu")),
    ("view", "PUB", 2, u"Viewing terrace", _sw_icon("view")),
    ("ring", "PUB", 3, u"Programme at the hubs", _pl23_sw_box("ring", None, 0.3)),
    ("seat", "PUB", 3, u"Seats", _sw_icon("seat")),
    ("square", "PUB", 4, u"Hub square", _pl23_sw_box("square", "square_edge", PL23_FILL_A, PL23_LW["square"])),
    ("study", "ANN", 0, R28_STUDY_NAME, _sw_line(BM_STUDY_LINE["colour"], BM_STUDY_LINE["width_mm"],
                                                 list(BM_STUDY_LINE["dash_mm"]))),
    ("left", "ANN", 0, u"a-z Left as it is (list)", _pl23_sw_ring("left", u"a"))] + \
    [("tree_" + k_, "GRN", 1, _PL23_SP(k_), _pl23_sw_plant(k_)) for k_ in PL23_TREE_KEYS]


# ---------------------------------------------------------------- round 5 (S6, G-R5-12): the page as items
def _pl23_north_deg(C):
    """north's turn from the drawing's +y, degrees counter-clockwise (the frame's u, v axes; as pl23_marks drew it)"""
    V = C.V
    nu, nv = V.uv((V.cx, V.cy + 1.0))
    o_u, o_v = V.uv((V.cx, V.cy))
    nu, nv = nu - o_u, nv - o_v
    L = math.hypot(nu, nv) or 1.0
    return round(math.degrees(math.atan2(-nu / L, nv / L)), 2)


def _pl23_src_key(t):
    return u"mp_" + u"".join(c if c.isalnum() else u"_" for c in t.lower())[:40]


def p23_items(ix, C, warn):
    """Round 5 (S6; G-R5-12, addendum 1 Nov 22:37 point 2; BRIEF P23.1-P23.7): the masterplan page (25-page p23, item
    page MPX_PAGE["p23"]) as items: no sheet, no side column, no scale bar, no north arrow, no burned-in page text.
    The rows are still drawn by draw_corridor into a recorder Page (rows stacked, PL23_GAP apart) so the markers keep
    their free-spot search; each row then becomes ONE true-scale drawing (mpx_drawing) in the analysis frame's own
    metres (x = m from the frame's upstream end, y = m from its foot; north_deg = north's turn from +y,
    counter-clockwise): "mp_plan_r1" (upstream half) and "mp_plan_r2" (downstream half; one "mp_plan_r1" when only
    the 1:10,000 strip fits), group "mp_plan". Markers: disc shapes in the drawing, glyph texts role "marker" (badge
    on its disc). Hub names: labels anchored at the hub (booklet placer). Legend (only what the rows draw), the moves
    by number and the designed places by letter: ix.legend / ix.list.
    Round 6 (S8, BRIEF row 20): page id p20 (MPX_PAGE); the SON page 21 drawing (draw_corridor, own survey base, no
    D9 tint); legends one per category from the hue table (G6-6, hue_log line); lists: the moves by number, the
    collect-clean-hold numbers 1-11 on the map (pl23_cch, rings in the water works hue), the areas left as they are
    a-z (SON); labels: street cuts R1-R4 (pl23_street_cuts), producers' market at K5; log lines "proposals <name>
    drawn|missing", "trees p20 ...", "groups p20 ..." (mpx_drawing). Public sources: ix.source rows (+ the round 4
    plan_sources dict under items.json "extra"). Returns log lines."""
    page = MPX_PAGE["p23"]
    lines = []
    scale, rows = pl23_rows(C, warn)
    k = 1000.0 / scale
    V = C.V
    dh = (V.v1 - V.v0) * k
    rw = [(row["b"] - row["a"]) * k for row in rows]
    W, H = max(rw), len(rows) * dh + (len(rows) - 1) * PL23_GAP
    sh = Page(W, H)
    sh.text_page(u"p20", (0.0, 0.0, W, H), margins=PL23_TP_MARGINS)
    pl23_mk_tables(C)
    pl23_water_groups(C, warn)
    base, tint = [], []                                   # round 6 (S8): SON page 21's own survey base, no D9 tint
    used, rws, boxes, icon_boxes = set(), [], [], []
    y_top = H
    for i, row in enumerate(rows):
        dw = rw[i]
        x0, y0 = 0.0, y_top - dh
        T, mine = pl23_row_T(C, row, k)
        pg = Page(dw, dh)
        u_, specs, icons = draw_corridor(pg, T, k, C, mine, dw, dh, base, tint)
        used |= u_
        blit(sh, pg, x0, y0)
        ib = []
        for b, nm in icons:                               # the pictograms: no label or marker on them
            bb = (b[0] + x0, b[1] + y0, b[2] + x0, b[3] + y0)
            sh.keep(bb, "icon", nm)
            ib.append(bb)
        Ts, _ = pl23_row_T(C, row, k, x0, y0)
        if len(rows) > 1:                                 # the match line where the halves meet (a label, anchored)
            xm = x0 + ((row["eb"] if i == 0 else row["ea"]) - row["a"]) * k
            with mpx_grp(sh, "annotations", u"match line"):
                sh.line([(xm, y0), (xm, y0 + dh)], hue("CTX", 2), 0.3, [1.6, 0.8], cap=0)          # noqa: F821
            t_ = u"match line · continues below" if i == 0 else u"match line · from above"
            tw = text_w(t_, KEY_MIN)
            sh.text(t_, xm - 1.2 - tw if i == 0 else xm + 1.2, y0 + dh - 3.0, KEY_MIN, COL["ink2"], role="label")
        specs = [dict(s_, xy=(s_["xy"][0] + x0, s_["xy"][1] + y0)) for s_ in specs]
        rws.append((Ts, mine, (x0 + PL23_ROW_PAD, y0 + PL23_ROW_PAD, x0 + dw - PL23_ROW_PAD, y0 + dh - PL23_ROW_PAD),
                    specs))
        boxes.append((x0, y0, x0 + dw, y0 + dh))
        icon_boxes.append(ib)
        y_top = y0 - PL23_GAP
    ents, vl = pl23_markers(sh, C, rws, warn)
    for nt, grp, nm, line, ok in ents:
        if not ok:
            warn.append(u"masterplan move {} has no marker on the map (no free spot on or round its places in the "
                        u"rows): only in the list ({})".format(nt["n"], nm))
    # ---- the drawings (one per row) and what is anchored on them
    nd = _pl23_north_deg(C)
    dids, kk = [], scale / 1000.0                         # kk: drawing m per page mm
    n_names = 0
    for i, row in enumerate(rows):
        b = boxes[i]
        did = u"mp_plan_r%d" % (i + 1)
        Dd = mpx_drawing(ix, did, page, sh, b, scale, origin_m=(row["a"], 0.0), dkind="plan", north_deg=nd,
                         scale_pref=sorted(set([int(scale), int(PL23_SCALE), int(PL23_FALLBACK)])), group=u"mp_plan",
                         priority=1)
        dids.append(Dd["id"])
        to_d = lambda q, b=b, row=row: (row["a"] + (q[0] - b[0]) * kk, (q[1] - b[1]) * kk)
        for bb in icon_boxes[i]:
            p0, p1 = to_d(bb[:2]), to_d(bb[2:])
            ix.keep(Dd, (p0[0], p0[1], p1[0], p1[1]), "icon")
        for s_ in rws[i][3]:                              # hub names (Turkish, G-R4-11): labels at the hub
            at = to_d(s_["xy"])
            if s_["study"]:
                ix.text(page, s_["text"], "label", drawing=Dd["id"], at=at, size_pt=PL23_NAME_PT[0], bold=True,
                        colour=COL["ink_dark"], positions=["E", "W", "NE", "NW", "N", "S", "SE", "SW"],
                        priority=3, group=u"mp_plan")
            else:                                         # a hub outside the study area: a base place name only
                ix.text(page, s_["text"], "label", drawing=Dd["id"], at=at, size_pt=PL23_BASE_NAME_PT, bold=False,
                        colour=BM_MUTED["name"], priority=7, group=u"mp_plan")
            n_names += 1
    d1 = dids[0]

    def anchor_of(glyph):
        for (i, x, y) in C.pl23_mk_at.get(glyph, ()):
            if i == 0:
                b = boxes[0]
                return (rows[0]["a"] + (x - b[0]) * kk, (y - b[1]) * kk)
        return None
    # ---- title, caption (P23.1: bigger drawings, less text)
    ix.text(page, u"Masterplan: an ecological corridor", "title", id=u"mp_plan_title", group=u"mp_plan", priority=1)
    cap = u"The corridor across the whole {}{}; the stream flows left to right.".format(
        R28_FRAME_NAME.lower(), u": upstream half on top, downstream half below" if len(rows) > 1 else u"")
    ix.text(page, cap, "caption", drawing=d1, id=u"mp_plan_caption", group=u"mp_plan", priority=1)   # v42 box
    # ---- round 6 (S8): the street cuts R1-R4 of page 8 and the producers' market at K5, labels at their place
    cuts, cerr = pl23_street_cuts()
    if cerr:
        warn.append(u"masterplan p20: street cuts R1-R4 not marked: " + cerr)
    n_cut = 0
    for rid in sorted(cuts):
        c_ = cuts[rid]
        mid = ((c_["a"][0] + c_["b"][0]) / 2.0, (c_["a"][1] + c_["b"][1]) / 2.0)
        for i, row in enumerate(rows):
            if rws[i][1](mid):
                b = boxes[i]
                x, y = rws[i][0](mid)
                ix.text(page, rid + (u" · " + c_["change"] if c_.get("change") else u""), "label", drawing=dids[i],
                        at=(row["a"] + (x - b[0]) * kk, (y - b[1]) * kk), size_pt=PL23_MK_PT, bold=True,
                        colour=pl23_h("street_cut"), priority=4, group=u"mp_plan")
                used.add("street_cut")
                n_cut += 1
                break
    k5 = next((h for h in C.hubs if h["id"] == u"K5"), None)
    if k5 is not None:
        for i, row in enumerate(rows):
            if rws[i][1](k5["xy"]):
                b = boxes[i]
                x, y = rws[i][0](k5["xy"])
                ix.text(page, u"producers' market", "label", drawing=dids[i], at=(row["a"] + (x - b[0]) * kk,
                        (y - b[1]) * kk), size_pt=PL23_BASE_NAME_PT, colour=pl23_h("market"),
                        positions=["S", "SE", "SW", "E", "W"], priority=5, group=u"mp_plan")
                used.add("market")
                break
    if getattr(C, "pl23_cch_on", None):
        used.add("cch")
    if vl:
        used.add("left")
    # ---- the legend by category (G6-6): one ix.legend per category, its rows darkest first
    cats = list(HUE_CATS) + ["ANN"]                                                       # noqa: F821
    ent = 0
    for cat in cats:
        rows_ = sorted([(rk, nm, f) for key, c_, rk, nm, f in PL23_LEGEND if c_ == cat and key in used],
                       key=lambda r_: r_[0])
        if not rows_:
            continue
        ix.legend(page, d1, [(mpx_sw(f), nm) for _rk, nm, f in rows_],
                  title=HUE_NAMES.get(cat, u"Marks") if cat != "ANN" else u"Marks",          # noqa: F821
                  id=u"mp_plan_legend_" + cat.lower(), group=u"mp_plan")
        ent += len(rows_)
    lines.append(hue_log(page) if "hue_log" in globals() else u"legend %s hues=table" % page)   # noqa: F821
    # ---- the moves by number (name · its reason line, P22.8), collect-clean-hold 1-11, the areas left as they are
    if ents:
        ns = [nt["n"] for nt, _g, _nm, _l, _ok in ents]
        numbered = ns == list(range(1, len(ns) + 1))
        texts = [(u"" if numbered else u"%d " % nt["n"]) + nm + (u" · " + line if line else u"")
                 for nt, _g, nm, line, _ok in ents]
        ix.text(page, u"The moves, by number", "heading", drawing=d1, id=u"mp_plan_moves_head", group=u"mp_plan",
                priority=3)
        ix.list(page, d1, texts, numbered=numbered, anchors=[anchor_of(u"%d" % nt["n"]) for nt, _g, _n, _l, _o in ents],
                id=u"mp_plan_moves", group=u"mp_plan")
    cc = pl23_cch(C)
    if cc["err"]:
        warn.append(u"masterplan p20: collect-clean-hold numbers not drawn ({})".format(cc["err"]))
    on_ = getattr(C, "pl23_cch_on", None) or []
    if on_:
        seen_ = []
        for n_, nm, i, spot in sorted(on_):
            if n_ not in seen_:
                seen_.append(n_)
        ix.text(page, u"Collect, clean, hold · the numbers of page 11", "heading", drawing=d1,
                id=u"mp_plan_cch_head", group=u"mp_plan", priority=3)
        ix.list(page, d1, [u"%d %s" % (n_, cch_name(n_)) for n_ in seen_], numbered=False,      # noqa: F821
                anchors=[anchor_of(u"%d" % n_) for n_ in seen_], id=u"mp_plan_cch", group=u"mp_plan")
    if cc["missing"]:
        lines.append(u"FLAG p20 collect-clean-hold numbers with no place on the plan (left out): {}".format(
            u", ".join(u"%d %s" % (n_, nm) for n_, nm in cc["missing"])))
    if vl:
        texts = [u"{} · {} · {}".format(v["letter"], u_area(v["regions"][0]["ha"] * 1e4, "ha"), v["reason"])
                 for v in vl]
        ix.text(page, u"Left as it is · no intervention, because", "heading", drawing=d1,
                id=u"mp_plan_left_head", group=u"mp_plan", priority=3)
        ix.list(page, d1, texts, numbered=False, anchors=[anchor_of(v["letter"]) for v in vl], id=u"mp_plan_left",
                group=u"mp_plan")
    # ---- sources (public only, as round 4's plan_sources)
    ps = pl28_plan_sources(ents, vl)
    seen = set()
    for m_ in ps["markers"]:
        for s_ in m_["sources"]:
            if s_["text"] not in seen:
                seen.add(s_["text"])
                ix.source(_pl23_src_key(s_["text"]), s_["text"], None, page=page)
    for v in ps["left_as_is"]:
        for t in v["sources"]:
            if t not in seen:
                seen.add(t)
                ix.source(_pl23_src_key(t), t, None, page=page)
    ix.d.setdefault("extra", {})["plan_sources"] = ps
    if getattr(C, "pl23_dg_err", None):
        warn.append(u"masterplan p20: Demeter's Garden design not drawn ({}): the zone-base field is drawn".format(
            C.pl23_dg_err))
    elif pl23_dg(C) is None:
        lines.append(u"FLAG p20 Demeter's Garden: no dg_design (parts/02g_demeter.py) or no outline: the zone-base "
                     u"field is drawn")
    C.ni_placed = sum(1 for r_ in C.nogo if r_.get("placed"))
    MPX_PAGES.append(("A", "p23", sh))
    n_on = sum(1 for e in ents if e[4])
    lines.append(u"p20 (items {}): {} row(s) at 1:{:,.0f}; moves {} ({} on the map); left as it is {} ({} lettered "
                 u"on the map); collect-clean-hold numbers {} on the map, {} left out; street cuts {}; hub names {}; "
                 u"legend rows {}".format(page, len(rows), scale, len(ents), n_on, len(vl),
                                          sum(v["n_map"] for v in vl), len(on_), len(cc["missing"]), n_cut, n_names,
                                          ent))
    for nm_ in (u"walking hubs", u"transit hub", u"gateway K6", u"sub-hubs in the bed", u"reed basins", u"side arm",
                u"widened wetland", u"footbridge", u"stepping stones", u"Demeter's Garden", u"riverside walk",
                u"bed walk", u"bike lane", u"forest corridor", u"viewing terrace", u"canopied walkway",
                u"bus line later", u"spillway", u"winter store", u"dry-top terraces", u"floodable planting",
                u"steps 1-11", u"street changes R1-R4", u"producers' market"):
        key_ = {u"walking hubs": "walkhub", u"transit hub": "transit", u"gateway K6": "gate",
                u"sub-hubs in the bed": "sub", u"reed basins": "reed", u"side arm": "arm", u"widened wetland": "widen",
                u"footbridge": "foot", u"stepping stones": "stones", u"Demeter's Garden": "dg",
                u"riverside walk": "walk", u"bed walk": "walk_bed", u"bike lane": "bike",
                u"forest corridor": "tree_plane", u"viewing terrace": "view", u"canopied walkway": "canopy",
                u"bus line later": "road_later", u"spillway": "spill", u"dry-top terraces": "drytop",
                u"floodable planting": "flood_plant", u"street changes R1-R4": "street_cut",
                u"producers' market": "market"}.get(nm_)
        ok_ = (any(n_ == 4 for n_, _nm, _i, _s in on_) if nm_ == u"winter store" else
               (bool(on_) if nm_ == u"steps 1-11" else
                (any(k_.startswith("tree_") for k_ in used) if key_ == "tree_plane" else key_ in used)))
        lines.append(u"proposals {} {}".format(nm_, u"drawn" if ok_ else u"missing"))
    lines.append(u"trees {} species={} generic=0 (proposed planting, species from the planting rule; no survey "
                 u"trees on this plan)".format(page, sum(PL23_TREE_N.values())))
    PL23_TREE_N.clear()
    lines.append(u"proposals boardwalk missing (no plan geometry: section W4 only; left out, PLAN §5)")
    return lines
