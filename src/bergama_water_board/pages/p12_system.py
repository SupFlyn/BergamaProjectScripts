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
# (masterplan parts/02b_detail.py CUT_AT = water board CUTS); K4, K5 = the bridges (site board BRIDGES_K)
P12_PLACES = [(u"UPSTREAM ENTRY", (29693.022, 32569.176)), (u"K4 · ULUCAMİ ÖNÜ", (29846.40, 32277.71)),
              (u"K5 · ÜÇ KEMER", (30293.63, 31792.25)), (u"DOWNSTREAM END", (30991.856, 31039.404))]
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
P12_K5_NAMES = 6                     # names of the base data drawn around K5 at most
P12_ZOOM_H = 48.0                    # mm: the up-close section band (v9: one band, style a, below the map)
P12_BLD_NEAR_M = 60.0                # v9 (Aras 31 Oct): buildings drawn as volumes only this close to the Selinos line
#                                      (m, drawing rule; heritage always); the rest as flat footprints
P12_BLD_FAR = ("E4E0D9", 0.55)       # the far footprints: fill, opacity (drawing values: faint, no edge)
P12_ZOOM_GAP = 5.0                   # mm between the band and the map
P12_ZOOM_KEY_W = 70.0                # mm: the band's key column (title, callouts, water, scale bar)
P12_ZOOM_DEN = 500                   # the up-close section at 1:500 (D6 standard scale)
P12_ZOOM_BAR = (0, 5, 10, 20)        # its scale bar marks, m
P12_ZOOM_CUT = "W1"                  # the registry cut whose levels it draws (the upstream entry)
P12_ZOOM_BANK_M = 12.0               # m of the far bank kept beyond the stream (drawing rule)
P12_WALL_T = 0.50                    # m: the channel wall drawn in cut (drawing rule: the data gives no thickness)
P12_KERB_H = 0.15                    # m: reed cell kerb over the ground (drawing value, as p.13 and p.22)
P12_BASIN = (5.0, 1.5, 0.90, 0.50, 0.65)   # reed cell length, gap, floor under the rim, media, water over the floor
#                                            (m; drawing values, as p.22 P24_BASIN)
P12_ZOOM_TEXT = {"WT": u"Reed basins, lined: the stream cleaned once",
                 "WD": u"Spillway: clean water back to the stream",
                 "GR": u"Shaded walk: a bench in the trees' shade",
                 "WS": u"Dry-top terraces: winter water held below",
                 "WP": u"Streamside planting, fed by the clean stream",
                 "DG": u"Demeter's garden: olives, aromatics",
                 "WA": u"Flood terraces: high water spreads here",
                 "wall": u"Stone walls of the walled town reach",
                 "strip": u"Summer strip: water in the bed all summer"}
P12_COL_W = 112.0                    # the column beside the map, mm
P12_ZONE = {"WS": MP["storage"], "WT": MP["wetland"], "WD": MP["discharge"], "GR": MP["park"],
            "WA": MP["amphibious"], "WP": ("ABBBAE", "748878", "3B4D3F"), "DG": MP["agriculture"]}
P12_STEP_COL = {1: MP["discharge"][1], 2: MP["wetland"][2], 3: MP["storage"][2], 4: MP["discharge"][2],
                5: MP["agriculture"][2]}


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


# ---------------------------------------------------------------- labels on the map (G4: never on each other)
def _p12_wh(spec):
    ic = 7.0 if spec.get("icon") else 0.0
    ws = [text_w(spec["head"], 3.2, True)]
    if spec.get("big"):
        ws.append(text_w(spec["big"], 3.8, True))
    ws += [text_w(s, FS_MIN) for s in spec.get("small", ())]
    h = 3.2 * 1.3 + (3.8 * 1.25 if spec.get("big") else 0.0) + len(spec.get("small", ())) * FS_MIN * 1.3 + 0.4
    return ic + max(ws) + 0.8, max(h, ic)


def _p12_label(pg, b, spec):
    """a map label in its box b: the icon on the left, the step and verb, the figure, the keywords"""
    x = b[0]
    if spec.get("icon"):
        _p12_put(pg, ico_draw(spec["icon"], b[0] + 3.0, b[3] - 3.2, 6.0))
        x += 7.0
    col = spec.get("col") or COL["ink_dark"]
    y = b[3] - 3.2 * CAP - 0.4
    pg.text(spec["head"], x, y, 3.2, col, bold=True)
    if spec.get("big"):
        y -= 3.8 * 1.22
        pg.text(spec["big"], x, y, 3.8, COL["ink_dark"], bold=True)
    for s in spec.get("small", ()):
        y -= FS_MIN * 1.3
        pg.text(s, x, y, FS_MIN, COL["ink"])


def _p12_place(pg, specs, taken, bounds, segs, log):
    """places and draws the labels of specs (anchor x, y) beside their points, on a thin leader when off it"""
    rings = (1.5, 4.0, 7.0, 11.0, 16.0, 22.0, 30.0, 40.0, 52.0, 66.0)
    for sp in specs:
        w, h = _p12_wh(sp)
        got = label_spot(sp["x"], sp["y"], w, h, taken, bounds, segs, 0.8, rings, 24) or \
            label_spot(sp["x"], sp["y"], w, h, taken, bounds, (), 0.8, rings, 24)
        if not got:
            log.append(u"p.12: no room on the map for the label '{}'".format(sp["head"]))
            continue
        b = got[0]
        taken.append(b)
        e = lp_leader_end(b, (sp["x"], sp["y"]))
        d = math.hypot(e[0] - sp["x"], e[1] - sp["y"])
        if d > 1.2:
            r0 = sp.get("r0", 0.0)
            s0 = (sp["x"] + (e[0] - sp["x"]) * r0 / d, sp["y"] + (e[1] - sp["y"]) * r0 / d)
            pg.line([s0, e], COL["ink2"], 0.18)
            if not r0:
                pg.circle(sp["x"], sp["y"], 0.45, fill=COL["ink2"])
        _p12_label(pg, b, sp)


# ---------------------------------------------------------------- the axonometric map (v6: a true 3D object)
def _p12_axo(pts, area, margins):
    """T(p, z=0) survey m -> page mm for the map, its inverse at z = 0, k (page mm per m) and view (the horizontal
    unit vector from the scene towards the viewer, survey axes): the plan turned by the one of P12_ROTS that gives
    the largest scale (ties: nearest the old -12 deg), seen from above at the angle of P12_SIN / P12_COS (depth x
    sin, heights x cos; one scale), fitted into area less the margins (left, right, bottom, top)"""
    cx, cy = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
    ml, mr, mb, mt = margins
    W, H = area[2] - area[0] - ml - mr, area[3] - area[1] - mb - mt
    best = None
    for deg in sorted(P12_ROTS, key=lambda d_: abs(d_ + 12.0)):
        rho = math.radians(deg)
        c, s = math.cos(rho), math.sin(rho)
        U = [((p[0] - cx) * c - (p[1] - cy) * s, ((p[0] - cx) * s + (p[1] - cy) * c) * P12_SIN) for p in pts]
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


def _p12_base(pg, items, T, K, hook=None):
    """the shared basemap items (or M11 axo items with T = identity) through T, clipped to K; hook(rings, hex) ->
    True takes a fill over (the tree cover is drawn as a canopy texture)"""
    def fill(rings, col, alpha, nonzero):
        rr = [r for r in (_p12_cring(R, K) for R in rings) if r]
        if rr and not (hook and hook(rr, col)):
            pg.poly(rr, fill=col, alpha=alpha if alpha is not None and alpha < 0.999 else None)

    def line(pts, col, w, dash, alpha):
        for piece in _p12_cline(pts, K):
            pg.line(piece, col, w, dash)
    return basemap_draw(items, T, fill, line)


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


def _p12_channel(pg, L, T, K, k, view, sb, zones, log):
    """G8 on the map: the Selinos as water lying in its channel. The surveyed water (the bank line at average flow)
    is sunk by the registry drop (_p12_drop_fn) and textured (M5 water_plan); the bank faces that look toward the
    viewer are drawn from the ground down to the water (stone in the walled town reach, earth elsewhere); the summer
    strip (zone base: the LOW-FLOW WATER STRIP) lies on the water as the low-flow channel, without an outline (the
    old squiggle); then the ground is laid over everything as a white sheet with the stream cut out (even-odd), so
    the near bank hides what lies under it. Returns what it drew (for the legend)."""
    out = dict(strip=False, wall=False, bank=False, water=False)
    groups = [g for g in (L.get("water") or []) if g and len(g[0]) >= 3 and _p12_hit(g[0], sb)]
    if not groups:
        return out
    pal = _wat_pal()
    dz = _p12_drop_fn(_p12_drops(log))
    faces, tops = [], []
    for gi, g in enumerate(groups):
        low = None
        for ri, R in enumerate(g):
            if len(R) < 3:
                continue
            zs = [dz(p) for p in R]
            if ri == 0:
                low = [T(p, -z[0]) for p, z in zip(R, zs)]
            tops.append([T(p) for p in R])
            ar = sum(R[i][0] * R[(i + 1) % len(R)][1] - R[(i + 1) % len(R)][0] * R[i][1] for i in range(len(R))) > 0
            left = ar == (ri == 0)                       # the water lies left of each edge
            n = len(R)
            for i in range(n):
                p, q = R[i], R[(i + 1) % n]
                ex, ey = q[0] - p[0], q[1] - p[1]
                Le = math.hypot(ex, ey)
                if Le < 1e-6:
                    continue
                nx, ny = (-ey / Le, ex / Le) if left else (ey / Le, -ex / Le)
                if nx * view[0] + ny * view[1] <= 0.02:  # faces away from the viewer: hidden by the near bank
                    continue
                zp, zq = zs[i][0], zs[(i + 1) % n][0]
                if zp < 0.05 and zq < 0.05:
                    continue
                faces.append(((p[0] + q[0]) / 2.0 * view[0] + (p[1] + q[1]) / 2.0 * view[1],
                              [T(p), T(q), T(q, -zq), T(p, -zp)], zs[i][1] or zs[(i + 1) % n][1]))
        surf = _p12_cring(low, K) if low else []
        if surf:
            out["water"] = True
            try:
                _p12_shapes(pg, water_plan(surf, k, bank=False, seed=gi + 1).shapes())
            except Exception as ex:
                log.append(u"p.12: water_plan failed ({}): the stream drawn in its plain tone".format(ex))
                pg.poly([surf], fill=pal["surface"])
    for z in zones:                                     # the low-flow channel on the water
        if z["code"] == "STRIP":
            rr = _p12_cring([T(p, -dz(p)[0]) for p in z["ring"]], K)
            if rr:
                pg.poly([rr], fill=pal["low"], alpha=0.85)
                out["strip"] = True
    faces.sort(key=lambda f_: f_[0])                    # far first
    for _, ring, walled in faces:
        rr = _p12_cring(ring, K)
        if rr:
            pg.poly([rr], fill=SCT["stone"] if walled else SCT["earth"])
            out["wall" if walled else "bank"] = True
    holes = [r for r in (_p12_cring(R, K) for R in tops) if r]
    pg.poly([list(K["C"])] + holes, fill=COL["white"])  # the ground: even-odd, the stream left open
    for r in holes:
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
    """the tree cover (survey / WorldCover, page rings at z = 0) as a canopy texture: the cover's pale ground, then
    leaf clusters on a jittered P12_CANOPY_M lattice, their shadows first, pushed to the lower right (light from the
    upper left, as the buildings and trees); returns the number of clusters"""
    st = TREE_STYLES["context"]
    s = max(0.9, P12_CANOPY_M * k)
    pts = []
    for R in rings:
        if len(R) < 3:
            continue
        pg.poly([R], fill=st["light"], alpha=0.6)
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
        pg.poly([[(q[0] + 0.35 * r, q[1] - 0.22 * r) for q in _p12_circle_pts(px, py, r, 10)]], fill=st["shadow"],
                alpha=st["shadow_a"])
    for px, py, r, c in pts:
        pg.poly([_tree_blob(px, py, r, _tree_rand(px, py), 9)], fill=(st["mid"], st["dark"], st["light"])[c], alpha=0.85)
    return len(pts)


def _p12_zone_trees(zones, log):
    """the planted trees of the project's zones (survey m): a mixed, ecologically zoned scatter (plants.py, G9:
    never rows), wet to dry away from the Selinos line, in the streamside planting, the walks and dry tops and
    Demeter's garden; [(key, x, y, crown m, height m)], heights the species' sourced drawing heights"""
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
    return out


def _p12_legend(pg, ga, rows, avoid, taken):
    """the map's legend (M2 Legend, G1: every symbol it draws), in the inside corner of the map holding the fewest
    drawn key points, on a paper plate; rows = [(label, kind fill / line / dash / tree, sample)]; returns its box"""
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
    pg.poly([rect(b[0], b[1], b[2], b[3])], fill=COL["white"], stroke=COL["faint"], lw=0.15, alpha=0.92)
    for r in Lo["rows"]:
        x0, y0, x1, y1 = r["swatch"]
        ym = (y0 + y1) / 2.0
        if r["kind"] == "fill":
            pg.poly([rect(x0, y0, x1, y1)], fill=r["colour"], stroke=r.get("edge"), lw=0.12)
        elif r["kind"] in ("line", "dash"):
            pg.line([(x0, ym), (x1, ym)], r["colour"], r.get("width", 0.3), r.get("dash"))
        elif r["kind"] == "tree":
            st = TREE_STYLES[r.get("style", "tree")]
            for i, (dx, rr, c) in enumerate(((0.3, 0.42, "dark"), (0.62, 0.38, "mid"), (0.45, 0.3, "light"))):
                cx = x0 + (x1 - x0) * dx
                R = (y1 - y0) * rr
                pg.poly([_tree_blob(cx, ym + (0.15 if i == 2 else 0.0) * (y1 - y0), R, _tree_rand(cx, ym), 9)],
                        fill=st[c], alpha=0.9)
        pg.text(r["label"], r["text"][0], r["text"][1], r["size_pt"] * GRID_PT_, COL["ink"])
    return b


def _p12_k5_check(L, D, log):
    """the base-data check of the brief (Üç Kemer, K5: "is it really that empty?"): what the shared basemap holds
    within P12_K5_CHECK_M of the bridge, written to the log (the map draws all of it: buildings, streets, parks,
    tree cover, names)"""
    k5 = dict(P12_PLACES).get(u"K5 · ÜÇ KEMER")
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
    log.append(u"p.12 base data around K5 Üç Kemer ({:.0f} m): {} buildings ({} heritage, {} with a survey height), "
               u"{} parks / green areas, {} tree-cover patches, {} field patches; names: {}".format(
                   R, len(bl), sum(1 for b in bl if b.get("her")), sum(1 for b in bl if b.get("h")), len(gr), len(tc),
                   len(fl), u", ".join(nm) or u"none"))


def _p12_map(pg, ga, zones, links, f, Z, D, log):
    """the axonometric water map in the area ga (page mm): the ground as a 3D object (G7, G8, R09, R10): the stream
    sunk in its channel with its walls, streets, fields, parks and the tree cover as a canopy texture, the project's
    zones on the ground, the buildings as light volumes at their survey heights with hipped roofs (M11), the zones'
    trees in 3D at their species heights (G6, G9), the store, the links, the steps, the up-close section's line and
    the legend. Returns what the labels need."""
    key = list(P12_SELINOS) + [p for _, p in P12_PLACES]
    for z in zones:
        key += z["ring"]
    T, Ti, k, view = _p12_axo(key, ga, (12.0, 16.0, 16.0, 12.0))
    log.append(u"p.12: the water map, an axonometric at about 1:{:,.0f} (a diagram: no scale bar)".format(1000.0 / k))
    K = _p12_clipper([(ga[0], ga[1]), (ga[2], ga[1]), (ga[2], ga[3]), (ga[0], ga[3])], ga)
    P3 = lambda x, y, z: T((x, y), z)
    pal = _wat_pal()
    lg = []                                              # legend rows, in the order drawn
    L = (D or {}).get("layers") if D else None
    ch, top, fills, ncan, her = {}, {}, set(), 0, False
    if L:
        cs = [Ti(ga[0], ga[1]), Ti(ga[2], ga[1]), Ti(ga[2], ga[3]), Ti(ga[0], ga[3])]
        b0 = _p12_bbox(cs)
        sb = (b0[0] - 40.0, b0[1] - 40.0, b0[2] + 40.0, b0[3] + 40.0)
        ch = _p12_channel(pg, L, T, K, k, view, sb, zones, log)
        items = basemap_items("simple", {"stream": False, "buildings": False, "streets": True, "green": True,
                                         "trees": True, "fields": True}, box=sb, D=D, split_buildings=True)
        canopy = []

        def hook(rr, col):
            if col == BM_COL["tree"]:
                canopy.extend(rr)
                return True
            return False
        _p12_base(pg, items, T, K, hook)
        fills = set(it[2] for it in items if it[0] == "fill")
        ncan = _p12_canopy(pg, canopy, k, log)
        top = _p12_stream_top(pg, L, T, K, sb)
        _p12_k5_check(L, D, log)
    # the zones of the project, flat on the ground (the summer strip lies on the water, drawn with the stream)
    for z in zones:
        if z["code"] == "STRIP":
            continue
        tones = P12_ZONE.get(z["code"], (COL["faint"], COL["structure"]))
        rr = _p12_cring([T(p) for p in z["ring"]], K)
        if rr:
            pg.poly([rr], fill=tones[0], stroke=tones[1], lw=0.15, alpha=0.9)
    # the buildings (v9, Aras 31 Oct: the city was too crowded to read): volumes at their survey heights (M11) only
    # within P12_BLD_NEAR_M of the Selinos line and for heritage (in its rose); the rest as faint flat footprints
    nfar = 0
    if L:
        units = [b for b in L.get("buildings") or [] if b.get("rings") and _p12_hit(b["rings"][0], sb)]
        her = any(b.get("her") for b in units)
        near, far = [], []
        for b in units:
            (near if b.get("her") or _p12_near(b["rings"][0], P12_SELINOS, P12_BLD_NEAR_M) else far).append(b)
        for b in far:
            for R_ in b["rings"][:1]:
                rr = _p12_cring([T(p) for p in R_], K)
                if rr:
                    pg.poly([rr], fill=P12_BLD_FAR[0], alpha=P12_BLD_FAR[1])
                    nfar += 1
        log.append(u"p.12 map: {} buildings as volumes (within {:.0f} m of the stream, heritage), {} as flat "
                   u"footprints".format(len(near), P12_BLD_NEAR_M, len(far)))
        units = near
        its = bld_axo_items([b for b in units if not b.get("her")], P3, view=view, box=sb)
        if her:
            its += bld_axo_items([b for b in units if b.get("her")], P3, view=view, box=sb, cols=P12_HER_COLS)
        _p12_base(pg, its, lambda p: p, K)
    # the zones' trees in 3D (shadows first, then far to near)
    trees = sorted(_p12_zone_trees(zones, log), key=lambda t_: t_[1] * view[0] + t_[2] * view[1])
    trees = [t_ for t_ in trees if ga[0] + 1.0 < T((t_[1], t_[2]))[0] < ga[2] - 1.0 and
             ga[1] + 1.0 < T((t_[1], t_[2]))[1] < ga[3] - 3.0]
    for key_, x, y, cm, h in trees:
        tree_shadow(pg, P3, k, x, y, cm / 2.0, TREE_STYLES[P12_TREE_STY.get(key_, "tree")])
    for key_, x, y, cm, h in trees:
        draw_tree(pg, P3, k, x, y, cm / 2.0, h, TREE_STYLES[P12_TREE_STY.get(key_, "tree")], shadow=False)
    # the flow: in at the top (hand arrow on the first 16 mm), out to the farms beyond the last point
    S = [T(p) for p in P12_SELINOS]
    Ls = _p12_len(S)
    segs = [(S[i], S[i + 1]) for i in range(len(S) - 1)]
    taken = []
    hand_arrow(pg, [_p12_along(S, t)[0] for t in (0.0, 4.0, 8.0, 12.0, 16.0)], "water", 0.8)
    (ex, ey), (ux, uy) = S[-1], _p12_along(S, Ls)[1]
    room = min([(ga[2] - 3.0 - ex) / ux if ux > 1e-6 else 99.0, (ey - ga[1] - 3.0) / -uy if uy < -1e-6 else 99.0,
                (ga[3] - 3.0 - ey) / uy if uy > 1e-6 else 99.0, (ex - ga[0] - 3.0) / -ux if ux < -1e-6 else 99.0])
    Lf = max(6.0, min(16.0, room - 5.0))              # room left for the step marker beyond the tip
    farm_tip = (ex + ux * Lf, ey + uy * Lf)
    hand_arrow(pg, [(ex - ux * 2.0, ey - uy * 2.0), farm_tip], "water", 0.8, (MP["agriculture"][1], MP["agriculture"][2]))
    segs.append(((ex, ey), farm_tip))
    # HOLD: the design store as a cube at the map's own scale, below the upstream entry's terraces and basins (dashed:
    # in the ground), an arrow down into it
    up = _p12_pick(zones, "WS", "aras") + _p12_pick(zones, "WT", "aras")
    hold = (sum(_p12_cen(z["ring"])[0] for z in up) / len(up), sum(_p12_cen(z["ring"])[1] for z in up) / len(up)) \
        if up else P12_PLACES[0][1]
    e = max(f["store"]) ** (1.0 / 3.0) if f["store"] else 0.0
    cube_b = None
    if e > 0.0:
        P = lambda i, j, l: T((hold[0] + (i - 0.5) * e, hold[1] + (j - 0.5) * e), -l * e)
        hull = _p12_hull([P(i, j, l) for i in (0, 1) for j in (0, 1) for l in (0, 1)])
        pg.poly([hull], fill=MP["storage"][0], alpha=0.55)
        for a_, b_ in (((0, 0, 0), (1, 0, 0)), ((1, 0, 0), (1, 1, 0)), ((1, 1, 0), (0, 1, 0)), ((0, 1, 0), (0, 0, 0)),
                       ((0, 0, 1), (1, 0, 1)), ((1, 0, 1), (1, 1, 1)), ((1, 1, 1), (0, 1, 1)), ((0, 1, 1), (0, 0, 1)),
                       ((0, 0, 0), (0, 0, 1)), ((1, 0, 0), (1, 0, 1)), ((1, 1, 0), (1, 1, 1)), ((0, 1, 0), (0, 1, 1))):
            pg.line([P(*a_), P(*b_)], MP["storage"][2], 0.22, [0.9, 0.6])
        cube_b = _p12_bbox(hull)
        arrow(pg, [T(hold), T(hold, -0.55 * e)], MP["storage"][2], 0.4, 1.5)
    # the links of the project (zone base INT_LINK_*): flood onto the terraces (dashed), clean water to the planting,
    # people down to the bed
    lk = set()
    for ln in links:
        a, b = T(ln["P"][0]), T(ln["P"][-1])
        if ln.get("kind") == "flood":
            r = _p12_arrow(pg, a, b, MP["amphibious"][2], 0.4, 6.0, [1.0, 0.6])
        elif ln.get("kind") == "people":
            r = _p12_arrow(pg, a, b, COL["accent"], 0.3, 4.5, [0.6, 0.5], 1.4)
        elif u"PLANTING" in (ln.get("label") or u""):
            r = _p12_arrow(pg, a, b, P12_ZONE["WP"][2], 0.4, 6.0)
            if r:
                lk.add("planting")
        else:
            r = None
        if r:
            segs.append(r)
            if ln.get("kind") in ("flood", "people"):
                lk.add(ln["kind"])
    # the up-close section's line (the band beside the map draws it)
    if Z:
        za, zb_ = T(Z["A"]), T(Z["B"])
        for piece in _p12_cline([za, zb_], K):
            pg.line(piece, COL["accent"], 0.35, [1.6, 0.6, 0.3, 0.6])
        for p_ in (za, zb_):
            if K["bb"][0] <= p_[0] <= K["bb"][2] and K["bb"][1] <= p_[1] <= K["bb"][3]:
                pg.circle(p_[0], p_[1], 0.6, fill=COL["accent"])
        segs.append((za, zb_))
    # the steps: a numbered marker where each happens
    wt, ws, wd = _p12_pick(zones, "WT", "aras"), _p12_pick(zones, "WS", "aras"), _p12_pick(zones, "WD", "aras")
    at = {1: T(_p12_cen(ws[0]["ring"])) if ws else T(P12_PLACES[0][1]),
          2: T(_p12_cen(wt[0]["ring"])) if wt else None,
          3: ((cube_b[0] + cube_b[2]) / 2.0, cube_b[1]) if cube_b else None,
          4: T(_p12_cen(wd[0]["ring"])) if wd else None,
          5: (farm_tip[0] + ux * 3.2, farm_tip[1] + uy * 3.2)}
    for n in (1, 2, 4, 5):
        if at[n]:
            taken.append(_p12_step(pg, n, at[n][0], at[n][1], 3.6))
    if cube_b:
        taken.append(cube_b)
    # the legend (G1): every symbol of the drawing, nothing else
    if ch.get("water"):
        lg.append((u"Selinos stream, water at average yearly flow", "fill", dict(colour=pal["surface"], edge=pal["edge"])))
    if ch.get("strip"):
        lg.append((u"Summer strip: the low-flow channel, 400 cm", "fill", dict(colour=pal["low"])))
    if ch.get("wall"):
        lg.append((u"Stone channel wall, walled town reach", "fill", dict(colour=SCT["stone"])))
    if ch.get("bank"):
        lg.append((u"Earth bank", "fill", dict(colour=SCT["earth"])))
    if L and units:
        lg.append((u"Building at its survey height", "fill", dict(colour=BLD_COL["wall_lit"], edge=BLD_COL["axo_line"])))
    if nfar:
        lg.append((u"Building further from the stream, footprint", "fill", dict(colour=P12_BLD_FAR[0])))
    if her:
        lg.append((u"Heritage building", "fill", dict(colour=P12_HER_COLS["wall_lit"], edge=P12_HER_COLS["axo_line"])))
    if BM_COL["road"] in fills:
        lg.append((u"Street", "fill", dict(colour=BM_COL["road"], edge=BM_COL["road_edge"])))
    if BM_COL["park"] in fills:
        lg.append((u"Park, grass", "fill", dict(colour=BM_COL["park"])))
    if BM_COL["field"] in fills:
        lg.append((u"Field, orchard", "fill", dict(colour=BM_COL["field"])))
    if ncan:
        lg.append((u"Tree cover", "tree", dict(style="context")))
    if trees:
        lg.append((u"Planted tree, true height", "tree", dict(style="tree")))
    if top.get("bridge"):
        lg.append((u"Bridge", "line", dict(colour=BM_COL["ink"], width=0.3)))
    if top.get("covered"):
        lg.append((u"Covered stream", "dash", dict(colour=BM_COL["water_edge"], width=0.3, dash=list(BM_COVERED_DASH))))
    if cube_b:
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
        lg.append((u"Section up close (band)", "dash", dict(colour=COL["accent"], width=0.35, dash=[1.6, 0.6, 0.3, 0.6])))
    if lg:
        avoid = [p for p in S] + [T(p) for z in zones for p in z["ring"][::4]]
        taken.append(_p12_legend(pg, ga, lg, avoid, taken))
    nd = (T((hold[0], hold[1] + 100.0))[0] - T(hold)[0], T((hold[0], hold[1] + 100.0))[1] - T(hold)[1])
    nl = math.hypot(*nd)
    return dict(T=T, k=k, S=S, segs=segs, taken=taken, at=at, hold=hold, e=e, nd=(nd[0] / nl, nd[1] / nl))


def _p12_map_labels(pg, ga, M, zones, f, D, log):
    """the verbs with their figures (R03, R04), the programme icons along the strip (R05), the places and the base
    data's own names around Üç Kemer (K5: what is there, the brief's base-data check)"""
    T, at, taken, segs = M["T"], M["at"], M["taken"], M["segs"]
    specs = []
    take, site = f["collect"]
    if at[1]:
        sm = []
        if take is not None:
            sm.append(u"{:,.0f} m³ from the winter stream".format(take))
        if site is not None:
            sm.append(u"{:,.0f} m³ street + roof runoff".format(site))
        specs.append(dict(x=at[1][0], y=at[1][1], r0=1.8, icon="rain", head=u"1 COLLECT", col=P12_STEP_COL[1],
                          big=u"{:,.0f} m³ a year".format((take or 0) + (site or 0)) if sm else None, small=sm))
    if at[2]:
        specs.append(dict(x=at[2][0], y=at[2][1], r0=1.8, icon="reeds", head=u"2 CLEAN", col=P12_STEP_COL[2],
                          big=u"{:,.0f} m² of reed basins".format(f["reed_m2"]) if f["reed_m2"] else None,
                          small=[u"lined, root-contained · cleaned once,", u"then the whole reach runs clean"]))
    if at[3]:
        specs.append(dict(x=at[3][0], y=at[3][1], icon="storage", head=u"3 HOLD", col=P12_STEP_COL[3],
                          big=u"{:,.0f}-{:,.0f} m³".format(*f["store"]) if f["store"] else None,
                          small=[u"winter water held in the ground,", u"at most a year · cube at the map's scale"]))
    if at[4]:
        sm = [u"spillway: overflow back to the stream"]
        if f["left"]:
            sm.append(u"of its winter flow · driest year {:.0f} %".format(math.floor(f["left"][0])))
        specs.append(dict(x=at[4][0], y=at[4][1], r0=1.8, icon="stream", head=u"4 GIVE BACK", col=P12_STEP_COL[4],
                          big=u"{:.0f} % stays in the stream".format(math.floor(f["left"][1])) if f["left"] else None,
                          small=sm[::-1] if f["left"] else sm))
    sm = [u"the clean stream leaves the site"]
    if f["farm_ha"]:
        sm.append(u"for {:.1f} ha of farms outside it".format(f["farm_ha"]))
    specs.append(dict(x=at[5][0], y=at[5][1], r0=1.8, icon="stream_out", head=u"5 TO THE FARMS", col=P12_STEP_COL[5],
                      big=u"{:,.0f} m³ a year".format(f["farms"]) if f["farms"] else None, small=sm))
    # the summer strip, on its longest piece between K4 and K5
    st = sorted(_p12_pick(zones, "STRIP", "begum"), key=lambda z: -_p12_area(z["ring"]))
    if st and f["strip"]:
        c0 = _p12_cen(st[0]["ring"])
        p0 = min(st[0]["ring"], key=lambda p: (p[0] - c0[0]) ** 2 + (p[1] - c0[1]) ** 2)
        q = T(p0)
        specs.append(dict(x=q[0], y=q[1], icon="water", head=u"SUMMER STRIP", col=MP["discharge"][2],
                          big=u"400 × {:.0f} cm · {:,.0f} m".format(STRIP_DEPTH * 100.0, f["strip"][0]),
                          small=[u"first fill {:,.0f} m³ · {:,.0f} m³ a summer".format(f["strip"][1], f["strip"][2]),
                                 u"clean water in the bed all summer"]))
    fl = _p12_pick(zones, "WA", "begum_alan[1]", u"FLOOD") or _p12_pick(zones, "WA", "begum", u"FLOOD")
    if fl:
        q = T(_p12_cen(fl[0]["ring"]))
        specs.append(dict(x=q[0], y=q[1], icon="high_water", head=u"HIGH WATER", col=MP["amphibious"][2],
                          small=[u"spreads onto the flood terraces"]))
    # the programme along the strip (R05): what people do where, from the zones
    for code, area, lab, ic, words in (("GR", "begum_alan[0]", None, "people", [u"raised dry top · steps to the bed"]),
                                       ("GR", "begum_alan[1]", None, "people", [u"raised dry top · steps to the bed"]),
                                       ("DG", None, None, "olive", [u"olives, aromatics, beds"]),
                                       ("WP", None, None, "plants", [u"fed by the clean stream"]),
                                       ("GR", "aras", None, "shade", [u"along the basins"])):
        zz = _p12_pick(zones, code, area, lab)
        if not zz:
            continue
        cs = [_p12_cen(z["ring"]) for z in zz]
        q = T((sum(c[0] for c in cs) / len(cs), sum(c[1] for c in cs) / len(cs)))
        head = {"DG": u"DEMETER'S GARDEN", "WP": u"STREAMSIDE PLANTING"}.get(code, u"DRY TOP" if ic == "people"
                                                                            else u"SHADED WALK")
        specs.append(dict(x=q[0], y=q[1], icon=ic, head=head, col=COL["ink_dark"], small=words))
    _p12_place(pg, specs, taken, ga, segs, log)
    # the places, in small capitals, last (they may sit farther off)
    pl = [dict(x=T(p)[0], y=T(p)[1], head=nm, col=COL["ink2"]) for nm, p in P12_PLACES]
    _p12_place(pg, pl, taken, ga, segs, log)
    k5 = dict(P12_PLACES).get(u"K5 · ÜÇ KEMER")
    if k5 and D:
        R = P12_K5_CHECK_M
        nm = sorted(basemap_names((k5[0] - R, k5[1] - R, k5[0] + R, k5[1] + R), D),
                    key=lambda q: math.hypot(q[1][0] - k5[0], q[1][1] - k5[1]))[:P12_K5_NAMES]
        sp = [dict(x=T(p)[0], y=T(p)[1], head=u"", small=[n], col=COL["ink2"]) for n, p in nm
              if ga[0] < T(p)[0] < ga[2] and ga[1] < T(p)[1] < ga[3]]
        _p12_place(pg, sp, taken, ga, segs, log)


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
    return dict(o=o, e=e, u0=u0, u1=u1, wet=(wl, wr), els=els, strip=strip, bed=reg["bed"],
                top=sum(tops) / len(tops), walled=bool(reg["walled"]), trimmed=trimmed,
                A=(o[0] + e[0] * u0, o[1] + e[1] * u0), B=(o[0] + e[0] * u1, o[1] + e[1] * u1),
                units=list(L.get("buildings") or []))


def _p12_zoom(pg, band, Z, style, log):
    """the up-close section in the band (page mm, y up) at 1:P12_ZOOM_DEN, in style "a" (cutout people and trees over
    the same drawn ground, D1 a) or "b" (vector, D1 b), from ONE geometry Z: the cut ground (survey buildings in cut,
    M11), the stone walls and the bed with the water at average yearly flow, the summer strip, Q100 / Q500 (M5, G8,
    the registry levels of P12_ZOOM_CUT), and each zone as the place it is (G10): the lined reed basins with people
    watching, the stone spillway, the shaded walk with its trees, a bench and walkers, the dry-top terraces with low
    planting and children playing; numbered callouts with their reason, the key, the water legend and the scale bar
    on the left (G1). Everything at true size (G6, logged)."""
    x0, y0, x1, y1 = band
    den = P12_ZOOM_DEN
    k = sf_k(den)
    sx = x0 + P12_ZOOM_KEY_W + 6.0
    u0, u1 = Z["u0"], Z["u1"]
    X = lambda u: sx + (u - u0) * k
    yb = y0 + 1.0
    y_of = sf_y_of(Z["bed"] - STRIP_DEPTH - 1.0, yb, k)
    gy, bed_y = y_of(Z["top"]), y_of(Z["bed"])
    sky = (y1 - 1.0 - gy) / k                           # m of room over the ground
    allow = [q for q in PLA_NICHE if PLA_SPECIES[q]["h_m"] * 1.08 <= sky - 0.3]
    back = [q for q in PLA_NICHE if PLA_SPECIES[q]["layer"] == "tree" and PLA_SPECIES[q]["h_m"] * 1.08 * 0.8 <= sky - 0.3]
    W = water_layers()
    co = SfCallouts()
    wl, wr = Z["wet"]
    t = P12_WALL_T * k
    xa_s, xb_s = X(u0), X(u1)
    sf_atmosphere(xa_s, xb_s, gy, y1 - 0.5, k, seed=5, trees=bool(back), birds=False, mix=back or None,
                  density=0.5, style=style, into=W)
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
        co.add(X(wr) + t / 2.0, bed_y - 2.2, P12_ZOOM_TEXT["wall"])          # in the cut, under the water lines
    for sa, sb_ in Z["strip"][:1]:
        co.add(X((sa + sb_) / 2.0), bed_y + 3.4, P12_ZOOM_TEXT["strip"])      # between average flow and Q100
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
    # the zones as places (G10)
    trees = []
    near = X(wr) + t                                    # the stream's NE wall face: where "toward the stream" points
    for i, (code, ua, ub) in enumerate(Z["els"]):
        xa, xb = X(ua), X(ub)
        xm = (xa + xb) / 2.0
        sgn = -1.0 if xm > near else 1.0
        if code == "WT":                                # lined reed cells, as p.22 (P12_BASIN drawing values)
            ln, gap, fl, media, wat = P12_BASIN
            u = ua + 0.3
            while u + 2.0 <= ub - 0.3:
                ue = min(u + ln, ub - 0.3)
                W.add("structures", [("poly", [(X(u), gy - (fl - wat) * k), (X(ue), gy - (fl - wat) * k), (X(ue), gy),
                                               (X(u), gy)], COL["white"], None, 0.1)])      # the open cell over the water
                W.add("structures", pla_reed_basin(X(u), X(ue), gy - fl * k, gy, k, P12_KERB_H, media_m=media,
                                                   wl_y=gy - (fl - wat) * k))
                u = ue + gap
            for j, xx in enumerate((xa - 0.9 * k, xb + 0.9 * k)):
                if (xx > near + 0.5 * k) and (xx < xb_s - 0.5 * k):
                    W.add("figures", fig_side("watch", xx, gy, k, facing=1 if j == 0 else -1, style=style))
        elif code == "WD":                              # the stone spillway, back to the stream
            W.add("structures", sct_hatch_fill([(xa, gy - 0.4 * k), (xb, gy - 0.4 * k), (xb, gy), (xa, gy)], "stone",
                                               k, SCT["cut"], 0.2))
            W.add("water", [("line", [(xa, gy - 0.06 * k), (xb, gy - 0.06 * k)], _wat_pal()["deep"], 0.35)])
            ax0, ax1 = xm - sgn * 3.0, xm + sgn * 3.0
            W.add("labels", [("line", [(ax0, gy + 1.4), (ax1, gy + 1.4)], COL["river_mid"], 0.3),
                             ("poly", [(ax1 + sgn * 1.2, gy + 1.4), (ax1, gy + 2.0), (ax1, gy + 0.8)], COL["river_mid"],
                              None, 0.1)])
        elif code == "GR":                              # the shaded walk: gravel, trees, a bench in the shade, walkers
            W.add("ground", sf_lane(xa, gy, ub - ua, k, kind="gravel"))
            if allow:
                sh, pl = pla_scatter_section(xa, xb, gy, k, t0=0.45, t1=0.7, mix=allow, seed=11 + i, style=style,
                                             density=0.9)
                W.add("vegetation", sh)
                trees += pl
            if xb - xa > 14.0:
                xbch = xa + 0.35 * (xb - xa)
                an = fig_meta("sit_step", facing=1, seat_h=SF_SEAT_H)
                W.add("structures", sf_bench(xbch, gy, k))
                W.add("figures", fig_side("sit_step", xbch + 0.225 * k - an.get("seat_x", 0.0) * k, gy, k, facing=1,
                                          seat_h=SF_SEAT_H, style=style))
                for a_, b_, sd in ((xa + 1.0, xbch - 2.0, 3 + i), (xbch + 3.0, xb - 1.0, 4 + i)):
                    if b_ - a_ > 4.0:
                        W.add("figures", fig_activity("walkway", a_, b_, gy, k, seed=sd, density=0.8, style=style)[0])
            else:
                W.add("figures", fig_activity("walkway", xa + 0.5, xb - 0.5, gy, k, seed=3 + i, density=0.8,
                                              style=style)[0])
        elif code == "WS":                              # the dry-top terraces: low planting, people, children playing
            W.add("ground", [("line", [(xa, gy + 0.05), (xb, gy + 0.05)], MP["park"][1], 0.45)])
            low = [q for q in allow if PLA_NICHE[q][0] >= 0.5]
            if low:
                sh, pl = pla_scatter_section(xa, xb, gy, k, t0=0.8, t1=1.0, mix=low, seed=21 + i, style=style,
                                             density=0.6)
                W.add("vegetation", sh)
                trees += pl
            for j, (fr, pose) in enumerate(((0.18, "stand"), (0.36, "child_play"), (0.62, "walk"), (0.82, "watch"))):
                W.add("figures", fig_side(pose, xa + fr * (xb - xa), gy, k, facing=1 if j % 2 else -1, style=style))
        elif code in ("WP", "DG"):                      # planting: wet band by the stream, Demeter's garden dry
            mix = [q for q in allow if (q in ("olive", "rosemary", "lavender")) == (code == "DG")]
            if mix:
                sh, pl = pla_scatter_section(xa, xb, gy, k, t0=0.05 if code == "WP" else 0.8,
                                             t1=0.4 if code == "WP" else 1.0, mix=mix, seed=31 + i, style=style)
                W.add("vegetation", sh)
                trees += pl
        if code in P12_ZOOM_TEXT and xb - xa > 3.0:
            if code == "WT":                            # the mark in the cut ground, under the element
                ym = gy - (P12_BASIN[2] + 0.4) * k - 1.6
            elif code == "WD":
                ym = gy - 0.4 * k - 1.8
            else:
                ym = gy - 2.2
            co.add(xm, ym, P12_ZOOM_TEXT[code])
    W.add("labels", co.marks(size=2.2))
    _p12_shapes(pg, W.shapes())
    if Z["trimmed"]:
        break_mark(pg, xb_s, yb, gy + 2.0)
    bad = sf_assert_g6(k, trees=[(q[0], q[2]) for q in trees], strict=False)
    for s_ in bad:
        log.append(u"p.12 up close: " + s_)
    # the key column: title, callout key, water legend, scale bar
    yy = y1 - 3.0 * CAP - 0.5
    pg.text(u"UP CLOSE · the upstream entry in section", x0, yy, 3.0, COL["ink_dark"], bold=True)
    sz = 2.2
    yk = yy - 2.6
    _p12_shapes(pg, co.key(x0, yk, size=sz))
    nk = len(set(n_ for n_, _x, _y, _t in co.items))
    yw = yk - nk * 1.5 * sz - 0.6
    _p12_shapes(pg, water_legend(x0, yw, size=sz, floods=True))
    yb_ = max(y0 + 0.6, yw - 4 * 1.6 * sz - 3.4)
    _p12_bar(pg, x0, yb_, den, P12_ZOOM_BAR)
    pg.text(sf_scale_text(den), x0 + P12_ZOOM_BAR[-1] * k + 8.0, yb_ + 0.1, FS_MIN, COL["ink_dark"], bold=True)
    log.append(u"p.12: the up-close section (style {}) at {}".format(style, sf_scale_text(den)))


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


def _p12_column(pg, cb):
    """the column beside the map (G7): the two charts, why; the conclusion at its foot (v6: the logic block went,
    the map's numbered steps 1-5 say it once, G4). The blocks share the column's height (equal gaps), measured on a
    dry run first"""
    x, y0, x1, y1 = cb
    w = x1 - x
    blocks = (_p12_coliforms, _p12_plants, _p12_why)
    dry = Page(1, 1)
    hs = []
    yy = y1
    for fn in blocks:
        yn = fn(dry, x, yy, w)
        hs.append(yy - yn)
        yy = yn
    end = r28_para(dry, x, 0.0, w, CONTEXT["system"], 3.2, COL["ink"], kcol=COL["ink_dark"])
    hc = -end + 1.0
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
    Returns [(crop id, bbox, scale den or None)]: wb_system = map + band (both booklet builds take it)."""
    x0, y0, x1, y1 = box
    zones, links = _p12_zones(log)
    f = _p12_figures(zones)
    if not WB_LIVE:                                      # v6.1
        log.append("p.12: no water_balance_results.json: HOLD volume and strip figures left out (run the water balance first)")
    D = basemap_load(log=log)
    hz, gp = P12_ZOOM_H, P12_ZOOM_GAP
    Z = _p12_zoom_geom(zones, D, (x1 - x0 - P12_ZOOM_KEY_W - 6.0) * P12_ZOOM_DEN / 1000.0, log)
    my0, my1 = (y0 + hz + gp, y1) if Z else (y0, y1)   # v9: one band, at the bottom
    xs = x1 - P12_COL_W
    ga = (x0, my0, xs - 7.0, my1)
    n0 = len(pg.items)
    M = _p12_map(pg, ga, zones, links, f, Z, D, log)
    for nx_, ny_ in ((ga[0] + 5.0, ga[1] + 4.0), (ga[2] - 6.0, ga[1] + 4.0), (ga[0] + 5.0, ga[3] - 12.0),
                     (ga[2] - 6.0, ga[3] - 12.0)):
        if not any(lp_hit((nx_ - 3.0, ny_ - 3.0, nx_ + 9.0, ny_ + 10.0), t) for t in M["taken"]):
            break                                     # the map's north arrow in a free corner
    M["taken"].append(_p12_north(pg, nx_, ny_, M["nd"]))
    _p12_map_labels(pg, ga, M, zones, f, D, log)
    _p12_column(pg, (xs, my0, x1, my1))
    bm = items_bbox(pg.items[n0:])
    if not Z:
        return [("wb_system", bm, None)]
    n1 = len(pg.items)
    _p12_zoom(pg, (x0, y0, x1, y0 + hz), Z, "a", log)
    cl = cut_log_line()
    if cl:
        log.append(u"p.12: " + cl)
    return [("wb_system", union(bm, items_bbox(pg.items[n1:])), None)]
