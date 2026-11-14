# -*- coding: utf-8 -*-
"""Bergama Group 6: NODES COMMON v1 (14 Nov 2026): the shared parts of the six node page scripts
scripts/bergama_node_n1_v*.py ... bergama_node_n6_v*.py (Panel Review II slides 7-12, one script per node, Aras 14 Nov
11:14 UTC "dont build all those nodes into single script"). Loaded (not pasted) by each node script.

One A3 landscape page per node (420 x 297 mm, PDF with layers + review PNGs via pages_common pc_review). CHAINED, no
job done twice (Aras 14 Nov 12:38 UTC): Basemap -> MapBase -> Sections -> the node scripts.
  PLAN      the node frame (Data/section_lines.json "nodes") + NODE_MARGIN_M round it on its own axes; context = MapBase
            (mb_draw, its cache); over it the section lines, bus lines (quiet), stops, hubs, heritage loop, the
            streamside spine and stream walk (proposed paths), the city square idea (a loop stop and a bus stop in the
            same node) and V1; everything cut to the plan frame (FLAG on ink outside)
  SECTIONS  N#-A, N#-B from cached/bergama_sections/cuts.json (Sections v1.6.4+), the first cached scale that fits
  DIAGRAMS  land use of the node frame (Page02's land_use on MapBase data), water over the bed by season (cached levels)
  PLACEHOLDERS V1 perspective, program brief, building proposal (NO DRAWING rule: Aras makes them)
Reads the newest scripts/bergama_basemap_v*, bergama_p02_what_is_there_v*, bergama_sections_v*, bergama_mapbase_v*
(code only), Data/bergama_pages_common.py, section_lines.json, bergama_access_heritage.json and the caches above.
"""
import os, re, glob, json, math, time

NC_VERSION = "v9.5"   # v9.5: diagram levels run to the banks, N5 town band lower and label over its move; cuts packed from the top, why-here block follows, perspective room grows; V1 clear of stops, names and its arrows; v9.4: v9.4: at least 30 % (or 90 m) of a cut in view, so flat cuts get taller; v9.3: v9.3: section fit by the drawing without its sky, at least 55 % (or 150 m) of the cut in view, sky cut to the room; v9.2: v9.2 (fresh review of run 4): sections fill their rooms (cropped round the stream, own scale bar), no intro line, short key words, V1 in ink, land use = 5 classes + other with names on one row, program brief under the story, diagram arrows start at their cause, slots as voids, FLAG count includes carried FLAGs; v9.1: v9.1: diagrams to DIAGRAM_STYLE v2 (Niarchos measured: low ground, names under it, small accent); v9: v9: why-here diagrams redrawn on the shared diagram kit (pc_dg_kit, DIAGRAM_STYLE.md; Aras 21:30 UTC); v8.4: v8.4: scale + north above the plan (off his drawing), intro wording; v8.3: v8.3: B cut subtitle "along the bank", N3 diagram label clear of the dots; v8.2: v8.2: 4-corner picture rectangles of the masterplan left out (no solid green blocks), the river filled as water; v8.1: v8.1: masterplan sheet / texture frames (> 0.1 km2) left out, legend columns balanced, intro without the old levels text; v8: plan = his masterplan drawing; why-here story + one concept diagram per node; water bars and meets line gone; v7.5: v7.5: section_lines v2 (B along the bank: looks at the stream, no water bars); v7.4: v7.4: cut marks = two end arrows, no line between (pages_common v3.14); v7.3: v7.3: scale + north ignore the node frame line; v7.2: v7.2: the proposal from his masterplan SVG (MasterplanBase cache); v7.1: v7.1: R01 cut arrows (pc_cut_mark), no city-square ring, land-use columns >= 45 mm; v7: v7: every drawing fills its room on the A3 sheet, no 1:x printed (scale bars kept); v6.7: v6.7: no sources on the page (log only); v6.6: v6.6: scale + north to the emptiest plan corner; V1 also clear of link lines; v6.5: v6.5: V1 placed clear of labels; light backing behind plan labels; v6.4: v6.4: no repeats (R4 R5 R10): only the city-square stop, loop stops in the frame, no plant callouts; v6.3: v6.3: level marker stack (layer "levels") left out of the cuts; v6.2: v6.2: own section header (cached title block dropped), scales to 1:3000, land-use columns fit; v6.1: v6.1: cut items from cuts/<name>.json (Sections v1.6.5); v6: sections read from the Sections cache (cuts.json); v5   # v5: the plan context is the shared MapBase (mb_draw), Aras 12:17-12:18 UTC   # v4: brief plan rules (existing vs proposal, V1 viewpoint, program + building placeholders)   # v2: also output/presentation/<slide>.pdf (Aras 14 Nov 11:22 UTC)
ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
PAGE_W, PAGE_H = 420.0, 297.0
NODE_MARGIN_M = 25.0                       # m of town round the node frame on the plan
MP_MAX_M2 = 100000.0                 # m2: a bigger masterplan piece is a sheet / texture frame (v8.1)
PLAN_BOX = (14.0, 100.0, 200.0, 264.0)     # mm: x0, y0, x1, y1 of the plan's room
SEC_ROOMS = ((214.0, 192.0, 406.0, 286.0), (214.0, 102.0, 406.0, 186.0))   # v9.2: A up to the top (no intro line)   # mm: N#-A, N#-B
INK, GREY, RED = "2C2219", "6E675E", "8B2D2D"
OCC_LAYERS = ("node_frame", "bus_stops", "heritage_loop", "city_square", "section_names", "hubs", "viewpoints", "proposed_path")
# v8: his masterplan layer ids -> (existing?, the key's words); ids not here are drawn but not keyed
MP_WORDS = {"existing_buildings": (True, u"buildings"), "builts2": (True, u"buildings"),
            "existing_roads": (True, u"roads"), "heritage": (True, u"heritage"), "kizil_avlu": (True, u"heritage"),
            "su": (True, u"the Selinos"), "ana_su": (True, u"the Selinos"),
            "teras": (False, u"terraces stepping into the river"), "kanopi": (False, u"canopy, raised gathering place"),
            "iskele_kenari": (False, u"pier edges"), "normal": (False, u"walks"), "kopruler": (False, u"bridges"),
            "path": (False, u"paths"), "desings": (False, u"designed places"), "istinaat": (False, u"retaining walls"),
            "yeni": (False, u"cycle path"), "kesin_yesil": (False, u"new green"), "belki_yesil": (False, u"green, possible"),
            "su_bitkii": (False, u"water planting"), "yol_kenar": (False, u"street edges")}
LBL_LAYERS = ("bus_stops", "heritage_loop", "city_square", "section_names")   # v6.5: plan labels kept apart
SQUARE_C = "C07A2E"                        # the city-square ring (a contrast to the red loop and blue lines; ours)
CUT_C = "2C2219"


def _newest(pat):
    found = glob.glob(os.path.join(ROOT, "scripts", pat))
    if not found:
        raise RuntimeError(u"no scripts/%s in %s: run Bergama.bat once (the kit copies it)" % (pat, ROOT))
    return max(found, key=lambda p: [int(n) for n in re.findall(r"\d+", os.path.basename(p))])


def _exec(path, name):
    with open(path, encoding="utf-8") as f:
        code = f.read()
    ns = {"__name__": name}                   # no ghenv here: the script's Grasshopper block does not run
    exec(compile(code, path, "exec"), ns)
    return ns, code


def load_all(node, out_folder, log):
    """P = Page02's code (with B = the Basemap's), X = the Sections code, G = the pages common"""
    pp = _newest("bergama_p02_what_is_there_v*.py")
    P, _ = _exec(pp, "bergama_p02_lib")
    B = P["load_lib"](log)
    cdir = os.path.join(ROOT, "cached", out_folder)
    os.makedirs(cdir, exist_ok=True)
    B["HOUSE_FILE"] = os.path.join(cdir, "osm_houses_node.json")     # its own: the caches are made per frame
    B["STREET_FILE"] = os.path.join(cdir, "streets_node.json")
    log.append(u"page code: %s (%s %s)" % (pp, P.get("GH_LABEL"), P.get("VERSION")))
    xp = _newest("bergama_sections_v*.py")
    X, xcode = _exec(xp, "bergama_sections_lib")
    X["OUT_DIR"] = os.path.join(ROOT, "output", out_folder)
    X["CACHE_DIR"] = cdir
    log.append(u"section code: %s (%s %s)" % (xp, X.get("GH_LABEL"), X.get("VERSION")))
    X["write_pdf_node"] = _writer(X, xcode, log)
    gp = os.path.join(ROOT, "Data", "bergama_pages_common.py")
    G, _ = _exec(gp, "bergama_pages_common")
    G["PC_STATE"]["to_survey"] = B["to_survey"]
    with open(os.path.join(ROOT, "Data", "section_lines.json"), encoding="utf-8") as f:
        SL = json.load(f)
    if node not in SL["nodes"]:
        raise RuntimeError(u"%s is not in Data/section_lines.json" % node)
    D = G["pc_data"](log)
    return P, B, X, G, SL, D


def _writer(X, code, log):
    """the Sections PDF writer (it places the people cutouts), taught two things of the plan: "~" fills (drawn plain:
    this writer has no paper grain) and even-odd rings ("eo", holes stay open)"""
    a = code.index("def write_pdf(")
    b = code.index("\n\n\n", a)
    src = code[a:b].replace("def write_pdf(", "def write_pdf_node(", 1)
    old1 = "rings, fill, stroke, lw, dash, _ly, join, stripes, alpha = it[1:10]"
    old2 = 'A.append("B" if (fill and stroke) else "f" if fill else "S")'
    if old1 not in src or old2 not in src:
        log.append(u"FLAG the Sections writer changed: plan fills with holes may print filled")
        return X["write_pdf"]
    pad = src[:src.index(old1)].rsplit("\n", 1)[1]
    src = src.replace(old1, old1 + "\n" + pad + "eo = stripes == 'eo'\n" + pad +
                      "fill = fill.lstrip('~')[:6] if fill else fill\n" + pad +
                      "alpha = alpha if isinstance(alpha, (int, float)) else None\n" + pad +
                      "dash = dash if isinstance(dash, (list, tuple)) else None", 1)
    src = src.replace(old2, 'A.append(("B*" if eo else "B") if (fill and stroke) else ("f*" if eo else "f") if fill '
                            'else "S")', 1)
    exec(compile(src, "write_pdf_node", "exec"), X)
    return X["write_pdf_node"]


class Cut(object):
    """v6: one cached cut (cached/bergama_sections/cuts.json) with its line ends: what the page needs of it"""

    def __init__(self, name, ab, J, CL):
        self.name, self.J = name, J
        self.A, self.B = tuple(ab[0]), tuple(ab[1])
        self.L = math.hypot(self.B[0] - self.A[0], self.B[1] - self.A[1])
        J = J or {}
        self.z_th, self.window = J.get("z_th", 0.0), tuple(J.get("window") or (0.0, self.L))
        self.levels = {}
        for k_, v in (J.get("levels") or {}).items():
            if u"|" in k_:
                sea, q = k_.split(u"|")
                k_ = (sea, float(q))
            self.levels[k_] = tuple(v)
        self.bld, self.roads, self.trees = J.get("bld", []), J.get("roads", []), J.get("trees", [])
        sc = None
        for a, b in zip(CL[:-1], CL[1:]):                 # where the line crosses the Selinos centreline
            d = (self.B[0] - self.A[0]) * (b[1] - a[1]) - (self.B[1] - self.A[1]) * (b[0] - a[0])
            if abs(d) < 1e-12:
                continue
            t = ((a[0] - self.A[0]) * (b[1] - a[1]) - (a[1] - self.A[1]) * (b[0] - a[0])) / d
            u = ((a[0] - self.A[0]) * (self.B[1] - self.A[1]) - (a[1] - self.A[1]) * (self.B[0] - self.A[0])) / d
            if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0 and (sc is None or t < sc):
                sc = t
        self.crosses = sc is not None                     # v7.5: section_lines v2: B runs along the bank
        self.s_th = (sc if sc is not None else 0.5) * self.L

    def xy(self, s):
        return (self.A[0] + (self.B[0] - self.A[0]) * s / self.L, self.A[1] + (self.B[1] - self.A[1]) * s / self.L)


# ================================================================ v8: why each node (Aras 16:30-16:32 UTC)
# the text of /mnt/project-files/node_slides/node_stories_v1.md (sources and tags stay there and in the log)
STORY = {
    "N1": (u"One stream, two neighbourhoods", (
        u"The largest free ground on the site: pieces A, B and C, 11,616 m2.",
        u"No hub and no heritage stop: only the village buses 831-833 stop here.",
        u"Our move: a neighbourhood house in the west park that reaches both banks.")),
    "N2": (u"1,800 years of one crossing", (
        u"A Roman bridge of the 2nd-3rd century AD, repaired by the Ottomans, named after Ulu Cami (1398-99) for "
        u"standing in front of it. Tabaklar Hamami and the tanners by the stream.",
        u"Hub K4, heritage stop 4 and the village buses meet here; the Q100 and Q500 floods rise above the bank.",
        u"Our move: terraces stepping into the river upstream of the bridge; the bank road split into a ramp and "
        u"seating.")),
    "N3": (u"The bazaar walks over its river", (
        u"Tabak Köprüsü is Roman; the arasta and hamam date from 1513; the tanners named the stream Tabakhane Deresi.",
        u"Here the stream goes under the town for 234 m, mostly in the Roman tunnels of the Red Hall: it stays covered.",
        u"Hub K3, half of transit hub T, heritage stops 3 and 5. Our move: a market hall, a bus arrival corner and the "
        u"hidden stream marked on the surface.")),
    "N4": (u"The temple that stands on the river", (
        u"Under Hadrian (AD 117-138) the Red Hall was built over the Selinos on twin tunnels that still carry it.",
        u"Heritage stop 2, half of transit hub T and K5 at the edge.",
        u"Our move: people gather where the stream leaves the tunnels, a route on top runs to Üç Kemer, and a raised "
        u"platform stands above the flood.")),
    "N5": (u"The bank as the front yard", (
        u"Free pieces D and E, 5,768 m2; houses turn their backs to the stream.",
        u"The town buses 651-653 and 656 and the village buses 831-833 stop here.",
        u"Our move: a small day-care and sports pavilion on the dry top, terraces down to the water.")),
    "N6": (u"The door to the town", (
        u"The only node where regional buses stop: 643, 644, 836 and 936. K6 is the gateway hub.",
        u"Our move: a workers hall and a research centre lifted on the dry top, facing the arrival.")),
}
DG_INK, DG_GREY, DG_WATER = "1E1E1E", "C9C6BF", "A2B6B5"


def concept(node, items, x0, y0, W, H, G=None):
    """v9.1 (DIAGRAM_STYLE v2, measured on RPBW's Niarchos sketch): the node's one claim as a long low strip in a W x H
    mm box at (x0, y0), drawn with the shared kit (pages_common pc_dg_kit): the ground low (about 70 % air above),
    3 x heavier than every other line, with poché; the town one low band on it; the driver at the frame edge; our
    move the only accent and small; names under the ground on hairline brackets; one accent label in the air.
    Shapes are diagrams, not to scale; the names come from the node's story."""
    K = G["pc_dg_kit"](items, x0, y0, W, H, "concept", dash_at=4)   # nodes write with the Sections writer
    lab, br = K["label"], K["bracket"]

    def lvl(y, xa, xb):                                   # v9.5: a named level continued over the flooded width
        K["line"]([(xa, y), (xb, y)], K["C"]["water_ln"], K["W"]["hair"] * 2, (1.4, 0.9))
    if node == "N1":                                      # one stream, two neighbourhoods: a garden deck joins them
        g = [(0, 10), (68, 7), (82, 2.5), (110, 2.5), (124, 7), (192, 10)]
        K["ground"](g)
        K["water"](82, 110, 0.8, 3.4)
        K["city"](g, 14, 64, step=3.4, h=1.6, focus=96)
        K["city"](g, 128, 188, step=3.4, h=1.6, focus=96)
        K["steps"](64, 82, 8.6, 3.4, 4, base=2.5)
        K["steps"](128, 110, 8.6, 3.4, 4, base=2.5)
        K["move"]([(70, 13.0), (122, 13.0), (122, 14.3), (70, 14.3)])
        for x in (74, 118):
            K["line"]([(x, 7.0), (x, 13.0)], K["C"]["move"], K["W"]["move"])
        K["people"]([84, 90, 97, 104], 14.3)
        K["road"](0, 10.2, 11.0)
        K["arrow"]((4.0, 16.0), (20.0, 11.6), "bus")
        lab(u"one garden across the stream", 96, 19.5, True, "C")
        br(0, 12, -0.6, u"VILLAGE BUSES")
        br(16, 64, -0.6, u"UPPER")
        br(128, 188, -0.6, u"LOWER")
    elif node == "N2":                                    # 1,800 years of one crossing: terraces step into the river
        g = [(0, 9), (62, 9), (102, 2.5), (192, 2.5)]
        K["ground"](g)
        K["water"](100, 192, 0.8, 3.4, [(5.6, u"WINTER")])
        lvl(5.6, 62 + (9 - 5.6) / 6.5 * 40, 100)          # v9.5: the level runs on to where it meets the bank
        K["city"](g, 2, 14, step=3.4, h=1.6, focus=80)
        K["silhouette"]("mosque", 27, 9, 0.85)
        K["silhouette"]("minaret", 38, 9, 0.9)
        K["silhouette"]("dome", 52, 9, 0.7)
        K["steps"](62, 102, 9, 2.5, 6, base=2.5)
        K["people"]([72, 80, 88], 7.0)
        K["arrow"]((56.0, 10.6), (68.0, 9.4), "people")
        K["silhouette"]("arches", 146, 2.5, 2.2)
        lab(u"terraces into the river", 84, 19.0, True, "C")
        br(15, 42, -0.6, u"ULU CAMI")
        br(46, 58, -0.6, u"HAMAM")
        br(128, 164, -0.6, u"ROMAN BRIDGE")
    elif node == "N3":                                    # the bazaar walks over its river: slots open the hidden stream
        g = [(0, 2.5), (14, 2.5), (18, 9), (174, 9), (178, 2.5), (192, 2.5)]
        K["ground"](g)
        K["water"](0, 16, 0.8, 2.2)
        K["water"](176, 192, 0.8, 2.2)
        K["poly"]([(16, 2.2), (176, 2.2), (176, 5.0), (16, 5.0)], K["C"]["water"])
        K["city"](g, 22, 172, step=3.0, h=1.6, focus=96, roof=False)
        for x in (54, 82, 110, 138):                      # v9.2: slots are voids cut through the plate, accent edged
            K["poly"]([(x - 1.6, 5.0), (x + 1.6, 5.0), (x + 1.6, 9.0), (x - 1.6, 9.0)], "FFFFFF")
            for xe in (x - 1.6, x + 1.6):
                K["line"]([(xe, 5.0), (xe, 9.4)], K["C"]["move"], 0.45)
            K["arrow"]((x, 13.5), (x, 6.0), "water")
        K["people"]([58, 86, 114], 9.4)
        K["road"](188, 2.6, 11.0)
        K["arrow"]((187.0, 14.0), (179.5, 4.2), "bus")
        lab(u"slots to the water below", 96, 17.0, True, "C")
        br(0, 16, -0.6, u"TABAK KÖPRÜSÜ")
        br(20, 172, -0.6, u"THE STREAM UNDER THE TOWN · 234 M")
        br(178, 192, -0.6, u"BUSES")
    elif node == "N4":                                    # the temple that stands on the river
        g = [(0, 9), (124, 9), (130, 2.5), (192, 2.5)]
        K["ground"](g)
        K["water"](128, 174, 0.8, 3.4, [(6.2, u"Q500")])
        K["water"](174, 192, 0.8, 3.4)
        lvl(6.2, 124 + (9 - 6.2) / 6.5 * 6, 128)          # v9.5: Q500 across the whole flooded width
        lvl(6.2, 174, 192)
        for xa in (70, 96):                               # the twin tunnels under the hall, the stream inside
            arch = [(xa, 0.6)] + [(xa + 11 - 11 * math.cos(math.radians(a)), 0.6 + 5.2 * math.sin(math.radians(a)))
                                  for a in range(0, 181, 12)] + [(xa + 22, 0.6)]
            K["poly"](arch, K["C"]["water"], K["C"]["ink"], K["W"]["thin"])
        K["city"](g, 4, 58, step=3.4, h=1.6, focus=150)
        K["silhouette"]("basilica", 92, 9, 0.75)
        K["steps"](120, 136, 9, 2.5, 4, base=2.5)
        K["people"]([126, 132], 5.8)
        K["move"]([(142, 16.0), (172, 16.0), (172, 17.3), (142, 17.3)])
        for x in (146, 157, 168):
            K["line"]([(x, 3.4), (x, 16.0)], K["C"]["move"], K["W"]["move"])
        K["people"]([148, 155, 162], 17.3)
        K["silhouette"]("arches", 184, 2.5, 1.0)
        K["arrow"]((172.5, 17.6), (179.5, 7.6), "people")
        lab(u"raised gathering", 150, 22.5, True, "C")
        br(80, 104, -0.6, u"RED HALL")
        br(118, 138, -0.6, u"TUNNEL MOUTH")
        br(176, 192, -0.6, u"ÜÇ KEMER")
    elif node == "N5":                                    # the bank as the front yard
        g = [(0, 9), (124, 9), (146, 2.5), (192, 2.5)]
        K["ground"](g)
        K["water"](142, 192, 0.8, 3.4)
        K["city"](g, 8, 116, step=7.2, h=1.8, focus=124)   # v9.5: the town band stays low (STYLE v2)
        K["line"]([(119, 9), (119, 12.0)], K["C"]["ink"], K["W"]["thin"] * 2)
        K["move"]([(124, 9), (134, 9), (134, 12.6), (124, 12.6)])
        K["steps"](134, 148, 9, 2.5, 4, base=2.5)
        K["people"]([138, 142, 146], 5.8)
        K["arrow"]((110.0, 10.4), (123.0, 11.6), "people")
        K["road"](0, 9.2, 11.0)
        K["arrow"]((4.0, 15.0), (18.0, 10.4), "bus")
        lab(u"front yard to the water", 136, 15.5, True, "C")   # v9.5: over its move
        br(0, 6, -0.6, u"BUSES")
        br(10, 116, -0.6, u"HOUSES TURN THEIR BACKS TO THE STREAM")
        br(124, 150, -0.6, u"THE BANK")
    elif node == "N6":                                    # the door to the town
        g = [(0, 9), (106, 9), (118, 2.5), (150, 2.5), (160, 9), (192, 9)]
        K["ground"](g)
        K["water"](116, 152, 0.8, 3.4)
        for i in range(4):                                # the sheds: one low saw-tooth band
            xa = 4 + i * 17.0
            K["poly"]([(xa, 9), (xa + 15, 9), (xa + 15, 10.6), (xa + 7.5, 11.6), (xa + 7.5, 10.6), (xa, 11.6)],
                      K["C"]["ctx"])
        K["poly"]([(106, 9.0), (160, 9.0), (160, 10.0), (106, 10.0)], "FFFFFF", K["C"]["ink"], 0.3)   # road bridge
        for x in (128, 140):
            K["line"]([(x, 2.5), (x, 9.0)], K["C"]["ink"], 0.3)
        K["road"](188, 9.2, 11.0)
        K["arrow"]((186.0, 12.0), (162.0, 12.0), "bus")
        K["move"]([(80, 14.0), (104, 14.0), (104, 15.4), (80, 15.4)])
        for x in (84, 100):
            K["line"]([(x, 9), (x, 14.0)], K["C"]["move"], K["W"]["move"])
        K["people"]([87, 93, 99], 15.4)
        K["arrow"]((112.0, 10.4), (105.0, 13.6), "people")
        lab(u"lifted, facing the arrival", 92, 21.0, True, "C")
        br(4, 72, -0.6, u"SHEDS")
        br(108, 160, -0.6, u"ROAD BRIDGE")
        br(164, 192, -0.6, u"REGIONAL BUSES")
    if node in ("N1", "N2", "N3", "N4", "N5", "N6"):     # v9.2: the one heavy line runs whole, over water and moves
        K["line"](g, K["C"]["ink"], K["W"]["cut"])


# ================================================================ small helpers (page mm)
def T_(s, x, y, size, col=INK, bold=False, align="L", layer="text"):
    return ("text", s, x, y, size, col, bold, align, layer, None, None)


def L_(pts, col, lw, layer, dash=None):
    return ("line", [tuple(p) for p in pts], col, lw, list(dash) if dash else None, layer, 1)


def R_(rings, fill, stroke, lw, layer, eo=False):
    return ("poly", [[tuple(p) for p in r] for r in rings], fill, stroke, lw, None, layer, 1, "eo" if eo else None,
            None)


def ring(cx, cy, r, n=48):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def box(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def wrap(B, s, size, width, bold=False):
    out, ln = [], u""
    for wd in s.split(u" "):
        if ln and B["text_w"](ln + u" " + wd, size, bold) > width:
            out.append(ln)
            ln = wd
        else:
            ln = (ln + u" " + wd).strip()
    if ln:
        out.append(ln)
    return out


def para(B, items, s, x, y, size, width, col=INK, bold=False, step=None, layer="text"):
    for ln in wrap(B, s, size, width, bold):
        items.append(T_(ln, x, y, size, col, bold, "L", layer))
        y -= step or size * 1.4
    return y


def scale_items(items, f, ox, oy, dx, dy):
    """items scaled by f about (ox, oy), then moved by (dx, dy): points, radii, text and image sizes"""
    S = lambda p: (ox + (p[0] - ox) * f + dx, oy + (p[1] - oy) * f + dy)
    out = []
    for it in items:
        t = it[0]
        if t == "poly":
            out.append((t, [[S(p) for p in r] for r in it[1]]) + tuple(it[2:]))
        elif t == "line":
            out.append((t, [S(p) for p in it[1]]) + tuple(it[2:]))
        elif t == "circle":
            q = S((it[1], it[2]))
            out.append((t, q[0], q[1], it[3] * f) + tuple(it[4:]))
        elif t == "text":
            q = S((it[2], it[3]))
            out.append((t, it[1], q[0], q[1], it[4] * f) + tuple(it[5:]))
        elif t == "image":
            q = S((it[1], it[2]))
            out.append((t, q[0], q[1], it[3] * f, it[4] * f) + tuple(it[5:]))
        else:
            out.append(it)
    return out


def scale_north(F, den, xr, y0):
    """north arrow and a scale bar of 50 / 100 / 200 m (the longest under 40 mm), lower right inside the plan"""
    k = 1000.0 / den
    bar = max(b for b in (25.0, 50.0, 100.0, 200.0) if b * k <= 40.0 or b == 25.0)
    Lm = bar * k
    w = Lm + 26.0
    X, Y = xr - w - 3.0, y0 + 3.0
    it = []                                               # transparent: no box behind (Aras 14 Nov 12:10 UTC)
    cx, cy, r = X + 7.0, Y + 7.0, 5.0
    it.append(R_([ring(cx, cy, r, 48)], None, INK, 0.2, "scale_north"))
    nx, ny = F.north()
    tip = (cx + nx * r, cy + ny * r)
    it.append(R_([[tip, (cx - nx * r * 0.55 - ny * r * 0.45, cy - ny * r * 0.55 + nx * r * 0.45), (cx, cy),
                   (cx - nx * r * 0.55 + ny * r * 0.45, cy - ny * r * 0.55 - nx * r * 0.45)]], INK, None, 0.0,
                 "scale_north"))
    it.append(T_(u"N", tip[0] + nx * 1.8 - 0.8, tip[1] + ny * 1.8 - 0.8, 2.2, INK, True, "L", "scale_north"))
    xb, yb = X + 17.0, Y + 4.0
    for i in range(4):
        it.append(R_([box(xb + Lm * i / 4.0, yb, xb + Lm * (i + 1) / 4.0, yb + 1.2)], INK if i % 2 == 0 else "FFFFFF",
                     INK, 0.15, "scale_north"))
    it.append(T_(u"0", xb, yb - 2.8, 2.0, INK, False, "C", "scale_north"))
    it.append(T_(u"%d m" % bar, xb + Lm, yb - 2.8, 2.0, INK, False, "C", "scale_north"))
    return it


def occ_points(B, items, skip, layers=None):
    """v6.6: page points taken by plan marks and labels (text along its width, lines every 1 mm, ring vertices)"""
    occ, OL = [], layers or OCC_LAYERS
    for it in items:
        if id(it) in skip:
            continue
        if it[0] == "text" and it[8] in OL:
            w_ = B["text_w"](it[1], it[4], it[6])
            xa = it[2] - (w_ / 2.0 if it[7] == "C" else (w_ if it[7] == "R" else 0.0))
            occ += [(xa + w_ * i / 8.0, it[3] + it[4] * 0.35) for i in range(9)]
        elif it[0] == "line" and it[5] in OL:
            for a, b in zip(it[1][:-1], it[1][1:]):
                n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1])))
                occ += [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(n + 1)]
        elif it[0] == "poly" and it[6] in OL:
            occ += [p_ for r in it[1] for p_ in r]
    return occ


SRC_W = (u"WorldCover", u"OSM", u"ESHOT", u"MapBase", u"Page", u"DSI", u"image", u"GLO-30", u"survey", u"calculated",
         u"inferred", u"OpenStreetMap", u"ESA", u"ODbL", u"Data/", u"Sections")


def no_src(t):
    """v6.7: a page text without its source tags (Aras 15:23 UTC: no sources in the drawings)"""
    t = re.sub(u"\\s+as Page\\w+", u"", t)
    def grp(m):
        keep = [x.strip() for x in re.split(u"[;,]", m.group(2)) if not any(w in x for w in SRC_W)]
        return m.group(1) + u"(%s)" % u", ".join(keep) if keep else u""
    t = re.sub(u"(\\s*)\\(([^()]*)\\)", grp, t)
    t = t.replace(u"survey tree", u"tree")
    parts = []
    for x in t.split(u" · "):
        if x.strip() and x.strip() not in parts:
            parts.append(x.strip())
    return u" · ".join(parts) if u" · " in t else t.strip()


def clip_plan(B, items, bx, log):
    """plan items cut to the frame bx (page mm): lines and rings cut, texts moved inside or (no room) left out"""
    out, moved, lost = [], 0, []
    for it in items:
        t = it[0]
        if t == "line":
            for run in B["clip_line"](it[1], bx):
                if len(run) >= 2:
                    out.append((t, [tuple(q) for q in run]) + tuple(it[2:]))
        elif t == "poly":
            rr = [R for R in (B["clip_ring"](R_, bx) for R_ in it[1]) if len(R) >= 3]
            if rr:
                out.append((t, [[tuple(q) for q in R] for R in rr]) + tuple(it[2:]))
        elif t == "text":
            w = B["text_w"](it[1], it[4], it[6])
            x = it[2] - {"L": 0.0, "C": w / 2.0, "R": w}.get(it[7], 0.0)
            y = it[3]
            if not (bx[0] - 2.0 <= it[2] <= bx[2] + 2.0 and bx[1] <= y <= bx[3]):
                lost.append(it[1])
                continue
            dx = max(0.0, bx[0] + 0.5 - x) - max(0.0, x + w - (bx[2] - 0.5))
            dy = max(0.0, bx[1] + 0.5 - y) - max(0.0, y + it[4] - (bx[3] - 0.5))
            if dx or dy:
                if w > bx[2] - bx[0] - 1.0:
                    lost.append(it[1])
                    continue
                moved += 1
                it = (t, it[1], it[2] + dx, it[3] + dy) + tuple(it[4:])
            out.append(it)
        else:
            out.append(it)
    log.append(u"plan cut to its frame: %d name(s) moved inside" % moved)
    if lost:
        log.append(u"FLAG plan names outside the frame, left out: %s" % u", ".join(lost[:12]))
    return out


# ================================================================ the plan
def node_frame(B, corners):
    """the node frame on its own axes (long side flat) with NODE_MARGIN_M m round it"""
    F0 = B["Frame"]([tuple(p) for p in corners])
    T = [F0.raw(p) for p in corners]
    u0, u1 = min(q[0] for q in T) - NODE_MARGIN_M, max(q[0] for q in T) + NODE_MARGIN_M
    v0, v1 = min(q[1] for q in T) - NODE_MARGIN_M, max(q[1] for q in T) + NODE_MARGIN_M

    def back(qx, qy):
        return (F0.ca * qx + F0.sa * qy, -F0.sa * qx + F0.ca * qy)
    return B["Frame"]([back(u0, v0), back(u1, v0), back(u1, v1), back(u0, v1)])


def load_mb(log):
    """v5: the library part of the newest MapBase script (mb_load, mb_draw, mb_legend): one base map for every map
    (Aras 14 Nov 12:17-12:18 UTC: "create one map from that (outlines and etc.) and every map should use that")"""
    pth = _newest("bergama_mapbase_v*.py")
    with open(pth, encoding="utf-8") as f:
        code = f.read()
    end = "\n# ================================================================ main\n"
    ns = {"__name__": "bergama_mapbase_lib"}
    exec(compile(code[:code.index(end)], pth, "exec"), ns)
    ns["BERGAMA_ROOT"] = ROOT
    log.append(u"base map: %s (%s %s)" % (pth, ns.get("GH_LABEL"), ns.get("VERSION")))
    return ns


def mb_plan(MB, C, F, T, k, lim, B, P, log):
    """the plan's context from MapBase (its default look, no grain: this writer has none; water hatched) and, for the
    land-use count, the buildings, river and streets in frame m"""
    items = []
    cnt = MB["mb_draw"](C, items, T, k, lim, None, style={"grain": False})
    riv = [R for R in (B["clip_ring"]([T(p) for p in R_], lim) for R_ in C["polys"].get("river", [])) if len(R) >= 3]
    items += hatch(riv, 1.0, P["WATER_LINE"], 0.08, "water_hatch")
    inF = lambda q: -5.0 <= q[0] <= F.w + 5.0 and -5.0 <= q[1] <= F.h + 5.0
    units = []
    for R, fab_, com, src, nm in C["bld"]:
        Q = [F.local(p) for p in R]
        if len(Q) >= 3 and any(inF(q) for q in Q):
            units.append({"P": Q, "fab": fab_, "com": com, "src": src, "A": abs(P["area"](Q)),
                          "cx": sum(q[0] for q in Q) / len(Q), "cy": sum(q[1] for q in Q) / len(Q)})
    loc = lambda Rs: [(True, Q, 0.0, 0.0) for Q in ([F.local(p) for p in R] for R in Rs) if len(Q) >= 3]
    L = {"river": loc(C["polys"].get("river", [])), "road_net": loc(C["polys"].get("streets", []))}
    lc = dict((k_, [Q for cl, Q, a, b in loc(v)]) for k_, v in (C.get("lc") or {}).items())
    log.append(u"plan context (MapBase): %d buildings in the frame (%s); drawn: %s" % (
        len(units), u", ".join(u"%s %d" % (s_, n_) for s_, n_ in sorted(
            dict((u["src"], sum(1 for v in units if v["src"] == u["src"])) for u in units).items())),
        u", ".join(u"%s %d" % kv for kv in sorted(cnt.items()))))
    return items, cnt, units, L, lc


def hatch(rings, gap, col, lw, layer):
    """45 degree lines every gap mm inside the rings (even-odd), page mm: the textured water"""
    out = []
    if not rings:
        return out
    c, s = math.cos(math.pi / 4), math.sin(math.pi / 4)
    rot = lambda p: (p[0] * c + p[1] * s, -p[0] * s + p[1] * c)
    back = lambda q: (q[0] * c - q[1] * s, q[0] * s + q[1] * c)
    RR = [[rot(p) for p in R] for R in rings]
    vs = [q[1] for R in RR for q in R]
    v = math.floor(min(vs) / gap) * gap + gap / 2.0
    while v < max(vs):
        X = []
        for R in RR:
            for i in range(len(R)):
                a, b = R[i - 1], R[i]
                if (a[1] <= v) != (b[1] <= v):
                    X.append(a[0] + (v - a[1]) * (b[0] - a[0]) / (b[1] - a[1]))
        X.sort()
        for x0, x1 in zip(X[0::2], X[1::2]):
            if x1 - x0 > 0.05:
                out.append(L_([back((x0, v)), back((x1, v))], col, lw, layer))
        v += gap
    return out


# ================================================================ the page
def node_page(cfg, log):
    """cfg: NODE, SLIDE, OUT_FOLDER, NAME, INTRO (each node script's own words)"""
    t0 = time.time()
    node, out_folder = cfg["NODE"], cfg["OUT_FOLDER"]
    out_dir = os.path.join(ROOT, "output", out_folder)
    P, B, X, G, SL, D = load_all(node, out_folder, log)
    nd = SL["nodes"][node]
    F = node_frame(B, nd["corners"])
    pw, ph = PLAN_BOX[2] - PLAN_BOX[0], PLAN_BOX[3] - PLAN_BOX[1]
    den = 1000.0 / min(pw / F.w, ph / F.h)               # v7: the plan fills its box (scale not important, Aras 15:25)
    k = 1000.0 / den
    X0 = PLAN_BOX[0] + (pw - F.w * k) / 2.0
    Y0 = PLAN_BOX[3] - F.h * k
    log.append(u"plan: %s frame %.0f x %.0f m (+%.0f m round it), 1:%.0f, %.0f x %.0f mm" % (
        node, F.w - 2 * NODE_MARGIN_M, F.h - 2 * NODE_MARGIN_M, NODE_MARGIN_M, den, F.w * k, F.h * k))
    MB = load_mb(log)
    MC = MB["mb_load"](log)
    if MC is None:
        raise RuntimeError(u"MapBase cache missing: press MapBase once (after Basemap), then this node")
    items = [R_([box(X0, Y0, X0 + F.w * k, Y0 + F.h * k)], P["PAPER"], None, 0.0, "map_paper")]
    its_, mb_cnt, units, L, lc = mb_plan(MB, MC, F, lambda xy: (X0 + F.local(xy)[0] * k, Y0 + F.local(xy)[1] * k), k,
                                         (X0, Y0, X0 + F.w * k, Y0 + F.h * k), B, P, log)
    # v8 (Aras 16:30 UTC "use masterplan drawing directly with more details"): the plan IS his masterplan drawing
    # (MasterplanBase cache, every layer); MapBase stays behind the land-use count, and draws only if that cache is missing
    mp_rows, ex_rows = [], []
    try:
        MPn, MPC = G["pc_mp_data"](log)
        # v8.1 (run 1: the plan came out as one beige sheet): pieces over MP_MAX_M2 are his picture / texture frames
        # (1.4 and 2.1 km2), not plan elements (the same cut as Sections v1.11); they are left out
        ar_ = lambda P_: abs(sum(P_[i][0] * P_[i - 1][1] - P_[i - 1][0] * P_[i][1] for i in range(len(P_)))) / 2.0
        # v8.2 (run 2: whole blocks went solid green): a 4-corner clipped picture area is the picture's own rectangle,
        # not the shape he drew (his greens are irregular clipped patches), so it is left out too
        cut_ = lambda e_: len(e_[4]) > 2 and (ar_(e_[4]) > MP_MAX_M2 or (e_[0] == "a" and len(e_[4]) == 4))
        n_big = sum(1 for v_ in MPC["layers"].values() for e_ in v_ if cut_(e_))
        MPC = dict(MPC, layers=dict((kk, [e_ for e_ in v_ if not cut_(e_)]) for kk, v_ in MPC["layers"].items()))
        log.append(u"masterplan: %d sheet frames (> %.0f m2) and picture rectangles left out" % (n_big, MP_MAX_M2))
        mp_cnt = MPn["mp_draw"](MPC, items, lambda xy: (X0 + F.local(xy)[0] * k, Y0 + F.local(xy)[1] * k), k,
                                (X0, Y0, X0 + F.w * k, Y0 + F.h * k), None,
                                layers=set(kk.split("/")[0] for kk in MPC["layers"]),
                                style={"fill": {"su_outline": P["WATER_C"]}})   # v8.2: his river (a picture) as water
        seen = set()
        for kk in mp_cnt:
            nm = next(((ex, w_) for part in reversed(kk.split("/")) for ww, (ex, w_) in MP_WORDS.items() if part == ww),
                      None)
            if nm is None or nm[1] in seen:
                continue
            seen.add(nm[1])
            kind, fill, stroke, w, P_ = MPC["layers"][kk][0]
            col = (next((v for ww, v in MPn["AREA_FILL"].items() if ww in kk.split("/")), MPn["AREA_DEFAULT"])
                   if kind == "a" else (fill or stroke or MPn["AREA_DEFAULT"]))
            col = P["WATER_C"] if nm[1] == u"the Selinos" else col      # v8.2: drawn as water above
            # v9.2 (review: "legend doesn't match the plan"): an outline-only piece is keyed as its outline
            (ex_rows if nm[0] else mp_rows).append(("box" if (kind == "a" or fill or nm[1] == u"the Selinos") else
                                                    "line", col, nm[1]))
        log.append(u"plan = his masterplan: %s" % (u", ".join(u"%s %d" % kv for kv in sorted(mp_cnt.items())) or
                                                  u"nothing in this frame"))
        if not mp_cnt:
            items += its_
    except Exception as ex_:
        items += its_
        log.append(u"FLAG masterplan not drawn (%s: %s): press MasterplanBase once; MapBase drawn instead" % (
            type(ex_).__name__, ex_))
    sec_ids = set()
    pgS = lambda xy: (X0 + F.local(xy)[0] * k, Y0 + F.local(xy)[1] * k)
    inside = lambda q, m=0.0: X0 + m <= q[0] <= X0 + F.w * k - m and Y0 + m <= q[1] <= Y0 + F.h * k - m
    bxF = (0.0, 0.0, F.w, F.h)

    def sline(pts, col, lw, layer, dash=None):
        for run in B["clip_line"]([F.local(p) for p in pts], bxF):
            if len(run) >= 2:
                items.append(L_([(X0 + q[0] * k, Y0 + q[1] * k) for q in run], col, lw, layer, dash))
    # node frame
    sline(nd["corners"] + [nd["corners"][0]], INK, 0.35, "node_frame", (3.0, 1.0, 0.6, 1.0))

    # ---- sections first (their windows go on the plan). v6 (Aras 12:38 UTC "don't ever do the same job twice ...
    # cache it and make it usable by the next script"): read from the Sections cache, never rebuilt here
    E = X["load_engine"](log)                             # only its text widths (the writer centres text with them)
    X["_ENGINE_W"][:] = [E["text_w"]]
    CL, cum = X["load_centreline"](log)
    pc = os.path.join(ROOT, "cached", "bergama_sections", "cuts.json")
    if not os.path.isfile(pc):
        raise RuntimeError(u"%s not found: press Sections (v1.6.4 or newer) first, then this node" % pc)
    with open(pc, encoding="utf-8") as f:
        CJ = json.load(f)
    log.append(u"sections: %s (Sections %s, run %s)" % (pc, CJ.get("version"), CJ.get("run")))
    for nm in (node + u"-A", node + u"-B"):              # v6.1: Sections v1.6.5 keeps items in cuts/<name>.json
        j_ = CJ["cuts"].get(nm)
        if j_ and "items" not in j_ and j_.get("items_file"):
            with open(os.path.join(os.path.dirname(pc), j_["items_file"]), encoding="utf-8") as f:
                j_["items"] = json.load(f)
    cuts = [Cut(nm, SL["lines"][nm], CJ["cuts"].get(nm), CL) for nm in (node + u"-A", node + u"-B")]
    done = []
    cur_top = SEC_ROOMS[0][3]                       # v9.5 (run 8: empty bands under each cut): cuts packed from the top
    for C, room in zip(cuts, SEC_ROOMS):
        x0, y0, x1, y1 = room
        y0, y1 = cur_top - (y1 - y0), cur_top
        if C.J is None:
            items.append(T_(u"FLAG: section %s is not in the Sections cache" % C.name, x0, y1 - 12.0, 2.6, RED))
            sec_ids.add(id(items[-1]))
            log.append(u"FLAG section %s not in %s: press Sections again" % (C.name, pc))
            continue
        # v6.2 (run 3: 8 of 12 cuts shrunk, mostly by the cached 13 mm title block): the cached title, scale and
        # subtitle are left out and the page prints one header line plus the "meets" line; the drawing gets the rest
        top_y = y1 - 10.0
        # v7 (Aras 15:25-15:27 UTC "fit every drawing into A3's like the scale is not important"): each cut fills
        # its room: the largest cached scale that nearly fits, then stretched evenly to fit (scale bar kept, no 1:x)
        # v9.2 (review of run 4: "sections are thin strips in white space"): the most detailed cached scale, scaled
        # so the cut FILLS its room's height (true proportions, no exaggeration), then cropped left and right round the
        # stream to the room's width; the plan marks show the cropped part; our own scale bar under it
        den_s = min(int(d_) for d_ in C.J["items"])
        e_ = C.J["items"][str(den_s)]
        LYR = {"text": 8, "poly": 6, "line": 5, "circle": 7, "image": 9}
        body = [it for it in e_["items"] if it[LYR.get(it[0], 0)] not in ("title", "levels")]
        px = set(round(it[2], 2) for it in body if it[0] == "text" and it[8] == "callouts" and
                 any(w in it[1] for w in (u"Meadow", u"grasses", u"reed", u"Kamış", u"iris", u"süsen")))
        body = [it for it in body if not (it[LYR.get(it[0], 0)] == "callouts" and round(
            it[1][0][0] if it[0] == "line" else (it[1] if it[0] == "circle" else it[2]), 2) in px)]
        ys_ = [p_[1] for it in body if it[0] == "poly" for r in it[1] for p_ in r] + \
            [p_[1] for it in body if it[0] == "line" for p_ in it[1]]
        xs_ = [p_[0] for it in body if it[0] == "poly" for r in it[1] for p_ in r]
        bb = [min(xs_), min(ys_), max(xs_), max(ys_)]
        # v9.3 (run 6: the cuts came out as tall sky over a few metres of ground): the height that counts is the
        # drawing without its sky; at least 55 % of the cut (or 150 m) stays in view; the sky is cut to what is left
        yc_ = [p_[1] for it in body if it[0] == "poly" and it[6] != "sky" for r in it[1] for p_ in r] + \
            [p_[1] for it in body if it[0] == "line" and it[5] != "sky" for p_ in it[1]]
        w, h = bb[2] - bb[0], max(yc_) - bb[1] + 4.0
        Wr, Hr = x1 - x0, top_y - y0 - 8.0
        vmin = min(w, max(0.30 * w, 90.0 * 1000.0 / den_s))   # v9.4 (run 7: flat cuts still 10 mm tall): 30 % / 90 m
        f = min(Hr / h, Wr / vmin, 1.8)
        wx = [p_[0] for it in body if it[0] == "poly" and it[6] == "water" for r in it[1] for p_ in r]
        cx = (min(wx) + max(wx)) / 2.0 if wx else (C.s_th - C.window[0]) * 1000.0 / den_s
        if w * f <= Wr:
            xa, xb = bb[0], bb[2]
        else:
            vw = Wr / f
            xa = min(max(bb[0], cx - vw / 2.0), bb[2] - vw)
            xb = xa + vw
        h = min(bb[3] - bb[1], Hr / f)
        bb[3] = bb[1] + h
        cropB = (xa, bb[1] - 1.0, xb, bb[3] + 1.0)
        cut_ = []
        for it in body:
            t_ = it[0]
            if t_ == "line":
                for run in B["clip_line"](it[1], cropB):
                    if len(run) >= 2:
                        cut_.append((t_, [tuple(q) for q in run]) + tuple(it[2:]))
            elif t_ == "poly":
                rr = [R for R in (B["clip_ring"](R_, cropB) for R_ in it[1]) if len(R) >= 3]
                if rr:
                    cut_.append((t_, [[tuple(q) for q in R] for R in rr]) + tuple(it[2:]))
            elif t_ == "text":
                if xa + 1.0 <= it[2] <= xb - 1.0 and it[3] <= bb[3] - it[4]:
                    cut_.append(it)
            elif t_ == "circle":
                if xa <= it[1] - it[3] and it[1] + it[3] <= xb and it[2] + it[3] <= bb[3]:
                    cut_.append(it)
            elif t_ == "image":
                if xa <= it[1] and it[1] + it[3] <= xb and it[2] + it[4] <= bb[3]:
                    cut_.append(it)
        w0 = C.window[0]
        C.window = (w0 + xa * den_s / 1000.0, w0 + xb * den_s / 1000.0)
        items.append(T_(u"SECTION %s" % C.name, x0, y1 - 3.5, 2.8, INK, True, "L", "sections"))
        sub = next((it[1] for it in e_["items"] if it[0] == "text" and it[1].startswith(u"both banks")), u"")
        if not C.crosses:                                 # v8.3: a B cut runs along the bank, not across both
            sub = sub.replace(u"both banks", u"along the bank")
        items.append(T_(sub, x0 + 30.0, y1 - 3.5, 2.2, INK, False, "L", "sections"))
        sec_ids.update(id(it) for it in items[-2:])
        ox = x0 + (Wr - (xb - xa) * f) / 2.0
        its = scale_items(cut_, f, xa, bb[3], ox - xa, top_y - bb[3])
        items += its
        den_e = den_s / f                                 # our scale bar (the cached one may be cropped away)
        mpm = 1000.0 / den_e
        bar = max(b_ for b_ in (5.0, 10.0, 20.0, 25.0, 50.0) if b_ * mpm <= 30.0 or b_ == 5.0)
        yb_ = top_y - h * f - 5.0
        for k_ in range(4):
            its.append(R_([box(ox + bar * mpm * k_ / 4.0, yb_, ox + bar * mpm * (k_ + 1) / 4.0, yb_ + 1.0)],
                          INK if k_ % 2 == 0 else "FFFFFF", INK, 0.15, "sections"))
        its.append(T_(u"0", ox, yb_ - 2.6, 1.9, INK, False, "C", "sections"))
        its.append(T_(u"%d m" % bar, ox + bar * mpm, yb_ - 2.6, 1.9, INK, False, "C", "sections"))
        cur_top = yb_ - 9.0
        items += its[-6:]
        sec_ids.update(id(it) for it in its)
        w, h = xb - xa, h
        log.append(u"section %s: %.0f x %.0f mm, about 1:%.0f (cached 1:%d x%.2f)" % (C.name, w * f, h * f, den_s / f,
                                                                                     den_s, f))
        done.append(C)
        log += [u"%s: %s" % (C.name, n_) for n_ in C.J.get("notes", []) if n_.startswith(u"FLAG")]

    # ---- section lines on the plan. v7.1 (Aras 15:37 UTC "draw two distinct arrows you have been doing that before"):
    # the R01 cut symbol of the older scripts (pages_common pc_cut_mark) over the drawn part, looking downstream
    names_at = []
    for C in cuts:
        s0, s1 = C.window if C in done else (0.0, C.L)
        pa, pb = C.xy(s0), C.xy(s1)
        if C.crosses:                                     # across the stream: looking downstream
            dl = X["cl_project"](CL, cum, *C.xy(C.s_th))[2]
        else:                                             # v7.5 along the bank (section_lines v2 B): at the stream
            mid = C.xy((s0 + s1) / 2.0)
            near = min(CL, key=lambda c_: G["pc_dist"](c_, mid))
            dl = (near[0] - mid[0], near[1] - mid[1])
        q0 = pgS(C.xy(C.s_th))
        q1 = pgS((C.xy(C.s_th)[0] + dl[0], C.xy(C.s_th)[1] + dl[1]))
        for it in G["pc_cut_mark"](pgS(pa), pgS(pb), (q1[0] - q0[0], q1[1] - q0[1]), C.name, layer="section_names"):
            if it[0] == "text":                           # two cuts sharing an end (N1): one name there
                if any(G["pc_dist"]((it[2], it[3]), q) < 5.0 for q in names_at):
                    continue
                names_at.append((it[2], it[3]))
            items.append(it)

    # ---- transit and heritage over the plan (PageTransit / PageHeritage data and colours)
    K = D["key"]
    for g in K["line_order"]:
        col, lw, dash = K["lines"][g]
        for ref, r in D["routes"].items():
            if G["pc_group_of"](D, ref) != g:
                continue
            for wid in r["ways"]:
                P_ = D["ways"].get(wid)
                if P_:
                    sline(P_, P["mixh"](col, P["PAPER"], 0.55), lw * 0.45, "bus_lines", dash)   # v4.4: quiet
    H = sorted(D["heritage"], key=lambda h: int(h["n"]))
    sq = None     # v7.1 (Aras 15:36 UTC "this marking is totally wrong"): no city-square ring; his gathering points
    #               come from the masterplan (MasterplanBase cache, when it is ready)
    # v6.4 no-repeat (Aras 13:02 UTC "make sure nothing repeats in the slides", REUSE_MAP R4, R5): slide 5 keeps the
    # stops and the heritage loop; a node plan keeps only the bus stop of its city square and the loop stops inside
    for nm, xy, ln in ([sq[2]] if sq else []):
        q = pgS(xy)
        if inside(q):
            items.append(R_([ring(q[0], q[1], 1.2, 20)], "FFFFFF", INK, 0.35, "bus_stops"))
            items.append(T_(u"%s · %s" % (nm, u" ".join(sorted(ln, key=lambda r: (len(r), r)))), q[0] + 1.8, q[1] - 2.8,
                            2.2, INK, False, "L", "bus_stops"))
    # v4.4 (Aras 12:15 UTC "public transport lines should be less appearant compared to our proposed path"): the
    # proposed paths lead: the streamside spine K4 -> K5 and the stream walk (loop 3 -> 4) along the Selinos, strong
    sp = None if mp_rows else G["pc_selinos"](D["hubs"]["K4"], D["hubs"]["K5"])   # v7.2: his paths, not ours
    if sp:
        sline(sp, "FFFFFF", 2.2, "proposed_path")
        sline(sp, SQUARE_C, 1.4, "proposed_path")
    for h in H:
        q = pgS(h["xy"])
        if inside(q):
            items.append(R_([ring(q[0], q[1], K["heritage_r"], 32)], RED, "FFFFFF", 0.35, "heritage_loop"))
            items.append(T_(h["n"], q[0], q[1] - 1.0, 2.8, "FFFFFF", True, "C", "heritage_loop"))
            items.append(T_(h["name"], q[0] + K["heritage_r"] + 1.0, q[1] + 1.2, 2.4, RED, True, "L", "heritage_loop"))
    for code, xy in D["hubs"].items():
        q = pgS(xy)
        if inside(q):
            hc = "T" if code in ("IST", "RED") else code
            col = K["hub"][D["hub_kind"][hc]]
            items.append(R_([box(q[0] - 2.3, q[1] - 2.3, q[0] + 2.3, q[1] + 2.3)], col, "FFFFFF", 0.3, "hubs"))
            items.append(T_(hc, q[0], q[1] - 0.9, 2.4, "FFFFFF", True, "C", "hubs"))

    # ---- the city square (Aras's idea): a heritage loop stop and a bus stop both in the node frame
    if sq:
        d_, h, s = sq
        mid = ((h["xy"][0] + s[1][0]) / 2.0, (h["xy"][1] + s[1][1]) / 2.0)
        r_m = d_ / 2.0 + 20.0
        q = pgS(mid)
        items.append(("poly", [ring(q[0], q[1], r_m * k, 64)], None, SQUARE_C, 0.6, [2.0, 1.0], "city_square", 1,
                      None, None))
        qa, qb = pgS(h["xy"]), pgS(s[1])
        items.append(L_([qa, qb], SQUARE_C, 0.4, "city_square", (0.01, 0.9)))
        items.append(T_(u"CITY SQUARE (idea)", q[0], q[1] + r_m * k + 1.5, 2.6, SQUARE_C, True, "C", "city_square"))
        sq = (h, s, d_)
        log.append(u"city square: loop stop %s %s and bus stop %s are %.0f m apart (straight line)" % (
            h["n"], h["name"], s[0], d_))
    # ---- V1, the viewpoint of the perspective (brief: viewpoints marked on each node plan; place assumed): from the
    # city square, else from the bank end of the drawn part of section A, looking to the stream bed of the nearest cut
    vp = None
    if done:
        if sq:
            c0 = ((sq[0]["xy"][0] + sq[1][1][0]) / 2.0, (sq[0]["xy"][1] + sq[1][1][1]) / 2.0)
            Cn = min(done, key=lambda C: G["pc_dist"](C.xy(C.s_th), c0))
        else:
            Cn = done[0]
            c0 = Cn.xy(Cn.window[0])
        vp = (c0, Cn.xy(Cn.s_th))
        qa, qb = pgS(vp[0]), pgS(vp[1])
        # v6.5 (run 5: V1 sat on the Kızıl Avlu label in N4 and on the square's dotted link in N2): V1 moves to the
        # nearby spot farthest from the plan's labels and markers (inside the square when there is one)
        occ = [o for o in occ_points(B, items, sec_ids) if G["pc_dist"](o, qa) > 0.1]
        # v9.5 (run 8: V1 on the Kizil Avlu stop in N4 and on the N3-A name): wider search, and the view arrows
        # must be clear too
        rr = [0.0, 4.0, 8.0, 12.0] if not sq else [0.0, 0.3 * r_m * k, 0.6 * r_m * k, 8.0, 12.0]
        cand = [(qa[0] + r * math.cos(a_ * math.pi / 8.0), qa[1] + r * math.sin(a_ * math.pi / 8.0), r)
                for r in rr for a_ in range(16 if r else 1)]
        cand = [c for c in cand if inside(c, 5.0)] or [(qa[0], qa[1], 0.0)]

        def clear(c):
            an = math.atan2(qb[1] - c[1], qb[0] - c[0])
            pts = [c[:2]] + [(c[0] + d_ * math.cos(an), c[1] + d_ * math.sin(an)) for d_ in (4.5, 8.0)]
            return min([7.0] + [G["pc_dist"](p_, o) for p_ in pts for o in occ]) - 0.05 * c[2]
        best = max(cand, key=clear)
        qa = best[:2]
        ang = math.atan2(qb[1] - qa[1], qb[0] - qa[0])
        for da in (-0.35, 0.35):
            items.append(L_([qa, (qa[0] + 9.0 * math.cos(ang + da), qa[1] + 9.0 * math.sin(ang + da))], INK, 0.35,
                            "viewpoints"))
        items.append(R_([ring(qa[0], qa[1], 2.0, 24)], INK, "FFFFFF", 0.3, "viewpoints"))   # v9.2: accent = our move only
        items.append(T_(u"V1", qa[0], qa[1] - 0.8, 2.2, "FFFFFF", True, "C", "viewpoints"))
        log.append(u"V1 viewpoint (assumed): %s, looking to the bed of %s" % (
            u"the city square" if sq else u"the bank end of %s" % Cn.name, Cn.name))
    # v6.5 (run 5: stop and loop labels read poorly over buildings and the spine): a light backing behind plan labels
    lab = []
    for it in items:
        if id(it) not in sec_ids and it[0] == "text" and it[8] in LBL_LAYERS and it[5] != "FFFFFF":
            w_ = B["text_w"](it[1], it[4], it[6])
            xa = it[2] - (w_ / 2.0 if it[7] == "C" else (w_ if it[7] == "R" else 0.0))
            lab.append(("poly", [box(xa - 0.5, it[3] - 0.35 * it[4], xa + w_ + 0.5, it[3] + 0.85 * it[4])], "FFFFFF",
                        None, 0.0, None, it[8], 1, None, 0.75))
        lab.append(it)
    items = lab
    # v4.3 (Aras 12:14 UTC "drawings do flows outside of it"): every plan item cut to the plan frame
    items = clip_plan(B, [it for it in items if id(it) not in sec_ids], (X0, Y0, X0 + F.w * k, Y0 + F.h * k), log) + \
        [it for it in items if id(it) in sec_ids]
    G["pc_frame_check"]([it for it in items if id(it) not in sec_ids], (X0, Y0, X0 + F.w * k, Y0 + F.h * k), log,
                        lambda t, z, b_: B["text_w"](t, z, b_))
    items.append(L_([(X0, Y0), (X0 + F.w * k, Y0), (X0 + F.w * k, Y0 + F.h * k), (X0, Y0 + F.h * k), (X0, Y0)], INK,
                    0.25, "map_frame"))
    # v6.6 (run 6, N3: hub tile T on the scale bar): scale and north go to the plan corner with the fewest marks
    sn = scale_north(F, den, X0 + F.w * k, Y0)
    xs = [p_[0] for it in sn if it[0] == "poly" for r in it[1] for p_ in r] + [it[2] for it in sn if it[0] == "text"]
    ys = [p_[1] for it in sn if it[0] == "poly" for r in it[1] for p_ in r] + [it[3] for it in sn if it[0] == "text"]
    sx0, sx1, sy0, sy1 = min(xs) - 1.0, max(xs) + 5.0, min(ys) - 1.0, max(ys) + 3.0
    # v8.4 (run 3, N3 + N6: the transparent marks sat on his drawing and across the node frame): scale and north go
    # OUTSIDE the plan, above its top right corner, shrunk only if the slide title would run into them
    ytop = Y0 + F.h * k
    tw = 14.0 + B["text_w"](u"%s · %s" % (node, nd["name"]), 7.5, True) + 3.0
    lim_ = 276.0 if sx0 < tw else 286.0
    f_sn = min(1.0, (lim_ - ytop - 1.0) / (sy1 - sy0))
    items += scale_items(sn, f_sn, sx1, sy0, 0.0, ytop + 1.0 - sy0)
    if f_sn < 0.6:
        log.append(u"FLAG scale + north: only %.0f %% size fits above the plan" % (100.0 * f_sn))

    # ---- key under the plan
    ky = Y0 - 5.0
    items.append(T_(u"Plan · %s %s · EXISTING today and the PROPOSAL" % (node, nd["name"]), PLAN_BOX[0], ky, 2.8, INK, True))
    ky -= 5.0
    if ex_rows or mp_rows:                                # v8: the key of his drawing as drawn here
        rows1 = [("hdr", None, u"EXISTING")] + ex_rows + [("box", P["WATER_C"], u"the Selinos")] * (not any(
            r_[2] == u"the Selinos" for r_ in ex_rows)) + [("hdr", None, u"PROPOSAL")] + mp_rows   # v8.1: balanced
    else:
        rows1 = [("hdr", None, u"EXISTING: GROUND AND GREEN")] + MB["mb_legend"](MC, mb_cnt, {"grain": False})
    rows2 = [("hdr", None, u"EXISTING: MOVEMENT AND HERITAGE"),
             ("line", P["mixh"](K["lines"]["town"][0], P["PAPER"], 0.55), u"bus line"),
             ("disc", RED, u"heritage loop stop"),
             ("box", K["hub"]["walk"], u"transit hub"),
             ("line", "C0392B", u"section cut, arrows = view direction"),
             ] + ([] if mp_rows else [("hdr", None, u"PROPOSAL"),
                  ("line", SQUARE_C, u"streamside spine K4 - K5 along the Selinos (proposed path)")]) + [
             ("disc", INK, u"V1 viewpoint")]
    rows1, rows2 = [[(r_[0], r_[1], no_src(r_[2])) for r_ in rr_] for rr_ in (rows1, rows2)]   # v6.7: before wrapping
    cw = (PLAN_BOX[2] - PLAN_BOX[0]) / 2.0
    yk1 = P["draw_rows"](B, items, rows1, PLAN_BOX[0], ky, cw - 3.0, step=3.0, ts=2.1)
    yk2 = P["draw_rows"](B, items, rows2, PLAN_BOX[0] + cw, ky, cw - 3.0, step=3.4, ts=2.3)

    # ---- land use of the node frame (Page02's count, 1 m cells, on the node frame's own box)
    fq = [F.local(p) for p in nd["corners"]]
    fbox = (min(q[0] for q in fq), min(q[1] for q in fq), max(q[0] for q in fq), max(q[1] for q in fq))
    su = [u for u in units if fbox[0] <= u["cx"] <= fbox[2] and fbox[1] <= u["cy"] <= fbox[3]]
    lu, tot = P["land_use"](su, L, lc, fbox, log)
    # v9.2 (review: "15 classes, slivers, a separate list"): the five largest classes plus "other", one full-width bar,
    # each class named with its % in one row under the bar (no method note in the title)
    lx0, bw, ly = PLAN_BOX[0], PLAN_BOX[2] - PLAN_BOX[0], min(yk1, yk2) - 4.0
    items.append(T_(u"LAND USE IN THE NODE FRAME · %.1f ha" % (tot / 1e4), lx0, ly, 2.8, INK, True, "L", "diagrams"))
    keep = sorted([r_ for r_ in lu if r_[2] > 0], key=lambda r_: -r_[2])
    top = [r_ for r_ in keep if not r_[0].lower().startswith(u"other")][:5]
    rest = sum(r_[2] for r_ in keep if r_ not in top)
    if rest > 0:
        top.append((u"Other", "E6E3DC", rest))
    bar_y, bar_h = ly - 8.0, 4.5
    xx = lx0
    for lab, col, a_ in top:
        w_ = bw * a_ / tot
        items.append(R_([box(xx, bar_y, xx + w_, bar_y + bar_h)], col, "FFFFFF", 0.3, "diagrams"))
        xx += w_
    cwl = bw / max(1, len(top))
    for i_, (lab, col, a_) in enumerate(top):
        xl = lx0 + i_ * cwl
        items.append(R_([box(xl, bar_y - 5.2, xl + 2.4, bar_y - 2.8)], col, None, 0.0, "diagrams"))
        pc_ = 100.0 * a_ / tot
        t_ = u"%s %s" % (no_src(lab), (u"%.0f%%" % pc_) if pc_ >= 0.5 else u"< 1%")
        for k_, ln in enumerate(wrap(B, t_, 2.0, cwl - 4.0)[:2]):
            items.append(T_(ln, xl + 3.2, bar_y - 4.9 - 2.6 * k_, 2.0, INK, False, "L", "diagrams"))

    # ---- v8 (Aras 16:30-16:32 UTC): why this node, its story and ONE abstract concept diagram (Niarchos sketch
    # spirit: the city as dots, the stream low, our move the only solid shape); water bars gone (slide 3 keeps seasons)
    st = STORY.get(node)
    if st:
        # v9.5: the why-here block follows the packed cuts up; the perspective room grows by what is freed
        yw = max(95.0, min(cur_top - 1.0, 150.0))
        items.append(T_(u"WHY HERE · %s" % st[0].upper(), 214.0, yw, 2.8, INK, True, "L", "diagrams"))
        concept(node, items, 214.0, yw - 33.0, 192.0, 30.0, G)
        yy = yw - 41.0
        y_story = yy
        for para_ in st[1]:
            for ln in wrap(B, para_, 2.2, 90.0):
                items.append(T_(ln, 214.0, yy, 2.2, INK, False, "L", "diagrams"))
                yy -= 3.0
            yy -= 1.2
        if yy < 12.0:
            log.append(u"FLAG story of %s runs below y 12 mm (%.0f)" % (node, yy))
    else:
        log.append(u"FLAG no story for %s yet" % node)

    # ---- placeholders (NO DRAWING rule; brief: perspective, program brief, building proposal per node)
    def holder(x0, y0, x1, y1, title, sub, layer):
        items.append(R_([box(x0, y0, x1, y1)], "F1EFEA", GREY, 0.3, layer))
        items.append(L_([(x0, y0), (x1, y1)], "C9C5BC", 0.2, layer))
        items.append(L_([(x0, y1), (x1, y0)], "C9C5BC", 0.2, layer))
        hw = min(30.0, (x1 - x0) / 2.0 - 2.0)                 # v4.1: the label band stays inside its box
        items.append(R_([box((x0 + x1) / 2.0 - hw, (y0 + y1) / 2.0 - 5.0, (x0 + x1) / 2.0 + hw,
                             (y0 + y1) / 2.0 + 6.5)], "F1EFEA", None, 0.0, layer))
        items.append(T_(title, (x0 + x1) / 2.0, (y0 + y1) / 2.0 + 2.0, 2.8, INK, True, "C", layer))
        yy_ = (y0 + y1) / 2.0 - 2.0
        for ln in wrap(B, sub, 2.0, min(58.0, x1 - x0 - 4.0)):
            items.append(T_(ln, (x0 + x1) / 2.0, yy_, 2.0, GREY, False, "C", layer))
            yy_ -= 2.6
    # v9.2 (review: "a 66 x 38 mm empty area under the story"): the program brief fills the story column under the
    # text, the perspective and the building proposal share the right half
    holder(310.0, 31.0, 406.0, (y_story if st else 54.0), u"V1 · PERSPECTIVE · %s" % node,
           u"placeholder: Aras's render (Archicad, Unreal 5) from V1 on the plan", "placeholder_perspective")
    yp = (yy if st else 54.0) - 1.0
    if yp - 12.0 >= 12.0:
        holder(214.0, 12.0, 304.0, yp, u"PROGRAM BRIEF", u"placeholder: what happens here, for whom, in which season",
               "placeholder_program")
        holder(310.0, 12.0, 406.0, 28.0, u"BUILDING PROPOSAL",
               u"placeholder: plan, section, elevation (if the node has one)", "placeholder_building")
    else:
        holder(310.0, 12.0, 356.0, 28.0, u"PROGRAM BRIEF", u"placeholder: what happens here, for whom, in which season",
               "placeholder_program")
        holder(360.0, 12.0, 406.0, 28.0, u"BUILDING PROPOSAL",
               u"placeholder: plan, section, elevation (if the node has one)", "placeholder_building")
    # ---- title band and credit
    items.append(T_(u"C  NODES IN DETAIL · SLIDE %d" % cfg["SLIDE"], 14.0, 288.0, 2.6, INK, True))
    items.append(T_(u"%s · %s" % (node, nd["name"]), 14.0, 278.5, 7.5, INK, True))
    # v9.2 (review: the intro line was the same boilerplate on every slide): no intro; section A takes the room
    # v6.7 (Aras 14 Nov 15:23-15:24 UTC "dont give sources in the drawings at all", "no sources for nothing"):
    # sources go to the log only; every page text loses its source tags
    log.append(u"Sources: survey Bergama_Altlik.3dm; node frames and section lines Data/section_lines.json (11 Nov); "
               u"OpenStreetMap 28 Jul 2026 (ODbL); ESHOT; ESA WorldCover 2021; flows DSI and gauges as the Sections "
               u"script. Distances straight line, calculated.")
    items = [(it[0], no_src(it[1])) + tuple(it[2:]) if it[0] == "text" else it for it in items]
    items = [it for it in items if not (it[0] == "text" and not it[1].strip())]

    bb = X["items_bbox"](items)                           # anything past the sheet edge: FLAG (Aras 11:26 UTC)
    if bb[0] < -0.5 or bb[1] < -0.5 or bb[2] > PAGE_W + 0.5 or bb[3] > PAGE_H + 0.5:
        log.append(u"FLAG drawing runs past the page: ink from x %.0f to %.0f, y %.0f to %.0f mm (page %.0f x %.0f)" % (
            bb[0], bb[2], bb[1], bb[3], PAGE_W, PAGE_H))
    os.makedirs(out_dir, exist_ok=True)
    pdf = X["write_pdf_node"](os.path.join(out_dir, cfg["NAME"] + u".pdf"), [(PAGE_W, PAGE_H, items)],
                              u"Slide %d, %s %s" % (cfg["SLIDE"], node, nd["name"]))
    log.append(u"%s  %s" % (pdf, time.strftime("%H:%M:%S")))
    G["pc_present"](pdf, cfg["SLIDE"], log)
    G["pc_review"](pdf, os.path.join(out_dir, "review"), log)     # v3: the shared standard (pages_common v3)
    flags = [l for l in log if u"FLAG" in l]               # v9.2: the Sections FLAGs carried through count too
    return u"%s\n%s, %d of 2 section(s), %d FLAG line(s), %.1f s" % (u"\n".join(log), node, len(done), len(flags),
                                                                    time.time() - t0)
