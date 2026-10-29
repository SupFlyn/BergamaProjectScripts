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
P12_ROT = -12.0                      # the axonometric: the plan turned 12 deg clockwise ...
P12_SIN, P12_COS = 0.62, 0.785       # ... and seen from 38 deg above (depth x sin, heights x cos; one scale)
P12_DET_DEN = 2000.0                 # the round zoom: the upstream entry in plan at 1:2,000
P12_DET_R = 46.0                     # its radius, mm (92 m on site)
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
    f["store"] = WB_STORE
    left = _p12_get("design", "river_left_pct")
    f["left"] = tuple(left) if left else None
    mix = _p12_get("design", "mix")
    f["farms"] = _p12_get("cutoff", mix, "central", "delivered_m3_per_year") if mix else None
    ha = [_p12_get("lands", "cropland_ha"), _p12_get("lands", "orchard_ha")]
    f["farm_ha"] = sum(ha) if None not in ha else None
    s2 = _p12_get("lands", "strip_m2")
    f["strip"] = (s2 / 4.0, s2 * STRIP_DEPTH, WB_STRIP) if s2 else None      # 400 cm wide (the strip's design)
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


# ---------------------------------------------------------------- the axonometric map
def _p12_axo(pts, area, margins):
    """T(p, z=0) survey m -> page mm for the map, its inverse at z = 0, and k (page mm per m): the plan turned by
    P12_ROT and seen from above at the angle of P12_SIN / P12_COS, one scale, fitted into area less the margins
    (left, right, bottom, top)"""
    rho = math.radians(P12_ROT)
    c, s = math.cos(rho), math.sin(rho)
    cx, cy = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
    U = [((p[0] - cx) * c - (p[1] - cy) * s, ((p[0] - cx) * s + (p[1] - cy) * c) * P12_SIN) for p in pts]
    u0, u1 = min(u for u, w in U), max(u for u, w in U)
    w0, w1 = min(w for u, w in U), max(w for u, w in U)
    ml, mr, mb, mt = margins
    W, H = area[2] - area[0] - ml - mr, area[3] - area[1] - mb - mt
    k = min(W / max(u1 - u0, 1.0), H / max(w1 - w0, 1.0))
    ox = area[0] + ml + (W - (u1 - u0) * k) / 2.0 - u0 * k
    oy = area[1] + mb + (H - (w1 - w0) * k) / 2.0 - w0 * k

    def T(p, z=0.0):
        u = (p[0] - cx) * c - (p[1] - cy) * s
        v = (p[0] - cx) * s + (p[1] - cy) * c
        return (ox + u * k, oy + (v * P12_SIN + z * P12_COS) * k)

    def Ti(X, Y):
        u, v = (X - ox) / k, (Y - oy) / k / P12_SIN
        return (cx + u * c + v * s, cy - u * s + v * c)
    return T, Ti, k


def _p12_base(pg, items, T, K):
    """the shared basemap items through T, clipped to K"""
    def fill(rings, col, alpha, nonzero):
        rr = [r for r in (_p12_cring(R, K) for R in rings) if r]
        if rr:
            pg.poly(rr, fill=col, alpha=alpha if alpha is not None and alpha < 0.999 else None)

    def line(pts, col, w, dash, alpha):
        for piece in _p12_cline(pts, K):
            pg.line(piece, col, w, dash)
    return basemap_draw(items, T, fill, line)


def _p12_map(pg, ga, zones, links, f, log):
    """the axonometric water map in the area ga (page mm); returns what the labels and the zoom need"""
    key = list(P12_SELINOS) + [p for _, p in P12_PLACES]
    for z in zones:
        key += z["ring"]
    T, Ti, k = _p12_axo(key, ga, (12.0, 16.0, 16.0, 12.0))
    log.append(u"p.12: the water map at about 1:{:,.0f} (a diagram: no scale bar)".format(1000.0 / k))
    K = _p12_clipper([(ga[0], ga[1]), (ga[2], ga[1]), (ga[2], ga[3]), (ga[0], ga[3])], ga)
    # the shared basemap (02 §1): minimal mode (stream, main and lane streets, very faint buildings) with the fields on,
    # so the farms the water goes to read
    D = basemap_load(log=log)
    if D:
        cs = [Ti(ga[0], ga[1]), Ti(ga[2], ga[1]), Ti(ga[2], ga[3]), Ti(ga[0], ga[3])]
        sb = _p12_bbox(cs)
        _p12_base(pg, basemap_items("minimal", {"fields": True}, box=sb, D=D, split_buildings=True), T, K)
    # the zones of the project, flat on the ground
    for z in zones:
        if z["code"] == "STRIP":
            continue
        tones = P12_ZONE.get(z["code"], (COL["faint"], COL["structure"]))
        rr = _p12_cring([T(p) for p in z["ring"]], K)
        if rr:
            pg.poly([rr], fill=tones[0], stroke=tones[1], lw=0.15, alpha=0.9)
    for z in zones:                                      # the summer strip over everything: the line the page follows
        if z["code"] == "STRIP":
            rr = _p12_cring([T(p) for p in z["ring"]], K)
            if rr:
                pg.poly([rr], fill=MP["discharge"][1], stroke=MP["discharge"][2], lw=0.12)
    # the flow: the Selinos line dashed, a chevron every 22 mm pointing downstream
    S = [T(p) for p in P12_SELINOS]
    for piece in _p12_cline(S, K):
        pg.line(piece, MP["discharge"][2], 0.22, [1.0, 0.8])
    Ls = _p12_len(S)
    d = 30.0
    while d < Ls - 20.0:
        (px, py), (ux, uy) = _p12_along(S, d)
        pg.poly([[(px + ux * 1.4, py + uy * 1.4), (px - ux * 1.0 - uy * 1.1, py - uy * 1.0 + ux * 1.1),
                  (px - ux * 1.0 + uy * 1.1, py - uy * 1.0 - ux * 1.1)]], fill=MP["discharge"][2])
        d += 22.0
    segs = [(S[i], S[i + 1]) for i in range(len(S) - 1)]
    taken = []
    # the stream comes in (hand arrow on the first 16 mm) and leaves for the farms (beyond the last point)
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
    # people down to the bed; the upstream entry's links are drawn at their true length in the round zoom
    for ln in links:
        a, b = T(ln["P"][0]), T(ln["P"][-1])
        if ln.get("kind") == "flood":
            r = _p12_arrow(pg, a, b, MP["amphibious"][2], 0.4, 6.0, [1.0, 0.6])
        elif ln.get("kind") == "people":
            r = _p12_arrow(pg, a, b, COL["accent"], 0.3, 4.5, [0.6, 0.5], 1.4)
        elif u"PLANTING" in (ln.get("label") or u""):
            r = _p12_arrow(pg, a, b, P12_ZONE["WP"][2], 0.4, 6.0)
        else:
            r = None
        if r:
            segs.append(r)
    # the round zoom's place on the map: the survey circle it shows, seen in the axonometric (an ellipse), dashed
    det = _p12_pick(zones, "WT", "aras") + _p12_pick(zones, "WS", "aras") + _p12_pick(zones, "WD", "aras") + \
        _p12_pick(zones, "GR", "aras")
    if det:
        bb = _p12_bbox([p for z in det for p in z["ring"]])
        dc = ((bb[0] + bb[2]) / 2.0, (bb[1] + bb[3]) / 2.0)
    else:
        dc = P12_PLACES[0][1]
    Rm = P12_DET_R * P12_DET_DEN / 1000.0
    ell = [T(p) for p in _p12_circle_pts(dc[0], dc[1], Rm, 48)]
    pg.line(ell + ell[:1], COL["ink"], 0.25, [0.8, 0.6])
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
    nd = (T((hold[0], hold[1] + 100.0))[0] - T(hold)[0], T((hold[0], hold[1] + 100.0))[1] - T(hold)[1])
    nl = math.hypot(*nd)
    return dict(T=T, k=k, S=S, segs=segs, taken=taken, at=at, dc=dc, ell=ell, hold=hold, e=e,
                nd=(nd[0] / nl, nd[1] / nl))


def _p12_map_labels(pg, ga, M, zones, f, log):
    """the verbs with their figures (R03, R04), the programme icons along the strip (R05) and the places"""
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
                          big=u"{:,.0f}-{:,.0f} m³".format(*f["store"]),
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


# ---------------------------------------------------------------- the round zoom: the upstream entry in plan, 1:2,000
def _p12_detail(pg, ga, M, zones, links, log):
    """the upstream entry as a plan at 1:2,000 in a circle, in the empty corner of the map farthest from the stream;
    its links at true length, the zones named, the steps numbered as on the map; the scale bar and north arrow
    under it; the dashed lines to its ellipse on the map"""
    R, den = P12_DET_R, P12_DET_DEN
    kd = 1000.0 / den
    dc = M["dc"]
    pts = M["S"] + [M["at"][n] for n in M["at"] if M["at"][n]]
    cands = [(ga[2] - R - 2.0, ga[3] - R - 2.0), (ga[0] + R + 2.0, ga[1] + R + 16.0),
             (ga[2] - R - 2.0, (ga[1] + ga[3]) / 2.0 + 10.0)]
    ccx, ccy = max(cands, key=lambda c: min(math.hypot(p[0] - c[0], p[1] - c[1]) for p in pts))
    Td = lambda p: (ccx + (p[0] - dc[0]) * kd, ccy + (p[1] - dc[1]) * kd)
    C = _p12_circle_pts(ccx, ccy, R, 96)
    h = R * 0.70
    K = _p12_clipper(C, (ccx - h, ccy - h, ccx + h, ccy + h))
    # the dashed connectors from the map's ellipse to the circle (drawn first, under the white disc)
    ec = ((min(p[0] for p in M["ell"]) + max(p[0] for p in M["ell"])) / 2.0,
          (min(p[1] for p in M["ell"]) + max(p[1] for p in M["ell"])) / 2.0)
    dx, dy = ccx - ec[0], ccy - ec[1]
    dl = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / dl, dx / dl
    re = max(abs(nx * (p[0] - ec[0]) + ny * (p[1] - ec[1])) for p in M["ell"])
    for sg in (1, -1):
        pg.line([(ec[0] + nx * re * sg, ec[1] + ny * re * sg), (ccx + nx * R * sg, ccy + ny * R * sg)], COL["ink2"], 0.2,
                [0.8, 0.6])
    pg.poly([C], fill=COL["white"])
    D = basemap_load(log=log)
    if D:
        Rm = R / kd
        _p12_base(pg, basemap_items("simple", None, box=(dc[0] - Rm, dc[1] - Rm, dc[0] + Rm, dc[1] + Rm), D=D,
                                    split_buildings=True), Td, K)
    up = [z for z in zones if (z.get("study_area") or u"").startswith("aras")]
    for z in zones:
        Q = [Td(p) for p in z["ring"]]
        if z["code"] == "STRIP":
            continue
        inside = all(math.hypot(p[0] - ccx, p[1] - ccy) < R - 0.3 for p in Q)
        if z["code"] == "WT" and inside:              # D2 a: common reed only in lined, root-contained cells
            _p12_put(pg, pla_cell_plan("reed", Q, kd))
            continue
        tones = P12_ZONE.get(z["code"], (COL["faint"], COL["structure"]))
        rr = _p12_cring(Q, K)
        if rr:
            pg.poly([rr], fill=tones[0], stroke=tones[1], lw=0.2)
    for z in zones:
        if z["code"] == "STRIP":
            rr = _p12_cring([Td(p) for p in z["ring"]], K)
            if rr:
                pg.poly([rr], fill=MP["discharge"][1], stroke=MP["discharge"][2], lw=0.12)
    taken = []
    segs = []
    for ln in links:                                  # the links at their true length (1:2,000)
        a, b = Td(ln["P"][0]), Td(ln["P"][-1])
        if max(math.hypot(p[0] - ccx, p[1] - ccy) for p in (a, b)) > R - 3.0:
            continue
        col = {"flood": MP["amphibious"][2], "people": COL["accent"]}.get(ln.get("kind"), MP["discharge"][2])
        arrow(pg, [a, b], col, 0.5, 1.8, [0.8, 0.5] if ln.get("kind") == "people" else None)
        segs.append((a, b))
    # the steps where they happen: 1 the stream and the held runoff into the basins, 2 the basins, 4 back to the stream
    lk = dict((ln.get("label") or u"", ln) for ln in links)
    marks = []
    for n, lab, end in ((1, u"RIVER INTO THE CLEANSING BASINS", 0), (1, u"HELD RUNOFF INTO THE CLEANSING BASINS", 0),
                        (4, u"CLEAN WATER BACK TO THE RIVER", -1)):
        if lab in lk:
            p = Td(lk[lab]["P"][end])
            if math.hypot(p[0] - ccx, p[1] - ccy) < R - 3.0:
                marks.append((n, p))
    wt = [z for z in up if z["code"] == "WT"]
    if wt:
        marks.append((2, Td(_p12_cen(wt[0]["ring"]))))
    for n, p in marks:
        taken.append(_p12_step(pg, n, p[0], p[1], 3.2))
    # zone names, inside the circle
    names = {"WT": u"REED BASINS, LINED", "WS": u"RETENTION TERRACES", "WD": u"SPILLWAY", "GR": u"SHADED WALK"}
    specs = []
    for z in up:
        if z["code"] in names:
            c = Td(_p12_cen(z["ring"]))
            if math.hypot(c[0] - ccx, c[1] - ccy) < R - 4.0:
                specs.append(dict(x=c[0], y=c[1], head=u"", small=[names[z["code"]]]))
    for sp in specs:
        w = text_w(sp["small"][0], FS_MIN) + 0.6
        got = label_spot(sp["x"], sp["y"], w, FS_MIN * 1.25, taken, (ccx - h, ccy - h, ccx + h, ccy + h), segs, 0.5,
                         (1.0, 3.0, 6.0, 10.0, 15.0), 24)
        if not got:
            log.append(u"p.12: the zoom has no room for '{}'".format(sp["small"][0]))
            continue
        b = got[0]
        taken.append(b)
        if got[1]:
            e = lp_leader_end(b, (sp["x"], sp["y"]))
            pg.line([(sp["x"], sp["y"]), e], COL["ink2"], 0.15)
        pg.text(sp["small"][0], b[0] + 0.3, b[1] + FS_MIN * 0.3, FS_MIN, COL["ink_dark"], bold=True)
    pg.poly([C], stroke=COL["ink"], lw=0.35)
    # caption, scale bar and north arrow, flush under the circle (SCRIPT_STANDARD §8: a bar beside every plan)
    yb = ccy - R - 4.0
    pg.text(u"UPSTREAM ENTRY · plan 1:{:,.0f}".format(den), ccx - R, yb, 3.0, COL["ink_dark"], bold=True)
    bb = _p12_bar(pg, ccx - R, yb - 6.5, den)
    nb = _p12_north(pg, ccx + R - 4.0, yb - 6.5, (0.0, 1.0), 5.0)
    log.append(u"p.12: the round zoom (upstream entry) in plan at 1:{:,.0f}".format(den))
    return (ccx - R - 0.5, min(bb[1], nb[1]), ccx + R + 0.5, ccy + R + 0.5)


# ---------------------------------------------------------------- beside the map (G7): the logic, two charts, why
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


def _p12_logic(pg, x, y, w):
    """the system's logic: the five steps of the map, one row each (marker, icon, verb, how), joined by the flow"""
    y = _p12_head(pg, x, y, w, u"THE LOGIC, IN ONE DIRECTION", u"numbers as on the map")
    rh = 10.2
    for i, (n, ic, verb, how) in enumerate(CHAIN):
        cy = y - rh / 2.0 + 1.0
        if i:
            pg.line([(x + 2.4, cy + rh - 2.0), (x + 2.4, cy + 2.6)], P12_STEP_COL[n], 0.35)
            pg.poly([[(x + 2.4, cy + 2.2), (x + 1.5, cy + 3.6), (x + 3.3, cy + 3.6)]], fill=P12_STEP_COL[n])
        _p12_step(pg, n, x + 2.4, cy, 4.4)
        _p12_put(pg, ico_draw(ic, x + 10.0, cy, 7.0))
        pg.text(verb, x + 15.5, cy + 0.6, 3.4, P12_STEP_COL[n], bold=True)
        lines = wrap(how, FS_MIN, w - 15.5)[:2]
        for j, ln in enumerate(lines):
            pg.text(ln, x + 15.5, cy - 3.0 - j * FS_MIN * 1.25, FS_MIN, COL["ink"])
        y -= rh
    return y


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
    """the column beside the map (G7): the logic, the two charts, why; the conclusion at its foot. The blocks share
    the column's height (equal gaps), measured on a dry run first"""
    x, y0, x1, y1 = cb
    w = x1 - x
    blocks = (_p12_logic, _p12_coliforms, _p12_plants, _p12_why)
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
    """v5 (revision 29 Oct, T3b WO-T3b-2): the whole p.12 panel in box (page mm, y up): the axonometric water map with
    its round plan zoom on the left, the column beside it on the right. Returns [(crop id, bbox, scale den or None)]."""
    x0, y0, x1, y1 = box
    zones, links = _p12_zones(log)
    f = _p12_figures(zones)
    xs = x1 - P12_COL_W
    ga = (x0, y0, xs - 7.0, y1)
    n0 = len(pg.items)
    M = _p12_map(pg, ga, zones, links, f, log)
    M["taken"].append(_p12_detail(pg, ga, M, zones, links, log))
    for nx_, ny_ in ((ga[0] + 5.0, ga[1] + 4.0), (ga[2] - 6.0, ga[1] + 4.0), (ga[0] + 5.0, ga[3] - 12.0)):
        if not any(lp_hit((nx_ - 3.0, ny_ - 3.0, nx_ + 9.0, ny_ + 10.0), t) for t in M["taken"]):
            break                                     # the map's north arrow in a free corner
    M["taken"].append(_p12_north(pg, nx_, ny_, M["nd"]))
    _p12_map_labels(pg, ga, M, zones, f, log)
    _p12_column(pg, (xs, y0, x1, y1))
    return [("wb_system", items_bbox(pg.items[n0:]), None)]
