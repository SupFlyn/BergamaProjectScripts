# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE 02 "What is there, grain of the town" v1 (14 Nov 2026). Rules: scripts/_template/SCRIPT_STANDARD.md.
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
import os, time, json, math, re, glob

# ---- SETTINGS ----
VERSION = "v1"
GH_LABEL = "Page02"
OUT_FOLDER = "bergama_p02"
LOG_NAME = "bergama_p02_log.txt"
GH_INPUTS = {}
LIB_GLOB = os.path.join("scripts", "bergama_basemap_v*.py")
LIB_END = "# ================================================================ main"
LC_FILE = os.path.join("Data", "bergama_landcover_worldcover2021.json")

PAGE_W, PAGE_H = 420.0, 297.0      # mm, A3 landscape (the booklet page)
MAP_X, MAP_TOP = 14.0, 269.0       # mm: the map's left edge and top (the booklet's frame p02.1: x 14, y 28 from the top)
MAP_MAX_W, MAP_MAX_H = 194.0, 169.0   # mm: the room of frame p02.1
P02_DEN = 25000                    # the map's scale 1:n (as the booklet's plan 01); a frame too large takes the next step
DEN_STEPS = (25000, 30000, 40000, 50000)
COL_X, COL_W = 210.0, 196.0        # mm: the right column
MARGIN_M = 15.0                    # m of paper round the survey's extent (as the site board's whole_frame)

P02_HAIR = 0.05                    # mm: the one pen of every building outline and survey wall (1.25 m at 1:25,000)
P02_EDGE_DARK = 0.35               # a building outline = its fabric colour mixed this far toward the ink (ours)
BEYOND_CELL = 50.0                 # m: OpenStreetMap is drawn only where no survey line lies in its cell or the 8 round it
BEYOND_W = {"motorway": 10.0, "trunk": 9.0, "primary": 8.0, "secondary": 7.0, "tertiary": 6.0, "unclassified": 5.0,
            "residential": 5.0, "living_street": 4.0, "service": 3.5, "pedestrian": 4.0}   # m drawn (ours: OSM has none)
PATH_TAGS = ("track", "footway", "path", "steps", "cycleway", "bridleway")
AREA_CELL = 1.0                    # m: cells of the land-use count of the site frame

# colours (the round 9 hue table of the board set; FAB = building fabric, in its rank order)
INK = "2C2219"
PAPER = "F7F5EF"
FAB = {"monument": "AF7474", "sacred": "8B3A3F", "traditional": "4A3F35", "block": "7A6E60", "regular": "BCB794",
       "selfbuilt": "DCD5C2", "large": "A2B6B5", "construction": "E6E0C8"}
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
LC_LIGHT = 0.45                    # land cover mixed this far toward the paper on the map (the buildings read first)
STREET_C, STREET_EDGE = "E9E6DE", "B0AC9C"
WALL_C = "B0AC9C"
WATER_C, WATER_LINE = "91ADB4", "5D7F8D"
HER_WALL = "B08870"
BRIDGE_C, CLASH_C = "84573E", "8B3A3F"
STUDY_C = "6A4C93"

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
    out = {"bld": [], "ways": [], "nodes": []}
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
    for w in root.iter("way"):
        tg = dict((t.get("k"), t.get("v")) for t in w.findall("tag"))
        refs = [nd.get("ref") for nd in w.findall("nd")]
        P = [B["to_survey"](*nodes[r]) for r in refs if r in nodes]
        if len(P) < 2:
            continue
        if "building" in tg:
            if len(refs) >= 4 and refs[0] == refs[-1] and len(P) >= 4:
                out["bld"].append((P[:-1], tg))
            continue
        out["ways"].append((P, tg))
    log.append(u"OpenStreetMap: %d building footprints, %d other ways, %d tagged points" % (
        len(out["bld"]), len(out["ways"]), len(out["nodes"])))
    return out


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
    out.append((u"Other open ground", "D8D5CC", max(0.0, rest)))
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
    # floors of the survey's closed outlines (the cache lists them in the order of the closed items)
    fl_of = {}
    fls = (D.get("floors") or {}).get("buildings") or []
    j_ = 0
    for cl, P in D["layers"].get("buildings", []):
        if cl and len(P) >= 3:
            if j_ < len(fls):
                fl_of[(round(P[0][0], 2), round(P[0][1], 2))] = fls[j_]
            j_ += 1
    D["layers"].update(B["osm_houses"](D, F, log))        # houses behind the survey's open fronts (whole map)
    D["layers"].update(B["sat_houses"](D, F, log))
    L = B["localise"](D, F)
    B["image_check"](L, F, log)
    B["road_surface"](L, F, log)
    B["town_streets"](L, F, log)
    try:
        B["build_river"](L, F, log)
    except Exception as e:
        L["river"] = []
        log.append(u"FLAG river: not built on the whole map (%s: %s): the stream is drawn as its survey lines" % (
            type(e).__name__, e))
    box = (0.0, 0.0, F.w, F.h)
    loc = lambda p: F.local((float(p[0]), float(p[1])))
    O = read_osm(B, log)
    # ---- the buildings
    names = [(loc((x, y)), t) for t, x, y, a_, kind in D.get("labels") or [] if kind != "street"]
    units = []
    for key in ("buildings", "heritage", "osm_houses", "sat_houses"):
        for cl, Q, a, b in L.get(key, []):
            if not (cl and len(Q) >= 3):
                continue
            A = abs(area(Q))
            if A < 2.0:
                continue
            fl = fl_of.get(_survey_key(F, Q[0]), 0) if key == "buildings" else 0
            units.append({"P": Q, "A": A, "fl": fl, "her": key == "heritage", "src": key})
    # OpenStreetMap where the survey has no line work at all (the Acropolis hill ...)
    cov = set()
    c_ = BEYOND_CELL
    for key in ("buildings", "heritage", "walls", "road_edges", "kerbs", "sheds"):
        for cl, Q, a, b in L.get(key, []):
            for q in Q:
                cov.add((int(q[0] // c_), int(q[1] // c_)))

    def free(q):
        i, j = int(q[0] // c_), int(q[1] // c_)
        return not any((i + di, j + dj) in cov for di in (-1, 0, 1) for dj in (-1, 0, 1))
    n_beyond = 0
    for P, tg in O["bld"]:
        Q = [F.local(p) for p in P]
        if not all(0 <= q[0] <= F.w and 0 <= q[1] <= F.h for q in Q) or not all(free(q) for q in Q):
            continue
        A = abs(area(Q))
        if A < 2.0:
            continue
        lv = 0
        try:
            lv = int(float(tg.get("building:levels") or 0))
        except ValueError:
            lv = 0
        units.append({"P": Q, "A": A, "fl": lv, "her": bool(tg.get("historic")), "src": "osm_beyond", "tags": tg})
        n_beyond += 1
    # names and OSM tags for the survey's buildings (a name text or a tagged OSM point / footprint centre inside)
    gU = {}
    for i_, u in enumerate(units):
        bb = (min(q[0] for q in u["P"]), min(q[1] for q in u["P"]), max(q[0] for q in u["P"]), max(q[1] for q in u["P"]))
        for i in range(int(bb[0] // 25.0), int(bb[2] // 25.0) + 1):
            for j in range(int(bb[1] // 25.0), int(bb[3] // 25.0) + 1):
                gU.setdefault((i, j), []).append(i_)

    def owner(q):
        for i_ in gU.get((int(q[0] // 25.0), int(q[1] // 25.0)), ()):
            if pip(q[0], q[1], units[i_]["P"]):
                return units[i_]
        return None
    n_nm = n_tg = 0
    for q, t in names:
        u = owner(q)
        if u is not None and not u.get("name"):
            u["name"] = t
            n_nm += 1
    for x, y, tg in O["nodes"]:
        u = owner(F.local((x, y)))
        if u is not None and not u.get("tags"):
            u["tags"] = tg
            n_tg += 1
    for P, tg in O["bld"]:
        if len(tg) <= 1 and tg.get("building") in ("yes", None):
            continue
        Q = [F.local(p) for p in P]
        u = owner((sum(q[0] for q in Q) / len(Q), sum(q[1] for q in Q) / len(Q)))
        if u is not None and not u.get("tags"):
            u["tags"] = tg
            n_tg += 1
    log.append(u"buildings on the map: %s, OpenStreetMap beyond the survey %d; %d with a name text, %d with OSM tags" % (
        u", ".join(u"%s %d" % (s_, sum(1 for u in units if u["src"] == s_)) for s_ in ("buildings", "heritage",
                                                                                       "osm_houses", "sat_houses")),
        n_beyond, n_nm, n_tg))
    fabric(units, log)
    # ---- land cover (ESA WorldCover) in frame m
    lc = {}
    src = os.path.join(BERGAMA_ROOT, LC_FILE)
    if os.path.isfile(src):
        try:
            with open(src, encoding="utf-8") as f:
                J = json.load(f)
            for k_, rings in (J.get("rings") or {}).items():
                lc[k_] = [R for R in ([F.local(p) for p in R_] for R_ in rings) if len(R) >= 3]
            log.append(u"land cover: %s (%s)" % (u", ".join(u"%s %d" % (k_, len(v)) for k_, v in sorted(lc.items())),
                                                 os.path.basename(src)))
        except Exception as e:
            log.append(u"FLAG land cover: %s not read (%s: %s)" % (src, type(e).__name__, e))
    else:
        log.append(u"FLAG land cover: %s not found: the map shows no ground cover" % src)
    # ---- the land-use count of the site frame (site_alan, the analysis frame)
    sb = [F.local(p) for p in D["frame"]]
    sbox = (min(q[0] for q in sb), min(q[1] for q in sb), max(q[0] for q in sb), max(q[1] for q in sb))
    su = [u for u in units if sbox[0] <= u["cx"] <= sbox[2] and sbox[1] <= u["cy"] <= sbox[3]]
    lu, lu_tot = land_use(su, L, lc, sbox, log)
    bt = sum(u["A"] for u in su) or 1.0
    shares = dict((f_, 100.0 * sum(u["A"] for u in su if u["fab"] == f_) / bt) for f_ in FAB_ORDER)

    # ================================================================ the page
    items = []
    X0, Y0 = MAP_X, MAP_TOP - F.h * k

    def pg(q):
        return (X0 + q[0] * k, Y0 + q[1] * k)

    def poly(rings, fill, layer, stroke=None, lw=0.0):
        rr = [R for R in (B["clip_ring"](R_, box) for R_ in rings) if len(R) >= 3]
        if rr:
            items.append(("poly", [[pg(q) for q in R] for R in rr], fill, stroke, lw, None, layer, 1, "eo", None))

    def line(P, col, lw, layer):
        for run in B["clip_line"](P, box):
            if len(run) >= 2:
                items.append(("line", [pg(q) for q in run], col, lw, None, layer, 1))
    items.append(("poly", [[pg((0, 0)), pg((F.w, 0)), pg((F.w, F.h)), pg((0, F.h))]], PAPER, None, 0.0, None,
                  "map_paper", 1, None, None))
    for k_ in LC_ORDER:                                   # land cover, light, under everything
        for R in lc.get(k_, []):
            poly([R], "~" + mixh(LC[k_][0], PAPER, LC_LIGHT), "landcover_" + k_)
    poly([Q for key in ("road_net", "town_net") for cl, Q, a, b in L.get(key, [])], STREET_C, "streets")
    for key in ("road_edges", "kerbs", "town_edges"):
        for cl, Q, a, b in L.get(key, []):
            line(Q, STREET_EDGE, P02_HAIR, "street_edges")
    n_st = n_pa = 0                                       # OpenStreetMap streets and paths beyond the survey
    for P, tg in O["ways"]:
        hw = tg.get("highway")
        if not hw or tg.get("area") == "yes" or (hw not in BEYOND_W and hw not in PATH_TAGS):
            continue
        run = []
        Q = [F.local(p) for p in P]
        for q in Q + [None]:
            if q is not None and free(q):
                run.append(q)
                continue
            if len(run) >= 2:
                if hw in BEYOND_W:
                    line(run, STREET_EDGE, BEYOND_W[hw] * k + 2 * P02_HAIR, "streets_osm")
                    line(run, STREET_C, BEYOND_W[hw] * k, "streets_osm")
                    n_st += 1
                else:
                    line(run, STREET_EDGE, P02_HAIR, "paths_osm")
                    n_pa += 1
            run = []
    poly([Q for cl, Q, a, b in L.get("river", [])], "~" + WATER_C, "water")
    for key, w_ in (("stream_banks", 0.12), ("ponds", 0.08)):
        for cl, Q, a, b in L.get(key, []):
            line(Q + ([Q[0]] if cl else []), WATER_LINE, w_, "water")
    for P, tg in O["ways"]:                               # OpenStreetMap streams beyond the survey
        if tg.get("waterway") in ("river", "stream", "canal"):
            Q = [F.local(p) for p in P]
            run = []
            for q in Q + [None]:
                if q is not None and free(q):
                    run.append(q)
                    continue
                if len(run) >= 2:
                    line(run, WATER_LINE, 0.12, "water")
                run = []
    for key in ("walls",):                                # survey walls: one pale hairline (they were 0.16 dark ink)
        for cl, Q, a, b in L.get(key, []):
            line(Q, WALL_C, P02_HAIR, "walls")
    for cl, Q, a, b in L.get("heritage_walls", []):
        line(Q, HER_WALL, 0.12, "heritage_walls")
    for P, tg in O["ways"]:                               # city walls beyond the survey (OSM historic=citywalls)
        if tg.get("historic") == "citywalls" or tg.get("barrier") == "city_wall":
            Q = [F.local(p) for p in P]
            if all(free(q) for q in Q):
                line(Q, HER_WALL, 0.12, "heritage_walls")
    # buildings: every outline at twice the hairline first, every fill over them (shared walls covered)
    for u in units:
        col = FAB[u["fab"]]
        rr = B["clip_ring"](u["P"], box)
        if len(rr) >= 3:
            items.append(("line", [pg(q) for q in rr + [rr[0]]], mixh(col, INK, P02_EDGE_DARK), 2 * P02_HAIR, None,
                          "buildings_outline", 1))
    for f_ in FAB_ORDER:
        rr = [R for R in (B["clip_ring"](u["P"], box) for u in units if u["fab"] == f_) if len(R) >= 3]
        for i0 in range(0, len(rr), 400):
            items.append(("poly", [[pg(q) for q in R] for R in rr[i0:i0 + 400]], FAB[f_], None, 0.0, None,
                          "buildings_" + f_, 1, None, None))
    for cl, Q, a, b in L.get("bridges", []):
        line(Q, INK, 0.12, "bridges")
    for R in D.get("calisma") or []:                      # the study area
        Q = [F.local(p) for p in R]
        line(Q + [Q[0]], STUDY_C, 0.35, "study_area")
    sq = sb + [sb[0]]
    line(sq, INK, 0.12, "site_alan")
    items.append(("line", [pg((0, 0)), pg((F.w, 0)), pg((F.w, F.h)), pg((0, F.h)), pg((0, 0))], INK, 0.25, None,
                  "map_frame", 1))
    r_mk = 2.0                                            # mm: marker radius

    def disc(x, y, txt, col, layer):
        items.append(("poly", [[(x + r_mk * math.cos(a_ * math.pi / 12.0), y + r_mk * math.sin(a_ * math.pi / 12.0))
                                for a_ in range(24)]], col, "FFFFFF", 0.25, None, layer, 1, None, None))
        items.append(("text", txt, x, y - 0.95, 2.6, "FFFFFF", True, "C", layer, None, None))
    for n_, nm, x, y in BRIDGES:
        p = pg(F.local((x, y)))
        disc(p[0] - 3.2, p[1] + 3.2, str(n_), BRIDGE_C, "bridge_numbers")
    for c_id, x, y, t in CLASHES:
        p = pg(F.local((x, y)))
        disc(p[0] + 3.2, p[1] - 3.2, c_id, CLASH_C, "clashes")
    items += B["corner_block"](F, S, den, X0 + F.w * k, Y0)
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
    rows1 = [("hdr", None, u"BUILDINGS · URBAN FABRIC (share of the site frame's built footprint)")]
    for f_ in FAB_ORDER:
        if shares.get(f_, 0.0) > 0 or any(u["fab"] == f_ for u in units):
            rows1.append(("box", FAB[f_], u"%s · %s" % (FAB_WORDS[f_], (u"%.0f%%" % shares[f_]) if shares[f_] >= 0.5
                                                         else u"< 1%")))
    rows2 = [("hdr", None, u"GROUND AND GREEN")]
    rows2 += [("box", mixh(LC[k_][0], PAPER, LC_LIGHT), LC[k_][1]) for k_ in ("trees", "orchard", "shrub", "grass",
                                                                              "farmland") if lc.get(k_)]
    rows2 += [("box", STREET_C, u"Streets (surveyed surface; OSM beyond the survey)"), ("box", WATER_C, u"The stream")]
    rows3 = [("hdr", None, u"LINES AND MARKS"),
             ("line", WALL_C, u"Walls (survey)"), ("line", HER_WALL, u"City walls"),
             ("line", STUDY_C, u"Study area (calisma_alan)"), ("line", INK, u"Analysis frame (site_alan)"),
             ("disc", BRIDGE_C, u"Bridge, upstream to downstream"), ("disc", CLASH_C, u"Where stream and town clash")]
    cw = MAP_MAX_W / 3.0
    for ci, rows in enumerate((rows1, rows2, rows3)):
        draw_rows(B, items, rows, MAP_X + ci * cw, ky, cw - 3.0)
    ycr = 30.0
    for ln in wrap(B, CREDIT, 1.9, MAP_MAX_W):
        items.append(("text", ln, MAP_X, ycr, 1.9, "6E675E", False, "L", "credit", None, None))
        ycr -= 2.6
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
    log.append(u"OpenStreetMap beyond the survey (%.0f m cells free of survey lines): %d buildings, %d street pieces, "
               u"%d paths" % (BEYOND_CELL, n_beyond, n_st, n_pa))
    if not n_beyond:
        log.append(u"FLAG beyond the survey: no OpenStreetMap building drawn: the top left of the map stays land cover only")
    os.makedirs(OUT_DIR, exist_ok=True)
    name = u"Page02_What_is_there"
    p = B["write_pdf"](os.path.join(OUT_DIR, name + u".pdf"), PAGE_W, PAGE_H, items, u"Page 02, " + TITLE, None)
    log.append(B["out_line"](p, PAGE_W, PAGE_H, den, items, u""))
    try:
        q = B["write_svg"](os.path.join(OUT_DIR, name + u".svg"), PAGE_W, PAGE_H, items, u"Page 02, " + TITLE, None)
        log.append(u"%s  %s (a group per layer)" % (q, time.strftime("%H:%M:%S")))
    except Exception as e:
        log.append(u"FLAG %s.svg not written (%s: %s); the PDF is complete" % (name, type(e).__name__, e))
    flags = [l for l in log if l.startswith(u"FLAG")]
    return u"%s\n%s %s, %d FLAG line(s), %.1f s" % (u"\n".join(log), GH_LABEL, VERSION, len(flags), time.time() - t0)


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
        if kind == "box":
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
