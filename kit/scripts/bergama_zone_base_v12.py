# CURRENT VERSION: bergama_zone_base_v12.py = v12 (9 Nov 2026; Aras's masterplan SVG read live and baked as new Option_A::INT_ layers; what changed: the NEW IN / VERSION notes below)
"""BERGAMA ZONE BASE v12 (2026-11-09): bakes Group 6's zone layout, and the zones of Aras's own masterplan drawing,
into the open Rhino file as an editable base.

NEW IN v12 (round 8, P1, 9 Nov 2026; Aras 9 Nov 05:47, decisions S1-S7 as proposed):
  (1) Aras's masterplan SVG is READ LIVE on every press: Downloads/Bergama/Data/assets/masterlastversion.svg (run kit:
      Data/assets/masterlastversion.svg). Nothing of the drawing is kept in this script: change the SVG, press again.
      It is placed on site_alan (the SVG's plan frame, 7514.18 x 1397.44 units = site_alan 2,844.97 x 529.09 m,
      2.64121 units per m; the frame copy of the Selinos group is the true one). Its zones are baked as NEW layers
      under Option_A (each object: user text source=svg, svg_group, kind, label, id, study_area, zone where meaningful,
      base_hash):
        INT_WATER_design            Selinos as he drew it = the design water (S2)                    closed curves
        INT_ZONE_WETLAND            wetland fills (part shallow_reeds / open_water)                   closed curves
        INT_ZONE_PLAZA              event plaza fills (group Layer_16)                                closed curves
        INT_ZONE_HERITAGE_SETTING   the 4 old-settlement rings round Kızıl Avlu (ring 1 = innermost)  closed curves
        INT_PATH_park               park paths (group seconder)                                       closed curves
        INT_PATH_walk               walk fills (part walk / paving / bridge_deck / grey_steps)        closed curves
        INT_PATH_bike               bike lane fills                                                   closed curves
        INT_ROUTE_circulation       circulation route lines, each run the way its arrows point       open curves
        INT_ROUTE_footbridge        the route's footbridge lines                                      open curves
        INT_PLANT_shrubgroup        rosemary symbols = shrub groups at the size drawn (S3)            circles
      A ring that is a hole in its fill carries hole=1 (and hole_in = the id of the ring round it).
  (2) NOT baked from the SVG: the trees (S5: MasterPlan regenerates them by its rules; their measured counts, crown
      sizes, spacing and zone shares go to the log and to Downloads/Bergama/cached/bergama_zone_base/
      svg_reference.json), the 25 m green corridor (S2: MasterPlan recomputes it as 25 m from INT_WATER_design), the reed
      tufts (a look: their density is in the json), the heritage trail (S4: only an 8 m stub is drawn; logged), the AI
      render, topography rasters, wall picture, asset drawings, labels and legend (S7), the survey context (roads,
      buildings, heritage blocks, Kızıl Avlu outline, contours, open meadow = the whole site rectangle, not a zone).
      The ground layer (ground_topt) sits 21.7 units (8.2 m) left of the plan frame in the SVG; it is shifted onto it
      before the green corridor is measured (S1).
  (3) The old base (BASE_DATA: WA beds, GR, WP, DG, WS, WT, WD, the strip, links, cleared buildings, labels, wetland
      edges) is baked exactly as in v11.2 (S6). No SVG, an unreadable SVG or any SVG check that fails: a WARNING line,
      the old base is baked, nothing stops; objects baked from an earlier SVG are then left as they are.
  (4) Your edits survive a press as before: only objects still exactly as baked are replaced (base_hash), for the
      SVG layers too (each SVG piece has a fixed base_id: A-svg-<layer>-<n>, n in the SVG's drawing order).

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
  one press bakes the whole base into the open Rhino file, under Option_A::INT_... (v9: option A only). These are the
  INT_ layers that bergama_masterplan reads, so after editing you press Build on the masterplan component.

  What is baked from the built-in base (the revised draft of 17-18 Oct, mp2/draft2/make_draft_markup_v2.py, checked
  against CONCEPT_RECORD v2.3 sections 3.3-3.6, 5.2, 5.4):
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
    Arrows INT_LINK_water / INT_LINK_people / INT_LINK_flood: 11, every one passes bergama_masterplan v6's
           link_check, and every water arrow points downstream.
           NEW IN v5 (Aras 15:03 "have the interaction arrows from the closest place possible always"): each arrow
           joins the two closest points of what it links (2.5 m inside each zone) along a line that crosses no third
           zone; a river end sits on open strip at or upstream of the zone it feeds, at or downstream of the zone it
           drains, so no arrow shows water running uphill. Every river end stays at least 1.5 m off any zone edge.
  Every size of the built-in base is a PLACEHOLDER, not a design size: each zone's user text `basis` says what it was
  sized on (open ground between surveyed obstacles, legibility). No storage volume, level or flow is drawn.
  What is baked from the SVG: see NEW IN v12 above (sizes as Aras drew them).

RULES IT KEEPS
  * It bakes only into a file whose study areas (aras_alan, begum_alan, nil_alan) sit where the course survey has
    them (within 5 cm): the base is in survey coordinates. Any other file: ERROR, nothing is baked.
  * The study-area curves are never touched.
  * YOUR EDITS ARE KEPT. Each baked object carries user text `base_hash` (its shape when baked). Pressing again
    deletes and re-bakes only the objects still exactly as baked; an object you moved, reshaped or recoloured
    stays, and its piece is not baked again. An object you deleted comes back on the next press.

INPUTS (any case; only the button is needed)
  run      Button
  option   ignored since v9 (option A only)

OUTPUT
  log: the log. It stays readable after the button is released, and is also written to
  Downloads/Bergama/logs/bergama_zone_base_log.txt.
  done: "done HH:MM:SS.ss · N s" after a good press (wire it into the next script's run: one-click chain).
  File: Downloads/Bergama/cached/bergama_zone_base/svg_reference.json (v12: the SVG's measured trees, shrub groups,
  reeds, route and legend colours, for MasterPlan to calibrate its rules against).
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

VERSION = "bergama_zone_base v12 (2026-11-09)"  # v12 round 8 P1: Aras's masterplan SVG (Data/assets/masterlastversion.svg) read live, its zones baked as new Option_A::INT_ layers (source=svg), trees measured into cached/bergama_zone_base/svg_reference.json; older: v11.2 fix (round 5 S5, CHK-12): the function bake() is now zb_bake(): a Button input named `bake` (offered below) read the function, so a press did nothing, as run() did in v11.1; v11.1 fix 1 Nov 16:40: the function run() replaced the Button input `run`, so a press did nothing; renamed main(); v11 round 4 S1: common/trigger.py (one start-up rule), bridge names on the K4/K5 dots; older: v10.2 fix 1 Nov 08:20: chain trigger keyed to each solve (Rhino keeps globals), so the chain continues after ZoneBase; v10.1 fix 1 Nov: a pasted or rewired component no longer runs by itself (chain trigger notes the wire on its first solve)
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
SHORT = "v12"
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
    "INT_LINK_water": "32525F", "INT_LINK_people": "8C1C32", "INT_LINK_flood": "5D7F8D",
    # v12: the layers baked from Aras's SVG, in the colours of his legend
    "INT_WATER_design": "51626C", "INT_ZONE_WETLAND": "A9C4C2", "INT_ZONE_PLAZA": "E3E5E5",
    "INT_ZONE_HERITAGE_SETTING": "F6E3DF", "INT_PATH_park": "8C8A6D", "INT_PATH_walk": "E8CFCF", "INT_PATH_bike": "A8705C",
    "INT_ROUTE_circulation": "BE3D72", "INT_ROUTE_footbridge": "BE3D72", "INT_PLANT_shrubgroup": "87967B"}
SVG_FILE = "masterlastversion.svg"                 # v12: Aras's masterplan, Downloads/Bergama/Data/assets/ (read live)
SVG_REF_JSON = "svg_reference.json"                # v12: in Downloads/Bergama/cached/bergama_zone_base/
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


def ensure_layer(doc, path, colour=None):
    """the layer's index; a new layer takes `colour` (hex) if given, else its LAYER_COLOURS tone"""
    idx = doc.Layers.FindByFullPath(path, -1)
    if idx >= 0:
        return idx
    parent, _, name = path.rpartition("::")
    lay = Rhino.DocObjects.Layer()
    lay.Name = name
    if parent:
        lay.ParentLayerId = doc.Layers[ensure_layer(doc, parent)].Id
    h = (colour or "").lstrip("#").upper() or LAYER_COLOURS.get(name)
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


# ================================================================ SVG READER (stdlib only) BEGIN
# v12: Aras's masterplan SVG (Downloads/Bergama/Data/assets/masterlastversion.svg) is read LIVE on every press; nothing
# of it is kept in this script. Parts copied from bergama_plan_to_rhino_v2 (path parser, transforms, placing).
import re as _re
import math as _m
SVG_NS = "{http://www.w3.org/2000/svg}"
SVG_XLINK = "{http://www.w3.org/1999/xlink}href"
_SVG_NUM = _re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")
SVG_ID = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
SVG_FLAT_U = 2.0                 # a curve piece of the SVG becomes straight pieces of about this length (units, ~0.76 m)


def svg_mul(a, b):
    """affine a*b (a after b); (a, b, c, d, e, f): x' = a x + c y + e, y' = b x + d y + f"""
    return (a[0] * b[0] + a[2] * b[1], a[1] * b[0] + a[3] * b[1],
            a[0] * b[2] + a[2] * b[3], a[1] * b[2] + a[3] * b[3],
            a[0] * b[4] + a[2] * b[5] + a[4], a[1] * b[4] + a[3] * b[5] + a[5])


def svg_pt(m, p):
    return (m[0] * p[0] + m[2] * p[1] + m[4], m[1] * p[0] + m[3] * p[1] + m[5])


def svg_scale(m):
    return _m.sqrt(abs(m[0] * m[3] - m[1] * m[2])) or 1.0


def svg_num(v, dflt=0.0):
    n = _SVG_NUM.findall(v or "")
    return float(n[0]) if n else dflt


def svg_transform(s):
    m = SVG_ID
    for name, args in _re.findall(r"(\w+)\s*\(([^)]*)\)", s or ""):
        v = [float(x) for x in _SVG_NUM.findall(args)]
        if name == "matrix" and len(v) == 6:
            t = tuple(v)
        elif name == "translate" and v:
            t = (1.0, 0.0, 0.0, 1.0, v[0], v[1] if len(v) > 1 else 0.0)
        elif name == "scale" and v:
            t = (v[0], 0.0, 0.0, v[1] if len(v) > 1 else v[0], 0.0, 0.0)
        elif name == "rotate" and v:
            a = _m.radians(v[0])
            r = (_m.cos(a), _m.sin(a), -_m.sin(a), _m.cos(a), 0.0, 0.0)
            t = svg_mul((1.0, 0.0, 0.0, 1.0, v[1], v[2]), svg_mul(r, (1.0, 0.0, 0.0, 1.0, -v[1], -v[2]))) \
                if len(v) == 3 else r
        elif name == "skewX" and v:
            t = (1.0, 0.0, _m.tan(_m.radians(v[0])), 1.0, 0.0, 0.0)
        elif name == "skewY" and v:
            t = (1.0, _m.tan(_m.radians(v[0])), 0.0, 1.0, 0.0, 0.0)
        else:
            continue
        m = svg_mul(m, t)
    return m


def svg_colour(v):
    """'#rgb' / '#rrggbb' -> '#rrggbb' (lower case); none / url(...) / unknown -> None"""
    v = (v or "").strip().lower()
    if not v.startswith("#"):
        return {"black": "#000000", "white": "#ffffff"}.get(v)
    h = v[1:]
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return "#" + h if len(h) == 6 and all(c in "0123456789abcdef" for c in h) else None


def svg_cubic(a, b, c, e):
    """one cubic piece as points (a excluded), about SVG_FLAT_U apart"""
    L = _m.hypot(b[0] - a[0], b[1] - a[1]) + _m.hypot(c[0] - b[0], c[1] - b[1]) + _m.hypot(e[0] - c[0], e[1] - c[1])
    n = max(1, min(48, int(_m.ceil(L / SVG_FLAT_U))))
    out = []
    for k in range(1, n + 1):
        t = k / float(n)
        u = 1.0 - t
        out.append((u * u * u * a[0] + 3 * u * u * t * b[0] + 3 * u * t * t * c[0] + t * t * t * e[0],
                    u * u * u * a[1] + 3 * u * u * t * b[1] + 3 * u * t * t * c[1] + t * t * t * e[1]))
    return out


def svg_arc(p0, rx, ry, phi, large, sweep, p1):
    """an elliptical arc as points (p0 excluded), W3C implementation notes F.6"""
    if rx == 0 or ry == 0 or p0 == p1:
        return [p1]
    ph = _m.radians(phi)
    cp, sp = _m.cos(ph), _m.sin(ph)
    dx, dy = (p0[0] - p1[0]) / 2.0, (p0[1] - p1[1]) / 2.0
    x1, y1 = cp * dx + sp * dy, -sp * dx + cp * dy
    lam = (x1 * x1) / (rx * rx) + (y1 * y1) / (ry * ry)
    if lam > 1:
        rx, ry = rx * _m.sqrt(lam), ry * _m.sqrt(lam)
    nu = rx * rx * ry * ry - rx * rx * y1 * y1 - ry * ry * x1 * x1
    de = rx * rx * y1 * y1 + ry * ry * x1 * x1
    co = _m.sqrt(max(0.0, nu / de)) if de else 0.0
    if large == sweep:
        co = -co
    cx1, cy1 = co * rx * y1 / ry, -co * ry * x1 / rx
    cx, cy = cp * cx1 - sp * cy1 + (p0[0] + p1[0]) / 2.0, sp * cx1 + cp * cy1 + (p0[1] + p1[1]) / 2.0
    ang = lambda ux, uy, vx, vy: _m.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
    t1 = ang(1, 0, (x1 - cx1) / rx, (y1 - cy1) / ry)
    dt = ang((x1 - cx1) / rx, (y1 - cy1) / ry, (-x1 - cx1) / rx, (-y1 - cy1) / ry)
    if not sweep and dt > 0:
        dt -= 2 * _m.pi
    elif sweep and dt < 0:
        dt += 2 * _m.pi
    n = max(2, min(64, int(_m.ceil(abs(dt) * max(rx, ry) / SVG_FLAT_U))))
    out = []
    for k in range(1, n + 1):
        t = t1 + dt * k / float(n)
        out.append((cx + rx * _m.cos(t) * cp - ry * _m.sin(t) * sp, cy + rx * _m.cos(t) * sp + ry * _m.sin(t) * cp))
    out[-1] = p1
    return out


def svg_path_rings(d):
    """SVG path data -> [(closed, [points])] in the path's own units, curves flattened"""
    toks = _re.findall(r"[MmZzLlHhVvCcSsQqTtAa]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?", d or "")
    subs, cur, pos, start = [], None, (0.0, 0.0), (0.0, 0.0)
    i, cmd, last_c, last_q = [0], None, None, None

    def num():
        v = float(toks[i[0]])
        i[0] += 1
        return v
    while i[0] < len(toks):
        t = toks[i[0]]
        if t.isalpha():
            cmd = t
            i[0] += 1
            if cmd in "Zz":
                if cur is not None:
                    subs.append((True, cur))
                    cur = None
                pos = start
                last_c = last_q = None
                continue
        elif cmd is None:
            i[0] += 1
            continue
        try:
            rel = cmd.islower()
            c = cmd.upper()
            ox, oy = pos if rel else (0.0, 0.0)
            if c == "M":
                p = (num() + ox, num() + oy)
                if cur is not None:
                    subs.append((False, cur))
                cur, pos, start = [p], p, p
                cmd = "l" if rel else "L"
                last_c = last_q = None
                continue
            if cur is None:
                cur = [pos]
            if c == "L":
                p = (num() + ox, num() + oy)
                cur.append(p)
                last_c = last_q = None
            elif c == "H":
                p = (num() + ox, pos[1])
                cur.append(p)
                last_c = last_q = None
            elif c == "V":
                p = (pos[0], num() + oy)
                cur.append(p)
                last_c = last_q = None
            elif c in "CS":
                if c == "C":
                    c1 = (num() + ox, num() + oy)
                else:
                    c1 = (2 * pos[0] - last_c[0], 2 * pos[1] - last_c[1]) if last_c else pos
                c2 = (num() + ox, num() + oy)
                p = (num() + ox, num() + oy)
                cur.extend(svg_cubic(pos, c1, c2, p))
                last_c, last_q = c2, None
            elif c in "QT":
                if c == "Q":
                    q = (num() + ox, num() + oy)
                else:
                    q = (2 * pos[0] - last_q[0], 2 * pos[1] - last_q[1]) if last_q else pos
                p = (num() + ox, num() + oy)
                c1 = (pos[0] + 2.0 / 3.0 * (q[0] - pos[0]), pos[1] + 2.0 / 3.0 * (q[1] - pos[1]))
                c2 = (p[0] + 2.0 / 3.0 * (q[0] - p[0]), p[1] + 2.0 / 3.0 * (q[1] - p[1]))
                cur.extend(svg_cubic(pos, c1, c2, p))
                last_q, last_c = q, None
            elif c == "A":
                rx, ry, phi = abs(num()), abs(num()), num()
                fa, fs = num(), num()
                p = (num() + ox, num() + oy)
                cur.extend(svg_arc(pos, rx, ry, phi, fa != 0, fs != 0, p))
                last_c = last_q = None
            else:
                i[0] += 1
                continue
        except (IndexError, ValueError):
            break
        pos = p
    if cur is not None and len(cur) > 1:
        subs.append((False, cur))
    return [(cl, s) for cl, s in subs if len(s) > 1]


def svg_shape_rings(tag, el):
    """rect / circle / ellipse / line / polygon / polyline -> the same form as svg_path_rings"""
    f = lambda k: svg_num(el.get(k), 0.0)
    if tag == "rect":
        x, y, w, h = f("x"), f("y"), f("width"), f("height")
        return [(True, [(x, y), (x + w, y), (x + w, y + h), (x, y + h)])] if w > 0 and h > 0 else []
    if tag in ("circle", "ellipse"):
        cx, cy = f("cx"), f("cy")
        rx = f("r") if tag == "circle" else f("rx")
        ry = f("r") if tag == "circle" else f("ry")
        if rx <= 0 or ry <= 0:
            return []
        n = max(12, min(96, int(2 * _m.pi * max(rx, ry) / SVG_FLAT_U)))
        return [(True, [(cx + rx * _m.cos(2 * _m.pi * k / n), cy + ry * _m.sin(2 * _m.pi * k / n)) for k in range(n)])]
    if tag == "line":
        return [(False, [(f("x1"), f("y1")), (f("x2"), f("y2"))])]
    if tag in ("polygon", "polyline"):
        v = [float(x) for x in _SVG_NUM.findall(el.get("points", ""))]
        pts = list(zip(v[0::2], v[1::2]))
        return [(tag == "polygon", pts)] if len(pts) >= 2 else []
    return []


def svg_key(gid):
    """a group id without Illustrator's copy endings ("wetland_shallow_water_reeds_2" / "Selinos1" -> base form);
    Illustrator's own layer names (Layer_16) are kept whole"""
    g = (gid or "").strip()
    return g if _re.match(r"^Layer_\d+$", g) else _re.sub(r"(_\d+|\d+)$", "", g)


class SvgPlan(object):
    """The SVG read once (stdlib only). For every drawn piece under one of the wanted groups:
       dict(tag, groups (ids outer -> inner), fill, stroke, sw (units), op (opacity,
       multiplied down), dash, rings [(closed, [(u, v), ...])] in SVG units, frame (the plan-frame clip it sits in))
    (group ids as written in the SVG; svg_key() gives their base form)
    and for every <use> of a symbol: dict(groups, href, c (centre), w, h (units), frame). Images and texts are counted."""

    def __init__(self, path, want):
        import xml.etree.ElementTree as ET
        self.root = ET.parse(path).getroot()
        self.ids = {}
        for el in self.root.iter():
            if el.get("id"):
                self.ids[el.get("id")] = el
        self.clips = {}
        for cp in self.root.iter(SVG_NS + "clipPath"):
            for r in cp:
                if r.tag == SVG_NS + "rect":
                    m = svg_transform(r.get("transform"))
                    x, y, w, h = (svg_num(r.get(k), 0.0) for k in ("x", "y", "width", "height"))
                    a, b = svg_pt(m, (x, y)), svg_pt(m, (x + w, y + h))
                    self.clips[cp.get("id")] = (min(a[0], b[0]), min(a[1], b[1]), abs(b[0] - a[0]), abs(b[1] - a[1]))
        big = max(self.clips.values(), key=lambda r: r[2] * r[3]) if self.clips else None
        self.big = big
        # every clip rectangle of the plan frame's size (Illustrator keeps one copy per layer; they differ in place)
        self.frame_ids = set(k for k, r in self.clips.items() if big and abs(r[2] - big[2]) < 0.002 * big[2] and
                             abs(r[3] - big[3]) < 0.002 * big[3])
        self.want = want
        self.pieces, self.uses, self.n_img, self.n_text, self.group_frames = [], [], 0, 0, {}
        self.walk(self.root, SVG_ID, {"fill": "#000000", "stroke": "none", "stroke-width": "1"}, 1.0, (), None, False)

    def walk(self, el, m, st, op, groups, frame, keep):
        for ch in el:
            tag = ch.tag.replace(SVG_NS, "") if isinstance(ch.tag, str) else ""
            if tag in ("defs", "clipPath", "mask", "metadata", "style", "title", "desc", "linearGradient", "symbol",
                       "radialGradient", "pattern", "filter", "marker"):
                continue
            s2 = dict(st)
            for k in ("fill", "stroke", "stroke-width", "fill-rule", "stroke-dasharray", "display", "visibility"):
                if ch.get(k) is not None:
                    s2[k] = ch.get(k)
            for part in (ch.get("style") or "").split(";"):
                if ":" in part:
                    k, v = part.split(":", 1)
                    s2[k.strip().lower()] = v.strip()
            if s2.get("display", "").strip() == "none":
                continue
            o2 = op * svg_num(s2.pop("opacity", None) or ch.get("opacity"), 1.0)
            mm = svg_mul(m, svg_transform(ch.get("transform")))
            fr = frame
            cpv = _re.search(r"url\(\s*#([^)\s]+)\s*\)", ch.get("clip-path") or s2.get("clip-path") or "")
            if cpv and cpv.group(1) in self.frame_ids:
                fr = self.clips[cpv.group(1)]
            if tag in ("g", "a", "switch"):
                g2, k2 = groups, keep
                if tag == "g" and ch.get("id"):
                    g2 = groups + (ch.get("id"),)
                    k2 = keep or self.want(g2)
                if tag == "g" and fr is not None and frame is None and groups:
                    for gk in groups[-3:]:
                        self.group_frames.setdefault(svg_key(gk), fr)
                self.walk(ch, mm, s2, o2, g2, fr, k2)
                continue
            if not keep:
                continue
            if tag == "image":
                self.n_img += 1
                continue
            if tag == "text":
                self.n_text += 1
                continue
            if tag == "use":
                ref = (ch.get(SVG_XLINK) or ch.get("href") or "").lstrip("#")
                tgt = self.ids.get(ref)
                if tgt is None:
                    continue
                mu = svg_mul(mm, (1.0, 0.0, 0.0, 1.0, svg_num(ch.get("x")), svg_num(ch.get("y"))))
                if tgt.tag == SVG_NS + "symbol":
                    vb = [float(x) for x in _SVG_NUM.findall(tgt.get("viewBox") or "")]
                    w = svg_num(ch.get("width"), vb[2] if len(vb) == 4 else 0.0)
                    h = svg_num(ch.get("height"), vb[3] if len(vb) == 4 else 0.0)
                    s = svg_scale(mu)
                    self.uses.append({"groups": groups + ((ch.get("id"),) if ch.get("id") else ()),
                                      "href": ref, "c": svg_pt(mu, (w / 2.0, h / 2.0)), "w": w * s, "h": h * s,
                                      "frame": fr, "op": o2})
                continue
            if tag == "path":
                rings = svg_path_rings(ch.get("d"))
            elif tag in ("rect", "circle", "ellipse", "line", "polygon", "polyline"):
                rings = svg_shape_rings(tag, ch)
            else:
                continue
            fill = None if tag in ("line", "polyline") else svg_colour(s2.get("fill"))
            stroke = svg_colour(s2.get("stroke"))
            if not rings or (fill is None and stroke is None):
                continue
            rings = [(cl, [svg_pt(mm, p) for p in P]) for cl, P in rings]
            da = (s2.get("stroke-dasharray") or "").strip()
            self.pieces.append({"tag": tag, "groups": groups, "fill": fill, "stroke": stroke,
                                "sw": svg_num(s2.get("stroke-width"), 1.0) * svg_scale(mm), "op": o2,
                                "dash": da if da and da != "none" else "", "rings": rings, "frame": fr,
                                "evenodd": (s2.get("fill-rule") or "").strip() == "evenodd"})

    def under(self, key):
        """pieces / uses whose group chain holds `key` (exact, after svg_key) or a group starting with key + '*'"""
        def hit(gs):
            for g in gs:
                k = svg_key(g)
                if key.endswith("*") and k.startswith(key[:-1]) or k == key:
                    return True
            return False
        return [p for p in self.pieces if hit(p["groups"])], [u for u in self.uses if hit(u["groups"])]
# ---- placing (from bergama_plan_to_rhino_v2: the SVG's plan frame IS site_alan turned flat) ----
SITE_COPY = [(29388.015, 32540.503), (31220.325, 30364.153), (31625.069, 30704.915), (29792.759, 32881.264)]   # site_alan of Bergama_Altlik.3dm (25 Oct 08:25), used when the open file has none


def svg_site_turn(site):
    """the angle (rad) that turns site_alan's longest side horizontal, its eastern end to the right"""
    best = None
    for a, b in zip(site, site[1:] + site[:1]):
        L = _m.hypot(b[0] - a[0], b[1] - a[1])
        if best is None or L > best[0]:
            best = (L, b[0] - a[0], b[1] - a[1])
    _, vx, vy = best
    if vx < 0:
        vx, vy = -vx, -vy
    return -_m.atan2(vy, vx)


def svg_world_matrix(site, rect, notes):
    """SVG units -> survey metres: the plan frame rect (x, y, w, h) = site_alan turned flat (long side horizontal,
    upstream left). Returns (affine, units per m)."""
    rot = svg_site_turn(site)
    ca, sa = _m.cos(rot), _m.sin(rot)
    ox, oy = site[0]
    turned = [(ox + ca * (p[0] - ox) - sa * (p[1] - oy), oy + sa * (p[0] - ox) + ca * (p[1] - oy)) for p in site]
    x0, y0 = min(p[0] for p in turned), min(p[1] for p in turned)
    x1, y1 = max(p[0] for p in turned), max(p[1] for p in turned)
    rx, ry, rw, rh = rect
    sx, sy = rw / (x1 - x0), rh / (y1 - y0)
    s = (sx + sy) / 2.0
    notes.append(u"SVG placing: plan frame %.2f x %.2f units = site_alan %.2f x %.2f m (%.5f units per m; width and "
                 u"height agree to %.3f %%)" % (rw, rh, x1 - x0, y1 - y0, s, abs(sx - sy) / s * 100.0))
    if abs(sx - sy) / s > 0.01:
        notes.append(u"WARNING SVG placing: the frame's width and height scales differ by %.1f %%: is the biggest clip "
                     u"rectangle still the plan frame?" % (abs(sx - sy) / s * 100.0))
    if abs(s - 2.64121) / 2.64121 > 0.01:
        notes.append(u"WARNING SVG placing: %.4f units per m, the 9 Nov file had 2.64121: did the sheet scale change?" % s)
    A = (1.0 / s, 0.0, 0.0, -1.0 / s, x0 - rx / s, y0 + (ry + rh) / s)
    Ri = (ca, -sa, sa, ca, ox - ca * ox - sa * oy, oy + sa * ox - ca * oy)
    return svg_mul(Ri, A), s


# ---- plane geometry in metres ----
def g_area(P):
    """signed area (shoelace) of a ring given without its closing point"""
    return 0.5 * sum(P[k - 1][0] * P[k][1] - P[k][0] * P[k - 1][1] for k in range(len(P)))


def g_len(P):
    return sum(_m.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(P[:-1], P[1:]))


def g_pip(x, y, P):
    ins, j = False, len(P) - 1
    for i in range(len(P)):
        xi, yi = P[i]
        xj, yj = P[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi:
            ins = not ins
        j = i
    return ins


def g_bbox(P):
    return (min(p[0] for p in P), min(p[1] for p in P), max(p[0] for p in P), max(p[1] for p in P))


def g_inner_pt(P):
    """a point inside ring P (the centroid when inside, else the middle of the widest horizontal chord)"""
    a = g_area(P)
    if abs(a) > 1e-9:
        cx = sum((P[k - 1][0] + P[k][0]) * (P[k - 1][0] * P[k][1] - P[k][0] * P[k - 1][1]) for k in range(len(P))) / (6 * a)
        cy = sum((P[k - 1][1] + P[k][1]) * (P[k - 1][0] * P[k][1] - P[k][0] * P[k - 1][1]) for k in range(len(P))) / (6 * a)
        if g_pip(cx, cy, P):
            return (cx, cy)
    bb = g_bbox(P)
    best = None
    for f in (0.5, 0.3, 0.7, 0.2, 0.8, 0.4, 0.6):
        y = bb[1] + f * (bb[3] - bb[1])
        xs = sorted(P[i - 1][0] + (y - P[i - 1][1]) * (P[i][0] - P[i - 1][0]) / ((P[i][1] - P[i - 1][1]) or 1e-12)
                    for i in range(len(P)) if (P[i][1] > y) != (P[i - 1][1] > y))
        for a_, b_ in zip(xs[0::2], xs[1::2]):
            if best is None or b_ - a_ > best[0]:
                best = (b_ - a_, ((a_ + b_) / 2.0, y))
    return best[1] if best else P[0]


def g_clip_ring(P, F):
    """Sutherland-Hodgman: ring P cut to rectangle F = (x, y, w, h)"""
    x0, y0, x1, y1 = F[0], F[1], F[0] + F[2], F[1] + F[3]
    for inside, cut in ((lambda p: p[0] >= x0, lambda a, b: (x0, a[1] + (b[1] - a[1]) * (x0 - a[0]) / (b[0] - a[0]))),
                        (lambda p: p[0] <= x1, lambda a, b: (x1, a[1] + (b[1] - a[1]) * (x1 - a[0]) / (b[0] - a[0]))),
                        (lambda p: p[1] >= y0, lambda a, b: (a[0] + (b[0] - a[0]) * (y0 - a[1]) / (b[1] - a[1]), y0)),
                        (lambda p: p[1] <= y1, lambda a, b: (a[0] + (b[0] - a[0]) * (y1 - a[1]) / (b[1] - a[1]), y1))):
        if not P:
            break
        out = []
        for i in range(len(P)):
            a, b = P[i - 1], P[i]
            if inside(b):
                if not inside(a):
                    out.append(cut(a, b))
                out.append(b)
            elif inside(a):
                out.append(cut(a, b))
        P = out
    return P


def g_clip_line(P, F):
    """an open polyline cut to rectangle F: the pieces inside (Liang-Barsky per segment)"""
    x0, y0, x1, y1 = F[0], F[1], F[0] + F[2], F[1] + F[3]
    pieces, cur = [], []
    for a, b in zip(P[:-1], P[1:]):
        t0, t1, dx, dy = 0.0, 1.0, b[0] - a[0], b[1] - a[1]
        ok = True
        for p_, q_ in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
            if p_ == 0:
                if q_ < 0:
                    ok = False
                    break
            else:
                r = q_ / p_
                if p_ < 0:
                    t0 = max(t0, r)
                else:
                    t1 = min(t1, r)
        if not ok or t0 > t1:
            if len(cur) > 1:
                pieces.append(cur)
            cur = []
            continue
        pa = (a[0] + t0 * dx, a[1] + t0 * dy)
        pb = (a[0] + t1 * dx, a[1] + t1 * dy)
        if not cur or cur[-1] != pa:
            if len(cur) > 1:
                pieces.append(cur)
            cur = [pa]
        cur.append(pb)
        if t1 < 1.0:
            pieces.append(cur)
            cur = []
    if len(cur) > 1:
        pieces.append(cur)
    return pieces


def g_clean(P, closed, tol=0.002):
    """drop repeated points (closer than tol m); a closed ring loses its closing point"""
    out = []
    for p in P:
        if not out or _m.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) > tol:
            out.append(p)
    if closed and len(out) > 2 and _m.hypot(out[0][0] - out[-1][0], out[0][1] - out[-1][1]) <= tol:
        out.pop()
    return out


def g_seg_dist(p, a, b):
    """(distance from p to segment ab, unit direction of ab)"""
    dx, dy = b[0] - a[0], b[1] - a[1]
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
    L = _m.sqrt(L2) or 1.0
    return _m.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy), (dx / L, dy / L)


def g_pct(v, q):
    """the q-quantile (0..1) of the values v (linear between ranks), None for none"""
    v = sorted(v)
    if not v:
        return None
    k = (len(v) - 1) * q
    f = int(_m.floor(k))
    c = min(f + 1, len(v) - 1)
    return round(v[f] + (v[c] - v[f]) * (k - f), 2)


def g_nn(pts, cell=40.0):
    """nearest-neighbour distance of each point (grid buckets)"""
    grid = {}
    for i, p in enumerate(pts):
        grid.setdefault((int(_m.floor(p[0] / cell)), int(_m.floor(p[1] / cell))), []).append(i)
    out = []
    for i, p in enumerate(pts):
        gx, gy = int(_m.floor(p[0] / cell)), int(_m.floor(p[1] / cell))
        best, r = None, 1
        while best is None or best > (r - 1) * cell:
            for ix in range(gx - r, gx + r + 1):
                for iy in range(gy - r, gy + r + 1):
                    for j in grid.get((ix, iy), ()):
                        if j != i:
                            d = _m.hypot(pts[j][0] - p[0], pts[j][1] - p[1])
                            if best is None or d < best:
                                best = d
            r += 1
            if r > 60:
                break
        if best is not None:
            out.append(best)
    return out


# ---- what is taken out of the SVG (group id in the SVG, after svg_key) ----
SVG_WANT = ("Selinos", "wetland_shallow_water_reeds", "green_corridor_open_ground_within_25_m_of_the_water",
            "open_meadow", "old_settlement_round_Kizil_Avlu_eski_yerlesim_light_red_grad", "walks_paths_bike_lane",
            "seconder", "Layer_16", "route_line", "route_footbridges", "route_arrows",
            "heritage_trail_along_the_walks", "heritage_trail", "trees_group", "LEGEND")
SVG_WALK_FILL = {                          # walks_paths_bike_lane: fill -> (layer, kind, part); strokes are look only
    "#e8cfcf": ("INT_PATH_walk", "walk", "walk"),             # = legend_walk
    "#a8705c": ("INT_PATH_bike", "bike_lane", "bike_lane"),   # = legend_bike
}
SVG_PAVING_FILLS = ("#efddda", "#eee5e1", "#f3edea", "#f8f5f3", "#e9ded8", "#e8e0c8", "#fafaf7")
SVG_DECK_FILLS = ("#8e918a", "#9c9f99")                # grey fills at the footbridge ends (0-5 m from them)
SVG_GREY_FILLS = ("#b2b4af", "#c9cac7", "#e1e2e0")      # three grey tones drawn together (steps?), 50-800 m from a bridge
SVG_REED_FILLS = ("#8da77a", "#7f9b6c", "#9db488")
SVG_MIN_M2 = 1.0                           # rings smaller than this (m2) are slivers: not baked
SVG_ARROW_NEAR_M = 6.0                     # an arrow within this of a route line gives that line its direction


def svg_want(groups):
    return any(svg_key(g) in SVG_WANT or svg_key(g).startswith("legend_") for g in groups)


def svg_frame_of(plan, notes):
    """(the plan frame, the ground layer's shift in units): the frame = the frame clip of the Selinos group (water
    frame), else the commonest frame-size clip; S1 (Aras 9 Nov): the ground_topt copy sits 21.7 units (8.2 m) left of
    it and is shifted onto it"""
    gf = plan.group_frames
    fr = gf.get("Selinos") or gf.get("wetland_shallow_water_reeds")
    if fr is None:
        cnt = {}
        for k in plan.frame_ids:
            r = tuple(round(x, 1) for x in plan.clips[k])
            cnt[r] = cnt.get(r, 0) + 1
        fr = max(cnt, key=cnt.get) if cnt else plan.big
        notes.append(u"WARNING SVG: no frame clip on the Selinos group; the commonest frame copy was used")
    g = gf.get("green_corridor_open_ground_within_25_m_of_the_water") or gf.get("open_meadow")
    shift = (fr[0] - g[0], fr[1] - g[1]) if g else (0.0, 0.0)
    others = sorted(set((round(r[0] - fr[0], 2), round(r[1] - fr[1], 2)) for k, r in gf.items()
                        if k not in ("ground_topography", "open_meadow", "green_corridor_open_ground_within_25_m_of_the_water",
                                     "ground_height_bands_survey_contours_low_dark")))
    notes.append(u"SVG frame: the Selinos frame copy at (%.2f, %.2f); ground_topt shifted by (%+.2f, %+.2f) units onto "
                 u"it (S1); other plan layers' frame copies lie %s units from it (not shifted)" % (
                     fr[0], fr[1], shift[0], shift[1], u", ".join(u"(%+.2f, %+.2f)" % d for d in others) or u"0"))
    return fr, shift


def svg_rings_m(piece, M, shift=(0.0, 0.0), clip=True):
    """a piece's rings cut at its frame (as drawn), moved by shift (units), in survey m: [(closed, [(x, y)])]"""
    out = []
    F = piece["frame"]
    for cl, P in piece["rings"]:
        if clip and F is not None:
            if cl:
                Q = g_clip_ring(P, F)
                parts = [Q] if len(Q) >= 3 else []
            else:
                parts = g_clip_line(P, F)
        else:
            parts = [P]
        for Q in parts:
            W = g_clean([svg_pt(M, (p[0] + shift[0], p[1] + shift[1])) for p in Q], cl)
            if len(W) >= (3 if cl else 2):
                out.append((cl, W))
    return out


def g_wind(x, y, P):
    """winding number of ring P round (x, y)"""
    w, n = 0, len(P)
    for i in range(n):
        a, b = P[i - 1], P[i]
        if a[1] <= y < b[1] and (b[0] - a[0]) * (y - a[1]) - (x - a[0]) * (b[1] - a[1]) > 0:
            w += 1
        elif b[1] <= y < a[1] and (b[0] - a[0]) * (y - a[1]) - (x - a[0]) * (b[1] - a[1]) < 0:
            w -= 1
    return w


def svg_holes(rings, evenodd=True):
    """[(ring, depth)] for the closed rings of one piece: depth = how many of the piece's larger rings hold it; a ring
    is a hole (depth returned odd) when the fill just inside it is off by the piece's fill rule (evenodd: odd depth;
    nonzero: the winding of the larger rings and its own adds up to 0)"""
    out = []
    for i, (cl, P) in enumerate(rings):
        q = g_inner_pt(P)
        big = [Q for j, (cl2, Q) in enumerate(rings) if j != i and abs(g_area(Q)) > abs(g_area(P)) and g_pip(q[0], q[1], Q)]
        d = len(big)
        if not evenodd and d:
            w = sum(1 if g_area(Q) > 0 else -1 for Q in big) + (1 if g_area(P) > 0 else -1)
            d = 1 if w == 0 else 2
        out.append((P, d))
    return out


def svg_zone_items(plan, M, s, shift, notes):
    """the SVG's zones as base items (survey m) + the svg_reference stats. Each item: dict(layer (under Option_A),
    kind ("SVG" / "SVG_LINE" / "SVG_CIRCLE"), P, closed, name, meta (user text), bid)."""
    items, ref, counts, seen, dup = [], {}, {}, set(), [0]
    m_per_u = 1.0 / s

    def add(layer, P, closed, meta, svg_group, piece=None):
        sig = (layer, closed, len(P), tuple(sorted((round(p[0], 2), round(p[1], 2)) for p in P[:: max(1, len(P) // 16)])))
        if sig in seen:                                      # the same shape drawn twice (stacked copies): once
            dup[0] += 1
            return False
        seen.add(sig)
        k = counts.get(layer, 0) + 1
        counts[layer] = k
        mt = {"source": "svg", "svg_group": svg_group}
        mt.update(meta)
        if piece is not None:
            mt["svg_fill"] = piece.get("fill") or piece.get("stroke") or ""
            mt["svg_opacity"] = "%.2f" % piece.get("op", 1.0)
        if closed:
            mt["area_m2"] = "%.1f" % abs(g_area(P))
        else:
            mt["length_m"] = "%.1f" % g_len(P)
        mt.setdefault("id", u"SVG-%s-%d" % (layer.replace("INT_", "").replace("_", "-").upper(), k))
        items.append({"layer": "Option_A::" + layer, "kind": "SVG_LINE" if not closed else "SVG", "P": P,
                      "closed": closed, "name": mt.get("label", ""), "meta": mt,
                      "bid": u"A-svg-%s-%d" % (layer, k)})
        return True

    def areas(pieces, layer, meta_fn, label):
        n_small = 0
        for pc in pieces:
            rings = [r for r in svg_rings_m(pc, M) if r[0]]
            outers = []
            for P, depth in sorted(svg_holes(rings, pc["evenodd"]), key=lambda t: t[1]):
                if abs(g_area(P)) < SVG_MIN_M2:
                    n_small += 1
                    continue
                if g_area(P) < 0:
                    P = P[::-1]                                  # counter-clockwise, as the masterplan reads zones
                mt = dict(meta_fn(pc))
                mt.setdefault("label", label)
                if depth % 2:
                    mt["hole"] = "1"
                    q = g_inner_pt(P)
                    own = [(abs(g_area(Q)), i_) for Q, i_ in outers if g_pip(q[0], q[1], Q)]
                    if own:
                        mt["hole_in"] = min(own)[1]
                ok = add(layer, P, True, mt, svg_key(next((g for g in reversed(pc["groups"]) if svg_key(g) in SVG_WANT),
                                                          pc["groups"][-1] if pc["groups"] else "")), pc)
                if ok and not depth % 2:
                    outers.append((P, items[-1]["meta"]["id"]))
        return n_small

    # 1 design water (S2)
    pcs, _ = plan.under("Selinos")
    pcs = [p for p in pcs if p["fill"]]
    if not pcs:
        notes.append(u"WARNING SVG: no Selinos group (design water) found: INT_WATER_design not baked")
    small = areas(pcs, "INT_WATER_design", lambda pc: {"kind": "water_design", "zone": "W"}, u"SELINOS (DESIGN WATER)")
    # 2 wetland zone (fills; the reed tufts are a look, regenerated: stats only)
    pcs, _ = plan.under("wetland_shallow_water_reeds")
    wet = [p for p in pcs if p["fill"] and p["fill"] not in SVG_REED_FILLS]
    reeds = [p for p in pcs if p["fill"] in SVG_REED_FILLS]
    if not wet:
        notes.append(u"WARNING SVG: no wetland fills found: INT_ZONE_WETLAND not baked")
    small += areas(wet, "INT_ZONE_WETLAND", lambda pc: {"kind": "wetland", "zone": "W", "part": "open_water"
                   if pc["fill"] == "#5d8980" else "shallow_reeds"}, u"WETLAND")
    # 3 plaza (Layer_16 fills; its image is the AI render: not baked)
    pcs, _ = plan.under("Layer_16")
    pcs = [p for p in pcs if p["fill"]]
    if not pcs:
        notes.append(u"WARNING SVG: no plaza fills (group Layer_16) found: INT_ZONE_PLAZA not baked")
    small += areas(pcs, "INT_ZONE_PLAZA", lambda pc: {"kind": "plaza", "zone": "D"}, u"EVENT PLAZA")
    # 4 park paths (seconder)
    pcs, _ = plan.under("seconder")
    pcs = [p for p in pcs if p["fill"]]
    if not pcs:
        notes.append(u"WARNING SVG: no park paths (group seconder) found: INT_PATH_park not baked")
    small += areas(pcs, "INT_PATH_park", lambda pc: {"kind": "park_path"}, u"PARK PATH")
    # 5 walks and bike lane (fills; edge lines, joints and the bike centre dash are the look: not baked)
    pcs, _ = plan.under("walks_paths_bike_lane")
    walk_other = {}
    for pc in pcs:
        f = pc["fill"]
        if f in SVG_WALK_FILL:
            lay, kind, part = SVG_WALK_FILL[f]
        elif f in SVG_PAVING_FILLS:
            lay, kind, part = "INT_PATH_walk", "walk", "paving"
        elif f in SVG_DECK_FILLS:
            lay, kind, part = "INT_PATH_walk", "walk", "bridge_deck"
        elif f in SVG_GREY_FILLS:
            lay, kind, part = "INT_PATH_walk", "walk", "grey_steps"
        else:
            if f:
                walk_other[f] = walk_other.get(f, 0) + 1
            continue
        small += areas([pc], lay, lambda pc_, k_=kind, p_=part: {"kind": k_, "part": p_},
                       {"walk": u"WALK", "paving": u"WALK PAVING", "bridge_deck": u"BRIDGE DECK",
                        "grey_steps": u"GREY STEPS", "bike_lane": u"BIKE LANE"}[part])
    if walk_other:
        notes.append(u"SVG walks: fills of no known kind, not baked: " + u", ".join(u"%s x%d" % kv for kv in sorted(walk_other.items())))
    # 6 old-settlement rings (ring 1 = innermost)
    pcs, _ = plan.under("old_settlement_round_Kizil_Avlu_eski_yerlesim_light_red_grad")
    rings = []
    for pc in pcs:
        if pc["fill"]:
            for cl, P in svg_rings_m(pc, M):
                if cl and abs(g_area(P)) >= SVG_MIN_M2:
                    rings.append((abs(g_area(P)), P, pc))
    rings.sort(key=lambda t: t[0])
    if not rings:
        notes.append(u"WARNING SVG: no old-settlement rings found: INT_ZONE_HERITAGE_SETTING not baked")
    for k, (a, P, pc) in enumerate(rings):
        if g_area(P) < 0:
            P = P[::-1]
        add("INT_ZONE_HERITAGE_SETTING", P, True, {"kind": "heritage_setting", "ring": str(k + 1),
            "rings": str(len(rings)), "around": u"Kızıl Avlu",
            "label": u"OLD SETTLEMENT SETTING %d" % (k + 1)}, "old_settlement_round_Kizil_Avlu_eski_yerlesim_light_red_grad", pc)
    # 7 circulation route + footbridges, direction from the arrows
    arrows = []
    for pc in plan.under("route_arrows")[0]:
        for cl, P in svg_rings_m(pc, M):
            V = g_clean(P, True, 0.05)
            if len(V) < 3:
                continue
            if len(V) > 3:                                   # a curved arrow: its three corners = the sharpest turns
                V = sorted(V, key=lambda p: -min(_m.hypot(p[0] - q[0], p[1] - q[1]) for q in V if q is not p))[:3]
            sides = [(_m.hypot(V[(i + 1) % 3][0] - V[(i + 2) % 3][0], V[(i + 1) % 3][1] - V[(i + 2) % 3][1]), i) for i in range(3)]
            i = min(sides)[1]                                # the apex faces the shortest side (the base)
            a, b, c = V[i], V[(i + 1) % 3], V[(i + 2) % 3]
            mid = ((b[0] + c[0]) / 2.0, (b[1] + c[1]) / 2.0)
            L = _m.hypot(a[0] - mid[0], a[1] - mid[1]) or 1.0
            arrows.append(((a[0] + b[0] + c[0]) / 3.0, (a[1] + b[1] + c[1]) / 3.0, (a[0] - mid[0]) / L, (a[1] - mid[1]) / L, L))
    lines = []
    for grp, lay, kind, lab in (("route_line", "INT_ROUTE_circulation", "route", u"CIRCULATION ROUTE"),
                                ("route_footbridges", "INT_ROUTE_footbridge", "footbridge", u"FOOTBRIDGE")):
        pcs, _ = plan.under(grp)
        if not pcs:
            notes.append(u"WARNING SVG: no %s group found: %s not baked" % (grp, lay))
        for pc in pcs:
            for cl, P in svg_rings_m(pc, M):
                if cl:
                    P = P + [P[0]]
                if g_len(P) >= 1.0:
                    lines.append([P, lay, kind, lab, pc, 0, 0, grp])
    n_far = 0
    for x, y, ux, uy, L in arrows:
        best = None
        for ln in lines:
            P = ln[0]
            for a, b in zip(P[:-1], P[1:]):
                d, t = g_seg_dist((x, y), a, b)
                if best is None or d < best[0]:
                    best = (d, ln, t)
        if best is None or best[0] > SVG_ARROW_NEAR_M:
            n_far += 1
            continue
        if best[2][0] * ux + best[2][1] * uy >= 0:
            best[1][5] += 1
        else:
            best[1][6] += 1
    for P, lay, kind, lab, pc, fw, bw, grp in lines:
        if bw > fw:
            P, fw, bw = P[::-1], bw, fw                      # the curve now runs the way most arrows point
        add(lay, P, False, {"kind": kind, "label": lab, "arrows_with": str(fw), "arrows_against": str(bw),
            "direction": "one-way" if fw and not bw else ("two-way" if fw and bw else "none")}, grp, pc)
    if n_far:
        notes.append(u"SVG route: %d of %d arrows lie more than %.0f m from every route line (no direction from them)" % (
            n_far, len(arrows), SVG_ARROW_NEAR_M))
    # 8 shrub groups (S3): rosemary symbols at the size drawn
    sym_all = [u for u in plan.uses if not any(svg_key(g) == "LEGEND" or svg_key(g).startswith("legend_") for g in u["groups"])]
    shrubs = [u for u in sym_all if u["href"] == "sym_rosemary"]
    for u in shrubs:
        c = svg_pt(M, u["c"])
        d = (u["w"] + u["h"]) / 2.0 * m_per_u
        k = counts.get("INT_PLANT_shrubgroup", 0) + 1
        counts["INT_PLANT_shrubgroup"] = k
        items.append({"layer": "Option_A::INT_PLANT_shrubgroup", "kind": "SVG_CIRCLE", "c": c, "r": d / 2.0,
                      "closed": True, "name": u"ROSEMARY GROUP",
                      "meta": {"source": "svg", "svg_group": svg_key(u["groups"][-1]) if u["groups"] else "plan_rosemary",
                               "kind": "shrub_group", "species": "rosemary", "diameter_m": "%.1f" % d,
                               "label": u"ROSEMARY GROUP", "id": u"SVG-SHRUB-%d" % k},
                      "bid": u"A-svg-INT_PLANT_shrubgroup-%d" % k})
    if not shrubs:
        notes.append(u"WARNING SVG: no rosemary symbols found: INT_PLANT_shrubgroup not baked")
    if small:
        notes.append(u"SVG: %d rings under %.0f m2 (slivers) not baked" % (small, SVG_MIN_M2))
    if dup[0]:
        notes.append(u"SVG: %d shapes drawn twice on the same spot baked once" % dup[0])

    # ---- svg_reference (S5): trees are measured, never baked ----
    zl = {}                                                  # kind -> [(bbox, ring, is_hole)] (m), for the zone shares
    for it in items:
        if it["kind"] == "SVG":
            zl.setdefault(it["meta"]["kind"], []).append((g_bbox(it["P"]), it["P"], it["meta"].get("hole") == "1"))
    gpcs, _ = plan.under("green_corridor_open_ground_within_25_m_of_the_water")
    for pc in gpcs:
        for P, depth in svg_holes([r for r in svg_rings_m(pc, M, shift) if r[0]], pc["evenodd"]):
            if abs(g_area(P)) >= SVG_MIN_M2:
                zl.setdefault("green25_svg", []).append((g_bbox(P), P, bool(depth % 2)))
    order = ("water_design", "wetland", "plaza", "walk", "bike_lane", "park_path", "heritage_setting", "green25_svg")

    def zone_of(p):
        for zk in order:
            hit = [h for bb, P, h in zl.get(zk, ()) if bb[0] <= p[0] <= bb[2] and bb[1] <= p[1] <= bb[3] and
                   g_pip(p[0], p[1], P)]
            if hit and not any(hit):
                return zk
            if hit and any(hit) and sum(1 for h in hit if not h) > sum(1 for h in hit if h):
                return zk
        return "none"
    trees = [u for u in sym_all if u["href"].startswith("sym_") and u["href"] != "sym_rosemary"]
    per = {}
    allp = []
    for u in trees:
        sp = u["href"][4:]
        c = svg_pt(M, u["c"])
        d = (u["w"] + u["h"]) / 2.0 * m_per_u
        z = zone_of(c)
        e = per.setdefault(sp, {"pts": [], "d": [], "zones": {}})
        e["pts"].append(c)
        e["d"].append(d)
        e["zones"][z] = e["zones"].get(z, 0) + 1
        allp.append(c)
    nn_all = g_nn(allp)
    sp_out = {}
    for sp in sorted(per):
        e = per[sp]
        nn_s = g_nn(e["pts"]) if len(e["pts"]) > 1 else []
        sp_out[sp] = {"count": len(e["pts"]),
                      "crown_d_m": {"median": g_pct(e["d"], 0.5), "p10": g_pct(e["d"], 0.1), "p90": g_pct(e["d"], 0.9),
                                    "min": round(min(e["d"]), 2), "max": round(max(e["d"]), 2)},
                      "spacing_same_species_m": {"p10": g_pct(nn_s, 0.1), "p50": g_pct(nn_s, 0.5)},
                      "zones": dict(sorted(e["zones"].items()))}
    zt = {}
    for sp in per:
        for z, n in per[sp]["zones"].items():
            zt[z] = zt.get(z, 0) + n
    reed_c, reed_d = [], []
    for pc in reeds:
        for cl, P in svg_rings_m(pc, M, clip=False):
            bb = g_bbox(P)
            reed_c.append(((bb[0] + bb[2]) / 2.0, (bb[1] + bb[3]) / 2.0))
            reed_d.append(max(bb[2] - bb[0], bb[3] - bb[1]))
            break
    wet_m2 = sum(abs(g_area(P)) * (-1 if h else 1) for bb, P, h in zl.get("wetland", ()))
    reeds_in = sum(1 for p in reed_c if zone_of(p) in ("water_design", "wetland"))
    reeds_wet = sum(1 for p in reed_c if zone_of(p) == "wetland")
    route_m = sum(g_len(it["P"]) for it in items if it["meta"].get("kind") == "route")
    bridge_m = sum(g_len(it["P"]) for it in items if it["meta"].get("kind") == "footbridge")
    pal = {}
    for lk in ("walk", "bike", "green", "plaza", "water", "wet", "green25", "her", "old", "kizil", "route",
               "t_plane", "t_ash", "t_willow", "t_olive", "t_pine", "t_tam", "c_her", "c_wat", "c_gar", "c_sq",
               "c_cul", "c_play", "c_rt", "c_des"):
        cs = [p for p in plan.pieces if any(g == "legend_" + lk or svg_key(g) == "legend_" + lk for g in p["groups"])
              and p["fill"] not in ("#1e1e1e", "#ffffff")]
        if cs:
            pal[lk] = [{"fill": p["fill"], "stroke": p["stroke"], "stroke_w_m": round(p["sw"] * m_per_u, 3) if p["stroke"]
                        else None, "dash": p["dash"] or None} for p in cs]
    ref = {"trees": {"count": len(trees), "species": sp_out, "zones": dict(sorted(zt.items())),
                     "spacing_any_species_m": {"p10": g_pct(nn_all, 0.1), "p50": g_pct(nn_all, 0.5), "p90": g_pct(nn_all, 0.9)},
                     "zone_order": list(order) + ["none"],
                     "note": "measured from the SVG; MasterPlan regenerates the trees by its rules (S5), none is baked"},
           "shrub_groups": {"rosemary": {"count": len(shrubs), "diameter_m": {
               "median": g_pct([(u["w"] + u["h"]) / 2.0 * m_per_u for u in shrubs], 0.5),
               "min": round(min([(u["w"] + u["h"]) / 2.0 * m_per_u for u in shrubs]), 2) if shrubs else None,
               "max": round(max([(u["w"] + u["h"]) / 2.0 * m_per_u for u in shrubs]), 2) if shrubs else None}}},
           "reeds": {"count": len(reed_c), "in_wetland": reeds_wet, "in_design_water": reeds_in - reeds_wet, "tuft_d_m": {"p10": g_pct(reed_d, 0.1), "median": g_pct(reed_d, 0.5),
                     "p90": g_pct(reed_d, 0.9)}, "nn_m_p50": g_pct(g_nn(reed_c, 10.0), 0.5),
                     "per_ha_of_wetland": round(reeds_wet / (wet_m2 / 10000.0), 1) if wet_m2 else None,
                     "fills": list(SVG_REED_FILLS)},
           "route": {"line_m": round(route_m, 1), "footbridge_m": round(bridge_m, 1), "arrows": len(arrows),
                     "arrow_len_m_median": g_pct([a[4] for a in arrows], 0.5),
                     "arrow_spacing_m_p50": g_pct(g_nn([(a[0], a[1]) for a in arrows]), 0.5)},
           "green25_svg": {"rings": len(zl.get("green25_svg", ())), "area_m2": round(sum(abs(g_area(P)) * (-1 if h else 1) for bb, P, h in zl.get("green25_svg", ())), 1),
                           "note": "not baked (S2): MasterPlan recomputes it as 25 m from INT_WATER_design"},
           "palette_legend": pal}
    return items, ref
# ================================================================ SVG READER (stdlib only) END


# ---------------------------------------------------------------- v12: the SVG in Rhino
def svg_site(doc, log):
    """site_alan's corners (survey m): the largest closed polyline on layer site_alan, else SITE_COPY"""
    best = None
    for lay in doc.Layers:
        if lay.IsDeleted or lay.Name != "site_alan":
            continue
        for o in doc.Objects.FindByLayer(lay) or []:
            g = o.Geometry
            if not isinstance(g, rg.Curve) or not g.IsClosed:
                continue
            res = g.TryGetPolyline()
            pl = res[1] if isinstance(res, tuple) and res[0] else None
            if pl is None or pl.Count < 4:
                continue
            P = [(p.X, p.Y) for p in pl]
            if P[0] == P[-1]:
                P = P[:-1]
            a = abs(g_area(P))
            if best is None or a > best[0]:
                best = (a, P)
    if best:
        return best[1]
    log.append(u"WARNING SVG placing: no closed site_alan outline in this file; the built-in copy (Bergama_Altlik.3dm, "
               u"25 Oct) was used")
    return list(SITE_COPY)


def svg_study_areas(doc):
    """{study-area name as the base writes it (aras_alan, begum_alan[0], ...): ring} from the open file's study-area
    curves; begum_alan's two pieces are numbered as STUDY_BBOX has them"""
    out = {}
    for nm, boxes in STUDY_BBOX.items():
        rings = []
        for lay in doc.Layers:
            if lay.IsDeleted or lay.Name != nm:
                continue
            for o in doc.Objects.FindByLayer(lay) or []:
                g = o.Geometry
                if not isinstance(g, rg.Curve) or not g.IsClosed:
                    continue
                res = g.TryGetPolyline()
                pl = res[1] if isinstance(res, tuple) and res[0] else None
                if pl is None:
                    try:
                        ts = g.DivideByCount(200, True)
                        pl = [g.PointAt(t) for t in ts] if ts else None
                    except Exception:
                        pl = None
                if pl:
                    rings.append([(p.X, p.Y) for p in pl])
        for R in rings:
            bb = g_bbox(R)
            k = min(range(len(boxes)), key=lambda i: sum(abs(bb[j] - boxes[i][j]) for j in range(4)))
            out[nm if len(boxes) == 1 else u"%s[%d]" % (nm, k)] = R
    return out


def svg_read(doc, log):
    """v12: Aras's masterplan SVG read now -> (items to bake, True) or ([], False) when it is missing or unreadable
    (WARNING lines, never stops). Writes svg_reference.json."""
    p = os.path.join(BERGAMA_ROOT, "Data", "assets", SVG_FILE)
    if not os.path.isfile(p):
        log.append(u"WARNING SVG: %s not found: only the built-in base was baked (objects baked from an earlier SVG "
                   u"are left as they are). Copy masterlastversion.svg from the run kit's Data/assets folder there." % p)
        return [], False
    t0 = time.time()
    try:
        plan = SvgPlan(p, svg_want)
        notes = []
        if not plan.frame_ids:
            raise ValueError("no clip rectangle (the plan frame) in the SVG, so it cannot be placed on site_alan")
        fr, shift = svg_frame_of(plan, notes)
        site = svg_site(doc, log)
        M, s = svg_world_matrix(site, fr, notes)
        items, ref = svg_zone_items(plan, M, s, shift, notes)
    except Exception as ex_:
        log.append(u"WARNING SVG: %s could not be read (%s: %s): only the built-in base was baked; objects baked from "
                   u"an earlier SVG are left as they are" % (SVG_FILE, type(ex_).__name__, ex_))
        return [], False
    st = os.stat(p)
    log.append(u"SVG: %s (%s, %.1f MB) read in %.1f s: %d pieces of the wanted groups, %d symbols" % (
        p, time.strftime("%d %b %Y %H:%M", time.localtime(st.st_mtime)), st.st_size / 1048576.0, time.time() - t0,
        len(plan.pieces), len(plan.uses)))
    log.extend(n if n.startswith("WARNING") else u"  " + n for n in notes)
    sa = svg_study_areas(doc)
    for it in items:
        q = it["c"] if it["kind"] == "SVG_CIRCLE" else (g_inner_pt(it["P"]) if it["closed"] else it["P"][len(it["P"]) // 2])
        own = next((k for k, R in sa.items() if g_pip(q[0], q[1], R)), None)
        if own:
            it["meta"]["study_area"] = own
        it["meta"]["svg_file"] = SVG_FILE
    # what the SVG gives, per layer (the contract MasterPlan reads)
    per = {}
    for it in items:
        lay = it["layer"].split("::")[-1]
        e = per.setdefault(lay, {"pieces": 0, "holes": 0, "area_m2": 0.0, "length_m": 0.0, "parts": {}})
        e["pieces"] += 1
        if it["kind"] == "SVG":
            a = abs(g_area(it["P"]))
            if it["meta"].get("hole") == "1":
                e["holes"] += 1
                e["area_m2"] -= a
            else:
                e["area_m2"] += a
        elif it["kind"] == "SVG_LINE":
            e["length_m"] += g_len(it["P"])
        pt = it["meta"].get("part")
        if pt:
            e["parts"][pt] = e["parts"].get(pt, 0) + 1
    for lay in sorted(per):
        e = per[lay]
        log.append(u"  SVG -> Option_A::%s: %d piece(s)%s%s%s%s" % (
            lay, e["pieces"], u" (%d holes)" % e["holes"] if e["holes"] else u"",
            u", %.2f ha" % (e["area_m2"] / 10000.0) if e["area_m2"] else u"",
            u", %.0f m" % e["length_m"] if e["length_m"] else u"",
            u"; " + u", ".join(u"%s %d" % kv for kv in sorted(e["parts"].items())) if e["parts"] else u""))
    tr = ref["trees"]
    log.append(u"  SVG trees (S5, measured, not baked): %d; %s; spacing to the nearest tree p10 %s m, p50 %s m" % (
        tr["count"], u", ".join(u"%s %d (crown d median %s m, p10 %s, p90 %s)" % (
            sp, v["count"], v["crown_d_m"]["median"], v["crown_d_m"]["p10"], v["crown_d_m"]["p90"])
            for sp, v in sorted(tr["species"].items())), tr["spacing_any_species_m"]["p10"], tr["spacing_any_species_m"]["p50"]))
    log.append(u"  SVG trees per zone: " + u", ".join(u"%s %d" % kv for kv in sorted(tr["zones"].items())))
    rd, ro = ref["reeds"], ref["route"]
    log.append(u"  SVG reeds (a look, not baked): %d tufts, %s in the wetland (%s per ha), tuft %s m; route %.0f m + "
               u"footbridges %.0f m, %d arrows about %s m apart" % (rd["count"], rd["in_wetland"], rd["per_ha_of_wetland"],
                                                                   rd["tuft_d_m"]["median"], ro["line_m"], ro["footbridge_m"],
                                                                   ro["arrows"], ro["arrow_spacing_m_p50"]))
    # S4 / S2 / S7: what is left out
    trail = sum(g_len(P) for pc in plan.under("heritage_trail*")[0] for cl, P in svg_rings_m(pc, M))
    log.append(u"  SVG heritage trail (S4): only %.0f m drawn: not baked; draw the whole line in the SVG to have it" % trail)
    log.append(u"  SVG not baked: green corridor 25 m (%d rings, %.2f ha in the SVG; S2: MasterPlan recomputes it from "
               u"INT_WATER_design), trees, reed tufts, AI render, topography rasters, wall picture, asset drawings, labels, "
               u"legend (S5, S7), survey context (roads, buildings, heritage blocks, Kızıl Avlu outline, contours); "
               u"open_meadow is the whole site rectangle, not a zone" % (
                   ref["green25_svg"]["rings"], ref["green25_svg"]["area_m2"] / 10000.0))
    ref.update({"made_by": VERSION, "made_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "svg": {"file": SVG_FILE, "path": p, "modified": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime)),
                        "bytes": st.st_size},
                "placing": {"units_per_m": round(s, 6), "frame_units": [round(x, 3) for x in fr],
                            "ground_topt_shift_units": [round(shift[0], 3), round(shift[1], 3)], "site_alan": [list(q) for q in site]},
                "baked": dict((k, {"pieces": v["pieces"], "holes": v["holes"], "area_m2": round(v["area_m2"], 1),
                                   "length_m": round(v["length_m"], 1), "parts": v["parts"]}) for k, v in per.items())})
    try:
        d = bg_cache("bergama_zone_base")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, SVG_REF_JSON), "w", encoding="utf-8") as f:
            json.dump(ref, f, indent=1, ensure_ascii=False, sort_keys=True)
        log.append(u"  SVG reference written: " + os.path.join(d, SVG_REF_JSON))
    except Exception as ex_:
        log.append(u"WARNING SVG: %s not written (%s)" % (SVG_REF_JSON, ex_))
    return items, True


def zb_bake(doc, which, log, svg_items=(), svg_ok=False):   # v11.2 (CHK-12): was bake(), a Button word; v12: + the SVG
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
            if not svg_ok and o.Attributes.GetUserString("source") == "svg":
                continue                                 # v12: no SVG this press: its last bake stays as it is
            if o.Attributes.GetUserString("base_hash") == shape_hash(o.Geometry):
                doc.Objects.Delete(o, True)
                gone += 1
            else:
                kept_ids.add(o.Attributes.GetUserString("base_id"))
        groups, dropped = {}, []
        mine = [i for i in items if i["layer"].startswith(parent + "::")]
        n_base = len(mine)
        mine += [i for i in svg_items if i["layer"].startswith(parent + "::")]       # v12: after the base (ids unchanged)
        for k_, it in enumerate(mine):
            bid = it.get("bid") or "{}-{}".format(o_, k_)
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
            elif it["kind"] in ("SVG", "SVG_LINE", "SVG_CIRCLE"):        # v12: from the SVG, never cut or left out
                if it["kind"] == "SVG_CIRCLE":
                    g = rg.ArcCurve(rg.Circle(rg.Point3d(it["c"][0], it["c"][1], 0.0), max(it["r"], 0.05)))
                else:
                    P = [rg.Point3d(p[0], p[1], 0.0) for p in it["P"]]
                    if it["closed"] and P[0].DistanceTo(P[-1]) > tol:
                        P.append(P[0])
                    g = rg.PolylineCurve(P)
                if g.IsValid:
                    att.SetUserString("base_hash", shape_hash(g))
                    gids.append(doc.Objects.AddCurve(g, att))
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
            who = "calisma_alan" if k_ < n_base else "svg " + SVG_FILE   # v6: one shared working area; v12: + the SVG
            grp = groups.setdefault(who, {})
            nm = {"ZONE": "zones", "WATER": "strip pieces", "SURFACE": "wetland edges", "REMOVE": "cleared buildings",
                  "ROAD": "paths", "LINK": "arrows", "LABEL": "labels"}.get(it["kind"]) or lay.split("::")[-1]
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
        try:
            svg_items, svg_ok = svg_read(doc, log)                  # v12: Aras's masterplan SVG, read now
        except Exception as ex_:
            svg_items, svg_ok = [], False
            log.append(u"WARNING SVG: %s: %s: only the built-in base was baked" % (type(ex_).__name__, ex_))
        n = zb_bake(doc, which, log, svg_items, svg_ok)
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
    tail = ["", "Every size of the built-in base is a placeholder (user text 'basis' on each zone); the SVG layers "
                "(user text source=svg) are as Aras drew them. Edit freely, then press Build on the masterplan component. "
                "Pressing here again keeps every object you changed."]
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
    elif any(ln.startswith("WARNING") for ln in log):     # v12: SVG checks warn, never stop
        gh_message("warning", " | ".join(ln for ln in log if ln.startswith("WARNING")))
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
