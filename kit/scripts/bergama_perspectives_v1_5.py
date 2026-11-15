# -*- coding: utf-8 -*-
"""Bergama Group 6: PERSPECTIVES v1 (15 Nov 2026): interim eye-level perspectives for every V box of the slides.

What Aras asked (15 Nov 2026, 15:16-15:20 UTC): "take these perspectives either from archicad or rhino (i dunno which
would look better)"; "we gonna make those perspectives into UE5 renders however it'll take time so feel free to
experiment there"; "please do that for all the placeholders in all the presentation".

Why Rhino: the slide 1 3D model (Page01Axo v4 axo_model.json, from MapBase) already holds the whole site (every
building, his asset trees, the flat river, streets, parks); the Archicad model holds only the strips behind the 12
section cuts and the canopies (no ground, river or trees).

What it does (run in Rhino 8, in Bergama_Altlik.3dm; the 3dm is never saved):
  1. reads every cached/bergama_perspectives/views_<page>.json a page script wrote: per view the eye and look points
     (survey m), the box size on the page (mm) and, where the page knows it, the proposed building rings;
  2. builds the slide 1 3D model in the open Rhino with Page01Axo's own axo3d_build (layer axo3d_page01), draped on the
     survey TIN of the open model (Sections library read_survey / Tin), the GLO-30 model where the survey has no point;
     the town as white volumes (liked set F03 / D12: context white, colour only where the project acts);
  3. adds the proposals of his master.svg (MasterplanBase cache) near the eyes:
       terraces    his teras / begum_su_merdiven / iskele_kenari rings as seat steps of RISE_M stepping down toward the
                   water (the Sections mp_surface rule), lifted TER_LIFT_M so the 5 m terrain mesh never covers them
       canopies    AcBuild's own build_canopies (folded facet skin, louvres, Y columns, plinth, deck, glazed rooms,
                   planters), its Archicad payloads turned into Rhino meshes here
       buildings   v1.1: each node's building as nodes common BUILD designs it (the node slides' drawings: length
                   from the rooms / depth, floors x storey, stone plinth, glazed every other bay, folded roof; N4 the
                   raised canopy platform), centred on his largest 'desings' piece in the node frame (slide 4 E: its
                   N6 outline) along its axis; a node without one is logged, not placed
  4. per view: a perspective camera EYE_M above the ground at the eye, looking level at the look point, LENS_MM lens,
     the axo3d layer alone in the flat display mode "Bergama Axo", captured PX_W px wide at the box's proportions with
     a transparent background (the page white is the sky) -> cached/bergama_perspectives/<page>_<view>.png;
  5. removes everything it added (layer axo3d_page01).
Interim: Unreal 5 renders replace these later (Aras 15:19 UTC).

Reads  cached/bergama_perspectives/views_*.json, cached/bergama_page01_axo/axo_model.json,
       cached/bergama_masterplanbase/masterplan.json, cached/bergama_sections/sections.json + cuts.json,
       scripts/bergama_page01_axo_v*.py, scripts/bergama_acbuild_v*.py, scripts/bergama_sections_v*.py (libraries),
       Data/bergama_dem_glo30.json, the open Rhino model's survey layers
Writes cached/bergama_perspectives/<page>_<view>.png, buildings.json (v1.2, for AcBuild), logs/bergama_perspectives_log.txt
Works when: the log lists one "capture" line per view and ends with 0 FLAG lines; then press the page scripts again.
"""
import os, re, json, math, time, glob

VERSION = "v1.5"   # v1.5 (own review of the v1.4 run: 5 of 8 eyes stood against a wall or inside a crown; terraces grey on grey; N2-N4 without a building): the eye moves along its view line to the first spot with CLEAR_M clear ahead (no house, no crown), else it is raised to EYE_HIGH_M; terraces in warm stone; a node with no desings piece gets its BUILD building across the stream from its V1, past the bed (placement ASSUMED, logged); v1.4 (own review of the v1.3 run, slide04 V1 / V2: wireframes, white on white, 4 terrace pieces): rendered by the view in its own display mode "Bergama Persp" (Shaded, lit, cast shadows, no wires; ViewCapture had ignored the mode and drew wires, as Axo v4.3 found), opaque white sky; the ground a warm grey so white houses read; terraces = his terrace hatch pieces (new master.svg: 612 small pieces) grouped within TER_GAP_M into zones, each zone stepped; lens set so a building fills about 70 % of the frame (24-50 mm); a FLAG when a capture is nearly empty or dark; v1.3: the Axo library cut at the AXO_LIB_END comment line (v1.2 cut at the word in Axo v5's docstring: no axo3d_build);   # v1.2 (Aras 17:24 UTC "every building drawing from Archicad"): each node building's placement and size written to cached/bergama_perspectives/buildings.json for AcBuild v1.14, so Archicad builds them where this script does; v1.1 (coordinator 15:26 UTC, Aras "zero gaps"): every node building raised as nodes common v13 BUILD designs it (same sizes as the node slides), not only N6; v1 (Aras 15 Nov 15:16-15:20 UTC): interim perspectives from the slide 1 3D model in Rhino
GH_LABEL = "Perspectives"
OUT_FOLDER = "bergama_perspectives"
LOG_NAME = "bergama_perspectives_log.txt"
GH_INPUTS = {}
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "cached", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
AXO_GLOB = os.path.join(BERGAMA_ROOT, "scripts", "bergama_page01_axo_v*.py")
ACB_GLOB = os.path.join(BERGAMA_ROOT, "scripts", "bergama_acbuild_v*.py")
AXO_MODEL = os.path.join(BERGAMA_ROOT, "cached", "bergama_page01_axo", "axo_model.json")
MP_JSON = os.path.join(BERGAMA_ROOT, "cached", "bergama_masterplanbase", "masterplan.json")
DEM_FILE = os.path.join(BERGAMA_ROOT, "Data", "bergama_dem_glo30.json")

EYE_M = 1.6                        # m: eye height above the ground (standing person, drawing rule)
LENS_MM = 24.0                     # 35 mm equivalent lens (wide architectural view, drawing choice)
LENS_MAX = 50.0                    # v1.4: longest lens when a view frames a building
PERSP_MODE = "Bergama Persp"       # v1.4: Shaded copy, lit, shadows, no wires / edges, white fill
CLEAR_M = 25.0                     # v1.5: m of clear view ahead of the eye (no house, no tree crown)
EYE_HIGH_M = 10.0                  # v1.5: eye height when no clear spot is found (a first-floor terrace view)
TER_GAP_M = 1.5                    # v1.4: terrace hatch pieces closer than this form one terrace zone
PX_W = 3000                        # capture width in pixels (about 250 ppi on a 130 mm box)
NEAR_M = 600.0                     # m: proposals built only this close to an eye
RISE_M, TREAD_MIN_M = 0.45, 0.6    # seat steps (Sections RISE_M, mp_surface 0.6 m least tread)
TER_LIFT_M = 1.0                   # m: terraces lifted over the draped terrain (its water sits 0.7 m up: AXO3D_DZ)
TER_KEYS = {"teras", "begum_su_merdiven", "iskele_kenari"}
NC_FILE = os.path.join("Data", "bergama_nodes_common.py")   # v1.1: BUILD (the node buildings' design) read live
MAX_PIECE_M2 = 20000.0             # masterplan pieces larger than this are picture frames, left out

# colours: town white volumes (A05 house tones), our proposals in the Sections materials, accent outline
TOWN = ("FFFFFF", "F5F3EE", "D9D4C8", "9E9889")     # roof, lit wall, shaded wall, outline
GROUND = {"c_slab": "E4DFD4", "c_street": "F5F3EE", "c_street_edge": "9E9889", "c_water": "A2B6B5", "c_water_edge": "7F9A9B"}
TER_TOP, TER_RISE, TER_EDGE = "D8C7A8", "B09A78", "8E7A5C"   # v1.5: warm stone (grey read as the ground)
SKIN = ("F5F3EE", "E6E1D6")        # canopy facets, alternate tones (Sections P_SHELL)
TIMBER, STEEL, STONE, GLASS, GREEN = "A9794B", "4F5559", "B8B2A6", "B9CDD3", "8E9E6A"
ACC = "C07A2E"                     # the project accent: outlines of our buildings
LIGHT = (-0.55, -0.45, 0.70)       # sun from the south-west, for lit / shaded walls of our buildings


def lib_newest(pattern):
    fs = glob.glob(pattern)
    if not fs:
        raise RuntimeError(u"%s missing: refresh the kit (Bergama.bat)" % pattern)
    return max(fs, key=lambda p: [int(x) for x in re.findall(r"\d+", os.path.basename(p))])


def load_axo(log):
    """Page01Axo's code above AXO_LIB_END (axo3d_build, axo3d_mode, axo3d_clear)"""
    p = lib_newest(AXO_GLOB)
    with open(p, encoding="utf-8") as f:
        code = f.read()
    mk = re.search(r"^#[^\n]*AXO_LIB_END", code, re.M)  # v1.3: the marker comment line, not the docstring's words
    i = mk.start() if mk else -1
    if i < 0:
        raise RuntimeError(u"%s has no AXO_LIB_END: use Page01Axo v4 or newer" % p)
    ns = {"__name__": "bergama_page01_axo_lib"}
    exec(compile(code[:code.rfind("\n", 0, i)], p, "exec"), ns)
    if "axo3d_build" not in ns:
        raise RuntimeError(u"%s has no axo3d_build: use Page01Axo v4 or newer" % p)
    log.append(u"library: %s (%s)" % (p, ns.get("VERSION")))
    return ns


def load_acb(log):
    """AcBuild as a library (its main is not run): build_canopies, load_lib (the Sections library), frame, so"""
    p = lib_newest(ACB_GLOB)
    ns = {"__name__": "bergama_acbuild_lib"}
    with open(p, encoding="utf-8") as f:
        exec(compile(f.read(), p, "exec"), ns)
    log.append(u"library: %s (%s)" % (p, ns.get("VERSION")))
    return ns


def glo_dem(log):
    with open(DEM_FILE, encoding="utf-8") as f:
        J = json.load(f)
    nr, nc, P = int(J["rows"]), int(J["cols"]), J["pts"]
    Z = [[q[2] for q in P[r * nc:(r + 1) * nc]] for r in range(nr)]
    gx0, gy0 = P[0][0], P[0][1]
    gdx, gdy = (P[nc - 1][0] - gx0) / float(nc - 1), (P[(nr - 1) * nc][1] - gy0) / float(nr - 1)

    def z(x, y):
        fi = min(nc - 1.000001, max(0.0, (x - gx0) / gdx))
        fj = min(nr - 1.000001, max(0.0, (y - gy0) / gdy))
        i, j = int(fi), int(fj)
        a, b = fi - i, fj - j
        return (Z[j][i] * (1 - a) + Z[j][i + 1] * a) * (1 - b) + (Z[j + 1][i] * (1 - a) + Z[j + 1][i + 1] * a) * b
    log.append(u"GLO-30 terrain: %d x %d points (%s)" % (nc, nr, DEM_FILE))
    return z


BLEN = {}                          # v1.4: node -> building length (lens choice)


def persp_mode(log):
    """v1.4: the perspective display mode: a copy of Shaded with its lighting, cast shadows, no isocurves / edges /
    mesh wires, a white solid fill"""
    import Rhino, System
    D = Rhino.Display.DisplayModeDescription
    m = D.FindByName(PERSP_MODE)
    if m is None:
        m = D.GetDisplayMode(D.CopyDisplayMode(D.FindByName("Shaded").Id, PERSP_MODE))
    a = m.DisplayAttributes
    miss = []
    for obj, nm, val in ((a, "ShowIsoCurves", False), (a, "ShowSurfaceEdges", False), (a, "ShowTangentEdges", False),
                         (a, "ShowTangentSeams", False), (a, "ShowGrid", False), (a, "ShowGridAxes", False),
                         (a, "ShowWorldAxes", False), (a, "ShadingEnabled", True), (a, "CastShadows", True)):
        try:
            setattr(obj, nm, val)
        except Exception:
            miss.append(nm)
    try:
        ma = a.MeshSpecificAttributes
        for nm in ("ShowMeshWires", "ShowMeshEdges", "ShowMeshNakedEdges", "ShowMeshNonmanifoldEdges"):
            setattr(ma, nm, False)
    except Exception:
        miss.append("mesh wires")
    try:
        a.FillMode = Rhino.Display.DisplayPipelineAttributes.FrameBufferFillMode.SolidColor
        a.SetFill(System.Drawing.Color.White)
    except Exception:
        miss.append("white fill")
    D.UpdateDisplayMode(m)
    log.append(u"display mode '%s'%s" % (PERSP_MODE, (u"; FLAG not set: " + u", ".join(miss)) if miss else u""))
    return m


def area(P):
    return 0.5 * sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(P, P[1:] + P[:1]))


def main():
    t0 = time.time()
    log = []
    import Rhino, System
    import Rhino.Geometry as rg
    doc = Rhino.RhinoDoc.ActiveDoc
    if doc is None:
        raise RuntimeError(u"no open Rhino model: open Bergama_Altlik.3dm")

    # ---- the views every page wrote
    views = []
    for fp in sorted(glob.glob(os.path.join(OUT_DIR, "views_*.json"))):
        with open(fp, encoding="utf-8") as f:
            J = json.load(f)
        pg = J.get("page") or os.path.basename(fp)[6:-5]
        for vn, v in sorted((J.get("views") or {}).items()):
            if v.get("eye") and v.get("look") and v.get("box_mm"):
                views.append((pg, vn, v))
            else:
                log.append(u"FLAG %s %s: no eye, look or box size: left out" % (pg, vn))
        log.append(u"views: %s (%s, %s)" % (fp, J.get("version"), u", ".join(sorted(J.get("views") or {}))))
    if not views:
        raise RuntimeError(u"no views_*.json in %s: press Slide04 (v1.8 or newer) first" % OUT_DIR)
    eyes = [tuple(v["eye"]) for _, _, v in views]
    near = lambda p: any(math.hypot(p[0] - e[0], p[1] - e[1]) <= NEAR_M for e in eyes)

    # ---- libraries, model, terrain
    AX = load_axo(log)
    AC = load_acb(log)
    L_ = AC["load_lib"](log)
    if not os.path.isfile(AXO_MODEL):
        raise RuntimeError(u"%s missing: press Page01Axo (v4 or newer) once" % AXO_MODEL)
    with open(AXO_MODEL, encoding="utf-8") as f:
        AM = json.load(f)
    d3 = AM.get("d3")
    if not d3:
        raise RuntimeError(u"%s holds no 3D inputs (d3): press Page01Axo v4 or newer once" % AXO_MODEL)
    d3 = dict(d3)
    d3.update(GROUND)
    d3["blds"] = [(P_, h_, TOWN) for P_, h_, _c in d3["blds"]]
    log.append(u"model: %s (%s): %d buildings, %d trees; town as white volumes" % (
        AXO_MODEL, AM.get("version"), len(d3["blds"]), len(d3["trees"])))
    xs, ys = [q[0] for q in d3["slab"]], [q[1] for q in d3["slab"]]
    box = (min(xs) - 50.0, min(ys) - 50.0, max(xs) + 50.0, max(ys) + 50.0)
    survey = L_["read_survey"](box, log)
    G = AC["GRID_M"]
    spots = {}
    for name in L_["SURVEY_LAYERS"]:
        for pl in survey.get(name, []):
            for p in pl:
                if p[2] > 1.0:
                    spots[(int(p[0] // G), int(p[1] // G))] = p
    ox, oy = round(sum(xs) / len(xs), -2), round(sum(ys) / len(ys), -2)
    tin = L_["Tin"]([(p[0] - ox, p[1] - oy, p[2]) for p in spots.values()])
    glo = glo_dem(log)
    n_t = [0, 0]

    def dem(x, y):
        z = tin.z(x - ox, y - oy)
        n_t[0 if z is not None else 1] += 1
        return z if z is not None else glo(x, y)
    log.append(u"terrain: survey TIN of %d spot heights (one per %.0f m cell), GLO-30 where the survey has none" % (
        len(spots), G))

    guids = []
    try:
        guids, bb = AX["axo3d_build"](doc, d3, dem, log)
        li = doc.Layers.FindByFullPath(AX["AXO3D_LAYER"], -1)
        tol = doc.ModelAbsoluteTolerance or 0.001

        def attr(h):
            a = Rhino.DocObjects.ObjectAttributes()
            a.LayerIndex = li
            a.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
            a.ObjectColor = System.Drawing.Color.FromArgb(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
            return a

        meshes = {}

        def mesh(h):
            return meshes.setdefault(h, rg.Mesh())

        def quad(M, pts):
            k = M.Vertices.Count
            for p in pts:
                M.Vertices.Add(*p)
            if len(pts) == 4:
                M.Faces.AddFace(k, k + 1, k + 2, k + 3)
            else:
                M.Faces.AddFace(k, k + 1, k + 2)

        def cap(M, ring, z):
            m = rg.Mesh.CreateFromClosedPolyline(rg.Polyline([rg.Point3d(q[0], q[1], z) for q in ring] +
                                                             [rg.Point3d(ring[0][0], ring[0][1], z)]))
            if m:
                M.Append(m)

        def prism(ring, z0, z1, top, side):
            for a, b in zip(ring, ring[1:] + ring[:1]):
                quad(mesh(side), [(a[0], a[1], z0), (b[0], b[1], z0), (b[0], b[1], z1), (a[0], a[1], z1)])
            cap(mesh(top), ring, z1)

        def line(pts, h):
            g = doc.Objects.AddPolyline(rg.Polyline([rg.Point3d(*p) for p in pts]), attr(h))
            if g != System.Guid.Empty:
                guids.append(g)

        # ---- masterplan pieces
        with open(MP_JSON, encoding="utf-8") as f:
            MPJ = json.load(f)
        water = [q for R in d3["water"] for q in R[::2]]

        # terraces: seat steps down toward the nearest water
        n_ter = n_step = 0
        # v1.4: his terrace layer is hatch pieces (new master.svg: 612, median 0.07 m2): pieces within TER_GAP_M are
        # grouped, each group's convex hull = one terrace zone; outlines of 2 m2 and more are zones of their own
        frag, zones = [], []
        for key, pieces in MPJ.get("layers", {}).items():
            if not set(key.split("/")) & TER_KEYS:
                continue
            for p in pieces:
                R = [tuple(q[:2]) for q in p[4]]
                if p[0] not in ("r", "s") or len(R) < 3 or abs(area(R)) > MAX_PIECE_M2:
                    continue
                c = (sum(q[0] for q in R) / len(R), sum(q[1] for q in R) / len(R))
                if not near(c):
                    continue
                if abs(area(R)) >= 2.0:
                    zones.append(R)
                else:
                    frag.append((R, min(q[0] for q in R), max(q[0] for q in R), min(q[1] for q in R),
                                 max(q[1] for q in R)))
        groups = []
        for it in frag:
            hit = [g for g in groups if g[1] - TER_GAP_M <= it[2] and it[1] <= g[2] + TER_GAP_M and
                   g[3] - TER_GAP_M <= it[4] and it[3] <= g[4] + TER_GAP_M]
            pts = list(it[0]) + [q for g in hit for q in g[0]]
            groups = [g for g in groups if g not in hit] + [(pts, min([it[1]] + [g[1] for g in hit]),
                                                            max([it[2]] + [g[2] for g in hit]),
                                                            min([it[3]] + [g[3] for g in hit]),
                                                            max([it[4]] + [g[4] for g in hit]))]

        def hull(P):
            P = sorted(set((round(q[0], 2), round(q[1], 2)) for q in P))
            if len(P) < 3:
                return []
            cr = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
            lo, hi = [], []
            for q in P:
                while len(lo) >= 2 and cr(lo[-2], lo[-1], q) <= 0:
                    lo.pop()
                lo.append(q)
            for q in reversed(P):
                while len(hi) >= 2 and cr(hi[-2], hi[-1], q) <= 0:
                    hi.pop()
                hi.append(q)
            return lo[:-1] + hi[:-1]
        for g in groups:
            H = hull(g[0])
            if len(H) >= 3 and abs(area(H)) >= 2.0:
                zones.append(H)
        log.append(u"terraces: %d hatch pieces near the eyes -> %d groups (gap %.1f m); %d zones in all" % (
            len(frag), len(groups), TER_GAP_M, len(zones)))
        for R in zones:
            if True:
                c = (sum(q[0] for q in R) / len(R), sum(q[1] for q in R) / len(R))
                if not near(c) or not water:
                    continue
                w = min(water, key=lambda q: (q[0] - c[0]) ** 2 + (q[1] - c[1]) ** 2)
                d_ = math.hypot(c[0] - w[0], c[1] - w[1]) or 1.0
                n_ = ((c[0] - w[0]) / d_, (c[1] - w[1]) / d_)       # away from the water
                T = lambda q: q[0] * n_[0] + q[1] * n_[1]
                ta, tb = min(T(q) for q in R), max(T(q) for q in R)
                z_hi = dem(*max(R, key=T))
                z_lo = dem(*min(R, key=T))
                n = 1
                if z_hi - z_lo >= RISE_M:
                    n = max(1, min(int((z_hi - z_lo) / RISE_M), int((tb - ta) / TREAD_MIN_M)))
                r_, t_ = ((z_hi - z_lo) / n if n > 1 else 0.0), (tb - ta) / n
                for i in range(n):
                    band = AC["_clip"](R, n_, tb - (i + 1) * t_ - 1e-6, tb - i * t_ + 1e-6)
                    if len(band) < 3:
                        continue
                    z = z_hi - i * r_ + TER_LIFT_M
                    prism(band, min(z_lo, z) - 1.0, z, TER_TOP, TER_RISE)
                    line([(q[0], q[1], z + 0.02) for q in band] + [(band[0][0], band[0][1], z + 0.02)], TER_EDGE)
                    n_step += 1
                n_ter += 1
        log.append(u"terraces: %d zones within %.0f m of an eye, %d steps (rise %.2f m, lifted %.1f m)" % (
            n_ter, NEAR_M, n_step, RISE_M, TER_LIFT_M))

        # canopies: AcBuild's own geometry, its Archicad payloads recorded and built here
        class Rec(object):
            def __init__(self):
                self.got = []

            def create(self, name, key, items, what):
                self.got.append((name, what, items))
                return [u"rec"] * len(items)
        rec = Rec()
        try:
            with open(os.path.join(BERGAMA_ROOT, "cached", "bergama_sections", "sections.json"), encoding="utf-8") as f:
                cuts = [(c_["name"], tuple(c_["A"]), tuple(c_["B"])) for c_ in json.load(f)["cuts"]]
            with open(os.path.join(BERGAMA_ROOT, "cached", "bergama_sections", "cuts.json"), encoding="utf-8") as f:
                CJ = json.load(f).get("cuts", {})
        except Exception as ex:
            cuts, CJ = [], {}
            log.append(u"FLAG canopies: Sections caches not read (%s): no flood levels, decks everywhere" % ex)
        rects = [(nm,) + (A,) + (B,) + AC["frame"](A, B) for nm, A, B in cuts]

        def near_cut(x, y):
            best = None
            for nm, A, B, Ln, u, nn in rects:
                s_, o_ = AC["so"]((x, y), A, u, nn)
                dd = abs(o_) + max(0.0, -s_, s_ - Ln)
                if nm in CJ and CJ[nm].get("levels") and (best is None or dd < best[0]):
                    best = (dd, nm)
            return CJ[best[1]]["levels"] if best else {}

        def q500_at(x, y):
            lv = near_cut(x, y).get("q500")
            return lv[0] if lv else None

        def wet_at(x, y, g):
            lv = [v[0] for v in near_cut(x, y).values() if isinstance(v, list) and v and v[0] is not None]
            return bool(lv) and g < min(lv) + 0.3
        xy = lambda p: {"x": round(p[0] - ox, 3), "y": round(p[1] - oy, 3)}
        try:
            AC["build_canopies"](rec, [], log, [None], lambda q, r: near(q), tin, ox, oy, 0.0, xy, q500_at, wet_at)
        except Exception as ex:
            log.append(u"FLAG canopies not built (%s: %s)" % (type(ex).__name__, ex))
        W = lambda d: (d["x"] + ox, d["y"] + oy)
        n_f = 0
        for name, what, items in rec.got:
            for it in items:
                if name == "CreateMeshes":
                    P3 = [(c_["x"] + ox, c_["y"] + oy, c_["z"]) for c_ in it["polygonCoordinates"]]
                    if "louvre" in what:
                        quad(mesh(TIMBER), P3)
                    else:
                        quad(mesh(SKIN[n_f % 2]), P3)
                        line(P3 + [P3[0]], TER_EDGE)
                        n_f += 1
                elif name == "CreateSlabs":
                    R = [W(c_) for c_ in it["polygonCoordinates"]]
                    col = STONE if "plinth" in what else (GREEN if "planter" in what else TIMBER)
                    prism(R, it["level"] - it["thickness"], it["level"], col, col)
                elif name == "CreateColumns":
                    b = it["coordinates"]
                    cyl = rg.Cylinder(rg.Circle(rg.Plane(rg.Point3d(b["x"] + ox, b["y"] + oy, b["z"]), rg.Vector3d.ZAxis),
                                                it["width"] / 2.0), it["height"])
                    mesh(STEEL).Append(rg.Mesh.CreateFromCylinder(cyl, 1, 10))
                elif name == "CreateBeams":
                    a, b = W(it["begCoordinate"]), W(it["endCoordinate"])
                    run = math.hypot(b[0] - a[0], b[1] - a[1])
                    za = it["zCoordinate"]
                    zb = za + run * math.tan(it["slantAngle"])
                    ln_ = rg.Line(rg.Point3d(a[0], a[1], za), rg.Point3d(b[0], b[1], zb))
                    cyl = rg.Cylinder(rg.Circle(rg.Plane(ln_.From, ln_.Direction), it["width"] / 2.0), ln_.Length)
                    mesh(STEEL).Append(rg.Mesh.CreateFromCylinder(cyl, 1, 8))
                elif name == "CreateWalls":
                    a, b = W(it["begCoordinate"]), W(it["endCoordinate"])
                    z0_, z1_ = it["zCoordinate"], it["zCoordinate"] + it["height"]
                    quad(mesh(GLASS), [(a[0], a[1], z0_), (b[0], b[1], z0_), (b[0], b[1], z1_), (a[0], a[1], z1_)])
                    line([(a[0], a[1], z0_), (b[0], b[1], z0_), (b[0], b[1], z1_), (a[0], a[1], z1_), (a[0], a[1], z0_)],
                         STEEL)
        log.append(u"canopies: %s" % (u"; ".join(u"%s %d" % (w_, len(i_)) for _, w_, i_ in rec.got) or u"none near an eye"))

        # v1.1: the node buildings as nodes common BUILD designs them (the node slides' plan / section / elevation):
        # L x depth, floors x storey on a stone plinth, glazed every other bay, folded roof; placed on his 'desings'
        # piece in the node frame (the largest), long side on its main axis (placement ASSUMED where not N6)
        NCn = {"__name__": "bergama_nodes_common"}
        with open(os.path.join(BERGAMA_ROOT, NC_FILE), encoding="utf-8") as f:
            exec(compile(f.read(), NC_FILE, "exec"), NCn)
        BUILD = NCn.get("BUILD") or {}
        PL, RISE, BAY = NCn.get("BP_PLINTH_M", 0.6), NCn.get("BP_RISE_M", 1.8), NCn.get("BP_BAY_M", 6.0)
        log.append(u"buildings: nodes common %s BUILD (%s)" % (NCn.get("NC_VERSION"), u", ".join(sorted(BUILD))))

        def inpoly(p, R):
            c_ = False
            for i in range(len(R)):
                a, b = R[i - 1], R[i]
                if (a[1] > p[1]) != (b[1] > p[1]) and p[0] < (b[0] - a[0]) * (p[1] - a[1]) / (b[1] - a[1]) + a[0]:
                    c_ = not c_
            return c_
        done_b = set()
        BREC = {}                                         # v1.2: for AcBuild (buildings.json)
        BLEN.clear()
        for pg, vn, v in views:
            nd = v.get("node") or ("N6" if v.get("building") else None)
            if not nd or nd in done_b:
                continue
            done_b.add(nd)
            bd = BUILD.get(nd)
            if not bd:
                log.append(u"FLAG %s: no BUILD design in nodes common: no building" % nd)
                continue
            rings = [[tuple(q[:2]) for q in R] for R in (v.get("building") or []) if len(R) >= 3]
            if not rings and v.get("frame"):
                fr = [tuple(q[:2]) for q in v["frame"]]
                for key, pieces in MPJ.get("layers", {}).items():
                    if key.split("/")[0] != "desings":
                        continue
                    for p in pieces:
                        R = [tuple(q[:2]) for q in p[4]]
                        if len(R) >= 3 and 4.0 <= abs(area(R)) <= MAX_PIECE_M2 and inpoly(
                                (sum(q[0] for q in R) / len(R), sum(q[1] for q in R) / len(R)), fr):
                            rings.append(R)
            if rings:
                R = max(rings, key=lambda R_: abs(area(R_)))
                cx, cy = sum(q[0] for q in R) / len(R), sum(q[1] for q in R) / len(R)
                sxx = sum((q[0] - cx) ** 2 for q in R); syy = sum((q[1] - cy) ** 2 for q in R)
                sxy = sum((q[0] - cx) * (q[1] - cy) for q in R)
                an = 0.5 * math.atan2(2 * sxy, sxx - syy)
                place = u"centred on his 'desings' piece (%.0f m2), long side on its axis%s" % (
                    abs(area(R)), u"" if nd == "N6" else u" (placement ASSUMED)")
            else:                                         # v1.5: across the stream from V1, past the bed
                E_, K_ = v["eye"], v["look"]
                dd = math.hypot(K_[0] - E_[0], K_[1] - E_[1]) or 1.0
                nx_, ny_ = (K_[0] - E_[0]) / dd, (K_[1] - E_[1]) / dd
                t_ = 0.0
                while t_ < 120.0 and any(inpoly((K_[0] + nx_ * t_, K_[1] + ny_ * t_), W_) for W_ in d3["water"]):
                    t_ += 1.0
                off = t_ + bd["depth"] / 2.0 + 3.0
                cx, cy = K_[0] + nx_ * off, K_[1] + ny_ * off
                an = math.atan2(ny_, nx_) + math.pi / 2.0
                place = (u"no 'desings' piece in the frame: placed ASSUMED across the stream from V1, %.0f m past "
                         u"the bed, long side along the bank" % off)
            u, w = (math.cos(an), math.sin(an)), (-math.sin(an), math.cos(an))
            D, hs, FL = bd["depth"], bd["storey"], bd["floors"]
            canopy = not FL
            Lb = bd.get("bays", 0) * BAY if canopy else max(sum(a for _n, a in f) for f in FL) / D
            nb = max(1, int(round(Lb / BAY)))
            nf = max(1, len(FL))
            P_ = lambda t, s: (cx + u[0] * t + w[0] * s, cy + u[1] * t + w[1] * s)
            foot = [P_(-Lb / 2, -D / 2), P_(Lb / 2, -D / 2), P_(Lb / 2, D / 2), P_(-Lb / 2, D / 2)]
            z0 = dem(cx, cy)
            zs = min(dem(*q) for q in foot) - 0.5
            zp = z0 + PL
            prism(foot, zs, zp, STONE, STONE)
            top = zp + nf * hs
            if canopy:                                     # N4: raised platform, deck at the storey height on columns
                prism(foot, top - 0.3, top, TIMBER, TIMBER)
                for k in range(nb + 1):
                    for s in (-D / 2 + 0.4, D / 2 - 0.4):
                        b = P_(-Lb / 2 + k * Lb / nb, s)
                        cyl = rg.Cylinder(rg.Circle(rg.Plane(rg.Point3d(b[0], b[1], zp), rg.Vector3d.ZAxis), 0.15),
                                          top - 0.3 - zp)
                        mesh(STEEL).Append(rg.Mesh.CreateFromCylinder(cyl, 1, 10))
                rail = [P_(-Lb / 2, -D / 2), P_(Lb / 2, -D / 2), P_(Lb / 2, D / 2), P_(-Lb / 2, D / 2), P_(-Lb / 2, -D / 2)]
                line([(q[0], q[1], top + 1.1) for q in rail], STEEL)
                line([(q[0], q[1], top) for q in rail], ACC)
            else:
                for k in range(nb):                       # long walls bay by bay: glass every other bay
                    t0_, t1_ = -Lb / 2 + k * Lb / nb, -Lb / 2 + (k + 1) * Lb / nb
                    for s in (-D / 2, D / 2):
                        a, b = P_(t0_, s), P_(t1_, s)
                        nx, ny = (w[0] * (1 if s > 0 else -1), w[1] * (1 if s > 0 else -1))
                        lit = nx * LIGHT[0] + ny * LIGHT[1] < 0
                        col = GLASS if k % 2 else (TOWN[1] if lit else TOWN[2])
                        quad(mesh(col), [(a[0], a[1], zp), (b[0], b[1], zp), (b[0], b[1], top), (a[0], a[1], top)])
                        line([(a[0], a[1], zp), (a[0], a[1], top)], ACC)
                for t_ in (-Lb / 2, Lb / 2):              # end walls
                    a, b = P_(t_, -D / 2), P_(t_, D / 2)
                    lit = (u[0] * (1 if t_ > 0 else -1)) * LIGHT[0] + (u[1] * (1 if t_ > 0 else -1)) * LIGHT[1] < 0
                    quad(mesh(TOWN[1] if lit else TOWN[2]), [(a[0], a[1], zp), (b[0], b[1], zp), (b[0], b[1], top),
                                                             (a[0], a[1], top)])
                for j in range(1, nf):                    # floor lines
                    zz = zp + j * hs
                    line([(q[0], q[1], zz) for q in foot] + [(foot[0][0], foot[0][1], zz)], TER_EDGE)
            # folded roof: valleys at the bay ends, ridges at the bay middles (BP_RISE_M), eaves at the wall top
            rz = top + (0.0 if not canopy else 2.3)
            ax = [(-Lb / 2 + Lb * kk / (2.0 * nb), rz + (RISE if kk % 2 else 0.0)) for kk in range(2 * nb + 1)]
            n_r = 0
            for kk in range(2 * nb):
                (ta, za), (tb, zb) = ax[kk], ax[kk + 1]
                for s in (-D / 2, D / 2):
                    pa, pb, ma, mb = P_(ta, s), P_(tb, s), P_(ta, 0.0), P_(tb, 0.0)
                    quad(mesh(SKIN[n_r % 2]), [(pa[0], pa[1], rz), (pb[0], pb[1], rz), (mb[0], mb[1], zb)])
                    quad(mesh(SKIN[(n_r + 1) % 2]), [(pa[0], pa[1], rz), (mb[0], mb[1], zb), (ma[0], ma[1], za)])
                    line([(pa[0], pa[1], rz), (mb[0], mb[1], zb)], TER_EDGE)
                    n_r += 1
            line([(q[0], q[1], rz) for q in foot] + [(foot[0][0], foot[0][1], rz)], ACC)
            if canopy:
                for k in range(nb + 1):
                    for s in (-D / 2 + 0.4, D / 2 - 0.4):
                        b = P_(-Lb / 2 + k * Lb / nb, s)
                        cyl = rg.Cylinder(rg.Circle(rg.Plane(rg.Point3d(b[0], b[1], top), rg.Vector3d.ZAxis), 0.12),
                                          rz - top)
                        mesh(STEEL).Append(rg.Mesh.CreateFromCylinder(cyl, 1, 10))
            BLEN[nd] = Lb
            BREC[nd] = {"c": [cx, cy], "u": list(u), "w": list(w), "L": Lb, "D": D, "nb": nb, "nf": 0 if canopy else nf,
                        "storey": hs, "plinth": PL, "rise": RISE, "ground": z0, "canopy": canopy,
                        "foot": [list(q) for q in foot]}
            log.append(u"%s building (%s): %.0f x %.0f m, %d floor(s) x %.1f m on a %.1f m plinth, %d bays, roof +%.1f m; "
                       u"at %.1f, %.1f, %s" % (
                           nd, bd["name"], Lb, D, 0 if canopy else nf, hs, PL, nb, RISE, cx, cy, place))
        try:
            os.makedirs(OUT_DIR, exist_ok=True)
            with open(os.path.join(OUT_DIR, "buildings.json"), "w", encoding="utf-8") as f:
                json.dump({"version": VERSION, "units": u"survey m; u = long axis, w = cross axis",
                           "buildings": BREC}, f, ensure_ascii=False)
            log.append(u"buildings.json: %s written for AcBuild" % (u", ".join(sorted(BREC)) or u"none"))
        except Exception as ex:
            log.append(u"FLAG buildings.json not written (%s)" % ex)
        for h, M in meshes.items():
            if M.Vertices.Count == 0:
                continue
            M.Normals.ComputeNormals()
            M.Compact()
            M.VertexColors.Clear()
            c_ = System.Drawing.Color.FromArgb(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
            for _ in range(M.Vertices.Count):
                M.VertexColors.Add(c_)
            g = doc.Objects.AddMesh(M, attr(h))
            if g != System.Guid.Empty:
                guids.append(g)

        # ---- one perspective capture per view
        view = doc.Views.ActiveView
        vp = view.ActiveViewport
        info0 = Rhino.DocObjects.ViewportInfo(vp)
        dm0 = vp.DisplayMode
        vis = [(l.Index, l.IsVisible) for l in doc.Layers if not l.IsDeleted]
        cur0 = doc.Layers.CurrentLayerIndex
        try:
            doc.Layers.SetCurrentLayerIndex(li, True)
            for l in doc.Layers:
                if l.IsDeleted:
                    continue
                on = l.Index == li
                if l.IsVisible != on:
                    l.IsVisible = on
                    doc.Layers.Modify(l, l.Index, True)
            pmode = persp_mode(log)

            def clear_eye(e, k):
                """v1.5: the first spot along the view line (from the marked eye, every 4 m up to 60 % of the way)
                with CLEAR_M ahead free of houses and tree crowns; else the marked eye raised to EYE_HIGH_M"""
                dd = math.hypot(k[0] - e[0], k[1] - e[1]) or 1.0
                nx_, ny_ = (k[0] - e[0]) / dd, (k[1] - e[1]) / dd
                R0 = dd + CLEAR_M + 50.0
                bl = [P_ for P_, h_, c_ in d3["blds"] if any(math.hypot(q[0] - e[0], q[1] - e[1]) < R0 for q in P_)]
                tr = [(x, y, D_ / 2.0 + 1.0) for x, y, D_, cl in d3["trees"] if math.hypot(x - e[0], y - e[1]) < R0]

                def ok(p):
                    for j in range(0, int(CLEAR_M) + 1, 2):
                        q = (p[0] + nx_ * j, p[1] + ny_ * j)
                        if any(math.hypot(q[0] - x, q[1] - y) < r for x, y, r in tr):
                            return False
                        if any(inpoly(q, P_) for P_ in bl):
                            return False
                    return True
                s_ = 0.0
                while s_ <= 0.6 * dd:
                    p = (e[0] + nx_ * s_, e[1] + ny_ * s_)
                    if ok(p):
                        return p, EYE_M, (u"marked eye" if s_ == 0 else u"moved %.0f m forward to a clear spot" % s_)
                    s_ += 4.0
                return e, EYE_HIGH_M, u"no clear spot at eye level: raised to %.0f m" % EYE_HIGH_M
            vp.DisplayMode = pmode
            os.makedirs(OUT_DIR, exist_ok=True)
            for pg, vn, v in views:
                e, k = tuple(v["eye"]), tuple(v["look"])
                e, eh, why = clear_eye(e, k)                  # v1.5: not against a wall or inside a crown
                ze = dem(*e) + eh
                cam, tg = rg.Point3d(e[0], e[1], ze), rg.Point3d(k[0], k[1], ze)
                if cam.DistanceTo(tg) < 1.0:
                    log.append(u"FLAG %s %s: eye and look points coincide: left out" % (pg, vn))
                    continue
                lens = LENS_MM
                nd_ = v.get("node") or ("N6" if v.get("building") else None)
                if nd_ in BLEN:                               # v1.4: the building fills about 70 % of the frame
                    lens = max(LENS_MM, min(LENS_MAX, 36.0 * cam.DistanceTo(tg) / (BLEN[nd_] / 0.7)))
                try:
                    vp.ChangeToPerspectiveProjection(True, lens)
                except Exception:
                    vp.ChangeToPerspectiveProjection(cam.DistanceTo(tg), True, lens)
                vp.SetCameraLocations(tg, cam)
                vp.CameraUp = rg.Vector3d.ZAxis
                vp.Camera35mmLensLength = lens
                view.Redraw()
                bw, bh = float(v["box_mm"][0]), float(v["box_mm"][1])
                W_, H_ = PX_W, int(round(PX_W * bh / bw))
                bmp = None
                AS = Rhino.ApplicationSettings.AppearanceSettings
                bg0 = AS.ViewportBackgroundColor
                try:                                      # v1.4: rendered in the mode itself (ViewCapture drew wires)
                    AS.ViewportBackgroundColor = System.Drawing.Color.White
                    view.Redraw()
                    bmp = view.CaptureToBitmap(System.Drawing.Size(W_, H_), pmode)
                except Exception as ex:
                    log.append(u"FLAG %s %s: view.CaptureToBitmap(size, mode) failed (%s: %s)" % (pg, vn, type(ex).__name__, ex))
                finally:
                    AS.ViewportBackgroundColor = bg0
                if bmp is None:
                    log.append(u"FLAG %s %s: Rhino returned no image" % (pg, vn))
                    continue
                n_all = n_ink = n_dark = 0                # v1.4: a quick look: empty (white) or wire-dark captures
                for yy in range(0, bmp.Height, 25):
                    for xx in range(0, bmp.Width, 25):
                        c_ = bmp.GetPixel(xx, yy)
                        n_all += 1
                        n_ink += 1 if c_.R + c_.G + c_.B < 735 else 0
                        n_dark += 1 if c_.R + c_.G + c_.B < 120 else 0
                png = os.path.join(OUT_DIR, u"%s_%s.png" % (pg, vn))
                bmp.Save(png, System.Drawing.Imaging.ImageFormat.Png)
                bmp.Dispose()
                log.append(u"capture %s %s (%s): eye %.1f, %.1f at %.1f m (ground + %.1f), looking %.0f m to %.1f, %.1f, "
                           u"%.0f mm lens, %d x %d px, %.0f %% ink, %.0f %% near-black -> %s" % (
                               pg, vn, why, e[0], e[1], ze, eh, cam.DistanceTo(tg), k[0], k[1], lens, W_, H_,
                               100.0 * n_ink / n_all, 100.0 * n_dark / n_all, png))
                if n_ink < 0.15 * n_all or n_dark > 0.12 * n_all:
                    log.append(u"FLAG %s %s: the capture looks empty or wire-dark: check the display mode" % (pg, vn))
        finally:
            for i_, was in vis:
                l = doc.Layers[i_]
                if l.IsVisible != was:
                    l.IsVisible = was
                    try:
                        doc.Layers.Modify(l, i_, True)
                    except Exception:
                        pass
            try:
                doc.Layers.SetCurrentLayerIndex(cur0, True)
                vp.SetViewProjection(info0, True)
                vp.DisplayMode = dm0
            except Exception:
                pass
            view.Redraw()
    finally:
        if guids:
            AX["axo3d_clear"](doc, guids, log)
    log.append(u"terrain reads: %d from the survey TIN, %d from GLO-30" % tuple(n_t))
    flags = [l for l in log if u"FLAG" in l]
    return u"%s\n%s %s, %d FLAG line(s), %.1f s" % (u"\n".join(log), GH_LABEL, VERSION, len(flags), time.time() - t0)


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


def _run():
    try:
        return main()
    except Exception as _ex:
        import traceback as _tb
        return "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-900:])


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
        _res = _run()
        _sc.sticky[_k + "_log"] = write_log(_res)
        _sc.sticky[_k + "_status"] = ("ERROR" if _res.startswith("ERROR") else
                                      time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky[_k + "_done"] = done_text(True, not _res.startswith("ERROR"), time.time() - _t0)
        _sc.sticky[_k + "_ver"] = VERSION
    if _sc.sticky.get(_k + "_ver") != VERSION:
        for _s in ("_log", "_status", "_done"):
            _sc.sticky.pop(_k + _s, None)
    done = _sc.sticky.get(_k + "_done", "idle")
    log = _sc.sticky.get(_k + "_log", "Press the Button to capture the perspectives")
    print(log)
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(_k + "_status", "idle")  # noqa: F821
    except Exception:
        pass
elif __name__ == "__main__":
    print(write_log(_run()))
