TRN_AMEN = {"parking", "bus_station", "fuel", "car_wash", "taxi", "charging_station"}
OSM_BKIND = {"school": "okul", "university": "okul", "college": "okul", "kindergarten": "okul", "hospital": "resmi",
             "public": "resmi", "civic": "resmi", "government": "resmi", "mosque": "dini", "church": "dini",
             "religious": "dini", "temple": "dini", "chapel": "dini", "synagogue": "dini", "shrine": "dini",
             "cathedral": "dini", "ruins": "harabe", "industrial": "fabrika", "warehouse": "fabrika",
             "construction": "insaat", "greenhouse": "sera"}
PED = {"footway", "path", "pedestrian", "steps", "cycleway", "bridleway", "track", "corridor"}
SKIP_HW = {"proposed", "construction", "platform", "bus_stop", "elevator"}
TREE_SYMBOL_R = {"pine": 3.2, "tree": 2.4, "olive": 2.4, "orchard": 2.4}     # map symbol radius of a surveyed tree


def street_w(r):
    """Measured width of a street or path in metres (see measure_widths); 0.0 where the survey does not show it."""
    return r.get("w") or 0.0


def measure_widths(S):
    """Width of every street and path from the survey: across the centreline every 4 m, the distance between the
    surveyed road edges (YOL_SOSE / YOL_BORDUR / YOL_TOPRAK) on both sides; where the edges are missing, between
    the facing frontages (building outlines, walls, fences). The median of the cuts is kept when enough of them
    (30 % road edges, 50 % frontages) see both sides within 15 m; otherwise the width stays unknown (None).
    An OSM width tag, where mapped, is used as it is."""
    RM = 15.0

    def seg_grid(polys, closed):
        g = Grid(20.0)
        for P in polys:
            n = len(P)
            for k in range(n if closed else n - 1):
                a, b = P[k], P[(k + 1) % n]
                g.add((a, b), (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])))
        return g
    g_edge = seg_grid(S.road_edges, False)
    g_front = seg_grid([P for u in S.bld for P in u["parts"]], True)
    for P in S.walls + S.fences:
        for k in range(len(P) - 1):
            a, b = P[k], P[k + 1]
            g_front.add((a, b), (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])))

    def hit(g, px, py, dx, dy):
        ex, ey = px + dx * RM, py + dy * RM
        best = None
        for a, b in g.query((min(px, ex), min(py, ey), max(px, ex), max(py, ey))):
            r = seg_x((px, py), (dx * RM, dy * RM), a, (b[0] - a[0], b[1] - a[1]))
            if r is not None and r[0] * RM > 0.3 and (best is None or r[0] * RM < best):
                best = r[0] * RM
        return best
    for r in S.roads + S.paths:
        tw_ = num(r["tags"].get("width"))
        if tw_ is not None and 0.5 <= tw_ <= 40.0:
            r["w"], r["w_src"] = tw_, "OSM width"
            continue
        if r["tags"].get("footway") in ("sidewalk", "crossing") or r["tags"].get("path") == "sidewalk":
            r["w"], r["w_src"] = None, None              # part of a street: measuring across it gives the street
            continue
        pts = resample(r["P"], 4.0)
        cuts = []
        for i in range(1, len(pts) - 1):
            x, y = pts[i]
            tx, ty = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
            L_ = math.hypot(tx, ty)
            if L_ >= 1e-6:
                cuts.append((x, y, -ty / L_, tx / L_))
        n = len(cuts)
        r["w"], r["w_src"] = None, None
        if not n:
            continue
        kw = []
        for x, y, nx, ny in cuts:
            a = hit(g_edge, x, y, nx, ny)
            b = hit(g_edge, x, y, -nx, -ny) if a is not None else None
            if a is not None and b is not None:
                kw.append(a + b)
        if len(kw) >= max(3, 0.3 * n):
            kw.sort()
            r["w"], r["w_src"] = kw[len(kw) // 2], "road edges"
            continue
        fw = []
        for x, y, nx, ny in cuts:
            a = hit(g_front, x, y, nx, ny)
            b = hit(g_front, x, y, -nx, -ny) if a is not None else None
            if a is not None and b is not None:
                fw.append(a + b)
        if len(fw) >= max(3, 0.5 * n):
            fw.sort()
            r["w"], r["w_src"] = fw[len(fw) // 2], "frontages"
    g_rd = Grid(30.0)
    for r in S.roads:
        g_rd.add(r, r["bb"])
    for r in S.paths:                                    # a path running inside a street is that street's pavement
        if not r.get("w") or r.get("w_src") == "OSM width":
            continue
        ds = []
        for x, y in resample(r["P"], 4.0):
            near = [pl_dist(x, y, q["P"], False) for q in g_rd.query((x - 20, y - 20, x + 20, y + 20))]
            ds.append(min(near) if near else 1e9)
        ds.sort()
        if ds and ds[len(ds) // 2] < r["w"] / 2.0:
            r["w"], r["w_src"] = None, None


# ============================================================ STREETS AS SURFACES (v16.2)
# Every street with a measured width becomes its surface between two edges. Across the centreline every 2 m each
# side is measured on its own to the surveyed road edge (YOL_SOSE / YOL_BORDUR / YOL_TOPRAK), so an OSM line that is
# off the middle of the street does not matter; a side without a surveyed edge within reach takes the street's
# measured width (measure_widths) less the other side. A street end reaches into the street it meets (half the
# narrower width) so junctions close; a dead end stops where the street does. The surfaces are merged into one outline
# per block of streets (raster union, as the river) and the outline is then laid back onto the measured edges, so the
# two edge lines are the measured ones, not the raster's steps. The open water is never a street: where a street's
# side reaches over the river it stops at the water, except on the bridges (OSM bridge ways, the surveyed decks) and
# where a street crosses the stream.
ROAD_CELL = 0.25           # m, raster of the union
ROAD_SNAP = 0.03           # m, simplification of an outline lying on a measured edge (the raster's steps: 0.75 cell)
ROAD_FILL = C("D3D4CC")    # street surface on the plan: a cool, light stone grey under the warm fabric
ROAD_EDGE = mix(INK, PAPER, 0.5)


def is_bridge(r):
    b = (r["tags"].get("bridge") or "").strip().lower()
    return b not in ("", "no", "0", "false")


def mask_at(F, M, x, y):
    """Is the point in a raster mask over the frame (dict rows / nx / ny / cell)?"""
    u, v = F.local(x, y)
    i, j = int(math.floor((u - F.u0) / M["cell"])), int(math.floor((v - F.v0) / M["cell"]))
    if 0 <= j < M["ny"] and 0 <= i < M["nx"]:
        return (M["rows"][j] >> i) & 1 == 1
    return False


def road_polys(S, wet=None):
    """The surface of every measured street and path as a polygon (world coordinates): [dict(P, bridge)]. With wet
    (a point test for open water), a stretch where a street crosses the stream comes out again as its own piece
    marked bridge, so the water never cuts a street where the street crosses it."""
    g_edge = Grid(20.0)
    for P in S.road_edges:
        for k in range(len(P) - 1):
            a, b = P[k], P[k + 1]
            g_edge.add((a, b), (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])))

    def hit(px, py, dx, dy, rm):
        ex, ey = px + dx * rm, py + dy * rm
        best = None
        for a, b in g_edge.query((min(px, ex), min(py, ey), max(px, ex), max(py, ey))):
            r = seg_x((px, py), (dx * rm, dy * rm), a, (b[0] - a[0], b[1] - a[1]))
            if r is not None and r[0] * rm > 0.3 and (best is None or r[0] * rm < best):
                best = r[0] * rm
        return best

    def smooth(vals, r):
        med = [sorted(vals[max(0, i - r):i + r + 1])[len(vals[max(0, i - r):i + r + 1]) // 2] for i in range(len(vals))]
        return [sum(med[max(0, i - 1):i + 2]) / float(len(med[max(0, i - 1):i + 2])) for i in range(len(med))]
    meas = [r for r in S.roads + S.paths if r.get("w") and r["w"] >= 0.8 and len(r["P"]) >= 2 and
            pl_length(r["P"]) >= 1.0]
    # every vertex of every measured way: an end on another way is a joint, an end on none a dead end
    g_v = Grid(2.0)
    for wi, r in enumerate(meas):
        for p in r["P"]:
            g_v.add((wi, p), (p[0], p[1], p[0], p[1]))

    def joint(wi, p):
        best = 0.0
        for wj, q in g_v.query((p[0] - 0.5, p[1] - 0.5, p[0] + 0.5, p[1] + 0.5)):
            if wj != wi and abs(q[0] - p[0]) <= 0.5 and abs(q[1] - p[1]) <= 0.5:
                best = max(best, meas[wj]["w"] / 2.0)
        return best
    # the stream's direction, to tell a street crossing it from one running along its bank
    g_riv = Grid(30.0)
    for P in getattr(S, "selinus", None) or []:
        for k in range(len(P) - 1):
            a, b = P[k], P[k + 1]
            g_riv.add((a, b), (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])))

    def across(x, y, tx, ty):
        best, d0 = None, 60.0
        for a, b in g_riv.query((x - 60, y - 60, x + 60, y + 60)):
            d = seg_dist(x, y, a[0], a[1], b[0], b[1])
            if d < d0:
                d0, best = d, (a, b)
        if best is None:
            return True                                  # other water: a way over it crosses it
        a, b = best
        L_ = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
        return abs(tx * (b[0] - a[0]) / L_ + ty * (b[1] - a[1]) / L_) < 0.7     # more than 45 degrees off the stream

    out = []
    for wi, r in enumerate(meas):
        w = r["w"]
        P = r["P"]
        pts = resample(P, 2.0)
        if math.hypot(pts[-1][0] - P[-1][0], pts[-1][1] - P[-1][1]) > 0.2:
            pts.append(P[-1])
        n = len(pts)
        if n < 2:
            continue
        rm = min(15.0, 1.5 * w + 2.0)
        T, Ls, Rs = [], [], []
        for k in range(n):
            a_, b_ = pts[max(0, k - 1)], pts[min(n - 1, k + 1)]
            d_ = math.hypot(b_[0] - a_[0], b_[1] - a_[1]) or 1.0
            tx, ty = (b_[0] - a_[0]) / d_, (b_[1] - a_[1]) / d_
            T.append((tx, ty))
            nx, ny = -ty, tx
            a = hit(pts[k][0], pts[k][1], nx, ny, rm)
            b = hit(pts[k][0], pts[k][1], -nx, -ny, rm)
            if a is not None and b is not None and 0.6 * w <= a + b <= 1.5 * w:
                l_, r_ = a, b
            elif a is not None and a <= 1.2 * w and w - a >= 0.3:
                l_, r_ = a, w - a
            elif b is not None and b <= 1.2 * w and w - b >= 0.3:
                l_, r_ = w - b, b
            else:
                l_ = r_ = w / 2.0
            Ls.append(l_)
            Rs.append(r_)
        Ls, Rs = smooth(Ls, 2), smooth(Rs, 2)
        Ls = [max(0.3, min(1.5 * w, v)) for v in Ls]
        Rs = [max(0.3, min(1.5 * w, v)) for v in Rs]
        left = [(p[0] - t[1] * l_, p[1] + t[0] * l_) for p, t, l_ in zip(pts, T, Ls)]
        right = [(p[0] + t[1] * r_, p[1] - t[0] * r_) for p, t, r_ in zip(pts, T, Rs)]
        closed = math.hypot(P[0][0] - P[-1][0], P[0][1] - P[-1][1]) < 0.3
        e0 = 0.5 * (Ls[0] + Rs[0]) if closed else min(0.5 * (Ls[0] + Rs[0]), joint(wi, P[0]))
        e1 = 0.5 * (Ls[-1] + Rs[-1]) if closed else min(0.5 * (Ls[-1] + Rs[-1]), joint(wi, P[-1]))
        t0, t1 = T[0], T[-1]
        L2 = [(left[0][0] - t0[0] * e0, left[0][1] - t0[1] * e0)] + left + [(left[-1][0] + t1[0] * e1, left[-1][1] + t1[1] * e1)]
        R2 = [(right[0][0] - t0[0] * e0, right[0][1] - t0[1] * e0)] + right + [(right[-1][0] + t1[0] * e1, right[-1][1] + t1[1] * e1)]
        brg = is_bridge(r)
        out.append(dict(P=L2 + list(reversed(R2)), bridge=brg))
        if brg or wet is None:
            continue
        # a crossing: a run of stations over open water, the street across the stream there
        k = 0
        while k < n:
            if not wet(pts[k][0], pts[k][1]):
                k += 1
                continue
            k0 = k
            while k < n and wet(pts[k][0], pts[k][1]):
                k += 1
            k1 = k - 1
            tx = sum(T[q][0] for q in range(k0, k1 + 1))
            ty = sum(T[q][1] for q in range(k0, k1 + 1))
            tl = math.hypot(tx, ty) or 1.0
            mid = pts[(k0 + k1) // 2]
            if across(mid[0], mid[1], tx / tl, ty / tl):
                a0, a1 = max(0, k0 - 1), min(n - 1, k1 + 1)
                out.append(dict(P=left[a0:a1 + 1] + list(reversed(right[a0:a1 + 1])), bridge=True))
    return out


def dp_tols(P, tols):
    """Douglas-Peucker on an open chain where every point carries its own tolerance: indices kept."""
    n = len(P)
    if n < 3:
        return list(range(n))
    keep = [False] * n
    keep[0] = keep[-1] = True
    stack = [(0, n - 1)]
    while stack:
        a, b = stack.pop()
        if b <= a + 1:
            continue
        ax, ay = P[a]
        dx, dy = P[b][0] - ax, P[b][1] - ay
        L_ = math.hypot(dx, dy)
        best, bi = 1.0, -1
        for i in range(a + 1, b):
            px, py = P[i]
            d = abs(dy * (px - ax) - dx * (py - ay)) / L_ if L_ > 1e-12 else math.hypot(px - ax, py - ay)
            q = d / tols[i]
            if q > best:
                best, bi = q, i
        if bi >= 0:
            keep[bi] = True
            stack.append((a, bi))
            stack.append((bi, b))
    return [i for i in range(n) if keep[i]]


def mask_regions(F, rows, nx, ny, cell, min_body, min_hole, tol, snap=None, wet_snap=None):
    """Outlines of a raster mask over the frame: [(outer, holes)] in world coordinates, plus the edge polylines (every
    outline less its stretches on the frame edge). snap: polygons (world) whose edges the outline is laid onto where it
    runs within a cell of them, so the outline is the measured edge itself, not the raster's steps; wet_snap: the
    same for the water's outline, whose stretches are then left out of the edge lines (the water draws its own)."""
    u1, v1 = F.u0 + F.w, F.v0 + F.h
    edge = 0.75 * cell

    def local(i, j):
        u, v = F.u0 + i * cell, F.v0 + j * cell
        b = False
        if i <= 0:
            u, b = F.u0, True
        elif u >= u1 - edge:
            u, b = u1, True
        if j <= 0:
            v, b = F.v0, True
        elif v >= v1 - edge:
            v, b = v1, True
        return (u, v), b
    sg = None
    if snap or wet_snap:
        sg = Grid(2.0)
        for tag, polys in ((0, snap or []), (1, wet_snap or [])):
            for P in polys:
                Q = [F.local(x, y) for x, y in P]
                m = len(Q)
                for k in range(m):
                    a, b = Q[k], Q[(k + 1) % m]
                    if abs(a[0] - b[0]) + abs(a[1] - b[1]) < 1e-9:
                        continue
                    sg.add((a, b, tag), (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])))
    rs = cell

    def snap_pt(p):
        best, bq, bt = rs, None, None
        px, py = p
        for a, b, tag in sg.query((px - rs, py - rs, px + rs, py + rs)):
            dx, dy = b[0] - a[0], b[1] - a[1]
            t = ((px - a[0]) * dx + (py - a[1]) * dy) / (dx * dx + dy * dy)
            t = 0.0 if t < 0.0 else (1.0 if t > 1.0 else t)
            qx, qy = a[0] + t * dx, a[1] + t * dy
            d = math.hypot(px - qx, py - qy)
            if d < best:
                best, bq, bt = d, (qx, qy), tag
        return bq, bt
    outers, holes = [], []
    for lp in mask_loops(rows, nx):
        pts, brd = [], []
        for i, j in lp:
            p, b = local(i, j)
            pts.append(p)
            brd.append(b)
        a = signed_area(pts)
        if a >= min_body:
            outers.append([pts, brd, a, []])
        elif a <= -min_hole:
            holes.append([pts, brd, a])
    outers.sort(key=lambda o: o[2])
    for h in holes:
        (x0, y0), (x1, y1) = h[0][0], h[0][1]
        L_ = math.hypot(x1 - x0, y1 - y0) or 1.0
        px, py = (x0 + x1) / 2.0 - (y1 - y0) / L_ * 0.25 * cell, (y0 + y1) / 2.0 + (x1 - x0) / L_ * 0.25 * cell
        for o in outers:
            if pip(px, py, o[0]):
                o[3].append(h)
                break

    def snapped(pts, brd):
        """The ring laid onto the measured edges and simplified: (points, tags) with tag 0 road edge, 1 water edge,
        2 frame edge, None raster."""
        Q, tg = [], []
        for p, b in zip(pts, brd):
            if b:
                Q.append(p)
                tg.append(2)
                continue
            q, t = snap_pt(p)
            Q.append(q if q is not None else p)
            tg.append(t)
        n = len(Q)
        tol_of = [ROAD_SNAP if t in (0, 1) else (0.75 * cell if t is None else 1e-9) for t in tg]
        anchors = [k for k in range(n) if tg[k] == 2]
        if not anchors:
            far = max(range(n), key=lambda k: (Q[k][0] - Q[0][0]) ** 2 + (Q[k][1] - Q[0][1]) ** 2)
            if far == 0:
                return Q, tg
            anchors = [0, far]
        keep = []
        for q in range(len(anchors)):
            s, e = anchors[q], anchors[(q + 1) % len(anchors)]
            idx = list(range(s, e + 1)) if e > s else list(range(s, n)) + list(range(0, e + 1))
            ch = dp_tols([Q[k] for k in idx], [tol_of[k] for k in idx])
            keep += [idx[k] for k in ch[:-1]]
        out, ot = [], []
        for k in keep:
            if not out or abs(Q[k][0] - out[-1][0]) > 1e-6 or abs(Q[k][1] - out[-1][1]) > 1e-6:
                out.append(Q[k])
                ot.append(tg[k])
        while len(out) > 2 and abs(out[0][0] - out[-1][0]) <= 1e-6 and abs(out[0][1] - out[-1][1]) <= 1e-6:
            out.pop()
            ot.pop()
        return out, ot
    regions, lines = [], []
    for pts, brd, area, hl in outers:
        rings = [(pts, brd)] + [(h[0], h[1]) for h in hl]
        final = None
        if sg is not None:
            cand = [snapped(p, b) for p, b in rings]
            if all(len(c[0]) >= 3 for c in cand) and loops_simple([c[0] for c in cand]) and \
                    signed_area(cand[0][0]) > 0 and all(signed_area(c[0]) < 0 for c in cand[1:]):
                final = cand
        if final is None:
            for tl, it in ((tol, 2), (tol, 0), (0.0, 0)):
                cand = [dedupe_ring(smooth_loop(p, b, tl, it) if tl > 0 else p) for p, b in rings]
                if all(len(c) >= 3 for c in cand) and (tl == 0.0 or loops_simple(cand)):
                    final = [(c, [None] * len(c)) for c in cand]
                    break
        if final is None:
            continue
        regions.append(([F.world(u, v) for u, v in final[0][0]], [[F.world(u, v) for u, v in c] for c, t in final[1:]]))
        for c, tg in final:
            n = len(c)
            on = [abs(u - F.u0) < 1e-6 or abs(u - u1) < 1e-6 or abs(v - F.v0) < 1e-6 or abs(v - v1) < 1e-6 for u, v in c]
            cut = [k for k in range(n) if (on[k] and on[(k + 1) % n] and (
                (abs(c[k][0] - c[(k + 1) % n][0]) < 1e-6) or (abs(c[k][1] - c[(k + 1) % n][1]) < 1e-6))) or
                   (tg[k] == 1 and tg[(k + 1) % n] == 1)]
            if not cut:
                lines.append([F.world(u, v) for u, v in c + [c[0]]])
                continue
            cuts = set(cut)
            s0 = (cut[0] + 1) % n
            run = [c[s0]]
            for q in range(1, n + 1):
                k = (s0 + q - 1) % n
                if k in cuts:
                    if len(run) >= 2:
                        lines.append([F.world(u, v) for u, v in run])
                    run = [c[(k + 1) % n]]
                else:
                    run.append(c[(k + 1) % n])
            if len(run) >= 2:
                lines.append([F.world(u, v) for u, v in run])
    return regions, lines


def mask_of(F, polys, cell, nx, ny, holes=None):
    """Raster rows (one int per row) of polygons given in world coordinates (non-zero winding; holes cut out)."""
    rows = [0] * ny
    for P in polys:
        loops = [[F.local(x, y) for x, y in P]]
        for j, spans in poly_spans(loops, F.u0, F.v0, cell, nx, ny, nonzero=True):
            m = rows[j]
            for a, b in spans:
                m |= ((1 << (b - a)) - 1) << a
            rows[j] = m
    if holes:
        hr = mask_of(F, holes, cell, nx, ny)
        rows = [r & ~h for r, h in zip(rows, hr)]
    return rows


def build_road_net(S):
    """The street surfaces merged into one outline per block of streets (S.road_net), their edges (S.road_lines_net),
    the raster itself (S.road_mask, for the sections) and the polygons (S.road_polys). Runs after the river."""
    F = S.F
    S.road_net, S.road_lines_net, S.road_mask, S.road_polys = [], [], None, []
    cell = ROAD_CELL
    nx, ny = int(math.ceil(F.w / cell)), int(math.ceil(F.h / cell))
    wat = [w for w in (getattr(S, "water", None) or []) if len(w["P"]) >= 3]
    wrows = None
    if wat:                                           # the open water (the bridge decks left out: streets cross there)
        wrows = mask_of(F, [w["P"] for w in wat], cell, nx, ny, holes=[h for w in wat for h in (w.get("H") or [])])
        decks = [P for P in (getattr(S, "decks", None) or []) if len(P) >= 3]
        if decks:
            drows = mask_of(F, decks, cell, nx, ny)
            wrows = [a & ~b for a, b in zip(wrows, drows)]
    WM = dict(rows=wrows, nx=nx, ny=ny, cell=cell) if wrows else None
    polys = road_polys(S, (lambda x, y: mask_at(F, WM, x, y)) if WM else None)
    S.road_polys = [d["P"] for d in polys]
    if not polys:
        return
    rows = mask_of(F, [d["P"] for d in polys if not d["bridge"]], cell, nx, ny)
    if wrows:
        rows = [a & ~b for a, b in zip(rows, wrows)]
    br = [d["P"] for d in polys if d["bridge"]]
    if br:
        rows = [a | b for a, b in zip(rows, mask_of(F, br, cell, nx, ny))]
    rows = mask_unpinch(mask_close(rows, nx, 1), nx)
    S.road_mask = dict(rows=rows, nx=nx, ny=ny, cell=cell)
    wet = [w["P"] for w in wat] + [h for w in wat for h in (w.get("H") or [])]
    regions, lines = mask_regions(F, rows, nx, ny, cell, 4.0, 2.0, 0.12, snap=S.road_polys, wet_snap=wet)
    S.road_net = [dict(P=P, H=H) for P, H in regions]
    S.road_lines_net = lines


ROAD_HATCH_SP = 0.13     # v16.5: street hatch, page units (U) between its lines, at 45 degrees ...
ROAD_HATCH_W = 0.03      # ... and their print weight (mm)
ROAD_SOLID = True        # v16.7 (Nil): street surfaces in one solid colour, no hatch lines. False = the v16.6 hatch
ROAD_FILL = (207, 204, 197)       # v16.7: that colour on the plans and in the land-use sections (a warm light grey)
ROAD_FILL_OVER = (178, 178, 184)  # v16.7: the street surfaces over the sound maps (T1), a cool grey that reads on them


def road_overlay(S, B, V, L, order, col=(52, 52, 58)):
    """v16.6: the streets drawn OVER an analysis map without hiding it: each street surface hatched with fine lines
    (no fill, the analysis colours show between them), its edges, and the centre line of a street whose width the
    survey does not show. Used on the sound maps (T1), where the streets are the sources."""
    net = getattr(S, "road_net", None)
    if net:
        for rg_ in net:
            if ROAD_SOLID:                                # v16.7: a solid surface over the map (hides the colour there)
                B.fill(V.Ps([rg_["P"]] + rg_["H"]), ROAD_FILL_OVER, L, order)
            else:
                B.hatch(V.Ps([rg_["P"]] + rg_["H"]), col, L, order, ROAD_HATCH_SP * 1.4 * S.U, w=ROAD_HATCH_W)
        for P in getattr(S, "road_lines_net", []):
            B.line(V.P(P), col, L, order + 1, 0.05)
        for r in S.roads:
            if not r.get("w"):
                B.line(V.P(r["P"]), col, L, order + 1, 0.06)
    else:
        for r in S.roads:
            B.line(V.P(r["P"]), col, L, order + 1, 0.06)


def is_heritage(t):
    h = t.get("historic")
    return (h is not None and h not in ("memorial", "boundary_stone", "milestone", "wayside_cross", "yes")) \
        or t.get("tourism") in ("museum", "attraction")


def zone_class(t):
    lu, le, na, am = t.get("landuse"), t.get("leisure"), t.get("natural"), t.get("amenity")
    if lu in AGRI_TREES_LU:
        return ("agri", "orchard")
    if lu in AGRI_FIELD_LU:
        return ("agri", "field")
    if lu in GREEN_WOOD_LU or na in GREEN_WOOD_NAT:
        return ("green", "wood")
    if le in GREEN_PARK_LE or lu in GREEN_PARK_LU:
        return ("green", "park")
    if lu in GREEN_GRASS_LU or na in GREEN_GRASS_NAT or le in GREEN_GRASS_LE:
        return ("green", "grass")
    if am in ("parking", "bus_station") or lu == "garages":
        return ("transport", None)
    if lu in VACANT_LU:
        return ("vacant", None)
    return None


def poi_class(t):
    am = t.get("amenity")
    if am == "place_of_worship" or is_heritage(t):
        return "religious"
    if am in INST_AMEN:
        return "institutional"
    if "shop" in t or "office" in t or "craft" in t or am in COM_AMEN or \
            t.get("tourism") in ("hotel", "guest_house", "hostel", "motel"):
        return "commercial"
    if am in TRN_AMEN:
        return "transport"
    return None


def chain_segments(segs, tol=0.02):
    """Join 2-point segments that share endpoints into polylines (fewer objects to draw)."""
    key = lambda p: (round(p[0] / tol), round(p[1] / tol))
    ends = {}
    for i, s in enumerate(segs):
        ends.setdefault(key(s[0]), []).append(i)
        ends.setdefault(key(s[-1]), []).append(i)
    used = [False] * len(segs)
    out = []
    for i in range(len(segs)):
        if used[i]:
            continue
        used[i] = True
        line = list(segs[i])
        for direction in (0, 1):
            while True:
                tip = line[-1] if direction == 0 else line[0]
                nxt = None
                for j in ends.get(key(tip), ()):
                    if not used[j]:
                        nxt = j
                        break
                if nxt is None:
                    break
                used[nxt] = True
                s = segs[nxt]
                pts = list(s) if key(s[0]) == key(tip) else list(reversed(s))
                if direction == 0:
                    line += pts[1:]
                else:
                    line = list(reversed(pts[1:])) + line
        out.append(line)
    return out


class Site(object):
    pass


# ------------------------------------------------------------ floors and heights that the survey does not record
NB_K = 5            # unlabelled buildings take the floor count shared by most of the 5 nearest surveyed counts
UNLAB_MIN_A = 12.0  # v50 (MIRAQUA 28 Oct, P06.3): m2, a house outline the survey closed without a floor label is kept
#                     (one storey) from this net area on ...
UNLAB_SHUT = 0.9    # ... unless this share of its outline runs along other buildings (a courtyard or a block's inside)
# Monuments with a published height (OSM way id: metres, source). Used instead of floors x storey height.
DOC_HEIGHT = {
    "1087234401": (19.0, "Red Basilica hall: walls stand to 19 m (Koester 2007, p. 171; Wikipedia 'Red Basilica')"),
    "1222770549": (18.0, "Red Basilica south rotunda: 18 m high (Wikipedia 'Red Basilica')"),
    "1222770550": (18.0, "Red Basilica north rotunda, Kurtulus Camii: 18 m high (Wikipedia 'Red Basilica')"),
}


def nearest_samples(g, x, y, k, skip=None):
    """The k surveyed floor counts nearest to (x, y) as [(distance, sample)], ties in order of position; g is a
    40 m Grid of the samples. Rings of cells are added until no unvisited cell can hold a nearer sample."""
    c = g.c
    i0, j0 = int(math.floor(x / c)), int(math.floor(y / c))
    get = g.d.get
    found = []
    r = 0
    while r <= 60:
        for i in range(i0 - r, i0 + r + 1):
            edge = abs(i - i0) == r
            for j in ((range(j0 - r, j0 + r + 1)) if edge else (j0 - r, j0 + r)):
                for s in get((i, j), ()):
                    if s is not skip:
                        found.append((math.hypot(s[0] - x, s[1] - y), s[0], s[1], s))
        if len(found) >= k:
            found.sort(key=lambda t: t[:3])
            if found[k - 1][0] <= r * c:
                break
        r += 1
    found.sort(key=lambda t: t[:3])
    return [(t[0], t[3]) for t in found[:k]]


def floors_from(nb):
    """The floor count shared by most of the neighbours; a tie goes to the nearest of the tied counts."""
    cnt = {}
    for d, s in nb:
        cnt[s[2]] = cnt.get(s[2], 0) + 1
    top = max(cnt.values())
    for d, s in nb:
        if cnt[s[2]] == top:
            return s[2]


HOUSING = {"residential": "housing", "mixed": "housing", "commercial": "housing", "annex": "housing"}


def floors_loo(samples, g, by_use=None):
    """How well the rule works here: each surveyed count predicted from its NB_K nearest others (of the same use
    for non-housing buildings, as the rule is applied). Returns (tested, % the same, % within one floor)."""
    n = same = near = 0
    for s in samples:
        gg = (by_use or {}).get(s[3], g) if len(s) > 3 and s[3] != "housing" else g
        nb = nearest_samples(gg, s[0], s[1], NB_K, skip=s)
        if not nb:
            continue
        f = floors_from(nb)
        n += 1
        same += f == s[2]
        near += abs(f - s[2]) <= 1
    return (n, 100.0 * same / n, 100.0 * near / n) if n else (0, 0.0, 0.0)


# ============================================================ SITE ASSEMBLY
def build_site(R, osm, places, F):
    S = Site()
    S.F = F
    S.U = F.w / 100.0
    S.frame_area = F.area
    bbm = (F.bb[0] - 40, F.bb[1] - 40, F.bb[2] + 40, F.bb[3] + 40)
    S.bbm = bbm
    S.stats = {}

    def seg_in(s):
        return bb_hit((min(s[0], s[2]), min(s[1], s[3]), max(s[0], s[2]), max(s[1], s[3])), bbm)

    lines = R["lines"]

    # ------------------------------------------------ survey footprints
    segs = []
    for lay in DWG["bld"]:
        segs += [(s[0], s[1], s[2], s[3], lay) for s in lines.get(lay, []) if seg_in(s)]
    segs += drop_x([(s[0], s[1], s[2], s[3], DWG["shed"]) for s in lines.get(DWG["shed"], []) if seg_in(s)])
    segs += [(s[0], s[1], s[2], s[3], "KAPI") for s in lines.get(DWG["door"], []) if seg_in(s)]
    segs += [(s[0], s[1], s[2], s[3], "WALL") for s in lines.get(DWG["walls"][0], []) if seg_in(s)]
    faces = polygonize(segs, holes=True)
    gF = Grid(40.0)
    for i, f in enumerate(faces):
        f["bb"] = bb_pts(f["P"])
        gF.add(i, f["bb"])
    labels = [(t[1], t[2], t[0].strip()) for t in R["texts"].get(DWG["floors"], [])
              if bbm[0] <= t[1] <= bbm[2] and bbm[1] <= t[2] <= bbm[3]]
    BLD_TAGS = set(DWG["bld"]) | {DWG["shed"], "KAPI"}

    def is_yard(tags):
        """A face closed mostly by garden walls is a yard or plot, not a building (its walls outweigh its building
        lines)."""
        return tags.get("WALL", 0.0) > sum(l for t, l in tags.items() if t in BLD_TAGS)

    def in_face(x, y, f):
        return pip(x, y, f["P"]) and not any(pip(x, y, H) for H in f.get("H") or ())
    lab, miss = {}, []
    n_yard_lab = 0
    for (x, y, v) in labels:
        c = [i for i in gF.query((x, y, x, y)) if in_face(x, y, faces[i])]
        if c:
            fi = min(c, key=lambda i: faces[i]["A"])
            if is_yard(faces[fi]["tags"]):
                miss.append((x, y, v))                     # the survey did not close this building's own outline
                n_yard_lab += 1
            else:
                lab.setdefault(fi, []).append((x, y, v))
        else:
            miss.append((x, y, v))
    gT = Grid(10.0)
    for s in segs:
        if s[4] in DWG["bld"] and math.hypot(s[2] - s[0], s[3] - s[1]) <= 6.0:
            gT.add(s, (min(s[0], s[2]), min(s[1], s[3]), max(s[0], s[2]), max(s[1], s[3])))

    def dom_kind(tags):
        best, bl = None, 0.0
        for t, l in tags.items():
            if (t in DWG["bld"] or t == DWG["shed"]) and l > bl:
                best, bl = t, l
        return best

    units = []
    gU_ = Grid(40.0)                                      # every unit so far (for the overlap tests below)

    def add_unit(parts, label, layer, src, tags=None, osm_id=None, holes=None):
        cp = []
        for P in parts:
            cp += [q for q in [F.clip_poly(P)] if q]
        if not cp:
            return None
        hs = [q for q in (F.clip_poly(H) for H in (holes or [])) if q]
        cp = [P if signed_area(P) > 0.0 else P[::-1] for P in cp]    # v50 (MIRAQUA 28 Oct, P06.3): outlines anti-
        hs = [H if signed_area(H) < 0.0 else H[::-1] for H in hs]    # clockwise, holes clockwise: the nonzero fill
        A = sum(shoelace(P)[0] for P in cp) - sum(shoelace(H)[0] for H in hs)   # keeps courtyards open
        if A < 1.0:
            return None
        cx = (sum(shoelace(P)[0] * shoelace(P)[1] for P in cp) - sum(shoelace(H)[0] * shoelace(H)[1] for H in hs)) / A
        cy = (sum(shoelace(P)[0] * shoelace(P)[2] for P in cp) - sum(shoelace(H)[0] * shoelace(H)[2] for H in hs)) / A
        u = dict(parts=cp, holes=hs, A=A, cx=cx, cy=cy, bb=bb_union([bb_pts(P) for P in cp]), layer=layer,
                 label=label, src=src, tags=tags or {}, name=((tags or {}).get("name") or "").strip(), osm_id=osm_id)
        units.append(u)
        gU_.add(u, u["bb"])
        return u

    def holes_in(H, Ps):
        """The holes whose inside lies in one of the outlines Ps."""
        out = []
        for h in H:
            x, y = interior_point(h)
            if any(pip(x, y, Q) for Q in Ps):
                out.append(h)
        return out

    for fi, labs in lab.items():
        f = faces[fi]
        layer = dom_kind(f["tags"]) or "BINA_MESKEN"
        if len(labs) == 1:
            add_unit([f["P"]], labs[0][2], layer, "dwg", holes=f["H"])
            continue
        ticks = [s for s in gT.query(f["bb"]) if pip((s[0] + s[2]) / 2.0, (s[1] + s[3]) / 2.0, f["P"])]
        try:
            for parts, l in split_face(f["P"], labs, ticks):
                add_unit(parts, l[2] if l else None, layer, "dwg", holes=holes_in(f["H"], parts))
        except Exception:
            for P, l in zip(voronoi_split(f["P"], [(l[0], l[1]) for l in labs]), labs):
                if P:
                    add_unit([P], l[2], layer, "dwg", holes=holes_in(f["H"], [P]))
    n_shed = n_yard = 0
    # v50 (MIRAQUA 28 Oct, P06.3): a house outline (BINA_MESKEN, BINA) the survey closed without a floor label is a
    # house too (left out until v49: the undercount on p.06); it is kept as one storey (no label, no surveyed floors)
    # unless it is under UNLAB_MIN_A, a yard closed by garden walls, larger than all but 1 % of the faces holding one
    # floor label, or shut in: UNLAB_SHUT of its outline runs along other buildings (a courtyard, a block's inside)
    bface = [dom_kind(f_["tags"]) is not None and not is_yard(f_["tags"]) for f_ in faces]
    gB = Grid(10.0)                                       # the building faces, for shut_in
    for j_, f_ in enumerate(faces):
        if bface[j_]:
            gB.add(j_, f_["bb"])
    la_ = sorted(faces[fi]["A"] for fi, labs in lab.items() if len(labs) == 1 and
                 DWG["bld"].get(dom_kind(faces[fi]["tags"])) == "mesken")
    a_big = la_[int(0.99 * (len(la_) - 1))] if la_ else None

    def shut_in(fi):
        """the share of face fi's outline whose outside (0.3 m off each edge's middle) lies in another building face"""
        P = faces[fi]["P"] if signed_area(faces[fi]["P"]) > 0.0 else faces[fi]["P"][::-1]
        tot = hit = 0.0
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            l_ = math.hypot(b[0] - a[0], b[1] - a[1])
            if l_ < 1e-6:
                continue
            px = 0.5 * (a[0] + b[0]) + 0.3 * (b[1] - a[1]) / l_
            py = 0.5 * (a[1] + b[1]) - 0.3 * (b[0] - a[0]) / l_
            tot += l_
            for j in gB.query((px, py, px, py)):
                bb = faces[j]["bb"]
                if j != fi and bb[0] <= px <= bb[2] and bb[1] <= py <= bb[3] and in_face(px, py, faces[j]):
                    hit += l_
                    break
        return hit / tot if tot > 0.0 else 0.0
    n_unlab = n_small = n_uyard = n_big = n_shut = 0
    a_unlab = []
    for fi, f in enumerate(faces):
        if fi in lab:
            continue
        layer = dom_kind(f["tags"])
        if (layer == DWG["shed"] and f["A"] > 2.5) or (layer in DWG["bld"] and DWG["bld"][layer] != "mesken" and f["A"] > 8.0):
            if is_yard(f["tags"]):
                n_yard += 1
                continue
            if layer == DWG["shed"]:
                u = add_unit([f["P"]], None, layer, "shed", holes=f["H"])
                n_shed += 1 if u else 0
            else:
                add_unit([f["P"]], None, layer, "dwg", holes=f["H"])
        elif layer in DWG["bld"] and DWG["bld"][layer] == "mesken":   # v50 (P06.3)
            if f["A"] < UNLAB_MIN_A:
                n_small += 1
            elif is_yard(f["tags"]):
                n_uyard += 1
            elif a_big is not None and f["A"] > a_big:
                n_big += 1
            elif shut_in(fi) >= UNLAB_SHUT:
                n_shut += 1
            else:
                u = add_unit([f["P"]], None, layer, "dwg", holes=f["H"])
                if u:
                    u["unlab"] = True
                    n_unlab += 1
                    a_unlab.append(u["A"])
    S.stats["unlabelled"] = n_unlab
    S.stats["unlabelled_left"] = (n_small, n_uyard, n_big, n_shut)
    LOG.append(u"P06.3 buildings: {:,} house outlines (BINA_MESKEN, BINA) the survey closed without a floor label are "
               u"kept as one storey ({:.2f} ha in the frame{}); left out, in and around the frame: {:,} under {:.0f} m², "
               u"{:,} walled yards, {:,} larger than {} (all but 1% of the one-label houses are smaller), {:,} shut in "
               u"by other buildings (courtyards, block insides).".format(
                   n_unlab, sum(a_unlab) / 1e4, (u", the largest " + u", ".join(u"{:,.0f} m²".format(a_) for a_ in
                                                                              sorted(a_unlab)[::-1][:3]))
                   if a_unlab else u"", n_small, UNLAB_MIN_A, n_uyard, n_big,
                   u"{:,.0f} m²".format(a_big) if a_big is not None else u"-", n_shut))
    S.stats["survey_units"] = len([u for u in units if u["src"] == "dwg"])
    S.stats["floor_labels"] = len(labels)
    S.stats["labels_unmatched"] = len(miss)
    S.stats["yards"] = (n_yard, n_yard_lab)

    # ------------------------------------------------ OSM buildings: fill what the survey lacks
    osm_b = []
    if osm:
        Pj = osm["P"]
        for wid, (refs, tags) in osm["ways"].items():
            if "building" in tags and len(refs) >= 4 and refs[0] == refs[-1]:
                P = [Pj(r) for r in refs[:-1]]
                P = [p for p in P if p]
                if len(P) >= 3 and bb_hit(bb_pts(P), bbm):
                    osm_b.append(dict(P=P, A=shoelace(P)[0], cx=shoelace(P)[1], cy=shoelace(P)[2],
                                      bb=bb_pts(P), tags=tags, used=False, id=wid))
    gO = Grid(40.0)
    for b in osm_b:
        gO.add(b, b["bb"])

    def covered(P, A):
        """Share of the OSM outline P already covered by the outlines kept so far (sampled on a fine grid)."""
        bb = bb_pts(P)
        cand = gU_.query(bb)
        if not cand:
            return 0.0
        step = max(0.5, math.sqrt(max(A, 1.0) / 600.0))
        n = hit = 0
        y = bb[1] + step / 2.0
        while y < bb[3]:
            x = bb[0] + step / 2.0
            while x < bb[2]:
                if pip(x, y, P):
                    n += 1
                    if any(pip(x, y, Q) for u in cand for Q in u["parts"]):
                        hit += 1
                x += step
            y += step
        return hit / float(n) if n else 0.0

    def osm_layer(tags):
        kind = OSM_BKIND.get(tags.get("building"))
        return [k for k, v in DWG["bld"].items() if v == kind][0] if kind else "BINA_MESKEN"
    n_fb = n_skip = 0
    for (x, y, v) in miss:
        for b in gO.query((x, y, x, y)):
            if not b["used"] and pip(x, y, b["P"]):
                if covered(b["P"], b["A"]) > 0.2:
                    b["used"] = True                       # OSM's outline is mostly a surveyed building already
                    n_skip += 1
                elif add_unit([b["P"]], v, osm_layer(b["tags"]), "osm+label", b["tags"], b["id"]):
                    b["used"] = True
                    n_fb += 1
                break
    # ------------------------------------------------ floor labels whose building outline the survey never closed:
    # the footprint is unknown, so no building is drawn or analysed there; the count still informs its neighbours
    S.labels_open = [(x, y, v) for (x, y, v) in miss
                     if F.inside(x, y) and not any(pip(x, y, P) for u in gU_.query((x, y, x, y)) for P in u["parts"])]
    S.stats["labels_open"] = len(S.labels_open)
    n_inf = 0
    for b in osm_b:
        if b["used"] or b["A"] < 15.0:
            continue
        if covered(b["P"], b["A"]) > 0.2:
            n_skip += 1
            continue
        if add_unit([b["P"]], None, osm_layer(b["tags"]), "osm", b["tags"], b["id"]):
            n_inf += 1
    S.stats["osm_fallback"] = n_fb
    S.stats["osm_infill"] = n_inf
    S.stats["osm_overlapping"] = n_skip
    # monuments with a published height keep it when the survey draws them (the OSM outline is then not used)
    for b in osm_b:
        if b["id"] in DOC_HEIGHT and not any(u.get("osm_id") == b["id"] for u in units):
            for u in gU_.query(b["bb"]):
                ix, iy = interior_point(u["parts"][0])
                if pip(ix, iy, b["P"]) or any(pip(*interior_point(b["P"]), Q) for Q in u["parts"]):
                    u["doc_id"] = b["id"]
    S.stats["sheds"] = n_shed

    # ------------------------------------------------ uses: survey layer > survey names > places/POIs
    gU = Grid(40.0)
    for u in units:
        gU.add(u, u["bb"])
    for t in R["texts"].get(DWG["names"], []):
        for u in gU.query((t[1], t[2], t[1], t[2])):
            if any(pip(t[1], t[2], P) for P in u["parts"]):
                u["name"] = (u["name"] + " " + t[0].strip()).strip()
                break
    pois = []
    for p in places or []:
        if F.inside(p["x"], p["y"]):
            pois.append(dict(p, in_bld=False))
    if osm:
        for ll, tags in osm["pois"]:
            pc = poi_class(tags)
            if pc:
                x, y = to_dwg(*ll)
                if F.inside(x, y):
                    pois.append(dict(x=x, y=y, cat=pc, name=tags.get("name", ""), src="osm", in_bld=False,
                                     her=is_heritage(tags)))
    S.pois = pois
    gP = Grid(30.0)
    for p in pois:
        gP.add(p, (p["x"], p["y"], p["x"], p["y"]))
    # ---- v16.7: each building's own name, where a source gives one (drawn instead of its type word: "Ulu Camii", not
    #      "mosque"). Survey name text inside it, then a named OpenStreetMap outline over it, then a named place of
    #      worship, heritage or civic point inside it. A name that is only a type word (cami, trafo, depo ...) is
    #      not a name. Nothing is guessed: a building no source names keeps its type word.
    for u in units:
        cand = [(u.get("name") or "", "survey name" if u["src"] not in ("osm", "osm+label") else "OpenStreetMap")]
        ix_, iy_ = interior_point(u["parts"][0])
        for b in gO.query(u["bb"]):
            nm_ = (b["tags"].get("name") or "").strip()
            if nm_ and (pip(ix_, iy_, b["P"]) or any(pip(b["cx"], b["cy"], Q) for Q in u["parts"])):
                cand.append((nm_, "OpenStreetMap"))
        for p in gP.query(u["bb"]):
            if p.get("name") and p["cat"] in ("religious", "institutional") and \
                    any(pip(p["x"], p["y"], Q) for Q in u["parts"]):
                cand.append((p["name"], "OpenStreetMap point" if p.get("src") == "osm" else "places"))
        u["proper"], u["proper_src"] = next(((proper_name(c_), sr_) for c_, sr_ in cand if proper_name(c_)), ("", ""))
    S.stats["named_buildings"] = sum(1 for u in units if u["proper"])
    # ---- pass 1: use (survey layer > survey names > places), surveyed floor counts, OpenStreetMap levels
    for u in units:
        kind = DWG["bld"].get(u["layer"], "mesken")
        cat = KIND_CAT.get(kind, "residential")
        nm = u["name"].lower()
        for key, c in NAME_RULES:
            if key in nm:
                cat = c
                break
        lbl = (u["label"] or "").strip()
        floors, fsrc = None, None
        if lbl.isdigit():
            floors, fsrc = max(1, int(lbl)), "survey"
        elif lbl:
            ll = lbl.lower()
            if ll.startswith("mezar") or ll.startswith("çeş") or ll.startswith("ces"):
                cat, floors, fsrc = "religious", 1, "survey"     # a tomb or fountain, as the survey names it
            elif "fab" in ll:
                cat = "industrial"
            elif "havuz" in ll:
                cat, floors, fsrc = "water", 0, "survey"
        tg = u.get("tags") or {}
        if floors is None:
            lv = num(tg.get("building:levels"))
            if lv is not None and 1.0 <= lv <= 60.0:
                floors, fsrc = int(round(lv)), "osm"
        if floors is None and u.get("unlab"):            # v50 (MIRAQUA 28 Oct, P06.3): no label, no surveyed floors
            floors, fsrc = 1, "unlabelled"
        cnt = {}
        for p in gP.query((u["bb"][0] - 3, u["bb"][1] - 3, u["bb"][2] + 3, u["bb"][3] + 3)):
            inside = any(pip(p["x"], p["y"], P) for P in u["parts"])
            if inside or min(pl_dist(p["x"], p["y"], P, True) for P in u["parts"]) <= 3.0:
                cnt[p["cat"]] = cnt.get(p["cat"], 0) + (2 if inside else 1)
                p["in_bld"] = True
        shop = False
        if u["src"] == "shed":
            cat = "annex"
            floors, fsrc = 1, "shed"                         # a sundurma is one open, roofed level
        elif cat == "residential":
            if cnt.get("religious", 0) >= 2:
                cat = "religious"
            elif cnt.get("institutional", 0) >= 2:
                cat = "institutional"
            elif cnt.get("commercial", 0):
                cat, shop = "commercial", True               # commerce, or mixed use once the floors are known
            elif cnt.get("industrial", 0):
                cat = "industrial"
        u["cat"], u["_shop"] = cat, shop
        u["floors"], u["floors_src"] = floors, fsrc
    # ---- every surveyed floor count, inside a closed outline or not, with the use of the building it stands in
    # (a count whose outline the survey never closed stands for a house). These are the measurements the buildings
    # without a count take theirs from: the count shared by most of the NB_K nearest; civic, sacred, industrial
    # and other non-housing buildings look only at surveyed buildings of their own use, where there are any.
    gUc = Grid(40.0)
    for u in units:
        gUc.add(u, u["bb"])
    samples = []
    for (x, y, v) in labels:
        if not v.isdigit():
            continue
        c_ = "residential"
        for u in gUc.query((x, y, x, y)):
            if u["floors_src"] == "survey" and any(pip(x, y, P) for P in u["parts"]):
                c_ = u["cat"]
                break
        samples.append((x, y, max(1, int(v)), HOUSING.get(c_, c_)))
    gS = Grid(40.0)
    by_use = {}
    for s_ in samples:
        gS.add(s_, (s_[0], s_[1], s_[0], s_[1]))
        if s_[3] != "housing":
            by_use.setdefault(s_[3], Grid(40.0)).add(s_, (s_[0], s_[1], s_[0], s_[1]))
    S.floor_samples = samples
    S.floor_test = floors_loo(samples, gS, by_use)
    for u in units:
        if u["floors"] is None:
            use = HOUSING.get(u["cat"], u["cat"])
            nb = nearest_samples(by_use[use] if use in by_use else gS, u["cx"], u["cy"], NB_K)
            if nb:
                u["floors"], u["floors_src"] = floors_from(nb), "neighbours"
        if u["_shop"] and (u["floors"] or 1) > 1:
            u["cat"] = "mixed"                           # shop below, home above
        u["floors_src"] = u["floors_src"] or "none"
        u["floors"] = u["floors"] if u["floors"] is not None else 0
        del u["_shop"]
    for u in units:                                     # sheds take the use of their neighbour
        if u["cat"] != "annex":
            continue
        best, bd = None, 6.0
        for v in gU.query((u["cx"] - 6, u["cy"] - 6, u["cx"] + 6, u["cy"] + 6)):
            if v is u or v["src"] == "shed" or v["cat"] in ("annex", "water"):
                continue
            d = min(pl_dist(u["cx"], u["cy"], P, True) for P in v["parts"])
            if d < bd:
                bd, best = d, v
        u["cat"] = best["cat"] if best else "residential"
        u["annex"] = True
    units = [u for u in units if u["cat"] != "water"]
    for u in units:
        u.setdefault("annex", False)
        doc = DOC_HEIGHT.get(u.get("doc_id") or u.get("osm_id") or "")
        hh = num((u.get("tags") or {}).get("height"))
        if doc:                                          # a monument with a published height
            u["h"], u["h_src"] = doc
            u["floors"], u["floors_src"] = 1, "published"
        elif hh is not None and 2.0 <= hh <= 200.0 and u["floors_src"] in ("osm", "neighbours", "none"):
            u["h"], u["h_src"] = hh, "OSM height tag"
            if u["floors_src"] != "osm":                  # floors to match the mapped height, not the neighbours'
                u["floors"] = max(1, int(round(hh / STOREY.get(u["cat"], FLOOR_H))))
            u["floors_src"] = "osm"
        elif u["annex"]:
            u["h"] = FLOOR_H * u["floors"]               # one level at the typical storey height
        else:
            u["h"] = u["floors"] * STOREY.get(u["cat"], FLOOR_H)
    S.bld = units
    S.g_bld = Grid(40.0)
    for u in units:
        S.g_bld.add(u, u["bb"])
    for t in R["texts"].get("YAZI_UNSUR", []):           # the survey's own word for a shack
        if "barak" not in t[0].lower():
            continue
        best, bd = None, 8.0
        for u in S.g_bld.query((t[1] - 8, t[2] - 8, t[1] + 8, t[2] + 8)):
            d = 0.0 if any(pip(t[1], t[2], P) for P in u["parts"]) else min(pl_dist(t[1], t[2], P, True) for P in u["parts"])
            if d < bd:
                best, bd = u, d
        if best is not None:
            best["baraka"] = True
            best["name"] = (best["name"] + " " + t[0].strip()).strip()
    mpts = [((s[0] + s[2]) / 2.0, (s[1] + s[3]) / 2.0) for s in lines.get(DWG["minarets"], [])]
    mpts += [(p[0], p[1]) for p in R["points"].get(DWG["minarets"], [])]
    for (x, y) in mpts:                                  # a minaret symbol marks the mosque it belongs to
        best, bd = None, 8.0
        for u in S.g_bld.query((x - 8, y - 8, x + 8, y + 8)):
            d = 0.0 if any(pip(x, y, P) for P in u["parts"]) else min(pl_dist(x, y, P, True) for P in u["parts"])
            if d < bd:
                best, bd = u, d
        if best is not None:
            best["minaret"] = True
            best["minaret_xy"] = (x, y)                  # v16.4: its place, for the minaret in the sections

    # ------------------------------------------------ OSM zones, streets, paths
    S.zones, S.roads, S.paths = [], [], []
    S.roads_noise = []                                  # every street with motor traffic, uncut by the frame (v16.3)
    if osm:
        Pj = osm["P"]

        def make_zone(kind, sub, outers, inners, tags):
            Ps = [q for q in (F.clip_poly(P) for P in outers) if q]
            Hs = [q for q in (F.clip_poly(P) for P in inners) if q]
            if not Ps:
                return
            A = sum(shoelace(P)[0] for P in Ps) - sum(shoelace(H)[0] for H in Hs)
            if A > 1.0:
                S.zones.append(dict(kind=kind, sub=sub, Ps=Ps, Hs=Hs, A=A, bb=bb_union([bb_pts(P) for P in Ps]), tags=tags))
        for refs, tags in osm["ways"].values():
            if len(refs) < 2 or "building" in tags:
                continue
            hw = tags.get("highway")
            if hw and hw not in SKIP_HW and tags.get("area") != "yes":
                P = [p for p in (Pj(r) for r in refs) if p]
                for run in F.clip_line(P):
                    (S.paths if hw in PED else S.roads).append(dict(P=run, bb=bb_pts(run), tags=tags, L=pl_length(run)))
                if len(P) >= 2 and hw in GPG_CAT:
                    for P_, tags_ in kgm_split(P, tags):           # the ring road in its two KGM sections
                        S.roads_noise.append(dict(P=P_, tags=tags_))
                continue
            if refs[0] == refs[-1] and len(refs) >= 4:
                zc = zone_class(tags)
                if zc:
                    P = [p for p in (Pj(r) for r in refs[:-1]) if p]
                    if len(P) >= 3:
                        make_zone(zc[0], zc[1], [P], [], tags)
        for mem, tags in osm["rels"]:
            if tags.get("type") != "multipolygon" or "building" in tags:
                continue
            if tags.get("ref:whc"):                      # v21 (R06-30): OSM's WHS relation is fenced areas, not the
                continue                                 # inscribed boundary; never an area of this map
            zc = zone_class(tags)
            if not zc:
                continue
            outer, inner = [], []
            for ref, role in mem:
                if ref in osm["ways"]:
                    P = [p for p in (Pj(r) for r in osm["ways"][ref][0]) if p]
                    if len(P) >= 2:
                        (inner if role == "inner" else outer).append([(p[0], p[1]) for p in P])
            loops = [c for c in chain_segments(outer, 0.05) if len(c) >= 4]
            holes = [c for c in chain_segments(inner, 0.05) if len(c) >= 4]
            if loops:
                make_zone(zc[0], zc[1], loops, holes, tags)
    S.g_road, S.g_path = Grid(60.0), Grid(60.0)
    for r in S.roads:
        S.g_road.add(r, r["bb"])
    for r in S.paths:
        S.g_path.add(r, r["bb"])
    S.g_green, S.g_park, S.g_vac, S.g_agri = Grid(80.0), Grid(80.0), Grid(80.0), Grid(120.0)
    for z in S.zones:
        {"green": S.g_green, "transport": S.g_park, "vacant": S.g_vac, "agri": S.g_agri}[z["kind"]].add(z, z["bb"])

    # ------------------------------------------------ survey line work (drawn and analysed)
    def clipped(layers):
        segs_ = []
        for lay in layers:
            for s in lines.get(lay, []):
                if seg_in(s):
                    segs_ += F.clip_line([(s[0], s[1]), (s[2], s[3])])
        return chain_segments(segs_)
    S.walls = clipped(DWG["walls"])
    S.walls_hist = clipped(["SINIR_TARIHI_SUR"])
    S.fences = clipped(DWG["fences"])
    S.slopes = clipped(DWG["slopes"])
    S.slope_hatch = clipped([DWG["slope_hatch"]])
    S.stairs = clipped([DWG["stairs"]])
    S.bridges = clipped(DWG["bridges"])
    S.road_edges = clipped(DWG["roads"])
    S.park_lines = clipped([DWG["park"]])
    S.banks = clipped(DWG["banks"])
    S.pools = clipped(DWG["water_misc"])
    S.g_wall = Grid(30.0)                               # surveyed walls
    for P in S.walls:
        S.g_wall.add(P, bb_pts(P))
    S.g_slope = Grid(30.0)                              # surveyed slope (sev) lines: embankments
    for P in S.slopes:
        S.g_slope.add(P, bb_pts(P))
    S.g_redge = Grid(30.0)
    for P in S.road_edges:
        S.g_redge.add(P, bb_pts(P))
    S.g_stairs = Grid(30.0)
    for P in S.stairs:
        S.g_stairs.add(P, bb_pts(P))

    # ------------------------------------------------ the Selinus: OSM centreline widened to the surveyed banks
    build_stream(S, R, osm)

    S.decks = list(getattr(S, "decks", []))

    # ------------------------------------------------ trees (survey symbols, kept symbolic)
    S.trees = []
    for lay, kind in DWG["trees"].items():
        pts = [((s[0] + s[2]) / 2.0, (s[1] + s[3]) / 2.0) for s in lines.get(lay, []) if seg_in(s)]
        pts += [(p[0], p[1]) for p in R["points"].get(lay, [])]
        par = list(range(len(pts)))                    # pieces of one symbol: linked within 1.6 m, transitively

        def root(i):
            while par[i] != i:
                par[i] = par[par[i]]
                i = par[i]
            return i
        g = Grid(2.0)
        for i, p in enumerate(pts):
            g.add(i, (p[0], p[1], p[0], p[1]))
        for i, p in enumerate(pts):
            for j in g.query((p[0] - 1.6, p[1] - 1.6, p[0] + 1.6, p[1] + 1.6)):
                if j != i and math.hypot(p[0] - pts[j][0], p[1] - pts[j][1]) < 1.6:
                    a_, b_ = root(i), root(j)
                    if a_ != b_:
                        par[a_] = b_
        groups = {}
        for i in range(len(pts)):
            groups.setdefault(root(i), []).append(pts[i])
        for grp in groups.values():
            if len(grp) >= 2:
                mx = sum(q[0] for q in grp) / len(grp)
                my = sum(q[1] for q in grp) / len(grp)
                sxx = sum((q[0] - mx) ** 2 for q in grp)
                syy = sum((q[1] - my) ** 2 for q in grp)
                sxy = sum((q[0] - mx) * (q[1] - my) for q in grp)
                tr_, det = sxx + syy, sxx * syy - sxy * sxy
                lam_min = tr_ / 2.0 - math.sqrt(max(0.0, tr_ * tr_ / 4.0 - det))
                if lam_min / len(grp) < 0.01 and tr_ / len(grp) > 0.01:
                    continue                           # dashes on a straight line: the symbol's ground line
            x = sum(q[0] for q in grp) / len(grp)
            y = sum(q[1] for q in grp) / len(grp)
            if F.inside(x, y):
                S.trees.append((x, y, TREE_SYMBOL_R.get(kind, 2.4), kind))
    S.n_trees_surveyed = len(S.trees)                      # positions as surveyed; the radius is the map symbol
    S.g_tree = Grid(20.0)
    for t in S.trees:
        S.g_tree.add(t, (t[0], t[1], t[0], t[1]))

    # ------------------------------------------------ street widths measured on the survey, and the street surfaces
    #                                                  (after the river: a street's side stops at the open water)
    measure_widths(S)
    build_road_net(S)

    # ------------------------------------------------ terrain (survey points + contours + spot heights)
    build_terrain(S, R)
    S.contours = r28e_contours(R, F)                     # v50 (MIRAQUA 28 Oct, P06.1): the stream edge plan's contours
    channel_profile(S)

    # ------------------------------------------------ areas (ground coverage inside the frame)
    S.area = dict((k, 0.0) for k in CAT_ORDER)
    for u in S.bld:
        S.area[u["cat"]] = S.area.get(u["cat"], 0.0) + u["A"]
    for z in S.zones:
        S.area[z["kind"]] += z["A"]
    for r in S.roads + S.paths:                          # streets with a measured width only
        if r.get("w"):
            S.area["transport"] += r["L"] * r["w"]
    S.street_km = (sum(r["L"] for r in S.roads) / 1000.0, sum(r["L"] for r in S.roads if r.get("w")) / 1000.0)
    S.area["water"] += sum(w["A"] for w in S.water)
    S.total_area = sum(S.area.values()) or 1.0
    S.built_area = sum(u["A"] for u in S.bld)
    greens = [z for z in S.zones if z["kind"] == "green"]
    S.n_major_green = len([z for z in greens if z["A"] >= 2500.0])
    S.green_pct = 100.0 * sum(z["A"] for z in greens) / S.frame_area
    S.path_km = sum(p["L"] for p in S.paths) / 1000.0
    return S


