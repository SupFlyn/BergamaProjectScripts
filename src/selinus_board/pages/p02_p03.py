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
def draw_landuse_map(S, B, V, bcol=None, den=None, kb=10.0):
    """bcol (v33): the colour of each building (default: its land-use colour). Revision 30 Oct (G7, M11): the buildings
    through _p02_bld_plan (outline per block + roof reading at 1:den; kb = board units per booklet mm), no piece
    outlines."""
    L = "LU_BOARD::Map"
    s = V.s
    U = S.U
    B.fill([V.P(S.F.P)], PAPER, L + "::paper", 2)
    draw_landcover(S, B, V, L + "::landcover", 3)       # v31: under the surveyed / OSM ground (4)
    for z in S.zones:
        if z["kind"] == "green":
            col = GREEN_SUB.get(z["sub"], CAT["green"][1])
        elif z["kind"] == "transport":
            col = mix(CAT["transport"][1], PAPER, 0.3)
        else:
            col = CAT[z["kind"]][1]
        B.fill(V.Ps(z["Ps"] + z["Hs"]), col, L + "::" + z["kind"], 4)
        if z["kind"] == "vacant" and TEXTURE:
            for ln in hatch_lines(z["Ps"], z["Hs"], z["bb"], 5.0, math.radians(45)):
                B.line(V.P(ln), mix(INK, PAPER, 0.55), L + "::texture", 5, 0.06)
        if z["kind"] == "agri" and z["sub"] == "field" and TEXTURE:
            ang = (_zlib_crc(repr([round(v_, 2) for v_ in z["bb"]]).encode("utf-8")) % 180) * math.pi / 180.0
            for ln in hatch_lines(z["Ps"], z["Hs"], z["bb"], 7.0, ang):
                B.line(V.P(ln), mix(CAT["agri"][1], INK, 0.22), L + "::texture", 5, 0.04)
    for w in S.water:
        B.fill(V.Ps([w["P"]] + w.get("H", [])), CAT["water"][1], L + "::water", 6)
    for q in getattr(S, "decks", []):
        B.fill([V.P(q)], ROADC, L + "::streets", 7)
    for P in getattr(S, "covered", []):              # the covered course: a hidden line over the streets and roofs
        for d in dashes(V.P(P), 0.35 * U, 0.25 * U):
            B.line(d, BLUE_D, L + "::water", 19, 0.12)
    for P in S.water_outline:                         # the river edge: one continuous line per stretch (under decks)
        B.line(V.P(P), BLUE_D, L + "::water", 6, 0.13)
    for P in river_free_banks(S):                     # other surveyed streams and ditches, thinner
        B.line(V.P(P), BLUE_D, L + "::water", 7, 0.07)
    for P in S.pools:
        B.line(V.P(P), BLUE_D, L + "::water", 7, 0.08)
    road_lines(S, B, V, L + "::streets", 8, casing=ROAD_EDGE, surface=ROADC, min_w=0.04, fill=ROAD_FILL)
    for p in S.paths:                                 # paths whose width the survey does not show: a thin line
        if not p.get("w"):
            B.line(V.P(p["P"]), ROADC, L + "::streets", 9, 0.04)
    if TEXTURE:
        for x, y, r, kind in S.trees:
            bx, by = V.p(x, y)
            B.fill([circle_pts(bx + 0.35 * r * s, by - 0.35 * r * s, r * s, 14)], TREE_SHADOW, L + "::trees", 10)
            B.fill([circle_pts(bx, by, r * s, 14)], TREE_COLS.get(kind, TREE_COLS["tree"]), L + "::trees", 11)
            if kind == "pine":
                B.fill([circle_pts(bx - 0.25 * r * s, by + 0.25 * r * s, 0.45 * r * s, 10)],
                       mix(TREE_COLS["pine"], PAPER, 0.35), L + "::trees", 12)
        sh = mix(INK, PAPER, 0.6)
        for u in S.bld:
            off = min(3.0, 0.11 * u["h"]) * s
            B.fill([[(x + off, y - off) for x, y in V.P(P)] for P in u["parts"] + (u.get("holes") or [])], sh,
                   L + "::texture", 13)
    _p02_bld_plan(S, B, V, L + "::buildings", 14, den or crop_scale(V.s) or 1000.0, kb, bcol=bcol)
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
            B.line(d, mix(CAT["green"][1], INK, 0.3), L + "::ground", 16, 0.08)
    for P in S.walls:
        B.line(V.P(P), INK, L + "::walls", 17, 0.16)
    for P in S.bridges:
        B.line(V.P(P), INK, L + "::walls", 18, 0.24)


def site_crowns(S, F2):
    """Canopy-map crowns (modelled, Meta/WRI 1 m canopy height map) inside F2: [(x, y, r, h, leaf)]."""
    rows = seam_pack().get("crowns", {}).get("rows", [])
    return [(r[0], r[1], r[2], r[3], r[4]) for r in rows if F2.inside(r[0], r[1])]


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


def fabric_col(u):
    """v40: a building on plan 01 by its fabric type (the fabric map's rule: sheds and annexes paler)."""
    col = FABRIC_PLAN[u.get("fabric", "regular")]
    return mix(col, PAPER, 0.45) if u["annex"] else col


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
    # v51 (WO-T3a-2, p.02 flipped): what the plan shows is no longer a line over the map: it opens plan 01's own key
    # panel (draw_plan01_key, crop drw_plan01_key) at the top of the page's side column; the map starts under the title
    _P02.clear()
    # revision 30 Oct (G4): one line; the page's own intro (the booklet PLAN, bold key words) says the finding
    _P02["text"] = (u"The survey area today: **buildings** by urban fabric, **ground and green**, the **Selinos stream** "
                    u"with its edges and bridges K1-K6, and where stream and town **clash**.")
    ymap = y - 0.8 * U
    V, mw, mh = view_fit(F2, x, ymap, w, 10.0 * w)
    s = V.s
    # quiet context: survey line work around the frame, pale
    B.fill([V.P(F2.P)], mix(PAPER, (255, 255, 255), 0.55), L, 1)
    ctx = getattr(S, "ctx_lines", None) or {}
    for key, col, wd in (("water", mix(BLUE_D, PAPER, 0.5), 0.06), ("road", mix(INK2, PAPER, 0.62), 0.04),
                         ("bld", mix(INK2, PAPER, 0.45), 0.04)):
        for a, b in ctx.get(key, []):
            B.line([V.p(*a), V.p(*b)], col, L, 2, wd)
    # the site: land use, land cover, ground, streets, trees, buildings (homes by fabric), walls, bridges
    # v40: buildings by urban fabric type; revision 30 Oct (G7, M11): outline per block + roof, no piece lines
    draw_landuse_map(S, B, V, bcol=fabric_col, den=den_bk, kb=kb)
    # canopy-map crowns (modelled), under the surveyed tree symbols
    crowns = [c for c in site_crowns(S, F) if F.inside(c[0], c[1])]
    for leaf in (0, 1, 2):
        pts = [circle_pts(V.p(cx, cy)[0], V.p(cx, cy)[1], max(0.06 * U, r * s), 10) for cx, cy, r, h, lf in crowns
               if lf == leaf]
        for k in range(0, len(pts), 400):
            B.fill(pts[k:k + 400], mix(LEAF_COL[leaf], PAPER, 0.25), L, 10)
    # footpaths (the open-space network's links)
    path_c = mix(CAT["green"][1], INK, 0.35)
    for p in S.paths:
        for d in dashes(V.P(p["P"]), 0.35 * U, 0.25 * U):
            B.line(d, path_c, L, 19, 0.16)
    # dense fabric (intensity): the outline of the densest floor-area class
    dens = dense_outline(S)
    dc = mix(INTENSITY[3], INK, 0.1)
    for a, b in dens:
        B.line([V.p(*a), V.p(*b)], dc, L, 23, 0.3)
    # stream thresholds, thinner, along the banks
    for typ, pts in getattr(S, "edge_runs", []):
        B.line(V.P(pts), EDGE[typ][1], L, 24, THRESH_W)
    for pts in getattr(S, "wall_runs", []):
        for d in dashes(V.P(pts), 0.16 * U, 0.14 * U):
            B.line(d, PAPER, L, 25, THRESH_W * 0.4)
    # frame, river name, section marks (shared with the section drawings)
    draw_map_annotations(S, B, V, U, rh=bk_hk(8.0, kb))  # v45: no cut lines; the stream's name 8 pt
    B.line(V.P(F.P + [F.P[0]]), INK, L, 26, 0.25)
    if RF is not None:                                    # v36: the analysis range (site_alan) on the whole-file map
        B.line(V.P(RF.P + [RF.P[0]]), INK, L, 26, 0.12)
    draw_r28_study(getattr(S, "site", S), B, V, kb, L, order=27)    # v50 (MIRAQUA 28 Oct, G8): the study area
    # bridges and conflicts (v40, Aras 25 Oct 21:41: drawn marks with plain short labels, no boxes, no sentences).
    # v51 (WO-T3a-2): the photo viewpoints 1-8 are gone from this map (the page has no photos; p.06 keeps them)
    cs = list(CONFLICTS_C)
    c5 = c5_point(S)
    if c5:
        cs.append(("C5", c5[0], c5[1], C5_TEXT))
    # v45: marks and names sized for the booklet page (K names 9 pt), each name placed clear of every mark and name
    # (place_labels: on a thin leader where it must move away)
    hk, hs = bk_hk(9.0, kb), bk_hk(7.5, kb)
    taken, labs = [], []
    for k, nm, bx, by in BRIDGES_K:                       # a tick across the stream
        if F.inside(bx, by):
            px, py = V.p(bx, by)
            n = stream_normal(S, bx, by) or (0.0, 1.0)
            a_ = V.p(bx + n[0], by + n[1])
            ln = math.hypot(a_[0] - px, a_[1] - py) or 1.0
            e = ((a_[0] - px) / ln * 1.6 * kb, (a_[1] - py) / ln * 1.6 * kb)
            B.line([(px - e[0], py - e[1]), (px + e[0], py + e[1])], INK, L, 62, bk_lw(0.35, kb))
            taken.append((px - 1.6 * kb, py - 1.6 * kb, px + 1.6 * kb, py + 1.6 * kb))
            labs.append(([k], px, py, hk, INK))
    # v51 (WO-T3a-2, "C markers legible at first glance"): each conflict is a disc P02_C_R mm wide in the accent with a
    # white rim, its name inside in white 7 pt bold, so it reads over any ground colour; where a bridge mark or another
    # disc sits on the point, the disc moves out on a short leader from a small dot at the exact place
    rc, hcn = P02_C_R * kb, bk_hk(7.0, kb)
    for k, cx, cy, t in sorted(cs):
        if not F.inside(cx, cy):
            continue
        px, py = V.p(cx, cy)
        spot = None
        for dd in (0.0, 2.7 * rc, 3.8 * rc):
            for a_ in (range(8) if dd else (0,)):
                an_ = math.radians(90.0 + 45.0 * a_)
                qx, qy = px + dd * math.cos(an_), py + dd * math.sin(an_)
                b_ = (qx - 1.2 * rc, qy - 1.2 * rc, qx + 1.2 * rc, qy + 1.2 * rc)
                if not (ymap - mh <= b_[1] and b_[3] <= ymap and V.X0 <= b_[0] and b_[2] <= V.X0 + mw) and dd:
                    continue
                if not any(_p02_hit(b_, t_) for t_ in taken):
                    spot = (qx, qy, b_)
                    break
            if spot:
                break
        qx, qy, b_ = spot or (px, py, (px - 1.2 * rc, py - 1.2 * rc, px + 1.2 * rc, py + 1.2 * rc))
        taken.append(b_)
        if (qx, qy) != (px, py):
            dl_ = math.hypot(qx - px, qy - py) or 1.0
            B.fill([circle_pts(px, py, 0.5 * kb, 12)], MARK_C, L, 63)
            B.line([(px, py), (qx - (qx - px) / dl_ * rc, qy - (qy - py) / dl_ * rc)], MARK_C, L, 63, bk_lw(0.3, kb))
        B.fill([circle_pts(qx, qy, rc + 0.4 * kb, 24)], WHITE, L, 63)
        B.fill([circle_pts(qx, qy, rc, 24)], MARK_C, L, 64)
        B.text(k, qx, qy, hcn, WHITE, L, order=65, font=FONT_TITLE, bold=True, align="MC")
    mb = ymap - mh
    pkey = place_labels(B, labs, taken, L, bounds=(V.X0, mb, V.X0 + mw, ymap), order=65)
    # v45: scale bar and north arrow under the map, never on it; numbers 7 pt under the bar
    sbl = nice_floor(F2.w / 8.0)
    mb_crop = min(draw_scalebar_bk(B, V.X0, mb - 3.0 * kb, s, sbl, kb, L), mb - 9.5 * kb)
    draw_north_at(B, F2, V.X0 + sbl * s + 12.0 * kb, mb - 5.0 * kb, 4.0, kb, L)
    if pkey:                                              # names with no free place: a number, the words under the bar
        mb_crop = draw_label_key(B, pkey, V.X0, mb_crop - 1.0 * kb, mw, hs, L)
    # v51 (WO-T3a-2): no photo strip under plan 01 any more (it was the sheet's crop drw_photos, on no booklet page;
    # the photos stay on p.06, drw_edge_build)
    yy = min(mb - 2.6 * U, mb_crop - 1.0 * U)
    # legend (v38: drawn samples with short names; explanations as [n] in the Sources key)
    r_home = bcite("Urban fabric: each building's type from its survey layer, names and heritage tags, surveyed floors, "
                   "footprint size and regularity, shared walls and the grain of the 40 m around it; shares of the "
                   "built footprint.")
    r_crown = bcite("Crowns: modelled heights and leaf types (Meta/WRI 1 m canopy height map, Tolan et al. 2024; CLC+ "
                    "2021 and Sentinel-2).")
    r_edge = bcite("Stream edges: what meets the water along each bank.")
    leg = [("hdr", None, "BUILDINGS · URBAN FABRIC " + r_home)]
    ftot = sum(S.fabric_area.values()) or 1.0
    for fab in FABRIC_ORDER:                              # v40: the fabric map's types; under 0.5 % left out
        v_ = 100.0 * S.fabric_area.get(fab, 0.0) / ftot
        if round(v_) >= 1 or (fab in ("monument", "sacred") and S.fabric_area.get(fab, 0.0) > 0):
            leg.append(("box", FABRIC_PLAN[fab], u"{} · {}".format(FABRIC_SHORT[fab], "{:.0f}%".format(v_)
                                                                    if round(v_) >= 1 else "< 1%")))
    leg += [("dense", dc, "Densest grain · floor-area ratio {:.2f}+ {}".format(
                S.int_breaks[2], bcite(u"Densest grain: floor-area ratio on 10 m cells, areas of 2,000 m²+."))
             if getattr(S, "int_breaks", None) else "Densest grain")]      # v49.1 (Prompt 8): m² (was m2)
    leg += [("hdr", None, "GROUND AND GREEN")]
    for k_, lab in (("wood", "Woods"), ("park", "Parks"), ("grass", "Grass & lawns")):
        leg.append(("box", GREEN_SUB[k_], lab))
    leg += [("box", CAT["agri"][1], "Fields & orchards (survey, OSM)"), ("box", CAT["vacant"][1], "Vacant ground"),
            ("box", mix(CAT["transport"][1], PAPER, 0.3), "Parking & yards"), ("box", CAT["water"][1], "The stream")]
    for k_, lab, col in LC_CLASSES:
        if getattr(S, "lc", {}).get(k_):
            leg.append(("box", col, lab))
    for lf in (0, 1, 2):
        if any(c[4] == lf for c in crowns):
            leg.append(("dot", mix(LEAF_COL[lf], PAPER, 0.25), "Crown · " + LEAF_NAME[lf] + " " + r_crown))
    leg += [("dot", TREE_COLS["pine"], "Tree symbols of the survey"), ("dash", path_c, "Footpaths")]
    leg += [("hdr", None, "THE STREAM EDGE " + r_edge)]
    for k_ in EDGE_ORDER:
        if S.edge_len.get(k_, 0) > 0:
            leg.append(("thin", EDGE[k_][1], short(EDGE[k_][0])))
    leg += [("hdr", None, "MARKS")]
    leg += [("ktick", INK, "Bridges K1-K6")]
    leg += [("cdot", MARK_C, "{} {}".format(k, t)) for k, cx, cy, t in sorted(cs) if F.inside(cx, cy)]
    leg.append(R28_STUDY_LEG)                             # v50 (G8): the study area, one name on every map
    if RF is not None:
        leg.append(("thin", INK, R28_FRAME_NAME + " (site_alan) " + r_map))   # v50 (G8): was "Analysis range"
    ly = draw_legend_items(B, leg, x, yy - 1.0 * U, mw, U, L, h=0.4)
    # v45: the booklet page's legend leaves out what the site readings key: the ground and green colours (the land-use
    # ring's key); footpaths as a line. v51 (WO-T3a-2, p.02 flipped): the plan's key is its own panel at the top of
    # the side column (draw_plan01_key, crop drw_plan01_key), so it keys the stream edge colours again (the edge strip
    # under it is a drawing now, not colours) and the plan's crop carries no legend of its own (nothing twice)
    ring_c = set(c_ for l_, c_, a_ in landuse_slices(getattr(S, "site", S))[0])
    leg_bk, grp = [], ""
    for kind, col, lab in leg:
        if kind == "hdr":
            grp = lab
        elif not (grp == "GROUND AND GREEN" and kind == "box" and col in ring_c):
            leg_bk.append(("line" if kind == "dash" else kind, col, lab))
    _P02["leg"] = leg_bk
    _P02["cs"] = [(k_, t_) for k_, cx_, cy_, t_ in sorted(cs) if F.inside(cx_, cy_)]
    crop_panel("plan01", V.X0, mb_crop - 0.5 * kb, V.X0 + mw, ymap + 0.3 * U, u"Plan 01 · what is there today",
               crop_scale(s), [])                         # v40; v51: from the map's top down, its key in drw_plan01_key
    # v42: survey x, y of the plan's frame corners and where they sit on the sheet, so a later script (the farms map,
    # bergama_agriculture_alternatives) can place its own layer on this very plan in the booklet crop
    CROP_PANELS[-1]["geo"] = [(px_, py_) + tuple(V.p(px_, py_)) for px_, py_ in F2.P[:4]]
    tot = sum(S.fabric_area.values()) or 1.0
    # v38: the caption's two figures as tiles (were sentences); its notes are the key entries cited above
    return vis_tiles(B, x, ly - 0.3 * U, min(mw, 44.0 * U), [
        ("build", "OLD TOWN · % OF BUILT FOOTPRINT", "{:.0f}%".format(100.0 * S.fabric_area.get("traditional", 0.0) / tot),
         r_home),
        ("green", "CROWNS IN THE FRAME", "{}".format(len(crowns)), r_crown)], U, L, h=1.3, ink=INK, grey=INK2,
        fill=mix(PAPER, (255, 255, 255), 0.5), rule=FAINT)


# ------------------------------------------------------------ v51 (revision 29 Oct 2026, WO-T3a-2): p.02 and p.03
_P02 = {}                 # plan 01's key for draw_plan01_key (set by draw_what_is_there): text, leg, cs [(name, words)]
P02_C_R = 2.3             # booklet mm: radius of a conflict disc C1-C6 on plan 01 (its name inside, white 7 pt bold)
P02_ET_MIN = 32.0         # m: a bank stretch shorter than this is drawn as its longer neighbour (legible at print)
P02_ET_LAND = 30.0        # m of land drawn beyond the bank line on each bank of the edge strip
P02_ET_ZONE = 8.0         # m: the edge zone along the water where each edge type gets its own drawing
P02_ET_ROWS = 2           # the straightened stream in two rows (upstream half over downstream half): twice the length
P02_LEAF_SP = {0: "plane", 1: "olive", 2: "stone_pine"}   # crown glyph (plants.py pla_plan) by the canopy map's leaf type
P02_GROUND = mix(PAPER, (255, 255, 255), 0.45)            # open ground in the edge strip
P02_ROOF = mix(INK2, PAPER, 0.62)                         # roofs in the edge strip (one tone: a plan, not a use map)
P02_ROOF_L = mix(INK2, PAPER, 0.1)                        # their ridges, hips and fall lines (M11)
P02_ROAD = mix(INK2, PAPER, 0.5)                          # carriageway
P02_MAP_W = grid_w(7)     # booklet mm: plan 01 on the M1 grid (7 columns) ...
P02_SIDE_W = grid_w(5)    # ... and p.02's side column beside it (5 columns): the key, the edge strip, the readings
P02_GAP = GRID_GUT        # booklet mm between the side panels' halves / columns (the grid's gutter)
P03_FIG_EDGE = 30.0       # m: one figure watching the water along each walkable bank stretch, every this many m
P03_FIG_PATH = 80.0       # m: one figure walking a footpath every this many m
P03_FIG_MAX = 240         # at most this many figures on the axonometric
FIG_INK = INK
FIG_FILL = mix(PAPER, (255, 255, 255), 0.45)


def _p02_hit(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def _p02_col(c):
    """a colour of the house shapes (hex without '#', or rgb) as the board's rgb tuple"""
    if c is None or isinstance(c, tuple):
        return c
    if isinstance(c, list):
        return tuple(c[:3])
    return C(str(c))


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


def _p02_bld_plan(S, B, V, L, order, den, kb, bcol=None, lw_f=0.6):
    """revision 30 Oct (G7, M11; Aras "just draw the outlines and hatch the inside"): plan 01's buildings through
    bld_plan_items: per colour (bcol, the urban fabric) the light fill and the roof reading (ridge and hips where a
    building is BLD_MIN_ROOF_MM wide at 1:den), then ONE outline per block (S.blocks, merged in build_site): no line
    between buildings that share a wall, no piece outlines. lw_f thins the module's pens for the 1:20,000 plan."""
    groups = {}
    for u in S.bld:
        if not u.get("parts"):
            continue
        col = bcol(u) if bcol is not None else (mix(CAT[u["cat"]][1], PAPER, 0.35) if u["annex"] else CAT[u["cat"]][1])
        groups.setdefault(crop_hex(col), []).append(u)
    roof_c = crop_hex(mix(INK, PAPER, 0.45))
    for h_, us in sorted(groups.items()):
        _p02_items(B, V, bld_plan_items(us, None, den, fill=h_, her_fill=h_, roof_col=roof_c, outline=False), L,
                   order, kb, lw_f)
    edge = crop_hex(FABRIC_EDGE)
    _p02_items(B, V, bld_plan_items(S.bld, getattr(S, "blocks", None), den, roof="none", edge=edge, her_edge=edge), L,
               order + 2, kb, lw_f, fills=False)


def _p02_fig(pose, x, y, k, facing=1, view="side", ang=0.0, mm_per_m=None, pick=None):
    """ONE helper for every human figure of p.02-03 (HELPER_BRIEF rule 3): house shapes, k = drawing units per metre.
    v52: the A1 pen figures of figures.py (adult 1.75 m since the revision of 30 Oct, D9). side: fig_side(pose) with
    its feet at (x, y); top: fig_top(pose) centred on (x, y) heading ang (radians, 0 = +x). mm_per_m = booklet mm per metre where k is not
    (keeps the pen at least 0.10 mm). Line weights in mm of the drawing it lands on."""
    if view == "top":
        return fig_top(pose, x, y, k, ang=ang, ink=FIG_INK, mm_per_m=mm_per_m)
    return fig_side(pose, x, y, k, facing, ink=FIG_INK, mm_per_m=mm_per_m, pick=pick)


def draw_plan01_key(S, B, x, y, w, U):
    """v51 (WO-T3a-2, p.02 flipped): plan 01's explanation as its own panel at the top of p.02's side column (crop
    drw_plan01_key, P02_SIDE_W mm on the booklet page, three grid columns): what the plan shows, the
    conflicts C1-C6 drawn as on the plan (disc, name inside, words beside), then the plan's key (the land-use ring
    under the edge strip keys the ground colours). Words 7-8 pt. Returns the y below."""
    import re as _re
    L = "LU_BOARD::SiteReadings"
    if not _P02.get("leg"):
        LOG.append("Plan 01's key (drw_plan01_key): plan 01 was not drawn before it, so not drawn.")
        return y
    k = w / P02_SIDE_W
    h7, h75, h8 = bk_hk(7.0, k), bk_hk(7.5, k), bk_hk(8.0, k)
    # revision 30 Oct (G2, M1): three columns on the side column's grid (was two on 156 mm): the key is a third shorter
    hw = (w - 2.0 * P02_GAP * k) / 3.0
    cols = tuple(x + j_ * (hw + P02_GAP * k) for j_ in range(3))
    top = y
    cs = _P02.get("cs", [])
    site28_fit(B, u"**PLAN 01 · WHAT IS THERE TODAY{}**".format(
        u" · {} PLACES WHERE STREAM AND TOWN CLASH".format(len(cs)) if cs else u""), x, y - h8, h8, w, INK, L)
    yy = site28_para(B, _P02.get("text", u""), x, y - h8 - 1.6 * k - h7, w, h7, INK2, L, lead=1.45)
    # the conflicts as plan 01 draws them
    nr = (len(cs) + 2) // 3
    rc, hn = 2.0 * k, bk_hk(6.5, k)
    for j, (nm_, t_) in enumerate(cs):
        kx, yk = cols[j // nr], yy - (j % nr) * 5.6 * k
        cx_, cy_ = kx + rc + 0.4 * k, yk - rc
        B.fill([circle_pts(cx_, cy_, rc + 0.35 * k, 20)], WHITE, L, 20)
        B.fill([circle_pts(cx_, cy_, rc, 20)], MARK_C, L, 21)
        B.text(nm_, cx_, cy_, hn, WHITE, L, order=22, font=FONT_TITLE, bold=True, align="MC")
        site28_fit(B, t_, kx + 2.0 * rc + 1.8 * k, cy_ - 0.5 * h75, h75, hw - 2.0 * rc - 2.5 * k, INK, L)
    yy -= nr * 5.6 * k + 1.0 * k
    # the plan's key in the booklet legend's look (a 4.0 mm sample, the name 5.5 mm in at 7.5 pt, 4.0 mm a row)
    leg = [(kd, c_, _re.sub(r"\s*\[\d+\]", u"", lb).strip()) for kd, c_, lb in _P02["leg"] if kd not in ("cdot", "pdot")]
    nr = (len(leg) + 2) // 3
    Us = 4.0 * k / 1.1
    for j, (kd, c_, lb) in enumerate(leg):
        kx, yk = cols[j // nr], yy - h75 - (j % nr) * 4.0 * k
        draw_symbol(B, kd, c_, kx, yk - 0.2 * k, Us, L, sw=1.1, sh=0.72)
        site28_fit(B, lb, kx + 5.5 * k, yk, h75, hw - 6.0 * k, INK, L)
    low = yy - h75 - (nr - 1) * 4.0 * k - 1.5 * k
    crop_panel("plan01_key", x, low, x + w, top + 0.5 * k, u"Plan 01 · how to read it")
    CROP_PANELS[-1]["bk_w"] = P02_SIDE_W                  # its width on the booklet page (p.02's side column) ...
    CROP_PANELS[-1]["grid"] = [(c_ - x) / k for c_ in cols]   # ... and its three columns' left edges
    return low - 1.0 * U


# ------------------------------------------------------------ p.2 the site readings beside plan 01
def reading_rows(S):
    """v45: the key question's six readings: (name, phrase, [(m of bank, colour)]), stacked parts dark first."""
    e = S.edge_len
    wl, em = S.walled_len, getattr(S, "embanked_len", 0.0)
    tot = sum(e.values()) or 1.0
    return [("ACCESSIBLE", u"walkable edges within reach", [(e.get("pedestrian", 0.0), EDGE["pedestrian"][1])]),
            ("VISIBLE", u"street edges, seen across the water", [(e.get("street", 0.0), EDGE["street"][1])]),
            ("PERMEABLE", u"planted edges that let the ground through", [(e.get("green", 0.0), EDGE["green"][1])]),
            ("ENCLOSED", u"built edges: backs of buildings face the bed", [(e.get("building", 0.0), INK)]),
            ("DISCONNECTED", u"walled {:.0f}% · embanked {:.0f}%: cut off from the street".format(
                100.0 * wl / tot, 100.0 * em / tot), [(wl, INK2), (em, mix(INK2, PAPER, 0.5))]),
            ("TRANSFORMABLE", u"parking {:.0f}% · loose {:.0f}%: open to change".format(
                100.0 * e.get("parking", 0.0) / tot, 100.0 * e.get("open", 0.0) / tot),
             [(e.get("parking", 0.0), EDGE["parking"][1]), (e.get("open", 0.0), EDGE["open"][1])])]


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
    rows = [(short(CAT[k_][0]), CAT[k_][1], S.area.get(k_, 0.0)) for k_ in
            ("residential", "mixed", "commercial", "institutional", "religious", "industrial")]
    rows += [(u"Streets", ROAD_FILL, max(0.0, S.area.get("transport", 0.0) - tz)),
             (u"Parking & yards", mix(CAT["transport"][1], PAPER, 0.3), tz),
             (u"Woods & tree cover", GREEN_SUB["wood"], gz.get("wood", 0.0) + rest_of(S, "trees")),
             (u"Parks", GREEN_SUB["park"], gz.get("park", 0.0)),
             (u"Grass", GREEN_SUB["grass"], gz.get("grass", 0.0) + rest_of(S, "grass")),
             (u"Shrubs", lcc.get("shrub", mix(CAT["green"][1], PAPER, 0.3)), rest_of(S, "shrub")),
             (u"Fields & orchards, mapped", CAT["agri"][1], S.area.get("agri", 0.0) + rest_of(S, "farmland")),
             (u"Orchards (satellite)", lcc.get("orchard", ORCH_C), rest_of(S, "orchard")),
             (u"Vacant ground", CAT["vacant"][1], S.area.get("vacant", 0.0)),
             (u"The stream", CAT["water"][1], S.area.get("water", 0.0)),
             (u"Other unmapped", REST_C, rest_of(S, "rest"))]
    tot = frame_total(S) or 1.0
    rows.append((u"Others", mix(PAPER, INK2, 0.45), max(0.0, tot - sum(a for _l, _c, a in rows))))
    keep = [r_ for r_ in rows[:-1] if r_[2] >= 0.005 * tot]
    small = sum(r_[2] for r_ in rows if r_[2] < 0.005 * tot) + (rows[-1][2] if rows[-1][2] >= 0.005 * tot else 0.0)
    if small > 0.0005 * tot:
        keep.append((u"Others, each under 0.5%", rows[-1][1], small))
    return keep, tot


def draw_site_readings(S, B, x, y, w, U):
    """v51 (WO-T3a-2, p.02 flipped: Aras "first that map's explanation, below it the edge strip, below that the strip's
    analyses"): p.02's side column, top down: plan 01's key (draw_plan01_key, crop drw_plan01_key), the stream edge
    drawn from above (draw_edge_types, crop drw_edge_types), the bank readings and the land-use ring (_p02_readings,
    crop drw_site_readings). Each its own crop at P02_SIDE_W mm (5 grid columns); returns the y below."""
    y = draw_plan01_key(S, B, x, y, w, U)
    y = draw_edge_types(S, B, x, y, w, U)
    return _p02_readings(S, B, x, y, w, U)


def _p02_readings(S, B, x, y, w, U):
    """v45 (p.2: old p.4 "grain of the town" folded in): the six readings of the bank (accessible ... transformable)
    as bars, and the land use of the site frame as a ring with its key, in plan 01's colours; one panel w wide,
    designed for P02_SIDE_W mm beside plan 01 on the booklet page. Returns the y below. v50 (MIRAQUA 28 Oct, P02.1,
    P02.2): the ring's key on the panel's two-column grid. v51: the last panel of the side column (the edge strip is
    drawn above it by draw_site_readings). Revision 30 Oct (G2, M1: no leftover space): the side column on 5 grid
    columns, the ring's key beside the ring (was under both halves), so the panel prints at its own size, not shrunk."""
    L = "LU_BOARD::SiteReadings"
    k = w / P02_SIDE_W
    h7, h75, h8, h9, h12 = (bk_hk(p_, k) for p_ in (7.0, 7.5, 8.0, 9.0, 12.0))
    hw = 0.5 * (w - P02_GAP * k)                          # each half; the grid's gutter between them
    top = y
    # left: the bars
    tot = sum(S.edge_len.values())
    B.text(u"WHERE IS THE STREAM ...?", x, y - h8, h8, INK, L, font=FONT_TITLE, bold=True)
    B.text(u"% of the bank length · both banks · every 4 m " + bcite(EDGE_SRC), x, y - h8 - 1.6 * k - h7, h7, INK2,
           L, font=FONT_TITLE)
    yy = y - h8 - 1.6 * k - h7 - 4.0 * k
    if tot > 0:
        for name, phrase, parts in reading_rows(S):
            pct = 100.0 * sum(v_ for v_, c_ in parts) / tot
            B.text(name, x, yy - h75, h75, INK, L, font=FONT_TITLE, bold=True)
            site28_text(B, u"**{:.0f}%**".format(pct), x + hw, yy - h9, h9, INK, L, align="R")   # v50: real width
            yb = yy - h9 - 1.0 * k
            B.fill([rect(x, yb - 2.2 * k, x + hw, yb)], FAINT, L, 20)
            bx = x
            for v_, c_ in parts:
                if v_ > 0:
                    B.fill([rect(bx, yb - 2.2 * k, bx + hw * v_ / tot, yb)], c_, L, 21)
                    bx += hw * v_ / tot
            yp = yb - 2.2 * k - 1.0 * k - h7
            B.text(phrase, x, yp, h7, INK2, L, font=FONT_TITLE)
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
        rx, y - h8 - 1.6 * k - h7, h7, INK2, L, font=FONT_TITLE)
    r1, r0 = 17.0 * k, 10.5 * k
    cx, cy = rx + r1, y - h8 - 1.6 * k - h7 - 4.0 * k - r1
    a0 = math.pi / 2.0
    for lab, col, a in sl:
        a1 = a0 - 2.0 * math.pi * a / ftot
        B.fill([annulus(cx, cy, r0, r1, a0, a1)], col, L, 20)
        B.line([(cx + r0 * math.cos(a0), cy + r0 * math.sin(a0)), (cx + r1 * math.cos(a0), cy + r1 * math.sin(a0))],
               WHITE, L, 21, bk_lw(0.25, k))
        a0 = a1
    site28_text(B, u"**{:,.1f}**".format(ftot / 1e4), cx, cy + 0.6 * k, h12, INK, L, align="C")   # v50: real widths
    site28_text(B, u"ha", cx, cy - 1.4 * k - h7, h7, INK2, L, align="C")
    low = min(low, cy - r1)
    # beside the ring: its key (the plan's ground and green colours, so the plan needs no other key), next to its
    # drawing (G1); each entry as the booklet's legend_item draws one: a 4.0 x 2.8 mm swatch from 0.2 mm under the
    # baseline, the name 5.5 mm in at 7 pt, 3.6 mm a row
    kx = cx + r1 + P02_GAP * k
    kw = rx + hw - kx
    ky = cy + r1 - h7
    for j, (lab, col, a) in enumerate(sl):
        yk = ky - j * 3.6 * k
        B.fill([rect(kx, yk - 0.2 * k, kx + 4.0 * k, yk + 2.6 * k)], col, L, 20)
        pct = 100.0 * a / ftot
        site28_fit(B, u"{} {}".format(lab, u"{:.0f}%".format(pct) if pct >= 1.0 else u"< 1%"), kx + 5.5 * k, yk, h7,
                   kw - 5.5 * k, INK, L)
    low = min(low, ky - max(0, len(sl) - 1) * 3.6 * k - 1.5 * k)
    crop_panel("site_readings", x, low, x + w, top + 0.5 * k, u"Site readings · bank and ground")
    CROP_PANELS[-1]["bk_w"] = P02_SIDE_W                  # v45: its width on the booklet page (side panel of p.2) ...
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
    the canopy map's crowns, the survey buildings, green ground (parks, woods, grass) and the footpaths. Revision 30
    Oct (G7, M11): the buildings are bld_plan_items at 1:den (light roof, ridge, hips and fall lines, ONE outline per
    block of S.blocks: no piece or parcel lines), each item's points carried onto the strip: st["bitems"] =
    [(bank, "fill", [rings], hex, None) | (bank, "line", pts, hex, width booklet mm)]."""
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
    bitems = _p02_strip_blds(S, LX, LY, LC, Lt, reach, beyond, ctr, den)
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
                cr.append((sd, s_, b_, c[2], c[4]))
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
    st = dict(types=[_p02_join([v_[0] if v_ else None for v_ in d["bins"][sd]], nmin) for sd in (0, 1)],
              walls=[_p02_join([v_[1] if v_ else None for v_ in d["bins"][sd]], nmin) for sd in (0, 1)],
              off=off, crowns=cr, bitems=bitems, greens=gr, paths=pth)
    S._p02_st = st
    LOG.append(u"Stream edge strip (drw_edge_types): {} crowns, {} building fills and outlines (M11), {} green areas "
               u"and {} path pieces within {:.0f} m of the banks; stretches under {:.0f} m joined to their "
               u"neighbour.".format(len(cr), len(bitems), len(gr), len(pth), P02_ET_LAND, P02_ET_MIN))
    return st


def _p02_strip_blds(S, LX, LY, LC, Lt, reach, beyond, ctr, den):
    """revision 30 Oct (G7, M11): the buildings within reach of the stream as bld_plan_items (survey m) at 1:den, in
    the strip's (chainage m, m beyond the bank line) per bank: a ring or line across the stream, out of the frame's
    chainage, past P02_ET_LAND or longer than 150 m is left out. Whole blocks: a block with one building in reach
    comes with all of its buildings, so its one outline is kept. Fills keep their rings together (courtyards open)."""
    if not S.bld:
        return []
    keep = set()
    cen = site28_project(LX, LY, LC, [ctr(u["parts"][0]) if u.get("parts") else (LX[0], LY[0]) for u in S.bld])
    for i, (u, (s_, o_)) in enumerate(zip(S.bld, cen)):
        if u.get("parts") and -60.0 <= s_ <= Lt + 60.0 and abs(o_) < reach:
            keep.add(i)
    blocks = getattr(S, "blocks", None)
    if blocks:
        for b_ in blocks:
            if any(i in keep for i in b_["units"]):
                keep.update(b_["units"])
    idx = sorted(keep)
    if not idx:
        return []
    remap = dict((i, j) for j, i in enumerate(idx))
    sb = [dict(b_, units=[remap[i] for i in b_["units"]]) for b_ in blocks
          if any(i in remap for i in b_["units"])] if blocks else None
    rf, ed = crop_hex(P02_ROOF), crop_hex(INK)            # heritage in the same tones: the strip has no heritage key
    items = bld_plan_items([S.bld[i] for i in idx], sb, den, roof="hatch", fill=rf, edge=ed,
                           roof_col=crop_hex(P02_ROOF_L), her_fill=rf, her_edge=ed)
    pts, segs = [], []                                    # every point projected in one go
    for n_, it in enumerate(items):
        if it[0] == "fill":
            for R in it[1]:
                if len(R) >= 3:
                    segs.append((n_, "fill", len(pts), len(R), it[2], None))
                    pts.extend(R)
        elif it[0] == "line" and len(it[1]) >= 2:
            segs.append((n_, "line", len(pts), len(it[1]), it[2], it[3]))
            pts.extend(it[1])
    q = site28_project(LX, LY, LC, pts)
    fills, out = {}, []
    for n_, kind, i0, m_, col, lw in segs:
        Q = q[i0:i0 + m_]
        sides = set(0 if o_ > 0.0 else 1 for s_, o_ in Q)
        if len(sides) != 1:
            continue
        sd = sides.pop()
        ring = [(s_, beyond(s_, o_, sd)) for s_, o_ in Q]
        ss, dd = [r_[0] for r_ in ring], [r_[1] for r_ in ring]
        if max(ss) < 0.0 or min(ss) > Lt or min(dd) > P02_ET_LAND or max(dd) < -1.0 or max(ss) - min(ss) > 150.0:
            continue
        if kind == "fill":
            fills.setdefault((n_, sd), (col, []))[1].append(ring)
        else:
            out.append((sd, "line", ring, col, lw))
    return [(sd, "fill", rings, col, None) for (n_, sd), (col, rings) in sorted(fills.items())] + out


def _p02_crown(leaf, cx, cy, D, k, seed=0):
    """a tree from above D board units wide: plants.py pla_plan's crown of the species standing for the canopy map's
    leaf type (P02_LEAF_SP), scaled to D; a plain crown when the plant module is missing"""
    fn = globals().get("pla_plan")
    if fn is not None:
        try:
            cm = 10.0
            sh = fn(P02_LEAF_SP.get(leaf, "plane"), 0.0, 0.0, D / k / cm, crown_m=cm, seed=seed)
            return [(s_[0], [(cx + px * k, cy + py * k) for px, py in s_[1]]) + tuple(s_[2:]) for s_ in sh]
        except Exception:
            pass
    return [("poly", circle_pts(cx, cy, 0.5 * D, 14), mix(LEAF_COL.get(leaf, LEAF_COL[0]), PAPER, 0.15), INK2, 0.08)]


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
        B.fill([r_], mix(EDGE["pedestrian"][1], PAPER, 0.8), L, order)
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
            _p02_put(B, _p02_fig("walk", fx, fy, 3.0 * k, view="top", ang=0.0 if j % 2 else math.pi, mm_per_m=3.0),
                     L, order + 3, k)
    elif t == "street":
        B.fill([r_], P02_ROAD, L, order)
        for y_ in (ya, yb):                               # kerbs
            B.line([(x0, y_), (x1, y_)], INK, L, order + 1, bk_lw(0.12, k))
        for d_ in dashes([(x0, 0.5 * (ya + yb)), (x1, 0.5 * (ya + yb))], 0.9 * k, 0.6 * k):
            B.line(d_, WHITE, L, order + 1, bk_lw(0.12, k))
    elif t == "parking":
        B.fill([r_], mix(INK2, PAPER, 0.62), L, order)
        B.line([(x0, yl), (x1, yl)], INK, L, order + 1, bk_lw(0.1, k))
        xx = x0 + 1.1 * k
        while xx < x1:                                    # bays
            B.line([(xx, yw), (xx, yw + sg * 0.75 * hz)], WHITE, L, order + 1, bk_lw(0.1, k))
            xx += 1.1 * k
    elif t == "green":
        B.fill([r_], mix(GREEN_SUB["grass"], PAPER, 0.35), L, order)
        tc, xx, j = mix(GREEN_SUB["wood"], INK, 0.15), x0 + 0.5 * k, 0
        while xx < x1 - 0.3 * k:                          # grass tufts
            ty = ya + (0.3 if j % 2 else 0.62) * hz
            B.line([(xx - 0.25 * k, ty + 0.35 * k), (xx, ty), (xx + 0.25 * k, ty + 0.35 * k)], tc, L, order + 1,
                   bk_lw(0.07, k))
            xx += 0.9 * k
            j += 1
    elif t == "open":
        B.fill([r_], mix(EDGE["open"][1], PAPER, 0.5), L, order)
        dc = mix(INK2, PAPER, 0.2)
        for j in range(int((x1 - x0) / (0.45 * k))):     # bare ground, stippled
            B.fill([circle_pts(x0 + (j + 0.5) * 0.45 * k, ya + ((j * 37) % 10 + 0.5) / 10.0 * hz, 0.1 * k, 6)], dc, L,
                   order + 1)
    elif t == "building":                                 # revision 30 Oct (G7, M11): a row of roofs, as the
        B.fill([r_], P02_ROOF, L, order)                  # buildings beyond: roof tone, ridge, party walls
        ym = 0.5 * (ya + yb)
        B.line([(x0, ym), (x1, ym)], P02_ROOF_L, L, order + 1, bk_lw(0.07, k))
        xx, j = x0 + 1.6 * k, 0
        while xx < x1 - 0.3 * k:                          # party walls between the roofs, a hip on each side
            B.line([(xx, ya), (xx, yb)], INK, L, order + 1, bk_lw(0.06, k))
            xx += (1.6 if j % 2 else 2.1) * k
            j += 1
        B.line([(x0, yl), (x1, yl)], INK, L, order + 2, bk_lw(0.12, k))
        B.line([(x0, yw), (x1, yw)], INK, L, order + 2, bk_lw(0.45, k))     # the backs on the water


def _p02_wall(B, wl, x0, x1, yw, yl, k, L, order):
    """v51: the bank face between the land (yl) and the water (yw) from above: a wall in stone courses (1), an
    embankment in slope hachures from its top line down to the water (2), else the ground running to the water"""
    if x1 - x0 < 0.15 * k:
        return
    ya, yb = min(yw, yl), max(yw, yl)
    r_ = rect(x0, ya, x1, yb)
    sg = 1.0 if yl > yw else -1.0
    if wl == 1:
        B.fill([r_], mix(INK2, PAPER, 0.25), L, order)
        ym = 0.5 * (ya + yb)
        B.line([(x0, ym), (x1, ym)], P02_GROUND, L, order + 1, bk_lw(0.05, k))
        xx, j = x0 + 0.45 * k, 0
        while xx < x1:                                    # joints, staggered course to course
            B.line([(xx, ya if j % 2 else ym), (xx, ym if j % 2 else yb)], P02_GROUND, L, order + 1, bk_lw(0.05, k))
            xx += 0.45 * k
            j += 1
        for y_ in (ya, yb):
            B.line([(x0, y_), (x1, y_)], INK, L, order + 1, bk_lw(0.12, k))
    elif wl == 2:
        B.fill([r_], mix(EDGE["open"][1], PAPER, 0.6), L, order)
        B.line([(x0, yl), (x1, yl)], INK2, L, order + 1, bk_lw(0.12, k))   # top of the slope
        xx, j = x0 + 0.25 * k, 0
        while xx < x1:                                    # hachures, long and short, down to the water
            B.line([(xx, yl), (xx, yl - sg * (yb - ya) * (0.95 if j % 2 == 0 else 0.5))], INK2, L, order + 1,
                   bk_lw(0.07, k))
            xx += 0.45 * k
            j += 1
    else:
        B.fill([r_], P02_GROUND, L, order)


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
    B.fill([rect(x0, y0, x1, y1)], CAT["water"][1], L, order)


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


def draw_edge_types(S, B, x, y, w, U):
    """v51 (WO-T3a-2, Aras: "redraw it in a top-view architectural drawing language ... not an analysis"; the idea of
    R01: each stretch of the corridor in its own drawn language): both banks of the Selinos stream straightened along
    its chainage (no scale: a diagram) and seen from above, in P02_ET_ROWS rows (upstream half over downstream half).
    The stream in the middle with its covered reaches hatched and its bridges as decks; on each bank the bank face (a
    wall in stone courses, an embankment in slope hachures) and an edge zone in its edge type's language (_p02_zone:
    people walking where it is walkable, a carriageway, parking bays, grass, bare ground, the buildings' backs), and
    beyond it what stands within P02_ET_LAND m of the water (_p02_strip): green ground, footpaths, the survey's
    buildings, the canopy map's trees (plants.py crowns). The same 4 m bank samples as the bars (site28_edge_bins),
    stretches under P02_ET_MIN m joined to their neighbour. Each edge type named on its longest stretch, K1-K6 under
    each row, the key as drawn samples. Its own crop (drw_edge_types), P02_SIDE_W mm in p.02's side column under plan
    01's key; words 6.5-8 pt. Returns the y below. Revision 30 Oct (PG1 p2, G7, G8, M2, M5, M11): buildings as
    outline + roof (bld_plan_items, no piece lines), the water through water_plan, decks in planks, paving in slabs, the
    key laid out by M2 Legend under the drawing; the page's finding (walled ... walkable ...) is the booklet intro
    only (not repeated here)."""
    L = "LU_BOARD::SiteReadings"
    d = site28_edge_bins(S)
    if not d:
        LOG.append("Stream edge diagram (drw_edge_types): no bank samples or no centreline in the data pack, so not "
                   "drawn.")
        return y
    k = w / P02_SIDE_W
    h65, h7, h8 = bk_hk(6.5, k), bk_hk(7.0, k), bk_hk(8.0, k)
    top = y
    # revision 30 Oct (G4): the heading names the drawing; the finding (walled ... walkable ...) is the page intro
    site28_fit(B, u"**THE STREAM EDGE FROM ABOVE · BOTH BANKS, STRAIGHTENED**", x, y - h8, h8, w, INK, L)
    yy = site28_para(B, u"What stands within {:.0f} m of the water, **left** and **right** bank looking downstream; "
                        u"chainage in m from the upstream end of the frame {}{}".format(
                            P02_ET_LAND, bcite(EDGE_SRC),
                            bcite("Crowns: modelled heights and leaf types (Meta/WRI 1 m canopy height map, Tolan et al. "
                                  "2024; CLC+ 2021 and Sentinel-2).")),
                     x, y - h8 - 1.6 * k - h7, w, h7, INK2, L, lead=1.45)
    lab_w = max(site28_tw(t_, h65, True) for t_ in (u"LEFT", u"RIGHT")) + 1.8 * k
    gx0, gx1 = x + lab_w, x + w
    nrow = max(1, P02_ET_ROWS)
    Lr = d["L"] / nrow
    sx = (gx1 - gx0) / Lr
    HB, WS, SW = 7.0 * k, 1.5 * k, 4.0 * k               # each bank, each bank face, the stream (booklet mm)
    my = HB / P02_ET_LAND
    st = _p02_strip(S, d, den=bk_std(1000.0 * k / my))   # M11 roofs read at the strip's scale across the banks
    bm = d["bm"]
    cov_c = mix(CAT["water"][1], PAPER, 0.55)
    path_c = mix(CAT["green"][1], INK, 0.35)
    LX, LY, LC = d["line"]
    kp = site28_project(LX, LY, LC, [(b_[2], b_[3]) for b_ in BRIDGES_K])
    bch = d["cor"].get("bridges_ch", [])
    decks = [(bch[i_], bch[i_ + 1]) for i_ in range(0, len(bch) - 1, 2)]
    covs = list(d["cor"].get("covered_reaches", []))
    longest = {}                                          # edge type -> its longest stretch on the page, to name it
    free = (0.0, 0.0, 0.0, 0.0, 0.0)                      # the longest open water, to name the stream
    yy -= 0.6 * k
    low = yy
    for r in range(nrow):
        s0, s1 = r * Lr, (r + 1) * Lr

        def X(s_, s0=s0):
            return gx0 + (s_ - s0) * sx
        ya = yy - h65
        v = math.ceil(s0 / 250.0 - 1e-9) * 250.0
        while v <= s1 + 1e-6:                             # the chainage every 250 m, its unit on the row's last number
            t_ = u"{:,.0f}".format(v) + (u" m" if v + 250.0 > s1 + 1e-6 else u"")
            tx = min(max(X(v) - 0.5 * site28_tw(t_, h65), gx0), gx1 - site28_tw(t_, h65))
            B.text(t_, tx, ya, h65, INK2, L, font=FONT_TITLE)
            B.line([(X(v), ya - 0.4 * k), (X(v), ya - 1.2 * k)], INK2, L, 21, bk_lw(0.15, k))
            v += 250.0
        yb0 = ya - 1.2 * k                                # left bank (land at the top), its face, the stream, the
        yLw = yb0 - HB                                    # right bank's face, the right bank (land at the bottom)
        yst = yLw - WS
        ysb = yst - SW
        yRw = ysb - WS
        ybot = yRw - HB
        band = {0: (yLw, yb0), 1: (ybot, yRw)}
        face = {0: (yst, yLw), 1: (yRw, ysb)}             # (water y, land y)

        def Yd(sd, b_):
            return yLw + b_ * my if sd == 0 else yRw - b_ * my
        for t_, sd in ((u"LEFT", 0), (u"RIGHT", 1)):
            B.text(t_, x, 0.5 * sum(band[sd]) - 0.5 * h65, h65, INK, L, font=FONT_TITLE, bold=True)
        for sd in (0, 1):
            lo, hi = band[sd]
            box = (gx0, lo, gx1, hi)
            B.fill([rect(gx0, lo, gx1, hi)], P02_GROUND, L, 20)
            for sd_, ring, sub in st["greens"]:           # green ground: parks, woods, grass
                if sd_ == sd and max(p[0] for p in ring) >= s0 and min(p[0] for p in ring) <= s1:
                    P = clip_rect_poly([(X(a_), Yd(sd, b_)) for a_, b_ in ring], box)
                    if len(P) >= 3:
                        B.fill([P], mix(GREEN_SUB.get(sub, GREEN_SUB["park"]), PAPER, 0.45), L, 21)
            zw, zl = Yd(sd, 0.0), Yd(sd, P02_ET_ZONE)
            for i0, i1, t_ in site28_runs(st["types"][sd]):        # the edge zone in its type's language
                a_, b_ = max(i0 * bm, s0), min(i1 * bm, s1)
                if b_ > a_:
                    _p02_zone(B, t_, X(a_), X(b_), zw, zl, k, L, 22)
                    if X(b_) - X(a_) > longest.get(t_, (0.0,))[0]:
                        longest[t_] = (X(b_) - X(a_), sd, X(a_), X(b_), lo, hi)
            for sd_, pl in st["paths"]:                   # footpaths
                if sd_ != sd:
                    continue
                for run_ in clip_rect_line([(X(a_), Yd(sd, b_)) for a_, b_ in pl], box):
                    if len(run_) > 1:
                        for d_ in dashes(list(run_), 0.5 * k, 0.35 * k):
                            B.line(d_, path_c, L, 23, bk_lw(0.12, k))
            for sd_, kd_, geo, col_, lw_ in st["bitems"]:  # the survey's buildings: roofs and block outlines (M11)
                if sd_ != sd:
                    continue
                if kd_ == "fill":
                    Ps = []
                    for ring in geo:
                        if max(p[0] for p in ring) >= s0 and min(p[0] for p in ring) <= s1:
                            P = clip_rect_poly([(X(a_), Yd(sd, b_)) for a_, b_ in ring], box)
                            if len(P) >= 3:
                                Ps.append(P)
                    if Ps:
                        B.fill(Ps, _p02_col(col_), L, 24)
                elif max(p[0] for p in geo) >= s0 and min(p[0] for p in geo) <= s1:
                    for run_ in clip_rect_line([(X(a_), Yd(sd, b_)) for a_, b_ in geo], box):
                        if len(run_) > 1:
                            B.line(list(run_), _p02_col(col_), L, 25, bk_lw(lw_, k))
            grid_, kept = {}, []                          # trees, the larger first, none hiding another
            for sd_, s_, b_, rr, lf in sorted(st["crowns"], key=lambda c_: -c_[3]):
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
                kept.append((cx_, cy_, D, lf, int(s_)))
            for cx_, cy_, D, lf, sd_seed in kept:
                _p02_put(B, _p02_crown(lf, cx_, cy_, D, k, sd_seed), L, 26, k)
            yw_, yl_ = face[sd]                           # the bank face
            B.fill([rect(gx0, min(yw_, yl_), gx1, max(yw_, yl_))], P02_GROUND, L, 20)
            for i0, i1, wv in site28_runs(st["walls"][sd]):
                a_, b_ = max(i0 * bm, s0), min(i1 * bm, s1)
                if b_ > a_:
                    _p02_wall(B, wv, X(a_), X(b_), yw_, yl_, k, L, 27)
        # the stream (M5 water_plan: surface, flow streaks deepening to the middle, bank edge), its covered reaches,
        # the bridges' decks
        _p02_water(B, gx0, ysb, gx1, yst, k, L, 20, seed=r)
        for a_, b_ in covs:
            a_, b_ = max(a_, s0), min(b_, s1)
            if b_ > a_:
                cr_ = rect(X(a_), ysb, X(b_), yst)
                B.fill([cr_], cov_c, L, 21)
                B.hatch([cr_], SS_COVER_C, L, 22, 0.8 * k, math.radians(45.0), bk_lw(0.12, k))
        for a_, b_ in decks:
            if b_ >= s0 and a_ <= s1:
                xm, hd = X(0.5 * (a_ + b_)), max(0.35 * k, 0.5 * (b_ - a_) * sx)
                _p02_deck(B, xm - hd, yRw, xm + hd, yLw, k, L, 29)
        c_ = s0
        for a_, b_ in sorted([(max(a_, s0), min(b_, s1)) for a_, b_ in covs + decks if b_ > s0 and a_ < s1]) + \
                [(s1, s1)]:
            if X(a_) - X(c_) > free[0]:
                free = (X(a_) - X(c_), X(c_), X(a_), ysb, yst)
            c_ = max(c_, b_)
        # K1-K6: a tick under the row, the name under it (placed clear of each other)
        items = []
        for (kk, nm_, bx, by), (s_, o_) in zip(BRIDGES_K, kp):
            if not s0 <= s_ < s1 or not 0.0 <= s_ <= d["L"] or abs(o_) > SITE28_K_NEAR:
                continue
            px = X(s_)
            B.line([(px, ybot - 0.2 * k), (px, ybot - 1.0 * k)], INK, L, 30, bk_lw(0.3, k))
            t_ = u"**{}** {}".format(kk, nm_)
            wd = site28_line_w(site28_one(t_, h7), h7) / k
            items.append(dict(x=px / k, y=(ybot - 1.0 * k) / k, rank=0, t=t_,
                              wh=(lambda f, wd=wd: (wd * f + 0.8, 1.5 * h7 / k * f))))
        taken = [(x / k, (ybot - 0.2 * k) / k, (x + w) / k, (ya + h65) / k)]
        got = place_labels_all(items, taken, bounds=(x / k, (ybot - 12.0 * k) / k, (x + w) / k, (ybot - 0.4 * k) / k),
                               sizes=(1.0,))
        low = ybot - 1.2 * k
        for i, (bx, lead, f) in got.items():
            it = items[i]
            e = lp_leader_end(bx, (it["x"], it["y"]))
            B.line([(it["x"] * k, it["y"] * k), (e[0] * k, e[1] * k)], INK2, L, 24, bk_lw(0.15, k))
            site28_text(B, it["t"], (bx[0] + 0.4) * k, bx[1] * k + 0.3 * h7, h7, INK, L)
            low = min(low, bx[1] * k)
        yy = low - 2.4 * k
    # names on the drawing: each edge type on its longest stretch (land side, on a paper ground), the stream
    names = dict(SITE28_ET_KEY)
    for t_, (wd, sd, xa, xb, lo, hi) in sorted(longest.items()):
        nm_ = names.get(t_, t_)
        tw_ = site28_tw(nm_, h65)
        if wd < tw_ + 1.6 * k:
            continue
        tx = 0.5 * (xa + xb) - 0.5 * tw_
        ty = hi - 0.5 * k - h65 if sd == 0 else lo + 0.6 * k
        B.fill([rect(tx - 0.4 * k, ty - 0.35 * k, tx + tw_ + 0.4 * k, ty + h65 + 0.35 * k)], WHITE, L, 31)
        B.text(nm_, tx, ty, h65, INK, L, order=32, font=FONT_TITLE)
    snm = u"Selinos stream"
    if free[0] > site28_tw(snm, h65) + 6.0 * k:
        sxm, sym = 0.5 * (free[1] + free[2]), 0.5 * (free[3] + free[4])
        wn_c = mix(CAT["water"][1], INK, 0.55)            # revision 30 Oct: dark on the calm M5 surface, on a
        tw_s = site28_tw(snm, h65)                        # plate of that surface (no streak through the name, G3)
        B.fill([rect(sxm - 1.2 * k - 0.5 * tw_s - 0.6 * k, sym - 0.75 * h65, sxm - 1.2 * k + 0.5 * tw_s + 4.0 * k,
                     sym + 0.75 * h65)], mix(CAT["water"][1], PAPER, 0.62), L, 30)
        B.text(snm, sxm - 1.2 * k, sym, h65, wn_c, L, order=31, font=FONT_TITLE, italic=True, align="MC")
        ax0 = sxm - 1.2 * k + 0.5 * site28_tw(snm, h65) + 0.8 * k        # the way it flows
        B.line([(ax0, sym), (ax0 + 2.0 * k, sym)], wn_c, L, 31, bk_lw(0.2, k))
        B.fill([[(ax0 + 2.6 * k, sym), (ax0 + 1.8 * k, sym + 0.45 * k), (ax0 + 1.8 * k, sym - 0.45 * k)]], wn_c, L,
               31)
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
    for cd_, nm_ in ((("g", None), u"green ground"), (("b", None), u"roofs and buildings"), (("t", None), u"trees"),
                     (("p", None), u"footpaths"), (("s", None), u"the stream"), (("c", None), u"covered stream"),
                     (("k", None), u"bridge deck")):
        lg.add(nm_, "sample", code=cd_)
    lay = lg.layout(lambda s_, pt_, b_: site28_tw(s_, bk_hk(pt_, k), b_) / k, size_pt=7.0)
    for row_ in lay["rows"]:
        kd, v_ = row_["code"]
        kx, y0_, x1_, y1_ = (c_ * k for c_ in row_["swatch"])
        if kd == "z":
            _p02_zone(B, v_, kx, x1_, y0_, y1_, k, L, 22)
        elif kd == "w":
            _p02_wall(B, v_, kx, x1_, y0_, y1_, k, L, 22)
        elif kd == "g":
            B.fill([rect(kx, y0_, x1_, y1_)], mix(GREEN_SUB["park"], PAPER, 0.45), L, 21)
        elif kd == "b":                                   # a building as the strip draws it (M11 roof reading)
            Pb = rect(kx + 0.4 * k, y0_ + 0.3 * k, x1_ - 0.4 * k, y1_ - 0.3 * k)
            B.fill([Pb], P02_ROOF, L, 21)
            for a_, b_ in bld_roof_lines(Pb, "ridge"):
                B.line([a_, b_], P02_ROOF_L, L, 22, bk_lw(0.07, k))
            B.line(Pb + [Pb[0]], INK, L, 22, bk_lw(0.18, k))
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
    low = lay["box"][1] * k - 1.0 * k
    crop_panel("edge_types", x, low, x + w, top + 0.5 * k, u"The stream edge · both banks, straightened, from above")
    CROP_PANELS[-1]["bk_w"] = P02_SIDE_W                  # its width on the booklet page (p.02's side column) ...
    CROP_PANELS[-1]["grid"] = [0.0, P02_SIDE_W - 0.5 * (P02_SIDE_W - P02_GAP)]   # ... on the readings' two halves
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


def export_axonometrics(S):
    """v33 (Aras Q8; Step 4, 07:05-07:09): S1 as a parallel axonometric, one A3 vector PDF beside the board's PDFs
    (S2 has none: its walk table gives each walk's climb). Returns the paths written."""
    import datetime as _dt
    DG, ctx = diagram_ctx(S)
    stamp = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    out = []
    if not os.path.isdir(pdf_folder()):
        os.makedirs(pdf_folder())
    del CROP_DIRECT[:]
    # v51 (WO-T3a-2, 02 §3): people on the axonometric. The engine (data/DIAG_SRC.py) is not this page's file: its
    # compose() calls chrome() last with the drawing's view, so the figures go in there (_p03_figures), and the
    # engine's own chrome is put back after the loop
    chrome0 = DG.get("chrome")

    def chrome_figs(pg_, ctx_, spec_, ext_, V_, stamp_):
        try:
            _p03_figures(S, pg_, V_, ext_["rect"])
        except Exception:
            LOG.append("WARNING: the axonometric's figures failed (drawn without them):\n" + traceback.format_exc())
        return chrome0(pg_, ctx_, spec_, ext_, V_, stamp_)
    if chrome0 is not None:
        DG["chrome"] = chrome_figs
    try:
        out = _p03_axo_loop(S, DG, ctx, stamp, out)
    finally:
        if chrome0 is not None:
            DG["chrome"] = chrome0
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
    for did, fn in (("S1", "Selinus_01_what_is_there_axonometric.pdf"),):
        t0 = time.time()
        ext = ctx.extents[0]
        try:
            spec = DG["SPECS"][did](ctx, ext)
            for c_ in spec.get("calls", []):
                c_["title"] = _re.sub(r"\s*\[\d+\]", u"", c_.get("title", u""))
            leg0 = spec["legend"]
            spec["legend"] = lambda leg0=leg0: [(k_, c_, _p03_label(t_)) for k_, c_, t_ in
                                                (leg0() if callable(leg0) else leg0)]
            pg, st = DG["compose"](ctx, spec, ext, stamp)
            p = os.path.join(pdf_folder(), fn)
            DG["write_pdf"]([pg], p)
            out.append((p, time.time() - t0))
            bx, ph = DG["BOX"], DG["PAGE_H"]                 # v40: the booklet crop: the page between the rules (the
            bx = (0.0, bx[1], DG["PAGE_W"], bx[3])            # callouts may sit beyond the drawing box, left and right)
            rm = (bx[0], ph - bx[3] - 4.0, bx[2], ph - bx[1] + 4.0)    # y down
            bb = _p03_bbox(pg, DG, bx[1] - 4.0, bx[3] + 4.0)
            if bb is not None:                                # tight round the model and its callouts (y down)
                rm = (max(rm[0], bb[0] - 2.0), max(rm[1], ph - bb[3] - 2.0), min(rm[2], bb[2] + 2.0),
                      min(rm[3], ph - bb[1] + 2.0))
            leg = [(("dot", DG["TREE_STYLES"].get(c_, DG["TREE_STYLES"]["tree"])["mid"]) if k_ == "tree" else (k_, c_))
                   + (t_,) for k_, c_, t_ in spec["legend"]() if c_ is not None]
            CROP_DIRECT.append(("axo_what_is_there", fn, rm,
                                u"What is there · heights, heritage, water, green", None, crop_legend(leg), []))
        except Exception:
            LOG.append("WARNING: the {} axonometric failed:\n{}".format(did, traceback.format_exc()))
    return out


def draw_landcover(S, B, V, L, order=2):
    """v31: the land-cover classes, each one fill (even-odd over all its rings), order 2 after the paper."""
    leg = []
    for k, lab, col in LC_CLASSES:
        rings = getattr(S, "lc", {}).get(k)
        if rings:
            for i in range(0, len(rings), 400):
                B.fill(V.Ps(rings[i:i + 400]), col, L, order)
            leg.append(("box", col, lab))
    return leg
