# -*- coding: utf-8 -*-
# r: pymupdf
"""Bergama Group 6: BOOKLET JPG v1 (4 Nov 2026). Rules: scripts/_template/SCRIPT_STANDARD.md.
Turns the newest booklet PDF into one JPG per page (page1.jpg, page2.jpg, ...) plus pages.txt (each page's text) and
zips them, so the booklet can be uploaded to Claude cheaply (Aras 4 Nov 08:06-08:07).
Why it is cheap to read: Claude scales any image down to MAX_PX on its long edge, so pixels above that cost upload
size and buy nothing; pages.txt gives the words as text, which costs far fewer tokens than reading them off a picture.

Component: Rhino 8 > Grasshopper > Python 3 Script, paste the whole file. The first run installs PyMuPDF (the "# r:"
line above; needs internet once).
  input  run   Button, or the Booklet's done output (chain position: after Booklet, last in the chain)
  input  dpi   number, optional: render resolution, default 100 (72 also works); the long edge is capped at MAX_PX
  output log   the last run's report
  output done  "done HH:MM:SS.ss · N s"
Reads  ~/Downloads/Bergama/output/bergama_booklet/   the newest .pdf there (the Booklet writes Bergama_booklet_A3.pdf)
Writes ~/Downloads/Bergama/cached/bergama_booklet_jpg/page1.jpg ... pageN.jpg + pages.txt (working files)
       ~/Downloads/Bergama/output/bergama_booklet_jpg/Bergama_booklet_jpg.zip (the file to upload; replaced each run)
"""
import os, time, zipfile, glob

# ---- SETTINGS ----
VERSION = "v1"
GH_LABEL = "BookletJpg"
OUT_FOLDER = "bergama_booklet_jpg"
LOG_NAME = "bergama_booklet_jpg_log.txt"
SRC_FOLDER = "bergama_booklet"      # the Booklet's output folder (OUT_FOLDER in bergama_booklet_v30_3.py)
ZIP_NAME = "Bergama_booklet_jpg.zip"
DPI = 100                           # used when the dpi input is empty
MAX_PX = 1568                       # long edge cap in pixels (Claude reads larger images scaled down to this)
JPG_QUALITY = 80                    # 0-100; 80 keeps small text sharp at a third of the size of 95

BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
CACHE_DIR = os.path.join(BERGAMA_ROOT, "cached", OUT_FOLDER)
SRC_DIR = os.path.join(BERGAMA_ROOT, "output", SRC_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
TRIG_WHY = [None]

# ---- trigger.py (round 4, S1, 1 Nov 2026; BRIEF §6, round 3 open row 13): ONE start-up / trigger file ----------------
# Replaces common/chain_fire.py, gh_in_items.py, _gh_inputs.py, to_bool.py and the scripts' own copies of chain_fire,
# upstream_done, button_state, find_button, _button_value and BUTTON_WORDS (each page session removes its copy and
# calls trig_should_run; the closing step deletes the four old files once nothing includes them).
#
# WHAT STARTS A COMPONENT (the same for all nine scripts; RUN_GUIDE quotes this):
#   1. A press of its Button: the input named run (or bake / build / go / press / button / start, any case), else the
#      input a Button is wired into. Only the press starts it (the rising edge: False -> True); holding the Button
#      or re-solving while it is True does not start it again.
#   2. A NEW "done ..." text arriving on any of its own inputs from the script before it in the chain (one-click
#      chain). The first solve after the component is pasted, opened or rewired only NOTES the text already on the
#      wire, so pasting code or rewiring never starts a run (Aras 1 Nov 08:04); when the wire brings nothing, the done
#      text the upstream component left in Rhino's memory is read (Null on the wire).
#   Nothing else starts it: settings written in the script (PHOTO_ANY_LICENCE = True ...) and old globals that
#   Rhino 8 keeps between solves are never read as a press (Aras 1 Nov 08:24); only the component's own inputs are.
#
#   trig_inputs() -> {name: value}         the component's own inputs only (VariableName / NickName / Name), never
#                                          the script's globals; {} outside Grasshopper
#   trig_get(name, default=None)           one own input by name in any case; a list gives its first non-None item
#   to_bool(v, default=False)              True / "true" / "yes" / "1" / "on" / non-zero; a list = any item true
#   upstream_done(name) -> str | None      the "done ..." text the component wired into input `name` left in memory
#   chain_fire(v, key, name=None) -> bool  a NEW done text on v (a list gives its first "done ..." item) fires once;
#                                          the first solve per component + wiring only notes it
#   trig_button(settings=()) -> name|None  the Button input (see 1. above); never a name in settings (inputs that
#                                          carry options, e.g. the masterplan's SETTINGS), never one starting with "_"
#   trig_should_run(key="chain_seen", settings=()) -> (run, why, button)
#                                          run: bool; why: "button <name>" | "chain <input>" | None; button: its name
#                                          or None. Each script logs "trigger: <why>" in its run log.
#
# ROUND 5 (S1, 1 Nov 2026; C2, CHK-13: an output folder appeared when Aras only OPENED the GH file, 16:29): every
# memory above (the first-solve note, the last done text seen, the Button's last state) is now kept per OPEN
# DOCUMENT (trig_doc_key: the GH document's runtime id, else its object hash), not per Rhino session. Before, the
# notes of an earlier opening survived in Rhino's sticky, so the first solve after a reopen was not "first" and a
# done text still on a wire (or a Toggle left True: prev False -> True) started a run. Now the first solve after any
# open, paste or rewire only NOTES the wire and the Button state; only a later change starts a run.
# CHANGED APPROACH (Aras 1 Nov 22:46: "if you struggle with an aspect over and over, change your approach"): the chain
# no longer trusts memory notes alone. A chain start exists ONLY after a Button press in THIS open document
# (trig_mark_chain stores (time, document id)); chain_fire fires a component only when such a press exists and its
# done text is newer than the last one it saw. Opening a file, pasting, rewiring or a Toggle left True can never start
# a chain: without a press in this load, every done text on a wire is only noted.
#   trig_doc_key() -> str                  the open GH document's per-load id ("" outside Grasshopper)
#   trig_mark_chain(why)                   a Button run notes the chain start time (sticky "bergama_chain_t0", read by
#                                          bergama_paths.bg_this_run); trig_should_run calls it
TRIGGER_BUTTON_WORDS = ("run", "bake", "build", "go", "press", "button", "start")


def trig_doc_key():
    """the open Grasshopper document's id for THIS load: GH_Document.RuntimeID (new each time a file is opened in a
    Rhino session), else the document object's hash; "" outside Grasshopper"""
    try:
        d_ = ghenv.Component.OnPingDocument()                              # noqa: F821
    except Exception:
        return ""
    if d_ is None:
        return ""
    for a_ in ("RuntimeID", "RuntimeId"):
        try:
            v_ = getattr(d_, a_)
            if v_ is not None:
                return "doc%s" % v_
        except Exception:
            pass
    try:
        return "doch%s" % d_.GetHashCode()
    except Exception:
        return "docp%s" % id(d_)


def trig_mark_chain(why):
    """a run started by a Button press is the start of a chain run: its time goes to sticky "bergama_chain_t0" so
    readers can tell this run's files from older ones (bergama_paths.bg_this_run)"""
    if not why or not str(why).startswith("button"):
        return
    try:
        import scriptcontext as _scx
        import time as _t
        _scx.sticky["bergama_chain_t0"] = _t.time()
        _scx.sticky["bergama_chain_doc"] = trig_doc_key()
    except Exception:
        pass


def trig_chain_live():
    """True when a Button press started a chain in THIS open document (see CHANGED APPROACH above)"""
    try:
        import scriptcontext as _scx
        return (_scx.sticky.get("bergama_chain_t0") is not None and
                _scx.sticky.get("bergama_chain_doc") == trig_doc_key())
    except Exception:
        return False


def trig_inputs():
    """{name: value} of this component's own inputs (globals holding them), nothing else"""
    g_ = globals()
    out = {}
    try:
        for p_ in ghenv.Component.Params.Input:                            # noqa: F821 (Grasshopper)
            for a_ in ("VariableName", "NickName", "Name"):
                n_ = getattr(p_, a_, None)
                if n_ and str(n_) in g_:
                    out[str(n_)] = g_[str(n_)]
                    break
    except Exception:
        return {}
    return out


def trig_get(name, default=None):
    """an own input by name, any case; a list gives its first non-None item; empty text = default"""
    for k_, v_ in trig_inputs().items():
        if k_.lower() == str(name).lower():
            if isinstance(v_, (list, tuple)):
                v_ = next((x for x in v_ if x is not None), None)
            return default if v_ is None or (isinstance(v_, str) and not v_.strip()) else v_
    return default


def to_bool(v, default=False):
    if v is None:
        return default
    if isinstance(v, (list, tuple)):
        return any(to_bool(x) for x in v)
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v != 0
    s = str(v).strip().lower()
    if not s:
        return default
    return s in ("true", "yes", "1", "on")


def upstream_done(name):
    """the done text of the component wired into input `name`, read from Rhino's memory (sticky) when the wire brings
    Null. Keys: "done:<guid>", "lu_done:<guid>" or "...<guid>_done" (template scripts)."""
    try:
        import scriptcontext as _scx
        for p_ in ghenv.Component.Params.Input:                            # noqa: F821
            if str(p_.NickName or p_.Name).lower() != str(name).lower():
                continue
            for src_ in p_.Sources:
                g = str(src_.Attributes.GetTopLevel.DocObject.InstanceGuid)
                for k_ in ("done:" + g, "lu_done:" + g):
                    v_ = _scx.sticky.get(k_)
                    if str(v_).startswith("done "):
                        return str(v_)
                for k_, v_ in list(_scx.sticky.items()):
                    if str(k_).endswith(g + "_done") and str(v_).startswith("done "):
                        return str(v_)
    except Exception:
        pass
    return None


def _chain_wiring():
    """the sources wired into this component (their ids, sorted): rewiring starts a new chain memory"""
    try:
        return ",".join(sorted(str(s_.Attributes.GetTopLevel.DocObject.InstanceGuid)          # noqa: F821
                               for p_ in ghenv.Component.Params.Input for s_ in p_.Sources))   # noqa: F821
    except Exception:
        return ""


def chain_fire(v, key, name=None):
    """True once for each NEW "done ..." text on v (see the module notes)"""
    if isinstance(v, (list, tuple)):
        v = next((x for x in v if str(x).startswith("done ")), None)
    s = str(v) if v is not None else ""
    if not s.startswith("done ") and name:
        s = upstream_done(name) or ""
    try:
        import scriptcontext as _scx
        try:
            key = key + ":" + str(ghenv.Component.InstanceGuid) + ":" + _chain_wiring() + ":" + trig_doc_key()  # noqa
        except Exception:
            pass
        # the first solve with this wiring (pasted, rewired or newly opened component) only notes what is on the
        # wire; "first" is tied to this solve's token (_CHAIN_SOLVE, made anew each time the script body runs), not
        # to a global, because Rhino 8 keeps a script's globals between solves
        tok = globals().get("_CHAIN_SOLVE")
        if _scx.sticky.get(key + ":init") is None:
            _scx.sticky[key + ":init"] = tok
        first = _scx.sticky.get(key + ":init") is tok
        if not s.startswith("done "):
            return False
        if first or _scx.sticky.get(key) == s or not trig_chain_live():
            _scx.sticky[key] = s
            return False
        _scx.sticky[key] = s
        return True
    except Exception:
        return False


def trig_button(settings=()):
    """the Button input's name, or None"""
    ins = trig_inputs()
    skip = set(str(n).lower() for n in settings or ())

    def ok(n):
        return n and not n.startswith("_") and n.lower() not in skip
    for k_ in ins:
        if ok(k_) and "".join(c for c in k_.lower() if c.isalpha()) in TRIGGER_BUTTON_WORDS:
            return k_
    try:
        for p_ in ghenv.Component.Params.Input:                            # noqa: F821
            nm = str(p_.NickName or p_.Name)
            if not ok(nm):
                continue
            for src_ in p_.Sources:
                if "button" in type(src_.Attributes.GetTopLevel.DocObject).__name__.lower():
                    return nm
    except Exception:
        pass
    return None


def trig_should_run(key="chain_seen", settings=()):
    """(run, why, button): does this solve start the script? (see the module notes)"""
    btn = trig_button(settings)
    ins = trig_inputs()
    try:
        import scriptcontext as _scx
        try:
            gk = str(ghenv.Component.InstanceGuid)                          # noqa: F821
        except Exception:
            gk = ""
        pk = "trig_prev:" + key + ":" + gk + ":" + trig_doc_key()
        on = to_bool(trig_get(btn)) if btn else False
        prev = _scx.sticky.get(pk)
        if prev is None:              # round 5 (C2): the first solve of this document only notes the Button's state
            prev = on
        prev = bool(prev)
        _scx.sticky[pk] = on
    except Exception:
        on, prev = (to_bool(trig_get(btn)) if btn else False), False
    if on and not prev:
        trig_mark_chain(u"button")
        return True, u"button " + btn, btn
    # the chain: the button input first (the board family wires the done text there), then every other own input
    skip = set(str(x).lower() for x in settings or ())
    names = ([btn] if btn else []) + [n for n in ins if n != btn and not n.startswith("_") and n.lower() not in skip]
    fired = None
    for n in names:
        v = ins.get(n)
        if v is None or isinstance(v, (bool, int, float)) or (isinstance(v, (list, tuple)) and not any(
                isinstance(x, str) for x in v)):
            if n != btn:
                continue
        if chain_fire(v, key + ":" + n, n) and fired is None:
            fired = n
    if fired:
        return True, u"chain " + fired, btn
    return False, None, btn


_CHAIN_SOLVE = object()     # a new token every time the script body runs (one per solve)


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


def main():
    t0 = time.time()
    try:
        import pymupdf as fz
    except ImportError:
        import fitz as fz
    pdfs = [p for p in glob.glob(os.path.join(SRC_DIR, "*.pdf")) if os.path.isfile(p)]
    if not pdfs:
        return "ERROR: no PDF in %s (run the Booklet first)" % SRC_DIR
    src = max(pdfs, key=os.path.getmtime)
    try:
        dpi = float(trig_get("dpi", DPI))
    except Exception:
        dpi = float(DPI)
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(OUT_DIR, exist_ok=True)
    for old in glob.glob(os.path.join(CACHE_DIR, "page*.jpg")):    # no pages left over from a longer booklet
        os.remove(old)
    doc = fz.open(src)
    files, texts, size = [], [], (0, 0)
    for i, page in enumerate(doc, 1):
        long_pt = max(page.rect.width, page.rect.height)
        zoom = min(dpi / 72.0, MAX_PX / long_pt)
        pix = page.get_pixmap(matrix=fz.Matrix(zoom, zoom), alpha=False)
        fn = os.path.join(CACHE_DIR, "page%d.jpg" % i)
        pix.save(fn, jpg_quality=JPG_QUALITY)
        files.append(fn)
        size = (pix.width, pix.height)
        texts.append("=== page%d ===\n%s" % (i, page.get_text("text").strip()))
    doc.close()
    txt = os.path.join(CACHE_DIR, "pages.txt")
    with open(txt, "w", encoding="utf-8") as f:
        f.write("source: %s\n\n%s\n" % (os.path.basename(src), "\n\n".join(texts)))
    zp = os.path.join(OUT_DIR, ZIP_NAME)
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_STORED) as z:          # JPGs are compressed already
        for fn in files + [txt]:
            z.write(fn, os.path.basename(fn))
    return ("trigger: %s\nsource: %s (%s)\n%d pages at %.0f dpi, capped to %d px long edge (last page %d x %d px)\n"
            "%s  %.1f MB  %s\n%s %s, %.1f s" % (
                TRIG_WHY[0], src, time.strftime("%d %b %H:%M", time.localtime(os.path.getmtime(src))), len(files),
                dpi, MAX_PX, size[0], size[1], zp, os.path.getsize(zp) / 1048576.0, time.strftime("%H:%M:%S"),
                GH_LABEL, VERSION, time.time() - t0))


# ---- Grasshopper wiring (same in every script; never define a function named run: it would hide the input) ----
if "ghenv" in globals():
    import scriptcontext as _sc
    _k = "bergama_" + OUT_FOLDER
    try:
        _k += ":" + str(ghenv.Component.InstanceGuid)   # noqa: F821
    except Exception:
        pass
    _pressed, _why, _btn = trig_should_run("bergama_booklet_jpg_chain", settings=("dpi",))
    TRIG_WHY[0] = _why
    if _pressed:
        _t0 = time.time()
        try:
            _res = main()
        except Exception as _ex:
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-600:])
        _sc.sticky[_k + "_log"] = write_log(_res)
        _sc.sticky[_k + "_status"] = ("ERROR" if _res.startswith("ERROR") else
                                      time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky[_k + "_done"] = done_text(True, not _res.startswith("ERROR"), time.time() - _t0)
        _sc.sticky[_k + "_ver"] = VERSION
    if _sc.sticky.get(_k + "_ver") != VERSION:   # a newly pasted version shows itself at once, idle
        for _s in ("_log", "_status", "_done"):
            _sc.sticky.pop(_k + _s, None)
    done = _sc.sticky.get(_k + "_done", "idle")
    log = _sc.sticky.get(_k + "_log", "Press the Button to turn the newest PDF in %s into %s" % (
        SRC_DIR, os.path.join(OUT_DIR, ZIP_NAME)))
    print(log)
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(_k + "_status", "idle")  # noqa: F821
    except Exception:
        pass
else:
    print(write_log(main()))
