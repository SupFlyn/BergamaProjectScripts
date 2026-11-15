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
  PLACEHOLDERS V1 perspective, building proposal (program brief filled since v12.7) (NO DRAWING rule: Aras makes them)
Reads the newest scripts/bergama_basemap_v*, bergama_p02_what_is_there_v*, bergama_sections_v*, bergama_mapbase_v*
(code only), Data/bergama_pages_common.py, section_lines.json, bergama_access_heritage.json and the caches above.
"""
import os, re, glob, json, math, time

NC_VERSION = "v12.8"   # v12.8: heritage, hub and V1 marks centred by pages_common pc_text_c (Aras 15 Nov 14:56 UTC "center the numbers in the boundries"); v12.7: PROGRAM BRIEF filled from NODE_IDEAS.md (text, no box; Aras 15 Nov 14:47 UTC "fill the placeholders"); v12.6 (Aras 15 Nov 14:45 UTC "we gonna use masterplan svg as the base of the maps"): the node plans show his masterplan drawing whole (his ev-yol / builts2 no longer hidden); MapBase stays only where his sheet is see-through; v12.5: the river in the node plans is a flat fill, no hatch (Aras 15 Nov 14:38 UTC); v12.4: every context from MapBase (Aras 13:41): node plan crops hide his ev-yol / builts2 and are see-through over MapBase (opaque crop refused, vector fallback; legend sampler skips see-through pixels); why-here houses, streets, parks, bridges from MapBase (houses raised by survey floors x 3.0 m, sacred 5.0 m, else flat); v12.3: no white box behind plan labels (Aras 15 Nov 13:44 UTC "dont have a opaque background for texts in any single of the drawings"): a letter-shaped white halo instead (pages_common v3.27 pc_halo); v12.2: svg_crop bg=False (transparent, for MapBase under; node plans unchanged); v12.1: why-here blocks in the language of his liked examples (white context, one heavy cut line, his masterplan move laid on the ground in depth, his canopy triangles folded on Y columns, his trees and people as his cutouts, one movement arrow; Aras 12:10 "compare with the examples"); v12: why-here diagrams drawn from the node's A cut in the Sections cache (true ground, bed, all water levels, masterplan move, buildings and bridges in depth; Aras 10:36 "this diagram is just so wrong"); v11.6: N4 canopy: every other bay a glazed room up to the louvres, planters in the open bay (Aras 10:02); v11.5: N4 raised gathering drawn as the designed canopy (folded triangle skin, louvres, Y columns; Sections v1.28 language); v11.4: svg_crop takes css (slide 4 sub-system colours), node plans unchanged; v11.3: MapBase under the plans in the A05 base map look (white houses with shadows, one road outline; MapBase v1.8 mb_a05_style; Aras 15 Nov 07:59 "you need to update other scripts so i can see the change in the basemap aswell"); v11.2: legend colours read from the crop itself, diagram town as gabled rows, moves as tint + accent edge, no arrows from the air, own figures, diagram right under its title, placeholders one system; v11: each node plan is a straight crop of master.svg (rendered by Edge / Chrome on his PC, cached), marks on top; v10: v10: why-here diagrams as section-axo blocks (depth, shaded planes, extruded town, accent move with shadow); MapBase always under the plan, his existing roads/buildings left out; v9.9: v9.9: a heritage stop on a cut line stays in the cropped section (N4-A Red Hall); v9.8: v9.8: Ulu Cami silhouette as built (hall, three domes, minaret on a stone base); v9.7: v9.7: Red Hall drawn as the roofless arched brick hall; diagram levels start at the riser they meet; v9.6: v9.6: program brief under the land-use bar when it fits, perspective the full right half; v9.5: v9.5: diagram levels run to the banks, N5 town band lower and label over its move; cuts packed from the top, why-here block follows, perspective room grows; V1 clear of stops, names and its arrows; v9.4: v9.4: at least 30 % (or 90 m) of a cut in view, so flat cuts get taller; v9.3: v9.3: section fit by the drawing without its sky, at least 55 % (or 150 m) of the cut in view, sky cut to the room; v9.2: v9.2 (fresh review of run 4): sections fill their rooms (cropped round the stream, own scale bar), no intro line, short key words, V1 in ink, land use = 5 classes + other with names on one row, program brief under the story, diagram arrows start at their cause, slots as voids, FLAG count includes carried FLAGs; v9.1: v9.1: diagrams to DIAGRAM_STYLE v2 (Niarchos measured: low ground, names under it, small accent); v9: v9: why-here diagrams redrawn on the shared diagram kit (pc_dg_kit, DIAGRAM_STYLE.md; Aras 21:30 UTC); v8.4: v8.4: scale + north above the plan (off his drawing), intro wording; v8.3: v8.3: B cut subtitle "along the bank", N3 diagram label clear of the dots; v8.2: v8.2: 4-corner picture rectangles of the masterplan left out (no solid green blocks), the river filled as water; v8.1: v8.1: masterplan sheet / texture frames (> 0.1 km2) left out, legend columns balanced, intro without the old levels text; v8: plan = his masterplan drawing; why-here story + one concept diagram per node; water bars and meets line gone; v7.5: v7.5: section_lines v2 (B along the bank: looks at the stream, no water bars); v7.4: v7.4: cut marks = two end arrows, no line between (pages_common v3.14); v7.3: v7.3: scale + north ignore the node frame line; v7.2: v7.2: the proposal from his masterplan SVG (MasterplanBase cache); v7.1: v7.1: R01 cut arrows (pc_cut_mark), no city-square ring, land-use columns >= 45 mm; v7: v7: every drawing fills its room on the A3 sheet, no 1:x printed (scale bars kept); v6.7: v6.7: no sources on the page (log only); v6.6: v6.6: scale + north to the emptiest plan corner; V1 also clear of link lines; v6.5: v6.5: V1 placed clear of labels; light backing behind plan labels; v6.4: v6.4: no repeats (R4 R5 R10): only the city-square stop, loop stops in the frame, no plant callouts; v6.3: v6.3: level marker stack (layer "levels") left out of the cuts; v6.2: v6.2: own section header (cached title block dropped), scales to 1:3000, land-use columns fit; v6.1: v6.1: cut items from cuts/<name>.json (Sections v1.6.5); v6: sections read from the Sections cache (cuts.json); v5   # v5: the plan context is the shared MapBase (mb_draw), Aras 12:17-12:18 UTC   # v4: brief plan rules (existing vs proposal, V1 viewpoint, program + building placeholders)   # v2: also output/presentation/<slide>.pdf (Aras 14 Nov 11:22 UTC)
ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
PAGE_W, PAGE_H = 420.0, 297.0
NODE_MARGIN_M = 25.0                       # m of town round the node frame on the plan
MP_EXISTING = ("ev-yol", "builts2")   # v10: his copy of the existing roads / buildings: MapBase draws those
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
            "su_bitkii": (False, u"water planting"), "yol_kenar": (False, u"street edges"),
            "PLANTING_v13_1": (False, u"trees (planting plan)"), "begum_su_merdiven": (False, u"water steps")}
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


# v12.7 (Aras 15 Nov 14:47 UTC "fill the placeholders"): the program brief, from
# library/node_ideas_2026-11-15/NODE_IDEAS.md (DESIGN; room areas are our proposal, totals = sum of the rooms, calculated)
PROGRAM = {
    "N1": (u"Neighbourhood house in the west park, ~500 m2 proposed: hall 200, kitchen 80, 3 workshops of 40, "
           u"children 60, tool and seed library 40; a waiting room for the village buses.",
           u"For: the Upper and Lower Neighbourhoods, riders of the village buses 831-833."),
    "N2": (u"Heritage walk point, ~400 m2 proposed: exhibition 250, info 40, café 80, lookout. Terraces step into the "
           u"river upstream of the bridge; the bank road splits into a ramp and seating; the hamam ruin becomes an open "
           u"room; 5 story markers.",
           u"For: heritage loop walkers (stop 4), hub K4, riders of the village buses 831-833."),
    "N3": (u"Craft and produce hall, ~850 m2 proposed: market 600, 3 workshop / sales rooms of 60, arrival + WC 60. "
           u"Viewing steps at the upstream tunnel mouth, the water line in the İstiklal paving, a live flow marker; the "
           u"stream stays covered (Roman tunnels; culvert work needs DSİ).",
           u"For: bazaar traders and makers, arrivals at transit hub T, heritage loops 3 and 5."),
    "N4": (u"No building. People gather where the stream leaves the tunnels; a bank-level route runs to Üç Kemer; a "
           u"raised canopy platform on the north bank never touches the monument.",
           u"For: visitors of heritage stop 2 and transit hub T."),
    "N5": (u"Day-care and sports pavilion, ~280 m2 proposed: day-care 150, changing + WC 100, store 30; courts on "
           u"the dry terraces.",
           u"For: families of the settled housing, riders of the town buses 651-653 and 656."),
    "N6": (u"Water-enrichment research and education centre, ~1,560 m2 proposed. Industry: 2 labs of 80, pilot "
           u"enrichment line 150 (in the irrigation line, never in the stream), canteen 200, showers 80, training "
           u"workshop 120. Education, open to all: display hall 250, 2 classrooms of 60, course room 80, greenhouse "
           u"400 + trial plots (cotton, maize, tomato).",
           u"For: industry workers, DEÜ Bergama MYO students, anyone interested."),
}


# ================================================================ v12: why-here diagrams from the real cut (Aras 15 Nov
# 10:36 UTC "this diagram is just so wrong and really conducted in a bad way please revise these diagrams for nodes")
DG_HALF_M = 80.0          # the cut in view: this far either side of the stream's channel middle (m)
DG_DEPTH_M = 50.0         # the block runs this far back along the view (m; v12.1: 50, his canopies lie 25-56 m off N2-A)
DG_OX, DG_OY = 0.55, 0.32 # oblique: 1 m of depth -> (0.55, 0.32) m on the page drawing
DG_BASE_M = 2.5           # poché under the lowest bed (m)
DG_BLD_DEPTH_M = 10.0     # a house's depth when only its front is known (ASSUMED, as the Sections background)
DG_ARCHES = {"K5": 3}     # arch counts known by name only: Üç Kemer = "three arches"
DG_LEVELS = (("q500", u"Q500"), ("q100", u"Q100"), (("winter", 3.36), u"WINTER"), (("spring", 0.752), u"SPRING"),
             (("autumn", 0.423), u"AUTUMN"))
DG_HARD = (u"Stepped terraces", u"Water deck", u"Square", u"Promenade", u"Pavilion", u"Canopy", u"Footbridge")


def _dp(P, tol):
    """Douglas-Peucker on a profile [(s, z)]"""
    if len(P) < 3:
        return list(P)
    a, b = P[0], P[-1]
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1e-9
    i_, d_ = 0, -1.0
    for i in range(1, len(P) - 1):
        d = abs((b[0] - a[0]) * (a[1] - P[i][1]) - (a[0] - P[i][0]) * (b[1] - a[1])) / L
        if d > d_:
            i_, d_ = i, d
    if d_ <= tol:
        return [a, b]
    return _dp(P[:i_ + 1], tol)[:-1] + _dp(P[i_:], tol)


# v12.1 (Aras 15 Nov 12:10 UTC "review the drawings yourself and compare with the examples that i have sent you before"):
# the block drawn like his liked examples (library/examples/liked_2026-11-12: white complete context, ONE heavy line,
# the project the only colour): white planes with hairline folds, his masterplan move laid on the ground in depth,
# his canopy triangles lifted and folded, his planted trees and people as his asset cutouts, one movement arrow
DG_CUT_DIR = os.path.join(ROOT, "Data", "cutouts")
DG_TREE_H_M = {"stone_pine": 20.0, "plane": 32.5, "ash": 17.5, "willow": 22.5, "olive": 7.5, "tamarisk": 4.0}  # = Sections v1.26 TREE_H_M (sourced there)
DG_TREE_LAYERS = (("trees_plane", "plane"), ("trees_ash", "ash"), ("trees_stone_pine", "stone_pine"))  # rosemary: a shrub
DG_MP_GREEN = ("master/kesin_yesil", "master/belki_yesil")
DG_MP_HARD = ("begum_su_merdiven/outline-2", "bisiklet/yeni", "yuruyus/iskele_kenari", "yuruyus/circulation", "desings")
DG_STOREY_M, DG_STOREY_SACRED_M = 3.0, 5.0   # Aras 12 Nov answers: storey 3.0 m, sacred 5.0 m
DG_KIZIL_H_M = 19.0       # Kızıl Avlu walls (Sections v1.18.1: Wikipedia "Its walls still survive up to a height of 19 metres")
DG_MP_LINES = ("teras_-_canopy/teras",)
DG_MP_FRAMES = ("yuruyus/bina_cerceve", "yuruyus/bina_cerceve/outline")
DG_MP_CANOPY = "teras_-_canopy/kanopi"
DG_CANOPY_CLEAR_M, DG_CANOPY_FREE_M, DG_CANOPY_RISE_M = 2.30, 0.60, 1.80   # = Sections v1.26 (rise ASSUMED there)
_DG_LIB = {}


def _dp_ring(P, tol):
    """Douglas-Peucker on a ring (its two halves split at the corner farthest from the first point)"""
    P = [tuple(p) for p in P]
    if len(P) > 1 and P[0] == P[-1]:
        P = P[:-1]
    if len(P) < 4:
        return P
    i_ = max(range(len(P)), key=lambda i: (P[i][0] - P[0][0]) ** 2 + (P[i][1] - P[0][1]) ** 2)
    return _dp(P[:i_ + 1], tol)[:-1] + _dp(P[i_:] + [P[0]], tol)[:-1]


def _dg_inside(q, P):
    c_ = False
    j = len(P) - 1
    for i in range(len(P)):
        if (P[i][1] > q[1]) != (P[j][1] > q[1]) and \
                q[0] < (P[j][0] - P[i][0]) * (q[1] - P[i][1]) / (P[j][1] - P[i][1]) + P[i][0]:
            c_ = not c_
        j = i
    return c_


def _dg_lerp(a, b, v, i):
    t = (v - a[i]) / (b[i] - a[i])
    return tuple(a[k] + (b[k] - a[k]) * t for k in range(len(a)))


def _dg_clip(P, box):
    """Sutherland-Hodgman of a ring [(x, d, ...)] to box (x0, x1, d0, d1); other coordinates interpolated"""
    for i, v, ge in ((0, box[0], True), (0, box[1], False), (1, box[2], True), (1, box[3], False)):
        if not P:
            break
        Q = []
        for j in range(len(P)):
            a, b = P[j - 1], P[j]
            ia, ib = (a[i] >= v) if ge else (a[i] <= v), (b[i] >= v) if ge else (b[i] <= v)
            if ib:
                if not ia:
                    Q.append(_dg_lerp(a, b, v, i))
                Q.append(b)
            elif ia:
                Q.append(_dg_lerp(a, b, v, i))
        P = Q
    return P


def _dg_seg(a, b, box):
    """Liang-Barsky: the part of segment a-b inside box (x0, x1, d0, d1), or None"""
    t0, t1 = 0.0, 1.0
    for i, v, ge in ((0, box[0], True), (0, box[1], False), (1, box[2], True), (1, box[3], False)):
        fa, fb = (a[i] - v, b[i] - v) if ge else (v - a[i], v - b[i])
        if fa < 0 and fb < 0:
            return None
        if fa < 0:
            t0 = max(t0, fa / (fa - fb))
        elif fb < 0:
            t1 = min(t1, fa / (fa - fb))
    if t1 <= t0 + 1e-9:
        return None
    return (tuple(a[k] + (b[k] - a[k]) * t0 for k in range(2)), tuple(a[k] + (b[k] - a[k]) * t1 for k in range(2)))


def _dg_cutout(items, key, cx, yb, h, n=0, depth=0, flip=False, layer="concept"):
    """one asset-library cutout (Data/cutouts, as the Sections cutout()) standing at page (cx, yb), h mm tall;
    False when the library or the file is missing"""
    lib = _DG_LIB.get("lib")
    if lib is None:
        lib = {}
        try:
            with open(os.path.join(DG_CUT_DIR, "cutouts.json"), encoding="utf-8") as f:
                js = json.load(f).get("cutouts", {})
            for k_, v_ in js.items():
                lib[k_] = [e for e in (v_ if isinstance(v_, list) else [v_])
                           if os.path.isfile(os.path.join(DG_CUT_DIR, e.get("file", "")))]
        except Exception:
            lib = {}
        _DG_LIB["lib"] = lib
    es = lib.get(key) or []
    if not es:
        return False
    e = es[n % len(es)]
    f_ = (e.get("depth") or {}).get(str(depth)) if depth else None
    p = os.path.join(DG_CUT_DIR, f_ if f_ and os.path.isfile(os.path.join(DG_CUT_DIR, f_)) else e["file"])
    sz = _DG_LIB.get(p)
    if sz is None:
        with open(p, "rb") as f:
            hd = f.read(24)
        sz = _DG_LIB[p] = (int.from_bytes(hd[16:20], "big"), int.from_bytes(hd[20:24], "big"))
    w = h * sz[0] / float(sz[1])
    items.append(("image", cx - w / 2.0, yb, w, h, p, None, bool(flip), None, layer))
    return True


def _dg_aspect(key, n=0):
    """width / height of a cutout (1.0 when unknown), to keep trees inside the box"""
    probe = []
    if not _dg_cutout(probe, key, 0.0, 0.0, 1.0, n):
        return None
    return probe[0][3]


def concept_cut(node, items, x0, y0, W, H, G, C, D, MPC, log, MC=None):
    """the node's A cut across the stream as an open section-axo block in the language of his liked examples: the
    surveyed ground and bed of the Sections cache at true proportions as white planes with hairline folds and one heavy
    cut line, every computed water level, his masterplan move (terraces, water stairs, cycle path, green, building
    frames) laid on the ground in depth, his canopy triangles lifted and folded on Y columns, his planted trees and
    people as his asset cutouts, the buildings and bridges in depth in white, one movement arrow from the dry top down to
    the water. Returns False (old diagram kept) when the cut has no profile."""
    J = C.J or {}
    V = [tuple(p) for p in (J.get("surface") or []) if p is not None and len(p) >= 2]
    if len(V) < 3 or not C.crosses:
        log.append(u"FLAG diagram %s: the A cut has no surface profile across the stream in the Sections cache; "
                   u"old diagram kept" % node)
        return False
    V.sort(key=lambda p: p[0])
    ch = J.get("channel") or [C.s_th, C.s_th]
    sm = (ch[0] + ch[1]) / 2.0 if ch[1] > ch[0] + 0.5 else C.s_th
    LAY = (MPC or {}).get("layers") or {}
    u = ((C.B[0] - C.A[0]) / C.L, (C.B[1] - C.A[1]) / C.L)
    sd0 = lambda xy: ((xy[0] - C.A[0]) * u[0] + (xy[1] - C.A[1]) * u[1],
                      -(xy[0] - C.A[0]) * u[1] + (xy[1] - C.A[1]) * u[0])
    # the block looks from the side of the cut where more of his move lies (canopies count 3): both sides counted
    # inside the block's reach; seen from the far side the cut is mirrored (a true view from there)
    score = [0, 0]
    for kk in (DG_MP_CANOPY,) + DG_MP_HARD + DG_MP_FRAMES + DG_MP_LINES:
        for r_ in LAY.get(kk, []):
            if len(r_[4]) < 2:
                continue
            q_ = [sd0(p) for p in r_[4]]
            q_ = [p for p in q_ if abs(p[0] - sm) <= DG_HALF_M and abs(p[1]) <= DG_DEPTH_M]
            for i_, ok_ in ((0, any(p[1] > 0.0 for p in q_)), (1, any(p[1] < 0.0 for p in q_))):
                score[i_] += (3 if kk == DG_MP_CANOPY else 1) if ok_ else 0
    flip = score[1] > score[0]
    if flip:
        V = sorted((C.L - s, z) for s, z in V)
        ch = [C.L - ch[1], C.L - ch[0]]
        sm = C.L - sm
    sd = (lambda xy: (lambda q: (C.L - q[0], -q[1]))(sd0(xy))) if flip else sd0
    lo, hi = max(V[0][0], sm - DG_HALF_M), min(V[-1][0], sm + DG_HALF_M)

    def zs(s):
        for a, b in zip(V, V[1:]):
            if a[0] <= s <= b[0]:
                return a[1] if b[0] - a[0] < 1e-9 else a[1] + (b[1] - a[1]) * (s - a[0]) / (b[0] - a[0])
        return V[0][1] if s < V[0][0] else V[-1][1]
    prof = _dp([(lo, zs(lo))] + [p for p in V if lo < p[0] < hi] + [(hi, zs(hi))], 0.12)
    zbed = min(p[1] for p in prof)
    zb0 = zbed - DG_BASE_M - 3.0                        # local y = z - zb0: 3 m of room under the cut for names
    X = lambda s: s - lo
    Y = lambda z: z - zb0
    g = [(X(s), Y(z)) for s, z in prof]

    def gyl(x):                                         # the drawn (simplified) ground, so things sit on the planes
        for a, b in zip(g, g[1:]):
            if a[0] <= x <= b[0]:
                return a[1] if b[0] - a[0] < 1e-9 else a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0])
        return g[0][1] if x < g[0][0] else g[-1][1]

    # ---- levels (computed by Sections: Manning on the surveyed cut), merged when within 0.15 m
    lev = []
    for key, name in DG_LEVELS:
        v = C.levels.get(key)
        if v and v[0] is not None and v[0] > zbed + 0.05 and not any(abs(v[0] - z_) < 0.15 for z_, _n in lev):
            lev.append((v[0], name))
    lev.sort()
    q500 = (C.levels.get("q500") or (None,))[0]

    def wet(z):
        """where the level z meets the banks either side of the channel middle"""
        a = b = sm
        while a > lo and zs(a) < z:
            a -= 0.25
        while b < hi and zs(b) < z:
            b += 0.25
        return X(a), X(b)

    # ---- what stands on and behind the line
    xd = lambda xy: (lambda q: (X(q[0]), q[1]))(sd(xy))
    parts = [((C.L - b, C.L - a, lab) if flip else (a, b, lab)) for a, b, lab in (J.get("parts") or [])]
    parts = [(max(lo, a), min(hi, b), lab) for a, b, lab in parts if b > lo and a < hi]
    her = []
    for h_ in list(D.get("heritage", [])) + list(D.get("heritage_dots", [])):
        s_, d_ = sd(h_["xy"])
        if lo <= s_ <= hi and -5.0 <= d_ <= 120.0:
            her.append((s_, d_, h_["name"]))
    bridges = []
    names = D.get("hub_names", {})
    for code, xy in (D.get("hubs") or {}).items():
        if not code.startswith(u"K"):
            continue
        s_, d_ = sd(xy)
        if not (lo - 20.0 <= s_ <= hi + 20.0 and 0.0 <= d_ <= DG_DEPTH_M + 30.0):
            continue
        pts = []                                          # v12.2: the bridge lines of MapBase (existing context)
        for cl_, P_ in ((MC or {}).get("lines") or {}).get("bridges") or []:
            if len(P_) >= 2 and min(math.hypot(p[0] - xy[0], p[1] - xy[1]) for p in P_) <= 40.0:
                pts += [sd(p) for p in P_]
        if len(pts) >= 3:
            sa, sb = min(p[0] for p in pts), max(p[0] for p in pts)
            da, db = min(p[1] for p in pts), max(p[1] for p in pts)
            src = u"MapBase bridge lines"
        else:
            sa, sb, da, db = ch[0] - 2.0, ch[1] + 2.0, d_ - 3.0, d_ + 3.0
            src = u"channel width on the cut (no outline found)"
        sa, sb = max(lo, sa), min(hi, sb)
        da, db = max(0.5, da), min(DG_DEPTH_M + 30.0, db)
        if sb - sa > 2.0 and db > da:
            bridges.append((da, db, sa, sb, code, names.get(code, code)))
            log.append(u"diagram %s: bridge %s %.0f-%.0f m behind the cut, span s %.0f-%.0f (%s)" % (
                node, names.get(code, code), da, db, sa, sb, src))
    Dm = max([DG_DEPTH_M] + [min(db, DG_DEPTH_M + 30.0) for da, db, sa, sb, c_, n_ in bridges])
    BOX = (0.0, X(hi), 0.0, Dm)
    blds = []                                           # v12.2: every house from MapBase (below)
    # ---- the houses inside the block from MapBase (Aras 15 Nov 13:41 "every 3D, 2D or whatever the drawing is should
    # use the basemap and it's extruded version"): its survey floors x his storey heights (Aras 12 Nov: 3.0 m, sacred
    # 5.0 m); no floors recorded = laid flat (height unknown); a heritage place inside a footprint marks it; Kızıl
    # Avlu roofless at its 19 m walls
    houses, n_flat = [], 0
    MB_ = MC or {}
    for i_, b_ in enumerate(MB_.get("bld") or []):
        R_ = b_[0]
        if len(R_) < 3:
            continue
        P_ = [xd(p) for p in R_]
        if max(p[0] for p in P_) < 0.0 or min(p[0] for p in P_) > X(hi) or max(p[1] for p in P_) < 0.0 or \
                min(p[1] for p in P_) > Dm:
            continue
        P_ = _dg_clip([xd(p) for p in _dp_ring(R_, 0.2)], BOX)
        if len(P_) < 3:
            continue
        fab = b_[1]
        fl = ((MB_.get("bld_x") or [])[i_][0] if i_ < len(MB_.get("bld_x") or []) else 0) or 0
        nm_ = (b_[4] if len(b_) > 4 else u"") or u""
        hit = [n_ for s_, d_, n_ in her if _dg_inside((X(s_), d_), P_)]
        her_ = bool(hit) or fab in (u"monument", u"sacred")
        kz = any(u"Kızıl" in t_ for t_ in hit + [nm_])
        try:
            fl = float(fl)
        except Exception:
            fl = 0.0
        h = DG_KIZIL_H_M if kz else (fl * (DG_STOREY_SACRED_M if fab == u"sacred" else DG_STOREY_M) if fl > 0 else None)
        ar_ = abs(sum(P_[i][0] * P_[i - 1][1] - P_[i - 1][0] * P_[i][1] for i in range(len(P_)))) / 2.0
        if h is not None and ar_ < 15.0:                  # a sliver cut by the block edge: laid flat, no tower
            h = None
        houses.append((P_, h, u"roofless" if kz else her_))
        n_flat += h is None

    # ---- his canopy triangles (masterplan), lifted: valleys at max(ground + 2.30, Q500 + 0.60), ridges 1.80 higher,
    # valley / ridge alternating along the cut; corners found by simplifying each drawn triangle
    tris, vk = [], {}
    for r_ in LAY.get(DG_MP_CANOPY, []):
        if r_[0] != "r" or len(r_[4]) < 3:
            continue
        P_ = [xd(p) for p in r_[4]]
        if max(p[0] for p in P_) < 0.0 or min(p[0] for p in P_) > X(hi) or max(p[1] for p in P_) < 0.0 or \
                min(p[1] for p in P_) > Dm:
            continue
        cs = _dp_ring(r_[4], 0.6)
        if len(cs) < 3:
            continue
        keys = []
        for p in cs:
            kq = (int(round(p[0] / 1.0)), int(round(p[1] / 1.0)))
            vk.setdefault(kq, xd(p))
            keys.append(kq)
        tris.append(keys)
    order = sorted(vk, key=lambda kq: vk[kq][0])
    zfloor = (Y(q500) + DG_CANOPY_FREE_M) if q500 is not None else -1e9
    VZ = {}
    for i_, kq in enumerate(order):
        x_, d_ = vk[kq]
        valley = max(gyl(x_) + DG_CANOPY_CLEAR_M, zfloor)
        VZ[kq] = (valley + (DG_CANOPY_RISE_M if i_ % 2 else 0.0), i_ % 2 == 0)
    facets = []
    for keys in tris:
        P3 = _dg_clip([(vk[kq][0], vk[kq][1], VZ[kq][0]) for kq in keys], BOX)
        if len(P3) >= 3:
            facets.append(P3)
    cols = [(vk[kq][0], vk[kq][1], VZ[kq][0]) for kq in order if VZ[kq][1] and
            0.0 <= vk[kq][0] <= X(hi) and 0.0 <= vk[kq][1] <= Dm and any(kq in t for t in tris)]

    # ---- his planted trees (PLANTING layer) inside the block, as his cutouts at the sourced heights (Sections v1.26)
    trees = []
    for lay_, sp in DG_TREE_LAYERS:
        recs = [v_ for kk, v_ in LAY.items() if kk.split(u"/")[-1] == lay_]
        for i_, r_ in enumerate([r_ for v_ in recs for r_ in v_ if len(r_[4]) >= 3]):
            cx_ = sum(p[0] for p in r_[4]) / len(r_[4])
            cy_ = sum(p[1] for p in r_[4]) / len(r_[4])
            x_, d_ = xd((cx_, cy_))
            if 1.0 <= x_ <= X(hi) - 1.0 and 0.0 <= d_ <= Dm:
                asp = _dg_aspect(sp, i_)
                if asp is None:
                    continue
                trees.append((x_, d_, DG_TREE_H_M[sp], sp, i_, asp))

    # ---- page fit at true proportions (trees, canopies and buildings inside the box)
    top = max(p[1] for p in g)
    for bb in blds:
        xm = X((bb[0] + bb[1]) / 2.0)
        top = max(top, gyl(xm) + min(bb[2], 24.0) + (DG_OY * min(bb[4], Dm) if not bb[3] else 0.0))
    for x_, d_, h_, sp, i_, asp in trees:
        top = max(top, gyl(x_) + h_ + DG_OY * d_)
    for P3 in facets:
        top = max([top] + [p[2] + DG_OY * p[1] for p in P3])
    if q500 is not None:
        top = max(top, Y(q500) + 4.5)
    lw_, lh_ = X(hi) + DG_OX * Dm, top + DG_OY * Dm + 1.0
    k = min(W / lw_, H / lh_)
    x0p = x0 + (W - lw_ * k) / 2.0
    K = G["pc_dg_kit"](items, x0p, y0, lw_ * k, lh_ * k, "concept", lw=lw_, lh=lh_, dash_at=4)
    PG = lambda p: (x0p + p[0] * k, y0 + p[1] * k)
    Cc, Wt = K["C"], K["W"]
    poly, line = K["poly"], K["line"]
    hair = Wt["hair"]
    INK_, M_FR, M_SIDE = Cc["ink"], Cc["move"], "9E5F1F"
    T_FLAT, T_DOWN, T_UP, T_EDGE = "FFFFFF", "F8F7F4", "F1EFEA", "CFCAC1"
    W_FR, W_TOP, W_SIDE, W_LN = "FFFFFF", "FFFFFF", "F3F1ED", "8F887E"
    o = lambda p, d: (p[0] + DG_OX * d, p[1] + DG_OY * d)
    hard = [(X(a), X(b), lab) for a, b, lab in parts if lab in DG_HARD]
    wl = next((z_ for z_, n_ in lev if n_ == u"AUTUMN"), lev[0][0] if lev else None)
    wa, wb = wet(wl) if wl is not None else (None, None)

    # 1. the land behind the cut: white planes, hairline folds; the bed under the water first, then the water plane,
    # then the land above it (so the water lies in its bed), the faces turned to us last
    segs = []
    for a, b in zip(g, g[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        if abs(dx) < 1e-9 and abs(dy) < 1e-9:
            continue
        vis = dx * DG_OY - dy * DG_OX > 1e-9
        tone = T_FLAT if abs(dy) < 0.08 * abs(dx) else (T_DOWN if dy < 0 else T_UP)
        low = wl is not None and max(a[1], b[1]) <= Y(wl) + 1e-6
        segs.append((a, b, vis, tone, low))
    for a, b, vis, tone, low in sorted([s_ for s_ in segs if s_[4]], key=lambda t: t[2]):
        poly([a, b, o(b, Dm), o(a, Dm)], tone, T_EDGE, hair * 0.7)
    if wl is not None:
        poly([(wa, Y(wl)), (wb, Y(wl)), o((wb, Y(wl)), Dm), o((wa, Y(wl)), Dm)], "DCE7E7", "BFD0D0", hair * 0.7)
    for a, b, vis, tone, low in sorted([s_ for s_ in segs if not s_[4]], key=lambda t: t[2]):
        poly([a, b, o(b, Dm), o(a, Dm)], tone, T_EDGE, hair * 0.7)
    line([o(p, Dm) for p in g], W_LN, hair)

    # 2. his masterplan move laid on the ground in depth: each footprint cut to the dry faces turned to us and laid on
    # them exactly (each face is a plane); green pale, the move in accent, our building frames dashed
    dry = [(a, b) for a, b, vis, tone, low in segs if vis and not low and b[0] > a[0] + 1e-6]
    on = lambda a, b, p: o((p[0], a[1] + (b[1] - a[1]) * (p[0] - a[0]) / (b[0] - a[0])), p[1])
    n_fp = {}

    def lay_ring(P_, fill, stroke, w):
        for a, b in dry:
            Q = _dg_clip(P_, (a[0], b[0], 0.0, Dm))
            if len(Q) >= 3:
                poly([on(a, b, q) for q in Q], fill, stroke, w)

    def lay_line(P_, col, w, dash=None):
        for a, b in dry:
            for p, q in zip(P_, P_[1:]):
                r = _dg_seg(p, q, (a[0], b[0], 0.0, Dm))
                if r:
                    line([on(a, b, r[0]), on(a, b, r[1])], col, w, dash)
    near = lambda P_: not (max(p[0] for p in P_) < 0.0 or min(p[0] for p in P_) > X(hi) or
                           max(p[1] for p in P_) < 0.0 or min(p[1] for p in P_) > Dm)
    n_mb = {}                                           # v12.2: MapBase streets and parks draped on the ground
    for key_, fill_, st_ in (("parks", "F1F3EC", "C5CBB5"), ("street_net", "FAFAF8", "D2CDC4"),
                             ("streets", "FAFAF8", "D2CDC4"), ("streets_town", "FAFAF8", "D2CDC4")):
        for R_ in ((MC or {}).get("polys") or {}).get(key_) or []:
            if len(R_) < 3:
                continue
            P_ = [xd(p) for p in R_]
            if not near(P_):
                continue
            n_mb[key_] = n_mb.get(key_, 0) + 1
            lay_ring([xd(p) for p in _dp_ring(R_, 0.25)], fill_, st_, hair * 0.6)
    for P_, h, her_ in houses:                         # flat house footprints: white with a hairline
        if h is None:
            lay_ring(P_, "F4E9E4" if her_ else "F2F0EB", Cc["her"] if her_ else W_LN, hair * (1.6 if her_ else 0.8))
    for kk, fill, stroke, w, ring in [(kk, "EEF1E6", "A3AD8A", hair * 0.8, True) for kk in DG_MP_GREEN] + \
            [(kk, "F6E4CE", M_FR, hair * 1.2, True) for kk in DG_MP_HARD] + \
            [(kk, None, M_FR, hair * 1.2, False) for kk in DG_MP_LINES] + \
            [(kk, None, M_FR, hair * 1.6, None) for kk in DG_MP_FRAMES]:
        for r_ in LAY.get(kk, []):
            if len(r_[4]) < 2 or r_[0] not in ("r", "l"):
                continue
            if ring and (r_[0] != "r" or r_[1] is not None and kk in DG_MP_GREEN):
                continue                                  # green: his outlined areas only (the filled bits are texture)
            P_ = [xd(p) for p in (_dp_ring(r_[4], 0.25) if r_[0] == "r" else _dp(list(r_[4]), 0.25))]
            if not near(P_):
                continue
            n_fp[kk] = n_fp.get(kk, 0) + 1
            if ring:
                lay_ring(P_, fill, stroke, w)
            elif ring is None:
                lay_line(P_ + [P_[0]], stroke, w, (1.2, 0.8))
            else:
                lay_line(P_, stroke, w)
    if not LAY:                                         # no masterplan cache: our ground on the cut tinted instead
        for a, b in dry:
            if any(ha - 0.3 <= a[0] and b[0] <= hb + 0.3 for ha, hb, l_ in hard):
                poly([a, b, o(b, Dm), o(a, Dm)], "F6E4CE", T_EDGE, hair * 0.7)

    # 3. bridges, buildings, trees, canopy, people: far to near (painter's order), each on the extruded ground
    things = [("bridge", x_[0], x_) for x_ in bridges] + \
             [("bld", (bb[4] if not bb[3] else 0.0), bb) for bb in blds] + \
             [("tree", t_[1], t_) for t_ in trees] + \
             [("house", min(p[1] for p in h_[0]), h_) for h_ in houses if h_[1] is not None] + \
             [("col", c_[1] + 0.01, c_) for c_ in cols] + \
             [("facet", sum(p[1] for p in P3) / len(P3), P3) for P3 in facets]
    big = max(hard, key=lambda t: t[1] - t[0]) if hard else None
    if big:
        for i_, (f_, dd) in enumerate(((0.3, 3.0), (0.55, 5.5), (0.8, 8.0))):
            things.append(("person", dd, (big[0] + (big[1] - big[0]) * f_, dd, i_)))
    if not facets:                                      # no canopy triangles in his plan here: the cut's canopy part
        for a, b, lab in hard:
            if lab == u"Canopy":
                things.append(("canopy_part", 2.0, (a, b)))
    for kind, dist, it in sorted(things, key=lambda t: -t[1]):
        if kind == "bridge":
            da, db, sa, sb, code, name = it
            xa, xb = X(sa), X(sb)
            zdeck = max(gyl(xa), gyl(xb))
            n = DG_ARCHES.get(code, 0)
            d0, d1 = min(da, Dm), min(db, Dm)
            poly([o((xa, zdeck), d0), o((xb, zdeck), d0), o((xb, zdeck), d1), o((xa, zdeck), d1)], W_TOP, W_LN, hair)
            fr = [(xa, zdeck), (xb, zdeck), (xb, zdeck - 1.0), (xa, zdeck - 1.0)]
            if n:
                ybed = Y(zbed) + 0.3
                span = (xb - xa) / n
                fr = [(xa, zdeck), (xb, zdeck), (xb, ybed)]
                for i in range(n - 1, -1, -1):
                    ca, cb = xa + span * i + span * 0.12, xa + span * (i + 1) - span * 0.12
                    r_ = (cb - ca) / 2.0
                    spring = max(ybed, zdeck - 1.0 - r_)
                    fr += [(cb, ybed), (cb, spring)] + [((ca + cb) / 2.0 + r_ * math.cos(math.radians(t_)),
                                                         spring + r_ * math.sin(math.radians(t_)))
                                                        for t_ in range(0, 181, 15)] + [(ca, spring), (ca, ybed)]
                fr += [(xa, ybed)]
            poly([o(p, d0) for p in fr], W_FR, Cc["her"] if code in (u"K3", u"K4", u"K5") else W_LN, hair * 1.6)
            line([o((xa, zdeck + 0.9), d0), o((xb, zdeck + 0.9), d0)], W_LN, hair)
        elif kind == "bld":
            a, b, h, cut, behind, hname = it
            xa, xb = X(a), X(b)
            d0 = 0.0 if cut else behind
            d1 = min(Dm, d0 + DG_BLD_DEPTH_M)
            yb = max(gyl(xa), gyl(xb))
            st_c, w_ = (W_LN, hair * 1.3) if hname is None else (Cc["her"], hair * 2.0)
            if hname and u"Kızıl" in hname:            # the Red Hall stands roofless: back wall, side, open rim
                poly([o((xa, yb), d1), o((xb, yb), d1), o((xb, yb + h), d1), o((xa, yb + h), d1)], "F4E9E4", st_c, hair)
                poly([o((xb, yb), d0), o((xb, yb), d1), o((xb, yb + h), d1), o((xb, yb + h), d0)], "EFE1DA", st_c, hair)
                poly([o((xa, yb), d0), o((xb, yb), d0), o((xb, yb + h), d0), o((xa, yb + h), d0)], "F8F0EC", st_c, w_)
                line([o((xa, yb + h), d0), o((xa, yb + h), d1), o((xb, yb + h), d1)], st_c, hair)
                continue
            if d1 > d0 + 0.5:
                poly([o((xb, yb), d0), o((xb, yb), d1), o((xb, yb + h), d1), o((xb, yb + h), d0)], W_SIDE, st_c, hair)
                poly([o((xa, yb + h), d0), o((xb, yb + h), d0), o((xb, yb + h), d1), o((xa, yb + h), d1)], W_TOP, st_c,
                     hair)
            poly([o((xa, yb), d0), o((xb, yb), d0), o((xb, yb + h), d0), o((xa, yb + h), d0)], W_FR, st_c, w_)
        elif kind == "house":
            P_, h, her_ = it
            roof = max(gyl(p[0]) for p in P_) + h
            st_c, w_ = (Cc["her"], hair * 1.8) if her_ else (W_LN, hair)
            walls = []
            for p, q in zip(P_, P_[1:] + P_[:1]):
                walls.append(((p[1] + q[1]) / 2.0, [o((p[0], gyl(p[0])), p[1]), o((q[0], gyl(q[0])), q[1]),
                                                    o((q[0], roof), q[1]), o((p[0], roof), p[1])]))
            for d_, q in sorted(walls, key=lambda t: -t[0]):
                poly(q, "F4E9E4" if her_ == u"roofless" else W_SIDE, st_c, w_)
            if her_ == u"roofless":                       # Kızıl Avlu stands roofless: its wall tops as an open rim
                line([o((p[0], roof), p[1]) for p in P_ + P_[:1]], st_c, w_)
            else:
                poly([o((p[0], roof), p[1]) for p in P_], W_TOP, st_c, w_)
        elif kind == "tree":
            x_, d_, h_, sp, i_, asp = it
            p = PG(o((x_, gyl(x_)), d_))
            wl_ = h_ * asp / 2.0                         # half the crown in local m: kept inside the box
            if x_ + DG_OX * d_ - wl_ >= 0.0 and x_ + DG_OX * d_ + wl_ <= lw_:
                _dg_cutout(items, sp, p[0], p[1], h_ * k, i_, 1 if d_ >= 40.0 else 0, i_ % 2 == 1)
        elif kind == "col":
            x_, d_, z_ = it                              # a Y column under a valley
            yg = gyl(x_)
            line([o((x_, yg), d_), o((x_, z_ - 1.0), d_)], M_SIDE, Wt["move"] * 0.8)
            line([o((x_ - 0.9, z_), d_), o((x_, z_ - 1.0), d_), o((x_ + 0.9, z_), d_)], M_SIDE, Wt["move"] * 0.8)
        elif kind == "facet":
            P3 = it
            e1 = [P3[1][j] - P3[0][j] for j in range(3)]
            e2 = [P3[2][j] - P3[0][j] for j in range(3)]
            nx_, nz_ = e1[1] * e2[2] - e1[2] * e2[1], e1[0] * e2[1] - e1[1] * e2[0]
            ny_ = e1[2] * e2[0] - e1[0] * e2[2]
            if ny_ < 0:
                nx_, nz_ = -nx_, -nz_
            tone = "F7E8D7" if nx_ <= 0 else "EAD0B4"   # facets turned to the light (left) paler: the fold reads
            poly([o((p[0], p[2]), p[1]) for p in P3], tone, M_FR, hair * 1.4)
        elif kind == "person":
            xp, dd, i_ = it
            p = PG(o((xp, gyl(xp)), dd))
            if not _dg_cutout(items, (u"person_stand", u"person_walk", u"person_stand")[i_], p[0], p[1], 1.75 * k, i_,
                              0, i_ == 1):
                q = o((xp, gyl(xp)), dd)
                line([(q[0], q[1]), (q[0], q[1] + 1.75)], INK_, hair * 2.0)
        elif kind == "canopy_part":
            a, b = it
            gmax = max([gyl(a), gyl(b)] + [p[1] for p in g if a <= p[0] <= b])
            valley = max(gmax + DG_CANOPY_CLEAR_M, zfloor)
            ridge = valley + DG_CANOPY_RISE_M
            d0, d1 = 2.0, min(Dm, 16.0)
            nb = max(2, int(round((b - a) / 6.0)))
            w_ = (b - a) / nb
            for i in range(nb + 1):
                xs = a + i * w_
                for dd in (d0 + 1.0, d1 - 1.0):
                    line([o((xs, gyl(xs)), dd), o((xs, valley - 1.0), dd)], M_SIDE, Wt["move"] * 0.8)
                    line([o((xs - 0.8, valley), dd), o((xs, valley - 1.0), dd), o((xs + 0.8, valley), dd)], M_SIDE,
                         Wt["move"] * 0.8)
            for i in range(nb):
                xa_, xm_, xb_ = a + i * w_, a + (i + 0.5) * w_, a + (i + 1) * w_
                for (pa, pb), tone in ((((xa_, valley), (xm_, ridge)), "F7E8D7"), (((xm_, ridge), (xb_, valley)), "EAD0B4")):
                    poly([o(pa, d0), o(pb, d0), o(pb, d1), o(pa, d1)], tone, M_FR, hair * 1.4)
    for a, b, lab in hard:
        if lab == u"Pavilion":
            yb = max(gyl(a), gyl(b))
            poly([o((a, yb), 1.0), o((b, yb), 1.0), o((b, yb + 3.5), 1.0), o((a, yb + 3.5), 1.0)], "F6E4CE", M_FR, hair * 1.6)

    # 4. the cut face: white below ONE heavy ground line, the water in the cut, our part of the line in accent
    yb0 = Y(zbed - DG_BASE_M)
    poly([(g[0][0], yb0)] + g + [(g[-1][0], yb0)], "FFFFFF", None, 0.0)
    if wl is not None:
        under = [p for p in g if wa <= p[0] <= wb and p[1] <= Y(wl) + 1e-6]
        poly([(wa, Y(wl))] + under + [(wb, Y(wl))], "C9D9D9", None, 0.0)
    line(g, INK_, 0.45)
    for a, b, lab in parts:
        seg = [p for p in g if X(a) - 1e-6 <= p[0] <= X(b) + 1e-6]
        if len(seg) >= 2 and lab != u"Green":
            line(seg, M_FR, 0.45)

    # 5. one movement arrow (dashed, accent): from the dry top of our largest move down to the water it opens
    if big and wl is not None:
        a, b = big[0], big[1]
        xs_ = a if gyl(a) >= gyl(b) else b
        xe_ = wa if abs(wa - xs_) < abs(wb - xs_) else wb
        if abs(xe_ - xs_) > 4.0 and gyl(xs_) > Y(wl) + 0.8:
            p0, p2 = (xs_, gyl(xs_) + 1.6), (xe_, Y(wl) + 0.5)
            p1 = ((p0[0] + p2[0]) / 2.0, max(p0[1], p2[1]) + 2.5)
            bz = [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0],
                   (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]) for t in [i / 16.0 for i in range(17)]]
            line(bz[:-1], M_FR, Wt["arrow"], (1.0, 0.6))
            ux_, uy_ = bz[-1][0] - bz[-3][0], bz[-1][1] - bz[-3][1]
            L_ = math.hypot(ux_, uy_) or 1.0
            ux_, uy_ = ux_ / L_, uy_ / L_
            hl = 1.4 / k                                  # the head 1.4 mm on the page
            poly([bz[-1], (bz[-1][0] - ux_ * hl - uy_ * hl * 0.45, bz[-1][1] - uy_ * hl + ux_ * hl * 0.45),
                  (bz[-1][0] - ux_ * hl + uy_ * hl * 0.45, bz[-1][1] - uy_ * hl - ux_ * hl * 0.45)], M_FR)

    # levels last: fine dashed lines bank to bank, names at the ends of their depth tails, kept apart
    last_y = -1e9
    for z_, name in lev:
        xa, xb = wet(z_)
        line([(xa, Y(z_)), (xb, Y(z_))], Cc["water_ln"], hair * 1.5, (1.0, 0.7))
        line([(xb, Y(z_)), o((xb, Y(z_)), Dm * 0.35)], Cc["water_ln"], hair, (1.0, 0.7))
        e_ = o((xb, Y(z_)), Dm * 0.35)
        ty = max(e_[1] - 0.2, last_y + 1.9 / k)
        K["text"](name, e_[0] + 0.6, ty, 1.4, Cc["water_ln"], True, "L")
        last_y = ty

    # 6. names under the ground on brackets: our move, heritage, bridges (at most 4)
    lab_ = []
    for a, b, lab in sorted(hard, key=lambda t: -(t[1] - t[0]))[:1]:
        lab_.append((a, b, lab.upper(), M_FR))
    for s_, d_, nm in her:
        if any(nm == b_[5] for b_ in bridges):
            continue
        lab_.append((max(0.0, X(s_) - 4.0), min(X(hi), X(s_) + 4.0), nm.upper(), INK_))
    for da, db, sa, sb, code, name in bridges:
        lab_.append((X(sa), X(sb), name.upper(), INK_))
    used = []
    for a, b, nm, col in lab_:
        if len(used) >= 4 or any(not (b < ua - 2.0 or a > ub + 2.0) for ua, ub in used):
            continue
        used.append((a, b))
        K["bracket"](a, b, 2.2, nm, col)
    log.append(u"diagram %s: cut %s s %.0f-%.0f m at true proportions (1 mm = %.2f m), levels %s, move %s, "
               u"%d buildings, %d house footprints (%d flat: height unknown), %d heritage, %d bridges, %d canopy facets, %d trees, "
               u"plan pieces %s, MapBase draped %s, seen from %s" % (
                   node, C.name, lo, hi, 1.0 / k, u", ".join(n_ for z_, n_ in lev) or u"none",
                   u", ".join(sorted(set(l_ for a_, b_, l_ in hard))) or u"none", len(blds), len(houses), n_flat, len(her), len(bridges),
                   len(facets), len(trees), u", ".join(u"%s %d" % (kk.split(u"/")[-1], v_) for kk, v_ in
                                                      sorted(n_fp.items())) or u"none",
                   u", ".join(u"%s %d" % kv for kv in sorted(n_mb.items())) or u"none",
                   u"the far side (mirrored: more of his move there)" if flip else u"the Sections side"))
    return True


def concept(node, items, x0, y0, W, H, G=None):
    """v10 (Aras 15 Nov 06:10 UTC "diagrams are awful ... should look really clear and abstract however not basic"):
    each node's one claim as a SECTION-AXO BLOCK (the cut model of the RPBW / BIG / Snøhetta concept diagrams): the cut
    face in poché with the one heavy ground line, the land behind it as shaded planes in oblique depth, the town as a
    regular row of small white blocks, heritage as its own built shape, the stream as a flat plane, our move the ONLY
    accent solid with its shadow, people on it, names under the ground on brackets. Not to scale; names from the story."""
    # the block's depth runs 13 units to the right: 205 x 47 local units fill the W x H box, nothing spills out
    K = G["pc_dg_kit"](items, x0, y0, W, H, "concept", lw=205.0, lh=36.0, dash_at=4)   # v11.2: no air band over it
    C, Wt = K["C"], K["W"]
    poly, line, lab, br = K["poly"], K["line"], K["label"], K["bracket"]
    OX, OY = 13.0, 8.5                                     # full depth of the block, oblique (local units)
    T_FLAT, T_DOWN, T_UP = "F4F1EB", "E9E4DA", "DED7CB"    # lit planes: flat, facing the light, facing away
    W_TOP, W_EDGE = "C3D2D1", "8FA6A5"
    M_FR, M_SIDE = C["move"], "9E5F1F"
    X_FR, X_TOP, X_SIDE, X_LN = "FFFFFF", "EFECE6", "E3DFD7", "9A938A"
    SHADOW = "CFC8BC"
    hair = Wt["hair"]

    def o(p, d):
        return (p[0] + OX * d, p[1] + OY * d)

    def steps(xa, xb, ya, yb, n):
        pts, dx, dy = [], (xb - xa) / float(n), (yb - ya) / float(n)
        for i in range(n):
            if yb < ya:                                   # down to the right: tread, then riser
                pts += [(xa + dx * (i + 1), ya + dy * i), (xa + dx * (i + 1), ya + dy * (i + 1))]
            else:                                         # up to the right: riser, then tread
                pts += [(xa + dx * i, ya + dy * (i + 1)), (xa + dx * (i + 1), ya + dy * (i + 1))]
        return pts

    def gy(g, x):
        for a, b in zip(g, g[1:]):
            if a[0] <= x <= b[0] and b[0] > a[0]:
                return a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0])
        return g[0][1] if x < g[0][0] else g[-1][1]

    TONE = {}

    def terrain(g, accent=()):
        """the land behind the cut: one plane per segment, shaded by its slope; accent spans tinted"""
        quads = []
        for a, b in zip(g, g[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            if abs(dx) < 1e-9 and abs(dy) < 1e-9:
                continue
            vis = dx * OY - dy * OX > 1e-9
            tone = T_FLAT if abs(dy) < 1e-6 else (T_DOWN if dy < 0 else T_UP)
            if abs(dy) < 1e-6 and any(xa - 1e-6 <= min(a[0], b[0]) and max(a[0], b[0]) <= xb + 1e-6
                                      for xa, xb in accent):
                tone = "F3E0C8"                           # our terraces: only their treads carry the tint
            quads.append((vis, [a, b, o(b, 1), o(a, 1)], tone))
            TONE[(a, b)] = tone
        for vis, q, tone in sorted(quads, key=lambda t: t[0]):
            poly(q, tone, tone, 0.05)
        line([o(p, 1) for p in g], X_LN, hair)            # the far edge of the block

    def water(xa, xb, yw, g):
        poly([(xa, yw), (xb, yw), o((xb, yw), 1), o((xa, yw), 1)], W_TOP)
        for d in (0.33, 0.66):                            # two hairlines = a flat plane, not a wave
            line([o((xa, yw), d), o((xb, yw), d)], W_EDGE, hair * 0.8)
        under = [p for p in g if xa <= p[0] <= xb and p[1] <= yw + 1e-6]
        poly([(xa, yw)] + under + [(xb, yw)], C["water"])
        for a, b in zip(g, g[1:]):                        # land above the water stays in front of the plane
            if min(a[1], b[1]) > yw + 1e-6 and (b[0] - a[0]) * OY - (b[1] - a[1]) * OX > 1e-9:
                tone = TONE.get((a, b), T_FLAT)
                poly([a, b, o(b, 1), o(a, 1)], tone, tone, 0.05)

    def cut(g, base, accent=()):
        """the cut face: poché down to the base, the right end face, the ONE heavy line"""
        poly([(g[0][0], base)] + list(g) + [(g[-1][0], base)], C["ground"])
        e = (g[-1][0], base)
        poly([e, g[-1], o(g[-1], 1), o(e, 1)], "CFC9BE")
        line(g, C["ink"], Wt["cut"])
        for xa, xb in accent:                             # our terraces in the cut: the line turns accent
            seg = [p for p in g if xa - 1e-6 <= p[0] <= xb + 1e-6]
            if len(seg) >= 2:
                line(seg, M_FR, Wt["cut"])

    def block(x0_, x1_, yb, h, d0, d1, kind="ctx", top_h=None):
        """an extruded block standing at depth d0..d1: front, top, right side"""
        fr, tp, sd, st, lw_ = {"ctx": (X_FR, X_TOP, X_SIDE, X_LN, 0.1),
                               "her": ("FBFAF7", "ECE8E1", "DCD6CC", C["her"], 0.16),
                               "move": ("F2DCC4", "F7E8D7", "EAD0B4", M_FR, 0.45),   # v11.2: tint + accent edge
                               "grey": ("E4E0D8", "D6D1C7", "C9C3B8", X_LN, 0.1),
                               "brick": ("EBD5CB", "E2C6B9", "D6B6A7", C["her"], 0.16)}[kind]
        a, b = o((x0_, yb), d0), o((x1_, yb), d0)
        a2, b2 = o((x0_, yb + h), d0), o((x1_, yb + h), d0)
        poly([b, o((x1_, yb), d1), o((x1_, yb + h), d1), b2], sd, st, lw_)
        poly([a2, b2, o((x1_, yb + h), d1), o((x0_, yb + h), d1)], tp, st, lw_)
        poly([a, b, b2, a2], fr, st, lw_)
        return a2, b2

    def shadow(x0_, x1_, y_, d0, d1, dx=2.0, on_water=False):
        poly([o((x0_ + dx, y_), d0), o((x1_ + dx, y_), d0), o((x1_ + dx, y_), d1), o((x0_ + dx, y_), d1)],
             "A9BDBC" if on_water else SHADOW)

    def slab(x0_, x1_, y_, g, d0, d1, stems=(), th=1.1, ys=None):
        shadow(x0_, x1_, gy(g, (x0_ + x1_) / 2.0) if ys is None else ys, d0, d1, on_water=ys is not None)
        for xs in stems:                                  # thin stems down to the land at the slab's middle depth
            dm = (d0 + d1) / 2.0
            line([o((xs, gy(g, xs)), dm), o((xs, y_), dm)], M_SIDE, Wt["move"])
        block(x0_, x1_, y_, th, d0, d1, "move")

    def canopy(x0_, x1_, y_, g, d0, d1, stems=(), ys=None, bay=4.0, fold=1.1):
        """v11.5 (Aras 09:52 UTC, the Sections canopy language): a folded skin of triangle facets (alternate light /
        shaded planes running into the depth), a louvre layer under it, Y-shaped columns under the valleys"""
        shadow(x0_, x1_, gy(g, (x0_ + x1_) / 2.0) if ys is None else ys, d0, d1, on_water=ys is not None)
        dm = (d0 + d1) / 2.0
        for xs in stems:                                  # Y columns: a stem, then two arms to the valleys
            yb_ = gy(g, xs)
            line([o((xs, yb_), dm), o((xs, y_ - 1.6), dm)], M_SIDE, Wt["move"])
            line([o((xs - 1.4, y_), dm), o((xs, y_ - 1.6), dm), o((xs + 1.4, y_), dm)], M_SIDE, Wt["move"])
        for k_ in range(3):                               # louvres: three hairlines under the skin
            yl_ = y_ - 0.25 - 0.22 * k_
            line([o((x0_, yl_), d0), o((x1_, yl_), d0)], M_SIDE, hair)
        n = max(2, int(round((x1_ - x0_) / bay)))
        w_ = (x1_ - x0_) / n
        for i in range(n):                                # facets: valley - ridge - valley, each run into the depth
            xa_, xm_, xb_ = x0_ + i * w_, x0_ + (i + 0.5) * w_, x0_ + (i + 1) * w_
            for (pa, pb), tone in ((((xa_, y_), (xm_, y_ + fold)), "F7E8D7"), (((xm_, y_ + fold), (xb_, y_)), "EAD0B4")):
                poly([o(pa, d0), o(pb, d0), o(pb, d1), o(pa, d1)], tone, M_FR, hair * 1.4)
        line([o((x0_ + i * w_ + (0.5 * w_ if j % 2 else 0.0), y_ + (fold if j % 2 else 0.0)), d0)
              for i in range(n) for j in range(2)] + [o((x1_, y_), d0)], M_FR, Wt["move"] * 2.0)

    def town(g, xa, xb, step, d0, d1, hmax, focus, roof=True):
        """v11.2 (review: "rows of identical sugar cubes"): the town as ONE continuous row of gabled houses of varied
        width and height (taller near our move), roofs run back in depth, a paler skyline band behind"""
        span = max(abs(xa - focus), abs(xb - focus), 1.0)
        rows, x_, i = [], xa, 0
        while x_ < xb - 0.5:
            w_ = min(xb - x_, step * (0.75 + 0.5 * ((i * 7 + int(xa)) % 5) / 4.0))
            f_ = 1.0 - 0.45 * abs(x_ + w_ / 2.0 - focus) / span
            h_ = hmax * f_ * (0.8 + 0.35 * ((i * 3 + int(xa)) % 4) / 3.0)
            rows.append((x_, w_, h_, max(gy(g, x_), gy(g, x_ + w_))))
            x_, i = x_ + w_, i + 1
        sky = []                                          # the far band: one pale skyline
        for x_, w_, h_, yb_ in rows:
            sky += [(x_, yb_ + h_ * 1.35), (x_ + w_, yb_ + h_ * 1.35)]
        poly([o(p_, d1) for p_ in sky + [(xb, gy(g, xb)), (xa, gy(g, xa))]], "ECE8E1")
        for x_, w_, h_, yb_ in rows:
            r_ = w_ * 0.32 if roof else 0.0
            if roof:                                      # the roof's back slope runs into the depth
                poly([o((x_ + w_ / 2.0, yb_ + h_ + r_), d0), o((x_ + w_, yb_ + h_), d0),
                      o((x_ + w_, yb_ + h_), d0 + 0.18), o((x_ + w_ / 2.0, yb_ + h_ + r_), d0 + 0.18)],
                     X_SIDE, X_LN, hair)
            fr = [(x_, yb_), (x_, yb_ + h_)] + ([(x_ + w_ / 2.0, yb_ + h_ + r_)] if roof else []) + \
                 [(x_ + w_, yb_ + h_), (x_ + w_, yb_)]
            poly([o(p_, d0) for p_ in fr], "FAF8F4", X_LN, hair)
            for k_ in range(max(1, int(w_ / 1.6))):        # one row of windows
                xw = x_ + (k_ + 0.5) * w_ / max(1, int(w_ / 1.6))
                q = o((xw, yb_ + h_ * 0.55), d0)
                poly([(q[0] - 0.22, q[1] - 0.35), (q[0] + 0.22, q[1] - 0.35), (q[0] + 0.22, q[1] + 0.35),
                      (q[0] - 0.22, q[1] + 0.35)], X_LN)

    def stop(x_, g, lab_=None):
        """a bus stop: a pole with its sign, standing on the land (no arrows from the air)"""
        p0 = (x_, gy(g, x_))
        line([p0, (x_, p0[1] + 4.2)], C["ink"], Wt["thin"])
        poly([(x_ - 0.9, p0[1] + 3.0), (x_ + 0.9, p0[1] + 3.0), (x_ + 0.9, p0[1] + 4.6), (x_ - 0.9, p0[1] + 4.6)],
             C["bus"], C["ink"], hair)

    def people(xs, y_, d):
        """v11.2 (review: "figures read as map pins"): small standing figures, legs, body, head"""
        for x_ in xs:
            p = o((x_, y_ if not callable(y_) else y_(x_)), d)
            line([(p[0] - 0.28, p[1]), (p[0], p[1] + 0.95), (p[0] + 0.28, p[1])], C["ink"], hair * 1.6)
            poly([(p[0] - 0.3, p[1] + 0.9), (p[0] + 0.3, p[1] + 0.9), (p[0] + 0.24, p[1] + 1.75),
                  (p[0] - 0.24, p[1] + 1.75)], C["ink"])
            poly([(p[0] + 0.27 * math.cos(math.radians(a_)), p[1] + 2.05 + 0.27 * math.sin(math.radians(a_)))
                  for a_ in range(0, 360, 40)], C["ink"])

    def level(y_, xa, xb, name, lx=None):
        line([(xa, y_), (xb, y_)], C["water_ln"], hair * 2, (1.4, 0.9))
        line([o((xb, y_), 0), o((xb, y_), 1)], C["water_ln"], hair * 2, (1.4, 0.9))
        K["text"](name, (xb - 0.5) if lx is None else lx, y_ + 0.6, 1.5, C["water_ln"], True, "R" if lx is None else "L")

    def arches_front(x0_, x1_, yb, h, d, n, kind="her"):
        """a bridge / arcade seen side-on at depth d: a block with n round openings through it"""
        block(x0_, x1_, yb, h, d, d + 0.18, kind)
        span = (x1_ - x0_) / n
        for i in range(n):
            cx = x0_ + span * (i + 0.5)
            r = span * 0.36
            pts = [(cx - r, yb)] + [(cx + r * math.cos(math.radians(a_)), yb + h * 0.42 + r * math.sin(math.radians(a_)))
                                    for a_ in range(180, -1, -15)] + [(cx + r, yb)]
            poly([o(p, d) for p in pts], W_TOP, C["her"], 0.16)

    BASE = 3.0
    if node == "N1":                                      # one stream, two neighbourhoods: a garden deck joins them
        g = [(0, 14.5), (64, 12.6)] + steps(64, 82, 12.6, 7.4, 4) + [(82, 5.6), (110, 5.6), (110, 7.4)] + \
            steps(110, 128, 7.4, 12.6, 4) + [(192, 14.5)]
        acc = ((64, 82), (110, 128))
        terrain(g, acc)
        water(82, 110, 7.4, g)
        town(g, 6, 58, 4.6, 0.42, 0.78, 3.0, 96)
        town(g, 134, 186, 4.6, 0.42, 0.78, 3.0, 96)
        slab(72, 120, 20.5, g, 0.28, 0.58, stems=(76, 116), th=0.9, ys=7.4)
        cut(g, BASE, acc)
        people([86, 94, 102], 21.4, 0.43)
        people([69, 123], lambda x_: gy(g, x_), 0.2)
        stop(3.0, g)
        lab(u"one garden across the stream", 96, 30.0, True, "C")
        br(0, 12, 2.0, u"VILLAGE BUSES")
        br(16, 62, 2.0, u"UPPER")
        br(130, 188, 2.0, u"LOWER")
    elif node == "N2":                                    # 1,800 years of one crossing: terraces step into the river
        g = [(0, 14.5), (62, 14.5)] + steps(62, 102, 14.5, 7.4, 6) + [(102, 5.6), (192, 5.6)]
        acc = ((62, 102),)
        terrain(g, acc)
        water(102, 192, 7.4, g)
        town(g, 2, 13, 3.6, 0.5, 0.8, 1.8, 80)
        a2, b2 = block(16, 36, 14.5, 4.4, 0.32, 0.8, "her")     # Ulu Cami: hall, three domes on the mihrab axis
        for xd in (20.5, 26.0, 31.5):
            c_ = o((xd, 18.9), 0.56)
            poly([(c_[0] + 2.0 * math.cos(math.radians(a_)), c_[1] + 2.0 * math.sin(math.radians(a_)))
                  for a_ in range(0, 181, 12)], "FBFAF7", C["her"], 0.16)
        block(38.4, 39.8, 14.5, 3.0, 0.56, 0.66, "her")         # minaret: stone base, round shaft, one balcony
        block(38.7, 39.5, 17.5, 8.5, 0.58, 0.64, "her")
        block(38.4, 39.8, 23.6, 0.5, 0.56, 0.66, "her")
        t_ = o((39.1, 26.0), 0.61)
        poly([(t_[0] - 0.4, t_[1]), (t_[0] + 0.4, t_[1]), (t_[0], t_[1] + 2.4)], "FBFAF7", C["her"], 0.16)
        block(46, 56, 14.5, 2.6, 0.4, 0.75, "her")              # Tabaklar Hamami
        c_ = o((51, 17.1), 0.57)
        poly([(c_[0] + 2.4 * math.cos(math.radians(a_)), c_[1] + 1.9 * math.sin(math.radians(a_)))
              for a_ in range(0, 181, 12)], "FBFAF7", C["her"], 0.16)
        arches_front(132, 166, 5.6, 7.6, 0.55, 3)               # the Roman bridge
        cut(g, BASE, acc)
        people([70, 80, 90], lambda x_: gy(g, x_), 0.35)
        level(9.6, 62 + 40 * 4 / 6.0, 192, u"WINTER")
        lab(u"terraces into the river", 84, 24.0, True, "C")
        br(14, 42, 2.0, u"ULU CAMI")
        br(45, 58, 2.0, u"HAMAM")
        br(130, 168, 2.0, u"ROMAN BRIDGE")
    elif node == "N3":                                    # the bazaar walks over its river: slots open the hidden stream
        g = [(0, 5.6), (14, 5.6), (14, 7.4), (18, 14.5), (174, 14.5), (178, 7.4), (178, 5.6), (192, 5.6)]
        terrain(g)
        water(0, 14, 7.4, g)
        water(178, 192, 7.4, g)
        town(g, 22, 170, 4.4, 0.62, 0.92, 2.6, 96)                # the arasta: one continuous row of shops
        slots = (54, 82, 110, 138)
        for xs in slots:                                          # the slots: voids in the plate, accent rims
            q = [o((xs - 2.4, 14.5), 0.18), o((xs + 2.4, 14.5), 0.18), o((xs + 2.4, 14.5), 0.5), o((xs - 2.4, 14.5), 0.5)]
            poly(q, "6F8E8D", M_FR, Wt["move"] * 1.6)
        cut(g, BASE)
        poly([(18, 6.0), (174, 6.0), (174, 9.6), (18, 9.6)], "8FA6A5")    # the stream under the town, in the cut
        poly([(18, 6.0), (174, 6.0), (174, 7.4), (18, 7.4)], C["water"])
        for xs in slots:
            poly([(xs - 1.2, 9.6), (xs + 1.2, 9.6), (xs + 1.2, 14.5), (xs - 1.2, 14.5)], "FFFFFF")
            line([(xs - 1.2, 9.6), (xs - 1.2, 14.5)], M_FR, Wt["move"] * 1.6)
            line([(xs + 1.2, 9.6), (xs + 1.2, 14.5)], M_FR, Wt["move"] * 1.6)
        people([60, 88, 116, 144], 14.5, 0.3)
        stop(188.0, [(178, 7.4), (192, 7.4)])
        lab(u"slots to the water below", 96, 29.0, True, "C")
        br(0, 16, 2.0, u"TABAK KÖPRÜSÜ")
        br(20, 172, 2.0, u"THE STREAM UNDER THE TOWN · 234 M")
        br(178, 192, 2.0, u"BUSES")
    elif node == "N4":                                    # the temple that stands on the river
        g = [(0, 14.5), (124, 14.5)] + steps(124, 138, 14.5, 7.4, 4) + [(138, 5.6), (192, 5.6)]
        acc = ((124, 138),)
        terrain(g, acc)
        water(138, 192, 7.4, g)
        town(g, 4, 60, 4.0, 0.45, 0.82, 2.4, 150)
        a2, b2 = block(78, 106, 14.5, 10.0, 0.3, 0.78, "brick")   # the Red Hall (brick): roofless, rows of arched windows
        for xw in (82.5, 88.0, 93.5, 99.0, 103.0):
            for yw0, hw in ((20.6, 2.2), (16.4, 2.2)):
                pts = [(xw - 0.8, yw0)] + [(xw + 0.8 * math.cos(math.radians(a_)), yw0 + hw + 0.8 *
                                            math.sin(math.radians(a_))) for a_ in range(180, -1, -30)] + [(xw + 0.8, yw0)]
                line([o(p, 0.3) for p in pts] + [o(pts[0], 0.3)], C["her"], hair * 1.6)
        canopy(142, 166, 22.0, g, 0.24, 0.56, stems=(145, 154, 163), ys=7.4)   # v11.5: the designed canopy
        arches_front(172, 190, 5.6, 6.6, 0.5, 3)                 # Üç Kemer
        cut(g, BASE, acc)
        for xa_ in (70, 96):                                     # the twin tunnels in the cut, the stream inside
            arch = [(xa_, 5.0)] + [(xa_ + 11 - 11 * math.cos(math.radians(a_)), 5.0 + 6.0 * math.sin(math.radians(a_)))
                                   for a_ in range(0, 181, 12)] + [(xa_ + 22, 5.0)]
            poly(arch, "8FA6A5", C["ink"], Wt["thin"])
            poly([(xa_ + 0.6, 5.0), (xa_ + 21.4, 5.0), (xa_ + 21.0, 7.4), (xa_ + 1.0, 7.4)], C["water"])
        block(143, 165, 12.0, 0.6, 0.28, 0.52, "move")           # the timber deck above Q500, under the roof
        # v11.6 (Aras 10:02 elevation, Sections v1.28.2): every other bay a closed glazed room up to the louvres (the
        # deck at 12.0 is above Q500 11.0 + 0.6), timber planters in the open bay
        gx0, gx1, gy0, gy1 = 145.6, 153.4, 12.6, 21.0
        poly([o((gx0, gy0), 0.36), o((gx1, gy0), 0.36), o((gx1, gy1), 0.36), o((gx0, gy1), 0.36)], "DDE8E9", M_FR, hair * 1.4)
        poly([o((gx1, gy0), 0.36), o((gx1, gy0), 0.48), o((gx1, gy1), 0.48), o((gx1, gy1), 0.36)], "C9D9DB", M_FR, hair * 1.4)
        for xm in (gx0 + (gx1 - gx0) * f for f in (0.25, 0.5, 0.75)):
            line([o((xm, gy0), 0.36), o((xm, gy1), 0.36)], M_FR, hair)
        for xp in (156.0, 160.0):
            block(xp, xp + 2.2, 12.6, 0.9, 0.34, 0.46, "move")
        people([155.0, 159.1, 163.4], 12.6, 0.3)
        people([127, 134], lambda x_: gy(g, x_), 0.2)
        level(11.0, 131.0, 192, u"Q500", lx=139.0)
        lab(u"raised gathering", 154, 31.5, True, "C")
        br(80, 104, 2.0, u"RED HALL")
        br(118, 138, 2.0, u"TUNNEL MOUTH")
        br(172, 190, 2.0, u"ÜÇ KEMER")
    elif node == "N5":                                    # the bank as the front yard
        g = [(0, 14.5), (134, 14.5)] + steps(134, 150, 14.5, 7.4, 4) + [(150, 5.6), (192, 5.6)]
        acc = ((134, 150),)
        terrain(g, acc)
        water(150, 192, 7.4, g)
        town(g, 10, 114, 7.0, 0.36, 0.82, 3.2, 124)
        shadow(124, 134, 14.5, 0.25, 0.7)
        block(124, 134, 14.5, 4.2, 0.25, 0.7, "move")                                  # the pavilion on the dry top
        cut(g, BASE, acc)
        people([138, 142, 146], lambda x_: gy(g, x_), 0.25)
        stop(3.0, g)
        lab(u"front yard to the water", 129, 27.5, True, "C")
        br(0, 6, 2.0, u"BUSES")
        br(10, 116, 2.0, u"HOUSES TURN THEIR BACKS TO THE STREAM")
        br(124, 152, 2.0, u"THE BANK")
    elif node == "N6":                                    # the door to the town
        g = [(0, 14.5), (106, 14.5), (116, 7.4), (118, 5.6), (150, 5.6), (152, 7.4), (160, 14.5), (192, 14.5)]
        terrain(g)
        water(116, 152, 7.4, g)
        for i in range(4):                                       # the sheds: one low saw-tooth band
            xa_ = 6 + i * 17.0
            block(xa_, xa_ + 15, 14.5, 2.0, 0.45, 0.9, "grey")
            r1, r2 = o((xa_, 16.5), 0.45), o((xa_ + 7.5, 16.5), 0.45)
            poly([r1, (r1[0], r1[1] + 1.6), r2], "D6D1C7", X_LN, 0.1)
            r1, r2 = o((xa_ + 7.5, 16.5), 0.45), o((xa_ + 15, 16.5), 0.45)
            poly([r1, (r1[0], r1[1] + 1.6), r2], "D6D1C7", X_LN, 0.1)
        block(106, 160, 14.5, 1.0, 0.25, 0.75, "ctx")            # the road bridge over the stream
        for xp in (126, 140):
            block(xp - 0.5, xp + 0.5, 5.6, 8.9, 0.42, 0.58, "grey")
        slab(78, 102, 20.0, g, 0.26, 0.56, stems=(82, 98), th=0.9)
        cut(g, BASE)
        people([84, 90, 96], 20.9, 0.41)
        stop(186.0, g)
        stop(190.0, g)
        lab(u"lifted, facing the arrival", 90, 29.0, True, "C")
        br(4, 74, 2.0, u"SHEDS")
        br(106, 160, 2.0, u"ROAD BRIDGE")
        br(166, 192, 2.0, u"REGIONAL BUSES")


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
            dx = max(0.0, bx[0] + 1.5 - x) - max(0.0, x + w - (bx[2] - 1.5))   # v11.2: 1.5 mm off the frame line
            dy = max(0.0, bx[1] + 1.5 - y) - max(0.0, y + it[4] - (bx[3] - 1.5))
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


# ================================================================ v11: the plan IS a crop of his master.svg
# Aras 15 Nov 06:19-06:24 UTC: "this is the latest masterplan ... use this masterplan for node slides", "nodes can take
# their zoom-ins directly from the svg", "no need to draw it really". Each node plan is his drawing itself, cut to the
# node frame and turned like the plan: the browser on his PC (Edge or Chrome, headless) renders master.svg wrapped in one
# matrix that maps it straight onto the plan box, at 300 dpi. Cached per node (svg size + time, frame, size).
CROP_SVG = os.path.join("Data", "assets", "plan", "master.svg")
CROP_DIR = os.path.join("cached", "bergama_node_crops")
CROP_DPI = 300.0
CROP_HIDE_EXISTING = u""   # v12.6: his drawing whole, the base of the node plans (Aras 14:45); v12.4 hid #ev-yol,#builts2 (MapBase gave them)
BROWSERS = (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe") + tuple(sorted(
    glob.glob(r"C:\Program Files (x86)\Microsoft\EdgeCore\*\msedge.exe"), reverse=True))   # v11.1: Windows IoT LTSC has only EdgeCore


def svg_crop(node, Wm, pgS, box, log, css=u"", bg=True):
    """PNG of master.svg mapped onto the page box (x0, y0, x1, y1 mm) by pgS (survey m -> page mm); Wm = the
    MasterplanBase matrix (svg units -> survey m); css = extra <defs>/<style> put before his drawing (v11.4, slide 4
    colours his layers by sub-system; empty for the node plans); bg=False = transparent paper (v12.2: MapBase shows under
    it). Returns the PNG path or None (FLAG logged)."""
    import subprocess
    src = os.path.join(ROOT, CROP_SVG)
    if not os.path.exists(src):
        log.append(u"FLAG node plan crop: %s is missing (copy master.svg there)" % src)
        return None
    x0, y0, x1, y1 = box
    PW, PH = int(round((x1 - x0) / 25.4 * CROP_DPI)), int(round((y1 - y0) / 25.4 * CROP_DPI))
    a, b, c, d, e, f = Wm

    def px(sx, sy):                                       # svg unit -> survey -> page mm -> pixel (y down)
        q = pgS((a * sx + c * sy + e, b * sx + d * sy + f))
        return ((q[0] - x0) / (x1 - x0) * PW, (y1 - q[1]) / (y1 - y0) * PH)
    o_, ex_, ey_ = px(0.0, 0.0), px(1000.0, 0.0), px(0.0, 1000.0)
    M = ((ex_[0] - o_[0]) / 1000.0, (ex_[1] - o_[1]) / 1000.0, (ey_[0] - o_[0]) / 1000.0, (ey_[1] - o_[1]) / 1000.0,
         o_[0], o_[1])
    st = os.stat(src)
    stamp = u"%d/%d/%s/%dx%d" % (st.st_size, int(st.st_mtime), u",".join(u"%.4f" % v for v in M), PW, PH)
    if css:
        import hashlib
        stamp += u"/css" + hashlib.md5(css.encode("utf-8")).hexdigest()[:12]
    if not bg:
        stamp += u"/t"
    out_dir = os.path.join(ROOT, CROP_DIR)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    png, js = os.path.join(out_dir, node + u".png"), os.path.join(out_dir, node + u".json")
    try:
        if os.path.exists(png) and json.load(open(js, encoding="utf-8")).get("stamp") == stamp:
            log.append(u"plan = master.svg crop (cached): %s, %d x %d px" % (png, PW, PH))
            return png
    except Exception:
        pass
    br = next((p_ for p_ in BROWSERS if os.path.exists(p_)), None)
    if br is None:
        log.append(u"FLAG node plan crop: no Edge / Chrome found (%s)" % u"; ".join(BROWSERS))
        return None
    t0 = time.time()
    with open(src, encoding="utf-8") as f_:
        txt = f_.read()
    i0 = txt.index("<svg")
    i1 = txt.index(">", i0) + 1
    j1 = txt.rindex("</svg>")
    head = (u'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%dpx" '
            u'height="%dpx" viewBox="0 0 %d %d">%s'
            u'%s<g transform="matrix(%.9f %.9f %.9f %.9f %.6f %.6f)">' % ((PW, PH, PW, PH, (u'<rect width="%d" height="%d" '
                                                                         u'fill="#ffffff"/>' % (PW, PH)) if bg else u"",
                                                                        css or u"") + M))
    wrap = os.path.join(out_dir, node + u"_wrap.svg")
    with open(wrap, "w", encoding="utf-8") as f_:
        f_.write(txt[:i0])
        f_.write(head)
        f_.write(txt[i1:j1])
        f_.write(u"</g></svg>")
    del txt
    if os.path.exists(png):
        os.remove(png)
    cmd = [br, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
           "--default-background-color=" + ("FFFFFFFF" if bg else "00000000"), "--virtual-time-budget=120000", "--window-size=%d,%d" % (PW, PH),
           "--screenshot=%s" % png, "file:///" + wrap.replace("\\", "/")]
    try:
        subprocess.run(cmd, timeout=280, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as ex_:
        log.append(u"FLAG node plan crop: the browser failed (%s: %s)" % (type(ex_).__name__, ex_))
    try:
        os.remove(wrap)
    except Exception:
        pass
    if not os.path.exists(png) or os.path.getsize(png) < 1000:
        log.append(u"FLAG node plan crop: no picture came out of %s" % br)
        return None
    if not bg:                                            # v12.4: the browser must have left the sheet see-through
        try:
            import clr
            clr.AddReference("System.Drawing")
            from System.Drawing import Bitmap
            bm_ = Bitmap(png)
            n_t = sum(1 for i in range(20) for j in range(20)
                      if bm_.GetPixel(int((i + 0.5) * bm_.Width / 20.0), int((j + 0.5) * bm_.Height / 20.0)).A < 128)
            bm_.Dispose()
        except Exception as ex_:
            n_t = -1
            log.append(u"crop: see-through check skipped (%s)" % ex_)
        if n_t == 0:
            log.append(u"FLAG crop: %s gave an opaque picture (no see-through pixels); MapBase + his drawing as "
                       u"vectors instead" % os.path.basename(br))
            return None
    with open(js, "w", encoding="utf-8") as f_:
        json.dump({"stamp": stamp, "svg": CROP_SVG, "px": [PW, PH], "matrix_px": list(M)}, f_)
    log.append(u"plan = master.svg crop: %s, %d x %d px, %.1f s (%s)" % (png, PW, PH, time.time() - t0,
                                                                     os.path.basename(br)))
    return png


def crop_sampler(png, box, log):
    """v11.2: colour of his drawing under a set of page points (the legend keys what the crop shows). Returns
    f(points_mm, area) -> hex or None; None when the picture can't be read (old colours kept, FLAG logged)"""
    try:
        import clr
        clr.AddReference("System.Drawing")
        from System.Drawing import Bitmap
        bm = Bitmap(png)
    except Exception as ex_:
        log.append(u"FLAG legend colours: the crop could not be read (%s); drawing colours used" % ex_)
        return None
    x0, y0, x1, y1 = box
    PW, PH = bm.Width, bm.Height
    tp = lambda q: ((q[0] - x0) / (x1 - x0) * PW, (y1 - q[1]) / (y1 - y0) * PH)

    def inside(x, y, P):
        c_ = False
        j = len(P) - 1
        for i in range(len(P)):
            if (P[i][1] > y) != (P[j][1] > y) and x < (P[j][0] - P[i][0]) * (y - P[i][1]) / (P[j][1] - P[i][1]) + P[i][0]:
                c_ = not c_
            j = i
        return c_

    def px(x, y, line):
        best = None
        for dx in ((-1, 0, 1) if line else (0,)):
            for dy in ((-1, 0, 1) if line else (0,)):
                xi, yi = int(x) + dx, int(y) + dy
                if 0 <= xi < PW and 0 <= yi < PH:
                    c = bm.GetPixel(xi, yi)
                    if c.A < 128:                         # v12.4: see-through (MapBase under it), not his colour
                        continue
                    v = (c.R, c.G, c.B)
                    if best is None or sum(v) < sum(best):
                        best = v
        return best

    def f(polys, area):
        got = []
        for P in polys:
            Q = [tp(q) for q in P]
            if area and len(Q) >= 3:
                xa, xb = max(0, min(q[0] for q in Q)), min(PW - 1, max(q[0] for q in Q))
                ya, yb = max(0, min(q[1] for q in Q)), min(PH - 1, max(q[1] for q in Q))
                if xb <= xa or yb <= ya:
                    continue
                for i in range(7):
                    for j in range(7):
                        x, y = xa + (xb - xa) * (i + 0.5) / 7.0, ya + (yb - ya) * (j + 0.5) / 7.0
                        if inside(x, y, Q):
                            got.append(px(x, y, False))
            else:
                for a_, b_ in zip(Q, Q[1:]):
                    n = max(1, int(math.hypot(b_[0] - a_[0], b_[1] - a_[1]) / 6.0))
                    for t in range(n):
                        v = px(a_[0] + (b_[0] - a_[0]) * t / float(n), a_[1] + (b_[1] - a_[1]) * t / float(n), True)
                        if v is not None and min(v) < 235:
                            got.append(v)
            if len(got) > 400:
                break
        got = [g for g in got if g is not None]
        if len(got) < 5:
            return None
        bins = {}
        for g in got:
            bins.setdefault(tuple(c // 24 for c in g), []).append(g)
        top = max(bins.values(), key=len)
        return u"%02X%02X%02X" % tuple(int(sum(g[i] for g in top) / len(top)) for i in range(3))
    f.close = bm.Dispose                                  # frees the PNG file (re-rendered next run)
    return f


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
    """the plan's context from MapBase (its default look, no grain: this writer has none; water flat) and, for the
    land-use count, the buildings, river and streets in frame m"""
    items = []
    st_ = dict(MB["mb_a05_style"]()) if "mb_a05_style" in MB else {}   # v11.3: the A05 base map look (Aras 07:59)
    st_["grain"] = False
    cnt = MB["mb_draw"](C, items, T, k, lim, None, style=st_)
    riv = [R for R in (B["clip_ring"]([T(p) for p in R_], lim) for R_ in C["polys"].get("river", [])) if len(R) >= 3]
    # v12.5: no hatch on the river, flat water fill from mb_draw (Aras 14:38 UTC "dont do hatches to river")
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
    mb_in = False
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
        # v10 (Aras 15 Nov 06:12 UTC "in the nodes it is so appearant how missing our basemap is"): the shared base
        # map (MapBase: joined streets, houses with shadows) is always under; his drawing adds everything but his own
        # copy of the existing roads and buildings (ev-yol, builts2), which were fragments
        pgS0 = lambda xy: (X0 + F.local(xy)[0] * k, Y0 + F.local(xy)[1] * k)
        crop_png = svg_crop(node, MPC["matrix"], lambda xy: (X0 + F.local(xy)[0] * k, Y0 + F.local(xy)[1] * k),
                            (X0, Y0, X0 + F.w * k, Y0 + F.h * k), log, css=CROP_HIDE_EXISTING, bg=False)
        if crop_png:                                      # v11: his drawing itself; nothing redrawn
            items += its_                                 # v12.4: MapBase under it (Aras 13:41-13:42)
            items.append(("image", X0, Y0, F.w * k, F.h * k, crop_png, None, False, None, "masterplan_svg"))
        else:
            items += its_
        mb_in = True
        mp_cnt = MPn["mp_draw"](MPC, items if not crop_png else [], lambda xy: (X0 + F.local(xy)[0] * k, Y0 + F.local(xy)[1] * k), k,
                                (X0, Y0, X0 + F.w * k, Y0 + F.h * k), None,
                                layers=set(kk.split("/")[0] for kk in MPC["layers"]) - set(MP_EXISTING),
                                style={"fill": {"su_outline": P["WATER_C"]}})   # v8.2: his river (a picture) as water
        seen = set()
        samp = crop_sampler(crop_png, (X0, Y0, X0 + F.w * k, Y0 + F.h * k), log) if crop_png else None
        n_samp = 0
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
            if samp is not None:                          # v11.2: the colour the crop shows for this layer
                isa = kind == "a" or bool(fill) or nm[1] == u"the Selinos"
                PL = [[pgS0(p_) for p_ in e_[4]] for kk2 in mp_cnt if kk2 == kk or MP_WORDS.get(kk2.split("/")[-1], (0, 0))[1] == nm[1]
                      for e_ in MPC["layers"][kk2] if e_[0] != "s" and len(e_[4]) >= 2]
                sc = samp(PL, isa)
                if sc:
                    col, n_samp = sc, n_samp + 1
            # v9.2 (review: "legend doesn't match the plan"): an outline-only piece is keyed as its outline
            (ex_rows if nm[0] else mp_rows).append(("box" if (kind == "a" or fill or nm[1] == u"the Selinos") else
                                                    "line", col, nm[1]))
        if samp is not None:
            samp.close()
            log.append(u"legend: %d key colours read from the crop" % n_samp)
        log.append(u"plan = his masterplan: %s" % (u", ".join(u"%s %d" % kv for kv in sorted(mp_cnt.items())) or
                                                  u"nothing in this frame"))
        if not crop_png:
            ex_rows[:0] = [r_ for r_ in MB["mb_legend"](MC, mb_cnt) if r_[0] in ("box", "line")][:4]
    except Exception as ex_:
        if not mb_in:
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
        # v9.9 (run 12: N4-A was moved onto the Red Hall but the crop round the stream cut the hall off, and the cut
        # mark landed on the Kizil Avlu stop): a heritage stop within 15 m of the line stays in view, 30 m spare
        hx = []
        for h_ in D.get("heritage", []):
            px_, py_ = h_["xy"][0] - C.A[0], h_["xy"][1] - C.A[1]
            dx_, dy_ = (C.B[0] - C.A[0]) / C.L, (C.B[1] - C.A[1]) / C.L
            s_ = px_ * dx_ + py_ * dy_
            if abs(px_ * dy_ - py_ * dx_) <= 15.0 and C.window[0] <= s_ <= C.window[1]:
                hx.append((s_ - C.window[0]) * 1000.0 / den_s)
                log.append(u"%s keeps heritage stop %s %s in view" % (C.name, h_["n"], h_.get("name", u"")))
        if hx:
            m_ = 30.0 * 1000.0 / den_s
            lo_ = max(bb[0], min(hx + [min(wx) if wx else cx]) - m_)
            hi_ = min(bb[2], max(hx + [max(wx) if wx else cx]) + m_)
            f = min(f, Wr / max(hi_ - lo_, 1.0))
            cx = (lo_ + hi_) / 2.0
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
            items.append(G["pc_text_c"](h["n"], q[0], q[1], 2.8, "FFFFFF", "heritage_loop"))   # v12.8: centred mark
            items.append(T_(h["name"], q[0] + K["heritage_r"] + 1.0, q[1] + 1.2, 2.4, RED, True, "L", "heritage_loop"))
    for code, xy in D["hubs"].items():
        q = pgS(xy)
        if inside(q):
            hc = "T" if code in ("IST", "RED") else code
            col = K["hub"][D["hub_kind"][hc]]
            items.append(R_([box(q[0] - 2.3, q[1] - 2.3, q[0] + 2.3, q[1] + 2.3)], col, "FFFFFF", 0.3, "hubs"))
            items.append(G["pc_text_c"](hc, q[0], q[1], 2.4, "FFFFFF", "hubs"))   # v12.8: centred mark

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
        items.append(G["pc_text_c"](u"V1", qa[0], qa[1], 2.2, "FFFFFF", "viewpoints"))   # v12.8: centred mark
        log.append(u"V1 viewpoint (assumed): %s, looking to the bed of %s" % (
            u"the city square" if sq else u"the bank end of %s" % Cn.name, Cn.name))
    # v6.5 (run 5: stop and loop labels read poorly over buildings and the spine): a light backing behind plan labels; v12.3: a letter-shaped halo, no box
    lab = []
    for it in items:
        if id(it) not in sec_ids and it[0] == "text" and it[8] in LBL_LAYERS and it[5] != "FFFFFF":
            lab += [h_[:8] + (it[8],) + it[9:] for h_ in G["pc_halo"](it[1], it[2], it[3], it[4], it[6], it[7], it[8])]   # v12.3
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
    lay_ = set(it[{"poly": 6, "line": 5, "text": 8}.get(it[0], 0)] for it in items if it[0] in ("poly", "line", "text"))
    rows2 = [("hdr", None, u"EXISTING: MOVEMENT AND HERITAGE")] + [r_ for r_, l_ in (   # v11.2: only what is drawn
             (("line", P["mixh"](K["lines"]["town"][0], P["PAPER"], 0.55), u"bus line"), "bus_lines"),
             (("disc", RED, u"heritage loop stop"), "heritage_loop"),
             (("box", K["hub"]["walk"], u"transit hub"), "hubs")) if l_ in lay_] + [
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
        CH = 192.0 * 36.0 / 205.0                         # v11.2: the kit's own aspect, no air band (review)
        if not concept_cut(node, items, 214.0, yw - 2.5 - CH, 192.0, CH, G, cuts[0], D, locals().get("MPC"), log,
                           MC=locals().get("MC")):
            concept(node, items, 214.0, yw - 2.5 - CH, 192.0, CH, G)
        yy = yw - CH - 7.5
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
        items.append(R_([box((x0 + x1) / 2.0 - hw, max(y0 + 0.4, (y0 + y1) / 2.0 - 5.0), (x0 + x1) / 2.0 + hw,
                             min(y1 - 0.4, (y0 + y1) / 2.0 + 6.5))], "F1EFEA", None, 0.0, layer))   # v11.2: inside
        items.append(T_(title, (x0 + x1) / 2.0, (y0 + y1) / 2.0 + 2.0, 2.8, INK, True, "C", layer))
        yy_ = (y0 + y1) / 2.0 - 2.0
        for ln in wrap(B, sub, 2.0, min(58.0, x1 - x0 - 4.0)):
            items.append(T_(ln, (x0 + x1) / 2.0, yy_, 2.0, GREY, False, "C", layer))
            yy_ -= 2.6
    # v9.2 (review: "a 66 x 38 mm empty area under the story"): the program brief fills the story column under the
    # text, the perspective and the building proposal share the right half
    # v9.6 (run 9: 60-90 mm empty under the land-use bar on N1, N3, N4): the program brief goes there when it fits;
    # the building proposal then takes the story column and the perspective the whole right half
    # v11.2 (review: V1 box 11 mm next to 16 mm ones, N3 without a building proposal, 29 mm empty under the land-use
    # bar on N1): the perspective always takes the whole right half under the story; the program brief goes under the
    # land-use bar when 16 mm fit, else it shares the story column with the building proposal
    ys_ = (y_story if st else 54.0)
    yp = (yy if st else 54.0) - 1.0
    yl = bar_y - 5.2 - 2.6 - 4.0
    PB = (u"PROGRAM BRIEF", None, "program")             # v12.7: filled from PROGRAM (no box, no fill)
    holder_ = holder

    def holder(x0, y0, x1, y1, title, sub, layer):         # v12.7: the program brief as text, smaller if it must
        if sub is not None:
            return holder_(x0, y0, x1, y1, title, sub, layer)
        pg = PROGRAM.get(node)
        if not pg:
            log.append(u"FLAG no program brief for %s" % node)
            return
        for sz in (2.2, 2.0, 1.8, 1.6):
            st_ = sz * 1.35
            rows = [wrap(B, p_, sz, x1 - x0) for p_ in pg]
            need = 3.6 + sum(len(r_) for r_ in rows) * st_ + 1.0 * (len(rows) - 1)
            if need <= y1 - y0:
                break
        else:
            log.append(u"FLAG program brief of %s needs %.0f mm, has %.0f" % (node, need, y1 - y0))
        items.append(T_(title, x0, y1 - 2.8, 2.6, INK, True, "L", layer))
        yy_ = y1 - 2.8 - 3.6
        for r_ in rows:
            for ln in r_:
                items.append(T_(ln, x0, yy_, sz, INK, False, "L", layer))
                yy_ -= st_
            yy_ -= 1.0
        log.append(u"program brief %s at %.1f mm text (NODE_IDEAS.md 15 Nov; areas proposed, totals summed)" % (node, sz))
    BP = (u"BUILDING PROPOSAL", u"placeholder: plan, section, elevation (if the node has one)", "placeholder_building")
    holder(310.0, 12.0, 406.0, ys_, u"V1 · PERSPECTIVE · %s" % node,
           u"placeholder: Aras's render (Archicad, Unreal 5) from V1 on the plan", "placeholder_perspective")
    left = [BP]
    if yl - 12.0 >= 16.0:
        holder(14.0, 12.0, 200.0, yl, *PB)
    else:
        left = [PB, BP]
    hl = yp - 12.0
    if hl >= 12.0 * len(left) + 3.0 * (len(left) - 1):
        hb = (hl - 3.0 * (len(left) - 1)) / len(left)
        for i_, h_ in enumerate(left):
            holder(214.0, yp - (i_ + 1) * hb - 3.0 * i_, 304.0, yp - i_ * hb - 3.0 * i_, *h_)
    elif hl >= 12.0 and len(left) == 2:
        holder(214.0, 12.0, 257.0, yp, *PB)
        holder(261.0, 12.0, 304.0, yp, *BP)
    else:
        log.append(u"FLAG no room for %s under the story of %s" % (u" and ".join(h_[0] for h_ in left), node))
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
