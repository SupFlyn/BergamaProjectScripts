# -*- coding: utf-8 -*-
# r: pymupdf==1.26.5
# CURRENT VERSION: bergama_booklet_v32.py = v32 (L1, 4 Nov 2026: the booklet PLACES everything: one box per drawing, labels moved / led out never shrunk, pages justified; see NEW IN v32); v31 (round 6 S9, 4 Nov 2026: 22 pages p01-p22 in the PLAN §2.1 order, each page
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
VERSION = "v32.4"  # v32.4 fix 4 Nov (p02 ran 10+ min in the 21:49 run): faster leader and collision tests (grid), the log shows the page and text count every 5 s, and a page past 150 s sets its remaining texts at their own spot without the search, so the booklet always finishes (hits named as WARNINGs); the PDF is saved without the duplicate merge (16+ min, now seconds); the Sources page composes again (its row height had slipped into a comment); v32.3 fix 4 Nov (Aras 21:38, no log again): the log file shows the page being composed while the booklet runs, and every page's time at the end; v32.2 speed 4 Nov (Aras 21:14): grid index for the page collision tests (same results, far fewer comparisons); v32.1 fix 4 Nov (kit v4.1 run): section label bands no longer loop for ever when two labels sit close (the booklet never finished); v32 4 Nov 2026 (L1): boxes, justified pages, collisions moved never shrunk; v31 4 Nov 2026 (round 6 S9): page frames (G6-1), 22 pages (G6-2), Sources last (G6-3), groups (G6-9); was v30.3 fix (2 Nov run: drawings small, things on top of each other): texts of diagrams, charts, key maps and site board drawings stay where their script set them, scaled with the drawing (site board: from its "sheet scale 1:N"), never moved or numbered into side lists; one factor per diagram row; right-column drawings share the room left; insets 1:100 or 1:200 as the row allows; p02 share 0.50, p07 notes as a 4th row, p13 share 0.78 + smaller key map; 1:50,000 for the p19 farms map; booklet scale list 1:200 ... 1:25,000 with 1:1,500, 1:7,500, 1:15,000 (Aras 06:20) and 1:25,000; scale_pref read as a range; diagrams up to 6 x (right column 2 x); page plan p07 3 rows, p10 windows 2 x 3, p11 share 0.80, p16 3 x 2 share 0.62, p21 share 0.75, p22 plans side by side at 1:1,000 or 1:1,500; v30.2 fix (round 5 open rows): p04/p05 rows = one drawing per cut (sb_sec_s1 ... s8), one scale per page (common); v30.1 fix (round 5 closing): the Sources page lists the masterplan's numbered places as "n name: sources" (v30 printed the raw dict); v30 2 Nov 2026 (round 5 S10): composer pages from items.json, 23 pages, one page numbering
GH_LABEL = "Booklet"
OUT_FOLDER = "bergama_booklet"
LOG_NAME = "bergama_booklet_log.txt"
PDF_NAME = "Bergama_booklet_A3.pdf"
PT = 25.4 / 72.0                             # mm per point (write_pdf needs it)

#@include parts/00_core.py
#@include ../common/hires.py
#@include parts/80_plan.py
#@include parts/81_ids.py
#@include parts/82_compose.py
#@include parts/83_cover_sources.py
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
    write_log(u"RUNNING %s since %s: reading the items.json files\n" % (VERSION, time.strftime("%H:%M:%S")))
    ix_load_all(need=())
    for f in BK_EXPECT:
        if f not in BK_IX:
            wn_warn(None, "missing", u"no items.json from %s (cached/booklet/%s/): run that script first; its pages "
                    u"stay empty" % (f, f))
    bk_remap(lines)
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
    lines.append(u"page times: " + u"; ".join(prog))
    ck_finish(BK_REF_PAGE)
    try:
        doc.subset_fonts()
    except Exception:
        pass
    out = os.path.join(OUT_DIR, PDF_NAME)
    write_log(u"RUNNING %s: saving the PDF (%s)\n%s\n" % (VERSION, time.strftime("%H:%M:%S"), u"\n".join(prog)))
    doc.save(out, garbage=1, deflate=True)          # v32.4: garbage=3 (merge duplicates) ran 16+ min on the 100 MB booklet
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
