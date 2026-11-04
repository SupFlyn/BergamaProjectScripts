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
