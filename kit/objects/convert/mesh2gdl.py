# mesh groups -> GDL 3D script text (VERT / VECT / EDGE / PGON bodies, one per colour)
import math
import numpy as np


def weld(V, F, tol=1e-4):
    """vertices closer than tol are one; triangles with a doubled corner or no area, and doubled triangles, are dropped"""
    V = np.asarray(V, float)
    F = np.asarray(F, int)
    key = np.round(V / tol).astype(np.int64)
    _u, idx, inv = np.unique(key, axis=0, return_index=True, return_inverse=True)
    V2 = V[idx]
    F2 = inv.reshape(-1)[F]
    ok = (F2[:, 0] != F2[:, 1]) & (F2[:, 1] != F2[:, 2]) & (F2[:, 0] != F2[:, 2])
    F2 = F2[ok]
    n = np.cross(V2[F2[:, 1]] - V2[F2[:, 0]], V2[F2[:, 2]] - V2[F2[:, 0]])
    a = np.linalg.norm(n, axis=1)
    keep = a > 1e-10
    F2 = F2[keep]
    s = np.sort(F2, axis=1)
    _u, first = np.unique(s, axis=0, return_index=True)
    F2 = F2[np.sort(first)]
    used = np.unique(F2)
    remap = -np.ones(len(V2), int)
    remap[used] = np.arange(len(used))
    return V2[used], remap[F2], ok, keep


def body(V, F, smooth_deg=35.0, flat_deg=1.0):
    """GDL lines of one body: indices start at 1 after BASE"""
    V, F, _a, _b = weld(V, F)
    if not len(F):
        return [], 0, 0
    N = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    N /= np.linalg.norm(N, axis=1)[:, None]
    recs = []                       # [a, b, face forward, face backward]
    by = {}
    fe = []
    for fi, (a, b, c) in enumerate(F):
        row = []
        for p, q in ((a, b), (b, c), (c, a)):
            k = (p, q) if p < q else (q, p)
            got = None
            for ri in by.get(k, ()):
                r = recs[ri]
                if r[0] == p and r[1] == q and r[2] < 0:
                    r[2] = fi
                    got = ri + 1
                    break
                if r[0] == q and r[1] == p and r[3] < 0:
                    r[3] = fi
                    got = -(ri + 1)
                    break
            if got is None:
                recs.append([p, q, fi, -1])
                by.setdefault(k, []).append(len(recs) - 1)
                got = len(recs)
            row.append(got)
        fe.append(row)
    cs, cf = math.cos(math.radians(smooth_deg)), math.cos(math.radians(flat_deg))
    est = []
    curved = np.zeros(len(F), bool)
    for a, b, f1, f2 in recs:
        st = 0
        if f1 >= 0 and f2 >= 0:
            d = float(np.dot(N[f1], N[f2]))
            if d >= cf:
                st = 1                                   # two triangles of one flat face: no line between them
            elif d >= cs:
                st = 2                                   # a rounded surface: a line only on its outline
                curved[f1] = curved[f2] = True
        est.append(st)
    L = ["BASE"]
    L += ["VERT %.4f, %.4f, %.4f" % tuple(v) for v in V]
    L += ["VECT %.4f, %.4f, %.4f" % tuple(n) for n in N]
    L += ["EDGE %d, %d, -1, -1, %d" % (r[0] + 1, r[1] + 1, s) for r, s in zip(recs, est)]
    L += ["PGON 3, %d, %d, %d, %d, %d" % (fi + 1, 2 if curved[fi] else 0, e[0], e[1], e[2]) for fi, e in enumerate(fe)]
    L.append("BODY -1")
    return L, len(V), len(F)


def body_uv(V, F, UV, smooth_deg=35.0, flat_deg=1.0):
    """as body(), each triangle with its own texture coordinates: UV is M x 3 x 2 (one u, v per corner), written
    per polygon (PGON{3}, wrap method 0, flag 4) so that corners on a texture seam stay one vertex"""
    V = np.asarray(V, float)
    F = np.asarray(F, int)
    UV = np.asarray(UV, float)
    key = np.round(V / 1e-4).astype(np.int64)
    _u, idx, inv = np.unique(key, axis=0, return_index=True, return_inverse=True)
    V = V[idx]
    F = inv.reshape(-1)[F]
    ok = (F[:, 0] != F[:, 1]) & (F[:, 1] != F[:, 2]) & (F[:, 0] != F[:, 2])
    F, UV = F[ok], UV[ok]
    N = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    a = np.linalg.norm(N, axis=1)
    keep = a > 1e-10
    F, UV, N = F[keep], UV[keep], N[keep] / a[keep][:, None]
    _u, first = np.unique(np.sort(F, axis=1), axis=0, return_index=True)
    first = np.sort(first)
    F, UV, N = F[first], UV[first], N[first]
    if not len(F):
        return [], 0, 0
    used = np.unique(F)
    remap = -np.ones(len(V), int)
    remap[used] = np.arange(len(used))
    V, F = V[used], remap[F]
    recs, by, fe = [], {}, []
    for fi, (a_, b_, c_) in enumerate(F):
        row = []
        for p, q in ((a_, b_), (b_, c_), (c_, a_)):
            k = (p, q) if p < q else (q, p)
            got = None
            for ri in by.get(k, ()):
                r = recs[ri]
                if r[0] == p and r[1] == q and r[2] < 0:
                    r[2] = fi
                    got = ri + 1
                    break
                if r[0] == q and r[1] == p and r[3] < 0:
                    r[3] = fi
                    got = -(ri + 1)
                    break
            if got is None:
                recs.append([p, q, fi, -1])
                by.setdefault(k, []).append(len(recs) - 1)
                got = len(recs)
            row.append(got)
        fe.append(row)
    cs, cf = math.cos(math.radians(smooth_deg)), math.cos(math.radians(flat_deg))
    est = []
    curved = np.zeros(len(F), bool)
    for _a, _b, f1, f2 in recs:
        st = 0
        if f1 >= 0 and f2 >= 0:
            d = float(np.dot(N[f1], N[f2]))
            if d >= cf:
                st = 1
            elif d >= cs:
                st = 2
                curved[f1] = curved[f2] = True
        est.append(st)
    L = ["BASE"]
    L += ["VERT %.4f, %.4f, %.4f" % tuple(v) for v in V]
    L += ["VECT %.4f, %.4f, %.4f" % tuple(n) for n in N]
    L += ["EDGE %d, %d, -1, -1, %d" % (r[0] + 1, r[1] + 1, s) for r, s in zip(recs, est)]
    L += ["PGON{3} 3, %d, %d, 0, 4, %d, %.4f, %.4f, %d, %.4f, %.4f, %d, %.4f, %.4f" % (
        fi + 1, 2 if curved[fi] else 0, e[0], UV[fi][0][0], UV[fi][0][1], e[1], UV[fi][1][0], UV[fi][1][1],
        e[2], UV[fi][2][0], UV[fi][2][1]) for fi, e in enumerate(fe)]
    L.append("BODY -1")
    return L, len(V), len(F)


def script(part, groups, texture=None):
    """groups: [dict(name, rgb (0..1), kind 'matte' | 'metal' | 'glass', V, F[, UV])] -> (GDL 3D text, summary);
    texture = the index of the picture stored in the part (1 = its first): groups with UV get it on their surface"""
    kinds = {"matte": 2, "metal": 3, "plastic": 4, "glass": 5}
    L = ["! %s: mesh object made from Aras's file, sizes in m, origin at the middle of its footprint on the ground" % part]
    if texture:
        L.append('DEFINE TEXTURE "%s tex" %d, 1, 1, 0, 0' % (part, texture))
    tv = tf = 0
    for i, g in enumerate(groups):
        uv = texture and g.get("UV") is not None
        lines, nv, nf = body_uv(g["V"], g["F"], g["UV"]) if uv else body(g["V"], g["F"])
        if not nf:
            continue
        mn = "%s %02d" % (part, i + 1)
        if uv:
            L.append('DEFINE MATERIAL "%s" %d, %.3f, %.3f, %.3f, 0, 0, IND(TEXTURE, "%s tex")' % (
                mn, 20 + kinds[g.get("kind", "matte")], g["rgb"][0], g["rgb"][1], g["rgb"][2], part))
        else:
            L.append('DEFINE MATERIAL "%s" %d, %.3f, %.3f, %.3f' % (mn, kinds[g.get("kind", "matte")], g["rgb"][0], g["rgb"][1], g["rgb"][2]))
        L.append('MATERIAL "%s"' % mn)
        L += lines
        tv += nv
        tf += nf
    return "\n".join(L) + "\n", dict(vertices=tv, triangles=tf, lines=len(L))


def outline2d(groups, tol=0.01):
    """GDL 2D text: the top-view outline of all triangles (their union, simplified to tol m), as contour lines"""
    import shapely
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    P = []
    for g in groups:
        V, F = np.asarray(g["V"], float), np.asarray(g["F"], int)
        for a, b, c in F:
            t = Polygon([V[a][:2], V[b][:2], V[c][:2]])
            if t.area > 1e-8:
                P.append(t)
    U = unary_union([p.buffer(0.001) for p in P]).buffer(-0.001).simplify(tol)
    L = ["HOTSPOT2 0, 0"]
    n = 0
    for poly in getattr(U, "geoms", [U]):
        for ring in [poly.exterior] + list(poly.interiors):
            c = list(ring.coords)[:-1]
            if len(c) < 3:
                continue
            L.append("POLY2 %d, 1," % len(c))
            L += ["    %.3f, %.3f%s" % (x, y, "," if i < len(c) - 1 else "") for i, (x, y) in enumerate(c)]
            n += 1
    mnx, mny, mxx, mxy = U.bounds
    for x, y in ((mnx, mny), (mxx, mny), (mxx, mxy), (mnx, mxy)):
        L.append("HOTSPOT2 %.3f, %.3f" % (x, y))
    return "\n".join(L) + "\n", n
