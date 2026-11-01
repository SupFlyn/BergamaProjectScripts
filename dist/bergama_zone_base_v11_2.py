# CURRENT VERSION: bergama_zone_base_v11_2.py = v11.2 (2 Nov 2026; fix: bake() renamed zb_bake() so a Button named bake works; what changed: the NEW IN / VERSION notes below)
"""BERGAMA ZONE BASE v11 (2026-11-01): bakes Group 6's zone layout into the open Rhino file as an editable base.

NEW IN v11 (round 4, S1, 1 Nov 2026): (1) ONE start-up rule shared by all nine scripts (common/trigger.py, round 3
open row 13): a press of the Button wired into `run` (rising edge), or a NEW done text from the script before it;
pasting or rewiring never starts it; the log says what started it ("trigger: button run" / "trigger: chain run").
(2) Names from the project's names table (G-R4-11): the two text dots that read "K4" and "K5" now read the bridges'
names (Ulucami Önü Köprüsü, Üç Kemer Köprüsü); K-codes are never printed. Zones unchanged.

NEW IN v10 (Aras 27 Oct 11:07, output cleanup): writes nothing under output/ (its log is Downloads/Bergama/logs/
bergama_zone_base_log.txt); anything older versions left in output/bergama_zone_base/ is moved out (logs to logs/,
the rest to cached/). Zones unchanged.

NEW IN v9 (Aras 25 Oct 16:43: "the selection of A should be remember in the whole project so all scripts should drop B alternatives"): bakes option A only (Option_A::INT_*); option B is no longer baked and the option input is
ignored. Option_B layers already in a file are left as they are (delete them by hand if you want). Nothing else
changed.

OLDER VERSIONS: their notes are in HISTORY.md (repo SupFlyn/BergamaProjectScripts, src/bergama_zone_base/).

WHAT IT IS
  A Grasshopper Python 3 component. Wire a plain Button into an input named `run` (v8; bake / build / go / press also work);
  one press bakes the whole base, both presentations, into the open Rhino file:
    Option_A::INT_...   PanelReview1A: curved edges only where the project meets the water, straight elsewhere
    Option_B::INT_...   PanelReview1B: no organic forms, every edge straight or faceted
  These are the INT_ layers that bergama_masterplan reads, so after editing you press Build on the masterplan
  component and get one sheet per option.

  What is baked, per option (the revised draft of 17-18 Oct, mp2/draft2/make_draft_markup_v2.py, checked against
  CONCEPT_RECORD v2.3 sections 3.3-3.6, 5.2, 5.4):
    NEW IN v2 (Aras 2026-10-18 14:29): the water only runs downstream (Aras upstream, then Begum K4, K5, then Nil;
    the survey strip order). It is cleaned at Aras's end, so the whole river runs clean; Nil needs no treatment; no
    water flows back up.
    Aras   aras_alan      "Collect, clean and hold": WS 1 retention terraces (dry top) hold the runoff, WT 1
                          cleansing reed basins (v1's planted basins) take river water and the held runoff, WD 1
                          spillway gives the clean water back to the strip; GR 1 shaded walk
    Begum  begum_alan[0]  K4 "Amphibious heritage threshold": WA 1-2 bed (W), WA 3 flood terrace (F), GR 2 raised dry
                          top (D) on the cleared plot (2 INT_REMOVE_cleared buildings, gone in the 1 Oct photos)
           begum_alan[1]  K5: WA 4-5 bed, WA 6 flood terrace, GR 3 raised dry top
    Nil    nil_alan       "Give back": WP 1-2 floodable riverside planting fed by the clean river (v1's reed beds),
                          floodable boardwalk. No farmland and no farm channel inside the site (v3/v4, Aras 14:49 and
                          15:02: the farms are the existing ones on the slopes just outside the site)
    All    the continuous low-flow water strip (INT_WATER_strip, decision D8; labelled CLEAN WATER STRIP below Aras),
           wetland planting edges (INT_SURFACE_wetland), labels (INT_LABEL_notes)
    Arrows INT_LINK_water / INT_LINK_people / INT_LINK_flood: 11 per option, every one passes bergama_masterplan v6's
           link_check, and every water arrow points downstream.
           NEW IN v5 (Aras 15:03 "have the interaction arrows from the closest place possible always"): each arrow
           joins the two closest points of what it links (2.5 m inside each zone) along a line that crosses no third
           zone; a river end sits on open strip at or upstream of the zone it feeds, at or downstream of the zone it
           drains, so no arrow shows water running uphill. Every river end stays at least 1.5 m off any zone edge.
  Every size is a PLACEHOLDER, not a design size: each zone's user text `basis` says what it was sized on (open
  ground between surveyed obstacles, legibility). No storage volume, level or flow is drawn.

RULES IT KEEPS
  * It bakes only into a file whose study areas (aras_alan, begum_alan, nil_alan) sit where the course survey has
    them (within 5 cm): the base is in survey coordinates. Any other file: ERROR, nothing is baked.
  * The study-area curves are never touched.
  * YOUR EDITS ARE KEPT. Each baked object carries user text `base_hash` (its shape when baked). Pressing again
    deletes and re-bakes only the objects still exactly as baked; an object you moved, reshaped or recoloured
    stays, and its draft piece is not baked again. An object you deleted comes back on the next press (to stop
    that, set `option` to the other option or do not press again).
  * A and B are two designs for the same ground, so they lie in the same place on separate parent layers (the
    masterplan needs them there to read them). Switch a parent layer off to see one at a time; the masterplan bakes
    its two sheets side by side.

INPUTS (any case; only the button is needed)
  run      Button
  option   "both" (default), "A" or "B"

OUTPUT
  log: the log. It stays readable after the button is released, and is also written to
  Downloads/Bergama/logs/bergama_zone_base_log.txt (v11.2: this text said output/, the file has been in logs/ since v10).
"""

import os
import json
import time
import zlib
import base64
import hashlib
import tempfile
import datetime

import Rhino
import Rhino.Geometry as rg
import System
import System.Drawing
import scriptcontext as sc

VERSION = "bergama_zone_base v11.2 (2026-11-02)"  # v11.2 fix (round 5 S5, CHK-12): the function bake() is now zb_bake(): a Button input named `bake` (offered below) read the function, so a press did nothing, as run() did in v11.1; v11.1 fix 1 Nov 16:40: the function run() replaced the Button input `run`, so a press did nothing; renamed main(); v11 round 4 S1: common/trigger.py (one start-up rule), bridge names on the K4/K5 dots; older: v10.2 fix 1 Nov 08:20: chain trigger keyed to each solve (Rhino keeps globals), so the chain continues after ZoneBase; v10.1 fix 1 Nov: a pasted or rewired component no longer runs by itself (chain trigger notes the wire on its first solve)
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


def bg_out_dir(name):
    """round 5 (C2): output/<name>/ made only now, just before a file is written into it (a run that stops early, or a
    solve that never runs, leaves no empty folder). Returns the path."""
    p = bg_output(name)
    os.makedirs(p, exist_ok=True)
    return p


def bg_result(script, fn):
    """round 5 (C10): where another script's result file `fn` is: cached/<script>/fn, then cached/<script>/from_output/
    fn (moved there by bg_tidy_output), then output/<script>/fn (older versions); the first that exists, else the
    first path (shade_july.json was looked for in output/ after the site board had moved it to cached/)."""
    return bg_first([os.path.join(bg_cache(script), fn), os.path.join(bg_cache(script), "from_output", fn),
                     os.path.join(bg_output(script), fn)])


def bg_this_run(path):
    """round 5 (C10): (fresh, note) for a result file another script wrote: fresh = written at or after the start of
    this chain run (the Button press that started the chain, sticky "bergama_chain_t0" from trigger.py); note = a short
    log text ("this run 23:01" / "from an earlier run 22:40" / "missing" / "no chain start known"). A reader logs the
    note and, when not fresh, a WARNING (the value is from the run before: one press must give one answer)."""
    import time as _t
    if not os.path.isfile(path):
        return False, u"missing"
    m = os.path.getmtime(path)
    hm = _t.strftime("%d %b %H:%M", _t.localtime(m))
    try:
        import scriptcontext as _scx
        t0 = _scx.sticky.get("bergama_chain_t0")
    except Exception:
        t0 = None
    if t0 is None:
        return True, u"no chain start known (file of %s)" % hm
    if m + 1.0 >= t0:
        return True, u"this run %s" % hm
    return False, u"from an earlier run %s" % hm


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
LOG_DIR = bg_logs()                        # Aras 25 Oct 09:34-09:35: every script's log here

BASE_MD5 = "cdfe4fe55413b71ba9d80dd092ff1112"  # the decompressed base data (701,976 bytes of JSON, survey coordinates)
# The base: mp2/draft2/draft_markup.json (Option_A / Option_B, 14 zones each) + 11 typed arrows per option, JSON,
# zlib + base64. Generated by prep_auto_v5.py; v7 appends 10 Demeter's Garden items (2 zones + 3 labels per option).
# Do not edit by hand.
def bergama_data(name, _c={}):
    """Built-in data kept in Downloads/Bergama/Data/bergama_zone_base_data.py (Aras 25 Oct 21:29, scripts shortened): runs its
    section `name` here, as if it were written in this place. The file is read once per run; a missing file or one
    from another version of this script stops the script with a message saying which file to copy."""
    import os as _os, hashlib as _hl
    if not _c:
        p_ = _os.path.join(_os.path.expanduser("~"), "Downloads", "Bergama", "Data", "bergama_zone_base_data.py")
        if not _os.path.isfile(p_):
            raise RuntimeError("Data file missing: copy bergama_zone_base_data.py from the run kit's Data folder into " + _os.path.dirname(p_))
        with open(p_, encoding="utf-8", newline="") as f_:
            for part_ in f_.read().split("\n#@@ ")[1:]:
                k_, _, b_ = part_.partition("\n")
                _c[k_] = b_
    b_ = _c.get(name)
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != {'BASE_DATA': 'cf047935732fa0db32aed2866224f6ea', 'NAMES': '5106ee0771c09305a6fcf44ed5f835ad'}.get(name):
        raise RuntimeError("Data file bergama_zone_base_data.py is not the one made with this script version (part " + name +
                           "): copy it again from the same run kit as the script")
    exec(compile(b_, "bergama_zone_base_data.py:" + name, "exec"), globals())


bergama_data("BASE_DATA")
SHORT = "v11.2"
TAG = "bergama_zone_base"                          # user text key on every baked object (value = VERSION)
STUDY_BBOX = {                                     # the course survey's study areas (survey = file coordinates, m)
    "aras_alan": [(29610.0960, 32247.0612, 29880.6932, 32794.2334)],
    "begum_alan": [(29792.1139, 32108.0060, 30053.4176, 32398.0733), (30138.0721, 31405.2525, 30555.8868, 31924.6365)],
    "nil_alan": [(30389.6859, 30542.0263, 31415.5004, 31450.8529)],
}
BBOX_TOL = 0.05
LAYER_COLOURS = {                                  # the masterplan palette's tones for the starter layers (sRGB hex)
    "INT_ZONE_WS": "5D7F8D", "INT_ZONE_WD": "4E7A88", "INT_ZONE_WT": "6F8F6A", "INT_ZONE_WA": "7FA2A6",
    "INT_ZONE_WI": "A79A5A", "INT_ZONE_GR": "7E9A62", "INT_ZONE_DG": "89986A", "INT_WATER_strip": "32525F", "INT_SURFACE_wetland": "6F8F6A",
    "INT_REMOVE_cleared": "6E6A66", "INT_ROAD_path": "8C7B66", "INT_LABEL_notes": "3A3536",
    "INT_LINK_water": "32525F", "INT_LINK_people": "8C1C32", "INT_LINK_flood": "5D7F8D"}
PARENT = {"A": "Option_A", "B": "Option_B"}


# ---------------------------------------------------------------- Grasshopper inputs, memory, status
# v11 (round 4): what starts this component = common/trigger.py (its notes say it for all nine scripts)
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


_GH_IN = trig_inputs()
_T_START = time.time()

bergama_data("NAMES")
# ---- Names (round 3, A2, 31 Oct 2026; G16 / D9): every printed bridge or place name comes from data/NAMES.py ---------
#   bridge_name(code, short=False)   "K3" -> "Tabak Köprüsü" (short: "Tabak", only where the full name is in the
#                                     same drawing's key or title); unknown code -> KeyError (never print a K-code)
#   bridges_in_order()               the codes upstream first: K1, K2, K4, K3, K5, K6 (lists, keys, rulers)
#   place_name(key)                  "bank_NE" -> "Kale side · north bank", "stream" -> "Selinos stream"
#   cut_end_labels(cid)              ("W3", "W3'") the cut id + prime at its ends (D6)
#   landmark_name(key, descr=None)   round 4 (S1, G-R4-11): "kizil_avlu" -> "Kızıl Avlu"; descr=True adds the table's
#                                     English descriptor ("Kızıl Avlu · Hadrian's temple"), descr="text" adds that text;
#                                     unknown key -> KeyError (never type a landmark name locally)
#   landmark_keys()                  the landmark keys in the table
# Needs data/NAMES.py included before it.


def bridge_name(code, short=False):
    """the one spelling of a bridge by its internal code (K1-K6, any case)"""
    row = NAMES["bridges"][str(code).strip().upper()]
    return row["short"] if short else row["name"]


def bridges_in_order():
    """the bridge codes in stream order, upstream first"""
    b = NAMES["bridges"]
    return sorted(b, key=lambda c: b[c]["order"])


def place_name(key):
    """the one spelling of a place (stream, banks, sides)"""
    return NAMES["places"][key]


def cut_end_labels(cid):
    """D6: the labels at a cut's two ends: the cut id and the id with a prime ("W3", "W3'")"""
    c = str(cid).strip()
    return c, c + u"'"


def landmark_name(key, descr=None):
    """the one (Turkish) spelling of a landmark, optionally followed by an English descriptor"""
    row = NAMES["landmarks"][str(key).strip().lower()]
    if descr is True:
        d = row.get("descr")
        if not d:
            raise KeyError(u"landmark %s has no descriptor in the names table" % key)
    else:
        d = descr or None
    return row["name"] + (u" · " + d if d else u"")


def landmark_keys():
    """the landmark keys in the names table"""
    return sorted(NAMES["landmarks"])


def done_text(ran, ok, secs):
    """The done output: kept until the next run (this Rhino session)."""
    return ("done " if ok else "ERROR ") + time.strftime("%H:%M:%S") + ".%02d" % int((time.time() % 1) * 100) + \
        " · %.0f s" % secs if ran else None



def gin(name, default=None):
    """An input by name in any case (bake = Bake = BAKE)."""
    for k_, v_ in _GH_IN.items():
        if k_.lower() == name.lower():
            if isinstance(v_, (list, tuple)):
                v_ = next((x for x in v_ if x is not None), None)
            return default if v_ is None or (isinstance(v_, str) and not v_.strip()) else v_
    return default


# 25 Oct (Aras 09:55): remembered for this Rhino session only (sticky); no temp state file. The one copy on disk is
# the log in Downloads/Bergama/logs/, read back only if the session lost the last log.
def _key(k):
    try:
        return "{}:{}".format(k, ghenv.Component.InstanceGuid)      # noqa: F821
    except Exception:
        return k


def mem_get(k, default=None):
    kk = _key(k)
    try:
        if kk in sc.sticky:
            return sc.sticky[kk]
    except Exception:
        pass
    if k == "last":
        try:
            with open(os.path.join(LOG_DIR, "bergama_zone_base_log.txt"), encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return default


def mem_set(k, v):
    try:
        sc.sticky[_key(k)] = v
    except Exception:
        pass


GH_LABEL = "ZoneBase"                                # Aras 25 Oct 09:44: name under the component


def gh_status(text):
    """The text under the component: name, version, then the time of the last run and its length (or idle)."""
    try:
        ghenv.Component.Message = GH_LABEL + " " + text              # noqa: F821
    except Exception:
        pass


def gh_message(level, text):
    try:
        import Grasshopper
        lv = {"error": Grasshopper.Kernel.GH_RuntimeMessageLevel.Error,
              "warning": Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning}[level]
        ghenv.Component.AddRuntimeMessage(lv, text[:500])            # noqa: F821
    except Exception:
        pass


# ---------------------------------------------------------------- the base
def base_items():
    raw = zlib.decompress(base64.b64decode("".join(BASE_DATA)))
    if hashlib.md5(raw).hexdigest() != BASE_MD5:
        raise ValueError("the embedded base data is damaged (md5 differs): copy the script again")
    return json.loads(raw.decode("utf-8"))


def shape_hash(g):
    """A short hash of an object's shape (curve vertices or a text dot's point and text), rounded to 1 mm."""
    pts = []
    try:
        if isinstance(g, rg.TextDot):
            pts = [(g.Point.X, g.Point.Y), g.Text]
        else:
            res = g.TryGetPolyline()
            pl = res[1] if isinstance(res, tuple) and res[0] else None
            pts = [(p.X, p.Y) for p in pl] if pl is not None else [
                (g.PointAtStart.X, g.PointAtStart.Y), (g.PointAtEnd.X, g.PointAtEnd.Y), round(g.GetLength(), 3)]
    except Exception:
        pts = [str(g)]
    s_ = ";".join("{:.3f},{:.3f}".format(*p) if isinstance(p, tuple) else str(p) for p in pts)
    return hashlib.md5(s_.encode("utf-8")).hexdigest()[:16]


CALISMA_COPY = [                                   # v6: calisma_alan of Bergama_Altlik.3dm (25 Oct 08:25: closed, ends snapped onto site_alan), survey m
    [(29696.903, 32800.562), (29872.423, 32572.84), (29880.693, 32496.334), (29818.865, 32475.301), (29825.821, 32398.074), (29923.185, 32344.348), (29904.985, 32311.252), (29997.056, 32290.092), (30053.417, 32139.667), (30004.049, 32108.006), (29954.803, 32210.611), (29792.114, 32247.062), (29761.684, 32302.735), (29754.016, 32451.383), (29678.437, 32447.696), (29632.398, 32496.591), (29665.339, 32526.253), (29612.859, 32696.506), (29600.496, 32719.394)],
    [(30178.18, 31923.887), (30138.072, 31887.655), (30257.694, 31773.217), (30389.686, 31405.252), (30701.152, 30991.252), (30840.053, 31053.865), (31044.852, 30781.877), (31014.2, 30757.409), (31373.442, 30493.066), (31453.175, 30560.194), (31332.978, 30864.179), (31012.679, 31323.349), (30737.856, 31286.66), (30712.87, 31331.891), (30556.09, 31450.103), (30454.629, 31577.301), (30434.156, 31607.332), (30313.613, 31812.92)],
]
CALISMA_LAYER = "calisma_alan"
CLOSE_GAP = 5.0                                   # v6: m, an open outline closer than this counts as closed
SNAP_M = 15.0                                     # v6: m, a proposal this close to calisma_alan counts as on it
SURVEY_PROBE = ("HIDRO_DERE_SULU", "SEV_UST", "BINA_MESKEN")   # v6: survey layers that cross the study areas
STUDY_NOTE = []                                                   # v6: what study_check accepted, for the log


def survey_on_study_areas(doc):
    """v6: True when objects on the SURVEY_PROBE layers overlap every recorded study area (survey coordinates)."""
    boxes = [b for bs in STUDY_BBOX.values() for b in bs]
    hit = [False] * len(boxes)
    for lay in doc.Layers:
        if lay.IsDeleted or lay.Name not in SURVEY_PROBE:
            continue
        for o in doc.Objects.FindByLayer(lay) or []:
            bb = o.Geometry.GetBoundingBox(True)
            for k, b in enumerate(boxes):
                if not hit[k] and bb.Max.X >= b[0] and bb.Min.X <= b[2] and bb.Max.Y >= b[1] and bb.Min.Y <= b[3]:
                    hit[k] = True
            if all(hit):
                return True
    return all(hit)


def study_check(doc):
    """'' when the open file's study areas sit where the course survey has them (or, v6, the file has none and its
    survey lies on the recorded study areas), else why not."""
    del STUDY_NOTE[:]
    have = {}
    for lay in doc.Layers:
        if lay.IsDeleted or lay.Name not in STUDY_BBOX:
            continue
        for o in doc.Objects.FindByLayer(lay) or []:
            bb = o.Geometry.GetBoundingBox(True)
            have.setdefault(lay.Name, []).append((bb.Min.X, bb.Min.Y, bb.Max.X, bb.Max.Y))
    if not have:                                                  # v6: e.g. the larger survey, no study layers
        if survey_on_study_areas(doc):
            STUDY_NOTE.append("No study-area layers in this file: its survey lies on the recorded study areas "
                              "(STUDY_BBOX), so it is the survey in survey coordinates; the base was baked there.")
            return ""
        return "no study-area layers, and no survey ({}) on the recorded study areas".format(", ".join(SURVEY_PROBE))
    for nm, boxes in STUDY_BBOX.items():
        got = list(have.get(nm, []))
        if len(got) < len(boxes):
            return "layer {} holds {} curve(s), the course survey has {}".format(nm, len(got), len(boxes))
        for b in boxes:
            j = next((k for k, q in enumerate(got) if max(abs(q[i] - b[i]) for i in range(4)) <= BBOX_TOL), None)
            if j is None:
                return "a study area on {} is not where the course survey has it (more than {} m off)".format(
                    nm, BBOX_TOL)
            got.pop(j)
    return ""


def ensure_layer(doc, path):
    idx = doc.Layers.FindByFullPath(path, -1)
    if idx >= 0:
        return idx
    parent, _, name = path.rpartition("::")
    lay = Rhino.DocObjects.Layer()
    lay.Name = name
    if parent:
        lay.ParentLayerId = doc.Layers[ensure_layer(doc, parent)].Id
    h = LAYER_COLOURS.get(name)
    if h:
        lay.Color = System.Drawing.Color.FromArgb(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    return doc.Layers.Add(lay)


def calisma_areas(doc, tol, log):
    """v6: the closed working-area outlines: calisma_alan of the open file, else CALISMA_COPY."""
    out = []
    for lay in doc.Layers:
        if lay.IsDeleted or lay.Name.lower() != CALISMA_LAYER:
            continue
        for o in doc.Objects.FindByLayer(lay) or []:
            c = o.Geometry
            if not isinstance(c, rg.Curve):
                continue
            if not c.IsClosed:
                if c.PointAtStart.DistanceTo(c.PointAtEnd) > CLOSE_GAP:
                    log.append("calisma_alan: an open curve ({:.1f} m between its ends) was skipped".format(
                        c.PointAtStart.DistanceTo(c.PointAtEnd)))
                    continue
                res = c.TryGetPolyline()
                pl_ = res[1] if isinstance(res, tuple) and res[0] else None
                if pl_ is not None:
                    pl_.Add(pl_[0])
                    c = rg.PolylineCurve(pl_)
                else:
                    c = c.DuplicateCurve()
                    if not c.MakeClosed(CLOSE_GAP):
                        log.append("calisma_alan: a curve could not be closed and was skipped")
                        continue
            out.append(c)
    if out:
        log.append("Working area: {} calisma_alan outline(s) of this file, worked as one area".format(len(out)))
        return out
    log.append("Working area: no calisma_alan in this file; the built-in copy (Bergama_Altlik.3dm, 25 Oct) was used")
    return [rg.PolylineCurve([rg.Point3d(x, y, 0.0) for x, y in P + [P[0]]]) for P in CALISMA_COPY]


def near_work(g, areas, tol):
    """v6: True when curve g lies in, crosses or comes within SNAP_M of the working area (Aras 08:11: lines that
    nearly match are taken as overlapping, the larger area is the true one, so nothing is cut)."""
    pl = rg.Plane.WorldXY
    for A in areas:
        if A.Contains(g.PointAtStart, pl, tol) != rg.PointContainment.Outside:
            return True
        res = g.ClosestPoints(A)
        if res and res[0] and res[1].DistanceTo(res[2]) <= SNAP_M:
            return True
    return False


def zb_bake(doc, which, log):   # v11.2 (CHK-12): was bake(), a Button word
    """Bake the base for options `which` (('A', 'B') by default). Returns the number of objects baked."""
    items = base_items()
    tol = doc.ModelAbsoluteTolerance or 0.001
    areas = calisma_areas(doc, tol, log)
    n_all = 0
    for o_ in which:
        parent = PARENT[o_]
        t_ = time.time()
        # earlier bake of this script under this parent: untouched objects go, edited ones stay
        kept_ids, gone = set(), 0
        for o in list(doc.Objects):
            try:
                lp = doc.Layers[o.Attributes.LayerIndex].FullPath
            except Exception:
                continue
            if not lp.startswith(parent + "::") or o.Attributes.GetUserString(TAG) is None:
                continue
            if o.Attributes.GetUserString("base_hash") == shape_hash(o.Geometry):
                doc.Objects.Delete(o, True)
                gone += 1
            else:
                kept_ids.add(o.Attributes.GetUserString("base_id"))
        groups, dropped = {}, []
        for k_, it in enumerate(i for i in items if i["layer"].startswith(parent + "::")):
            bid = "{}-{}".format(o_, k_)
            if bid in kept_ids and (it["kind"] != "LABEL" or not it.get("lead") or bid + "-lead" in kept_ids):
                continue
            lay = it["layer"]
            att = Rhino.DocObjects.ObjectAttributes()
            att.LayerIndex = ensure_layer(doc, lay)
            att.Name = it.get("name") or ""
            for mk, mv in (it.get("meta") or {}).items():
                att.SetUserString(mk, str(mv))
            att.SetUserString(TAG, VERSION)
            att.SetUserString("base_id", bid)
            gids = []
            if it["kind"] == "LABEL":
                if it.get("pt") and bid not in kept_ids:
                    txt = it.get("text") or it.get("name") or ""
                    if txt.strip().upper() in NAMES["bridges"]:  # v11 (G-R4-11): a bridge by its name, never "K4"
                        txt = bridge_name(txt)
                    g = rg.TextDot(txt, rg.Point3d(it["pt"][0], it["pt"][1], 0.0))
                    if it.get("font"):                       # v7: the very small "idea: Begum" credit
                        g.FontHeight = int(it["font"])
                    att.SetUserString("base_hash", shape_hash(g))
                    gids.append(doc.Objects.AddTextDot(g, att))
                if it.get("lead") and bid + "-lead" not in kept_ids:
                    g = rg.PolylineCurve([rg.Point3d(p[0], p[1], 0.0) for p in it["lead"]])
                    a2 = att.Duplicate()
                    a2.SetUserString("base_id", bid + "-lead")
                    a2.SetUserString("base_hash", shape_hash(g))
                    gids.append(doc.Objects.AddCurve(g, a2))
            else:
                P = [rg.Point3d(p[0], p[1], 0.0) for p in it["P"]]
                if it.get("closed") and P[0].DistanceTo(P[-1]) > tol:
                    P.append(P[0])
                g0 = rg.PolylineCurve(P)
                if not near_work(g0, areas, tol):            # v6: nothing is cut; only what lies far off is left out
                    dropped.append((it.get("meta") or {}).get("id") or it.get("name") or bid)
                    continue
                for g in [g0]:
                    a2 = att.Duplicate()
                    a2.SetUserString("base_hash", shape_hash(g))
                    gids.append(doc.Objects.AddCurve(g, a2))
            ok = sum(1 for g_ in gids if g_ != System.Guid.Empty)
            who = "calisma_alan"                         # v6: one shared working area, no split by person
            grp = groups.setdefault(who, {})
            nm = {"ZONE": "zones", "WATER": "strip pieces", "SURFACE": "wetland edges", "REMOVE": "cleared buildings",
                  "ROAD": "paths", "LINK": "arrows", "LABEL": "labels"}[it["kind"]]
            grp[nm] = grp.get(nm, 0) + ok
            n_all += ok
        dt = time.time() - t_
        log.append("{}: {:.1f} s{}{}".format(parent, dt, "; {} untouched objects of the last press replaced".format(
            gone) if gone else "", "; {} of your edited objects kept as they are".format(len(kept_ids))
            if kept_ids else ""))
        for who in sorted(groups):
            log.append("  {}  {}".format(who, ", ".join("{} {}".format(v, k) for k, v in sorted(groups[who].items()))))
        if dropped:
            log.append("  more than {:.0f} m outside calisma_alan, not baked: ".format(SNAP_M) + ", ".join(dropped))
    doc.Views.Redraw()
    return n_all


def main():    # v11.1: was run(), which replaced the Button input `run` (Button did nothing)
    pressed, why, btn = trig_should_run("chain_seen")          # v11: common/trigger.py
    if btn is None and not pressed:
        text = "No button found: wire a Button into an input named run. ({})".format(VERSION)
        gh_status(SHORT + " · no button")
        gh_message("warning", text)
        return text
    btn = btn or "run"
    globals()["_ran_now"] = pressed
    if not pressed:
        last = mem_get("last", "")
        gh_status(mem_get("status", "") or SHORT + " · idle")
        return (last + "\n\n(This is the log of the last press. Press {} to bake again.)".format(btn)) if last else \
            "Idle. Press {} to bake the zone base into Option_A. ({})".format(btn, VERSION)
    t0 = time.time()
    gh_status(SHORT + " · baking")
    log, err = ["trigger: " + why], None
    doc = Rhino.RhinoDoc.ActiveDoc
    which = ("A",)                                     # v9: option A only, project-wide (Aras 25 Oct 16:43)
    # v5 24 Oct: all files under Downloads/Bergama/ (Aras rule); was beside the .3dm
    folder = LOG_DIR                                   # v10: the log is its only file (was named output/bergama_zone_base)
    log.extend(bg_tidy_output("bergama_zone_base"))     # v10: output/ = PDFs only (27 Oct)
    n = 0
    try:
        if doc is None:
            raise RuntimeError("no Rhino file is open")
        if doc.ModelUnitSystem != Rhino.UnitSystem.Meters:
            raise RuntimeError("the file is not in metres ({}): the base is in metres".format(doc.ModelUnitSystem))
        why = study_check(doc)
        if why:
            raise RuntimeError("this is not the Bergama survey in survey coordinates ({}). The base is in those "
                               "coordinates, so nothing was baked. Open Bergama_Altlik.3dm and press again".format(why))
        log.extend(STUDY_NOTE)
        n = zb_bake(doc, which, log)
    except Exception as ex_:
        err = "ERROR: {}: {}".format(type(ex_).__name__, ex_)
    secs = time.time() - t0
    head = ["Run at {} | {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), VERSION),
            ("RESULT: " + err) if err else "RESULT: done in {:.0f} s: {} objects baked ({})".format(
                secs, n, " and ".join(PARENT[w] for w in which)),
            "DESTINATION: this Rhino file, layers {} (true place on the survey){}".format(
                " and ".join(PARENT[w] + "::INT_..." for w in which),
                "; log file in " + folder if folder else ""),
            "-" * 60]
    tail = ["", "Every size is a placeholder (user text 'basis' on each zone). Edit freely, then press Build on the "
                "masterplan component. Pressing here again keeps every object you changed."]
    text = "\n".join(head + log + ([] if err else tail))
    if folder:
        try:
            os.makedirs(LOG_DIR, exist_ok=True)
            with open(os.path.join(LOG_DIR, "bergama_zone_base_log.txt"), "w", encoding="utf-8") as f:
                f.write(text)
        except Exception:
            pass
    status = "{} · {}".format(SHORT, "ERROR" if err else time.strftime("%H:%M") + " · {:.0f} s".format(secs))
    mem_set("last", text)
    mem_set("status", status)
    gh_status(status)
    if err:
        gh_message("error", err)
    return text


try:
    _txt = main()
except Exception as _ex:
    _txt = "ERROR: {}: {} ({})".format(type(_ex).__name__, _ex, VERSION)
    gh_status(SHORT + " · ERROR")
    mem_set("last", _txt)   # 25 Oct: the error stays on the log after the Button is released
    mem_set("status", SHORT + " · ERROR")
log = _txt
print(_txt)                  # 25 Oct 12:10: the canvas's log output is Grasshopper's "out" (printed text): print the log
if globals().get("_ran_now"):
    mem_set("done", done_text(True, "ERROR" not in str(mem_get("status", "")), time.time() - _T_START))
done = mem_get("done", "idle")   # 25 Oct 10:20: stays after the run; wire into the next script's run (one-click chain)
