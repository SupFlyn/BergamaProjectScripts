# -*- coding: utf-8 -*-
"""Bergama Group 6: NODE N2 v1 (14 Nov 2026): Panel Review II slide 8, node N2 "Cultural Heritage" in detail, one A3 page.
One script per node (Aras 14 Nov 11:14 UTC: "dont build all those nodes into single script"); the shared drawing code is
Data/bergama_nodes_common.py (read its header for what is drawn and where every element comes from):
plan of the node (urban fabric, streets, the Selinos, bus lines and stops, hubs, heritage loop, the city square idea
where a heritage loop stop and a bus stop share the node), sections N2-A and N2-B (the Sections script's code),
land use of the node frame, water over the bed by season at both cuts, what the cuts meet, a perspective placeholder.
Change this node's words in INTRO below; everything else is shared.

Outputs (Downloads/Bergama/output/bergama_node_n2/): N2_slide8.pdf (layers) + review/ PNGs.
Run it in Bergama_Altlik.3dm (the sections read the survey layers); press Basemap once before (its cache).
Grasshopper: a Button on any input runs it.
"""
import os, time

VERSION = "v1"
GH_LABEL = "NodeN2"
OUT_FOLDER = "bergama_node_n2"
LOG_NAME = "bergama_node_n2_log.txt"
GH_INPUTS = {}
COMMON = os.path.join("Data", "bergama_nodes_common.py")
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
NODE, SLIDE = "N2", 8
INTRO = (u"Cultural Heritage: the node today in plan, its two cuts across the Selinos and the water at each. The levels show "
         u"which ground the water leaves dry in each season, the ground the stepped, amphibious bed of the design idea "
         u"would give to people one terrace at a time.")


def main():
    log = []
    p = os.path.join(BERGAMA_ROOT, COMMON)
    if not os.path.isfile(p):
        raise RuntimeError(u"%s missing: run Bergama.bat once (the kit copies it), then press again" % p)
    ns = {"__name__": "bergama_nodes_common"}
    with open(p, encoding="utf-8") as f:
        exec(compile(f.read(), p, "exec"), ns)
    log.append(u"common: %s (%s)" % (p, ns.get("NC_VERSION")))
    res = ns["node_page"](dict(NODE=NODE, SLIDE=SLIDE, OUT_FOLDER=OUT_FOLDER, NAME=u"%s_slide%d" % (NODE, SLIDE),
                               INTRO=INTRO), log)
    return u"%s\n%s %s" % (res, GH_LABEL, VERSION)


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
