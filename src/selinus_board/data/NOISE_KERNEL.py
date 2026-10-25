NOISE_KERNEL = r'''import math

NOISE_LAT_FROM = 3.0     # dB: the ways round the sides are worked out where the way over the roof screens more than this


def pip(x, y, P):
    inside = False
    n = len(P)
    j = n - 1
    for i in range(n):
        xi, yi = P[i]
        xj, yj = P[j]
        if (yi > y) != (yj > y):
            if x < (xj - xi) * (y - yi) / (yj - yi) + xi:
                inside = not inside
        j = i
    return inside


def convex_hull(pts):
    """Monotone chain hull (the turn test written inline: same arithmetic, no function call per point)."""
    pts = sorted(set(pts))
    if len(pts) < 3:
        return pts
    lo, hi = [], []
    for p in pts:
        px, py = p
        while len(lo) >= 2:
            o, a = lo[-2], lo[-1]
            if (a[0] - o[0]) * (py - o[1]) - (a[1] - o[1]) * (px - o[0]) <= 0:
                lo.pop()
            else:
                break
        lo.append(p)
    for p in reversed(pts):
        px, py = p
        while len(hi) >= 2:
            o, a = hi[-2], hi[-1]
            if (a[0] - o[0]) * (py - o[1]) - (a[1] - o[1]) * (px - o[0]) <= 0:
                hi.pop()
            else:
                break
        hi.append(p)
    return lo[:-1] + hi[:-1]


def screen_db(t0, t1, Hb, dist, zr, zs, D=None):
    """Screening of one building (flat roof Hb from t0 to t1 along the ray) between a receiver (height zr, t = 0) and
    a source (height zs, t = dist). Path difference z over the roof: the shortest way above it (receiver, the roof
    edges that rise above the straight line, source) minus the direct line; negative when the line of sight passes
    above the roof (ISO 9613-2). RLS-90-type: Dz = 10 lg(3 + 80 z Kw), Kw = exp(-sqrt(A B s / 2z) / 2000) (A, B:
    source and receiver to their diffraction edge, s: the direct distance; the factor 80 is not confirmed against the
    RLS-90 text). v21 (R01-14): the limits, at most 20 dB over one edge and 25 dB over two, are ISO 9613-2:1996 rules,
    and the cut-off, none once 3 + 80 z Kw <= 1, follows ISO 9613-2:2024 / VBUS eq. 15; RLS-90 gives no maximum."""
    hypot = math.hypot
    if D is None:
        D = hypot(dist, zr - zs)
    k = (zs - zr) / dist
    above0 = Hb > zr + k * t0                            # roof edge above the line of sight
    above1 = Hb > zr + k * t1
    kw, cap = 1.0, 20.0
    if above0 or above1:
        if zr < Hb and zs < Hb:                          # over both roof edges
            A, B = hypot(dist - t1, Hb - zs), hypot(t0, Hb - zr)
            z_ = B + (t1 - t0) + A - D
            cap = 25.0
        elif zr >= Hb:                                   # receiver above the roof: only the far edge counts
            A, B = hypot(dist - t1, Hb - zs), hypot(t1, zr - Hb)
            z_ = B + A - D
        else:                                            # source above the roof: only the near edge counts
            A, B = hypot(dist - t0, zs - Hb), hypot(t0, Hb - zr)
            z_ = B + A - D
        if z_ > 0.0:
            kw = math.exp(-math.sqrt(A * B * D / (2.0 * z_)) / 2000.0)
    else:
        z_ = D - min(hypot(t0, Hb - zr) + hypot(dist - t0, Hb - zs), hypot(t1, Hb - zr) + hypot(dist - t1, Hb - zs))
    arg = 3.0 + 80.0 * z_ * kw
    if arg <= 1.0:
        return 0.0
    return min(cap, 10.0 * math.log10(arg))


def round_paths(H, x, y, mx, my):
    """v16.4: the plan lengths of the two shortest ways from (x, y) to (mx, my) round a convex hull H, one past each
    side (the taut string: the perimeter of the hull of the two ends and the hull corners on that side, less the
    straight line); None when either end lies inside the hull (a courtyard: no way round)."""
    dx, dy = mx - x, my - y
    D2 = math.hypot(dx, dy)
    if D2 < 1e-6 or pip(x, y, H) or pip(mx, my, H):
        return None
    c, s_ = dx / D2, dy / D2
    left, right = [], []
    for px, py in H:
        qx, qy = (px - x) * c + (py - y) * s_, -(px - x) * s_ + (py - y) * c
        if qy > 1e-9:
            left.append((qx, qy))
        elif qy < -1e-9:
            right.append((qx, -qy))
    out = []
    for side in (left, right):
        if not side:
            out.append(D2)
            continue
        hh = convex_hull([(0.0, 0.0), (D2, 0.0)] + side)
        n = len(hh)
        per = sum(math.hypot(hh[(q + 1) % n][0] - hh[q][0], hh[(q + 1) % n][1] - hh[q][1]) for q in range(n))
        out.append(per - D2)
    return out


def lateral_db(dtop, paths, D, zr, zs):
    """v16.4: the screening of one building block with the sound that bends round its two sides (ISO 9613-2 7.4, the
    lateral paths around the vertical edges, with K = 1) added to the way over its roof (dtop): the three paths
    combined by energy, A = -10 lg(10^(-Dtop/10) + 10^(-Dleft/10) + 10^(-Dright/10)); each side's Dz by the formula of
    the roof, 10 lg(3 + 80 z), at most 20 dB, z = the way round in 3D less the direct distance D."""
    if paths is None:
        return dtop
    e = 10.0 ** (-0.1 * dtop)
    dh = zr - zs
    for P in paths:
        z_ = math.hypot(P, dh) - D
        arg = 3.0 + 80.0 * z_
        d_ = 0.0 if arg <= 1.0 else min(20.0, 10.0 * math.log10(arg))
        e += 10.0 ** (-0.1 * d_)
    return max(0.0, -10.0 * math.log10(e))


class TRCore(object):
    """The terrain raster's bilinear read (TerrainRaster)."""

    def z(self, x, y):
        fi = (x - self.x0) / self.c
        fj = (y - self.y0) / self.c
        i = min(self.nx - 2, max(0, int(fi)))
        j = min(self.ny - 2, max(0, int(fj)))
        ti = min(1.0, max(0.0, fi - i))
        tj = min(1.0, max(0.0, fj - j))
        r0, r1 = self.Z[j], self.Z[j + 1]
        return (r0[i] * (1 - ti) + r0[i + 1] * ti) * (1 - tj) + (r1[i] * (1 - ti) + r1[i + 1] * ti) * tj


class NoiseCore(object):
    """What a receiver needs of the sound model (NoiseModel): the same code in Rhino and in a worker process."""

    def inside(self, x, y):
        return any(pip(x, y, b["P"]) and not any(pip(x, y, H) for H in b.get("holes") or ())
                   for b in self.gR.query((x, y, x, y)))

    def ground_mean(self, x, y, zg, mx, my, zsg):
        """Mean ground height under the path from the receiver (ground zg) to a road piece (ground zsg): the
        terrain at a quarter, half and three quarters of the way, trapezoid rule."""
        z_ = self.TR.z
        dx, dy = mx - x, my - y
        return (0.5 * zg + z_(x + 0.25 * dx, y + 0.25 * dy) + z_(x + 0.5 * dx, y + 0.5 * dy)
                + z_(x + 0.75 * dx, y + 0.75 * dy) + 0.5 * zsg) / 4.0

    def crossings(self, x, y, ang, ztop):
        """Buildings crossed by the ray from (x, y) at angle ang within R, nearest first: [(t0, t1, roof)], up to and
        including the first whose roof reaches ztop. A receiver above a roof keeps that roof as a screen from t = 0.
        The ray walks the 15 m building grid cell by cell (each cell once) and tests a building's walls only when the
        ray meets its bounding box."""
        dx, dy = math.cos(ang), math.sin(ang)
        R = self.R
        rx, ry = dx * R, dy * R
        cs = self.gR.c
        cells = self.gR.d
        floor = math.floor
        ci, cj = int(floor(x / cs)), int(floor(y / cs))
        stx = 1 if dx > 0 else -1
        sty = 1 if dy > 0 else -1
        if abs(dx) > 1e-12:
            nxb = (ci + (1 if dx > 0 else 0)) * cs
            tmx, tdx = (nxb - x) / dx, cs / abs(dx)
        else:
            tmx, tdx = 1e30, 1e30
        if abs(dy) > 1e-12:
            nyb = (cj + (1 if dy > 0 else 0)) * cs
            tmy, tdy = (nyb - y) / dy, cs / abs(dy)
        else:
            tmy, tdy = 1e30, 1e30
        seen_ = set()
        found = []
        t_stop = None
        t_cell = 0.0
        while t_cell < R and (t_stop is None or t_cell < t_stop):
            for b in cells.get((ci, cj), ()):
                k = id(b)
                if k in seen_:
                    continue
                seen_.add(k)
                bb = b["bb"]
                # slab test of the ray segment against the bounding box
                lo_, hi_ = 0.0, R
                if abs(dx) > 1e-12:
                    ta, tb = (bb[0] - x) / dx, (bb[2] - x) / dx
                    if ta > tb:
                        ta, tb = tb, ta
                    lo_, hi_ = max(lo_, ta), min(hi_, tb)
                elif not (bb[0] <= x <= bb[2]):
                    continue
                if abs(dy) > 1e-12:
                    ta, tb = (bb[1] - y) / dy, (bb[3] - y) / dy
                    if ta > tb:
                        ta, tb = tb, ta
                    lo_, hi_ = max(lo_, ta), min(hi_, tb)
                elif not (bb[1] <= y <= bb[3]):
                    continue
                if lo_ > hi_ + 1e-9:
                    continue
                ed = b.get("_ed")
                if ed is None:
                    ed = []
                    for P in [b["P"]] + list(b.get("holes") or ()):  # courtyard walls are crossed too
                        n = len(P)
                        ed += [(P[q][0], P[q][1], P[(q + 1) % n][0] - P[q][0], P[(q + 1) % n][1] - P[q][1])
                               for q in range(n)]
                    b["_ed"] = ed
                ts = []
                for ax, ay, sx, sy in ed:
                    rxs = rx * sy - ry * sx
                    if abs(rxs) < 1e-12:
                        continue
                    qx, qy = ax - x, ay - y
                    t = (qx * sy - qy * sx) / rxs
                    if 0.0 < t <= 1.0:
                        u = (qx * ry - qy * rx) / rxs
                        if 0.0 <= u <= 1.0:
                            ts.append(t * R)
                if len(ts) >= 2:
                    f = (min(ts), max(ts), b["top"], b)
                elif len(ts) == 1 and pip(x, y, b["P"]):
                    f = (0.0, ts[0], b["top"], b)
                else:
                    continue
                found.append(f)
                if f[2] >= ztop and (t_stop is None or f[0] < t_stop):
                    t_stop = f[0]
            if tmx < tmy:
                t_cell = tmx
                tmx += tdx
                ci += stx
            else:
                t_cell = tmy
                tmy += tdy
                cj += sty
        found.sort(key=lambda f: (f[0], f[1], f[2]))
        out = []
        for f in found:
            out.append(f)
            if f[2] >= ztop:
                break
        return out

    def column(self, x, y, zg, heights):
        """Levels at heights above ground at (x, y): per height (Ld, Le, Ln, Lden) in dB(A), or None."""
        R, wbin, two_pi = self.R, self.wbin, 2.0 * math.pi
        zrs = [zg + h for h in heights]
        ztop = max(zrs)
        rays = {}
        acc = [[0.0, 0.0, 0.0] for _ in heights]
        log10, hypot, atan2 = math.log10, math.hypot, math.atan2
        cs, cells = self.gS.c, self.gS.d
        near = []
        for i in range(int(math.floor((x - R) / cs)), int(math.floor((x + R) / cs)) + 1):
            ex = max(i * cs - x, 0.0, x - (i + 1) * cs)
            for j in range(int(math.floor((y - R) / cs)), int(math.floor((y + R) / cs)) + 1):
                lst = cells.get((i, j))
                if lst and hypot(ex, max(j * cs - y, 0.0, y - (j + 1) * cs)) <= R:
                    near.extend(lst)                         # each road piece sits in exactly one cell
        for s in near:
            mx, my = s["m"]
            dist = hypot(mx - x, my - y)
            if dist > R:
                continue
            dist = max(dist, s["L"] / 2.0, 1.0)
            zs, zsg = s["zs"], s["z"]
            cr = None
            if dist > 4.0:
                kb = int((atan2(my - y, mx - x) % two_pi) / wbin)
                cr = rays.get(kb)
                if cr is None:
                    cr = rays[kb] = self.crossings(x, y, (kb + 0.5) * wbin, ztop)
            em = s["em"]
            gmean = self.ground_mean(x, y, zg, mx, my, zsg)
            for q, zr in enumerate(zrs):
                D = hypot(dist, zr - zs)                    # RLS-90 distance: road piece to receiver, in 3D
                hm = max(0.5, (zr + zs) / 2.0 - gmean)      # mean height of the path above the ground under it
                dbm = max(0.0, 4.8 - (hm / D) * (34.0 + 600.0 / D))
                dz = 0.0
                if cr:
                    for t0, t1, Hb, b_ in cr:
                        if t1 < dist:
                            d_ = screen_db(t0, t1, Hb, dist, zr, zs, D)
                            if d_ > NOISE_LAT_FROM and d_ > dz:      # v16.4: and the ways round the block's sides
                                d_ = lateral_db(d_, round_paths(b_["_hull"], x, y, mx, my), D, zr, zs)
                            if d_ > dz:
                                dz = d_
                                if dz >= 25.0:
                                    break
                        if Hb >= zr:
                            break
                base = s["lgL"] + (11.2 - 20.0 * log10(D) - D / 200.0) - max(dbm, dz)
                a_ = acc[q]
                for k in range(3):
                    if em[k] is not None:
                        a_[k] += 10.0 ** ((em[k] + base) / 10.0)
        out = []
        for a_ in acc:
            if a_[0] <= 0.0:
                out.append(None)
                continue
            Ld, Le, Ln = (10.0 * log10(v) if v > 0.0 else None for v in a_)
            if Le is None or Ln is None:
                out.append(None)
                continue
            lden = 10.0 * log10((12.0 * 10 ** (Ld / 10.0) + 4.0 * 10 ** ((Le + 5.0) / 10.0)
                                 + 8.0 * 10 ** ((Ln + 10.0) / 10.0)) / 24.0)
            out.append((Ld, Le, Ln, lden))
        return out

    def column_multi(self, x, y, zg, zrs):
        """column() for many receivers above one point (absolute heights zrs): the same model and, per height, the
        same arithmetic (screen_db written out); what does not depend on the height is worked out once per road
        piece. A roof edge stops being tested once the receiver is so far above the sight line over it that its path
        difference is below -0.025 m (where screen_db gives exactly 0; any path over a point p off the sight line is
        at least 2 p^2 / (D + p) longer), unless it is still the roof that ends the ray. Returns per height
        (Ld, Le, Ln, Lden) in dB(A), or None."""
        R, wbin, two_pi = self.R, self.wbin, 2.0 * math.pi
        ztop = max(zrs)
        rays = {}
        acc = [[0.0, 0.0, 0.0] for _ in zrs]
        hts = sorted(enumerate(zrs), key=lambda qz: qz[1])
        zrs_lo, zrs_hi = min(zrs), max(zrs)
        log10, hypot, atan2, sqrt, exp_ = math.log10, math.hypot, math.atan2, math.sqrt, math.exp
        c_ = 0.025 + 1e-9
        cs, cells = self.gS.c, self.gS.d
        near = []
        for i in range(int(math.floor((x - R) / cs)), int(math.floor((x + R) / cs)) + 1):
            ex = max(i * cs - x, 0.0, x - (i + 1) * cs)
            for j in range(int(math.floor((y - R) / cs)), int(math.floor((y + R) / cs)) + 1):
                lst = cells.get((i, j))
                if lst and hypot(ex, max(j * cs - y, 0.0, y - (j + 1) * cs)) <= R:
                    near.extend(lst)
        for s in near:
            mx, my = s["m"]
            dist = hypot(mx - x, my - y)
            if dist > R:
                continue
            dist = max(dist, s["L"] / 2.0, 1.0)
            zs, zsg = s["zs"], s["z"]
            live = None
            if dist > 4.0:
                kb = int((atan2(my - y, mx - x) % two_pi) / wbin)
                cr = rays.get(kb)
                if cr is None:
                    cr = rays[kb] = self.crossings(x, y, (kb + 0.5) * wbin, ztop)
                if cr:
                    Dm = hypot(dist, max(abs(zrs_hi - zs), abs(zrs_lo - zs)))
                    dreq = (c_ + sqrt(c_ * c_ + 8.0 * c_ * Dm)) / 4.0 * Dm / dist + 1e-6
                    live = []
                    for t0, t1, Hb, b_ in cr:
                        if t1 < dist:
                            f0, f1 = t0 / dist, t1 / dist          # receiver height clearing both edges by dreq
                            zsf = max((Hb + dreq - zs * f0) / (1.0 - f0), (Hb + dreq - zs * f1) / (1.0 - f1))
                            live.append((t0, t1, Hb, True, hypot(dist - t0, Hb - zs), hypot(dist - t1, Hb - zs), zsf, b_))
                        else:
                            live.append((t0, t1, Hb, False, 0.0, 0.0, -1e30, b_))
            e0, e1, e2 = s["em"]
            gmean = self.ground_mean(x, y, zg, mx, my, zsg)
            lgL = s["lgL"]
            rpaths = {}
            for q, zr in hts:
                D = hypot(dist, zr - zs)                    # RLS-90 distance: road piece to receiver, in 3D
                hm = max(0.5, (zr + zs) / 2.0 - gmean)
                dbm = max(0.0, 4.8 - (hm / D) * (34.0 + 600.0 / D))
                dz = 0.0
                if live:
                    live = [e for e in live if e[2] >= zr or e[6] > zr]     # heights only rise: dropped edges stay out
                    if live:
                        k = (zs - zr) / dist
                        for t0, t1, Hb, before, S0, S1, zsf, b_ in live:
                            if before and zr < zsf:
                                kw, cap = 1.0, 20.0
                                if Hb > zr + k * t0 or Hb > zr + k * t1:
                                    if zr < Hb and zs < Hb:
                                        B_, A_ = hypot(t0, Hb - zr), S1
                                        z_ = B_ + (t1 - t0) + A_ - D
                                        cap = 25.0
                                    elif zr >= Hb:
                                        B_, A_ = hypot(t1, zr - Hb), S1
                                        z_ = B_ + A_ - D
                                    else:
                                        B_, A_ = hypot(t0, Hb - zr), S0
                                        z_ = B_ + A_ - D
                                    if z_ > 0.0:
                                        kw = exp_(-sqrt(A_ * B_ * D / (2.0 * z_)) / 2000.0)
                                else:
                                    z_ = D - min(hypot(t0, Hb - zr) + S0, hypot(t1, Hb - zr) + S1)
                                arg = 3.0 + 80.0 * z_ * kw
                                if arg > 1.0:
                                    d_ = min(cap, 10.0 * log10(arg))
                                    if d_ > NOISE_LAT_FROM and d_ > dz:      # v16.4: the ways round the sides
                                        rp_ = rpaths.get(id(b_), 0)
                                        if rp_ == 0:
                                            rp_ = rpaths[id(b_)] = round_paths(b_["_hull"], x, y, mx, my)
                                        d_ = lateral_db(d_, rp_, D, zr, zs)
                                    if d_ > dz:
                                        dz = d_
                                        if dz >= 25.0:
                                            break
                            if Hb >= zr:
                                break
                base = lgL + (11.2 - 20.0 * log10(D) - D / 200.0) - max(dbm, dz)
                a_ = acc[q]
                if e0 is not None:
                    a_[0] += 10.0 ** ((e0 + base) / 10.0)
                if e1 is not None:
                    a_[1] += 10.0 ** ((e1 + base) / 10.0)
                if e2 is not None:
                    a_[2] += 10.0 ** ((e2 + base) / 10.0)
        out = []
        for a_ in acc:
            if a_[0] <= 0.0:
                out.append(None)
                continue
            Ld, Le, Ln = (10.0 * log10(v) if v > 0.0 else None for v in a_)
            if Le is None or Ln is None:
                out.append(None)
                continue
            lden = 10.0 * log10((12.0 * 10 ** (Ld / 10.0) + 4.0 * 10 ** ((Le + 5.0) / 10.0)
                                 + 8.0 * 10 ** ((Ln + 10.0) / 10.0)) / 24.0)
            out.append((Ld, Le, Ln, lden))
        return out


# ---- v17: the same code run by worker processes (one per core) for the sound map and the sound sections
class _Cells(object):
    """The parts of Grid a receiver reads (c, d, query), rebuilt from plain data in a worker."""

    def __init__(self, c, d):
        self.c, self.d = c, d

    def query(self, bb):
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


def _math_probe():
    """Fingerprint of the float arithmetic a worker would use (exact reprs): it must equal Rhino's own."""
    import sys
    v = [sys.version_info[0], sys.version_info[1]]
    for a in (0.37, 1.7, 3.3, 12.9, 77.7, 312.4):
        v += [repr(math.log10(a)), repr(10.0 ** (-a / 10.0)), repr(math.hypot(a, 1.3 * a + 0.1)),
              repr(math.atan2(a - 2.0, 1.1)), repr(math.exp(-a / 7.0)), repr(math.sqrt(a)), repr(math.cos(a)),
              repr(math.sin(a)), repr(10 ** (a / 10.0)), repr(a % (2.0 * math.pi))]
    return "|".join(str(x) for x in v)


def _noise_model_from(m):
    M = NoiseCore()
    M.R, M.wbin = m["R"], m["wbin"]
    tr = TRCore()
    tr.x0, tr.y0, tr.c, tr.nx, tr.ny, tr.Z = m["TR"]
    M.TR = tr
    M.gS = _Cells(m["gS"][0], m["gS"][1])
    M.gR = _Cells(m["gR"][0], m["gR"][1])
    return M


def _noise_worker_main(argv):
    import pickle
    if argv[1] == "--probe":
        print(_math_probe())
        return
    with open(argv[1], "rb") as f:
        M = _noise_model_from(pickle.load(f))
    with open(argv[2], "rb") as f:
        mode, tasks = pickle.load(f)
    fn = M.column_multi if mode == "multi" else M.column
    out = [fn(*t) for t in tasks]
    with open(argv[3], "wb") as f:
        pickle.dump(out, f, protocol=4)
'''
