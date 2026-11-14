# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE01 MOVE v1.1 (14 Nov 2026; v1.1 = Aras 13:02 UTC "make sure nothing repeats in the slides": the shop buildings and the ground key are on Page02 (same slide), so here the base is plain MapBase with no shop colour and no ground key), slide 1 (analysis): how people use the streets, ONE map.
Redoes SUBMISSION_SON p7 ("How people use it": shops and everyday walks / pedestrian flow / vehicles, three maps) as one
drawing on the one MapBase, each piece of information once (Aras 14 Nov 12:36 UTC: "p7 we need to merge all those into
one single drawing. With colours diffrentiated ... informations shouldn't be repeated ... again using the latest
basemap"; 12:38 UTC: "if one scripts does that job cache it and make it usable by the next script").

Method (the movement potential of selinus_board v67 / bergama_movement v1, its route search copied unchanged): every
street piece of OpenStreetMap counts the shortest routes that pass along it, from every building (origins: all MapBase
buildings) to every everyday destination (Overture places with confidence 0.45+, OSM shops, offices, services, places
of worship, schools, bus stops) within 800 m on foot (flat ground) or 600 s by car (OSM maxspeed, else 50 km/h, one-way
streets kept). Index 100 = the busiest piece inside the frame, per mode. Walking and driving are the two layers of the
map: walking a wide warm band, driving a thin dark line on top; shops are the buildings MapBase marks with shops, offices
or workshops; everyday destinations other than shops are small symbols.

Outputs (Downloads/Bergama/output/bergama_page01_move/): StreetUse.pdf, StreetUse.svg, review/ PNGs; the cache
cached/bergama_movement/movement.json (every street piece with its walking and driving index) for later pages (slide 5).
The route search runs only when the cache is missing or older than the OSM file, MapBase cache or places file.
Reads: Data/bergama_pages_common.py (v3.5+), Data/bergama_access_heritage.json (frame), Data/bergama_osm.osm,
Data/bergama_places.geojson, the newest MapBase script and its cache. Grasshopper: a Button runs it; input scale.
"""
import os, time, math, json, heapq

VERSION = "v1.1"
GH_LABEL = "Page01Move"
OUT_FOLDER = "bergama_page01_move"
LOG_NAME = "bergama_page01_move_log.txt"
GH_INPUTS = {"scale": "int 1000..10000 = 2500"}
COMMON = os.path.join("Data", "bergama_pages_common.py")
PLACES = os.path.join("Data", "bergama_places.geojson")
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
MV_FILE = os.path.join(BERGAMA_ROOT, "cached", "bergama_movement", "movement.json")
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
NAME = "StreetUse"
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
WALK_W = (0.0, 0.7, 1.2, 1.8, 2.6)              # mm: walking band per class (class 0 not drawn)
WALK_C = ("F3E2CF", "EBC3A0", "D9926B", "B5583F", "8B2D2D")    # warm ramp to the palette's 8B2D2D
CAR_W = (0.0, 0.18, 0.3, 0.45, 0.65)            # mm: driving line per class
CAR_C = "1F2A30"
DEST = {"institutional": (u"Schools, health, civic offices", "5C7A86"), "religious": (u"Mosques, heritage places",
        "4C2528"), "transport": (u"Bus stops, bus station, car parks, fuel", "3C4733")}
MV_ENGINE = "v1"                                # the route search's version (the cache is reused while it holds)
N_NAMES = 8                                     # street names: the busiest named streets on foot


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
    den = int(globals().get("scale") or K["scale"])
    M = G["Map"](D, den)
    MB, C = G["pc_mb_data"](log)
    R = compute(lib, C, D, log)
    P_, L_, circle = G["P_"], G["L_"], G["circle"]
    tm, INK = K["text_mm"], K["ink"]
    T = M.T

    # ---- the base: MapBase quiet; buildings with shops in the shop colour (each fact once: shops ARE the buildings)
    items, mb_rows, cnt = G["pc_mapbase"](M, K, log)     # v1.1: shops shown once, on Page02
    items += G["pc_study"](M, K, log)

    # ---- walking bands (under), driving lines (on top), by class; low classes first
    P = R["pieces"]
    nw, nc = [0] * 5, [0] * 5
    for k_ in range(1, 5):
        for x1, y1, x2, y2, w, c, nm, hw in P:
            if cls_of(w) == k_:
                for run in M.clip([T((x1, y1)), T((x2, y2))]):
                    items.append(L_(run, WALK_C[k_], WALK_W[k_], "walking_%d" % k_))
                nw[k_] += 1
    for k_ in range(1, 5):
        for x1, y1, x2, y2, w, c, nm, hw in P:
            if cls_of(c) == k_:
                for run in M.clip([T((x1, y1)), T((x2, y2))]):
                    items.append(L_(run, CAR_C, CAR_W[k_], "driving_%d" % k_))
                nc[k_] += 1
    log.append(u"drawn: walking pieces by class %s; driving %s" % (nw[1:], nc[1:]))

    # ---- everyday destinations other than shops (shops are the coloured buildings)
    lab = G["Labels"](M, lib)
    nd = {}
    for x, y, cat in R["dest"]:
        if cat not in DEST:
            continue
        q = T((x, y))
        if not M.inside(q, 1.0):
            continue
        items.append(P_([circle(q[0], q[1], 0.75, 12)], DEST[cat][1], "FFFFFF", 0.15, "dest_" + cat))
        nd[cat] = nd.get(cat, 0) + 1
    # ---- names of the busiest named streets on foot (each name once, at its busiest piece)
    best = {}
    for x1, y1, x2, y2, w, c, nm, hw in P:
        if nm and (nm not in best or w > best[nm][0]):
            best[nm] = (w, ((x1 + x2) / 2.0, (y1 + y2) / 2.0))
    for nm, (w, q) in sorted(best.items(), key=lambda kv: -kv[1][0])[:N_NAMES]:
        if M.inside(T(q), 5.0):
            lab.put(nm, T(q), tm["small"], INK, "street_names", False, gap=2.0)
    items += lab.items

    # ---- legend
    def band(c_, w_):
        return lambda x, y: [L_([(x - 4.5, y), (x + 4.5, y)], c_, w_, "legend")]

    def cls_txt(i):
        return u"index %d-%d" % (0 if i == 0 else CLS[i - 1], CLS[i])
    legend = [(None, u"ON FOOT: ROUTES FROM HOMES TO EVERYDAY PLACES (800 M)")]
    legend += [(band(WALK_C[i], WALK_W[i]), u"%s (%d street pieces)" % (cls_txt(i), nw[i])) for i in range(4, 0, -1)]
    legend += [(None, u"BY CAR: THE SAME ROUTES WITHIN 10 MINUTES")]
    legend += [(band(CAR_C, CAR_W[i]), u"%s (%d street pieces)" % (cls_txt(i), nc[i])) for i in range(4, 0, -1)]
    legend += [(None, u"WHERE PEOPLE GO (SHOPS: ON THE SITE MAP)")]
    legend += [(lambda x, y, c_=c_: [P_([circle(x, y, 0.75, 12)], c_, "FFFFFF", 0.15, "legend")],
                u"%s (%d)" % (w_, nd.get(k_, 0))) for k_, (w_, c_) in sorted(DEST.items())]
    legend += [(None, u"EXISTING: CONTEXT (KEY ON THE SITE MAP)")] + [
        (lambda x, y: [L_([(x - 4.5, y), (x + 4.5, y)], K["study"][0], K["study"][1], "legend", (2.4, 0.8))],
         u"study area")]
    notes = [u"Index 100 = the street piece the most routes use inside the frame, per mode (walking %s, driving %s "
             u"route pairs). Routes: every building to every everyday place; walking on flat ground, driving at OSM "
             u"speed limits, else %.0f km/h. Classes as SUBMISSION_SON p7." % (
                 format(R["max_walk_pairs"], ",d"), format(R["max_car_pairs"], ",d"), URBAN)]
    credit = (u"Sources: © OpenStreetMap contributors (ODbL): streets, speed limits, one-way streets, places; Overture "
              u"Maps places (CDLA Permissive 2.0); MapBase buildings (survey, OSM, 2023 image). Method: selinus_board "
              u"v67 movement potential (bergama_movement v1).")
    items += G["pc_sheet"](M, K, lib, u"How people use the streets", u"Walking, driving and where people go, on one "
                           u"map", legend, notes, credit)
    G["pc_write"](lib, M, items, OUT_DIR, NAME, u"How people use the streets, 1:%d" % den, log)
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
