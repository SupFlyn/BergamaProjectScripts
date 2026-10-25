exec(compile(NOISE_KERNEL, "selinus_noise_kernel", "exec"), globals())


def region_contains(x, y, Ps, Hs):
    if not any(pip(x, y, P) for P in Ps):
        return False
    return not any(pip(x, y, H) for H in Hs)


def bb_pts(P):
    xs = [p[0] for p in P]
    ys = [p[1] for p in P]
    return (min(xs), min(ys), max(xs), max(ys))


def bb_union(bs):
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))


def bb_hit(a, b, pad=0.0):
    return not (a[2] + pad < b[0] or b[2] + pad < a[0] or a[3] + pad < b[1] or b[3] + pad < a[1])


def seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    l2 = dx * dx + dy * dy
    if l2 < 1e-12:
        return math.hypot(px - ax, py - ay)
    t = ((px - ax) * dx + (py - ay) * dy) / l2
    t = 0.0 if t < 0.0 else (1.0 if t > 1.0 else t)
    return math.hypot(px - ax - t * dx, py - ay - t * dy)


def pl_dist(px, py, P, closed):
    n = len(P)
    if n == 0:
        return 1e18
    if n == 1:
        return math.hypot(px - P[0][0], py - P[0][1])
    m = n if closed else n - 1
    best = 1e18
    for i in range(m):
        a = P[i]
        b = P[(i + 1) % n]
        d = seg_dist(px, py, a[0], a[1], b[0], b[1])
        if d < best:
            best = d
    return best


def seg_x(p, r, q, s):
    rxs = r[0] * s[1] - r[1] * s[0]
    if abs(rxs) < 1e-12:
        return None
    qx, qy = q[0] - p[0], q[1] - p[1]
    t = (qx * s[1] - qy * s[0]) / rxs
    u = (qx * r[1] - qy * r[0]) / rxs
    if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
        return t, u
    return None


def pl_length(P):
    return sum(math.hypot(P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1]) for i in range(len(P) - 1))


def pl_point_at(P, s):
    acc = 0.0
    for i in range(len(P) - 1):
        a, b = P[i], P[i + 1]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if acc + L >= s and L > 0:
            t = (s - acc) / L
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        acc += L
    a, b = P[-2], P[-1]
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    return P[-1], ((b[0] - a[0]) / L, (b[1] - a[1]) / L)


def resample(P, sp):
    out = [P[0]]
    carry = 0.0
    for i in range(len(P) - 1):
        ax, ay = P[i]
        bx, by = P[i + 1]
        seg = math.hypot(bx - ax, by - ay)
        if seg < 1e-9:
            continue
        d = sp - carry
        while d <= seg:
            t = d / seg
            out.append((ax + (bx - ax) * t, ay + (by - ay) * t))
            d += sp
        carry = seg - (d - sp)
    return out


def hull(pts):
    pts = sorted(set(pts))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def nice_floor(v):
    if v <= 0:
        return 1.0
    e = 10.0 ** math.floor(math.log10(v))
    for m in (5.0, 2.5, 2.0, 1.0):
        if m * e <= v:
            return m * e
    return e


def num(v):
    if v is None:
        return None
    try:
        s = str(v).lower().replace("m", "").replace(",", ".").strip()
        return float(s.split(";")[0].split(" ")[0])
    except ValueError:
        return None


def join_names(names):
    names = [n for n in names if n]
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " and " + names[-1]


def circle_pts(x, y, r, n=20):
    return [(x + r * math.cos(2 * math.pi * k / n), y + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def ellipse_pts(x, y, rx, ry, n=22):
    return [(x + rx * math.cos(2 * math.pi * k / n), y + ry * math.sin(2 * math.pi * k / n)) for k in range(n)]


#@include ../../common/rect.py


def annulus(cx, cy, r0, r1, a0, a1):
    n = max(2, int(abs(a1 - a0) / math.radians(2.0)) + 1)
    pts = [(cx + r1 * math.cos(a0 + (a1 - a0) * k / n), cy + r1 * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)]
    pts += [(cx + r0 * math.cos(a1 + (a0 - a1) * k / n), cy + r0 * math.sin(a1 + (a0 - a1) * k / n)) for k in range(n + 1)]
    return pts


def dashes(P, dash, gap):
    out = []
    L = pl_length(P)
    s = 0.0
    while s < L - 1e-9 and len(out) < 3000:
        e = min(L, s + dash)
        seg = [pl_point_at(P, s)[0]]
        acc = 0.0
        for i in range(len(P) - 1):
            l = math.hypot(P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1])
            if s < acc + l < e:
                seg.append(P[i + 1])
            acc += l
        seg.append(pl_point_at(P, e)[0])
        out.append(seg)
        s += dash + gap
    return out


def make_runs(seq, idx):
    runs = []
    cur, val = [], None
    for s in seq:
        if s is None:
            if len(cur) >= 2:
                runs.append((val, cur))
            cur, val = [], None
            continue
        p = (s[0], s[1])
        if not cur:
            cur, val = [p], s[idx]
        elif s[idx] == val:
            cur.append(p)
        else:
            cur.append(p)
            if len(cur) >= 2:
                runs.append((val, cur))
            cur, val = [p], s[idx]
    if len(cur) >= 2:
        runs.append((val, cur))
    return runs


class Grid(object):
    def __init__(self, cell):
        self.c = float(cell)
        self.d = {}

    def _keys(self, bb):
        c = self.c
        for i in range(int(math.floor(bb[0] / c)), int(math.floor(bb[2] / c)) + 1):
            for j in range(int(math.floor(bb[1] / c)), int(math.floor(bb[3] / c)) + 1):
                yield (i, j)

    def add(self, item, bb):
        for k in self._keys(bb):
            self.d.setdefault(k, []).append(item)

    def query(self, bb):
        """Items whose cells meet the box, each once, in the same order as always (cells column by column)."""
        c = self.c
        floor = math.floor
        i0, i1 = int(floor(bb[0] / c)), int(floor(bb[2] / c))
        j0, j1 = int(floor(bb[1] / c)), int(floor(bb[3] / c))
        get = self.d.get
        seen = set()
        add = seen.add
        out = []
        app = out.append
        for i in range(i0, i1 + 1):
            for j in range(j0, j1 + 1):
                lst = get((i, j))
                if lst:
                    for it in lst:
                        k = id(it)
                        if k not in seen:
                            add(k)
                            app(it)
        return out


# ---------------------------------------------------------------- convex clipping (frame)
class Frame(object):
    """Convex map frame with a local axis (u along the corridor, v across)."""

    def __init__(self, P):
        a, cx, cy = shoelace(P)
        if self._signed(P) < 0:
            P = list(reversed(P))
        self.P = P
        self.bb = bb_pts(P)
        self.area = a
        best, ang = -1.0, 0.0
        for i in range(len(P)):
            q0, q1 = P[i], P[(i + 1) % len(P)]
            L = math.hypot(q1[0] - q0[0], q1[1] - q0[1])
            if L > best:
                best, ang = L, math.atan2(q1[1] - q0[1], q1[0] - q0[0])
        while ang > math.pi / 2:
            ang -= math.pi
        while ang <= -math.pi / 2:
            ang += math.pi
        self.ang = ang
        self._lc, self._ls = math.cos(-ang), math.sin(-ang)          # rotation terms, computed once (same values)
        self._wc, self._ws = math.cos(ang), math.sin(ang)
        self.cx, self.cy = cx, cy
        L = [self.local(x, y) for x, y in P]
        self.u0, self.v0 = min(p[0] for p in L), min(p[1] for p in L)
        self.u1, self.v1 = max(p[0] for p in L), max(p[1] for p in L)
        self.w, self.h = self.u1 - self.u0, self.v1 - self.v0

    @staticmethod
    def _signed(P):
        return sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))

    def local(self, x, y):
        c, s = self._lc, self._ls
        dx, dy = x - self.cx, y - self.cy
        return (c * dx - s * dy, s * dx + c * dy)

    def world(self, u, v):
        c, s = self._wc, self._ws
        return (self.cx + c * u - s * v, self.cy + s * u + c * v)

    def inside(self, x, y):
        return pip(x, y, self.P)

    def clip_poly(self, P):
        if not P or not bb_hit(bb_pts(P), self.bb):
            return []
        out = list(P)
        n = len(self.P)
        for i in range(n):
            if not out:
                break
            a, b = self.P[i], self.P[(i + 1) % n]
            ex, ey = b[0] - a[0], b[1] - a[1]
            res = []
            m = len(out)
            for k in range(m):
                p, q = out[k], out[(k + 1) % m]
                dp = ex * (p[1] - a[1]) - ey * (p[0] - a[0])
                dq = ex * (q[1] - a[1]) - ey * (q[0] - a[0])
                if dp >= 0:
                    res.append(p)
                if (dp >= 0) != (dq >= 0):
                    t = dp / (dp - dq)
                    res.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
            out = res
        return out if len(out) >= 3 and shoelace(out)[0] > 0.01 else []

    def clip_line(self, P):
        if len(P) < 2 or not bb_hit(bb_pts(P), self.bb):
            return []
        runs, cur = [], []
        n = len(self.P)
        for k in range(len(P) - 1):
            p0, p1 = P[k], P[k + 1]
            t0, t1 = 0.0, 1.0
            dx, dy = p1[0] - p0[0], p1[1] - p0[1]
            ok = True
            for i in range(n):
                a, b = self.P[i], self.P[(i + 1) % n]
                ex, ey = b[0] - a[0], b[1] - a[1]
                num_ = ex * (p0[1] - a[1]) - ey * (p0[0] - a[0])
                den = ex * dy - ey * dx
                if abs(den) < 1e-12:
                    if num_ < 0:
                        ok = False
                        break
                    continue
                t = -num_ / den
                if den > 0:
                    t0 = max(t0, t)
                else:
                    t1 = min(t1, t)
                if t0 > t1:
                    ok = False
                    break
            if not ok:
                if len(cur) >= 2:
                    runs.append(cur)
                cur = []
                continue
            a_ = (p0[0] + dx * t0, p0[1] + dy * t0)
            b_ = (p0[0] + dx * t1, p0[1] + dy * t1)
            if cur and abs(cur[-1][0] - a_[0]) < 1e-9 and abs(cur[-1][1] - a_[1]) < 1e-9:
                cur.append(b_)
            else:
                if len(cur) >= 2:
                    runs.append(cur)
                cur = [a_, b_]
            if t1 < 1.0:
                runs.append(cur)
                cur = []
        if len(cur) >= 2:
            runs.append(cur)
        return runs


# ============================================================ POLYGONIZER (CAD line work -> faces)
def _sx(ax, ay, bx, by, cx, cy, dx, dy):
    rx, ry, sx, sy = bx - ax, by - ay, dx - cx, dy - cy
    den = rx * sy - ry * sx
    if abs(den) < 1e-12:
        return None
    qx, qy = cx - ax, cy - ay
    t = (qx * sy - qy * sx) / den
    u = (qx * ry - qy * rx) / den
    if -1e-9 <= t <= 1 + 1e-9 and -1e-9 <= u <= 1 + 1e-9:
        return t, u
    return None


def _seg_grid(segs, C):
    sg = {}
    for i, s in enumerate(segs):
        for a in range(int(math.floor(min(s[0], s[2]) / C)), int(math.floor(max(s[0], s[2]) / C)) + 1):
            for b in range(int(math.floor(min(s[1], s[3]) / C)), int(math.floor(max(s[1], s[3]) / C)) + 1):
                sg.setdefault((a, b), []).append(i)
    return sg


def polygonize(segs, tol=0.05, gap=0.35, extend=0.0, extend_tags=None, holes=False):
    """segs [(x1,y1,x2,y2,tag)] -> bounded faces [dict(P=ccw pts, A=area, tags={tag:length})]. holes=True: an
    outline standing free inside a face (a courtyard ring, a building inside a walled compound) is a hole of the
    smallest face around it: listed in its H, its area taken off A."""
    segs = [list(s) for s in segs if abs(s[0] - s[2]) + abs(s[1] - s[3]) > 1e-9]
    C = 4.0
    # 1. close small gaps at dangling ends
    sg = _seg_grid(segs, C)
    ends = {}
    for i, s in enumerate(segs):
        for (x, y) in ((s[0], s[1]), (s[2], s[3])):
            ends.setdefault((round(x / tol), round(y / tol)), []).append(i)

    def n_ends(x, y):
        kx, ky = round(x / tol), round(y / tol)
        return sum(len(ends.get((a, b), ())) for a in (kx - 1, kx, kx + 1) for b in (ky - 1, ky, ky + 1))
    for i, s in enumerate(segs):
        for k in (0, 1):
            x, y = (s[0], s[1]) if k == 0 else (s[2], s[3])
            if n_ends(x, y) > 1:
                continue
            ox, oy = (s[2], s[3]) if k == 0 else (s[0], s[1])
            Ls = math.hypot(x - ox, y - oy)
            if Ls < 1e-9:
                continue
            ux, uy = (x - ox) / Ls, (y - oy) / Ls
            best = None
            a0, b0 = int(math.floor(x / C)), int(math.floor(y / C))
            for a in (a0 - 1, a0, a0 + 1):
                for b in (b0 - 1, b0, b0 + 1):
                    for j in sg.get((a, b), ()):
                        if j == i:
                            continue
                        t = segs[j]
                        r = _sx(x, y, x + ux * gap, y + uy * gap, t[0], t[1], t[2], t[3])
                        if r is not None and (best is None or r[0] * gap < best[0]):
                            best = (r[0] * gap, x + ux * r[0] * gap, y + uy * r[0] * gap)
                        ex, ey = t[2] - t[0], t[3] - t[1]
                        l2 = ex * ex + ey * ey
                        if l2 > 1e-12:
                            q = max(0.0, min(1.0, ((x - t[0]) * ex + (y - t[1]) * ey) / l2))
                            px, py = t[0] + q * ex, t[1] + q * ey
                            d = math.hypot(px - x, py - y)
                            if d <= gap * 0.5 and (best is None or d < best[0]):
                                best = (d, px, py)
            if best is not None and best[0] > 1e-9:
                if k == 0:
                    s[0], s[1] = best[1], best[2]
                else:
                    s[2], s[3] = best[1], best[2]
    # 1b. extend short dangling ticks (party walls) across the face
    if extend > 0.0:
        sg = _seg_grid(segs, C)
        ends = {}
        for i, s in enumerate(segs):
            for (x, y) in ((s[0], s[1]), (s[2], s[3])):
                ends.setdefault((round(x / tol), round(y / tol)), []).append(i)

        def touches(x, y, me):
            kx, ky = round(x / tol), round(y / tol)
            for a in (kx - 1, kx, kx + 1):
                for b in (ky - 1, ky, ky + 1):
                    for j in ends.get((a, b), ()):
                        if j != me:
                            return True
            a0, b0 = int(math.floor(x / C)), int(math.floor(y / C))
            for a in (a0 - 1, a0, a0 + 1):
                for b in (b0 - 1, b0, b0 + 1):
                    for j in sg.get((a, b), ()):
                        if j == me:
                            continue
                        t = segs[j]
                        ex, ey = t[2] - t[0], t[3] - t[1]
                        l2 = ex * ex + ey * ey
                        if l2 < 1e-12:
                            continue
                        q = ((x - t[0]) * ex + (y - t[1]) * ey) / l2
                        if -0.001 <= q <= 1.001:
                            px, py = t[0] + q * ex, t[1] + q * ey
                            if abs(px - x) <= tol and abs(py - y) <= tol:
                                return True
            return False
        new = []
        for i, s in enumerate(segs):
            if extend_tags is not None and s[4] not in extend_tags:
                continue
            Ls = math.hypot(s[2] - s[0], s[3] - s[1])
            if Ls < 1e-6 or Ls > 6.0:
                continue
            d0, d1 = touches(s[0], s[1], i), touches(s[2], s[3], i)
            if d0 == d1:
                continue
            if d0:
                x, y, ox, oy = s[2], s[3], s[0], s[1]
            else:
                x, y, ox, oy = s[0], s[1], s[2], s[3]
            ux, uy = (x - ox) / Ls, (y - oy) / Ls
            best = None
            for j, t in enumerate(segs):
                if j == i:
                    continue
                r = _sx(x, y, x + ux * extend, y + uy * extend, t[0], t[1], t[2], t[3])
                if r is not None and r[0] * extend > 1e-3 and (best is None or r[0] * extend < best):
                    best = r[0] * extend
            if best is not None:
                new.append([x, y, x + ux * best, y + uy * best, s[4]])
        segs = segs + new
    # 2. node intersections, T-junctions and collinear overlaps
    sg = _seg_grid(segs, C)
    cuts = [[0.0, 1.0] for _ in segs]
    seen = set()
    for lst in sg.values():
        for ii in range(len(lst)):
            i = lst[ii]
            s = segs[i]
            for jj in range(ii + 1, len(lst)):
                j = lst[jj]
                key = (i, j) if i < j else (j, i)
                if key in seen:
                    continue
                seen.add(key)
                t = segs[j]
                r = _sx(s[0], s[1], s[2], s[3], t[0], t[1], t[2], t[3])
                if r is not None:
                    cuts[i].append(min(1.0, max(0.0, r[0])))
                    cuts[j].append(min(1.0, max(0.0, r[1])))
                else:
                    for (A, B, other) in ((s, i, t), (t, j, s)):
                        ex, ey = A[2] - A[0], A[3] - A[1]
                        l2 = ex * ex + ey * ey
                        if l2 < 1e-12:
                            continue
                        for (px, py) in ((other[0], other[1]), (other[2], other[3])):
                            q = ((px - A[0]) * ex + (py - A[1]) * ey) / l2
                            if 0.0 < q < 1.0:
                                qx, qy = A[0] + q * ex, A[1] + q * ey
                                if abs(qx - px) <= tol and abs(qy - py) <= tol:
                                    cuts[B].append(q)
    pieces = []
    for i, s in enumerate(segs):
        ts = sorted(set(round(t, 9) for t in cuts[i]))
        ex, ey = s[2] - s[0], s[3] - s[1]
        for k in range(len(ts) - 1):
            if ts[k + 1] - ts[k] > 1e-9:
                pieces.append((s[0] + ex * ts[k], s[1] + ey * ts[k], s[0] + ex * ts[k + 1], s[1] + ey * ts[k + 1], s[4]))
    # 3. snap vertices, dedupe edges
    cell = tol * 4.0
    grid, pts = {}, []

    def vid(x, y):
        k = (int(math.floor(x / cell)), int(math.floor(y / cell)))
        for a in (k[0] - 1, k[0], k[0] + 1):
            for b in (k[1] - 1, k[1], k[1] + 1):
                for v in grid.get((a, b), ()):
                    if abs(pts[v][0] - x) <= tol and abs(pts[v][1] - y) <= tol:
                        return v
        pts.append((x, y))
        grid.setdefault(k, []).append(len(pts) - 1)
        return len(pts) - 1
    und = {}
    for x1, y1, x2, y2, tag in pieces:
        a, b = vid(x1, y1), vid(x2, y2)
        if a != b:
            und.setdefault((a, b) if a < b else (b, a), set()).add(tag)
    # 4. prune dangles
    adj = {}
    for a, b in und:
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    stack = [v for v, n in adj.items() if len(n) < 2]
    while stack:
        v = stack.pop()
        nb = adj.get(v)
        if nb is None or len(nb) >= 2:
            continue
        for w in list(nb):
            adj[w].discard(v)
            if len(adj[w]) < 2:
                stack.append(w)
        del adj[v]
    order, pos = {}, {}
    for v, nb in adj.items():
        x, y = pts[v]
        order[v] = sorted(nb, key=lambda w: math.atan2(pts[w][1] - y, pts[w][0] - x))
        for i, w in enumerate(order[v]):
            pos[(v, w)] = i
    # 5. trace faces
    used = set()
    faces = []
    outers = []                                           # clockwise cycles: the outline of a connected group
    for v, lst in order.items():
        for w in lst:
            if (v, w) in used:
                continue
            cyc = []
            a, b = v, w
            while (a, b) not in used and len(cyc) < 50000:
                used.add((a, b))
                cyc.append(a)
                lb = order[b]
                c = lb[(pos[(b, a)] - 1) % len(lb)]
                a, b = b, c
            if len(cyc) < 3:
                continue
            P = [pts[k] for k in cyc]
            s2 = sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))
            if s2 > 1e-6:
                tags = {}
                ekeys, etags = [], []
                for i in range(len(cyc)):
                    k = (cyc[i], cyc[(i + 1) % len(cyc)])
                    kk = k if k[0] < k[1] else (k[1], k[0])
                    Ln = math.hypot(pts[k[1]][0] - pts[k[0]][0], pts[k[1]][1] - pts[k[0]][1])
                    tg_ = und.get(kk, set())
                    ekeys.append(kk)
                    etags.append(tg_)
                    for tg in tg_:
                        tags[tg] = tags.get(tg, 0.0) + Ln
                faces.append(dict(P=P, A=s2 / 2.0, tags=tags, E=ekeys, ET=etags, H=[]))
            elif s2 < -1e-6 and holes:
                outers.append((P, -s2 / 2.0))
    if holes and outers and faces:
        gf = {}
        CH = 40.0
        for i, f in enumerate(faces):
            bb = bb_pts(f["P"])
            f["_bb"] = bb
            f["_A0"] = f["A"]
            for gx in range(int(math.floor(bb[0] / CH)), int(math.floor(bb[2] / CH)) + 1):
                for gy in range(int(math.floor(bb[1] / CH)), int(math.floor(bb[3] / CH)) + 1):
                    gf.setdefault((gx, gy), []).append(i)
        for H, ah in outers:
            x, y = H[0]
            best = None
            for i in gf.get((int(math.floor(x / CH)), int(math.floor(y / CH))), ()):
                f = faces[i]
                bb = f["_bb"]
                if f["_A0"] > ah * (1.0 + 1e-6) + 1e-6 and bb[0] <= x <= bb[2] and bb[1] <= y <= bb[3] and pip(x, y, f["P"]):
                    if best is None or f["_A0"] < faces[best]["_A0"]:
                        best = i
            if best is not None:
                faces[best]["H"].append(list(reversed(H)) if signed_area(H) > 0 else H)
                faces[best]["A"] -= ah
        for f in faces:
            f.pop("_bb", None)
            f.pop("_A0", None)
    return faces


def drop_x(segs):
    """Remove X cross-marks (shed symbols): pairs of segments crossing near their middles."""
    g = {}
    for i, s in enumerate(segs):
        g.setdefault((int(((s[0] + s[2]) / 2) // 5.0), int(((s[1] + s[3]) / 2) // 5.0)), []).append(i)
    bad = set()
    for i, s in enumerate(segs):
        k = (int(((s[0] + s[2]) / 2) // 5.0), int(((s[1] + s[3]) / 2) // 5.0))
        for a in (k[0] - 1, k[0], k[0] + 1):
            for b in (k[1] - 1, k[1], k[1] + 1):
                for j in g.get((a, b), ()):
                    if j <= i:
                        continue
                    t = segs[j]
                    r = _sx(s[0], s[1], s[2], s[3], t[0], t[1], t[2], t[3])
                    if r and 0.2 < r[0] < 0.8 and 0.2 < r[1] < 0.8:
                        bad.add(i)
                        bad.add(j)
    return [s for i, s in enumerate(segs) if i not in bad]


def clip_half(P, px, py, nx, ny):
    out = []
    n = len(P)
    for i in range(n):
        a, b = P[i], P[(i + 1) % n]
        da = (a[0] - px) * nx + (a[1] - py) * ny
        db = (b[0] - px) * nx + (b[1] - py) * ny
        if da <= 0:
            out.append(a)
        if (da < 0 < db) or (db < 0 < da):
            t = da / (da - db)
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    return out


def voronoi_split(P, pts):
    cells = []
    for i, (x, y) in enumerate(pts):
        Cc = P
        for j, (u, v) in enumerate(pts):
            if i == j or not Cc:
                continue
            Cc = clip_half(Cc, (x + u) / 2.0, (y + v) / 2.0, u - x, v - y)
        cells.append(Cc if len(Cc) >= 3 else [])
    return cells


SPLIT_OWN = 150.0     # m2: a piece without a label at least this large is a building of its own (count from neighbours)


def split_face(P, labels, ticks):
    """Split a footprint holding several floor labels along its party-wall ticks. A piece without a label joins the
    labelled building it shares the longest wall with (pieces grow outwards from the labelled ones, so every building
    stays one contiguous outline); a piece of SPLIT_OWN m2 or more without a label is a building of its own whose
    floor count comes from its neighbours (label None)."""
    xs = [p[0] for p in P]
    ys = [p[1] for p in P]
    diag = math.hypot(max(xs) - min(xs), max(ys) - min(ys))
    segs = [(P[i][0], P[i][1], P[(i + 1) % len(P)][0], P[(i + 1) % len(P)][1], "B") for i in range(len(P))]
    segs += [(t[0], t[1], t[2], t[3], "T") for t in ticks]
    sub = polygonize(segs, extend=diag, extend_tags={"T"})
    sub = [f for f in sub if f["A"] > 0.05 and pip(interior_point(f["P"])[0], interior_point(f["P"])[1], P)]
    if not sub:
        sub = [dict(P=P, A=shoelace(P)[0], E=[])]
    lab_in = {}
    for li, (x, y, v) in enumerate(labels):
        for k, f in enumerate(sub):
            if pip(x, y, f["P"]):
                lab_in.setdefault(k, []).append(li)
                break
    units = {}
    owner = {}
    for k, f in enumerate(sub):
        Ls = lab_in.get(k, [])
        if len(Ls) == 1:
            units.setdefault(Ls[0], []).append(f["P"])
            owner[k] = Ls
        elif len(Ls) > 1:
            for i, cc in zip(Ls, voronoi_split(f["P"], [(labels[i][0], labels[i][1]) for i in Ls])):
                if cc:
                    units.setdefault(i, []).append(cc)
            owner[k] = Ls
    own = []
    for k, f in enumerate(sub):
        if k not in owner and f["A"] >= SPLIT_OWN:
            own.append(k)
            owner[k] = None
    # shared wall lengths between pieces (polygonize gives every edge the same vertex pair in both pieces)
    em = {}
    for k, f in enumerate(sub):
        Q = f["P"]
        for i, e in enumerate(f.get("E") or []):
            em.setdefault(e, []).append((k, math.hypot(Q[(i + 1) % len(Q)][0] - Q[i][0], Q[(i + 1) % len(Q)][1] - Q[i][1])))
    adj = {}
    for lst in em.values():
        for k, L_ in lst:
            for j, _ in lst:
                if j != k:
                    adj.setdefault(k, {})
                    adj[k][j] = adj[k].get(j, 0.0) + L_
    while True:
        grow = []
        for k, f in enumerate(sub):
            if k in owner:
                continue
            best = None
            for j, L_ in (adj.get(k) or {}).items():
                if owner.get(j) and (best is None or L_ > best[0]):
                    best = (L_, j)
            if best is not None:
                grow.append((k, best[1]))
        if not grow:
            break
        for k, j in grow:
            Ls = owner[j]
            if len(Ls) == 1:
                li = Ls[0]
            else:
                cx, cy = interior_point(sub[k]["P"])
                li = min(Ls, key=lambda i: (labels[i][0] - cx) ** 2 + (labels[i][1] - cy) ** 2)
            units.setdefault(li, []).append(sub[k]["P"])
            owner[k] = [li]
    for k, f in enumerate(sub):                       # pieces touching no labelled piece: the nearest label
        if k in owner:
            continue
        cx, cy = interior_point(f["P"])
        li = min(range(len(labels)), key=lambda i: (labels[i][0] - cx) ** 2 + (labels[i][1] - cy) ** 2)
        units.setdefault(li, []).append(f["P"])
    out = [(units[i], labels[i]) for i in range(len(labels)) if units.get(i)]
    return out + [([sub[k]["P"]], None) for k in own]


# ============================================================ READERS
def empty_raw():
    return dict(lines={}, plines={}, points={}, texts={})


def survey_layers():
    L = list(DWG["bld"].keys()) + [DWG["shed"], DWG["door"], DWG["stairs"], DWG["floors"], DWG["names"],
                                   DWG["stream_names"], DWG["park"], DWG["survey"], DWG["slope_hatch"], DWG["minarets"]]
    for k in ("walls", "fences", "slopes", "roads", "bridges", "banks", "water_misc", "contours", "spot_texts"):
        L += DWG[k]
    L += list(DWG["trees"].keys())
    L += [l for l in ALIGN_LAYERS if l not in L]
    return L


SYMBOL_LAYERS = set(DWG["trees"].keys()) | {DWG["minarets"], DWG["survey"]}


def read_rhino(bb, layers=None):
    """Read the survey layers of the open Rhino document (pure-python output)."""
    R = empty_raw()

    def inbb(x, y):
        return bb is None or (bb[0] <= x <= bb[2] and bb[1] <= y <= bb[3])
    for name in (layers or survey_layers()):
        idx = doc.Layers.FindByFullPath(name, -1)
        if idx < 0:
            for lay in doc.Layers:
                if not lay.IsDeleted and lay.Name == name:
                    idx = lay.Index
                    break
        if idx < 0:
            continue
        objs = doc.Objects.FindByLayer(doc.Layers[idx])
        if not objs:
            continue
        for o in objs:
            g = o.Geometry
            try:
                if isinstance(g, rg.TextEntity):
                    c = g.GetBoundingBox(True).Center
                    if inbb(c.X, c.Y):
                        xa = g.Plane.XAxis
                        o_ = g.Plane.Origin
                        R["texts"].setdefault(name, []).append((g.PlainText, c.X, c.Y, g.TextHeight,
                                                                math.atan2(xa.Y, xa.X), o_.X, o_.Y))
                elif isinstance(g, rg.Point):
                    p = g.Location
                    if inbb(p.X, p.Y):
                        R["points"].setdefault(name, []).append((p.X, p.Y, p.Z))
                elif isinstance(g, rg.Curve):
                    b = g.GetBoundingBox(True)
                    if bb is not None and not bb_hit((b.Min.X, b.Min.Y, b.Max.X, b.Max.Y), bb):
                        continue
                    if isinstance(g, rg.ArcCurve) and g.IsCircle() and name in SYMBOL_LAYERS:
                        cc = g.Arc.Center                    # a symbol drawn as a circle: its place only
                        R["points"].setdefault(name, []).append((cc.X, cc.Y, cc.Z))
                        continue
                    pts = None
                    res = g.TryGetPolyline()
                    if isinstance(res, tuple) and res[0]:
                        pl = res[1]
                        pts = [(pl[i].X, pl[i].Y, pl[i].Z) for i in range(pl.Count)]
                    if not pts:
                        n_ = max(8 if g.IsClosed else 2, int(g.GetLength() / 1.0))
                        ts = g.DivideByCount(n_, True) or []
                        pts = [(g.PointAt(t).X, g.PointAt(t).Y, g.PointAt(t).Z) for t in ts]
                        if g.IsClosed and len(pts) >= 3 and pts[0] != pts[-1]:
                            pts.append(pts[0])               # a closed curve's division leaves out its end
                    if len(pts) < 2:
                        continue
                    if len(pts) > 2:
                        R["plines"].setdefault(name, []).append(pts)
                    lst = R["lines"].setdefault(name, [])
                    for i in range(len(pts) - 1):
                        lst.append((pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1]))
                    if name in DWG["zlines"]:                # v33: their heights too, for the terrain (also 2-point lines)
                        R["plines"].setdefault("Z::" + name, []).append(pts)
            except Exception:
                pass
    return R


def parse_osm(path):
    root = ET.parse(path).getroot()
    nodes, pois = {}, []
    for n in root.iter("node"):
        try:
            ll = (float(n.get("lon")), float(n.get("lat")))
        except (TypeError, ValueError):
            continue
        nodes[n.get("id")] = ll
        tg = n.findall("tag")
        if tg:
            pois.append((ll, {t.get("k"): t.get("v") for t in tg}))
    ways = {}
    for w in root.iter("way"):
        ways[w.get("id")] = ([nd.get("ref") for nd in w.findall("nd")],
                             {t.get("k"): t.get("v") for t in w.findall("tag")})
    rels = []
    for r in root.iter("relation"):
        rels.append(([(m.get("ref"), m.get("role")) for m in r.findall("member") if m.get("type") == "way"],
                     {t.get("k"): t.get("v") for t in r.findall("tag")}))
    proj = {}

    def P(ref):
        p = proj.get(ref)
        if p is None and ref in nodes:
            p = to_dwg(*nodes[ref])
            proj[ref] = p
        return p
    return dict(nodes=nodes, ways=ways, rels=rels, pois=pois, P=P)


def place_cat(h, basic):
    top = h[0] if h else ""
    sub = h[1] if len(h) > 1 else ""
    if top == "cultural_and_historic":
        return "institutional" if sub == "cultural_center" else "religious"
    if top in ("education", "health_care", "community_and_government"):
        return "institutional"
    if top == "arts_and_entertainment":
        return "institutional" if sub in ("museum", "performing_arts_venue", "arts_and_crafts_space") else "commercial"
    if top == "travel_and_transportation":
        if sub in ("parking", "fueling_station", "ground_transport_facility_or_service"):
            return "transport"
        return "industrial" if sub == "vehicle_service" else "commercial"
    if top in ("shopping", "food_and_drink", "lodging", "lifestyle_services"):
        return "commercial"
    if top == "services_and_business":
        if sub in ("manufacturer", "b2b_transportation_and_storage_service", "storage_facility", "agricultural_service"):
            return "industrial"
        return "commercial"
    if top == "sports_and_recreation":
        return None if sub in ("park", "recreational_trail_or_path") else "commercial"
    return None


def parse_places(path):
    out = []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for ft in data.get("features", []):
        try:
            g = ft.get("geometry") or {}
            if g.get("type") != "Point":
                continue
            p = ft.get("properties") or {}
            conf = p.get("confidence") or 0.0
            if conf < 0.45:
                continue
            tx = p.get("taxonomy") or {}
            if isinstance(tx, str):
                tx = json.loads(tx)
            cat = place_cat(tx.get("hierarchy") or [], p.get("basic_category"))
            if not cat:
                continue
            nm = p.get("names") or {}
            if isinstance(nm, str):
                nm = json.loads(nm)
            x, y = to_dwg(*g["coordinates"][:2])
            hier = tx.get("hierarchy") or []
            her = bool(hier) and hier[0] == "cultural_and_historic" and (len(hier) < 2 or hier[1] != "cultural_center")
            out.append(dict(x=x, y=y, cat=cat, name=(nm or {}).get("primary") or "", src="overture", her=her))
        except Exception:
            continue
    return out


# ============================================================ WHERE IS THE SURVEY IN THIS FILE?
def fit_user_transform(texts):
    """Rigid + scale transform original survey -> this file, from labels found in both."""
    ref = {}
    for item in REF_LABELS.split(";"):
        parts = item.split("|")
        if len(parts) == 3:
            ref[parts[0]] = (float(parts[1]), float(parts[2]))
    seen, pos = {}, {}
    for lay in ALIGN_LAYERS:
        for t in texts.get(lay, []):
            s = t[0].strip()
            if s in ref:
                seen[s] = seen.get(s, 0) + 1
                pos[s] = (t[5], t[6]) if len(t) > 6 else (t[1], t[2])
    pairs = [(ref[s], pos[s]) for s in pos if seen[s] == 1]
    if len(pairs) < 3:
        return None

    def solve(pp):
        n = float(len(pp))
        ax = sum(a[0] for a, b in pp) / n
        ay = sum(a[1] for a, b in pp) / n
        bx = sum(b[0] for a, b in pp) / n
        by = sum(b[1] for a, b in pp) / n
        sxx = sum((a[0] - ax) * (b[0] - bx) + (a[1] - ay) * (b[1] - by) for a, b in pp)
        sxy = sum((a[0] - ax) * (b[1] - by) - (a[1] - ay) * (b[0] - bx) for a, b in pp)
        saa = sum((a[0] - ax) ** 2 + (a[1] - ay) ** 2 for a, b in pp) or 1.0
        th = math.atan2(sxy, sxx)
        s = math.hypot(sxx, sxy) / saa
        c, sn = math.cos(th), math.sin(th)
        return dict(s=s, th=th, c=c, sn=sn, tx=bx - s * (c * ax - sn * ay), ty=by - s * (sn * ax + c * ay))

    def resid(T, a, b):
        x, y = T_apply(T, a[0], a[1])
        return math.hypot(x - b[0], y - b[1])
    T = solve(pairs)
    for _ in range(3):
        r = sorted(resid(T, a, b) for a, b in pairs)
        lim = max(1.0, 3.0 * r[len(r) // 2])
        keep = [(a, b) for a, b in pairs if resid(T, a, b) <= lim]
        if len(keep) < 3 or len(keep) == len(pairs):
            break
        pairs = keep
        T = solve(pairs)
    r = sorted(resid(T, a, b) for a, b in pairs)
    T["n"], T["err"] = len(pairs), r[len(r) // 2]
    return T


IDENTITY = dict(s=1.0, th=0.0, c=1.0, sn=0.0, tx=0.0, ty=0.0, n=0, err=0.0)


def T_apply(T, x, y):
    return (T["s"] * (T["c"] * x - T["sn"] * y) + T["tx"], T["s"] * (T["sn"] * x + T["c"] * y) + T["ty"])


def T_inverse(T):
    s, c, sn = 1.0 / T["s"], T["c"], -T["sn"]
    tx, ty = -T["tx"], -T["ty"]
    return dict(s=s, th=-T["th"], c=c, sn=sn, tx=s * (c * tx - sn * ty), ty=s * (sn * tx + c * ty), n=T.get("n", 0),
                err=T.get("err", 0.0))


def raw_to_survey(R, T):
    """Bring everything read from the file back to original survey coordinates (metres)."""
    if abs(T["s"] - 1.0) < 1e-9 and abs(T["th"]) < 1e-12 and abs(T["tx"]) < 1e-9 and abs(T["ty"]) < 1e-9:
        return R
    I = T_inverse(T)
    zs = I["s"]
    out = empty_raw()
    for lay, lst in R["lines"].items():
        o = out["lines"][lay] = []
        for s in lst:
            a, b = T_apply(I, s[0], s[1]), T_apply(I, s[2], s[3])
            o.append((a[0], a[1], b[0], b[1]))
    for lay, lst in R["plines"].items():
        out["plines"][lay] = [[T_apply(I, p[0], p[1]) + (p[2] * zs,) for p in P] for P in lst]
    for lay, lst in R["points"].items():
        out["points"][lay] = [T_apply(I, p[0], p[1]) + (p[2] * zs,) for p in lst]
    for lay, lst in R["texts"].items():
        o = out["texts"][lay] = []
        for t in lst:
            c_ = T_apply(I, t[1], t[2])
            o_ = T_apply(I, t[5], t[6]) if len(t) > 6 else c_
            o.append((t[0], c_[0], c_[1], t[3] * zs, t[4] - T["th"], o_[0], o_[1]))
    return out


def _layer_points(R, lay):
    pts = []
    for s in R["lines"].get(lay, []):
        pts.append((s[0], s[1]))
        pts.append((s[2], s[3]))
    for P in R["plines"].get(lay, []):
        pts += [(p[0], p[1]) for p in P]
    for p in R["points"].get(lay, []):
        pts.append((p[0], p[1]))
    for t in R["texts"].get(lay, []):
        pts.append((t[1], t[2]))
    return pts


def _rigid_apply(M, x, y):
    c, s, tx, ty = M
    return (c * x - s * y + tx, s * x + c * y + ty)


def _rigid_fit(pairs):
    """Least-squares rotation + translation (no scale) taking a -> b for [(a, b)]."""
    n = float(len(pairs))
    ax = sum(a[0] for a, b in pairs) / n
    ay = sum(a[1] for a, b in pairs) / n
    bx = sum(b[0] for a, b in pairs) / n
    by = sum(b[1] for a, b in pairs) / n
    sxx = sum((a[0] - ax) * (b[0] - bx) + (a[1] - ay) * (b[1] - by) for a, b in pairs)
    sxy = sum((a[0] - ax) * (b[1] - by) - (a[1] - ay) * (b[0] - bx) for a, b in pairs)
    th = math.atan2(sxy, sxx)
    c, s = math.cos(th), math.sin(th)
    return (c, s, bx - (c * ax - s * ay), by - (s * ax + c * ay)), th


def register_layers(R):
    """Survey layers that were moved or turned on their own (typically left behind, locked or hidden, when the rest
    of the drawing was rotated or moved) are found and put back in memory. The shift is solved from corners they
    share with the buildings (doors and sheds sit on building walls); the Rhino file is not changed."""
    bl_layers = [l for l in DWG["bld"] if R["lines"].get(l)]
    if not bl_layers:
        return R
    main_lay = max(bl_layers, key=lambda l: len(R["lines"][l]))
    main = R["lines"][main_lay]
    if len(main) < 50:
        return R
    C = 100.0
    core = set()
    for s in main:
        for x, y in ((s[0], s[1]), (s[2], s[3])):
            core.add((int(math.floor(x / C)), int(math.floor(y / C))))
    zone = set((i + di, j + dj) for i, j in core for di in (-2, -1, 0, 1, 2) for dj in (-2, -1, 0, 1, 2))

    def inside(pts):
        if not pts:
            return 1.0
        return sum(1 for x, y in pts if (int(math.floor(x / C)), int(math.floor(y / C))) in zone) / float(len(pts))
    layers = sorted(set(R["lines"]) | set(R["plines"]) | set(R["points"]) | set(R["texts"]))
    frac = dict((l, inside(_layer_points(R, l))) for l in layers)
    off = [l for l in layers if frac[l] < 0.5 and l != main_lay]
    if not off:
        return R
    # anchors: endpoints of the layers that are in place, hashed at 1 cm
    anchors = {}
    alen = {}
    for l in layers:
        if l in off:
            continue
        for s in R["lines"].get(l, []):
            for x, y in ((s[0], s[1]), (s[2], s[3])):
                anchors[(int(round(x * 100.0)), int(round(y * 100.0)))] = (x, y)
            L_ = math.hypot(s[2] - s[0], s[3] - s[1])
            if L_ > 2.0:
                alen.setdefault(int(round(L_ * 1000.0)), []).append(s)

    def hit(x, y):
        kx, ky = int(round(x * 100.0)), int(round(y * 100.0))
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                a_ = anchors.get((kx + dx, ky + dy))
                if a_ is not None and abs(a_[0] - x) <= 0.02 and abs(a_[1] - y) <= 0.02:
                    return a_
        return None
    dsegs = [s for l in off for s in R["lines"].get(l, []) if math.hypot(s[2] - s[0], s[3] - s[1]) > 2.0]
    dpts = [(x, y) for l in off for s in R["lines"].get(l, []) for x, y in ((s[0], s[1]), (s[2], s[3]))]
    M = None
    if dsegs and dpts:
        rnd = random.Random(17)
        probe = rnd.sample(dpts, min(400, len(dpts)))
        quick = probe[:40]
        best, best_n = None, 0
        for _ in range(700):
            d = dsegs[rnd.randrange(len(dsegs))]
            Lk = int(round(math.hypot(d[2] - d[0], d[3] - d[1]) * 1000.0))
            cands = [a for k in (Lk - 1, Lk, Lk + 1) for a in alen.get(k, ())]
            if len(cands) > 40:
                cands = rnd.sample(cands, 40)
            for a in cands:
                for a0, a1 in (((a[0], a[1]), (a[2], a[3])), ((a[2], a[3]), (a[0], a[1]))):
                    th = math.atan2(a1[1] - a0[1], a1[0] - a0[0]) - math.atan2(d[3] - d[1], d[2] - d[0])
                    c, s_ = math.cos(th), math.sin(th)
                    H = (c, s_, a0[0] - (c * d[0] - s_ * d[1]), a0[1] - (s_ * d[0] + c * d[1]))
                    if sum(1 for x, y in quick if hit(*_rigid_apply(H, x, y)) is not None) < 3:
                        continue
                    n = sum(1 for x, y in probe if hit(*_rigid_apply(H, x, y)) is not None)
                    if n > best_n:
                        best, best_n = H, n
            if best_n >= 0.25 * len(probe):
                break
        if best is not None and best_n >= max(12, 0.05 * len(probe)):
            pairs = []
            for x, y in dpts:
                a_ = hit(*_rigid_apply(best, x, y))
                if a_ is not None:
                    pairs.append(((x, y), a_))
            if len(pairs) >= 20:
                M, th = _rigid_fit(pairs)
                res = sorted(math.hypot(_rigid_apply(M, a[0], a[1])[0] - b[0], _rigid_apply(M, a[0], a[1])[1] - b[1])
                             for a, b in pairs)
                M_info = (len(pairs), math.degrees(th), res[len(res) // 2])
    fixed, dropped, kept = [], [], []
    for l in off:
        if M is not None:
            moved_pts = [_rigid_apply(M, x, y) for x, y in _layer_points(R, l)]
            if inside(moved_pts) >= 0.8:
                th_ = math.atan2(M[1], M[0])
                if l in R["lines"]:
                    R["lines"][l] = [_rigid_apply(M, s[0], s[1]) + _rigid_apply(M, s[2], s[3]) for s in R["lines"][l]]
                if l in R["plines"]:
                    R["plines"][l] = [[_rigid_apply(M, p[0], p[1]) + tuple(p[2:]) for p in P] for P in R["plines"][l]]
                if l in R["points"]:
                    R["points"][l] = [_rigid_apply(M, p[0], p[1]) + tuple(p[2:]) for p in R["points"][l]]
                if l in R["texts"]:
                    out_ = []
                    for t in R["texts"][l]:
                        c_ = _rigid_apply(M, t[1], t[2])
                        o_ = _rigid_apply(M, t[5], t[6]) if len(t) > 6 else c_
                        out_.append((t[0], c_[0], c_[1], t[3], t[4] + th_, o_[0], o_[1]))
                    R["texts"][l] = out_
                fixed.append(l)
                continue
        if frac[l] < 0.2:
            for k in ("lines", "plines", "points", "texts"):
                R[k].pop(l, None)
            dropped.append(l)
        else:
            kept.append(l)
    if fixed:
        LOG.append("WARNING: {} survey layers sat away from the rest of the drawing (moved or turned on their own, "
                   "probably locked or hidden while the drawing was rotated): {}. They were put back in memory with "
                   "the shift found from {} corners they share with the buildings (turn {:.4f} deg, error {:.3f} m). "
                   "Your Rhino file still has them apart.".format(len(fixed), ", ".join(fixed), M_info[0], M_info[1],
                                                                 M_info[2]))
    if dropped:
        LOG.append("WARNING: these layers lie outside the survey and could not be lined up, so they were left out: "
                   "{}.".format(", ".join(dropped)))
    return R


# ============================================================ OSM TAG RULES (fallback layer)
GREEN_WOOD_LU = {"forest"}
AGRI_TREES_LU = {"orchard", "vineyard", "plant_nursery"}
AGRI_FIELD_LU = {"farmland", "meadow", "greenhouse_horticulture", "farmyard", "animal_keeping"}
GREEN_WOOD_NAT = {"wood", "scrub"}
GREEN_PARK_LU = {"village_green", "cemetery", "allotments", "recreation_ground"}
GREEN_PARK_LE = {"park", "garden", "nature_reserve"}
GREEN_GRASS_LU = {"grass", "greenery"}
GREEN_GRASS_NAT = {"grassland", "heath", "wetland"}
GREEN_GRASS_LE = {"pitch", "playground", "sports_centre", "dog_park"}
VACANT_LU = {"construction", "brownfield", "greenfield", "landfill"}
INST_AMEN = {"school", "university", "college", "kindergarten", "hospital", "clinic", "doctors", "dentist",
             "townhall", "police", "courthouse", "library", "post_office", "fire_station", "community_centre",
             "social_facility", "public_building", "prison", "arts_centre", "theatre"}
COM_AMEN = {"restaurant", "cafe", "bar", "pub", "fast_food", "bank", "pharmacy", "marketplace", "ice_cream",
            "bureau_de_change", "car_rental", "nightclub", "cinema"}
