# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE 02 "What is there, grain of the town" v2 (14 Nov 2026; v2: also output/presentation/1.pdf and review/ PNGs). Rules: scripts/_template/SCRIPT_STANDARD.md.
One script per page (Aras 14 Nov 2026 10:46 UTC: "i want everything that we talk today in new scripts in the end of the
day we gonna have 12 scripts for each page"). This script makes page 2 alone, as one A3 landscape page (PDF + SVG);
it does not go through the Booklet.

What Aras asked for this page (14 Nov 2026 10:31-10:33 UTC):
  "Fix the top left empty spot on the map, use the latest data we have gathered from both dwg and settalite imagery
  combined"; "Bring back urban fabric, like where is old town where is planned buildings etc."; "fix the outlines and
  colour change of that outlines. and these outlines are totally fucked"; "outlines are inconsistent all across the
  map fix those kinds of details"; "get rid of these drawings" (the stream-edge strips); the land-use ring "to show
  where is older town, where is newer planned buildings etc."

What is drawn (nothing is invented; every shape is the survey, a data file of the kit or OpenStreetMap):
  MAP 1:25,000 (P02_DEN), the whole survey file on the site frame's axes (site_alan long side flat, as every map of
          the set): land cover (ESA WorldCover 2021, Data/bergama_landcover_worldcover2021.json), road surfaces
          (Data/roads_survey.json, Data/streets_town.json), the river (the Basemap's build_river along the Selinos
          centreline) and the survey's stream lines, survey walls as one pale hairline, the buildings and the study
          area (calisma_alan), the analysis frame (site_alan), bridge numbers 1-6 and clashes C1-C6.
  BUILDINGS: survey closed outlines + OpenStreetMap footprints and satellite bodies where the survey has only open
          street fronts (Basemap osm_houses, sat_houses) + the 2023 image check (Data/buildings_image_check.json:
          added / not drawn) + the town-street trims. Where the survey has no line work at all (the Acropolis hill in
          the top left, and any other blank part of the frame), OpenStreetMap buildings, streets and paths.
          Every building is filled in the colour of its URBAN FABRIC type (fabric(), the rules of the site board's
          fabric_types: heritage, mosques, civic & industrial, apartment blocks, old town, planned low-rise, small
          irregular) and outlined with ONE hairline (P02_HAIR mm) in a darker shade of its own colour. Buildings that
          touch show no line between them: every outline is drawn first at twice the width and the fills lie over it
          (half of each outer line stays visible, every shared wall is covered).
  KEY under the map; right column: the land-use ring of the site frame (built ground by urban fabric + ground
          cover, counted on 1 m cells), bridges and clashes.
  Not on this page any more: the stream-edge strips and their bank bars (Aras 14 Nov "get rid of these drawings").

v2.1 (14 Nov 2026, the brief's plan rules relayed 11:32 UTC: "every plan gets a scale, a north arrow and a legend ...
the same N, section and viewpoint labels everywhere"): the six nodes N1-N6 (their frames, labelled) and the twelve
section cuts N1-A ... N6-B (labelled at their north-west end) from Data/section_lines.json, with their legend rows.
Scale bar and north arrow: corner_block of the Basemap code, as before. This page shows the existing situation only.

v2.2 (14 Nov 2026, check loop of the first laptop run, Aras 11:24 UTC "no collisions"): at 1:25,000 the bridge
numbers, clash markers, node names and cut names sat on top of each other (the site is 2.8 km in a 4.5 km map). The
overview map now carries no names or markers (nodes, cuts, site frame and study area as lines only); an INSET of the
site frame at 1:INSET_DEN in the right column carries them, each name and marker set at the nearest free spot
(place_free: no two overlap; no leader lines, the plan rule of 4 Nov G6-4).

v2.3 (14 Nov 2026, Aras 12:10 UTC on the v2.1/v2.2 run): "the stream and industrial is too close in colour. planned
low rise and small irregular is too close to ground and green colours. So industrial should have one colour Buildings
should have one colour Heritage should be one colour and they should be different shade underneath"; "diffrentiate
which buildings have ground floor as commercial ... they should be grouped with their previous ones"; "there is still
too many gaps in the main drawing"; "dont put a opaque background on scale and north sign".
  COLOUR FAMILIES: (v2.9: MapBase's palette, from the masterplan SVG) heritage (monuments, mosques) = its
  heritage reds, buildings (old town, blocks, planned low-rise, small irregular, under construction) = its stone greys,
  civic & industrial = its slate; the types are lightness steps of their
  family's hue (FAB). COMMERCIAL: a building with an OpenStreetMap shop, office, craft or trade amenity point inside it
  or within COM_NEAR m of its outline (or a shop-tagged OSM footprint centre inside it) is filled in the vivid shade of
  its own type (FAB_COM). OSM does not record the floor: "ground floor" is NOT verified, the key says "shop on the plot".
  GAPS: the map ground is GROUND_C (WorldCover's non-vegetated land: built-up and bare, not in the land-cover file),
  not white paper; OpenStreetMap footprints that overlap no drawn building are added everywhere (osm_fill), not only in
  cells without survey lines. Scale bar and north arrow: no background box (overview and inset).

v2.4 (14 Nov 2026, Aras 12:14 UTC "drawings do flows outside of it"): every map layer is CUT to its frame by a clip
path in the PDF and SVG (clip ids "overview" and "inset"; strokes and wide OSM streets no longer pass the frame line);
a marker or name with no free spot is pulled inside its frame; frame_check FLAGs any map mark still outside its frame. Aras 12:15 UTC "it is not eye catching enough like the lines are
too thin": heavier pens (P02_HAIR 0.09, LW), building outlines darker (P02_EDGE_DARK 0.5), land cover stronger
(LC_LIGHT 0.25), streets, street edges and the stream in more contrast.

v2.5 (14 Nov 2026, Aras 12:16-12:18 UTC "update all maps to include every detail, and top of the map, data is missing
please fill in that"; "create one script for base map ... every map should use that"): the map's context (buildings with
fabric and shop shades, WorldCover, the 2023 satellite land cover, OSM areas, streets, water, walls, contours, trees) is
drawn by MapBase (scripts/bergama_mapbase_v*.py, mb_draw) from its cache: press MapBase once before this page. This
page keeps its own look (MapBase's default style is this page's). The land-use ring counts MapBase's buildings.

v2.6 (14 Nov 2026, check loop of the first laptop run of v2.5): the GROUND AND GREEN key ran into the credit. Rows of
the same colour are now one row (WorldCover and the 2023 image share a colour), the OpenStreetMap areas and contours
get a column of their own (four key columns), and a FLAG is written if any key column reaches the credit.

v2.7 (14 Nov 2026, Aras 13:02 UTC "make sure nothing repeats in the slides"): the node frames N1-N6 and the section
cuts are no longer drawn here (slides 2 and 6 carry them); this page keeps the fabric key, the shop shades and the
land-use ring, which no other slide repeats.
v2.9 (14 Nov 2026, Aras 15:20-15:23 UTC): the purple is gone; FAB, FAB_COM and GROUND_C are read from MapBase v1.3,
the one palette of the set, built from the masterplan SVG's own colours; each fabric key row also gives the share with
shops ("also give us percentages for the ground floor differentiated use ones").
v2.10 (14 Nov 2026): no presentation/1.pdf copy any more; Slide01 composes slide 1 (one A3 per slide) and writes it.
v2.8 (14 Nov 2026, check loop of run 3): the inset's north arrow covered clash marker C6; the inset's north arrow and
scale are now placed first and the bridge and clash markers keep off them (no collisions).

Component: Rhino 8 > Grasshopper > Python 3 Script (the board builder places it from the cloud kit).
  input  run     Button (or the previous script's done text)
  output log / done   as every Bergama script
Reads  ~/Downloads/Bergama/scripts/bergama_basemap_v*.py              (the newest: the drawing code)
       ~/Downloads/Bergama/cached/bergama_basemap/basemap_layers.json  (the survey, written by Basemap: press it first)
       ~/Downloads/Bergama/Data/bergama_style.json, bergama_osm.osm, bergama_landcover_worldcover2021.json,
       roads_survey.json, streets_town.json, houses_sat2023.json, buildings_image_check.json, selinos_centreline.json
Writes ~/Downloads/Bergama/output/bergama_p02/Page02_What_is_there.pdf, Page02_What_is_there.svg
       ~/Downloads/Bergama/cached/bergama_p02/ (OpenStreetMap houses over the whole map)
       ~/Downloads/Bergama/logs/bergama_p02_log.txt
"""
import os, time, json, math, re, glob, ast

# ---- SETTINGS ----
VERSION = "v2.10"
SLIDE = 1                          # output/presentation/1.pdf (Aras 14 Nov 11:22 UTC; slide 1 = analysis)
GH_LABEL = "Page02"
OUT_FOLDER = "bergama_p02"
LOG_NAME = "bergama_p02_log.txt"
GH_INPUTS = {}
LIB_GLOB = os.path.join("scripts", "bergama_basemap_v*.py")
LIB_END = "# ================================================================ main"
LC_FILE = os.path.join("Data", "bergama_landcover_worldcover2021.json")
SECTION_FILE = os.path.join("Data", "section_lines.json")   # v2.1: the Panel Review II nodes N1-N6 and cuts N1-A ... N6-B

PAGE_W, PAGE_H = 420.0, 297.0      # mm, A3 landscape (the booklet page)
MAP_X, MAP_TOP = 14.0, 269.0       # mm: the map's left edge and top (the booklet's frame p02.1: x 14, y 28 from the top)
MAP_MAX_W, MAP_MAX_H = 194.0, 169.0   # mm: the room of frame p02.1
P02_DEN = 25000                    # the map's scale 1:n (as the booklet's plan 01); a frame too large takes the next step
DEN_STEPS = (25000, 30000, 40000, 50000)
COL_X, COL_W = 210.0, 196.0        # mm: the right column
MARGIN_M = 15.0                    # m of paper round the survey's extent (as the site board's whole_frame)

P02_HAIR = 0.09                    # mm: the one pen of every building outline and survey wall (v2.4: was 0.05, Aras
                                   # 12:15 UTC "the lines are too thin")
LW = {"water": 0.25, "osm_water": 0.22, "her_wall": 0.3, "bridge": 0.3, "study": 0.45, "node": 0.35, "cut": 0.45,
      "site": 0.3, "frame": 0.35}   # v2.4: heavier pens (were 0.12 / 0.12 / 0.12 / 0.12 / 0.35 / 0.18 / 0.25 / 0.12 / 0.25)
P02_EDGE_DARK = 0.5                # a building outline = its fabric colour mixed this far toward the ink (ours)
BEYOND_CELL = 50.0                 # m: OpenStreetMap is drawn only where no survey line lies in its cell or the 8 round it
BEYOND_W = {"motorway": 10.0, "trunk": 9.0, "primary": 8.0, "secondary": 7.0, "tertiary": 6.0, "unclassified": 5.0,
            "residential": 5.0, "living_street": 4.0, "service": 3.5, "pedestrian": 4.0}   # m drawn (ours: OSM has none)
PATH_TAGS = ("track", "footway", "path", "steps", "cycleway", "bridleway")
INSET_DEN = 15000                 # v2.2: the inset of the site frame (2.85 km fits the right column at 1:15,000)
AREA_CELL = 1.0                    # m: cells of the land-use count of the site frame

# colours (the round 9 hue table of the board set; FAB = building fabric, in its rank order)
INK = "2C2219"
PAPER = "F7F5EF"
# v2.9: FAB, FAB_COM and GROUND_C are MapBase's (the one palette of the set, from the masterplan SVG; Aras 14 Nov 15:20)
def _mb_colours():
    found = glob.glob(os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "scripts", "bergama_mapbase_v*.py"))
    src_ = max(found, key=lambda p: [int(n) for n in re.findall(r"\d+", os.path.basename(p))])
    with open(src_, encoding="utf-8") as f:
        code = f.read()
    ns = {}
    for name in ("FAB", "FAB_COM", "GROUND_C"):
        m = re.search(r"^%s = (\{[^}]*\}|\"[0-9A-F]{6}\")" % name, code, re.M)
        ns[name] = ast.literal_eval(m.group(1))
    return ns["FAB"], ns["FAB_COM"], ns["GROUND_C"]


FAB, FAB_COM, GROUND_C = _mb_colours()
COM_NEAR = 5.0                     # m: a shop point this close to an outline belongs to it (OSM vs survey offset; ours)
COM_SHOP_AMENITY = ("restaurant", "cafe", "bank", "pharmacy", "fast_food", "bar", "pub", "marketplace", "fuel",
                    "ice_cream", "bureau_de_change", "money_transfer")
FAB_ORDER = ["monument", "sacred", "traditional", "block", "regular", "selfbuilt", "large", "construction"]
FAB_WORDS = {"monument": u"Monuments, historic", "sacred": u"Mosques & sacred", "traditional": u"Old town fabric",
             "block": u"Apartment blocks", "regular": u"Planned low-rise", "selfbuilt": u"Small irregular",
             "large": u"Civic & industrial", "construction": u"Under construction"}
FAB_RULE = {"monument": u"survey heritage layers, heritage names, OSM historic tags",
            "sacred": u"mosque names, OSM places of worship",
            "traditional": u"dense, attached, irregular grain",
            "block": u"3+ surveyed floors on regular footprints",
            "regular": u"regular, aligned footprints",
            "selfbuilt": u"under 130 m2, irregular, loose grain",
            "large": u"public uses (OSM) or 1,000 m2+",
            "construction": u"OSM construction"}
LC = {"trees": ("74804F", u"Woods & tree cover"), "orchard": ("8F966A", u"Orchards (inferred)"),
      "shrub": ("A7AC86", u"Shrubs"), "grass": ("ABB287", u"Grass"), "farmland": ("BDB57A", u"Fields")}
LC_ORDER = ("farmland", "grass", "shrub", "orchard", "trees")
LC_LIGHT = 0.25                    # land cover mixed this far toward the paper on the map (the buildings read first)
STREET_C, STREET_EDGE = "F1EEE6", "8F8A7A"   # v2.4: more contrast (was E9E6DE, B0AC9C)
WALL_C = "B0AC9C"
WATER_C, WATER_LINE = "6B9FB8", "3F6F86"   # v2.4: stronger (was 91ADB4, 5D7F8D)
HER_WALL = "B08870"
BRIDGE_C, CLASH_C = "84573E", "8B3A3F"
STUDY_C = "6A4C93"
NODE_C, CUT_C = "4A3F35", "C0392B"   # v2.1: node frames (ink) and section cuts (the key-map cut red)

HERITAGE_WORDS = (u"tarihi", u"harabe", u"harap", u"kalıntı", u"kalinti", u"hamam", u" han ", u"bedesten", u"arasta",
                  u"türbe", u"turbe", u"medrese", u"kızıl avlu", u"kizil avlu", u"tapınağı", u"tapinagi", u"kilise",
                  u"sinagog", u"çeşme", u"cesme", u"sebil", u"kervansaray", u"müze", u"muze")
SACRED_WORDS = (u"cami", u"mescit", u"mescid", u"cemevi", u"tekke", u"zaviye")
LARGE_BUILDING = ("school", "hospital", "public", "civic", "government", "industrial", "warehouse", "commercial",
                  "retail", "kindergarten", "university", "college", "stadium", "sports_hall", "train_station",
                  "transportation", "office", "hotel", "supermarket", "factory", "hangar")
LARGE_AMENITY = ("school", "hospital", "college", "university", "kindergarten", "townhall", "courthouse", "police",
                 "fire_station", "clinic", "library", "marketplace", "bus_station", "community_centre")
SACRED_TAGS = ("mosque", "church", "synagogue", "temple", "chapel", "cathedral", "shrine")

# bridges (survey coordinates, the concept record table 2.1, as the site board BRIDGES_K) in stream order, upstream
# first, with the one spelling of common/data/NAMES.py; clashes C1-C6 (pr1_drawings v3.1; C5 = the centre of the K5
# working area, the site board's C5_XY)
BRIDGES = [(1, u"side inlet crossing", 29628.35, 32630.87), (2, u"small crossing", 29604.93, 32622.02),
           (3, u"Ulucami Önü Köprüsü", 29846.40, 32277.71), (4, u"Tabak Köprüsü", 30037.01, 32121.57),
           (5, u"Üç Kemer Köprüsü", 30293.63, 31792.25), (6, u"Adnan Menderes Bulvarı road bridge", 30646.94, 31251.65)]
CLASHES = [("C1", 29941.0, 32200.0, u"walls cut the town off"), ("C2", 30204.0, 31975.0, u"heritage over a hidden stream"),
           ("C3", 29846.0, 32278.0, u"Ulucami Önü Köprüsü: monument and traffic"),
           ("C4", 30031.6, 32119.5, u"dry bed, bad smell"), ("C5", 30359.2, 31631.8, u"flood against everyday life"),
           ("C6", 30830.0, 31160.0, u"industry at the confluence")]

KICKER = u"A  SITE AND STREAM EDGE · ANALYSIS"
TITLE = u"What is there, grain of the town"
INTRO = (u"The whole survey area as it is today: buildings by urban fabric, ground and green, the Selinos stream with "
         u"its six bridges, and the places where stream and town clash. The base the later plans are read on.")
CREDIT = (u"Sources: survey Bergama_Altlik.3dm (buildings, floors, walls, road lines, stream lines); road surfaces and "
          u"town streets read between the survey's lines (roads_survey.json, streets_town.json); houses behind open "
          u"survey fronts from OpenStreetMap and from Esri World Imagery (Maxar, 1 Mar 2023, about +-5 m; "
          u"houses_sat2023.json, buildings_image_check.json); beyond the survey (the Acropolis hill): (c) OpenStreetMap "
          u"contributors; land cover ESA WorldCover 2021 (10 m, CC BY 4.0), orchards inferred near surveyed olive and "
          u"fruit symbols. Urban fabric: each building's type from heritage layers and names, OSM tags, surveyed "
          u"floors, footprint size and regularity, shared walls and the grain of the 40 m around it (a reading, not a "
          u"survey record).")

# ---- folders (same in every script) ----
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
CACHE_DIR = os.path.join(BERGAMA_ROOT, "cached", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")


def load_lib(log):
    """the drawing code of the newest Basemap script (everything above its main) as a dict of names"""
    found = glob.glob(os.path.join(BERGAMA_ROOT, LIB_GLOB))
    if not found:
        raise RuntimeError(u"no %s: run Bergama.bat once (the kit copies the Basemap script), then press again"
                           % os.path.join(BERGAMA_ROOT, LIB_GLOB))
    src_ = max(found, key=lambda p: [int(n) for n in re.findall(r"\d+", os.path.basename(p))])
    with open(src_, encoding="utf-8") as f:
        code = f.read()
    if LIB_END not in code:
        raise RuntimeError(u"%s has no line %r: it is older than Basemap v4" % (src_, LIB_END))
    ns = {"__name__": "bergama_basemap_lib"}
    exec(compile(code[:code.index(LIB_END)], src_, "exec"), ns)
    for need in ("write_pdf", "write_svg", "localise", "osm_houses", "image_check", "town_streets", "build_river",
                 "clip_ring", "clip_line", "corner_block", "text_w", "to_survey"):
        if need not in ns:
            raise RuntimeError(u"%s has no %s: update the kit (Bergama.bat), then press again" % (src_, need))
    ns["BERGAMA_ROOT"] = BERGAMA_ROOT
    os.makedirs(CACHE_DIR, exist_ok=True)
    ns["HOUSE_FILE"] = os.path.join(CACHE_DIR, "osm_houses_whole.json")   # never the Basemap's own caches
    ns["STREET_FILE"] = os.path.join(CACHE_DIR, "streets_whole.json")
    log.append(u"drawing code: %s (%s %s)" % (src_, ns.get("GH_LABEL"), ns.get("VERSION")))
    return ns


# ================================================================ small geometry
def mixh(a, b, t):
    """two hex colours mixed: t = share of b"""
    pa = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    pb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join("%02X" % int(round(pa[i] + (pb[i] - pa[i]) * t)) for i in range(3))


def area(P):
    return 0.5 * sum(P[i - 1][0] * P[i][1] - P[i][0] * P[i - 1][1] for i in range(len(P)))


def pip(x, y, P):
    c = False
    n = len(P)
    for i in range(n):
        a, b = P[i - 1], P[i]
        if (a[1] > y) != (b[1] > y) and x < a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1]):
            c = not c
    return c


def hull(pts):
    p = sorted(set((round(q[0], 3), round(q[1], 3)) for q in pts))
    if len(p) < 3:
        return p

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for q in p:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(p):
        while len(up) >= 2 and cr(up[-2], up[-1], q) <= 0:
            up.pop()
        up.append(q)
    return lo[:-1] + up[:-1]


def min_rect(P):
    """(area, angle of its long side) of the smallest rectangle round P"""
    H = hull(P)
    if len(H) < 3:
        return None
    best = None
    for i in range(len(H)):
        a, b = H[i - 1], H[i]
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        c, s = math.cos(ang), math.sin(ang)
        us = [q[0] * c + q[1] * s for q in H]
        vs = [-q[0] * s + q[1] * c for q in H]
        A = (max(us) - min(us)) * (max(vs) - min(vs))
        if best is None or A < best[0]:
            best = (A, ang if (max(us) - min(us)) >= (max(vs) - min(vs)) else ang + math.pi / 2.0)
    return best


def seg_d(px, py, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 <= 0 else max(0.0, min(1.0, ((px - a[0]) * dx + (py - a[1]) * dy) / L2))
    return math.hypot(px - a[0] - t * dx, py - a[1] - t * dy)


# ================================================================ the whole map's frame
def whole_frame(B, D):
    """the survey's whole extent on the site frame's axes (long side of site_alan flat), MARGIN_M m round it"""
    FS = B["Frame"]([tuple(p) for p in D["frame"]])
    us, vs = [], []
    for key, items in D["layers"].items():
        for cl, P in items:
            for p in P:
                q = FS.raw(p)
                us.append(q[0])
                vs.append(q[1])
    u0, u1, v0, v1 = min(us) - MARGIN_M, max(us) + MARGIN_M, min(vs) - MARGIN_M, max(vs) + MARGIN_M

    def back(qx, qy):                                     # raw -> survey (the inverse turn)
        return (FS.ca * qx + FS.sa * qy, -FS.sa * qx + FS.ca * qy)
    FW = B["Frame"]([back(u0, v0), back(u1, v0), back(u1, v1), back(u0, v1)])
    return FS, FW


# ================================================================ OpenStreetMap
def read_osm(B, log):
    """{"bld": [(survey ring, tags)], "ways": [(survey points, tags)], "nodes": [(x, y, tags)]} of the kit's OSM file"""
    import xml.etree.ElementTree as ET
    src = os.path.join(BERGAMA_ROOT, B["OSM_FILE"])
    out = {"bld": [], "ways": [], "nodes": [], "shops": []}   # v2.3: shops = (x, y) of shop / office / craft points
    if not os.path.isfile(src):
        log.append(u"FLAG OpenStreetMap: %s not found: nothing drawn beyond the survey, no OSM tags for the fabric" % src)
        return out
    root = ET.parse(src).getroot()
    nodes = {}
    for n in root.iter("node"):
        try:
            ll = (float(n.get("lon")), float(n.get("lat")))
        except (TypeError, ValueError):
            continue
        nodes[n.get("id")] = ll
        tg = dict((t.get("k"), t.get("v")) for t in n.findall("tag"))
        if tg.get("amenity") or tg.get("building") or tg.get("historic"):
            x, y = B["to_survey"](*ll)
            out["nodes"].append((x, y, tg))
        if _is_shop(tg):
            out["shops"].append(B["to_survey"](*ll))
    for w in root.iter("way"):
        tg = dict((t.get("k"), t.get("v")) for t in w.findall("tag"))
        refs = [nd.get("ref") for nd in w.findall("nd")]
        P = [B["to_survey"](*nodes[r]) for r in refs if r in nodes]
        if len(P) < 2:
            continue
        if _is_shop(tg) and refs[0] == refs[-1]:          # v2.3: a shop footprint: its centre
            out["shops"].append((sum(q[0] for q in P[:-1]) / max(1, len(P) - 1), sum(q[1] for q in P[:-1]) / max(1, len(P) - 1)))
        if "building" in tg:
            if len(refs) >= 4 and refs[0] == refs[-1] and len(P) >= 4:
                out["bld"].append((P[:-1], tg))
            continue
        out["ways"].append((P, tg))
    log.append(u"OpenStreetMap: %d building footprints, %d other ways, %d tagged points, %d shop / office / craft places" % (
        len(out["bld"]), len(out["ways"]), len(out["nodes"]), len(out["shops"])))
    return out


def _is_shop(tg):
    """v2.3: an OSM tag set of a shop, office, workshop or trade amenity (the commercial uses OSM records)"""
    return bool(tg.get("shop") or tg.get("office") or tg.get("craft") or tg.get("amenity") in COM_SHOP_AMENITY or
                tg.get("building") in ("commercial", "retail"))


# ================================================================ urban fabric
def fabric(units, log):
    """u["fab"] for every unit: the rules of the site board's fabric_types (survey layer -> heritage, names, OSM tags,
    floors, footprint regularity, shared walls, the grain of the 40 m round it). Shared walls: two outlines within
    0.5 m of each other (OSM and satellite bodies never share an edge to the centimetre as survey faces do)."""
    t0 = time.time()
    g = {}
    for k, u in enumerate(units):
        u["bb"] = (min(q[0] for q in u["P"]), min(q[1] for q in u["P"]), max(q[0] for q in u["P"]), max(q[1] for q in u["P"]))
        u["cx"], u["cy"] = sum(q[0] for q in u["P"]) / len(u["P"]), sum(q[1] for q in u["P"]) / len(u["P"])
        r = min_rect(u["P"])
        u["rect"] = u["A"] / max(r[0], 1e-6) if r else 1.0
        u["ang"] = r[1] if r else 0.0
        for i in range(int(u["bb"][0] // 20.0), int(u["bb"][2] // 20.0) + 1):
            for j in range(int(u["bb"][1] // 20.0), int(u["bb"][3] // 20.0) + 1):
                g.setdefault((i, j), []).append(k)
    for k, u in enumerate(units):                         # attached: another outline within 0.5 m of a corner
        att = False
        near = set()
        for i in range(int((u["bb"][0] - 1) // 20.0), int((u["bb"][2] + 1) // 20.0) + 1):
            for j in range(int((u["bb"][1] - 1) // 20.0), int((u["bb"][3] + 1) // 20.0) + 1):
                near.update(g.get((i, j), ()))
        near.discard(k)
        for m in near:
            v = units[m]
            if v["bb"][0] > u["bb"][2] + 0.5 or v["bb"][2] < u["bb"][0] - 0.5 or v["bb"][1] > u["bb"][3] + 0.5 or \
                    v["bb"][3] < u["bb"][1] - 0.5:
                continue
            Q = v["P"]
            for p in u["P"]:
                if any(seg_d(p[0], p[1], Q[i - 1], Q[i]) <= 0.5 for i in range(len(Q))):
                    att = True
                    break
            if att:
                break
        u["att"] = att
    R = 40.0
    for k, u in enumerate(units):
        nb = set()
        for i in range(int((u["cx"] - R) // 20.0), int((u["cx"] + R) // 20.0) + 1):
            for j in range(int((u["cy"] - R) // 20.0), int((u["cy"] + R) // 20.0) + 1):
                nb.update(m for m in g.get((i, j), ()) if math.hypot(units[m]["cx"] - u["cx"], units[m]["cy"] - u["cy"]) <= R)
        mains = [units[m] for m in nb]
        w = sum(v["A"] for v in mains) or 1.0
        zx = sum(math.cos(4.0 * v["ang"]) * v["A"] for v in mains)
        zy = sum(math.sin(4.0 * v["ang"]) * v["A"] for v in mains)
        u["cov"] = sum(v["A"] for v in mains) / (math.pi * R * R)
        u["coh"] = math.hypot(zx, zy) / w
        u["attsh"] = sum(1 for v in mains if v["att"]) / float(max(1, len(mains)))
    for u in units:
        nm = u" " + (u.get("name") or u"").lower() + u" "
        tg = u.get("tags") or {}
        if u.get("her") or any(w_ in nm for w_ in HERITAGE_WORDS) or tg.get("historic") or tg.get("heritage") or \
                tg.get("building") in ("ruins", "historic"):
            t = "monument"
        elif any(w_ in nm for w_ in SACRED_WORDS) or tg.get("building") in SACRED_TAGS or \
                tg.get("amenity") == "place_of_worship":
            t = "sacred"
        elif tg.get("building") == "construction":
            t = "construction"
        elif tg.get("building") in LARGE_BUILDING or tg.get("amenity") in LARGE_AMENITY or u["A"] >= 1000.0:
            t = "large"
        elif u["fl"] >= 4 or (u["fl"] >= 3 and u["rect"] >= 0.75):
            t = "block"
        elif u["cov"] >= 0.35 and u["attsh"] >= 0.55 and (u["coh"] < 0.8 or u["rect"] < 0.85):
            t = "traditional"
        elif u["A"] < 130.0 and (u["rect"] < 0.8 or u["coh"] < 0.6) and u["attsh"] < 0.5:
            t = "selfbuilt"
        elif u["rect"] >= 0.8 and u["coh"] >= 0.6:
            t = "regular"
        elif u["cov"] >= 0.35:
            t = "traditional"
        else:
            t = "selfbuilt" if (u["rect"] < 0.8 and u["A"] < 130.0) else "regular"
        u["fab"] = t
    n = dict((f_, sum(1 for u in units if u["fab"] == f_)) for f_ in FAB_ORDER)
    log.append(u"urban fabric of %d buildings (%.1f s): %s" % (len(units), time.time() - t0, u", ".join(
        u"%s %d" % (FAB_WORDS[f_], n[f_]) for f_ in FAB_ORDER)))


# ================================================================ cells: the land-use count of the site frame
def rows_fill(rings, box, c):
    """even-odd fill of rings (frame m) on c m cells of box (u0, v0, u1, v1): [row bits], row 0 = the south edge"""
    nx, ny = int(math.ceil((box[2] - box[0]) / c)), int(math.ceil((box[3] - box[1]) / c))
    xs = [[] for _ in range(ny)]
    for Q in rings:
        for i in range(len(Q)):
            a, b = Q[i - 1], Q[i]
            if a[1] == b[1]:
                continue
            if a[1] > b[1]:
                a, b = b, a
            j = max(0, int(math.ceil((a[1] - box[1]) / c - 0.5)))
            k_ = (b[0] - a[0]) / (b[1] - a[1])
            while j < ny and box[1] + (j + 0.5) * c < b[1]:
                xs[j].append(a[0] + (box[1] + (j + 0.5) * c - a[1]) * k_)
                j += 1
    rows = []
    for X in xs:
        X.sort()
        r = 0
        for x0, x1 in zip(X[0::2], X[1::2]):
            a, b = max(0, int(round((x0 - box[0]) / c))), min(nx, int(round((x1 - box[0]) / c)))
            if b > a:
                r |= ((1 << (b - a)) - 1) << a
        rows.append(r)
    return rows


def land_use(units, L, lc, box, log):
    """[(label, hex, m2)] of the site frame box (frame m), each cell counted once, first come first served: buildings
    by fabric, the stream, streets, land cover by class, the rest open ground"""
    c = AREA_CELL
    nx = int(math.ceil((box[2] - box[0]) / c))
    full = (1 << nx) - 1
    taken = None
    out = []

    def take(label, col, rings):
        nonlocal taken
        R = rows_fill(rings, box, c)
        if taken is None:
            taken = [0] * len(R)
        R = [r & ~t & full for r, t in zip(R, taken)]
        taken = [r | t for r, t in zip(R, taken)]
        out.append((label, col, sum(bin(r).count("1") for r in R) * c * c))
    for f_ in FAB_ORDER:
        take(FAB_WORDS[f_], FAB[f_], [u["P"] for u in units if u["fab"] == f_])
    take(u"The stream", WATER_C, [Q for cl, Q, a, b in L.get("river", [])])
    take(u"Streets", STREET_C, [Q for key in ("road_net", "town_net") for cl, Q, a, b in L.get(key, [])])
    for k_ in ("trees", "orchard", "shrub", "grass", "farmland"):
        take(LC[k_][1], LC[k_][0], lc.get(k_, []))
    tot = (box[2] - box[0]) * (box[3] - box[1])
    rest = tot - sum(a_ for _, _, a_ in out)
    out.append((u"Other open ground", GROUND_C, max(0.0, rest)))
    log.append(u"land use of the site frame (%.1f ha, %.0f m cells): %s" % (tot / 1e4, c, u", ".join(
        u"%s %.2f ha" % (l_, a_ / 1e4) for l_, _, a_ in out)))
    return out, tot


# ================================================================ drawing
def main():
    t0 = time.time()
    log = []
    B = load_lib(log)
    S = B["load_style"]()
    B["set_grain"](S, log)                                # the paper grain of the "~" fills (as every drawing of the set)
    if not os.path.isfile(B["CACHE_FILE"]):
        raise RuntimeError(u"%s not found: press Basemap once first (it reads the survey and writes this cache)"
                           % B["CACHE_FILE"])
    with open(B["CACHE_FILE"], encoding="utf-8") as f:
        D = json.load(f)
    FS, F = whole_frame(B, D)
    den = next((d for d in DEN_STEPS if F.w * 1000.0 / d <= MAP_MAX_W and F.h * 1000.0 / d <= MAP_MAX_H), DEN_STEPS[-1])
    k = 1000.0 / den
    log.append(u"map: the whole survey file %.0f x %.0f m (+%.0f m) on site_alan's axes, 1:%s, %.1f x %.1f mm" % (
        F.w, F.h, MARGIN_M, format(den, ",d"), F.w * k, F.h * k))
    box = (0.0, 0.0, F.w, F.h)
    MBL = load_mb(log)                                    # v2.5: the one base map (MapBase)
    C = MBL["mb_load"](log)
    if C is None:
        raise RuntimeError(u"no MapBase cache: press MapBase once (after Basemap), then press this page again")
    units = []
    for R_, fab_, com, src, nm in C["bld"]:
        Q = [F.local(p) for p in R_]
        if len(Q) >= 3:
            units.append({"P": Q, "A": abs(area(Q)), "fab": fab_, "com": bool(com), "src": src,
                          "cx": sum(q[0] for q in Q) / len(Q), "cy": sum(q[1] for q in Q) / len(Q)})
    L = {"river": [(True, [F.local(p) for p in R_], 0, 0) for R_ in C["polys"].get("river", [])],
         "road_net": [(True, [F.local(p) for p in R_], 0, 0) for R_ in C["polys"].get("streets", [])]}
    lc = dict((k_, [[F.local(p) for p in R_] for R_ in v]) for k_, v in C["lc"].items())
    log.append(u"urban fabric (MapBase): %s; with shops %d" % (u", ".join(u"%s %d" % (FAB_WORDS[f_], sum(
        1 for u in units if u["fab"] == f_)) for f_ in FAB_ORDER), sum(1 for u in units if u["com"])))
    # ---- the land-use count of the site frame (site_alan, the analysis frame)
    sb = [F.local(p) for p in D["frame"]]
    sbox = (min(q[0] for q in sb), min(q[1] for q in sb), max(q[0] for q in sb), max(q[1] for q in sb))
    su = [u for u in units if sbox[0] <= u["cx"] <= sbox[2] and sbox[1] <= u["cy"] <= sbox[3]]
    lu, lu_tot = land_use(su, L, lc, sbox, log)
    bt = sum(u["A"] for u in su) or 1.0
    shares = dict((f_, 100.0 * sum(u["A"] for u in su if u["fab"] == f_) / bt) for f_ in FAB_ORDER)
    com_sh = dict((f_, 100.0 * sum(u["A"] for u in su if u["fab"] == f_ and u["com"]) / bt) for f_ in FAB_ORDER)
    log.append(u"shop shares (v2.9; footprint area of each type with MapBase's shop flag / all built footprint in the site "
               u"frame, so each is part of its type's share): %s" % u", ".join(
                   u"%s %.1f%% of %.1f%%" % (FAB_WORDS[f_], com_sh[f_], shares[f_]) for f_ in FAB_ORDER if shares[f_] > 0))

    # ================================================================ the page
    items = []
    secs = {}                                             # v2.7: no nodes N1-N6 or cuts here (slides 2 and 6 keep them;
                                                          # Aras 14 Nov 13:02 UTC "make sure nothing repeats in the slides")
    drawn = {}                                            # v2.5: what MapBase drew on the overview (for the key)
    taken = []                                            # v2.2: boxes (page mm) of the inset's names and markers

    clips = {}                                            # v2.4: clip id -> [[frame ring]] (page mm)
    frames = []                                           # v2.4: (clip id, page box) for frame_check

    def draw_map(X0, Y0, k, box, names, cid):
        """one drawing of the map layers: box (frame m) at 1000/k, its lower-left corner at page (X0, Y0) mm;
        names = the inset (names and markers, each at a free spot)"""
        def pg(q):
            return (X0 + (q[0] - box[0]) * k, Y0 + (q[1] - box[1]) * k)
        fb = (X0, Y0, X0 + (box[2] - box[0]) * k, Y0 + (box[3] - box[1]) * k)
        clips[cid] = [[[(fb[0], fb[1]), (fb[2], fb[1]), (fb[2], fb[3]), (fb[0], fb[3])]]]
        frames.append((cid, fb))
        n0 = len(items)

        def poly(rings, fill, layer, stroke=None, lw=0.0):
            rr = [R for R in (B["clip_ring"](R_, box) for R_ in rings) if len(R) >= 3]
            if rr:
                items.append(("poly", [[pg(q) for q in R] for R in rr], fill, stroke, lw, None, layer, 1, "eo", None))

        def line(P, col, lw, layer):
            for run in B["clip_line"](P, box):
                if len(run) >= 2:
                    items.append(("line", [pg(q) for q in run], col, lw, None, layer, 1))
        mbc = MBL["mb_draw"](C, items, lambda p: pg(F.local(p)), k, fb, cid)   # v2.5: the one base map
        if not names:
            drawn.update(mbc)
        for R in D.get("calisma") or []:                      # the study area
            Q = [F.local(p) for p in R]
            line(Q + [Q[0]], STUDY_C, LW["study"], "study_area")
        for nid, nd in sorted((secs.get("nodes") or {}).items()):
            Q = [F.local(p) for p in nd.get("corners") or []]
            if len(Q) >= 3:
                line(Q + [Q[0]], NODE_C, LW["node"], "nodes")
        for sid, ab in sorted((secs.get("lines") or {}).items()):
            if len(ab) >= 2:
                line([F.local(ab[0]), F.local(ab[1])], CUT_C, LW["cut"], "section_cuts")
        line(sb + [sb[0]], INK, LW["site"], "site_alan")
        for i_ in range(n0, len(items)):                  # v2.4: every map layer cut to the frame
            t_ = items[i_]
            if t_[0] == "poly" and t_[9] is None:
                items[i_] = t_[:9] + (cid,)
            elif t_[0] == "line" and t_[4] is None:
                items[i_] = t_[:4] + (cid,) + t_[5:]
        items.append(("line", [pg((box[0], box[1])), pg((box[2], box[1])), pg((box[2], box[3])), pg((box[0], box[3])),
                               pg((box[0], box[1]))], INK, LW["frame"], None, "map_frame", 1))
        if not names:
            return
        lim = (X0, Y0, X0 + (box[2] - box[0]) * k, Y0 + (box[3] - box[1]) * k)
        for n_, nm, x, y in BRIDGES:                      # markers first, bridges then clashes
            place_marker(items, taken, lim, pg(F.local((x, y))), str(n_), BRIDGE_C, "bridge_numbers")
        for c_id, x, y, t in CLASHES:
            place_marker(items, taken, lim, pg(F.local((x, y))), c_id, CLASH_C, "clashes")
        for nid, nd in sorted((secs.get("nodes") or {}).items()):
            Q = [pg(F.local(p)) for p in nd.get("corners") or []]
            if len(Q) >= 3:
                Q.sort(key=lambda q: -q[1])
                place_text(B, items, taken, lim, [Q[0], Q[1], Q[2], Q[3]], nid, 2.6, NODE_C, "nodes", log)
        for sid, ab in sorted((secs.get("lines") or {}).items()):
            if len(ab) >= 2:
                place_text(B, items, taken, lim, [pg(F.local(ab[0])), pg(F.local(ab[1]))], sid, 1.8, CUT_C,
                           "section_cuts", log)
    draw_map(MAP_X, MAP_TOP - F.h * k, k, box, False, "overview")     # the overview: lines only
    X0, Y0 = MAP_X, MAP_TOP - F.h * k
    ki = 1000.0 / INSET_DEN
    INS_Y0 = 42.0
    items.append(("text", u"The site frame (site_alan) · bridges and clashes · 1:%s" % format(INSET_DEN, ",d"),
                  COL_X, INS_Y0 + (sbox[3] - sbox[1]) * ki + 3.0, 3.2, INK, True, "L", "inset", None, None))
    cb = _no_box(B["corner_block"](F, S, INSET_DEN, COL_X + (sbox[2] - sbox[0]) * ki, INS_Y0))
    taken.extend(_bbox(B, [t]) for t in cb)               # v2.8: markers keep off the inset's north arrow and scale
    draw_map(COL_X, INS_Y0, ki, sbox, True, "inset")
    items += cb
    log.append(u"inset: site frame %.0f x %.0f m at 1:%s, %.1f x %.1f mm; %d names and markers placed" % (
        sbox[2] - sbox[0], sbox[3] - sbox[1], format(INSET_DEN, ",d"), (sbox[2] - sbox[0]) * ki,
        (sbox[3] - sbox[1]) * ki, len(taken)))
    r_mk = 2.0                                            # mm: marker radius (the lists)

    def disc(x, y, txt, col, layer):
        marker(items, x, y, txt, col, layer)
    items += _no_box(B["corner_block"](F, S, den, X0 + F.w * k, Y0))   # v2.3: no background box
    # ---- title band
    items.append(("text", KICKER, 14.0, 287.0, 2.6, INK, True, "L", "title", None, None))
    items.append(("text", TITLE, 14.0, 276.5, 7.5, INK, True, "L", "title", None, None))
    yy = 284.0
    for ln in wrap(B, INTRO, 2.8, 196.0):
        items.append(("text", ln, COL_X, yy, 2.8, INK, False, "L", "title", None, None))
        yy -= 3.8
    items.append(("text", u"A  SITE AND STREAM EDGE   2", 406.0, 8.0, 2.6, INK, True, "R", "title", None, None))
    # ---- key under the map
    ky = Y0 - 6.0
    items.append(("text", u"Plan 01 · what is there today · 1:%s" % format(den, ",d"), MAP_X, ky, 2.6, INK, True, "L",
                  "key", None, None))
    ky -= 6.0
    rows1 = [("hdr", None, u"BUILDINGS · URBAN FABRIC (% of the site frame's built footprint)"),
             ("hdr", None, u"left swatch: no shop recorded; right: a shop, office or workshop on the plot (OSM, floor "
                           u"not recorded)"),
             ("hdr", None, u"(shops x%) = the part of that share with a shop")]
    for f_ in FAB_ORDER:
        if shares.get(f_, 0.0) > 0 or any(u["fab"] == f_ for u in units):
            pc = lambda v: (u"%.0f%%" % v) if v >= 0.5 else (u"< 1%" if v > 0 else u"0%")
            rows1.append(("box2", (FAB[f_], FAB_COM[f_]), u"%s · %s (shops %s)" % (FAB_WORDS[f_], pc(shares[f_]),
                                                                                  pc(com_sh[f_]))))
    mrg = []                                              # v2.6: one row per colour
    for kd, col, txt in MBL["mb_legend"](C, drawn, raw=True):
        hit = next((i_ for i_, r_ in enumerate(mrg) if r_[0] == kd and r_[1] == col), None)
        if hit is None:
            mrg.append((kd, col, txt))
        else:
            mrg[hit] = (kd, col, mrg[hit][2] + u" · " + txt)
    rows2 = [("hdr", None, u"GROUND AND GREEN")] + [r_ for r_ in mrg if u"(OSM)" not in r_[2] and r_[0] != "line"]
    rows2 += [("box", STREET_C, u"Streets (surveyed surface; OSM where the survey has none)"), ("box", WATER_C, u"The stream")]
    rows3 = [("hdr", None, u"LINES AND MARKS"),
             ("line", WALL_C, u"Walls (survey)"), ("line", HER_WALL, u"City walls"),
             ("line", STUDY_C, u"Study area (calisma_alan)"), ("line", INK, u"Analysis frame (site_alan)"),
             ("disc", BRIDGE_C, u"Bridge, upstream to downstream"), ("disc", CLASH_C, u"Where stream and town clash")]
    rows4 = [("hdr", None, u"AREAS AND RELIEF")] + [r_ for r_ in mrg if u"(OSM)" in r_[2] or r_[0] == "line"]
    cw = MAP_MAX_W / 4.0                                  # v2.6: four key columns
    for ci, rows in enumerate((rows1, rows2, rows4, rows3)):
        rows = [(k_, c_, MBL["mb_clean"](t_)) for k_, c_, t_ in rows]   # v2.9: no sources (wrapped clean)
        y_end = draw_rows(B, items, rows, MAP_X + ci * cw, ky, cw - 3.0, step=3.6, ts=2.4)
        if y_end < 33.0:                                  # v2.6: the credit starts at 30 mm
            log.append(u"FLAG key column %d runs into the credit (ends at %.1f mm, the credit at 30 mm)" % (ci + 1, y_end))
    log.append(CREDIT)                                    # v2.9: sources in the log only, never on the page
    # ---- right column: the land-use ring, the bridges, the clashes
    cy0 = 255.0
    items.append(("text", u"LAND USE AND GROUND COVER", COL_X, cy0, 3.2, INK, True, "L", "ring", None, None))
    items.append(("text", u"site frame (site_alan) · %% of its %.1f ha, counted on %.0f m cells" % (
        lu_tot / 1e4, AREA_CELL), COL_X, cy0 - 4.5, 2.4, "6E675E", False, "L", "ring", None, None))
    keep = [r_ for r_ in lu if r_[2] >= 0.005 * lu_tot]
    small = sum(r_[2] for r_ in lu if r_[2] < 0.005 * lu_tot)
    if small > 0:
        keep.append((u"Others, each under 0.5%", "C9C5BC", small))
    ccx, ccy, R1, R0 = COL_X + 32.0, cy0 - 40.0, 30.0, 18.0
    a0 = math.pi / 2.0
    for lab, col, a_ in keep:
        da = 2.0 * math.pi * a_ / lu_tot
        n_ = max(2, int(da / 0.05))
        outer = [(ccx + R1 * math.cos(a0 - da * t / n_), ccy + R1 * math.sin(a0 - da * t / n_)) for t in range(n_ + 1)]
        inner = [(ccx + R0 * math.cos(a0 - da * t / n_), ccy + R0 * math.sin(a0 - da * t / n_)) for t in range(n_, -1, -1)]
        items.append(("poly", [outer + inner], col, "FFFFFF", 0.2, None, "ring", 1, None, None))
        a0 -= da
    items.append(("text", u"%.1f" % (lu_tot / 1e4), ccx, ccy - 0.5, 6.0, INK, True, "C", "ring", None, None))
    items.append(("text", u"ha", ccx, ccy - 5.5, 2.8, "6E675E", False, "C", "ring", None, None))
    rk = [("box", col, u"%s %s" % (lab, (u"%.0f%%" % (100.0 * a_ / lu_tot)) if 100.0 * a_ / lu_tot >= 0.5 else u"< 1%"))
          for lab, col, a_ in keep]
    draw_rows(B, items, rk, COL_X + 70.0, cy0 - 10.0, COL_W - 70.0, step=4.2, ts=2.6)
    by = cy0 - 10.0 - 4.2 * len(rk) - 8.0
    by = min(by, ccy - R1 - 10.0)
    items.append(("text", u"BRIDGES · upstream to downstream", COL_X, by, 3.2, INK, True, "L", "lists", None, None))
    by -= 6.0
    for i_, (n_, nm, x, y) in enumerate(BRIDGES):
        cx_, cy_ = COL_X + (i_ % 2) * (COL_W / 2.0), by - (i_ // 2) * 5.5
        disc(cx_ + r_mk, cy_ + 0.9, str(n_), BRIDGE_C, "lists")
        items.append(("text", nm, cx_ + 2 * r_mk + 2.0, cy_, 2.8, INK, False, "L", "lists", None, None))
    by -= 5.5 * ((len(BRIDGES) + 1) // 2) + 6.0
    items.append(("text", u"WHERE STREAM AND TOWN CLASH", COL_X, by, 3.2, INK, True, "L", "lists", None, None))
    by -= 6.0
    for i_, (c_id, x, y, t) in enumerate(CLASHES):
        cx_, cy_ = COL_X + (i_ % 2) * (COL_W / 2.0), by - (i_ // 2) * 5.5
        disc(cx_ + r_mk, cy_ + 0.9, c_id, CLASH_C, "lists")
        items.append(("text", t, cx_ + 2 * r_mk + 2.0, cy_, 2.8, INK, False, "L", "lists", None, None))
    frame_check(B, items, frames, log)
    os.makedirs(OUT_DIR, exist_ok=True)
    name = u"Page02_What_is_there"
    items = [t[:1] + (MBL["mb_clean"](t[1]),) + t[2:] if t[0] == "text" else t for t in items]   # v2.9: no sources
    p = B["write_pdf"](os.path.join(OUT_DIR, name + u".pdf"), PAGE_W, PAGE_H, items, u"Page 02, " + TITLE, clips)
    log.append(B["out_line"](p, PAGE_W, PAGE_H, den, items, u""))
    try:                                                  # output/presentation/<slide>.pdf (Aras 14 Nov 11:22 UTC)
        _pc = {"__name__": "bergama_pages_common"}
        _pp = os.path.join(BERGAMA_ROOT, "Data", "bergama_pages_common.py")
        with open(_pp, encoding="utf-8") as _f:
            exec(compile(_f.read(), _pp, "exec"), _pc)
        # v2.10: no presentation copy here; Slide01 (bergama_slide01_v*.py) writes presentation/1.pdf (one A3 per slide)
        _pc["pc_review"](p, os.path.join(OUT_DIR, "review"), log)     # review PNGs (Aras 14 Nov 11:25 UTC)
    except Exception as _ex:
        log.append(u"FLAG review PNGs not written (%s: %s)" % (type(_ex).__name__, _ex))
    try:
        q = B["write_svg"](os.path.join(OUT_DIR, name + u".svg"), PAGE_W, PAGE_H, items, u"Page 02, " + TITLE, clips)
        log.append(u"%s  %s (a group per layer)" % (q, time.strftime("%H:%M:%S")))
    except Exception as e:
        log.append(u"FLAG %s.svg not written (%s: %s); the PDF is complete" % (name, type(e).__name__, e))
    flags = [l for l in log if l.startswith(u"FLAG")]
    return u"%s\n%s %s, %d FLAG line(s), %.1f s" % (u"\n".join(log), GH_LABEL, VERSION, len(flags), time.time() - t0)


R_MK = 2.0                         # mm: marker radius


MB_GLOB = os.path.join("scripts", "bergama_mapbase_v*.py")
MB_END = "\n# ================================================================ main\n"


def load_mb(log):
    """v2.5: the library part of the newest MapBase script (mb_load, mb_draw, mb_legend, MB_STYLE)"""
    found = glob.glob(os.path.join(BERGAMA_ROOT, MB_GLOB))
    if not found:
        raise RuntimeError(u"no %s: run Bergama.bat once (the kit copies MapBase), press MapBase, then this page"
                           % os.path.join(BERGAMA_ROOT, MB_GLOB))
    src_ = max(found, key=lambda p: [int(n) for n in re.findall(r"\d+", os.path.basename(p))])
    with open(src_, encoding="utf-8") as f:
        code = f.read()
    ns = {"__name__": "bergama_mapbase_lib"}
    exec(compile(code[:code.index(MB_END)], src_, "exec"), ns)
    ns["BERGAMA_ROOT"] = BERGAMA_ROOT
    log.append(u"base map: %s (%s %s)" % (src_, ns.get("GH_LABEL"), ns.get("VERSION")))
    return ns


def _no_box(it):
    """v2.3 (Aras 12:10 UTC "dont put a opaque background on scale and north sign"): corner_block without its white box"""
    return [t for t in it if not (t[0] == "poly" and t[2] == "FFFFFF" and t[3] is None)]


def marker(items, x, y, txt, col, layer):
    items.append(("poly", [[(x + R_MK * math.cos(a_ * math.pi / 12.0), y + R_MK * math.sin(a_ * math.pi / 12.0))
                            for a_ in range(24)]], col, "FFFFFF", 0.25, None, layer, 1, None, None))
    items.append(("text", txt, x, y - 0.95, 2.6, "FFFFFF", True, "C", layer, None, None))


def _bbox(B, its):
    """v2.8: page box (mm) round a list of items (text by its width and alignment)"""
    xs, ys = [], []
    for t in its:
        if t[0] == "text":
            w = B["text_w"](t[1], t[4], t[6])
            x0 = t[2] - (w if t[7] == "R" else w / 2.0 if t[7] == "C" else 0.0)
            xs += [x0, x0 + w]
            ys += [t[3], t[3] + t[4]]
        elif t[0] in ("poly", "line"):
            for q in ([q for R in t[1] for q in R] if t[0] == "poly" else t[1]):
                xs.append(q[0])
                ys.append(q[1])
    return (min(xs) - 0.5, min(ys) - 0.5, max(xs) + 0.5, max(ys) + 0.5)


def _free(bx, taken, lim):
    if bx[0] < lim[0] or bx[1] < lim[1] or bx[2] > lim[2] or bx[3] > lim[3]:
        return False
    return not any(bx[0] < t[2] and t[0] < bx[2] and bx[1] < t[3] and t[1] < bx[3] for t in taken)


def place_marker(items, taken, lim, p, txt, col, layer):
    """v2.2: a marker on its point, else at the nearest free spot round it (up to 9 mm), never on another"""
    r = R_MK + 0.3
    for d in (0.0, 4.6, 6.0, 7.5, 9.0):
        for j in range(1 if d == 0 else 12):
            a = j * math.pi / 6.0
            x, y = p[0] + d * math.cos(a), p[1] + d * math.sin(a)
            bx = (x - r, y - r, x + r, y + r)
            if _free(bx, taken, lim):
                taken.append(bx)
                marker(items, x, y, txt, col, layer)
                return
    x = min(max(p[0], lim[0] + r), lim[2] - r)           # v2.4: no free spot: on its point, pulled inside the frame
    y = min(max(p[1], lim[1] + r), lim[3] - r)
    taken.append((x - r, y - r, x + r, y + r))
    marker(items, x, y, txt, col, layer)


def place_text(B, items, taken, lim, anchors, txt, size, col, layer, log):
    """v2.2: a name beside the first of its anchor points (page mm) where it overlaps nothing placed; the anchors in
    turn, then further out; FLAG when none is free (set at the first anchor)"""
    w = B["text_w"](txt, size, True)
    for d in (0.8, 2.0, 3.5, 5.0):
        for p in anchors:
            for dx, dy in ((d, d * 0.3), (-d - w, d * 0.3), (-w / 2.0, d), (-w / 2.0, -d - size), (d, -d - size * 0.6),
                           (-d - w, -d - size * 0.6)):
                bx = (p[0] + dx - 0.2, p[1] + dy - 0.3, p[0] + dx + w + 0.2, p[1] + dy + size + 0.2)
                if _free(bx, taken, lim):
                    taken.append(bx)
                    items.append(("text", txt, p[0] + dx, p[1] + dy, size, col, True, "L", layer, None, None))
                    return
    p = anchors[0]
    log.append(u"FLAG inset: no free spot for %s: set at its point (it may touch another name)" % txt)
    x = min(max(p[0] + 0.8, lim[0] + 0.3), lim[2] - w - 0.3)   # v2.4: pulled inside the frame
    y = min(max(p[1] + 0.3, lim[1] + 0.4), lim[3] - size - 0.3)
    items.append(("text", txt, x, y, size, col, True, "L", layer, None, None))


MAP_MARKS = ("bridge_numbers", "clashes", "nodes", "section_cuts")


def frame_check(B, items, frames, log):
    """v2.4: FLAG any unclipped map mark (marker, name) whose box leaves every map frame (Aras 12:14 UTC)"""
    bad = []
    for t in items:
        if t[0] == "text" and t[8] in MAP_MARKS:
            w = B["text_w"](t[1], t[4], bool(t[6]))
            bx = (t[2], t[3], t[2] + w, t[3] + t[4])
        elif t[0] in ("poly", "line") and (t[6] if t[0] == "poly" else t[5]) in MAP_MARKS and \
                (t[9] if t[0] == "poly" else t[4]) is None:
            pts = [q for R_ in t[1] for q in R_] if t[0] == "poly" else t[1]
            bx = (min(q[0] for q in pts), min(q[1] for q in pts), max(q[0] for q in pts), max(q[1] for q in pts))
        else:
            continue
        if not any(fb[0] - 0.05 <= bx[0] and bx[2] <= fb[2] + 0.05 and fb[1] - 0.05 <= bx[1] and bx[3] <= fb[3] + 0.05
                   for cid, fb in frames):
            bad.append(t[1] if t[0] == "text" else t[6] if t[0] == "poly" else t[5])
    if bad:
        log.append(u"FLAG frame check: %d map mark(s) outside their frame: %s" % (len(bad), u", ".join(
            str(b_) for b_ in bad[:12])))
    else:
        log.append(u"frame check: every map layer is cut to its frame; all %d frame(s) clean" % len(frames))


def _survey_key(F, q):
    """the survey point (rounded to the cm, as the floor table's key) of a frame point"""
    qx, qy = q[0] + F.u0, q[1] + F.v0
    return (round(F.ca * qx + F.sa * qy, 2), round(-F.sa * qx + F.ca * qy, 2))


def wrap(B, text, size, width):
    out, line_ = [], u""
    for wd in text.split(u" "):
        if line_ and B["text_w"](line_ + u" " + wd, size) > width:
            out.append(line_)
            line_ = wd
        else:
            line_ = (line_ + u" " + wd).strip()
    if line_:
        out.append(line_)
    return out


def draw_rows(B, items, rows, x, y, width, step=4.0, ts=2.5):
    """legend rows from (x, y) down: ("hdr", None, text), ("box"|"line"|"disc", hex, text)"""
    for kind, col, txt in rows:
        if kind == "hdr":
            for ln in wrap(B, txt, ts, width):
                items.append(("text", ln, x, y, ts, INK, True, "L", "key", None, None))
                y -= step
            y -= 0.6
            continue
        if kind == "box2":                                # v2.3: two swatches (plain, with shops)
            for i_, c_ in enumerate(col):
                items.append(("poly", [[(x + 3.0 * i_, y - 0.4), (x + 3.0 * i_ + 2.6, y - 0.4), (x + 3.0 * i_ + 2.6, y + 2.4),
                                        (x + 3.0 * i_, y + 2.4)]], c_, mixh(c_, INK, P02_EDGE_DARK), P02_HAIR, None, "key",
                              1, None, None))
        elif kind == "box":
            items.append(("poly", [[(x, y - 0.4), (x + 5.0, y - 0.4), (x + 5.0, y + 2.4), (x, y + 2.4)]], col,
                          mixh(col, INK, P02_EDGE_DARK), P02_HAIR, None, "key", 1, None, None))
        elif kind == "line":
            items.append(("line", [(x, y + 1.0), (x + 5.0, y + 1.0)], col, 0.4, None, "key", 1))
        else:
            items.append(("poly", [[(x + 2.5 + 1.4 * math.cos(a_ * math.pi / 8.0), y + 1.0 + 1.4 * math.sin(a_ * math.pi / 8.0))
                                    for a_ in range(16)]], col, None, 0.0, None, "key", 1, None, None))
        for j_, ln in enumerate(wrap(B, txt, ts, width - 7.0)):
            items.append(("text", ln, x + 7.0, y - j_ * step, ts, INK, False, "L", "key", None, None))
            if j_:
                y -= step
        y -= step
    return y


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
