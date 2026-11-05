# p.02-03 what is there, site readings, edge types and the axonometrics (split from parts/03_street_w.py, parts/04_river_faces.py, parts/06_draw_legend_items.py, parts/14_tsec_wind_arrows.py, parts/15e_v45_pages.py, parts/15l_r28_site.py, parts/16_write_city_link_movement.py, parts/17_board_fits.py on 29 Oct 2026; moved unchanged)


def road_lines(S, B, V, L, order, casing=None, surface=ROADC, min_w=0.06, paths=False, fill=None, hatch=True):
    """Streets at their surveyed width: the surface between its two edges (one outline per block of streets, so
    junctions are clean); a street whose width the survey does not show is a single thin line on its centre.
    Footpaths optional as thin dashes. v16.5: the street surfaces hatched (fine 45-degree lines, a shade darker than
    the edges' paper) in every plan that shows them."""
    casing = casing or mix(INK, PAPER, 0.5)
    net = getattr(S, "road_net", None)
    if net:
        col = fill if fill is not None else surface
        hc = mix(casing, col, 0.2)
        for rg_ in net:
            if hatch and ROAD_SOLID:                      # v16.7: one solid colour
                B.fill(V.Ps([rg_["P"]] + rg_["H"]), ROAD_FILL if fill is None else col, L, order)
                continue
            B.fill(V.Ps([rg_["P"]] + rg_["H"]), col, L, order)
            if hatch:
                B.hatch(V.Ps([rg_["P"]] + rg_["H"]), hc, L, order, ROAD_HATCH_SP * S.U, w=ROAD_HATCH_W)
        for P in getattr(S, "road_lines_net", []):
            B.line(V.P(P), casing, L, order + 1, 0.05)
        for r in S.roads:
            if not r.get("w"):
                B.line(V.P(r["P"]), casing, L, order + 1, 0.06)
    else:
        s = V.s
        rs = sorted(S.roads, key=lambda r: r["tags"].get("highway") in MAIN_ROADS)
        for r in rs:
            if r.get("w"):
                B.line(V.P(r["P"]), casing, L, order, max(min_w, r["w"] * s * MMU) + 0.07)
            else:
                B.line(V.P(r["P"]), casing, L, order, 0.07)
        for r in rs:
            if r.get("w"):
                B.line(V.P(r["P"]), surface, L, order + 1, max(min_w, r["w"] * s * MMU))
    if paths:
        for p in S.paths:
            for d in dashes(V.P(p["P"]), 0.3 * S.U, 0.2 * S.U):
                B.line(d, casing, L, order + 1, 0.05)


def river_free_banks(S, step=2.0, near=1.5):
    """Pieces of the surveyed stream lines lying clear of the merged river."""
    M = getattr(S, "water_mask", None)
    if M is None:
        return []
    r = max(1, int(round(near / M["cell"])))
    out = []
    for P in S.banks:
        run = []
        for x, y in resample(P, step):
            u, v = S.F.local(x, y)
            i, j = int(math.floor((u - S.F.u0) / M["cell"])), int(math.floor((v - S.F.v0) / M["cell"]))
            hit = False
            for jj in range(j - r, j + r + 1):
                if 0 <= jj < M["ny"] and (M["rows"][jj] >> max(0, i - r)) & ((1 << (2 * r + 1)) - 1):
                    hit = True
                    break
            if hit:
                if len(run) >= 2:
                    out.append(run)
                run = []
            else:
                run.append((x, y))
        if len(run) >= 2:
            out.append(run)
    return out


# ============================================================ THE LAND-USE MAP
def draw_landuse_map(S, B, V, bcol=None, den=None, kb=10.0, inside=None):
    """bcol (v33): the colour of each building (default: its land-use colour). Revision 30 Oct (G7, M11): the buildings
    through _p02_bld_plan (outline per block + roof reading at 1:den; kb = board units per booklet mm), no piece
    outlines. v59 (round 4, P02.2, G-R4-4): inside = _p02_inside(S): buildings outside the study area are base map
    (no cast shadow, no roof reading, the light base outline)."""
    L = "LU_BOARD::Map"
    s = V.s
    U = S.U
    # v61 (round 6, G6-6): colours from the hue table (_p02_hue, P02_HUE); G6-9: every layer drawn in its kind
    # (B.kind), each item its own element, each tree named by its species (G6-10, sb_tree_species)
    with B.kind("ground"):
        B.fill([V.P(S.F.P)], PAPER, L + "::paper", 2)
        draw_landcover(S, B, V, L + "::landcover", 3)   # v31: under the surveyed / OSM ground (4)
    for z in S.zones:
        if z["kind"] == "green":
            col = _p02_hue("g_" + str(z["sub"]), GREEN_SUB.get(z["sub"], CAT["green"][1])) \
                if z["sub"] in GREEN_SUB else _p02_hue("g_park", CAT["green"][1])
        elif z["kind"] == "transport":
            col = _p02_hue("transport", mix(CAT["transport"][1], PAPER, 0.3))
        else:
            col = _p02_hue(z["kind"], CAT[z["kind"]][1])
        with B.kind("fields" if z["kind"] == "agri" else "ground"):
            B.fill(V.Ps(z["Ps"] + z["Hs"]), col, L + "::" + z["kind"], 4)
            if z["kind"] == "vacant" and TEXTURE:
                for ln in hatch_lines(z["Ps"], z["Hs"], z["bb"], 5.0, math.radians(45)):
                    B.line(V.P(ln), mix(INK, PAPER, 0.55), L + "::texture", 5, 0.06)
            if z["kind"] == "agri" and z["sub"] == "field" and TEXTURE:
                ang = (_zlib_crc(repr([round(v_, 2) for v_ in z["bb"]]).encode("utf-8")) % 180) * math.pi / 180.0
                for ln in hatch_lines(z["Ps"], z["Hs"], z["bb"], 7.0, ang):
                    B.line(V.P(ln), mix(_p02_hue("agri", CAT["agri"][1]), INK, 0.22), L + "::texture", 5, 0.04)
    wc, wl = _p02_hue("water", CAT["water"][1]), _p02_hue("water_line", BLUE_D)
    with B.kind("water"):
        for w in S.water:
            B.fill(V.Ps([w["P"]] + w.get("H", [])), wc, L + "::water", 6)
    with B.kind("roads"):
        for q in getattr(S, "decks", []):
            B.fill([V.P(q)], ROADC, L + "::streets", 7)
    with B.kind("water"):
        for P in getattr(S, "covered", []):          # the covered course: a hidden line over the streets and roofs
            for d in dashes(V.P(P), 0.35 * U, 0.25 * U):
                B.line(d, wl, L + "::water", 19, 0.12)
        for P in S.water_outline:                     # the river edge: one continuous line per stretch (under decks)
            B.line(V.P(P), wl, L + "::water", 6, 0.13)
        for P in river_free_banks(S):                 # other surveyed streams and ditches, thinner
            B.line(V.P(P), wl, L + "::water", 7, 0.07)
        for P in S.pools:
            B.line(V.P(P), wl, L + "::water", 7, 0.08)
    with B.kind("roads"):
        road_lines(S, B, V, L + "::streets", 8, casing=ROAD_EDGE, surface=ROADC, min_w=0.04,
                   fill=_p02_hue("streets", ROAD_FILL))
        for p in S.paths:                             # paths whose width the survey does not show: a thin line
            if not p.get("w"):
                B.line(V.P(p["P"]), ROADC, L + "::streets", 9, 0.04)
    if TEXTURE:
        tcol = _p02_hue("tree_sym", None)
        for i_, (x, y, r, kind) in enumerate(S.trees):    # the survey's tree symbols (R5: no crown, unspecified,
            sp = sb_tree_species(S, x, y, None, None, r, None, page="p02")[0] \
                if "sb_tree_species" in globals() else None                    # but R0 the named K4 trees)
            ss_ = _P02.setdefault("sym_sp", {})
            ss_[sp] = ss_.get(sp, 0) + 1
            bx, by = V.p(x, y)
            with B.kind("trees", u"%s s%d" % (sp or "tree", i_)):
                B.fill([circle_pts(bx + 0.35 * r * s, by - 0.35 * r * s, r * s, 14)], TREE_SHADOW, L + "::trees", 10)
                tc_ = tcol if tcol is not None else TREE_COLS.get(kind, TREE_COLS["tree"])
                B.fill([circle_pts(bx, by, r * s, 14)], tc_, L + "::trees", 11)
                if kind == "pine":
                    B.fill([circle_pts(bx - 0.25 * r * s, by + 0.25 * r * s, 0.45 * r * s, 10)],
                           mix(tc_, PAPER, 0.35), L + "::trees", 12)
        sh = mix(INK, PAPER, 0.6)
        with B.kind("buildings"):
            for u in S.bld:
                if not _p02_u_inside(inside, u):         # v59 (round 4, P02.2): the base houses cast no dark shadow
                    continue
                off = min(3.0, 0.11 * u["h"]) * s
                B.fill([[(x + off, y - off) for x, y in V.P(P)] for P in u["parts"] + (u.get("holes") or [])], sh,
                       L + "::texture", 13)
    _p02_bld_plan(S, B, V, L + "::buildings", 14, den or crop_scale(V.s) or 1000.0, kb, bcol=bcol,
                  inside=inside)                          # v59 (round 4, P02.2)
    with B.kind("ground"):
        for P in S.slope_hatch:
            B.line(V.P(P), mix(INK2, PAPER, 0.4), L + "::ground", 16, 0.04)
        for P in S.slopes:
            B.line(V.P(P), INK2, L + "::ground", 16, 0.08)
        for P in S.stairs:
            B.line(V.P(P), INK2, L + "::ground", 16, 0.05)
        for P in S.fences:
            B.line(V.P(P), mix(INK2, PAPER, 0.3), L + "::ground", 16, 0.04)
        for P in S.park_lines:
            for d in dashes(V.P(P), 0.4 * U, 0.28 * U):
                B.line(d, mix(_p02_hue("g_park", CAT["green"][1]), INK, 0.3), L + "::ground", 16, 0.08)
        for P in S.walls:
            B.line(V.P(P), INK, L + "::walls", 17, 0.16)
    with B.kind("roads"):
        for P in S.bridges:
            B.line(V.P(P), INK, L + "::walls", 18, 0.24)


def site_crowns(S, F2):
    """Canopy-map crowns (modelled, Meta/WRI 1 m canopy height map) inside F2: [(x, y, r, h, leaf, leaf_src)]. v61
    (G6-10): from the environment file's rows (crowns_near_full: leaf and leaf_src kept, so sb_tree_species can name
    the species); without the environment file the built-in SEAM_PACK rows, which carry no leaf_src: those crowns
    stay generic (leaf_src None, _p02_sp gives them no species). _P02["crown_src"] says which."""
    rows = []
    if "crowns_near_full" in globals():
        try:
            fb = S.F.bb
            rows = [tuple(c_[:6]) for c_ in crowns_near_full(S, (fb[0] - 80, fb[1] - 80, fb[2] + 80, fb[3] + 80))]
        except Exception:
            rows = []
    if rows:
        _P02["crown_src"] = "env"
        return [c_ for c_ in rows if F2.inside(c_[0], c_[1])]
    _P02["crown_src"] = "pack"
    rows = seam_pack().get("crowns", {}).get("rows", [])
    return [(r[0], r[1], r[2], r[3], r[4], None) for r in rows if F2.inside(r[0], r[1])]


def _p02_sp(S, c):
    """v61 (G6-10): the species glyph key (plane / olive / stone_pine) of one p.02 crown c = (x, y, r, h, leaf,
    leaf_src), or None = generic (never named): sb_tree_species once per crown per run (plan 01 and the edge strip
    draw the same crown; it is counted once for `trees p02`). A SEAM_PACK crown (no leaf_src) is generic."""
    key = (c[0], c[1])
    if key in P02_SP:
        return P02_SP[key]
    sp = None
    if c[5] is not None and "sb_tree_species" in globals():
        try:
            sp = sb_tree_species(S, c[0], c[1], c[4], c[5], c[2], c[3], page="p02")[0]
        except Exception:
            sp = None
    else:                                                 # counted as a generic tree (SEAM_PACK row or no module)
        n_ = SB_TREE_N.setdefault("p02", {}) if "SB_TREE_N" in globals() else {}
        n_["tree"] = n_.get("tree", 0) + 1
    P02_SP[key] = sp
    return sp


def _p02_sp_name(sp):
    """v61 (G6-10): a species glyph key's name for a legend row (common/trees.py TREE_SPECIES), else the key"""
    try:
        return (TREE_SPECIES.get(sp) or {}).get("name") or sp.replace(u"_", u" ")                # noqa: F821
    except Exception:
        return (sp or u"").replace(u"_", u" ")


def dense_outline(S, cls_min=3, min_cells=20):
    """The outline of the densest grain: groups of at least min_cells touching cells of intensity class >= cls_min
    (10 m cells, so 20 cells = 2,000 m2); single dense cells are left out (they outline one building, not an area)."""
    cells = [P for P, cls, j in getattr(S, "int_cells", []) if cls >= cls_min]
    key = lambda a, b: tuple(sorted(((round(a[0], 2), round(a[1], 2)), (round(b[0], 2), round(b[1], 2)))))
    par = list(range(len(cells)))

    def find(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i
    owner, cnt = {}, {}
    for i, P in enumerate(cells):
        for k in range(len(P)):
            e = key(P[k], P[(k + 1) % len(P)])
            cnt[e] = cnt.get(e, 0) + 1
            if e in owner:
                a, b = find(i), find(owner[e])
                if a != b:
                    par[a] = b
            else:
                owner[e] = i
    size = {}
    for i in range(len(cells)):
        r = find(i)
        size[r] = size.get(r, 0) + 1
    return [list(e) for e, c in cnt.items() if c == 1 and size[find(owner[e])] >= min_cells]


def c5_point(S):
    if not getattr(S, "study_areas", None):
        return C5_XY
    best = None
    for a in getattr(S, "study_areas", []) or []:
        if a["name"] == "BEGUM" and (best is None or a["area"] > best["area"]):
            best = a
    if not best:
        return None
    _a, cx, cy = shoelace(best["P"])
    return (cx, cy)


P02_OUT_FADE = 0.22       # round 2 (PG1 p2 #8): share mixed toward the paper for buildings outside the study area
#                           (a drawing choice: "reduce the opacity a little, but not too much"). v59: no longer read
#                           (outside the study area the houses take the muted base tone, P02_BASE_BLD)
P02_IN_LIGHT = 0.40       # v59 (round 4, P02.2, G-R4-4): share each urban-fabric colour is mixed toward the paper inside
#                           the study area (Aras U61 "the dark house mass": the fabric reading stays, lighter)
P02_BASE_BLD = C(BM_MUTED["bld"]) if "BM_MUTED" in globals() else C("EDEBE6")         # v59 (round 4, P02.2, G-R4-4):
P02_BASE_EDGE = C(BM_MUTED["bld_edge"]) if "BM_MUTED" in globals() else C("C9C5BC")   # PLAN 4.3 base house tones
P02_BASE_LW = 0.12        # v59 (round 4, P02.2): mm, the base house outline (PLAN 4.3)


def _p02_inside(S):
    """v59 (round 4, P02.2, G-R4-4): f(x, y) -> True where (x, y) lies inside a study-area outline (r28_study), or
    None when the study area is not in the data (then every building keeps its fabric tone)"""
    polys = [(P, bb_pts(P)) for P in (getattr(getattr(S, "site", S), "r28_study", None) or []) if len(P) >= 3]
    if not polys:
        return None

    def f(x, y):
        return any(bb[0] <= x <= bb[2] and bb[1] <= y <= bb[3] and region_contains(x, y, [P], []) for P, bb in polys)
    return f


def _p02_u_inside(inside, u):
    """v59 (round 4, P02.2): a building counts as inside when its first part's centre is (the round 2 rule)"""
    if inside is None or not u.get("parts"):
        return True
    P0 = u["parts"][0]
    return inside(sum(p_[0] for p_ in P0) / len(P0), sum(p_[1] for p_ in P0) / len(P0))


def _p02_fab_light(c_):
    """v59 (round 4, P02.2): an urban-fabric colour as plan 01 draws it inside the study area (and its key shows it).
    v61 (G6-6): the hue table's tone as it is (P02_HUE already takes each fabric type one rank lighter, the v59
    lightening); the v59 mix toward the paper only without the table"""
    return c_ if "hue" in globals() else mix(c_, PAPER, P02_IN_LIGHT)


def _p02_fade_col(S):
    """round 2 (PG1 p2 #8, M3 fade, U20): plan 01's building colour by urban fabric. v59 (round 4, P02.2, G-R4-4; Aras
    U61 "gereksiz bir ev kalabalığı koyu renkliliği"): inside the study area the fabric colour mixed P02_IN_LIGHT
    toward the paper (_p02_fab_light); outside it every building takes the muted base house tone P02_BASE_BLD (base
    map back, light); everywhere the fabric tone when the study area is not in the data"""
    inside = _p02_inside(S)

    def col(u):
        if _p02_u_inside(inside, u):
            return _p02_fab_light(fabric_col(u))
        return _p02_hue("bld_out", P02_BASE_BLD)
    return col


def fabric_col(u):
    """v40: a building on plan 01 by its fabric type (the fabric map's rule: sheds and annexes paler). v61 (G6-6): the
    hue table's tone of its fabric type (P02_HUE "fab_<type>"); a heritage building whose name the table ranks r1 (the
    World Heritage listing, common/hues.py her_rank) takes HER r1."""
    fab = u.get("fabric", "regular")
    col = _p02_hue("fab_" + fab, FABRIC_PLAN[fab])
    if fab in ("monument", "sacred") and _p02_her1(u):
        col = C(hue("HER", 1))                                                               # noqa: F821
        _P02.setdefault("her1", set()).add(u.get("proper") or u.get("name"))
    return mix(col, PAPER, 0.45) if u["annex"] else col


def _p02_her1(u):
    """v61 (G6-6, H3): True when the building's own name is a heritage place the hue table ranks r1 (Akropol, Kızıl
    Avlu: her_rank); False without a name or the module"""
    nm = u.get("proper") or u.get("name") or u""
    if not nm or "her_rank" not in globals() or "hue" not in globals():
        return False
    try:
        return her_rank(nm) == 1                                                             # noqa: F821
    except Exception:
        return False


def draw_what_is_there(S, B, x, y, w, U):
    """S1: the site as it is on one plan, the frame and CONTEXT_M of quiet context, at the board scale. Returns the
    y below its legend."""
    L = "LU_BOARD::WhatIsThere"
    F = S.F
    RF = getattr(S, "range_F", None)                      # v36: set on the whole-file model: the analysis range
    F2 = F if RF is not None else context_frame(F)
    r_map = bcite("Plan 01: the map covers the whole survey file; the thin line is the analysis frame (site_alan). Crowns "
                  "exist for the site only." if RF is not None else
                  "Plan 01: context beyond the frame: survey line work only.")
    B.text("WHAT IS THERE · GROUND · BUILDINGS · GREEN · STREAM EDGE " + r_map, x, y, 1.05 * U, INK, L,
           font=FONT_TITLE, bold=True)                    # v38: keywords; the coverage note is a key entry
    # v45: plan 01 prints at 1:den_bk beside the site readings (P02_MAP_W mm wide): its marks and words are sized for
    # that page (kb = board units per booklet mm; the map is as wide as w)
    den_bk = bk_std(F2.w * 1000.0 / P02_MAP_W)        # revision 30 Oct (G2, M1): 7 grid columns wide
    kb = w / F2.w * den_bk / 1000.0
    # v51 (WO-T3a-2, p.02 flipped): what the plan shows is no longer a line over the map; the map starts under the
    # title. v58 (round 3, P02.1): its key is directly under the map, in this crop (_p02_key_under)
    _P02.clear()
    # v58 (round 3, G2): the map prints map_mm wide at 1:den_bk; the side column takes the whole grid columns it leaves
    # (6 for a map <= 194 mm, as the 1:25,000 plan: no 44 mm dead band between map and side column any more)
    map_mm = F2.w * 1000.0 / den_bk
    n_map = next((n_ for n_ in range(1, GRID_COLS + 1) if grid_w(n_) >= map_mm - 0.01), GRID_COLS)
    _P02["side_w"] = grid_w(max(5, min(6, GRID_COLS - n_map)))
    # v58 (round 3, G16): no bridge codes in the words (the booklet intro says the finding, G4)
    _P02["text"] = (u"The survey area today: **buildings** by urban fabric, **ground and green**, the **Selinos stream** "
                    u"with its edges and six bridges, and where stream and town **clash**.")
    ymap = y - 0.8 * U
    V, mw, mh = view_fit(F2, x, ymap, w, 10.0 * w)
    s = V.s
    i_map0 = len(B.items)                                 # v59 (round 4, P02.1): the map's own texts start here
    P02_SP.clear()                                        # v61 (G6-10): the crowns' species, once per run ...
    if "SB_TREE_N" in globals():
        SB_TREE_N.pop("p02", None)                        # ... and the page's species counts (sb_tree_log)
    # quiet context: survey line work around the frame, pale
    with B.kind("ground"):
        B.fill([V.P(F2.P)], mix(PAPER, (255, 255, 255), 0.55), L, 1)
    ctx = getattr(S, "ctx_lines", None) or {}
    for key, col, wd in (("water", mix(BLUE_D, PAPER, 0.5), 0.06), ("road", mix(INK2, PAPER, 0.62), 0.04),
                         ("bld", mix(INK2, PAPER, 0.45), 0.04)):
        with B.kind({"water": "water", "road": "roads"}.get(key, "buildings")):
            for a, b in ctx.get(key, []):
                B.line([V.p(*a), V.p(*b)], col, L, 2, wd)
    # the site: land use, land cover, ground, streets, trees, buildings (homes by fabric), walls, bridges
    # v40: buildings by urban fabric type; revision 30 Oct (G7, M11): outline per block + roof, no piece lines
    # round 2 (PG1 p2 #8, U20): the town fabric outside the study area a little fainter, "but not too much"
    draw_landuse_map(S, B, V, bcol=_p02_fade_col(S), den=den_bk, kb=kb, inside=_p02_inside(S))   # v59 (P02.2)
    # canopy-map crowns (modelled), under the surveyed tree symbols. v61 (G6-10, G6-9): each crown its own element
    # named by its species (sb_tree_species via _p02_sp; None = generic "tree"), its colour by leaf type (GRN ranks)
    crowns = [c for c in site_crowns(S, F) if F.inside(c[0], c[1])]
    sp_leaf = {}                                          # leaf type -> {species glyph or None: n}, for the key
    for i_, c_ in enumerate(crowns):
        cx, cy, r, h, lf = c_[:5]
        if lf not in (0, 1, 2):
            continue
        sp = _p02_sp(S, c_)
        sp_leaf.setdefault(lf, {})[sp] = sp_leaf.setdefault(lf, {}).get(sp, 0) + 1
        q_ = V.p(cx, cy)
        with B.kind("trees", u"%s %d" % (sp or "tree", i_)):
            B.fill([circle_pts(q_[0], q_[1], max(0.06 * U, r * s), 10)],
                   _p02_hue("crown_%d" % lf, mix(LEAF_COL[lf], PAPER, 0.25)), L, 10)
    # footpaths (the open-space network's links)
    path_c = _p02_hue("path", mix(CAT["green"][1], INK, 0.35))
    with B.kind("paths"):
        for p in S.paths:
            for d in dashes(V.P(p["P"]), 0.35 * U, 0.25 * U):
                B.line(d, path_c, L, 19, 0.16)
    # dense fabric (intensity): the outline of the densest floor-area class
    dens = dense_outline(S)
    dc = _p02_hue("dense", mix(INTENSITY[3], INK, 0.1))
    with B.kind("annotations", "densest grain"):
        for a, b in dens:
            B.line([V.p(*a), V.p(*b)], dc, L, 23, 0.3)
    # stream thresholds, thinner, along the banks
    with B.kind("water"):
        for typ, pts in getattr(S, "edge_runs", []):
            B.line(V.P(pts), _p02_hue("edge_" + typ, EDGE[typ][1]), L, 24, THRESH_W)
        for pts in getattr(S, "wall_runs", []):
            for d in dashes(V.P(pts), 0.16 * U, 0.14 * U):
                B.line(d, PAPER, L, 25, THRESH_W * 0.4)
    # frame, river name, section marks (shared with the section drawings)
    with B.kind("labels"):
        draw_map_annotations(S, B, V, U, rh=bk_hk(8.0, kb))   # v45: no cut lines; the stream's name 8 pt
    with B.kind("frame"):
        B.line(V.P(F.P + [F.P[0]]), INK, L, 26, 0.25)
        if RF is not None:                                # v36: the analysis range (site_alan) on the whole-file map
            B.line(V.P(RF.P + [RF.P[0]]), INK, L, 26, 0.12)
    with B.kind("annotations", "study area"):
        draw_r28_study(getattr(S, "site", S), B, V, kb, L, order=27)    # v50 (MIRAQUA 28 Oct, G8): the study area
    # bridges and conflicts (v40, Aras 25 Oct 21:41: drawn marks with plain short labels, no boxes, no sentences).
    # v51 (WO-T3a-2): the photo viewpoints 1-8 are gone from this map (the page has no photos; p.06 keeps them)
    cs = list(CONFLICTS_C)
    c5 = c5_point(S)
    if c5:
        cs.append(("C5", c5[0], c5[1], C5_TEXT))
    # v59 (round 4, P02.1, G-R4-1, G-R4-7, G-R4-9; Aras U61 S31: the C markers "birbiri iç içe girmiş üst üste binmiş"
    # and on the numbers 1-5). Interpretation: the "cut numbers 1-5" are the bridge marks (plan 01 draws no section
    # cut since v45), so each bridge is drawn as a BRIDGE (the map symbol: two deck lines across the stream with
    # flared ends, never a single cut-like stroke) and its number in a ring marker (mk_marker, the ink the bridges are
    # drawn in); each conflict a solid marker in the conflict colour (mk_marker; its key under the map shows the same
    # disc). Placed in booklet mm by _p02_spot: bridge numbers first beside their symbol, then the conflicts, each
    # clear of the bridge symbols, every marker placed before it, the map's own texts and the other conflict points
    # (pad SB_TP_PAD); a conflict that cannot sit on its point gets a dot on the point and a short leader to its
    # marker. No marker overlaps another: the page check (sb_text_check) sees the glyphs.
    # v61 (round 6, G6-4, G6-8; SON page2 overlaps "5 / 6 / C1" x "C5 / C6", the bridge 1-6 / clash C1-C6 cluster):
    # every marker keeps P02_MK_PAD (now 1.2 mm, twice the page check's pad) clear of every other marker and text,
    # the conflicts look further out (to 10 mm) and draw NO leader line and no dot (G6-4: no leader lines on a plan);
    # conflicts in the annotation ink of the hue table (ANN 2C2219, was the accent 8B3A3F)
    mb = ymap - mh
    knum = _p02_knum()
    mk_register("bridge", dict((k_, crop_hex(INK)) for k_ in knum))
    mk_register("conflict", dict((c_[0], crop_hex(_p02_hue("conflict", MARK_C))) for c_ in cs))
    pad = P02_MK_PAD
    bnd = (V.X0 / kb + 0.8, mb / kb + 0.8, (V.X0 + mw) / kb - 0.8, ymap / kb - 0.8)      # booklet mm, inside the crop
    # v61 (G6-4): first the cuts as an_cut marks just outside the drawing = the analysis frame F (the thick line), in the
    # quiet context band round it, at least P02_CUT_IN mm inside the crop's edges so no letter is cut by the crop; drawn
    # before the markers, which then keep clear of their names (taken)
    fq = V.P(F.P)
    fin = P02_CUT_IN * kb
    _p02_drawing_marks(B, V, kb, L, (max(min(q_[0] for q_ in fq), V.X0 + fin), max(min(q_[1] for q_ in fq), mb + fin),
                                     min(max(q_[0] for q_ in fq), V.X0 + mw - fin),
                                     min(max(q_[1] for q_ in fq), ymap - fin)))
    taken = _p02_text_boxes(B, i_map0, kb)                # the map's texts so far (stream name, cut names), mm
    ticks, ovl = [], []
    cpts = [(k_, cx_, cy_) for k_, cx_, cy_, t_ in sorted(cs) if F.inside(cx_, cy_)]
    for k, nm, bx, by in BRIDGES_K:                       # the bridge symbol across the stream
        if F.inside(bx, by) and k in knum:
            px, py = V.p(bx, by)
            n = stream_normal(S, bx, by) or (0.0, 1.0)
            a_ = V.p(bx + n[0], by + n[1])
            ln = math.hypot(a_[0] - px, a_[1] - py) or 1.0
            ux, uy = (a_[0] - px) / ln, (a_[1] - py) / ln        # across the stream (page)
            vx, vy = -uy, ux                                     # along it
            hl, hg, fl = P02_BR_HALF * kb, P02_BR_GAP * kb, 0.45 * kb
            with B.kind("roads", u"bridge %s" % k):       # v61 (G6-9): each bridge one element
                for sg in (-1.0, 1.0):                    # the two deck edges, each end flared away from the deck
                    ox, oy = sg * hg * vx, sg * hg * vy
                    e0 = (px + ox - hl * ux, py + oy - hl * uy)
                    e1 = (px + ox + hl * ux, py + oy + hl * uy)
                    B.line([(e0[0] - fl * (ux - sg * vx) * 0.7, e0[1] - fl * (uy - sg * vy) * 0.7), e0, e1,
                            (e1[0] + fl * (ux + sg * vx) * 0.7, e1[1] + fl * (uy + sg * vy) * 0.7)],
                           INK, L, 62, bk_lw(0.25, kb))
            cn_ = [((px + a1 * (hl + fl) * ux + a2 * (hg + 0.35 * kb) * vx) / kb,
                    (py + a1 * (hl + fl) * uy + a2 * (hg + 0.35 * kb) * vy) / kb) for a1 in (-1, 1) for a2 in (-1, 1)]
            taken.append((min(c_[0] for c_ in cn_), min(c_[1] for c_ in cn_), max(c_[0] for c_ in cn_),
                          max(c_[1] for c_ in cn_)))          # the symbol's own box (its turned rectangle's)
            ticks.append((k, px, py))
    cdots = [(V.p(cx_, cy_)[0] / kb, V.p(cx_, cy_)[1] / kb) for k_, cx_, cy_ in cpts]
    rb = P02_B_R
    for k_, px, py in ticks:                              # the bridge numbers: a ring marker beside the symbol
        ob = taken + [(qx - 0.9, qy - 0.9, qx + 0.9, qy + 0.9) for qx, qy in cdots]
        q = _p02_spot(px / kb, py / kb, rb + 0.2, ob, bnd, [rb + d_ for d_ in (2.1, 2.7, 3.4, 4.2, 5.2, 6.4)], pad)
        if q is None:
            q = (px / kb, py / kb + rb + 2.1)
            LOG.append(u"FLAG p02 plan 01: bridge {} number finds no free spot beside its symbol".format(knum[k_]))
        with B.kind("labels", u"bridge %d" % knum[k_]):
            bb_, r_ = _sb_marker(B, q[0] * kb, q[1] * kb, str(knum[k_]), mk_colour("bridge", k_), kb, L, order=64,
                                 style="ring", r_min=rb)
        taken.append(tuple(v_ / kb for v_ in bb_))
        ovl.append(bb_)
    rc = P02_C_R
    for j_, (k, cx, cy) in enumerate(cpts):               # the conflicts: on the point, else right beside it
        px, py = cdots[j_]
        ob = taken + [(qx - 0.9, qy - 0.9, qx + 0.9, qy + 0.9) for i_, (qx, qy) in enumerate(cdots) if i_ != j_]
        q = _p02_spot(px, py, rc + 0.2, ob, bnd, [0.0] + [rc + d_ for d_ in (0.0, 0.8, 1.6, 2.6, 3.8, 5.2, 6.8,
                                                                             8.4, 10.0)], pad)
        if q is None:
            q = (px, py)
            LOG.append(u"plan 01: conflict {} set on its point (no free spot near it; the booklet check moves the "
                       u"texts round it)".format(k))     # v62 (L2): a layout note, not a warning
        col_ = mk_colour("conflict", k)
        with B.kind("annotations", u"conflict %s" % k):   # v61 (G6-4): no dot, no leader line
            bb_, r_ = _sb_marker(B, q[0] * kb, q[1] * kb, k, col_, kb, L, order=64, r_min=rc)
        taken.append(tuple(v_ / kb for v_ in bb_))
        ovl.append(bb_)
    # v59 closing (G-R4-1): the map: its own names and markers (from i_map0) may sit on it, no other text
    sb_keep(B, (V.X0, mb, V.X0 + mw, ymap), u"p02 plan 01", "map", i_map0)
    # legend (v38: drawn samples with short names; explanations as [n] in the Sources key)
    r_home = bcite("Urban fabric: each building's type from its survey layer, names and heritage tags, surveyed floors, "
                   "footprint size and regularity, shared walls and the grain of the 40 m around it; shares of the "
                   "built footprint.")
    r_crown = bcite("Crowns: modelled heights and leaf types (Meta/WRI 1 m canopy height map, Tolan et al. 2024; CLC+ "
                    "2021 and Sentinel-2).")
    r_edge = bcite("Stream edges: what meets the water along each bank.")
    # v61 (round 6, G6-6): grouped by the hue table's categories (heritage apart from the grey fabric), the rows of a
    # group in the table's order and rank (_p02_leg_sort, common/hues.py legend_group), every colour from the table
    # (_p02_hue: the same call that drew it), rows sharing a colour keyed as one (_p02_merge_rows)
    ftot = sum(S.fabric_area.values()) or 1.0
    her_, fab_ = [], []
    for fab in FABRIC_ORDER:                              # v40: the fabric map's types; under 0.5 % left out
        v_ = 100.0 * S.fabric_area.get(fab, 0.0) / ftot
        if round(v_) >= 1 or (fab in ("monument", "sacred") and S.fabric_area.get(fab, 0.0) > 0):
            (her_ if fab in ("monument", "sacred") else fab_).append(
                ("box", _p02_fab_light(_p02_hue("fab_" + fab, FABRIC_PLAN[fab])), u"{} · {}".format(
                    FABRIC_SHORT[fab], "{:.0f}%".format(v_) if round(v_) >= 1 else "< 1%"), "fab_" + fab))
    if _P02.get("her1") and "hue" in globals():          # v61 (H3): a building the table ranks r1 (WH listing)
        her_.append(("box", C(hue("HER", 1)), u"World Heritage listing: " + u", ".join(          # noqa: F821
            sorted(n_ for n_ in _P02["her1"] if n_)), ("HER", 1)))
    leg = []
    if her_:
        leg += [("hdr", None, "HERITAGE " + r_home)] + _p02_leg_sort(her_)
    leg += [("hdr", None, "BUILDINGS · URBAN FABRIC" + (u"" if her_ else u" " + r_home))]
    leg += _p02_leg_sort(fab_)
    leg += [("dense", dc, "Densest grain · floor-area ratio {:.2f}+ {}".format(
                S.int_breaks[2], bcite(u"Densest grain: floor-area ratio on 10 m cells, areas of 2,000 m²+."))
             if getattr(S, "int_breaks", None) else "Densest grain")]      # v49.1 (Prompt 8): m² (was m2)
    gg = [("box", _p02_hue("g_" + k_, GREEN_SUB[k_]), lab, "g_" + k_)
          for k_, lab in (("wood", "Woods"), ("park", "Parks"), ("grass", "Grass & lawns"))]
    gg += [("box", _p02_hue("agri", CAT["agri"][1]), "Fields & orchards (survey, OSM)", "agri"),
           ("box", _p02_hue("vacant", CAT["vacant"][1]), "Vacant ground", "vacant"),
           ("box", _p02_hue("transport", mix(CAT["transport"][1], PAPER, 0.3)), "Parking & yards", "transport"),
           ("box", _p02_hue("water", CAT["water"][1]), "The stream", "water")]
    for k_, lab, col in LC_CLASSES:
        if getattr(S, "lc", {}).get(k_):
            gg.append(("box", _p02_hue("lc_" + k_, col), lab, "lc_" + k_))
    for lf in (0, 1, 2):                                  # v61 (G6-10): each leaf type's crowns, their species named
        if sp_leaf.get(lf):
            nm_ = [_p02_sp_name(sp_) for sp_ in sorted(k_ for k_ in sp_leaf[lf] if k_)]
            if not nm_:
                sp_t = u", species unspecified"
            else:
                sp_t = u": " + u", ".join(nm_) + (u"; the rest unspecified" if None in sp_leaf[lf] else u"")
            gg.append(("dot", _p02_hue("crown_%d" % lf, mix(LEAF_COL[lf], PAPER, 0.25)), u"Crown · {}{} {}".format(
                LEAF_NAME[lf].split(u" (")[0], sp_t, r_crown), "crown_%d" % lf))
    nm_ = [_p02_sp_name(sp_) for sp_ in sorted(k_ for k_ in (_P02.get("sym_sp") or {}) if k_)]
    gg += [("dot", _p02_hue("tree_sym", TREE_COLS["pine"]), u"Tree symbols of the survey" + (
        u": " + u", ".join(nm_) + u"; the rest unspecified" if nm_ else u""), "tree_sym"),
           ("dash", path_c, "Footpaths", "path")]
    leg += [("hdr", None, "GROUND AND GREEN")] + _p02_leg_sort(gg)
    leg += [("hdr", None, "THE STREAM EDGE " + r_edge)]
    leg += _p02_leg_sort([("thin", _p02_hue("edge_" + k_, EDGE[k_][1]), short(EDGE[k_][0]), "edge_" + k_)
                          for k_ in EDGE_ORDER if S.edge_len.get(k_, 0) > 0])
    leg += [("hdr", None, "STUDY AREA AND FRAME")]        # v58 (round 3, G1): was "MARKS" (its marks: the lists)
    leg.append(R28_STUDY_LEG)                             # v50 (G8): the study area, one name on every map
    if _p02_inside(S) is not None:                        # v59 (round 4, P02.2, G-R4-4): the base houses' tone
        leg.append(("box", _p02_hue("bld_out", P02_BASE_BLD), u"Buildings outside the study area"))
    if RF is not None:
        leg.append(("thin", INK, R28_FRAME_NAME + " (site_alan) " + r_map))   # v50 (G8): was "Analysis range"
    # v45: the booklet page's legend leaves out what the site readings key: the ground and green colours (the land-use
    # ring's key). v58 (round 3, P02.1, G1): the key sits directly UNDER plan 01, inside its crop drw_plan01 (was the
    # side column's crop drw_plan01_key), and it is also the board sheet's legend of the plan (shown once)
    ring_c = set(c_ for l_, c_, a_ in landuse_slices(getattr(S, "site", S))[0])
    leg_bk, grp = [], ""
    for kind, col, lab in leg:
        if kind == "hdr":
            grp = lab
            leg_bk.append((kind, col, lab))
        elif not (grp == "GROUND AND GREEN" and kind == "box" and col in ring_c):
            leg_bk.append(("line" if kind == "dash" else kind, col, lab))
    leg_bk = _p02_merge_rows(leg_bk)                      # v61 (G6-6): one row per shade of a group
    leg_bk = [e_ for j_, e_ in enumerate(leg_bk)          # v58: a group header with no row under it left out
              if e_[0] != "hdr" or (j_ + 1 < len(leg_bk) and leg_bk[j_ + 1][0] != "hdr")]
    _p02_legend_log()
    _P02["leg"] = leg_bk
    _P02["cs"] = [(k_, t_) for k_, cx_, cy_, t_ in sorted(cs) if F.inside(cx_, cy_)]
    # v45: scale bar and north arrow under the map, never on it; numbers 7 pt under the bar. v58 (round 3, P02.1, G2):
    # both in the map's first grid column; the bridge list beside them from the second grid column; the key under both
    gstep = (GRID_COL + GRID_GUT) * kb
    sbl = nice_floor(F2.w / 8.0)
    # v59.1: the bar 1 mm in from the crop's left edge (as on p06 and p20): its centred "0" hung half outside the crop
    with B.kind("annotations", "scale bar"):
        mb_crop = min(draw_scalebar_bk(B, V.X0 + 1.0 * kb, mb - 3.0 * kb, s, sbl, kb, L), mb - 9.5 * kb)
    _p02_north(B, F2, V.X0 + 1.0 * kb + sbl * s + 5.5 * kb, mb - 5.0 * kb, kb, L)   # v61 (G6-4): an_north
    with B.kind("legend", "bridges"):
        mb_crop = min(mb_crop, _p02_bridge_list(B, F, knum, V.X0 + gstep, mb - 1.5 * kb, V.X0 + mw, kb, L, ovl))
    i0_key = sb_mark(B)                                   # v59 closing (G-R4-1): the key's own texts from here
    with B.kind("legend"):
        low = _p02_key_under(B, leg_bk, _P02["cs"], V.X0, mb_crop - 2.0 * kb, mw, gstep, kb, L, ovl)
    sb_keep(B, (V.X0, low, V.X0 + mw, mb_crop - 2.0 * kb), u"p02 plan 01 key", "legend", i0_key)
    top_c = ymap + 0.3 * U
    crop_panel("plan01", V.X0, low - 0.5 * kb, V.X0 + mw, top_c, u"Plan 01 · what is there today",
               crop_scale(s), [])                         # v40; v58: the map, its lists and its key in one crop
    # v42: survey x, y of the plan's frame corners and where they sit on the sheet, so a later script (the farms map,
    # bergama_agriculture_alternatives) can place its own layer on this very plan in the booklet crop
    CROP_PANELS[-1]["geo"] = [(px_, py_) + tuple(V.p(px_, py_)) for px_, py_ in F2.P[:4]]
    _p02_ovl_add("plan01", (V.X0, low - 0.5 * kb, V.X0 + mw, top_c), kb, ovl)
    h_crop = (top_c - low + 0.5 * kb) / kb
    LOG.append(u"p.02 plan 01 (drw_plan01): map {:.0f} mm wide at 1:{:,.0f}, crop with its lists and key {:.0f} mm "
               u"tall (the page holds {:.0f} mm at that scale); side column {:.0f} mm.".format(
                   map_mm, den_bk, h_crop, P02_CROP_MAX, _p02_side_w()))
    if h_crop > P02_CROP_MAX:
        LOG.append(u"WARNING: p.02 plan 01's crop is {:.0f} mm tall, over the {:.0f} mm the page holds: the booklet "
                   u"prints the map at the next round scale.".format(h_crop, P02_CROP_MAX))
    tot = sum(S.fabric_area.values()) or 1.0
    # v38: the caption's two figures as tiles (were sentences); its notes are the key entries cited above
    with B.kind("labels", "tiles"):                       # v61 (G6-9)
        return vis_tiles(B, x, low - 1.3 * U, min(mw, 44.0 * U), [
            ("build", "OLD TOWN · % OF BUILT FOOTPRINT",
             "{:.0f}%".format(100.0 * S.fabric_area.get("traditional", 0.0) / tot), r_home),
            ("green", "CROWNS IN THE FRAME", "{}".format(len(crowns)), r_crown)], U, L, h=1.3, ink=INK, grey=INK2,
            fill=mix(PAPER, (255, 255, 255), 0.5), rule=FAINT)


# ------------------------------------------------------------ v51 (revision 29 Oct 2026, WO-T3a-2): p.02 and p.03
_P02 = {}                 # set by draw_what_is_there: text, leg, cs [(name, words)]; v58: side_w (the side column, mm),
#                           ovl (each p.02 crop's text boxes for _p02_flag), wlog
P02_C_R = 2.3             # booklet mm: radius of a conflict disc C1-C6 on plan 01 (its name inside, white 7 pt bold)
P02_ET_MIN = 32.0         # m: a bank stretch shorter than this is drawn as its longer neighbour (legible at print)
P02_ET_LAND = 30.0        # m of land drawn beyond the bank line on each bank of the edge strip
P02_ET_ZONE = 8.0         # m: the edge zone along the water where each edge type gets its own drawing
P02_ET_ROWS = 3           # v58 (round 3, P02.2, G2): the straightened stream in three rows (was two): half again the
#                           length along the stream, so neighbouring blocks part; the side column's freed height holds it
P02_ET_HB = 8.0           # v58 (round 3, P02.2): booklet mm of each bank's land band on the edge strip (was 7.0)
P02_ET_TOL = 1.0          # v58 (round 3, P02.2): m: blocks this close (along or across the strip) count as touching
P02_ET_STEP = 1.0         # v58 (round 3, P02.2): m: the chainage step of a merged block's outline
P02_CROP_MAX = 238.0      # v58 (round 3, G2): booklet mm: the tallest plan 01 crop the page holds at its round scale
#                           (booklet AREA 243 mm less the 5 mm caption band); taller drops the map to the next scale
P02_LEAF_SP = {0: "plane", 1: "olive", 2: "stone_pine"}   # v61 (G6-10): the GENERIC crown glyph (plants.py pla_plan) by
#                           the canopy map's leaf type, only for a tree with no supported species (sb_tree_species None:
#                           = common/trees.py's deciduous / evergreen / pine glyphs); it never names a species
# v61 (round 6, G6-6, PLAN §2.6; hues_and_proposals.md H1 p02 + H2 notes 1-3): every p.02 colour that a legend keys,
# as (category code, rank) of the subtle hue table (common/hues.py hue(); the strong set is never used on p.02).
# Existing context in CTX greys (buildings by fabric one rank lighter than the table's r1 = the v59 lighter fabric,
# Aras U61); uses on the ring: commerce MOV r1, mixed MOV r2, residential MOV r3, civic PUB r2, worship PUB r1,
# workshops CTX r2; heritage fabric HER (monuments r2: "Sit" registration of the archaeological lands, sacred r3: no
# sourced status, H3); existing green (woods, parks, grass) one GRN r4 tint with its trees drawn over it (H2 note
# 3's alternative: CTX holds five steps and p.02 keys nine existing ground classes; flip "g_*" / "lc_grass" /
# "lc_shrub" / "lc_trees" to ("CTX", 4) for the greys); crowns GRN r1-r3 by leaf type; stream WAT.
# Rows of one legend group (and ring slices) that share a colour are keyed as ONE row (_p02_merge_rows).
P02_HUE = {"fab_monument": ("HER", 2), "fab_sacred": ("HER", 3), "fab_traditional": ("CTX", 2),
           "fab_block": ("CTX", 3), "fab_regular": ("CTX", 4), "fab_selfbuilt": ("CTX", 5), "fab_large": ("CTX", 5),
           "fab_construction": ("CTX", 5), "bld_out": ("CTX", 5), "bld_out_edge": ("CTX", 4), "dense": ("CTX", 1),
           "g_wood": ("GRN", 4), "g_park": ("GRN", 4), "g_grass": ("GRN", 4), "lc_grass": ("GRN", 4),
           "lc_shrub": ("GRN", 4), "lc_trees": ("GRN", 4), "lc_farmland": ("AGR", 3), "lc_orchard": ("AGR", 2),
           "agri": ("AGR", 3), "vacant": ("CTX", 3), "transport": ("CTX", 3), "streets": ("CTX", 4),
           "rest": ("CTX", 5), "water": ("WAT", 3), "water_line": ("WAT", 2), "water_cov": ("WAT", 4),
           "residential": ("MOV", 3), "mixed": ("MOV", 2), "commercial": ("MOV", 1), "institutional": ("PUB", 2),
           "religious": ("PUB", 1), "industrial": ("CTX", 2), "crown_0": ("GRN", 2), "crown_1": ("GRN", 3),
           "crown_2": ("GRN", 1), "tree_sym": ("GRN", 1), "path": ("MOV", 3),
           "edge_building": ("CTX", 1), "edge_street": ("CTX", 2), "edge_pedestrian": ("MOV", 2),
           "edge_green": ("GRN", 1), "edge_parking": ("CTX", 3), "edge_open": ("CTX", 4),
           "wall_1": ("CTX", 2), "wall_2": ("CTX", 3), "et_ground": ("CTX", 5), "et_roof": ("CTX", 3),
           "et_road": ("CTX", 2), "et_park": ("CTX", 3), "et_walk": ("MOV", 4), "et_green": ("GRN", 4),
           "et_open": ("CTX", 4),
           "conflict": ("ANN", 0)}
P02_CUT_IN = 7.0          # v61 (G6-4): booklet mm, the least room between plan 01's cut-mark frame and its crop's edge
#                           (an_cut: 4 mm stub + 2 mm triangle + the name outside the frame)
P02_SP = {}               # v61 (G6-10): (x, y) of a p.02 crown -> its species glyph key or None (once per run)


def _p02_hue(key, old=None):
    """v61 (G6-6): the board colour (rgb) of a p.02 legend key from the hue table (P02_HUE, common/hues.py hue());
    the old colour when the table or the module is missing (the script then still draws)"""
    cr = P02_HUE.get(key)
    if cr is None:
        return old
    if cr[0] == "ANN":                                    # annotations: the table's text ink (not a category)
        return C("2C2219")
    if "hue" not in globals():
        return old
    try:
        return C(hue(cr[0], cr[1]))                                                          # noqa: F821
    except Exception:
        return old


def _p02_merge_rows(rows, lab_i=2, col_i=1, area_i=None):
    """v61 (G6-6): rows that share a colour inside one legend group (between "hdr" rows) become ONE row, its labels
    joined in order (and, area_i given, their areas summed): the table gives a category's items shades, and two items
    of one shade must not read as two keys"""
    out, seen = [], {}
    legend = area_i is None                               # legend rows (kind, colour, label); else ring slices
    for r_ in rows:
        if legend and r_[0] == "hdr":
            out.append(r_)
            seen = {}
            continue
        ck = r_[col_i]
        if ck is not None and ck in seen and (not legend or r_[0] == out[seen[ck]][0]):
            j_ = seen[ck]
            q = list(out[j_])
            q[lab_i] = u"%s, %s" % (q[lab_i], r_[lab_i])
            if area_i is not None:
                q[area_i] = q[area_i] + r_[area_i]
            out[j_] = tuple(q)
            continue
        if ck is not None:
            seen[ck] = len(out)
        out.append(r_)
    return out


def _p02_leg_sort(rows):
    """v61 (G6-6): legend rows (kind, colour, label, P02_HUE key or (code, rank)) in the hue table's order, category
    then rank (common/hues.py legend_group; the given order without it), as (kind, colour, label)"""
    ents = []
    for j_, r_ in enumerate(rows):
        cr = r_[3] if isinstance(r_[3], tuple) else P02_HUE.get(r_[3], ("CTX", 9))
        ents.append(dict(cat=cr[0], rank=cr[1], row=r_[:3], j=j_))
    if "legend_group" in globals():
        try:
            got = list(legend_group(ents))                                                   # noqa: F821
            if len(got) == len(ents) and all("row" in e_ for e_ in got):
                ents = got
        except Exception:
            pass
    return [e_["row"] for e_ in ents]


def _p02_legend_log():
    """v61 (G6-6): the `legend p02 hues=table` line (common/hues.py hue_log), once per legend"""
    try:
        LOG.append(hue_log("p02"))                                                           # noqa: F821
    except Exception:
        LOG.append(u"legend p02 hues=table (FLAG: common/hues.py hue_log not in this build)")


P02_GROUND = mix(PAPER, (255, 255, 255), 0.45)            # open ground in the edge strip
P02_ROOF = mix(INK2, PAPER, 0.62)                         # roofs in the edge strip (one tone: a plan, not a use map)
P02_ROOF_L = mix(INK2, PAPER, 0.1)                        # their ridges, hips and fall lines (M11)
P02_ROAD = mix(INK2, PAPER, 0.5)                          # carriageway
P02_MAP_W = grid_w(7)     # booklet mm: plan 01 on the M1 grid (7 columns) ...
P02_SIDE_W = grid_w(5)    # ... and p.02's side column beside it (5 columns): the key, the edge strip, the readings
#                           v58 (round 3, G2): the fallback only; _p02_side_w() gives the side column the grid columns
#                           the map leaves (6 when plan 01 prints <= 194 mm wide at its round scale)
P02_GAP = GRID_GUT        # booklet mm between the side panels' halves / columns (the grid's gutter)
P02_SIDE_H = 243.0        # v59 (round 4, P02.3): booklet mm of p.02's side column (the booklet AREA, y 30-273) ...
P02_CAP_H = 5.0           # ... the booklet's caption band under each side panel (bergama_booklet CAP_H) ...
P02_SIDE_SAFE = 3.0       # ... and a margin left free at its foot
P02_ET_GAP_MAX = 12.0     # v59 (round 4, P02.3): booklet mm, the most added between two rows of the edge from above
P02_ET_KIND = {"pedestrian": "paths", "street": "roads", "parking": "roads", "green": "plants", "open": "ground",
               "building": "buildings"}   # v61 (G6-9): the kind of each edge type's stretch on the edge strip
P02_RD_GAP = 2.6          # v61 (G6-8, SON page2 "LAND USE AND GROUND COVER / si" x "[2][3]"): booklet mm between a
#                           site-readings heading and its sub-line (was 1.6: the raised source marks touched the heading)
P02_ET_REACH = {3: (u"UPSTREAM", u"MIDDLE", u"DOWNSTREAM"), 2: (u"UPSTREAM", u"DOWNSTREAM")}   # v59: row headings
P03_FIG_EDGE = 30.0       # m: one figure watching the water along each walkable bank stretch, every this many m
P03_FIG_PATH = 80.0       # m: one figure walking a footpath every this many m
P03_FIG_MAX = 240         # at most this many figures on the axonometric
FIG_INK = INK
FIG_FILL = mix(PAPER, (255, 255, 255), 0.45)


def _p02_hit(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


P02_B_R = 1.6             # v59 (round 4, P02.1): booklet mm, the least radius of a bridge-number ring marker on plan 01
P02_BR_HALF = 1.6         # v59 (round 4, P02.1): booklet mm, half the length of a bridge symbol across the stream
P02_BR_GAP = 0.45         # v59 (round 4, P02.1): booklet mm, half the gap between its two deck lines
P02_MK_PAD = 1.2          # v59 (round 4, P02.1, G-R4-1): mm clear round every marker. v61 (G6-8, SON page2: bridge
#                           1-6 / clash C1-C6 cluster): twice the page check's 0.6 mm, so no two markers' glyphs touch
P02_SPOT_DIRS = (0, 4, 8, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15)   # v59: tried directions (x 22.5 deg from up,
#                                                                          clockwise): the four sides first


def _sb_marker(B, x, y, s, colour, k, L, order=64, style="solid", size_pt=7.0, r_min=None):
    """v59 (round 4, G-R4-7): ONE marker on a board drawing through common/marker.py mk_marker (the glyph centred on
    its ink box, the circle sized to it, white or ink glyph by contrast): (x, y) its centre in board units, k = board
    units per booklet mm, colour hex (or rgb) = the colour of what it names, size_pt / r_min (booklet mm) as
    mk_marker. Draws the disc (order) and the glyph (order + 1, its own text group). Returns (box, r) in board
    units (box = the outer box, rim included)."""
    hx = crop_hex(colour)
    shapes, box, r = mk_marker(x / k, y / k, s, hx, size_pt=size_pt, r_min=r_min, style=style)
    for sh in shapes:
        if sh[0] == "poly":
            ring = [(p_[0] * k, p_[1] * k) for p_ in sh[1]]
            if sh[2]:
                B.fill([ring], C(sh[2]), L, order)
            if sh[3] and sh[4]:
                B.line(ring + [ring[0]], C(sh[3]), L, order, bk_lw(sh[4], k))
        elif sh[0] == "text":
            B.text(sh[1], sh[2] * k, sh[3] * k, sh[4] * _PDF_CAP["sans"] * k, C(sh[5]), L, order=order + 1,
                   font=FONT_TITLE, bold=True, align="L")
    return tuple(v_ * k for v_ in box), r * k


def _sb_north(B, F, x, y, size_mm, k, L, order=60, ang=None):
    """v59 (round 4, G-R4-9): THE north arrow on a board map (common/keymap.py north_items: the arrow and "N", no
    plate or white half) for a map drawn on F's axes (or ang = north's angle on the page, radians from +x), centred
    on (x, y) board units, size_mm tall on the booklet page (k = board units per booklet mm). Returns its box
    (board units)."""
    a = math.atan2(math.cos(F.ang), math.sin(F.ang)) if ang is None else ang      # north on F's axes
    its = north_items(0.0, 0.0, a - 0.5 * math.pi, size_mm)
    tm = max(2.12, 0.42 * size_mm)
    h_all = size_mm + 1.5 * tm                            # the shaft foot to the top of the "N"
    ca, sa = math.cos(a - 0.5 * math.pi), math.sin(a - 0.5 * math.pi)
    fx, fy = x / k + 0.5 * h_all * sa, y / k - 0.5 * h_all * ca       # the foot, so the whole sign is centred on (x, y)
    pts = []
    for it in its:
        if it[0] == "line":
            P = [((fx + p_[0]) * k, (fy + p_[1]) * k) for p_ in it[1]]
            B.line(P, C(it[2]), L, order, bk_lw(it[3], k))
            pts += P
        elif it[0] == "fill":
            for R in it[1]:
                P = [((fx + p_[0]) * k, (fy + p_[1]) * k) for p_ in R]
                B.fill([P], C(it[2]), L, order)
                pts += P
        elif it[0] == "text":
            tx, ty = (fx + it[2][0]) * k, (fy + it[2][1]) * k
            B.text(it[1], tx, ty, it[3] * _PDF_CAP["sans"] * k, C(it[4]), L, order=order + 1, font=FONT_TITLE,
                   bold=bool(it[5]), align="MC")
            hw = 0.5 * it[3] * k
            pts += [(tx - hw, ty - hw), (tx + hw, ty + hw)]
    if not pts:
        return (x, y, x, y)
    return (min(p_[0] for p_ in pts), min(p_[1] for p_ in pts), max(p_[0] for p_ in pts), max(p_[1] for p_ in pts))


def _p02_north(B, F, x, y, k, L, size_mm=5.0):
    """v61 (round 6, G6-4): plan 01's north: common/annot.py an_north (plain solid arrow + N, no box) centred on (x, y)
    board units, outside the map (under it, beside the scale bar); north_deg = north's turn on the page from up,
    counter-clockwise, degrees (F's axes, as _sb_north). _sb_north (kept: p.06 and p.07 still draw it) without the
    module."""
    a = math.atan2(math.cos(F.ang), math.sin(F.ang))      # north on F's axes, radians from +x
    with B.kind("annotations", "north"):
        if "an_north" in globals():
            try:
                an_north(SbX(B, L, 60, k).cb(), (x / k, y / k), math.degrees(a - 0.5 * math.pi),   # noqa: F821
                         size_mm=size_mm)
                return
            except Exception as ex_:
                wn_warn("p02", "north", u"an_north failed ({}): the board's north arrow drawn".format(ex_))
        _sb_north(B, F, x, y, size_mm, k, L)


def _p02_text_boxes(B, i0, k):
    """v59 (round 4, P02.1, G-R4-1): the boxes (booklet mm) of the board texts drawn from item i0 on, measured with
    the real Arial widths (tw); a turned text as boxes of 4-letter chunks along its baseline (its strip, not its
    bounding box), as the page check measures it"""
    out = []
    for it in B.items[i0:]:
        if it[0] != "text" or not u"%s" % it[1]:
            continue
        txt, (x, y), h, bold, al, ang = u"%s" % it[1], it[2], it[3], bool(it[8]), it[9] or "L", it[10] or 0.0
        wd = tw(txt, h, "sans", bold)
        x0 = {"C": -0.5, "MC": -0.5, "R": -1.0}.get(al, 0.0) * wd
        yb = -0.5 * h if al == "MC" else 0.0              # "MC": (x, y) is the middle of the capitals
        ca, sa = math.cos(ang), math.sin(ang)
        step = wd if abs(ang) < 1e-3 else max(1e-9, wd / max(1, (len(txt) + 3) // 4))
        u_ = x0
        while u_ < x0 + wd - 1e-9:
            u1 = min(x0 + wd, u_ + step)
            cn = [(x + a_ * ca - b_ * sa, y + a_ * sa + b_ * ca) for a_ in (u_, u1)
                  for b_ in (yb - 0.32 * h, yb + 1.3 * h)]
            out.append((min(c_[0] for c_ in cn) / k, min(c_[1] for c_ in cn) / k, max(c_[0] for c_ in cn) / k,
                        max(c_[1] for c_ in cn) / k))
            u_ = u1
    return out


def _p02_spot(px, py, r, taken, bnd, rings, pad=0.6, lead=False):
    """v59 (round 4, P02.1, G-R4-1): the first free centre (booklet mm) for a marker of half-size r near (px, py): the
    distances in rings in turn (0 = on the point), P02_SPOT_DIRS at each, its box clear of every box in taken by
    pad and inside bnd; lead=True: the leader from (px, py) to the marker's edge must miss taken too (boxes holding
    the point itself excepted). None when nothing is free."""
    for d in rings:
        for j in (P02_SPOT_DIRS if d > 0 else (0,)):
            an = math.radians(90.0 - 22.5 * j)
            cx, cy = px + d * math.cos(an), py + d * math.sin(an)
            b_ = (cx - r - pad, cy - r - pad, cx + r + pad, cy + r + pad)
            if cx - r < bnd[0] or cy - r < bnd[1] or cx + r > bnd[2] or cy + r > bnd[3]:
                continue
            if any(_p02_hit(b_, t_) for t_ in taken):
                continue
            if lead and d > r:
                own = [t_ for t_ in taken if not (t_[0] <= px <= t_[2] and t_[1] <= py <= t_[3])]
                n_ = max(2, int((d - r) / 0.4))
                if any(t_[0] <= px + (cx - px) * f_ <= t_[2] and t_[1] <= py + (cy - py) * f_ <= t_[3]
                       for i_ in range(n_ + 1) for f_ in (i_ / float(n_) * (d - r) / d,) for t_ in own):
                    continue
            return (cx, cy)
    return None


def _p02_side_w():
    """v58 (round 3, G2): booklet mm of p.02's side column: the whole grid columns plan 01 leaves (set by
    draw_what_is_there from the map's printed width), else P02_SIDE_W"""
    return _P02.get("side_w") or P02_SIDE_W


def _p02_knum():
    """v58 (round 3, G16): {bridge code: its number on p.02}, 1.. in stream order (bridges_in_order, upstream first);
    the codes stay internal, the page prints the number and bridge_name"""
    have = set(b_[0] for b_ in BRIDGES_K)
    return dict((k_, j_ + 1) for j_, k_ in enumerate([c_ for c_ in bridges_in_order() if c_ in have]))


def _p02_tb(txt, x, y, h, wmax=None):
    """v58 (round 3, G3): the box (board units, y up) of one line of text from baseline y at capital height h, its
    width as site28_text measures it (capped at wmax: site28_fit shrinks to it)"""
    w_ = site28_line_w(site28_one(txt, h), h)
    if wmax is not None and wmax > 0:
        w_ = min(w_, wmax)
    return (x, y - 0.25 * h, x + w_, y + h)


def _p02_ovl_add(name, crop, k, boxes):
    """v58 (round 3, G3): one p.02 crop's text boxes (board units) for the page's overlap test (_p02_flag): crop =
    its rectangle (x0, y0, x1, y1, board units), k = board units per booklet mm"""
    _P02.setdefault("ovl", []).append((name, crop, k, [b_ for b_ in boxes if b_]))


def _p02_flag():
    """v58 (round 3, G3 done-when): FLAG overlap p02: every text box of p.02's crops placed where the booklet puts the
    crops (plan 01 at the left of the drawing area, the side panels stacked at its right margin, each followed by
    the booklet's 5 mm caption band), page mm y down; labels vs labels and vs the page's drawing area"""
    ovl = _P02.get("ovl") or []
    if not ovl:
        return
    x_side = GRID_PAGE[0] - GRID_MR - _p02_side_w()
    y_side = GRID_AREA[1]
    out = []
    for name, (cx0, cy0, cx1, cy1), k, boxes in ovl:
        if name == "plan01":
            X, Y = GRID_AREA[0], GRID_AREA[1]
        else:
            X, Y = x_side, y_side
            y_side += (cy1 - cy0) / k + 5.0               # the booklet's CAP_H under each side panel
        for b_ in boxes:
            out.append((X + (b_[0] - cx0) / k, Y + (cy1 - b_[3]) / k, X + (b_[2] - cx0) / k, Y + (cy1 - b_[1]) / k))
    lp_overlap_flag("p02", out, (), bounds=(GRID_AREA[0], GRID_AREA[1], GRID_AREA[2], GRID_AREA[3]))


def _p02_col(c):
    """a colour of the house shapes (hex without '#', or rgb) as the board's rgb tuple"""
    if c is None or isinstance(c, tuple):
        return c
    if isinstance(c, list):
        return tuple(c[:3])
    return C(str(c))


# v60 (round 5, P02.1, Aras U02 "lets show where we took that drawings from on the map"): every section cut of the
# booklet that the level table holds, its id at one end and the booklet pages at the other. v61 (round 6, G6-4, G6-2):
# no red line across the plan any more: each cut is a common/annot.py an_cut mark (filled triangle + name at each end
# just outside the map's frame, short dashed stub); the pages are the final 22-page numbers (PLAN §2.1): S1-S4 on
# p.4 and S5-S8 on p.5 (sections), W1-W4 on p.12 (proposals in section), S4 also on p.13 (four seasons) and p.14 (the
# S4 cut), W1, F2, F4 and S4 on p.16 (which plant goes where: plans A, B and their key map). Street cuts R1-R4 (p.8),
# A-A' (p.11) and D1/D2 (p.21) are not in the level table (their owning drawings compute them): not marked, logged.
P02_MARK_PAGES = [("S1", u"4"), ("S2", u"4"), ("S3", u"4"), ("S4", u"4, 13, 14, 16"), ("S5", u"5"), ("S6", u"5"),
                  ("S7", u"5"), ("S8", u"5"), ("W1", u"12, 16"), ("W2", u"12"), ("W3", u"12"), ("W4", u"12"),
                  ("F2", u"16"), ("F4", u"16")]


def _p02_drawing_marks(B, V, kb, L, frame, order=66):
    """v60 (P02.1); v61 (round 6, G6-4): the cuts of P02_MARK_PAGES on plan 01 as an_cut marks (common/annot.py: X =
    SbX(...).cb() in booklet mm, T = survey m -> booklet mm through V, frame = the map's rectangle, board units ->
    mm): the cut's name at its unprimed end, "<name>' p. <pages>" at the other; each mark in the kind "cuts". Logs
    `annot p02 cuts=n levels=0` (an_log) and the cuts left out."""
    if "an_cut" not in globals() or "level_ends" not in globals():
        wn_warn("p02", "marks", u"cut marks not drawn: common/annot.py (an_cut) or the level table is missing")
        return 0
    X = SbX(B, L, order, kb, kind="cuts").cb()
    T = lambda p_: (V.p(p_[0], p_[1])[0] / kb, V.p(p_[0], p_[1])[1] / kb)
    fr = tuple(v_ / kb for v_ in frame)
    done, miss = [], []
    for cid, pg_ in P02_MARK_PAGES:
        try:
            a_, b_ = level_ends(cid if cid not in ("S5", "S6") else cid + "-1")
        except Exception:
            miss.append(cid)
            continue
        try:
            an_cut(X, a_, b_, cid, fr, T=T, look=1, names=(cid, u"%s' p. %s" % (cid, pg_)), page="p02")  # noqa: F821
            done.append(cid)
        except Exception as ex_:
            wn_warn("p02", "marks", u"cut mark {} not drawn ({})".format(cid, ex_))
    try:
        LOG.append(an_log("p02"))                                                            # noqa: F821
    except Exception:
        LOG.append(u"annot p02 cuts=%d levels=0" % len(done))
    LOG.append(u"p02 cut marks (G6-4): {} cut(s) {}{}; not in the level table (not marked): p08 R1-R4, p11 A-A', "
               u"p21 D1/D2".format(len(done), u", ".join(done), u"; missing ends: " + u", ".join(miss) if miss else u""))
    return len(done)


def _p02_put(B, shapes, L, order, k):
    """house shapes ("poly", ring, fill, stroke, lw) / ("line", pts, colour, lw) in board units, line weights in
    booklet mm (k = board units per booklet mm), through the board's calls"""
    for sh in shapes:
        if sh[0] == "poly" and len(sh[1]) >= 3:
            fill, stroke = _p02_col(sh[2]), _p02_col(sh[3] if len(sh) > 3 else None)
            if fill is not None:
                B.fill([list(sh[1])], fill, L, order)
            if stroke is not None and len(sh) > 4 and sh[4]:
                B.line(list(sh[1]) + [sh[1][0]], stroke, L, order, bk_lw(sh[4], k))
        elif sh[0] == "line" and len(sh[1]) >= 2:
            B.line(list(sh[1]), _p02_col(sh[2]), L, order, bk_lw(sh[3] if len(sh) > 3 else 0.1, k))


def _p02_items(B, V, items, L, order, k, lw_f=1.0, fills=True, lines=True):
    """revision 30 Oct (M11): basemap-format items ("fill", rings, hex, alpha, nonzero) / ("line", pts, hex, width_mm,
    dash, alpha) in survey m, drawn on the board through V; line widths in booklet mm x lw_f (k = board units per
    booklet mm). A fill's rings go in one call (even-odd: courtyards stay open)."""
    for it in items:
        if it[0] == "fill" and fills:
            rings = [R for R in it[1] if len(R) >= 3]
            if rings:
                B.fill(V.Ps(rings), _p02_col(it[2]), L, order)
        elif it[0] == "line" and lines and len(it[1]) >= 2:
            B.line(V.P(it[1]), _p02_col(it[2]), L, order + 1, bk_lw(it[3] * lw_f, k))


def _p02_bld_plan(S, B, V, L, order, den, kb, bcol=None, lw_f=0.6, inside=None):
    """revision 30 Oct (G7, M11; Aras "just draw the outlines and hatch the inside"): plan 01's buildings through
    bld_plan_items: per colour (bcol, the urban fabric) the light fill and the roof reading (ridge and hips where a
    building is BLD_MIN_ROOF_MM wide at 1:den), then ONE outline per block (S.blocks, merged in build_site): no line
    between buildings that share a wall, no piece outlines. lw_f thins the module's pens for the 1:20,000 plan.
    v59 (round 4, P02.2, G-R4-4): inside = _p02_inside(S) (None: all inside): the buildings outside the study area
    are base map: no roof reading, and their blocks outlined in the base tone P02_BASE_EDGE, P02_BASE_LW mm."""
    groups = {}
    for u in S.bld:
        if not u.get("parts"):
            continue
        col = bcol(u) if bcol is not None else (mix(CAT[u["cat"]][1], PAPER, 0.35) if u["annex"] else CAT[u["cat"]][1])
        groups.setdefault((crop_hex(col), _p02_u_inside(inside, u)), []).append(u)
    roof_c = crop_hex(mix(INK, PAPER, 0.45))
    for (h_, in_), us in sorted(groups.items()):          # v61 (G6-9): heritage fabric in the kind "heritage"
        her_ = in_ and any(u_.get("fabric") in ("monument", "sacred") for u_ in us)
        with B.kind("heritage" if her_ else "buildings"):
            _p02_items(B, V, bld_plan_items(us, None, den, roof="ridge" if in_ else "none", fill=h_, her_fill=h_,
                                            roof_col=roof_c, outline=False), L, order, kb, lw_f)
    edge = crop_hex(FABRIC_EDGE)
    blocks = getattr(S, "blocks", None)
    with B.kind("buildings"):                             # v61 (G6-9): the block outlines, each its own element
        _p02_bld_outlines(S, B, V, L, order, den, kb, lw_f, inside, blocks, edge)


def _p02_bld_outlines(S, B, V, L, order, den, kb, lw_f, inside, blocks, edge):
    """v61 (split from _p02_bld_plan, unchanged): ONE outline per block, inside the study area in the fabric edge,
    outside it in the base tone (P02_HUE "bld_out_edge")"""
    if inside is None or blocks is None:
        _p02_items(B, V, bld_plan_items(S.bld, blocks, den, roof="none", edge=edge, her_edge=edge), L,
                   order + 2, kb, lw_f, fills=False)
        return
    b_in, b_out = [], []                                  # v59 (round 4, P02.2): each block by its outline's centre
    for bk in blocks:
        o = bk["outer"] if "outer" in bk else (bk.get("rings") or [[]])[0]
        if len(o) < 3:
            continue
        (b_in if inside(sum(p_[0] for p_ in o) / len(o), sum(p_[1] for p_ in o) / len(o)) else b_out).append(bk)
    if b_in:
        _p02_items(B, V, bld_plan_items(S.bld, b_in, den, roof="none", edge=edge, her_edge=edge), L,
                   order + 2, kb, lw_f, fills=False)
    if b_out:
        e_out = crop_hex(_p02_hue("bld_out_edge", P02_BASE_EDGE))
        _p02_items(B, V, bld_plan_items(S.bld, b_out, den, roof="none", edge=e_out, her_edge=e_out,
                                        lw=P02_BASE_LW / lw_f), L, order + 2, kb, lw_f, fills=False)


def _p02_fig(pose, x, y, k, facing=1, view="side", ang=0.0, mm_per_m=None, pick=None):
    """ONE helper for every human figure of p.02-03 (HELPER_BRIEF rule 3): house shapes, k = drawing units per metre.
    v52: the A1 pen figures of figures.py (adult 1.75 m since the revision of 30 Oct, D9). side: fig_side(pose) with
    its feet at (x, y); top: fig_top(pose) centred on (x, y) heading ang (radians, 0 = +x). mm_per_m = booklet mm per metre where k is not
    (keeps the pen at least 0.10 mm). Line weights in mm of the drawing it lands on."""
    if view == "top":
        return fig_top(pose, x, y, k, ang=ang, ink=FIG_INK, mm_per_m=mm_per_m)
    return fig_side(pose, x, y, k, facing, ink=FIG_INK, mm_per_m=mm_per_m, pick=pick)


def _p02_bridge_list(B, F, knum, x0, ytop, x1, kb, L, ovl=None):
    """v58 (round 3, G16, G3; was _p02_mark_list's "BRIDGES" half): under plan 01, x0..x1 from ytop down (board
    units; kb per booklet mm): "BRIDGES · UPSTREAM TO DOWNSTREAM", then each bridge in the frame with the map's tick,
    its number on the map and its one spelling (bridge_name), in stream order, three to a row in reading order (left
    to right, then down). Text boxes go to ovl. Returns the y below."""
    h7, h75 = bk_hk(7.0, kb), bk_hk(7.5, kb)
    rows = [(n_, k_) for k_, n_ in sorted(knum.items(), key=lambda t_: t_[1])
            if any(b_[0] == k_ and F.inside(b_[2], b_[3]) for b_ in BRIDGES_K)]
    if not rows:
        return ytop
    ovl = ovl if ovl is not None else []
    W = x1 - x0
    ncol = 3
    cw = (W - (ncol - 1) * P02_GAP * kb) / ncol
    hd = u"**BRIDGES** · upstream to downstream"
    site28_fit(B, hd, x0, ytop - h75, h75, W, INK, L)
    ovl.append(_p02_tb(hd, x0, ytop - h75, h75, W))
    low = ytop
    for j, (n_, k_) in enumerate(rows):
        cx0 = x0 + (j % ncol) * (cw + P02_GAP * kb)
        # v61 (G6-8, SON page2 "BRIDGES · upstream to downstre" x "1 / 2 / 3", "Tabak Köprüsü / Üç Kemer Köprü" x
        # "4 / 5 / 6"): the first row's ring marker (1.8 mm half-size with its rim) 1.0 mm under the heading's
        # descenders (was 0.3 mm over its baseline), the rows 4.8 mm apart (was 4.0: a name's descenders touched the
        # next row's rings)
        yb = ytop - 1.3 * h75 - 2.8 * kb - 0.5 * h7 - (j // ncol) * 4.8 * kb
        # v59 (round 4, P02.1, G-R4-7): the number in the map's ring marker (the bridges' ink), then the real name
        mb_, r_ = _sb_marker(B, cx0 + P02_B_R * kb + 0.15 * kb, yb + 0.5 * h7, str(n_), mk_colour("bridge", k_), kb, L,
                             order=64, style="ring", r_min=P02_B_R)
        tx_ = mb_[2] + 1.0 * kb
        txt = bridge_name(k_)
        site28_fit(B, txt, tx_, yb, h7, cx0 + cw - tx_, INK, L)
        ovl.append(_p02_tb(txt, tx_, yb, h7, cx0 + cw - tx_))
        low = min(low, yb - 1.2 * kb)
    return low


def _p02_key_under(B, leg, cl, x0, ytop, W, gstep, kb, L, ovl=None):
    """v58 (round 3, P02.1, G1, G2; was draw_plan01_key's panel in the side column + _p02_mark_list's conflicts): plan
    01's key directly under the map, from x0 (the map's left edge) and ytop down, W wide (board units; kb per booklet
    mm). Three columns on the booklet grid (each two grid columns, gstep = one grid column + gutter, board units; equal
    thirds when the map is narrower), filled top-down in the legend's order with its group headers, then "WHERE STREAM
    AND TOWN CLASH": each conflict as the map draws it (P02_C_R disc, white rim, its name inside) and its words. Rows
    4.0 mm (a conflict 2 radii + 0.8 mm), words 7.5 pt, the column height the least that holds every row in three
    columns. Text boxes go to ovl. Returns the y below."""
    import re as _re
    ovl = ovl if ovl is not None else []
    h75 = bk_hk(7.5, kb)
    rc, hcn = P02_C_R * kb, bk_hk(7.0, kb)
    rows = []                                             # (kind, row height mm, colour, label)
    for kd, c_, lb in leg:
        lb = _re.sub(r"\s*\[\d+\]", u"", lb).strip()
        rows.append((kd, 4.0, c_, lb))
    if cl:
        rows.append(("hdr", 4.0, None, u"WHERE STREAM AND TOWN CLASH"))
        rows += [("cdisc", 2.0 * P02_C_R + 0.8, nm_, t_) for nm_, t_ in cl]
    if not rows:
        return ytop
    ncol = 3
    if 2.0 * (2.0 * gstep) + 40.0 * kb <= W:            # the grid: columns 1-2, 3-4, 5-6 of the map's width
        cxs = [x0 + j_ * 2.0 * gstep for j_ in range(ncol)]
        cws = [min(grid_w(2) * kb, x0 + W - c_ - 0.5 * kb) for c_ in cxs]   # v59.1: a text fitted to the last
        # column ended exactly on the crop's right edge ("Ulucami Önü Köprüsü: monument and traffic" hit it); 0.5 mm in
    else:
        cw_ = (W - (ncol - 1) * P02_GAP * kb) / ncol
        cxs = [x0 + j_ * (cw_ + P02_GAP * kb) for j_ in range(ncol)]
        cws = [cw_] * ncol

    def flow(H):
        cols, yo = [[]], 0.0
        for i_, r_ in enumerate(rows):
            need = r_[1] + (rows[i_ + 1][1] if r_[0] == "hdr" and i_ + 1 < len(rows) else 0.0)
            if yo + need > H + 1e-6 and cols[-1]:
                cols.append([])
                yo = 0.0
            cols[-1].append((yo, r_))
            yo += r_[1]
        return cols
    H = max(max(r_[1] for r_ in rows), sum(r_[1] for r_ in rows) / ncol)
    cols = flow(H)
    while len(cols) > ncol:
        H += 1.0
        cols = flow(H)
    Us = 4.0 * kb / 1.1
    low = ytop
    for j_, col_ in enumerate(cols):
        cx, cw = cxs[j_], cws[j_]
        for yo, (kd, rh, c_, lb) in col_:
            yt = ytop - yo * kb                           # the row's top
            if kd == "hdr":
                yk = yt - h75 - 0.6 * kb
                site28_fit(B, u"**{}**".format(lb), cx, yk, h75, cw, INK, L)
                ovl.append(_p02_tb(lb, cx, yk, h75, cw))
            elif kd == "cdisc":                           # the map's disc, at the map's size
                dx, dy = cx + rc + 0.4 * kb, yt - rc - 0.4 * kb
                _sb_marker(B, dx, dy, c_, mk_colour("conflict", c_), kb, L, order=64, r_min=P02_C_R)   # v59 (G-R4-7)
                tx = cx + 2.0 * rc + 2.0 * kb
                site28_fit(B, lb, tx, dy - 0.5 * h75, h75, cx + cw - tx, INK, L)
                ovl.append(_p02_tb(lb, tx, dy - 0.5 * h75, h75, cx + cw - tx))
            else:                                         # the booklet legend's look: 4.0 mm sample, name 5.5 mm in
                yk = yt - h75 - 0.6 * kb
                draw_symbol(B, kd, c_, cx, yk - 0.2 * kb, Us, L, sw=1.1, sh=0.72)
                site28_fit(B, lb, cx + 5.5 * kb, yk, h75, cw - 6.0 * kb, INK, L)
                ovl.append(_p02_tb(lb, cx + 5.5 * kb, yk, h75, cw - 6.0 * kb))
            low = min(low, yt - rh * kb)
    return low


def draw_plan01_key(S, B, x, y, w, U):
    """v51 (WO-T3a-2): plan 01's key panel at the top of p.02's side column (crop drw_plan01_key). v58 (round 3,
    P02.1): the key moved directly under plan 01, inside its crop drw_plan01 (_p02_key_under), so this panel draws
    nothing: it keeps the crop id drw_plan01_key as a 0.5 mm empty strip with no caption, so the booklet's p.02 plan
    (side = drw_plan01_key, drw_edge_types, drw_site_readings) needs no change (session C may drop it from the side
    list, then delete this). Returns the y below."""
    k = w / _p02_side_w()
    crop_panel("plan01_key", x, y - 0.5 * k, x + w, y, u"")
    CROP_PANELS[-1]["bk_w"] = _p02_side_w()               # its width on the booklet page (p.02's side column)
    _p02_ovl_add("plan01_key", (x, y - 0.5 * k, x + w, y), k, [])
    return y - 0.5 * k


# ------------------------------------------------------------ p.2 the site readings beside plan 01
def reading_rows(S):
    """v45: the key question's six readings: (name, phrase, [(m of bank, colour)]), stacked parts dark first. v61
    (G6-6): the edge types' colours from the hue table (_p02_hue "edge_<type>", "wall_<1|2>"), as plan 01 draws them."""
    e = S.edge_len
    wl, em = S.walled_len, getattr(S, "embanked_len", 0.0)
    tot = sum(e.values()) or 1.0
    ec = lambda t_: _p02_hue("edge_" + t_, INK if t_ == "building" else EDGE[t_][1])
    return [("ACCESSIBLE", u"walkable edges within reach", [(e.get("pedestrian", 0.0), ec("pedestrian"))]),
            ("VISIBLE", u"street edges, seen across the water", [(e.get("street", 0.0), ec("street"))]),
            ("PERMEABLE", u"planted edges that let the ground through", [(e.get("green", 0.0), ec("green"))]),
            ("ENCLOSED", u"built edges: backs of buildings face the bed", [(e.get("building", 0.0), ec("building"))]),
            ("DISCONNECTED", u"walled {:.0f}% · embanked {:.0f}%: cut off from the street".format(
                100.0 * wl / tot, 100.0 * em / tot), [(wl, _p02_hue("wall_1", INK2)),
                                                       (em, _p02_hue("wall_2", mix(INK2, PAPER, 0.5)))]),
            ("TRANSFORMABLE", u"parking {:.0f}% · loose {:.0f}%: open to change".format(
                100.0 * e.get("parking", 0.0) / tot, 100.0 * e.get("open", 0.0) / tot),
             [(e.get("parking", 0.0), ec("parking")), (e.get("open", 0.0), ec("open"))])]


def landuse_slices(S):
    """v45: the site frame's ground in plan 01's own colours, for the land-use ring: [(label, colour, m2)]: buildings
    by use, the streets' measured surface, parking & yards, woods and tree cover, parks, grass, shrubs, fields,
    orchards (inferred), vacant ground, the stream and the unmapped rest; under 0.5 % joined as "others"."""
    lcc = dict((k_, c_) for k_, l_, c_ in LC_CLASSES)
    tz = sum(z["A"] for z in S.zones if z["kind"] == "transport")
    gz = {}
    for z in S.zones:
        if z["kind"] == "green":
            sub = z.get("sub") if z.get("sub") in GREEN_SUB else "park"   # as on the plan: other greens in the park tone
            gz[sub] = gz.get(sub, 0.0) + z["A"]
    H = _p02_hue                                          # v61 (G6-6): the hue table's colours, as the plan's
    rows = [(short(CAT[k_][0]), H(k_, CAT[k_][1]), S.area.get(k_, 0.0)) for k_ in
            ("residential", "mixed", "commercial", "institutional", "religious", "industrial")]
    rows += [(u"Streets", H("streets", ROAD_FILL), max(0.0, S.area.get("transport", 0.0) - tz)),
             (u"Parking & yards", H("transport", mix(CAT["transport"][1], PAPER, 0.3)), tz),
             (u"Woods & tree cover", H("g_wood", GREEN_SUB["wood"]), gz.get("wood", 0.0) + rest_of(S, "trees")),
             (u"Parks", H("g_park", GREEN_SUB["park"]), gz.get("park", 0.0)),
             (u"Grass", H("g_grass", GREEN_SUB["grass"]), gz.get("grass", 0.0) + rest_of(S, "grass")),
             (u"Shrubs", H("lc_shrub", lcc.get("shrub", mix(CAT["green"][1], PAPER, 0.3))), rest_of(S, "shrub")),
             (u"Fields & orchards, mapped", H("agri", CAT["agri"][1]), S.area.get("agri", 0.0) + rest_of(S, "farmland")),
             (u"Orchards (satellite)", H("lc_orchard", lcc.get("orchard", ORCH_C)), rest_of(S, "orchard")),
             (u"Vacant ground", H("vacant", CAT["vacant"][1]), S.area.get("vacant", 0.0)),
             (u"The stream", H("water", CAT["water"][1]), S.area.get("water", 0.0)),
             (u"Other unmapped", H("rest", REST_C), rest_of(S, "rest"))]
    tot = frame_total(S) or 1.0
    rows.append((u"Others", H("rest", mix(PAPER, INK2, 0.45)), max(0.0, tot - sum(a for _l, _c, a in rows))))
    keep = [r_ for r_ in rows[:-1] if r_[2] >= 0.005 * tot]
    small = sum(r_[2] for r_ in rows if r_[2] < 0.005 * tot) + (rows[-1][2] if rows[-1][2] >= 0.005 * tot else 0.0)
    if small > 0.0005 * tot:
        keep.append((u"Others, each under 0.5%", rows[-1][1], small))
    # v61 (G6-6): slices of one shade (the table's ranks are fewer than the classes) are one slice and one key row
    return _p02_merge_rows(keep, lab_i=0, col_i=1, area_i=2), tot


def draw_site_readings(S, B, x, y, w, U):
    """v51 (WO-T3a-2, p.02 flipped: Aras "first that map's explanation, below it the edge strip, below that the strip's
    analyses"): p.02's side column, top down: plan 01's key (draw_plan01_key, crop drw_plan01_key), the stream edge
    drawn from above (draw_edge_types, crop drw_edge_types), the bank readings and the land-use ring (_p02_readings,
    crop drw_site_readings). Each its own crop at P02_SIDE_W mm (5 grid columns); returns the y below. v58 (round 3,
    P02.1, G2): plan 01's key is under the map (drw_plan01_key stays an empty strip); the side column is
    _p02_side_w() mm wide (6 grid columns beside a 1:25,000 plan 01); then the page's overlap test (_p02_flag)."""
    y = draw_plan01_key(S, B, x, y, w, U)
    y = draw_edge_types(S, B, x, y, w, U)
    y = _p02_readings(S, B, x, y, w, U)
    _p02_flag()                                           # v58 (round 3, G3): FLAG overlap p02, once
    if "sb_tree_log" in globals():                        # v61 (G6-10): plan 01 and the edge strip, once
        LOG.append(sb_tree_log("p02"))
        if _P02.get("crown_src") == "pack":
            LOG.append(u"FLAG p02 trees: no environment file: crowns from the built-in SEAM_PACK rows (no leaf_src), "
                       u"all drawn generic")
    return y


def _p02_readings_mm(S):
    """v59 (round 4, P02.3): the booklet height (mm) of the site readings crop as _p02_readings lays it out (the same
    steps at 1 board unit per booklet mm; keep the two in step): the bars' column, the ring and the ring's key, the
    deepest of the three, plus the crop's 0.5 mm top margin"""
    h7, h8, h9 = (bk_hk(p_, 1.0) for p_ in (7.0, 8.0, 9.0))
    head = h8 + P02_RD_GAP + h7 + 4.0
    d_bars = head + (len(reading_rows(S)) * (h9 + 1.0 + 2.2 + 1.0 + h7 + 2.0) if sum(S.edge_len.values()) > 0 else 0.0)
    r1 = 17.0
    n_sl = len(landuse_slices(S)[0])
    d_key = head + h7 + max(0, n_sl - 1) * 3.6 + 1.5
    return 0.5 + max(d_bars, head + 2.0 * r1, d_key)


def _p02_readings(S, B, x, y, w, U):
    """v45 (p.2: old p.4 "grain of the town" folded in): the six readings of the bank (accessible ... transformable)
    as bars, and the land use of the site frame as a ring with its key, in plan 01's colours; one panel w wide,
    designed for P02_SIDE_W mm beside plan 01 on the booklet page. Returns the y below. v50 (MIRAQUA 28 Oct, P02.1,
    P02.2): the ring's key on the panel's two-column grid. v51: the last panel of the side column (the edge strip is
    drawn above it by draw_site_readings). Revision 30 Oct (G2, M1: no leftover space): the side column on 5 grid
    columns, the ring's key beside the ring (was under both halves), so the panel prints at its own size, not shrunk."""
    L = "LU_BOARD::SiteReadings"
    k = w / _p02_side_w()                                 # v58 (round 3, G2): the side column's width
    h7, h75, h8, h9, h12 = (bk_hk(p_, k) for p_ in (7.0, 7.5, 8.0, 9.0, 12.0))
    hw = 0.5 * (w - P02_GAP * k)                          # each half; the grid's gutter between them
    top = y
    ovl = []                                              # v58 (round 3, G3): its text boxes for _p02_flag
    # left: the bars
    tot = sum(S.edge_len.values())
    B.text(u"WHERE IS THE STREAM ...?", x, y - h8, h8, INK, L, font=FONT_TITLE, bold=True)
    ovl += [_p02_tb(u"WHERE IS THE STREAM ...?", x, y - h8, h8), _p02_tb(u"% of the bank length · both banks · every "
                                                                          u"4 m [0]", x, y - h8 - P02_RD_GAP * k - h7, h7)]
    B.text(u"% of the bank length · both banks · every 4 m " + bcite(EDGE_SRC), x, y - h8 - P02_RD_GAP * k - h7, h7, INK2,
           L, font=FONT_TITLE)
    yy = y - h8 - P02_RD_GAP * k - h7 - 4.0 * k
    if tot > 0:
        for name, phrase, parts in reading_rows(S):
            pct = 100.0 * sum(v_ for v_, c_ in parts) / tot
            B.text(name, x, yy - h75, h75, INK, L, font=FONT_TITLE, bold=True)
            site28_text(B, u"**{:.0f}%**".format(pct), x + hw, yy - h9, h9, INK, L, align="R")   # v50: real width
            yb = yy - h9 - 1.0 * k
            with B.kind("annotations", u"bar " + name.lower()):    # v61 (G6-9): each bar one element
                B.fill([rect(x, yb - 2.2 * k, x + hw, yb)], _p02_hue("rest", FAINT), L, 20)
                bx = x
                for v_, c_ in parts:
                    if v_ > 0:
                        B.fill([rect(bx, yb - 2.2 * k, bx + hw * v_ / tot, yb)], c_, L, 21)
                        bx += hw * v_ / tot
            sb_keep(B, (x, yb - 2.2 * k, x + hw, yb), u"p02 bar " + name, "bar")   # v59 closing (G-R4-1): no text
            yp = yb - 2.2 * k - 1.0 * k - h7
            B.text(phrase, x, yp, h7, INK2, L, font=FONT_TITLE)
            ovl += [_p02_tb(name, x, yy - h75, h75), _p02_tb(phrase, x, yp, h7)]
            yy = yp - 2.0 * k
    low = yy
    # right: the land-use ring
    rx = x + w - hw
    sl, ftot = landuse_slices(S)
    B.text(u"LAND USE AND GROUND COVER", rx, y - h8, h8, INK, L, font=FONT_TITLE, bold=True)
    B.text(u"site frame · % of its {:,.1f} ha {}".format(ftot / 1e4, bcite(
        u"Land use and ground cover of the site frame (site_alan, {:,.1f} ha), as plan 01 draws it: buildings by use "
        u"and the measured street surfaces from the survey; parks, fields, vacant ground, parking and yards from the "
        u"survey and OpenStreetMap; the unmapped rest by satellite class.".format(ftot / 1e4)) + bcite(LC_CREDIT)),
        rx, y - h8 - P02_RD_GAP * k - h7, h7, INK2, L, font=FONT_TITLE)
    ovl += [_p02_tb(u"LAND USE AND GROUND COVER", rx, y - h8, h8), _p02_tb(u"site frame · % of its 000.0 ha [0][0]", rx,
                                                                            y - h8 - P02_RD_GAP * k - h7, h7)]
    r1, r0 = 17.0 * k, 10.5 * k
    cx, cy = rx + r1, y - h8 - P02_RD_GAP * k - h7 - 4.0 * k - r1
    a0 = math.pi / 2.0
    i0_ring = sb_mark(B)                                  # v59 closing (G-R4-1): the ring's own texts (its centre)
    for lab, col, a in sl:
        a1 = a0 - 2.0 * math.pi * a / ftot
        with B.kind("annotations", u"ring " + lab):       # v61 (G6-9): each slice one element
            B.fill([annulus(cx, cy, r0, r1, a0, a1)], col, L, 20)
            B.line([(cx + r0 * math.cos(a0), cy + r0 * math.sin(a0)),
                    (cx + r1 * math.cos(a0), cy + r1 * math.sin(a0))], WHITE, L, 21, bk_lw(0.25, k))
        a0 = a1
    site28_text(B, u"**{:,.1f}**".format(ftot / 1e4), cx, cy + 0.6 * k, h12, INK, L, align="C")   # v50: real widths
    site28_text(B, u"ha", cx, cy - 1.4 * k - h7, h7, INK2, L, align="C")
    sb_keep(B, (cx - r1, cy - r1, cx + r1, cy + r1), u"p02 land-use ring", "ring", i0_ring)
    low = min(low, cy - r1)
    # beside the ring: its key (the plan's ground and green colours, so the plan needs no other key), next to its
    # drawing (G1); each entry as the booklet's legend_item draws one: a 4.0 x 2.8 mm swatch from 0.2 mm under the
    # baseline, the name 5.5 mm in at 7 pt, 3.6 mm a row
    kx = cx + r1 + P02_GAP * k
    kw = rx + hw - kx
    ky = cy + r1 - h7
    i0_rk = sb_mark(B)                                    # v59 closing (G-R4-1): the ring key's own texts
    for j, (lab, col, a) in enumerate(sl):
        yk = ky - j * 3.6 * k
        with B.kind("legend", u"ring key " + lab):
            B.fill([rect(kx, yk - 0.2 * k, kx + 4.0 * k, yk + 2.6 * k)], col, L, 20)
        pct = 100.0 * a / ftot
        site28_fit(B, u"{} {}".format(lab, u"{:.0f}%".format(pct) if pct >= 1.0 else u"< 1%"), kx + 5.5 * k, yk, h7,
                   kw - 5.5 * k, INK, L)
        ovl.append(_p02_tb(lab + u" 00%", kx + 5.5 * k, yk, h7, kw - 5.5 * k))
    low = min(low, ky - max(0, len(sl) - 1) * 3.6 * k - 1.5 * k)
    if sl:
        sb_keep(B, (kx, ky - (len(sl) - 1) * 3.6 * k - 0.2 * k, rx + hw, ky + 2.6 * k), u"p02 ring key", "legend",
                i0_rk)
    if sl:
        _p02_legend_log()                                 # v61 (G6-6): the ring key reads the hue table
    crop_panel("site_readings", x, low, x + w, top + 0.5 * k, u"Site readings · bank and ground")
    CROP_PANELS[-1]["bk_w"] = _p02_side_w()               # v45: its width on the booklet page (side panel of p.2) ...
    _p02_ovl_add("site_readings", (x, low, x + w, top + 0.5 * k), k, ovl)
    CROP_PANELS[-1]["grid"] = [0.0, (w - hw) / k]         # ... and its two halves' left edges (the legend under it)
    return low - 1.0 * U                                  # v51: the edge strip now sits above (draw_site_readings)


def site28_project(LX, LY, LC, pts):
    """the chainage and signed offset (m; + left, looking downstream) of each point on a centreline with vertices
    LX, LY and chainages LC: from its nearest vertex and the line's direction there (as shade_strip_calc)"""
    n = len(LX)
    if not pts:
        return []
    if HAVE_NP:
        X, Y = np.asarray(LX, float), np.asarray(LY, float)
        Q = np.asarray(pts, float)
        J = np.zeros(len(pts), np.int64)
        for a in range(0, len(pts), 500):                 # in chunks (memory)
            c_ = Q[a:a + 500]
            d2 = (c_[:, 0][:, None] - X[None, :]) ** 2 + (c_[:, 1][:, None] - Y[None, :]) ** 2
            J[a:a + 500] = d2.argmin(axis=1)
        J = [int(j_) for j_ in J]
    else:                                                 # every 10th vertex, then its neighbours
        cand = list(range(0, n, 10)) + [n - 1]
        J = []
        for px, py in pts:
            i0 = min(cand, key=lambda i: (LX[i] - px) ** 2 + (LY[i] - py) ** 2)
            J.append(min(range(max(0, i0 - 10), min(n, i0 + 11)), key=lambda i: (LX[i] - px) ** 2 + (LY[i] - py) ** 2))
    out = []
    for (px, py), j in zip(pts, J):
        tx, ty = LX[min(n - 1, j + 1)] - LX[max(0, j - 1)], LY[min(n - 1, j + 1)] - LY[max(0, j - 1)]
        tl = math.hypot(tx, ty) or 1.0
        tx, ty = tx / tl, ty / tl
        dx, dy = px - LX[j], py - LY[j]
        out.append((LC[j] + tx * dx + ty * dy, tx * dy - ty * dx))
    return out


def site28_edge_bins(S):
    """v50 (MIRAQUA 28 Oct, P02.2): the bank edge samples (S.edge_samples: every 4 m, the bars' own data) on the data
    pack's centreline (the tree-cover and shade charts' chainage, 0 at the upstream frame edge): dict(n, bm, L,
    bins = [left, right], each [(type, walled 0/1/2) or None per SITE28_ET_BIN bin: the most samples], used = m of
    bank drawn, tot = m the bars count, cor, line); None without samples or line. Once per run (S._s28_et)."""
    if getattr(S, "_s28_et", None) is not None:
        return S._s28_et or None
    S._s28_et = {}
    pk = seam_pack()
    cor, sel = pk.get("corridor") or {}, pk.get("selinos") or {}
    LX, LY, LC = ([float(v_) for v_ in (sel.get(q) or [])] for q in ("x", "y", "ch"))
    if len(LX) < 2 or len(LC) != len(LX) or len(LY) != len(LX) or not getattr(S, "edge_samples", None):
        return None
    Lt = float(cor.get("n_bins") or 0) * float(cor.get("bin_m") or 0.0) or LC[-1]
    nb = max(1, int(math.ceil(Lt / SITE28_ET_BIN)))
    cnt = [[None] * nb, [None] * nb]
    used = 0
    for (ex, ey, t_, wl_), (s_, o_) in zip(S.edge_samples, site28_project(LX, LY, LC, [(e[0], e[1])
                                                                                     for e in S.edge_samples])):
        if abs(o_) > SITE28_ET_NEAR or not 0.0 <= s_ < Lt:
            continue
        sd = 0 if o_ > 0.0 else 1
        i_ = min(nb - 1, int(s_ / SITE28_ET_BIN))
        if cnt[sd][i_] is None:
            cnt[sd][i_] = ({}, {})
        tc, wc = cnt[sd][i_]
        tc[t_] = tc.get(t_, 0) + 1
        wc[wl_] = wc.get(wl_, 0) + 1
        used += 1
    bins = []
    for sd in (0, 1):
        row = []
        for c_ in cnt[sd]:
            if c_ is None:
                row.append(None)
                continue
            tc, wc = c_
            row.append((max(sorted(tc), key=lambda q: (tc[q], q)), max(sorted(wc), key=lambda q: (wc[q], q))))
        for i_ in range(1, nb - 1):                       # a one-bin gap between two equal bins is closed
            if row[i_] is None and row[i_ - 1] is not None and row[i_ - 1] == row[i_ + 1]:
                row[i_] = row[i_ - 1]
        bins.append(row)
    S._s28_et = dict(n=nb, bm=SITE28_ET_BIN, L=Lt, bins=bins, used=4.0 * used, tot=4.0 * len(S.edge_samples), cor=cor,
                     line=(LX, LY, LC))
    return S._s28_et


def site28_runs(vals):
    """[(i0, i1, value)]: the runs of equal values (None left out)"""
    out, i = [], 0
    while i < len(vals):
        j = i
        while j + 1 < len(vals) and vals[j + 1] == vals[i]:
            j += 1
        if vals[i] is not None:
            out.append((i, j + 1, vals[i]))
        i = j + 1
    return out


def _p02_join(vals, nmin):
    """v51: runs of equal values shorter than nmin bins take the value of their longer touching neighbour, the
    shortest first (None = no data: never joined, never joins)"""
    v = list(vals)
    for _it in range(20000):
        runs = site28_runs(v)
        done = True
        for j in sorted(range(len(runs)), key=lambda q: runs[q][1] - runs[q][0]):
            i0, i1, val = runs[j]
            if i1 - i0 >= nmin:
                break
            nb_ = [r_ for r_ in ((runs[j - 1] if j > 0 else None), (runs[j + 1] if j + 1 < len(runs) else None))
                   if r_ is not None and (r_[1] == i0 or r_[0] == i1)]
            if not nb_:
                continue
            best = max(nb_, key=lambda r_: r_[1] - r_[0])
            for i in range(i0, i1):
                v[i] = best[2]
            done = False
            break
        if done:
            break
    return v


def _p02_strip(S, d, den=5000.0):
    """v51: the edge strip's data, once per run (S._p02_st; build once, reuse): on the straightened stream
    (d = site28_edge_bins) per bank the edge types and the bank faces (walled 1, embanked 2, else 0) as stretches
    (_p02_join, P02_ET_MIN), the bank line's distance from the centreline per bin (the bank samples' mean, smoothed
    over 7 bins), and what stands within P02_ET_LAND m beyond the bank line, in (chainage m, m beyond the bank line):
    the canopy map's crowns, the survey buildings, green ground (parks, woods, grass) and the footpaths. Round 2 (31
    Oct, PG1 p2 #6): the buildings are strict blocks st["boxes"] = [(bank, s0, s1, b0, b1)] (_p02_strip_boxes), their
    roofs drawn on the page; den is no longer used (kept for the callers)."""
    st = getattr(S, "_p02_st", None)
    if st is not None:
        return st
    LX, LY, LC = d["line"]
    nb, bm, Lt = d["n"], d["bm"], d["L"]
    reach = SITE28_ET_NEAR + P02_ET_LAND + 60.0           # m from the centreline: anything farther is not drawn
    acc = [[[0.0, 0] for _i in range(nb)] for _s in (0, 1)]
    for s_, o_ in site28_project(LX, LY, LC, [(e[0], e[1]) for e in S.edge_samples]):
        if abs(o_) <= SITE28_ET_NEAR and 0.0 <= s_ < Lt:
            a_ = acc[0 if o_ > 0.0 else 1][min(nb - 1, int(s_ / bm))]
            a_[0] += abs(o_)
            a_[1] += 1
    off = []
    for sd in (0, 1):
        row = [a_ / n_ if n_ else None for a_, n_ in acc[sd]]
        known = [i for i, v_ in enumerate(row) if v_ is not None]
        full = [row[min(known, key=lambda q: abs(q - i))] if known else 10.0 for i in range(nb)]
        off.append([sum(full[max(0, i - 3):i + 4]) / len(full[max(0, i - 3):i + 4]) for i in range(nb)])

    def beyond(s_, o_, sd):
        return abs(o_) - off[sd][min(nb - 1, max(0, int(s_ / bm)))]

    def near(items, ctr):
        q = site28_project(LX, LY, LC, [ctr(it) for it in items])
        return [it for it, (s_, o_) in zip(items, q) if -60.0 <= s_ <= Lt + 60.0 and abs(o_) < reach]

    def rings_of(rings, cap):
        out = []
        for P in rings:
            if len(P) < 3:
                continue
            q = site28_project(LX, LY, LC, P)
            sides = set(0 if o_ > 0.0 else 1 for s_, o_ in q)
            if len(sides) != 1:                           # across the stream (a bridge deck, a big zone): left out
                continue
            sd = sides.pop()
            ring = [(s_, beyond(s_, o_, sd)) for s_, o_ in q]
            ss, dd = [r_[0] for r_ in ring], [r_[1] for r_ in ring]
            if max(ss) < 0.0 or min(ss) > Lt or min(dd) > P02_ET_LAND or max(dd) < -1.0 or max(ss) - min(ss) > cap:
                continue
            out.append((sd, ring))
        return out

    def ctr(P):
        return (sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P))
    boxes = _p02_strip_boxes(S, LX, LY, LC, Lt, reach, beyond, ctr)
    gr = []
    for z in near([z for z in S.zones if z["kind"] == "green" and z.get("Ps")], lambda z: ctr(z["Ps"][0])):
        gr += [(sd, ring, z.get("sub")) for sd, ring in rings_of(z["Ps"], 400.0)]
    crw = site_crowns(S, S.F)
    cr = []
    for c, (s_, o_) in zip(crw, site28_project(LX, LY, LC, [(c[0], c[1]) for c in crw])):
        if 0.0 <= s_ < Lt and abs(o_) < reach:
            sd = 0 if o_ > 0.0 else 1
            b_ = beyond(s_, o_, sd)
            if -3.0 <= b_ <= P02_ET_LAND:
                cr.append((sd, s_, b_, c[2], c[4], c))    # v61 (G6-10): + the crown, for its species
    pth = []
    for p in S.paths:
        P = p.get("P") or []
        if len(P) < 2:
            continue
        cur, csd = [], None
        for s_, o_ in site28_project(LX, LY, LC, P):
            sd = 0 if o_ > 0.0 else 1
            b_ = beyond(s_, o_, sd)
            ok = 0.0 <= b_ <= P02_ET_LAND + 5.0 and -5.0 <= s_ <= Lt + 5.0 and abs(o_) < reach
            if ok and (csd is None or (sd == csd and abs(s_ - cur[-1][0]) < 40.0)):
                cur.append((s_, b_))
                csd = sd
            else:
                if len(cur) > 1:
                    pth.append((csd, cur))
                cur, csd = ([(s_, b_)], sd) if ok else ([], None)
        if len(cur) > 1:
            pth.append((csd, cur))
    nmin = max(1, int(round(P02_ET_MIN / bm)))
    blocks = _p02_blocks(boxes)                           # v58 (round 3, P02.2): no footprint over another
    st = dict(types=[_p02_join([v_[0] if v_ else None for v_ in d["bins"][sd]], nmin) for sd in (0, 1)],
              walls=[_p02_join([v_[1] if v_ else None for v_ in d["bins"][sd]], nmin) for sd in (0, 1)],
              off=off, crowns=cr, boxes=boxes, blocks=blocks, greens=gr, paths=pth)
    S._p02_st = st
    LOG.append(u"Stream edge strip (drw_edge_types): {} crowns, {} buildings drawn as {} blocks beyond the {:.0f} m "
               u"edge zone (touching ones merged, none overlapping: {} single, {} merged), {} green areas and {} path "
               u"pieces within {:.0f} m of the banks; stretches under {:.0f} m joined to their neighbour.".format(
                   len(cr), len(boxes), len(blocks), P02_ET_ZONE, sum(1 for b_ in blocks if b_[2] == 1),
                   sum(1 for b_ in blocks if b_[2] > 1), len(gr), len(pth), P02_ET_LAND, P02_ET_MIN))
    return st


def _p02_strip_boxes(S, LX, LY, LC, Lt, reach, beyond, ctr):
    """round 2 (31 Oct, PG1 p2 #6, U18: "brown boxes meaningless"): each survey building within reach of the stream
    as ONE strict block on the strip = the extent of its footprint in the strip's (chainage m, m beyond the bank
    line) on its bank: [(bank, s0, s1, b0, b1)]. The straightening bends every footprint, so the bent outlines and
    roof lines of the 30 Oct strip tangled; the block keeps where and how big each building is and gets its roof drawn
    on the page (draw_edge_types). Left out: a building across the stream, out of the frame's chainage, past
    P02_ET_LAND or longer than 150 m along the stream. All points projected in one go."""
    if not S.bld:
        return []
    cen = site28_project(LX, LY, LC, [ctr(u["parts"][0]) if u.get("parts") else (LX[0], LY[0]) for u in S.bld])
    pts, segs = [], []
    for u, (s_, o_) in zip(S.bld, cen):
        if not u.get("parts") or not (-60.0 <= s_ <= Lt + 60.0 and abs(o_) < reach):
            continue
        P = [p_ for R in u["parts"] for p_ in R]
        if len(P) >= 3:
            segs.append((len(pts), len(P)))
            pts.extend(P)
    q = site28_project(LX, LY, LC, pts)
    out = []
    for i0, m_ in segs:
        Q = q[i0:i0 + m_]
        sides = set(0 if o_ > 0.0 else 1 for s_, o_ in Q)
        if len(sides) != 1:
            continue
        sd = sides.pop()
        ss = [s_ for s_, o_ in Q]
        dd = [beyond(s_, o_, sd) for s_, o_ in Q]
        if max(ss) < 0.0 or min(ss) > Lt or min(dd) > P02_ET_LAND or max(dd) < -1.0 or max(ss) - min(ss) > 150.0:
            continue
        out.append((sd, min(ss), max(ss), max(0.0, min(dd)), min(P02_ET_LAND, max(dd))))
    return out


def _p02_roof_block(B, P, k, L, order):
    """round 2 (PG1 p2 #6, G7, M11, R01): one building from above on the edge strip: the roof tone, its roof read as
    a hipped roof (ridge, hips, fall lines every 0.4 booklet mm: bld_roof_lines "hatch"; hipped = the repo's M11
    drawing convention, roof forms are not surveyed) where it is wide enough to read, its outline firm"""
    xs, ys = [p_[0] for p_ in P], [p_[1] for p_ in P]
    dw = min(max(xs) - min(xs), max(ys) - min(ys))
    B.fill([P], _p02_hue("et_roof", P02_ROOF), L, order)   # v61 (G6-6): CTX r3
    if dw >= 0.6 * k:
        for a_, b_ in bld_roof_lines(P, "hatch" if dw >= 1.0 * k else "ridge", spacing=0.4 * k):
            B.line([a_, b_], P02_ROOF_L, L, order, bk_lw(0.05, k))
    B.line(list(P) + [P[0]], INK, L, order, bk_lw(0.12, k))


def _p02_blocks(boxes, zone=P02_ET_ZONE, tol=P02_ET_TOL, step=P02_ET_STEP):
    """v58 (round 3, P02.2, G7; U02 "houses pile up and overlap"): the strip's building blocks with NO overlap: each
    building's block (bank, s0, s1, b0, b1 in chainage m and m beyond the bank line, _p02_strip_boxes) cut to the land
    beyond the edge zone (b >= zone: the edge zone keeps its edge type's own drawing, built included, readable), then
    blocks that overlap or touch (within tol m along or across the strip) merged, again until none touches another;
    each merged group drawn as ONE outline: per step m of chainage from its nearest to its farthest extent (gaps
    inside a group close up, as a town block). Returns [(bank, ring [(s, b)], n buildings)]."""
    import math as _m
    out = []
    for sd in (0, 1):
        rs = [(a_, b_, max(d0, zone), d1) for s_, a_, b_, d0, d1 in boxes
              if s_ == sd and b_ > a_ and d1 > max(d0, zone) + 0.5]
        if not rs:
            continue

        def env(c):                                       # {bin: [lo, hi]}, bins contiguous (gaps take the last)
            e = {}
            for a_, b_, d0, d1 in c:
                for i in range(int(_m.floor(a_ / step)), int(_m.ceil(b_ / step))):
                    v = e.get(i)
                    e[i] = [d0, d1] if v is None else [min(v[0], d0), max(v[1], d1)]
            ks = sorted(e)
            for i in range(ks[0], ks[-1] + 1):
                if i not in e:
                    e[i] = list(e[i - 1])
            return e

        def hit(ea, eb):
            for i, (lo, hi) in eb.items():
                for j in (i - 1, i, i + 1):
                    v = ea.get(j)
                    if v is not None and v[0] <= hi + tol and lo <= v[1] + tol:
                        return True
            return False
        cl = [[r_] for r_ in sorted(rs)]
        for _it in range(200):
            cl.sort(key=lambda c: min(r_[0] for r_ in c))
            es = [env(c) for c in cl]
            ends = [max(r_[1] for r_ in c) for c in cl]
            used, nxt, moved = [False] * len(cl), [], False
            for i in range(len(cl)):
                if used[i]:
                    continue
                cur, ec, end = list(cl[i]), es[i], ends[i]
                for j in range(i + 1, len(cl)):
                    if used[j]:
                        continue
                    if min(r_[0] for r_ in cl[j]) > end + tol + step:
                        break
                    if hit(ec, es[j]):
                        cur += cl[j]
                        ec, end = env(cur), max(end, ends[j])
                        used[j] = moved = True
                nxt.append(cur)
            cl = nxt
            if not moved:
                break
        for c in cl:
            e = env(c)
            ks = sorted(e)
            a0, b1 = min(r_[0] for r_ in c), max(r_[1] for r_ in c)
            lo_, hi_ = [], []
            for i in ks:
                x0, x1 = max(i * step, a0), min((i + 1) * step, b1)
                if x1 <= x0:
                    continue
                lo_ += [(x0, e[i][0]), (x1, e[i][0])]
                hi_ += [(x0, e[i][1]), (x1, e[i][1])]
            ring = lo_ + hi_[::-1]
            pts = []
            for p_ in ring:                               # drop repeats and points on a straight run
                if pts and abs(p_[0] - pts[-1][0]) < 1e-9 and abs(p_[1] - pts[-1][1]) < 1e-9:
                    continue
                if len(pts) >= 2 and ((abs(pts[-2][1] - pts[-1][1]) < 1e-9 and abs(pts[-1][1] - p_[1]) < 1e-9) or
                                      (abs(pts[-2][0] - pts[-1][0]) < 1e-9 and abs(pts[-1][0] - p_[0]) < 1e-9)):
                    pts[-1] = p_
                    continue
                pts.append(p_)
            if len(pts) >= 3:
                out.append((sd, pts, len(c)))
    return out


def _p02_block_roof(B, P, k, L, order):
    """v58 (round 3, P02.2, G7): a merged block of buildings from above on the edge strip: the roof tone, a simple
    roof hatch (fall lines 0.6 booklet mm apart at 45 degrees; roof forms are not surveyed) and one firm outline:
    no party walls drawn (not surveyed)"""
    B.fill([P], _p02_hue("et_roof", P02_ROOF), L, order)   # v61 (G6-6): CTX r3
    B.hatch([P], P02_ROOF_L, L, order, 0.6 * k, math.radians(45.0), bk_lw(0.05, k))
    B.line(list(P) + [P[0]], INK, L, order, bk_lw(0.12, k))


def _p02_crown(leaf, cx, cy, D, k, seed=0, sp=None):
    """a tree from above D board units wide: plants.py pla_plan's crown of the species standing for the canopy map's
    leaf type (P02_LEAF_SP), scaled to D; a plain crown when the plant module is missing. v61 (G6-10): sp = the
    tree's species glyph key (sb_tree_species); None = the generic glyph of its leaf type (never named)"""
    fn = globals().get("pla_plan")
    if fn is not None:
        old_ = pla_images(False) if "pla_images" in globals() else None   # v60 (S4 interface): this putter takes
        try:                                                                # vector rings only (no image items)
            cm = 10.0
            sh = fn(sp or P02_LEAF_SP.get(leaf, "plane"), 0.0, 0.0, D / k / cm, crown_m=cm, seed=seed)
            return [(s_[0], [(cx + px * k, cy + py * k) for px, py in s_[1]]) + tuple(s_[2:]) for s_ in sh]
        except Exception:
            pass
        finally:
            if old_ is not None:
                pla_images(old_)
    return [("poly", circle_pts(cx, cy, 0.5 * D, 14), _p02_hue("crown_%s" % leaf, mix(LEAF_COL.get(leaf, LEAF_COL[0]),
                                                                                     PAPER, 0.15)), INK2, 0.08)]


def _p02_zone(B, t, x0, x1, yw, yl, k, L, order):
    """v51: one edge type's own drawing from above in the edge zone x0-x1 (yw the water side, yl the land side):
    walkable = paving with people walking it, street = carriageway with kerbs and a centre line, parking = bays,
    planted = grass with tufts, loose = bare ground stippled, built = the buildings' backs on the water"""
    if x1 - x0 < 0.15 * k:
        return
    ya, yb = min(yw, yl), max(yw, yl)
    hz = yb - ya
    r_ = rect(x0, ya, x1, yb)
    sg = 1.0 if yl > yw else -1.0                         # towards the land
    if t == "pedestrian":
        B.fill([r_], _p02_hue("et_walk", mix(EDGE["pedestrian"][1], PAPER, 0.8)), L, order)   # v61: MOV r4
        jc = mix(INK2, PAPER, 0.55)                       # revision 30 Oct (R02): paving slabs in a running bond
        for yj in (ya + hz / 3.0, ya + 2.0 * hz / 3.0):   # course joints
            B.line([(x0, yj), (x1, yj)], jc, L, order + 1, bk_lw(0.05, k))
        for c_ in range(3):                               # cross joints, staggered course to course
            xx = x0 + (0.35 if c_ % 2 else 0.7) * k
            while xx < x1:
                B.line([(xx, ya + c_ * hz / 3.0), (xx, ya + (c_ + 1) * hz / 3.0)], jc, L, order + 1, bk_lw(0.05, k))
                xx += 0.7 * k
        B.line([(x0, yl), (x1, yl)], INK2, L, order + 1, bk_lw(0.1, k))
        n = int((x1 - x0) / (4.2 * k)) or (1 if x1 - x0 >= 2.0 * k else 0)
        for j in range(n):                                # people walking it, both ways
            fx = x0 + (j + 0.5) * (x1 - x0) / n
            fy = 0.5 * (ya + yb) + (0.08 if j % 2 else -0.08) * hz
            with B.kind("people"):                    # v61 (G6-9): each walker its own element
                _p02_put(B, _p02_fig("walk", fx, fy, 3.0 * k, view="top", ang=0.0 if j % 2 else math.pi,
                                     mm_per_m=3.0), L, order + 3, k)
    elif t == "street":
        B.fill([r_], _p02_hue("et_road", P02_ROAD), L, order)            # v61 (G6-6): CTX r2
        for y_ in (ya, yb):                               # kerbs
            B.line([(x0, y_), (x1, y_)], INK, L, order + 1, bk_lw(0.12, k))
        for d_ in dashes([(x0, 0.5 * (ya + yb)), (x1, 0.5 * (ya + yb))], 0.9 * k, 0.6 * k):
            B.line(d_, WHITE, L, order + 1, bk_lw(0.12, k))
    elif t == "parking":
        B.fill([r_], _p02_hue("et_park", mix(INK2, PAPER, 0.62)), L, order)   # v61 (G6-6): CTX r3
        B.line([(x0, yl), (x1, yl)], INK, L, order + 1, bk_lw(0.1, k))
        xx = x0 + 1.1 * k
        while xx < x1:                                    # bays
            B.line([(xx, yw), (xx, yw + sg * 0.75 * hz)], WHITE, L, order + 1, bk_lw(0.1, k))
            xx += 1.1 * k
    elif t == "green":
        B.fill([r_], _p02_hue("et_green", mix(GREEN_SUB["grass"], PAPER, 0.35)), L, order)   # v61: GRN r4
        tc, xx, j = _p02_hue("edge_green", mix(GREEN_SUB["wood"], INK, 0.15)), x0 + 0.5 * k, 0
        while xx < x1 - 0.3 * k:                          # grass tufts
            ty = ya + (0.3 if j % 2 else 0.62) * hz
            B.line([(xx - 0.25 * k, ty + 0.35 * k), (xx, ty), (xx + 0.25 * k, ty + 0.35 * k)], tc, L, order + 1,
                   bk_lw(0.07, k))
            xx += 0.9 * k
            j += 1
    elif t == "open":
        B.fill([r_], _p02_hue("et_open", mix(EDGE["open"][1], PAPER, 0.5)), L, order)   # v61 (G6-6): CTX r4
        dc = mix(INK2, PAPER, 0.2)
        for j in range(int((x1 - x0) / (0.45 * k))):     # bare ground, stippled
            B.fill([circle_pts(x0 + (j + 0.5) * 0.45 * k, ya + ((j * 37) % 10 + 0.5) / 10.0 * hz, 0.1 * k, 6)], dc, L,
                   order + 1)
    elif t == "building":                                 # round 2 (PG1 p2 #6, G7): the row of roofs on the water
        _p02_roof_block(B, r_, k, L, order)               # as the blocks beyond (ridge, hips, fall lines); no
        #                                                   party walls at a made-up spacing (not surveyed)
        B.line([(x0, yw), (x1, yw)], INK, L, order + 2, bk_lw(0.45, k))     # the backs on the water


def _p02_wall(B, wl, x0, x1, yw, yl, k, L, order):
    """v51: the bank face between the land (yl) and the water (yw) from above: a wall in stone courses (1), an
    embankment in slope hachures from its top line down to the water (2), else the ground running to the water"""
    if x1 - x0 < 0.15 * k:
        return
    ya, yb = min(yw, yl), max(yw, yl)
    r_ = rect(x0, ya, x1, yb)
    sg = 1.0 if yl > yw else -1.0
    gr_ = _p02_hue("et_ground", P02_GROUND)                # v61 (G6-6): CTX r5
    if wl == 1:
        B.fill([r_], _p02_hue("wall_1", mix(INK2, PAPER, 0.25)), L, order)   # v61: CTX r2
        ym = 0.5 * (ya + yb)
        B.line([(x0, ym), (x1, ym)], gr_, L, order + 1, bk_lw(0.05, k))
        xx, j = x0 + 0.45 * k, 0
        while xx < x1:                                    # joints, staggered course to course
            B.line([(xx, ya if j % 2 else ym), (xx, ym if j % 2 else yb)], gr_, L, order + 1, bk_lw(0.05, k))
            xx += 0.45 * k
            j += 1
        for y_ in (ya, yb):
            B.line([(x0, y_), (x1, y_)], INK, L, order + 1, bk_lw(0.12, k))
    elif wl == 2:
        B.fill([r_], _p02_hue("et_open", mix(EDGE["open"][1], PAPER, 0.6)), L, order)   # v61: CTX r4
        B.line([(x0, yl), (x1, yl)], INK2, L, order + 1, bk_lw(0.12, k))   # top of the slope
        xx, j = x0 + 0.25 * k, 0
        while xx < x1:                                    # hachures, long and short, down to the water
            B.line([(xx, yl), (xx, yl - sg * (yb - ya) * (0.95 if j % 2 == 0 else 0.5))], INK2, L, order + 1,
                   bk_lw(0.07, k))
            xx += 0.45 * k
            j += 1
    else:
        B.fill([r_], gr_, L, order)


def _p02_water(B, x0, y0, x1, y1, k, L, order, seed=0, bank=True):
    """revision 30 Oct (G8, M5): water in the rectangle x0-x1, y0-y1 (board units) through water.py's water_plan
    (calm surface, flow streaks along the stream deepening toward the middle, the bank edge), drawn in booklet mm
    (k = board units per booklet mm); a plain fill only when the module is missing or fails (logged once)"""
    fn = globals().get("water_plan")
    if fn is not None:
        try:
            ring = [(x0 / k, y0 / k), (x1 / k, y0 / k), (x1 / k, y1 / k), (x0 / k, y1 / k)]
            sh = fn(ring, 1.0, flow_deg=0.0, bank=bank, seed=seed, spacing=0.9).shapes()
            _p02_put(B, [(s_[0], [(px * k, py * k) for px, py in s_[1]]) + tuple(s_[2:]) for s_ in sh], L, order, k)
            return
        except Exception:
            if not _P02.get("wlog"):
                _P02["wlog"] = 1
                LOG.append("WARNING: the edge strip's water (water_plan) failed, drawn as a plain fill:\n" +
                           traceback.format_exc())
    B.fill([rect(x0, y0, x1, y1)], _p02_hue("water", CAT["water"][1]), L, order)


def _p02_deck(B, x0, y0, x1, y1, k, L, order):
    """revision 30 Oct (R02): a bridge deck over the water from above: the deck in planks across the way it crosses
    (y), its two edges firm"""
    B.fill([rect(x0, y0, x1, y1)], WHITE, L, order)
    pc, yy = mix(INK2, PAPER, 0.5), y0 + 0.35 * k
    while yy < y1 - 0.1 * k:
        B.line([(x0, yy), (x1, yy)], pc, L, order, bk_lw(0.05, k))
        yy += 0.35 * k
    for xe in (x0, x1):
        B.line([(xe, y0), (xe, y1)], INK, L, order, bk_lw(0.15, k))


def draw_edge_types(S, B, x, y, w, U, _gap=None, _pre=None, _measure=False):
    """v51 (WO-T3a-2, Aras: "redraw it in a top-view architectural drawing language ... not an analysis"; the idea of
    R01: each stretch of the corridor in its own drawn language): both banks of the Selinos stream straightened along
    its chainage (no scale: a diagram) and seen from above, in P02_ET_ROWS rows (upstream half over downstream half).
    The stream in the middle with its covered reaches hatched and its bridges as decks; on each bank the bank face (a
    wall in stone courses, an embankment in slope hachures) and an edge zone in its edge type's language (_p02_zone:
    people walking where it is walkable, a carriageway, parking bays, grass, bare ground, the buildings' backs), and
    beyond it what stands within P02_ET_LAND m of the water (_p02_strip): green ground, footpaths, the survey's
    buildings, the canopy map's trees (plants.py crowns). The same 4 m bank samples as the bars (site28_edge_bins),
    stretches under P02_ET_MIN m joined to their neighbour. (v61: the edge types named in the key only), the bridges
    under each row (v58: by real name, or their p.02 number where no room), the key as drawn samples. Its own crop
    (drw_edge_types), _p02_side_w() mm in p.02's side column (v58: at its top, plan 01's key is under the map); words 6.5-8 pt. Returns the y below. Revision 30 Oct (PG1 p2, G7, G8, M2, M5, M11): buildings as
    outline + roof (bld_plan_items, no piece lines), the water through water_plan, decks in planks, paving in slabs, the
    key laid out by M2 Legend under the drawing; the page's finding (walled ... walkable ...) is the booklet intro
    only (not repeated here). v59 (round 4, P02.3; Aras U61 "üçünün arasındaki mesafe çok dar birbirinden farklı
    durmuyor ... sayfanın altındaki boşluk kullanarak"): the three rows spaced apart by the side column's empty band
    at the page bottom (_gap booklet mm between rows: the free height of the side column, measured by a first pass
    into a scratch Board (_measure=True returns the crop's booklet height), less the readings crop under it
    (_p02_readings_mm), shared by the rows, at most P02_ET_GAP_MAX), and each row headed by its reach (upstream /
    middle / downstream) and chainage, so the three read as three different stretches. _pre = (d, st) of the first
    pass."""
    L = "LU_BOARD::SiteReadings"
    d = _pre[0] if _pre else site28_edge_bins(S)
    if not d:
        LOG.append("Stream edge diagram (drw_edge_types): no bank samples or no centreline in the data pack, so not "
                   "drawn.")
        return y
    k = w / _p02_side_w()                                 # v58 (round 3, G2): the side column's width
    if _gap is None:                                      # v59 (round 4, P02.3): measure, then share the free band
        my0 = P02_ET_HB * k / P02_ET_LAND
        pre = (d, _p02_strip(S, d, den=bk_std(1000.0 * k / my0)))
        h0 = draw_edge_types(S, Board(), x, y, w, U, _gap=0.0, _pre=pre, _measure=True)
        h_rd = _p02_readings_mm(S)
        nr0 = max(1, P02_ET_ROWS)
        free = P02_SIDE_H - 2.0 * P02_CAP_H - P02_SIDE_SAFE - h_rd - h0
        _gap = max(0.0, min(P02_ET_GAP_MAX, free / nr0)) if nr0 > 1 else 0.0
        _pre = pre
        LOG.append(u"p02 edge from above (P02.3): crop {:.0f} mm + readings {:.0f} mm in the {:.0f} mm side column; "
                   u"{:.1f} mm added between its {} rows".format(h0 + (nr0 - 1) * _gap, h_rd, P02_SIDE_H, _gap, nr0))
    h65, h7, h8 = bk_hk(6.5, k), bk_hk(7.0, k), bk_hk(8.0, k)
    top = y
    ovl = []                                              # v58 (round 3, G3): its text boxes for _p02_flag
    knum = _p02_knum()                                    # v58 (round 3, G16): the bridges' numbers on p.02
    knm = []                                              # [(number, name)] of bridges shown by number (no room)
    # revision 30 Oct (G4): the heading names the drawing; the finding (walled ... walkable ...) is the page intro
    site28_fit(B, u"**THE STREAM EDGE FROM ABOVE · BOTH BANKS, STRAIGHTENED**", x, y - h8, h8, w, INK, L)
    ovl.append(_p02_tb(u"THE STREAM EDGE FROM ABOVE · BOTH BANKS, STRAIGHTENED", x, y - h8, h8, w))
    yy = site28_para(B, u"What stands within {:.0f} m of the water, **left** and **right** bank looking downstream; "
                        u"chainage in m from the upstream end of the frame {}{}".format(
                            P02_ET_LAND, bcite(EDGE_SRC),
                            bcite("Crowns: modelled heights and leaf types (Meta/WRI 1 m canopy height map, Tolan et al. "
                                  "2024; CLC+ 2021 and Sentinel-2).")),
                     x, y - h8 - 1.6 * k - h7, w, h7, INK2, L, lead=1.45)
    ovl.append((x, yy + 1.45 * h7 - 0.25 * h7, x + w, y - h8 - 1.6 * k))   # the line(s) under the heading
    lab_w = max(site28_tw(t_, h65, True) for t_ in (u"LEFT", u"RIGHT")) + 1.8 * k
    gx0, gx1 = x + lab_w, x + w
    nrow = max(1, P02_ET_ROWS)
    Lr = d["L"] / nrow
    sx = (gx1 - gx0) / Lr
    HB, WS, SW = P02_ET_HB * k, 1.5 * k, 4.0 * k         # each bank, each bank face, the stream (booklet mm)
    my = HB / P02_ET_LAND
    st = _pre[1] if _pre else _p02_strip(S, d, den=bk_std(1000.0 * k / my))   # M11 roofs read at the strip's scale
    #                                                                             across the banks (v59: _pre given)
    bm = d["bm"]
    cov_c = _p02_hue("water_cov", mix(CAT["water"][1], PAPER, 0.55))   # v61 (G6-6): the hue table (WAT r4)
    path_c = _p02_hue("path", mix(CAT["green"][1], INK, 0.35))          # MOV r3, as plan 01
    gnd_c = _p02_hue("et_ground", P02_GROUND)                           # CTX r5
    LX, LY, LC = d["line"]
    kp = site28_project(LX, LY, LC, [(b_[2], b_[3]) for b_ in BRIDGES_K])
    bch = d["cor"].get("bridges_ch", [])
    decks = [(bch[i_], bch[i_ + 1]) for i_ in range(0, len(bch) - 1, 2)]
    covs = list(d["cor"].get("covered_reaches", []))
    free = (0.0, 0.0, 0.0, 0.0, 0.0)                      # the longest open water, to name the stream
    yy -= 0.6 * k
    low = yy
    reach = P02_ET_REACH.get(nrow) or tuple(u"PART %d" % (j_ + 1) for j_ in range(nrow))
    i0_et, et_boxes = sb_mark(B), []                      # v59 closing (G-R4-1): the strips' own texts, their boxes
    for r in range(nrow):
        s0, s1 = r * Lr, (r + 1) * Lr

        def X(s_, s0=s0):
            return gx0 + (s_ - s0) * sx
        # v59 (round 4, P02.3): the free band between the rows, and each row's heading (its reach and chainage)
        if r > 0:
            yy -= (_gap or 0.0) * k
        rh_ = u"**{}** · {:,.0f}-{:,.0f} m".format(reach[r], s0, s1)
        site28_fit(B, rh_, x, yy - 2.3 * k, h7, w, INK, L)
        ovl.append(_p02_tb(rh_.replace(u"**", u""), x, yy - 2.3 * k, h7, w))
        yy -= 4.3 * k
        ya = yy - h65
        v = math.ceil(s0 / 250.0 - 1e-9) * 250.0
        while v <= s1 + 1e-6:                             # the chainage every 250 m, its unit on the row's last number
            t_ = u"{:,.0f}".format(v) + (u" m" if v + 250.0 > s1 + 1e-6 else u"")
            tx = min(max(X(v) - 0.5 * site28_tw(t_, h65), gx0), gx1 - site28_tw(t_, h65))
            B.text(t_, tx, ya, h65, INK2, L, font=FONT_TITLE)
            ovl.append(_p02_tb(t_, tx, ya, h65))
            with B.kind("annotations", u"chainage %d" % int(v)):
                B.line([(X(v), ya - 0.4 * k), (X(v), ya - 1.2 * k)], INK2, L, 21, bk_lw(0.15, k))
            v += 250.0
        yb0 = ya - 1.2 * k                                # left bank (land at the top), its face, the stream, the
        yLw = yb0 - HB                                    # right bank's face, the right bank (land at the bottom)
        yst = yLw - WS
        ysb = yst - SW
        yRw = ysb - WS
        ybot = yRw - HB
        et_boxes.append((gx0, ybot, gx1, yb0))
        band = {0: (yLw, yb0), 1: (ybot, yRw)}
        face = {0: (yst, yLw), 1: (yRw, ysb)}             # (water y, land y)

        def Yd(sd, b_):
            return yLw + b_ * my if sd == 0 else yRw - b_ * my
        for t_, sd in ((u"LEFT", 0), (u"RIGHT", 1)):
            B.text(t_, x, 0.5 * sum(band[sd]) - 0.5 * h65, h65, INK, L, font=FONT_TITLE, bold=True)
            ovl.append(_p02_tb(t_, x, 0.5 * sum(band[sd]) - 0.5 * h65, h65))
        for sd in (0, 1):
            lo, hi = band[sd]
            box = (gx0, lo, gx1, hi)
            with B.kind("ground"):
                B.fill([rect(gx0, lo, gx1, hi)], gnd_c, L, 20)
            for sd_, ring, sub in st["greens"]:           # green ground: parks, woods, grass
                if sd_ == sd and max(p[0] for p in ring) >= s0 and min(p[0] for p in ring) <= s1:
                    P = clip_rect_poly([(X(a_), Yd(sd, b_)) for a_, b_ in ring], box)
                    if len(P) >= 3:
                        with B.kind("ground"):
                            B.fill([P], _p02_hue("g_park", mix(GREEN_SUB.get(sub, GREEN_SUB["park"]), PAPER, 0.45)),
                                   L, 21)
            zw, zl = Yd(sd, 0.0), Yd(sd, P02_ET_ZONE)
            for i0, i1, t_ in site28_runs(st["types"][sd]):        # the edge zone in its type's language
                a_, b_ = max(i0 * bm, s0), min(i1 * bm, s1)
                if b_ > a_:
                    with B.kind(P02_ET_KIND.get(t_, "ground")):   # v61 (G6-9): each stretch its kind
                        _p02_zone(B, t_, X(a_), X(b_), zw, zl, k, L, 22)
            for sd_, pl in st["paths"]:                   # footpaths
                if sd_ != sd:
                    continue
                for run_ in clip_rect_line([(X(a_), Yd(sd, b_)) for a_, b_ in pl], box):
                    if len(run_) > 1:
                        with B.kind("paths"):
                            for d_ in dashes(list(run_), 0.5 * k, 0.35 * k):
                                B.line(d_, path_c, L, 23, bk_lw(0.12, k))
            # round 2 (PG1 p2 #6, U18): the survey's buildings as strict roof blocks. v58 (round 3, P02.2, G7):
            # beyond the edge zone only, touching blocks merged into one (_p02_blocks): no roof lies over another; a
            # lone building keeps its hipped roof reading, a merged block a simple roof hatch
            for sd_, ring_, nb_ in st["blocks"]:
                if sd_ != sd or max(p_[0] for p_ in ring_) < s0 or min(p_[0] for p_ in ring_) > s1:
                    continue
                P = clip_rect_poly([(X(a_), Yd(sd, b_)) for a_, b_ in ring_], box)
                if len(P) >= 3:
                    with B.kind("buildings"):
                        (_p02_roof_block if nb_ == 1 else _p02_block_roof)(B, P, k, L, 24)
            grid_, kept = {}, []                          # trees, the larger first, none hiding another
            for sd_, s_, b_, rr, lf, c0_ in sorted(st["crowns"], key=lambda c_: -c_[3]):
                if sd_ != sd or not s0 <= s_ < s1:
                    continue
                D = min(2.6, max(1.3, 0.9 + 0.26 * rr)) * k
                cx_ = X(s_)
                cy_ = min(max(Yd(sd, max(0.0, b_)), lo + 0.35 * D), hi - 0.35 * D)
                gk = (int(cx_ // (3.0 * k)), int(cy_ // (3.0 * k)))
                if any(math.hypot(qx - cx_, qy - cy_) < 0.42 * (qd + D) for gi in (-1, 0, 1) for gj in (-1, 0, 1)
                       for qx, qy, qd in grid_.get((gk[0] + gi, gk[1] + gj), ())):
                    continue
                grid_.setdefault(gk, []).append((cx_, cy_, D))
                kept.append((cx_, cy_, D, lf, int(s_), c0_))
            for j_, (cx_, cy_, D, lf, sd_seed, c0_) in enumerate(kept):   # v61 (G6-10): each tree its species
                sp = _p02_sp(S, c0_)
                with B.kind("trees", u"%s e%d.%d.%d" % (sp or "tree", r, sd, j_)):
                    _p02_put(B, _p02_crown(lf, cx_, cy_, D, k, sd_seed, sp=sp), L, 26, k)
            yw_, yl_ = face[sd]                           # the bank face
            with B.kind("ground"):
                B.fill([rect(gx0, min(yw_, yl_), gx1, max(yw_, yl_))], gnd_c, L, 20)
                for i0, i1, wv in site28_runs(st["walls"][sd]):
                    a_, b_ = max(i0 * bm, s0), min(i1 * bm, s1)
                    if b_ > a_:
                        _p02_wall(B, wv, X(a_), X(b_), yw_, yl_, k, L, 27)
        # the stream (M5 water_plan: surface, flow streaks deepening to the middle, bank edge), its covered reaches,
        # the bridges' decks
        with B.kind("water", u"stream %d" % (r + 1)):
            _p02_water(B, gx0, ysb, gx1, yst, k, L, 20, seed=r)
        for a_, b_ in covs:
            a_, b_ = max(a_, s0), min(b_, s1)
            if b_ > a_:
                cr_ = rect(X(a_), ysb, X(b_), yst)
                with B.kind("water"):
                    B.fill([cr_], cov_c, L, 21)
                    B.hatch([cr_], SS_COVER_C, L, 22, 0.8 * k, math.radians(45.0), bk_lw(0.12, k))
        for a_, b_ in decks:
            if b_ >= s0 and a_ <= s1:
                xm, hd = X(0.5 * (a_ + b_)), max(0.35 * k, 0.5 * (b_ - a_) * sx)
                with B.kind("roads"):
                    _p02_deck(B, xm - hd, yRw, xm + hd, yLw, k, L, 29)
        c_ = s0
        for a_, b_ in sorted([(max(a_, s0), min(b_, s1)) for a_, b_ in covs + decks if b_ > s0 and a_ < s1]) + \
                [(s1, s1)]:
            if X(a_) - X(c_) > free[0]:
                free = (X(a_) - X(c_), X(c_), X(a_), ysb, yst)
            c_ = max(c_, b_)
        # the bridges: a tick under the row, the real name beside it (bridge_name). v58 (round 3, G3, G16): placed by
        # lp_place (booklet mm, no leader); a name with no room beside its tick becomes the bridge's p.02 number
        # (stream order, as under plan 01) and is listed in the key under the strip; no K-code printed
        items, kk_ = [], []
        for (kk, nm_, bx, by), (s_, o_) in zip(BRIDGES_K, kp):
            if not s0 <= s_ < s1 or not 0.0 <= s_ <= d["L"] or abs(o_) > SITE28_K_NEAR or kk not in knum:
                continue
            px = X(s_)
            with B.kind("annotations", u"bridge tick %s" % kk):
                B.line([(px, ybot - 0.2 * k), (px, ybot - 1.0 * k)], INK, L, 30, bk_lw(0.3, k))
            t_ = bridge_name(kk)
            wd = site28_line_w(site28_one(t_, h7), h7) / k
            items.append(dict(x=px / k, y=(ybot - 1.0 * k) / k, w=wd + 0.8, h=1.5 * h7 / k, r=0.4, t=t_))
            kk_.append(kk)
        taken = [(x / k, (ybot - 0.2 * k) / k, (x + w) / k, (ya + h65) / k)]
        # v61 (G6-8, SON page2: "2" of "small crossing" touched "side inlet crossing"): 1.2 mm clear between two
        # bridge names / numbers (lp_place pad, was its 0.6 default)
        got = lp_place(items, obstacles=taken, bounds=(x / k, (ybot - 12.0 * k) / k, (x + w) / k, (ybot - 0.4 * k) / k),
                       sizes=(1.0,), pad=1.2) if items else []
        low = ybot - 1.2 * k
        for it, kk, g_ in zip(items, kk_, got):
            if not g_:
                continue
            bx = g_["box"]
            if g_.get("number"):                          # no room: the bridge's number on the spot, its name in the key
                t_ = u"**{}**".format(knum[kk])
                knm.append((knum[kk], it["t"]))
            else:
                t_ = it["t"]
            site28_text(B, t_, (bx[0] + 0.4) * k, bx[1] * k + 0.3 * h7, h7, INK, L)
            ovl.append(_p02_tb(t_.replace(u"**", u""), (bx[0] + 0.4) * k, bx[1] * k + 0.3 * h7, h7))
            low = min(low, bx[1] * k)
        yy = low - 2.4 * k
    # v61 (G6-8, SON page2: the strip label "built" sat on the UPSTREAM strip's drawing): the edge types are no longer
    # named on the strips (each was a word on a white plate over the drawing); the key under the strip names every
    # type with its drawn sample. The stream keeps its name on its own water (a label naming what it sits on).
    snm = place_name("stream")                            # v59 (round 4, G-R4-11): the names table's one spelling
    if free[0] > site28_tw(snm, h65) + 6.0 * k:
        sxm, sym = 0.5 * (free[1] + free[2]), 0.5 * (free[3] + free[4])
        wn_c = _p02_hue("water_line", mix(CAT["water"][1], INK, 0.55))   # revision 30 Oct: dark on the calm M5
        tw_s = site28_tw(snm, h65)                        # surface, on a plate of that surface (no streak, G3)
        with B.kind("labels", "stream name"):
            B.fill([rect(sxm - 1.2 * k - 0.5 * tw_s - 0.6 * k, sym - 0.75 * h65, sxm - 1.2 * k + 0.5 * tw_s + 4.0 * k,
                         sym + 0.75 * h65)], _p02_hue("water_cov", mix(CAT["water"][1], PAPER, 0.62)), L, 30)
            B.text(snm, sxm - 1.2 * k, sym, h65, wn_c, L, order=31, font=FONT_TITLE, italic=True, align="MC")
            ax0 = sxm - 1.2 * k + 0.5 * site28_tw(snm, h65) + 0.8 * k    # the way it flows
            B.line([(ax0, sym), (ax0 + 2.0 * k, sym)], wn_c, L, 31, bk_lw(0.2, k))
            B.fill([[(ax0 + 2.6 * k, sym), (ax0 + 1.8 * k, sym + 0.45 * k), (ax0 + 1.8 * k, sym - 0.45 * k)]], wn_c,
                   L, 31)
        ovl.append((sxm - 1.2 * k - 0.5 * tw_s, sym - 0.5 * h65, sxm - 1.2 * k + 0.5 * tw_s, sym + 0.5 * h65))
    for j_, eb_ in enumerate(et_boxes):                   # v59 closing (G-R4-1): each strip: its names may sit on
        sb_keep(B, eb_, u"p02 edge strip %d" % (j_ + 1), "strip", i0_et)   # it, no other text
    i0_etk = sb_mark(B)
    # the key: drawn samples of what is drawn (each the drawing's own texture), laid out by M2 Legend under the drawing
    tys = set(v_ for row_ in st["types"] for v_ in row_ if v_)
    wls = set(v_ for row_ in st["walls"] for v_ in row_ if v_ in (1, 2))
    lg = Legend((x / k, yy / k, (x + w) / k, top / k), side="below", gap=0.6, y_down=False, swatch=(6.0, 2.8),
                col_gap=3.0)
    for t_, nm_ in ((u"pedestrian", u"walkable paving"), (u"street", u"street"), (u"green", u"planted"),
                    (u"building", u"built: backs on the water"), (u"parking", u"parking"), (u"open", u"loose ground")):
        if t_ in tys:
            lg.add(nm_, "sample", code=("z", t_))
    for v_, nm_ in ((1, u"wall"), (2, u"embankment")):
        if v_ in wls:
            lg.add(nm_, "sample", code=("w", v_))
    for cd_, nm_ in ((("g", None), u"green ground"), (("b", None), u"a building"),
                     (("m", None), u"buildings that touch, as one block"), (("t", None), u"trees"),
                     (("p", None), u"footpaths"), (("s", None), u"the stream"), (("c", None), u"covered stream"),
                     (("k", None), u"bridge deck")):
        lg.add(nm_, "sample", code=cd_)
    for n_, nm_ in sorted(set(knm)):                      # v58 (round 3, G3): numbered bridges, in number order
        lg.add(nm_, "sample", code=("n", n_))
    lay = lg.layout(lambda s_, pt_, b_: site28_tw(s_, bk_hk(pt_, k), b_) / k, size_pt=7.0)
    with B.kind("legend"):                                # v61 (G6-9): the key's samples
        for row_ in lay["rows"]:
            kd, v_ = row_["code"]
            kx, y0_, x1_, y1_ = (c_ * k for c_ in row_["swatch"])
            if kd == "z":
                _p02_zone(B, v_, kx, x1_, y0_, y1_, k, L, 22)
            elif kd == "w":
                _p02_wall(B, v_, kx, x1_, y0_, y1_, k, L, 22)
            elif kd == "g":
                B.fill([rect(kx, y0_, x1_, y1_)], _p02_hue("g_park", mix(GREEN_SUB["park"], PAPER, 0.45)), L, 21)
            elif kd == "b":                                   # a building as the strip draws it (M11 roof reading)
                _p02_roof_block(B, rect(kx + 0.4 * k, y0_ + 0.3 * k, x1_ - 0.4 * k, y1_ - 0.3 * k), k, L, 21)
            elif kd == "m":                                   # v58 (round 3, P02.2): a merged block (a stepped outline)
                _p02_block_roof(B, [(kx + 0.4 * k, y0_ + 0.3 * k), (x1_ - 0.4 * k, y0_ + 0.3 * k),
                                    (x1_ - 0.4 * k, y1_ - 1.0 * k), (kx + 0.5 * (x1_ - kx), y1_ - 1.0 * k),
                                    (kx + 0.5 * (x1_ - kx), y1_ - 0.3 * k), (kx + 0.4 * k, y1_ - 0.3 * k)], k, L, 21)
            elif kd == "n":                                   # v58 (round 3, G3): a bridge's number as on the strip
                B.line([(kx + 0.6 * k, y0_), (kx + 0.6 * k, y1_)], INK, L, 30, bk_lw(0.3, k))
                site28_text(B, u"**{}**".format(v_), kx + 1.4 * k, y0_ + 0.3 * k, h7, INK, L)
            elif kd == "t":
                for j_, lf in enumerate((0, 2)):
                    _p02_put(B, _p02_crown(lf, kx + (1.5 + 3.0 * j_) * k, 0.5 * (y0_ + y1_), 2.4 * k, k, j_), L, 26, k)
            elif kd == "p":
                for d_ in dashes([(kx, 0.5 * (y0_ + y1_)), (x1_, 0.5 * (y0_ + y1_))], 0.5 * k, 0.35 * k):
                    B.line(d_, path_c, L, 23, bk_lw(0.12, k))
            elif kd == "s":
                _p02_water(B, kx, y0_, x1_, y1_, k, L, 21, seed=7)
            elif kd == "c":
                B.fill([rect(kx, y0_, x1_, y1_)], cov_c, L, 21)
                B.hatch([rect(kx, y0_, x1_, y1_)], SS_COVER_C, L, 22, 0.8 * k, math.radians(45.0), bk_lw(0.12, k))
            elif kd == "k":
                _p02_water(B, kx, y0_, x1_, y1_, k, L, 21, seed=3, bank=False)
                _p02_deck(B, kx + 2.2 * k, y0_, kx + 3.8 * k, y1_, k, L, 22)
            B.text(row_["label"], row_["text"][0] * k, row_["text"][1] * k, bk_hk(row_["size_pt"], k), INK, L,
                   font=FONT_TITLE)
            ovl.append(_p02_tb(row_["label"], row_["text"][0] * k, row_["text"][1] * k, bk_hk(row_["size_pt"], k)))
    low = lay["box"][1] * k - 1.0 * k
    sb_keep(B, tuple(c_ * k for c_ in lay["box"]), u"p02 edge key", "legend", i0_etk)   # v59 closing (G-R4-1)
    if not _measure:
        _p02_legend_log()                                 # v61 (G6-6): the edge key reads the hue table
    if _measure:                                          # v59 (round 4, P02.3): the first pass only measures
        return (top + 0.5 * k - low) / k
    crop_panel("edge_types", x, low, x + w, top + 0.5 * k, u"The stream edge · both banks, straightened, from above")
    sw_ = _p02_side_w()                                   # v58 (round 3, G2): the side column's width
    CROP_PANELS[-1]["bk_w"] = sw_                         # its width on the booklet page (p.02's side column) ...
    CROP_PANELS[-1]["grid"] = [0.0, sw_ - 0.5 * (sw_ - P02_GAP)]   # ... on the readings' two halves
    _p02_ovl_add("edge_types", (x, low, x + w, top + 0.5 * k), k, ovl)
    LOG.append("Stream edge diagram (drw_edge_types): {:,.0f} m of the bars' {:,.0f} m of bank lie within {:.0f} m of "
               "the stream's centreline and are drawn ({} bins of {:.0f} m a bank, {} rows).".format(
                   d["used"], d["tot"], SITE28_ET_NEAR, d["n"], d["bm"], nrow))
    return low - 1.0 * U


def _p03_pip(x, y, P):
    ins, j = False, len(P) - 1
    for i in range(len(P)):
        xi, yi, xj, yj = P[i][0], P[i][1], P[j][0], P[j][1]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi:
            ins = not ins
        j = i
    return ins


def _p03_segd(px, py, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = max(0.0, min(1.0, ((px - a[0]) * dx + (py - a[1]) * dy) / ((dx * dx + dy * dy) or 1e-12)))
    return math.hypot(px - a[0] - t * dx, py - a[1] - t * dy)


def _p03_figures(S, pg, V, R):
    """v51 (WO-T3a-2, 02 §3; v52 A1 pen figures; 1.75 m since 30 Oct, D9): people at true height (_p02_fig side view) on the p.03 axonometric, placed by
    what they do there: watching the water along the walkable bank stretches (the edge samples of type walkable, one
    every P03_FIG_EDGE m, facing the stream) and walking the footpaths (one every P03_FIG_PATH m, facing the way the
    path runs); only on open ground (no building footprint within 3 m) inside the model's extent R, far to near.
    Drawn on the page just before its chrome (over the buildings: open ground only, so none stands behind a roof).
    Returns the number drawn."""
    cells = {}
    for u in S.bld:                                       # footprints in 25 m cells (3 m margin) for the open test
        for P in u.get("parts") or []:
            xs_, ys_ = [p[0] for p in P], [p[1] for p in P]
            for i in range(int((min(xs_) - 3.0) // 25.0), int((max(xs_) + 3.0) // 25.0) + 1):
                for j in range(int((min(ys_) - 3.0) // 25.0), int((max(ys_) + 3.0) // 25.0) + 1):
                    cells.setdefault((i, j), []).append(P)

    def open_at(px, py):
        for P in cells.get((int(px // 25.0), int(py // 25.0)), ()):
            if _p03_pip(px, py, P) or min(_p03_segd(px, py, P[i], P[(i + 1) % len(P)]) for i in range(len(P))) < 3.0:
                return False
        return True
    d = site28_edge_bins(S)
    LX, LY = (d["line"][0], d["line"][1]) if d else ([], [])
    spots = []
    for ex, ey, t_, wl_ in getattr(S, "edge_samples", []):
        if t_ != "pedestrian" or not R.inside(ex, ey) or len(spots) >= P03_FIG_MAX:
            continue
        if any(math.hypot(ex - qx, ey - qy) < P03_FIG_EDGE for qx, qy, _p, _f in spots) or not open_at(ex, ey):
            continue
        fc = 1
        if LX:                                            # facing the stream (its nearest centreline vertex)
            j = min(range(len(LX)), key=lambda i: (LX[i] - ex) ** 2 + (LY[i] - ey) ** 2)
            fc = 1 if (LX[j] - ex) * V.st - (LY[j] - ey) * V.ct >= 0.0 else -1
        spots.append((ex, ey, "watch", fc))
    for p in S.paths:
        P = p.get("P") or []
        run = 0.5 * P03_FIG_PATH
        for a, b in zip(P[:-1], P[1:]):
            sl = math.hypot(b[0] - a[0], b[1] - a[1])
            while sl > 0.0 and run <= sl:
                px, py = a[0] + run / sl * (b[0] - a[0]), a[1] + run / sl * (b[1] - a[1])
                if R.inside(px, py) and len(spots) < P03_FIG_MAX and open_at(px, py):
                    fc = 1 if (b[0] - a[0]) * V.st - (b[1] - a[1]) * V.ct >= 0.0 else -1
                    spots.append((px, py, "walk", fc))
                run += P03_FIG_PATH
            run -= sl
    zg = V.zg
    g0, g1 = V.st, -V.ct                                  # the ground direction across the page: figures face us
    col = crop_hex(FIG_INK)
    for px, py, pose, fc in sorted(spots, key=lambda s_: -V.depth(s_[0], s_[1])):
        z0 = zg(px, py) if zg is not None else 0.0
        for sh in _p02_fig(pose, 0.0, 0.0, 1.0, fc, pick=int(abs(px) + abs(py))):   # metres, feet at the origin
            pts = []
            for fx, fy in sh[1]:
                u_, v_ = V.uv(px + fx * g0, py + fx * g1, z0 + fy)
                pts.append((V.ox + V.k * u_, V.oy + V.k * v_))
            pg.poly([pts], fill=col, stroke=None, layer="figures")
    LOG.append(u"p.03 axonometric: {} figures at true height (1.75 m = {:.2f} mm on the sheet): {} watching the water "
               u"on walkable banks, {} walking footpaths.".format(len(spots), 1.75 * V.k * V.cp,
                                                                  sum(1 for s_ in spots if s_[2] == "watch"),
                                                                  sum(1 for s_ in spots if s_[2] == "walk")))
    return len(spots)


_P03 = {}                 # v58 (round 3, P03.1): the axonometric's callouts taken from the engine (calls), the hook flag
P03_MK_PT = 7.0           # v59 (round 4, PALL.2, G-R4-7): the numbers' size on the p.03 sheet (printed 1:1)
P03_MK_R = 1.9            # v59: mm, the least radius of a p.03 marker (so 1-9 and 10-12 read as one set)
P03_MK_RINGS = (1.0, 2.0, 3.0, 4.0, 5.0)    # v59: mm, how far a marker may leave its spot to find free room
P03_T_MIN = 2.15          # v59 (round 4, G-R4-1): mm, the smallest em on the p.03 sheet (6.1 pt; DIAG_SRC TP_MIN_EM)


def _p03_marker(pg, x, y, s, colour, name):
    """v59 (round 4, PALL.2, G-R4-7): ONE marker on the p.03 sheet (the engine's Page, page mm y up): common/marker.py
    mk_marker; its disc drawn and registered as a keep of the sheet's TextPage under name, its glyph registered
    allowed on that disc only. Returns the marker's box."""
    shapes, box, r = mk_marker(x, y, s, colour, size_pt=P03_MK_PT, r_min=P03_MK_R)
    for sh in shapes:
        if sh[0] == "poly":
            pg.poly([sh[1]], fill=sh[2], stroke=sh[3], lw=sh[4] or 0.1, layer="callouts")
            pg.keep(sh[1], "marker", name)
        elif sh[0] == "text":
            pg.text(sh[1], sh[2], sh[3], sh[4], sh[5], bold=True, align="L", layer="callouts", name=name,
                    allow=(name,))
    return box


def _p03_title(t):
    """v58 (round 3, G16): a callout title without its source mark; a bridge ("K4 <name>") by its one spelling
    (bridge_name), never its code"""
    import re as _re
    t = _re.sub(r"\s*\[\d+\]", u"", t or u"")
    m = _re.match(r"^(K\d)\b\s*", t)
    if m:
        try:
            return bridge_name(m.group(1))
        except Exception:
            return t[m.end():] or t
    # v59 (round 4, G-R4-11): a translated, variant or surveyed landmark name -> the names table (closing: the one
    # survey-name map SB_LANDMARK_ALIAS of parts/05_build_terrain.py, shared with the p04-05 cut-building tags)
    return sb_landmark(t)


def _p03_marks(pg, V, calls, DG, BP):
    """v58 (round 3, P03.1, G3): the axonometric's callouts without leaders (the engine's place_callouts draws a leader
    and a circled letter per callout; data/DIAG_SRC.py is not this page's file, so _p03_axo_loop hands the engine no
    calls and they are drawn here, from the chrome hook, after the model and the figures): the engine's choice (prio,
    one per title and place, at most MAX_CALLOUTS), numbered in reading order (lp_reading_order: rows from the top
    of the page, left to right), each number in a disc in its kind's deep tone ON its spot (moved at most 2 mm off it
    where another disc is there), and the key "n  title · fact" in the same order in the free sky above the model
    (the highest free room of the drawing box, right first: no line to any number). Returns (label boxes, drawing
    boxes, bounds) for the overlap test, page mm y up."""
    CORE = BP.CORE
    tw_ = DG.get("text_w") or (lambda s_, z_, b_=False: 0.6 * z_ * len(s_))
    cap = DG.get("CAP", 0.716)
    box = DG["BOX"]
    seen, keep = set(), []
    for c in sorted(calls, key=lambda c_: -c_.get("prio", 0.0)):
        if len(keep) >= DG.get("MAX_CALLOUTS", 12):
            break
        key = (c["title"], round(c["x"]), round(c["y"]))
        if key in seen:
            continue
        seen.add(key)
        ax, ay = V.P(c["x"], c["y"], c.get("z", 0.0))
        keep.append((c, ax, ay))
    if not keep:
        return [], [], box
    ro = lp_reading_order([(ax, ay) for c, ax, ay in keep], y_down=False, row_mm=12.0)
    # v59 (round 4, PALL.2, G-R4-7, G-R4-1): each number in the ONE marker (mk_marker: centred on its ink box, sized
    # to it, in the deep tone of the kind it names), on its spot or the nearest free place within P03_MK_RINGS mm
    # (clear of every disc and text registered on the sheet: the ground words), its disc a keep of the sheet's
    # TextPage (only its own glyph may sit on it); a callout with no free place is left out and logged (G-R4-2:
    # the lowest priorities go first, they are numbered after the kept ones)
    RD = 2.0 * (P03_MK_R + 0.15)                          # the key column's disc width (mm)
    labs, dboxes, n = [], [], 0
    for i in ro:
        c, ax, ay = keep[i]
        deep = BP.tones_of(c["color"])["outline"] if c.get("color") and c["color"] != "141414" else CORE["ink"]
        n_ = n + 1
        sh0, b0, r0 = mk_marker(ax, ay, str(n_), deep, size_pt=P03_MK_PT, r_min=P03_MK_R)
        spot = None
        for dd in (0.0,) + P03_MK_RINGS:
            for a_ in (range(8) if dd else (0,)):
                qx = ax + dd * math.cos(math.radians(45.0 * a_ + 90.0))
                qy = ay + dd * math.sin(math.radians(45.0 * a_ + 90.0))
                hb = (b0[2] - b0[0]) / 2.0
                bq = (qx - hb, qy - hb, qx + hb, qy + hb)
                if all(not _p02_hit((bq[0] - 0.6, bq[1] - 0.6, bq[2] + 0.6, bq[3] + 0.6), d_) for d_ in dboxes) and \
                        pg.box_free(bq):
                    spot = (qx, qy)
                    break
            if spot:
                break
        if spot is None:                                  # v62 (L2, Aras 4 Nov 19:17): never left out: set on its own
            spot = (ax, ay)                               # spot; its number and key row go to the booklet's check
            LOG.append(u"p.03 axonometric: callout {!r} set on its spot (no free place within {:.0f} mm)".format(
                _p03_title(c.get("title", u"")), P03_MK_RINGS[-1]))
        n = n_
        _p03_marker(pg, spot[0], spot[1], str(n), deep, u"p03 mark %d" % n)
        hb = (b0[2] - b0[0]) / 2.0
        dboxes.append((spot[0] - hb, spot[1] - hb, spot[0] + hb, spot[1] + hb))
        labs.append((n, deep, _p03_title(c.get("title", u"")), c.get("fact", u"")))
    if not labs:
        return dboxes, [], box
    # the key: n in the same marker, the title bold, its fact after it; rows 4.6 mm. v59: the fact at 6 pt
    T1, T2, ROW = 2.3, P03_T_MIN, 4.6
    hd = u"NUMBERED ON THE DRAWING"
    rows_w = [RD + 1.6 + tw_(t_, T1, True) + (1.2 + tw_(u"· " + f_, T2) if f_ else 0.0) for n_, d_, t_, f_ in labs]
    Wk = max([tw_(hd, T1, True)] + rows_w)
    Hk = T1 + 2.0 + ROW * len(labs)
    # the sky above the model: per 4 mm of page width the highest thing drawn between the rules (not the sheet's
    # title, legend, north arrow or scale bars); the key goes where its whole width is free, nearest the box's top right
    step = 4.0
    nb = int((box[2] - box[0]) / step) + 1
    top = [box[1]] * nb

    def put(x_, y_):
        if box[0] <= x_ <= box[2] and y_ <= box[3] + 4.0:
            j_ = int((x_ - box[0]) / step)
            if y_ > top[j_]:
                top[j_] = y_
    for it in pg.items:
        if it[0] == "poly" and it[6] not in ("sheet", "legend", "north", "scale"):
            for R_ in it[1]:
                for p_ in R_:
                    put(p_[0], p_[1])
        elif it[0] == "line" and it[5] not in ("sheet", "legend", "north", "scale"):
            for p_ in it[1]:
                put(p_[0], p_[1])
        elif it[0] == "circle" and it[7] not in ("sheet", "legend", "north", "scale"):
            put(it[1] - it[3], it[2] + it[3])
            put(it[1] + it[3], it[2] + it[3])
        elif it[0] == "text" and it[8] not in ("sheet", "legend", "north", "scale"):
            put(it[2], it[3] + it[4])
    y_hi = box[3] - 1.0                                   # the key's top: under the upper rule
    best = None
    jn = int(math.ceil(Wk / step)) + 1
    for j0 in range(nb - jn, -1, -1):                     # right first
        x0 = box[0] + j0 * step
        if x0 + Wk > box[2]:
            continue
        # v59 (round 4, PALL.2, G-R4-1): the key's whole box must also be clear of every text and marker on the sheet
        if not pg.box_free((x0, y_hi - Hk, x0 + Wk, y_hi + 0.3)):
            continue
        clear = (y_hi - Hk) - (max(top[j0:j0 + jn]) + 3.0)
        if clear >= 0.0:                                  # the first free place from the right
            best = (clear, x0, j0)
            break
        if best is None or clear > best[0]:               # else the least overlap (logged)
            best = (clear, x0, j0)
    clear, kx, j0 = best or ((y_hi - Hk) - (max(top) + 3.0), box[0], 0)
    if best is None:
        LOG.append(u"FLAG p.03 axonometric: the numbered key finds no place clear of the sheet's texts")
    ky = y_hi - T1
    pg.text(hd, kx, ky, T1, CORE["ink"], bold=True, layer="callouts")
    lab_boxes = dboxes + [(kx, ky - 0.3 * T1, kx + tw_(hd, T1, True), ky + T1)]
    for j_, (n_, d_, t_, f_) in enumerate(labs):
        yc = ky - 2.0 - ROW * j_ - ROW / 2.0
        _p03_marker(pg, kx + RD / 2.0, yc, str(n_), d_, u"p03 key %d" % n_)    # v59 (G-R4-7): the same marker
        tx = kx + RD + 1.6
        pg.tgroup()                                       # v59: the title and its fact are one row (one group)
        pg.text(t_, tx, yc - T1 * cap / 2.0, T1, CORE["ink"], bold=True, layer="callouts")
        x1_ = tx + tw_(t_, T1, True)
        if f_:
            pg.text(u"· " + f_, x1_ + 1.2, yc - T1 * cap / 2.0, T2, CORE["ink2"], layer="callouts")
            x1_ += 1.2 + tw_(u"· " + f_, T2)
        pg.tgroup(False)
        lab_boxes.append((kx, yc - RD / 2.0, x1_, yc + RD / 2.0))
    # what the key may not touch: the drawing under its columns (none where it found free sky)
    draw_boxes = [(box[0] + j_ * step, box[1], box[0] + (j_ + 1) * step, top[j_] + 3.0) for j_ in range(j0, j0 + jn)
                  if j_ < nb and top[j_] + 3.0 > y_hi - Hk]
    LOG.append(u"p.03 axonometric: {} places numbered on the spot in reading order (no leaders), key of {} rows at "
               u"x {:.0f} mm{}.".format(len(labs), len(labs), kx, u"" if clear >= 0.0 else
                                        u" (no free sky wide enough: it overlaps the drawing by {:.0f} mm)".format(-clear)))
    return lab_boxes, draw_boxes, (box[0], box[1], box[2], box[3] + 4.0)


def export_axonometrics(S):
    """v33 (Aras Q8; Step 4, 07:05-07:09): S1 as a parallel axonometric, one A3 vector PDF beside the board's PDFs
    (S2 has none: its walk table gives each walk's climb). Returns the paths written."""
    import datetime as _dt
    DG, ctx = diagram_ctx(S)
    stamp = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    out = []
    del CROP_DIRECT[:]                                    # v60: no sheet PDF; the page items go to the booklet items
    # v51 (WO-T3a-2, 02 §3): people on the axonometric. The engine (data/DIAG_SRC.py) is not this page's file: its
    # compose() calls chrome() last with the drawing's view, so the figures go in there (_p03_figures), and the
    # engine's own chrome is put back after the loop
    chrome0 = DG.get("chrome")

    def chrome_figs(pg_, ctx_, spec_, ext_, V_, stamp_):
        try:
            _p03_figures(S, pg_, V_, ext_["rect"])
        except Exception:
            LOG.append("WARNING: the axonometric's figures failed (drawn without them):\n" + traceback.format_exc())
        try:                                              # v58 (round 3, P03.1, G3): numbers on the spot + key
            lb_, db_, bd_ = _p03_marks(pg_, V_, _P03.get("calls") or [], DG, ctx_.BP)
        except Exception:
            LOG.append("WARNING: the axonometric's numbered places failed (drawn without them):\n" +
                       traceback.format_exc())
        return chrome0(pg_, ctx_, spec_, ext_, V_, stamp_)
    _P03.clear()
    if chrome0 is not None:
        DG["chrome"] = chrome_figs
        _P03["hook"] = True                               # v58: the calls are drawn by the hook, not the engine
    try:
        out = _p03_axo_loop(S, DG, ctx, stamp, out)
    finally:
        if chrome0 is not None:
            DG["chrome"] = chrome0
        _P03.clear()
    LOG.extend(u"Axonometric engine: " + m for m in DG["LOG"])
    return out


def _p03_label(t):
    """revision 30 Oct (G1, G12): a legend name of the axonometric without its internal source words (where the data
    comes from goes to the Sources page): "(survey)", "(OSM)", the canopy map's method"""
    import re as _re
    t = _re.sub(r"\s*\((survey|OSM)\)", u"", t)
    t = _re.sub(r"^Tree crowns 3 m and taller, radius and height from the Meta/WRI canopy height map", u"Tree crowns", t)
    t = _re.sub(r"^Surveyed tree symbols, drawn at a fixed size: no size in the survey", u"Tree symbols", t)
    return t.replace(u"; leaf type not in the environment file", u"")


def _p03_bbox(pg, DG, y0, y1):
    """revision 30 Oct (G2: no leftover space): the extent (x0, y0, x1, y1, page mm, y up) of what the axonometric
    draws between the sheet's rules y0-y1 (model, words, callouts; not the sheet's title, legend, scale bars or north
    arrow, which lie outside the rules); None when nothing is there"""
    xs, ys = [], []
    tw = DG.get("text_w")
    for it in pg.items:
        if it[0] == "poly" and it[6] not in ("sheet", "legend", "north", "scale"):
            for R in it[1]:
                xs += [p_[0] for p_ in R]
                ys += [p_[1] for p_ in R]
        elif it[0] == "line" and it[5] not in ("sheet", "legend", "north", "scale"):
            xs += [p_[0] for p_ in it[1]]
            ys += [p_[1] for p_ in it[1]]
        elif it[0] == "circle" and it[7] not in ("sheet", "legend", "north", "scale"):
            xs += [it[1] - it[3], it[1] + it[3]]
            ys += [it[2] - it[3], it[2] + it[3]]
        elif it[0] == "text" and it[8] not in ("sheet", "legend", "north", "scale"):
            s_, x_, y_, sz = it[1], it[2], it[3], it[4]
            w_ = tw(s_, sz, it[6]) if tw is not None else 0.6 * sz * len(s_)
            x0_ = x_ - w_ if it[7] == "R" else (x_ - 0.5 * w_ if it[7] == "C" else x_)
            xs += [x0_, x0_ + w_]
            ys += [y_ - 0.3 * sz, y_ + sz]
    pts = [(a_, b_) for a_, b_ in zip(xs, ys) if y0 <= b_ <= y1]
    if not pts:
        return None
    return (min(p_[0] for p_ in pts), min(p_[1] for p_ in pts), max(p_[0] for p_ in pts), max(p_[1] for p_ in pts))


def _p03_axo_loop(S, DG, ctx, stamp, out):
    """export_axonometrics' loop (v33-v40; v51 moved here so the figures' hook wraps it). Revision 30 Oct (PG1 p3):
    the callout titles without source marks, the legend names without source words (_p03_label), the booklet crop
    tight round what is drawn between the rules (_p03_bbox, 2 mm margin: no empty band above the model)"""
    import re as _re
    if "SB_TREE_N" in globals():                          # v61 (G6-10): this run's p.03 species counts
        SB_TREE_N.pop("p03", None)
    try:                                                  # v61 (G6-10): the trees' legend swatch (P-3: GRN r1)
        tree_dot = hue("GRN", 1)                                                             # noqa: F821
    except Exception:
        tree_dot = None
    for did, fn in (("S1", "Selinus_01_what_is_there_axonometric.pdf"),):
        t0 = time.time()
        ext = ctx.extents[0]
        try:
            spec = DG["SPECS"][did](ctx, ext)
            for c_ in spec.get("calls", []):
                c_["title"] = _p03_title(c_.get("title", u""))     # v58 (G16): no [n], bridges by bridge_name
            if _P03.get("hook"):                          # v58 (round 3, P03.1, G3): the engine's callouts make
                _P03["calls"] = list(spec.get("calls", []))   # leaders: it gets none; _p03_marks numbers them on
                spec["calls"] = []                        # the spot (chrome hook) with the key in reading order
            leg0 = spec["legend"]
            spec["legend"] = lambda leg0=leg0: [(k_, c_, _p03_label(t_)) for k_, c_, t_ in
                                                (leg0() if callable(leg0) else leg0)]
            pg, st = DG["compose"](ctx, spec, ext, stamp)
            # v60 (round 5, G-R5-12): no sheet PDF and no text check here: the page's items (pg.items, mm, y up)
            # go to the booklet items (16d_items.py _six_axo); the booklet sets and checks the texts
            out.append((fn[:-4] + " items", time.time() - t0))
            bx, ph = DG["BOX"], DG["PAGE_H"]                 # v40: the booklet crop: the page between the rules (the
            bx = (0.0, bx[1], DG["PAGE_W"], bx[3])            # callouts may sit beyond the drawing box, left and right)
            rm = (bx[0], ph - bx[3] - 4.0, bx[2], ph - bx[1] + 4.0)    # y down
            bb = _p03_bbox(pg, DG, bx[1] - 4.0, bx[3] + 4.0)
            if bb is not None:                                # tight round the model and its callouts (y down)
                rm = (max(rm[0], bb[0] - 2.0), max(rm[1], ph - bb[3] - 2.0), min(rm[2], bb[2] + 2.0),
                      min(rm[3], ph - bb[1] + 2.0))
            leg = [(("dot", tree_dot or DG["TREE_STYLES"].get(c_, DG["TREE_STYLES"]["tree"])["mid"]) if k_ == "tree"
                    else (k_, c_)) + (t_,) for k_, c_, t_ in spec["legend"]() if c_ is not None]
            try:                                          # v61 (G6-6): the legend reads the hue table (S1_HUE)
                LOG.append(hue_log("p03"))                                                   # noqa: F821
            except Exception:
                LOG.append(u"legend p03 hues=table (FLAG: common/hues.py hue_log not in this build)")
            if "sb_tree_log" in globals():                # v61 (G6-10): the axonometric's trees, once
                LOG.append(sb_tree_log("p03"))
                LOG.append(u"FLAG p03 trees: the axonometric's trees export on layer 'trees' (one element each); "
                           u"their species is not in the group names (16d_items _six_axo keys groups on the layer)")
            CROP_DIRECT.append(("axo_what_is_there", fn, rm,
                                u"What is there · heights, heritage, water, green", None, crop_legend(leg), [],
                                pg, ph))                  # v60: + the page and its height (16d_items)
        except Exception:
            LOG.append("WARNING: the {} axonometric failed:\n{}".format(did, traceback.format_exc()))
    return out


def draw_landcover(S, B, V, L, order=2):
    """v31: the land-cover classes, each one fill (even-odd over all its rings), order 2 after the paper. v61 (G6-6):
    in the hue table's colours (_p02_hue "lc_<class>"; only p.02 draws it)."""
    leg = []
    for k, lab, col in LC_CLASSES:
        col = _p02_hue("lc_" + k, col)
        rings = getattr(S, "lc", {}).get(k)
        if rings:
            for i in range(0, len(rings), 400):
                B.fill(V.Ps(rings[i:i + 400]), col, L, order)
            leg.append(("box", col, lab))
    return leg
