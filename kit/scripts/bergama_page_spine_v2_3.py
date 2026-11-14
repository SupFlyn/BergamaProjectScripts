# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE SPINE v2.3 (14 Nov 2026; v2.3 = Aras 16:17 UTC "KEEP EVERY DRAWING STRICTLY IN SITE_ALAN" (the one exception: Plan 01, Page02): the map strip is now exactly site_alan, turned along its long side, nothing drawn outside it; v2.2 = Aras 15:3x UTC "please take these from the masterplan that i have given you anything that concerns masterplans that should use it": the proposal on the map (terraces, canopy, walks, bridges, retaining walls, cycle route, designs) now comes from the MasterplanBase cache (his B19_setB_layers259.svg), the hand-drawn spine line is gone; v2.1 = run 4 review: upper spoke names clear of their marks, the diagram taller and the cards down to the page margin (23 mm were empty)), Panel Review II slide 2: the six nodes along the streamside spine
(output/presentation/2.pdf; one script per page, Aras 14 Nov 10:46 UTC).

v2 = Aras 15:25 UTC: "dont have this like that have nodes more like pointers and give some diagrams to explain and draw it
in landscape and fit every drawing into A3's like the scale is not important"; 15:26: "maybe semi transparent area fill
would be the answer". So: A3 landscape; the map a strip across the top, turned so the stream runs left to right, at the
scale that fits; each node a semi-transparent area (a "soft" item: flat colour through an 8-bit mask, the Basemap
writer's own item) with a pointer tag N#; under the map one card per node: what meets there (a spoke diagram: hub,
heritage loop stops, bus lines, shop buildings; a missing one dashed = the weak link), the hub's levels section,
the idea (N2, N4: Aras's two marks), the project's places in it. The v1 hub cards are folded into the node cards.
Kept rules: no sources on the page (log only, Aras 15:23); no repeats (stops and lines on slide 5, shop shading on
slide 1: counts only here); never import old PDF pages (code from CityLink v13: HUBS, FUNCS, hub_glyph).
v1 history: p9 spine + hub cards without the bottom band, p8 shops folded in (Aras 12:50 UTC).

Drawn from the one MapBase (pages_common pc_mapbase, turned), nodes from Data/section_lines.json (live: if the frames
move, this page follows), hubs, stops and heritage loop from Data/bergama_access_heritage.json.
Outputs (Downloads/Bergama/output/bergama_page_spine/): Spine.pdf, Spine.svg, review/ PNGs; copy presentation/2.pdf.
Reads: Data/bergama_pages_common.py, Data/bergama_access_heritage.json, Data/section_lines.json,
Data/selinos_centreline.json, cached MapBase (press MapBase first), newest scripts/bergama_basemap_v*.py (writer).
Grasshopper: a Button on any input runs it.
"""
import os, re, time, math, zlib, json

VERSION = "v2.3"
SLIDE = 2
GH_LABEL = "PageSpine"
OUT_FOLDER = "bergama_page_spine"
LOG_NAME = "bergama_page_spine_log.txt"
GH_INPUTS = {}
COMMON = os.path.join("Data", "bergama_pages_common.py")
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
NAME = "Spine"
PAGE_W, PAGE_H, MARGIN = 420.0, 297.0, 12.0      # A3 landscape (mm)
SIDE_W = 95.0                                    # the column right of the map: title, legend, north, scale
DEN_STEP = 500                                   # the scale is rounded up to a 1:500 step
CARD_GAP, CARD_PAD = 4.0, 2.4                    # mm
NODE_ALPHA = 0.32                                # the node areas' opacity
NODE_COL = dict(N1="70754C", N2="8B2D2D", N3="5C7A86", N4="4C2528", N5="89986A", N6="8E8F8A")   # palette colours
MP_ROWS = [(u"terraces (masterplan)", ("teras_-_canopy/teras",)), (u"canopy (masterplan)", ("teras_-_canopy/kanopi",)),
           (u"walks (masterplan)", ("yuruyus",)), (u"bridges (masterplan)", ("kopruler",)),
           (u"designs (masterplan)", ("desings",)), (u"retaining walls (masterplan)", ("istinaat",)),
           (u"cycle route (masterplan)", ("bisiklet",))]   # the layer names as the nodes pages use them
IDEAS = {   # Aras's two marks (thread "Develop building function ideas", 14 Nov 15:13-15:16 UTC); the others still open
    "N2": u"stepped gathering terraces into the river by the Roman bridge · a split ramp down to the water",
    "N4": u"gathering where the stream leaves the Roman tunnels · a route on top · a raised gathering point"}
MB_LAYERS = {"ground", "lc", "areas", "parks", "contours", "streets", "water", "walls", "buildings", "bridges", "trees"}
# MapBase layers: all but "veg" (the 2023 satellite cover stops inside this frame at x 29521 / y 32880: a seam; as Transit v2.5)
NODE_C = "4C2528"                    # node frames (palette 4C2528)
PLACE_C = "C07A2E"                   # the project's places (proposal orange, as the spine)
GLY = dict(structure="CFC8BA", water="A2B6B5", water_light="CFDBE4", water_deep="5C7A86", green="3C4733",
           ink2="6E675E", accent="C07A2E")
WHO = dict(L=u"residents", T=u"visitors", S=u"students")
GROWS = dict(W=u"water", E=u"stream edge", A=u"agriculture", H=u"heritage")
# CityLink v13 HUBS (L12875) and FUNCS (L686), names resolved through its names table (bergama_city_link_data.py)
HUBS = [
    dict(code="K4", pts=("K4",), kind="walk", role=u"Ulucami + Tabaklar Hamamı",
         trips=u"today 831-833 only · 2-3 trips a day each way",
         later=u"later step: a town line (e.g. 651) extended to Ulucami Önü", places=(7, 1)),
    dict(code="K3", pts=("K3",), kind="walk", role=u"the tanning reach: craft",
         trips=u"831-833 only · 2-3 trips a day each way", places=(6, 2)),
    dict(code="T", pts=("IST", "RED"), kind="hidden", role=u"the covered reach",
         trips=u"651: 54 departures a weekday, every 15-20 min", places=(3, 4)),
    dict(code="K5", pts=("K5",), kind="walk", role=u"producers' market",
         trips=u"656: 12 a weekday · 831-833: 2-3", places=(5,)),
    dict(code="K6", pts=("K6",), kind="gateway", role=u"gateway out of town",
         trips=u"643 644 651 652 653 656 836 936", places=()),
]
CH = dict(K4=467, K3=709, K5=1126, K6=1767)      # chainage m (h02 card s62, CityLink v13 L764)
PLACES = {
    1: dict(name=u"Bank bazaar", xy=(29890.4, 32243.6), who="LT", grows="HE",
            kw=(u"Ottoman bazaar on this bank: Papuçcular Arastası", u"stalls bring it back")),
    2: dict(name=u"Parchment and leather workshops", xy=(30062.0, 32106.0), who="TSL", grows="H",
            kw=(u"tanning named the stream · last master died 2026", u"teach and sell the craft")),
    3: dict(name=u"Junction square", xy=(30058.0, 32047.0), who="LTS", grows="WEH",
            kw=(u"the one place the main road meets the stream", u"a slot: view down to the water strip")),
    4: dict(name=u"Kızıl Avlu water terrace", xy=(30238.7, 31931.2), who="TL", grows="HW",
            kw=(u"Kızıl Avlu reopens: target 2026", u"its visitors step out onto the stream")),
    5: dict(name=u"Producers' market", xy=(30294.0, 31792.0), who="LT", grows="A",
            kw=(u"food from fields on our stored water · olive oil", u"Wednesdays · town producers' market: Saturdays")),
    6: dict(name=u"Study terraces", xy=(29941.0, 32200.0), who="SL", grows="EW",
            kw=(u"shaded seats by the water strip", u"for students · out of the street noise")),
    7: dict(name=u"Clean-water classroom", xy=None, ch=200, who="SL", grows="W",
            kw=(u"the cleaning basins as a lesson", u"how the stream works")),
}
KEYS = {"walk": [(u"DRY HUB", True), (u"street level, above Q500", False), (u"SUB-HUB in the bed", True),
                 (u"open Jul-Sep · shut in floods", False)],
        "hidden": [(u"HIDDEN STREAM SQUARE", True), (u"water line in the paving over the culvert", False),
                   (u"KIZIL AVLU TUNNEL MOUTHS", True), (u"a viewing edge", False)],
        "gateway": [(u"GATEWAY OUT", True), (u"no hub square", False)]}
WORD = {"walk": u"walking hub", "transit": u"MAIN TRANSIT HUB", "gateway": u"gateway"}


def load_common():
    p = os.path.join(BERGAMA_ROOT, COMMON)
    if not os.path.isfile(p):
        raise RuntimeError(u"%s missing: run Bergama.bat once (the kit copies it), then press again" % p)
    ns = {"__name__": "bergama_pages_common"}
    with open(p, encoding="utf-8") as f:
        exec(compile(f.read(), p, "exec"), ns)
    return ns


def no_src(t):
    """v1.3: a legend text without its brackets (the sources) and without repeated parts"""
    out = []
    for part in t.split(u" · "):
        part = re.sub(r"\s*\([^)]*\)", u"", part).strip(u" ;,")
        if part and part.lower() not in [o.lower() for o in out]:
            out.append(part)
    return u" · ".join(out)


def pip(x, y, R):
    c = False
    for (x1, y1), (x2, y2) in zip(R, R[1:] + R[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


def glyph(G, kind, x, y, w, h):
    """CityLink v13 hub_glyph (L11815) as items: the hub's levels as a small section in (x, y - h)-(x + w, y)"""
    P_, L_ = G["P_"], G["L_"]
    P = lambda pts: [(x + a * w / 10.0, y - h + b * h / 8.0) for a, b in pts]
    it = []
    if kind == "walk":
        it.append(P_([P([(0, 0), (0, 5.6), (4.2, 5.6), (4.2, 4.65), (4.75, 4.65), (4.75, 3.7), (5.3, 3.7), (5.3, 2.75),
                         (5.85, 2.75), (5.85, 1.8), (8.0, 1.8), (8.0, 0.8), (10, 0.8), (10, 0)])], GLY["structure"],
                     None, 0.0, "cards"))
        it.append(P_([P([(8.0, 0.8), (10, 0.8), (10, 1.5), (8.0, 1.5)])], GLY["water"], None, 0.0, "cards"))
        it.append(L_(P([(0, 5.6), (4.2, 5.6)]), GLY["green"], 0.8, "cards"))
        it.append(L_(P([(5.85, 1.8), (8.0, 1.8)]), GLY["water_deep"], 0.8, "cards"))
        it.append(L_(P([(4.2, 5.0), (10, 5.0)]), GLY["water_deep"], 0.3, "cards", (0.8, 0.6)))   # Q500
    elif kind == "hidden":
        it.append(P_([P([(0, 0), (0, 5.6), (10, 5.6), (10, 0)])], GLY["structure"], None, 0.0, "cards"))
        it.append(P_([P([(3.2, 0.6), (7.2, 0.6), (7.2, 2.6), (6.4, 3.4), (4.0, 3.4), (3.2, 2.6)])], GLY["water_light"],
                     None, 0.0, "cards"))
        it.append(P_([P([(3.2, 0.6), (7.2, 0.6), (7.2, 1.3), (3.2, 1.3)])], GLY["water"], None, 0.0, "cards"))
        it.append(L_(P([(0, 5.6), (10, 5.6)]), "2B2B2B", 0.6, "cards"))
        it.append(L_(P([(2.0, 5.95), (8.4, 5.95)]), GLY["water_deep"], 0.9, "cards"))
    else:
        it.append(P_([P([(0, 2.6), (7.0, 2.6), (7.0, 4.4), (0, 4.4)])], GLY["ink2"], None, 0.0, "cards"))
        it.append(P_([P([(7.0, 1.6), (10, 3.5), (7.0, 5.4)])], GLY["accent"], None, 0.0, "cards"))
    return it




def soft_poly(R, colour, alpha, layer, clip, ppm=4.0):
    """a semi-transparent area: the ring R (page mm) as a flat colour through an 8-bit mask ("soft" item of the
    Basemap writer, PDF and SVG), ppm pixels a mm"""
    x0, y0 = min(p[0] for p in R), min(p[1] for p in R)
    x1, y1 = max(p[0] for p in R), max(p[1] for p in R)
    pw, ph = max(1, int(math.ceil((x1 - x0) * ppm))), max(1, int(math.ceil((y1 - y0) * ppm)))
    a = int(round(255 * alpha))
    out = bytearray()
    E = list(zip(R, R[1:] + R[:1]))
    for j in range(ph):                                  # top row first
        y = y1 - (j + 0.5) / ppm
        xs = sorted(p[0] + (y - p[1]) * (q[0] - p[0]) / (q[1] - p[1]) for p, q in E if (p[1] > y) != (q[1] > y))
        row = bytearray(pw)
        for i in range(0, len(xs) - 1, 2):
            i0 = max(0, int(round((xs[i] - x0) * ppm)))
            i1 = min(pw, int(round((xs[i + 1] - x0) * ppm)))
            row[i0:i1] = bytes([a]) * max(0, i1 - i0)
        out += row
    return ("soft", zlib.compress(bytes(out), 9), pw, ph, x0, y0, pw / ppm, ph / ppm, colour, None, layer, clip)


def mp_swatch(ns, C, prefixes):
    """the colour a masterplan group is drawn in (its first piece): ("area", fill, stroke) / ("line", stroke, None)"""
    for pre in prefixes:
        for key in ns["mp_keys"](C, pre):
            for kind, fill, stroke, w, P in C["layers"][key]:
                if kind == "a":
                    return ("area", next((v for wd, v in ns["AREA_FILL"].items() if wd in key.split("/")),
                                         ns["AREA_DEFAULT"]), None)
                if kind == "r" and (fill or stroke):
                    return ("area", fill, stroke)
                if kind == "l" and stroke:
                    return ("line", stroke, None)
    return None


def node_card(G, lib, K, nk, nd, info, x, ytop, w, hfix=None, dh=38.0):
    """one node card: head, what meets here (spoke diagram), the hub's levels, the idea, the places, the weak link;
    returns (items, height mm)"""
    P_, L_, T_, circle, wrap = G["P_"], G["L_"], G["T_"], G["circle"], G["wrap"]
    tw = lib["text_w"]
    INK = K["ink"]
    col = NODE_COL.get(nk, NODE_C)
    it = []
    xi, wi = x + CARD_PAD, w - 2 * CARD_PAD

    def para(s, y, size, c=INK, bold=False, xx=None, ww=None, al="L"):
        xx = xi if xx is None else xx
        for ln in wrap(s, size, ww or wi, tw, bold):
            it.append(T_(ln, xx, y - size * 0.75, size, c, "cards", bold, al))
            y -= size * 1.32
        return y
    y = ytop - 2.0 - CARD_PAD
    tile = (9.0, 6.0)
    it.append(P_([[(xi, y - tile[1]), (xi + tile[0], y - tile[1]), (xi + tile[0], y), (xi, y)]], col, None, 0.0, "cards"))
    it.append(T_(nk, xi + tile[0] / 2, y - tile[1] + 1.6, 3.2, "FFFFFF", "cards", True, "C"))
    y2 = para(nd["name"], y - 0.4, 3.2, INK, True, xi + tile[0] + 2.0, wi - tile[0] - 2.0)
    y = min(y - tile[1], y2) - 2.4
    # ---- what meets here: the node in the middle, four spokes; a missing one dashed grey (the weak link)
    it.append(T_(u"WHAT MEETS HERE", xi, y - 2.0, 2.3, GLY["ink2"], "cards", True))
    y -= 4.0
    cx, cy = xi + wi / 2.0, y - dh / 2.0
    spokes = [(u"hub", info["hubs"], -wi * 0.30, dh * 0.30), (u"heritage loop", info["loop"], wi * 0.30, dh * 0.30),
              (u"bus lines", info["bus"], -wi * 0.30, -dh * 0.30), (u"shop buildings", info["shops"], wi * 0.30, -dh * 0.30)]
    for name, val, dx, dy in spokes:
        ex, ey = cx + dx, cy + dy
        has = bool(val)
        it.append(L_([(cx, cy), (ex, ey)], col if has else "B0AC9C", 0.7 if has else 0.35, "cards",
                     None if has else (0.8, 0.7)))
        if name == u"hub" and has:
            for i_, (code, kd) in enumerate(val):
                hx = ex + (i_ - (len(val) - 1) / 2.0) * 7.0
                c_ = K["hub"]["transit" if kd == "hidden" else kd]
                it.append(P_([[(hx - 3.0, ey - 3.0), (hx + 3.0, ey - 3.0), (hx + 3.0, ey + 3.0), (hx - 3.0, ey + 3.0)]],
                             c_, "FFFFFF", 0.3, "cards"))
                it.append(T_(code, hx, ey - 1.0, 2.4, "FFFFFF", "cards", True, "C"))
            lab = u"hub"
        elif name == u"heritage loop" and has:
            for i_, (n_, nm) in enumerate(val):
                hx = ex + (i_ - (len(val) - 1) / 2.0) * 6.0
                it.append(P_([circle(hx, ey, 2.6, 24)], K["heritage"], "FFFFFF", 0.3, "cards"))
                it.append(T_(n_, hx, ey - 0.9, 2.4, "FFFFFF", "cards", True, "C"))
            lab = u"loop stop " + u", ".join(nm for n_, nm in val)
        elif has:
            it.append(P_([circle(ex, ey, 3.4, 28)], "FFFFFF", col, 0.5, "cards"))
            it.append(T_(str(val), ex, ey - 1.0, 2.6, col, "cards", True, "C"))
            lab = name
        else:
            it.append(P_([circle(ex, ey, 2.6, 24)], "FFFFFF", "B0AC9C", 0.35, "cards"))
            lab = u"no " + (u"loop stop" if name == u"heritage loop" else name.rstrip(u"s").replace(u" line", u" line"))
        lns = wrap(lab, 2.2, wi * 0.48, tw)
        ly = ey + 4.4 + (len(lns) - 1) * 2.8 if dy > 0 else ey - 7.0   # v2.1: above the mark, last line lowest
        for j_, ln in enumerate(lns):
            it.append(T_(ln, ex, ly - j_ * 2.8, 2.2, INK if has else GLY["ink2"], "cards", False, "C"))
    it.append(P_([circle(cx, cy, 5.2, 36)], col, "FFFFFF", 0.4, "cards"))
    it.append(T_(nk, cx, cy - 1.1, 3.0, "FFFFFF", "cards", True, "C"))
    y = cy - dh / 2.0 - 3.0
    # ---- the hub's levels (CityLink v13 hub_glyph) with its keys
    if info["hub_kind"]:
        gw = min(30.0, wi * 0.48)
        gh = gw * 15.0 / 24.0
        it += glyph(G, info["hub_kind"], xi, y, gw, gh)
        ky = y
        for j, (s_, b_) in enumerate(KEYS[info["hub_kind"]]):
            if j and b_:
                ky -= 0.6
            ky = para(s_, ky, 2.1, INK, b_, xi + gw + 2.0, wi - gw - 2.0)
        y = min(y - gh, ky) - 2.4
    # ---- the idea
    it.append(T_(u"IDEA", xi, y - 2.0, 2.3, GLY["ink2"], "cards", True))
    y = para(IDEAS.get(nk, u"open"), y - 3.4, 2.4, col if nk in IDEAS else GLY["ink2"], nk in IDEAS) - 1.8
    # ---- the project's places in the node
    for n in info["places"]:
        f = PLACES[n]
        it.append(P_([circle(xi + 1.8, y - 1.8, 1.8, 24)], "FFFFFF", PLACE_C, 0.35, "cards"))
        it.append(T_(str(n), xi + 1.8, y - 2.6, 2.2, PLACE_C, "cards", True, "C"))
        y = para(f["name"], y - 0.2, 2.4, INK, True, xi + 5.0, wi - 5.0)
        y = para(f["kw"][0] + u" · " + f["kw"][1], y, 2.1, INK, False, xi + 5.0, wi - 5.0) - 1.2
    # ---- the weak link (what is missing, from the spokes)
    miss = [s for s, v in ((u"no hub", info["hubs"]), (u"no heritage loop stop", info["loop"]),
                           (u"no bus line", info["bus"]), (u"no shops", info["shops"])) if not v]
    y -= 0.8
    it.append(T_(u"WEAK LINK", xi, y - 2.0, 2.3, GLY["ink2"], "cards", True))
    y = para(u" · ".join(miss) if miss else u"none of the four missing", y - 3.4, 2.4, INK) - 1.0
    h = max(ytop - (y - CARD_PAD), hfix or 0.0)
    yb = ytop - h
    return [P_([[(x, ytop - 2.0), (x + w, ytop - 2.0), (x + w, ytop), (x, ytop)]], col, None, 0.0, "cards"),
            P_([[(x, yb), (x + w, yb), (x + w, ytop), (x, ytop)]], None, "B0AC9C", 0.25, "cards")] + it, h


def main():
    t0 = time.time()
    log = []
    G = load_common()
    lib = G["pc_lib"](log)
    D = G["pc_data"](log)
    K = D["key"]
    with open(os.path.join(BERGAMA_ROOT, "Data", "section_lines.json"), encoding="utf-8") as f:
        NODES = json.load(f)["nodes"]
    dist, L_, P_, T_, circle, wrap = G["pc_dist"], G["L_"], G["P_"], G["T_"], G["circle"], G["wrap"]
    INK, tm, tw = K["ink"], K["text_mm"], lib["text_w"]
    H = D["hubs"]
    nks = sorted(NODES)
    cen = dict((k, (sum(p[0] for p in NODES[k]["corners"]) / len(NODES[k]["corners"]),
                    sum(p[1] for p in NODES[k]["corners"]) / len(NODES[k]["corners"]))) for k in nks)
    # ---- the map = site_alan exactly (v2.3), turned along its long side so node N1 to N6 runs left to right
    mpns, MPC = G["pc_mp_data"](log)                     # the MasterplanBase library also reads site_alan
    SA = mpns["site_alan"](log)
    e_ = max(zip(SA, SA[1:] + SA[:1]), key=lambda e: dist(e[0], e[1]))
    a = math.atan2(e_[1][1] - e_[0][1], e_[1][0] - e_[0][0])
    if math.cos(a) * (cen[nks[-1]][0] - cen[nks[0]][0]) + math.sin(a) * (cen[nks[-1]][1] - cen[nks[0]][1]) < 0:
        a += math.pi
    ca, sa = math.cos(a), math.sin(a)
    rot = lambda p: (p[0] * ca + p[1] * sa, -p[0] * sa + p[1] * ca)
    pts = [rot(p) for p in SA]
    u0, u1 = min(p[0] for p in pts), max(p[0] for p in pts)
    v0, v1 = min(p[1] for p in pts), max(p[1] for p in pts)
    off = max(min(abs(p[0] - u0), abs(p[0] - u1)) + min(abs(p[1] - v0), abs(p[1] - v1)) for p in pts)
    if off > 1.0:
        log.append(u"FLAG: site_alan is not a rectangle (a corner %.1f m off its turned box): the frame is that box" % off)
    mw_max = PAGE_W - 2 * MARGIN - 8.0 - SIDE_W
    den = int(math.ceil((u1 - u0) / mw_max * 1000.0 / DEN_STEP) * DEN_STEP)
    k = 1000.0 / den
    mw, mh = (u1 - u0) * k, (v1 - v0) * k
    log.append(u"map = site_alan, %.0f x %.0f m" % (u1 - u0, v1 - v0))

    class RM(G["Map"]):
        def __init__(self):
            self.den, self.k = float(den), k
            self.mw, self.mh = mw, mh
            self.x0, self.y0 = MARGIN, PAGE_H - MARGIN - mh
            self.w, self.h = PAGE_W, PAGE_H
            self.box = (self.x0, self.y0, self.x0 + mw, self.y0 + mh)
            self.b = None

        def T(self, p):
            q = rot(p)
            return (self.x0 + (q[0] - u0) * k, self.y0 + (q[1] - v0) * k)
    M = RM()
    T = M.T
    log.append(u"map: turned %.1f deg (node %s to %s left to right), 1:%d, %.0f x %.0f mm" % (
        math.degrees(a), nks[0], nks[-1], den, mw, mh))

    # ---- what each node holds (calculated)
    ns, C = G["pc_mb_data"](log)
    shops = [(sum(p[0] for p in R) / len(R), sum(p[1] for p in R) / len(R)) for R, fab_, com, src, nm in C["bld"] if com]
    lines_of = G["pc_stop_lines"](D)
    info = {}
    for nk in nks:
        R = NODES[nk]["corners"]
        inn = lambda xy: pip(xy[0], xy[1], R)
        hubs = [(hb["code"], hb["kind"]) for hb in HUBS if any(inn(H[p]) for p in hb["pts"])]
        loop = [(h["n"], h["name"]) for h in D["heritage"] if inn(h["xy"])]
        bus = set()
        for s in D["stops"]:
            if inn(s["xy"]):
                bus |= set(lines_of.get(s["name"], s["lines"]))
        info[nk] = dict(hubs=hubs, loop=loop, bus=len(bus), shops=sum(1 for s in shops if inn(s)),
                        hub_kind=hubs[0][1] if hubs else None,
                        places=[n for n, f in sorted(PLACES.items()) if f["xy"] and inn(f["xy"])])
        log.append(u"%s %s: hubs %s; loop %s; %d bus lines; %d shop buildings; places %s" % (
            nk, NODES[nk]["name"], u" ".join(c for c, _ in hubs) or u"-", u" ".join(n for n, _ in loop) or u"-",
            len(bus), info[nk]["shops"], u" ".join(str(n) for n in info[nk]["places"]) or u"-"))

    # ---- the map
    MB = G["pc_mapbase"](M, K, log, MB_LAYERS, {"lc_light": 0.8})
    items = MB[0]
    items += G["pc_study"](M, K, log)
    lab = G["Labels"](M, lib)
    cnt = mpns["mp_draw"](MPC, items, T, k, M.box, "map", set(p for _, ps in MP_ROWS for p in ps))
    log.append(u"masterplan drawn: " + (u", ".join(u"%s %d" % kv for kv in sorted(cnt.items())) or u"nothing"))
    if not cnt:
        log.append(u"FLAG: no masterplan piece inside the map strip")
    for nk in nks:                                       # the node areas, semi-transparent
        items.append(soft_poly([T(p) for p in NODES[nk]["corners"]], NODE_COL.get(nk, NODE_C), NODE_ALPHA,
                               "node_areas", "map"))
    inbox = lambda q, r=0.0: M.box[0] + r <= q[0] <= M.box[2] - r and M.box[1] + r <= q[1] <= M.box[3] - r
    for n, f in sorted(PLACES.items()):
        if f["xy"] and not inbox(T(f["xy"]), 1.5):
            log.append(u"place %d outside site_alan: not drawn" % n)
        elif f["xy"]:
            q = T(f["xy"])
            items.append(P_([circle(q[0], q[1], 1.5, 20)], "FFFFFF", PLACE_C, 0.35, "places"))
            items.append(T_(str(n), q[0], q[1] - 0.65, 1.8, PLACE_C, "places", True, "C"))
            lab.block_pt(q, 1.8)
    s_ = 3.6
    for hb in HUBS:
        c_ = K["hub"]["transit" if hb["kind"] == "hidden" else hb["kind"]]
        for p in hb["pts"]:
            q = T(H[p])
            if not inbox(q, s_ / 2):
                log.append(u"hub %s (%s) outside site_alan: not drawn" % (hb["code"], p))
                continue
            items.append(P_([[(q[0] - s_ / 2, q[1] - s_ / 2), (q[0] + s_ / 2, q[1] - s_ / 2), (q[0] + s_ / 2, q[1] + s_ / 2),
                              (q[0] - s_ / 2, q[1] + s_ / 2)]], c_, "FFFFFF", 0.25, "hubs"))
            items.append(T_(hb["code"], q[0], q[1] - 0.7, 2.0, "FFFFFF", "hubs", True, "C"))
            lab.block_pt(q, s_ / 2 + 0.3)
    # pointers: a tag above (odd) or below (even) the node's area, a leader to its middle
    for i, nk in enumerate(nks):
        RR = [T(p) for p in NODES[nk]["corners"]]
        c = T(cen[nk])
        up = i % 2 == 0
        ye = (max(p[1] for p in RR) + 5.0) if up else (min(p[1] for p in RR) - 5.0)
        ye = min(M.box[3] - 6.0, max(M.box[1] + 6.0, ye))
        txt = u"%s %s" % (nk, NODES[nk]["name"])
        wt = tw(txt, 2.6, True) + 3.0
        xe = min(M.box[2] - wt / 2.0 - 1.0, max(M.box[0] + wt / 2.0 + 1.0, c[0]))
        col = NODE_COL.get(nk, NODE_C)
        items.append(L_([c, (xe, ye - 2.2 if up else ye + 2.2)], col, 0.35, "node_pointers"))
        items.append(P_([circle(c[0], c[1], 0.9, 16)], col, "FFFFFF", 0.2, "node_pointers"))
        items.append(P_([[(xe - wt / 2, ye - 2.2), (xe + wt / 2, ye - 2.2), (xe + wt / 2, ye + 2.2), (xe - wt / 2, ye + 2.2)]],
                        col, "FFFFFF", 0.3, "node_pointers"))
        items.append(T_(txt, xe, ye - 0.95, 2.6, "FFFFFF", "node_pointers", True, "C"))
    items += lab.items
    items.append(P_([[(M.box[0], M.box[1]), (M.box[2], M.box[1]), (M.box[2], M.box[3]), (M.box[0], M.box[3])]], None,
                    INK, 0.25, "frame"))

    # ---- the node cards under the map
    yt = M.box[1] - 9.0
    items.append(T_(u"THE SIX NODES: WHAT MEETS AT EACH, WHAT IS MISSING", MARGIN, yt + 3.0, tm["sub"], INK, "cards", True))
    cw = (PAGE_W - 2 * MARGIN - (len(nks) - 1) * CARD_GAP) / len(nks)
    hc = max(node_card(G, lib, K, nk, NODES[nk], info[nk], 0.0, 0.0, cw)[1] for nk in nks)
    room = yt - MARGIN
    dh = 38.0 + max(0.0, min(20.0, room - hc - 2.0))     # v2.1: the spare height goes to the diagram
    hc = max(node_card(G, lib, K, nk, NODES[nk], info[nk], 0.0, 0.0, cw, None, dh)[1] for nk in nks)
    hc = max(hc, room)                                   # the cards reach the page margin
    if hc > room + 0.1:
        log.append(u"FLAG: the node cards need %.0f mm, the page gives %.0f mm under the map" % (hc, room))
    for i, nk in enumerate(nks):
        items += node_card(G, lib, K, nk, NODES[nk], info[nk], MARGIN + i * (cw + CARD_GAP), yt, cw, hc, dh)[0]

    # ---- the side column: title, legend, north, scale
    x = M.box[2] + 8.0
    y = M.box[3] - tm["title"]
    for ln in wrap(u"THE SIX NODES ALONG THE SPINE", tm["title"], SIDE_W, tw, True):
        items.append(T_(ln, x, y, tm["title"], INK, "title", True))
        y -= tm["title"] * 1.25
    for ln in wrap(u"Where the town meets the stream, node by node", tm["sub"], SIDE_W, tw):
        items.append(T_(ln, x, y, tm["sub"], INK, "title"))
        y -= tm["sub"] * 1.4
    y -= 3.0
    sq = lambda f_, s__=3.0: (lambda xx, yy: [P_([[(xx - s__ / 2, yy - s__ / 2), (xx + s__ / 2, yy - s__ / 2),
                                                 (xx + s__ / 2, yy + s__ / 2), (xx - s__ / 2, yy + s__ / 2)]],
                                               f_, "FFFFFF", 0.25, "legend")])
    rows = [(lambda xx, yy: [soft_poly([(xx - 4.5, yy - 1.8), (xx + 4.5, yy - 1.8), (xx + 4.5, yy + 1.8),
                                        (xx - 4.5, yy + 1.8)], NODE_COL["N2"], NODE_ALPHA, "legend", None)],
             u"node area, its tag points to its card"),
            (lambda xx, yy: [P_([circle(xx, yy, 1.5, 20)], "FFFFFF", PLACE_C, 0.35, "legend")],
             u"the project's places, numbered as on the cards"),
            (sq(K["hub"]["walk"]), u"walking hub"), (sq(K["hub"]["transit"]), u"main transit hub"),
            (sq(K["hub"]["gateway"]), u"gateway out of town"),
            (lambda xx, yy: [P_([circle(xx, yy, 1.6, 20)], K["heritage"], "FFFFFF", 0.25, "legend")],
             u"heritage loop stop (cards)")]
    for txt, pres in MP_ROWS:                            # masterplan rows, in the colours the map uses
        sw = mp_swatch(mpns, MPC, pres) if any(c_.split("/")[0] in pres or any(c_ == p_ or c_.startswith(p_ + "/")
                                                                                for p_ in pres) for c_ in cnt) else None
        if not sw:
            log.append(u"legend: %s not on the map, no row" % txt)
            continue
        if sw[0] == "line":
            rows.append(((lambda c__: lambda xx, yy: [L_([(xx - 4.5, yy), (xx + 4.5, yy)], c__, 0.6, "legend")])(sw[1]),
                         txt))
        else:
            rows.append(((lambda f__, s__: lambda xx, yy: [P_([[(xx - 4.5, yy - 1.8), (xx + 4.5, yy - 1.8),
                                                                 (xx + 4.5, yy + 1.8), (xx - 4.5, yy + 1.8)]],
                                                               f__, s__, 0.2 if s__ else 0.0, "legend")])(sw[1], sw[2]),
                         txt))
    for draw, txt in rows:
        items += draw(x + 5.0, y - 1.0)
        yy = y
        for ln in wrap(txt, tm["legend"] - 0.2, SIDE_W - 14.0, tw):
            items.append(T_(ln, x + 13.0, yy - 2.0, tm["legend"] - 0.2, INK, "legend"))
            yy -= (tm["legend"] - 0.2) * 1.3
        y = min(y - 5.0, yy - 1.5)
    yb = M.box[1] + 7.0                                  # north (turned) + scale bar at the column's foot
    if y < yb + 12.0:
        log.append(u"FLAG: the legend reaches the north arrow (%.1f mm)" % (y - yb - 12.0))
    cx, cy, r = x + 5.5, yb + 1.0, 4.5
    nd_ = math.degrees(a)
    can, san = math.cos(math.radians(nd_)), math.sin(math.radians(nd_))
    rr = lambda dx, dy: (cx + dx * can + dy * san, cy - dx * san + dy * can)
    items.append(P_([circle(cx, cy, r, 40)], None, INK, 0.2, "north_scale"))
    items.append(P_([[rr(0, r), rr(-2.0, -2.2), rr(0, -1.0), rr(2.0, -2.2)]], INK, None, 0.0, "north_scale"))
    qn = rr(0, r + 2.2)
    items.append(T_(u"N", qn[0], qn[1] - 0.9, 2.4, INK, "north_scale", True, "C"))
    bar = 250.0 if den <= 12000 else 500.0
    Lb, xb = bar * k, x + 16.0
    for i in range(4):
        items.append(P_([[(xb + Lb * i / 4, yb), (xb + Lb * (i + 1) / 4, yb), (xb + Lb * (i + 1) / 4, yb + 1.2),
                          (xb + Lb * i / 4, yb + 1.2)]], INK if i % 2 == 0 else "FFFFFF", INK, 0.15, "north_scale"))
    items.append(T_(u"0", xb, yb - 2.8, 2.0, INK, "north_scale", False, "C"))
    items.append(T_(u"%d m" % bar, xb + Lb, yb - 2.8, 2.0, INK, "north_scale", False, "C"))
    items.append(T_(u"1:%s" % format(den, ",d"), xb, yb + 3.0, 2.8, INK, "north_scale", True))

    log.append(u"sources (log only): " + D["sources"]["osm"] + u"; hubs, places, hub sections: CityLink v13 "
               u"(SUBMISSION_SON p9); proposal: MasterplanBase (B19_setB_layers259.svg); context: MapBase; nodes: Data/section_lines.json; ideas N2, N4: Aras 14 Nov")
    orig = G["pc_frame_check"]                           # the cards and the column sit outside the map frame by design
    G["pc_frame_check"] = lambda its, box, lg, tw_=None: orig(its, box, lg, tw_, skip=G["PC_SHEET_LAYERS"] + (
        "cards", "node_pointers"))
    paths = G["pc_write"](lib, M, items, OUT_DIR, NAME, u"The six nodes along the spine", log)
    pdfs = [p_ for p_ in paths if p_.lower().endswith(".pdf")]
    if pdfs:
        G["pc_present"](pdfs[0], SLIDE, log)
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
