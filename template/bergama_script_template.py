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
Files (SCRIPT_STANDARD.md §1, Aras 27 Oct 11:07): reads data from ~/Downloads/Bergama/Data/ and other scripts' results
from ~/Downloads/Bergama/cached/<their folder>/; writes FINAL PDFs ONLY to output/<OUT_FOLDER>/, results JSON and every
other working file to cached/<OUT_FOLDER>/, booklet assets to cached/booklet/<OUT_FOLDER>/ and ONE log file to
logs/<LOG_NAME> (overwritten by each press); bg_tidy_output() at the end of main() moves anything else out of output/. The panel keeps the last log for this Rhino
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

# ---- folders (same in every script; in the repo this block is src/common/bergama_paths.py: #@include it) ----
# ---- Bergama folders (Aras 24 Oct 08:28 + 27 Oct 11:07; SCRIPT_STANDARD §9). Every script uses ONLY these. ----
#   Downloads/Bergama/output/<name>/          final PDFs only
#   Downloads/Bergama/logs/                    every log file and log folder
#   Downloads/Bergama/cached/<name>/           caches, results other scripts read, any other working file
#   Downloads/Bergama/cached/booklet/<name>/   the script's booklet assets (blocks.json, results, images);
#                                              the booklet's own leftovers in cached/booklet/
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")


def bg_output(name):
    return os.path.join(BERGAMA_ROOT, "output", name)


def bg_cache(name):
    return os.path.join(BERGAMA_ROOT, "cached", name)


def bg_booklet(name):
    return os.path.join(BERGAMA_ROOT, "cached", "booklet", name)


def bg_logs(*sub):
    return os.path.join(BERGAMA_ROOT, "logs", *sub)


def bg_first(paths):
    """The first path that exists (new place first, then where older versions wrote it), else the first."""
    for p in paths:
        if os.path.exists(p):
            return p
    return paths[0]


def bg_tidy_output(name, cache_dir=None):
    """output/<name>/ keeps PDFs only: log files and anything in a log folder move to logs/<name>/, every other
    non-PDF file to cached/<name>/from_output/ (or cache_dir: the booklet uses cached/booklet/; moved, never deleted;
    same sub-folders). Empty folders go.
    Returns short log lines (counts, not one line per file)."""
    import shutil as _sh
    root, moved, fail = bg_output(name), {}, []
    if not os.path.isdir(root):
        return []
    for d, subs, files in os.walk(root, topdown=False):
        rel = os.path.relpath(d, root)
        rel = "" if rel == "." else rel
        for fn in files:
            if fn.lower().endswith(".pdf"):
                continue
            is_log = "log" in fn.lower() or any("log" in p.lower() for p in rel.split(os.sep) if p)
            dst = os.path.join(bg_logs(name) if is_log else (cache_dir or os.path.join(bg_cache(name), "from_output")), rel, fn)
            try:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if os.path.exists(dst):
                    os.remove(dst)
                _sh.move(os.path.join(d, fn), dst)
                top = bg_logs(name) if is_log else (cache_dir or os.path.join(bg_cache(name), "from_output"))
                moved[top] = moved.get(top, 0) + 1
            except Exception as ex:
                fail.append(u"%s (%s)" % (os.path.join(rel, fn), type(ex).__name__))
        if d != root:
            try:
                os.rmdir(d)                       # only when empty
            except Exception:
                pass
    return ([u"output/%s: %d non-PDF file(s) moved to %s" % (name, n, d) for d, n in sorted(moved.items())] +
            ([u"output/%s: could not move %s" % (name, ", ".join(fail[:5]))] if fail else []))


BERGAMA = BERGAMA_ROOT
DATA_DIR = os.path.join(BERGAMA, "Data")
OUT_DIR = bg_output(OUT_FOLDER)             # final PDFs ONLY
CACHE_DIR = bg_cache(OUT_FOLDER)            # results JSON, caches, any other working file
LOG_DIR = bg_logs()                         # the one log file
ANALYSIS_LAYER = "site_alan"                # analysis range (rectangle)
WORK_LAYER = "calisma_alan"                 # working area, one shared area
SNAP_M = 15.0                               # a proposal this close to calisma_alan counts as on it; nothing is cut


def data_file(name):
    """Downloads/Bergama/Data/<name> if it is there, else None (the script then uses its built-in copy or skips it)."""
    p = os.path.join(DATA_DIR, name)
    return p if os.path.isfile(p) else None


def read_result(folder, name):
    """Another script's results JSON from cached/<folder>/<name>, or None if that script has not run yet."""
    try:
        with open(os.path.join(bg_cache(folder), name), encoding="utf-8") as f:
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
    os.makedirs(CACHE_DIR, exist_ok=True)       # a results JSON is a working file: cached/, never output/
    res = {"site_alan_curves": len(layer_curves(ANALYSIS_LAYER)), "calisma_alan_curves": len(layer_curves(WORK_LAYER))}
    out = os.path.join(CACHE_DIR, "results.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    lines = ["%s  %s" % (out, time.strftime("%H:%M:%S"))] + bg_tidy_output(OUT_FOLDER)   # output/ = final PDFs only
    return "%s\n%s %s, %.1f s" % ("\n".join(lines), GH_LABEL, VERSION, time.time() - t0)


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
