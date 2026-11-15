# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE TRANSIT v2.23 (15 Nov 2026; v2.23 = hub tile codes centred (pages_common pc_text_c v3.31); v2.22 = Aras 15 Nov 14:45 UTC "except the 1st slide we gonna use masterplan svg as the base of the maps. another exception is the heritage loop map that should use basemap aswell also please make our working area dashed line as the most foreground line": his masterplan (master.svg, MasterplanBase cache, vector; pages_common v3.29 pc_masterplan) drawn over the base map, and the working-area dashes drawn last, on top of everything (pages_common v3.29 pc_write); v2.21 = run 10 review: loop badges 4 and 5 were still half under the K4 / K3 tiles (the hubs layer prints above the loop): a badge near a hub tile or gondola station now sits fully clear of it, off its upper right corner by the smallest step (tile half + badge radius / sqrt 2 + 0.3 mm), no leader; v2.20 = Aras 15 Nov 13:43-13:44 UTC "dont use these dashed lines to connect the stops to areas in the heritage loop map" / "it makes drawing too busy also dont have a opaque background for texts in any single of the drawings": no dashed links from hubs or loop stops to bus stops (every pin and tile sits at its true spot; stop names and metres stay in the legend and the log), no white boxes behind names (a thin text-shaped halo, pages_common v3.27 pc_halo); v2.19 = Aras 15 Nov 06:02 UTC "write the stop names that are closest to marked areas and our nodes. like stop that is closest to k4 should be written etc. same goes for asklepoion aswell": the hub stop names back on the map, and each heritage loop stop gets the nearest bus stop of the data, drawn, named and tied to it on foot (metres in the log); v2.18 = run 6: "Tabaklar Hamamı" still went under the K4 stop (every place near its ring crosses a line); a heritage-place name with no free place now goes right beside its ring, on a white halo, even over a thin line; v2.17 = run 5 review: "Tabaklar Hamamı" had no free place and the least-overlap search put it about 7 mm from its ring, by the K4 stop; a heritage-place name now searches only within 3.6 mm of its ring (gap 1.0); v2.16 = run 4 review (23:18 UTC): "Yıldız Garajı (Eski Garaj)" had no free place and sat on the loop and the bus lines, and the 570 m walk from the Teleferik ended at a stop that was not drawn: the bus station and the Teleferik's nearest town-bus stop are named with their walking metres in the legend, the stop is drawn, and no metres are printed on the map; v2.15 = run 3 review (23:11 UTC): the hub stop names left off the map (each hub row of the legend names its stop, and the dashed link ties the stop to its tile; Aras 16:26 "you dont need to write every single stops name"); they were forced over the loop names; the spine 1.2 mm (was 2.4: it outweighed the loop), bus line weights 0.9 / 0.6 / 0.35 / 0.25 so the weight steps read, the "ridership not known" note dropped; badge 7 sat on the lower Teleferik station: it moves to the station corner, and that station is named by the loop alone; v2.14 = the loop legend row names the edge arrows only when a stop lies beyond the frame (Page05 v1.6 frames the whole loop, Aras 21:30 / 21:37 UTC); v2.13 = the shared diagram style (library/diagram_style/DIAGRAM_STYLE.md rule 5, Aras 21:31 UTC "all the diagrams are awful"): one accent C07A2E = our moves (spine, walk links and now the hub tiles); existing = ink and grey, so the bus lines go grey and blue is water only; the heritage loop keeps its deep red (Aras 15:31 "just like the old diagram"); v2.12 = recheck of the 20:01 UTC laptop run against Aras's feedback: the loop badges 4 and 5 sat under the K4 / K3 tiles (now on the tile corner), the hub walk metres repeated the legend and covered "Tabak Köprüsü" and "Üç Kemer Köprüsü" (now only the links the legend does not list, placed after the names), the heritage places inside site_alan (Ulucami, Tabaklar Hamamı) named (Aras 16:27 "the names of the heritages is not in the map"); v2.11 = Aras 16:26-16:27 UTC: "remove the not needed stops you can keep the route in terms of lines however you dont need to write every single stops name"; "route should start from askepelion"; "the names of the heritages is not in the map that is on the left side": only the hub stops drawn and named (the bus lines stay), the heritage loop numbered from Asklepion with its stop names on the map, title for the one slide-5 map; v2.10 = Aras 15:31 UTC "the bold connection between the heritage should stay there just like the old diagram": the heritage loop (bold red legs, numbered stops) drawn here too by pages_common pc_loop, before the names, so no name sits on it; v2.9 = Aras 15:23 UTC "dont give sources in the brackets dont give sources in the drawings at all", 15:24 "no sources for nothing": no source in any label, legend row, note or credit (sources in the log only); v2.8 = run 8 review: a hub stop is named without its line numbers (they are in the legend, hub by hub: printed once; "Bergama Sanayi · 643 ... 936" covered the roundabout); v2.7 = Aras 13:02 rule check, run 6 review: names kept off the spine, the Selinos and the study line (Labels.block_line); WorldCover off (its 10 m cells drew stair steps); v2.6 = Aras 13:02 UTC "make sure nothing repeats in the slides": the heritage places are left out (the heritage loop page draws them); v2.5 = run 4 review: the 2023 satellite cover ends inside this frame (x 29521, y 32880) and drew a straight seam west and north, so WorldCover alone (it covers the whole frame), fainter; v2.4 = Aras 12:16 UTC "update all maps to include every detail, and top of the map, data is missing": the context is the one MapBase (survey + OSM + satellite + contours), quiet look; v2.3 = run 2 review: Bergama Garajı still two squares (50 m merge); v2.2 v2.2 = brief plan rules as the node pages: the legend in
EXISTING / PROPOSAL MARKS groups, proposal marks orange (spine, walking links; key in the data file). v2.1 v2.1 = fixes after the first run's review PNGs: heritage dots were
drawn over the K4 / K3 tiles; walking links too faint (now 0.6 / 0.5 mm dashes); Yıldız Garajı drawn as two overlapping
squares (OSM station + its unnamed building, now one); Turkish letters in the regional-line legend row (data file).
v2: also output/presentation/5.pdf): the public-transport hubs, stops and lines round the streamside
spine, as one map (a page script of the new set: one script per page, Aras 14 Nov 10:46 UTC).

Aras 14 Nov 10:44 UTC, on CityLink's p09 "The streamside spine, hub by hub": "we need to make this diagram more clear.
Like where the bus and metro or whatever public transport hubs do we have and how they can be connected to each other";
10:45: it and the heritage loop map "should not collide with each other"; 10:51: "transit hubs and heritage loop is two
different slides". So this script and bergama_page_heritage_v*.py share Data/bergama_pages_common.py (one frame, one
scale, one context, one key) and Data/bergama_access_heritage.json (the data, made offline from the OSM extract by
library/access_heritage_2026-11-14/build_data.py).

What is drawn (nothing is invented; every element names its source in the legend or the notes):
  context      OpenStreetMap buildings, roads and streams (extract of 28 Jul 2026), quiet grey; the study area
               (calisma_alan) from the Basemap cache, dash-dot
  bus lines    every OSM bus route way (15 ESHOT lines), one lane per line group side by side where groups share a road;
               line weight = buses a weekday (ESHOT timetables): town ring 651-653 thick, 656 medium, the Kozak village
               lines 831-833 thin dashed, regional lines thin grey
  stops        every OSM bus stop in the frame (the two sides of a street as one), open rings; the six hub stops bold
               with their lines (ESHOT where it differs from OSM: İstiklal Meydanı also 831-833)
  stations     OSM bus stations (Yıldız Garajı, Bergama Garajı) as squares; the Teleferik (gondola) lower and upper
               stations and its cable, ticked, then the walk up to Akropol
  hubs         K4, K3, T, K5, K6 as code tiles (the hub cards' codes); its stop(s) named in its legend row (v2.20: no link lines)
               and from the gondola to the nearest stop with a town line, with straight-line metres (calculated)
  spine        the streamside spine K4 -> K5 along the Selinos (OSM line), as on p09
  heritage     v2.6: not drawn (the heritage loop page draws them; Aras 13:02 "make sure nothing repeats")
Not drawn: metro, tram, train (Bergama has none; the nearest rail is İZBAN at Aliağa, line 835), ridership (none found).

Outputs (Downloads/Bergama/output/bergama_page_transit/): Transit.pdf (vector, layers), Transit.svg, review/ PNGs
(Aras 14 Nov 10:44: "all scripts should produce PNG's aswell which should be optimized for your viewing").
Reads: Data/bergama_access_heritage.json, Data/bergama_pages_common.py, Data/selinos_centreline.json, cached MapBase (press MapBase first), the newest
scripts/bergama_basemap_v*.py (PDF/SVG writer) and cached/bergama_basemap/basemap_layers.json (study area; press
Basemap once). Grasshopper: a Button on any input runs it; input `scale` (default from the data file, 1:2,500).
"""
import os, time

VERSION = "v2.23"   # v2.23 = hub codes centred in their tiles by pc_text_c (Aras 15 Nov 14:56 UTC "center the numbers in the boundries", standing)
NO_STOP_NAMES = False                # v2.19: the stop names on the map again (Aras 06:02)
SLIDE = 5                          # output/presentation/5.pdf (Aras 14 Nov 11:22 UTC)
GH_LABEL = "PageTransit"
OUT_FOLDER = "bergama_page_transit"
LOG_NAME = "bergama_page_transit_log.txt"
GH_INPUTS = {"scale": "int 1000..10000 = 2500"}
COMMON = os.path.join("Data", "bergama_pages_common.py")
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
NAME = "Transit"


def load_common():
    p = os.path.join(BERGAMA_ROOT, COMMON)
    if not os.path.isfile(p):
        raise RuntimeError(u"%s missing: run Bergama.bat once (the kit copies it), then press again" % p)
    ns = {"__name__": "bergama_pages_common"}
    with open(p, encoding="utf-8") as f:
        exec(compile(f.read(), p, "exec"), ns)
    return ns


def pc_lines_of(G, D, name):
    return G["pc_stop_lines"](D).get(name, set())


MB_LAYERS = {"ground", "areas", "parks", "contours", "streets", "water", "walls", "buildings", "bridges", "trees"}
# v2.5: MapBase layers drawn: all but "veg" (the 2023 satellite cover stops inside this frame: a seam)


def main():
    t0 = time.time()
    log = []
    G = load_common()
    lib = G["pc_lib"](log)
    D = G["pc_data"](log)
    K = dict(D["key"])
    ACC = "C07A2E"                                           # v2.13: DIAGRAM_STYLE rule 5, one accent = our moves
    K["hub"] = {k_: ACC for k_ in K["hub"]}
    K["lines"] = {"town": ["5E5E5E", 0.9, None], "656": ["7A7A7A", 0.6, None],      # existing = ink and grey
                  "village": ["8E8E8E", 0.35, [1.4, 0.8]], "regional": ["ABABAB", 0.25, None]}   # v2.15: steps that read
    K["spine_w"] = 1.2                                       # v2.15: the loop is the one heavy line (review 23:15)
    K["station"] = K["ink"]
    den = int(globals().get("scale") or K["scale"])
    M = G["Map"](D, den)
    T, L_, P_, T_, circle, dist = M.T, G["L_"], G["P_"], G["T_"], G["circle"], G["pc_dist"]
    INK, tm = K["ink"], K["text_mm"]
    MB = G["pc_mapbase"](M, K, log, MB_LAYERS, {"lc_light": 0.8})                      # v2.4: the one base map (every detail we have)
    items = MB[0]
    items += G["pc_masterplan"](M, log)                     # v2.22: his masterplan over the base map (Aras 14:45)
    mb_rows = G["pc_mb_legend"]([r_ for r_ in MB[1] if u"WorldCover" not in r_[2]], K)   # v2.7: no WorldCover
    items += G["pc_study"](M, K, log)
    lab = G["Labels"](M, lib)

    items += G["pc_loop"](M, D, K, lab, log, True)          # v2.10: the heritage loop (one code with the heritage map)
    RED, R = K["heritage"], K["heritage_r"]                  # v2.12: the other heritage places in the frame (Aras 16:27)
    dots = [d_ for d_ in D.get("heritage_dots", []) if M.inside(T(d_["xy"])) and
            min(dist(T(d_["xy"]), T(h["xy"])) for h in D["heritage"]) > 1.4 * R]   # off the badge
    for d_ in dots:
        q = T(d_["xy"])
        items.append(P_([circle(q[0], q[1], 1.0, 16)], "FFFFFF", RED, 0.4, "heritage_places"))
        lab.block_pt(q, 1.3)
    log.append(u"heritage places named: %s" % (u", ".join(d_["name"] for d_ in dots) or u"none in the frame"))

    # the streamside spine K4 -> K5 along the Selinos
    sp = G["pc_selinos"](D["hubs"]["K4"], D["hubs"]["K5"])
    if sp:
        Q = [T(p) for p in sp]
        items.append(L_(Q, "FFFFFF", K["spine_w"] + 0.8, "spine"))
        items.append(L_(Q, K["spine"], K["spine_w"], "spine"))
        items.append(G["arrow_head"](Q[1], Q[0], K["spine"], 2.6, "spine"))
        items.append(G["arrow_head"](Q[-2], Q[-1], K["spine"], 2.6, "spine"))
        log.append(u"spine: K4 -> K5 along the Selinos, %.0f m" % sum(dist(a, b) for a, b in zip(sp, sp[1:])))
    else:
        log.append(u"FLAG: the Selinos line of the OSM extract does not reach K4 and K5 within 80 m: no spine drawn")

    lab.block_items(items, ("spine", "study_area"))                # v2.7: names off these lines
    lab.block_line([T(p) for p in G["pc_selinos_line"]()], 2.5)       # v2.7: names off the stream

    # bus lines, one lane per group
    items += G["pc_line_items"](M, D, K)

    # gondola: cable ticked, stations, the walk up to Akropol
    st_g = [s for s in D["stations"] if s["kind"] == "gondola"]
    lower = next((s for s in st_g if u"Aşağı" in (s["name"] or u"")), None)
    upper = next((s for s in st_g if u"Yukarı" in (s["name"] or u"")), None)
    cab = [T(p) for p in D["cable"]]
    for run in M.clip(cab):
        items += G["ticked"](run, K["cable"], 0.35, 2.5, 0.9, "gondola")
    if upper:
        a, b = T(upper["xy"]), T(D["akropol"])
        for run in M.clip([a, b]):
            items.append(L_(run, K["cable"], 0.3, "gondola", (0.6, 0.8)))
    for s in st_g:
        q = T(s["xy"])
        if M.inside(q):
            items.append(P_([[(q[0] - 1.4, q[1] - 1.4), (q[0] + 1.4, q[1] - 1.4), (q[0] + 1.4, q[1] + 1.4),
                              (q[0] - 1.4, q[1] + 1.4)]], K["cable"], "FFFFFF", 0.2, "gondola"))
            lab.block_pt(q, 1.8)

    # bus stations (OSM amenity=bus_station); v2.1: a station and its unnamed building within 50 m are one square (v2.3: Bergama Garajı's are 33 m apart)
    bus_st = []
    for s in sorted([s for s in D["stations"] if s["kind"] == "bus_station"], key=lambda s: s.get("name") is None):
        if not any(dist(s["xy"], o["xy"]) < 50.0 for o in bus_st):
            bus_st.append(s)
    for s in bus_st:
        q = T(s["xy"])
        if M.inside(q):
            items.append(P_([[(q[0] - 1.6, q[1] - 1.6), (q[0] + 1.6, q[1] - 1.6), (q[0] + 1.6, q[1] + 1.6),
                              (q[0] - 1.6, q[1] + 1.6)]], "FFFFFF", K["station"], 0.45, "bus_stations"))
            lab.block_pt(q, 2.0)

    # stops (merged by name), hub stops bold
    groups = G["pc_stop_groups"](D)
    hub_stop_names = set(n for v in D["hub_stops"].values() for n in v)
    order = K["line_order"]
    stop_q, stop_all = {}, {}
    for name, xy, lines in groups:
        q = T(xy)
        stop_all.setdefault(name, []).append((q, xy, lines))
        if not M.inside(q) or name not in hub_stop_names:         # v2.11: only the hub stops (Aras 16:26)
            continue
        stop_q.setdefault(name, []).append((q, xy, lines))
        gs = [g for g in order if any(G["pc_group_of"](D, r) == g for r in lines)]
        sc = K["lines"][gs[0]][0] if gs else K["stop_line"]
        hub = name in hub_stop_names
        r = K["hub_stop_r"] if hub else K["stop_r"]
        items.append(P_([circle(q[0], q[1], r, 24)], "FFFFFF", INK if hub else sc, 0.45 if hub else 0.3, "bus_stops"))
        lab.block_pt(q, r + 0.4)

    # hubs: tiles and walking links
    hubpts = {"K4": [D["hubs"]["K4"]], "K3": [D["hubs"]["K3"]], "T": [D["hubs"]["IST"], D["hubs"]["RED"]],
              "K5": [D["hubs"]["K5"]], "K6": [D["hubs"]["K6"]]}
    links = []
    for code, pts in hubpts.items():
        for nm in D["hub_stops"][code]:
            cands = [(dist(xy, hp), hp, xy) for hp in pts for (_q, xy, _l) in stop_q.get(nm, [])]
            if cands:
                d_, hp, xy = min(cands)
                links.append((code, nm, hp, xy, d_))
    if lower:
        town = [(dist(lower["xy"], xy), nm, xy) for nm, v in stop_all.items() for (_q, xy, ln) in v
                if any(G["pc_group_of"](D, r) in ("town", "656") for r in ln)]
        if town:
            d_, nm, xy = min(town)
            links.append(("Teleferik", nm, lower["xy"], xy, d_))
    yg = next((s for s in D["stations"] if s["kind"] == "bus_station" and u"Yıldız" in (s["name"] or u"")), None)
    if yg:
        links.append(("T", yg["name"], D["hubs"]["IST"], yg["xy"], dist(D["hubs"]["IST"], yg["xy"])))
    dl = []
    for code, nm, a, b, d_ in links:
        qa, qb = T(a), T(b)
        if dist(qa, qb) < 1.0:
            continue
        if code == "Teleferik" and M.inside(qb):          # v2.16: the stop the walk ends at is drawn
            items.append(P_([circle(qb[0], qb[1], K["hub_stop_r"], 24)], "FFFFFF", INK, 0.45, "bus_stops"))
            lab.block_pt(qb, K["hub_stop_r"] + 0.4)
        log.append(u"walking link: %s -> %s %.0f m (straight line)" % (code, nm, d_))
    near = {}                                                # v2.19: the bus stop nearest each loop stop
    for h in D["heritage"]:
        qh = T(h["xy"])
        if not M.inside(qh):
            continue
        cands = [(dist(h["xy"], xy), nm, xy) for nm, v in stop_all.items() for (_q, xy, _l) in v]
        if not cands:
            continue
        d_, nm, xy = min(cands)
        qb = T(xy)
        log.append(u"nearest bus stop: %s %s -> %s %.0f m (straight line)" % (h["n"], h["name"], nm, d_))
        tel = nm in [l_[1] for l_ in links if l_[0] == "Teleferik"]   # that walk and stop are drawn already
        if nm in stop_q or nm in near or not M.inside(qb):
            continue
        near[nm] = [(qb, xy, [])]
        if not tel:
            items.append(P_([circle(qb[0], qb[1], K["hub_stop_r"], 24)], "FFFFFF", INK, 0.45, "bus_stops"))
        lab.block_pt(qb, K["hub_stop_r"] + 0.4)
    for code, pts in hubpts.items():
        col = K["hub"][D["hub_kind"][code]]
        s_ = K["hub_tile"]
        for hp in pts:
            q = T(hp)
            if not M.inside(q):
                continue
            items.append(P_([[(q[0] - s_ / 2, q[1] - s_ / 2), (q[0] + s_ / 2, q[1] - s_ / 2),
                              (q[0] + s_ / 2, q[1] + s_ / 2), (q[0] - s_ / 2, q[1] + s_ / 2)]], col, "FFFFFF", 0.3,
                            "hubs"))
            items.append(G["pc_text_c"](code, q[0], q[1], tm["label"], "FFFFFF", "hubs"))   # v2.23: centred mark
            lab.block_pt(q, s_ / 2 + 0.4)
    # v2.12: a loop badge under a hub tile (4 = K4, 5 = K3; run of 20:01 UTC) moves to the tile's upper right corner
    hq = [T(hp) for pts in hubpts.values() for hp in pts if M.inside(T(hp))] + \
        [T(s["xy"]) for s in st_g if M.inside(T(s["xy"]))]          # v2.15: a gondola station too
    keep, moved, shift = [], [], {}                          # v2.21: badge centre -> its move, clear of the tile
    for it_ in items:
        if it_[0] == "poly" and it_[6] == "loop_stops" and it_[2] == RED and len(it_[1][0]) == 32:
            c_ = (sum(p[0] for p in it_[1][0]) / 32.0, sum(p[1] for p in it_[1][0]) / 32.0)
            near_h = [h_ for h_ in hq if dist(c_, h_) < K["hub_tile"]]
            if near_h:
                h_ = min(near_h, key=lambda h: dist(c_, h))
                rb = max(dist(c_, p) for p in it_[1][0])
                a_ = K["hub_tile"] / 2.0 + rb / 1.41421 + 0.3
                shift[c_] = (h_[0] + a_ - c_[0], h_[1] + a_ - c_[1])
    for it_ in items:
        if it_[0] == "poly" and it_[6] == "loop_stops" and it_[2] == RED and len(it_[1][0]) == 32:
            c_ = (sum(p[0] for p in it_[1][0]) / 32.0, sum(p[1] for p in it_[1][0]) / 32.0)
        elif it_[0] == "text" and it_[8] == "loop_stops":
            c_ = (it_[2], it_[3] + G["PC_CAP"] * it_[4])
        else:
            keep.append(it_)
            continue
        k_ = min(shift, key=lambda c: dist(c, c_)) if shift else None
        if k_ is None or dist(k_, c_) > 0.5:
            keep.append(it_)
            continue
        dx, dy = shift[k_]
        if it_[0] == "poly":
            moved.append(P_([[(p[0] + dx, p[1] + dy) for p in it_[1][0]]], it_[2], it_[3], it_[4], "loop_stops"))
            lab.block_pt((c_[0] + dx, c_[1] + dy), R + 0.6)
        else:
            moved.append(it_[:2] + (it_[2] + dx, it_[3] + dy) + it_[4:])
    items = keep + moved
    log.append(u"loop badges moved clear of a hub tile / station: %d" % (len(moved) // 2))

    # names, most important first: hub stops, stations, other stops, heritage (the hubs' names are in the legend)
    for name, v in ([] if NO_STOP_NAMES else list(stop_q.items()) + list(near.items())):   # v2.19: hub + loop stops
        for q, xy, lines in v:
            hub = name in hub_stop_names
            off = next((fx["official_name"] for fx in D.get("official_fixes", []) if fx["name"] == name and
                        fx.get("official_name")), None)
            nm_ = name + (u" (%s)" % off if off else u"")
            lab.put(nm_, q, tm["label"],
                    INK, "stop_names", hub, gap=1.8)
    for s in D["stations"]:
        q = T(s["xy"])
        if M.inside(q) and s.get("name") and s["kind"] == "gondola" and u"Aşağı" not in s["name"]:   # v2.15/16
            nm = G["pc_station_name"](s)
            lab.put(nm, q, tm["label"], K["cable"] if s["kind"] == "gondola" else K["station"], "station_names", True)
    for d_ in dots:
        n_f = len(lab.forced)
        lab.put(d_["name"], T(d_["xy"]), tm["small"], RED, "loop_names", gap=1.0)   # v2.17: kept by its ring
        if len(lab.forced) > n_f and lab.items and lab.items[-1][0] == "text":      # v2.18: right beside its ring
            q, w_ = T(d_["xy"]), lib["text_w"](d_["name"], tm["small"], False)
            x_, y_ = q[0] + 1.6, q[1] - tm["small"] * 0.375
            b_ = (x_ - 0.3, y_ - 0.25 * tm["small"] - 0.3, x_ + w_ + 0.3, y_ + tm["small"] * 0.75 + 0.3)
            del lab.items[-1]
            while lab.items and (lab.items[-1][8] if lab.items[-1][0] == "text" else lab.items[-1][6]) == \
                    "loop_names_halo":                       # v2.20: the halo copies of pages_common v3.27
                del lab.items[-1]
            lab.boxes[-1] = b_
            lab.items += G["pc_halo"](d_["name"], x_, y_, tm["small"], False, "L", "loop_names_halo")   # v2.20: no box
            lab.items.append(T_(d_["name"], x_, y_, tm["small"], RED, "loop_names", False, "L"))
            log.append(u"%s: no free place, printed right beside its ring" % d_["name"])
    for s_t, mid in dl:                                      # v2.12: metres last (names first)
        lab.put(s_t, mid, tm["small"], K["walk_link"], "walking_links_text", gap=0.8)
    items += lab.items
    if lab.forced:
        log.append(u"names with no free place (printed where they overlap least): %s" % u", ".join(lab.forced))

    # legend, notes, title
    def sw_line(col, w, dash=None):
        return lambda x, y: [L_([(x - 4.5, y), (x + 4.5, y)], col, w, "legend", tuple(dash) if dash else None)]

    def sw_sq(fill, stroke, lw, s_=3.0, code=None, tc="FFFFFF"):
        def f(x, y):
            it = [P_([[(x - s_ / 2, y - s_ / 2), (x + s_ / 2, y - s_ / 2), (x + s_ / 2, y + s_ / 2),
                       (x - s_ / 2, y + s_ / 2)]], fill, stroke, lw, "legend")]
            if code:
                it.append(G["pc_text_c"](code, x, y, 2.2, tc, "legend"))   # v2.23: centred mark
            return it
        return f
    LN = D["lines"]
    # v2.2 (brief plan rules, as the node pages, PR #176): EXISTING kept apart from the PROPOSAL marks (orange)
    legend = [(None, u"EXISTING: PUBLIC TRANSPORT")]
    legend += [(sw_line(K["lines"][g][0], K["lines"][g][1], K["lines"][g][2]),
                u"%s: %s a weekday" % (LN[g]["word"], LN[g]["per_weekday"])) for g in order]
    legend += [
        (lambda x, y: [P_([circle(x, y, K["hub_stop_r"], 24)], "FFFFFF", INK, 0.45, "legend")],
         u"bus stop nearest a hub or a loop stop, named (a hub's stop, lines and metres on foot: hub rows below)"),
        (sw_sq("FFFFFF", K["station"], 0.45), u"bus station" + u"".join(
            u": %s, %d m on foot from T" % (G["pc_station_name"]({"name": nm}), round(d_, -1))
            for c_, nm, _a, _b, d_ in links if c_ == "T" and nm not in stop_q)),
        (lambda x, y: G["ticked"]([(x - 4.5, y), (x + 4.5, y)], K["cable"], 0.35, 2.5, 0.9, "legend") +
         sw_sq(K["cable"], "FFFFFF", 0.2, 2.6)(x + 4.5, y), u"Teleferik (gondola) and its stations; dotted: on foot to Akropol" + u"".join(
            u"; nearest town-bus stop %s, %d m on foot" % (nm, round(d_, -1))
            for c_, nm, _a, _b, d_ in links if c_ == "Teleferik")),
        (None, u"EXISTING: CONTEXT"),
    ] + mb_rows + [
        (sw_line(K["water"][0], 0.3), u"Selinos and side streams"),
        (sw_line(K["study"][0], K["study"][1], (2.4, 0.8)), u"study area"),
        (None, u"PROPOSAL MARKS"),
        (sw_line(K["spine"], K["spine_w"]), u"streamside spine, K4 to K5, along the Selinos"),
        (lambda x, y: [L_([(x - 4.5, y), (x + 4.5, y)], "FFFFFF", K["heritage_w"] + 0.6, "legend"),
                       L_([(x - 4.5, y), (x + 4.5, y)], K["heritage"], K["heritage_w"], "legend"),
                       P_([circle(x + 4.5, y, 1.4, 24)], K["heritage"], "FFFFFF", 0.3, "legend")],
         u"heritage loop, stop to stop, from 1 Asklepion to 7 Teleferik" +
         (u"; arrows: stops beyond the map" if any(not M.inside(T(h["xy"])) for h in D["heritage"]) else u"")),
        (lambda x, y: [P_([circle(x, y, 1.0, 16)], "FFFFFF", K["heritage"], 0.4, "legend")],
         u"other heritage place"),
    ]
    word = {"walk": u"walking hub", "transit": u"main transit hub", "gateway": u"gateway out of town"}
    for code in ("K4", "K3", "T", "K5", "K6"):           # one row per hub: what it is, its stop(s), lines, metres
        kd = D["hub_kind"][code]
        st = [u"%s %d m (%s)" % (nm, round(d_), u" ".join(sorted(pc_lines_of(G, D, nm), key=lambda r: (len(r), r))))
              for c_, nm, _a, _b, d_ in links if c_ == code and nm in stop_q]
        legend.append((sw_sq(K["hub"][kd], "FFFFFF", 0.3, 4.2, code),
                       u"%s = %s, %s; stop: %s" % (code, D["hub_names"][code], word[kd], u"; ".join(st) or u"none")))
    notes = [u"No metro, tram or train runs in Bergama. The nearest rail is İZBAN at Aliağa: line 835 runs there 44 times "
             u"each way a weekday, timed to İZBAN.",
             u"Line weight = buses a weekday. Where line groups share a road they run side by side."]
    log.append(u"sources (log only, Aras 15:23): " + u"; ".join(D["sources"][k] for k in ("osm", "eshot")) +
               u". Distances: straight line, calculated.")
    credit = u""
    items += G["pc_sheet"](M, K, lib, u"Public transport and the heritage loop",
                           u"Bus lines, the hubs and their stops, the Teleferik and the loop from Asklepion",
                           legend, notes, credit)
    paths = G["pc_write"](lib, M, items, OUT_DIR, NAME, u"Public transport round the spine, 1:%d" % den, log)
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
