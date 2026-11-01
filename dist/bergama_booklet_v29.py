# -*- coding: utf-8 -*-
# r: pymupdf==1.26.5
# CURRENT VERSION: bergama_booklet_v29.py = v29 (1 Nov 2026: saved with placeholders (orange warning); booklet words under 6 pt on a scaled crop set at 6 pt; crop marks may lie in the footer band; v28.1: every layout check that stopped the run (text size, lines, column width, rows, legend room) is a WARNING line and an orange warning; 6.00 pt no longer counts as under 6.0; v28: a source mark too long for its room is set at 6 pt with a warning, the run goes on; v27: text collisions are orange warnings with one WARNING line each, the run goes on (Aras 1 Nov 17:11 + 18:52); v26: round 4 S9; what changed: the NEW IN / VERSION notes below)
"""Bergama Group 6: A3 BOOKLET ASSEMBLER (26 Oct 2026). Rules: scripts/_template/SCRIPT_STANDARD.md §8.
Builds ONE multi-page landscape A3 PDF (420 x 297 mm) from the scripts' OWN sheet PDFs.

Component: Rhino 8 > Grasshopper > Python 3 Script, paste the whole file. The first run installs PyMuPDF 1.26.5 (the
"# r:" line above; needs internet once).
  input  run   Button
  output log   the last run's report: pages, missing drawings, the word size each page prints at
  output done  "done HH:MM:SS.ss · N s" (for the one-click chain: wire the last script's done into run)
Reads  ~/Downloads/Bergama/output/<script folder>/booklet/blocks.json (the panels of each sheet) + the sheet PDFs
Writes ~/Downloads/Bergama/output/bergama_booklet/Bergama_booklet_A3.pdf (one booklet in style a: each crop's _a
  version where its script still writes one, else the crop itself)
NEW IN v26 (round 4, session S9, 1 Nov 2026, a feature change; revision_2026-11-01_round4/PLAN.md):
  * 25 pages (D2): "The proposals in section" on two pages (p13a W1 + W2, p13b W3 + W4: crops ps_p1, ps_p2 at 1:250)
    and "Which plant goes where, in section" on two (p18a F2 + F4, p18b W1 + S4: crops wb_plants_b1, wb_plants_b2 at
    1:250); p19 in four story rows at 1:1 (P19.1: wb_farms | wb_farms_out, ag1_stream | wb_decision, ag1_bars |
    ag1_context, ag1_history | ag1_crops), no caption bands, rows flush with the left margin (PLAN "cap_h", "flush").
  * Cover (P01.1, P01.2, D8): the cover collage Data/W01_cover_collage.jpg (<= 205 mm wide, never enlarged) under the
    title block with the approved text in 4 lines under it; names and date at the foot of the left column; the
    contents column starts level with the top of the MIRAQUA title, lists EVERY page (25: no title is listed once
    for two pages) and the Sources page, with its line spacing stretched to fill the column (up to x1.35).
  * No footer rule on any page (G-R4-10, PALL.1): the footer is the theme name and the page number only.
  * Placeholders RAISE (P09.1, CHK1_2 F1.4): every missing drawing is counted, the log says "placeholders N" (0 too)
    and N > 0 stops the run before the PDF is saved, naming each page and crop.
  * Assembled-page text test (G-R4-1): every word the booklet writes goes through one TextPage per page
    (common/text_place.py, real Arial metrics): titles, intros, captions, legends, footer, cover, contents, Sources;
    each crop is a drawing block no booklet word may enter, each whole-sheet page's own words are kept clear of its
    page number. Log "overlap pNN checked n, collisions 0" for every page; any collision stops the run before the
    PDF is saved (all pages are tested first and listed together). Intros keep >= 2 words on their last line.
  * Sources (P23.1): never below the 6 pt minimum; a second Sources page follows when one page cannot hold them at
    6 pt (logged, contents name the first). The masterplan's places left as they are carry their place names.
  * One trigger file (common/trigger.py, round 4 S1): the Button press or a new done text from the script before it;
    the log says "trigger: ...". Turkish proper names in the plan's text (G-R4-11).
  * Round 4 closing (same v26): the words the booklet writes INTO a crop copy (renumbered source marks, rescaled
    scale words) are registered in the page's TextPage at their printed place and size (copy_words_put); a mark set
    smaller to fit never goes under 6 pt: one that cannot fit RAISES (was down to 0.75 x, unregistered).
NEW IN v25 (round 3, session C, a feature change): contents in three type levels (theme 9.5 pt accent caps, stage
  8 pt bold blue-grey small caps, page titles 7.5 pt) with the page numbers right-aligned in one column (P01.1);
  page numbers are the number only ("17", G2, also on the contents); one minimum type size, grid.py GRID_MIN_PT 6 pt
  (the log's "TYPE BELOW" line); p18 + p19 on one page from round 3's 1:1 crops (P18.1; two pages only if the
  page would overrun or print under 6 pt; log line "p18-19: ..."); the sources page lists the p11 relief's height
  data: the course survey (the one named exception to public-only, N3) and Copernicus GLO-30 with its credit line
  (P23.1); every booklet page logs "FLAG overlap pNN n (booklet text)"; real names in the page intros (G16).
NEW IN v24 (round 2, Aras 31 Oct 11:13 + U24/U31, a feature change): p18 + p19 on ONE page ("Where the clean water
  goes, and what it grows"; the side blocks beside the rows they explain), the two compact pages only if one page
  would print labels under 6 pt; p8 street sections whole: they move to their own page "The streets, before and
  after" when p8 cannot hold them at that size. Both choices are logged.
NEW IN v23 (Aras 31 Oct 08:43-08:46, a feature change): ONE booklet in style a (no alt_b): Bergama_booklet_A3.pdf;
  the old ..._alt_a.pdf / ..._alt_b.pdf in output/bergama_booklet/ are deleted at the run (logged). p6 beige palette,
  p11 b's layout with the section at the bottom drawn in style a: both come from their scripts' plain crops.
NEW IN v21 (Aras 30 Oct 06:20, a feature change): the Sources page lists every asset source once under its own
  ASSETS heading (high-res silhouettes from Data/assets_hires.json, the A1 scale figure sets); no source note beside
  a drawing.
NEW IN v20.1 (bugfix, T5 fix pass 29 Oct): "inferred" joins the status words the sources page never prints.
NEW IN v20 (revision 29 Oct, WO-T5-1; a feature change, so the next whole number):
  * Page list of the revision (data/PLAN.py): p.02 side column = plan 01's key, the edge from above, the readings;
    p.04-05, p.14-15 and p.21 carry their key maps inside their crops (D11: each shows only its page's cuts), no key
    band; p.06 holds the old p.22 filter (D1 a); movement on three pages (D8 b): how people use it, the framework +
    who the project brings + street sections before/after (D3 b), the spine hub by hub; p.17 on two pages, the plant
    ladder page gone (D9 a); masterplan at 1:5,000, the water edge plans with their sections at 1:1,000.
  * Sources page public only (D13, Aras 29 Oct 18:56): a source text prints only the parts that name a public source;
    our survey, readings and calculations get no line; "assumed / interpolated / calculated / estimated" never print;
    a mark with no entry is taken off its page (logged); the site board's p.21 sources and every Commons photo credit
    are listed (blocks.json "sources", PLAN ALWAYS_KEYS); own site photos carry no credit.
  * One figure, one value (G10) also checks the olive area (ha). The pp.07-08 ALT page and the filter page switch
    (MERGE_21_22) are gone with the pages they joined.
NEW IN v19 (MIRAQUA 28 Oct, booklet revision v4; a feature change, so the next whole number):
  * G1 footer without the project and course lines (legend from column 1); G2 every word the booklet adds to a crop
    in the embedded Arial; G9 each crop shows its own stripped copy of its sheet page (words, images and line art
    outside it removed, 0.5 mm margin; G9_LINE_ART = False turns the line-art pass off).
  * G10 one figure, one value: a figure printed two ways is logged. N1 pages renumbered, cross-references checked by
    theme and title, references by number logged.
  * P04.1 / P14.1 section and heritage key maps at 1:1 in a band under the title; the rows make room.
  * N2 sources page: photo credits, the OSM footprints note, Corn (Mısır), the masterplan's place sources (its
    plan_sources), the senses sheet. F5 sources that are not public online removed with their marks (F5_DROP); the
    log lists the figures left without one.
  * D1 "Open ground and where we can build" is one page (MERGE_21_22); S1 new senses page after the S4 cut; p.02 edge
    types, p.07 notes beside the maps, p.09 index change, p.20 key map; no spreads.
  * P78.ALT pp.07 and 08 on one page as a separate PDF (Bergama_booklet_A3_ALT_p07-08.pdf) when legible, otherwise
    the log says why.
NEW IN v18 (Aras 27 Oct 17:35, Prompt 8 "final check of every page"): one source numbering for the whole booklet: the
[n] marks are renumbered in page order (first use first, one number per source text), the sources page lists only what
the pages cite, grouped by theme, and the log names marks without a source entry; the words of a sheet that no page
shows are taken out of it (the hidden stray "1:1,511" of the old p.10, junk in Illustrator); a whole-sheet page gets
the booklet's page number (and its theme where the corner is free); sheet pages are titled in the contents as the
sheets print them; a page whose drawings are all still frames ("later prompt") is left out (PLAN FRAME_PAGES); a
legend too long for the footer goes in columns under the rows when they leave room; two or more rows that leave more
than 40 mm of the page empty share that height out (above, between and below them).
NEW IN v17 (Aras 27 Oct 17:35, Prompt 7 "masterplan"; masterplan v26, site board v49): theme E is the open ground
(crop mp_max_area, now 1:5,000), then one spread: "Before the masterplan: the edge and where we can build" (site board
crop drw_edge_build_e) on the left page, "Masterplan: an ecological corridor" (crop mp_plan: both halves, the notes as
callouts beside them) on the right; all three the whole site frame at 1:5,000, drawn for the page at 1:1. "Why each
place" is gone. A page marked flex goes after the spread that follows it when that spread would open on a right page
(the log says so).
NEW IN v16 (Aras 27 Oct 20:51 "Move the line"; site board v48): the S4 pages ("Four seasons on one cut", "The S4 cut,
north-east bank") get the key map of the sections pages in their title band, S4 alone in ink (site board crop
sec_sections_key_s4): the board's S4 is now the water board's S4. Without that crop the page is built as before and
the log says "key map left out". Prompt 6 (water balance v4, water board v3.1, agriculture v3) needs nothing else here.
NEW IN v15 (Aras 27 Oct 17:34, Prompt 5 "water, part 2"; water board v3, site board v47, agriculture v2): a crop drawn
for its width on the booklet page (block "bk_w") keeps that size in a row too (it was shrunk with the page's one
scale, and a crop with a scale then fell to the next round scale, half size: p.22's plants printed at 1:500 in a
corner); the other crops of the page share what it leaves. p.20, p.21 and p.22's plants panel are such crops (water
board v3, 1:1 on A3). p.22 "Which plant goes where": the plants over the site board's July shade strip (crop
drw_shade_strip, hours of shade along the reach; the tree-cover chart where the board has not made it yet, a plan
key "a||b" = the first of these the scripts have written).
NEW IN v14 (Aras 27 Oct 17:34, Prompt 4 "water, part 1"; water balance v3, water board v2): "How the stream behaves"
is no longer its own page: the water balance sheet (v3) opens with it in a band beside its title, so the page reads
analysis first, then what we got (stage "Analysis, what we got"); "Collect, clean, hold" keeps its crop (the water board
v2 drops the tiles without data). One page fewer from p.12 on.
NEW IN v13 (Aras 27 Oct 17:34, Prompt 3 "movement and the city"; site board v46, city link v2): p.8 "How people use
it" stacks its three maps (the plan, walking today, driving today), each the whole site frame at 1:10,000 with its
scale bar and north arrow under it; p.10 and p.23 take the board's redrawn maps at the same scale (same crops).
NEW IN v12 (Aras 27 Oct 17:34, Prompt 2 "site and stream edge"; site board v45): p.2 "What is there" = plan 01 with the
site readings (bank bars and land-use ring, crop drw_site_readings) as a side panel at the right margin, top-aligned,
the plan's legend in two columns under it on the panel's own grid; p.6 "The stream edge and where we can build" (crop
drw_edge_build at 1:5,000, replaces the edge plan and the photo strip); each sections page has its key map (crop
sec_sections_key_n, 1:50,000) in the title band at the right; a drawing designed at a round booklet scale keeps it
when its sheet scale is rounded (a 0.05 % tolerance; it could print at the next scale, half size).
NEW IN v11 (Aras 27 Oct 17:27, Prompt 1: structure only): pages run in theme cycles A site and stream edge,
B movement and the city, C water, D history and heritage, E masterplan as the synthesis; each theme runs analysis ->
what we got -> what we do with it, named in every page's kicker, the footer and the contents. Merges set up as frames:
old p2 + p4, p5 + p6 one page each; the heritage loop on its own page in D; the masterplan halves + open ground + new
edge diagram + the notes as a two-page spread (left page even). A drawing a later prompt makes is a labelled frame.
NEW IN v10.1 (bugfix, 27 Oct 16:04): page "Why each place" after the masterplan halves, when masterplan v24.1 writes
the notes its key columns had no room for (crop mp_notes); the text under the component shows a newly pasted version
at once, idle.
NEW IN v9 (Aras 27 Oct 06:20 "pair them anyway"): the four proposal sections always share pages two at a time.
NEW IN v8 (Aras 26 Oct 08:27-08:28, on the v7 build): the two masterplan halves share one page, side by side, each at
its own round scale; "Long section along the spine" is left out (it repeated the "What is there" map); water board
v1.13 (larger storage figures).
NEW IN v7 (deck review 26 Oct 07:06, last pass R7; site board v43, water board v1.12, masterplan v23, city link
v1.10, proposal sections v6, agriculture v1.5): no half-empty pages: two drawings planned together share one page
when both fit at no less than 3/4 of the size each gets alone, else each keeps its own page (the four proposal
sections); a sheet's own title words it marks as not for the booklet (" · form A") are taken out of its crop, its
source marks [n] stay (the sources page lists them); more air between a caption and the next row; where several sheet
PDFs match a name, the newest file is used (an old version left in the folder is never picked).
NEW IN v6 (deck review 26 Oct 07:06, water board v1.12): the water board's panels are each laid out as one A3 page;
"Four seasons on one cut" is one crop (wb_s4_seasons, the four rows at 1:250); planting bands and species share one
page (the species list was a half-empty page of its own).
NEW IN v5 (Aras's deck review 26 Oct 07:06, site board v42): "The stream edge" page adds the plan of what meets the
water (drw_edge_plan) between the tree cover and the photos; "Sections across the stream" shows ALL the board's cuts
(S1-S8) at one round scale on at most two pages (sec_sections_1, sec_sections_2), not S1-S5 one by one.
NEW IN v4 (Aras 26 Oct 06:35, lasting rules): one drawing is never divided over two pages (each panel goes on its
page whole, and "what is there" appears once); every printed scale is a round number (1:1,000, 1:2,500, 1:5,000,
1:10,000 ...): the page takes the largest round scale at which everything fits, and a scale a sheet states inside a
panel is changed to the scale the booklet prints it at.
NEW IN v3 (Aras 26 Oct 05:54 "the booklet transformation is not really successful ... drawings themselves in a
separate pdf much more better"; 06:02 picked "sheet pages, split to 5 pt"): every page IS the sheet. An A3 sheet goes
in as it is; a panel of a big sheet is cut out WITH its own words and shown at one scale per page (never stretched,
nothing rewritten or moved). The
booklet adds only the cover, page titles, captions, page numbers and one sources page (each sheet's own source key).
A missing drawing leaves a labelled placeholder, so the booklet always builds.
"""
import os, re, time, json, fnmatch

# ---- SETTINGS ----
VERSION = "v29"  # v29 1 Nov 22:10 (Aras 19:49): saved with placeholders (orange warning); booklet words under 6 pt on a scaled crop set at 6 pt; crop marks may lie in the footer band; v28.1 1 Nov 21:40 (Aras 19:33, p05 '1:1,000' at 6.00 pt): every layout check that stopped the run (text size, lines, column width, rows, legend room) is a WARNING line and an orange warning; 6.00 pt no longer counts as under 6.0; v28 1 Nov 21:15 (Aras 19:08, the source mark [16,20] on the water balance sheet): a renumbered source mark that needs under 6 pt is set at 6 pt with a WARNING line and an orange warning instead of stopping; v27 1 Nov 20:55: text collisions are orange warnings with one WARNING line each, the run goes on (Aras 1 Nov 17:11 + 18:52); v26 (round 4 S9, 1 Nov 2026): 25 pages, cover collage + contents, no footer rule, placeholders and text collisions raise, one trigger file; v25.3 fix 1 Nov 08:30: only the component's own inputs can start it (a True setting inside the script no longer does); v25.2 fix 1 Nov 08:20: chain trigger keyed to each solve (Rhino keeps globals), so the chain continues after ZoneBase; v25.1 fix 1 Nov: a pasted or rewired component no longer runs by itself (chain trigger notes the wire on its first solve)
GH_LABEL = "Booklet"
OUT_FOLDER = "bergama_booklet"
LOG_NAME = "bergama_booklet_log.txt"
PDF_NAME = "Bergama_booklet_A3.pdf"
FONT = "Arial"                               # "Arial" (every Windows PC) or "Inter" (if installed)
G9_MARGIN = 0.5                              # v19 (MIRAQUA 28 Oct, G9): mm round a crop that its own copy keeps
G9_LINE_ART = True                           # v19 (G9): False keeps the line art outside a crop (only words and images go)

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
GRID_MIN_PT = 6.0                                 # no text below this size on any page (PLAN p18-19 rule)

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
    if c0 < 1 or c0 + n - 1 > GRID_COLS:
        raise ValueError("grid span %d+%d is off the %d-column grid" % (c0, n, GRID_COLS))
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
    baseline: [rect]; raises when the stack runs past the drawing area (no block may leave the page)"""
    y = GRID_AREA[1] if y0 is None else grid_snap_y(y0, up=False)
    out = []
    for h in heights:
        r = grid_cell(c0, n, y, h)
        out.append(r)
        y = r[3] + gap
    if out and out[-1][3] > GRID_AREA[3] + 1e-6:
        raise ValueError("grid stack runs %.1f mm past the drawing area" % (out[-1][3] - GRID_AREA[3]))
    return out


def grid_row(widths_cols, y, h, c0=1):
    """blocks side by side on one baseline row: widths_cols = [n columns each] from column c0: [rect]"""
    out, c = [], c0
    for n in widths_cols:
        out.append(grid_cell(c, n, y, h))
        c += n
    if c - 1 > GRID_COLS:
        raise ValueError("grid row needs %d columns, the grid has %d" % (c - 1, GRID_COLS))
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
# ---- text_place.py (round 4, S1, 1 Nov 2026; G-R4-1, G-R4-2, PLAN §4.1): ONE text placer, a collision RAISES -------
# Replaces label_place.py (its lp_* names stay as shims there until the closing step, see label_place.py).
# Every printed letter of a page goes through ONE TextPage: it measures with the real font (font_metrics.py), keeps
# every box, draws everything in .emit(drawer) (no other text path), and .check() RAISES TextCollision when any two
# texts, a text and an obstacle, a text and the page edge / margins / footer zone, or two drawing blocks overlap.
# Needs, included before it: pdf_fonts.py, font_metrics.py, grid.py (GRID_MIN_PT, grid_marked_runs).
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
#                                                     never below min_pt, never dropped: no spot and no side_list
#                                                     raises TextCollision. rank orders nothing here (callers place
#                                                     rank 0 first); kept for the interface
#   tp.check(raise_=True, log=None) -> n_items        the collision test; logs "overlap <page> checked n, collisions k"
#                                                     and raises TextCollision(page, item, other) when k > 0
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
TP_LOG = []
TP_PT = 25.4 / 72.0
TP_ROW_MM = 8.0                 # reading order: anchors within this many mm of height count as one row
TP_POSITIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
TP_LINE_KINDS = ("line", "edge", "street", "road", "cut", "stream", "bank", "contour", "leader")


class TextError(RuntimeError):
    pass


TP_WARN_ONLY = [True]   # 1 Nov (Aras): check() writes hits as warnings instead of raising; [False] = raise


def tp_warn(msg):
    """1 Nov (Aras 19:33 "get this already"): a layout check that used to stop the run writes "WARNING <msg>" to
    TP_LOG and an orange Grasshopper warning, and the run goes on (TP_WARN_ONLY = [False] raises TextError again)"""
    if not TP_WARN_ONLY[0]:
        raise TextError(msg)
    TP_LOG.append(u"WARNING " + msg)
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
                tp_warn(u"the word %r (%.1f mm at %.1f pt) is wider than its column (%.1f mm): it runs over" % (
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
            raise TextError(u"side list %s is closed: place its labels before close()" % self.name)
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
            tp_warn(u"%s: %r prints at %.2f pt, below the %.1f pt minimum" % (
                self.name, text[:40], pt * self.scale, self.min_pt))

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
            lines = tp_wrap(text, w * u, size, bold, min_last_words, bold_marks)
            lead = lead * size / float(pt)
        if max_lines is not None and len(lines) > max_lines:
            tp_warn(u"%s: %r needs %d lines, %d allowed: shorten it" % (self.name, text[:50], len(lines),
                                                                       max_lines))
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

    def place(self, text, anchor, positions=TP_POSITIONS, alts=(), pt=7.0, rank=0, side_list=None, bold=False,
              colour=None, name=None, r=0.0, gap=0.8, allow=(), role="label"):
        """a label beside its point (see the module notes); returns the registered item"""
        d = float(r) * self.unit_mm + gap
        for t in (text,) + tuple(alts or ()):
            t = u"%s" % t
            self._size_ok(t, pt)
            for code in positions:
                x, y, al = self._at(code, t, anchor, pt, bold, d)
                b = self._box(t, x, y, pt, bold, al, 0.0)
                if self._free(b, allow):
                    self.put(t, x, y, pt, bold, al, 0.0, name, role, colour, allow)
                    return self.items[-1]
        if side_list is None:
            raise TextCollision(self.name, dict(text=u"%s" % text, name=name), u"no free spot round its point and no "
                                u"side list to number it")
        x, y, al = self._at("C", u"0", anchor, pt, True, 0.0)
        self.put(u"0", x, y, pt, True, "C", 0.0, name, "number", colour, tuple(allow) + ("marker",))
        it = self.items[-1]
        if side_list not in self.sides:
            self.sides.append(side_list)
        side_list.add(anchor, u"%s" % text, it)
        return it

    # -- the test
    def check(self, raise_=True, log=None):
        """the collision test (see the module notes); returns the number of texts checked"""
        for sl in self.sides:
            if not sl.closed:
                tp_warn(u"%s: side list %s was never closed (its numbers are not set)" % (self.name, sl.name))
        hits = []
        I = self.items
        for i, a in enumerate(I):
            b = a["box"]
            if not (self.inner[0] - 1e-6 <= b[0] and b[2] <= self.inner[2] + 1e-6 and
                    self.inner[1] - 1e-6 <= b[1] and b[3] <= self.inner[3] + 1e-6):
                hits.append((a, u"the page edge or its margins"))
            if self.footer_zone and a["role"] not in ("footer", "crop_word") and tp_hit(b, self.footer_zone, 0.0):
                hits.append((a, u"the footer zone"))
            for c in I[i + 1:]:
                if c["group"] != a["group"] and tp_hit(b, c["box"], self.pad):
                    hits.append((a, c))
            for K in self.keeps:
                if K["name"] in a["allow"] or K["kind"] in a["allow"]:
                    continue
                if _tp_keep_hits(b, K, self.pad):
                    hits.append((a, K))
        B = self.blocks
        for i, a in enumerate(B):
            for c in B[i + 1:]:
                if tp_hit(a["box"], c["box"], -0.01 / self.unit_mm):
                    hits.append((a, c))
        line = u"overlap %s checked %d, collisions %d" % (self.name, len(I), len(hits))
        lg = log if log is not None else (self.log if self.log is not None else TP_LOG)
        lg.append(line)
        self.checked = True
        if hits and raise_ and TP_WARN_ONLY[0]:          # 1 Nov (Aras 17:11 / 18:51): every hit a WARNING line and an
            k_ = len(lg) - 1                             # orange warning; the run goes on, one run collects them all
            lg[k_:k_] = [u"WARNING %s text hit: %s against %s" % (self.name, _tp_desc(a_), _tp_desc(b_))
                         for a_, b_ in hits]             # (before the "overlap ..." line, which stays the last)
            try:
                ghenv.Component.AddRuntimeMessage(__import__("Grasshopper").Kernel.GH_RuntimeMessageLevel.Warning,
                                                  u"%s: %d text hits (each one in the log, 'WARNING %s text hit')" %
                                                  (self.name, len(hits), self.name))
            except Exception:
                pass
            return len(I)
        if hits and raise_:
            raise TextCollision(self.name, hits[0][0], hits[0][1], len(hits), hits[1:])
        return len(I)

    def emit(self, drawer):
        """draws every registered text through drawer(item); returns how many"""
        n = 0
        for it in self.items:
            if not it["emit"]:
                continue
            if it["role"] == "number" and it["text"] == u"0":
                raise TextError(u"%s: a numbered label was never given its number (close its side list)" % self.name)
            drawer(it)
            n += 1
        return n

    def export(self):
        """boxes in mm, y DOWN from the top-left of bounds (crop-local), for the booklet's assembled-page test"""
        if not self.checked:
            raise TextError(u"%s: export() before check()" % self.name)
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
TRIGGER_BUTTON_WORDS = ("run", "bake", "build", "go", "press", "button", "start")


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
            key = key + ":" + str(ghenv.Component.InstanceGuid) + ":" + _chain_wiring()      # noqa: F821
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
        if first or _scx.sticky.get(key) == s:
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
        pk = "trig_prev:" + key + ":" + gk
        on = to_bool(trig_get(btn)) if btn else False
        prev = bool(_scx.sticky.get(pk, False))
        _scx.sticky[pk] = on
    except Exception:
        on, prev = (to_bool(trig_get(btn)) if btn else False), False
    if on and not prev:
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
TRIG_WHY = [None]                            # v26 (round 4 S1/S9): what started this run (trig_should_run), in the log
COVER_IMG = "W01_cover_collage.jpg"          # v26 (P01.2): the cover collage, in Downloads/Bergama/Data/ (own work, no
COVER_IMG_W = 205.0                          # credit); printed 205 mm wide (1600 x 810 px: ~200 dpi, never larger)
COVER_TEXT = (u"MIRAQUA turns the walled Selinos stream through Bergama into a landscape that lives in all four seasons. "
              u"Clean water is collected, cleaned and held at the upstream entry, kept in the bed as a summer strip, and "
              u"given to the farms outside the site. Planting follows the days under water, from wet to dry; when the "
              u"water rises, life on the banks pauses and returns as it drops. A streamside spine of five bridge places "
              u"ties the Kale side to the bazaar side.")   # v26 (D8, approved as drafted: BRIEF P01.2)
BERGAMA = BERGAMA_ROOT
OUT_DIR = bg_output(OUT_FOLDER)                  # v10 (27 Oct): the booklet PDF only
LOG_DIR = bg_logs()
ASSET_ROOT = os.path.join(BERGAMA, "output")     # the scripts' sheet PDFs
BK_ROOT = bg_booklet("")                         # v10: the scripts' booklet assets (cached/booklet/<folder>/blocks.json)

# ---- GRID (design-language.md: all values in mm, origin top-left) ----
# revision 30 Oct (M1): the ONE booklet grid lives in common/grid.py; the names below are its values
PW, PH = GRID_PAGE
ML, MT, MB = GRID_ML, GRID_MT, GRID_MB       # left/right margin, top, bottom
COLS, COL, GUT = GRID_COLS, GRID_COL, GRID_GUT   # 14 + 12 x 29 + 11 x 4 + 14 = 420
BASE = GRID_BASE                             # baseline grid, from y = 12
BOOK_VARIANTS = ("a",)                       # v23 (Aras 31 Oct 08:46): one PDF in style a, each crop id taken with
                                             # the suffix _a where its script still writes one
INTRO_MIN_COLS = 5                           # the intro sits beside the title when this many columns are free
LEG_ROW, LEG_GAP = 4.0, 4.0                  # a drawing's legend: row pitch, gap between its columns (mm)
FOOT_RULE, FOOT_B1, FOOT_B2 = 276.0, 280.0, 284.0
FOOT_LEG_COL = 1                             # v19 (MIRAQUA 28 Oct, G1): the footer legend from column 1 (was 4: the
                                             # project and course lines sat in columns 1-3)
PT = 25.4 / 72.0                             # mm per point
K = 72.0 / 25.4                              # points per mm

# ---- TYPE (pt; size follows design importance) ----
T = dict(title=40, part=24, figure=24, sub=14, statement=13, body=9.5, caption=7.5, label=7.5, kicker=8, pageno=14)
LEAD = dict(title=16.0, part=10.0, statement=6.0, sub=6.0, body=4.0, caption=3.2, label=3.2)   # mm
MIN_BODY, MIN_CAPTION = 9.0, GRID_MIN_PT   # v25 (round 3): ONE minimum, grid.py GRID_MIN_PT (6 pt)

# ---- COLOUR (palette v1.4 core roles; contrast on white checked in design-language.md) ----
INK, INK2, ACCENT = "4A3F35", "6B645B", "8B3A3F"
# v25 (round 3, P01.1, PLAN §2 "type levels on contents"): theme > stage > page title, each its own size and colour
CONT_PT = dict(part=9.5, stage=8.0, title=7.5, no=7.5)   # pt
CONT_STAGE = "5C7A86"                        # the stage line's colour (palette reference 5C7A86)
CONT_NO_W = 6.0                              # mm: the page numbers' column, right-aligned at its right edge
SMALL_CAPS = 0.8                             # small capitals: the lower-case letters as capitals at 0.8 x the size
RULE, FRAME, PAPER = "B0AC9C", "D8D5CC", "FFFFFF"

def bergama_data(name, _c={}):
    """Built-in data kept in Downloads/Bergama/Data/bergama_booklet_data.py (Aras 25 Oct 21:29, scripts shortened): runs its
    section `name` here, as if it were written in this place. The file is read once per run; a missing file or one
    from another version of this script stops the script with a message saying which file to copy."""
    import os as _os, hashlib as _hl
    if not _c:
        p_ = _os.path.join(_os.path.expanduser("~"), "Downloads", "Bergama", "Data", "bergama_booklet_data.py")
        if not _os.path.isfile(p_):
            raise RuntimeError("Data file missing: copy bergama_booklet_data.py from the run kit's Data folder into " + _os.path.dirname(p_))
        with open(p_, encoding="utf-8", newline="") as f_:
            for part_ in f_.read().split("\n#@@ ")[1:]:
                k_, _, b_ = part_.partition("\n")
                _c[k_] = b_
    b_ = _c.get(name)
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != {'PLAN': 'b9f328b8a62f719d17df13cc3633100e'}.get(name):
        raise RuntimeError("Data file bergama_booklet_data.py is not the one made with this script version (part " + name +
                           "): copy it again from the same run kit as the script")
    exec(compile(b_, "bergama_booklet_data.py:" + name, "exec"), globals())


bergama_data("PLAN")


def colx(c):
    return ML + (c - 1) * (COL + GUT)


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


# ------------------------------------------------------------------ fonts
def font_files():
    """(regular, bold) TrueType files for FONT, else Arial, else Liberation Sans/DejaVu (offline test only)."""
    win = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
    user = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts")
    cands = {"Inter": [("Inter-Regular.ttf", "Inter-Bold.ttf"), ("Inter-Regular.otf", "Inter-Bold.otf")],
             "Arial": [("arial.ttf", "arialbd.ttf")]}
    order = [FONT] + [f for f in ("Arial",) if f != FONT]
    for fam in order:
        for reg, bold in cands.get(fam, []):
            for d in (win, user, "/usr/share/fonts/opentype/inter"):
                r, b = os.path.join(d, reg), os.path.join(d, bold)
                if os.path.isfile(r) and os.path.isfile(b):
                    return fam, r, b
    for d, r, b in (("/usr/share/fonts/truetype/liberation", "LiberationSans-Regular.ttf", "LiberationSans-Bold.ttf"),
                    ("/usr/share/fonts/truetype/dejavu", "DejaVuSans.ttf", "DejaVuSans-Bold.ttf")):
        if os.path.isfile(os.path.join(d, r)):
            return "fallback " + r[:-4], os.path.join(d, r), os.path.join(d, b)
    raise RuntimeError("no TrueType font found (looked for %s and Arial in %s)" % (FONT, win))


class Typo(object):
    """Text writer: whole lines as live text, one embedded font, wrapping by measured width."""
    def __init__(self, fitz):
        self.fam, self.freg, self.fbold = font_files()
        self.F = {False: fitz.Font(fontfile=self.freg), True: fitz.Font(fontfile=self.fbold)}
        self.issues, self.notes = [], []
        self.tp = None              # v26 (G-R4-1): the TextPage of the page being built (frame_page opens it)
        self.tps = []               # v26: every page's TextPage, in page order (text_test checks them)

    def width(self, s, size, bold=False):
        return self.F[bold].text_length(s, fontsize=size) * PT

    def split_long(self, word, w, size, bold=False):
        """A word wider than w (a URL) cut into pieces that fit, after / . - _ ? & = where possible."""
        out, cur = [], ""
        for ch in word:
            if cur and self.width(cur + ch, size, bold) > w:
                m = max(cur.rfind(c) for c in "/.-_?&=")
                if m > len(cur) // 2:
                    out.append(cur[:m + 1]); cur = cur[m + 1:]
                else:
                    out.append(cur); cur = ""
            cur += ch
        return out + [cur]

    def wrap(self, s, w, size, bold=False):
        out = []
        for para in str(s).split("\n"):
            line = ""
            words = []
            for word in para.split(" "):
                words += self.split_long(word, w, size, bold) if self.width(word, size, bold) > w else [word]
            for word in words:
                t = (line + " " + word).strip()
                if line and self.width(t, size, bold) > w:
                    out.append(line); line = word
                else:
                    line = t
            out.append(line)
        return out

    def line(self, page, s, x, y, size, col=INK, bold=False, align="L", angle=0.0, small_ok=False, role="label",
             group=None, name=None):
        """One line of live text; (x, y) = left (or centre/right) end of the baseline, mm; angle in degrees
        (counter-clockwise, about the baseline start). v26 (round 4, G-R4-1): every line is registered in the page's
        TextPage (real Arial box; role "footer" for the footer band; lines of one paragraph share a group, so only
        other texts are tested against them); nothing goes below the 6 pt minimum (small_ok is no longer used)."""
        if not s:
            return
        if size < MIN_CAPTION:
            self.issues.append("TYPE BELOW %g pt (%.1f): %s" % (MIN_CAPTION, size, s[:40]))
        if self.tp is not None:
            self.tp.put(s, x, y, size, bold, align, angle, name=name or s[:24], role=role, group=group, emit=False)
        if align != "L":
            wd = self.width(s, size, bold)
            x -= wd / 2 if align == "C" else wd
        if abs(angle) > 0.5:
            import fitz as _fz
            pt = _fz.Point(x * K, y * K)
            page.insert_text(pt, s, fontname="FB" if bold else "FR", fontsize=size, color=hexrgb(col),
                             morph=(pt, _fz.Matrix(-angle)))
        else:
            page.insert_text((x * K, y * K), s, fontname="FB" if bold else "FR", fontsize=size, color=hexrgb(col))


# ------------------------------------------------------------------ assets
def load_assets():
    """{script folder: blocks.json dict (with its folder)} for every script that wrote booklet assets."""
    found = {}
    names = set()
    for root in (BK_ROOT, ASSET_ROOT):
        if os.path.isdir(root):
            names.update(n for n in os.listdir(root) if os.path.isdir(os.path.join(root, n)))
    for name in sorted(names):
        p = bg_first([os.path.join(BK_ROOT, name, "blocks.json"),                 # v10: cached/booklet/<folder>/
                      os.path.join(ASSET_ROOT, name, "booklet", "blocks.json")])   # scripts before 27 Oct
        if os.path.isfile(p):
            try:
                with open(p, encoding="utf-8") as f:
                    d = json.load(f)
                d["_dir"] = os.path.dirname(p)
                d["_time"] = time.strftime("%d %b %H:%M", time.localtime(os.path.getmtime(p)))
                found[name] = d
            except Exception as ex:
                found[name] = {"_error": "%s: %s" % (type(ex).__name__, ex)}
    return found


# ------------------------------------------------------------------ sheets
_DOCS = {}


def sheet_doc(fitz, path):
    if path not in _DOCS:
        _DOCS[path] = fitz.open(path)
    return _DOCS[path]


def find_pdf(folder, name):
    """A sheet PDF of a script's output folder (subfolders too, e.g. the board's selinus_board_pdf); name may hold *."""
    root = os.path.join(ASSET_ROOT, folder)
    hit = [os.path.join(d, n) for d, _, names in os.walk(root) for n in names if fnmatch.fnmatch(n, name)]
    return max(hit, key=os.path.getmtime) if hit else None    # v7: the newest (v1_8 sorts after v1_12 by name)


_COPY = {}       # v19 (G9): (sheet path, page index, clip key) -> (doc, page index): one copy per place a page shows
_COPY_PUT = {}   # v26 closing (G-R4-1): the same key -> the words the booklet wrote into that copy (copy_of)
_PAGE_TXT = {}   # v19: (sheet path, page index) -> (its lines of words, invisible words, images): read once a run
_FONTBUF = {}    # v19 (G2): bold -> (font file bytes, fitz.Font): the booklet's Arial, read once a run
G9_STATS = dict(copies=0, lines=0, chars=0, images=0, failed=[])
_RED = dict(img_none=0, img_remove=1, art_none=0, art_covered=1, txt_remove=0, txt_none=1)   # PyMuPDF redaction codes


def clip_key(clip):
    return None if clip is None else tuple(round(v, 1) for v in clip)


def src_page(fitz, path, pno_, clip=None):
    """v18: (doc, page index) the booklet shows of a sheet page. v19 (MIRAQUA 28 Oct, G9): one copy per (sheet, page,
    clip), made once (strip_copy): its marks in the booklet's source numbers and, for a crop, nothing outside it"""
    return copy_of(fitz, path, pno_, clip, _SRC[0] if _SRC else None)


def copy_of(fitz, path, pno_, clip, srcs):
    """v26 closing (G-R4-1): the cached copy of (sheet, page, clip) (strip_copy), made once, with the words the
    booklet wrote into it (_COPY_PUT: (x pt, baseline y pt, text, size pt, bold) on the sheet page)"""
    ck = (path, pno_, clip_key(clip))
    if ck not in _COPY:
        put = []
        _COPY[ck] = strip_copy(fitz, path, pno_, clip, srcs, put)
        _COPY_PUT[ck] = put
    return _COPY[ck]


def copy_words(path, pno_, clip=None):
    """v26 closing: the words the booklet wrote into the copy of (sheet, page, clip) (see copy_of)"""
    return list(_COPY_PUT.get((path, pno_, clip_key(clip))) or ())


def _bk_warn(msg):
    """v29: a WARNING line in the log and an orange warning; the booklet is still saved"""
    TP_LOG.append(u"WARNING " + msg)
    try:
        ghenv.Component.AddRuntimeMessage(__import__("Grasshopper").Kernel.GH_RuntimeMessageLevel.Warning, msg)
    except Exception:
        pass


def copy_words_put(typo, key, words, clip, x, y, s, allow=None):
    """v26 closing (G-R4-1, closing part C F): the words the booklet itself writes into a crop copy (renumbered
    source marks, rescaled scale words; raw insert_text there) registered in the page's TextPage at their printed
    place and size (sheet pt -> page mm: the clip's corner at (x, y) mm, factor s; clip None = a whole sheet from
    the page's corner), so a word under the 6 pt minimum RAISES TextError there and the text test sees them. They
    may sit on their own crop (its keep, or allow); one group per crop (marks side by side may touch)."""
    if typo.tp is None or not words:
        return 0
    nm = key.split("/", 1)[-1] if key else "crop"
    x0, y0 = (clip.x0, clip.y0) if clip is not None else (0.0, 0.0)
    g = typo.tp._group()
    for px, py, t, size, bold in words:
        typo.tp.put(t, x + (px - x0) / K * s, y + (py - y0) / K * s, size * s, bold, "L", 0.0,
                    name=u"%s · booklet word %s" % (nm, t), role="crop_word", allow=allow or (nm,), group=g,
                    emit=False)                        # v29: a word of the crop may lie where the crop does (footer band)
    return len(words)


def own_font(fitz, pg, bold=False):
    """v19 (MIRAQUA 28 Oct, G2): the booklet's Arial, embedded on a copied sheet page for the words the booklet
    rewrites there (scales, source numbers; they were the standard Helvetica helv/hebo, not embedded):
    (font name on pg, fitz.Font to measure with)"""
    if bold not in _FONTBUF:
        with open(font_files()[2 if bold else 1], "rb") as f:
            data = f.read()
        _FONTBUF[bold] = (data, fitz.Font(fontbuffer=data))
    name = "BkB" if bold else "BkR"                  # never the sheets' own /F1 ... names
    pg.insert_font(fontname=name, fontbuffer=_FONTBUF[bold][0])
    return name, _FONTBUF[bold][1]


def page_text(fitz, path, i):
    """v19: a sheet page's lines of words (rawdict), its invisible words (render mode 3, e.g. the water balance's
    source key) and its images (bboxes), read once a run for every copy made of it (laptop speed: they were read
    again for each copy)"""
    k = (path, i)
    if k not in _PAGE_TXT:
        page = sheet_doc(fitz, path)[i]
        lines = [ln for b in page.get_text("rawdict")["blocks"] for ln in b.get("lines", [])]
        try:
            inv = [fitz.Rect(s_["bbox"]) for s_ in page.get_texttrace() if s_.get("type") == 3]
        except Exception:
            inv = []
        try:
            ims = [fitz.Rect(im["bbox"]) for im in page.get_image_info()]
        except Exception:
            ims = []
        _PAGE_TXT[k] = (lines, inv, ims)
    return _PAGE_TXT[k]


def strip_copy(fitz, path, i, clip, srcs=None, out=None):
    """v19 (MIRAQUA 28 Oct, G9 "remove everything that isn't visible on its own page"): (doc, page index) of sheet page
    i copied for ONE place the booklet shows it; the sheet page itself when nothing changes or the copy fails (logged).
    v26 closing: out (a list) gets the words the copy writes (see _strip_copy); a mark that cannot fit at 6 pt
    RAISES (TextError is never taken for a failed copy)"""
    try:
        return _strip_copy(fitz, path, i, clip, srcs, out)
    except TextError:
        raise
    except Exception as ex:
        G9_STATS["failed"].append("%s page %d (%s: %s)" % (os.path.basename(path), i + 1, type(ex).__name__, ex))
        if out is not None:
            del out[:]                                 # the sheet page itself is shown: it holds none of them
        return sheet_doc(fitz, path), i


def _strip_copy(fitz, path, i, clip, srcs, out=None):
    """The copy: its [n] marks in the booklet's numbers (srcs; v18) and, for a crop (clip), what no viewer sees taken out
    (v18 took out only the words outside every crop of the page, 3 mm round them; graphics and images all stayed):
    the words outside the clip + G9_MARGIN (whole lines, else the letters of a line across its edge); the images
    wholly outside it; the line art lying wholly in the four bands round it (PDF_REDACT_LINE_ART_REMOVE_IF_COVERED: a
    path partly inside stays whole with its hidden part, e.g. the long street lines and the big building fills; never
    IF_TOUCHED, which would cut visible lines). Three redaction passes: words, images, line art, each blind to the others."""
    lines, inv, ims = page_text(fitz, path, i)
    folder = (srcs.used.get((path, i)) or [None])[0] if srcs else None
    kid = srcs.key_for(folder, path, i) if srcs and folder else None
    pr = sheet_doc(fitz, path)[i].rect
    mg = G9_MARGIN * K
    near = None if clip is None else fitz.Rect(clip.x0 - mg, clip.y0 - mg, clip.x1 + mg, clip.y1 + mg)
    cut, put, seen, n_l, n_c = [], [], [], 0, 0

    def mid(r, a=None, b=None):                       # the middle of letters: the lines above and below stay whole
        a, b = r if a is None else a, r if b is None else b
        return fitz.Rect(r.x0 + 0.2 * a.width, r.y0 + 0.3 * r.height, r.x1 - 0.2 * b.width, r.y1 - 0.3 * r.height)
    for ln in lines:
        lr = fitz.Rect(ln["bbox"])
        if lr.width < 0.1 or lr.height < 0.1:
            continue
        if near is not None and not lr.intersects(near):          # shown nowhere here: the whole line goes
            cut.append(fitz.Rect(lr.x0, lr.y0 + 0.3 * lr.height, lr.x1, lr.y1 - 0.3 * lr.height))
            n_l += 1
            continue
        seen.append(lr)
        seq = [(ch, s_) for s_ in ln["spans"] for ch in s_["chars"]]
        if near is not None and not near.contains(lr):            # across the clip's edge: its letters outside
            run = []
            for ch, _ in seq + [(None, None)]:
                cr = fitz.Rect(ch["bbox"]) if ch is not None else None
                if cr is not None and cr.width > 0.05 and not cr.intersects(near):
                    run.append(cr)
                    continue
                if run:
                    u = fitz.Rect(run[0])
                    for c_ in run[1:]:
                        u |= c_
                    cut.append(mid(fitz.Rect(u.x0, lr.y0, u.x1, lr.y1), run[0], run[-1]))
                    n_c += len(run)
                    run = []
        if kid is None or abs(ln["dir"][1]) > 0.01 or any(lr.intersects(v) for v in inv):
            continue                                              # turned words, the invisible key
        txt = "".join(ch["c"] for ch, _ in seq)
        for m in MARKS.finditer(txt):
            new = srcs.renum(m.group(0), kid)
            if new == m.group(0):
                continue
            (c0, s0), c1 = seq[m.start()], seq[m.end() - 1][0]
            r = fitz.Rect(c0["bbox"]) | fitz.Rect(c1["bbox"])
            if near is not None and not r.intersects(near):
                continue                                          # it goes with the letters outside the clip
            cut.append(mid(r, fitz.Rect(c0["bbox"]), fitz.Rect(c1["bbox"])))
            if new:                                               # v19 (F5): "" = its sources are not public online
                nxt = next((ch["bbox"][0] for ch, _ in seq[m.end():] if ch["c"].strip()), None)
                ends = [clip.x1] if clip is not None and clip.intersects(r) else []
                room = min([pr.x1 if nxt is None else nxt] + ends) - c0["origin"][0] - 0.3
                put.append((c0["origin"], new, s0["size"], s0["color"], "bold" in s0["font"].lower(), room))
    gone, bands = [], []
    if near is not None:
        keep = [r for r in ims if r.intersects(near)]
        for r in ims:                                 # an image wholly outside: a dot at its centre that hits nothing seen
            if r.is_empty or r.intersects(near):
                continue
            c = fitz.Point((r.x0 + r.x1) / 2.0, (r.y0 + r.y1) / 2.0)
            if not any(k_.contains(c) for k_ in keep + seen):
                gone.append(fitz.Rect(c.x - 0.05, c.y - 0.05, c.x + 0.05, c.y + 0.05))
        if G9_LINE_ART:                               # left and right bands full height: a corner path lies in one
            bands = [b for b in (fitz.Rect(pr.x0, pr.y0, pr.x1, near.y0), fitz.Rect(pr.x0, near.y1, pr.x1, pr.y1),
                                 fitz.Rect(pr.x0, pr.y0, near.x0, pr.y1), fitz.Rect(near.x1, pr.y0, pr.x1, pr.y1))
                     if b.width > 1.0 and b.height > 1.0]
    if clip is None and not cut and not put:
        return sheet_doc(fitz, path), i               # a whole sheet page with nothing to renumber: the sheet itself
    tmp = fitz.open()
    tmp.insert_pdf(sheet_doc(fitz, path), from_page=i, to_page=i)
    pg = tmp[0]
    for annots, opt in ((cut, dict(images=_RED["img_none"], graphics=_RED["art_none"], text=_RED["txt_remove"])),
                        (gone, dict(images=_RED["img_remove"], graphics=_RED["art_none"], text=_RED["txt_none"])),
                        (bands, dict(images=_RED["img_none"], graphics=_RED["art_covered"], text=_RED["txt_none"]))):
        if annots:
            for r in annots:
                pg.add_redact_annot(r, fill=False)
            pg.apply_redactions(**opt)
    fonts = {}
    for org, new, size, col, bold, room in put:       # the new numbers in the booklet's own Arial (G2)
        if bold not in fonts:
            fonts[bold] = own_font(fitz, pg, bold)
        fn, font = fonts[bold]
        w = font.text_length(new, fontsize=size)
        if w > room > 0:                              # the words after it stay clear: set smaller to fit, never
            size2 = size * room / w                   # under MIN_CAPTION (6 pt; v26 closing: was down to 0.75 x)
            if size2 < MIN_CAPTION - 1e-6:            # v28 (Aras 1 Nov 19:08): a WARNING and an orange warning, set
                msg_ = (u"%s page %d: the source mark %r needs %.2f pt to fit before the next word, under the "
                        u"%.1f pt minimum: set at %.1f pt (it may touch the next word); give it room in its sheet" %
                        (os.path.basename(path), i + 1, new, size2, MIN_CAPTION, MIN_CAPTION))
                TP_LOG.append(u"WARNING " + msg_)     # at the minimum; the run goes on
                try:
                    ghenv.Component.AddRuntimeMessage(
                        __import__("Grasshopper").Kernel.GH_RuntimeMessageLevel.Warning, msg_)
                except Exception:
                    pass
                size2 = MIN_CAPTION
            if srcs:
                srcs.n_tight += 1
            size = size2
        pg.insert_text(org, new, fontname=fn, fontsize=size,
                       color=((col >> 16 & 255) / 255.0, (col >> 8 & 255) / 255.0, (col & 255) / 255.0))
        if out is not None:                           # v26 closing: registered where the copy is shown
            out.append((org[0], org[1], new, size, bold))
    if clip is not None:
        G9_STATS["copies"] += 1
        G9_STATS["lines"] += n_l
        G9_STATS["chars"] += n_c
        G9_STATS["images"] += len(gone)
    return tmp, 0


def resolve(assets, key):
    """(crop block, sheet path) of "<folder>/<crop id>"; an id missing under its own sheet key or letter case is looked
    up by its panel name (the board's sections are section_s1 ... on whichever sheet holds them)."""
    folder, _, bid = key.partition("/")
    bl = (assets.get(folder) or {}).get("blocks") or {}
    b = bl.get(bid)
    if b is None:
        tail = bid.lower().split("_", 1)[-1]
        b = next((v for k, v in sorted(bl.items()) if k.lower() == bid.lower() or
                  k.lower().split("_", 1)[-1] == tail), None)
    if not b or b.get("type") != "crop":
        return None, None
    return b, find_pdf(folder, os.path.basename(b.get("pdf", "")))


SCALE_WORD = re.compile(r"1\s?:\s?(\d{1,3}(?:,\d{3})+|\d{2,})")


def rescaled(fitz, path, pno_, clip, s, drop=(), out=None):
    """v4: the sheet page with each scale it states inside clip ("1:400") changed to the scale the booklet prints it
    at (1:400 / s), in the same place, size and colour; the drawing itself untouched. v7: a line of the sheet's words
    matching one of its crop's "drop" patterns is taken out (source marks "[n]" stay). (doc, page index).
    v26 closing (G-R4-1): out (a list) gets every word the booklet wrote into the page it returns (the copy's marks,
    the new scale words) as (x pt, baseline y pt, text, size pt, bold), for copy_words_put"""
    pno0 = pno_
    src, pno_ = src_page(fitz, path, pno_, clip)         # v18: the booklet's source numbers; v19 (G9): this crop's copy
    words = copy_words(path, pno0, clip)
    page = src[pno_]
    pats = [re.compile(d) for d in drop or () if not d.startswith("^\\[")]
    hits, gone = {}, []
    for b in page.get_text("dict", clip=clip)["blocks"]:
        for ln in b.get("lines", []):
            if pats and any(p.search("".join(sp["text"] for sp in ln["spans"]).strip()) for p in pats):
                gone.append(fitz.Rect(ln["bbox"]))
                continue
            for sp in ln["spans"]:
                for m in SCALE_WORD.finditer(sp["text"]):
                    hits[m.group(0)] = (int(m.group(1).replace(",", "")), sp["size"], sp["color"],
                                        "bold" in sp["font"].lower())
    if abs(s - 1.0) < 1e-3:
        hits = {}
    ms_ = (MIN_CAPTION + 0.01) / s                    # v29 (Aras 1 Nov 19:49, p12 marks at 3.76 pt): the words the
    small = [w_ for w_ in words if w_[3] < ms_ - 1e-6]   # booklet writes print at 6 pt at least on the page
    if not hits and not gone and not small:
        if out is not None:
            out.extend(words)
        return src, pno_
    tmp = fitz.open()
    tmp.insert_pdf(src, from_page=pno_, to_page=pno_)
    pg = tmp[0]
    for r in gone:                                   # the middle of the line only: the lines above/below stay whole
        pg.add_redact_annot(fitz.Rect(r.x0, r.y0 + 0.3 * r.height, r.x1, r.y1 - 0.3 * r.height), fill=False)
    put = []
    for word, (den, size, col, bold) in hits.items():
        for r in pg.search_for(word, clip=clip):
            pg.add_redact_annot(r, fill=False)
            put.append((r, "1:{:,.0f}".format(den / s), max(size, ms_), col, bold))
    big = []                                         # v29: a renumbered mark under 6 pt on the page, set again bigger
    for w_ in small:
        wx, wy, wt, wsz, wb = w_
        fw_ = own_font(fitz, pg, wb)[1].text_length(wt, fontsize=wsz)
        r = fitz.Rect(wx, wy - 0.95 * wsz, wx + fw_, wy + 0.25 * wsz)
        pg.add_redact_annot(r, fill=False)
        big.append((fitz.Rect(wx, wy + 0.22 * ms_ - ms_, wx + fw_, wy + 0.22 * ms_), wt, ms_, 0x4A3F35, wb))
    put += big
    pg.apply_redactions(images=0, graphics=0, text=0)
    fonts = {}
    for r, txt, size, col, bold in put:              # v19 (MIRAQUA 28 Oct, G2): in the booklet's embedded Arial
        if bold not in fonts:
            fonts[bold] = own_font(fitz, pg, bold)[0]
        pg.insert_text((r.x0, r.y1 - 0.22 * size), txt, fontsize=size, fontname=fonts[bold],
                       color=((col >> 16 & 255) / 255.0, (col >> 8 & 255) / 255.0, (col & 255) / 255.0))
    if out is not None:                              # v26 closing: the marks still there, then the new scale words
        out.extend(w_ for w_ in words if not any(r.contains(fitz.Point(w_[0] + 0.1, w_[1] - 0.3 * w_[3]))
                                                 for r in gone) and w_ not in small)
        out.extend((r.x0, r.y1 - 0.22 * size, txt, size, bold) for r, txt, size, col, bold in put)
    return tmp, 0


def word_sizes(page, clip):
    return sorted(sp["size"] for b in page.get_text("dict", clip=clip)["blocks"] for ln in b.get("lines", [])
                  for sp in ln["spans"] if sp["text"].strip())


def std_scale(den):
    """v4 (Aras 26 Oct 06:35 "they need to be round numbers"): the first round scale at or above den. v12: within
    0.05 % counts as that scale (a drawing made at a round booklet scale, its sheet scale rounded to whole numbers)"""
    return next((d for d in STD_SCALES if d >= den - max(0.5, 5e-4 * den)), den)


def nearest_std(v):
    """v12: the round scale nearest v"""
    return min(STD_SCALES, key=lambda d: abs(d - v) / d)


STD_SCALES = (100, 200, 250, 500, 1000, 2000, 2500, 5000, 10000, 20000, 25000, 50000, 100000)
CAP_H, ROW_GAP = 5.0, 6.0                        # caption band under each panel, gap between rows (mm)
AREA = (ML, 30.0, PW - ML, FOOT_RULE - 3.0)        # where the panels go (mm)


# ------------------------------------------------------------------ pages
def frame_page(fitz, doc, typo, footer_band=True):
    """a new A3 page with the booklet's fonts. v26 (round 4, G-R4-1): opens the page's TextPage "pNN" (the booklet
    page number): its margins are half the page margins (the kicker sits at y 12), the footer band below FOOT_RULE
    holds only footer text and, on pages the booklet lays out (footer_band), is a block no drawing may enter"""
    pg = doc.new_page(width=PW * K, height=PH * K)
    pg.insert_font(fontname="FR", fontfile=typo.freg)
    pg.insert_font(fontname="FB", fontfile=typo.fbold)
    tp = TextPage("p%02d" % doc.page_count, (0.0, 0.0, PW, PH), y_down=True, pad=0.6,
                  margins=(ML * 0.5, MT * 0.5, ML * 0.5, MB * 0.5), footer_zone=(0.0, FOOT_RULE, PW, PH))
    if footer_band:
        tp.block((ML, FOOT_RULE, PW - ML, PH - MB * 0.5), "footer band")
    typo.tp = tp
    typo.tps.append(tp)
    return pg


def crop_block(typo, key, x, y, w, h):
    """v26 (round 4, G-R4-1): a crop (or its frame) placed at (x, y), w x h mm: a drawing block (blocks may touch,
    never overlap) and an obstacle no booklet word may enter (the crop's own words are its script's, checked there)"""
    if typo.tp is not None and w > 0 and h > 0:
        nm = key.split("/", 1)[-1] if key else "crop"
        typo.tp.block((x, y, x + w, y + h), nm)
        typo.tp.keep((x, y, x + w, y + h), "crop", nm)


_TOTAL = [0]       # revision 30 Oct (G2): the final page count of the booklet being built (cover + pages + sources)
_VARIANT = [None]  # revision 30 Oct (D1, D5): "a" / "b" while that PDF is built


def page_no(pno):
    """the page number, bottom right: v25 (round 3, G2) the number only, "7" (grid_page_counter; a text is kept)"""
    if isinstance(pno, str):
        return pno
    return grid_page_counter(pno)


def intro_layout(typo, spec):
    """revision 30 Oct (M1, G4): the page intro of PLAN (spec "intro", key words marked "*word*") as (lines, size,
    lead, x, first baseline, extra): beside the title in the title band when INTRO_MIN_COLS columns are free there,
    else under the rule, where `extra` mm is the room the panels give up. None without an intro."""
    txt = spec.get("intro")
    if not txt:
        return None
    measure = lambda s_, size_, bold_: typo.width(s_, size_, bold_)
    tw = typo.width(spec.get("title", ""), T["part"], True)
    c0 = next((c for c in range(2, COLS + 1) if colx(c) >= colx(1) + tw + GUT), COLS + 1)

    def intro(w):                                     # v26 (round 4, G-R4-2): >= 2 words on the last line (no widow):
        res = None                                    # the measure narrows by 4 % steps, at most 4 times, else logged
        for k_ in range(5):
            res = grid_intro(txt, w * (1.0 - 0.04 * k_), measure, 3, log=typo.issues if k_ == 4 else None)
            if len(res[0]) < 2 or len(res[0][-1]) >= 2:
                return res
        typo.issues.append(u"WIDOW in the intro of '%s': one word on its last line" % spec.get("title", ""))
        return res
    if COLS - c0 + 1 >= INTRO_MIN_COLS:
        x = colx(c0)
        lines, size, lead, _ = intro(PW - ML - x)
        y0 = 25.0 - 1.6 - lead * (len(lines) - 1)     # the last line sits on the band's lowest baseline
        return lines, size, lead, x, max(MT + 2.4, y0), 0.0
    lines, size, lead, _ = intro(PW - 2 * ML)
    return lines, size, lead, colx(1), 25.0 + BASE + 0.4, grid_snap_h(lead * len(lines) + 1.0)


def header(pg, typo, spec):
    part = PARTS.get(spec.get("part"), "")
    stage = STAGES.get(spec.get("stage"), "")         # v11: where the page sits in its theme's cycle
    typo.line(pg, (spec.get("part", "") + "   " + part + ("   ·   " + stage if stage else "")).upper(), colx(1), 12,
              T["kicker"], ACCENT, True)
    typo.line(pg, spec.get("title", ""), colx(1), 22, T["part"], INK, True)
    pg.draw_line((colx(1) * K, 25 * K), ((PW - ML) * K, 25 * K), color=hexrgb(RULE), width=0.25)
    il = intro_layout(typo, spec)                     # revision 30 Oct (M1, G4): 2-3 lines, key words bold
    if il:
        lines, size, lead, x, y0, extra = il
        for s_, x_, y_, b_ in grid_text_runs(lines, x, y0, lead):
            typo.line(pg, s_, x_, y_, size, INK, b_, group="intro", name="intro")
        return extra
    return 0.0


def intro_extra(typo, spec):
    """the mm the intro takes from the panel area (0 when it sits beside the title)"""
    il = intro_layout(typo, spec)
    return il[5] if il else 0.0


def foot_label(spec):
    part = PARTS.get(spec.get("part"), "")
    return (spec.get("part", "") + "  " + part).upper() if part else ""


def foot_x1(typo, spec):
    """v11: the legend band ends 5 mm before the footer's theme label (longer since v11), never under it"""
    lab = foot_label(spec)
    return PW - ML - 12 - (typo.width(lab, T["caption"], True) + 5.0 if lab else 22.0)


def footer(pg, typo, pno, spec, legend):
    """v19 (MIRAQUA 28 Oct, G1): the theme label and the page number (pno: a number, or the words to print there);
    the project and course lines are gone. v26 (round 4, G-R4-10, PALL.1): no rule line above the footer (FOOT_RULE
    stays the top of the footer band)"""
    no = page_no(pno)                                # revision 30 Oct (G2): "NN/total", computed
    typo.line(pg, no, PW - ML, FOOT_B2 + 0.6, T["pageno"], ACCENT, True, "R", role="footer", name="page number")
    lab_x = PW - ML - 12 - max(0.0, typo.width(no, T["pageno"], True) - typo.width("00", T["pageno"], True))
    if foot_label(spec):
        typo.line(pg, foot_label(spec), lab_x, FOOT_B2, T["caption"], INK2, True, "R", role="footer",
                  name="footer label")
    # legend: same place on every page (v19: from column 1 of the footer band), drawn samples + plain names
    x0, x1 = colx(FOOT_LEG_COL), foot_x1(typo, spec) - (PW - ML - 12 - lab_x)
    x, y = x0, FOOT_B1
    for it in legend or []:
        w = 4.0 + 1.5 + typo.width(it.get("label", ""), T["caption"]) + 5.0
        if x + w > x1:
            x, y = x0, y + 4.0
            if y > FOOT_B2 + 4.5:
                typo.issues.append("LEGEND TOO LONG p.%s" % pno)
                break
        legend_item(pg, typo, it, x, y, role="footer")
        x += w


def legend_item(pg, typo, it, x, y, role="label"):
    """one legend entry: a drawn sample (fill, line or dot) and its plain name, baseline y"""
    c = hexrgb(it.get("colour", INK))
    kind = it.get("kind", "fill")
    if kind == "line":
        pg.draw_line((x * K, (y - 1.2) * K), ((x + 4.0) * K, (y - 1.2) * K), color=c, width=it.get("width", 1.2))
    elif kind == "dot":
        pg.draw_circle(((x + 2.0) * K, (y - 1.2) * K), 1.3 * K, color=None, fill=c)
    elif kind in ("dash", "dashdot"):                    # MIRAQUA round: dashed samples (dashdot = the study area, G8)
        pat = "[3 0.8 0.4 0.8]" if kind == "dashdot" else "[1.6 0.9]"
        pg.draw_line((x * K, (y - 1.2) * K), ((x + 5.0) * K, (y - 1.2) * K), color=c, width=it.get("width", 1.2),
                     dashes="[%s] 0" % " ".join("%.2f" % (float(v) * K) for v in pat.strip("[]").split()))
    else:
        pg.draw_rect((x * K, (y - 2.6) * K, (x + 4.0) * K, (y + 0.2) * K), color=None, fill=c)
    typo.line(pg, it.get("label", ""), x + 5.5, y, T["caption"], INK, role=role, name="legend")


_PLACEHOLDERS = []   # v26 (round 4, P09.1, CHK1_2 F1.4): (page number, what is missing) of every placeholder drawn
_CUR_PNO = [0]       # v26: the page being built (build_variant sets it)


def placeholder(pg, typo, rect, text):
    """a labelled frame where a drawing is missing. v26 (round 4, P09.1): every one is counted; build_variant stops
    the run before the PDF is saved when there is any (log "placeholders N")"""
    _PLACEHOLDERS.append((_CUR_PNO[0], text))
    x, y, w, h = rect
    pg.draw_rect((x * K, y * K, (x + w) * K, (y + h) * K), color=hexrgb(FRAME), width=0.5, dashes="[2 2] 0")
    typo.line(pg, text, x + w / 2, y + h / 2, T["body"], INK2, False, "C", name="placeholder")


def sheet_page(fitz, doc, typo, pno, spec):
    """A whole A3 sheet page, as it is (a sheet of another size: scaled to fit, one scale)."""
    folder, _, name = spec["sheet"].partition("/")
    path = find_pdf(folder, name)
    pg = frame_page(fitz, doc, typo, footer_band=False)          # v26: the sheet fills the page, footer band too
    if not path or int(spec.get("page", 0)) >= len(sheet_doc(fitz, path)):
        header(pg, typo, spec)
        placeholder(pg, typo, (ML, AREA[1], PW - 2 * ML, AREA[3] - AREA[1]),
                    "%s · %s missing: run the script" % (SCRIPT_OF.get(folder, folder), name))
        footer(pg, typo, pno, spec, [])
        return "p.%d %s: MISSING %s" % (pno, spec["title"], name)
    sd, si = src_page(fitz, path, int(spec.get("page", 0)))     # v18: marks in the booklet's source numbers
    src = sd[si]
    f = min(PW * K / src.rect.width, PH * K / src.rect.height)
    pg.show_pdf_page(fitz.Rect(0, 0, src.rect.width * f, src.rect.height * f), sd, si)
    copy_words_put(typo, spec["sheet"], copy_words(path, int(spec.get("page", 0))), None, 0.0, 0.0, f,
                   allow=("sheet",))                 # v26 closing: its renumbered marks (on the sheet's own words)
    sheet_foot(fitz, pg, typo, pno, spec, src, f)
    return "p.%d %s: sheet %s page %d as it is%s" % (pno, spec["title"], os.path.basename(path),
                                                   int(spec.get("page", 0)) + 1, "" if f > 0.999 else " (x%.2f)" % f)


def sheet_foot(fitz, pg, typo, pno, spec, src, f):
    """v18 (Prompt 8: "footers and page numbers"): a whole-sheet page gets the booklet's page number in the footer's
    place, and its theme left of it where the sheet leaves that corner free; the log says when the number sits on
    the sheet's own words or drawing."""
    no = page_no(pno)                                # revision 30 Oct (G2): "NN/total", computed
    wn, lab = typo.width(no, T["pageno"], True), foot_label(spec)
    rn = (PW - ML - wn - 1.0, FOOT_B2 - 4.6, PW - ML + 0.5, FOOT_B2 + 1.4)
    wl = typo.width(lab, T["caption"], True) if lab else 0.0
    sh_ = max(0.0, wn - typo.width("00", T["pageno"], True))      # revision 30 Oct: the longer "NN/total"
    rl = (PW - ML - 12 - sh_ - wl - 1.0, FOOT_B2 - 2.8, PW - ML - 12 - sh_ + 0.5, FOOT_B2 + 1.0)
    try:
        big = 0.5 * abs(src.rect)                      # a sheet's white ground is not "content"
        boxes = [fitz.Rect(d["rect"]) for d in src.get_drawings() if abs(fitz.Rect(d["rect"])) < big]
        words = [fitz.Rect(w[:4]) for w in src.get_text("words")]
        boxes += words
    except Exception:
        boxes, words = [], []
    if typo.tp is not None:                            # v26 (G-R4-1): the sheet's own words, kept clear of the number
        for r in words:
            typo.tp.keep((r.x0 * f / K, r.y0 * f / K, r.x1 * f / K, r.y1 * f / K), "sheet", "sheet words")

    def free(r):
        R = fitz.Rect(r[0] * K / f, r[1] * K / f, r[2] * K / f, r[3] * K / f)
        return not any(b.intersects(R) for b in boxes)
    if not free(rn):
        typo.issues.append("PAGE NUMBER ON THE SHEET'S OWN CONTENT p.%d %s" % (pno, spec.get("title", "")))
    typo.line(pg, no, PW - ML, FOOT_B2 + 0.6, T["pageno"], ACCENT, True, "R", role="footer", name="page number")
    lab_ok = bool(lab) and free(rl)
    if lab_ok and typo.tp is not None:                 # v26: and clear of the sheet's words by the text test's measure
        b_ = typo.tp._box(lab, PW - ML - 12 - sh_, FOOT_B2, T["caption"], True, "R")
        lab_ok = not any(_tp_keep_hits(b_, K_, typo.tp.pad) for K_ in typo.tp.keeps)
    if lab_ok:
        typo.line(pg, lab, PW - ML - 12 - sh_, FOOT_B2, T["caption"], INK2, True, "R", role="footer",
                  name="footer label")


def wh(it):
    if it[3] is None and it[1] and it[1].get("slot"):  # v11: a frame for a later drawing keeps its planned size
        return it[1]["size_mm"]
    return (it[3].width / K, it[3].height / K) if it[3] is not None else (200.0, 60.0)


def fixed(it):
    """v15: a crop drawn for its width on the booklet page (block "bk_w") keeps that size (own_s) in a row"""
    return bool(it[1] and it[1].get("bk_w") and it[3] is not None)


def absent(it):
    """v19: a panel its script has not written (a frame for a later drawing is not absent)"""
    return it[3] is None and not (it[1] and it[1].get("slot"))


def row_items(r):
    """v19: the panels of a row that set its size: a missing panel beside drawn ones only takes the room they leave
    (its labelled frame there), so a note not yet written never shrinks the maps of p.07"""
    return [it for it in r if not absent(it)] or r


def scale_of(it, s_fit):
    """v19 (was panel_page's sc): the factor a panel prints at on a page of scale s_fit: drawn for its booklet width
    (v15): its own size; with a true scale: the round scale at or below s_fit (v4); else s_fit"""
    if fixed(it):
        return own_s(it)
    den = it[1].get("scale_den") if it[1] and it[3] is not None else None
    return den / std_scale(den / s_fit) if den else s_fit


def fit(rows, aw=None, ah=None, cap=None):
    """the one scale at which every row fits the panel area's width (v12: or aw mm) and all rows its height (v19: or ah
    mm: a key map's band takes its share); v15: the fixed crops (fixed) keep their own size, the others share the
    width and height they leave. v26: cap = the caption band under each row (default CAP_H; PLAN "cap_h")"""
    cap = CAP_H if cap is None else cap
    aw = aw if aw is not None else AREA[2] - AREA[0]
    ah = ah if ah is not None else AREA[3] - AREA[1]
    ws, hs, hfix = [], [], 0.0
    for r in rows:
        r = row_items(r)                               # v19
        free = [it for it in r if not fixed(it)]
        if free:
            ws.append((aw - GUT * (len(r) - 1) - sum(wh(it)[0] * own_s(it) for it in r if fixed(it))) /
                      sum(wh(it)[0] for it in free))
            hs.append(max(wh(it)[1] for it in free))
        else:
            hfix += max(wh(it)[1] * own_s(it) for it in r)
    if not hs:
        return 1.0
    return max(0.02, min(ws + [(ah - len(rows) * cap - (len(rows) - 1) * ROW_GAP - hfix) / sum(hs)]))


def own_s(it):
    """v12: the factor a crop prints at when it is drawn for a width on the booklet page (block "bk_w", mm): exactly
    its round scale when it has one"""
    w, h = wh(it)
    blk = it[1] or {}
    s = blk["bk_w"] / w if blk.get("bk_w") and it[3] is not None else 1.0
    den = blk.get("scale_den") if it[3] is not None else None
    return den / nearest_std(den / s) if den else s


def show(fitz, pg, typo, it, x, y, s, rep, missing, cap=True):
    """v12: one crop (or its labelled placeholder) at (x, y) mm, factor s, its caption under it; returns its height"""
    key, blk, path, clip = it
    w, h = wh(it)
    if clip is None:
        missing.add(key.partition("/")[0])
        placeholder(pg, typo, (x, y, w * s, h * s), "%s · %s" % (SCRIPT_OF.get(key.partition("/")[0], ""),
                                                                key.split("/")[1]))
        rep.append("%s MISSING" % key)
        return h * s
    bw = []
    src, pi = rescaled(fitz, path, int(blk.get("page", 0)), clip, s, blk.get("drop"), bw)
    pg.show_pdf_page(fitz.Rect(x * K, y * K, (x + w * s) * K, (y + h * s) * K), src, pi, clip=clip)
    crop_block(typo, key, x, y, w * s, h * s)          # v26 (G-R4-1)
    copy_words_put(typo, key, bw, clip, x, y, s)       # v26 closing: the booklet's own words in the copy
    if cap:
        c = renum(blk.get("caption", ""), key, blk, path)      # v18: its marks in the booklet's source numbers
        if blk.get("scale_den"):
            c = (c + " · " if c else "") + "1:{:,.0f}".format(blk["scale_den"] / s)
        typo.line(pg, c, x, y + h * s + 3.6, T["caption"], INK2, name="caption " + key.split("/", 1)[-1])
    ws = word_sizes(src[pi], clip)
    if ws:
        rep.append("%s words %.1f pt (smallest tenth %.1f)" % (key.split("/", 1)[1], ws[len(ws) // 2] * s,
                                                                ws[len(ws) // 10] * s))
    return h * s


def panel_page(fitz, doc, typo, pno, spec, rows, assets, missing):
    """rows of [(key, crop block, sheet path, clip)]: one scale for the page, the largest at which every row fits the
    width and all rows the height; a drawing with a true scale takes the round scale at or just below it (v4), so
    its printed scale is always round; each panel with its own words. v12: "side" panels at the right margin beside
    the rows (their own width), the page's legend under them; a "key" map in the title band at the right.
    v19 (MIRAQUA 28 Oct, P04.1, P14.1): the key map at scale 1.0 (drawn at its booklet size, 190 x <= 42 mm; never
    stretched) in a band under the title, the rows below it making room; beside the rows at the top right instead
    when that costs them less (a narrow map, or a fixed crop the band would push past the page).
    Revision 30 Oct (G1, M1, M2): each crop's legend is drawn under it, aligned to its left edge, in the columns its
    width holds (never in the footer band, never detached); the rows make room for it. The page intro (PLAN "intro",
    G4) sits beside the title or under it; the footer prints the page counter NN/total.
    v26 (round 4): PLAN "cap_h" = the caption band under each row (p19: 0, its headings are inside the crops), "flush"
    = rows start at the left margin; every crop is a drawing block of the page's TextPage (G-R4-1)."""
    cap = float(spec.get("cap_h", CAP_H))
    top0 = AREA[1] + intro_extra(typo, spec)          # revision 30 Oct (G4): an intro under the title takes its room
    aw, ah = AREA[2] - AREA[0], AREA[3] - top0
    side_it = spec.get("_side") or []
    # v19: a missing side panel does not set the column's width (its labelled frame takes the column)
    side_w = min(aw / 2.0, max([wh(it)[0] * own_s(it) for it in row_items(side_it)] or [0.0]))
    aw_r = aw - side_w - GUT if side_it else aw      # the rows' width
    key_it, key_at, kw, kh, ks = spec.get("_key"), None, 0.0, 0.0, 1.0
    if key_it is not None and key_it[3] is not None:
        kw, kh = wh(key_it)
        ks = min(1.0, aw / kw)
        kw, kh = kw * ks, kh * ks
        opts = [("band", aw_r, ah - kh - ROW_GAP)] + ([("beside", aw_r - kw - GUT, ah)]
                                                       if not side_it and aw_r - kw - GUT >= 60.0 else [])
        best = None
        for at, w_, h_ in opts:                      # least overrun first, then the largest scale; a tie: the band
            s_ = fit(rows, w_, h_, cap)
            hh = sum(max(wh(it)[1] * scale_of(it, s_) for it in row_items(r)) + cap for r in rows) + \
                ROW_GAP * (len(rows) - 1)
            ww = max(sum(wh(it)[0] * scale_of(it, s_) for it in row_items(r)) + GUT * (len(row_items(r)) - 1)
                     for r in rows)
            cost = (round(max(0.0, hh - h_, ww - w_), 1), -round(s_, 4))
            if best is None or cost < best[0]:
                best = (cost, at)
        key_at = best[1]
        if ks < 0.999:
            typo.issues.append("KEY MAP WIDER THAN THE PAGE p.%d: printed at %.0f %%" % (pno, 100.0 * ks))
        if kh > 42.5:
            typo.issues.append("KEY MAP TALLER THAN 42 mm p.%d (%.0f mm): the rows lose that height" % (pno, kh))
    ah_r = ah - (kh + ROW_GAP if key_at == "band" else 0.0)
    aw_r -= kw + GUT if key_at == "beside" else 0.0

    def row_leg(r, s_):                              # revision 30 Oct (G1): the legend band under a row's crops
        return max([legend_h(typo, crop_legend(it), wh(it)[0] * scale_of(it, s_)) for it in row_items(r)] or [0.0])
    s_fit = fit(rows, aw_r, ah_r, cap)
    for _ in range(3):                               # narrower crops hold fewer legend columns: settle the scale
        s_fit = fit(rows, aw_r, ah_r - sum(row_leg(r, s_fit) for r in rows), cap)
    leg_rows = [row_leg(r, s_fit) for r in rows]

    def sc(it):                                      # v4, v15 (v19: scale_of)
        return scale_of(it, s_fit)
    pg = frame_page(fitz, doc, typo)
    header(pg, typo, spec)
    rep = []
    y = y_top = top0 + (kh + ROW_GAP if key_at == "band" else 0.0)
    if key_it is not None and key_it[3] is None:
        rep.append("%s MISSING (key map left out)" % key_it[0])
    rws = [sum(wh(it)[0] * sc(it) for it in row_items(r)) + GUT * (len(row_items(r)) - 1) for r in rows]
    if key_at:                                       # v19: the key map, scale 1.0, no caption (no scale: a key map)
        kx = AREA[2] - kw if key_at == "beside" or side_it else \
            max(AREA[0], min(AREA[2], AREA[0] + (aw + max(rws)) / 2.0) - kw)   # band: flush with the rows' right edge
        show(fitz, pg, typo, key_it, kx, top0, ks, rep, missing, cap=False)
        rep.append("key map %s" % ("beside the rows" if key_at == "beside" else "in the band under the title"))
    # v18 (Prompt 8, rule 4 "no large empty areas"): rows that leave more than 40 mm of the height empty share it out
    # (old p.10: 91 mm under two maps the width holds at 1:10,000)
    free = ah_r - sum(max(wh(it)[1] * sc(it) for it in row_items(r)) + cap + lh + ROW_GAP
                      for r, lh in zip(rows, leg_rows)) + ROW_GAP
    pad = free / (len(rows) + 1) if len(rows) > 1 and free > 40.0 and not side_it else 0.0
    y += pad
    for r, rw, lh in zip(rows, rws, leg_rows):       # rows centred across the page
        pres = row_items(r)
        fill = [it for it in r if not any(it is p for p in pres)]    # v19: missing beside drawn panels
        x = AREA[0] + (0.0 if side_it or fill or key_at == "beside" or spec.get("flush") else
                       max(0.0, (aw - rw) / 2.0))
        rh = max(wh(it)[1] * sc(it) for it in pres)
        fw = (aw_r - rw - GUT * len(fill)) / len(fill) if fill else 0.0
        for it in r:
            key, blk, path, clip = it
            if any(it is f for f in fill):          # v19: its labelled frame in the room the drawn panels leave
                missing.add(key.partition("/")[0])
                rep.append("%s MISSING" % key)
                if fw >= 20.0:
                    placeholder(pg, typo, (x, y, fw, rh), "%s · %s" % (SCRIPT_OF.get(key.partition("/")[0], ""),
                                                                      key.split("/")[1]))
                    x += fw + GUT
                else:                                # v26 (P09.1): counted even where no frame fits
                    _PLACEHOLDERS.append((pno, "%s · %s (no room for its frame)" % (
                        SCRIPT_OF.get(key.partition("/")[0], ""), key.split("/")[1])))
                continue
            s = sc(it)
            w, h = wh(it)
            if clip is None and blk and blk.get("slot"):     # v11: frame for a drawing a later prompt makes
                placeholder(pg, typo, (x, y, w * s, h * s), blk["slot"])
                rep.append("frame: %s" % blk["slot"])
            elif clip is None:
                missing.add(key.partition("/")[0])
                placeholder(pg, typo, (x, y, w * s, h * s), "%s · %s" % (SCRIPT_OF.get(key.partition("/")[0], ""),
                                                                        key.split("/")[1]))
                rep.append("%s MISSING" % key)
            else:
                bw = []
                src, pi = rescaled(fitz, path, int(blk.get("page", 0)), clip, s, blk.get("drop"), bw)
                pg.show_pdf_page(fitz.Rect(x * K, y * K, (x + w * s) * K, (y + h * s) * K), src, pi, clip=clip)
                crop_block(typo, key, x, y, w * s, h * s)     # v26 (G-R4-1)
                copy_words_put(typo, key, bw, clip, x, y, s)  # v26 closing: the booklet's own words in the copy
                cap_t = renum(blk.get("caption", ""), key, blk, path)   # v18: the booklet's source numbers
                if blk.get("scale_den"):
                    cap_t = (cap_t + " · " if cap_t else "") + "1:{:,.0f}".format(blk["scale_den"] / s)
                    if round(blk["scale_den"] / s) not in STD_SCALES:
                        typo.issues.append("SCALE NOT ROUND p.%d %s: 1:%.0f" % (pno, key, blk["scale_den"] / s))
                if cap_t and cap < 4.0:              # v26: a page without caption bands prints no caption (logged)
                    typo.issues.append("CAPTION NOT PRINTED p.%d %s (the page has no caption band): %s" % (
                        pno, key, cap_t[:50]))
                else:
                    typo.line(pg, cap_t, x, y + h * s + 3.6, T["caption"], INK2, name="caption " + key.split("/")[-1])
                lg = crop_legend(it)                 # revision 30 Oct (G1): its legend under it, aligned to it
                if lg:
                    draw_legend_under(pg, typo, lg, x, y + h * s + cap - 0.6, w * s, pno)
                ws = word_sizes(src[pi], clip)
                if ws:
                    med, low = ws[len(ws) // 2] * s, ws[len(ws) // 10] * s
                    rep.append("%s words %.1f pt (smallest tenth %.1f)" % (key.split("/", 1)[1], med, low))
            x += w * s + GUT
        y += rh + cap + lh + ROW_GAP + pad
    if y - ROW_GAP > AREA[3] + 0.5:                  # v15: fixed crops are not shrunk: say when they overrun
        typo.issues.append("PAGE OVERRUNS ITS AREA p.%d by %.1f mm" % (pno, y - ROW_GAP - AREA[3]))
    if side_it:                                      # v12: beside the rows, right margin, top-aligned
        x1, ys = AREA[0] + max(rws) + GUT, y_top
        for it in side_it:
            w, h = wh(it)
            lg = crop_legend(it)                     # revision 30 Oct (G1): each side panel's legend under it
            s = max(0.05, min(own_s(it), (AREA[2] - x1) / w,
                              (AREA[3] - ys - CAP_H - legend_h(typo, lg, AREA[2] - x1)) / h))
            xs = AREA[2] - w * s
            ys += show(fitz, pg, typo, it, xs, ys, s, rep, missing) + CAP_H
            if lg:
                draw_legend_under(pg, typo, lg, xs, ys - 0.6, w * s, pno)
                ys += legend_h(typo, lg, w * s)
            if ys > AREA[3] + 0.5:
                typo.issues.append("SIDE COLUMN OVERRUNS ITS AREA p.%d by %.1f mm" % (pno, ys - AREA[3]))
    footer(pg, typo, pno, spec, [])
    return "p.%d %s: x%.2f · %s" % (pno, spec["title"], s_fit, "; ".join(rep))


def crop_legend(it):
    """revision 30 Oct (G1, M2): a crop's own legend entries, its marks in the booklet's source numbers ([] for a
    missing crop)"""
    if it is None or it[3] is None:
        return []
    out = []
    for e in (it[1] or {}).get("legend") or []:
        e = dict(e, label=renum(e.get("label", ""), it[0], it[1], it[2]))     # v18
        if all(e.get("label") != o.get("label") for o in out):
            out.append(e)
    return out


def legend_cols(typo, legend, w):
    """(columns, rows, column width mm) of a drawing's legend laid out under it, w mm wide"""
    if not legend:
        return 0, 0, 0.0
    lw = 6.0 + max(typo.width(e.get("label", ""), T["caption"]) for e in legend)
    ncol = max(1, min(len(legend), int((w + LEG_GAP) // (lw + LEG_GAP))))
    return ncol, -(-len(legend) // ncol), lw


def legend_h(typo, legend, w):
    """the height (mm) a drawing's legend takes under its caption, w mm wide"""
    n = legend_cols(typo, legend, w)[1]
    return n * LEG_ROW + 1.0 if n else 0.0


def draw_legend_under(pg, typo, legend, x, y, w, pno):
    """revision 30 Oct (G1): a drawing's legend under it from its left edge (y = the top of the legend band), in the
    columns its width holds: next to its drawing, aligned to it, never at the page bottom"""
    ncol, nrow, lw = legend_cols(typo, legend, w)
    if lw > w + 0.5:
        typo.issues.append("LEGEND WIDER THAN ITS DRAWING p.%d (%.0f mm, the drawing %.0f mm)" % (pno, lw, w))
    for i, e in enumerate(legend):
        legend_item(pg, typo, e, x + (i // nrow) * (lw + LEG_GAP), y + 3.0 + LEG_ROW * (i % nrow))


def panel_item(fitz, assets, key):
    """a plan key -> (key, block, path, clip) (v19: was expand's own item, now also for the P78.ALT page)"""
    if "||" in key:                                    # v15: "a||b": the first of these the scripts have written
        its = [panel_item(fitz, assets, k) for k in key.split("||")]
        return next((it for it in its if it[3] is not None), its[0])
    if key.startswith("slot|"):                        # v11: SLOT(text, w, h) of the plan
        _, w, h, text = key.split("|", 3)
        return (key, {"slot": text, "size_mm": (float(w), float(h))}, None, None)
    if _VARIANT[0]:                                    # revision 30 Oct (D1, D5): the _a / _b crop of this PDF where
        folder, _, bid = key.partition("/")             # its script wrote one, under the plan's own key
        vk = "%s_%s" % (bid, _VARIANT[0])
        if vk in ((assets.get(folder) or {}).get("blocks") or {}):
            _VARIANT_USED.add(folder + "/" + vk)
            return (key,) + tuple(panel_item_one(fitz, assets, folder + "/" + vk)[1:])
    return panel_item_one(fitz, assets, key)


_VARIANT_USED = set()   # revision 30 Oct: the _a / _b crops this build took (logged)


def panel_item_one(fitz, assets, key):
    """panel_item for one plain crop key (no "||", no slot, no variant)"""
    blk, path = resolve(assets, key)
    if not path:
        return (key, blk, None, None)
    page = sheet_doc(fitz, path)[int(blk.get("page", 0))]
    r = blk["rect_mm"]
    clip = fitz.Rect(r[0] * K, r[1] * K, r[2] * K, r[3] * K) & page.rect
    if not blk.get("scale_den"):                     # v4: a panel that states one scale in its words is to scale
        dens = set(int(m.group(1).replace(",", "")) for m in SCALE_WORD.finditer(page.get_text(clip=clip)))
        if len(dens) == 1:
            blk = dict(blk, scale_den=dens.pop())
    return (key, blk, path, clip)


def expand(fitz, spec, assets, typo=None):
    """One plan entry -> [(spec, rows)]: keys resolved to (key, block, path, clip); each panel whole (v4). typo (v25):
    measures the page intro, so the one-page test of or_pages knows the room the page really has."""
    def item(key):
        return panel_item(fitz, assets, key)
    rows = [[item(k) for k in r] for r in spec["rows"]]
    rows = [r for r in ([it for it in r if not (it[0] in OPTIONAL_KEYS and it[3] is None)] for r in rows) if r]
    spec = dict(spec, _side=[item(k) for k in spec.get("side", [])],          # v12: side panels, title-band key map
                _key=item(spec["key"]) if spec.get("key") else None)
    if not rows:
        return []
    if spec.get("optional") and all(it[3] is None for r in rows for it in r):
        return []
    if spec.get("alone") and fit(rows) < 0.75 * min(fit([r]) for r in rows):   # v7: together only if both stay big
        return [(dict(spec, title=t), [r]) for t, r in zip(spec["alone"], rows)]
    if spec.get("or_pages"):                         # v24 (round 2): one page while every row keeps ONE_PAGE_MIN
        # v25 (round 3, P18.1, D8): the room is the drawing area less the intro's (none when it sits beside the title);
        # crops drawn at 1:1 for the page ("bk_w") are never shrunk, so the page also goes on its or_pages when they
        # would need more height than it has (they would overrun the footer). Log tag: PLAN "log" (e.g. "p18-19")
        ah = AREA[3] - AREA[1] - (intro_extra(typo, spec) if typo is not None else ONE_PAGE_INTRO)
        cap = float(spec.get("cap_h", CAP_H))         # v26: p19 has no caption bands
        s1 = fit(rows, None, ah, cap)
        need = sum(max(wh(it)[1] * scale_of(it, s1) for it in row_items(r)) + cap for r in rows) + \
            ROW_GAP * (len(rows) - 1)
        tag = spec.get("log") or "'%s'" % spec["title"]
        if s1 < ONE_PAGE_MIN or need > ah + 0.5:
            why = ("on one page its rows would print at x%.2f (< x%.2f, labels under 6 pt)" % (s1, ONE_PAGE_MIN)
                   if s1 < ONE_PAGE_MIN else "on one page its 1:1 rows would need %.0f of %.0f mm" % (need, ah))
            _EXPAND_NOTES.append("%s: %d pages, %s" % (tag, len(spec["or_pages"]), why))
            return [pr for sp in spec["or_pages"] for pr in expand(fitz, sp, assets, typo)]
        _EXPAND_NOTES.append("%s: one page at x%.2f (rows %.0f of %.0f mm)" % (tag, s1, need, ah))
    return [(spec, rows)]


ONE_PAGE_MIN = 6.0 / 7.0    # v24: the sheets' smallest labels are 7 pt; the booklet's minimum is 6 pt
ONE_PAGE_INTRO = 12.0       # v24: room an intro under the title may take (mm), kept free when judging one page
_EXPAND_NOTES = []          # v24: which or_pages entries went on one page, logged


CONT_STEP = dict(group=6.0, part=5.6, stage=4.4, title=4.0)   # v26 (P01.1): contents line steps at x1 (mm): before a
CONT_STRETCH = 1.35                          # theme (not the first), after a theme, a stage, a title; stretched to fill
CAP = 0.716                                  # Arial's capital height (1467 / 2048 em): tops of capitals line up


def cover(pg, typo, pages):
    """the cover: left column title block, the collage and its text, names and date; right column the contents.
    v26 (round 4, P01.1, P01.2, D8): the collage (Data/COVER_IMG, COVER_IMG_W mm wide, never enlarged) under the title
    block, the approved text (COVER_TEXT, 4 lines at most, >= 2 words on the last) under it at the collage's width;
    names and date at the foot of the column (the date on the drawing area's last baseline, y 272); the contents
    start level with the top of the MIRAQUA capitals, list every page and the Sources page (pages: [(number, spec)];
    a spec without "part" is listed after a group gap, without a theme), the line steps stretched to fill the column"""
    import fitz as _fz
    x = colx(1)
    typo.line(pg, BOOK["course"].upper(), x, 16, T["kicker"], ACCENT, True, name="course")
    typo.line(pg, BOOK["hook"], x, 64, 48, ACCENT, True, name="hook")
    y = 82
    for ln in typo.wrap(BOOK["title"], 7 * COL + 6 * GUT, T["part"], True):
        typo.line(pg, ln, x, y, T["part"], INK, True, name="title"); y += 10
    ysub = y + 2
    typo.line(pg, BOOK["subtitle"], x, ysub, T["sub"], INK, name="subtitle")
    # the collage on the next baseline at least 8 mm under the subtitle (baseline grid: y = 12 + 4n)
    yi = 12.0 + BASE * -(-(ysub + 8.0 - 12.0) // BASE)
    path = os.path.join(BERGAMA, "Data", COVER_IMG)
    iw, ih = COVER_IMG_W, COVER_IMG_W * 810.0 / 1600.0
    if os.path.isfile(path):
        try:
            pm = _fz.Pixmap(path)
            ih = COVER_IMG_W * pm.height / float(pm.width)
            if pm.width < COVER_IMG_W / 25.4 * 150.0:
                typo.issues.append("COVER COLLAGE prints at %.0f dpi (%d px over %.0f mm)" % (
                    pm.width / (COVER_IMG_W / 25.4), pm.width, COVER_IMG_W))
            pm = None
            pg.insert_image(_fz.Rect(x * K, yi * K, (x + iw) * K, (yi + ih) * K), filename=path, keep_proportion=True)
            crop_block(typo, "cover collage", x, yi, iw, ih)
            typo.notes.append("cover collage %s: %.0f x %.0f mm at (%.0f, %.0f)" % (COVER_IMG, iw, ih, x, yi))
        except Exception as ex:
            typo.issues.append("COVER COLLAGE NOT READ (%s: %s)" % (type(ex).__name__, ex))
            placeholder(pg, typo, (x, yi, iw, ih), "cover collage %s unreadable" % COVER_IMG)
    else:
        placeholder(pg, typo, (x, yi, iw, ih), "%s missing: copy it into Downloads/Bergama/Data/" % COVER_IMG)
    # the cover text under the collage, at its width: 9.5 pt, 4 lines at most, no widow (the measure narrows 3 %
    # steps, then the size steps down to 9 pt, MIN_BODY)
    lines, size = None, T["body"]
    for size in (T["body"], 9.25, MIN_BODY):
        for k_ in range(4):
            lines = typo.wrap(COVER_TEXT, iw * (1.0 - 0.03 * k_), size)
            if len(lines[-1].split()) >= 2:
                break
        if len(lines) <= 4 and len(lines[-1].split()) >= 2:
            break
    if len(lines) > 4 or len(lines[-1].split()) < 2:
        typo.issues.append("COVER TEXT %d lines at %.2f pt (rule: 3-4 lines, >= 2 words on the last)" % (len(lines),
                                                                                                       size))
    lead = 4.4 * size / T["body"]
    yt = 12.0 + BASE * -(-(yi + ih + 4.0 + CAP * size * PT - 12.0) // BASE)
    for i, ln in enumerate(lines):
        typo.line(pg, ln, x, yt + i * lead, size, INK, group="cover text", name="cover text")
    ydate = 272.0
    yb = ydate - 8.0 - LEAD["body"] * (len(BOOK["names"]) - 1)
    if yb - CAP * T["body"] * PT < yt + (len(lines) - 1) * lead + 6.0:
        typo.issues.append("COVER: the names come within 6 mm of the cover text (%.1f mm)" % yb)
    for ln in BOOK["names"]:
        typo.line(pg, ln, x, yb, T["body"], INK, group="names", name="names"); yb += LEAD["body"]
    typo.line(pg, BOOK["date"], x, ydate, T["caption"], INK2, name="date")
    # contents, columns 9-12: theme (9.5 pt bold accent capitals), stage (8 pt bold CONT_STAGE small capitals), page
    # title (7.5 pt ink); page numbers (7.5 pt bold ink2, "7") right-aligned in one column, stages and titles after it.
    # v26: the CONTENTS kicker's capitals start level with the MIRAQUA capitals; every page listed (a title split over
    # two pages is listed twice: the 25 pages, D2); the steps CONT_STEP stretched by up to CONT_STRETCH to fill down to
    # the date's baseline (y 272)
    cx = colx(9)
    nx, tx = cx + CONT_NO_W, cx + CONT_NO_W + 3.0
    yk = 64.0 - CAP * 48 * PT + CAP * T["kicker"] * PT
    typo.line(pg, "CONTENTS", cx, yk, T["kicker"], ACCENT, True, name="contents kicker")
    rows, last, lstage = [], None, None
    for no, sp in pages:
        t = sp.get("title", "")
        if sp.get("part") is None:
            rows.append(("group", None, None))
            rows.append(("title", t, no))
            last, lstage = None, None
            continue
        if sp.get("part") != last:
            last, lstage = sp.get("part"), None
            if rows:
                rows.append(("group", None, None))
            rows.append(("part", (last + "  " + PARTS.get(last, "")).upper(), None))
        if sp.get("stage") != lstage:                  # v11: the cycle step, once where it starts
            lstage = sp.get("stage")
            rows.append(("stage", STAGES.get(lstage, ""), None))
        rows.append(("title", t, no))
    y0 = yk + 8.0 + CAP * CONT_PT["part"] * PT
    need = sum(CONT_STEP[k_] for k_, _, _ in rows[:-1])
    f = max(1.0, min(CONT_STRETCH, (ydate - y0) / need)) if need > 0 else 1.0
    cy = y0
    for i, (kind, t, no) in enumerate(rows):
        if kind == "part":
            typo.line(pg, t, cx, cy, CONT_PT["part"], ACCENT, True, name="contents theme")
        elif kind == "stage":
            small_caps(pg, typo, t, tx, cy, CONT_PT["stage"], CONT_STAGE, True)
        elif kind == "title":
            typo.line(pg, "%d" % no, nx, cy, CONT_PT["no"], INK2, True, "R", name="contents number")
            typo.line(pg, t, tx, cy, CONT_PT["title"], INK, name="contents title")
        if i < len(rows) - 1:
            cy += CONT_STEP[kind] * f
    typo.notes.append("contents: %d pages listed, line steps x%.2f, last line at %.0f mm" % (
        sum(1 for k_, _, _ in rows if k_ == "title"), f, cy))
    if cy > ydate + 0.5:
        typo.issues.append("CONTENTS RUN INTO THE FOOTER (%.0f mm)" % cy)


def small_caps(pg, typo, s, x, y, size, col, bold=False):
    """v25 (round 3, P01.1): s in small capitals from (x, y): capitals at size, lower-case letters as capitals at
    SMALL_CAPS x size (8 pt -> 6.4 pt, above GRID_MIN_PT)"""
    runs = []
    for ch in s or "":
        sm = ch.islower()
        if runs and runs[-1][0] == sm:
            runs[-1][1] += ch
        else:
            runs.append([sm, ch])
    g_ = "small caps %.1f %.1f" % (x, y)               # v26: the runs of one word are one text (G-R4-1)
    for sm, txt in runs:
        sz, t_ = size * SMALL_CAPS if sm else size, txt.upper()
        typo.line(pg, t_, x, y, sz, col, bold, group=g_, name="contents stage")
        x += typo.width(t_, sz, bold)


_F5_RX = []


def f5_rx():
    """v19 (F5): the plan's (F5_INTERNAL, F5_PUBLIC, F5_STRIP) patterns, compiled once"""
    if not _F5_RX:
        _F5_RX.extend([re.compile(p) for p in ps] for ps in (F5_INTERNAL, F5_PUBLIC, F5_STRIP))
        _F5_RX.append(re.compile(F5_STATUS))          # v20 (Aras 29 Oct 18:56): status words
    return _F5_RX


def split_top(t, sep=";"):
    """t split at sep outside brackets (the separators stay out)"""
    out, cur, depth = [], "", 0
    for ch in t:
        depth += (ch in "([") - (ch in ")]")
        if ch == sep and depth <= 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    return out + [cur]


def corn(t):
    """v19 (MIRAQUA 28 Oct, G11): "Corn (Mısır)", never maize, in the booklet's sources text; Wikimedia file names
    (File:... .jpg) and links stay as they are"""
    if not t or "aize" not in t:
        return t
    parts = re.split(r"(File:[^\n]*?\.(?:jpe?g|png|tiff?|gif|svg|webp)|\S*wikimedia\.org\S*)", t, flags=re.I)
    for k in range(0, len(parts), 2):
        p = re.sub(u"\\b[Mm]aize \\(Mısır\\)", u"Corn (Mısır)", parts[k])
        parts[k] = re.sub(r"\bmaize\b", "corn", re.sub(r"\bMaize\b", "Corn", p))
    return "".join(parts)


def public_src(t):
    """v19 (MIRAQUA 28 Oct, F5, Aras 28 Oct 11:38: "every [n] whose source is not public online (research cards,
    notes, decisions, chats, Begüm's page) goes"): a source text as the sources page prints it, or None when it cites
    our own working material (F5_INTERNAL) and names no public source (F5_PUBLIC). A kept text loses its ';' parts
    that only cite that material, and the brackets and register codes of F5_STRIP. Corn, not maize (G11).
    v20 (Aras 29 Oct 18:56, D13): every ';' part must name a public source (F5_PUBLIC), else it goes, our survey and
    our own readings and calculations too; None when no part is left; the status words (F5_STATUS) never print."""
    t = (t or "").strip()
    if not t or not F5_DROP:
        return corn(t)
    rin, rpub, rstrip, rstat = f5_rx()
    t = ";".join(s for s in split_top(t) if s.strip() and any(r.search(s) for r in rpub) and
                 re.sub(r"\W+", "", rstat.sub("", s)))
    if not t:
        return None
    for r in rstrip:
        t = r.sub("", t)
    t = re.sub(r"\s*,\s*(?=[;)]|$)", "", rstat.sub("", t))
    t = re.sub(r"\s{2,}", " ", t).strip(" ;,")
    return corn(t[:1].upper() + t[1:]) if t else None


def src_line(e):
    """"[n] text" -> the line the sources page prints (public_src), or None (F5)"""
    m = KEY_LINE.match(str(e or ""))
    if not m:
        return public_src(str(e or "")) or None
    t = public_src(m.group(2) or "")
    return "[%s] %s" % (m.group(1), t) if t else None


def plan_codes(assets):
    """v19 (MIRAQUA 28 Oct, P23.2 + N2): the technical source codes the masterplan's numbered list no longer prints,
    from its booklet results.json key "plan_codes" (a list of "n name: codes" lines, or of {"n", "name", "codes"}, or
    {n: codes / {"name", "codes"}}): ["n · name: codes", ...] with only the public ones (F5); [] when there are none"""
    a = assets.get(MP.rstrip("/")) or {}
    try:
        with open(os.path.join(a.get("_dir", ""), "results.json"), encoding="utf-8") as f:
            j_ = json.load(f)
    except Exception:
        return []
    d, ps = j_.get("plan_codes"), j_.get("plan_sources")
    if not d and isinstance(ps, dict):                    # masterplan v27 writes "plan_sources" (pl28_plan_sources)
        d = [{"n": m_.get("n"), "name": m_.get("name"),
              "codes": [s_.get("text", "") for s_ in m_.get("sources") or [] if s_.get("kind") == u"public online"]}
             for m_ in ps.get("markers") or []] + \
            [{"n": l_.get("id"), "name": l_.get("place") or u"left as it is", "codes": l_.get("sources") or []}
             for l_ in ps.get("left_as_is") or []]
    if isinstance(d, dict):
        d = [dict(v, n=k) if isinstance(v, dict) else {"n": k, "codes": v} for k, v in
             sorted(d.items(), key=lambda kv: (int(kv[0]) if str(kv[0]).isdigit() else 999, str(kv[0])))]
    out = []
    for e in d or []:
        if not isinstance(e, dict):
            t = public_src(str(e))
            if t:
                out.append(t)
            continue
        codes = e.get("codes") or e.get("source") or e.get("sources") or ""
        codes = [str(c) for c in codes] if isinstance(codes, (list, tuple)) else \
            [c for c in re.split(r"\s*[,;]\s*", str(codes)) if c]
        codes = [c for c in (public_src(c) for c in codes) if c]
        if codes:
            head = " · ".join(str(v) for v in (e.get("n"), e.get("name")) if v not in (None, ""))
            out.append((head + ": " if head else "") + ", ".join(codes))
    return out


def sheet_sources(fitz, assets):
    """[(heading, [entries])]: each sheet page's own source key. v10 (Aras 27 Oct: source footers go): first the
    key a script writes into its blocks.json "sheet_sources" ({page or "pdf#page": ["[1] ...", ...]}), else the
    key as the sheet prints it ("Sources by number: [1] ... [2] ..." or lines starting [n], visible or not).
    v19 (F5, G11): public online sources only, corn not maize (src_line)."""
    out, done = [], set()
    for pat in SOURCE_SHEETS:
        folder, _, name = pat.partition("/")
        keyed = (assets.get(folder) or {}).get("sheet_sources") or {}
        if keyed:
            if folder not in done:
                done.add(folder)
                for k in sorted(keyed, key=lambda k_: str(k_)):
                    ents = [e for e in (src_line(e_) for e_ in keyed[k] if e_) if e]
                    if ents:
                        out.append((SCRIPT_OF.get(folder, folder) + ("" if len(keyed) == 1 else " · page %d" % (int(k) + 1) if str(k).isdigit()
                                                                    else " · " + re.sub(r"\.pdf(#\d+)?$", "", str(k)).replace("_", " ")), ents))
            continue
        path = find_pdf(folder, name)
        if not path:
            continue
        d = sheet_doc(fitz, path)
        for i, page in enumerate(d):
            txt = []
            for b in page.get_text("blocks"):
                t = re.sub(r"\s+", " ", b[4]).strip()
                if "Sources by number:" in t:
                    txt.append(t.split("Sources by number:", 1)[1])
                elif re.match(r"\[\d+\] ", t):
                    txt.append(t)
            ents = [e for e in (src_line(e_.strip()) for e_ in re.split(r"\s(?=\[\d+\] )", " " + " ".join(txt))
                                if e_.strip()) if e]
            if ents:
                head = SCRIPT_OF.get(folder, folder) + (" · page %d" % (i + 1) if len(d) > 1 else "")
                if "axonometric" in name:
                    head += " · axonometric"
                out.append((head, ents))
    return out


# ------------------------------------------------------------------ v18 sources: one numbering for the whole booklet
MARK = re.compile(u"\\[(\\d{1,3}(?:\\s*[,–-]\\s*\\d{1,3})*)\\]")              # one mark: [3] [7,8] [3-5]
MARKS = re.compile(u"\\[\\d{1,3}(?:\\s*[,–-]\\s*\\d{1,3})*\\](?:\\s*\\[\\d{1,3}(?:\\s*[,–-]\\s*\\d{1,3})*\\])*")
KEY_LINE = re.compile(r"^\s*\[(\d{1,3})\]\s*(.*\S)?")
WMARK = re.compile(u"(\\s*)" + MARK.pattern)         # v19: a mark with the space before it (F5: both go)
_SRC = []        # v18: this run's Sources (main), read by renum


def renum(s, key, blk, path):
    """v18: s with its [n] marks in the booklet's source numbers (unchanged when Sources is not working)"""
    if not s or not _SRC or "[" not in s:
        return s
    return _SRC[0].renum(s, _SRC[0].key_for(key.partition("/")[0], path, int((blk or {}).get("page", 0))))


# v21 (Aras 30 Oct 06:20): the scale figure sets the pages draw from (common/figures.py, library/figures_A1/INDEX.md);
# the high-res silhouettes come from Data/assets_hires.json (hr_sources)
BK_ASSET_SOURCES = [
    u"Scale figures: Wijayarathna S., Architectural human figures sketches (set 1), https://sashx.gumroad.com/l/gSAgZ",
    u"Scale figures: studio_articulation, Sketchy Human Figures 2, "
    u"https://learnarchitecture.online/products/sketchy-human-figures-2",
    u"Scale figures: studio_articulation, Sketchy Human Figures 3, "
    u"https://learnarchitecture.online/products/sketchy-human-figures-3"]


# v25 (round 3, P23.1, N3 a+b, Aras 31 Oct 21:37): the height data of the water board's relief (crop wb_system): the
# course survey inside the site frame (the ONE named exception to public-only sources, N3 a) and Copernicus GLO-30
# outside it (its own source and credit lines, read from the Data file the water board reads; this copy if missing)
ELEV_SURVEY = u"Site survey, Bergama (course file), contours 1-10 m: the ground inside the site frame"
ELEV_DEM_FILE = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "Data", "bergama_dem_glo30.json")
ELEV_DEM = dict(
    source=u"Copernicus DEM GLO-30, ESA / DLR / Airbus, TanDEM-X 2011-2015; https://dataspace.copernicus.eu/"
           u"explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM",
    credit=u"© DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the "
           u"European Union and ESA; all rights reserved")


def elevation_sources(numbered):
    """v25 (P23.1, N3): (heading, [survey line, GLO-30 line]) for the sources page when a page shows the water board's
    wb_system (the relief), else None. Printed as they are: the survey line never goes through public_src (N3 a)."""
    title = next((sp.get("title", "") for _, sp, rows in numbered or [] if rows and
                  any(it[0] == WB + "wb_system" for r in rows for it in r)), None)
    if title is None:
        return None
    d = dict(ELEV_DEM)
    try:
        with open(ELEV_DEM_FILE, encoding="utf-8") as f_:
            j_ = json.load(f_)
        d.update((k, str(j_[k]).strip()) for k in ("source", "credit") if j_.get(k))
    except Exception:
        pass
    return (u"HEIGHT DATA OF THE RELIEF IN ‘%s’" % title.upper(),
            [ELEV_SURVEY, d["source"].rstrip(" ;") + u": the ground outside the site frame; " + d["credit"]])


def cutout_sources():
    """T4 30 Oct (M12, D1 a): one line per cutout source in Data/cutouts/cutouts.json (optional "source" of an entry:
    author / title / URL), once each, in key order; [] when the file or the field is missing"""
    p_ = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "Data", "cutouts", "cutouts.json")
    try:
        with open(p_, encoding="utf-8") as f_:
            d_ = json.load(f_).get("cutouts") or {}
    except Exception:
        return []
    out = []
    for key, ents in sorted(d_.items()):
        for e_ in (ents if isinstance(ents, list) else [ents]):
            t = str((e_ or {}).get("source") or "").strip() if isinstance(e_, dict) else ""
            if t and t not in out:
                out.append(t)
    return [u"Cutout: " + t for t in out]


class Sources(object):
    """v18 (Aras 27 Oct, Prompt 8: "every [n] used exists, none are unused, numbering follows the new order"): every
    [n] mark the pages show (sheet words inside each crop, captions, legend names), read in page order, takes one
    booklet number: first use first, one number per source text (the board's drawings and sections sheets share a
    key). v19 (G9): each place a sheet page is shown gets its own copy (strip_copy): its marks rewritten in place (same
    size, colour and baseline, in the booklet's Arial; a longer number set smaller where the words after it would be
    hit) and nothing outside that crop. v19 (F5): a source not public online takes no number; its marks go."""
    def __init__(self, fitz, assets):
        self.fz = fitz
        self.assets = assets    # v19: for the photo credits and the masterplan's plan_codes (N2)
        self.f5 = []            # v19 (F5): the marks taken out, for the log
        self.numbered = []      # v19: the booklet's pages (collect), for the sources page's headings
        self.keys = {}          # key id -> {n: source text}
        self.glob = {}          # (key id, n) -> booklet number
        self.by_text = {}       # source text (normalised) -> booklet number
        self.order = []         # [(booklet number, key id, n, part, page, folder)]
        self.used = {}          # (sheet path, page index) -> [folder, [clips]] (clip None = the whole page)
        self.kid = {}           # (folder, path, page index) -> key id
        self.first = {}         # T4 30 Oct (M12): folder -> first booklet page showing it (credits in page order)
        self.log, self.n_tight = [], 0
        for folder, a in sorted(assets.items()):
            for k, ents in sorted(((a or {}).get("sheet_sources") or {}).items(), key=lambda kv: str(kv[0])):
                k = str(k)
                if "#" in k:                           # the board: "<sheet pdf>#<page>"
                    pdf, _, p_ = k.rpartition("#")
                    kid = (folder, os.path.basename(pdf), int(p_) if p_.isdigit() else None)
                elif k.isdigit():                      # a page of the script's sheet (one key = all its pages)
                    kid = (folder, None, int(k))
                else:
                    kid = (folder, os.path.basename(k), None)
                self.keys[kid] = self.entries(ents or [])

    @staticmethod
    def entries(ents):
        """["[1] text", ...] -> {1: "text", ...} (an entry without its number takes its place in the list)"""
        out = {}
        for i, e in enumerate([str(e_).strip() for e_ in ents if e_ and str(e_).strip()]):
            m = KEY_LINE.match(e)
            out.setdefault(int(m.group(1)) if m else i + 1, ((m.group(2) or "") if m else e).strip())
        return out

    def parsed(self, path, i):
        """the key a sheet page prints itself ("Sources by number: [1] ..." or lines starting [n], visible or not)"""
        kid = ("sheet", path, i)
        if kid not in self.keys:
            txt = []
            for b in sheet_doc(self.fz, path)[i].get_text("blocks"):
                t = re.sub(r"\s+", " ", b[4]).strip()
                if "Sources by number:" in t:
                    txt.append(t.split("Sources by number:", 1)[1])
                elif re.match(r"\[\d+\] ", t):
                    txt.append(t)
            self.keys[kid] = self.entries(re.split(r"\s(?=\[\d+\] )", " " + " ".join(txt)))
        return kid if self.keys[kid] else None

    def key_for(self, folder, path, i):
        """the key the marks of this sheet page refer to: the script's own (blocks.json "sheet_sources": per sheet PDF
        and page, per page, or one for all), else the one the sheet prints (this page, else the one page of this
        sheet or of the folder's SOURCE_SHEETS sheet that has one); ("none", folder) when there is none"""
        ck = (folder, path, i)
        if ck not in self.kid:
            pdf = os.path.basename(path or "")
            kid = next((k for k in ((folder, pdf, i), (folder, pdf, None), (folder, None, i)) if self.keys.get(k)),
                       None)
            own = [k for k in self.keys if k[0] == folder and self.keys[k]]
            if kid is None and len(own) == 1:
                kid = own[0]
            if kid is None and path:
                kid = self.parsed(path, i)
                cands = [path] + [p for p in (find_pdf(folder, pat.partition("/")[2]) for pat in SOURCE_SHEETS
                                              if pat.partition("/")[0] == folder) if p and p != path]
                for p in cands if kid is None else []:
                    hits = [k for k in (self.parsed(p, j) for j in range(len(sheet_doc(self.fz, p)))) if k]
                    if len(hits) == 1:
                        kid = hits[0]
                        break
            self.kid[ck] = kid or ("none", folder)
        return self.kid[ck]

    @staticmethod
    def nums(s):
        """"3" / "7,8" / "3-5" -> [3] / [7, 8] / [3, 4, 5]"""
        out = []
        for part in s.split(","):
            ab = [x for x in re.split(u"[–-]", part) if x.strip()]
            try:
                a, b = int(ab[0]), int(ab[-1])
            except (ValueError, IndexError):
                continue
            out += list(range(a, b + 1)) if 0 <= b - a <= 12 else [a, b]
        return out

    def invisible(self, page):
        """rects of the page's invisible words (render mode 3: e.g. the water balance's source key)"""
        try:
            return [self.fz.Rect(s_["bbox"]) for s_ in page.get_texttrace() if s_.get("type") == 3]
        except Exception:
            return []

    def lines_in(self, page, clip, inv=None):
        """the visible lines of words inside clip (None = the page) holding a "[", outside any printed source key
        (v19: inv = the page's invisible words when read before, page_text)"""
        inv, out = self.invisible(page) if inv is None else inv, []
        for b in page.get_text("dict", clip=clip)["blocks"]:
            lines = [("".join(s_["text"] for s_ in ln["spans"]), self.fz.Rect(ln["bbox"])) for ln in b.get("lines", [])]
            if any("Sources by number:" in t for t, _ in lines):
                continue
            out += [t for t, r in lines if "[" in t and not any(r.intersects(v) for v in inv)]
        return out

    def use(self, kid, n, part, pno, folder):
        if (kid, n) in self.glob:
            return
        t = (self.keys.get(kid) or {}).get(n)
        if t and public_src(t) is None:                # v19 (F5): not public online: no number, its marks go
            self.glob[(kid, n)] = 0
            self.f5.append(u"p.%02d [%d] (%s): %s" % (pno, n, SCRIPT_OF.get(folder, folder), t[:110]))
            return
        if not t:                                      # v20 (D13): no entry = nothing public to print: the mark goes
            self.glob[(kid, n)] = 0
            self.log.append("SOURCE MARK WITHOUT AN ENTRY p.%d [%d] (%s): taken off the page" % (
                pno, n, SCRIPT_OF.get(folder, folder)))
            return
        norm = re.sub(r"\W+", " ", t).strip().lower() if t else None
        if norm and norm in self.by_text:              # the same source under another sheet's number
            self.glob[(kid, n)] = self.by_text[norm]
            return
        g = len(self.order) + 1
        self.glob[(kid, n)] = g
        if norm:
            self.by_text[norm] = g
        self.order.append((g, kid, n, part, pno, folder))

    def collect(self, numbered):
        """pass 1: the marks of every page in page order -> booklet numbers; which parts of which sheet pages show"""
        self.numbered = numbered
        for pno, sp, rows in numbered:
            its = []
            if rows is None:
                folder, _, name = sp["sheet"].partition("/")
                path, i = find_pdf(folder, name), int(sp.get("page", 0))
                if path and i < len(sheet_doc(self.fz, path)):
                    its.append((folder, path, i, None, "", []))
            else:
                for key, blk, path, clip in [it for r in rows for it in r] + list(sp.get("_side") or []) + \
                        ([sp["_key"]] if sp.get("_key") else []):
                    if clip is not None:
                        its.append((key.partition("/")[0], path, int(blk.get("page", 0)), clip,
                                    blk.get("caption") or "", [e.get("label", "") for e in blk.get("legend") or []]))
            for folder, path, i, clip, cap, labels in its:
                self.used.setdefault((path, i), [folder, []])[1].append(clip)
                self.first.setdefault(folder, pno)
                kid = self.key_for(folder, path, i)
                inv = page_text(self.fz, path, i)[1]   # v19: read once per sheet page, not once per crop
                for t in self.lines_in(sheet_doc(self.fz, path)[i], clip, inv) + [cap] + labels:
                    for m in MARK.finditer(t):
                        for n in self.nums(m.group(1)):
                            self.use(kid, n, sp.get("part"), pno, folder)

    def renum(self, s, kid):
        """s with its marks in the booklet's numbers; v19 (F5): a mark whose sources all are not public online goes
        with the space before it, a mark with some keeps the others"""
        def one(m):
            ns = [self.glob.get((kid, n)) for n in self.nums(m.group(2))]
            if not ns or None in ns:
                return m.group(0)
            ns = sorted(set(n for n in ns if n))
            if not ns:
                return ""
            if len(ns) > 2 and ns[-1] - ns[0] == len(ns) - 1:
                return m.group(1) + "[%d-%d]" % (ns[0], ns[-1])
            return m.group(1) + "[%s]" % (", " if ", " in m.group(2) else ",").join(str(n) for n in ns)
        return WMARK.sub(one, s)

    def build(self):
        """pass 2 (v19, G9): the copy of every place a sheet page is shown (strip_copy), made now, its marks renumbered"""
        for (path, i), (folder, clips) in self.used.items():
            for clip in clips:
                copy_of(self.fz, path, i, clip, self)  # v26 closing: with the words it writes (_COPY_PUT)

    def groups(self):
        """[(theme heading, ["[n] text", ...])] in booklet order, for sources_page. v19: public online sources only (F5)
        and corn, not maize (G11) (public_src); then (N2) the photo credits and data notes of the sheets shown that no
        page cites by a number (plan ALWAYS_LIST; blocks.json "photo_credits"), once each, and the technical source
        codes the masterplan's list no longer prints (plan_codes), headed by that page's title (N1)"""
        def ck(t):                                    # one photo = one credit (its Commons page id)
            m = re.search(r"curid=(\d+)", t or "")
            return ("id", m.group(1)) if m else ("t", re.sub(r"\W+", " ", t or "").strip().lower())
        out, last, printed = [], object(), set()
        for g, kid, n, part, pno, folder in self.order:
            if part != last:
                last = part
                out.append(((part + "  " + PARTS.get(part, "")).upper() if part else u"COVER", []))
            t = (self.keys.get(kid) or {}).get(n)
            t = public_src(t) if t else t
            printed.add(ck(t))
            out[-1][1].append(u"[%d] %s" % (g, t))
        pats, texts, extra = [re.compile(p) for p in ALWAYS_LIST], [], []
        for kid in sorted(set(self.kid.values()), key=str):
            texts += [t for n, t in sorted((self.keys.get(kid) or {}).items())
                      if (kid, n) not in self.glob and t and any(p.search(t) for p in pats)]
        shown = set(f for f, _ in self.used.values())
        # T4 30 Oct (M12): the scripts' photo credits in booklet page order (first page each sheet shows on), so the
        # p.20 photo credits moved off the heritage map print here with the others
        for f_, a in sorted(self.assets.items(), key=lambda kv: (self.first.get(kv[0], 999), str(kv[0]))):
            texts += [str(t) for t in (a or {}).get("photo_credits") or [] if t]
            try:                                      # T4 (M12): photo_credits.json beside blocks.json (masterplan
                with open(os.path.join((a or {}).get("_dir") or "", "photo_credits.json"), encoding="utf-8") as fh:
                    texts += [str(t) for t in json.load(fh).get("photo_credits") or [] if t]   # senses photos)
            except Exception:
                pass
            if f_ in shown:                           # v20 (WO-T5-1): registered public sources and photo credits
                texts += [str((v or {}).get("text") or "") for k, v in sorted(((a or {}).get("sources") or {}).items())
                          if re.match(ALWAYS_KEYS, str(k)) and isinstance(v, dict)]
        for t in texts:
            t = public_src(t)
            if t and ck(t) not in printed:
                printed.add(ck(t))
                extra.append(t)
        if extra:
            out.append((u"PHOTO CREDITS AND DATA NOTES", extra))
        elev = elevation_sources(self.numbered)       # v25 (P23.1, N3): the relief's height data
        if elev:
            out.append(elev)
        codes = plan_codes(self.assets)
        if codes:
            title = next((sp.get("title", "") for _, sp, rows in self.numbered if rows and
                          any(it[0] == MP + "mp_plan" for r in rows for it in r)), u"Masterplan: an ecological corridor")
            out.append((u"SOURCES OF THE NUMBERED PLACES IN ‘%s’" % title.upper(), codes))
        assets = [public_src(t) or corn(t) for t in hr_sources() + BK_ASSET_SOURCES + cutout_sources()]
        if assets:                                    # v21 (Aras 30 Oct 06:20): every asset source once, under ASSETS
            out.append((u"ASSETS", assets))
        return out

    def report(self):
        kids = set(self.kid.values())
        left = sum(1 for k in kids for n in (self.keys.get(k) or {}) if (k, n) not in self.glob)
        return ("sources: %d cited, numbered in page order (one number per source); %d entries of the scripts' keys "
                "for these sheets not cited on any page, left out; %d not public online, their marks taken off the "
                "pages (F5, listed at the end of this log); %d marks set smaller to fit" % (
                    len(self.order), left, len(self.f5), self.n_tight))


def sources_page(new_page, typo, pno, groups, head=u"Sources, by sheet"):
    """All sources, each sheet's own key (v18: each theme) under its name, three columns, the type size lowered step by
    step from 7.5 pt until everything fits on one page (Aras 25 Oct 21:54). v26 (round 4, P23.1, PLAN §2 technical
    call): never below the 6 pt minimum (G-R4-1): when one page cannot hold them at 6 pt they run on over a second
    (third ...) page, logged. new_page() -> a new booklet page; returns how many pages were made."""
    cols = [colx(1), colx(5), colx(9)]
    y0, y1 = 31.0, FOOT_RULE - 3.0
    w = 4 * COL + 3 * GUT
    items = []
    for head_, ents in groups:
        items.append((True, head_))
        items += [(False, e) for e in ents]

    def layout(size, max_pages):
        """[(page index, column, first baseline, lines, bold)] or None when max_pages pages cannot hold them"""
        lead, gap = size * PT * 1.18, size * PT * 0.45
        out, pi, ci, y = [], 0, 0, y0 + size * PT
        for bold, t in items:
            lines = typo.wrap(t, w - 1.5, size, bold)
            need = len(lines) * lead + (gap * 2 if bold else 0)
            if y + need - lead > y1:
                ci, y = ci + 1, y0 + size * PT
                if ci >= len(cols):
                    pi, ci = pi + 1, 0
                    if pi >= max_pages:
                        return None
            if bold and y > y0 + size * PT + 0.1:
                y += gap * 2
            out.append((pi, ci, y, lines, bold))
            y += len(lines) * lead + gap
        return out, lead
    size, res = T["caption"], None
    while size >= MIN_CAPTION - 1e-6:
        res = layout(size, 1)
        if res:
            break
        size = round(size - 0.25, 2)
    if not res:
        size = MIN_CAPTION
        res = layout(size, 99)
        typo.notes.append("sources on %d pages at %.2f pt (one page would need less than the %.1f pt minimum)" % (
            1 + max(r[0] for r in res[0]), size, MIN_CAPTION))
    rows, lead = res
    n_pages = 1 + max([r[0] for r in rows] or [0])
    for k_ in range(n_pages):
        pg = new_page()
        typo.line(pg, "SOURCES", colx(1), 12, T["kicker"], ACCENT, True, name="kicker")
        typo.line(pg, head + (u" (continued)" if k_ else u""), colx(1), 22, T["part"], INK, True, name="title")
        pg.draw_line((colx(1) * K, 25 * K), ((PW - ML) * K, 25 * K), color=hexrgb(RULE), width=0.25)
        for pi, ci, y, lines, bold in rows:
            if pi != k_:
                continue
            for j_, ln in enumerate(lines):         # one column is one text block (its lines are 1.18 x the size apart)
                typo.line(pg, ln, cols[ci] + (1.5 if j_ else 0.0), y + j_ * lead, size, ACCENT if bold else INK, bold,
                          group="sources %d.%d" % (k_, ci), name="sources")
        footer(pg, typo, pno + k_, {"part": None}, [])
    if size < T["caption"]:
        typo.notes.append("sources set at %.2f pt (%d entries, %d page%s)" % (size, len(items), n_pages,
                                                                            "s" if n_pages > 1 else ""))
    return n_pages


def flex_order(plan, typo):
    """v17: a spread opens on a left (even) page: when it would open on a right page and the page before it is marked
    flex, that page goes after the spread instead (plan index i = page i + 2: page 1 is the cover)."""
    for i in range(1, len(plan) - 1):
        if plan[i][0].get("spread") == "L" and i % 2 and plan[i - 1][0].get("flex"):
            typo.notes.append("page '%s' moved after the spread '%s' so the spread opens on a left page" % (
                plan[i - 1][0].get("title", ""), plan[i][0].get("title", "")))
            n = 2 if plan[i + 1][0].get("spread") == "R" else 1
            return plan[:i - 1] + plan[i:i + n] + [plan[i - 1]] + plan[i + n:]
    return plan


def pno_of(numbered, key=None, sheet=None, page=0):
    """v19: the page number (2 digits) of the page showing crop key, or sheet page; "" when no page does"""
    for pno, sp, rows in numbered:
        if (key and rows and any(it[0] == key for r in rows for it in r)) or \
                (sheet and rows is None and sp.get("sheet") == sheet and int(sp.get("page", 0)) == page):
            return "%d" % pno                       # v25 (G2): the number only
    return ""


def page_checks(doc, numbered, typo):
    """v19 (MIRAQUA 28 Oct): read back from the finished pages. G10 ("one number, one calculation"): a figure of the
    plan's FIGURE_CHECKS printed two ways on the booklet's pages (e.g. the frame 150.5 ha on p.02, 151 ha on p.21)
    is logged with every page of each value. N1: the cross-references the pages print still point right after the
    renumbering: "NEXT <theme letter> <theme>" names the next theme, "see '<title>'" a page title; a reference by
    page number is logged (pages are named by their titles). The sources page and the cover are not read."""
    last = len(doc)
    texts = {}
    for i, pg in enumerate(doc):
        if 0 < i < last - 1:
            try:
                texts[i + 1] = re.sub(r"\s+", " ", pg.get_text("text"))
            except Exception:
                texts[i + 1] = ""
    for name, unit, pats in FIGURE_CHECKS:
        seen = {}
        for pno, t in texts.items():
            for p in pats:
                for m in re.finditer(p, t):
                    seen.setdefault(m.group("v").replace(",", ""), set()).add(pno)
        if len(seen) > 1:
            typo.issues.append(u"ONE FIGURE, TWO VALUES (G10) %s: %s" % (name, u" · ".join(
                u"%s %s (p.%s)" % (v, unit, ", ".join("%02d" % p for p in sorted(ps))) for v, ps in sorted(seen.items()))))
        elif seen and len(list(seen.values())[0]) > 1:
            v, ps = list(seen.items())[0]
            typo.notes.append(u"G10 %s: %s %s on p.%s, the same everywhere" % (name, v, unit,
                                                                            ", ".join("%02d" % p for p in sorted(ps))))
    titles = dict((re.sub(r"\W+", " ", sp.get("title", "")).strip().lower(), pno) for pno, sp, _ in numbered)
    part_of = dict((pno, sp.get("part")) for pno, sp, _ in numbered)
    n_ok = 0
    for pno, t in sorted(texts.items()):
        for m in re.finditer(u"NEXT\\W{0,4}([A-E])\\b", t):
            nxt = next((part_of[p] for p in sorted(part_of) if p > pno and part_of[p] != part_of.get(pno)), None)
            if m.group(1) != nxt:
                typo.issues.append(u"CROSS-REFERENCE p.%02d: \"NEXT %s\", but the next theme is %s" % (
                    pno, m.group(1), nxt or "none"))
            else:
                n_ok += 1
        for m in re.finditer(u"(?i)\\bsee\\s+[‘'\"“]([^’'\"”]{3,80})[’'\"”]", t):
            if re.sub(r"\W+", " ", m.group(1)).strip().lower() not in titles:
                typo.issues.append(u"CROSS-REFERENCE p.%02d: see '%s', but no page has that title" % (pno, m.group(1)))
            else:
                n_ok += 1
        for m in re.finditer(r"(?i)\b(?:pp?\.|page) ?\d{1,2}\b(?! ?of\b)", t):
            typo.issues.append(u"CROSS-REFERENCE BY NUMBER p.%02d: \"%s\" (pages are renumbered: name the page by its "
                               u"title)" % (pno, m.group(0)))
    if n_ok:
        typo.notes.append("cross-references checked (N1): %d point to the right theme or title" % n_ok)


# ------------------------------------------------------------------ main
def main():
    """v23: one booklet in style a (BOOK_VARIANTS = ("a",)), each crop taken as its _a version where its script still
    writes one (else the crop itself)"""
    t0 = time.time()
    rows = []
    for v in BOOK_VARIANTS:
        rows += build_variant(v)
    rows += drop_old_alt()                       # v23: the two-booklet PDFs of v22 go
    rows += bg_tidy_output(OUT_FOLDER, BK_ROOT)  # v10 (27 Oct): output/ = the PDF only, leftovers to cached/booklet/
    rows.append("%s %s, %.1f s" % (GH_LABEL, VERSION, time.time() - t0))
    return "\n".join(rows)


def variant_pdf(v):
    """the PDF name: v23 (one booklet in style a) always Bergama_booklet_A3.pdf"""
    return PDF_NAME


def drop_old_alt():
    """v23: delete v22's Bergama_booklet_A3_alt_a.pdf / _alt_b.pdf from output/bergama_booklet/ (one log line)"""
    root, ext = os.path.splitext(PDF_NAME)
    gone, kept = [], []
    for v_ in ("a", "b"):
        f = os.path.join(OUT_DIR, "%s_alt_%s%s" % (root, v_, ext))
        if os.path.exists(f):
            try:
                os.remove(f)
                gone.append(os.path.basename(f))
            except Exception as ex:
                kept.append("%s (%s, open in a viewer?)" % (os.path.basename(f), type(ex).__name__))
    return (["old booklets deleted: " + ", ".join(gone)] if gone else []) + \
           (["OLD BOOKLET NOT DELETED: " + ", ".join(kept)] if kept else [])


def build_variant(variant):
    """one booklet PDF (variant "a" / "b", None = the plain one): its log rows"""
    import fitz                                   # PyMuPDF
    os.makedirs(OUT_DIR, exist_ok=True)
    _VARIANT[0] = variant
    _VARIANT_USED.clear()
    tp_log_lines()                                # v26: no text log lines left from an earlier run
    assets = load_assets()
    typo = Typo(fitz)
    doc = fitz.open()
    plan = []
    del _EXPAND_NOTES[:]
    for spec in PAGES:
        if spec.get("sheet"):
            plan.append((spec, None))
        elif not FRAME_PAGES and all(k.startswith("slot|") for r in spec.get("rows", []) for k in r):
            typo.notes.append("page '%s' left out: its drawings are not made yet (frames only; PLAN FRAME_PAGES)" %
                              spec.get("title", ""))           # v18 (Prompt 8): no empty frame page in the booklet
        else:
            plan += expand(fitz, spec, assets, typo)
    typo.notes += _EXPAND_NOTES                     # v24: one page or two (p8 street sections, p18 + p19)
    plan = flex_order(plan, typo)
    numbered = [(i + 2, sp, rows) for i, (sp, rows) in enumerate(plan)]   # page 1 = cover + contents
    _TOTAL[0] = len(numbered) + 2                   # revision 30 Oct (G2): cover + pages + sources, the counter's total
    _COPY.clear()
    _COPY_PUT.clear()
    _PAGE_TXT.clear()
    G9_STATS.update(copies=0, lines=0, chars=0, images=0, failed=[])
    del _SRC[:]
    srcs = Sources(fitz, assets)                    # v18: one source numbering for the booklet, in page order
    try:
        srcs.collect(numbered)
        srcs.build()
        _SRC.append(srcs)
        typo.notes.append(srcs.report())
        typo.issues += srcs.log
    except TextError:                               # v26 closing: a source mark that cannot fit at 6 pt stops
        raise                                       # the booklet (never taken for a failed renumbering)
    except Exception as ex:
        _COPY.clear()
        _COPY_PUT.clear()
        typo.issues.append("SOURCES NOT RENUMBERED (%s: %s): marks and sources page by sheet, as before v18" %
                           (type(ex).__name__, ex))
    del _PLACEHOLDERS[:]
    typo.tps, typo.tp = [], None
    _CUR_PNO[0] = 1
    cover(frame_page(fitz, doc, typo), typo, [(n, sp) for n, sp, _ in numbered] +
          [(len(numbered) + 2, {"title": u"Sources", "part": None})])     # v26: the Sources page listed too
    missing, rep = set(), []
    for pno, sp, rows in numbered:                   # v11: a spread opens on a left (even) page
        if sp.get("spread") == "L" and pno % 2:
            typo.issues.append("SPREAD STARTS ON A RIGHT PAGE p.%d %s" % (pno, sp.get("title", "")))
    for pno, sp, rows in numbered:
        _CUR_PNO[0] = pno
        rep.append(sheet_page(fitz, doc, typo, pno, sp) if rows is None else
                   panel_page(fitz, doc, typo, pno, sp, rows, assets, missing))
    _CUR_PNO[0] = len(numbered) + 2
    n_src = sources_page(lambda: frame_page(fitz, doc, typo), typo, len(numbered) + 2,
                         *((srcs.groups(), u"Sources, in page order") if _SRC else (sheet_sources(fitz, assets),)))
    _TOTAL[0] = len(numbered) + 1 + n_src           # v26: the Sources may run over more than one page
    page_checks(doc, numbered, typo)                 # v19: G10 figures, N1 cross-references
    typo.notes.append("G9: %d crops each shown from its own copy of its sheet page; taken out of the copies: %d lines "
                      "and %d letters of words outside them, %d images wholly outside, the line art lying wholly "
                      "outside%s" % (G9_STATS["copies"], G9_STATS["lines"], G9_STATS["chars"], G9_STATS["images"],
                                     "" if G9_LINE_ART else " (off: G9_LINE_ART)"))
    typo.issues += ["G9 COPY FAILED, the whole sheet page shown: %s" % f for f in G9_STATS["failed"]]
    # v26 (round 4, P09.1 + G-R4-1): placeholders and text collisions stop the run here, before the PDF is saved
    stop = []
    log_ph = "placeholders %d" % len(_PLACEHOLDERS)
    if _PLACEHOLDERS:                               # v29 (Aras 1 Nov 19:49): saved anyway, with an orange warning
        _bk_warn("booklet saved with %d placeholder frame%s: %s (run the scripts that make them, then the booklet "
                 "again)" % (len(_PLACEHOLDERS), "" if len(_PLACEHOLDERS) == 1 else "s",
                             "; ".join("p%02d %s" % (n_, t_) for n_, t_ in _PLACEHOLDERS)))
    if False:
        stop.append("placeholders %d: %s (run the scripts that make them, then the booklet again)" % (
            len(_PLACEHOLDERS), "; ".join("p%02d %s" % (n_, t_) for n_, t_ in _PLACEHOLDERS)))
    hits = text_test(typo)
    if hits:
        stop.append("text collisions on %d page%s: %s" % (len(hits), "" if len(hits) == 1 else "s", " | ".join(hits)))
    if stop:
        doc.close()
        raise RuntimeError("booklet not saved: " + " || ".join(stop) + " || " + "; ".join(tp_log_lines()))
    doc.subset_fonts()
    out = os.path.join(OUT_DIR, variant_pdf(variant))
    doc.save(out, garbage=3, deflate=True)
    n = doc.page_count
    doc.close()
    if n != _TOTAL[0]:
        typo.issues.append("PAGE COUNTER: %d pages built, the counter says %d" % (n, _TOTAL[0]))
    rows = ["%s  %s  (%d pages, font %s)" % (out, time.strftime("%H:%M:%S"), n, typo.fam),
            "trigger: %s" % (TRIG_WHY[0] or "run outside Grasshopper"), log_ph]
    rows += tp_log_lines()                            # v26: "overlap pNN checked n, collisions 0", every page
    if variant:
        rows.append("variant %s: %d crops taken as their _%s version%s" % (
            variant, len(_VARIANT_USED), variant, (": " + ", ".join(sorted(_VARIANT_USED))) if _VARIANT_USED else ""))
    for name in sorted(assets):
        rows.append("assets %s: %s" % (name, assets[name].get("_error") or assets[name]["_time"]))
    for m in sorted(missing):
        rows.append("MISSING drawings of %s: placeholders left" % SCRIPT_OF.get(m, m))
    rows += rep + typo.notes
    rows += typo.issues[:40] + (["... %d more" % (len(typo.issues) - 40)] if len(typo.issues) > 40 else [])
    if _SRC and _SRC[0].f5:                       # v19 (F5): Aras's list of figures left without a public source
        rows += ["F5 · sources not public online: left off the sources page, their marks taken off the pages; the "
                 "figures they backed have no public source now (page, the sheet's own mark, its source):"]
        rows += ["  " + t for t in _SRC[0].f5]
    return rows


def text_test(typo):
    """v26 (round 4, G-R4-1; replaces v25's text_check, which read the booklet's words back and only logged): every
    page's TextPage (titles, intros, captions, legends, footer, cover, contents, Sources; crops and the cover collage
    as drawing blocks no booklet word may enter; a whole sheet's own words kept clear of its page number) is checked:
    each logs "overlap pNN checked n, collisions k"; returns the collisions of every page (one line each)"""
    hits = []
    for tp in typo.tps:
        try:
            tp.check(raise_=True)
        except TextCollision as ex:
            hits.append(u"%s" % ex)
    return hits


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
    # v26 (round 4 S1/S9): one trigger file (common/trigger.py): a Button press or a new done text from the script
    # before it on one of the component's own inputs; settings in the script are never read as a press
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
    if _sc.sticky.get(_k + "_ver") != VERSION:   # v10.1 (Aras 27 Oct 15:35): a newly pasted version shows itself at once,
        for _s in ("_log", "_status", "_done"):   # idle, without the old run's time or log
            _sc.sticky.pop(_k + _s, None)
    done = _sc.sticky.get(_k + "_done", "idle")
    log = _sc.sticky.get(_k + "_log", "Press the Button to build " + " and ".join(
        os.path.join(OUT_DIR, variant_pdf(v_)) for v_ in BOOK_VARIANTS))
    print(log)
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(_k + "_status", "idle")  # noqa: F821
    except Exception:
        pass
else:
    print(write_log(main()))
