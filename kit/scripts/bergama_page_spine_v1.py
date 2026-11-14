# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE SPINE v1 (14 Nov 2026), Panel Review II slide 2: the streamside spine hub by hub, with the
six nodes N1-N6 and the shops (output/presentation/2.pdf; one script per page, Aras 14 Nov 10:46 UTC).

Aras 14 Nov 12:50 UTC: "for slide 2 page 9-10 are the same things. so we gonna include page 9 without the bottom part
of the page ... and page 8 can be combined into it"; 12:50: "we dont need this part" (page 8's street sections R1-R4).
So: SUBMISSION_SON p9 "The streamside spine, hub by hub" (CityLink v13 spine map + hub cards) WITHOUT its bottom band
(flood rule, which bank the spine takes, producers' market), with p8's message "the stream joins the town where the
shops already are" folded into the same map (the shop buildings) and into each card (shops near the hub). p10 dropped.

Drawn from the one MapBase (pages_common pc_mapbase, nothing redrawn), shop buildings = MapBase's own "com" flag
(buildings holding an OSM shop / office / craft place) in ochre. Over it: the node frames N1-N6 (Data/section_lines.json,
the frames of slides 7-12), the streamside spine K4 -> K5 along the Selinos centreline (as slide 5), the hub tiles and
the hubs' bus stops (Data/bergama_access_heritage.json, as slide 5), the project's places 1-6 (CityLink v13 FUNCS).
Under the map one card per hub (CityLink v13 HUBS / hub_card, texts kept): role, bus stops with lines and straight-line
metres (calculated), trips (ESHOT), the hub's levels as a small section with its keys, the node it sits in
(calculated), shop buildings within SHOP_R m (calculated from MapBase), its places.

Outputs (Downloads/Bergama/output/bergama_page_spine/): Spine.pdf, Spine.svg, review/ PNGs; copy presentation/2.pdf.
Reads: Data/bergama_pages_common.py, Data/bergama_access_heritage.json, Data/section_lines.json,
Data/selinos_centreline.json, cached MapBase (press MapBase first), newest scripts/bergama_basemap_v*.py (writer).
Grasshopper: a Button on any input runs it; input `scale` (default 1:4,000).
"""
import os, time, math

VERSION = "v1"
SLIDE = 2
GH_LABEL = "PageSpine"
OUT_FOLDER = "bergama_page_spine"
LOG_NAME = "bergama_page_spine_log.txt"
GH_INPUTS = {"scale": "int 1000..10000 = 4000"}
COMMON = os.path.join("Data", "bergama_pages_common.py")
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
NAME = "Spine"
DEN = 4000
WIN_PAD_M = 60.0                     # m of town round the node frames and hubs (a drawing rule)
SHOP_R = 100.0                       # m: shop buildings counted round a hub point (centroid distance, calculated)
SHOP_C = "D99A45"                    # ochre: buildings with shops (p8's shop streets were ochre)
CARD_GAP, CARD_PAD = 4.0, 2.4        # mm
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


def card(G, lib, K, hb, info, x, ytop, w):
    """one hub card (CityLink v13 hub_card, boxed): returns (items, height mm)"""
    P_, L_, T_, circle, wrap = G["P_"], G["L_"], G["T_"], G["circle"], G["wrap"]
    tw = lib["text_w"]
    INK = K["ink"]
    it = []
    kd = "transit" if hb["kind"] == "hidden" else hb["kind"]
    col = K["hub"][kd]
    xi, wi = x + CARD_PAD, w - 2 * CARD_PAD

    def para(s, y, size, c=INK, bold=False, xx=None, ww=None):
        xx = xi if xx is None else xx
        for ln in wrap(s, size, ww or wi, tw, bold):
            it.append(T_(ln, xx, y - size * 0.75, size, c, "cards", bold))
            y -= size * 1.32
        return y
    y = ytop - 2.0 - CARD_PAD                                # under the coloured bar
    tile = (8.0, 5.6)
    it.append(P_([[(xi, y - tile[1]), (xi + tile[0], y - tile[1]), (xi + tile[0], y), (xi, y)]], col, None, 0.0, "cards"))
    it.append(T_(hb["code"], xi + tile[0] / 2, y - tile[1] + 1.5, 3.0, "FFFFFF", "cards", True, "C"))
    y2 = para(info["name"], y - 0.6, 3.3, INK, True, xi + tile[0] + 2.0, wi - tile[0] - 2.0)
    y = min(y - tile[1], y2) - 1.6
    y = para(WORD[kd] + u" · " + hb["role"], y, 2.5, col if kd == "transit" else GLY["ink2"], kd == "transit") - 1.0
    for nm, lines, m in info["stops"]:                       # bus stop: name ... metres; lines under it
        it.append(P_([circle(xi + 1.1, y - 1.1, 1.0, 20)], "FFFFFF", INK, 0.3, "cards"))
        ms = u"%d m" % m
        it.append(T_(ms, xi + wi, y - 1.9, 2.5, K["spine"], "cards", True, "R"))
        y_ = para(nm, y, 2.5, INK, True, xi + 3.4, wi - 3.4 - tw(ms, 2.5, True) - 2.0)
        y = para(u"lines " + lines, y_, 2.2, GLY["ink2"], False, xi + 3.4, wi - 3.4) - 0.6
    if hb.get("later"):
        y = para(hb["later"], y, 2.3, K["spine"], True, xi + 3.4, wi - 3.4)
    y = para(hb["trips"], y, 2.3, GLY["ink2"], False, xi + 3.4, wi - 3.4) - 2.0
    gw = min(42.0, wi * 0.45)                                # the levels glyph + its keys
    gh = gw * 15.0 / 24.0
    it += glyph(G, hb["kind"], xi, y, gw, gh)
    ky = y
    for j, (s_, b_) in enumerate(KEYS[hb["kind"]]):
        if j and b_:
            ky -= 0.8
        ky = para(s_, ky, 2.3, INK, b_, xi + gw + 2.5, wi - gw - 2.5)
    y = min(y - gh, ky) - 2.4
    y = para(info["node"], y, 2.5, NODE_C, True) - 0.4    # node + shops (p8 folded in)
    it.append(P_([[(xi, y - 2.4), (xi + 4.0, y - 2.4), (xi + 4.0, y), (xi, y)]], SHOP_C, None, 0.0, "cards"))
    y = para(info["shops"], y, 2.4, INK, False, xi + 5.4, wi - 5.4) - 1.6
    for n in hb["places"]:                                   # the project's places
        f = PLACES[n]
        it.append(P_([circle(xi + 1.8, y - 1.8, 1.8, 24)], "FFFFFF", PLACE_C, 0.35, "cards"))
        it.append(T_(str(n), xi + 1.8, y - 2.6, 2.2, PLACE_C, "cards", True, "C"))
        y = para(f["name"], y - 0.2, 2.6, INK, True, xi + 5.0, wi - 5.0)
        y = para(u"for " + u", ".join(WHO[c] for c in f["who"]) + u" · grows from " +
                 u", ".join(GROWS[c] for c in f["grows"]), y, 2.2, GLY["ink2"], False, xi + 5.0, wi - 5.0)
        kw = f["kw"][0] + u" · " + f["kw"][1]
        if n == 7:                                           # chainage, as CityLink (calculated, about +-30 m)
            kw += u" · about %d m upstream of Ulucami Önü" % int(round((CH["K4"] - f["ch"]) / 10.0) * 10)
        y = para(kw, y, 2.3, INK, False, xi + 5.0, wi - 5.0) - 1.4
    h = ytop - (y - CARD_PAD)
    yb = ytop - h
    frame = [(x, yb), (x + w, yb), (x + w, ytop), (x, ytop)]
    return [P_([[(x, ytop - 2.0), (x + w, ytop - 2.0), (x + w, ytop), (x, ytop)]], col, None, 0.0, "cards"),
            P_([frame], None, "B0AC9C", 0.25, "cards")] + it, h


def main():
    t0 = time.time()
    log = []
    G = load_common()
    lib = G["pc_lib"](log)
    D = G["pc_data"](log)
    K = D["key"]
    import json
    with open(os.path.join(BERGAMA_ROOT, "Data", "section_lines.json"), encoding="utf-8") as f:
        NODES = json.load(f)["nodes"]
    den = int(globals().get("scale") or DEN)
    dist, L_, P_, T_, circle = G["pc_dist"], G["L_"], G["P_"], G["T_"], G["circle"]
    INK, tm = K["ink"], K["text_mm"]
    H = D["hubs"]
    pts = [p for nd in NODES.values() for p in nd["corners"]] + list(H.values())
    win = [min(p[0] for p in pts) - WIN_PAD_M, min(p[1] for p in pts) - WIN_PAD_M,
           max(p[0] for p in pts) + WIN_PAD_M, max(p[1] for p in pts) + WIN_PAD_M]
    M = G["Map"]({"box": win}, den)

    # ---- card texts (live: bus stops and lines from the access data, nodes, shops from MapBase)
    ns, C = G["pc_mb_data"](log)
    shops = []
    for R, fab_, com, src, nm in C["bld"]:
        if com:
            shops.append((sum(p[0] for p in R) / len(R), sum(p[1] for p in R) / len(R)))
    log.append(u"shop buildings (MapBase com flag) in the cache: %d" % len(shops))
    groups = G["pc_stop_groups"](D)
    info = {}
    for hb in HUBS:
        hp = [H[k] for k in hb["pts"]]
        st = []
        for nm in D["hub_stops"][hb["code"]]:
            c = [(min(dist(xy, p) for p in hp), xy, ln) for n_, xy, ln in groups if n_ == nm]
            if c:
                m, xy, ln = min(c, key=lambda t: t[0])
                st.append((nm, u" ".join(sorted(ln, key=lambda r: (len(r), r))), int(round(m))))
            else:
                log.append(u"FLAG: hub %s stop %s not in the access data" % (hb["code"], nm))
        inn = [k for k in sorted(NODES) if any(pip(p[0], p[1], NODES[k]["corners"]) for p in hp)]
        ns_ = sum(1 for s in shops if min(dist(s, p) for p in hp) <= SHOP_R)
        info[hb["code"]] = dict(
            name=D["hub_names"][hb["code"]], stops=st,
            node=(u"in node " + u", ".join(u"%s %s" % (k, NODES[k]["name"]) for k in inn)) if inn else
            u"outside the node frames",
            shops=u"%d buildings with shops within %d m (MapBase, calculated)" % (ns_, SHOP_R))
        log.append(u"card %s: %s; %s; %d shop buildings within %d m" % (hb["code"], u", ".join(
            u"%s %d m" % (a, c_) for a, _b, c_ in st), info[hb["code"]]["node"], ns_, SHOP_R))

    # ---- the cards' band under the map (measured first, then the map is lifted above it)
    cw = (M.w - 2 * M.x0 - 4 * CARD_GAP) / 5.0
    band = max(card(G, lib, K, hb, info[hb["code"]], 0.0, 0.0, cw)[1] for hb in HUBS)
    lift = band + 10.0 + 8.0
    M.y0 += lift
    M.h += lift
    M.box = (M.x0, M.y0, M.x0 + M.mw, M.y0 + M.mh)
    T = M.T

    # ---- the map: MapBase, shop buildings in ochre
    fk = list(ns["MB_STYLE"]["fab_com"].keys())
    MB = G["pc_mapbase"](M, K, log, MB_LAYERS, {"lc_light": 0.8, "fab_com": dict((k_, SHOP_C) for k_ in fk)})
    items = MB[0]
    mb_rows = G["pc_mb_legend"](MB[1], K)
    items += G["pc_study"](M, K, log)
    lab = G["Labels"](M, lib)
    # node frames N1-N6
    for k in sorted(NODES):
        R = [T(p) for p in NODES[k]["corners"]]
        for run in M.clip(R + [R[0]]):
            items.append(L_(run, NODE_C, 0.45, "node_frames", (3.0, 1.0, 0.6, 1.0)))
    # the spine K4 -> K5 along the Selinos (as slide 5)
    sp = G["pc_selinos"](H["K4"], H["K5"])
    if sp:
        Q = [T(p) for p in sp]
        items.append(L_(Q, "FFFFFF", K["spine_w"] + 0.8, "spine"))
        items.append(L_(Q, K["spine"], K["spine_w"], "spine"))
        items.append(G["arrow_head"](Q[1], Q[0], K["spine"], 2.6, "spine"))
        items.append(G["arrow_head"](Q[-2], Q[-1], K["spine"], 2.6, "spine"))
        log.append(u"spine: K4 -> K5 along the Selinos, %.0f m" % sum(dist(a, b) for a, b in zip(sp, sp[1:])))
    else:
        log.append(u"FLAG: the Selinos centreline does not reach K4 and K5 within 80 m: no spine drawn")
    # the hubs' bus stops, walking links
    for hb in HUBS:
        for nm in D["hub_stops"][hb["code"]]:
            for n_, xy, ln in groups:
                if n_ != nm:
                    continue
                q = T(xy)
                hp = min((H[k] for k in hb["pts"]), key=lambda p: dist(p, xy))
                qa = T(hp)
                if dist(qa, q) > 1.0:
                    items.append(L_([qa, q], K["walk_link"], 0.35, "walking_links", (0.6, 0.5)))
                items.append(P_([circle(q[0], q[1], K["hub_stop_r"], 24)], "FFFFFF", INK, 0.45, "bus_stops"))
                lab.block_pt(q, K["hub_stop_r"] + 0.4)
    # places 1-6
    for n, f in sorted(PLACES.items()):
        if f["xy"] is None:
            continue
        q = T(f["xy"])
        items.append(P_([circle(q[0], q[1], 2.0, 24)], "FFFFFF", PLACE_C, 0.4, "places"))
        items.append(T_(str(n), q[0], q[1] - 0.85, 2.4, PLACE_C, "places", True, "C"))
        lab.block_pt(q, 2.4)
    # hub tiles
    s_ = K["hub_tile"]
    for hb in HUBS:
        col = K["hub"]["transit" if hb["kind"] == "hidden" else hb["kind"]]
        for k in hb["pts"]:
            q = T(H[k])
            items.append(P_([[(q[0] - s_ / 2, q[1] - s_ / 2), (q[0] + s_ / 2, q[1] - s_ / 2),
                              (q[0] + s_ / 2, q[1] + s_ / 2), (q[0] - s_ / 2, q[1] + s_ / 2)]], col, "FFFFFF", 0.3, "hubs"))
            items.append(T_(hb["code"], q[0], q[1] - tm["label"] * 0.36, tm["label"], "FFFFFF", "hubs", True, "C"))
            lab.block_pt(q, s_ / 2 + 0.4)
    # names: nodes at their highest corner, then the hub stops
    for k in sorted(NODES):
        top = max(NODES[k]["corners"], key=lambda p: p[1])
        lab.put(u"%s %s" % (k, NODES[k]["name"]), T(top), tm["label"] + 0.6, NODE_C, "node_names", True, gap=1.4)
    for hb in HUBS:
        for nm in D["hub_stops"][hb["code"]]:
            for n_, xy, ln in groups:
                if n_ == nm:
                    lab.put(nm, T(xy), tm["small"], INK, "stop_names", False, gap=1.8)
    items += lab.items
    if lab.forced:
        log.append(u"names with no free place (printed on the right of their point): %s" % u", ".join(lab.forced))

    # ---- the cards
    yt = M.y0 - 10.0
    items.append(T_(u"THE BRIDGE PLACES, HUB BY HUB, UPSTREAM TO DOWNSTREAM", M.x0, yt + 3.0, tm["sub"], INK, "cards",
                    True))
    for i, hb in enumerate(HUBS):
        it, _h = card(G, lib, K, hb, info[hb["code"]], M.x0 + i * (cw + CARD_GAP), yt, cw)
        items += it

    # ---- legend, notes, title
    def sw_line(col, w, dash=None):
        return lambda x, y: [L_([(x - 4.5, y), (x + 4.5, y)], col, w, "legend", tuple(dash) if dash else None)]

    def sw_sq(fill, stroke, lw, s=3.0, code=None):
        def f(x, y):
            it = [P_([[(x - s / 2, y - s / 2), (x + s / 2, y - s / 2), (x + s / 2, y + s / 2), (x - s / 2, y + s / 2)]],
                     fill, stroke, lw, "legend")]
            if code:
                it.append(T_(code, x, y - 0.8, 2.2, "FFFFFF", "legend", True, "C"))
            return it
        return f
    legend = [(None, u"EXISTING"),
              (lambda x, y: [P_([[(x - 4.5, y - 2.0), (x + 4.5, y - 2.0), (x + 4.5, y + 2.0), (x - 4.5, y + 2.0)]],
                                SHOP_C, None, 0.0, "legend")],
               u"building with shops: holds an OSM shop, office or craft place (MapBase)"),
              (lambda x, y: [P_([circle(x, y, K["hub_stop_r"], 24)], "FFFFFF", INK, 0.45, "legend")],
               u"bus stop of a hub (OSM; lines ESHOT where they differ)")] + mb_rows + [
              (sw_line(K["study"][0], K["study"][1], (2.4, 0.8)), u"study area"),
              (None, u"NODES (slides 7-12)"),
              (sw_line(NODE_C, 0.45, (3.0, 1.0, 0.6, 1.0)), u"node frame N1-N6 (Data/section_lines.json)"),
              (None, u"PROPOSAL MARKS")]
    legend += [(sw_line(K["spine"], K["spine_w"]), u"streamside spine, K4 to K5, along the Selinos"),
               (sw_line(K["walk_link"], 0.35, (0.6, 0.5)), u"on foot from a hub to its stop (metres on the cards)"),
               (lambda x, y: [P_([circle(x, y, 2.0, 24)], "FFFFFF", PLACE_C, 0.4, "legend"),
                              T_(u"1", x, y - 0.85, 2.4, PLACE_C, "legend", True, "C")],
                u"the project's places 1-6 (7: reed basins upstream, off the map's hubs; see K4's card)")]
    for hb in HUBS:
        kd = "transit" if hb["kind"] == "hidden" else hb["kind"]
        legend.append((sw_sq(K["hub"][kd], "FFFFFF", 0.3, 4.2, hb["code"]),
                       u"%s = %s, %s" % (hb["code"], D["hub_names"][hb["code"]], WORD[kd].lower())))
    notes = [u"Five bridge places on existing bus stops: walking hubs with a sub-hub in the bed, one transit hub, "
             u"one gateway out of town.",
             u"The stream joins the town where the shops already are: shop buildings cluster round the covered reach "
             u"(T) and the bridges (counts on the cards, %d m round each hub point)." % SHOP_R,
             u"Distances: straight line, calculated. Trips a weekday: ESHOT timetables."]
    credit = (u"Sources: " + u"; ".join(D["sources"][k] for k in ("osm", "eshot")) +
              u". Hubs and places: CityLink v13 (SUBMISSION_SON p9). Context: MapBase.")
    items += G["pc_sheet"](M, K, lib, u"The streamside spine, hub by hub",
                           u"Five bridge places, the six nodes and where the shops already are", legend, notes, credit)
    orig = G["pc_frame_check"]                       # the cards sit outside the map frame by design
    G["pc_frame_check"] = lambda its, box, lg, tw=None: orig(its, box, lg, tw, skip=G["PC_SHEET_LAYERS"] + ("cards",))
    paths = G["pc_write"](lib, M, items, OUT_DIR, NAME, u"The streamside spine, hub by hub, 1:%d" % den, log)
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
