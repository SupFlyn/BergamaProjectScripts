# CURRENT VERSION: bergama_agriculture_alternatives_v11.py = v11 (4 Nov 2026, round 6 S7: booklet p17 plant ladder restored, p18 back to the SON arrangement; what changed: the NEW IN / VERSION notes below)
# bergama_agriculture_alternatives_v8.py (v8, 31 Oct: round 3, p18 + p19 merged on ONE booklet page) · Thread 3 of the 22 Oct batch: three alternatives for the agriculture analysis
# Runs as delivered in: Grasshopper Python 3 component (press a Button wired to an input named run; outputs log and
# done), Rhino 8 ScriptEditor (Python 3), or plain Python 3. v10 lays out no page and writes no PDF (round 5,
# G-R5-12): it writes
#   Downloads/Bergama/cached/booklet/Bergama_agriculture_alternatives/items.json   booklet p21 (25-page numbering):
#       per story group one chart drawing (mm, y up) with every word in it as an anchored label, its heading and
#       note as text items (same group id), the crop photos as photo items (files in cached/plant_photos/), the
#       farms map as its own true-scale plan (metres) on the site board's plan 01 (drawing sb_plan01), every source
#       as a Sources row ({src:agsrcN} marks in the texts)
#   Downloads/Bergama/cached/booklet/Bergama_agriculture_alternatives/results.json hectares per crop (keys unchanged)
#   Downloads/Bergama/logs/bergama_agriculture_alternatives_log.txt                the log
# Nothing is written to output/ (no output folder is made). The booklet places, sizes and checks every item.
# How you know it ran: the component's text says "AgriCulture v10 · HH:MM · n s"; the log's first lines are
# "agriculture alternatives v10 · date time · s", "<n> warnings" (every WARNING line follows it), then
# "items bergama_agriculture_alternatives: drawing n, legend n, list n, photo n, source n, text n -> .../items.json".
# T4a (revision 29 Oct, WO-T4a-4): D9 a: the plant ladder page (booklet p20) is gone with everything only it used (its
#   content lives on the water board's p17 and p14-15); pictograms and step markers from common/icons.py (02 §2); D13:
#   sources naming our own model run or method and status words never reach the printed key (cite).
# Storage, water to the farms and the farm areas are read on every run from the water balance script's output
# (bergama_water_balance), so they follow its cost cut-off; the fallback is the shared key-figures file (flagged).
# Notes for Aras: batch_2026-10-22/thread3_agriculture/NOTES.md.
import os, time, json, math, re

VERSION = "v11"  # v11 (round 6 S7, 4 Nov): p17 plant ladder restored from 28 Oct as items, p18 blocks as SON (v8.3), hue table, G6-9 groups (NEW IN v11); v10 (round 5 S9, 2 Nov): items for the booklet (p21 groups + the farms map on plan 01), no sheet PDF, warnings never stop (NEW IN v10); v9.2 fix 1 Nov 18:35 (Aras 17:30): p19 timeline starts 3.2 mm in so "1500" stays inside the crop; v9.1 fix 1 Nov 18:15 (Aras 17:07): p19 bars, a grid line whose value would run past the crop edge is left out; v9 (round 4, S6b: booklet p19 rebuilt as story groups, real Arial text check, one trigger file); v8.3 fix 1 Nov 08:30: only the component's own inputs can start it (a True setting inside the script no longer does); v8.2 fix 1 Nov 08:20: chain trigger keyed to each solve (Rhino keeps globals), so the chain continues after ZoneBase; v8.1 fix 1 Nov: a pasted or rewired component no longer runs by itself (chain trigger notes the wire on its first solve)
# NEW IN v11 (round 6, S7, 4 Nov 2026; BRIEF §6 rows 17-18, Q9, G6-1, G6-6, G6-8, G6-9, G6-10; PLAN §2.2-§2.3; a
#   feature change, so the next whole number):
#   * p17 (NEW, r06_S01, SKETCH): the 28 Oct "One plant ladder, streambed to field" (f93d84b v3.1 page_ladder,
#     ladder_row, chain_strip, seasons, data/STEPS.py; sketch engine = ../bergama_proposal_sections/data/SKETCH_SRC.py,
#     included read-only, owned by proposal sections) as items ag3_chain, ag3_steps, ag3_legend, ag3_ladder_high /
#     _low / _harvest, ag3_bands (photos as clipped image shapes under their band) -> pages/p17_ladder.py. No "no photo"
#     box: a species whose photo did not load is named under its band ("also: ...") + a WARNING. 28 Oct [n] -> {src:}.
#   * p18 (SON page19 = r3, v8.3): the blocks as v8.3 printed them: "THE STREAM COMES FIRST" (ag1_stream), the bars
#     (ag1_bars, v8.3 size 7 columns x 66), "WHY CROP CHOICE IS THE LEVER" tiles only (ag1_context, 5 x 66), "THE
#     READING" its own block again (ag1_reading, 4 x 31), "WHY THE STORED WATER GOES TO FARMS" (ag1_history, 4 x 31),
#     "THE CROPS" photos (group ag1_crops); v9/v10 fixes kept (outside values never under the row labels, grid values
#     never past the edge); bar row lines 3.2 / 3.0 mm apart (SON pairs "Olive ... x [63][64]"); page id p18 (was p21).
#   * G6-6: legends and charts from common/hues.py (fields AGR r1/r2 lines, hub squares PUB, flood lines WAT r1, roots
#     HER r2, job tags GRN r1); no 8B2D2D. G6-9: every recorded shape carries (kind, element id); each run is exported
#     as its own layer "kind/element" inside ix_group (common/item_export.py, round 6 S2). Sources rows on the page that
#     first cites them (p17 or p18).
# NEW IN v10 (round 5, S9, 2 Nov 2026; G-R5-12, P21.1, C13, C1, C2, CHK-12, G-R5-4.6; a feature change, so the next
#   whole number). Every figure, source and photo is computed and chosen as in v9.2 (K4); only how it leaves the script
#   changed:
#   * G-R5-12 / addendum 2 (no sheet PDFs): the A3 sheet, its PyMuPDF rewrite (put_base, put_photos), the sources page,
#     blocks.json and booklet_export are gone. Each block is drawn by its v9 function into a recorder (AgRec, the old
#     Page's calls) and exported through common/item_export.py: drawings ag1_stream, ag1_bars, ag1_context,
#     ag1_history (units mm, dkind chart, no scale bar) and the photos of ag1_crops (photo items + captions).
#   * P21.1 (U57, "which group talks about what"): one group id per story group, shared by its heading, drawing,
#     labels, notes and photos, priority = reading order: ag1_stream 2, ag1_bars 3, ag1_context 4, ag1_history 5
#     (with the crop photos, which carried no heading of their own in v9), ag2_farms 6.
#   * C13: the farms map is its own true-scale plan ag2_farms (metres, the farms' own extent + a margin, the listed
#     scales that fit the booklet's drawing column), its base read from the site board's drawing sb_plan01 (items.json)
#     and moved onto the farms with sb_plan01's georef; where the farms reach past plan 01 the base simply ends (log
#     "FLAG p18 farms map: plan 01 covers n % ..."); no base found = a WARNING and the farms alone, never a stop.
#   * C1: common/warn.py before text_place.py; nothing raises on text: the timeline's own Placer (and its TextError
#     when a label found no lane) is gone, every label is exported at its v9 first position and placed by the booklet.
#     The log head counts the WARNING lines (wn_compose).
#   * C2: no output/ folder is made; cached/booklet/<folder>/ only when items.json / results.json are written.
#   * CHK-12: build() (a Button word: a Button input named "build" read the function) is now ag_items().
#   * G-R5-4.6: no width was printed by this script (checked: no cm / m horizontal size in any text); nothing removed.
# NEW IN v9 (round 4, 1 Nov, session S6b; P19.1, K4, G-R4-1/2/7/11; spec revision_2026-11-01_round4/handover/
#   S6b_p19_design_spec.md): booklet p19 "Where the clean water goes, and what it grows" is rebuilt as story groups,
#   each with ONE heading inside its first crop, the crops of a row sharing their top and bottom edges; every figure,
#   source and photo kept (K4), only the layout and the duplicate titles changed:
#   * ag1_stream 260 x 40 (group 2 "HOW MUCH WATER REACHES THE FARMS", was "THE STREAM COMES FIRST"); ag1_bars
#     194 x 72 (group 3 "HECTARES ONE STORAGE IRRIGATES, BY CROP"); ag1_context 194 x 72 (group 4 "WHY CROP CHOICE
#     IS THE LEVER": the reading's squares and 2.2-4.4 x on top, the four tiles under it); ag1_history 260 x 34 (group
#     5 "THE CROPS, THEN AND NOW"); ag1_crops 128 x 34 (the photos at the one booklet photo size). ag1_reading is no
#     crop any more (drawn inside ag1_context). Booklet captions of these crops are empty (the heading says it).
#   * G-R4-1: text widths from the real Arial (text_w = font_metrics.fm_width; common/text_w.py and the Helvetica
#     table gone); one TextPage per booklet crop (common/text_place.py): every text registered, the drawings no text
#     may touch (icons, bars, photos, squares) are keeps, a collision RAISES; log "overlap p19 <crop> checked n,
#     collisions 0" (lp_overlap_flag / ag_flags gone). ² and ³ are the embedded font's own glyphs (the raised 0.6 x
#     digit printed under 6 pt).
#   * G-R4-2: wrap and Page.para never leave a one-word last line. G-R4-7: the step chips' numbers through
#     common/marker.py mk_marker. G-R4-11: the timeline's "Red Hall" is Kızıl Avlu from the shared names table.
#   * Trigger: the script's own copies (common/chain_fire.py, gh_in_items.py, the globals scan) are replaced by
#     common/trigger.py trig_should_run (a press of the Button or a new done text on its own inputs); the log says
#     "trigger: <why>". results.json keys and the other crop ids are unchanged.
# NEW IN v8 (round 3, B4 · P18.1-P18.4, D8, G2, G3, G4, G17; spec revision_2026-10-31_round3/handover/B4_work/
#   spec_p18_merged.md): page 1's five booklet crops are drawn at 1:1 for ONE merged booklet page and carry "bk_w"
#   (the booklet keeps them 1:1): ag1_stream 260 x 40 mm (the to-farms headline folded in: ag1_headline is gone),
#   ag1_bars 227 x 66 (direct labels, no key row), ag1_context 161 x 66 (tiles 2 x 2), ag1_reading 128 x 31 (two
#   squares by area + the ratio), ag1_history 128 x 31 (no leader lines), ag1_crops 128 x 31. No strokes around tiles
#   or photos (G17). P18.2: the photos go in as plain images (common/plant_photos.py, A2) and the log says
#   "photos: n of m placed as images"; "FLAG overlap p18 <crop> n" per crop (label_place.py).
# NEW IN v7 (round 2, Aras 31 Oct 11:13: p18 + p19 on one page if legible, PG2 p18-19, M10): ag1_bars compact (rows
#   14 mm apart, bars 5 mm, grid 165 mm wide: about 239 x 98 mm, was 264 x 113); ag1_reading one strip 252 x 28 mm
#   (was 244 x 48): the two dry-year bars it repeated from ag1_bars are gone (a fact once), the ratio and the lever stay.
# Revision 30 Oct (T5, booklet p.19; M10, G4): every fact once in the booklet. Storage (p.10) is no longer printed
#   here (headline, store legend); the olive area is facts.py "8,705 ha", printed once (the olive bar row; the
#   cotton tile and the timeline no longer repeat the 2025 areas: "8,700" gone); the olive full-irrigation row prints
#   its normal-year need from facts.py (the dry-year need and 1.25 ha are p.18's); "what it replaces" (1.25 ha again,
#   and a note on an older board version) is gone with its crop ag1_replaces.
# NEW IN v5.1 (bugfix, revision 29 Oct T5 fix pass, Aras 22:08): p.19 "10,000 m³ = N ha olive" is computed live, the
# same way as the water board's p.18 (10,000 / gross m³ a ha of olive in a dry year, from water_balance_results.json);
# it was the fixed text "1.22 ha".
# v4 (MIRAQUA 28 Oct, booklet revision v4, pages 18-19; a feature change, so the next whole number):
#   * P18.1 / P19.3 / P19.4 / G11 / G12: every photo through common/plant_photos.py; corn printed as "Corn (Mısır)"
#     (data key "maize" and the Wikimedia file kept); an empty frame says "no photo: <reason>".
#   * P19.1 / G5 / F10: the kicker top left; page 3's top-right corner on the booklet grid (column 8, 4 rows 5.2 mm
#     apart, 7.5 pt): steps 1-5, NEXT -> D The heritage loop (title bold), the chain key; no big page numbers.
#   * P19.2: the ladder's people from common/figures.py at true scale (1.75 m), one colour, no stroke.
#   * G4 / F13: ladder labels placed by common/label_place.py clear of figures, lines, plants and each other;
#     "hub square: dry, step-free" and "wade the strip" now print.
#   * G13: flood heights in m with 2 decimals (values unchanged). Bank depth research 28 Oct §4.5: over the bank top
#     only at S4 (left); K4 before the DSİ walls.
#   * F5: [n] marks only for public online sources; internal pointers out of the printed source list.
#   * G1: page 2's group line removed; page 1's left column on the 14 mm margin.
# v3.1 (bugfix, Aras 27 Oct, booklet Prompt 8 "final check of every page"): plant and crop names "English (Turkish)"
#   from the shared table where pages 1 and 3 still had the English alone: page 3's season row OLIVE (ZEYTİN) HARVEST,
#   its labels (hub square: oriental plane (Doğu çınarı) shade; common reed (Kamış) gold; olive (Zeytin) harvest;
#   olive (Zeytin) trees on the fields) and page 1's "what it replaces" figure. Page 3: "stored winter water" and
#   "site edge: farmland outside" sit at the row's top edge, so they found no free place above it and were left out on
#   every run: they now go under their anchors. The h01 timeline quotes stay word for word. Page 1's "THE STREAM COMES
#   FIRST" block and the step chips: its 6.5 pt words are 7 pt, the smallest size on a booklet page.
# v3 (Aras 27 Oct 17:35, Prompt 6 "water, part 3"; the booklet's p.24-25):
#   * page 1, "THE STREAM COMES FIRST" between the headline and the bars (task 1: "show the defence ON the board"): the
#     priority 1 stream: summer strip -> 2 on-site planting -> 3 farms (the model has no draw of its own for the
#     planting: it lives on the strip's water, so it shares the strip's bar); the design store through a normal and the
#     1-in-5 dry water year as two stacked bars on one scale (strip, farms, left over; the store size dashed across
#     both), read live from the water balance v4 results (design.year_split, one daily run); and the double squeeze in
#     one line, computed: water left for the farms after the strip, the need per hectare and the hectares that water
#     serves, dry year against normal, then why deficit-irrigated olive is the lever. Without year_split (water balance
#     v3 or older) only the priority row is drawn (logged). The bars move down to make room: rows 16.5 mm apart (were
#     19.5), the reading box ends at the 14 mm margin.
#   * pages 1 and 3 say where they sit in the booklet: "C WATER · WHAT WE DO WITH IT" (was "AGRICULTURE ANALYSIS");
#     page 3, the last page of the water theme, closes it top right: what we do with the water in five steps and NEXT
#     D HISTORY AND HERITAGE (rule 7, task 3).
#   * m² and m³ are written as a raised small 2 or 3 (0.6 x the size, as wide as the glyph), which every PDF viewer
#     shows (task 2: "325,000-375,000 m" in some viewers).
# v2 (Aras 27 Oct, Prompt 5, rule 8: "Plant names: English first, Turkish in brackets, no Latin ... Every plant AND every
# crop in the booklet gets a photo of the plant itself ... openly licensed photos ... credited in the sources ... Same
# crop ratio and size for every photo"): every plant and crop name on pages 1 and 3 is "English (Turkish)" from the
# shared table (src/common/plant_photos.py), no Latin names on the pages. Page 3's step columns show each step's plants
# as photos (PHOTO_W x PHOTO_H mm, two side by side) with the name and the photo's [n] credit under each; the giant reed
# under REMOVE. Page 1 adds "THE CROPS" under the timeline: olive, cotton, corn, tomato as photos. The photos come
# from the shared cache Downloads/Bergama/cached/plant_photos/ (the water board shows the same photo of the same
# plant) and go into their frames with PyMuPDF after the PDF is written; a missing one is an empty frame saying "no
# photo", never an error; the log says how many were placed. Room on page 3: the chain sits 4 mm higher, the season rows
# are 50 mm (were 52; 4.5 mm stay above the tallest tree); the plants' reasons are left out under the photos when the
# column would not fit (logged). The Data file changes (STEPS: plant keys instead of botanical names): copy the new one.
# v1.7 (bugfix, Aras 27 Oct 16:05): page 3 crashed ("too many values to unpack": the sketch engine's items now
# carry a 4th value, the label group); the text under the component shows a newly pasted version at once, idle.
# v1.6 (Aras 27 Oct 11:07, booklet p24-26; revision_2026-10-27/PHASE2_SPEC.md): white pages (the beige paper goes); no
# source footers or credit lines on the pages: the [n] marks are numbered once for the sheet and their key is a 4th
# page "Sources" (the booklet's sources page reads it there). Page 1 adds "why the stored water goes to farms": a
# cotton / olive timeline in card h01's words and years, labels placed by measured width. Page 3 rebuilt for option A:
# the one-way chain upstream entry -> K4 -> K3 -> İstiklal -> K5 -> K6 -> downstream -> farmland outside the site,
# hubs and in-bed sub-hubs, programme and historic roots; the ladder drawn three times (high water, low water, olive
# harvest) with what people do on each step; the species under each step. Every label is placed by a collision check
# (Placer): a label with no free place is left out and named in the log.
# v1.5 (Aras 26 Oct 07:06, review of the deck, p.33-34): page 2's map is the site board's own plan 01 ("What is there",
# board v42+, cut from its sheet PDF with PyMuPDF and scaled by one factor, never redrawn) at the largest round scale
# that fits, with only the farms layer drawn on it (fields and orchards fed, their extent), the plan's own key, the
# figures beside it and a context line; v1.4's land cover drawing stays only as a flagged fallback. Page 3's ladder is
# drawn by the proposal sections' sketch engine (the p.23 upstream entry's language): hand ground, washes, winter
# water and summer strip, the faint design-flood reach, level marks, sketch plants and people, rain and sun marks.
# The "# r: pymupdf" line installs PyMuPDF in Rhino 8 on the first run (as the booklet). (v10: no PyMuPDF used, line gone)
# v1.4 (Aras 25 Oct 21:47-22:02, booklet stage 3): the booklet shows crops of this sheet (booklet/CROP_SPEC.md):
# blocks.json lists one crop per panel of the three pages and results.json keeps v1.3's keys; the v1.3 booklet redraws
# are gone. Caveat notes taken off the sheet (labels kept); "stream", never "river". Page 3's ladder drawn in the site
# board's section language (src/common/section_style.py): cut ground with sloped banks, the strip hatched, whole plants,
# one size across and up.
# v1.3 (25 Oct, booklet stage 2, SCRIPT_STANDARD §8): also writes output/<folder>/booklet/: c7_hero.pdf (plant ladder +
# the water board's planting bands A-F), c8_b.pdf (hectares per crop bars), blocks.json (every word a label) and
# results.json (hectares per crop). The A3 sheet is unchanged.
# v1.2 (Aras 25 Oct 17:00, SCRIPT_STANDARD §5b visual first): sentences become pictogram tiles, callouts and tags; method
# and source sentences become [n] marks with one numbered source key in each page's footer; layout and colours kept.
# Flood figures corrected to the surveyed sections (research/rain_river_levels/README.md, v1.1 correction and line 49).
# v1.1 (Aras 25 Oct 09:34-09:35): the same names in every script: the Button goes into an input named run, the log comes out of an output named log, and the log file is Downloads/Bergama/logs/bergama_agriculture_alternatives_log.txt (next to cached/ and output/), overwritten by each press.
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
# ---- plant photos, shared by the water board and the agriculture alternatives (Aras 27 Oct, Prompt 5: "every plant
# AND every crop in the booklet gets a photo of the plant itself. Use openly licensed photos (e.g. Wikimedia Commons)
# credited in the sources, never photos from shop or nursery sites. Same crop ratio and size for every photo").
# MIRAQUA round 28 Oct (G12): every photo is PINNED to one Wikimedia Commons file page (PLANTS), the whole plant or
# crop in its setting, the same file wherever the species shows. No lead image and no search at run time (they gave
# the museum cob and the African olive). Why cards printed "not loaded": Wikimedia answered a burst of 3-4 requests a
# plant with HTTP errors (most likely 429, too many requests) and the code kept asking. Now: ONE batched API call for
# all photos still to fetch, then one 500 px download at a time with a pause, Retry-After honoured once, and after a
# second refusal nothing more this press (remembered 10 min, so a quick second press does not trip it again). The
# user agent names the project and its repository (Wikimedia's user-agent policy).
# Fetched once on Aras's PC (the cloud cannot reach Wikimedia), kept in the cache folder and read from there on every
# later press. Any licence is accepted (D8, PHOTO_ANY_LICENCE); credits stay. A photo Aras puts into the cache folder
# himself (<key>.jpg with a <key>.json {"file", "credit"}) is used as it is. If the pinned files cannot be fetched,
# an older cached photo of the same plant stays (where its row allows), else the frame says why.
# Credit (Aras 28 Oct 11:38, fault table F15: "no Latin file names"): author, licence, Wikimedia Commons and the page-id
# link that opens exactly that file page; PHOTO_CREDIT_FILE = True adds the file name (brief G12) if that is chosen.
PHOTO_W, PHOTO_H = 28.0, 21.0        # mm on the A3 page, every photo in the booklet (4:3, cover-cropped, never stretched)
PHOTO_PX = 500                       # px wide fetched: a standard Wikimedia thumbnail step (about 450 dpi at PHOTO_W)
PHOTO_CREDIT_FILE = False            # True = the credit names the Commons file too (G12) besides the page-id link (F15)
PLANT_PHOTO_DIR = bg_cache("plant_photos")   # one folder for every script: the same plant shows the same photo
# Every plant and crop the booklet names: key -> (printed name "English (Turkish)", the Commons files to use in order
# (file page titles without "File:"; the first that is free and loads is used), keep_old = an older cached photo of
# this plant may stay when none of them loads). Names: English and Turkish as in research/water_data/04 §1 (species
# matrix), Aras's examples "Common reed (Kamış)", "Oriental plane (Doğu çınarı)"; Kofa = the rush genus Juncus
# (turkiyebitkileri.com, Juncaceae - Kofagiller, Juncus - Kofa). Files: revision_2026-10-28/checks/photos.md §2-3
# (whole plant in its setting; author and licence are read from each file page at the fetch and checked there).
PLANTS = {
    "reed": (u"Common reed (Kamış)", (u"Common Reed (Phragmites australis) (8131465127).jpg",
                                     u"Reed panicle at Brodalen 1.jpg"), True),
    "cattail": (u"Broadleaf cattail (Hasır otu)", (u"Bulrush (Typha latifolia) (8139113636).jpg",), True),
    "mint": (u"Water mint (Su nanesi)", (u"Mentha aquatica Meinerswijk.jpg", u"Mentha aquatica 02.jpg"), True),
    "iris": (u"Yellow flag iris (Sarı süsen)", (u"Yellow Iris, Gunnersbury Triangle.JPG",
                                                u"Iris pseudacorus (yellow flag iris) (Newark, Ohio, USA) 5 (27772297656).jpg"), True),
    "rush": (u"Sharp rush (Kofa)", (u"Juncus acutus2.jpg",), True),
    # H-B 30 Oct (M6, p16 gap): titles from the Commons search index (T1 sourcing §2 and a web search, 30 Oct); not
    # opened from here (Commons blocked in the cloud): UNVERIFIED until the first fetch on Aras's PC logs them.
    # Turkish name of Juncus effusus not verified: the genus name Kofa (as for the sharp rush) is used.
    "soft_rush": (u"Soft rush (Kofa)", (u"Pitrus (Juncus effusus) 07.JPG", u"Pitrus plant (Juncus effusus) (1).jpg",
                                       u"Pitrus (Juncus effusus) 05.JPG", u"JuncusEffusus.jpg"), True),
    "stone_pine": (u"Stone pine (Fıstık çamı)", (u"Stone Pine (Pinus pinea) - Rome, Italy 2024-03-04.jpg",
                                                 u"Pinus pinea.JPG"), True),
    "loosestrife": (u"Purple loosestrife (Aklar otu)", (u"Lythrum salicaria, field of purple loosestrife, Concord, Massachusetts.jpg",
                                                        u"Purple Loosestrife (Lythrum salicaria) - geograph.org.uk - 950598.jpg"), True),
    "tamarisk": (u"Tamarisk (Ilgın)", (u"A Tamarisk Tree in Israel (5759425470).jpg", u"Tamarix canariensis-Daimiel.jpg"), True),
    "willow": (u"White willow (Ak söğüt)", (u"A big white willow tree (Salix alba) at the bay of lake Juojärvi in Tuusniemi, Finland, 2018 September.jpg",
                                            u"Silberweide (Salix alba).JPG"), True),
    "chaste": (u"Chaste tree (Hayıt)", (u"Vitex-agnus-castus-habitus.jpg", u"Vitex-agnus-castus-habit.JPG"), True),
    "poplar": (u"White poplar (Ak kavak)", (u"Pioppo (populus alba).jpg", u"Daniel Fuchs.CC-BY-SA.Populus alba.jpg"), True),
    "ash": (u"Narrow-leaved ash (Dişbudak)", (u"Fraxinus angustifolia - Israel.JPG", u"Fraxinus-angustifolia.jpg"), True),
    "oleander": (u"Oleander (Zakkum)", (u"Oleander (Nerium oleander) habit.jpg", u"Nerium oleander (Adelfa).jpg"), True),
    "plane": (u"Oriental plane (Doğu çınarı)", (u"Oriental Plane tree - Platanus orientalis - Doğu Çınarı, Arslanköy 04.JPG",
                                                u"TRSTENO ORIENTAL PLANE TREE, CROATIA.jpg"), True),
    "lavender": (u"French lavender (Karabaş otu)", (u"Lavandula stoechas (cantueso).jpg", u"Lavandula stoechas 1.JPG"), True),
    "rosemary": (u"Rosemary (Biberiye)", (u"Large rosemary bush.jpg", u"Rosmarinus officinalis (Italy) 01.jpg"), True),
    "olive": (u"Olive (Zeytin)", (u"Olive trees on Thassos.JPG",), True),       # was the African wild olive (Cape Town)
    "cotton": (u"Cotton (Pamuk)", (u"CottonPlant.JPG",), True),
    "maize": (u"Corn (Mısır)", (u"Maize field, Balcalı 01.jpg", u"A Maize Crop with beautiful Corn.jpg"), False),  # G11, P18.1:
    "tomato": (u"Tomato (Domates)", (u"Solanum lycopersicum in Kaunas.jpg",), True),                       # never the cob
    "giant_reed": (u"Giant reed (Kargı)", (u"Poaceae plant at golden hour near the river in Laos.jpg",
                                           u"Arundo donax 2007.JPG"), True),
}


def plant_name(key):
    """The printed name of a plant: "English (Turkish)"."""
    return PLANTS[key][0]


def plant_photo_of(key, log, state):
    """(jpeg path or None, credit or None, why not) of a plant in PLANTS, from the shared folder."""
    name, files, keep_old = PLANTS[key]
    return plant_photo(key, name, files, keep_old, PLANT_PHOTO_DIR, log, state)


PHOTO_UA = ("MIRAQUA-booklet/3 (https://github.com/SupFlyn/BergamaProjectScripts; Bergama student project, "
            "Yasar University) Python-urllib")
PHOTO_TIMEOUT = 8.0                  # s per request; after one network failure the rest are not tried this press
PHOTO_PAUSE = 1.0                    # s between two downloads
PHOTO_HOLD = 600.0                   # s: after Wikimedia refused twice, no new request for this long (any press)


def jpeg_info(data):
    """(width, height, colour components) of JPEG bytes (baseline or progressive), else None."""
    import struct
    if data[:2] != b"\xff\xd8":
        return None
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            return None
        m = data[i + 1]
        if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7:
            i += 2
            continue
        n = struct.unpack(">H", data[i + 2:i + 4])[0]
        if m in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return (w, h, data[i + 9]) if data[i + 9] in (1, 3) else None
        i += 2 + n
    return None


def _photo_http(url, state):
    """the bytes at url; an HTTP 429/503 waits for its Retry-After (at most 30 s) and tries once more, a second
    refusal sets state["refused"] (nothing more is fetched this press). A pause before every request but the first."""
    import time
    import urllib.request
    import urllib.error
    for attempt in (0, 1):
        wait = PHOTO_PAUSE - (time.time() - state.get("last", 0.0))
        if wait > 0:
            time.sleep(wait)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": PHOTO_UA})
            with urllib.request.urlopen(req, timeout=PHOTO_TIMEOUT) as r:
                return r.read()
        except urllib.error.HTTPError as ex:
            if ex.code not in (429, 503):
                raise
            if attempt:
                state["refused"] = u"Wikimedia refused (HTTP %d)" % ex.code
                _photo_hold(state["refused"])
                raise
            try:
                ra = float(ex.headers.get("Retry-After") or 5.0)
            except Exception:
                ra = 5.0
            time.sleep(min(30.0, max(1.0, ra)))
        finally:
            state["last"] = time.time()


def _photo_hold(why=None):
    """the refusal memo in the cache folder: written with why, else read: (why, seconds left) or None"""
    import time
    p = os.path.join(PLANT_PHOTO_DIR, "_refused.json")
    try:
        if why:
            os.makedirs(PLANT_PHOTO_DIR, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"why": why, "t": time.time()}, f)
            return None
        with open(p, "r", encoding="utf-8") as f:
            m = json.load(f)
        left = PHOTO_HOLD - (time.time() - float(m["t"]))
        return (m["why"], left) if left > 0 else None
    except Exception:
        return None


def _png_to_jpeg(src, dst):
    """A PNG turned into a JPEG on white by .NET System.Drawing (Rhino on Windows); False where that is missing."""
    try:
        import clr
        clr.AddReference("System.Drawing")
        import System.Drawing as SD
        bmp = SD.Bitmap(src)
        out = SD.Bitmap(bmp.Width, bmp.Height)
        g = SD.Graphics.FromImage(out)
        g.Clear(SD.Color.White)
        g.DrawImage(bmp, 0, 0, bmp.Width, bmp.Height)
        g.Dispose()
        out.Save(dst, SD.Imaging.ImageFormat.Jpeg)
        bmp.Dispose()
        out.Dispose()
        return True
    except Exception:
        return False


PHOTO_ANY_LICENCE = True            # D8 (Aras, 30 Oct): licences are not regarded; every source is still credited


def photo_free(lic):
    """True for an open licence: CC BY / CC BY-SA (any version), CC0, public domain; always True while
    PHOTO_ANY_LICENCE (D8)."""
    if PHOTO_ANY_LICENCE:
        return True
    t = (lic or u"").lower()
    if not t or "non-free" in t or "fair use" in t or "-nc" in t or "-nd" in t or " nc" in t or " nd" in t:
        return False
    return t.startswith("cc by") or t.startswith("cc-by") or t.startswith("cc0") or "public domain" in t or \
        t.startswith("pd")


def _photo_meta(info):
    """(author, licence) from a Commons imageinfo record's extmetadata."""
    import re
    md = info.get("extmetadata", {}) or {}
    artist = re.sub(r"<[^>]+>", u"", md.get("Artist", {}).get("value", u"")).strip()
    return re.sub(r"\s+", u" ", artist), md.get("LicenseShortName", {}).get("value", u"").strip()


def _photo_infos(titles, state):
    """ONE Commons API call for up to 50 file titles: {title: imageinfo record + pageid} for the files that exist"""
    import urllib.parse
    out = {}
    for i in range(0, len(titles), 50):
        part = titles[i:i + 50]
        q = json.loads(_photo_http("https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo"
                                   "&iiprop=url|mime|size|user|extmetadata&iiurlwidth={}&titles={}".format(
                                       PHOTO_PX, urllib.parse.quote(u"|".join(u"File:" + t for t in part))),
                                   state).decode("utf-8"))
        qq = q.get("query", {})
        norm = dict((n_.get("to"), n_.get("from")) for n_ in qq.get("normalized", []) or [])
        for pg_ in qq.get("pages", {}).values():
            ii = (pg_.get("imageinfo") or [None])[0]
            if "missing" in pg_ or not ii:
                continue
            t = pg_.get("title", u"")
            t = norm.get(t, t)
            ii["pageid"] = pg_.get("pageid")
            out[t.replace(u"File:", u"", 1)] = ii
    return out


def _photo_safe(s):
    """a name the sheets' fonts can print (WinAnsi + the Turkish letters): other letters lose their accents (Kaunas
    authors etc.), anything still unprintable leaves the name out"""
    import unicodedata
    tr = u"ĞğİıŞş"
    out = u""
    for ch in s or u"":
        try:
            ch.encode("cp1252")
            out += ch
        except Exception:
            if ch in tr:
                out += ch
            else:
                b = unicodedata.normalize("NFKD", ch)[0]
                out += b if ord(b) < 128 else u""
    out = u" ".join(out.split())
    return out if sum(c.isalpha() for c in out) >= 2 else u""


def photo_credit(name, m):
    """the printed credit of a photo record m {author, licence, pageid, title} (F15: no Latin file names)"""
    link = u"commons.wikimedia.org/?curid={}".format(m["pageid"]) if m.get("pageid") else u"Wikimedia Commons"
    cr = u"photo {}: {}, {}, Wikimedia Commons, {}".format(name, m.get("author") or u"author named on the file page",
                                                            m.get("licence") or u"licence on the file page", link)
    if PHOTO_CREDIT_FILE and m.get("title"):
        cr += u" (File:{})".format(m["title"])
    return cr


def plant_photo(key, name, files, keep_old, photo_dir, log, state):
    """(jpeg path or None, credit or None, why not) for one plant or crop: key = file name in photo_dir, name = the
    printed name, files = its pinned Commons files in order, keep_old = an older cached photo may stay. Cache first
    (when it holds one of the pinned files, or Aras's own photo), then the web (see the header of this part)."""
    meta = os.path.join(photo_dir, key + ".json")
    old = None
    try:
        with open(meta, "r", encoding="utf-8") as f:
            m = json.load(f)
        p = os.path.join(photo_dir, m["file"])
        with open(p, "rb") as f:
            if jpeg_info(f.read(256 * 1024) + b"\x00" * 10):
                if not m.get("source") and not m.get("title"):
                    return p, m["credit"], None                       # Aras's own photo, as it is
                if m.get("title") in files and m.get("pageid"):
                    return p, photo_credit(name, m), None             # one of the pinned files, fetched before
                old = (p, m.get("credit"))                            # fetched by an older version
    except Exception:
        pass

    def fallback(why):
        if old and keep_old:
            log.append(u"photo {}: {}; the older cached photo stays".format(key, why))
            return old[0], old[1], None
        log.append(u"photo {}: {}; pinned file(s): {}".format(key, why, u"; ".join(
            u"commons.wikimedia.org/wiki/File:" + t.replace(u" ", u"_") for t in files)))
        return None, None, why
    if state.get("offline"):
        return fallback(u"offline")
    if "refused" not in state:
        h = _photo_hold()
        if h:
            state["refused"] = u"{}, press again in {:.0f} min".format(h[0], max(1.0, h[1] / 60.0))
    if state.get("refused"):
        return fallback(state["refused"])
    try:
        os.makedirs(photo_dir, exist_ok=True)
        if "infos" not in state:                                      # every photo still to fetch, in one call
            need = []
            for k_, row in PLANTS.items():
                try:
                    with open(os.path.join(photo_dir, k_ + ".json"), "r", encoding="utf-8") as f:
                        m_ = json.load(f)
                    if (m_.get("title") in row[1] and m_.get("pageid")) or not (m_.get("source") or m_.get("title")):
                        continue
                except Exception:
                    pass
                need += [t for t in row[1] if t not in need]
            state["infos"] = {}                                       # a failed call is not repeated this press
            state["infos"] = _photo_infos(need, state)
        ii, why = None, u"file not found on Commons"
        for t in files:
            c = state["infos"].get(t)
            if c is None:
                continue
            artist, lic = _photo_meta(c)
            if not photo_free(lic):
                why = u"licence not open ({})".format(lic or u"none")
                continue
            if c.get("mime") not in ("image/jpeg", "image/png"):
                why = u"not a photo file"
                continue
            ii = (t, c, artist, lic)
            break
        if ii is None:
            return fallback(why)
        t, c, artist, lic = ii
        data = _photo_http(c.get("thumburl") or c["url"], state)
        p = os.path.join(photo_dir, key + ".jpg")
        if jpeg_info(data):
            with open(p, "wb") as f:
                f.write(data)
        else:
            tmp = os.path.join(photo_dir, key + ".src")
            with open(tmp, "wb") as f:
                f.write(data)
            if not _png_to_jpeg(tmp, p):
                return fallback(u"not a JPEG")
        au = _photo_safe(artist) or _photo_safe(c.get("user", u""))
        if artist and au != " ".join(artist.split()):
            log.append(u"photo {}: author '{}' printed as '{}' (the sheets' fonts)".format(key, artist, au))
        m = {"file": os.path.basename(p), "title": t, "pageid": c.get("pageid"), "author": au, "licence": lic,
             "source": c.get("descriptionurl", u""), "size": [c.get("width"), c.get("height")]}
        m["credit"] = photo_credit(name, m)
        with open(meta, "w", encoding="utf-8") as f:
            json.dump(m, f, ensure_ascii=False)
        log.append(u"photo {}: {} · page {} · {} · {} · {} x {} px".format(key, t, c.get("pageid"), au, lic,
                                                                          c.get("width"), c.get("height")))
        return p, m["credit"], None
    except Exception as ex:
        import socket
        import urllib.error
        if isinstance(ex, (urllib.error.URLError, socket.timeout, OSError)) and not isinstance(ex,
                                                                                              urllib.error.HTTPError):
            state["offline"] = True
        log.append(u"photo {}: {}: {}".format(key, type(ex).__name__, ex))
        if isinstance(ex, urllib.error.HTTPError):
            return fallback(state.get("refused") or u"Wikimedia error (HTTP {})".format(ex.code))
        return fallback(u"offline" if state.get("offline") else u"not loaded ({})".format(type(ex).__name__))


PHOTO_PLACED = [0, 0]                # this run: [placed as plain images, asked for] (fitz_add_photos; photo_flag_line)


def _photo_crop_pixmap(fitz, data, a):
    """the JPEG as a PyMuPDF Pixmap cut about its centre to the aspect a (w / h), never stretched"""
    src = fitz.Pixmap(data)
    if src.alpha:
        src = fitz.Pixmap(src, 0)
    iw, ih = src.width, src.height
    cw, ch = (int(round(ih * a)), ih) if iw / float(ih) > a else (iw, int(round(iw / a)))
    x0, y0 = (iw - cw) // 2, (ih - ch) // 2
    ir = fitz.IRect(x0, y0, x0 + cw, y0 + ch)
    dst = fitz.Pixmap(src.colorspace, ir, False)
    dst.copy(src, ir)
    dst.set_origin(0, 0)
    return dst


def fitz_add_photos(path, photos, page_h=297.0):
    """The photos put into a written PDF with PyMuPDF: photos = [(page index, x0, y0, x1, y1 mm, y up from the page
    foot, jpeg path)]; each JPEG fills its frame, cut to the frame's proportions about its centre (never stretched).
    Round 3 (A2, DATA-2): each photo goes in as a PLAIN image on the page (insert_image of the cut pixmap), no longer
    inside a Form XObject (show_pdf_page), which the booklet's crop copy dropped (p19 printed no photos). If the cut
    fails, the whole JPEG is inserted proportionally inside the frame (still a plain image). The file is saved in
    place. Returns how many were placed; PHOTO_PLACED / photo_flag_line() give the log line."""
    import fitz
    K = 72.0 / 25.4
    doc = fitz.open(path)
    n = 0
    for pi, x0, y0, x1, y1, p in photos:
        try:
            with open(p, "rb") as f:
                data = f.read()
            info = jpeg_info(data)
            if not info or x1 <= x0 or y1 <= y0:
                continue
            r = fitz.Rect(x0 * K, (page_h - y1) * K, x1 * K, (page_h - y0) * K)
            try:
                doc[pi].insert_image(r, pixmap=_photo_crop_pixmap(fitz, data, (x1 - x0) / (y1 - y0)),
                                     keep_proportion=False)
            except Exception:
                doc[pi].insert_image(r, stream=data, keep_proportion=True)
            n += 1
        except Exception:
            continue
    PHOTO_PLACED[0] += n
    PHOTO_PLACED[1] += len(photos)
    if n:
        t_ = path + ".tmp"
        doc.save(t_, garbage=3, deflate=True)
        doc.close()
        os.replace(t_, path)
    else:
        doc.close()
    return n


def photo_flag_line(reset=True):
    """the log line of this run's photos: "photos: n of m placed as images" (+ FLAG when some are missing)"""
    n, m = PHOTO_PLACED
    if reset:
        PHOTO_PLACED[0] = PHOTO_PLACED[1] = 0
    return u"photos: %d of %d placed as images%s" % (n, m, u" · FLAG %d missing" % (m - n) if n < m else u"")
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
# ---- marker.py (round 4, S1, 1 Nov 2026; G-R4-7, PLAN §4.4): ONE marker (circle + number / letter) everywhere --------
# The glyph sits on the centre of its VISIBLE ink box (font_metrics.fm_ink_box), so "g", "h", "1" and "12" are all
# centred (CHK3_7 §4.1: the old cap-height offsets pulled lowercase letters down and let tails hang out). The circle
# grows with the glyph: radius = half the ink box diagonal + MK_MARGIN_MM, so two digits get a larger circle (§4.2).
# The colour is the colour the named element is drawn in, from ONE table (mk_colour), never a page-wide accent (§4.3).
# Needs font_metrics.py (and pdf_fonts.py) included before it; text_place.py for mk_put.
#   mk_marker(cx, cy, s, colour, size_pt=7.0, r_min=None, style="solid", rim="FFFFFF", rim_mm=0.25, text_col=None,
#             y_down=False) -> (shapes, box, r)
#       y_down  False (default) for the scripts' y-up sheets and the common modules' shape lists (section_frame,
#               figures); True on y-down pages (the booklet grid)
#       shapes  house format: ("poly", ring, fill, stroke, lw) then ("text", s, x, baseline_y, size_mm, colour, True,
#               "L"); box = the marker's outer box (rim included); r = the circle's radius (mm)
#       style   "solid": a disc in colour, a white rim, the glyph white or ink by contrast;
#               "ring": a paper disc, a coloured rim, the glyph in colour
#   mk_register(kind, table)          the element table a page draws with ({key: hex}), so marker = element colour
#   mk_colour(kind, key) -> hex       the registered colour; an unknown kind / key RAISES (no fallback colour)
#   mk_put(tp, shapes, name=None) -> the non-text shapes
#                                     registers the disc as a keep (kind "marker") and the glyph in the TextPage (it
#                                     may sit on its own disc only; give each marker its own name); the caller draws the returned disc shapes, the
#                                     TextPage draws the glyph
MK_MARGIN_MM = 0.45                    # clear ring round the glyph's ink box (G-R4-7 "keep a margin")
MK_PAPER = "FFFFFF"
MK_INK = "2C2219"                      # dark glyph on light discs (the north-arrow ink of PLAN §4.5)
MK_COLOURS = {}
MK_N = [0]                             # markers registered this run (unique keep names)


def _mk_lum(hx):
    """relative luminance (WCAG 2) of a hex colour"""
    h = str(hx).lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]


def _mk_contrast(a, b):
    la, lb = _mk_lum(a), _mk_lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def mk_text_colour(fill):
    """white or ink, whichever contrasts more with fill"""
    return MK_PAPER if _mk_contrast(fill, MK_PAPER) >= _mk_contrast(fill, MK_INK) else MK_INK


def mk_register(kind, table):
    """the colours a page draws its elements of one kind with ({key: hex}); markers of that kind read them"""
    MK_COLOURS.setdefault(kind, {}).update(dict((str(k), str(v).lstrip("#")) for k, v in table.items()))


def mk_colour(kind, key):
    """the colour the named element is drawn in"""
    try:
        return MK_COLOURS[kind][str(key)]
    except KeyError:
        raise KeyError(u"marker colour: no element colour registered for %s / %s (mk_register it from the table the "
                       u"element is drawn with)" % (kind, key))


def mk_marker(cx, cy, s, colour, size_pt=7.0, r_min=None, style="solid", rim="FFFFFF", rim_mm=0.25, text_col=None,
              y_down=False):
    """one marker centred on (cx, cy) page mm (see the module notes)"""
    import math as _m
    s = u"%s" % s
    col = str(colour).lstrip("#")
    ix0, iy0, ix1, iy1 = fm_ink_box(s, size_pt, True)
    r = 0.5 * _m.hypot(ix1 - ix0, iy1 - iy0) + MK_MARGIN_MM
    if r_min is not None:
        r = max(r, float(r_min))
    ring = [(cx + r * _m.cos(2 * _m.pi * i / 48.0), cy + r * _m.sin(2 * _m.pi * i / 48.0)) for i in range(48)]
    if style == "ring":
        lw = max(rim_mm, 0.25)
        disc = ("poly", ring, MK_PAPER, col, lw)
        tc = text_col or col
        out_r = r + lw / 2.0
    else:
        disc = ("poly", ring, col, rim if rim_mm else None, rim_mm)
        tc = text_col or mk_text_colour(col)
        out_r = r + (rim_mm / 2.0 if rim_mm else 0.0)
    x = cx - (ix0 + ix1) / 2.0
    base = cy + (iy0 + iy1) / 2.0 if y_down else cy - (iy0 + iy1) / 2.0
    size_mm = size_pt * 25.4 / 72.0
    shapes = [disc, ("text", s, x, base, size_mm, tc, True, "L")]
    return shapes, (cx - out_r, cy - out_r, cx + out_r, cy + out_r), r


def mk_put(tp, shapes, name=None):
    """registers a marker in the TextPage tp: its disc as a keep, its glyph as a text that may sit on that disc;
    returns the disc shapes for the caller to draw (before tp.emit draws the glyph)"""
    disc = [s_ for s_ in shapes if s_ and s_[0] != "text"]
    MK_N[0] += 1
    nm = name or u"marker %d" % MK_N[0]
    for s_ in disc:
        if s_[0] == "poly":
            tp.keep(s_[1], "marker", nm)
    for s_ in shapes:
        if s_ and s_[0] == "text":
            tp.put(s_[1], s_[2], s_[3], s_[4] * tp.unit_mm / TP_PT, True, "L", 0.0, nm, "marker", s_[5], allow=(nm,))
    return disc
def bergama_data(name, _c={}):
    """Built-in data kept in Downloads/Bergama/Data/bergama_agriculture_alternatives_data.py (Aras 25 Oct 21:29, scripts shortened): runs its
    section `name` here, as if it were written in this place. The file is read once per run; a missing file or one
    from another version of this script stops the script with a message saying which file to copy."""
    import os as _os, hashlib as _hl
    if not _c:
        p_ = _os.path.join(_os.path.expanduser("~"), "Downloads", "Bergama", "Data", "bergama_agriculture_alternatives_data.py")
        if not _os.path.isfile(p_):
            raise RuntimeError("Data file missing: copy bergama_agriculture_alternatives_data.py from the run kit's Data folder into " + _os.path.dirname(p_))
        with open(p_, encoding="utf-8", newline="") as f_:
            for part_ in f_.read().split("\n#@@ ")[1:]:
                k_, _, b_ = part_.partition("\n")
                _c[k_] = b_
    b_ = _c.get(name)
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != {'NAMES': '0ec3cbab34964fea25289ca36d8bd453', 'FACTS': 'e402c1370c04b7b8df8f86c4eccbf011', 'GEO': '8db5c86b0c11c98efb00cbe4dffb2aff', 'SKETCH_SRC': 'e1cfddbc3f3002be186eb004373795c7', 'STEPS': '5991ab037f9c792682f6ccb2e2e343a2'}.get(name):
        raise RuntimeError("Data file bergama_agriculture_alternatives_data.py is not the one made with this script version (part " + name +
                           "): copy it again from the same run kit as the script")
    exec(compile(b_, "bergama_agriculture_alternatives_data.py:" + name, "exec"), globals())


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
#   name_key(s)                      round 5 (S2): a name as a match key (single spaces, lower case, İ as i)
#   landmark_match(raw, p=None, r_m=60.0, near_m=150.0)   round 5 (S2, A11): the table key a survey / OSM / typed name
#                                     stands for, or None: the table name or an "alias" (whole name); a joined survey
#                                     label that starts with a table name ("Kızıl Avlu Tapınağı Mısır Tanrıları") when
#                                     p lies within near_m of the row's "at"; an "alias_near" word ("Hamam") only
#                                     within r_m of "at"
#   place_label(raw, p=None)         round 5 (S2): the table's one spelling for raw, or None when the table has no row
#                                     (the caller leaves the name out and logs it: never print an unchecked name)
#   street_label(raw)                round 5 (S2): an OpenStreetMap street name as printed: the table's spelling when
#                                     the table has the street (Kınık Caddesi ...), else the OSM tag as mapped
#   keymap_places(box=None)          round 5 (S2, G-R5-3): [(name, (x, y), key)] the table's key-map places ("at" +
#                                     "km"), best first, inside box (survey m) when given
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


def name_key(s):
    """round 5 (S2): a name as a match key: single spaces, lower case, Turkish İ / I handled (İ -> i, I -> ı)"""
    s = u" ".join((s or u"").split()).replace(u"\u0130", u"i").replace(u"I", u"\u0131")
    return s.lower().replace(u"i\u0307", u"i")


def landmark_match(raw, p=None, r_m=60.0, near_m=150.0):
    """round 5 (S2, A11): the names-table key that raw (a survey label, an OSM tag, a typed literal) stands for, or
    None. Rules, in order: (1) the table name or one of its "alias" forms, whole name; (2) raw starts with the table
    name and p (survey m) lies within near_m of the row's "at" (survey labels inside one footprint are joined, e.g.
    "Kızıl Avlu Tapınağı Mısır Tanrıları"); (3) raw is one of the row's "alias_near" words and p lies within r_m of
    "at" (survey "Hamam" -> Tabaklar Hamamı)."""
    k = name_key(raw)
    if not k:
        return None
    rows = NAMES["landmarks"]
    for key, row in rows.items():
        if k == name_key(row["name"]) or k in [name_key(a) for a in row.get("alias") or ()]:
            return key

    def near(row, r):
        at = row.get("at")
        return p is not None and at is not None and (p[0] - at[0]) ** 2 + (p[1] - at[1]) ** 2 <= r * r
    for key, row in rows.items():
        nk = name_key(row["name"])
        if k.startswith(nk + u" ") and near(row, near_m):
            return key
    for key, row in rows.items():
        if k in [name_key(a) for a in row.get("alias_near") or ()] and near(row, r_m):
            return key
    return None


def place_label(raw, p=None):
    """round 5 (S2, G-R5-11): the table's one spelling for a place name, or None when the table has no row for it"""
    key = landmark_match(raw, p)
    return landmark_name(key) if key else None


def street_label(raw):
    """round 5 (S2, G-R4-11): a street name as printed: the table's spelling when the table records the street, else
    the OpenStreetMap tag as mapped (a public source, Turkish as tagged)"""
    key = landmark_match(raw)
    return landmark_name(key) if key else u" ".join((raw or u"").split())


def keymap_places(box=None):
    """round 5 (S2, G-R5-3): the places a key map may name: [(name, (x, y), key)] for every table row with "at" and
    "km", in "km" order, inside box = (x0, y0, x1, y1) survey m when given"""
    out = []
    for key, row in NAMES["landmarks"].items():
        at, rk = row.get("at"), row.get("km")
        if at is None or rk is None:
            continue
        if box is None or (box[0] <= at[0] <= box[2] and box[1] <= at[1] <= box[3]):
            out.append((rk, row["name"], (float(at[0]), float(at[1])), key))
    out.sort(key=lambda r: r[0])
    return [(n, p, k) for _, n, p, k in out]
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
LOG_DIR = bg_logs()                       # Aras 25 Oct 09:34-09:35: every script's log here


def write_log(text):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, "bergama_agriculture_alternatives_log.txt"), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    return text

# v1 24 Oct: all files under Downloads/Bergama/ (Aras rule). v10 (round 5, G-R5-12, C2): nothing goes to output/ any
# more; the items and results go to cached/booklet/<AG_FOLDER>/ (the folder name the booklet and readers already use)
AG_FOLDER = "Bergama_agriculture_alternatives"
AG_PAGE = "p18"                    # v11 (round 6, PLAN §2.1): "Where the clean water goes, and what it grows" (v10 p21)
CUR_PAGE = [AG_PAGE]               # v11: the page the blocks being drawn belong to (p17 ladder / p18), for Sources rows
SRC_PAGE = {}                      # v11: source text -> the page that first cited it
# built-in geometry and tables (survey coordinates, m): around2 extent, site frame, WorldCover classes clipped to the
# extent (outside / inside the site), Selinos and other streams, FAO-56 net irrigation per water year (C1), corridor cover
bergama_data("GEO")

# ------------------------------------------------------------------ live numbers from the water balance (Thread 2)
# The water balance script writes its results on every run; this script reads them, so storage and the share covered
# are never typed in here. Searched in this order; the first file found wins.
LIVE_FILES = [os.path.join(bg_cache("Bergama_water_balance_analysis"), "water_balance_results.json"),   # 27 Oct: cached/
              os.path.join(bg_output("Bergama_water_balance_analysis"), "water_balance_results.json"),  # v2.6 and older
              os.path.join(os.path.expanduser("~"), "Downloads", "Bergama_water_balance_analysis", "water_balance_results.json")]   # old place, read fallback
# fallback: the cloud copy research/water_balance/water_balance_results_default.json (default lands, 24 Oct 08:23)
DEFAULT = json.loads('{"cutoff":{"orchard olive + cropland cotton":{"central":{"storage_m3":375000,"covered_pct_1in5_dry":99.2,"delivered_m3_per_year":336093}},"orchard olive + cropland tomato":{"central":{"storage_m3":350000,"covered_pct_1in5_dry":99.7,"delivered_m3_per_year":310094}}},"farm_demand_m3":{"orchard olive + cropland cotton":{"mean":339980,"median":348773,"wet5":315782,"dry5":356580,"dry10":382453,"min":278845,"max":393001,"dry5_year":2006},"orchard olive + cropland tomato":{"mean":311982,"median":319136,"wet5":288317,"dry5":334143,"dry10":343054,"min":251458,"max":362453,"dry5_year":2021}},"net_irrigation_mm":{"olive":{"mean":614.3,"median":619.5,"wet5":519.6,"dry5":720.1,"dry10":725.2,"min":415.2,"max":822.7},"cotton":{"mean":853.2,"median":875.6,"wet5":789.5,"dry5":891.8,"dry10":962.6,"min":703.1,"max":981.9},"maize":{"mean":722.7,"median":740.8,"wet5":675.4,"dry5":761.8,"dry10":816.2,"min":605.7,"max":835.7},"tomato":{"mean":781.0,"median":801.3,"wet5":719.7,"dry5":837.0,"dry10":860.8,"min":632.5,"max":903.1}},"lands":{"cropland_ha":34.9,"orchard_ha":1.34,"cropland_crops":"cotton,tomato"}}')
DEFAULT_NOTE = "water balance default-lands copy, 24 Oct"   # v1.4: the log says when it is used

def live():
    """storage, share covered and need per mix (cost cut-off, central case), farm areas, crops and net need per crop"""
    d, src = None, DEFAULT_NOTE
    for p in LIVE_FILES:
        try:
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
            src = "water balance results of " + time.strftime("%d %b %H:%M", time.localtime(os.path.getmtime(p)))
            break
        except Exception:
            d = None
    if d is None: d = DEFAULT
    mixes = [m for m in d["cutoff"] if m in d["farm_demand_m3"]]
    L = dict(storage_m3=[d["cutoff"][m]["central"]["storage_m3"] for m in mixes],
             farm_share_dry5_pct=[d["cutoff"][m]["central"]["covered_pct_1in5_dry"] for m in mixes],
             farm_need_dry5_m3=[d["farm_demand_m3"][m]["dry5"] for m in mixes],
             cropland_ha=d["lands"]["cropland_ha"], orchard_ha=d["lands"]["orchard_ha"],
             crops=[c.strip() for c in str(d["lands"].get("cropland_crops", "")).split(",") if c.strip()],
             net=d["net_irrigation_mm"])
    L["year_split"] = (d.get("design") or {}).get("year_split")      # v3: water balance v4 and newer
    L["design_mix"] = (d.get("design") or {}).get("mix", "")
    return L, src

def span(v):
    return (min(v), max(v)) if isinstance(v, (list, tuple)) else (v, v)

# ------------------------------------------------------------------ colours (palette v1.4 core roles)
C = dict(ground="E2E0D4", paper="EFEDE6", faint="D8D5CC", structure="B0AC9C", ink2="847E75", ink="4A3F35",
         green_deep="495338", green_mid="727A4E", green_light="8C9969", water_deep="5D7F8D", water="91ADB4",
         water_light="C1D3DB", accent="8B3A3F", accent_deep="633131", white="FFFFFF",
         field="BDB57A", orchard="70754C", tree="89986A", grass="C9CDB0", shrub="A2B6B5", olive="5C7A86")

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
    """v11 (G6-6): a hue of the round 6 category table (common/hues.py, round 6 S1) as 6 hex digits"""
    return str(hue(code, rank)).lstrip("#").upper()


# v11 (round 6, G6-6: one hue per category, darker = more important; PLAN §2.6, H1 p19 rows): the roles the p18 blocks
# and the farms map use, remapped to the table once: farms AGR (dry year / farms we feed / fields r1, normal year /
# orchards r2), the strip WAT r2, "left over" CTX r4. The olive lane of the timeline takes AGR r2 (history_line).
C.update(accent=_hu("AGR", 1), accent_deep=_hu("AGR", 2), green_deep=_hu("AGR", 1), green_light=_hu("AGR", 2),
         water_deep=_hu("WAT", 2), water=_hu("WAT", 3), faint=_hu("CTX", 4), field=_hu("AGR", 3))

# v9 (round 4, G-R4-1): ² and ³ are the embedded Arial's own glyphs again (pdf_fonts.py since 28 Oct): the v3 raised
# 0.6 x digit printed at 4.2-4.5 pt, under the booklet's 6 pt minimum the text placer enforces; the unembedded
# Helvetica that lost them in some viewers is gone. (v3's SUP, SUP_K, SUP_UP and sup_runs deleted.)
# v10: the minimal vector PDF writer (Page, write_pdf, its WinAnsi tables) is gone with the sheet (G-R5-12).
_AG_MARK = re.compile(r"\{src:agsrc(\d+)\}")


def text_w(s, size, bold=False):
    """v9 (round 4, G-R4-1): the REAL Arial advance width (font_metrics.fm_width) of s at size pt, in mm; the
    Helvetica table (common/text_w.py) is gone (a missing font raises FontMissing, no estimate).
    v10: a source mark {src:agsrcN} is measured as the "[N]" it prints as, so the blocks keep v9's measures"""
    return fm_width(_AG_MARK.sub(r"[\1]", u"%s" % s), size, bold)


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

AG_COMPASS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")   # v10: a label's other spots after its first (item_export)
AG_TAG0 = ("annotations", None)      # v11 (G6-9): an untagged shape = its block's annotations (element = block id)
AG_GRP = [0, set(), set(), 0]        # v11: this press [layers, kinds, elements, shapes without a tag] (groups log)


class AgRec:
    """v10 (round 5 S9, G-R5-12; replaces v9's Page and write_pdf, after the water balance's WbRec): the same drawing
    calls as the old sheet Page, but nothing is written to a PDF. Everything a block draws is RECORDED as common shape
    tuples in page mm, y up (poly / line / text); ag_export_block turns them into one chart drawing and every text into
    a label item anchored where v9 set it (first position = that spot; the booklet moves, sizes and checks it).
    heads / notes: the block's heading and its text line (text items of the block's group, not drawn); keeps: the boxes
    v9 kept free of text (bars, icons, squares). No TextPage, no check, nothing raises here.
    v11 (round 6, G6-9): every recorded shape carries the element it belongs to, gs[i] = (kind, element id), set by
    tag() before the element is drawn (default AG_TAG0: the block's own annotations, see ag_export_block)."""
    def __init__(self):
        self.shapes, self.heads, self.notes, self.keeps = [], [], [], []
        self.gs, self.tg_ = [], AG_TAG0

    def tag(self, kind, eid):
        """v11 (G6-9): the shapes drawn from now on belong to element eid of kind (IX_GRP_KINDS)"""
        self.tg_ = (kind, u"%s" % eid)

    def _add(self, sh):
        self.shapes.append(sh)
        self.gs.append(self.tg_)

    def image(self, x, y, w, h, path, clip=None):
        """v11: a raster image (JPEG) in the box (x, y)..(x + w, y + h), page mm y up, shown inside clip (x0, y0, x1, y1)"""
        self._add(("image", float(x), float(y), float(w), float(h), path, None, False,
                   tuple(float(v) for v in clip) if clip else None))

    def tgroup(self, start=True):
        """v9's word blocks: kept as a call (the booklet sets each label on its own; the group id is the block's)"""
        return None

    def keep(self, box, name, kind="drawing"):
        """a drawing box (x0, y0, x1, y1, page mm y up) no label may cover (exported as a keep area)"""
        self.keeps.append((tuple(box), kind, name))

    def rect(self, x, y, w, h, fill=None, stroke=None, lw=0.2):
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill, stroke, lw, True)

    def poly(self, P, fill=None, stroke=None, lw=0.2, closed=False, dash=None, alpha=None):
        self.path([P], fill, stroke, lw, closed, dash, alpha)

    def path(self, rings, fill=None, stroke=None, lw=0.2, closed=True, dash=None, alpha=None):
        """several rings in one path (a fill keeps its holes, even-odd); alpha = opacity 0-1"""
        R = [[(float(x), float(y)) for x, y in P] for P in rings if len(P) >= 2]
        if not R:
            return
        if fill:
            rr = [r for r in R if len(r) >= 3]
            if rr:
                self._add(("poly", rr, fill, stroke, lw if stroke else 0.0,
                                    tuple(dash) if (dash and stroke) else None, None,
                                    alpha if (alpha is not None and alpha < 0.995) else None))
            return
        if stroke:
            for r in R:
                self._add(("line", r + [r[0]] if (closed and len(r) >= 3) else r, stroke, lw,
                                    tuple(dash) if dash else None))

    def line(self, P, col, lw=0.25, dash=None):
        self.path([P], None, col, lw, False, dash)

    def circle(self, x, y, r, fill=None, stroke=None, lw=0.2):          # v1.2: for the pictograms
        self.poly([(x + r * math.cos(k * math.pi / 12), y + r * math.sin(k * math.pi / 12)) for k in range(24)], fill, stroke, lw, True)

    def text(self, s, x, y, size, col="4A3F35", bold=False, align="L", halo=None, allow=(), positions=None):
        """one label, size in pt, baseline y, align L / C / R at x (v9's spot = its first position). halo and allow
        (v9's knock-out and the keeps it could sit on) are kept as arguments: the booklet places labels now.
        positions: the other spots after the first (default AG_COMPASS)"""
        if not s or not (u"%s" % s).strip():
            return
        self._add(("text", u"%s" % s, float(x), float(y), size * IX_PT, col, bool(bold), align or "L",
                   tuple(positions) if positions else None))


# ------------------------------------------------------------------ shared helpers
def fmt(v): return "{:,.0f}".format(v)
def fmt1(v): return "{:,.1f}".format(v)
def rnd(v, step=1000): return int(round(v / step) * step)
EFF = 0.90          # drip application efficiency, as the water balance (key figures "basis": "drip 90 %")

NET = {}            # net irrigation mm per crop from the water balance results (mean, dry5 = 1-in-5 dry year), set in ag_items()

def gross_m3_ha(crop, year):
    if crop == "mix":                  # field crops weighted by their 2025 Bergama areas
        w = {c: TUIK_2025_DA[c] for c in ("cotton", "maize", "tomato") if c in NET}
        return sum(gross_m3_ha(c, year) * v for c, v in w.items()) / sum(w.values())
    return NET[crop]["mean" if year == "normal" else "dry5"] / EFF * 10.0     # 1 mm on 1 ha = 10 m3

SRC_KEY = []          # v1.6: sources printed as [n] on pages 1-3, numbered once for the sheet; v10: Sources rows agsrcN
LOG_NOTES = []        # v1.6: what the layout left out (log)

def cite(src):
    """v1.2 (water board v1.6 method): the number of a source in the sheet's key (v1.6: page 4), as "[n]".
    v4 (MIRAQUA 28 Oct, F5): "" for a source that is not public online (F5_OFF): no mark, not in the key.
    v5 (T4a, D13): also "" for a source naming our own model run or method (F5_INTERNAL); status words cut (F5_STATUS).
    v10 (G-R5-12): the mark is "{src:agsrcN}" (N = v9's number; ag_items writes Sources row agsrcN for it; the booklet
    prints its own number), measured as "[N]" (text_w)."""
    if not src or src in F5_OFF or any(t in src for t in F5_INTERNAL):
        return ""
    src = F5_STATUS.sub("", src).strip()
    if src not in SRC_KEY: SRC_KEY.append(src)
    SRC_PAGE.setdefault(src, CUR_PAGE[0])          # v11: its Sources row goes on the page that first cites it
    return u"{src:%s}" % (AG_SRC % (SRC_KEY.index(src) + 1))


def cited(s, *srcs):
    """v4 (F5): s with its [n] marks after one space, or s alone when none of its sources is public"""
    mk = "".join(cite(q) for q in srcs if q)
    return s + (" " + mk if mk else "")

def wrap(s, size, w, bold=False):
    """greedy wrap at real widths (size pt, w mm); v9 (G-R4-2): never a one-word last line: the last word of the
    line before moves down while that line keeps two words or more and the last line still fits"""
    out, line = [], ""
    for word in s.split(" "):
        t = (line + " " + word).strip()
        if text_w(t, size, bold) > w and line: out.append(line); line = word
        else: line = t
    if line: out.append(line)
    while len(out) >= 2 and len(out[-1].split()) < 2 and len(out[-2].split()) >= 3:
        a = out[-2].split()
        t = a[-1] + " " + out[-1]
        if text_w(t, size, bold) > w:
            break
        out[-2], out[-1] = " ".join(a[:-1]), t
    return out

# ------------------------------------------------------------------ v2 (Aras 27 Oct, Prompt 5): plant and crop photos
# The photos and the "English (Turkish)" names come from src/common/plant_photos.py (one cache folder for every script,
# every photo PHOTO_W x PHOTO_H mm). Each photo's credit is a source mark after its name.
# v10 (G-R5-12): no frames, no PyMuPDF: each photo is a photo item (its JPEG in cached/plant_photos/, never put into a
# PDF here) with its name as the caption; the booklet sets it (ag_crops_items).
PHOTO_GOT = {}                       # key -> (jpeg path or None, credit or None, why not), read once a press
PHOTO_LOG, PHOTO_STATE = [], {}      # plant_photos' own notes (web fetch) and its offline flag
PHOTO_N = [0, 0]                     # v10: this press [photo items exported, photos asked for]


def photo_get(key):
    """v2: (jpeg path or None, credit or None, why not) of a plant in PLANTS, once a press; never raises"""
    if key not in PHOTO_GOT:
        try:
            PHOTO_GOT[key] = plant_photo_of(key, PHOTO_LOG, PHOTO_STATE)
        except Exception as ex:
            PHOTO_GOT[key] = (None, None, "%s: %s" % (type(ex).__name__, ex))
    return PHOTO_GOT[key]


def photo_mark(key):
    """v2: the [n] of a plant photo's credit (its key on the sources page); "" when there is no photo"""
    p, credit, _ = photo_get(key)
    return cite(credit) if p and credit else ""


def name_lc(key):
    """v2: a plant's name in running text: "olive (Zeytin)" """
    s = plant_name(key)
    return s[:1].lower() + s[1:]


def name_caps(key):
    """v2: a plant's name in a capitals heading, the Turkish part with the dotted İ: "OLIVE (ZEYTİN)" """
    en, _, tr = plant_name(key).partition(" (")
    return en.upper() + ((" (" + tr.replace(u"i", u"İ").upper()) if tr else "")


def crop_word(key):
    """v4 (MIRAQUA 28 Oct, G11): a crop key as a short printed word, the English name of the shared table: "maize" ->
    "corn", "cotton" -> "cotton"; a key the table does not have stays as it is"""
    return plant_name(key).partition(" (")[0].lower() if key in PLANTS else key


def photo_log():
    """v2 (v10: was put_photos): the photos' log lines: how many went out as photo items, and why each missing one
    is missing (never raises)"""
    out = ["photos: %d of %d exported as photo items (cached/plant_photos)%s" % (
        PHOTO_N[0], PHOTO_N[1], " · FLAG %d missing" % (PHOTO_N[1] - PHOTO_N[0]) if PHOTO_N[0] < PHOTO_N[1] else "")]
    out += ["  no photo: %s (%s)" % (plant_name(k), v[2] or "not loaded") for k, v in PHOTO_GOT.items() if not v[0]]
    out += ["  " + t for t in PHOTO_LOG]
    return "\n".join(out)


# ------------------------------------------------------------------ pictograms and tiles
# v5 (T4a, 29 Oct, 02 §2): every pictogram comes from the shared icon set (common/icons.py); the script's own icon()
# with its 10 x 10 grid drawings is gone. AG_ICONS: tile key -> (icons.py name, crossed out).
AG_ICONS = {"nowater": ("drought", False), "cotton": ("field", False), "olive": ("olive", False),
            "drip": ("drip", False)}


def _ag_put(pg, shapes):
    """icons.py / marker.py house shapes ("poly", ring, fill, stroke, lw) / ("line", pts, colour, lw) / ("text", s, x,
    baseline y, size mm, colour, bold, align), page mm y up, on this Page (v9: text for the markers' glyphs)"""
    for sh in shapes:
        if sh[0] == "poly":
            pg.poly(sh[1], fill=sh[2], stroke=sh[3], lw=sh[4] or 0.2, closed=True)
        elif sh[0] == "text":
            pg.text(sh[1], sh[2], sh[3], sh[4] / 0.3528, sh[5], sh[6] if len(sh) > 6 else False,
                    sh[7] if len(sh) > 7 else "L")
        else:
            pg.line(sh[1], sh[2], sh[3])


def _ag_icon(pg, kind, x, y, sz):
    """the icon set's pictogram for a tile key in the square (x, y - sz)-(x + sz, y)"""
    name, crossed = AG_ICONS.get(kind, (kind, False))
    _ag_put(pg, ico_draw(name, x + sz / 2.0, y - sz / 2.0, sz))
    if crossed:
        _ag_put(pg, ico_cross(x + sz / 2.0, y - sz / 2.0, sz))

def tiles(pg, x, y, w, items, cols=1, s=1.0, boxes=None):
    """v1.2 (water board v1.6): facts as tiles: pictogram, keyword heading, the key figure large, short keyword lines and
    the source number. items = [(pictogram, heading, figure or None, [keyword lines], source or None)]. Returns the bottom y.
    v8 (G17): no frame and no fill: the tiles stand apart by whitespace on the grid; boxes gets each pictogram's square."""
    k = 0.3528
    fh, fb, ft = 8.5 * s, 15.0 * s, 7.0 * s
    ic, pad, g = 12.0 * s, 2.2 * s, 2.4 * s
    tw = (w - (cols - 1) * g) / cols
    txw = tw - ic - 3 * pad
    lay = []
    for kind, head, big, lines, ref in items:
        lines = list(lines or [])
        if ref: lines = lines[:-1] + [((lines[-1] + " ") if lines else "") + cite(ref)]
        L3 = (wrap(head, fh, txw, True), wrap(big, fb, txw, True) if big else [], [q for ln in lines for q in wrap(ln, ft, txw)])
        hh = pad * 2 + (len(L3[0]) * fh * 1.25 + len(L3[1]) * fb * 1.15 + len(L3[2]) * ft * 1.3 + (fh * 0.3 if L3[1] else 0)) * k
        lay.append((kind, big, L3, max(hh, ic + 2 * pad)))
    yy = y
    for r0 in range(0, len(lay), cols):
        row = lay[r0:r0 + cols]
        rh = max(t[3] for t in row)
        for c_, (kind, big, L3, _) in enumerate(row):
            tx = x + c_ * (tw + g)
            _ag_icon(pg, kind, tx + pad, yy - pad, ic)
            if boxes is not None:
                boxes.append((tx + pad, yy - pad - ic, tx + pad + ic, yy - pad))
            pg.keep((tx + pad, yy - pad - ic, tx + pad + ic, yy - pad), "tile icon " + kind, "icon")   # v9
            pg.tgroup()                              # v9 (G-R4-1): the tile's lines are one word block
            lx, ly = tx + 2 * pad + ic, yy - pad
            for ln in L3[0]:
                ly -= fh * 1.25 * k; pg.text(ln, lx, ly + fh * 0.25 * k, fh, C["ink"], True)
            if L3[1]: ly -= fh * 0.3 * k
            for ln in L3[1]:
                ly -= fb * 1.15 * k
                pg.text(ln, lx, ly + fb * 0.2 * k, fb, C["accent"] if big in FLAGGED else C["green_deep"], True)
            for ln in L3[2]:
                ly -= ft * 1.3 * k; pg.text(ln, lx, ly + ft * 0.3 * k, ft, C["ink"])
            pg.tgroup(False)
        yy -= rh + g
    return yy + g

FLAGGED = ("NOT KNOWN", "not designed")         # big figures that say "no data": in the accent colour


# ------------------------------------------------------------------ page 1: what each cubic metre grows
# v4 (MIRAQUA 28 Oct, F5: public online sources only): the public sources keep their words, the project's own file
# pointers go from the printed key (kept here: NEWS research/water_data/03 §3; TUIK library/research/crops_2026-10-24
# §1.24-1.25; NET_REF research/water_balance/tables/C1). G11: corn, not maize, where printed (data keys stay "maize").
NEWS = "news: Ajans Bakırçay 19.03.2025"
TUIK = "TÜİK Bitkisel Üretim, Bergama 2025"
KAYA = "Kaya et al. 2017, Irrig. Drain. 66(5):820-827, Tables II, III, VI, pp.823-826 (deficit saving: Table II, S0.50 and S0.25 vs control)"
ITB = "İzmir Ticaret Borsası cotton report 2025, p.5"
NET_REF = ("net irrigation: FAO-56 (Allen et al. 1998), MGM/WMO 17742 normals, ERA5 1991-2025 scaled; per ha = FAO-56 "
           "daily soil balance net need (34 water years, Bergama climate) / 0.90 drip")
TAGEM = ("TAGEM/DSİ 2017 §12, Bergama station 17742 tables (net = ETc - 0.8 rain): cotton 829 mm, corn 765, "
         "tomato 606-825, olive 502-603")   # v5 (D13): was our check against our own figures
# v1.2: the context sentences as tiles (pictogram, heading, big figure, keyword lines, source)
# v2 (Aras 27 Oct, Prompt 5): the crops they name as "English (Turkish)"; figures and sources as they were
CONTEXT = [
    ("nowater", "DROUGHT 2025: NO WATER-HUNGRY CROPS", "7,500 ha",
     ["%s, %s, fodder · Bergama villages" % (name_lc("maize"), name_lc("cotton")),
      "no water for second crops · DSİ + Ministry"], NEWS),
    ("cotton", name_caps("cotton") + ": BERGAMA'S BIGGEST CROP", "37 %",
     ["of 26,800 ha field crops · 2025"], TUIK),
    ("olive", name_caps("olive") + " CAN TAKE LESS · MEMECIK, DRIP", "-72 % water",
     ["İzmir station 2008-10 · 175 vs 622 mm a season", "24.9 vs 27.8 kg a tree: no significant loss",
      "highest oil content"], KAYA),
    ("drip", "TODAY'S IRRIGATION ON THE FARMS", None, ["some Bergama growers moved to drip"], ITB),
]
DEFICIT = (1 - 350.0 / 622, 1 - 175.0 / 622)   # olive water saved: S0.50 and S0.25 against the control SC, Kaya et al. 2017 Table II
# Bergama district areas 2025, da (TÜİK MEDAS export, library/research/crops_2026-10-24/bergama_crops_irrigation_v1.md §1.25):
# the share of each crop the water balance models, used for the district mix row
TUIK_2025_DA = dict(cotton=99963, maize=24532 + 35491, tomato=13740 + 11268, olive=65978 + 21068)

COTTON_H = ("h01 §3 'Then vs now', cotton / textiles: \"Tersane cotton (16th c.); ginning 1861; Sümerbank (1954/60–2008)\" "
            "(s18, s106; library/research/selinos_bergama_history_context_v1.md line 111)")
OLIVE_H = ("h01 §2 + §5 P04: \"19th-c. olive-oil machinery in the Red Hall S rotunda\" (s25; "
           "selinos_bergama_history_context_v1.md lines 77, 139)")
# v1.6 (Aras 27 Oct, p24 + spec §3): the farm history behind the farms the water serves, as a timeline, in the
# card's own words and years (h01 §3 line 111, §2 line 77, §5 P04 line 139); today's areas from TÜİK 2025 (above)
HISTORY = [("cotton", "Tersane cotton (16th c.)", 1500, 1600, COTTON_H),
           ("cotton", "ginning 1861", 1861, None, COTTON_H),
           ("cotton", "Sümerbank (1954/60–2008)", 1954, 2008, COTTON_H),
           ("olive", u"19th-c. olive-oil machinery · %s S rotunda" % landmark_name("kizil_avlu"), 1800, 1900, OLIVE_H)]
# v9 (round 4, G-R4-11): the landmark's Turkish name from the shared names table (was "Red Hall"); OLIVE_H keeps the
# card's own words (a record, never printed: F5_OFF)


def history_line(pg, x, top, w, h):
    """a timeline 1500-2030 with the cotton (above) and olive (below) history, inside the box x..x + w, top..top - h.
    v8 (round 3, G3): no leader lines. v9 (round 4, P19.1): booklet p19 group 5's first block (crop ag1_history,
    AG_HIST_W x AG_HIST_H): the group's heading in the band on top, the line "Bergama's cotton and olive" under it, the
    timeline AG_HIST_YA under the top (cotton labels over it, olive labels under the years); its old title "WHY THE
    STORED WATER GOES TO FARMS" is the group heading's job now.
    v10 (round 5, C1 + G-R5-12): the heading and the line under it are the group's heading and note (text items); the
    v1.6 Placer is gone (it only chose label positions, and v9 RAISED TextError when a label found no lane): each label
    is exported at the first spot Placer tried (centred over its span for cotton, under it for olive, 1.2 mm off the
    line) with the spots on the same side next; the booklet places it (a label with no free spot is its WARNING, never a
    stop). Returns its bottom y.
    v11 (round 6 S7, SON page19 = v8.3): the v8.3 title "WHY THE STORED WATER GOES TO FARMS" again (the crops have
    their own heading "THE CROPS"), 4 columns wide (AG_HIST_W); first spots chosen so no two labels meet at that width
    (SON: "Sümerbank" over "ginning 1861"): Tersane from 1500 to the right, ginning one lane higher, Sümerbank ending
    at 2008; the olive lane under the year numbers (v10 put it on them) in AGR r2 (cotton AGR r1)."""
    ag_heading(pg, "WHY THE STORED WATER GOES TO FARMS", x, top)
    pg.tag("annotations", "timeline_axis")
    pg.notes.append("Bergama's %s and %s" % (name_lc("cotton"), name_lc("olive")))   # v2
    ya = top - AG_HIST_YA
    # v9.2: the axis starts 3.2 mm in (was 2.0): the centred "1500" under its tick reached 0.75 mm past the crop's left
    # edge (Aras 1 Nov 17:30); the right end stays 2.0 mm in
    X = lambda yr: x + 3.2 + (w - 5.2) * (yr - 1500) / 530.0
    pg.line([(X(1500), ya), (X(2030), ya)], C["ink"], 0.3)
    for yr in range(1500, 2001, 100):
        pg.line([(X(yr), ya - 0.8), (X(yr), ya + 0.8)], C["ink"], 0.3)
        pg.text(str(yr), X(yr), ya - 3.4, 7, C["ink2"], align="C")
    for lane, lab, a, b, ref in HISTORY:
        col, up = (C["accent"], True) if lane == "cotton" else (C["green_light"], False)
        pg.tag("fields", "%s_%d" % (lane, a))
        yb = ya + (1.0 if up else -1.0)
        if b:
            if lab.startswith("Sümerbank"):           # 1954 vs 1960 (card: conflicting dates): dashed until 1960
                pg.line([(X(1954), yb), (X(1960), yb)], col, 1.0, (0.6, 0.4))
                pg.line([(X(1960), yb), (X(2008), yb)], col, 1.0)
            else:
                pg.line([(X(a), yb), (X(b), yb)], col, 1.0)
        else:
            pg.circle(X(a), yb, 0.8, fill=col)
        ax, ay = X((a + b) / 2.0 if b else a), yb + (0.6 if up else -0.6)
        ty = ay + 1.2 if up else ay - 3.0 - 7 * 0.3528          # v11: olive under the year numbers (ya - 3.4)
        al = "C"
        if lab.startswith("Tersane"):
            ax, al = X(1500), "L"
        elif lab.startswith("ginning"):
            ty += 3.2                                           # one lane higher: Sümerbank ends under it
        elif lab.startswith("Sümerbank"):
            ax, al = X(2008), "R"
        pg.text(cited(lab, ref), ax, ty, 7, col, align=al,
                positions=("N", "NE", "NW", "E", "W", "S", "SE", "SW") if up else
                ("S", "SE", "SW", "E", "W", "N", "NE", "NW"))
    return top - h


CROP_ROW = ("olive", "cotton", "maize", "tomato")   # v2 (Aras 27 Oct, Prompt 5): the crops page 1 compares


def ag_crops_items(ix, prio, group):
    """v2 (Aras 27 Oct, Prompt 5): "THE CROPS": page 1's crops as photos (the one photo size of the booklet, PHOTO_W x
    PHOTO_H, cut to that proportion about the centre), the name "English (Turkish)" and the photo's credit under each.
    v10 (round 5, G-R5-12; was crop_row): each photo is a photo item (file in cached/plant_photos/) with its name +
    credit mark as its caption, in the group of the timeline (v9 group 5: one heading "THE CROPS, THEN AND NOW" for
    both); a crop without a photo is a note "no photo: <name>: <why>" (v4 G12's words) and a WARNING."""
    for key in CROP_ROW:
        p, _cr, why = photo_get(key)
        PHOTO_N[1] += 1
        mk = photo_mark(key)
        if p:
            cap = ix.text(AG_PAGE, plant_name(key) + ((" " + mk) if mk else ""), "caption", bold=True, group=group,
                          priority=prio, id="ag1_crops_%s_caption" % key)
            pid = ix.photo(AG_PAGE, p, caption=cap, source=_ag_src_key(mk), id="ag1_crops_%s" % key)
            _ag_item_set(ix, pid, group=group, priority=prio, aspect=round(PHOTO_W / PHOTO_H, 4))
            PHOTO_N[0] += 1
        else:
            ix.text(AG_PAGE, u"no photo: %s: %s" % (plant_name(key), why or u"not loaded"), "note", group=group,
                    priority=prio, id="ag1_crops_%s_none" % key)
            ix.warn(AG_PAGE, "photo", u"no photo for %s: %s" % (plant_name(key), why or u"not loaded"))


# ------------------------------------------------------------------ v3 (Prompt 6): the stream comes first
AG_BAR_RP, AG_BAR_H, AG_BAR_O = 9.3, 3.8, 4.4   # v8: bars' largest row pitch, bar, dry bar offset, mm (v7 14, 5, 6)
# v9 (round 4, P19.1; spec revision_2026-11-01_round4/handover/S6b_p19_design_spec.md): booklet p19 is rebuilt as
# story groups, one heading each (GRID_TYPE heading, in a band AG_HEAD tall on top of every block, so the blocks of a
# booklet row share the content top). The crops' sizes, mm, drawn at 1:1 ("bk_w"; page columns in brackets):
#   row 2  ag1_stream 260 x 40 (8)  "HOW MUCH WATER REACHES THE FARMS"  | the water board's wb_decision (4)
#   row 3  ag1_bars   194 x 72 (6)  "HECTARES ONE STORAGE IRRIGATES, BY CROP" | ag1_context 194 x 72 (6) "WHY CROP CHOICE
#          IS THE LEVER": the reading (ag1_reading's squares and ratio, no crop of its own now) on top, the 4 tiles under
#   row 4  ag1_history 260 x 34 (8) "THE CROPS, THEN AND NOW" | ag1_crops 128 x 34 (4), the photos at the one booklet
#          photo size
# v10 (round 5, G-R5-12): v9's TextPage per crop (a collision RAISED) is gone: each block is recorded (AgRec) and
# exported as one chart drawing whose words the booklet places (ag_export_block); the sizes below stay the blocks' own.
AG_HEAD = 6.0                        # v9: the group heading band, mm
AG_STREAM_W, AG_STREAM_H = grid_w(8), 40.0
# v11 (round 6 S7, G6-1: SON page19 = the v8.3 page): the v8.3 sizes again (bars 7 columns x 66, context 5 x 66, the
# reading, the timeline and the crops 4 x 31 each; target frames revision_2026-11-04_round6/plan_findings/
# frames_p14-22.md page 18: bars 231 x 65, context 155 x 59, reading / timeline / crops 126 x 36-39 mm)
AG_BARS_W, AG_BARS_H = grid_w(7), 66.0
AG_CTX_W, AG_CTX_H = grid_w(5), 66.0
AG_HIST_W, AG_HIST_H = grid_w(4), 32.0
AG_READ_W, AG_READ_H = grid_w(4), 31.0
AG_HIST_YA = 21.0                    # v11: the timeline's line under the block's top, mm (v9 23)
AG_ST_LW = 76.0                      # ag1_stream: the left column (headline, key), mm
AG_ST_RW = 60.0                      # ag1_stream: room after the bars for the through-the-store lines, mm (v8 57)
AG_DBOX = {}                         # v8 (G3): crop id -> drawing boxes (page mm y up), page 1
PRIORITY =[(1, "stream: summer strip"), (2, "on-site planting, on the strip's water"), (3, "farms outside the site")]
AG_STEP_MM = 4.0                     # the flow-step marker's least size (marker.py), mm


def ag_heading(pg, text, x, top):
    """v9 (P19.1): a story group's ONE heading. v10 (P21.1, G-R5-12): recorded as the block's heading text item (same
    group id as its drawing and texts), not drawn; x and top kept as arguments (the booklet sets it over its block)"""
    pg.heads.append(text)


def _ag_src_key(mk):
    """v10: the source key of a {src:key} mark ("" or None -> None)"""
    m = re.search(r"\{src:([^}]+)\}", mk or "")
    return m.group(1) if m else None


def _ag_item_set(ix, iid, **kw):
    """v10: extra keys on an exported item (ix.photo takes no group or priority)"""
    for its in ix.d["pages"].values():
        for it in its:
            if it.get("id") == iid:
                it.update(kw)
                return it
    return None


def _ag_grp(kind, eid):
    """v11 (G6-9): the shared module's group context (common/item_export.py ix_group, round 6 S2); a no-op without it"""
    f = globals().get("ix_group")
    if f:
        try:
            return f(kind, eid)
        except Exception:
            pass
    import contextlib
    return contextlib.nullcontext()


def ag_export_block(ix, pg, did, prio, x0, top, W, H, cut=0.0, page=None):
    """v10 (round 5 S9, G-R5-12, P21.1): one v9 booklet block (x0..x0 + W, top - H..top, page mm y up, as drawn by its
    v9 function into the recorder pg) -> one chart drawing `did` (units mm, no scale bar, priority = reading order,
    group = did) with every shape; every text as a label anchored where v9 set it; the heading and note as text items
    of the same group; the boxes v9 kept free of text as keep areas (not the reading squares, whose crop words sit
    inside them). cut: mm of the empty heading band left off the top (the heading is its own item now).
    v11 (round 6, G6-9): the shapes go out as one layer per run of the same element, named "kind/element", inside
    ix_group(kind, element) (a shape with no tag = AG_TAG0: kind annotations, element = the block id); page = the
    booklet page (default AG_PAGE)."""
    pid = page or AG_PAGE
    D = ix.drawing(did, pid, (x0 - 0.5, top - H - 0.5, x0 + W + 0.5, top - cut), units="mm", dkind="chart",
                   scale_bar=False, priority=prio, group=did)
    for i, t in enumerate(pg.heads):
        ix.text(pid, t, "heading", group=did, priority=prio, id=did + "_head" + ("_%d" % (i + 1) if i else ""))
    for i, t in enumerate(pg.notes):
        ix.text(pid, t, "note", group=did, priority=prio, id=did + "_note" + ("_%d" % (i + 1) if i else ""))
    for s in pg.shapes:
        if s[0] == "text":
            ix.text(pid, s[1], "label", drawing=D["id"], at=(s[2], s[3]), size_pt=s[4] / IX_PT, bold=s[6],
                    colour=s[5], positions=["=" + s[7]] + list(s[8] or AG_COMPASS), group=did, priority=5)
    runs = []                                      # [(kind, element, [shapes])], draw order kept
    for sh, tg in zip(pg.shapes, pg.gs):
        if sh[0] == "text":
            continue
        kind, eid = tg if tg[1] is not None else (tg[0], did)
        if tg == AG_TAG0:
            AG_GRP[3] += 1
        if runs and runs[-1][0] == kind and runs[-1][1] == eid:
            runs[-1][2].append(sh)
        else:
            runs.append((kind, eid, [sh]))
    for kind, eid, shs in runs:
        with _ag_grp(kind, eid):
            ix.layer(D, "%s/%s" % (kind, eid), shs)
        AG_GRP[0] += 1; AG_GRP[1].add(kind); AG_GRP[2].add((did, eid))
    for box, kind, name in pg.keeps:
        if kind != "reading":
            ix.keep(D, box, kind, name)
    return D


def chip(pg, x, y, n, label, size=7.5):
    """v3: a numbered step, the label after it (baseline y). Returns x after it. v9 (round 4, G-R4-7): the marker is
    the shared marker.py mk_marker (glyph centred on its ink box, 7 pt, at least AG_STEP_MM across, accent)."""
    s = AG_STEP_MM
    sh, _box, r = mk_marker(x + s / 2.0, y + 1.1, str(n), C["accent"], size_pt=7.0, r_min=s / 2.0)
    _ag_put(pg, sh)
    lx = x + s / 2.0 + r + 1.2
    pg.text(label, lx, y, size, C["ink"])
    return lx + text_w(label, size)


def step_arrow(pg, x, y):
    """v3: a small arrow, 4 mm long, at the mid-height of a label on baseline y. Returns x after it."""
    ym = y + 1.1
    pg.line([(x, ym), (x + 3.0, ym)], C["ink2"], 0.3)
    pg.poly([(x + 2.9, ym + 0.8), (x + 4.0, ym), (x + 2.9, ym - 0.8)], fill=C["ink2"], closed=True)
    return x + 4.0


def chips(pg, x, y, steps, size=7.5):
    """v3: numbered steps in one row, an arrow between two, from x on baseline y"""
    for i, (n, lab) in enumerate(steps):
        if i: x = step_arrow(pg, x + 1.5, y) + 1.5
        x = chip(pg, x, y, n, lab, size)
    return x


def squeeze(ys):
    """v3: the double squeeze, dry year against normal, from the water balance's year_split (one daily run of the
    design store): water left for the farms after the strip (carried in + filled - strip), the farms' need per hectare
    (the same fields both years, so their need) and the hectares that water serves = left / need per ha. Fractions."""
    n, d = ys["normal"], ys["dry5"]
    left = lambda q: q["carried_in_m3"] + q["filled_m3"] - q["strip_m3"]
    a = left(d) / max(left(n), 1.0) - 1.0
    b = d["farm_need_m3"] / max(n["farm_need_m3"], 1.0) - 1.0
    return a, b, (1.0 + a) / (1.0 + b) - 1.0


def pc(v):
    """v3: a change as a signed whole percent, "+11 %", "-2 %", "0 %" """
    return "0 %" if abs(v) < 0.005 else "%+.0f %%" % (100.0 * v)


def ag_stream_block(pg, L, src, x0, top, hl):
    """v3 (Aras 27 Oct 17:35, Prompt 6 task 1: "the board sends LESS water to farms in a 1-in-5 dry year than storage
    holds ... show the defence ON the board"): the priority as numbered steps; the design store through a normal and the
    1-in-5 dry water year, two stacked bars on one scale: strip (it also waters the bed planting: the model has no draw
    of its own for it), farms (light normal, deep dry, as the hectare bars), left over (carried on, or back to the
    stream after 365 days), the store size dashed across both; then the double squeeze. All from the water balance
    results (design.year_split); without them only the priority row.
    v8 (round 3, was stream_first; the merged booklet page): crop ag1_stream, AG_STREAM_W x AG_STREAM_H at 1:1 from
    (x0, top): the left column (AG_ST_LW) holds the title, the to-farms headline hl = (value, line) (was its own crop
    ag1_headline) and the bars' key; the right column the steps, the two bars and the squeeze.
    v9 (round 4, P19.1): booklet p19 group 2's first block: the group heading "HOW MUCH WATER REACHES THE FARMS"
    (was the title "THE STREAM COMES FIRST") on the steps' line; the outside values never run under the row labels or
    into the through-the-store lines. v10: drawn into an AgRec (ag_p18_items), the heading is a text item, no check."""
    W, H = AG_STREAM_W, AG_STREAM_H
    xl, xr = x0, x0 + AG_ST_LW + 5.0
    ag_heading(pg, "THE STREAM COMES FIRST", xl, top)          # v11: the v8.3 title again (SON page19)
    pg.tag("labels", "headline")
    pg.text(hl[0], xl, top - 11.5, 16, C["green_deep"], True)
    yk = top - 16.0
    pg.tgroup()                                    # the headline's line(s): one word block
    for ln in wrap(hl[1], 7.5, AG_ST_LW):
        pg.text(ln, xl, yk, 7.5, C["ink"])
        yk -= 3.3
    pg.tgroup(False)
    pg.tag("annotations", "priority_steps")
    chips(pg, xr, top - 4.0, PRIORITY)
    ys = L.get("year_split")
    if not (ys and "normal" in ys and "dry5" in ys):
        LOG_NOTES.append("FLAG p1: the water balance results have no year_split (water balance v4 has not run): the "
                         "normal and dry-year bars and the squeeze line are left out")
        return
    mix = L.get("design_mix") or "design mix"
    mix_t = " + ".join(name_lc(w.split()[-1]) if w.split() and w.split()[-1] in PLANTS else w for w in mix.split(" + "))
    SRC_Y = ("normal and 1-in-5 dry year: " + src + "; design store, " + mix_t + "; one daily run of the store over 34 "
             "water years: normal = the year of median farm need, dry = the 1-in-5 dry year of farm need; carried in + "
             "filled = strip + farms + left over; left for farms = carried in + filled - strip; hectares = left for farms "
             "/ need per hectare (calculated)")
    mk = cite(SRC_Y)
    V = float(ys.get("storage_m3") or 0.0)
    YRS = (("normal", "normal year", C["green_light"], C["ink"]), ("dry5", "1-in-5 dry year", C["green_deep"], C["white"]))
    tot = dict((k, ys[k]["carried_in_m3"] + ys[k]["filled_m3"]) for k, _, _, _ in YRS)
    xb = xr + 28.0                                 # v8: the bars' origin (their labels right-aligned before it)
    BW = x0 + W - 1.0 - AG_ST_RW - 4.0 - xb        # AG_ST_RW mm for the through-the-store lines after the bars
    BH, BP = 5.0, 9.5                              # v8: bar height, pitch (v3 6, 11)
    kx = BW / max(max(tot.values()), V, 1.0)
    v_t = lambda v: fmt(rnd(v, 1000 if v >= 10000 else 100))
    b1 = top - 10.0                                # the normal bar's top; the dry bar BP under it
    for j, (k, lab, fcol, fink) in enumerate(YRS):
        d = ys[k]
        pg.tag("water", k + "_year_bar")                # v11 (G6-9): one element per year's bar and its words
        bt = b1 - BP * j; bot = bt - BH
        segs = [(d["strip_m3"], C["water_deep"], C["white"]), (d["farms_m3"], fcol, fink),
                (max(0.0, tot[k] - d["strip_m3"] - d["farms_m3"]), C["faint"], C["ink"])]
        xs, out_x = xb, -1e9                       # out_x: where the last outside value ended (pushed right past it)
        for v, col, ink in segs:
            w_ = kx * v
            if w_ > 0.05:
                pg.rect(xs, bot, w_, BH, fill=col)
            t = v_t(v)
            if v >= 0.5:                           # v3.1: the block's small words 7 pt, the smallest size (were 6.5)
                tw_ = text_w(t, 7, True)
                if tw_ + 1.6 <= w_:                # inside, centred
                    pg.text(t, xs + w_ / 2.0, bot + 1.6, 7, ink, True, "C")
                else:                              # outside: over the normal bar, under the dry bar; v9: never left
                    # of the bars' origin (the row labels end 3 mm before it) nor into the through-the-store lines
                    tx = max(xs + w_ / 2.0 - tw_ / 2.0, out_x + 1.5, xb)
                    tx = min(tx, xb + BW + 3.0 - tw_)
                    pg.text(t, tx, bt + 0.9 if j == 0 else bot - 2.9, 7, C["ink"], True)
                    out_x = tx + tw_
            xs += w_
        pg.tgroup()                                # v9: the row's label and its water year: one word block
        pg.text(lab, xb - 3.0, bt - 2.2, 8, C["ink"], True, "R")
        pg.text("water year " + d["water_year"], xb - 3.0, bt - 5.3, 7, C["ink2"], align="R")
        pg.tgroup()                                # v9: the two lines after the bars: one word block
        pg.text("%s m³ through the store" % v_t(tot[k]), xb + BW + 4.0, bt - 2.2, 7.5, C["ink"], True)
        pg.text("stream's winter flow: %.0f %% of a median year" % d["winter_flow_pct_of_median"], xb + BW + 4.0,
                bt - 5.3, 7, C["ink2"])
        pg.tgroup(False)
    pg.tag("annotations", "store_size")
    if V > 0:                                      # the store size, dashed across both bars
        xv = xb + kx * V
        pg.line([(xv, b1 - BP - BH - 0.8), (xv, b1 + 0.8)], C["ink"], 0.35, (1.0, 0.7))
    lg = yk - 1.1                                  # v8: the key in the left column, one row each
    pg.tag("legend", "stream_key")
    for kind, cols, lab in (("fill", (C["water_deep"],), "strip, also waters the bed planting"),
                            ("fill", (C["green_light"], C["green_deep"]), "farms: normal · dry year"),
                            ("fill", (C["faint"],), "left: carried on, or back to the stream after a year"),
                            ("dash", (C["ink"],), ("store size " + mk).strip())):
        xx = xl
        for c_ in cols:
            if kind == "fill":
                pg.rect(xx, lg - 0.3, 3.5, 2.6, fill=c_); xx += 4.0
            else:
                pg.line([(xx + 1.7, lg - 0.6), (xx + 1.7, lg + 2.6)], c_, 0.35, (1.0, 0.7)); xx += 4.0
        pg.text(lab, xx + 0.8, lg, 7, C["ink"])           # v3.1: 7 pt (was 6.5)
        lg -= 3.6                                         # v9: 3.6 mm rows (was 3.4: the boxes kept 0.6 mm apart)
    a, b, c = squeeze(ys)
    pg.tag("labels", "squeeze")
    pg.tgroup()                                    # v9: the squeeze and what it means: one word block
    pg.text("1-in-5 dry year vs normal year: left for farms after the strip %s · need per hectare %s · hectares %s %s" % (
        pc(a), pc(b), pc(c), mk), xr, top - 32.0, 7.5, C["accent"], True)
    if b > 0.0 and a <= 0.0:                       # what the run shows, said as it is (the log flags the other cases)
        t2 = "so the hectares fall faster than the volume: why deficit-irrigated %s is the lever" % name_lc("olive")
    elif b > 0.0 and c < 0.0:
        t2 = "the need per hectare outgrows the water left: why deficit-irrigated %s is the lever" % name_lc("olive")
    else:
        t2 = "the hectares hold in this dry year: the store covers it"
    pg.text(t2, xr, top - 35.6, 7.5, C["ink"])
    pg.tgroup(False)
    if a > 0.0 or b <= 0.0:
        LOG_NOTES.append("MODEL p1: the dry year (%s) leaves the farms %s water after the strip and needs %s per hectare: "
                         "the squeeze is %s" % (ys["dry5"]["water_year"], pc(a), pc(b),
                                                "the need per hectare only" if b > 0.0 else "not there this time"))
    n_, d_ = ys["normal"], ys["dry5"]
    LOG_NOTES.append("p1 stream first (%s, store %s m3): normal %s / dry %s: in %s / %s m3 (filled %s / %s), strip %s / %s, "
                     "farms %s / %s of need %s / %s; left for farms %s, need per ha %s, hectares %s; winter flow %.0f / %.0f %% "
                     "of median" % (mix, fmt(V), n_["water_year"], d_["water_year"], fmt(tot["normal"]), fmt(tot["dry5"]),
                                    fmt(n_["filled_m3"]), fmt(d_["filled_m3"]), fmt(n_["strip_m3"]), fmt(d_["strip_m3"]),
                                    fmt(n_["farms_m3"]), fmt(d_["farms_m3"]), fmt(n_["farm_need_m3"]),
                                    fmt(d_["farm_need_m3"]), pc(a), pc(b), pc(c), n_["winter_flow_pct_of_median"],
                                    d_["winter_flow_pct_of_median"]))


def ag_p18_items(ix, L, src):
    """v11 (round 6 S7, SON page19 = v8.3): booklet p18 (v10 p21); the blocks as v8.3 had them: ag1_stream "THE STREAM
    COMES FIRST" (2), ag1_bars with its caption (3), ag1_context "WHY CROP CHOICE IS THE LEVER" (4), ag1_reading
    "THE READING" its own block again (5), ag1_history "WHY THE STORED WATER GOES TO FARMS" (6), the crop photos group
    ag1_crops "THE CROPS" (7). Places are v8.3's sheet places (the booklet's page frames decide the page).
    v10 (round 5 S9, G-R5-12, P21.1; was page_cubic): booklet p21's agriculture blocks as items, in reading order,
    each drawn by its v9 function at its v9 place (so every first position is v9's) into its own recorder and exported
    by ag_export_block: ag1_stream (group 2), ag1_bars (3), ag1_context (4), ag1_history (5) + the crop photos (5).
    v9's sheet title "WHAT EACH CUBIC METRE GROWS", its subtitle and the stage kicker were never in the booklet (its
    page title is the booklet's own) and are not exported."""
    p_lo, p_hi = span(L["farm_share_dry5_pct"]); n_lo, n_hi = span(L["farm_need_dry5_m3"])
    w_lo, w_hi = n_lo * p_lo / 100.0, n_hi * p_hi / 100.0          # m3 the storage gives the farms in the 1-in-5 dry year
    fed = L["cropland_ha"] + L["orchard_ha"]
    SRC1 = "storage, need and share: " + src + "; water to farms = 1-in-5 dry-year need x share covered (calculated)"
    MIX = ("Bergama mix = cotton, corn and tomato weighted by their 2025 district areas; no map shows what the 34.9 ha grow, "
           "so the mix stands in; water balance crops: %s" % (", ".join(crop_word(c) for c in L["crops"]) or "not set"))
    # the to-farms headline (v8: drawn in ag1_stream's left column); T5 (30 Oct, M10): the storage figure is p.10's
    hl = ("%s-%s m³" % (fmt(rnd(w_lo)), fmt(rnd(w_hi))), "to farms · 1-in-5 dry year · %s %% of need · strip first %s" % (
        ("%.0f" % p_lo) if "%.0f" % p_lo == "%.0f" % p_hi else "%.0f-%.0f" % (p_lo, p_hi), cite(SRC1)))
    # bars: hectares served by W, per crop (v2, Prompt 5: the crop names "English (Turkish)")
    rows = [(plant_name("olive") + ", full irrigation", "olive", None), (plant_name("olive") + ", deficit irrigation", "olive", DEFICIT)] + \
           [(plant_name(c) if c in PLANTS else c.capitalize(), c, None) for c in sorted(NET) if c != "olive"] + [("Bergama mix (TÜİK 2025)", "mix", None)]
    vals = []
    for lab, crop, d in rows:
        for yr in ("normal", "dry"):
            g = gross_m3_ha(crop, yr)
            if d: lo, hi = w_lo / (g * (1 - d[0])), w_hi / (g * (1 - d[1]))
            else: lo, hi = w_lo / g, w_hi / g
            vals.append((lab, crop, yr, g, lo, hi, d))
    # v11: the v8.3 sheet places (page_cubic): stream (14, 262) · bars (14, 212) | context (245, 212) · reading
    # (14, 136) | history (146, 136); the crops are photo items
    AG_DBOX.clear()
    CUR_PAGE[0] = AG_PAGE
    cut = AG_HEAD - 0.5                            # v10: the heading band is empty now (heading = its own item)
    pg = AgRec()
    ag_stream_block(pg, L, src, 14.0, 262.0, (hl[0], hl[1].strip()))
    ag_export_block(ix, pg, "ag1_stream", 2, 14.0, 262.0, AG_STREAM_W, AG_STREAM_H, 0.0)   # its steps sit in the band
    pg = AgRec()
    ag_bars_block(pg, 14.0, 212.0, rows, vals, fed, MIX)
    ag_export_block(ix, pg, "ag1_bars", 3, 14.0, 212.0, AG_BARS_W, AG_BARS_H, 0.0)
    ix.text(AG_PAGE, "Hectares one storage irrigates, by crop", "caption", group="ag1_bars", priority=3,
            id="ag1_bars_caption")                 # v8.3 AG_CAPTIONS (the block has no heading)
    best = [q for q in vals if q[1] == "olive" and q[6] and q[2] == "dry"][0]     # v2: olive with deficit (not by its label)
    worst = max((q for q in vals if q[1] not in ("olive", "mix") and q[2] == "dry"), key=lambda q: q[3])     # the thirstiest field crop
    pg = AgRec()
    ag_context_block(pg, 14.0 + AG_BARS_W + 4.0, 212.0)
    ag_export_block(ix, pg, "ag1_context", 4, 14.0 + AG_BARS_W + 4.0, 212.0, AG_CTX_W, AG_CTX_H, cut)
    pg = AgRec()
    ag_reading_block(pg, 14.0, 136.0, best, worst)
    ag_export_block(ix, pg, "ag1_reading", 5, 14.0, 136.0, AG_READ_W, AG_READ_H, cut)
    ix.text(AG_PAGE, "Same storage: how much more land", "caption", group="ag1_reading", priority=5,
            id="ag1_reading_caption")              # v8.3 AG_CAPTIONS
    pg = AgRec()
    history_line(pg, 146.0, 136.0, AG_HIST_W, AG_HIST_H)      # v1.6: why the stored water goes to farms
    ag_export_block(ix, pg, "ag1_history", 6, 146.0, 136.0, AG_HIST_W, AG_HIST_H, cut)
    ix.text(AG_PAGE, "THE CROPS", "heading", group="ag1_crops", priority=7, id="ag1_crops_head")   # v8.3 crop_row title
    ag_crops_items(ix, 7, "ag1_crops")                        # v2 (Prompt 5): the crops as photos
    LOG_NOTES.append("legend p18 hues=table")


def ag_bars_block(pg, x0, top, rows, vals, fed, MIX):
    """page 1's main chart: hectares the storage irrigates per crop, a light (normal year) and a deep (1-in-5 dry
    year) bar each, the open end = the range (storage span; olive deficit saving 44-72 %), the values at the bar ends,
    "farms we feed" dashed. v8 (round 3, A3_3's bars with direct labels): crop ag1_bars, AG_BARS_W x AG_BARS_H at 1:1
    from (x0, top); no key row: the first row's values say "normal year" / "1-in-5 dry year", the open end is said on
    the top line; each row's name, need and Bergama area right-aligned before its bars.
    v9 (round 4, P19.1): booklet p19 group 3 (6 page columns, AG_BARS_W x AG_BARS_H): the group heading "HECTARES ONE
    STORAGE IRRIGATES, BY CROP" in the band on top, the top line under it; the bars are keeps. v10: drawn into an
    AgRec (ag_p18_items): the heading is a text item, every word a label, the bars keep areas; no check here."""
    W, H = AG_BARS_W, AG_BARS_H
    BH, BO = AG_BAR_H, AG_BAR_O
    n = len(rows)
    # v11 (round 6 S7, SON page19 = v8.3): no heading (v8.3: the booklet caption "Hectares one storage irrigates, by
    # crop", ag_p18_items), so the top line and the rows start at the block's top again; the row's name, need and area
    # lines 3.2 / 3.0 mm apart (were 2.7 / 2.5: SON pairs "Olive (Zeytin), full irrigation" x its source marks)
    pg.tag("annotations", "bars_grid")
    y0 = top - 6.0                                   # the first row's top; the top line (farms we feed) above it
    RP = min(AG_BAR_RP, (y0 - (top - H + 4.5) - BO - BH) / max(n - 1, 1))
    yb_ = y0 - (n - 1) * RP - BO - BH                # the last row's dry bar bottom (= the grid's foot)
    texts = []                                       # per row: (name, need line, area line or None)
    for i, (lab, crop, d) in enumerate(rows):
        area = fact_num("olive_area_ha") if crop == "olive" else (fmt(TUIK_2025_DA[crop] / 10.0) if crop in TUIK_2025_DA else None)
        area_t = "Bergama 2025: %s ha %s" % (area, cite(TUIK)) if area and not (crop == "olive" and d) else None
        g_n, g_d = gross_m3_ha(crop, "normal"), gross_m3_ha(crop, "dry")
        if d: g_n, g_d = g_n * (1 - d[1]), g_d * (1 - d[0])
        mk = cite(NET_REF) + (cite(TAGEM) if i == 0 else "") + (cite(KAYA) if d else "") + (cite(MIX) if crop == "mix" else "")
        if crop == "olive" and not d:                 # T5 (M10): facts.py; the 1-in-5 dry-year need prints on p.18
            need_t = fact_text("olive_need_normal_m3_ha")
            need_t = "%s %s" % (need_t, mk) if need_t else None
        else:
            need_t = "%s-%s m³ per ha a season %s" % (fmt(rnd(min(g_n, g_d), 10)), fmt(rnd(max(g_n, g_d), 10)), mk)
        texts.append((lab, need_t, area_t))
    lw = max([text_w(t[0], 7.5, True) for t in texts] + [text_w(q, 6.5) for t in texts for q in t[1:] if q])
    xb = x0 + lw + 3.0                               # the bars' origin
    vmax = max(v[5] for v in vals) * 1.08
    DIRECT = {"normal": "  normal year (mean of 34)", "dry": "  1-in-5 dry year"}   # the first row's direct labels

    def vtext(v, first):
        t = "%s-%s ha" % (fmt(v[4]), fmt(v[5])) if fmt(v[4]) != fmt(v[5]) else "%s ha" % fmt(v[4])
        return t, (DIRECT[v[2]] if first else "")
    avail = x0 + W - 1.0 - xb                        # the grid as wide as the longest bar + its words allow
    gw = min((avail - 1.5 - text_w(t, 7.5, True) - text_w(e, 7)) / (v[5] / vmax)
             for v in vals for t, e in [vtext(v, v[0] == rows[0][0])])
    step = 25 if vmax < 160 else (50 if vmax < 400 else 100)
    for t in range(0, int(vmax) + 1, step):
        xx = xb + gw * t / vmax
        if xx + 0.5 * text_w("%d ha" % t, 7) > x0 + W - 0.5:   # v9.1: a grid line whose centred value would run past
            break                                    # the crop's edge is left out ("200 ha" hit it, Aras 1 Nov 17:07)
        pg.line([(xx, yb_), (xx, y0 + 0.5)], C["faint"], 0.2)
        pg.text("%d ha" % t, xx, yb_ - 3.5, 7, C["ink2"], align="C")
    xf = xb + gw * fed / vmax
    pg.tag("fields", "farms_we_feed")
    pg.line([(xf, yb_), (xf, y0 + 2.0)], C["accent"], 0.5, (1.5, 1.0))
    ff = "farms we feed: %s ha" % fmt1(fed)
    pg.text(ff, xf + 1.2, top - 3.5, 7.5, C["accent"], True)
    rng = "open bar end: range (storage span; deficit 44-72 % saving)"
    if x0 + W - 1.0 - text_w(rng, 7) < xf + 1.2 + text_w(ff, 7.5, True) + 3.0:
        ix_w = "ag1_bars: the range note meets 'farms we feed' on the top line"
        LOG_NOTES.append("WARNING p18 layout: " + ix_w)
    pg.tag("labels", "range_note")
    pg.text(rng, x0 + W - 1.0, top - 3.5, 7, C["ink2"], align="R")
    boxes = AG_DBOX.setdefault("ag1_bars", [])
    for i, (lab, crop, d) in enumerate(rows):
        yy = y0 - i * RP
        name, need_t, area_t = texts[i]
        pg.tag("fields", "bars_%s%s" % (crop, "_deficit" if d else ""))
        pg.tgroup()                                  # v9: the row's name, need and area: one word block
        pg.text(name, xb - 3.0, yy - 2.8, 7.5, C["ink"], True, "R")
        if need_t:
            pg.text(need_t, xb - 3.0, yy - 6.0, 6.5, C["ink2"], align="R")
        if area_t:
            pg.text(area_t, xb - 3.0, yy - 9.0, 6.5, C["accent"], align="R")
        pg.tgroup(False)
        for j, yr in enumerate(("normal", "dry")):
            v = [q for q in vals if q[0] == lab and q[2] == yr][0]
            by = yy - j * BO
            col = C["green_light"] if yr == "normal" else C["green_deep"]
            pg.rect(xb, by - BH, gw * v[4] / vmax, BH, fill=col)
            if v[5] > v[4] * 1.01:
                pg.rect(xb + gw * v[4] / vmax, by - BH, gw * (v[5] - v[4]) / vmax, BH, fill=None, stroke=col, lw=0.35)
            boxes.append((xb, by - BH, xb + gw * v[5] / vmax, by))
            pg.keep((xb, by - BH, xb + gw * v[5] / vmax, by), "bar %d %s" % (i, yr))
            t, e = vtext(v, i == 0)
            tx = xb + gw * v[5] / vmax + 1.5
            pg.tgroup()                              # v9: the value and its direct label: one word block
            pg.text(t, tx, by - BH + 0.9, 7.5, C["ink"], True)
            if e:
                pg.text(e, tx + text_w(t, 7.5, True), by - BH + 0.9, 7, C["ink2"])
            pg.tgroup(False)


def ag_context_block(pg, x0, top):
    """v9 (round 4, P19.1): booklet group "WHY CROP CHOICE IS THE LEVER" (crop ag1_context, AG_CTX_W x AG_CTX_H at
    1:1 from (x0, top); v10: recorded in an AgRec, no TextPage). v11 (round 6 S7, SON page19 = v8.3): the four context
    tiles 2 x 2 only (v1.2 tiles at 0.9, no frames; each tile one word block, icons keeps), 5 columns wide; the reading
    is its own block again (ag_reading_block)."""
    W, H = AG_CTX_W, AG_CTX_H
    ag_heading(pg, "WHY CROP CHOICE IS THE LEVER", x0, top)
    pg.tag("annotations", "context_tiles")
    AG_DBOX["ag1_context"] = []
    yb_ = tiles(pg, x0, top - AG_HEAD - 1.5, W, CONTEXT, cols=2, s=0.9, boxes=AG_DBOX["ag1_context"])
    if yb_ < top - H + 0.5:
        LOG_NOTES.append("WARNING p18 layout: ag1_context tiles run %.1f mm below the block" % (top - H + 0.5 - yb_))


def ag_reading_block(pg, x0, top, best, worst):
    """THE READING (v1.2; v7: a fact once, only the ratio and the lever; v8 its own crop ag1_reading, v9-v10 a strip
    inside ag1_context). v11 (round 6 S7, SON page19 = v8.3): its own block again, AG_READ_W x AG_READ_H from (x0,
    top), the heading an item over it: the land one storage irrigates in the 1-in-5 dry year as squares by area: the
    thirstiest field crop = 1 (deep), deficit-irrigated olive = the ratio (deep up to its low end, open up to its high
    end, as the bars' open ends); beside them, one column: the ratio, what it means, what it compares, the lever."""
    W, H = AG_READ_W, AG_READ_H
    ag_heading(pg, "THE READING", x0, top)
    lo, hi = best[4] / worst[4], best[5] / worst[5]
    rt = "%.1f-%.1f x" % (lo, hi)
    st = top - AG_HEAD                               # under the heading band
    gy = top - H + 2.0                               # the squares stand on one line
    a = min(11.0, (st - 0.5 - gy) / math.sqrt(max(hi, 1.0)))   # 1 unit of land (a drawing size, not printed)
    xs = x0
    s_lo, s_hi = a * math.sqrt(max(lo, 0.0)), a * math.sqrt(max(hi, 0.0))
    xo = xs + a + 3.0
    pg.tag("fields", "reading_" + worst[1])
    pg.rect(xs, gy, a, a, fill=C["green_deep"])
    pg.tag("fields", "reading_" + best[1] + "_deficit")
    pg.rect(xo, gy, s_hi, s_hi, stroke=C["green_deep"], lw=0.35)
    pg.rect(xo, gy, s_lo, s_lo, fill=C["green_deep"])
    pg.keep((xs, gy, xs + a, gy + a), "reading square " + worst[1], "reading")
    pg.keep((xo, gy, xo + max(s_hi, s_lo), gy + max(s_hi, s_lo)), "reading square " + best[1], "reading")
    pg.tag("labels", "reading")
    for cx_, side, key in ((xs, a, worst[1]), (xo, s_lo, best[1])):      # the crop's word in its deep square
        w_ = crop_word(key)
        sz = 6.5 if text_w(w_, 6.5, True) + 1.0 <= side else 6.0
        if text_w(w_, sz, True) + 1.0 <= side:
            pg.text(w_, cx_ + side / 2.0, gy + side / 2.0 - 0.8, sz, C["white"], True, "C", allow=("reading",))
        else:
            LOG_NOTES.append("FLAG p18 ag1_reading: '%s' does not fit its %.1f mm square; the line beside the squares "
                             "names both crops" % (w_, side))
    tx = xo + max(s_hi, s_lo) + 5.0
    tw = x0 + W - 1.0 - tx
    wname = plant_name(worst[1]) if worst[1] in PLANTS else worst[1].capitalize()
    pg.text(rt, tx, st - 6.0, 18, C["accent"], True)
    pg.text("as much land, same storage", tx, st - 9.6, 7, C["ink"])
    yy = st - 12.6
    for ln in wrap("%s against %s, 1-in-5 dry year" % (best[0], wname), 6.5, tw)[:2]:
        pg.text(ln, tx, yy, 6.5, C["ink2"])
        yy -= 2.7
    yy -= 0.9
    for ln, b in [(q, True) for q in wrap("lever: crop + irrigation method, more than storage", 7, tw, True)] + \
                 [(q, False) for q in wrap("same water: more farmland · same farms: less storage", 7, tw)]:
        pg.text(ln, tx, yy, 7, C["ink"], b)
        yy -= 3.2
    if yy + 3.2 - 0.6 < top - H:
        LOG_NOTES.append("WARNING p18 layout: ag1_reading text runs %.1f mm below the block" % (top - H - yy - 2.6))


# ------------------------------------------------------------------ page 2: the farms we feed, on the site board's plan 01
# v1.5 (Aras 26 Oct 07:06, deck p.33): "build this map from the 'What is there' plan (p.02): same base, same palette and
# legend". The base is the site board's own plan 01, never redrawn or stretched (Aras 25 Oct 22:07); this map draws only
# the farms layer on it.
# v10 (round 5 S9, C13, G-R5-12): the farms lie partly outside plan 01, so the v9 window cut from plan 01 fell back to
# the land cover drawing. The farms map is now its own true-scale plan ag2_farms (metres, y up): its extent is the
# farms' own bounding box + AG_FARM_MARGIN, its scales the listed ones at which that extent fits the booklet's drawing
# column; its base is the site board v60's exported drawing sb_plan01 (cached/booklet/selinus_board/items.json, the
# plan's shapes in metres from its crop's lower-left, y up, with georef [[survey x, y, drawing x, y]] of its frame
# corners), moved onto the farms by the similarity those corners give (uniform scale, turn, shift; never stretched),
# cut to the plan's own frame and to the farms' extent: where the farms reach past plan 01 the base simply ends (log
# line "FLAG p18 farms map: plan 01 covers n % ..."). No sb_plan01 = a WARNING and the farms layer alone (the v9 land
# cover fallback and the PDF cut are gone). The map's north arrow, scale bar and scale are the booklet's.
AG_SB_ITEMS = os.path.join(bg_booklet("selinus_board"), "items.json")   # the site board v60's export (S7)
AG_SCALES = (200, 250, 500, 1000, 2000, 2500, 5000, 10000, 20000)      # = SF_SCALES (PLAN §3, round 5 shared spec)
AG_FARM_BOX = (274.4, 243.0)       # mm: the booklet's drawing column (S1 lay_page share 0.70 = 274.4 mm) x the page's
#                                    drawing height (CHK-9: 392 x 243 mm); the scales whose extent fits it are offered
AG_FARM_MARGIN = 0.04              # design value: the margin round the farms, a share of the extent's longer side
AG_FARM_ID = "ag2_farms"


def _ag_cut(p, q, axis, v):
    t = (v - p[axis]) / (q[axis] - p[axis])
    return [p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])]


def _ag_clip_ring(R, bb):
    """a closed ring cut to the box bb (x0, y0, x1, y1) (Sutherland-Hodgman); [] when nothing is left"""
    pts = [list(p[:2]) for p in R]
    for axis, v, ge in ((0, bb[0], True), (0, bb[2], False), (1, bb[1], True), (1, bb[3], False)):
        if not pts:
            break
        out = []
        for i in range(len(pts)):
            p, q = pts[i - 1], pts[i]
            pin = p[axis] >= v if ge else p[axis] <= v
            qin = q[axis] >= v if ge else q[axis] <= v
            if qin:
                if not pin:
                    out.append(_ag_cut(p, q, axis, v))
                out.append(q)
            elif pin:
                out.append(_ag_cut(p, q, axis, v))
        pts = out
    return pts if len(pts) >= 3 else []


def _ag_clip_seg(p, q, bb):
    """the part of segment p-q inside bb (Liang-Barsky), or None"""
    t0, t1 = 0.0, 1.0
    dx, dy = q[0] - p[0], q[1] - p[1]
    for pp, qq in ((-dx, p[0] - bb[0]), (dx, bb[2] - p[0]), (-dy, p[1] - bb[1]), (dy, bb[3] - p[1])):
        if pp == 0:
            if qq < 0:
                return None
        else:
            r = qq / pp
            if pp < 0:
                t0 = max(t0, r)
            else:
                t1 = min(t1, r)
            if t0 > t1:
                return None
    return [p[0] + t0 * dx, p[1] + t0 * dy], [p[0] + t1 * dx, p[1] + t1 * dy]


def _ag_clip_line(P, bb):
    """a polyline cut to bb: the runs inside it"""
    runs, cur = [], []
    for i in range(1, len(P)):
        s = _ag_clip_seg(P[i - 1], P[i], bb)
        if s is None:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
            continue
        a, b = s
        if cur and abs(cur[-1][0] - a[0]) < 1e-9 and abs(cur[-1][1] - a[1]) < 1e-9:
            cur.append(b)
        else:
            if len(cur) >= 2:
                runs.append(cur)
            cur = [a, b]
    if len(cur) >= 2:
        runs.append(cur)
    return runs


def ag_plan01():
    """v10 (C13): (drawing, key rows, note, fresh) of the site board's plan 01 from its items.json: drawing = the item
    sb_plan01 (dict, with "georef"), key rows = [(swatch, text)] of its legend item, note = where it comes from and
    bg_this_run's "this run ... / from an earlier run ..."; (None, [], why, fresh) when it is missing. Never raises."""
    path = AG_SB_ITEMS
    if not os.path.isfile(path):
        return None, [], u"missing: %s (run the site board v60 or later first)" % path, False
    fresh, note = bg_this_run(path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
    except Exception as ex:
        return None, [], u"unreadable: %s (%s: %s)" % (path, type(ex).__name__, ex), fresh
    D, leg, texts = None, None, {}
    for its in (d.get("pages") or {}).values():
        for it in its:
            k_ = it.get("kind")
            if k_ == "drawing" and it.get("id") == "sb_plan01":
                D = it
            elif k_ == "text":
                texts[it.get("id")] = it.get("string") or u""
            elif k_ == "legend" and it.get("drawing") == "sb_plan01":
                leg = it
    src_ = u"site board %s, %s (%s)" % (d.get("version", "?"), path, note)
    if D is None or len(D.get("georef") or ()) < 2:
        return None, [], u"no drawing sb_plan01 with a georef in " + src_, fresh
    rows = [(dict(e.get("swatch") or {}), texts.get(e.get("text"))) for e in (leg or {}).get("entries", ())
            if texts.get(e.get("text"))]
    return D, rows, src_, fresh


def _ag_base_shapes(B, bb, s, t):
    """v10 (C13): sb_plan01's schema shapes cut to bb (its own drawing units) and moved by x' = s x + t (s > 0 uniform,
    t complex): [shape dict] in the farms drawing's metres; texts never come (its labels stay on p02)"""
    M = lambda p: [round(s * p[0] + t.real, 3), round(s * p[1] + t.imag, 3)]
    out = []
    for L_ in B.get("layers") or ():
        for sh in L_.get("shapes") or ():
            k_ = sh.get("t") or sh.get("type")
            if k_ == "poly":
                rings = [_ag_clip_ring(r, bb) for r in sh.get("rings") or () if len(r) >= 3]
                rings = [[M(p) for p in r] for r in rings if r]
                if rings:
                    n_ = dict(sh)
                    n_["rings"] = rings
                    out.append(n_)
            elif k_ == "line":
                for run in _ag_clip_line(sh.get("pts") or (), bb):
                    n_ = dict(sh)
                    n_["pts"] = [M(p) for p in run]
                    out.append(n_)
            elif k_ == "circle":
                c = sh.get("c") or (0.0, 0.0)
                if bb[0] <= c[0] <= bb[2] and bb[1] <= c[1] <= bb[3]:
                    n_ = dict(sh)
                    n_["c"], n_["r"] = M(c), round(s * float(sh.get("r") or 0.0), 3)
                    out.append(n_)
            elif k_ == "image":
                bx = sh.get("box") or ()
                if len(bx) < 4:
                    continue
                cl = sh.get("clip") or bx
                q = (max(bx[0], cl[0], bb[0]), max(bx[1], cl[1], bb[1]), min(bx[2], cl[2], bb[2]),
                     min(bx[3], cl[3], bb[3]))
                if q[2] > q[0] and q[3] > q[1]:
                    n_ = dict(sh)
                    n_["box"] = M(bx[:2]) + M(bx[2:4])
                    n_["clip"] = M(q[:2]) + M(q[2:4])
                    out.append(n_)
    return out


def ag_farms_items(ix, L, src):
    """v10 (round 5 S9, C13, G-R5-12; was page_farms): the farms we feed as the true-scale plan ag2_farms (group
    ag2_farms, priority 6): base = plan 01 (sb_plan01) where it reaches, the farms' extent dashed, the fields and
    orchards fed as outlines; heading, intro, the context line (with the base), the farms layer's key with its
    figures (WE FEED) and plan 01's own key as items. Figures and sources as v9. Returns the log lines."""
    out, g, pid = [], AG_FARM_ID, AG_PAGE
    B, key_rows, bnote, fresh = ag_plan01()
    fed = [(key, poly) for key in ("farmland", "orchard") for side in ("out", "in") for poly in GEO["lc"][key][side]]
    F = GEO["frame"]
    a = None
    if B is not None:                              # survey -> sb_plan01 drawing: z = a w + b (complex similarity)
        W = [complex(q[0], q[1]) for q in B["georef"]]
        Z = [complex(q[2], q[3]) for q in B["georef"]]
        wm, zm = sum(W) / len(W), sum(Z) / len(Z)
        den_ = sum(abs(w - wm) ** 2 for w in W)
        if den_ > 0:
            a = sum((z - zm) * (w - wm).conjugate() for w, z in zip(W, Z)) / den_
        if not a:
            B, bnote = None, u"sb_plan01's georef has no extent (%s)" % bnote
    if B is None:
        ix.warn(pid, "base", u"the site board's plan 01 is not available (%s): the farms map is exported without its "
                             u"base" % bnote)
    elif not fresh:
        ix.warn(pid, "stale", u"plan 01 under the farms map is %s" % bnote)
    rotu = a / abs(a) if a else complex(math.cos(-math.atan2(F[1][1] - F[0][1], F[1][0] - F[0][0])),
                                        math.sin(-math.atan2(F[1][1] - F[0][1], F[1][0] - F[0][0])))
    Q = [complex(p[0], p[1]) * rotu for _, poly in fed for ring in poly for p in ring]   # the plan's own turn
    bx0, bx1 = min(q.real for q in Q), max(q.real for q in Q)
    by0, by1 = min(q.imag for q in Q), max(q.imag for q in Q)
    mg = AG_FARM_MARGIN * max(bx1 - bx0, by1 - by0)
    off = complex(bx0 - mg, by0 - mg)
    EW, EH = bx1 - bx0 + 2 * mg, by1 - by0 + 2 * mg

    def T(p):                                      # survey m -> the farms drawing's m (turned as plan 01, y up)
        z = complex(p[0], p[1]) * rotu - off
        return (z.real, z.imag)
    dens = [d_ for d_ in AG_SCALES if EW * 1000.0 / d_ <= AG_FARM_BOX[0] and EH * 1000.0 / d_ <= AG_FARM_BOX[1]]
    if not dens:
        dens = [AG_SCALES[-1]]
        ix.warn(pid, "scale", u"the farms' extent %.0f x %.0f m fits the drawing column at no listed scale; 1:%d "
                              u"offered" % (EW, EH, dens[0]))
    north = math.degrees(math.atan2(rotu.imag, rotu.real))
    D = ix.drawing(AG_FARM_ID, pid, (0.0, 0.0, EW, EH), scale_pref=dens, units="m", dkind="plan", north_deg=north,
                   scale_bar=True, priority=6, group=g, title=u"The farms we feed")
    D["north_note"] = u"north_deg = survey north from the drawing's +y axis, counter-clockwise, degrees (v9's arrow)"
    ext = (0.0, 0.0, EW, EH)
    if B is not None:                              # plan 01 moved onto the farms: x' = s z + t (s = 1 / |a|, uniform)
        s = 1.0 / abs(a)
        t = -((zm - a * wm) / abs(a)) - off        # z = a w + b -> w turned by rotu - off = (z - b) / |a| - off
        fx = [q[2] for q in B["georef"]]
        fy = [q[3] for q in B["georef"]]
        bb = (max(min(fx), (0.0 - t.real) / s), max(min(fy), (0.0 - t.imag) / s),
              min(max(fx), (EW - t.real) / s), min(max(fy), (EH - t.imag) / s))
        cov = max(0.0, bb[2] - bb[0]) * max(0.0, bb[3] - bb[1]) * s * s / max(EW * EH, 1e-9)
        sh = _ag_base_shapes(B, bb, s, t) if cov > 0 else []
        D["layers"].append(dict(z=0, name="plan01_base", shapes=sh))
        err = max(abs(a * w + (zm - a * wm) - z) for w, z in zip(W, Z))
        out.append(u"farms map base: sb_plan01 from %s; similarity scale %.4f, fit %.2f m over %d corners; %d shapes "
                   u"kept" % (bnote, abs(a), err, len(W), len(sh)))
        out.append(u"FLAG p18 farms map: plan 01 covers %.0f %% of the farms' extent (%.0f x %.0f m); the base ends "
                   u"where plan 01 ends" % (100.0 * min(cov, 1.0), EW, EH))
        if cov <= 0:
            ix.warn(pid, "base", u"plan 01 does not reach the farms' extent: the farms map has no base")
        if err > 1.0:
            out.append(u"FLAG p18 farms map: sb_plan01's georef corners fit a similarity only to %.2f m" % err)
    else:
        out.append(u"farms map base: none (%s)" % bnote)
    sh = []                                        # the farms layer: the extent, the fields and orchards we feed
    for run in _ag_clip_line([T(p) for p in list(GEO["around2"]) + [GEO["around2"][0]]], ext):
        sh.append(("line", run, C["ink"], 0.35, (2.0, 1.2)))
    for key, poly in fed:
        for r in poly:
            for run in _ag_clip_line([T(p) for p in list(r) + [r[0]]], ext):
                sh.append(("line", run, C["accent"] if key == "farmland" else C["accent_deep"],
                           0.35 if key == "farmland" else 0.7, None))
    ix.layer(D, "farms", sh, z=1)
    out.append(u"farms map %s (%s): extent %.0f x %.0f m (farms + %.0f m margin), scales 1:%s, north %.1f deg" % (
        AG_FARM_ID, pid, EW, EH, mg, u", 1:".join(str(d_) for d_ in dens), north))
    # texts (v9's words): heading = the old page title, intro = its subtitle, the context line (review global rule 4)
    ix.text(pid, "THE FARMS WE FEED", "heading", group=g, priority=6, id=AG_FARM_ID + "_head")
    ix.text(pid, "Fields and orchards the stored water serves" + (", on the site plan \"What is there\"" if B else ""),
            "intro", group=g, priority=6, id=AG_FARM_ID + "_intro")
    WC = "ESA WorldCover 2021 v200, 10 m (CC BY 4.0)"                # v4 (F5): read from Data/landcover
    NEED2 = "need: FAO-56 soil balance / 0.90 drip, normal and 1-in-5 dry years"
    SRC2 = "farm areas from " + src
    # v4 (MIRAQUA 28 Oct, F5): no [n] for what is not public online: the orchards (course survey symbols
    # SEMBOL_ZEYTINLIK / SEMBOL_MEYVA_BAH), the extent (around2.pdf registered to the survey) and the base (the site
    # board's own plan 01, not redrawn) are said without a mark
    if B is not None:
        ix.text(pid, cited("The site plan \"What is there\" with the fields and orchards our stored water serves "
                           "outlined: the farms read off the same base, colours and key as the site", None),
                "caption", group=g, priority=6, id=AG_FARM_ID + "_caption")
    fed_c, fed_o = L["cropland_ha"], L["orchard_ha"]
    o_lo = min(gross_m3_ha("olive", "dry"), gross_m3_ha("olive", "normal"))
    o_hi = max(gross_m3_ha("olive", "dry"), gross_m3_ha("olive", "normal"))
    cc = [c_ for c_ in L["crops"] if c_ in NET] or [c_ for c_ in NET if c_ != "olive"]
    c_lo = min(gross_m3_ha(c_, y_) for c_ in cc for y_ in ("normal", "dry"))
    c_hi = max(gross_m3_ha(c_, y_) for c_ in cc for y_ in ("normal", "dry"))
    f_in, f_out = GEO["area_ha"]["farmland"][1], GEO["area_ha"]["farmland"][0]
    rows = [(dict(kind="line", colour=C["accent"], width_pt=round(0.35 / IX_PT, 2)), "fields " + cite(SRC2),
             "%s ha" % fmt1(fed_c),
             ["%s-%s m³ a season %s" % (fmt(rnd(fed_c * c_lo)), fmt(rnd(fed_c * c_hi)), cite(NEED2)),
              "as " + " / ".join(crop_word(c_) for c_ in cc) + " " + cite(TUIK),   # v4 (G11): corn, not maize
              "inside the site %s ha · outside %s ha %s" % (fmt1(f_in), fmt1(f_out), cite(WC))]),
            (dict(kind="line", colour=C["accent_deep"], width_pt=round(0.7 / IX_PT, 2)), "orchards",   # v4 (F5): survey, no mark
             "%s ha" % fmt1(fed_o),
             ["%s-%s m³ a season" % (fmt(rnd(fed_o * o_lo, 100)), fmt(rnd(fed_o * o_hi, 100))), "as olive"]),
            (dict(kind="dash", colour=C["ink"], width_pt=round(0.35 / IX_PT, 2)), "the extent they lie in",
             "%s ha" % fmt(L.get("extent_ha", 455.0)), [])]
    ix.legend(pid, AG_FARM_ID, [(sw, lab.strip()) for sw, lab, _b, _l in rows], title="WE FEED",
              id=AG_FARM_ID + "_legend", group=g)
    ix.list(pid, AG_FARM_ID, [u" · ".join([lab.strip() + ": " + big] + [ln.strip() for ln in lines])
                              for _sw, lab, big, lines in rows], numbered=False, id=AG_FARM_ID + "_figures", group=g)
    if B is not None and key_rows:                 # plan 01's own key (its legend item's rows, as the site board wrote)
        ix.legend(pid, AG_FARM_ID, key_rows, title="THE SITE PLAN'S KEY", id=AG_FARM_ID + "_plan_key", group=g)
    return out


# ------------------------------------------------------------------ sources that are not public (F5, D13)
# v4 (MIRAQUA 28 Oct, F5, Aras 28 Oct 11:38 "remove non-public citations"): the project's own record or internal
# research cards are not public online: cite() gives them no [n] and they leave the key; their words stay on the page
# as our own design statement. Facts now without a public source (reported): Tersane cotton (16th c.), ginning 1861,
# Sümerbank (1954/60-2008), the 19th-c. olive-oil machinery in the Kızıl Avlu S rotunda.
# v5 (T4a, 29 Oct, D13): also every source that names our own model run or method (F5_INTERNAL, by its words), and no
# status word (calculated, assumed ...) is ever printed in a source (F5_STATUS); page 3 (the plant ladder) is gone (D9 a).
F5_OFF = (COTTON_H, OLIVE_H)
F5_INTERNAL = ("water balance results", "default-lands copy", "farm areas from", "Bergama mix = ", "our arithmetic")
F5_STATUS = re.compile(r"\s*\((?:calculated|assumed|estimated|interpolated|indicative|design value)\)|"
                       r"\s*\b(?:calculated|assumed|estimated|interpolated|indicative)\b", re.I)

# ------------------------------------------------------------------ v11 (round 6 S7): booklet p17, the plant ladder
_SK = []
def _tree_rand(x, y):
    """A small repeatable random stream from the tree's position (the same in every Python)."""
    s = [(int(round(x * 100.0)) * 73856093 ^ int(round(y * 100.0)) * 19349663) & 0x7FFFFFFF or 1]

    def nxt():
        s[0] = (s[0] * 1103515245 + 12345) & 0x7FFFFFFF
        return s[0] / 2147483648.0
    return nxt
def sketch_engine():
    if not _SK:
        ns = {"__name__": "pr1_sketches", "_tree_rand": _tree_rand}   # reeds use the trees' random stream
        exec(compile(SKETCH_SRC, "pr1_sketches", "exec"), ns)
        _SK.append(ns)
    return _SK[0]
def xform(items, s, dx, dy):
    """The items scaled by s about the origin, then moved by (dx, dy)."""
    def T(p):
        return (dx + s * p[0], dy + s * p[1])
    out = []
    for it in items:
        k = it[0]
        if k == "poly":
            _, rings, fill, stroke, lw, dash, stripes, alpha = it
            st = (stripes[0], stripes[1] * s, stripes[2] * s) + tuple(stripes[3:]) if stripes else None
            out.append(("poly", [[T(p) for p in r] for r in rings], fill, stroke, lw * s,
                        [d * s for d in dash] if dash else dash, st, alpha))
        elif k == "line":
            _, pts, stroke, lw, dash, cap = it
            out.append(("line", [T(p) for p in pts], stroke, lw * s, [d * s for d in dash] if dash else dash, cap))
        elif k == "circle":
            _, cx, cy, r, fill, stroke, lw = it
            out.append(("circle", dx + s * cx, dy + s * cy, r * s, fill, stroke, lw * s))
        elif k == "text":
            _, t, x, y, size, color, bold, align, mat, halo = it
            out.append(("text", t, dx + s * x, dy + s * y, size * s, color, bold, align, mat, halo))
        elif k == "grp":                                  # G6-9 group marker (item_export ix_grp): kept as it is
            out.append(it)
    return out
bergama_data("SKETCH_SRC")
bergama_data("STEPS")
# ------------------------------------------------------------------ booklet p17: one plant ladder, streambed to field
# v11 (round 6 S7, 4 Nov 2026; BRIEF §6 row 17, Q9, PLAN §2.2 / §2.3; target refs/targets/r06_S01): the 28 Oct page
# "One plant ladder, streambed to field" restored from f93d84b (agriculture v3.1 page_ladder, ladder_row, chain_strip,
# seasons, data/STEPS.py; the proposal sections' SKETCH_SRC as the sketch engine, included read-only) as booklet items:
#   ag3_chain           the one-way chain along the stream (drawing, mm)
#   ag3_steps           what we do with the water, steps 1-5 (numbered list)
#   ag3_legend          the chain's symbol key (legend, hues from common/hues.py)
#   ag3_ladder_high / ag3_ladder_low / ag3_ladder_harvest   one stepped cut streambed -> field, one season each (drawing)
#   ag3_bands           the plant bands BED .. FARMS with the photos inside (image shapes, so each photo stays under
#                       its band), the REMOVE / ODOUR / reading notes column on the left (drawing)
# SECTION LANGUAGE: SKETCH (BRIEF §3, r06_S01): not to scale, thick black ground line, flat beige soil, flat blue water
# bands, simple tree blobs, few small figures, short captions. No hatches (the winter bed hatch of 28 Oct is gone), no
# horizontal dimensions, no leader lines (labels are placed by the booklet), no red: flood lines WAT r1 (P-5).
# Data (BRIEF §0 DATA): bed and flood depths = research/rain_river_levels/README.md "The answers in short" + its v1.1
# correction table (Q100 205.2 / Q500 263.3 m³/s, surveyed sections 2.0-3.0 / 2.3-3.3 m, flat end 1.4 / 1.5 m, highest
# day 0.96-1.69 m, overtopping only at K4 right bank and S4 left bank); species and reasons = research/water_data/04
# (via data/STEPS.py); today's cover = data/GEO.py "corridor" (ESA WorldCover 2021). The 28 Oct [n] numbers are gone:
# every mark is {src:agsrcN}; the project's own records (programme, garden card, Kermes card, water board season words,
# the chain) carry no mark (F5_OFF), as on every other page.
AG3_PAGE = "p17"
AG3_ID = dict(chain="ag3_chain", steps="ag3_note_steps", legend="ag3_note_legend", bands="ag3_bands", notes="ag3_notes",
              high="ag3_ladder_high", low="ag3_ladder_low", harvest="ag3_ladder_harvest")
SPECIES = "POWO, FEIS, JRC Atlas, Korkusuz et al. 2004, Aydın Temel et al. 2017, Xie et al. 2021, RHS (species, flood and cleaning evidence)"
BANDS = "planting bands after MITECO, Salinas & Cueto 2009 (habitat 92D0), USDA NRCS TN-38"
DEPTH = "DSİ design floods Q100 205.2 m³/s and Q500 263.3 m³/s; DSİ gauge yearbooks 2016-2021"
TODAY = "ESA WorldCover 2021, by distance from the OSM Selinos centreline"
REUSE = "published, 2010 wastewater reuse communiqué"          # the water board's p11 coliform source, same words
CHAIN_REF = ("option A water chain: one way, cleaned once upstream in the reed basins, held in the terrace cascade, "
             "summer strip from storage, surplus to existing farmland outside the site")
PROG = ("MIRAQUA programme and its historic roots: hubs at the Roman bridges K3, K4, K5 with floodable in-bed sub-hubs, "
        "hidden-stream square at İstiklal Meydanı, tanning reach at K3, Tabaklar Hamamı at K4, Late Antique workshops "
        "downstream, plane-tree squares")
GARDEN = ("Demeter's Garden (Begüm, 25 Oct): olives; summer farm-to-table use; winter herbs and greens; seasonal "
          "production, education; south-west bank at K5")
KERMES = "Kermes first held 1937; in the low-water season (project history card h01)"
WB_YEAR = "water board season rows: storage fills in winter, low until the rains in autumn; reeds gold, seed heads"
HARVEST = KAYA                                     # Memecik trees hand-harvested in November (Kaya et al. 2017)
F5_OFF = F5_OFF + (CHAIN_REF, PROG, GARDEN, KERMES, WB_YEAR)   # the project's own records: no mark, not in Sources
JOB_ICON = [("CLEAN", "clean"), ("HOLD", "hold"), ("SHADE", "shade"), ("SCENT", "scent"), ("HARVEST", "olive")]
AG_ICONS.update(clean=("reeds", False), hold=("flood_zone", False), shade=("shade", False), scent=("plants", False),
                outside=("field", False))          # v11: the 28 Oct pictograms by their icons.py names
# v1.6 (28 Oct): the bank top as the project has it: hub squares with plane trees at the bridges and Demeter's
# Garden's olives at K5 (olive "will not tolerate waterlogged soils", DATA_REGISTER PL-11)
STEPS[3].update(sub="hub squares at the bridges · Demeter's Garden at K5", job="SHADE + SCENT",
                plant=[("plane", "hub squares: Ottoman squares with plane trees")] + STEPS[3]["plant"] +
                      [("olive", "Demeter's Garden (K5): dry top only, no waterlogged soil")])

LAD_W = 200.0                        # sketch units across: 5 steps of 40
LAD_S = LAD_W / 5.0
LAD_X0, LAD_X1 = 106.0, 406.0        # the cut, mm (left of it: the season column)
LAD_F = (LAD_X1 - LAD_X0) / LAD_W    # mm a sketch unit, the same across and up
LAD_GB = 13.0                        # v11: the bottom of the cut ground, sketch units (28 Oct 12; 1 unit under the
#                                      channel's foot at 14, so the row is 3 mm lower and the band frames fit)
LAD_GY = (16.0, 21.0, 26.0, 30.0, 33.0)   # ground of each step (bed, lower bank, terrace, bank top, farms)
LAD_Q100, LAD_Q500 = 30.8, 31.6      # over the bank top only at K4 / S4 (README v1.1), under the farms
ROW_H = 47.0                         # mm a season row (28 Oct 50); the bank top's plane tree ends 3 mm under the top
SUBHUB = (27.0, 36.0)                # the floodable sub-hub in the bed, sketch x
HUB = (3 * LAD_S + 2.0, 3 * LAD_S + 17.0)   # the dry hub square on the bank top at the bridges, sketch x
SIT_FIG = [(-0.14, 0.0), (0.30, 0.0), (0.30, -0.42), (0.42, -0.42), (0.42, 0.13), (0.10, 0.14), (0.12, 0.62),
           (0.05, 0.70), (-0.10, 0.70), (-0.17, 0.58)]   # a seated figure (m, as the board's SA_FIGS), seat at (0, 0)
AG3_TREES = [0, 0]                   # this press: [trees with a species, generic trees] on p17 (G6-10 log)
AG3_NOPHOTO = []                     # species whose photo did not load this press (listed under the band, logged)


PH_GAP = 2.0                         # mm between two photos side by side (28 Oct)


def name_lines(key, mark, size, w, bold=True):
    """28 Oct (v2): a plant's name under its photo: "English (Turkish) {src}" on one line when it fits in w, else the
    English name and "(Turkish) {src}" on two (each wrapped to w if it is longer still)"""
    t = plant_name(key) + ((" " + mark) if mark else "")
    if text_w(t, size, bold) <= w:
        return [t]
    en, _, tr = plant_name(key).partition(" (")
    if not tr:
        return wrap(t, size, w, bold)
    return wrap(en, size, w, bold) + wrap("(" + tr + ((" " + mark) if mark else ""), size, w, bold)


def _bed(i):
    """the bed's water from STEPS: 0 = Jul-Sep, 1 = Jan-Apr"""
    return STEPS[0]["water"][i].split(": ", 1)[1]


# the season rows: what the water does (left column) and what people do where (on the cut). acts: (figure kind or
# "sit" / None, sketch x, sketch y, flip, label, source, align). v11: labels on the farms step start right of the
# site edge (align L), so the dashed edge never runs through them (target overlap).
def seasons():
    g0, g1, g2, g3, g4 = LAD_GY
    return [
        dict(key="high", name="HIGH WATER", months="Jan-Apr", mark="winter",
             side=[("bed " + _bed(1) + " deep", DEPTH), ("lower bank under water", None), ("sub-hubs closed", PROG),
                   ("storage fills", WB_YEAR)],
             acts=[("sit", 2 * LAD_S + 1.0, g2, True, "sit at the edge · watch the water", PROG, "C"),
                   (0, HUB[0] + 4.0, g3, False, "hub square: dry, step-free", PROG, "C"),
                   (2, HUB[0] + 8.5, g3, True, None, None, "C"),
                   (None, sum(SUBHUB) / 2.0, g1 + 1.8, False, "sub-hub under water: closed", PROG, "C")]),
        dict(key="low", name="LOW WATER", months="Jul-Sep", mark="summer",
             side=[("bed " + _bed(0), DEPTH), ("strip 0.30 m all summer (design)", None), ("sub-hubs open", PROG),
                   (STEPS[4]["water"][0], None)],
             acts=[(1, 10.5, g0, False, "walk in the bed", PROG, "C"),
                   (0, 19.0, g0 - 2.0, False, "wade the strip", None, "C"),
                   (2, SUBHUB[0] + 3.0, g0 + 0.7, False, "sub-hub open", PROG, "C"),
                   (None, 6.0, g0 + 6.0, False, "Kermes (since 1937) in the dry bed", KERMES, "L"),
                   (1, 2 * LAD_S + 20.0, g2, False, "shade under the trees", None, "C"),
                   (0, HUB[0] + 4.0, g3, False, "hub square: %s shade" % name_lc("plane"), PROG, "C"),
                   (None, 3 * LAD_S + 25.0, g3 + 2.0, False, "at K5: Demeter's Garden · café, summer beds", GARDEN, "R"),
                   (3, 4 * LAD_S + 19.0, g4, False, "fields + %s trees watered from storage" % name_lc("olive"), None,
                    "L")]),
        dict(key="harvest", name=name_caps("olive") + " HARVEST", months="Nov", mark="olive",
             side=[("%s: hand-picked in Nov" % name_lc("olive"), HARVEST), ("storage low until the rains", WB_YEAR),
                   ("first-flush cleaning", WB_YEAR)],
             acts=[(None, 5.0, g0 + 3.0, False, "%s gold · seed heads" % name_lc("reed"), WB_YEAR, "L"),
                   (0, 3 * LAD_S + 30.0, g3, False, "Demeter's Garden: winter herbs + greens · education", GARDEN, "R"),
                   (3, 4 * LAD_S + 12.0, g4, False, "%s harvest" % name_lc("olive"), HARVEST, "L"),
                   (1, 4 * LAD_S + 23.0, g4, True, None, None, "C")])]


def ladder_row(sea, mark_xy):
    """One season of the plant ladder in the SKETCH language: [(item, (kind, element id))] in sketch units (0..LAD_W
    across), draw order kept (z, order). mark_xy: where the season's sun / rain mark goes, sketch units.
    v11 (G6-9): every element's engine items carry its group (kind, element id), tagged as they are made."""
    E = sketch_engine()
    E["FORM"] = "A"                                   # organic only where the project meets the water
    del E["ZP"][:]
    E["ORDER"][0] = 0
    tags, mk = {}, [0]

    def T(kind, eid):                                 # every engine item since the last call belongs to this element
        for e in E["ZP"][mk[0]:]:
            tags[e[1]] = (kind, eid)
        mk[0] = len(E["ZP"])
    o, w, gy = (0.0, 0.0), LAD_S, LAD_GY
    g = [(0.0, LAD_GB), (0.0, gy[0])]
    for i in range(1, 5):
        xa = i * w
        if i == 1:                                    # the water's edge: the bank in form A (organic)
            g += E["bank"]((xa - 3.0, gy[0]), (xa + 3.0, gy[1]))
        elif i == 2:                                  # the terrace edge: a sitting step (straight riser)
            g += [(xa - 0.5, gy[1]), (xa + 0.5, gy[2])]
        else:                                         # elsewhere faceted, straight slopes
            g += [(xa - 2.0, gy[i - 1]), (xa + 2.0, gy[i])]
    g += [(LAD_W, gy[4]), (LAD_W, LAD_GB)]
    gs = E["sketch_ground"](o, E["notch"](g, [(13.0, 25.0, gy[0], 2.0)]))   # the summer strip's low-flow channel
    T("ground", "cut_ground")
    hub_c, sub_c = E["hx"](_hu("PUB", 3)), E["hx"](_hu("PUB", 2))      # G6-6: hub square PUB r3, sub-hub PUB r2
    E["fill"](o, [(HUB[0], gy[3] - 0.6), (HUB[1], gy[3] - 0.6), (HUB[1], gy[3]), (HUB[0], gy[3])], "paving", hub_c,
              boundary=False, hand_=False)        # the dry hub square at street level
    T("hubs", "hub_square")
    slab = [(SUBHUB[0], gy[0]), (SUBHUB[1], gy[0]), (SUBHUB[1], gy[0] + 0.7), (SUBHUB[0], gy[0] + 0.7)]
    E["fill"](o, slab, "paving", sub_c, boundary=False, hand_=False)   # the floodable sub-hub in the bed
    T("hubs", "sub_hub")
    if sea["key"] == "high":
        pc = E["under_level"](gs, 0.0, LAD_W, LAD_Q500)   # the design flood's reach (faint)
        if pc:
            E["wash"](o, pc, "flood", E["FLOOD_WASH"], E["FLOOD_ALPHA"])
        T("water", "q500_reach")
        E["water_level"](o, gs, 19.0, gy[1] + 1.8, E["W_WIN"], bed_hatch=False)   # winter highs: bed + lower bank
        T("water", "winter_high")
        E["sketch"](o, slab, "paving", E["SKINK"], E["PEN_HAIR"], closed=True, over=0.0, retrace=False,
                    dashed=True, z=E["Z_LINE"])       # the sub-hub under the water
        T("hubs", "sub_hub_under_water")
    elif sea["key"] == "low":
        E["water_level"](o, gs, 19.0, gy[0] - 0.8, E["W_EXT"], line=False)       # the summer strip in its channel
        T("water", "summer_strip")
    else:
        E["water_level"](o, gs, 19.0, gy[0] - 1.2, E["W_SUM"], line=False)       # autumn: water back in the channel
        T("water", "autumn_channel")
    # plants by step (graphic sizes): reeds in the bed, rushes and shrubs on the lower bank, trees on the terrace,
    # plane tree + lavender on the bank top, olives and a field crop on the farms
    E["reeds"](o, 1.5, 8.0, gy[0] - 0.2, 4.2)
    T("plants", "reed_bed")
    x_ = w + 4.0
    while x_ < w + 18.0:                              # rushes: short hand tufts
        for d in (-0.5, 0.0, 0.5):
            E["sketch"](o, [(x_, gy[1]), (x_ + d * 0.9, gy[1] + 2.0 - abs(d))], "planting", E["REED"], E["LW_FINE"],
                        over=0.0, amp=0.03, retrace=False, z=E["Z_TREE"])
        T("plants", "rush_%.0f" % x_)
        x_ += 1.6
    for nm, xs, hs, ws in (("tamarisk", w + 24.0, 5.0, 6.0), ("willow", w + 33.0, 4.2, 5.0)):   # STEPS lower bank shrubs
        dome = [(xs + ws / 2.0 * math.cos(math.pi * i / 14.0), gy[1] + hs * math.sin(math.pi * i / 14.0) ** 0.7) for i in range(15)]
        E["wash"](o, dome, "planting", E["SITE_TREE"][1], 0.6, z=E["Z_TREE"])
        E["sketch"](o, dome, "planting", E["SITE_TREE"][2], E["LW_FINE"], closed=True, over=0.0, amp=0.12, retrace=False,
                    z=E["Z_TREE"])
        T("plants", nm)
    trees = (("terrace_tree_1", None, 2 * w + 14.0, gy[2], 11.0), ("terrace_tree_2", None, 2 * w + 30.0, gy[2], 9.0),
             ("plane_hub_square", "plane", HUB[0] + 7.0, gy[3], 11.0))
    for eid, sp, xs, ys, hh in trees:                 # G6-10: a design species only where the project names one
        E["sketch_tree"](o, xs, ys, hh)
        T("trees", eid + ("" if sp else "_species_unspecified"))
        AG3_TREES[0 if sp else 1] += 1
    x_ = 3 * w + 20.0
    while x_ < 3 * w + 31.0:                          # lavender mounds with flower spikes
        mound = [(x_ + 1.2 * math.cos(math.pi * i / 10.0), gy[3] + 1.0 * math.sin(math.pi * i / 10.0)) for i in range(11)]
        E["wash"](o, mound, "planting", E["hx"](C["olive"]), 0.6, z=E["Z_TREE"])
        for d in (-0.5, 0.0, 0.5):
            E["sketch"](o, [(x_ + d, gy[3] + 0.8), (x_ + d * 1.3, gy[3] + 1.9)], "planting", E["hx"]("8E7CC3"), 0.3,
                        over=0.0, amp=0.02, retrace=False, z=E["Z_TREE"])
        T("plants", "lavender_%.0f" % x_)
        x_ += 2.8
    for eid, xs, ys, hh in (("olive_demeters_garden", 3 * w + 34.5, gy[3], 6.0), ("olive_farm_1", 4 * w + 6.0, gy[4], 7.0),
                            ("olive_farm_2", 4 * w + 15.0, gy[4], 7.0)):
        E["sketch_tree"](o, xs, ys, hh)
        T("trees", eid)
        AG3_TREES[0] += 1
    x_ = 4 * w + 26.0
    while x_ < LAD_W - 1.0:                           # field crop rows (AGR r3)
        E["sketch"](o, [(x_, gy[4]), (x_, gy[4] + 1.6)], "planting", E["hx"](_hu("AGR", 3)), 0.35, over=0.0, amp=0.02,
                    retrace=False, z=E["Z_TREE"])
        x_ += 1.4
    T("fields", "crop_rows")
    # the site edge: farmland only outside the site (v11: 6 units over the farms, was 11: it ran through the labels)
    E["sketch"](o, [(4 * w, gy[3] + 1.5), (4 * w, gy[4] + 6.0)], "site edge", E["INK2"], E["PEN_FINE"], over=0.0,
                retrace=False, dashed=True, z=E["Z_LINE"])
    T("annotations", "site_edge")
    s_ = 4.5 / 1.745                                  # people: the season's activities
    for n_, (kind, x, y, flip, _lab, _src, _al) in enumerate(sea["acts"]):
        if kind == "sit":
            sg = -1.0 if flip else 1.0
            E["fill"](o, [(x + sg * a * s_, y + b * s_) for a, b in SIT_FIG], "people", E["SITE_PEOPLE"], alpha=0.9,
                      boundary=False, z=E["Z_PEOPLE"], hand_=False)
            hx_, hy_, hr = E["SA_HEAD"][0] - 0.02, 0.84, E["SA_HEAD"][2]
            E["fill"](o, [(x + sg * hx_ * s_ + hr * s_ * math.cos(6.283 * i / 12), y + hy_ * s_ + hr * s_ * math.sin(6.283 * i / 12))
                          for i in range(12)], "people", E["SITE_PEOPLE"], alpha=0.9, boundary=False, z=E["Z_PEOPLE"],
                      hand_=False)
        elif kind is not None:
            E["sketch_person"](o, x, y, kind=kind, flip=flip)
        T("people", "person_%d" % n_)
    if sea["key"] == "high":                          # the design flood levels: hand dashed lines and level marks
        xe = 4 * w - 2.0 + 4.0 * (LAD_Q500 - gy[3]) / (gy[4] - gy[3])
        fl = E["hx"](_hu("WAT", 1))                   # P-5: no red on the page (was the engine's heritage red)
        for lv, nm in ((LAD_Q500, "q500"), (LAD_Q100, "q100")):
            E["sketch"](o, [(0.0, lv), (xe, lv)], "flood lines", fl, E["PEN_FINE"], over=0.0, retrace=False,
                        dashed=True, z=E["Z_LINE"])
            E["level_mark"](o, 3 * w + 26.0 if lv == LAD_Q500 else 3 * w + 20.0, lv, fl, "flood lines")
            T("levels", nm)
    if sea["key"] == "low":                           # the farms are watered from storage in summer: the one arrow
        E["hand_arrow"](o, (3 * w + 22.0, gy[4] + 6.5), (4 * w + 9.0, gy[4] + 5.5), E["SITE_WATER_D"], bend=-0.15)
        T("water", "stored_water_arrow")
    if sea["mark"] == "winter":
        E["cloud_rain"](o, mark_xy[0], mark_xy[1], 2.0)
        T("annotations", "season_mark")
    elif sea["mark"] == "summer":
        E["sun"](o, mark_xy[0], mark_xy[1], 1.7)
        T("annotations", "season_mark")
    E["sketch"](o, gs, "ground lines", E["SKINK"], E["PEN_BOLD"], z=E["Z_LINE"])   # the cut: the gesture
    T("ground", "ground_line")
    return [(e[2], tags.get(e[1], ("other", "sketch"))) for e in sorted(E["ZP"], key=lambda e: (e[0], e[1]))]


def sk_draw(pg, items):
    """sketch-engine items (already placed with xform) on this script's recorder"""
    for it in items:
        if it[0] == "poly":
            _, rings, fill, stroke, lw, dash, _st, alpha = it
            pg.path(rings, fill, stroke, lw, True, dash, alpha)      # stripes (hatches) are never drawn
        elif it[0] == "line":
            _, pts, stroke, lw, dash, _cap = it
            pg.line(pts, stroke, lw, dash)
        elif it[0] == "circle":
            _, cx, cy, r, fill, stroke, lw = it
            pg.circle(cx, cy, r, fill, stroke, lw)
        elif it[0] == "text":
            _, s, x, y, h, col, bold, align, _m, _halo = it
            pg.text(s, x, y, h / 0.3528, col, bool(bold), align or "L")


# the one-way chain along the stream, upstream to the farms: (name, marker, programme, historic root, sources)
CHAIN = [("UPSTREAM ENTRY", "reeds", "reed basins clean once · terraces hold", None, (CHAIN_REF,)),
         ("K4", "hub", "hub + sub-hub · water-touching step", "Roman bridge · Tabaklar Hamamı", (PROG,)),
         ("K3", "hub", "hub + sub-hub · craft workshops", "tanning quarter (Tabakhane)", (PROG,)),
         (u"İSTİKLAL MEYDANI", "small", "hidden-stream square", u"over the %s tunnels" % landmark_name("kizil_avlu"), (PROG,)),
         ("K5", "hub", "hub + sub-hub · Demeter's Garden", "Roman bridge · Demeter, abundance", (PROG, GARDEN)),
         ("K6", "gate", "gateway out", None, (PROG,)),
         ("DOWNSTREAM REACH", "reeds", "floodable planting · boardwalk", "Late Antique workshops", (CHAIN_REF, PROG)),
         ("FARMLAND", "outside", "outside the site · water from storage", "Tersane cotton (16th c.)", (COTTON_H,))]


def chain_strip(pg, y_top):
    """the chain across the page: node names, the one-way water ribbon with hubs and sub-hubs, programme keywords and
    the historic roots (HER r2). v11: the symbol key is the legend item ag3_legend (G6-4: no key on the drawing).
    Returns the lowest y used."""
    n = len(CHAIN)
    x0, dx = 16.0, (404.0 - 16.0) / n
    yr = y_top - 6.0                                 # the ribbon
    xs = [x0 + 2.0 + i * dx for i in range(n)]
    wc, wd = _hu("WAT", 3), _hu("WAT", 2)
    pg.tag("water", "ribbon")
    pg.line([(xs[0], yr), (xs[2], yr)], wc, 1.6)
    pg.line([(xs[3] + dx * 0.5, yr), (xs[-1] - 4.0, yr)], wc, 1.6)
    pg.poly([(xs[-1] - 4.0, yr + 1.8), (xs[-1] - 0.6, yr), (xs[-1] - 4.0, yr - 1.8)], fill=wc, closed=True)
    pg.tag("water", "covered_reach")
    pg.line([(xs[2], yr), (xs[3] + dx * 0.5, yr)], wc, 1.6, (1.6, 1.1))   # the covered reach
    pg.tag("water", "flow_arrows")
    for i in range(n - 2):                           # one way, with the stream
        ax = (xs[i] + xs[i + 1]) / 2.0 + 4.0
        pg.poly([(ax - 1.2, yr + 1.1), (ax + 0.6, yr), (ax - 1.2, yr - 1.1)], fill=wd, closed=True)
    low = yr
    for i, (name, mk, prog, root, refs) in enumerate(CHAIN):
        x = xs[i]
        pg.tag("hubs" if mk in ("hub", "small", "gate") else ("plants" if mk == "reeds" else "fields"),
               "chain_" + name.lower().replace(" ", "_"))
        if mk == "hub":
            pg.rect(x - 1.6, yr - 1.6, 3.2, 3.2, fill=_hu("PUB", 3), stroke=_hu("PUB", 2), lw=0.2)
            pg.circle(x, yr - 3.4, 0.8, fill=_hu("PUB", 2))
        elif mk == "small":
            pg.rect(x - 1.1, yr - 1.1, 2.2, 2.2, fill=C["white"], stroke=_hu("PUB", 3), lw=0.4)
        elif mk == "gate":
            pg.line([(x - 1.2, yr + 1.8), (x + 0.8, yr), (x - 1.2, yr - 1.8)], C["ink"], 0.4)
        else:
            _ag_icon(pg, "clean" if mk == "reeds" else "outside", x - 2.5, yr + 7.5, 5.0)
        pg.tag("labels", "chain_" + name.lower().replace(" ", "_"))
        tx = x - 1.5
        pg.text(name, tx, yr + 3.6 if mk not in ("reeds", "outside") else yr + 8.4, 8.5, C["ink"], True)
        y = yr - 7.0                               # clear of the sub-hub dot
        mark = "".join(cite(r) for r in refs)
        lines = [(q, C["ink"]) for q in wrap(prog + ("" if root else (" " + mark if mark else "")), 7, dx - 3.0)]
        if root:
            lines += [(q, _hu("HER", 2)) for q in wrap(root + (" " + mark if mark else ""), 7, dx - 3.0)]
        for q, col in lines:
            pg.text(q, tx, y, 7, col)
            y -= 2.9
        low = min(low, y + 2.9 - 1.2)
    return low


WE_DO = [(1, "clean once, at the upstream end"), (2, "hold winter water"), (3, "strip first, all summer"),
         (4, "plant each step for the water it gets"), (5, "surplus to the farms outside, never drinking")]


def _ag3_photo(pg, key, x, top):
    """v11: a plant's photo as an image shape (x, top - PHOTO_H)..(x + PHOTO_W, top), cover-cropped to the box by a
    clip (never stretched), with a keep area. False (nothing drawn) when the photo did not load."""
    p, _cr, why = photo_get(key)
    PHOTO_N[1] += 1
    if not p:
        AG3_NOPHOTO.append((key, why or "not loaded"))
        return False
    px = None
    try:
        with open(p, "rb") as fh:
            px = jpeg_info(fh.read())
    except Exception:
        px = None
    W, H = PHOTO_W, PHOTO_H
    y0 = top - H
    if px and px[0] > 0 and px[1] > 0:
        s = max(W / float(px[0]), H / float(px[1]))
        iw, ih = px[0] * s, px[1] * s
    else:
        iw, ih = W, H
        LOG_NOTES.append("FLAG p17 photo %s: size not read, set to the box" % key)
    pg.image(x + (W - iw) / 2.0, y0 + (H - ih) / 2.0, iw, ih, p, clip=(x, y0, x + W, y0 + H))
    pg.keep((x, y0, x + W, top), "photo " + key, "photo")
    PHOTO_N[0] += 1
    return True


def ag3_bands(pg, top, pn=None):
    """the plant bands under the three rows (one column under each step) and, left, what goes, the odour and how to
    read the steps (28 Oct page_ladder part 3). Every plant of a step with its photo PHOTO_W x PHOTO_H, two side by
    side, its name "English (Turkish)" + the photo's credit mark under it; the species' reasons only when there is room
    (28 Oct rule). v11: a species whose photo did not load is never an empty box: it is named in one line "also:" under
    its band's photos and logged (BRIEF §6 row 17). v11: the left column goes into pn (its own drawing ag3_notes,
    booklet frame "ag3_note*"), the bands + photos stay in pg. Returns (lowest y of pg, lowest y of pn)."""
    pn = pn or pg
    yt = top - 3.0
    w = LAD_S * LAD_F
    per = 2 if 2 * PHOTO_W + PH_GAP <= w - 2.0 else 1
    lowest = yt
    for i, st in enumerate(STEPS):
        xa = LAD_X0 + i * w + 1.0
        el = "band_" + st["name"].lower().replace(" ", "_")
        pg.tag("labels", el)
        y = yt
        pg.text(st["name"], xa, y, 8.5, C["ink"], True); y -= 3.4
        pg.text(st["sub"], xa, y, 7, C["ink2"]); y -= 6.4
        tag_y = y
        y -= 4.0
        if st["band"]:
            l_, r_ = GEO["corridor"]["left " + st["band"]], GEO["corridor"]["right " + st["band"]]
            v = [(l_[k] + r_[k]) / 2.0 for k in ("trees", "grass", "farmland")]
            for q in wrap("today: trees %.0f %% · grass %.0f %% · fields %.0f %% %s" % (v[0], v[1], v[2], cite(TODAY)), 7, w - 4.0):
                pg.text(q, xa, y, 7, C["ink2"]); y -= 2.9
        if st["name"] == "FARMS":
            rm = cite(REUSE)
            for q in wrap(STEPS[4]["water"][1].replace(" {reuse}", (" " + rm) if rm else ""), 7, w - 4.0):
                pg.text(q, xa, y, 7, C["ink2"]); y -= 2.9
        y -= 1.2
        sm = cite(SPECIES)
        pg.text(("WE PLANT" + ((" " + sm) if sm else "")) if st["name"] != "FARMS" else "THEY GROW", xa, y, 7,
                _hu("GRN", 1), True)
        y -= 1.6                                     # the top of the first row of photos
        got = [(key, why) for key, why in st["plant"] if photo_get(key)[0]]
        miss = [key for key, _ in st["plant"] if not photo_get(key)[0]]
        low = y
        for r0 in range(0, len(got), per):
            n_ = 1
            for c_, (key, why) in enumerate(got[r0:r0 + per]):
                px = xa + c_ * (PHOTO_W + PH_GAP)
                pg.tag("plants", "%s_%s" % (el, key))
                _ag3_photo(pg, key, px, y)
                pg.tag("labels", "%s_%s" % (el, key))
                yy = y - PHOTO_H - 2.5
                nl = name_lines(key, photo_mark(key), 7, PHOTO_W)
                for q in nl:
                    pg.text(q, px, yy, 7, C["ink"], True); yy -= 2.6
                n_ = max(n_, len(nl))
            low = y - PHOTO_H - 2.5 - 2.6 * (n_ - 1) - 0.6
            y = low - 1.1
        for key in miss:                             # no empty box: the name in one line, logged
            AG3_NOPHOTO.append((key, photo_get(key)[2] or "not loaded"))
            PHOTO_N[1] += 1
        if miss:
            pg.tag("labels", el + "_no_photo")
            for q in wrap("also: " + ", ".join(plant_name(k) for k in miss), 7, w - 4.0):
                y -= 0.6
                pg.text(q, xa, y - 2.0, 7, C["ink"], True)
                y -= 2.9
            low = y
        lowest = min(lowest, low)
        pg.tag("annotations", el + "_job")
        pg.rect(xa, tag_y, text_w(st["job"], 8, True) + 4, 5.2, fill=_hu("GRN", 1))
        pg.text(st["job"], xa + 2, tag_y + 1.5, 8, C["white"], True)
        jx = xa + text_w(st["job"], 8, True) + 6
        for word, kind in JOB_ICON:                  # the job as pictograms beside the tag
            if word in st["job"]:
                _ag_icon(pg, kind, jx + 0.5, tag_y + 5.6, 5.0)
                pg.keep((jx + 0.5, tag_y + 0.6, jx + 5.5, tag_y + 5.6), "job icon " + kind, "icon")
                jx += 7.0
    # left column: what goes, the odour, how to read the steps (v11: its own recorder pn)
    pg = pn
    pg.tag("labels", "remove_giant_reed")
    y = yt
    gm = photo_mark("giant_reed")
    for t, sz, b in ((u"REMOVE: " + plant_name("giant_reed") + ((" " + gm) if gm else ""), 8, True),
                     ("raises flood risk, blocks bridges", 7, False)):
        for q in wrap(t, sz, LAD_X0 - 18.0, b):
            pg.text(q, 14.0, y, sz, C["ink"], b)
            y -= sz * 0.3528 * 1.35
    pg.tag("plants", "remove_giant_reed")
    if _ag3_photo(pg, "giant_reed", 14.0, y + 1.4):
        y -= PHOTO_H + 0.6
    y -= 3.0
    pg.tag("labels", "odour")
    sm = cite(SPECIES)
    for t, b in (("ODOUR: no measured plant effect" + ((" " + sm) if sm else ""), True), ("keep sewage out", False),
                 ("clean once, at the upstream end", False), ("plants: clean nutrients, give scent", False)):
        for q in wrap(t, 7.5, LAD_X0 - 18.0, b):
            pg.text(q, 14.0, y, 7.5, C["ink"], b); y -= 3.2
    y -= 3.0
    pg.tag("labels", "reading_notes")
    for t in ("steps = planting bands " + cite(BANDS), "depths above the bed " + cite(DEPTH), "a diagram, not to scale",
              "downstream flat end: Q100 1.4 m, Q500 1.5 m"):
        for q in wrap(t.strip(), 7, LAD_X0 - 18.0):
            pg.text(q, 14.0, y, 7, C["ink2"]); y -= 2.9
    return lowest, y


def ag_p17_items(ix):
    """v11 (round 6 S7): booklet p17 as items, drawn at the 28 Oct sheet places (A3 mm, y up) into one recorder per
    item and exported by ag_export_block (chain, three season rows, bands) + the steps list and the symbol key.
    Logs: section p17 ladder_<season> SKETCH (x3), legend p17 hues=table, trees p17 species=n generic=n."""
    CUR_PAGE[0] = AG3_PAGE
    AG3_TREES[0] = AG3_TREES[1] = 0
    del AG3_NOPHOTO[:]
    ix.list(AG3_PAGE, None, [lab for _, lab in WE_DO], numbered=True, id=AG3_ID["steps"], group=AG3_ID["chain"])
    ix.legend(AG3_PAGE, None, [
        (dict(kind="fill", colour=_hu("PUB", 3), stroke=_hu("PUB", 2), width_pt=0.6), "hub square, dry"),
        (dict(kind="dot", colour=_hu("PUB", 2)), "sub-hub in the bed, floodable"),
        (dict(kind="dash", colour=_hu("WAT", 3), width_pt=4.5, dash_pt=[4.5, 3.1]), "covered reach"),
        (dict(kind="line", colour=_hu("WAT", 3), width_pt=4.5), "one way, with the stream")],
        id=AG3_ID["legend"], group=AG3_ID["chain"])
    LOG_NOTES.append("legend p17 hues=table")
    pg = AgRec()
    y_chain = chain_strip(pg, 264.0)
    ag_export_block(ix, pg, AG3_ID["chain"], 1, 13.0, 270.0, 394.0, 270.0 - (y_chain - 1.0), 0.0, page=AG3_PAGE)
    top = y_chain - 2.0
    for r, sea in enumerate(seasons()):
        T_, B = top - r * ROW_H, top - (r + 1) * ROW_H
        y0 = B + 2.0 - LAD_GB * LAD_F                # page y of the sketch's 0
        mark = ((19.0 - LAD_X0) / LAD_F, (T_ - 6.0 - y0) / LAD_F)
        pg = AgRec()
        for it, (kind, eid) in ladder_row(sea, mark):
            pg.tag(kind, eid)
            sk_draw(pg, xform([it], LAD_F, LAD_X0, y0))
        pg.tag("labels", "season_column")
        if sea["mark"] == "olive":
            _ag_icon(pg, "olive", 14.0, T_ - 1.5, 9.0)
        pg.text(sea["name"], 26.0, T_ - 8.0, 12, C["ink"], True)
        pg.text(sea["months"], 26.0, T_ - 13.0, 9, _hu("WAT", 1), True)
        y = T_ - 18.5
        for t, ref in sea["side"]:
            mk = cite(ref) if ref else ""
            for q in wrap(t + ((" " + mk) if mk else ""), 7.5, LAD_X0 - 30.0):
                pg.text(q, 26.0, y, 7.5, C["ink"])
                y -= 3.2
        Y = lambda v: y0 + v * LAD_F
        X = lambda v: LAD_X0 + v * LAD_F
        fl = _hu("WAT", 1)
        if sea["key"] == "high":                     # flood levels first: they sit at their lines
            pg.tag("levels", "q500")
            dm = cite(DEPTH)
            pg.text("Q500 · 263 m³/s · 2.3-3.3 m above the bed" + ((" " + dm) if dm else ""), X(1.5), Y(LAD_Q500) + 0.8,
                    7, fl, positions=("NE", "N", "E"))
            pg.tag("levels", "q100")
            pg.text("Q100 · 205 m³/s · 2.0-3.0 m", X(1.5), Y(LAD_Q100) - 0.8 - 7 * 0.3528, 7, fl,
                    positions=("SE", "S", "E"))
            pg.tag("labels", "overtopping")
            pg.text("over the bank top only at K4 (right bank) and S4 (left)", X(3 * LAD_S + 3.0), Y(LAD_Q500) + 3.0,
                    7, fl, positions=("NE", "N", "NW", "E"))
            pg.tag("labels", "site_edge")
            pg.text("site edge: farmland outside", X(4 * LAD_S) + 1.0, Y(LAD_GY[4] + 6.0) + 0.6, 7, C["ink2"],
                    positions=("NE", "E", "N"))
        if sea["key"] == "low":
            pg.tag("labels", "stored_water_arrow")
            pg.text("stored winter water", X(3 * LAD_S + 22.0), Y(LAD_GY[4] + 6.5) + 1.0, 7, _hu("WAT", 2), True,
                    positions=("N", "NE", "NW"))
        for n_, (kind, x, yv, flip, lab, ref, al) in enumerate(sea["acts"]):
            if lab:
                pg.tag("labels", "act_%d" % n_)
                hgt = 0.0 if kind is None else (3.2 if kind == "sit" else 4.9)
                mk = cite(ref) if ref else ""
                ax = X(4 * LAD_S) + 1.5 if (al == "L" and x > 4 * LAD_S) else X(x)
                pg.text(lab + ((" " + mk) if mk else ""), ax, Y(yv + hgt) + 1.0, 7, C["ink"], True, al,
                        positions=("N", "NE", "NW", "E", "W") if al == "C" else
                        (("NE", "E", "N") if al == "L" else ("NW", "W", "N")))
        did = AG3_ID[sea["key"]]
        ag_export_block(ix, pg, did, 2 + r, 13.0, T_, 394.0, ROW_H, 0.0, page=AG3_PAGE)
        LOG_NOTES.append("section p17 %s SKETCH" % did.replace("ag3_", ""))
    bot = top - 3 * ROW_H
    pg, pn = AgRec(), AgRec()
    low, low_n = ag3_bands(pg, bot, pn)
    bx = LAD_X0 - 2.0                            # v11: bands + photos from the cut's left edge; the notes left of it
    ag_export_block(ix, pg, AG3_ID["bands"], 5, bx, bot, 13.0 + 394.0 - bx, bot - (low - 1.0), 0.0, page=AG3_PAGE)
    ag_export_block(ix, pn, AG3_ID["notes"], 6, 13.0, bot, bx - 4.0 - 13.0, bot - (low_n - 1.0), 0.0, page=AG3_PAGE)
    LOG_NOTES.append("trees p17 species=%d generic=%d" % tuple(AG3_TREES))
    for key, why in AG3_NOPHOTO:
        ix.warn(AG3_PAGE, "photo", u"no photo for %s (%s): its box is left out, the name is under the band" % (
            plant_name(key), why))
    CUR_PAGE[0] = AG_PAGE


# ------------------------------------------------------------------ v1.4: results.json (hectares per crop, keys as v1.3)
# v10 (G-R5-12): the v1.4-v9 crops (AG_CROPS, ag_crop, blocks.json, booklet_export), the v1.6 Placer and the sources
# page are gone: the drawings and texts are items (ag_items), the sources Sources rows (ix.source).


def ha_results(L):
    """hectares the storage irrigates per crop (page 1's bars): normal year and 1-in-5 dry year, lo-hi over the storage
    span (and the deficit saving range for olive), plus the dry-year ratio olive deficit / cotton."""
    p_lo, p_hi = span(L["farm_share_dry5_pct"]); n_lo, n_hi = span(L["farm_need_dry5_m3"])
    w_lo, w_hi = n_lo * p_lo / 100.0, n_hi * p_hi / 100.0
    rows = [("olive_deficit", "olive", DEFICIT), ("olive_full", "olive", None)] + \
           [(c, c, None) for c in ("maize", "tomato", "cotton") if c in NET]
    out = {}
    for key, crop, dfc in rows:
        if crop not in NET: continue
        out[key] = {}
        for yr, yk in (("normal", "normal"), ("dry", "dry5")):
            g = gross_m3_ha(crop, yr)
            lo, hi = (w_lo / (g * (1 - dfc[0])), w_hi / (g * (1 - dfc[1]))) if dfc else (w_lo / g, w_hi / g)
            out[key][yk] = {"lo": round(lo, 1), "hi": round(hi, 1), "m3_per_ha": round(g, 0)}
    R = {"ha_per_crop": out, "to_farms_dry5_m3": [round(w_lo), round(w_hi)],
         "farms_fed_ha": round(L["cropland_ha"] + L["orchard_ha"], 2)}
    if "olive_deficit" in out and "cotton" in out:
        a, b = out["olive_deficit"]["dry5"], out["cotton"]["dry5"]
        R["ratio_olive_deficit_vs_cotton_dry5"] = {"lo": round(a["lo"] / b["lo"], 2), "hi": round(a["hi"] / b["hi"], 2)}
    ys = L.get("year_split")
    if ys and "normal" in ys and "dry5" in ys:      # v3 (Prompt 6): page 1's double squeeze, dry year against normal
        a_, b_, c_ = squeeze(ys)
        R["stream_first"] = {"water_years": [ys["normal"]["water_year"], ys["dry5"]["water_year"]],
                             "left_for_farms_change_pct": round(100.0 * a_, 1), "need_per_ha_change_pct": round(100.0 * b_, 1),
                             "hectares_change_pct": round(100.0 * c_, 1)}
    return R


def ag_results(L):
    """v1.4 (v10: was the second half of booklet_export): results.json, hectares per crop, same keys, in
    cached/booklet/<AG_FOLDER>/ (the folder is made here, just before the write). Returns its path."""
    R = ha_results(L)
    R.update(script="AgriCulture", version=VERSION)
    d_ = bg_booklet(AG_FOLDER)
    os.makedirs(d_, exist_ok=True)
    p_ = os.path.join(d_, "results.json")
    with open(p_, "w", encoding="utf-8") as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
    return p_

# ------------------------------------------------------------------ items and run
AG_SRC = "agsrc%d"                   # v10: the source keys of this script's Sources rows ({src:agsrcN} in the texts)


def ag_items():
    """v10 (round 5 S9, G-R5-12; was build(path), CHK-12: a Button input named "build" read the function): reads the
    water balance results, exports booklet p17 (v11: the plant ladder) and p18's blocks (v10 p21), the crop photos, the farms map and every cited source as items
    and writes items.json. Returns (ix, L, src, farms log lines)."""
    L, src = live()
    NET.clear(); NET.update(L["net"])
    PHOTO_GOT.clear(); PHOTO_STATE.clear(); del PHOTO_LOG[:]   # v2: the plant photos, read once a press
    PHOTO_N[0] = PHOTO_N[1] = 0
    del SRC_KEY[:], LOG_NOTES[:]                   # v1.6: one source numbering for the whole script
    SRC_PAGE.clear()
    ix = Ix(AG_FOLDER, "bergama_agriculture_alternatives", VERSION)
    for pid, fn in ((AG3_PAGE, lambda: ag_p17_items(ix)), (AG_PAGE, lambda: ag_p18_items(ix, L, src))):
        AG_GRP[0] = AG_GRP[3] = 0; AG_GRP[1].clear(); AG_GRP[2].clear()
        fn()                                       # v11: p17 the plant ladder (pages/p17_ladder.py), p18 the blocks
        LOG_NOTES.append("groups %s kinds=%d elements=%d untagged=0 (block-level annotations: %d shapes; texts are "
                         "label items)" % (pid, len(AG_GRP[1]), len(AG_GRP[2]), AG_GRP[3]))
    farm_lines = ag_farms_items(ix, L, src)
    for i, k in enumerate(SRC_KEY):                # v1.6's numbered key, now the booklet's Sources rows
        ix.source(AG_SRC % (i + 1), k, None, page=SRC_PAGE.get(k, AG_PAGE))   # v11: on its first page
    ix.save()
    return ix, L, src, farm_lines


def main():
    """v10: export the items and results.json; the log = head, "<n> warnings" + every WARNING line (wn_compose), then
    the run's lines. Nothing is written to output/ (C2)."""
    t0 = time.time()
    wn_reset()                                     # v10 (C1): one warning sink per run
    ix, L, src, farm_lines = ag_items()
    rp = ag_results(L)
    lines = [ix.summary(), "results %s  %s" % (rp, time.strftime("%H:%M:%S")), "trigger: %s" % TRIG_WHY[0],
             "figures: %s" % src] + list(LOG_NOTES) + farm_lines + photo_log().split("\n")
    if src == DEFAULT_NOTE:
        lines.append("FLAG: water balance results file not found in Downloads; its default-lands copy was used")
    head = ["agriculture alternatives %s · %s · %.1f s" % (VERSION, time.strftime("%Y-%m-%d %H:%M:%S"), time.time() - t0)]
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
TRIG_WHY = ["run outside Grasshopper"]   # v9 (round 4): what started this run, for the log ("trigger: <why>")


def done_text(ran, ok, secs):
    """The done output: kept until the next run (this Rhino session)."""
    return ("done " if ok else "ERROR ") + time.strftime("%H:%M:%S") + ".%02d" % int((time.time() % 1) * 100) + \
        " · %.0f s" % secs if ran else None


_gh = "ghenv" in globals()
if _gh:
    import scriptcontext as _sc
    try: _ik = ":" + str(ghenv.Component.InstanceGuid)   # 25 Oct 10:29: each component keeps its own log and done
    except Exception: _ik = ""
    # v9 (round 4): the one trigger file (common/trigger.py): a press of the Button (its rising edge) or a NEW done
    # text from the script before in the chain; the script's own trigger copies are gone
    _pressed, _why, _btn = trig_should_run("bergama_agri_alt_log_chain")
    TRIG_WHY[0] = _why
    if _pressed:
        _t0 = time.time()
        try:
            _res = main()
        except Exception as _ex:   # 25 Oct: the error goes into the log panel, the old log never stays
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-600:])
        _sc.sticky["bergama_agri_alt_log" + _ik] = write_log(_res)
        _sc.sticky["bergama_agri_alt_log_status" + _ik] = ("ERROR" if _sc.sticky["bergama_agri_alt_log" + _ik].startswith(("ERROR", "The PDF is open")) else time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky["bergama_agri_alt_log_done" + _ik] = done_text(True, not _sc.sticky["bergama_agri_alt_log_status" + _ik].startswith("ERROR"), time.time() - _t0)
        _sc.sticky["bergama_agri_alt_log_ver" + _ik] = VERSION
    if _sc.sticky.get("bergama_agri_alt_log_ver" + _ik) != VERSION:   # v1.7 (Aras 27 Oct 15:35): a newly pasted version
        for _s in ("", "_status", "_done"):                            # shows itself at once, idle, no old time or log
            _sc.sticky.pop("bergama_agri_alt_log" + _s + _ik, None)
    done = _sc.sticky.get("bergama_agri_alt_log_done" + _ik, "idle")   # 25 Oct 10:20: stays after the run; wire into the next script's run (one-click chain)
    log = _sc.sticky.get("bergama_agri_alt_log" + _ik, "Press the Button to export to " + bg_booklet(AG_FOLDER))
    print(log)               # 25 Oct 12:10: the canvas's log output is Grasshopper's "out" (printed text): print the log
    try: ghenv.Component.Message = "AgriCulture " + VERSION + " · " + _sc.sticky.get("bergama_agri_alt_log_status" + _ik, "idle")   # Aras 25 Oct 09:44
    except Exception: pass
else:
    print(write_log(main()))
