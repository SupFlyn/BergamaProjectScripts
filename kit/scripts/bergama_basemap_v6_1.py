# -*- coding: utf-8 -*-
"""Bergama Group 6: BASEMAP v5 (12 Nov 2026). Rules: scripts/_template/SCRIPT_STANDARD.md.
The existing situation inside site_alan, from ONE read of the open survey model (Bergama_Altlik.3dm), turned so the
frame's long side lies flat (eastern end right, as his plan), kept by layer in a cache the other new scripts read.
This file is also the drawing library of the new set: the Masterplan script (bergama_plan_base) loads everything above
the line "main" from it, so the survey context, the style and the PDF writer are the same in every drawing.

Aras 12 Nov 2026 (his words, in order):
  10:53 "every road should be outlined as well as the buildings ... Heritage buildings should be marked. Our site_alan
        should be our frame for that basemap and keymap"
  11:13 "use sattalite imagery and dwg combined together"; "dont add shadows to the basemap for now"
  11:15 "if a road starts somewhere i dont want it to disappear along the road ... it should be consistent"
  17:07-17:26 "we want the base map first"; routes "leave that to last"; the thin red line stays, "outside of that line
        will be white and inside is colourful"; "lighter more soft colours generally"
  18:52 "also create the pdf's scaled into A0"
  19:0x "at one place the housing is hatched with gray another one is solid white fill like keep it consistent
        everywhere"; "combine vectoral and raster drawing however maximize the quality first than optimize for resource
        consumption while viewing in the file (also the size a little)"
  19:10 "textured fills like the examples like the colour palatte that i gave to you"; 19:12 "we want grainy however
        ... this image is too grainy"; of his favourite palette chart: "this is fine maybe a little bit more"
v4 = what follows from the 19:0x messages and the look review of the first Rhino runs:
  ONE STYLE  every colour, line weight and text size is read from Data/bergama_style.json (one entry per meaning:
             building, street, heritage, water ...). Basemap, Keymap and Masterplan use the same entry for the same
             thing. Buildings are the same everywhere: white with one thin outline, closed or not.
  HOUSING    the satellite land cover is never drawn on housing: it is cut away inside every closed building outline
             (+ FACE_HALO_M m) and within MASK_M m of every other building line (the old town's open block lines).
             Only tree cover and low green are drawn, as two pale tones without outlines, patches under COVER_MIN_M2
             m2 dropped. Open ground is white (the page).
  VECTOR + RASTER  lines, outlines and text are vector. Two things are raster: (1) the land cover is ONE 1-bit stencil
             of COVER_M m cells per tone (instead of 12,000 outlines and hatch lines), (2) the grain: every coloured
             fill is painted with a paper grain, ONE shared seamless tile per colour (GRAIN in the style file: +-amp
             of the tone, his "fine, maybe a little more" level; 0 = flat). White stays white.
  A0         <name>_A0.pdf = the frame cut in two bands (west above, east below, BAND_OVERLAP_M m shared) on an A0
             landscape page at the smallest round scale that fits (calculated in the run: 1:1,500), title and legend
             in the right column.
  LOG        every output is logged with its size in MB and the number of drawn objects.
  Basemap_colour.svg is no longer written: the Masterplan script draws his plan on this base map.
v4.1 (first Rhino run of v4, look review 12 Nov 19:23 UTC; all drawing values, ours): the far context lines are
lightened less (FADE_MIX 0.25: the building outlines were too faint); a style entry may carry its own grain strength
("grain": 0.09 on water); line swatches in the legend are drawn LEGEND_LINE_K times heavier, in the legend only; the
two A0 bands sit in the middle of the page height and the column under the legend holds a small key plan (streets,
stream, heritage, red line, the two bands, the section lines); when the model has no layer section_lines the key map
reads Data/section_lines.json; a PDF that is open in a viewer is still written under a timed name, and the log says so.
v4.2 (second look review, 12 Nov 19:28 UTC; drawing values, ours): a style entry may carry "ticks" (the water's
short wave strokes, vector, inside the same shared tile as its grain; Aras 18:40 "water ... should get textures");
legend lines are at least LEGEND_LINE_MIN mm; a section line is named once, above its upper end, names that would
touch are stacked; on a sheet smaller than A0 / 2 the north and scale block sits under the frame, not on the map.
v6.1 (first Rhino run of v6, 0 FLAG; look check): the street surface's stepped edge is smoothed once (corner
cutting); a road edge, bridge or stream line piece shorter than FRAG_M m is dropped on the layers the clean-up cut
(the cut left short leftovers inside parcels and the green; his "get rid of these kind of stray lines").
v6, Aras 12 Nov 19:51-20:05 UTC: "take the tree information from the site data"; "all trees are group together and a
subgroup would include a tree"; "you seem to be missing houses in a lot of the places"; "get rid of these kind of
stray lines". So: (1) the survey's tree symbols (TREE_LAYERS) are read into the cache as "trees" [x, y, radius or 0,
layer]; (2) the missing houses: v5 dropped loose building stubs again and again until none was left, which ate whole
open house outlines made of short lines. Now a short line is dropped only when it is a real tick: one end free and the
other on a corner where three or more lines meet (under TICK_M m), or free at both ends and under CRUMB_M m (once,
never repeated); (3) bridge
side lines that run beside the joined street surface are dropped like the road edges (the thick doubles along the
street edge); (4) write_svg: the same items as an SVG with a named group per layer and a subgroup per "layer/name"
(each tree), for editing; a layer name "a/b" is PDF layer "a". New helpers stroke_rings and join_rings (shapes and
wide lines joined into one outlined surface) for the plan's roads and paths.
v5, Aras 12 Nov 19:42-19:45 UTC: "dont divide drawings into two like ever ... produce a long single drawing always";
"I dont want wave texture on water i want textured hatches"; "base map looks ass however keymap looks pretty decent";
"implement the river drawing technique from older scripts"; "a lot of stray lines, lines that are overlapping ... and
lines that are like %75 each other and shifted ever so slightly"; "roads do miss eachother"; "show us how those 3 roads
do intersect"; "Try to make example a05 example as accurate as possible". So (this replaces the A0 bands, the key plan,
the wave strokes and the grey land cover stencil described above):
  ONE DRAWING  every sheet is the whole frame in one piece. <name>_A0.pdf = the frame once on A0 landscape at the
               smallest round scale that fits its width (calculated: 1:2,500).
  ROADS        all street bands are painted into one mask and its outline is traced back to vector: ONE street surface
               with ONE edge, so every junction is joined and no edge crosses a street (join_streets).
  RIVER        the site board's technique: the channel between the survey's stream lines along the Selinos centreline,
               one filled surface in the water tone with the grain, no outline, no wave strokes (build_river).
  CLEAN LINES  doubled building lines once; loose stubs dropped; survey road edges, kerbs and stream lines that run
               beside a joined surface dropped (clean_lines; every count in the log). Walls, sheds, kerbs and park
               lines are not drawn on the maps any more (the key map never had them); they stay in the cache.
  GREEN        A05's soft green: the 2023 tree cover as a pale green tone that fades out at its edge (a blurred raster
               tone, HAZE_BLUR_M m), housing still cut out. Low green is not drawn.
MASK_C, MASK_TOL, TICK_M, NEAR_M, the RIVER_* and HAZE_* values are drawing values (ours).
Kept from v1-v3.3: heritage rule (BINA_TARIHI / BINA_HARABE or a heritage word in a YAZI_YAPI name inside), building
lines joined into closed outlines (FACE_MIN..FACE_MAX m2), floor counts (YAZI_KAT_ADEDI) in the cache, the continuous
street bands along the OpenStreetMap centrelines (survey edge / building front / carried width; streets.json), the two
tones of the context lines (full within FADE_M m of calisma_alan, lighter beyond), names from the survey, the corner
block. Distances and tones marked "ours" are drawing values, not his.

Component: Rhino 8 > Grasshopper > Python 3 Script (the board builder places it from the cloud kit).
  input  run            Button (or the previous script's done text)
  input  scale          sheet scale 1:n of Basemap.pdf (default 2000)
  input  keymap_scale   sheet scale 1:n of Keymap.pdf (default 10000)
  output log / done     as every Bergama script
Reads  the open Rhino model's survey layers (once; the same model = the cache is used, nothing read again)
       ~/Downloads/Bergama/Data/bergama_style.json (the style table; without it the script stops with a clear line)
       ~/Downloads/Bergama/Data/veg2023.json      (satellite land cover; without it the map is drawn without, FLAG)
       ~/Downloads/Bergama/Data/bergama_osm.osm   (street centrelines; without it only the survey edges, FLAG)
Writes ~/Downloads/Bergama/output/bergama_basemap/Basemap.pdf, Keymap.pdf, Basemap_A0.pdf, Keymap_A0.pdf
       ~/Downloads/Bergama/cached/bergama_basemap/basemap_layers.json   every layer in survey m, the frame, the turn
       ~/Downloads/Bergama/cached/bergama_basemap/streets.json          the street bands and footpaths in survey m
       ~/Downloads/Bergama/logs/bergama_basemap_log.txt
"""
import os, time, json, math, re, zlib, random, struct, base64
import xml.etree.ElementTree as ET

# ---- SETTINGS ----
VERSION = "v6.1"
GH_LABEL = "Basemap"
OUT_FOLDER = "bergama_basemap"
LOG_NAME = "bergama_basemap_log.txt"
GH_INPUTS = {"scale": "int 500..10000 = 2000", "keymap_scale": "int 2000..50000 = 10000"}

FRAME_LAYER = "site_alan"
FRAME_COPY = [(29388.015, 32540.503), (31220.325, 30364.153), (31625.069, 30704.915), (29792.759, 32881.264)]
SECTION_LAYER = "section_lines"
WORK_LAYER = "calisma_alan"
BLD_LAYERS = ["BINA_MESKEN", "BINA", "BINA_RESMI", "BINA_OKUL", "BINA_DINI_TESIS", "BINA_DINITESIS", "BINA_TARIHI",
              "BINA_HARABE", "BINA_FABRIKA", "BINA_SERA", "BINA_SPOR_TESISLERI", "BINA_AKARYAKIT", "BINA_INS_HALINDE"]
HER_LAYERS = ("BINA_TARIHI", "BINA_HARABE")
NAME_LAYER = "YAZI_YAPI"
FLOOR_LAYER = "YAZI_KAT_ADEDI"
STREET_NAME_LAYER = "YAZI_CADDE_YOL"
HERITAGE_WORDS = ("tarihi", "harabe", "harap", "kalıntı", "kalinti", "hamam", " han ", "bedesten", "arasta", "türbe",
                  "turbe", "medrese", "kızıl avlu", "kizil avlu", "tapınağı", "tapinagi", "kilise", "sinagog", "çeşme",
                  "cesme", "sebil", "kervansaray", "müze", "muze", "cami", "mescit", "mescid", "cemevi", "tekke", "zaviye")
TREE_LAYERS = ("SEMBOL_TEK_AGAC", "SEMBOL_YPDKN_AGAC", "SEMBOL_YAP_DOKMEYEN")   # the survey's tree symbols
# cache layer -> (survey layers, closed shapes?)
SURVEY = [
    ("sheds", ["BINA_SUNDURMA"]),
    ("road_edges", ["YOL_SOSE", "YOL_TOPRAK"]),
    ("kerbs", ["YOL_BORDUR"]),
    ("bridges", ["YOL_KOPRU"]),
    ("stream_banks", ["HIDRO_DERE_SULU", "HIDRO_DERE_KURU"]),
    ("ponds", ["HIDRO_HAVUZ", "HIDRO_GOL"]),
    ("parks", ["ORMAN_PARK_BAHCE"]),
    ("walls", ["SINIR_DUVAR", "SINIR_HARAP_DUVAR"]),
    ("heritage_walls", ["SINIR_TARIHI_SUR"]),
]
VEG_FILE = os.path.join("Data", "veg2023.json")
VEG_KEYS = (("bare", "sat_bare"), ("grass", "sat_grass"), ("trees", "sat_trees"))
# the satellite image's own extent in survey m (library/satellite_2026-11-06/sat_2023-03-01_0p5m_survey.json:
# x0 29520.496, y1 32880.562, 4025 x 4934 px of 0.5 m)
VEG_BOX = (29520.496, 30413.562, 31532.996, 32880.562)
CREDIT = (u"Buildings, road edges, water: survey. Land cover: Esri World Imagery (Maxar), 1 Mar 2023, by colour rules. "
          u"Street bands: survey edges and fronts along OpenStreetMap centrelines.")
OSM_FILE = os.path.join("Data", "bergama_osm.osm")
# OSM longitude / latitude -> survey m: TM 27 (GRS80) then the fit to the survey (the site board's GEO values)
_A, _FL = 6378137.0, 1 / 298.257222101
_E2 = _FL * (2 - _FL)
_EP2 = _E2 / (1 - _E2)
GEO = dict(s=1.0001121171177874, th=-0.0015904735313230483, tx=-492593.7399912414, ty=-4299748.4497664515)
STREET_STEP, EDGE_MAX, FRONT_MAX, STREET_MIN = 4.0, 12.0, 8.0, 1.0     # m
PATH_CLASSES = ("footway", "path", "steps", "cycleway", "bridleway", "track")
SKIP_CLASSES = ("proposed", "construction", "platform", "elevator", "corridor", "bus_stop", "rest_area", "services")
STREET_FORMAT = 2
FACE_MIN, FACE_MAX = 4.0, 20000.0      # m2: a closed cell of building lines is a building between these
FADE_M, FADE_MIX = 100.0, 0.25     # m from calisma_alan where the context lines turn lighter; how far towards white
FADE_KEYS = ("parks", "paths", "streets", "street_net", "road_edges", "kerbs", "bridges", "walls", "sheds", "buildings")
STYLE_FILE = os.path.join("Data", "bergama_style.json")
A0_W, A0_H, A0_MARGIN, A0_STEP = 1189.0, 841.0, 15.0, 500     # mm, mm, mm, scale step
COVER_M, COVER_MIN_M2 = 0.5, 80.0  # m cell of the land cover stencil (the image's own 0.5 m); smallest patch drawn (ours)
LEGEND_LINE_MIN = 0.3               # mm: no legend line swatch thinner than this (legend only)
LEGEND_LINE_K = 3.0                # line swatches in the legend: this many times the drawn weight (legend only)
SECTION_FILE = os.path.join("Data", "section_lines.json")
MASK_C, MASK_TOL = 0.5, 0.35       # m: cell of the joining masks; how far a traced outline may leave the cell staircase
STREET_CLOSE_M, STREET_MIN_M2 = 1.0, 20.0     # m seams closed in the street surface; smallest island / hole kept
CENTRE_FILE = os.path.join("Data", "selinos_centreline.json")
RIVER_STEP, RIVER_REACH, RIVER_GAP = 3.0, 45.0, 4000.0   # m between cross lines; how far a bank is looked for; longest stretch carried without a stream line (the whole frame: the river never stops)
RIVER_CLOSE_M, RIVER_MIN_M2 = 1.0, 25.0
FRAG_M = 12.0                      # m: a road edge, bridge or stream line piece shorter than this is dropped (v6.1)
CRUMB_M = 2.0                      # m: a building line loose at both ends and shorter than this is dropped
TICK_M, NEAR_M = 4.0, 2.0          # m: loose building stubs shorter than this are dropped; "beside a joined surface"
HAZE_C, HAZE_BLUR_M, HAZE_MAX = 2.0, 6.0, 0.9    # m cell and blur of the soft green; its strongest opacity
MASK_M, FACE_HALO_M = 8.0, 1.0     # m kept free of land cover around open building lines / closed outlines (ours)
# ---- folders (same in every script) ----
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
CACHE_DIR = os.path.join(BERGAMA_ROOT, "cached", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
CACHE_FILE = os.path.join(CACHE_DIR, "basemap_layers.json")
CACHE_FORMAT = 3
STREET_FILE = os.path.join(CACHE_DIR, "streets.json")


# ================================================================ the open Rhino model
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


def _curve_pts(g):
    """(closed?, [(x, y)]) of a curve: its own corners when it is a polyline, else a point every metre"""
    try:
        ok, pl = g.TryGetPolyline()
        if ok:
            P = [(p.X, p.Y) for p in pl]
            cl = bool(g.IsClosed)
            if cl and len(P) > 1 and math.hypot(P[0][0] - P[-1][0], P[0][1] - P[-1][1]) < 1e-6:
                P = P[:-1]
            return cl, P
    except Exception:
        pass
    try:
        ts = g.DivideByLength(1.0, True) or []
        P = [(g.PointAt(t).X, g.PointAt(t).Y) for t in ts]
        cl = bool(g.IsClosed)
        if not cl and P:
            P.append((g.PointAtEnd.X, g.PointAtEnd.Y))
        return cl, P
    except Exception:
        return False, []


def model_key(doc):
    try:
        p = doc.Path or ""
        st = os.stat(p) if p and os.path.isfile(p) else None
        return u"%d|%s|%s|%s|%d" % (CACHE_FORMAT, VERSION, p, (u"%d|%d" % (st.st_size, st.st_mtime_ns)) if st else u"unsaved",
                                    doc.Objects.Count)
    except Exception:
        return None


def building_faces(segs):
    """segs [(layer, a, b)] -> ([(ring, share of sides on heritage layers)], [segs that bound no kept cell]).
    The lines are joined at shared end points (1 cm) and every bounded cell of the net is walked once."""
    def key(p):
        return (int(round(p[0] * 100.0)), int(round(p[1] * 100.0)))
    edge = {}                                             # (ka, kb) sorted -> layer
    pt = {}
    for nm, a, b in segs:
        ka, kb = key(a), key(b)
        if ka == kb:
            continue
        pt[ka], pt[kb] = a, b
        e = (ka, kb) if ka < kb else (kb, ka)
        if e not in edge or nm in HER_LAYERS:
            edge[e] = nm
    nb = {}
    for ka, kb in edge:
        nb.setdefault(ka, []).append(kb)
        nb.setdefault(kb, []).append(ka)
    order = {}
    for k_, L in nb.items():                              # the neighbours of each point, counter-clockwise
        L.sort(key=lambda q: math.atan2(q[1] - k_[1], q[0] - k_[0]))
        order[k_] = dict((q, i) for i, q in enumerate(L))
    seen, faces, used = set(), [], set()
    for ka, kb in list(edge):
        for u, v in ((ka, kb), (kb, ka)):
            if (u, v) in seen:
                continue
            ring, a2 = [], 0
            while (u, v) not in seen:
                seen.add((u, v))
                ring.append(u)
                a2 += u[0] * v[1] - v[0] * u[1]
                L = nb[v]
                w = L[(order[v][u] - 1) % len(L)]         # the next line clockwise around v: keeps the cell on the left
                u, v = v, w
            area = a2 / 2.0 / 10000.0                     # the keys are in cm
            if FACE_MIN <= area <= FACE_MAX and len(ring) >= 3:
                es = [(ring[i], ring[(i + 1) % len(ring)]) for i in range(len(ring))]
                es = [(p_, q_) if p_ < q_ else (q_, p_) for p_, q_ in es]
                used.update(es)
                faces.append(([pt[k_] for k_ in ring], sum(1 for e in es if edge[e] in HER_LAYERS) / float(len(es))))
    loose = [(nm, pt[e[0]], pt[e[1]]) for e, nm in edge.items() if e not in used]
    return faces, loose


def read_model(doc, log):
    """every layer as [[closed, [(x, y)]]] in survey m, uncut; names = [(text, x, y)]"""
    import Rhino
    rg = Rhino.Geometry
    out, cnt = {}, {}

    def curves(names):
        L = []
        for nm in names:
            for o in _layer_objs(doc, nm):
                g = o.Geometry
                if isinstance(g, rg.Curve):
                    cl, P = _curve_pts(g)
                    if len(P) >= 2:
                        L.append((nm, o, cl, P))
        return L
    fr = [P for _, _, cl, P in curves([FRAME_LAYER]) if len(P) >= 4]
    if fr:
        frame = max(fr, key=lambda P: abs(g_area(P)))[:4]
    else:
        frame = list(FRAME_COPY)
        log.append(u"FLAG frame: no closed curve on layer %s in the open model: the built-in copy of site_alan used"
                   % FRAME_LAYER)
    work = [P for _, _, cl, P in curves([WORK_LAYER]) if len(P) >= 3]
    if not work:
        log.append(u"FLAG calisma_alan: no curve on layer %s in the open model: no working-area outline, and "
                   u"Basemap_colour.svg is not written" % WORK_LAYER)
    names = []
    for o in _layer_objs(doc, NAME_LAYER):
        g = o.Geometry
        try:
            if isinstance(g, rg.TextEntity):
                names.append((g.PlainText.strip(), g.Plane.Origin.X, g.Plane.Origin.Y))
            elif isinstance(g, rg.TextDot):
                names.append((g.Text.strip(), g.Point.X, g.Point.Y))
        except Exception:
            pass
    labels = []                                           # [text, x, y, turn deg, kind]
    for lay_, kind in ((STREET_NAME_LAYER, "street"), (NAME_LAYER, "place")):
        for o in _layer_objs(doc, lay_):
            g = o.Geometry
            try:
                if isinstance(g, rg.TextEntity) and g.PlainText.strip():
                    ax = g.Plane.XAxis
                    labels.append([u" ".join(g.PlainText.split()), round(g.Plane.Origin.X, 2), round(g.Plane.Origin.Y, 2),
                                   round(math.degrees(math.atan2(ax.Y, ax.X)), 1), kind])
                elif isinstance(g, rg.TextDot) and g.Text.strip():
                    labels.append([u" ".join(g.Text.split()), round(g.Point.X, 2), round(g.Point.Y, 2), 0.0, kind])
            except Exception:
                pass
    segs = []
    for nm, o, cl, P in curves(BLD_LAYERS):
        Q = list(P) + ([P[0]] if cl else [])
        segs += [(nm, a_, b_) for a_, b_ in zip(Q[:-1], Q[1:])]
    faces, loose = building_faces(segs)
    bld, her = [], []
    grid = {}
    for i, (P, hshare) in enumerate(faces):
        for cx in range(int(min(q[0] for q in P) // 25.0), int(max(q[0] for q in P) // 25.0) + 1):
            for cy in range(int(min(q[1] for q in P) // 25.0), int(max(q[1] for q in P) // 25.0) + 1):
                grid.setdefault((cx, cy), []).append(i)
    inside = {}
    for t, x, y in names:
        for i in grid.get((int(x // 25.0), int(y // 25.0)), ()):
            if g_pip(x, y, faces[i][0]):
                inside.setdefault(i, []).append(t)
    for i, (P, hshare) in enumerate(faces):
        ins = inside.get(i, [])
        word = next((t for t in ins if any(w in u" %s " % t.lower() for w in HERITAGE_WORDS)), None)
        if hshare >= 0.5 or word:
            her.append({"ring": P, "layer": u"BINA_TARIHI / BINA_HARABE" if hshare >= 0.5 else u"name text",
                        "name": word or (ins[0] if ins else u"")})
        else:
            bld.append([True, P])
    n_faces = len(bld)
    fl = {}
    n_txt = 0
    for o in _layer_objs(doc, FLOOR_LAYER):
        g = o.Geometry
        try:
            if isinstance(g, rg.TextEntity):
                t, x, y = g.PlainText.strip(), g.Plane.Origin.X, g.Plane.Origin.Y
            elif isinstance(g, rg.TextDot):
                t, x, y = g.Text.strip(), g.Point.X, g.Point.Y
            else:
                continue
            v = int(float(t.replace(",", ".")))
        except Exception:
            continue
        if not 1 <= v <= 40:
            continue
        n_txt += 1
        for i in grid.get((int(x // 25.0), int(y // 25.0)), ()):
            if g_pip(x, y, faces[i][0]):
                fl[i] = max(fl.get(i, 0), v)
                break
    is_her = set(id(h["ring"]) for h in her)
    floors = {"buildings": [fl.get(i, 0) for i, (P, _) in enumerate(faces) if id(P) not in is_her],
              "heritage": [fl.get(i, 0) for i, (P, _) in enumerate(faces) if id(P) in is_her]}
    log.append(u"floors: %d floor texts on %s; %d of the %d closed outlines have one inside" % (
        n_txt, FLOOR_LAYER, len(fl), len(faces)))
    her_lines = [[False, [a_, b_]] for nm, a_, b_ in loose if nm in HER_LAYERS]
    bld += [[False, [a_, b_]] for nm, a_, b_ in loose if nm not in HER_LAYERS]
    log.append(u"buildings: %d survey lines on %d BINA layers joined into %d closed outlines (%d heritage); %d lines "
               u"close no outline and are drawn as lines" % (len(segs), len(BLD_LAYERS), len(faces), len(her), len(loose)))
    if segs and not faces:
        log.append(u"FLAG buildings: the building lines close no outline: check the BINA layers of the open model")
    out["buildings"] = bld
    out["heritage"] = [[True, h["ring"]] for h in her] + her_lines
    cnt["buildings"], cnt["heritage"] = n_faces, len(her)
    for key, layers in SURVEY:
        out[key] = [[cl, P] for _, _, cl, P in curves(layers)]
        cnt[key] = len(out[key])
    sec = []
    for i, (_, o, cl, P) in enumerate(curves([SECTION_LAYER])):
        nm = u""
        try:
            nm = (o.Attributes.Name or u"").strip()
        except Exception:
            pass
        sec.append({"name": nm or u"L%d" % (i + 1), "line": [P[0], P[-1]]})
    tr = {}                                               # the survey's tree symbols, one per place (0.5 m)
    for lay_ in TREE_LAYERS:
        for o in _layer_objs(doc, lay_):
            g = o.Geometry
            try:
                if isinstance(g, rg.Point):
                    x, y, r = g.Location.X, g.Location.Y, 0.0
                elif isinstance(g, rg.InstanceReferenceGeometry):   # a symbol block: its insertion point
                    q = g.Xform * rg.Point3d(0.0, 0.0, 0.0)
                    x, y, r = q.X, q.Y, 0.0
                elif isinstance(g, rg.Curve):             # a drawn symbol: the middle and half the size of its box
                    b = g.GetBoundingBox(True)
                    x, y = (b.Min.X + b.Max.X) / 2.0, (b.Min.Y + b.Max.Y) / 2.0
                    r = max(b.Max.X - b.Min.X, b.Max.Y - b.Min.Y) / 2.0
                else:
                    continue
            except Exception:
                continue
            k_ = (int(round(x * 2.0)), int(round(y * 2.0)))
            if k_ not in tr or tr[k_][2] < r:
                tr[k_] = [round(x, 2), round(y, 2), round(r, 2), lay_]
    trees = list(tr.values())
    log.append(u"survey trees: %d symbols (%s)" % (len(trees), u", ".join(
        u"%s %d" % (lay_, sum(1 for t in trees if t[3] == lay_)) for lay_ in TREE_LAYERS)))
    log.append(u"model read: " + u", ".join(u"%s %d" % kv for kv in sorted(cnt.items())) +
               u"; name texts %d (streets %d); section lines %d" % (
                   len(labels), sum(1 for l in labels if l[4] == "street"), len(sec)))
    for h in her:
        c = (sum(p[0] for p in h["ring"]) / len(h["ring"]), sum(p[1] for p in h["ring"]) / len(h["ring"]))
        log.append(u"  heritage: %s (%s) at %.0f, %.0f" % (h["name"] or u"no name text inside", h["layer"], c[0], c[1]))
    return {"frame": frame, "layers": out, "sections": sec, "calisma": work, "labels": labels, "floors": floors,
            "trees": trees, "heritage_names": [[h["name"], h["layer"]] for h in her]}


# ================================================================ plane geometry
def g_area(P):
    return 0.5 * sum(P[k - 1][0] * P[k][1] - P[k][0] * P[k - 1][1] for k in range(len(P)))


def g_pip(x, y, P):
    ins, n = False, len(P)
    for i in range(n):
        a, b = P[i - 1], P[i]
        if (a[1] > y) != (b[1] > y) and x < a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]):
            ins = not ins
    return ins


def clip_ring(P, box):
    """Sutherland-Hodgman: a closed ring cut at box (x0, y0, x1, y1)"""
    x0, y0, x1, y1 = box
    for axis, lim, keep_ge in ((0, x0, True), (0, x1, False), (1, y0, True), (1, y1, False)):
        Q = []
        n = len(P)
        for i in range(n):
            a, b = P[i - 1], P[i]
            ia = (a[axis] >= lim) if keep_ge else (a[axis] <= lim)
            ib = (b[axis] >= lim) if keep_ge else (b[axis] <= lim)
            if ia != ib:
                t = (lim - a[axis]) / (b[axis] - a[axis])
                Q.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
            if ib:
                Q.append(b)
        P = Q
        if len(P) < 3:
            return []
    return P


def clip_line(P, box):
    """an open polyline cut at box: the runs inside"""
    x0, y0, x1, y1 = box
    runs, cur = [], []
    for a, b in zip(P[:-1], P[1:]):
        t0, t1 = 0.0, 1.0
        dx, dy = b[0] - a[0], b[1] - a[1]
        ok = True
        for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
            if abs(p) < 1e-12:
                if q < 0:
                    ok = False
                    break
            else:
                t = q / p
                if p < 0:
                    t0 = max(t0, t)
                else:
                    t1 = min(t1, t)
        if not ok or t0 > t1:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
            continue
        pa = (a[0] + dx * t0, a[1] + dy * t0)
        pb = (a[0] + dx * t1, a[1] + dy * t1)
        if not cur or math.hypot(cur[-1][0] - pa[0], cur[-1][1] - pa[1]) > 1e-6:
            if len(cur) >= 2:
                runs.append(cur)
            cur = [pa]
        cur.append(pb)
        if t1 < 1.0:
            runs.append(cur)
            cur = []
    if len(cur) >= 2:
        runs.append(cur)
    return runs


class Frame(object):
    """site_alan turned flat: survey (x, y) -> local (u, v) m, u along the long side with its eastern end right"""

    def __init__(self, corners):
        best = None
        for a, b in zip(corners, corners[1:] + corners[:1]):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            if best is None or L > best[0]:
                best = (L, b[0] - a[0], b[1] - a[1])
        _, vx, vy = best
        if vx < 0:
            vx, vy = -vx, -vy
        self.rot = -math.atan2(vy, vx)
        self.ca, self.sa = math.cos(self.rot), math.sin(self.rot)
        T = [self.raw(p) for p in corners]
        self.u0, self.v0 = min(p[0] for p in T), min(p[1] for p in T)
        self.w = max(p[0] for p in T) - self.u0
        self.h = max(p[1] for p in T) - self.v0

    def raw(self, p):
        return (self.ca * p[0] - self.sa * p[1], self.sa * p[0] + self.ca * p[1])

    def local(self, p):
        q = self.raw(p)
        return (q[0] - self.u0, q[1] - self.v0)

    def north(self):
        """the page direction of survey north (0, 1)"""
        return (-self.sa, self.ca)


# ================================================================ near and far from calisma_alan
class Fade(object):
    """a 10 m raster of the frame (local m): 1 = inside calisma_alan or within FADE_M m of it"""
    C = 10.0

    def __init__(self, D, F):
        self.rows = None
        if not D.get("calisma"):
            return
        c = self.C
        nx, ny = int(F.w // c) + 1, int(F.h // c) + 1
        rows = [bytearray(nx) for _ in range(ny)]
        r = int(math.ceil(FADE_M / c))
        disc = [(i, j) for i in range(-r, r + 1) for j in range(-r, r + 1) if (i * i + j * j) * c * c <= FADE_M * FADE_M]
        seen = set()
        for P in D["calisma"]:
            Q = [F.local(p) for p in P]
            for a, b in zip(Q, Q[1:] + Q[:1]):
                n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / (c / 2.0)))
                for t in range(n + 1):
                    ci = int((a[0] + (b[0] - a[0]) * t / n) // c)
                    cj = int((a[1] + (b[1] - a[1]) * t / n) // c)
                    if (ci, cj) in seen:
                        continue
                    seen.add((ci, cj))
                    for i, j in disc:
                        if 0 <= ci + i < nx and 0 <= cj + j < ny:
                            rows[cj + j][ci + i] = 1
            for j in range(ny):                           # the inside, row by row
                y = (j + 0.5) * c
                xs = sorted(a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]) for a, b in zip(Q, Q[1:] + Q[:1])
                            if (a[1] > y) != (b[1] > y))
                for x0, x1 in zip(xs[0::2], xs[1::2]):
                    for i in range(max(0, int(x0 // c)), min(nx - 1, int(x1 // c)) + 1):
                        rows[j][i] = 1
        self.rows, self.nx, self.ny = rows, nx, ny
        self.share = sum(sum(r_) for r_ in rows) / float(nx * ny)

    def far(self, q):
        if self.rows is None:
            return False
        i = min(self.nx - 1, max(0, int(q[0] // self.C)))
        j = min(self.ny - 1, max(0, int(q[1] // self.C)))
        return not self.rows[j][i]

    def far_ring(self, R):
        return self.far((sum(q[0] for q in R) / len(R), sum(q[1] for q in R) / len(R)))

    def split(self, Q):
        """a polyline as [(far?, run)]: the tone changes where the line leaves the near zone"""
        out = []
        for a, b in zip(Q[:-1], Q[1:]):
            f = self.far(((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0))
            if out and out[-1][0] == f:
                out[-1][1].append(b)
            else:
                out.append((f, [a, b]))
        return out


def load_veg(D, log):
    """the satellite land cover as layers sat_* = [[True, ring]] (outer rings and holes, even-odd), survey m"""
    src = os.path.join(BERGAMA_ROOT, VEG_FILE)
    if not os.path.isfile(src):
        log.append(u"FLAG satellite land cover: %s not found: the maps are drawn without it" % src)
        return {}
    with open(src, encoding="utf-8") as f:
        V = json.load(f)
    out = {}
    for k_, key in VEG_KEYS:
        out[key] = [[True, R] for R in (V.get("rings") or {}).get(k_, []) if len(R) >= 3]
    fr = [tuple(p) for p in D["frame"]]
    cov = clip_ring(fr, VEG_BOX)
    share = abs(g_area(cov)) / abs(g_area(fr)) if len(cov) >= 3 else 0.0
    log.append(u"satellite land cover %s (%s): %s rings; the image covers %.1f %% of the frame, the rest of the frame "
               u"has no land cover drawn" % (os.path.basename(src), V.get("date", u"no date"), u", ".join(
                   u"%s %d" % (key, len(out[key])) for _, key in VEG_KEYS), 100.0 * share))
    return out


# ================================================================ the one style table (Data/bergama_style.json)
def _mix(col, t):
    """col mixed t towards white (t > 0) or towards black (t < 0)"""
    to = 255 if t > 0 else 0
    return u"".join(u"%02X" % int(round(int(col[i:i + 2], 16) + (to - int(col[i:i + 2], 16)) * abs(t))) for i in (0, 2, 4))


def lighter(col, t=None):
    return _mix(col, FADE_MIX if t is None else t)


def load_style():
    """the style table: {"cat": {name: {label, fill, line, w, grain}}, "text": mm sizes, "grain": the tile values}"""
    src = os.path.join(BERGAMA_ROOT, STYLE_FILE)
    if not os.path.isfile(src):
        raise RuntimeError(u"%s not found: run Bergama.bat once (the kit copies it), then press again" % src)
    with open(src, encoding="utf-8") as f:
        J = json.load(f)
    pal = J["palette"]

    def col(ref):
        if not ref:
            return None
        m = re.match(r"^([A-Za-z_]\w*?)([+-]\d*\.?\d+)?$", ref)
        if m and m.group(1) in pal:
            return _mix(pal[m.group(1)], float(m.group(2) or 0.0))
        h = ref.strip().lstrip("#").upper()
        if not re.match(r"^[0-9A-F]{6}$", h):
            raise ValueError(u"%s: unknown colour %r" % (src, ref))
        return h
    cat = {}
    for k_, c in J["categories"].items():
        fill = col(c.get("fill"))
        cat[k_] = {"label": c.get("label", k_), "fill": fill, "line": col(c.get("line")), "w": float(c.get("w") or 0.0),
                   "ticks": ([float(v) for v in c["ticks"][:4]] + [col(c["ticks"][4])]) if c.get("ticks") else None,
                   "grain": (float(c["grain"]) if isinstance(c.get("grain"), (int, float)) and not isinstance(
                       c.get("grain"), bool) else True) if (fill and fill != "FFFFFF" and c.get("grain", True)) else False}
    return {"cat": cat, "text": J["text_mm"], "grain": J.get("grain") or {}, "ink": col("ink"), "col": col,
            "version": J.get("version", u"no version")}


def fill_of(c):
    """a category's fill for the PDF writer: "~RRGGBB" = painted with the grain of that colour"""
    if not c["grain"]:
        return c["fill"]
    t = c.get("ticks")
    return u"~" + c["fill"] + (u"" if c["grain"] is True else u"@%g" % c["grain"]) + (
        (u"|%g,%g,%g,%g,%s" % tuple(t)) if t else u"")


# ================================================================ the grain (one seamless tile, shared by every fill)
_GRAIN = {"amp": 0.0}


def set_grain(S, log=None):
    """the grain tile: px x px cells of LEVELS tones; soft clouds (four sizes) plus a share of fine grain; it repeats
    without a seam. Kept as compressed bytes; write_pdf gives every colour its own tone table over the same cells."""
    g = S.get("grain") or {}
    amp, px = float(g.get("amp", 0.0)), int(g.get("px", 512))
    _GRAIN.clear()
    _GRAIN.update({"amp": amp, "px": px, "tile": float(g.get("tile_mm", 160.0)), "levels": int(g.get("levels", 32))})
    if amp <= 0:
        return
    rnd = random.Random(int(g.get("seed", 7)))
    acc = [[0.0] * px for _ in range(px)]
    tot = 0.0
    for cells, wgt in ((8, 1.0), (16, 0.7), (32, 0.5), (64, 0.35)):
        lat = [[rnd.random() for _ in range(cells)] for _ in range(cells)]
        st = px // cells
        tt = [(i % st) / float(st) for i in range(px)]
        tt = [t * t * (3.0 - 2.0 * t) for t in tt]
        i0 = [i // st for i in range(px)]
        i1 = [(i // st + 1) % cells for i in range(px)]
        rows = [[r[a] + (r[b] - r[a]) * t for a, b, t in zip(i0, i1, tt)] for r in lat]     # along x, per lattice row
        for j in range(px):
            A, B, t = rows[i0[j]], rows[i1[j]], tt[j]
            acc[j] = [v + wgt * (a + (b - a) * t) for v, a, b in zip(acc[j], A, B)]
        tot += wgt
    fine = float(g.get("fine", 0.3))
    lv = _GRAIN["levels"]
    flat = [v for r in acc for v in r]
    lo, hi = min(flat), max(flat)
    out = bytearray()
    for r in acc:
        out += bytes(min(lv - 1, max(0, int(((v - lo) / (hi - lo) * (1.0 - fine) + rnd.random() * fine) * lv))) for v in r)
    _GRAIN["z"] = zlib.compress(bytes(out), 9)
    if log is not None:
        log.append(u"grain: +-%.0f %% of each tone, one %d x %d tile repeated every %.0f mm of paper (%.0f kB per colour)"
                   % (100.0 * amp, px, px, _GRAIN["tile"], len(_GRAIN["z"]) / 1024.0))


# ================================================================ satellite land cover as a stencil, housing cut out
def localise(D, F):
    """every cache layer once in frame m: {key: [(closed, points, umin, umax)]}"""
    L = {}
    for key, items in D["layers"].items():
        out = []
        for cl, P in items:
            Q = [F.local(p) for p in P]
            if not Q or max(q[1] for q in Q) < 0 or min(q[1] for q in Q) > F.h:
                continue
            out.append((cl, Q, min(q[0] for q in Q), max(q[0] for q in Q)))
        L[key] = out
    return L


class Cover(object):
    """rows of bits, COVER_M m cells over the frame (bit i = column i from the west, row 0 = the south edge)"""

    def __init__(self, L, F, log):
        c = self.c = COVER_M
        self.nx, self.ny = int(math.ceil(F.w / c)), int(math.ceil(F.h / c))
        t0 = time.time()
        full = (1 << self.nx) - 1
        faces = self.fill([Q for key in ("buildings", "heritage") for cl, Q, _, _ in L.get(key, []) if cl and len(Q) >= 3])
        loose = [0] * self.ny
        for key in ("buildings", "heritage", "sheds"):
            for cl, Q, _, _ in L.get(key, []):
                if cl and len(Q) >= 3:
                    continue
                for a, b in zip(Q[:-1], Q[1:]):
                    n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / (c * 0.9)))
                    for t in range(n + 1):
                        i, j = int((a[0] + (b[0] - a[0]) * t / n) // c), int((a[1] + (b[1] - a[1]) * t / n) // c)
                        if 0 <= i < self.nx and 0 <= j < self.ny:
                            loose[j] |= 1 << i
        A, B = self.grow(faces, int(round(FACE_HALO_M / c)), full), self.grow(loose, int(round(MASK_M / c)), full)
        built = [a | b for a, b in zip(A, B)]
        self.rows, share = {}, {}
        taken = built
        for key in ("sat_trees",):
            rings = [Q for cl, Q, _, _ in L.get(key, [])]
            big = set(i for i, Q in enumerate(rings) if abs(g_area(Q)) >= COVER_MIN_M2)
            R = self.fill([Q for i, Q in enumerate(rings) if i in big or abs(g_area(Q)) < 0])
            R = [r & ~t & full for r, t in zip(R, taken)]
            self.rows[key] = R
            taken = [r | t for r, t in zip(R, taken)]
            share[key] = sum(bin(r).count("1") for r in R) * c * c
        self.soft = haze_data(self.rows["sat_trees"], F)
        log.append(u"tree cover 2023 as a soft tone: %d x %d cells of %.2f m, %.0f m2 after cutting the housing away "
                   u"(closed outlines + %.0f m, other building lines + %.0f m), patches under %.0f m2 dropped; blurred "
                   u"%.0f m on %.0f m cells (%.1f s)" % (self.nx, self.ny, c, share.get("sat_trees", 0), FACE_HALO_M, MASK_M,
                                                       COVER_MIN_M2, HAZE_BLUR_M, HAZE_C, time.time() - t0))

    def fill(self, rings):
        """even-odd fill of all rings together"""
        c, nx, ny = self.c, self.nx, self.ny
        xs = [[] for _ in range(ny)]
        for Q in rings:
            for i in range(len(Q)):
                a, b = Q[i - 1], Q[i]
                if a[1] == b[1]:
                    continue
                if a[1] > b[1]:
                    a, b = b, a
                j = max(0, int(math.ceil(a[1] / c - 0.5)))
                k_ = (b[0] - a[0]) / (b[1] - a[1])
                while j < ny and (j + 0.5) * c < b[1]:
                    xs[j].append(a[0] + ((j + 0.5) * c - a[1]) * k_)
                    j += 1
        rows = []
        for X in xs:
            X.sort()
            r = 0
            for x0, x1 in zip(X[0::2], X[1::2]):
                a, b = max(0, int(round(x0 / c))), min(nx, int(round(x1 / c)))
                if b > a:
                    r |= ((1 << (b - a)) - 1) << a
            rows.append(r)
        return rows

    @staticmethod
    def grow(rows, r, full):
        for _ in range(r):
            rows = [(m | (m << 1) | (m >> 1)) & full for m in rows]
        n = len(rows)
        for _ in range(r):
            rows = [rows[j] | rows[max(0, j - 1)] | rows[min(n - 1, j + 1)] for j in range(n)]
        return rows

    def item(self, key, u0, u1, x0, y0, k, fill, layer):
        """the stencil of one tone for the window u0..u1 as a "mask" item (None when empty)"""
        c = self.c
        c0, c1 = max(0, int(round(u0 / c))), min(self.nx, int(round(u1 / c)))
        n = c1 - c0
        if n <= 0:
            return None
        nb, m, fmt = (n + 7) // 8, (1 << n) - 1, "0%db" % n
        pad = "0" * (nb * 8 - n)
        out, any_ = bytearray(), 0
        for r in reversed(self.rows[key]):                 # the image's first row is the top
            w = (r >> c0) & m
            any_ |= w
            out += int(format(w, fmt)[::-1] + pad, 2).to_bytes(nb, "big")
        if not any_:
            return None
        return ("mask", zlib.compress(bytes(out), 9), n, self.ny, x0 + (c0 * c - u0) * k, y0, n * c * k, self.ny * c * k,
                fill, None, layer, None)


# ================================================================ masks: joined surfaces from many pieces
# A mask = rows of bits, MASK_C m cells over the frame (bit i = column i from the west, row 0 = the south edge).
# Pieces (street bands, river slices) are painted into one mask and its outline is traced back to vector rings, so
# pieces that meet become ONE surface with one edge: junctions join, nothing overlaps, no line is drawn twice.
def mask_size(F, c):
    return int(math.ceil(F.w / c)), int(math.ceil(F.h / c))


def mask_add(rows, ring, c, nx):
    """paint one ring (frame m) into rows (even-odd inside this ring, OR onto what is there)"""
    ny = len(rows)
    lo = max(0, int(math.floor(min(q[1] for q in ring) / c - 0.5)))
    hi = min(ny - 1, int(math.ceil(max(q[1] for q in ring) / c)))
    if hi < lo:
        return
    xs = [[] for _ in range(hi - lo + 1)]
    for i in range(len(ring)):
        a, b = ring[i - 1], ring[i]
        if a[1] == b[1]:
            continue
        if a[1] > b[1]:
            a, b = b, a
        j = max(lo, int(math.ceil(a[1] / c - 0.5)))
        k_ = (b[0] - a[0]) / (b[1] - a[1])
        while j <= hi and (j + 0.5) * c < b[1]:
            xs[j - lo].append(a[0] + ((j + 0.5) * c - a[1]) * k_)
            j += 1
    for j, X in enumerate(xs):
        X.sort()
        r = 0
        for x0, x1 in zip(X[0::2], X[1::2]):
            a, b = max(0, int(round(x0 / c))), min(nx, int(round(x1 / c)))
            if b > a:
                r |= ((1 << (b - a)) - 1) << a
        rows[j + lo] |= r


def mask_grow(rows, r, nx):
    full = (1 << nx) - 1
    for _ in range(r):
        rows = [(m | (m << 1) | (m >> 1)) & full for m in rows]
    n = len(rows)
    for _ in range(r):
        rows = [rows[j] | rows[max(0, j - 1)] | rows[min(n - 1, j + 1)] for j in range(n)]
    return rows


def mask_close(rows, r, nx):
    """seams and pinholes narrower than 2 r cells are closed (grow, then shrink)"""
    full = (1 << nx) - 1
    g = mask_grow(rows, r, nx)
    inv = mask_grow([~m & full for m in g], r, nx)
    return [(~m & full) | o for m, o in zip(inv, rows)]


def mask_at(rows, c, nx, q):
    i, j = int(q[0] // c), int(q[1] // c)
    return 0 <= j < len(rows) and 0 <= i < nx and (rows[j] >> i) & 1 == 1


_RUN = re.compile("1+")


def _runs(m):
    return [(k.start(), k.end()) for k in _RUN.finditer(bin(m)[:1:-1])] if m else []


def mask_loops(rows, nx):
    """the outline of a mask as closed loops of lattice points (i, j); the inside lies on the left of each loop"""
    ny = len(rows)
    out = {}

    def edge(a, b):
        out.setdefault(a, []).append(b)
    for j in range(ny):
        m = rows[j]
        if not m:
            continue
        below = rows[j - 1] if j else 0
        above = rows[j + 1] if j + 1 < ny else 0
        for a, b in _runs(m):
            edge((a, j + 1), (a, j))
            edge((b, j), (b, j + 1))
        for a, b in _runs(m & ~below):
            edge((a, j), (b, j))
        for a, b in _runs(m & ~above):
            edge((b, j + 1), (a, j + 1))
    loops = []
    while out:
        s, ends = next(iter(out.items()))
        p = s
        lp = []
        while True:
            lp.append(p)
            ends = out[p]
            q = ends.pop()
            if not ends:
                del out[p]
            p = q
            if p == s:
                break
        loops.append(lp)
    return loops


def _dp(P, tol):
    """Douglas-Peucker on an open line"""
    keep = [False] * len(P)
    keep[0] = keep[-1] = True
    st = [(0, len(P) - 1)]
    while st:
        a, b = st.pop()
        if b - a < 2:
            continue
        ax, ay = P[a]
        dx, dy = P[b][0] - ax, P[b][1] - ay
        L_ = math.hypot(dx, dy) or 1e-12
        best, bi = -1.0, a
        for i in range(a + 1, b):
            d = abs((P[i][0] - ax) * dy - (P[i][1] - ay) * dx) / L_ if L_ > 1e-9 else math.hypot(P[i][0] - ax, P[i][1] - ay)
            if d > best:
                best, bi = d, i
        if best > tol:
            keep[bi] = True
            st.append((a, bi))
            st.append((bi, b))
    return [p for p, k_ in zip(P, keep) if k_]


def mask_rings(rows, nx, c, F, tol, min_area, smooth=0):
    """a mask as vector rings in frame m (outer rings and holes together: draw even-odd). Points on the frame edge stay
    on it; the staircase of the cells is straightened to within tol m; rings under min_area m2 are dropped."""
    out = []
    for lp in mask_loops(rows, nx):
        P = [(min(F.w, i * c), min(F.h, j * c)) for i, j in lp]
        if abs(g_area(P)) < min_area:
            continue
        far = max(range(len(P)), key=lambda i: (P[i][0] - P[0][0]) ** 2 + (P[i][1] - P[0][1]) ** 2)
        R = _dp(P[:far + 1], tol)[:-1] + _dp(P[far:] + P[:1], tol)[:-1]
        for _ in range(smooth):                           # corner cutting, never on the frame edge
            Q = []
            for i in range(len(R)):
                a, b = R[i], R[(i + 1) % len(R)]
                on = lambda q: q[0] <= 0 or q[1] <= 0 or q[0] >= F.w or q[1] >= F.h      # noqa: E731
                if on(a) or on(b):
                    Q += [a] if on(a) else []
                    if not on(a):
                        Q.append(a)
                    continue
                Q += [(a[0] * 0.75 + b[0] * 0.25, a[1] * 0.75 + b[1] * 0.25),
                      (a[0] * 0.25 + b[0] * 0.75, a[1] * 0.25 + b[1] * 0.75)]
            R = Q
        if len(R) >= 3:
            out.append(R)
    return out


def join_streets(L, F, log):
    """every street band as ONE surface: L["street_net"] = rings (even-odd), and its mask for the line clean-up"""
    c = MASK_C
    nx, ny = mask_size(F, c)
    rows = [0] * ny
    n = 0
    for cl, Q, _, _ in L.get("streets", []):
        if len(Q) >= 3:
            mask_add(rows, Q, c, nx)
            n += 1
    rows = mask_close(rows, int(round(STREET_CLOSE_M / c)), nx)
    rings = mask_rings(rows, nx, c, F, MASK_TOL * 1.5, STREET_MIN_M2, smooth=1)   # v6.1: corners of the steps cut
    L["street_net"] = [(True, R, min(q[0] for q in R), max(q[0] for q in R)) for R in rings]
    log.append(u"streets joined: %d bands -> one surface of %d outline(s), %d points (junctions meet, no edge crosses a "
               u"street)" % (n, len(rings), sum(len(R) for R in rings)))
    return rows


def stroke_rings(P, hw):
    """a line of half width hw m as rings to paint: one quad per piece and an eight-sided disc on every point"""
    out = []
    for a, b in zip(P[:-1], P[1:]):
        d = math.hypot(b[0] - a[0], b[1] - a[1])
        if d < 1e-9:
            continue
        ox, oy = -(b[1] - a[1]) / d * hw, (b[0] - a[0]) / d * hw
        out.append([(a[0] + ox, a[1] + oy), (b[0] + ox, b[1] + oy), (b[0] - ox, b[1] - oy), (a[0] - ox, a[1] - oy)])
    for q in P:
        out.append([(q[0] + hw * math.cos(i * math.pi / 4.0), q[1] + hw * math.sin(i * math.pi / 4.0)) for i in range(8)])
    return out


def join_rings(shapes, F, close_m, min_m2, tol, smooth=0):
    """shapes [[ring, ...]] (frame m; a shape of several rings is filled even-odd) joined into ONE surface, as
    join_streets does for the street bands: returns (rings to draw even-odd, mask rows)"""
    c = MASK_C
    nx, ny = mask_size(F, c)
    rows = [0] * ny
    for rings in shapes:
        rings = [R for R in rings if len(R) >= 3]
        if len(rings) == 1:
            mask_add(rows, rings[0], c, nx)
        elif rings:                                       # holes stay holes
            tmp = [0] * ny
            for R in rings:
                one = [0] * ny
                mask_add(one, R, c, nx)
                tmp = [a ^ b for a, b in zip(tmp, one)]
            rows = [a | b for a, b in zip(rows, tmp)]
    if close_m:
        rows = mask_close(rows, max(1, int(round(close_m / c))), nx)
    return mask_rings(rows, nx, c, F, tol, min_m2, smooth), rows


def build_river(L, F, log):
    """The river as a filled surface, the site board's technique (selinus_board river: 'the channel, sorted by the
    survey itself'): along the Selinos centreline, every RIVER_STEP m, the edge on each side is the survey's stream
    line (HIDRO_DERE_*) met by the cross line within RIVER_REACH m; a side with no stream line there takes the width
    between its measured neighbours; a stretch with no stream line on either side for more than RIVER_GAP m is not
    drawn (covered or not surveyed). The slices are joined into one surface and outlined once.
    Returns the mask rows (or None); L["river"] = rings."""
    src = os.path.join(BERGAMA_ROOT, CENTRE_FILE)
    banks = L.get("stream_banks", [])
    if not os.path.isfile(src) or not banks:
        log.append(u"FLAG river: %s: the stream is drawn as its survey lines only" % (
            (u"%s not found" % src) if not os.path.isfile(src) else u"no stream lines in the survey"))
        return None
    with open(src, encoding="utf-8") as f:
        C = [F.local(p) for p in json.load(f)["points"]]
    g = SegGrid()
    for cl, Q, _, _ in banks:
        for a, b in zip(Q[:-1], Q[1:]):
            g.add(a, b)
    st = []                                               # stations (point, normal) inside the frame + reach
    for a, b in zip(C[:-1], C[1:]):
        d = math.hypot(b[0] - a[0], b[1] - a[1])
        if d < 1e-6:
            continue
        nx_, ny_ = -(b[1] - a[1]) / d, (b[0] - a[0]) / d
        for i in range(int(d // RIVER_STEP) + 1):
            p = (a[0] + (b[0] - a[0]) * i * RIVER_STEP / d, a[1] + (b[1] - a[1]) * i * RIVER_STEP / d)
            if -RIVER_REACH <= p[0] <= F.w + RIVER_REACH and -RIVER_REACH <= p[1] <= F.h + RIVER_REACH:
                st.append((p, (nx_, ny_)))
    if len(st) < 3:
        log.append(u"FLAG river: the centreline %s does not cross the frame: survey lines only" % src)
        return None
    W = [[g.hit(p[0], p[1], n[0] * s, n[1] * s, RIVER_REACH) for p, n in st] for s in (1.0, -1.0)]
    n_meas = [sum(1 for v in w if v is not None) for w in W]
    open_ = [W[0][i] is not None or W[1][i] is not None for i in range(len(st))]
    gap = int(RIVER_GAP / RIVER_STEP)
    i = 0
    while i < len(st):                                    # short gaps stay open water, long ones are left out
        if not open_[i]:
            j = i
            while j < len(st) and not open_[j]:
                j += 1
            if j - i <= gap:
                for k_ in range(i, j):
                    open_[k_] = True
            i = j
        else:
            i += 1
    for w in W:                                           # a missing side: the width between its measured neighbours
        known = [i for i, v in enumerate(w) if v is not None]
        if not known:
            log.append(u"FLAG river: no stream line met on one side of the centreline: survey lines only")
            return None
        for i in range(len(w)):
            if w[i] is None:
                lo = max([k_ for k_ in known if k_ < i] or [None], key=lambda v: -1 if v is None else v)
                hi = min([k_ for k_ in known if k_ > i] or [None], key=lambda v: 10 ** 9 if v is None else v)
                if lo is None:
                    w[i] = w[hi]
                elif hi is None:
                    w[i] = w[lo]
                else:
                    w[i] = w[lo] + (w[hi] - w[lo]) * (i - lo) / float(hi - lo)
    for w in W:                                           # one stray hit (a side stream's line) is evened out: median of 5
        w[:] = [sorted(w[max(0, i - 2):i + 3])[len(w[max(0, i - 2):i + 3]) // 2] for i in range(len(w))]
    c = MASK_C
    nx, ny = mask_size(F, c)
    rows = [0] * ny
    m_open = 0.0
    for i in range(len(st) - 1):
        if not (open_[i] and open_[i + 1]):
            continue
        (p, n), (q, n2) = st[i], st[i + 1]
        if math.hypot(q[0] - p[0], q[1] - p[1]) > 2 * RIVER_STEP:
            continue
        quad = [(p[0] + n[0] * W[0][i], p[1] + n[1] * W[0][i]), (q[0] + n2[0] * W[0][i + 1], q[1] + n2[1] * W[0][i + 1]),
                (q[0] - n2[0] * W[1][i + 1], q[1] - n2[1] * W[1][i + 1]), (p[0] - n[0] * W[1][i], p[1] - n[1] * W[1][i])]
        mask_add(rows, quad, c, nx)
        m_open += RIVER_STEP
    rows = mask_close(rows, int(round(RIVER_CLOSE_M / c)), nx)
    rings = mask_rings(rows, nx, c, F, MASK_TOL * 2, RIVER_MIN_M2, smooth=2)
    L["river"] = [(True, R, min(q[0] for q in R), max(q[0] for q in R)) for R in rings]
    log.append(u"river: %d cross lines every %.0f m along %s; stream line met on %d (one side) / %d (other side) of them, "
               u"the rest carried between measured neighbours; %.0f m drawn as open water, %d outline(s), %.0f m2" % (
                   len(st), RIVER_STEP, os.path.basename(src), n_meas[0], n_meas[1], m_open, len(rings),
                   sum(bin(r).count("1") for r in rows) * c * c))
    return rows


def clean_lines(L, F, street_rows, river_rows, log):
    """the line clean-up: no line twice, no line beside its own copy, no stubs.
    1 building lines drawn twice (same two ends to 1 cm) are kept once; a building line that hangs loose at one end
      and on a corner of three or more lines at the other and is shorter than TICK_M m (the old town's party-wall
      ticks), or loose at both ends and shorter than CRUMB_M m, is dropped, once (v5 repeated it and ate whole open house outlines)
    2 survey road edges and kerbs inside the joined street surface or within NEAR_M m of it are dropped: there the
      street's own edge is the line (the survey edge and the band edge ran side by side, slightly apart)
    3 survey stream lines inside the river surface or within NEAR_M m of it are dropped: the river's edge is the line"""
    c = MASK_C
    nx, _ = mask_size(F, c)

    def key(p):
        return (int(round(p[0] * 100.0)), int(round(p[1] * 100.0)))
    deg, seen, kept, dup = {}, set(), [], 0
    for name in ("buildings", "heritage"):
        for it in L.get(name, []):
            cl, Q = it[0], it[1]
            if cl and len(Q) >= 3:
                for q in Q:
                    deg[key(q)] = deg.get(key(q), 0) + 2
    open_ = []
    for it in L.get("buildings", []):
        cl, Q = it[0], it[1]
        if cl and len(Q) >= 3:
            kept.append(it)
            continue
        e = tuple(sorted((key(Q[0]), key(Q[-1])))) if len(Q) == 2 else None
        if e is not None and e in seen:
            dup += 1
            continue
        if e is not None:
            seen.add(e)
        open_.append(it)
        for q in (Q[0], Q[-1]):
            deg[key(q)] = deg.get(key(q), 0) + 1
    ticks = 0
    while True:
        rest, cut = [], 0
        for it in open_:
            Q = it[1]
            a, b = key(Q[0]), key(Q[-1])
            da, db = deg.get(a, 0), deg.get(b, 0)         # a tick: free at both ends, or free at one end and on a
            d_ = math.hypot(Q[-1][0] - Q[0][0], Q[-1][1] - Q[0][1])   # corner of 3+ lines; a crumb: free at both, tiny
            tick = ((da <= 1 and db >= 3) or (db <= 1 and da >= 3)) and d_ < TICK_M
            if len(Q) == 2 and (tick or (da <= 1 and db <= 1 and d_ < CRUMB_M)):
                cut += 1
            else:
                rest.append(it)
        open_ = rest
        ticks += cut
        break                                             # once only: repeating it ate whole open house outlines
    L["buildings"] = kept + open_
    drops, frag = {}, {}
    for names, rows in ((("road_edges", "kerbs", "bridges"), street_rows), (("stream_banks",), river_rows)):
        if rows is None:
            continue
        zone = mask_grow(rows, int(round(NEAR_M / c)), nx)
        for name in names:
            out = []
            for cl, Q, a, b in L.get(name, []):
                run = []
                for i in range(len(Q) - 1):
                    mid = ((Q[i][0] + Q[i + 1][0]) / 2.0, (Q[i][1] + Q[i + 1][1]) / 2.0)
                    if mask_at(zone, c, nx, mid):
                        drops[name] = drops.get(name, 0) + 1
                        if len(run) >= 2:
                            out.append((False, run, min(q[0] for q in run), max(q[0] for q in run)))
                        run = []
                    else:
                        run = run or [Q[i]]
                        run.append(Q[i + 1])
                if len(run) >= 2:
                    out.append((False, run, min(q[0] for q in run), max(q[0] for q in run)))
            if drops.get(name):                           # v6.1: what the cut left as crumbs goes too
                keep = [it for it in out if sum(math.hypot(b_[0] - a_[0], b_[1] - a_[1])
                                                for a_, b_ in zip(it[1][:-1], it[1][1:])) >= FRAG_M]
                frag[name] = len(out) - len(keep)
                out = keep
            L[name] = out
    log.append(u"line clean-up: %d building lines drawn twice kept once; %d loose stubs under %.0f m dropped; pieces "
               u"dropped beside or inside a joined surface (within %.1f m): %s" % (
                   dup, ticks, TICK_M, NEAR_M, u", ".join(u"%s %d" % kv for kv in sorted(drops.items())) or u"none") +
               u"; leftover pieces under %.0f m dropped: %s" % (
                   FRAG_M, u", ".join(u"%s %d" % kv for kv in sorted(frag.items())) or u"none"))


def haze_data(rows_or_discs, F):
    """a soft tone that fades out at its edge (A05's green under the trees), as (zlib 8-bit rows, px w, px h) or None.
    rows_or_discs = mask rows (MASK_C cells) or [(u, v, radius m)]; coverage on HAZE_C m cells, blurred HAZE_BLUR_M m"""
    c2 = HAZE_C
    nx2, ny2 = int(math.ceil(F.w / c2)), int(math.ceil(F.h / c2))
    G = [[0.0] * nx2 for _ in range(ny2)]
    if rows_or_discs and isinstance(rows_or_discs[0], int):
        f = int(round(c2 / MASK_C))
        for j2 in range(ny2):
            acc = [0] * nx2
            for r in rows_or_discs[j2 * f:(j2 + 1) * f]:
                if r:
                    s = bin(r)[:1:-1]
                    for a, b in ((k.start(), k.end()) for k in _RUN.finditer(s)):
                        for i2 in range(a // f, min(nx2 - 1, (b - 1) // f) + 1):
                            acc[i2] += min(b, (i2 + 1) * f) - max(a, i2 * f)
            G[j2] = [v / float(f * f) for v in acc]
    else:
        for u, v, r in rows_or_discs:
            rr = r / c2
            for j2 in range(max(0, int((v - r) / c2)), min(ny2 - 1, int((v + r) / c2)) + 1):
                dy = (j2 + 0.5) - v / c2
                if abs(dy) > rr:
                    continue
                h = math.sqrt(rr * rr - dy * dy)
                row = G[j2]
                for i2 in range(max(0, int(u / c2 - h)), min(nx2 - 1, int(u / c2 + h)) + 1):
                    row[i2] = 1.0
    if not any(any(r) for r in G):
        return None
    rb = max(1, int(round(HAZE_BLUR_M / c2)))
    for _ in range(2):                                    # two box blurs each way = a soft edge
        H = []
        for row in G:
            ps = [0.0]
            for v in row:
                ps.append(ps[-1] + v)
            H.append([(ps[min(nx2, i + rb + 1)] - ps[max(0, i - rb)]) / (2 * rb + 1) for i in range(nx2)])
        cols = [[0.0] * (ny2 + 1) for _ in range(nx2)]
        G = [[0.0] * nx2 for _ in range(ny2)]
        for i in range(nx2):
            ps = cols[i]
            for j in range(ny2):
                ps[j + 1] = ps[j] + H[j][i]
        for j in range(ny2):
            lo, hi = max(0, j - rb), min(ny2, j + rb + 1)
            G[j] = [(cols[i][hi] - cols[i][lo]) / (2 * rb + 1) for i in range(nx2)]
    out = bytearray()
    for row in reversed(G):
        out += bytes(min(255, int(v * HAZE_MAX * 255.0)) for v in row)
    return (zlib.compress(bytes(out), 9), nx2, ny2)


def soft_item(data, colour, layer, clip, den, x0, y0):
    """a haze_data() tone placed with the frame's lower-left at page (x0, y0) mm"""
    k = 1000.0 / den
    return ("soft", data[0], data[1], data[2], x0, y0, data[1] * HAZE_C * k, data[2] * HAZE_C * k, colour, None, layer, clip)





# ================================================================ drawing (items in page mm, y up)
# cache layer -> style category, PDF layer; drawn in this order
CONTEXT = [
    ("river", "water", "existing_water"), ("stream_banks", "stream_bank", "existing_water"),
    ("ponds", "pond", "existing_water"), ("paths", "path", "existing_paths"),
    ("street_net", "street", "existing_streets"), ("road_edges", "road_edge", "existing_roads"),
    ("bridges", "bridge", "existing_bridges"), ("heritage_walls", "heritage_wall", "existing_heritage"),
    ("buildings", "building", "existing_buildings"), ("heritage", "heritage", "existing_heritage")]
KEY_SKIP = ("paths",)              # too fine for the key map; everything else the same


def draw_context(L, F, S, den, x0, y0, u0, u1, lw_k=1.0, cover=None, fade=None, skip=()):
    """the existing situation at 1:den, the frame's lower-left at page (x0, y0) mm (always the whole frame: u0 = 0,
    u1 = F.w); returns (items, {style category: count})"""
    k = 1000.0 / den
    box = (u0, 0.0, u1, F.h)
    items, cnt = [], {}

    def pg(p):
        return (x0 + (p[0] - u0) * k, y0 + p[1] * k)
    if cover is not None and cover.soft:
        items.append(soft_item(cover.soft, S["cat"]["tree_cover"]["fill"], "satellite_trees", None, den, x0, y0))
        cnt["tree_cover"] = 1
    for key, cname, layer in CONTEXT:
        if key in skip:
            continue
        c = S["cat"][cname]
        stroke, lw, fill = c["line"], c["w"] * lw_k, fill_of(c)
        fd = fade if (fade is not None and fade.rows is not None and key in FADE_KEYS and stroke) else None
        far_ = lighter(stroke) if fd else stroke
        n = 0
        if key in ("street_net", "river"):               # one joined surface: all rings in one even-odd shape
            rings = [R for R in (clip_ring(Q, box) for cl, Q, a, b in L.get(key, [])) if len(R) >= 3]
            if not rings:
                continue
            items.append(("poly", [[pg(q) for q in R] for R in rings], fill, None, 0.0, None, layer, 1, "eo", None))
            if key == "street_net":                      # its one edge, lighter far from the working area
                for R in rings:
                    run_ = []
                    for a, b in zip(R, R[1:] + R[:1]):   # never along the frame: the frame line is drawn there
                        on = (a[0] <= 0 and b[0] <= 0) or (a[1] <= 0 and b[1] <= 0) or \
                            (a[0] >= F.w and b[0] >= F.w) or (a[1] >= F.h and b[1] >= F.h)
                        if on:
                            if len(run_) >= 2:
                                for f_, run in (fd.split(run_) if fd else [(False, run_)]):
                                    items.append(("line", [pg(q) for q in run], far_ if f_ else stroke, lw, None, layer, 1))
                            run_ = []
                        else:
                            run_ = run_ or [a]
                            run_.append(b)
                    if len(run_) >= 2:
                        for f_, run in (fd.split(run_) if fd else [(False, run_)]):
                            items.append(("line", [pg(q) for q in run], far_ if f_ else stroke, lw, None, layer, 1))
            cnt[cname] = len(rings)
            continue
        for cl, Q, a, b in L.get(key, []):
            if b < u0 or a > u1:
                continue
            if cl and len(Q) >= 3:
                R = clip_ring(Q, box)
                if len(R) >= 3:
                    items.append(("poly", [[pg(q) for q in R]], fill, far_ if (fd and fd.far_ring(R)) else stroke, lw,
                                  None, layer, 1, None, None))
                    n += 1
            elif stroke:
                for run_ in clip_line(Q, box):
                    for f_, run in (fd.split(run_) if fd else [(False, run_)]):
                        items.append(("line", [pg(q) for q in run], far_ if f_ else stroke, lw, None, layer, 1))
                    n += 1
        if n:
            cnt[cname] = cnt.get(cname, 0) + n
    return items, cnt


def draw_top(D, F, S, den, x0, y0, u0, u1, names=False, sections=False, lw_k=1.0):
    """what lies over everything: the frame of the window, calisma_alan, the names, the section lines"""
    k = 1000.0 / den
    box = (u0, 0.0, u1, F.h)
    items = []

    def pg(p):
        return (x0 + (p[0] - u0) * k, y0 + p[1] * k)
    c = S["cat"]["calisma"]
    for P in D.get("calisma", []):
        R = [F.local(p) for p in P]
        for run in clip_line(R + R[:1], box):
            items.append(("line", [pg(q) for q in run], c["line"], c["w"] * lw_k, None, "calisma_alan", 1))
    c = S["cat"]["frame"]
    items.append(("poly", [[pg(q) for q in ((u0, 0), (u1, 0), (u1, F.h), (u0, F.h))]], None, c["line"], c["w"] * lw_k, None,
                  "frame", 0, None, None))
    if names:
        nm, ncol = S["text"]["names"], S["cat"]["road_edge"]["line"]
        for t, x, y, ang, kind in D.get("labels", []):
            u, v = F.local((x, y))
            if not (u0 + 2.0 < u < u1 - 2.0 and 2.0 < v < F.h - 2.0):
                continue
            a = (ang + math.degrees(F.rot)) % 360.0
            if 90.0 < a <= 270.0:                         # never upside down
                a -= 180.0
            X, Y = pg((u, v))
            items.append(("text", t, X, Y, nm, ncol, False, "L", "names_streets" if kind == "street" else "names_places",
                          a, "i" if kind == "street" else None))
    if sections:
        c = S["cat"]["section_line"]
        ts = 2.2 if lw_k >= 0.6 else 1.6
        placed = []                                       # (x, level): one name per line, above its upper end
        for s in sorted(D.get("sections", []), key=lambda s_: s_["name"]):
            a, b = F.local(s["line"][0]), F.local(s["line"][1])
            for run in clip_line([a, b], box)[:1]:
                items.append(("line", [pg(q) for q in run], c["line"], c["w"] * lw_k, None, "section_lines", 1))
                X, Y = pg(max(run[0], run[-1], key=lambda q: q[1]))
                wd = text_w(s["name"], ts, True) + 1.0
                lvl = 0
                while any(l_ == lvl and abs(X - x_) < wd for x_, l_ in placed):
                    lvl += 1
                placed.append((X, lvl))
                if lvl:                                   # a thin leader up to a stacked name
                    items.append(("line", [(X, Y), (X, Y + 0.6 + lvl * ts * 1.3)], c["line"], 0.05, None,
                                  "section_lines", 1))
                items.append(("text", s["name"], X, Y + 0.8 + lvl * ts * 1.3, ts, c["line"], True, "C", "section_lines",
                              None, None))
    return items


def corner_block(F, S, den, xr, y0):
    """north circle, scale text and a segmented scale bar inside the lower right corner (xr = the frame's right edge)"""
    INK = S["ink"]
    k = 1000.0 / den
    bar = 100.0 if den <= 2500 else 500.0
    L = bar * k
    w, h = L + 26.0, 16.0
    X, Y = xr - w - 4.0, y0 + 4.0
    it = [("poly", [[(X, Y), (X + w, Y), (X + w, Y + h), (X, Y + h)]], "FFFFFF", None, 0.0, None, "corner_block", 1,
           None, None)]
    cx, cy, r = X + 8.0, Y + 8.0, 5.5
    it.append(("poly", [[(cx + r * math.cos(a * math.pi / 24.0), cy + r * math.sin(a * math.pi / 24.0))
                         for a in range(48)]], None, INK, 0.2, None, "corner_block", 1, None, None))
    nx, ny = F.north()
    tip = (cx + nx * r, cy + ny * r)
    it.append(("poly", [[tip, (cx - nx * r * 0.55 - ny * r * 0.45, cy - ny * r * 0.55 + nx * r * 0.45), (cx, cy),
                         (cx - nx * r * 0.55 + ny * r * 0.45, cy - ny * r * 0.55 - nx * r * 0.45)]], INK, None, 0.1, None,
               "corner_block", 1, None, None))
    it.append(("text", u"N", tip[0] + nx * 2.0 - 0.8, tip[1] + ny * 2.0 - 0.8, 2.4, INK, True, "L", "corner_block", None,
               None))
    xb, yb = X + 20.0, Y + 4.0
    for i in range(4):                                    # four cells, dark and white in turn
        c = [(xb + L * i / 4.0, yb), (xb + L * (i + 1) / 4.0, yb), (xb + L * (i + 1) / 4.0, yb + 1.4),
             (xb + L * i / 4.0, yb + 1.4)]
        it.append(("poly", [c], INK if i % 2 == 0 else "FFFFFF", INK, 0.15, None, "corner_block", 1, None, None))
    it.append(("text", u"0", xb, yb - 3.0, 2.0, INK, False, "C", "corner_block", None, None))
    it.append(("text", u"%d m" % bar, xb + L, yb - 3.0, 2.0, INK, False, "C", "corner_block", None, None))
    it.append(("text", u"1/%d" % den, xb, yb + 4.0, 3.2, INK, True, "L", "corner_block", None, None))
    return it


def furniture(S, x, y, width, tk, title, sub, legend, credit=None):
    """title, subtitle, legend and credit from (x, y) downwards inside width mm; text sizes x tk.
    legend = [style category]; a filled category shows a swatch, a line category a line. Returns (items, height mm)"""
    T, INK = S["text"], S["ink"]
    it = []
    yy = y - T["title"] * tk
    it.append(("text", title.upper(), x, yy, T["title"] * tk, INK, True, "L", "title", None, None))
    yy -= T["subtitle"] * tk * 1.5
    it.append(("text", sub, x, yy, T["subtitle"] * tk, INK, False, "L", "title", None, None))
    yy -= T["subtitle"] * tk * 1.2
    sw, sh, ts = 10.0 * tk, 6.0 * tk, T["legend"] * tk
    xx = x
    yy -= sh * 1.5
    for cname in legend:
        c = S["cat"][cname]
        need = sw + 2.5 * tk + text_w(c["label"], ts) + 8.0 * tk
        if xx > x and xx + need > x + width:
            xx = x
            yy -= sh * 1.6
        if c["fill"]:
            box_ = [(xx, yy), (xx + sw, yy), (xx + sw, yy + sh), (xx, yy + sh)]
            it.append(("poly", [box_], fill_of(c), c["line"] or S["cat"]["kerb"]["line"], c["w"] or 0.05, None, "legend", 1,
                       None, None))
        else:
            it.append(("line", [(xx, yy + sh / 2.0), (xx + sw, yy + sh / 2.0)], c["line"], min(max(c["w"] * LEGEND_LINE_K, LEGEND_LINE_MIN), sh * 0.2), None,
                       "legend", 1))
        it.append(("text", c["label"], xx + sw + 2.5 * tk, yy + sh / 2.0 - ts * 0.36, ts, INK, False, "L", "legend", None,
                   None))
        xx += need
    if credit:
        cs = T["credit"] * tk
        words, line = credit.split(u" "), u""
        yy -= cs * 1.2
        for wd in words + [None]:
            if wd is None or text_w(line + u" " + wd, cs) > width:
                yy -= cs * 1.4
                it.append(("text", line, x, yy, cs, S["cat"]["road_edge"]["line"], False, "L", "title", None, None))
                line = wd or u""
            else:
                line = (line + u" " + wd).strip()
    return it, y - yy + 2.0


def prepare(D, L, F, log):
    """what every drawing of the set shares: the streets as one surface, the river as one surface, the clean lines"""
    street_rows = join_streets(L, F, log)
    river_rows = build_river(L, F, log)
    clean_lines(L, F, street_rows, river_rows, log)


def load_sections(D, log):
    """section lines for the key map: the model's layer, else Data/section_lines.json"""
    if D.get("sections"):
        return
    src = os.path.join(BERGAMA_ROOT, SECTION_FILE)
    try:
        with open(src, encoding="utf-8") as f:
            J = json.load(f)
        D["sections"] = [{"name": k_, "line": v} for k_, v in sorted(J["lines"].items())]
        log.append(u"section lines: none on layer %s in the model, %d read from %s" % (SECTION_LAYER, len(D["sections"]), src))
    except Exception:
        log.append(u"no curves on layer %s in the model and no %s: the key map has no section lines" % (SECTION_LAYER, src))


def a0_scale(F):
    """the smallest round scale 1:N at which the whole frame fits on A0 landscape in one piece"""
    need = max(F.w * 1000.0 / (A0_W - 2 * A0_MARGIN), F.h * 1000.0 / (A0_H - 2 * A0_MARGIN - 80.0))
    return int(math.ceil(need / A0_STEP) * A0_STEP)


def sheet(F, S, den, a0, title, sub, legend_of, credit, band_fn, key_fn=None):
    """lay a drawing out, always the whole frame in ONE piece (Aras 12 Nov 19:42 UTC: never divided): on a page as
    large as the frame, or centred on A0 landscape. band_fn(den, x, y, 0, F.w, tag) -> (items, clips, counts).
    legend_of(counts) -> [style category]. key_fn is not used any more (kept so older callers still run).
    Returns (page w mm, page h mm, items, clips, counts)"""
    k = 1000.0 / den
    m = A0_MARGIN
    fw = F.w * k
    if a0:
        w, h, tk = A0_W, A0_H, 1.0
        x, y = (w - fw) / 2.0, (h - F.h * k) / 2.0 + 30.0
        fx, fy = x, y - 8.0
    else:
        tk = max(0.3, min(1.0, (fw + 2 * m) / A0_W))
        probe, fh = furniture(S, 0.0, 0.0, fw, tk, title, sub, list(S["cat"])[:14], credit)
        fh = max(fh + 6.0 * tk, 24.0 if tk < 0.5 else 0.0)
        w, h = fw + 2 * m, F.h * k + 2 * m + fh
        x, y = m, m + fh
        fx, fy = m, m + fh - 3.0 * tk
    items, clips, cnt = band_fn(den, x, y, 0.0, F.w, "b0")
    if not a0 and tk < 0.5:                               # a small sheet: north and scale under the frame, off the map
        items += corner_block(F, S, den, x + fw + 4.0, y - 23.0)
    else:
        items += corner_block(F, S, den, x + fw, y)
    fi, _ = furniture(S, fx, fy, fw, tk, title, sub, legend_of(cnt), credit)
    return w, h, items + fi, clips, cnt


# ================================================================ the continuous street net
def to_survey(lon, lat):
    phi = math.radians(lat)
    lam = math.radians(lon - 27.0)
    sn, c, t = math.sin(phi), math.cos(phi), math.tan(phi)
    N = _A / math.sqrt(1 - _E2 * sn * sn)
    T, Cc, Aa = t * t, _EP2 * c * c, c * lam
    e4, e6 = _E2 * _E2, _E2 ** 3
    M = _A * ((1 - _E2 / 4 - 3 * e4 / 64 - 5 * e6 / 256) * phi
              - (3 * _E2 / 8 + 3 * e4 / 32 + 45 * e6 / 1024) * math.sin(2 * phi)
              + (15 * e4 / 256 + 45 * e6 / 1024) * math.sin(4 * phi) - (35 * e6 / 3072) * math.sin(6 * phi))
    E = N * (Aa + (1 - T + Cc) * Aa ** 3 / 6 + (5 - 18 * T + T * T + 72 * Cc - 58 * _EP2) * Aa ** 5 / 120) + 500000.0
    Nn = M + N * t * (Aa * Aa / 2 + (5 - T + 9 * Cc + 4 * Cc * Cc) * Aa ** 4 / 24
                      + (61 - 58 * T + T * T + 600 * Cc - 330 * _EP2) * Aa ** 6 / 720)
    c_, s_ = math.cos(GEO["th"]), math.sin(GEO["th"])
    return (GEO["s"] * (c_ * E - s_ * Nn) + GEO["tx"], GEO["s"] * (s_ * E + c_ * Nn) + GEO["ty"])


class SegGrid(object):
    """line segments in 15 m cells; hit() = the nearest one a ray meets"""
    C = 15.0

    def __init__(self):
        self.g = {}

    def add(self, a, b):
        C = self.C
        for i in range(int(min(a[0], b[0]) // C), int(max(a[0], b[0]) // C) + 1):
            for j in range(int(min(a[1], b[1]) // C), int(max(a[1], b[1]) // C) + 1):
                self.g.setdefault((i, j), []).append((a[0], a[1], b[0] - a[0], b[1] - a[1]))

    def hit(self, px, py, dx, dy, rm):
        C = self.C
        ex, ey = px + dx * rm, py + dy * rm
        best = None
        for i in range(int(min(px, ex) // C), int(max(px, ex) // C) + 1):
            for j in range(int(min(py, ey) // C), int(max(py, ey) // C) + 1):
                for ax, ay, sx, sy in self.g.get((i, j), ()):
                    den = dx * sy - dy * sx
                    if abs(den) < 1e-12:
                        continue
                    t = ((ax - px) * sy - (ay - py) * sx) / den
                    if t <= 0.3 or t > rm or (best is not None and t >= best):
                        continue
                    u = ((ax - px) * dy - (ay - py) * dx) / den
                    if -1e-9 <= u <= 1.0 + 1e-9:
                        best = t
        return best


def _median(v):
    v = sorted(v)
    return v[len(v) // 2] if v else None


def build_streets(D, F, log):
    """{"streets": [[True, band ring]], "paths": [[False, line]]} in survey m; see the head of the file"""
    src = os.path.join(BERGAMA_ROOT, OSM_FILE)
    if not os.path.isfile(src):
        log.append(u"FLAG streets: %s not found: only the survey's own road edges are drawn" % src)
        return {}
    key = u"%s|%d|%d|%d|%s" % (D.get("key"), os.path.getsize(src), int(os.path.getmtime(src)), STREET_FORMAT,
                               (STREET_STEP, EDGE_MAX, FRONT_MAX, STREET_MIN))
    if os.path.isfile(STREET_FILE):
        try:
            with open(STREET_FILE, encoding="utf-8") as f:
                S = json.load(f)
            if S.get("key") == key:
                log.append(u"streets: %s used (same model and OSM file): %s" % (STREET_FILE, S.get("note", u"")))
                return S["layers"]
        except Exception:
            pass
    t0 = time.time()
    pad = 45.0

    def near(p, m=pad):
        u, v = F.local(p)
        return -m <= u <= F.w + m and -m <= v <= F.h + m
    g_edge, g_front = SegGrid(), SegGrid()
    for g, keys in ((g_edge, ("road_edges", "kerbs")), (g_front, ("buildings", "heritage", "walls", "heritage_walls"))):
        for k_ in keys:
            for cl, P in D["layers"].get(k_, []):
                Q = list(P) + ([P[0]] if cl else [])
                for a, b in zip(Q[:-1], Q[1:]):
                    if near(a) or near(b):
                        g.add(a, b)
    root = ET.parse(src).getroot()
    nodes = {}
    for n in root.iter("node"):
        try:
            nodes[n.get("id")] = (float(n.get("lon")), float(n.get("lat")))
        except (TypeError, ValueError):
            pass
    proj = {}
    ways, paths = [], []
    for w in root.iter("way"):
        tags = dict((t.get("k"), t.get("v")) for t in w.findall("tag"))
        h = tags.get("highway")
        if not h or h in SKIP_CLASSES or tags.get("area") == "yes":
            continue
        if tags.get("footway") in ("sidewalk", "crossing") or tags.get("path") == "sidewalk":
            continue                                      # part of a street, already inside its band
        P = []
        for nd in w.findall("nd"):
            r = nd.get("ref")
            if r in nodes:
                if r not in proj:
                    proj[r] = to_survey(*nodes[r])
                if not P or math.hypot(proj[r][0] - P[-1][0], proj[r][1] - P[-1][1]) > 0.05:
                    P.append(proj[r])
        if len(P) < 2 or not any(near(p, 30.0) for p in P):
            continue
        if h in PATH_CLASSES:
            paths.append([False, [[round(p[0], 2), round(p[1], 2)] for p in P]])
            continue
        S = []                                            # a point every STREET_STEP m: (x, y, nx, ny)
        for a, b in zip(P[:-1], P[1:]):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            n = max(1, int(round(L / STREET_STEP)))
            for i in range(n):
                S.append((a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n, -(b[1] - a[1]) / L, (b[0] - a[0]) / L))
        a, b = P[-2], P[-1]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        S.append((b[0], b[1], -(b[1] - a[1]) / L, (b[0] - a[0]) / L))
        side = []
        for sg in (1.0, -1.0):
            v, src_ = [], []
            for x, y, nx, ny in S:
                e = g_edge.hit(x, y, sg * nx, sg * ny, EDGE_MAX)
                f = g_front.hit(x, y, sg * nx, sg * ny, FRONT_MAX)
                if e is not None and (f is None or e <= f):
                    v.append(e)
                    src_.append("e")
                elif f is not None:
                    v.append(f)
                    src_.append("f")
                else:
                    v.append(None)
                    src_.append("n")
            side.append((v, src_))
        ways.append(dict(h=h, S=S, side=side))
    cls = {}
    for W in ways:
        for v, _ in W["side"]:
            cls.setdefault(W["h"], []).extend(x for x in v if x is not None)
    cmed = dict((h, _median(v)) for h, v in cls.items() if v)
    allmed = _median([x for v in cls.values() for x in v])
    m = {"e": 0.0, "f": 0.0, "n": 0.0, "class": 0.0}
    bands, dropped = [], 0
    for W in ways:
        S, off = W["S"], []
        for v, src_ in W["side"]:
            known = [x for x in v if x is not None]
            med = _median(known)
            if med is not None:                           # a far hit across a junction or a yard is not the street edge
                lim = max(1.8 * med, med + 3.0)
                for i, x in enumerate(v):
                    if x is not None and x > lim:
                        v[i], src_[i] = None, "n"
            idx = [i for i, x in enumerate(v) if x is not None]
            whole = None
            if not idx:
                whole = cmed.get(W["h"]) or allmed
                if whole is None:
                    off = None
                    break
            o = []
            for i in range(len(v)):
                if whole is not None:
                    o.append(whole)
                    m["class"] += STREET_STEP / 2.0
                    continue
                m[src_[i]] += STREET_STEP / 2.0
                if v[i] is not None:
                    o.append(v[i])
                    continue
                lo = max([j for j in idx if j < i] or [None], key=lambda j: -1 if j is None else j)
                hi = min([j for j in idx if j > i] or [None], key=lambda j: 10 ** 9 if j is None else j)
                if lo is None:
                    o.append(v[hi])
                elif hi is None:
                    o.append(v[lo])
                else:
                    o.append(v[lo] + (v[hi] - v[lo]) * (i - lo) / float(hi - lo))
            o = [max(STREET_MIN, sorted(o[max(0, i - 1):i + 2])[len(o[max(0, i - 1):i + 2]) // 2]) for i in range(len(o))]
            off.append(o)
        if off is None:
            dropped += 1
            continue
        # half a metre past each end, so that the bands of one street overlap where OSM splits it
        x, y, nx, ny = S[0]
        S = [(x - ny * 0.5, y + nx * 0.5, nx, ny)] + S
        x, y, nx, ny = S[-1]
        S = S + [(x + ny * 0.5, y - nx * 0.5, nx, ny)]
        off = [[o[0]] + o + [o[-1]] for o in off]
        left = [(q[0] + q[2] * d, q[1] + q[3] * d) for q, d in zip(S, off[0])]
        right = [(q[0] - q[2] * d, q[1] - q[3] * d) for q, d in zip(S, off[1])]
        bands.append([True, [[round(p[0], 2), round(p[1], 2)] for p in left + right[::-1]]])
    tot = sum(m.values()) or 1.0
    note = (u"%d street bands, %d footpath lines; band edges: %.0f m on a survey road edge (%.0f %%), %.0f m on a "
            u"building or wall front (%.0f %%), %.0f m carried on between measured stretches (%.0f %%), %.0f m at the "
            u"class median (%.0f %%; medians of the half width, m: %s)" % (
                len(bands), len(paths), m["e"], 100 * m["e"] / tot, m["f"], 100 * m["f"] / tot, m["n"],
                100 * m["n"] / tot, m["class"], 100 * m["class"] / tot,
                u", ".join(u"%s %.1f" % kv for kv in sorted(cmed.items()))))
    if dropped:
        log.append(u"FLAG streets: %d street(s) without any measured width in the frame: not drawn" % dropped)
    layers = {"streets": bands, "paths": paths}
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(STREET_FILE, "w", encoding="utf-8") as f:
        json.dump({"key": key, "note": note, "made_by": u"%s %s" % (GH_LABEL, VERSION),
                   "made_at": time.strftime("%Y-%m-%d %H:%M:%S"), "layers": layers}, f)
    log.append(u"%s  %s (%.1f s): %s" % (STREET_FILE, time.strftime("%H:%M:%S"), time.time() - t0, note))
    return layers




# ================================================================ PDF (vector, layers as PDF layers)
PT = 25.4 / 72.0
_TR = {u"Ğ": 129, u"ğ": 141, u"İ": 143, u"ı": 144, u"Ş": 157, u"ş": 158, u"–": 150, u"—": 151, u"’": 146}
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"
_HELV = {" ": 278, "1": 556, ":": 278, ",": 278, ".": 278, "i": 222, "l": 222, "t": 278, "f": 278, "r": 333, "m": 833,
         "w": 722, "M": 833, "W": 944, "I": 278, "j": 222}


def text_w(s, size, bold=False):
    """mm: Helvetica widths for the narrow and wide letters, 556/1000 em for the rest (labels are short)"""
    return sum(_HELV.get(ch, 667 if ch.isupper() else 556) for ch in s) / 1000.0 * size * (1.05 if bold else 1.0)


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



_LOCKED = []


def _item_layer(it):
    t = it[0]
    return it[6] if t == "poly" else it[5] if t == "line" else it[10] if t in ("mask", "soft") else it[8]


def _item_clip(it):
    t = it[0]
    return it[9] if t == "poly" else it[4] if t == "line" else it[11] if t in ("mask", "soft") else None


def write_pdf(path, w, h, items, title, clips=None):
    """one page w x h mm; items in page mm, y up; each item's layer becomes a PDF layer.
    poly  ("poly", rings, fill, stroke, lw, None, layer, 1, "eo"|None, clip)   fill "~RRGGBB" = with the grain
    line  ("line", pts, stroke, lw, clip, layer, 1)
    text  ("text", s, x, y, size, colour, bold, align, layer, angle, "i"|None)
    mask  ("mask", zlib 1-bit rows, px w, px h, x, y, w mm, h mm, fill, None, layer, clip)   a stencil painted in fill
    clips = {clip id: [rings, rings, ...]}: an item with a clip id is cut to every ring set of that id in turn"""
    objs = []
    clips = clips or {}

    def add(b):
        objs.append(b)
        return len(objs)

    def lay(it):
        return _item_layer(it).split("/")[0]             # "trees/tree_0001" is PDF layer "trees"

    def clip_of(it):
        t = it[0]
        return it[9] if t == "poly" else it[4] if t == "line" else it[11] if t in ("mask", "soft") else None
    layers = []
    for it in items:
        if lay(it) not in layers:
            layers.append(lay(it))
    ocg = dict((ly, add(("<< /Type /OCG /Name (%s) >>" % _pdf_txt(ly).decode("latin-1")).encode("latin-1")))
               for ly in layers)
    f_r = add(("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding << /Type /Encoding /BaseEncoding "
               "/WinAnsiEncoding %s >> >>" % _DIFF).encode())
    f_i = add(("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding << /Type /Encoding "
               "/BaseEncoding /WinAnsiEncoding %s >> >>" % _DIFF).encode())
    f_b = add(("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding << /Type /Encoding /BaseEncoding "
               "/WinAnsiEncoding %s >> >>" % _DIFF).encode())
    k = 72.0 / 25.4
    pats, imgs = {}, {}

    def paint(fill):
        """the operators that set the fill: a flat colour, or the grain pattern of that colour"""
        if not fill.startswith("~") or _GRAIN.get("amp", 0) <= 0 or "z" not in _GRAIN:
            return "%s rg" % _col(fill.lstrip("~")[:6])
        col = fill[1:]
        if col not in pats:
            lv, amp, T = _GRAIN["levels"], _GRAIN["amp"], _GRAIN["tile"]
            ticks = col.split("|")[1].split(",") if "|" in col else None
            if "@" in col:
                amp = float(col.split("|")[0].split("@")[1])
            table = "".join(_mix(col[:6], (2.0 * i / (lv - 1) - 1.0) * amp) for i in range(lv))
            z = _GRAIN["z"]
            im = add(("<< /Type /XObject /Subtype /Image /Width %d /Height %d /ColorSpace [/Indexed /DeviceRGB %d <%s>] "
                      "/BitsPerComponent 8 /Interpolate true /Filter /FlateDecode /Length %d >>\nstream\n" % (
                          _GRAIN["px"], _GRAIN["px"], lv - 1, table, len(z))).encode() + z + b"\nendstream")
            body_ = "q %s 0 0 %s 0 0 cm /G Do Q" % (_f(T), _f(T))
            if ticks:                                    # wave strokes over the grain; whole rows and pitches per tile
                row, tl, pitch, lw_ = [float(v) for v in ticks[:4]]
                nr, nc = max(2, 2 * int(round(T / row / 2.0))), max(1, int(round(T / pitch)))
                row, pitch = T / nr, T / nc
                A = ["q 1 J %s RG %s w" % (_col(ticks[4]), _f(lw_))]
                for j in range(nr):
                    y = (j + 0.5) * row
                    for i in range(nc):
                        x = (i + 0.25 + 0.5 * (j % 2)) * pitch - tl / 2.0
                        A.append("%s %s m %s %s %s %s %s %s c %s %s %s %s %s %s c" % (
                            _f(x), _f(y), _f(x + tl / 6.0), _f(y + tl / 7.0), _f(x + tl / 3.0), _f(y + tl / 7.0),
                            _f(x + tl / 2.0), _f(y), _f(x + tl * 2 / 3.0), _f(y - tl / 7.0), _f(x + tl * 5 / 6.0),
                            _f(y - tl / 7.0), _f(x + tl), _f(y)))
                A.append("S Q")
                body_ += "\n" + "\n".join(A)
            body_ = zlib.compress(body_.encode(), 6)
            pats[col] = add(("<< /Type /Pattern /PatternType 1 /PaintType 1 /TilingType 2 /BBox [0 0 %s %s] /XStep %s "
                             "/YStep %s /Matrix [%s 0 0 %s 0 0] /Resources << /XObject << /G %d 0 R >> >> /Filter /FlateDecode /Length %d >>\n"
                             "stream\n" % (_f(T), _f(T), _f(T), _f(T), _f(k), _f(k), im, len(body_))).encode()
                            + body_ + b"\nendstream")
        return "/Pattern cs /P%d scn" % pats[col]

    def ring_path(rings):
        A = []
        for r in rings:
            A.append("%s %s m" % (_f(r[0][0]), _f(r[0][1])))
            A += ["%s %s l" % (_f(p[0]), _f(p[1])) for p in r[1:]]
            A.append("h")
        return A
    body = bytearray(("%s 0 0 %s 0 0 cm\n1 J 1 j\n" % (_f(k), _f(k))).encode())
    for ly in layers:                                    # one marked block per layer, in first-use order
        body += ("/OC /oc%d BDC\n" % ocg[ly]).encode()
        cur = None
        for it in items:
            if lay(it) != ly:
                continue
            t = it[0]
            cid = clip_of(it)
            if cid not in clips:
                cid = None
            if cid != cur:                               # the clip stays open for a run of items with the same id
                if cur is not None:
                    body += b"Q\n"
                if cid is not None:
                    A = ["q"]
                    for rs in clips[cid]:
                        A += ring_path(rs) + ["W* n"]
                    body += ("\n".join(A) + "\n").encode()
                cur = cid
            if t == "poly":
                rings, fill, stroke, lw = it[1:5]
                if not fill and not stroke:
                    continue
                A = ["q"] + ring_path(rings)
                if fill:
                    A.append(paint(fill))
                if stroke:
                    A.append("%s RG %s w" % (_col(stroke), _f(lw or 0.1)))
                eo = "*" if it[8] == "eo" else ""
                A.append("B" + eo if (fill and stroke) else "f" + eo if fill else "S")
                A.append("Q")
                body += ("\n".join(A) + "\n").encode()
            elif t == "line":
                pts, stroke, lw = it[1:4]
                A = ["q %s RG %s w" % (_col(stroke), _f(lw or 0.1)), "%s %s m" % (_f(pts[0][0]), _f(pts[0][1]))]
                A += ["%s %s l" % (_f(p[0]), _f(p[1])) for p in pts[1:]]
                A.append("S Q")
                body += ("\n".join(A) + "\n").encode()
            elif t == "mask":
                z, pw, ph, x, y, mw, mh, fill = it[1:9]
                im = add(("<< /Type /XObject /Subtype /Image /Width %d /Height %d /ImageMask true /BitsPerComponent 1 "
                          "/Decode [1 0] /Filter /FlateDecode /Length %d >>\nstream\n" % (pw, ph, len(z))).encode()
                         + z + b"\nendstream")
                imgs[im] = 1
                body += ("q %s %s 0 0 %s %s %s cm /I%d Do Q\n" % (paint(fill), _f(mw), _f(mh), _f(x), _f(y), im)).encode()
            elif t == "soft":                            # a flat colour through an 8-bit soft mask (fades out)
                z, pw, ph, x, y, mw, mh, colour = it[1:9]
                sm = add(("<< /Type /XObject /Subtype /Image /Width %d /Height %d /ColorSpace /DeviceGray "
                          "/BitsPerComponent 8 /Interpolate true /Filter /FlateDecode /Length %d >>\nstream\n" % (
                              pw, ph, len(z))).encode() + z + b"\nendstream")
                zz = zlib.compress(b"\x00" * (((pw + 7) // 8) * ph), 9)
                im = add(("<< /Type /XObject /Subtype /Image /Width %d /Height %d /ColorSpace [/Indexed /DeviceRGB 0 <%s>] "
                          "/BitsPerComponent 1 /Interpolate true /SMask %d 0 R /Filter /FlateDecode /Length %d >>\nstream\n"
                          % (pw, ph, colour, sm, len(zz))).encode() + zz + b"\nendstream")
                imgs[im] = 1
                body += ("q %s 0 0 %s %s %s cm /I%d Do Q\n" % (_f(mw), _f(mh), _f(x), _f(y), im)).encode()
            elif t == "text":
                s, x, y, size, color, bold, align = it[1:8]
                wmm = text_w(s, size, bold)
                xx = x - {"L": 0.0, "C": wmm / 2.0, "R": wmm}.get(align, 0.0)
                ang = math.radians(it[9]) if isinstance(it[9], (int, float)) else 0.0
                ca, sa = math.cos(ang), math.sin(ang)
                if ang:
                    xx = x
                body += ("BT /%s %s Tf %s rg %s %s %s %s %s %s Tm (" % (
                    "F2" if bold else "F3" if it[10] == "i" else "F1", _f(size / PT), _col(color), _f(PT * ca), _f(PT * sa), _f(-PT * sa),
                    _f(PT * ca), _f(xx), _f(y))).encode()
                body += _pdf_txt(s) + b") Tj ET\n"
        if cur is not None:
            body += b"Q\n"
        body += b"EMC\n"
    zb = zlib.compress(bytes(body), 6)
    cid = add(b"<< /Filter /FlateDecode /Length %d >>\nstream\n" % len(zb) + zb + b"\nendstream")
    props = " ".join("/oc%d %d 0 R" % (i, i) for i in ocg.values())
    res = add(("<< /Font << /F1 %d 0 R /F2 %d 0 R /F3 %d 0 R >> /Properties << %s >> /Pattern << %s >> /XObject << %s >> "
               ">>" % (f_r, f_b, f_i, props, " ".join("/P%d %d 0 R" % (i, i) for i in pats.values()),
                       " ".join("/I%d %d 0 R" % (i, i) for i in imgs))).encode())
    pages_id = len(objs) + 2
    page = add(("<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %s %s] /Contents %d 0 R /Resources %d 0 R >>" % (
        pages_id, _f(w / PT), _f(h / PT), cid, res)).encode())
    assert add(("<< /Type /Pages /Kids [%d 0 R] /Count 1 >>" % page).encode()) == pages_id
    oc = " ".join("%d 0 R" % i for i in ocg.values())
    cat = add(("<< /Type /Catalog /Pages %d 0 R /OCProperties << /OCGs [%s] /D << /Order [%s] /ON [%s] >> >> >>" % (
        pages_id, oc, oc, oc)).encode())
    info = add(b"<< /Title (" + _pdf_txt(title) + b") /Producer (Bergama drawing set) >>")
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
    except PermissionError:                              # open in a viewer: a timed name
        _LOCKED.append(os.path.basename(path))
        path = path[:-4] + time.strftime("_%H%M%S") + ".pdf"
        with open(path, "wb") as f:
            f.write(bytes(out))
    return path


def out_line(p, w, h, den, items, extra=u""):
    """the log line of one output: its size and how many objects it draws"""
    if _LOCKED:
        extra += u"; %s was open in a viewer, so this timed copy was written: close the viewer to get the plain name" % _LOCKED.pop()
    return u"%s  %s (%.0f x %.0f mm, 1:%s; %.1f MB, %s drawn objects%s)" % (
        p, time.strftime("%H:%M:%S"), w, h, format(den, ",d"), os.path.getsize(p) / 1048576.0, format(len(items), ",d"),
        extra)


def _png_rgba(z, pw, ph, colour):
    """an 8-bit coverage image (zlib rows, top row first) as a PNG of one colour with that coverage as its alpha"""
    raw = zlib.decompress(z)
    line = bytearray(4 * pw)
    for i in range(3):
        line[i::4] = bytes([int(colour[2 * i:2 * i + 2], 16)]) * pw
    out = bytearray()
    for j in range(ph):
        line[3::4] = raw[j * pw:(j + 1) * pw]
        out += b"\x00" + line

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", pw, ph, 8, 6, 0, 0, 0)) +
            chunk(b"IDAT", zlib.compress(bytes(out), 6)) + chunk(b"IEND", b""))


def _xml(t):
    return (u"%s" % t).replace(u"&", u"&amp;").replace(u"<", u"&lt;").replace(u">", u"&gt;").replace(u'"', u"&quot;")


def write_svg(path, w, h, items, title, clips=None):
    """the same items as write_pdf, as an SVG for editing: one named group per layer, in the PDF's order; a layer name
    "a/b" becomes group b inside group a (every tree its own group inside the trees group). Fills are flat colours
    here (the grain lives in the PDF, the print file); a soft tone is an embedded PNG with its own transparency."""
    clips = clips or {}

    def d_of(rings):
        return u" ".join(u"M" + u" L".join(u"%.2f %.2f" % (q[0], h - q[1]) for q in R) + u" Z" for R in rings if R)
    A = [u'<?xml version="1.0" encoding="UTF-8"?>',
         u'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%.2fmm" '
         u'height="%.2fmm" viewBox="0 0 %.2f %.2f">' % (w, h, w, h), u"<title>%s</title>" % _xml(title), u"<defs>"]
    cnum = {}
    for cid in clips:
        cnum[cid] = len(cnum)
        for i, rs in enumerate(clips[cid]):
            A.append(u'<clipPath id="clip%d_%d"><path clip-rule="evenodd" d="%s"/></clipPath>' % (cnum[cid], i, d_of(rs)))
    A.append(u"</defs>")
    layers = []
    for it in items:
        ly = _item_layer(it).split("/")[0]
        if ly not in layers:
            layers.append(ly)
    for ly in layers:
        A.append(u'<g id="%s">' % _xml(ly))
        cur, sub, depth = None, None, 0
        for it in items:
            full = _item_layer(it)
            if full.split("/")[0] != ly:
                continue
            t = it[0]
            cid = _item_clip(it)
            if cid not in clips:
                cid = None
            sb = full.split("/", 1)[1] if "/" in full else None
            if cid != cur or sb != sub:
                if sub is not None:
                    A.append(u"</g>")
                    sub = None
                if cid != cur:
                    A.append(u"</g>" * depth)
                    depth = 0
                    if cid is not None:
                        depth = len(clips[cid])
                        A.append(u"".join(u'<g clip-path="url(#clip%d_%d)">' % (cnum[cid], i) for i in range(depth)))
                    cur = cid
                if sb is not None:
                    A.append(u'<g id="%s">' % _xml(sb))
                    sub = sb
            if t == "poly":
                rings, fill, stroke, lw = it[1:5]
                if not fill and not stroke:
                    continue
                A.append(u'<path d="%s" fill="%s"%s%s/>' % (
                    d_of(rings), (u"#" + fill.lstrip("~")[:6]) if fill else u"none",
                    u' fill-rule="evenodd"' if it[8] == "eo" else u"",
                    (u' stroke="#%s" stroke-width="%.3f" stroke-linejoin="round"' % (stroke, lw or 0.1)) if stroke else u""))
            elif t == "line":
                pts, stroke, lw = it[1:4]
                A.append(u'<polyline points="%s" fill="none" stroke="#%s" stroke-width="%.3f" stroke-linecap="round" '
                         u'stroke-linejoin="round"/>' % (u" ".join(u"%.2f,%.2f" % (q[0], h - q[1]) for q in pts), stroke,
                                                         lw or 0.1))
            elif t == "soft":
                z, pw, ph, x, y, mw, mh, colour = it[1:9]
                A.append(u'<image x="%.2f" y="%.2f" width="%.2f" height="%.2f" preserveAspectRatio="none" '
                         u'xlink:href="data:image/png;base64,%s"/>' % (
                             x, h - y - mh, mw, mh, base64.b64encode(_png_rgba(z, pw, ph, colour)).decode("ascii")))
            elif t == "text":
                s_, x, y, size, color, bold, align = it[1:8]
                ang = it[9] if isinstance(it[9], (int, float)) else 0.0
                A.append(u'<text x="%.2f" y="%.2f" font-family="Helvetica, Arial, sans-serif" font-size="%.3f" fill="#%s"'
                         u'%s%s text-anchor="%s"%s>%s</text>' % (
                             x, h - y, size, color, u' font-weight="bold"' if bold else u"",
                             u' font-style="italic"' if it[10] == "i" else u"",
                             u"start" if ang else {"C": u"middle", "R": u"end"}.get(align, u"start"),
                             (u' transform="rotate(%.3f %.2f %.2f)"' % (-ang, x, h - y)) if ang else u"", _xml(s_)))
        if sub is not None:
            A.append(u"</g>")
        A.append(u"</g>" * depth)
        A.append(u"</g>")
    A.append(u"</svg>")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = u"\n".join(a for a in A if a).encode("utf-8")
    try:
        with open(path, "wb") as f:
            f.write(data)
    except PermissionError:                              # open in another program: a timed name
        path = path[:-4] + time.strftime("_%H%M%S") + ".svg"
        with open(path, "wb") as f:
            f.write(data)
    return path


def plan_frame(txt, F):
    """the plan frame in his SVG (x, y, w, h units): the frame-shaped clip rectangle his Selinos group uses, else the
    commonest clip rectangle of the frame's proportions"""
    rects = {}
    for m in re.finditer(r'<clipPath id="([^"]+)">\s*<rect([^>]*)>', txt):
        a = dict(re.findall(r'([\w:-]+)="([^"]*)"', m.group(2)))
        try:
            r = (float(a.get("x", 0)), float(a.get("y", 0)), float(a["width"]), float(a["height"]))
        except Exception:
            continue
        if r[3] > 0 and abs(r[2] / r[3] - F.w / F.h) / (F.w / F.h) < 0.01 and "transform" not in a:
            rects[m.group(1)] = r
    if not rects:
        return None, u"no clip rectangle of the frame's proportions"
    i = txt.find('id="Selinos"')
    if i >= 0:
        for cid in re.findall(r'clip-path="url\(#([^)]+)\)"', txt[i:i + 600]):
            if cid in rects:
                return rects[cid], u"the Selinos group's frame clip %s" % cid
    cnt = {}
    for r in rects.values():
        cnt[r] = cnt.get(r, 0) + 1
    return max(cnt, key=cnt.get), u"the commonest frame-shaped clip rectangle (no Selinos group clip found)"


_TOK = re.compile(r"([MmLlHhVvCcSsQqTtAaZz])|([-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)")
_N = {"m": 2, "l": 2, "h": 1, "v": 1, "c": 6, "s": 4, "q": 4, "t": 2, "a": 7, "z": 0}


def path_rings(d, step=1.5):
    """an SVG path as [(closed?, [(x, y)])], curves cut into pieces of about step units (arcs as chords)"""
    out, cur, cmd = [], [], None
    x = y = sx = sy = 0.0
    px = py = None                                        # the last control point (for S and T)

    def bez(P):
        n = max(2, int(sum(math.hypot(P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1]) for i in range(len(P) - 1)) / step))
        for k in range(1, n + 1):
            t = k / float(n)
            Q = list(P)
            while len(Q) > 1:
                Q = [(Q[i][0] + (Q[i + 1][0] - Q[i][0]) * t, Q[i][1] + (Q[i + 1][1] - Q[i][1]) * t) for i in range(len(Q) - 1)]
            cur.append(Q[0])

    def flush(closed):
        if len(cur) >= 2:
            out.append((closed, list(cur)))
        del cur[:]
    toks = _TOK.findall(d)
    i = 0
    while i < len(toks):
        if toks[i][0]:
            cmd = toks[i][0]
            i += 1
            if cmd in "Zz":
                flush(True)
                x, y = sx, sy
                px = py = None
                continue
        if cmd is None:
            break
        n = _N[cmd.lower()]
        a = []
        while len(a) < n and i < len(toks) and not toks[i][0]:
            a.append(float(toks[i][1]))
            i += 1
        if len(a) < n:
            if i < len(toks) and toks[i][0]:
                continue
            break
        rel = cmd.islower()
        c = cmd.lower()
        ox, oy = (x, y) if rel else (0.0, 0.0)
        if c == "m":
            flush(False)
            x, y = ox + a[0], oy + a[1]
            sx, sy = x, y
            cur.append((x, y))
            cmd = "l" if rel else "L"
            px = py = None
        elif c == "l":
            x, y = ox + a[0], oy + a[1]
            cur.append((x, y))
            px = py = None
        elif c == "h":
            x = (x if rel else 0.0) + a[0]
            cur.append((x, y))
            px = py = None
        elif c == "v":
            y = (y if rel else 0.0) + a[0]
            cur.append((x, y))
            px = py = None
        elif c in "cs":
            if c == "c":
                p1 = (ox + a[0], oy + a[1])
                p2, p3 = (ox + a[2], oy + a[3]), (ox + a[4], oy + a[5])
            else:
                p1 = (2 * x - px, 2 * y - py) if px is not None else (x, y)
                p2, p3 = (ox + a[0], oy + a[1]), (ox + a[2], oy + a[3])
            if not cur:
                cur.append((x, y))
            bez([(x, y), p1, p2, p3])
            px, py = p2
            x, y = p3
        elif c in "qt":
            if c == "q":
                p1, p2 = (ox + a[0], oy + a[1]), (ox + a[2], oy + a[3])
            else:
                p1 = (2 * x - px, 2 * y - py) if px is not None else (x, y)
                p2 = (ox + a[0], oy + a[1])
            if not cur:
                cur.append((x, y))
            bez([(x, y), p1, p2])
            px, py = p1
            x, y = p2
        elif c == "a":
            x, y = ox + a[5], oy + a[6]
            cur.append((x, y))
            px = py = None
    flush(False)
    return out


def _group_span(body, gid):
    """(start, end) of <g id="gid"> ... its closing tag, or None"""
    m = re.search(r'<g\b[^>]*\bid="%s"[^>]*>' % re.escape(gid), body)
    if not m:
        return None
    d = 0
    for k in re.finditer(r'<g\b[^>]*?(/?)>|</g>', body[m.start():]):
        t = k.group(0)
        if t.startswith("</g"):
            d -= 1
        elif not t.endswith("/>"):
            d += 1
        if d == 0:
            return m.start(), m.start() + k.end()
    return None


def _hex6(c):
    c = (c or "").strip().lstrip("#")
    if len(c) == 3:
        c = u"".join(ch * 2 for ch in c)
    return c.upper() if re.match(r"^[0-9a-fA-F]{6}$", c) else None



# ================================================================ main
def load_or_read(log):
    import Rhino
    doc = Rhino.RhinoDoc.ActiveDoc
    key = model_key(doc)
    if key and os.path.isfile(CACHE_FILE):
        try:
            with open(CACHE_FILE, encoding="utf-8") as f:
                D = json.load(f)
            if D.get("key") == key:
                log.append(u"same model as the cache: %s used, the model not read again" % CACHE_FILE)
                return D
        except Exception:
            pass
    t0 = time.time()
    D = read_model(doc, log)
    D["key"] = key
    D["made_by"] = u"%s %s" % (GH_LABEL, VERSION)
    D["made_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    D["what"] = (u"survey layers of the open model in survey m, uncut; frame = site_alan corners; draw with the frame "
                 u"turned flat (long side horizontal, eastern end right)")
    for k_, L in D["layers"].items():
        D["layers"][k_] = [[bool(cl), [[round(p[0], 2), round(p[1], 2)] for p in P]] for cl, P in L]
    D["frame"] = [[round(p[0], 3), round(p[1], 3)] for p in D["frame"]]
    D["calisma"] = [[[round(p[0], 3), round(p[1], 3)] for p in P] for P in D.get("calisma", [])]
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(D, f, ensure_ascii=False)
    log.append(u"%s  %s (model read in %.1f s)" % (CACHE_FILE, time.strftime("%H:%M:%S"), time.time() - t0))
    return D


def main():
    t0 = time.time()
    log = []
    den = int(globals().get("scale") or 2000)
    kden = int(globals().get("keymap_scale") or 10000)
    S = load_style()
    set_grain(S, log)
    log.append(u"style: %s, %d categories (%s)" % (S["version"], len(S["cat"]), os.path.join(BERGAMA_ROOT, STYLE_FILE)))
    D = load_or_read(log)
    F = Frame([tuple(p) for p in D["frame"]])
    D["turn_deg"] = round(math.degrees(F.rot), 4)
    D["layers"].update(load_veg(D, log))
    D["layers"].update(build_streets(D, F, log))
    L = localise(D, F)
    prepare(D, L, F, log)
    fade = Fade(D, F)
    if fade.rows is not None:
        log.append(u"fade: context lines full within %.0f m of calisma_alan (%.0f %% of the frame), lighter beyond" % (
            FADE_M, 100.0 * fade.share))
    log.append(u"frame: site_alan %.2f x %.2f m, turned %.2f deg; north on the page points (%.3f, %.3f)" % (
        F.w, F.h, math.degrees(F.rot), F.north()[0], F.north()[1]))
    load_sections(D, log)
    cover = Cover(L, F, log) if (L.get("sat_trees") or L.get("sat_grass")) else None
    n_a0 = a0_scale(F)
    log.append(u"A0: the whole frame in one piece at 1:%s (the smallest step of %d at which %.0f m fits %.0f mm wide)"
               % (format(n_a0, ",d"), A0_STEP, F.w, A0_W - 2 * A0_MARGIN))
    order = ["tree_cover"] + [c for _, c, _ in CONTEXT][::-1] + ["calisma", "section_line"]
    for name, d0, key, title in ((u"Basemap", den, False, u"Base map"), (u"Keymap", kden, True, u"Key map")):
        for a0 in (False, True):
            d = n_a0 if a0 else d0

            def band(den_, x, y, u0, u1, tag, key=key):
                items, cnt = draw_context(L, F, S, den_, x, y, u0, u1, lw_k=0.6 if (key and den_ > 4000) else 1.0,
                                          cover=None if key else cover, fade=fade, skip=KEY_SKIP if key else ())
                items += draw_top(D, F, S, den_, x, y, u0, u1, names=not key, sections=key,
                                  lw_k=0.6 if (key and den_ > 4000) else 1.0)
                cnt["calisma"] = len(D.get("calisma", []))
                if key and D.get("sections"):
                    cnt["section_line"] = len(D["sections"])
                return items, {}, cnt
            w, h, items, clips, cnt = sheet(F, S, d, a0, title, u"Existing situation, 1:%s" % format(d, ",d"),
                                            lambda c: [k_ for k_ in order[::-1] if c.get(k_)][::-1],
                                            None if key else CREDIT, band)
            p = write_pdf(os.path.join(OUT_DIR, name + (u"_A0.pdf" if a0 else u".pdf")), w, h, items,
                          u"%s, site_alan, 1:%d" % (name, d), clips)
            log.append(out_line(p, w, h, d, items, u"" if a0 else u"; " + u", ".join(
                u"%s %d" % kv for kv in sorted(cnt.items()))))
    flags = [l for l in log if l.startswith(u"FLAG")]
    return u"%s\n%s %s, %d FLAG line(s), %.1f s" % (u"\n".join(log), GH_LABEL, VERSION, len(flags), time.time() - t0)


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

