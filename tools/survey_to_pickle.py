"""Read a Rhino survey file once (rhino3dm) into a small pickle the fake Rhino doc loads fast.
usage: python3 tools/survey_to_pickle.py <file.3dm> <out.pkl>"""
import sys, pickle, math, rhino3dm
m = rhino3dm.File3dm.Read(sys.argv[1])
P = lambda p: (p.X, p.Y, p.Z)
layers = [dict(name=l.Name, full=l.FullPath, index=l.Index, id=str(l.Id), parent=str(l.ParentLayerId)) for l in m.Layers]
objs = []
for o in m.Objects:
    g = o.Geometry; a = o.Attributes; k = type(g).__name__
    rec = dict(id=str(a.Id), layer=a.LayerIndex, name=a.Name or "", us={u[0]: u[1] for u in (a.GetUserStrings() or [])} if hasattr(a, "GetUserStrings") else {})
    if k == "LineCurve":
        rec.update(t="line", pts=[P(g.PointAtStart), P(g.PointAtEnd)])
    elif k == "PolylineCurve":
        rec.update(t="pline", pts=[P(g.Point(i)) for i in range(g.PointCount)])
    elif k == "ArcCurve":
        arc = g.Arc
        pl = arc.Plane
        rec.update(t="arc", c=P(arc.Center), r=arc.Radius, x=P(pl.XAxis), y=P(pl.YAxis),
                   a0=arc.AngleDomain.T0, a1=arc.AngleDomain.T1, circle=bool(g.IsCompleteCircle))
    elif k == "Point":
        rec.update(t="point", p=P(g.Location))
    elif k == "Text":
        pl = g.Plane
        try:
            ds = m.DimStyles.FindId(g.DimensionStyleId)
            b = g.GetBoundingBox(ds); h = g.GetTextHeight(ds)
            bmin, bmax = P(b.Min), P(b.Max)
        except Exception:                      # approximate box: origin + text run along the x axis
            h = 1.0; bmin = bmax = None
        rec.update(t="text", s=g.PlainText, o=P(pl.Origin), x=P(pl.XAxis), y=P(pl.YAxis), h=h, bmin=bmin, bmax=bmax)
    else:
        continue
    objs.append(rec)
pickle.dump(dict(units="Meters", layers=layers, objs=objs, source=sys.argv[1]), open(sys.argv[2], "wb"), protocol=4)
print(len(layers), "layers,", len(objs), "objects")
