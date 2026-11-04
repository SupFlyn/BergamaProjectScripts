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
#@include ../common/bergama_paths.py
#@include ../common/warn.py
#@include ../common/plant_photos.py
#@include ../common/icons.py
#@include ../common/grid.py
#@include ../common/text_place.py
#@include ../common/marker.py
#@include ../common/data/NAMES.py
#@include ../common/names.py
#@include ../common/data/FACTS.py
#@include ../common/facts.py
#@include ../common/item_export.py
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
#@include data/GEO.py

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

#@include ../common/rgb.py
#@include ../common/hues.py


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


#@include ../common/pdf_fonts.py
#@include ../common/font_metrics.py

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
#@include ../common/fmt.py
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
#@include ../common/_tree_rand.py
#@include ../common/sketch_engine.py
#@include ../common/xform.py
#@include ../bergama_proposal_sections/data/SKETCH_SRC.py
#@include data/STEPS.py
#@include pages/p17_ladder.py


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

#@include ../common/trigger.py
TRIG_WHY = ["run outside Grasshopper"]   # v9 (round 4): what started this run, for the log ("trigger: <why>")


#@include ../common/done_text.py


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
