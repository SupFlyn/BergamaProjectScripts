# ACIS 4.0 SAB solids (ODA writer: planes + exact NURBS surfaces, all curves NURBS) -> triangle meshes
import math, sys
import numpy as np
import sabread


def _bspl(ctrl, w, knots, deg, ts):
    """rational B-spline points at parameters ts (de Boor)"""
    ctrl = np.asarray(ctrl, float)
    w = np.ones(len(ctrl)) if w is None else np.asarray(w, float)
    P = np.hstack([ctrl * w[:, None], w[:, None]])
    out = []
    n = len(ctrl)
    for t in ts:
        t = min(max(t, knots[deg]), knots[n])
        k = deg
        while k < n - 1 and t >= knots[k + 1]:
            k += 1
        d = [P[j + k - deg].copy() for j in range(deg + 1)]
        for r in range(1, deg + 1):
            for j in range(deg, r - 1, -1):
                i = j + k - deg
                den = knots[i + deg - r + 1] - knots[i]
                a = 0.0 if den == 0 else (t - knots[i]) / den
                d[j] = (1 - a) * d[j - 1] + a * d[j]
        out.append(d[deg][:3] / d[deg][3])
    return np.array(out)


def _knots(pairs, deg):
    """ACIS (value, multiplicity) pairs -> full knot vector (end knots one more than stored)"""
    k = []
    for v, m in pairs:
        k += [v] * m
    return [k[0]] + k + [k[-1]]


class Curve:
    def __init__(self, toks):
        i = next(j for j, t in enumerate(toks) if t[0] == "n" and t[1] in ("nubs", "nurbs"))
        self.rat = toks[i][1] == "nurbs"
        self.deg = toks[i + 1][1]
        nk = toks[i + 3][1]
        j = i + 4
        pairs = [(toks[j + 2 * q][1], toks[j + 2 * q + 1][1]) for q in range(nk)]
        j += 2 * nk
        self.pairs = pairs
        self.knots = _knots(pairs, self.deg)
        n = len(self.knots) - self.deg - 1
        st = 4 if self.rat else 3
        vals = [toks[j + q][1] for q in range(n * st)]
        A = np.array(vals, float).reshape(n, st)
        self.ctrl = A[:, :3]
        self.w = A[:, 3] if self.rat else None

    def sample(self, seg_deg=30.0, min_r=0.0):
        if self.deg == 1:
            return self.ctrl.copy()
        t0, t1 = self.knots[self.deg], self.knots[len(self.ctrl)]
        fine = _bspl(self.ctrl, self.w, self.knots, self.deg, np.linspace(t0, t1, 65))
        d = np.diff(fine, axis=0)
        ln = np.linalg.norm(d, axis=1)
        ok = ln > 1e-12
        d = d[ok] / ln[ok, None]
        turn = float(np.degrees(np.arccos(np.clip((d[1:] * d[:-1]).sum(1), -1, 1))).sum()) if len(d) > 1 else 0.0
        size = float(np.linalg.norm(fine.max(0) - fine.min(0)))
        n = max(1, int(math.ceil(turn / (90.0 if size < min_r else seg_deg) - 1e-3)))   # a small fillet: one chord a quarter turn
        return _bspl(self.ctrl, self.w, self.knots, self.deg, np.linspace(t0, t1, n + 1))


class Surf:
    def __init__(self, toks):
        i = next(j for j, t in enumerate(toks) if t[0] == "n" and t[1] in ("nubs", "nurbs"))
        self.rat = toks[i][1] == "nurbs"
        self.du, self.dv = toks[i + 1][1], toks[i + 2][1]
        j = i + 3
        while toks[j][0] != "i":
            j += 1
        nku, nkv = toks[j][1], toks[j + 1][1]
        j += 2
        pu = [(toks[j + 2 * q][1], toks[j + 2 * q + 1][1]) for q in range(nku)]
        j += 2 * nku
        pv = [(toks[j + 2 * q][1], toks[j + 2 * q + 1][1]) for q in range(nkv)]
        j += 2 * nkv
        self.ku, self.kv = _knots(pu, self.du), _knots(pv, self.dv)
        nu, nv = len(self.ku) - self.du - 1, len(self.kv) - self.dv - 1
        st = 4 if self.rat else 3
        A = np.array([toks[j + q][1] for q in range(nu * nv * st)], float).reshape(nv, nu, st)
        self.P = A[:, :, :3]
        self.W = A[:, :, 3] if self.rat else np.ones((nv, nu))
        self.nu, self.nv = nu, nv

    def grid(self, us, vs):
        rows = []
        for iv in range(self.nv):                         # curves along u for every v control row
            rows.append((_bspl(self.P[iv], self.W[iv], self.ku, self.du, us),
                         _bspl(self.W[iv][:, None] * np.ones((1, 3)), None, self.ku, self.du, us)[:, 0]))
        G = np.zeros((len(vs), len(us), 3))
        for a in range(len(us)):
            cp = np.array([rows[iv][0][a] for iv in range(self.nv)])
            cw = np.array([rows[iv][1][a] for iv in range(self.nv)])
            G[:, a, :] = _bspl(cp, cw, self.kv, self.dv, vs)
        return G


def solid(d):
    """-> dict(recs, faces=[dict(kind, sense, loops=[[coedge...]] ...)])"""
    hdr, recs, _rest = sabread.records(d)
    return hdr, recs


def _plane_basis(n):
    n = n / np.linalg.norm(n)
    a = np.cross(n, [1.0, 0, 0]) if abs(n[0]) < 0.9 else np.cross(n, [0, 1.0, 0])
    a /= np.linalg.norm(a)
    return a, np.cross(n, a)


def _cdt(rings2d):
    """rings2d: [Nx2 arrays], the largest is the outline, the rest holes -> triangles as index triples into the
    stacked points (constrained Delaunay on the rings' own points only)"""
    import shapely
    from shapely.geometry import Polygon
    pts = np.vstack(rings2d)
    ar = [abs(Polygon(r).area) if len(r) >= 3 else 0.0 for r in rings2d]
    o = int(np.argmax(ar))
    P = Polygon(rings2d[o], [r for i, r in enumerate(rings2d) if i != o and len(r) >= 3])
    if not P.is_valid or P.area <= 0:
        return None
    T = shapely.constrained_delaunay_triangles(P)
    key = {}
    for i, p in enumerate(pts):
        key.setdefault((round(float(p[0]), 7), round(float(p[1]), 7)), i)
    tris = []
    for g in T.geoms:
        c = list(g.exterior.coords)[:3]
        try:
            tris.append([key[(round(x, 7), round(y, 7))] for x, y in c])
        except KeyError:
            return None
    return tris


def _fan(pts3):
    """fallback: fan from the middle of the loop (adds one point)"""
    c = pts3.mean(0)
    n = len(pts3)
    return np.vstack([pts3, c]), [[i, (i + 1) % n, n] for i in range(n)]


def mesh(d, seg_deg=30.0, min_r=12.0, stats=None):
    """one SAB solid -> (V Nx3 in file units, F Mx3), every edge sampled once so neighbours share its points"""
    stats = {} if stats is None else stats
    _hdr, E = sabread.records(d)[:2]

    def ent(p):
        return E[p] if p >= 0 else None

    def pt(vi):
        return np.array(ent(E[vi][1][2][1])[1][1][1], float)
    ecache = {}

    def edge_pts(ei):
        if ei not in ecache:
            t = E[ei][1]
            c = Curve(ent(t[4][1])[1])
            p = c.sample(seg_deg, min_r)
            if t[5][1]:
                p = p[::-1]
            p = p.copy()
            p[0], p[-1] = pt(t[1][1]), pt(t[2][1])
            ecache[ei] = p
        return ecache[ei]
    V, F = [], []
    nv = 0
    for nm, t in E:
        if nm != "face":
            continue
        su = ent(t[5][1])
        rings = []
        lp = ent(t[2][1])
        while lp is not None:
            c0 = lp[1][2][1]
            c = c0
            ring = []
            guard = 0
            while True:
                ct = E[c][1]
                p = edge_pts(ct[4][1])
                if ct[5][1]:
                    p = p[::-1]
                ring.append(p[:-1])
                c = ct[1][1]
                guard += 1
                if c == c0 or guard > 100000:
                    break
            r = np.vstack(ring)
            keep = [0] + [i for i in range(1, len(r)) if np.linalg.norm(r[i] - r[i - 1]) > 1e-6]
            r = r[keep]
            if len(r) > 1 and np.linalg.norm(r[0] - r[-1]) <= 1e-6:
                r = r[:-1]
            if len(r) >= 3:
                rings.append(r)
            lp = ent(lp[1][1][1])
        if not rings:
            stats["empty"] = stats.get("empty", 0) + 1
            continue
        P3 = np.vstack(rings)
        tris = None
        gref = None
        if su[0] == "plane-surface":
            n = np.array(su[1][2][1], float)
            a, b = _plane_basis(n)
            o = np.array(su[1][1][1], float)
            tris = _cdt([np.stack([(r - o) @ a, (r - o) @ b], axis=1) for r in rings])
            kind = "plane"
        else:
            kind = "spline"
            try:
                s = Surf(su[1])
                us = np.linspace(s.ku[s.du], s.ku[s.nu], 25 if s.du > 1 else 3)
                vs = np.linspace(s.kv[s.dv], s.kv[s.nv], 25 if s.dv > 1 else 3)
                G = s.grid(us, vs)
                gn = np.cross(np.gradient(G, axis=1), np.gradient(G, axis=0)).reshape(-1, 3)
                if su[1][1][1]:
                    gn = -gn
                gref = (G.reshape(-1, 3), gn)
                lu = np.linalg.norm(np.diff(G, axis=1), axis=2).sum(1).mean()       # true lengths along u, v
                lv = np.linalg.norm(np.diff(G, axis=0), axis=2).sum(1).mean()
                su_ = lu / max(us[-1] - us[0], 1e-12)
                sv_ = lv / max(vs[-1] - vs[0], 1e-12)
                flat = G.reshape(-1, 3)
                uvr = []
                for r in rings:
                    q = []
                    for p in r:
                        k = int(np.argmin(((flat - p) ** 2).sum(1)))
                        iv, iu = divmod(k, len(us))
                        u, v = us[iu], vs[iv]
                        du_, dv_ = (us[1] - us[0]), (vs[1] - vs[0])
                        for _ in range(4):                    # refine on a shrinking 5 x 5 patch round the best point
                            uu = np.clip(np.linspace(u - du_, u + du_, 5), us[0], us[-1])
                            vv = np.clip(np.linspace(v - dv_, v + dv_, 5), vs[0], vs[-1])
                            g = s.grid(uu, vv).reshape(-1, 3)
                            k2 = int(np.argmin(((g - p) ** 2).sum(1)))
                            b2, a2 = divmod(k2, 5)
                            u, v = uu[a2], vv[b2]
                            du_ /= 2.5
                            dv_ /= 2.5
                        q.append((u * su_, v * sv_))
                    uvr.append(np.array(q))
                tris = _cdt(uvr)
            except Exception as ex:
                stats["spline_err"] = stats.get("spline_err", 0) + 1
                stats.setdefault("spline_err_first", str(ex)[:120])
        if tris is None:                                   # no clean outline in the plane / parameter plane
            n = np.zeros(3)
            for r in rings[:1]:
                c = r.mean(0)
                for i in range(len(r)):
                    n += np.cross(r[i] - c, r[(i + 1) % len(r)] - c)
            if np.linalg.norm(n) > 1e-9 and len(rings) == 1:
                a, b = _plane_basis(n)
                tris = _cdt([np.stack([(rings[0] - rings[0].mean(0)) @ a, (rings[0] - rings[0].mean(0)) @ b], axis=1)])
            if tris is None:
                P3, tris = _fan(rings[0])
                stats[kind + "_fan"] = stats.get(kind + "_fan", 0) + 1
            else:
                stats[kind + "_bestplane"] = stats.get(kind + "_bestplane", 0) + 1
        else:
            stats[kind] = stats.get(kind, 0) + 1
        tris = np.array(tris, int)
        tn = np.cross(P3[tris[:, 1]] - P3[tris[:, 0]], P3[tris[:, 2]] - P3[tris[:, 0]])
        if su[0] == "plane-surface":
            ref = np.tile(np.array(su[1][2][1], float), (len(tris), 1))
        elif gref is not None:
            cen = P3[tris].mean(1)
            ref = gref[1][[int(np.argmin(((gref[0] - c) ** 2).sum(1))) for c in cen]]
        else:
            ref = None
            stats["no_ref"] = stats.get("no_ref", 0) + 1
        if ref is not None:
            if t[6][1]:
                ref = -ref
            flip = (tn * ref).sum(1) < 0
            tris[flip] = tris[flip][:, ::-1]
        V.append(P3)
        F += [[i + nv for i in tr] for tr in tris.tolist()]
        nv += len(P3)
    if not V:
        return np.zeros((0, 3)), np.zeros((0, 3), int)
    return np.vstack(V), np.array(F, int)
