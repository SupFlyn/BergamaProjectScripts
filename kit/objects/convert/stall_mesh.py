import pickle, sys, collections, time
import numpy as np, trimesh
sys.path.insert(0, sys.argv[2])
import acis_mesh, mesh2gdl
recs = pickle.load(open(sys.argv[1], "rb"))
seg = float(sys.argv[4]) if len(sys.argv) > 4 else 30.0
minr = float(sys.argv[5]) if len(sys.argv) > 5 else 12.0
st = {}; vol = []; cons = 0; out = []; t0 = time.time(); nw = 0; tot = 0
for h, d in recs:
    V, F = acis_mesh.mesh(d, seg, minr, st)
    Vw, Fw, _a, _b = mesh2gdl.weld(V, F, 1e-3)
    m = trimesh.Trimesh(Vw, Fw, process=False)
    wt = bool(m.is_watertight)
    if wt:
        vol.append(float(m.volume)); cons += bool(m.is_winding_consistent)
    nw += wt; tot += len(m.faces)
    out.append(dict(handle=h, V=np.asarray(m.vertices), F=np.asarray(m.faces), watertight=wt, volume=float(m.volume) if wt else None))
print("solids", len(out), "watertight", nw, "triangles", tot, "time %.0f s" % (time.time() - t0))
print("faces by method", st)
print("watertight solids: volume > 0:", sum(v > 0 for v in vol), "< 0:", sum(v < 0 for v in vol), "winding consistent:", cons)
for o in out: o["bbox"] = (o["V"].min(0), o["V"].max(0))
bad = [(o["handle"], len(o["F"])) for o in out if not o["watertight"]]
print("not watertight:", bad[:20])
pickle.dump(out, open(sys.argv[3], "wb"))
