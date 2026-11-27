import sys, pickle, numpy as np
sys.path.insert(0, sys.argv[4])
import mesh2gdl
solids = pickle.load(open(sys.argv[1], "rb"))
# colours: the 3D .dwg carries none (all 115 solids on one layer, colour by layer). ASSUMED from the look noted in the
# research answer (ANSWER_archicad_objects_v7.md: "Red steel shelter: double-pitched sheet roof on a row of posts with
# Y-struts, long timber table under the ridge"): the two table tops timber, everything else red steel; shades ASSUMED
RED, TIMBER = (0.62, 0.12, 0.11), (0.72, 0.56, 0.38)
gr = {"steel": ([], [], 0), "timber": ([], [], 0)}
nv = {"steel": 0, "timber": 0}
names = []
for o in solids:
    V = o["V"] / 1000.0                                  # mm -> m
    V = np.stack([V[:, 1], -V[:, 0], V[:, 2]], axis=1)   # its length along x
    sz = np.round((o["V"].max(0) - o["V"].min(0))).astype(int)
    k = "timber" if (sz[0], sz[1], sz[2]) == (900, 2700, 40) else "steel"
    gr[k][0].append(V); gr[k][1].append(o["F"] + nv[k]); nv[k] += len(V)
groups = []
for k, rgb in (("steel", RED), ("timber", TIMBER)):
    V = np.vstack(gr[k][0]); F = np.vstack(gr[k][1])
    groups.append(dict(name=k, rgb=rgb, kind="matte", V=V, F=F))
    print(k, "solids", len(gr[k][0]), "tris", len(F))
allV = np.vstack([g["V"] for g in groups]); mn, mx = allV.min(0), allV.max(0)
off = np.array([(mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2, mn[2]])
for g in groups: g["V"] = g["V"] - off
txt, info = mesh2gdl.script("Market Stall Shelter", groups)
open(sys.argv[2], "w", encoding="utf-8", newline="\n").write(txt)
t2, n2 = mesh2gdl.outline2d(groups)
rx = [g_ for g_ in gr["steel"][0] if abs((g_[:, 0].max() - g_[:, 0].min()) - 2.930) < 0.002 and abs((g_[:, 1].max() - g_[:, 1].min()) - 0.542) < 0.002]
x0, x1 = min(g_[:, 0].min() for g_ in rx) - off[0], max(g_[:, 0].max() for g_ in rx) - off[0]   # the two ridge beams
t2 += "LINE2 %.3f, 0, %.3f, 0\n" % (x0, x1)
print("ridge line", round(x0, 3), round(x1, 3), "from", len(rx), "ridge beams")
open(sys.argv[3], "w", encoding="utf-8", newline="\n").write(t2)
print(info, "size", (mx - mn).round(3), "offset", off.round(4), "bytes", len(txt), "2D rings", n2, "2D bytes", len(t2))
