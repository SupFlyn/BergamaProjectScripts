# -*- coding: utf-8 -*-
"""Bergama Group 6: BASEMAP v3.3 (12 Nov 2026). Rules: scripts/_template/SCRIPT_STANDARD.md.
Aras 12 Nov 2026 10:53 UTC: "we need a fresh basemap and keymap style. For basemap every road should be outlined as well
as the buildings and all should be outlined aswell. Heritage buildings should be marked. Our site_alan should be our
frame for that basemap and keymap for that matter".

ONE read of the open survey model (Bergama_Altlik.3dm), cut at site_alan, turned so the frame's long side lies flat
(its eastern end to the right, as his plan), kept by layer in a cache that the other new scripts copy from:
  Basemap.pdf   outline drawing at 1:scale: every building, road edge, kerb, bridge, stream bank, pond, park, wall and
                shed as its own outline; heritage buildings marked (filled in the palette red, heavier outline);
                frame = site_alan, north arrow, scale bar, legend of what is drawn
  Keymap.pdf    the key map style at 1:keymap_scale: buildings as light solid blocks, heritage solid red, road edges
                faint, stream banks blue, the frame; section lines of the model layer "section_lines" with their names
  heritage      a building is heritage when it is on BINA_TARIHI / BINA_HARABE, or a survey name text (YAZI_YAPI) with a
                heritage or sacred word (HERITAGE_WORDS, the site board's list) stands inside it; walls on
                SINIR_TARIHI_SUR are drawn in the heritage colour. Nothing else decides it; the log lists them by name.
Aras 10:54 UTC: "we need to see our calisma_alan, and inside calisma_alan it'll be colourful just as the published svg
and outside it should be black and white".
  Basemap.pdf / Keymap.pdf are grey on white outside calisma_alan (see 11:11 below for the look).
  Basemap_colour.svg = his plan SVG (Data/assets/masterlastversion.svg, unchanged, nothing redrawn) shown only inside
                calisma_alan (a clip path) and outside the plan frame (his legend and texts), over the black and white
                survey outlines, which therefore show everywhere else in the frame. Placed by the plan frame = site_alan
                (the frame-size clip rectangle of his Selinos group). Groups: existing_basemap_bw/<layer>,
                plan_inside_calisma_alan, calisma_alan_outline. Open it in Illustrator.
Aras 11:11 UTC: his example for the look = the Viinikanlahti general plan (Arkkitehtuurikilpailuja 5/2020, p. 8): the
context is white buildings with thin grey outlines and a soft grey shadow, white streets with thin grey edges, small
grey street and place names, key buildings red, the project boundary a thin red line, colour only inside it. So here:
thin grey outlines, the survey's street names (YAZI_CADDE_YOL) and building names (YAZI_YAPI) in small grey text at their survey place and
turn, heritage buildings solid palette red, calisma_alan a thin red line.
Aras 11:13 UTC: "use sattalite imagery and dwg combined together however everything should be outlined and hatched
accordingly (solid white or whatever it is)"; "dont add shadows to the basemap for now".
  Under the survey lines: the land cover traced from the 2023 satellite image (Data/veg2023.json: Esri World Imagery,
  Maxar capture 1 Mar 2023, classified by colour rules, its limits in that file): tree cover outlined with a light
  fill, low green outlined with a line hatch, open ground outlined and solid white. The image stops at VEG_BOX; the
  log says what share of the frame it covers. No shadows (SHADOWS = False; the code stays for later).
Aras 11:15 UTC: "if a road starts somewhere i dont want it to disappear along the road ... it should be consistent".
  The survey draws a road edge (YOL_SOSE / YOL_BORDUR / YOL_TOPRAK) only along part of the streets; in the old town
  the street is the gap between the houses. So every street is drawn as ONE continuous white band with a thin grey
  edge along its whole OpenStreetMap centreline (Data/bergama_osm.osm): every STREET_STEP m its edge on each side is
  the nearest survey road edge (within EDGE_MAX m) or building / wall front (within FRONT_MAX m); where the survey
  shows neither, the width runs on from the measured stretches of the same street (straight line between them), and
  a street with no measured point at all takes the median of its class in the frame. The log gives the metres of
  each kind. Footpaths (PATH_CLASSES) are one thin line along their whole length. The survey's own road edges and
  kerbs are still drawn on top, unchanged. Cached in streets.json.
Line weights, the grey tones, the hatch and EDGE_MAX / FRONT_MAX / STREET_STEP are drawing values (ours).
v2, Aras 12 Nov 17:07-17:26 UTC (thread "Inspect reference drawings and merge best parts", brief
library/examples/liked_2026-11-12/MERGED_SPEC_v0.1.md, a draft): "Masterplan is our first goal"; "we want the base map
first"; routes and connections "leave that to last ... those are the lines that we can put on the base map"; the thin
red line stays, "outside of that line will be white and inside is colourful"; the pale green under the tree groups:
"yes we do want that"; "lighter more soft colours generally", his palette follows. So:
  COLOURS  every colour sits in the block "COLOURS" below, one line per meaning: his palette is swapped in there.
  FADE     the context lines have two tones: full within FADE_M m of calisma_alan, lighter (FADE_MIX towards white)
           beyond, so the sheet corners are nearly white. Heritage, the stream and the red line keep their tone.
  CORNER   north circle, the scale as text and a segmented scale bar sit inside the frame's lower right corner.
  NAMES    street names in italic along the street (their survey turn), place names upright.
  Basemap_colour.svg: the route groups of his plan (BASE_OFF) are switched off (display none; they stay in the file
           and are switched on again in the Illustrator layer panel), and under his trees lies the planted-ground
           underlay: three flat pale green rings around every tree symbol of his plan (UNDERLAY_M m beyond the crown),
           no outline, drawn only where his plan has a tree, inside calisma_alan only.
FADE_M, FADE_MIX, UNDERLAY_M and the underlay tints are drawing values (ours), not his.
v2.1, Aras 12 Nov 17:46 UTC: five liked palettes (library/examples/palettes_2026-11-12/), the favourite the chart
"Dusty Rose / Mauve / Sage Green / Taupe / Ivory / Terracotta / Deep Wine": "feel free to combine them according to the
colour science". PALETTE below = ten colours, one per meaning, each sampled from one of his images (the median of a
patch of the swatch) or, where marked, lightened from a sampled colour. Every other tone is a tint of these.
v3, Aras 12 Nov 18:40 UTC: "water, hardground should get textures. Like hardground should get a textures (the promanade
that we propose)". In Basemap_colour.svg two textures are laid on his plan as real vector lines (no pattern fills),
each directly above the shape it belongs to, cut to that shape, in a tone of that shape's own fill:
  water      every filled path of his group "Selinos": short wave ticks in rows WATER_ROW m apart, a tick WATER_TICK m
             long every WATER_PITCH m, each second row shifted by half; the rows run along the frame's long side (the
             general flow), they do not turn with each bend
  promenade  the paths of his group "walks_paths_bike_lane" whose fill is in PROMENADE_FILLS (the pale rose band, read
             as his riverside walk: not confirmed by him): joint lines JOINT_M m apart across the frame's long side
His shapes and colours are not changed. The spacings are graphic values (ours), not a paving design.
v3.1, Aras 12 Nov 18:52 UTC: "also create the pdf's scaled into A0". Next to each PDF a second one on an A0 landscape
page (1189 x 841 mm): Basemap_A0.pdf, Keymap_A0.pdf. Its scale 1:N is the smallest N in steps of A0_STEP at which the
frame fits inside the A0_MARGIN mm margin (calculated in the run, written in the log, on the sheet and in its scale
bar); the map is drawn again at that scale (same line weights and text sizes in mm), centred on the page.
v3.2 (fix, first Rhino run 12 Nov 18:55 UTC: "buildings 2, heritage 0"): the survey draws its buildings as single
straight lines (79,213 separate lines on BINA_MESKEN alone, counted in Bergama_Altlik.3dm), not as closed outlines,
and v1-v3.1 kept only curves of three points or more. Now every building line is kept: the lines are joined at their
shared end points (to 1 cm) and every closed cell they form between FACE_MIN and FACE_MAX m2 becomes one building
outline (white, or heritage); lines that close no cell are drawn as lines. A cell is heritage when at least half of
its sides lie on BINA_TARIHI / BINA_HARABE or a heritage name text stands inside it. A yard fully enclosed by building
lines also counts as a cell (the survey does not tell them apart); it only gets the white fill.
v3.3: the survey's floor counts (number texts on YAZI_KAT_ADEDI) are read and kept in the cache next to the outlines
("floors": one number per closed outline of "buildings" and of "heritage", 0 = no floor text inside; the largest
when several stand inside), so that Sections draws its background buildings from this cache alone.

Component: Rhino 8 > Grasshopper > Python 3 Script (the board builder places it from the cloud kit).
  input  run            Button (or the previous script's done text)
  input  scale          sheet scale 1:n of Basemap.pdf (default 2000)
  input  keymap_scale   sheet scale 1:n of Keymap.pdf (default 10000)
  output log / done     as every Bergama script
Reads  the open Rhino model's survey layers (once; the same model = the cache is used, nothing read again)
       ~/Downloads/Bergama/Data/veg2023.json      (satellite land cover; without it the map is drawn without, FLAG)
       ~/Downloads/Bergama/Data/bergama_osm.osm   (street centrelines; without it only the survey edges, FLAG)
       ~/Downloads/Bergama/Data/assets/masterlastversion.svg (his plan, for Basemap_colour.svg)
Writes ~/Downloads/Bergama/output/bergama_basemap/Basemap.pdf, Keymap.pdf   (PDF layers existing_<thing>)
       ~/Downloads/Bergama/output/bergama_basemap/Basemap_A0.pdf, Keymap_A0.pdf   (A0 landscape, scale in the log)
       ~/Downloads/Bergama/output/bergama_basemap/Basemap_colour.svg
       ~/Downloads/Bergama/cached/bergama_basemap/basemap_layers.json   every layer in survey m, the frame, the turn
       ~/Downloads/Bergama/cached/bergama_basemap/streets.json          the street bands and footpaths in survey m
       ~/Downloads/Bergama/logs/bergama_basemap_log.txt
"""
import os, time, json, math, re
import xml.etree.ElementTree as ET

# ---- SETTINGS ----
VERSION = "v3.3"
GH_LABEL = "Basemap"
OUT_FOLDER = "bergama_basemap"
LOG_NAME = "bergama_basemap_log.txt"
GH_INPUTS = {"scale": "int 500..10000 = 2000", "keymap_scale": "int 2000..50000 = 10000"}

FRAME_LAYER = "site_alan"
FRAME_COPY = [(29388.015, 32540.503), (31220.325, 30364.153), (31625.069, 30704.915), (29792.759, 32881.264)]
SECTION_LAYER = "section_lines"
WORK_LAYER = "calisma_alan"
PLAN_SVG = os.path.join("Data", "assets", "masterlastversion.svg")
BLD_LAYERS = ["BINA_MESKEN", "BINA", "BINA_RESMI", "BINA_OKUL", "BINA_DINI_TESIS", "BINA_DINITESIS", "BINA_TARIHI",
              "BINA_HARABE", "BINA_FABRIKA", "BINA_SERA", "BINA_SPOR_TESISLERI", "BINA_AKARYAKIT", "BINA_INS_HALINDE"]
HER_LAYERS = ("BINA_TARIHI", "BINA_HARABE")
NAME_LAYER = "YAZI_YAPI"
FLOOR_LAYER = "YAZI_KAT_ADEDI"
STREET_NAME_LAYER = "YAZI_CADDE_YOL"
SHADOWS = False              # Aras 12 Nov 11:13 UTC: no shadows on the basemap for now
SHADOW_M = (2.5, -2.5)       # m on the turned frame: the shadow copy lies to the lower right
NAME_MM = 1.5                # text height of the names in mm at the sheet scale
HERITAGE_WORDS = ("tarihi", "harabe", "harap", "kalıntı", "kalinti", "hamam", " han ", "bedesten", "arasta", "türbe",
                  "turbe", "medrese", "kızıl avlu", "kizil avlu", "tapınağı", "tapinagi", "kilise", "sinagog", "çeşme",
                  "cesme", "sebil", "kervansaray", "müze", "muze", "cami", "mescit", "mescid", "cemevi", "tekke", "zaviye")
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
HATCH_GEOM = {"sat_grass": (3.0, 45.0, 0.05)}        # spacing m on the ground, angle deg, line mm
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
FADE_M, FADE_MIX = 100.0, 0.5      # m from calisma_alan where the context lines turn lighter; how far towards white
FADE_KEYS = ("parks", "paths", "streets", "road_edges", "kerbs", "bridges", "walls", "sheds", "buildings")
BASE_OFF = ("CIRCULATION", "heritage_trail")     # groups of his plan switched off in the base map (routes come later)
TREE_SYMBOL = "sym_"               # his tree symbols: <use xlink:href="#sym_...">
UNDERLAY_M = (6.0, 4.0, 2.0)       # m beyond the crown: the three rings, widest first
WATER_GROUP, WATER_ROW, WATER_TICK, WATER_PITCH = "Selinos", 5.0, 6.0, 16.0     # m
PROMENADE_GROUP, PROMENADE_FILLS, JOINT_M = "walks_paths_bike_lane", ("#e8cfcf",), 2.0
A0_W, A0_H, A0_MARGIN, A0_STEP = 1189.0, 841.0, 15.0, 500     # mm, mm, mm, scale step
TEXTURE_W = 0.18                   # m on the ground: line width of both textures
# ================= COLOURS: one line per meaning; a new palette is swapped in here =================
def _tint(col, t):
    """col mixed t (0..1) towards white"""
    return u"".join(u"%02X" % int(round(int(col[i:i + 2], 16) + (255 - int(col[i:i + 2], 16)) * t)) for i in (0, 2, 4))


PALETTE = {
    "water": "5F7380",        # stream fill: his image 5 frame 294455, 25 % lighter (calculated)
    "water_edge": "A9B4BB",   # wet edge, first step: the same 294455, 60 % lighter (calculated)
    "water_pale": "E0ECE6",   # wet edge, palest step: image 4, swatch 2
    "tree_dark": "446455",    # image 4, swatch 8
    "tree_mid": "8B8E79",     # image 1 (favourite), Sage Green
    "tree_light": "A8B59E",   # image 3, the light green; also soft ground
    "hard_ground": "EBD6C4",  # image 1, the palest Taupe
    "heritage": "A35F60",     # image 1, Mauve; also the calisma_alan line
    "accent": "C46441",       # image 1, Terracotta: main route, new buildings (not used on the base map yet)
    "context": "A08B8A",      # image 5, swatch 4: context lines and names
}
INK = "3A3A38"                                       # frame, title, scale bar (not from his palettes)
GREY, PALE = PALETTE["context"], _tint(PALETTE["context"], 0.4)      # context lines; the faintest context lines
NAME_GREY = PALETTE["context"]
UNDERLAY = tuple(_tint(PALETTE["tree_light"], t) for t in (0.8, 0.65, 0.5))   # under his trees, widest ring first
HER = HER_FILL = PALETTE["heritage"]
WATER, PARK = PALETTE["context"], _tint(PALETTE["context"], 0.25)    # survey water and park lines stay grey (context)
SAT_TREE = _tint(PALETTE["context"], 0.82)           # satellite tree cover outside his plan: a pale grey fill
SHADOW = _tint(PALETTE["context"], 0.6)
HATCH = dict((k_, (v[0], v[1], _tint(PALETTE["context"], 0.5), v[2])) for k_, v in HATCH_GEOM.items())
# Basemap.pdf: cache layer -> (PDF layer, stroke, line width mm, fill, alpha)
STYLE = [
    ("sat_bare", "satellite_open_ground", PALE, 0.05, "FFFFFF"),
    ("sat_grass", "satellite_low_green", PALE, 0.05, None),
    ("sat_trees", "satellite_trees", PARK, 0.06, SAT_TREE),
    ("parks", "existing_parks", PARK, 0.10, None),
    ("ponds", "existing_water", WATER, 0.18, None),
    ("stream_banks", "existing_water", WATER, 0.22, None),
    ("paths", "existing_paths", GREY, 0.07, None),
    ("streets", "existing_streets", GREY, 0.10, "FFFFFF"),
    ("road_edges", "existing_roads", GREY, 0.10, None),
    ("kerbs", "existing_roads", PALE, 0.06, None),
    ("bridges", "existing_bridges", GREY, 0.18, None),
    ("walls", "existing_walls", PALE, 0.06, None),
    ("heritage_walls", "existing_heritage", HER, 0.20, None),
    ("sheds", "existing_buildings", PALE, 0.06, None),
    ("buildings", "existing_buildings", GREY, 0.09, "FFFFFF"),
    ("heritage", "existing_heritage", HER, 0.09, HER_FILL),
]
KEY_STYLE = [
    ("sat_trees", "satellite_trees", None, 0.0, SAT_TREE),
    ("streets", "existing_streets", PALE, 0.05, "FFFFFF"),
    ("road_edges", "existing_roads", PALE, 0.05, None),
    ("stream_banks", "existing_water", WATER, 0.25, None),
    ("ponds", "existing_water", WATER, 0.15, None),
    ("bridges", "existing_bridges", GREY, 0.15, None),
    ("buildings", "existing_buildings", None, 0.0, _tint(PALETTE["context"], 0.6)),
    ("heritage", "existing_heritage", None, 0.0, HER_FILL),
]
# Basemap_colour.svg: stroke widths in metres on the ground (the SVG has no sheet scale)
SVG_W = {"sat_bare": 0.1, "sat_grass": 0.1, "sat_trees": 0.12, "streets": 0.2, "paths": 0.15, "parks": 0.2, "ponds": 0.3, "stream_banks": 0.4, "road_edges": 0.2, "kerbs": 0.12, "bridges": 0.35, "walls": 0.12,
         "heritage_walls": 0.4, "sheds": 0.12, "buildings": 0.18, "heritage": 0.18}
LEGEND = [("buildings", u"Building"), ("heritage", u"Heritage building"), ("streets", u"Street"),
          ("paths", u"Footpath"), ("road_edges", u"Road edge (survey)"), ("kerbs", u"Kerb"), ("bridges", u"Bridge"), ("stream_banks", u"Stream bank"), ("parks", u"Park"),
          ("walls", u"Wall"), ("sat_trees", u"Tree cover 2023"), ("sat_grass", u"Low green 2023"),
          ("sat_bare", u"Open ground 2023")]

# ---- folders (same in every script) ----
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
CACHE_DIR = os.path.join(BERGAMA_ROOT, "cached", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
CACHE_FILE = os.path.join(CACHE_DIR, "basemap_layers.json")
# ================= end of COLOURS =================
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
    log.append(u"model read: " + u", ".join(u"%s %d" % kv for kv in sorted(cnt.items())) +
               u"; name texts %d (streets %d); section lines %d" % (
                   len(labels), sum(1 for l in labels if l[4] == "street"), len(sec)))
    for h in her:
        c = (sum(p[0] for p in h["ring"]) / len(h["ring"]), sum(p[1] for p in h["ring"]) / len(h["ring"]))
        log.append(u"  heritage: %s (%s) at %.0f, %.0f" % (h["name"] or u"no name text inside", h["layer"], c[0], c[1]))
    return {"frame": frame, "layers": out, "sections": sec, "calisma": work, "labels": labels, "floors": floors,
            "heritage_names": [[h["name"], h["layer"]] for h in her]}


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
def lighter(col, t=None):
    t = FADE_MIX if t is None else t
    return u"".join(u"%02X" % int(round(int(col[i:i + 2], 16) + (255 - int(col[i:i + 2], 16)) * t)) for i in (0, 2, 4))


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


# ================================================================ satellite land cover
def hatch_lines(rings, spacing, angle_deg):
    """even-odd line hatch of rings: [(a, b)] segments in the rings' own units"""
    ca, sa = math.cos(math.radians(angle_deg)), math.sin(math.radians(angle_deg))
    rows = {}
    for R in rings:
        T = [(p[0] * ca + p[1] * sa, -p[0] * sa + p[1] * ca) for p in R]
        for i in range(len(T)):
            a, b = T[i - 1], T[i]
            if a[1] == b[1]:
                continue
            if a[1] > b[1]:
                a, b = b, a
            j = int(math.ceil(a[1] / spacing - 0.5))
            while (j + 0.5) * spacing < b[1]:
                y = (j + 0.5) * spacing
                if y >= a[1]:
                    rows.setdefault(j, []).append(a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]))
                j += 1
    out = []
    for j, xs in rows.items():
        xs.sort()
        y = (j + 0.5) * spacing
        for x0, x1 in zip(xs[0::2], xs[1::2]):
            if x1 - x0 > 1e-6:
                out.append(((x0 * ca - y * sa, x0 * sa + y * ca), (x1 * ca - y * sa, x1 * sa + y * ca)))
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


# ================================================================ drawing (items: the Sections page format)
def draw(D, F, den, styles, x0, y0, sections=False, shadows=False, names=False, fade=None):
    """items of the map at 1:den, the frame's lower-left corner at page (x0, y0) mm"""
    k = 1000.0 / den
    box = (0.0, 0.0, F.w, F.h)
    items, cnt = [], {}

    def pg(p):
        return (x0 + p[0] * k, y0 + p[1] * k)
    if shadows:                                          # a shadow copy under every building (drawing device)
        for key in ("buildings", "heritage"):
            for cl, P in D["layers"].get(key, []):
                R = clip_ring([(q[0] + SHADOW_M[0], q[1] + SHADOW_M[1]) for q in (F.local(p) for p in P)], box)
                if len(R) >= 3:
                    items.append(("poly", [[pg(q) for q in R]], SHADOW, None, 0.0, None, "existing_shadows", 1, None, None))
    for key, layer, stroke, lw, fill in styles:
        n = 0
        fd = fade if (fade is not None and key in FADE_KEYS and stroke) else None
        far_ = lighter(stroke) if fd else stroke
        if key.startswith("sat_") or key == "streets":
            rings, local = [], []
            for cl, P in D["layers"].get(key, []):
                R = clip_ring([F.local(p) for p in P], box)
                if len(R) >= 3:
                    local.append(R)
                    rings.append([pg(q) for q in R])
            if rings and key == "streets":               # every edge first, then every surface: junctions stay open
                for R in local:
                    for f_, run in (fd.split(R + R[:1]) if fd else [(False, R + R[:1])]):
                        items.append(("line", [pg(q) for q in run], far_ if f_ else stroke, lw, None, layer, 1))
                items += [("poly", [R], fill, None, 0.0, None, layer, 1, None, None) for R in rings]
            elif rings:                                  # one shape, even-odd: the holes stay open
                items.append(("poly", rings, fill, stroke, lw, None, layer, 1, "eo", None))
                hp = HATCH.get(key)
                if hp:
                    for a, b in hatch_lines(rings, hp[0] * k, hp[1]):
                        items.append(("line", [a, b], hp[2], hp[3], None, layer, 1))
            cnt[key] = len(rings)
            continue
        for cl, P in D["layers"].get(key, []):
            Q = [F.local(p) for p in P]
            if min(q[0] for q in Q) > F.w or max(q[0] for q in Q) < 0 or min(q[1] for q in Q) > F.h or max(q[1] for q in Q) < 0:
                continue
            if cl and len(Q) >= 3:
                R = clip_ring(Q, box)
                if len(R) >= 3:
                    items.append(("poly", [[pg(q) for q in R]], fill, far_ if (fd and fd.far_ring(R)) else stroke, lw,
                                  None, layer, 1, None, None))
                    n += 1
            else:
                for run_ in clip_line(Q, box):
                    for f_, run in (fd.split(run_) if fd else [(False, run_)]):
                        items.append(("line", [pg(q) for q in run], (far_ if f_ else stroke) or PALE, lw or 0.05, None,
                                      layer, 1))
                    n += 1
        cnt[key] = n
    fr = [pg(q) for q in ((0, 0), (F.w, 0), (F.w, F.h), (0, F.h))]
    items.append(("poly", [fr], None, INK, 0.3, None, "frame", 0, None, None))
    for P in D.get("calisma", []):                         # the working area, a heavy line
        R = [pg(F.local(p)) for p in P]
        items.append(("line", R + R[:1], HER, 0.3, None, "calisma_alan", 1))
    if names:
        for t, x, y, ang, kind in D.get("labels", []):
            u, v = F.local((x, y))
            if not (2.0 < u < F.w - 2.0 and 2.0 < v < F.h - 2.0):
                continue
            a = (ang + math.degrees(F.rot)) % 360.0
            if 90.0 < a <= 270.0:                         # never upside down
                a -= 180.0
            X, Y = pg((u, v))
            items.append(("text", t, X, Y, NAME_MM, NAME_GREY, False, "L",
                          "names_streets" if kind == "street" else "names_places", a,
                          "i" if kind == "street" else None))
    if sections:
        for s in D.get("sections", []):
            a, b = F.local(s["line"][0]), F.local(s["line"][1])
            for run in clip_line([a, b], box):
                items.append(("line", [pg(q) for q in run], INK, 0.35, None, "section_lines", 1))
                for q, al in ((run[0], "R"), (run[-1], "L")):
                    X, Y = pg(q)
                    items.append(("text", s["name"], X + (-1.0 if al == "R" else 1.0), Y + 0.8, 2.2, INK, True, al,
                                  "section_lines", None, None))
    return items, cnt


def corner_block(F, den, x0, y0):
    """north circle, scale text and a segmented scale bar inside the frame's lower right corner, on white"""
    k = 1000.0 / den
    bar = 100.0 if den <= 2500 else 500.0
    L = bar * k
    w, h = L + 26.0, 16.0
    X, Y = x0 + F.w * k - w - 4.0, y0 + 4.0
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
    for i in range(4):                                    # four cells, black and white in turn
        c = [(xb + L * i / 4.0, yb), (xb + L * (i + 1) / 4.0, yb), (xb + L * (i + 1) / 4.0, yb + 1.4),
             (xb + L * i / 4.0, yb + 1.4)]
        it.append(("poly", [c], INK if i % 2 == 0 else "FFFFFF", INK, 0.15, None, "corner_block", 1, None, None))
    it.append(("text", u"0", xb, yb - 3.0, 2.0, INK, False, "C", "corner_block", None, None))
    it.append(("text", u"%d m" % bar, xb + L, yb - 3.0, 2.0, INK, False, "C", "corner_block", None, None))
    it.append(("text", u"1/%d" % den, xb, yb + 4.0, 3.2, INK, True, "L", "corner_block", None, None))
    return it


def furniture(F, den, x0, y0, title, legend, credit=None):
    """title and legend under the frame (north and scale bar: corner_block)"""
    k = 1000.0 / den
    it = []
    y = y0 - 8.0
    it.append(("text", title, x0, y, 4.0, INK, True, "L", "title", None, None))
    it.append(("text", u"1:%s" % format(den, ",d"), x0, y - 5.0, 3.0, INK, False, "L", "title", None, None))
    x = x0 + 40.0
    for key, layer, stroke, lw, fill, lab in legend:
        if fill or key in ("buildings", "heritage", "parks", "sat_grass"):
            box_ = [(x, y - 4.6), (x + 6.0, y - 4.6), (x + 6.0, y - 1.4), (x, y - 1.4)]
            it.append(("poly", [box_], fill, stroke, lw, None, "legend", 1, None, None))
            hp = HATCH.get(key)
            if hp:
                for a, b in hatch_lines([box_], hp[0] * k, hp[1]):
                    it.append(("line", [a, b], hp[2], hp[3], None, "legend", 1))
        else:
            it.append(("line", [(x, y - 3.0), (x + 6.0, y - 3.0)], stroke, lw, None, "legend", 1))
        it.append(("text", lab, x + 7.5, y - 3.8, 2.4, INK, False, "L", "legend", None, None))
        x += 7.5 + 0.5 * 2.4 * len(lab) + 7.0
    if credit:
        it.append(("text", credit, x0, y0 - 14.5, 1.8, GREY, False, "L", "title", None, None))
    return it


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


def write_pdf(path, w, h, items, title):
    """one page w x h mm; items in page mm, y up; each item's layer becomes a PDF layer"""
    objs = []

    def add(b):
        objs.append(b)
        return len(objs)

    def lay(it):
        t = it[0]
        return it[6] if t == "poly" else it[5] if t == "line" else it[8]
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
    body = bytearray(("%s 0 0 %s 0 0 cm\n1 J 1 j\n" % (_f(k), _f(k))).encode())
    for ly in layers:                                    # one marked block per layer, in first-use order
        body += ("/OC /oc%d BDC\n" % ocg[ly]).encode()
        for it in items:
            if lay(it) != ly:
                continue
            t = it[0]
            if t == "poly":
                rings, fill, stroke, lw = it[1:5]
                if not fill and not stroke:
                    continue
                A = ["q"]
                for r in rings:
                    A.append("%s %s m" % (_f(r[0][0]), _f(r[0][1])))
                    A += ["%s %s l" % (_f(p[0]), _f(p[1])) for p in r[1:]]
                    A.append("h")
                if fill:
                    A.append("%s rg" % _col(fill))
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
        body += b"EMC\n"
    cid = add(b"<< /Length %d >>\nstream\n" % len(body) + bytes(body) + b"\nendstream")
    props = " ".join("/oc%d %d 0 R" % (i, i) for i in ocg.values())
    res = add(("<< /Font << /F1 %d 0 R /F2 %d 0 R /F3 %d 0 R >> /Properties << %s >> >>" % (f_r, f_b, f_i, props)).encode())
    pages_id = len(objs) + 2
    page = add(("<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %s %s] /Contents %d 0 R /Resources %d 0 R >>" % (
        pages_id, _f(w / PT), _f(h / PT), cid, res)).encode())
    assert add(("<< /Type /Pages /Kids [%d 0 R] /Count 1 >>" % page).encode()) == pages_id
    oc = " ".join("%d 0 R" % i for i in ocg.values())
    cat = add(("<< /Type /Catalog /Pages %d 0 R /OCProperties << /OCGs [%s] /D << /Order [%s] /ON [%s] >> >> >>" % (
        pages_id, oc, oc, oc)).encode())
    info = add(b"<< /Title (" + _pdf_txt(title) + b") /Producer (Bergama Basemap) >>")
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
        path = path[:-4] + time.strftime("_%H%M%S") + ".pdf"
        with open(path, "wb") as f:
            f.write(bytes(out))
    return path


# ================================================================ Basemap_colour.svg (his plan inside calisma_alan)
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


# ================================================================ textures on his plan
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


def add_textures(body, s, log):
    """the water ticks and the promenade joints, each put directly after the path it lies on"""
    jobs = ((WATER_GROUP, None, "water"), (PROMENADE_GROUP, PROMENADE_FILLS, "promenade"))
    for gid, fills, kind in jobs:
        span = _group_span(body, gid)
        if span is None:
            log.append(u"FLAG texture %s: no group %s in his plan: no texture" % (kind, gid))
            continue
        g = body[span[0]:span[1]]
        out, last, n_shapes, n_lines = [], 0, 0, 0
        for m in re.finditer(r"<path\b[^>]*?/>", g):
            a = dict(re.findall(r'([\w:-]+)="([^"]*)"', m.group(0)))
            col = _hex6(a.get("fill"))
            if col is None or (fills is not None and (a.get("fill") or "").lower() not in fills):
                continue
            rings = [P for cl, P in path_rings(a.get("d", ""), 1.5) if len(P) >= 3]
            if not rings:
                continue
            d = []
            if kind == "water":
                row, tick, pitch = WATER_ROW * s, WATER_TICK * s, WATER_PITCH * s
                for (x0, y), (x1, _) in hatch_lines(rings, row, 0.0):
                    j = int(round(y / row - 0.5))
                    k_ = int(math.floor((x0 - (j % 2) * pitch / 2.0) / pitch))
                    while True:
                        xa = k_ * pitch + (j % 2) * pitch / 2.0
                        k_ += 1
                        if xa > x1 - tick:
                            break
                        if xa >= x0:                      # a small wave: up, then down
                            d.append(u"M%.1f,%.1fq%.1f,%.1f %.1f,0t%.1f,0" % (xa, y, tick / 4.0, -tick / 6.0,
                                                                          tick / 2.0, tick / 2.0))
                tone = _tint(col, 0.35)
            else:
                for p_, q_ in hatch_lines(rings, JOINT_M * s, 90.0):
                    d.append(u"M%.1f,%.1fL%.1f,%.1f" % (p_[0], p_[1], q_[0], q_[1]))
                tone = u"".join(u"%02X" % int(round(int(col[i:i + 2], 16) * 0.85)) for i in (0, 2, 4))
            if not d:
                continue
            n_shapes += 1
            n_lines += len(d)
            out.append(g[last:m.end()])
            out.append(u'<path id="texture_%s_%d" fill="none" stroke="#%s" stroke-width="%.3f" stroke-linecap="round" '
                       u'd="%s"/>' % (kind, n_shapes, tone, TEXTURE_W * s, u"".join(d)))
            last = m.end()
        out.append(g[last:])
        body = body[:span[0]] + u"".join(out) + body[span[1]:]
        if n_shapes:
            log.append(u"texture %s: %d line(s) on %d shape(s) of his group %s" % (kind, n_lines, n_shapes, gid))
        else:
            log.append(u"FLAG texture %s: no filled path %sin his group %s: no texture" % (
                kind, (u"with fill %s " % u" / ".join(fills)) if fills else u"", gid))
    return body


def plan_base(body, s, log):
    """his plan for the base map: the route groups switched off, the planted-ground underlay put under his trees"""
    off = []
    for g in BASE_OFF:
        m = re.search(r'<g\b[^>]*\bid="%s"[^>]*>' % re.escape(g), body)
        if m and "display=" not in m.group(0):
            body = body[:m.start()] + m.group(0)[:-1] + u' display="none">' + body[m.end():]
            off.append(g)
    trees, hidden, stack = [], 0, []
    for m in re.finditer(r'<g\b[^>]*?(/?)>|</g>|<use\b[^>]*>', body):
        t = m.group(0)
        if t.startswith("</g"):
            if stack and stack.pop():
                hidden -= 1
        elif t.startswith("<g"):
            if not t.endswith("/>"):
                h = 'display="none"' in t
                stack.append(h)
                hidden += 1 if h else 0
        elif not hidden and ('href="#' + TREE_SYMBOL) in t and 'display="none"' not in t:
            a = dict(re.findall(r'([\w:-]+)="([^"]*)"', t))
            tr = a.get("transform", "")
            mt = re.search(r"translate\(\s*([-\d.eE]+)[\s,]*([-\d.eE]+)?\s*\)", tr)
            ms = re.search(r"scale\(\s*([-\d.eE]+)", tr)
            mr = re.search(r"rotate\(\s*([-\d.eE]+)", tr)
            try:
                w, h = float(a["width"]), float(a["height"])
                sc = float(ms.group(1)) if ms else 1.0
                tx, ty = (float(mt.group(1)), float(mt.group(2) or 0.0)) if mt else (0.0, 0.0)
            except Exception:
                continue
            ang = math.radians(float(mr.group(1))) if mr else 0.0
            hx, hy = w * sc / 2.0, h * sc / 2.0
            trees.append((tx + hx * math.cos(ang) - hy * math.sin(ang), ty + hx * math.sin(ang) + hy * math.cos(ang),
                          max(w, h) * abs(sc) / 2.0))
    i = body.find(u'<g id="trees_group"')
    if trees and i >= 0:
        g = [u'<g id="planted_ground_underlay">']
        for d, col in zip(UNDERLAY_M, UNDERLAY):
            g.append(u'<g id="underlay_%s_m" fill="#%s" stroke="none">' % (("%g" % d).replace(".", "_"), col))
            g += [u'<circle cx="%.2f" cy="%.2f" r="%.2f"/>' % (x, y, r + d * s) for x, y, r in trees]
            g.append(u"</g>")
        g.append(u"</g>\n")
        body = body[:i] + u"\n".join(g) + body[i:]
    else:
        log.append(u"FLAG underlay: %s: no planted-ground underlay drawn" % (
            u"no tree symbols (%s...) found in his plan" % TREE_SYMBOL if not trees else u"no group trees_group in his plan"))
    log.append(u"his plan as base map: groups switched off: %s; planted-ground underlay under %d tree symbols of his plan"
               % (u", ".join(off) or u"none found", len(trees) if i >= 0 else 0))
    return add_textures(body, s, log)


def write_colour_svg(D, F, log, fade=None):
    src = os.path.join(BERGAMA_ROOT, PLAN_SVG)
    if not D.get("calisma"):
        return
    if not os.path.isfile(src):
        log.append(u"FLAG Basemap_colour.svg not written: %s not found" % src)
        return
    with open(src, encoding="utf-8") as f:
        txt = f.read()
    fr, how = plan_frame(txt, F)
    if fr is None:
        log.append(u"FLAG Basemap_colour.svg not written: %s in %s" % (how, src))
        return
    rx, ry, rw, rh = fr
    s = rw / F.w
    m0 = re.search(r"<svg\b[^>]*>", txt)
    m1 = txt.rfind("</svg>")
    vb = re.search(r'viewBox="([^"]+)"', m0.group(0)) if m0 else None
    if not m0 or m1 < 0 or not vb:
        log.append(u"FLAG Basemap_colour.svg not written: %s has no svg root with a viewBox" % src)
        return
    vx, vy, vw, vh = [float(v) for v in vb.group(1).replace(",", " ").split()]

    def U(p):
        u, v = F.local(p)
        return "%.2f,%.2f" % (rx + u * s, ry + rh - v * s)

    def UL(q):
        return "%.2f,%.2f" % (rx + q[0] * s, ry + rh - q[1] * s)
    box = (0.0, 0.0, F.w, F.h)
    out = [m0.group(0), u"<defs><clipPath id=\"bg_calisma_clip\"><path clip-rule=\"evenodd\" d=\"M%s,%s h%s v%s h%s Z "
           u"M%s,%s h%s v%s h%s Z %s\"/></clipPath></defs>" % (
               vx, vy, vw, vh, -vw, rx, ry, rw, rh, -rw,
               u" ".join(u"M" + u" L".join(U(p) for p in P) + u" Z" for P in D["calisma"])),
           u"<g id=\"existing_basemap_bw\">",
           u"<rect id=\"white_ground\" x=\"%s\" y=\"%s\" width=\"%s\" height=\"%s\" fill=\"#ffffff\"/>" % (rx, ry, rw, rh)]
    n = 0
    hp = HATCH["sat_grass"]
    out.append(u"<defs><pattern id=\"bg_hatch\" patternUnits=\"userSpaceOnUse\" width=\"%.3f\" height=\"%.3f\" "
               u"patternTransform=\"rotate(%.1f)\"><line x1=\"0\" y1=\"0\" x2=\"%.3f\" y2=\"0\" stroke=\"#%s\" "
               u"stroke-width=\"%.3f\"/></pattern></defs>" % (hp[0] * s, hp[0] * s, -hp[1], hp[0] * s, hp[2], 0.2 * s))
    out.append(u"<g id=\"existing_shadows\" fill=\"#%s\" stroke=\"none\">" % SHADOW)
    for key in (("buildings", "heritage") if SHADOWS else ()):
        for cl, P in D["layers"].get(key, []):
            R = clip_ring([(q[0] + SHADOW_M[0], q[1] + SHADOW_M[1]) for q in (F.local(p) for p in P)], box)
            if len(R) >= 3:
                out.append(u"<polygon points=\"%s\"/>" % u" ".join(UL(q) for q in R))
    out.append(u"</g>")
    for key, layer, stroke, lw, fill in STYLE:
        if key.startswith("sat_") or key == "streets":
            rings = [R for R in (clip_ring([F.local(p) for p in P], box) for cl, P in D["layers"].get(key, []))
                     if len(R) >= 3]
            n += len(rings)
            if key == "streets":
                out.append(u"<g id=\"%s_edges\" fill=\"none\" stroke=\"#%s\" stroke-width=\"%.3f\">" % (
                    layer, stroke, SVG_W[key] * s))
                for R in rings:
                    for f_, run in (fade.split(R + R[:1]) if fade else [(False, R + R[:1])]):
                        out.append(u"<polyline%s points=\"%s\"/>" % (
                            (u" stroke=\"#%s\"" % lighter(stroke)) if f_ else u"", u" ".join(UL(q) for q in run)))
                out.append(u"</g>")
                out.append(u"<g id=\"%s_surface\" fill=\"#%s\" stroke=\"none\">" % (layer, fill))
                out += [u"<polygon points=\"%s\"/>" % u" ".join(UL(q) for q in R) for R in rings]
                out.append(u"</g>")
            else:
                out.append(u"<path id=\"%s\" fill-rule=\"evenodd\" fill=\"%s\" stroke=\"#%s\" stroke-width=\"%.3f\" "
                           u"d=\"%s\"/>" % (layer, u"url(#bg_hatch)" if key in HATCH else u"#" + fill, stroke,
                                            SVG_W[key] * s, u" ".join(u"M" + u" L".join(UL(q) for q in R) + u" Z"
                                                                      for R in rings)))
            continue
        out.append(u"<g id=\"%s_%s\" fill=\"%s\" stroke=\"#%s\" stroke-width=\"%.3f\" stroke-linejoin=\"round\">" % (
            layer, key, (u"#" + fill) if fill else u"none", stroke, SVG_W.get(key, 0.2) * s))
        fd = fade if (fade is not None and key in FADE_KEYS) else None
        far_ = u" stroke=\"#%s\"" % lighter(stroke)
        for cl, P in D["layers"].get(key, []):
            Q = [F.local(p) for p in P]
            if cl and len(Q) >= 3:
                R = clip_ring(Q, box)
                if len(R) >= 3:
                    out.append(u"<polygon%s points=\"%s\"/>" % (far_ if (fd and fd.far_ring(R)) else u"",
                                                                u" ".join(UL(q) for q in R)))
                    n += 1
            else:
                for run_ in clip_line(Q, box):
                    for f_, run in (fd.split(run_) if fd else [(False, run_)]):
                        out.append(u"<polyline fill=\"none\"%s points=\"%s\"/>" % (far_ if f_ else u"",
                                                                                   u" ".join(UL(q) for q in run)))
                    n += 1
        out.append(u"</g>")
    out.append(u"<g id=\"names\" fill=\"#%s\" font-family=\"Arial, Helvetica, sans-serif\" font-size=\"%.2f\">" % (
        NAME_GREY, 3.0 * s))
    for t, x, y, ang, kind in D.get("labels", []):
        u, v = F.local((x, y))
        if not (2.0 < u < F.w - 2.0 and 2.0 < v < F.h - 2.0):
            continue
        a = (ang + math.degrees(F.rot)) % 360.0
        if 90.0 < a <= 270.0:
            a -= 180.0
        X, Y = rx + u * s, ry + rh - v * s
        out.append(u"<text x=\"%.2f\" y=\"%.2f\"%s transform=\"rotate(%.1f %.2f %.2f)\">%s</text>" % (
            X, Y, u" font-style=\"italic\"" if kind == "street" else u"", -a, X, Y, t.replace(u"&", u"&amp;").replace(u"<", u"&lt;")))
    out.append(u"</g>")
    out.append(u"</g>")
    out.append(u"<g id=\"plan_inside_calisma_alan\" clip-path=\"url(#bg_calisma_clip)\">")
    head = u"\n".join(out)
    tail = [u"</g>", u"<g id=\"calisma_alan_outline\" fill=\"none\" stroke=\"#%s\" stroke-width=\"%.3f\">" % (HER, 0.6 * s)]
    tail += [u"<polygon points=\"%s\"/>" % u" ".join(U(p) for p in P) for P in D["calisma"]]
    tail += [u"</g>", u"<rect id=\"site_alan_frame\" x=\"%s\" y=\"%s\" width=\"%s\" height=\"%s\" fill=\"none\" "
             u"stroke=\"#3a3a38\" stroke-width=\"%.3f\"/>" % (rx, ry, rw, rh, 0.4 * s), u"</svg>"]
    dst = os.path.join(OUT_DIR, "Basemap_colour.svg")
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt[:m0.start()])
        f.write(head)
        f.write(plan_base(txt[m0.end():m1], s, log))
        f.write(u"\n".join(tail))
    log.append(u"%s  %s (his plan %s, %.1f MB, inside calisma_alan; frame = %s at (%.2f, %.2f) %.2f x %.2f units, %.4f "
               u"units per m; %d black and white outlines under it)" % (
                   dst, time.strftime("%H:%M:%S"), os.path.basename(src), os.path.getsize(src) / 1048576.0, how, rx, ry, rw,
                   rh, s, n))


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
    D = load_or_read(log)
    F = Frame([tuple(p) for p in D["frame"]])
    D["turn_deg"] = round(math.degrees(F.rot), 4)
    D["layers"].update(load_veg(D, log))
    D["layers"].update(build_streets(D, F, log))
    fade = Fade(D, F)
    if fade.rows is not None:
        log.append(u"fade: context lines full within %.0f m of calisma_alan (%.0f %% of the frame), lighter beyond" % (
            FADE_M, 100.0 * fade.share))
    log.append(u"frame: site_alan %.2f x %.2f m, turned %.2f deg; north on the page points (%.3f, %.3f)" % (
        F.w, F.h, math.degrees(F.rot), F.north()[0], F.north()[1]))
    need = max(F.w * 1000.0 / (A0_W - 2 * A0_MARGIN), F.h * 1000.0 / (A0_H - 2 * A0_MARGIN - 16.0))
    n_a0 = int(math.ceil(need / A0_STEP) * A0_STEP)       # the smallest round scale at which the frame fits on A0
    for name, d, styles, sec, title in ((u"Basemap", den, STYLE, False, u"BASEMAP · existing"),
                                        (u"Keymap", kden, KEY_STYLE, True, u"KEY MAP")):
        for a0 in (False, True):
            if a0:
                d = n_a0
                w, h = A0_W, A0_H
                x0, y0 = (w - F.w * 1000.0 / d) / 2.0, (h - F.h * 1000.0 / d) / 2.0 + 8.0
            else:
                m = 15.0
                w = F.w * 1000.0 / d + 2 * m
                h = F.h * 1000.0 / d + 2 * m + 16.0
                x0, y0 = m, m + 16.0
            items, cnt = draw(D, F, d, styles, x0, y0, sections=sec, shadows=SHADOWS and not sec, names=not sec,
                              fade=fade)
            by = dict((s[0], s) for s in styles)
            leg = [by[k_] + (lab,) for k_, lab in LEGEND if k_ in by and cnt.get(k_)]
            items += corner_block(F, d, x0, y0)
            items += furniture(F, d, x0, y0, title, leg, None if sec else CREDIT)
            p = write_pdf(os.path.join(OUT_DIR, name + (u"_A0.pdf" if a0 else u".pdf")), w, h, items,
                          u"%s, site_alan, 1:%d" % (name, d))
            if a0:
                log.append(u"%s  A0 %.0fx%.0f mm, 1:%d" % (p, w, h, d))
            else:
                log.append(u"%s  %s (%.0f x %.0f mm, 1:%d; %s)" % (p, time.strftime("%H:%M:%S"), w, h, d, u", ".join(
                    u"%s %d" % kv for kv in sorted(cnt.items()))))
    write_colour_svg(D, F, log, fade)
    if not D.get("sections"):
        log.append(u"no curves on layer %s in the model: the key map has no section lines yet" % SECTION_LAYER)
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
