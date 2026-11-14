# -*- coding: utf-8 -*-
"""Bergama Group 6: SECTIONS v1.5 (14 Nov 2026; v1.5: all sections on ONE page of one PDF, Aras 14 Nov 09:42 UTC "produce all those sections in a single pdf", 09:42:59 "merge
all cuts into a single page": stacked top to bottom in line order, same scale, left edges aligned). Rules: scripts/_template/SCRIPT_STANDARD.md.
Aras 12 Nov 2026 10:43-10:46 UTC: "create these kind of sections and make them creatable by section lines"; "show the
contexts on those sections"; "like the buildings in background, if there is a road you should show the road"; "we had a
like texture band beneath it ... include those as a thin line"; "these gonna be our new sections they gonna be generic
and we'll produce our 12 sections from those".

ONE generic section per section line, in the look of the 27 Oct detail section (his image: S4, both banks, 1:500):
stippled earth, heavy cut line, reeds, iris, meadow, trees, people, light-blue water, the blue level lines Q500, Q100 and
the Oct-Dec high end, a thin material band under the cut, a scale bar. New script; the cut, TIN and water-level method
are SectionFromLine v1.1's (kept as they were checked on S4), the drawing pieces are the 27 Oct detail engine, now in its
own file Data/bergama_sections_engine.py.
  lines    in this order: lines wired to section_line (named L1, L2 ...); else the curves on the open model's layer
           "section_lines" (each named by its object name, else S1, S2 ...); else the 12 lines N1-A ... N6-B of
           Data/section_lines.json (survey coordinates, from his section lines layer v3 of 11 Nov)
  window   half_width m either side of where the line crosses the stream centreline (default 100 m), never past the
           line's own ends
  ground   a TIN of the open file's survey heights within 60 m of the line, cut every 0.25 m
  water    Manning normal depth on this cut (n 0.050, Chow 1959), bed slope from the lowest bed height per 25 m bin 300 m
           up and down the centreline; flows DSI Q100 205.2 / Q500 263.33 m3/s and the Oct-Dec gauge flow 0.423 m3/s
           (research/rain_river_levels). Summer strip 4.0 m x 0.30 m at the bed low point (design).
  context  from cached/basemap/basemap.json (the site step's layers): buildings the line cuts and buildings up to
           BACK_M behind it (looking direction), each at its own floor count x storey height on the survey ground, flat
           topped (the survey holds no roof forms); roads = the street areas the line crosses, and street centrelines
           crossed between two survey road edges (YOL_SOSE / YOL_BORDUR) within 12 m. A building without a height in
           the basemap is not drawn (counted in the log). Grey tones of the context are drawing values (ours).
  planting by rule (design intention, ours): reeds and iris on the wet bed, meadow above, survey trees within 3 m.
  NO design of terraces, steps or decks: the plan holds no levels. On S4 only (the 27 Oct cut wired as a line) the
  engine's designed banks are drawn.

Component: Rhino 8 > Grasshopper > Python 3 Script (the board builder places it from the cloud kit).
  input  run           Button (or the previous script's done text)
  input  section_line  Line list: lines picked in Rhino (survey coordinates); none = the 12 node sections
  input  scale         sheet scale 1:n (default 500)
  input  half_width    m drawn either side of the stream (default 100)
  output log / done    as every Bergama script
Reads  ~/Downloads/Bergama/Data/bergama_sections_engine.py, Data/section_lines.json, Data/selinos_centreline.json,
       ~/Downloads/Bergama/cached/bergama_basemap/basemap_layers.json + streets.json (press Basemap first; else the old
       cached/basemap/basemap.json), the open Rhino model's survey layers (read once per press)
Writes ~/Downloads/Bergama/output/bergama_sections/Sections.pdf          ONE page, every line stacked top to bottom (1:scale, PDF layers)
       ~/Downloads/Bergama/cached/bergama_sections/sections.json         every cut's numbers
       ~/Downloads/Bergama/logs/bergama_sections_log.txt
"""
import os, time, json, math, bisect

# ---- SETTINGS ----
VERSION = "v1.5"
GH_LABEL = "Sections"
OUT_FOLDER = "bergama_sections"
LOG_NAME = "bergama_sections_log.txt"
GH_INPUTS = {"section_line": "line list", "scale": "int 50..2000 = 500", "half_width": "int 20..400 = 100"}
SECTION_LAYER = "section_lines"   # the model layer his own section lines sit on (object name = section name)
SEASON = "autumn"          # the one drawing per line: Q500, Q100 and the Oct-Dec high end, as in his image
# v1.3, Aras 12 Nov 19:10 UTC: "for storey height you got the data look for it". The project's own values (site board
# scripts/selinus_board_v67.py: FLOOR_H = 3.0 and STOREY = {"religious": 5.0, "institutional": 3.5, "industrial": 4.5},
# printed on its sheets as "Storey heights 3.0 m; civic 3.5, sacred 5.0, industry 4.5"): typical values, not measured.
# The Basemap cache tells heritage / sacred outlines from the rest, so those take 5.0 m and every other building
# 3.0 m; civic (3.5) and industry (4.5) are not told apart in the cache yet and are drawn at 3.0 m.
STOREY_M = 3.0             # m per floor, every building that is not heritage / sacred
STOREY_HERITAGE_M = 5.0    # m per floor, the Basemap's heritage outlines (sacred and heritage)
BACK_M = 30.0              # buildings up to this far behind the cut are drawn as background
ROAD_EDGE_M = 12.0         # a street centreline crossing counts as a road between survey edges this close to it
ROAD_T = 0.25              # m, drawn thickness of the road surface
BLD_FILL, BLD_EDGE, BLD_CUT_FILL = "F1EFEA", "9A948C", "E2DFD8"   # context greys (drawing values, ours)
ROAD_FILL = "6E6B66"       # existing road surface (drawing value, ours; the engine's red asphalt is the design's)
BAND_H = 2.0               # mm, the thin material band

SURVEY_LAYERS = ["NOKTA_TAKEOMETRI", "NOKTA_POLIGON", "NOKTA_NIRENGI", "EGRI_1M", "EGRI_2M", "EGRI_5M", "EGRI_10M", "EGRI_ARA", "SEV_UST", "SEV_ALT",
                 "HIDRO_DERE_SULU"]
MARK_LAYERS = {"SEV_UST": "bank top", "SEV_ALT": "bank toe", "HIDRO_DERE_SULU": "stream line", "YOL_SOSE": "road edge",
               "YOL_BORDUR": "kerb"}
TREE_LAYERS = ["SEMBOL_TEK_AGAC", "SEMBOL_YPDKN_AGAC", "SEMBOL_YAP_DOKMEYEN"]
CORRIDOR_M = 60.0          # survey heights this close to the line build the TIN
# v1.2 (first Rhino run, 12 Nov: N2-A, N3-A, N3-B not drawn, "only 18 survey heights within 60 m"): in the old town
# the survey has almost no height points (counted in Bergama_Altlik.3dm within 60 m of N2-A: 0 tacheometric points,
# 22 traverse points on NOKTA_POLIGON, which v1.1 did not read). Now the traverse and triangulation points are read
# too, and where fewer than HEIGHTS_WANT heights lie in the corridor it is widened step by step (CORRIDOR_STEPS);
# the cut is drawn from HEIGHTS_MIN heights on, with a FLAG line that says how thin its ground is.
CORRIDOR_STEPS = (60.0, 100.0, 150.0)
HEIGHTS_WANT, HEIGHTS_MIN = 50, 8
DS = 0.25                  # drawn profile step, m
HYD_HALF, HYD_DS = 200.0, 0.5   # hydraulic cut: 200 m either side of the stream crossing, 0.5 m steps (research)
CHANNEL_M = 40.0           # the bed low point is the lowest ground within this distance of the crossing
MAX_LEN_M = 200.0          # a longer line is drawn 100 m either side of its stream crossing (FLAG)
N_MANNING = 0.050          # worst-case roughness, gravel-cobble bed (Chow 1959; research A3s)
SLOPE_HALF, SLOPE_BIN = 300.0, 25.0
TREE_NEAR_M = 3.0          # survey tree symbols this close to the line are drawn on it
OBLIQUE_DEG = 20.0         # a cut further than this off square to the stream: FLAG (flow area overstated)
STRIP_W, STRIP_D = 4.0, 0.30    # summer water strip (design, case.md s.4)
WET_BAND_M = 1.0           # planting by rule: reeds / iris on ground up to this height above the bed (design, ours)
# flows, m3/s: DSI design floods (Danistay 6. D. E.2021/9521 K.2023/4193, as cited on the water board) and the
# area-scaled gauge flows WY2016-2021 (research/rain_river_levels/tables/A3s_monthly_mean_depth_surveyed_sections.csv,
# A3s_levels_by_event_surveyed_sections.csv: Jan via Ilica 3.36, Apr via Ilica 0.752, Dec via Komurcu 0.423,
# highest daily mean 6 Jan 2017 43.9)
Q100, Q500 = 205.2, 263.33
SEASON_WATER = {   # (Q, filled?, label with %+.2f and %.2f)
    "winter": [(3.36, True, u"Jan-Feb mean %+.2f (%.2f m, calculated)"),
               (43.9, False, u"highest day 6 Jan 2017 %+.2f (%.2f m, calculated)")],
    "spring": [(0.752, True, u"Mar-Apr, low end %+.2f (%.2f m, calculated)"),
               (3.36, False, u"high end of Jan-Apr %+.2f (%.2f m, calculated)")],
    "summer": [],
    "autumn": [(0.423, True, u"Oct-Dec high end %+.2f (%.2f m, calculated)")],
}
SEASONS_ORDER = ("winter", "spring", "summer", "autumn")
STRIP_HELD = {"winter": False, "spring": True, "summer": True, "autumn": True}   # engine SEASONS strip_held
S4_WINDOW = (538.0, 652.0)      # the engine's design of both banks (SECTIONS 1-1' s 538-598, 2-2' s 652-588)

# ---- Bergama folders (Aras 24 Oct 08:28 + 27 Oct 11:07; SCRIPT_STANDARD §9). Every script uses ONLY these. ----
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")


def bg_output(name):
    return os.path.join(BERGAMA_ROOT, "output", name)


def bg_cache(name):
    return os.path.join(BERGAMA_ROOT, "cached", name)


def bg_booklet(name):
    return os.path.join(BERGAMA_ROOT, "cached", "booklet", name)


def bg_logs(*sub):
    return os.path.join(BERGAMA_ROOT, "logs", *sub)


DATA_DIR = os.path.join(BERGAMA_ROOT, "Data")
OUT_DIR = bg_output(OUT_FOLDER)
CACHE_DIR = bg_cache(OUT_FOLDER)
LOG_DIR = bg_logs()


# ================================================================ the engine (27 Oct look)
def load_engine(log):
    p = os.path.join(DATA_DIR, "bergama_sections_engine.py")
    with open(p, encoding="utf-8") as f:
        txt = f.read()
    ns = {"__name__": "bergama_sections_engine"}
    exec(compile(txt, "bergama_sections_engine", "exec"), ns)
    log.append(u"engine: %s read from %s" % (ns.get("VERSION"), p))
    return ns


def load_basemap(log):
    """the context (survey m): buildings with heights, street areas, street centrelines; {} if missing.
    v1.1: read from the Basemap script's caches (cached/bergama_basemap/basemap_layers.json: closed building
    outlines + the survey's floor counts; streets.json: the street bands); a building's height = its floor count x
    STOREY_M (the project's storey height, an assumption, not a survey height). Only when that cache is missing, the
    old site board's cached/basemap/basemap.json is read as before."""
    p = os.path.join(bg_cache("bergama_basemap"), "basemap_layers.json")
    if os.path.isfile(p):
        try:
            with open(p, encoding="utf-8") as f:
                J = json.load(f)
            B, n_out = [], 0
            for key in ("buildings", "heritage"):
                rings = [P for cl, P in J.get("layers", {}).get(key, []) if cl and len(P) >= 3]
                fls = (J.get("floors") or {}).get(key) or []
                for i, r in enumerate(rings):
                    n_out += 1
                    fl = int(fls[i]) if i < len(fls) else 0
                    xs, ys = [q[0] for q in r], [q[1] for q in r]
                    B.append((min(xs), min(ys), max(xs), max(ys), r, fl * (STOREY_HERITAGE_M if key == "heritage" else STOREY_M), fl))
            A = []
            ps = os.path.join(bg_cache("bergama_basemap"), "streets.json")
            if os.path.isfile(ps):
                with open(ps, encoding="utf-8") as f:
                    for cl, r in json.load(f).get("layers", {}).get("streets", []):
                        if len(r) >= 3:
                            xs, ys = [q[0] for q in r], [q[1] for q in r]
                            A.append((min(xs), min(ys), max(xs), max(ys), r))
            else:
                log.append(u"FLAG context: %s not found: no road surfaces drawn; press Basemap once" % ps)
            log.append(u"context: %s (%s): %d building outlines, %d with a floor count (height = floors x %.1f m, heritage and "
                       u"sacred x %.1f m: the site board's typical storey heights); %d street bands" % (
                           p, J.get("made_by", u"?"), n_out, sum(1 for b_ in B if b_[6] > 0), STOREY_M, STOREY_HERITAGE_M,
                           len(A)))
            return {"buildings": B, "areas": A, "streets": []}
        except Exception as ex:
            log.append(u"FLAG context: %s not read (%s); trying the old site board's cache" % (p, type(ex).__name__))
    p = os.path.join(bg_cache("basemap"), "basemap.json")
    try:
        with open(p, encoding="utf-8") as f:
            L = json.load(f).get("layers", {})
    except Exception as ex:
        log.append(u"FLAG context: %s not read (%s): no buildings or roads drawn; press Basemap once"
                   % (p, type(ex).__name__))
        return {}
    B = []
    for b in L.get("buildings", []):
        r = (b.get("rings") or [[]])[0]
        if len(r) >= 3:
            xs, ys = [q[0] for q in r], [q[1] for q in r]
            B.append((min(xs), min(ys), max(xs), max(ys), r, float(b.get("h") or 0.0), int(b.get("floors") or 0)))
    A = []
    for r in L.get("street_areas", []):
        if len(r) >= 3:
            xs, ys = [q[0] for q in r], [q[1] for q in r]
            A.append((min(xs), min(ys), max(xs), max(ys), r))
    Sx = [st[1] for st in L.get("streets_in", []) if len(st) > 1 and len(st[1]) >= 2]
    log.append(u"context: %s: %d buildings, %d street areas, %d street lines" % (p, len(B), len(A), len(Sx)))
    return {"buildings": B, "areas": A, "streets": Sx}


def context_for(C, BM, tin, ox, oy, lg):
    """C.bld = [(s0, s1, base z, height, cut?, distance behind, floors)], C.roads = [(s0, s1)], C.streets = [s]"""
    C.bld, C.roads, C.streets = [], [], []
    if not BM:
        return
    w0, w1 = C.window
    pa, pb = C.xy(w0), C.xy(w1)
    pad = BACK_M + 5.0
    box = (min(pa[0], pb[0]) - pad, min(pa[1], pb[1]) - pad, max(pa[0], pb[0]) + pad, max(pa[1], pb[1]) + pad)
    no_h = 0
    for x0, y0, x1, y1, r, h, fl in BM["buildings"]:
        if x1 < box[0] or x0 > box[2] or y1 < box[1] or y0 > box[3]:
            continue
        so = [C.su(q[0], q[1]) for q in r]
        omin, omax = min(o for _, o in so), max(o for _, o in so)
        if omax <= 0.0 or omin > BACK_M:
            continue
        is_cut = omin < 0.0
        if is_cut:
            xs = []
            for (sa, oa), (sb, ob) in zip(so, so[1:] + so[:1]):
                if (oa < 0.0) != (ob < 0.0):
                    xs.append(sa + (sb - sa) * (0.0 - oa) / (ob - oa))
            if len(xs) < 2:
                continue
            a, b = min(xs), max(xs)
        else:
            a, b = min(q[0] for q in so), max(q[0] for q in so)
        a, b = max(a, w0), min(b, w1)
        if b - a < 0.5:
            continue
        if h <= 0.0:
            no_h += 1
            continue
        cx, cy = sum(q[0] for q in r) / len(r), sum(q[1] for q in r) / len(r)
        zb = None if is_cut else tin.z(cx - ox, cy - oy)
        C.bld.append((a, b, zb, h, is_cut, max(0.0, omin), fl))
    C.bld.sort(key=lambda t: -t[5])
    iv = []
    for x0, y0, x1, y1, r in BM["areas"]:
        if x1 < box[0] or x0 > box[2] or y1 < box[1] or y0 > box[3]:
            continue
        xs = sorted(t * C.L for t in (seg_cross(C.A, C.B, p, q) for p, q in zip(r, r[1:] + r[:1])) if t is not None)
        for a, b in zip(xs[0::2], xs[1::2]):
            a, b = max(a, w0), min(b, w1)
            if b - a >= 0.5:
                iv.append((a, b))
    edges = sorted(m[0] for m in C.marks if m[1] in ("road edge", "kerb"))
    for pl in BM["streets"]:
        for p, q in zip(pl[:-1], pl[1:]):
            if max(p[0], q[0]) < box[0] or min(p[0], q[0]) > box[2] or max(p[1], q[1]) < box[1] or min(p[1], q[1]) > box[3]:
                continue
            t = seg_cross(C.A, C.B, p, q)
            if t is None or not (w0 <= t * C.L <= w1):
                continue
            sc = t * C.L
            if any(a - 0.5 <= sc <= b + 0.5 for a, b in iv):
                continue
            le = [e for e in edges if sc - ROAD_EDGE_M <= e < sc]
            ri = [e for e in edges if sc < e <= sc + ROAD_EDGE_M]
            if le and ri and ri[0] - le[-1] >= 1.5:
                iv.append((le[-1], ri[0]))
            else:
                C.streets.append(sc)
    iv.sort()
    for a, b in iv:
        if C.roads and a <= C.roads[-1][1] + 0.3:
            C.roads[-1] = (C.roads[-1][0], max(C.roads[-1][1], b))
        else:
            C.roads.append((a, b))
    C.streets = [x for x in sorted(C.streets) if not any(a - 0.5 <= x <= b + 0.5 for a, b in C.roads)]
    lg.append(u"context %s: %d building(s) cut, %d behind within %.0f m, %d without a height left out; %d road(s) %s; %d "
              u"street line(s) without survey edges (marked, no width)" % (
                  C.name, sum(1 for t in C.bld if t[4]), sum(1 for t in C.bld if not t[4]), BACK_M, no_h, len(C.roads),
                  u", ".join(u"%.1f-%.1f m" % r for r in C.roads), len(C.streets)))


# ================================================================ survey from the open Rhino model
def _layer_objs(doc, name):
    idx = doc.Layers.FindByFullPath(name, -1)
    if idx < 0:
        for lay in doc.Layers:
            if not lay.IsDeleted and lay.Name == name:
                idx = lay.Index
                break
    if idx < 0:
        return []
    return list(doc.Objects.FindByLayer(doc.Layers[idx]) or [])


def _curve_pts(rg, g):
    try:
        ok, pl = g.TryGetPolyline()
        if ok:
            return [(p.X, p.Y, p.Z) for p in pl]
    except Exception:
        pass
    try:
        ts = g.DivideByLength(1.0, True) or []
        pts = [g.PointAt(t) for t in ts]
        if g.IsClosed is False and pts:
            pts.append(g.PointAtEnd)
        return [(p.X, p.Y, p.Z) for p in pts]
    except Exception:
        return []


def read_survey(box, log):
    """{layer: [polyline [(x, y, z)], ...]} (points as one-point polylines) inside box (x0, y0, x1, y1)"""
    import Rhino
    rg = Rhino.Geometry
    doc = Rhino.RhinoDoc.ActiveDoc
    out, cnt = {}, {}
    for name in SURVEY_LAYERS + list(MARK_LAYERS) + TREE_LAYERS:
        if name in out:
            continue
        L = []
        for o in _layer_objs(doc, name):
            g = o.Geometry
            if isinstance(g, rg.Point):
                p = g.Location
                if box[0] <= p.X <= box[2] and box[1] <= p.Y <= box[3]:
                    L.append([(p.X, p.Y, p.Z)])
            elif isinstance(g, rg.Curve):
                b = g.GetBoundingBox(True)
                if b.Max.X < box[0] or b.Min.X > box[2] or b.Max.Y < box[1] or b.Min.Y > box[3]:
                    continue
                if isinstance(g, rg.ArcCurve) and g.IsCircle():          # a symbol drawn as a circle: its centre
                    c = g.Arc.Center
                    L.append([(c.X, c.Y, c.Z)])
                    continue
                P = _curve_pts(rg, g)
                if P:
                    L.append(P)
            elif isinstance(g, rg.InstanceReferenceGeometry):            # a symbol block: its insertion point
                p = g.Xform * rg.Point3d(0.0, 0.0, 0.0)
                if box[0] <= p.X <= box[2] and box[1] <= p.Y <= box[3]:
                    L.append([(p.X, p.Y, p.Z)])
        out[name] = L
        cnt[name] = len(L)
    log.append(u"survey read: " + u", ".join(u"%s %d" % kv for kv in sorted(cnt.items())))
    return out


def delaunay(xy):
    """triangles (index triples) of 2D points (Grasshopper's Delaunay, as the engine's re-cut uses it)"""
    import Grasshopper.Kernel.Geometry as GKG
    nodes = GKG.Node2List()
    for x, y in xy:
        nodes.Append(GKG.Node2(x, y))
    return [(f.A, f.B, f.C) for f in GKG.Delaunay.Solver.Solve_Faces(nodes, 1)]


class Tin(object):
    def __init__(self, pts):
        self.p = pts                       # [(x, y, z)] (local coordinates)
        self.t = delaunay([(p[0], p[1]) for p in pts])
        self.cell = {}
        for t in self.t:
            xs = [pts[i][0] for i in t]
            ys = [pts[i][1] for i in t]
            for i in range(int(min(xs) // 5), int(max(xs) // 5) + 1):
                for j in range(int(min(ys) // 5), int(max(ys) // 5) + 1):
                    self.cell.setdefault((i, j), []).append(t)

    def z(self, x, y):
        P = self.p
        for (ia, ib, ic) in self.cell.get((int(x // 5), int(y // 5)), ()):
            a, b, c = P[ia], P[ib], P[ic]
            det = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
            if abs(det) < 1e-12:
                continue
            l1 = ((b[1] - c[1]) * (x - c[0]) + (c[0] - b[0]) * (y - c[1])) / det
            l2 = ((c[1] - a[1]) * (x - c[0]) + (a[0] - c[0]) * (y - c[1])) / det
            l3 = 1.0 - l1 - l2
            if min(l1, l2, l3) >= -1e-9:
                return l1 * a[2] + l2 * b[2] + l3 * c[2]
        return None


def fill_gaps(Z):
    """stations outside the TIN take the nearest station's height; None when nothing was cut"""
    idx = [i for i, z in enumerate(Z) if z is not None]
    if not idx:
        return None, len(Z)
    out = list(Z)
    miss = 0
    for i, z in enumerate(Z):
        if z is None:
            j = min(idx, key=lambda k: abs(k - i))
            out[i] = Z[j]
            miss += 1
    return out, miss


# ================================================================ the stream centreline, slope and levels
def load_centreline(log):
    p = os.path.join(DATA_DIR, "selinos_centreline.json")
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    CL = [tuple(q) for q in d["points"]]
    cum = [0.0]
    for a, b in zip(CL[:-1], CL[1:]):
        cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    log.append(u"centreline: %d points, %.0f m (%s)" % (len(CL), cum[-1], p))
    return CL, cum


def cl_project(CL, cum, x, y):
    """(distance, chainage, unit direction) of the nearest centreline point"""
    best = None
    for i in range(len(CL) - 1):
        ax, ay = CL[i]
        bx, by = CL[i + 1]
        ex, ey = bx - ax, by - ay
        l2 = ex * ex + ey * ey
        t = 0.0 if l2 < 1e-12 else max(0.0, min(1.0, ((x - ax) * ex + (y - ay) * ey) / l2))
        d = math.hypot(ax + t * ex - x, ay + t * ey - y)
        if best is None or d < best[0]:
            L = math.sqrt(l2) or 1.0
            best = (d, cum[i] + t * L, (ex / L, ey / L))
    return best


def seg_cross(p, q, a, b):
    """parameter t on p-q where it crosses a-b, or None"""
    rx, ry = q[0] - p[0], q[1] - p[1]
    sx, sy = b[0] - a[0], b[1] - a[1]
    den = rx * sy - ry * sx
    if abs(den) < 1e-12:
        return None
    t = ((a[0] - p[0]) * sy - (a[1] - p[1]) * sx) / den
    u = ((a[0] - p[0]) * ry - (a[1] - p[1]) * rx) / den
    return t if (0.0 <= t <= 1.0 and 0.0 <= u <= 1.0) else None


def stream_crossing(CL, A, B):
    """distance along A-B where the line crosses the centreline (the first crossing), or None"""
    L = math.hypot(B[0] - A[0], B[1] - A[1])
    best = None
    for a, b in zip(CL[:-1], CL[1:]):
        t = seg_cross(A, B, a, b)
        if t is not None and (best is None or t < best):
            best = t
    return None if best is None else best * L


def bed_slope(CL, cum, ch0, survey, log):
    """research method: lowest bed height per 25 m bin within 300 m of chainage ch0 (stream-line vertices within 30 m
    of the centreline, tacheometric points within 12 m), straight line fitted; (slope, bins) or (None, bins)"""
    keep = [i for i in range(len(CL) - 1) if cum[i + 1] >= ch0 - SLOPE_HALF - 60.0 and cum[i] <= ch0 + SLOPE_HALF + 60.0]
    CL = CL[keep[0]:keep[-1] + 2]
    cum = cum[keep[0]:keep[-1] + 2]
    bed = []
    for pl in survey.get("HIDRO_DERE_SULU", []):
        for p in pl:
            if p[2] > 1.0:
                d, s, _ = cl_project(CL, cum, p[0], p[1])
                if d < 30.0 and abs(s - ch0) < SLOPE_HALF:
                    bed.append((s, p[2]))
    for pl in survey.get("NOKTA_TAKEOMETRI", []):
        p = pl[0]
        if p[2] > 1.0:
            d, s, _ = cl_project(CL, cum, p[0], p[1])
            if d < 12.0 and abs(s - ch0) < SLOPE_HALF:
                bed.append((s, p[2]))
    bx, bz = [], []
    a = ch0 - SLOPE_HALF
    while a < ch0 + SLOPE_HALF:
        inb = [q for q in bed if a <= q[0] < a + SLOPE_BIN]
        if inb:
            q = min(inb, key=lambda r: r[1])
            bx.append(q[0])
            bz.append(q[1])
        a += SLOPE_BIN
    if len(bx) < 4:
        log.append(u"FLAG slope: only %d bed bins within %.0f m (need 4): no water levels on this cut" % (
            len(bx), SLOPE_HALF))
        return None, len(bx)
    n = float(len(bx))
    mx, mz = sum(bx) / n, sum(bz) / n
    sxx = sum((x - mx) ** 2 for x in bx)
    sxz = sum((x - mx) * (z - mz) for x, z in zip(bx, bz))
    return -sxz / sxx, len(bx)


def hydraulics(u, z, h):
    """area and wetted perimeter of the water at level h connected to the lowest ground within CHANNEL_M of u = 0
    (research levels.py: walls at the cut ends when the water spills past them)"""
    mid = [i for i in range(len(u)) if abs(u[i]) <= CHANNEL_M]
    i0 = min(mid, key=lambda i: z[i])
    a = i0
    while a > 0 and z[a - 1] < h:
        a -= 1
    b = i0
    while b < len(z) - 1 and z[b + 1] < h:
        b += 1
    spill = a == 0 or b == len(z) - 1
    A = Pw = 0.0
    for k in range(max(a - 1, 0), min(b + 1, len(z) - 1)):
        u1, u2, z1, z2 = u[k], u[k + 1], z[k], z[k + 1]
        d1, d2 = h - z1, h - z2
        if d1 <= 0 and d2 <= 0:
            continue
        if d1 > 0 and d2 > 0:
            A += (d1 + d2) / 2 * (u2 - u1)
            Pw += math.hypot(u2 - u1, z2 - z1)
        else:
            t = d1 / (d1 - d2)
            if d1 > 0:
                A += d1 * t * (u2 - u1) / 2
                Pw += math.hypot(t * (u2 - u1), t * (z2 - z1))
            else:
                A += d2 * (1 - t) * (u2 - u1) / 2
                Pw += math.hypot((1 - t) * (u2 - u1), (1 - t) * (z2 - z1))
    if spill:
        Pw += max(h - z[a], 0) + max(h - z[b], 0)
    return A, Pw, spill


def level_for(u, z, Q, slope):
    """Manning normal depth: the level h at which (1/n) A R^(2/3) S^(1/2) = Q (bisection, 60 steps)"""
    zb = min(z[i] for i in range(len(u)) if abs(u[i]) <= CHANNEL_M)
    lo, hi = zb, zb + 15.0
    spill = False
    for _ in range(60):
        h = (lo + hi) / 2
        A, Pw, spill = hydraulics(u, z, h)
        q = A * (A / Pw) ** (2.0 / 3.0) * math.sqrt(slope) / N_MANNING if Pw > 0 else 0.0
        if q < Q:
            lo = h
        else:
            hi = h
    return hi, spill


# ================================================================ one cut
class Cut(object):
    """one section line: survey-coordinate ends A, B; s = metres from A along A-B; drawn left (A) to right (B)"""

    def __init__(self, n, A, B, src, name=None):
        self.n, self.A, self.B, self.src = n, A, B, src
        self.name = name or u"L%d" % n
        self.survey = None
        self.bld, self.roads, self.streets = [], [], []
        self.L = math.hypot(B[0] - A[0], B[1] - A[1])
        self.u = ((B[0] - A[0]) / self.L, (B[1] - A[1]) / self.L)
        self.is_s4 = False
        self.notes = []

    def xy(self, s):
        return (self.A[0] + self.u[0] * s, self.A[1] + self.u[1] * s)

    def su(self, x, y):
        dx, dy = x - self.A[0], y - self.A[1]
        return dx * self.u[0] + dy * self.u[1], -dx * self.u[1] + dy * self.u[0]


def compass(dx, dy):
    a = (math.degrees(math.atan2(dx, dy)) + 360.0) % 360.0          # 0 = north (survey y), clockwise
    return ("north", "north-east", "east", "south-east", "south", "south-west", "west",
            "north-west")[int((a + 22.5) // 45) % 8]


def build_cut(C, CL, cum, E, log, BM=None):
    """C.prof (s0, DS, Z), C.window, C.s_th, C.z_th, C.levels, C.marks, C.trees"""
    lg = C.notes
    x_c = stream_crossing(CL, C.A, C.B)
    C.cross = x_c
    if C.is_s4:
        w0, w1 = S4_WINDOW
    elif C.L > MAX_LEN_M and x_c is not None:
        w0, w1 = max(0.0, x_c - MAX_LEN_M / 2), min(C.L, x_c + MAX_LEN_M / 2)
        lg.append(u"line %d (%s) is %.0f m long: drawn %.0f-%.0f m (%.0f m either side of the stream)" % (
            C.n, C.name, C.L, w0, w1, MAX_LEN_M / 2))
    elif C.L > MAX_LEN_M:
        w0, w1 = 0.0, MAX_LEN_M
        lg.append(u"FLAG line %d is %.0f m long and does not cross the stream: its first %.0f m drawn" % (
            C.n, C.L, MAX_LEN_M))
    else:
        w0, w1 = 0.0, C.L
    C.window = (w0, w1)
    h0, h1 = (x_c - HYD_HALF, x_c + HYD_HALF) if x_c is not None else (w0, w1)
    a0, a1 = min(w0, h0), max(w1, h1)
    pa, pb = C.xy(a0), C.xy(a1)
    pad = max(CORRIDOR_STEPS[-1], SLOPE_HALF + 20.0 if x_c is not None else 0.0)
    box = (min(pa[0], pb[0]) - pad, min(pa[1], pb[1]) - pad, max(pa[0], pb[0]) + pad, max(pa[1], pb[1]) + pad)
    survey = C.survey if getattr(C, "survey", None) is not None else read_survey(box, log)
    C.survey = survey
    # ---- TIN of the heights in the corridor
    ox, oy = C.A
    for cor in CORRIDOR_STEPS:
        pts = {}
        count = {}
        for name in SURVEY_LAYERS:
            for pl in survey.get(name, []):
                for p in pl:
                    if p[2] <= 1.0:
                        continue
                    s, off = C.su(p[0], p[1])
                    if a0 - 5.0 <= s <= a1 + 5.0 and abs(off) <= cor:
                        pts[(round(p[0] - ox, 2), round(p[1] - oy, 2))] = p[2]
                        count[name] = count.get(name, 0) + 1
        if len(pts) >= HEIGHTS_WANT:
            break
    if len(pts) < HEIGHTS_MIN:
        raise RuntimeError(u"line %d: only %d survey heights within %.0f m: is Bergama_Altlik.3dm open and the line "
                           u"on the site?" % (C.n, len(pts), cor))
    if len(pts) < HEIGHTS_WANT or cor > CORRIDOR_STEPS[0]:
        log.append(u"FLAG line %d: thin ground: %d survey heights within %.0f m of the line (%s); the ground line "
                   u"between them is a straight fill, not surveyed" % (C.n, len(pts), cor, u", ".join(
                       u"%s %d" % kv for kv in sorted(count.items()))))
    keys = list(pts)
    tin = Tin([(k[0], k[1], pts[k]) for k in keys])
    lg.append(u"TIN line %d: %d heights (%s), %d triangles" % (C.n, len(pts), u", ".join(
        u"%s %d" % kv for kv in sorted(count.items())), len(tin.t)))

    def cut(s0, s1, ds):
        n = int(round((s1 - s0) / ds))
        Z = []
        for i in range(n + 1):
            x, y = C.xy(s0 + i * ds)
            Z.append(tin.z(x - ox, y - oy))
        return fill_gaps(Z)
    Z, miss = cut(w0, w1, DS)
    if Z is None:
        raise RuntimeError(u"line %d: the TIN does not reach the line" % C.n)
    if miss:
        lg.append(u"FLAG line %d: %d of %d stations outside the survey TIN took the nearest height" % (C.n, miss, len(Z)))
    C.prof = (w0, DS, Z)
    if C.is_s4:
        pz = E["PROFILE_Z"]
        d = [abs(E["prof_z"](C.prof, E["PROFILE_S0"] + i * E["PROFILE_DS"]) - pz[i]) for i in range(len(pz))
             if w0 <= E["PROFILE_S0"] + i * E["PROFILE_DS"] <= w1]
        lg.append(u"S4 check: the re-cut differs from the engine's embedded profile by at most %.3f m" % max(d))
    # ---- bed low point, slope, levels
    C.levels, C.slope = {}, None
    rng_ = [i for i in range(len(Z)) if x_c is None or abs(w0 + i * DS - x_c) <= CHANNEL_M]
    i_th = min(rng_ or range(len(Z)), key=lambda i: Z[i])
    C.s_th, C.z_th = w0 + i_th * DS, Z[i_th]
    if C.is_s4:                                     # the engine's surveyed low point and strip, so S4 stays 1:1
        lg.append(u"S4 bed low point: re-cut s %.2f %+.2f, engine s %.2f %+.2f (engine kept)" % (
            C.s_th, C.z_th, E["THALWEG"][0], E["THALWEG"][1]))
        C.s_th, C.z_th = E["THALWEG"]
    if x_c is None:
        lg.append(u"FLAG line %d does not cross the stream centreline: no water levels, no strip" % C.n)
        C.look = compass(-C.u[1], C.u[0])
    else:
        xc, yc = C.xy(x_c)
        d_, ch, t_ = cl_project(CL, cum, xc, yc)
        ang = math.degrees(math.acos(min(1.0, abs(C.u[0] * t_[0] + C.u[1] * t_[1]))))
        C.angle = 90.0 - ang
        if abs(C.angle) > OBLIQUE_DEG:
            lg.append(u"FLAG line %d crosses the stream %.0f deg off square: the flow area is overstated, the levels "
                      u"low" % (C.n, abs(C.angle)))
        lk = (-C.u[1], C.u[0])
        dot = lk[0] * t_[0] + lk[1] * t_[1]
        C.look = compass(*lk) + (u" (downstream)" if dot > 0.7 else u" (upstream)" if dot < -0.7 else u"")
        S, nb = bed_slope(CL, cum, ch, survey, lg)
        C.slope, C.chainage = S, ch
        if S is not None and S > 0:
            hu, hz = [], []
            Zh, _m = cut(h0, h1, HYD_DS)
            for i, z in enumerate(Zh):
                hu.append(h0 + i * HYD_DS - x_c)
                hz.append(z)
            zb = min(hz[i] for i in range(len(hu)) if abs(hu[i]) <= CHANNEL_M)
            for key, Q in (("q100", Q100), ("q500", Q500)):
                h, sp = level_for(hu, hz, Q, S)
                C.levels[key] = (h, sp)
            for sea, ws in SEASON_WATER.items():
                for Q, fill, lab in ws:
                    h, sp = level_for(hu, hz, Q, S)
                    C.levels[(sea, Q)] = (h, sp)
            lg.append(u"levels line %d: chainage %.0f m, bed slope %.2f %% (%d bins), bed %+.2f; Q100 %+.2f, Q500 "
                      u"%+.2f (Manning n %.3f)%s" % (
                          C.n, ch, 100 * S, nb, zb, C.levels["q100"][0], C.levels["q500"][0], N_MANNING,
                          u"; Q500 spills past the 400 m cut" if C.levels["q500"][1] else u""))
        elif S is not None:
            lg.append(u"FLAG line %d: the fitted bed rises downstream (%.2f %%): no water levels" % (C.n, 100 * S))
    # ---- survey crossings and trees
    C.marks = []
    for name, what in MARK_LAYERS.items():
        for pl in survey.get(name, []):
            for a, b in zip(pl[:-1], pl[1:]):
                t = seg_cross(C.A, C.B, a, b)
                if t is not None and w0 <= t * C.L <= w1:
                    C.marks.append((t * C.L, what))
    C.marks.sort()
    C.trees = []
    for name in TREE_LAYERS:
        for pl in survey.get(name, []):
            p = pl[0]
            s, off = C.su(p[0], p[1])
            if w0 + 2.0 <= s <= w1 - 2.0 and abs(off) <= TREE_NEAR_M:
                C.trees.append(s)
    C.trees.sort()
    lg.append(u"survey on line %d: %s; trees within %.0f m: %d" % (C.n, u", ".join(
        u"%s %d" % (w, sum(1 for m in C.marks if m[1] == w)) for w in sorted(set(MARK_LAYERS.values()))),
        TREE_NEAR_M, len(C.trees)))
    context_for(C, BM, tin, ox, oy, lg)


# ================================================================ the section surface and its contents
class Sec(object):
    """the engine's Sec, for one cut: s (m from A) -> page x, level -> page y; d holds the planting and design lists"""

    def __init__(self, E, C, sea):
        self.E, self.C = E, C
        w0, w1 = C.window
        self.prof = C.prof
        self.dir = 1.0
        self.lo, self.hi = w0, w1
        self.X0 = self.Y0 = 0.0
        self.K = E["K"]
        self.has_strip = C.cross is not None and C.slope is not None
        self.strip = (C.s_th - STRIP_W / 2, C.s_th + STRIP_W / 2, STRIP_D) if self.has_strip else (-1e9, -1e9, 0.0)
        self.zb = C.z_th - STRIP_D - 1.9
        self.d = dict(key=u"sfl%d" % C.n, s_from=w0, s_to=w1, grass=[], lavender=[], iris=[], reeds=[], shrubs=[],
                      trees=[], callouts=[], rails=[], regrade=(w1, w1))
        self.banks = []          # engine Sec objects of the S4 design banks
        self.flats = []
        self.steps = []
        self.design = []         # (s from, s to) under the design
        left, right = [], []
        if C.is_s4:
            for dsec in E["SECTIONS"]:
                b = E["Sec"](dsec, self.prof)
                self.banks.append(b)
                ra, rb = dsec["regrade"]
                k = [i for i, p in enumerate(b.V) if abs(p[0] - rb) < 1e-9][0]
                pts = b.V[:k + 1]
                if b.dir < 0:
                    right = pts[::-1]
                else:
                    left = pts
                self.design.append(tuple(sorted((dsec["s_from"], rb))))
                for kk in ("grass", "lavender", "iris", "reeds", "shrubs", "trees", "callouts"):
                    self.d[kk] += list(dsec.get(kk, []))
                self.flats += [(sa, sb, z, mat, lab) for sa, sb, z, mat, lab in b.flats]
            self.d["rails"] = [(s, side) for dsec in E["SECTIONS"] for s, side in dsec["rails"]]
            self.d["balcony"] = E["SECTIONS"][1].get("balcony")
            self.d["pergola"] = E["SECTIONS"][1].get("pergola")
        self.V = self._surface(left, right)
        if not C.is_s4:
            self._rule_planting(sea)

    def X(self, s):
        return self.X0 + (s - self.lo) * self.K

    def Y(self, z):
        return self.Y0 + (z - self.zb) * self.K

    def P(self, s, z):
        return (self.X(s), self.Y(z))

    def ex(self, s):
        return self.E["prof_z"](self.prof, s)

    def _surface(self, left, right):
        w0, w1 = self.lo, self.hi
        a = left[-1][0] if left else w0
        b = right[0][0] if right else w1
        mid = []
        n = int(round((b - a) / DS))
        for i in range(n + 1):
            mid.append((a + (b - a) * i / max(n, 1), None))
        V = list(left)
        sa, sb, dep = self.strip
        for s, _ in mid:
            if sa < s < sb:
                continue
            if left and s <= a + 1e-9:
                continue
            if right and s >= b - 1e-9:
                continue
            if V and V[-1][0] < sa and s > sb:            # the strip: a 4 m low-flow channel 0.30 m into the bed
                zt = self.C.z_th
                V += [(sa, self.ex(sa)), (sa, zt - dep), (sb, zt - dep), (sb, self.ex(sb))]
            V.append((s, self.ex(s)))
        V += list(right)
        return V

    def surf(self, s):
        V = self.V
        best = None
        xs = getattr(self, "_xs", None)
        if xs is None:
            xs = [p[0] for p in V]
            self._xs = xs = xs if all(xs[i] <= xs[i + 1] + 1e-9 for i in range(len(xs) - 1)) else False
        if xs:
            i0 = max(0, bisect.bisect_left(xs, s - 1e-6) - 2)
            i1 = min(len(V) - 1, bisect.bisect_right(xs, s + 1e-6) + 1)
        else:
            i0, i1 = 0, len(V) - 1
        for i in range(i0, i1):
            a, b = V[i], V[i + 1]
            lo_, hi_ = sorted((a[0], b[0]))
            if lo_ - 1e-9 <= s <= hi_ + 1e-9:
                if abs(b[0] - a[0]) < 1e-9:
                    z = min(a[1], b[1])
                else:
                    z = a[1] + (b[1] - a[1]) * (s - a[0]) / (b[0] - a[0])
                best = z if best is None else min(best, z)
        return best if best is not None else self.ex(s)

    def built(self, s):
        """on a road or inside a building the line cuts: no planting, no people"""
        C = self.C
        return any(a <= s <= b for a, b in C.roads) or any(t[4] and t[0] <= s <= t[1] for t in C.bld)

    def _rule_planting(self, sea):
        """design intention (ours): reeds and iris on the wet bed (up to WET_BAND_M above the bed, never in the strip),
        meadow grass above it; survey trees on ground above Q100 (drawn at the engine's plane size)"""
        C, d = self.C, self.d
        wet = C.z_th + WET_BAND_M
        sa, sb, _ = self.strip
        runs, cur, kind = [], None, None
        s = self.lo
        while s <= self.hi + 1e-9:
            if sa - 0.4 <= s <= sb + 0.4 or self.built(s):
                k = None
            else:
                k = "wet" if self.surf(s) <= wet else "dry"
            if k != kind:
                if cur is not None and kind is not None:
                    runs.append((cur, s, kind))
                cur, kind = s, k
            s += 0.5
        if kind is not None and cur is not None:
            runs.append((cur, self.hi, kind))
        n_r = 0
        for a, b, k in runs:
            if b - a < 0.8:
                continue
            if k == "dry":
                d["grass"].append((a, b))
                continue
            x = a
            while x < b - 0.5:                                 # reeds 3 m, iris 1.2 m, alternating
                y = min(b, x + (3.0 if n_r % 2 == 0 else 1.2))
                if n_r % 2 == 0:
                    d["reeds"].append((x, y, 2.0))
                else:
                    d["iris"].append((x, y))
                n_r += 1
                x = y
        q100 = C.levels.get("q100", (None,))[0]
        wet = []
        for s in C.trees:
            if q100 is None or self.surf(s) >= q100:
                d["trees"].append((s, 3.9, 7.5, "plane"))
            else:
                wet.append(s)
        if wet:                                           # v1.4: one log line per section, not one per tree
            C.notes.append(u"line %d: %d survey tree(s) not drawn, they stand below Q100 (at s %s m)" % (
                C.n, len(wet), u", ".join(u"%.1f" % s for s in wet)))
        if d["reeds"]:
            r0 = max(d["reeds"], key=lambda r: abs(r[1] - r[0]))
            d["callouts"].append(((r0[0] + r0[1]) / 2, None, u"Common reed (Kamış)"))
        if d["iris"]:
            i0 = max(d["iris"], key=lambda r: abs(r[1] - r[0]))
            d["callouts"].append(((i0[0] + i0[1]) / 2, None, u"Yellow flag iris (Sarı süsen)"))
        if d["grass"]:
            g0 = max(d["grass"], key=lambda r: abs(r[1] - r[0]))
            d["callouts"].append(((g0[0] + g0[1]) / 2, None, u"Meadow, native grasses"))
        for s, _r, _h, _k in d["trees"][:3]:
            d["callouts"].append((s, None, u"Tree (survey point)"))
        if self.has_strip:
            d["callouts"].append((C.s_th, None, u"Summer water strip 400 cm × 0.30 m"))
        for a, b in C.roads:
            d["callouts"].append(((a + b) / 2, None, u"Road"))
        for x in C.streets:
            d["callouts"].append((x, None, u"Street"))
        back = [t for t in C.bld if not t[4]]
        if back:
            t = max(back, key=lambda t: t[1] - t[0])
            d["callouts"].append(((t[0] + t[1]) / 2, (t[2] if t[2] is not None else self.ex((t[0] + t[1]) / 2)) + t[3],
                                  u"Buildings behind the cut"))
        for t in C.bld:
            if t[4]:
                d["callouts"].append(((t[0] + t[1]) / 2, self.ex((t[0] + t[1]) / 2) + t[3],
                                      u"Building, %d floor%s" % (t[6], u"" if t[6] == 1 else u"s") if t[6] else u"Building"))


class _Bank(object):
    """an S4 design bank seen through the combined section: its own flats, steps, stair, dir and regrade, the
    combined surface and page mapping"""

    def __init__(self, S, b):
        self.S, self.b = S, b
        self.flats, self.steps, self.dir, self.d = b.flats, b.steps, b.dir, b.d
        self.stair = getattr(b, "stair", None)

    def __getattr__(self, k):
        return getattr(self.S, k)


def people_for(S, sea_key, E):
    """S4: the engine's people of both banks for the season; other cuts: walkers on dry, gentle ground every ~9 m"""
    if S.C.is_s4:
        for dsea in E["SEASONS"]:
            if dsea["key"] == sea_key:
                return (list(dsea["people"].get("1", [])) + list(dsea["people"].get("2", [])),
                        list(dsea["bikes"].get("1", [])) + list(dsea["bikes"].get("2", [])))
        return [], []
    out = []
    kinds = (0, 1, 2, 4, 3)
    s = S.lo + 4.0
    n = 0
    while s < S.hi - 4.0:
        g = S.surf(s)
        if abs(S.surf(s + 0.5) - S.surf(s - 0.5)) < 0.25 and not any(t[4] and t[0] <= s <= t[1] for t in S.C.bld):
            out.append((s, kinds[n % len(kinds)], n % 2 == 1))
            n += 1
            s += 9.0
        else:
            s += 1.0
        _ = g
    return out, []


def season_water(C, sea):
    """[(level, filled, label, dash)] of the season on this cut"""
    out = []
    for Q, fill, lab in SEASON_WATER[sea]:
        lv = C.levels.get((sea, Q))
        if lv:
            out.append((lv[0], fill, lab % (lv[0], lv[0] - C.z_th), None if fill else [1.6, 0.6, 0.3, 0.6]))
    return out


def draw_cut(E, C, sea, den, x_left, y_top, with_text=True):
    """one season of one cut on a new engine Page at 1:den; returns (page, S, bottom y)"""
    E["K"] = 1000.0 / den
    E["SEA"] = dict(E["SEASON_LOOK"][sea])
    S = Sec(E, C, sea)
    E["STRIP"] = S.strip if S.has_strip else (-1e9, -1e9, 0.0)
    E["THALWEG"] = (C.s_th, C.z_th)
    pg = E["Page"](u"sfl%d_%s" % (C.n, sea), u"")
    d = S.d
    size = 2.65
    K = E["K"]
    q100 = C.levels.get("q100", (None,))[0]
    q500 = C.levels.get("q500", (None,))[0]
    tops = [S.surf(t[0]) + t[2] for t in d["trees"]] + [max(z for _, z in S.V) + 1.9]
    tops += [(t[2] if t[2] is not None else S.ex((t[0] + t[1]) / 2)) + t[3] + 0.5 for t in C.bld]
    if d.get("pergola"):
        tops.append(E["DRY"] + max(p[2] for p in d["pergola"]["plates"]) + 0.1)
    z_top = max(tops)
    S.X0 = x_left
    items = list(d["callouts"]) if with_text else []
    placed = E["place_labels"](S, [(S.X(s), 0.0, txt) for s, z, txt in items], size) if items else []
    rows = (max(p["row"] for p in placed) + 1) if placed else 0
    gap = size * 2 * 1.25 + 3.0
    title_h = 16.0 if with_text else 0.0
    label_h = rows * gap + (4.0 if rows else 0.0)
    S.Y0 = y_top - title_h - label_h - (z_top - S.zb) * K - (6.0 if with_text else 0.0)
    by_x = dict((round(S.X(s), 3), (s, z)) for s, z, txt in items)
    for p in placed:
        s, z = by_x[round(p["x"], 3)]
        p["y"] = S.Y(S.surf(s) + 0.02 if z is None else z)
    if with_text:
        pg.text(u"SECTION %s" % C.name, x_left, y_top - 6.0, 5.0, E["INK"], bold=True, layer="title")
        pg.text(u"SCALE 1:%d" % den, x_left, y_top - 11.5, 3.6, E["INK"], layer="title")
        pg.text(u"both banks · looking %s" % C.look, x_left + 34.0, y_top - 11.5, 2.0, E["INK2"], layer="title")
    # back to front: the context buildings first (the earth poche covers them below the ground line)
    for a, b, zb_, h, is_cut, dist, fl in C.bld:
        base = zb_ if zb_ is not None else min(S.ex(a), S.ex(b))
        ring = [S.P(a, S.zb), S.P(b, S.zb), S.P(b, base + h), S.P(a, base + h)]
        pg.poly([ring], fill=BLD_CUT_FILL if is_cut else BLD_FILL, stroke=BLD_EDGE, lw=0.25 if is_cut else 0.1,
                layer="context buildings")
        if fl and fl > 1 and (b - a) * K > 3.0:
            for i in range(1, fl):
                zf = base + h * i / fl
                pg.line([S.P(a, zf), S.P(b, zf)], BLD_EDGE, 0.05, layer="context buildings")
    for s, r_, h, kind in d["trees"]:
        g = S.surf(s)
        if q500 is not None and g < q500 - 1e-6 and C.is_s4:
            continue
        X, Y = S.P(s, g)
        E["veg_tree"](pg, X, Y, h * K, 2 * r_ * K, (d["key"], round(s, 2)))
    people, bikes = people_for(S, sea, E)
    bal = d.get("balcony")
    on_bal = []
    if bal:
        lo_b, hi_b = min(bal["s0"], bal["s1"]), max(bal["s0"], bal["s1"])
        on_bal = [(p[0], 5, p[2]) for p in people if p[1] == 3 and lo_b <= p[0] <= hi_b]
        people = [p for p in people if not (p[1] == 3 and lo_b <= p[0] <= hi_b)]
    if d.get("pergola"):
        E["pergola"](pg, S, d["pergola"])
    if bal:
        E["balcony"](pg, S, bal, on_bal)
    if q500 is not None:
        E["level_line"](pg, S, q500, u"Q500 %+.2f (calculated on this cut)" % q500, [2.0, 1.0])
        E["level_line"](pg, S, q100, u"Q100 %+.2f (calculated on this cut)" % q100, [0.8, 0.8])
    sw = season_water(C, sea)
    for z, fill_, lab, dash in sw:
        if not fill_:
            E["level_line"](pg, S, z, lab, dash, colour=E["WATER_LINE"])
    E["poche"](pg, S)
    E["soft_ground"](pg, S)
    for b in S.banks:
        E["walls_and_slabs"](pg, _Bank(S, b))
    E["existing_ground"](pg, S)
    for a, b in C.roads:                               # the road surface on the ground line
        n = max(2, int((b - a) / DS))
        top = [(a + (b - a) * i / n) for i in range(n + 1)]
        ring = [S.P(x, S.surf(x)) for x in top] + [S.P(x, S.surf(x) - ROAD_T) for x in reversed(top)]
        pg.poly([ring], fill=ROAD_FILL, stroke=None, layer="context roads")
    for a, b in d["grass"]:
        E["tufts"](pg, S, a, b)
    for a, b in d["lavender"]:
        E["lavender"](pg, S, a, b)
    for s, h, w in d["shrubs"]:
        E["shrub"](pg, S, s, h, w)
    for a, b, h in d["reeds"]:
        E["reeds"](pg, S, a, b, h)
    for a, b in d["iris"]:
        E["iris"](pg, S, a, b)
    filled = [w for w in sw if w[1]]
    for z, fill_, lab, dash in filled:
        E["water"](pg, S, z)
        E["level_line"](pg, S, z, lab, None, colour=E["FLOOD"])
    held = STRIP_HELD[sea] and S.has_strip
    if held:
        E["water"](pg, S, C.z_th)
        if not filled:
            E["level_line"](pg, S, C.z_th, u"continuous strip %+.2f, 0.30 m (design)" % C.z_th, None,
                            colour=E["FLOOD"])
    wl = max([C.z_th if held else -99.0] + [w[0] for w in filled])
    for s, kind, flip in people:
        g = S.surf(s)
        if g < wl + 0.02 and kind != 8:
            continue                                        # never a person in the water (Aras 31 Oct 11:28)
        E["figure"](pg, S, s, kind, flip)
    for s, flip in bikes:
        E["bike"](pg, S, s, flip)
    for s, side in d["rails"]:
        E["handrail"](pg, S, s + side * 0.15, S.surf(s + side * 0.3))
    if with_text and placed:
        E["callouts"](pg, S, placed, S.Y(z_top) + 6.0, size)
    spread_levels(E, pg, S, short=True)
    y_band = S.Y(S.zb) - 3.0
    if with_text:
        band(E, pg, S, y_band - BAND_H, h=BAND_H)
        y_band -= BAND_H + 12.0
        bar = 10.0 if den <= 500 else 50.0              # scale bar beside the drawing (SCRIPT_STANDARD s.8)
        xb, yb = S.X(S.lo), y_band - 4.0
        pg.line([(xb, yb), (xb + bar * K, yb)], E["INK"], 0.3, layer="title")
        for i in (0.0, 0.5, 1.0):
            pg.line([(xb + bar * K * i, yb), (xb + bar * K * i, yb + 1.2)], E["INK"], 0.2, layer="title")
        pg.text(u"0", xb, yb - 3.0, 2.0, E["INK"], align="C", layer="title")
        pg.text(u"%d m" % bar, xb + bar * K, yb - 3.0, 2.0, E["INK"], align="C", layer="title")
        pg.text(u"1:%d" % den, xb + bar * K + 8.0, yb - 0.6, 2.0, E["INK2"], align="L", layer="title")
        y_band = yb - 6.0
    return pg, S, y_band


def spread_levels(E, pg, S, short=False, gap=2.6):
    """v1.1: the level texts (engine level_line puts them on the cut's right end, over the design) move just right of
    the cut, top to bottom in level order, at least gap mm apart, each with a thin tick from the cut end"""
    lv = [it for it in pg.items if it[0] == "text" and it[8] == "levels"]
    if not lv:
        return
    x_end = S.X(S.hi)

    def _sign(it):                                       # the engine's level sign (triangle + bar) at the cut end
        if it[0] == "poly" and it[6] == "levels" and len(it[1]) == 1 and len(it[1][0]) == 3:
            return all(x_end - 4.6 <= p[0] <= x_end - 1.4 for p in it[1][0])
        if it[0] == "line" and it[5] == "levels" and len(it[1]) == 2 and abs(it[1][1][0] - it[1][0][0]) <= 1.7:
            return all(x_end - 4.6 <= p[0] <= x_end - 1.4 for p in it[1]) and abs(it[1][1][1] - it[1][0][1]) < 1e-6
        return False
    pg.items = [it for it in pg.items if not (it[0] == "text" and it[8] == "levels") and not _sign(it)]
    xr = x_end + 3.0
    y_prev = None
    for it in sorted(lv, key=lambda t: -t[3]):
        txt = it[1].split(u" (")[0] if short else it[1]
        y0 = it[3] - 0.6
        y = y0 if y_prev is None else min(y0, y_prev - gap)
        y_prev = y
        pg.line([(x_end + 0.3, y0), (xr - 0.5, y)], it[5], 0.08, layer="levels")
        X = xr + 1.3                                     # the level sign beside its value
        pg.poly([[(X - 1.3, y + 1.9), (X + 1.3, y + 1.9), (X, y)]], fill=None, stroke=it[5], lw=0.2, layer="levels")
        pg.line([(X - 0.8, y - 0.6), (X + 0.8, y - 0.6)], it[5], 0.2, layer="levels")
        pg.text(txt, xr + 3.4, y - 0.4, it[4], it[5], bold=it[6], align="L", layer="levels")


def band(E, pg, S, y, h=9.0):
    """the material band under the cut (the engine's swatches, no widths): design flats on S4, else bed gravel, the
    strip and native vegetation by the rule planting"""
    C = S.C
    items = [(min(sa, sb), max(sa, sb), mat, lab) for sa, sb, z, mat, lab in S.flats]
    items += [(a, b, "road", u"Road") for a, b in C.roads]        # "road": the engine's plain grey swatch
    items += [(t[0], t[1], "concrete", u"Building") for t in C.bld if t[4]]
    if C.is_s4:                                     # the engine's own band of both banks
        for b_ in S.banks:
            ra, rb = b_.d["regrade"]
            items.append((min(ra, rb), max(ra, rb), "gravel", u"Stream gravel"))
            items += [(min(a, b), max(a, b), m, l) for a, b, m, l in b_.d["band_more"]]
    covered = sorted((a, b) for a, b, m, l in items)
    wet = C.z_th + WET_BAND_M
    s, cur = S.lo, None
    sa_, sb_, _ = S.strip
    while s < S.hi - 1e-9:
        e = min(S.hi, s + 0.5)
        m = (s + e) / 2
        if any(a - 1e-6 <= m <= b + 1e-6 for a, b in covered):
            k = None
        elif sa_ <= m <= sb_:
            k = ("water", u"Summer water strip")
        elif S.surf(m) <= wet or any(a <= m <= b for a, b in S.design):
            k = ("gravel", u"Stream gravel")
        else:
            k = ("veg", u"Native vegetation")
        if k is not None:
            if cur and cur[2] == k[0] and cur[3] == k[1] and abs(cur[1] - s) < 1e-6:
                cur = (cur[0], e, k[0], k[1])
            else:
                if cur:
                    items.append(cur)
                cur = (s, e, k[0], k[1])
        else:
            if cur:
                items.append(cur)
            cur = None
        s = e
    if cur:
        items.append(cur)
    items.sort(key=lambda t: t[0])
    merged = []
    for a, b, mat, lab in items:
        if merged and merged[-1][3] == lab and abs(merged[-1][1] - a) < 0.6:
            merged[-1] = (merged[-1][0], b, mat, lab)
        else:
            merged.append((a, b, mat, lab))
    drop = 0.0
    for j, (a, b, mat, lab) in enumerate(merged):
        x0, x1 = S.X(a), S.X(b)
        if x1 - x0 < 0.3:
            continue
        E["swatch"](pg, x0, x1, y, h, mat, S.d["key"])
        if x1 - x0 < 6.0:
            continue                                     # too short for a name: the swatch alone
        lines = E["wrap"](lab, max(6, int((x1 - x0 + 4.0) / 1.1)))
        y0 = y - 2.8 - (drop if j % 2 else 0.0)
        for i, l in enumerate(lines):
            pg.text(l, (x0 + x1) / 2, y0 - i * 2.6, 2.0, E["INK2"], align="C", layer="band")
        if j % 2 == 0:
            drop = len(lines) * 2.6 + 0.6


# ================================================================ PDF (vector, layers as PDF layers)
PT = 25.4 / 72.0
_TR = {u"Ğ": 129, u"ğ": 141, u"İ": 143, u"ı": 144, u"Ş": 157, u"ş": 158, u"–": 150, u"—": 151, u"’": 146,
       u"‘": 145, u"“": 147, u"”": 148, u"•": 149, u"€": 128}
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"


def _pdf_txt(s):
    out = bytearray()
    for ch in s:
        c = _TR.get(ch)
        if c is None:
            o = ord(ch)
            c = o if (32 <= o < 127 or 160 <= o < 256) else 63
        if c in (40, 41, 92):
            out += b"\\"
        out.append(c)
    return bytes(out)


def _col(h):
    h = (h or "000000").lstrip("#")
    return "%.3f %.3f %.3f" % (int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0)


def _f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def write_pdf(path, pages, title):
    """pages: [(w_mm, h_mm, items)] engine Page items, page mm, y up"""
    objs = []

    def add(b):
        objs.append(b)
        return len(objs)
    layers = []
    for _, _, items in pages:
        for it in items:
            ly = it[6] if it[0] == "poly" else it[5] if it[0] == "line" else it[7] if it[0] == "circle" else it[8]
            if ly not in layers:
                layers.append(ly)
    ocg = dict((ly, add(("<< /Type /OCG /Name (%s) >>" % _pdf_txt(u"%s" % ly).decode("latin-1")).encode("latin-1")))
               for ly in layers)
    f_r = add(("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding << /Type /Encoding /BaseEncoding "
               "/WinAnsiEncoding %s >> >>" % _DIFF).encode())
    f_b = add(("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding << /Type /Encoding /BaseEncoding "
               "/WinAnsiEncoding %s >> >>" % _DIFF).encode())
    alphas = {}
    pages_id = len(objs) + 1 + 2 * len(pages) + 50          # placeholder, set below
    kids = []
    content_ids = []
    for w, h, items in pages:
        k = 72.0 / 25.4
        A = ["%s 0 0 %s 0 0 cm" % (_f(k), _f(k)), "1 J 1 j"]
        cur = None
        for it in items:
            t = it[0]
            ly = it[6] if t == "poly" else it[5] if t == "line" else it[7] if t == "circle" else it[8]
            if ly != cur:
                if cur is not None:
                    A.append("EMC")
                A.append("/OC /oc%d BDC" % ocg[ly])
                cur = ly
            if t == "poly":
                rings, fill, stroke, lw, dash, _ly, join, stripes, alpha = it[1:10]
                if not fill and not stroke:
                    continue
                A.append("q")
                if alpha is not None and alpha < 0.999:
                    a = round(alpha * 20) / 20.0
                    alphas[a] = 1
                    A.append("/GA%d gs" % int(a * 100))
                pth = []
                for r in rings:
                    pth.append("%s %s m" % (_f(r[0][0]), _f(r[0][1])))
                    pth += ["%s %s l" % (_f(p[0]), _f(p[1])) for p in r[1:]]
                    pth.append("h")
                A += pth
                if fill:
                    A.append("%s rg" % _col(fill))
                if stroke:
                    A.append("%s RG %s w" % (_col(stroke), _f(lw or 0.1)))
                    A.append(("[%s] 0 d" % " ".join(_f(v) for v in dash)) if dash else "[] 0 d")
                A.append("B" if (fill and stroke) else "f" if fill else "S")
                A.append("Q")
            elif t == "line":
                pts, stroke, lw, dash, _ly, cap = it[1:7]
                A.append("q %s RG %s w %d J" % (_col(stroke), _f(lw or 0.1), {0: 0, 1: 1, 2: 2}.get(cap, 1)))
                A.append(("[%s] 0 d" % " ".join(_f(v) for v in dash)) if dash else "[] 0 d")
                A.append("%s %s m" % (_f(pts[0][0]), _f(pts[0][1])))
                A += ["%s %s l" % (_f(p[0]), _f(p[1])) for p in pts[1:]]
                A.append("S Q")
            elif t == "circle":
                cx, cy, r, fill, stroke, lw = it[1:7]
                c = 0.5523 * r
                A.append("q")
                A.append("%s %s m %s %s %s %s %s %s c %s %s %s %s %s %s c %s %s %s %s %s %s c %s %s %s %s %s %s c h" % tuple(
                    _f(v) for v in (cx + r, cy, cx + r, cy + c, cx + c, cy + r, cx, cy + r, cx - c, cy + r, cx - r, cy + c,
                                    cx - r, cy, cx - r, cy - c, cx - c, cy - r, cx, cy - r, cx + c, cy - r, cx + r,
                                    cy - c, cx + r, cy)))
                if fill:
                    A.append("%s rg" % _col(fill))
                if stroke:
                    A.append("%s RG %s w" % (_col(stroke), _f(lw or 0.1)))
                A.append("B" if (fill and stroke) else "f" if fill else "S")
                A.append("Q")
            elif t == "text":
                s, x, y, size, color, bold, align = it[1:8]
                wmm = text_w_any(s, size, bold)
                x0 = x - {"L": 0.0, "C": wmm / 2.0, "R": wmm}.get(align, 0.0)
                pt = size / PT
                A.append("BT /%s %s Tf %s rg %s 0 0 %s %s %s Tm (" % ("F2" if bold else "F1", _f(pt), _col(color),
                                                                     _f(PT), _f(PT), _f(x0), _f(y)))
                A.append(None)
                A[-1] = _pdf_txt(s)
                A.append(") Tj ET")
        if cur is not None:
            A.append("EMC")
        body = bytearray()
        for a in A:
            if isinstance(a, bytes):
                body += a
            else:
                body += a.encode("latin-1") + (b"" if a.endswith("(") else b"\n")
        cid = add(b"<< /Length %d >>\nstream\n" % len(body) + bytes(body) + b"\nendstream")
        content_ids.append((cid, w, h))
    gs = " ".join("/GA%d << /Type /ExtGState /ca %s /CA %s >>" % (int(a * 100), _f(a), _f(a)) for a in sorted(alphas))
    props = " ".join("/oc%d %d 0 R" % (i, i) for i in ocg.values())
    res = add(("<< /Font << /F1 %d 0 R /F2 %d 0 R >> /ExtGState << %s >> /Properties << %s >> >>" % (
        f_r, f_b, gs, props)).encode("latin-1"))
    pages_id = len(objs) + len(content_ids) + 1
    for cid, w, h in content_ids:
        kids.append(add(("<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %s %s] /Contents %d 0 R /Resources %d 0 R >>" % (
            pages_id, _f(w / PT), _f(h / PT), cid, res)).encode()))
    assert add(("<< /Type /Pages /Kids [%s] /Count %d >>" % (" ".join("%d 0 R" % k for k in kids), len(kids))).encode()) \
        == pages_id
    oc = " ".join("%d 0 R" % i for i in ocg.values())
    cat = add(("<< /Type /Catalog /Pages %d 0 R /OCProperties << /OCGs [%s] /D << /Order [%s] /ON [%s] >> >> >>" % (
        pages_id, oc, oc, oc)).encode())
    info = add(b"<< /Title (" + _pdf_txt(title) + b") /Producer (Bergama Sections) >>")
    out = bytearray(b"%PDF-1.5\n%\xe2\xe3\xcf\xd3\n")
    offs = []
    for i, b in enumerate(objs):
        offs.append(len(out))
        out += b"%d 0 obj\n" % (i + 1) + b + b"\nendobj\n"
    x = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for o in offs:
        out += b"%010d 00000 n \n" % o
    out += b"trailer\n<< /Size %d /Root %d 0 R /Info %d 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, cat, info, x)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "wb") as f:
            f.write(bytes(out))
    except PermissionError:                                   # open in a viewer: a timed name
        path = path[:-4] + time.strftime("_%H%M%S") + ".pdf"
        with open(path, "wb") as f:
            f.write(bytes(out))
    return path


_ENGINE_W = []


def text_w_any(s, size, bold):
    if _ENGINE_W:
        return _ENGINE_W[0](s, size, bold)
    return 0.5 * size * len(s)


def items_bbox(items):
    xs, ys = [], []
    for it in items:
        t = it[0]
        if t == "poly":
            for r in it[1]:
                xs += [p[0] for p in r]
                ys += [p[1] for p in r]
        elif t == "line":
            xs += [p[0] for p in it[1]]
            ys += [p[1] for p in it[1]]
        elif t == "circle":
            xs += [it[1] - it[3], it[1] + it[3]]
            ys += [it[2] - it[3], it[2] + it[3]]
        elif t == "text":
            w = text_w_any(it[1], it[4], it[6])
            x0 = it[2] - {"L": 0.0, "C": w / 2.0, "R": w}.get(it[7], 0.0)
            xs += [x0, x0 + w]
            ys += [it[3] - 0.3 * it[4], it[3] + it[4]]
    return min(xs), min(ys), max(xs), max(ys)


# ================================================================ booklet items (bergama-items/1)
def _lines_in():
    g = globals()
    v = g.get("section_line")
    if v is None:
        return []
    if not isinstance(v, (list, tuple)):
        v = [v]
    out = []
    for ln in v:
        try:
            if hasattr(ln, "From"):
                a, b = ln.From, ln.To
            elif hasattr(ln, "PointAtStart"):
                a, b = ln.PointAtStart, ln.PointAtEnd
            else:
                continue
            if math.hypot(b.X - a.X, b.Y - a.Y) > 1.0:
                out.append(((a.X, a.Y), (b.X, b.Y)))
        except Exception:
            pass
    return out


def model_lines(log):
    """the curves on layer section_lines of the open model (Aras 12 Nov 10:53 UTC: "i will give the section lines in
    .3dm"): [(name, A, B)], the name = the object's name, else S1, S2 ... in the layer's order"""
    try:
        import Rhino
        doc = Rhino.RhinoDoc.ActiveDoc
        out = []
        for o in _layer_objs(doc, SECTION_LAYER):
            g = o.Geometry
            if not isinstance(g, Rhino.Geometry.Curve):
                continue
            a, b = g.PointAtStart, g.PointAtEnd
            if math.hypot(b.X - a.X, b.Y - a.Y) <= 1.0:
                continue
            nm = (o.Attributes.Name or u"").strip() or u"S%d" % (len(out) + 1)
            out.append((nm, (a.X, a.Y), (b.X, b.Y)))
        if out:
            log.append(u"section_line: nothing wired: %d line(s) read from the model layer %s (%s)" % (
                len(out), SECTION_LAYER, u", ".join(n for n, _, _ in out)))
        return out
    except Exception as ex:
        log.append(u"FLAG model layer %s not read (%s)" % (SECTION_LAYER, type(ex).__name__))
        return []


def named_lines(log):
    """the node sections of Data/section_lines.json: [(name, A, B)]"""
    p = os.path.join(DATA_DIR, "section_lines.json")
    try:
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        out = [(k, tuple(v[0]), tuple(v[1])) for k, v in sorted(d["lines"].items())]
        log.append(u"section_line: nothing wired: %d named lines read from %s" % (len(out), p))
        return out
    except Exception as ex:
        log.append(u"FLAG section lines: %s not read (%s)" % (p, type(ex).__name__))
        return []


def main():
    global MAX_LEN_M
    t0 = time.time()
    log = []
    E = load_engine(log)
    E["_DRY0"] = E["DRY"]
    _ENGINE_W[:] = [E["text_w"]]
    den = int(globals().get("scale") or 500)
    MAX_LEN_M = 2.0 * float(globals().get("half_width") or 100)
    CL, cum = load_centreline(log)
    wired = _lines_in()
    s4a, s4b = E["S4_A"], E["S4_B"]
    lines = [(u"L%d" % (i + 1), a, b) for i, (a, b) in enumerate(wired)] or model_lines(log) or named_lines(log)
    if not lines:
        lines = [(u"S4", s4a, s4b)]
        log.append(u"no lines: S4 (the 27 Oct cut) drawn")
    cuts = []
    for i, (name, a, b) in enumerate(lines):
        C = Cut(i + 1, a, b, name, name)
        for (p, q) in ((a, b), (b, a)):
            if math.hypot(p[0] - s4a[0], p[1] - s4a[1]) < 1.0 and math.hypot(q[0] - s4b[0], q[1] - s4b[1]) < 1.0:
                C = Cut(i + 1, s4a, s4b, u"S4", u"S4")
                C.is_s4 = True
        cuts.append(C)
    BM = load_basemap(log)
    # the survey is read ONCE for all lines (build once, Aras 29 Oct): the box holds every line's corridor
    pad = max(CORRIDOR_STEPS[-1], SLOPE_HALF + 20.0) + HYD_HALF
    xs = [p[0] for C in cuts for p in (C.A, C.B)]
    ys = [p[1] for C in cuts for p in (C.A, C.B)]
    survey = read_survey((min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad), log)
    res = []
    pages = []
    os.makedirs(OUT_DIR, exist_ok=True)
    for C in cuts:
        try:
            C.survey = survey
            build_cut(C, CL, cum, E, log, BM)
            pg, S, ybot = draw_cut(E, C, SEASON, den, 15.0, 0.0)
            b = items_bbox(pg.items)
            w, h = b[2] - b[0] + 30.0, b[3] - b[1] + 30.0
            moved = [_shift(it, 15.0 - b[0], 15.0 - b[1]) for it in pg.items]
            pages.append((w, h, moved))
            log.append(u"page %d: %s (%.0f x %.0f mm, 1:%d)" % (len(pages), C.name, w, h, den))
        except Exception as ex:
            import traceback as _tb
            log.append(u"FLAG section %s not drawn: %s: %s | %s" % (C.name, type(ex).__name__, ex,
                                                                    u" / ".join(_tb.format_exc()[-500:].splitlines())))
            log += C.notes
            continue
        log += C.notes
        res.append(dict(name=C.name, A=list(C.A), B=list(C.B), window=list(C.window), look=C.look,
                        bed_low=[round(C.s_th, 2), round(C.z_th, 2)], slope=C.slope,
                        levels=dict((k if isinstance(k, str) else u"%s %.3g m3/s" % k, round(v[0], 2))
                                    for k, v in C.levels.items()),
                        marks=[[round(s_, 2), w_] for s_, w_ in C.marks], trees=[round(s_, 2) for s_ in C.trees],
                        roads=[[round(a, 2), round(b_, 2)] for a, b_ in C.roads],
                        buildings=[dict(s=[round(t[0], 2), round(t[1], 2)], h=t[3], cut=t[4], behind_m=round(t[5], 1))
                                   for t in C.bld]))
    if pages:
        # one page: first cut on top (PDF y is up), GAP_MM between cuts, left edges aligned
        GAP_MM = 20.0
        pw = max(w for w, _, _ in pages)
        ph = sum(h for _, h, _ in pages) + GAP_MM * (len(pages) - 1)
        allit, y = [], ph
        for w, h, its in pages:
            y -= h
            allit += [_shift(it, 0.0, y) for it in its]
            y -= GAP_MM
        log.append(u"one page %.0f x %.0f mm, %d cut(s)" % (pw, ph, len(pages)))
        pages = [(pw, ph, allit)]
        p = write_pdf(os.path.join(OUT_DIR, u"Sections.pdf"), pages,
                      u"Sections %s, both banks, 1:%d" % (u", ".join(r_["name"] for r_ in res), den))
        log.append(u"%s  %s" % (p, time.strftime("%H:%M:%S")))
    else:
        log.append(u"FLAG no section drawn: no PDF written")
    os.makedirs(CACHE_DIR, exist_ok=True)
    pj = os.path.join(CACHE_DIR, "sections.json")
    with open(pj, "w", encoding="utf-8") as f:
        json.dump(dict(version=VERSION, run=time.strftime("%Y-%m-%d %H:%M:%S"), scale=den, cuts=res), f,
                  ensure_ascii=False, indent=1)
    log.append(u"%s  %s" % (pj, time.strftime("%H:%M:%S")))
    flags = [l for l in log if l.startswith(u"FLAG")]
    return u"%s\n%s %s, %d of %d section(s) drawn, %d FLAG line(s), %.1f s" % (
        u"\n".join(log), GH_LABEL, VERSION, len(res), len(cuts), len(flags), time.time() - t0)


def _shift(it, dx, dy):
    t = it[0]
    if t == "poly":
        return (t, [[(p[0] + dx, p[1] + dy) for p in r] for r in it[1]]) + tuple(it[2:])
    if t == "line":
        return (t, [(p[0] + dx, p[1] + dy) for p in it[1]]) + tuple(it[2:])
    if t == "circle":
        return (t, it[1] + dx, it[2] + dy) + tuple(it[3:])
    if t == "text":
        return (t, it[1], it[2] + dx, it[3] + dy) + tuple(it[4:])
    return it


# ---- Grasshopper wiring (same in every script) ----
def chain_fire(v, key):
    if isinstance(v, (list, tuple)):
        v = next((x for x in v if x is not None), None)
    s = str(v) if v is not None else ""
    if not s.startswith("done "):
        return False
    try:
        import scriptcontext as _scx
        try:
            key = key + ":" + str(ghenv.Component.InstanceGuid)              # noqa: F821
        except Exception:
            pass
        if _scx.sticky.get(key) == s:
            return False
        _scx.sticky[key] = s
        return True
    except Exception:
        return False


def done_text(ran, ok, secs):
    return ("done " if ok else "ERROR ") + time.strftime("%H:%M:%S") + ".%02d" % int((time.time() % 1) * 100) + \
        " · %.0f s" % secs if ran else None


def write_log(text):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, LOG_NAME), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    return text


if "ghenv" in globals():
    import scriptcontext as _sc
    _k = "bergama_" + OUT_FOLDER
    try:
        _k += ":" + str(ghenv.Component.InstanceGuid)   # noqa: F821
    except Exception:
        pass
    _pressed = any(v is True for k, v in list(globals().items())
                   if not k.startswith("_") and isinstance(v, bool) and k not in ("True", "False", "done")) or \
        any(chain_fire(v, _k + "_chain") for k, v in list(globals().items()) if not k.startswith("_") and k != "done" and isinstance(v, str))
    if _pressed:
        _t0 = time.time()
        try:
            _res = main()
        except Exception as _ex:
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-900:])
        _sc.sticky[_k + "_log"] = write_log(_res)
        _sc.sticky[_k + "_status"] = ("ERROR" if _res.startswith("ERROR") else
                                      time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky[_k + "_done"] = done_text(True, not _res.startswith("ERROR"), time.time() - _t0)
        _sc.sticky[_k + "_ver"] = VERSION
    if _sc.sticky.get(_k + "_ver") != VERSION:
        for _s in ("_log", "_status", "_done"):
            _sc.sticky.pop(_k + _s, None)
    done = _sc.sticky.get(_k + "_done", "idle")
    log = _sc.sticky.get(_k + "_log", "Press the Button to export to " + OUT_DIR)
    print(log)
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(_k + "_status", "idle")  # noqa: F821
    except Exception:
        pass
