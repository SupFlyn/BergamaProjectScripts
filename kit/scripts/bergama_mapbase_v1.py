# -*- coding: utf-8 -*-
"""Bergama Group 6: MAPBASE v1 (14 Nov 2026): ONE base map for every map of the set. Rules: scripts/_template/SCRIPT_STANDARD.md.

What Aras asked (14 Nov 2026, 12:16-12:18 UTC): "please update all maps to include every detail, and top of the map,
data is missing please fill in that"; "create one script for base map"; "that base map should provide us the most up
to date satallite and whatever data we have"; "like you have done that before comparison with satallite imagery and
so on"; "create one map from that (outlines and etc.) and every map should use that"; "newer maps can keep how they
do look".

What it does: pressed once (after Basemap), it builds the whole context of the survey's extent ONCE and writes it to
cached/bergama_mapbase/mapbase.json in SURVEY metres. Every map script then loads this script as a library (the code
above "# ==== main") and draws the context with mb_draw() through its own page transform, in the default look
(MB_STYLE, the look of Page02) or its own (a style dict: "newer maps can keep how they do look").

The data (nothing invented; every shape is the survey, a data file of the kit or OpenStreetMap):
  BUILDINGS  survey closed outlines + heritage, OpenStreetMap footprints and 2023 satellite bodies behind the survey's
             open fronts (Basemap osm_houses, sat_houses), the by-eye check against the 1 Mar 2023 satellite image
             (Data/buildings_image_check.json: added / not drawn; PARTIAL, 22 of 36 pieces read on 13 Nov), the
             town-street trims; OpenStreetMap beyond the survey and wherever no drawn building overlaps a footprint.
             Each building carries its URBAN FABRIC type (fabric(): heritage, mosques, civic & industrial, blocks,
             old town, planned low-rise, small irregular, under construction) and a SHOP flag (an OSM shop, office,
             craft or trade amenity point inside it or within COM_NEAR m; OSM does not record the floor).
  GROUND     ESA WorldCover 2021 (10 m), the 2023 satellite land cover (Data/veg2023.json, 0.5 m: trees, grass, bare,
             in the image's box), OpenStreetMap areas (parks, sports grounds, school / hospital / mosque grounds, car
             parks, archaeological sites, cemeteries, grass, woods, fields, land-use zones, water), each with its name.
  STREETS    survey road surfaces (roads_survey.json) and town streets (streets_town.json) with their edge lines;
             OpenStreetMap streets and paths wherever the survey has no road line within MB_ROAD_CELL m.
  WATER      the Selinos (Basemap build_river), survey stream banks and ponds, OpenStreetMap waterways and water.
  WALLS      survey walls and heritage walls; OpenStreetMap walls, retaining walls and city walls where the survey has
             none near (the Acropolis hill).
  POINTS     OpenStreetMap trees and taxi stands.
  CONTOURS   Copernicus GLO-30 (a SURFACE model: roofs and tree tops included), 3 x 3 smoothed, every MB_CONTOUR m with
             an index line every MB_INDEX m; lattice points taken back to lon/lat by the file's linear fit and placed by
             the Basemap's to_survey (the fit alone is about 7 m off).
  roads_design.json is the PROPOSAL (Aras's design roads) and is not part of the existing base.

Library entry points (exec the code above the main line; see Page02 v2.5 for a caller):
  mb_load(log)                                -> C (the cache + WorldCover + satellite land cover), or None + FLAG
  mb_draw(C, items, T, k, lim, cid, style=None, layers=None)
        T(p) = page mm of a survey point; k = page mm per metre; lim = page box (x0, y0, x1, y1) to cull by;
        cid = the clip id the caller registers (clips[cid] = [[frame ring]]) so nothing passes the frame line.
        Appends Basemap-format items; returns {layer: count}.
  mb_legend(C, style=None, used=None)         -> [("box"|"line", hex, text)] of the ground and green drawn
  MB_STYLE                                    the default look (copy it, change entries, pass it as style)

Component: Rhino 8 > Grasshopper > Python 3 Script (the board builder places it from the cloud kit).
  input  run     Button (or the previous script's done text)
  output log / done   as every Bergama script
Reads  ~/Downloads/Bergama/scripts/bergama_basemap_v*.py              (the newest: the drawing code)
       ~/Downloads/Bergama/cached/bergama_basemap/basemap_layers.json  (the survey, written by Basemap: press it first)
       ~/Downloads/Bergama/Data/: bergama_osm.osm, bergama_landcover_worldcover2021.json, veg2023.json,
       bergama_dem_glo30.json, roads_survey.json, streets_town.json, houses_sat2023.json, buildings_image_check.json,
       selinos_centreline.json, bergama_style.json
Writes ~/Downloads/Bergama/cached/bergama_mapbase/mapbase.json (+ its OSM house caches)
       ~/Downloads/Bergama/logs/bergama_mapbase_log.txt
"""
import os, time, json, math, re, glob

# ---- SETTINGS ----
VERSION = "v1"
GH_LABEL = "MapBase"
OUT_FOLDER = "bergama_mapbase"
LOG_NAME = "bergama_mapbase_log.txt"
GH_INPUTS = {}
LIB_GLOB = os.path.join("scripts", "bergama_basemap_v*.py")
LIB_END = "# ================================================================ main"
LC_FILE = os.path.join("Data", "bergama_landcover_worldcover2021.json")
VEG_FILE = os.path.join("Data", "veg2023.json")
DEM_FILE = os.path.join("Data", "bergama_dem_glo30.json")
MB_FILE = "mapbase.json"
MARGIN_M = 15.0                    # m of paper round the survey's extent (as the site board's whole_frame)
BEYOND_CELL = 50.0                 # m: OSM buildings beyond the survey: no survey line in the cell or the 8 round it
MB_ROAD_CELL = 25.0                # m: an OSM street is drawn where no survey road line lies in its cell or the 8 round
MB_WALL_CELL = 25.0                # m: the same for OSM walls against survey walls
BEYOND_W = {"motorway": 10.0, "trunk": 9.0, "primary": 8.0, "secondary": 7.0, "tertiary": 6.0, "unclassified": 5.0,
            "residential": 5.0, "living_street": 4.0, "service": 3.5, "pedestrian": 4.0}   # m drawn (ours: OSM has none)
PATH_TAGS = ("track", "footway", "path", "steps", "cycleway", "bridleway")
MB_CONTOUR, MB_INDEX = 10.0, 50.0  # m: contour step and index step (the transit thread's ask, 14 Nov 12:18 UTC)
P02_HAIR = 0.09                    # mm: building outline and wall pen of the default look (Page02 v2.4)
P02_EDGE_DARK = 0.5                # a building outline = its fill mixed this far toward the ink

# colours (the round 9 hue table of the board set; FAB = building fabric, in its rank order)
INK = "2C2219"
PAPER = "F7F5EF"
# v2.3: three families, one hue each (heritage wine 352 deg, buildings umber 22 deg, civic & industrial violet 270 deg);
# the types are lightness steps (HSL S 0.50 / 0.25 / 0.25); FAB_COM = the same type with shops (hue +10, S 0.8, L +0.04)
FAB = {"monument": "732630", "sacred": "AC3949", "traditional": "4C392E", "block": "735645", "regular": "99725C",
       "selfbuilt": "AF8D79", "large": "6B5086", "construction": "C6AD9F"}
FAB_COM = {"monument": "A0120D", "sacred": "E71A13", "traditional": "814B0E", "block": "B86B14", "regular": "E78B23",
           "selfbuilt": "ECA351", "large": "9123C7", "construction": "F2C088"}
GROUND_C = "DCD6CB"                # v2.3: the map ground where WorldCover has no vegetation (built-up, bare)
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
    out = {"bld": [], "ways": [], "nodes": [], "shops": [], "pts": []}   # v2.3: shops = (x, y) of shop / office / craft points
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
        if tg.get("natural") == "tree" or tg.get("amenity") == "taxi":   # MapBase: trees and taxi stands
            out["pts"].append(B["to_survey"](*ll) + (tg,))
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



def _survey_key(F, q):
    """the survey point (rounded to the cm, as the floor table's key) of a frame point"""
    qx, qy = q[0] + F.u0, q[1] + F.v0
    return (round(F.ca * qx + F.sa * qy, 2), round(-F.sa * qx + F.ca * qy, 2))




# ================================================================ OpenStreetMap areas, walls, points (MapBase v1)
OSM_AREA_ORDER = ("landuse", "farm", "wood", "green", "cemetery", "archaeo", "grounds", "worship", "parking", "sport",
                  "park", "water")


def osm_area_class(tg):
    """(class, sub) of a closed OSM way that is an area, else None"""
    lu, le, am, na, hi = tg.get("landuse"), tg.get("leisure"), tg.get("amenity"), tg.get("natural"), tg.get("historic")
    if na == "water" or lu in ("reservoir", "basin") or tg.get("water"):
        return ("water", na or lu)
    if le in ("park", "garden"):
        return ("park", le)
    if le in ("pitch", "playground", "sports_centre", "stadium", "track", "swimming_pool"):
        return ("sport", le)
    if am in ("school", "college", "university", "kindergarten", "hospital", "clinic"):
        return ("grounds", am)
    if am == "place_of_worship":
        return ("worship", am)
    if am == "parking":
        return ("parking", am)
    if hi == "archaeological_site":
        return ("archaeo", hi)
    if lu == "cemetery" or am == "grave_yard":
        return ("cemetery", lu or am)
    if lu in ("grass", "flowerbed", "meadow", "village_green", "recreation_ground"):
        return ("green", lu)
    if lu == "forest" or na in ("wood", "scrub"):
        return ("wood", lu or na)
    if lu in ("farmland", "orchard", "vineyard", "farmyard", "allotments"):
        return ("farm", lu)
    if lu in ("residential", "commercial", "retail", "industrial", "military", "construction", "quarry", "railway"):
        return ("landuse", lu)
    return None


def _cells(L, keys, c):
    out = set()
    for key in keys:
        for cl, Q, a, b in L.get(key, []):
            for i in range(len(Q)):
                q = Q[i]
                out.add((int(q[0] // c), int(q[1] // c)))
                if i:                                     # long segments: their midpoints too
                    p = Q[i - 1]
                    n = int(math.hypot(q[0] - p[0], q[1] - p[1]) // c)
                    for t in range(1, n + 1):
                        out.add((int((p[0] + (q[0] - p[0]) * t / (n + 1.0)) // c),
                                 int((p[1] + (q[1] - p[1]) * t / (n + 1.0)) // c)))
    return out


def _runs(Q, ok):
    """the pieces of a polyline whose points pass ok()"""
    out, run = [], []
    for q in list(Q) + [None]:
        if q is not None and ok(q):
            run.append(q)
            continue
        if len(run) >= 2:
            out.append(run)
        run = []
    return out


# ================================================================ contours of the DEM
def contours(B, log):
    """[(points survey m, z, is_index)] of DEM_FILE: 3 x 3 mean, marching squares, joined into polylines"""
    src = os.path.join(BERGAMA_ROOT, DEM_FILE)
    if not os.path.isfile(src):
        log.append(u"FLAG contours: %s not found: no contours" % src)
        return []
    t0 = time.time()
    with open(src, encoding="utf-8") as f:
        J = json.load(f)
    nr, nc = int(J["rows"]), int(J["cols"])
    P = J["pts"]
    if len(P) != nr * nc:
        log.append(u"FLAG contours: %d points for %d x %d: not read" % (len(P), nr, nc))
        return []
    Z = [[P[r * nc + c][2] for c in range(nc)] for r in range(nr)]
    S = [[0.0] * nc for _ in range(nr)]
    for r in range(nr):
        for c in range(nc):
            v = [Z[rr][cc] for rr in (r - 1, r, r + 1) for cc in (c - 1, c, c + 1) if 0 <= rr < nr and 0 <= cc < nc]
            S[r][c] = sum(v) / len(v)
    x0, y0 = P[0][0], P[0][1]
    dx = (P[nc - 1][0] - x0) / float(nc - 1)
    dy = (P[(nr - 1) * nc][1] - y0) / float(nr - 1)
    m = re.search(r"x = ([\d.]+) \+ \(lon - ([\d.]+)\) \* (\d+), y = ([\d.]+) \+ \(lat - ([\d.]+)\) \* (\d+)", J.get("transform", ""))
    fx = (float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)), float(m.group(5)),
          float(m.group(6))) if m else None
    if fx is None:
        log.append(u"FLAG contours: the file's lon/lat fit not found: placed by the fit-free lattice (about 7 m off)")

    def place(rc):
        x, y = x0 + rc[1] * dx, y0 + rc[0] * dy
        if fx is None:
            return (x, y)
        lon = fx[1] + (x - fx[0]) / fx[2]
        lat = fx[4] + (y - fx[3]) / fx[5]
        return B["to_survey"](lon, lat)
    seg = {}
    for r in range(nr - 1):
        for c in range(nc - 1):
            a, b_, c_, d = S[r][c], S[r][c + 1], S[r + 1][c + 1], S[r + 1][c]
            lo, hi = min(a, b_, c_, d), max(a, b_, c_, d)
            lv = math.ceil(lo / MB_CONTOUR) * MB_CONTOUR
            while lv <= hi:
                l_ = lv + 1e-6
                pts = []
                for (p, zp), (q, zq) in ((((r, c), a), ((r, c + 1), b_)), (((r, c + 1), b_), ((r + 1, c + 1), c_)),
                                         (((r + 1, c + 1), c_), ((r + 1, c), d)), (((r + 1, c), d), ((r, c), a))):
                    if (zp - l_) * (zq - l_) < 0:
                        t = (l_ - zp) / (zq - zp)
                        pts.append((round(p[0] + (q[0] - p[0]) * t, 4), round(p[1] + (q[1] - p[1]) * t, 4)))
                if len(pts) == 2:
                    seg.setdefault(lv, []).append((pts[0], pts[1]))
                elif len(pts) == 4:
                    seg.setdefault(lv, []).extend([(pts[0], pts[1]), (pts[2], pts[3])])
                lv += MB_CONTOUR
    out = []
    for lv, S_ in seg.items():                            # join the cell pieces into polylines
        ends = {}
        for i, (p, q) in enumerate(S_):
            ends.setdefault(p, []).append(i)
            ends.setdefault(q, []).append(i)
        used = [False] * len(S_)
        for i in range(len(S_)):
            if used[i]:
                continue
            used[i] = True
            line = [S_[i][0], S_[i][1]]
            for end in (1, 0):
                while True:
                    tip = line[-1] if end else line[0]
                    nxt = next((j for j in ends.get(tip, ()) if not used[j]), None)
                    if nxt is None:
                        break
                    used[nxt] = True
                    p, q = S_[nxt]
                    new = q if p == tip else p
                    if end:
                        line.append(new)
                    else:
                        line.insert(0, new)
            out.append(([tuple(round(v, 1) for v in place(rc)) for rc in line], lv,
                        abs(lv / MB_INDEX - round(lv / MB_INDEX)) < 1e-6))
    log.append(u"contours: %d lines, %d index (every %.0f / %.0f m, Copernicus GLO-30 DSM, %.1f s)" % (
        len(out), sum(1 for o in out if o[2]), MB_CONTOUR, MB_INDEX, time.time() - t0))
    return out


# ================================================================ build (pressed once)
def build():
    t0 = time.time()
    log = []
    B = load_lib(log)
    if not os.path.isfile(B["CACHE_FILE"]):
        raise RuntimeError(u"%s not found: press Basemap once first (it reads the survey and writes this cache)"
                           % B["CACHE_FILE"])
    with open(B["CACHE_FILE"], encoding="utf-8") as f:
        D = json.load(f)
    FS, F = whole_frame(B, D)
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
    B["image_check"](L, F, log)                           # the 2023 satellite check (buildings_image_check.json)
    B["road_surface"](L, F, log)
    B["town_streets"](L, F, log)
    try:
        B["build_river"](L, F, log)
    except Exception as e:
        L["river"] = []
        log.append(u"FLAG river: not built (%s: %s): the stream is its survey lines only" % (type(e).__name__, e))
    O = read_osm(B, log)
    sv = lambda q: _to_survey(F, q)
    # ---- buildings (as Page02 v2.4)
    names = [(F.local((x, y)), t) for t, x, y, a_, kind in D.get("labels") or [] if kind != "street"]
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
    cov = set()
    c_ = BEYOND_CELL
    for key in ("buildings", "heritage", "walls", "road_edges", "kerbs", "sheds"):
        for cl, Q, a, b in L.get(key, []):
            for q in Q:
                cov.add((int(q[0] // c_), int(q[1] // c_)))

    def free(q):
        i, j = int(q[0] // c_), int(q[1] // c_)
        return not any((i + di, j + dj) in cov for di in (-1, 0, 1) for dj in (-1, 0, 1))
    inside = lambda q: 0 <= q[0] <= F.w and 0 <= q[1] <= F.h
    n_beyond = 0
    for P, tg in O["bld"]:
        Q = [F.local(p) for p in P]
        if not all(inside(q) for q in Q) or not all(free(q) for q in Q):
            continue
        A = abs(area(Q))
        if A < 2.0:
            continue
        units.append({"P": Q, "A": A, "fl": _levels(tg), "her": bool(tg.get("historic")), "src": "osm_beyond", "tags": tg})
        n_beyond += 1
    gU = {}
    for i_, u in enumerate(units):
        _grid_add(gU, i_, u["P"])

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
    n_fill = 0                                            # OSM footprints that overlap no drawn building
    for P, tg in O["bld"]:
        Q = [F.local(p) for p in P]
        if not all(inside(q) for q in Q):
            continue
        A = abs(area(Q))
        if A < 2.0:
            continue
        cq = (sum(q[0] for q in Q) / len(Q), sum(q[1] for q in Q) / len(Q))
        if owner(cq) is not None or any(owner(q) is not None for q in Q):
            continue
        bb = (min(q[0] for q in Q), min(q[1] for q in Q), max(q[0] for q in Q), max(q[1] for q in Q))
        near = set()
        for i in range(int(bb[0] // 25.0), int(bb[2] // 25.0) + 1):
            for j in range(int(bb[1] // 25.0), int(bb[3] // 25.0) + 1):
                near.update(gU.get((i, j), ()))
        if any(bb[0] <= v[0] <= bb[2] and bb[1] <= v[1] <= bb[3] and pip(v[0], v[1], Q) for i_ in near
               for v in units[i_]["P"]):
            continue
        units.append({"P": Q, "A": A, "fl": _levels(tg), "her": bool(tg.get("historic")), "src": "osm_fill", "tags": tg})
        _grid_add(gU, len(units) - 1, Q)
        n_fill += 1
    log.append(u"buildings: %s; OpenStreetMap beyond the survey %d, where no drawn building overlaps %d; %d with a "
               u"name text, %d with OSM tags" % (u", ".join(u"%s %d" % (s_, sum(1 for u in units if u["src"] == s_))
                                                            for s_ in ("buildings", "heritage", "osm_houses",
                                                                       "sat_houses")), n_beyond, n_fill, n_nm, n_tg))
    fabric(units, log)
    n_in = n_near = n_none = 0                            # shops
    for x, y in O["shops"]:
        q = F.local((x, y))
        if not inside(q):
            continue
        u = owner(q)
        if u is not None:
            u["com"] = True
            n_in += 1
            continue
        best, bd = None, COM_NEAR
        for i in range(int((q[0] - COM_NEAR) // 25.0), int((q[0] + COM_NEAR) // 25.0) + 1):
            for j in range(int((q[1] - COM_NEAR) // 25.0), int((q[1] + COM_NEAR) // 25.0) + 1):
                for i_ in gU.get((i, j), ()):
                    V = units[i_]["P"]
                    d = min(seg_d(q[0], q[1], V[m - 1], V[m]) for m in range(len(V)))
                    if d <= bd:
                        best, bd = units[i_], d
        if best is not None:
            best["com"] = True
            n_near += 1
        else:
            n_none += 1
    log.append(u"shops (OSM shop / office / craft places): %d inside a building, %d within %.0f m of one, %d with no "
               u"building near; buildings marked: %s" % (n_in, n_near, COM_NEAR, n_none, u", ".join(
                   u"%s %d" % (FAB_WORDS[f_], sum(1 for u in units if u["fab"] == f_ and u.get("com")))
                   for f_ in FAB_ORDER)))
    # ---- OSM streets, paths, waterways, walls where the survey has none near; OSM areas; points
    roads = _cells(L, ("road_edges", "kerbs", "town_edges", "road_net", "town_net"), MB_ROAD_CELL)
    walls = _cells(L, ("walls", "heritage_walls"), MB_WALL_CELL)
    rfree = lambda q: inside(q) and not any((int(q[0] // MB_ROAD_CELL) + di, int(q[1] // MB_ROAD_CELL) + dj) in roads
                                            for di in (-1, 0, 1) for dj in (-1, 0, 1))
    wfree = lambda q: inside(q) and not any((int(q[0] // MB_WALL_CELL) + di, int(q[1] // MB_WALL_CELL) + dj) in walls
                                            for di in (-1, 0, 1) for dj in (-1, 0, 1))
    ost, opa, owa, owl, ocw, areas = [], [], [], [], [], []
    for P, tg in O["ways"]:
        Q = [F.local(p) for p in P]
        hw = tg.get("highway")
        if hw and tg.get("area") != "yes" and (hw in BEYOND_W or hw in PATH_TAGS):
            for run in _runs(Q, rfree):
                (ost if hw in BEYOND_W else opa).append(([sv(q) for q in run], BEYOND_W.get(hw, 0.0), hw,
                                                          tg.get("name") or u""))
            continue
        if tg.get("waterway") in ("river", "stream", "canal", "ditch", "drain"):
            for run in _runs(Q, free):
                owa.append([sv(q) for q in run])
            continue
        if tg.get("historic") == "citywalls" or tg.get("barrier") == "city_wall":
            for run in _runs(Q, wfree):
                ocw.append([sv(q) for q in run])
            continue
        if tg.get("barrier") in ("wall", "retaining_wall"):
            for run in _runs(Q, wfree):
                owl.append([sv(q) for q in run])
            continue
        if len(P) >= 4 and P[0] == P[-1]:
            ac = osm_area_class(tg)
            if ac and any(inside(q) for q in Q):
                areas.append(([sv(q) for q in Q[:-1]], ac[0], ac[1], tg.get("name") or u""))
    trees, taxi = [], []
    for x, y, tg in O["pts"]:
        if not inside(F.local((x, y))):
            continue
        if tg.get("natural") == "tree":
            trees.append((round(x, 1), round(y, 1)))
        elif tg.get("amenity") == "taxi":
            taxi.append((round(x, 1), round(y, 1), tg.get("name") or u""))
    log.append(u"OpenStreetMap where the survey has none near: %d street pieces, %d paths, %d waterways, %d walls, "
               u"%d city-wall pieces; %d areas (%s); %d trees, %d taxi stands" % (
                   len(ost), len(opa), len(owa), len(owl), len(ocw), len(areas), u", ".join(
                       u"%s %d" % (c, sum(1 for a in areas if a[1] == c)) for c in OSM_AREA_ORDER), len(trees), len(taxi)))
    # ---- the cache, in survey m
    rd = lambda Q: [(round(p[0], 2), round(p[1], 2)) for p in (sv(q) for q in Q)]
    lay = lambda key: [[cl, rd(Q)] for cl, Q, a, b in L.get(key, [])]
    C = {"version": VERSION, "made": time.strftime("%Y-%m-%d %H:%M"), "frame": D.get("frame"),
         "extent": [rd([(0.0, 0.0), (F.w, 0.0), (F.w, F.h), (0.0, F.h)])],
         "bld": [[rd(u["P"]), u["fab"], 1 if u.get("com") else 0, u["src"], u.get("name") or u""] for u in units],
         "polys": {"streets": [rd(Q) for key in ("road_net", "town_net") for cl, Q, a, b in L.get(key, [])],
                   "river": [rd(Q) for cl, Q, a, b in L.get("river", [])],
                   "parks": [rd(Q) for cl, Q, a, b in L.get("parks", []) if cl and len(Q) >= 3]},
         "lines": dict([(key, lay(key)) for key in ("road_edges", "kerbs", "town_edges", "walls", "heritage_walls",
                                                    "stream_banks", "ponds", "bridges")]),
         "osm_streets": ost, "osm_paths": opa, "osm_waterways": owa, "osm_walls": owl, "osm_citywalls": ocw,
         "areas": areas, "trees": trees, "taxi": taxi, "contours": contours(B, log),
         "calisma": D.get("calisma") or []}
    os.makedirs(CACHE_DIR, exist_ok=True)
    p = os.path.join(CACHE_DIR, MB_FILE)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(C, f, ensure_ascii=False, separators=(",", ":"))
    log.append(u"%s  %.1f MB, %s" % (p, os.path.getsize(p) / 1e6, time.strftime("%H:%M:%S")))
    flags = [l for l in log if l.startswith(u"FLAG")]
    return u"%s\n%s %s, %d FLAG line(s), %.1f s" % (u"\n".join(log), GH_LABEL, VERSION, len(flags), time.time() - t0)


def _levels(tg):
    try:
        return int(float(tg.get("building:levels") or 0))
    except ValueError:
        return 0


def _grid_add(g, i_, P):
    bb = (min(q[0] for q in P), min(q[1] for q in P), max(q[0] for q in P), max(q[1] for q in P))
    for i in range(int(bb[0] // 25.0), int(bb[2] // 25.0) + 1):
        for j in range(int(bb[1] // 25.0), int(bb[3] // 25.0) + 1):
            g.setdefault((i, j), []).append(i_)


def _to_survey(F, q):
    """the survey point of a frame point (the inverse of Frame.local)"""
    qx, qy = q[0] + F.u0, q[1] + F.v0
    return (F.ca * qx + F.sa * qy, -F.sa * qx + F.ca * qy)


# ================================================================ library: load and draw
MB_STYLE = {
    "ground": GROUND_C, "lc": dict((k_, v[0]) for k_, v in LC.items()), "lc_light": LC_LIGHT,
    "veg": {"trees": LC["trees"][0], "grass": LC["grass"][0], "bare": "D6C7A6"},
    "areas": {"landuse": None, "farm": "C9C08A", "wood": "7F8C5A", "green": "B2BC8E", "cemetery": "A9B194",
              "archaeo": "E0C7A3", "grounds": "E8DEC8", "worship": "E6D2CB", "parking": "E3E0D8", "sport": "BCC896",
              "park": "9DB37A", "water": WATER_C},
    "landuse": {"industrial": "D8D3DF", "commercial": "EADFCF", "retail": "EADFCF", "military": "D6D3CB"},
    "street": STREET_C, "street_edge": STREET_EDGE, "path": STREET_EDGE, "water": WATER_C, "water_line": WATER_LINE,
    "wall": WALL_C, "her_wall": HER_WALL, "osm_wall": WALL_C, "bridge": INK, "tree": "5F6E3F",
    "contour": "9C927E", "contour_index": "7E7462",
    "fab": dict(FAB), "fab_com": dict(FAB_COM), "edge_dark": P02_EDGE_DARK, "ink": INK,
    "lw": {"hair": P02_HAIR, "edge": P02_HAIR, "path": P02_HAIR, "water": 0.25, "osm_water": 0.22, "wall": P02_HAIR,
           "her_wall": 0.3, "osm_wall": 0.07, "bridge": 0.3, "contour": 0.06, "contour_index": 0.13, "tree_r": 0.25},
    "grain": True}
MB_WORDS = {"ground": u"Built-up and bare ground (no WorldCover vegetation)", "farm": u"Fields & orchards (OSM)",
            "wood": u"Woods (OSM)", "green": u"Grass (OSM)", "cemetery": u"Cemeteries (OSM)",
            "archaeo": u"Archaeological sites (OSM)", "grounds": u"School & hospital grounds (OSM)",
            "worship": u"Mosque & church grounds (OSM)", "parking": u"Car parks (OSM)", "sport": u"Sports grounds (OSM)",
            "park": u"Parks & gardens (OSM)", "water": u"Water (OSM)", "veg_trees": u"Trees (2023 image)",
            "veg_grass": u"Grass (2023 image)", "veg_bare": u"Bare ground (2023 image)",
            "parks": u"Parks (survey)", "contour": u"Contours %.0f m, index %.0f m (GLO-30 surface)" % (MB_CONTOUR, MB_INDEX)}


def mb_load(log):
    """the MapBase cache + WorldCover + the 2023 satellite land cover (all survey m), or None (FLAG)"""
    p = os.path.join(BERGAMA_ROOT, "cached", "bergama_mapbase", MB_FILE)
    if not os.path.isfile(p):
        log.append(u"FLAG MapBase: %s not found: press MapBase once first; the map has no context" % p)
        return None
    with open(p, encoding="utf-8") as f:
        C = json.load(f)
    C["lc"], C["veg"] = {}, {}
    for key, fn in (("lc", LC_FILE), ("veg", VEG_FILE)):
        src = os.path.join(BERGAMA_ROOT, fn)
        if not os.path.isfile(src):
            log.append(u"FLAG MapBase: %s not found: drawn without it" % src)
            continue
        try:
            with open(src, encoding="utf-8") as f:
                J = json.load(f)
            C[key] = dict((k_, [R for R in v if len(R) >= 3]) for k_, v in (J.get("rings") or {}).items())
        except Exception as e:
            log.append(u"FLAG MapBase: %s not read (%s: %s)" % (src, type(e).__name__, e))
    log.append(u"MapBase %s of %s: %d buildings, %d OSM areas, %d contour lines" % (
        C.get("version"), C.get("made"), len(C["bld"]), len(C["areas"]), len(C["contours"])))
    return C


def mb_draw(C, items, T, k, lim, cid, style=None, layers=None):
    """the base map into items: survey m -> page mm by T, cut to lim (page box) and to the caller's clip cid.
    layers = None (all) or a set of: ground, lc, veg, areas, parks, contours, streets, water, walls, buildings,
    bridges, trees. Returns {layer: items added}"""
    st = dict(MB_STYLE)
    st.update(style or {})
    lw = dict(MB_STYLE["lw"])
    lw.update((style or {}).get("lw") or {})
    on = lambda key: layers is None or key in layers
    g = "~" if st.get("grain") else ""
    cnt = {}

    def pbox(Pp):
        return (min(q[0] for q in Pp), min(q[1] for q in Pp), max(q[0] for q in Pp), max(q[1] for q in Pp))

    def seen(b):
        return b[2] >= lim[0] and b[0] <= lim[2] and b[3] >= lim[1] and b[1] <= lim[3]

    def rings(Rs):
        out = []
        for R in Rs:
            Pp = [T(p) for p in R]
            if len(Pp) >= 3 and seen(pbox(Pp)):
                out.append(Pp)
        return out

    def poly(Rs, fill, layer):
        rr = rings(Rs)
        if rr and fill:
            items.append(("poly", rr, fill, None, 0.0, None, layer, 1, "eo", cid))
            cnt[layer] = cnt.get(layer, 0) + len(rr)

    def line(P, col, w, layer):
        Pp = [T(p) for p in P]
        if len(Pp) >= 2 and seen(pbox(Pp)):
            items.append(("line", Pp, col, w, cid, layer, 1))
            cnt[layer] = cnt.get(layer, 0) + 1
    light = lambda c: mixh(c, PAPER, st["lc_light"])
    if on("ground"):
        items.append(("poly", [[(lim[0], lim[1]), (lim[2], lim[1]), (lim[2], lim[3]), (lim[0], lim[3])]], st["ground"],
                      None, 0.0, None, "ground", 1, None, cid))
    if on("lc"):
        for k_ in LC_ORDER:
            poly(C["lc"].get(k_, []), g + light(st["lc"][k_]), "landcover_" + k_)
    if on("veg"):
        for k_ in ("bare", "grass", "trees"):
            poly(C["veg"].get(k_, []), g + light(st["veg"][k_]), "satellite_" + k_)
    if on("areas"):
        for c_ in OSM_AREA_ORDER:
            for R, cl, sub, nm in C["areas"]:
                if cl != c_:
                    continue
                col = st["landuse"].get(sub) if cl == "landuse" else st["areas"].get(cl)
                if col:
                    poly([R], col, "osm_" + cl)
    if on("parks"):
        poly(C["polys"].get("parks", []), g + light(st["areas"]["park"]), "parks")
    if on("contours"):
        for P, z, ix in C["contours"]:
            line(P, st["contour_index"] if ix else st["contour"], lw["contour_index"] if ix else lw["contour"],
                 "contours")
    if on("streets"):
        poly(C["polys"].get("streets", []), st["street"], "streets")
        for key in ("road_edges", "kerbs", "town_edges"):
            for cl, P in C["lines"].get(key, []):
                line(P + ([P[0]] if cl else []), st["street_edge"], lw["edge"], "street_edges")
        for P, w, hw, nm in C["osm_streets"]:
            line(P, st["street_edge"], w * k + 2 * lw["edge"], "streets_osm")
        for P, w, hw, nm in C["osm_streets"]:
            line(P, st["street"], w * k, "streets_osm")
        for P, w, hw, nm in C["osm_paths"]:
            line(P, st["path"], lw["path"], "paths_osm")
    if on("water"):
        poly(C["polys"].get("river", []), g + st["water"], "water")
        for key, w_ in (("stream_banks", lw["water"]), ("ponds", lw["water"] * 0.7)):
            for cl, P in C["lines"].get(key, []):
                line(P + ([P[0]] if cl else []), st["water_line"], w_, "water")
        for P in C["osm_waterways"]:
            line(P, st["water_line"], lw["osm_water"], "water")
    if on("walls"):
        for cl, P in C["lines"].get("walls", []):
            line(P, st["wall"], lw["wall"], "walls")
        for P in C["osm_walls"]:
            line(P, st["osm_wall"], lw["osm_wall"], "walls_osm")
        for cl, P in C["lines"].get("heritage_walls", []):
            line(P, st["her_wall"], lw["her_wall"], "heritage_walls")
        for P in C["osm_citywalls"]:
            line(P, st["her_wall"], lw["her_wall"], "heritage_walls")
    if on("buildings"):                                   # outlines at twice the pen, then fills (shared walls hidden)
        groups = {}
        for R, fab_, com, src, nm in C["bld"]:
            Pp = [T(p) for p in R]
            if len(Pp) < 3 or not seen(pbox(Pp)):
                continue
            col = (st["fab_com"] if com else st["fab"]).get(fab_, st["fab"].get("regular"))
            items.append(("line", Pp + [Pp[0]], mixh(col, st["ink"], st["edge_dark"]), 2 * lw["hair"], cid,
                          "buildings_outline", 1))
            groups.setdefault((fab_, com, col), []).append(Pp)
        for f_ in FAB_ORDER:
            for (fab_, com, col), rr in sorted(groups.items()):
                if fab_ != f_:
                    continue
                for i0 in range(0, len(rr), 400):
                    items.append(("poly", rr[i0:i0 + 400], col, None, 0.0, None,
                                  "buildings_" + fab_ + ("_shops" if com else ""), 1, None, cid))
                cnt["buildings"] = cnt.get("buildings", 0) + len(rr)
    if on("bridges"):
        for cl, P in C["lines"].get("bridges", []):
            line(P + ([P[0]] if cl else []), st["bridge"], lw["bridge"], "bridges")
    if on("trees"):
        r = lw["tree_r"]
        for x, y in C["trees"]:
            p = T((x, y))
            if lim[0] <= p[0] <= lim[2] and lim[1] <= p[1] <= lim[3]:
                items.append(("poly", [[(p[0] + r * math.cos(a * math.pi / 6.0), p[1] + r * math.sin(a * math.pi / 6.0))
                                        for a in range(12)]], st["tree"], None, 0.0, None, "trees_osm", 1, None, cid))
                cnt["trees_osm"] = cnt.get("trees_osm", 0) + 1
    return cnt


def mb_legend(C, cnt, style=None):
    """legend rows (kind, hex, text) of the ground, green, areas and contours that mb_draw drew (cnt = its return)"""
    st = dict(MB_STYLE)
    st.update(style or {})
    light = lambda c: mixh(c, PAPER, st["lc_light"])
    rows = [("box", st["ground"], MB_WORDS["ground"])]
    for k_ in ("trees", "orchard", "shrub", "grass", "farmland"):
        if cnt.get("landcover_" + k_):
            rows.append(("box", light(st["lc"][k_]), LC[k_][1] + u" (WorldCover)"))
    for k_ in ("trees", "grass", "bare"):
        if cnt.get("satellite_" + k_):
            rows.append(("box", light(st["veg"][k_]), MB_WORDS["veg_" + k_]))
    if cnt.get("parks"):
        rows.append(("box", light(st["areas"]["park"]), MB_WORDS["parks"]))
    for c_ in OSM_AREA_ORDER:
        if c_ != "landuse" and cnt.get("osm_" + c_):
            rows.append(("box", st["areas"][c_], MB_WORDS[c_]))
    if cnt.get("osm_landuse"):
        rows.append(("box", st["landuse"]["industrial"], u"Industrial / commercial zones (OSM)"))
    if cnt.get("contours"):
        rows.append(("line", st["contour_index"], MB_WORDS["contour"]))
    return rows


# ================================================================ main
main = build


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
