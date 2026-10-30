# ---- M11 (revision 30 Oct 2026, H-A): the building renderer, plan / axonometric / section ---------------------------
# G7 "buildings look like buildings": plan = the footprint outline + a roof reading (ridge and hips, or fall-line
# hatch), never loose stripes; axonometric = light volumes with roofs (idea R09); section = profiles with their real
# heights in m, roofs and openings. Also the merge that fixes the fake parcel division lines AT THE SOURCE (bld_merge,
# called by the site board's build_site and by basemap_export): pieces of one footprint that share an edge become ONE
# outline, so no survey tick, party-wall split or Voronoi cut is ever drawn as a line.
# Geometry: survey m in, items out in the basemap item format (common/basemap.py head):
#   ("fill", rings, hex, alpha, nonzero)   ("line", pts, hex, width_mm, dash_mm, alpha)
#   ("text", s, (x, y), size_mm, hex, bold, align)
# plan items are in survey m (draw them with basemap_draw and the map's T); axo items are already projected (the
# caller's proj); section items are in (s, z) m along the cut (the caller's section transform).
# A unit (building) is either a site board unit (parts, holes, h, floors) or a basemap building (rings, np, h, floors).
# Roof form: the survey records no roof shapes, so the plan and axo read every pitched building as a hipped tile roof
# at BLD_PITCH (the common Bergama roof; a drawing convention, never printed as data); a unit flagged roof="flat" (or
# with h >= BLD_FLAT_H) is drawn flat with a parapet.
BLD_PITCH = 30.0                    # degrees, hipped tile roofs (drawing convention)
BLD_FLAT_H = 1e9                    # m: units at or above this height drawn flat (off: no survey of roof forms)
BLD_STOREY = 3.0                    # m per storey where a unit gives no floor count
BLD_COL = dict(fill="ECE9E3", edge="7D756C", roof="A39A90", her_fill="EEDCDB", her_edge="AF7474",
               wall_lit="F7F5F1", wall_shade="DCD8D1", roof_lit="EAE5DE", roof_shade="CFC8BE", axo_line="7D756C",
               sec_fill="EEEBE6", sec_cut="2C2219", sec_line="7D756C", opening="FFFFFF", glass="9FB3BA",
               text="4A3F35")
BLD_LW = dict(block=0.18, roof=0.07, hatch=0.05, axo=0.08, sec_cut=0.30, sec_line=0.10, glass=0.08)
BLD_MIN_ROOF_MM = 1.6               # a roof mark only where the building is at least this wide on the page


# ------------------------------------------------------------------------------------------- small geometry
def _bld_area(P):
    n = len(P)
    return 0.5 * sum(P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1] for i in range(n))


def _bld_pip(x, y, P):
    c, n = False, len(P)
    j = n - 1
    for i in range(n):
        xi, yi, xj, yj = P[i][0], P[i][1], P[j][0], P[j][1]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi:
            c = not c
        j = i
    return c


def _bld_bb(P):
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    return min(xs), min(ys), max(xs), max(ys)


def _bld_inner(P):
    """a point strictly inside polygon P (its centroid when inside, else the middle of the first span of a scan
    line through it)"""
    A = _bld_area(P)
    n = len(P)
    if abs(A) > 1e-9:
        cx = sum((P[i][0] + P[(i + 1) % n][0]) * (P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1])
                 for i in range(n)) / (6.0 * A)
        cy = sum((P[i][1] + P[(i + 1) % n][1]) * (P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1])
                 for i in range(n)) / (6.0 * A)
        if _bld_pip(cx, cy, P):
            return cx, cy
    else:
        cy = sum(p[1] for p in P) / float(n)
    b = _bld_bb(P)
    for f in (0.5, 0.37, 0.63, 0.25, 0.75, 0.1, 0.9):
        y = b[1] + (b[3] - b[1]) * f
        xs = []
        for i in range(n):
            a, c = P[i], P[(i + 1) % n]
            if (a[1] > y) != (c[1] > y):
                xs.append(a[0] + (y - a[1]) * (c[0] - a[0]) / (c[1] - a[1]))
        xs.sort()
        if len(xs) >= 2 and xs[1] - xs[0] > 1e-6:
            return (xs[0] + xs[1]) / 2.0, y
    return P[0][0], P[0][1]


def _bld_unit(u):
    """(outlines, holes) of a site board unit or a basemap building"""
    if "parts" in u:
        return list(u["parts"]), list(u.get("holes") or [])
    R = u.get("rings") or []
    k = u.get("np", len(R))
    return list(R[:k]), list(R[k:])


def _bld_her(u):
    """a heritage building (basemap flag her, or a site board unit of fabric monument / sacred)"""
    return bool(u.get("her")) or u.get("fabric") in ("monument", "sacred")


def _bld_h(u):
    h = u.get("h")
    if h:
        return float(h)
    f = u.get("floors") or 1
    return BLD_STOREY * f


# ------------------------------------------------------------------------------------------- merge (G7 at the source)
def bld_merge(rings, holes=(), tol=0.03):
    """the outlines of pieces merged where they share an edge (also along part of an edge: T-junctions are split
    first), by cancelling every edge two pieces share: [(outline ccw, [holes cw])]. tol (m): points this close are
    one point. Pieces that only overlap (no shared edge) stay as they are."""
    import math as _m
    pts, grid = [], {}

    def vid(p):
        kx, ky = int(_m.floor(p[0] / tol)), int(_m.floor(p[1] / tol))
        for i in (kx - 1, kx, kx + 1):
            for j in (ky - 1, ky, ky + 1):
                for k in grid.get((i, j), ()):
                    q = pts[k]
                    if abs(q[0] - p[0]) <= tol and abs(q[1] - p[1]) <= tol:
                        return k
        pts.append((float(p[0]), float(p[1])))
        grid.setdefault((kx, ky), []).append(len(pts) - 1)
        return len(pts) - 1
    loops = []
    for R in rings:
        if len(R) >= 3:
            loops.append(list(R) if _bld_area(R) > 0 else list(R)[::-1])
    for H in holes:
        if len(H) >= 3:
            loops.append(list(H) if _bld_area(H) < 0 else list(H)[::-1])
    edges = []
    for R in loops:
        ids = [vid(p) for p in R]
        ids = [k for i, k in enumerate(ids) if k != ids[i - 1]] if len(ids) > 1 else ids
        for i in range(len(ids)):
            a, b = ids[i], ids[(i + 1) % len(ids)]
            if a != b:
                edges.append((a, b))
    C = 5.0                                              # T-junctions: points lying on another piece's edge
    vg = {}
    for k, p in enumerate(pts):
        vg.setdefault((int(_m.floor(p[0] / C)), int(_m.floor(p[1] / C))), []).append(k)
    cnt = {}
    for a, b in edges:
        pa, pb = pts[a], pts[b]
        dx, dy = pb[0] - pa[0], pb[1] - pa[1]
        L2 = dx * dx + dy * dy
        cand = []
        if L2 > (2.0 * tol) ** 2:
            Ln = _m.sqrt(L2)
            for i in range(int(_m.floor((min(pa[0], pb[0]) - tol) / C)), int(_m.floor((max(pa[0], pb[0]) + tol) / C)) + 1):
                for j in range(int(_m.floor((min(pa[1], pb[1]) - tol) / C)),
                               int(_m.floor((max(pa[1], pb[1]) + tol) / C)) + 1):
                    for k in vg.get((i, j), ()):
                        if k == a or k == b:
                            continue
                        p = pts[k]
                        t = ((p[0] - pa[0]) * dx + (p[1] - pa[1]) * dy) / L2
                        if t <= 1e-6 or t >= 1.0 - 1e-6:
                            continue
                        if abs((p[0] - pa[0]) * dy - (p[1] - pa[1]) * dx) / Ln <= tol:
                            cand.append((t, k))
        seq = [a] + [k for _, k in sorted(cand)] + [b]
        for s0, s1 in zip(seq, seq[1:]):
            if s0 != s1:
                cnt[(s0, s1)] = cnt.get((s0, s1), 0) + 1
    out = {}
    keep = [e for e, c in cnt.items() if c > cnt.get((e[1], e[0]), 0)]
    for a, b in keep:
        out.setdefault(a, []).append(b)
    used, res_loops = set(), []
    for a0, b0 in keep:
        if (a0, b0) in used:
            continue
        used.add((a0, b0))
        ring, prev, cur, ok = [a0], a0, b0, False
        for _ in range(len(keep) + 1):
            if cur == a0:
                ok = True
                break
            ring.append(cur)
            nxt = [n for n in out.get(cur, ()) if (cur, n) not in used]
            if not nxt:
                break
            if len(nxt) > 1:                             # a pinch point: the sharpest right turn keeps rings simple
                ix, iy = pts[cur][0] - pts[prev][0], pts[cur][1] - pts[prev][1]
                nxt.sort(key=lambda n: _m.atan2(ix * (pts[n][1] - pts[cur][1]) - iy * (pts[n][0] - pts[cur][0]),
                                                ix * (pts[n][0] - pts[cur][0]) + iy * (pts[n][1] - pts[cur][1])))
            used.add((cur, nxt[0]))
            prev, cur = cur, nxt[0]
        if ok and len(ring) >= 3:
            res_loops.append([pts[k] for k in ring])
    clean = []
    for R in res_loops:                                  # straight-through points go
        changed = True
        while changed and len(R) > 3:
            changed = False
            for i in range(len(R)):
                p, q, r = R[i - 1], R[i], R[(i + 1) % len(R)]
                dx, dy = r[0] - p[0], r[1] - p[1]
                L = _m.hypot(dx, dy)
                if L < 1e-9:
                    continue
                if abs((q[0] - p[0]) * dy - (q[1] - p[1]) * dx) / L <= tol * 0.5 and \
                        (q[0] - p[0]) * dx + (q[1] - p[1]) * dy > 0 and (r[0] - q[0]) * dx + (r[1] - q[1]) * dy > 0:
                    del R[i]
                    changed = True
                    break
        A = _bld_area(R)
        if abs(A) >= 0.05:
            clean.append((A, R))
    outs = [[A, R, []] for A, R in clean if A > 0]
    outs.sort(key=lambda o: o[0])
    for A, R in clean:
        if A < 0:
            x, y = _bld_inner(R[::-1])
            for o in outs:                               # the smallest outline holding it
                if _bld_pip(x, y, o[1]):
                    o[2].append(R)
                    break
    return [(R, H) for _, R, H in outs]


def bld_merge_unit(parts, holes=(), tol=0.03):
    """(parts, holes) of ONE building with its pieces merged into one outline per connected piece (the survey's
    party-wall ticks, extended across the face, are not building edges). The input comes back unchanged when the
    merge would change the area by more than 1 % (a piece overlapping another)."""
    A0 = sum(abs(_bld_area(P)) for P in parts) - sum(abs(_bld_area(H)) for H in holes)
    if len(parts) < 2 and not holes:
        return list(parts), list(holes)
    try:
        res = bld_merge(parts, holes, tol)
    except Exception:
        return list(parts), list(holes)
    A1 = sum(_bld_area(o) + sum(_bld_area(h) for h in hs) for o, hs in res)
    if not res or abs(A1 - A0) > 0.01 * max(A0, 1.0):
        return list(parts), list(holes)
    return [o for o, _ in res], [h for _, hs in res for h in hs]


def bld_blocks(units, tol=0.03):
    """the blocks: buildings that share a wall merged into ONE outline (the plan's outline layer; no party walls
    drawn as lines): [dict(outer, holes, units=[index], h=max height m)]. A block whose merged area exceeds its
    buildings' (a failed merge) falls back to its buildings' own outlines."""
    rings, holes = [], []
    for u in units:
        P_, H_ = _bld_unit(u)
        rings += P_
        holes += H_
    res = bld_merge(rings, holes, tol) if rings else []
    cells = {}
    C = 40.0
    for bi, (o, hs) in enumerate(res):
        b = _bld_bb(o)
        for i in range(int(b[0] // C), int(b[2] // C) + 1):
            for j in range(int(b[1] // C), int(b[3] // C) + 1):
                cells.setdefault((i, j), []).append(bi)
    members = {}
    lone = []
    for i, u in enumerate(units):
        P_, _ = _bld_unit(u)
        if not P_:
            continue
        P0 = max(P_, key=lambda P: abs(_bld_area(P)))
        x, y = _bld_inner(P0 if _bld_area(P0) > 0 else P0[::-1])
        hit = None
        for bi in sorted(cells.get((int(x // C), int(y // C)), ()), key=lambda k: _bld_area(res[k][0])):
            if _bld_pip(x, y, res[bi][0]):
                hit = bi
                break
        if hit is None:
            lone.append(i)
        else:
            members.setdefault(hit, []).append(i)
    out = []
    for bi, idx in members.items():
        o, hs = res[bi]
        A = _bld_area(o) + sum(_bld_area(h) for h in hs)
        A_u = sum(sum(abs(_bld_area(P)) for P in _bld_unit(units[i])[0]) -
                  sum(abs(_bld_area(H)) for H in _bld_unit(units[i])[1]) for i in idx)
        if A > 1.02 * A_u + 1.0:
            lone += idx
            continue
        out.append(dict(outer=o, holes=hs, units=sorted(idx), h=max(_bld_h(units[i]) for i in idx)))
    for i in lone:
        P_, H_ = _bld_unit(units[i])
        for P in P_:
            out.append(dict(outer=P if _bld_area(P) > 0 else P[::-1], holes=[], units=[i], h=_bld_h(units[i])))
        for k, H in enumerate(H_):
            out[-1]["holes"].append(H)
    return out


# ------------------------------------------------------------------------------------------- roof geometry
def bld_rect(P):
    """the minimum-area rectangle round P: (cx, cy, ux, uy, L, W), u along the long side (L >= W)"""
    import math as _m
    pts = sorted(set((round(p[0], 4), round(p[1], 4)) for p in P))
    if len(pts) < 3:
        return None

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    hull = lo[:-1] + hi[:-1]
    best = None
    for i in range(len(hull)):
        a, b = hull[i], hull[(i + 1) % len(hull)]
        L = _m.hypot(b[0] - a[0], b[1] - a[1])
        if L < 1e-9:
            continue
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        su = [p[0] * ux + p[1] * uy for p in hull]
        sv = [-p[0] * uy + p[1] * ux for p in hull]
        area = (max(su) - min(su)) * (max(sv) - min(sv))
        if best is None or area < best[0]:
            best = (area, ux, uy, min(su), max(su), min(sv), max(sv))
    if best is None:
        return None
    _, ux, uy, u0, u1, v0, v1 = best
    cu, cv = (u0 + u1) / 2.0, (v0 + v1) / 2.0
    cx, cy = cu * ux - cv * uy, cu * uy + cv * ux
    Lu, Lv = u1 - u0, v1 - v0
    if Lv > Lu:
        ux, uy, Lu, Lv = -uy, ux, Lv, Lu
    return cx, cy, ux, uy, Lu, Lv


def _bld_clip_seg(a, b, P):
    """the pieces of segment a-b inside polygon P"""
    ts = [0.0, 1.0]
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = len(P)
    for i in range(n):
        p, q = P[i], P[(i + 1) % n]
        ex, ey = q[0] - p[0], q[1] - p[1]
        den = dx * ey - dy * ex
        if abs(den) < 1e-12:
            continue
        t = ((p[0] - a[0]) * ey - (p[1] - a[1]) * ex) / den
        s = ((p[0] - a[0]) * dy - (p[1] - a[1]) * dx) / den
        if 0.0 < t < 1.0 and -1e-9 <= s <= 1.0 + 1e-9:
            ts.append(t)
    ts.sort()
    out = []
    for t0, t1 in zip(ts, ts[1:]):
        if t1 - t0 < 1e-6:
            continue
        tm = (t0 + t1) / 2.0
        if _bld_pip(a[0] + dx * tm, a[1] + dy * tm, P):
            out.append([(a[0] + dx * t0, a[1] + dy * t0), (a[0] + dx * t1, a[1] + dy * t1)])
    return out


def bld_roof_lines(P, mode="ridge", spacing=None):
    """the roof reading of one footprint P (survey m): segments [(a, b)] clipped to P. mode "ridge" = ridge + four
    hips of a hipped roof on the footprint's minimum rectangle; "hatch" = the same plus fall lines across the long
    planes every `spacing` m; "flat" = a parapet line inset 0.4 m; "none" = []"""
    if mode == "none":
        return []
    r = bld_rect(P)
    if r is None:
        return []
    cx, cy, ux, uy, L, W = r
    vx, vy = -uy, ux
    out = []
    if mode == "flat":
        k = 0.4
        if W > 2.5 * k:
            Q = [(cx + ux * su * (L / 2 - k) + vx * sv * (W / 2 - k), cy + uy * su * (L / 2 - k) + vy * sv * (W / 2 - k))
                 for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            for a, b in zip(Q, Q[1:] + Q[:1]):
                out += _bld_clip_seg(a, b, P)
        return out
    h = (L - W) / 2.0
    e1, e2 = (cx - ux * h, cy - uy * h), (cx + ux * h, cy + uy * h)
    segs = [(e1, e2)] if h > 0.05 else []
    for e, su in ((e1, -1), (e2, 1)):
        for sv in (-1, 1):
            segs.append((e, (cx + ux * su * L / 2 + vx * sv * W / 2, cy + uy * su * L / 2 + vy * sv * W / 2)))
    if mode == "hatch" and spacing and h > spacing:
        k = -h + spacing / 2.0
        while k < h:
            for sv in (-1, 1):
                a = (cx + ux * k, cy + uy * k)
                segs.append((a, (a[0] + vx * sv * W / 2, a[1] + vy * sv * W / 2)))
            k += spacing
    for a, b in segs:
        out += _bld_clip_seg(a, b, P)
    return out


def _bld_roof_mode(u, mode):
    if u.get("roof") == "flat" or _bld_h(u) >= BLD_FLAT_H:
        return "flat"
    return mode


# ------------------------------------------------------------------------------------------- plan
def bld_plan_items(units, blocks=None, scale_den=1000.0, roof="ridge", box=None, fill=None, edge=None,
                   roof_col=None, her_fill=None, her_edge=None, alpha=1.0, outline=True, hatch_mm=1.2):
    """G7 plan: buildings as items (survey m): a light fill per building, the roof reading (ridge + hips; roof="hatch"
    adds fall lines every hatch_mm on the page; "none" leaves it out) where the building is at least BLD_MIN_ROOF_MM
    wide at 1:scale_den, and ONE outline per block (blocks: bld_blocks(units), made when not given): no line between
    buildings that share a wall. Heritage units (her=True) in their own tone. box (x0, y0, x1, y1): only what touches
    it."""
    fill, edge = fill or BLD_COL["fill"], edge or BLD_COL["edge"]
    roof_col = roof_col or BLD_COL["roof"]
    her_fill, her_edge = her_fill or BLD_COL["her_fill"], her_edge or BLD_COL["her_edge"]
    mpm = scale_den / 1000.0                             # survey m per page mm

    def hit(P):
        if box is None:
            return True
        b = _bld_bb(P)
        return not (b[2] < box[0] or b[0] > box[2] or b[3] < box[1] or b[1] > box[3])
    out, chunk, chunk_h, roofs = [], [], [], []
    for u in units:
        P_, H_ = _bld_unit(u)
        P_ = [P for P in P_ if len(P) >= 3 and hit(P)]
        if not P_:
            continue
        (chunk_h if _bld_her(u) else chunk).extend(P_ + H_)
        if roof != "none":
            mode = _bld_roof_mode(u, roof)
            for P in P_:
                r = bld_rect(P)
                if r is None or r[5] / mpm < BLD_MIN_ROOF_MM:
                    continue
                roofs += bld_roof_lines(P, mode, hatch_mm * mpm)
        if len(chunk) >= 300:
            out.append(("fill", chunk, fill, alpha, True))
            chunk = []
    if chunk:
        out.append(("fill", chunk, fill, alpha, True))
    if chunk_h:
        out.append(("fill", chunk_h, her_fill, alpha, True))
    for a, b in roofs:
        out.append(("line", [a, b], roof_col, BLD_LW["roof"], None, alpha))
    if outline:
        if blocks is None:
            blocks = bld_blocks(units)
        her_idx = set(i for i, u in enumerate(units) if _bld_her(u))
        for bk in blocks:
            o = bk["outer"] if "outer" in bk else bk["rings"][0]
            hs = bk.get("holes") if "outer" in bk else bk["rings"][1:]
            if len(o) < 3 or not hit(o):
                continue
            col = her_edge if bk.get("her") or (bk.get("units") and all(i in her_idx for i in bk["units"])) else edge
            for R in [o] + list(hs or []):
                out.append(("line", list(R) + [R[0]], col, BLD_LW["block"], None, alpha))
    return out


# ------------------------------------------------------------------------------------------- axonometric
def _bld_mix(a, b, t):
    pa = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    pb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join("%02X" % int(round(pa[i] + (pb[i] - pa[i]) * t)) for i in range(3))


def bld_axo_items(units, proj, view=(-0.70711, -0.70711), ground=None, pitch=BLD_PITCH, box=None, sun=(-0.6, 0.8),
                  cols=None, lw=None, roofs=True):
    """G7 axonometric (idea R09): light volumes with roofs, as page items. proj(x, y, z) -> (X, Y) page mm (the
    caller's axonometric); view = the horizontal direction from the scene TOWARDS the viewer (survey axes), used for
    which walls show and the drawing order (far first); ground(x, y) -> terrain m (else u["z0"] or 0); sun = the
    horizontal light direction (lit walls and roof planes lighter). Pitched units get a hipped roof on their
    minimum rectangle when the footprint fills >= 80 % of it, else a flat top; flat units a flat top."""
    import math as _m
    C = dict(BLD_COL)
    C.update(cols or {})
    lw = lw if lw is not None else BLD_LW["axo"]
    vx, vy = view
    sn = _m.hypot(*sun) or 1.0
    sx, sy = sun[0] / sn, sun[1] / sn
    jobs = []
    for u in units:
        P_, H_ = _bld_unit(u)
        for P in P_:
            if len(P) < 3:
                continue
            if box is not None:
                b = _bld_bb(P)
                if b[2] < box[0] or b[0] > box[2] or b[3] < box[1] or b[1] > box[3]:
                    continue
            P = P if _bld_area(P) > 0 else P[::-1]
            cx, cy = _bld_inner(P)
            jobs.append((cx * vx + cy * vy, u, P, cx, cy))
    jobs.sort(key=lambda j: j[0])                         # far first
    out = []
    for _, u, P, cx, cy in jobs:
        z0 = ground(cx, cy) if ground else float(u.get("z0") or 0.0)
        h = _bld_h(u)
        zt = z0 + h
        walls = []
        n = len(P)
        for i in range(n):
            p, q = P[i], P[(i + 1) % n]
            ex, ey = q[0] - p[0], q[1] - p[1]
            L = _m.hypot(ex, ey)
            if L < 1e-6:
                continue
            nx, ny = ey / L, -ex / L                     # outward (ccw outline)
            if nx * vx + ny * vy <= 1e-6:
                continue
            lit = nx * sx + ny * sy
            col = _bld_mix(C["wall_shade"], C["wall_lit"], max(0.0, min(1.0, 0.5 + 0.5 * lit)))
            mx, my = (p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0
            walls.append((mx * vx + my * vy, [proj(p[0], p[1], z0), proj(q[0], q[1], z0), proj(q[0], q[1], zt),
                                              proj(p[0], p[1], zt)], col))
        walls.sort(key=lambda w: w[0])
        for _, ring, col in walls:
            out.append(("fill", [ring], col, 1.0, True))
            out.append(("line", ring + ring[:1], C["axo_line"], lw, None, 1.0))
        r = bld_rect(P)
        pitched = roofs and _bld_roof_mode(u, "ridge") != "flat" and r is not None and \
            abs(_bld_area(P)) >= 0.8 * r[4] * r[5]
        if pitched:
            rcx, rcy, ux, uy, L, W = r
            wx, wy = -uy, ux
            rise = _m.tan(_m.radians(pitch)) * W / 2.0
            hh = (L - W) / 2.0
            c4 = [(rcx + ux * su * L / 2 + wx * sv * W / 2, rcy + uy * su * L / 2 + wy * sv * W / 2)
                  for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            r1, r2 = (rcx - ux * hh, rcy - uy * hh), (rcx + ux * hh, rcy + uy * hh)
            planes = [([c4[0], c4[1], r2, r1], (-wx, -wy)), ([c4[2], c4[3], r1, r2], (wx, wy)),
                      ([c4[3], c4[0], r1], (-ux, -uy)), ([c4[1], c4[2], r2], (ux, uy))]
            rp = []
            for pl, (nx, ny) in planes:
                pts3 = [(x, y, zt if (x, y) in c4 else zt + rise) for x, y in pl]
                mx = sum(p[0] for p in pl) / len(pl)
                my = sum(p[1] for p in pl) / len(pl)
                lit = nx * sx + ny * sy
                col = _bld_mix(C["roof_shade"], C["roof_lit"], max(0.0, min(1.0, 0.5 + 0.5 * lit)))
                rp.append((mx * vx + my * vy, [proj(*p3) for p3 in pts3], col))
            rp.sort(key=lambda w: w[0])
            for _, ring, col in rp:
                out.append(("fill", [ring], col, 1.0, True))
                out.append(("line", ring + ring[:1], C["axo_line"], lw, None, 1.0))
        else:
            top = [proj(p[0], p[1], zt) for p in P]
            hs = [[proj(p[0], p[1], zt) for p in H] for H in H_ if len(H) >= 3 and _bld_pip(H[0][0], H[0][1], P)]
            out.append(("fill", [top] + hs, C["roof_lit"], 1.0, False))
            out.append(("line", top + top[:1], C["axo_line"], lw, None, 1.0))
    return out


# ------------------------------------------------------------------------------------------- section
def bld_section_profile(s0, s1, z0, h, floors=None, roof="gable", pitch=BLD_PITCH, depth_w=None, wall=0.3,
                        openings=True, label=False, label_mm=2.2, cols=None, lw=None, label_gap_m=1.5):
    """G7 section: ONE building cut between s0 and s1 (m along the section), ground z0 and eaves height h (m), as
    items in (s, z) m: the profile (light fill), the cut walls and floor slabs in ink with a window opening per floor
    in each cut wall (sill 0.90 m, head 2.10 m above the floor where the storey allows), the roof cut: "gable" (cut
    across the ridge: apex in the middle), "hip" (cut along the ridge: slopes of depth_w / 2 at both ends), "flat"
    (a 0.60 m parapet). label=True writes the real height "9.60 m" centred label_gap_m over the roof top (2
    decimals; run it through M2 lp_place when buildings stand close)."""
    import math as _m
    C = dict(BLD_COL)
    C.update(cols or {})
    lw = lw or BLD_LW
    if s1 < s0:
        s0, s1 = s1, s0
    w = s1 - s0
    if w <= 2.0 * wall or h <= 0.5:
        return []
    zt = z0 + h
    t = _m.tan(_m.radians(pitch))
    if roof == "flat":
        top = [(s1, zt), (s1, zt + 0.6), (s1 - wall, zt + 0.6), (s1 - wall, zt), (s0 + wall, zt), (s0 + wall, zt + 0.6),
               (s0, zt + 0.6), (s0, zt)]
        apex = zt + 0.6
    elif roof == "hip":
        run = min(w / 2.0, (depth_w or w) / 2.0)
        rise = t * run
        top = [(s1, zt), (s1 - run, zt + rise), (s0 + run, zt + rise), (s0, zt)]
        apex = zt + rise
    else:
        rise = t * w / 2.0
        top = [(s1, zt), ((s0 + s1) / 2.0, zt + rise), (s0, zt)]
        apex = zt + rise
    prof = [(s0, z0), (s1, z0)] + top
    out = [("fill", [prof], C["sec_fill"], 1.0, True)]
    nf = int(floors) if floors else max(1, int(round(h / BLD_STOREY)))
    st = h / float(nf)
    for k in range(1, nf + 1):                           # floor slabs (the top one under the roof)
        z = z0 + k * st
        out.append(("fill", [[(s0, z - 0.25), (s1, z - 0.25), (s1, z), (s0, z)]], C["sec_cut"], 1.0, True))
    for sa in (s0, s1 - wall):                           # cut walls, each storey with its window opening
        for k in range(nf):
            zf = z0 + k * st
            if openings and st >= 2.4:
                for za, zb in ((zf, zf + 0.9), (zf + 2.1, zf + st)):
                    if zb - za > 1e-3:
                        out.append(("fill", [[(sa, za), (sa + wall, za), (sa + wall, zb), (sa, zb)]], C["sec_cut"], 1.0,
                                    True))
                out.append(("line", [(sa + wall / 2.0, zf + 0.9), (sa + wall / 2.0, zf + 2.1)], C["glass"],
                            lw["glass"], None, 1.0))
            else:
                out.append(("fill", [[(sa, zf), (sa + wall, zf), (sa + wall, zf + st), (sa, zf + st)]], C["sec_cut"],
                            1.0, True))
    out.append(("line", list(top), C["sec_cut"], lw["sec_cut"], None, 1.0))
    out.append(("line", [(s0, z0), (s0, zt)], C["sec_line"], lw["sec_line"], None, 1.0))
    out.append(("line", [(s1, z0), (s1, zt)], C["sec_line"], lw["sec_line"], None, 1.0))
    if label:
        out.append(("text", u"{:.2f} m".format(h), ((s0 + s1) / 2.0, apex + label_gap_m), label_mm, C["text"], False,
                    "MC"))
    return out


def bld_section_items(a, b, units, ground=None, pitch=BLD_PITCH, label=False, openings=True, cols=None):
    """G7 section along the cut a -> b (survey m): every building the cut passes through, as bld_section_profile
    items in (s, z) m (s from a). ground(x, y) -> terrain m (else u["z0"] or 0). The roof is cut "gable" where the
    cut crosses the ridge (within 45 degrees of square to it), else "hip"; flat units flat. Heights are the units'
    own (u["h"], m)."""
    import math as _m
    L = _m.hypot(b[0] - a[0], b[1] - a[1])
    if L < 1e-6:
        return []
    dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    out = []
    for u in units:
        P_, _ = _bld_unit(u)
        for P in P_:
            bb = _bld_bb(P)
            if max(min(a[0], b[0]), bb[0]) > min(max(a[0], b[0]), bb[2]) + 1e-6 or \
                    max(min(a[1], b[1]), bb[1]) > min(max(a[1], b[1]), bb[3]) + 1e-6:
                continue
            ts = []
            n = len(P)
            for i in range(n):
                p, q = P[i], P[(i + 1) % n]
                ex, ey = q[0] - p[0], q[1] - p[1]
                den = dx * ey - dy * ex
                if abs(den) < 1e-12:
                    continue
                t = ((p[0] - a[0]) * ey - (p[1] - a[1]) * ex) / den
                s = ((p[0] - a[0]) * dy - (p[1] - a[1]) * dx) / den
                if -1e-9 <= s < 1.0 - 1e-9:
                    ts.append(t)
            ts.sort()
            r = bld_rect(P)
            across = r is None or abs(dx * r[2] + dy * r[3]) < 0.7071
            mode = _bld_roof_mode(u, "ridge")
            for t0, t1 in zip(ts[0::2], ts[1::2]):
                t0, t1 = max(0.0, t0), min(L, t1)
                if t1 - t0 < 1.0:
                    continue
                mx, my = a[0] + dx * (t0 + t1) / 2.0, a[1] + dy * (t0 + t1) / 2.0
                z0 = ground(mx, my) if ground else float(u.get("z0") or 0.0)
                out += bld_section_profile(t0, t1, z0, _bld_h(u), u.get("floors"),
                                           "flat" if mode == "flat" else ("gable" if across else "hip"), pitch,
                                           r[5] if r else None, openings=openings, label=label, cols=cols)
    return out
