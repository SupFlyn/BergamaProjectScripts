# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE HERITAGE v1.5 (14 Nov 2026; v1.5 = Aras 13:02 rule check, run 6 review: names kept off the loop, the Selinos and the study line (Labels.block_line); WorldCover off (its 10 m cells drew stair steps); v1.4 = Aras 13:02 UTC "make sure nothing repeats in the slides": the grey bus routes and stops are left out (the transit page draws them); v1.3 = run 4 review: the 2023 satellite cover ends inside this frame (x 29521, y 32880) and drew a straight seam west and north, so WorldCover alone (it covers the whole frame), fainter; v1.2 = Aras 12:16 UTC "update all maps to include every detail, and top of the map, data is missing": the context is the one MapBase (survey + OSM + satellite + contours), quiet look; v1.1 = legend in EXISTING / PROPOSAL groups as the node pages)
v1 (14 Nov 2026): the heritage loop, Teleferik to Asklepion, as one map (a page
script of the new set: one script per page, Aras 14 Nov 10:46 UTC). Redraws the heritage loop of selinus_board v67
(booklet p19, HER_STOPS: the loop order and its places) on the shared page frame.

Aras 14 Nov 10:45 UTC: the transit map and this map "should not collide with each other"; 10:51: "transit hubs and
heritage loop is two different slides". So this script and bergama_page_transit_v*.py share
Data/bergama_pages_common.py (one frame, one scale, one context, one key) and Data/bergama_access_heritage.json.
The shared key: RED = heritage only (the loop, its numbered places); the bus network is only quiet grey context here
(it is the transit page's subject); the Teleferik's ticked cable is the same symbol on both pages; the hub codes
(K4 ...) and the project's place numbers are not on this page, so a number here is always a loop stop.

What is drawn: the OSM context and the study area (as the transit page); bus routes thin grey, bus stops small grey
rings without names; the Teleferik cable and stations; the loop in red: 1 Teleferik -> 2 Kızıl Avlu -> 3 Tabak Köprüsü
-> (the stream walk along the Selinos) -> 4 Ulucami Önü Köprüsü -> 5 Arasta -> 6 Bergama Müzesi -> 7 Asklepion, and
from the upper station on foot to Akropol (dotted); each stop a red numbered circle with its name; Ulucami and
Tabaklar Hamamı as small red rings by stop 4. The side column lists the seven stops with one line each (the texts of
selinus_board v67 HER21_PLACES, public sources HER_SRC).

Outputs (Downloads/Bergama/output/bergama_page_heritage/): HeritageLoop.pdf, HeritageLoop.svg, review/ PNGs.
Reads: as the transit page. Grasshopper: a Button on any input runs it; input `scale` (default 1:2,500).
"""
import os, time

VERSION = "v1.5"
GH_LABEL = "PageHeritage"
OUT_FOLDER = "bergama_page_heritage"
LOG_NAME = "bergama_page_heritage_log.txt"
GH_INPUTS = {"scale": "int 1000..10000 = 2500"}
COMMON = os.path.join("Data", "bergama_pages_common.py")
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
NAME = "HeritageLoop"
# one line per stop: selinus_board v67 pages/p21_heritage.py HER21_PLACES "txt" (sources noted there; HER_SRC)
STOP_TXT = {"teleferik": u"cable car (2010): the loop starts here",
            "kizil_avlu": u"Hadrian's temple, built over the stream",
            "tabak_koprusu": u"Roman bridge: the stream walk starts",
            "ulucami_onu": u"bridge to Ulucami (mosque of 1398-99) and Tabaklar Hamamı",
            "arasta": u"bazaar of 1513; its hamam: Parchment Museum",
            "bergama_muzesi": u"museum of 1936: Pergamon's finds",
            "asklepion": u"healing sanctuary, 4th c. BC: the loop's end"}
AKROPOL_TXT = u"World Heritage hill city: the loop's goal, up by the Teleferik"


def load_common():
    p = os.path.join(BERGAMA_ROOT, COMMON)
    if not os.path.isfile(p):
        raise RuntimeError(u"%s missing: run Bergama.bat once (the kit copies it), then press again" % p)
    ns = {"__name__": "bergama_pages_common"}
    with open(p, encoding="utf-8") as f:
        exec(compile(f.read(), p, "exec"), ns)
    return ns


MB_LAYERS = {"ground", "areas", "parks", "contours", "streets", "water", "walls", "buildings", "bridges", "trees"}
# v1.3: MapBase layers drawn: all but "veg" (the 2023 satellite cover stops inside this frame: a seam)


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
    tm, RED = K["text_mm"], K["heritage"]
    MB = G["pc_mapbase"](M, K, log, MB_LAYERS, {"lc_light": 0.8})                      # v1.2: the one base map (every detail we have)
    items = MB[0]
    mb_rows = G["pc_mb_legend"]([r_ for r_ in MB[1] if u"WorldCover" not in r_[2]], K)   # v1.5: no WorldCover
    items += G["pc_study"](M, K, log)
    lab = G["Labels"](M, lib)

    # the Teleferik (same symbol as the transit page)
    st_g = [s for s in D["stations"] if s["kind"] == "gondola"]
    upper = next((s for s in st_g if u"Yukarı" in (s["name"] or u"")), None)
    for run in M.clip([T(p) for p in D["cable"]]):
        items += G["ticked"](run, K["cable"], 0.35, 2.5, 0.9, "gondola")
    for s in st_g:
        q = T(s["xy"])
        if M.inside(q):
            items.append(P_([[(q[0] - 1.4, q[1] - 1.4), (q[0] + 1.4, q[1] - 1.4), (q[0] + 1.4, q[1] + 1.4),
                              (q[0] - 1.4, q[1] + 1.4)]], K["cable"], "FFFFFF", 0.2, "gondola"))
            lab.block_pt(q, 1.8)

    # the loop: legs stop to stop; 3 -> 4 along the Selinos (the stream walk)
    H = sorted(D["heritage"], key=lambda h: int(h["n"]))
    W = K["heritage_w"]
    legs = []
    for a, b in zip(H, H[1:]):
        if (a["key"], b["key"]) == ("tabak_koprusu", "ulucami_onu"):
            sw = G["pc_selinos"](a["xy"], b["xy"])
            if sw:
                legs.append(("walk", sw))
                log.append(u"stream walk: Tabak Köprüsü -> Ulucami Önü along the Selinos, %.0f m" % sum(
                    dist(p, q) for p, q in zip(sw, sw[1:])))
                continue
            log.append(u"FLAG: the OSM Selinos line is over 80 m from stop 3 or 4: the stream walk is drawn straight")
        legs.append(("leg", [a["xy"], b["xy"]]))
    for kind, P in legs:
        Q = [T(p) for p in P]
        for run in M.clip(Q):
            items.append(L_(run, "FFFFFF", W + 0.6, "loop"))
            items.append(L_(run, RED, W + (0.6 if kind == "walk" else 0.0), "loop"))
            if kind == "walk":
                items.append(L_(run, "FFFFFF", 0.3, "loop", (1.2, 1.2)))
    if upper:
        for run in M.clip([T(upper["xy"]), T(D["akropol"])]):
            items.append(L_(run, RED, 0.5, "loop", (0.01, 1.0)))
    log.append(u"loop: %d stops, %d legs, %.0f m stop to stop (straight legs; the walk along the stream)" % (
        len(H), len(legs), sum(dist(p, q) for _k, P in legs for p, q in zip(P, P[1:]))))

    lab.block_items(items, ("loop", "study_area"))                # v1.5: names off these lines
    lab.block_line([T(p) for p in G["pc_selinos_line"]()], 2.5)       # v1.5: names off the stream

    # the stops: red numbered circles; Akropol a red ring; Ulucami and Tabaklar Hamamı small red rings
    R = K["heritage_r"]
    for h in H:
        q = T(h["xy"])
        if not M.inside(q):
            log.append(u"FLAG: stop %s %s lies outside the frame" % (h["n"], h["name"]))
            continue
        items.append(P_([circle(q[0], q[1], R, 32)], RED, "FFFFFF", 0.35, "loop_stops"))
        items.append(T_(h["n"], q[0], q[1] - tm["label"] * 0.36, tm["label"] + 0.2, "FFFFFF", "loop_stops", True, "C"))
        lab.block_pt(q, R + 0.4)
    qa = T(D["akropol"])
    items.append(P_([circle(qa[0], qa[1], R * 0.8, 32)], "FFFFFF", RED, 0.6, "loop_stops"))
    lab.block_pt(qa, R)
    for d_ in D.get("heritage_dots", []):
        q = T(d_["xy"])
        items.append(P_([circle(q[0], q[1], 1.0, 16)], "FFFFFF", RED, 0.4, "heritage_places"))
        lab.block_pt(q, 1.3)
    for h in H:
        lab.put(h["name"], T(h["xy"]), tm["label"], RED, "loop_names", True, gap=R + 1.0)
    lab.put(u"Akropol", qa, tm["label"], RED, "loop_names", True, gap=R + 0.6)
    for d_ in D.get("heritage_dots", []):
        lab.put(d_["name"], T(d_["xy"]), tm["small"], RED, "loop_names", gap=1.6)
    for s in st_g:
        if s.get("name") and u"Yukarı" in s["name"]:
            lab.put(u"Teleferik, upper station", T(s["xy"]), tm["small"], K["cable"], "station_names")
    items += lab.items
    if lab.forced:
        log.append(u"names with no free place (printed where they overlap least): %s" % u", ".join(lab.forced))

    # legend: the seven stops in order, then the symbols
    def stop_sw(n):
        return lambda x, y: [P_([circle(x, y, R, 32)], RED, "FFFFFF", 0.35, "legend"),
                             T_(n, x, y - tm["label"] * 0.36, tm["label"] + 0.2, "FFFFFF", "legend", True, "C")]
    # v1.1 (brief plan rules, as the node pages): EXISTING kept apart from the PROPOSAL (the loop, in red, its own colour)
    legend = [(None, u"EXISTING: HERITAGE PLACES, LOOP ORDER")]
    legend += [(stop_sw(h["n"]), u"%s: %s" % (h["name"], STOP_TXT.get(h["key"], u""))) for h in H]
    legend += [
        (lambda x, y: [P_([circle(x, y, R * 0.8, 32)], "FFFFFF", RED, 0.6, "legend")], u"Akropol: " + AKROPOL_TXT),
        (None, u"PROPOSAL: THE HERITAGE LOOP (RED)"),
        (lambda x, y: [L_([(x - 4.5, y), (x + 4.5, y)], "FFFFFF", W + 0.6, "legend"),
                       L_([(x - 4.5, y), (x + 4.5, y)], RED, W, "legend")], u"heritage loop, stop to stop"),
        (lambda x, y: [L_([(x - 4.5, y), (x + 4.5, y)], RED, W + 0.6, "legend"),
                       L_([(x - 4.5, y), (x + 4.5, y)], "FFFFFF", 0.3, "legend", (1.2, 1.2))],
         u"stream walk Tabak Köprüsü to Ulucami Önü, along the Selinos"),
        (lambda x, y: [L_([(x - 4.5, y), (x + 4.5, y)], RED, 0.5, "legend", (0.01, 1.0))],
         u"on foot from the Teleferik's upper station to Akropol"),
        (None, u"EXISTING: CONTEXT"),
    ] + mb_rows + [
        (lambda x, y: G["ticked"]([(x - 4.5, y), (x + 4.5, y)], K["cable"], 0.35, 2.5, 0.9, "legend"),
         u"Teleferik (gondola) and its stations, OSM"),
        (lambda x, y: [P_([circle(x, y, 1.0, 16)], "FFFFFF", RED, 0.4, "legend")], u"other heritage building"),
        (lambda x, y: [L_([(x - 4.5, y), (x + 4.5, y)], K["water"][0], 0.3, "legend")],
         u"Selinos (survey banks) and side streams (OSM), from MapBase"),
        (lambda x, y: [L_([(x - 4.5, y), (x + 4.5, y)], K["study"][0], K["study"][1], "legend", (2.4, 0.8))],
         u"study area"),
    ]
    notes = [u"Numbers = the loop's order (selinus_board v67, HER_STOPS). Legs are drawn straight from stop to stop; "
             u"they show the order, not the streets walked."]
    credit = (u"Sources: " + D["sources"]["osm"] + u"; places and texts: Wikipedia 'Pergamon', 'Bergama Acropolis "
              u"Gondola', 'Red Basilica', 'Bergama Museum'; UNESCO WHL 1457 and ICOMOS 2014; Kültür Envanteri; Visit "
              u"İzmir; KTB (as selinus_board v67 HER_SRC).")
    items += G["pc_sheet"](M, K, lib, u"The heritage loop", u"From the Teleferik to Asklepion, across the Selinos",
                           legend, notes, credit)
    G["pc_write"](lib, M, items, OUT_DIR, NAME, u"The heritage loop, 1:%d" % den, log)
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
