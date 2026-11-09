# CURRENT VERSION: bergama_water_balance_v11.py = v11 (4 Nov 2026; what changed: the NEW IN / VERSION notes below)
# bergama_water_balance_v8.py (v8, 31 Oct: round 3, p10 charts fill the page, sentence-case title; v7, 30 Oct: revision T5, p10 answer box, carries and cost cut-off as small diagrams; v6, 29 Oct: revision T3b, the year as one G7 chart, the zones for p.12; v5, 28 Oct: MIRAQUA revision, the sheet in reading order; v4.1, 27 Oct: m² / m³ / hm³ drawn as raised digits; v4: the design store's normal and dry year in the results; v3 sheet kept) · Thread 2 of the 22 Oct batch: water balance (demand, collection, storage, cost cut-off)
# Runs as delivered in: Grasshopper Python 3 component (press a Button wired to any input), Rhino 8 ScriptEditor
# (Python 3), or plain Python 3. Every press RECOMPUTES the balance from the current lands (Aras 24 Oct 08:13):
#   1. lands: optional GH inputs > objects in the open Rhino file > built-in defaults (see LANDS below);
#   2. 34 water years 1991-2025, daily: FAO-56 soil water balance on the farms, river + site catch into storage,
#      strip first, nothing stored over 365 days, cost ladder; the cost cut-off sets the size and the % covered;
#   3. writes Downloads/Bergama/cached/Bergama_water_balance_analysis/water_balance_results.json, which other scripts
#      read instead of fixed numbers (read_results() below), and v10: cached/booklet/Bergama_water_balance_analysis/
#      items.json, the p10 drawings and texts the booklet composes (no sheet PDF any more; v11: page id p10).
# Built-in inputs (weather, river, Kc) come from research/water_balance/scripts/water_balance_v2.py, 24 Oct 2026;
# sources and methods: research/water_balance/NOTES.md.
#
# Lands read from the open Rhino file (zone base layers, option A only since v2.3):
#   Option_A::INT_ZONE_WS  -> terrace_m2 (retention terraces)     Option_A::INT_ZONE_GR -> walk_m2 (walk tops)
#   Option_A::INT_WATER_strip -> strip_m2 (the low-flow strip)
# Any closed curve with the user text  water_balance = <key>  adds its area to that key instead (keys: roof, walk,
# riverside_walk, terrace, strip, pond_land, cropland, orchard). So a new storage plot or roof only needs a closed
# curve with that user text. GH inputs with these names override both: cropland_ha, orchard_ha, pond_land_ha,
# roof_m2, walk_m2, riverside_walk_m2, terrace_m2, strip_m2, cropland_crops (text "cotton,tomato"), option.
import os, time, json, zlib, base64, math, datetime as dt
from collections import deque, defaultdict

VERSION = "v12"  # v12 (L6 layout plan, 4 Nov): producer keeps only data warnings (the "wrap" / "widow" layout warnings gone; every text was already an anchored label, nothing left out; one box per drawing: number badge, heading and subtitle caption carry drawing=D) (NEW IN v12); v11 (round 6 S7, 4 Nov): page id p10, run stamp dropped, hue table, G6-9 groups (NEW IN v11); v10 (round 5 S5, 2 Nov): items for the booklet, no sheet PDF, warnings never stop (NEW IN v10); v9 (round 4 S7, PALL.2 p11): one text placer (a collision RAISES), real Arial widths, one trigger file; v8.3 fix 1 Nov 08:30: only the component's own inputs can start it (a True setting inside the script no longer does); v8.2 fix 1 Nov 08:20: chain trigger keyed to each solve (Rhino keeps globals), so the chain continues after ZoneBase; v8.1 fix 1 Nov: a pasted or rewired component no longer runs by itself (chain trigger notes the wire on its first solve)
# NEW IN v11 (round 6 S7, 4 Nov 2026; BRIEF §6 row 10, G6-1, G6-6, G6-9):
#   * page id p10 (round 6 22-page numbering; was p11): WB_PAGE and the log; the water board's page is now p11 (the
#     "zones for p11" log line).
#   * the run stamp (text item wb_run, "lands option A · run <time>") is gone from the page (Aras: debug text on the page).
#   * G6-6 hues: every colour of the drawings from the shared hue table (common/hues.py, hue(code, rank)): the store
#     tones WW r4/r3/r1, the site catch and the cheaper costs WW r2, the cut-off and its words WW r1, the farm need and
#     both curves AGR r2 (mean / median year) and AGR r1 (1 in 5 dry), the Jun-Sep band AGR r4 with its words AGR r1,
#     recycled water / dearer CTX r2; the stream and strip keep the water tones (= WAT r2-r4). No 8B2D2D / 8B3A3F /
#     633131 is left on the page's drawings. Log: "legend p10 hues=table".
#   * G6-9 groups: every element of a block is its own group inside its kind (water, fields, annotations, labels,
#     legend, other): WbRec.tag(kind, eid) before each element; wb_items() writes each run of one tag as its own layer
#     "<kind>/<eid>" inside the shared module's ix_group (a no-op before it exists). Log: "groups p10 kinds=.. elements=..
#     untagged=..". Figures, the results JSON and every computation unchanged.
# NEW IN v10 (round 5, S5, 2 Nov 2026; G-R5-12, G-R5-1, C1, C10, CHK-12; a feature change, so the next whole number):
#   * CHANGE OF APPROACH for p11's text collisions (round 4 failed on them more than once): this script lays out no page
#     and writes no sheet PDF (addendum 1 Nov 22:37 point 2). Each of the four blocks is drawn as before into a
#     recorder (WbRec, same calls as the old Page) and exported as one chart drawing (mm, y up) through common/
#     item_export.py into cached/booklet/Bergama_water_balance_analysis/items.json: wb_year, wb_curve, wb_store,
#     wb_answer. Every word is a text item: the page title, the question (intro), each block's number + title
#     (heading) and keyword line (note), the run line (note), and every word inside a chart as a label anchored where
#     v9 set it (the booklet places, sizes and checks them: G-R5-12). Source marks are {src:key} (ix.source rows);
#     the invisible source key and booklet/blocks.json are gone. Figures and the results JSON are unchanged.
#   * warnings, never stops (C1): common/warn.py is included before text_place.py; the log head is "<n> warnings"
#     followed by every WARNING line (wn_compose); nothing raises on a text hit (a widow is set one word short).
#   * CHK-12: build() (a Button word: a Button input named "build" read the function) is now wb_items().
#   * C10: the riverside walks area from the masterplan's results is read with bg_result and dated with bg_this_run:
#     the log names the masterplan run it comes from; a value from an EARLIER chain run (or the built-in placeholder)
#     is a WARNING. One press gives one answer only when this component is wired AFTER the masterplan (RUN_GUIDE).
#   * C2: no output/ folder is made (nothing is written there any more).
# NEW IN v9 (round 4, S7, 1 Nov 2026, PALL.2 on booklet p11, G-R4-1 / G-R4-10; a feature change): every visible text
#   of the sheet is registered in ONE TextPage ("p11", common/text_place.py) with its real Arial box (font_metrics.py)
#   before it is drawn; the labels that look for a free place ask it; its check RAISES on any collision, so no sheet
#   with text on text is written (the log says "overlap p11 checked n, collisions 0"; the old "FLAG overlap p10" line
#   and the estimated Helvetica widths are gone). No footer or rule is drawn on the sheet (the booklet sets the page
#   number). Start-up: common/trigger.py (only a Button press or a new done text starts it; "trigger: <why>" in the
#   log). Computation, results JSON and the sheet's layout unchanged. Closing (same v9): Page.para and rich_para wrap
#   with the shared tp_wrap (no one-word last line, G-R4-2).
# NEW IN v8 (round 3, 31 Oct 2026, P10.1 + G2/G3; a feature change, so the next whole number): the white space goes
#   to the charts: block 1 grows 92 -> 100 mm and its rows follow the block (YEAR_RH from the height, 13.5 -> 15.4 mm); blocks 2-3 move down 8 mm;
#   block 3's rows follow its height; block 4 is a tighter band (36 -> 32 mm, no empty field under its line); the
#   title in sentence case like every booklet page ("The water balance"); the log prints "FLAG overlap p10 n".
# NEW IN v6 (revision 29 Oct 2026, T3b WO-T3b-2, package C items 1-4 and G7; a feature change, so the next whole
#   number). Pages 11-12 are one story: p.12 (water board) is now one diagrammatic water map, so the analysis it shows
#   left this sheet, and what stays is drawn per G7 (R31: every user its own row, one common time axis, bars):
#   * block 1 "One year of water": the stream, the site catch, the store, the summer strip and the farms as five rows of
#     icons.py pictograms and bars on ONE month axis (replaces the question, the farm tiles, the monthly chart with its
#     number rows, and the stream's monthly flow). The store's monthly level is new: results key
#     design.store_month_m3 (run_storage now records the level, `lev`; store_months()).
#   * gone from the sheet: the site-catch bars (block 4; its figures are on the p.12 map, results keys unchanged), the
#     1:500 flood cut (the flood levels belong to the sections, p.13), the open-pond curves, the claims column.
#   * blocks 2 storage curve, 3 cost, 4 the answer with ONE short conclusion paragraph; icons from common/icons.py
#     (the sheet's own icon() and tile() are gone); crops wb_year, wb_curve, wb_store, wb_answer (wb_tiles,
#     wb_timing, wb_catch, wb_stream removed).
#   * results key "zones" (new): the Option A zones and water links in survey m (zone base layers of the open Rhino file,
#     else the built-in copy data/ZONE_COPY.py), read by the water board's p.12 map. Every other key unchanged.
# NEW IN v5 (MIRAQUA 28 Oct, booklet revision v4: P11.1, P11.2, G3/G5/G11/G13; bank depth research 28 Oct §4.3; a
#   feature change, so the next whole number):
#   * The sheet re-laid in reading order: 1 the question, 2 how the stream behaves, 3 what the farms need, 4 what the
#     site can catch, 5 storage size, 6 cost, 7 the answer (a light water-tint band, not the dark block).
#   * Bold keywords in every block line; DSİ with its İ; corn (not maize); heights with 2 decimals; the 1:500 cut's
#     scale bar in cm; land areas in ha on the whole sheet (Aras 28 Oct 13:21), the cistern's land per m³ in m².
#   * "K4: right bank floods from Q100" left out (the survey shows K4 before the DSİ walls); no internal file name in
#     the sources. Every number is computed as before.
# NEW IN v4.1 (bugfix, Aras 27 Oct, Prompt 8 final check): ² and ³ on the sheet are drawn as a raised small 2 or 3
#   (0.6 x the size, as the water board v3.1 and agriculture v3 do; see SUP): the unembedded Helvetica's ²/³ glyph was
#   missing in some viewers ("hm" for "hm³"). The invisible source key names only public sources (no internal research
#   file names: "Calculations: research/water_balance/NOTES.md", "rain_river_levels README / table A2 / A3s" gone).
#   Layout, figures and the results JSON unchanged.
# v4 (Aras 27 Oct 17:35, booklet Prompt 6 "water, part 3", p24: "show the defence ON the board ... normal year vs dry
#   year as two stacked bars"): the results JSON gains design.year_split, the design store through two real water years
#   of the same daily run: "normal" = the year whose farm need is nearest the median, "dry5" = the 1-in-5 dry year
#   (farm_demand_m3 dry5_year). Each: carried in (Oct 1), filled that year (stream + site catch), the strip's draw and
#   need, the farms' draw and need, released after 365 days, carried out (Sep 30), and the stream's winter water that
#   year as % of a median year. run_storage also counts per water year what it lets go after 365 days and the store
#   at the year's end (the store is closed, no evaporation: carried in + filled = strip + farms + released + carried
#   out). The agriculture sheet draws it. The sheet and every other key are unchanged.
# v3 (Aras 27 Oct 17:34, booklet Prompt 4 "water, part 1"; v2.7's layout kept, nothing moved):
#   * panel 2 "What the site can catch" adds what the STREAM gives, same units and bars: the Selinos winter flow the
#     store takes (Nov-Apr, the worst-case gauge series the storage already runs on, at the design store) and the share
#     of that winter flow left in the stream (mean year and the driest year). Computed live: run_storage now also counts
#     the stream's part of what enters the store (site catch first, the stream tops up: the stream's part is the low
#     side); results JSON gains design.river_take_m3_per_year, river_take_share_pct, river_left_pct, river_avail_m3_per_year.
#   * "How the stream behaves" (was the booklet page before this one, the water board's wb_water) leads the sheet as a
#     band beside the title: the natural flow past the site by month (Jul-Sep marked dry), and how high the stream rises
#     on the surveyed upstream-entry cut at 1:500 (Jan-Feb, max 2017, Q100, Q500), its scale bar under the label column.
#     Only what carries the argument; its figures from rain_river_levels A2 / A3s (constants below, sourced).
#   * the text under the component shows a newly pasted version at once, idle (Aras 27 Oct 15:35).
# v2.7 (Aras 27 Oct 11:07, booklet p10; PHASE2_SPEC §6 "p9-10"): white sheet; no source footer (the numbered key is now an
#   invisible text layer the booklet's sources page still reads; [n] marks stay); NEW LAYOUT read top-left -> bottom-right:
#   THE ANSWER (focal: store m³ -> % of the farms carried -> cost cut-off, our claims under it), farm tiles, then
#   1 timing | 2 site catch, 3 storage curve | 4 cost per m³; sentences -> keywords; labels placed with measured boxes
#   (text_w) and an overlap check (the log names any overlap). Computation and results JSON unchanged (script name only).
# v2.6 (Aras 25 Oct 21:47-21:51, booklet/CROP_SPEC.md): the booklet shows this sheet's own drawings: booklet/blocks.json
#   lists one crop per panel (1-5 and the header tiles; rects from PANELS / TILES below); the separate booklet redraws
#   (bk_timing, bk_catch, bk_curve, bk_store and their PDFs) are gone. Sheet words: the Selinos is a stream ("Stream"
#   row, "Streamside walks"), no "(FLAG)" caveat. Layout, look and the results JSON keys unchanged.
# v2.5 (25 Oct, booklet stage 2, SCRIPT_STANDARD §8): also writes output/Bergama_water_balance_analysis/booklet/ (4 text-free
#   drawing PDFs at their booklet frame size + blocks.json with every word as a label); results JSON gains
#   jun_sep_share_of_need_pct and site_catch_share_of_need_pct. The A3 sheet is unchanged.
# v2.3 (Aras 25 Oct 16:43: "the selection of A should be remember in the whole project so all scripts should drop B alternatives"): option A only; the option input is ignored.
# v2.2 (Aras 25 Oct 09:34-09:35): the same names in every script: the Button goes into an input named run, the log comes out of an output named log, and the log file is Downloads/Bergama/logs/bergama_water_balance_log.txt (next to cached/ and output/), overwritten by each press.
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
# ---- warn.py (round 5, S1, 1 Nov 2026; G-R5-1, C11; PLAN §3 "Warnings"): ONE warning sink for every script -----------
# Aras 1 Nov 17:11 / 18:51: a check hit never stops the run; it is an orange Grasshopper warning plus one
# "WARNING <page> <kind> ..." log line, so one run collects every hit. Hard stops only for missing data, fonts or
# levels (raise those as before). C11 (round 4: "0 warnings" printed with a hit in the log): the count at the log's
# head is COUNTED from the finished log's WARNING lines (wn_compose), never kept as a separate number.
# Needs nothing. Include it BEFORE text_place.py: text_place then uses WN_LOG as its TP_LOG (one list, so a script that
# prints tp_log_lines() prints every warning) and routes tp_warn here.
#
#   wn_warn(page, kind, msg, log=None) -> line   one hit: "WARNING <page> <kind>: <msg>" (page / kind may be None) into
#                                                 log (default WN_LOG) + one orange message; returns the line
#   wn_orange(msg)                                the orange Grasshopper message only (no log line); capped at
#                                                 WN_ORANGE_MAX per solve, the rest summed in one message by wn_compose
#   wn_is(line) -> bool                           a WARNING line (its text, leading blanks ignored, starts "WARNING")
#   wn_compose(lines, head=()) -> [str]           the finished log: head lines, then "<n> warnings" with n = the number
#                                                 of WARNING lines found, then every WARNING line (moved, in order, so
#                                                 each is in the log ONCE), then the other lines in their order
#   wn_count(lines) -> n                          WARNING lines in lines
#   wn_reset()                                    empties WN_LOG and the orange counter (call at the start of a run)
WN_LOG = []
WN_ORANGE_MAX = 60
_WN_N = [0, 0]           # [orange messages shown this run, orange messages held back]


def _wn_gh(msg):
    try:
        ghenv.Component.AddRuntimeMessage(__import__("Grasshopper").Kernel.GH_RuntimeMessageLevel.Warning,  # noqa: F821
                                          u"%s" % msg)
    except Exception:
        pass


def wn_orange(msg):
    """one orange (Warning level) runtime message on this component; outside Grasshopper nothing"""
    if _WN_N[0] >= WN_ORANGE_MAX:
        _WN_N[1] += 1
        return
    _WN_N[0] += 1
    _wn_gh(msg)


def wn_warn(page, kind, msg, log=None):
    """one hit as a WARNING line + an orange message; the run goes on"""
    head = u" ".join(u"%s" % p for p in (page, kind) if p not in (None, u"", ""))
    line = u"WARNING " + (head + u": " if head else u"") + u"%s" % msg
    (WN_LOG if log is None else log).append(line)
    wn_orange(line[8:])
    return line


def wn_is(line):
    return (u"%s" % line).lstrip().startswith(u"WARNING")


def wn_count(lines):
    return sum(1 for ln in lines if wn_is(ln))


def wn_compose(lines, head=()):
    """the log with its warning head (see the module notes); the count equals the WARNING lines by construction"""
    flat = []
    for ln in lines:                                   # a list item may hold several lines
        flat.extend((u"%s" % ln).split(u"\n"))
    warn = [ln.strip() for ln in flat if wn_is(ln)]
    rest = [ln for ln in flat if not wn_is(ln)]
    out = list(head) + [u"%d warnings" % len(warn)] + warn
    if _WN_N[1]:
        out.append(u"(orange messages: the first %d shown on the component, %d more only here)" % (_WN_N[0], _WN_N[1]))
        _wn_gh(u"%d more warnings: see the log's head" % _WN_N[1])
    return out + [u""] + rest


def wn_reset():
    del WN_LOG[:]
    _WN_N[0] = _WN_N[1] = 0
LOG_DIR = bg_logs()                        # Aras 25 Oct 09:34-09:35: every script's log here


def write_log(text):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, "bergama_water_balance_log.txt"), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    return text

# v2 24 Oct: all files under Downloads/Bergama/ (Aras rule). v2.1 (Thread 5): riverside_walk_m2 read live from the
# masterplan (v11) results when no GH input or Rhino curve gives it
OUT_DIR = bg_output("Bergama_water_balance_analysis")        # v10: read fallback only (v9 and older wrote here)
RES_DIR = bg_cache("Bergama_water_balance_analysis")         # 27 Oct: the results JSON other scripts read
OLD_OUT_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama_water_balance_analysis")   # read fallback only
WB_FOLDER = "Bergama_water_balance_analysis"                  # v10: cached/booklet/<this>/items.json (the booklet reads it)
WB_PAGE = "p10"                                               # v11: the booklet page id (round 6 22-page numbering: p10; was p11)
OUT_JSON = "water_balance_results.json"
MP_FILE = bg_result("bergama_masterplan", "masterplan_results.json")   # v10 (C10): cached/, from_output/, output/

# ------------------------------------------------------------------ lands: defaults (used when nothing else is given)
LANDS = dict(
    cropland_ha=34.9,          # around2.pdf farm extent, ESA WorldCover 2021 cropland (satellite)
    orchard_ha=1.34,           # same, orchards inferred within 35 m of survey olive/fruit symbols; grown as olive
    pond_land_ha=2.81,         # vacant flat land in the around2.pdf land-use table, for open ponds
    roof_m2=20110.0,           # survey roofs in the four study areas (rain_river s.2, lower bound)
    walk_m2=2682.0,            # zone base v5 GR 1-3 walk tops, grated paving
    riverside_walk_m2=17694.0, # DESIGN placeholder: 2 x 2,949 m x 3 m; v2.1 reads the masterplan's walks instead (MP_FILE)
    terrace_m2=3490.0,         # zone base v5 WS 1 retention terraces (overflow only)
    strip_m2=4.0 * 2949.0,     # rain_river s.4 reference strip 4 m x 2,949 m (DESIGN)
    cropland_crops="cotton,maize,tomato",  # run as each; design = larger size. Bergama's main irrigated crops, TÜİK 2025
                                           # (library/research/crops_2026-10-24 §1.25); fields' own crops not mapped
)
ZONE_LAYERS = {"INT_ZONE_WS": "terrace_m2", "INT_ZONE_GR": "walk_m2", "INT_WATER_strip": "strip_m2"}
TAG_KEYS = {"roof": "roof_m2", "walk": "walk_m2", "riverside_walk": "riverside_walk_m2", "terrace": "terrace_m2",
            "strip": "strip_m2", "pond_land": "pond_land_ha", "cropland": "cropland_ha", "orchard": "orchard_ha"}

# ------------------------------------------------------------------ method constants (sources: NOTES.md)
TAW_M = 0.13                 # FAO-56 Table 19, nearest row to the SoilGrids clay loam, low end (safe side)
CROP_SOIL = dict(olive=dict(Zr=1.2, p=0.65), cotton=dict(Zr=1.0, p=0.65), maize=dict(Zr=1.0, p=0.55),
                 tomato=dict(Zr=0.7, p=0.40))      # FAO-56 Table 22, lower end of root depth
FALLOW_KC = 0.30             # FLAG: bare soil between annual crops
INFIL_MAX = 50.0             # FLAG: mm/day that can soak in
DRIP_EFF = 0.90              # FAO Training Manual 4 ch.3
STRIP_SEEP = 5.0             # mm/day, clay-sealed bed (rain_river s.4)
EVAP_OW = 1.05               # FAO-56 open water
SEEP_LINED = 0.5             # FLAG: mm/day through a pond liner
POND_DEPTH, POND_USE = 3.0, 0.7   # DESIGN / FLAG
CRATE_DEPTH, CRATE_VOID = 1.5, 0.95  # FLAG / Wavin
INTAKE_DAYS = 60.0           # intake fills at most V/60 per day
MAX_AGE = 365                # Aras 07:59: no water sits in storage more than a year; older water goes to the strip/river
SURF = dict(roof=(0.90, 1.0, 1.00), walk=(0.75, 1.5, 0.90), terrace=(0.04, 10.0, 1.00))  # C, Ia mm, capture (FLAG)
STRIP_TODAY = 26675.0        # today's storage, the strip only (rain_river A6, sealed worst case)
# costs: Ross & Hasnain 2018 (MAR, levelised USD); UK EA 2015 / Royal Haskoning 2012 SuDS capital GBP x 1.25 (FLAG)
RECHARGE_USD = (0.19, 0.45)
ALTERNATIVE_USD = (0.74, 1.89)  # recycled water through aquifer recharge
GBP, RATE = 1.25, 0.05
BUILT = [("pond", "Ponds, vacant land", (15, 55), 25), ("crates", "Crates under walks", (200, 350), 30),
         ("cistern", "Cisterns, plazas", (449, 590), 50)]
CASES = (("strict", RECHARGE_USD[1], ALTERNATIVE_USD[0]), ("central", sum(RECHARGE_USD) / 2, sum(ALTERNATIVE_USD) / 2),
         ("loose", RECHARGE_USD[0], ALTERNATIVE_USD[1]))
STEP = 5000.0                # m3, storage sweep step
ET0_NORMAL = 1369.1          # mm/yr, FAO-56 Penman-Monteith on WMO 17742 normals (v1 table B1)

# v3: how the stream behaves (the band beside the title). Natural flow past the site, m³ a month Jan-Dec:
# rain_river_levels/tables/A2_rain_to_river_monthly_m3.csv "from_catchment_m3" (DSİ gauges D04A053 + D04A063,
# Oct 2015-Sep 2021, each area-scaled to 101 km², mean of the two; the upper case, the Kestel diversion not counted).
STREAM_MONTH_M3 = [7073107, 4466564, 3692654, 2319752, 917943, 427462, 154468, 39136, 37531, 208432, 513967, 1101169]
STREAM_DRY_DAYS = (0, 111)   # measured: days a year both gauges were completely dry, 2016-2021 (rain_river README §1)
# v6 (T3b): the 1:500 upstream-entry flood cut (STREAM_CUT, CUT_Q500, K4_RIGHT_BANK, K4_Q100, STREAM_DEN) left the
# sheet: flood levels belong to the sections (p.13, the level table), not to the water balance

def bergama_data(name, _c={}):
    """Built-in data kept in Downloads/Bergama/Data/bergama_water_balance_data.py (Aras 25 Oct 21:29, scripts shortened): runs its
    section `name` here, as if it were written in this place. The file is read once per run; a missing file or one
    from another version of this script stops the script with a message saying which file to copy."""
    import os as _os, hashlib as _hl
    if not _c:
        p_ = _os.path.join(_os.path.expanduser("~"), "Downloads", "Bergama", "Data", "bergama_water_balance_data.py")
        if not _os.path.isfile(p_):
            raise RuntimeError("Data file missing: copy bergama_water_balance_data.py from the run kit's Data folder into " + _os.path.dirname(p_))
        with open(p_, encoding="utf-8", newline="") as f_:
            for part_ in f_.read().split("\n#@@ ")[1:]:
                k_, _, b_ = part_.partition("\n")
                _c[k_] = b_
    b_ = _c.get(name)
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != {'INPUT_DATA': '1c4b3056c69043ddf2d0e860039d5e8b', 'ZONE_COPY': 'f6b0e5bb3b4894b038cff898d3ce30fb', 'FACTS': 'e402c1370c04b7b8df8f86c4eccbf011'}.get(name):
        raise RuntimeError("Data file bergama_water_balance_data.py is not the one made with this script version (part " + name +
                           "): copy it again from the same run kit as the script")
    exec(compile(b_, "bergama_water_balance_data.py:" + name, "exec"), globals())


bergama_data("INPUT_DATA")
# v6 (T3b WO-T3b-2): ZONE_COPY = the Option A zones and links of zone base v7 (the masterplan's data/ZONE_COPY.py,
# md5 7c7d4a4a21af391460ac0701ae5e3902, Option A only, rings thinned to 10 cm), JSON {zones: [{code, label, id,
# study_area, zone, ring}], links: [{kind, label, P}]}, zlib + base64; used when the open Rhino file has no zones
bergama_data("ZONE_COPY")

# ------------------------------------------------------------------ lands: GH inputs > Rhino objects > defaults
def _num(v):
    try:
        return float(v) if v is not None and str(v).strip() != "" else None
    except (TypeError, ValueError):
        return None

def rhino_lands(option):
    """Areas from the open Rhino file (m2, or ha for land keys); {} when not in Rhino or nothing is found."""
    try:
        import Rhino
        doc = Rhino.RhinoDoc.ActiveDoc
    except Exception:
        return {}
    if doc is None:
        return {}
    s2 = Rhino.RhinoMath.UnitScale(doc.ModelUnitSystem, Rhino.UnitSystem.Meters) ** 2
    out = {}
    for o in doc.Objects.GetObjectList(Rhino.DocObjects.ObjectType.Curve):
        g = o.Geometry
        if not g.IsClosed:
            continue
        tag = (o.Attributes.GetUserString("water_balance") or "").strip().lower()
        if tag:
            key = TAG_KEYS.get(tag)
        else:
            path = doc.Layers[o.Attributes.LayerIndex].FullPath
            key = ZONE_LAYERS.get(path.split("::")[-1]) if path.startswith("Option_" + option + "::") else None
        if not key:
            continue
        amp = Rhino.Geometry.AreaMassProperties.Compute(g)
        if amp is None:
            continue
        a = amp.Area * s2
        out[key] = out.get(key, 0.0) + (a / 1e4 if key.endswith("_ha") else a)
    return out

def masterplan_lands(option):
    """v2.1: {riverside_walk_m2: ...} and its source from bergama_masterplan v11's masterplan_results.json.
    v10 (C10): (lands, source note, fresh): fresh = the masterplan wrote it in THIS chain run (bg_this_run)."""
    fresh, note = bg_this_run(MP_FILE)
    try:
        with open(MP_FILE, "r", encoding="utf-8") as f:
            v = json.load(f)["options"][option]["riverside_walk_m2"]
        return {"riverside_walk_m2": float(v)}, "masterplan results (" + note + ")", fresh
    except Exception:
        return {}, None, False

def get_lands(g):
    option = "A"                                         # v2.3: option A only, project-wide (Aras 25 Oct 16:43)
    rh = rhino_lands(option)
    mp, mp_src, mp_fresh = masterplan_lands(option)
    L, src = {}, {}
    for k, v in LANDS.items():
        gv = g.get(k)
        if k == "cropland_crops":
            L[k] = str(gv) if gv else v; src[k] = "gh" if gv else "default"
        elif _num(gv) is not None:
            L[k] = _num(gv); src[k] = "gh"
        elif k in rh:
            L[k] = rh[k]; src[k] = "rhino option " + option
        elif k in mp:
            L[k] = mp[k]; src[k] = mp_src + " option " + option
        else:
            L[k] = v; src[k] = "default"
    L["option"] = option
    if src["riverside_walk_m2"] == "default":            # v10 (C10): a placeholder is never silent
        wn_warn(WB_PAGE, "stale", u"riverside walks %s m² = the built-in placeholder (no masterplan results at %s); "
                u"run the masterplan before this component" % (fmt(L["riverside_walk_m2"]), MP_FILE))
    elif src["riverside_walk_m2"].startswith("masterplan") and not mp_fresh:
        wn_warn(WB_PAGE, "stale", u"riverside walks %s m² from the masterplan of an EARLIER run (%s): wire this "
                u"component after the masterplan so one press gives one answer" % (fmt(L["riverside_walk_m2"]), mp_src))
    return L, src

# ------------------------------------------------------------------ v6: the project's zones and links, for p.12's map
ZONE_CODES = ("WS", "WT", "WD", "GR", "WA", "WP", "DG")    # retention terraces, reed basins, spillway, walks / dry tops,
                                                          # bed + flood terraces, streamside planting, Demeter's Garden

def ring_area(P):
    return abs(sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))) / 2.0

def rhino_zones(option):
    """v6: (zones, links) of Option_<option> in the open Rhino file, survey m: closed curves on INT_ZONE_<code> and
    INT_WATER_strip (code "STRIP"), with the zone base's user text (label, id, study_area, zone); INT_LINK_<kind>
    curves as start -> end. None when not in Rhino or the file has none."""
    try:
        import Rhino
        doc = Rhino.RhinoDoc.ActiveDoc
    except Exception:
        return None
    if doc is None:
        return None
    s = Rhino.RhinoMath.UnitScale(doc.ModelUnitSystem, Rhino.UnitSystem.Meters)
    parent = "Option_" + option + "::"
    zones, links = [], []
    for o in doc.Objects.GetObjectList(Rhino.DocObjects.ObjectType.Curve):
        path = doc.Layers[o.Attributes.LayerIndex].FullPath
        if not path.startswith(parent):
            continue
        lay = path[len(parent):].split("::")[0]
        g, a = o.Geometry, o.Attributes
        meta = dict((k, a.GetUserString(k)) for k in ("label", "id", "study_area", "zone") if a.GetUserString(k))
        meta.setdefault("label", a.Name or "")
        if lay.startswith("INT_LINK_"):
            p0, p1 = g.PointAtStart, g.PointAtEnd
            links.append(dict(kind=lay[len("INT_LINK_"):], label=meta["label"],
                              P=[[round(p0.X * s, 2), round(p0.Y * s, 2)], [round(p1.X * s, 2), round(p1.Y * s, 2)]]))
            continue
        code = "STRIP" if lay == "INT_WATER_strip" else (lay[len("INT_ZONE_"):][:2].upper() if lay.startswith("INT_ZONE_") else None)
        if code not in ZONE_CODES + ("STRIP",) or not g.IsClosed:
            continue
        pts = None
        try:
            ok, pl = g.TryGetPolyline()
            if ok:
                pts = [(p.X, p.Y) for p in pl]
        except Exception:
            pts = None
        if not pts:                                     # a smooth curve: points about every 50 cm
            ts = g.DivideByCount(max(8, min(800, int(g.GetLength() * s / 0.5))), True) or []
            pts = [(g.PointAt(t).X, g.PointAt(t).Y) for t in ts]
        if len(pts) > 1 and pts[0] == pts[-1]:
            pts = pts[:-1]
        if len(pts) < 3:
            continue
        ring = [[round(x * s, 2), round(y * s, 2)] for x, y in pts]
        zones.append(dict(meta, code=code, ring=ring, m2=round(ring_area(ring), 1)))
    return (zones, links) if zones else None

def get_zones(option="A"):
    """v6: the results key "zones": the open Rhino file's Option A zones when it has the reed basins, else the
    built-in copy (data/ZONE_COPY.py); the water board's p.12 water map reads it."""
    rz = rhino_zones(option)
    if rz and any(z["code"] == "WT" for z in rz[0]):
        zs, ls, src = rz[0], rz[1], "rhino option " + option
    else:
        d = json.loads(zlib.decompress(base64.b64decode("".join(ZONE_COPY))).decode("utf-8"))
        zs, ls, src = d["zones"], d["links"], "built-in copy (zone base v7, option A)"
        for z in zs:
            z["m2"] = round(ring_area(z["ring"]), 1)
    return dict(source=src, option=option, zones=zs, links=ls,
                note="survey m; zones: INT_ZONE_<code> and INT_WATER_strip (code STRIP); links: INT_LINK_<kind>, start -> end")

# ------------------------------------------------------------------ built-in daily inputs
def load_inputs():
    d = json.loads(zlib.decompress(base64.b64decode("".join(INPUT_DATA))).decode("utf-8"))
    d0 = dt.date.fromisoformat(d["start"])
    d["days"] = [d0 + dt.timedelta(i) for i in range(d["n"])]
    d["P"] = [x / 100.0 for x in d["P"]]; d["E"] = [x / 100.0 for x in d["E"]]
    d["KC"] = {c: [x / 1000.0 for x in k] for c, k in d["KC"].items()}
    return d

def wy(d): return d.year + 1 if d.month >= 10 else d.year

# ------------------------------------------------------------------ farms: FAO-56 ch.8 daily soil water balance
def soil_irrigation(crop, I, use_rain=True):
    """Daily net irrigation (mm): Dr = Dr - Pe + Kc ET0; refill to field capacity when Dr > RAW (in season)."""
    s = CROP_SOIL[crop]; TAW = 1000 * TAW_M * s["Zr"]; RAW = s["p"] * TAW
    kc, ever = I["KC"][crop], I["EVERGREEN"][crop]
    Dr, out = 0.0, []
    for d, P, E in zip(I["days"], I["P"], I["E"]):
        k = kc[min(d.timetuple().tm_yday - 1, 364)]
        Pe = min(P if (use_rain and P >= 0.2 * E) else 0.0, INFIL_MAX)
        Dr = max(0.0, Dr - Pe) + (k if k > 0 else FALLOW_KC) * E
        x = 0.0
        if (ever or k > 0) and Dr > RAW:
            x = Dr; Dr = 0.0
        elif Dr > TAW:
            Dr = TAW
        out.append(x)
    return out

def ranked(vals):
    s = sorted(vals); n = len(s)
    q = lambda f: s[int(round(f * (n - 1)))]
    return dict(mean=sum(s) / n, median=s[n // 2], wet5=q(0.2), dry5=q(0.8), dry10=q(0.9), min=s[0], max=s[-1])

# ------------------------------------------------------------------ storage: daily, first in first out
def strip_reserve(strip, days):
    rem = [0.0] * len(days); acc = 0.0
    for i in range(len(days) - 1, -1, -1):
        d = days[i]
        acc = 0.0 if (d.month == 10 and d.day == 31) or d.month in (11, 12, 1, 2, 3, 4) else acc
        acc += strip[i]; rem[i] = acc if 5 <= d.month <= 10 else 0.0
    best = defaultdict(float)
    for d, r in zip(days, rem): best[(d.month, d.day)] = max(best[(d.month, d.day)], r)
    return [best[(d.month, d.day)] for d in days]

def run_storage(V, A, demand, strip, inflow, et0, days, reserve, max_age=MAX_AGE, site=None, lev=None):
    """v3: with site (the site catch each day) also counts per water year the stream's part of what enters the
    store (per[y][4]) and all that enters it (per[y][5]): the site catch fills first, the stream tops up.
    v6: with lev (a list) the store's level at the end of every day is appended to it."""
    Q = deque(); S = 0.0; flushed = 0.0; oldest = 0
    per = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])   # v4: [6] released after max_age, [7] store at the end
    i = 0
    def take(n, keep=0.0):
        nonlocal S, oldest
        n = min(n, max(0.0, S - keep)); got = 0.0
        while n > 1e-9 and Q:
            t = min(n, Q[0][1]); oldest = max(oldest, i - Q[0][0])
            Q[0][1] -= t; n -= t; got += t
            if Q[0][1] <= 1e-9: Q.popleft()
        S -= got
        return got
    for i, d in enumerate(days):
        while Q and i - Q[0][0] >= max_age:
            flushed += Q[0][1]; per[wy(d)][6] += Q[0][1]; S -= Q[0][1]; Q.popleft()
        x = min(V - S, inflow[i])
        if x > 0:
            Q.append([i, x]); S += x
            if site is not None: r_ = per[wy(d)]; r_[4] += max(0.0, x - site[i]); r_[5] += x
        if A and S > 0:
            loss = min(S, A * min(1.0, S / max(V, 1.0)) * (et0[i] * EVAP_OW + SEEP_LINED) / 1000)
            S -= loss
            while loss > 1e-9 and Q:
                t = min(loss, Q[0][1]); Q[0][1] -= t; loss -= t
                if Q[0][1] <= 1e-9: Q.popleft()
        gs = take(strip[i]); gf = take(demand[i], reserve[i])
        r = per[wy(d)]; r[0] += demand[i]; r[1] += gf; r[2] += strip[i]; r[3] += gs; r[7] = S
        if lev is not None: lev.append(S)
    return per, flushed, oldest

def store_months(V, demand, strip, R, site, et0, days, reserve):
    """v6 (T3b, G7): the closed design store V through the same daily run as year_split: its mean level at the end of
    each calendar month, m3, Jan-Dec (the first water year, the spin-up, left out). Sheet block 1, the store's row."""
    inflow = [min(V / INTAKE_DAYS, r) + s for r, s in zip(R, site)]
    lev = []
    run_storage(V, 0.0, demand, strip, inflow, et0, days, reserve, lev=lev)
    y0 = wy(days[0]); acc = defaultdict(list)
    for i, d in enumerate(days):
        if wy(d) == y0: continue
        if i + 1 == len(days) or days[i + 1].month != d.month: acc[d.month].append(lev[i])
    return [round(sum(acc[m]) / len(acc[m])) if acc[m] else 0 for m in range(1, 13)]

def crf(r, n): return r * (1 + r) ** n / ((1 + r) ** n - 1)

def year_split(V, demand, strip, R, site, et0, days, reserve, avail, fd):
    """v4 (Aras 27 Oct, Prompt 6): the closed store V (no open water, so no evaporation) through two water years of one
    daily run: "normal" = the year whose farm need is nearest the median, "dry5" = the 1-in-5 dry year of the farm need
    (fd["dry5_year"]; the nearest year when that is the spin-up year). m3 per water year (Oct-Sep):
    carried in + filled = strip + farms + released + carried out."""
    inflow = [min(V / INTAKE_DAYS, r) + s for r, s in zip(R, site)]
    per, _, _ = run_storage(V, 0.0, demand, strip, inflow, et0, days, reserve, site=site)
    ys = sorted(per)
    start = {y: (per[ys[k - 1]][7] if k else 0.0) for k, y in enumerate(ys)}
    ys = ys[1:]                                             # the first water year is the spin-up (the store starts empty)
    near = lambda v: min(ys, key=lambda y: abs(per[y][0] - v))
    yd = fd["dry5_year"] if fd.get("dry5_year") in ys else near(fd["dry5"])
    yn = near(fd["median"])
    a_med = sorted(avail[y] for y in ys)[len(ys) // 2]
    out = {}
    for k, y in (("normal", yn), ("dry5", yd)):
        r = per[y]
        out[k] = dict(water_year="%d-%02d" % (y - 1, y % 100), carried_in_m3=round(start[y]), filled_m3=round(r[5]),
                      strip_m3=round(r[3]), strip_need_m3=round(r[2]), farms_m3=round(r[1]), farm_need_m3=round(r[0]),
                      released_m3=round(r[6]), carried_out_m3=round(r[7]),
                      winter_flow_pct_of_median=round(100.0 * avail[y] / max(a_med, 1.0), 1))
    out["storage_m3"] = int(V)
    out["note"] = "closed store, one daily run; normal = median farm-need year, dry5 = 1-in-5 dry year of the farm need"
    return out

def compute(L):
    I = load_inputs(); days, P, E, R = I["days"], I["P"], I["E"], I["R"]
    nY = len(set(wy(d) for d in days))
    crops = ["olive"] + [c.strip().lower() for c in L["cropland_crops"].split(",") if c.strip().lower() in CROP_SOIL and c.strip().lower() != "olive"]
    crops = list(dict.fromkeys(crops))
    if len(crops) == 1: crops.append("cotton")
    irr = {c: soil_irrigation(c, I) for c in set(crops) | set(CROP_SOIL)}
    res = dict(script="bergama_water_balance_v8_3.py", version=VERSION, run_time=time.strftime("%Y-%m-%d %H:%M:%S"),
               lands={k: (round(v, 3) if isinstance(v, float) else v) for k, v in L.items()})
    # net irrigation per crop (mm a water year) and the rain the fields hold
    res["net_irrigation_mm"] = {}; res["rain_credit_pct"] = {}
    for c in CROP_SOIL:
        by = defaultdict(float)
        for d, x in zip(days, irr[c]): by[wy(d)] += x
        res["net_irrigation_mm"][c] = {k: round(v, 1) for k, v in ranked(list(by.values())).items()}
        dry = sum(soil_irrigation(c, I, use_rain=False))
        res["rain_credit_pct"][c] = round(100.0 * (1 - sum(irr[c]) / dry), 1) if dry else 0.0
    # supplies and the strip
    sa = [("roof", L["roof_m2"]), ("walk", L["walk_m2"] + L["riverside_walk_m2"]), ("terrace", L["terrace_m2"])]
    site = [sum(a * SURF[s][2] * SURF[s][0] * max(0.0, p - SURF[s][1]) / 1000 for s, a in sa) for p in P]
    strip = [(L["strip_m2"] * (e * EVAP_OW + STRIP_SEEP) / 1000) if 5 <= d.month <= 10 else 0.0 for d, e in zip(days, E)]
    RES = strip_reserve(strip, days)
    mon = lambda series: [round(sum(x for d, x in zip(days, series) if d.month == m + 1) / nY) for m in range(12)]
    res["river_month_m3"] = mon(R); res["strip_month_m3"] = mon(strip); res["site_month_m3"] = mon(site)
    res["strip_m3_per_year"] = round(sum(strip) / nY)
    steps = [("Roofs", "roof", L["roof_m2"]), ("Walk tops", "walk", L["walk_m2"]),
             ("Streamside walks", "walk", L["riverside_walk_m2"]), ("Retention terraces", "terrace", L["terrace_m2"])]
    res["site_catch_steps"] = [dict(name=n, m2=round(a), m3_per_year=round(sum(a * SURF[s][2] * SURF[s][0] * max(0.0, p - SURF[s][1]) / 1000 for p in P) / nY))
                               for n, s, a in steps]
    res["site_catch_m3_per_year"] = round(sum(site) / nY)
    # farm demand per mix (m3 at the intake, drip)
    res["farm_demand_m3"] = {}; res["farm_demand_month_m3"] = {}; dem = {}
    for c in crops[1:]:
        mix = "orchard olive + cropland " + c
        dem[mix] = [(L["orchard_ha"] * irr["olive"][i] + L["cropland_ha"] * irr[c][i]) / DRIP_EFF * 10 for i in range(len(days))]
        by = defaultdict(float)
        for d, x in zip(days, dem[mix]): by[wy(d)] += x
        rk = ranked(list(by.values()))
        y5 = min(by, key=lambda y: abs(by[y] - rk["dry5"]))
        res["farm_demand_m3"][mix] = dict({k: round(v) for k, v in rk.items()}, dry5_year=y5)
        res["farm_demand_month_m3"][mix] = dict(mean=mon(dem[mix]),
                                                dry5=[round(sum(x for d, x in zip(days, dem[mix]) if wy(d) == y5 and d.month == m + 1)) for m in range(12)])
    avail = defaultdict(float)                              # v3: the stream's winter water an intake may take, per water year
    for d, r in zip(days, R): avail[wy(d)] += r
    def stats(V, mix, Vopen=0.0):
        inflow = [min(V / INTAKE_DAYS, r) + s for r, s in zip(R, site)]
        per, fl, old = run_storage(V, Vopen / POND_DEPTH, dem[mix], strip, inflow, E, days, RES, site=site)
        per.pop(min(per))                                   # first water year = spin-up (storage starts empty)
        cov = sorted(per[y][1] / per[y][0] for y in per if per[y][0] > 0)
        n = len(cov)
        tk = [per[y][4] / avail[y] for y in per if avail[y] > 0]     # v3: share of each year's winter water taken
        return dict(median=cov[n // 2], dry5=cov[int(round(0.2 * (n - 1)))], dry10=cov[int(round(0.1 * (n - 1)))],
                    delivered=sum(per[y][1] for y in per) / len(per), released=fl / len(per), oldest=old,
                    strip_min=min(per[y][3] / per[y][2] for y in per if per[y][2] > 0) if any(per[y][2] for y in per) else 1.0,
                    river_in=sum(per[y][4] for y in per) / len(per), stored=sum(per[y][5] for y in per) / len(per),
                    river_share=sum(per[y][4] for y in per) / max(sum(avail[y] for y in per), 1.0),
                    river_share_max=max(tk) if tk else 0.0, avail=sum(avail[y] for y in per) / len(per))
    pct = lambda x: round(100.0 * x, 1)
    # closed storage swept in steps until one more step is not worth even the cheapest recharge (loose case)
    res["curve_closed"] = {}; res["cutoff"] = {}; res["need_for_target_1in5_dry_m3"] = {}; res["today_strip_storage"] = {}
    for mix in dem:
        rows = []; V = 0.0; low = 0; started = False; lim = 6.0 * res["farm_demand_m3"][mix]["max"] + 1e5
        while V <= lim:
            st = stats(V, mix); rows.append((V, st))
            if len(rows) > 1:
                md = (st["delivered"] - rows[-2][1]["delivered"]) / STEP
                started = started or st["delivered"] > 0
                low = low + 1 if started and md < CASES[2][1] / CASES[2][2] else 0
                if low >= 3 or (started and st["dry5"] >= 0.9999 and low >= 1): break
            V += STEP
        res["curve_closed"][mix] = [[int(v), pct(s["median"]), pct(s["dry5"]), pct(s["dry10"]), round(s["delivered"]), round(s["released"]), s["oldest"]] for v, s in rows]
        cut = {}
        for case, c, alt in CASES:
            ok = [rows[j][0] for j in range(1, len(rows)) if (rows[j][1]["delivered"] - rows[j - 1][1]["delivered"]) / STEP >= c / alt]
            Vc = max(ok) if ok else 0.0
            s = dict(rows)[Vc]
            cut[case] = dict(storage_m3=int(Vc), recharge_usd_m3=round(c, 3), alternative_usd_m3=round(alt, 3),
                             covered_pct_1in5_dry=pct(s["dry5"]), covered_pct_median=pct(s["median"]), covered_pct_1in10_dry=pct(s["dry10"]),
                             delivered_m3_per_year=round(s["delivered"]), released_365d_m3_per_year=round(s["released"]),
                             oldest_days=s["oldest"], strip_served_pct_worst_year=pct(s["strip_min"]))
        res["cutoff"][mix] = cut
        nt = {}
        for t in (25, 50, 75, 100):
            hit = None
            for j in range(1, len(rows)):
                a, b = rows[j - 1], rows[j]
                if b[1]["dry5"] * 100 >= t - 1e-6:
                    f = (t / 100.0 - a[1]["dry5"]) / max(b[1]["dry5"] - a[1]["dry5"], 1e-9)
                    hit = int(round((a[0] + f * STEP) / 1000.0) * 1000); break
            nt[str(t)] = hit
        res["need_for_target_1in5_dry_m3"][mix] = nt
        s = stats(STRIP_TODAY, mix)
        res["today_strip_storage"][mix] = dict(storage_m3=STRIP_TODAY, covered_pct_1in5_dry=pct(s["dry5"]), strip_served_pct_worst_year=pct(s["strip_min"]))
    design = max(dem, key=lambda m: res["cutoff"][m]["central"]["storage_m3"])
    allc = [res["cutoff"][m][k] for m in dem for k in res["cutoff"][m]]
    dc = res["cutoff"][design]["central"]
    res["design"] = dict(mix=design, case="central", storage_m3=dc["storage_m3"], covered_pct_1in5_dry=dc["covered_pct_1in5_dry"],
                         covered_pct_median=dc["covered_pct_median"],
                         central_range_m3=[min(res["cutoff"][m]["central"]["storage_m3"] for m in dem), dc["storage_m3"]],
                         central_range_pct_1in5_dry=[min(res["cutoff"][m]["central"]["covered_pct_1in5_dry"] for m in dem), max(res["cutoff"][m]["central"]["covered_pct_1in5_dry"] for m in dem)],
                         full_range_m3=[min(x["storage_m3"] for x in allc), max(x["storage_m3"] for x in allc)],
                         full_range_pct_1in5_dry=[min(x["covered_pct_1in5_dry"] for x in allc), max(x["covered_pct_1in5_dry"] for x in allc)],
                         note="aquifer recharge sized by cost; valid only if borehole tests accept recharge (arsenic, DSI rights)")
    # v3: what the stream gives at the design store (mean of the water years after the spin-up year)
    st = stats(dc["storage_m3"], design)
    res["design"].update(river_take_m3_per_year=round(st["river_in"]),
                         river_take_share_pct=round(100.0 * st["river_in"] / max(st["stored"], 1.0), 1),
                         river_left_pct=[round(100.0 * (1.0 - st["river_share_max"]), 1), round(100.0 * (1.0 - st["river_share"]), 1)])
    res["river_avail_m3_per_year"] = round(st["avail"])
    # v4 (Prompt 6): the design store through a normal and the 1-in-5 dry water year, from the same daily run
    res["design"]["year_split"] = year_split(dc["storage_m3"], dem[design], strip, R, site, E, days, RES, avail,
                                             res["farm_demand_m3"][design])
    res["design"]["store_month_m3"] = store_months(dc["storage_m3"], dem[design], strip, R, site, E, days, RES)   # v6
    # open ponds for comparison (design mix) and the built-storage ladder without recharge (US$ per m3 delivered)
    vmax = res["curve_closed"][design][-1][0]
    res["curve_open"] = [[int(v), pct(s["median"]), pct(s["dry5"])] for v in [vmax * k / 8.0 for k in range(9)] for s in [stats(v, design, v)]]
    caps = dict(pond=L["pond_land_ha"] * 1e4 * POND_DEPTH * POND_USE, crates=(L["walk_m2"] + L["riverside_walk_m2"]) * CRATE_DEPTH * CRATE_VOID,
                cistern=150000.0)
    lad = []; Vc = Vo = 0.0; prev = stats(0.0, design)["delivered"]
    for key, name, gbp, life in BUILT:
        cap = caps[key]
        if cap <= 0: continue
        if key == "pond": Vo += cap
        else: Vc += cap
        st = stats(Vc + Vo, design, Vo)
        dd = max(st["delivered"] - prev, 1e-6); prev = st["delivered"]
        f = crf(RATE, life) * GBP * cap / dd
        lad.append(dict(key=key, step=name, from_m3=round(Vc + Vo - cap), to_m3=round(Vc + Vo), added_delivery_m3_per_year=round(dd),
                        usd_per_m3_low=round(gbp[0] * f, 2), usd_per_m3_high=round(gbp[1] * f, 2), covered_pct_1in5_dry=pct(st["dry5"])))
    res["ladder_no_recharge"] = lad
    res["recharge_usd_m3"] = list(RECHARGE_USD); res["alternative_usd_m3"] = list(ALTERNATIVE_USD)
    return res

def read_results(path=None):
    """For other scripts: the latest results dict (design storage and % under res['design']), or None."""
    p = path or bg_first([os.path.join(RES_DIR, OUT_JSON), os.path.join(OUT_DIR, OUT_JSON), os.path.join(OLD_OUT_DIR, OUT_JSON)])
    try:
        with open(p, encoding="utf-8") as f: return json.load(f)
    except Exception:
        return None

# ------------------------------------------------------------------ colours (palette v1.4 core roles)
C = dict(ground="E2E0D4", paper="EFEDE6", faint="D8D5CC", structure="B0AC9C", ink2="847E75", ink="4A3F35",
         green_deep="495338", green_mid="727A4E", green_light="8C9969", water_deep="5D7F8D", water="91ADB4",
         water_light="C1D3DB", accent="8B3A3F", accent_deep="633131", white="FFFFFF")
C["accent_tint"] = "".join("%02X" % int(round(255 - 0.12 * (255 - int(C["accent"][i:i + 2], 16)))) for i in (0, 2, 4))   # v2.7: accent at 12 % on white (the Jun-Sep band)
C["water_tint"] = "".join("%02X" % int(round(255 - 0.15 * (255 - int(C["water_light"][i:i + 2], 16)))) for i in (0, 2, 4))  # revision 30 Oct (p10, G5): water_light at 15 % on white (was 40 %), the answer's light field
CROP_NAME = dict(maize="corn")            # v5 (MIRAQUA 28 Oct, G11): the name printed for a crop key (keys unchanged)

def rgb(h): return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
# ---- Category -> hue table (round 6 S1, 4 Nov 2026; G6-6, Q5, Q7; PLAN.md §2.6) ------------------------------------
# ONE table every legend reads (Aras 4 Nov 09:44-10:08: "categorize the legends like heritage is categorized under
# heritage with similar shades of the same colour. The darker the shade is the more important it is"): each category
# one hue, items inside it = its ranks, r1 darkest = most important; never a separate hue per item. Subtle set on
# every plan, section, chart and legend; strong set (HUE_KEY) on key maps only. Values: PLAN.md §2.6 ->
# revision_2026-11-04_round6/plan_findings/hues_and_proposals.md H2 (method and contrast checks there).
# Included by common/keymap.py (so every script that includes basemap.py has it); a script without basemap.py (the
# booklet) includes it itself, once.
#   HUE[code][rank] hex      HUE_KEY[name] hex      hue(code, rank, strong=False)      HER_RANK[name] -> 1/2/3
#   legend_group(entries)    entries sorted by category (table order) then rank
#   hue_log(page, log=None)  the line `legend <page> hues=table`
HUE_CATS = ("CTX", "HER", "WAT", "WW", "GRN", "AGR", "MOV", "PUB")          # legend order: context first
HUE_NAMES = {"CTX": u"Existing context", "HER": u"Heritage", "WAT": u"The Selinos stream",
             "WW": u"Water works: collect, clean, hold", "GRN": u"Planting", "AGR": u"Farms",
             "MOV": u"Streets, shops and movement", "PUB": u"Public life and hubs"}
HUE = {
    # existing context: ground, buildings, streets, bridges, existing green (with tree symbols), workshops, vacant
    "CTX": {1: "4A3F35", 2: "847E75", 3: "B0AC9C", 4: "D8D5CC", 5: "EFEDE6"},
    # heritage (Q5): r1 inside the UNESCO World Heritage listing, r2 registered monument, r3 other historic or no
    # sourced status, r4 heritage area tint
    "HER": {1: "512E1A", 2: "84573E", 3: "B08870", 4: "E7CABB"},
    "WAT": {1: "32525F", 2: "5D7F8D", 3: "91ADB4", 4: "C1D3DB"},
    # water works: reed basins, spillway, winter store, dry-top terraces, side arm, widened wetland
    "WW": {1: "2D564E", 2: "54857D", 3: "87BBAA", 4: "CBEDE5"},
    # proposed planting: bands wet -> dry, forest corridor, designed green (plant swatches: tree r1, shrub r2,
    # ground / emergent r3, P-3)
    "GRN": {1: "3C4733", 2: "70754C", 3: "89986A", 4: "C2CCB3"},
    "AGR": {1: "534E25", 2: "948B49", 3: "C6C08D", 4: "E6E3C5"},
    # streets and movement: pedestrian r1, calmed r2, shared r3; commerce r1, mixed r2, residential r3
    "MOV": {1: "734C17", 2: "A67628", 3: "CCA363", 4: "EAD1A4"},
    # public life: walking hubs, transit hub, sub-hubs, hub squares, market, civic, people groups by headcount
    "PUB": {1: "452842", 2: "7F5B7B", 3: "AE90AA", 4: "DECFDC"},
}
# annotations (not a category): study area line, plan cut marks (G6-4), text ink
HUE_ANN = {"study": "6A4C93", "cut": "8E8F8A", "ink": "2C2219"}
# strong set: key maps only (G6-5, the p08 "Where each street is cut" look)
HUE_KEY = {"fabric_mix": 0.40, "her1": "663214", "her2": "965630", "her3": "C18A65",
           "trees": "A0A681", "park": "B1B792", "grass": "C4C7A6", "farmland": "CFC99D",
           "stream": "7FA4B3", "stream_edge": "5E8494", "road": "FAF8F1", "road_edge": "DCD5C2",
           "street_names": "A4A1A3", "cut": "C0392B", "study": "6A4C93"}
HUE_NAME_PT = 4.0                    # key-map street names: exactly the 4 pt floor (PLAN §2.7)
# heritage ranks of the heritage-loop places (Q5; H3): Kızıl Avlu r1 is a reading (ICOMOS names its tunnels; the
# boundary is not stated): set it to 2 if Aras reads it as registered only. Teleferik is context (CTX), not heritage.
HER_RANK = {u"Akropol": 1, u"Kızıl Avlu": 1, u"Tabak Köprüsü": 3, u"Ulucami Önü Köprüsü": 3, u"Ulucami": 3,
            u"Ulu Cami": 3, u"Tabaklar Hamamı": 3, u"Arasta": 3, u"Üç Kemer Köprüsü": 3, u"Bergama Müzesi": 3,
            u"Asklepion": 3}
HUE_LOG = []


def hue(code, rank, strong=False):
    """the hex of category `code` at `rank` (1 = darkest, most important); strong=True on key maps: heritage ranks
    from HUE_KEY (her1-3), every other name of HUE_KEY by itself (hue("trees", 0, True)). An unknown code or rank
    raises (a legend never invents a colour); a rank past the ramp takes its lightest step with a WARNING line"""
    if strong:
        if code == "HER":
            return HUE_KEY["her%d" % min(3, max(1, int(rank)))]
        if code in HUE_KEY:
            return HUE_KEY[code]
    if code == "ANN":
        return HUE_ANN[rank]
    ramp = HUE[code]
    r = int(rank)
    if r not in ramp:
        HUE_LOG.append(u"WARNING legend: %s has no rank %s; its lightest step used" % (code, rank))
        r = max(ramp)
    return ramp[r]


def her_rank(name, default=3):
    """the heritage rank of a place name (HER_RANK; no sourced status = 3)"""
    return HER_RANK.get(name, default)


def legend_group(entries):
    """legend entries sorted by category (HUE_CATS order) then rank, darkest first. An entry is a dict with "cat"
    and "rank" (other keys kept), or a tuple (cat, rank, ...). Each dict gets "hex" (its table colour) and
    "cat_name" (the category's heading) when missing, so a legend draws only table hues"""
    def key(e):
        c, r = (e.get("cat"), e.get("rank")) if isinstance(e, dict) else (e[0], e[1])
        return (HUE_CATS.index(c) if c in HUE_CATS else len(HUE_CATS), r if isinstance(r, int) else 9)
    out = sorted(entries, key=key)
    for e in out:
        if isinstance(e, dict) and e.get("cat") in HUE:
            e.setdefault("hex", hue(e["cat"], e.get("rank") or 1))
            e.setdefault("cat_name", HUE_NAMES[e["cat"]])
    return out


def hue_log(page, log=None):
    """the done-when line of a legend drawn from this table: `legend <page> hues=table`"""
    ln = u"legend %s hues=table" % page
    (log if log is not None else HUE_LOG).append(ln)
    return ln


def _hu(code, rank):
    """v11 (G6-6): one colour of the shared hue table (common/hues.py) as the 6-hex string the drawings use"""
    return str(hue(code, rank)).lstrip("#").upper()

# ------------------------------------------------------------------ minimal vector PDF (mm units, Arial embedded)
# v9 (round 4, G-R4-1): the real font widths (font_metrics.py, Arial) and ONE text placer (text_place.py)
# ---- font_metrics.py (round 4, S1, 1 Nov 2026; G-R4-1, PLAN §4.1): REAL Arial widths and glyph boxes, one source -----
# Every width and text box in the scripts comes from here (the text placer text_place.py, the markers marker.py).
# It reads the same font files the sheets embed (pdf_fonts.py: arial.ttf / arialbd.ttf from the Windows font folder),
# so what is measured is what prints. A missing font RAISES FontMissing: there is no estimate fallback (CHK1_2 F2.1:
# the old Helvetica tables measured bold Ö as 600/1000 against Arial's 778, "walking hubthe busy hub").
# Needs pdf_fonts.py included before it (_pf_path, _pf_tables, _PF_FILES).
#   fm_load(bold=False, italic=False)          the font's tables (read once per run, cached)
#   fm_width(s, pt, bold=False)                -> mm   advance width of s at pt (no kerning: the sheets' PDF
#                                                      writers place glyphs by advance, so this is what prints)
#   fm_box(s, x, y, pt, bold=False, align="L", angle=0, y_down=True) -> (x0, y0, x1, y1) page mm
#                                              the box of s set with its baseline at (x, y): width = the advance
#                                              (or the ink if wider), height = the real ink of its glyphs (accents of
#                                              İ Ö Ü, the tails of ğ g y inside); angle in degrees, counter-clockwise
#                                              as seen on the page; align L / C / R at (x, y); "MC" = (x, y) is
#                                              the middle of the ink (the shape lists' middle-centre text)
#   fm_ink_box(s, pt, bold=True)               -> (x0, y0, x1, y1) mm, the visible glyph box with the pen at (0, 0)
#                                              on the baseline, y UP (for centring a glyph in a marker)
#   fm_asc_desc(pt, bold=False)                -> (ascender, descender) mm of the font (descender negative)
# Units: pt = font size in points (the em); 1 pt = 25.4 / 72 mm (FM_PT).
# Round 5 (S1, P04.7 "bazaar side ? Kale side"): a character the font has no glyph for no longer stops a run where the
# caller checks first:
#   fm_missing(s, bold=False) -> [ch]          the characters of s the font has no glyph for (blanks never count)
#   fm_safe(s, bold=False, sub=u"\u2013") -> (s2, missing)
#                                              s with each missing character replaced by sub ("–", else "-"); the
#                                              booklet composer runs every text through it at load (one WARNING each)
FM_PT = 25.4 / 72.0
_FM_CACHE = {}


class FontMissing(RuntimeError):
    pass


def fm_load(bold=False, italic=False):
    """the font tables for one style, read once per run; raises FontMissing when the font file is not there"""
    st = ("B" if bold else "") + ("I" if italic else "") or "R"
    if st not in _FM_CACHE:
        if "_pf_tables" not in globals():
            raise FontMissing("font_metrics needs common/pdf_fonts.py included before it")
        fn = _PF_FILES[st][0]
        p = _pf_path(fn)
        if not p:
            raise FontMissing("font %s not found (Windows font folder or the user's font folder): text cannot be "
                              "measured, so nothing is placed. Install Arial or copy %s there" % (fn, fn))
        with open(p, "rb") as fh:
            T = _pf_tables(fh.read())
        T["adv_c"], T["ink_c"] = {}, {}
        T["file"] = p
        _FM_CACHE[st] = T
    return _FM_CACHE[st]


def _fm_glyph(T, ch):
    """(advance, ink box or None) of one character in font units; raises when the font has no glyph for it"""
    a = T["adv_c"].get(ch)
    if a is None:
        g = T["gid"](ord(ch)) if ord(ch) <= 0xFFFF else 0
        if not g and ch not in u" ":
            raise ValueError(u"the font %s has no glyph for %r (U+%04X): use another character" % (
                T["file"], ch, ord(ch)))
        a = T["adv"][min(g, T["nhm"] - 1)]
        T["adv_c"][ch] = a
        T["ink_c"][ch] = T["glyph_box"](g) if g else None
    return a, T["ink_c"][ch]


def fm_width(s, pt, bold=False, italic=False):
    """advance width of s in mm at pt points"""
    T = fm_load(bold, italic)
    u = 0
    for ch in u"%s" % s:
        if ch in u"\r\n":
            continue
        u += _fm_glyph(T, ch)[0]
    return u * pt * FM_PT / float(T["upm"])


def fm_ink_box(s, pt, bold=True, italic=False):
    """the visible glyph box of s in mm, pen at (0, 0) on the baseline, y up: (x0, y0, x1, y1); an all-blank string
    gives its advance with zero height"""
    T = fm_load(bold, italic)
    k = pt * FM_PT / float(T["upm"])
    x, box = 0, None
    for ch in u"%s" % s:
        if ch in u"\r\n":
            continue
        a, b = _fm_glyph(T, ch)
        if b:
            r = (x + b[0], b[1], x + b[2], b[3])
            box = r if box is None else (min(box[0], r[0]), min(box[1], r[1]), max(box[2], r[2]), max(box[3], r[3]))
        x += a
    if box is None:
        return (0.0, 0.0, x * k, 0.0)
    return (box[0] * k, box[1] * k, box[2] * k, box[3] * k)


def fm_asc_desc(pt, bold=False, italic=False):
    """the font's ascender and descender (hhea) in mm at pt; descender is negative"""
    T = fm_load(bold, italic)
    k = pt * FM_PT / float(T["upm"])
    return T["asc"] * k, T["desc"] * k


def fm_box(s, x, y, pt, bold=False, align="L", angle=0.0, y_down=True, italic=False):
    """the page box (x0, y0, x1, y1) of s with its baseline at (x, y); see the module notes"""
    import math as _m
    w = fm_width(s, pt, bold, italic)
    ix0, iy0, ix1, iy1 = fm_ink_box(s, pt, bold, italic)
    a0, a1 = min(0.0, ix0), max(w, ix1)
    dx = {"L": 0.0, "C": -w / 2.0, "R": -w}.get(str(align or "L")[:1].upper(), 0.0)
    dv = 0.0
    if str(align or "").upper() in ("MC", "CM"):          # middle centre: (x, y) is the middle of the ink
        dx, dv = -w / 2.0, -(iy0 + iy1) / 2.0
    # corners in text space (along the baseline u, up from it v), then onto the page
    corners = [(a0 + dx, iy0 + dv), (a1 + dx, iy0 + dv), (a1 + dx, iy1 + dv), (a0 + dx, iy1 + dv)]
    t = _m.radians(angle or 0.0)
    c, s_ = _m.cos(t), _m.sin(t)
    sg = -1.0 if y_down else 1.0          # page y of "up"
    P = [(x + u * c - v * s_, y + sg * (u * s_ + v * c)) for u, v in corners]
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    return (min(xs), min(ys), max(xs), max(ys))


def fm_missing(s, bold=False, italic=False):
    """the characters of s the font has no glyph for"""
    T = fm_load(bold, italic)
    out = []
    for ch in u"%s" % s:
        if ch in u"\r\n\t " or ch in out:
            continue
        try:
            _fm_glyph(T, ch)
        except ValueError:
            out.append(ch)
    return out


def fm_safe(s, bold=False, sub=u"\u2013", italic=False):
    """(s with missing glyphs replaced by sub, the missing characters); sub falls back to "-" when the font lacks it"""
    miss = fm_missing(s, bold, italic)
    if not miss:
        return u"%s" % s, []
    if fm_missing(sub, bold, italic):
        sub = u"-"
    s2 = u"%s" % s
    for ch in miss:
        s2 = s2.replace(ch, sub)
    return s2, miss


def text_w(s, size, bold=False):
    """v9: the real Arial width (mm) of s at size pt"""
    return fm_width(s, size, bold)


# ---- G13 units (MIRAQUA round 28 Oct 2026; Aras 28 Oct 13:21; SCRIPT_STANDARD §8 "UNITS") -----------------------
# Dimensions in cm, areas in m², heights and levels in m with 2 decimals. Where a cm or m² figure would be unreadable,
# one step up (m or km; ha), the same for every drawing of a type, never mixed inside one drawing; every scale bar and
# dimension says its unit. Converting a unit never changes the value. Inputs are always metres / square metres.
def u_num(v, nd=0):
    """1,234,567 / 12.35: thousands with commas, nd decimals"""
    return ("{:,.%df}" % nd).format(v)


def u_dim(m, unit="cm", nd=None, bare=False):
    """a dimension (horizontal or a chain): 3.0 -> '300' (unit 'cm'), '3.00 m', '1.2 km'; bare = no unit (a chain
    whose unit is written once at its end)"""
    if unit == "cm":
        s = u_num(m * 100.0, 0 if nd is None else nd)
    elif unit == "km":
        s = u_num(m / 1000.0, 1 if nd is None else nd)
    else:
        s = u_num(m, 2 if nd is None else nd)
    return s if bare else s + " " + unit


def u_level(m, sign=True):
    """a level or spot height: +47.60 (always 2 decimals)"""
    return ("%+.2f" if sign else "%.2f") % m


def u_height(m):
    """a height or depth: '6.00 m' (always 2 decimals)"""
    return "%.2f m" % m


def u_area(m2, unit="m²", nd=None):
    """an area: '11,524 m²' or '1.15 ha' (1 ha = 10,000 m²)"""
    if unit == "ha":
        return u_num(m2 / 10000.0, (1 if m2 >= 100000.0 else 2) if nd is None else nd) + " ha"
    return u_num(m2, 0 if nd is None else nd) + u" m²"


def u_volume(m3, nd=0):
    return u_num(m3, nd) + u" m³"


# ---- the booklet's one icon set (02_SHARED_SYSTEMS §2, WO-T2b-1; M9 30 Oct: every icon has its legend name,
# ICO_LEGEND / ico_legend_entry): every symbol drawn on one 24-unit square grid,
# scaled to `size` page mm, with one stroke weight, one corner radius and one colour rule, so water, planting, plant,
# people and warning marks read as one family (quality bar: refs/R19, the crossed glass on page 18).
#   grid      24 x 24 units, origin at the icon centre, y up; drawing inside +-10 (2 units clear on every side)
#   stroke    ICO_LW_UNITS = 1.5 units = size / 16 page mm (0.375 at 6 mm, 1.25 at 20 mm); one weight per icon;
#             only the "not allowed" cross is heavier (1.5 x), on a paper casing
#   corners   boxes rounded at 1.5 units (one stroke); open lines end on whole or half grid units; gaps >= 2 units
#   colour    ink lines + at most two flat colours (c1, c2) from palette v1.4; c2 left None = c1 mixed 60 % to paper
#   text      none: numbers and labels are drawn by the caller (ico_step gives the anchor)
# Pure geometry: shapes in the house format of section_style.py, page mm, y up; the script's own put() draws them.
#   ("poly", ring, fill, stroke, lw)    ("line", pts, colour, lw)


# palette v1.4 (/mnt/project-files/palette/bergama_palette.py) and section_style.py SEC: hex without '#'
ICO_PAL = dict(
    ink="4A3F35",          # CORE ink
    paper="EFEDE6",        # CORE paper
    structure="B0AC9C",    # CORE structure
    water="91ADB4",        # CORE water
    water_deep="5D7F8D",   # CORE water_deep
    water_light="C1D3DB",  # CORE water_light
    green_mid="727A4E",    # CORE green_mid
    green_light="8C9969",  # CORE green_light
    olive="8E9A6C",        # section_style SEC olive
    reed="8E9466",         # section_style SEC reed
    agri="BDB57A",         # LAND_USE agri
    accent="8B3A3F",       # CORE accent (heritage, walking routes, warnings)
    market="BC6F45",       # LAND_USE commercial
    uv="8C7088",           # LAND_USE institutional (the violet of UV light)
    sun="F4C178",          # SCHEMES D5 education
    timber="AA8148",       # MASTERPLAN centre mid
    sewage="767167",       # MASTERPLAN service mid
)

ICO_GRID = 24.0
ICO_LW_UNITS = 1.5

# default (c1, c2) of every icon; None = c1 mixed toward paper
ICO_COL = {
    "water": ("water", None),
    "stream": ("water", "water_deep"),
    "stream_out": ("water", "agri"),
    "flow": ("water_deep", None),
    "depth": ("water", None),
    "high_water": ("water", "water_deep"),
    "rain": ("water_light", "water_deep"),
    "drought": ("agri", "sun"),
    "sun": ("sun", None),
    "shade": ("green_mid", "structure"),
    "reeds": ("water", "reed"),
    "plants": ("green_light", "green_mid"),
    "tree": ("green_mid", None),
    "olive": ("olive", None),
    "field": ("agri", None),
    "drip": ("water", None),
    "sewage": ("sewage", "structure"),
    "nutrients": ("water", "sewage"),
    "treatment": ("water", "structure"),
    "storage": ("water", "water_light"),
    "uv": ("water", "uv"),
    "glass": ("water", None),
    "not_drinkable": ("water", None),
    "chart": ("water_deep", "water"),
    "people": ("accent", None),
    "walk": ("accent", None),
    "bike": ("accent", None),
    "hub": ("accent", None),
    "market": ("market", None),
    "heritage": ("accent", None),
    "cafe": ("market", None),
    "seating": ("timber", None),
    "viewpoint": ("accent", None),
    "warning": ("accent", None),
    "key_area": ("accent", None),
    "key_line": ("accent", None),
    "key_dash": ("accent", None),
    "key_point": ("accent", None),
    # M9 (30 Oct): the plant-group functions of p.17 (G9) and the p.15 flood zone mark
    "flood_zone": ("water", "water_deep"),
    "wind": ("structure", None),
    "noise": ("structure", None),
    "corridor": ("green_mid", "green_light"),
}

ICO_NAMES = tuple(ICO_COL.keys())

# M9 (30 Oct): every icon's legend name (G1: no icon without its meaning). A page's legend row for an icon is
# ico_legend_entry(name) (or the Legend of label_place.py: lg.add(ico_legend_name(n), kind="icon", icon=n)).
ICO_LEGEND = {
    "water": u"Water", "stream": u"Selinos stream", "stream_out": u"Clean stream water to the fields",
    "flow": u"Flow direction", "depth": u"Water depth", "high_water": u"High water (flood level)",
    "rain": u"Rain", "drought": u"Dry season", "sun": u"Sun", "shade": u"Gives shade",
    "reeds": u"Reed basin (cleans water)", "plants": u"Planting", "tree": u"Tree", "olive": u"Olive grove",
    "field": u"Farmland", "drip": u"Drip irrigation", "sewage": u"Sewage outfall", "nutrients": u"Nutrients in the water",
    "treatment": u"Treatment works", "storage": u"Storage", "uv": u"UV disinfection", "glass": u"Drinking water",
    "not_drinkable": u"Not drinking water", "chart": u"Figures", "people": u"People", "walk": u"Walking",
    "bike": u"Cycling", "hub": u"Hub (meeting point)", "market": u"Market", "heritage": u"Heritage site",
    "cafe": u"Café", "seating": u"Seating", "viewpoint": u"Viewpoint", "warning": u"Warning",
    "key_area": u"Area", "key_line": u"Route", "key_dash": u"Path", "key_point": u"Place",
    "flood_zone": u"Flood zone", "wind": u"Cuts wind", "noise": u"Cuts street noise",
    "corridor": u"Ecological corridor",
}


def ico_legend_name(name):
    """M9: the legend name of icon `name` (every icon has one)"""
    if name not in ICO_LEGEND:
        raise ValueError("icons: %r has no legend name (ICO_LEGEND)" % (name,))
    return ICO_LEGEND[name]


def ico_legend_entry(name, label=None, **colours):
    """M9: the legend row of an icon: dict(label, kind="icon", icon=name, ...) for a page legend (label overrides the
    standard name only where the page means something narrower, e.g. "Kermes market")"""
    _ico_grid(name)                                                  # unknown names stop here
    return dict(colours, label=label or ico_legend_name(name), kind="icon", icon=name)


def ico_lw(size):
    """The one stroke weight (page mm) of an icon `size` mm square: 1.5 grid units = size / 16."""
    return size * ICO_LW_UNITS / ICO_GRID


def _ico_mix(a, b, t):
    """hex a -> hex b by t."""
    pa = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    pb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join("%02X" % int(round(pa[i] + (pb[i] - pa[i]) * t)) for i in range(3))


def _ico_arc(x, y, rx, ry, a0, a1, n=16):
    """Points on an ellipse arc from a0 to a1 degrees (both included), grid units."""
    import math as _m
    return [(x + rx * _m.cos(_m.radians(a0 + (a1 - a0) * i / float(n))),
             y + ry * _m.sin(_m.radians(a0 + (a1 - a0) * i / float(n)))) for i in range(n + 1)]


def _ico_circ(x, y, r, n=32):
    return _ico_arc(x, y, r, r, 0.0, 360.0, n)[:-1]


def _ico_ell(x, y, rx, ry, n=32):
    return _ico_arc(x, y, rx, ry, 0.0, 360.0, n)[:-1]


def _ico_rrect(x0, y0, x1, y1, r=1.5):
    """A box with the set's rounded corners (r grid units, clipped to half the short side)."""
    r = max(0.0, min(r, (x1 - x0) / 2.0, (y1 - y0) / 2.0))
    if r <= 0.0:
        return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return (_ico_arc(x1 - r, y0 + r, r, r, 270.0, 360.0, 4) + _ico_arc(x1 - r, y1 - r, r, r, 0.0, 90.0, 4)
            + _ico_arc(x0 + r, y1 - r, r, r, 90.0, 180.0, 4) + _ico_arc(x0 + r, y0 + r, r, r, 180.0, 270.0, 4))


def _ico_drop(x, yc, r, apex):
    """A water drop: round body r at (x, yc), point at (x, apex)."""
    import math as _m
    a = _m.degrees(_m.acos(r / float(apex - yc)))
    return [(x, apex)] + _ico_arc(x, yc, r, r, 90.0 + a, 450.0 - a, 24)


def _ico_leaf(b, t, w):
    """A pointed leaf from base b to tip t, w wide at its middle."""
    import math as _m
    dx, dy = t[0] - b[0], t[1] - b[1]
    L = _m.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    pts = []
    for s_ in (1, -1):
        rng = range(11) if s_ > 0 else range(10, -1, -1)
        for i in rng:
            s = i / 10.0
            o = s_ * w / 2.0 * _m.sin(_m.pi * s)
            pts.append((b[0] + dx * s + nx * o, b[1] + dy * s + ny * o))
    return pts[:-1]


def _ico_wave(x0, x1, y, amp, periods, n=24):
    import math as _m
    return [(x0 + (x1 - x0) * i / float(n), y + amp * _m.sin(2 * _m.pi * periods * i / float(n))) for i in range(n + 1)]


def _ico_union(ox, oy, circles, rect, n=72):
    """Outline of circles [(x, y, r)] united with a box (x0, y0, x1, y1) around (ox, oy), sampled by rays."""
    import math as _m
    out = []
    for i in range(n):
        a = 2 * _m.pi * i / n
        dx, dy = _m.cos(a), _m.sin(a)
        ts = []
        if abs(dx) > 1e-9:
            ts.append(((rect[2] if dx > 0 else rect[0]) - ox) / dx)
        if abs(dy) > 1e-9:
            ts.append(((rect[3] if dy > 0 else rect[1]) - oy) / dy)
        t = min(ts)
        for cx, cy, r in circles:
            px, py = ox - cx, oy - cy
            b = dx * px + dy * py
            disc = b * b - (px * px + py * py - r * r)
            if disc >= 0.0:
                t = max(t, -b + _m.sqrt(disc))
        out.append((ox + t * dx, oy + t * dy))
    return out


def _ico_arrowhead(x, y, ang, L=3.0, w=3.0):
    """A filled arrow tip at (x, y) pointing at ang degrees."""
    import math as _m
    a = _m.radians(ang)
    ux, uy = _m.cos(a), _m.sin(a)
    bx, by = x - ux * L, y - uy * L
    return [(x, y), (bx - uy * w / 2.0, by + ux * w / 2.0), (bx + uy * w / 2.0, by - ux * w / 2.0)]


def _ico_grid(name):
    """The icon in grid units with colour tokens: ("poly", ring, fill, stroke) / ("line", pts, colour)."""
    import math as _m
    P, L = "poly", "line"
    G = -8.0                                                         # the ground line of standing objects
    if name == "water":
        return [(P, _ico_drop(0.0, -3.0, 6.5, 10.0), "c1", "ink")]
    if name == "stream":
        top, bot = _ico_wave(-10.0, 10.0, 3.0, 1.2, 1.5), _ico_wave(-10.0, 10.0, -5.0, 1.2, 1.5)
        return [(P, top + bot[::-1], "c1", None), (L, top, "ink"), (L, bot, "ink"),
                (L, _ico_wave(-6.0, 6.0, -1.0, 1.0, 1.0, 16), "c2")]
    if name == "stream_out":                                         # page 18: the clean stream leaves past the fields
        return [(P, [(-10.0, 3.5), (2.0, 3.5), (2.0, 0.5), (10.0, 5.5), (2.0, 10.5), (2.0, 7.5), (-10.0, 7.5)],
                 "c1", "ink"),
                (P, [(-10.0, -9.0), (4.0, -9.0), (10.0, -2.0), (-4.0, -2.0)], "c2", "ink"),
                (L, [(-5.3, -9.0), (0.7, -2.0)], "ink"), (L, [(-0.7, -9.0), (5.3, -2.0)], "ink")]
    if name == "flow":
        return [(P, [(-10.0, -1.75), (2.0, -1.75), (2.0, -6.0), (10.0, 0.0), (2.0, 6.0), (2.0, 1.75), (-10.0, 1.75)],
                 "c1", "ink")]
    if name == "depth":                                              # a basin section with its water depth
        return [(P, [(-8.0, 1.0), (8.0, 1.0), (5.0, -8.0), (-5.0, -8.0)], "c1", None),
                (L, [(-11.0, 5.0), (-9.4, 5.0), (-5.0, -8.0), (5.0, -8.0), (9.4, 5.0), (11.0, 5.0)], "ink"),
                (L, [(0.0, -5.0), (0.0, -2.0)], "ink"), (P, _ico_arrowhead(0.0, -8.0, -90.0), "ink", None),
                (P, _ico_arrowhead(0.0, 1.0, 90.0), "ink", None)]
    if name == "high_water":
        surf = _ico_wave(-10.0, 10.0, -1.0, 0.9, 2.0)
        return [(P, surf + [(10.0, -9.0), (-10.0, -9.0)], "c1", None), (L, surf, "ink"),
                (P, [(-3.5, 6.0), (3.5, 6.0), (0.0, 0.0)], "c2", "ink"),
                (L, [(-2.5, -3.5), (2.5, -3.5)], "ink"), (L, [(-1.25, -6.0), (1.25, -6.0)], "ink"),
                (L, [(8.0, 0.5), (8.0, 6.5)], "ink"), (P, _ico_arrowhead(8.0, 10.0, 90.0, 3.5, 4.0), "ink", None)]
    if name == "rain":
        cloud = _ico_union(0.0, 0.0, [(-6.5, -0.5, 2.5), (6.5, -0.5, 2.5), (-3.0, 2.0, 3.5), (2.5, 3.0, 4.5)],
                           (-6.5, -3.0, 6.5, 2.0))
        return [(P, cloud, "c1", "ink")] + [(L, [(x, -5.5), (x - 1.5, -9.5)], "c2") for x in (-4.0, 0.5, 5.0)]
    if name == "drought":
        sh = [(P, _ico_rrect(-10.0, -9.0, 10.0, -3.0), "c1", "ink"),
              (L, [(-5.0, -3.0), (-3.8, -5.2), (-5.8, -7.0), (-4.8, -9.0)], "ink"),
              (L, [(3.5, -3.0), (2.4, -5.6), (4.4, -7.2), (3.6, -9.0)], "ink"),
              (P, _ico_circ(0.0, 4.5, 3.0), "c2", "ink")]
        return sh + [(L, _ico_arc(0.0, 4.5, 4.75, 4.75, a, a, 1)[:1] + _ico_arc(0.0, 4.5, 6.75, 6.75, a, a, 1)[:1],
                      "ink") for a in (0.0, 45.0, 90.0, 135.0, 180.0)]
    if name == "sun":
        sh = [(P, _ico_circ(0.0, 0.0, 4.5), "c1", "ink")]
        return sh + [(L, _ico_arc(0.0, 0.0, 6.5, 6.5, a, a, 1)[:1] + _ico_arc(0.0, 0.0, 9.5, 9.5, a, a, 1)[:1], "ink")
                     for a in range(0, 360, 45)]
    if name == "shade":                                              # a crown and the shadow it casts
        return [(P, _ico_ell(0.0, G - 0.5, 9.0, 1.75), "c2", None), (L, [(0.0, G), (0.0, -1.0)], "ink"),
                (P, _ico_ell(0.0, 3.5, 9.0, 5.0), "c1", "ink")]
    if name == "reeds":                                              # D2 a: common reed only in a lined, root-contained basin
        sh = [(P, [(-7.55, -3.0), (7.55, -3.0), (5.0, -9.0), (-5.0, -9.0)], "c1", None)]
        for x, h, s, ly in ((-4.0, 6.5, -1.0, -1.0), (0.0, 8.5, 1.0, 1.0), (4.0, 5.5, 1.0, -2.0)):
            sh += [(L, [(x, -6.0), (x, h - 2.0)], "c2"),
                   (P, _ico_leaf((x, ly), (x + 3.0 * s, ly + 3.5), 1.6), "c2", None),
                   (P, _ico_ell(x, h, 1.1, 2.4, 16), "c2", "ink")]
        return sh + [(L, [(-11.0, 0.5), (-8.8, 0.5), (-5.0, -9.0), (5.0, -9.0), (8.8, 0.5), (11.0, 0.5)], "ink")]
    if name == "plants":
        return [(P, _ico_leaf((-0.75, G), (-8.0, 2.0), 4.0), "c1", "ink"),
                (P, _ico_leaf((0.75, G), (8.0, 2.0), 4.0), "c1", "ink"),
                (P, _ico_leaf((0.0, G), (0.0, 8.0), 5.0), "c2", "ink"), (L, [(-10.0, G), (10.0, G)], "ink")]
    if name == "tree":
        return [(L, [(0.0, G - 1.0), (0.0, -3.0)], "ink"), (L, [(-5.0, G - 1.0), (5.0, G - 1.0)], "ink"),
                (P, _ico_circ(0.0, 3.0, 7.0), "c1", "ink")]
    if name == "olive":                                              # a forked trunk under a wide crown, three fruits
        return [(L, [(0.0, G - 1.0), (0.0, -5.0), (-3.0, -1.5)], "ink"), (L, [(0.0, -5.0), (3.0, -1.5)], "ink"),
                (L, [(-5.0, G - 1.0), (5.0, G - 1.0)], "ink"), (P, _ico_ell(0.0, 3.5, 9.5, 5.5), "c1", "ink"),
                (P, _ico_circ(-4.0, 3.0, 1.25, 12), "ink", None), (P, _ico_circ(1.0, 5.5, 1.25, 12), "ink", None),
                (P, _ico_circ(3.5, 1.5, 1.25, 12), "ink", None)]
    if name == "field":
        return [(P, [(-10.0, -6.0), (4.0, -6.0), (10.0, 6.0), (-4.0, 6.0)], "c1", "ink"),
                (L, [(-5.3, -6.0), (0.7, 6.0)], "ink"), (L, [(-0.7, -6.0), (5.3, 6.0)], "ink")]
    if name == "drip":
        sh = [(L, [(-10.0, 4.0), (10.0, 4.0)], "ink"), (L, [(-10.0, G), (10.0, G)], "ink")]
        for x in (-6.0, 0.0, 6.0):
            sh += [(P, _ico_rrect(x - 1.25, 2.75, x + 1.25, 5.25, 0.6), "ink", None),
                   (P, _ico_drop(x, -3.0, 1.75, 0.5), "c1", "ink")]
        return sh
    if name == "sewage":                                             # a pipe mouth and what falls from it
        return [(P, _ico_rrect(-10.0, 1.0, 4.0, 7.0, 0.0), "c2", "ink"),
                (P, _ico_rrect(3.5, -0.5, 6.0, 8.5), "c2", "ink"),
                (P, _ico_drop(8.0, -3.0, 2.0, 1.0), "c1", "ink"),
                (P, _ico_ell(5.0, -8.5, 5.0, 1.5), "c1", "ink")]
    if name == "nutrients":                                          # a drop with what it carries (NH4-N, P)
        return [(P, _ico_drop(0.0, -3.0, 6.5, 10.0), "c1", "ink"),
                (P, _ico_circ(-2.5, -4.5, 1.25, 12), "c2", None), (P, _ico_circ(2.0, -2.0, 1.25, 12), "c2", None),
                (P, _ico_circ(0.5, -6.5, 1.25, 12), "c2", None), (P, _ico_circ(-0.5, 1.5, 1.0, 12), "c2", None)]
    if name == "treatment":                                          # a sawtooth works hall and a round settling tank
        return [(L, [(-11.0, G), (11.0, G)], "ink"),
                (P, [(-10.0, G), (-2.0, G), (-2.0, 4.0), (-6.0, 1.5), (-6.0, 4.0), (-10.0, 1.5)], "c2", "ink"),
                (P, _ico_circ(5.5, -3.25, 4.75), "c1", "ink"), (P, _ico_circ(5.5, -3.25, 2.0, 16), None, "ink")]
    if name == "storage":                                            # a cylinder tank, filled to its level
        rx, ry, top, lev, bot = 7.0, 2.0, 5.0, -1.0, -7.0
        front = _ico_arc(0.0, bot, rx, ry, 180.0, 360.0)
        return [(P, [(-rx, top)] + front + [(rx, top)], "paper", None),
                (P, [(-rx, lev)] + front + [(rx, lev)] + _ico_arc(0.0, lev, rx, ry, 0.0, -180.0), "c1", None),
                (P, _ico_ell(0.0, lev, rx, ry), "c2", None),
                (L, [(-rx, top)] + front + [(rx, top)], "ink"),
                (P, _ico_ell(0.0, top, rx, ry), "paper", "ink")]
    if name == "uv":                                                 # a UV lamp over the water it disinfects
        sh = [(P, _ico_rrect(-10.0, -9.0, 10.0, -4.0, 0.0), "c1", None), (L, [(-10.0, -4.0), (10.0, -4.0)], "ink"),
              (P, _ico_rrect(-7.0, 2.0, 7.0, 5.5, 1.75), "c2", "ink")]
        sh += [(L, [(x, 0.0), (x * 1.25, -2.5)], "c2") for x in (-6.0, -3.0, 0.0, 3.0, 6.0)]
        return sh + [(L, [(x, 7.5), (x * 1.25, 10.0)], "c2") for x in (-4.5, 0.0, 4.5)]
    if name in ("glass", "not_drinkable"):
        return [(P, [(-5.5, 3.0), (5.5, 3.0), (4.5, -9.0), (-4.5, -9.0)], "c1", None),
                (L, [(-6.0, 9.0), (-4.5, -9.0), (4.5, -9.0), (6.0, 9.0)], "ink")]
    if name == "chart":
        return [(P, _ico_rrect(-7.0, -9.0, -3.0, 5.0, 0.0), "c1", None),
                (P, _ico_rrect(-1.0, -9.0, 3.0, -1.0, 0.0), "c2", None),
                (P, _ico_rrect(5.0, -9.0, 9.0, -5.0, 0.0), "c2", None),
                (L, [(-10.0, 9.0), (-10.0, -9.0), (10.0, -9.0)], "ink")]
    if name == "people":
        return [(P, _ico_circ(-4.0, 5.5, 2.5, 20), "ink", None), (P, _ico_rrect(-8.0, -9.0, 0.0, 2.0, 3.0), "c1", "ink"),
                (P, _ico_circ(5.0, 2.5, 2.0, 20), "ink", None), (P, _ico_rrect(2.0, -9.0, 8.0, -0.5, 2.5), "c2", "ink")]
    if name == "walk":
        return [(P, _ico_circ(1.0, 7.5, 2.25, 20), "c1", None),
                (L, [(0.5, 4.0), (-1.0, -2.0)], "c1"), (L, [(-1.0, -2.0), (-4.0, -5.0), (-5.0, -9.0)], "c1"),
                (L, [(-1.0, -2.0), (2.0, -5.5), (3.5, -9.0)], "c1"), (L, [(-4.5, -0.5), (-2.5, 2.5), (0.3, 3.2)], "c1"),
                (L, [(0.3, 3.2), (2.5, 0.5), (5.0, -0.5)], "c1")]
    if name == "bike":
        return [(P, _ico_circ(-6.0, -4.0, 4.0), None, "ink"), (P, _ico_circ(6.0, -4.0, 4.0), None, "ink"),
                (L, [(-6.0, -4.0), (-1.0, -4.0), (-3.0, 2.0), (-6.0, -4.0)], "c1"),
                (L, [(-3.0, 2.0), (4.0, 2.0), (-1.0, -4.0)], "c1"), (L, [(6.0, -4.0), (3.0, 5.0), (5.5, 5.0)], "c1"),
                (L, [(-5.0, 3.5), (-1.5, 3.5)], "c1")]
    if name == "hub":                                                # a meeting node: a disc in a ring, routes leaving it
        sh = [(P, _ico_circ(0.0, 0.0, 7.0), "c2", "ink"), (P, _ico_circ(0.0, 0.0, 3.5, 24), "c1", "ink")]
        return sh + [(L, _ico_arc(0.0, 0.0, 7.0, 7.0, a, a, 1)[:1] + _ico_arc(0.0, 0.0, 10.5, 10.5, a, a, 1)[:1], "ink")
                     for a in (45.0, 135.0, 225.0, 315.0)]
    if name == "market":                                             # a Kermes stall: striped awning, posts, counter
        sh = [(P, [(-10.0, 7.0), (0.0, 10.0), (10.0, 7.0)], "c1", "ink"),
              (L, [(-8.75, 3.0), (-8.75, G)], "ink"), (L, [(8.75, 3.0), (8.75, G)], "ink")]
        for i in range(4):
            x0 = -10.0 + 5.0 * i
            sh.append((P, [(x0, 7.0)] + _ico_arc(x0 + 2.5, 4.0, 2.5, 2.0, 180.0, 360.0, 8) + [(x0 + 5.0, 7.0)],
                       "c1" if i % 2 == 0 else "c2", "ink"))
        return sh + [(P, _ico_rrect(-10.0, G - 1.0, 10.0, -3.5), "c2", "ink")]
    if name == "heritage":                                           # a temple front
        sh = [(P, [(-10.0, 3.0), (10.0, 3.0), (0.0, 9.5)], "c1", "ink"), (P, _ico_rrect(-10.0, -9.0, 10.0, -6.0, 0.0), "c1", "ink")]
        return sh + [(P, _ico_rrect(x - 1.0, -6.0, x + 1.0, 3.0, 0.0), "c2", "ink") for x in (-6.5, -2.2, 2.2, 6.5)]
    if name == "cafe":
        steam = [(L, [(x + 0.8 * _m.sin(i * 1.05), 4.0 + i * 0.75) for i in range(8)], "ink") for x in (-3.0, 1.5)]
        return steam + [(L, _ico_arc(5.3, -2.0, 3.0, 3.0, -90.0, 90.0, 10), "ink"),
                        (P, [(-7.0, 2.0), (6.0, 2.0), (4.5, -6.5), (-5.5, -6.5)], "c1", "ink"),
                        (L, [(-9.0, -8.5), (8.0, -8.5)], "ink")]
    if name == "seating":                                            # a bench with a back
        return [(L, [(-10.0, G), (10.0, G)], "ink"), (L, [(-7.5, -1.5), (-7.5, G)], "ink"),
                (L, [(7.5, -1.5), (7.5, G)], "ink"), (L, [(-7.5, 0.5), (-7.5, 3.5)], "ink"),
                (L, [(7.5, 0.5), (7.5, 3.5)], "ink"),
                (P, _ico_rrect(-10.0, -2.0, 10.0, 0.5, 0.75), "c1", "ink"),
                (P, _ico_rrect(-10.0, 3.0, 10.0, 6.0, 0.75), "c1", "ink")]
    if name == "viewpoint":                                          # an eye
        return [(P, _ico_arc(0.0, -6.0, 11.66, 11.66, 30.96, 149.04, 16)
                 + _ico_arc(0.0, 6.0, 11.66, 11.66, 210.96, 329.04, 16), "paper", "ink"),
                (P, _ico_circ(0.0, 0.0, 3.75, 24), "c1", "ink"), (P, _ico_circ(0.0, 0.0, 1.25, 12), "ink", None)]
    if name == "warning":
        return [(P, [(-10.0, -8.0), (10.0, -8.0), (0.0, 9.32)], "c1", "c1"),
                (P, _ico_rrect(-1.0, -2.5, 1.0, 4.5, 1.0), "paper", None), (P, _ico_circ(0.0, -5.25, 1.25, 12), "paper", None)]
    if name == "key_area":
        return [(P, _ico_rrect(-9.0, -6.0, 9.0, 6.0), "c1", "ink")]
    if name == "key_line":
        return [(L, [(-10.0, 0.0), (10.0, 0.0)], "c1")]
    if name == "key_dash":
        return [(L, [(x, 0.0), (x + 4.0, 0.0)], "c1") for x in (-10.0, -2.0, 6.0)]
    if name == "key_point":
        return [(P, _ico_circ(0.0, 0.0, 4.5, 24), "c1", "ink")]
    if name == "flood_zone":                                         # a ground band under a raised wave line
        surf = _ico_wave(-10.0, 10.0, 2.0, 1.2, 2.0)
        return [(P, surf + [(10.0, -8.0), (-10.0, -8.0)], "c1", None), (L, surf, "ink"),
                (L, [(-10.0, -8.0), (10.0, -8.0)], "ink"),
                (L, _ico_wave(-7.0, 7.0, -3.0, 0.9, 1.5, 16), "c2"),
                (L, [(0.0, 5.5), (0.0, 9.5)], "ink"), (P, _ico_arrowhead(0.0, 10.5, 90.0, 3.0, 3.5), "ink", None)]
    if name == "wind":                                               # three gusts stopped by a crown
        sh = [(L, _ico_wave(-10.0, -1.0, y, 0.6, 1.0, 12), "ink") for y in (4.0, 0.0, -4.0)]
        return sh + [(P, _ico_ell(5.5, 1.0, 4.5, 7.0), "c1", "ink"), (L, [(5.5, -6.0), (5.5, -9.0)], "ink")]
    if name == "noise":                                              # sound arcs stopped by a crown
        sh = [(L, _ico_arc(-10.0, 0.0, r, r, -45.0, 45.0, 8), "ink") for r in (3.0, 6.0, 9.0)]
        return sh + [(P, _ico_ell(5.5, 1.0, 4.5, 7.0), "c1", "ink"), (L, [(5.5, -6.0), (5.5, -9.0)], "ink")]
    if name == "corridor":                                           # a green band linking two patches
        return [(P, _ico_circ(-6.5, 0.0, 3.5, 24), "c1", "ink"), (P, _ico_circ(6.5, 0.0, 3.5, 24), "c1", "ink"),
                (P, _ico_rrect(-6.5, -1.75, 6.5, 1.75, 0.0), "c2", None),
                (L, [(-3.4, 1.75), (3.4, 1.75)], "ink"), (L, [(-3.4, -1.75), (3.4, -1.75)], "ink")]
    raise ValueError("icons: unknown icon %r (see ICO_NAMES)" % (name,))


# round 4 (S2, G-R4-6): plant icons take the species' own general colour from the plant module (plants.py pla_colours,
# S3) when it is there; the ICO_PAL greens stay only as the fallback until then
ICO_PLANT_KEY = dict(olive="olive", reeds="reed")     # species icons only; generic tree / planting icons keep ICO_PAL


def _ico_plant_colour(name):
    """the general (no-season) leaf colour of an icon's species from pla_colours(key, None), or None"""
    f, key = globals().get("pla_colours"), ICO_PLANT_KEY.get(name)
    if not callable(f) or not key:
        return None
    try:
        c = f(key, None)
    except Exception:
        return None
    if isinstance(c, dict):
        c = c.get("leaf") or c.get("fill") or c.get("main")
    elif isinstance(c, (list, tuple)):
        c = c[0] if c else None
    return c if isinstance(c, str) and len(c.lstrip("#")) == 6 else None


def _ico_colours(name, ink, accent, second):
    """Token -> hex for one icon: ink, c1 (accent overrides), c2 (second overrides; None = c1 mixed to paper)."""
    d1, d2 = ICO_COL[name]
    c1 = accent or _ico_plant_colour(name) or ICO_PAL[d1]
    c2 = second or (ICO_PAL[d2] if d2 else _ico_mix(c1, ICO_PAL["paper"], 0.6))
    return dict(ink=ink or ICO_PAL["ink"], c1=c1, c2=c2, paper=ICO_PAL["paper"])


def ico_cross(cx, cy, size, colour=None, casing=True):
    """The "not allowed / not drinkable" cross over an icon: corner to corner of the live area, 1.5 x the stroke,
    on a paper casing one stroke wider."""
    u, lw = size / ICO_GRID, ico_lw(size)
    a, b = [(cx - 9.5 * u, cy - 9.5 * u), (cx + 9.5 * u, cy + 9.5 * u)], [(cx - 9.5 * u, cy + 9.5 * u), (cx + 9.5 * u, cy - 9.5 * u)]
    sh = [("line", a, ICO_PAL["paper"], 2.5 * lw), ("line", b, ICO_PAL["paper"], 2.5 * lw)] if casing else []
    return sh + [("line", a, colour or ICO_PAL["accent"], 1.5 * lw), ("line", b, colour or ICO_PAL["accent"], 1.5 * lw)]


def ico_draw(name, cx, cy, size, ink=None, accent=None, second=None):
    """Icon `name` (ICO_NAMES) centred at (cx, cy), size mm square: shapes. accent recolours c1, second c2."""
    u, lw = size / ICO_GRID, ico_lw(size)
    grid = _ico_grid(name)                                           # unknown names stop here
    col = _ico_colours(name, ink, accent, second)
    out = []
    for s in grid:
        if s[0] == "poly":
            ring = [(cx + x * u, cy + y * u) for x, y in s[1]]
            out.append(("poly", ring, col.get(s[2]) if s[2] else None, col.get(s[3]) if s[3] else None, lw))
        else:
            out.append(("line", [(cx + x * u, cy + y * u) for x, y in s[1]], col.get(s[2], s[2]), lw))
    if name == "not_drinkable":
        out += ico_cross(cx, cy, size)
    return out


def ico_badge(name, cx, cy, size, frame="circle", fill=None, edge=None, ink=None, accent=None, second=None):
    """Icon `name` on a round ("circle") or rounded-square ("square") plate size mm across, for legends: the icon at
    0.72 of the plate; plate in paper unless fill, with an edge line (one stroke of the plate size) only if edge."""
    lw = ico_lw(size)
    if frame == "square":
        h = size / 2.0 - lw / 2.0
        r = size * 3.0 / ICO_GRID
        ring = [(cx + x, cy + y) for x, y in _ico_rrect(-h, -h, h, h, r)]
    else:
        ring = [(cx + x, cy + y) for x, y in _ico_circ(0.0, 0.0, size / 2.0 - lw / 2.0, 40)]
    plate = ("poly", ring, fill or ICO_PAL["paper"], edge, lw if edge else 0.0)
    return [plate] + ico_draw(name, cx, cy, size * 0.72, ink, accent, second)


def ico_step(cx, cy, size, style="solid", colour=None, ink=None):
    """A numbered flow-step marker (page 18, steps 1-7) size mm across: (shapes, (ax, ay), text_hex, cap_mm).
    The caller writes the number centred on (ax, ay) in text_hex at cap height cap_mm (0.42 x size)."""
    lw = ico_lw(size)
    c = colour or ICO_PAL["water_deep"]
    ring = [(cx + x, cy + y) for x, y in _ico_circ(0.0, 0.0, size / 2.0 - lw / 2.0, 40)]
    if style == "ring":
        return [("poly", ring, ICO_PAL["paper"], c, lw)], (cx, cy), (ink or ICO_PAL["ink"]), 0.42 * size
    return [("poly", ring, c, None, lw)], (cx, cy), ICO_PAL["paper"], 0.42 * size
# ---- M1 (revision 30 Oct 2026, H-A): ONE booklet grid and ONE set of type styles for every page ----------------------
# Page mm, A3 landscape 420 x 297, origin top-left, y DOWN (the booklet's own system). A script that draws y-up calls
# grid_flip(y) / grid_rect_up(r) for its coordinates. Every block of a page (map, section, legend, intro, key map, box)
# is placed by grid cells: a column span (c0, n) and baseline rows, never by hand-tuned mm.
#   columns   12 x 29 mm, gutters 4 mm, margins 14 mm left/right: 14 + 12 x 29 + 11 x 4 + 14 = 420
#   rows      baseline 4 mm from y = 12 (the top margin); title band 12..25, drawing area 30..273, footer from 276
#   crops     a crop the booklet shows at 1:1 is drawn GRID_W(n) wide (n whole columns), so its own sub-blocks fall on
#             the page grid when the booklet places it on a column line (grid_sub gives that sub-grid inside a crop)
# Type: GRID_TYPE (pt, bold, lead mm, colour role). Intro helper: "*word*" (or "**word**") marks the bold key words.
GRID_PAGE = (420.0, 297.0)
GRID_ML, GRID_MR, GRID_MT, GRID_MB = 14.0, 14.0, 12.0, 12.0
GRID_COLS, GRID_COL, GRID_GUT = 12, 29.0, 4.0
GRID_BASE = 4.0                                   # baseline step, from y = GRID_MT
GRID_TITLE_Y, GRID_RULE_Y = 22.0, 25.0            # title baseline, the rule under the title band
GRID_AREA = (GRID_ML, 30.0, GRID_PAGE[0] - GRID_MR, 273.0)   # where drawings go (x0, y0, x1, y1)
GRID_FOOT_RULE = 276.0
GRID_MIN_PT = 4.0                                 # no text below this size on any page, measured AFTER scaling
                                                  # (round 5 D1, Aras 1 Nov 21:26: 4 pt floor; was 6.0)
# round 5 (S1; PLAN §3 "Fonts and sizes", D1): the STARTING size of every text role the booklet composer sets (pt,
# bold, lead as a multiple of the size, colour role). The composer may step a text down to GRID_MIN_PT, never below.
# Content scripts put these sizes on their exported text items (common/item_export.py takes them from here).
GRID_ROLE_PT = dict(
    title=(16.0, True, 1.15, "ink"),              # the page title
    heading=(7.0, True, 1.25, "ink"),             # a drawing's heading
    intro=(6.0, False, 1.3, "ink"),               # the page intro / a short text block
    caption=(5.0, False, 1.3, "ink2"),            # under a drawing: what, scale
    legend=(5.0, False, 1.3, "ink"),              # legend entries
    list_item=(5.0, False, 1.3, "ink"),           # numbered / bulleted list rows
    note=(5.0, False, 1.3, "ink2"),
    source=(5.0, False, 1.3, "ink2"),
    label=(4.5, False, 1.2, "ink"),               # in-drawing labels (place names, element names)
    badge=(4.5, True, 1.2, "ink"),                # number badges on a drawing
    level_value=(4.5, False, 1.2, "ink"),         # "+43.71" beside a level marker
    pageno=(7.0, True, 1.2, "accent"),            # the page number
)

# colour roles (palette v1.4 core): ink, second ink, accent, rule
GRID_INK = dict(ink="4A3F35", ink2="6B645B", accent="8B3A3F", rule="B0AC9C", paper="FFFFFF")
# style -> (size pt, bold, lead mm, colour role)
GRID_TYPE = dict(
    page_title=(24.0, True, 10.0, "ink"),         # the page's title (booklet header)
    kicker=(8.0, True, 3.6, "accent"),            # the theme line above the title
    intro=(9.5, False, 4.0, "ink"),               # 2-3 lines, key words bold (G4)
    heading=(10.0, True, 4.0, "ink"),             # a drawing's own heading ("Pedestrian flow")
    subheading=(8.0, True, 3.6, "ink2"),
    label=(7.0, False, 3.0, "ink"),               # labels on drawings
    label_small=(6.0, False, 2.6, "ink"),         # the smallest a label may get (crowded maps)
    legend=(7.0, False, 4.0, "ink"),              # legend entries (row pitch = lead)
    legend_title=(7.0, True, 4.0, "ink"),
    caption=(7.5, False, 3.2, "ink2"),            # under a drawing: what, scale
    value=(18.0, True, 7.0, "accent"),            # a box's one headline value (G4)
    note=(7.5, False, 3.2, "ink2"),               # the one line under a value
    pageno=(14.0, True, 6.0, "accent"),
)
GRID_PT = 25.4 / 72.0                             # mm per pt


def grid_role(role):
    """(size_pt, bold, lead_mm_per_pt, hex) of a round 5 text role (GRID_ROLE_PT); unknown roles = 'note'"""
    s, b, ld, c = GRID_ROLE_PT.get(role, GRID_ROLE_PT["note"])
    return s, b, ld, GRID_INK[c]


def _grid_warn(msg):
    """round 5: a grid misfit is a WARNING line + orange message, never a stop (common/warn.py when included)"""
    g_ = globals()
    if "wn_warn" in g_:
        g_["wn_warn"](None, "grid", msg)
    elif "tp_warn" in g_:
        g_["tp_warn"](u"grid: " + msg)
    else:
        print(u"WARNING grid: " + msg)


def grid_style(name):
    """(size_pt, bold, lead_mm, hex) of a type style (GRID_TYPE)"""
    s, b, ld, role = GRID_TYPE[name]
    return s, b, ld, GRID_INK[role]


def grid_w(n):
    """width (mm) of n whole columns with their inner gutters"""
    n = max(1, int(n))
    return n * GRID_COL + (n - 1) * GRID_GUT


def grid_x(c):
    """left edge (mm) of column c (1-based; c = GRID_COLS + 1 gives the right margin line)"""
    return GRID_ML + (c - 1) * (GRID_COL + GRID_GUT)


def grid_x1(c):
    """right edge (mm) of column c"""
    return grid_x(c) + GRID_COL


def grid_span(c0, n):
    """(x, w) of the span of n columns from column c0"""
    if c0 < 1 or c0 + n - 1 > GRID_COLS:              # round 5: a WARNING, the span is kept on the grid
        _grid_warn("span %d+%d is off the %d-column grid: clamped" % (c0, n, GRID_COLS))
        c0 = min(max(1, int(c0)), GRID_COLS)
        n = max(1, min(int(n), GRID_COLS - c0 + 1))
    return grid_x(c0), grid_w(n)


def grid_cols_for(w, lo=1):
    """the fewest whole columns (>= lo) at least w mm wide (GRID_COLS when w is wider than the page)"""
    for n in range(max(1, lo), GRID_COLS + 1):
        if grid_w(n) >= w - 1e-6:
            return n
    return GRID_COLS


def grid_snap_y(y, up=True):
    """y (mm from the top) on the baseline grid: the next line at or below the point (up=True gives the line at or
    above it)"""
    import math as _m
    k = (y - GRID_MT) / GRID_BASE
    k = _m.floor(k + 1e-6) if up else _m.ceil(k - 1e-6)
    return GRID_MT + k * GRID_BASE


def grid_snap_h(h):
    """a height rounded UP to whole baseline steps"""
    import math as _m
    return GRID_BASE * _m.ceil(h / GRID_BASE - 1e-6)


def grid_rows(n):
    """the height of n baseline rows"""
    return n * GRID_BASE


def grid_cell(c0, n, y, h, snap=True):
    """the block rect (x0, y0, x1, y1) of n columns from c0, top y, height h; snap: top on the baseline (next line
    down) and the height to whole steps"""
    x, w = grid_span(c0, n)
    if snap:
        y, h = grid_snap_y(y, up=False), grid_snap_h(h)
    return (x, y, x + w, y + h)


def grid_stack(heights, c0, n, y0=None, gap=GRID_BASE):
    """blocks of the given heights stacked down one column span from y0 (default the drawing area's top), each on the
    baseline: [rect]; a stack that runs past the drawing area is a WARNING (round 5; the composer's layout check
    reports the edge hit too)"""
    y = GRID_AREA[1] if y0 is None else grid_snap_y(y0, up=False)
    out = []
    for h in heights:
        r = grid_cell(c0, n, y, h)
        out.append(r)
        y = r[3] + gap
    if out and out[-1][3] > GRID_AREA[3] + 1e-6:
        _grid_warn("stack runs %.1f mm past the drawing area" % (out[-1][3] - GRID_AREA[3]))
    return out


def grid_row(widths_cols, y, h, c0=1):
    """blocks side by side on one baseline row: widths_cols = [n columns each] from column c0: [rect]"""
    out, c = [], c0
    for n in widths_cols:
        out.append(grid_cell(c, n, y, h))
        c += n
    if c - 1 > GRID_COLS:
        _grid_warn("row needs %d columns, the grid has %d" % (c - 1, GRID_COLS))
    return out


def grid_sub(width_mm, n=None):
    """the sub-grid INSIDE a crop of width_mm (drawn to be shown at 1:1 on the page): [(x0, x1)] of its columns from
    the crop's left edge; n defaults to the whole page columns the width holds"""
    n = n or max(1, int(round((width_mm + GRID_GUT) / (GRID_COL + GRID_GUT))))
    col = (width_mm - (n - 1) * GRID_GUT) / float(n)
    return [(i * (col + GRID_GUT), i * (col + GRID_GUT) + col) for i in range(n)]


def grid_flip(y, page_h=None):
    """a top-down y (mm) as y-up (or back): page_h - y"""
    return (page_h or GRID_PAGE[1]) - y


def grid_rect_up(r, page_h=None):
    """a top-down rect (x0, y0, x1, y1) as a y-up rect (x0, y0, x1, y1) with y0 < y1"""
    H = page_h or GRID_PAGE[1]
    return (r[0], H - r[3], r[2], H - r[1])


def grid_page_counter(n, total=None):
    """the page number, bottom right: the current page only, "17" (round 3, G2 / U20: no "NN/total"; total is
    accepted and ignored so older callers keep working)"""
    return "%d" % int(n)


# ------------------------------------------------------------------------------------------- intro with bold runs
def grid_marked_runs(text):
    """marked text -> runs [(s, bold)]: "*word*" or "**words**" are bold key words, the rest regular. An unpaired
    star is printed as it is."""
    import re as _re
    out = []
    pos = 0
    for m in _re.finditer(r"\*\*(.+?)\*\*|\*(?!\s)([^*]+?)\*", text):
        if m.start() > pos:
            out.append((text[pos:m.start()], False))
        out.append((m.group(1) if m.group(1) is not None else m.group(2), True))
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], False))
    return [(s, b) for s, b in out if s]


def grid_plain(text):
    """marked text without its marks (for measuring or logging)"""
    return "".join(s for s, _ in grid_marked_runs(text))


def grid_wrap_runs(runs, width_mm, size_pt, measure):
    """runs wrapped to width_mm: lines of [(s, bold, x_offset_mm)]. measure(s, size_pt, bold) -> mm. Words keep their
    own weight; a bold run is never split from its following punctuation."""
    words = []                                    # [word, bold, space_before]
    sp_next = False
    for s, b in runs:
        for ch in s:
            if ch.isspace():
                sp_next = True
            elif words and not sp_next and words[-1][1] == b:
                words[-1][0] += ch
            else:
                words.append([ch, b, bool(words) and sp_next])
                sp_next = False
    lines, cur, x = [], [], 0.0
    for w, b, sp in words:
        gap = measure(" ", size_pt, False) if (sp and cur) else 0.0
        ww = measure(w, size_pt, b)
        if cur and x + gap + ww > width_mm + 1e-6 and sp:
            lines.append(cur)
            cur, x, gap = [], 0.0, 0.0
        if cur and not sp:                       # glued (e.g. "word," after a bold run): no space
            gap = 0.0
        cur.append((w, b, x + gap))
        x += gap + ww
    if cur:
        lines.append(cur)
    out = []                                      # merge neighbouring words of one weight into one run
    for ln in lines:
        m = []
        for w, b, xo in ln:
            if m and m[-1][1] == b:
                m[-1] = (m[-1][0] + (" " if xo > m[-1][3] + 1e-6 else "") + w, b, m[-1][2], xo + measure(w, size_pt, b))
            else:
                m.append((w, b, xo, xo + measure(w, size_pt, b)))
        out.append([(s, b, xo) for s, b, xo, _ in m])
    return out


def grid_intro(text, width_mm, measure, max_lines=3, style="intro", min_pt=8.0, log=None):
    """the page intro (G4: 2-3 lines, key words bold): marked text -> (lines, size_pt, lead_mm, hex). lines =
    [[(s, bold, x_offset_mm)]]. The size steps down by 0.5 pt (not below min_pt) until it fits max_lines; text that
    still does not fit keeps its lines and a WARNING goes to log (shorten it: the rule is 3 lines)."""
    size, _, lead, col = grid_style(style)
    runs = grid_marked_runs(text)
    s = size
    while True:
        lines = grid_wrap_runs(runs, width_mm, s, measure)
        if len(lines) <= max_lines or s - 0.5 < min_pt - 1e-6:
            break
        s -= 0.5
    if len(lines) > max_lines and log is not None:
        log.append(u"WARNING: intro longer than %d lines at %.1f pt (%d lines): %s" % (
            max_lines, s, len(lines), grid_plain(text)[:60]))
    return lines, s, lead * s / size, col


def grid_text_runs(lines, x, y, lead, y_down=True):
    """intro lines placed: [(s, x_mm, baseline_y_mm, bold)] from the first baseline (x, y); y_down=False for y-up
    pages (lines go to smaller y)"""
    out = []
    for i, ln in enumerate(lines):
        yy = y + i * lead if y_down else y - i * lead
        for s, b, xo in ln:
            out.append((s, x + xo, yy, b))
    return out
# ---- text_place.py (round 4, S1, 1 Nov 2026; G-R4-1, G-R4-2, PLAN §4.1): ONE text placer (round 5: hits WARN) ----
# Replaces label_place.py (its lp_* names stay as shims there until the closing step, see label_place.py).
# Every printed letter of a page goes through ONE TextPage: it measures with the real font (font_metrics.py), keeps
# every box, draws everything in .emit(drawer) (no other text path), and .check() reports (round 5: WARNING lines) any
# two texts, a text and an obstacle, a text and the page edge / margins / footer zone, or two drawing blocks overlap.
# Needs, included before it: pdf_fonts.py, font_metrics.py, grid.py (GRID_MIN_PT, grid_marked_runs); warn.py optional
# (round 5: the one warning sink; without it tp_warn writes its WARNING line itself).
#
#   tp = TextPage(name, bounds, y_down=True, min_pt=None, pad=0.6, margins=None, footer_zone=None, scale=1.0,
#                 unit_mm=1.0, log=None)
#       name        the round 4 BOOKLET page id ("p13a", "p15"), used in every log line and error
#       bounds      (x0, y0, x1, y1) of the sheet / crop in page units; no text outside it (minus margins)
#       y_down      True when page y grows downward (the booklet grid), False for y-up sheets
#       min_pt      smallest PRINTED size (default GRID_MIN_PT = 6.0): pt x scale must reach it, else TextError
#       pad         clear gap (mm) every text keeps from other texts and obstacles
#       margins     (left, top, right, bottom) mm kept free inside bounds ("top" = the visual top)
#       footer_zone (x0, y0, x1, y1) page units where only role="footer" text may sit
#       scale       print factor of this sheet in the booklet (printed mm / sheet mm), for the min_pt test
#       unit_mm     mm per page unit (1.0 for mm sheets; the site board's board units differ)
#       log         a list for the log lines (default TP_LOG; tp_log_lines() empties it)
#   tp.keep(geom, kind="keep", name=None, line=None)   an obstacle no text may touch: a box (x0, y0, x1, y1), a closed
#                                                     area [(x, y) ...] or, with line=True (or kind in TP_LINE_KINDS),
#                                                     an open polyline (streets, banks, cut lines)
#   tp.block(box, name)                               a drawing block (map, section, key map, legend): blocks may touch,
#                                                     never overlap
#   tp.put(text, x, y, pt, bold=False, align="L", angle=0, name=None, role="label", colour=None, allow=(),
#          group=None, emit=True, **extra) -> box     one fixed text (title, caption, footer, scale figure, legend row);
#                                                     (x, y) = the baseline point at `align` (L / C / R; "MC" = the
#                                                     middle of the ink); angle degrees, counter-clockwise on the page;
#                                                     allow = names / kinds of keeps this text may sit on (a number
#                                                     on its own marker disc); emit=False registers text another
#                                                     writer draws (the booklet's crop text)
#   tp.para(text, x, y, w, pt, lead, bold_marks=True, name=None, bold=False, colour=None, role="para",
#           max_lines=None, min_last_words=2, allow=()) -> next baseline
#                                                     wraps with tp_wrap (real widths; "*word*" / "**word**" bold;
#                                                     "\n" breaks; last line >= 2 words, else 0.25 pt smaller once if
#                                                     that stays >= min_pt, else TextError); each run is placed at its
#                                                     measured x, so "Ulucami Önü" + " walking hub" keep their space
#   tp.place(text, anchor, positions=TP_POSITIONS, alts=(), pt=7.0, rank=0, side_list=None, bold=False,
#            colour=None, name=None, r=0.0, gap=0.8, allow=(), role="label") -> item dict
#                                                     a label beside its point: positions in reading order (E, NE, N,
#                                                     NW, W, SW, S, SE, C, or (dx, dy, align) in page units), then the
#                                                     shorter alts, then a NUMBER on the point + a row in side_list;
#                                                     never below min_pt, never dropped (round 5 order: see below;
#                                                     rings=TP_RINGS, step=0.5 pt). rank orders nothing here (callers
#                                                     place rank 0 first); kept for the interface
#   tp.check(raise_=True, log=None, blocks_in=False) -> n_items
#                                                     the collision test; one "WARNING <page> overlap|edge: ..." line
#                                                     per hit, then "overlap <page> checked n, collisions k"; raises
#                                                     only with TP_WARN_ONLY = [False]; tp.hits = [(kind, a, b)]
#   tp.hits_now(blocks_in=False) -> [(kind, a, b)]   v32: check()'s hits, silent (no log, no message)
#   tp.unput(item) -> bool                            v32: a registered text taken off again (to be placed anew)
#   tp.emit(drawer) -> n                              drawer(item) for every text in order; item = dict(text, x, y,
#                                                     pt, size_mm, bold, align, angle, colour, role, name, extra)
#   tp.export() -> dict                               boxes in mm, y DOWN from the bounds' top-left (crop-local) for
#                                                     the booklet (BkBlocks.crop(..., text_boxes, keep))
#   TpSideList(name, row_mm=8.0)                      the numbered key rows of place(); .close(tp) numbers them in
#                                                     reading order (top row first, left to right); .rows() ->
#                                                     [(n, text)]; check() raises while a side list is open
#   tp_wrap(text, w_mm, pt, bold=False, min_last_words=2, bold_marks=True) -> [[(s, bold, x_mm)]]
#   tp_shapes(shapes, tp, name=None, allow=(), y_down=None) -> the other shapes
#                                                     registers the ("text", ...) shapes of the common modules
#                                                     (section_frame, water, basemap, figures, buildings, node, para,
#                                                     xform) in tp, which then draws them; returns the non-text shapes
#                                                     for the caller to draw as before
# Geometry helpers (moved here from label_place.py): tp_hit, tp_seg_box, tp_seg_cross, TpSegIndex, tp_reading_order.
#
# ROUND 5 (S1, 1 Nov 2026; G-R5-1, G-R5-12, C11; PLAN §3 "Warnings"): nothing here stops a run on a layout hit.
#   * tp_warn goes to common/warn.py (wn_warn) when it is included, so every hit is ONE "WARNING <page> <kind>: ..."
#     line in TP_LOG plus an orange message; kinds: overlap, edge, min_text, widow, wrap, side_list, number.
#   * check() writes one WARNING line per hit whatever raise_ says (C11: raise_=False used to log only the count, so
#     "collisions 1" and "0 warnings" could both appear); it raises only when TP_WARN_ONLY = [False] and raise_.
#     check(blocks_in=True) also tests every block against the inner bounds (the booklet composer's edge test).
#   * place() order (G-R5-12 "prevent, not just detect"): its positions, then nearby free spots on rings round the
#     anchor (TP_RINGS mm), then the shorter alts the same way, then the side list number, then smaller sizes in
#     0.5 pt steps down to min_pt; only when all fail: a WARNING and the label at its first position (never dropped).
#   * para(): a widow that 0.25 pt smaller cannot fix is a WARNING and the paragraph is set without the widow rule.
#   * emit(): a "0" number whose side list was never closed is a WARNING and is not drawn; export() checks first.
TP_LOG = WN_LOG if "WN_LOG" in globals() else []   # round 5: with warn.py included, ONE list (the warning sink)
TP_PT = 25.4 / 72.0
TP_ROW_MM = 8.0                 # reading order: anchors within this many mm of height count as one row
TP_POSITIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
TP_LINE_KINDS = ("line", "edge", "street", "road", "cut", "stream", "bank", "contour", "leader")
TP_RINGS = (1.5, 3.0, 4.5, 6.0)  # round 5: mm from the anchor's own positions where place() looks for a free spot
TP_RING_STEPS = 12               # spots per ring (every 30 degrees, starting east, counter-clockwise on the page)


class TextError(RuntimeError):
    pass


TP_WARN_ONLY = [True]   # 1 Nov (Aras): check() writes hits as warnings instead of raising; [False] = raise


def tp_warn(msg, log=None):
    """1 Nov (Aras 19:33 "get this already"): a layout check that used to stop the run writes "WARNING <msg>" to
    TP_LOG (or log) and an orange Grasshopper warning, and the run goes on (TP_WARN_ONLY = [False] raises TextError
    again). Round 5: through common/warn.py when it is included (one sink, capped orange messages)."""
    if not TP_WARN_ONLY[0]:
        raise TextError(msg)
    lg = TP_LOG if log is None else log
    if "wn_warn" in globals():
        wn_warn(None, None, msg, lg)
        return
    lg.append(u"WARNING " + msg)
    try:
        ghenv.Component.AddRuntimeMessage(__import__("Grasshopper").Kernel.GH_RuntimeMessageLevel.Warning, msg)
    except Exception:
        pass


class TextCollision(TextError):
    def __init__(self, page, item, other, n=1, more=()):
        self.page, self.item, self.other, self.n, self.more = page, item, other, n, list(more)
        msg = u"text collision on %s: %s against %s" % (page, _tp_desc(item), _tp_desc(other))
        if n > 1:
            msg += u" (and %d more: %s)" % (n - 1, u"; ".join(u"%s / %s" % (_tp_desc(a), _tp_desc(b))
                                                               for a, b in self.more[:4]))
        RuntimeError.__init__(self, msg)


def _tp_desc(it):
    if it is None:
        return u"-"
    if isinstance(it, str):
        return it
    if isinstance(it, dict):
        if "text" in it:
            return u"text %r%s" % (it["text"][:40], (u" (%s)" % it["name"]) if it.get("name") else u"")
        return u"%s %s" % (it.get("kind", "obstacle"), it.get("name") or u"")
    return u"%r" % (it,)


def tp_log_lines():
    """this run's text log lines, oldest first; the list is emptied"""
    out = list(TP_LOG)
    del TP_LOG[:]
    return out


# ------------------------------------------------------------------------------------------------ geometry
def tp_hit(a, b, pad=0.0):
    """True when boxes a and b (x0, y0, x1, y1) come closer than pad"""
    return a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad


def tp_seg_box(p, q, b):
    """True when the segment p-q passes through box b (Liang-Barsky)"""
    x0, y0 = p
    dx, dy = q[0] - x0, q[1] - y0
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, x0 - b[0]), (dx, b[2] - x0), (-dy, y0 - b[1]), (dy, b[3] - y0)):
        if pp == 0:
            if qq < 0:
                return False
        else:
            t = qq / pp
            if pp < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


def tp_seg_cross(p, q, r, s):
    """True when segments p-q and r-s cross (touching at a shared end point does not count)"""
    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    for a in (p, q):
        for b in (r, s):
            if abs(a[0] - b[0]) < 1e-9 and abs(a[1] - b[1]) < 1e-9:
                return False
    d1, d2, d3, d4 = orient(r, s, p), orient(r, s, q), orient(p, q, r), orient(p, q, s)
    return d1 * d2 < 0 and d3 * d4 < 0


class TpSegIndex(object):
    """linework in buckets, so a box tests only the segments near it"""
    def __init__(self, polylines=(), segs=(), cell=10.0):
        self.cell, self.b = float(cell), {}
        for P in polylines:
            for a, c in zip(P, P[1:]):
                self.add(a, c)
        for a, c in segs:
            self.add(a, c)

    def add(self, a, c):
        k = self.cell
        for i in range(int(min(a[0], c[0]) // k), int(max(a[0], c[0]) // k) + 1):
            for j in range(int(min(a[1], c[1]) // k), int(max(a[1], c[1]) // k) + 1):
                self.b.setdefault((i, j), []).append((a, c))

    def near(self, box):
        k, seen, out = self.cell, set(), []
        for i in range(int(box[0] // k), int(box[2] // k) + 1):
            for j in range(int(box[1] // k), int(box[3] // k) + 1):
                for sg in self.b.get((i, j), ()):
                    if id(sg) not in seen:
                        seen.add(id(sg))
                        out.append(sg)
        return out

    def __iter__(self):
        seen = set()
        for lst in self.b.values():
            for sg in lst:
                if id(sg) not in seen:
                    seen.add(id(sg))
                    yield sg


def tp_reading_order(pts, y_down=False, row_mm=TP_ROW_MM):
    """the indexes of pts [(x, y)] in reading order: rows from the visual top down (rows row_mm high), left to right"""
    import math as _m
    if not pts:
        return []
    top = min(p[1] for p in pts) if y_down else max(p[1] for p in pts)
    row = (lambda p: int(_m.floor((p[1] - top) / row_mm))) if y_down else \
        (lambda p: int(_m.floor((top - p[1]) / row_mm)))
    return sorted(range(len(pts)), key=lambda i: (row(pts[i]), pts[i][0], i))


def _tp_in_poly(pt, P):
    x, y = pt
    inside = False
    n = len(P)
    for i in range(n):
        (x1, y1), (x2, y2) = P[i], P[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / ((y2 - y1) or 1e-12) + x1:
            inside = not inside
    return inside


def _tp_keep_hits(b, K, pad):
    """True when box b comes within pad of the obstacle K"""
    if not tp_hit(b, K["box"], pad):
        return False
    if K["pts"] is None:
        return True
    bb = (b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad)
    for p, q in K["segs"].near(bb):
        if tp_seg_box(p, q, bb):
            return True
    if K["line"]:
        return False
    return _tp_in_poly(((bb[0] + bb[2]) / 2.0, (bb[1] + bb[3]) / 2.0), K["pts"]) or \
        _tp_in_poly(K["pts"][0], [(bb[0], bb[1]), (bb[2], bb[1]), (bb[2], bb[3]), (bb[0], bb[3])])


# ------------------------------------------------------------------------------------------------ wrapping
def _tp_units(text, bold, bold_marks):
    """the text as word units (each a list of (s, bold) pieces glued without a space); None marks a forced break"""
    runs = grid_marked_runs(text) if (bold_marks and "grid_marked_runs" in globals()) else [(text, False)]
    units, cur = [], None
    for s, b in runs:
        b = bool(b or bold)
        for ch in s:
            if ch == "\n":
                if cur:
                    units.append(cur)
                units.append(None)
                cur = None
            elif ch.isspace():
                if cur:
                    units.append(cur)
                cur = None
            elif cur is not None and cur[-1][1] == b:
                cur[-1] = (cur[-1][0] + ch, b)
            elif cur is not None:
                cur.append((ch, b))
            else:
                cur = [(ch, b)]
    if cur:
        units.append(cur)
    return units


class TpWidow(TextError):
    pass


def tp_wrap(text, w_mm, pt, bold=False, min_last_words=2, bold_marks=True):
    """text wrapped to w_mm with real widths: lines of [(s, bold, x_offset_mm)] (neighbouring words of one weight
    merged into one run). "\\n" forces a break. A word wider than w_mm raises TextError. The last line of every
    wrapped paragraph holds at least min_last_words words (words are pulled down from the line before); when that
    cannot be done, TpWidow is raised (TextPage.para then tries 0.25 pt smaller)."""
    sp_w = fm_width(u" ", pt, False)

    def uw(u):
        return sum(fm_width(s, pt, b) for s, b in u)
    paras, cur = [], []
    for u in _tp_units(text, bold, bold_marks):
        if u is None:
            paras.append(cur)
            cur = []
        else:
            cur.append(u)
    paras.append(cur)
    out = []
    for words in paras:
        if not words:
            out.append([])
            continue
        lines, ln, x = [], [], 0.0
        for u in words:
            w = uw(u)
            if w > w_mm + 1e-6:
                tp_warn(u"wrap: the word %r (%.1f mm at %.1f pt) is wider than its column (%.1f mm): it runs over" % (
                    u"".join(s for s, _ in u), w, pt, w_mm))
            if ln and x + sp_w + w > w_mm + 1e-6:
                lines.append(ln)
                ln, x = [], 0.0
            x += (sp_w if ln else 0.0) + w
            ln.append(u)
        lines.append(ln)
        if len(lines) >= 2 and min_last_words > 1:
            while len(lines[-1]) < min_last_words:
                prev = lines[-2]
                if len(prev) <= 2:
                    raise TpWidow(u"last line %r would hold fewer than %d words" % (
                        u"".join(s for s, _ in lines[-1][0]), min_last_words))
                mv = prev.pop()
                lines[-1].insert(0, mv)
                if sum(uw(u) for u in lines[-1]) + sp_w * (len(lines[-1]) - 1) > w_mm + 1e-6:
                    raise TpWidow(u"last line cannot take one more word without passing the column width")
        for ln in lines:
            row, x = [], 0.0                       # row: [text, bold, x_offset]; one run per stretch of one weight
            for i, u in enumerate(ln):
                for j, (s, b) in enumerate(u):
                    gap = (i > 0 and j == 0)
                    if row and row[-1][1] == b:
                        row[-1][0] += (u" " if gap else u"") + s
                    else:
                        row.append([s, b, x + (sp_w if gap else 0.0)])
                    x += (sp_w if gap else 0.0) + fm_width(s, pt, b)
            out.append([(s, b, xo) for s, b, xo in row])
    return out


# ------------------------------------------------------------------------------------------------ the page
class TpSideList(object):
    """the numbered key of place(): rows numbered in reading order when closed"""
    def __init__(self, name, row_mm=TP_ROW_MM):
        self.name, self.row_mm, self.entries, self.closed = name, row_mm, [], False

    def add(self, anchor, text, item):
        if self.closed:
            tp_warn(u"side_list: %s is closed: %r gets no number (place its labels before close())" % (
                self.name, u"%s" % text))
        e = dict(anchor=tuple(anchor), text=text, item=item, n=None)
        self.entries.append(e)
        return e

    def close(self, tp):
        """numbers the entries in reading order and re-measures their number boxes"""
        order = tp_reading_order([e["anchor"] for e in self.entries], tp.y_down, self.row_mm / tp.unit_mm)
        for n, j in enumerate(order, 1):
            e = self.entries[j]
            e["n"] = n
            it = e["item"]
            it["text"] = u"%d" % n
            it["box"] = tp._box(it["text"], it["x"], it["y"], it["pt"], it["bold"], it["align"], it["angle"])
        self.closed = True
        return self.rows()

    def rows(self):
        return [(e["n"], e["text"]) for e in sorted(self.entries, key=lambda e: e["n"] or 0)]


class TextPage(object):
    def __init__(self, name, bounds, y_down=True, min_pt=None, pad=0.6, margins=None, footer_zone=None, scale=1.0,
                 unit_mm=1.0, log=None):
        if not bounds or len(bounds) != 4 or bounds[2] <= bounds[0] or bounds[3] <= bounds[1]:
            raise TextError(u"TextPage %s: bounds must be (x0, y0, x1, y1)" % name)
        self.name, self.bounds, self.y_down = name, tuple(float(v) for v in bounds), bool(y_down)
        self.min_pt = float(GRID_MIN_PT if min_pt is None else min_pt)
        self.unit_mm, self.scale = float(unit_mm), float(scale)
        self.pad = pad / self.unit_mm
        m = [v / self.unit_mm for v in (margins or (0.0, 0.0, 0.0, 0.0))]
        b = self.bounds
        if self.y_down:
            self.inner = (b[0] + m[0], b[1] + m[1], b[2] - m[2], b[3] - m[3])
        else:
            self.inner = (b[0] + m[0], b[1] + m[3], b[2] - m[2], b[3] - m[1])
        self.footer_zone = tuple(footer_zone) if footer_zone else None
        self.log = log
        self.items, self.keeps, self.blocks, self.sides = [], [], [], []
        self._gid, self.checked = 0, False
        self.hits = []

    # -- measuring
    def _box(self, text, x, y, pt, bold=False, align="L", angle=0.0):
        b = fm_box(text, 0.0, 0.0, pt, bold, align, angle, self.y_down)
        u = self.unit_mm
        return (x + b[0] / u, y + b[1] / u, x + b[2] / u, y + b[3] / u)

    def _group(self):
        self._gid += 1
        return "g%d" % self._gid

    def _size_ok(self, text, pt):
        if pt * self.scale < self.min_pt - 0.005:       # 1 Nov: 6.00 pt is not under 6.0 (rounding)
            tp_warn(u"%s min_text: %r prints at %.2f pt, below the %.1f pt minimum" % (
                self.name, text[:40], pt * self.scale, self.min_pt), self.log)

    # -- registering
    def keep(self, geom, kind="keep", name=None, line=None):
        """an obstacle no text may touch (see the module notes)"""
        g = list(geom)
        if len(g) == 4 and not hasattr(g[0], "__len__"):
            K = dict(kind=kind, name=name, box=tuple(float(v) for v in g), pts=None, line=False, segs=None)
        else:
            P = [tuple(p[:2]) for p in g]
            if len(P) < 2:
                return None
            is_line = (kind in TP_LINE_KINDS) if line is None else bool(line)
            xs, ys = [p[0] for p in P], [p[1] for p in P]
            segs = list(zip(P, P[1:])) + ([] if is_line else [(P[-1], P[0])])
            K = dict(kind=kind, name=name, box=(min(xs), min(ys), max(xs), max(ys)), pts=P, line=is_line,
                     segs=TpSegIndex(segs=segs, cell=max(5.0 / self.unit_mm, 1e-6)))
        self.keeps.append(K)
        return K

    def block(self, box, name):
        """a drawing block (blocks may touch, never overlap)"""
        B = dict(kind="block", name=name, box=tuple(float(v) for v in box))
        self.blocks.append(B)
        return B["box"]

    def put(self, text, x, y, pt, bold=False, align="L", angle=0.0, name=None, role="label", colour=None, allow=(),
            group=None, emit=True, **extra):
        """one fixed text; returns its box"""
        text = u"%s" % text
        if not text.strip():
            return None
        self._size_ok(text, pt)
        it = dict(text=text, x=float(x), y=float(y), pt=float(pt), size_mm=pt * TP_PT, bold=bool(bold),
                  align=align or "L", angle=float(angle or 0.0), colour=colour, role=role, name=name,
                  allow=tuple(allow or ()), group=group or self._group(), emit=bool(emit), extra=extra)
        it["box"] = self._box(text, it["x"], it["y"], it["pt"], it["bold"], it["align"], it["angle"])
        self.items.append(it)
        self.checked = False
        return it["box"]

    def para(self, text, x, y, w, pt, lead, bold_marks=True, name=None, bold=False, colour=None, role="para",
             max_lines=None, min_last_words=2, allow=()):
        """a wrapped paragraph from the first baseline (x, y), w and lead in page units; returns the next baseline"""
        u = self.unit_mm
        size = float(pt)
        try:
            lines = tp_wrap(text, w * u, size, bold, min_last_words, bold_marks)
        except TpWidow:
            size = size - 0.25
            self._size_ok(text, size)
            try:
                lines = tp_wrap(text, w * u, size, bold, min_last_words, bold_marks)
            except TpWidow as ex:                       # round 5: a WARNING, set without the widow rule
                tp_warn(u"%s widow: %r: %s" % (self.name, text[:50], ex), self.log)
                lines = tp_wrap(text, w * u, size, bold, 1, bold_marks)
            lead = lead * size / float(pt)
        if max_lines is not None and len(lines) > max_lines:
            tp_warn(u"%s overrun: %r needs %d lines, %d allowed: shorten it" % (self.name, text[:50], len(lines),
                                                                               max_lines), self.log)
        g = self._group()
        sg = 1.0 if self.y_down else -1.0
        yy = float(y)
        for ln in lines:
            for s, b, xo in ln:
                self.put(s, x + xo / u, yy, size, b, "L", 0.0, name, role, colour, allow, g)
            yy += sg * lead
        return yy

    def _at(self, code, text, anchor, pt, bold, d):
        """(x, y, align) of a compass position code round the anchor"""
        if not isinstance(code, str):
            dx, dy, al = code
            return anchor[0] + dx, anchor[1] + dy, al
        ix0, iy0, ix1, iy1 = fm_ink_box(text, pt, bold)
        u, sg = self.unit_mm, (-1.0 if self.y_down else 1.0)
        k = 0.7071 * d
        mid = -(iy0 + iy1) / 2.0
        tab = dict(E=(d, mid, "L"), W=(-d, mid, "R"), N=(0.0, d - iy0, "C"), S=(0.0, -d - iy1, "C"),
                   NE=(k, k - iy0, "L"), NW=(-k, k - iy0, "R"), SE=(k, -k - iy1, "L"), SW=(-k, -k - iy1, "R"),
                   C=(0.0, mid, "C"))
        dx, v, al = tab[code.upper()]
        return anchor[0] + dx / u, anchor[1] + sg * v / u, al

    def _free(self, b, allow=(), group=None):
        if not (self.inner[0] <= b[0] and b[2] <= self.inner[2] and self.inner[1] <= b[1] and b[3] <= self.inner[3]):
            return False
        if self.footer_zone and tp_hit(b, self.footer_zone, 0.0):
            return False
        for it in self.items:
            if it["group"] != group and tp_hit(b, it["box"], self.pad):
                return False
        for K in self.keeps:
            if K["name"] in allow or K["kind"] in allow:
                continue
            if _tp_keep_hits(b, K, self.pad):
                return False
        return True

    def _ring_spots(self, text, anchor, pt, bold, d, rings):
        """(x, y, align) spots on rings round the anchor (round 5: the nearby free spots of G-R5-12)"""
        import math as _m
        ix0, iy0, ix1, iy1 = fm_ink_box(text, pt, bold)
        u, sg = self.unit_mm, (-1.0 if self.y_down else 1.0)
        mid = -(iy0 + iy1) / 2.0
        n = max(4, int(TP_RING_STEPS))
        for rr in rings or ():
            R_ = d + float(rr)
            for k in range(n):
                a = 2.0 * _m.pi * k / n
                dx, dv = R_ * _m.cos(a), R_ * _m.sin(a)
                al = "L" if dx > 0.3 * R_ else ("R" if dx < -0.3 * R_ else "C")
                if al == "C":                          # above / below: the ink edge, not its middle, at the ring
                    v = (dv - iy0) if dv > 0 else (dv - iy1)
                else:
                    v = dv + mid
                yield anchor[0] + dx / u, anchor[1] + sg * v / u, al

    def _try(self, t, anchor, positions, pt, bold, d, allow, rings):
        for code in positions:
            x, y, al = self._at(code, t, anchor, pt, bold, d)
            if self._free(self._box(t, x, y, pt, bold, al, 0.0), allow):
                return x, y, al
        for x, y, al in self._ring_spots(t, anchor, pt, bold, d, rings):
            if self._free(self._box(t, x, y, pt, bold, al, 0.0), allow):
                return x, y, al
        return None

    def place(self, text, anchor, positions=TP_POSITIONS, alts=(), pt=7.0, rank=0, side_list=None, bold=False,
              colour=None, name=None, r=0.0, gap=0.8, allow=(), role="label", rings=TP_RINGS, step=0.5):
        """a label beside its point (see the module notes); returns the registered item. Order (round 5): positions,
        rings, alts the same way, the side list number, then pt - step ... down to min_pt (printed), then a WARNING
        and the first position (the label is never dropped; check() names what it hits)"""
        d = float(r) * self.unit_mm + gap
        texts = [u"%s" % t for t in (text,) + tuple(alts or ())]
        self._size_ok(texts[0], pt)
        for t in texts:
            got = self._try(t, anchor, positions, pt, bold, d, allow, rings)
            if got:
                self.put(t, got[0], got[1], pt, bold, got[2], 0.0, name, role, colour, allow)
                return self.items[-1]
        if side_list is None:
            p_ = float(pt) - step
            while p_ * self.scale >= self.min_pt - 0.005:
                for t in texts:
                    got = self._try(t, anchor, positions, p_, bold, d, allow, rings)
                    if got:
                        self.put(t, got[0], got[1], p_, bold, got[2], 0.0, name, role, colour, allow)
                        return self.items[-1]
                p_ -= step
            tp_warn(u"%s overlap: label %r has no free spot round its point down to %.1f pt and no side list: set at "
                    u"its first position" % (self.name, texts[0], self.min_pt), self.log)
            x, y, al = self._at(positions[0] if positions else "E", texts[-1], anchor, pt, bold, d)
            self.put(texts[-1], x, y, pt, bold, al, 0.0, name, role, colour, allow, forced=True)
            return self.items[-1]
        x, y, al = self._at("C", u"0", anchor, pt, True, 0.0)
        self.put(u"0", x, y, pt, True, "C", 0.0, name, "number", colour, tuple(allow) + ("marker",))
        it = self.items[-1]
        if side_list not in self.sides:
            self.sides.append(side_list)
        side_list.add(anchor, u"%s" % text, it)
        return it

    # -- the test
    def check(self, raise_=True, log=None, blocks_in=False):
        """the collision test (see the module notes); returns the number of texts checked. Every hit is one
        "WARNING <page> overlap|edge: ..." line (round 5, C11: also with raise_=False); self.hits keeps them as
        (kind, a, b) for the caller's own counts"""
        lg = log if log is not None else (self.log if self.log is not None else TP_LOG)
        for sl in self.sides:
            if not sl.closed:
                tp_warn(u"%s side_list: %s was never closed (its numbers are not set)" % (self.name, sl.name), lg)
        hits = self.hits_now(blocks_in)
        I = self.items
        self.hits = hits
        self.checked = True
        if hits and raise_ and not TP_WARN_ONLY[0]:
            raise TextCollision(self.name, hits[0][1], hits[0][2], len(hits), [h[1:] for h in hits[1:]])
        for k_, a_, b_ in hits:                          # one WARNING line each; the run goes on
            ln_ = u"WARNING %s %s: %s against %s" % (self.name, k_, _tp_desc(a_), _tp_desc(b_))
            lg.append(ln_)
        if hits:
            if "wn_orange" in globals():
                wn_orange(u"%s: %d text hits (each one in the log, 'WARNING %s ...')" % (self.name, len(hits),
                                                                                       self.name))
            else:
                try:
                    ghenv.Component.AddRuntimeMessage(                                           # noqa: F821
                        __import__("Grasshopper").Kernel.GH_RuntimeMessageLevel.Warning,
                        u"%s: %d text hits (each one in the log)" % (self.name, len(hits)))
                except Exception:
                    pass
        lg.append(u"overlap %s checked %d, collisions %d" % (self.name, len(I), len(hits)))
        return len(I)

    def unput(self, it):
        """v32 (L1): takes a registered text off the page again (the booklet's collision fix places it anew)"""
        for i, c in enumerate(self.items):
            if c is it:
                del self.items[i]
                self.checked = False
                return True
        return False

    def hits_now(self, blocks_in=False):
        """v32 (L1): the hits of check() as [(kind, a, b)], with no log line and no message (the booklet's fix
        passes look before the final check)"""
        hits = []
        I = self.items
        inn = self.inner

        def inside(b):
            return (inn[0] - 1e-6 <= b[0] and b[2] <= inn[2] + 1e-6 and inn[1] - 1e-6 <= b[1] and
                    b[3] <= inn[3] + 1e-6)
        for i, a in enumerate(I):
            b = a["box"]
            if not inside(b):
                hits.append(("edge", a, u"the page edge or its margins"))
            if self.footer_zone and a["role"] not in ("footer", "crop_word") and tp_hit(b, self.footer_zone, 0.0):
                hits.append(("edge", a, u"the footer zone"))
            for c in I[i + 1:]:
                if c["group"] != a["group"] and tp_hit(b, c["box"], self.pad):
                    hits.append(("overlap", a, c))
            for K in self.keeps:
                if K["name"] in a["allow"] or K["kind"] in a["allow"]:
                    continue
                if _tp_keep_hits(b, K, self.pad):
                    hits.append(("overlap", a, K))
        B = self.blocks
        for i, a in enumerate(B):
            if blocks_in and not inside(a["box"]):
                hits.append(("edge", a, u"the page edge or its margins"))
            for c in B[i + 1:]:
                if tp_hit(a["box"], c["box"], -0.01 / self.unit_mm):
                    hits.append(("overlap", a, c))
        return hits

    def emit(self, drawer):
        """draws every registered text through drawer(item); returns how many"""
        n = 0
        for it in self.items:
            if not it["emit"]:
                continue
            if it["role"] == "number" and it["text"] == u"0":
                tp_warn(u"%s number: a numbered label was never given its number (close its side list): not drawn" %
                        self.name, self.log)
                continue
            drawer(it)
            n += 1
        return n

    def export(self):
        """boxes in mm, y DOWN from the top-left of bounds (crop-local), for the booklet's assembled-page test"""
        if not self.checked:
            self.check(False)
        u, b = self.unit_mm, self.bounds

        def mm(r):
            if self.y_down:
                return ((r[0] - b[0]) * u, (r[1] - b[1]) * u, (r[2] - b[0]) * u, (r[3] - b[1]) * u)
            return ((r[0] - b[0]) * u, (b[3] - r[3]) * u, (r[2] - b[0]) * u, (b[3] - r[1]) * u)
        return dict(page=self.name, size_mm=((b[2] - b[0]) * u, (b[3] - b[1]) * u),
                    texts=[dict(box=mm(it["box"]), role=it["role"], name=it["name"], text=it["text"])
                           for it in self.items],
                    keep=[dict(box=mm(K["box"]), kind=K["kind"], name=K["name"]) for K in self.keeps],
                    blocks=[dict(box=mm(B["box"]), name=B["name"]) for B in self.blocks])


def tp_shapes(shapes, tp, name=None, allow=(), y_down=None):
    """registers the text shapes of a common module's shape list in tp (tp draws them in emit) and returns the other
    shapes. Text shape forms: ("text", s, x, y, size_mm, colour, bold, align[, mat, halo]) and
    ("text", s, (x, y), size_mm, colour, bold, align); align "MC" = (x, y) is the middle of the ink."""
    rest = []
    for s_ in shapes or ():
        if not s_ or s_[0] != "text":
            rest.append(s_)
            continue
        if isinstance(s_[2], (tuple, list)):
            x, y = s_[2][0], s_[2][1]
            tail = list(s_[3:])
        else:
            x, y = s_[2], s_[3]
            tail = list(s_[4:])
        size_mm = tail[0]
        col = tail[1] if len(tail) > 1 else None
        bold = tail[2] if len(tail) > 2 else False
        al = tail[3] if len(tail) > 3 else "L"
        extra = {}
        if len(tail) > 4 and tail[4] is not None:
            extra["mat"] = tail[4]
        if len(tail) > 5 and tail[5] is not None:
            extra["halo"] = tail[5]
        tp.put(s_[1], x, y, size_mm * tp.unit_mm / TP_PT, bold, al, 0.0, name, "shape", col, allow, **extra)
    return rest
# ---- item_export.py (round 5, S1, 1 Nov 2026; G-R5-12, PLAN §4 schema v1): content scripts EXPORT, the booklet composes
# Aras 1 Nov 22:00: "produce every text every drawing and everything and in the last run make it place it and align it
# and booklet it". A content script lays out no page and burns no page text into a drawing: it hands every drawing
# (true-scale vector geometry in draw order) and every text (role, string, anchor) to one Ix, and Ix.save() writes
# Downloads/Bergama/cached/booklet/<folder>/items.json. The booklet (bergama_booklet parts 10-70) reads every such
# file, picks scales, sets and places every text, aligns blocks and checks the page. Successor of booklet_assets.py
# (blocks.json crops); addendum 1 Nov 22:37: no per-script sheet PDFs or previews (a script may still save its single
# drawings under output/<folder>/, but the booklet reads only items.json).
# Needs, included before it: bergama_paths.py (bg_booklet), grid.py (GRID_ROLE_PT, GRID_MIN_PT); warn.py optional (the
# content checks' WARNING lines go through wn_warn when it is included).
#
# items.json = {"schema": "bergama-items/1", "script", "version", "run": "YYYY-MM-DD HH:MM", "units": "m",
#               "pages": {page_id: [item, ...]}, "sources": {key: {text, url}}, "warnings": [str]}
# page_id = the round 5 23-page id ("p13", "p19"); an item with page None goes to "any" (the booklet's PLAN.py says
# where it is shown). Common keys of every item: id (unique in the file), page, kind, role, priority (1 first ... 9),
# group (items that belong together, e.g. one section's level column, legend and texts).
#
#   ix = Ix(folder, script, version)                      folder = the script's cached/booklet/ folder name
#   D = ix.drawing(id, page, extent, scale_pref=None, units="m", dkind="plan", north_deg=None, scale_bar=True,
#                  priority=1, group=None, fit=None, title=None)
#         extent (x0, y0, x1, y1) in drawing units, y UP, the area that must show; scale_pref = allowed 1:den (default
#         SF_SCALES); units "m" = true scale; "mm" = a scale-free diagram/chart in design mm, fit = (min_f, max_f)
#   ix.layer(D, name, shapes, z=None, k=1.0, origin=(0, 0), grp=None)   grp: G6-9 group (see "G6-9 groups" below)
#         adds shapes (the common modules' tuples: poly/line/circle/image; text shapes become anchored label items)
#         to layer `name` (water.py WAT_LAYERS for sections, map_layers ML_LAYERS for maps); coordinates are mapped
#         x_d = origin_x + k * x (k = drawing units per shape unit: den / 1000 for page-mm shapes drawn at 1:den);
#         line widths, dashes stay PRINT sizes (mm in the tuples, stored as pt); z defaults to the call order.
#         Stripes (hatches) are dropped: G-R5-4.1 no hatches (one WARNING per layer)
#   ix.keep(D, geom, kind="keep", name=None)               an area (drawing units) no label may cover
#   ix.anchor(D, name, xy)                                 a named point (cut ends, hubs) other items refer to
#   ix.text(page, string, role="label", drawing=None, at=None, size_pt=None, bold=None, colour=None, short_forms=(),
#           side_list_ok=True, justify=None, positions=None, priority=5, group=None, id=None, min_pt=None) -> id
#         role: title, intro, heading, caption, legend, list_item, note, label, level_value, badge, source;
#         a label of a drawing: drawing=id, at=(x, y) in drawing units (the booklet sets it beside that point)
#   ix.legend(page, drawing, entries, title=None, id=None, group=None)
#         entries: [(swatch, text)], swatch = dict(kind="fill"|"line"|"dash"|"dot"|"image", colour, stroke,
#         width_pt, dash_pt, file); text = a string (made a legend text item) or a text id
#   ix.list(page, drawing, texts, numbered=True, anchors=None, id=None, group=None)   ordered text rows
#   ix.levels(page, drawing, levels, side="R", id=None, group=None)
#         levels = [(name, z_m)] (z on the drawing's y axis, m a.s.l. for sections); the booklet draws the level
#         markers (PLAN §3, Aras's sketch U04) and their "+43.71" values beside the drawing
#   ix.inset(page, parent, window, child, factor, id=None)   child = a drawing id of the zoom; window in parent units
#   ix.keymap(page, cuts, looks=None, names=(), zooms=(), id=None)   the key-map module (S2) draws it in the booklet
#   ix.photo(page, file, crop=None, caption=None, source=None, id=None)
#   ix.chart(page, w_mm, h_mm, shapes, id=None)            a vector chart in its own mm box (y up)
#   ix.source(key, text, url, page=None)                   a Sources page row (texts cite it as {src:key})
#   ix.warn(page, kind, msg)                               a content check hit: WARNING line + orange + "warnings"
#   ix.save() -> path                                      writes items.json (UTF-8, 3 decimals), logs nothing itself
#   ix.summary() -> str                                    "items <script>: drawings n, texts n, ... -> <path>"
#
# ---- G6-9 groups (round 6, S2, 4 Nov 2026; Aras 17:50-17:51 "apply this to everything"): every exported shape dict
# carries "grp" = "<kind>/<element id>" (kind from IX_GRP_KINDS); the booklet passes it to write_pdf, which writes
# Drawing > kind > element as nested groups. Tag at the point of drawing, first match wins per shape:
#   1. markers in the shape list: ix_grp(kind, eid) -> ("grp", "kind/eid") opens, ix_grp_end() -> ("grp", None)
#      closes; ix_tag(kind, eid, shapes) -> [open] + shapes + [close]. Converters that rebuild tuples must pass
#      ("grp", ...) items through (xform.py does; page_stream ignores them, so sheets draw as before).
#   2. with ix_group(kind, eid): ...            every ix.layer call inside it (context manager)
#   3. ix.layer(D, name, shapes, grp="kind/eid")   the whole layer as one element
#   4. the layer name (IX_LAYER_KIND, e.g. "water", "figures", "proj_labels"): each shape its own element
#   5. none: the shape has no grp; the booklet's write_pdf puts it in "other" + one WARNING per drawing.
# Element ids: anything unique in the drawing, with the species/name first where there is one, e.g.
#   shapes += ix_tag("trees", u"%s %d" % (TREE_SPECIES[sp]["name"], i), pla_plan(sp, x, y, r))   (trees.py tree_grp)
IX_GRP_KINDS = ("trees", "buildings", "people", "plants", "water", "ground", "roads", "paths", "fields", "heritage",
                "hubs", "annotations", "cuts", "levels", "labels", "legend", "keymap", "frame", "other")
IX_LAYER_KIND = dict(ground="ground", bed="water", water="water", vegetation="plants", figures="people",
                     labels="labels", base_ground="ground", base_contours="ground", base_water="water",
                     base_names="labels", proj_water="water", proj_vegetation="plants", study="annotations",
                     proj_marks="annotations", proj_labels="labels", farms="fields", numbers="labels", chart="other")
IX_CUR_GRP = []             # the open ix_group contexts (innermost last)


def ix_grp(kind, eid=None):
    """the marker that opens a group for the shapes after it"""
    return ("grp", u"%s/%s" % (kind, eid if eid is not None else kind))


def ix_grp_end():
    return ("grp", None)


def ix_tag(kind, eid, shapes):
    return [ix_grp(kind, eid)] + list(shapes or ()) + [ix_grp_end()]


def ix_layer_kind(name):
    return IX_LAYER_KIND.get(u"%s" % name) if name else None


class ix_group(object):
    """with ix_group("legend", "p04"): ix.layer(...)  -> every shape of those layers in that one element"""
    def __init__(self, kind, eid=None):
        self.g = ix_grp(kind, eid)[1]

    def __enter__(self):
        IX_CUR_GRP.append(self.g)
        return self.g

    def __exit__(self, *a):
        if IX_CUR_GRP:
            IX_CUR_GRP.pop()
        return False


IX_SCHEMA = "bergama-items/1"
IX_PT = 25.4 / 72.0
IX_KINDS = ("drawing", "text", "legend", "list", "level_column", "inset", "keymap", "photo", "chart", "source")
IX_TEXT_ROLES = ("title", "intro", "heading", "caption", "legend", "list_item", "note", "label", "level_value",
                 "badge", "source")


def _ix_r(v, nd=3):
    try:
        return round(float(v), nd)
    except Exception:
        return v


def _ix_is_pt(p):
    return isinstance(p, (list, tuple)) and len(p) >= 2 and isinstance(p[0], (int, float)) and \
        isinstance(p[1], (int, float))


class Ix(object):
    def __init__(self, folder, script, version):
        import time as _t
        self.folder, self.path = folder, None
        self.d = {"schema": IX_SCHEMA, "script": script, "version": version,
                  "run": _t.strftime("%Y-%m-%d %H:%M"), "units": "m", "pages": {}, "sources": {}, "warnings": []}
        self.ids, self._z, self._n = set(), {}, 0

    # -- bookkeeping
    def _id(self, want, kind):
        if want is None:
            self._n += 1
            want = "%s_%s_%d" % (self.folder[:12], kind[:3], self._n)
        want = u"%s" % want
        if want in self.ids:
            k = 2
            while "%s_%d" % (want, k) in self.ids:
                k += 1
            self.warn(None, "export", u"item id %r used twice: the second is %s_%d" % (want, want, k))
            want = "%s_%d" % (want, k)
        self.ids.add(want)
        return want

    def _put(self, page, item):
        self.d["pages"].setdefault(page or "any", []).append(item)
        return item

    def _item(self, page, kind, id_, role=None, priority=5, group=None, **kw):
        it = dict(id=self._id(id_, kind), page=page, kind=kind, role=role or kind, priority=int(priority),
                  group=group)
        it.update(kw)
        return self._put(page, it)

    def warn(self, page, kind, msg):
        line = u"WARNING " + u" ".join(u"%s" % p for p in (page, kind) if p) + u": %s" % msg
        if "wn_warn" in globals():
            line = wn_warn(page, kind, msg)
        self.d["warnings"].append(line)
        return line

    # -- drawings
    def drawing(self, id, page, extent, scale_pref=None, units="m", dkind="plan", north_deg=None, scale_bar=True,
                priority=1, group=None, fit=None, title=None):
        x0, y0, x1, y1 = [float(v) for v in extent]
        if x1 <= x0 or y1 <= y0:
            self.warn(page, "export", u"drawing %s has an empty extent %r" % (id, extent))
        sp = list(scale_pref) if scale_pref else (list(SF_SCALES) if "SF_SCALES" in globals() else
                                                   [200, 250, 500, 1000, 2000, 2500, 5000, 10000, 20000])
        D = self._item(page, "drawing", id, "drawing", priority, group, dkind=dkind, units=units,
                       extent=[_ix_r(x0), _ix_r(y0), _ix_r(x1), _ix_r(y1)],
                       scale_pref=None if units == "mm" else [int(v) for v in sp],
                       fit=list(fit) if fit else ([0.5, 2.0] if units == "mm" else None),
                       north_deg=north_deg, scale_bar=bool(scale_bar and units == "m"), layers=[], keep_areas=[],
                       anchors={}, title=title)
        self._z[D["id"]] = 0
        return D

    def _shape(self, s, k, o):
        """one common-module shape tuple -> a schema shape dict (None for text and unknown kinds)"""
        def P(p):
            return [_ix_r(o[0] + k * p[0]), _ix_r(o[1] + k * p[1])]
        t = s[0]
        if t == "poly":
            if s[1] and not _ix_is_pt(s[1][0]):                       # page item: rings, fill, stroke, lw, dash,
                rings = [list(r) for r in s[1]]                       # stripes, alpha
                fill, stroke = s[2], (s[3] if len(s) > 3 else None)
                lw = s[4] if len(s) > 4 else 0.0
                dash = s[5] if len(s) > 5 else None
                stripes = s[6] if len(s) > 6 else None
                alpha = s[7] if len(s) > 7 else None
            else:                                                     # shape: ring, fill, stroke, lw, alpha, holes
                rings = [list(s[1])] + [list(R) for R in (s[6] if len(s) > 6 and s[6] else ()) if len(R) >= 3]
                fill, stroke = s[2], (s[3] if len(s) > 3 else None)
                lw = s[4] if len(s) > 4 else 0.0
                alpha = s[5] if len(s) > 5 else None
                dash, stripes = None, None
            rings = [[P(p) for p in r] for r in rings if len(r) >= 3]
            if not rings:
                return None
            return dict(t="poly", rings=rings, fill=fill or None, stroke=stroke or None,
                        width_pt=_ix_r((lw or 0.0) / IX_PT), dash_pt=[_ix_r(v / IX_PT) for v in dash] if dash else None,
                        opacity=alpha, _stripes=bool(stripes))
        if t == "line":
            if len(s[1]) < 2:
                return None
            dash = s[4] if len(s) > 4 else None
            return dict(t="line", pts=[P(p) for p in s[1]], stroke=s[2], width_pt=_ix_r((s[3] or 0.0) / IX_PT),
                        dash_pt=[_ix_r(v / IX_PT) for v in dash] if dash else None, cap=s[5] if len(s) > 5 else 1)
        if t == "circle":
            return dict(t="circle", c=P((s[1], s[2])), r=_ix_r(k * s[3]), fill=s[4] or None,
                        stroke=(s[5] if len(s) > 5 else None) or None,
                        width_pt=_ix_r(((s[6] if len(s) > 6 else 0.0) or 0.0) / IX_PT))
        if t == "image":
            x, y, w, h, f = s[1:6]
            clip = s[8] if len(s) > 8 else None
            return dict(t="image", box=P((x, y)) + P((x + w, y + h)), file=f, opacity=s[6] if len(s) > 6 else None,
                        flip=bool(s[7]) if len(s) > 7 else False,
                        clip=(P(clip[:2]) + P(clip[2:4])) if clip else None)
        return None

    def _grp_ok(self, D, g):
        """g with a known kind (an unknown kind becomes "other", one WARNING per kind and drawing)"""
        if not g:
            return None
        k_, _s, e_ = (u"%s" % g).partition("/")
        if k_ in IX_GRP_KINDS:
            return g
        seen = D.setdefault("_grp_bad", [])
        if k_ not in seen:
            seen.append(k_)
            self.warn(D["page"], "groups", u"%s: group kind %r unknown, written as other (kinds: %s)" % (
                D["id"], k_, u", ".join(IX_GRP_KINDS)))
        return u"other/%s" % (e_ or k_)

    def layer(self, D, name, shapes, z=None, k=1.0, origin=(0.0, 0.0), grp=None):
        out, texts, hatch = [], 0, 0
        mark = None                                       # G6-9: the open ("grp", ...) marker in this list
        ctx = IX_CUR_GRP[-1] if IX_CUR_GRP else None
        lk = ix_layer_kind(name)
        for s in shapes or ():
            if not s:
                continue
            if s[0] == "grp":
                mark = s[1] if len(s) > 1 else None
                continue
            if s[0] == "text":
                self._text_shape(D, s, k, origin)
                texts += 1
                continue
            sh = self._shape(s, float(k), origin)
            if sh is None:
                continue
            if sh.pop("_stripes", False):
                hatch += 1
            g = mark or ctx or grp or (u"%s/%s %d" % (lk, name, len(out) + 1) if lk else None)
            if g:
                sh["grp"] = self._grp_ok(D, g)
            out.append(sh)
        if hatch:
            self.warn(D["page"], "hatch", u"%s layer %s: %d hatch fill(s) dropped (G-R5-4.1 solid colours only)" % (
                D["id"], name, hatch))
        if z is None:
            self._z[D["id"]] = self._z.get(D["id"], 0) + 1
            z = self._z[D["id"]]
        D["layers"].append(dict(z=z, name=name, shapes=out))
        return len(out), texts

    def _text_shape(self, D, s, k, o):
        if isinstance(s[2], (tuple, list)):
            x, y = s[2][0], s[2][1]
            tail = list(s[3:])
        else:
            x, y = s[2], s[3]
            tail = list(s[4:])
        size_mm = float(tail[0]) if tail else 2.0
        al = tail[3] if len(tail) > 3 and tail[3] else "L"
        self.text(D["page"], s[1], "label", drawing=D["id"], at=(o[0] + k * x, o[1] + k * y),
                  size_pt=size_mm / IX_PT, bold=bool(tail[2]) if len(tail) > 2 else False,
                  colour=tail[1] if len(tail) > 1 and isinstance(tail[1], str) else None,
                  positions=["=" + str(al)] + ["E", "NE", "N", "NW", "W", "SW", "S", "SE"], group=D.get("group"))

    def keep(self, D, geom, kind="keep", name=None):
        g = list(geom)
        if len(g) == 4 and not hasattr(g[0], "__len__"):
            g = [[g[0], g[1]], [g[2], g[1]], [g[2], g[3]], [g[0], g[3]]]
        D["keep_areas"].append(dict(kind=kind, name=name, pts=[[_ix_r(p[0]), _ix_r(p[1])] for p in g]))

    def anchor(self, D, name, xy):
        D["anchors"][name] = [_ix_r(xy[0]), _ix_r(xy[1])]

    # -- texts and the rest
    def text(self, page, string, role="label", drawing=None, at=None, size_pt=None, bold=None, colour=None,
             short_forms=(), side_list_ok=True, justify=None, positions=None, priority=5, group=None, id=None,
             min_pt=None):
        if role not in IX_TEXT_ROLES:
            self.warn(page, "export", u"text role %r unknown (taken as note): %r" % (role, (u"%s" % string)[:80]))
            role = "note"
        if "names_fix" in globals():                       # G-R4-11 / G-R5-11: proper names through the names table
            try:
                string = names_fix(string)                                                     # noqa: F821
            except Exception:
                pass
        if "sf_strip_widths" in globals():                 # G-R5-4.6 (S3): no width in any exported text
            string = sf_strip_widths(string, page)                                             # noqa: F821
            if not (u"%s" % string).strip():
                return None
        pt0, b0, _ld, c0 = grid_role(role) if "grid_role" in globals() else (5.0, False, 1.3, "4A3F35")
        it = self._item(page, "text", id, role, priority, group, string=u"%s" % string,
                        anchor=None if drawing is None else dict(drawing=drawing,
                                                                 pt=None if at is None else [_ix_r(at[0]),
                                                                                             _ix_r(at[1])]),
                        size_pt=_ix_r(size_pt if size_pt is not None else pt0, 2),
                        min_pt=float(min_pt if min_pt is not None else (GRID_MIN_PT if "GRID_MIN_PT" in globals()
                                                                       else 4.0)),
                        bold=b0 if bold is None else bool(bold), colour=colour or c0,
                        short_forms=[u"%s" % t for t in short_forms or ()], side_list_ok=bool(side_list_ok),
                        justify=(role in ("intro", "caption", "note", "list_item", "source")) if justify is None
                        else bool(justify), positions=list(positions) if positions else None)
        return it["id"]

    def _tid(self, page, t, role, group):
        if isinstance(t, dict) and "id" in t:
            return t["id"]
        if isinstance(t, str) and t in self.ids:
            return t
        return self.text(page, t, role, group=group)

    def legend(self, page, drawing, entries, title=None, id=None, group=None):
        ents = []
        for sw, t in entries:
            tid = self._tid(page, t, "legend", group)
            if tid is not None:                            # a text that was only a width is gone (G-R5-4.6)
                ents.append(dict(swatch=dict(sw), text=tid))
        return self._item(page, "legend", id, "legend", 3, group, drawing=drawing, entries=ents,
                          title=None if title is None else self._tid(page, title, "heading", group))["id"]

    def list(self, page, drawing, texts, numbered=True, anchors=None, id=None, group=None):
        rows = [r for r in (self._tid(page, t, "list_item", group) for t in texts) if r is not None]
        return self._item(page, "list", id, "list", 4, group, drawing=drawing, items=rows, numbered=bool(numbered),
                          anchors=[[_ix_r(a[0]), _ix_r(a[1])] if a else None for a in anchors] if anchors else None)["id"]

    def levels(self, page, drawing, levels, side="R", id=None, group=None):
        lv = [dict(name=u"%s" % n, z=_ix_r(z, 3)) for n, z in levels]
        return self._item(page, "level_column", id, "level_column", 2, group, drawing=drawing, levels=lv,
                          side=side)["id"]

    def inset(self, page, parent, window, child, factor, id=None):
        return self._item(page, "inset", id, "inset", 2, None, parent=parent, window=[_ix_r(v) for v in window],
                          child=child, factor=float(factor))["id"]

    def keymap(self, page, cuts, looks=None, names=(), zooms=(), id=None):
        return self._item(page, "keymap", id, "keymap", 3, None, cuts=list(cuts), looks=dict(looks or {}),
                          names=list(names), zooms=list(zooms))["id"]

    def photo(self, page, file, crop=None, caption=None, source=None, id=None):
        cap = None if caption is None else self._tid(page, caption, "caption", None)
        return self._item(page, "photo", id, "photo", 2, None, file=file, crop=list(crop) if crop else None,
                          caption=cap, source=source)["id"]

    def chart(self, page, w_mm, h_mm, shapes, id=None):
        D = self.drawing(id, page, (0.0, 0.0, w_mm, h_mm), units="mm", dkind="chart", scale_bar=False,
                         fit=(0.75, 1.5))
        self.layer(D, "chart", shapes)
        D["kind_note"] = "chart"
        return D["id"]

    def source(self, key, text, url, page=None):
        self.d["sources"][key] = dict(text=text, url=url)
        if page:
            self._item(page, "source", "src_" + key, "source", 9, None, key=key)

    # -- out
    def save(self):
        import json as _j
        for its in self.d["pages"].values():               # G6-9 bookkeeping key, not part of the schema
            for it in its:
                it.pop("_grp_bad", None)
        d_ = bg_booklet(self.folder)
        os.makedirs(d_, exist_ok=True)
        self.path = os.path.join(d_, "items.json")
        with open(self.path, "w", encoding="utf-8") as f:
            _j.dump(self.d, f, ensure_ascii=False, separators=(",", ":"))
        return self.path

    def summary(self):
        n = {}
        for its in self.d["pages"].values():
            for it in its:
                n[it["kind"]] = n.get(it["kind"], 0) + 1
        return u"items %s: %s -> %s" % (self.d["script"], u", ".join(u"%s %d" % kv for kv in sorted(n.items())),
                                         self.path or u"(not saved)")
bergama_data("FACTS")
# ---- Shared facts reader (H-B 30 Oct 2026, M10). Include the data first:
#   #@include ../common/data/FACTS.py
#   #@include ../common/facts.py
# fact(key) = the value (float, or a (lo, hi) tuple for a range), unrounded; fact_text(key) = the printed form with
# the fact's fixed rounding and unit ("8,000 m³ per ha (1-in-5 dry year)"); None when a live file is missing (the
# page then prints nothing for it, never a typed copy). Live values come from Downloads/Bergama outputs on every run.
# The one page that prints a fact: fact_owner(key); a page that is not the owner should not print it (G4).
FACT_LOG = []
_FACT_CACHE = {}


def _fact_home(*p):
    import os as _o
    return _o.path.join(_o.path.expanduser("~"), "Downloads", "Bergama", *p)


# results files other scripts write (new place first, then where older versions wrote them)
FACT_FILES = dict(water_balance=[
    ("cached", "Bergama_water_balance_analysis", "water_balance_results.json"),
    ("output", "Bergama_water_balance_analysis", "water_balance_results.json")])


def _fact_rows():
    rows = globals().get("FACTS")
    if rows is None:
        raise RuntimeError("FACTS data missing: include ../common/data/FACTS.py before ../common/facts.py")
    return rows


def fact_file(name):
    """the parsed results file of another script (dict) or None; read once per run"""
    import os as _o
    import json as _j
    if name in _FACT_CACHE:
        return _FACT_CACHE[name]
    data = None
    paths = [_fact_home(*p) for p in FACT_FILES.get(name, [])]
    if name == "water_balance":                    # the oldest place, before Downloads/Bergama (water board WB_FILES)
        paths.append(_o.path.join(_o.path.expanduser("~"), "Downloads", "Bergama_water_balance_analysis",
                                  "water_balance_results.json"))
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8") as fh:
                data = _j.load(fh)
            FACT_LOG.append(u"Facts: %s read from %s" % (name, p))
            break
        except Exception:
            pass
    if data is None:
        FACT_LOG.append(u"Facts: %s results not found (run that script first); its facts are left out" % name)
    _FACT_CACHE[name] = data
    return data


def _fact_conv(row, v):
    c = row.get("conv")
    if v is None or c is None:
        return v
    if c == "drip_m3_ha":                          # net mm -> m³ per ha at the intake (1 mm on 1 ha = 10 m³)
        return v / fact("drip_efficiency") * 10.0
    if c == "ha_per_10000":
        return 10000.0 / v
    if c == "ratio":
        return float(v[0]) / float(v[1])
    if c == "da_sum_ha":                           # decares summed -> ha
        return sum(v) / 10.0
    raise ValueError("facts: unknown conv %r" % c)


def fact(key):
    """the value of a fact, unrounded (float, or (lo, hi)); None when a live source is missing"""
    rows = _fact_rows()
    if key not in rows:
        raise KeyError("no fact %r; known: %s" % (key, ", ".join(sorted(rows))))
    row = rows[key]
    k = row["kind"]
    if k == "static":
        return _fact_conv(row, row["value"])
    if k == "derived":
        return _fact_conv(row, fact(row["of"]))
    d = fact_file(row["file"])
    try:
        for p in row["path"]:
            d = d[p]
    except Exception:
        if d is not None:
            FACT_LOG.append(u"Facts: %s not in the %s results" % (key, row["file"]))
        return None
    if isinstance(d, (list, tuple)):
        return tuple(float(x) for x in d)
    return _fact_conv(row, float(d))


def fact_live(key):
    """True when the fact has a value now (static, or its live file was read)"""
    return fact(key) is not None


def fact_round(key, v):
    """v rounded as the fact prints it (round step, or nd decimals)"""
    row = _fact_rows()[key]
    if row.get("round"):
        st = float(row["round"])
        return int(round(v / st) * st)
    return round(v, row.get("nd", 0))


def fact_num(key, v=None):
    """the printed number only ("8,000", "1.25", "350,000-375,000"); None when missing"""
    v = fact(key) if v is None else v
    if v is None:
        return None
    row = _fact_rows()[key]
    nd = 0 if row.get("round") else row.get("nd", 0)

    def one(x):
        return ("{:,.%df}" % nd).format(fact_round(key, x))
    if isinstance(v, tuple):
        a, b = one(v[0]), one(v[1])
        return a if a == b else u"%s-%s" % (a, b)
    return one(v)


def fact_text(key, note=True):
    """number + unit (+ note): "8,000 m³ per ha (1-in-5 dry year)", "4.4 × its potential"; None when missing"""
    n = fact_num(key)
    if n is None:
        return None
    row = _fact_rows()[key]
    s = n + (u" " + row["unit"] if row.get("unit") else u"")
    if note and row.get("note"):
        s += u" " + row["note"]
    return s


def fact_ref(key):
    """(internal reference, public citation or None) of a fact"""
    row = _fact_rows()[key]
    return row.get("ref"), row.get("public")


def fact_owner(key):
    """the booklet page that prints the fact ("18"), None for a value that is never printed"""
    return _fact_rows()[key].get("printed_on")


def fact_prints_on(key, page):
    """True when page (a booklet page number) is the one that prints this fact (G4: once in the booklet)"""
    return str(_fact_rows()[key].get("printed_on")) == str(page)


# ---- G2/G3 (MIRAQUA round, 28 Oct 2026): Arial EMBEDDED in every sheet PDF -------------------------------------
# The sheets wrote the PDF standard fonts without embedding (Helvetica, Courier) with the Turkish letters in unused
# WinAnsi slots: the text was right (it copies and searches as İ ğ ş), but viewers without those glyphs drew nothing
# ("stiklal", "De irmen"). Now each font slot is Arial, embedded as a simple TrueType font with the SAME encoding
# (WinAnsi + the six Turkish letters in slots 129/141/143/144/157/158), so the strings, their measuring and the
# booklet's reading of the sheets stay as they were. Arial has Helvetica's widths, so nothing moves; text measured
# as Courier (the old monospace captions) comes out a little shorter. Text stays live for Illustrator.
# The font files are the system's (C:\Windows\Fonts\arial*.ttf, or the user's font folder): read and packed once per
# run. If a file is missing, that slot falls back to the old standard font and PDF_FONT_NOTE says so (for the log).
_PF_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}
_PF_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"
_PF_FILES = {"R": ("arial.ttf", "ArialMT", "Helvetica"), "B": ("arialbd.ttf", "Arial-BoldMT", "Helvetica-Bold"),
             "I": ("ariali.ttf", "Arial-ItalicMT", "Helvetica-Oblique"),
             "BI": ("arialbi.ttf", "Arial-BoldItalicMT", "Helvetica-BoldOblique")}
_PF_CACHE = {}
PDF_FONT_NOTE = []


def _pf_path(fn):
    import os as _o
    dirs = [_o.path.join(_o.environ.get("WINDIR", r"C:\Windows"), "Fonts"),
            _o.path.join(_o.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts"),
            "/Library/Fonts", "/System/Library/Fonts/Supplemental", "/usr/share/fonts/truetype/msttcorefonts"]
    for d in dirs:
        for nm in (fn, fn.capitalize(), fn.upper()):
            p = _o.path.join(d, nm)
            if _o.path.isfile(p):
                return p
    return None


def _pf_tables(data):
    """Round 4 (S1, 1 Nov 2026): the TrueType tables both the embedding (_pf_metrics) and the measuring
    (font_metrics.py) read, parsed once: upm, gid(char code) -> glyph id, adv (advance per glyph id), glyph_box(gid)
    -> (xMin, yMin, xMax, yMax) in font units or None (empty glyph), and the table offsets"""
    import struct as _s
    n = _s.unpack(">H", data[4:6])[0]
    tab = {}
    for i in range(n):
        tag, _c, off, ln = _s.unpack(">4sIII", data[12 + 16 * i:28 + 16 * i])
        tab[tag.decode("latin-1")] = (off, ln)
    h = tab["head"][0]
    upm = _s.unpack(">H", data[h + 18:h + 20])[0]
    bbox = _s.unpack(">hhhh", data[h + 36:h + 44])
    hh = tab["hhea"][0]
    asc, desc = _s.unpack(">hh", data[hh + 4:hh + 8])
    nhm = _s.unpack(">H", data[hh + 34:hh + 36])[0]
    hm = tab["hmtx"][0]
    adv = [_s.unpack(">H", data[hm + 4 * i:hm + 4 * i + 2])[0] for i in range(nhm)]
    cm = tab["cmap"][0]
    sub = None
    for i in range(_s.unpack(">H", data[cm + 2:cm + 4])[0]):
        pid, eid, off = _s.unpack(">HHI", data[cm + 4 + 8 * i:cm + 12 + 8 * i])
        if pid == 3 and eid == 1:
            sub = cm + off
    seg = _s.unpack(">H", data[sub + 6:sub + 8])[0] // 2
    ends = _s.unpack(">%dH" % seg, data[sub + 14:sub + 14 + 2 * seg])
    p = sub + 16 + 2 * seg
    starts = _s.unpack(">%dH" % seg, data[p:p + 2 * seg])
    deltas = _s.unpack(">%dh" % seg, data[p + 2 * seg:p + 4 * seg])
    ro_at = p + 4 * seg
    ros = _s.unpack(">%dH" % seg, data[ro_at:ro_at + 2 * seg])

    def gid(u):
        for k in range(seg):
            if starts[k] <= u <= ends[k]:
                if ros[k] == 0:
                    return (u + deltas[k]) & 0xFFFF
                a = ro_at + 2 * k + ros[k] + 2 * (u - starts[k])
                g = _s.unpack(">H", data[a:a + 2])[0]
                return (g + deltas[k]) & 0xFFFF if g else 0
        return 0
    ng = _s.unpack(">H", data[tab["maxp"][0] + 4:tab["maxp"][0] + 6])[0] if "maxp" in tab else 0
    lfmt = _s.unpack(">h", data[h + 50:h + 52])[0]

    def glyph_box(g):
        if "loca" not in tab or "glyf" not in tab or not (0 <= g < ng):
            return None
        lo = tab["loca"][0]
        if lfmt == 0:
            a, b = (2 * v for v in _s.unpack(">HH", data[lo + 2 * g:lo + 2 * g + 4]))
        else:
            a, b = _s.unpack(">II", data[lo + 4 * g:lo + 4 * g + 8])
        if b <= a:
            return None
        o = tab["glyf"][0] + a
        return _s.unpack(">hhhh", data[o + 2:o + 10])
    return dict(tab=tab, upm=upm, bbox=bbox, asc=asc, desc=desc, adv=adv, nhm=nhm, gid=gid, glyph_box=glyph_box)


def _pf_metrics(data):
    """widths of codes 32-255 (1000 units per em) and the descriptor numbers, read from the TrueType tables"""
    import struct as _s
    T = _pf_tables(data)
    tab, upm, bbox, asc, desc, adv, nhm, gid = (T[k] for k in ("tab", "upm", "bbox", "asc", "desc", "adv", "nhm",
                                                               "gid"))
    inv = dict((v, k) for k, v in _PF_EXTRA.items())
    widths = []
    for code in range(32, 256):
        try:
            ch = inv.get(code) or bytes([code]).decode("cp1252")
        except Exception:
            ch = None
        g = gid(ord(ch)) if ch else 0
        widths.append(int(round(adv[min(g, nhm - 1)] * 1000.0 / upm)) if g else 0)
    cap, ital, weight = 0.716 * upm, 0.0, 400
    if "OS/2" in tab:
        o = tab["OS/2"][0]
        weight = _s.unpack(">H", data[o + 4:o + 6])[0]
        if _s.unpack(">H", data[o:o + 2])[0] >= 2:
            cap = _s.unpack(">h", data[o + 88:o + 90])[0]
    if "post" in tab:
        o = tab["post"][0]
        ital = _s.unpack(">i", data[o + 4:o + 8])[0] / 65536.0
    k = 1000.0 / upm
    return dict(widths=widths, bbox=[int(round(v * k)) for v in bbox], asc=int(round(asc * k)),
                desc=int(round(desc * k)), cap=int(round(cap * k)), ital=ital, bold=weight >= 600)


def _pf_style(st):
    """(compressed font file, its length, metrics, PostScript name) of one style, or None: read once per run"""
    if st not in _PF_CACHE:
        fn, ps, _std = _PF_FILES[st]
        p, got = _pf_path(fn), None
        if p:
            try:
                import zlib as _z
                with open(p, "rb") as fh:
                    raw = fh.read()
                got = (_z.compress(raw, 6), len(raw), _pf_metrics(raw), ps)
            except Exception as e:
                PDF_FONT_NOTE.append("font %s not read (%s): standard font used" % (fn, e))
        else:
            PDF_FONT_NOTE.append("font %s not found: standard font %s used (Turkish letters may not show)" % (fn, _std))
        _PF_CACHE[st] = got
    return _PF_CACHE[st]


def pdf_fonts(add, styles, content=None):
    """Font objects for a PDF writer: styles = one of "R", "B", "I", "BI" per font slot /F1, /F2 ... in order (a slot
    may repeat a style: the same objects are used). add(bytes) -> object number, as the writers' own add().
    content: the page content (str or bytes); when given, a slot it never uses gets the light standard-font object
    instead of an embedded file. Returns the object numbers, one per slot."""
    if isinstance(content, bytes):
        content = content.decode("latin-1")
    made, out = {}, []
    for i, st in enumerate(styles):
        used = content is None or ("/F%d " % (i + 1)) in content
        key = st if used else "std-" + st
        if key not in made:
            got = _pf_style(st) if used else None
            if got is None:
                made[key] = add(("<< /Type /Font /Subtype /Type1 /BaseFont /%s /Encoding << /Type /Encoding "
                                 "/BaseEncoding /WinAnsiEncoding %s >> >>" % (_PF_FILES[st][2], _PF_DIFF)).encode("latin-1"))
            else:
                data, n, m, ps = got
                ff = add(("<< /Length %d /Length1 %d /Filter /FlateDecode >>\nstream\n" % (len(data), n)).encode("latin-1")
                         + data + b"\nendstream")
                flags = 32 + (64 if "I" in st else 0)
                fd = add(("<< /Type /FontDescriptor /FontName /%s /Flags %d /FontBBox [%s] /ItalicAngle %s /Ascent %d "
                          "/Descent %d /CapHeight %d /StemV %d /FontFile2 %d 0 R >>" % (
                              ps, flags, " ".join(str(v) for v in m["bbox"]), ("%.1f" % m["ital"]), m["asc"], m["desc"],
                              m["cap"], 140 if m["bold"] else 80, ff)).encode("latin-1"))
                made[key] = add(("<< /Type /Font /Subtype /TrueType /BaseFont /%s /FirstChar 32 /LastChar 255 "
                                 "/Widths [%s] /FontDescriptor %d 0 R /Encoding << /Type /Encoding /BaseEncoding "
                                 "/WinAnsiEncoding %s >> >>" % (ps, " ".join(str(w) for w in m["widths"]), fd, _PF_DIFF)
                                 ).encode("latin-1"))
        out.append(made[key])
    return out

_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}   # Turkish letters in unused WinAnsi slots
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"
# v4.1 (Aras 27 Oct, Prompt 8: "hm" for "hm³"): ² and ³ are drawn as the digit at 0.6 x the size, raised 0.28 x the
# size (then as wide as the ²/³ glyph, 333/1000), as water board v3.1: the unembedded Helvetica's ²/³ was missing in some viewers
SUP = {u"²": u"2", u"³": u"3"}
SUP_K, SUP_UP = 0.6, 0.28


def sup_runs(s):
    """v4.1: s cut into (text, raised) runs at ² and ³, which become a plain 2 or 3"""
    out, cur = [], u""
    for ch in s:
        if ch in SUP:
            if cur: out.append((cur, False))
            out.append((SUP[ch], True)); cur = u""
        else:
            cur += ch
    if cur: out.append((cur, False))
    return out


WB_TP_MARGINS = (0.0, 0.0, 0.0, 0.0)  # v10: the recorder's TextPage only answers "is this spot free" (no margins, no check)


class WbRec:
    """v10 (round 5 S5, G-R5-12; replaces v9's Page and write_pdf): the same drawing calls as the old sheet Page, but
    nothing is written to a PDF. v11 (G6-9): each shape also carries the element tag set by tag() (.gs). Everything a block draws is RECORDED as common shape tuples in page mm, y up
    (poly / line / text), which item_export turns into one chart drawing; every text becomes a label item anchored
    where v9 set it (first position = that spot, so v9's look is the start; the booklet moves, sizes and checks it).
    A TextPage still answers place()'s "is this spot free" so the labels start where v9 put them; it is never
    checked here and nothing raises (the booklet's layout check reports hits as warnings).
    panel_title() records its number, title and keyword line in .heads (heading + note texts, not drawn)."""
    def __init__(self, w=420.0, h=297.0, name=WB_PAGE):
        self.w, self.h, self.shapes, self.heads = w, h, [], []
        self.tp = TextPage(name, (0.0, 0.0, w, h), y_down=False, pad=0.6, margins=WB_TP_MARGINS)
        self.tg = None
        self.tg_ = ("other", "misc")                       # v11 (G6-9): the element tag every recorded shape carries
        self.gs = []                                       # v11: one tag per entry of .shapes (parallel list)
    def tag(self, kind, eid):
        """v11 (G6-9): the (kind, element id) the next shapes belong to; kind one of water, fields, annotations,
        labels, legend, other"""
        self.tg_ = (kind, str(eid))
    def group(self, start=True):
        """open (True) or close (False) one text group; returns whether this call opened it"""
        if start:
            if self.tg is not None:
                return False
            self.tg = self.tp._group()
            return True
        self.tg = None
        return False
    def box(self, s, x, y, size, bold=False, align="L"):
        return self.tp._box(s, x, y, size, bold, align, 0.0)
    def free(self, b):
        return self.tp._free(b)
    def rect(self, x, y, w, h, fill=None, stroke=None, lw=0.2):
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill, stroke, lw, True)
    def poly(self, P, fill=None, stroke=None, lw=0.2, closed=False, dash=None):
        P = [(float(x), float(y)) for x, y in P]
        if len(P) < 2:
            return
        if (fill or closed) and len(P) >= 3:
            self.shapes.append(("poly", P, fill, stroke, lw if stroke else 0.0, None)); self.gs.append(self.tg_)
        elif stroke:
            self.shapes.append(("line", P, stroke, lw, tuple(dash) if dash else None)); self.gs.append(self.tg_)
    def line(self, P, col, lw=0.25, dash=None): self.poly(P, None, col, lw, False, dash)
    def text(self, s, x, y, size, col="4A3F35", bold=False, align="L", hidden=False, _reg=True):
        """one label (size pt, baseline y, align L/C/R at x); ² and ³ stay Unicode (the booklet embeds Arial)"""
        if hidden or not s or not s.strip():
            return
        if _reg:
            self.tp.put(s, x, y, size, bold, align, 0.0, None, "label", col, (), self.tg, emit=False)
        self.shapes.append(("text", s, float(x), float(y), size * IX_PT, col, bool(bold), align or "L")); self.gs.append(self.tg_)
    def para(self, s, x, y, w, size, col="4A3F35", bold=False, lead=1.3, hidden=False):
        """s wrapped to w mm from baseline y at size pt (one label per line); returns the next line's baseline.
        v10: never raises: a widow at this size and 0.25 pt smaller is set without the two-word rule + WARNING"""
        if hidden or not (s or "").strip():
            return y
        lines = wb_wrap(s, w, size, bold, False)
        g_ = self.group()
        yy = y
        for ln in lines:
            for t, b, xo in ln:
                self.text(t, x + xo, yy, size, col, b)
            yy -= size * 0.3528 * lead
        if g_: self.group(False)
        return yy


def wb_wrap(s, w, size, bold=False, marks=True):
    """v10: tp_wrap with its two-word last line; when that fails at size and size - 0.25, the plain wrap + WARNING
    (round 4 raised TpWidow here)"""
    for sz in (size, size - 0.25):
        try:
            return tp_wrap(s, w, sz, bold, min_last_words=2, bold_marks=marks)
        except TpWidow:
            pass
        except TextError:                                 # a word wider than the column: one line (v12, L6: no
            return [[(s, bold, 0.0)]]                     # layout WARNING here; the booklet sizes and checks it)
    return tp_wrap(s, w, size, bold, min_last_words=1, bold_marks=marks)

# ------------------------------------------------------------------ helpers on the live results
MON = "J F M A M J J A S O N D".split()

def fmt(v):
    return "{:,.0f}".format(v)

def k_(v):
    return "%.1fk" % (v / 1000.0) if v >= 1000 else fmt(v)

def nice(v):
    """the next round number above v (1, 2, 2.5, 5 x 10^n)"""
    if v <= 0: return 1.0
    e = 10 ** math.floor(math.log10(v))
    return next(m * e for m in (1, 2, 2.5, 5, 10) if m * e >= v)

# ------------------------------------------------------------------ v2.7 labels; v9: real boxes from the page's TextPage
def place(pg, s, cands, size, col, bold=False, halo=False):
    """v2.7: label s at the first candidate (x, y, align) whose real box (v9: pg.box) is free on the page's TextPage;
    else the last one (v9: the page's check then RAISES). halo: a white field under the words, over the lines drawn
    before. v10: the spot found is only the label's FIRST position (the booklet may move it), so no halo is drawn: a
    white field left behind a moved label would cut the curves (halo kept as an argument, ignored)."""
    for x, y, al in cands:
        b = pg.box(s, x, y, size, bold, al)
        if pg.free(b): break
    pg.text(s, x, y, size, col, bold, al)
    return b

def fit_size(s, w, size, bold=False, low=7.0):
    """the largest size <= size (down to low) at which s fits w mm"""
    while size > low and text_w(s, size, bold) > w: size -= 0.5
    return size

def panel_title(pg, x, y, w, n, title, sub=None):
    """v2.7: a supporting panel's head: a rule over the panel's width, number, title, keyword line.
    v5 (MIRAQUA 28 Oct, G5): the keyword line's **...** runs are set bold (rich_parts).
    v10 (G-R5-12): nothing is drawn: the number + title and the keyword line are recorded in pg.heads and exported as
    a heading and a note text (the booklet sets them over the block; the rule above the title is the booklet's)"""
    pg.heads.append((n, title, sub))


# v5 (MIRAQUA 28 Oct, G5): one or two bold keywords per explanatory line, written "a **key** word"
def rich_tokens(s):
    """'a **key** word.' -> [(text, bold)] cut at the spaces (each space its own token)"""
    out = []
    for i, t in enumerate(s.split("**")):
        for k, piece in enumerate(t.split(" ")):
            if k: out.append((" ", bool(i % 2)))
            if piece: out.append((piece, bool(i % 2)))
    return out


def rich_parts(toks, size, col, bcol=None):
    """tokens [(text, bold)] or a '**' string -> inline() parts, runs of one weight merged; bold runs in bcol"""
    if isinstance(toks, str): toks = rich_tokens(toks)
    parts = []
    for t, b in toks:
        if parts and parts[-1][3] == b:
            parts[-1] = (parts[-1][0] + t, size, parts[-1][2], b)
        else:
            parts.append((t, size, (bcol or col) if b else col, b))
    return parts


# v10: rich_para (the sheet's question paragraph) is gone: the question is the page's intro text item

def arrow(pg, x0, x1, y, col, lw=0.6):
    pg.line([(x0, y), (x1 - 2.2, y)], col, lw)
    pg.poly([(x1 - 2.6, y + 1.5), (x1, y), (x1 - 2.6, y - 1.5)], fill=col, closed=True)

# ------------------------------------------------------------------ v2.4 visual first (SCRIPT_STANDARD 5b): [n] marks, pictograms, tiles
SOURCES = dict(    # every source and method sentence of the v2.3 sheet; v2.7: an invisible text layer (the booklet's sources page reads it)
    esa="ESA WorldCover 2021: farms = analysis area of the land-use map, unless changed",
    mgm="MGM/WMO 17742 normals 1991-2020",
    era5="Open-Meteo ERA5 daily 1991-2025 (scaled to the station)",
    dsi=u"DSİ gauges D04A053, D04A063 2016-2021, area-scaled",      # v5 (MIRAQUA 28 Oct, G3): DSİ with its İ
    fao56="FAO-56 (Allen et al. 1998): daily soil water balance, Penman-Monteith ET0",
    fao_t="FAO-56 Tables 19 and 22",
    fao_tm4="FAO Training Manual 4 (drip)",
    rg="RG 30802 minimum flow: stream counted above the legal minimum, worst case",
    ross="Ross & Hasnain 2018",
    suds="UK EA 2015 and Royal Haskoning 2012 SuDS costs (GBP x 1.25)",
    flow=u"Natural flow past the site = DSİ gauges D04A053 + D04A063, Oct 2015-Sep 2021, "   # v4.1 (Prompt 8): no internal file names
         u"each area-scaled to 101 km², mean of the two (upper case: the Kestel diversion not counted); both gauges fully dry 0-111 days a year")
# v6 (T3b): "dwa", "abu" (the site-catch block) and "lev" (the flood cut) left with what cited them
SRC_KEY = []

def cite(*keys):
    """v2.4: "[n]" (or "[n,m]") for sources in SOURCES; the numbered key is the sheet's hidden source layer (v2.7).
    v10 (G-R5-12): "{src:key}" per source (item_export's citation form; the booklet numbers them on its Sources page,
    where wb_items() registers every SOURCES row with ix.source)."""
    for k in keys:
        if k not in SRC_KEY: SRC_KEY.append(k)
    return " ".join("{src:%s}" % k for k in keys)        # one word per mark: a run of marks never outgrows a column

def ico(pg, name, cx, cy, size):
    """v6 (T3b, 02 §2): an icon of the booklet's one set (common/icons.py) centred on (cx, cy), size mm square; the
    sheet's own 10 x 10 pictograms (icon, tile) are gone"""
    for sh in ico_draw(name, cx, cy, size):
        if sh[0] == "poly":
            if sh[2] or sh[3]:
                pg.poly(sh[1], sh[2], sh[3], sh[4], True)
        else:
            pg.line(sh[1], sh[2], sh[3])

def inline(pg, x, y, parts):
    """v2.4: a keyword row: parts = [(text, size, colour, bold)] set one after another; returns the end x. v9: the
    runs are one text group (they touch by design)"""
    g_ = pg.group()
    for s, size, col, bold in parts:
        pg.text(s, x, y, size, col, bold); x += text_w(s, size, bold)
    if g_: pg.group(False)
    return x

def inline_w(parts):
    return sum(text_w(s, size, bold) for s, size, col, bold in parts)

def span(a, b, f=fmt):
    return f(a) if a == b else "%s-%s" % (f(a), f(b))

# ------------------------------------------------------------------ 7 THE ANSWER: the conclusion (store -> carries -> cut-off)
def panel_answer(pg, R, x, y, w, h):
    """The answer, read left to right: the store (the sheet's one headline value) -> what it carries -> where cost stops
    it. Every figure from R (results JSON): design.central_range_m3 / _pct_1in5_dry; prices RECHARGE_USD /
    ALTERNATIVE_USD (Ross & Hasnain 2018).
    revision 30 Oct (p10, G4/G5): a LIGHT field (water_tint at 15 %), the emphasis in the type: one headline value (the
    store, M10 storage_m3 formatted from the live results) plus one line; the carries and cost parts are small diagrams
    on the M1 columns (headline cols 1-5, carries 6-8, cost 9-12). v6's conclusion paragraph left (today's strip moved
    to block 2's marker; the cost cut-off is block 2's marker)."""
    d = R["design"]
    panel_title(pg, x, y + h, w, "4", "The answer")
    top = y + h - 7.0                                           # the light field under the title
    pg.tag("annotations", "answer_field")
    pg.rect(x, y, w, top - y, fill=C["water_tint"])
    lo_, hi_ = d["central_range_m3"]; plo, phi = d["central_range_pct_1in5_dry"]
    ky, vy, ly = top - 5.0, top - 12.5, top - 18.5               # kicker, headline value, the one line (v8: 3.5 mm above the field's foot)
    vpt, _, _, vcol = grid_style("value"); npt, _, _, ncol = grid_style("note")
    # A: the store, the one headline value (cols 1-5)
    ax, aw = grid_span(1, 5)
    pg.tag("annotations", "answer_store")
    ico(pg, "storage", ax + 9.0, vy + 2.0, 11.0)
    tx = ax + 18.0
    pg.text("STORE", tx, ky, 7.5, C["ink2"], True)
    s = u"%s m³" % (fact_num("storage_m3", (float(lo_), float(hi_))) or span(lo_, hi_))
    fs = fit_size(s, aw - 22.0, vpt, True)
    pg.text(s, tx, vy, fs, vcol, True)
    line = rich_parts("winter water held in the ground: **aquifer recharge**, if **borehole tests** accept it",
                      npt, ncol, C["ink"])
    inline(pg, tx, ly, line)
    a0 = tx + max(text_w(s, fs, True), inline_w(line)) + 4.0
    # B: what it carries (cols 6-8): a 100 % bar filled to the lower % of the range
    bx, bw_ = grid_span(6, 3); wb = bw_ - 14.0
    pg.tag("annotations", "answer_carries")
    if bx - 3.0 - a0 > 6.0: arrow(pg, a0, bx - 3.0, vy + 2.0, C["water_deep"], 0.5)
    pg.text("CARRIES", bx, ky, 7.5, C["ink2"], True)
    pg.rect(bx, vy + 0.5, wb, 3.0, fill=C["white"], stroke=C["structure"], lw=0.2)
    pg.rect(bx, vy + 0.5, wb * min(plo, 100.0) / 100.0, 3.0, fill=C["water_deep"])
    pg.text("100 %", bx + wb, vy - 3.0, 6.5, C["ink2"], False, "R")
    inline(pg, bx, ly, rich_parts("**%s %%** of the farms' need, **1 in 5 dry** year" % span(round(plo), round(phi)),
                                  npt, ncol, C["ink"]))
    # C: the cost cut-off (cols 9-12): the two price ranges on one linear US$ scale, each named at its bar's end
    cx, cw_ = grid_span(9, 4); ws = 58.0
    pg.tag("annotations", "answer_cutoff")
    arrow(pg, bx + wb + 2.0, cx - 3.0, vy + 2.0, C["water_deep"], 0.5)
    pg.text("COST CUT-OFF", cx, ky, 7.5, C["ink2"], True)
    vm = ALTERNATIVE_USD[1] * 1.02
    for i, (rng, col, lab) in enumerate(((RECHARGE_USD, _hu("WW", 2), "recharge $%g-%g /m³ " % RECHARGE_USD + cite("ross")),
                                         (ALTERNATIVE_USD, _hu("CTX", 2), "recycled water $%g-%g /m³" % ALTERNATIVE_USD))):
        yy = vy + 3.0 - i * 4.5
        pg.line([(cx, yy + 0.9), (cx + ws, yy + 0.9)], C["water_light"], 0.3)
        pg.rect(cx + ws * rng[0] / vm, yy, ws * (rng[1] - rng[0]) / vm, 1.8, fill=col)
        pg.text(lab, cx + ws + 3.0, yy, fit_size(lab, cw_ - ws - 3.0, 7.5, True, 6.0), _hu("WW", 1) if i == 0 else _hu("CTX", 2), True)
    inline(pg, cx, ly, rich_parts("past it, each more m³ costs **more than recycled water**", npt, ncol, C["ink"]))

# ------------------------------------------------------------------ the question (v6: the sheet's subtitle, under the title)
QUESTION = u"How much **winter water** can we hold for the farms' **dry summer**, and at what **cost**?"


# ------------------------------------------------------------------ v6 (T3b, G7): 1 one year of water, five rows, one month axis
STORE_COL = (_hu("WW", 4), _hu("WW", 3), _hu("WW", 1))   # v11 (G6-6): the store tones (light, mid, dark) from the hue table (were CBD9F8, 92A3C9, 3E4C6E)
YEAR_HEAD, YEAR_FOOT = 10.0, 13.0                # block 1: title + keyword line above the rows, months + Jun-Sep line under them, mm
YEAR_LAB_W, YEAR_TOT_W = 68.0, 40.0              # the label column before the month axis, the year column after it


def panel_year(pg, R, x, y, w, h):
    """v6 (revision 29 Oct, T3b WO-T3b-2; G7 after R31: every user its own row with its pictogram, one common time
    axis drawn as bars, figures read as charts): block 1, the whole balance through one year. Five rows share the
    month axis J-D: the Selinos stream (natural flow, Dec-Apr dark), the site catch, the design store's level, the
    summer strip and the farms (mean year and 1 in 5 dry). Each row has its own scale: its peak month carries its
    figure, its year total sits at the right. One band marks Jun-Sep across all rows and says what it means. Replaces
    v5's question block, farm tiles, monthly chart with its number rows, and the stream's monthly flow."""
    mix = R["design"]["mix"]; L = R["lands"]; crop = mix.split()[-1]
    q = STREAM_MONTH_M3; yr = float(sum(q)); win = (0, 1, 2, 3, 11)
    dn = R["farm_demand_month_m3"][mix]["mean"]; dd = R["farm_demand_month_m3"][mix]["dry5"]
    sm = R["design"].get("store_month_m3") or [0] * 12
    # revision 30 Oct (D3, M10): the field / olive grove areas print on p9 (their owner); here only when M10 says p10
    fa = (u_area(L["cropland_ha"] * 1e4, "ha") + " ") if fact_prints_on("cropland_ha", "10") else ""
    oa = (u_area(L["orchard_ha"] * 1e4, "ha") + " ") if fact_prints_on("orchard_ha", "10") else ""
    farm_sub = "%s%s fields + %solive grove, drip %s" % (fa, CROP_NAME.get(crop, crop), oa,
                                                        cite("fao56", "fao_t", "fao_tm4", "esa"))
    panel_title(pg, x, y + h, w, "1", "One year of water: it comes in winter, it is needed in summer",
                "**one month axis** for every user · each row to its own scale: its peak month and its year are written")
    lx, rx = x + YEAR_LAB_W, x + w - YEAR_TOT_W
    bw = (rx - lx) / 12.0
    top = y + h - YEAR_HEAD                                   # the first row's top
    rows = [
        ("stream", "Selinos stream", "natural flow past the site " + cite("flow"), (q,),
         lambda m: C["water_deep"] if m in win else C["water"], "%.1f million m³" % (yr / 1e6),
         "a year, %d %% in Dec-Apr" % round(100.0 * sum(q[m] for m in win) / yr)),
        ("rain", "Site catch", "roofs, walks, terraces " + cite("era5", "mgm"), (R["site_month_m3"],),
         lambda m: _hu("WW", 2), "%s m³" % fmt(R["site_catch_m3_per_year"]), "a year"),
        ("storage", "The store", "winter water held in the ground, level at month end " + cite("dsi", "rg"), (sm,),
         lambda m: STORE_COL[1], "%s m³" % fmt(max(sm)), "at its fullest"),
        ("water", "Summer strip", "%s, sealed: evaporation + seepage" % u_area(L["strip_m2"], "ha"),
         (R["strip_month_m3"],), lambda m: C["water"], "%s m³" % fmt(R["strip_m3_per_year"]), "a year, May-Oct"),
        ("olive", "Farms", farm_sub,
         (dn, dd), None, "%s m³" % fmt(R["farm_demand_m3"][mix]["dry5"]), "a year, 1 in 5 dry")]
    YEAR_RH = (h - YEAR_HEAD - YEAR_FOOT) / float(len(rows))   # v8 (P10.1): the rows fill the block (15.4 mm at h 100)
    yb_rows = top - len(rows) * YEAR_RH
    bx0, bx1 = lx + 5 * bw, lx + 9 * bw                      # Jun-Sep: one band behind every row
    pg.tag("annotations", "jun_sep_band")
    pg.rect(bx0, yb_rows - 13.0, bx1 - bx0, top + 1.0 - (yb_rows - 13.0), fill=_hu("AGR", 4))
    row_tag = dict(stream=("water", "row_stream"), rain=("water", "row_site_catch"), storage=("water", "row_store"),
                   water=("water", "row_strip"), olive=("fields", "row_farms"))    # v11 (G6-9): one element per row
    for i, (ic, name, sub, series, colf, tot, tot2) in enumerate(rows):
        ty = top - i * YEAR_RH
        pg.tag(*row_tag[ic])
        by, bh = ty - YEAR_RH + 2.6, YEAR_RH - 7.0
        ico(pg, ic, x + 5.0, ty - YEAR_RH / 2.0 + 0.6, 9.0)
        pg.text(name, x + 12.0, ty - 5.0, 9, C["ink"], True)
        pg.para(sub, x + 12.0, ty - 8.8, YEAR_LAB_W - 14.0, 7, C["ink2"])
        pg.line([(lx, by), (rx, by)], C["structure"], 0.2)
        vmax = float(max(max(s) for s in series)) or 1.0
        pk = None
        for m in range(12):
            x0 = lx + m * bw
            if len(series) == 1:
                v = series[0][m]; hh = bh * v / vmax
                if v > 0: pg.rect(x0 + bw * 0.2, by, bw * 0.6, max(0.3, hh), fill=colf(m))
                if pk is None or v > pk[1]: pk = (x0 + bw / 2.0, v, hh)
            else:                                             # the farms: mean year and 1 in 5 dry side by side
                for j, (s, col) in enumerate(((series[0], _hu("AGR", 2)), (series[1], _hu("AGR", 1)))):
                    v = s[m]; hh = bh * v / vmax
                    if v > 0: pg.rect(x0 + bw * (0.16 + 0.35 * j), by, bw * 0.33, max(0.3, hh), fill=col)
                    if j == 1 and (pk is None or v > pk[1]): pk = (x0 + bw * 0.675, v, hh)
        if pk and pk[1] > 0 and ic != "storage":              # (the store's peak is its year figure, at the right)
            s_ = ("%.2f million m³" % (pk[1] / 1e6)) if ic == "stream" else "%s m³" % fmt(pk[1])
            pg.text(s_, pk[0], by + pk[2] + 0.9, 7, C["ink"], True, "C")
        pg.text(tot, x + w, ty - 5.0, 9, C["ink"], True, "R")
        pg.text(tot2, x + w, ty - 8.6, 7, C["ink2"], False, "R")
        if len(series) == 2:                                  # the farms' two bars, named in the year column
            ex = x + w - inline_w([("mean", 7, 0, False), ("1 in 5 dry", 7, 0, False)]) - 2 * 3.6 - 4.0
            pg.tag("legend", "year_key")
            pg.rect(ex, ty - 12.6, 2.4, 2.4, fill=_hu("AGR", 2)); ex = inline(pg, ex + 3.6, ty - 12.3, [("mean", 7, C["ink"], False)])
            pg.rect(ex + 4.0, ty - 12.6, 2.4, 2.4, fill=_hu("AGR", 1)); pg.text("1 in 5 dry", ex + 7.6, ty - 12.3, 7)
    pg.tag("annotations", "year_axes")
    for m in range(12):
        pg.text(MON[m], lx + (m + 0.5) * bw, yb_rows - 1.4, 7.5, C["ink"], True, "C")
    js = round(100.0 * sum(dn[5:9]) / max(sum(dn), 1))
    pg.tag("annotations", "jun_sep_band")
    pg.text("JUN-SEP: %d %% of the farms' need" % js, (bx0 + bx1) / 2.0, yb_rows - 7.0, 8, _hu("AGR", 1), True, "C")
    pg.text("%.0f %% of the stream's flow" % (100.0 * sum(q[5:9]) / yr), (bx0 + bx1) / 2.0, yb_rows - 10.6, 7.5, C["ink"],
            False, "C")


# ------------------------------------------------------------------ 5 storage size: the sizing curve (v5: was panel 3)
def panel_curve(pg, R, x, y, w, h):
    mix = R["design"]["mix"]; crop = mix.split()[-1]
    panel_title(pg, x, y + h, w, "2", "How much to hold: the farm need covered, by store size",   # v6: block 2
                "34 water years 1991-2025 · daily · cropland as %s %s · in: **winter stream + site catch**, strip first %s"
                % (CROP_NAME.get(crop, crop), cite("era5", "fao56"), cite("dsi")))     # v5 (G11): "corn", the key stays maize
    lgx = x + w - 52                                         # legend column right of the plot
    cx, cy = x + 16, y + 12; cw = lgx - 6 - cx; ch = (y + h - 10) - cy
    cc = R["curve_closed"][mix]; tick = nice(cc[-1][0] / 8.0); nt = int(math.ceil(cc[-1][0] / tick)); vmax = tick * nt
    pg.tag("annotations", "curve_axes")
    for t in range(0, 101, 25):
        yy = cy + ch * t / 100.0; hl = t in (25, 50)
        pg.line([(cx, yy), (cx + cw, yy)], C["structure"] if hl else C["faint"], 0.3 if hl else 0.15, (1.2, 0.8) if hl else None)
        pg.text("%d %%" % t, cx - 1.5, yy - 1, 7, C["ink2"], hl, "R")
    for j in range(nt + 1):
        v = tick * j
        pg.text(fmt(v / 1000) + "k" if v else "0", cx + cw * v / vmax, cy - 4.5, 7, C["ink2"], False, "C")
    pg.text("storage, m³", cx + cw, cy - 9, 7, C["ink2"], False, "R")
    series = [(cc, 1, _hu("AGR", 2), None, "median year"),   # v11 (G6-6): both = the farms' need covered (AGR), dry year darker          # v6 (T3b): the open-pond curves left the sheet
              (cc, 2, _hu("AGR", 1), None, "1 in 5 dry year")]          # (results key curve_open unchanged)
    for (rows, col, colr, dash, lab), eid in zip(series, ("curve_median", "curve_dry5")):
        pg.tag("fields", eid)                                 # v11 (G6-9): each series its own element
        pg.line([(cx + cw * r[0] / vmax, cy + ch * min(r[col], 100.0) / 100.0) for r in rows], colr, 0.7, dash)
    xs = cx + cw * STRIP_TODAY / vmax
    pg.tag("annotations", "today_strip")
    pg.line([(xs, cy), (xs, cy + ch)], C["ink2"], 0.25, (0.6, 0.6))
    d = R["design"]
    xr = cx + cw * d["storage_m3"] / vmax; yr_ = cy + ch * min(d["covered_pct_1in5_dry"], 100.0) / 100.0
    pg.tag("annotations", "cutoff")
    pg.line([(xr, cy), (xr, yr_)], _hu("WW", 1), 0.4, (0.8, 0.6))   # v11: the chosen store size = WW r1
    pg.poly([(xr - 1.8, yr_), (xr, yr_ + 1.8), (xr + 1.8, yr_), (xr, yr_ - 1.8)], fill=_hu("WW", 1), closed=True)
    # labels last, each at the first free place (white field under it over the curves)
    tc = max(t["covered_pct_1in5_dry"] for t in R["today_strip_storage"].values())   # revision 30 Oct: from block 4's paragraph
    pg.tag("annotations", "today_strip")
    place(pg, "today %s m³: the strip only, %.0f %% of the need" % (fmt(STRIP_TODAY), tc), [(xs + 1.2, cy + ch - 3, "L"), (xs + 1.2, cy + ch - 7, "L")], 7, C["ink2"], halo=True)
    s1 = "cost cut-off " + cite("ross"); s2 = "%s m³ = %.0f %%" % (fmt(d["storage_m3"]), d["covered_pct_1in5_dry"])
    pg.tag("annotations", "cutoff")
    for dx, al, dy in ((-2.5, "R", -5.0), (2.5, "L", -5.0), (-2.5, "R", -14.0)):
        b1 = pg.box(s1, xr + dx, yr_ + dy, 8, True, al); b2 = pg.box(s2, xr + dx, yr_ + dy - 3.8, 8.5, True, al)
        if pg.free(b1) and pg.free(b2) and b1[3] < cy + ch and b2[1] > cy: break
    place(pg, s1, [(xr + dx, yr_ + dy, al)], 8, _hu("WW", 1), True, halo=True)
    place(pg, s2, [(xr + dx, yr_ + dy - 3.8, al)], 8.5, _hu("WW", 1), True, halo=True)
    pg.tag("legend", "curve_key")
    for i, (rows, col, colr, dash, lab) in enumerate(series):
        lyy = y + h - 13 - i * 4.6
        pg.line([(lgx, lyy + 1), (lgx + 6, lyy + 1)], colr, 0.7, dash); pg.text(lab, lgx + 7.5, lyy, 7)
    pg.tag("annotations", "max_365_days")
    ico(pg, "storage", lgx + 2.75, y + h - 36.75, 5.5)
    pg.text("max 365 days", lgx + 7.5, y + h - 36.5, 8, C["ink"], True)
    pg.text("in store, then to the strip", lgx + 7.5, y + h - 40.3, 7, C["ink2"])

# ------------------------------------------------------------------ 6 cost per m3, where to stop (v5: was panel 4)
def panel_store(pg, R, x, y, w, h):
    L = R["lands"]
    panel_title(pg, x, y + h, w, "3", "Cost per m³: cheapest first, then stop",   # v6: block 3
                "**US$/m³ delivered** · log scale · capital 5 %/yr " + cite("suds"))
    na = {r["key"]: r for r in R["ladder_no_recharge"]}
    rows = [("Aquifer recharge", "winter water into the alluvium " + cite("ross"), RECHARGE_USD[0], RECHARGE_USD[1])]
    # v5 (MIRAQUA 28 Oct, G13 + Aras 13:21 "if a page uses ha for areas try to keep ha for everywhere"): land areas in
    # ha like block 3's farm land (same values); the cistern's land per m³ stays a m² ratio
    lab = dict(pond="%s, %s m³ at most" % (u_area(L["pond_land_ha"] * 1e4, "ha"), fmt(L["pond_land_ha"] * 1e4 * POND_DEPTH * POND_USE)),
               crates="%s of walks" % u_area(L["walk_m2"] + L["riverside_walk_m2"], "ha"), cistern="0.12 m² of land per m³")
    for key, name, _, _ in BUILT:
        if key in na: rows.append((name, lab[key], na[key]["usd_per_m3_low"], na[key]["usd_per_m3_high"]))
    bx = x + 48; bw = w - 50
    lg = lambda v: (math.log10(min(max(v, 0.1), 100.0)) + 1) / 3.0          # 0.1 .. 100 US$ on a log axis
    n = len(rows); top = y + h - 16
    rh = min(12.0, max(8.5, (h - 36.0) / max(n, 1)))       # v8 (P10.1): rows follow the block height (8.5 mm before)
    pg.tag("annotations", "cost_axes")
    for t in (0.1, 1, 10, 100):
        xx = bx + bw * lg(t)
        pg.line([(xx, top + 3), (xx, top - n * rh + 1)], C["faint"], 0.15)
        pg.text(("$%g" % t), xx, top - n * rh - 2.5, 7, C["ink2"], False, "R" if t == 100 else "C")
    a0, a1 = ALTERNATIVE_USD
    pg.tag("water", "recycled_band")
    pg.rect(bx + bw * lg(a0), top - n * rh + 1, bw * (lg(a1) - lg(a0)), n * rh + 2, fill=C["water_light"])
    pg.text("recycled water " + cite("ross"), bx + bw * lg(a0), top + 4.2, 7, C["water_deep"], True)
    for i, (nm, ld, lo, hi) in enumerate(rows):
        yy = top - i * rh
        pg.tag("water", "cost_%d" % i)                        # v11 (G6-9): each cost row its own element
        pg.text(nm, x, yy, 7.5, C["ink"], True); pg.text(ld, x, yy - 3.2, fit_size(ld, bx - x - 1.5, 7.0), C["ink2"])
        pg.rect(bx + bw * lg(lo), yy - 1.5, max(0.8, bw * (lg(hi) - lg(lo))), 4, fill=_hu("WW", 2) if hi < a0 else _hu("CTX", 2))
    ky = top - n * rh - 7.5                                  # colour key, then the result
    pg.tag("legend", "cost_key")
    pg.rect(x, ky - 0.4, 3, 3, fill=_hu("WW", 2)); ex = inline(pg, x + 4.5, ky, [("cheaper than recycled", 7, C["ink"], False)])
    pg.rect(ex + 5, ky - 0.4, 3, 3, fill=_hu("CTX", 2)); pg.text("dearer", ex + 9.5, ky, 7)
    cheap = [r[0] for r in rows if r[3] < a0]
    pg.tag("annotations", "cost_result")
    inline(pg, x, ky - 6.0, ([] if cheap else [("nothing cheaper · ", 7.5, _hu("WW", 1), True)]) +
           [("recharge pays, up to the cost cut-off in 2", 7.5, _hu("WW", 1), True)])   # revision 30 Oct: the m³ once, in 4
    ico(pg, "storage", x + 2.25, ky - 10.85, 4.5)
    inline(pg, x + 6, ky - 11.8, rich_parts("**recharge fails tests**: built > recycled, every step " + cite("suds"), 7, C["ink2"], C["ink"]))

# v5 (MIRAQUA 28 Oct, P11.2): the sheet re-laid in Aras's reading order, top-left -> bottom-right, a rule and a numbered
# title over every block and 8-10 mm between the rows:
#   [title + 1 the question] [2 how the stream behaves: monthly flow | the flood cut at 1:500]
#   [3 what the farms need: tiles | monthly need]           [4 what the site can catch]
#   [5 storage size]                                         [6 cost]
#   [7 the answer: a light band across the foot, the bottom-right corner left free for the booklet's page number]
# (x, y bottom, w, h) in mm, y up; a block's title sits on y + h, its rule 4.5 mm above (panel_title). Shared with the
# booklet crops (booklet_export). Replaces v2.7's FARMS / PANELS / STREAM_BAND.
# v6 (T3b WO-T3b-2, G7): four blocks in reading order, the question as the sheet's subtitle:
#   [title + the question, the run line at the right]
#   [1 one year of water: five rows on one month axis, across the sheet (the focal block)]
#   [2 how much to hold: the storage curve]                 [3 cost per m³]
#   [4 the answer: store -> carries -> cost cut-off | the conclusion, the bottom-right corner free for the page number]
# revision 30 Oct (p10, D3 a, G2): the same four blocks on the M1 grid (columns, 4 mm baselines, top-down tops), the
# graphs at a secondary scale (block 1 rows 16.5 -> 13.5 mm; block 2 cols 1-7, block 3 cols 8-12), 16-20 mm between the
# rows, block 4 a light band across the foot that ends on the drawing area's last baseline (273)
def _grid_block(c0, n, top, h):
    """(x, y bottom, w, h) mm y-up of an M1 grid cell: n columns from c0, top (mm from the page top), height h"""
    r = grid_rect_up(grid_cell(c0, n, top, h))
    return (r[0], r[1], r[2] - r[0], r[3] - r[1])


# v8 (round 3, P10.1 "too much empty area"): block 1 36-136 (was 36-128) with taller rows, blocks 2-3 152-224 (were
# 144-216), block 4 240-272 (was 236-272, 32 mm: its empty field under the one line goes); tops on baselines, heights in
# whole 4 mm steps (grid_cell rounds up), 16 mm between the rows as before
BLOCKS = dict(year=_grid_block(1, 12, 36.0, 100.0),
              curve=_grid_block(1, 7, 152.0, 72.0), store=_grid_block(8, 5, 152.0, 72.0),
              answer=_grid_block(1, 12, 240.0, 32.0))


# v10 (G-R5-12): each block = one chart drawing; its window = v9's booklet crop (the block under its title line)
WB_PANELS = (("wb_year", "year", 7.5, 1), ("wb_curve", "curve", 7.5, 2), ("wb_store", "store", 7.5, 3),
             ("wb_answer", "answer", 6.5, 4))          # (drawing id, BLOCKS key, mm cut off the top, reading order)


def _wb_grp(kind, eid):
    """G6-9: the shared module's group context (common/item_export.py ix_group, built in round 6 S2); a no-op before it exists"""
    f = globals().get("ix_group")
    if f:
        try:
            return f(kind, eid)
        except Exception:
            pass
    import contextlib
    return contextlib.nullcontext()


def wb_items(R):
    """v10 (round 5 S5, G-R5-12; was build(), CHK-12): p10 (v11; was p11) as items, no sheet PDF. The page title and
    the question (intro) (v11: the run line is gone); per block (BLOCKS, reading order 1-4) one chart drawing in page mm (y up) with
    every shape the block draws (WbRec) and every word inside it as an anchored label, plus its number + title as a
    heading and its keyword line as a note (group = the drawing id); every SOURCES row as an ix.source. Writes
    cached/booklet/Bergama_water_balance_analysis/items.json; returns the Ix (summary for the log).
    v5 (MIRAQUA 28 Oct, P11.2): the blocks drawn in reading order, so the source marks count up that way.
    v6 (T3b): four blocks (1 the year, 2 the curve, 3 the cost, 4 the answer); the question under the title.
    v11 (G6-9): each run of shapes with one tag (WbRec.tag) is its own layer "<kind>/<eid>" inside _wb_grp(kind, eid);
    the counts go to ix.grp_counts (kinds, elements, untagged) for the log."""
    ix = Ix(WB_FOLDER, "bergama_water_balance", VERSION)
    del SRC_KEY[:]
    ix.text(WB_PAGE, "The water balance", "title", id="wb_title", priority=1)
    ix.text(WB_PAGE, QUESTION, "intro", id="wb_question", priority=2)
    fns = dict(year=panel_year, curve=panel_curve, store=panel_store, answer=panel_answer)
    kinds, elems, untagged = set(), set(), 0
    for did, key, cut, n in WB_PANELS:
        x, y, w, h = BLOCKS[key]
        pg = WbRec()
        fns[key](pg, R, x, y, w, h)
        D = ix.drawing(did, WB_PAGE, (x - 0.5, y - 0.5, x + w + 0.5, y + h - cut), units="mm", dkind="chart",
                       scale_bar=False, priority=n, group=did)
        for hn, ht, hs in pg.heads:                       # v12 (L6, one box per drawing): disc + title + subtitle
            ix.text(WB_PAGE, hn, "badge", drawing=did, group=did, id=did + "_num", priority=n)
            ix.text(WB_PAGE, ht, "heading", drawing=did, group=did, id=did + "_head", priority=n)
            if hs:
                ix.text(WB_PAGE, hs, "caption", drawing=did, group=did, id=did + "_note", priority=1)
        runs = []                                         # v11 (G6-9): consecutive runs of one tag
        for sh, tg in zip(pg.shapes, pg.gs):
            if runs and runs[-1][0] == tg:
                runs[-1][1].append(sh)
            else:
                runs.append((tg, [sh]))
        for (kind, eid), run in runs:
            with _wb_grp(kind, eid):
                ix.layer(D, "%s/%s" % (kind, eid), run)
        kinds.update(tg[0] for tg in pg.gs); elems.update(pg.gs)
        untagged += sum(1 for tg in pg.gs if tg == ("other", "misc"))
    for k in SOURCES:                                     # v2.4: one source list (no source can drop out)
        ix.source(k, SOURCES[k], None, page=WB_PAGE)
    ix.grp_counts = (len(kinds), len(elems), untagged)
    ix.save()
    return ix

# ------------------------------------------------------------------ v2.6-v9 booklet crops (blocks.json) gone in v10: wb_items()

def booklet_figures(R):
    """v2.5: figures the booklet prints that the sheet only computed inline (results JSON keys, read live)."""
    dn = R["farm_demand_month_m3"][R["design"]["mix"]]["mean"]
    R["jun_sep_share_of_need_pct"] = round(100.0 * sum(dn[5:9]) / max(sum(dn), 1), 1)
    sh = [100.0 * R["site_catch_m3_per_year"] / d["mean"] for d in R["farm_demand_m3"].values() if d["mean"]]
    R["site_catch_share_of_need_pct"] = [round(min(sh), 1), round(max(sh), 1)] if sh else [0.0, 0.0]


# ------------------------------------------------------------------ run (GH Button on any input, ScriptEditor, or python)
def main(g):
    """v10: compute, write the results JSON, export p10's items (v11; was p11); the log = "<n> warnings" + every WARNING line on
    top (wn_compose), then the run's lines. Nothing is written to output/ (C2)."""
    t0 = time.time()
    wn_reset()                                            # v10: one warning sink per run
    L, src = get_lands(g)
    R = compute(L); R["lands_source"] = src
    try:                                                  # v6 (T3b): the zones for the water board's p.12 map; never
        R["zones"] = get_zones(L["option"])               # breaks the balance (no key = p.12 shows the places only)
        zone_line = "zones for p11: %d zones, %d links (%s)" % (len(R["zones"]["zones"]), len(R["zones"]["links"]), R["zones"]["source"])
    except Exception as ex:
        zone_line = "zones for p11 NOT WRITTEN: %s: %s" % (type(ex).__name__, ex)
        wn_warn(WB_PAGE, "data", zone_line)
    booklet_figures(R)                                    # v2.5: results keys the booklet prints
    os.makedirs(RES_DIR, exist_ok=True)
    with open(os.path.join(RES_DIR, OUT_JSON), "w", encoding="utf-8") as f:
        json.dump(R, f, indent=1, ensure_ascii=False)
    ix = wb_items(R)                                      # v10: the page's items (G-R5-12); v11: p10
    d = R["design"]; tm = time.strftime("%H:%M:%S")
    lines = ["%s  %s" % (os.path.join(RES_DIR, OUT_JSON), tm), ix.summary(),
             "cut-off %s m3 = %.1f %% (1 in 5 dry)" % (fmt(d["storage_m3"]), d["covered_pct_1in5_dry"]),
             "stream: %s m3 a year taken = %.1f %% of the water stored; %.1f %% of its winter flow left (driest year %.1f %%)" % (
                 fmt(d["river_take_m3_per_year"]), d["river_take_share_pct"], d["river_left_pct"][1], d["river_left_pct"][0]),
             "riverside walks %s m2 from %s" % (fmt(L["riverside_walk_m2"]), src["riverside_walk_m2"]),
             zone_line, "trigger: " + (TRIG_WHY[0] or "-"), "legend p10 hues=table",
             "groups p10 kinds=%d elements=%d untagged=%d" % getattr(ix, "grp_counts", (0, 0, 0))]
    lines += ["year %s (%s): in %s + %s m3, strip %s, farms %s of %s, released %s, out %s; winter flow %.0f %% of median" % (
        k, v["water_year"], fmt(v["carried_in_m3"]), fmt(v["filled_m3"]), fmt(v["strip_m3"]), fmt(v["farms_m3"]),
        fmt(v["farm_need_m3"]), fmt(v["released_m3"]), fmt(v["carried_out_m3"]), v["winter_flow_pct_of_median"])
        for k, v in ((yk, d["year_split"][yk]) for yk in ("normal", "dry5"))]     # v4 (Prompt 6)
    head = ["water balance %s · %s · %.1f s" % (VERSION, time.strftime("%Y-%m-%d %H:%M:%S"), time.time() - t0)]
    return "\n".join(wn_compose(tp_log_lines() + lines, head))

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
TRIG_WHY = [None]                                         # v9: what started this run (trig_should_run), for the log


def done_text(ran, ok, secs):
    """The done output: kept until the next run (this Rhino session)."""
    return ("done " if ok else "ERROR ") + time.strftime("%H:%M:%S") + ".%02d" % int((time.time() % 1) * 100) + \
        " · %.0f s" % secs if ran else None


_gh = "ghenv" in globals()
if _gh:
    import scriptcontext as _sc
    try: _ik = ":" + str(ghenv.Component.InstanceGuid)   # 25 Oct 10:29: each component keeps its own log and done
    except Exception: _ik = ""
    _pressed, _why, _btn = trig_should_run("bergama_water_balance_log_chain")   # v9 (round 4 S1): one trigger file
    TRIG_WHY[0] = _why
    if _pressed:
        _t0 = time.time()
        try:
            _res = main(globals())
        except Exception as _ex:   # 25 Oct: the error goes into the log panel, the old log never stays
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-600:])
        _sc.sticky["bergama_water_balance_log" + _ik] = write_log(_res)
        _sc.sticky["bergama_water_balance_log_status" + _ik] = ("ERROR" if _sc.sticky["bergama_water_balance_log" + _ik].startswith(("ERROR", "The PDF is open")) else time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky["bergama_water_balance_log_done" + _ik] = done_text(True, not _sc.sticky["bergama_water_balance_log_status" + _ik].startswith("ERROR"), time.time() - _t0)
        _sc.sticky["bergama_water_balance_log_ver" + _ik] = VERSION
    if _sc.sticky.get("bergama_water_balance_log_ver" + _ik) != VERSION:   # v3 (Aras 27 Oct 15:35): a newly pasted version
        for _s in ("", "_status", "_done"):                                 # shows itself at once, idle, without the old
            _sc.sticky.pop("bergama_water_balance_log" + _s + _ik, None)     # run's time or log
    done = _sc.sticky.get("bergama_water_balance_log_done" + _ik, "idle")   # 25 Oct 10:20: stays after the run; wire into the next script's run (one-click chain)
    log = _sc.sticky.get("bergama_water_balance_log" + _ik, "Press the Button to compute and export to " + RES_DIR + " and " + bg_booklet(WB_FOLDER))
    print(log)               # 25 Oct 12:10: the canvas's log output is Grasshopper's "out" (printed text): print the log
    try: ghenv.Component.Message = "WaterBalance " + VERSION + " · " + _sc.sticky.get("bergama_water_balance_log_status" + _ik, "idle")   # Aras 25 Oct 09:44
    except Exception: pass
else:
    print(write_log(main(globals())))
