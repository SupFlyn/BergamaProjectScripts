# -*- coding: utf-8 -*-
# r: pymupdf==1.26.5
# CURRENT VERSION: bergama_booklet_v38_1.py = v38.1 (12 Nov 2026: p13 season cuts from SectionFromLine); v38 (11 Nov 2026, round 9 Part BK: frames from the round 9 table R9_FRAMES, free scale with the round label rule (bar at the true scale, label printed), map windows round the focus, badges / tags / card boxes centred on their ink, B19 on p20, underfill / cover checks; see NEW IN v38); v37 (8 Nov 2026, round 8: absolute frames + uniform fit +-6 %, no flow; see NEW IN v37); v35 (5 Nov 2026: editable layout table Data/booklet_layout.csv + flow: blocks at their table place and scale, grown to fit, shifted off each other, scale never changed; see NEW IN v35); v33 (round 7 S7, 5 Nov 2026: every block at its SON frame (mm) and SON printed scale, nothing fitted, misfit = WARNING; kicker "· PART" and footer label; see NEW IN v33); v32 (L1, 4 Nov 2026: the booklet PLACES everything: one box per drawing, labels moved / led out never shrunk, pages justified; see NEW IN v32); v31 (round 6 S9, 4 Nov 2026: 22 pages p01-p22 in the PLAN §2.1 order, each page
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
NEW IN v38 (round 9 Part BK, 11 Nov 2026; revision_2026-11-11_round9: BRIEF G9-1, G9-2, G9-6, ADDENDUM A1 §0, §B, §E,
F2.2-F2.4, A9, PLAN §cause c1-c3, d1-d10, e1-e2, f2, f4):
  * FRAMES from R9_FRAMES (frames_r9, the one table of round 9, pasted before 80_plan): every page 2-21 is built from it
    (bk_r9_frames; kind S / M / F / C / T, series, r8, bar, split, gap, cols, pt, merge, grid, card, over, allow, opt).
  * SCALE (ADDENDUM §0): Tfit measured in the frame; the producer's true scale is kept when it fits, else r9_label
    (round labels, the second list only under §0.4); a series shares one T and one label (pre-pass after _bk_match);
    the bar is drawn at the true scale T, the label L is printed; "{scale:<id>}" tokens become "1:L"; log
    "scale <page> <block> fit 1:<Tfit> true 1:<T> label 1:<L> list <round|second> size <%>".
  * M MAPS: the focus box is fitted; the window = the frame at T centred on the focus, clamped to the exported extent;
    texts outside the window are dropped and counted (log "window ...").
  * F frames: uniform fit, largest that fits (WARNING "text<4pt" when the fit would set text under 4 pt); C frames keep
    the 1.15 cap; T frames never grow a drawing; board texts at factor 1.0.
  * BADGES / TAGS (G9-1): bk_centre sets a glyph on the middle of its INK box ("MC" is ink-centred everywhere); S1
    badges draw their disc (fill, ring, r_mm) at print size, their disc polys are skipped; tags draw their box; card
    boxes on p09 (grey frame, bar in the hub colour, K-tile, fixed texts); log "centre <page> n=".
  * PHOTOS centre-cropped to their cell; BK_GAP 2 mm; scale bar steps add 25 and 250; B19 line opacity drawn.
  * CHECKS: WARNING "<page> <block> underfill <%>" (frame used < 80 %), "<page> cover <%>" (page < 85 %), "empty",
    "overlap" (p03 list on the axonometric, then the list moves down the right edge); page_boxes.csv gains "used".
  * Layout table plan "v38" (frames written with one decimal); BK_EXPECT + bergama_b19_plan.
NEW IN v37 (round 8 S6, 8 Nov 2026; revision_2026-11-08_round8/PLAN.md §cause, BRIEF §3 L1-L4, §8):
  * ABSOLUTE FRAMES: every block sits in its table frame; nothing flows, grows or is pushed (the v35 flow, the v34 pack and
    their helpers deleted). FIT (bk_fit): one uniform factor per frame (a split group fitted as one), true scale within
    +-6 % of the printed one (else WARNING "<page> <drawing> fit true 1:n needed 1:m", overflow, nothing moves); scale
    bar at the true scale, printed ratio = the table's; diagrams / charts / key maps free fit up to x1.15.
  * Title band = SON page2 (kicker 8 pt, title 24 pt, lead 9.5 pt beside it on 2 lines, rule y 25; number 14 pt,
    footer label 7.5 pt); a lead that repeats the kicker is replaced by the page's own lead.
  * Level tags one column, 1 mm out, short dash + ▽ + value, crowded values move vertically only.
  * Log: "scale <page> <drawing> printed 1:n true 1:m", WARNING "<page> <block> fit | offsheet | textfit | unlisted";
    output/bergama_booklet/page_boxes.csv; Data/booklet_layout.csv carries a plan column (an older table is kept as
    booklet_layout_<old>_<time>.csv and the v37 plan written fresh).
  * PAGE TABLE (round 8 table pass, 9 Nov; PLAN.md §table + Aras's answers): every page re-framed for what the
    producers export now (MainBoard v65, MasterPlan v45, WaterBoard v19, AgriCulture v14): union frames for one-item
    boards (p02 plan 01, p06, p19), p07 map + scale rows merged, p04 1:2,500 / p05 1:2,000 with the ratio in the note
    frames (bar=), p08 street cuts one row (bars only), p13 one 1:500 drawing per season (rigid=: labels as set, no
    band), p14 zoom 1:200, p16 plans 1:3,000, p20 SON format (row notes, 3 legend groups), p21 sections staggered,
    p18 skips ag2_farms*. A frame without note= keeps room for its drawings' attached notes (no "unlisted").
  * Label boxes: a text exported with a "box" (MasterPlan v45 context labels mp_plan_ctx_*) gets a white 70 % box
    with a #5A6670 outline under its placed text (bk_text_boxes).
NEW IN v35 (5 Nov 2026; Aras 12:32 "pages should be able to move drawings when needed", decision 09:45 "Both"):
  * LAYOUT TABLE ~/Downloads/Bergama/Data/booklet_layout.csv: written from the built-in plan on the first run, then
    read on every run. One row per frame: page_order;page;block;x_mm;y_mm;w_mm;h_mm;scale;size;on. Change a page's
    order, a frame's place or size, a drawing's scale (n of 1:n) or switch a frame off (on = 0), save, press the
    Button. Delete the file to get the built-in plan back. A row the plan does not know = WARNING.
  * FLOW (parts/84_flow.py) replaces v34's pack + page factor: each block starts at its table place at its table
    scale, is measured (drawing + levels + scale band + notes), grows if it needs more room, and moves below or beside
    the block it lands on (2 mm grid, 4 mm gap), else to the first free place; none = WARNING "page full". The scale
    never changes. Log "flow <page> <block> moved dx,dy grown dw,dh".
  * A booklet PDF open in a viewer is no longer an ERROR: saved as Bergama_booklet_A3_<HHMMSS>.pdf + WARNING.
NEW IN v33 (round 7 S7, 5 Nov 2026; revision_2026-11-05_round7/PLAN.md §2-§4, BRIEF §3 L1-L6):
  * The page plan (parts/80_plan.py) is FIXED: each frame is the measured SON frame in mm (H4 §5, key maps H4 §3)
    with SON's printed scale (den) or a size factor (f = 1: the exported size). No code picks, rounds, snaps or fits
    a scale or a frame: the scale ladder, _bk_fit, _bk_same, _bk_justify, the margin clamp, extent-weighted cells,
    sc_pick / sc_factor / sc_inset_den and the text shrink loops are deleted. A drawing past its frame = WARNING
    "<page> <drawing> frame" with the overflow per side; the scale is kept (L3).
  * Key maps (G7-3, S1 module) placed 1:1 at their SON frame; their north arrow and heading by their anchors.
  * Title band in SON page2's place (mm); kicker "<letter> <CHAPTER> · <PART>"; footer "<letter> <CHAPTER>  <n>".
  * p09 drops the windows row (SON9 has none, F13), p18 the farms map (not on SON19, F12): logged "skip ...".
  * Log: "frame <page> <key> x,y,w,h", "scale <page> <drawing> 1:<n> (table|script|sheet|board)", "size <page>
    <drawing> x1.00 w x h mm", "keymap <page> module <id>", "check <page> drawings= scale_ok= frames_ok= moved=",
    "pagenum <n>"; every misfit a WARNING, never a stop.
NEW IN v32 (L1, 4 Nov 2026; revision_2026-11-04_round6/LAYOUT_PLAN_booklet_places_all.md §3.2, handover/L1_engine.md;
Aras 19:17-19:30 "scripts just produce the drawings ... booklet ... detects the size needed for each drawing and where
they needs to go and places them", "making it smaller ... is a band-aid", the W1 box and WINTER row images; a feature):
  * ONE BOX PER DRAWING, built here at print size: number disc + title, subtitle, (sections) a label band above the
    drawing with vertical leaders (rows when two would touch), the drawing, its level column (2nd column / joining
    line when values crowd, every value printed), notes + scale under. Each box is measured at every allowed scale;
    the largest scale at which the whole box fits its frame is taken.
  * Pages JUSTIFIED: every frame with content grows into the free page space to the margins / its neighbour's gutter
    (the SON arrangement kept); a frame flush with the right margin sets its drawing right.
  * Collisions: after placing, every text that hits something runs the chain again: free spot round its point, short
    form, OUTSIDE the drawing with a leader line, number + key row. No drawing is scaled down and no text shrunk to
    clear a hit. Multi-line labels move as one. Diagram / board texts no longer set blind (they take the chain too).
  * Paragraphs justified, last line left, the Sources page included (Aras 19:22). Key-map cuts closer than 1.5 mm:
    names pushed apart (no WARNING); a cut "look" given as text no longer breaks the key map (common/keymap.py).
  * Log per page: "layout <page> drawings n, labels n (moved n, short n, leader n, numbered n), drawings made smaller
    0, hits left n (frames grown n)". WARNING only for hits left after all that (texts still printed).
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
VERSION = "v38.1"  # v38.1 12 Nov 2026 (Aras 11 Nov 22:23-22:24 UTC): p13 season frames take SectionFromLine's sfl_season_* cuts (27 Oct look, both banks of S4), WaterBoard's p15_season_* only as a fallback id; v38 11 Nov 2026 (round 9 Part BK): R9_FRAMES table, ADDENDUM §0 label rule + series, M map windows, bk_centre badges / tags, p09 card boxes, B19 p20, underfill / cover; v37 8 Nov 2026 (round 8 S6, engine pass): absolute frames (v35 flow + v34 pack deleted), uniform fit within +-6 % of the printed scale (bar at the true scale, printed ratio = table), attach-by-frame, notes textfit, SON title band + footer, one-column level tags, sheet bounds (offsheet), page_boxes.csv, version-stamped layout table; page table (BK_PAGES) not yet re-done; was "v36"  # v36 8 Nov 2026 (Aras: no backward reads between scripts): a text another script exports into a drawing's group (the masterplan's section-note link sb_sec_note_<cut>_mp, group sb_sec_<cut>) comes after that drawing's own texts (bk_items); v35 5 Nov 2026 (Aras 12:32 "pages should be able to move drawings when needed"): LAYOUT TABLE Data/booklet_layout.csv (written on the first run; edit page order, frames, scales, on/off in Excel) + FLOW: every block at its table place and table scale, grown to its measured size, shifted below / beside the block it lands on, scale never changed (no page factor); a locked PDF (open in a viewer) is saved under a timed name with a WARNING; was "v34"  # v34 5 Nov 2026 (Aras 11:42 "change your approach"): MEASURE, THEN PACK: SON frames give only the order and arrangement, every block is measured at its scale with its labels and the page is laid out from those real sizes (no two blocks can overlap); a page that does not fit gets ONE factor for every drawing on it (true 1:n printed), texts keep their size, key maps size 1; log "pack <pid> k=..."; was "v33"  # v33 round 7 S7 5 Nov 2026: fixed SON frames + SON scales, nothing fitted, misfit = WARNING (see NEW IN v33); v32.6 v32.6 fix 5 Nov (offline run on Aras's items, page images checked): a level value never sits on the line of the value beside it; text-only note columns (p04, p05, p07) keep their script's lines (they were pushed onto each other) and the runs of one line follow each other; p04/p05 note frames as wide as the notes; p18 farms map in its own frame (the reading diagram had 4 mm, x0.03); a legend in a band frame uses the frame's width (p19 ran 28 mm past the foot); script texts with no leader kept inside the page margins; v32.5 fix 4-5 Nov (offline runs on the scripts' outputs, page images checked): a script's texts move only inside their own drawing (no leader lines across other drawings), frames inside the 14 mm margins, wide note frames in columns, legends take more columns before a smaller size, a detail that fits none of its scales takes the next coarser one, the Sources columns inside the margins, p21 rows re-set, texts a script set on top of each other are named per drawing and script; v32.4 fix 4 Nov (p02 ran 10+ min in the 21:49 run): faster leader and collision tests (grid), the log shows the page and text count every 5 s, and a page past 150 s sets its remaining texts at their own spot without the search, so the booklet always finishes (hits named as WARNINGs); the PDF is saved without the duplicate merge (16+ min, now seconds); the Sources page composes again (its row height had slipped into a comment); v32.3 fix 4 Nov (Aras 21:38, no log again): the log file shows the page being composed while the booklet runs, and every page's time at the end; v32.2 speed 4 Nov (Aras 21:14): grid index for the page collision tests (same results, far fewer comparisons); v32.1 fix 4 Nov (kit v4.1 run): section label bands no longer loop for ever when two labels sit close (the booklet never finished); v32 4 Nov 2026 (L1): boxes, justified pages, collisions moved never shrunk; v31 4 Nov 2026 (round 6 S9): page frames (G6-1), 22 pages (G6-2), Sources last (G6-3), groups (G6-9); was v30.3 fix (2 Nov run: drawings small, things on top of each other): texts of diagrams, charts, key maps and site board drawings stay where their script set them, scaled with the drawing (site board: from its "sheet scale 1:N"), never moved or numbered into side lists; one factor per diagram row; right-column drawings share the room left; insets 1:100 or 1:200 as the row allows; p02 share 0.50, p07 notes as a 4th row, p13 share 0.78 + smaller key map; 1:50,000 for the p19 farms map; booklet scale list 1:200 ... 1:25,000 with 1:1,500, 1:7,500, 1:15,000 (Aras 06:20) and 1:25,000; scale_pref read as a range; diagrams up to 6 x (right column 2 x); page plan p07 3 rows, p10 windows 2 x 3, p11 share 0.80, p16 3 x 2 share 0.62, p21 share 0.75, p22 plans side by side at 1:1,000 or 1:1,500; v30.2 fix (round 5 open rows): p04/p05 rows = one drawing per cut (sb_sec_s1 ... s8), one scale per page (common); v30.1 fix (round 5 closing): the Sources page lists the masterplan's numbered places as "n name: sources" (v30 printed the raw dict); v30 2 Nov 2026 (round 5 S10): composer pages from items.json, 23 pages, one page numbering
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


def bk_warn(page, block, what, log=None):
    """v37 (round 8 BRIEF §8): one WARNING line in the form "WARNING <page> <block> <what>" (fit, offsheet, textfit,
    unlisted ...) + an orange message; the run goes on"""
    line = u"WARNING %s %s %s" % (page or u"-", block or u"-", what)
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
        dx, dv = -(ix0 + ix1) / 2.0, -(iy0 + iy1) / 2.0   # v38 (c2): centred on the ink box, not the advance
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
            _, pts, stroke, lw, dash, cap = it[:6]
            la = it[6] if len(it) > 6 else None               # v38 (B19): a see-through line (opacity < 0.975)
            if la is not None and la < 0.975:
                A("q /A{:02d} gs".format(max(1, min(19, int(round(la * 20))))))
                cur.clear()
            col(stroke, True)
            lw_dash(lw, dash, cap)
            path(pts, False)
            A("S")
            if la is not None and la < 0.975:
                A("Q")
                cur.clear()
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
    add.objs = objs                                       # G6-9: _wp_set_obj fills a reserved object later
    font = pdf_fonts(add, ("R", "B"))                     # G2/G3 28 Oct: Arial embedded (common/pdf_fonts.py)
    gs = [add("<< /Type /ExtGState /ca {0} /CA {0} >>".format(_f(i / 20.0)).encode("latin-1")) for i in range(1, 20)]
    gs_res = " ".join("/A{:02d} {} 0 R".format(i + 1, o_) for i, o_ in enumerate(gs))
    pages_id = add(b"")
    xo_res = ""
    if getattr(pg, "grouped", False) or getattr(pg, "grp", None) is not None or any(it[0] == "grp" for it in pg.items):   # G6-9 (round 6): nested groups
        stream, xo = _wp_group_stream(pg, add, font, gs_res, title)
        xo_res = " /XObject << {} >>".format(" ".join("/{} {} 0 R".format(n_, o_) for n_, o_ in xo)) if xo else ""
    elif any(it[0] == "image" for it in pg.items):        # D1 a (30 Oct): raster cutouts between the vector items
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
    names, xo = {}, []
    return _wp_run(pg.items, pg.W, pg.H, add, names, xo), xo


def _wp_run(items, W, H, add, names, xo):
    """the content stream of items in their order: vector runs through page_stream (each in q ... Q), images as
    XObjects (names: file -> name or None, shared by the whole PDF; xo collects [(name, id)]); "grp" markers skipped"""
    class _Run(object):
        pass
    parts, run = [], []

    def flush():
        if run:
            r = _Run()
            r.W, r.H, r.items = W, H, list(run)
            parts.append(b"q\n" + page_stream(r) + b"\nQ")
            del run[:]
    for it in items:
        if it[0] == "grp":
            continue
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
    return b"\n".join(parts)


# ---- G6-9 nested groups (round 6, S2, 4 Nov 2026; Aras 17:50-17:51: "every tree its own group inside one Trees
# group ... apply this to everything") -------------------------------------------------------------------------------
# A page item ("grp", "<kind>/<element id>") opens a group for the items after it; ("grp", None) closes it (made by
# item_export.py ix_grp / ix_tag; page_stream and xform pass over them). When pg.items holds such markers, or the caller
# sets pg.grouped = True (the booklet's drawings, 30_render), write_pdf writes every element as its own Form XObject
# inside one Form XObject of its kind, in draw order. Illustrator opens a Form XObject as a group (UNVERIFIED here:
# never run; Aras checks "groups in Illustrator"), so a booklet drawing (itself one Form XObject via show_pdf_page)
# opens as Drawing > Trees > tree. Each group's name is also written as marked content (/G69 <</Name (...)>> BDC ...
# EMC) for readers that list it. Draw order is never changed: a kind that comes back after another kind starts a
# second group of that kind (counted as repeats in the log). Items under no open group go to kind "other" (one element
# per run) + one WARNING per drawing.
#   wp_grp_of(shape) -> "<kind>/<id>" or None   the group of an items.json shape dict (Ix stamps "grp" on every
#                                               shape at export, item_export.py)
#   wp_groups_log(page) -> "groups <page> kinds=n elements=n untagged=n"   one line per page (after its drawings)
# Two ways to tag, same result: markers in pg.items, or pg.grp = a list parallel to pg.items ("<kind>/<id>" or None
# each; the booklet's form, S9) with pg.grp_root = the drawing id (its name, marked content round the kinds).
# Stats key: pg.page if set, else the PDF title.
WP_GRP_STATS = {}           # page -> dict(kinds=set, elements=n, untagged=n, repeats=n, drawings=n)


def wp_grp_of(shape):
    return (shape.get("grp") or None) if isinstance(shape, dict) else None


def wp_groups_log(page):
    st = WP_GRP_STATS.get(page)
    if not st:
        return u"groups %s kinds=0 elements=0 untagged=0" % page
    return u"groups %s kinds=%d elements=%d untagged=%d%s" % (
        page, len(st["kinds"]), st["elements"], st["untagged"],
        u" repeats=%d" % st["repeats"] if st["repeats"] else u"")


def _wp_split_grp(g, n):
    g = u"%s" % g
    if "/" in g:
        k, e = g.split("/", 1)
        return (k.strip() or "other"), (e.strip() or u"%s %d" % (k, n))
    return g, u"%s %d" % (g, n)


def _wp_set_obj(add, oid, b):
    add.objs[oid - 1] = b


def _wp_group_stream(pg, add, font, gs_res, title=None):
    """(page content stream, [(name, id)] for the page's /XObject): kinds and elements as nested Form XObjects"""
    seq = pg.items
    pgrp = getattr(pg, "grp", None)
    if pgrp is not None:                                  # S9 form: pg.grp parallel to pg.items (str or None each)
        seq = []
        for i_, it in enumerate(pg.items):
            seq.append(("grp", pgrp[i_] if i_ < len(pgrp) else None))
            seq.append(it)
    runs, cur, buf, untagged = [], None, [], 0
    for it in seq:
        if it[0] == "grp":
            g = it[1] if len(it) > 1 and it[1] else None
            if g != cur:
                if buf:
                    runs.append((cur, buf))
                    buf = []
                cur = g
            continue
        buf.append(it)
        if cur is None:
            untagged += 1
    if buf:
        runs.append((cur, buf))
    kinds, n_other = [], 0                                # [[kind, [(element name, items)]]] consecutive by kind
    for g, its in runs:
        if g is None:
            n_other += 1
            k, e = "other", u"other %d" % n_other
        else:
            k, e = _wp_split_grp(g, len(runs))
        if kinds and kinds[-1][0] == k:
            kinds[-1][1].append((e, its))
        else:
            kinds.append([k, [(e, its)]])
    bbox = "[0 0 {} {}]".format(_f(pg.W / PT), _f(pg.H / PT))
    base_id = add(b"")
    names, img = {}, []

    def form(stream, res_id):
        data = zlib.compress(stream, 6)
        return add(("<< /Type /XObject /Subtype /Form /BBox {} /Resources {} 0 R /Length {} /Filter /FlateDecode >>"
                    "\nstream\n".format(bbox, res_id, len(data))).encode("latin-1") + data + b"\nendstream")

    def mc(name, xname):
        return b"/G69 << /Name " + pdf_str(name) + b" >> BDC /" + xname.encode("latin-1") + b" Do EMC"
    el_ids = []                                           # per kind: [(E name, id, element name)]
    n_el = 0
    for k, els in kinds:
        row = []
        for e, its in els:
            n_el += 1
            row.append(("E%d" % n_el, form(_wp_run(its, pg.W, pg.H, add, names, img), base_id), e))
        el_ids.append(row)
    base = "/Font << /F1 {} 0 R /F2 {} 0 R >> /ExtGState << {} >>".format(font[0], font[1], gs_res)
    img_res = " ".join("/{} {} 0 R".format(n_, o_) for n_, o_ in img)
    objs_base = "<< {}{} >>".format(base, " /XObject << {} >>".format(img_res) if img_res else "")
    _wp_set_obj(add, base_id, objs_base.encode("latin-1"))
    page_xo, parts, seen = list(img), [], {}
    for i, (k, els) in enumerate(kinds):
        row = el_ids[i]
        res = add("<< {} /XObject << {} {} >> >>".format(base, img_res, " ".join(
            "/{} {} 0 R".format(n_, o_) for n_, o_, _e in row)).encode("latin-1"))
        kid = form(b"\n".join(mc(e, n_) for n_, _o, e in row), res)
        kn = "K%d" % (i + 1)
        page_xo.append((kn, kid))
        seen[k] = seen.get(k, 0) + 1
        parts.append(mc(k, kn))
    key = getattr(pg, "page", None) or (u"%s" % title if title else "page")
    st = WP_GRP_STATS.setdefault(key, dict(kinds=set(), elements=0, untagged=0, repeats=0, drawings=0))
    st["kinds"].update(seen)
    st["elements"] += n_el
    st["untagged"] += untagged
    st["repeats"] += sum(v - 1 for v in seen.values())
    st["drawings"] += 1
    if untagged:
        msg = u"%s: %d item(s) with no group went to kind \"other\" (G6-9: tag them with ix_grp at the point of " \
              u"drawing)" % (title or key, untagged)
        if "wn_warn" in globals():
            wn_warn(key, "groups", msg)                                                         # noqa: F821
        else:
            WP_IMG_LOG.append(msg)
    root = getattr(pg, "grp_root", None)
    if root:                                              # the drawing's own name round its kinds (no extra form:
        parts = [b"/G69 << /Name " + pdf_str(u"%s" % root) + b" >> BDC"] + parts + [b"EMC"]   # show_pdf_page's
    return b"\n".join(parts), page_xo                    # Form XObject is the drawing group)
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
    win = D.get("_window")                       # v38 (d4): a map placed through a window: texts outside it left out
    for its in BK_IX.get(D.get("_folder"), {}).get("pages", {}).values():
        for it in its:
            a_ = it.get("anchor")
            if it.get("kind") == "text" and isinstance(a_, dict) and a_.get("drawing") == D["id"]:
                if win is not None and not _bk_in_win(it, win):
                    continue
                out.append(it)
    return sorted(out, key=lambda t: t.get("priority", 5))


def _bk_in_win(it, win):
    """v38: True when a text's point (anchor pt / point, or a badge's "at") lies inside win = (x0, y0, x1, y1); a text
    with no point counts as inside"""
    p_ = it.get("at") or _pl_apt(it)
    if p_ is None:
        return True
    return win[0] - 1e-6 <= float(p_[0]) <= win[2] + 1e-6 and win[1] - 1e-6 <= float(p_[1]) <= win[3] + 1e-6


def ix_text(t, folder=None):
    if t is None:
        return u""
    it = ix_get(t, folder) if not isinstance(t, dict) else t
    if it is not None and it.get("kind") == "text":
        return it.get("string", u"")
    return u"%s" % t
# ---- 20_scale (composer core, round 5 S1; round 7 v33: no scale list, no picking): drawing -> page mm ---------------
#   sc_size(D, den_or_f) -> (w_mm, h_mm)       the printed size of a drawing's extent
#   v33 (round 7, BRIEF L1/L3): the scale ladder (BK_SCALES, BK_MM_MAX) and every picker (sc_pick, sc_pick_common,
#   sc_factor, sc_inset_den, _sc_allowed) are DELETED: a drawing's scale is read from the page table (82_compose
#   _bk_den), never chosen here.
#   BkT(D, s, x, y)                              the drawing's transform onto the page: s = den ("m") or f ("mm");
#                                               (x, y) = the page mm (y DOWN) of the extent's top-left corner;
#                                               .k (page mm per drawing unit), .pt(x, y), .rect, .den (None for "mm")
def _sc_ext(D):
    e = D["extent"]
    return float(e[2]) - float(e[0]), float(e[3]) - float(e[1])


def sc_size(D, s):
    ew, eh = _sc_ext(D)
    k = (1000.0 / float(s)) if D.get("units", "m") == "m" else float(s)
    return ew * k, eh * k


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
    bats = [b_["at"] for b_ in bk_s1_badges(D)]       # v38 (c1): S1 badges draw their own disc (bk_badges)
    for L in sorted(D.get("layers") or [], key=lambda L: L.get("z", 0)):
        for s in L.get("shapes") or []:
            n0 = len(out)
            t = s.get("t") or s.get("type")         # Ix writes "t", the key-map module (S2) "type"
            if t == "poly" and s.get("badge_disc") and bats and _bk_disc_has(s, bats):
                BK_DISC_SKIP[0] += 1                  # v38: a badge's disc poly: the booklet draws it with its glyph
                continue
            if t == "poly":
                rings = [[P(p) for p in r] for r in s.get("rings") or [] if len(r) >= 3]
                if rings and (s.get("fill") or s.get("stroke")):
                    out.append(("poly", rings, s.get("fill"), s.get("stroke"), (s.get("width_pt") or 0.0) * mm,
                                [v * mm for v in s["dash_pt"]] if s.get("dash_pt") else None, None, s.get("opacity")))
            elif t == "line":
                pts = [P(p) for p in s.get("pts") or []]
                if len(pts) >= 2 and s.get("stroke"):
                    out.append(("line", pts, s["stroke"], (s.get("width_pt") or 0.25) * mm,
                                [v * mm for v in s["dash_pt"]] if s.get("dash_pt") else None, s.get("cap", 1),
                                s.get("opacity")))            # v38: line opacity (B19 roads)
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


def bk_line(P, pts, stroke, width_pt=0.5, dash=None, alpha=None):
    """a polyline on the page (page mm, y down); v38: alpha = stroke opacity (B19 legend swatches)"""
    import fitz as _fz
    sh = P.page.new_shape()
    sh.draw_polyline([_fz.Point(x * BK_K, y * BK_K) for x, y in pts])
    sh.finish(color=hex_rgb(stroke), width=width_pt, closePath=False,
              dashes=("[%s] 0" % " ".join("%g" % d for d in dash)) if dash else None,
              stroke_opacity=float(alpha) if alpha is not None and float(alpha) < 0.995 else 1)
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


# ---- v32.4 (p02 ran 10+ min in Aras's 4 Nov 21:49 run): PyMuPDF picks a fresh resource name for each drawing, photo
# and font it adds by listing EVERY xobject, image and font of the page, recursing into each drawing already placed
# (each one holds thousands of nested group xobjects, G6-9), with a list as its "seen" set: the time grows with the
# square of the drawing's groups. A new name only has to differ from the names in the page's OWN resource
# dictionaries, so the booklet's document lists those (shallow); the picture is the same. full=True (font
# subsetting at the end) still gets the original deep lists.
def _bk_res_shallow(doc, pno, key):
    try:
        x_ = doc[pno].xref
        t_, v_ = doc.xref_get_key(x_, "Resources/" + key)
        if t_ == "xref":
            v_ = doc.xref_object(int(v_.split()[0]), compressed=True)
        elif t_ != "dict":
            return []
        return [(int(m_.group(2)), m_.group(1)) for m_ in re.finditer(r"/([^\s/<>\[\]()]+)\s*(\d+)\s+\d+\s+R", v_)]
    except Exception:
        return []


def bk_shallow_res(doc):
    f0, i0, x0 = doc.get_page_fonts, doc.get_page_images, doc.get_page_xobjects

    def fonts(pno, full=False):
        if full:
            return f0(pno, full=True)
        return [(xr, u"", u"", u"", nm, u"") for xr, nm in _bk_res_shallow(doc, pno, "Font")]

    def images(pno, full=False):
        if full:
            return i0(pno, full=True)
        return []                                   # image names are in the XObject dictionary: listed below

    def xobjects(pno):
        return [(xr, nm, 0, None) for xr, nm in _bk_res_shallow(doc, pno, "XObject")]
    doc.get_page_fonts, doc.get_page_images, doc.get_page_xobjects = fonts, images, xobjects
    return doc
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
#         (lines, pt, lead_mm, height_mm)      v33: set at pt (no stepping down unless min_pt is given); past h =
#                                              WARNING "overrun" (L2: text keeps its point size)
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
    lo = float(min_pt or pt)          # v33 (L2): text keeps its point size unless a caller names a floor; overrun = WARNING
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
        xr = {"BKR": P.page.insert_font(fontname="BKR", fontfile=r),
              "BKB": P.page.insert_font(fontname="BKB", fontfile=b)}
        _ins0 = P.page.insert_font

        def _ins(fontname="helv", fontfile=None, **kw):       # v32.4: PyMuPDF looked the font up again for EVERY
            k = fontname[1:] if fontname.startswith("/") else fontname   # text by scanning all the page's
            if k not in xr:                                   # resources, inside each embedded drawing too (p02:
                xr[k] = _ins0(fontname=fontname, fontfile=fontfile, **kw)   # 10+ min); the xref is the same each
            return xr[k]                                      # time, so it is kept after the first look-up
        P.page.insert_font = _ins
        P._fonts = True
    bk_text_boxes(P)                                          # v37: label boxes (item key "box") under their texts

    def draw(it):
        s, pt, bold = it["text"], it["pt"], it["bold"]
        w = fm_width(s, pt, bold)
        al = str(it.get("align") or "L").upper()
        x, y = it["x"], it["y"]
        if al in ("MC", "CM"):
            ix0, iy0, ix1, iy1 = fm_ink_box(s, pt, bold)
            dx, y = -(ix0 + ix1) / 2.0, y + (iy0 + iy1) / 2.0     # v38 (c2): the ink box's middle on (x, y)
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


BK_TEXT_BOX = {}            # v37: text id -> its exported "box" (MasterPlan v45 context labels mp_plan_ctx_*), bk_items
BK_TEXT_BOX_PAD = 0.6       # mm round the text
BK_TEXT_BOX_LW = 0.3        # pt outline


def bk_text_boxes(P):
    """v37 (round 8, MasterPlan v45 P2 Q8): a text exported with a "box" (dict fill, alpha, stroke) gets a rectangle
    under its PLACED text (after the label pass): fill at alpha (default white at 70 %), a BK_TEXT_BOX_LW outline
    (default #5A6670), BK_TEXT_BOX_PAD mm round it; the lines of one label (same id and group) share one box. -> n"""
    import fitz as _fz
    got = {}
    for it in P.tp.items:
        b_ = BK_TEXT_BOX.get(it.get("name"))
        if not isinstance(b_, dict) or not it.get("emit", True) or it.get("role") == "number":
            continue
        k_ = (it.get("name"), it.get("group"))
        r = it["box"]
        o = got.get(k_)
        got[k_] = (b_, tuple(r) if o is None else (min(o[1][0], r[0]), min(o[1][1], r[1]), max(o[1][2], r[2]),
                                                   max(o[1][3], r[3])))
    pd = BK_TEXT_BOX_PAD
    for b_, r in got.values():
        try:
            a_ = float(b_.get("alpha", 0.7))
        except (TypeError, ValueError):
            a_ = 0.7
        sh = P.page.new_shape()
        sh.draw_rect(_fz.Rect((r[0] - pd) * BK_K, (r[1] - pd) * BK_K, (r[2] + pd) * BK_K, (r[3] + pd) * BK_K))
        sh.finish(color=hex_rgb(u"%s" % (b_.get("stroke") or "5A6670")),
                  fill=hex_rgb(u"%s" % (b_.get("fill") or "FFFFFF")), fill_opacity=max(0.0, min(1.0, a_)),
                  width=BK_TEXT_BOX_LW)
        sh.commit()
    return len(got)
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
#                                                                       drawing, values "+43.71"; v32: crowded values in a
#                                                                       2nd column or pushed down with a joining line
#   pl_levels_w(lc, k, e_top) -> mm                                     v32: the level column's measured width
#   pl_chain(P, fx, side=None, first=True) -> item                      v32: the one chain for every movable text
#   pl_scalebar(P, placed, x=None, y=None, max_mm=30.0) -> box           beside its drawing (default under its left end)
#   (pl_inset deleted in v33: an inset takes its frame's den from the page table)
#   pl_mm_drawing(P, D, T) -> placed                                    v33: a scale-free drawing (key map) at T, never
#                                                                       fitted, + its texts at their own size
#   pl_photo(P, ph, x, y, w, h) -> box                                  a photo kept rectangular, never stretched
# Every placed thing is a TextPage text, block or keep, so 70_check sees it.
PL_LEVEL = dict(gap=1.0, dash=(3.0,), tri_w=2.2, tri_h=1.4, lw=0.5, label_gap=0.8, clear=0.8,
                ink="4A3F35")          # v37 (D4): 1.0 mm out from the drawing's end, ONE short 3 mm dash, ▽, value (mm, pt)
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


def _pl_try(P, t, anchor, codes, pt, bold, allow, win, d=0.8, group=None):
    tp = P.tp
    for code in codes:
        x, y, al = tp._at(code, t, anchor, pt, bold, d)
        b = tp._box(t, x, y, pt, bold, al, 0.0)
        if _pl_inside(b, win) and tp._free(b, allow, group):
            return x, y, al
    for x, y, al in tp._ring_spots(t, anchor, pt, bold, d, TP_RINGS):
        b = tp._box(t, x, y, pt, bold, al, 0.0)
        if _pl_inside(b, win) and tp._free(b, allow, group):
            return x, y, al
    return None


PL_FIX = ("moved", "short", "leader", "numbered", "forced")
PL_LEAD = dict(gap=1.5, col=14.0, cols=4, lw=0.3, ink="4A3F35", row_gap=0.8)    # leader lines (mm, pt)


def pl_stat(P):
    """v32: the page's label counts (log "layout <page> ... labels n (moved n, short n, leader n, numbered n)")"""
    if not hasattr(P, "fx_stat"):
        P.fx_stat = dict((k, 0) for k in ("labels",) + PL_FIX)
        P.fx_leaders = []
    return P.fx_stat


def _pl_seg_clear(P, p, q):
    """True when the leader p-q crosses no text already on the page (v32.4: only the texts in the grid cells of the
    leader's box are tested; a text outside that box cannot touch it, so the answer is the same)"""
    tp = P.tp
    _s, gi, _gk = _bk_index(tp)
    bb = (min(p[0], q[0]), min(p[1], q[1]), max(p[0], q[0]), max(p[1], q[1]))
    I = tp.items
    return not any(tp_seg_box(p, q, I[n]["box"]) for n in _bk_near(gi, bb, 0.0))


def _pl_leader(P, fx, t):
    """v32: a spot for text t OUTSIDE its drawing (fx["rect"]) with a leader line from its anchor: beside the drawing
    (the anchor's nearer side first, then the other, columns further out), level with the anchor or the nearest free
    row above / below. Same size, never smaller (Aras 4 Nov 19:25). -> (x, y, align, (p, q)) or None"""
    r = fx.get("rect")
    if not r:
        return None
    tp, L = P.tp, PL_LEAD
    ax, ay = fx["anchor"]
    pt, bold = fx["pt"], fx["bold"]
    a_, d_ = fm_asc_desc(pt, bold)
    step = (a_ - d_) + L["row_gap"]
    sides = ("R", "L") if ax >= (r[0] + r[2]) / 2.0 else ("L", "R")
    for j in range(L["cols"]):
        for sd in sides:
            x = (r[2] + L["gap"] + j * L["col"]) if sd == "R" else (r[0] - L["gap"] - j * L["col"])
            al = "L" if sd == "R" else "R"
            for k_ in range(0, 41):
                dy = ((k_ + 1) // 2) * step * (1.0 if k_ % 2 else -1.0)
                yc = ay + dy
                base = yc + (a_ + d_) / 2.0
                b = tp._box(t, x, base, pt, bold, al, 0.0)
                q = (x - 0.4, yc) if sd == "R" else (x + 0.4, yc)
                if tp._free(b, fx["allow"], fx.get("group")) and _pl_seg_clear(P, (ax, ay), q):
                    return x, base, al, ((ax, ay), q)
    return None


def pl_draw_leaders(P):
    """draws the leader lines of the page's texts that kept a leader (after the fix pass, so moved ones are gone)"""
    n = 0
    for fx in P.fx_leaders:
        if fx.get("leader"):
            p, q = fx["leader"][0]
            bk_line(P, [p, q], PL_LEAD["ink"], PL_LEAD["lw"])
            n += 1
    return n


def pl_unleader(P, fx):
    """takes a text's leader (and its keep) off again before the text is placed anew"""
    ld = fx.pop("leader", None)
    if ld and ld[1] in P.tp.keeps:
        P.tp.keeps.remove(ld[1])


def pl_chain(P, fx, side=None, first=True):
    """v32 (L1, LAYOUT_PLAN §3.2-3; Aras 4 Nov 19:25 "making it smaller ... is a band-aid"): ONE chain for every
    movable text, at its own size: (1) its exported spot, (2) free spots on rings round its anchor inside its window
    (moved), (3) its short forms the same way (short), (4) OUTSIDE its drawing with a leader line, full text first
    (leader), (5) a number on the anchor + a row in the side list (numbered; side None or side_list_ok False skips
    it), (6) set at its first spot (forced: the final check names it). Never dropped, never shrunk.
    fx = dict(anchor, texts, codes, pt, lo, bold, colour, role, name, allow, win, rect, d, side_ok, owner); the text
    keeps fx in item["extra"]["fx"], so bk_fix (82_compose) can take it off and run the chain again (first=False)."""
    st = pl_stat(P)
    tp = P.tp
    anchor, texts, codes = fx["anchor"], fx["texts"], fx["codes"]
    pt0, bold, win, d = fx["pt"], fx["bold"], fx.get("win"), fx.get("d", 0.8)
    late = bk_progress(fx.get("name"))                    # v32.4: progress line; past the page budget: no search

    def put(t, x, y, al, kind, allow=None, **kw):
        tp.put(t, x, y, pt0, bold, al, 0.0, fx.get("name"), fx.get("role", "label"), fx.get("colour"),
               allow or fx["allow"], fx.get("group"), fx=fx, **kw)
        if kind:
            st[kind] += 1
        return tp.items[-1]
    if first:
        st["labels"] += 1
    for i, t in enumerate(texts):
        if first and i == 0 and codes:                    # its own exported spot first
            x, y, al = tp._at(codes[0], t, anchor, pt0, bold, d)
            b = tp._box(t, x, y, pt0, bold, al, 0.0)
            if fx.get("no_leader"):                       # v32.5: a script's spot past the page margins moves in
                inn = tp.inner                            # just far enough (p04/p05 level words left of a section)
                dx = max(0.0, inn[0] - b[0]) - max(0.0, b[2] - inn[2])
                dy = max(0.0, inn[1] - b[1]) - max(0.0, b[3] - inn[3])
                if dx or dy:
                    x, y = x + dx, y + dy
                    b = tp._box(t, x, y, pt0, bold, al, 0.0)
            if (_pl_inside(b, win) or fx.get("no_leader")) and tp._free(b, fx["allow"], fx.get("group")):
                return put(t, x, y, al, None)                 # (a script's own spot may lie outside its drawing)
        if late:
            break
        got = _pl_try(P, t, anchor, codes, pt0, bold, fx["allow"], win, d, fx.get("group"))
        if got:
            return put(t, got[0], got[1], got[2], "moved" if i == 0 else "short")
    for t in ([] if late or fx.get("no_leader") else texts):
        got = _pl_leader(P, fx, t)
        if got:
            nm = u"leader %s %d" % (fx.get("name"), id(fx))
            K = tp.keep([got[3][0], got[3][1]], "leader", nm, line=True)
            fx["leader"] = (got[3], K)
            if fx not in P.fx_leaders:
                P.fx_leaders.append(fx)
            return put(t, got[0], got[1], got[2], "leader", allow=tuple(fx["allow"]) + (nm, "leader"))
    if side is not None and fx.get("side_ok", True):
        tp.put(u"0", anchor[0], anchor[1], pt0, True, "MC", 0.0, fx.get("name"), "number", fx.get("colour"),
               tuple(fx["allow"]) + ("marker",))
        num = tp.items[-1]
        side.add(anchor, texts[0], num)
        if side not in tp.sides:
            tp.sides.append(side)
        st["numbered"] += 1
        return num
    x, y, al = tp._at(codes[0] if codes else "E", texts[0], anchor, pt0, bold, d)
    if late:
        BK_PG["late"] += 1
    return put(texts[0], x, y, al, "forced", forced=True)


# ---- v32.4 (Aras 4 Nov 21:50, p02 ran 10+ min): progress in the log file during a page, and a time budget per page.
# Past BK_PAGE_BUDGET s a page's remaining texts skip the ring / leader search and are set at their own first spot
# (never dropped, never smaller; the final check names every hit left as a WARNING), so the booklet always finishes.
BK_PAGE_BUDGET = 150.0
BK_PG = dict(t0=0.0, pid=None, n=0, last=0.0, late=0, head=u"", tail=u"")


def bk_page_start(pid, head=u"", tail=u""):
    BK_PG.update(t0=time.time(), pid=pid, n=0, last=time.time(), late=0, head=head, tail=tail)


def bk_late():
    return bool(BK_PG["t0"]) and time.time() - BK_PG["t0"] > BK_PAGE_BUDGET


def bk_progress(name=None):
    """counts the page's texts; every 5 s writes the progress line to the log file; True once past the budget"""
    BK_PG["n"] += 1
    now = time.time()
    if now - BK_PG["last"] >= 5.0 and "write_log" in globals():
        BK_PG["last"] = now
        try:
            write_log(u"%s\n  page %s: %.0f s, text %d (%s)%s\n%s\n" % (
                BK_PG["head"], BK_PG["pid"], now - BK_PG["t0"], BK_PG["n"], name,
                u", past the %.0f s budget: texts set at their own spot" % BK_PAGE_BUDGET if bk_late() else u"",
                BK_PG["tail"]))
        except Exception:
            pass
    return bk_late()


# ---- the label band of a section (v32, Aras 4 Nov 19:26 W1 box: labels above the section, vertical leaders) -------
def pl_band_rows(texts, xs, wmax, pt, bold=False):
    """texts at their x (mm from the drawing's left edge) set in rows ABOVE the drawing: each in the lowest row where
    it touches no neighbour and no lower-row label covers its leader; left-aligned at its x (right-aligned at its x
    when it would run past wmax). -> ([(i, x0, row, align)], n_rows)"""
    rows, out = [], []
    # v32.1 fix (kit v4.1 run: the booklet never finished): right to left, so a label's leader passes the labels set
    # before it; a label whose leader is covered by a lower label in every row used to loop for ever: on a NEW row it
    # is now set anyway (its leader crosses that label; the page check reports it)
    for i in sorted(range(len(texts)), key=lambda j: -xs[j]):
        w = fm_width(texts[i], pt, bold)
        x = xs[i]
        al = "L" if x + w <= wmax + 0.5 else "R"
        iv = (x, x + w) if al == "L" else (x - w, x)
        r = 0
        while True:
            fresh = r == len(rows)
            if fresh:
                rows.append([])
            ok = all(not (iv[0] < b_ + 1.2 and a_ < iv[1] + 1.2) for a_, b_ in rows[r])
            ok = ok and all(not (a_ - 0.4 <= x <= b_ + 0.4) for rr in rows[:r] for a_, b_ in rr)
            if ok or fresh:
                rows[r].append(iv)
                out.append((i, x, r, al))
                break
            r += 1
    return out, len(rows)


def pl_band_h(n_rows, pt):
    a_, d_ = fm_asc_desc(pt, False)
    return (n_rows * ((a_ - d_) + PL_LEAD["row_gap"]) + PL_LEAD["gap"]) if n_rows else 0.0


def pl_band_items(D):
    """the anchored labels of a section that go into its band"""
    return [it for it in ix_texts(D) if it.get("role", "label") == "label" and _pl_apt(it) is not None and
            (it.get("string") or u"")]


def pl_band_need(D, k):
    """the band height (mm) a section's labels need at k page mm per drawing unit"""
    its = pl_band_items(D)
    if not its:
        return 0.0
    pt = grid_role("label")[0]
    e0 = float(D["extent"][0])
    ew = (float(D["extent"][2]) - e0) * k
    _o, n = pl_band_rows([it["string"] for it in its], [(_pl_apt(it)[0] - e0) * k for it in its], ew, pt)
    return pl_band_h(n, pt)


def pl_band(P, placed):
    """sets a section's labels in the band above it (its top at placed rect top - band height), each with a vertical
    leader down to its point; band texts are fixed (no chain needed: the rows keep them apart). -> n"""
    D, T, r = placed["D"], placed["T"], placed["rect"]
    its = pl_band_items(D)
    if not its:
        return 0
    st = pl_stat(P)
    pt = grid_role("label")[0]
    a_, d_ = fm_asc_desc(pt, False)
    lh = (a_ - d_) + PL_LEAD["row_gap"]
    anchors = [T.pt(_pl_apt(it)[0], _pl_apt(it)[1]) for it in its]
    rows, _n = pl_band_rows([it["string"] for it in its], [a[0] - r[0] for a in anchors], r[2] - r[0], pt)
    for i, x, row, al in rows:
        it, (ax, ay) = its[i], anchors[i]
        base = r[1] - PL_LEAD["gap"] - row * lh + d_     # row 0 just above the drawing
        P.tp.put(it["string"], r[0] + x + (0.3 if al == "L" else -0.3), base, pt, bool(it.get("bold")), al, 0.0,
                 it.get("id"), "label", it.get("colour"), (placed["id"], "leader"))
        bk_line(P, [(ax, ay), (ax, base - a_ * 0.0 + 0.4)], PL_LEAD["ink"], PL_LEAD["lw"])
        st["labels"] += 1
        st["leader"] += 1
    return len(rows)


def pl_label(P, it, placed, side=None, window=None):
    """an in-drawing label (true-scale drawing): the chain, kept inside its drawing's window"""
    a_ = _pl_apt(it)
    if a_ is None:
        return None
    texts = [t for t in [it.get("string", u"")] + list(it.get("short_forms") or []) if t]
    if not texts:
        return None
    fx = dict(anchor=placed["T"].pt(a_[0], a_[1]), texts=texts, codes=_pl_codes(it.get("positions")),
              pt=float(it.get("size_pt") or grid_role(it.get("role", "label"))[0]),
              lo=max(float(it.get("min_pt") or GRID_MIN_PT), GRID_MIN_PT), bold=bool(it.get("bold")),
              colour=it.get("colour"), role=it.get("role", "label"), name=it.get("id"), allow=(placed["id"],),
              win=window or placed["rect"], rect=placed["rect"], d=0.8, side_ok=it.get("side_list_ok", True),
              owner=placed["id"])
    return pl_chain(P, fx, side)


def pl_rigid(P, placed, s, roles=None, fixed=False):
    """v30.3 / v32: a scale-free drawing (diagram, chart, key map, axo) or a board drawing: each text is tried FIRST at
    the spot its script set, scaled with the drawing (size x s, offsets x s); v32 (L1, Aras 4 Nov 19:17 "detect the
    collisions and fix it"): a spot that hits anything goes through the same chain as labels (pl_chain: rings, short
    forms, number, smaller), anywhere on the page, never on another drawing. Floor GRID_MIN_PT (D1). v38: badges and
    tags first (bk_badges, bk_tags: centred, never moved); fixed=True (p09 card texts, "=al" fixed by CityLink): every
    text at its own spot, never moved by the chain"""
    T = placed["T"]
    n = 0
    bk_badges(P, placed, s)
    bk_tags(P, placed)
    done_ = placed.get("_done") or set()
    import re as _re
    stems = {}                                          # v32: lines of one multi-line label (<id>_lbl_<g>_<line>, L5)
    for it in ix_texts(placed["D"]):
        m_ = _re.match(r"^(.*_lbl_\d+)_\d+$", u"%s" % it.get("id", u""))
        if m_ and _pl_apt(it) is not None and it.get("string"):
            stems.setdefault(m_.group(1), []).append(it)
    done = set()
    for st_, its in stems.items():
        if len(its) > 1:
            n += _pl_rigid_group(P, placed, s, its)
            done.update(id(i_) for i_ in its)
    adj = _pl_runs(placed, s)
    # v32.6: a text-only note crop (sb_sec_note_*, sb_mv_note_*) keeps its script's lines as set (their leading is
    # tighter than the booklet's test pad, so each line was pushed off its spot): its texts do not push each other;
    # they still keep clear of everything else, and any pair truly on top of each other is named ("own" WARNING)
    for it in sorted(ix_texts(placed["D"]), key=lambda t: t.get("priority", 5)):
        if roles and it.get("role") not in roles:
            continue
        if id(it) in done or id(it) in done_:
            continue
        a_ = _pl_apt(it)
        t = it.get("string", u"")
        if a_ is None or not t:
            continue
        pt0 = float(it.get("size_pt") or grid_role(it.get("role", "label"))[0])
        pt = max(GRID_MIN_PT, pt0 * s)
        c = (_pl_codes(it.get("positions")) or ["E"])[0]
        if not isinstance(c, str):
            c = (c[0] * s, c[1] * s, c[2])
        if fixed or it.get("role") == "badge":        # v38: a card's fixed text (and any badge left) at its own spot
            x, y, al = P.tp._at(c, t, T.pt(a_[0], a_[1]), pt, bool(it.get("bold", it.get("role") == "badge")), 0.0)
            P.tp.put(t, x, y, pt, bool(it.get("bold", it.get("role") == "badge")), al, 0.0, it.get("id"),
                     it.get("role", "label"), it.get("colour"), (placed["id"], "marker"))
            n += 1
            continue
        texts = [x_ for x_ in [t] + list(it.get("short_forms") or []) if x_]
        fx = dict(anchor=adj.get(id(it)) or T.pt(a_[0], a_[1]), texts=texts, codes=[c], pt=pt,
                  lo=max(float(it.get("min_pt") or GRID_MIN_PT), GRID_MIN_PT), bold=bool(it.get("bold")),
                  colour=it.get("colour"), role=it.get("role", "label"), name=it.get("id"), allow=(placed["id"],),
                  win=_pl_dwin(placed), rect=placed["rect"], d=0.8 * s, side_ok=False,
                  owner=placed["id"], no_leader=True, dgrp=_pl_dgrp(placed),
                  group=(u"note:%s" % placed["id"]) if u"_note" in u"%s" % placed["id"] else adj.get(("g", id(it))))
        pl_chain(P, fx, getattr(P, "fx_side", None))
        n += 1
    return n


def _pl_runs(placed, s):
    """v32.5: the runs of one line (a bold keyword, then the plain rest; texts on one baseline set "=L" one after the
    other) are re-spaced with the booklet's own font widths: a run that would start inside the run before it moves
    right to follow it (the scripts measured the runs a little narrower: "Street colour" / ": the share ...", p04,
    p05, p07 notes). Same size, same line. -> {id(item): page anchor}"""
    T = placed["T"]
    rows = {}
    for it in ix_texts(placed["D"]):
        a_ = _pl_apt(it)
        pos = it.get("positions") or []
        if a_ is None or not it.get("string") or not pos or pos[0] != "=L" or abs(float(it.get("angle") or 0)) > 0.01:
            continue
        rows.setdefault(round(float(a_[1]), 2), []).append(it)
    adj = {}
    for rk, its in rows.items():
        if len(its) < 2:
            continue
        end = None
        for it in sorted(its, key=lambda i_: float(_pl_apt(i_)[0])):
            a_ = _pl_apt(it)
            pt = max(GRID_MIN_PT, float(it.get("size_pt") or grid_role(it.get("role", "label"))[0]) * s)
            x, y = T.pt(a_[0], a_[1])
            st_ = u"%s" % it["string"]
            gap = 0.15 if st_[:1] in u",.;:)·%" else fm_width(u" ", pt, bool(it.get("bold")))
            # v32.6: a run that follows the one before within 4 mm is set right after it (one space; the scripts'
            # widths left gaps or overlaps); runs of one line are one group, so they never push each other off
            if end is not None and x < end + max(gap, 4.0):
                x = end + gap
                adj[id(it)] = (x, y)
            if end is None or id(it) in adj or x < end + 4.0:
                adj[("g", id(it))] = u"run:%s:%s" % (placed["id"], rk)
            end = x + fm_width(u"%s" % it["string"], pt, bool(it.get("bold")))
    return adj


def _pl_dgrp(placed):
    """v32.4: the drawing a text belongs to (the log's per-drawing count of texts its script set on top of each
    other)"""
    return u"drw:%s" % placed["id"]


def _pl_dwin(placed, pad=1.5):
    """v32.4: a text its script set inside a drawing moves only WITHIN that drawing (its box + 1.5 mm): rings round
    its point, then its short forms; no leader line out of the drawing (they crossed other drawings, p07/p18); if
    nothing is free it stays at its own spot and the final check names the hit. Same size, never dropped."""
    r = placed["rect"]
    return (r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad)


def _pl_rigid_group(P, placed, s, its):
    """v32: the lines of one multi-line label move TOGETHER: their exported spots, else one shared offset on rings
    round them (every line free), else outside the drawing in a column beside it; never split, never shrunk"""
    T, tp = placed["T"], P.tp
    allow = (placed["id"],)
    spots = []
    for it in its:
        a_ = _pl_apt(it)
        pt = max(GRID_MIN_PT, float(it.get("size_pt") or grid_role(it.get("role", "label"))[0]) * s)
        c = (_pl_codes(it.get("positions")) or ["E"])[0]
        if not isinstance(c, str):
            c = (c[0] * s, c[1] * s, c[2])
        x, y, al = tp._at(c, it["string"], T.pt(a_[0], a_[1]), pt, bool(it.get("bold")), 0.8 * s)
        spots.append((it, x, y, al, pt))

    def boxes(dx, dy):
        return [tp._box(it["string"], x + dx, y + dy, pt, bool(it.get("bold")), al, 0.0) for it, x, y, al, pt in spots]

    win, dg = _pl_dwin(placed), None

    def ok(bs, own=False):
        g_ = []
        for b in bs:
            if (not own and not _pl_inside(b, win)) or not tp._free(b, allow, dg):
                return False
            if any(tp_hit(b, c_, tp.pad) for c_ in g_):
                return False
            g_.append(b)
        return True
    import math as _m
    off = None
    st = pl_stat(P)
    late = bk_progress(its[0].get("id") if its else None)
    if ok(boxes(0.0, 0.0), True):
        off = (0.0, 0.0)
    elif not late:
        for R_ in TP_RINGS + (8.0, 10.0, 12.0):
            for k in range(TP_RING_STEPS):
                a = 2.0 * _m.pi * k / TP_RING_STEPS
                d_ = (R_ * _m.cos(a), -R_ * _m.sin(a))
                if ok(boxes(*d_)):
                    off = d_
                    break
            if off:
                st["moved"] += 1
                break
    if off is None and False:                           # v32.4: no column + leader out of the drawing (see _pl_dwin)
        r = placed["rect"]
        y0 = min(y for _i, _x, y, _a, _p in spots)
        x0 = min(b[0] for b in boxes(0.0, 0.0))
        for xx in (r[2] + PL_LEAD["gap"], r[0] - PL_LEAD["gap"] - max(b[2] - b[0] for b in boxes(0.0, 0.0))):
            for k in range(0, 41):
                dy = ((k + 1) // 2) * 2.5 * (1.0 if k % 2 else -1.0)
                d_ = (xx - x0, dy)
                if ok(boxes(*d_)):
                    off = d_
                    break
            if off:
                st["leader"] += 1
                ax, ay = spots[0][1], spots[0][2]
                q = (xx - 0.4 if xx > r[2] else xx + 0.4 + 0.0, y0 + d_[1])
                bk_line(P, [(ax, ay), q], PL_LEAD["ink"], PL_LEAD["lw"])
                break
    forced = off is None
    off = off or (0.0, 0.0)
    if forced:
        st["forced"] += 1
        if late:
            BK_PG["late"] += 1
    g = tp._group()
    for it, x, y, al, pt in spots:
        tp.put(it["string"], x + off[0], y + off[1], pt, bool(it.get("bold")), al, 0.0, it.get("id"),
               it.get("role", "label"), it.get("colour"), allow, g, forced=forced, dgrp=_pl_dgrp(placed))
    st["labels"] += 1
    return len(spots)


def pl_labels(P, placed, side=None, roles=("label", "badge")):
    n = 0
    done_ = placed.get("_done") or set()               # v38: badges, tags and their "_sub" lines are set already
    for it in ix_texts(placed["D"]):
        if it.get("role") in roles and _pl_apt(it) is not None and id(it) not in done_:
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
    sw = sw or {}
    k = sw.get("kind", "fill")
    col = sw.get("colour") or sw.get("fill") or GRID_INK["ink"]
    if sw.get("badge") is not None or sw.get("bubble"):  # v38 (c3): a marker sample = a bubble: disc + bk_centre
        bb = dict(sw.get("bubble") or {})
        r = min(float(bb.get("r_mm") or min(W, H) * 0.45), min(W, H) * 0.5)
        bk_badge_disc(P, x + W / 2.0, y + H / 2.0, r, bb.get("fill") or col, bb.get("ring"), bb.get("ring_mm"),
                      u"swatch disc")
        t = u"%s" % (sw.get("badge") if sw.get("badge") is not None else bb.get("text", u""))
        if t.strip():
            bk_centre(P, t, x + W / 2.0, y + H / 2.0, max(float(bb.get("pt") or 4.5), GRID_MIN_PT),
                      bb.get("bold", True), bb.get("colour") or "FFFFFF", None, "badge")
        P.tp.keep((x, y, x + W, y + H), "swatch", None)
        return
    if sw.get("tag"):                                    # v38 (c3): a letter chip sample = a tag: box + bk_centre
        tg_ = sw["tag"]
        bk_rect(P, (x, y, x + W, y + H), tg_.get("fill") or col, tg_.get("ring"), 0.3)
        if tg_.get("text"):
            bk_centre(P, tg_["text"], x + W / 2.0, y + H / 2.0, max(float(tg_.get("pt") or 4.5), GRID_MIN_PT),
                      tg_.get("bold", True), tg_.get("colour"), None, "tag")
        P.tp.keep((x, y, x + W, y + H), "swatch", None)
        return
    if k == "fill":
        bk_rect(P, (x, y, x + W, y + H), col, sw.get("stroke"), sw.get("width_pt") or 0.3)
    elif k in ("line", "dash"):
        bk_line(P, [(x, y + H / 2.0), (x + W, y + H / 2.0)], col, sw.get("width_pt") or 1.0,
                sw.get("dash_pt") or ((2.0, 1.2) if k == "dash" else None), alpha=sw.get("opacity"))
        if sw.get("mark") == "triangle":                 # v38: the key map's cut row (a small filled triangle)
            bk_poly(P, [(x + W, y + H / 2.0), (x + W - 1.6, y + H / 2.0 - 1.0), (x + W - 1.6, y + H / 2.0 + 1.0)],
                    col, None, 0.1)
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


def pl_legend(P, lg, x, y, w, h=None, max_cols=2, allow=(), warn=True, pt=None, fixed=False):
    """the legend in columns (filled top to bottom), one size for every entry (stepped down together). v37: allow =
    keeps its texts may sit on (a legend inside a map, frame option allow=); warn=False: the caller reports the frame's
    textfit. v38: pt = the frame's point size (p21.7 4 pt); fixed=True: exactly max_cols columns (frame cols=)"""
    ents = [(e.get("swatch") or {}, ix_text(e.get("text"), lg.get("_folder"))) for e in lg.get("entries") or []]
    title = ix_text(lg.get("title"), lg.get("_folder")) if lg.get("title") else None
    cap = max(1, int((w + 4.0) // 40.0) or 1)
    if fixed:
        cap = max(1, int(max_cols))
    cols = max(1, min(int(max_cols), cap))
    pt0 = float(pt) if pt else grid_role("legend")[0]
    s = pt0
    while True:
        cw = (w - 4.0 * (cols - 1)) / float(cols)
        tw = cw - PL_SW["w"] - PL_SW["gap"]
        hs = [st_fit(t, tw, None, "legend", s, justify=True, page=P.pid)[3] for _sw, t in ents]
        hs = [max(hh, PL_SW["h"]) + PL_SW["row_gap"] for hh in hs]
        th = (st_fit(title, w, None, "heading", page=P.pid)[3] + 1.2) if title else 0.0
        per = -(-len(hs) // cols) if hs else 0
        colh = [sum(hs[i * per:(i + 1) * per]) for i in range(cols)]
        need = th + (max(colh) if colh else 0.0)
        if h is None or need <= h + 1e-6:
            break
        if cols < cap and cols < len(hs):                # v32.4: more columns first (same size); v33: never smaller
            cols += 1
            continue
        break
    if warn and h is not None and need > h + 1e-6:
        wn_warn(P.pid, "overrun", u"legend %s needs %.1f mm at %.1f pt, %.1f mm free" % (lg.get("id"), need, s, h))
    yy = y
    if title:
        hh, _p = st_para(P, title, x, yy, w, None, "heading", page=P.pid, allow=allow)
        yy += hh + 1.2
    g = P.tp._group()
    for i, ((sw, t), hh) in enumerate(zip(ents, hs)):
        c = i // per if per else 0
        r0 = yy + sum(hs[c * per:i])
        cx = x + c * (cw + 4.0)
        _pl_swatch(P, sw, cx, r0)
        st_para(P, t, cx + PL_SW["w"] + PL_SW["gap"], r0, tw, None, "legend", s, group=g, page=P.pid, allow=allow)
    box = (x, y, x + w, y + need)
    if allow:                                          # v37: a legend inside a map is no block beside it
        P.ink.append(("legend", box, lg.get("id")))
    else:
        P.tp.block(box, u"legend %s" % lg.get("id"))
    return box


def pl_list(P, ls, x, y, w, h=None, allow=(), pt=None):
    """numbered (or bulleted) rows; texts justified; one size for all rows (v37: h=None = no own overrun warning;
    allow as pl_legend; v38: pt = the frame's point size)"""
    rows = [ix_text(t, ls.get("_folder")) for t in ls.get("items") or []]
    numbered = ls.get("numbered", True)
    ind = 4.0
    s = float(pt) if pt else grid_role("list_item")[0]
    while True:
        hs = [st_fit(t, w - ind, None, "list_item", s, page=P.pid)[3] + 0.8 for t in rows]
        break                                          # v33: one size (L2), overrun = WARNING below
    if h is not None and sum(hs) > h + 1e-6:
        wn_warn(P.pid, "overrun", u"list %s needs %.1f mm at %.1f pt, %.1f mm free" % (ls.get("id"), sum(hs), s, h))
    yy = y
    for i, (t, hh) in enumerate(zip(rows, hs)):
        mark = (u"%d" % (i + 1)) if numbered else u"•"
        mark = fm_safe(mark, True)[0]
        P.tp.put(mark, x, yy + fm_asc_desc(s, True)[0], s, True, "L", 0.0, None, "list_item", None, tuple(allow))
        st_para(P, t, x + ind, yy, w - ind, None, "list_item", s, page=P.pid, allow=allow)
        yy += hh
    box = (x, y, x + w, yy)
    if allow:
        P.ink.append(("list", box, ls.get("id")))
    else:
        P.tp.block(box, u"list %s" % ls.get("id"))
    return box


def _pl_level_rows(lc, ry, pt):
    """v37 (round 8, D4): the level values in ONE column: [(y, lv, baseline, 0)]. A value that would crowd the one
    above it moves DOWN only (vertical, min clear PL_LEVEL["clear"]); no second column, no joining line. Never
    dropped."""
    L = PL_LEVEL
    a_, d_ = fm_asc_desc(pt, False)
    need = (a_ - d_) + L["clear"]
    rows = sorted([(ry(lv["z"]), lv) for lv in lc.get("levels") or [] if lv.get("z") is not None], key=lambda r: r[0])
    last, out = -1e9, []
    for y, lv in rows:
        b = max(y + (a_ + d_) / 2.0, last + need)
        last = b
        out.append((y, lv, b, 0))
    return out


def _pl_level_txt(lv):
    txt = u"%+.2f" % float(lv["z"])
    if lv.get("name"):
        txt += u" " + fm_safe(u"%s" % lv["name"])[0]
    return txt


def pl_levels_w(lc, k, e_top):
    """v37: the width (mm) the one-column level tags take beside a drawing at k page mm per m (reserved by bk_fit)"""
    L = PL_LEVEL
    pt = grid_role("level_value")[0]
    rows = _pl_level_rows(lc, lambda z: (e_top - float(z)) * k, pt)
    if not rows:
        return 0.0
    base = L["gap"] + sum(L["dash"]) + L["tri_w"] / 2.0 + L["label_gap"]
    return base + max(fm_width(_pl_level_txt(lv), pt) for _y, lv, _b, _c in rows)


def pl_levels(P, lc, placed, side=None):
    """level markers beside the drawing (never on it): v37 (D4) one column at the drawing's end, 1.0 mm out, a short
    dash, ▽, the value; a crowded value moves vertically only (no joining line, no second column); every value
    printed"""
    L = PL_LEVEL
    T = placed["T"]
    r = placed["rect"]
    side = (side or lc.get("side") or "R").upper()[:1]
    sg = 1.0 if side == "R" else -1.0
    length = sum(L["dash"])
    tw, th = L["tri_w"], L["tri_h"]
    pt = grid_role("level_value")[0]
    rows = _pl_level_rows(lc, T.ry, pt)
    for y, lv, _b, _c in rows:
        if not (r[1] - 1e-6 <= y <= r[3] + 1e-6):
            wn_warn(P.pid, "edge", u"level %s %+.2f of %s is outside its drawing" % (lv.get("name"), lv["z"],
                                                                                   placed["id"]))
    a_, d_ = fm_asc_desc(pt, False)
    edge = r[2] if side == "R" else r[0]
    n = 0
    for y, lv, base, col in rows:
        x0 = edge + sg * L["gap"]                          # the dash runs outward from the drawing
        xs, on = x0, True
        for dd in L["dash"]:
            if on:
                bk_line(P, [(xs, y), (xs + sg * dd, y)], L["ink"], L["lw"])
            xs += sg * dd
            on = not on
        xe = x0 + sg * length
        bk_poly(P, [(xe - tw / 2.0, y - th), (xe + tw / 2.0, y - th), (xe, y)], None, L["ink"], L["lw"])
        bx = (min(edge, xe - tw / 2.0), y - th, max(edge, xe + tw / 2.0), y + 0.2)
        P.tp.keep(bx, "marker", u"level %s" % lv.get("name"))
        P.ink.append(("marker", bx, lc.get("id")))
        lx = xe + sg * (tw / 2.0 + L["label_gap"])
        P.tp.put(_pl_level_txt(lv), lx, base, pt, False, "L" if side == "R" else "R", 0.0, lc.get("id"),
                 "level_value", L["ink"], ("marker",))
        n += 1
    return n


def pl_scalebar(P, placed, x=None, y=None, max_mm=30.0, printed=None):
    """a scale bar for a true-scale drawing (never for key maps or diagrams): round length, 4 cells, "0", "L m",
    "1:den"; (x, y) = the bar's top-left (page mm, y down), default 2 mm under the drawing's left end. v37 (L2): the
    bar is drawn at the drawing's TRUE scale (T.k); the ratio printed after it is `printed` (the page table's value),
    none when printed is None"""
    T = placed["T"]
    if not T.den:
        return None
    k = T.k                                   # mm per m
    Lm = 1.0
    for c in BK_BAR_STEPS:                    # v38 (e1): 25 and 250 added
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
    rt = u"1:{:,}".format(int(printed)) if printed else u""
    if rt:
        P.tp.put(rt, x + Lw + 3.0, y + hb, pt, False, "L", 0.0, None, "scale", ink, (), "sb_%s" % placed["id"])
    box = (x, y, x + Lw + 3.0 + (fm_width(rt, pt) if rt else 0.0), y + hb + 0.6 + a_ - _d)
    P.tp.keep((x, y, x + Lw, y + hb), "scalebar", placed["id"])
    P.ink.append(("scalebar", box, placed["id"]))
    return box


def pl_mm_drawing(P, D, T):
    """v33: a scale-free drawing (key map) at the transform T it is given (size 1 = its exported mm, never fitted), its
    texts placed round their anchors at their own size"""
    placed = rd_drawing(P, D, T)
    pl_rigid(P, placed, T.k)                # texts stay where the script set them (T.k = 1: their own point size)
    return placed


def pl_photo(P, ph, x, y, w, h, crop=True):
    """a photo kept rectangular, never stretched (G-R4-8). v38 (G9-2, PLAN d8): crop=True fills the cell: the photo
    at the cover scale, centre-cropped to the cell (a one-page PDF of the photo shown with clip=); crop=False: the
    largest size inside the box, letterboxed (v37)"""
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
    box = None
    if crop and w > 0.5 and h > 0.5:
        try:
            src = _fz.open()
            pg_ = src.new_page(width=pw, height=phh)
            pg_.insert_image(pg_.rect, filename=f)
            s = max(w / pw, h / phh)                     # cover: the photo fills the cell, the overflow is cut
            cw_, ch_ = w / s, h / s                      # the part of the photo shown (photo pixels = PDF units)
            cx0, cy0 = (pw - cw_) / 2.0, (phh - ch_) / 2.0
            P.page.show_pdf_page(_fz.Rect(x * BK_K, y * BK_K, (x + w) * BK_K, (y + h) * BK_K), src, 0,
                                 keep_proportion=False, clip=_fz.Rect(cx0, cy0, cx0 + cw_, cy0 + ch_))
            RD_DOCS.append(src)
            box = (x, y, x + w, y + h)
        except Exception as ex:
            wn_warn(P.pid, "photo", u"photo %s not cropped (%s: %s): set whole" % (ph.get("id"), type(ex).__name__, ex))
    if box is None:
        s = min(w / pw, h / phh)
        bw, bh = pw * s, phh * s
        bx, by = x + (w - bw) / 2.0, y + (h - bh) / 2.0
        P.page.insert_image(_fz.Rect(bx * BK_K, by * BK_K, (bx + bw) * BK_K, (by + bh) * BK_K), filename=f)
        box = (bx, by, bx + bw, by + bh)
    P.tp.block(box, u"photo %s" % ph.get("id"))
    P.tp.keep(box, "photo", ph.get("id"))
    P.ink.append(("photo", box, ph.get("id")))
    return box


# ---- v32.2 speed (Aras 4 Nov 21:14 "cant we squeeze in some performance boost"): a grid index for the page's texts and
# obstacles. TextPage._free and TextPage.hits_now looked at EVERY text and obstacle of the page for every spot tried
# (rings, short forms, fix passes); now only those in the grid cells the box touches. Same tests, same order of hits,
# same result: only the search is shorter. The index is rebuilt when a text or obstacle is added or taken off, and
# when a side list renumbers its boxes.
_BK_CELL = 8.0                                            # grid cell, page mm


def _bk_cells(b, pad):
    c = _BK_CELL
    return (range(int((b[0] - pad) // c), int((b[2] + pad) // c) + 1),
            range(int((b[1] - pad) // c), int((b[3] + pad) // c) + 1))


def _bk_index(tp):
    sig = (len(tp.items), id(tp.items[-1]) if tp.items else 0, len(tp.keeps), id(tp.keeps[-1]) if tp.keeps else 0,
           getattr(tp, "_bk_mut", 0))
    ix = getattr(tp, "_bk_ix", None)
    if ix is not None and ix[0] == sig:
        return ix[:3]
    gi, gk = {}, {}
    starts = (0, 0)
    if ix is not None and len(ix) > 3:                    # v32.4: texts / obstacles only ADDED since: index just those
        old, (ni, nk, li, lk, mut) = ix, ix[3]
        if (mut == getattr(tp, "_bk_mut", 0) and len(tp.items) >= ni and len(tp.keeps) >= nk and
                (ni == 0 or tp.items[ni - 1] is li) and (nk == 0 or tp.keeps[nk - 1] is lk)):
            gi, gk, starts = old[1], old[2], (ni, nk)
    for g, objs, n0 in ((gi, tp.items, starts[0]), (gk, tp.keeps, starts[1])):
        for n in range(n0, len(objs)):
            xs, ys = _bk_cells(objs[n]["box"], 0.0)
            for cx in xs:
                for cy in ys:
                    g.setdefault((cx, cy), []).append(n)
    ni, nk = len(tp.items), len(tp.keeps)
    ix = (sig, gi, gk, (ni, nk, tp.items[ni - 1] if ni else None, tp.keeps[nk - 1] if nk else None,
                        getattr(tp, "_bk_mut", 0)))
    tp._bk_ix = ix
    return ix[:3]                                         # (sig, texts grid, obstacles grid)


def _bk_near(g, b, pad):
    xs, ys = _bk_cells(b, pad)
    out = set()
    for cx in xs:
        for cy in ys:
            out.update(g.get((cx, cy), ()))
    return out


def _bk_free(self, b, allow=(), group=None):
    if not (self.inner[0] <= b[0] and b[2] <= self.inner[2] and self.inner[1] <= b[1] and b[3] <= self.inner[3]):
        return False
    if self.footer_zone and tp_hit(b, self.footer_zone, 0.0):
        return False
    _s, gi, gk = _bk_index(self)
    for n in _bk_near(gi, b, self.pad):
        it = self.items[n]
        if it["group"] != group and tp_hit(b, it["box"], self.pad):
            return False
    for n in _bk_near(gk, b, self.pad):
        K = self.keeps[n]
        if K["name"] in allow or K["kind"] in allow:
            continue
        if _tp_keep_hits(b, K, self.pad):
            return False
    return True


def _bk_hits_now(self, blocks_in=False):
    hits = []
    I = self.items
    inn = self.inner
    _s, gi, gk = _bk_index(self)

    def inside(b):
        return (inn[0] - 1e-6 <= b[0] and b[2] <= inn[2] + 1e-6 and inn[1] - 1e-6 <= b[1] and
                b[3] <= inn[3] + 1e-6)
    band = globals().get("BK_BAND_ROLES", ())
    for i, a in enumerate(I):
        b = a["box"]
        if not inside(b) and a["role"] not in band:      # v37: title band + footer sit outside the margins by design
            hits.append(("edge", a, u"the page edge or its margins"))
        if self.footer_zone and a["role"] not in ("footer", "crop_word") and tp_hit(b, self.footer_zone, 0.0):
            hits.append(("edge", a, u"the footer zone"))
        for n in sorted(j for j in _bk_near(gi, b, self.pad) if j > i):
            c = I[n]
            if c["group"] != a["group"] and tp_hit(b, c["box"], self.pad):
                hits.append(("overlap", a, c))
        for n in sorted(_bk_near(gk, b, self.pad)):
            K = self.keeps[n]
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


_bk_close0 = TpSideList.close


def _bk_close(self, tp):
    tp._bk_mut = getattr(tp, "_bk_mut", 0) + 1            # its number boxes change: the index is rebuilt
    try:
        return _bk_close0(self, tp)
    finally:
        tp._bk_mut = getattr(tp, "_bk_mut", 0) + 1


TextPage._free = _bk_free
TextPage.hits_now = _bk_hits_now
TpSideList.close = _bk_close
# ---- 60_layout (composer core, round 5 S1; round 6 S9 v31: G6-1 page frames): one page = one grid ------------------
# A3 landscape 420 x 297 mm, margins 14 / 12 (grid.py; = SON page2 margins x 3.3-96.7 %, PLAN P-6: one set for every
# page). Round 6 (v31): every block of a page sits in a FRAME of the page plan (80_plan, PLAN §3 "Target frames"),
# given in % of the page ([x, y, w, h], 0,0 top left; 1 % x = 4.2 mm, 1 % y = 2.97 mm). Title band (PLAN §3, frames
# files "common SON frame"): section label y 3-4 %, title y 5-8 %, the intro right of the title, a thin rule at 8.8 %;
# content from y 10 %; the page number alone, bottom right (PLAN §2.1: no "NN/23", no theme footer).
#   P = bk_page(doc, pid, n=None)            a new page: P.page (PyMuPDF), P.tp (TextPage over the whole sheet with the
#                                            14/12 mm margins, the edge test of 70_check), P.placed, P.ink, P.boxes
#   bk_kicker(spec) / bk_footer(spec)       v33 (L4): "<letter> <CHAPTER> · <PART>" / "<letter> <CHAPTER>" labels
#   bk_band(P, label, title, intro=None) -> y_mm   v37: kicker 8 pt, title 24 pt, lead 9.5 pt beside it (2 lines), rule
#                                            (older note: v31 title band: section label, title (16 pt bold), intro (6 pt,
#                                            justified) right of the title, rule; returns the rule's y
#   bk_caption(P, text, box)                 a caption (5 pt, justified, last line left) in its box
#   bk_pageno(P, n, label=None)              the footer: label + page number, bottom right (7 pt bold accent); log
#                                            line "pagenum <n>"
#   bk_finish(P) -> n texts                  draws every text (40_set bk_emit) after the drawings
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
BK_BAND = dict(x0=14.0, x1=406.0, kicker_pt=8.0, kicker_base=12.0, title_pt=24.0, title_base=22.0, lead_pt=9.5,
               lead_x=146.0, lead_gap=8.0, lead_step=4.0, lead_last=23.4, lead_lines=2, rule_y=25.0, rule_pt=0.25,
               no_pt=14.0, no_base=284.6, foot_pt=7.5, foot_base=284.0, foot_gap=3.0)
#                                     v37 (round 8 L4): SON page2's code (b2 40747b2 `header` / `footer`), mm and pt
BK_BAND_ROLES = ("title", "band", "footer")        # v37: title band + footer texts (no edge / offsheet test, L3)
BK_PAGENO_LOG = []                  # "pagenum <n>" lines (code.py adds them to the log)


def bk_kicker(spec):
    """v33 (L4): "<letter> <CHAPTER> · <PART>" in caps (SON page2), from the one page list"""
    part = spec.get("part")
    if not part:
        return None
    st = STAGES.get(spec.get("stage"), u"")
    return (u"%s  %s%s" % (part, PARTS.get(part, u""), (u"  ·  " + st) if st else u"")).upper()


def bk_footer(spec):
    """v33 (L4): the footer label "<letter>  <CHAPTER>" (the number follows it)"""
    part = spec.get("part")
    return (u"%s  %s" % (part, PARTS.get(part, u""))).upper() if part else None


def bk_band(P, label, title, intro=None):
    """v37 title band (round 8 L4, SON page2's code b2 40747b2 `header`): kicker 8 pt bold accent on baseline 12;
    title 24 pt bold ink on baseline 22; lead 9.5 pt (key words bold, *word* marks) beside the title from x = max(146,
    title end + 8) to 406, up to 2 lines ending on baseline 23.4, 4.0 mm apart (more lines = WARNING textfit, never
    shrunk); rule y 25, x 14-406, 0.25 pt. Every text of the band has role "title" / "band" (BK_BAND_ROLES: no edge or
    offsheet test). Returns the rule's y (mm)"""
    B = BK_BAND
    x0, x1 = B["x0"], B["x1"]
    acc, ink = GRID_INK["accent"], GRID_INK["ink"]
    if label:
        P.tp.put(label, x0, B["kicker_base"], B["kicker_pt"], True, "L", 0.0, "label", "title", acc)
    P.tp.put(title, x0, B["title_base"], B["title_pt"], True, "L", 0.0, "title", "title", ink)
    w = fm_width(title, B["title_pt"], True)
    if intro:
        lx = max(B["lead_x"], x0 + w + B["lead_gap"])
        lw = x1 - lx
        if lw < 40.0:
            wn_warn(P.pid, "title", u"title %.0f mm wide at %.0f pt: the lead gets only %.0f mm" % (w, B["title_pt"], lw))
            lw = max(lw, 20.0)
        lines, s_, lead_mm, _hh = st_fit(intro, lw, None, "intro", pt=B["lead_pt"], lead=B["lead_step"], page=P.pid)
        lines = [ln for ln in lines if ln["words"]]
        if len(lines) > B["lead_lines"]:
            bk_warn(P.pid, u"lead", u"textfit %.1f" % ((len(lines) - B["lead_lines"]) * lead_mm))
        g = P.tp._group()
        yy = B["lead_last"] - (len(lines) - 1) * lead_mm
        for ln in lines:
            for wd, b, xo in ln["words"]:
                if wd:
                    P.tp.put(wd, lx + xo, yy, s_, b, "L", 0.0, "lead", "band", ink, (), g)
            yy += lead_mm
    bk_line(P, [(x0, B["rule_y"]), (x1, B["rule_y"])], GRID_INK["rule"], B["rule_pt"])
    return B["rule_y"]


def bk_caption(P, text, box):
    return st_para(P, text, box[0], box[1], box[2] - box[0], box[3] - box[1], "caption", page=P.pid)


def bk_pageno(P, n, label=None):
    """v37 (round 8 L4, b2 40747b2 `footer`): page number 14 pt bold accent right-aligned at x 406, baseline 284.6;
    footer label "<letter>  <CHAPTER>" 7.5 pt bold ink2 right-aligned ending 3 mm left of the number, baseline 284"""
    B = BK_BAND
    xr = B["x1"]
    num = u"%d" % int(n)
    P.tp.put(num, xr, B["no_base"], B["no_pt"], True, "R", 0.0, "pageno", "footer", GRID_INK["accent"], ("footer",))
    if label:
        P.tp.put(label, xr - fm_width(num, B["no_pt"], True) - B["foot_gap"], B["foot_base"], B["foot_pt"], True, "R",
                 0.0, "footer_label", "footer", GRID_INK["ink2"], ("footer",))
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
        ln = u"layout %s fill=%.2f ref_%s=%s empty_band=%.0f overlaps %d edge %d min_text=%s" % (
            r["pid"], r["fill"], ref, (u"%.2f" % rf) if rf is not None else u"none", r["band_mm"], r["overlaps"],
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
# ---- frames_r9.py (round 9, Part A, 11 Nov 2026; G9-2, ADDENDUM A1 §0, §A, §E, §F4; PLAN §spec S2) --------------------
# THE one frame table of round 9 (plan_findings/PAGE_TABLE.md = BRIEF §4 merged with ADDENDUM §A/§E/§F4; p13 option B,
# p20 one B19 map with a legend only (PLAN Q6), p21 one shared legend (A9)). The SAME text is pasted into every producer
# (MainBoard, MasterPlan, CityLink, WaterBoard, ProposalSections, AgriCulture, WaterBalance, B19Plan) and the booklet:
# producers read their own rows (frame w x h, so F/C/key maps are drawn at frame size and M maps export context over
# r9_window); the booklet builds every F() mm from it. No file is read (script_reads.txt unchanged).
# mm, A3 landscape 420 x 297, origin top-left, y down; content x 14-406, y 26-279; 2 mm gutter between blocks.
#   R9_FRAMES["pNN.<block>"] = dict(x, y, w, h, kind, ids, series, r8, est, ...)
#       kind    S scaled drawing · M map (context grows to fill) · F fitted, no ratio · C chart (plot fills) · T text
#       ids     item id patterns (fnmatch, first frame whose pattern matches an item places it; order = stack order).
#               v37 ids where the item exists today (H1 §1.3); new=True marks ids PROPOSED here for an item a wave-2
#               part must split off (the part names its item exactly so, or lists the id it used in its handover)
#       series  name shared by the members of one series (ADDENDUM §0.6: one T, one label)
#       r8      R8's TRUE scale denominator of that drawing (context/WRITER_SYNC_2026-11-11/run_r8/page_boxes.csv),
#               None where R8 had no comparable drawing; used by ADDENDUM §0.4 only
#       est     the writer's expected printed label (PAGE_TABLE "label (writer est.)"), for the closing check only;
#               NEVER a fixed scale (the run computes it with r9_label)
#       bar     the frame key that gets this drawing's scale bar / ratio / north (booklet `bar=`)
#       others  over, allow, split, gap, cols, pt, merge, grid, card, check (an UNVERIFIED id or reading)
#   r9_frame(key) -> dict (a copy, "key" added) or None (FLAG line in R9_LOG)
#   r9_wh(key) -> (w, h) mm or None
#   r9_frame_of(item_id, page=None) -> the first frame dict whose ids match (page order, then table order), or None
#   r9_label(Tfit, r8=None) -> dict(L, T, list, size, small)        ADDENDUM §0.2-0.4: the printed label and true scale
#   r9_series_label(tfits, r8s=()) -> the same dict for a series (§0.6: Tfit = the largest member Tfit)
#   r9_tfit(focus_box, key_or_wh) -> Tfit (1:n) at which the focus box fits the frame, uniform, no stretch
#   r9_window(focus_box, key_or_wh, grow=R9_WINDOW_GROW) -> (x0, y0, x1, y1) the context extent an M map exports
#   r9_scale_line(page, block, Tfit, lab) -> the §0.9 log line (and the WARNING line when lab["small"])
# Log lines: r9_frame misses go to R9_LOG as FLAG lines (a page script appends R9_LOG to its log).
import fnmatch as _r9_fn

R9_TABLE_VERSION = "r9"
R9_GUTTER_MM = 2.0
R9_CONTENT = (14.0, 26.0, 406.0, 279.0)          # x0, y0, x1, y1 mm: the cover check's content area (BRIEF G9-2)
# ADDENDUM §0.2 (Aras 11 Nov 20:39 and 20:42): round labels first, the second list only under §0.4
R9_LBL_ROUND = (100, 200, 500, 1000, 1250, 1500, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 12500, 15000,
                20000, 30000, 40000, 50000)
R9_LBL_SECOND = (250, 2500, 25000)
R9_LBL_TOL = 1.08          # §0.3: the label may round Tfit down by up to 8 %
R9_LBL_MIN = 0.85          # §0.4: under 85 % of the fit size the second list is tried (writer's reading)
R9_WINDOW_GROW = 1.3       # PLAN §cause d4: an M map's context window = its focus grown to the frame aspect x 1.3
R9_LOG = []


def _r9(x, y, w, h, kind, ids, series=None, r8=None, est=None, **kw):
    d = dict(x=float(x), y=float(y), w=float(w), h=float(h), kind=kind, ids=tuple(ids), series=series, r8=r8,
             est=est)
    d.update(kw)
    return d


R9_FRAMES = {
    # ---- p02 (rows 2-4 and 7-8 need MainBoard to export the parts as their own items: H1 §1.3)
    "p02.1": _r9(14, 28, 194, 169, "M", ("sb_plan01",), r8=25048, est=25000, bar="p02.2"),
    "p02.5": _r9(210, 28, 196, 148, "F", ("sb_edge_types",)),
    "p02.6": _r9(210, 178, 60, 3, "T", ("sb_edge_types_caption",)),
    "p02.7": _r9(210, 183, 96, 96, "F", ("sb_site_indicators", "sb_site_readings"), new=True,
                 check=u"sb_site_readings is the v37 union item (rows 7+8); MainBoard splits it"),
    "p02.8": _r9(308, 183, 98, 96, "F", ("sb_site_landuse",), new=True),
    "p02.2": _r9(14, 199, 155, 10, "T", ("sb_plan01_bridges*",), new=True),
    "p02.3": _r9(14, 211, 194, 56, "T", ("sb_plan01_legend*",), new=True, cols=3),
    "p02.4": _r9(14, 269, 60, 3, "T", ("sb_plan01_caption",)),
    # ---- p03
    "p03.1": _r9(354, 30, 52, 56, "T", ("sb_axo_what_is_there_list*", "sb_p03_list*"),
                 check=u"the list 1-12 may be inside the axo drawing today (H1 §1.3 UNVERIFIED)"),
    "p03.2": _r9(14, 40, 392, 200, "F", ("sb_axo_what_is_there", "sb_axo_what_is_there_caption")),
    "p03.3": _r9(14, 246, 120, 24, "T", ("sb_axo_what_is_there_legend", "sb_p03_legend*")),
    "p03.4": _r9(136, 246, 198, 24, "T", ("sb_p03_sources*", "sb_axo_what_is_there_sources*")),
    "p03.5": _r9(336, 246, 70, 24, "T", ("sb_p03_axes*", "sb_axo_what_is_there_axes*")),
    # ---- p04 (series p04: S1-S4 one T, one label; A1 1, T1, T10)
    "p04.1": _r9(14, 28, 316, 59, "F", ("sb_sec_keymap_p04",)),
    "p04.2": _r9(332, 28, 74, 22, "T", ("sb_sec_keymap_p04_legend", "sb_sec_legend_p04", "sb_sec_intro*"),
                 check=u"where sb_sec_intro* belongs is UNVERIFIED (H1 §1.3)"),
    "p04.3": _r9(14, 89, 316, 58.5, "S", ("sb_sec_s1",), series="p04", r8=2479, est=2500, bar="p04.7"),
    "p04.7": _r9(332, 89, 74, 20, "T", ("sb_sec_note_s1*",)),
    "p04.4": _r9(14, 149.5, 316, 32.2, "S", ("sb_sec_s2",), series="p04", r8=2440, est=2500, bar="p04.8"),
    "p04.8": _r9(332, 149.5, 74, 20, "T", ("sb_sec_note_s2*",)),
    "p04.5": _r9(14, 183.7, 316, 54, "S", ("sb_sec_s3",), series="p04", r8=2561, est=2500, bar="p04.9"),
    "p04.9": _r9(332, 183.7, 74, 20, "T", ("sb_sec_note_s3*",)),
    "p04.6": _r9(14, 239.7, 316, 35.1, "S", ("sb_sec_s4",), series="p04", r8=2415, est=2500, bar="p04.10"),
    "p04.10": _r9(332, 239.7, 74, 20, "T", ("sb_sec_note_s4*",)),
    # ---- p05 (series p05: S5-S8; A1 2, T2)
    "p05.1": _r9(14, 28, 316, 59, "F", ("sb_sec_keymap_p05",)),
    "p05.2": _r9(332, 28, 74, 37, "T", ("sb_sec_keymap_p05_legend", "sb_sec_legend_p05", "sb_sec_intro*")),
    "p05.3": _r9(14, 89, 316, 39.7, "S", ("sb_sec_s5",), series="p05", r8=2128, est=1500, bar="p05.7"),
    "p05.7": _r9(332, 89, 74, 20, "T", ("sb_sec_note_s5*",)),
    "p05.4": _r9(14, 130.7, 316, 47.5, "S", ("sb_sec_s6",), series="p05", r8=2128, est=1500, bar="p05.8"),
    "p05.8": _r9(332, 130.7, 74, 20, "T", ("sb_sec_note_s6*",)),
    "p05.5": _r9(14, 180.2, 316, 49, "S", ("sb_sec_s7",), series="p05", r8=2128, est=1500, bar="p05.9"),
    "p05.9": _r9(332, 180.2, 74, 20, "T", ("sb_sec_note_s7*",)),
    "p05.6": _r9(14, 231.2, 316, 45, "S", ("sb_sec_s8",), series="p05", r8=2128, est=1500, bar="p05.10"),
    "p05.10": _r9(332, 231.2, 74, 20, "T", ("sb_sec_note_s8*",)),
    # ---- p06 (all parts need MainBoard to split its one board drawing: H1 §1.3)
    "p06.1": _r9(14, 28, 288, 56, "M", ("sb_edge_build",), r8=10000, est=10000, bar="p06.2"),
    "p06.4": _r9(304, 28, 102, 92, "T", ("sb_edge_build_edge*", "sb_edge_build_legend*"), new=True),
    "p06.2": _r9(14, 86, 53, 5, "T", ()),
    "p06.3": _r9(14, 93, 288, 21, "F", ("sb_edge_build_cards*",), new=True),
    "p06.5": _r9(14, 121, 62, 3, "T", ("sb_edge_build_photos_head",), new=True),
    "p06.6": _r9(14, 126, 392, 150, "F", ("sb_edge_build_photo_*",), new=True, grid=(4, 2)),
    "p06.7": _r9(14, 277, 300, 2, "T", ("sb_edge_build_caption",)),
    # ---- p07 (T11)
    "p07.1": _r9(14, 28, 292, 70, "M", ("sb_movement",), r8=10138, est=10000, bar="p07.2"),
    "p07.3": _r9(308, 28, 98, 63, "T", ("sb_mv_note_1*",)),
    "p07.2": _r9(14, 100, 90, 10, "T", ("sb_movement_caption",)),
    "p07.4": _r9(14, 112, 292, 70, "M", ("sb_walking_today",), r8=10138, est=10000, bar="p07.5"),
    "p07.6": _r9(308, 112, 98, 63, "T", ("sb_mv_note_2*",)),
    "p07.5": _r9(14, 184, 90, 10, "T", ("sb_walking_today_caption",)),
    "p07.7": _r9(14, 196, 292, 70, "M", ("sb_driving_today",), r8=10138, est=10000, bar="p07.8"),
    "p07.9": _r9(308, 196, 98, 63, "T", ("sb_mv_note_3*",)),
    "p07.8": _r9(14, 268, 90, 11, "T", ("sb_driving_today_caption",)),
    # ---- p08 (T3, T4; D6)
    "p08.1": _r9(14, 28, 300, 5, "T", ("cl_p08_corridor_head",)),
    "p08.2": _r9(14, 35, 292, 58, "M", ("cl_p08_corridor",), r8=9947, est=10000),
    "p08.3": _r9(308, 35, 98, 24, "T", ("cl_p08_corridor_legend", "cl_p08_shops")),
    "p08.4": _r9(14, 95, 392, 113, "C", ("cl_p08_who", "cl_p08_who_head")),
    "p08.5": _r9(14, 210, 186, 6, "T", ("cl_p08_who_legend", "cl_p08_who_note")),
    "p08.6": _r9(14, 218, 186, 6, "T", ("sb_street_title_n1", "sb_street_title_n2", "sb_street_title*")),
    "p08.7": _r9(14, 226, 322, 53, "F", ("sb_street_R1", "sb_street_R2", "sb_street_R3", "sb_street_R4"), r8=643,
                 split="row", gap=2.0),
    "p08.8": _r9(338, 226, 68, 9, "F", ("sb_street_keymap",),
                 check=u"D6: if unreadable at 68 x 9 mm: WARNING, the legend keeps the column"),
    "p08.9": _r9(338, 237, 68, 42, "T", ("sb_street_keymap_legend", "sb_street_legend*")),
    # ---- p09 (T5; d10: the bar frame is 3 mm, the booklet's bar band 5.5 mm)
    "p09.1": _r9(14, 28, 300, 5, "T", ("cl_p09_spine_head",)),
    "p09.2": _r9(14, 35, 292, 56, "M", ("cl_p09_spine",), r8=9983, est=10000, bar="p09.4"),
    "p09.3": _r9(308, 35, 98, 50, "T", ("cl_p09_legend", "cl_p10_legend")),
    "p09.4": _r9(14, 92, 120, 3, "T", ()),
    "p09.5a": _r9(14, 97, 76, 102, "F", ("cl_p09_card_K4", "cl_p09_card_1", "cl_p10_hub_1"), card=True),
    "p09.5b": _r9(93, 97, 76, 102, "F", ("cl_p09_card_K3", "cl_p09_card_2", "cl_p10_hub_2"), card=True),
    "p09.5c": _r9(172, 97, 76, 102, "F", ("cl_p09_card_T", "cl_p09_card_3", "cl_p10_hub_3"), card=True),
    "p09.5d": _r9(251, 97, 76, 102, "F", ("cl_p09_card_K5", "cl_p09_card_4", "cl_p10_hub_4"), card=True),
    "p09.5e": _r9(330, 97, 76, 102, "F", ("cl_p09_card_K6", "cl_p09_card_5", "cl_p10_hub_5"), card=True),
    "p09.6": _r9(14, 201, 392, 4, "T", ("cl_p09_card_key*", "cl_p09_key*"), opt=True),
    "p09.7": _r9(14, 213, 190, 66, "F", ("cl_p10_flood", "cl_p10_flood_head")),
    "p09.8": _r9(206, 213, 110, 66, "C", ("cl_p10_bank", "cl_p10_bank_head")),
    "p09.9": _r9(318, 213, 88, 46, "T", ("cl_p10_market", "cl_p10_market_head")),
    # ---- p10
    "p10.1": _r9(14, 28, 392, 105, "C", ("wb_year",)),
    "p10.2": _r9(14, 135, 230, 115, "C", ("wb_curve",)),
    "p10.3": _r9(246, 135, 160, 115, "C", ("wb_store",)),
    "p10.4": _r9(14, 252, 392, 27, "C", ("wb_answer",)),
    # ---- p11 (frames 2 and 3 inside frame 1; T6)
    "p11.1": _r9(14, 28, 276, 180, "F", ("p12_map",)),
    "p11.4": _r9(292, 28, 114, 42, "T", ("p12_steps",)),
    "p11.2": _r9(102, 30, 62, 74, "F", ("p12_zoom",), over=True),
    "p11.3": _r9(200, 30, 82, 114, "T", ("wb_p12_map_legend", "p12_map_legend", "wb_p12_map_letters",
                                         "wb_p12_relief_note"), over=True, allow="p12_map"),
    "p11.5": _r9(292, 72, 114, 55, "C", ("p12_coliforms",)),
    "p11.6": _r9(292, 129, 114, 40, "C", ("p12_plants",)),
    "p11.7": _r9(292, 171, 114, 18, "T", ("p12_why",)),
    "p11.8": _r9(292, 191, 114, 4, "T", ("wb_p12_conclusion", "p12_conclusion")),
    "p11.12": _r9(14, 210, 150, 4, "T", ("wb_p12_section_caption",),
                  check=u"which id is the caption is UNVERIFIED (H1 §1.3)"),
    "p11.9": _r9(14, 216, 40, 13, "T", ("wb_p12_section_key", "p12_section_key*", "p12_section_list*",
                                        "p12_section_head*")),
    "p11.10": _r9(56, 216, 298, 63, "F", ("p12_section_sketch", "p12_section")),
    "p11.11": _r9(356, 216, 50, 31, "T", ("wb_p12_section_levels", "wb_p12_strip_note", "wb_p12_section_legend",
                                          "p12_section_legend*")),
    # ---- p12
    "p12.1": _r9(14, 28, 180, 3, "T", ("ps_caption*", "ps_intro_note*")),
    "p12.2": _r9(300, 28, 106, 22, "F", ("ps_keymap_p12",)),
    "p12.3": _r9(14, 52, 195, 103, "F", ("ps_panel_1", "ps_W1")),
    "p12.4": _r9(211, 52, 195, 103, "F", ("ps_panel_2", "ps_W2")),
    "p12.5": _r9(14, 157, 195, 103, "F", ("ps_panel_3", "ps_W3")),
    "p12.6": _r9(211, 157, 195, 103, "F", ("ps_panel_4", "ps_W4")),
    "p12.7": _r9(14, 262, 392, 17, "T", ("ps_keymap_p12_legend", "ps_legend_strip", "ps_legend")),
    # ---- p13 option B (D12; series p13: the four cuts one T, one label; A1 3, T12; the column and the animals line
    # are new items WaterBoard splits off the season drawing, H2 §6)
    "p13.4": _r9(14, 28, 42, 12, "F", ("p15_keymap",)),
    "p13.2": _r9(60, 28, 274, 12, "F", ("p15_monthbar",)),
    "p13.1": _r9(336, 28, 70, 12, "T", ("p15_hubkey",)),
    "p13.5": _r9(14, 42, 42, 57, "T", ("p15_col_winter",), new=True),
    "p13.6": _r9(58, 42, 348, 54, "S", ("sfl_season_winter", "p15_season_winter"), series="p13", r8=487, est=250, rigid=True),
    "p13.17W": _r9(58, 96, 348, 3, "T", ("p15_animals_winter",), new=True),
    "p13.8": _r9(14, 101, 42, 57, "T", ("p15_col_spring",), new=True),
    "p13.9": _r9(58, 101, 348, 54, "S", ("sfl_season_spring", "p15_season_spring"), series="p13", r8=487, est=250, rigid=True),
    "p13.17S": _r9(58, 155, 348, 3, "T", ("p15_animals_spring",), new=True),
    "p13.11": _r9(14, 160, 42, 57, "T", ("p15_col_summer",), new=True),
    "p13.12": _r9(58, 160, 348, 54, "S", ("sfl_season_summer", "p15_season_summer"), series="p13", r8=487, est=250, rigid=True),
    "p13.17U": _r9(58, 214, 348, 3, "T", ("p15_animals_summer",), new=True),
    "p13.14": _r9(14, 219, 42, 57, "T", ("p15_col_autumn",), new=True),
    "p13.15": _r9(58, 219, 348, 54, "S", ("sfl_season_autumn", "p15_season_autumn"), series="p13", r8=487, est=250, rigid=True),
    "p13.17A": _r9(58, 273, 348, 3, "T", ("p15_animals_autumn",), new=True),
    # ---- p14 (T8, A4, A5)
    "p14.1": _r9(14, 28, 165, 5, "T", ("p16_section_head", "p16_head*"),
                 check=u"which id the heading is: UNVERIFIED (H1 §1.3)"),
    "p14.5": _r9(329, 28, 77, 135, "T", ("p16_parts", "p16_groups", "p16_bands")),
    "p14.2": _r9(14, 35, 100, 24, "F", ("p16_keymap",)),
    "p14.3": _r9(120, 35, 60, 24, "S", ("p16_section_inset",), r8=189, est=500,
                 check=u"WARNING p14 zoom scale small expected (A1 5)"),
    "p14.4": _r9(14, 61, 313, 104, "S", ("p16_section",), r8=238, est=200),
    "p14.6": _r9(14, 167, 392, 101, "C", ("p16_year",)),
    "p14.7": _r9(14, 270, 392, 9, "T", ("p16_year_plants", "p16_caption*")),
    # ---- p15 (six maps, each picked on its own)
    "p15.1": _r9(14, 28, 149, 82, "M", ("mp_sn_zones",), r8=20000, est=20000),
    "p15.2": _r9(165, 28, 44, 82, "T", ("mp_sn_zones_key",)),
    "p15.3": _r9(211, 28, 149, 82, "M", ("mp_sn_feeling",), r8=20000, est=20000),
    "p15.4": _r9(362, 28, 44, 82, "T", ("mp_sn_feeling_key", "mp_sn_feeling_wheel")),
    "p15.5": _r9(14, 112, 149, 82, "M", ("mp_sn_sound",), r8=20000, est=20000),
    "p15.6": _r9(165, 112, 44, 82, "T", ("mp_sn_sound_key",)),
    "p15.7": _r9(211, 112, 149, 82, "M", ("mp_sn_smell",), r8=20000, est=20000),
    "p15.8": _r9(362, 112, 44, 82, "T", ("mp_sn_smell_key",)),
    "p15.9": _r9(14, 196, 149, 82, "M", ("mp_sn_encounters",), r8=20000, est=20000),
    "p15.10": _r9(165, 196, 44, 82, "T", ("mp_sn_encounters_key",)),
    "p15.11": _r9(211, 196, 149, 82, "M", ("mp_sn_history", "mp_sn_photo_*"), r8=20000, est=20000,
                  check=u"the History photos row sits on the map's top (PAGE_TABLE)"),
    "p15.12": _r9(362, 196, 44, 82, "T", ("mp_sn_history_key",)),
    # ---- p16 (series p16: plans A + B; A1 6, A1 7, T7)
    "p16.1": _r9(14, 28, 64, 26, "F", ("p18_keymap", "p18_keymap_s4"), split="col", gap=2.0),
    "p16.3": _r9(80, 28, 98, 111, "S", ("p18_plan_A",), series="p16", r8=3052, est=3000),
    "p16.5": _r9(180, 28, 226, 111, "S", ("p18_plan_B",), series="p16", r8=3053, est=3000),
    "p16.2": _r9(14, 56, 64, 76, "T", ("p18_plans_legend", "p16_plans_legend", "p18_keymap_legend",
                                       "p18_keymap_s4_legend")),
    "p16.4": _r9(80, 141, 98, 10, "T", ("p18_plan_A_list",)),
    "p16.6": _r9(180, 141, 226, 9, "T", ("p18_plan_B_list",)),
    "p16.7": _r9(14, 153, 56, 35, "F", ("p18_bands", "p18_bands_head"), r8=9434),
    "p16.8": _r9(72, 153, 46, 22, "T", ("p18_band_shares", "p18_band_shares_key")),
    "p16.9": _r9(120, 153, 46, 22, "T", ("p18_foliage_shares", "p18_foliage_shares_key")),
    "p16.10": _r9(168, 153, 238, 51, "C", ("p18_heights",)),
    "p16.11": _r9(14, 206, 392, 67, "F", ("p18_card_*",), split="row", gap=2.0),
    "p16.12": _r9(14, 275, 392, 4, "T", ("p18_catalogue_sources", "p18_caption*")),
    # ---- p17 (AgriCulture splits each ladder's text from its cut: new text ids)
    "p17.1": _r9(14, 28, 392, 22, "F", ("ag3_chain",)),
    "p17.2": _r9(14, 52, 64, 45, "T", ("ag3_ladder_high_text",), new=True),
    "p17.3": _r9(80, 52, 326, 45, "F", ("ag3_ladder_high",)),
    "p17.4": _r9(14, 99, 64, 47, "T", ("ag3_ladder_low_text",), new=True),
    "p17.5": _r9(80, 99, 326, 47, "F", ("ag3_ladder_low",)),
    "p17.6": _r9(14, 148, 64, 46, "T", ("ag3_ladder_harvest_text",), new=True),
    "p17.7": _r9(80, 148, 326, 46, "F", ("ag3_ladder_harvest",)),
    "p17.8": _r9(14, 196, 60, 83, "T", ("ag3_notes", "ag3_remove*", "ag3_odour*", "ag3_note_steps", "ag3_note_legend",
                                       "ag3_note_*")),
    "p17.9": _r9(76, 196, 330, 83, "F", ("ag3_bands",)),
    # ---- p18 (rows 4-5 = ag1_stream split by AgriCulture)
    "p18.1": _r9(14, 28, 240, 60, "F", ("wb_farms", "wb_p21_cap_wb_farms"), check=u"flow 1-7 = wb_farms: UNVERIFIED"),
    "p18.2": _r9(256, 28, 150, 60, "F", ("wb_farms_out",)),
    "p18.3": _r9(14, 90, 130, 34, "F", ("wb_decision", "wb_p21_cap_wb_decision"),
                 check=u"four figures = wb_decision: UNVERIFIED"),
    "p18.4": _r9(146, 90, 70, 26, "T", ("ag1_stream_text", "ag1_stream_head"), new=True),
    "p18.5": _r9(218, 90, 188, 40, "C", ("ag1_stream",)),
    "p18.6": _r9(14, 132, 240, 103, "C", ("ag1_bars", "ag1_bars_caption")),
    "p18.7": _r9(256, 132, 150, 103, "F", ("ag1_context", "ag1_context_head")),
    "p18.8": _r9(14, 237, 128, 42, "F", ("ag1_reading*",)),
    "p18.9": _r9(144, 237, 130, 42, "F", ("ag1_history", "ag1_history_head", "ag1_history_note")),
    "p18.10": _r9(276, 237, 130, 42, "F", ("ag1_crops_*",)),
    # ---- p19 (all parts need MainBoard to split its one board drawing)
    "p19.1": _r9(14, 28, 96, 113, "F", ("sb_heritage_loop_diagrams",), new=True),
    "p19.3": _r9(112, 28, 224, 205, "M", ("sb_heritage_loop",), r8=10000, est=9000, bar="p19.4"),
    "p19.5": _r9(338, 28, 68, 205, "F", ("sb_heritage_loop_photo_*",), new=True),
    "p19.2": _r9(14, 143, 96, 92, "F", ("sb_heritage_loop_places",), new=True),
    "p19.4": _r9(112, 235, 120, 6, "T", ("sb_heritage_loop_ab*",), new=True),
    "p19.6": _r9(14, 243, 270, 16, "T", ("sb_heritage_loop_legend", "sb_heritage_legend")),
    "p19.7": _r9(14, 275, 100, 4, "T", ("sb_heritage_loop_caption",)),
    # ---- p20 (F4 + PLAN Q6: B19 exports a legend only -> legend 392 wide, rows 4-5 not used; R8 drew two halves at
    # 1:4,991, not comparable with one map (F3), so r8=None)
    "p20.1": _r9(14, 28, 392, 190, "M", ("b19_p20_map",), est=7000, new=True, bar="p20.2"),
    "p20.2": _r9(14, 220, 392, 5, "T", ("b19_p20_caption",), new=True),
    "p20.3": _r9(14, 227, 392, 52, "T", ("b19_p20_legend*",), new=True, cols=3),
    # ---- p21 (A9: one shared legend 4 pt; series p21s: sections D1 + D2)
    "p21.1": _r9(14, 28, 195, 124, "M", ("mp_dt_*upstream",), r8=1062, est=1000, bar="p21.4"),
    "p21.2": _r9(211, 28, 195, 124, "M", ("mp_dt_*k5",), r8=1062, est=1000, bar="p21.5"),
    "p21.4": _r9(14, 154, 80, 6, "T", ()),
    "p21.5": _r9(211, 154, 80, 6, "T", ()),
    "p21.6": _r9(14, 162, 195, 48, "S", ("mp_dt_*upstream_sec",), series="p21s", r8=1012, est=1250),
    "p21.8": _r9(211, 162, 195, 48, "S", ("mp_dt_*k5_sec",), series="p21s", r8=1012, est=1250),
    "p21.7": _r9(14, 212, 362, 67, "T", ("mp_dt_*upstream_sec_key", "mp_dt_*upstream_leg*", "mp_dt_*upstream_route",
                                        "mp_dt_*upstream_why", "mp_dt_*k5_sec_key", "mp_dt_*k5_leg*",
                                        "mp_dt_*k5_route", "mp_dt_*k5_why", "mp_dt_keymap_legend"),
                 merge=True, cols=4, pt=4.0),
    "p21.3": _r9(380, 243, 26, 36, "F", ("mp_dt_keymap",),
                 check=u"PAGE_TABLE calls it T*: a key map placed F-style (uniform fit)"),
}
# pages whose v37 items are no longer placed (logged "skip" by the booklet): ADDENDUM F2.4
R9_PAGE_SKIP = {"p20": ("mp_plan_*",)}


def _r9_order(key):
    """page, then the table's own order (dict order is insertion order on Python 3.7+)"""
    return (key.split(".")[0], list(R9_FRAMES).index(key))


def r9_frame(key):
    """the frame of R9_FRAMES[key] as a copy with "key" added; None (and a FLAG line in R9_LOG) when the table has
    no such key"""
    f = R9_FRAMES.get(key)
    if f is None:
        R9_LOG.append(u"FLAG r9_frame %s: no such frame in R9_FRAMES (table %s)" % (key, R9_TABLE_VERSION))
        return None
    return dict(f, key=key)


def r9_wh(key):
    """(w, h) mm of a frame key, or a (w, h) pair passed through; None for an unknown key"""
    if isinstance(key, (tuple, list)) and len(key) == 2:
        return float(key[0]), float(key[1])
    f = r9_frame(key)
    return (f["w"], f["h"]) if f else None


def r9_frame_of(item_id, page=None):
    """the first frame (page order, then table order) whose ids match item_id (fnmatch, case-sensitive); page
    ("p13") limits the search to that page; None when no pattern matches"""
    s = u"%s" % item_id
    for key in sorted(R9_FRAMES, key=_r9_order):
        if page and not key.startswith(u"%s." % page):
            continue
        for pat in R9_FRAMES[key]["ids"]:
            if _r9_fn.fnmatchcase(s, pat):
                return dict(R9_FRAMES[key], key=key)
    return None


def _r9_pick(Tfit, labels):
    """ADDENDUM §0.3: the smallest label L with Tfit <= L x 1.08 (the largest label when none qualifies)"""
    cand = sorted(set(int(v) for v in labels))
    for L in cand:
        if Tfit <= L * R9_LBL_TOL:
            return L
    return cand[-1]


def r9_label(Tfit, r8=None):
    """ADDENDUM §0.2-0.4 for one S drawing or M map: dict(L = printed label 1:L, T = true scale 1:T = max(Tfit, L),
    list "round" | "second", size = Tfit / T, small = True when even the second list misses 85 % or R8's size).
    The second list is tried when the round pick draws under 85 % of the fit size or smaller than R8 drew it.
    Writer's reading of "smaller than R8 drew it" (needed so §0.4's own p4 example holds): T larger than
    max(r8, Tfit), i.e. smaller than R8 unless the frame itself does not allow R8's size. Examples (§0.4): Tfit 1,252
    -> L 1,250, T 1,252; Tfit 2,560 with r8 2,479 -> 3,000 is smaller than R8 -> second list -> L 2,500, T 2,560."""
    Tfit = float(Tfit)

    def bad(T_):
        return Tfit / T_ < R9_LBL_MIN or (r8 is not None and T_ > max(float(r8), Tfit) * 1.0005)
    L = _r9_pick(Tfit, R9_LBL_ROUND)
    T = max(Tfit, float(L))
    lst, small = "round", False
    if bad(T):
        L2 = _r9_pick(Tfit, R9_LBL_ROUND + R9_LBL_SECOND)
        T2 = max(Tfit, float(L2))
        small = bad(T2)                                  # the combined pick is also the biggest drawing possible
        L, T = L2, T2
        lst = "second" if L2 in R9_LBL_SECOND else "round"
    return dict(L=int(L), T=T, list=lst, size=Tfit / T, small=small)


def r9_series_label(tfits, r8s=()):
    """ADDENDUM §0.6: one T and one label for a series: Tfit = the largest member Tfit (the one that fits every
    member), r8 = the largest member R8 true scale (writer's reading); None without members"""
    tf = [float(v) for v in tfits if v]
    if not tf:
        return None
    r8 = [float(v) for v in r8s if v]
    return r9_label(max(tf), max(r8) if r8 else None)


def r9_tfit(focus_box, key_or_wh):
    """Tfit (the 1:n denominator) at which focus_box = (x0, y0, x1, y1) in drawing METRES fits the frame (key or
    (w, h) mm) uniformly; None for an unknown frame"""
    wh = r9_wh(key_or_wh)
    if not wh:
        return None
    fw = max(1e-6, float(focus_box[2]) - float(focus_box[0]))
    fh = max(1e-6, float(focus_box[3]) - float(focus_box[1]))
    return max(fw * 1000.0 / wh[0], fh * 1000.0 / wh[1])


def r9_window(focus_box, key_or_wh, grow=None):
    """PLAN §cause d4: the context extent an M map exports: the focus box (drawing metres, the map's own axes) grown
    to the frame's aspect at Tfit and then x grow (default R9_WINDOW_GROW 1.3, room for T up to 1.3 x Tfit), centred
    on the focus. Returns (x0, y0, x1, y1) metres, or the focus box itself (FLAG in R9_LOG) for an unknown frame.
    The producer exports its context over this window (clamped to its data, logging where the data ends) plus the
    focus box as the drawing's "focus"; the booklet fits the focus and clips a frame-sized window"""
    wh = r9_wh(key_or_wh)
    if not wh:
        R9_LOG.append(u"FLAG r9_window %s: unknown frame, the focus box is used as the window" % (key_or_wh,))
        return tuple(float(v) for v in focus_box)
    g = float(R9_WINDOW_GROW if grow is None else grow)
    tf = r9_tfit(focus_box, wh)
    W, H = wh[0] * tf / 1000.0 * g, wh[1] * tf / 1000.0 * g
    cx = 0.5 * (float(focus_box[0]) + float(focus_box[2]))
    cy = 0.5 * (float(focus_box[1]) + float(focus_box[3]))
    return (cx - 0.5 * W, cy - 0.5 * H, cx + 0.5 * W, cy + 0.5 * H)


def r9_scale_line(page, block, Tfit, lab):
    """ADDENDUM §0.9: `scale <page> <block> fit 1:<Tfit> true 1:<T> label 1:<L> list <round|second> size <%>`; a
    second line `WARNING <page> <block> scale small` when lab["small"]. Returns the lines (a list)."""
    out = [u"scale %s %s fit 1:%d true 1:%d label 1:%d list %s size %d %%" % (
        page, block, int(round(float(Tfit))), int(round(lab["T"])), lab["L"], lab["list"],
        int(round(100.0 * lab["size"])))]
    if lab.get("small"):
        out.append(u"WARNING %s %s scale small" % (page, block))
    return out
# ---- Category -> hue table r9 (round 9 S5, 11 Nov 2026; BRIEF G9-6, PLAN.md §spec S5; replaces the round 6 table) ----
# ONE table every key, legend and map reads (Aras 4 Nov 09:44-10:08: "categorize the legends like heritage is categorized
# under heritage with similar shades of the same colour. The darker the shade is the more important it is"): each
# category one hue family, items inside it = its ranks, r1 darkest = most important; never a separate hue per item.
# Round 9 adds the G9-6 families CLA (clashes), LC (green / land cover), STR (streets), RDG (readings) and FAB (building
# fabric), redefines HER_RANK (r1 monuments, r2 historic bridges, r3 other historic buildings) and adds HUE_NAME, one
# name -> (code, rank) map so keys and maps look the same thing up the same way. Existing ramps are unchanged.
# Paste: replaces the block from "# ---- Category -> hue table" to the end of hue_log in all 8 producer copies; the
# booklet gets one copy (modules/INTERFACES.md). Values: PLAN.md §spec S5 (sources per row below).
#   HUE[code][rank] hex      HUE_KEY[name] hex      hue(code, rank, strong=False)      HER_RANK[name] -> 1/2/3
#   her_rank(name, default=3)                       hue_name(name, default=None, cat=None) -> (code, rank) or default
#   hue_of(name, default=None, cat=None) -> hex     fab_hex(cls) / lc_hex(cls) / str_hex(cls) -> hex
#   legend_group(entries)    entries sorted by category (table order) then rank
#   hue_log(page, log=None)  the line `legend <page> hues=table r9`
HUE_TABLE = "r9"
HUE_CATS = ("CTX", "FAB", "HER", "CLA", "WAT", "WW", "LC", "GRN", "AGR", "STR", "MOV", "PUB", "RDG")  # legend order
HUE_NAMES = {"CTX": u"Existing context", "FAB": u"Building fabric", "HER": u"Heritage", "CLA": u"Clashes",
             "WAT": u"The Selinos stream", "WW": u"Water works: collect, clean, hold",
             "LC": u"Existing green and land cover", "GRN": u"Planting", "AGR": u"Farms", "STR": u"Streets",
             "MOV": u"Streets, shops and movement", "PUB": u"Public life and hubs", "RDG": u"Readings"}
HUE = {
    # existing context: ground, buildings, streets, bridges, existing green (with tree symbols), workshops, vacant;
    # r2 = named buildings that are not heritage (G9-6: e.g. Les Pergamon Boutique Hotel)
    "CTX": {1: "4A3F35", 2: "847E75", 3: "B0AC9C", 4: "D8D5CC", 5: "EFEDE6"},
    # building fabric on maps (G9-4 / A1 C1): FABRIC_PLAN SB:17437-17444 in its class order, + CTX r4 for unsurveyed
    "FAB": {1: "AF7474", 2: "8B3A3F", 3: "4A3F35", 4: "7A6E60", 5: "BCB794", 6: "DCD5C2", 7: "FAF8F1", 8: "E6E0C8",
            9: "D8D5CC"},
    # heritage (G9-6): r1 monuments, r2 historic bridges, r3 other historic buildings, r4 heritage area tint
    "HER": {1: "512E1A", 2: "84573E", 3: "B08870", 4: "E7CABB"},
    # clashes C1-C6 (G9-6, Q8): one dark-red shade (MARK_C SB:17460)
    "CLA": {1: "8B3A3F"},
    # water (G9-6): r1 stream, r2 basins, r3 channels, r4 tint
    "WAT": {1: "32525F", 2: "5D7F8D", 3: "91ADB4", 4: "C1D3DB"},
    # water works: reed basins, spillway, winter store, dry-top terraces, side arm, widened wetland (own family, kept)
    "WW": {1: "2D564E", 2: "54857D", 3: "87BBAA", 4: "CBEDE5"},
    # existing green / land cover (G9-6 woods -> orchards -> grass; SB:1050 GREEN_SUB, SB:45289-45295 LC_CLASSES):
    # r1 woods, r2 orchards (shrub ACB38C shares r2: LC_HEX), r3 grass, r4 fields
    "LC": {1: "74804F", 2: "8F966A", 3: "ABB287", 4: "BDB57A"},
    # proposed planting: bands wet -> dry, forest corridor, designed green (plant swatches: tree r1, shrub r2,
    # ground / emergent r3, P-3) (own family, kept)
    "GRN": {1: "3C4733", 2: "70754C", 3: "89986A", 4: "C2CCB3"},
    "AGR": {1: "534E25", 2: "948B49", 3: "C6C08D", 4: "E6E3C5"},
    # streets (G9-6 oranges, main -> secondary -> local): the SON SEQ stops SB:18275; casing STR_CASING
    "STR": {1: "EA8C3E", 2: "F6CF85", 3: "EEE9DA"},
    # streets and movement: pedestrian r1, calmed r2, shared r3; commerce r1, mixed r2, residential r3
    "MOV": {1: "734C17", 2: "A67628", 3: "CCA363", 4: "EAD1A4"},
    # project moves and hubs (G9-6): r1 transit hub T, r2 walking hubs K3-K5, r3 numbered places, r4 tint
    "PUB": {1: "452842", 2: "7F5B7B", 3: "AE90AA", 4: "DECFDC"},
    # readings: sky view and similar (G9-6 blue-grey, one shade; PLAN S5 value, distinct from WAT)
    "RDG": {1: "7C8A99"},
}
# annotations (not a category): study area line, plan cut marks (G6-4), text ink
HUE_ANN = {"study": "6A4C93", "cut": "8E8F8A", "ink": "2C2219"}
# strong set: key maps only (G6-5, the p08 "Where each street is cut" look)
HUE_KEY = {"fabric_mix": 0.40, "her1": "663214", "her2": "965630", "her3": "C18A65",
           "trees": "A0A681", "park": "B1B792", "grass": "C4C7A6", "farmland": "CFC99D",
           "stream": "7FA4B3", "stream_edge": "5E8494", "road": "FAF8F1", "road_edge": "DCD5C2",
           "street_names": "A4A1A3", "cut": "C0392B", "study": "6A4C93"}
HUE_NAME_PT = 4.0                    # key-map street names: exactly the 4 pt floor (PLAN §2.7)
# building fabric classes (A1 C1; SB fabric_types) in FAB rank order; legend words = SB FABRIC_SHORT (SB:5371)
FAB_CLASSES = ("monument", "sacred", "traditional", "block", "regular", "selfbuilt", "large", "construction",
               "unsurveyed")
FAB_RANK = dict((c, i + 1) for i, c in enumerate(FAB_CLASSES))
FAB_WORDS = {"monument": u"Monuments, historic", "sacred": u"Mosques & sacred", "traditional": u"Old town fabric",
             "block": u"Apartment blocks", "regular": u"Planned low-rise", "selfbuilt": u"Small irregular",
             "large": u"Civic & industrial", "construction": u"Under construction",
             "unsurveyed": u"Type not surveyed"}
# land-cover classes of basemap.json "lc" (WorldCover keys) and map zones -> hex and LC rank. Shrub and park are the
# map colours already printed (SB:45291 shrub = mix(CAT green, PAPER, 0.3); SB:1050 park); their ranks are readings.
LC_HEX = {"trees": "74804F", "wood": "74804F", "orchard": "8F966A", "shrub": "ACB38C", "park": "8F9A68",
          "grass": "ABB287", "farmland": "BDB57A", "agri": "BDB57A"}
LC_RANK = {"trees": 1, "wood": 1, "orchard": 2, "shrub": 2, "park": 3, "grass": 3, "farmland": 4, "agri": 4}
# street classes of basemap.json streets ("main", "secondary", "lane"; "path" = pedestrian) -> STR rank
STR_RANK = {"main": 1, "secondary": 2, "lane": 3, "local": 3, "path": 3}
STR_CASING = "B0AC9C"                # CTX r3: the casing line of a street area / centreline (PLAN S5)
STR_CASING_MM = 0.1
# heritage ranks (G9-6, PLAN S5): r1 monuments (Kızıl Avlu, Bergama Ulu Cami; Akropol and Asklepion as ancient
# monuments = writer reading), r2 historic bridges, r3 other historic buildings. A name not listed and marked historic
# in the data (NAMES "cat" her) takes r3 (her_rank default). Teleferik is context (CTX), not heritage.
HER_RANK = {u"Kızıl Avlu": 1, u"Ulucami": 1, u"Ulu Cami": 1, u"Bergama Ulu Cami": 1, u"Akropol": 1, u"Asklepion": 1,
            u"Ulucami Önü Köprüsü": 2, u"Üç Kemer Köprüsü": 2, u"Tabak Köprüsü": 2,
            u"Bergama Yabets Havrası": 3, u"Tabaklar Hamamı": 3, u"Arasta": 3, u"Bergama Müzesi": 3,
            u"Emir Sultan Cami": 3, u"Eski Çırçır Fabrikası": 3}
# named things -> (code, rank): hub codes and clash codes (K3-K5 as walking hubs, K6 the gateway, T the transit hub,
# CL HUB_CODE / HUB_COL CL:11029), the descriptive crossings (context), readings, named non-heritage buildings.
# Heritage names are read from HER_RANK; any other row of the names table falls back by its "cat" (hue_name).
HUE_NAME = {u"T": ("PUB", 1), u"K3": ("PUB", 2), u"K4": ("PUB", 2), u"K5": ("PUB", 2), u"K6": ("CTX", 2),
            u"C1": ("CLA", 1), u"C2": ("CLA", 1), u"C3": ("CLA", 1), u"C4": ("CLA", 1), u"C5": ("CLA", 1),
            u"C6": ("CLA", 1),
            u"side inlet crossing": ("CTX", 2), u"small crossing": ("CTX", 2),
            u"Adnan Menderes Bulvarı road bridge": ("CTX", 2),
            u"sky view": ("RDG", 1), u"Les Pergamon Boutique Hotel": ("CTX", 2), u"Teleferik": ("CTX", 1)}
# NAMES r9 "cat" -> (code, rank) for a names-table row in neither HUE_NAME nor HER_RANK (hub request 11 Nov 18:47)
HUE_CAT_FALLBACK = {"her": ("HER", 3), "sacred": ("FAB", 2), "culture": ("CTX", 2), "civic": ("CTX", 2)}
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
    """the heritage rank of a place name (HER_RANK; any other historic place = 3)"""
    return HER_RANK.get(name, default)


def _hue_key(s):
    """a name as a lookup key: single spaces, lower case, Turkish İ / I handled (as names.py name_key)"""
    s = u" ".join((s or u"").split()).replace(u"İ", u"i").replace(u"I", u"ı")
    return s.lower().replace(u"i̇", u"i")


_HUE_NAME_K = dict((_hue_key(k), v) for k, v in HUE_NAME.items())
_HER_RANK_K = dict((_hue_key(k), v) for k, v in HER_RANK.items())


def _hue_name_cat(name):
    """the "cat" of the names-table row a name stands for (NAMES r9 landmarks, read through landmark_match when the
    script has names.py), or None (no table, no row, or a row without "cat")"""
    N = globals().get("NAMES")
    if not isinstance(N, dict):
        return None
    rows = N.get("landmarks") or {}
    lm = globals().get("landmark_match")
    key = None
    if callable(lm):
        try:
            key = lm(name)
        except Exception:
            key = None
    if key is None:
        k = _hue_key(name)
        for kk, row in rows.items():
            if k == _hue_key(row.get("name")) or k in [_hue_key(a) for a in row.get("alias") or ()]:
                key = kk
                break
    row = rows.get(key) if key is not None else None
    return row.get("cat") if isinstance(row, dict) else None


def hue_name(name, default=None, cat=None):
    """(code, rank) of a named thing: HUE_NAME first (hub and clash codes, crossings, readings, named non-heritage
    buildings), then HER_RANK (("HER", rank)), then the names-table "cat" (given, or looked up): her -> HER r3,
    sacred -> FAB sacred, culture / civic -> CTX r2. Else default (None: the caller keeps its own category)"""
    k = _hue_key(name)
    if k in _HUE_NAME_K:
        return _HUE_NAME_K[k]
    if k in _HER_RANK_K:
        return ("HER", _HER_RANK_K[k])
    c = cat if cat is not None else _hue_name_cat(name)
    if c in HUE_CAT_FALLBACK:
        return HUE_CAT_FALLBACK[c]
    return default


def hue_of(name, default=None, cat=None):
    """the hex of a named thing (hue_name -> hue), or default when the name has no category"""
    cr = hue_name(name, None, cat)
    return hue(cr[0], cr[1]) if cr else default


def fab_hex(cls):
    """the map colour of a building fabric class (FAB ramp; an unknown class = unsurveyed)"""
    return HUE["FAB"][FAB_RANK.get(cls, FAB_RANK["unsurveyed"])]


def lc_hex(cls, default=None):
    """the map colour of a land-cover class (LC_HEX), or default"""
    return LC_HEX.get(cls, default)


def str_hex(cls):
    """the colour of a street class (STR ramp; an unknown class = local)"""
    return HUE["STR"][STR_RANK.get(cls, 3)]


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
    """the done-when line of a legend or key drawn from this table: `legend <page> hues=table r9`"""
    ln = u"legend %s hues=table %s" % (page, HUE_TABLE)
    (log if log is not None else HUE_LOG).append(ln)
    return ln
# ---- 80_plan (round 7 S7, v33; v37 round 8 table pass): the 22-page booklet plan as ABSOLUTE FRAMES, FITTED ---------
# round 8 page table = PLAN.md §table (revision_2026-11-08_round8: BRIEF §3 frame rows + PLAN §table corrections +
# Aras's answers Q1-Q8; SON source edition per page in the comment above each page). Ids = what the producers export
# today (MainBoard v65, MasterPlan v45, WaterBoard v19, AgriCulture v14, ProposalSections v23, CityLink v12,
# WaterBalance v13); handover P6_booklet_table_done.md lists every frame, the skipped ids and the expected WARNINGs.
# ONE numbering: p01 ... p22 (BRIEF §6), exported directly by every content script. Each content page: part / stage
# (kicker "<letter> <CHAPTER> · <PART>", contents, footer "<letter> <CHAPTER>  <n>"), title, intro (lead; used only when
# no script exports a role "intro" text, or when the exported one repeats the kicker), frames, side (the frame key
# where unlisted items go, each with WARNING "<page> <id> unlisted").
# A frame F(ids, x, y, w, h, den=None, f=1.0, **opt): ids = one fnmatch pattern or a tuple of them (the first frame
# naming an item places it, in that frame only); x, y, w, h in MM on the A3 sheet (420 x 297, origin top left, y
# down), every box inside x 14-406, y 26-279 (L3); the box is ABSOLUTE: it never moves or grows, no block depends on
# another (L1). Everything in it is FITTED (bk_fit, L2): the frame's drawings (one, or a split "row" | "col" group as
# one) get ONE uniform factor, the largest that fits after their head, subtitle, label band, level column, scale band
# and the frame's texts (its own matched texts and, when the frame has no note=, its drawings' attached notes that no
# frame names). den = the PRINTED scale (n of 1:n, true-scale "m" drawings; an int, or a dict id -> den in a split
# frame): the true scale stays within +-6 % of it (else WARNING "<page> <drawing> fit true 1:n needed 1:m", overflow,
# nothing moves), the bar is drawn at the true scale, the ratio printed is den. No den: free fit (bar only). "mm"
# drawings (diagrams, charts, boards, key maps, sketches) fit freely, never above x1.15 of f (their base size, 1.0 =
# the exported size; no frame sets it).
# Options: key (name; default the first pattern), note (frame key where this frame's drawings' attached notes and
# numbered-label rows go), split + gap (several drawings side by side / stacked, fitted as one group), al ("TL"
# default; "TR", "MC" ...), bar (frame key: the drawing's bar / ratio / north at the bottom-left of THAT frame, e.g. a
# section's note frame, or an empty opt= frame kept for it), noscale (no ratio printed: SON prints none, the drawing's
# own bar is its scale), rigid (a section keeps its labels where its script set them, no label band above it: p13),
# allow (an item id whose keep this frame's texts may sit on: the p11 legend inside its map, L9), opt (an empty frame
# is no WARNING "missing"), over (documentation only: the frame sits on another one on purpose).
# skip: item id patterns a page does not place (SON has no block for them; logged "skip <page> <id> ...", D4 / F12).
# v38 (round 9): the frames below are built from R9_FRAMES (bk_r9_frames after BK_PAGES): den is no longer a table
# value (a layout-table den = Aras's fixed label); kind S / M get the ADDENDUM §0 label rule (bk_fit, bk_prepass),
# F fits freely, C at most x1.15, T never grows; new options cols, pt, merge, grid, card, series, r8 (see NEW IN v38).


def F(ids, x, y, w, h, den=None, f=1.0, **kw):
    return dict(kw, ids=ids, mm=(float(x), float(y), float(x) + float(w), float(y) + float(h)), den=den, f=float(f))


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

BK_PAGES = [                          # v38: frames and side frame of pages 2-21 from R9_FRAMES (bk_r9_frames)
    dict(pid="p01", kind="cover"),
    dict(pid="p02", part="A", stage="an", title=u"What is there, grain of the town",
         intro=u"The whole survey area *as it is today*: buildings by *urban fabric*, ground and green, the *Selinos "
               u"stream* with its edges and *six bridges*, and the places where *stream and town clash*."),
    dict(pid="p03", part="A", stage="an", title=u"Heights and enclosure",
         intro=u"Plan 01 as a parallel axonometric: *heights* are what the plan cannot show; the *sky view* from the "
               u"stream bed marks its *most enclosed* stretch."),
    dict(pid="p04", part="A", stage="an", title=u"Sections across the stream",
         intro=u"Cuts *across the Selinos stream*, each drawn *as it is*: the ground, the *bed and banks*, the "
               u"buildings, trees and fields it crosses."),
    dict(pid="p05", part="A", stage="an", title=u"Sections across the stream",
         intro=u"Cuts *across the Selinos stream*, each drawn *as it is*: the ground, the *bed and banks*, the "
               u"buildings, trees and fields it crosses."),
    dict(pid="p06", part="A", stage="got", title=u"The stream edge and where we can build",
         intro=u"Both banks *every 4 m*, and the ground *open to change*: where the project *can build*."),
    dict(pid="p07", part="B", stage="an", title=u"How people use it",
         intro=u"*Shops* line Kınık Caddesi and Üç Kemer Caddesi, the *primary commercial spines*; *walking* and "
               u"*driving* today, street by street."),
    dict(pid="p08", part="B", stage="got", title=u"The stream joins the town where the shops already are",
         intro=u"One *corridor*: the shop streets, the *hidden stream* and the project from end to end; *who* comes "
               u"when; each *street cut* today and with the project."),
    dict(pid="p09", part="B", stage="do", title=u"The streamside spine, hub by hub",
         intro=u"*Five bridge places* on existing bus stops, *walking hubs* with a *sub-hub in the bed*, one *transit "
               u"hub*: the spine along the Selinos, hub by hub.",
         skip=("cl_p10_win_*", "cl_p10_windows_head", "cl_p09_windows_head")),
    dict(pid="p10", part="C", stage="an+got", title=u"The water balance",
         intro=u"How much *winter water* can we hold for the farms' *dry summer*, and at *what cost*?"),
    dict(pid="p11", part="C", stage="do", title=u"Collect, clean, hold",
         intro=u"*Collect* winter stream water and runoff at the upstream entry, *clean* it once in *lined reed "
               u"basins*, *hold* it in the ground for the dry summer; the clean stream leaves for the *farms outside*."),
    dict(pid="p12", part="C", stage="do", title=u"The proposals in section",
         intro=u"Four cuts, *upstream to downstream*: each proposal *in section*, the winter water and the summer "
               u"strip, the reach of the *design flood (Q500)*."),
    dict(pid="p13", part="C", stage="do", title=u"Four seasons on one cut",
         intro=u"*One cut, one viewpoint, four seasons*: the *water level* decides what the place becomes, which "
               u"plants are in *leaf or flower*, and which animals are about."),
    dict(pid="p14", part="C", stage="do", title=u"The S4 cut, north-east bank",
         intro=u"The north-east bank of S4: *seat steps* and a *raised promenade* over Q500 stay; the *planting follows "
               u"the days under water*, the use follows the months."),
    dict(pid="p15", part="C", stage="do", title=u"The senses and the water",
         intro=u"The *fade-out zones* and the *senses*, zone by zone, *upstream to downstream*."),
    dict(pid="p16", part="C", stage="do", title=u"Which plant goes where",
         intro=u"*Wet to dry, low to high*: rushes and loosestrife *at the water*, willow and tamarisk on the *banks "
               u"that flood*, shade trees and olives on the *dry tops*; reed and water mint only in *lined basins*."),
    dict(pid="p17", part="C", stage="do", title=u"One plant ladder, streambed to field",
         intro=u"One cut from the *stream to the farms*, through the year: what the *water* does and what *people* do "
               u"on each step."),
    dict(pid="p18", part="C", stage="do", title=u"Where the clean water goes, and what it grows",
         intro=u"Clean water to *farmland outside the site*, easing an *overused aquifer*, *never drinking water*; "
               u"*same storage, different crops*: the *hectares* each crop irrigates.",
         skip=("ag2_farms*",)),
    dict(pid="p19", part="D", stage="do", title=u"The heritage loop",
         intro=u"The Selinos is the *seam*: *bridges, crafts and events* tie the *Kale side* to the *bazaar side*."),
    dict(pid="p20", part="E", stage="do", title=u"Masterplan: an ecological corridor",
         intro=u"The whole project on one plan: *walking hubs*, *reed basins* and terraces that *hold the rain*, "
               u"*calmed streets*, along the Selinos as an *ecological corridor*."),
    dict(pid="p21", part="E", stage="do", title=u"The water edge, plan and section",
         intro=u"Two windows, each *plan with its section*: the *upstream entry* (collect, clean, hold) and *Üç Kemer "
               u"Köprüsü* with Demeter's Garden."),
    dict(pid="p22", kind="sources", part="E", stage="do", title=u"Sources"),
]
# v38 (round 9, BRIEF G9-2, ADDENDUM §E / F2.4 / A9): pages 2-21 take their frames from R9_FRAMES (frames_r9 above,
# the one table of round 9; plan_findings/PAGE_TABLE.md). Each frame = F(ids, x, y, w, h, key=<R9 key>, kind, series,
# r8, bar=<R9 key>, and every option of its row: split, gap, cols, pt, merge, grid, card, over, allow, opt, rigid);
# F, C and T frames print no ratio (noscale); a frame with no ids (a bar slot: p06.2, p09.4, p21.4, p21.5) is opt.
# BK_R9_IDS: ids the round 9 producers export that the table has no row for (WaterBoard v20 handover: the p13 / p14
# key-map legends). BK_R9_SIDE: the frame where a page's unlisted items go (each one also a WARNING "unlisted").
# BK_R9_FIRST: frames placed before the others of their page (p03.2: the list p03.1 is tested against the axonometric).
BK_R9_IDS = {"p13.1": ("p15_keymap_legend",), "p14.5": ("p16_keymap_legend",)}
BK_R9_SIDE = {"p02": "p02.3", "p03": "p03.3", "p04": "p04.2", "p05": "p05.2", "p06": "p06.4", "p07": "p07.9",
              "p08": "p08.5", "p09": "p09.3", "p10": "p10.4", "p11": "p11.11", "p12": "p12.7", "p13": "p13.1",
              "p14": "p14.5", "p15": "p15.12", "p16": "p16.2", "p17": "p17.8", "p18": "p18.7", "p19": "p19.6",
              "p20": "p20.3", "p21": "p21.7"}
BK_R9_FIRST = {"p03": ("p03.2",)}
BK_R9_CLEAR = {"p03.1": "p03.2"}     # BRIEF §5 page 3: frame 1 must not touch frame 2's drawing, else it moves down


def bk_r9_frames(pid):
    """v38: the page's frames from R9_FRAMES in table order (BK_R9_FIRST first) -> [F(...)]"""
    out = []
    for key in sorted((k for k in R9_FRAMES if k.split(".")[0] == pid), key=_r9_order):
        r = dict(R9_FRAMES[key])
        x, y, w, h = r.pop("x"), r.pop("y"), r.pop("w"), r.pop("h")
        ids = tuple(r.pop("ids")) + tuple(BK_R9_IDS.get(key, ()))
        if r.get("kind") not in ("S", "M"):
            r.setdefault("noscale", True)
        if not ids:
            r["opt"] = True
        out.append(F(ids, x, y, w, h, key=key, **r))
    first = BK_R9_FIRST.get(pid) or ()
    out.sort(key=lambda f_: 0 if f_["key"] in first else 1)
    return out


for _sp in BK_PAGES:
    if _sp.get("kind") or not any(k_.split(".")[0] == _sp["pid"] for k_ in R9_FRAMES):
        continue
    _sp["frames"] = bk_r9_frames(_sp["pid"])
    _sp["side"] = BK_R9_SIDE.get(_sp["pid"])
    _sp["skip"] = tuple(_sp.get("skip") or ()) + tuple(R9_PAGE_SKIP.get(_sp["pid"], ()))
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
# Round 8 (v37, BRIEF §3 L1-L4, work order S6 §1): ABSOLUTE FRAMES + FIT. Every frame keeps its table box (the v35 flow
# and the dead v34 pack are deleted; no block's place depends on another, L1). Step 3 is now bk_fit: the frame's
# drawings (one, or a split row / col group as ONE group) get one uniform factor, the largest that fits the frame after
# head, subtitle, label band, level tags, scale band and the frame's own texts; printed scale (table den) kept within
# -6 % .. +6 % (true den = den / f; below = WARNING "<page> <drawing> fit true 1:<n> needed 1:<m>", overflow, nothing
# moves); no printed scale: free fit ("mm" at most x1.15). The scale bar is drawn at the TRUE scale, the printed ratio is
# the table's (bk_marks; frame option bar="<frame key>" puts bar / ratio / north at the bottom-left of that frame). An
# item a frame names is placed in that frame only (_bk_detach). Notes stack top-down in their frame, wrapped to its
# width; taller = WARNING "<page> <frame> textfit <mm>". After each page bk_bounds: every placed box vs x 14-406,
# y 26-279 = WARNING "<page> <block> offsheet <mm>"; page_boxes.csv. Frame option allow="<drawing id>" (or a tuple):
# the frame's texts may sit on that drawing's keep (a legend inside a map, L9). The v33 notes below are history.
# Round 7 (v33, BRIEF §3 L1-L3): a page is its FIXED FRAMES (80_plan: SON frames in mm + SON printed scales) + every
# item its scripts exported for it. NOTHING is fitted: step 3 below is now "scale = the table's den (m drawings) or
# factor f (mm drawings, default 1 = exported size); a drawing that does not fit its frame = WARNING "<pid> <did>
# frame", scale kept". The round 6 fitters (_bk_fit, _bk_same, _bk_justify, the frame clamp, extent-weighted cells)
# are deleted. Round 6 (PLAN §3, G6-1): a page is its FRAMES + every item its scripts exported for it. The v30 rows / right column / share are gone. Steps per page:
#   1. sort the page's items (bk_items) and attach every unanchored text, legend and list to one drawing (bk_attach:
#      its "drawing" key, else the longest drawing id its own id starts with, else the one drawing of its group)
#   2. match: each frame takes the items whose id matches one of its fnmatch patterns (first frame wins; drawings,
#      key maps, texts, legends, lists, photos alike)
#   3. scale (v33): every drawing at the page table's scale (den for maps / sections, f for diagrams, key maps at
#      their SON frame size), placed at its frame's top-left; heading, level column and the scale band ("1:den" +
#      north arrow, outside the drawing, G6-4) sit inside the frame; past the frame = WARNING, scale kept
#   4. draw: heading, drawing (30_render), north, level markers, labels (50_place), scale; then the drawing's attached
#      texts / legends / lists / side-list rows go to the frame's "note" frame, else under the drawing in its own frame,
#      else the page's "side" frame
#   5. every item no frame names and no drawing owns = WARNING "unlisted" and goes to the page's side frame (PLAN §2.2:
#      never lost); frames of one page that overlap = WARNING "frames"; an empty frame = WARNING "missing"
#   6. page number; layout check (70_check: overlaps, edges, empty bands, < 4 pt = one WARNING each, G6-7/G6-8); log
#      "page <pid> frames=<n> placed=<n> unlisted=<n>" and "groups <pid> kinds=<n> elements=<n> untagged=<n>" (G6-9)
# Nothing here raises on layout: every misfit is a WARNING (one run collects all; Aras 1 Nov 17:11).
BK_GAP = 2.0               # mm between cells / rows / right-column blocks (v38: the round 9 gutter, R9_GUTTER_MM)
BK_HEAD_H = 4.5            # heading band over a drawing
BK_SCALE_H = 5.5           # scale bar / "1:den" band under a true-scale drawing
BK_LEVEL_W = 24.0          # level markers + "+43.71 Q500" beside a section (3 gap + 9 marker + 12 label)
BK_NORTH_MM = 4.6          # v31: the north arrow sits in the scale band under the plan, right end (outside, G6-4)
BK_NOTE_GAP = 1.5          # mm between stacked notes / legends / lists
BK_RATIO_H = 3.4           # v37: band under a drawing that prints only its ratio (it carries its own bar geometry)
BK_FIT_LO, BK_FIT_HI = 0.94, 1.06   # v37 (L2, D5): true scale within -6 % .. +6 % of the printed one
BK_MM_HI = 1.15            # v37: a chart (C) / key map grows at most this much (v38: F frames have no cap, d5)
BK_T_HI = 1.0              # v38: a drawing in a T frame never grows (its texts are set at their print size)
BK_TXT_MIN = 4.0           # v38 (d5): WARNING "<page> <block> text<4pt" when a fit sets a drawing's text under this
BK_BAR_STEPS = (1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000)   # v38 (e1): scale bar lengths, m (25, 250 added)
BK_UNDER = 0.80            # v38 (G9-2): WARNING "<page> <block> underfill <used %>" under this share of the frame
BK_COVER = 0.85            # v38 (G9-2): WARNING "<page> cover <%>" under this share of the content area
BK_BOXES = []              # v37: page_boxes.csv rows (page, block, x, y, w, h, printed, true)


def _bk_own_bar(D):
    """v37: the drawing carries its own scale bar geometry (scale_note "own scale bar drawn as geometry ...")"""
    return u"own scale bar" in (u"%s" % (D.get("scale_note") or u""))


def _bk_pden(F, did, D):
    """v38 (d1): the PRINTED label (L of 1:L) of an "m" drawing = the label bk_fit / the series pre-pass computed for
    it (F["_lab"]), else the frame's den in the layout table, else None"""
    if not F or D.get("units", "m") != "m":
        return None
    lab = (F.get("_lab") or {}).get(did)
    if lab:
        return int(lab["L"])
    d_ = F.get("den")
    if isinstance(d_, dict):
        d_ = d_.get(did)
    return int(d_) if d_ else None


def _bk_sm(F):
    """v38: the frame is an S (scaled drawing) or M (map) frame of the round 9 table"""
    return (F or {}).get("kind") in ("S", "M")


def _bk_marks_of(D, F, pden):
    """v37: (north, bar, ratio) drawn for a drawing: north arrow (plans with north_deg, not key maps); a scale bar at the
    TRUE scale when the drawing has no bar of its own and asks for one (scale_bar) or has no printed scale; the PRINTED
    ratio (table value) unless the frame says noscale"""
    m = D.get("units", "m") == "m"
    north = D.get("north_deg") is not None and D.get("role") != "keymap"
    sm = _bk_sm(F)                                 # v38 (e1): S / M: the bar at the true scale + the label, always
    bar = m and not _bk_own_bar(D) and bool(D.get("scale_bar") or not pden or sm)
    ratio = m and bool(pden or sm) and not (F and F.get("noscale"))
    return north, bar, ratio


def _bk_band_h(D, F, pden):
    """v37: height of the band under a drawing: bar / north = BK_SCALE_H, ratio only = BK_RATIO_H, none = 0; 0 when the
    frame sends them to another frame (bar="<frame key>")"""
    if F and F.get("bar"):
        return 0.0
    north, bar, ratio = _bk_marks_of(D, F, pden)
    if north or bar:
        return BK_SCALE_H
    return BK_RATIO_H if ratio else 0.0


def _bk_pat(p):
    return any(c in p for c in "*?[")


def bk_items(pid):
    its = [it for it in ix_page(pid) if isinstance(it, dict)]
    S = dict(items=its, draw={}, keymaps=[], anchored=[], texts=[], legends=[], lists=[], levels=[], insets=[], photos=[],
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
        if k == "text" and isinstance(it.get("box"), dict):   # v37: a label box, drawn by bk_text_boxes
            BK_TEXT_BOX[it.get("id")] = it["box"]
        if k == "drawing":
            a_ = it.get("anchor")
            if it.get("role") == "keymap":
                S["keymaps"].append(it)
            elif it.get("outside") and isinstance(a_, dict) and a_.get("drawing"):
                S["anchored"].append(it)                  # v33: a key map's north (S1 km_export_items): with its map
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
    # v36 (8 Nov): a text exported by another script into a drawing's group (masterplan v44's sb_sec_note_<cut>_mp in
    # group sb_sec_<cut>) follows that drawing's own texts, whatever the folders' load order (stable sort)
    S["texts"].sort(key=lambda t: 0 if (S["draw"].get(t.get("group")) or {}).get("_folder", t.get("_folder")) ==
                    t.get("_folder") else 1)
    return S


def bk_attach(S):
    """who belongs to which drawing (see step 1); att[did] = dict(head=[texts], side=[items]); page-level in S["page"]"""
    ids = sorted(S["draw"], key=len, reverse=True)
    groups = {}
    for d in sorted(S["draw"].values(), key=lambda d: (d.get("priority", 5), d["id"])):
        groups.setdefault(d.get("group"), []).append(d["id"])
    att = dict((d, dict(head=[], side=[], levels=[], badge=None, sub=None)) for d in S["draw"])
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
        elif t.get("role") == "badge" and att[d]["badge"] is None and not t.get("at"):   # v32 box: the drawing's
            #                                                   number disc (v38: an anchored S1 badge never is)
            att[d]["badge"] = t
        elif t.get("role") == "caption" and t.get("priority", 5) <= 1 and att[d]["sub"] is None:
            att[d]["sub"] = t                                           # v32 box: the subtitle under the title
        elif t.get("role") == "heading" and not att[d]["head"]:
            att[d]["head"].append(t)
        else:
            att[d]["side"].append(t)
    strs = set(u"%s" % t.get("string", u"") for t in S["items"] if t.get("kind") == "text")
    for d, a in att.items():                         # v32 box: a title given only as ix.drawing(title=) heads its box
        tt = S["draw"][d].get("title")
        if not a["head"] and isinstance(tt, str) and tt.strip() and tt not in strs:
            a["head"].append(dict(kind="text", role="heading", string=tt, id=u"%s_title" % d, priority=1))
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


def _bk_k(D, s):
    """page mm per drawing unit at s (den for "m" drawings, factor for "mm")"""
    return (1000.0 / float(s)) if D.get("units", "m") == "m" else float(s)


def _bk_res(S, did, s=None, F=None):
    """(extra width, extra height) round a drawing: level tags (v37: one column, measured at s), heading, subtitle,
    label band, scale band (v37: _bk_band_h, none when the frame sends its bar to another frame, bar=)"""
    D = S["draw"][did]
    att = S["att"].get(did, {})
    rw = 0.0
    if att.get("levels"):
        if s is None:
            rw = BK_LEVEL_W
        else:
            k = _bk_k(D, s)
            rw = max(pl_levels_w(lc, k, float(D["extent"][3])) for lc in att["levels"])
    rh = _bk_band_h(D, F, _bk_pden(F, did, D))
    if s is not None:
        dw = sc_size(D, s)[0]
        rh += _bk_head_h(att, dw + rw) + (pl_band_need(D, _bk_k(D, s)) if _bk_is_band(D, F) else 0.0)
    else:
        rh += (BK_HEAD_H if att.get("head") or att.get("badge") else 0.0)
    return rw, rh


def _bk_is_band(D, F=None):
    """v32: a true-scale section sets its labels in a band above it (Aras's W1 box); v37: not in a frame with
    rigid=True (its labels stay where its script set them, at their point size: p13 seasons, r06_S03 "activity labels
    on the cut")"""
    return D.get("dkind") == "section" and D.get("units", "m") == "m" and not bk_design_den(D) and \
        not (F and F.get("rigid"))


def _bk_head_h(att, w):
    """v32 box head: number disc + title row, then the subtitle (wrapped to the box width)"""
    h = BK_HEAD_H if (att.get("head") or att.get("badge")) else 0.0
    if att.get("sub"):
        h += st_fit(att["sub"].get("string", u""), max(20.0, w), None, "caption")[3] + 1.0
    return h


def bk_disc(P, cx, cy, r, fill):
    import fitz as _fz
    sh = P.page.new_shape()
    sh.draw_circle(_fz.Point(cx * BK_K, cy * BK_K), r * BK_K)
    sh.finish(color=None, fill=hex_rgb(fill), width=0)
    sh.commit()


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


# ---- v38 (round 9 G9-1; PLAN §cause c1-c3, f2, f4): ONE centring path for every bubble, tag and card glyph -------
# bk_centre is the only function that sets a bubble / tag / tile glyph: the middle of the glyph's INK box on the disc
# or box centre ("MC" is ink-centred in fm_box and bk_emit, c2). S1 badges (INTERFACES §4: role "badge" + at, r_mm,
# fill, ring, ring_mm, text, pt, bold, colour) draw their disc here at PRINT size; their exported disc poly
# (badge_disc: true) is skipped by rd_items. Tags (role "tag" + box_mm, fill, ring, ring_mm) draw their box here.
BK_CENTRE = {}             # page -> glyphs set by bk_centre (log "centre <page> n=")
BK_DISC_SKIP = [0]         # badge disc polys left to bk_badges (rd_items), whole run
BK_TAG_PAD = (1.0, 0.6)    # mm round a tag's ink when its box_mm is None (x, y)


def bk_s1_badges(D):
    """the S1 badges of a drawing (role "badge" with r_mm and a point)"""
    return [dict(it, at=it.get("at") or _pl_apt(it)) for it in ix_texts(D)
            if it.get("role") == "badge" and it.get("r_mm") is not None and (it.get("at") or _pl_apt(it))]


def _bk_disc_has(s, ats):
    """True when one of the badge points lies inside the disc poly's box (drawing units)"""
    pts = [p for r in s.get("rings") or [] for p in r]
    if not pts:
        return False
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    e = 0.05 * max(x1 - x0, y1 - y0)
    return any(x0 - e <= float(a[0]) <= x1 + e and y0 - e <= float(a[1]) <= y1 + e for a in ats)


def bk_centre(P, s, cx, cy, pt, bold=True, colour=None, name=None, role="badge", allow=()):
    """G9-1 (c1, c2): THE centring function: the glyph(s) s with the middle of their INK box on (cx, cy) page mm (y
    down); fixed (the label pass never moves it); counted per page for "centre <page> n=" """
    BK_CENTRE[P.pid] = BK_CENTRE.get(P.pid, 0) + 1
    return P.tp.put(u"%s" % s, cx, cy, pt, bool(bold), "MC", 0.0, name, role, colour, tuple(allow) + ("marker",))


def bk_badge_disc(P, cx, cy, r, fill, ring=None, ring_mm=0.0, name=None):
    """an S1 badge's disc at print size: fill (None = none), ring stroke ring_mm wide (none when ring is None)"""
    import fitz as _fz
    sh = P.page.new_shape()
    sh.draw_circle(_fz.Point(cx * BK_K, cy * BK_K), r * BK_K)
    rw = float(ring_mm or 0.0) * BK_K if ring else 0.0
    sh.finish(color=hex_rgb(ring) if ring and rw > 0 else None, fill=hex_rgb(fill) if fill else None, width=rw)
    sh.commit()
    b = (cx - r, cy - r, cx + r, cy + r)
    P.tp.keep(b, "marker", name)
    P.ink.append(("marker", b, name))


def bk_badges(P, placed, s=1.0):
    """v38 (c1): every badge of a placed drawing, never moved, never shrunk. An S1 badge: its disc (fill, ring,
    ring_mm, r_mm) and glyph (pt, bold, colour) at PRINT size, the glyph centred by bk_centre; an older badge (its disc
    drawn in the drawing): its glyph at its first exported position, size x s ("=MC" through bk_centre). Each one is
    marked done in placed["_done"] (pl_rigid / pl_labels skip it)"""
    T, did = placed["T"], placed["id"]
    done = placed.setdefault("_done", set())
    for it in ix_texts(placed["D"]):
        if it.get("role") != "badge" or id(it) in done:
            continue
        a_ = it.get("at") or _pl_apt(it)
        if a_ is None:
            continue
        done.add(id(it))
        t = it.get("string") or it.get("text") or u""
        bold = bool(it.get("bold", True))
        cx, cy = T.pt(a_[0], a_[1])
        if it.get("r_mm") is not None:
            bk_badge_disc(P, cx, cy, float(it["r_mm"]), it.get("fill"), it.get("ring"), it.get("ring_mm"),
                          u"disc %s" % it.get("id"))
            pt = max(float(it.get("pt") or it.get("size_pt") or grid_role("badge")[0]), GRID_MIN_PT)
            bk_centre(P, t, cx, cy, pt, bold, it.get("colour"), it.get("id"), "badge", (did,))
            continue
        pt = max(float(it.get("size_pt") or grid_role("badge")[0]) * float(s), GRID_MIN_PT)
        c = _pl_codes(it.get("positions") or ["=C"])[0]
        if not isinstance(c, str):
            if abs(c[0]) < 1e-9 and abs(c[1]) < 1e-9 and u"%s" % c[2] in ("MC", "CM"):
                bk_centre(P, t, cx, cy, pt, bold, it.get("colour"), it.get("id"), "badge", (did,))
                continue
            c = (c[0] * s, c[1] * s, c[2])
        x, y, al = P.tp._at(c, t, (cx, cy), pt, bold, 0.0)
        P.tp.put(t, x, y, pt, bold, al, 0.0, it.get("id"), "badge", it.get("colour"), (did, "marker"))


def bk_tags(P, placed):
    """v38 (S1 tags: plates, K-tiles of the p09 cards, B19 callouts): every role "tag" text of a placed drawing: its
    box (box_mm, or the text's ink + BK_TAG_PAD) centred on its point, fill and ring (ring_mm; 0.3 pt when 0), the
    text by bk_centre; a text "<tag id>_sub" is the tag's second line, set under the box (its own positions, chain).
    Marks them done (placed["_done"])"""
    T, did = placed["T"], placed["id"]
    done = placed.setdefault("_done", set())
    its = ix_texts(placed["D"])
    subs = dict((u"%s" % t.get("id"), t) for t in its if (u"%s" % t.get("id", u"")).endswith(u"_sub"))
    for it in its:
        if it.get("role") != "tag" or id(it) in done:
            continue
        a_ = _pl_apt(it)
        t = it.get("string", u"")
        if a_ is None or not t:
            continue
        done.add(id(it))
        cx, cy = T.pt(a_[0], a_[1])
        pt = max(float(it.get("size_pt") or grid_role("label")[0]), GRID_MIN_PT)
        bold = bool(it.get("bold", True))
        bm = it.get("box_mm")
        if bm:
            w, h = float(bm[0]), float(bm[1])
        else:
            ix0, iy0, ix1, iy1 = fm_ink_box(t, pt, bold)
            w, h = (ix1 - ix0) + 2.0 * BK_TAG_PAD[0], (iy1 - iy0) + 2.0 * BK_TAG_PAD[1]
        box = (cx - w / 2.0, cy - h / 2.0, cx + w / 2.0, cy + h / 2.0)
        if it.get("fill") or it.get("ring"):
            rw = float(it.get("ring_mm") or 0.0) * BK_K
            bk_rect(P, box, it.get("fill"), it.get("ring"), rw if rw > 0 else 0.3)
        P.tp.keep(box, "marker", u"tag %s" % it.get("id"))
        P.ink.append(("tag", box, it.get("id")))
        bk_centre(P, t, cx, cy, pt, bold, it.get("colour"), it.get("id"), "tag", (did,))
        sb = subs.get(u"%s_sub" % it.get("id"))
        if sb is not None and id(sb) not in done and sb.get("string"):
            done.add(id(sb))
            fx = dict(anchor=(cx, cy), texts=[sb["string"]] + list(sb.get("short_forms") or []),
                      codes=_pl_codes(sb.get("positions") or ["S", "SE", "SW", "E", "W", "N"]),
                      pt=float(sb.get("size_pt") or grid_role("label")[0]),
                      lo=max(float(sb.get("min_pt") or GRID_MIN_PT), GRID_MIN_PT), bold=bool(sb.get("bold")),
                      colour=sb.get("colour"), role="label", name=sb.get("id"), allow=(did,),
                      win=placed["rect"], rect=placed["rect"], d=0.5 * h + 0.5, side_ok=False, owner=did)
            pl_chain(P, fx, None)


def bk_card(P, placed):
    """v38 (BRIEF §5 row 9, U17, PLAN f4; CityLink v13 Dc["card"]): a p09 hub card's box: the thin grey frame round the
    card (frame_colour, frame_pt), the bar across its top in the hub colour (bar_mm x the card's factor); the K-tile and
    the name are the card's own tag / heading texts (bk_tags, fixed texts)"""
    C = placed["D"].get("card") or {}
    r, T = placed["rect"], placed["T"]
    col = C.get("colour") or (hue_of(C.get("title"), None) if C.get("title") else None) or GRID_INK["accent"]
    bh = float(C.get("bar_mm") or 1.2) * T.k
    bk_rect(P, (r[0], r[1], r[2], r[1] + bh), col, None, 0)
    bk_rect(P, r, None, C.get("frame_colour") or GRID_INK["rule"], float(C.get("frame_pt") or 0.3))
    BK_PAGENO_LOG.append(u"card %s %s colour %s frame %.1fx%.1f mm" % (P.pid, placed["id"], col, r[2] - r[0],
                                                                      r[3] - r[1]))


def bk_design_den(D):
    """the scale a true-scale drawing's texts were designed at: "sheet scale 1:N" in its scale_note, else None"""
    import re as _re
    m_ = _re.search(r"sheet scale 1:([0-9][0-9,]*)", u"%s" % (D.get("scale_note") or u""))
    return int(m_.group(1).replace(",", "")) if m_ else None


def bk_place(P, S, did, s, x, y, side, F=None, pden=None, tden=None):
    """one cell at (x, y) top-left: heading, drawing, north, levels, labels, scale (see step 3) -> placed. v37: s = the
    TRUE scale (den, or the factor of an "mm" drawing) bk_fit chose; pden = the printed scale (table) or None; tden =
    the scale a board drawing's texts are sized for (pden, else the drawing's own scale): its texts keep the point
    size of that scale (L5), they are not scaled with the fit; F = its frame (bar=, noscale)"""
    D = S["draw"][did]
    att = S["att"].get(did, dict(head=[], side=[], levels=[]))
    rw, rh = _bk_res(S, did, s, F)
    dw, dh = sc_size(D, s)
    yy = y
    W = max(dw + rw, 30.0)
    if att["head"] or att.get("badge"):                # v32 box head (Aras's W1 box): disc, title
        hx = x
        if att.get("badge"):
            b_ = att["badge"]                          # v38 (f2): the disc in the badge's own / its hub's colour
            r_ = float(b_.get("r_mm") or 1.8)
            fill_ = b_.get("fill") or (D.get("card") or {}).get("colour") or GRID_INK["accent"]
            bk_disc(P, x + r_, y + r_ + 0.2, r_, fill_)
            P.tp.keep((x, y, x + 2 * r_, y + 2 * r_ + 0.4), "marker", u"disc %s" % did)
            bk_centre(P, b_.get("string") or b_.get("text") or u"", x + r_, y + r_ + 0.2,
                      float(b_.get("pt") or 5.0), b_.get("bold", True), b_.get("colour") or "FFFFFF", b_.get("id"))
            hx += 2 * r_ + 1.2
        if att["head"]:
            st_para(P, att["head"][0].get("string", u""), hx, y, W - (hx - x), BK_HEAD_H - 0.6, "heading",
                    justify=False, page=P.pid)
        yy += BK_HEAD_H
    if att.get("sub"):
        hh, _s2 = st_para(P, att["sub"].get("string", u""), x, yy, W, None, "caption", page=P.pid)
        yy += hh + 1.0
    if _bk_is_band(D, F):                              # the label band sits between the head and the drawing
        yy += pl_band_need(D, _bk_k(D, s))
    ox_, oy_ = D.get("_woff") or (0.0, 0.0)          # v38 (d4): a clamped map window keeps the focus centred
    T = BkT(D, s, x + ox_, yy + oy_)
    placed = rd_drawing(P, D, T)
    S["placed"][did] = placed
    placed["pden"] = pden
    if D.get("window_m"):                            # p09 windows: one size, framed (no frame in the drawing)
        bk_rect(P, T.rect, None, GRID_INK["ink"], 0.5)
    if not T.den:
        lo = (D.get("fit") or (0.5, 2.0))[0]
        if s < lo - 1e-3:
            wn_warn(P.pid, "scale", u"%s set at x%.2f, below its x%.2f minimum (row too full)" % (did, s, lo))
    for lc in att["levels"]:
        pl_levels(P, lc, placed, "R")
    dden = bk_design_den(D) or ((tden or T.den) if F and F.get("rigid") else None)   # v37: rigid= frame, labels as
    if D.get("card"):                               # v38 (f4): a p09 hub card's frame and bar under its texts
        bk_card(P, placed)
    bk_badges(P, placed, 1.0 if T.den else s)       # v38 (c1): S1 badges at print size, in every branch
    bk_tags(P, placed)                              # v38: tags, K-tiles, B19 callouts (+ their "_sub" lines)
    if T.den and dden:                              # a board drawing / rigid= frame keeps its own text layout;
        pl_rigid(P, placed, 1.0)                    # v38 (d2): its texts at their own print size (factor 1.0)
    elif T.den:
        if _bk_is_band(D, F):
            pl_band(P, placed)
        else:
            pl_labels(P, placed, side, roles=("label",))
    else:                                           # v30.3: diagrams keep their own text layout, scaled with them
        pl_rigid(P, placed, s, fixed=bool(D.get("card")))     # v38: card texts fixed where CityLink set them
    bk_marks(P, S, F, placed, pden)
    BK_STAT["drawings"] += 1
    BK_STAT["scales"].append(u"%s %s" % (did, (u"1:%d" % T.den) if T.den else (u"x%.2f" % T.k)))
    if F is not None:                               # v38: the placed box from the drawn rect (a clamped window)
        hd_ = bool(att["head"] or att.get("badge") or att.get("sub"))
        _bk_box(F, (x if hd_ else T.rect[0], y if hd_ else T.rect[1], max(T.rect[2] + rw, x + W if hd_ else 0.0),
                    T.rect[3] + _bk_band_h(D, F, pden)))
    return placed


def bk_marks(P, S, F, placed, pden):
    """v37 (round 8 L2, work order §1.3): north arrow, scale bar at the TRUE scale (T.k) and the PRINTED ratio (pden,
    the table's value) of one placed drawing (_bk_marks_of says which); in the band under the drawing, or at the
    bottom-left of the frame named by the drawing frame's bar="<frame key>" (north at that frame's right end)"""
    D, T, did = placed["D"], placed["T"], placed["id"]
    north, bar, ratio = _bk_marks_of(D, F, pden)
    if not (north or bar or ratio):
        return None
    bf = (S.get("fbykey") or {}).get(F.get("bar")) if F else None
    if F and F.get("bar") and bf is None:
        wn_warn(P.pid, u"%s bar" % did, u"bar=%r names no frame of the page: set under the drawing" % F.get("bar"))
    if bf is not None:
        b = bf["mm"]
        x0, x1 = b[0], b[2]
        band = BK_SCALE_H if (north or bar) else BK_RATIO_H
        top = b[3] - band if b[3] - b[1] >= band - 1e-6 else b[1] - 1.2   # v38 (d10): a bar frame lower than the
        #                                                    band (p09.4 3 mm): the bar starts at the frame's top
    else:
        x0, x1, top = T.rect[0], T.rect[2], T.rect[3]
    if north:
        bk_north(P, (x0, top - 1.0, x1, top), D["north_deg"], did)
        if bf is not None:                           # v38: the bar frame's used box (page_boxes.csv, underfill)
            _bk_box(bf, (x1 - BK_NORTH_MM - 6.0, top, x1, top + BK_SCALE_H))
    if bar:
        bx = pl_scalebar(P, placed, x0, top + 1.2, printed=pden if ratio else None)
        if bf is not None and bx:
            _bk_box(bf, bx)
        return bx
    if ratio and pden:
        pt = grid_role("caption")[0]
        a_, _d = fm_asc_desc(pt)
        bx = P.tp.put(u"1:{:,}".format(int(pden)), x0, top + 1.2 + a_, pt, False, "L", 0.0, None, "scale",
                      GRID_INK["ink"], (), "sb_%s" % did)
        if bf is not None and bx:
            _bk_box(bf, bx)
        return bx
    return None


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
def bk_side_item(P, it, x, y, w, ybot, allow=(), cols=None, pt=None):
    """one attached thing in its frame at (x, y), wrapped to the width w at its own point size: returns the height
    used. v37: no per-text overrun warning (the frame's "textfit" WARNING in _bk_put); allow = keeps it may sit on.
    v38: cols = a legend's columns (frame cols=, exactly that many); pt = the frame's point size (frame pt=)"""
    h = max(4.0, ybot - y)
    k = it.get("kind")
    if k == "text":
        role = it.get("role") or "note"
        if role not in GRID_ROLE_PT:
            role = "note"
        if pt:
            hh, _s = st_para(P, it.get("string", u""), x, y, w, None, role, float(pt), justify=role != "heading",
                             page=P.pid, allow=allow)
        else:
            hh, _s = st_para(P, it.get("string", u""), x, y, w, None, role, justify=role != "heading", page=P.pid,
                             allow=allow)
        return hh
    if k == "legend":
        b = pl_legend(P, it, x, y, w, h, int(cols) if cols else 2, allow=allow, warn=False, pt=pt, fixed=bool(cols))
        return b[3] - b[1]
    if k == "list":
        b = pl_list(P, it, x, y, w, None, allow=allow, pt=pt)
        return b[3] - b[1]
    return 0.0


# ---- the page -----------------------------------------------------------------------------------------------------
BK_STAT = dict(drawings=0, scales=[], pages=[])




# ---- frames (v31, G6-1) -------------------------------------------------------------------------------------------
def _bk_frames(spec, pid):
    """v33 / v37: the page plan's frames as given in mm (the table box, never moved, clamped or grown) -> [dict(key,
    pats, mm, opts)]; log "frame <pid> <key> x,y,w,h" per frame (= the table box)"""
    out = []
    ml, mt, mr, mb = GRID_ML, GRID_MT, GRID_PAGE[0] - GRID_MR, GRID_PAGE[1] - GRID_MB
    for f in spec.get("frames") or []:
        pats = [f["ids"]] if isinstance(f["ids"], str) else list(f["ids"])
        m_ = tuple(f["mm"])
        F_ = dict(f, pats=pats, key=f.get("key") or pats[0], mm=m_, mm0=m_)
        out.append(F_)
        BK_PAGENO_LOG.append(u"frame %s %s %.1f,%.1f,%.1f,%.1f" % (pid, F_["key"], m_[0], m_[1], m_[2] - m_[0],
                                                                    m_[3] - m_[1]))
    # v37: every frame keeps this table box (no flow, L1); the logged box is the one used
    return out


def _bk_pool(S):
    """every placeable item of the page, in export order: (id, kind, item); kind drawing | keymap | text | legend |
    list | photo"""
    out = [(d, "drawing", S["draw"][d]) for d in sorted(S["draw"], key=lambda d: (S["draw"][d].get("priority", 5), d))]
    out += [(k.get("id"), "keymap", k) for k in S["keymaps"]]
    heads = set(id(h) for a in S["att"].values() for h in a["head"] + [a.get("badge"), a.get("sub")] if h)
    out += [(t.get("id"), "text", t) for t in S["texts"] if t is not S.get("intro") and id(t) not in heads]
    out += [(it.get("id"), k, it) for k in ("legend", "list", "photo") for it in S[k + "s"]]
    return out


def _bk_match(S, frames, skip=()):
    """each frame's items in pattern order (first frame wins); returns the set of matched item object ids. v33: ids
    matching a page's skip pattern (SON has no block for them, D4 / F12) are left out with a log line "skip <page> <kind> <id>" """
    pool = _bk_pool(S)
    got = set()
    for iid, k, it in pool:
        if iid is not None and any(fnmatch.fnmatchcase(iid, p) for p in skip):
            got.add(id(it))
            BK_PAGENO_LOG.append(u"skip %s %s %s (SON has no block for it)" % (S.get("pid", u"?"), k, iid))
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


def _bk_den(S, F, did, D, pid, quiet=False):
    """v33 (L1): the ONE scale of a drawing, read, never picked: "m" drawings -> the frame's den (int, or dict id ->
    den), else the producer's single fixed scale (scale_pref of one value, then its "sheet scale 1:N", then board_den /
    scale_den), each logged with its source; "mm" drawings -> the frame's factor f (1.0 = the exported size)"""
    if D.get("units", "m") != "m":
        return float(F.get("f") or 1.0), u"size"
    d_ = F.get("den")
    if isinstance(d_, dict):
        d_ = d_.get(did)
    if d_:
        return int(d_), u"table"
    sp = [int(v) for v in (D.get("scale_pref") or [])]
    if len(sp) == 1:
        return sp[0], u"script"
    for k_, v_ in ((u"sheet", bk_design_den(D)), (u"board", D.get("board_den")), (u"script", D.get("scale_den"))):
        if v_:
            return int(v_), k_
    if quiet:
        return 1000, u"none"
    wn_warn(pid, u"%s scale" % did, u"no SON scale in the page table and no fixed scale from its script%s: set at "
            u"1:1,000 (put its SON scale in 80_plan)" % ((u" (it offers 1:%s)" % u", 1:".join(str(v) for v in sp))
                                                       if sp else u""))
    return 1000, u"none"


class _BkTgt(object):
    """a place where notes stack: a box and its running y"""
    def __init__(self, key, box, y=None, F=None):
        self.key, self.box, self.y, self.over = key, box, box[1] if y is None else y, False
        self.F = F                                   # v37: its frame (page_boxes.csv box, allow=)
        a_ = (F or {}).get("allow") or ()
        self.allow = (a_,) if isinstance(a_, str) else tuple(a_)


BK_FLOW_COL = 64.0                 # v32.4: a notes frame at least 2 x this wide flows its notes in columns


def _bk_est_h(P, it, w):
    """a quick height estimate of one note at width w (only to choose where a column breaks)"""
    k = it.get("kind")
    if k == "legend":
        n_ = len(it.get("entries") or [])
        cols = max(1, min(2, int((w + 4.0) // 40.0) or 1))
        return 1.3 * (PL_SW["h"] + PL_SW["row_gap"] + 0.6) * (-(-n_ // cols)) + (5.0 if it.get("title") else 0.0)
    if k == "list":
        return 3.4 * len(it.get("items") or [])
    if k == "text":
        role = it.get("role") or "note"
        try:
            return st_fit(it.get("string", u""), w, None, role if role in GRID_ROLE_PT else "note", page=P.pid)[3]
        except Exception:
            return 6.0
    return 0.0


def _bk_put(P, tg, it):
    """one text / legend / list at the target's running y, wrapped to the frame's width at its own point size; v37:
    past the frame's foot = one WARNING "<page> <frame> textfit <mm>" per frame (never shrunk, nothing moves).
    v32.4: in a frame at least 2 x BK_FLOW_COL wide the notes flow in columns (top to bottom, then the next column),
    so a stack of legends no longer runs past the page foot while the frame's width stays empty (p21)"""
    x0, _y0, x1, y1 = tg.box
    Fo = getattr(tg, "F", None) or {}
    nc = int((x1 - x0 + 4.0) // BK_FLOW_COL) if it.get("kind") != "photo" else 1
    if Fo.get("cols"):                             # v38: a frame with cols= (p02.3, p20.3): its legends span the
        nc = int(getattr(tg, "force_nc", 1) or 1)  # frame in exactly that many columns, the rest full width
        #                                            (merge=: its lists flow in cols columns first, bk_merge)
    if it.get("kind") == "legend" and not getattr(tg, "col", 0) and (x1 - x0) > 4.0 * max(1.0, y1 - _y0):
        nc = 1                                     # v32.6: a legend in a band frame (4 x wider than tall) takes the
    if nc >= 2:                                    # frame's width in its own columns (in one 64 mm column it ran
        #                                            28 mm past the p19 foot)
        cw = (x1 - x0 - 4.0 * (nc - 1)) / float(nc)
        c = getattr(tg, "col", 0)
        top = getattr(tg, "ctop", tg.y)
        tg.ctop = top
        if c < nc - 1 and tg.y > top + 1e-6 and tg.y + _bk_est_h(P, it, cw) > y1 + 0.5:
            c += 1
            tg.y = top
        tg.col = c
        x0 = x0 + c * (cw + 4.0)
        x1 = x0 + cw
    y_at = tg.y
    n0, k0 = len(P.tp.items), len(P.tp.keeps)
    if it.get("kind") == "photo":
        hh = _bk_photo_grid(P, [it], (x0, tg.y, x1, y1), Fo.get("grid"))
    else:
        hh = bk_side_item(P, it, x0, tg.y, x1 - x0, y1, getattr(tg, "allow", ()), Fo.get("cols"), Fo.get("pt"))
    tg.y += hh + BK_NOTE_GAP
    tg.cbot = max(getattr(tg, "cbot", tg.y), tg.y)     # v38: the lowest column foot (bk_merge)
    ink = [t_["box"] for t_ in P.tp.items[n0:]] + [k_["box"] for k_ in P.tp.keeps[k0:] if k_.get("kind") == "swatch"]
    if ink and it.get("kind") != "photo":          # v38 (d9): a text block's used box = its ink, not the frame width
        _bk_box(getattr(tg, "F", None), (min(b[0] for b in ink), min(b[1] for b in ink), max(b[2] for b in ink),
                                         max(b[3] for b in ink)))
    else:
        _bk_box(getattr(tg, "F", None), (x0, y_at, x1, y_at + hh))
    over = y_at + hh - y1
    if over > 0.5:
        tg.over = max(float(tg.over or 0.0), over)     # v37: the frame's textfit WARNING once, after the page (_bk_compose)
    return hh


def _bk_photo_grid(P, photos, box, grid=None):
    """photos in a grid filling the box (proportions kept, never stretched; v38: each centre-cropped to its cell);
    captions under each; grid = (cols, rows) from the frame (p06.6 4 x 2); -> height used"""
    if not photos:
        return 0.0
    import math as _m
    x0, y0, x1, y1 = box
    w, h = x1 - x0, max(8.0, y1 - y0)
    n = len(photos)
    cols = max(1, min(n, int(round(_m.sqrt(n * w / h))) or 1))
    if grid and int(grid[0]) >= 1:
        cols = max(1, min(n, int(grid[0])))
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


def _bk_anchored(P, S, did, T):
    """v33 (S1 §4): a key map's north arrow ("<id>.north", outside=True) at its anchor = its lower-left in the key
    map's mm (y up), at size 1; its "<id>.head" text is placed with the key map (pl_rigid, anchor point)"""
    for N in S["anchored"]:
        a_ = N.get("anchor") or {}
        if a_.get("drawing") != did or not a_.get("point"):
            continue
        px, py = T.pt(a_["point"][0], a_["point"][1])
        nh = float(N["extent"][3]) - float(N["extent"][1])
        TN = BkT(N, 1.0, px, py - nh)
        pn = rd_drawing(P, N, TN)
        pl_rigid(P, pn, 1.0)
        S["placed"][N["id"]] = pn
        S["done_anch"].add(id(N))


def _bk_box(F, b):
    """v37: grows the frame's placed-content box (page_boxes.csv) by b"""
    if F is None or b is None:
        return
    o = F.get("_box")
    F["_box"] = tuple(b) if o is None else (min(o[0], b[0]), min(o[1], b[1]), max(o[2], b[2]), max(o[3], b[3]))


def _bk_focus(D):
    """v38 (d4): an M map's focus box (x0, y0, x1, y1, drawing metres) when it exports a usable one, else None"""
    f_ = D.get("focus")
    try:
        f_ = [float(v) for v in f_]
    except Exception:
        return None
    if len(f_) != 4 or f_[2] - f_[0] <= 1e-6 or f_[3] - f_[1] <= 1e-6:
        return None
    return tuple(f_)


def bk_label(D, Tfit, r8=None):
    """v38 (ADDENDUM §0, d1): the printed label and true scale of one S drawing / M map: the producer's own (den or
    rec_den = its true scale, label_den = its label) when that drawing still fits the frame (T >= Tfit), so a producer
    that laid its labels out at T is placed 1:1; else r9_label(Tfit, r8). -> dict(L, T, list, size, small, src)"""
    pT = D.get("den") or D.get("rec_den")
    pL = D.get("label_den")
    try:
        pT, pL = float(pT), int(pL)
    except Exception:
        pT = pL = None
    if pT and pL and pT >= float(Tfit) * 0.999:
        return dict(L=pL, T=pT, list=u"%s" % (D.get("scale_list") or u"round"), size=float(Tfit) / pT, small=False,
                    src=u"script")
    lab = r9_label(Tfit, r8)
    lab["src"] = u"booklet"
    return lab


def _bk_min_pt(D):
    """v38: the smallest point size of a drawing's own texts (badges and tags excluded), None without texts"""
    pts = [float(t.get("size_pt") or grid_role(t.get("role", "label"))[0]) for t in ix_texts(D)
           if t.get("role") not in ("badge", "tag") and t.get("string")]
    return min(pts) if pts else None


def bk_fit(P, S, F, ds, pid, quiet=False):
    """v38 (round 9 G9-2, ADDENDUM §0, PLAN d1, d4, d5): ONE uniform factor f for the frame's drawings (one drawing, or
    a split row / col group fitted as one) = the largest at which they fit the frame after the room their head,
    subtitle, label band, level tags and scale band take and the frame's own texts under them (f_fit). Then by kind:
    S / M ("m" drawings): Tfit = base / f_fit (an M map measures its FOCUS box, not its exported window); its label and
    true scale = the series' (pre-pass, S["lab"]) or bk_label (the producer's T when it fits, else r9_label with the
    frame's r8; a layout-table den = a fixed label); the bar is drawn at T, the label L is printed. F: f = f_fit, no cap
    (WARNING "text<4pt" when its texts would go under 4 pt); C and key maps: f at most BK_MM_HI; T: f at most 1.0.
    quiet=True: measure only (the pre-pass): -> {did: Tfit} of the frame's "m" drawings.
    -> {did: (s_true, s_base, label or None)}; F["_lab"][did] = the label dict; F["_avail"] = (w, h) the drawings get"""
    x0, y0, x1, y1 = F["mm"]
    kind = F.get("kind")
    sp = F.get("split") or "row"
    gap = float(F.get("gap", BK_GAP))
    base = []
    for did, kk, it in ds:
        if kk == "keymap":
            base.append((did, it, 1.0, True, it))
        else:
            D = S["draw"][did]
            s0, _src = _bk_den(S, F, did, D, pid, quiet=True)
            Dm = D
            if kind == "M" and D.get("units", "m") == "m" and _bk_focus(D):
                Dm = dict(D, extent=list(_bk_focus(D)))      # v38 (d4): the map is fitted by its focus box
            base.append((did, D, float(s0), False, Dm))
    tx = [it for _i, kk, it in F["items"] if kk in ("text", "legend", "list")]
    if not F.get("note"):                          # v37 table pass: attached notes no frame names stack under their
        fr_ = S.get("framed") or set()             # drawing in this frame (_bk_compose): their room is kept too
        for did, kk, _it in ds:
            if kk != "keymap":
                tx += [it for it in S["att"].get(did, {}).get("side", []) if id(it) not in fr_]
    tw_ = x1 - x0
    th = sum(_bk_est_h(P, it, tw_) + BK_NOTE_GAP for it in tx)
    W, H = x1 - x0, y1 - y0 - th
    F["_avail"] = (W, H)
    n = len(base)

    def at(f):
        out = []
        for did, D, s0, km, Dm in base:
            s = (s0 / f) if D.get("units", "m") == "m" else s0 * f
            dw, dh = sc_size(Dm, s)
            rw, rh = (0.0, 0.0) if km else _bk_res(S, did, s, F)
            out.append((dw / f, dh / f, rw, rh))         # natural size (f = 1) and the reserves at f
        return out
    f = 1.0
    for _i in range(5):
        L = at(f)
        if sp == "col":
            fw = min([(W - rw) / dw for dw, dh, rw, rh in L if dw > 1e-6] or [1.0])
            sh = sum(dh for dw, dh, rw, rh in L)
            fh = ((H - sum(rh for _a, _b, _c, rh in L) - gap * (n - 1)) / sh) if sh > 1e-6 else 1.0
        else:
            sw = sum(dw for dw, dh, rw, rh in L)
            fw = ((W - sum(rw for _a, _b, rw, _d in L) - gap * (n - 1)) / sw) if sw > 1e-6 else 1.0
            fh = min([(H - rh) / dh for dw, dh, rw, rh in L if dh > 1e-6] or [1.0])
        nf = max(0.05, min(fw, fh))
        done = abs(nf - f) < 1e-4
        f = nf
        if done:
            break
    f_fit = f
    if quiet:
        return dict((did, s0 / f_fit) for did, D, s0, km, Dm in base if not km and D.get("units", "m") == "m")
    if kind == "F":
        f = f_fit                                        # v38 (d5): F uniform, the largest that fits
    elif kind == "T":
        f = min(BK_T_HI, f_fit)
    else:
        f = min(BK_MM_HI, f_fit)
    out = {}
    labs = F.setdefault("_lab", {})
    for did, D, s0, km, Dm in base:
        if km:
            out[did] = (s0 * f, s0, None)
            continue
        if D.get("units", "m") == "m":
            Tfit = s0 / f_fit
            if _bk_sm(F):
                d_ = F.get("den")
                d_ = d_.get(did) if isinstance(d_, dict) else d_
                if d_:                                   # a layout-table den: Aras's fixed label (bar still at T)
                    lab = dict(L=int(d_), T=max(Tfit, float(d_)), list=u"table", size=Tfit / max(Tfit, float(d_)),
                               small=False, src=u"table")
                else:
                    lab = (S.get("lab") or {}).get(did)        # the pre-pass (series share one T and label)
                    lab = dict(lab, size=Tfit / float(lab["T"])) if lab else bk_label(D, Tfit, F.get("r8"))
                labs[did] = dict(lab, Tfit=Tfit)
                blk = F["key"] if len(base) == 1 else u"%s/%s" % (F["key"], did)
                BK_PAGENO_LOG.append(r9_scale_line(pid, blk, Tfit, lab)[0] + u" (%s)" % lab.get("src", u"booklet"))
                if lab.get("small"):
                    bk_warn(pid, blk, u"scale small")
                out[did] = (int(round(lab["T"])), s0, int(lab["L"]))
            else:                                        # an "m" drawing in an F / C / T frame: free fit, no label
                st = int(round(s0 / f))
                BK_PAGENO_LOG.append(u"scale %s %s true 1:%d (no label: %s frame)" % (pid, F["key"], st, kind))
                out[did] = (st, s0, None)
        else:
            mp_ = _bk_min_pt(D)
            if f < 1.0 - 1e-6 and mp_ is not None and mp_ * f < BK_TXT_MIN - 1e-6:
                bk_warn(pid, F["key"], u"text<4pt %s x%.2f sets %.1f pt text at %.1f pt" % (did, f, mp_, mp_ * f))
            out[did] = (s0 * f, s0, None)
    return out


def bk_window(S, F, did, T, pid):
    """v38 (PLAN d4, ADDENDUM §0): an M map is drawn through a window = the frame's room for it (F["_avail"] less its
    reserves) at its true scale T, centred on its focus, clamped to its exported extent (never stretched, never past
    the data); the clamped part keeps the focus centred (_woff). S["draw"][did] becomes the windowed copy (extent =
    window, _window); its texts outside the window are left out and counted (log "window <page> <block> ...")"""
    D = S["draw"][did]
    fo = _bk_focus(D)
    if fo is None or D.get("units", "m") != "m":
        BK_PAGENO_LOG.append(u"window %s %s %s: no focus exported, the whole extent drawn" % (pid, F["key"], did))
        return D
    W, H = F.get("_avail") or (F["mm"][2] - F["mm"][0], F["mm"][3] - F["mm"][1])
    rw, rh = _bk_res(S, did, T, F)
    wm, hm = max(1.0, W - rw) * float(T) / 1000.0, max(1.0, H - rh) * float(T) / 1000.0
    cx, cy = 0.5 * (fo[0] + fo[2]), 0.5 * (fo[1] + fo[3])
    full = (cx - wm / 2.0, cy - hm / 2.0, cx + wm / 2.0, cy + hm / 2.0)
    e = [float(v) for v in D["extent"]]
    win = (max(full[0], e[0]), max(full[1], e[1]), min(full[2], e[2]), min(full[3], e[3]))
    if win[2] - win[0] <= 1e-6 or win[3] - win[1] <= 1e-6:
        bk_warn(pid, F["key"], u"window %s: the frame at 1:%d misses the exported extent, the extent drawn" % (did, T))
        return D
    k = 1000.0 / float(T)
    out = [t for t in ix_texts(D) if not _bk_in_win(t, win)]
    D2 = dict(D, extent=list(win), _window=win, _woff=((win[0] - full[0]) * k, (full[3] - win[3]) * k),
              _wmm=(max(1.0, W - rw), max(1.0, H - rh)))
    S["draw"][did] = D2
    ends = u"".join(c_ for c_, hit in ((u"w", e[0] > full[0] + 1e-3), (u"e", e[2] < full[2] - 1e-3),
                                         (u"s", e[1] > full[1] + 1e-3), (u"n", e[3] < full[3] - 1e-3)) if hit)
    nm = [u"%s" % (t.get("string") or u"")[:24] for t in out if t.get("role", "label") == "label"][:6]
    BK_PAGENO_LOG.append(u"window %s %s %s 1:%d %.0f,%.0f,%.0f,%.0f m (%.0f x %.0f m)%s; texts outside left out n=%d%s" % (
        pid, F["key"], did, int(round(T)), win[0], win[1], win[2], win[3], win[2] - win[0], win[3] - win[1],
        (u", the exported extent ends on side %s" % ends) if ends else u"", len(out),
        (u" (%s)" % u"; ".join(nm)) if nm else u""))
    return D2

BK_SCALE_TOK = re.compile(r"\{scale:([^}]+)\}")
BK_LABELS = {}             # v38: drawing id -> its printed label, every page composed so far ({scale:<id>} tokens)


def bk_prepass(P, S, frames, pid):
    """v38 (ADDENDUM §0.6, PLAN d1, e2): before anything is placed: every S / M drawing's Tfit (bk_fit quiet); ONE
    label for each series (the members' common producer T when it fits them all, else r9_series_label over the
    members' Tfit and r8), the others by bk_label -> S["lab"][did]; log "series <page> <name> ..."; then the
    "{scale:<id>}" tokens of the page's texts become "1:L" (bk_tokens)"""
    S["lab"] = {}
    ser = {}
    for F in frames:
        if not _bk_sm(F) or F.get("den"):
            continue
        ds = [(iid, kk, it) for iid, kk, it in F["items"] if kk == "drawing"]
        if not ds:
            continue
        for did, Tfit in bk_fit(P, S, F, ds, pid, quiet=True).items():
            if F.get("series"):
                ser.setdefault(F["series"], []).append((did, Tfit, F.get("r8")))
            else:
                S["lab"][did] = bk_label(S["draw"][did], Tfit, F.get("r8"))
    for name, mem in sorted(ser.items()):
        Ds = [S["draw"][d] for d, _t, _r in mem]
        tmax = max(t for _d, t, _r in mem)
        lab = None
        if len(set((D.get("den") or D.get("rec_den"), D.get("label_den")) for D in Ds)) == 1:
            lab = bk_label(Ds[0], tmax)
            if lab.get("src") != u"script":
                lab = None
        if lab is None:
            lab = r9_series_label([t for _d, t, _r in mem], [r for _d, _t, r in mem])
            lab["src"] = u"booklet"
        lab["series"] = name
        for d, _t, _r in mem:
            S["lab"][d] = lab
        BK_PAGENO_LOG.append(u"series %s %s n=%d fit 1:%d true 1:%d label 1:%d list %s (%s)" % (
            pid, name, len(mem), int(round(tmax)), int(round(lab["T"])), lab["L"], lab["list"], lab["src"]))
    bk_tokens(S, pid)


def _bk_tok_sub(txt, labs, pid, where):
    """v38 (e2): every "{scale:<id>}" of txt -> "1:L" (the label of drawing <id>: this page, an earlier page, or the
    label_den it exported); an unknown one is left out with a WARNING"""
    def rep(m_):
        did = m_.group(1).strip()
        L = labs.get(did) or BK_LABELS.get(did)
        if L is None:
            L = (ix_get(did) or {}).get("label_den")
        if L is None:
            bk_warn(pid, did, u"scale token in %s: no label known for it, left out" % where)
            return u""
        return u"1:{:,}".format(int(L))
    return BK_SCALE_TOK.sub(rep, txt)


def bk_tokens(S, pid):
    """v38 (e2): the page's "{scale:<id>}" tokens (texts, legend titles and entries, list rows, photo captions,
    drawing titles) replaced after the pre-pass; log "tokens <page> scale n=" """
    labs = dict((d, int(l["L"])) for d, l in (S.get("lab") or {}).items())
    BK_LABELS.update(labs)
    n = [0]

    def sub(v, where):
        if isinstance(v, str) and u"{scale:" in v:
            n[0] += 1
            return _bk_tok_sub(v, labs, pid, where)
        return v

    def fix(d_, key, where):                       # only a value that holds a token is rewritten
        v = d_.get(key)
        if isinstance(v, str) and u"{scale:" in v:
            d_[key] = sub(v, where)
    for it in S["items"]:
        k, iid = it.get("kind"), it.get("id")
        if k == "text":
            fix(it, "string", iid)
            if it.get("short_forms"):
                it["short_forms"] = [sub(t, iid) for t in it["short_forms"]]
        elif k == "legend":
            fix(it, "title", iid)
            for e_ in it.get("entries") or []:
                fix(e_, "text", iid)
        elif k == "list" and it.get("items"):
            it["items"] = [sub(t, iid) for t in it["items"]]
        elif k == "photo":
            fix(it, "caption", iid)
        elif k == "drawing":
            fix(it, "title", iid)
    if n[0]:
        BK_PAGENO_LOG.append(u"tokens %s scale n=%d" % (pid, n[0]))


def _bk_frame_draw(P, S, F, same, tg_of, pid):
    """v37: the drawings of one frame, FITTED into it (bk_fit: one uniform factor for one drawing or a split "row" |
    "col" group, F gap apart), top-left aligned unless the frame says al=; the frame never moves or grows (L1); logs
    "size <pid> <did> x<f>" and "keymap <pid> module" (v38: the "scale ..." line comes from bk_fit; M maps go through
    bk_window first); returns ([did], bottom)"""
    ds = [(iid, kk, it) for iid, kk, it in F["items"] if kk in ("drawing", "keymap")]
    out, bottom = [], F["mm"][1]
    if not ds:
        return out, bottom
    al = (F.get("al") or "TL").upper()
    x0, y0, x1, y1 = F["mm"]
    sp = F.get("split") or "row"
    gap = float(F.get("gap", BK_GAP))
    fit = bk_fit(P, S, F, ds, pid)
    if F.get("kind") == "M":                         # v38 (d4): each map through its window (the frame at T)
        for did, kk, it in ds:
            if kk == "drawing":
                bk_window(S, F, did, fit[did][0], pid)
    sizes = []
    for did, kk, it in ds:
        s = fit[did][0]
        if kk == "keymap":
            dw, dh = sc_size(it, s)
            sizes.append((dw, dh))
        else:
            rw, rh = _bk_res(S, did, s, F)
            dw, dh = S["draw"][did].get("_wmm") or sc_size(S["draw"][did], s)   # v38: a map's whole window
            sizes.append((dw + rw, dh + rh))
    if sp == "col":
        gw, gh = max(w for w, h in sizes), sum(h for w, h in sizes) + gap * (len(sizes) - 1)
    else:
        gw, gh = sum(w for w, h in sizes) + gap * (len(sizes) - 1), max(h for w, h in sizes)
    cx = x0 + {"C": (x1 - x0 - gw) / 2.0, "R": x1 - x0 - gw}.get(al[1:2], 0.0)
    cy = y0 + {"M": (y1 - y0 - gh) / 2.0, "B": y1 - y0 - gh}.get(al[:1], 0.0)
    for (did, kk, it), (tw, th) in zip(ds, sizes):
        s, s0, pden = fit[did]
        if kk == "keymap":                           # G7-3: the one key-map module, fitted (L8), texts with it
            T = BkT(it, s, cx, cy)
            pl = pl_mm_drawing(P, it, T)
            S["placed"][did] = pl
            _bk_anchored(P, S, did, T)
            BK_STAT["drawings"] += 1
            BK_PAGENO_LOG.append(u"keymap %s module %s %.1fx%.1f mm at %.1f,%.1f" % (pid, did, tw, th, cx, cy))
            BK_PAGENO_LOG.append(u"size %s %s x%.2f" % (pid, did, s))
            _bk_box(F, pl["rect"])
            S.setdefault("rec", {})[did] = dict(F=F, mm=F["mm"], s=s, printed=None, rect=tuple(pl["rect"]))
        else:
            D = S["draw"][did]
            side = TpSideList(u"%s %s" % (pid, did))
            if F.get("noscale"):                     # SON prints no ratio here / the drawing's own bar is its scale
                S.setdefault("noscale", set()).add(did)
            pl = bk_place(P, S, did, s, cx, cy, side, F=F, pden=pden, tden=pden or s0)
            if pl["T"].den:                          # v38: the "scale ..." line is written by bk_fit (ADDENDUM §0.9)
                pass
            else:
                BK_PAGENO_LOG.append(u"size %s %s x%.2f %.1fx%.1f mm" % (pid, did, pl["T"].k, pl["T"].w, pl["T"].h))
            S.setdefault("rec", {})[did] = dict(F=F, mm=F["mm"], s=s, printed=pden, rect=tuple(pl["rect"]))
            if side.entries:                       # labels that fell back to numbers: their rows with the notes
                tg = tg_of(F, did)
                tg.y += pl_side_rows(P, side, tg.box[0], tg.y, tg.box[2] - tg.box[0], max(4.0, tg.box[3] - tg.y)) + \
                    BK_NOTE_GAP
        bottom = max(bottom, cy + th)
        out.append(did)
        if sp == "col":
            cy += th + gap
        else:
            cx += tw + gap
    return out, bottom


def bk_check_page(P, S, frames, pid, before):
    """v37 invariants, log only: every placed drawing prints its table scale (true scale within the fit band, bk_fit),
    its frame unchanged, its rect not moved by the label pass (L6); one line "check <pid> drawings=<n> scale_ok=<n>
    frames_ok=<n> moved=<n>" """
    n = ok_s = ok_f = mv = 0
    for did, r in (S.get("rec") or {}).items():
        n += 1
        F = r["F"]
        D = S["draw"].get(did)
        want = _bk_pden(F, did, D) if D else None
        if r.get("printed") == want:
            ok_s += 1
        else:
            wn_warn(pid, u"%s scale" % did, u"printed %s, table %s" % (r.get("printed"), want))
        if tuple(F["mm"]) == tuple(r["mm"]):
            ok_f += 1
        else:
            wn_warn(pid, u"%s frame" % did, u"frame changed %s -> %s" % (r["mm"], F["mm"]))
        if before.get(did) != r["rect"]:
            mv += 1
            wn_warn(pid, u"%s moved" % did, u"the drawing moved during the label pass (L6)")
    BK_PAGENO_LOG.append(u"check %s drawings=%d scale_ok=%d frames_ok=%d moved=%d" % (pid, n, ok_s, ok_f, mv))


# ---- v32 labels (L1, LAYOUT_PLAN_booklet_places_all.md §3.2; Aras 4 Nov 19:17-19:25): after placing, the collision
# test runs and every text that hits something is placed again by the chain (bk_fix -> pl_chain: free spot round its
# point, short form, OUTSIDE the drawing with a leader line, number + key row). NO drawing is scaled down and NO text
# is shrunk to clear a hit; only hits left after that are WARNINGs, the texts printed. (v33: the round 6 page
# justification and scale picking that stood here are deleted, BRIEF L3.)


def bk_fix(P, rounds=3):
    """v32: the texts that hit something run the chain again (pl_chain; the later / movable one of each pair moves);
    returns the hits left"""
    for _r in range(rounds):
        if bk_late():                                     # v32.4: past the page budget, no more fix rounds
            break
        hits = P.tp.hits_now(True)
        movers, seen = [], set()
        for _k, a, b in hits:
            for t in ((b, a) if isinstance(b, dict) and "text" in b else (a,)):
                if isinstance(t, dict) and "text" in t and (t.get("extra") or {}).get("fx") and id(t) not in seen:
                    seen.add(id(t))
                    movers.append(t)
                    break
        if not movers:
            return hits
        for t in movers:
            fx = t["extra"]["fx"]
            if fx.get("tries", 0) >= 3:
                continue
            fx["tries"] = fx.get("tries", 0) + 1
            if P.tp.unput(t):
                pl_unleader(P, fx)
                pl_chain(P, fx, P.fx_side, first=False)
    return P.tp.hits_now(True)


def bk_own_hits(P):
    """v32.4: overlaps left INSIDE one drawing after the booklet moved what it could within that drawing (texts its
    script exported on top of each other): one WARNING per drawing naming the script, with the first pairs, so the
    rest is fixed where it is made (the page test also lists each pair)"""
    tp = P.tp
    by = {}
    for n, it in enumerate(tp.items):
        ex = it.get("extra") or {}
        g = u"%s" % (ex.get("dgrp") or (ex.get("fx") or {}).get("dgrp") or u"")
        if g.startswith(u"drw:"):
            by.setdefault(g[4:], []).append(it)
    for did, its in by.items():
        pairs = []
        for i, a in enumerate(its):
            for c in its[i + 1:]:
                if tp_hit(a["box"], c["box"], 0.0) and a.get("text") != c.get("text"):
                    pairs.append((a["text"], c["text"]))
        if pairs:
            sc_ = (BK_IX_OWNER.get(did) if "BK_IX_OWNER" in globals() else None) or did.split(u"_")[0]
            wn_warn(P.pid, "own", u"%s: %d text pairs still on top of each other inside it (its script %s set them so), e.g. %s"
                    % (did, len(pairs), sc_, u"; ".join(u"%r / %r" % (a[:30], b[:30]) for a, b in pairs[:3])))


BK_BOUNDS = (14.0, 26.0, 406.0, 279.0)      # v37 (L3): content area x 14-406, y 26-279 (title band, footer exempt)


def bk_bounds(P):
    """v37 (round 8 BRIEF L3): every placed box of the page (drawings, texts, legends, lists, key maps, photos, level
    tags, scale bars) except the title band and footer (BK_BAND_ROLES) against BK_BOUNDS: one WARNING "<page> <block>
    offsheet <mm outside>" per block (its farthest box); nothing is moved or cut. Returns the number of blocks"""
    x0, y0, x1, y1 = BK_BOUNDS
    worst = {}

    def chk(name, b):
        o = max(x0 - b[0], b[2] - x1, y0 - b[1], b[3] - y1)
        if o > 0.05:
            worst[name] = max(worst.get(name, 0.0), o)
    for it in P.tp.items:
        if it.get("role") in BK_BAND_ROLES:
            continue
        chk(u"%s" % (it.get("name") or u"text %r" % it.get("text", u"")[:24]), it["box"])
    for B in P.tp.blocks:
        chk(u"%s" % B.get("name"), B["box"])
    for k_, b, nm in P.ink:
        chk(u"%s" % (nm or k_), b)
    for name, o in sorted(worst.items()):
        bk_warn(P.pid, name, u"offsheet %.1f" % o)
    return len(worst)


def bk_content_page(doc, spec, n, lines):
    """one content page from its frames (see the part notes): compose, fix every hit by moving texts, check"""
    pid = spec["pid"]
    R = _bk_compose(doc, spec, n)
    P, S = R["P"], R["S"]
    st = pl_stat(P)
    bk_bounds(P)                                          # v37 (L3): every placed box inside x 14-406, y 26-279
    bk_own_hits(P)                                        # v32.4: texts a script set on top of each other
    ck_page(P)                                            # the final test: every hit left = one WARNING line
    bk_cover_check(P)                                         # v38 (G9-2): WARNING "<page> cover <%>" under 85 %
    bk_finish(P)
    g = BK_GRP.get(pid, dict(kinds=set(), elements=set(), untagged=0))
    lines.append(u"page %s frames=%d placed=%d unlisted=%d (attached notes %d)" % (pid, len(R["frames"]),
                                                                                R["placed"], R["unl"], R["att"]))
    lines.append(u"layout %s drawings %d, labels %d (moved %d, short %d, leader %d, numbered %d), drawings made "
                 u"smaller 0, hits left %d (frames grown %d)" % (
                     pid, len(S["placed"]), st["labels"], st["moved"], st["short"], st["leader"], st["numbered"],
                     len(R["left"]), R["grown"]))
    if BK_PG["late"]:
        wn_warn(pid, "time", u"page past its %.0f s budget: %d texts set at their own spot without the search "
                u"(%.0f s)" % (BK_PAGE_BUDGET, BK_PG["late"], time.time() - BK_PG["t0"]))
    if "wp_groups_log" in globals():                # S2's writer counts what it actually wrote
        lines.append(wp_groups_log(pid))
    else:
        lines.append(u"groups %s kinds=%d elements=%d untagged=%d" % (pid, len(g["kinds"]), len(g["elements"]),
                                                                    g["untagged"]))
    lines.append(u"page %d %s: drawings %s" % (
        n, pid, u", ".join(u"%s %s" % (d, (u"1:%d" % p_["T"].den) if p_["T"].den else (u"x%.2f" % p_["T"].k))
                           for d, p_ in S["placed"].items())))
    return P


def _bk_compose(doc, spec, n):
    """one content page (see the part notes); returns dict(P, S, frames, left hits, counts)"""
    pid = spec["pid"]
    S = bk_items(pid)
    S["placed"], S["pid"] = {}, pid
    bk_attach(S)
    P = bk_page(doc, pid, n)
    P.fx_side = TpSideList(u"%s page key" % pid)
    pl_stat(P)
    kick = bk_kicker(spec)
    intro = spec.get("intro")
    if S["intro"]:                                        # v37 (R7 p15): an exported intro that repeats the kicker is
        if _bk_is_kicker(S["intro"], kick):               # not the lead: the page's own lead is used
            BK_PAGENO_LOG.append(u"lead %s: exported %s repeats the kicker, page lead used" % (pid, S["intro"].get("id")))
        else:
            intro = S["intro"].get("string")
    rule_y = bk_band(P, kick, spec["title"], intro)
    frames = _bk_frames(spec, pid)
    S["done_anch"] = set()                                # a key map's north is placed with its key map
    S["fbykey"] = dict((F["key"], F) for F in frames)     # v37: bar="<frame key>"
    n_det = _bk_detach(S, frames)                         # v37: an item a frame names is placed in that frame only
    if n_det:
        BK_PAGENO_LOG.append(u"attach %s: %d item(s) a frame names taken off their drawing's head / side" % (pid, n_det))
    framed = _bk_match(S, frames, spec.get("skip") or ())
    S["framed"] = framed                                  # v37: bk_fit keeps room for attached notes no frame names
    bk_prepass(P, S, frames, pid)                         # v38 (d1, e2): labels, series, {scale:<id>} tokens
    grown = 0                                             # v37: frames never move or grow (L1); no flow
    same = {}
    tg = {}
    for F in frames:
        tg[F["key"]] = _BkTgt(F["key"], F["mm"], F=F)
    side_key = spec.get("side")
    if side_key not in tg:
        wn_warn(pid, "frames", u"the page plan names no side frame (%r): unlisted items go under the last frame"
                % side_key)
        side_key = frames[-1]["key"] if frames else None
    if side_key is None:
        tg[None] = _BkTgt(None, GRID_AREA)

    def tg_of(F, did=None):
        """where a drawing's numbered-label rows go: its frame's "note" frame, else under it in its own frame, else
        the side"""
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
            if not F.get("opt"):                          # v38: WARNING "<page> <block> empty"
                bk_warn(pid, F["key"], u"empty (nothing exported for %s: its script not run, or the id changed)"
                        % u", ".join(F["pats"]))
            continue
        if F["key"] in BK_R9_CLEAR:                       # v38 (BRIEF §5 page 3): clear of the axonometric
            bk_clear(P, S, F, S["fbykey"].get(BK_R9_CLEAR[F["key"]]), pid, tg)
        ds, bottom = _bk_frame_draw(P, S, F, same, tg_of, pid)
        for d in ds:
            owner_f[d] = F
        if ds:
            tg[F["key"]].y = bottom + BK_NOTE_GAP
        photos = [it for _i, kk, it in F["items"] if kk == "photo"]
        if photos:
            t = tg[F["key"]]
            ph_h = _bk_photo_grid(P, photos, (t.box[0], t.y, t.box[2], t.box[3]), F.get("grid"))
            _bk_box(F, (t.box[0], t.y, t.box[2], t.y + ph_h))
            t.y += ph_h + BK_NOTE_GAP
        if F.get("merge"):                                # v38 (A9): p21.7 one shared legend, lists first
            bk_merge_put(P, tg[F["key"]], F, pid)
        else:
            for _i, kk, it in F["items"]:
                if kk in ("text", "legend", "list"):
                    _bk_put(P, tg[F["key"]], it)
        n_placed += len(F["items"])
    bk_insets(P, S)
    # a placed drawing's attached items that no frame names: its frame's "note" frame, else under it in its own frame
    # only if they fit there (v37), else the page's side frame with WARNING "<page> <id> unlisted"
    n_att = 0
    for did, F in owner_f.items():
        for it in S["att"].get(did, {}).get("side", []):
            if id(it) not in framed:
                framed.add(id(it))
                t = tg.get(F.get("note"))
                if t is None:
                    t = tg[F["key"]]
                    if t.y + _bk_est_h(P, it, t.box[2] - t.box[0]) > t.box[3] + 0.5:
                        bk_warn(pid, it.get("id"), u"unlisted (no room under its drawing %s: set in the side frame %s)"
                                % (did, side_key))
                        t = tg[side_key]
                _bk_put(P, t, it)
                n_att += 1
    # everything else: unlisted -> the side frame, WARNING (never lost)
    unl = [(iid, kk, it) for iid, kk, it in _bk_pool(S) if id(it) not in framed]
    for iid, kk, it in sorted(unl, key=lambda r: u"%s" % r[0]):
        bk_warn(pid, iid, u"unlisted (%s in no frame of the page plan: set in the side frame %s)" % (kk, side_key))
        t = tg[side_key]
        if kk in ("drawing", "keymap"):
            Fx = dict(key=u"side %s" % iid, mm=(t.box[0], t.y, t.box[2], max(t.y + 10.0, t.box[3])),
                      items=[(iid, kk, it)])
            _ds, bottom = _bk_frame_draw(P, S, Fx, {}, lambda F_, d_=None: t, pid)
            t.y = bottom + BK_NOTE_GAP
            if t.y > t.box[3] + 0.5:
                bk_warn(pid, iid, u"fit side frame %s: runs %.1f mm past its foot" % (side_key, t.y - t.box[3]))
        else:
            _bk_put(P, t, it)
    bk_pageno(P, n, bk_footer(spec))
    before = dict((d, r["rect"]) for d, r in (S.get("rec") or {}).items())
    left = bk_fix(P)
    if P.fx_side.entries:                                 # texts the fix pass numbered: their key rows in the side frame
        t = tg[side_key]
        t.y += pl_side_rows(P, P.fx_side, t.box[0], t.y, t.box[2] - t.box[0], max(4.0, t.box[3] - t.y)) + BK_NOTE_GAP
        left = P.tp.hits_now(True)
    pl_draw_leaders(P)
    for d, pl_ in S["placed"].items():                    # the label pass never moves a drawing (L6)
        r_ = (S.get("rec") or {}).get(d)
        if r_ is not None:
            r_["rect"] = tuple(pl_["rect"])
    for it in S["anchored"]:
        if id(it) not in S["done_anch"]:
            wn_warn(pid, u"%s anchor" % it.get("id"), u"its key map %r is not on this page: not placed"
                    % (it.get("anchor") or {}).get("drawing"))
    for k_, t in sorted(tg.items(), key=lambda kv: u"%s" % kv[0]):    # v37 (L2): text taller than its frame, once
        if t.over:
            bk_warn(pid, k_, u"textfit %.1f" % float(t.over))
    bk_check_page(P, S, frames, pid, before)
    for F in frames:                                      # v37: page_boxes.csv, one row per frame (placed content)
        recs = [(d, r) for d, r in (S.get("rec") or {}).items() if r["F"] is F]
        pr = u"|".join((u"1:%d" % r["printed"]) if r.get("printed") else u"" for _d, r in recs).strip(u"|")
        tr = u"|".join((u"1:%d" % S["placed"][d]["T"].den) if S["placed"][d]["T"].den else
                       (u"x%.2f" % S["placed"][d]["T"].k) for d, _r in recs if d in S["placed"])
        used = bk_used(F)                                 # v38 (G9-2): the share of the frame its content uses
        if F["items"] and F["pats"] and used < BK_UNDER:
            bk_warn(pid, F["key"], u"underfill %d %%" % int(round(100.0 * used)))
        BK_BOXES.append((pid, F["key"], F.get("_box"), pr, tr, used))
    BK_PAGENO_LOG.append(u"centre %s n=%d" % (pid, BK_CENTRE.get(pid, 0)))
    return dict(P=P, S=S, frames=frames, left=left, placed=n_placed, unl=len(unl), att=n_att, grown=grown)


def bk_used(F):
    """v38 (G9-2, d9): the share (0-1) of the frame's area its placed content uses (the placed box inside the frame)"""
    b, m = F.get("_box"), F["mm"]
    A = max(1e-6, (m[2] - m[0]) * (m[3] - m[1]))
    if not b:
        return 0.0
    w = min(b[2], m[2]) - max(b[0], m[0])
    h = min(b[3], m[3]) - max(b[1], m[1])
    return max(0.0, w) * max(0.0, h) / A


def bk_cover_check(P):
    """v38 (G9-2): the share of the content area (BK_BOUNDS) the page's placed boxes cover (texts except the title
    band and footer, blocks, drawings, legends, photos, bars), on the 1 mm grid of the checks; WARNING "<page> cover <%>"
    under BK_COVER; returns the share"""
    inn = BK_BOUNDS
    cols, rows = int((inn[2] - inn[0]) / CK_CELL), int((inn[3] - inn[1]) / CK_CELL)
    G = bytearray(cols * rows)
    for it in P.tp.items:
        if it.get("role") not in BK_BAND_ROLES:
            _ck_mark(G, cols, rows, inn, it["box"])
    for B in P.tp.blocks:
        _ck_mark(G, cols, rows, inn, B["box"])
    for _k, b, _n in P.ink:
        _ck_mark(G, cols, rows, inn, b)
    c = sum(G) / float(cols * rows) if cols and rows else 0.0
    BK_PAGENO_LOG.append(u"cover %s %d %%" % (P.pid, int(round(100.0 * c))))
    if c < BK_COVER:
        bk_warn(P.pid, u"cover", u"%d %%" % int(round(100.0 * c)))
    return c


def bk_merge_put(P, tg, F, pid):
    """v38 (A9, MasterPlan v47 handover): a merge=True frame (p21.7) sets ONE legend: the numbered lists and texts
    first, flowing in the frame's cols columns, then every legend entry once (same text, swatch kind and colour = one
    entry) across the frame in cols columns, all at the frame's pt; past the foot = the frame's textfit WARNING"""
    its = [(kk, it) for _i, kk, it in F["items"] if kk in ("text", "legend", "list")]
    legs = [it for kk, it in its if kk == "legend"]
    first = [it for kk, it in its if kk == "list"] + [it for kk, it in its if kk == "text"]
    seen, ents = set(), []
    for lg in legs:
        for e in lg.get("entries") or []:
            sw = e.get("swatch") or {}
            t = ix_text(e.get("text"), lg.get("_folder"))
            k_ = (t, sw.get("kind"), sw.get("colour") or sw.get("fill"), u"%s" % sw.get("badge"),
                  u"%s" % (sw.get("tag") or {}).get("text"))
            if k_ in seen:
                continue
            seen.add(k_)
            ents.append(dict(e, text=t))
    cols = int(F.get("cols") or 1)
    tg.force_nc = cols
    for it in first:
        _bk_put(P, tg, it)
    if ents:
        tg.force_nc = 1
        tg.y = max(tg.y, getattr(tg, "cbot", tg.y))
        tg.col, tg.ctop = 0, tg.y
        _bk_put(P, tg, dict(kind="legend", id=u"%s_legend" % F["key"], entries=ents, title=None,
                            _folder=legs[0].get("_folder")))
    BK_PAGENO_LOG.append(u"merge %s %s legends=%d entries=%d (repeats left out %d) lists/texts=%d cols=%d pt=%s" % (
        pid, F["key"], len(legs), len(ents), sum(len(l_.get("entries") or []) for l_ in legs) - len(ents),
        len(first), cols, F.get("pt") or u"own"))


def bk_clear(P, S, F, G, pid, tg):
    """v38 (BRIEF §5 page 3): frame F sits in frame G's corner where G's drawing leaves the box empty: when a point of
    G's drawn geometry lies inside F's box: WARNING "<page> <F> overlap" and F moves down the right edge in 2 mm steps
    (never past G's foot) to the first place clear of it (log "frame <page> <F> moved ...")"""
    if not G:
        return
    pts = []
    for d, r in (S.get("rec") or {}).items():
        if r["F"] is not G or d not in S["placed"]:
            continue
        pl = S["placed"][d]
        T, R = pl["T"], pl["rect"]
        for L in pl["D"].get("layers") or []:
            for sh in L.get("shapes") or []:
                for ring in list(sh.get("rings") or []) + ([sh["pts"]] if sh.get("pts") else []):
                    for q in ring:
                        x_, y_ = T.pt(q[0], q[1])
                        if R[0] <= x_ <= R[2] and R[1] <= y_ <= R[3]:
                            pts.append((x_, y_))
    if not pts:
        return
    x0, y0, x1, y1 = F["mm"]
    h = y1 - y0

    def hit(a, b):
        return any(x0 - 0.5 <= p_[0] <= x1 + 0.5 and a - 0.5 <= p_[1] <= b + 0.5 for p_ in pts)
    if not hit(y0, y1):
        BK_PAGENO_LOG.append(u"clear %s %s: clear of the %s drawing" % (pid, F["key"], G["key"]))
        return
    bk_warn(pid, F["key"], u"overlap the %s drawing reaches its corner" % G["key"])
    y = y0
    while y + 2.0 + h <= G["mm"][3] + 1e-6:
        y += 2.0
        if not hit(y, y + h):
            F["mm"] = (x0, y, x1, y + h)
            tg[F["key"]] = _BkTgt(F["key"], F["mm"], F=F)
            BK_PAGENO_LOG.append(u"frame %s %s moved %.1f,%.1f,%.1f,%.1f (clear of the %s drawing)" % (
                pid, F["key"], x0, y, x1 - x0, h, G["key"]))
            return
    bk_warn(pid, F["key"], u"overlap no clear place down the right edge of %s: kept at its table box" % G["key"])


def _bk_is_kicker(it, kick):
    """v37 (R7 p15): True when an exported intro repeats the page's kicker (id ending "_kicker", or the same text
    ignoring case, spaces and ·)"""
    if (u"%s" % it.get("id", u"")).endswith(u"_kicker"):
        return True
    norm = lambda t: u"".join(c for c in (u"%s" % (t or u"")).casefold() if not c.isspace() and c not in u"·•")
    return bool(kick) and norm(grid_plain(it.get("string", u""))) == norm(kick)


def _bk_frame_of(frames, iid):
    """v37: the first frame of the page whose patterns name iid (the same order as _bk_match), or None"""
    if iid is None:
        return None
    for F in frames:
        for p in F["pats"]:
            if (fnmatch.fnmatchcase(iid, p) if _bk_pat(p) else iid == p):
                return F
    return None


def _bk_detach(S, frames):
    """v37 (round 8 work order §1.4; R7 p20: mp_plan_caption became mp_plan_r1's subtitle, mp_plan_moves_head its
    head): an exported item a frame pattern of the page names is placed in THAT frame only. When that frame is not
    the frame of the drawing it is attached to, it is taken off the drawing's head / subtitle / badge / side list (so
    the frame match takes it); an item named by its own drawing's frame keeps its head / subtitle place in that frame.
    Returns the number taken off."""
    own = set(id(t) for t in S["texts"]) | set(id(t) for k_ in ("legends", "lists") for t in S[k_])
    n = 0
    for did, a in S["att"].items():
        fd = _bk_frame_of(frames, did)

        def off(it):
            if it is None or id(it) not in own:
                return False
            fi = _bk_frame_of(frames, it.get("id"))
            return fi is not None and fi is not fd
        keep_h = [h for h in a["head"] if not off(h)]
        n += len(a["head"]) - len(keep_h)
        a["head"] = keep_h
        for k_ in ("sub", "badge"):
            if off(a.get(k_)):
                a[k_] = None
                n += 1
        keep_s = [it for it in a["side"] if not off(it)]
        n += len(a["side"]) - len(keep_s)
        a["side"] = keep_s
    return n
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
    f = BK_CONTENTS_F                     # v33 (L3): a fixed row step (was fitted to the column)
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
    # v32: justified, last line left (Aras 4 Nov 19:22); v32.4: the "[3] + 0.9" had slipped into this comment
    return st_fit(body, cw - (BK_SRC_IND if m_ else 0.0), None, "source", s, justify=True, page="sources")[3] + 0.9


BK_CONTENTS_F = 1.25        # v33: contents row step x this (SON page1: CONTENTS y 15 -> "Sources" y 262.7 mm, H4 §5;
#                             22 rows at the steps below = ~1.25); past y 276 = WARNING "overrun"


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
    def _cols(nc):                              # v32.4: the columns span the page's own margins (14 mm, grid.py);
        g_ = 4.0                                # the fixed % columns began at 12.6 mm, inside the left margin
        w_ = (GRID_PAGE[0] - GRID_ML - GRID_MR - g_ * (nc - 1)) / float(nc)
        return [(GRID_ML + i_ * (w_ + g_), w_) for i_ in range(nc)]
    for ncol, lo in ((4, BK_SRC_PT[1]), (5, GRID_MIN_PT)):
        cw = _cols(ncol)[0][1]
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
    cols = _cols(ncol)
    sp_ = next((x_ for x_ in BK_PAGES if x_.get("pid") == pid), dict(part=part, stage="do"))
    label, foot = bk_kicker(sp_), bk_footer(sp_)          # v33 (L4): kicker "· PART" and the footer label
    pages, P, col, y = [], None, 0, y0
    for (k, t), hh in zip(flat, hs):
        if P is None or y + hh > y1 + 1e-6:
            if P is not None:
                col += 1
                y = y0
            if P is None or col >= ncol:
                if P is not None:
                    bk_pageno(P, n + len(pages) - 1, foot)
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
                st_para(P, t[m_.end():], cx + BK_SRC_IND, y, cw - BK_SRC_IND, None, "source", s, justify=True,
                        page=pid)
            else:
                st_para(P, t, cx, y, cw, None, "source", s, justify=True, page=pid)
        y += hh
    if P is not None:
        bk_pageno(P, n + len(pages) - 1, foot)
        ck_page(P)
        bk_finish(P)
    if len(pages) > 1:
        wn_warn(pid, "overrun", u"the sources need %d pages at %.2f pt in %d columns (the booklet has %d + %d)" % (
            len(pages), s, ncol, n, len(pages) - 1))
    lines.append(u"sources page: %d rows at %.2f pt, %d columns, %d page(s)" % (len(flat), s, ncol, len(pages)))
    return len(pages)
# ---- 84_table (v35 layout table; v37 round 8: the v35 automatic flow is DELETED, BRIEF L1 "absolute frames").
# 1. LAYOUT TABLE  ~/Downloads/Bergama/Data/booklet_layout.csv (written from parts/80_plan.py on the first run; then
#    YOURS: edit it in Excel, save as CSV, press the Button). One row per frame:
#      page_order;page;block;x_mm;y_mm;w_mm;h_mm;scale;size;on;plan
#    page_order = where the page sits in the booklet (sort key; the cover stays first, Sources last);
#    block = the frame key (80_plan); x, y, w, h = the frame on the A3 sheet in mm (origin top left);
#    scale = 1:n PRINTED for its true-scale drawings (n only; "id=n;id=n" for a frame holding several, written as
#    id=n|id=n); size = kept for reading (v37: every diagram / chart / key map is fitted to its frame, at most x1.15,
#    bk_fit); on = 0 leaves the frame's items out; plan = the booklet version that wrote the row (BK_TABLE_VERSION).
#    A row whose page / block the plan does not know = WARNING (ignored). Numbers: whole mm, "." or "," both read.
# 2. v37 VERSION STAMP: a table whose rows do not all say plan = BK_TABLE_VERSION was written by an older booklet (its
#    frames are the old plan): it is renamed booklet_layout_<its plan or v36>_<yyyymmdd_hhmm>.csv in the same folder
#    (kept for reference) and the v37 plan is written fresh under the same name (the read list does not change).
# 3. NO FLOW (v37): every frame keeps its table box; no block moves, grows or is pushed by another (L1).
BK_TABLE = os.path.join(BERGAMA_ROOT, "Data", "booklet_layout.csv")
BK_TABLE_COLS = ["page_order", "page", "block", "x_mm", "y_mm", "w_mm", "h_mm", "scale", "size", "on", "plan"]
BK_TABLE_VERSION = "v38"         # v37: the plan column every written row carries (a table without it is an old plan);
#                                  v38: the round 9 frames (R9_FRAMES), so a v37 table is kept aside and written fresh


def _bk_fkey(f):
    ids = f.get("ids")
    return f.get("key") or (ids if isinstance(ids, str) else list(ids)[0])


def _bk_num(s):
    s = (u"%s" % s).strip().replace(u",", u".")
    return float(s) if s else None


def _bk_table_write(path):
    rows = []
    for i, sp in enumerate(BK_PAGES, 1):
        if sp.get("kind") or not sp.get("frames"):
            continue
        for f in sp["frames"]:
            m = f["mm"]
            d = f.get("den")
            sc = u"|".join(u"%s=%d" % kv for kv in sorted(d.items())) if isinstance(d, dict) else (u"%d" % d if d else u"")
            rows.append([u"%d" % i, sp["pid"], _bk_fkey(f), u"%.1f" % m[0], u"%.1f" % m[1],     # v38 (d7): 0.1 mm
                         u"%.1f" % (m[2] - m[0]), u"%.1f" % (m[3] - m[1]), sc,
                         (u"%g" % f.get("f", 1.0)) if not d else u"", u"1", BK_TABLE_VERSION])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as fh:
        fh.write(u"sep=;\r\n")                      # Excel opens it in columns in any language setting
        fh.write(u";".join(BK_TABLE_COLS) + u"\r\n")
        for r in rows:
            fh.write(u";".join(r) + u"\r\n")
    return len(rows)


def _bk_table_read(path):
    with open(path, "r", encoding="utf-8-sig") as fh:
        raw = [ln.rstrip(u"\r\n") for ln in fh if ln.strip()]
    if raw and raw[0].lower().startswith(u"sep="):
        raw = raw[1:]
    if not raw:
        return []
    sep = u";" if raw[0].count(u";") >= raw[0].count(u",") else u","
    head = [h.strip().lower() for h in raw[0].split(sep)]
    out = []
    for ln in raw[1:]:
        cells = [c.strip().strip(u'"') for c in ln.split(sep)]
        out.append(dict(zip(head, cells + [u""] * (len(head) - len(cells)))))
    return out


def bk_table_apply(lines):
    """read (or first write) the layout table and apply it to BK_PAGES: page order, frame mm, scale, size, on/off"""
    if not os.path.isfile(BK_TABLE):
        n = _bk_table_write(BK_TABLE)
        lines.append(u"layout table written from the built-in plan: %d frames -> %s (edit it, press the Button)"
                     % (n, BK_TABLE))
        return
    try:
        rows = _bk_table_read(BK_TABLE)
    except Exception as ex:
        wn_warn(None, "table", u"layout table not read (%s: %s): the built-in plan is used" % (type(ex).__name__, ex))
        return
    if not rows or any((r.get("plan") or u"").strip() != BK_TABLE_VERSION for r in rows):
        olds = sorted(set((r.get("plan") or u"").strip() for r in rows) - set([u"", BK_TABLE_VERSION]))
        old = u"_".join(olds) if olds else u"v36"          # v37: a table from an older booklet: kept, plan written fresh
        kept = os.path.join(os.path.dirname(BK_TABLE), u"booklet_layout_%s_%s.csv" % (old, time.strftime("%Y%m%d_%H%M")))
        try:
            os.replace(BK_TABLE, kept)
        except Exception as ex:
            wn_warn(None, "table", u"older layout table %s not renamed (%s: %s): the built-in %s plan is used" % (
                BK_TABLE, type(ex).__name__, ex, BK_TABLE_VERSION))
            return
        n = _bk_table_write(BK_TABLE)
        lines.append(u"layout table from %s kept as %s; the %s plan written fresh: %d frames -> %s" % (
            old, kept, BK_TABLE_VERSION, n, BK_TABLE))
        return
    bypid = dict((sp["pid"], sp) for sp in BK_PAGES if sp.get("pid"))
    order, used = {}, 0
    for r in rows:
        pid, key = r.get("page", u""), r.get("block", u"")
        sp = bypid.get(pid)
        if sp is None or sp.get("kind"):
            wn_warn(None, "table", u"layout table row %s / %s: no such content page (ignored)" % (pid, key))
            continue
        try:
            po = _bk_num(r.get("page_order", u""))
            if po is not None:
                order[pid] = min(order.get(pid, po), po)
            f = next((f for f in sp.get("frames") or [] if _bk_fkey(f) == key), None)
            if f is None:
                wn_warn(pid, "table", u"layout table block %r is not a frame of %s (ignored)" % (key, pid))
                continue
            x, y, w, h = [_bk_num(r.get(c, u"")) for c in ("x_mm", "y_mm", "w_mm", "h_mm")]
            if None not in (x, y, w, h) and w > 0 and h > 0:
                f["mm"] = (x, y, x + w, y + h)
            sc = (r.get("scale") or u"").strip()
            if u"=" in sc:
                f["den"] = dict((a.strip(), int(round(_bk_num(b)))) for a, b in
                                (p.split(u"=", 1) for p in sc.replace(u";", u"|").split(u"|") if u"=" in p))
            elif sc:
                f["den"] = int(round(_bk_num(sc.replace(u"1:", u""))))
            sz = _bk_num(r.get("size", u""))
            if sz:
                f["f"] = sz
            if (r.get("on") or u"1").strip() in (u"0", u"no", u"off"):
                sp["skip"] = list(sp.get("skip") or []) + [p for p in ([f["ids"]] if isinstance(f["ids"], str)
                                                                        else list(f["ids"]))]
                f["ids"], f["opt"] = (u"__off__%s" % key,), True
            used += 1
        except Exception as ex:
            wn_warn(pid, "table", u"layout table row %s / %s not read (%s: %s)" % (pid, key, type(ex).__name__, ex))
    if order:
        idx = dict((id(sp), i) for i, sp in enumerate(BK_PAGES))
        last = len(BK_PAGES) + 1000

        def key_(sp):
            if sp.get("kind") == "cover":
                return (-1e9, 0)
            if sp.get("kind") == "sources":
                return (1e9, 0)
            return (order.get(sp.get("pid"), idx[id(sp)] + 1), idx[id(sp)])
        BK_PAGES.sort(key=key_)
        _ = last
    lines.append(u"layout table %s: %d rows applied; page order %s" % (
        BK_TABLE, used, u" ".join(sp.get("pid", u"?") for sp in BK_PAGES)))


TRIG_WHY = [None]
OUT_DIR = bg_output(OUT_FOLDER)
LOG_DIR = bg_logs()
BK_EXPECT = ("selinus_board", "bergama_masterplan", "Bergama_water_balance_analysis", "Bergama_agriculture_alternatives",
             "bergama_water_board", "bergama_proposal_sections", "Bergama_city_link_analysis",
             "bergama_b19_plan")              # v38 (round 9 a1): B19Plan is a chain step, p20's map comes from it


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
    del BK_BOXES[:]
    BK_CENTRE.clear()                             # v38: per-run counts and labels (Rhino keeps globals)
    BK_LABELS.clear()
    BK_DISC_SKIP[0] = 0
    del R9_LOG[:]
    lines = []
    write_log(u"RUNNING %s since %s: reading the items.json files\n" % (VERSION, time.strftime("%H:%M:%S")))
    ix_load_all(need=())
    for f in BK_EXPECT:
        if f not in BK_IX:
            wn_warn(None, "missing", u"no items.json from %s (cached/booklet/%s/): run that script first; its pages "
                    u"stay empty" % (f, f))
    bk_remap(lines)
    bk_table_apply(lines)                         # v35: the editable layout table (84_flow)
    lines.append(u"glyph U+0131 dotless i: %s in the booklet font (Arial, %s)" % (
        u"mapped" if not fm_safe(u"\u0131", False)[1] and not fm_safe(u"\u0131", True)[1] else u"MISSING",
        bk_font_files()[0]))
    write_log(u"RUNNING %s since %s: sources and page numbers (%s)\n" % (
        VERSION, time.strftime("%H:%M:%S", time.localtime(t0)), time.strftime("%H:%M:%S")))
    bk_sources_collect()
    pids = [sp["pid"] for sp in BK_PAGES if not sp.get("kind")]
    n_marks = bk_src_number(pids)
    lines.append(u"source marks rewritten in %d texts; %d sources numbered" % (n_marks, len(BK_SRC["order"])))
    os.makedirs(OUT_DIR, exist_ok=True)
    doc = bk_shallow_res(fitz.open())           # v32.4: resource names listed per page, not through every drawing
    n_src = 0
    prog = []                                     # v32.3: progress in the log file while it runs (a hang shows its page)
    for n, sp in enumerate(BK_PAGES, 1):
        t_pg = time.time()
        _head = u"RUNNING %s since %s: page %d of %d (%s) started %s" % (
            VERSION, time.strftime("%H:%M:%S", time.localtime(t0)), n, len(BK_PAGES), sp.get("pid", sp.get("kind")),
            time.strftime("%H:%M:%S"))
        write_log(_head + u"\n" + u"\n".join(prog) + u"\n")
        bk_page_start(sp.get("pid", sp.get("kind")), _head, u"\n".join(prog))
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
        prog.append(u"page %d (%s) %.1f s%s" % (n, sp.get("pid", sp.get("kind")), time.time() - t_pg,
                                                (u", %d texts past the budget" % BK_PG["late"]) if BK_PG["late"] else u""))
        BK_PG["t0"] = 0.0
    lines.extend(BK_PAGENO_LOG)
    lines.append(u"badges %d disc polys drawn by the booklet with their glyph (bk_centre); frames table %s" % (
        BK_DISC_SKIP[0], R9_TABLE_VERSION))
    lines.extend(R9_LOG)
    lines.append(u"page times: " + u"; ".join(prog))
    bk_boxes_write(lines)                         # v37: OUT_DIR/page_boxes.csv (BookletJpg reads only *.pdf there)
    ck_finish(BK_REF_PAGE)
    try:
        doc.subset_fonts()
    except Exception:
        pass
    out = os.path.join(OUT_DIR, PDF_NAME)
    write_log(u"RUNNING %s: saving the PDF (%s)\n%s\n" % (VERSION, time.strftime("%H:%M:%S"), u"\n".join(prog)))
    try:
        doc.save(out, garbage=1, deflate=True)      # v32.4: garbage=3 (merge duplicates) ran 16+ min on the 100 MB booklet
    except Exception as ex_:                        # v35: the PDF is open in a viewer (Windows locks it)
        out2 = os.path.join(OUT_DIR, PDF_NAME[:-4] + time.strftime("_%H%M%S") + ".pdf")
        wn_warn(None, "save", u"%s could not be replaced (%s: open in a viewer? close it): saved as %s" % (
            out, type(ex_).__name__, out2))
        out = out2
        doc.save(out, garbage=1, deflate=True)
    npg = doc.page_count
    doc.close()
    rd_close()
    head = [u"%s  %s  (%d pages, %s)" % (out, time.strftime("%H:%M:%S"), npg, VERSION),
            u"trigger: %s" % (TRIG_WHY[0] or u"run outside Grasshopper")]
    lines.append(u"%s %s, %d drawings placed, %.1f s" % (GH_LABEL, VERSION, BK_STAT["drawings"], time.time() - t0))
    return u"\n".join(wn_compose(tp_log_lines() + lines, head))


def bk_boxes_write(lines):
    """v37 (BRIEF §8): the page box report OUT_DIR/page_boxes.csv, one row per frame: page, block, x, y, w, h (mm, the
    placed content's box; empty when nothing was placed), printed scale, true scale ("|" between the drawings of one
    frame), so the next round compares numbers, not pictures"""
    fn = os.path.join(OUT_DIR, "page_boxes.csv")
    try:
        os.makedirs(OUT_DIR, exist_ok=True)
        with open(fn, "w", encoding="utf-8-sig", newline="") as fh:
            fh.write(u"page,block,x,y,w,h,printed,true,used\r\n")
            for row in BK_BOXES:
                pid, key, b, pr, tr = row[:5]
                used = row[5] if len(row) > 5 else None           # v38 (G9-2): used % of the frame
                box = ([u"%.1f" % b[0], u"%.1f" % b[1], u"%.1f" % (b[2] - b[0]), u"%.1f" % (b[3] - b[1])] if b else
                       [u""] * 4)
                fh.write(u",".join([pid, u'"%s"' % key] + box + [pr, tr, (u"%d" % int(round(100.0 * used)))
                                                                    if used is not None else u""]) + u"\r\n")
        lines.append(u"page boxes: %d frames -> %s" % (len(BK_BOXES), fn))
    except Exception as ex:
        wn_warn(None, "page_boxes", u"%s not written (%s: %s)" % (fn, type(ex).__name__, ex))


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
