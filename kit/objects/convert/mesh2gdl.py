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


def script(part, groups):
    """groups: [dict(name, rgb (0..1), kind 'matte' | 'metal' | 'glass', V, F)] -> (GDL 3D text, summary)"""
    kinds = {"matte": 2, "metal": 3, "plastic": 4, "glass": 5}
    L = ["! %s: mesh object made from Aras's file, sizes in m, origin at the middle of its footprint on the ground" % part]
    tv = tf = 0
    for i, g in enumerate(groups):
        lines, nv, nf = body(g["V"], g["F"])
        if not nf:
            continue
        mn = "%s %02d" % (part, i + 1)
        L.append('DEFINE MATERIAL "%s" %d, %.3f, %.3f, %.3f' % (mn, kinds[g.get("kind", "matte")], g["rgb"][0], g["rgb"][1], g["rgb"][2]))
        L.append('MATERIAL "%s"' % mn)
        L += lines
        tv += nv
        tf += nf
    return "\n".join(L) + "\n", dict(vertices=tv, triangles=tf, lines=len(L))
