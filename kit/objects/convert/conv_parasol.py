import sys, json, numpy as np, assimp_py
from PIL import Image
sys.path.insert(0, sys.argv[4])
import mesh2gdl, colors
fbx, tex, out = sys.argv[1], sys.argv[2], sys.argv[3]
sc = assimp_py.import_file(fbx, assimp_py.Process_Triangulate | assimp_py.Process_PreTransformVertices)
m = sc.meshes[0]
V = np.array(m.vertices).reshape(-1, 3)
F = np.array(m.indices).reshape(-1, 3)
UV = np.array(m.texcoords[0]).reshape(len(V), -1)[:, :2]
print("raw", len(V), len(F), "uv", UV.min(0), UV.max(0))
V = np.stack([V[:, 0], -V[:, 2], V[:, 1]], axis=1) * 0.01          # cm, Y up -> m, Z up
mn, mx = V.min(0), V.max(0)
V[:, 0] -= (mn[0] + mx[0]) / 2; V[:, 1] -= (mn[1] + mx[1]) / 2; V[:, 2] -= mn[2]
C = colors.face_rgb(Image.open(tex), UV, F)
A = colors.areas(V, F)
lab, cols = colors.palette(C, A, 6)
groups = []
for j in sorted(set(lab.tolist()), key=lambda j: -A[lab == j].sum()):
    msk = lab == j
    groups.append(dict(name="c%d" % j, rgb=[float(x) for x in cols[j]], kind="matte", V=V, F=F[msk], UV=UV[F[msk]]))
    zz = V[F[msk]].reshape(-1, 3)
    print("colour", [round(float(x), 3) for x in cols[j]], "tris", int(msk.sum()), "area %.2f m2" % A[msk].sum(), "z %.2f..%.2f" % (zz[:, 2].min(), zz[:, 2].max()))
txt, info = mesh2gdl.script("Market Umbrella White", groups)
open(out, "w", encoding="utf-8", newline="\n").write(txt)
txt2, info2 = mesh2gdl.script("Market Umbrella White", groups, texture="market_umbrella_white.png")
open(out.replace(".gdl", "_tex.gdl"), "w", encoding="utf-8", newline="\n").write(txt2)
Image.open(tex).convert("RGB").save(out.replace(".gdl", ".png"), optimize=True)
print("textured", info2, "bytes", len(txt2))
print(info, "size", (V.max(0) - V.min(0)).round(3), "bytes", len(txt))
