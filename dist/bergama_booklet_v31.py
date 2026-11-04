# -*- coding: utf-8 -*-
# r: pymupdf==1.26.5
# CURRENT VERSION: bergama_booklet_v31.py = v31 (round 6 S9, 4 Nov 2026: 22 pages p01-p22 in the PLAN §2.1 order, each page
# laid out in its FRAMES (G6-1: the SUBMISSION_SON arrangement, drawings enlarged uniformly into their frames), title
# band + bare page number, Sources last with every source numbered in page order (G6-3), G6-9 group tags handed to the
# PDF writer, every overlap / edge / empty band / < 4 pt = WARNING (G6-7, G6-8)); v30.3 (fix 2 Nov 06:40: maps larger: round scales 1:1,500, 1:7,500, 1:15,000, 1:25,000 added, a script's scale range open to them; diagrams free-size up to 6 x; p07, p10, p16, p22 re-planned so rows fit; p11, p21 wider); v30.2 (fix 2 Nov: p04/p05 one row per cut, one scale, from site board v60.2); v30.1 (closing fix 2 Nov: Sources lists the masterplan places properly); v30 (round 5 S10, 2 Nov 2026: the booklet COMPOSES every page from the
# scripts' exported items (G-R5-12): 23 pages, one page numbering, no sheet crops; see NEW IN v30)
"""Bergama Group 6: A3 BOOKLET COMPOSER (round 5; round 6 v31 page frames). Rules: scripts/_template/SCRIPT_STANDARD.md §9.
Builds ONE multi-page landscape A3 PDF (420 x 297 mm) from every content script's booklet items.

Component: Rhino 8 > Grasshopper > Python 3 Script, paste the whole file. The first run installs PyMuPDF 1.26.5 (the
"# r:" line above; needs internet once).
  input  run   Button (or the done text of the script before it in the chain)
  output log   the last run's report: "<n> warnings" + every WARNING line on top, then per page its drawings and scales,
               "layout <page> fill=… ref_p15=… empty_band=… overlaps n edge n min_text=…", "text justified n"
  output done  "done HH:MM:SS.ss · N s"
Reads  ~/Downloads/Bergama/cached/booklet/<script folder>/items.json (every content script, round 5)
Writes ~/Downloads/Bergama/output/bergama_booklet/Bergama_booklet_A3.pdf; temporary drawing PDFs in
       ~/Downloads/Bergama/cached/booklet/_render/
NEW IN v31 (round 6, session S9, 4 Nov 2026; revision_2026-11-04_round6/PLAN.md §2.1, §2.2, §3, §7 S9; a feature):
  * G6-1: the page plan (parts/80_plan.py) is a list of FRAMES per page ([x, y, w, h] in % of A3, from
    plan_findings/frames_*.md "Target frames"); each frame takes the exported items whose ids match its patterns;
    maps and sections take the largest round scale that fits their frame (frames with one "same" key share one scale),
    diagrams the largest factor; an item no frame names goes to the page's side frame with a WARNING (never lost).
  * G6-2: 22 pages, the content scripts export the new ids p01-p22 directly (the 25 -> 23 map is gone); contents on the
    cover from the same list; the page number alone, bottom right; log "pagenum <n>".
  * G6-3: Sources = page 22, four (or five) columns, "[n] text" in page order, hanging indent; {src:key} marks are
    numbered in texts, legend entries, list rows and photo captions, plus a drawing's "src_keys" list.
  * G6-4 north arrow outside the drawing (scale band, right end). G6-9: each shape's "grp" tag goes to write_pdf as
    pg.grp (log "groups <page> kinds=<n> elements=<n> untagged=<n>"). Log "page <pid> frames=<n> placed=<n> unlisted=<n>".
Run it LAST in the chain (zone base -> site board -> masterplan -> water balance -> agriculture -> water board ->
proposal sections -> city link -> booklet).
NEW IN v30 (round 5, session S10, 2 Nov 2026; revision_2026-11-01_round5/PLAN.md §10 S10; a feature change):
  * Change of approach (G-R5-12; round 4 failed on text collisions and sheet crops): no sheet PDF and no crop is read
    any more. Each content script exports its drawings (true-scale geometry) and texts; this script picks every scale
    from the Bergama list, sets every text (justified, last line left, >= 4 pt), places labels at their anchors,
    legends / lists / level markers / key maps beside their drawings, and checks every page (warnings, never stops).
  * 23 pages (D7, D9): p13 = W1-W4 on one page at one scale (N3 1:500), p18 = F2, F4, W1, S4 on one page; one page
    numbering (parts/81_ids.py maps the scripts that still export 25-page ids); contents for 23 pages (P01.2).
  * Cover photo full bleed under a white veil (P01.1). Scales printed by the booklet ("1:den" under every true-scale
    drawing, scale bars where the drawing has none of its own), north arrows from each plan's north_deg, {src:key}
    marks numbered in page order with one Sources page; the false "· style a" crop label gone (P22).
  * Layout check per page (70_check) against p14 (= the 25-page p15, D2): fill, empty band, overlaps, edges, min text.
"""
import os, re, time, json, fnmatch

# ---- SETTINGS ----
VERSION = "v31"  # v31 4 Nov 2026 (round 6 S9): page frames (G6-1), 22 pages (G6-2), Sources last (G6-3), groups (G6-9); was v30.3 fix (2 Nov run: drawings small, things on top of each other): texts of diagrams, charts, key maps and site board drawings stay where their script set them, scaled with the drawing (site board: from its "sheet scale 1:N"), never moved or numbered into side lists; one factor per diagram row; right-column drawings share the room left; insets 1:100 or 1:200 as the row allows; p02 share 0.50, p07 notes as a 4th row, p13 share 0.78 + smaller key map; 1:50,000 for the p19 farms map; booklet scale list 1:200 ... 1:25,000 with 1:1,500, 1:7,500, 1:15,000 (Aras 06:20) and 1:25,000; scale_pref read as a range; diagrams up to 6 x (right column 2 x); page plan p07 3 rows, p10 windows 2 x 3, p11 share 0.80, p16 3 x 2 share 0.62, p21 share 0.75, p22 plans side by side at 1:1,000 or 1:1,500; v30.2 fix (round 5 open rows): p04/p05 rows = one drawing per cut (sb_sec_s1 ... s8), one scale per page (common); v30.1 fix (round 5 closing): the Sources page lists the masterplan's numbered places as "n name: sources" (v30 printed the raw dict); v30 2 Nov 2026 (round 5 S10): composer pages from items.json, 23 pages, one page numbering
GH_LABEL = "Booklet"
OUT_FOLDER = "bergama_booklet"
LOG_NAME = "bergama_booklet_log.txt"
PDF_NAME = "Bergama_booklet_A3.pdf"
PT = 25.4 / 72.0                             # mm per point (write_pdf needs it)

# ---- composer core: includes (round 5, S1, 1 Nov 2026; G-R5-12, PLAN §6 "schema + composer core") -------------------
# S10 puts ONE line "#@include parts/00_core.py" into code.py (after its imports and VERSION, PT globals) and removes
# code.py's own includes of the common files below (a file included twice is harmless, but keep one). Order matters:
# write_pdf needs the globals VERSION and PT (mm per pt) from code.py. warn.py before text_place.py (one warning list), pdf_fonts before font_metrics, grid before text_place.
import math, zlib
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
_ENC_EXTRA = dict(_PF_EXTRA)          # pdf_str's six Turkish slots (the same table as the sheets')
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
def hex_rgb(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0)
def _f(v):
    s = "{:.3f}".format(v).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s
def pdf_str(s):
    out = bytearray()
    for ch in s:
        if ch in _ENC_EXTRA:
            out.append(_ENC_EXTRA[ch])
            continue
        try:
            b = ch.encode("cp1252")
        except Exception:
            b = b"?"
        if b in (b"\x9e",):
            b = b"?"
        out += b
    s2 = bytes(out).replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")
    return b"(" + s2 + b")"
def page_stream(pg):
    o = []
    A = o.append
    A("2.834646 0 0 2.834646 0 0 cm 1 J 1 j")
    cur = {}

    def col(c, stroke):
        k = "S" if stroke else "f"
        if cur.get(k) == c:
            return
        cur[k] = c
        r, g, b = hex_rgb(c)
        A("{} {} {} {}".format(_f(r), _f(g), _f(b), "RG" if stroke else "rg"))

    def path(pts, close):
        A("{} {} m".format(_f(pts[0][0]), _f(pts[0][1])))
        for p in pts[1:]:
            A("{} {} l".format(_f(p[0]), _f(p[1])))
        if close:
            A("h")

    def lw_dash(lw, dash, cap=1):
        A("{} w {} J 1 j [{}] 0 d".format(_f(lw), cap, " ".join(_f(d) for d in (dash or []))))

    for it in pg.items:
        kind = it[0]
        if kind == "poly":
            _, rings, fill, stroke, lw, dash, stripes, alpha = it
            if alpha is not None and alpha < 0.975:                 # see-through: an ExtGState of write_pdf
                A("q /A{:02d} gs".format(max(1, int(round(alpha * 20)))))
                cur.clear()
            if fill:
                col(fill, False)
            if stroke:
                col(stroke, True)
                lw_dash(lw, dash)
            for r in rings:
                path(r, True)
            A("B*" if fill and stroke else ("f*" if fill else "S"))
            if stripes:                       # (colour, spacing mm, width mm[, angle deg, wavy])
                sc_, sp_, w_ = stripes[:3]
                ang = math.radians(stripes[3] if len(stripes) > 3 else 45.0)
                wavy = len(stripes) > 4 and stripes[4]
                A("q")
                for r in rings:
                    path(r, True)
                A("W* n")
                col(sc_, True)
                lw_dash(w_, None, 1)
                dx_, dy_ = math.cos(ang), math.sin(ang)
                nx_, ny_ = -dy_, dx_
                allp = [p for r in rings for p in r]
                ns = [p[0] * nx_ + p[1] * ny_ for p in allp]
                ds = [p[0] * dx_ + p[1] * dy_ for p in allp]
                s_ = min(ns)
                while s_ < max(ns):
                    if wavy:
                        t_, pts_ = min(ds), []
                        while t_ <= max(ds) + 0.5:
                            o_ = s_ + sp_ * 0.22 * math.sin(t_ * 2.0 * math.pi / 3.2)
                            pts_.append((dx_ * t_ + nx_ * o_, dy_ * t_ + ny_ * o_))
                            t_ += 0.5
                        path(pts_, False)
                    else:
                        A("{} {} m {} {} l".format(_f(dx_ * min(ds) + nx_ * s_), _f(dy_ * min(ds) + ny_ * s_),
                                                   _f(dx_ * max(ds) + nx_ * s_), _f(dy_ * max(ds) + ny_ * s_)))
                    s_ += sp_
                A("S Q")
                cur.pop("S", None)
            if alpha is not None and alpha < 0.975:
                A("Q")
                cur.clear()
        elif kind == "line":
            _, pts, stroke, lw, dash, cap = it
            col(stroke, True)
            lw_dash(lw, dash, cap)
            path(pts, False)
            A("S")
        elif kind == "circle":
            _, cx, cy, r, fill, stroke, lw = it
            kk = 0.5523 * r
            if fill:
                col(fill, False)
            if stroke:
                col(stroke, True)
                lw_dash(lw, None)
            A("{} {} m".format(_f(cx + r), _f(cy)))
            for (a1, a2, a3) in (((cx + r, cy + kk), (cx + kk, cy + r), (cx, cy + r)),
                                 ((cx - kk, cy + r), (cx - r, cy + kk), (cx - r, cy)),
                                 ((cx - r, cy - kk), (cx - kk, cy - r), (cx, cy - r)),
                                 ((cx + kk, cy - r), (cx + r, cy - kk), (cx + r, cy))):
                A("{} {} {} {} {} {} c".format(_f(a1[0]), _f(a1[1]), _f(a2[0]), _f(a2[1]), _f(a3[0]), _f(a3[1])))
            A("h " + ("B" if fill and stroke else ("f" if fill else "S")))
        elif kind == "text":
            _, s, x, y, size, color, bold, align, mat, halo = it
            w = text_w(s, size, bold)
            reps = [(halo, True), (color, False)] if halo else [(color, False)]
            for c_, hal in reps:
                if hal:
                    r_, g_, b_ = hex_rgb(c_)
                    A("q {} {} {} RG {} w 1 j 1 Tr".format(_f(r_), _f(g_), _f(b_), _f(size * 0.16)))
                else:
                    col(color, False)
                    A("0 Tr")
                _text_ops(A, s, x, y, size, bold, align, mat, w)
                if hal:
                    A("Q")
    return "\n".join(o).encode("latin-1")
def write_pdf(pg, path, title):
    objs = []

    def add(b):
        objs.append(b)
        return len(objs)
    font = pdf_fonts(add, ("R", "B"))                     # G2/G3 28 Oct: Arial embedded (common/pdf_fonts.py)
    gs = [add("<< /Type /ExtGState /ca {0} /CA {0} >>".format(_f(i / 20.0)).encode("latin-1")) for i in range(1, 20)]
    gs_res = " ".join("/A{:02d} {} 0 R".format(i + 1, o_) for i, o_ in enumerate(gs))
    pages_id = add(b"")
    xo_res = ""
    if any(it[0] == "image" for it in pg.items):          # D1 a (30 Oct): raster cutouts between the vector items
        stream, xo = _wp_image_stream(pg, add)
        xo_res = " /XObject << {} >>".format(" ".join("/{} {} 0 R".format(n_, o_) for n_, o_ in xo)) if xo else ""
    else:
        stream = page_stream(pg)
    data = zlib.compress(stream, 6)
    cid = add(b"<< /Length " + str(len(data)).encode() + b" /Filter /FlateDecode >>\nstream\n" + data +
              b"\nendstream")
    kid = add("<< /Type /Page /Parent {} 0 R /MediaBox [0 0 {} {}] /Contents {} 0 R /Resources << /Font "
              "<< /F1 {} 0 R /F2 {} 0 R >> /ExtGState << {} >>{} >> >>".format(pages_id, _f(pg.W / PT), _f(pg.H / PT), cid,
                                                                                font[0], font[1], gs_res, xo_res).encode("latin-1"))
    objs[pages_id - 1] = "<< /Type /Pages /Kids [{} 0 R] /Count 1 >>".format(kid).encode("latin-1")
    cat = add("<< /Type /Catalog /Pages {} 0 R >>".format(pages_id).encode("latin-1"))
    info = add(b"<< /Title " + pdf_str(title) + b" /Producer " + pdf_str(VERSION) + b" >>")
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offs = []
    for i, b in enumerate(objs):
        offs.append(len(out))
        out += "{} 0 obj\n".format(i + 1).encode() + b + b"\nendobj\n"
    x = len(out)
    out += "xref\n0 {}\n0000000000 65535 f \n".format(len(objs) + 1).encode()
    for o_ in offs:
        out += "{:010d} 00000 n \n".format(o_).encode()
    out += "trailer\n<< /Size {} /Root {} 0 R /Info {} 0 R >>\nstartxref\n{}\n%%EOF\n".format(
        len(objs) + 1, cat, info, x).encode()
    with open(path, "wb") as fh:
        fh.write(bytes(out))


# ---- images in the page (H-B, 30 Oct 2026; D1 a: layered raster collage) ------------------------------------------
# A page item ("image", x, y, w, h, path, alpha, flip, clip) puts a PNG (with or without alpha) or a JPEG at x, y
# (lower left, page mm, y up), w x h mm (the caller keeps the proportions), alpha 0-1 or None, flip True = mirrored,
# clip None or (x0, y0, x1, y1) mm. figures.py cut_image() makes these items; section_frame.py shp_put() puts them on
# a page (pg.items). The items are drawn in their place among the vector items (the order of pg.items = the layer
# order). Pages without an image item are written exactly as before. An unreadable image is skipped (WP_IMG_LOG).
# PNG: 8 or 16 bit, grey / grey+alpha / RGB / RGBA / palette (+tRNS), not interlaced; the alpha becomes an SMask.
WP_IMG_LOG = []


def _wp_png(path):
    """(w, h, colour bytes, n colours 1|3, alpha bytes or None) of a PNG, or None"""
    import struct as _st
    with open(path, "rb") as f:
        d = f.read()
    if d[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    pos, idat, plte, trns, hdr = 8, [], None, None, None
    while pos + 8 <= len(d):
        n = _st.unpack(">I", d[pos:pos + 4])[0]
        t, c = d[pos + 4:pos + 8], d[pos + 8:pos + 8 + n]
        pos += 12 + n
        if t == b"IHDR":
            hdr = _st.unpack(">IIBBBBB", c[:13])
        elif t == b"PLTE":
            plte = c
        elif t == b"tRNS":
            trns = c
        elif t == b"IDAT":
            idat.append(c)
        elif t == b"IEND":
            break
    if not hdr:
        return None
    w, h, bd, ct, _cm, _fm, il = hdr
    ch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(ct)
    if ch is None or il or bd not in (8, 16) or (ct == 3 and bd != 8):
        return None
    bpp = ch * bd // 8
    raw = zlib.decompress(b"".join(idat))
    stride = w * bpp
    out = bytearray(h * stride)
    prev = bytearray(stride)
    i = 0
    for y in range(h):
        ft = raw[i]
        ln = bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        if ft == 1:
            for x in range(bpp, stride):
                ln[x] = (ln[x] + ln[x - bpp]) & 255
        elif ft == 2:
            for x in range(stride):
                ln[x] = (ln[x] + prev[x]) & 255
        elif ft == 3:
            for x in range(stride):
                ln[x] = (ln[x] + (((ln[x - bpp] if x >= bpp else 0) + prev[x]) >> 1)) & 255
        elif ft == 4:
            for x in range(stride):
                a = ln[x - bpp] if x >= bpp else 0
                b = prev[x]
                c = prev[x - bpp] if x >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                ln[x] = (ln[x] + (a if pa <= pb and pa <= pc else (b if pb <= pc else c))) & 255
        out[y * stride:(y + 1) * stride] = ln
        prev = ln
    if bd == 16:                                          # keep the high byte of every sample
        out = out[0::2]
    n = w * h
    if ct == 3:
        pal = bytes(plte or b"") + b"\x00" * (768 - len(plte or b""))
        rgb = bytearray(n * 3)
        for k_ in range(3):
            rgb[k_::3] = bytes(out).translate(bytes(pal[3 * j + k_] for j in range(256)))
        alpha = bytes(out).translate(bytes(trns or b"") + b"\xff" * (256 - len(trns or b""))) if trns else None
        return w, h, bytes(rgb), 3, alpha
    if ct == 0:
        return w, h, bytes(out), 1, None
    if ct == 4:
        return w, h, bytes(out[0::2]), 1, bytes(out[1::2])
    if ct == 2:
        return w, h, bytes(out), 3, None
    rgb = bytearray(n * 3)
    rgb[0::3], rgb[1::3], rgb[2::3] = out[0::4], out[1::4], out[2::4]
    alpha = bytes(out[3::4])
    return w, h, bytes(rgb), 3, (None if alpha.count(b"\xff") == n else alpha)


def _wp_jpeg(d):
    """(w, h, n colours) of a baseline / progressive JPEG, or None"""
    if d[:2] != b"\xff\xd8":
        return None
    i = 2
    while i + 9 < len(d):
        if d[i] != 0xFF:
            return None
        m = d[i + 1]
        if m in (0xC0, 0xC1, 0xC2):
            return (d[i + 7] << 8) | d[i + 8], (d[i + 5] << 8) | d[i + 6], d[i + 9]
        i += 2 + ((d[i + 2] << 8) | d[i + 3])
    return None


def _wp_image_obj(path, add):
    """the XObject id of one image file (PNG with its SMask, or JPEG), or None"""
    try:
        with open(path, "rb") as f:
            head = f.read(4)
        if head == b"\x89PNG":
            r = _wp_png(path)
            if not r:
                WP_IMG_LOG.append(u"image %s: PNG type not supported (interlaced or < 8 bit)" % path)
                return None
            w, h, col, nc, alpha = r
            sm = ""
            if alpha is not None:
                a = zlib.compress(alpha, 6)
                sid = add(("<< /Type /XObject /Subtype /Image /Width {} /Height {} /ColorSpace /DeviceGray "
                           "/BitsPerComponent 8 /Filter /FlateDecode /Length {} >>\nstream\n".format(w, h, len(a))
                           ).encode("latin-1") + a + b"\nendstream")
                sm = " /SMask {} 0 R".format(sid)
            c = zlib.compress(col, 6)
            return add(("<< /Type /XObject /Subtype /Image /Width {} /Height {} /ColorSpace /{} /BitsPerComponent 8"
                        "{} /Filter /FlateDecode /Length {} >>\nstream\n".format(
                            w, h, "DeviceRGB" if nc == 3 else "DeviceGray", sm, len(c))).encode("latin-1") + c +
                       b"\nendstream")
        with open(path, "rb") as f:
            d = f.read()
        info = _wp_jpeg(d)
        if not info:
            WP_IMG_LOG.append(u"image %s: neither PNG nor JPEG" % path)
            return None
        w, h, nc = info
        return add(("<< /Type /XObject /Subtype /Image /Width {} /Height {} /ColorSpace /{} /BitsPerComponent 8 "
                    "/Filter /DCTDecode /Length {} >>\nstream\n".format(
                        w, h, {1: "DeviceGray", 4: "DeviceCMYK"}.get(nc, "DeviceRGB"), len(d))).encode("latin-1") + d +
                   b"\nendstream")
    except Exception as ex:
        WP_IMG_LOG.append(u"image %s: %s" % (path, type(ex).__name__))
        return None


def _wp_image_stream(pg, add):
    """(content stream, [(name, id)]): runs of vector items through page_stream (each in q ... Q), the images
    between them in their order; one XObject per file"""
    class _Run(object):
        pass
    parts, run, names, xo = [], [], {}, []

    def flush():
        if run:
            r = _Run()
            r.W, r.H, r.items = pg.W, pg.H, list(run)
            parts.append(b"q\n" + page_stream(r) + b"\nQ")
            del run[:]
    for it in pg.items:
        if it[0] != "image":
            run.append(it)
            continue
        flush()
        x, y, w, h, p = it[1:6]
        alpha = it[6] if len(it) > 6 else None
        flip = it[7] if len(it) > 7 else False
        clip = it[8] if len(it) > 8 else None
        if p not in names:
            oid = _wp_image_obj(p, add)
            names[p] = None if oid is None else "Im%d" % (len(xo) + 1)
            if oid is not None:
                xo.append((names[p], oid))
        if names[p] is None or w <= 0 or h <= 0:
            continue
        ops = ["q 2.834646 0 0 2.834646 0 0 cm"]
        if alpha is not None and alpha < 0.975:
            ops.append("/A{:02d} gs".format(max(1, min(19, int(round(alpha * 20))))))
        if clip:
            ops.append("{} {} {} {} re W n".format(_f(clip[0]), _f(clip[1]), _f(clip[2] - clip[0]), _f(clip[3] - clip[1])))
        ops.append("{} 0 0 {} {} {} cm /{} Do Q".format(_f(-w if flip else w), _f(h), _f(x + w if flip else x), _f(y),
                                                       names[p]))
        parts.append(" ".join(ops).encode("latin-1"))
    flush()
    return b"\n".join(parts), xo
# ---- 10_load (composer core, round 5 S1; G-R5-12, P04.7): read every content script's items.json -------------------
#   ix_load_all(need=(), root=None, log=None) -> {folder: export}
#         reads Downloads/Bergama/cached/booklet/<folder>/items.json for every folder; a folder in `need` without a
#         readable file = HARD STOP (missing data); any other unreadable file = WARNING. Validates (ix_validate),
#         indexes every item (ix_get), runs every text through the glyph check (P04.7: a character the font lacks is a
#         WARNING and becomes "–"), logs "items <folder> <script> <version> <run>: <kinds> (<this run | earlier>)"
#   ix_validate(d, folder) -> [problem]      schema, kinds, page keys, drawing refs, units (each a WARNING)
#   ix_get(id, folder=None) -> item | None   by id (ids clash across files: "folder/id" always works)
#   ix_page(pid) -> [item]                    every item exported for page pid, in file then export order
#   ix_texts(item_or_id) -> [item]            the text items of a drawing (anchor.drawing == its id), by priority
#   ix_text(id) -> str                        the string of a text id (a plain string passes through)
#   bk_font_files() -> (regular, bold)        the SAME Arial files font_metrics measures with (pdf_fonts _pf_path); a
#                                             missing file raises FontMissing (hard stop: fonts)
BK_IX = {}            # folder -> export dict
BK_ID = {}            # id and "folder/id" -> item


def bk_font_files():
    r, b = _pf_path(_PF_FILES["R"][0]), _pf_path(_PF_FILES["B"][0])
    if not r or not b:
        raise FontMissing("Arial (arial.ttf / arialbd.ttf) not found in the Windows or user font folder: the booklet "
                          "cannot measure or set text. Install Arial.")
    return r, b


def ix_validate(d, folder):
    bad = []
    if d.get("schema") != IX_SCHEMA_R:
        bad.append(u"schema %r, expected %r" % (d.get("schema"), IX_SCHEMA_R))
    pages = d.get("pages")
    if not isinstance(pages, dict):
        return bad + [u"no pages"]
    ids = set(it.get("id") for its in pages.values() for it in its if isinstance(it, dict))
    for pid, its in pages.items():
        for it in its:
            k = it.get("kind")
            if k not in IX_KINDS_R:
                bad.append(u"%s: item %s has unknown kind %r" % (pid, it.get("id"), k))
            if not it.get("id"):
                bad.append(u"%s: an item without id (%s)" % (pid, k))
            if k == "drawing":
                e = it.get("extent") or []
                if len(e) != 4 or e[2] <= e[0] or e[3] <= e[1]:
                    bad.append(u"%s: drawing %s extent %r" % (pid, it.get("id"), e))
                if it.get("units") not in ("m", "mm"):
                    bad.append(u"%s: drawing %s units %r" % (pid, it.get("id"), it.get("units")))
            for ref in ("drawing", "parent", "child"):
                r_ = it.get(ref)
                if r_ and r_ not in ids:
                    bad.append(u"%s: %s %s names %s %r, not in this file" % (pid, k, it.get("id"), ref, r_))
            a_ = it.get("anchor")
            if isinstance(a_, dict) and a_.get("drawing") and a_["drawing"] not in ids:
                bad.append(u"%s: text %s anchored to %r, not in this file" % (pid, it.get("id"), a_["drawing"]))
    return bad


IX_SCHEMA_R = "bergama-items/1"
IX_KINDS_R = ("drawing", "text", "legend", "list", "level_column", "inset", "keymap", "photo", "chart", "source")


def ix_load_all(need=(), root=None, log=None):
    import json as _j
    lg = WN_LOG if log is None else log          # the one warning list (warn.py): it reaches the log
    BK_IX.clear()
    BK_ID.clear()
    root = root or bg_booklet("")
    names = sorted(n for n in os.listdir(root) if os.path.isdir(os.path.join(root, n))) if os.path.isdir(root) else []
    for n in need:
        if n not in names:
            names.append(n)
    for folder in names:
        p = os.path.join(root, folder, "items.json")
        if not os.path.isfile(p):
            if folder in need:
                raise RuntimeError(u"items.json of %s missing (%s): run that script first" % (folder, p))
            continue
        try:
            with open(p, encoding="utf-8") as f:
                d = _j.load(f)
        except Exception as ex:
            if folder in need:
                raise RuntimeError(u"items.json of %s unreadable (%s: %s)" % (folder, type(ex).__name__, ex))
            wn_warn(None, "load", u"%s/items.json unreadable (%s): skipped" % (folder, type(ex).__name__), lg)
            continue
        for b_ in ix_validate(d, folder):
            wn_warn(None, "load", u"%s: %s" % (folder, b_), lg)
        d["_folder"], d["_path"] = folder, p
        fresh, note = bg_this_run(p)
        BK_IX[folder] = d
        n = {}
        for pid, its in (d.get("pages") or {}).items():
            for it in its:
                it["_folder"] = folder
                n[it.get("kind")] = n.get(it.get("kind"), 0) + 1
                iid = it.get("id")
                BK_ID[u"%s/%s" % (folder, iid)] = it
                if iid in BK_ID and BK_ID[iid] is not it:
                    BK_ID[iid] = None                     # clash: only "folder/id" finds it
                elif iid not in BK_ID:
                    BK_ID[iid] = it
                if it.get("kind") == "text":
                    _ix_glyphs(it, pid, lg)
        lg.append(u"items %s %s %s %s: %s (%s)" % (folder, d.get("script"), d.get("version"), d.get("run"),
                                                   u", ".join(u"%s %d" % kv for kv in sorted(n.items())), note))
        if d.get("warnings"):
            lg.append(u"  %s logged %d content warnings in its own log" % (folder, len(d["warnings"])))
    return BK_IX


def _ix_glyphs(it, pid, lg):
    """P04.7: every character of the text must be in the font it is set in; a missing one -> WARNING + "–\""""
    s = u"%s" % it.get("string", u"")
    s2, miss = fm_safe(s, bool(it.get("bold")))
    if miss:
        wn_warn(pid, "glyph", u"%s: %s not in the font, set as %r" % (
            it.get("id"), u", ".join(u"U+%04X %s" % (ord(c), c) for c in miss), s2[:60]), lg)
        it["string"] = s2
    alt = []
    for t in it.get("short_forms") or ():
        alt.append(fm_safe(t, bool(it.get("bold")))[0])
    if alt:
        it["short_forms"] = alt


def ix_get(iid, folder=None):
    if iid is None:
        return None
    if isinstance(iid, dict):
        return iid
    if folder:
        return BK_ID.get(u"%s/%s" % (folder, iid))
    return BK_ID.get(iid) or BK_ID.get(u"%s" % iid)


def ix_page(pid):
    out = []
    for folder in sorted(BK_IX):
        out.extend(BK_IX[folder].get("pages", {}).get(pid, []))
    return out


def ix_texts(drawing):
    D = ix_get(drawing)
    if D is None:
        return []
    out = []
    for its in BK_IX.get(D.get("_folder"), {}).get("pages", {}).values():
        for it in its:
            a_ = it.get("anchor")
            if it.get("kind") == "text" and isinstance(a_, dict) and a_.get("drawing") == D["id"]:
                out.append(it)
    return sorted(out, key=lambda t: t.get("priority", 5))


def ix_text(t, folder=None):
    if t is None:
        return u""
    it = ix_get(t, folder) if not isinstance(t, dict) else t
    if it is not None and it.get("kind") == "text":
        return it.get("string", u"")
    return u"%s" % t
# ---- 20_scale (composer core, round 5 S1; G-R5-12, D2, PLAN §3 "Scales"): ONE scale list, drawing -> page mm ---------
# The Bergama list is section_frame's SF_SCALES (PLAN §3; the booklet's own STD_SCALES with 25,000-100,000 is retired),
# insets SF_INSET_SCALES (adds 1:100) at >= 2 x the parent's scale. The values are taken from section_frame.py when it
# is included, else these (the same numbers).
#   sc_size(D, den_or_f) -> (w_mm, h_mm)       the printed size of a drawing's extent
#   sc_pick(D, w, h, allowed=None, min_den=None, page=None) -> den
#         the LARGEST printed size (smallest 1:den) of D's allowed scales (its scale_pref within the list) at which
#         its extent fits w x h mm; none fits -> the smallest size on its list + WARNING "scale" (never a stop)
#   sc_pick_common(Ds, w, h, gap=4.0, stack=True, page=None) -> den
#         one scale for drawings stacked (stack=True: heights + gaps add up) or side by side (widths add up) in w x h
#         (merged pages D7, D9: four cuts at one scale, N3 = 1:500)
#   sc_factor(D, w, h, page=None) -> f          a "mm" drawing (diagram, chart, key map): the largest factor in its
#                                               fit range at which it fits; below the range -> fits anyway + WARNING
#   sc_inset_den(parent_den, D, w, h, page=None) -> den   an inset's scale: >= 2 x the parent (SF_INSET_MIN_ZOOM)
#   BkT(D, s, x, y)                              the drawing's transform onto the page: s = den ("m") or f ("mm");
#                                               (x, y) = the page mm (y DOWN) of the extent's top-left corner;
#                                               .k (page mm per drawing unit), .pt(x, y), .rect, .den (None for "mm")
# v30.3 (Aras 2 Nov 06:20, decision card): the booklet's own round list adds 1:1,500, 1:7,500, 1:15,000 (and 1:25,000
# for the whole-survey plans that overran A3 at 1:20,000), so a map no longer halves in size between two list steps.
# Only maps and sections take a list scale and print it; diagrams, charts and the axo take any size (Aras 06:24
# "diagrams can be at different scales ... dont write scales to diagrams, just maps").
BK_SCALES = (200, 250, 500, 1000, 1500, 2000, 2500, 5000, 7500, 10000, 15000, 20000, 25000, 50000)  # 50,000: p19 farms map in the right column
BK_INSET_SCALES = (100,) + BK_SCALES
BK_MM_MAX = 6.0            # v30.3: a scale-free drawing may grow to 6 x its exported size (was 2 x), room permitting
BK_INSET_ZOOM = 2.0


def _sc_ext(D):
    e = D["extent"]
    return float(e[2]) - float(e[0]), float(e[3]) - float(e[1])


def sc_size(D, s):
    ew, eh = _sc_ext(D)
    k = (1000.0 / float(s)) if D.get("units", "m") == "m" else float(s)
    return ew * k, eh * k


def _sc_allowed(D, allowed=None, inset=False):
    lst = BK_INSET_SCALES if inset else BK_SCALES
    want = allowed or D.get("scale_pref") or lst
    want = [int(v) for v in want]
    if not allowed and want:                 # v30.3: a script's scale_pref is a RANGE on the booklet's list, so the
        lo, hi = min(want), max(want)        # in-between round scales are open to it; 1:20,000 maps may go 1:25,000
        if hi >= 20000:
            hi = max(lst)
        out = sorted(v for v in lst if lo <= v <= hi)
    else:
        out = sorted(v for v in want if v in lst)
    return out or list(lst)


def sc_pick(D, w, h, allowed=None, min_den=None, page=None):
    al = _sc_allowed(D, allowed)
    for den in al:
        if min_den and den < min_den:
            continue
        dw, dh = sc_size(D, den)
        if dw <= w + 1e-6 and dh <= h + 1e-6:
            return den
    den = al[-1]
    dw, dh = sc_size(D, den)
    wn_warn(page or D.get("page"), "scale", u"%s does not fit %.0f x %.0f mm at any of 1:%s; set at 1:%d (%.0f x %.0f mm)"
            % (D.get("id"), w, h, u", 1:".join(str(v) for v in al), den, dw, dh))
    return den


def sc_pick_common(Ds, w, h, gap=4.0, stack=True, page=None):
    al = sorted(set.intersection(*[set(_sc_allowed(D)) for D in Ds])) if Ds else list(BK_SCALES)
    al = al or list(BK_SCALES)
    for den in al:
        sz = [sc_size(D, den) for D in Ds]
        if stack:
            ok = max(s[0] for s in sz) <= w + 1e-6 and sum(s[1] for s in sz) + gap * (len(sz) - 1) <= h + 1e-6
        else:
            ok = max(s[1] for s in sz) <= h + 1e-6 and sum(s[0] for s in sz) + gap * (len(sz) - 1) <= w + 1e-6
        if ok:
            return den
    wn_warn(page, "scale", u"%s do not fit %.0f x %.0f mm together at any common scale; set at 1:%d" % (
        u", ".join(D.get("id", u"?") for D in Ds), w, h, al[-1]))
    return al[-1]


def sc_factor(D, w, h, page=None, hi_max=None):
    ew, eh = _sc_ext(D)
    f = min(w / ew, h / eh)
    lo, hi = (D.get("fit") or (0.5, 2.0))[:2]
    hi = max(float(hi), BK_MM_MAX if hi_max is None else float(hi_max))
    if f > hi:
        return float(hi)
    if f < lo:
        wn_warn(page or D.get("page"), "scale", u"%s needs x%.2f to fit %.0f x %.0f mm, below its x%.2f minimum" % (
            D.get("id"), f, w, h, lo))
    return f


def sc_inset_den(parent_den, D, w, h, page=None):
    al = [d for d in _sc_allowed(D, inset=True) if d * BK_INSET_ZOOM <= parent_den + 1e-6]
    if not al:
        wn_warn(page or D.get("page"), "scale", u"inset %s: no scale >= %.0f x the parent's 1:%d" % (
            D.get("id"), BK_INSET_ZOOM, parent_den))
        al = [min(BK_INSET_SCALES)]
    for den in al:
        dw, dh = sc_size(D, den)
        if dw <= w + 1e-6 and dh <= h + 1e-6:
            return den
    wn_warn(page or D.get("page"), "scale", u"inset %s does not fit %.0f x %.0f mm at any inset scale >= 2 x 1:%d; "
            u"set at 1:%d" % (D.get("id"), w, h, parent_den, al[-1]))
    return al[-1]


class BkT(object):
    """drawing units (y up) -> page mm (y down); see the part notes"""
    def __init__(self, D, s, x, y):
        self.D = D
        self.e = [float(v) for v in D["extent"]]
        self.den = int(s) if D.get("units", "m") == "m" else None
        self.k = (1000.0 / float(s)) if self.den else float(s)
        self.x, self.y = float(x), float(y)
        self.w, self.h = (self.e[2] - self.e[0]) * self.k, (self.e[3] - self.e[1]) * self.k
        self.rect = (self.x, self.y, self.x + self.w, self.y + self.h)

    def pt(self, x, y):
        return self.x + (float(x) - self.e[0]) * self.k, self.y + (self.e[3] - float(y)) * self.k

    def ry(self, y):
        return self.y + (self.e[3] - float(y)) * self.k
# ---- 30_render (composer core, round 5 S1; G-R5-12): an exported drawing drawn on the booklet page at its scale -------
# The drawing's layers (in z order, then export order) become one small vector PDF of exactly the drawing's printed
# size (the common write_pdf: polygons with holes, lines, circles, see-through, images), which is then set on the page
# 1:1 with PyMuPDF show_pdf_page: geometry is scaled from drawing units to page mm, line widths and dashes stay PRINT
# sizes (never scaled, unlike xform), and the page box clips everything outside the extent. No text is drawn here:
# every text is a text item set by 40_set / 50_place (a "text" shape left in a layer is a WARNING and is skipped).
#   rd_drawing(P, D, T, frame=None) -> placed     draws D with transform T (20_scale BkT) on BkPage P; registers the
#                                                 drawing rect as a TextPage block + keep (kind "drawing", name = its
#                                                 id: only its own labels may sit on it) and its keep_areas as keeps;
#                                                 placed = dict(D, T, rect, den, id) also kept in P.placed
#                                                 frame = None | (colour, width_pt): a thin frame round the rect (insets)
#   rd_close()                                    closes the temporary PDFs (after the booklet is saved)
# Temporary files: Downloads/Bergama/cached/booklet/_render/<page>_<id>.pdf (overwritten each run).
# v31 (round 6 S9, G6-9 "every element its own group inside its kind group inside its drawing group"): each shape's
# "grp" ("<kind>/<element id>", common/item_export.py §2.8) is handed to write_pdf as pg.grp, a list parallel to
# pg.items (None = untagged), with pg.grp_root = the drawing id; write_pdf (S2) writes drawing > kind > element as
# nested groups. The drawing PDF is then set on the page as one Form XObject (show_pdf_page) = the drawing's group.
# Counts per page go to BK_GRP (log "groups <page> kinds=<n> elements=<n> untagged=<n>", 82_compose).
BK_K = 72.0 / 25.4          # pt per mm
RD_DOCS = []
BK_GRP = {}                 # page -> dict(kinds=set, elements=set, untagged=n)    (G6-9 log line)


class _RdPg(object):
    pass


def _rd_img_path(f):
    if not f:
        return f
    if os.path.isabs(f):
        return f
    for base in (os.path.join(BERGAMA_ROOT, "Data"), BERGAMA_ROOT):
        p = os.path.join(base, f)
        if os.path.isfile(p):
            return p
    return f


def rd_items(D, T, page=None, grp=None):
    """D's shapes as write_pdf page items in mm, y up from the drawing's lower-left corner; grp (a list) gets each
    item's "grp" tag (G6-9), parallel to the items"""
    e, k = T.e, T.k
    mm = 25.4 / 72.0

    def P(p):
        return ((float(p[0]) - e[0]) * k, (float(p[1]) - e[1]) * k)
    out, skipped = [], 0
    for L in sorted(D.get("layers") or [], key=lambda L: L.get("z", 0)):
        for s in L.get("shapes") or []:
            n0 = len(out)
            t = s.get("t") or s.get("type")         # Ix writes "t", the key-map module (S2) "type"
            if t == "poly":
                rings = [[P(p) for p in r] for r in s.get("rings") or [] if len(r) >= 3]
                if rings and (s.get("fill") or s.get("stroke")):
                    out.append(("poly", rings, s.get("fill"), s.get("stroke"), (s.get("width_pt") or 0.0) * mm,
                                [v * mm for v in s["dash_pt"]] if s.get("dash_pt") else None, None, s.get("opacity")))
            elif t == "line":
                pts = [P(p) for p in s.get("pts") or []]
                if len(pts) >= 2 and s.get("stroke"):
                    out.append(("line", pts, s["stroke"], (s.get("width_pt") or 0.25) * mm,
                                [v * mm for v in s["dash_pt"]] if s.get("dash_pt") else None, s.get("cap", 1)))
            elif t == "circle":
                cx, cy = P(s["c"])
                r = s["r_mm"] if s.get("r_mm") is not None else float(s.get("r") or 0.0) * k
                if r > 0 and (s.get("fill") or s.get("stroke")):
                    out.append(("circle", cx, cy, r, s.get("fill"), s.get("stroke"), (s.get("width_pt") or 0.0) * mm))
            elif t == "image":
                b = s.get("box") or [0, 0, 0, 0]
                x0, y0 = P(b[:2])
                x1, y1 = P(b[2:4])
                c = s.get("clip")
                clip = None
                if c:
                    cx0, cy0 = P(c[:2])
                    cx1, cy1 = P(c[2:4])
                    clip = (min(cx0, cx1), min(cy0, cy1), max(cx0, cx1), max(cy0, cy1))
                out.append(("image", min(x0, x1), min(y0, y1), abs(x1 - x0), abs(y1 - y0), _rd_img_path(s.get("file")),
                            s.get("opacity"), bool(s.get("flip")), clip))
            elif t == "text":
                skipped += 1
            if grp is not None and len(out) > n0:
                grp.append(wp_grp_of(s) if "wp_grp_of" in globals() else (s.get("grp") or L.get("grp")))
    if skipped:
        wn_warn(page or D.get("page"), "text", u"%s: %d text shape(s) inside its layers not drawn (texts are items: "
                u"Ix.layer turns them into labels)" % (D.get("id"), skipped))
    return out


def rd_drawing(P, D, T, frame=None):
    import fitz as _fz
    pg = _RdPg()
    pg.W, pg.H = T.w, T.h
    did = u"%s" % D.get("id")
    pg.grp = []
    pg.items = rd_items(D, T, P.pid, pg.grp)
    pg.grp_root = did
    pg.page = P.pid                                 # write_pdf's per-page group counts (wp_groups_log, S2)
    st_ = BK_GRP.setdefault(P.pid, dict(kinds=set(), elements=set(), untagged=0))
    for g_ in pg.grp:
        if g_:
            st_["kinds"].add(u"%s" % g_.split(u"/")[0])
            st_["elements"].add(u"%s|%s" % (did, g_))
        else:
            st_["untagged"] += 1
    d_ = bg_booklet("_render")
    os.makedirs(d_, exist_ok=True)
    fn = os.path.join(d_, u"%s_%s.pdf" % (P.pid, "".join(c if c.isalnum() or c in "-_" else "_" for c in did)))
    placed = dict(D=D, T=T, rect=T.rect, den=T.den, id=did)
    if pg.items and pg.W > 0.01 and pg.H > 0.01:
        write_pdf(pg, fn, did)
        src = _fz.open(fn)
        RD_DOCS.append(src)
        r = T.rect
        P.page.show_pdf_page(_fz.Rect(r[0] * BK_K, r[1] * BK_K, r[2] * BK_K, r[3] * BK_K), src, 0)
        if "WP_IMG_LOG" in globals():
            for ln in WP_IMG_LOG:
                wn_warn(P.pid, "image", u"%s: %s" % (did, ln))
            del WP_IMG_LOG[:]
    else:
        wn_warn(P.pid, "drawing", u"%s has nothing to draw (no shapes or zero size)" % did)
    if frame:
        bk_rect(P, T.rect, None, frame[0], frame[1])
    P.tp.block(T.rect, did)
    P.tp.keep(T.rect, "drawing", did)
    for K_ in D.get("keep_areas") or []:
        if isinstance(K_, dict):
            pts, kk, nm = [T.pt(p[0], p[1]) for p in K_.get("pts") or []], K_.get("kind") or "keep", K_.get("name")
        else:                                   # a box [x0, y0, x1, y1] (the key-map module's form)
            e_ = T.e
            if (K_[2] - K_[0]) * (K_[3] - K_[1]) >= 0.95 * (e_[2] - e_[0]) * (e_[3] - e_[1]):
                continue                        # the whole frame: already the drawing's own keep (its labels may enter)
            a_, b_ = T.pt(K_[0], K_[3]), T.pt(K_[2], K_[1])
            pts, kk, nm = [a_, (b_[0], a_[1]), b_, (a_[0], b_[1])], "keep", None
        if len(pts) >= 3:
            P.tp.keep(pts, kk, u"%s:%s" % (did, nm or "keep"))
    P.placed.append(placed)
    P.ink.append(("drawing", T.rect, did))
    return placed


def bk_rect(P, r, fill=None, stroke=None, width_pt=0.5, dash=None):
    """a rectangle on the page (page mm, y down); colours hex"""
    import fitz as _fz
    sh = P.page.new_shape()
    sh.draw_rect(_fz.Rect(r[0] * BK_K, r[1] * BK_K, r[2] * BK_K, r[3] * BK_K))
    sh.finish(color=hex_rgb(stroke) if stroke else None, fill=hex_rgb(fill) if fill else None,
              width=width_pt, dashes=("[%s] 0" % " ".join("%g" % d for d in dash)) if dash else None)
    sh.commit()


def bk_line(P, pts, stroke, width_pt=0.5, dash=None):
    """a polyline on the page (page mm, y down)"""
    import fitz as _fz
    sh = P.page.new_shape()
    sh.draw_polyline([_fz.Point(x * BK_K, y * BK_K) for x, y in pts])
    sh.finish(color=hex_rgb(stroke), width=width_pt, closePath=False,
              dashes=("[%s] 0" % " ".join("%g" % d for d in dash)) if dash else None)
    sh.commit()


def bk_poly(P, pts, fill=None, stroke=None, width_pt=0.5):
    """a closed polygon on the page (page mm, y down)"""
    import fitz as _fz
    sh = P.page.new_shape()
    sh.draw_polyline([_fz.Point(x * BK_K, y * BK_K) for x, y in pts])
    sh.finish(color=hex_rgb(stroke) if stroke else None, fill=hex_rgb(fill) if fill else None, width=width_pt,
              closePath=True)
    sh.commit()


def rd_close():
    for d in RD_DOCS:
        try:
            d.close()
        except Exception:
            pass
    del RD_DOCS[:]
# ---- 40_set (composer core, round 5 S1; G-R5-2, D1, C8, C12): the text setter -----------------------------------------
# Every paragraph, list text and caption is JUSTIFIED with its LAST line LEFT (refs/U29 sketch); single lines stay left.
# Widths are real Arial (font_metrics, the same files the page embeds: 10_load bk_font_files). Sizes start at the
# role's size (grid.py GRID_ROLE_PT) and step down 0.25 pt until the text fits its box, never below GRID_MIN_PT
# (4.0 pt, D1); what still does not fit is a WARNING "overrun" and is set at 4 pt running past its box (the layout
# check reports the edge). No widows: the last line keeps >= 2 words (tp_wrap pulls words down; when that fails at
# this size the next smaller size is tried; at 4 pt a WARNING "widow"). Words are placed one by one at their
# justified x, so no PDF word spacing is needed (PyMuPDF writes Identity-H text, where Tw does not apply).
# C8 (round 4: a renumbered source mark squeezed to 6 pt "may touch the next word"): marks are now ordinary text in
# their paragraph, set and measured with it; nothing is squeezed into a frozen sheet layout.
#   st_lines(text, w, pt, bold=False, justify=True) -> [line]   line = dict(words=[(s, bold, x_mm)], width, last)
#         paragraphs split at "\n"; "*word*" bold; x_mm already justified (last line of each paragraph left)
#   st_fit(text, w, h, role="intro", pt=None, bold=None, lead=None, justify=True, min_pt=None) ->
#         (lines, pt, lead_mm, height_mm)      the largest size <= pt at which the text fits w x h mm (h None = any)
#   st_para(P, text, x, y, w, h=None, role="intro", pt=None, bold=None, colour=None, justify=True, name=None,
#           allow=(), group=None, page=None) -> (height_mm, pt)
#         sets a paragraph block with its TOP at y (page mm, y down) into P's TextPage (drawn by bk_emit at the end)
#   st_line(P, s, x, y, pt, bold=False, colour=None, align="L", role="label", name=None, allow=(), group=None)
#         one line, baseline at y (no wrapping), through the TextPage
#   bk_emit(P) -> n                            draws every text of the page (TextPage.emit) with the page's fonts
#   ST_COUNT                                   dict(justified=n paragraphs justified, lines=n): log "text justified n"
ST_COUNT = dict(justified=0, lines=0, paras=0)


def st_lines(text, w, pt, bold=False, justify=True, min_last_words=2):
    """see the part notes; raises TpWidow when the last-line rule cannot hold at this size"""
    sp = fm_width(u" ", pt, False)
    out = []
    for para in (u"%s" % text).split(u"\n"):
        if not para.strip():
            out.append(dict(words=[], width=0.0, last=True))
            continue
        lines = tp_wrap(para, w, pt, bold, min_last_words, True)
        lines = [ln for ln in lines if ln]
        for i, ln in enumerate(lines):
            words, x = [], 0.0
            for s, b, xo in ln:                       # a run: words of one weight; xo = where the run starts
                x = xo
                for j, wd in enumerate(s.split(u" ")):
                    if j > 0:
                        x += sp
                    words.append([wd, b, x])
                    x += fm_width(wd, pt, b)
            # the extra space goes only into real word spaces: a word glued to the one before (a bold word and its
            # comma, two runs without a space) keeps its place relative to it
            nat = x
            last = (i == len(lines) - 1)
            gaps = []
            for k in range(1, len(words)):
                prev_end = words[k - 1][2] + fm_width(words[k - 1][0], pt, words[k - 1][1])
                gaps.append(words[k][2] - prev_end > 1e-6)
            n_sp = sum(1 for g in gaps if g)
            if justify and not last and n_sp > 0 and nat < w:
                extra = (w - nat) / float(n_sp)
                add = 0.0
                for k in range(1, len(words)):
                    if gaps[k - 1]:
                        add += extra
                    words[k][2] += add
                ST_COUNT["lines"] += 1
            out.append(dict(words=[(s_, b_, xo_) for s_, b_, xo_ in words],
                            width=(w if justify and not last and n_sp and nat < w else nat), last=last))
    return out


def st_fit(text, w, h, role="intro", pt=None, bold=None, lead=None, justify=True, min_pt=None, page=None):
    p0, b0, ld0, _c = grid_role(role)
    pt = float(pt or p0)
    bold = b0 if bold is None else bool(bold)
    lo = float(min_pt or GRID_MIN_PT)
    lines, used = None, pt
    s = pt
    while True:
        lead_mm = (lead / pt * s) if lead else s * ld0 * GRID_PT
        try:
            lines = st_lines(text, w, s, bold, justify)
            hh = _st_height(lines, s, lead_mm, bold)
            if h is None or hh <= h + 1e-6:
                return lines, s, lead_mm, hh
        except TpWidow:
            pass
        if s - 0.25 < lo - 1e-6:
            break
        s -= 0.25
    s = lo
    lead_mm = (lead / pt * s) if lead else s * ld0 * GRID_PT
    try:
        lines = st_lines(text, w, s, bold, justify)
    except TpWidow as ex:
        wn_warn(page, "widow", u"%r: %s (set without the last-line rule)" % (grid_plain(text)[:50], ex))
        lines = st_lines(text, w, s, bold, justify, 1)
    hh = _st_height(lines, s, lead_mm, bold)
    if h is not None and hh > h + 1e-6:
        wn_warn(page, "overrun", u"%r needs %.1f mm at %.1f pt, %.1f mm free: cut the text or give it room" % (
            grid_plain(text)[:50], hh, s, h))
    return lines, s, lead_mm, hh


def _st_height(lines, pt, lead_mm, bold):
    if not lines:
        return 0.0
    a, d = fm_asc_desc(pt, bold)
    return a + (len(lines) - 1) * lead_mm - d


def st_para(P, text, x, y, w, h=None, role="intro", pt=None, bold=None, colour=None, justify=True, name=None,
            allow=(), group=None, page=None, lead=None):
    p0, b0, _ld, c0 = grid_role(role)
    bold = b0 if bold is None else bool(bold)
    lines, s, lead_mm, hh = st_fit(text, w, h, role, pt, bold, lead, justify, page=page or P.pid)
    a, _d = fm_asc_desc(s, bold)
    g = group or P.tp._group()
    yy = y + a
    for ln in lines:
        for wd, b, xo in ln["words"]:
            if wd:
                P.tp.put(wd, x + xo, yy, s, b, "L", 0.0, name, role, colour or c0, allow, g)
        yy += lead_mm
    ST_COUNT["paras"] += 1
    if justify and len([l for l in lines if l["words"]]) > 1:
        ST_COUNT["justified"] += 1
    return hh, s


def st_line(P, s, x, y, pt, bold=False, colour=None, align="L", role="label", name=None, allow=(), group=None,
            angle=0.0):
    return P.tp.put(s, x, y, pt, bold, align, angle, name, role, colour or GRID_INK["ink"], allow, group)


def bk_emit(P):
    """every text of the page drawn with the page's embedded Arial (the files it was measured with)"""
    import fitz as _fz
    if not getattr(P, "_fonts", False):
        r, b = bk_font_files()
        P.page.insert_font(fontname="BKR", fontfile=r)
        P.page.insert_font(fontname="BKB", fontfile=b)
        P._fonts = True

    def draw(it):
        s, pt, bold = it["text"], it["pt"], it["bold"]
        w = fm_width(s, pt, bold)
        al = str(it.get("align") or "L").upper()
        x, y = it["x"], it["y"]
        if al in ("MC", "CM"):
            ix0, iy0, ix1, iy1 = fm_ink_box(s, pt, bold)
            dx, y = -w / 2.0, y + (iy0 + iy1) / 2.0
        else:
            dx = {"L": 0.0, "C": -w / 2.0, "R": -w}.get(al[:1], 0.0)
        col = hex_rgb(it.get("colour") or GRID_INK["ink"])
        ang = float(it.get("angle") or 0.0)
        if abs(ang) > 0.01:
            import math as _m
            t = _m.radians(ang)
            pp = _fz.Point((x + dx * _m.cos(t)) * BK_K, (y - dx * _m.sin(t)) * BK_K)
            P.page.insert_text(pp, s, fontname="BKB" if bold else "BKR", fontsize=pt, color=col,
                               morph=(pp, _fz.Matrix(-ang)))
        else:
            P.page.insert_text(_fz.Point((x + dx) * BK_K, y * BK_K), s, fontname="BKB" if bold else "BKR",
                               fontsize=pt, color=col)
    return P.tp.emit(draw)
# ---- 50_place (composer core, round 5 S1; G-R5-12 "prevent, not just detect", G-R5-2, G-R5-10, PLAN §3) -------------
# Everything that belongs to a drawing is placed by the booklet, after the drawing, in priority order: in-drawing
# labels, level column, legend, lists, notes. A label tries (1) its exported positions round its anchor, (2) nearby
# free spots on rings (text_place TP_RINGS), (3) its short forms the same way, (4) a number on the point + a row in the
# drawing's side list, (5) smaller sizes down to 4 pt; only then a WARNING and its first position. A label never
# crosses its drawing's window (G-R5-10 "no half labels"): spots that would are not taken.
#   pl_label(P, it, placed, side=None, window=None) -> TextPage item
#   pl_labels(P, placed, side=None, roles=("label", "badge")) -> n     every anchored text of the drawing, by priority
#   pl_side_rows(P, side, x, y, w, h=None) -> height                    closes the side list, sets its numbered rows
#   pl_legend(P, lg, x, y, w, h=None, max_cols=2) -> box                swatches + justified texts in columns
#   pl_list(P, ls, x, y, w, h=None) -> box                              numbered / bulleted rows
#   pl_levels(P, lc, placed, side=None) -> n                            level markers (Aras's sketch U04) beside the
#                                                                       drawing, values "+43.71"; labels spread >= 0.8 mm
#   pl_scalebar(P, placed, x=None, y=None, max_mm=30.0) -> box           beside its drawing (default under its left end)
#   pl_inset(P, ins, parent, x, y, w, h) -> placed                      the zoom at >= 2 x the parent, framed; the
#                                                                       window drawn on the parent
#   pl_mm_drawing(P, D, texts, x, y, w, h, align="C") -> placed         a scale-free drawing (key map from the S2
#                                                                       module, diagram, chart) fitted into a box + its texts
#   pl_photo(P, ph, x, y, w, h) -> box                                  a photo kept rectangular, never stretched
# Every placed thing is a TextPage text, block or keep, so 70_check sees it.
PL_LEVEL = dict(gap=3.0, dash=(3.5, 0.8, 0.8, 0.8, 3.1), tri_w=2.2, tri_h=1.4, lw=0.5, label_gap=0.8, clear=0.8,
                ink="4A3F35")          # PLAN §3 level marker (refs/U04): mm, line width pt
PL_SW = dict(w=4.0, h=2.4, gap=1.4, row_gap=0.8)     # legend swatch (mm)


def _pl_codes(pos):
    out = []
    for c in pos or TP_POSITIONS:
        if isinstance(c, str) and c.startswith("="):
            out.append((0.0, 0.0, c[1:] or "L"))
        elif isinstance(c, (list, tuple)):
            out.append(tuple(c))
        else:
            out.append(c)
    return out


def _pl_apt(it):
    """a text item's anchor point in its drawing's units: anchor.pt (Ix) or anchor.point (key-map module, S2)"""
    a_ = it.get("anchor") or {}
    if not isinstance(a_, dict):
        return None
    p_ = a_.get("pt")
    return p_ if p_ is not None else a_.get("point")


def _pl_inside(b, win):
    return win is None or (win[0] <= b[0] + 1e-6 and b[2] <= win[2] + 1e-6 and win[1] <= b[1] + 1e-6 and
                           b[3] <= win[3] + 1e-6)


def _pl_try(P, t, anchor, codes, pt, bold, allow, win, d=0.8):
    tp = P.tp
    for code in codes:
        x, y, al = tp._at(code, t, anchor, pt, bold, d)
        b = tp._box(t, x, y, pt, bold, al, 0.0)
        if _pl_inside(b, win) and tp._free(b, allow):
            return x, y, al
    for x, y, al in tp._ring_spots(t, anchor, pt, bold, d, TP_RINGS):
        b = tp._box(t, x, y, pt, bold, al, 0.0)
        if _pl_inside(b, win) and tp._free(b, allow):
            return x, y, al
    return None


def pl_label(P, it, placed, side=None, window=None):
    a_ = _pl_apt(it)
    if a_ is None:
        return None
    T = placed["T"]
    anchor = T.pt(a_[0], a_[1])
    win = window or placed["rect"]
    allow = (placed["id"],)
    texts = [it.get("string", u"")] + list(it.get("short_forms") or [])
    texts = [t for t in texts if t]
    if not texts:
        return None
    pt0 = float(it.get("size_pt") or grid_role(it.get("role", "label"))[0])
    lo = max(float(it.get("min_pt") or GRID_MIN_PT), GRID_MIN_PT)
    bold, col, role = bool(it.get("bold")), it.get("colour"), it.get("role", "label")
    codes = _pl_codes(it.get("positions"))
    for t in texts:
        got = _pl_try(P, t, anchor, codes, pt0, bold, allow, win)
        if got:
            P.tp.put(t, got[0], got[1], pt0, bold, got[2], 0.0, it.get("id"), role, col, allow)
            return P.tp.items[-1]
    if side is not None and it.get("side_list_ok", True):
        P.tp.put(u"0", anchor[0], anchor[1], pt0, True, "MC", 0.0, it.get("id"), "number", col, allow + ("marker",))
        num = P.tp.items[-1]
        side.add(anchor, texts[0], num)
        if side not in P.tp.sides:
            P.tp.sides.append(side)
        return num
    p_ = pt0 - 0.5
    while p_ >= lo - 1e-6:
        for t in texts:
            got = _pl_try(P, t, anchor, codes, p_, bold, allow, win)
            if got:
                P.tp.put(t, got[0], got[1], p_, bold, got[2], 0.0, it.get("id"), role, col, allow)
                return P.tp.items[-1]
        p_ -= 0.5
    wn_warn(P.pid, "overlap", u"label %r of %s: no free spot inside its drawing down to %.1f pt and no side list: set at "
            u"its first position" % (texts[0], placed["id"], lo))
    x, y, al = P.tp._at(codes[0] if codes else "E", texts[-1], anchor, lo, bold, 0.8)
    P.tp.put(texts[-1], x, y, lo, bold, al, 0.0, it.get("id"), role, col, allow, forced=True)
    return P.tp.items[-1]


def pl_rigid(P, placed, s, roles=None):
    """v30.3 (2 Nov run: diagram texts on top of each other): a scale-free drawing (diagram, chart, key map, axo) keeps
    its texts exactly where its script set them, scaled WITH the drawing (size x s, offsets x s), never moved to a free
    spot or numbered into a side list: the script designed them together, so they only collide if the script's own
    design does. Floor GRID_MIN_PT (D1); below it the layout gives the drawing more room instead."""
    T = placed["T"]
    n = 0
    for it in sorted(ix_texts(placed["D"]), key=lambda t: t.get("priority", 5)):
        if roles and it.get("role") not in roles:
            continue
        a_ = _pl_apt(it)
        t = it.get("string", u"")
        if a_ is None or not t:
            continue
        anchor = T.pt(a_[0], a_[1])
        pt0 = float(it.get("size_pt") or grid_role(it.get("role", "label"))[0])
        pt = max(GRID_MIN_PT, pt0 * s)
        c = (_pl_codes(it.get("positions")) or ["E"])[0]
        if not isinstance(c, str):
            c = (c[0] * s, c[1] * s, c[2])
        x, y, al = P.tp._at(c, t, anchor, pt, bool(it.get("bold")), 0.8 * s)
        P.tp.put(t, x, y, pt, bool(it.get("bold")), al, 0.0, it.get("id"), it.get("role", "label"), it.get("colour"),
                 (placed["id"],), forced=True)
        n += 1
    return n


def pl_labels(P, placed, side=None, roles=("label", "badge")):
    n = 0
    for it in ix_texts(placed["D"]):
        if it.get("role") in roles and _pl_apt(it) is not None:
            if pl_label(P, it, placed, side):
                n += 1
    return n


def pl_side_rows(P, side, x, y, w, h=None):
    """closes the side list (numbers in reading order) and sets its rows "n  text" from (x, y) down"""
    rows = side.close(P.tp)
    yy = y
    for n, t in rows:
        P.tp.put(u"%d" % n, x, yy + fm_asc_desc(grid_role("list_item")[0], True)[0], grid_role("list_item")[0], True,
                 "L", 0.0, None, "list_item", None, ())
        hh, _s = st_para(P, t, x + 4.0, yy, w - 4.0, None if h is None else max(0.0, y + h - yy), "list_item")
        yy += hh + 0.8
    if h is not None and yy - y > h + 1e-6:
        wn_warn(P.pid, "overrun", u"side list %s needs %.1f mm, %.1f mm free" % (side.name, yy - y, h))
    return yy - y


def _pl_swatch(P, sw, x, y):
    """one legend swatch in the box (x, y) .. (x + w, y + h) (page mm, y down)"""
    W, H = PL_SW["w"], PL_SW["h"]
    k = (sw or {}).get("kind", "fill")
    col = sw.get("colour") or sw.get("fill") or GRID_INK["ink"]
    if k == "fill":
        bk_rect(P, (x, y, x + W, y + H), col, sw.get("stroke"), sw.get("width_pt") or 0.3)
    elif k in ("line", "dash"):
        bk_line(P, [(x, y + H / 2.0), (x + W, y + H / 2.0)], col, sw.get("width_pt") or 1.0,
                sw.get("dash_pt") or ((2.0, 1.2) if k == "dash" else None))
    elif k == "dot":
        import fitz as _fz
        sh = P.page.new_shape()
        sh.draw_circle(_fz.Point((x + W / 2.0) * BK_K, (y + H / 2.0) * BK_K), min(W, H) * 0.35 * BK_K)
        sh.finish(color=hex_rgb(sw.get("stroke")) if sw.get("stroke") else None, fill=hex_rgb(col),
                  width=sw.get("width_pt") or 0.3)
        sh.commit()
    elif k == "image" and sw.get("file"):
        import fitz as _fz
        try:
            P.page.insert_image(_fz.Rect(x * BK_K, y * BK_K, (x + W) * BK_K, (y + H) * BK_K),
                                filename=_rd_img_path(sw["file"]), keep_proportion=True)
        except Exception as ex:
            wn_warn(P.pid, "image", u"legend swatch %s: %s" % (sw.get("file"), type(ex).__name__))
    P.tp.keep((x, y, x + W, y + H), "swatch", None)


def pl_legend(P, lg, x, y, w, h=None, max_cols=2):
    """the legend in columns (filled top to bottom), one size for every entry (stepped down together)"""
    ents = [(e.get("swatch") or {}, ix_text(e.get("text"), lg.get("_folder"))) for e in lg.get("entries") or []]
    title = ix_text(lg.get("title"), lg.get("_folder")) if lg.get("title") else None
    cols = max(1, min(int(max_cols), int((w + 4.0) // 40.0) or 1))
    cw = (w - 4.0 * (cols - 1)) / float(cols)
    tw = cw - PL_SW["w"] - PL_SW["gap"]
    pt0 = grid_role("legend")[0]
    s = pt0
    while True:
        hs = [st_fit(t, tw, None, "legend", s, justify=True, page=P.pid)[3] for _sw, t in ents]
        hs = [max(hh, PL_SW["h"]) + PL_SW["row_gap"] for hh in hs]
        th = (st_fit(title, w, None, "heading", page=P.pid)[3] + 1.2) if title else 0.0
        per = -(-len(hs) // cols) if hs else 0
        colh = [sum(hs[i * per:(i + 1) * per]) for i in range(cols)]
        need = th + (max(colh) if colh else 0.0)
        if h is None or need <= h + 1e-6 or s - 0.25 < GRID_MIN_PT - 1e-6:
            break
        s -= 0.25
    if h is not None and need > h + 1e-6:
        wn_warn(P.pid, "overrun", u"legend %s needs %.1f mm at %.1f pt, %.1f mm free" % (lg.get("id"), need, s, h))
    yy = y
    if title:
        hh, _p = st_para(P, title, x, yy, w, None, "heading", page=P.pid)
        yy += hh + 1.2
    g = P.tp._group()
    for i, ((sw, t), hh) in enumerate(zip(ents, hs)):
        c = i // per if per else 0
        r0 = yy + sum(hs[c * per:i])
        cx = x + c * (cw + 4.0)
        _pl_swatch(P, sw, cx, r0)
        st_para(P, t, cx + PL_SW["w"] + PL_SW["gap"], r0, tw, None, "legend", s, group=g, page=P.pid)
    box = (x, y, x + w, y + need)
    P.tp.block(box, u"legend %s" % lg.get("id"))
    return box


def pl_list(P, ls, x, y, w, h=None):
    """numbered (or bulleted) rows; texts justified; one size for all rows"""
    rows = [ix_text(t, ls.get("_folder")) for t in ls.get("items") or []]
    numbered = ls.get("numbered", True)
    ind = 4.0
    s = grid_role("list_item")[0]
    while True:
        hs = [st_fit(t, w - ind, None, "list_item", s, page=P.pid)[3] + 0.8 for t in rows]
        if h is None or sum(hs) <= h + 1e-6 or s - 0.25 < GRID_MIN_PT - 1e-6:
            break
        s -= 0.25
    if h is not None and sum(hs) > h + 1e-6:
        wn_warn(P.pid, "overrun", u"list %s needs %.1f mm at %.1f pt, %.1f mm free" % (ls.get("id"), sum(hs), s, h))
    yy = y
    for i, (t, hh) in enumerate(zip(rows, hs)):
        mark = (u"%d" % (i + 1)) if numbered else u"•"
        mark = fm_safe(mark, True)[0]
        P.tp.put(mark, x, yy + fm_asc_desc(s, True)[0], s, True, "L", 0.0, None, "list_item", None, ())
        st_para(P, t, x + ind, yy, w - ind, None, "list_item", s, page=P.pid)
        yy += hh
    box = (x, y, x + w, yy)
    P.tp.block(box, u"list %s" % ls.get("id"))
    return box


def pl_levels(P, lc, placed, side=None):
    """level markers beside the drawing (never on it): PLAN §3 "Level marker" (refs/U04)"""
    L = PL_LEVEL
    T = placed["T"]
    r = placed["rect"]
    side = (side or lc.get("side") or "R").upper()[:1]
    length = sum(L["dash"])
    tw, th = L["tri_w"], L["tri_h"]
    if side == "R":                             # marker from the drawing outward, its value after the triangle
        x0 = r[2] + L["gap"]
        xe = x0 + length
        lx, lal = xe + tw / 2.0 + L["label_gap"], "L"
    else:                                       # left side: the value left of the marker, right-aligned
        xe = r[0] - L["gap"] - tw / 2.0
        x0 = xe - length
        lx, lal = x0 - L["label_gap"], "R"
    pt = grid_role("level_value")[0]
    rows = []
    for lv in lc.get("levels") or []:
        y = T.ry(lv["z"])
        if not (r[1] - 1e-6 <= y <= r[3] + 1e-6):
            wn_warn(P.pid, "edge", u"level %s %+.2f of %s is outside its drawing" % (lv.get("name"), lv["z"],
                                                                                   placed["id"]))
        rows.append([y, lv])
    rows.sort(key=lambda a: a[0])
    a_, d_ = fm_asc_desc(pt, False)
    hgt = a_ - d_
    ly = []                                     # label baselines, spread so labels keep L["clear"] apart
    for y, lv in rows:
        b = y + (a_ + d_) / 2.0                 # the label's middle on the line
        if ly and b - ly[-1] < hgt + L["clear"]:
            b = ly[-1] + hgt + L["clear"]
        ly.append(b)
    n = 0
    for (y, lv), base in zip(rows, ly):
        xs, segs, on = x0, [], True
        for dd in L["dash"]:
            if on:
                segs.append((xs, xs + dd))
            xs += dd
            on = not on
        for a, b in segs:
            bk_line(P, [(a, y), (b, y)], L["ink"], L["lw"])
        bk_poly(P, [(xe - tw / 2.0, y - th), (xe + tw / 2.0, y - th), (xe, y)], None, L["ink"], L["lw"])
        P.tp.keep((x0, y - th, xe + tw / 2.0, y + 0.2), "marker", u"level %s" % lv.get("name"))
        P.ink.append(("marker", (x0, y - th, xe + tw / 2.0, y + 0.2), lc.get("id")))
        txt = u"%+.2f" % float(lv["z"])
        if lv.get("name"):
            txt += u" " + fm_safe(u"%s" % lv["name"])[0]
        P.tp.put(txt, lx, base, pt, False, lal, 0.0, lc.get("id"), "level_value",
                 L["ink"], ("marker",))
        n += 1
    return n


def pl_scalebar(P, placed, x=None, y=None, max_mm=30.0):
    """a scale bar for a true-scale drawing (never for key maps or diagrams): round length, 4 cells, "0", "L m",
    "1:den"; (x, y) = the bar's top-left (page mm, y down), default 2 mm under the drawing's left end"""
    T = placed["T"]
    if not T.den:
        return None
    k = T.k                                   # mm per m
    Lm = 1.0
    for c in (1, 2, 5, 10, 20, 50, 100, 200, 500, 1000):
        if c * k <= max_mm:
            Lm = float(c)
    Lw, hb = Lm * k, 1.2
    r = placed["rect"]
    x = r[0] if x is None else x
    y = r[3] + 2.0 if y is None else y
    ink = GRID_INK["ink"]
    for i in range(4):
        a, b = x + Lw * i / 4.0, x + Lw * (i + 1) / 4.0
        bk_rect(P, (a, y, b, y + hb), ink if i % 2 == 0 else "FFFFFF", ink, 0.3)
    pt = grid_role("caption")[0]
    a_, _d = fm_asc_desc(pt)
    P.tp.put(u"0", x, y + hb + 0.6 + a_, pt, False, "C", 0.0, None, "scale", ink, (), "sb_%s" % placed["id"])
    P.tp.put(u"%g m" % Lm, x + Lw, y + hb + 0.6 + a_, pt, False, "C", 0.0, None, "scale", ink, (),
             "sb_%s" % placed["id"])
    P.tp.put(u"1:{:,}".format(int(T.den)), x + Lw + 3.0, y + hb, pt, False, "L", 0.0, None, "scale", ink, (),
             "sb_%s" % placed["id"])
    box = (x, y, x + Lw + 3.0 + fm_width(u"1:{:,}".format(int(T.den)), pt), y + hb + 0.6 + a_ - _d)
    P.tp.keep((x, y, x + Lw, y + hb), "scalebar", placed["id"])
    P.ink.append(("scalebar", box, placed["id"]))
    return box


def pl_inset(P, ins, parent, x, y, w, h):
    """the zoom (child drawing) inside (x, y, w, h), centred, at its own scale (>= 2 x the parent's), framed; the
    parent shows the window it zooms into (thin dark frame)"""
    D = ix_get(ins.get("child"), ins.get("_folder"))
    if D is None:
        wn_warn(P.pid, "inset", u"inset %s: child drawing %r not exported" % (ins.get("id"), ins.get("child")))
        return None
    den = sc_inset_den(parent["den"] or 1000, D, w, h, P.pid)
    dw, dh = sc_size(D, den)
    T = BkT(D, den, x + (w - dw) / 2.0, y + (h - dh) / 2.0)
    placed = rd_drawing(P, D, T, frame=(GRID_INK["ink"], 0.5))
    wi = ins.get("window")
    if wi:
        a = parent["T"].pt(wi[0], wi[3])
        b = parent["T"].pt(wi[2], wi[1])
        bk_rect(P, (a[0], a[1], b[0], b[1]), None, GRID_INK["ink"], 0.5)
    return placed


def pl_mm_drawing(P, D, texts, x, y, w, h, align="C"):
    """a scale-free drawing fitted into the box (factor within its fit range), its texts placed round their anchors"""
    f = sc_factor(D, w, h, P.pid)
    dw, dh = sc_size(D, f)
    ox = x + ((w - dw) / 2.0 if align == "C" else (0.0 if align == "L" else w - dw))
    T = BkT(D, f, ox, y + (h - dh) / 2.0)
    placed = rd_drawing(P, D, T)
    pl_rigid(P, placed, f)                  # v30.3: texts stay where the script set them, scaled with the drawing
    return placed


def pl_photo(P, ph, x, y, w, h):
    """a photo at the largest size inside the box, its proportions kept (never stretched, G-R4-8 rectangular)"""
    import fitz as _fz
    f = _rd_img_path(ph.get("file"))
    if not f or not os.path.isfile(f):
        wn_warn(P.pid, "photo", u"photo %s missing: %s" % (ph.get("id"), f))
        return None
    try:
        pix = _fz.Pixmap(f)
        pw, phh = float(pix.width), float(pix.height)
        pix = None
    except Exception as ex:
        wn_warn(P.pid, "photo", u"photo %s unreadable (%s)" % (ph.get("id"), type(ex).__name__))
        return None
    s = min(w / pw, h / phh)
    bw, bh = pw * s, phh * s
    bx, by = x + (w - bw) / 2.0, y + (h - bh) / 2.0
    P.page.insert_image(_fz.Rect(bx * BK_K, by * BK_K, (bx + bw) * BK_K, (by + bh) * BK_K), filename=f)
    box = (bx, by, bx + bw, by + bh)
    P.tp.block(box, u"photo %s" % ph.get("id"))
    P.tp.keep(box, "photo", ph.get("id"))
    P.ink.append(("photo", box, ph.get("id")))
    return box
# ---- 60_layout (composer core, round 5 S1; round 6 S9 v31: G6-1 page frames): one page = one grid ------------------
# A3 landscape 420 x 297 mm, margins 14 / 12 (grid.py; = SON page2 margins x 3.3-96.7 %, PLAN P-6: one set for every
# page). Round 6 (v31): every block of a page sits in a FRAME of the page plan (80_plan, PLAN §3 "Target frames"),
# given in % of the page ([x, y, w, h], 0,0 top left; 1 % x = 4.2 mm, 1 % y = 2.97 mm). Title band (PLAN §3, frames
# files "common SON frame"): section label y 3-4 %, title y 5-8 %, the intro right of the title, a thin rule at 8.8 %;
# content from y 10 %; the page number alone, bottom right (PLAN §2.1: no "NN/23", no theme footer).
#   P = bk_page(doc, pid, n=None)            a new page: P.page (PyMuPDF), P.tp (TextPage over the whole sheet with the
#                                            14/12 mm margins, the edge test of 70_check), P.placed, P.ink, P.boxes
#   bk_pct(box) -> (x0, y0, x1, y1) mm       a frame [x, y, w, h] in % of the page -> page mm
#   lay_split(box, n, gap=4.0, vertical=True, weights=None) -> [box]   a box cut into n parts (rows or columns)
#   bk_band(P, label, title, intro=None) -> y_mm   v31 title band: section label, title (16 pt bold), intro (6 pt,
#                                            justified) right of the title, rule; returns the rule's y
#   bk_caption(P, text, box)                 a caption (5 pt, justified, last line left) in its box
#   bk_pageno(P, n)                          the page number, bottom right (7 pt bold accent), role "footer"; log
#                                            line "pagenum <n>"
#   bk_finish(P) -> n texts                  draws every text (40_set bk_emit) after the drawings
BK_GUT = 4.0
BK_PAGENO_Y = 283.5                 # baseline of the page number: inside the 12 mm bottom margin line (285)


class BkPage(object):
    def __init__(self, doc, pid, n=None):
        self.pid, self.n = pid, n
        self.page = doc.new_page(width=GRID_PAGE[0] * BK_K, height=GRID_PAGE[1] * BK_K)
        self.tp = TextPage(pid, (0.0, 0.0, GRID_PAGE[0], GRID_PAGE[1]), y_down=True,
                           margins=(GRID_ML, GRID_MT, GRID_MR, GRID_MB), footer_zone=None)
        self.placed, self.ink, self.boxes, self.layout = [], [], {}, None
        self._fonts = False


def bk_page(doc, pid, n=None):
    return BkPage(doc, pid, n)


BK_PCT = (GRID_PAGE[0] / 100.0, GRID_PAGE[1] / 100.0)      # mm per % (x 4.2, y 2.97)
BK_BAND = dict(label_y=4.05, title_y=5.1, rule_y=8.8, intro_gap=8.0)   # % of the page (PLAN §3; label on the 12 mm margin)
BK_PAGENO_LOG = []                  # "pagenum <n>" lines (code.py adds them to the log)


def bk_pct(b):
    """[x, y, w, h] in % of the page -> (x0, y0, x1, y1) page mm"""
    x, y, w, h = [float(v) for v in b]
    return (x * BK_PCT[0], y * BK_PCT[1], (x + w) * BK_PCT[0], (y + h) * BK_PCT[1])


def bk_band(P, label, title, intro=None):
    """v31 title band (see the part notes): label line, title, intro beside it, rule; returns the rule's y (mm)"""
    x0, x1 = GRID_ML, GRID_PAGE[0] - GRID_MR
    acc, ink = GRID_INK["accent"], GRID_INK["ink"]
    if label:
        pt = 6.0
        a_, _d = fm_asc_desc(pt, True)
        P.tp.put(label, x0, BK_BAND["label_y"] * BK_PCT[1] + a_, pt, True, "L", 0.0, "label", "title", acc)
    pt = grid_role("title")[0]
    tw_max = 0.55 * (x1 - x0)                       # the title takes at most 55 % of the width; the intro the rest
    w = fm_width(title, pt, True)
    if w > tw_max:
        pt = max(GRID_MIN_PT, pt * tw_max / w)
        w = fm_width(title, pt, True)
    a_, _d = fm_asc_desc(pt, True)
    ty = BK_BAND["title_y"] * BK_PCT[1]
    P.tp.put(title, x0, ty + a_, pt, True, "L", 0.0, "title", "title", ink)
    ry = BK_BAND["rule_y"] * BK_PCT[1]
    if intro:
        ix = x0 + w + BK_BAND["intro_gap"]
        st_para(P, intro, ix, ty, max(30.0, x1 - ix), ry - ty - 0.8, "intro", page=P.pid)
    bk_line(P, [(x0, ry), (x1, ry)], GRID_INK["rule"], 0.4)
    return ry


def lay_split(box, n, gap=BK_GUT, vertical=True, weights=None):
    x0, y0, x1, y1 = box
    n = max(1, int(n))
    wts = list(weights) if weights else [1.0] * n
    tot = float(sum(wts))
    span = ((y1 - y0) if vertical else (x1 - x0)) - gap * (n - 1)
    out, p = [], (y0 if vertical else x0)
    for wv in wts:
        d = span * wv / tot
        out.append((x0, p, x1, p + d) if vertical else (p, y0, p + d, y1))
        p += d + gap
    return out


def bk_caption(P, text, box):
    return st_para(P, text, box[0], box[1], box[2] - box[0], box[3] - box[1], "caption", page=P.pid)


def bk_pageno(P, n):
    pt, b, _l, col = grid_role("pageno")
    P.tp.put(u"%d" % int(n), GRID_PAGE[0] - GRID_MR, BK_PAGENO_Y, pt, b, "R", 0.0, "pageno", "footer", col,
             ("footer",))
    BK_PAGENO_LOG.append(u"pagenum %d" % int(n))


def bk_finish(P):
    return bk_emit(P)
# ---- 70_check (composer core, round 5 S1; G-R5-1, D1, D2, C7, C11, C12): the layout check on FINAL page coordinates ---
# Runs after a page is composed (every drawing, label, legend, list, marker, scale bar and text placed). Measures:
#   fill        area of the union of everything placed (drawing windows, photos, markers, scale bars, legend / list
#               blocks, every text box) inside the margins (14 / 12 mm) / that area; 1 mm cells
#   empty_band  the tallest run of 1 mm rows inside the margins with nothing placed on them, in mm
#   overlaps    TextPage.check: text/text, text/drawing (a drawing's window is a keep only its own labels may enter),
#               text/legend swatch, text/marker, block/block (drawings, legends, lists, key maps, photos)
#   edge        text or block past the margins (blocks too: check(blocks_in=True)); labels never cross their window
#               (50_place does not take such spots)
#   min_text    the smallest printed size on the page (D1: >= 4.0 pt after scaling; C12)
# Every overlap / edge hit is one WARNING line (TextPage.check); fill below the reference and a band over the limit are
# WARNING lines in ck_finish; a text under 4 pt is its own WARNING when it is set. Nothing stops the run.
# The measure counts boxes (a drawing's window is filled), the same measure for p15 and every page (D2).
#   ck_page(P) -> dict(pid, fill, band_mm, overlaps, edge, min_text, n_text)   (kept in CK_RES)
#   ck_finish(ref="p15", log=None) -> [line]
#         after all pages: the reference fill = p15's measured fill (D2: the round 5 p15 composed by this booklet);
#         per page "layout <page> fill=<x> ref_p15=<y> empty_band=<mm> overlaps <n> edge <n> min_text=<pt>", a WARNING
#         "fill" when fill < ref, a WARNING "empty_band" when the band > CK_BAND_MAX of the inner height (D2: 3 %),
#         then "text justified n" (40_set). Lines go to log (default the warning list, so they reach the log).
CK_RES = []
CK_CELL = 1.0
CK_BAND_MAX = 0.03


def _ck_inner():
    return (GRID_ML, GRID_MT, GRID_PAGE[0] - GRID_MR, GRID_PAGE[1] - GRID_MB)


def _ck_mark(G, cols, rows, inn, b):
    import math as _m
    x0, y0 = max(b[0], inn[0]), max(b[1], inn[1])
    x1, y1 = min(b[2], inn[2]), min(b[3], inn[3])
    if x1 <= x0 or y1 <= y0:
        return
    c0, c1 = int(_m.floor((x0 - inn[0]) / CK_CELL)), min(cols, int(_m.ceil((x1 - inn[0]) / CK_CELL)))
    r0, r1 = int(_m.floor((y0 - inn[1]) / CK_CELL)), min(rows, int(_m.ceil((y1 - inn[1]) / CK_CELL)))
    if c1 <= c0:
        return
    run = b"\x01" * (c1 - c0)
    for r in range(r0, r1):
        G[r * cols + c0:r * cols + c1] = run


def ck_page(P):
    tp = P.tp
    tp.check(raise_=False, blocks_in=True)
    ov = sum(1 for h in tp.hits if h[0] == "overlap")
    ed = sum(1 for h in tp.hits if h[0] == "edge")
    inn = _ck_inner()
    cols = int((inn[2] - inn[0]) / CK_CELL)
    rows = int((inn[3] - inn[1]) / CK_CELL)
    G = bytearray(cols * rows)
    for it in tp.items:
        _ck_mark(G, cols, rows, inn, it["box"])
    for B in tp.blocks:
        _ck_mark(G, cols, rows, inn, B["box"])
    for _k, b, _n in P.ink:
        _ck_mark(G, cols, rows, inn, b)
    fill = sum(G) / float(cols * rows) if cols and rows else 0.0
    band = best = 0
    for r in range(rows):
        if any(G[r * cols:(r + 1) * cols]):
            band = 0
        else:
            band += 1
            best = max(best, band)
    pts = [it["pt"] * tp.scale for it in tp.items if it.get("emit", True)]
    res = dict(pid=P.pid, fill=fill, band_mm=best * CK_CELL, overlaps=ov, edge=ed,
               min_text=min(pts) if pts else None, n_text=len(pts))
    CK_RES.append(res)
    return res


def ck_finish(ref="p15", log=None):
    lg = WN_LOG if log is None else log
    R = [r for r in CK_RES if r["pid"] == ref]
    rf = R[-1]["fill"] if R else None
    if rf is None:
        wn_warn(None, "fill", u"the reference page %s was not composed: no fill threshold this run (D2)" % ref, lg)
    lim = CK_BAND_MAX * (GRID_PAGE[1] - GRID_MT - GRID_MB)
    out = []
    for r in CK_RES:
        if rf is not None and r["pid"] != ref and r["fill"] < rf - 1e-4:
            wn_warn(r["pid"], "fill", u"fill %.2f below %s's %.2f: enlarge the drawings (D2)" % (r["fill"], ref, rf), lg)
        if r["band_mm"] > lim + 1e-6:
            wn_warn(r["pid"], "empty_band", u"an empty band %.0f mm tall (limit %.1f mm = 3 %% of the height, D2)" % (
                r["band_mm"], lim), lg)
        # min_text: every text under the floor was already one WARNING "min_text" when it was set (TextPage._size_ok)
        ln = u"layout %s fill=%.2f ref_p15=%s empty_band=%.0f overlaps %d edge %d min_text=%s" % (
            r["pid"], r["fill"], (u"%.2f" % rf) if rf is not None else u"none", r["band_mm"], r["overlaps"],
            r["edge"], (u"%.2f" % r["min_text"]) if r["min_text"] is not None else u"-")
        lg.append(ln)
        out.append(ln)
    ln = u"text justified %d (of %d paragraphs set; %d lines stretched)" % (ST_COUNT["justified"], ST_COUNT["paras"],
                                                                          ST_COUNT["lines"])
    lg.append(ln)
    out.append(ln)
    return out


def ck_reset():
    del CK_RES[:]
    for k in ST_COUNT:
        ST_COUNT[k] = 0
# ---- high-res silhouettes (assets_2, Aras 30 Oct 2026): PhyloPic trees, crops and animals as filled vector rings,
# drawn only in the detailed (true-to-cut) sections and recoloured there with that section's own colours. The
# sketchy sections and diagrams keep their own drawing (an abstract set comes later).
# Library: Downloads/Bergama/Data/assets_hires.json (run kit Data/), built in the cloud by
# tools/assets2/build_hires.py from revision_2026-10-29/assets_2_2026-10/ (roots cut at the ground, height 1.0,
# ground / feet at y = 0, y up). Each part = one keyhole ring for the even-odd fill + its outer and hole rings for
# outlines. Uniform scale only (never stretched). No JSON on the PC -> callers fall back to their own drawing.
# The sources are listed once on the booklet's Sources page under ASSETS (Aras 30 Oct 06:20), never beside a drawing.

HR_LOG = []
_HR_LIB = {}


def hr_library():
    """the high-res library (dict key -> asset) or {} when Downloads/Bergama/Data/assets_hires.json is missing"""
    import os as _o
    import json as _j
    if "lib" in _HR_LIB:
        return _HR_LIB["lib"]
    lib = {}
    p = _o.path.join(_o.path.expanduser("~"), "Downloads", "Bergama", "Data", "assets_hires.json")
    if _o.path.exists(p):
        try:
            with open(p, "r") as fh:
                lib = _j.load(fh).get("lib", {})
            HR_LOG.append(u"High-res assets: %d from %s" % (len(lib), p))
        except Exception as ex:
            HR_LOG.append(u"High-res assets: %s unreadable (%s); own drawings used" % (p, type(ex).__name__))
    else:
        HR_LOG.append(u"High-res assets: Data/assets_hires.json not found; own drawings used")
    _HR_LIB["lib"] = lib
    return lib


def _hr_draw(a, T, fill, edge, lw):
    out = []
    for part in a.get("parts", []):
        out.append(("poly", [T(q) for q in part["fill"]], fill, None, 0.0))   # lw 0.0 marks a high-res fill
        if edge:
            for r in part["lines"]:
                pts = [T(q) for q in r]
                out.append(("line", pts + [pts[0]], edge, lw))
    return out


def hr_side(key, x, gy, k, h_m, w_m=None, fill="000000", edge=None, lw=0.08, facing=1):
    """house shapes of one high-res plant: ground at (x, gy) page mm, h_m tall (m), k page mm per m; when w_m is given
    and the silhouette would be wider, the whole drawing is scaled down until it is w_m wide (uniform). facing -1 =
    mirrored. None when the library or the key is missing."""
    a = hr_library().get(key) if key else None
    if not a or not h_m:
        return None
    s = h_m * k
    wd = float(a["x1"] - a["x0"])
    if w_m and wd * h_m > w_m:
        s = w_m / wd * k
    f = -1.0 if facing < 0 else 1.0
    return _hr_draw(a, lambda q: (x + f * q[0] * s, gy + q[1] * s), fill, edge, lw)


def hr_fauna(key, x, y, size, fill="000000", edge=None, lw=0.05, facing=1, foot=None):
    """house shapes of one high-res animal in a size-mm square centred on (x, y), head to the left (facing -1: to the
    right, PhyloPic draws most animals facing left; the library's face tells which way each one looks); with foot
    the feet sit foot x size below y (the pictograms' ground rule), otherwise the animal is centred. None when
    missing."""
    a = hr_library().get(key) if key else None
    if not a:
        return None
    wd = float(a["x1"] - a["x0"])
    s = size / max(wd, 1.0)
    cx = (a["x0"] + a["x1"]) / 2.0
    f = (-1.0 if facing < 0 else 1.0) * (-1.0 if a.get("face", 1) < 0 else 1.0)
    y0 = y - foot * size if foot is not None else y - s / 2.0
    return _hr_draw(a, lambda q: (x + f * (q[0] - cx) * s, y0 + q[1] * s), fill, edge, lw)


def hr_sources():
    """one line per asset used from the library, for the booklet's Sources page (ASSETS)"""
    out = []
    for key, a in sorted(hr_library().items()):
        out.append(u"%s silhouette, %s, PhyloPic (%s), %s" % (a.get("what", key), a.get("author", ""),
                                                              a.get("url", ""), a.get("licence", "")))
    return out
# ---- 80_plan (round 5 S10; round 6 S9 v31, G6-1/G6-2): the 22-page booklet plan as FRAMES ---------------------------
# ONE numbering: p01 ... p22 (PLAN §2.1), exported directly by every content script. Each content page: part / stage
# (contents on the cover), title (PLAN §2.1), intro (used only when no script exports a role "intro" text), frames,
# side (the frame key where unlisted items and overflow notes go).
# A frame F(ids, x, y, w, h, **opt): ids = one fnmatch pattern or a tuple of them (item ids of PLAN §2.2 first, then
# the ids the scripts export today, so a page composes before and after the round 6 content sessions); box in % of
# the A3 page, 0,0 top left (PLAN §3: plan_findings/frames_p01-08.md, frames_p09-13.md, frames_p14-22.md, "Target
# frames", est. +-1 %). Options: key (name; default the first pattern), same (frames with one key share one scale /
# factor), note (the frame key where this frame's drawings' attached notes go), foot (% of the page kept under the
# drawings for their notes), split ("row" | "col" for several drawings in one frame), al ("TL" default, "MC", "BL"
# ...), over (may sit on another frame), opt (an empty frame is no WARNING).
# Every frame is inside the one margin set x 3.3-96.7 % (P-6) and above the page number (y <= 94 %).


def F(ids, x, y, w, h, **kw):
    return dict(kw, ids=ids, box=(x, y, w, h))


BOOK = dict(
    hook=u"MIRAQUA",
    title=u"From stream corridor to hydrological commons",
    subtitle=u"Selinos stream edge, Bergama",
    course=u"Yaşar University · ARCH 4410 Architectural Design Studio V · 2026-2027 Fall",
    names=[u"Aras Özkaymakcı", u"Begüm Arslan", u"Nil Çetin"],
    date=u"October 2026",             # round 4 value kept (change here if the booklet date moves)
)
PARTS = {"A": u"Site and stream edge", "B": u"Movement and the city", "C": u"Water", "D": u"History and heritage",
         "E": u"Masterplan: the synthesis"}
STAGES = {"an": u"Analysis", "got": u"What we got", "an+got": u"Analysis, what we got", "do": u"What we do with it"}
COVER_IMG = "W01_cover_collage.jpg"          # Downloads/Bergama/Data/ (own work, round 4 P01.2)
COVER_VEIL = 0.82                            # P01.1: white veil over the full-bleed photo = photo at 18 % strength
COVER_TEXT = (u"MIRAQUA turns the walled Selinos stream through Bergama into a landscape that lives in all four seasons. "
              u"Clean water is collected, cleaned and held at the upstream entry, kept in the bed as a summer strip, and "
              u"given to the farms outside the site. Planting follows the days under water, from wet to dry; when the "
              u"water rises, life on the banks pauses and returns as it drops. A streamside spine of five bridge places "
              u"ties the Kale side to the bazaar side.")      # round 4 approved text (BRIEF P01.2 r4), unchanged

BK_PAGES = [
    dict(pid="p01", kind="cover"),
    # 2 · SON page2 (G6-1: map x1.035, right column as SON, lower block down 1.5)
    dict(pid="p02", part="A", stage="an", title=u"What is there, grain of the town",
         intro=u"The whole survey area *as it is today*: buildings by *urban fabric*, ground and green, the *Selinos "
               u"stream* with its edges and *six bridges*, and the places where *stream and town clash*.",
         frames=[F("sb_plan01", 3.3, 10.0, 45.2, 59.5, note="plan01_notes"),
                 F(("sb_plan01_*", "sb_p02_legend*", "sb_p02_note*"), 3.3, 70.5, 45.2, 21.0, key="plan01_notes"),
                 F("sb_edge_types", 50.5, 10.0, 46.2, 52.5),
                 F("sb_site_readings", 50.5, 64.0, 46.2, 27.5)],
         side="plan01_notes"),
    # 3 · SON page3 (axo x1.047, bottom zone rebuilt clear of the footer)
    dict(pid="p03", part="A", stage="an", title=u"Heights and enclosure",
         intro=u"Plan 01 as a parallel axonometric: *heights* are what the plan cannot show; the *sky view* from the "
               u"stream bed marks its *most enclosed* stretch.",
         frames=[F("sb_axo_what_is_there", 3.3, 10.0, 93.4, 72.0, key="axo"),
                 F(("sb_axo_what_is_there_legend", "sb_p03_legend*"), 3.3, 83.0, 55.0, 6.5, key="legend"),
                 F(("sb_axo_what_is_there_caption", "sb_axo_*", "sb_p03_*"), 3.3, 90.0, 56.0, 4.0, key="notes")],
         side="notes"),
    # 4 · SON page4 (P-7, U20): one scale for S1-S4, each note level with its cut
    dict(pid="p04", part="A", stage="an", title=u"Sections across the stream",
         intro=u"Cuts *across the Selinos stream*, each drawn *as it is*: the ground, the *bed and banks*, the "
               u"buildings, trees and fields it crosses.",
         frames=[F(("sb_sec_keymap_p04", "*keymap*"), 7.0, 10.0, 72.0, 19.5, key="km"),
                 F(("sb_sec_legend_p04", "sb_sec_intro*"), 80.0, 10.0, 16.7, 20.0, key="legend"),
                 F("sb_sec_s1", 7.0, 31.0, 72.0, 18.5, same="cuts", note="n1"),
                 F("sb_sec_note_s1*", 80.0, 31.0, 16.7, 18.5, key="n1"),
                 F("sb_sec_s2", 7.0, 51.0, 72.0, 10.5, same="cuts", note="n2"),
                 F("sb_sec_note_s2*", 80.0, 51.0, 16.7, 10.5, key="n2"),
                 F("sb_sec_s3", 7.0, 63.0, 72.0, 18.5, same="cuts", note="n3"),
                 F("sb_sec_note_s3*", 80.0, 63.0, 16.7, 18.5, key="n3"),
                 F("sb_sec_s4", 7.0, 83.0, 72.0, 10.5, same="cuts", note="n4"),
                 F("sb_sec_note_s4*", 80.0, 83.0, 16.7, 10.5, key="n4")],
         side="legend"),
    # 5 · SON page5 (as page 4; inside the one margin set, P-6)
    dict(pid="p05", part="A", stage="an", title=u"Sections across the stream",
         intro=u"Cuts *across the Selinos stream*, each drawn *as it is*: the ground, the *bed and banks*, the "
               u"buildings, trees and fields it crosses.",
         frames=[F(("sb_sec_keymap_p05", "*keymap*"), 3.3, 10.0, 74.0, 18.5, key="km"),
                 F(("sb_sec_legend_p05", "sb_sec_intro*"), 79.0, 10.0, 17.7, 19.0, key="legend"),
                 F("sb_sec_s5", 3.3, 30.0, 74.0, 12.5, same="cuts", note="n5"),
                 F("sb_sec_note_s5*", 79.0, 30.0, 17.7, 12.5, key="n5"),
                 F("sb_sec_s6", 3.3, 44.0, 74.0, 14.5, same="cuts", note="n6"),
                 F("sb_sec_note_s6*", 79.0, 44.0, 17.7, 14.5, key="n6"),
                 F("sb_sec_s7", 3.3, 60.0, 74.0, 18.5, same="cuts", note="n7"),
                 F("sb_sec_note_s7*", 79.0, 60.0, 17.7, 18.5, key="n7"),
                 F("sb_sec_s8", 3.3, 80.0, 74.0, 13.5, same="cuts", note="n8"),
                 F("sb_sec_note_s8*", 79.0, 80.0, 17.7, 13.5, key="n8")],
         side="legend"),
    # 6 · SON page6 (one board drawing: map, cards, photos, right column)
    dict(pid="p06", part="A", stage="got", title=u"The stream edge and where we can build",
         intro=u"Both banks *every 4 m*, and the ground *open to change*: where the project *can build*.",
         frames=[F("sb_edge_build", 3.3, 10.0, 93.4, 80.0, key="edge"),
                 F(("sb_edge_build_*", "sb_p06_*"), 3.3, 90.5, 60.0, 3.5, key="notes")],
         side="notes"),
    # 7 · SON page7 (P-8, U19): maps x1.10 one scale, right column 16.9 %, each note level with its map
    dict(pid="p07", part="B", stage="an", title=u"How people use it",
         intro=u"*Shops* line Kınık Caddesi and Üç Kemer Caddesi, the *primary commercial spines*; *walking* and "
               u"*driving* today, street by street.",
         frames=[F("sb_movement", 3.3, 10.5, 75.0, 26.0, same="maps", note="n1"),
                 F("sb_mv_note_1*", 79.7, 10.7, 17.0, 25.5, key="n1"),
                 F("sb_walking_today", 3.3, 39.0, 75.0, 26.0, same="maps", note="n2"),
                 F("sb_mv_note_2*", 79.7, 39.0, 17.0, 25.5, key="n2"),
                 F("sb_driving_today", 3.3, 67.3, 75.0, 26.0, same="maps", note="n3"),
                 F("sb_mv_note_3*", 79.7, 67.3, 17.0, 25.5, key="n3")],
         side="n3"),
    # 8 · SON page8 (P-9 option A, U18): key map up beside the corridor, R1-R4 strip full width
    dict(pid="p08", part="B", stage="got", title=u"The stream joins the town where the shops already are",
         intro=u"One *corridor*: the shop streets, the *hidden stream* and the project from end to end; *who* comes "
               u"when; each *street cut* today and with the project.",
         frames=[F("cl_p08_corridor", 3.3, 10.0, 67.5, 25.5, note="corr_legend"),
                 F("cl_p08_corridor_legend", 72.0, 10.0, 24.7, 15.5, key="corr_legend"),
                 F(("sb_street_keymap*", "*keymap*"), 72.0, 26.0, 24.7, 7.5, key="km"),
                 F("cl_p08_shops", 72.0, 33.8, 24.7, 2.7, key="shops"),
                 F("cl_p08_who", 3.3, 37.0, 93.4, 31.0, note="who_notes"),
                 F(("cl_p08_who_legend", "cl_p08_who_note"), 3.3, 68.5, 93.4, 4.5, key="who_notes"),
                 F("sb_street_legend*", 3.3, 73.5, 93.4, 3.5, key="street_legend"),
                 F(("sb_street_R*", "sb_street_sections"), 3.3, 77.5, 93.4, 16.5, key="streets", same="streets",
                   split="row", foot=1.5)],
         side="who_notes"),
    # 9 · SON page9 + page10 (P-10, U16, U17): spine x0.69, windows above their cards, bottom band enlarged
    dict(pid="p09", part="B", stage="do", title=u"The streamside spine, hub by hub",
         intro=u"*Five bridge places* on existing bus stops, *walking hubs* with a *sub-hub in the bed*, one *transit "
               u"hub*: the spine along the Selinos, hub by hub.",
         frames=[F("cl_p09_spine", 3.3, 10.0, 48.0, 16.5, key="spine"),
                 F(("cl_p09_legend", "cl_p10_legend"), 53.0, 10.0, 43.7, 16.5, key="legend"),
                 F(("cl_p10_windows_head", "cl_p09_windows_head"), 3.3, 27.0, 60.0, 2.2, key="win_head"),
                 F("cl_p10_win_1", 3.3, 29.5, 17.5, 17.5, same="win"),
                 F("cl_p10_win_2", 22.0, 29.5, 17.5, 17.5, same="win"),
                 F(("cl_p10_win_3a", "cl_p10_win_3b", "cl_p10_win_3*"), 40.8, 29.5, 17.5, 17.5, same="win",
                   split="row", key="win_3"),
                 F("cl_p10_win_4", 59.6, 29.5, 17.5, 17.5, same="win"),
                 F("cl_p10_win_5", 78.4, 29.5, 18.3, 17.5, same="win"),
                 F(("cl_p09_card_1", "cl_p10_hub_1"), 3.3, 48.0, 17.5, 23.5, same="cards"),
                 F(("cl_p09_card_2", "cl_p10_hub_2"), 22.0, 48.0, 17.5, 23.5, same="cards"),
                 F(("cl_p09_card_3", "cl_p10_hub_3"), 40.8, 48.0, 17.5, 23.5, same="cards"),
                 F(("cl_p09_card_4", "cl_p10_hub_4"), 59.6, 48.0, 17.5, 23.5, same="cards"),
                 F(("cl_p09_card_5", "cl_p10_hub_5"), 78.4, 48.0, 18.3, 23.5, same="cards"),
                 F("cl_p10_flood", 3.3, 74.0, 46.0, 19.5),
                 F("cl_p10_bank", 51.4, 74.0, 28.6, 19.5),
                 F("cl_p10_market", 82.0, 74.0, 14.7, 19.5)],
         side="legend"),
    # 10 · SON page11 (G6-1: panel 2 chart enlarged; the run stamp leaves, S7)
    dict(pid="p10", part="C", stage="an+got", title=u"The water balance",
         intro=u"How much *winter water* can we hold for the farms' *dry summer*, and at *what cost*?",
         frames=[F("wb_year", 3.3, 10.5, 93.4, 38.0, foot=3.0),
                 F("wb_curve", 3.3, 50.0, 53.0, 28.0, foot=3.0),
                 F("wb_store", 58.3, 50.0, 38.4, 28.0, foot=4.0),
                 F("wb_answer", 3.3, 79.5, 93.4, 14.0)],
         side="wb_answer"),
    # 11 · SON page12 (A-A' SKETCH; map legend off the map into the left column, G6-4)
    dict(pid="p11", part="C", stage="do", title=u"Collect, clean, hold",
         intro=u"*Collect* winter stream water and runoff at the upstream entry, *clean* it once in *lined reed "
               u"basins*, *hold* it in the ground for the dry summer; the clean stream leaves for the *farms outside*.",
         frames=[F(("wb_p12_map_legend", "p12_map_legend", "wb_p12_map_letters", "wb_p12_relief_note"), 3.3, 10.0,
                   13.0, 63.0, key="map_legend"),
                 F("p12_map", 17.0, 10.0, 51.0, 63.0, note="map_legend"),
                 F("p12_zoom", 24.0, 12.0, 26.0, 23.0, over=True),
                 F("p12_steps", 69.5, 10.0, 27.2, 14.5),
                 F("p12_coliforms", 69.5, 26.5, 27.2, 16.0),
                 F("p12_plants", 69.5, 44.0, 27.2, 11.5),
                 F("p12_why", 69.5, 57.0, 27.2, 9.5),
                 F(("wb_p12_conclusion", "p12_conclusion"), 69.5, 68.0, 27.2, 5.0, key="conclusion"),
                 F(("p12_section_head*", "p12_section_list*", "wb_p12_section_key", "p12_section_key*"), 3.3, 74.5,
                   17.0, 18.5, key="aa_list"),
                 F(("p12_section_sketch", "p12_section"), 21.4, 74.5, 42.0, 18.5, key="aa", note="aa_list"),
                 F("p12_section_reeds", 64.0, 74.5, 20.0, 18.5),
                 F(("p12_keymap", "*keymap*"), 84.8, 74.5, 11.9, 7.0, key="km"),
                 F(("wb_p12_section_legend", "p12_section_legend*", "wb_p12_strip_note"), 84.8, 82.0, 11.9, 11.0,
                   key="aa_legend")],
         side="aa_legend"),
    # 12 · SON page13 + page14 = r06_S02 (P-12, P-1): four SKETCH panels, legend strip above the footer
    dict(pid="p12", part="C", stage="do", title=u"The proposals in section",
         intro=u"Four cuts, *upstream to downstream*: each proposal *in section*, the winter water and the summer "
               u"strip, the reach of the *design flood (Q500)*.",
         frames=[F(("ps_panel_1", "ps_W1"), 3.3, 10.0, 46.4, 40.0, same="panels"),
                 F(("ps_panel_2", "ps_W2"), 50.3, 10.0, 46.4, 40.0, same="panels"),
                 F(("ps_panel_3", "ps_W3"), 3.3, 51.0, 46.4, 38.0, same="panels"),
                 F(("ps_panel_4", "ps_W4"), 50.3, 51.0, 46.4, 38.0, same="panels"),
                 F(("ps_caption*", "ps_intro_note*"), 3.3, 89.2, 60.0, 1.6, key="caption", opt=True),
                 F(("ps_legend_strip", "ps_legend"), 3.3, 90.9, 74.0, 2.8, key="legend"),
                 F(("ps_keymap_p12", "ps_keymap_*"), 80.0, 89.2, 16.7, 4.6, key="km")],
         side="legend"),
    # 13 · SON page15 = r06_S03 + animal column (P-11): one row per season, cut at one scale
    dict(pid="p13", part="C", stage="do", title=u"Four seasons on one cut",
         intro=u"*One cut, one viewpoint, four seasons*: the *water level* decides what the place becomes, which "
               u"plants are in *leaf or flower*, and which animals are about.",
         frames=[F("p15_hubkey", 3.3, 10.0, 12.0, 5.5),
                 F("p15_monthbar", 17.0, 10.0, 48.0, 5.5),
                 F("p15_season_winter", 3.3, 16.0, 67.0, 17.5, same="seasons"),
                 F("p15_season_spring", 3.3, 34.0, 67.0, 17.5, same="seasons"),
                 F("p15_season_summer", 3.3, 52.0, 67.0, 17.5, same="seasons"),
                 F("p15_season_autumn", 3.3, 70.0, 67.0, 17.5, same="seasons"),
                 F("p15_feel*", 72.0, 10.0, 13.5, 78.0, key="feel"),
                 F("p15_animals*", 87.0, 10.0, 9.7, 78.0, key="animals"),
                 F(("p15_keymap", "p13_keymap", "*keymap*"), 3.3, 88.5, 12.0, 5.5, key="km"),
                 F(("p15_caption*", "p15_scale*"), 17.0, 88.5, 50.0, 2.0, key="caption", opt=True)],
         side="animals"),
    # 14 · SON page16 (ACCURATE S4 NE; no horizontal dimension row; year chart kept)
    dict(pid="p14", part="C", stage="do", title=u"The S4 cut, north-east bank",
         intro=u"The north-east bank of S4: *seat steps* and a *raised promenade* over Q500 stay; the *planting follows "
               u"the days under water*, the use follows the months.",
         frames=[F(("p16_keymap", "p14_keymap", "*keymap*"), 3.3, 10.5, 30.0, 12.5, key="km"),
                 F("p16_section", 3.3, 24.0, 65.0, 28.5, note="parts"),
                 F("p16_section_inset", 35.0, 10.5, 17.0, 12.5),
                 F(("p16_parts", "p16_groups", "p16_bands"), 69.5, 10.5, 27.2, 42.0, key="parts"),
                 F("p16_year", 3.3, 54.0, 93.4, 39.5, foot=3.0)],
         side="parts"),
    # 15 · SON page17 (G6-1 only): six maps 2 x 3 at one scale, each legend in its column
    dict(pid="p15", part="C", stage="do", title=u"The senses and the water",
         intro=u"The *fade-out zones* and the *senses*, zone by zone, *upstream to downstream*.",
         frames=[F("mp_sn_zones", 3.3, 10.0, 35.7, 27.0, same="sn", note="k_zones"),
                 F("mp_sn_zones_key", 39.5, 10.0, 10.0, 27.0, key="k_zones"),
                 F("mp_sn_feeling", 50.3, 10.0, 35.7, 27.0, same="sn", note="k_feeling"),
                 F("mp_sn_feeling_wheel", 86.5, 10.0, 10.2, 10.0),
                 F("mp_sn_feeling_key", 86.5, 21.0, 10.2, 16.0, key="k_feeling"),
                 F("mp_sn_sound", 3.3, 38.5, 35.7, 27.0, same="sn", note="k_sound"),
                 F("mp_sn_sound_key", 39.5, 38.5, 10.0, 27.0, key="k_sound"),
                 F("mp_sn_smell", 50.3, 38.5, 35.7, 27.0, same="sn", note="k_smell"),
                 F("mp_sn_smell_key", 86.5, 38.5, 10.2, 27.0, key="k_smell"),
                 F("mp_sn_encounters", 3.3, 67.0, 35.7, 26.5, same="sn", note="k_enc"),
                 F("mp_sn_encounters_key", 39.5, 67.0, 10.0, 26.5, foot=16.5, key="k_enc"),
                 # one id for the diagram and the legend (masterplan p16_senses.py:1567 / :1649): diagram on top,
                 # the legend in the foot
                 F("mp_sn_history", 50.3, 67.0, 35.7, 26.5, same="sn", note="k_hist"),
                 F("mp_sn_photo_*", 86.5, 67.0, 10.2, 14.0, key="photos"),
                 F("mp_sn_history_key", 86.5, 82.0, 10.2, 11.5, key="k_hist")],
         side="k_hist"),
    # 16 · SON page18 (G6-1 + 23 overlaps): key map + legend left, plans A/B, middle row, species row
    dict(pid="p16", part="C", stage="do", title=u"Which plant goes where",
         intro=u"*Wet to dry, low to high*: rushes and loosestrife *at the water*, willow and tamarisk on the *banks "
               u"that flood*, shade trees and olives on the *dry tops*; reed and water mint only in *lined basins*.",
         frames=[F(("p18_keymap", "p16_keymap", "*keymap*"), 3.3, 10.5, 16.0, 18.5, key="km"),
                 F(("p18_plans_legend", "p16_plans_legend"), 3.3, 30.0, 16.0, 21.5, key="legend"),
                 F("p18_plan_A", 20.0, 10.0, 21.0, 31.5, same="plans", note="list_A"),
                 F("p18_plan_A_list", 20.0, 42.0, 21.0, 9.5, key="list_A"),
                 F("p18_plan_B", 42.0, 10.0, 54.7, 38.5, same="plans", note="list_B"),
                 F("p18_plan_B_list", 42.0, 49.0, 54.7, 3.0, key="list_B"),
                 F("p18_bands", 3.3, 53.0, 17.0, 14.0, foot=2.5),
                 F("p18_band_shares", 21.0, 53.0, 10.5, 14.0, foot=4.0),
                 F("p18_foliage_shares", 32.0, 53.0, 10.5, 14.0, foot=4.0),
                 F("p18_heights", 43.0, 53.0, 53.7, 14.0),
                 F("p18_card_*", 3.3, 68.0, 93.4, 25.0, key="cards", split="row", same="cards")],
         side="legend"),
    # 17 · NEW = r06_S01 (SKETCH plant ladder)
    dict(pid="p17", part="C", stage="do", title=u"One plant ladder, streambed to field",
         intro=u"One cut from the *stream to the farms*, through the year: what the *water* does and what *people* do "
               u"on each step.",
         frames=[F("ag3_chain", 3.3, 9.5, 93.4, 9.8),
                 F("ag3_ladder_high", 3.3, 20.0, 93.4, 15.0, same="ladder"),
                 F("ag3_ladder_low", 3.3, 36.0, 93.4, 15.0, same="ladder"),
                 F("ag3_ladder_harvest", 3.3, 52.0, 93.4, 15.0, same="ladder"),
                 F(("ag3_note*", "ag3_remove*", "ag3_odour*"), 3.3, 69.0, 18.0, 24.5, key="notes"),
                 F("ag3_bands", 23.0, 69.0, 73.7, 5.0),
                 F(("ag3_photos", "ag3_photo_*"), 23.0, 74.5, 73.7, 19.0, key="photos")],
         side="notes"),
    # 18 · SON page19 (G6-1 + 16 overlaps): four rows, one right line at x 60
    dict(pid="p18", part="C", stage="do", title=u"Where the clean water goes, and what it grows",
         intro=u"Clean water to *farmland outside the site*, easing an *overused aquifer*, *never drinking water*; "
               u"*same storage, different crops*: the *hectares* each crop irrigates.",
         frames=[F("wb_farms", 3.3, 10.0, 55.0, 20.5),
                 F("wb_farms_out", 60.0, 10.0, 36.7, 20.5),
                 F("wb_decision", 3.3, 32.0, 30.0, 15.5),
                 F("ag1_stream", 35.0, 32.0, 61.7, 15.5),
                 F("ag1_bars", 3.3, 49.0, 55.0, 25.0),
                 F("ag1_context", 60.0, 49.0, 36.7, 25.0),
                 F(("ag1_reading*", "ag2_farms"), 3.3, 76.0, 30.0, 17.5, key="reading"),
                 F("ag1_history", 35.0, 76.0, 30.0, 17.5),
                 F("ag1_crops_*", 67.0, 76.0, 29.7, 17.5, key="crops")],
         side="ag1_context"),
    # 19 · SON page20 (heritage symbols in the brown ramp, S3); legends in one row under the board
    dict(pid="p19", part="D", stage="do", title=u"The heritage loop",
         intro=u"The Selinos is the *seam*: *bridges, crafts and events* tie the *Kale side* to the *bazaar side*.",
         frames=[F("sb_heritage_loop", 3.3, 10.0, 93.4, 76.0, key="loop"),
                 F(("sb_heritage_loop_legend", "sb_heritage_legend"), 3.3, 87.0, 93.4, 4.5, key="legend"),
                 F(("sb_heritage_loop_caption", "sb_heritage_*"), 3.3, 92.0, 50.0, 1.8, key="caption")],
         side="legend"),
    # 20 · SON page21 (base map kept; legend regrouped by category; proposals drawn, S8)
    dict(pid="p20", part="E", stage="do", title=u"Masterplan: an ecological corridor",
         intro=u"The whole project on one plan: *walking hubs*, *reed basins* and terraces that *hold the rain*, "
               u"*calmed streets*, along the Selinos as an *ecological corridor*.",
         frames=[F("mp_plan_r1", 3.3, 10.0, 69.0, 38.5, same="mp"),
                 F("mp_plan_r2", 3.3, 50.0, 69.0, 39.5, same="mp"),
                 F("mp_plan_legend", 73.0, 10.0, 23.7, 23.0, key="legend"),
                 F(("mp_plan_moves_head", "mp_plan_moves"), 73.0, 34.0, 23.7, 27.0, key="moves"),
                 F(("mp_plan_places_head", "mp_plan_places"), 73.0, 62.0, 23.7, 27.0, key="places"),
                 F("mp_plan_caption", 3.3, 90.5, 50.0, 1.8, key="caption")],
         side="places"),
    # 21 · SON page22 (P-13, U15): plans, each section as wide as its plan at its own round scale, key map in the band
    dict(pid="p21", part="E", stage="do", title=u"The water edge at 1:1,000",
         intro=u"Two windows, each *plan with its section*: the *upstream entry* (collect, clean, hold) and *Üç Kemer "
               u"Köprüsü* with Demeter's Garden.",
         frames=[F(("mp_dt_upstream", "mp_dt_dt_upstream"), 3.3, 10.0, 45.7, 43.0, key="d1", same="dplans"),
                 F(("mp_dt_k5", "mp_dt_dt_k5"), 50.0, 10.0, 46.7, 43.0, key="d2", same="dplans"),
                 F(("mp_dt_upstream_sec", "mp_dt_dt_upstream_sec"), 3.3, 54.0, 45.7, 20.0, key="s1", foot=2.5,
                   note="leg1"),
                 F(("mp_dt_k5_sec", "mp_dt_dt_k5_sec"), 50.0, 54.0, 46.7, 25.0, key="s2", foot=2.5, note="leg2"),
                 F(("mp_dt_keymap", "*keymap*"), 38.0, 75.0, 11.0, 13.0, key="km"),
                 F(("mp_dt_*upstream_leg*", "mp_dt_*upstream_route", "mp_dt_*upstream_why"), 3.3, 75.0, 34.0, 18.0,
                   key="leg1"),
                 F(("mp_dt_*k5_leg*", "mp_dt_*k5_route", "mp_dt_*k5_why"), 50.0, 79.5, 46.7, 14.0, key="leg2")],
         side="leg2"),
    dict(pid="p22", kind="sources", part="E", title=u"Sources"),
]
BK_REF_PAGE = "p13"          # D2 reference fill: "Four seasons on one cut" = round 6 p13 (PLAN §2.1)
# ---- 81_ids (round 5 S10; round 6 S9 v31, G6-2): ONE page numbering, group aliases, text clean-up, {src:key} numbers ---
# Round 6 (PLAN §2.1, G6-2): every content script exports the 22-page ids p01 ... p22 itself; the old 25 -> 23 map
# (BK_PAGE_IDS, BK_25_TO_23) is gone. An item exported for a page id outside p01-p22 = WARNING and is not shown.
BK_NPAGES = 22
# Group aliases ("folder/group" -> group): S8 asked agriculture's "stream comes first" block to join the water board's
# group p21_g2_figures (heading + both blocks); agriculture exports it as group "ag1_stream" (S9). Set here, once.
BK_GROUP_ALIAS = {"Bergama_agriculture_alternatives/ag1_stream": "p21_g2_figures"}
BK_SRC_RE = re.compile(r"(?:\s*\{src:([A-Za-z0-9_]+)\})+")
BK_SRC_ONE = re.compile(r"\{src:([A-Za-z0-9_]+)\}")
BK_SRC = dict(order=[], num={}, text={}, missing=set())
BK_FALSE_LABELS = (re.compile(r"\s*·\s*style a(?: \(cutouts\))?", re.I),      # P22 closing row: false crop label
                   re.compile(r"\s*·\s*1:[\d,]+\s*$"))                       # a scale tail the composer now prints


def bk_remap(log):
    """every loaded file: page ids checked (p01-p22, G6-2), group aliases, text clean-up; one log line per file"""
    for folder, d in BK_IX.items():
        bad = []
        for pid, its in (d.get("pages") or {}).items():
            if pid != "any" and (not re.match(r"^p\d\d$", u"%s" % pid) or not 1 <= int(pid[1:]) <= BK_NPAGES):
                bad.append(pid)
                wn_warn(pid, "page", u"%s exports %d items for page %s, not in the 22-page booklet (G6-2): not shown"
                        % (folder, len(its), pid))
            for it in its:
                it["page"] = pid
                g = BK_GROUP_ALIAS.get(u"%s/%s" % (folder, it.get("group")))
                if g:
                    it["group"] = g
                if it.get("kind") == "text":
                    bk_clean_text(it)
        log.append(u"pages %s: %s%s" % (folder, u" ".join(sorted(k for k in (d.get("pages") or {}))),
                                        (u"; not shown " + u" ".join(sorted(bad))) if bad else u""))


def bk_clean_text(it):
    s = u"%s" % it.get("string", u"")
    s = s.replace(u"**", u"*")                  # "**bold**" (water balance, city link) -> the setter's "*bold*"
    for rx in BK_FALSE_LABELS:
        s = rx.sub(u"", s)
    it["string"] = s


def bk_sources_collect():
    """every source row of every file: key -> text (first file wins; a different text for the same key = WARNING)"""
    for folder, d in sorted(BK_IX.items()):
        for k, v in (d.get("sources") or {}).items():
            t = (v or {}).get("text") or u""
            u_ = (v or {}).get("url")
            full = (u"%s, %s" % (t, u_)) if u_ and u_ not in t else t
            if k in BK_SRC["text"] and BK_SRC["text"][k] != full:
                wn_warn(None, "source", u"source key %s has two texts (%s kept)" % (k, folder))
                continue
            BK_SRC["text"].setdefault(k, full)


def bk_src_number(pids):
    """numbers every {src:key} in page order (texts in export order), then rewrites each mark run as "[1, 4]"; a key
    no file defines = WARNING and "[?]" """
    BK_SRC["order"][:] = []
    BK_SRC["num"].clear()
    for pid in pids:
        its = ix_page(pid)
        keys = []
        for it in its:
            for t_ in _bk_src_strings(it):
                keys += BK_SRC_ONE.findall(t_)
            keys += [k_ for k_ in it.get("src_keys") or () if isinstance(k_, str)]   # v31: a drawing's own sources
        keys += [it.get("key") for it in its if it.get("kind") == "source" and it.get("key")]   # page source rows
        for k in keys:
            if True:
                if k not in BK_SRC["num"]:
                    if k not in BK_SRC["text"]:
                        if k not in BK_SRC["missing"]:
                            wn_warn(pid, "source", u"mark {src:%s} has no source row in any items.json" % k)
                        BK_SRC["missing"].add(k)
                        continue
                    BK_SRC["order"].append(k)
                    BK_SRC["num"][k] = len(BK_SRC["order"])

    def rep(m):
        ks = BK_SRC_ONE.findall(m.group(0))
        ns = []
        for k in ks:
            n = BK_SRC["num"].get(k)
            v = u"%d" % n if n else u"?"
            if v not in ns:
                ns.append(v)
        return u" [%s]" % u", ".join(ns)
    n = 0
    for d in BK_IX.values():
        for its in d.get("pages", {}).values():
            for it in its:
                k = it.get("kind")
                if k == "text" and u"{src:" in (it.get("string") or u""):
                    it["string"] = BK_SRC_RE.sub(rep, it["string"]).lstrip()
                    it["short_forms"] = [BK_SRC_RE.sub(rep, t).lstrip() for t in it.get("short_forms") or []]
                    n += 1
                elif k == "legend":                  # v31 (G6-3): plain-string legend texts and titles carry marks too
                    for e in it.get("entries") or ():
                        if isinstance(e.get("text"), str) and u"{src:" in e["text"]:
                            e["text"] = BK_SRC_RE.sub(rep, e["text"]).lstrip()
                            n += 1
                    if isinstance(it.get("title"), str) and u"{src:" in it["title"]:
                        it["title"] = BK_SRC_RE.sub(rep, it["title"]).lstrip()
                        n += 1
                elif k == "list":
                    its_ = it.get("items") or []
                    for i_, t_ in enumerate(its_):
                        if isinstance(t_, str) and u"{src:" in t_:
                            its_[i_] = BK_SRC_RE.sub(rep, t_).lstrip()
                            n += 1
                elif k == "photo" and isinstance(it.get("caption"), str) and u"{src:" in it["caption"]:
                    it["caption"] = BK_SRC_RE.sub(rep, it["caption"]).lstrip()
                    n += 1
    return n


def _bk_src_strings(it):
    """the strings of an item that may carry {src:key} marks, in reading order (text, legend title + entries, list
    rows, photo caption)"""
    k = it.get("kind")
    if k == "text":
        return [it.get("string") or u""]
    out = []
    if k == "legend":
        if isinstance(it.get("title"), str):
            out.append(it["title"])
        out += [e.get("text") for e in it.get("entries") or () if isinstance(e.get("text"), str)]
    elif k == "list":
        out += [t for t in it.get("items") or () if isinstance(t, str)]
    elif k == "photo" and isinstance(it.get("caption"), str):
        out.append(it["caption"])
    return out
# ---- 82_compose (round 5 S10; round 6 S9 v31: G6-1 page frames, G6-7/G6-8, G6-9 log): one content page from its items -
# Round 6 (PLAN §3, G6-1): a page is its FRAMES (80_plan, the SUBMISSION_SON arrangement with the drawings enlarged)
# + every item its scripts exported for it. The v30 rows / right column / share are gone. Steps per page:
#   1. sort the page's items (bk_items) and attach every unanchored text, legend and list to one drawing (bk_attach:
#      its "drawing" key, else the longest drawing id its own id starts with, else the one drawing of its group)
#   2. match: each frame takes the items whose id matches one of its fnmatch patterns (first frame wins; drawings,
#      key maps, texts, legends, lists, photos alike)
#   3. scale: every drawing is scaled UNIFORMLY into its frame (never stretched): maps and sections at the largest
#      Bergama-list scale that fits (frames with the same "same" key share one scale = the smallest of their fits, so
#      p04/p05 cuts and p13 seasons print one scale), diagrams / charts / key maps at the largest factor that fits
#      (<= BK_MM_MAX); an inset at >= 2 x its parent's scale. Heading, level column and the scale band (bar or
#      "1:den" + north arrow, outside the drawing, G6-4) are reserved inside the frame
#   4. draw: heading, drawing (30_render), north, level markers, labels (50_place), scale; then the drawing's attached
#      texts / legends / lists / side-list rows go to the frame's "note" frame, else under the drawing in its own frame,
#      else the page's "side" frame
#   5. every item no frame names and no drawing owns = WARNING "unlisted" and goes to the page's side frame (PLAN §2.2:
#      never lost); frames of one page that overlap = WARNING "frames"; an empty frame = WARNING "missing"
#   6. page number; layout check (70_check: overlaps, edges, empty bands, < 4 pt = one WARNING each, G6-7/G6-8); log
#      "page <pid> frames=<n> placed=<n> unlisted=<n>" and "groups <pid> kinds=<n> elements=<n> untagged=<n>" (G6-9)
# Nothing here raises on layout: every misfit is a WARNING (one run collects all; Aras 1 Nov 17:11).
BK_GAP = 4.0               # mm between cells / rows / right-column blocks (grid gutter)
BK_HEAD_H = 4.5            # heading band over a drawing
BK_SCALE_H = 5.5           # scale bar / "1:den" band under a true-scale drawing
BK_LEVEL_W = 24.0          # level markers + "+43.71 Q500" beside a section (3 gap + 9 marker + 12 label)
BK_NORTH_MM = 4.6          # v31: the north arrow sits in the scale band under the plan, right end (outside, G6-4)
BK_NOTE_GAP = 1.5          # mm between stacked notes / legends / lists


def _bk_pat(p):
    return any(c in p for c in "*?[")


def bk_items(pid):
    its = [it for it in ix_page(pid) if isinstance(it, dict)]
    S = dict(items=its, draw={}, keymaps=[], texts=[], legends=[], lists=[], levels=[], insets=[], photos=[],
             titles=[], used=set())
    ref = set()
    for it in its:
        k = it.get("kind")
        if k == "legend":
            ref.update(e.get("text") for e in it.get("entries") or [] if isinstance(e.get("text"), str))
            if isinstance(it.get("title"), str):
                ref.add(it["title"])
        elif k == "list":
            ref.update(t for t in it.get("items") or [] if isinstance(t, str))
        elif k == "photo" and isinstance(it.get("caption"), str):
            ref.add(it["caption"])
    for it in its:
        k = it.get("kind")
        if k == "drawing":
            if it.get("role") == "keymap":
                S["keymaps"].append(it)
            else:
                S["draw"][it["id"]] = it
        elif k == "text":
            a_ = it.get("anchor")
            if it.get("id") in ref:
                continue
            if isinstance(a_, dict) and a_.get("drawing") and _pl_apt(it) is not None:
                continue                                  # an in-drawing label: placed with its drawing
            if it.get("role") == "title":
                S["titles"].append(it)
            else:
                S["texts"].append(it)
        elif k in ("legend", "list", "photo"):
            S[k + "s"].append(it)
        elif k == "level_column":
            S["levels"].append(it)
        elif k == "inset":
            S["insets"].append(it)
    return S


def bk_attach(S):
    """who belongs to which drawing (see step 1); att[did] = dict(head=[texts], side=[items]); page-level in S["page"]"""
    ids = sorted(S["draw"], key=len, reverse=True)
    groups = {}
    for d in sorted(S["draw"].values(), key=lambda d: (d.get("priority", 5), d["id"])):
        groups.setdefault(d.get("group"), []).append(d["id"])
    att = dict((d, dict(head=[], side=[], levels=[])) for d in S["draw"])
    S["page"], S["intro"] = [], None

    def owner(it):
        a_ = it.get("anchor")
        d = it.get("drawing") or (a_.get("drawing") if isinstance(a_, dict) else None)
        if d in att:
            return d
        iid = u"%s" % it.get("id", u"")
        for d in ids:
            if iid.startswith(d + u"_"):
                return d
        g = groups.get(it.get("group"))
        if g:
            return g[0]
        return None
    for t in S["texts"]:
        d = owner(t)
        if t.get("role") == "intro" and (d is None or not (u"%s" % t.get("id", u"")).startswith(d + u"_")):
            if S["intro"] is None:
                S["intro"] = t
                continue
        if d is None:
            S["page"].append(t)
        elif t.get("role") == "heading" and not att[d]["head"]:
            att[d]["head"].append(t)
        else:
            att[d]["side"].append(t)
    for it in S["legends"] + S["lists"]:
        d = owner(it)
        (att[d]["side"] if d else S["page"]).append(it)
    for it in S["levels"]:
        d = it.get("drawing")
        if d in att:
            att[d]["levels"].append(it)
        else:
            wn_warn(it.get("page"), "levels", u"level column %s names drawing %r, not on this page" % (it.get("id"), d))
    S["att"] = att
    for k in ("side",):
        for d in att:
            att[d][k].sort(key=lambda it: (it.get("priority", 5), {"heading": 0, "note": 1, "caption": 2}.get(
                it.get("role"), 3)))
    S["page"].sort(key=lambda it: it.get("priority", 5))
    return att


# ---- sizes --------------------------------------------------------------------------------------------------------
def _bk_parent(S, did):
    for ins in S["insets"]:
        if ins.get("child") == did:
            return ins.get("parent")
    return None


def _bk_res(S, did):
    """(extra width, extra height) round a drawing: level column, heading, scale band"""
    D = S["draw"][did]
    att = S["att"].get(did, {})
    rw = BK_LEVEL_W if att.get("levels") else 0.0
    band = D.get("units") == "m" or (D.get("north_deg") is not None and D.get("role") != "keymap")
    rh = (BK_HEAD_H if att.get("head") else 0.0) + (BK_SCALE_H if band else 0.0)
    return rw, rh


# ---- drawing ------------------------------------------------------------------------------------------------------
def bk_north(P, rect, deg, did):
    """true-north arrow (plain solid arrow + N, no box) OUTSIDE the drawing (G6-4): in the scale band under it, at its
    right end; deg = north's turn from page-up, counter-clockwise (keymap.py north_items convention; UNVERIFIED
    against each script's own sign)"""
    import math as _m
    h = BK_NORTH_MM
    t = _m.radians(float(deg))
    ux, uy = -_m.sin(t), -_m.cos(t)               # page y down
    px, py = -uy, ux
    cx, cy = rect[2] - h / 2.0 - 0.5, rect[3] + BK_SCALE_H / 2.0 + 0.3
    fx, fy = cx - ux * h / 2.0, cy - uy * h / 2.0

    def R(a, b):
        return (fx + ux * b + px * a, fy + uy * b + py * a)
    ink = "2C2219"
    bk_line(P, [R(0.0, 0.0), R(0.0, 0.62 * h)], ink, 0.6)
    hw = 0.24 * h
    bk_poly(P, [R(0.0, h), R(-hw, 0.52 * h), R(hw, 0.52 * h)], ink, None, 0.1)
    pt = 5.0
    P.tp.put(u"N", cx - h / 2.0 - 0.8, cy + fm_asc_desc(pt, True)[0] / 2.0, pt, True, "R", 0.0, "north", "label", ink,
             (did,))
    P.tp.keep((cx - h / 2.0 - 0.3, cy - h / 2.0 - 0.3, cx + h / 2.0 + 0.3, cy + h / 2.0 + 0.3), "north", did)


def bk_badges(P, placed):
    """marker digits stay ON their discs (S6, S8, S9 §5): set at their first exported position, never moved, never
    shrunk (a free spot elsewhere would leave the disc empty)"""
    T = placed["T"]
    for it in ix_texts(placed["D"]):
        if it.get("role") != "badge":
            continue
        a_ = _pl_apt(it)
        if a_ is None:
            continue
        anchor = T.pt(a_[0], a_[1])
        codes = _pl_codes(it.get("positions") or ["=C"])
        pt = max(float(it.get("size_pt") or grid_role("badge")[0]), GRID_MIN_PT)
        x, y, al = P.tp._at(codes[0], it.get("string", u""), anchor, pt, bool(it.get("bold", True)), 0.0)
        P.tp.put(it.get("string", u""), x, y, pt, bool(it.get("bold", True)), al, 0.0, it.get("id"), "badge",
                 it.get("colour"), (placed["id"], "marker"))


def bk_design_den(D):
    """the scale a true-scale drawing's texts were designed at: "sheet scale 1:N" in its scale_note, else None"""
    import re as _re
    m_ = _re.search(r"sheet scale 1:([0-9][0-9,]*)", u"%s" % (D.get("scale_note") or u""))
    return int(m_.group(1).replace(",", "")) if m_ else None


def bk_place(P, S, did, s, x, y, side):
    """one cell at (x, y) top-left: heading, drawing, north, levels, labels, scale (see step 3) -> placed"""
    D = S["draw"][did]
    att = S["att"].get(did, dict(head=[], side=[], levels=[]))
    rw, rh = _bk_res(S, did)
    dw, dh = sc_size(D, s)
    yy = y
    if att["head"]:
        st_para(P, att["head"][0].get("string", u""), x, y, max(dw + rw, 30.0), BK_HEAD_H - 0.6, "heading",
                justify=False, page=P.pid)
        yy += BK_HEAD_H
    T = BkT(D, s, x, yy)
    placed = rd_drawing(P, D, T)
    S["placed"][did] = placed
    if D.get("north_deg") is not None and D.get("role") != "keymap":
        bk_north(P, T.rect, D["north_deg"], did)
    if D.get("window_m"):                            # p09 windows: one size, framed (no frame in the drawing)
        bk_rect(P, T.rect, None, GRID_INK["ink"], 0.5)
    if not T.den:
        lo = (D.get("fit") or (0.5, 2.0))[0]
        if s < lo - 1e-3:
            wn_warn(P.pid, "scale", u"%s set at x%.2f, below its x%.2f minimum (row too full)" % (did, s, lo))
    for lc in att["levels"]:
        pl_levels(P, lc, placed, "R")
    dden = bk_design_den(D)
    if T.den and dden:                              # v30.3: a board drawing (site board: "sheet scale 1:N") keeps its
        pl_rigid(P, placed, float(dden) / float(T.den))   # own text layout, scaled from its sheet scale to this one
    elif T.den:
        bk_badges(P, placed)
        pl_labels(P, placed, side, roles=("label",))
    else:                                           # v30.3: diagrams keep their own text layout, scaled with them
        pl_rigid(P, placed, s)
    if T.den:
        r = T.rect
        if D.get("scale_bar"):
            pl_scalebar(P, placed, r[0], r[3] + 1.2)
        else:                                       # the drawing carries its own bar (S7 crops): the scale only
            pt = grid_role("caption")[0]
            a_, _d = fm_asc_desc(pt)
            P.tp.put(u"1:{:,}".format(int(T.den)), r[0], r[3] + 1.2 + a_, pt, False, "L", 0.0, None, "scale",
                     GRID_INK["ink"], (), "sb_%s" % did)
    BK_STAT["drawings"] += 1
    BK_STAT["scales"].append(u"%s %s" % (did, (u"1:%d" % T.den) if T.den else (u"x%.2f" % T.k)))
    return placed


def bk_insets(P, S):
    for ins in S["insets"]:
        a, b = S["placed"].get(ins.get("parent")), S["placed"].get(ins.get("child"))
        wi = ins.get("window")
        if a and b and wi and len(wi) == 4:
            p0 = a["T"].pt(wi[0], wi[3])
            p1 = a["T"].pt(wi[2], wi[1])
            bk_rect(P, (min(p0[0], p1[0]), min(p0[1], p1[1]), max(p0[0], p1[0]), max(p0[1], p1[1])), None,
                    GRID_INK["ink"], 0.5)
            bk_rect(P, b["rect"], None, GRID_INK["ink"], 0.5)


# ---- right column -------------------------------------------------------------------------------------------------
def bk_side_item(P, it, x, y, w, ybot):
    """one attached thing in the right column at (x, y): returns the height used"""
    h = max(4.0, ybot - y)
    k = it.get("kind")
    if k == "text":
        role = it.get("role") or "note"
        if role not in GRID_ROLE_PT:
            role = "note"
        hh, _s = st_para(P, it.get("string", u""), x, y, w, h, role, justify=role != "heading", page=P.pid)
        return hh
    if k == "legend":
        b = pl_legend(P, it, x, y, w, h, 2)
        return b[3] - b[1]
    if k == "list":
        b = pl_list(P, it, x, y, w, h)
        return b[3] - b[1]
    return 0.0


# ---- the page -----------------------------------------------------------------------------------------------------
BK_STAT = dict(drawings=0, scales=[], pages=[])




# ---- frames (v31, G6-1) -------------------------------------------------------------------------------------------
def _bk_frames(spec, pid):
    """the page plan's frames -> [dict(key, pats, mm box, opts)]; overlapping frames = WARNING "frames" (a plan error;
    a frame marked over=True may sit on another, e.g. p03's list over the axo's empty corner)"""
    out = []
    for f in spec.get("frames") or []:
        pats = [f["ids"]] if isinstance(f["ids"], str) else list(f["ids"])
        out.append(dict(f, pats=pats, key=f.get("key") or pats[0], mm=bk_pct(f["box"])))
    for i, a in enumerate(out):
        for b in out[i + 1:]:
            if a.get("over") or b.get("over"):
                continue
            ox = min(a["mm"][2], b["mm"][2]) - max(a["mm"][0], b["mm"][0])
            oy = min(a["mm"][3], b["mm"][3]) - max(a["mm"][1], b["mm"][1])
            if ox > 0.5 and oy > 0.5:
                wn_warn(pid, "frames", u"frames %s and %s overlap %.0f x %.0f mm (page plan)" % (a["key"], b["key"],
                                                                                              ox, oy))
    return out


def _bk_pool(S):
    """every placeable item of the page, in export order: (id, kind, item); kind drawing | keymap | text | legend |
    list | photo"""
    out = [(d, "drawing", S["draw"][d]) for d in sorted(S["draw"], key=lambda d: (S["draw"][d].get("priority", 5), d))]
    out += [(k.get("id"), "keymap", k) for k in S["keymaps"]]
    heads = set(id(h) for a in S["att"].values() for h in a["head"])      # set over their drawing by bk_place
    out += [(t.get("id"), "text", t) for t in S["texts"] if t is not S.get("intro") and id(t) not in heads]
    out += [(it.get("id"), k, it) for k in ("legend", "list", "photo") for it in S[k + "s"]]
    return out


def _bk_match(S, frames):
    """each frame's items in pattern order (first frame wins); returns the set of matched item object ids"""
    pool = _bk_pool(S)
    got = set()
    for F in frames:
        F["items"] = []
        for p in F["pats"]:
            for iid, k, it in pool:
                if id(it) in got or iid is None:
                    continue
                if (fnmatch.fnmatchcase(iid, p) if _bk_pat(p) else iid == p):
                    got.add(id(it))
                    F["items"].append((iid, k, it))
    return got


def _bk_fit(S, did, w, h, pid):
    """the uniform size of drawing did in a w x h mm box: den (maps, sections: the largest list scale that fits) or
    factor (diagrams, charts, key maps: the largest that fits, <= BK_MM_MAX); reserves its heading / levels / band"""
    D = S["draw"].get(did) or ix_get(did)
    rw, rh = _bk_res(S, did) if did in S["draw"] else (0.0, 0.0)
    if D.get("units") == "m" and D.get("role") != "keymap":
        return sc_pick(D, max(1.0, w - rw), max(1.0, h - rh), page=pid)
    return sc_factor(D, max(1.0, w - rw), max(1.0, h - rh), pid)


def _bk_boxes(F, n):
    """a frame's box (less its "foot") cut into n cells: side by side (split "row") or stacked ("col"); default along
    its longer side"""
    b = F["mm"]
    if F.get("foot"):                              # room kept under the drawings for their notes (% of the page)
        b = (b[0], b[1], b[2], max(b[1] + 5.0, b[3] - float(F["foot"]) * BK_PCT[1]))
    if n <= 1:
        return [b]
    sp = F.get("split") or ("row" if (b[2] - b[0]) >= (b[3] - b[1]) else "col")
    return lay_split(b, n, BK_GAP, vertical=(sp == "col"))


def _bk_same(S, frames, pid):
    """frames sharing a "same" key: one scale (the smallest print of their fits) / one factor (the smallest)"""
    val = {}
    for F in frames:
        k = F.get("same")
        if not k:
            continue
        ds = [(iid, kk) for iid, kk, _it in F["items"] if kk in ("drawing", "keymap")]
        for (did, kk), b in zip(ds, _bk_boxes(F, len(ds))):     # the same cells as _bk_frame_draw
            if kk != "drawing" or _bk_parent(S, did):
                continue
            s = _bk_fit(S, did, b[2] - b[0], b[3] - b[1], pid)
            m = S["draw"][did].get("units") == "m"
            cur = val.get(k)
            if cur is None:
                val[k] = (m, s)
            elif cur[0] != m:
                wn_warn(pid, "scale", u"frames \"%s\" mix maps and diagrams: %s keeps its own size" % (k, did))
            else:
                val[k] = (m, max(cur[1], s) if m else min(cur[1], s))
    return val


class _BkTgt(object):
    """a place where notes stack: a box and its running y"""
    def __init__(self, key, box, y=None):
        self.key, self.box, self.y, self.over = key, box, box[1] if y is None else y, False


def _bk_put(P, tg, it):
    """one text / legend / list at the target's running y; past the box foot = one WARNING "overrun" per target"""
    x0, _y0, x1, y1 = tg.box
    if it.get("kind") == "photo":
        hh = _bk_photo_grid(P, [it], (x0, tg.y, x1, y1))
    else:
        hh = bk_side_item(P, it, x0, tg.y, x1 - x0, y1)
    tg.y += hh + BK_NOTE_GAP
    if tg.y > y1 + 0.5 and not tg.over:
        tg.over = True
        wn_warn(P.pid, "overrun", u"frame %s: its texts run %.0f mm past its foot (y %.0f mm)" % (tg.key, tg.y - y1, y1))
    return hh


def _bk_photo_grid(P, photos, box):
    """photos in a grid filling the box (proportions kept, never stretched); captions under each; -> height used"""
    if not photos:
        return 0.0
    import math as _m
    x0, y0, x1, y1 = box
    w, h = x1 - x0, max(8.0, y1 - y0)
    n = len(photos)
    cols = max(1, min(n, int(round(_m.sqrt(n * w / h))) or 1))
    rows = -(-n // cols)
    cw = (w - BK_GAP * (cols - 1)) / float(cols)
    ch = (h - BK_GAP * (rows - 1)) / float(rows)
    ybot = y0
    for i, ph in enumerate(photos):
        c, r = i % cols, i // cols
        cx, cy = x0 + c * (cw + BK_GAP), y0 + r * (ch + BK_GAP)
        cap = ph.get("caption")
        t = ix_text(cap, ph.get("_folder")) if cap else u""
        ch_img = ch - (6.0 if t else 0.0)
        bx = pl_photo(P, ph, cx, cy, cw, max(4.0, ch_img))
        yb = bx[3] if bx else cy
        if t:
            h2, _s = st_para(P, t, cx, yb + 0.8, cw, 5.2, "caption", page=P.pid)
            yb += h2 + 0.8
        ybot = max(ybot, yb)
    return ybot - y0


def _bk_frame_draw(P, S, F, same, tg_of, pid):
    """the drawings of one frame (see steps 3-4); returns [did]"""
    ds = [(iid, kk, it) for iid, kk, it in F["items"] if kk in ("drawing", "keymap")]
    out, bottom = [], F["mm"][1]
    al = (F.get("al") or "TL").upper()
    for (did, kk, it), b in zip(ds, _bk_boxes(F, len(ds))):
        w, h = b[2] - b[0], b[3] - b[1]
        if kk == "keymap":
            f = sc_factor(it, w, h, pid)
            dw, dh = sc_size(it, f)
            ox = b[0] + {"C": (w - dw) / 2.0, "R": w - dw}.get(al[1:2], 0.0)
            oy = b[1] + {"M": (h - dh) / 2.0, "B": h - dh}.get(al[:1], 0.0)
            pl = pl_mm_drawing(P, it, ix_texts(it), ox, oy, dw, dh, "L")
            BK_STAT["drawings"] += 1
            bottom = max(bottom, pl["rect"][3])
            out.append(did)
            continue
        D = S["draw"][did]
        rw, rh = _bk_res(S, did)
        par = _bk_parent(S, did)
        if par and D.get("units") == "m":
            pp = S["placed"].get(par)
            if pp and pp["T"].den:
                s = sc_inset_den(pp["T"].den, D, max(1.0, w - rw), max(1.0, h - rh), pid)
            else:
                wn_warn(pid, "scale", u"inset %s placed before its parent %s (page plan order): own fit" % (did, par))
                s = _bk_fit(S, did, w, h, pid)
        elif F.get("same") in same and same[F["same"]][0] == (D.get("units") == "m"):
            s = same[F["same"]][1]
        else:
            s = _bk_fit(S, did, w, h, pid)
        dw, dh = sc_size(D, s)
        tw, th = dw + rw, dh + rh
        ox = b[0] + {"C": (w - tw) / 2.0, "R": w - tw}.get(al[1:2], 0.0)
        oy = b[1] + {"M": (h - th) / 2.0, "B": h - th}.get(al[:1], 0.0)
        side = TpSideList(u"%s %s" % (pid, did))
        pl = bk_place(P, S, did, s, ox, oy, side)
        yb = pl["rect"][3] + (BK_SCALE_H if (pl["T"].den or D.get("north_deg") is not None) else 0.0)
        bottom = max(bottom, yb)
        out.append(did)
        if side.entries:                           # labels that fell back to numbers: their rows with the notes
            tg = tg_of(F, did)
            tg.y += pl_side_rows(P, side, tg.box[0], tg.y, tg.box[2] - tg.box[0], max(4.0, tg.box[3] - tg.y)) + \
                BK_NOTE_GAP
    return out, bottom


def bk_content_page(doc, spec, n, lines):
    """one content page from its frames (see the part notes)"""
    pid = spec["pid"]
    S = bk_items(pid)
    S["placed"] = {}
    bk_attach(S)
    P = bk_page(doc, pid, n)
    intro = S["intro"].get("string") if S["intro"] else spec.get("intro")
    part = spec.get("part")
    bk_band(P, (u"%s  %s" % (part, PARTS.get(part, u""))).upper() if part else None, spec["title"], intro)
    frames = _bk_frames(spec, pid)
    framed = _bk_match(S, frames)
    same = _bk_same(S, frames, pid)
    tg = {}
    for F in frames:
        tg[F["key"]] = _BkTgt(F["key"], F["mm"])
    side_key = spec.get("side")
    if side_key not in tg:
        wn_warn(pid, "frames", u"the page plan names no side frame (%r): unlisted items go under the last frame"
                % side_key)
        side_key = frames[-1]["key"] if frames else None
    if side_key is None:
        tg[None] = _BkTgt(None, GRID_AREA)

    def tg_of(F, did=None):
        """where a drawing's notes go: its frame's "note" frame, else under it in its own frame, else the side"""
        k = F.get("note")
        if k in tg:
            return tg[k]
        t = tg[F["key"]]
        if t.box[3] - t.y >= 8.0:
            return t
        return tg[side_key]
    owner_f = {}
    n_placed = 0
    for F in frames:
        if not F["items"]:
            if not F.get("opt"):
                wn_warn(pid, "missing", u"frame %s: nothing exported for %s (its script not run, or the id changed)"
                        % (F["key"], u", ".join(F["pats"])))
            continue
        ds, bottom = _bk_frame_draw(P, S, F, same, tg_of, pid)
        for d in ds:
            owner_f[d] = F
        if ds:
            tg[F["key"]].y = bottom + BK_NOTE_GAP
        photos = [it for _i, kk, it in F["items"] if kk == "photo"]
        if photos:
            t = tg[F["key"]]
            t.y += _bk_photo_grid(P, photos, (t.box[0], t.y, t.box[2], t.box[3])) + BK_NOTE_GAP
        for _i, kk, it in F["items"]:
            if kk in ("text", "legend", "list"):
                _bk_put(P, tg[F["key"]], it)
        n_placed += len(F["items"])
    bk_insets(P, S)
    # a placed drawing's attached items that no frame names: with their drawing
    n_att = 0
    for did, F in owner_f.items():
        for it in S["att"].get(did, {}).get("side", []):
            if id(it) not in framed:
                framed.add(id(it))
                _bk_put(P, tg_of(F, did), it)
                n_att += 1
    # everything else: unlisted -> the side frame, WARNING (never lost)
    unl = [(iid, kk, it) for iid, kk, it in _bk_pool(S) if id(it) not in framed]
    for iid, kk, it in sorted(unl, key=lambda r: u"%s" % r[0]):
        wn_warn(pid, "unlisted", u"%s %s is in no frame of the page plan: set in the side frame %s" % (kk, iid, side_key))
        t = tg[side_key]
        if kk in ("drawing", "keymap"):
            Fx = dict(key=u"side %s" % iid, mm=(t.box[0], t.y, t.box[2], max(t.y + 10.0, t.box[3])),
                      items=[(iid, kk, it)])
            _ds, bottom = _bk_frame_draw(P, S, Fx, {}, lambda F_, d_=None: t, pid)
            t.y = bottom + BK_NOTE_GAP
            if t.y > t.box[3] + 0.5:
                wn_warn(pid, "overrun", u"side frame %s: %s runs past its foot" % (side_key, iid))
        else:
            _bk_put(P, t, it)
    bk_pageno(P, n)
    ck_page(P)
    bk_finish(P)
    g = BK_GRP.get(pid, dict(kinds=set(), elements=set(), untagged=0))
    lines.append(u"page %s frames=%d placed=%d unlisted=%d (attached notes %d)" % (pid, len(frames), n_placed,
                                                                                len(unl), n_att))
    if "wp_groups_log" in globals():                # S2's writer counts what it actually wrote
        lines.append(wp_groups_log(pid))
    else:
        lines.append(u"groups %s kinds=%d elements=%d untagged=%d" % (pid, len(g["kinds"]), len(g["elements"]),
                                                                    g["untagged"]))
    lines.append(u"page %d %s: drawings %s" % (
        n, pid, u", ".join(u"%s %s" % (d, (u"1:%d" % p_["T"].den) if p_["T"].den else (u"x%.2f" % p_["T"].k))
                           for d, p_ in S["placed"].items())))
    return P
# ---- 83_cover_sources (round 5 S10; round 6 S9 v31: G6-2 contents, G6-3 Sources last): the two pages the booklet draws
# v31: contents list the 22 pages of PLAN §2.1 from BK_PAGES (Sources = page 22, the last row of part E); the Sources
# page has the v31 title band, four text columns (five when four would need < 4.5 pt), entries "[n] text" numbered in
# page order with a hanging indent, left-aligned (lists, not justified), 4.5-5 pt (frames_p14-22 "new page 22").
# Cover (P01.1): the cover photo (Data/COVER_IMG) fills the WHOLE page behind everything (full bleed, proportions kept,
# the overflow cut by the page edge) under a white veil of COVER_VEIL opacity, so the photo shows very light and the
# text stays readable. Left: course, MIRAQUA, title, subtitle, the approved text, names, date. Right (P01.2): contents
# of the 22 pages (theme, stage, page title with its number).
# Sources: every source cited on a page ({src:key} marks and the scripts' page source rows), numbered in page order as
# the pages print them (81_ids bk_src_number), then the masterplan's numbered places, the relief's height data and the
# assets (scale figures, silhouettes, cutouts) once each, under their headings (round 4 rules kept).
BK_ASSET_SOURCES = [
    u"Scale figures: Wijayarathna S., Architectural human figures sketches (set 1), https://sashx.gumroad.com/l/gSAgZ",
    u"Scale figures: studio_articulation, Sketchy Human Figures 2, "
    u"https://learnarchitecture.online/products/sketchy-human-figures-2",
    u"Scale figures: studio_articulation, Sketchy Human Figures 3, "
    u"https://learnarchitecture.online/products/sketchy-human-figures-3"]          # v21-v29 list, unchanged
ELEV_SOURCES = [
    u"Site survey, Bergama (course file), contours 1-10 m: the ground inside the site frame",
    u"Copernicus DEM GLO-30, ESA / DLR / Airbus, TanDEM-X 2011-2015; https://dataspace.copernicus.eu/explore-data/"
    u"data-collections/copernicus-contributing-missions/collections-description/COP-DEM; © DLR e.V. 2010-2014 and © "
    u"Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA"]   # v25-v29


def bk_cover(doc, n, lines):
    import fitz as _fz
    P = bk_page(doc, "p01", n)
    W_, H_ = GRID_PAGE
    path = os.path.join(BERGAMA_ROOT, "Data", COVER_IMG)
    if os.path.isfile(path):
        try:
            pm = _fz.Pixmap(path)
            pw, ph = float(pm.width), float(pm.height)
            pm = None
            s = max(W_ / pw, H_ / ph)
            iw, ih = pw * s, ph * s
            x0, y0 = (W_ - iw) / 2.0, (H_ - ih) / 2.0
            P.page.insert_image(_fz.Rect(x0 * BK_K, y0 * BK_K, (x0 + iw) * BK_K, (y0 + ih) * BK_K), filename=path,
                                keep_proportion=False)
            sh = P.page.new_shape()
            sh.draw_rect(P.page.rect)
            sh.finish(color=None, fill=(1, 1, 1), fill_opacity=COVER_VEIL)
            sh.commit()
            P.ink.append(("photo", (0.0, 0.0, W_, H_), "cover"))
            lines.append(u"cover photo %s full bleed, veil %.2f (photo at %.0f %%)" % (COVER_IMG, COVER_VEIL,
                                                                                       100 * (1 - COVER_VEIL)))
        except Exception as ex:
            wn_warn("p01", "photo", u"cover photo %s unreadable (%s)" % (COVER_IMG, type(ex).__name__))
    else:
        wn_warn("p01", "photo", u"cover photo missing: copy %s into Downloads/Bergama/Data/" % COVER_IMG)
    ink, acc = GRID_INK["ink"], GRID_INK["accent"]
    x = GRID_ML
    lw = 225.0
    st_line(P, BOOK["course"].upper(), x, 18.0, 8.0, True, acc, role="title")
    st_line(P, BOOK["hook"], x, 64.0, 48.0, True, acc, role="title")
    y = 82.0
    hh, _s = st_para(P, BOOK["title"], x, y - 8.0, lw, 24.0, "title", pt=24.0, bold=True, justify=False)
    y += hh
    st_line(P, BOOK["subtitle"], x, y + 6.0, 14.0, False, ink, role="title")
    y += 16.0
    hh, _s = st_para(P, COVER_TEXT, x, y, 205.0, 40.0, "intro", pt=9.5)
    yb = 250.0
    for nm in BOOK["names"]:
        st_line(P, nm, x, yb, 9.5, False, ink, role="intro")
        yb += 4.4
    st_line(P, BOOK["date"], x, 272.0, 7.5, False, GRID_INK["ink2"], role="caption")
    # contents (P01.2, G6-2): from column 9 (x = 14 + 8 x 33 = 66.2 % as SON), 22 pages
    cx = GRID_ML + 8 * 33.0
    st_line(P, u"CONTENTS", cx, 18.0, 8.0, True, acc, role="title")
    rows, last, lst = [], None, None
    for i, sp in enumerate(BK_PAGES, 1):
        if i == 1:
            continue
        if sp.get("kind") == "sources":          # v31: the last row of part E (frames_p01-08 page 1 target)
            rows.append(("title", sp["title"], i))
            continue
        if sp.get("part") != last:
            last, lst = sp.get("part"), None
            if rows:
                rows.append(("gap", None, None))
            rows.append(("part", (last + u"  " + PARTS.get(last, u"")).upper(), None))
        if sp.get("stage") != lst:
            lst = sp.get("stage")
            rows.append(("stage", STAGES.get(lst, u""), None))
        rows.append(("title", sp["title"], i))
    step = dict(part=5.2, stage=4.4, title=4.4, gap=3.0)
    need = sum(step[k] for k, _t, _n in rows)
    f = max(1.0, min(1.35, (272.0 - 30.0) / need)) if need else 1.0
    cy = 30.0
    for k, t, no in rows:
        if k == "part":
            st_line(P, t, cx, cy, 8.0, True, acc, role="title")
        elif k == "stage":
            st_line(P, t, cx + 9.0, cy, 6.5, True, "5C7A86", role="heading")
        elif k == "title":
            st_line(P, u"%d" % no, cx + 6.0, cy, 7.0, True, GRID_INK["ink2"], "R", role="list_item")
            st_line(P, t, cx + 9.0, cy, 7.0, False, ink, role="list_item")
        cy += step[k] * f
    if cy > 276.0:
        wn_warn("p01", "overrun", u"contents run to %.0f mm, past the margin" % cy)
    lines.append(u"contents: %d pages listed" % sum(1 for k, _t, _n in rows if k == "title"))
    ck_page(P)
    bk_finish(P)
    return P


def _bk_cutout_sources():
    p_ = os.path.join(BERGAMA_ROOT, "Data", "cutouts", "cutouts.json")
    try:
        with open(p_, encoding="utf-8") as f_:
            d_ = json.load(f_).get("cutouts") or {}
    except Exception:
        return []
    out = []
    for key, ents in sorted(d_.items()):
        for e_ in (ents if isinstance(ents, list) else [ents]):
            t = (u"%s" % ((e_ or {}).get("source") or u"")).strip() if isinstance(e_, dict) else u""
            if t and t not in out:
                out.append(t)
    return [u"Cutout: " + t for t in out]


def bk_source_groups(lines):
    groups = [(u"SOURCES, IN PAGE ORDER", [u"[%d] %s" % (i, BK_SRC["text"][k]) for i, k in
                                           enumerate(BK_SRC["order"], 1)])]
    mp = BK_IX.get("bergama_masterplan", {}).get("extra", {}).get("plan_sources")
    if mp:
        rows = []
        if isinstance(mp, dict):                           # v30.1 (closing): masterplan plan_sources dict
            for m_ in mp.get("markers") or ():             # (p23_plan.py: crop, heading, markers, left_as_is)
                if not isinstance(m_, dict):
                    continue
                ts = [(u"%s" % ((s_ or {}).get("text") or u"")).strip() for s_ in m_.get("sources") or ()
                      if isinstance(s_, dict)]
                ts = [t for t in ts if t]
                if ts:
                    rows.append(u"%s %s: %s" % (m_.get("n", u""), m_.get("name") or u"", u"; ".join(ts)))
        else:
            for r in (mp if isinstance(mp, list) else []):
                rows.append(u" · ".join(u"%s" % v for v in r) if isinstance(r, (list, tuple)) else u"%s" % r)
        if rows:
            groups.append((u"SOURCES OF THE NUMBERED PLACES ON THE MASTERPLAN", rows))
    groups.append((u"HEIGHT DATA", list(ELEV_SOURCES)))
    hr = []
    if "hr_sources" in globals():
        try:
            hr = list(hr_sources())
        except Exception:
            hr = []
    assets = []
    for t in hr + BK_ASSET_SOURCES + _bk_cutout_sources():
        if t not in assets:
            assets.append(t)
    groups.append((u"ASSETS", assets))
    unused = [k for d in BK_IX.values() for k in (d.get("sources") or {}) if k not in BK_SRC["num"]]
    lines.append(u"sources: %d cited in page order; %d rows of the scripts not cited on any page, left out%s" % (
        len(BK_SRC["order"]), len(unused), (u" (" + u", ".join(sorted(set(unused))[:30]) + u")") if unused else u""))
    return [(h, r) for h, r in groups if r]


BK_SRC_COLS = {4: [(3.0, 22.0), (26.0, 22.0), (50.0, 22.0), (73.0, 24.0)],          # % of the page (x, w)
               5: [(3.0, 17.6), (22.0, 17.6), (41.0, 17.6), (60.0, 17.6), (79.0, 18.0)]}
BK_SRC_Y = (10.0, 92.0)            # % of the page: columns top / foot
BK_SRC_PT = (5.0, 4.5)             # largest / smallest size before a fifth column (then down to GRID_MIN_PT)
BK_SRC_IND = 4.6                   # mm: the hanging indent of an entry ("[142] " at 5 pt is about 4.2 mm)
_BK_SRC_NUM = re.compile(r"^(\[\d+\])\s+")


def _bk_src_h(k, t, cw, s):
    if k == "heading":
        return st_fit(t, cw, None, "heading", 6.0, justify=False, page="sources")[3] + 1.4
    m_ = _BK_SRC_NUM.match(t)
    body = t[m_.end():] if m_ else t
    return st_fit(body, cw - (BK_SRC_IND if m_ else 0.0), None, "source", s, justify=False, page="sources")[3] + 0.9


def bk_sources(doc, n, lines, pid="p22", title=u"Sources", part=None):
    """the Sources page(s), see the part notes; a second page only if even five columns at 4 pt do not hold them"""
    groups = bk_source_groups(lines)
    flat = []
    for h, rows in groups:
        flat.append(("heading", h))
        flat += [("source", r) for r in rows]
    y0, y1 = BK_SRC_Y[0] * BK_PCT[1], BK_SRC_Y[1] * BK_PCT[1]
    colh = y1 - y0
    pick = None
    for ncol, lo in ((4, BK_SRC_PT[1]), (5, GRID_MIN_PT)):
        cw = BK_SRC_COLS[ncol][-2][1] * BK_PCT[0]
        s = BK_SRC_PT[0]
        while True:
            hs = [_bk_src_h(k, t, cw, s) for k, t in flat]
            if sum(hs) <= ncol * colh * 0.96 or s - 0.25 < lo - 1e-6:
                break
            s -= 0.25
        pick = (ncol, s, hs)
        if sum(hs) <= ncol * colh * 0.96:
            break
    ncol, s, hs = pick
    cols = [(x * BK_PCT[0], w * BK_PCT[0]) for x, w in BK_SRC_COLS[ncol]]
    label = (u"%s  %s" % (part, PARTS.get(part, u""))).upper() if part else None
    pages, P, col, y = [], None, 0, y0
    for (k, t), hh in zip(flat, hs):
        if P is None or y + hh > y1 + 1e-6:
            if P is not None:
                col += 1
                y = y0
            if P is None or col >= ncol:
                if P is not None:
                    bk_pageno(P, n + len(pages) - 1)
                    ck_page(P)
                    bk_finish(P)
                P = bk_page(doc, pid, n + len(pages))
                bk_band(P, label, title if not pages else title + u" (continued)")
                pages.append(P)
                col, y = 0, y0
        cx, cw = cols[col]
        if k == "heading":
            st_para(P, t, cx, y, cw, None, "heading", 6.0, justify=False, page=pid)
        else:
            m_ = _BK_SRC_NUM.match(t)
            if m_:                                  # hanging indent: the number, then the text block beside it
                a_, _d = fm_asc_desc(s)
                P.tp.put(m_.group(1), cx, y + a_, s, False, "L", 0.0, None, "source", GRID_INK["ink2"], ())
                st_para(P, t[m_.end():], cx + BK_SRC_IND, y, cw - BK_SRC_IND, None, "source", s, justify=False,
                        page=pid)
            else:
                st_para(P, t, cx, y, cw, None, "source", s, justify=False, page=pid)
        y += hh
    if P is not None:
        bk_pageno(P, n + len(pages) - 1)
        ck_page(P)
        bk_finish(P)
    if len(pages) > 1:
        wn_warn(pid, "overrun", u"the sources need %d pages at %.2f pt in %d columns (the booklet has %d + %d)" % (
            len(pages), s, ncol, n, len(pages) - 1))
    lines.append(u"sources page: %d rows at %.2f pt, %d columns, %d page(s)" % (len(flat), s, ncol, len(pages)))
    return len(pages)
TRIG_WHY = [None]
OUT_DIR = bg_output(OUT_FOLDER)
LOG_DIR = bg_logs()
BK_EXPECT = ("selinus_board", "bergama_masterplan", "Bergama_water_balance_analysis", "Bergama_agriculture_alternatives",
             "bergama_water_board", "bergama_proposal_sections", "Bergama_city_link_analysis")


def main():
    """the booklet: load every items.json, one page numbering, number the sources, compose the 23 pages, check, save"""
    import fitz                                   # PyMuPDF
    t0 = time.time()
    wn_reset()
    ck_reset()
    tp_log_lines()                                # no text log lines left from an earlier run
    BK_STAT.update(drawings=0, scales=[], pages=[])
    BK_GRP.clear()
    del BK_PAGENO_LOG[:]
    lines = []
    ix_load_all(need=())
    for f in BK_EXPECT:
        if f not in BK_IX:
            wn_warn(None, "missing", u"no items.json from %s (cached/booklet/%s/): run that script first; its pages "
                    u"stay empty" % (f, f))
    bk_remap(lines)
    lines.append(u"glyph U+0131 dotless i: %s in the booklet font (Arial, %s)" % (
        u"mapped" if not fm_safe(u"\u0131", False)[1] and not fm_safe(u"\u0131", True)[1] else u"MISSING",
        bk_font_files()[0]))
    bk_sources_collect()
    pids = [sp["pid"] for sp in BK_PAGES if not sp.get("kind")]
    n_marks = bk_src_number(pids)
    lines.append(u"source marks rewritten in %d texts; %d sources numbered" % (n_marks, len(BK_SRC["order"])))
    os.makedirs(OUT_DIR, exist_ok=True)
    doc = fitz.open()
    n_src = 0
    for n, sp in enumerate(BK_PAGES, 1):
        try:
            if sp.get("kind") == "cover":
                bk_cover(doc, n, lines)
            elif sp.get("kind") == "sources":
                n_src = bk_sources(doc, n, lines, sp["pid"], sp.get("title", u"Sources"), sp.get("part"))
            else:
                bk_content_page(doc, sp, n, lines)
        except Exception as ex:                   # a page that fails is a WARNING; the others still build
            import traceback as _tb
            wn_warn(sp["pid"], "page", u"page %d not composed: %s: %s | %s" % (
                n, type(ex).__name__, ex, _tb.format_exc().strip().splitlines()[-3:]))
            if doc.page_count < n:
                doc.new_page(width=GRID_PAGE[0] * BK_K, height=GRID_PAGE[1] * BK_K)
    lines.extend(BK_PAGENO_LOG)
    ck_finish(BK_REF_PAGE)
    try:
        doc.subset_fonts()
    except Exception:
        pass
    out = os.path.join(OUT_DIR, PDF_NAME)
    doc.save(out, garbage=3, deflate=True)
    npg = doc.page_count
    doc.close()
    rd_close()
    head = [u"%s  %s  (%d pages, %s)" % (out, time.strftime("%H:%M:%S"), npg, VERSION),
            u"trigger: %s" % (TRIG_WHY[0] or u"run outside Grasshopper")]
    lines.append(u"%s %s, %d drawings placed, %.1f s" % (GH_LABEL, VERSION, BK_STAT["drawings"], time.time() - t0))
    return u"\n".join(wn_compose(tp_log_lines() + lines, head))


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


# ---- Grasshopper wiring (same in every script; never define a function named run: it would hide the input) ----
if "ghenv" in globals():
    import scriptcontext as _sc
    _k = "bergama_" + OUT_FOLDER
    try:
        _k += ":" + str(ghenv.Component.InstanceGuid)   # noqa: F821
    except Exception:
        pass
    _pressed, _why, _btn = trig_should_run("bergama_booklet_chain")
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
    log = _sc.sticky.get(_k + "_log", "Press the Button to build " + os.path.join(OUT_DIR, PDF_NAME))
    print(log)
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(_k + "_status", "idle")  # noqa: F821
    except Exception:
        pass
else:
    print(write_log(main()))
