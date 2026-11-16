# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE01 MOVE v1.19 (15 Nov 2026; v1.19 = Aras 14:45 UTC "please make our working area dashed line as the most foreground line": the study area dashed line is drawn last, over every other line, mark and name of the map; v1.18 = Aras 14:38 UTC "dont do hatches to river" (a rule for every drawing): the water is a flat fill, no hatch; v1.17 = Aras dislikes purple: the civic offices pin slate 5C7A86 (was purple 6F42C1); Aras 13:44 UTC "dont have a opaque background for texts in any single of the drawings": the street names have no white box behind them (Labels halo off); v1.16 = Aras 13:36 UTC "these three are whole different categories" / "3 of these 4 are different categories" / "mosque and heritage places are somewhat related ... showing car parks or fuel stations is not needed": the places on the map are drawn in their own kinds, each with its own mark and its count from the data (OSM tags, Overture place categories): schools, health, civic offices and public services, mosques with heritage places and museums (one kind), bus stops and the bus station; car parks, fuel and car services are no longer drawn (the route index is unchanged: the cached route search still counts them as destinations); v1.15 = Aras 13:35 UTC "why do we have blue lines in middle ?": the navy driving lines ran down the middle of the walking bands (same street centre lines) and read as one cluttered stripe: each driving line now runs BESIDE its street's walking band (offset to the north-east side by half the band + a 0.35 mm gap), so the two layers read apart; the legend shows the line under the band the same way; v1.14 = Aras 10:33 UTC "this map is not readable ... degraded in the information intensity": on the new A05 base (MapBase v1.6+) the houses are WHITE on a pale ground, so the town fabric vanished under the routes and the hatched water shouted: here the houses are a light warm grey again (the fabric reads, as on the v1.5 base), monuments and mosques a shade warmer, the ground paler, the water hatch light, so the routes and places are the strongest layer; v1.13 = run 15: in the slide panel the map was held down by the page height and ran only ~60 % of the width: the map's scale now comes from the width alone (edge to edge, Aras 05:54 UTC); the page grows down for the legend (the slide fits the whole page by its ink); v1.12 = run 13: the legend under the map in 3-4 even columns broke its groups (the route classes split over two columns): at most 2 columns, the routes group in the first, places + study area in the second; v1.11 = run 13: a place mark at the frame edge reached past it (FLAG): place marks are cut to the map frame; v1.10 = Aras 05:54 UTC "this map is too cramped you need to extend it from most left to most right": the map now runs the whole page width, the legend in columns UNDER it (north and scale under the legend's first column); v1.9 = slide 1 run 8: the north arrow and scale sat over the legend's last rows (pc_sheet draws them 30-48 mm above the span foot): the span foot is now 55 mm under the legend's last line; v1.8 = slide 1 run 7: the long first legend head ran into the second column: split in two short heads; north and scale right under the legend, not at the page foot (they made the page tall); v1.7 = slide 1 review (run 5): the walking bands' round ends stuck out ~1 mm below the map frame: every route line is now cut to the frame (clip); street names 1.35 x larger; legend heads no longer point to "the site map" (shops: see Plan 01); "800 M" written 800 m; v1.6 = v1.6 = slide01 run 3: the legend needed two columns in the slide panel and the map shrank to a third of it: walking and driving share one row per index class (wide band = on foot, dark line = by car), 15 rows -> 9; v1.5 = Aras 16:17 UTC "KEEP EVERY DRAWING STRICTLY IN SITE_ALAN": the map is site_alan turned flat (pages_common SiteMap) along the page top, the legend in as many columns as the page height needs right of it, north turned with the frame; v1.4 = Aras 16:16 UTC "these are too close in colours ... line differences are not appearant enough": the places get three contrasting hues AND shapes (blue circle, gold diamond, green square); the walking ramp has wide lightness steps (pale yellow to deep wine) and wider bands; driving lines navy, the two lower classes dashed; v1.3 = Aras 15:25 UTC "fit every drawing into A3's like the scale is not important": scale 0 (default) = the largest round scale that fits A3 landscape (or the slide sheet's page_mm), centred; v1.2 = Aras 15:23 UTC "dont give sources in the drawings at all": no source words in notes or credit, sources to the log only; v1.1 = Aras 13:02 UTC "make sure nothing repeats in the slides": the shop buildings and the ground key are on Page02 (same slide), so here the base is plain MapBase with no shop colour and no ground key), slide 1 (analysis): how people use the streets, ONE map.
Redoes SUBMISSION_SON p7 ("How people use it": shops and everyday walks / pedestrian flow / vehicles, three maps) as one
drawing on the one MapBase, each piece of information once (Aras 14 Nov 12:36 UTC: "p7 we need to merge all those into
one single drawing. With colours diffrentiated ... informations shouldn't be repeated ... again using the latest
basemap"; 12:38 UTC: "if one scripts does that job cache it and make it usable by the next script").

Method (the movement potential of selinus_board v67 / bergama_movement v1, its route search copied unchanged): every
street piece of OpenStreetMap counts the shortest routes that pass along it, from every building (origins: all MapBase
buildings) to every everyday destination (Overture places with confidence 0.45+, OSM shops, offices, services, places
of worship, schools, bus stops) within 800 m on foot (flat ground) or 600 s by car (OSM maxspeed, else 50 km/h, one-way
streets kept). Index 100 = the busiest piece inside the frame, per mode. Walking and driving are the two layers of the
map: walking a wide warm band, driving a thin dark line beside it; shops are the buildings MapBase marks with shops, offices
or workshops; everyday destinations other than shops are small symbols.

Outputs (Downloads/Bergama/output/bergama_page01_move/): StreetUse.pdf, StreetUse.svg, review/ PNGs; the cache
cached/bergama_movement/movement.json (every street piece with its walking and driving index) for later pages (slide 5).
The route search runs only when the cache is missing or older than the OSM file, MapBase cache or places file.
Reads: Data/bergama_pages_common.py (v3.5+), Data/bergama_access_heritage.json (frame), Data/bergama_osm.osm,
Data/bergama_places.geojson, the newest MapBase script and its cache. Grasshopper: a Button runs it; input scale.
"""
import os, time, math, json, heapq

VERSION = "v1.27"  # v1.27 (Aras 16 Nov 00:32 UTC "take node pins into the working area and in the middle width wise"): each pin keeps its place along the strip (map x) and is moved to the middle of the working area across the strip at that x (between its edges); FLAG if the working area does not cross that x; v1.26 v1.26 (Aras 23:44 UTC "get node pins into how people use it diagram"): the six nodes N1-N6 as orange pins (NODE_C, the same pin as Page01Free v1.20: in the middle of each node's part inside the working area, from Data/section_lines.json), drawn last; a legend row; v1.25 v1.25 (Aras 23:38 UTC "make the colour change instead of thickness"): every use line one width (USE_W), how much use = colour ramp WALK_C (pale yellow to deep wine, 4 classes); the share-on-foot colours dropped (log only); legend = the 4 colour steps under "RELATIVE USE, NOT COUNTED PEOPLE"; v1.24 v1.24 (Aras 21:16 UTC "like how many total people use there and how"): band width = all routes on the piece (on foot + by car, route pairs, relative use), colour = share on foot (3 steps); legend to match; v1.23: v1.23 (Aras 21:15 UTC "those thicker lines should be average of both"): each band's class = the mean of the piece's on-foot and by-car index (both 0-100 inside the frame); v1.22: v1.22 (Aras 21:09 UTC "remove these dashed and solid thin lines from how people use street diagram"): no by-car lines and no working-area line on this diagram (legend to match); v1.21: v1.21 (Aras 17:03 UTC "why do we have these dashed lines again ?" / "these lines above roads ?", default until he says otherwise: main roads only): only the two upper by-car classes are drawn, as thin solid navy lines beside their bands; the dotted / dashed lower classes are gone (the only dashed line left is the working area); v1.20: v1.20: line weights scale with the drawing size (Aras 15:57 UTC, pages_common v3.33 pc_stroke_k);
GH_LABEL = "Page01Move"
OUT_FOLDER = "bergama_page01_move"
LOG_NAME = "bergama_page01_move_log.txt"
GH_INPUTS = {"scale": "int 0..30000 = 0"}
COMMON = os.path.join("Data", "bergama_pages_common.py")
PLACES = os.path.join("Data", "bergama_places.geojson")
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
MV_FILE = os.path.join(BERGAMA_ROOT, "cached", "bergama_movement", "movement.json")
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
NAME = "StreetUse"
TITLE = u"How people use the streets"
SUB = u"Walking, driving and where people go, on one map"
# movement options of bergama_movement v1 (selinus_board v67 MV_OPT): parameters, not data
R_WALK, T_CAR, SNAP, URBAN = 800.0, 600.0, 150.0, 50.0   # m, s, m, km/h (urban limit, Karayolları Trafik Yön. md. 100)
WALK_NO_HW = {"motorway", "motorway_link"}
CAR_HW = {"trunk", "trunk_link", "primary", "primary_link", "secondary", "secondary_link", "tertiary", "tertiary_link",
          "unclassified", "residential", "living_street", "service", "road"}
SKIP_HW = {"proposed", "construction", "platform", "bus_stop", "elevator"}
INST_AMEN = {"school", "university", "college", "kindergarten", "hospital", "clinic", "doctors", "dentist", "townhall",
             "courthouse", "police", "fire_station", "library", "community_centre", "post_office", "social_facility"}
COM_AMEN = {"restaurant", "cafe", "bar", "pub", "fast_food", "bank", "pharmacy", "marketplace", "ice_cream",
            "bureau_de_change", "money_transfer"}
TRN_AMEN = {"parking", "bus_station", "fuel", "car_wash", "taxi", "charging_station"}
CLS = (2.0, 10.0, 25.0, 50.0, 100.0)             # index classes 0-2, 2-10, 10-25, 25-50, 50-100 (selinus_board R28MV_CLS)
WALK_W = (0.0, 0.8, 1.6, 2.6, 3.8)              # mm: walking band per class (class 0 not drawn); v1.4 wider steps
WALK_C = ("FFFFFF", "F7D488", "F0A04B", "D2452E", "7A1020")    # v1.4: pale yellow, orange, red, deep wine
CAR_W = (0.0, 0.2, 0.35, 0.4, 0.55)             # mm: driving line per class (v1.21: thinner, Aras 17:03)
CAR_D = (1, 1, 1, 1, 1)                          # v1.21: solid only (no dashed car lines)
CAR_SHOWN = ()  # v1.22: no car lines (Aras 21:09 UTC); v1.21 was (3, 4)                               # v1.21: the by-car classes drawn (main roads only)       # v1.4: the two lower classes dotted / dashed, the upper two solid
HOW_C = ("F0A04B", "C77B5E", "5B7A99")          # v1.24: mostly on foot / mixed / mostly by car (v1.25: not drawn)
NODE_C = "C07A2E"                                # v1.26: the node pins (proposal accent, as Page01Free)
USE_W = 1.2                                      # v1.25: mm, the one width of every use line (colour = how much)
CAR_C = "16324F"                                 # v1.4: navy (cool against the warm walking bands)
DEST = {"institutional": (u"Schools, health, civic offices", "1F78D1", "circle"),
        "religious": (u"Mosques, heritage places", "F2B705", "diamond"),
        "transport": (u"Bus stops, bus station, car parks, fuel", "17A673", "square")}   # v1.4: hue + shape (routes)
# v1.16 (Aras 13:36 UTC): the kinds DRAWN, in legend order: (key, words, colour, mark)
KINDS = [("school", u"Schools", "1F78D1", "circle"), ("health", u"Health: hospitals, clinics", "D6336C", "cross"),
         ("civic", u"Civic offices, public services", "5C7A86", "square"),
         ("sacred", u"Mosques, heritage places, museums", "F2B705", "diamond"),
         ("transit", u"Bus stops, bus station", "17A673", "triangle")]
K_SCHOOL = {"school", "university", "college", "kindergarten"}
K_HEALTH = {"hospital", "clinic", "doctors", "dentist"}
K_CIVIC = {"townhall", "courthouse", "police", "fire_station", "library", "community_centre", "post_office",
           "social_facility"}
MV_ENGINE = "v1"                                # the route search's version (the cache is reused while it holds)
N_NAMES = 8                                     # street names: the busiest named streets on foot


def pin(q, label, P_, T_, circle, box=None, clip=None, layer="nodes", tc=None):
    """v1.13: a map pin, its tip at q: a disc with the node name over a short point; v1.14: inside box (down when
    near the top, the head shifted in from the sides), cut to clip"""
    r, h = 2.7, 4.6
    up = box is None or q[1] + h + r + 0.4 <= box[3]
    cx, cy = q[0], q[1] + (h if up else -h)
    if box is not None:
        cx = min(max(cx, box[0] + r + 0.4), box[2] - r - 0.4)
    sg = 1.0 if up else -1.0
    tri = [(q[0], q[1]), (cx - r * 0.72, cy - sg * r * 0.69), (cx + r * 0.72, cy - sg * r * 0.69)]
    out = [P_([tri], NODE_C, None, 0.0, layer), P_([circle(cx, cy, r, 32)], NODE_C, "FFFFFF", 0.3, layer),
           tc(label, cx, cy, 2.3, "FFFFFF", layer) if tc else T_(label, cx, cy - 0.85, 2.3, "FFFFFF", layer, True, "C")]
    if clip:
        out = [it[:9] + (clip,) + tuple(it[10:]) if it[0] == "poly" else it for it in out]
    return out


def clip_convex(P, C):
    """v1.19: polygon P cut by the convex polygon C (Sutherland-Hodgman; both [(x, y)])"""
    def side(a, b, p):
        return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
    sg = 1.0 if sum(C[i - 1][0] * C[i][1] - C[i][0] * C[i - 1][1] for i in range(len(C))) > 0 else -1.0
    out = list(P)
    for i in range(len(C)):
        a, b = C[i - 1], C[i]
        inp, out = out, []
        for j in range(len(inp)):
            p, q = inp[j - 1], inp[j]
            sp, sq = sg * side(a, b, p), sg * side(a, b, q)
            if sq >= 0:
                if sp < 0:
                    t = sp / (sp - sq)
                    out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
                out.append(q)
            elif sp >= 0:
                t = sp / (sp - sq)
                out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
        if not out:
            break
    return out


def inner_point(P):
    """v1.19: the grid point of P farthest from its edges (a point well inside, even in a thin or bent piece)"""
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    st = max(1.0, max(max(xs) - min(xs), max(ys) - min(ys)) / 40.0)

    def inside(x, y):
        c = False
        for i in range(len(P)):
            (x1, y1), (x2, y2) = P[i - 1], P[i]
            if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
                c = not c
        return c

    def edge_d(x, y):
        d = 1e18
        for i in range(len(P)):
            (ax, ay), (bx, by) = P[i - 1], P[i]
            dx, dy = bx - ax, by - ay
            L2 = dx * dx + dy * dy or 1e-12
            t = max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / L2))
            d = min(d, math.hypot(x - ax - t * dx, y - ay - t * dy))
        return d
    best, bd = None, -1.0
    y = min(ys) + st / 2.0
    while y < max(ys):
        x = min(xs) + st / 2.0
        while x < max(xs):
            if inside(x, y):
                d = edge_d(x, y)
                if d > bd:
                    best, bd = (x, y), d
            x += st
        y += st
    return best


def thin_lines(items, k):
    """v1.20 (Aras 15 Nov 15:57 UTC "scale the lines according to the drawing size ... across all drawings", standing):
    every line heavier than 0.25 mm times the drawing's stroke factor k (pages_common pc_stroke_k), never under 0.25"""
    return [it[:3] + (max(0.25, it[3] * k),) + it[4:] if it[0] == "line" and it[3] and it[3] > 0.25 else it
            for it in items]


def load_common():
    p = os.path.join(BERGAMA_ROOT, COMMON)
    if not os.path.isfile(p):
        raise RuntimeError(u"%s missing: run Bergama.bat once (the kit copies it), then press again" % p)
    ns = {"__name__": "bergama_pages_common"}
    with open(p, encoding="utf-8") as f:
        exec(compile(f.read(), p, "exec"), ns)
    return ns


# ---------------- the route search (selinus_board v67 MV_KERNEL mv_source, unchanged)
def mv_source(adj, s, ws, dw, limit):
    dist = {s: 0.0}
    pred = {}
    seen = set()
    order = []
    h = [(0.0, s)]
    while h:
        d, i = heapq.heappop(h)
        if i in seen:
            continue
        seen.add(i)
        order.append(i)
        for j, c, e in adj[i]:
            nd = d + c
            if nd <= limit and (j not in dist or nd < dist[j]):
                dist[j] = nd
                pred[j] = (i, e)
                heapq.heappush(h, (nd, j))
    flow = {}
    out = {}
    for i in reversed(order):
        f = flow.get(i, 0) + dw.get(i, 0)
        if f and i != s:
            p, e = pred[i]
            out[e] = out.get(e, 0) + ws * f
            flow[p] = flow.get(p, 0) + f
    return out


def compress(pieces, use, key_extra, car):
    """selinus_board v67 compress (no slope): chains between junctions; adj over key nodes"""
    inc = {}
    for pi in use:
        p = pieces[pi]
        inc.setdefault(p["a"], []).append(pi)
        inc.setdefault(p["b"], []).append(pi)
    keys = set(n for n, l in inc.items() if len(l) != 2) | (set(key_extra) & set(inc))
    for n, l in inc.items():
        if len(l) == 2 and l[0] == l[1]:
            keys.add(n)
    done = set()
    chains = []

    def walk_from(k, pi):
        nodes, seq, cur = [k], [], k
        while True:
            p = pieces[pi]
            done.add(pi)
            nxt = p["b"] if p["a"] == cur else p["a"]
            seq.append((pi, p["a"] == cur))
            nodes.append(nxt)
            cur = nxt
            if cur in keys:
                break
            l = inc[cur]
            pi = l[0] if l[1] == pi else l[1]
            if pi in done:
                break
        return nodes, seq
    for k in sorted(keys):
        for pi in inc[k]:
            if pi not in done:
                chains.append(walk_from(k, pi))
    for pi in use:
        if pi not in done:
            k = min(pieces[pi]["a"], pieces[pi]["b"])
            keys.add(k)
            chains.append(walk_from(k, pi))
    kl = sorted(keys)
    kidx = dict((n, i) for i, n in enumerate(kl))
    adj = [[] for _ in kl]
    for ci, (nodes, seq) in enumerate(chains):
        L = sum(pieces[pi]["L"] for pi, _ in seq)
        if car:
            f = all(pieces[pi]["cf"] if fw else pieces[pi]["cb"] for pi, fw in seq)
            b = all(pieces[pi]["cb"] if fw else pieces[pi]["cf"] for pi, fw in seq)
            c = sum(pieces[pi]["L"] / (pieces[pi]["v"] / 3.6) for pi, _ in seq)
        else:
            f = b = True
            c = L
        u, v = kidx[nodes[0]], kidx[nodes[-1]]
        if f:
            adj[u].append((v, c, ci))
        if b:
            adj[v].append((u, c, ci))
    return [tuple(sorted(a)) for a in adj], chains, kidx


def snap(pts, xy, ids, dmax):
    g = {}
    for n in ids:
        g.setdefault((int(xy[n][0] // dmax), int(xy[n][1] // dmax)), []).append(n)
    out, far = {}, 0
    for x, y in pts:
        best, bd = None, dmax
        i0, j0 = int(x // dmax), int(y // dmax)
        for i in (i0 - 1, i0, i0 + 1):
            for j in (j0 - 1, j0, j0 + 1):
                for n in g.get((i, j), ()):
                    d = math.hypot(xy[n][0] - x, xy[n][1] - y)
                    if d < bd or (d == bd and best is not None and n < best):
                        best, bd = n, d
        if best is None:
            far += 1
        else:
            out[best] = out.get(best, 0) + 1
    return out, far


def potential(pieces, use, org, dst, car, label, log):
    t0 = time.time()
    adj, chains, kidx = compress(pieces, use, list(org) + list(dst), car)
    dw = dict((kidx[n], w) for n, w in dst.items() if n in kidx)
    tot = {}
    tasks = [(kidx[n], w) for n, w in sorted(org.items()) if n in kidx]
    for s, ws in tasks:
        for e, v in mv_source(adj, s, ws, dw, T_CAR if car else R_WALK).items():
            tot[e] = tot.get(e, 0) + v
    val = {}
    for ci, (nodes, seq) in enumerate(chains):
        for pi, _ in seq:
            val[pi] = tot.get(ci, 0)
    log.append(u"%s: %d origin nodes, %d destination nodes, %.1f s" % (label, len(tasks), len(dw), time.time() - t0))
    return val


def _walk_ok(t):
    if t.get("highway") in WALK_NO_HW:
        return False
    if t.get("foot") in ("yes", "designated", "permissive"):
        return True
    return t.get("foot") != "no" and t.get("access") != "no"


def _car_dirs(t):
    if t.get("highway") not in CAR_HW:
        return False, False
    if any(t.get(k_) == "no" for k_ in ("access", "vehicle", "motor_vehicle", "motorcar")):
        return False, False
    ow = (t.get("oneway") or "").lower()
    if ow in ("yes", "1", "true"):
        return True, False
    if ow == "-1":
        return False, True
    if t.get("junction") in ("roundabout", "circular") and ow != "no":
        return True, False
    return True, True


def _speed(t):
    v = (t.get("maxspeed") or "").strip().lower()
    try:
        num = float(v.replace("km/h", "").replace("kmh", "").strip().split(";")[0])
        if v.endswith("mph"):
            num *= 1.609344
        if 3.0 <= num <= 150.0:
            return num
    except Exception:
        pass
    return URBAN


def poi_class(t):
    am = t.get("amenity")
    h = t.get("historic")
    if am == "place_of_worship" or (h is not None and h not in ("memorial", "boundary_stone", "milestone",
                                                                  "wayside_cross", "yes")) or \
            t.get("tourism") in ("museum", "attraction"):
        return "religious"
    if am in INST_AMEN:
        return "institutional"
    if "shop" in t or "office" in t or "craft" in t or am in COM_AMEN or \
            t.get("tourism") in ("hotel", "guest_house", "hostel", "motel"):
        return "commercial"
    if am in TRN_AMEN:
        return "transport"
    return None


def place_cat(h, basic):
    top = h[0] if h else ""
    sub = h[1] if len(h) > 1 else ""
    if top == "cultural_and_historic":
        return "institutional" if sub == "cultural_center" else "religious"
    if top in ("education", "health_care", "community_and_government"):
        return "institutional"
    if top == "arts_and_entertainment":
        return "institutional" if sub in ("museum", "performing_arts_venue", "arts_and_crafts_space") else "commercial"
    if top == "travel_and_transportation":
        if sub in ("parking", "fueling_station", "ground_transport_facility_or_service"):
            return "transport"
        return "industrial" if sub == "vehicle_service" else "commercial"
    if top in ("shopping", "food_and_drink", "lodging", "lifestyle_services"):
        return "commercial"
    if top == "services_and_business":
        if sub in ("manufacturer", "b2b_transportation_and_storage_service", "storage_facility", "agricultural_service"):
            return "industrial"
        return "commercial"
    if top == "sports_and_recreation":
        return None if sub in ("park", "recreational_trail_or_path") else "commercial"
    return None


def osm_kind(t):
    """v1.16: the kind drawn for an OSM feature, or None (car parks, fuel, shops are not drawn)"""
    if t.get("highway") == "bus_stop" or t.get("public_transport") == "platform" or \
            t.get("amenity") in ("bus_station", "taxi"):
        return "transit"
    c = poi_class(t)
    if c == "religious":
        return "sacred"
    if c == "institutional":
        am = t.get("amenity")
        return "school" if am in K_SCHOOL else "health" if am in K_HEALTH else "civic"
    return None


def place_kind(h):
    """v1.16: the kind drawn for an Overture place (its category hierarchy), or None"""
    top = h[0] if h else ""
    sub = h[1] if len(h) > 1 else ""
    if top == "education":
        return "civic" if sub == "library" else "school"
    if top == "health_care":
        return "health"
    if top == "community_and_government":
        return "civic"
    if top == "cultural_and_historic":
        return "civic" if sub == "cultural_center" else "sacred"
    if top == "arts_and_entertainment" and sub in ("museum", "performing_arts_venue", "arts_and_crafts_space"):
        return "sacred" if sub == "museum" else "civic"
    if top == "travel_and_transportation" and sub == "ground_transport_facility_or_service":
        return "transit"
    return None


def read_kinds(lib, box, log):
    """v1.16: every place drawn, (x, y, kind), from the same sources and rules as the route search's destinations
    (OSM nodes and closed ways; Overture places of confidence 0.45+ not within 10 m of an OSM one of the same kind)"""
    import xml.etree.ElementTree as ET
    osm = os.path.join(BERGAMA_ROOT, lib["OSM_FILE"])
    plc = os.path.join(BERGAMA_ROOT, PLACES)
    to_s = lib["to_survey"]
    root = ET.parse(osm).getroot()
    ll, out = {}, []
    for n in root.iter("node"):
        try:
            ll[n.get("id")] = (float(n.get("lon")), float(n.get("lat")))
        except (TypeError, ValueError):
            continue
        tg = dict((t.get("k"), t.get("v")) for t in n.findall("tag"))
        k = osm_kind(tg) if tg else None
        if k:
            out.append(to_s(*ll[n.get("id")]) + (k, "osm"))
    for w in root.iter("way"):
        tg = dict((t.get("k"), t.get("v")) for t in w.findall("tag"))
        if tg.get("highway"):
            continue
        refs = [nd.get("ref") for nd in w.findall("nd") if nd.get("ref") in ll]
        k = osm_kind(tg) if len(refs) >= 4 and refs[0] == refs[-1] else None
        if k:
            P = [to_s(*ll[r]) for r in refs[:-1]]
            out.append((sum(q[0] for q in P) / len(P), sum(q[1] for q in P) / len(P), k, "osm"))
    if os.path.isfile(plc):
        with open(plc, encoding="utf-8") as f:
            J = json.load(f)
        for ft in J.get("features", []):
            try:
                g, p = ft.get("geometry") or {}, ft.get("properties") or {}
                if g.get("type") != "Point" or (p.get("confidence") or 0.0) < 0.45:
                    continue
                tx = p.get("taxonomy") or {}
                if isinstance(tx, str):
                    tx = json.loads(tx)
                k = place_kind(tx.get("hierarchy") or [])
                if k:
                    x, y = to_s(*g["coordinates"][:2])
                    if not any(d[2] == k and d[3] == "osm" and math.hypot(d[0] - x, d[1] - y) <= 10.0 for d in out):
                        out.append((x, y, k, "overture"))
            except Exception:
                continue
    b = box
    out = [d for d in out if b[0] <= d[0] <= b[2] and b[1] <= d[1] <= b[3]]
    log.append(u"places drawn by kind (OSM + Overture, frame box): %s" % u", ".join(
        u"%s %d" % (k_, sum(1 for d in out if d[2] == k_)) for k_, w_, c_, m_ in KINDS))
    return out


def compute(lib, C, D, log):
    """the street pieces with their walking / driving index (the cache); route search once"""
    import xml.etree.ElementTree as ET
    osm = os.path.join(BERGAMA_ROOT, lib["OSM_FILE"])
    plc = os.path.join(BERGAMA_ROOT, PLACES)
    mbf = os.path.join(BERGAMA_ROOT, "cached", "bergama_mapbase", "mapbase.json")
    srcs = [p for p in (osm, plc, mbf) if os.path.isfile(p)]
    if os.path.isfile(MV_FILE) and os.path.getmtime(MV_FILE) > max(os.path.getmtime(p) for p in srcs):
        with open(MV_FILE, encoding="utf-8") as f:
            R = json.load(f)
        if R.get("version") == MV_ENGINE:
            log.append(u"movement: cache %s (%s)" % (MV_FILE, R.get("made")))
            return R
    to_s = lib["to_survey"]
    root = ET.parse(osm).getroot()
    ll, dst = {}, []
    for n in root.iter("node"):
        try:
            ll[n.get("id")] = (float(n.get("lon")), float(n.get("lat")))
        except (TypeError, ValueError):
            continue
        tg = dict((t.get("k"), t.get("v")) for t in n.findall("tag"))
        if tg:
            bus = tg.get("highway") == "bus_stop" or tg.get("public_transport") == "platform"
            pc = "transport" if bus else poi_class(tg)
            if pc:
                dst.append(to_s(*ll[n.get("id")]) + (pc, "osm"))
    xy, segs, n_sp = {}, [], 0
    for w in root.iter("way"):
        tg = dict((t.get("k"), t.get("v")) for t in w.findall("tag"))
        refs = [nd.get("ref") for nd in w.findall("nd") if nd.get("ref") in ll]
        hw = tg.get("highway")
        if not hw:
            pc = poi_class(tg) if len(refs) >= 4 and refs[0] == refs[-1] else None
            if pc:
                P = [to_s(*ll[r]) for r in refs[:-1]]
                dst.append((sum(q[0] for q in P) / len(P), sum(q[1] for q in P) / len(P), pc, "osm"))
            continue
        if hw in SKIP_HW or tg.get("area") == "yes" or "building" in tg or len(refs) < 2:
            continue
        walk = _walk_ok(tg)
        cf, cb = _car_dirs(tg)
        if not (walk or cf or cb):
            continue
        v = _speed(tg)
        n_sp += v != URBAN
        prev = None
        for r in refs:
            nid = int(r)
            if nid not in xy:
                xy[nid] = to_s(*ll[r])
            if prev is not None and prev != nid:
                segs.append(dict(a=prev, b=nid, walk=walk, cf=cf, cb=cb, v=v, name=tg.get("name") or u"", hw=hw))
            prev = nid
    for s in segs:
        s["L"] = math.hypot(xy[s["b"]][0] - xy[s["a"]][0], xy[s["b"]][1] - xy[s["a"]][1])
    log.append(u"network: %d street pieces from OSM (%d with an OSM maxspeed; else %.0f km/h)" % (len(segs), n_sp, URBAN))
    n_pl = 0
    if os.path.isfile(plc):
        with open(plc, encoding="utf-8") as f:
            J = json.load(f)
        for ft in J.get("features", []):
            try:
                g, p = ft.get("geometry") or {}, ft.get("properties") or {}
                if g.get("type") != "Point" or (p.get("confidence") or 0.0) < 0.45:
                    continue
                tx = p.get("taxonomy") or {}
                if isinstance(tx, str):
                    tx = json.loads(tx)
                cat = place_cat(tx.get("hierarchy") or [], p.get("basic_category"))
                if cat:
                    x, y = to_s(*g["coordinates"][:2])
                    if not any(d[2] == cat and d[3] == "osm" and abs(d[0] - x) <= 10 and abs(d[1] - y) <= 10 and
                               math.hypot(d[0] - x, d[1] - y) <= 10.0 for d in dst):
                        dst.append((x, y, cat, "overture"))
                        n_pl += 1
            except Exception:
                continue
    else:
        log.append(u"FLAG: %s not found: destinations from OSM only" % plc)
    org = [(sum(q[0] for q in R) / len(R), sum(q[1] for q in R) / len(R)) for R, fab, com, s_, nm in C["bld"] if R]
    log.append(u"origins: %d MapBase buildings; destinations: %d (%d Overture places, the rest OSM): %s" % (
        len(org), len(dst), n_pl, u", ".join(u"%s %d" % (c_, sum(1 for d in dst if d[2] == c_))
                                            for c_ in sorted(set(d[2] for d in dst)))))
    walk = [i for i, s in enumerate(segs) if s["walk"]]
    car = [i for i, s in enumerate(segs) if s["cf"] or s["cb"]]
    wn = set(n for i in walk for n in (segs[i]["a"], segs[i]["b"]))
    cn = set(n for i in car for n in (segs[i]["a"], segs[i]["b"]))
    dd = [(d[0], d[1]) for d in dst]
    o_w, f1 = snap(org, xy, wn, SNAP)
    d_w, f2 = snap(dd, xy, wn, SNAP)
    o_c, f3 = snap(org, xy, cn, SNAP)
    d_c, f4 = snap(dd, xy, cn, SNAP)
    log.append(u"attached within %.0f m: walking %d / %d, driving %d / %d (too far: %d %d %d %d)" % (
        SNAP, sum(o_w.values()), sum(d_w.values()), sum(o_c.values()), sum(d_c.values()), f1, f2, f3, f4))
    Vw = potential(segs, walk, o_w, d_w, False, u"walking", log)
    Vc = potential(segs, car, o_c, d_c, True, u"driving", log)
    b = D["box"]
    inside = lambda s: b[0] <= (xy[s["a"]][0] + xy[s["b"]][0]) / 2.0 <= b[2] and \
        b[1] <= (xy[s["a"]][1] + xy[s["b"]][1]) / 2.0 <= b[3]
    ins = [i for i, s in enumerate(segs) if inside(s)]
    mw = max([Vw.get(i, 0) for i in ins] or [0]) or 1
    mc = max([Vc.get(i, 0) for i in ins] or [0]) or 1
    R = {"version": MV_ENGINE, "made": time.strftime("%Y-%m-%d %H:%M"), "max_walk_pairs": mw, "max_car_pairs": mc,
         "method": u"routes buildings -> everyday destinations, 800 m on foot (flat), 600 s by car; index 100 = "
                   u"busiest piece in the frame",
         "pieces": [[round(xy[segs[i]["a"]][0], 2), round(xy[segs[i]["a"]][1], 2), round(xy[segs[i]["b"]][0], 2),
                     round(xy[segs[i]["b"]][1], 2), round(100.0 * Vw.get(i, 0) / mw, 2),
                     round(100.0 * Vc.get(i, 0) / mc, 2), segs[i]["name"], segs[i]["hw"]] for i in ins],
         "dest": [[round(d[0], 1), round(d[1], 1), d[2]] for d in dst if b[0] <= d[0] <= b[2] and b[1] <= d[1] <= b[3]]}
    os.makedirs(os.path.dirname(MV_FILE), exist_ok=True)
    with open(MV_FILE, "w", encoding="utf-8") as f:
        json.dump(R, f, ensure_ascii=False, separators=(",", ":"))
    log.append(u"movement cache: %s (%d pieces in the frame; index 100 = %d walking / %d driving route pairs)" % (
        MV_FILE, len(R["pieces"]), mw, mc))
    return R


def cls_of(v):
    for i, c in enumerate(CLS):
        if v <= c:
            return i
    return len(CLS) - 1


def main():
    t0 = time.time()
    log = []
    G = load_common()
    lib = G["pc_lib"](log)
    D = G["pc_data"](log)
    K = D["key"]
    den = int(globals().get("scale") or 0)
    page = tuple(globals().get("page_mm") or G["PC_A3"])     # v1.3: A3, or the slide sheet's panel
    # v1.5: site_alan strip along the page top; the legend columns the page height needs (measured with a stand-in
    # legend of the same rows: 4 headers, 4 + 4 classes, 3 places, study area, the notes)
    class _Dry(object):
        pass
    dry = _Dry()
    dry.box, dry.k, dry.den = (0.0, -5000.0, 0.0, 0.0), 1.0, 1000.0
    nul = lambda x, y: []
    stand = ([(None, u"ROUTES FROM HOMES TO EVERYDAY PLACES"), (None, u"BAND = ON FOOT, 800 m; LINE BESIDE IT = BY CAR, 10 min")] +
             [(nul, u"index 50-100: 9999 pieces on foot, 9999 by car")] * 4 +
             [(None, u"WHERE PEOPLE GO (SHOPS: SEE PLAN 01)")] +
             [(nul, u"%s (999)" % w_) for k_, w_, c_, sh_ in KINDS] +
             [(None, u"OUR NODES"), (nul, u"N1-N6: the six nodes of the proposal")])   # v1.26: node row
    note_s = [u"Index 100 = the street piece the most routes use inside the frame, per mode (walking 9,999,999, driving "
              u"9,999,999 route pairs). Routes: every building to every everyday place; walking on flat ground, driving "
              u"at the speed limits, else 50 km/h."]
    # v1.10: the map across the whole page width, the legend in as many columns as fit across, under it
    SW = G["PC_SIDE_MM"]
    ncol = max(1, min(2, int((page[0] - 24.0 + 6.0) // (SW + 6.0))))   # v1.12: 2 columns keep the groups whole
    ys = [it[3] for it in G["pc_sheet"](dry, K, lib, TITLE, SUB, stand, note_s, u"", cols=ncol)
          if it[0] == "text" and it[8] in ("title", "legend", "notes")]
    hl = -min(ys) + 3.0                                  # the legend block's height (title to the last line)
    NB = 50.0                                            # north + scale under the legend
    M = G["pc_site_map"](1000.0, [])
    if den <= 0:
        dw = M.F.w * 1000.0 / (page[0] - 24.0)
        dh = M.F.h * 1000.0 / max(page[1] - 24.0 - 8.0 - hl - NB, 10.0)
        den = int(math.ceil(dw / 500.0) * 500)          # v1.13: the width alone (edge to edge)
    M = G["pc_site_map"](den, log)
    M.x0 = 12.0
    M.y0 = page[1] - 12.0 - M.mh                         # the map along the page top, edge to edge
    M.box = (M.x0, M.y0, M.x0 + M.mw, M.y0 + M.mh)
    M.w, M.h = page
    if M.y0 - 8.0 - hl - NB < 12.0 - 0.5:                # v1.13: the page grows down (no FLAG: the slide fits by ink)
        M.h = page[1] + (12.0 - (M.y0 - 8.0 - hl - NB))
        dy_ = M.h - page[1]
        M.y0 += dy_
        M.box = (M.x0, M.y0, M.x0 + M.mw, M.y0 + M.mh)
        page = (page[0], M.h)
        log.append(u"page grown %.0f mm down for the legend" % dy_)
    log.append(u"layout: map %.0f x %.0f mm at 1:%s across the page, legend %d column(s) under it"
               % (M.mw, M.mh, format(int(M.den), ",d"), ncol))
    MB, C = G["pc_mb_data"](log)
    R = compute(lib, C, D, log)
    P_, L_, circle = G["P_"], G["L_"], G["circle"]
    tm, INK = K["text_mm"], K["ink"]
    T = M.T

    # ---- the base: MapBase quiet; buildings with shops in the shop colour (each fact once: shops ARE the buildings)
    MBS = G["pc_mb_lib"](log)["MB_STYLE"]                # v1.14: the fabric reads again under the routes
    fab_ = dict((k_, "D3CFC6") for k_ in MBS["fab"])
    fab_c = dict((k_, "D3CFC6") for k_ in MBS["fab_com"])
    for k_ in ("monument", "sacred"):
        fab_[k_] = fab_c[k_] = "D9C6B8"
    base_st = {"fab": fab_, "fab_com": fab_c, "ground": "F3F1EB", "ink": "A8A398", "edge_dark": 0.35,
               "water_hatch": None}
    items, mb_rows, cnt = G["pc_mapbase"](M, K, log, None, base_st)     # v1.1: shops shown once, on Page02

    # ---- walking bands (under), driving lines (on top), by class; low classes first
    P = [p_ for p_ in R["pieces"] if M.inside(T(((p_[0] + p_[2]) / 2.0, (p_[1] + p_[3]) / 2.0)))]
    fw_ = max([p_[4] for p_ in P] or [0.0]) or 100.0     # v1.5: index 100 = the busiest piece INSIDE site_alan
    fc_ = max([p_[5] for p_ in P] or [0.0]) or 100.0
    P = [p_[:4] + [100.0 * p_[4] / fw_, 100.0 * p_[5] / fc_] + list(p_[6:]) for p_ in P]
    R = dict(R, max_walk_pairs=int(round(R["max_walk_pairs"] * fw_ / 100.0)),
             max_car_pairs=int(round(R["max_car_pairs"] * fc_ / 100.0)))
    log.append(u"site_alan: %d street pieces inside; index rescaled so its busiest piece = 100 (walking x %.2f, "
               u"driving x %.2f)" % (len(P), 100.0 / fw_, 100.0 / fc_))
    nw, nc = [0] * 5, [0] * 5
    # v1.24 (Aras 21:16 UTC "like how many total people use there and how"): width = ALL routes using the piece (on
    # foot + by car, in route pairs: home to everyday place, a relative use, not counted people), colour = how: the
    # share of those routes on foot
    wp_, cp_ = R["max_walk_pairs"] / 100.0, R["max_car_pairs"] / 100.0
    tot_ = lambda w, c: w * wp_ + c * cp_
    ft_ = max([tot_(p_[4], p_[5]) for p_ in P] or [1.0]) or 1.0
    def how(w, c):
        t_ = tot_(w, c)
        f_ = w * wp_ / t_ if t_ > 0 else 1.0
        return 0 if f_ >= 2.0 / 3.0 else 1 if f_ > 1.0 / 3.0 else 2
    nh = [0, 0, 0]
    for k_ in range(1, 5):
        for x1, y1, x2, y2, w, c, nm, hw in P:
            if cls_of(100.0 * tot_(w, c) / ft_) == k_:
                h_ = how(w, c)
                for run in M.clip([T((x1, y1)), T((x2, y2))]):
                    items.append(L_(run, WALK_C[k_], USE_W, "use_%d" % k_)[:4] + (G["PC_CLIP"],) +
                                 L_(run, WALK_C[k_], USE_W, "use_%d" % k_)[5:])
                nw[k_] += 1
                nh[h_] += 1
    log.append(u"lines (v1.25): one width; colour = all routes on the piece (on foot + by car, route pairs; index 100 = %s pairs), "
               u"share on foot, log only (2/3 or more / between / 1/3 or less): %d / %d / %d pieces; classes %s" % (
                   format(int(round(ft_)), ",d"), nh[0], nh[1], nh[2], nw[1:]))
    def beside(a, b, w, k_):                             # v1.15: the driving line beside the walking band
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = (dx * dx + dy * dy) ** 0.5 or 1.0
        nx, ny = -dy / L, dx / L
        if ny < 0 or (ny == 0 and nx < 0):               # always the same side of the street (page north / east)
            nx, ny = -nx, -ny
        d = WALK_W[cls_of(w)] / 2.0 + 0.35 + CAR_W[k_] / 2.0
        return [(a[0] + nx * d, a[1] + ny * d), (b[0] + nx * d, b[1] + ny * d)]
    for k_ in CAR_SHOWN:                                 # v1.21: main roads only (the two upper classes)
        for x1, y1, x2, y2, w, c, nm, hw in P:
            if cls_of(c) == k_:
                for run in M.clip(beside(T((x1, y1)), T((x2, y2)), w, k_)):
                    items.append(L_(run, CAR_C, CAR_W[k_], "driving_%d" % k_, CAR_D[k_])[:4] + (G["PC_CLIP"],) +
                                 L_(run, CAR_C, CAR_W[k_], "driving_%d" % k_, CAR_D[k_])[5:])
                nc[k_] += 1
    log.append(u"drawn: walking pieces by class %s; driving %s" % (nw[1:], nc[1:]))

    # ---- everyday destinations other than shops (shops are the coloured buildings)
    def mark(shape, x, y, r=1.0):                        # v1.4: one shape per kind of place
        if shape == "diamond":
            return [(x, y - 1.3 * r), (x + 1.3 * r, y), (x, y + 1.3 * r), (x - 1.3 * r, y)]
        if shape == "square":
            return [(x - 0.9 * r, y - 0.9 * r), (x + 0.9 * r, y - 0.9 * r), (x + 0.9 * r, y + 0.9 * r),
                    (x - 0.9 * r, y + 0.9 * r)]
        if shape == "triangle":
            return [(x - 1.1 * r, y - 0.8 * r), (x + 1.1 * r, y - 0.8 * r), (x, y + 1.1 * r)]
        if shape == "cross":
            a, b = 0.35 * r, 1.05 * r
            return [(x - a, y - b), (x + a, y - b), (x + a, y - a), (x + b, y - a), (x + b, y + a), (x + a, y + a),
                    (x + a, y + b), (x - a, y + b), (x - a, y + a), (x - b, y + a), (x - b, y - a), (x - a, y - a)]
        return circle(x, y, r, 16)
    lab = G["Labels"](M, lib)
    nd = {}
    KD = dict((k_, (w_, c_, m_)) for k_, w_, c_, m_ in KINDS)
    for x, y, cat, src_ in read_kinds(lib, D["box"], log):   # v1.16: drawn by kind (Aras 13:36 UTC)
        q = T((x, y))
        if not M.inside(q, 1.0):
            continue
        items.append(P_([mark(KD[cat][2], q[0], q[1])], KD[cat][1], "1F1F1F", 0.15, "dest_" + cat)[:9] +
                     (G["PC_CLIP"],))      # v1.11: cut to the frame
        nd[cat] = nd.get(cat, 0) + 1
    # ---- names of the busiest named streets on foot (each name once, at its busiest piece)
    best = {}
    for x1, y1, x2, y2, w, c, nm, hw in P:
        if nm and (nm not in best or w > best[nm][0]):
            best[nm] = (w, ((x1 + x2) / 2.0, (y1 + y2) / 2.0))
    for nm, (w, q) in sorted(best.items(), key=lambda kv: -kv[1][0])[:N_NAMES]:
        if M.inside(T(q), 5.0):
            lab.put(nm, T(q), tm["small"] * 1.35, INK, "street_names", False, gap=2.0, halo=False)
    items += lab.items
    # ---- v1.26: our nodes as pins (as Page01Free v1.20), drawn last so nothing covers them
    try:
        with open(os.path.join(BERGAMA_ROOT, "Data", "section_lines.json"), encoding="utf-8") as f:
            NODES = json.load(f)["nodes"]
    except Exception as ex:
        NODES = {}
        log.append(u"FLAG: no node pins (Data/section_lines.json: %s)" % ex)
    try:                                                 # the working area (Basemap study area rings)
        with open(os.path.join(G["pc_root"](), G["PC_STUDY_CACHE"]), encoding="utf-8") as f:
            CAL = [[tuple(p) for p in R_] for R_ in (json.load(f).get("calisma") or [])]
    except Exception as ex:
        CAL = []
        log.append(u"FLAG: no working area for the node pins (%s): pins at the frame middles" % ex)
    for nk in sorted(NODES):
        cs = NODES[nk]["corners"]
        q = M.T((sum(c[0] for c in cs) / len(cs), sum(c[1] for c in cs) / len(cs)))
        parts = [Q_ for Q_ in (clip_convex(R_, [tuple(c) for c in cs]) for R_ in CAL) if len(Q_) >= 3]
        parts = [Q_ for Q_ in parts if abs(sum(Q_[i - 1][0] * Q_[i][1] - Q_[i][0] * Q_[i - 1][1]
                                               for i in range(len(Q_)))) / 2.0 > 50.0]
        if CAL and not parts:
            log.append(u"FLAG node %s: its frame does not reach into the working area: pin at the frame middle" % nk)
        if parts:
            big = max(parts, key=lambda Q_: abs(sum(Q_[i - 1][0] * Q_[i][1] - Q_[i][0] * Q_[i - 1][1]
                                                    for i in range(len(Q_)))))
            ip = inner_point(big)
            if ip:
                q = M.T(ip)
        ys = []                                          # v1.27: the working area's edges across the strip at q's x
        for R_ in CAL:
            Rm = [M.T(p) for p in R_]
            for i in range(len(Rm)):
                (x1, y1), (x2, y2) = Rm[i - 1], Rm[i]
                if (x1 > q[0]) != (x2 > q[0]):
                    ys.append(y1 + (q[0] - x1) * (y2 - y1) / (x2 - x1))
        ys.sort()
        spans = [(ys[i], ys[i + 1]) for i in range(0, len(ys) - 1, 2)]
        if spans:
            inn = [sp for sp in spans if sp[0] <= q[1] <= sp[1]]
            a_, b_ = inn[0] if inn else max(spans, key=lambda sp: sp[1] - sp[0])
            q = (q[0], (a_ + b_) / 2.0)
            log.append(u"node %s: pin in the middle of the working area across the strip (%.1f mm wide there)"
                       % (nk, b_ - a_))
        else:
            log.append(u"FLAG node %s: the working area does not cross its place along the strip: pin left as it was" % nk)
        if not M.inside(q):
            log.append(u"node %s lies outside site_alan: no pin" % nk)
            continue
        items += pin(q, nk, P_, None, circle, M.box, G["PC_CLIP"], tc=G["pc_text_c"])
    log.append(u"node pins: %s" % u", ".join(sorted(NODES)))
    # v1.22 (Aras 21:09 UTC "remove these dashed and solid thin lines"): no working-area line on this diagram

    # ---- legend
    def cls_txt(i):
        return u"index %d-%d" % (0 if i == 0 else CLS[i - 1], CLS[i])
    def pair(i):                                         # v1.6: the walking band with the driving line beside it
        d_ = WALK_W[i] / 2.0 + 0.35 + CAR_W[i] / 2.0       # v1.15: the line beside the band, as on the map
        return lambda x, y: [L_([(x - 4.5, y), (x + 4.5, y)], WALK_C[i], WALK_W[i], "legend")] + (
            [L_([(x - 4.5, y + d_), (x + 4.5, y + d_)], CAR_C, CAR_W[i], "legend", CAR_D[i])] if i in CAR_SHOWN else [])
    legend = [(None, u"HOW MUCH: ALL ROUTES FROM HOMES TO EVERYDAY PLACES"),
              (None, u"ON FOOT 800 m + BY CAR 10 min (RELATIVE USE, NOT COUNTED PEOPLE)")]
    legend += [((lambda x, y, i=i: [L_([(x - 4.5, y), (x + 4.5, y)], WALK_C[i], 2.4, "legend")]),   # v1.25: colour step
                u"%s%s: %d pieces" % (cls_txt(i), u" (most use)" if i == 4 else u" (least use)" if i == 1 else u"",
                                       nw[i])) for i in range(4, 0, -1)]
    legend += [(None, u"OUR NODES"), (lambda x, y: pin((x, y - 3.2), u"N1", P_, None, circle, layer="legend",
                                                       tc=G["pc_text_c"]), u"N1-N6: the six nodes of the proposal")]   # v1.26
    legend += [(None, u"WHERE PEOPLE GO (SHOPS: SEE PLAN 01)")]
    legend += [(lambda x, y, c_=c_, sh_=sh_: [P_([mark(sh_, x, y)], c_, "1F1F1F", 0.15, "legend")],
                u"%s (%d)" % (w_, nd.get(k_, 0))) for k_, w_, c_, sh_ in KINDS]
    notes = [u"Index 100 = the street piece the most routes use inside the frame, per mode (walking %s, driving %s "
             u"route pairs). Routes: every building to every everyday place; walking on flat ground, driving at the "
             u"speed limits, else %.0f km/h." % (
                 format(R["max_walk_pairs"], ",d"), format(R["max_car_pairs"], ",d"), URBAN)]
    credit = u""                                         # v1.2: no sources in the drawing (Aras 15:23 UTC)
    log.append(u"sources (log only): OpenStreetMap (ODbL) streets, speed limits, one-way, places; Overture Maps places "
               u"(CDLA Permissive 2.0); MapBase buildings; method selinus_board v67 movement potential; classes as "
               u"SUBMISSION_SON p7")
    class _Col(object):                                  # v1.10: the legend block under the map (pc_sheet: x = box[2] + 8)
        pass
    Mc = _Col()
    ytop = M.y0 - 8.0
    Mc.box, Mc.den, Mc.k = (0.0, ytop - hl - NB, M.x0 - 8.0, ytop), M.den, M.k
    items += [it for it in G["pc_sheet"](Mc, K, lib, TITLE, SUB, legend, notes, credit,
                                         north=G["pc_north_deg"](M.north), cols=ncol)
              if not (it[0] == "poly" and it[6] == "frame")]
    items.append(P_([[(M.box[0], M.box[1]), (M.box[2], M.box[1]), (M.box[2], M.box[3]), (M.box[0], M.box[3])]], None,
                    INK, 0.25, "frame"))
    items = thin_lines(items, G["pc_stroke_k"](M.box[2] - M.box[0], M.box[3] - M.box[1], log, NAME))   # v1.20
    G["pc_write"](lib, M, items, OUT_DIR, NAME, u"How people use the streets, 1:%d" % M.den, log)
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
