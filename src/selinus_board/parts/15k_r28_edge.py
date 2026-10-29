# ---- MIRAQUA round 28 Oct 2026 (site board v50): p.06/p.22 the stream edge and where we can build, p.16 shade strip, P06.3, the open-to-change export (worker SB-edge). Shared pieces: parts/15h_r28_shared.py,
# common/r28_style.py, common/units.py, common/label_place.py, common/figures.py (revision_2026-10-28/PLAN.md).
# v50 (MIRAQUA 28 Oct, P06.1-P06.4, P22.1, D1, G3-G8, G13; worker SB-edge). Every drawing here is ONE strip of the
# whole analysis frame at 1:10,000 on the booklet page, on the frame's own axis (G7: 284.5 x 52.9 mm; 1:5,000 would
# need 569 mm), with the study area's outline (G8) and its scale bar and north arrow under it, never on it:
#   * p.06 drw_edge_build: the strip; THE EDGE and WHERE WE CAN BUILD beside it; the map's key under it (it holds the
#     hatches and outlined fills the booklet's legend cannot draw); the eight photos in the height the second strip
#     left (P06.4). p.22 drw_edge_build_e: the same strip without photos (P22.1).
#   * P06.1 context: street names (OpenStreetMap: the main streets first, then the longest named), mahalle names
#     (OpenStreetMap boundary=administrative, admin_level 8), heritage names (the buildings' own names, then named
#     heritage points), bridge names (BRIDGES_K), the survey's 5 m contours (10 m bolder), the study area; placed by
#     common/label_place.py (G4): bridge and stream names always, the others dropped where nothing is free (logged).
#   * P06.2 where we can build: vector hatches in R28_BUILD_HATCH over a light tint of their colour; the loose ground
#     is drawn from the very cells frame_rest counts (S.rest_rows), traced into outlines, simplified (Douglas-Peucker),
#     smoothed (Chaikin) and scaled back to the traced area; the satellite trees and fields are smoothed the same way.
#     Every printed area still comes from the count (ground_open): the drawing moves no figure.
#   * P06.3: buildings in R28E_BLD, darker than the streets, filled by the nonzero rule (r28_nz: overlapping outlines
#     no longer print white); OpenStreetMap footprints with a thin outline; both in the key.
#   * D1: r28_open_to_change.json (r28e_export_open) and the filter sheet drw_filter (r28e_draw_filter): analysis frame
#     -> open ground (the masterplan's r28_open_ground.json) -> of which open to change, and why.
#   * p.16 drw_shade_strip (draw_shade_strip): its rows laid along the frame's axis at 1:10,000, the study area marked.
# Labels and notes are measured with r28mv_tw and set with r28mv_lines / r28mv_para (parts/15i_r28_movement.py).
R28E_DEN = B_DEN                 # 1:10,000 on the booklet page (the theme-B maps' scale)
R28E_SB_M = B_SB_M               # m: the scale bar under each strip, four parts of 100 m
R28E_GAP = BK_GAP_MM             # mm between a strip and the column beside it
R28E_BLD = mix(MPL["bld"], C(R28_OPEN["building"]), 0.45)   # P06.3: A7A299, dE00 about 11 to the streets (was 2.3)
R28E_OSM_EDGE = mix(R28E_BLD, INK, 0.6)                    # P06.3: the thin outline of an OpenStreetMap footprint
R28E_HER_TXT = C(dict((k_, h_) for k_, n_, h_ in R28_MARKERS)["heritage"])   # heritage names (R28 "heritage and views")
R28E_CONTOUR = mix(INK2, WHITE, 0.5)                       # P06.1: contours, light (G6)
R28E_CONTOUR_W = (0.07, 0.13)    # mm: a 5 m and a 10 m contour on the booklet page
R28E_DP_M = (4.0, 2.0)           # m: Douglas-Peucker tolerances tried in turn on a raster outline (steps of 2-10 m) ...
R28E_DP_FINE = 0.3               # m: ... and once more after the corner cutting (fewer points, the same curve)
R28E_CHAIKIN = 2                 # corner-cutting rounds
R28E_SHAPE = 0.25                # the most a ring's area may change before it is scaled back (else the next tolerance)
R28E_MIN_A = 30.0                # m2: smaller rings stay as traced (0.5 mm across at 1:10,000)
R28E_TINT = 0.86                 # a hatch's ground: its line colour this far to white (G6: light)
R28E_HATCH_MM = (1.0, 0.12)      # mm: hatch spacing and line weight on the booklet page
R28E_HATCH = dict((k_, (lab_, C(hx_), ang_)) for k_, lab_, hx_, ang_ in R28_BUILD_HATCH)
R28E_KEYS = (("vacant", "open"), ("parking", "parking"), ("loose", "loose"))   # ground_open's parts -> hatch keys
R28E_N_HER, R28E_N_STREET = 8, 6     # heritage and street names at most (G4 may drop some of them)
R28E_STREET_MIN = 150.0          # m: a named street runs at least this far inside the frame
R28E_MAH_MIN = 20000.0           # m2: a mahalle named on the strip has at least this much ground inside the frame
R28E_OPEN_JSON = os.path.join(SELINUS_RES_DIR, "r28_open_to_change.json")    # D1: the polygons and figures p.06 prints
R28E_MP_JSON = "r28_open_ground.json"    # D1: the masterplan's open ground, next to its masterplan_results.json


class R28NZ(tuple):
    """v50 (MIRAQUA 28 Oct, P06.3): a fill colour the PDF fills by the nonzero winding rule (_pdf_page: "f", not
    "f*"): overlapping building outlines stay filled (even-odd printed their overlap white); courtyards turn the other
    way round (add_unit in 03_street_w.py) and stay open. Rhino bakes it as the plain colour."""
    nz = True


class R28NZTint(Tint):
    """v50 (P06.3): a multiplying Tint (15f) filled by the nonzero rule"""
    nz = True


def r28_nz(c):
    """v50 (P06.3): colour c filled by the nonzero rule (a Tint stays a multiplying Tint)"""
    if getattr(c, "nz", False):
        return c
    return R28NZTint(c) if getattr(c, "mul", False) else R28NZ(c)


def r28e_memo(S):
    """the run's memo of this part (traced and smoothed outlines, names, the export), kept on the site model"""
    m = getattr(S, "_r28e", None)
    if m is None:
        m = S._r28e = {}
    return m


# ------------------------------------------------------------ P06.2: raster outlines as smooth vector rings
def r28e_dp_ring(P, tol):
    """Douglas-Peucker on a closed ring: cut at its first point and the point farthest from it, both kept"""
    n = len(P)
    if n < 4:
        return list(P)
    x0, y0 = P[0]
    j = max(range(n), key=lambda i: (P[i][0] - x0) ** 2 + (P[i][1] - y0) ** 2)
    if j == 0:
        return list(P)
    return dp_simplify(P[:j + 1], tol)[:-1] + dp_simplify(P[j:] + [P[0]], tol)[:-1]


def r28e_smooth(P):
    """P06.2: a raster outline as a smooth vector ring: Douglas-Peucker (the first tolerance of R28E_DP_M that keeps
    the area within R28E_SHAPE), Chaikin corner cutting (R28E_CHAIKIN rounds), Douglas-Peucker once more
    (R28E_DP_FINE), then scaled about its centroid back to the area it had (holes too, so drawing and count agree);
    rings under R28E_MIN_A stay as they are"""
    P = [(float(p[0]), float(p[1])) for p in P]
    if len(P) > 3 and P[0] == P[-1]:
        P = P[:-1]
    A0 = signed_area(P)
    if len(P) < 4 or abs(A0) < R28E_MIN_A:
        return P
    for tol in R28E_DP_M:
        Q = r28e_dp_ring(P, tol)
        if len(Q) < 3:
            continue
        Q = r28e_dp_ring(chaikin_closed(Q, R28E_CHAIKIN), R28E_DP_FINE)
        A1 = signed_area(Q) if len(Q) >= 3 else 0.0
        if A1 * A0 <= 0.0 or abs(A1 / A0 - 1.0) > R28E_SHAPE:
            continue
        a_, cx, cy = shoelace(Q)
        f = math.sqrt(A0 / A1)
        return [(cx + (x - cx) * f, cy + (y - cy) * f) for x, y in Q]
    return P


def _r28e_turn(d, e):
    """the turn from direction d to direction e on the cell grid: 0 left, 1 straight on, 2 right, 3 back"""
    if e == (-d[1], d[0]):
        return 0
    if e == d:
        return 1
    if e == (d[1], -d[0]):
        return 2
    return 3


def r28e_trace(rows):
    """P06.2: the outlines of a raster mask (rows of bits as frame_rest's: bit a of row j = cell a, j) in cell
    corners (a, j): outer rings anticlockwise, holes clockwise; cells that touch only at a corner make separate
    rings (the left turn first where two outlines meet in a point); straight-through corners left out"""
    out = {}
    ny = len(rows)
    for j in range(ny):
        m = rows[j]
        if not m:
            continue
        below = rows[j - 1] if j > 0 else 0
        above = rows[j + 1] if j + 1 < ny else 0
        for bits, kind in ((m & ~below, 0), (m & ~above, 1), (m & ~(m >> 1), 2), (m & ~(m << 1), 3)):
            while bits:
                b = bits & -bits
                a = b.bit_length() - 1
                bits ^= b
                if kind == 0:                             # bottom side, eastwards (the cell on the left)
                    s, e = (a, j), (a + 1, j)
                elif kind == 1:                           # top side, westwards
                    s, e = (a + 1, j + 1), (a, j + 1)
                elif kind == 2:                           # right side, northwards
                    s, e = (a + 1, j), (a + 1, j + 1)
                else:                                     # left side, southwards
                    s, e = (a, j + 1), (a, j)
                out.setdefault(s, []).append(e)
    rings = []
    while out:
        s0 = next(iter(out))
        lst = out[s0]
        e = lst.pop()
        if not lst:
            del out[s0]
        ring, prev, cur = [s0], s0, e
        while cur != s0:
            ring.append(cur)
            lst = out.get(cur)
            if not lst:                                   # never expected: every corner has as many ways in as out
                break
            d = (cur[0] - prev[0], cur[1] - prev[1])
            nxt = lst[0] if len(lst) == 1 else min(lst, key=lambda q: _r28e_turn(d, (q[0] - cur[0], q[1] - cur[1])))
            lst.remove(nxt)
            if not lst:
                del out[cur]
            prev, cur = cur, nxt
        n = len(ring)
        keep = [ring[i] for i in range(n)
                if (ring[i][0] - ring[i - 1][0]) * (ring[(i + 1) % n][1] - ring[i][1]) !=
                (ring[i][1] - ring[i - 1][1]) * (ring[(i + 1) % n][0] - ring[i][0])]
        if len(keep) >= 4:
            rings.append(keep)
    return rings


def r28e_groups(rings):
    """outer rings (anticlockwise) each with the holes (clockwise) inside it: [[outer, hole, ...], ...], so that a
    fill or hatch drawn group by group never loses a hole"""
    outs, hols = [], []
    for P in rings:
        a_ = signed_area(P)
        if a_ > 0.0:
            outs.append((a_, P))
        elif a_ < 0.0:
            hols.append(P)
    grp = [[P] for a_, P in outs]
    if hols and outs:
        g = Grid(60.0)
        for i, (a_, P) in enumerate(outs):
            g.add(i, bb_pts(P))
        for H in hols:
            x, y = interior_point(H)
            best = None
            for i in g.query((x, y, x, y)):
                if (best is None or outs[i][0] < outs[best][0]) and pip(x, y, outs[i][1]):
                    best = i
            if best is not None:
                grp[best].append(H)
    return grp


def r28e_lc(S, key):
    """P06.2: a satellite class (S.lc[key]: WorldCover 10 m pixel outlines) smoothed (r28e_smooth) and grouped"""
    m = r28e_memo(S)
    if ("lc", key) not in m:
        m[("lc", key)] = r28e_groups([r28e_smooth(P) for P in (getattr(S, "lc", None) or {}).get(key) or []])
    return m[("lc", key)]


def r28e_loose(S):
    """P06.2: the loose ground as frame_rest counts it (grass or shrub cells of the frame's unmapped ground on the
    REST_CELL raster, S.rest_rows) as smooth outlines, grouped: [[outer, holes ...], ...] in survey m"""
    m = r28e_memo(S)
    if "loose" in m:
        return m["loose"]
    rr = getattr(S, "rest_rows", None) or {}
    g_, s_ = rr.get("grass") or [], rr.get("shrub") or []
    mask = [(g_[j] if j < len(g_) else 0) | (s_[j] if j < len(s_) else 0) for j in range(max(len(g_), len(s_)))]
    F, c = S.F, REST_CELL
    raw = [[F.world(F.u0 + a * c, F.v0 + j * c) for a, j in R_] for R_ in r28e_trace(mask)]
    sm = [r28e_smooth(P) for P in raw]
    m["loose"] = r28e_groups(sm)
    LOG.append(u"Where we can build (P06.2): the loose ground's {:,} raster cells traced into {:,} outlines ({:.2f} ha "
               u"traced, {:.2f} ha drawn after smoothing); the figure printed is the count, {:.2f} ha.".format(
                   sum(bin(r_).count("1") for r_ in mask), len(raw), sum(signed_area(P) for P in raw) / 1e4,
                   sum(signed_area(P) for P in sm) / 1e4, rest_of(S, "grass", "shrub") / 1e4))
    return m["loose"]


def r28e_open_groups(S):
    """P06.2: the ground open to change as drawn, by ground_open's parts: {"vacant", "parking": the mapped zones
    (outlines with their holes), "loose": r28e_loose}"""
    m = r28e_memo(S)
    if "open" not in m:
        m["open"] = {"vacant": [z["Ps"] + z["Hs"] for z in S.zones if z["kind"] == "vacant"],
                     "parking": [z["Ps"] + z["Hs"] for z in S.zones if z["kind"] == "transport"],
                     "loose": r28e_loose(S)}
    return m["open"]


def r28e_hatched(CB, V, groups, key, k, L, order, fill=True):
    """P06.2: one part of where we can build (key of R28_BUILD_HATCH): the light tint of its colour (fill=False:
    none) and its hatch, R28E_HATCH_MM apart and wide on the booklet page at its angle (vector lines), group by group"""
    lab, col, ang = R28E_HATCH[key]
    chunk = []
    for i, g in enumerate(groups):
        chunk.extend(g)
        if len(chunk) >= 400 or i == len(groups) - 1:
            Ps = V.Ps(chunk)
            if fill:
                CB.fill(Ps, mix(col, WHITE, R28E_TINT), L, order)
            CB.hatch(Ps, col, L, order + 1, R28E_HATCH_MM[0] * k, math.radians(ang), bk_lw(R28E_HATCH_MM[1], k))
            chunk = []


# ------------------------------------------------------------ P06.1: contours and names
def r28e_contours(R, F):
    """P06.1 (called by build_site, so kept with the site model): the survey's contours inside the frame,
    [(10 m line, polyline)], every 5 m, simplified to 0.5 m. A line's height = the median of its points' heights; a
    line without heights counts by its layer (EGRI_10M, EGRI_5M); other heights are left out."""
    out = []
    for lay in DWG["contours"]:
        for P in (R.get("plines") or {}).get(lay, []):
            if len(P) < 2:
                continue
            zs = sorted(p[2] for p in P)
            z = zs[len(zs) // 2]
            if z > 0.5:
                if abs(z / 5.0 - round(z / 5.0)) > 0.01:
                    continue
                major = abs(z / 10.0 - round(z / 10.0)) < 0.006
            elif lay in ("EGRI_10M", "EGRI_5M"):
                major = lay == "EGRI_10M"
            else:
                continue
            for run in F.clip_line([(p[0], p[1]) for p in P]):
                out.append((major, dp_simplify(run, 0.5)))
    return out


# ------------------------------------------------------------ the strip and its base
def r28e_base(S, CB, V, k, L):
    """v50 (P06.1-P06.3, replaces draw_eb_base): the stream edge plan's base through ClipB CB, crisp, in the
    masterplan's tones and layer order: satellite trees and fields (smoothed), mapped parks, woods and fields, where
    we can build (vector hatches), contours, street surfaces, the stream and its edge, the covered course,
    buildings (R28E_BLD, nonzero; heritage with its edge, OpenStreetMap footprints with a thin outline), bridges,
    street edges, the study area (G8). The ground (white) is the caller's."""
    for key, col in (("trees", MPL["tree"]), ("farmland", MPL["field"]), ("orchard", MPL["field"])):
        fill_units(CB, V, r28e_lc(S, key), col, L, 3)
    for z in S.zones:
        if z["kind"] in ("green", "agri"):
            CB.fill(V.Ps(z["Ps"] + z["Hs"]), MPL["field"] if z["kind"] == "agri" else (
                MPL["tree"] if z.get("sub") == "wood" else MPL["park"]), L, 4)
    og = r28e_open_groups(S)
    for part, hk in R28E_KEYS:
        r28e_hatched(CB, V, og[part], hk, k, L, 6)
    for major, P in getattr(S, "contours", None) or []:
        CB.line(V.P(P), R28E_CONTOUR, L, 8, bk_lw(R28E_CONTOUR_W[1 if major else 0], k))
    for rg_ in getattr(S, "road_net", None) or []:
        CB.fill(V.Ps([rg_["P"]] + rg_["H"]), MPL["road"], L, 10)
    for wt in S.water:
        CB.fill(V.Ps([wt["P"]] + wt.get("H", [])), MPL["water"], L, 15)
    for P in getattr(S, "water_outline", []) or []:
        CB.line(V.P(P), MPL["water_edge"], L, 16, bk_lw(0.18, k))
    for q in getattr(S, "decks", []) or []:               # streets on decks over the water stay above it
        CB.fill([V.P(q)], MPL["road"], L, 17)
    for P in getattr(S, "covered", []) or []:             # the covered course under streets and roofs
        for d in dashes(V.P(P), 1.6 * k, 0.9 * k):
            CB.line(d, MPL["water_edge"], L, 18, bk_lw(0.3, k))
    her = lambda u: u.get("fabric") in ("monument", "sacred")
    mini_buildings(S, CB, V, L, lambda u: MPL["her"] if her(u) else R28E_BLD, order=20)
    for u in S.bld:
        if her(u):
            for P in u["parts"]:
                CB.line(V.P(list(P) + [P[0]]), MPL["her_edge"], L, 21, bk_lw(0.12, k))
        elif u.get("src") in ("osm", "osm+label"):        # P06.3: a footprint the survey does not have
            for P in u["parts"]:
                CB.line(V.P(list(P) + [P[0]]), R28E_OSM_EDGE, L, 21, bk_lw(0.08, k))
    for P in getattr(S, "bridges", []) or []:
        CB.line(V.P(P), MPL["ink_dark"], L, 25, bk_lw(0.3, k))
    for P in getattr(S, "road_lines_net", []) or []:
        CB.line(V.P(P), MPL["road_edge"], L, 30, bk_lw(0.12, k))
    for r_ in S.roads:
        if not r_.get("w"):
            CB.line(V.P(r_["P"]), MPL["road_edge"], L, 30, bk_lw(0.12, k))
    draw_r28_study(S, CB, V, k, L)


