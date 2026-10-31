# p.12 the water system (split from code.py on 29 Oct 2026). v5 (revision 29 Oct 2026, T3b WO-T3b-2, package C items
# 1-4): ONE diagrammatic map replaces the chain ribbon, the storage cubes and the cleaning tiles. An axonometric of the
# site (the shared basemap, survey m -> page through _p12_axo) carries the project's verbs where they happen (collect,
# clean, hold, give back, to the farms; idea of R03), the volumes and yearly flows as figures on the drawing (R04; read
# live from water_balance_results.json = WB, never typed in), the programme as icons along the strip (R05, icons.py)
# and ONE circular zoom: the upstream entry as a PLAN at 1:2,000 with its scale bar and north arrow (not a perspective).
# Positions come only from project data: the Option A zones and water links of the zone base (the water balance v6
# writes them to its results, key "zones"), the Selinos line and the four places of P12_PLACES. What the map makes
# redundant is gone (the cubes, the IN/OUT lines, the tiles); what stays sits beside it (G7): the logic in five rows,
# the coliform chart, the plants' removal bars (D2, D6), why we clean, one short conclusion.
# v6 (revision 30 Oct 2026, T7, brief PG4 p11): the map is a true 3D object: the stream sunk in its channel by the
# registry levels (walls, water at average flow, the summer strip as the low-flow channel: no mid-stream squiggle,
# no dashed centre line), streets, fields, parks and tree cover as a canopy texture, buildings as volumes at their
# survey heights (M11), the zones' trees in 3D at species heights (M6), a legend (M2); the axo turns to the largest
# scale. The round plan zoom is replaced by an up-close SECTION of the upstream entry (G10: people, use, materials;
# D1: style a above the map, style b below it, crops wb_system_a / wb_system_b / wb_system). The logic block went.
# v9 (Aras 31 Oct, booklet p11): one up-close band at the bottom in style a (crop wb_system); buildings as volumes only
# near the stream (P12_BLD_NEAR_M) and heritage, the rest as faint footprints, so the city reads.
# R2-C (31 Oct, PG4 p11 #6-8): the map keeps only the five numbered step markers (leader-free) and short place names,
# the steps' texts and figures moved to the column's key (G3: the upstream entry was crowded); the up-close band gets
# the designed sky (D8), back trees on a ground dipping into the channel (G14), mixed planting groups on depth
# layers (G9), people by zone (G10), callouts "Element: reason" with one per planting group.
# v12 (round 3, booklet p11, B2 helper p11; spec handover/B2_work/spec_p11.md): the map stands on the real relief
# (P11.1, N3: survey contours inside the frame, Copernicus GLO-30 outside it, bias-matched and blended; stepped,
# shaded ground; everything draped on it); the upstream entry (the blue box) re-drawn in a zoom with steps 1-4 and the
# winter store's definition (P11.2); the project along the channel as letters B, C, D ... with a key, the reaches
# without an element flagged (P11.3, G18); water textured in its channel, no summer strip in plan (P11.4, D2); fields
# as one texture and one symbol each (P11.5); no leaders (G3), no alpha, species colours (G9), clipped to land and
# logged draw order (G8), real names (G16), no borders (G17); the up-close band with birds, levels, cut-end names,
# a zoom of the reed basins (G15).

P12_TITLE = u"CLEANED ONCE, HELD OVER WINTER, GIVEN BACK CLEAN TO THE FARMS · one way, with the stream"

# the Selinos line, survey m, upstream first: agriculture data/GEO.py "selinos" as proposal sections PS_KEY_SELINOS,
# thinned to 2 m (Douglas-Peucker); only the flow direction and the arrows use it (the water itself is the basemap's)
P12_SELINOS = [
    (29642.6, 32739.4), (29633.1, 32660.6), (29643.3, 32638.1), (29671.3, 32612.4), (29710.7, 32540.0),
    (29769.1, 32480.8), (29784.7, 32450.4), (29789.1, 32431.9), (29777.7, 32369.0), (29781.7, 32325.3),
    (29795.2, 32299.4), (29822.6, 32279.6), (29865.9, 32271.5), (29920.8, 32274.0), (29974.1, 32261.0),
    (29985.8, 32252.3), (30000.2, 32215.9), (30005.5, 32176.9), (30022.8, 32126.7), (30052.7, 32087.9),
    (30148.1, 31931.0), (30200.4, 31867.1), (30275.6, 31802.4), (30345.9, 31706.8), (30378.4, 31640.0),
    (30405.5, 31555.5), (30444.1, 31464.0), (30493.0, 31382.7), (30593.4, 31294.4), (30682.7, 31240.2),
    (30753.5, 31180.3), (30833.2, 31152.0), (30935.6, 31090.4), (30987.4, 31044.7), (31015.8, 31010.8),
    (31137.6, 30847.4), (31154.8, 30764.8), (31158.1, 30761.4), (31242.2, 30700.3), (31308.9, 30668.1),
    (31393.4, 30634.5)]
# the four places of the project's chain, survey m: the upstream entry and downstream reach = the surveyed cut centres
# (masterplan parts/02b_detail.py CUT_AT = water board CUTS); K4, K5 = the bridges (site board BRIDGES_K). v12 (G16):
# a bridge by its code only (an internal key, read by p17_planting too): the page prints bridge_name(code)
P12_PLACES = [(u"Upstream entry", (29693.022, 32569.176)), (u"K4", (29846.40, 32277.71)),
              (u"K5", (30293.63, 31792.25)), (u"Downstream end", (30991.856, 31039.404))]
P12_ROTS = tuple(range(-40, 41, 4))  # v6: the plan's candidate turns (deg); the one giving the largest map scale wins
P12_SIN, P12_COS = 0.62, 0.785       # ... seen from 38 deg above (depth x sin, heights x cos; one scale)
P12_W_CUTS = ("W1", "W2", "W3", "W4", "W5")   # the registry cuts whose bank tops and average flow sink the stream
P12_HER_COLS = dict(wall_lit="F7EEED", wall_shade="E6D2D1", roof_lit="EEDCDB", roof_shade="D8BFBE",
                    axo_line="AF7474")   # heritage volumes: buildings.py her_fill / her_edge, lit and shaded
P12_ZONE_MIX = {"WP": None, "GR": None, "DG": ["olive", "rosemary", "lavender"]}   # zones planted on the map (G9)
P12_BAND_M = 60.0                    # m: the wet-to-dry band away from the Selinos line (drawing rule, as p.16)
P12_TREE_STY = {"olive": "olive", "stone_pine": "pine"}   # core TREE_STYLES per species (else "tree")
P12_CANOPY_M = 6.0                   # m: the tree-cover texture's cluster spacing (drawing rule)
P12_CANOPY_CAP = 6000                # most clusters drawn (PDF size)
P12_K5_CHECK_M = 200.0               # m: the base-data check around Üç Kemer (logged; its names drawn)
P12_K5_NAMES = 3                     # names of the base data drawn around K5 at most (v12: few labels, G3)
P12_ZOOM_H = 48.0                    # mm: the up-close section band (v9: one band, style a, below the map)
P12_BLD_NEAR_M = 60.0                # v9 (Aras 31 Oct): buildings drawn as volumes only this close to the Selinos line
#                                      (m, drawing rule; heritage always); the rest as flat footprints
P12_BLD_FAR = ("E4E0D9", 0.45)       # the far footprints: fill, mixed this far toward white (v12: opaque, no edge)
P12_ZOOM_GAP = 5.0                   # mm between the band and the map
P12_ZOOM_KEY_W = 70.0                # mm: the band's key column (title, callouts; R2: water and scale bar right)
P12_ZOOM_DEN = 500                   # the up-close section at 1:500 (D6 standard scale)
P12_ZOOM_BAR = (0, 5, 10, 20)        # its scale bar marks, m
P12_ZOOM_CUT = "W1"                  # the registry cut whose levels it draws (the upstream entry)
P12_ZOOM_BANK_M = 12.0               # m of the far bank kept beyond the stream (drawing rule)
P12_WALL_T = 0.50                    # m: the channel wall drawn in cut (drawing rule: the data gives no thickness)
P12_KERB_H = 0.15                    # m: reed cell kerb over the ground (drawing value, as p.13 and p.22)
P12_BASIN = (5.0, 1.5, 0.90, 0.50, 0.65)   # reed cell length, gap, floor under the rim, media, water over the floor
#                                            (m; drawing values, as p.22 P24_BASIN)
P12_ZOOM_TEXT = {"WT": u"Reed basins, lined: clean the stream once",      # R2: "Element: reason" (shared style)
                 "WD": u"Spillway: clean water back to the stream",
                 "GR": u"Shaded walk: a bench in the trees' shade, lit at night",
                 "WS": u"Dry-top terraces: play over the winter store",
                 "WP": u"Streamside planting: fed by the clean stream",
                 "DG": u"Demeter's garden: olives and aromatics",
                 "WA": u"Flood terraces: high water spreads here",
                 "wall": u"Stone walls: the walled town reach, kept",
                 "strip": u"Summer strip: water in the bed all summer"}
P12_COL_W = 112.0                    # the column beside the map, mm
P12_ZOOM_LEG_W = 52.0                # R2: mm at the band's right for the water legend and the scale bar (the callout
#                                      key takes the whole left column: one line per element and planting group)
P12_GROUP_DO = {"shade": u"shade", "wind": u"break the wind", "noise": u"soften the noise",
                "corridor": u"green corridor", "cleaning": u"clean the water", "perception": u"colour and scent"}
#                                      R2 (G9): what a planting group does, from plants.py's purpose tags (sure only)
P12_ZONE = {"WS": MP["storage"], "WT": MP["wetland"], "WD": MP["discharge"], "GR": MP["park"],
            "WA": MP["amphibious"], "WP": ("ABBBAE", "748878", "3B4D3F"), "DG": MP["agriculture"]}
P12_STEP_COL = {1: MP["discharge"][1], 2: MP["wetland"][2], 3: MP["storage"][2], 4: MP["discharge"][2],
                5: MP["agriculture"][2]}
P12_MAP_MARG = (12.0, 16.0, 16.0, 12.0)   # mm kept free round the map's key points (left, right, bottom, top)
# v12 (round 3, P11.1, N3 merged): the relief. Inside the analysis frame the survey contours (basemap.json layers
# "contours"), outside it Copernicus GLO-30 (Data/bergama_dem_glo30.json; research/elevation_2026-10-31/README.md),
# shifted by the median survey - GLO-30 difference along the frame edge and blended into the survey over 60 m
P12_DEM_FILE = "bergama_dem_glo30.json"
P12_DEM_BLEND_M = 60.0               # m: the blend band outside the frame (the merge rule)
P12_DEM_EDGE_M = (20.0, 10.0)        # m: the bias samples along the frame edge, and how far inside it (the merge rule)
P12_DEM_BUCKET = 25.0                # m: the contour vertex index cell (drawing rule)
P12_DEM_SEARCH = 16                  # index cells searched at most round a point for its contours (400 m)
P12_RELIEF_CELL_MM = 1.6             # mm: a ground cell on the page (drawing rule)
P12_RELIEF_CELL_M = (3.0, 40.0)      # m: the ground cell's least and largest size
P12_RELIEF_PAD_M = 150.0             # m: the ground grid reaches this far beyond the drawn box
P12_RELIEF_BAND_M = 5.0              # m: the height steps of the ground tone (the stepped relief)
P12_ZX = (0.5, 2.0, 0.6, 0.12)       # the ground's lift (a diagram: free scale): least and most exaggeration, the
#                                      steepest lifted slope allowed (no fold: < the view's 0.79), the share of the
#                                      map's height the lift may take
P12_GROUND = dict(low="EFEDE6", high="B0AC9C", high_t=0.35, lit="FFFFFF", lit_t=0.25, shade="8E8F8A", shade_t=0.30,
                  steps=5, step=0.06)  # palette paper -> structure by height; lit toward white, shade toward 8E8F8A
P12_CONTOUR = (("847E75", 0.5, 0.035), ("847E75", 0.0, 0.06))   # the 5 m and 25 m contours: ink, mix to paper, mm
P12_INSET = (92.0, 64.0)             # mm: the map's zoom of the upstream entry (the blue box, P11.2)
P12_MARK_R = 1.6                     # mm: the radius of a letter marker (P11.3, G18)
P12_LETTERS = u"BCDEFGHJKLMNPQRSTUVWXYZ"   # the project's letters (P11.3): no A (the section's A-A'), no I/O (1/0)
P12_DEF_NEAR_M = (40.0, 15.0, 10.0, 60.0, 150.0)   # m: a zone this near the Selinos line defines it; the strip; the
#                                      station step; the shortest reach counted; the shortest strip reach marked
P12_DEF = {"WA_bed": u"Amphibious bed: floods with the water level",
           "GR_dry": u"Raised dry top: dry ground above the flood terraces",
           "stream": u"Selinos stream kept as it runs: no work in this reach"}
#                                      the zones' roles: bergama_zone_base/code.py l.20-36 (GR 2-3 "raised dry top",
#                                      WA "bed" / "flood terrace"); palette MASTERPLAN "amphibious" (floods with the level)
P12_ORCHARD = ("8C9969", "727A4E", "B1BA97", "5B5147")   # the generic orchard tree: crown, shade, light, trunk
#                                      (TREE_STYLES "tree"; the land cover's crop is not sourced: no species)
P12_FIELD_MM = (1.0, 0.08, 30.0, 4.0)   # field rows: spacing mm, pen mm; least patch (mm²) with a symbol; symbol mm
P12_ZOOM_SPOT = (20.0, 2.5)          # the band's zoom of the reed basins: spot width mm, enlargement (G15)
_P12_MEMO = {}                       # one run's ground model, drops, trees, tree styles


# ---------------------------------------------------------------- small geometry (page mm unless said)
def _p12_get(*path):
    """a value of the water balance results (WB) by its keys, None when it is not there"""
    d = WB
    for k in path:
        try:
            d = d[k]
        except (KeyError, IndexError, TypeError):
            return None
    return d


def _p12_area(R):
    return abs(sum(R[i][0] * R[(i + 1) % len(R)][1] - R[(i + 1) % len(R)][0] * R[i][1] for i in range(len(R)))) / 2.0


def _p12_cen(R):
    """the area centroid of a ring"""
    a = cx = cy = 0.0
    n = len(R)
    for i in range(n):
        (xa, ya), (xb, yb) = R[i], R[(i + 1) % n]
        f = xa * yb - xb * ya
        a += f
        cx += (xa + xb) * f
        cy += (ya + yb) * f
    if abs(a) < 1e-9:
        return (sum(p[0] for p in R) / n, sum(p[1] for p in R) / n)
    return (cx / (3.0 * a), cy / (3.0 * a))


def _p12_bbox(P):
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    return (min(xs), min(ys), max(xs), max(ys))


def _p12_lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def _p12_lr(a, b, p):
    """> 0 when p lies left of a -> b"""
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def _p12_clip_ring(R, C):
    """the ring R clipped to the convex counter-clockwise polygon C (Sutherland-Hodgman); [] when nothing is left"""
    out = list(R)
    for i in range(len(C)):
        a, b = C[i], C[(i + 1) % len(C)]
        inp, out = out, []
        if not inp:
            return []
        p = inp[-1]
        fp = _p12_lr(a, b, p)
        for q in inp:
            fq = _p12_lr(a, b, q)
            if fq >= 0.0:
                if fp < 0.0:
                    out.append(_p12_lerp(p, q, fp / (fp - fq)))
                out.append(q)
            elif fp >= 0.0:
                out.append(_p12_lerp(p, q, fp / (fp - fq)))
            p, fp = q, fq
    return out if len(out) >= 3 else []


def _p12_clip_line(P, C):
    """the pieces of the polyline P inside the convex counter-clockwise polygon C (Cyrus-Beck, segment by segment)"""
    pieces, cur = [], None
    for i in range(len(P) - 1):
        p, q = P[i], P[i + 1]
        t0, t1, ok = 0.0, 1.0, True
        for j in range(len(C)):
            a, b = C[j], C[(j + 1) % len(C)]
            fp, fq = _p12_lr(a, b, p), _p12_lr(a, b, q)
            if fp < 0.0 and fq < 0.0:
                ok = False
                break
            if fp < 0.0:
                t0 = max(t0, fp / (fp - fq))
            elif fq < 0.0:
                t1 = min(t1, fp / (fp - fq))
        if not ok or t0 > t1:
            cur = None
            continue
        a_, b_ = _p12_lerp(p, q, t0), _p12_lerp(p, q, t1)
        if cur is not None and t0 == 0.0:
            cur.append(b_)
        else:
            cur = [a_, b_]
            pieces.append(cur)
        if t1 < 1.0:
            cur = None
    return pieces


def _p12_clipper(C, inner):
    """a clip region: the convex polygon C (counter-clockwise) and a box surely inside it (no clipping needed there)"""
    return dict(C=C, bb=_p12_bbox(C), inner=inner)


def _p12_cring(R, K):
    b, o, i_ = _p12_bbox(R), K["bb"], K["inner"]
    if b[2] < o[0] or b[0] > o[2] or b[3] < o[1] or b[1] > o[3]:
        return []
    if i_[0] <= b[0] and b[2] <= i_[2] and i_[1] <= b[1] and b[3] <= i_[3]:
        return list(R)
    return _p12_clip_ring(R, K["C"])


def _p12_cline(P, K):
    b, o, i_ = _p12_bbox(P), K["bb"], K["inner"]
    if b[2] < o[0] or b[0] > o[2] or b[3] < o[1] or b[1] > o[3]:
        return []
    if i_[0] <= b[0] and b[2] <= i_[2] and i_[1] <= b[1] and b[3] <= i_[3]:
        return [list(P)]
    return _p12_clip_line(P, K["C"])


def _p12_hull(P):
    """convex hull, counter-clockwise (monotone chain)"""
    P = sorted(set(P))
    if len(P) < 3:
        return P

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in P:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(hi) >= 2 and cr(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def _p12_len(P):
    return sum(math.hypot(P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1]) for i in range(len(P) - 1))


def _p12_along(P, d):
    """the point and the unit direction at arc length d along the polyline P"""
    for i in range(len(P) - 1):
        L = math.hypot(P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1])
        if d <= L or i == len(P) - 2:
            if L < 1e-9:
                return P[i], (1.0, 0.0)
            t = max(0.0, min(1.0, d / L))
            return _p12_lerp(P[i], P[i + 1], t), ((P[i + 1][0] - P[i][0]) / L, (P[i + 1][1] - P[i][1]) / L)
        d -= L
    return P[-1], (1.0, 0.0)


def _p12_circle_pts(cx, cy, r, n=72):
    return [(cx + r * math.cos(2.0 * math.pi * i / n), cy + r * math.sin(2.0 * math.pi * i / n)) for i in range(n)]


def _p12_dense(P, step, closed=False):
    """the polyline (a ring when closed) P with points added so that no segment is longer than step"""
    if step <= 0.0 or len(P) < 2:
        return [tuple(p[:2]) for p in P]
    Q = [tuple(p[:2]) for p in P] + ([tuple(P[0][:2])] if closed else [])
    out = [Q[0]]
    for a, b in zip(Q, Q[1:]):
        n = int(math.hypot(b[0] - a[0], b[1] - a[1]) / step)
        for i in range(1, n + 1):
            t = i / float(n + 1)
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
        out.append(b)
    return out[:-1] if closed else out


def _p12_seg_d(p, a, b):
    """the distance from p to the segment a-b, and the segment's point nearest to p"""
    ex, ey = b[0] - a[0], b[1] - a[1]
    L2 = ex * ex + ey * ey
    t = 0.0 if L2 <= 0.0 else max(0.0, min(1.0, ((p[0] - a[0]) * ex + (p[1] - a[1]) * ey) / L2))
    q = (a[0] + t * ex, a[1] + t * ey)
    return math.hypot(q[0] - p[0], q[1] - p[1]), q


def _p12_free_spot(x, y, w, h, taken, bounds, rings=(0.0, 1.0, 2.0, 3.5, 5.0, 7.0), n=16, pad=0.4):
    """v12 (G3, no leaders): the box w x h centred on (x, y), else the nearest free one round it (rings mm, n
    directions) inside bounds and off every taken box; None when every try hits"""
    for r in rings:
        for i in range(n if r > 0.0 else 1):
            a = 2.0 * math.pi * i / n
            cx, cy = x + r * math.cos(a), y + r * math.sin(a)
            b = (cx - w / 2.0, cy - h / 2.0, cx + w / 2.0, cy + h / 2.0)
            if bounds and (b[0] < bounds[0] or b[1] < bounds[1] or b[2] > bounds[2] or b[3] > bounds[3]):
                continue
            if not any(lp_hit(b, t, pad) for t in taken):
                return b
    return None


def _p12_axis(R):
    """the direction (radians) of a ring's long side (principal axis of its points)"""
    n = float(len(R))
    mx, my = sum(p[0] for p in R) / n, sum(p[1] for p in R) / n
    sxx = sum((p[0] - mx) ** 2 for p in R)
    syy = sum((p[1] - my) ** 2 for p in R)
    sxy = sum((p[0] - mx) * (p[1] - my) for p in R)
    return 0.5 * math.atan2(2.0 * sxy, sxx - syy)


def _p12_hatch(rings, ang, sp, cap=4000):
    """the segments of parallel lines at the angle ang (radians), sp apart, inside the rings (even-odd), same units"""
    out = []
    if sp <= 0.0 or not rings:
        return out
    u, n = (math.cos(ang), math.sin(ang)), (-math.sin(ang), math.cos(ang))
    vs = [p[0] * n[0] + p[1] * n[1] for R in rings for p in R]
    v, v1 = min(vs) + sp / 2.0, max(vs)
    while v < v1 and len(out) < cap:
        ts = []
        for R in rings:
            m = len(R)
            for i in range(m):
                p, q = R[i], R[(i + 1) % m]
                vp, vq = p[0] * n[0] + p[1] * n[1] - v, q[0] * n[0] + q[1] * n[1] - v
                if (vp > 0.0) != (vq > 0.0):
                    t = vp / (vp - vq)
                    x, y = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
                    ts.append((x * u[0] + y * u[1], (x, y)))
        ts.sort()
        for i in range(0, len(ts) - 1, 2):
            out.append((ts[i][1], ts[i + 1][1]))
        v += sp
    return out


def _p12_place_nm(n):
    """G16 (v12): a place of P12_PLACES as printed: a bridge code (K1-K6) as its real name (names module)"""
    return bridge_name(n) if n in (u"K1", u"K2", u"K3", u"K4", u"K5", u"K6") else n


def _p12_put(pg, shapes):
    """icons.py / plants.py shapes onto the page (the core's sec_put)"""
    sec_put(pg, shapes)


def _p12_step(pg, n, x, y, size=4.2):
    """the numbered step marker n (icons.py ico_step) centred on (x, y); returns its box"""
    sh, (ax, ay), th, cap = ico_step(x, y, size, "solid", P12_STEP_COL.get(n))
    _p12_put(pg, sh)
    pg.text(str(n), ax, ay - cap / 2.0, cap / CAP, th, bold=True, align="C")
    return (x - size / 2.0, y - size / 2.0, x + size / 2.0, y + size / 2.0)


def _p12_arrow(pg, a, b, col, lw=0.45, minlen=6.0, dash=None, head=1.8):
    """an arrow along a -> b (page), drawn at least minlen mm long about its middle (a project link is often a few
    metres: at the map's scale it is lengthened, never turned)"""
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    if L < 1e-6:
        return None
    if L < minlen:
        m, f = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0), minlen / L / 2.0
        a, b = (m[0] - (b[0] - a[0]) * f, m[1] - (b[1] - a[1]) * f), (m[0] + (b[0] - a[0]) * f, m[1] + (b[1] - a[1]) * f)
    arrow(pg, [a, b], col, lw, head, dash)
    return (a, b)


def _p12_bar(pg, x, y, den, marks=(0, 20, 50, 100)):
    """the scale bar of the plan zoom from (x, y): ink and white segments 1.2 mm high, marks in m over them; box"""
    k = 1000.0 / den
    for i in range(len(marks) - 1):
        pg.poly([rect(x + marks[i] * k, y, x + marks[i + 1] * k, y + 1.2)], fill=COL["ink"] if i % 2 == 0 else COL["white"],
                stroke=COL["ink"], lw=0.12)
    for i, v in enumerate(marks):
        pg.text(u"{}{}".format(v, u" m" if i == len(marks) - 1 else u""), x + v * k, y + 2.0, FS_MIN, COL["ink"], align="C")
    return (x - 2.0, y - 0.2, x + marks[-1] * k + 6.0, y + 2.0 + FS_MIN)


def _p12_north(pg, x, y, d, L=7.0):
    """a north arrow at (x, y) pointing along the unit page direction d; returns its box"""
    tip = (x + d[0] * L, y + d[1] * L)
    arrow(pg, [(x, y), tip], COL["ink"], 0.3, 2.0)
    pg.text(u"N", tip[0] + d[0] * 1.6, tip[1] + d[1] * 1.6 - FS_MIN * CAP / 2.0, FS_MIN, COL["ink"], bold=True, align="C")
    xs, ys = [x, tip[0] + d[0] * 3.5], [y, tip[1] + d[1] * 3.5]
    return (min(xs) - 2.5, min(ys) - 2.5, max(xs) + 2.5, max(ys) + 2.5)


# ---------------------------------------------------------------- the data: zones and links, figures
def _p12_zones(log):
    """the Option A zones and water links (survey m) from the water balance's results, key "zones" (v6)"""
    z = _p12_get("zones")
    if not z or not z.get("zones"):
        log.append(u"p.12: water_balance_results.json has no zones (run the water balance v6): the map shows the "
                   u"stream, the places and the flows only")
        return [], []
    log.append(u"p.12: zones from the water balance ({})".format(z.get("source", u"?")))
    zs = [dict(q, ring=[tuple(p) for p in q["ring"]]) for q in z["zones"] if len(q.get("ring") or []) >= 3]
    return zs, [dict(q, P=[tuple(p) for p in q["P"]]) for q in z.get("links") or [] if len(q.get("P") or []) >= 2]


def _p12_pick(zones, code, area=None, label=None):
    return [z for z in zones if z["code"] == code and (area is None or (z.get("study_area") or u"").startswith(area))
            and (label is None or label in (z.get("label") or u""))]


def _p12_figures(zones):
    """every figure the map prints, from the water balance results (None = left out)"""
    f = {}
    take, site = _p12_get("design", "river_take_m3_per_year"), _p12_get("site_catch_m3_per_year")
    f["collect"] = (take, site)
    wt = _p12_pick(zones, "WT")
    f["reed_m2"] = sum(z.get("m2") or _p12_area(z["ring"]) for z in wt) if wt else None
    f["store"] = WB_STORE if WB_LIVE else None          # v6.1: never the built-in default
    left = _p12_get("design", "river_left_pct")
    f["left"] = tuple(left) if left else None
    mix = _p12_get("design", "mix")
    f["farms"] = _p12_get("cutoff", mix, "central", "delivered_m3_per_year") if mix else None
    ha = [_p12_get("lands", "cropland_ha"), _p12_get("lands", "orchard_ha")]
    f["farm_ha"] = sum(ha) if None not in ha else None
    s2 = _p12_get("lands", "strip_m2")
    f["strip"] = (s2 / 4.0, s2 * STRIP_DEPTH, WB_STRIP) if s2 and WB_LIVE else None      # 400 cm wide (the strip's design)
    return f


# ---------------------------------------------------------------- labels on the map (G3: no leaders, never stacked)
def _p12_place(pg, specs, taken, bounds, segs, log, size=None, bold=False):
    """v12 (round 3, G3): the names of specs (x, y, head, col) on or right next to their point (M2 lp_place,
    leaders=False); on a map only place names stand, so a name with no room there is left out (logged), never
    numbered. Returns the drawn boxes (also added to taken)."""
    size = size or FS_MIN
    specs = [sp for sp in specs if sp.get("head")]
    if not specs:
        return []
    labels = [dict(x=sp["x"], y=sp["y"], w=text_w(sp["head"], size, bold) + 0.6, h=size * 1.15) for sp in specs]
    got = lp_place(labels, obstacles=taken, lines=segs, bounds=bounds, sizes=(1.0,), leaders=False)
    out = []
    for sp, g in zip(specs, got):
        if not g or g.get("number"):
            log.append(u"p11 map: no room beside its point for the name '{}' (left out, G3)".format(sp["head"]))
            continue
        b = g["box"]
        taken.append(b)
        pg.text(sp["head"], b[0] + 0.3, b[1] + (b[3] - b[1] - size * CAP) / 2.0, size, sp.get("col") or COL["ink2"],
                bold=bold)
        out.append(b)
    return out


# ---------------------------------------------------------------- the axonometric map (v6: a true 3D object)
def _p12_axo(pts, area, margins):
    """T(p, z=0) survey m -> page mm for the map, its inverse at z = 0, k (page mm per m) and view (the horizontal
    unit vector from the scene towards the viewer, survey axes): the plan turned by the one of P12_ROTS that gives
    the largest scale (ties: nearest the old -12 deg), seen from above at the angle of P12_SIN / P12_COS (depth x
    sin, heights x cos; one scale), fitted into area less the margins (left, right, bottom, top). v12 (P11.1): a
    point may carry its drawn lift (x, y, z m): the fit then holds it lifted (the relief never leaves the box, G2)"""
    cx, cy = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
    ml, mr, mb, mt = margins
    W, H = area[2] - area[0] - ml - mr, area[3] - area[1] - mb - mt
    best = None
    for deg in sorted(P12_ROTS, key=lambda d_: abs(d_ + 12.0)):
        rho = math.radians(deg)
        c, s = math.cos(rho), math.sin(rho)
        U = [((p[0] - cx) * c - (p[1] - cy) * s, ((p[0] - cx) * s + (p[1] - cy) * c) * P12_SIN +
              (p[2] if len(p) > 2 else 0.0) * P12_COS) for p in pts]
        u0, u1 = min(u for u, w in U), max(u for u, w in U)
        w0, w1 = min(w for u, w in U), max(w for u, w in U)
        k = min(W / max(u1 - u0, 1.0), H / max(w1 - w0, 1.0))
        if best is None or k > best[0] + 1e-9:
            best = (k, rho, u0, u1, w0, w1)
    k, rho, u0, u1, w0, w1 = best
    c, s = math.cos(rho), math.sin(rho)
    ox = area[0] + ml + (W - (u1 - u0) * k) / 2.0 - u0 * k
    oy = area[1] + mb + (H - (w1 - w0) * k) / 2.0 - w0 * k

    def T(p, z=0.0):
        u = (p[0] - cx) * c - (p[1] - cy) * s
        v = (p[0] - cx) * s + (p[1] - cy) * c
        return (ox + u * k, oy + (v * P12_SIN + z * P12_COS) * k)

    def Ti(X, Y):
        u, v = (X - ox) / k, (Y - oy) / k / P12_SIN
        return (cx + u * c + v * s, cy - u * s + v * c)
    return T, Ti, k, (-s, -c)


def _p12_base(pg, items, T, K, hook=None, step=None):
    """the shared basemap items (or M11 axo items with T = identity) through T, clipped to K; hook(rings, hex) ->
    True takes a fill over (the tree cover is drawn as a canopy texture). v12: step (survey m) adds points to every
    ring and line first, so that what T lifts onto the relief follows the ground"""
    if step:
        items = _p12_dense_items(items, step)

    def fill(rings, col, alpha, nonzero):
        rr = [r for r in (_p12_cring(R, K) for R in rings) if r]
        if rr and not (hook and hook(rr, col)):
            pg.poly(rr, fill=col)                       # v12 (G9): opaque

    def line(pts, col, w, dash, alpha):
        for piece in _p12_cline(pts, K):
            pg.line(piece, col, w, dash)
    return basemap_draw(items, T, fill, line)


def _p12_dense_items(items, step):
    """basemap fill / line items (survey m) with their rings and lines densified to step (draping, P11.1)"""
    out = []
    for it in items:
        if it[0] == "fill":
            out.append(("fill", [_p12_dense(R, step, True) for R in it[1]]) + tuple(it[2:]))
        elif it[0] == "line":
            out.append(("line", _p12_dense(it[1], step)) + tuple(it[2:]))
        else:
            out.append(it)
    return out


# ---------------------------------------------------------------- the relief (v12, round 3: P11.1, N3 merged)
def _p12_dem(D, log):
    """the ground model of the map, built once a run (merge rule N3, research/elevation_2026-10-31/README.md):
    dict(h=f(x, y) -> m a.s.l. (None: no model), kind both / survey / glo / flat). Inside the analysis frame
    (basemap_frame) the survey contours: between the nearest contour vertex (z1, d1) and the nearest one of another
    height (z2, d2), (z1 d2 + z2 d1) / (d1 + d2). Outside it Copernicus GLO-30 (DATA_DIR/P12_DEM_FILE, bilinear)
    plus the bias (median survey - GLO-30 at points every P12_DEM_EDGE_M[0] m along the frame, P12_DEM_EDGE_M[1] m
    inside it), blended over P12_DEM_BLEND_M with the survey value at the nearest frame-edge point. Missing file:
    survey only (outside = the frame-edge value); no contour heights: GLO-30 only; neither: flat. Logs the elevation
    source line, and a FLAG when every contour height is a multiple of 5 m (an old basemap.json cache)."""
    if "dem" in _P12_MEMO:
        return _P12_MEMO["dem"]
    L = ((D or {}).get("layers") or {}) if D else {}
    F = basemap_frame(D) if D else None
    cz = [(float(c[1]), c[2]) for c in L.get("contours") or [] if c[1] is not None and len(c[2]) >= 2]
    B = P12_DEM_BUCKET
    idx = {}
    for z, P in cz:
        for p in _p12_dense(P, 5.0):
            idx.setdefault((int(math.floor(p[0] / B)), int(math.floor(p[1] / B))), []).append((p[0], p[1], z))
    if cz and all(abs(z - 5.0 * round(z / 5.0)) < 1e-6 for z, _P in cz):
        log.append(u"FLAG p11 contour heights rounded to 5 m (an old basemap.json: the site board's next run writes "
                   u"them to 0.1 m): the relief steps at 5 m")
    sv = bool(cz and F)
    memo = {}

    def hs(x, y):
        """the survey ground at (x, y); None with no contour within P12_DEM_SEARCH cells"""
        key = (round(x, 1), round(y, 1))
        if key in memo:
            return memo[key]
        i0, j0 = int(math.floor(x / B)), int(math.floor(y / B))
        best, r_ = {}, 0
        while r_ <= P12_DEM_SEARCH:
            for i in range(i0 - r_, i0 + r_ + 1):
                for j in range(j0 - r_, j0 + r_ + 1):
                    if max(abs(i - i0), abs(j - j0)) != r_:
                        continue
                    for px, py, z in idx.get((i, j), ()):
                        d = math.hypot(px - x, py - y)
                        if d < best.get(z, 1e18):
                            best[z] = d
            if len(best) >= 2 and sorted(best.values())[1] <= r_ * B:
                break                                   # no vertex not yet seen can be nearer
            r_ += 1
        out = None
        if best:
            ds = sorted((d, z) for z, d in best.items())
            if len(ds) == 1 or ds[0][0] + ds[1][0] <= 1e-9:
                out = ds[0][1]
            else:
                (d1, z1), (d2, z2) = ds[0], ds[1]
                out = (z1 * d2 + z2 * d1) / (d1 + d2)
        memo[key] = out
        return out

    g, gerr = None, None
    fn = os.path.join(DATA_DIR, P12_DEM_FILE)
    try:
        import io
        with io.open(fn, "r", encoding="utf-8") as fh:
            j_ = json.load(fh)
        pts, nr, nc = j_["pts"], int(j_["rows"]), int(j_["cols"])
        if len(pts) == nr * nc and nr > 1 and nc > 1:
            g = dict(x0=float(pts[0][0]), y0=float(pts[0][1]), dx=float(pts[1][0] - pts[0][0]),
                     dy=float(pts[nc][1] - pts[0][1]), nr=nr, nc=nc, z=[float(p[2]) for p in pts])
            if abs(g["dx"]) < 1e-9 or abs(g["dy"]) < 1e-9:
                g, gerr = None, u"not a regular grid"
        else:
            gerr = u"{} points for {} x {}".format(len(pts), nr, nc)
    except Exception as ex:
        gerr = u"{}: {}".format(type(ex).__name__, ex)

    def hg(x, y):
        """GLO-30 at (x, y), bilinear; None outside its clip"""
        if not g:
            return None
        fc, fr = (x - g["x0"]) / g["dx"], (y - g["y0"]) / g["dy"]
        if fc < 0.0 or fr < 0.0 or fc > g["nc"] - 1 or fr > g["nr"] - 1:
            return None
        c0, r0 = min(int(fc), g["nc"] - 2), min(int(fr), g["nr"] - 2)
        tc, tr = fc - c0, fr - r0
        Z, nc_ = g["z"], g["nc"]
        a, b = Z[r0 * nc_ + c0], Z[r0 * nc_ + c0 + 1]
        c, d = Z[(r0 + 1) * nc_ + c0], Z[(r0 + 1) * nc_ + c0 + 1]
        return (a * (1.0 - tc) + b * tc) * (1.0 - tr) + (c * (1.0 - tc) + d * tc) * tr

    bias, nb = 0.0, 0
    if g and sv:
        cx_, cy_ = sum(p[0] for p in F) / len(F), sum(p[1] for p in F) / len(F)
        st, ins = P12_DEM_EDGE_M
        dif = []
        for a, b in zip(F, F[1:] + F[:1]):
            Le = math.hypot(b[0] - a[0], b[1] - a[1])
            for i in range(int(Le / st) + 1):
                t = min(1.0, i * st / max(Le, 1e-9))
                p = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
                dc = math.hypot(cx_ - p[0], cy_ - p[1]) or 1.0
                q = (p[0] + (cx_ - p[0]) * ins / dc, p[1] + (cy_ - p[1]) * ins / dc)
                s_, g_ = hs(q[0], q[1]), hg(q[0], q[1])
                if s_ is not None and g_ is not None:
                    dif.append(s_ - g_)
        if dif:
            dif.sort()
            nb = len(dif)
            bias = dif[nb // 2] if nb % 2 else 0.5 * (dif[nb // 2 - 1] + dif[nb // 2])

    def edge(x, y):
        best = None
        for a, b in zip(F, F[1:] + F[:1]):
            d, q = _p12_seg_d((x, y), a, b)
            if best is None or d < best[0]:
                best = (d, q)
        return best

    def h(x, y):
        if not sv:
            return hg(x, y)
        if _p12_pip(x, y, F):
            v = hs(x, y)
            if v is not None:
                return v
            gv = hg(x, y)
            return gv + bias if gv is not None else None
        gv = hg(x, y)
        d, q = edge(x, y)
        if gv is not None and d >= P12_DEM_BLEND_M:
            return gv + bias
        ev = hs(q[0], q[1])
        if gv is None:
            return ev
        if ev is None:
            return gv + bias
        w = d / P12_DEM_BLEND_M
        return (1.0 - w) * ev + w * (gv + bias)

    if sv and g:
        kind = "both"
        src = u"elevation source: survey contours (frame) + Copernicus GLO-30 (outside, bias {:.2f} m)".format(bias)
    elif sv:
        kind = "survey"
        src = u"elevation source: survey contours (frame), GLO-30 file missing ({}: {}): survey only".format(fn, gerr)
    elif g:
        kind = "glo"
        src = u"elevation source: Copernicus GLO-30 only (survey contours carry no height)"
    else:
        kind = "flat"
        src = u"elevation source: none (no contour heights, GLO-30 file {}: {}): ground drawn flat".format(fn, gerr)
    log.append(src)
    if kind == "both":
        log.append(u"p11 relief: bias from {} frame-edge samples; GLO-30 {} x {} points".format(nb, g["nr"], g["nc"]))
    _P12_MEMO["dem"] = dict(h=h if kind != "flat" else None, kind=kind)
    return _P12_MEMO["dem"]


def _p12_grid(dem, box, s):
    """the ground heights on a regular grid over box (survey m) at the step s: dict(x0, y0, s, nx, ny, H rows);
    a node with no value takes the lowest value found (flat ground without a model)"""
    x0, y0 = box[0], box[1]
    nx = max(1, int(math.ceil((box[2] - x0) / s)))
    ny = max(1, int(math.ceil((box[3] - y0) / s)))
    f = dem.get("h")
    H = [[(f(x0 + i * s, y0 + j * s) if f else 0.0) for i in range(nx + 1)] for j in range(ny + 1)]
    vals = [v for r in H for v in r if v is not None]
    lo = min(vals) if vals else 0.0
    H = [[lo if v is None else v for v in r] for r in H]
    return dict(x0=x0, y0=y0, s=float(s), nx=nx, ny=ny, H=H)


def _p12_hat(G, x, y):
    """the grid's ground at (x, y), bilinear, held at the grid's edge beyond it"""
    s = G["s"]
    fx = max(0.0, min(G["nx"] - 1e-9, (x - G["x0"]) / s))
    fy = max(0.0, min(G["ny"] - 1e-9, (y - G["y0"]) / s))
    i, j = int(fx), int(fy)
    tx, ty = fx - i, fy - j
    H = G["H"]
    return (H[j][i] * (1.0 - tx) + H[j][i + 1] * tx) * (1.0 - ty) + \
        (H[j + 1][i] * (1.0 - tx) + H[j + 1][i + 1] * tx) * ty


def _p12_zx(G, sb, ga_h, k):
    """the ground's lift over the drawn box sb: (z0 the lowest ground, the range, ZX the exaggeration): P12_ZX's
    most, held so that no lifted slope folds over (99th percentile) and the lift takes at most its share of the
    map's height (G2), never under its least"""
    s, H = G["s"], G["H"]
    zs, sl = [], []
    for j in range(G["ny"] + 1):
        y = G["y0"] + j * s
        if not (sb[1] <= y <= sb[3]):
            continue
        for i in range(G["nx"] + 1):
            x = G["x0"] + i * s
            if not (sb[0] <= x <= sb[2]):
                continue
            zs.append(H[j][i])
            if 0 < i < G["nx"] and 0 < j < G["ny"]:
                sl.append(math.hypot((H[j][i + 1] - H[j][i - 1]) / (2.0 * s), (H[j + 1][i] - H[j - 1][i]) / (2.0 * s)))
    if not zs:
        return 0.0, 0.0, 1.0
    z0, zr = min(zs), max(zs) - min(zs)
    lo, hi, fold, share = P12_ZX
    zx = hi
    if sl:
        sl.sort()
        s99 = sl[int(0.99 * (len(sl) - 1))]
        if s99 > 1e-6:
            zx = min(zx, fold / s99)
    if zr > 1e-6 and k > 0.0:
        zx = min(zx, share * ga_h / (zr * P12_COS * k))
    return z0, zr, max(lo, zx)


def _p12_tone_fn(G, zx, z0, zr, light):
    """the ground's tone at a point (hex), memoised by step: the height band (P12_RELIEF_BAND_M, paper -> structure
    toward the top) lit from the page's upper left (light = the horizontal direction to it, survey axes; 45 deg up):
    lit slopes toward white, shaded ones toward the reference grey, in P12_GROUND steps (a stepped, shaded relief)"""
    C = P12_GROUND
    lx, ly = light
    ce = se = math.sqrt(0.5)
    s = G["s"]
    nb = max(1, int(math.ceil(max(zr, P12_RELIEF_BAND_M) / P12_RELIEF_BAND_M)))
    memo = {}

    def tone(x, y):
        gx = (_p12_hat(G, x + s, y) - _p12_hat(G, x - s, y)) / (2.0 * s) * zx
        gy = (_p12_hat(G, x, y + s) - _p12_hat(G, x, y - s)) / (2.0 * s) * zx
        lam = (-gx * lx * ce - gy * ly * ce + se) / math.sqrt(gx * gx + gy * gy + 1.0) - se
        q = max(-C["steps"], min(C["steps"], int(round(lam / C["step"]))))
        b = int(math.floor(max(0.0, _p12_hat(G, x, y) - z0) / P12_RELIEF_BAND_M))
        key = (b, q)
        if key not in memo:
            c = _sec_mix(C["low"], C["high"], C["high_t"] * min(1.0, b / float(nb)))
            if q > 0:
                c = _sec_mix(c, C["lit"], C["lit_t"] * q / float(C["steps"]))
            elif q < 0:
                c = _sec_mix(c, C["shade"], C["shade_t"] * -q / float(C["steps"]))
            memo[key] = c
        return memo[key]
    return tone


def _p12_relief(G, zx, z0, zr, light):
    """the relief of one drawing: its grid, lift(x, y) (drawn m over z0) and tone(x, y)"""
    return dict(G=G, s=G["s"], zx=zx, z0=z0, zr=zr, light=light,
                lift=lambda x, y: zx * (_p12_hat(G, x, y) - z0), tone=_p12_tone_fn(G, zx, z0, zr, light))


def _p12_terrain(pg, R, T, K):
    """P11.1: the ground as stepped, shaded faces: each grid cell at its nodes' lifted heights, a row's run of one
    tone joined into one face (every node kept on both edges), clipped to K, each face edged in its own tone (no
    hairline seams); no fold is possible (ZX keeps the lifted slopes under the view's), so no order is needed.
    Returns the number of faces."""
    G, zx, z0, tone = R["G"], R["zx"], R["z0"], R["tone"]
    s, x0, y0, nx, ny, H = G["s"], G["x0"], G["y0"], G["nx"], G["ny"], G["H"]
    bb = K["bb"]
    n = 0
    prow = [T((x0 + i * s, y0), zx * (H[0][i] - z0)) for i in range(nx + 1)]
    for j in range(ny):
        nrow = [T((x0 + i * s, y0 + (j + 1) * s), zx * (H[j + 1][i] - z0)) for i in range(nx + 1)]
        run = None
        for i in range(nx + 1):
            tn = None
            if i < nx:
                q = (prow[i], prow[i + 1], nrow[i + 1], nrow[i])
                if not (max(p[0] for p in q) < bb[0] or min(p[0] for p in q) > bb[2] or
                        max(p[1] for p in q) < bb[1] or min(p[1] for p in q) > bb[3]):
                    tn = tone(x0 + (i + 0.5) * s, y0 + (j + 0.5) * s)
            if run is not None and tn != run[1]:
                rr = _p12_cring(prow[run[0]:i + 1] + nrow[run[0]:i + 1][::-1], K)
                if rr:
                    pg.poly([rr], fill=run[1], stroke=run[1], lw=0.05)
                    n += 1
                run = None
            if tn is not None and run is None:
                run = (i, tn)
        prow = nrow
    return n


def _p12_contours(pg, L, R, T, K, sb):
    """the survey contours (inside the frame) on the lifted ground at their own heights: every 5 m a fine line,
    every 25 m a little stronger (P12_CONTOUR); with an old cache (heights rounded to 5 m) only the major ones.
    Returns the number of pieces drawn."""
    cs = [c for c in L.get("contours") or [] if c[1] is not None and len(c[2]) >= 2]
    if not cs:
        return 0
    rounded = all(abs(float(c[1]) - 5.0 * round(float(c[1]) / 5.0)) < 1e-6 for c in cs)
    n = 0
    for major, z, P in cs:
        z = float(z)
        if rounded and not major:
            continue
        if not rounded and abs(z - 5.0 * round(z / 5.0)) > 0.15:
            continue
        if not _p12_hit(P, sb):
            continue
        col, t, w = P12_CONTOUR[1 if abs(z - 25.0 * round(z / 25.0)) <= 0.15 else 0]
        c_ = _sec_mix(col, P12_GROUND["low"], t) if t else col
        lz = R["zx"] * (z - R["z0"])
        for piece in _p12_cline([T(p, lz) for p in P], K):
            pg.line(piece, c_, w)
            n += 1
    return n


def _p12_near(R, line, d):
    """True when any corner of ring R (survey m) lies within d m of the polyline line"""
    d2 = d * d
    for (px, py) in R:
        for (ax, ay), (bx, by) in zip(line, line[1:]):
            ex, ey = bx - ax, by - ay
            L2 = ex * ex + ey * ey
            t = 0.0 if L2 <= 0.0 else max(0.0, min(1.0, ((px - ax) * ex + (py - ay) * ey) / L2))
            qx, qy = ax + t * ex - px, ay + t * ey - py
            if qx * qx + qy * qy <= d2:
                return True
    return False


def _p12_hit(P, box):
    b = _p12_bbox(P)
    return not (b[2] < box[0] or b[0] > box[2] or b[3] < box[1] or b[1] > box[3])


def _p12_pip(x, y, R):
    """point in ring (even-odd)"""
    c, j = False, len(R) - 1
    for i in range(len(R)):
        (xi, yi), (xj, yj) = R[i], R[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            c = not c
        j = i
    return c


def _p12_station(P, p):
    """the arc length (m) along the polyline P of the point of P nearest to p"""
    best, s, acc = None, 0.0, 0.0
    for i in range(len(P) - 1):
        a, b = P[i], P[i + 1]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dy * dy
        L = math.sqrt(L2)
        t = 0.0 if L2 < 1e-12 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
        d2 = (a[0] + t * dx - p[0]) ** 2 + (a[1] + t * dy - p[1]) ** 2
        if best is None or d2 < best:
            best, s = d2, acc + t * L
        acc += L
    return s


def _p12_drops(log):
    """the registry W cuts as (station along P12_SELINOS m, drop m, walled): drop = the wall or bank tops (mean of
    the sides that have one) minus the water at average yearly flow, i.e. how far the water lies under the ground"""
    out = []
    for cid in P12_W_CUTS:
        try:
            r = level_registry(cid)
            a, b = level_ends(cid)
        except Exception:
            continue
        tops = [t for _ty, t in r["walls"].values() if t is not None]
        if not tops or r["avg_flow"] is None:
            continue
        out.append((_p12_station(P12_SELINOS, ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)),
                    sum(tops) / len(tops) - r["avg_flow"], bool(r["walled"])))
    if not out:
        log.append(u"p.12: no W cut in the level registry has a bank top and an average flow: the stream is drawn "
                   u"flat on the map")
    return sorted(out)


def _p12_drop_fn(drops):
    """f(p) -> (drop m, walled) at a survey point: the registry cuts' drops along the stream, linear between two
    cuts by their station on P12_SELINOS, the end cut's value beyond (drawn, never printed)"""
    memo = {}

    def f(p):
        key = (round(p[0], 2), round(p[1], 2))
        if key in memo:
            return memo[key]
        if not drops:
            r = (0.0, False)
        else:
            s = _p12_station(P12_SELINOS, p)
            r = (drops[-1][1], drops[-1][2])
            if s <= drops[0][0]:
                r = (drops[0][1], drops[0][2])
            else:
                for (s0, d0, w0), (s1, d1, w1) in zip(drops, drops[1:]):
                    if s <= s1:
                        t = (s - s0) / max(1e-6, s1 - s0)
                        r = (d0 + (d1 - d0) * t, w0 if t < 0.5 else w1)
                        break
        memo[key] = r
        return r
    return f


def _p12_channel(pg, L, T, K, k, view, sb, log, R, dz):
    """G8 on the map (v12, round 3): the Selinos lying in its channel on the relief. The surveyed water (the bank line
    at average flow) is sunk by the registry drop dz (true depth) under the ground's lift there and textured (M5
    water_plan: islands left open, A2 streak cap, no waves); no summer strip in plan (D2: the section shows it); the
    bank faces that look toward the viewer go from the ground down to the water (stone in the walled town reach,
    earth elsewhere), far first; the faces looking away are filled with the ground's tone (R tone), so the near ground
    hides the sunk water under it (was a white sheet over the whole map); then the bank line. Returns what it drew
    (for the legend)."""
    out = dict(wall=False, bank=False, water=False)
    groups = [g for g in (L.get("water") or []) if g and len(g[0]) >= 3 and _p12_hit(g[0], sb)]
    if not groups:
        return out
    pal = _wat_pal()
    lift, tone = R["lift"], R["tone"]
    faces, masks, tops = [], [], []
    for gi, g in enumerate(groups):
        low, isl = None, []
        for ri, Rg in enumerate(g):
            if len(Rg) < 3:
                continue
            zs = [dz(p) for p in Rg]
            ls = [lift(p[0], p[1]) for p in Rg]
            sunk = [T(p, l_ - z[0]) for p, l_, z in zip(Rg, ls, zs)]
            if ri == 0:
                low = sunk
            else:
                isl.append(sunk)
            tops.append([T(p, l_) for p, l_ in zip(Rg, ls)])
            ar = sum(Rg[i][0] * Rg[(i + 1) % len(Rg)][1] - Rg[(i + 1) % len(Rg)][0] * Rg[i][1]
                     for i in range(len(Rg))) > 0
            left = ar == (ri == 0)                       # the water lies left of each edge
            n = len(Rg)
            for i in range(n):
                p, q = Rg[i], Rg[(i + 1) % n]
                ex, ey = q[0] - p[0], q[1] - p[1]
                Le = math.hypot(ex, ey)
                if Le < 1e-6:
                    continue
                zp, zq = zs[i][0], zs[(i + 1) % n][0]
                if zp < 0.05 and zq < 0.05:
                    continue
                lp_, lq_ = ls[i], ls[(i + 1) % n]
                quad = [T(p, lp_), T(q, lq_), T(q, lq_ - zq), T(p, lp_ - zp)]
                nx, ny = (-ey / Le, ex / Le) if left else (ey / Le, -ex / Le)
                if nx * view[0] + ny * view[1] <= 0.02:  # faces away from the viewer: the near ground covers it
                    masks.append((quad, tone((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0)))
                else:
                    faces.append(((p[0] + q[0]) / 2.0 * view[0] + (p[1] + q[1]) / 2.0 * view[1], quad,
                                  zs[i][1] or zs[(i + 1) % n][1]))
        surf = _p12_cring(low, K) if low else []
        if surf:
            out["water"] = True
            hs_ = [r for r in (_p12_cring(H_, K) for H_ in isl) if r]
            try:
                _p12_shapes(pg, water_plan(surf, k, bank=False, seed=gi + 1, holes=hs_ or None).shapes())
            except Exception as ex:
                log.append(u"p.12: water_plan failed ({}): the stream drawn in its plain tone".format(ex))
                pg.poly([surf] + hs_, fill=pal["surface"])
    faces.sort(key=lambda f_: f_[0])                    # far first
    for _, ring, walled in faces:
        rr = _p12_cring(ring, K)
        if rr:
            pg.poly([rr], fill=SCT["stone"] if walled else SCT["earth"])
            out["wall" if walled else "bank"] = True
    for ring, c in masks:                               # the near ground over the sunk water
        rr = _p12_cring(ring, K)
        if rr:
            pg.poly([rr], fill=c, stroke=c, lw=0.05)
    for r in (_p12_cring(R_, K) for R_ in tops):
        if r:
            pg.line(r + r[:1], pal["edge"], 0.18)
    return out


def _p12_stream_top(pg, L, T, K, sb):
    """what lies over or beyond the open stream, flat on the ground: bridge decks and lines, the covered course
    (dashed), OpenStreetMap's water beyond the survey frame"""
    out = dict(bridge=False, covered=False)
    pal = _wat_pal()
    for g in L.get("water_out") or []:
        rr = [r for r in (_p12_cring([T(p) for p in R], K) for R in g if len(R) >= 3) if r]
        if rr:
            pg.poly(rr, fill=pal["surface"])
    for kind, P in L.get("waterways_out") or []:
        for piece in _p12_cline([T(p) for p in P], K):
            pg.line(piece, BM_COL["water"], 0.3)
    for R in L.get("decks") or []:
        if len(R) >= 3 and _p12_hit(R, sb):
            rr = _p12_cring([T(p) for p in R], K)
            if rr:
                pg.poly([rr], fill=BM_COL["road"], stroke=BM_COL["road_edge"], lw=0.1)
                out["bridge"] = True
    for P in L.get("bridges") or []:
        if len(P) >= 2 and _p12_hit(P, sb):
            for piece in _p12_cline([T(p) for p in P], K):
                pg.line(piece, BM_COL["ink"], 0.3)
                out["bridge"] = True
    for P in L.get("covered") or []:
        if len(P) >= 2 and _p12_hit(P, sb):
            for piece in _p12_cline([T(p) for p in P], K):
                pg.line(piece, BM_COL["water_edge"], 0.3, list(BM_COVERED_DASH))
                out["covered"] = True
    return out


def _p12_shapes(pg, shapes):
    """water.py / plants.py / figures.py shapes (with text, alpha and images) onto the page"""
    shp_put(pg, shapes)


def _p12_canopy(pg, rings, k, log):
    """the tree cover (survey / WorldCover, page rings on the lifted ground) as a canopy texture: leaf clusters on a
    jittered P12_CANOPY_M lattice, their shadows first, pushed to the lower right (light from the upper left, as the
    buildings and trees); v12 (G9, D7): every shape opaque, no pale ground under them (the relief shows between the
    clusters); returns the number of clusters"""
    st = TREE_STYLES["context"]
    shadow = _sec_mix(st["shadow"], P12_GROUND["low"], 0.75)
    s = max(0.9, P12_CANOPY_M * k)
    pts = []
    for R in rings:
        if len(R) < 3:
            continue
        b = _p12_bbox(R)
        j, y = 0, b[1] + s / 2.0
        while y < b[3] and len(pts) < P12_CANOPY_CAP:
            x = b[0] + s / 2.0 + (s / 2.0 if j % 2 else 0.0)
            while x < b[2]:
                rnd = _tree_rand(x, y)
                px, py = x + (rnd() - 0.5) * 0.5 * s, y + (rnd() - 0.5) * 0.5 * s
                if _p12_pip(px, py, R):
                    pts.append((px, py, s * (0.42 + 0.16 * rnd()), int(rnd() * 3.0) % 3))
                x += s
            y += s * 0.866
            j += 1
    if len(pts) >= P12_CANOPY_CAP:
        log.append(u"p.12: the tree-cover texture stops at {} clusters".format(P12_CANOPY_CAP))
    for px, py, r, _c in pts:
        pg.poly([[(q[0] + 0.35 * r, q[1] - 0.22 * r) for q in _p12_circle_pts(px, py, r, 10)]], fill=shadow)
    for px, py, r, c in pts:
        pg.poly([_tree_blob(px, py, r, _tree_rand(px, py), 9)], fill=(st["mid"], st["dark"], st["light"])[c])
    return len(pts)


def _p12_zone_trees(zones, log, water_rings=()):
    """the planted trees of the project's zones (survey m): a mixed, ecologically zoned scatter (plants.py, G9:
    never rows), wet to dry away from the Selinos line, in the streamside planting, the walks and dry tops and
    Demeter's garden; [(key, x, y, crown m, height m)], heights the species' sourced drawing heights. v12 (G8): none
    whose trunk or half its crown stands over the stream (water_clip_points on water_rings, survey m; logged)"""
    out = []
    for i, z in enumerate(zones):
        if z["code"] not in P12_ZONE_MIX:
            continue
        try:
            _, placed = pla_scatter_plan(z["ring"], 1.0, {"wet": P12_SELINOS, "width_m": P12_BAND_M},
                                         mix=P12_ZONE_MIX[z["code"]], seed=i + 1, density=0.8)
        except Exception as ex:
            log.append(u"p.12: no trees in zone {} ({})".format(z.get("label") or z["code"], ex))
            continue
        for key, x, y, cm in placed:
            sp = PLA_SPECIES[key]
            if sp["layer"] != "tree" or not sp.get("crown_m"):
                continue
            out.append((key, x, y, cm, pla_height_ok(key, sp["h_m"] * cm / sp["crown_m"])))
    kept = water_clip_points([(x, y, cm / 2.0, key, cm, h) for key, x, y, cm, h in out], list(water_rings),
                             page="p11")
    return [(q[3], q[0], q[1], q[4], q[5]) for q in kept]


def _p12_tree_style(key):
    """G9 (D7, v12): the draw_tree colours of one species from the shared plant module (pla_colour: each species its
    own colour, opaque) on its form's leaf-cluster count (P12_TREE_STY); its shadow opaque, on the ground's tone"""
    sty = _P12_MEMO.setdefault("sty", {})
    if key not in sty:
        base = TREE_STYLES[P12_TREE_STY.get(key, "tree")]
        try:
            c = pla_colour(key)
        except Exception:
            c = {}
        fill = c.get("fill") or base["mid"]
        sty[key] = dict(base, mid=fill, dark=c.get("edge") or _sec_mix(fill, "000000", 0.25),
                        light=c.get("lt") or _sec_mix(fill, "FFFFFF", 0.35), trunk=c.get("stem") or base["trunk"],
                        shadow=_sec_mix(base["shadow"], P12_GROUND["low"], 0.82), shadow_a=None)
    return sty[key]


def _p12_orchard_tree(pg, x, y, s):
    """P11.5: the generic orchard tree (the land cover's crop is not sourced: no species), s mm high, standing on
    (x, y): an opaque ground shadow, a short trunk, a round crown lit from the upper left"""
    cr, cs, cl, tk = P12_ORCHARD
    r = 0.36 * s
    cy = y + s - r
    pg.poly([[(x + 0.18 * s + 0.42 * s * math.cos(t), y + 0.1 * s * math.sin(t)) for t in
              [2.0 * math.pi * i / 20 for i in range(20)]]], fill=_sec_mix("495338", P12_GROUND["low"], 0.8))
    pg.line([(x, y), (x, cy - 0.4 * r)], tk, max(0.12, 0.05 * s))
    pg.poly([_p12_circle_pts(x + 0.07 * s, cy - 0.06 * s, r, 28)], fill=cs)
    pg.poly([_p12_circle_pts(x - 0.03 * s, cy + 0.02 * s, 0.9 * r, 28)], fill=cr)
    pg.poly([_p12_circle_pts(x - 0.12 * s, cy + 0.11 * s, 0.38 * r, 18)], fill=cl)
    return (x - r - 0.1 * s, y - 0.1 * s, x + 0.6 * s, y + s)


def _p12_fields(pg, L, Tg, K, k, sb, step):
    """P11.5 (G9 agriculture, Aras 31 Oct: "simplify the farms like a single icon is enough"): the land cover's
    fields and orchards and the survey's agricultural zones as ONE flat fill with fine rows along each patch's long
    side (P12_FIELD_MM, page spacing), and ONE symbol on each patch big enough to read: the generic orchard tree on
    an orchard, the field pictogram on a field, drawn last over every patch. Returns {"field": n, "orchard": n}."""
    lc = L.get("lc") or {}
    pats = [("orchard", g) for g in lc.get("orchard") or []] + [("field", g) for g in lc.get("farmland") or []] + \
        [("field", z["rings"]) for z in L.get("zones") or [] if z.get("kind") == "agri" and z.get("rings")]
    sp_mm, pen, amin, sym = P12_FIELD_MM
    row = _sec_mix(BM_COL["field"], MP["agriculture"][1], 0.45)
    out, syms = dict(field=0, orchard=0), []
    for kind, g in pats:
        rings = [R for R in g if len(R) >= 3]
        if not rings or not _p12_hit(rings[0], sb):
            continue
        pr = [r for r in (_p12_cring([Tg(p) for p in _p12_dense(R, step, True)], K) for R in rings) if r]
        if not pr:
            continue
        pg.poly(pr, fill=BM_COL["field"])
        out[kind] += 1
        for a, b in _p12_hatch(rings, _p12_axis(rings[0]), sp_mm / max(k, 1e-6), 600):
            for piece in _p12_cline([Tg(p) for p in _p12_dense([a, b], step)], K):
                pg.line(piece, row, pen)
        c = _p12_cen(rings[0])
        if _p12_area(pr[0]) >= amin and _p12_pip(c[0], c[1], rings[0]):
            syms.append((kind, Tg(c)))
    bb = K["bb"]
    for kind, (x, y) in syms:
        if bb[0] + sym < x < bb[2] - sym and bb[1] + 1.0 < y < bb[3] - sym:
            if kind == "orchard":
                _p12_orchard_tree(pg, x, y, sym)
            else:
                _p12_put(pg, ico_draw("field", x, y + 0.5 * sym, sym))
    return out


def _p12_legend(pg, ga, rows, avoid, taken):
    """the map's legend (M2 Legend, G1: every symbol it draws) and the key of its letters (G3), in the inside corner
    of the map holding the fewest drawn key points and taken boxes, on a white ground with no edge (v12: G17, no
    alpha); rows = [(label, kind fill / line / dash / tree / ground / orchard / letter, sample)]; returns its box"""
    meas = lambda s_, pt, b_: text_w(s_, pt * GRID_PT_, b_)
    best = None
    for side in ("inside_bl", "inside_tl", "inside_br", "inside_tr"):
        lg = Legend(ga, side=side, y_down=False)
        for lab, kind, smp in rows:
            lg.add(lab, kind, **smp)
        Lo = lg.layout(meas)
        b = Lo["box"]
        n = sum(1 for p in avoid if b[0] <= p[0] <= b[2] and b[1] <= p[1] <= b[3]) + \
            sum(20 for t in taken if lp_hit(b, t))
        if best is None or n < best[0]:
            best = (n, Lo)
    Lo = best[1]
    b = Lo["box"]
    pg.poly([rect(b[0], b[1], b[2], b[3])], fill=COL["white"])
    G_ = P12_GROUND
    for r in Lo["rows"]:
        x0, y0, x1, y1 = r["swatch"]
        ym = (y0 + y1) / 2.0
        if r["kind"] == "fill":
            pg.poly([rect(x0, y0, x1, y1)], fill=r["colour"], stroke=r.get("edge"), lw=0.12)
        elif r["kind"] in ("line", "dash"):
            pg.line([(x0, ym), (x1, ym)], r["colour"], r.get("width", 0.3), r.get("dash"))
        elif r["kind"] == "ground":                    # the stepped, shaded ground with a contour
            for i, c in enumerate((_sec_mix(G_["low"], G_["lit"], G_["lit_t"]), G_["low"],
                                   _sec_mix(_sec_mix(G_["low"], G_["high"], G_["high_t"]), G_["shade"], G_["shade_t"]))):
                pg.poly([rect(x0 + i * (x1 - x0) / 3.0, y0, x0 + (i + 1) * (x1 - x0) / 3.0, y1)], fill=c)
            pg.line([(x0, y0 + 0.3 * (y1 - y0)), (x1, y0 + 0.7 * (y1 - y0))], P12_CONTOUR[1][0], P12_CONTOUR[1][2])
        elif r["kind"] == "tree":                      # one opaque crown per colour (species colours, G9)
            cols = r.get("cols") or [TREE_STYLES["tree"]["mid"]]
            n_ = len(cols)
            R = min((y1 - y0) * 0.5, (x1 - x0) / (2.0 * n_) + 0.25)
            for i, c in enumerate(cols):
                cx = x0 + (x1 - x0) * (i + 0.5) / n_
                pg.poly([_tree_blob(cx, ym, R, _tree_rand(cx, ym), 9)], fill=c)
        elif r["kind"] == "orchard":
            _p12_orchard_tree(pg, (x0 + x1) / 2.0, y0 - 0.2, (y1 - y0) + 0.6)
        elif r["kind"] == "letter":
            _p12_letter(pg, r["letter"], (x0 + x1) / 2.0, ym, r["colour"])
        pg.text(r["label"], r["text"][0], r["text"][1], r["size_pt"] * GRID_PT_, COL["ink"])
    return b


def _p12_k5_check(L, D, log):
    """the base-data check of the brief (Üç Kemer, K5: "is it really that empty?"): what the shared basemap holds
    within P12_K5_CHECK_M of the bridge, written to the log (the map draws all of it: buildings, streets, parks,
    tree cover, names)"""
    k5 = dict(P12_PLACES).get(u"K5")
    if not k5:
        return
    R = P12_K5_CHECK_M
    near = lambda P: any(math.hypot(p[0] - k5[0], p[1] - k5[1]) < R for p in P)
    bl = [b for b in L.get("buildings") or [] if b.get("rings") and near(b["rings"][0])]
    gr = [z for z in L.get("zones") or [] if z.get("kind") == "green" and z.get("rings") and near(z["rings"][0])]
    tc = [g for g in (L.get("lc") or {}).get("trees", []) if g and len(g[0]) >= 3 and near(g[0])]
    fl = [g for g in (L.get("lc") or {}).get("farmland", []) + (L.get("lc") or {}).get("orchard", [])
          if g and len(g[0]) >= 3 and near(g[0])]
    nm = [n for n, _p in basemap_names((k5[0] - R, k5[1] - R, k5[0] + R, k5[1] + R), D)]
    log.append(u"p.12 base data around " + bridge_name(u"K5") + u" ({:.0f} m): {} buildings ({} heritage, {} with a survey height), "
               u"{} parks / green areas, {} tree-cover patches, {} field patches; names: {}".format(
                   R, len(bl), sum(1 for b in bl if b.get("her")), sum(1 for b in bl if b.get("h")), len(gr), len(tc),
                   len(fl), u", ".join(nm) or u"none"))


def _p12_scene(pg, K, T, k, view, R, zones, links, f, Z, D, log, sb, dz, trees):
    """v12 (round 3): the axonometric water map's drawing, shared by the map and its zoom of the upstream entry (the
    same scene re-drawn at the zoom's scale, P11.2): T(p, z) survey m and drawn lift -> page mm, K the clip, R the
    relief (_p12_relief), sb the survey box drawn, dz the channel's drop, trees the planted trees (clipped to land).
    In the G8 order: the ground (the stepped, shaded relief, P11.1; streets, parks, fields, tree cover, the study
    area and the survey contours, all draped on it), the bed and water (_p12_channel), the zones (a zone in the bed on
    the sunk water), the structures (bridge decks, buildings at their survey heights standing on the ground,
    heritage in its rose, the winter store), the vegetation (planted trees, each species its colour), then the
    flow, the links and the up-close cut line (A, A'). Returns what the legend, the marks and the labels need."""
    L = (D or {}).get("layers") if D else None
    lift = R["lift"]
    Tg = lambda p: T(p, lift(p[0], p[1]))
    P3 = lambda x, y, z: T((x, y), z)
    P3g = lambda x, y, z: T((x, y), z + lift(x, y))
    step = R["s"]
    bb = K["bb"]
    ins = lambda p: bb[0] + 0.5 <= p[0] <= bb[2] - 0.5 and bb[1] + 0.5 <= p[1] <= bb[3] - 0.5
    out = dict(ch={}, top={}, fills=set(), ncan=0, her=False, nfar=0, near=0, far=0, units=False, trees=[],
               fields={}, study=False, ncont=0, cube_b=None, labels=[], lk=set(), farm_tip=None, u=(1.0, 0.0))
    # the ground (terrain): the relief, then what lies flat on it
    out["nground"] = _p12_terrain(pg, R, T, K)
    if L:
        items = basemap_items("simple", {"stream": False, "buildings": False, "streets": True, "green": True,
                                         "trees": True, "fields": False}, box=sb, D=D, split_buildings=True)
        canopy = []

        def hook(rr, col):
            if col == BM_COL["tree"]:
                canopy.extend(rr)
                return True
            return False
        _p12_base(pg, items, Tg, K, hook, step)
        out["fills"] = set(it[2] for it in items if it[0] == "fill")
        out["fields"] = _p12_fields(pg, L, Tg, K, k, sb, step)
        out["ncan"] = _p12_canopy(pg, canopy, k, log)
        for Rs in basemap_study(D):
            if len(Rs) >= 3 and _p12_hit(Rs, sb):
                for piece in _p12_cline([Tg(p) for p in _p12_dense(list(Rs) + [Rs[0]], step)], K):
                    pg.line(piece, COL["ink2"], 0.18, [1.2, 0.5])
                    out["study"] = True
        out["ncont"] = _p12_contours(pg, L, R, T, K, sb)
        # the bed and the water
        out["ch"] = _p12_channel(pg, L, T, K, k, view, sb, log, R, dz)
    # the zones of the project, flat on the ground (the summer strip: in the section only, D2)
    wr = [g[0] for g in ((L or {}).get("water") or []) if g and len(g[0]) >= 3]
    wbb = [_p12_bbox(R_) for R_ in wr]
    for z in zones:
        if z["code"] == "STRIP":
            continue
        tones = P12_ZONE.get(z["code"], (COL["faint"], COL["structure"]))
        c = _p12_cen(z["ring"])
        wet = any(b_[0] <= c[0] <= b_[2] and b_[1] <= c[1] <= b_[3] and _p12_pip(c[0], c[1], R_)
                  for R_, b_ in zip(wr, wbb))
        dn = _p12_dense(z["ring"], step, True)
        rr = _p12_cring([T(p, lift(p[0], p[1]) - dz(p)[0]) for p in dn] if wet else [Tg(p) for p in dn], K)
        if rr:
            pg.poly([rr], fill=tones[0], stroke=tones[1], lw=0.15)
    # the structures: over the stream, the buildings (v9: volumes only near the stream and heritage, the rest as
    # faint footprints; v12: standing on the relief, footprints opaque)
    if L:
        out["top"] = _p12_stream_top(pg, L, Tg, K, sb)
        units = [b for b in L.get("buildings") or [] if b.get("rings") and _p12_hit(b["rings"][0], sb)]
        out["her"] = any(b.get("her") for b in units)
        near, far = [], []
        for b in units:
            (near if b.get("her") or _p12_near(b["rings"][0], P12_SELINOS, P12_BLD_NEAR_M) else far).append(b)
        farc = _sec_mix(P12_BLD_FAR[0], COL["white"], P12_BLD_FAR[1])
        for b in far:
            for R_ in b["rings"][:1]:
                rr = _p12_cring([Tg(p) for p in _p12_dense(R_, step, True)], K)
                if rr:
                    pg.poly([rr], fill=farc)
                    out["nfar"] += 1
        out["near"], out["far"], out["units"] = len(near), len(far), bool(near)
        gfn = lambda x, y: lift(x, y)
        its = bld_axo_items([b for b in near if not b.get("her")], P3, view=view, box=sb, ground=gfn)
        if out["her"]:
            its += bld_axo_items([b for b in near if b.get("her")], P3, view=view, box=sb, cols=P12_HER_COLS,
                                 ground=gfn)
        _p12_base(pg, its, lambda p: p, K)
    # HOLD: the design store as a cube at the map's own scale, under the upstream entry's terraces and basins
    # (dashed: in the ground; v12 opaque), an arrow down into it
    up = _p12_pick(zones, "WS", "aras") + _p12_pick(zones, "WT", "aras")
    hold = (sum(_p12_cen(z["ring"])[0] for z in up) / len(up), sum(_p12_cen(z["ring"])[1] for z in up) / len(up)) \
        if up else P12_PLACES[0][1]
    e = max(f["store"]) ** (1.0 / 3.0) if f["store"] else 0.0
    out["hold"], out["e"] = hold, e
    if e > 0.0:
        lh = lift(hold[0], hold[1])
        P = lambda i, j, l: T((hold[0] + (i - 0.5) * e, hold[1] + (j - 0.5) * e), lh - l * e)
        rr = _p12_cring(_p12_hull([P(i, j, l) for i in (0, 1) for j in (0, 1) for l in (0, 1)]), K)
        if rr:
            pg.poly([rr], fill=MP["storage"][0])
            for a_, b_ in (((0, 0, 0), (1, 0, 0)), ((1, 0, 0), (1, 1, 0)), ((1, 1, 0), (0, 1, 0)), ((0, 1, 0), (0, 0, 0)),
                           ((0, 0, 1), (1, 0, 1)), ((1, 0, 1), (1, 1, 1)), ((1, 1, 1), (0, 1, 1)), ((0, 1, 1), (0, 0, 1)),
                           ((0, 0, 0), (0, 0, 1)), ((1, 0, 0), (1, 0, 1)), ((1, 1, 0), (1, 1, 1)), ((0, 1, 0), (0, 1, 1))):
                for piece in _p12_cline([P(*a_), P(*b_)], K):
                    pg.line(piece, MP["storage"][2], 0.22, [0.9, 0.6])
            out["cube_b"] = _p12_bbox(rr)
            a_, b_ = T(hold, lh), T(hold, lh - 0.55 * e)
            if ins(a_) and ins(b_):
                arrow(pg, [a_, b_], MP["storage"][2], 0.4, 1.5)
    # the vegetation: the zones' trees in 3D (shadows first, then far to near; each species its colour, opaque)
    trs = sorted(trees, key=lambda t_: t_[1] * view[0] + t_[2] * view[1])
    keep = []
    for t_ in trs:
        q = Tg((t_[1], t_[2]))
        rx, top = t_[3] / 2.0 * k + 0.5, t_[4] * P12_COS * k + 0.5
        if bb[0] + rx < q[0] < bb[2] - rx and bb[1] + 1.0 < q[1] < bb[3] - top:
            keep.append(t_)
    for key_, x, y, cm, h in keep:
        tree_shadow(pg, P3g, k, x, y, cm / 2.0, _p12_tree_style(key_))
    for key_, x, y, cm, h in keep:
        draw_tree(pg, P3g, k, x, y, cm / 2.0, h, _p12_tree_style(key_), shadow=False)
    out["trees"] = keep
    # the flow: in at the top (hand arrow on the first 16 mm), out to the farms beyond the last point
    S = [Tg(p) for p in P12_SELINOS]
    Ls = _p12_len(S)
    segs = [(S[i], S[i + 1]) for i in range(len(S) - 1)]
    ha = [_p12_along(S, t)[0] for t in (0.0, 4.0, 8.0, 12.0, 16.0)]
    if all(ins(p) for p in ha):
        hand_arrow(pg, ha, "water", 0.8)
    (ex, ey), (ux, uy) = S[-1], _p12_along(S, Ls)[1]
    if ins((ex, ey)):
        room = min([(bb[2] - 3.0 - ex) / ux if ux > 1e-6 else 99.0, (ey - bb[1] - 3.0) / -uy if uy < -1e-6 else 99.0,
                    (bb[3] - 3.0 - ey) / uy if uy > 1e-6 else 99.0, (ex - bb[0] - 3.0) / -ux if ux < -1e-6 else 99.0])
        Lf = max(6.0, min(16.0, room - 5.0))          # room left for the step marker beyond the tip
        farm_tip = (ex + ux * Lf, ey + uy * Lf)
        hand_arrow(pg, [(ex - ux * 2.0, ey - uy * 2.0), farm_tip], "water", 0.8,
                   (MP["agriculture"][1], MP["agriculture"][2]))
        segs.append(((ex, ey), farm_tip))
        out["farm_tip"], out["u"] = farm_tip, (ux, uy)
    # the links of the project (zone base INT_LINK_*): flood onto the terraces (dashed), clean water to the planting,
    # people down to the bed
    for ln in links:
        a, b = Tg(ln["P"][0]), Tg(ln["P"][-1])
        if not (ins(a) and ins(b)):
            continue
        if ln.get("kind") == "flood":
            r = _p12_arrow(pg, a, b, MP["amphibious"][2], 0.4, 6.0, [1.0, 0.6])
        elif ln.get("kind") == "people":
            r = _p12_arrow(pg, a, b, COL["accent"], 0.3, 4.5, [0.6, 0.5], 1.4)
        elif u"PLANTING" in (ln.get("label") or u""):
            r = _p12_arrow(pg, a, b, P12_ZONE["WP"][2], 0.4, 6.0)
            if r:
                out["lk"].add("planting")
        else:
            r = None
        if r:
            segs.append(r)
            if ln.get("kind") in ("flood", "people"):
                out["lk"].add(ln["kind"])
    # the up-close section's line (the band below draws it), its ends A and A' (D6)
    if Z:
        za, zb_ = Tg(Z["A"]), Tg(Z["B"])
        for piece in _p12_cline([za, zb_], K):
            pg.line(piece, COL["accent"], 0.35, [1.6, 0.6, 0.3, 0.6])
        Lz = math.hypot(zb_[0] - za[0], zb_[1] - za[1]) or 1.0
        uz = ((zb_[0] - za[0]) / Lz, (zb_[1] - za[1]) / Lz)
        for p_, s_, sg in ((za, u"A", -1.0), (zb_, u"A'", 1.0)):
            if ins(p_):
                tx, ty = p_[0] + sg * uz[0] * 1.9, p_[1] + sg * uz[1] * 1.9
                w_ = text_w(s_, FS_MIN, True)
                pg.text(s_, tx, ty - FS_MIN * CAP / 2.0, FS_MIN, COL["accent"], bold=True, align="C")
                out["labels"].append((tx - w_ / 2.0, ty - FS_MIN * CAP / 2.0, tx + w_ / 2.0, ty + FS_MIN * CAP / 2.0))
        segs.append((za, zb_))
    out["S"], out["segs"] = S, segs
    return out


def _p12_map(pg, ga, zones, links, f, Z, D, log):
    """the axonometric water map in the area ga (page mm), v12 (round 3) on the real relief (P11.1): the plan turned
    and fitted as before, the ground model on a grid round it (_p12_dem: survey contours + GLO-30), its lift (free
    diagram scale, _p12_zx) and the fit again with the lift (nothing leaves ga, G2); the scene (_p12_scene); the
    zoom of the upstream entry (_p12_inset, P11.2); the five steps' markers (1-4 in the zoom, leader-free); the
    project along the channel as letters (_p12_letters, P11.3); the legend with the letters' key. Returns what the
    labels and the page need."""
    key = list(P12_SELINOS) + [p for _, p in P12_PLACES]
    for z in zones:
        key += z["ring"]
    L = (D or {}).get("layers") if D else None
    T0, Ti0, k0, view = _p12_axo(key, ga, P12_MAP_MARG)
    b0 = _p12_bbox([Ti0(ga[0], ga[1]), Ti0(ga[2], ga[1]), Ti0(ga[2], ga[3]), Ti0(ga[0], ga[3])])
    sb0 = (b0[0] - 40.0, b0[1] - 40.0, b0[2] + 40.0, b0[3] + 40.0)
    dem = _p12_dem(D, log)
    s = max(P12_RELIEF_CELL_M[0], min(P12_RELIEF_CELL_M[1], P12_RELIEF_CELL_MM / k0))
    pad = P12_RELIEF_PAD_M
    G = _p12_grid(dem, (sb0[0] - pad, sb0[1] - pad, sb0[2] + pad, sb0[3] + pad), s)
    z0, zr, zx = _p12_zx(G, sb0, ga[3] - ga[1], k0)
    lift0 = lambda x, y: zx * (_p12_hat(G, x, y) - z0)
    T, Ti, k, view = _p12_axo([(p[0], p[1], lift0(p[0], p[1])) for p in key], ga, P12_MAP_MARG)
    log.append(u"p.12: the water map, an axonometric at about 1:{:,.0f} (a diagram: no scale bar)".format(1000.0 / k))
    b1 = _p12_bbox([Ti(ga[0], ga[1]), Ti(ga[2], ga[1]), Ti(ga[2], ga[3]), Ti(ga[0], ga[3])])
    lm = 40.0 + min(pad, zr * zx * P12_COS / P12_SIN)
    sb = (b1[0] - lm, b1[1] - lm, b1[2] + lm, b1[3] + lm)
    Xc, Yc = (ga[0] + ga[2]) / 2.0, (ga[1] + ga[3]) / 2.0
    a_, b_ = Ti(Xc, Yc), Ti(Xc - 1.0, Yc + 1.0)        # the page's upper left, in survey axes: the light
    ll = math.hypot(b_[0] - a_[0], b_[1] - a_[1]) or 1.0
    R = _p12_relief(G, zx, z0, zr, ((b_[0] - a_[0]) / ll, (b_[1] - a_[1]) / ll))
    K = _p12_clipper([(ga[0], ga[1]), (ga[2], ga[1]), (ga[2], ga[3]), (ga[0], ga[3])], ga)
    if "drops" not in _P12_MEMO:
        _P12_MEMO["drops"] = _p12_drops(log) if L else []
    dz = _p12_drop_fn(_P12_MEMO["drops"])
    wr = [R_ for g in ((L or {}).get("water") or []) for R_ in g if len(R_) >= 3]
    trees = _p12_zone_trees(zones, log, wr)
    Sc = _p12_scene(pg, K, T, k, view, R, zones, links, f, Z, D, log, sb, dz, trees)
    log.append(u"p11 relief: ground lifted x{:.2f} (a diagram: free scale), {:.2f} to {:.2f} m in view, grid {:.0f} m, "
               u"{} ground faces, {} contour pieces".format(zx, z0, z0 + zr, s, Sc["nground"], Sc["ncont"]))
    if L:
        _p12_k5_check(L, D, log)
        log.append(u"p.12 map: {} buildings as volumes on the ground (within {:.0f} m of the stream, heritage), {} as "
                   u"flat footprints".format(Sc["near"], P12_BLD_NEAR_M, Sc["far"]))
    Tg = lambda p: T(p, R["lift"](p[0], p[1]))
    M = dict(T=T, Ti=Ti, Tg=Tg, k=k, view=view, R=R, dem=dem, Sc=Sc, S=Sc["S"], segs=list(Sc["segs"]), dz=dz,
             trees=trees, taken=list(Sc["labels"]), labels=list(Sc["labels"]), hold=Sc["hold"], e=Sc["e"], legend=None)
    I = _p12_inset(pg, ga, M, zones, links, f, Z, D, log)
    M["inset"] = I
    if I:
        M["taken"] += [I["box"], I["title_box"]] + list(I["Sc"]["labels"])
        M["labels"] += [I["title_box"]] + list(I["Sc"]["labels"])
    # the steps: a numbered marker where each happens, leader-free (R2, G3: their texts in the column's key); 1-4 in
    # the zoom of the upstream entry when there is one (P11.2), 5 at the farms' arrow; a marker that would sit on
    # another moves the least distance off it
    wt, ws, wd = _p12_pick(zones, "WT", "aras"), _p12_pick(zones, "WS", "aras"), _p12_pick(zones, "WD", "aras")
    Tq, cb, bnd = (I["Tg"], I["Sc"]["cube_b"], I["box"]) if I else (Tg, Sc["cube_b"], ga)
    ft, (ux, uy) = Sc["farm_tip"], Sc["u"]
    at = {1: Tq(_p12_cen(ws[0]["ring"])) if ws else Tq(P12_PLACES[0][1]),
          2: Tq(_p12_cen(wt[0]["ring"])) if wt else None,
          3: ((cb[0] + cb[2]) / 2.0, cb[1] - 2.4) if cb else None,
          4: Tq(_p12_cen(wd[0]["ring"])) if wd else None,
          5: (ft[0] + ux * 3.2, ft[1] + uy * 3.2) if ft else None}
    sz, marks = 3.6, []
    for n in (1, 2, 3, 4, 5):
        if not at[n]:
            continue
        obst = marks + M["labels"] + ([I["box"]] if I and n == 5 else [])
        b_ = _p12_free_spot(at[n][0], at[n][1], sz, sz, obst, bnd if n < 5 else ga, (0.0, 1.0, 2.0, 3.5, 5.0))
        x_, y_ = ((b_[0] + b_[2]) / 2.0, (b_[1] + b_[3]) / 2.0) if b_ else at[n]
        at[n] = (x_, y_)
        marks.append(_p12_step(pg, n, x_, y_, sz))
    M["taken"] += marks
    M["at"], M["marks"] = at, marks
    if Sc["cube_b"]:
        M["taken"].append(Sc["cube_b"])
    lrows = _p12_letters(pg, ga, M, zones, D, log)
    # the legend (G1): every symbol of the drawing, nothing else; then the letters' key (G3)
    ch, top = Sc["ch"], Sc["top"]
    pal = _wat_pal()
    lk = set(Sc["lk"]) | (set(I["Sc"]["lk"]) if I else set())
    lg = []
    if dem["kind"] != "flat":
        src = {"both": u"survey contours + Copernicus GLO-30", "survey": u"survey contours",
               "glo": u"Copernicus GLO-30"}[dem["kind"]]
        lg.append((u"Ground: {}, heights ×{:.1f}, 5 m steps".format(src, zx), "ground", {}))
    if ch.get("water"):
        lg.append((u"Selinos stream, water at average yearly flow", "fill", dict(colour=pal["surface"], edge=pal["edge"])))
    if ch.get("wall"):
        lg.append((u"Stone channel wall, walled town reach", "fill", dict(colour=SCT["stone"])))
    if ch.get("bank"):
        lg.append((u"Earth bank", "fill", dict(colour=SCT["earth"])))
    if Sc["units"]:
        lg.append((u"Building at its survey height", "fill", dict(colour=BLD_COL["wall_lit"], edge=BLD_COL["axo_line"])))
    if Sc["nfar"]:
        lg.append((u"Building further from the stream, footprint", "fill",
                   dict(colour=_sec_mix(P12_BLD_FAR[0], COL["white"], P12_BLD_FAR[1]))))
    if Sc["her"]:
        lg.append((u"Heritage building", "fill", dict(colour=P12_HER_COLS["wall_lit"], edge=P12_HER_COLS["axo_line"])))
    if BM_COL["road"] in Sc["fills"]:
        lg.append((u"Street", "fill", dict(colour=BM_COL["road"], edge=BM_COL["road_edge"])))
    if BM_COL["park"] in Sc["fills"]:
        lg.append((u"Park, grass", "fill", dict(colour=BM_COL["park"])))
    if Sc["fields"].get("field"):
        lg.append((u"Field: the farms that take the clean water", "fill", dict(colour=BM_COL["field"])))
    if Sc["fields"].get("orchard"):
        lg.append((u"Orchard: one tree for each orchard", "orchard", {}))
    if Sc["ncan"]:
        lg.append((u"Tree cover", "tree", dict(cols=[TREE_STYLES["context"]["mid"], TREE_STYLES["context"]["dark"]])))
    tk_ = sorted(set(t_[0] for t_ in Sc["trees"] + (I["Sc"]["trees"] if I else [])))
    if tk_:
        lg.append((u"Planted tree at its species' height, each species its colour", "tree",
                   dict(cols=[_p12_tree_style(q)["mid"] for q in tk_][:4])))
    if top.get("bridge"):
        lg.append((u"Bridge", "line", dict(colour=BM_COL["ink"], width=0.3)))
    if top.get("covered"):
        lg.append((u"Covered stream", "dash", dict(colour=BM_COL["water_edge"], width=0.3, dash=list(BM_COVERED_DASH))))
    if Sc["cube_b"] or (I and I["Sc"]["cube_b"]):
        lg.append((u"Winter store in the ground, to scale", "dash", dict(colour=MP["storage"][2], width=0.22,
                                                                          dash=[0.9, 0.6])))
    if "flood" in lk:
        lg.append((u"High water onto the terraces", "dash", dict(colour=MP["amphibious"][2], width=0.4,
                                                                  dash=[1.0, 0.6])))
    if "people" in lk:
        lg.append((u"People down to the bed", "dash", dict(colour=COL["accent"], width=0.3, dash=[0.6, 0.5])))
    if "planting" in lk:
        lg.append((u"Clean water to the planting", "line", dict(colour=P12_ZONE["WP"][2], width=0.4)))
    if Z:
        lg.append((u"Section up close A-A' (band below)", "dash", dict(colour=COL["accent"], width=0.35,
                                                                      dash=[1.6, 0.6, 0.3, 0.6])))
    if Sc["study"]:
        lg.append((u"Study area", "dash", dict(colour=COL["ink2"], width=0.18, dash=[1.2, 0.5])))
    for ch_, txt, col in lrows:
        lg.append((txt, "letter", dict(letter=ch_, colour=col)))
    if lg:
        avoid = list(M["S"]) + [Tg(p) for z in zones for p in z["ring"][::4]]
        M["legend"] = _p12_legend(pg, ga, lg, avoid, M["taken"])
        M["taken"].append(M["legend"])
    hold = M["hold"]
    nd = (T((hold[0], hold[1] + 100.0))[0] - T(hold)[0], T((hold[0], hold[1] + 100.0))[1] - T(hold)[1])
    nl = math.hypot(*nd)
    M["nd"] = (nd[0] / nl, nd[1] / nl)
    return M


def _p12_inset(pg, ga, M, zones, links, f, Z, D, log):
    """P11.2 (v12): the upstream entry (the blue box: the winter store under the dry-top terraces, the reed basins,
    the spillway, the shaded walk) re-drawn at a larger scale in a box P12_INSET over the map's emptiest place
    (fewest projected project points, then nearest the spot): the same scene (_p12_scene) through the map's own view
    scaled about the spot, on its own finer ground grid (the same lift), on white, with a 0.25 pt neatline and the
    title "ZOOMED IN · ..." over it; on the map the spot's rectangle and one connector to the box's nearest corner
    (SF_ZOOM pens, PLAN §2 zoom inset). None (logged) without the upstream entry's zones or without room."""
    T, Ti, k, view, R, Sc, Tg = M["T"], M["Ti"], M["k"], M["view"], M["R"], M["Sc"], M["Tg"]
    up = [z for z in zones if (z.get("study_area") or u"").startswith("aras") and z["code"] in ("WS", "WT", "WD", "GR")]
    if not up:
        log.append(u"p11 map: no upstream-entry zones: no zoom of the upstream entry")
        return None
    pts = [Tg(p) for z in up for p in z["ring"]] + [Tg(Sc["hold"])]
    if Sc["cube_b"]:
        pts += [(Sc["cube_b"][0], Sc["cube_b"][1]), (Sc["cube_b"][2], Sc["cube_b"][3])]
    sp = _p12_bbox(pts)
    sp = (sp[0] - 3.0, sp[1] - 3.0, sp[2] + 3.0, sp[3] + 3.0)
    W, H = P12_INSET
    tl, m = FS_MIN * 1.8, 4.0
    corners = lambda b: [(b[0], b[1]), (b[2], b[1]), (b[2], b[3]), (b[0], b[3])]
    cand = [(ga[2] - m - W, ga[3] - m - tl - H), ((ga[0] + ga[2] - W) / 2.0, ga[3] - m - tl - H),
            (ga[0] + m, ga[3] - m - tl - H), (ga[2] - m - W, ga[1] + m), (ga[0] + m, ga[1] + m)]
    proj = list(Sc["S"]) + [Tg(p) for z in zones for p in z["ring"][::3]]
    best = None
    for bx, by in cand:
        b = (bx, by, bx + W, by + H)
        if b[0] < ga[0] or b[1] < ga[1] or b[2] > ga[2] or b[3] + tl > ga[3] or lp_hit(b, sp, 2.0):
            continue
        n = sum(1 for p in proj if b[0] <= p[0] <= b[2] and b[1] <= p[1] <= b[3])
        d = min(math.hypot(a[0] - c[0], a[1] - c[1]) for a in corners(sp) for c in corners(b))
        if best is None or n + d / 10.0 < best[0]:
            best = (n + d / 10.0, b)
    if not best:
        log.append(u"FLAG p11 map: no room for the zoom of the upstream entry ({:.0f} x {:.0f} mm)".format(W, H))
        return None
    box = best[1]
    fz = min(W / max(sp[2] - sp[0], 1e-6), H / max(sp[3] - sp[1], 1e-6))
    if fz < 1.5:
        log.append(u"FLAG p11 map: the upstream entry is already {:.0f} x {:.0f} mm on the map: no zoom".format(
            sp[2] - sp[0], sp[3] - sp[1]))
        return None
    scx, scy = (sp[0] + sp[2]) / 2.0, (sp[1] + sp[3]) / 2.0
    bcx, bcy = (box[0] + box[2]) / 2.0, (box[1] + box[3]) / 2.0

    def Tin(p, z=0.0):
        q = T(p, z)
        return (bcx + (q[0] - scx) * fz, bcy + (q[1] - scy) * fz)

    def Tiin(X, Y):
        return Ti(scx + (X - bcx) / fz, scy + (Y - bcy) / fz)
    kin = k * fz
    C = corners(box)
    Kin = _p12_clipper(C, box)
    b1 = _p12_bbox([Tiin(c[0], c[1]) for c in C])
    lmax = max([R["lift"](x_, y_) for x_ in (b1[0], (b1[0] + b1[2]) / 2.0, b1[2])
                for y_ in (b1[1], (b1[1] + b1[3]) / 2.0, b1[3])] + [0.0])
    lm = 40.0 + min(P12_RELIEF_PAD_M, lmax * P12_COS / P12_SIN)
    sbin = (b1[0] - lm, b1[1] - lm, b1[2] + lm, b1[3] + lm)
    s_in = max(P12_RELIEF_CELL_M[0], min(P12_RELIEF_CELL_M[1], P12_RELIEF_CELL_MM / kin))
    Rin = _p12_relief(_p12_grid(M["dem"], sbin, s_in), R["zx"], R["z0"], R["zr"], R["light"])
    pg.poly([rect(box[0], box[1], box[2], box[3])], fill=COL["white"])
    Sci = _p12_scene(pg, Kin, Tin, kin, view, Rin, zones, links, f, Z, D, log, sbin, M["dz"], M["trees"])
    pg.poly([rect(box[0], box[1], box[2], box[3])], stroke=COL["ink"], lw=SF_ZOOM["lw_box"])
    title = u"ZOOMED IN · the upstream entry: collect, clean, hold"
    ty = box[3] + 0.6 * FS_MIN
    pg.text(title, box[0], ty, FS_MIN, COL["ink_dark"], bold=True)
    tb = (box[0], ty - 0.2, box[0] + text_w(title, FS_MIN, True), ty + FS_MIN * CAP)
    pg.poly([rect(sp[0], sp[1], sp[2], sp[3])], stroke=COL["ink"], lw=SF_ZOOM["lw_spot"])
    a_, b_ = min(((a, c) for a in corners(sp) for c in C),
                 key=lambda ac: (ac[0][0] - ac[1][0]) ** 2 + (ac[0][1] - ac[1][1]) ** 2)
    pg.line([a_, b_], COL["ink"], SF_ZOOM["lw_spot"])
    log.append(u"p11 map: the upstream entry zoomed x{:.1f} (about 1:{:,.0f}) in a {:.0f} x {:.0f} mm box, ground "
               u"grid {:.0f} m".format(fz, 1000.0 / kin, W, H, s_in))
    return dict(box=box, title_box=tb, spot=sp, T=Tin, Tg=lambda p: Tin(p, Rin["lift"](p[0], p[1])), k=kin, Sc=Sci,
                R=Rin)


def _p12_letter(pg, ch, x, y, col, r=None):
    """a letter marker (P11.3): the letter in white on the element's dark tone, a white rim; returns its box"""
    r = r or P12_MARK_R
    pg.poly([_p12_circle_pts(x, y, r, 24)], fill=col, stroke=COL["white"], lw=0.15)
    pg.text(ch, x, y - FS_MIN * CAP / 2.0, FS_MIN, COL["white"], bold=True, align="C")
    return (x - r, y - r, x + r, y + r)


def _p12_letters(pg, ga, M, zones, D, log):
    """P11.3 + G18 (v12): what the project does along the channel, as LETTERS on the spot (B, C, D ... in reading
    order, left to right then top down; the digits are the five steps), explained in the legend (G3: no names over
    the project): each zone group of the zone base that no step marks (bergama_zone_base/code.py l.20-36), the
    walled town reach (registry "walled"), the reaches the summer strip alone defines (it lies in the bed, drawn in
    the section: D2) and any reach of the stream inside the study area with no element at all (Aras 31 Oct: "kept as
    it runs", factual only; FLAG). A zone inside the zoom's spot is marked in the zoom. Returns [(letter, text,
    colour)] in key order; the markers' boxes join M["taken"] and M["labels"]."""
    Tg, I, dz = M["Tg"], M.get("inset"), M["dz"]
    groups, order = {}, []

    def grp(key, text, col):
        if key not in groups:
            groups[key] = dict(text=text, col=col, pts=[])
            order.append(key)
        return groups[key]["pts"]
    for z in zones:
        c, sa = z["code"], (z.get("study_area") or u"")
        if c not in ("WT", "WD", "WS", "GR", "WA", "WP", "DG"):
            continue
        if sa.startswith("aras") and c in ("WT", "WD", "WS"):
            continue                                    # the steps 1, 2 and 4 mark them
        if c == "WA":
            fl = u"FLOOD" in (z.get("label") or u"").upper()
            key, txt = ("WA_fl", P12_ZOOM_TEXT["WA"]) if fl else ("WA_bed", P12_DEF["WA_bed"])
        elif c == "GR" and not sa.startswith("aras"):
            key, txt = "GR_dry", P12_DEF["GR_dry"]
        else:
            key, txt = c, P12_ZOOM_TEXT[c]
        grp(key, txt, P12_ZONE[c][2]).append((_p12_area(z["ring"]), _p12_cen(z["ring"])))
    # the stream's reaches: a zone near (or round) the Selinos line, else the wall, else the strip, else nothing
    near_m, strip_m, st_m, min_m, strip_min = P12_DEF_NEAR_M
    B = 25.0
    zi, si, zb = {}, {}, []
    for z in zones:
        idx = si if z["code"] == "STRIP" else zi
        for p in _p12_dense(z["ring"], 10.0, True):
            idx.setdefault((int(math.floor(p[0] / B)), int(math.floor(p[1] / B))), []).append(p)
        if z["code"] != "STRIP":
            zb.append((_p12_bbox(z["ring"]), z["ring"]))

    def near(idx, p, d):
        r_ = int(d / B) + 1
        i0, j0 = int(math.floor(p[0] / B)), int(math.floor(p[1] / B))
        for i in range(i0 - r_, i0 + r_ + 1):
            for j in range(j0 - r_, j0 + r_ + 1):
                for q in idx.get((i, j), ()):
                    if (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2 <= d * d:
                        return True
        return False
    study = basemap_study(D) if D else []
    if not study:
        log.append(u"p11 letters: no study-area outline in the basemap: the whole Selinos line checked (G18)")
    Ls, s_, runs = _p12_len(P12_SELINOS), 0.0, []
    while s_ <= Ls:
        p = _p12_along(P12_SELINOS, s_)[0]
        if study and not any(_p12_pip(p[0], p[1], R_) for R_ in study):
            cls = None
        elif near(zi, p, near_m) or any(b[0] <= p[0] <= b[2] and b[1] <= p[1] <= b[3] and _p12_pip(p[0], p[1], R_)
                                        for b, R_ in zb):
            cls = "zone"
        elif dz(p)[1]:
            cls = "wall"
        elif near(si, p, strip_m):
            cls = "strip"
        else:
            cls = "none"
        if runs and runs[-1][0] == cls:
            runs[-1][2] = s_
        else:
            runs.append([cls, s_, s_])
        s_ += st_m
    for cls, s0, s1 in runs:
        Lr = s1 - s0 + st_m
        if cls in (None, "zone") or Lr < min_m:
            continue
        pm = _p12_along(P12_SELINOS, (s0 + s1) / 2.0)[0]
        if cls == "wall":
            grp("wall", P12_ZOOM_TEXT["wall"], COL["ink"]).append((Lr, pm))
        elif cls == "strip":
            if Lr >= strip_min:
                grp("strip", P12_ZOOM_TEXT["strip"], MP["discharge"][2]).append((Lr, pm))
        else:
            grp("stream", P12_DEF["stream"], COL["river_mid"]).append((Lr, pm))
            log.append(u"FLAG p11 undefined reach {:.0f}-{:.0f} m along the Selinos line ({:.0f} m): no zone base "
                       u"element, no wall; keyed '{}'".format(s0, s1 + st_m, Lr, P12_DEF["stream"]))
    # where each group's markers go (the zoom for the spot), then letters in reading order of the first marker
    sp = I["spot"] if I else None
    placed, anchors = {}, []
    for key in order:
        ps = []
        for _a, c in sorted(groups[key]["pts"], key=lambda q: -q[0]):
            pm = Tg(c)
            if sp and sp[0] <= pm[0] <= sp[2] and sp[1] <= pm[1] <= sp[3]:
                pi = I["Tg"](c)
                bx = I["box"]
                if bx[0] < pi[0] < bx[2] and bx[1] < pi[1] < bx[3]:
                    ps.append((pi, True, pm))
            elif ga[0] < pm[0] < ga[2] and ga[1] < pm[1] < ga[3] and not \
                    (I and I["box"][0] <= pm[0] <= I["box"][2] and I["box"][1] <= pm[1] <= I["box"][3]):
                ps.append((pm, False, pm))
        if ps:
            placed[key] = ps
            anchors.append((key, ps[0][2]))
    out, r = [], P12_MARK_R
    obst = list(M["taken"])
    for ix in lp_reading_order([a_[1] for a_ in anchors], y_down=False):
        key = anchors[ix][0]
        g, got = groups[key], []
        for (x, y), in_z, _pm in placed[key]:
            if any(math.hypot(x - a_, y - b_) < 8.0 for a_, b_, _i in got):
                continue
            obs = [t for t in obst if not (in_z and t == I["box"])]
            b = _p12_free_spot(x, y, 2.0 * r, 2.0 * r, obs, I["box"] if in_z else ga)
            if b:
                got.append(((b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0, b))
                obst.append(b)
        if not got:
            log.append(u"p11 letters: no room for the marker of '{}'".format(g["text"]))
            continue
        ch_ = P12_LETTERS[len(out)] if len(out) < len(P12_LETTERS) else P12_LETTERS[-1]
        for x, y, b in got:
            M["labels"].append(_p12_letter(pg, ch_, x, y, g["col"]))
        out.append((ch_, g["text"], g["col"]))
    M["taken"] = obst
    log.append(u"p11 letters: {} along the channel ({})".format(len(out), u", ".join(c_ for c_, _t, _c in out)))
    return out


def _p12_step_rows(f, at):
    """R2 (31 Oct, G3): the five steps' texts for the column's key (_p12_steps), the map keeps only their numbered
    markers: [(n, icon, head, big, small lines)] for each step the map marks (at[n]); every figure read live from the
    water balance results (_p12_figures), never typed in"""
    rows = []
    take, site = f["collect"]
    if at.get(1):
        sm = []
        if take is not None:
            sm.append(u"{:,.0f} m³ from the winter stream".format(take))
        if site is not None:
            sm.append(u"{:,.0f} m³ street + roof runoff".format(site))
        rows.append((1, "rain", u"1 COLLECT", u"{:,.0f} m³ a year".format((take or 0) + (site or 0)) if sm else None,
                     sm))
    if at.get(2):
        rows.append((2, "reeds", u"2 CLEAN", u"{:,.0f} m² of reed basins".format(f["reed_m2"]) if f["reed_m2"] else None,
                     [u"lined, root-contained · cleaned once,", u"then the whole reach runs clean"]))
    if at.get(3):
        rows.append((3, "storage", u"3 HOLD", u"{:,.0f}-{:,.0f} m³".format(*f["store"]) if f["store"] else None,
                     [u"winter water held in the ground,", u"at most a year · cube at the map's scale"]))
    if at.get(4):
        sm = [u"spillway: overflow back to the stream"]
        if f["left"]:
            sm.append(u"of its winter flow · driest year {:.0f} %".format(math.floor(f["left"][0])))
        rows.append((4, "stream", u"4 GIVE BACK",
                     u"{:.0f} % stays in the stream".format(math.floor(f["left"][1])) if f["left"] else None,
                     sm[::-1] if f["left"] else sm))
    sm = [u"the clean stream leaves the site"]
    if f["farm_ha"]:
        sm.append(u"for {:.1f} ha of farms outside it".format(f["farm_ha"]))
    rows.append((5, "stream_out", u"5 TO THE FARMS", u"{:,.0f} m³ a year".format(f["farms"]) if f["farms"] else None,
                 sm))
    return rows


def _p12_map_labels(pg, ga, M, zones, f, D, log):
    """G3 (v12, round 3): on the map only place names, on or right next to their point, never on a leader: in the
    zoom of the upstream entry first the definition of the winter store beside its cube (the blue box, P11.2) and
    the short names of its parts; then the chain's places by their real names (G16), the stream's name and a few of
    the base data's names round Üç Kemer (the brief's base-data check). The project's zones are letters
    (_p12_letters), the steps numbers, the summer strip in the section (D2). Returns the drawn text boxes (for the
    overlap test)."""
    Tg, taken, segs = M["Tg"], M["taken"], M["segs"]
    boxes = []
    I = M.get("inset")
    if I:
        bx = I["box"]
        tk = [t for t in taken if t != bx]
        cb = I["Sc"]["cube_b"]
        if cb and f.get("store"):
            l1, l2 = u"WINTER STORE · in the ground", u"{:,.0f}-{:,.0f} m³ · cube to scale".format(*f["store"])
            s1 = 3.0
            w = max(text_w(l1, s1, True), text_w(l2, FS_MIN)) + 0.6
            h = s1 * CAP + 1.2 + FS_MIN * CAP + FS_MIN * 0.35 + 0.6
            cxc, cyc = (cb[0] + cb[2]) / 2.0, (cb[1] + cb[3]) / 2.0
            got = None
            for gx, gy in ((cb[2] + 1.0, cyc - h / 2.0), (cb[0] - 1.0 - w, cyc - h / 2.0), (cxc - w / 2.0, cb[3] + 1.0),
                           (cxc - w / 2.0, cb[1] - 1.0 - h)):
                b = (gx, gy, gx + w, gy + h)
                if b[0] < bx[0] + 0.5 or b[1] < bx[1] + 0.5 or b[2] > bx[2] - 0.5 or b[3] > bx[3] - 0.5:
                    continue
                if not any(lp_hit(b, t, 0.3) for t in tk):
                    got = b
                    break
            if got is None:
                got = _p12_free_spot(cxc, cyc, w, h, tk + [cb], bx, (8.0, 12.0, 16.0, 20.0, 25.0, 30.0), 24)
            if got:
                y_ = got[3] - s1 * CAP - 0.3
                pg.text(l1, got[0] + 0.3, y_, s1, MP["storage"][2], bold=True)
                pg.text(l2, got[0] + 0.3, y_ - 1.2 - FS_MIN * CAP, FS_MIN, MP["storage"][2])
                tk.append(got)
                taken.append(got)
                boxes.append(got)
            else:
                log.append(u"FLAG p11 map: no room in the zoom beside the winter store for its definition")
        nms = []
        for code, head in (("WT", u"Reed basins"), ("WD", u"Spillway"), ("WS", u"Dry-top terraces")):
            zz = _p12_pick(zones, code, "aras")
            if zz:
                c = I["Tg"](_p12_cen(zz[0]["ring"]))
                nms.append(dict(x=c[0], y=c[1], head=head, col=P12_ZONE[code][2]))
        nb = _p12_place(pg, nms, tk, bx, (), log)
        taken.extend(nb)
        boxes += nb
    pl = [dict(x=Tg(p)[0], y=Tg(p)[1], head=_p12_place_nm(nm)) for nm, p in P12_PLACES]
    q = _p12_along(M["S"], 0.55 * _p12_len(M["S"]))[0]
    pl.append(dict(x=q[0], y=q[1], head=place_name("stream")))
    inside = lambda s_: ga[0] < s_["x"] < ga[2] and ga[1] < s_["y"] < ga[3] and not \
        (I and I["box"][0] <= s_["x"] <= I["box"][2] and I["box"][1] <= s_["y"] <= I["box"][3])
    boxes += _p12_place(pg, [s_ for s_ in pl if inside(s_)], taken, ga, segs, log)
    k5 = dict(P12_PLACES).get(u"K5")
    if k5 and D:
        R = P12_K5_CHECK_M
        nm = sorted(basemap_names((k5[0] - R, k5[1] - R, k5[0] + R, k5[1] + R), D),
                    key=lambda q_: math.hypot(q_[1][0] - k5[0], q_[1][1] - k5[1]))[:P12_K5_NAMES]
        sp = [dict(x=Tg(p)[0], y=Tg(p)[1], head=n) for n, p in nm]
        boxes += _p12_place(pg, [s_ for s_ in sp if inside(s_)], taken, ga, segs, log)
    return boxes


# ---------------------------------------------------------------- up close: the upstream entry in section (D1 a + b)
def _p12_cross_u(R, o, e):
    """the u (m along the unit vector e from o) where the line o + u e crosses the ring R, sorted"""
    n = (-e[1], e[0])
    out = []
    for i in range(len(R)):
        p, q = R[i], R[(i + 1) % len(R)]
        vp = (p[0] - o[0]) * n[0] + (p[1] - o[1]) * n[1]
        vq = (q[0] - o[0]) * n[0] + (q[1] - o[1]) * n[1]
        if (vp > 0.0) != (vq > 0.0):
            t = vp / (vp - vq)
            x, y = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
            out.append((x - o[0]) * e[0] + (y - o[1]) * e[1])
    return sorted(out)


def _p12_free(iv, occ):
    """the parts of the interval iv not covered by the intervals occ"""
    out = [iv]
    for a, b in occ:
        nxt = []
        for c, d in out:
            if b <= c or a >= d:
                nxt.append((c, d))
                continue
            if a > c:
                nxt.append((c, a))
            if b < d:
                nxt.append((b, d))
        out = nxt
    return [(c, d) for c, d in out if d - c > 1.0]


def _p12_zoom_geom(zones, D, max_m, log):
    """the up-close section, survey m, from data only: a cut parallel to the registry cut P12_ZOOM_CUT (W1, the
    upstream entry), moved along the stream to where it crosses the most of the upstream entry's zones (reed
    basins, spillway, shaded walk, dry-top terraces); from P12_ZOOM_BANK_M beyond the far wall to the last of those
    zones (cut to max_m, the band's room at 1:P12_ZOOM_DEN). The levels are the cut's registry levels. None (logged)
    when the zones, the registry cut or the stream are missing."""
    up = [z for z in zones if (z.get("study_area") or u"").startswith("aras") and z["code"] in ("WT", "WD", "GR", "WS")]
    L = (D or {}).get("layers") if D else None
    if not up or not L:
        log.append(u"p.12: no upstream-entry zones or no basemap: the up-close section is left out (map full height)")
        return None
    try:
        a, b = level_ends(P12_ZOOM_CUT)
        reg = level_registry(P12_ZOOM_CUT)
    except Exception as ex:
        log.append(u"p.12: cut {} not in the level registry ({}): the up-close section is left out".format(P12_ZOOM_CUT,
                                                                                                         ex))
        return None
    tops = [t for _ty, t in reg["walls"].values() if t is not None]
    if reg["bed"] is None or reg["avg_flow"] is None or not tops:
        log.append(u"p.12: cut {} has no bed, average flow or bank top: the up-close section is left out".format(
            P12_ZOOM_CUT))
        return None
    Lc = math.hypot(b[0] - a[0], b[1] - a[1])
    e = ((b[0] - a[0]) / Lc, (b[1] - a[1]) / Lc)          # SW -> NE (the registry's end order)
    n = (-e[1], e[0])
    c = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)
    ivs = []
    for z in up:
        vs = [(p[0] - c[0]) * n[0] + (p[1] - c[1]) * n[1] for p in z["ring"]]
        ivs.append((min(vs), max(vs)))
    ends = sorted(set(v for iv in ivs for v in iv))
    best = None
    for i in range(len(ends) - 1):
        vm = (ends[i] + ends[i + 1]) / 2.0
        cnt = sum(1 for lo, hi in ivs if lo < vm < hi)
        if best is None or cnt > best[0]:
            best = (cnt, vm)
    if not best:
        return None
    o = (c[0] + n[0] * best[1], c[1] + n[1] * best[1])
    wet = []
    for g in L.get("water") or []:
        if g and len(g[0]) >= 3:
            us = _p12_cross_u(g[0], o, e)
            wet += [(us[i], us[i + 1]) for i in range(0, len(us) - 1, 2)]
    if not wet:
        log.append(u"p.12: the up-close cut does not cross the surveyed stream: the section is left out")
        return None
    wl, wr = min(wet, key=lambda w_: abs((w_[0] + w_[1]) / 2.0))
    t = P12_WALL_T
    els, occ = [], [(wl - t, wr + t)]
    for code in ("WT", "WD", "GR", "WS", "WP", "DG", "WA"):
        for z in zones:
            if z["code"] != code:
                continue
            us = _p12_cross_u(z["ring"], o, e)
            for i in range(0, len(us) - 1, 2):
                for ua, ub in _p12_free((us[i], us[i + 1]), occ):
                    els.append((code, ua, ub))
                    occ.append((ua, ub))
    strip = []
    for z in zones:
        if z["code"] == "STRIP":
            us = _p12_cross_u(z["ring"], o, e)
            strip += [(max(wl, us[i]), min(wr, us[i + 1])) for i in range(0, len(us) - 1, 2)
                      if min(wr, us[i + 1]) - max(wl, us[i]) > 0.5]
    u0 = wl - t - P12_ZOOM_BANK_M
    u1 = max([ub for c_, ua, ub in els if c_ in ("WT", "WD", "GR", "WS")] or [wr + 20.0]) + 6.0
    trimmed = u1 - u0 > max_m
    if trimmed:
        u1 = u0 + max_m
    els = sorted([(c_, max(ua, u0), min(ub, u1)) for c_, ua, ub in els if ua < u1 - 1.0 and ub > u0 + 1.0],
                 key=lambda t_: t_[1])
    log.append(u"p.12: the up-close section crosses {} ({:.0f} m{})".format(
        u", ".join(c_ for c_, _a, _b in els) or u"the stream only", u1 - u0, u", cut at the band" if trimmed else u""))
    return dict(o=o, e=e, u0=u0, u1=u1, wet=(wl, wr), els=els, strip=strip, bed=reg["bed"], avg=reg["avg_flow"],
                top=sum(tops) / len(tops), walled=bool(reg["walled"]), trimmed=trimmed, q100=reg.get("q100"),
                q500=reg.get("q500"),
                reg_t=(o[0] - a[0]) * e[0] + (o[1] - a[1]) * e[1], reg_d=(o[0] - a[0]) * n[0] + (o[1] - a[1]) * n[1],
                A=(o[0] + e[0] * u0, o[1] + e[1] * u0), B=(o[0] + e[0] * u1, o[1] + e[1] * u1),
                units=list(L.get("buildings") or []))


def _p12_group_text(keys, tags):
    """R2 (G9): the callout of one planting group, "Element: reason" (<= 55 letters): its species, what it does
    (plants.py purpose tags, sure only); None when no sourced purpose is known"""
    does = [P12_GROUP_DO[t_] for t_ in PLA_TAGS if t_ in tags and t_ in P12_GROUP_DO][:2]
    if not does:
        return None
    nm = []
    for q in keys:
        w_ = PLA_SPECIES[q]["name"]
        nm.append(w_.lower() if w_.split()[-1].lower() == "tree" else w_.split()[-1].lower())
    tail = u": " + u", ".join(does)
    n = min(3, len(nm))
    while n > 1 and len(u" + ".join(nm[:n]) + tail) > 55:
        n -= 1
    s = u" + ".join(nm[:n]) + tail
    return s[:1].upper() + s[1:]


def _p12_zoom(pg, band, Z, style, log, f=None):
    """the up-close section in the band (page mm, y up) at 1:P12_ZOOM_DEN, in style "a" (cutout people and trees over
    the same drawn ground, D1 a) or "b" (vector, D1 b), from ONE geometry Z: the cut ground (survey buildings in cut,
    M11), the stone walls and the bed with the water at average yearly flow, the summer strip, Q100 / Q500 (M5, G8,
    the registry levels of P12_ZOOM_CUT), and each zone as the place it is (G10): the lined reed basins with people
    on the paths between the cells, the stone spillway, the shaded walk with mixed tree groups, a bench and walkers,
    the dry-top terraces with low planting round a lawn where children play. R2 (31 Oct): the designed sky (D8);
    the basemap houses behind the cut on the depth layers' ground, under that layer's trees (pass 2, checklist 7);
    the back trees stand on a ground that dips into the channel (walls and bed) and none where the water is (G14);
    planting in mixed groups on depth layers (G9, pla_group_section), people by zone (G10, fig_place_zones, nobody
    in the water), every item seated (sf_g14_line logged); numbered callouts "Element: reason", one per planting
    group saying what it does; the key on the left, the water legend and the scale bar on the right (G1, G3).
    Everything at true size (G6, logged). v12 (round 3, G15): the sky with birds and its own variant (cid), the
    callouts numbered left to right (G3), people fishing and watching at the far wall, a lamp on the shaded walk,
    a zoom of the reed basins (people legible), the cut's levels (m, 2 decimals) and the summer strip's figures
    (moved off the map, D2) under the scale bar, the cut's ends named (D6). Returns the text boxes it drew."""
    x0, y0, x1, y1 = band
    den = P12_ZOOM_DEN
    k = sf_k(den)
    sx = x0 + P12_ZOOM_KEY_W + 6.0
    u0, u1 = Z["u0"], Z["u1"]
    X = lambda u: sx + (u - u0) * k
    yb = y0 + 1.0
    y_of = sf_y_of(Z["bed"] - STRIP_DEPTH - 1.0, yb, k)
    gy, bed_y, avg_y = y_of(Z["top"]), y_of(Z["bed"]), y_of(Z["avg"])
    sky = (y1 - 1.0 - gy) / k                           # m of room over the ground
    allow = [q for q in PLA_NICHE if PLA_SPECIES[q]["h_m"] * 1.08 <= sky - 0.3]
    back = [q for q in PLA_NICHE if PLA_SPECIES[q]["layer"] == "tree" and PLA_SPECIES[q]["h_m"] * 1.08 * 0.8 <= sky - 0.3]
    W = water_layers()
    co = SfCallouts()
    wl, wr = Z["wet"]
    t = P12_WALL_T * k
    xa_s, xb_s = X(u0), X(u1)
    # the depth layers' ground (G14): the bank tops, down the walls into the bed (walls a hair battered so the
    # profile stays a function of x); with water = the average flow no back tree stands over the channel
    bprof = [(xa_s, gy), (X(wl), gy), (X(wl) + 0.01, bed_y), (X(wr) - 0.01, bed_y), (X(wr), gy), (xb_s, gy)]
    sf_atmosphere(xa_s, xb_s, gy, y1 - 0.5, k, seed=5, sky="d8", trees=False, birds=True, style=style, into=W,
                  back_ground={2: bprof, 1: bprof}, groups=True, water=avg_y, cid="p11_up")
    pend = []                                           # v12: the callouts, numbered left to right at the end (G3)
    # R2-C pass 2 (Aras 31 Oct 12:01 "no background houses"): layer by layer, farthest first, the basemap houses
    # SF_BACK_BAND m behind this cut (sf_back_buildings on the registry cut, shifted to this parallel cut: reg_t
    # along, reg_d behind) on the layer's own ground at their data height (else floors x BLD_STOREY), then that
    # layer's trees round them; none over the channel (it runs on behind the cut), none whose roof leaves the band
    gfn, ch = sf_gy(bprof), (X(wl) - t, X(wr) + t)
    dm = 0.5 * (SF_BACK_BAND[0] + SF_BACK_BAND[1])
    hl = sf_back_buildings(P12_ZOOM_CUT, u0 + Z["reg_t"], u1 + Z["reg_t"], SF_BACK_BAND[0] + Z["reg_d"],
                           SF_BACK_BAND[1] + Z["reg_d"], log=log)
    nh, nx, hbx = 0, 0, []
    for layer_ in (2, 1):
        hs = []
        for ta, tb, h_m, fl, d in hl:
            if (1 if d - Z["reg_d"] < dm else 2) != layer_ or tb - ta < 3.0:   # 3.0 m: sf_back_house's one bay
                continue
            ha, hb = X(ta - Z["reg_t"]), X(tb - Z["reg_t"])
            if hb > ch[0] and ha < ch[1]:
                nx += 1
                continue
            hsh = sf_back_house(ha, hb, gfn, h_m, k, layer=layer_, floors=fl)
            if max(p_[1] for s_ in hsh for p_ in s_[1]) > y1 - 0.5:
                nx += 1
                continue
            W.add("background", hsh)
            hs.append((ha, hb))
            hbx.append(_p12_bbox([p_ for s_ in hsh if s_[0] in ("poly", "line") for p_ in s_[1]]))
            nh += 1
        if back:
            sh_, _pl, _gr = pla_group_section(xa_s, xb_s, gfn, k, t0=0.45, t1=0.95, mix=back, seed=5 + 31 * layer_,
                                              layers=(layer_,), style=style, density=0.5, avoid=hs or None,
                                              hires=False, detail=False, water=avg_y)
            W.add("background", sh_)
    log.append(u"p.12 up close: {} background houses drawn ({} left out: over the channel or above the band)".format(
        nh, nx))
    # the cut ground, the walls, the bed and the water (G8: never dry; Q100 / Q500 wall to wall)
    for surf in ([(xa_s, gy), (X(wl) - t, gy)], [(X(wr) + t, gy), (xb_s, gy)]):
        if surf[1][0] - surf[0][0] > 0.2:
            sf_ground(surf, k, bottom_y=yb, into=W)
    wall = "stone" if Z["walled"] else "earth"
    for xw in (X(wl) - t, X(wr)):
        W.add("ground", sct_hatch_fill([(xw, yb), (xw + t, yb), (xw + t, gy), (xw, gy)], wall, k, SCT["cut"], 0.25))
    W.add("ground", sct_hatch_fill([(X(wl), yb), (X(wr), yb), (X(wr), bed_y - 0.6 * k), (X(wl), bed_y - 0.6 * k)],
                                   "earth", k))
    prof = [(X(wl), gy), (X(wl), bed_y)]
    for sa, sb_ in sorted(Z["strip"]):
        prof += [(X(sa), bed_y), (X(sa), bed_y - STRIP_DEPTH * k), (X(sb_), bed_y - STRIP_DEPTH * k), (X(sb_), bed_y)]
    prof += [(X(wr), bed_y), (X(wr), gy)]
    water_section(prof, k, y_of, cid=P12_ZOOM_CUT, fill_ground=False, labels=False, into=W)
    W.add("ground", [("line", prof, SCT["cut"], 0.35)])
    if Z["walled"]:
        pend.append((X(wr) + t / 2.0, bed_y - 2.2, P12_ZOOM_TEXT["wall"]))   # in the cut, under the water lines
    for sa, sb_ in Z["strip"][:1]:
        pend.append((X((sa + sb_) / 2.0), bed_y + 3.4, P12_ZOOM_TEXT["strip"]))   # between average flow and Q100
    # the survey's buildings the cut passes through (M11, their own heights; any taller than the band is left out)
    its = bld_section_items(Z["A"], Z["B"], Z["units"], ground=lambda x_, y_: Z["top"])
    for it in its:
        if it[0] == "fill":
            for R in it[1]:
                pts = [(X(u0 + s_), y_of(z_)) for s_, z_ in R]
                if len(pts) >= 3 and max(p[1] for p in pts) <= y1 - 0.3:
                    W.add("structures", [("poly", pts, it[2], None, 0.1)])
        elif it[0] == "line":
            pts = [(X(u0 + s_), y_of(z_)) for s_, z_ in it[1]]
            if len(pts) >= 2 and max(p[1] for p in pts) <= y1 - 0.3:
                W.add("structures", [("line", pts, it[2], it[3], it[4])])
    # the zones as places (G10): people by zone kind (nobody where the water is), planting in mixed groups (G9)
    trees, groups, people, planted = [], [], [], set()

    def plant(xa_, xb_, t0_, t1_, mix_, seed_, dens, avoid_=None):
        if not mix_:
            return False
        sh_, pl_, gr_ = pla_group_section(xa_, xb_, gy, k, t0=t0_, t1=t1_, mix=mix_, seed=seed_, style=style,
                                          density=dens, avoid=avoid_, water=avg_y)
        W.add("vegetation", sh_)
        trees.extend(pl_)
        groups.extend(gr_)
        return bool(gr_)

    # R2-C pass 2 (scenes): who stays looks at what the place is for: the reed basins, else the stream
    looks = [X((wl + wr) / 2.0)] + [(X(ua_) + X(ub_)) / 2.0 for c_, ua_, ub_ in Z["els"] if c_ == "WT"]

    def crowd(zs_, seed_, layer_=0, dens=0.8, mx=None, focus=None):
        fz = focus or (lambda _k, xa_, xb_: min(looks, key=lambda q: abs(q - (xa_ + xb_) / 2.0)))
        sh_, pl_ = fig_place_zones(zs_, gy, k, seed=seed_, layer=layer_, style=style, density=dens, water=avg_y,
                                   max_per_zone=mx, focus=fz)
        W.add("figures", sh_)
        people.extend(pl_)
    near = X(wr) + t                                    # the stream's NE wall face: where "toward the stream" points
    for i, (code, ua, ub) in enumerate(Z["els"]):
        xa, xb = X(ua), X(ub)
        xm = (xa + xb) / 2.0
        sgn = -1.0 if xm > near else 1.0
        if code == "WT":                                # lined reed cells, as p.22 (P12_BASIN drawing values)
            ln, gap, fl, media, wat = P12_BASIN
            u, cells = ua + 0.3, []
            while u + 2.0 <= ub - 0.3:
                ue = min(u + ln, ub - 0.3)
                W.add("structures", [("poly", [(X(u), gy - (fl - wat) * k), (X(ue), gy - (fl - wat) * k), (X(ue), gy),
                                               (X(u), gy)], COL["white"], None, 0.1)])      # the open cell over the water
                W.add("structures", pla_reed_basin(X(u), X(ue), gy - fl * k, gy, k, P12_KERB_H, media_m=media,
                                                   wl_y=gy - (fl - wat) * k))
                cells.append((u, ue))
                u = ue + gap
            # the edge between the cells: people watching the basins (viewing terrace kind, one each)
            cf = dict((round(X(a_[1]) + 0.1 * k, 3), X((a_[0] + a_[1]) / 2.0)) for a_ in cells)
            crowd([("viewing_terrace", X(a_[1]) + 0.1 * k, X(b_[0]) - 0.1 * k) for a_, b_ in zip(cells, cells[1:])
                   if X(a_[1]) > near], 41 + i, mx=1,
                  focus=lambda _k, xa_, xb_: cf.get(round(xa_, 3), (xa_ + xb_) / 2.0))   # the cell beside them
        elif code == "WD":                              # the stone spillway, back to the stream
            W.add("structures", sct_hatch_fill([(xa, gy - 0.4 * k), (xb, gy - 0.4 * k), (xb, gy), (xa, gy)], "stone",
                                               k, SCT["cut"], 0.2))
            W.add("water", [("line", [(xa, gy - 0.06 * k), (xb, gy - 0.06 * k)], _wat_pal()["deep"], 0.35)])
            ax0, ax1 = xm - sgn * 3.0, xm + sgn * 3.0
            W.add("labels", [("line", [(ax0, gy + 1.4), (ax1, gy + 1.4)], COL["river_mid"], 0.3),
                             ("poly", [(ax1 + sgn * 1.2, gy + 1.4), (ax1, gy + 2.0), (ax1, gy + 0.8)], COL["river_mid"],
                              None, 0.1)])
        elif code == "GR":                              # the shaded walk: gravel, tree groups, a bench in the shade
            W.add("ground", sf_lane(xa, gy, ub - ua, k, kind="gravel"))
            if xb - xa > 14.0:
                xbch = xa + 0.35 * (xb - xa)
                an = fig_meta("sit_step", facing=1, seat_h=SF_SEAT_H)
                xs_ = xbch + 0.225 * k - an.get("seat_x", 0.0) * k
                ys_ = sf_seat_x(gy, xbch + 0.225 * k, 0.6 * k)   # G14: bench and sitter on the same seated ground
                W.add("structures", sf_bench(xbch, ys_, k))
                W.add("structures", sf_lamp(xa + 0.12 * (xb - xa), gy, k, side=1))   # v12 (G15): the walk lit at night
                W.add("figures", fig_side("sit_step", xs_, ys_, k, facing=1, seat_h=SF_SEAT_H, style=style))
                people.append((u"bench", u"sit_step", xs_))
                free = [(xbch - 1.0 * k, xbch + 1.5 * k)]
                crowd([("walkway", xa + 0.5, xbch - 1.0 * k), ("walkway", xbch + 1.5 * k, xb - 0.5)], 3 + i)
            else:
                free = None
                crowd([("walkway", xa + 0.5, xb - 0.5)], 3 + i)
            crowd([("walkway", xa + 0.5, xb - 0.5)], 13 + i, layer_=1, dens=0.4)     # further off: smaller, paler
            if plant(xa, xb, 0.45, 0.7, allow, 11 + i, 0.9, free):
                planted.add(code)
        elif code == "WS":                              # the dry-top terraces: low planting round a play lawn
            W.add("ground", [("line", [(xa, gy + 0.05), (xb, gy + 0.05)], MP["park"][1], 0.45)])
            pa, pb = xa + 0.3 * (xb - xa), xb - 0.3 * (xb - xa)
            low = [q for q in allow if PLA_NICHE[q][0] >= 0.5]
            if plant(xa, xb, 0.8, 1.0, low, 21 + i, 0.6, [(pa, pb)]):
                planted.add(code)
            crowd([("lawn", pa, pb)], 23 + i)
            crowd([("lawn", xa + 0.5, xb - 0.5)], 33 + i, layer_=1, dens=0.35)
        elif code in ("WP", "DG"):                      # planting: wet band by the stream, Demeter's garden dry
            mix = [q for q in allow if (q in ("olive", "rosemary", "lavender")) == (code == "DG")]
            if plant(xa, xb, 0.05 if code == "WP" else 0.8, 0.4 if code == "WP" else 1.0, mix, 31 + i, 1.0):
                planted.add(code)
        if code in P12_ZOOM_TEXT and xb - xa > 3.0 and not (code == "WP" and code in planted):   # v10: DG keeps its name (G10)
            if code == "WT":                            # the mark in the cut ground, under the element
                ym = gy - (P12_BASIN[2] + 0.4) * k - 1.6
            elif code == "WD":
                ym = gy - 0.4 * k - 1.8
            else:
                ym = gy - 2.2
            pend.append((xm, ym, P12_ZOOM_TEXT[code]))
    # G15 (v12): on the far wall's top people fish and watch the water (water_edge: nobody in it)
    if X(wl) - t - xa_s > 6.0:
        crowd([("water_edge", max(xa_s + 0.5, X(wl) - t - 8.0), X(wl) - t - 0.3)], 51,
              focus=lambda _k, xa_, xb_: X((wl + wr) / 2.0))
    # one callout per planting group (G9): what it does there; the mark in the cut ground under the group, a row
    # below the zones' marks; a group right behind another one's mark shares it
    gm, ng = [], 0
    room = int((y1 - 3.0 * CAP - 3.1 - y0) / (1.5 * FS_MIN))     # v10: key lines that fit beside the band (G3)
    for layer_, ga_, gb_, ks, tags in sorted(groups, key=lambda g_: (g_[0], g_[1])):
        if layer_ == 2:
            continue
        if len(set(q[2] for q in pend)) >= room:
            log.append(u"p.12 up close: the key is full ({} lines): further planting groups not called out".format(room))
            break
        txt = _p12_group_text(ks, tags)
        if not txt:
            log.append(u"p.12 up close: a group of {} has no sourced purpose (no callout)".format(u", ".join(ks)))
            continue
        xg = (ga_ + gb_) / 2.0
        if any(abs(xg - q) < 3.6 for q in gm):
            continue
        gm.append(xg)
        pend.append((xg, max(yb + 1.9, gy - 5.6), txt))
        ng += 1
    for x_, y_, t_ in sorted(pend, key=lambda q: (round(q[0], 1), -q[1])):   # G3: numbered left to right
        co.add(x_, y_, t_)
    W.add("labels", co.marks(size=FS_MIN))
    _p12_shapes(pg, W.shapes())
    boxes = []
    # G15 zoom (v12): the reed basins with the people on their paths at a legible size, in the sky over the channel
    # beside them (one short connector), clear of the houses behind; left out (logged) when there is no such room
    wt_ = [(ua_, ub_) for c_, ua_, ub_ in Z["els"] if c_ == "WT"]
    zi = None
    if wt_:
        sx0 = X(wt_[0][0])
        sx1 = min(X(wt_[0][1]), sx0 + P12_ZOOM_SPOT[0])
        sy0, sy1 = gy - (P12_BASIN[2] + 0.3) * k, gy + 2.2 * k
        fz_ = P12_ZOOM_SPOT[1]
        w_, h_ = (sx1 - sx0) * fz_, (sy1 - sy0) * fz_
        ztop = y1 - 1.0 - FS_MIN * 1.4
        for dx0 in (sx0 - 3.0 - w_, sx1 + 3.0):
            d_ = (dx0, ztop - h_, dx0 + w_, ztop)
            if d_[0] < xa_s or d_[2] > xb_s or d_[1] < gy + 1.0 or any(lp_hit(d_, hb_) for hb_ in hbx):
                continue
            zi = d_
            break
        if zi:
            _p12_shapes(pg, sf_zoom_inset((sx0, sy0, sx1, sy1), zi, k, k * fz_, W, u"reed basins", size=FS_MIN))
            boxes.append((zi[0], zi[3], zi[0] + text_w(u"ZOOMED IN · reed basins", FS_MIN, True),
                          zi[3] + 0.6 * FS_MIN + FS_MIN * CAP))
            log.append(u"p11 up close: the reed basins zoomed x{:.1f} (people {:.1f} mm high)".format(
                fz_, 1.75 * k * fz_))
        else:
            log.append(u"p11 up close: no free sky beside the reed basins for their zoom (left out)")
    # the cut's ends (D6): A, A' as on the map, the banks by place
    for s_, x_, al in ((u"A · " + place_name("side_SW"), xa_s + 0.8, "L"),
                       (place_name("side_NE") + u" · A'", xb_s - 0.8, "R")):
        pg.text(s_, x_, yb + 0.6, FS_MIN, COL["ink2"], align=al)
        w_ = text_w(s_, FS_MIN)
        boxes.append((x_ - (w_ if al == "R" else 0.0), yb + 0.4, x_ + (0.0 if al == "R" else w_),
                      yb + 0.6 + FS_MIN * CAP))
    if Z["trimmed"]:
        break_mark(pg, xb_s, yb, gy + 2.0)
    bad = sf_assert_g6(k, trees=[(q[0], q[2]) for q in trees], strict=False)
    for s_ in bad:
        log.append(u"p.12 up close: " + s_)
    log.append(u"p.12 up close: {} planting groups ({} called out), {} people ({})".format(
        len(groups), ng, len(people), u", ".join(sorted(set(q[1] for q in people))) or u"none"))
    gl = sf_g14_line()
    if gl:
        log.append(u"p.12 up close: " + gl)
    # the key column: title, callout key (left); the water legend and the scale bar right of the drawing (R2, G3)
    yy = y1 - 3.0 * CAP - 0.5
    tt = u"UP CLOSE · the upstream entry in section A-A'"
    pg.text(tt, x0, yy, 3.0, COL["ink_dark"], bold=True)
    boxes.append((x0, yy - 0.2, x0 + text_w(tt, 3.0, True), yy + 3.0 * CAP))
    sz = FS_MIN                                          # v10: the shared callout size (p.12, p.17), the booklet's least text
    yk = yy - 2.6
    _p12_shapes(pg, co.key(x0, yk, size=sz))
    seen = []
    for n_, _x, _y, t_ in sorted(co.items):
        if n_ in seen:
            continue
        seen.append(n_)
        yr = yk - (len(seen) - 1) * 1.5 * sz - 0.76 * sz
        boxes.append((x0, yr - 0.25 * sz, x0 + 2.0 * sz + text_w(t_, sz), yr + CAP * sz))
    nk = len(seen)
    if yk - nk * 1.5 * sz < y0:
        log.append(u"p.12 up close: the callout key ({} lines) runs {:.1f} mm below the band".format(
            nk, y0 - (yk - nk * 1.5 * sz)))
    xl = xb_s + 4.0
    _p12_shapes(pg, water_legend(xl, y1 - 1.0, size=sz, floods=True))
    yb_ = y1 - 1.0 - 4 * 1.6 * sz - 3.4
    _p12_bar(pg, xl, yb_, den, P12_ZOOM_BAR)
    ys = yb_ - FS_MIN * 1.4
    pg.text(sf_scale_text(den), xl, ys, FS_MIN, COL["ink_dark"], bold=True)
    # checklist 10 (v12): the cut's levels in m with 2 decimals, then the summer strip's figures (off the map, D2)
    lines = [(u"{} levels: bed +{:.2f}".format(P12_ZOOM_CUT, Z["bed"]), COL["ink_dark"]),
             (u"average flow +{:.2f}".format(Z["avg"]), COL["ink_dark"])]
    if Z.get("q100") is not None and Z.get("q500") is not None:
        lines.append((u"Q100 +{:.2f} · Q500 +{:.2f}".format(Z["q100"], Z["q500"]), COL["ink_dark"]))
    if f and f.get("strip"):
        lines += [(u"Summer strip 400 × {:.0f} cm · {:,.0f} m".format(STRIP_DEPTH * 100.0, f["strip"][0]),
                   MP["discharge"][2]),
                  (u"first fill {:,.0f} m³".format(f["strip"][1]), MP["discharge"][2]),
                  (u"{:,.0f} m³ a summer".format(f["strip"][2]), MP["discharge"][2])]
    wmax, joined = x1 - xl - 0.3, []
    for t_, c_ in lines:                                 # two short lines of one kind share a line when they fit
        if joined and joined[-1][1] == c_ and text_w(joined[-1][0] + u" · " + t_, FS_MIN) <= wmax:
            joined[-1] = (joined[-1][0] + u" · " + t_, c_)
        else:
            joined.append((t_, c_))
    for i, (t_, c_) in enumerate(joined):
        yl = ys - (i + 1) * FS_MIN * 1.3
        if yl - 0.25 * FS_MIN < y0:
            log.append(u"FLAG p11 up close: {} of the level and strip lines do not fit under the scale bar".format(
                len(joined) - i))
            break
        pg.text(t_, xl, yl, FS_MIN, c_)
        boxes.append((xl, yl - 0.25 * FS_MIN, xl + text_w(t_, FS_MIN), yl + CAP * FS_MIN))
    log.append(u"p.12: the up-close section (style {}) at {}".format(style, sf_scale_text(den)))
    return boxes


# ---------------------------------------------------------------- beside the map (G7): two charts, why
def _p12_head(pg, x, y, w, title, sub=None):
    """a block head of the column: a hairline, the title (the takeaway), one keyword line; returns the y under it"""
    pg.line([(x, y), (x + w, y)], COL["structure"], 0.3)
    size = 3.8
    while size > 3.0 and text_w(title, size, True) > w:
        size -= 0.1
    y -= 3.8 * CAP + 1.6
    pg.text(title, x, y, size, COL["ink_dark"], bold=True)
    if sub:
        y -= FS_MIN * 1.45
        pg.text(sub, x, y, FS_MIN, COL["ink2"])
    return y - 3.0


def _p12_coliforms(pg, x, y, w):
    """G7: the coliform figures as a chart on one log axis (left after a wetland against the reuse limits), and
    the move they lead to (UV where people touch the water)"""
    y = _p12_head(pg, x, y, w, u"NOT CLEAN ENOUGH TO TOUCH WITHOUT UV",
                  u"coliform bacteria per 100 ml, log scale")
    lx = x + 44.0                                     # the zero column, then 1 .. 100,000
    a0, a1 = lx + 7.0, x + w - 6.0
    pos = lambda v: a0 + (a1 - a0) * math.log10(max(v, 1.0)) / 5.0
    rows = [(COLIFORM[0][0], COLIFORM[0][1], COLIFORM[0][2], MP["wetland"][1], COLIFORM[0][4])] + \
           [(lab, lo, hi, C["acc"], src) for lab, lo, hi, _, src in COLIFORM[1:]]
    top = y + 1.0
    for i, (lab, lo, hi, col, src) in enumerate(rows):
        yy = y - i * 5.2
        pg.text(lab, x, yy - 0.9, FS_MIN, COL["ink"])
        c = cite(src)
        if c:
            pg.text(c, x + text_w(lab, FS_MIN) + 0.8, yy - 0.9, FS_MIN, COL["ink2"])
        if hi <= 0:                                   # a zero limit: a dot in the zero column
            pg.circle(lx + 3.0, yy, 0.9, fill=col)
        elif lo == hi:                                # a limit: a tick
            pg.poly([rect(pos(lo) - 0.35, yy - 1.6, pos(lo) + 0.35, yy + 1.6)], fill=col)
            pg.text(u"{:,.0f}".format(lo), pos(lo) + 1.2, yy - 0.9, FS_MIN, col, bold=True)
        else:                                         # a range: a bar
            pg.poly([rect(pos(lo), yy - 1.5, pos(hi), yy + 1.5)], fill=col)
            pg.text(u"{:,.0f}-{:,.0f}".format(lo, hi), pos(lo) + 1.0, yy - 0.9, FS_MIN, COL["white"], bold=True)
    yb = y - (len(rows) - 1) * 5.2 - 3.6
    pg.line([(lx, yb), (a1, yb)], COL["ink2"], 0.2)
    for v, s in ((0, u"0"), (1, u"1"), (100, u"100"), (10000, u"10,000"), (100000, u"100,000")):
        xx = lx + 3.0 if v == 0 else pos(v)
        pg.line([(xx, yb), (xx, top)], COL["faint"], 0.15)
        pg.text(s, xx, yb - FS_MIN * 1.25, FS_MIN, COL["ink2"], align="C")
    pg.line([(lx + 6.0, yb + 0.9), (lx + 7.0, yb - 0.9)], COL["ink2"], 0.2)   # the break between 0 and 1
    y = yb - FS_MIN * 1.25 - 5.0
    _p12_put(pg, ico_draw("uv", x + 3.5, y + 0.4, 7.0))
    pg.text(u"UV where people touch the water", x + 9.0, y + 0.8, 3.4, COL["ink_dark"], bold=True)
    pg.text(u"class A reuse (parks, water people touch) allows 0", x + 9.0, y - 2.8, FS_MIN, COL["ink"])
    return y - 5.6


def _p12_plants(pg, x, y, w):
    """G7: what the planting removes, as bars on one 0-100 % axis (D2: the reed figure only as the pilot result;
    D6: loosestrife TN > 60 %, no P)"""
    y = _p12_head(pg, x, y, w, u"WHAT THE PLANTING TAKES OUT", u"share of the nutrient removed")
    bx0, bx1 = x + 44.0, x + w - 14.0
    for ic, name, what, bars, src in HOW_T:
        _p12_put(pg, ico_draw(ic, x + 3.0, y - 1.6 - 1.4 * (len(bars) - 1), 6.0))
        pg.text(name, x + 7.5, y - 0.9, FS_MIN, COL["ink_dark"], bold=True)
        c = cite(src) if src else u""
        pg.text(what + (u" " + c if c else u""), x + 7.5, y - 0.9 - FS_MIN * 1.25, FS_MIN, COL["ink2"])
        for j, (lab, v, s) in enumerate(bars):
            yy = y - j * 4.6
            pg.poly([rect(bx0, yy - 1.3, bx1, yy + 1.3)], fill=COL["paper"])
            pg.poly([rect(bx0, yy - 1.3, bx0 + (bx1 - bx0) * v / 100.0, yy + 1.3)], fill=MP["wetland"][1])
            if s.startswith(u">"):                    # an open end: at least this much
                xe = bx0 + (bx1 - bx0) * v / 100.0
                pg.poly([[(xe, yy - 1.3), (xe + 2.2, yy), (xe, yy + 1.3)]], fill=MP["wetland"][1])
            if lab:
                pg.text(lab, bx0 + 1.0, yy - 0.9, FS_MIN, COL["white"], bold=True)
            pg.text(s, bx1 + 1.2, yy - 0.9, FS_MIN, COL["ink_dark"], bold=True)
        y -= max(len(bars) * 4.6, FS_MIN * 2.6) + 2.4
    return y


def _p12_why(pg, x, y, w):
    """why we clean here: the two published facts as pictogram rows (icon, figure, keywords)"""
    y = _p12_head(pg, x, y, w, u"WHY THE STREAM NEEDS CLEANING")
    for ic, head, big, short, src in WHY_T:
        _p12_put(pg, ico_draw(ic, x + 3.5, y - 2.2, 7.0))
        pg.text(big, x + 9.5, y - 1.0, 3.8, COL["ink_dark"], bold=True)
        tx = x + 9.5 + text_w(big, 3.8, True) + 2.0
        pg.text(head, tx, y - 1.0, FS_MIN, COL["ink2"], bold=True)
        c = cite(src)
        pg.text(short + (u" " + c if c else u""), x + 9.5, y - 1.0 - FS_MIN * 1.4, FS_MIN, COL["ink"])
        y -= 9.4
    return y


def _p12_steps(pg, x, y, w, rows, small=True):
    """R2 (31 Oct, G3): the key of the map's numbered steps, taken off the map: per step its marker and icon, the
    verb with its figure, the keywords on one line (two when one is too wide); small=False drops the keywords
    (logged by the caller) when the column is short"""
    y = _p12_head(pg, x, y, w, u"FIVE STEPS, NUMBERED ON THE MAP AND ITS ZOOM", u"figures from the water balance")
    tx = x + 13.0
    for n, ic, head, big, sm in rows:
        _p12_step(pg, n, x + 2.1, y - 1.2, 4.2)
        _p12_put(pg, ico_draw(ic, x + 8.0, y - 1.2, 5.0))
        pg.text(head, tx, y - 2.3, 3.2, P12_STEP_COL.get(n) or COL["ink_dark"], bold=True)
        if big:
            pg.text(big, tx + text_w(head, 3.2, True) + 2.0, y - 2.3, 3.2, COL["ink_dark"], bold=True)
        y -= 3.2 * 1.3 + 0.6
        if small and sm:
            one = u" · ".join(sm)
            lines = [one] if text_w(one, FS_MIN) <= x + w - tx else list(sm)
            for s_ in lines:
                pg.text(s_, tx, y - 1.4, FS_MIN, COL["ink"])
                y -= FS_MIN * 1.3
        y -= 1.6
    return y


def _p12_column(pg, cb, rows, log):
    """the column beside the map (G7): the key of the map's five steps (R2, 31 Oct: taken off the map, G3), the two
    charts, why; the conclusion at its foot. The blocks share the column's height (equal gaps), measured on a dry run
    first; when they do not fit, the steps lose their keyword lines (logged)"""
    x, y0, x1, y1 = cb
    w = x1 - x
    end = r28_para(Page(1, 1), x, 0.0, w, CONTEXT["system"], 3.2, COL["ink"], kcol=COL["ink_dark"])
    hc = -end + 1.0
    for small in (True, False):
        blocks = ((lambda pg_, x_, y_, w_: _p12_steps(pg_, x_, y_, w_, rows, small)),
                  _p12_coliforms, _p12_plants, _p12_why)
        dry = Page(1, 1)
        hs = []
        yy = y1
        for fn in blocks:
            yn = fn(dry, x, yy, w)
            hs.append(yy - yn)
            yy = yn
        if y1 - y0 - sum(hs) - hc >= 3.0 * len(blocks):
            break
        log.append(u"p.12 column: {} the column{}".format(
            u"the steps' keyword lines do not fit" if small else u"the blocks still overflow",
            u": the keywords left out" if small else u" (shorten a block)"))
    gap = max(3.0, min(14.0, (y1 - y0 - sum(hs) - hc) / float(len(blocks))))
    y = y1
    for fn in blocks:
        y = fn(pg, x, y, w) - gap
    pg.line([(x, y0 + hc + 1.5), (x + w, y0 + hc + 1.5)], COL["structure"], 0.3)
    r28_para(pg, x, y0 + hc, w, CONTEXT["system"], 3.2, COL["ink"], kcol=COL["ink_dark"])


# ---------------------------------------------------------------- the page
def p12_page(pg, box, opt, storage, log):
    """v9 (Aras 31 Oct): the whole p.12 panel in box (page mm, y up): the axonometric water map with the column beside
    it on top, the up-close section of the upstream entry in ONE band below it, in style a (b's layout, a's drawing).
    Returns [(crop id, bbox, scale den or None)]: wb_system = map + band (both booklet builds take it). v12 (round 3):
    logs the map's draw order (G8, wat_draw_order_lines) and the page's text overlap test (G3, lp_overlap_flag
    "p11": the map's names, letters and zoom texts, the band's texts; against the legend, the north arrow, the winter store's cube and the step markers)."""
    x0, y0, x1, y1 = box
    _P12_MEMO.clear()                                    # one run's ground model, drops, trees and tree styles
    zones, links = _p12_zones(log)
    f = _p12_figures(zones)
    if not WB_LIVE:                                      # v6.1
        log.append("p.12: no water_balance_results.json: HOLD volume and strip figures left out (run the water balance first)")
    D = basemap_load(log=log)
    hz, gp = P12_ZOOM_H, P12_ZOOM_GAP
    Z = _p12_zoom_geom(zones, D, (x1 - x0 - P12_ZOOM_KEY_W - 6.0 - P12_ZOOM_LEG_W) * P12_ZOOM_DEN / 1000.0, log)
    my0, my1 = (y0 + hz + gp, y1) if Z else (y0, y1)   # v9: one band, at the bottom
    xs = x1 - P12_COL_W
    ga = (x0, my0, xs - 7.0, my1)
    n0 = len(pg.items)
    M = _p12_map(pg, ga, zones, links, f, Z, D, log)
    for nx_, ny_ in ((ga[0] + 5.0, ga[1] + 4.0), (ga[2] - 6.0, ga[1] + 4.0), (ga[0] + 5.0, ga[3] - 12.0),
                     (ga[2] - 6.0, ga[3] - 12.0)):
        if not any(lp_hit((nx_ - 3.0, ny_ - 3.0, nx_ + 9.0, ny_ + 10.0), t) for t in M["taken"]):
            break                                     # the map's north arrow in a free corner
    nb_ = _p12_north(pg, nx_, ny_, M["nd"])
    M["taken"].append(nb_)
    lbl = list(M["labels"]) + _p12_map_labels(pg, ga, M, zones, f, D, log)
    _p12_column(pg, (xs, my0, x1, my1), _p12_step_rows(f, M["at"]), log)
    wat_draw_order_lines(page="p11", steps=["ground", "bed", "water", "structures", "vegetation", "labels"])
    dbx = [b_ for b_ in [M.get("legend"), nb_, M["Sc"]["cube_b"]] + list(M.get("marks") or []) if b_]
    bm = items_bbox(pg.items[n0:])
    if not Z:
        lp_overlap_flag("p11", lbl, dbx, box)
        return [("wb_system", bm, None)]
    n1 = len(pg.items)
    lbl += _p12_zoom(pg, (x0, y0, x1, y0 + hz), Z, "a", log, f)
    lp_overlap_flag("p11", lbl, dbx, box)
    cl = cut_log_line()
    if cl:
        log.append(u"p.12: " + cl)
    return [("wb_system", union(bm, items_bbox(pg.items[n1:])), None)]
