"""A small stand-in for RhinoCommon, enough to run the Bergama scripts offline on the real survey file.

Not Rhino: geometry is polylines only, text boxes are points, anything not written here is a MagicMock.
It exists for old-vs-new regression runs (same input -> same output files), not to reproduce Rhino exactly.
install(pickle_path or None) puts Rhino, Rhino.Geometry, scriptcontext, System ... into sys.modules."""
import sys, os, math, types, pickle, uuid
from unittest import mock


# ---------------------------------------------------------------- geometry
class Point3d(object):
    __slots__ = ("X", "Y", "Z")

    def __init__(self, x=0.0, y=0.0, z=0.0):
        if isinstance(x, Point3d):
            x, y, z = x.X, x.Y, x.Z
        self.X, self.Y, self.Z = float(x), float(y), float(z)

    def DistanceTo(self, o):
        return math.sqrt((self.X - o.X) ** 2 + (self.Y - o.Y) ** 2 + (self.Z - o.Z) ** 2)

    def __add__(self, o): return Point3d(self.X + o.X, self.Y + o.Y, self.Z + o.Z)
    def __sub__(self, o): return Vector3d(self.X - o.X, self.Y - o.Y, self.Z - o.Z)
    def __mul__(self, k): return Point3d(self.X * k, self.Y * k, self.Z * k)
    __rmul__ = __mul__
    def __eq__(self, o): return isinstance(o, Point3d) and (self.X, self.Y, self.Z) == (o.X, o.Y, o.Z)
    def __hash__(self): return hash((self.X, self.Y, self.Z))
    def __getitem__(self, i): return (self.X, self.Y, self.Z)[i]
    def __iter__(self): return iter((self.X, self.Y, self.Z))
    def __repr__(self): return "%r,%r,%r" % (self.X, self.Y, self.Z)
    @property
    def IsValid(self): return True


class Vector3d(Point3d):
    __slots__ = ()
    def __sub__(self, o): return Vector3d(self.X - o.X, self.Y - o.Y, self.Z - o.Z)
    @property
    def Length(self): return math.sqrt(self.X ** 2 + self.Y ** 2 + self.Z ** 2)


Point3d.Origin = Point3d(0, 0, 0)
Point3d.Unset = Point3d(-1.23432101234321e+308, -1.23432101234321e+308, -1.23432101234321e+308)
Vector3d.XAxis, Vector3d.YAxis, Vector3d.ZAxis = Vector3d(1, 0, 0), Vector3d(0, 1, 0), Vector3d(0, 0, 1)


class Point2d(Point3d):
    __slots__ = ()


class BoundingBox(object):
    def __init__(self, a=None, b=None):
        if a is not None and b is None:          # from a list of points
            P = list(a)
            a = Point3d(min(p.X for p in P), min(p.Y for p in P), min(p.Z for p in P))
            b = Point3d(max(p.X for p in P), max(p.Y for p in P), max(p.Z for p in P))
        self.Min, self.Max = a, b

    @property
    def IsValid(self): return self.Min is not None
    @property
    def Center(self): return Point3d((self.Min.X + self.Max.X) / 2, (self.Min.Y + self.Max.Y) / 2, (self.Min.Z + self.Max.Z) / 2)

    def Union(self, o):
        if not o.IsValid: return
        if not self.IsValid:
            self.Min, self.Max = o.Min, o.Max; return
        self.Min = Point3d(min(self.Min.X, o.Min.X), min(self.Min.Y, o.Min.Y), min(self.Min.Z, o.Min.Z))
        self.Max = Point3d(max(self.Max.X, o.Max.X), max(self.Max.Y, o.Max.Y), max(self.Max.Z, o.Max.Z))


BoundingBox.Empty = BoundingBox(None, None)


class Interval(object):
    def __init__(self, a, b): self.T0, self.T1 = a, b
    @property
    def Length(self): return self.T1 - self.T0
    @property
    def Min(self): return min(self.T0, self.T1)
    @property
    def Max(self): return max(self.T0, self.T1)


class Polyline(list):
    def __init__(self, pts=()):
        list.__init__(self, [p if isinstance(p, Point3d) else Point3d(*p) for p in pts])
    @property
    def Count(self): return len(self)
    @property
    def IsClosed(self): return len(self) > 2 and self[0].DistanceTo(self[-1]) < 1e-9
    @property
    def Length(self): return sum(self[i].DistanceTo(self[i + 1]) for i in range(len(self) - 1))
    def ToPolylineCurve(self): return PolylineCurve(self)
    def ToNurbsCurve(self): return PolylineCurve(self)
    def Add(self, *a): self.append(a[0] if len(a) == 1 else Point3d(*a))


class GeometryBase(object):
    def Duplicate(self):
        import copy
        return copy.deepcopy(self)
    def GetUserString(self, k): return getattr(self, "_us", {}).get(k)
    def SetUserString(self, k, v):
        self.__dict__.setdefault("_us", {})[k] = v; return True
    @property
    def IsValid(self): return True


class Curve(GeometryBase):
    """A polyline curve. Parameter t runs 0..n segments (as RhinoCommon's PolylineCurve)."""
    def __init__(self, pts=()):
        self._P = [p if isinstance(p, Point3d) else Point3d(*p) for p in pts]

    @property
    def IsClosed(self): return len(self._P) > 2 and self._P[0].DistanceTo(self._P[-1]) < 1e-9
    @property
    def PointAtStart(self): return self._P[0]
    @property
    def PointAtEnd(self): return self._P[-1]
    @property
    def Domain(self): return Interval(0.0, float(len(self._P) - 1))
    @property
    def PointCount(self): return len(self._P)
    def Point(self, i): return self._P[i]
    @property
    def SpanCount(self): return len(self._P) - 1

    def GetBoundingBox(self, *a): return BoundingBox(self._P)
    def GetLength(self, *a): return sum(self._P[i].DistanceTo(self._P[i + 1]) for i in range(len(self._P) - 1))
    def TryGetPolyline(self, *a): return True, Polyline(self._P)
    def IsPolyline(self): return True
    def IsLinear(self, *a): return len(self._P) == 2
    def IsPlanar(self, *a): return True
    def IsArc(self, *a): return False
    def IsCircle(self, *a): return False
    def ToNurbsCurve(self): return self
    def ToPolyline(self, *a): return PolylineCurve(self._P)
    Degree = 1                     # a polyline's NURBS form; ArcCurve says 2
    @property
    def Points(self): return [types.SimpleNamespace(Location=p) for p in self._P]

    def PointAt(self, t):
        n = len(self._P) - 1
        t = max(0.0, min(float(n), t)); i = min(int(t), n - 1) if n > 0 else 0
        if n == 0: return self._P[0]
        f = t - i; a, b = self._P[i], self._P[i + 1]
        return Point3d(a.X + (b.X - a.X) * f, a.Y + (b.Y - a.Y) * f, a.Z + (b.Z - a.Z) * f)

    def _arc_params(self):
        L = [0.0]
        for i in range(len(self._P) - 1):
            L.append(L[-1] + self._P[i].DistanceTo(self._P[i + 1]))
        return L

    def DivideByCount(self, n, ends=True, *a):
        L = self._arc_params(); tot = L[-1]
        if n < 1 or tot <= 0: return None
        out = []
        for k in range(n + 1):
            s = tot * k / n; i = 0
            while i < len(L) - 2 and L[i + 1] < s: i += 1
            seg = L[i + 1] - L[i]
            out.append(i + ((s - L[i]) / seg if seg > 0 else 0.0))
        if not ends: out = out[1:-1]
        elif self.IsClosed: out = out[:-1]
        return out

    def DivideByLength(self, d, ends=True, *a):
        tot = self.GetLength()
        return self.DivideByCount(max(1, int(tot / d)), ends) if d > 0 else None

    def ClosestPoint(self, p, *a):
        best = (1e300, 0.0)
        for i in range(len(self._P) - 1):
            a_, b_ = self._P[i], self._P[i + 1]; dx, dy = b_.X - a_.X, b_.Y - a_.Y; L2 = dx * dx + dy * dy
            f = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p.X - a_.X) * dx + (p.Y - a_.Y) * dy) / L2))
            d = (a_.X + dx * f - p.X) ** 2 + (a_.Y + dy * f - p.Y) ** 2
            if d < best[0]: best = (d, i + f)
        return True, best[1]

    def ClosestPoints(self, other, *a):
        """(True, point on self, point on other): nearest pair over all vertex-to-segment pairs."""
        best = None
        for A, B in ((self, other), (other, self)):
            for p in A._P:
                ok, t = B.ClosestPoint(p); q = B.PointAt(t); d = p.DistanceTo(q)
                if best is None or d < best[0]:
                    best = (d, p, q) if A is self else (d, q, p)
        return True, best[1], best[2]

    def Contains(self, p, *a):
        P = self._P; ins = False; j = len(P) - 1
        for i in range(len(P)):
            if (P[i].Y > p.Y) != (P[j].Y > p.Y) and p.X < (P[j].X - P[i].X) * (p.Y - P[i].Y) / ((P[j].Y - P[i].Y) or 1e-300) + P[i].X:
                ins = not ins
            j = i
        return PointContainment.Inside if ins else PointContainment.Outside

    def Reverse(self):
        self._P.reverse(); return True

    def Translate(self, *a):
        v = a[0] if len(a) == 1 else Vector3d(*a)
        self._P = [Point3d(p.X + v.X, p.Y + v.Y, p.Z + v.Z) for p in self._P]; return True


class PolylineCurve(Curve):
    pass


class NurbsCurve(Curve):
    pass


class LineCurve(Curve):
    def __init__(self, a, b=None):
        if b is None and isinstance(a, Line): a, b = a.From, a.To
        Curve.__init__(self, [a, b])
    @property
    def Line(self): return Line(self._P[0], self._P[1])


class Line(object):
    def __init__(self, a, b, *c):
        if c: a, b = Point3d(a, b, c[0]), Point3d(*c[1:])
        self.From, self.To = a, b
    @property
    def Length(self): return self.From.DistanceTo(self.To)
    def PointAt(self, t): return Point3d(self.From.X + (self.To.X - self.From.X) * t, self.From.Y + (self.To.Y - self.From.Y) * t, self.From.Z + (self.To.Z - self.From.Z) * t)


class Plane(object):
    def __init__(self, o=None, x=None, y=None):
        self.Origin = o or Point3d(0, 0, 0); self.XAxis = x or Vector3d(1, 0, 0); self.YAxis = y or Vector3d(0, 1, 0)
        self.ZAxis = Vector3d(0, 0, 1)


Plane.WorldXY = Plane()


class Arc(object):
    def __init__(self, c, r, a0=0.0, a1=2 * math.pi, x=None, y=None):
        self.Center, self.Radius, self.a0, self.a1 = c, r, a0, a1
        self.Plane = Plane(c, x or Vector3d(1, 0, 0), y or Vector3d(0, 1, 0))
    def pt(self, a):
        x, y = self.Plane.XAxis, self.Plane.YAxis; c = self.Center; r = self.Radius
        ca, sa = math.cos(a), math.sin(a)
        return Point3d(c.X + r * (ca * x.X + sa * y.X), c.Y + r * (ca * x.Y + sa * y.Y), c.Z + r * (ca * x.Z + sa * y.Z))


class Circle(Arc):
    def __init__(self, *a):
        if len(a) == 2 and isinstance(a[0], Plane): Arc.__init__(self, a[0].Origin, a[1], 0, 2 * math.pi, a[0].XAxis, a[0].YAxis)
        else: Arc.__init__(self, a[0], a[1])


class ArcCurve(Curve):
    """Kept as a polyline of 2-degree steps (at least 8), plus its arc."""
    def __init__(self, arc, circle=False):
        self.Arc, self._circle = arc, circle
        n = max(8, int(abs(arc.a1 - arc.a0) / math.radians(2)))
        Curve.__init__(self, [arc.pt(arc.a0 + (arc.a1 - arc.a0) * k / n) for k in range(n + 1)])
        if circle: self._P[-1] = self._P[0]
    Degree = 2
    def IsCircle(self, *a): return self._circle
    def IsArc(self, *a): return True
    def TryGetPolyline(self, *a): return False, None
    def IsPolyline(self): return False
    def GetLength(self, *a): return abs(self.Arc.a1 - self.Arc.a0) * self.Arc.Radius
    @property
    def IsCompleteCircle(self): return self._circle


class Point(GeometryBase):
    def __init__(self, p): self.Location = p
    def GetBoundingBox(self, *a): return BoundingBox(self.Location, self.Location)


class TextEntity(GeometryBase):
    def __init__(self): self.PlainText = ""; self.Text = ""; self.TextHeight = 1.0; self.Plane = Plane(); self._b = None
    def GetBoundingBox(self, *a): return self._b or BoundingBox(self.Plane.Origin, self.Plane.Origin)
    @staticmethod
    def Create(text, plane, *a):
        t = TextEntity(); t.PlainText = t.Text = text; t.Plane = plane; return t


class TextDot(GeometryBase):
    def __init__(self, text="", p=None): self.Text = text; self.Point = p or Point3d(); self.FontHeight = 14
    def GetBoundingBox(self, *a): return BoundingBox(self.Point, self.Point)


class Hatch(GeometryBase):
    @staticmethod
    def Create(curves, *a): return [Hatch()]
    def GetBoundingBox(self, *a): return BoundingBox.Empty


class _Enum(object):
    def __init__(self, **k): self.__dict__.update(k)
    def __getattr__(self, k): return k


PointContainment = _Enum(Inside="Inside", Outside="Outside", Coincident="Coincident", Unset="Unset")
CurveOrientation = _Enum(Clockwise="Clockwise", CounterClockwise="CounterClockwise", Undefined="Undefined")


class AreaMassProperties(object):
    @staticmethod
    def Compute(g, *a):
        P = getattr(g, "_P", None)
        if not P or len(P) < 3: return None
        A = cx = cy = 0.0
        for i in range(len(P) - 1):
            c = P[i].X * P[i + 1].Y - P[i + 1].X * P[i].Y; A += c; cx += (P[i].X + P[i + 1].X) * c; cy += (P[i].Y + P[i + 1].Y) * c
        r = AreaMassProperties(); A /= 2.0
        r.Area = abs(A); r.Centroid = Point3d(cx / (6 * A), cy / (6 * A), 0) if A else P[0]; return r


# ---------------------------------------------------------------- document
class Layer(object):
    def __init__(self):
        self.Name = ""; self.FullPath = ""; self.Index = -1; self.Id = str(uuid.uuid4()); self.ParentLayerId = "00000000-0000-0000-0000-000000000000"
        self.IsDeleted = False; self.Color = (0, 0, 0); self.IsVisible = True; self.IsLocked = False


class ObjectAttributes(object):
    def __init__(self): self.LayerIndex = 0; self.Name = ""; self._us = {}; self.ObjectColor = None; self.ColorSource = None
    def GetUserString(self, k): return self._us.get(k)
    def SetUserString(self, k, v): self._us[k] = v; return True
    def GetUserStrings(self): return dict(self._us)
    def Duplicate(self):
        a = ObjectAttributes(); a.__dict__.update(self.__dict__); a._us = dict(self._us); return a
    def __getattr__(self, k): return mock.MagicMock(name="attr." + k)


class RhinoObject(object):
    def __init__(self, geo_or_rec, att, oid):
        self._g = geo_or_rec; self.Attributes = att; self.Id = oid; self.IsDeleted = False
    @property
    def Geometry(self):
        if isinstance(self._g, dict): self._g = _geo(self._g)
        return self._g
    def CommitChanges(self): return True


def _geo(r):
    P = lambda t: Point3d(*t)
    t = r["t"]
    if t == "line": return LineCurve(P(r["pts"][0]), P(r["pts"][1]))
    if t == "pline": return PolylineCurve([P(p) for p in r["pts"]])
    if t == "arc": return ArcCurve(Arc(P(r["c"]), r["r"], r["a0"], r["a1"], Vector3d(*r["x"]), Vector3d(*r["y"])), r["circle"])
    if t == "point": return Point(P(r["p"]))
    if t == "text":
        g = TextEntity(); g.PlainText = g.Text = r["s"]; g.TextHeight = r["h"]; g.Plane = Plane(P(r["o"]), Vector3d(*r["x"]), Vector3d(*r["y"]))
        if r.get("bmin"): g._b = BoundingBox(P(r["bmin"]), P(r["bmax"]))
        return g
    raise ValueError(t)


class Layers(list):
    def FindByFullPath(self, path, default=-1):
        for l in self:
            if l.FullPath == path and not l.IsDeleted: return l.Index
        return default
    def FindName(self, name, *a):
        for l in self:
            if l.Name == name and not l.IsDeleted: return l
        return None
    def Find(self, name, *a):
        l = self.FindName(name); return l.Index if l else -1
    def FindIndex(self, i): return self[i]
    def Add(self, lay, *a):
        if isinstance(lay, str): n = Layer(); n.Name = lay; lay = n
        par = next((l for l in self if l.Id == lay.ParentLayerId), None)
        lay.FullPath = (par.FullPath + "::" if par else "") + lay.Name
        lay.Index = len(self); self.append(lay); return lay.Index


class Objects(list):
    def __init__(self, doc): list.__init__(self); self.doc = doc; self._by_layer = {}; self._by_id = {}
    def _add(self, g, att):
        if att is None: att = ObjectAttributes()
        oid = str(uuid.UUID(int=len(self._by_id) + 1)) if not isinstance(g, dict) else g["id"]
        o = RhinoObject(g, att, oid); self.append(o); self._by_layer.setdefault(att.LayerIndex, []).append(o); self._by_id[oid] = o
        return oid
    def FindByLayer(self, lay):
        if isinstance(lay, str): lay = self.doc.Layers.FindName(lay)
        if lay is None: return []
        return [o for o in self._by_layer.get(lay.Index, []) if not o.IsDeleted]
    def FindId(self, i): return self._by_id.get(str(i))
    def Find(self, i): return self._by_id.get(str(i))
    def GetObjectList(self, *a):
        want = a[0] if a else None
        for o in list(self):
            if o.IsDeleted: continue
            if want == "Curve" and not isinstance(o.Geometry, Curve): continue
            yield o
    def AddCurve(self, g, att=None, *a): return self._add(g, att)
    AddPolyline = AddCurve
    def AddTextDot(self, g, att=None, *a): return self._add(g if isinstance(g, TextDot) else TextDot(g, a[0] if a else None), att)
    def AddText(self, g, att=None, *a): return self._add(g if isinstance(g, TextEntity) else TextEntity.Create(str(g), Plane()), att if isinstance(att, ObjectAttributes) else None)
    def AddHatch(self, g, att=None, *a): return self._add(g, att)
    def AddPoint(self, p, att=None, *a): return self._add(Point(p), att)
    def AddPictureFrame(self, *a): return str(uuid.uuid4())
    def Delete(self, o, *a):
        o = o if isinstance(o, RhinoObject) else self._by_id.get(str(o))
        if o is None or o.IsDeleted: return False
        o.IsDeleted = True; return True
    def ModifyAttributes(self, o, att, *a):
        o = o if isinstance(o, RhinoObject) else self._by_id.get(str(o))
        if o is None: return False
        self._by_layer.get(o.Attributes.LayerIndex, []).remove(o) if o in self._by_layer.get(o.Attributes.LayerIndex, []) else None
        o.Attributes = att; self._by_layer.setdefault(att.LayerIndex, []).append(o); return True
    def __iter__(self): return iter([o for o in list.__iter__(self) if not o.IsDeleted])
    @property
    def BoundingBox(self):
        b = BoundingBox(None, None)
        for o in self: b.Union(o.Geometry.GetBoundingBox(True))
        return b


class Doc(object):
    def __init__(self, survey=None, path=None):
        self.Layers = Layers(); self.Objects = Objects(self); self.ModelUnitSystem = "Meters"
        self.ModelAbsoluteTolerance = 0.001; self.Path = path; self.Name = os.path.basename(path or "stub.3dm")
        self.Views = mock.MagicMock(name="doc.Views")
        if survey:
            d = pickle.load(open(survey, "rb"))
            byid = {}
            for r in d["layers"]:
                l = Layer(); l.Name, l.FullPath, l.Index, l.Id, l.ParentLayerId = r["name"], r["full"], r["index"], r["id"], r["parent"]
                self.Layers.append(l)
            for r in d["objs"]:
                a = ObjectAttributes(); a.LayerIndex = r["layer"]; a.Name = r["name"]; a._us = dict(r["us"])
                self.Objects._add(r, a)
    def __getattr__(self, k): return mock.MagicMock(name="doc." + k)


# ---------------------------------------------------------------- modules
class _Mod(types.ModuleType):
    def __getattr__(self, k):
        if k.startswith("__"): raise AttributeError(k)
        m = mock.MagicMock(name=self.__name__ + "." + k); setattr(self, k, m); return m


def install(survey=None, home=None):
    doc = Doc(survey, os.path.join(home or ".", "Bergama_Altlik.3dm") if survey else None)
    R = _Mod("Rhino"); G = _Mod("Rhino.Geometry"); DO = _Mod("Rhino.DocObjects")
    for k, v in list(globals().items()):
        if isinstance(v, type) and v.__module__ == __name__ and k not in ("Layer", "ObjectAttributes", "RhinoObject", "Layers", "Objects", "Doc", "_Mod", "_Enum"):
            setattr(G, k, v)
    G.PointContainment = PointContainment; G.CurveOrientation = CurveOrientation
    DO.Layer = Layer; DO.ObjectAttributes = ObjectAttributes; DO.ObjectType = _Enum(Curve="Curve", Point="Point", Annotation="Annotation", AnyObject=None)
    R.Geometry = G; R.DocObjects = DO
    R.RhinoDoc = types.SimpleNamespace(ActiveDoc=doc)
    R.UnitSystem = _Enum(Meters="Meters", Millimeters="Millimeters", Centimeters="Centimeters")
    R.RhinoMath = types.SimpleNamespace(UnitScale=lambda a, b: 1.0, ToRadians=math.radians, ToDegrees=math.degrees, UnsetValue=-1.23432101234321e+308, ZeroTolerance=2.3283064365386963e-10)
    R.RhinoApp = mock.MagicMock(name="RhinoApp")
    S = _Mod("System"); SD = _Mod("System.Drawing")
    class Guid(str):
        def __new__(cls, s=None): return str.__new__(cls, str(s) if s is not None else str(uuid.uuid4()))
        @staticmethod
        def NewGuid(): return Guid()
    Guid.Empty = Guid("00000000-0000-0000-0000-000000000000")
    S.Guid = Guid; S.Drawing = SD
    SD.Color = types.SimpleNamespace(FromArgb=lambda *a: tuple(a), Black=(0, 0, 0), White=(255, 255, 255))
    sc = types.ModuleType("scriptcontext"); sc.sticky = {}; sc.doc = doc
    mods = {"Rhino": R, "Rhino.Geometry": G, "Rhino.DocObjects": DO, "System": S, "System.Drawing": SD, "scriptcontext": sc}
    for n in ["Rhino.Display", "Rhino.FileIO", "System.Collections", "System.Collections.Generic", "Grasshopper", "Grasshopper.Kernel",
              "Grasshopper.Kernel.Parameters", "Grasshopper.Kernel.Special", "rhinoscriptsyntax", "clr", "ghpythonlib", "ghpythonlib.components"]:
        mods[n] = _Mod(n)
    sys.modules.update(mods)
    return doc
