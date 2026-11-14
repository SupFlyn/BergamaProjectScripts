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

NC_VERSION = "v8.1"   # v8.1: masterplan sheet / texture frames (> 0.1 km2) left out, legend columns balanced, intro without the old levels text; v8: plan = his masterplan drawing; why-here story + one concept diagram per node; water bars and meets line gone; v7.5: v7.5: section_lines v2 (B along the bank: looks at the stream, no water bars); v7.4: v7.4: cut marks = two end arrows, no line between (pages_common v3.14); v7.3: v7.3: scale + north ignore the node frame line; v7.2: v7.2: the proposal from his masterplan SVG (MasterplanBase cache); v7.1: v7.1: R01 cut arrows (pc_cut_mark), no city-square ring, land-use columns >= 45 mm; v7: v7: every drawing fills its room on the A3 sheet, no 1:x printed (scale bars kept); v6.7: v6.7: no sources on the page (log only); v6.6: v6.6: scale + north to the emptiest plan corner; V1 also clear of link lines; v6.5: v6.5: V1 placed clear of labels; light backing behind plan labels; v6.4: v6.4: no repeats (R4 R5 R10): only the city-square stop, loop stops in the frame, no plant callouts; v6.3: v6.3: level marker stack (layer "levels") left out of the cuts; v6.2: v6.2: own section header (cached title block dropped), scales to 1:3000, land-use columns fit; v6.1: v6.1: cut items from cuts/<name>.json (Sections v1.6.5); v6: sections read from the Sections cache (cuts.json); v5   # v5: the plan context is the shared MapBase (mb_draw), Aras 12:17-12:18 UTC   # v4: brief plan rules (existing vs proposal, V1 viewpoint, program + building placeholders)   # v2: also output/presentation/<slide>.pdf (Aras 14 Nov 11:22 UTC)
ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
PAGE_W, PAGE_H = 420.0, 297.0
NODE_MARGIN_M = 25.0                       # m of town round the node frame on the plan
MP_MAX_M2 = 100000.0                 # m2: a bigger masterplan piece is a sheet / texture frame (v8.1)
PLAN_BOX = (14.0, 100.0, 200.0, 264.0)     # mm: x0, y0, x1, y1 of the plan's room
SEC_ROOMS = ((214.0, 186.0, 406.0, 266.0), (214.0, 100.0, 406.0, 180.0))   # mm: N#-A, N#-B
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


def concept(node, items, x0, y0, W, H):
    """v8: the node's one abstract concept diagram, a long thin section sketch in a W x H mm box at (x0, y0): ink
    lines, one grey, the water, and our move (SQUARE_C) the only solid accent. Shapes are diagrams, not to scale."""
    import random
    rnd = random.Random(sum(ord(c) for c in node))
    P_ = lambda pts: [(x0 + a * W / 192.0, y0 + b * H / 30.0) for a, b in pts]

    def ln(pts, col=DG_INK, lw=0.35, dash=None):
        items.append(L_(P_(pts), col, lw, "concept", dash))

    def pg(pts, fill, stroke=None, lw=0.0):
        items.append(R_([P_(pts)], fill, stroke, lw, "concept"))

    def dots(xa, xb, yfun, n, r=0.45, col=DG_INK):
        for _ in range(n):
            x = rnd.uniform(xa, xb)
            y = yfun(x) + rnd.uniform(0.6, 3.2)
            q = P_([(x, y)])[0]
            items.append(R_([ring(q[0], q[1], r * rnd.uniform(0.7, 1.2), 10)], col, None, 0.0, "concept"))

    def txt(t, x, y, size=1.8, col=GREY, bold=False, al="L"):
        q = P_([(x, y)])[0]
        items.append(T_(t, q[0], q[1], size, col, bold, al, "concept"))

    def arrow(a, b, col=DG_INK, lw=0.35):
        ln([a, b], col, lw)
        L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        pg([b, (b[0] - ux * 2.2 - uy * 0.9, b[1] - uy * 2.2 + ux * 0.9),
            (b[0] - ux * 2.2 + uy * 0.9, b[1] - uy * 2.2 - ux * 0.9)], col)

    def water(xa, xb, yb, yt):
        pg([(xa, yb), (xb, yb), (xb, yt), (xa, yt)], DG_WATER)

    def steps(xa, xb, ya, yb, n, col=SQUARE_C):
        pts = [(xa, ya)]
        for i in range(n):
            x1 = xa + (xb - xa) * (i + 1) / float(n)
            y1 = ya + (yb - ya) * (i + 1) / float(n)
            pts += [(pts[-1][0], y1), (x1, y1)]
        ln(pts, col, 0.6)

    if node == "N1":
        g = lambda x: 22.0 - 14.0 * x / 80.0 if x < 80 else (8.0 if x < 112 else 8.0 + 14.0 * (x - 112) / 80.0)
        ln([(0, 22), (80, 8), (86, 3), (106, 3), (112, 8), (192, 22)], DG_INK, 0.45)
        water(86, 106, 3, 5.5)
        dots(2, 70, g, 38)
        dots(122, 190, g, 38)
        pg([(78, 8.5), (114, 8.5), (114, 9.6), (78, 9.6)], SQUARE_C)
        steps(70, 86, 10, 4, 4)
        steps(122, 106, 10, 4, 4)
        txt(u"UPPER", 18, 26, 2.0, DG_INK, True)
        txt(u"LOWER", 160, 26, 2.0, DG_INK, True)
        arrow((-2, 27), (24, 27))
        txt(u"village buses", 0, 28.6)
        txt(u"one garden across the stream", 96, 11.5, 1.9, SQUARE_C, True, "C")
    elif node == "N2":
        ln([(0, 12), (70, 12), (110, 3), (192, 3)], DG_INK, 0.45)
        water(70, 192, 3, 6.5)
        ln([(70, 8.5), (192, 8.5)], "3F86B8", 0.3, (1.5, 1.0))
        txt(u"winter", 188, 9.3, 1.6, "3F86B8", False, "R")
        steps(62, 110, 12, 3.5, 6)
        dots(64, 96, lambda x: 12.0 - 8.5 * (x - 62) / 48.0, 14, 0.4, SQUARE_C)
        pts = [(132, 3)]
        for a in range(0, 181, 15):
            pts.append((147 - 15 * math.cos(math.radians(a)), 3 + 11 * math.sin(math.radians(a))))
        ln(pts + [(162, 3)], DG_INK, 0.45)
        ln([(128, 14), (166, 14)], DG_INK, 0.6)
        pg([(14, 12), (30, 12), (30, 18), (14, 18)], DG_GREY, DG_INK, 0.3)
        ln([(32, 12), (32, 26)], DG_INK, 0.35)
        txt(u"Ulu Cami 1398-99", 14, 20, 1.8, DG_INK)
        pts = [(42, 12)] + [(49 - 7 * math.cos(math.radians(a)), 15 + 4 * math.sin(math.radians(a)))
                            for a in range(0, 181, 20)] + [(56, 12)]
        ln(pts, DG_INK, 0.35)
        txt(u"hamam", 49, 20.5, 1.8, DG_INK, False, "C")
        txt(u"Roman bridge, 2nd-3rd c.", 147, 16, 1.8, DG_INK, False, "C")
        txt(u"terraces into the river", 86, 14.5, 1.9, SQUARE_C, True, "C")
        arrow((40, 13.5), (64, 13.5), SQUARE_C, 0.45)
        txt(u"ramp + seating", 40, 15.2, 1.7, SQUARE_C)
    elif node == "N3":
        pg([(0, 10), (192, 10), (192, 12), (0, 12)], DG_GREY, DG_INK, 0.3)
        water(0, 18, 3, 6)
        water(174, 192, 3, 6)
        ln([(18, 5), (174, 5)], DG_INK, 0.35, (1.2, 0.9))
        dots(4, 188, lambda x: 12.0, 90, 0.42)
        for x in (48, 78, 108, 138):
            pg([(x - 0.7, 5.5), (x + 0.7, 5.5), (x + 0.7, 12.5), (x - 0.7, 12.5)], SQUARE_C)
        arrow((96, 28), (96, 17))
        txt(u"buses arrive", 98, 25)
        txt(u"Tabak Köprüsü", 2, 1.2, 1.8, DG_INK)
        txt(u"the stream under the town, 234 m", 96, 1.2, 1.8, DG_INK, False, "C")
        txt(u"slots show the water below", 93, 14.0, 1.9, SQUARE_C, True, "C")
    elif node == "N4":
        ln([(0, 10), (60, 10)], DG_INK, 0.45)
        pg([(60, 10), (124, 10), (124, 24), (60, 24)], DG_GREY, DG_INK, 0.35)
        txt(u"Red Hall, Hadrian", 92, 26, 1.8, DG_INK, False, "C")
        for xa in (66, 94):
            pts = [(xa, 2)] + [(xa + 12 - 12 * math.cos(math.radians(a)), 2 + 6 * math.sin(math.radians(a)))
                               for a in range(0, 181, 15)] + [(xa + 24, 2)]
            ln(pts, DG_INK, 0.35)
        ln([(66, 4), (124, 4)], DG_INK, 0.3, (1.2, 0.9))
        ln([(124, 10), (130, 3), (192, 3)], DG_INK, 0.45)
        water(128, 192, 3, 6)
        ln([(128, 8.2), (192, 8.2)], "3F86B8", 0.3, (1.5, 1.0))
        txt(u"Q500", 190, 8.9, 1.6, "3F86B8", False, "R")
        steps(124, 140, 10, 4, 4)
        ln([(140, 12), (192, 12)], SQUARE_C, 0.6)
        txt(u"route on top to Üç Kemer", 190, 12.8, 1.8, SQUARE_C, False, "R")
        pg([(148, 18), (176, 18), (176, 19.4), (148, 19.4)], SQUARE_C)
        for x in (151, 162, 173):
            ln([(x, 12), (x, 18)], SQUARE_C, 0.35)
        dots(150, 174, lambda x: 19.4, 10, 0.4, SQUARE_C)
        txt(u"raised gathering", 162, 23.5, 1.9, SQUARE_C, True, "C")
        txt(u"gathering at the tunnel mouth", 132, 1.0, 1.8, SQUARE_C)
    elif node == "N5":
        ln([(0, 12), (128, 12), (150, 3), (192, 3)], DG_INK, 0.45)
        water(146, 192, 3, 6)
        for i in range(9):
            xa = 6 + i * 13.0
            pg([(xa, 12), (xa + 8, 12), (xa + 8, 17), (xa + 4, 19.5), (xa, 17)], DG_GREY, DG_INK, 0.3)
        ln([(124, 12), (124, 16)], DG_INK, 0.5)
        txt(u"backs to the stream", 122, 20, 1.8, DG_INK, False, "R")
        pg([(128, 12), (140, 12), (140, 17), (128, 17)], SQUARE_C)
        steps(140, 154, 12, 3.5, 4)
        txt(u"front yard to the water", 150, 14.5, 1.9, SQUARE_C, True, "L")
        arrow((60, 28), (60, 21))
        txt(u"town and village buses", 62, 26)
    elif node == "N6":
        ln([(0, 10), (110, 10), (122, 3), (150, 3), (158, 10), (192, 10)], DG_INK, 0.45)
        water(120, 152, 3, 6)
        for i in range(5):
            xa = 6 + i * 20.0
            pg([(xa, 10), (xa + 16, 10), (xa + 16, 15), (xa, 15)], DG_GREY, DG_INK, 0.3)
        ln([(156, 20), (196, 20)], DG_INK, 0.7)
        for x in (164, 180):
            ln([(x, 10), (x, 20)], DG_INK, 0.45)
        for yy_ in (22.5, 25.5):
            arrow((200, yy_), (168, yy_))
        txt(u"regional buses 643 644 836 936", 190, 27.5, 1.8, DG_INK, False, "R")
        pg([(104, 17), (146, 17), (146, 19.4), (104, 19.4)], SQUARE_C)
        for x in (108, 142):
            ln([(x, 10 if x < 110 else 6), (x, 17)], SQUARE_C, 0.35)
        txt(u"lifted, facing the arrival", 125, 21.5, 1.9, SQUARE_C, True, "C")
        txt(u"sheds", 40, 16.5, 1.8, DG_INK, False, "C")


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
        n_big = sum(1 for v_ in MPC["layers"].values() for e_ in v_ if len(e_[4]) > 2 and ar_(e_[4]) > MP_MAX_M2)
        MPC = dict(MPC, layers=dict((kk, [e_ for e_ in v_ if len(e_[4]) < 3 or ar_(e_[4]) <= MP_MAX_M2])
                                    for kk, v_ in MPC["layers"].items()))
        log.append(u"masterplan: %d sheet / texture frames over %.0f m2 left out" % (n_big, MP_MAX_M2))
        mp_cnt = MPn["mp_draw"](MPC, items, lambda xy: (X0 + F.local(xy)[0] * k, Y0 + F.local(xy)[1] * k), k,
                                (X0, Y0, X0 + F.w * k, Y0 + F.h * k), None,
                                layers=set(kk.split("/")[0] for kk in MPC["layers"]))
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
            (ex_rows if nm[0] else mp_rows).append(("box" if kind in ("a", "r", "s") else "line", col, nm[1]))
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
    for C, room in zip(cuts, SEC_ROOMS):
        x0, y0, x1, y1 = room
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
        for den_s in sorted(int(d_) for d_ in C.J["items"]):
            e_ = C.J["items"][str(den_s)]
            LYR = {"text": 8, "poly": 6, "line": 5, "circle": 7, "image": 9}     # v6.3 (Aras 13:01 UTC): no level
            body = [it for it in e_["items"] if not (it[0] == "text" and it[8] == "title" and (it[3] > -15.0 or
                                                                                            it[1].startswith(u"1:")))
                    and it[LYR.get(it[0], 0)] != "levels"]                                 # a new diagram shows it
            # v6.4 no-repeat (Aras 13:02 UTC, REUSE_MAP R10): plants drawn, no species callouts (slide 4 keeps them)
            px = set(round(it[2], 2) for it in body if it[0] == "text" and it[8] == "callouts" and
                     any(w in it[1] for w in (u"Meadow", u"grasses", u"reed", u"Kamış", u"iris", u"süsen")))
            body = [it for it in body if not (it[LYR.get(it[0], 0)] == "callouts" and round(
                it[1][0][0] if it[0] == "line" else (it[1] if it[0] == "circle" else it[2]), 2) in px)]
            bb = list(e_["bbox"])
            bb[3] = max([p_[1] for it in body if it[0] == "poly" for r in it[1] for p_ in r] +
                        [p_[1] for it in body if it[0] == "line" for p_ in it[1]] +
                        [it[3] + it[4] for it in body if it[0] == "text"] +
                        [it[2] + it[3] for it in body if it[0] == "circle"])
            w, h = bb[2] - bb[0], bb[3] - bb[1]
            f = min((x1 - x0) / w, (top_y - y0) / h)
            if f >= 0.85:
                break
        f = min(f, 1.3)
        items.append(T_(u"SECTION %s" % C.name, x0, y1 - 4.5, 4.5, INK, True, "L", "sections"))
        sub = next((it[1] for it in e_["items"] if it[0] == "text" and it[1].startswith(u"both banks")), u"")
        items.append(T_(sub, x0 + 42.0, y1 - 4.5, 2.4, GREY, False, "L", "sections"))
        sec_ids.update(id(it) for it in items[-2:])
        its = scale_items(body, f, bb[0], bb[3], x0 - bb[0], top_y - bb[3])
        items += its
        sec_ids.update(id(it) for it in its)
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
        rr = [0.0, 4.0, 8.0] if not sq else [0.0, 0.3 * r_m * k, 0.6 * r_m * k]
        cand = [(qa[0] + r * math.cos(a_ * math.pi / 8.0), qa[1] + r * math.sin(a_ * math.pi / 8.0), r)
                for r in rr for a_ in range(16 if r else 1)]
        cand = [c for c in cand if inside(c, 5.0)] or [(qa[0], qa[1], 0.0)]
        best = max(cand, key=lambda c: min([6.0] + [G["pc_dist"](c[:2], o) for o in occ]) - 0.05 * c[2])
        qa = best[:2]
        ang = math.atan2(qb[1] - qa[1], qb[0] - qa[0])
        for da in (-0.35, 0.35):
            items.append(L_([qa, (qa[0] + 9.0 * math.cos(ang + da), qa[1] + 9.0 * math.sin(ang + da))], SQUARE_C, 0.35,
                            "viewpoints"))
        items.append(R_([ring(qa[0], qa[1], 2.0, 24)], SQUARE_C, "FFFFFF", 0.3, "viewpoints"))
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
    occ = occ_points(B, items, sec_ids, OCC_LAYERS[1:])   # v7.3 (run 9: every corner FLAG): the node frame line may run under it
    xs = [p_[0] for it in sn if it[0] == "poly" for r in it[1] for p_ in r] + [it[2] for it in sn if it[0] == "text"]
    ys = [p_[1] for it in sn if it[0] == "poly" for r in it[1] for p_ in r] + [it[3] for it in sn if it[0] == "text"]
    sx0, sx1, sy0, sy1 = min(xs) - 1.0, max(xs) + 5.0, min(ys) - 1.0, max(ys) + 3.0
    best = None
    for dx in (0.0, X0 + 3.0 - sx0):
        for dy in (0.0, Y0 + F.h * k - 3.0 - sy1):
            n = sum(1 for o in occ if sx0 + dx <= o[0] <= sx1 + dx and sy0 + dy <= o[1] <= sy1 + dy)
            if best is None or n < best[0]:
                best = (n, dx, dy)
    items += scale_items(sn, 1.0, 0.0, 0.0, best[1], best[2])
    if best[0]:
        log.append(u"FLAG scale + north: every plan corner has marks under it (%d points in the best)" % best[0])

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
             ("line", P["mixh"](K["lines"]["town"][0], P["PAPER"], 0.55), u"bus lines, quiet"),
             ("disc", RED, u"heritage loop stop in the frame, loop order; the loop on slide 5"),
             ("box", K["hub"]["walk"], u"hub tile (K4, K3, T, K5, K6)"),
             ("line", "C0392B", u"section N#-A / N#-B: its two ends, the arrows look the way the section looks"),
             ] + ([] if mp_rows else [("hdr", None, u"PROPOSAL"),
                  ("line", SQUARE_C, u"streamside spine K4 - K5 along the Selinos (proposed path)")]) + [
             ("disc", SQUARE_C, u"V1 viewpoint of the perspective (place assumed)")]
    rows1, rows2 = [[(r_[0], r_[1], no_src(r_[2])) for r_ in rr_] for rr_ in (rows1, rows2)]   # v6.7: before wrapping
    cw = (PLAN_BOX[2] - PLAN_BOX[0]) / 2.0
    yk1 = P["draw_rows"](B, items, rows1, PLAN_BOX[0], ky, cw - 3.0, step=3.0, ts=2.1)
    yk2 = P["draw_rows"](B, items, rows2, PLAN_BOX[0] + cw, ky, cw - 3.0, step=3.4, ts=2.3)

    # ---- land use of the node frame (Page02's count, 1 m cells, on the node frame's own box)
    fq = [F.local(p) for p in nd["corners"]]
    fbox = (min(q[0] for q in fq), min(q[1] for q in fq), max(q[0] for q in fq), max(q[1] for q in fq))
    su = [u for u in units if fbox[0] <= u["cx"] <= fbox[2] and fbox[1] <= u["cy"] <= fbox[3]]
    lu, tot = P["land_use"](su, L, lc, fbox, log)
    # v6.4 (run 4, N2: the key ran long, land use had no room): under the shorter key column when they differ much
    lx0, bw, ly, ncmax = PLAN_BOX[0], PLAN_BOX[2] - PLAN_BOX[0], min(yk1, yk2) - 3.0, 5
    if yk1 < yk2 - 12.0:
        lx0, bw, ly, ncmax = PLAN_BOX[0] + cw, cw - 3.0, yk2 - 3.0, 3
    items.append(T_(u"LAND USE OF THE NODE FRAME · %.1f ha, 1 m cells (calculated)" % (tot / 1e4), lx0, ly,
                    2.8, INK, True, "L", "diagrams"))
    bar_y, bar_h = ly - 7.0, 4.0
    xx = lx0
    keep = [r_ for r_ in lu if r_[2] > 0]
    for lab, col, a_ in keep:
        w_ = bw * a_ / tot
        items.append(R_([box(xx, bar_y, xx + w_, bar_y + bar_h)], col, "FFFFFF", 0.15, "diagrams"))
        xx += w_
    rows = [("box", col, u"%s %s" % (no_src(lab), (u"%.0f%%" % (100.0 * a_ / tot)) if 100.0 * a_ / tot >= 0.5 else u"< 1%"))
            for lab, col, a_ in keep]
    # v6.2 (run 3, N2: rows ran into the credit line): as many columns as it takes to stay above y 10 mm
    per = max(1, int((bar_y - 5.0 - 10.0) / 3.0) + 1)
    ncmax = max(1, int(bw // 45.0))                       # v7.1 (run 8: "Mosques & sacred <" / "1%" wrapped)
    nc = max(1, -(-len(rows) // per))
    if nc > ncmax:
        log.append(u"FLAG land use: %d rows need %d columns; rows below y 10 mm cut" % (len(rows), nc))
        nc = ncmax
    third = -(-len(rows) // nc)
    for ci in range(nc):
        P["draw_rows"](B, items, rows[ci * third:(ci + 1) * third][:per], lx0 + ci * bw / nc, bar_y - 5.0,
                       bw / nc - 3.0, step=3.0, ts=2.1)

    # ---- v8 (Aras 16:30-16:32 UTC): why this node, its story and ONE abstract concept diagram (Niarchos sketch
    # spirit: the city as dots, the stream low, our move the only solid shape); water bars gone (slide 3 keeps seasons)
    st = STORY.get(node)
    if st:
        items.append(T_(u"WHY HERE · %s" % st[0].upper(), 214.0, 95.0, 2.8, INK, True, "L", "diagrams"))
        concept(node, items, 214.0, 62.0, 192.0, 30.0)
        yy = 56.5
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
    holder(310.0, 37.0, 406.0, 58.0, u"V1 · PERSPECTIVE · %s" % node,
           u"placeholder: Aras's render (Archicad, Unreal 5) from V1 on the plan", "placeholder_perspective")
    holder(310.0, 12.0, 356.0, 34.0, u"PROGRAM BRIEF", u"placeholder: what happens here, for whom, in which season",
           "placeholder_program")
    holder(360.0, 12.0, 406.0, 34.0, u"BUILDING PROPOSAL", u"placeholder: plan, section, elevation (if the node has one)",
           "placeholder_building")
    # ---- title band and credit
    items.append(T_(u"C  NODES IN DETAIL · SLIDE %d" % cfg["SLIDE"], 14.0, 288.0, 2.6, INK, True))
    items.append(T_(u"%s · %s" % (node, nd["name"]), 14.0, 278.5, 7.5, INK, True))
    intro = u"%s: why we chose this node, the node in plan (his masterplan over the town today) and its two cuts, " \
            u"A across the Selinos and B along the bank." % cfg["INTRO"].split(u":")[0]   # v8.1: no old levels text
    para(B, items, intro, 214.0, 288.0, 2.6, 192.0, INK, False, 3.6, "title")
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
    flags = [l for l in log if l.startswith(u"FLAG")]
    return u"%s\n%s, %d of 2 section(s), %d FLAG line(s), %.1f s" % (u"\n".join(log), node, len(done), len(flags),
                                                                    time.time() - t0)
