import sys, json, numpy as np, trimesh, fast_simplification
from scipy.spatial import cKDTree
sys.path.insert(0, sys.argv[3])
import mesh2gdl, colors
glb, out = sys.argv[1], sys.argv[2]
BUDGET = int(sys.argv[4]) if len(sys.argv) > 4 else 30000
MINF = 48
sc = trimesh.load(glb, process=False)
nodes = []
for nd in sorted(sc.graph.nodes_geometry):
    T, gn = sc.graph[nd]
    g = sc.geometry[gn]
    V = trimesh.transform_points(g.vertices, T)
    V = np.stack([V[:, 0], -V[:, 2], V[:, 1]], axis=1)             # glTF Y up -> Z up, metres
    F = np.asarray(g.faces)
    if np.linalg.det(T[:3, :3]) < 0:
        F = F[:, ::-1]
    mat = g.visual.material
    tex = getattr(mat, "baseColorTexture", None)
    fac = getattr(mat, "baseColorFactor", None)
    fac = np.array([1, 1, 1, 1.0]) if fac is None else np.asarray(fac, float) / 255.0
    uv = getattr(g.visual, "uv", None)
    if tex is not None and uv is not None:
        C = colors.face_rgb(tex, np.asarray(uv), F) * fac[None, :3]
    else:
        C = np.tile(fac[:3], (len(F), 1))
    glass = getattr(mat, "alphaMode", None) == "BLEND"
    nodes.append(dict(name=nd, mat=mat.name, V=V, F=F, C=C, glass=glass, area=float(colors.areas(V, F).sum())))
tot0 = sum(len(n["F"]) for n in nodes)
# faces allowed per node: by the root of its surface, never under MINF, never more than it has
w = np.array([n["area"] ** 0.5 for n in nodes])
allow = np.array([len(n["F"]) for n in nodes], float)
free = np.ones(len(nodes), bool)
for _ in range(20):
    rest = BUDGET - allow[~free].sum()
    t = np.maximum(MINF, rest * w / w[free].sum())
    newly = free & (t >= allow)
    if not newly.any():
        break
    free &= ~newly
allow[free] = np.maximum(MINF, (BUDGET - allow[~free].sum()) * w[free] / w[free].sum())
for n, a in zip(nodes, allow):
    a = int(min(len(n["F"]), a))
    if a < len(n["F"]):
        Vw, Fw, _o, _k = mesh2gdl.weld(n["V"], n["F"])
        V2, F2 = fast_simplification.simplify(Vw.astype(np.float32), Fw.astype(np.int32), target_count=a, agg=5)
        V2 = np.asarray(V2, float); F2 = np.asarray(F2, int)
        cen0 = n["V"][n["F"]].mean(1)
        _d, ix = cKDTree(cen0).query(V2[F2].mean(1))
        n["C"] = n["C"][ix]; n["V"], n["F"] = V2, F2
allV = np.vstack([n["V"] for n in nodes])
mn, mx = allV.min(0), allV.max(0)
off = np.array([(mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2, mn[2]])
groups = []
for glass, k in ((False, 20), (True, 3)):
    sel = [n for n in nodes if n["glass"] == glass]
    if not sel:
        continue
    base = np.cumsum([0] + [len(n["V"]) for n in sel])
    V = np.vstack([n["V"] for n in sel]) - off
    F = np.vstack([n["F"] + b for n, b in zip(sel, base)])
    C = np.vstack([n["C"] for n in sel])
    A = colors.areas(V, F)
    lab, cols = colors.palette(C, A, k, merge=0.07)
    for j in sorted(set(lab.tolist()), key=lambda j: -A[lab == j].sum()):
        m = lab == j
        groups.append(dict(name="%s%d" % ("glass" if glass else "c", j), rgb=[float(x) for x in cols[j]], kind="glass" if glass else "matte", V=V, F=F[m]))
        print("%s colour %s tris %5d area %.2f m2" % ("glass" if glass else "matte", [round(float(x), 2) for x in cols[j]], int(m.sum()), A[m].sum()))
txt, info = mesh2gdl.script("Food Kiosk", groups)
open(out, "w", encoding="utf-8", newline="\n").write(txt)
print("triangles %d -> %d" % (tot0, info["triangles"]), info, "size", (mx - mn).round(3), "bytes", len(txt))
