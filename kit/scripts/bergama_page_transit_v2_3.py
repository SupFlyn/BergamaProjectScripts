# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE TRANSIT v2.3 (14 Nov 2026; v2.3 = run 2 review: Bergama Garajı still two squares (50 m merge); v2.2 v2.2 = brief plan rules as the node pages: the legend in
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
  hubs         K4, K3, T, K5, K6 as code tiles (the hub cards' codes); a dotted walking link from each hub to its stop(s)
               and from the gondola to the nearest stop with a town line, with straight-line metres (calculated)
  spine        the streamside spine K4 -> K5 along the Selinos (OSM line), as on p09
  heritage     the heritage places as small red dots with names, no numbers (the numbers belong to the heritage page)
Not drawn: metro, tram, train (Bergama has none; the nearest rail is İZBAN at Aliağa, line 835), ridership (none found).

Outputs (Downloads/Bergama/output/bergama_page_transit/): Transit.pdf (vector, layers), Transit.svg, review/ PNGs
(Aras 14 Nov 10:44: "all scripts should produce PNG's aswell which should be optimized for your viewing").
Reads: Data/bergama_access_heritage.json, Data/bergama_pages_common.py, Data/bergama_osm.osm, the newest
scripts/bergama_basemap_v*.py (PDF/SVG writer) and cached/bergama_basemap/basemap_layers.json (study area; press
Basemap once). Grasshopper: a Button on any input runs it; input `scale` (default from the data file, 1:2,500).
"""
import os, time

VERSION = "v2.3"
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


def main():
    t0 = time.time()
    log = []
    G = load_common()
    lib = G["pc_lib"](log)
    D = G["pc_data"](log)
    K = D["key"]
    den = int(globals().get("scale") or K["scale"])
    M = G["Map"](D, den)
    T, L_, P_, T_, circle, dist = M.T, G["L_"], G["P_"], G["T_"], G["circle"], G["pc_dist"]
    INK, tm = K["ink"], K["text_mm"]
    C = G["pc_context"](M, D, log)
    items = G["pc_context_items"](M, C, K)
    items += G["pc_study"](M, K, log)
    lab = G["Labels"](M, lib)

    # the streamside spine K4 -> K5 along the Selinos
    sp = G["pc_selinos"](C, D["hubs"]["K4"], D["hubs"]["K5"])
    if sp:
        Q = [T(p) for p in sp]
        items.append(L_(Q, "FFFFFF", K["spine_w"] + 0.8, "spine"))
        items.append(L_(Q, K["spine"], K["spine_w"], "spine"))
        items.append(G["arrow_head"](Q[1], Q[0], K["spine"], 2.6, "spine"))
        items.append(G["arrow_head"](Q[-2], Q[-1], K["spine"], 2.6, "spine"))
        log.append(u"spine: K4 -> K5 along the Selinos, %.0f m" % sum(dist(a, b) for a, b in zip(sp, sp[1:])))
    else:
        log.append(u"FLAG: the Selinos line of the OSM extract does not reach K4 and K5 within 80 m: no spine drawn")

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
    stop_q = {}
    for name, xy, lines in groups:
        q = T(xy)
        if not M.inside(q):
            continue
        stop_q.setdefault(name, []).append((q, xy, lines))
        gs = [g for g in order if any(G["pc_group_of"](D, r) == g for r in lines)]
        sc = K["lines"][gs[0]][0] if gs else K["stop_line"]
        hub = name in hub_stop_names
        r = K["hub_stop_r"] if hub else K["stop_r"]
        items.append(P_([circle(q[0], q[1], r, 24)], "FFFFFF", INK if hub else sc, 0.45 if hub else 0.3, "bus_stops"))
        lab.block_pt(q, r + 0.4)

    # heritage places: red dots, names, no numbers (v2.1: drawn before the hub tiles, so a tile is never covered)
    her = [(h["name"], h["xy"]) for h in D["heritage"]] + [(u"Akropol", D["akropol"])] + \
          [(h["name"], h["xy"]) for h in D.get("heritage_dots", [])]
    for nm, xy in her:
        q = T(xy)
        if M.inside(q):
            items.append(P_([circle(q[0], q[1], 0.8, 16)], K["heritage"], None, 0.0, "heritage_places"))
            lab.block_pt(q, 1.0)

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
        town = [(dist(lower["xy"], xy), nm, xy) for nm, v in stop_q.items() for (_q, xy, ln) in v
                if any(G["pc_group_of"](D, r) in ("town", "656") for r in ln)]
        if town:
            d_, nm, xy = min(town)
            links.append(("Teleferik", nm, lower["xy"], xy, d_))
    yg = next((s for s in D["stations"] if s["kind"] == "bus_station" and u"Yıldız" in (s["name"] or u"")), None)
    if yg:
        links.append(("T", yg["name"], D["hubs"]["IST"], yg["xy"], dist(D["hubs"]["IST"], yg["xy"])))
    for code, nm, a, b, d_ in links:
        qa, qb = T(a), T(b)
        if dist(qa, qb) < 1.0:
            continue
        items.append(L_([qa, qb], K["walk_link"], 0.35, "walking_links", (0.6, 0.5)))
        mid = ((qa[0] + qb[0]) / 2.0, (qa[1] + qb[1]) / 2.0)
        lab.put(u"%d m" % round(d_, -1 if d_ >= 100 else 0), mid, tm["small"], K["walk_link"], "walking_links_text",
                gap=0.8)
        log.append(u"walking link: %s -> %s %.0f m (straight line)" % (code, nm, d_))
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
            items.append(T_(code, q[0], q[1] - tm["label"] * 0.36, tm["label"], "FFFFFF", "hubs", True, "C"))
            lab.block_pt(q, s_ / 2 + 0.4)

    # names, most important first: hub stops, stations, other stops, heritage (the hubs' names are in the legend)
    for name, v in stop_q.items():
        for q, xy, lines in v:
            ref = sorted(lines, key=lambda r: (len(r), r))
            hub = name in hub_stop_names
            off = next((fx["official_name"] for fx in D.get("official_fixes", []) if fx["name"] == name and
                        fx.get("official_name")), None)
            nm_ = name + (u" (ESHOT: %s)" % off if off else u"")
            lab.put(u"%s · %s" % (nm_, u" ".join(ref)) if hub else nm_, q, tm["label"] if hub else tm["small"],
                    INK, "stop_names", hub, gap=1.8)
    for s in D["stations"]:
        q = T(s["xy"])
        if M.inside(q) and s.get("name"):
            nm = s["name"].replace(u"Akropolis Teleferik - ", u"Teleferik, ").replace(u" ( ", u" (").replace(u" )", u")")
            lab.put(nm, q, tm["label"], K["cable"] if s["kind"] == "gondola" else K["station"], "station_names", True)
    named = set(stop_q) | set(D["hub_names"].values()) | {u"Teleferik"}
    for nm, xy in her:                                    # a heritage place named by its stop or hub: not twice
        if nm not in named and M.inside(T(xy)):
            lab.put(nm, T(xy), tm["label"] if nm == u"Akropol" else tm["small"], K["heritage"], "heritage_names",
                    nm == u"Akropol", gap=1.2)
    items += lab.items
    if lab.forced:
        log.append(u"names with no free place (printed on the right of their point): %s" % u", ".join(lab.forced))

    # legend, notes, title
    def sw_line(col, w, dash=None):
        return lambda x, y: [L_([(x - 4.5, y), (x + 4.5, y)], col, w, "legend", tuple(dash) if dash else None)]

    def sw_sq(fill, stroke, lw, s_=3.0, code=None, tc="FFFFFF"):
        def f(x, y):
            it = [P_([[(x - s_ / 2, y - s_ / 2), (x + s_ / 2, y - s_ / 2), (x + s_ / 2, y + s_ / 2),
                       (x - s_ / 2, y + s_ / 2)]], fill, stroke, lw, "legend")]
            if code:
                it.append(T_(code, x, y - 0.8, 2.2, tc, "legend", True, "C"))
            return it
        return f
    LN = D["lines"]
    # v2.2 (brief plan rules, as the node pages, PR #176): EXISTING kept apart from the PROPOSAL marks (orange)
    legend = [(None, u"EXISTING: PUBLIC TRANSPORT")]
    legend += [(sw_line(K["lines"][g][0], K["lines"][g][1], K["lines"][g][2]),
                u"%s: %s a weekday (ESHOT)" % (LN[g]["word"], LN[g]["per_weekday"])) for g in order]
    legend += [
        (lambda x, y: [P_([circle(x, y, K["hub_stop_r"], 24)], "FFFFFF", INK, 0.45, "legend")],
         u"bus stop at a hub, with its lines (OSM; ESHOT where they differ)"),
        (lambda x, y: [P_([circle(x, y, K["stop_r"], 24)], "FFFFFF", K["stop_line"], 0.3, "legend")],
         u"other bus stop (OSM), ring in the colour of its busiest line group"),
        (sw_sq("FFFFFF", K["station"], 0.45), u"bus station (OSM amenity=bus_station)"),
        (lambda x, y: G["ticked"]([(x - 4.5, y), (x + 4.5, y)], K["cable"], 0.35, 2.5, 0.9, "legend") +
         sw_sq(K["cable"], "FFFFFF", 0.2, 2.6)(x + 4.5, y), u"Teleferik (gondola) and its stations, OSM; dotted: on foot to Akropol"),
        (None, u"EXISTING: CONTEXT"),
        (lambda x, y: [P_([G["circle"](x, y, 0.8, 16)], K["heritage"], None, 0.0, "legend")],
         u"heritage place (numbered on the heritage loop page)"),
        (sw_line(K["water"][0], 1.4), u"Selinos and side streams (OSM centre lines); dashed: covered"),
        (sw_line(K["study"][0], K["study"][1], (2.4, 0.8)), u"study area"),
        (None, u"PROPOSAL MARKS"),
        (sw_line(K["spine"], K["spine_w"]), u"streamside spine, K4 to K5, along the Selinos"),
        (sw_line(K["walk_link"], 0.35, (0.6, 0.5)), u"on foot from a hub to its stop, straight-line metres (calculated)"),
    ]
    word = {"walk": u"walking hub", "transit": u"main transit hub", "gateway": u"gateway out of town"}
    for code in ("K4", "K3", "T", "K5", "K6"):           # one row per hub: what it is, its stop(s), lines, metres
        kd = D["hub_kind"][code]
        st = [u"%s %d m (%s)" % (nm, round(d_), u" ".join(sorted(pc_lines_of(G, D, nm), key=lambda r: (len(r), r))))
              for c_, nm, _a, _b, d_ in links if c_ == code and nm in stop_q]
        legend.append((sw_sq(K["hub"][kd], "FFFFFF", 0.3, 4.2, code),
                       u"%s = %s, %s; stop: %s" % (code, D["hub_names"][code], word[kd], u"; ".join(st) or u"none")))
    notes = [u"No metro, tram or train runs in Bergama. The nearest rail is İZBAN at Aliağa: line 835 runs there 44 times "
             u"each way a weekday, timed to İZBAN (ESHOT).",
             u"Line weight = buses a weekday. Where line groups share a road they run side by side.",
             u"Ridership by line or stop: none found. Which lines start at the bus stations is not in our sources."]
    credit = u"Sources: " + u"; ".join(D["sources"][k] for k in ("osm", "eshot")) + u". Distances: straight line, calculated."
    items += G["pc_sheet"](M, K, lib, u"Public transport round the spine",
                           u"Bus lines, stops, stations and the Teleferik, and how the hubs reach them on foot",
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
