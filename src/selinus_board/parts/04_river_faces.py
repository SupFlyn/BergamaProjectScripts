def river_faces(S, R, seeds, cl):
    """The river as the survey draws it: faces closed by stream lines, walls, buildings, bridges and road edges,
    grown from the faces the stream runs through and across stream lines that lie inside the channel."""
    F = S.F
    out = dict(water=[], decks=[], outline=[], faces=[])
    bb = (F.bb[0] - 60, F.bb[1] - 60, F.bb[2] + 60, F.bb[3] + 60)
    bank_l = set(DWG["banks"])
    bridge_l = set(DWG["bridges"])
    layers = DWG["banks"] + DWG["walls"] + DWG["fences"] + list(DWG["bld"]) + DWG["bridges"] + DWG["roads"]
    segs = []
    for lay in layers:
        for s in R["lines"].get(lay, []):
            if bb_hit((min(s[0], s[2]), min(s[1], s[3]), max(s[0], s[2]), max(s[1], s[3])), bb):
                segs.append((s[0], s[1], s[2], s[3], lay))
    if not segs or not seeds:
        return out
    n = len(F.P)
    segs += [(F.P[i][0], F.P[i][1], F.P[(i + 1) % n][0], F.P[(i + 1) % n][1], "FRAME") for i in range(n)]
    faces = polygonize(segs, tol=0.05, gap=1.5)
    gF = Grid(40.0)
    for i, f in enumerate(faces):
        f["bb"] = bb_pts(f["P"])
        gF.add(i, f["bb"])
    gC = Grid(30.0)
    if cl:
        for k in range(len(cl) - 1):
            a, b = cl[k], cl[k + 1]
            gC.add((a, b), (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])))

    def far_from_stream(f, lim=80.0):
        if not cl:
            return False
        for (x, y) in f["P"][::max(1, len(f["P"]) // 40)]:
            near = gC.query((x - lim, y - lim, x + lim, y + lim))
            if not near or min(seg_dist(x, y, a[0], a[1], b[0], b[1]) for a, b in near) > lim:
                return True
        return False

    def is_building(f):
        a, cx, cy = shoelace(f["P"])
        return any(in_unit(cx, cy, u) for u in S.g_bld.query((cx, cy, cx, cy)))

    def acceptable(i):
        f = faces[i]
        if f["A"] < 2.0 or f["A"] > 600000.0:
            return False
        per = sum(math.hypot(f["P"][(k + 1) % len(f["P"])][0] - f["P"][k][0],
                             f["P"][(k + 1) % len(f["P"])][1] - f["P"][k][1]) for k in range(len(f["P"])))
        if 2.0 * f["A"] / max(per, 1e-9) > 70.0:
            return False
        return not is_building(f) and not far_from_stream(f)
    start = set()
    for (x, y) in seeds:
        c = [i for i in gF.query((x, y, x, y)) if pip(x, y, faces[i]["P"])]
        if c:
            start.add(min(c, key=lambda i: faces[i]["A"]))
    edge_faces = {}
    for i, f in enumerate(faces):
        for kk in f["E"]:
            edge_faces.setdefault(kk, []).append(i)
    ok = {}
    queue = [i for i in start if acceptable(i)]
    for i in queue:
        ok[i] = True
    while queue:
        i = queue.pop()
        for kk, tg in zip(faces[i]["E"], faces[i]["ET"]):
            if tg and tg <= bank_l:                      # stream lines inside the channel do not stop the river
                for j in edge_faces.get(kk, ()):
                    if j not in ok:
                        ok[j] = acceptable(j)
                        if ok[j]:
                            queue.append(j)
    for i, good in ok.items():
        if not good:
            continue
        f = faces[i]
        tot = sum(f["tags"].values()) or 1.0
        cp = F.clip_poly(f["P"])
        if not cp:
            continue
        if sum(v for t_, v in f["tags"].items() if t_ in bridge_l) / tot >= 0.3:
            out["decks"].append(cp)
            continue
        out["water"].append(dict(P=cp, A=shoelace(cp)[0], bb=bb_pts(cp)))
        out["faces"].append(f["P"])
        run = []                                         # river edges, without frame and bridge edges
        P = f["P"]
        for k in range(len(P)):
            tg = f["ET"][k]
            if tg and not (tg & bridge_l) and "FRAME" not in tg:
                if not run:
                    run = [P[k]]
                run.append(P[(k + 1) % len(P)])
            else:
                if len(run) >= 2:
                    out["outline"].append(run)
                run = []
        if len(run) >= 2:
            out["outline"].append(run)
    return out


def stream_from_banks(S, R):
    """No OSM centreline: seed the river from the survey's stream names and stream lines."""
    F = S.F
    seeds = [(t[1], t[2]) for t in R["texts"].get(DWG["stream_names"], []) if F.inside(t[1], t[2])]
    for P in S.banks:
        for (x, y) in resample(P, 25.0):
            seeds.append((x, y))
    rf = river_faces(S, R, seeds, None)
    S.water += rf["water"]
    S.decks = list(getattr(S, "decks", [])) + rf["decks"]
    S.water_outline = rf["outline"] or [P for P in S.banks]
    river_union(S)
    S.covered = []
    names = [t[0].strip() for t in R["texts"].get(DWG["stream_names"], []) if F.inside(t[1], t[2]) and t[0].strip()]
    if S.banks:
        main = max(S.banks, key=pl_length)
        p, t = pl_point_at(main, pl_length(main) * 0.5)
        nm = max(set(names), key=names.count) if names else "SELİNOS DERESİ"
        S.river_label = (p[0], p[1], t, tr_upper(nm))


def bank_pair_channel(S):
    """Where both stream lines (HIDRO) exist, the river is simply the ground between them."""
    F = S.F
    chains = [P for P in S.banks if len(P) >= 2 and pl_length(P) > 6.0]
    g = Grid(15.0)
    for ci, P in enumerate(chains):
        for k in range(len(P) - 1):
            a, b = P[k], P[k + 1]
            g.add((ci, a, b), (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])))

    def opposite(p, t, ci):
        best = None
        for cj, a, b in g.query((p[0] - 45, p[1] - 45, p[0] + 45, p[1] + 45)):
            if cj == ci:
                continue
            ex, ey = b[0] - a[0], b[1] - a[1]
            l2 = ex * ex + ey * ey
            if l2 < 1e-9:
                continue
            q = max(0.0, min(1.0, ((p[0] - a[0]) * ex + (p[1] - a[1]) * ey) / l2))
            qx, qy = a[0] + q * ex, a[1] + q * ey
            d = math.hypot(qx - p[0], qy - p[1])
            if not 3.0 <= d <= 45.0:
                continue
            if abs(((qx - p[0]) * t[0] + (qy - p[1]) * t[1]) / d) > 0.5:       # straight across, not along
                continue
            if abs((ex * t[0] + ey * t[1]) / math.sqrt(l2)) < 0.5:              # the other bank runs alongside
                continue
            if best is None or d < best[0]:
                best = (d, (qx, qy))
        return best

    def simple(P):
        n = len(P)
        for i in range(n):
            a, b = P[i], P[(i + 1) % n]
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue
                c, d = P[j], P[(j + 1) % n]
                r = seg_x(a, (b[0] - a[0], b[1] - a[1]), c, (d[0] - c[0], d[1] - c[1]))
                if r and 1e-6 < r[0] < 1 - 1e-6 and 1e-6 < r[1] < 1 - 1e-6:
                    return False
        return True
    # every stream line has one water side; a strip counts only when both lines see each other on that side
    samples = []
    for ci, P in enumerate(chains):
        pts = resample(P, 3.0)
        if math.hypot(pts[-1][0] - P[-1][0], pts[-1][1] - P[-1][1]) > 0.5:
            pts.append(P[-1])
        n = len(pts)
        tans, hits = [], []
        for k in range(n):
            a_, b_ = pts[max(0, k - 1)], pts[min(n - 1, k + 1)]
            d_ = math.hypot(b_[0] - a_[0], b_[1] - a_[1]) or 1.0
            t_ = ((b_[0] - a_[0]) / d_, (b_[1] - a_[1]) / d_)
            tans.append(t_)
            hits.append(opposite(pts[k], t_, ci))
        samples.append((pts, tans, hits))
    water_side = []
    S.bank_sides = []
    for pts, tans, hits in samples:
        sgn = [1 if (t_[0] * (h[1][1] - p[1]) - t_[1] * (h[1][0] - p[0])) > 0 else -1
               for p, t_, h in zip(pts, tans, hits) if h]
        water_side.append(1 if sgn.count(1) >= sgn.count(-1) else -1)
        n1, n2 = sgn.count(1), sgn.count(-1)
        if n1 + n2 >= 3 and max(n1, n2) >= 0.75 * (n1 + n2):   # the side is known: the other bank was seen there
            S.bank_sides.append((pts, tans, 1 if n1 >= n2 else -1))
    gS = Grid(15.0)
    for ci, (pts, tans, hits) in enumerate(samples):
        for p, t_ in zip(pts, tans):
            gS.add((ci, p, t_), (p[0], p[1], p[0], p[1]))

    def side_of(ci, q, p):
        near = [(math.hypot(x[1][0] - q[0], x[1][1] - q[1]), x) for x in gS.query((q[0] - 6, q[1] - 6, q[0] + 6, q[1] + 6))
                if x[0] == ci]
        if not near:
            return None
        _, (c_, qq, t_) = min(near, key=lambda z: z[0])
        return 1 if (t_[0] * (p[1] - qq[1]) - t_[1] * (p[0] - qq[0])) > 0 else -1
    pieces, centres = [], []
    for ci, (pts, tans, hits) in enumerate(samples):
        n = len(pts)
        opp = []
        for k in range(n):
            h = hits[k]
            ok = False
            if h:
                own = 1 if (tans[k][0] * (h[1][1] - pts[k][1]) - tans[k][1] * (h[1][0] - pts[k][0])) > 0 else -1
                cj = min(((math.hypot(x[1][0] - h[1][0], x[1][1] - h[1][1]), x[0])
                          for x in gS.query((h[1][0] - 6, h[1][1] - 6, h[1][0] + 6, h[1][1] + 6)) if x[0] != ci),
                         default=(None, None))[1]
                if own == water_side[ci] and cj is not None and side_of(cj, h[1], pts[k]) == water_side[cj]:
                    ok = True
            opp.append(h[1] if ok else None)
        k = 0                                             # bridge short breaks in the opposite line (<= 30 m)
        while k < n:
            if opp[k] is None:
                j = k
                while j < n and opp[j] is None:
                    j += 1
                if k > 0 and j < n and j - k <= 10:
                    for m in range(k, j):
                        f = (m - k + 1) / float(j - k + 1)
                        opp[m] = (opp[k - 1][0] + (opp[j][0] - opp[k - 1][0]) * f,
                                  opp[k - 1][1] + (opp[j][1] - opp[k - 1][1]) * f)
                k = j
            else:
                k += 1
        for k in range(n):
            if opp[k] is not None:
                centres.append(((pts[k][0] + opp[k][0]) / 2.0, (pts[k][1] + opp[k][1]) / 2.0))
        runs, cur = [], []
        for k in range(n):
            ok = opp[k] is not None
            if ok and cur:
                w0 = math.hypot(opp[cur[-1]][0] - pts[cur[-1]][0], opp[cur[-1]][1] - pts[cur[-1]][1])
                w1 = math.hypot(opp[k][0] - pts[k][0], opp[k][1] - pts[k][1])
                if abs(w1 - w0) > 6.0:                    # a sudden jump means another line was caught: split
                    if len(cur) >= 2:
                        runs.append(cur)
                    cur = []
            if ok:
                cur.append(k)
            else:
                if len(cur) >= 2:
                    runs.append(cur)
                cur = []
        if len(cur) >= 2:
            runs.append(cur)
        for run in runs:
            left = [pts[k] for k in run]
            right = [opp[k] for k in run]
            k = 0
            while k < len(run) - 1:
                m = min(12, len(run) - 1 - k)
                while m > 1:
                    Pp = left[k:k + m + 1] + list(reversed(right[k:k + m + 1]))
                    if simple(Pp):
                        break
                    m //= 2
                Pp = left[k:k + m + 1] + list(reversed(right[k:k + m + 1]))
                cp = F.clip_poly(Pp)                  # merged into one outline afterwards: no slice is dropped
                if cp:
                    pieces.append(cp)
                k += m
    return pieces, chains, centres


# ============================================================ THE RIVER AS ONE OUTLINE
# The channel is first assembled from many short slices (between the two stream lines, or measured out to the
# nearest wall, slope or building). Those slices are merged here into clean outlines: one closed polyline per
# stretch of open water, islands as holes, never crossing itself. Every drawing, hatch and analysis then uses
# these outlines, so Rhino always receives a single, valid boundary to hatch.
RIVER_CELL = 0.5           # m, raster used to merge the slices
RIVER_CLOSE = 1.0          # m, seams and pinholes narrower than twice this are closed
RIVER_TOL = 0.4            # m, outline simplification tolerance
RIVER_DRY = 20.0           # m: the dry side of a surveyed stream line that is never water
RIVER_PAIR_D = 30.0        # m (v16.7): a stream-line pair is the river when it lies within this of its centre line
RIVER_FAR = 80.0           # m (v16.7): how far a wide dry bed is followed to its slope toe or street edge


def poly_spans(loops, u0, v0, cell, nx, ny, nonzero=True):
    """Scanline fill of one or more loops on a grid (cell centres). Yields (row, [(a, b), ...]): cells a..b-1 inside.
    nonzero winding fills overlapping or self-crossing slices; even-odd treats inner loops as holes."""
    edges = []
    for L_ in loops:
        n = len(L_)
        for k in range(n):
            (x0, y0), (x1, y1) = L_[k], L_[(k + 1) % n]
            if y0 == y1:
                continue
            d = 1
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                d = -1
            edges.append((y0, y1, x0, (x1 - x0) / (y1 - y0), d))
    if not edges:
        return
    edges.sort()
    vmax = max(e[1] for e in edges)
    j0 = max(0, int(math.ceil((edges[0][0] - v0) / cell - 0.5)))
    j1 = min(ny - 1, int(math.floor((vmax - v0) / cell - 0.5)))
    active = []
    k, ne = 0, len(edges)
    for j in range(j0, j1 + 1):
        yc = v0 + (j + 0.5) * cell
        while k < ne and edges[k][0] <= yc:
            active.append(edges[k])
            k += 1
        active = [e for e in active if e[1] > yc]
        if not active:
            continue
        xs = sorted((e[2] + (yc - e[0]) * e[3], e[4]) for e in active)
        spans = []
        wnd = 0
        start = 0.0
        for x, d in xs:
            was = wnd != 0
            wnd = (wnd + d) if nonzero else (1 - wnd)
            if wnd != 0 and not was:
                start = x
            elif was and wnd == 0:
                a = max(0, int(math.ceil((start - u0) / cell - 0.5)))
                b = min(nx, int(math.floor((x - u0) / cell - 0.5)) + 1)
                if b > a:
                    spans.append((a, b))
        if spans:
            yield j, spans


def bit_runs(x):
    """(start, length) of every run of set bits in an integer row."""
    while x:
        s = (x & -x).bit_length() - 1
        y = x >> s
        n = ((y + 1) & ~y).bit_length() - 1
        yield s, n
        x &= ~(((1 << n) - 1) << s)


def mask_close(rows, nx, r):
    """Morphological closing with a (2r+1) square: fills seams, slivers and pinholes, never removes water."""
    full = (1 << nx) - 1
    ny = len(rows)

    def dil(x):
        y = x
        for k in range(1, r + 1):
            y |= (x << k) | (x >> k)
        return y & full

    def ero(x):                                      # beyond the frame counts as water, so cuts stay at the edge
        y = x
        for k in range(1, r + 1):
            y &= ((x << k) | ((1 << k) - 1)) & full
            y &= (x >> k) | (full ^ (full >> k))
        return y
    hd = [dil(x) for x in rows]
    D = []
    for j in range(ny):
        y = 0
        for jj in range(max(0, j - r), min(ny, j + r + 1)):
            y |= hd[jj]
        D.append(y)
    he = [ero(x) for x in D]
    out = []
    for j in range(ny):
        y = full
        for jj in range(max(0, j - r), min(ny, j + r + 1)):
            y &= he[jj]
        out.append(y | rows[j])
    return out


def mask_unpinch(rows, nx):
    """Join water cells that touch only at a corner, so every traced outline is a simple loop."""
    full = (1 << nx) - 1
    lim = full >> 1
    for _ in range(6):
        changed = False
        for j in range(len(rows) - 1):
            a, b = rows[j], rows[j + 1]
            p1 = a & ~(a >> 1) & ~b & (b >> 1) & lim
            p2 = ~a & (a >> 1) & b & ~(b >> 1) & lim
            if p1 or p2:
                rows[j] = (a | (p1 << 1) | p2) & full
                changed = True
        if not changed:
            break
    return rows


def mask_loops(rows, nx):
    """Boundary loops of a raster mask in cell-corner coordinates, water on the left: outer loops anticlockwise,
    holes clockwise. Without corner-only contacts every loop is simple and the loops never touch."""
    ny = len(rows)
    nxt = {}
    for j in range(ny):
        m = rows[j]
        if not m:
            continue
        below = rows[j - 1] if j > 0 else 0
        above = rows[j + 1] if j < ny - 1 else 0
        for s, n in bit_runs(m & ~below):
            nxt[(s, j)] = (s + n, j)
        for s, n in bit_runs(m & ~above):
            nxt[(s + n, j + 1)] = (s, j + 1)
        for s, n in bit_runs(m & ~(m >> 1)):
            for i in range(s, s + n):
                nxt[(i + 1, j)] = (i + 1, j + 1)
        for s, n in bit_runs(m & ~(m << 1)):
            for i in range(s, s + n):
                nxt[(i, j + 1)] = (i, j)
    loops = []
    while nxt:
        start, cur = nxt.popitem()
        loop = [start]
        guard = 0
        while cur != start and guard < 10 ** 7:
            loop.append(cur)
            cur = nxt.pop(cur, start)
            guard += 1
        out = []
        n = len(loop)
        for k in range(n):                          # drop vertices in the middle of straight runs
            a, b, c = loop[k - 1], loop[k], loop[(k + 1) % n]
            if (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]) != 0:
                out.append(b)
        if len(out) >= 4:
            loops.append(out)
    return loops


def dp_simplify(P, tol):
    """Douglas-Peucker on an open chain; the two ends are kept."""
    n = len(P)
    if n < 3:
        return list(P)
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
        best, bi = -1.0, -1
        for i in range(a + 1, b):
            px, py = P[i]
            d = abs(dy * (px - ax) - dx * (py - ay)) / L_ if L_ > 1e-12 else math.hypot(px - ax, py - ay)
            if d > best:
                best, bi = d, i
        if best > tol:
            keep[bi] = True
            stack.append((a, bi))
            stack.append((bi, b))
    return [P[i] for i in range(n) if keep[i]]


def chaikin_open(P, it):
    """Corner cutting on an open chain; both ends stay where they are."""
    for _ in range(it):
        n = len(P)
        if n < 3:
            return P
        Q = [P[0]]
        for k in range(n - 1):
            (x0, y0), (x1, y1) = P[k], P[k + 1]
            if k > 0:
                Q.append((0.75 * x0 + 0.25 * x1, 0.75 * y0 + 0.25 * y1))
            if k < n - 2:
                Q.append((0.25 * x0 + 0.75 * x1, 0.25 * y0 + 0.75 * y1))
        Q.append(P[-1])
        P = Q
    return P


def chaikin_closed(P, it):
    for _ in range(it):
        n = len(P)
        Q = []
        for k in range(n):
            (x0, y0), (x1, y1) = P[k], P[(k + 1) % n]
            Q.append((0.75 * x0 + 0.25 * x1, 0.75 * y0 + 0.25 * y1))
            Q.append((0.25 * x0 + 0.75 * x1, 0.25 * y0 + 0.75 * y1))
        P = Q
    return P


def loops_simple(loops, cell=6.0):
    """True when no loop crosses or touches itself or another loop of the same set."""
    segs = []
    for li, L_ in enumerate(loops):
        n = len(L_)
        for k in range(n):
            segs.append((li, k, n, L_[k], L_[(k + 1) % n]))
    g = {}
    for idx, (li, k, n, a, b) in enumerate(segs):
        for gx in range(int(math.floor(min(a[0], b[0]) / cell)), int(math.floor(max(a[0], b[0]) / cell)) + 1):
            for gy in range(int(math.floor(min(a[1], b[1]) / cell)), int(math.floor(max(a[1], b[1]) / cell)) + 1):
                g.setdefault((gx, gy), []).append(idx)
    seen = set()
    for lst in g.values():
        for p in range(len(lst)):
            for q in range(p + 1, len(lst)):
                i1, i2 = lst[p], lst[q]
                key = (i1, i2) if i1 < i2 else (i2, i1)
                if key in seen:
                    continue
                seen.add(key)
                l1, k1, n1, a1, b1 = segs[i1]
                l2, k2, n2, a2, b2 = segs[i2]
                if l1 == l2 and (abs(k1 - k2) == 1 or abs(k1 - k2) == n1 - 1):
                    continue                        # neighbours share their common vertex
                r = seg_x(a1, (b1[0] - a1[0], b1[1] - a1[1]), a2, (b2[0] - a2[0], b2[1] - a2[1]))
                if r is not None:
                    return False
    return True


def smooth_loop(L_, border, tol, it):
    """Simplify and round a raster loop; vertices on the frame edge stay fixed so cuts stay straight."""
    n = len(L_)
    anchors = [k for k in range(n) if border[k]]
    if not anchors:
        far = max(range(n), key=lambda k: (L_[k][0] - L_[0][0]) ** 2 + (L_[k][1] - L_[0][1]) ** 2)
        if far == 0:
            return list(L_)
        a = dp_simplify(L_[:far + 1], tol)
        b = dp_simplify(L_[far:] + [L_[0]], tol)
        return chaikin_closed(a[:-1] + b[:-1], it) if it else a[:-1] + b[:-1]
    out = []
    for q in range(len(anchors)):
        s, e = anchors[q], anchors[(q + 1) % len(anchors)]
        chain = L_[s:e + 1] if e > s else L_[s:] + L_[:e + 1]
        if len(anchors) == 1:
            chain = L_[s:] + L_[:s + 1]
        ch = dp_simplify(chain, tol)
        if it and not (border[s] and border[e] and len(chain) == 2):
            ch = chaikin_open(ch, it)
        out += ch[:-1]
    return out


def dedupe_ring(P, eps=1e-6):
    out = []
    for p in P:
        if not out or abs(p[0] - out[-1][0]) > eps or abs(p[1] - out[-1][1]) > eps:
            out.append(p)
    while len(out) > 2 and abs(out[0][0] - out[-1][0]) <= eps and abs(out[0][1] - out[-1][1]) <= eps:
        out.pop()
    return out


def river_union(S, cell=RIVER_CELL, close_m=RIVER_CLOSE, min_body=25.0, min_hole=40.0):
    """Merge every water slice into clean outlines (see above). Replaces S.water and S.water_outline."""
    F = S.F
    pieces = [w["P"] for w in S.water if len(w["P"]) >= 3]
    if not pieces:
        return
    nx, ny = int(math.ceil(F.w / cell)), int(math.ceil(F.h / cell))
    rows = [0] * ny
    for P in pieces:
        for j, spans in poly_spans([[F.local(x, y) for x, y in P]], F.u0, F.v0, cell, nx, ny, nonzero=True):
            m = rows[j]
            for a, b in spans:
                m |= ((1 << (b - a)) - 1) << a
            rows[j] = m
    rows = mask_unpinch(mask_close(rows, nx, max(1, int(round(close_m / cell)))), nx)
    cut = getattr(S, "river_cut", None)
    if cut:                                         # never over a building or the dry side of a surveyed bank
        sub = mask_of(F, cut["bld"] + cut["dry"], cell, nx, ny)
        rows = mask_unpinch([w_ & ~s_ for w_, s_ in zip(rows, sub)], nx)
    S.water_mask = dict(rows=rows, nx=nx, ny=ny, cell=cell)
    u1, v1 = F.u0 + F.w, F.v0 + F.h
    edge = 0.75 * cell

    def local(i, j):                                 # snap to the frame edge where the water is cut by it
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
    outers, holes = [], []
    for lp in mask_loops(rows, nx):
        pts, brd = [], []
        for i, j in lp:
            p, b = local(i, j)
            pts.append(p)
            brd.append(b)
        a = signed_area(pts)                             # outer loops anticlockwise (+), holes clockwise (-)
        if a >= min_body:
            outers.append([pts, brd, a, []])
        elif a <= -min_hole:
            holes.append([pts, brd, a])
    outers.sort(key=lambda o: o[2])
    for h in holes:                                  # a point just on the water side of the hole's first edge
        (x0, y0), (x1, y1) = h[0][0], h[0][1]
        L_ = math.hypot(x1 - x0, y1 - y0) or 1.0
        px, py = (x0 + x1) / 2.0 - (y1 - y0) / L_ * 0.25 * cell, (y0 + y1) / 2.0 + (x1 - x0) / L_ * 0.25 * cell
        for o in outers:
            if pip(px, py, o[0]):
                o[3].append(h)
                break
    water, outline, nv, fallback = [], [], 0, 0
    for pts, brd, area, hl in outers:
        rings = [(pts, brd)] + [(h[0], h[1]) for h in hl]
        final = None
        for tol, it in ((RIVER_TOL, 2), (RIVER_TOL, 0), (0.0, 0)):
            cand = [dedupe_ring(smooth_loop(p, b, tol, it) if tol > 0 else p) for p, b in rings]
            if all(len(c) >= 3 for c in cand) and (tol == 0.0 or loops_simple(cand)):
                final = cand
                break
        if final is not cand or tol != RIVER_TOL or it != 2:
            fallback += 1                            # this stretch kept a less smoothed (still valid) outline
        nv += sum(len(c) for c in final)
        Pw = [F.world(u, v) for u, v in final[0]]
        Hw = [[F.world(u, v) for u, v in c] for c in final[1:]]
        net = shoelace(final[0])[0] - sum(abs(shoelace(c)[0]) for c in final[1:])
        water.append(dict(P=Pw, H=Hw, A=net, bb=bb_pts(Pw), src="river"))
        for c in final:                              # river lines: every outline minus the cuts at the frame edge
            on = [abs(u - F.u0) < 1e-6 or abs(u - u1) < 1e-6 or abs(v - F.v0) < 1e-6 or abs(v - v1) < 1e-6 for u, v in c]
            n = len(c)
            cut = [k for k in range(n) if on[k] and on[(k + 1) % n] and (
                (abs(c[k][0] - c[(k + 1) % n][0]) < 1e-6) or (abs(c[k][1] - c[(k + 1) % n][1]) < 1e-6))]
            if not cut:
                outline.append([F.world(u, v) for u, v in c + [c[0]]])
                continue
            cuts = set(cut)
            s0 = (cut[0] + 1) % n
            run = [c[s0]]
            for q in range(1, n + 1):
                k = (s0 + q - 1) % n
                if k in cuts:
                    if len(run) >= 2:
                        outline.append([F.world(u, v) for u, v in run])
                    run = [c[(k + 1) % n]]
                else:
                    run.append(c[(k + 1) % n])
            if len(run) >= 2:
                outline.append([F.world(u, v) for u, v in run])
    S.water = water
    S.water_outline = outline
    S.stats["river_outlines"] = (len(water), sum(len(w["H"]) for w in water), nv, fallback)


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


def water_at(S, x, y):
    """Is the point in the river? (raster lookup: fast and consistent with the drawn outline)"""
    M = getattr(S, "water_mask", None)
    if M is None:
        return any(region_contains(x, y, [w["P"]], w.get("H", [])) for w in S.water)
    u, v = S.F.local(x, y)
    i, j = int(math.floor((u - S.F.u0) / M["cell"])), int(math.floor((v - S.F.v0) / M["cell"]))
    if 0 <= j < M["ny"] and 0 <= i < M["nx"]:
        return (M["rows"][j] >> i) & 1 == 1
    return False


def build_stream(S, R, osm):
    F = S.F
    S.water, S.selinus, S.stations, S.river_label, S.water_outline, S.covered = [], [], [], None, [], []
    S.decks = []
    chains = []
    if osm:
        Pj = osm["P"]
        by_name = {}
        for refs, tags in osm["ways"].values():
            if tags.get("waterway") in ("river", "stream", "canal"):
                P = [p for p in (Pj(r) for r in refs) if p]
                if len(P) >= 2:
                    by_name.setdefault(tags.get("name") or "", []).append(P)
        main_named = []                                  # v16.7: every Selinos/Bergama piece, to continue the line
        for nm, segs_ in by_name.items():
            for ch in chain_segments(segs_, 1.0):
                inside = sum(pl_length(r) for r in F.clip_line(ch))
                low = nm.lower().replace("i̇", "i")
                if "selin" in low or "bergama" in low:
                    main_named.append((nm, ch))
                if inside > 30.0:
                    pref = 1.6 if ("selin" in low or "bergama" in low) else (1.0 if nm else 0.5)
                    chains.append((inside * pref, nm, ch))
    if not chains:
        LOG.append("No stream centreline from OSM inside the frame; the river comes from the survey alone.")
        stream_from_banks(S, R)
        S.g_water = Grid(30.0)
        for w in S.water:
            S.g_water.add(w, w["bb"])
        return
    score, sname, cl = max(chains, key=lambda c: c[0])
    # v16.7: the river keeps its course where OSM changes its name. "Selinos Çayı" ends at the Ilıca junction bridge and
    # the same water goes on as "Bergama Deresi" (OSM way 1077764102) to the frame edge; v16.6 stopped at that name
    # change. Pieces named Selinos/Bergama whose end lies within 10 m of either end of the line are joined on (the
    # Ilıca Deresi, which also meets there, is a tributary and is not joined).
    cl = list(cl)
    joined = []
    rest = [(nm, ch) for nm, ch in main_named if ch is not cl and ch != cl]
    grew = True
    while grew and rest:
        grew = False
        for idx_, (nm, ch) in enumerate(rest):
            e0, e1 = cl[0], cl[-1]
            d_ = [(math.hypot(ch[0][0] - e1[0], ch[0][1] - e1[1]), "tail", ch),
                  (math.hypot(ch[-1][0] - e1[0], ch[-1][1] - e1[1]), "tail", list(reversed(ch))),
                  (math.hypot(ch[-1][0] - e0[0], ch[-1][1] - e0[1]), "head", ch),
                  (math.hypot(ch[0][0] - e0[0], ch[0][1] - e0[1]), "head", list(reversed(ch)))]
            dd, where, ch2 = min(d_, key=lambda z: z[0])
            if dd <= 10.0:
                cl = cl + ch2[1:] if where == "tail" else ch2[:-1] + cl
                joined.append(nm)
                rest.pop(idx_)
                grew = True
                break
    S.stats["river_osm_joined"] = joined
    S.river_cl = cl
    # stretches OSM maps as in a tunnel or culvert (used only where the survey shows no open channel)
    g_tun = Grid(20.0)
    n_tun = 0
    for refs, tags in osm["ways"].values():
        if tags.get("waterway") in ("river", "stream", "canal", "drain", "ditch") and (
                tags.get("tunnel") in ("yes", "culvert", "building_passage") or tags.get("covered") == "yes"):
            P = [p for p in (osm["P"](r) for r in refs) if p]
            for k in range(len(P) - 1):
                a_, b_ = P[k], P[k + 1]
                g_tun.add((a_, b_), (min(a_[0], b_[0]) - 6, min(a_[1], b_[1]) - 6, max(a_[0], b_[0]) + 6, max(a_[1], b_[1]) + 6))
                n_tun += 1

    def in_tunnel(q):
        for a_, b_ in g_tun.query((q[0], q[1], q[0], q[1])):
            if seg_dist(q[0], q[1], a_[0], a_[1], b_[0], b_[1]) <= 5.0:
                return True
        return False
    # ---- the channel, sorted by the survey itself: on each side, every 3 m, the edge is the stream line (HIDRO) when
    #      it exists; otherwise the slope toe, then a wall, then a building front - whichever layer is there first.
    #      Administrative lines, symbols, texts and contours never count as edges.
    bbx = (F.bb[0] - 120, F.bb[1] - 120, F.bb[2] + 120, F.bb[3] + 120)

    def seg_grid(layers):
        g = Grid(10.0)
        for lay in layers:
            for s in R["lines"].get(lay, []):
                sb = (min(s[0], s[2]), min(s[1], s[3]), max(s[0], s[2]), max(s[1], s[3]))
                if bb_hit(sb, bbx):
                    g.add(((s[0], s[1]), (s[2], s[3])), sb)
        return g
    PRIORITY = [("stream lines", seg_grid(DWG["banks"]), 30.0),
                ("slope toes", seg_grid(["SEV_ALT", "SEV_SEVALT"]), 25.0),
                ("walls", seg_grid(DWG["walls"]), 25.0),
                ("building fronts", seg_grid(list(DWG["bld"])), 25.0)]

    def hit(g, p, d, maxd):
        q = (p[0] + d[0] * maxd, p[1] + d[1] * maxd)
        best = None
        for s in g.query((min(p[0], q[0]), min(p[1], q[1]), max(p[0], q[0]), max(p[1], q[1]))):
            r = seg_x(p, (q[0] - p[0], q[1] - p[1]), s[0], (s[1][0] - s[0][0], s[1][1] - s[0][1]))
            if r and r[0] * maxd > 0.3 and (best is None or r[0] * maxd < best):
                best = r[0] * maxd
        return best

    def side(p, d):
        for name, g_, maxd in PRIORITY:
            h = hit(g_, p, d, maxd)
            if h is not None:
                return h, name
        return None, None

    def in_building(x, y):
        return any(in_unit(x, y, u) for u in S.g_bld.query((x, y, x, y)))
    # pass 1 - stations on the OSM line: both edges, then a corrected, smooth centre line between them
    L = pl_length(cl)
    stations = []
    s = 0.0
    while s <= L:
        p, t = pl_point_at(cl, s)
        u, v = F.local(p[0], p[1])
        if F.u0 - 60 <= u <= F.u1 + 60 and F.v0 - 60 <= v <= F.v1 + 60:
            stations.append((p, (-t[1], t[0])))
        s += 3.0
    N = len(stations)
    if N < 3:
        S.selinus = F.clip_line(cl)
        return
    off = []
    for p, n_ in stations:
        if in_building(p[0], p[1]):
            off.append(None)
            continue
        (a1, k1), (b1, k2) = side(p, n_), side(p, (-n_[0], -n_[1]))
        off.append((a1 - b1) / 2.0 if (a1 is not None and b1 is not None) else None)

    def fill_series(vals):
        known = [i for i, v_ in enumerate(vals) if v_ is not None]
        if not known:
            return [0.0] * len(vals)
        out_ = list(vals)
        for i in range(len(vals)):
            if out_[i] is None:
                lo = max([k for k in known if k < i], default=None)
                hi = min([k for k in known if k > i], default=None)
                if lo is None:
                    out_[i] = vals[hi]
                elif hi is None:
                    out_[i] = vals[lo]
                else:
                    out_[i] = vals[lo] + (vals[hi] - vals[lo]) * (i - lo) / float(hi - lo)
        return out_

    def median_filter(vals, r):
        return [sorted(vals[max(0, i - r):i + r + 1])[len(vals[max(0, i - r):i + r + 1]) // 2] for i in range(len(vals))]

    def mean_filter(vals, r):
        return [sum(vals[max(0, i - r):i + r + 1]) / float(len(vals[max(0, i - r):i + r + 1])) for i in range(len(vals))]
    off = mean_filter(median_filter(fill_series(off), 5), 3)
    Q = [(p[0] + n_[0] * o, p[1] + n_[1] * o) for (p, n_), o in zip(stations, off)]
    pair_pieces, pair_chains, pair_centres = bank_pair_channel(S)
    # v16.7: only the river's own stream-line pairs are river. Another pair of HIDRO lines (the strip labelled "Kestel
    # Deresi" north of the Ilıca junction, which Nil confirmed on site is not a river bed) is no longer filled; its
    # lines stay as thin surveyed stream lines. A pair counts when its middle lies within RIVER_PAIR_D of the river's
    # centre line (OSM, joined as above).
    g_cl = Grid(20.0)
    for k in range(len(cl) - 1):
        a_, b_ = cl[k], cl[k + 1]
        g_cl.add((a_, b_), (min(a_[0], b_[0]), min(a_[1], b_[1]), max(a_[0], b_[0]), max(a_[1], b_[1])))

    def d_cl(x, y, r=RIVER_PAIR_D):
        best = None
        for a_, b_ in g_cl.query((x - r, y - r, x + r, y + r)):
            d_ = seg_dist(x, y, a_[0], a_[1], b_[0], b_[1])
            if best is None or d_ < best:
                best = d_
        return best if best is not None else 1e9

    def on_main(pts):
        near_ = sum(1 for x, y in pts if d_cl(x, y) <= RIVER_PAIR_D)
        return near_ >= 0.5 * len(pts)
    keep_p = [P for P in pair_pieces if on_main(P)]
    S.stats["river_pairs_dropped"] = [(round(shoelace(P)[1]), round(shoelace(P)[2]), round(abs(shoelace(P)[0])))
                                      for P in pair_pieces if not on_main(P)]
    pair_pieces = keep_p
    pair_chains = [P for P in pair_chains if on_main(resample(P, 3.0))]
    pair_centres = [c_ for c_ in pair_centres if d_cl(c_[0], c_[1]) <= RIVER_PAIR_D]
    S.bank_sides = [b_ for b_ in getattr(S, "bank_sides", []) if on_main(b_[0])]
    gC = Grid(15.0)
    for c_ in pair_centres:
        gC.add(c_, (c_[0], c_[1], c_[0], c_[1]))
    for i in range(N):                                   # inside the paired channel the centre is its true middle
        q = Q[i]
        near = [(math.hypot(c_[0] - q[0], c_[1] - q[1]), c_) for c_ in gC.query((q[0] - 20, q[1] - 20, q[0] + 20, q[1] + 20))]
        if near:
            d_, c_ = min(near, key=lambda z: z[0])
            if d_ <= 20.0:
                Q[i] = c_
    T = []
    for i in range(N):                                   # direction from the nearest distinct centres around i
        lo_, hi_ = max(0, i - 2), min(N - 1, i + 2)
        while lo_ > 0 and math.hypot(Q[hi_][0] - Q[lo_][0], Q[hi_][1] - Q[lo_][1]) < 1.0:
            lo_ -= 1
        while hi_ < N - 1 and math.hypot(Q[hi_][0] - Q[lo_][0], Q[hi_][1] - Q[lo_][1]) < 1.0:
            hi_ += 1
        a_, b_ = Q[lo_], Q[hi_]
        d_ = math.hypot(b_[0] - a_[0], b_[1] - a_[1])
        if d_ < 1e-9:
            a_, b_ = stations[max(0, i - 1)][0], stations[min(N - 1, i + 1)][0]
            d_ = math.hypot(b_[0] - a_[0], b_[1] - a_[1]) or 1.0
        T.append(((b_[0] - a_[0]) / d_, (b_[1] - a_[1]) / d_))
    # a station the OSM line puts on the dry side of a surveyed bank (whose water side the other bank showed) is moved
    # across it, 3 m into the water: the OSM line is metres off in places, the survey is not
    gB_ = Grid(15.0)
    for pts_, tans_, side_ in getattr(S, "bank_sides", []):
        for p_, t_ in zip(pts_, tans_):
            gB_.add((p_, t_, side_), (p_[0], p_[1], p_[0], p_[1]))
    moved = 0
    for i in range(N):
        q = Q[i]
        near_ = [(math.hypot(p_[0] - q[0], p_[1] - q[1]), p_, t_, sd_) for p_, t_, sd_ in
                 gB_.query((q[0] - 20, q[1] - 20, q[0] + 20, q[1] + 20))]
        if not near_:
            continue
        d_, p_, t_, sd_ = min(near_, key=lambda z: z[0])
        own = 1 if (t_[0] * (q[1] - p_[1]) - t_[1] * (q[0] - p_[0])) > 0 else -1
        if own != sd_ and d_ <= 20.0 and not in_building(q[0], q[1]):
            Q[i] = (p_[0] - sd_ * t_[1] * 3.0, p_[1] + sd_ * t_[0] * 3.0)
            moved += 1
    S.stats["river_stations_moved"] = moved
    # the directions again, from the centres as moved and over 4 stations each way (12 m): a centre line that wanders
    # by a metre or two no longer fans the cuts across the channel (a fan leaves wedges of dry ground in the water)
    T = []
    for i in range(N):
        lo_, hi_ = max(0, i - 4), min(N - 1, i + 4)
        while lo_ > 0 and math.hypot(Q[hi_][0] - Q[lo_][0], Q[hi_][1] - Q[lo_][1]) < 1.0:
            lo_ -= 1
        while hi_ < N - 1 and math.hypot(Q[hi_][0] - Q[lo_][0], Q[hi_][1] - Q[lo_][1]) < 1.0:
            hi_ += 1
        a_, b_ = Q[lo_], Q[hi_]
        d_ = math.hypot(b_[0] - a_[0], b_[1] - a_[1])
        if d_ < 1e-9:
            a_, b_ = stations[max(0, i - 1)][0], stations[min(N - 1, i + 1)][0]
            d_ = math.hypot(b_[0] - a_[0], b_[1] - a_[1]) or 1.0
        T.append(((b_[0] - a_[0]) / d_, (b_[1] - a_[1]) / d_))
    # the surveyed bridges (pairs of YOL_KOPRU lines): the river runs on under them, they never cover it
    bsegs0 = [((s_[0], s_[1]), (s_[2], s_[3])) for lay in DWG["bridges"] for s_ in R["lines"].get(lay, [])
              if bb_hit((min(s_[0], s_[2]), min(s_[1], s_[3]), max(s_[0], s_[2]), max(s_[1], s_[3])), bbx)]
    bgroups = []
    for sgm in bsegs0:
        near_ = [gp for gp in bgroups if any(min(math.hypot(a[0] - c[0], a[1] - c[1]) for a in sgm for c in o) < 14.0
                                              for o in gp)]
        if near_:
            merged = [sgm]
            for gp in near_:
                merged += gp
                bgroups.remove(gp)
            bgroups.append(merged)
        else:
            bgroups.append([sgm])
    bridge_hulls = [H_ for H_ in (hull([pt for sgm in gp for pt in sgm]) for gp in bgroups if len(gp) >= 2) if len(H_) >= 3]

    def on_bridge(q):
        return any(pip(q[0], q[1], H_) for H_ in bridge_hulls)
    # pass 2 - measure from the smooth centre line. Each bank keeps one edge layer along a stretch (the most common
    #          one around it, priority breaking ties) and short breaks in that layer are bridged, not jumped.
    gPair = Grid(30.0)
    for P in pair_pieces:
        gPair.add(P, bb_pts(P))

    def in_pair(x, y):
        return any(pip(x, y, P) for P in gPair.query((x, y, x, y)))
    names_ = [nm for nm, _, _ in PRIORITY]
    D = {+1: [], -1: []}
    state = []
    for q, t in zip(Q, T):
        n_ = (-t[1], t[0])
        for sg in (+1, -1):
            D[sg].append([hit(g_, q, (n_[0] * sg, n_[1] * sg), maxd) for nm, g_, maxd in PRIORITY])
        if in_building(q[0], q[1]):
            state.append("covered")
        elif in_pair(q[0], q[1]):
            state.append("pair")
        elif in_tunnel(q) and not on_bridge(q):
            state.append("covered")
        else:
            state.append("open" if any(v_ is not None for v_ in D[+1][-1] + D[-1][-1]) else "unknown")

    def stable(sg):
        first = [next((li for li, v_ in enumerate(D[sg][k]) if v_ is not None), None) for k in range(N)]
        vals, kinds = [], []
        for k in range(N):
            win = [first[j] for j in range(max(0, k - 5), min(N, k + 6)) if first[j] is not None]
            if not win:
                vals.append(None)
                kinds.append(None)
                continue
            stream_near = [D[sg][j][0] for j in range(max(0, k - 5), min(N, k + 6)) if D[sg][j][0] is not None]
            li = 0 if stream_near else max(set(win), key=lambda x: (win.count(x), -x))   # stream lines always win
            v_ = D[sg][k][li]
            if v_ is None:
                nb = [D[sg][j][li] for j in range(max(0, k - 8), min(N, k + 9)) if D[sg][j][li] is not None]
                v_ = sorted(nb)[len(nb) // 2] if nb else (D[sg][k][first[k]] if first[k] is not None else None)
                lo_ = any(D[sg][j][li] is not None for j in range(max(0, k - 8), k))
                hi_ = any(D[sg][j][li] is not None for j in range(k + 1, min(N, k + 9)))
                if nb and not (lo_ and hi_) and first[k] is not None and D[sg][k][first[k]] <= v_ + 8.0:
                    v_ = D[sg][k][first[k]]
            vals.append(v_)
            kinds.append(names_[li])
        return vals, kinds
    A, KA = stable(+1)
    Bv, KB = stable(-1)
    found = sorted([v_ for v_ in A + Bv if v_ is not None])
    half = found[len(found) // 2] if found else 8.0

    def repair(vals, other):
        out_ = list(vals)
        for i in range(N):
            if state[i] == "covered" or out_[i] is not None:
                continue
            nb = [vals[k] for k in range(max(0, i - 8), min(N, i + 9)) if vals[k] is not None and state[k] != "covered"]
            if nb:
                out_[i] = sorted(nb)[len(nb) // 2]
            elif other[i] is not None:
                out_[i] = min(other[i], half)
        return out_
    A2, B2 = repair(A, Bv), repair(Bv, A)
    S.stats["river_states_before_bridging"] = dict((k_, state.count(k_)) for k_ in set(state))
    S.stats["open_missing_side"] = sum(1 for k_ in range(N) if state[k_] == "open" and (A2[k_] is None or B2[k_] is None))
    i = 0
    while i < N:                                         # bridge short stretches with no edge at all (<= 45 m)
        if state[i] == "unknown" or (state[i] == "open" and (A2[i] is None or B2[i] is None)):
            j = i
            while j < N and (state[j] == "unknown" or (state[j] == "open" and (A2[j] is None or B2[j] is None))):
                j += 1
            ok_lo = i > 0 and state[i - 1] == "open" and A2[i - 1] is not None and B2[i - 1] is not None
            ok_hi = j < N and state[j] == "open" and A2[j] is not None and B2[j] is not None
            for k in range(i, j):
                if ok_lo and ok_hi and (j - i) <= 15:
                    f = (k - i + 1) / float(j - i + 1)
                    A2[k] = A2[i - 1] + (A2[j] - A2[i - 1]) * f
                    B2[k] = B2[i - 1] + (B2[j] - B2[i - 1]) * f
                    state[k] = "open"
                    KA[k] = KB[k] = "bridged"
                else:
                    state[k] = "none"
            i = j
        else:
            i += 1

    def tidy(vals, kinds=None, sg=1):
        """Per stretch of consecutive open stations (stretches apart do not influence each other): isolated spikes
        through gaps go (median of 11), and the bank may only drift gradually (1.2 m per station) - except on a
        surveyed stream line, which keeps its measured distance unless that is a spike (3 m off the median). The
        filters work on where the bank is across the mean of 11 centres, so a centre that wanders by a metre or two
        does not make a straight wall look like a row of spikes."""
        out_ = list(vals)
        k = 0
        while k < N:
            if state[k] != "open":
                k += 1
                continue
            j = k
            while j < N and state[j] == "open":
                j += 1
            idx = list(range(k, j))
            sh = []
            for q in idx:
                win = idx[max(0, q - k - 5):q - k + 6]
                mx = sum(Q[w][0] for w in win) / float(len(win))
                my = sum(Q[w][1] for w in win) / float(len(win))
                sh.append((Q[q][0] - mx) * (-T[q][1] * sg) + (Q[q][1] - my) * (T[q][0] * sg))
            raw = [vals[q] + s_ for q, s_ in zip(idx, sh)]
            seq = median_filter(raw, 5)
            line = [kinds is not None and kinds[q] == "stream lines" for q in idx]
            for q in range(len(seq)):
                if line[q] and abs(raw[q] - seq[q]) <= 3.0:
                    seq[q] = raw[q]
            for q in range(1, len(seq)):
                if not line[q]:
                    seq[q] = min(seq[q], seq[q - 1] + 1.2)
            for q in range(len(seq) - 2, -1, -1):
                if not line[q]:
                    seq[q] = min(seq[q], seq[q + 1] + 1.2)
            seq = [v_ - s_ for v_, s_ in zip(seq, sh)]
            for q, v_ in zip(idx, seq):
                out_[q] = max(1.0, min(v_, RIVER_FAR if q in far_k else 30.0))
            k = j
        return out_
    # a surveyed kerb nearer than the bank found is the bank: the water never runs on over a street. Kerbs on a bridge
    # or within 3 m of one are left out (the river runs on under it, the street onto it is no bank), and only kerbs
    # running with the stream count (within 40 degrees of it): a street crossing the stream is not its bank.
    hull_bb = [(bb_pts(H_), H_) for H_ in bridge_hulls]

    def near_bridge(p, d):
        for bb_, H_ in hull_bb:
            if bb_[0] - d <= p[0] <= bb_[2] + d and bb_[1] - d <= p[1] <= bb_[3] + d and (
                    pip(p[0], p[1], H_) or pl_dist(p[0], p[1], H_, True) < d):
                return True
        return False
    g_kerb = Grid(10.0)
    for lay in DWG["roads"]:
        for s_ in R["lines"].get(lay, []):
            a_, b_ = (s_[0], s_[1]), (s_[2], s_[3])
            m_ = ((s_[0] + s_[2]) / 2.0, (s_[1] + s_[3]) / 2.0)
            sb = (min(s_[0], s_[2]), min(s_[1], s_[3]), max(s_[0], s_[2]), max(s_[1], s_[3]))
            if bb_hit(sb, bbx) and not (near_bridge(m_, 3.0) or near_bridge(a_, 3.0) or near_bridge(b_, 3.0)):
                g_kerb.add((a_, b_), sb)

    # v16.7: a wide dry bed. Where neither side has an edge within the usual 25-30 m for more than 45 m of river (east
    # of the Fabrika Caddesi bend up to and past the Ilıca junction bridge, where the bed is 40-70 m wide), v16.6
    # drew no water at all and the bed looked empty. Those stations now follow the bed out to RIVER_FAR: the nearest
    # slope toe, wall, building front or street edge on each side that runs with the stream (within 40 degrees of
    # it, so a street crossing the river is never its bank; streets on or within 3 m of a surveyed bridge are left
    # out). A side that already had a near edge keeps it. Stations upstream that had edges are not changed.
    far_grids = [g_ for nm, g_, md in PRIORITY[1:]] + [g_kerb]

    def far_hit(p, d, t, maxd=RIVER_FAR):
        q = (p[0] + d[0] * maxd, p[1] + d[1] * maxd)
        best = None
        for g_ in far_grids:
            for a_, b_ in g_.query((min(p[0], q[0]), min(p[1], q[1]), max(p[0], q[0]), max(p[1], q[1]))):
                sx, sy = b_[0] - a_[0], b_[1] - a_[1]
                sl = math.hypot(sx, sy)
                if sl < 1e-9 or abs(sx * t[0] + sy * t[1]) / sl < 0.766:
                    continue
                r = seg_x(p, (q[0] - p[0], q[1] - p[1]), a_, (sx, sy))
                if r and r[0] * maxd > 0.3 and (best is None or r[0] * maxd < best):
                    best = r[0] * maxd
        return best
    far_k = set()
    for k in range(N):
        if state[k] != "none" or in_building(Q[k][0], Q[k][1]):
            continue
        t = T[k]
        n_ = (-t[1], t[0])
        a_ = A[k] if A[k] is not None else far_hit(Q[k], n_, t)
        b_ = Bv[k] if Bv[k] is not None else far_hit(Q[k], (-n_[0], -n_[1]), t)
        if a_ is not None and b_ is not None:
            if A[k] is None:
                KA[k] = "far edge (wide bed)"
            if Bv[k] is None:
                KB[k] = "far edge (wide bed)"
            A2[k], B2[k], state[k] = a_, b_, "open"
            far_k.add(k)
    i = 0                                                # short breaks inside the wide bed (a street crossing it on
    while i < N:                                         # a bridge hides its edges): carried across, <= 45 m
        if state[i] == "none":
            j = i
            while j < N and state[j] == "none":
                j += 1
            if 0 < i and j < N and (i - 1 in far_k or j in far_k) and state[i - 1] == "open" and state[j] == "open" \
                    and j - i <= 15:
                for k in range(i, j):
                    f = (k - i + 1) / float(j - i + 1)
                    A2[k] = A2[i - 1] + (A2[j] - A2[i - 1]) * f
                    B2[k] = B2[i - 1] + (B2[j] - B2[i - 1]) * f
                    state[k] = "open"
                    KA[k] = KB[k] = "bridged"
                    far_k.add(k)
            i = j
        else:
            i += 1
    S.stats["river_far_stations"] = len(far_k)
    A2, B2 = tidy(A2, KA, 1), tidy(B2, KB, -1)

    def kerb_hit(p, d, maxd, t):
        q = (p[0] + d[0] * maxd, p[1] + d[1] * maxd)
        best = None
        for a_, b_ in g_kerb.query((min(p[0], q[0]), min(p[1], q[1]), max(p[0], q[0]), max(p[1], q[1]))):
            sx, sy = b_[0] - a_[0], b_[1] - a_[1]
            sl = math.hypot(sx, sy)
            if sl < 1e-9 or abs(sx * t[0] + sy * t[1]) / sl < 0.766:
                continue
            r = seg_x(p, (q[0] - p[0], q[1] - p[1]), a_, (sx, sy))
            if r and r[0] * maxd > 0.3 and (best is None or r[0] * maxd < best):
                best = r[0] * maxd
        return best
    kerbed = 0
    for k in range(N):
        if state[k] != "open":
            continue
        q, t = Q[k], T[k]
        n_ = (-t[1], t[0])
        for sg, arr in ((+1, A2), (-1, B2)):
            if arr[k] is None:
                continue
            h = kerb_hit(q, (n_[0] * sg, n_[1] * sg), arr[k], t)
            if h is not None and h >= 1.0 and h < arr[k] - 0.3:
                arr[k] = h
                kerbed += 1
    if kerbed:
        A2, B2 = tidy(A2, KA, 1), tidy(B2, KB, -1)
    S.stats["river_kerb_stops"] = kerbed
    S.stats["river_states"] = dict((k_, state.count(k_)) for k_ in set(state))
    S.stats["river_edges"] = {}
    for k in range(N):
        if state[k] == "open":
            for kname in (KA[k] or "neighbours", KB[k] or "neighbours"):
                S.stats["river_edges"][kname] = S.stats["river_edges"].get(kname, 0) + 1
    st = []
    for k in range(N):
        q, t = Q[k], T[k]
        if state[k] in ("open", "pair"):
            st.append([q[0], q[1], t[0], t[1], A2[k], B2[k], state[k]])
        else:
            st.append([q[0], q[1], t[0], t[1], None, None, state[k]])
    def capped(vals):
        out_ = list(vals)
        for k in range(N):
            if st[k][6] != "pair" or vals[k] is None:
                continue
            win = sorted(vals[j] for j in range(max(0, k - 5), min(N, k + 6))
                         if vals[j] is not None and st[j][6] in ("open", "pair"))
            out_[k] = min(vals[k], win[len(win) // 2] + 2.0)
        return out_
    ca_, cb_ = capped([r[4] for r in st]), capped([r[5] for r in st])
    for k in range(N):
        st[k][4], st[k][5] = ca_[k], cb_[k]
    S.river_st = st
    idx_runs, cur = [], []
    for k in range(N):
        if st[k][6] == "open" or (st[k][6] == "pair" and st[k][4] is not None and st[k][5] is not None):
            cur.append(k)
        else:
            if cur:
                idx_runs.append(cur)
            cur = []
    if cur:
        idx_runs.append(cur)
    runs = []
    def paired(k_):
        return st[k_][6] == "pair" and st[k_][4] is not None and st[k_][5] is not None
    for r_ in idx_runs:                                  # overlap into the paired channel (up to 8 stations): no seam
        pre, post = [], []
        while len(pre) < 8 and r_[0] - len(pre) - 1 >= 0 and paired(r_[0] - len(pre) - 1):
            pre.insert(0, r_[0] - len(pre) - 1)
        while len(post) < 8 and r_[-1] + len(post) + 1 < N and paired(r_[-1] + len(post) + 1):
            post.append(r_[-1] + len(post) + 1)
        r_ = pre + r_ + post
        if len(r_) >= 2:
            runs.append([st[k] for k in r_])
    cov, ccur = [], []
    for row in st + [None]:
        if row is not None and row[6] == "covered":
            ccur.append(row)
        else:
            if len(ccur) >= 2:
                cov.append(ccur)
            ccur = []
    for c_ in cov:
        S.covered += F.clip_line([(r[0], r[1]) for r in c_])
    for P in pair_pieces:                                # the channel between the two stream lines
        S.water.append(dict(P=P, A=0.5 * shoelace(P)[0], bb=bb_pts(P), src="pair"))
    S.water_outline += [P for P in pair_chains]
    S.stats["river_edges"]["stream lines (both banks)"] = 2 * sum(1 for x in state if x == "pair")
    def simple(P):
        n = len(P)
        for i in range(n):
            a, b = P[i], P[(i + 1) % n]
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue
                c, d = P[j], P[(j + 1) % n]
                r = seg_x(a, (b[0] - a[0], b[1] - a[1]), c, (d[0] - c[0], d[1] - c[1]))
                if r and 1e-6 < r[0] < 1 - 1e-6 and 1e-6 < r[1] < 1 - 1e-6:
                    return False
        return True
    for run in runs:
        left = [(r[0] - r[3] * r[4], r[1] + r[2] * r[4]) for r in run]
        right = [(r[0] + r[3] * r[5], r[1] - r[2] * r[5]) for r in run]
        k = 0
        while k < len(run) - 1:                          # merge slices into larger clean pieces (no seams)
            m = min(12, len(run) - 1 - k)
            while m > 1:
                P = left[k:k + m + 1] + list(reversed(right[k:k + m + 1]))
                if simple(P):
                    break
                m //= 2
            P = left[k:k + m + 1] + list(reversed(right[k:k + m + 1]))
            if m == 1 and not simple(P):
                H_ = hull(P)
                if len(H_) >= 3:
                    P = H_
            cp = F.clip_poly(P)
            if cp:
                S.water.append(dict(P=cp, A=shoelace(cp)[0], bb=bb_pts(cp), src="axis"))
            k += m
        S.water_outline += F.clip_line(left) + F.clip_line(right)
    dry = []
    for pts, tans, side in getattr(S, "bank_sides", []):
        if len(pts) < 2:
            continue
        inner = [(p[0] + side * t_[1] * 0.6, p[1] - side * t_[0] * 0.6) for p, t_ in zip(pts, tans)]
        outer = [(p[0] + side * t_[1] * RIVER_DRY, p[1] - side * t_[0] * RIVER_DRY) for p, t_ in zip(pts, tans)]
        dry.append(inner + list(reversed(outer)))
    S.river_cut = dict(bld=[P for u in S.bld for P in u["parts"]], dry=dry)
    S.stats["river_tunnel_ways"] = n_tun
    river_union(S)
    # ---- bridge decks: each pair of surveyed bridge lines, drawn over the water
    bsegs = [((s[0], s[1]), (s[2], s[3])) for lay in DWG["bridges"] for s in R["lines"].get(lay, [])
             if bb_hit((min(s[0], s[2]), min(s[1], s[3]), max(s[0], s[2]), max(s[1], s[3])), bbx)]
    groups = []
    for sgm in bsegs:
        near = [gp for gp in groups if any(min(math.hypot(a[0] - c[0], a[1] - c[1]) for a in sgm for c in o) < 14.0
                                               for o in gp)]
        if near:
            merged = [sgm]
            for gp in near:
                merged += gp
                groups.remove(gp)
            groups.append(merged)
        else:
            groups.append([sgm])
    for gp in groups:
        if len(gp) < 2:
            continue
        H = hull([pt for sgm in gp for pt in sgm])
        if len(H) >= 3:
            a_, cx_, cy_ = shoelace(H)
            probe = [(cx_, cy_)] + H + [((H[k][0] + H[(k + 1) % len(H)][0]) / 2.0, (H[k][1] + H[(k + 1) % len(H)][1]) / 2.0)
                                        for k in range(len(H))]
            if any(water_at(S, x_, y_) for x_, y_ in probe):  # a deck only where the bridge really spans water
                cp = F.clip_poly(H)
                if cp:
                    S.decks.append(cp)
    S.selinus = F.clip_line(cl)
    S.g_water = Grid(30.0)
    for w in S.water:
        S.g_water.add(w, w["bb"])
    if S.selinus:
        main = max(S.selinus, key=pl_length)
        p, t = pl_point_at(main, pl_length(main) * 0.5)
        S.river_label = (p[0], p[1], t, tr_upper(sname or "Selinos Çayı"))


