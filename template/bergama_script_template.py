# -*- coding: utf-8 -*-
"""Bergama Group 6: TEMPLATE for a new Grasshopper Python 3 script (25 Oct 2026). Rules: scripts/_template/SCRIPT_STANDARD.md.
Copy this file, rename it bergama_<subject>_v1.py, set the four lines under SETTINGS, write main(). Keep the rest as it is.

Component: Rhino 8 > Grasshopper > Python 3 Script, paste the whole file.
  input  run   Button (the script does nothing until it is pressed; any other True bool input also counts)
  output log   the last run's report (errors included)
  output done  "done HH:MM:SS.ss · N s" after a good run ("ERROR ..." after a failed one, "idle" before), kept until the
               next run: wire it into the next script's run for the one-click chain; each NEW done text fires that
               script once (add the output with the + on the component)
Text under the component: "<GH_LABEL> <VERSION> · HH:MM · N s" after a run, "· idle" before one, "· ERROR" on an error.
Files: reads data from ~/Downloads/Bergama/Data/, other scripts' results from ~/Downloads/Bergama/output/<their folder>/,
writes results to ~/Downloads/Bergama/output/<OUT_FOLDER>/, caches to ~/Downloads/Bergama/cached/<OUT_FOLDER>/ and ONE log
file to ~/Downloads/Bergama/logs/<LOG_NAME> (overwritten by each press). The panel keeps the last log for this Rhino
session only.
Sheets: VISUAL FIRST (SCRIPT_STANDARD.md §5b): pictograms, charts and callouts instead of sentences; keywords only where
something cannot be drawn; sources as [n] with one numbered key in the footer; legends as drawn samples.
"""
import os, time, json

# ---- SETTINGS (change these four) ----
VERSION = "v1"
GH_LABEL = "NewScript"                      # one CamelCase word, shown under the component
OUT_FOLDER = "bergama_new_script"           # folder name under output/ and cached/
LOG_NAME = "bergama_new_script_log.txt"     # file name in logs/ (no version in it)

# ---- folders (same in every script) ----
BERGAMA = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
DATA_DIR = os.path.join(BERGAMA, "Data")
OUT_DIR = os.path.join(BERGAMA, "output", OUT_FOLDER)
CACHE_DIR = os.path.join(BERGAMA, "cached", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA, "logs")
ANALYSIS_LAYER = "site_alan"                # analysis range (rectangle)
WORK_LAYER = "calisma_alan"                 # working area, one shared area
SNAP_M = 15.0                               # a proposal this close to calisma_alan counts as on it; nothing is cut


def data_file(name):
    """Downloads/Bergama/Data/<name> if it is there, else None (the script then uses its built-in copy or skips it)."""
    p = os.path.join(DATA_DIR, name)
    return p if os.path.isfile(p) else None


def read_result(folder, name):
    """Another script's results JSON from output/<folder>/<name>, or None if that script has not run yet."""
    try:
        with open(os.path.join(BERGAMA, "output", folder, name), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def layer_curves(layer_name):
    """Curves on a layer of the open Rhino file (Bergama_Altlik.3dm); [] outside Rhino or if the layer is missing."""
    try:
        import Rhino
        doc = Rhino.RhinoDoc.ActiveDoc
        idx = doc.Layers.FindByFullPath(layer_name, -1)
        if idx < 0:
            return []
        return [o.Geometry for o in doc.Objects.FindByLayer(doc.Layers[idx]) if isinstance(o.Geometry, Rhino.Geometry.Curve)]
    except Exception:
        return []


def chain_fire(v, key):
    """25 Oct 10:20 (one-click chain): the previous script's done output is a text "done HH:MM:SS.ss ..." that stays
    after the Button is released; each NEW text fires this script once (the Button still works as before)."""
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
    """The done output: kept until the next run (this Rhino session)."""
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


def main():
    """The script's work. Return the log text: one line per file written, with its time; nothing more.
    EXAMPLE body only: counts the two boundary layers and writes a small JSON. Replace it."""
    t0 = time.time()
    os.makedirs(OUT_DIR, exist_ok=True)
    res = {"site_alan_curves": len(layer_curves(ANALYSIS_LAYER)), "calisma_alan_curves": len(layer_curves(WORK_LAYER))}
    out = os.path.join(OUT_DIR, "results.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    return "%s  %s\n%s %s, %.1f s" % (out, time.strftime("%H:%M:%S"), GH_LABEL, VERSION, time.time() - t0)


# ---- Grasshopper wiring (same in every script; never define a function named run: it would hide the input) ----
if "ghenv" in globals():
    import scriptcontext as _sc
    _k = "bergama_" + OUT_FOLDER
    try:
        _k += ":" + str(ghenv.Component.InstanceGuid)   # each component copy keeps its own log and done  # noqa: F821
    except Exception:
        pass
    _pressed = any(v is True for k, v in list(globals().items())
                   if not k.startswith("_") and isinstance(v, bool) and k not in ("True", "False", "rhino_bake", "done")) or \
        any(chain_fire(v, _k + "_chain") for k, v in list(globals().items()) if not k.startswith("_") and k != "done" and isinstance(v, str))
    if _pressed:
        _t0 = time.time()
        try:
            _res = main()
        except Exception as _ex:                 # the error goes into the log panel; the old log never stays
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-600:])
        _sc.sticky[_k + "_log"] = write_log(_res)
        _sc.sticky[_k + "_status"] = ("ERROR" if _res.startswith("ERROR") else
                                      time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky[_k + "_done"] = done_text(True, not _res.startswith("ERROR"), time.time() - _t0)
    done = _sc.sticky.get(_k + "_done", "idle")
    log = _sc.sticky.get(_k + "_log", "Press the Button to export to " + OUT_DIR)
    print(log)               # 25 Oct 12:10: on Aras's canvas the log output is Grasshopper's "out" (printed text)
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(_k + "_status", "idle")  # noqa: F821
    except Exception:
        pass
else:
    print(write_log(main()))
