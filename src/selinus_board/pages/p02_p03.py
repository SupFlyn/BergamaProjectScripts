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
def edge_key(a, b):
    return frozenset(((round(a[0], 3), round(a[1], 3)), (round(b[0], 3), round(b[1], 3))))


def edge_counts(polys):
    n = {}
    for P in polys:
        for i in range(len(P)):
            e = edge_key(P[i], P[(i + 1) % len(P)])
            n[e] = n.get(e, 0) + 1
    return n


def unit_outline(parts, n=None):
    """v41 (Aras 26 Oct 06:35 "these lines in what is there looks weird"): the pale outline of a building = its edges
    without the walls it shares with another piece (n: edge counts over all buildings), so a footprint the survey
    draws as one block and the script cuts along its party walls reads as one mass, with no cut lines through it.
    Open runs of edges, or the closed piece where nothing is shared."""
    n = n or edge_counts(parts)
    k = edge_key
    out = []
    for P in parts:
        m = len(P)
        inner = [n.get(k(P[i], P[(i + 1) % m]), 0) > 1 for i in range(m)]
        if not any(inner):
            out.append(P + [P[0]])
            continue
        i0 = inner.index(True)
        run = []
        for j in range(1, m + 1):
            i = (i0 + j) % m
            if inner[i]:
                if len(run) > 1:
                    out.append(run)
                run = []
            else:
                run = run or [P[i]]
                run.append(P[(i + 1) % m])
        if len(run) > 1:
            out.append(run)
    return out


def draw_landuse_map(S, B, V, bcol=None):
    """bcol (v33): the colour of each building (default: its land-use colour)."""
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
    shared = edge_counts([P for u in S.bld for P in u["parts"]]) if TEXTURE else None
    for u in S.bld:
        col = CAT[u["cat"]][1]
        if u["annex"]:
            col = mix(col, PAPER, 0.35)
        if bcol is not None:
            col = bcol(u)
        B.fill(V.Ps(u["parts"] + (u.get("holes") or [])), col, L + "::" + u["cat"], 14)
        if TEXTURE:
            for P in unit_outline(u["parts"], shared) + [H + [H[0]] for H in u.get("holes") or []]:
                B.line(V.P(P), PAPER, L + "::texture", 15, 0.04)
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
                  "and photos exist for the site only." if RF is not None else
                  "Plan 01: context beyond the frame: survey line work only.")
    B.text("WHAT IS THERE · GROUND · BUILDINGS · GREEN · STREAM EDGE " + r_map, x, y, 1.05 * U, INK, L,
           font=FONT_TITLE, bold=True)                    # v38: keywords; the coverage note is a key entry
    # v45: plan 01 prints at 1:den_bk beside the site readings (P01_BK_W mm wide): its marks and words are sized for
    # that page (kb = board units per booklet mm; the map is as wide as w)
    den_bk = bk_std(F2.w * 1000.0 / P01_BK_W)
    kb = w / F2.w * den_bk / 1000.0
    # v42 (review rule 4): what the plan shows, why it is here, what to read from it; sized with the plan's width
    ch_ = max(CTX_H * U * max(1.0, w / (120.0 * U)), bk_hk(7.0, kb, mono=True))
    ctop = y - 0.6 * U - ch_
    ymap = ctx_line(B, u"The whole survey area as it is today, on one plan: buildings by urban fabric, ground and green, "
                       u"the Selinos with its edges, bridges and photo points. It is the base the later plans are read "
                       u"on: what the project keeps, joins and changes.", x, ctop, w, ch_, L) - 0.2 * ch_
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
    draw_landuse_map(S, B, V, bcol=fabric_col)            # v40: buildings by urban fabric type
    for u in S.bld:                                       # light types get a hairline so they read on paper
        if not u["annex"] and u.get("fabric") in ("selfbuilt", "large", "construction"):
            for P in u["parts"]:
                B.line(V.P(P + [P[0]]), FABRIC_EDGE, L, 15, 0.03)
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
    # bridges, conflicts, photos (v40, Aras 25 Oct 21:41: drawn marks with plain short labels, no boxes, no sentences)
    cs = list(CONFLICTS_C)
    c5 = c5_point(S)
    if c5:
        cs.append(("C5", c5[0], c5[1], C5_TEXT))
    photos = []
    try:
        photos = photo_files(os.path.join(SELINUS_RES_DIR, "_site_photos"))
    except Exception:
        LOG.append("WARNING: the site photos could not be written:\n" + traceback.format_exc())
    # v45: marks and names sized for the booklet page (K names 9 pt, C and photo numbers 7.5 pt), each name placed
    # clear of every mark and name (place_labels: on a thin leader where it must move away)
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
    for k, cx, cy, t in cs:                               # a dot in the accent
        if F.inside(cx, cy):
            px, py = V.p(cx, cy)
            B.fill([circle_pts(px, py, 0.9 * kb, 12)], MARK_C, L, 63)
            taken.append((px - 0.9 * kb, py - 0.9 * kb, px + 0.9 * kb, py + 0.9 * kb))
            labs.append(([k], px, py, hs, MARK_C))
    for i, (p, it) in enumerate(photos):                  # a small ink dot
        px, py = V.p(it["x"], it["y"])
        B.fill([circle_pts(px, py, 0.7 * kb, 12)], INK, L, 64)
        taken.append((px - 0.7 * kb, py - 0.7 * kb, px + 0.7 * kb, py + 0.7 * kb))
        labs.append(([str(i + 1)], px, py, hs, INK))
    mb = ymap - mh
    pkey = place_labels(B, labs, taken, L, bounds=(V.X0, mb, V.X0 + mw, ymap), order=65)
    # v45: scale bar and north arrow under the map, never on it; numbers 7 pt under the bar
    sbl = nice_floor(F2.w / 8.0)
    mb_crop = min(draw_scalebar_bk(B, V.X0, mb - 3.0 * kb, s, sbl, kb, L), mb - 9.5 * kb)
    draw_north_at(B, F2, V.X0 + sbl * s + 12.0 * kb, mb - 5.0 * kb, 4.0, kb, L)
    if pkey:                                              # names with no free place: a number, the words under the bar
        mb_crop = draw_label_key(B, pkey, V.X0, mb_crop - 1.0 * kb, mw, hs, L)
    # photo strip under the map
    yy = min(mb - 2.6 * U, mb_crop - 1.0 * U)
    if photos:                                        # v44: a keyword caption under each photo, numbers 12 pt
        n = len(photos)
        g = 0.6 * U
        pw = (mw - (n - 1) * g) / n
        ph = pw * 0.75
        s_ph = bk_s(mw, ph * 1.4)                         # the strip across a booklet page (row of its own)
        hc, hn = bk_h(7.5, s_ph), bk_h(12.0, s_ph)
        bn = 1.7 * hn
        low = yy - ph
        r_ph = bcite(u"Photos: site visit 2026-10-01 (group photos, GPS within {:.0f} m); the disc marks where each "
                     u"was taken. Captions: keywords of the photo index (a visual reading); Roman bridges after h01 "
                     u"§5.".format(max(it.get("gps_err_m", 0.0) for p, it in photos)))
        for i, (p, it) in enumerate(photos):
            px = V.X0 + i * (pw + g)
            B.image(p, px, yy - ph, px + pw, yy, L, order=5)
            B.fill([rect(px, yy - bn, px + bn, yy)], INK, L, 64)
            B.text(str(i + 1), px + 0.5 * bn, yy - 0.5 * bn, hn, (255, 255, 255), L, order=65,
                   font=FONT_TITLE, bold=True, align="MC")
            cap = photo_caption(it) + (u" " + r_ph if i == n - 1 else u"")
            cy_ = yy - ph - 0.6 * hc - hc
            for ln in wrap(cap, pw, hc, "sans")[:2]:
                B.text(ln, px, cy_, hc, INK, L, font=FONT_TITLE)
                low = min(low, cy_)
                cy_ -= 1.45 * hc
        crop_panel("photos", V.X0, low - 0.5 * hc, V.X0 + mw, yy, u"Site photos · 1 Oct 2026")     # v40
        yy = low - 1.2 * U
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
    if photos:
        leg.append(("pdot", INK, "Photo viewpoints 1-{}".format(len(photos))))
    leg.append(R28_STUDY_LEG)                             # v50 (G8): the study area, one name on every map
    if RF is not None:
        leg.append(("thin", INK, R28_FRAME_NAME + " (site_alan) " + r_map))   # v50 (G8): was "Analysis range"
    ly = draw_legend_items(B, leg, x, yy - 1.0 * U, mw, U, L, h=0.4)
    # v45: the booklet page's legend leaves out what the site readings beside the plan already key: the ground and
    # green colours (the land-use ring's key) and the edge types (the bars); footpaths as a line
    ring_c = set(c_ for l_, c_, a_ in landuse_slices(getattr(S, "site", S))[0])
    leg_bk, grp = [], ""
    for kind, col, lab in leg:
        if kind == "hdr":
            grp = lab
        elif not ((grp == "GROUND AND GREEN" and kind == "box" and col in ring_c) or grp.startswith("THE STREAM EDGE")):
            leg_bk.append(("line" if kind == "dash" else kind, col, lab))
    crop_panel("plan01", V.X0, mb_crop - 0.5 * kb, V.X0 + mw, ctop + ch_ + 0.3 * U, u"Plan 01 · what is there today",
               crop_scale(s), crop_legend(leg_bk))        # v40; v42: from the context line down
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
             (u"Orchards, inferred", lcc.get("orchard", ORCH_C), rest_of(S, "orchard")),
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
    """v45 (p.2: old p.4 "grain of the town" folded in): the six readings of the bank (accessible ... transformable)
    as bars, and the land use of the site frame as a ring with its key, in plan 01's colours; one panel w wide,
    designed for RD_BK_W mm beside plan 01 on the booklet page. Returns the y below. v50 (MIRAQUA 28 Oct, P02.1,
    P02.2): the ring's key on the panel's two-column grid; the stream edge diagram (draw_edge_types, its own crop
    drw_edge_types) drawn under the panel."""
    L = "LU_BOARD::SiteReadings"
    k = w / RD_BK_W
    h7, h75, h8, h9, h12 = (bk_hk(p_, k) for p_ in (7.0, 7.5, 8.0, 9.0, 12.0))
    hw = 74.0 * k                                         # each half; 8 mm between them
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
            yy = yp - 3.0 * k
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
    r1, r0 = 25.0 * k, 15.0 * k
    cx, cy = rx + 0.5 * hw, y - h8 - 1.6 * k - h7 - 4.0 * k - r1
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
    # under both: the ring's key (the plan's ground and green colours, so the plan needs no other key). v50 (MIRAQUA
    # 28 Oct, P02.1): on the panel's grid, two columns at the halves' left edges (0 and RD_BK_W - 74 mm: the grid of
    # the booklet's legend under the panel), each entry as the booklet's legend_item draws one: a 4.0 x 2.8 mm
    # swatch from 0.2 mm under the baseline, the name 5.5 mm in at 7.5 pt, 4.0 mm a row (were three columns, 7 pt)
    ky = low - 5.0 * k
    nr = (len(sl) + 1) // 2
    for j, (lab, col, a) in enumerate(sl):
        kx = x + (j // nr) * (w - hw)
        yk = ky - (j % nr) * 4.0 * k
        B.fill([rect(kx, yk - 0.2 * k, kx + 4.0 * k, yk + 2.6 * k)], col, L, 20)
        pct = 100.0 * a / ftot
        site28_fit(B, u"{} {}".format(lab, u"{:.0f}%".format(pct) if pct >= 1.0 else u"< 1%"), kx + 5.5 * k, yk, h75,
                   hw - 5.5 * k, INK, L)
    low = ky - (nr - 1) * 4.0 * k - 1.5 * k
    crop_panel("site_readings", x, low, x + w, top + 0.5 * k, u"Site readings · bank and ground")
    CROP_PANELS[-1]["bk_w"] = RD_BK_W                     # v45: its width on the booklet page (side panel of p.2) ...
    CROP_PANELS[-1]["grid"] = [0.0, RD_BK_W - 74.0]       # ... and its two halves' left edges (the legend under it)
    return draw_edge_types(S, B, x, low - 1.0 * U, w, U)  # v50 (P02.2): the stream edge alone, its own crop under it


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


def draw_edge_types(S, B, x, y, w, U):
    """v50 (MIRAQUA 28 Oct, P02.2): the stream edge alone, straightened: both banks as two bands along the stream's
    chainage (m from the upstream frame edge; no scale: a diagram), each bin coloured by its edge type in the bars'
    own colours (the same 4 m samples, SITE28_ET_BIN bins), walls and embankments as a thin strip on the water side,
    the stream between them with its covered reaches hatched and its bridges as ticks, K1-K6 as ticks across it all
    with their names under it (placed clear of each other, label_place). Its own crop (drw_edge_types), designed for
    RD_BK_W mm in p.02's side column under the site readings; words 7-8 pt. Returns the y below."""
    L = "LU_BOARD::SiteReadings"
    d = site28_edge_bins(S)
    if not d:
        LOG.append("Stream edge diagram (drw_edge_types): no bank samples or no centreline in the data pack, so not "
                   "drawn.")
        return y
    k = w / RD_BK_W
    h7, h8 = bk_hk(7.0, k), bk_hk(8.0, k)
    top = y
    B.text(u"WHERE EACH EDGE IS · BOTH BANKS, STRAIGHTENED", x, y - h8, h8, INK, L, font=FONT_TITLE, bold=True)
    yy = site28_para(B, u"chainage along the stream, m · left and right looking downstream · every 4 m, in the "
                        u"readings' colours " + bcite(EDGE_SRC), x, y - h8 - 1.6 * k - h7, w, h7, INK2, L, lead=1.45)
    lab_w = max(site28_tw(t_, h7, True) for t_ in (u"LEFT BANK", u"RIGHT BANK")) + 2.5 * k
    gx0, gx1 = x + lab_w, x + w
    sx = (gx1 - gx0) / d["L"]

    def X(s_):
        return gx0 + max(0.0, min(d["L"], s_)) * sx
    band, strip, stream = 5.5 * k, 1.2 * k, 3.0 * k
    ya = yy - 0.4 * k                                     # the chainage axis' numbers, then the bands
    yb0 = ya - 1.8 * k
    yls = yb0 - band                                      # left strip, stream, right strip, right band (tops)
    yst = yls - strip
    yrs = yst - stream
    yrb = yrs - strip
    ybot = yrb - band
    v = 0.0
    while v <= d["L"] + 1e-6:                             # the axis every 500 m, its unit on the last number
        t_ = u"{:,.0f}".format(v)
        tx = X(v) - 0.5 * site28_tw(t_, h7)
        if v + 500.0 > d["L"]:
            t_ += u" m"
        tx = min(max(tx, gx0), gx1 - site28_tw(t_, h7))
        B.text(t_, tx, ya, h7, INK2, L, font=FONT_TITLE)
        B.line([(X(v), ya - 0.5 * k), (X(v), yb0)], INK2, L, 21, bk_lw(0.15, k))
        v += 500.0
    for t_, yb_ in ((u"LEFT BANK", yb0 - band), (u"RIGHT BANK", ybot)):
        B.text(t_, x, yb_ + 0.5 * band - 0.5 * h7, h7, INK, L, font=FONT_TITLE, bold=True)
    for sd, (yt_, yb_), (st_, sb_) in ((0, (yb0, yls), (yls, yst)), (1, (yrb, ybot), (yrs, yrb))):
        B.fill([rect(gx0, yb_, gx1, yt_)], FAINT, L, 20)
        for i0, i1, t_ in site28_runs([v_[0] if v_ else None for v_ in d["bins"][sd]]):
            B.fill([rect(X(i0 * d["bm"]), yb_, X(i1 * d["bm"]), yt_)], SITE28_ET_COL.get(t_, FAINT), L, 21)
        for i0, i1, wl_ in site28_runs([v_[1] if v_ and v_[1] in SITE28_ET_WL else None for v_ in d["bins"][sd]]):
            B.fill([rect(X(i0 * d["bm"]), sb_, X(i1 * d["bm"]), st_)], SITE28_ET_WL[wl_], L, 21)
    cov_c = mix(CAT["water"][1], PAPER, 0.55)
    B.fill([rect(gx0, yrs, gx1, yst)], CAT["water"][1], L, 20)
    for a_, b_ in d["cor"].get("covered_reaches", []):
        cr_ = rect(X(a_), yrs, X(b_), yst)
        B.fill([cr_], cov_c, L, 21)
        B.hatch([cr_], SS_COVER_C, L, 22, 0.8 * k, math.radians(45.0), bk_lw(0.12, k))
    bch = d["cor"].get("bridges_ch", [])
    for i_ in range(0, len(bch) - 1, 2):                  # every bridge: a tick across the stream
        bx_ = X(0.5 * (bch[i_] + bch[i_ + 1]))
        B.line([(bx_, yls), (bx_, yrb)], INK, L, 23, bk_lw(0.3, k))
    # K1-K6: a tick across it all, the name under it
    LX, LY, LC = d["line"]
    kp = site28_project(LX, LY, LC, [(b_[2], b_[3]) for b_ in BRIDGES_K])
    items = []
    for (kk, nm_, bx, by), (s_, o_) in zip(BRIDGES_K, kp):
        if not 0.0 <= s_ <= d["L"] or abs(o_) > SITE28_K_NEAR:
            continue
        px = X(s_)
        B.line([(px, yb0 + 0.6 * k), (px, ybot - 0.6 * k)], INK, L, 24, bk_lw(0.35, k))
        t_ = u"**{}** {}".format(kk, nm_)
        wd = site28_line_w(site28_one(t_, h7), h7) / k
        items.append(dict(x=px / k, y=(ybot - 0.6 * k) / k, rank=0, t=t_, wh=(lambda f, wd=wd: (wd * f + 0.8,
                                                                                               1.5 * h7 / k * f))))
    taken = [(x / k, (ybot - 0.4 * k) / k, (x + w) / k, (ya + h7) / k)]
    got = place_labels_all(items, taken, bounds=(x / k, (ybot - 16.0 * k) / k, (x + w) / k, (ybot - 0.4 * k) / k),
                           sizes=(1.0,))
    low = ybot - 1.0 * k
    for i, (bx, lead, f) in got.items():
        it = items[i]
        e = lp_leader_end(bx, (it["x"], it["y"]))
        B.line([(it["x"] * k, it["y"] * k), (e[0] * k, e[1] * k)], INK2, L, 24, bk_lw(0.15, k))
        site28_text(B, it["t"], (bx[0] + 0.4) * k, bx[1] * k + 0.3 * h7, h7, INK, L)
        low = min(low, bx[1] * k)
    # the key: the edge types in the bars' colours, walls, embankments, the covered stream, bridges
    ky = low - 2.5 * k - h7
    kx = x
    keys = [(SITE28_ET_COL[t_], t_w) for t_, t_w in SITE28_ET_KEY] + [(SITE28_ET_WL[1], u"walled"),
                                                                       (SITE28_ET_WL[2], u"embanked"),
                                                                       (CAT["water"][1], u"stream"),
                                                                       (None, u"covered stream"), (INK, u"bridge")]
    for col_, t_ in keys:
        iw = 5.5 * k + site28_tw(t_, h7)
        if kx > x and kx + iw > x + w:
            kx, ky = x, ky - 4.0 * k
        sw_ = rect(kx, ky - 0.2 * k, kx + 4.0 * k, ky + 2.6 * k)
        if t_ == u"bridge":
            B.line([(kx + 2.0 * k, ky - 0.4 * k), (kx + 2.0 * k, ky + 2.8 * k)], INK, L, 24, bk_lw(0.35, k))
        elif col_ is None:
            B.fill([sw_], cov_c, L, 21)
            B.hatch([sw_], SS_COVER_C, L, 22, 0.8 * k, math.radians(45.0), bk_lw(0.12, k))
        else:
            B.fill([sw_], col_, L, 21)
        B.text(t_, kx + 5.5 * k, ky, h7, INK, L, font=FONT_TITLE)
        kx += iw + 3.5 * k
    low = ky - 1.5 * k
    crop_panel("edge_types", x, low, x + w, top + 0.5 * k, u"The stream edge · both banks, straightened")
    CROP_PANELS[-1]["bk_w"] = RD_BK_W                     # its width on the booklet page (p.02's side column) ...
    CROP_PANELS[-1]["grid"] = [0.0, RD_BK_W - 74.0]       # ... on the site readings' grid
    LOG.append("Stream edge diagram (drw_edge_types): {:,.0f} m of the bars' {:,.0f} m of bank lie within {:.0f} m of "
               "the stream's centreline and are drawn ({} bins of {:.0f} m a bank).".format(
                   d["used"], d["tot"], SITE28_ET_NEAR, d["n"], d["bm"]))
    return low - 1.0 * U


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
    for did, fn in (("S1", "Selinus_01_what_is_there_axonometric.pdf"),):
        t0 = time.time()
        ext = ctx.extents[0]
        try:
            spec = DG["SPECS"][did](ctx, ext)
            pg, st = DG["compose"](ctx, spec, ext, stamp)
            p = os.path.join(pdf_folder(), fn)
            DG["write_pdf"]([pg], p)
            out.append((p, time.time() - t0))
            bx, ph = DG["BOX"], DG["PAGE_H"]                 # v40: the booklet crop: the page between the rules (the
            bx = (0.0, bx[1], DG["PAGE_W"], bx[3])            # callouts may sit beyond the drawing box, left and right)
            leg = [(("dot", DG["TREE_STYLES"].get(c_, DG["TREE_STYLES"]["tree"])["mid"]) if k_ == "tree" else (k_, c_))
                   + (t_,) for k_, c_, t_ in spec["legend"]() if c_ is not None]
            CROP_DIRECT.append(("axo_what_is_there", fn, (bx[0], ph - bx[3] - 4.0, bx[2], ph - bx[1] + 4.0),
                                u"What is there · heights, heritage, water, green", None, crop_legend(leg), []))
        except Exception:
            LOG.append("WARNING: the {} axonometric failed:\n{}".format(did, traceback.format_exc()))
    LOG.extend(u"Axonometric engine: " + m for m in DG["LOG"])
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
