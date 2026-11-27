# Aras's kiosk (.glb) -> GDL mesh object: small props thinned, flat colours per group, and one texture atlas
import sys, json, numpy as np, trimesh, fast_simplification
from PIL import Image
from scipy.spatial import cKDTree
sys.path.insert(0, sys.argv[3])
import mesh2gdl, colors
glb, out = sys.argv[1], sys.argv[2]
BUDGET = int(sys.argv[4]) if len(sys.argv) > 4 else 30000
ATLAS = int(sys.argv[5]) if len(sys.argv) > 5 else 2048
MINF = 48
sc = trimesh.load(glb, process=False)
nodes, texs = [], {}
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
        uv = np.asarray(uv, float)
        C = colors.face_rgb(tex, uv, F) * fac[None, :3]
        UVc = uv[F]
    else:
        C = np.tile(fac[:3], (len(F), 1))
        UVc = np.full((len(F), 3, 2), 0.5)
        tex = None
    key = mat.name
    if key not in texs:
        texs[key] = dict(img=tex, fac=fac[:3], area=0.0)
    glass = getattr(mat, "alphaMode", None) == "BLEND"
    A = colors.areas(V, F)
    if not glass:
        texs[key]["area"] += float(A.sum())
    nodes.append(dict(name=nd, mat=key, V=V, F=F, C=C, UV=UVc, glass=glass, area=float(A.sum())))
tot0 = sum(len(n["F"]) for n in nodes)
uvall = np.vstack([n["UV"].reshape(-1, 2) for n in nodes])
print("uv range", uvall.min(0).round(3), uvall.max(0).round(3))
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
        T0 = n["V"][n["F"]]                               # the old triangles: each new one takes the texture
        _d, ix = cKDTree(T0.mean(1)).query(V2[F2].mean(1))   # map of the old one nearest to its middle
        P = V2[F2]                                        # M x 3 x 3
        a0, e1, e2 = T0[ix][:, 0], T0[ix][:, 1] - T0[ix][:, 0], T0[ix][:, 2] - T0[ix][:, 0]
        d11, d12, d22 = (e1 * e1).sum(1), (e1 * e2).sum(1), (e2 * e2).sum(1)
        den = d11 * d22 - d12 * d12
        den[np.abs(den) < 1e-18] = 1e-18
        uv0 = n["UV"][ix]                                  # M x 3 x 2
        lo, hi = uv0.min(1) - 0.02, uv0.max(1) + 0.02
        UVn = np.zeros((len(F2), 3, 2))
        for c in range(3):
            r = P[:, c] - a0
            p1, p2 = (r * e1).sum(1), (r * e2).sum(1)
            b1 = (d22 * p1 - d12 * p2) / den
            b2 = (d11 * p2 - d12 * p1) / den
            q = uv0[:, 0] + b1[:, None] * (uv0[:, 1] - uv0[:, 0]) + b2[:, None] * (uv0[:, 2] - uv0[:, 0])
            UVn[:, c] = np.clip(q, lo, hi)
        n["C"] = n["C"][ix]; n["V"], n["F"], n["UV"] = V2, F2, UVn
# the atlas: one cell per texture, its size by the surface that carries it
SIGNS = ("coffee_shop", "banner", "menu_stand", "poster")   # lettering: these get a large cell whatever their surface
order = sorted(texs, key=lambda k: -(texs[k]["area"] + (5.0 if k in SIGNS else 0.0)))


def pack(sizes):
    pos, x, y, rowh = {}, 0, 0, 0
    for k, z in sorted(zip(order, sizes), key=lambda kz: -kz[1]):
        if x + z > ATLAS:
            x, y, rowh = 0, y + rowh, 0
        if y + z > ATLAS:
            return None, 0
        pos[k] = (x, y, z)
        x += z
        rowh = max(rowh, z)
    return pos, y + rowh


cells = None
for scheme in ((1, 6, 10, 8), (1, 5, 10, 8), (1, 4, 10, 8), (0, 7, 10, 8), (0, 4, 12, 8), (0, 0, 12, 12)):
    sizes, r = [], 0
    for k in order:
        if texs[k]["img"] is None:
            sizes.append(16)
            continue
        sizes.append(1024 if r < scheme[0] else 512 if r < sum(scheme[:2]) else 256 if r < sum(scheme[:3]) else
                     128 if r < sum(scheme) else 64)
        r += 1
    if ATLAS < 2048:
        sizes = [max(16, z // (2048 // ATLAS)) for z in sizes]
    cells, used_h = pack(sizes)
    if cells:
        break
if not cells:
    raise SystemExit("atlas full")
atlas = Image.new("RGB", (ATLAS, ATLAS), (128, 128, 128))
for k in order:
    x, y, z = cells[k]
    t = texs[k]
    if t["img"] is None:
        im = Image.new("RGB", (z, z), tuple(int(255 * c) for c in t["fac"]))
    else:
        im = t["img"].convert("RGB").resize((z, z), Image.LANCZOS)
        if not np.allclose(t["fac"], 1.0):
            im = Image.fromarray((np.asarray(im, float) * t["fac"][None, None, :]).clip(0, 255).astype(np.uint8))
    atlas.paste(im, (x, y))
print("largest cells:", [(k, cells[k][2], round(texs[k]["area"], 2)) for k in order[:8]])
print("atlas", ATLAS, "used height", used_h, "cells", len(cells), "sizes", sorted(set(sizes), reverse=True))
atlas.save(out.replace(".gdl", ".png"), optimize=True)
for n in nodes:                                           # texture coordinates -> atlas coordinates (v up)
    cx, cy, z = cells[n["mat"]]
    uv = n["UV"].copy()
    uv -= np.floor(uv.mean(1))[:, None, :]                 # a repeated texture: the triangle's own tile
    uv = np.clip(uv, 0.0, 1.0)
    half = 0.5 / z
    uv = half + uv * (1 - 2 * half)                        # stay inside the cell
    n["UVa"] = np.stack([(cx + uv[:, :, 0] * z) / ATLAS, 1.0 - (cy + (1.0 - uv[:, :, 1]) * z) / ATLAS], axis=2)
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
    UV = np.vstack([n["UVa"] for n in sel])
    A = colors.areas(V, F)
    lab, cols = colors.palette(C, A, k, merge=0.07)
    for j in sorted(set(lab.tolist()), key=lambda j: -A[lab == j].sum()):
        m = lab == j
        groups.append(dict(name="%s%d" % ("glass" if glass else "c", j), rgb=[float(x) for x in cols[j]], kind="glass" if glass else "matte",
                           V=V, F=F[m], UV=None if glass else UV[m]))
        print("%s colour %s tris %5d area %.2f m2" % ("glass" if glass else "matte", [round(float(x), 2) for x in cols[j]], int(m.sum()), A[m].sum()))
txt, info = mesh2gdl.script("Food Kiosk", [dict(g, UV=None) for g in groups])
open(out, "w", encoding="utf-8", newline="\n").write(txt)
txt2, info2 = mesh2gdl.script("Food Kiosk", groups, texture="food_kiosk.png")
open(out.replace(".gdl", "_tex.gdl"), "w", encoding="utf-8", newline="\n").write(txt2)
print("triangles %d -> %d" % (tot0, info["triangles"]), info, "size", (mx - mn).round(3), "bytes", len(txt), "textured bytes", len(txt2))
