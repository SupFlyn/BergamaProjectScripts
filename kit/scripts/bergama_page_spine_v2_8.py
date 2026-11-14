# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE SPINE v2.8 (14 Nov 2026; v2.8 = Aras 21:31 UTC "all the diagrams are awful": "What meets here" redrawn to library/diagram_style/DIAGRAM_STYLE.md v1 (one cut across the stream, poché ground, context rhythm, drivers at the edges, one accent for the move, people on it, at most 4 labels, the claim as title); the card plans, tiles and hub glyph removed; v2.7 = Aras 21:21 UTC "recheck every drawing for not applied feedback": the Q500 level mark left in the hub glyph and its key removed (Aras: remove the water and level markers), card plans and their counts cut to site_alan (16:17 rule), masterplan rows say "proposed" not "masterplan" (no sources on drawings), card water textured (water rule); v2.6 = run 7 review: neighbourhood and street lines cut to their frames (a line's clip id sits at item[4]), smoother area edges (8 mask pixels a mm); v2.5 = run 6: a shorter legend row (it ran over its column); v2.4 = Aras 16:19 UTC "mark the areas properly mark the areas that are neighborhoods diversify neighborhoods according to their specialities" and 16:22 UTC on the what-meets-here diagrams "too basic ... more diagramatic more in a architectural design language way": node areas follow their blocks, not boxes; the neighbourhoods (OSM mahalle boundaries) drawn and named with their main fabric, the two neighbourhood nodes (N1, N5) coloured by it; each card's diagram is now the node's own plan (figure-ground, stream, masterplan, hub / loop stops / places at their points, bar, north) over a row of four tiles; the legend a band under the map; the frame from pages_common SiteMap; v2.3 = Aras 16:17 UTC "KEEP EVERY DRAWING STRICTLY IN SITE_ALAN" (the one exception: Plan 01, Page02): the map strip is now exactly site_alan, turned along its long side, nothing drawn outside it; v2.2 = Aras 15:3x UTC "please take these from the masterplan that i have given you anything that concerns masterplans that should use it": the proposal on the map (terraces, canopy, walks, bridges, retaining walls, cycle route, designs) now comes from the MasterplanBase cache (his B19_setB_layers259.svg), the hand-drawn spine line is gone; v2.1 = run 4 review: upper spoke names clear of their marks, the diagram taller and the cards down to the page margin (23 mm were empty)), Panel Review II slide 2: the six nodes along the streamside spine
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

VERSION = "v2.8"
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
SIDE_W = 95.0                                    # the column right of the map: title, north, scale (v2.4: legend under the map)
DEN_STEP = 500                                   # the scale is rounded up to a 1:500 step
CARD_GAP, CARD_PAD = 4.0, 2.4                    # mm
NODE_ALPHA = 0.32                                # the node areas' opacity
EDGE_ALPHA = 0.9                                 # v2.4: their edge (one mask pixel, 0.25 mm)
MASK_PPM = 8.0                                   # v2.4: mask pixels a mm (v2.6: 8, smoother edges)
CLOSE_M, ERODE_M = 12.0, 9.0                     # v2.4: the area closes over streets up to 2 x 12 m wide, then 9 m back
NEIGH_NODES = ("N1", "N5")                       # the nodes that are neighbourhoods (section_lines.json names:
                                                 # "Neighbourhoods (Upper + Lower)", "Settled Housing")
MIN_BLD = 15                                     # a neighbourhood with fewer buildings in site_alan gets no name
CHAR_COL = {"traditional": "B5562F", "block": "4A6A8A", "regular": "C8A03C", "selfbuilt": "6E8B5E",
            "large": "5F5F66", "monument": "A33B2B", "sacred": "A33B2B"}   # our picks; a neighbourhood's main fabric
MAH_C = "6E675E"                                 # v2.4: neighbourhood lines and names
DG = dict(ground="F4F1EA", street="FFFFFF", water="~A2B6B5", bld="8E897F")   # v2.7: water with the grain (textured)     # v2.4: the card plans
NODE_COL = dict(N1="70754C", N2="8B2D2D", N3="5C7A86", N4="4C2528", N5="89986A", N6="8E8F8A")   # palette colours
MP_ROWS = [(u"terraces (proposed)", ("teras_-_canopy/teras",)), (u"canopy (proposed)", ("teras_-_canopy/kanopi",)),
           (u"walks (proposed)", ("yuruyus",)), (u"bridges (proposed)", ("kopruler",)),
           (u"designs (proposed)", ("desings",)), (u"retaining walls (proposed)", ("istinaat",)),
           (u"cycle route (proposed)", ("bisiklet",))]   # the layer names as the nodes pages use them
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
KEYS = {"walk": [(u"DRY HUB", True), (u"street level", False), (u"SUB-HUB in the bed", True),
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


# ================================================================ v2.4: areas that follow the fabric, neighbourhoods
def fill_ring(g, W, H, gx0, gy1, ppm, R, val):
    """scanline fill of the ring R (page mm) into the byte grid g (W x H, row 0 at the top edge gy1)"""
    if len(R) < 3:
        return
    ys = [p[1] for p in R]
    j0, j1 = max(0, int((gy1 - max(ys)) * ppm)), min(H - 1, int((gy1 - min(ys)) * ppm) + 1)
    E = list(zip(R, R[1:] + R[:1]))
    for j in range(j0, j1 + 1):
        y = gy1 - (j + 0.5) / ppm
        xs = sorted(p[0] + (y - p[1]) * (q[0] - p[0]) / (q[1] - p[1]) for p, q in E if (p[1] > y) != (q[1] > y))
        b = j * W
        for a_ in range(0, len(xs) - 1, 2):
            i0, i1 = max(0, int(round((xs[a_] - gx0) * ppm))), min(W, int(round((xs[a_ + 1] - gx0) * ppm)))
            if i1 > i0:
                g[b + i0:b + i1] = bytes([val]) * (i1 - i0)


def dilate(g, W, H, r):
    """binary dilation by a (2r+1) square (two running sums)"""
    t = bytearray(W * H)
    for j in range(H):
        c = [0]
        for v in g[j * W:(j + 1) * W]:
            c.append(c[-1] + (1 if v else 0))
        for i in range(W):
            if c[min(W, i + r + 1)] - c[max(0, i - r)]:
                t[j * W + i] = 1
    o = bytearray(W * H)
    for i in range(W):
        c = [0]
        for j in range(H):
            c.append(c[-1] + t[j * W + i])
        for j in range(H):
            if c[min(H, j + r + 1)] - c[max(0, j - r)]:
                o[j * W + i] = 1
    return o


def erode(g, W, H, r):
    inv = bytearray(0 if v else 1 for v in g)
    return bytearray(0 if v else 1 for v in dilate(inv, W, H, r))


def soft_grid(vals, W, H, gx0, gy1, ppm, colour, layer, clip):
    """a byte grid of opacities (row 0 at the top) as a Basemap-writer "soft" item"""
    return ("soft", zlib.compress(bytes(vals), 9), W, H, gx0, gy1 - H / ppm, W / ppm, H / ppm, colour, None, layer, clip)


def cen_of(R):
    return (sum(p[0] for p in R) / len(R), sum(p[1] for p in R) / len(R))


def node_mask(M, T, k, C, frame, log, nk):
    """v2.4 (Aras 16:19 UTC "mark the areas properly"): the node's area follows its blocks: every building and ground
    area whose middle lies in the node frame, closed over the streets between them (CLOSE_M, then back ERODE_M), plus
    the stream inside the frame; cut to the map (site_alan). Returns (grid, W, H, gx0, gy1)"""
    R = [T(p) for p in frame]
    gx0, gy0 = max(M.box[0], min(p[0] for p in R) - 4.0), max(M.box[1], min(p[1] for p in R) - 4.0)
    gx1, gy1 = min(M.box[2], max(p[0] for p in R) + 4.0), min(M.box[3], max(p[1] for p in R) + 4.0)
    W, H = max(1, int(math.ceil((gx1 - gx0) * MASK_PPM))), max(1, int(math.ceil((gy1 - gy0) * MASK_PPM)))
    gx1, gy0 = gx0 + W / MASK_PPM, gy1 - H / MASK_PPM
    xs, ys = [p[0] for p in frame], [p[1] for p in frame]
    fb = (min(xs), min(ys), max(xs), max(ys))
    infr = lambda c: fb[0] <= c[0] <= fb[2] and fb[1] <= c[1] <= fb[3] and pip(c[0], c[1], frame)
    g = bytearray(W * H)
    nb = na = 0
    for Rb, fab_, com, src, nm in C["bld"]:
        if len(Rb) >= 3 and infr(cen_of(Rb)):
            fill_ring(g, W, H, gx0, gy1, MASK_PPM, [T(p) for p in Rb], 1)
            nb += 1
    for A in C.get("areas") or []:
        if A[1] not in ("landuse", "farm", "wood") and len(A[0]) >= 3 and infr(cen_of(A[0])):
            fill_ring(g, W, H, gx0, gy1, MASK_PPM, [T(p) for p in A[0]], 1)
            na += 1
    r1, r2 = max(1, int(round(CLOSE_M * k * MASK_PPM))), max(1, int(round(ERODE_M * k * MASK_PPM)))
    g = erode(dilate(g, W, H, r1), W, H, r2)
    rv, fm = bytearray(W * H), bytearray(W * H)
    for Rr in (C.get("polys") or {}).get("river", []):
        fill_ring(rv, W, H, gx0, gy1, MASK_PPM, [T(p) for p in Rr], 1)
    fill_ring(fm, W, H, gx0, gy1, MASK_PPM, R, 1)
    for i in range(W * H):
        if rv[i] and fm[i]:
            g[i] = 1
    log.append(u"%s area: %d buildings + %d ground areas in its frame, closed over %.0f m, back %.0f m, + the stream "
               u"in the frame; %.0f %% of the frame's own surface" % (nk, nb, na, CLOSE_M, ERODE_M,
                                                                     100.0 * sum(1 for i in range(W * H) if g[i] and fm[i]) / max(1, sum(fm))))
    return g, W, H, gx0, gy1


def read_mahalle(lib, log):
    """the neighbourhoods (mahalle = OpenStreetMap administrative boundaries, admin_level 8) of the kit's OSM file:
    [(name, [survey rings])]; a ring the file cuts off is closed straight (logged)"""
    import xml.etree.ElementTree as ET
    src = os.path.join(BERGAMA_ROOT, "Data", "bergama_osm.osm")
    if not os.path.isfile(src):
        log.append(u"FLAG: %s missing: no neighbourhoods" % src)
        return []
    nodes, ways, rels = {}, {}, []
    for ev, el in ET.iterparse(src, events=("end",)):
        if el.tag == "node":
            try:
                nodes[el.get("id")] = (float(el.get("lon")), float(el.get("lat")))
            except (TypeError, ValueError):
                pass
            el.clear()
        elif el.tag == "way":
            ways[el.get("id")] = [n.get("ref") for n in el.findall("nd")]
            el.clear()
        elif el.tag == "relation":
            tg = dict((t.get("k"), t.get("v")) for t in el.findall("tag"))
            if tg.get("boundary") == "administrative" and tg.get("admin_level") == "8" and tg.get("name"):
                rels.append((tg["name"], [m.get("ref") for m in el.findall("member")
                                          if m.get("type") == "way" and m.get("role") in ("outer", "", None)]))
            el.clear()
    to_s = lib["to_survey"]
    out = []
    for name, wids in rels:
        left = [[r for r in ways[w] if r in nodes] for w in wids if w in ways]
        left = [w for w in left if len(w) >= 2]
        rings = []
        while left:
            cur = left.pop(0)
            grown = True
            while cur[0] != cur[-1] and grown:
                grown = False
                for i, w in enumerate(left):
                    if w[0] == cur[-1]:
                        cur = cur + w[1:]
                    elif w[-1] == cur[-1]:
                        cur = cur + w[::-1][1:]
                    elif w[-1] == cur[0]:
                        cur = w[:-1] + cur
                    elif w[0] == cur[0]:
                        cur = w[::-1][:-1] + cur
                    else:
                        continue
                    left.pop(i)
                    grown = True
                    break
            P = [to_s(*nodes[r]) for r in cur]
            if cur[0] != cur[-1]:
                log.append(u"neighbourhood %s: a ring cut by the file's edge closed straight across %.0f m" % (
                    name, math.hypot(P[0][0] - P[-1][0], P[0][1] - P[-1][1])))
            else:
                P = P[:-1]
            if len(P) >= 3:
                rings.append(P)
        if rings:
            out.append((name, rings))
    log.append(u"neighbourhoods (OpenStreetMap admin_level 8): %d read" % len(out))
    return out


# ================================================================ v2.8: the diagram standard (library/diagram_style/DIAGRAM_STYLE.md v1)
# local copies with the standard's pc_dg_* signatures (pages_common has none yet); switch to G["pc_dg_*"] when they land
DGS = dict(ground="D9D4CA", accent="C07A2E", water="A2B6B5", ink="2B2B2B", grey="8E897F", tint="F0DEC9")
LW_CUT, LW_MOVE, LW_CTX, LW_HAIR = 0.70, 0.45, 0.18, 0.10


def dg_ground(G, pts, base_y):
    """the 0.70 cut line + the D9D4CA poché down to base_y"""
    R = list(pts) + [(pts[-1][0], base_y), (pts[0][0], base_y)]
    return [G["P_"]([R], DGS["ground"], None, 0.0, "cards"), G["L_"](pts, DGS["ink"], LW_CUT, "cards")]


def dg_city(G, x0, x1, y, step, seed=0, toward=1):
    """one rhythm row of small blocks on the ground line y, shrinking toward the far edge (toward=1: right, -1: left)"""
    it, n = [], max(1, int((x1 - x0) / step))
    hs = (1.6, 2.2, 1.8, 2.5, 1.9)
    for i in range(n):
        f = (i / float(max(1, n - 1))) if toward > 0 else (1.0 - i / float(max(1, n - 1)))
        sc = 1.0 - 0.45 * f
        w_, h_ = step * 0.62 * sc, hs[(i + seed) % len(hs)] * sc
        xa = x0 + i * step + (step - w_) / 2.0
        it.append(G["P_"]([[(xa, y), (xa + w_, y), (xa + w_, y + h_), (xa, y + h_)]], "FFFFFF", DGS["grey"], LW_CTX, "cards"))
    return it


def dg_water(G, R):
    return [G["P_"]([R], DGS["water"], None, 0.0, "cards")]


def dg_arrow(G, a, b, kind):
    """a short 0.45 arrow with a solid head: people accent, water blue, bus grey"""
    col = {"people": DGS["accent"], "water": "5C7A86", "bus": DGS["grey"]}[kind]
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L
    hl, hw = 1.4, 0.7
    c = (b[0] - ux * hl, b[1] - uy * hl)
    return [G["L_"]([a, c], col, LW_MOVE, "cards"),
            G["P_"]([[b, (c[0] - uy * hw, c[1] + ux * hw), (c[0] + uy * hw, c[1] - ux * hw)]], col, None, 0.0, "cards")]


def dg_person(G, x, y):
    """one 2.4 mm standing figure, feet at (x, y)"""
    L_, P_, circle = G["L_"], G["P_"], G["circle"]
    return [P_([circle(x, y + 2.05, 0.33, 12)], DGS["ink"], None, 0.0, "cards"),
            L_([(x, y + 1.7), (x, y + 0.85)], DGS["ink"], 0.3, "cards"),
            L_([(x - 0.35, y), (x, y + 0.85), (x + 0.35, y)], DGS["ink"], 0.25, "cards"),
            L_([(x - 0.45, y + 1.0), (x, y + 1.5), (x + 0.45, y + 1.0)], DGS["ink"], 0.2, "cards")]


def dg_bracket(G, x0, x1, y, name):
    """the hairline bracket under the ground with its name beneath ("the agora" way)"""
    L_, T_ = G["L_"], G["T_"]
    return [L_([(x0, y + 0.8), (x0, y), (x1, y), (x1, y + 0.8)], DGS["ink"], LW_HAIR, "cards"),
            T_(name.upper(), (x0 + x1) / 2.0, y - 2.1, 1.7, DGS["ink"], "cards", True, "C")]


def dg_road(G, x, y, h):
    """the driver pictogram: dense vertical hatching (the bus road)"""
    return [G["L_"]([(x + i * 0.35, y), (x + i * 0.35, y + h * (0.75 + 0.25 * ((i * 7) % 4) / 3.0))], DGS["grey"],
                    LW_CTX, "cards") for i in range(8)]


def dg_label(G, x, y, s, accent=False, al="C"):
    return [G["T_"](s.upper(), x, y, 1.7, DGS["accent"] if accent else DGS["ink"], "cards", True, al)]


def dg_monument(G, x, y, h):
    """heritage silhouette: an arch block in grey outline (the loop stop driver)"""
    w = h * 0.8
    r = w * 0.22
    arch = [(x + w / 2 - r, y)] + [(x + w / 2 + r * math.cos(math.pi - math.pi * i / 10.0), y + h * 0.45 + r * math.sin(math.pi * i / 10.0))
                                   for i in range(11)] + [(x + w / 2 + r, y)]
    return [G["P_"]([[(x, y), (x + w, y), (x + w, y + h), (x, y + h)]], "FFFFFF", DGS["grey"], LW_CTX, "cards"),
            G["L_"](arch, DGS["grey"], LW_CTX, "cards")]


def node_strip(G, nk, info, x, ytop, w):
    """v2.8 "What meets here" to the diagram standard: one long low cut across the stream; the ground the one heavy
    line (poché under it), the stream in the middle; context a rhythm of blocks on both banks; the drivers at the edges
    (bus road left, heritage loop monument right, both grey); the move in the one accent (the hub: steps into the bed /
    a square over the culvert; N4's raised point); people only on the move; at most 4 labels. Returns (items, height)"""
    hb = info["hubs"]
    kind = info["hub_kind"]
    H_ = 24.0
    yg = ytop - 13.0                                     # air above the ground: 13 of 24 mm
    base = ytop - H_ + 4.5
    xm = x + w * 0.5
    it = []
    labels = 0
    # ---- the ground, cut across the stream
    if kind == "walk":                                   # steps down into the bed on the near bank
        prof = [(x, yg), (xm - 9.0, yg), (xm - 9.0, yg - 1.0), (xm - 7.5, yg - 1.0), (xm - 7.5, yg - 2.1),
                (xm - 6.0, yg - 2.1), (xm - 6.0, yg - 3.2), (xm + 5.0, yg - 3.2), (xm + 7.0, yg), (x + w, yg)]
        wat = [(xm - 6.0, yg - 1.6), (xm + 6.0, yg - 1.6), (xm + 5.0, yg - 3.2), (xm - 6.0, yg - 3.2)]
    else:
        prof = [(x, yg), (xm - 7.0, yg), (xm - 5.0, yg - 3.2), (xm + 5.0, yg - 3.2), (xm + 7.0, yg), (x + w, yg)]
        wat = [(xm - 6.0, yg - 1.6), (xm + 6.0, yg - 1.6), (xm + 5.0, yg - 3.2), (xm - 5.0, yg - 3.2)]
    it += dg_water(G, wat)
    it += dg_ground(G, prof, base)
    # ---- context: one rhythm row on each bank (grey), shrinking toward the edges
    it += dg_city(G, x + 5.0, xm - 11.0, yg, 2.6, 0, -1)
    it += dg_city(G, xm + 8.5, x + w - 5.5, yg, 2.6, 2, 1)
    # ---- drivers at the edges (grey)
    if info["bus"]:
        it += dg_road(G, x + 0.4, yg, 6.0)
        it += dg_arrow(G, (x + 3.6, yg + 4.2), (x + 9.0, yg + 4.2), "bus")
        it += dg_label(G, x + 0.4, yg + 7.6, u"%d bus lines" % info["bus"], False, "L")
        labels += 1
    if info["loop"]:
        it += dg_monument(G, x + w - 4.2, yg, 4.6)
        it += dg_label(G, x + w, yg + 6.4, u"loop stop " + u" ".join(str(n_) for n_, nm in info["loop"]), False, "R")
        labels += 1
    # ---- the move (the one accent) + people on it
    A = DGS["accent"]
    if kind == "walk":
        st = [(xm - 9.0, yg), (xm - 9.0, yg - 1.0), (xm - 7.5, yg - 1.0), (xm - 7.5, yg - 2.1), (xm - 6.0, yg - 2.1),
              (xm - 6.0, yg - 3.2)]
        it.append(G["L_"](st, A, LW_CUT + 0.25, "cards"))
        it += [G["P_"]([[(xm - 13.0, yg), (xm - 9.0, yg), (xm - 9.0, yg + 0.6), (xm - 13.0, yg + 0.6)]], A, None, 0.0, "cards")]
        it += dg_person(G, xm - 8.3, yg - 1.0) + dg_person(G, xm - 11.5, yg + 0.6)
        it += dg_arrow(G, (xm - 12.0, yg + 3.4), (xm - 7.2, yg + 0.6), "people")
        mx = xm - 9.0
    elif kind == "hidden":
        it.append(G["P_"]([[(xm - 8.0, yg), (xm + 8.0, yg), (xm + 8.0, yg + 0.7), (xm - 8.0, yg + 0.7)]], A, A, LW_MOVE, "cards"))
        it.append(G["L_"]([(xm - 5.0, yg + 0.75), (xm + 5.0, yg + 0.75)], "5C7A86", LW_CTX, "cards"))
        it += dg_person(G, xm - 3.0, yg + 0.7) + dg_person(G, xm + 2.2, yg + 0.7)
        if nk == "N4" and nk in IDEAS:                   # the raised gathering point (Aras's mark), on thin stems
            it.append(G["P_"]([[(xm + 3.5, yg + 5.2), (xm + 10.5, yg + 5.2), (xm + 10.5, yg + 5.8), (xm + 3.5, yg + 5.8)]],
                              A, None, 0.0, "cards"))
            it += [G["L_"]([(xm + 4.5, yg + 0.7), (xm + 4.5, yg + 5.2)], A, LW_CTX, "cards"),
                   G["L_"]([(xm + 9.5, yg + 0.7), (xm + 9.5, yg + 5.2)], A, LW_CTX, "cards")]
            it += dg_person(G, xm + 7.0, yg + 5.8)
        mx = xm
    elif kind == "gateway":
        it += dg_arrow(G, (xm + 2.0, yg + 3.0), (x + w - 7.0, yg + 3.0), "people")
        mx = xm
    else:
        it.append(G["L_"]([(xm - 13.0, yg + 0.1), (xm - 7.0, yg + 0.1), (xm - 7.0, yg + 3.0), (xm - 13.0, yg + 3.0),
                           (xm - 13.0, yg + 0.1)], DGS["grey"], LW_CTX, "cards", (0.8, 0.6)))
        mx = xm - 10.0
    if hb:
        word = (KEYS.get(kind) or [(u"", True)])[0][0]
        s_ = u"%s %s" % (u" · ".join(c for c, k_ in hb), word)
        tw_ = len(s_) * 1.7 * 0.62
        lx = min(max(mx, x + tw_ / 2.0 + 10.0), x + w - tw_ / 2.0 - 1.0)
        it += dg_label(G, lx, yg + (8.6 if kind == "hidden" and nk == "N4" else 4.6), s_, True)
    else:
        it += dg_label(G, mx, yg + 4.0, u"no hub", False)
    labels += 1
    # ---- the shops: a bracket under the ground of the far bank
    if info["shops"] and labels < 4:
        it += dg_bracket(G, xm + 8.0, x + w - 5.0, base - 0.6, u"%d shop buildings" % info["shops"])
    return it, H_ + 1.0


def strip_claim(nk, info):
    """the title: one claim, from what is there and what is missing"""
    have = [w_ for w_, v in ((u"a hub", info["hubs"]), (u"buses", info["bus"]), (u"the loop", info["loop"]),
                             (u"shops", info["shops"])) if v]
    miss = [w_ for w_, v in ((u"hub", info["hubs"]), (u"buses", info["bus"]), (u"loop", info["loop"]),
                             (u"shops", info["shops"])) if not v]
    if not have:
        return u"NOTHING MEETS HERE YET"
    a = (u", ".join(have[:-1]) + u" and " + have[-1]) if len(have) > 1 else have[0]
    return (a + u" meet" + (u"s" if len(have) == 1 else u"") + (u" · no " + u", no ".join(miss) if miss else u"")).upper()


def node_card(G, lib, K, nk, nd, info, x, ytop, w, hfix=None, dh=38.0, X=None):
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
    # ---- what meets here (v2.8): one cut to the diagram standard, its claim as the title, the hub keys as text
    for ln in wrap(u"WHAT MEETS HERE · " + strip_claim(nk, info), 2.6, wi, tw, True):
        it.append(T_(ln, xi, y - 2.0, 2.6, INK, "cards", True))
        y -= 2.6 * 1.3
    y -= 2.0
    si, sh = node_strip(G, nk, info, xi, y, wi)
    it += si
    y -= sh + 1.0
    if info["hub_kind"]:
        for j, (s_, b_) in enumerate(KEYS[info["hub_kind"]]):
            y = para(s_, y, 2.2, INK, b_)
        y -= 2.0
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
    # ---- the map = site_alan (v2.4: pages_common SiteMap), across the top, scale to a 1:500 step
    mpns, MPC = G["pc_mp_data"](log)
    M = G["pc_site_map"](10000, log)
    mw_max = PAGE_W - 2 * MARGIN - 8.0 - SIDE_W
    den = int(math.ceil(M.F.w / mw_max * 1000.0 / DEN_STEP) * DEN_STEP)
    k = 1000.0 / den
    M.den, M.k = float(den), k
    M.mw, M.mh = M.F.w * k, M.F.h * k
    M.x0, M.y0 = MARGIN, PAGE_H - MARGIN - M.mh
    M.w, M.h = PAGE_W, PAGE_H
    M.box = (M.x0, M.y0, M.x0 + M.mw, M.y0 + M.mh)
    T = M.T
    log.append(u"map = site_alan %.0f x %.0f m at 1:%d = %.0f x %.0f mm" % (M.F.w, M.F.h, den, M.mw, M.mh))
    if T(cen[nks[0]])[0] > T(cen[nks[-1]])[0]:
        log.append(u"FLAG: %s sits right of %s on the map" % (nks[0], nks[-1]))

    # ---- what each node holds (calculated)
    ns, C = G["pc_mb_data"](log)
    shops = [(sum(p[0] for p in R) / len(R), sum(p[1] for p in R) / len(R)) for R, fab_, com, src, nm in C["bld"] if com]
    lines_of = G["pc_stop_lines"](D)
    info = {}
    for nk in nks:
        R = NODES[nk]["corners"]
        inn = lambda xy: pip(xy[0], xy[1], R) and M.inside(T(xy))     # v2.7: in the node frame and in site_alan
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
    # ---- the neighbourhoods (mahalle) and their main fabric (calculated: MapBase buildings in site_alan)
    MAH = read_mahalle(lib, log)
    bld_in = [(cen_of(Rb), fab_) for Rb, fab_, com, src, nm in C["bld"] if len(Rb) >= 3 and M.inside(T(cen_of(Rb)))]
    words = ns.get("FAB_WORDS") or {}
    char = {}
    for name, rings in MAH:
        bb = [(min(p[0] for p in R_), min(p[1] for p in R_), max(p[0] for p in R_), max(p[1] for p in R_)) for R_ in rings]
        cnt_ = {}
        pts_ = []
        for c_, fab_ in bld_in:
            if any(b[0] <= c_[0] <= b[2] and b[1] <= c_[1] <= b[3] and pip(c_[0], c_[1], R_) for b, R_ in zip(bb, rings)):
                cnt_[fab_] = cnt_.get(fab_, 0) + 1
                pts_.append(c_)
        tot = sum(cnt_.values())
        if not tot:
            continue
        main_ = max((f_ for f_ in cnt_ if f_ != "construction"), key=lambda f_: cnt_[f_], default=None)
        char[name] = dict(fab=main_, n=tot, share=100.0 * cnt_.get(main_, 0) / tot, pts=pts_, rings=rings)
        log.append(u"neighbourhood %s: %d buildings in site_alan; main fabric %s %.0f %% (%s)" % (
            name, tot, main_, char[name]["share"], u", ".join(u"%s %d" % kv for kv in sorted(cnt_.items()))))
    for name, c_ in char.items():                        # the boundaries, dashed, cut to the map
        for R_ in c_["rings"]:
            items.append(("line", [T(p) for p in R_ + [R_[0]]], MAH_C, 0.3, "map", "neighbourhoods", (1.4, 0.8)))
    used_char = []
    for nk in nks:                                       # the node areas: their blocks, semi-transparent, edged
        g, W, Hh, gx0, gy1 = node_mask(M, T, k, C, NODES[nk]["corners"], log, nk)
        inv = bytearray(0 if v else 1 for v in g)
        edge = bytearray(1 if (g[i] and v) else 0 for i, v in enumerate(dilate(inv, W, Hh, 1)))
        colr = NODE_COL.get(nk, NODE_C)
        a_in, a_ed = int(round(255 * NODE_ALPHA)), int(round(255 * EDGE_ALPHA))
        lbl = bytearray(W * Hh)
        parts = []
        if nk in NEIGH_NODES:                            # a neighbourhood node: each part in its neighbourhood's colour
            for name, c_ in char.items():
                if c_["n"] < MIN_BLD or c_["fab"] not in CHAR_COL:
                    continue
                parts.append(name)
                for R_ in c_["rings"]:
                    fill_ring(lbl, W, Hh, gx0, gy1, MASK_PPM, [T(p) for p in R_], len(parts))
        for j, name in enumerate(parts):
            vals = bytearray(a_in if (g[i] and not edge[i] and lbl[i] == j + 1) else 0 for i in range(W * Hh))
            if any(vals):
                items.append(soft_grid(vals, W, Hh, gx0, gy1, MASK_PPM, CHAR_COL[char[name]["fab"]], "node_areas", "map"))
                used_char.append(char[name]["fab"])
                log.append(u"%s part in %s: coloured as %s" % (nk, name, char[name]["fab"]))
        vals = bytearray(a_ed if edge[i] else (a_in if (g[i] and not (parts and lbl[i])) else 0) for i in range(W * Hh))
        items.append(soft_grid(vals, W, Hh, gx0, gy1, MASK_PPM, colr, "node_areas", "map"))
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
    for name, c_ in sorted(char.items()):                # the neighbourhoods' names with their main fabric
        q_ = [T(p) for p in c_["pts"]]
        if c_["n"] >= MIN_BLD and q_:
            q = (sum(p[0] for p in q_) / len(q_), sum(p[1] for p in q_) / len(q_))
            nm_ = name.replace(u" Mahallesi", u"")
            lab.put(u"%s: %s" % (nm_, (words.get(c_["fab"]) or c_["fab"] or u"").lower()), q, 2.0, MAH_C,
                    "neighbourhood_names", False)
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

    # ---- the legend: a band under the map (v2.4: the map strip is site_alan, too low for a column legend)
    sq = lambda f_, s__=3.0: (lambda xx, yy: [P_([[(xx - s__ / 2, yy - s__ / 2), (xx + s__ / 2, yy - s__ / 2),
                                                 (xx + s__ / 2, yy + s__ / 2), (xx - s__ / 2, yy + s__ / 2)]],
                                               f_, "FFFFFF", 0.25, "legend")])
    box_ = lambda xx, yy: [(xx - 4.5, yy - 1.8), (xx + 4.5, yy - 1.8), (xx + 4.5, yy + 1.8), (xx - 4.5, yy + 1.8)]
    rows = [(lambda xx, yy: [soft_poly(box_(xx, yy), NODE_COL["N2"], NODE_ALPHA, "legend", None),
                             P_([box_(xx, yy)], None, NODE_COL["N2"], 0.25, "legend")],
             u"node area: its blocks and stream")]
    for f_ in [f_ for f_ in CHAR_COL if f_ in used_char]:
        rows.append(((lambda c__: lambda xx, yy: [soft_poly(box_(xx, yy), c__, NODE_ALPHA, "legend", None)])(CHAR_COL[f_]),
                     u"neighbourhood node, part mostly %s" % (words.get(f_) or f_).lower()))
    rows += [(lambda xx, yy: [L_([(xx - 4.5, yy), (xx + 4.5, yy)], MAH_C, 0.3, "legend", (1.4, 0.8))],
              u"neighbourhood (mahalle) boundary: name, main fabric"),
             (lambda xx, yy: [P_([circle(xx, yy, 1.5, 20)], "FFFFFF", PLACE_C, 0.35, "legend")],
              u"the project's places, numbered as on the cards"),
             (sq(K["hub"]["walk"]), u"walking hub"), (sq(K["hub"]["transit"]), u"main transit hub"),
             (sq(K["hub"]["gateway"]), u"gateway out of town"),
             (lambda xx, yy: [P_([circle(xx, yy, 1.6, 20)], K["heritage"], "FFFFFF", 0.25, "legend")],
              u"heritage loop stop (cards)")]
    for txt, pres in MP_ROWS:                            # masterplan rows, in the colours the map uses
        sw = mp_swatch(mpns, MPC, pres) if any(any(c_ == p_ or c_.startswith(p_ + "/") for p_ in pres)
                                               for c_ in cnt) else None
        if not sw:
            log.append(u"legend: %s not on the map, no row" % txt)
            continue
        if sw[0] == "line":
            rows.append(((lambda c__: lambda xx, yy: [L_([(xx - 4.5, yy), (xx + 4.5, yy)], c__, 0.6, "legend")])(sw[1]),
                         txt))
        else:
            rows.append(((lambda f__, s__: lambda xx, yy: [P_([box_(xx, yy)], f__, s__, 0.2 if s__ else 0.0, "legend")])(
                sw[1], sw[2]), txt))
    ncol = 5
    nrow = int(math.ceil(len(rows) / float(ncol)))
    colw, rh, ls = (PAGE_W - 2 * MARGIN) / ncol, 4.6, tm["legend"] - 0.2
    yl = M.box[1] - 5.0
    for i, (draw, txt) in enumerate(rows):
        xx, yy = MARGIN + (i // nrow) * colw, yl - (i % nrow) * rh
        items += draw(xx + 5.0, yy)
        lns = wrap(txt, ls, colw - 16.0, tw)
        if len(lns) > 1:
            log.append(u"FLAG: legend row too long for its column: %s" % txt)
        items.append(T_(lns[0], xx + 12.0, yy - ls * 0.38, ls, INK, "legend"))
    ylb = yl - nrow * rh

    # ---- the node cards under the legend
    X = dict(M=M, C=C, D=D, H=H, mpns=mpns, MPC=MPC, clips={}, mp_layers=set(p for _, ps in MP_ROWS for p in ps))
    yt = ylb - 6.0
    items.append(T_(u"THE SIX NODES: WHAT MEETS AT EACH, WHAT IS MISSING", MARGIN, yt + 3.0, tm["sub"], INK, "cards", True))
    cw = (PAGE_W - 2 * MARGIN - (len(nks) - 1) * CARD_GAP) / len(nks)
    hc = max(node_card(G, lib, K, nk, NODES[nk], info[nk], 0.0, 0.0, cw, None, 38.0, X)[1] for nk in nks)
    room = yt - MARGIN
    dh = 38.0 + max(0.0, min(40.0, room - hc - 2.0))     # the spare height goes to the plans
    hc = max(node_card(G, lib, K, nk, NODES[nk], info[nk], 0.0, 0.0, cw, None, dh, X)[1] for nk in nks)
    if hc > room + 0.1:
        log.append(u"FLAG: the node cards need %.0f mm, the page gives %.0f mm under the legend" % (hc, room))
    hc = max(hc, room)                                   # the cards reach the page margin
    for i, nk in enumerate(nks):
        items += node_card(G, lib, K, nk, NODES[nk], info[nk], MARGIN + i * (cw + CARD_GAP), yt, cw, hc, dh, X)[0]
    log.append(u"cards: %.0f mm high, plans %.0f mm" % (hc, dh))

    # ---- the side column: title, north, scale
    x = M.box[2] + 8.0
    y = M.box[3] - tm["title"]
    for ln in wrap(u"THE SIX NODES ALONG THE SPINE", tm["title"], SIDE_W, tw, True):
        items.append(T_(ln, x, y, tm["title"], INK, "title", True))
        y -= tm["title"] * 1.25
    for ln in wrap(u"Where the town meets the stream, node by node", tm["sub"], SIDE_W, tw):
        items.append(T_(ln, x, y, tm["sub"], INK, "title"))
        y -= tm["sub"] * 1.4
    yb = M.box[1] + 4.0
    if y < yb + 14.0:
        log.append(u"FLAG: the title reaches the north arrow (%.1f mm)" % (y - yb - 14.0))
    items += G["pc_north_items"](x + 5.5, yb + 5.0, 4.5, M.north, INK)
    bar = 250.0 if den <= 12000 else 500.0
    Lb, xb = bar * k, x + 16.0
    for i in range(4):
        items.append(P_([[(xb + Lb * i / 4, yb), (xb + Lb * (i + 1) / 4, yb), (xb + Lb * (i + 1) / 4, yb + 1.2),
                          (xb + Lb * i / 4, yb + 1.2)]], INK if i % 2 == 0 else "FFFFFF", INK, 0.15, "north_scale"))
    items.append(T_(u"0", xb, yb - 2.8, 2.0, INK, "north_scale", False, "C"))
    items.append(T_(u"%d m" % bar, xb + Lb, yb - 2.8, 2.0, INK, "north_scale", False, "C"))
    items.append(T_(u"1:%s" % format(den, ",d"), xb, yb + 3.0, 2.8, INK, "north_scale", True))

    log.append(u"sources (log only): " + D["sources"]["osm"] + u"; hubs, places, hub sections: CityLink v13 "
               u"(SUBMISSION_SON p9); neighbourhoods: OpenStreetMap admin_level 8 (Data/bergama_osm.osm), main fabric = the most common MapBase fabric type of the buildings in site_alan; proposal: MasterplanBase (B19_setB_layers259.svg); context: MapBase; nodes: Data/section_lines.json; ideas N2, N4: Aras 14 Nov")
    orig = G["pc_frame_check"]                           # the cards and the column sit outside the map frame by design
    G["pc_frame_check"] = lambda its, box, lg, tw_=None: orig(its, box, lg, tw_, skip=G["PC_SHEET_LAYERS"] + (
        "cards", "node_pointers"))
    clips = {"map": [[[(M.box[0], M.box[1]), (M.box[2], M.box[1]), (M.box[2], M.box[3]), (M.box[0], M.box[3])]]]}
    clips.update(X["clips"])
    paths = G["pc_write"](lib, M, items, OUT_DIR, NAME, u"The six nodes along the spine", log, None, clips)
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
