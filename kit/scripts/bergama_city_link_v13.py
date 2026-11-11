# CURRENT VERSION: bergama_city_link_v13.py = v13 (11 Nov 2026, round 9 Part CL: the round 9 shared modules pasted (frames_r9, hues r9, basemap context, key map, marker badges, item export); p08 corridor map and p09 spine map in basemap mode context over r9_window with a focus box, drawn at the ADDENDUM §0 true scale; the who comes chart and which bank drawn at their frame sizes; the five hub cards at 76 x 102 with their parts exported for the booklet's box; every marker a badge; names table r9). Earlier: bergama_city_link_v12.py = v12 (5 Nov 2026, round 7 S5: spine fixed at SON's 1:10,000 (no pick, WARNING if over its SON frame), map names small (G7-2, 5 pt), who-chart source marks after the line as set (L6), scale log lines); v11 (4 Nov 2026, layout plan L7: every map name (landmarks, streets, the stream) is handed to the booklet as a label anchored on its point; no name is left out by this script, the booklet places them); v10 (round 6, session S4, 4 Nov 2026: p08 + p09 for the 22-page booklet: G6-6 category hues (common/hues.py), G6-9 element groups, G6-4 no leader lines, hub codes K4/K3/T/K5/K6 on every map and card; p09 = SON page9 + page10 merged (spine map restored from c493fac page_spine, plans widened to the hub columns at one scale, no key map, flood rule SKETCH, bottom band enlarged); p08 who-chart source marks clear of their blocks; v9.2 hunks ported into src); v9.2 (fix 2 Nov: run warnings, p10 zones off the water + key map); v9.1 (fix 2 Nov: p10 hub-square trees by the plant module); v9 (round 5 S9: items, no sheet PDF); v8.x / v7 (round 4)
# bergama_city_link_v6.py (v6, 31 Oct: round 3, p08 one corridor arrow over the whole study area + p09 hub plans; v5.1, 31 Oct: bugfix, rebuilt with the shared base map fix of 31 Oct: the stream (M5 water) no longer stops on "list - float"; v5, 30 Oct: revision T5, p8 framework map + who calendar, p9 spine) · Thread 4 of the 22 Oct batch: connection to the city (the streamside spine and what it adds)
# Runs as delivered in: Grasshopper Python 3 component (a Button wired into the input `run`; outputs `log`, `done`),
# Rhino 8 ScriptEditor (Python 3), or plain Python 3. v9 lays out no page and writes NO PDF (round 5, G-R5-12 and
# Aras's addendum 1 Nov 22:37 point 2: the booklet is the only output of the drawings). Each press writes:
#   Downloads/Bergama/cached/booklet/Bergama_city_link_analysis/items.json   every drawing and text of booklet p08
#        and p10 as items (common/item_export.py; the booklet sizes, places, aligns and checks them):
#        p08 THE STREAM JOINS THE TOWN WHERE THE SHOPS ALREADY ARE: the corridor map (true scale, m, the site frame's
#            axes) with its heading, legend and shops note; who comes to the stream and when (a chart in mm) with its
#            heading, note and legend
#        p10 THE STREAMSIDE SPINE, HUB BY HUB: the key map (common/keymap.py km_map + km_items), one plan window per
#            bridge place (ONE window size in m for all, true scale), one hub diagram per hub of the same structure
#            (grouped with its window), the plans' legend, the flood rule, which bank, the producers' market
#   Downloads/Bergama/cached/Bergama_city_link_analysis/city_link_results.json   (same keys as before)
#   Downloads/Bergama/logs/bergama_city_link_log.txt
# Nothing is written to output/ (C2). How we know it ran: the component text reads "CityLink v9.1 · HH:MM · n s"; the
# log's head is "city link v9.1 · <time> · <s> s", then "<n> warnings" (= the WARNING lines listed right under it),
# and the run lines include "items bergama_city_link: … -> …/items.json".
# NEW IN v9 (round 5 S9, 2 Nov 2026; BRIEF P08.1-P08.3, P10.1-P10.4, G-R5-1/3/8/12, C1, C2, C10, CHK-12):
#   * G-R5-12: the page functions draw into a recorder (Page: page mm, y up, nothing written); cl_drawing() makes
#     one item drawing per booklet block (maps true scale in m, diagrams and charts in mm); every word inside a
#     drawing is an anchored label, titles / intros / headings / notes / legends are text and legend items; sources
#     are {src:key} marks + ix.source rows. write_pdf, the A3 sheet, booklet_export and blocks.json are gone.
#   * P08.1: the shop streets ranked by their shops (the site board's order): the first in ochre, the others in the
#     palette's 8B2D2D, thinner (a street of lower rank, far from the stream's blues); each carried on along the
#     OpenStreetMap street centrelines to the map's edge (cl_street_extend). P08.2: the project corridor line along
#     the stream (and its end bar in the water) is gone. P08.3: the map and the chart are separate drawings, sized
#     by the booklet.
#   * P10.1: the locator is the key-map module (km_map fitted and turned, km_items exported); no own north arrow,
#     neatline or scale. P10.2: one window size in m for every hub (hub_plan_layout). P10.3: one hub diagram per hub
#     with the same structure, grouped with its window. P10.4: the layout is the booklet's.
#   * C10: the masterplan's corridor (spine, hub squares, movement) read with bg_result + bg_this_run (WARNING p10
#     stale when not from this chain run); the bank comparison with the last results file ("press the chain once
#     more") is gone: the vote is the one of this run's site board file (WARNING p10 stale when that file is older
#     than this chain's Button press). C1: warn.py; nothing raises on text; log head "<n> warnings". CHK-12:
#     build() -> cl_items().
# city_link_results.json = the spine, the function sites and (v1.11) the hubs in survey coordinates. The site board (selinus_board v34,
# plan 07) reads it for the movement potential with the spine; the masterplan builds the same spine from common/city_spine.py (v6.2).
# Read live on every run: the water balance results (farm areas for the producers' market) and the site board's
# movement result (walking potential on the spine), each with a flagged fallback.
# Notes for Aras: batch_2026-10-22/thread4_city_link/NOTES.md (every figure with its source).
import os, time, json, zlib, math, base64

VERSION = "v13"  # v13 11 Nov (round 9 Part CL: modules r9, p08/p09 maps context + window + focus at the §0 scale, charts and hub cards at frame size, card parts, badges, names r9); v12 5 Nov (round 7 S5): spine 1:10,000 fixed, names 5 pt (G7-2), who marks after the set line (L6), scale lines; v11.2 fix: common key map names never left out (the booklet places them); v11.1 fix 4 Nov (kit v4.1 run): p09 legend rows passed as swatch dicts (cl_sw), was TypeError 'function' object is not iterable; v11 4 Nov (L7: names anchored for the booklet, none left out); v10 4 Nov (round 6 S4, see line 1); v9.2 2 Nov (run warnings, port in src); v9.1 fix 2 Nov (round 5 open rows, G-R5-6): the p10 hub-square planes come from common/plants.py (pla_plan) instead of 16-gon discs in the local green; v9 2 Nov (round 5 S9): items for the booklet, no sheet PDF (NEW IN v9 above); v8.2 1 Nov 22:10 (Aras 19:49): p08 north arrow off the margin, p10 key names off the hub markers, flood lines 3.5 mm apart; v8.1 1 Nov 21:40 (Aras 19:33): every layout check that stopped the run (text size, lines, column width, rows, legend room) is a WARNING line and an orange warning; 6.00 pt no longer counts as under 6.0; v8 1 Nov 20:55: text collisions are orange warnings with one WARNING line each, the run goes on (Aras 1 Nov 17:11 + 18:52); v7 (round 4, S5, 1 Nov 2026): p08 and p10 redrawn on the shared round 4 modules (see NEW IN v7); v6.5 fix 1 Nov 08:30: only the component's own inputs can start it (a True setting inside the script no longer does); v6.4 fix 1 Nov 08:20: chain trigger keyed to each solve (Rhino keeps globals), so the chain continues after ZoneBase; v6.3 fix 1 Nov: a pasted or rewired component no longer runs by itself (chain trigger notes the wire on its first solve)
# NEW IN v7 (round 4, session S5, 1 Nov 2026; BRIEF P08.1-P08.3, P10.1-P10.6, G-R4-1/2/4/7/9/11; a feature change,
# so the next whole number; design spec revision_2026-11-01_round4/handover/S5_design_spec.md):
#   * Text (G-R4-1): every text of both pages is registered in the page's TextPage (common/text_place.py) with its
#     real Arial box (common/font_metrics.py) as it is drawn; pg.check_text() RAISES TextCollision on any text over
#     text, over a marker or map, or past the page margins (the sheet is then not written; the log names both items).
#     The Helvetica width table, label_place.py (lp_place, Legend, lp_overlap_flag) and the slanted street names are
#     gone; no widow lines (cl_wrap keeps >= 2 words on a last line).
#   * Maps (G-R4-4): both pages draw through map_draw (common/map_layers.py): the muted base (light houses with
#     closed outlines) at the bottom, the D9 tint, our lines, the study line, our markers and labels on top; p10's
#     proposals are clipped to the study area. North arrows are north_items (no plate, G-R4-9); every number in a
#     circle is mk_marker (glyph centred, colour = what it names, G-R4-7).
#   * p08 (P08.1-P08.3): the heavy multiplied band with its orange arrowheads is gone: the project corridor is ONE
#     thin line along the stream with a bar at each end, over the study area's light tint; the hubs are numbered 1-5
#     (the p10 numbers) with their names in the legend; the shop streets in ochre; the shops headline wraps without a
#     widow; the calendar rows are 3.4 mm apart.
#   * p10 (P10.1-P10.6): a key map (km_map) at the left of the plan row locates every plan (red frames + numbered
#     markers); each plan carries its number and real name; the order is plans, their legend, then the hub cards
#     (five columns, bigger text and glyphs); the plans are 70 mm high; the masterplan's hub squares
#     (masterplan_results.json "hub_squares") are drawn with their trees; the spine is one continuous simplified
#     solid line (no dashed deck squiggle, runs under 8 m dropped) and the streamside walks are no longer drawn.
#   * G-R4-11: every landmark, street and square name from the names table (landmark_name / bridge_name), in Turkish
#     (Kızıl Avlu, Ulucami); no translated name is left in this script.
#   * Run trigger: common/trigger.py (trig_should_run); the log prints "trigger: <why>".
# NEW IN v6.2 (1 Nov 2026, Aras 07:48): the spine, its bank vote and the stops moved to common/city_spine.py, which
# the masterplan includes too, so the masterplan no longer reads city_link_results.json; city link runs once, after
# the masterplan. Same spine, same vote, same pages.
# NEW IN v6 (round 3, 31 Oct 2026, session B4, BRIEF P08.1 P08.3 P09.1-P09.3, D1 D9, G2 G3 G4 G16 G17 G19; a feature
# change, so the next whole number): p.08's framework is the basic whole-corridor overview (D1): the project is ONE
# corridor arrow along the stream from the upstream entry to the downstream end of the study area (corridor_line: the
# study area's chainage on STREAM_REF), the shop streets today under it, the hubs on top; only place names, placed
# by lp_place without leaders (numbers + key where there is no room), never over the corridor; the shops figure is a
# headline beside the legend; road changes, bus line, crossings and the spine move to p.09. p.09 zooms into each
# bridge place: six plans in stream order at one scale (hub_windows, hub_plan_layout, hub_plan: stops, sub-hub
# crossing in the bed, footbridges, spine, walks, road changes, bus stops) with its card under it (no frames, no
# K-code badges, text laid out by real line heights: no overlap) and one key; real names from common/names.py;
# FLAG overlap p08 / p09 in the log; no borders (maps keep a 0.25 pt neatline).
# REVISION 30 Oct 2026 (booklet revision, page thread p.08 ① ② + p.09; version set by the lead): p.08's framework in
# one graphic language on the faint shared base (M3) with its legend beside it (M2 Legend) and lp_place labels, scale
# bar and north arrow; the who calendar over soft seasons with the stream's monthly flow, places open per month,
# figures on the year and icon rows (R03, R05); p.09's map = the whole study area with its one outline and the
# masterplan's streamside walks, hubs as badges matched on the cards (no leaders), the flood rule as a stair, which
# bank with a bank glyph per piece, the market's farm areas from M10 facts (no typed fallback).
# NEW IN v4.1 (bugfix, revision 29 Oct T5 fix pass, Aras 22:08): the flood depths over the bed on p.08's flood tile and
# p.09's bank-top rule come from the level table (common/data/LEVELS.py, cuts S1-S8: Q100 and Q500 minus the bed, and
# where Q100 tops a bank), no longer typed in (they read "Q100 2.0-3.0 m · Q500 2.3-3.3 m", against 1.71-4.25 m there).
# NEW IN v4 (T3a WO-T3a-5, 29 Oct 2026, package B, decisions D3 b, D8 b, D10 a; a feature change, so the next whole
# number): the movement pages are three: p.07 how people use it (site board), p.08 this sheet's page 1, p.09 its
# page 2. Page 1 = ONE framework diagram (framework_map: shops and uses as soft zones, the stream hidden where the
# main road meets it, the busiest streets on foot and by car, the masterplan's road changes as arrows, the town bus
# line, the streamside spine, new crossings, hubs with walk-reach rings; refs R27-R30 as ideas) on the shared simple
# basemap (common/basemap.py), with who the project brings (who_panel, G7 / R31: a block per user group, its size as
# a bar, the places that serve it on one month axis, one line of conclusion) and the seven reasons. The v3 shops
# plan, the two shop charts and the walking potential bars are gone (D3 b: the street sections the site board draws
# replace them). Page 2: the schematic strip is now a map on the same basemap (hubs, bus stops, places, spine),
# decluttered; pictograms from the shared icon set (common/icons.py) where it has one. Sources: only public ones get
# a [n] (D13; cite() keeps PUB_SRC only). Reads the site board's movement_framework.json (FW_FILES).
# NEW IN v3 (MIRAQUA 28 Oct, booklet revision v4; a feature change, so the next whole number):
#   * Page 1 (booklet p.08): street and stream names along their own lines, the other labels placed clear of each
#     other with leaders (P08.1, G4); the covered reach as a thin strip under chart A's axis, no block behind the bars
#     (P08.2); the study-area outline and its key row (G8); lengths in m (G13); flood tile: over the banks only at S4,
#     K4 before the DSİ walls (bank depth research 28 Oct §4.2).
#   * Page 2 (p.10): the strip at 1:5,000 along the stream with its own scale bar, panels numbered 1, 2, 3 (F9); reach
#     on foot as a thin rim under the band in three classes to the nearest hub (P10.1); Oriental plane (Doğu çınarı)
#     and crops in English (Turkish), Corn (Mısır) (F13, G11); K4 card and flood-rule row as page 1; ha, terrace +1.00 m.
#   * Both pages: no big page number and no "PAGE n OF 2 · GROUP 6" line (F10, G1); bold keywords (G5); no [n] for
#     sources that are not public online (F5). Booklet crops cl_why_1 to cl_why_3 for the pp.07+08 alternative.
# NEW IN v2.1 (bugfix, Aras 27 Oct, booklet Prompt 8 "final check of every page"): page 1 (booklet "Why shops meet
# the stream only where it is hidden"): the "PEDESTRIANS ON THE STREETS · no data" row of who comes is gone (rule: no
# "no data" rows; no count exists, so no estimate either) with its source, the five rows that stay share the six rows'
# height, and walking potential's [n] moves up one (the source key follows); chart A prints "0" on its empty 100 m bins
# too. Page 2: the corner note names the heritage loop drawing instead of a booklet page number (the pages moved).
# NEW IN v2 (Aras 27 Oct 17:34, booklet Prompt 3 "movement and the city"; a feature change, so the next whole number):
# page 1 (booklet p9): the plan is the whole site frame at 1:10,000 on the frame's own axes (one scale, frame and north
# with the site board's movement maps), a band across the top, with light context underneath in layer order (water,
# homes by the sections' building types, bridges K1-K6, streets by class: the site board's city_context.json, v46+)
# and the shops (the board's OSM points for the whole frame), the main spine and the open / covered stream on top as
# the strongest layer; scale bar and north arrow under the plan, the key beside it; the two charts side by side under
# it. Page 2 (booklet p11): the spine and the hubs as gradients of reach, not a fixed line of a fixed length: each hub
# a fading field along the stream out to the movement method's walking radius (read from the board, 800 m), tints
# multiplied (PDF blend mode) so overlapping reaches darken; the spine a soft band fading out past K4 and K5; no
# length in the title or label. Hub cards, flood rule, bank and market unchanged. The info pane shows the pasted
# version at once. Without the board's context file both pages still draw (logged: no context, central shops only).
# NEW IN v1.11 (Aras 27 Oct 11:07, revision_2026-10-27/PHASE2_SPEC.md §6; history decisions D2 D3 D6 D8 D10; Aras
# 12:05 on the transit hub): both pages white (the beige paper goes) and without the source footer (the [n] marks
# stay; their sources go to booklet/blocks.json "sheet_sources"); no sentences, keywords and pictograms; text >= 7 pt;
# every text box is recorded and labels are placed clear of other text (Page.hit, spot, label: overlaps and labels
# left off go to the log). Page 1 (p9): new layout in reading order: (1) the plan, now 1:5,000 and the focal point,
# with "31 of 57 shops" pinned to the road crossing and the places named large; (2) and (3) the two charts beside it;
# (4) the reasons; (5) who comes and (6) walking potential at the bottom. Page 2 (p17): the 8 stops regrouped into
# the bridge places (HUBS): K4, K3, K5 walking hubs (dry hub with plane trees above Q500 + sub-hub in the bed),
# İstiklal Meydanı + Kızıl Avlu the main transit hub (MAIN_TRANSIT_HUB), K6 the gateway; each with its existing
# OSM bus stop, the metres to it (calculated) and its lines (h03 Q1); a town line to K4 as a proposed later step.
# The city heritage loop is not drawn here (page 6). city_link_results.json gets "hubs"; every earlier key stays.
# NEW IN v1.10 (Aras's deck review of 26 Oct 07:06, p.12 and p.21; library/_index/revision_2026-10-26.md R2):
# p.12: the main spine plan now locates the shops too: every OSM shop / café / restaurant / bar in the plan's window as a
# dot in the shop colour of chart A (SHOPS_XY, built-in data, same OSM extract and tags as the shop counts), next to the
# covered reach and the main road crossing it already showed; a key row and a context line (what the plan shows, what
# to take from it) under the plan. Chart B: the "n" (buildings) of a short bar sits above its value, no longer pale on
# the bar. p.21: a context block in the strip's empty corner (what the spine stands for, why it is there, how to read
# it: spine, main spine, stops, who each serves). Every v1.9 panel, figure and source stays.
# NEW IN v1.9 (Aras 26 Oct 06:39: "for this page we used to have main spine showing where the main activity is at we
# need to insert that into this page aswell without losing any data in this page (it can be little more cramped)"):
# page 1 gets back a plan of the MAIN SPINE (Bankalar - Kınık Caddesi, the street of the shops and the through road)
# and the Selinos stream at 1:10,000 (x and y alike): the one crossing over the covered reach. Drawn from data the
# project already holds: MAIN_SPINE below (in city_link_results.json since v1, drawn by the masterplan) and the
# masterplan's stream reference line (STREAM_REF, built-in data). The top row is three panels now (plan, chart A,
# chart B, the charts narrower); every panel, figure and source of v1.8 stays, and the old [n] numbers stay.
# "main road crosses" no longer runs through the "stream covered" label. Booklet: blocks.json gets the plan's crop.
# v1.8 (Aras 25 Oct 21:47-21:51, booklet/CROP_SPEC.md): the booklet shows this sheet's own drawings: booklet/blocks.json
# lists one crop per panel of the two pages (rects from the layout numbers P1_* / P2_* below); the separate booklet
# redraw (c2_hero.pdf, booklet_spine) is gone. Sheet words: the Selinos is a stream (titles, labels, keywords), no
# caveat notes ("not designed here ...", "not to scale", "no mahalle populations yet" taken off; open points go to the
# log). Figures (booklet/research/FIGURE_CONFLICTS.md): the spine length is the masterplan's drawn pieces read live
# (was a typed "about 660 m"); the typed bed depth "1.1-6.7 m" is gone (no results file carries the board's live value).
# Layout and look unchanged.
# v1.7 (A3 booklet, SCRIPT_STANDARD §8, booklet/content/STAGE2_BRIEF.md): also writes booklet/c2_hero.pdf (the streamside spine
# strip drawn at its booklet frame size, no text) + booklet/blocks.json (its words as labels); city_link_results.json gets
# "shops" (the page 1 shop figures, computed by shop_figures()). The two sheet pages are unchanged.
# v1.6 (Aras 25 Oct 17:00, visual first; audit batch_2026-10-25_visual_first/VISUAL_AUDIT.md §3): reasons as pictogram tiles,
# who comes as a people bar chart (log scale, "no data" bar), chart figures as callouts, walking potential as bars, stops as
# pictogram + keywords, events as a Jul-Sep calendar strip, flood rules as pictograms, bank vote as paired bars, sources as
# [n] with one numbered key per page. Flood depths corrected to research/rain_river_levels/README.md v1.1 (line 49).
# v1.5 (Aras 25 Oct 09:34-09:35): the same names in every script: the Button goes into an input named run, the log comes out of an output named log, and the log file is Downloads/Bergama/logs/bergama_city_link_log.txt (next to cached/ and output/), overwritten by each press.
# v1.11 (Aras 27 Oct 12:05): the main transit hub of page 2: "İstiklal" = İstiklal Meydanı + Kızıl Avlu (the town lines
# 651/652/653 stop there; K3, K4, K5 are walking hubs); "bridges" = K3, K4, K5 drawn as the transit hubs instead
MAIN_TRANSIT_HUB = "İstiklal"
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


def write_log(text):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, "bergama_city_link_log.txt"), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    return text

# all files under Downloads/Bergama/ (Aras rule, 24 Oct)
BERGAMA = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
CL_FOLDER = "Bergama_city_link_analysis"   # v9: cached/booklet/<this>/items.json and cached/<this>/ (no output/ folder: C2)
RES_DIR = bg_cache(CL_FOLDER)             # 27 Oct: city_link_results.json (the board and masterplan read it)
OUT_JSON = "city_link_results.json"
WB_FILES = [os.path.join(bg_cache("Bergama_water_balance_analysis"), "water_balance_results.json"),   # 27 Oct: cached/
            os.path.join(BERGAMA, "output", "Bergama_water_balance_analysis", "water_balance_results.json"),
            os.path.join(os.path.expanduser("~"), "Downloads", "Bergama_water_balance_analysis", "water_balance_results.json")]
# v9 (round 5, C10): the site board's movement (bank vote) and the masterplan's corridor are found with bg_result
# (cached/<script>/, cached/<script>/from_output/, output/<script>/) and dated with bg_this_run in live()
MV_FILE = ("selinus_board", "city_link_movement.json")          # written by selinus_board v34+
MP_FILE = ("bergama_masterplan", "masterplan_results.json")     # v1.8: the drawn spine's length; v9: the corridor
BD_FILES = [os.path.join(bg_booklet("selinus_board"), "results.json"),                    # v1.8: bed depth (board v40)
            os.path.join(BERGAMA, "output", "selinus_board", "booklet", "results.json")]

# v1.9 STREAM_REF: the Selinos reference line of the masterplan (v11, Thread 5, calculated 24 Oct 2026): OpenStreetMap
# "Selinos Çayı" (extract of 28 Jul 2026) converted with the h01 §0 formula (+-10-30 m), moved onto the middle of the
# survey channel (HIDRO_DERE_SULU / walls) and thinned to 10 m; a covered flag per segment (OSM tunnel / culvert ways).
# Zipped JSON {"P": points, "covered": flags}; drawn on page 1's main spine plan.
def bergama_data(name, _c={}):
    """Built-in data kept in Downloads/Bergama/Data/bergama_city_link_data.py (Aras 25 Oct 21:29, scripts shortened): runs its
    section `name` here, as if it were written in this place. The file is read once per run; a missing file or one
    from another version of this script stops the script with a message saying which file to copy."""
    import os as _os, hashlib as _hl
    if not _c:
        p_ = _os.path.join(_os.path.expanduser("~"), "Downloads", "Bergama", "Data", "bergama_city_link_data.py")
        if not _os.path.isfile(p_):
            raise RuntimeError("Data file missing: copy bergama_city_link_data.py from the run kit's Data folder into " + _os.path.dirname(p_))
        with open(p_, encoding="utf-8", newline="") as f_:
            for part_ in f_.read().split("\n#@@ ")[1:]:
                k_, _, b_ = part_.partition("\n")
                _c[k_] = b_
    b_ = _c.get(name)
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != {'STREAM_REF': '6462357102432c243b7a34f595c055c7', 'SHOPS_XY': '938d12716e4355018e4de86927b3b4ab', 'LEVELS': '3cc5394beb1de45118b6226d608a766b', 'NAMES': '06f1746b6cc05729b557d9f37713906f', 'FACTS': 'e402c1370c04b7b8df8f86c4eccbf011'}.get(name):
        raise RuntimeError("Data file bergama_city_link_data.py is not the one made with this script version (part " + name +
                           "): copy it again from the same run kit as the script")
    exec(compile(b_, "bergama_city_link_data.py:" + name, "exec"), globals())


bergama_data("STREAM_REF")
# v1.10 SHOPS_XY: shops on page 1's plan = OSM shop=* and amenity cafe/restaurant/fast_food/bar/pub/ice_cream (nodes,
# and buildings at the mean of their corners) of the same extract (28 Jul 2026, bergama_osm.osm of the commercial spine
# thread), converted with the h01 §0 formula (+-10-30 m), kept inside the v1.11 plan's 960 x 740 m window (survey x
# 29700-30660, y 31570-32310): 150 places (calculated 26 Oct 2026). v2: the plan covers the whole site frame and takes
# the site board's shop points (same OSM file and tags, city_context.json); these are its fallback (window only, logged)
bergama_data("SHOPS_XY")
bergama_data("LEVELS")
# ---- Level table reader (H-levels 29 Oct 2026; WO-T2a-2) ------------------------------------------------------------
# Reads LEVELS (../common/data/LEVELS.py: one row per cut crossing, every number a {value, status, source[, public]}
# dict; the row schema and how to add a row are at the top of that file). Include the data first:
#   #@include ../common/data/LEVELS.py
#   #@include ../common/levels.py
# Values come back as floats rounded to 2 decimals (levels and heights m, widths cm), None where a field is absent or
# has no value (a bank with no crest). No drawing and no label text here: nothing about a status is ever printed on a
# page (Aras); level_public_source() gives the one source text a page may print, and only for a published source.
# A cut id with one crossing names its row ("S4", "W1"); S5 and S6 have rows "S5-1".."S5-3", "S6-1".."S6-3", and
# their bare id ("S5") is accepted only where the answer is the same on every crossing (ends, end labels).

def _lv_rows():
    """the LEVELS rows, or a clear stop when the data part was not included"""
    rows = globals().get("LEVELS")
    if rows is None:
        raise RuntimeError("LEVELS data missing: include ../common/data/LEVELS.py before ../common/levels.py")
    return rows


def level_ids():
    """the row ids in table order"""
    return [r["id"] for r in _lv_rows()]


def _lv_cut_rows(cid):
    """the rows of a bare cut id ("S5" -> its crossing rows), [] when there are none"""
    return [r for r in _lv_rows() if r.get("cut") == cid]


def level_cut(cid):
    """the row dict of cut (crossing) cid (an alias such as F1 -> W1, F3 -> S4 is accepted); KeyError naming the
    known ids"""
    for r in _lv_rows():
        if r["id"] == cid:
            return r
    for r in _lv_rows():
        if cid in (r.get("aliases") or ()):
            return r
    many = _lv_cut_rows(cid)
    if len(many) == 1:
        return many[0]
    if many:
        raise KeyError("level cut %s crosses the stream %d times: use one of %s"
                       % (cid, len(many), ", ".join(r["id"] for r in many)))
    raise KeyError("no level cut %r; known: %s" % (cid, ", ".join(level_ids())))


def _lv_value(cid, key, side=None):
    """the {value, status, source} dict of a field (side "NE"/"SW" for a bank field), None if absent"""
    r = level_cut(cid)
    if side is not None:
        if side not in ("NE", "SW"):
            raise KeyError("level side must be 'NE' or 'SW', not %r" % (side,))
        r = r.get(side) or {}
    v = r.get(key)
    return v if isinstance(v, dict) and "value" in v else None


def _lv_r2(x):
    return None if x is None else round(float(x), 2)


def level(cid, key, side=None):
    """the value of a field as a float (level("S4", "bed"), level("W1", "top", "NE"), level("S4", "q500")); None if
    the field is absent or has no value"""
    v = _lv_value(cid, key, side)
    return None if v is None else _lv_r2(v["value"])


def level_status(cid, key, side=None):
    """"s" surveyed / "i" interpolated / "a" assumed / "c" calculated; internal tracking only, never printed"""
    v = _lv_value(cid, key, side)
    return None if v is None else v.get("status")


def level_public_source(cid, key, side=None):
    """the source to print, only when it is publicly available (e.g. the SYGM 2019 report); else None. Internal
    sources (the survey, scripts, decisions, "calculated", "assumed", ...) are never returned (Aras 29 Oct)"""
    v = _lv_value(cid, key, side)
    return None if v is None else (v.get("public") or None)


def _lv_ends_row(cid):
    """the row holding the cut line: a bare S5/S6 id takes its first crossing (all crossings share the line)"""
    try:
        return level_cut(cid)
    except KeyError:
        many = _lv_cut_rows(cid)
        if not many:
            raise
        return many[0]


LV_ENDS_OVERRIDE = {}     # round 4 (S4, N4 b): {cut: ((x1, y1), (x2, y2))} a script that draws a cut on another line
                          # than the table's (site board: S5 across the stream at one crossing) sets it each run;
                          # empty in every other script, so nothing changes there


def level_ends(cid):
    """((x1, y1), (x2, y2)): the cut's two ends in survey m, unprimed end first (LV_ENDS_OVERRIDE first)"""
    r_ = _lv_ends_row(cid)
    ov = LV_ENDS_OVERRIDE.get(r_.get("cut") or cid) or LV_ENDS_OVERRIDE.get(cid)
    if ov:
        return (float(ov[0][0]), float(ov[0][1])), (float(ov[1][0]), float(ov[1][1]))
    (a, b) = r_["ends"]["value"]
    return (float(a[0]), float(a[1])), (float(b[0]), float(b[1]))


def level_end_labels(cid):
    """(label1, label2) of the ends, e.g. ("S1", "S1'"); ("SW", "NE") on the W cuts"""
    a, b = _lv_ends_row(cid)["ends"]["labels"]
    return a, b


def level_depth(cid, side):
    """bank (or wall) top minus bed on side "NE"/"SW" (m, 2 decimals); None where the bank has no crest"""
    top, bed = level(cid, "top", side), level(cid, "bed")
    return None if top is None or bed is None else round(top - bed, 2)


def level_flood_depth(cid, which):
    """flood level minus bed (m, 2 decimals); which = "q100" or "q500" (100 / 500 and "Q100" also accepted)"""
    k = str(which).lower()
    k = k if k.startswith("q") else "q" + k
    if k not in ("q100", "q500"):
        raise KeyError("level flood must be q100 or q500, not %r" % (which,))
    q, bed = level(cid, k), level(cid, "bed")
    return None if q is None or bed is None else round(q - bed, 2)


# ---- cut registry (H-B 30 Oct 2026, M8): one entry per LEVELS row; every section on every page reads its levels here,
# never types them. Printed name = the row id (W1, never F1: PLAN T1).
def level_name(cid):
    """the one printed name of a cut: the row id ("F1" -> "W1", "F3" -> "S4")"""
    return level_cut(cid)["id"]


def level_avg_flow(cid):
    """water level at the mean yearly flow (m a.s.l., 2 decimals): the level a section draws its water at (G8)"""
    return level(cid, "avg_flow")


def level_month_depth(cid, month):
    """(round 3, A2, DATA-1) the mean water depth above the bed (m) in month 1-12 at a cut with a depth_month row (S4):
    the higher of the two gauge routes (Kömürcü, Ilıca), as the water board's DEPTH rule; None without the row"""
    v = _lv_value(cid, "depth_month")
    if v is None:
        return None
    d = v["value"]
    m = (int(month) - 1) % 12
    return max(float(d["komurcu"][m]), float(d["ilica"][m]))


def level_season_depth(cid, months):
    """the mean of level_month_depth over months (1-12, e.g. (12, 1, 2) for winter); None without the row"""
    ds = [level_month_depth(cid, m) for m in months]
    if not ds or any(d is None for d in ds):
        return None
    return sum(ds) / float(len(ds))


def level_registry(cid):
    """the registry entry of a cut: dict(id, name, location, chainage_m, walled, bed, avg_flow, avg_flow_depth, q100,
    q500, walls={NE: (type, top), SW: (type, top)}, bed_width_cm, pages (booklet), aliases); levels m a.s.l."""
    r = level_cut(cid)
    i = r["id"]
    return dict(id=i, name=r.get("name"), location=r.get("location"), chainage_m=level(i, "chainage_m"),
                walled=bool(r.get("walled")), bed=level(i, "bed"), avg_flow=level(i, "avg_flow"),
                avg_flow_depth=level(i, "avg_flow_depth"), q100=level(i, "q100"), q500=level(i, "q500"),
                walls=dict((s_, ((r.get(s_) or {}).get("type"), level(i, "top", s_))) for s_ in ("NE", "SW")),
                bed_width_cm=level(i, "bed_width_cm"), pages=list(r.get("booklet_pages") or []),
                aliases=list(r.get("aliases") or []))


def level_registry_all(page=None):
    """every registry entry in table order; page = a booklet page number ("12") keeps only the cuts drawn there"""
    out = [level_registry(i) for i in level_ids()]
    return [e for e in out if page is None or str(page) in e["pages"]]
# v6 (round 3, G16 / D9): every printed bridge or place name from the one names table (bridge_name, place_name)
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
# 1 Nov (v6.2): the spine, its bank vote and the stops live in common/city_spine.py (the masterplan builds them too)
# city_spine.py (1 Nov 2026, Aras 07:48: "move that part of the city link code into the masterplans script"): the
# streamside spine, its bank vote and its stops, shared by bergama_city_link and bergama_masterplan, so the masterplan
# builds the spine itself (spine_spec) and no longer needs city_link_results.json; city link then runs once, after it.
# Needs bridge_name, landmark_name (common/names.py) and bg_cache (common/bergama_paths.py) included before it.
# Round 4 (S1, 1 Nov 2026, G-R4-11): every printed place name comes from the names table (Kızıl Avlu, never "Red Hall";
# Ulucami; bridges by name, never a K-code); the K-codes below stay internal keys and comments only.

# ------------------------------------------------------------------ the spine and the function sites (survey m)
# Anchors are surveyed points (h01 §0 and §5, source s62): K4 Ulucami Önü (29846,32278), K3 Tabak Köprüsü (30037,32122),
# P04 Red Hall south rotunda "Müze" (30238.7,31931.2), K5 Üç Kemer (30294,31792). side_ref = a surveyed point on the bank
# the piece runs on (P05 Ulu Cami; P02 Red Hall); offset_m = distance from the stream centreline (schematic, for the
# movement network only; Thread 5 draws the real edge). Piece B runs over the covered reach (offset 0), where the main
# spine (Kınık Caddesi) crosses the stream.
SPINE = [
    dict(id="A", name=landmark_name("ulucami") + u" to " + bridge_name("K3") + u" bank walk", frm=[29846.0, 32278.0], to=[30037.0, 32122.0], side_ref=[29844.2, 32313.3], offset_m=15.0, side="auto", catch_m=250.0),
    dict(id="B", name="Junction over the covered reach", frm=[30037.0, 32122.0], to=[30238.7, 31931.2], side_ref=None, offset_m=0.0),
    dict(id="C", name=landmark_name("kizil_avlu") + u" to " + bridge_name("K5") + u" bank walk", frm=[30238.7, 31931.2], to=[30294.0, 31792.0], side_ref=[30245.0, 31962.0], offset_m=15.0, side="auto", catch_m=250.0),
]
# the main spine (Bankalar Caddesi + Kınık Caddesi, OSM "secondary" ways of the same extract, converted with the h01 §0
# formula, +-10-30 m), from Bankalar's south end east past the junction; the masterplan (v11) draws it (Thread 5)
MAIN_SPINE = [[29756.1, 31655.4], [29777.7, 31668.2], [29793.7, 31679.4], [29806.4, 31691.6], [29813.1, 31702.3], [29819.3, 31712.8], [29828.2, 31728.8], [29852.9, 31760.3], [29869.5, 31780.3], [29880.9, 31808.0], [29885.0, 31824.8], [29896.2, 31862.5], [29901.7, 31880.7], [29908.9, 31905.2], [29916.1, 31928.8], [29919.2, 31939.1], [29929.8, 31960.8], [29944.8, 31984.6], [29951.9, 31990.3], [29956.3, 31993.2], [29992.8, 32017.4], [29995.4, 32019.8], [29998.6, 32022.6], [30005.0, 32029.4], [30032.5, 32038.3], [30084.6, 32056.0], [30089.7, 32057.7], [30092.6, 32056.5], [30096.2, 32055.0], [30138.7, 32039.0], [30153.1, 32036.3], [30235.7, 32021.9], [30245.0, 32020.1], [30269.2, 32015.6], [30274.2, 32014.5], [30278.7, 32012.8], [30281.9, 32010.3], [30285.0, 32007.1], [30308.8, 31981.0], [30310.4, 31979.3], [30317.5, 31972.1], [30331.6, 31957.6], [30373.7, 31924.2], [30399.9, 31903.0], [30432.4, 31879.5], [30499.5, 31831.0], [30545.8, 31800.5], [30562.8, 31796.3], [30574.8, 31795.5], [30598.1, 31797.7], [30626.3, 31799.4], [30663.0, 31801.6], [30682.2, 31803.0], [30709.6, 31804.9], [30718.5, 31805.5], [30741.5, 31803.1], [30767.5, 31791.6], [30786.2, 31779.9], [30813.0, 31760.8], [30824.8, 31752.4], [30889.1, 31700.8], [30978.8, 31622.0], [30993.4, 31611.0], [31007.0, 31604.5], [31023.2, 31601.7]]

# side="auto": the bank is picked by the data (Aras 24 Oct 09:08: where more people live and modern buildings
# concentrate). Per bank, within catch_m of the stream along the piece: people = floors of homes (a proxy; footprints
# not weighted), modern = buildings of 3+ floors. More of both wins; on a split, modern decides when people differ by
# under 10 %, else people. The site board v34 recomputes it live from its buildings (survey floors + inferred) and
# writes the vote to city_link_movement.json, which wins over the built-in vote below.
# Built-in vote: survey floor labels YAZI_KAT_ADEDI (2,894 labels, course DXF of 17 Oct), the same floors as the board's
# density drawings; stream = OSM Selinos line; chainage and bank on the K4-K3-K5 chord (calculated, about ±30 m).
BANK_VOTE = {
    "A": dict(NE=dict(buildings=327, people_floors=425, modern_3plus=3), SW=dict(buildings=326, people_floors=436, modern_3plus=16)),
    "B": dict(NE=dict(buildings=403, people_floors=592, modern_3plus=4), SW=dict(buildings=263, people_floors=437, modern_3plus=31)),
    "C": dict(NE=dict(buildings=56, people_floors=73, modern_3plus=1), SW=dict(buildings=187, people_floors=245, modern_3plus=4)),
}

def bank_of(v):
    """the vote rule: (bank, why)"""
    ne, sw = v["NE"], v["SW"]
    if ne["people_floors"] >= sw["people_floors"] and ne["modern_3plus"] >= sw["modern_3plus"]:
        return "NE", "more people and more modern buildings"
    if sw["people_floors"] >= ne["people_floors"] and sw["modern_3plus"] >= ne["modern_3plus"]:
        return "SW", "more people and more modern buildings"
    if abs(ne["people_floors"] - sw["people_floors"]) < 0.10 * max(ne["people_floors"], sw["people_floors"], 1):
        return ("NE" if ne["modern_3plus"] > sw["modern_3plus"] else "SW"), "people within 10 %, more modern buildings"
    return ("NE" if ne["people_floors"] > sw["people_floors"] else "SW"), "more people (banks split on modern buildings)"

SRC_WET = "Days wet: research/rain_river_levels/README.md §3 (mean of water years 2016-2021)"
# who: L locals, T tourists, S students; grows: W water, E stream edge, A agriculture, H heritage
FUNCS = [
    dict(n=1, name="Bank bazaar", where=landmark_name("tabaklar_hamami"), ch=522, bank="NE", xy=[29890.4, 32243.6], who="LT", grows="HE",
         icon="stall", kw=(u"Ottoman bazaar on this bank: " + landmark_name("pabuccular_arastasi"), "stalls bring it back"), src="h02 s32"),
    dict(n=2, name="Parchment and leather workshops", where=u"old tanneries by " + bridge_name("K3"), ch=737, bank="both", xy=[30062.0, 32106.0], who="TSL", grows="H",
         icon="hide", kw=("tanning named the stream · last master died 2026", "teach and sell the craft"), src="h02 s44 s45"),
    dict(n=3, name="Junction square", where=landmark_name("kinik_caddesi") + u" over the covered stream", ch=781, bank="over", xy=[30058.0, 32047.0], who="LTS", grows="WEH",
         icon="slot", kw=("the one place the main road meets the stream", "a slot: view down to the water strip"), src=None),
    dict(n=4, name=landmark_name("kizil_avlu") + u" water terrace", where=landmark_name("kizil_avlu") + u", Roman tunnels' outlet", ch=962, bank="NE", xy=[30238.7, 31931.2], who="TL", grows="HW",
         icon="arch", kw=(landmark_name("kizil_avlu") + u" reopens: target 2026", "its visitors step out onto the stream"), src="h02 s41"),
    dict(n=5, name="Producers' market", where=bridge_name("K5") + ", Wednesdays", ch=1126, bank="spine", xy=[30294.0, 31792.0], who="LT", grows="A",
         icon="olive", kw=("food from fields on our stored water · olive oil", "Wednesdays · town producers' market: Saturdays"), src="h02 s25"),
    dict(n=6, name="Study terraces", where=u"Spine bank between " + bridge_name("K4") + u" and " + bridge_name("K3"), ch=620, bank="spine", xy=[29941.0, 32200.0], who="SL", grows="EW",
         icon="bench", kw=("shaded seats by the water strip", "for students · out of the street noise"), src=None),
    dict(n=7, name="Clean-water classroom", where="Reed basins, upstream entry", ch=200, bank="bed", xy=None, stage="entry", who="SL", grows="W",
         icon="reed", kw=("the cleaning basins as a lesson", "how the stream works"), src=None),
]
EVENTS = dict(n=8, name="Summer bed events", where="Dry bed beside the 4 m water strip", who="LT", grows="WE",
              icon="calendar", kw=("open-air events · Jul-Sep", "bed 3 cm or less · cleared by October"), src=SRC_WET)
# v1.6: kw = 2 keyword lines (were one "why" sentence); src = the source number in the page key; icon = the stop's pictogram

# the site board's own vote (selinus_board v34+, city_link_movement.json; it runs before both scripts)
SPINE_MV_FILES = [os.path.join(bg_cache("selinus_board"), "city_link_movement.json"),
                  os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "output", "selinus_board",
                               "city_link_movement.json")]


def spine_votes(mv, mv_src):
    """(votes, vote_src, sides) of the spine pieces: the site board's vote (mv = city_link_movement.json) wins over
    the built-in BANK_VOTE; sides = bank per piece by bank_of ("over" for pieces without side="auto")."""
    votes = dict((k, dict(v)) for k, v in BANK_VOTE.items())
    vote_src = "survey floor labels (built in, 24 Oct)"
    for v in (mv or {}).get("bank_votes") or []:
        if v.get("id") in votes:
            votes[v["id"]] = dict(NE=v["NE"], SW=v["SW"])
            vote_src = "site board buildings (" + mv_src + ")"
    sides = dict((pc["id"], bank_of(votes[pc["id"]])[0] if pc.get("side") == "auto" else "over") for pc in SPINE)
    return votes, vote_src, sides


def spine_spec():
    """(spec, source) for the masterplan: the same keys city_link_results.json had (spine, spine_banks, functions,
    main_spine), built here from the site board's vote of this run (or the built-in vote)."""
    mv, mv_src = None, ""
    for p in SPINE_MV_FILES:
        try:
            with open(p, "r", encoding="utf-8") as fh:
                mv = json.load(fh)
            mv_src = "site board movement of " + time.strftime("%d %b %H:%M", time.localtime(os.path.getmtime(p)))
            break
        except Exception:
            continue
    votes, vote_src, sides = spine_votes(mv, mv_src)
    spec = dict(spine=SPINE, spine_banks=sides, bank_votes=votes, main_spine=MAIN_SPINE,
                functions=[dict((k, f.get(k)) for k in ("n", "name", "where", "xy", "stage", "who", "grows", "ch", "bank"))
                           for f in FUNCS + [EVENTS]])
    return spec, u"spine and stops built into this script; banks from " + vote_src


def cl_flood():
    """v4.1: ("a-b m" Q100 over the bed, "a-b m" Q500 over the bed, "over the banks only at S4" or similar) on the
    level table's cuts S1-S8 (every crossing of S5/S6), heights in m with 2 decimals"""
    ids = [c for c in level_ids() if c.startswith("S")]
    def rng(which):
        v = [d for d in (level_flood_depth(c, which) for c in ids) if d is not None]
        return u"{:.2f}-{:.2f} m".format(min(v), max(v)) if v else u""
    over = []
    for c in ids:
        q, tops = level(c, "q100"), [level(c, "top", s) for s in ("NE", "SW")]
        if q is not None and any(t is not None and q > t for t in tops) and c.split("-")[0] not in over:
            over.append(c.split("-")[0])
    return rng("q100"), rng("q500"), (u"over the banks only at " + u", ".join(over)) if over else \
        u"inside the banks on every cut"


CL_Q100, CL_Q500, CL_OVER = cl_flood()

# chainage along the stream from the frame's north-west end: bridges from h02 card (s62): K4 467, K3 709, K5 1,126,
# K6 1,767 m; other places projected onto the K4-K3-K5-K6 chord here (calculated, about ±30 m)
CH = dict(K4=467, K3=709, K5=1126, K6=1767, cross=781, cov0=709, cov1=949)
# v1.6: source texts printed once in each page's numbered key (cite() gives their [n])
SRC_FLOOD = ("Floods: DSİ Q100/Q500; depth by Manning on the surveyed cross-sections, "
             "research/rain_river_levels/README.md v1.1 correction of 24 Oct (supersedes §3 levels)")
SRC_RULES = ("Taşkın ve Rüsubat Kontrolü Yönetmeliği Art. 17(1), 4(1)(n), 6(2); Planlı Alanlar İmar Yönetmeliği "
             "Art. 5(10)")                        # v4 (D13): the public regulations only
SRC_SHOPS = ("OpenStreetMap contributors, extract of 28 Jul 2026: shop=* and café, restaurant, fast food, bar, pub, "
             "ice cream")                          # v4 (D13): the public data only
SRC_CH = "Chainage from the frame's NW end; bridges h02 card (s62); covered reach K3 to the end of the survey gap (h02 E01)"
SRC_HIST = "History: h01, h02 (sources s13 s28 s32 s36 s40 s42 s43 s59 s110)"
SRC_WHO = "Who comes: library/research/city_link_2026-10-24/city_link_research_v1.md §0"   # v2.1: no "no data" row left
SRC_STRIP = ("Chainage along the stream, to scale (bridges s62; other places from h01 §5 survey coordinates, calculated, "
             "±30 m)")
SRC_TABAK = ("h02 calls Tabaklar Hamamı 'opposite Ulucami on the right bank' (s32), but both survey points lie on the "
             "north-east bank [U]")
# v1.9: the page 1 main spine plan
SRC_MAIN = "OpenStreetMap contributors, extract of 28 Jul 2026: streets, the Selinos stream (covered pieces), bus stops"
SRC_STREAM = SRC_MAIN                    # v4 (D13): one public source line for the OSM layers

# ------------------------------------------------------------------ computed here from OSM (extract of 28 Jul 2026)
# shops = OSM shop=* or amenity cafe/restaurant/fast_food/bar/pub/ice_cream (points and buildings); stream = the OSM
# Selinos lines between the frame's NW end and K6, covered pieces = tunnel/culvert tags; chainage as CH above
SHOPS_PER_100M = [(300, 2), (400, 3), (500, 1), (600, 2), (700, 17), (800, 14), (900, 6), (1000, 3), (1100, 2),
                  (1200, 0), (1300, 0), (1400, 1), (1500, 5), (1600, 1)]           # shops within 60 m of the stream
BANDS = ["0-30", "30-60", "60-120", "120-250", "250-500"]                          # m from the stream
OPEN_BAND = [(30, 9), (168, 27), (401, 37), (689, 25), (769, 27)]                 # (buildings, shops) by the open stream
COVERED_BAND = [(24, 15), (11, 6), (30, 18), (85, 23), (135, 6)]                  # ... by the covered pieces
SRC_BANK = "PR1 board p.2 (v18 bank analysis)"
SRC_BED = ("Bed depth: the site board's channel profile (survey bank crests; in the walled town reach the walls, "
           "5.0 m above the bed, site photos 1 Oct 2026)")      # v3: bank-depth research REPORT §4.1-4.2, §5
REASONS = [  # v1.6 tiles: (pictogram, keyword heading, big figure, keyword lines, source in the key)
    ("road", "MAIN ROAD MEETS THE STREAM", "1 crossing", (landmark_name("bankalar_caddesi") + u" - " + landmark_name("kinik_caddesi"), "only where the stream runs covered"), "OSM, calculated"),
    # v3 (MIRAQUA 28 Oct, G13): lengths on this page in m (a 1:10,000 map page): "1.7 km" -> "1,700 m", same value
    ("front", "BUILDINGS WITHIN 30 M", "30 buildings", ("on 1,700 m of open stream", "almost no frontage for a shop"), "OSM, calculated"),
    ("bank", "BANK DISCONNECTED", "68 %", ("12 % enclosed by building backs", "2 % accessible"), SRC_BANK),
    # v1.8 (booklet/research/FIGURE_CONFLICTS.md §1): the typed "1.1-6.7 m" (an old 9-10 Oct board run) is gone; the
    # site board v40 writes it live (bed_below_banks_min_m/max_m): read in bed_depth(); no figure when it has not run.
    # v3 (MIRAQUA 28 Oct, bank-depth research REPORT §4.2): it follows the board's bank crests (v50: the crest of the
    # bank, the walled town reach at the walls' 5.0 m above the bed, Aras 28 Oct 14:12) through the same two keys
    ("deep", "BED BELOW THE BANKS", "", ("walls", "no way down"), SRC_BED),
    # v1.6 fix (VISUAL_AUDIT accuracy 1): was "0.4-1.4 m / Q500 rises over the banks; Q100 tops every bank too" (withdrawn);
    # now README v1.1 line 49: "on the surveyed sections Q100 2.0-3.0 m and Q500 2.3-3.3 m, flat end 1.4 / 1.5 m,
    # overtopping only at K4 and S4". v3 (MIRAQUA 28 Oct, bank-depth research REPORT §4.2 + §5, Aras 14:12: the survey
    # is the inferior source): K4's low bank is the survey's, before the DSİ walls; the depths stay as they are
    ("flood", "Q100 OVER THE BED", CL_Q100, (u"Q500 " + CL_Q500, CL_OVER,    # v4.1: from the level table
                                             bridge_name("K4") + u" before the DSİ walls (survey)"), SRC_FLOOD),
    ("sewage", "SEPTIC SEWAGE IN THE STREAM", "until 2024", ("odour", "flies"), "İZSU sewer, s59; E13"),
    ("arch", landmark_name("kizil_avlu").replace(u"i", u"İ").upper() + u" OVER THE STREAM", "AD 117-138", ("Ottoman bazaar still met it", "at Tabaklar Hamamı"), "h02 s13 s28; s32"),
]
WHO = [  # v1.6 bars: (pictogram, keyword heading, big figure, low, high, keyword lines, source); None = no data.
    # Research: library/research/city_link_2026-10-24/city_link_research_v1.md
    ("visitor", "VISITS · PERGAMON SITES 2023", "433,000", 433000, 433000, ("Minister: about 480,000", "mostly day trips"), "AA; research §0 Q2 [U]"),
    ("resident", "RESIDENTS · 7 MAHALLES 2025", "11,002", 11002, 11002, ("by the stream", "district 107,549"), "TÜİK ADNKS via republishers; §0 Q3"),
    # v3 (MIRAQUA 28 Oct, G13): distances in m on this page, as its map ("3.5-3.7 km" = "3,500-3,700 m")
    ("student", "STUDENTS · EGE UNIV. MYO", "1,425", 1425, 1425, ("2024/25", "campus 3,500-3,700 m away"), "Ege MYO report 2025; §0 Q1"),
    ("student", "STUDENTS · DEÜ BERGAMA MYO", "400-500", 400, 500, ("2025", "campus 1,500-1,700 m away"), "press 01.08.2025; §0 Q1"),
    ("bed", "KYK STUDENT DORMITORY", "750 beds", 750, 750, ("on the Ege campus", "Efeler Cad. 7"), "two sources; §0 Q1 [V]"),
    # v2.1 (Prompt 8, rule: no "no data" rows): "PEDESTRIANS ON THE STREETS" gone: no count exists (§0 Q8), no estimate
]
FLOOD = [  # v1.6: (level, keyword lines on how often wet, [(rule pictogram, rule keywords)], source of the wet lines)
    ("Bed", ("dry or 3 cm Jul-Sep", "0.1 m on about 100 days"),
     [("nofix", "nothing fixed narrows the bed (17/1)"), ("calendar", "clearable stalls and events, Jul-Sep only")], SRC_WET),
    ("Terrace +1.00 m", ("0 days in an average year", "floods only"),     # v3 (G13): a level, 2 decimals
     [("stamp", "low stone seats only with DSİ approval"), ("stall", "stalls taken in on a warning")], SRC_WET),
    # v1.6 fix (VISUAL_AUDIT accuracy 1): was "Q100 2.6-3.0 m and Q500 2.9-3.5 m over the bed" (withdrawn); README v1.1
    # line 49 and its table (Q100 2.05-2.99 m, Q500 2.33-3.30 m on the five surveyed cuts; flat end 1.38 / 1.54 m).
    # v3 (MIRAQUA 28 Oct, bank-depth research REPORT §4.2 + §5): as page 1's flood tile, K4's bank is the survey's,
    # before the DSİ walls (one claim on both pages); the depths stay as they are
    ("Bank top", (u"Q100 {} · Q500 {} over the bed".format(CL_Q100, CL_Q500), CL_OVER,   # v4.1: level table
                  bridge_name("K4") + u" before the DSİ walls (survey)"),   # v6 (G16): real name
     [("road", "service road kept clear"),   # v9 (G-R5-4.6): no width ("6 m" gone)
       ("crest", "occupied floors at DSİ crest + 1.50 m (5/10)")], SRC_FLOOD),
]
# ------------------------------------------------------------------ colours (palette v1.4 core roles)
C = dict(ground="E2E0D4", paper="EFEDE6", faint="D8D5CC", structure="B0AC9C", ink2="847E75", ink="4A3F35",
         green_deep="495338", green_mid="727A4E", green_light="8C9969", water_deep="5D7F8D", water="91ADB4",
         water_light="C1D3DB", accent="8B3A3F", accent_deep="633131", white="FFFFFF",
         field="BDB57A", orchard="70754C", tree="89986A", grass="C9CDB0", shrub="A2B6B5", olive="5C7A86")

def rgb(h): return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
# ---- MIRAQUA round 28 Oct 2026: ONE set of shared definitions for every script (revision_2026-10-28/PLAN.md) ----
# Colours chosen in OKLCH next to palette v1.4 (palette/README.md) and checked by CIEDE2000 (dE00) against each other
# and the base map colours (method and numbers: PLAN.md "Shared definitions"). Same meaning = same colour on every
# page. Hex without '#'.

# G8: the study area (layer calisma_alan, two parts, worked as ONE area) on every map, one line style, one name.
# The rectangle site_alan is the analysis frame (the strip map's own edge); where a figure is counted over it, it is
# named R28_FRAME_NAME.
R28_STUDY_NAME = u"Study area · çalışma alanı"
R28_FRAME_NAME = u"Analysis frame"
# round 4 (S2, G-R4-4, U18/U19): violet long-dash-dot, its own hue, never ink / grey / a road colour; the same values
# as basemap.py BM_STUDY_LINE (one style everywhere; map_layers draws it in its own layer above the project fills)
R28_STUDY_LINE = dict(colour="6A4C93", width_mm=0.35, dash_mm=(3.0, 0.8, 0.6, 0.8))   # long dash-dot, print mm

# G7: one strip per map; standard scales only (SCRIPT_STANDARD §8). Round 4 (S2, D11): section_frame.py SF_SCALES is
# the one list; this copy is read only where section_frame is not included (r28_scale reads SF_SCALES first)
R28_SCALES = (200, 250, 500, 1000, 2000, 2500, 5000, 10000, 20000)


def r28_scale(length_m, avail_mm, height_m=0.0, avail_h_mm=1e9):
    """the largest standard scale (smallest denominator) at which length_m x height_m fits avail_mm x avail_h_mm"""
    sc = globals().get("SF_SCALES") or R28_SCALES
    for d in sc:
        if length_m * 1000.0 / d <= avail_mm and height_m * 1000.0 / d <= avail_h_mm:
            return d
    return sc[-1]


def r28_axis(frame):
    """frame = the four site_alan corners [A, B, C, D] (A->B the long side, A = upstream end): (A, u, v, L, W):
    unit vector u along the stream (upstream -> downstream), v across it (towards D), the side lengths in m"""
    import math as _m
    (ax, ay), (bx, by), (cx, cy) = frame[0], frame[1], frame[2]
    L = _m.hypot(bx - ax, by - ay)
    W = _m.hypot(cx - bx, cy - by)
    u = ((bx - ax) / L, (by - ay) / L)
    v = (-u[1], u[0])
    if (frame[3][0] - ax) * v[0] + (frame[3][1] - ay) * v[1] < 0:
        v = (-v[0], -v[1])
    return (ax, ay), u, v, L, W


def r28_to_strip(p, axis):
    """survey point -> (s, t) in m: s along the stream from the upstream end, t across it"""
    (ax, ay), u, v = axis[0], axis[1], axis[2]
    dx, dy = p[0] - ax, p[1] - ay
    return dx * u[0] + dy * u[1], dx * v[0] + dy * v[1]


# P06.2 / P22.1 "where we can build": three hatches, apart from the base map and from each other (dE00 >= 19.6 to the
# base colours, >= 24.4 between them)
R28_BUILD_HATCH = (("open", u"Vacant ground", "BD5833", 45.0),         # (key, legend name, line colour, hatch angle);
                   # 28 Oct: "Vacant ground", not "Open ground" (that is the masterplan's open ground, P21.2)
                   ("parking", u"Parking & yards", "6C5594", -45.0),
                   ("loose", u"Loose ground", "BF8F34", 0.0))

# P21.1 open ground: every category apart (dE00 >= 11.4)
R28_OPEN = dict(open_fill="EDDDB1", noplant_hatch="7E522C", stream="91ADB4", building="6B645B", road="CFCCC5",
                bridge="4A3F35")

# P09.1 / P10.1 reach on foot from a hub, three classes (thin streets or light rings, never a glow over the plan)
R28_REACH = ((100, u"0-100 m", "216253"), (400, u"100-400 m", "569484"), (800, u"400-800 m", "A0C8BC"))

# P23.1 / P23.2 masterplan marker groups (number circles and list numbers)
R28_MARKERS = (("roads", u"Roads: kept, calmed, pedestrian, shared", "6E675F"),
               ("hubs", u"Hubs and transit", "A25E2B"),
               ("water", u"Water and ecology", "327382"),
               ("crossings", u"Crossings", "695A85"),
               ("heritage", u"Heritage and views", "8B3A3F"))

# P24 + S1 programme zones (fade-out fields): ONE set for the 1:1,000 plans and the senses page, same colours
R28_ZONES = (("reed", u"Reed basins · cleaning", "58B292"),
             ("terraces", u"Terraces · holding rain", "ADA052"),
             ("hub", u"Hub square", "D4896E"),
             ("subhub", u"Sub-hub in the bed", "6AA4DA"),
             ("demeter", u"Demeter's Garden", "AD8ED1"),
             ("forest", u"Forest corridor", "83AD6D"),
             ("wetland", u"Widened stream · wetland", "41B0BC"),
             ("cafe", u"Café", "D084A1"))
R28_ZONE = dict((k, (lab, hx)) for k, lab, hx in R28_ZONES)
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
# ---- Shared basemap (revision 29 Oct 2026, brief 02 §1, WO-T2a-1) -------------------------------------------------
# ONE base for every map of the booklet (site board, water board, city link, masterplan, agriculture): the same
# stream, streets, buildings, green, tree cover, fields and contours, switched on and off per page by its MODE, with a
# per-drawing override (D5: Zones a, Feeling b stream only, Sound b stream + main roads, Smell b stream only ...).
#
# WHERE THE DATA COMES FROM (decided 29 Oct, T2a): not from the open Rhino file. The site board already builds the
# whole site model once (survey of Bergama_Altlik.3dm + OpenStreetMap + WorldCover, cached); it calls
# basemap_export(S) once a run and writes Downloads/Bergama/cached/basemap/basemap.json. Every other script reads that
# file with basemap_load(). Inside the analysis frame (site_alan) the layers are the site board's own (survey quality,
# exactly as p.06 draws them); between the frame and the wider EXTENT they are OpenStreetMap's (Data/bergama_osm.osm),
# so p.21 reaches the Asklepion, the Akropol, the cable car and the museum, and p.16's frames can widen. Scripts that
# run before the site board in the chain (zone base, masterplan, water balance) read the file of the last run; before
# the very first site board run there is no file: basemap_load() returns None, logs it, and every draw call draws
# nothing (the caller's own drawing goes on).
#
# GEOMETRY: survey metres everywhere. Line widths and marker sizes are PRINT mm on the booklet page, so a call needs
# the drawing's scale denominator only where a size in mm becomes metres (cut-line markers). Colours: hex 'RRGGBB'.
# A draw call returns ITEMS, bottom first; the caller turns them into its own page calls (basemap_draw does that
# through two or three small functions the caller gives). Items:
#   ("fill", rings, hex, alpha, nonzero)        rings = [[(x, y), ...], ...] (outlines and their holes)
#   ("line", pts, hex, width_mm, dash_mm, alpha) dash_mm = None or [on, off, ...] in print mm
#   ("text", s, (x, y), size_mm, hex, bold, align)   align as the scripts' text calls ("MC" = middle centre)
# M3 (revision 30 Oct 2026, H-A): the 29 Oct modes and switches are kept as they were; added the layers study_area
# (calisma_alan, ONE outline reused on every map, R28_STUDY_LINE), names (place names) and the building styles "plan" /
# "plan_faint" (M11: block outlines + roof reading, no stripes), the modes "base" (the faint base of a map page) and
# "key" (key maps, M4), the water drawn by M5 (water_plan, when included) and keymap_items (M4). The data carries per
# building its height (h, floors) and a "blocks" layer (buildings sharing a wall merged: no fake division lines).
import os as _bm_os
import json as _bm_json
import math as _bm_math

BASEMAP_FILE = _bm_os.path.join(_bm_os.path.expanduser("~"), "Downloads", "Bergama", "cached", "basemap",
                                "basemap.json")
BASEMAP_FORMAT = 2               # round 5 (S2): 2 = buildings carry "fabric" and "annex", land cover adds grass / shrub
BASEMAP_FORMATS_READ = (1, 2)    # a format 1 file (written before round 5) still reads: key maps then draw one house
#                                  tone and log a FLAG until the site board has written format 2
BASEMAP_MARGIN = 250.0           # m: the extent reaches this far beyond the farthest REACH place
# the places the extent must hold (survey m; the heritage loop's positions, selinus_board parts/15j_r28_heritage.py)
BASEMAP_REACH = ((u"Asklepion", (29077.3, 31867.3)),          # OSM ticket building
                 (u"Akropol", (30209.0, 33177.0)),            # Trajaneum, OSM way 1410335587
                 (u"Teleferik", (30720.4, 32370.1)),          # valley station, OSM node 2295928011
                 (u"Bergama Müzesi", (29560.0, 31358.0)))

# tones: the p.06 stream edge plan's (selinus_board MPL, R28E_*) so the detailed mode is p.06's base
BM_COL = dict(bld="A7A299", bld_osm_edge="736A62", her="E4CAC9", her_edge="AF7474", water="91ADB4",
              water_edge="5D7F8D", tree="C4CCB5", park="DFEBC0", grass="DFEBC0", field="C6C08D", road="CFCCC5",
              road_edge="847E75", ink="2C2219", contour="BDB7B0", cut="2C2219")
BM_FAINT = dict(bld="D3D0CB", bld_veryfaint="E9E7E3", road="E2E0DB", road_line="B9B4AC")
# round 4 (S2, G-R4-4, PLAN §4.3): the MUTED base under every map page: light houses with a closed block outline,
# light streets with their edges, every outline after every fill (CHK-3 §1.5-1.6); heritage a pale rose.
BM_MUTED = dict(bld="EDEBE6", bld_edge="C9C5BC", her="F1E6E5", her_edge="CDAAAA", road="F4F2EE", road_edge="CFCBC2",
                name="9A948A", lw=0.12)
# round 5 (S2, G-R5-3, D3, U69 "just draw it like page 2"): the key-map look = the p02 map (site board plan 01) at
# small scale. BM_FABRIC is the site board's FABRIC_PLAN (selinus_board/parts/14_tsec_wind_arrows.py v40) moved to
# common as hex (the site board keeps its own name for it until its round 5 pass reads this table). BM_KEY: the p02
# ground tones (site board parts/01__gh_inputs.py CAT, GREEN_SUB, TREE_COLS, PAPER, BLUE_D; parts/17_board_fits.py
# LC_CLASSES), lightened toward the paper by "light" (greens) and "fabric_light" (houses, = p02 P02_IN_LIGHT 0.40)
# so the red cut symbols lead; design values.
BM_FABRIC = {"monument": "AF7474", "sacred": "8B3A3F", "traditional": "4A3F35", "block": "7A6E60",
             "regular": "BCB794", "selfbuilt": "DCD5C2", "large": "FAF8F1", "construction": "E6E0C8",
             "unsurveyed": "D8D5CC"}   # round 9 (S3): houses beyond the survey (OpenStreetMap), = HUE CTX r4
BM_KEY = dict(paper="F1EDDF", grass="ABB287", shrub=("8F9A68", "F1EDDF", 0.3), trees="74804F", farmland="BDB57A",
              orchard=("98A271", "4A3F35", 0.12), park="8F9A68", wood="74804F", agri="BDB57A", water="7FA4B3",
              water_edge="5E8494", road="FAF8F1", road_line="DCD5C2", bridge="4A3F35", light=0.35, fabric_light=0.40,
              annex=0.45, lw=0.12)


def _bm_mix(a, b, t):
    """hex a mixed t of the way toward hex b (the site board's mix on hex)"""
    return "".join("%02X" % int(round(int(a[j:j + 2], 16) + (int(b[j:j + 2], 16) - int(a[j:j + 2], 16)) * t))
                   for j in (0, 2, 4))


def bm_key_col(name, light=None):
    """round 5 (S2): a BM_KEY tone as hex ('shrub' / 'orchard' are mixes), mixed light (default BM_KEY['light'] for
    ground tones, none for paper / water / road / bridge) toward the paper"""
    v = BM_KEY[name]
    c = _bm_mix(*v) if isinstance(v, tuple) else v
    if light is None:
        light = 0.0 if name in ("paper", "water", "water_edge", "road", "road_line", "bridge") else BM_KEY["light"]
    return _bm_mix(c, BM_KEY["paper"], light) if light else c


def bm_fabric_col(b, light=None):
    """round 5 (S2): a basemap building's key-map colour by its urban fabric (format 2 "fabric"; round 9:
    "unsurveyed" when the file has none, i.e. OpenStreetMap houses beyond the frame), annexes paler (the p02 rule),
    mixed BM_KEY['fabric_light'] toward the paper"""
    c = BM_FABRIC.get(b.get("fabric") or "unsurveyed", BM_FABRIC["unsurveyed"])
    if b.get("annex"):
        c = _bm_mix(c, BM_KEY["paper"], BM_KEY["annex"])
    return _bm_mix(c, BM_KEY["paper"], BM_KEY["fabric_light"] if light is None else light)


class _BmIt(tuple):
    """round 5 (S2, G-R5-8): a basemap item that knows its map layer (.layer, a map_layers ML_LAYERS name): reads as
    the plain tuple everywhere; map_draw files a flat base list by it, so the stream is drawn above every tint"""
    pass


def _bm_tag(t, layer, ctx=None, cls=None):
    o = _BmIt(t)
    o.layer = layer
    o.ctx = ctx              # round 9 (S3): the G9-4 context letter a-j (modes "context" / "keymap"), else None
    o.cls = cls              # round 9 (S3): the item's class (fabric, land cover, street class, "name", ...)
    return o


# contours coloured to the relief (G-R4-4, U48): green tones, lighter = lower (palette 3C4733 and its 89986A tints)
BM_HEIGHT_RAMP = ("C9D6B0", "A7B68C", "89986A", "3C4733")
BM_LW = dict(contour=(0.07, 0.13), contour_topo=(0.08, 0.14), water_edge=0.18, covered=0.30, bridge=0.30,
             road_edge=0.12, osm_edge=0.08, her_edge=0.12, main=0.45, secondary=0.32, lane=0.22, path=0.10, river_osm=0.6,
             stream_osm=0.35, cut=0.35)
BM_COVERED_DASH = (1.6, 0.9)     # mm: the covered course

# the modes of 02 §1; a value per layer: False = off, True = on, "faint" / "veryfaint" = buildings or streets faint,
# a tuple of street classes ("main", "lane", "path") = only those as centrelines, "height" = contours by height
BASEMAP_MODES = {
    "detailed": dict(stream=True, streets=True, buildings=True, green=True, trees=True, fields=True, contours=True,
                     study_area=False, names=False),
    "simple": dict(stream=True, streets="faint", buildings="faint", green=False, trees=False, fields=False,
                   contours=False, study_area=False, names=False),
    "minimal": dict(stream=True, streets=("main", "lane"), buildings="veryfaint", green=False, trees=False,
                    fields=False, contours=False, study_area=False, names=False),
    "topographic": dict(stream=True, streets=False, buildings="faint", green=False, trees=False, fields=False,
                        contours="height", study_area=False, names=False),
    # M3 (30 Oct): the faint base under a map page's message (G5), and the key map's base (M4)
    "base": dict(stream=True, streets="faint", buildings="plan_faint", green=False, trees=False, fields=False,
                 contours=False, study_area=True, names=False),
    "key": dict(stream=True, streets=("main",), buildings="veryfaint", green=False, trees=False, fields=False,
                contours=False, study_area=True, names=False),
    # round 4 (S2, G-R4-4): the muted base of map_layers.ml_base; the study line is drawn by map_draw in its own
    # layer (above the project fills), so it is off here; contours are switched on by the call ("height")
    "muted": dict(stream=True, streets="muted", buildings="muted", green=False, trees=False, fields=False,
                  contours=False, study_area=False, names=False),
    # round 5 (S2, G-R5-3): the key map = the p02 look at small scale: land cover and green ground, houses by urban
    # fabric (fills only, no outlines at key-map scales), the stream blue (a flat fill: legible at 1:50,000+), light
    # street areas, bridges; the study line and names are the key map's own
    "keymap": dict(stream=True, streets="key", buildings="fabric", green=True, trees=True, fields=True,
                   contours=False, study_area=False, names=False),
    # round 9 (S3, G9-4, A1 C2): the map context, layers a-j to the window's edge (SON page2/7/9 the floor); mode
    # "keymap" now draws the same layers quieter (every street class, G9-5); the study line is map_draw's own layer
    "context": dict(stream=True, streets=True, buildings="fabric", green=True, trees=True, fields=True,
                    contours=True, study_area=False, names=True),
}
# M3 layer list -> switches: basemap_layers accepts these names too (buildings, streets, water, topography,
# study_area, names; green, trees, fields as before)
BM_LAYER_ALIAS = dict(water="stream", topography="contours")
# round 4 (S2, G-R4-4, U18/U19): ONE study-area line everywhere: violet long-dash-dot, its own hue (never ink, grey
# or a road colour); r28_style.py R28_STUDY_LINE holds the same values (either file may be included first)
BM_STUDY_LINE = dict(colour="6A4C93", width_mm=0.35, dash_mm=(3.0, 0.8, 0.6, 0.8))
BM_NAME_MM = 2.47                  # place names: the M1 label size (7 pt)
_BM_MEMO = {}
_BM_WARN = []

# ---- round 9 (S3, 11 Nov 2026; BRIEF G9-4, A1 C2, PLAN.md §spec S3): mode "context" = the map context layers a-j ----
# drawn to the window's edge in the G9-4 order land cover (e) -> terrain (i) -> buildings (d) -> streets (a) ->
# stream (f) -> bridges (g) -> names (b, c, f, g, h); the project follows (map_draw), the study line (j) is
# map_draw's own layer. Mode "keymap" draws the same layers quieter (G9-5, PLAN S4). Colours from the hue table r9
# (FAB, LC, STR, WAT, CTX families). Every item carries .layer, .ctx (the letter) and .cls (its class).
BM_CTX_LETTERS = (("a", u"streets"), ("b", u"main street names"), ("c", u"mahalle names"),
                  ("d", u"buildings by fabric"), ("e", u"land cover"), ("f", u"stream and its name"),
                  ("g", u"bridges and their names"), ("h", u"heritage and landmark names"), ("i", u"terrain"),
                  ("j", u"study area"))
BM_CTX_SRC = dict(a=u"basemap.json layers street_areas / streets_in / streets_out",
                  b=u"basemap.json layers street_names", c=u"basemap.json layers mahalle",
                  d=u"basemap.json layers buildings", e=u"basemap.json layers lc / zones",
                  f=u"basemap.json layers water / water_out / waterways_out",
                  g=u"basemap.json layers bridges / bridges_out / bridge_names",
                  h=u"names table landmarks (NAMES r9) + basemap.json layers names",
                  i=u"basemap.json layers contours / contours_out", j=u"basemap.json layers study")
BM_UNMAPPED = "F1EDDF"             # "unmapped ground" (G9-4 item 3): the p02 paper tone BM_KEY paper; design value
BM_STR_W = dict(main=0.85, secondary=0.55, lane=0.30, path=0.10)        # mm: MV_W (SB:18495); path = BM_LW path
BM_STR_W_KEY = dict(main=0.40, secondary=0.28, lane=0.14, path=0.0)     # mm, key maps (quiet); design values
BM_STR_LANE_DEN = 2500.0           # at 1:2,500 and larger the surveyed street areas show the lanes (no centreline)
BM_BLD_EDGE_MM = 0.10              # G9-4 (d): stroke <= 0.1 mm; half of it at 1:10,000 and smaller (design value)
BM_BLD_EDGE_DARK = 0.25            # "one step darker": the fill mixed 25 % toward the ink (design value)
BM_CTX_QUIET = 0.35                # key maps: land cover, streets mixed toward the paper (= BM_KEY light)
BM_PT_MM = 25.4 / 72.0
BM_CTX_PT = dict(street=5.0, mahalle=5.0, bridge=5.0, place=5.0, place_r1=6.0, stream=6.0)   # pt (4-6, floor 4)
BM_STREAM_NAME = u"SELİNOS ÇAYI"   # G9-4 (f), not on p3 (U09: stream_name=False)
BM_CTX_NAME_CATS = ("her", "sacred", "culture")    # names-table "cat" always named; "civic" only where asked
BM_CTX_WORDS = dict(unmapped=u"Unmapped ground", trees=u"Woods", orchard=u"Orchards", shrub=u"Shrubland",
                    park=u"Parks and green", grass=u"Grassland", farmland=u"Fields", area=u"Street space",
                    main=u"Main street", secondary=u"Secondary street", lane=u"Local street", path=u"Footpath",
                    stream=u"Selinos stream", bridge=u"Bridge", contour=u"Contours")


# ------------------------------------------------------------------------------------------- reading
def basemap_load(path=None, log=None):
    """the basemap data (dict) written by the site board's basemap_export, read once a run; None when the file is
    missing or of another format (a line goes to log, a list, when given)"""
    p = path or BASEMAP_FILE
    if p in _BM_MEMO:
        return _BM_MEMO[p]
    d = None
    try:
        with open(p, "r", encoding="utf-8") as fh:
            d = _bm_json.load(fh)
        if not isinstance(d, dict) or d.get("format") not in BASEMAP_FORMATS_READ:
            if log is not None:
                log.append(u"WARNING: {} is of another format: the shared basemap is left out (run the site board "
                           u"once).".format(p))
            d = None
        elif log is not None:
            log.append(u"Shared basemap: {} ({}).".format(p, d.get("source", "")))
            if d.get("format") != BASEMAP_FORMAT:
                log.append(u"FLAG basemap format {} (no urban fabric per house): key maps draw one house tone until "
                           u"the site board writes format {}.".format(d.get("format"), BASEMAP_FORMAT))
    except Exception as ex:
        if log is not None:
            log.append(u"WARNING: the shared basemap {} could not be read ({}): maps are drawn without it until the "
                       u"site board has run once.".format(p, type(ex).__name__))
    _BM_MEMO[p] = d
    return d


def basemap_frame(D=None):
    """the analysis frame (site_alan) as four survey corners, upstream end first, from the data; None without data"""
    D = D if D is not None else basemap_load()
    return [tuple(p) for p in D["frame"]] if D else None


def basemap_extent(D=None):
    """the whole basemap's rectangle as four survey corners (frame axes); None without data"""
    D = D if D is not None else basemap_load()
    return [tuple(p) for p in D["extent"]] if D else None


def basemap_layers(mode, override=None):
    """the layer switches of a mode (BASEMAP_MODES) with a drawing's own changes laid over them, e.g.
    basemap_layers("minimal", {"streets": ("main",), "buildings": False}) for D5 Sound b (stream + main roads).
    M3 (30 Oct): override may also be a LIST of layer names = only those on (the others off), each at the mode's
    own value, e.g. basemap_layers("base", ["buildings", "water", "study_area"]); "water" = stream, "topography" =
    contours. buildings: True / "faint" / "veryfaint" / "plan" / "plan_faint" (M11) / False."""
    if mode not in BASEMAP_MODES:
        raise ValueError(u"basemap mode '{}' unknown: one of {}".format(mode, ", ".join(sorted(BASEMAP_MODES))))
    lay = dict(BASEMAP_MODES[mode])
    if isinstance(override, (list, tuple, set, frozenset)):
        want = set(BM_LAYER_ALIAS.get(k, k) for k in override)
        for k in want:
            if k not in lay:
                raise ValueError(u"basemap layer '{}' unknown: one of {}".format(k, ", ".join(sorted(lay))))
        on = dict(BASEMAP_MODES["detailed"], study_area=True, names=True)
        override = dict((k, (lay[k] or on[k]) if k in want else False) for k in lay)
    for k, v in (override or {}).items():
        k = BM_LAYER_ALIAS.get(k, k)
        if k not in lay:
            raise ValueError(u"basemap layer '{}' unknown: one of {}".format(k, ", ".join(sorted(lay))))
        lay[k] = v
    return lay


def _bm_bb(P):
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    return min(xs), min(ys), max(xs), max(ys)


def _bm_hit(P, box):
    if box is None:
        return True
    b = _bm_bb(P)
    return not (b[2] < box[0] or b[0] > box[2] or b[3] < box[1] or b[1] > box[3])


def _bm_ramp(t):
    """BM_HEIGHT_RAMP at t in 0..1 (hex)"""
    t = min(1.0, max(0.0, t))
    n = len(BM_HEIGHT_RAMP) - 1
    i = min(n - 1, int(t * n))
    f = t * n - i
    a, b = BM_HEIGHT_RAMP[i], BM_HEIGHT_RAMP[i + 1]
    return "".join("%02X" % int(round(int(a[j:j + 2], 16) + (int(b[j:j + 2], 16) - int(a[j:j + 2], 16)) * f))
                   for j in (0, 2, 4))


def basemap_items(mode="detailed", override=None, box=None, D=None, split_buildings=False, scale_den=None, opts=None):
    """the basemap of a drawing as items (bottom first; see the head of this file), in survey m. mode: "detailed",
    "simple", "minimal", "topographic" (02 §1), "base", "key" (M3, 30 Oct); override: layer changes for this drawing,
    a dict or a list of the layers to show (basemap_layers); box = (x0, y0, x1, y1) survey m: only what touches it
    (the caller clips to its frame); split_buildings=True gives every building its own fill item (for a page that
    fills even-odd only; default: nonzero fills in chunks); scale_den: the drawing's scale (1:scale_den) for the
    M11 roof marks of buildings "plan" / "plan_faint" (default 1:5,000). Round 9 (S3): mode "context" = the map
    context layers a-j and "keymap" the same quieter (_bm_context_items; opts: civic, stream_name, ring,
    street_classes). [] without data."""
    D = D if D is not None else basemap_load()
    if not D:
        return []
    # the same request in one run is made once and copied (Aras 29 Oct 19:18: build once, cache, copy the layers)
    ov = sorted(override) if isinstance(override, (list, tuple, set, frozenset)) else sorted((override or {}).items())
    mk = ("items", id(D), mode, repr(ov), tuple(box) if box else None, bool(split_buildings), scale_den,
          repr(sorted((opts or {}).items())))
    if mk in _BM_MEMO:
        return list(_BM_MEMO[mk])
    _BM_MEMO[mk] = _bm_items(D, mode, override, box, split_buildings, scale_den, opts)
    return list(_BM_MEMO[mk])


def basemap_water_rings(items):
    """M3: the stream's rings (survey m) in an item list, whether drawn plain (fill items of the water colour) or by
    M5 (the "water" item): for a page that clips or measures by the water"""
    out = []
    for it in items:
        if it[0] == "water":
            out += [R for g in it[1] for R in g if len(R) >= 3]
        elif it[0] == "fill" and it[2] == BM_COL["water"]:
            out += [R for R in it[1] if len(R) >= 3]
    return out


def basemap_warnings():
    """M3: what the basemap could not draw as asked this run (e.g. the M5 water drawing failed): log lines, emptied"""
    out = list(_BM_WARN)
    del _BM_WARN[:]
    return out


def basemap_study(D=None):
    """M3: the study area (calisma_alan, two closed parts worked as one) as rings in survey m: the basemap's study
    layer, else the recorded copy a script includes (R28_STUDY_COPY, CALISMA_COPY, CL_STUDY); [] without either"""
    D = D if D is not None else basemap_load()
    st = ((D or {}).get("layers") or {}).get("study")
    if st:
        return [[tuple(p) for p in R] for R in st]
    for nm in ("R28_STUDY_COPY", "CALISMA_COPY", "CL_STUDY"):
        v = globals().get(nm)
        if v:
            return [[tuple(p) for p in R] for R in v]
    return []


def basemap_study_items(D=None, style=None):
    """M3: the study-area outline as line items (survey m), one style everywhere (R28_STUDY_LINE when included)"""
    st = style or globals().get("R28_STUDY_LINE") or BM_STUDY_LINE
    return [("line", list(R) + [R[0]], st["colour"], st["width_mm"], list(st["dash_mm"]), 1.0)
            for R in basemap_study(D) if len(R) >= 3]


def basemap_names(box=None, D=None):
    """M3: the place names [(name, (x, y))] in survey m (the extent's landmarks and named heritage buildings), for a
    page to place with M2 (lp_place) so no name collides"""
    D = D if D is not None else basemap_load()
    if not D:
        return []
    nm = (D.get("layers") or {}).get("names") or [[n, list(p)] for n, p in (D.get("reach") or BASEMAP_REACH)]
    out = []
    for n, p in nm:
        if box is None or (box[0] <= p[0] <= box[2] and box[1] <= p[1] <= box[3]):
            out.append((n, (p[0], p[1])))
    return out


def basemap_street_names(box=None, D=None, classes=("main",), min_len_m=0.0):
    """round 4 (S2, G-R4-9 U55): the street names of OpenStreetMap's `name` tags (Turkish as mapped), one per name
    at the middle of its longest run: [(name, (x, y), angle_deg, class, run_m)] in survey m, longest first; classes
    = the street classes kept ("main", "lane"); [] when the basemap file predates round 4 (run the site board)"""
    D = D if D is not None else basemap_load()
    out = []
    for n, p, a, cl, ln in ((D or {}).get("layers") or {}).get("street_names") or []:
        if cl in classes and ln >= min_len_m and (box is None or (box[0] <= p[0] <= box[2] and box[1] <= p[1] <= box[3])):
            out.append((n, (p[0], p[1]), a, cl, ln))
    out.sort(key=lambda r: -r[4])
    return out


def _bm_nk(s):
    """round 9: a name as a match key (single spaces, lower case)"""
    return u" ".join((s or u"").split()).lower()


def _bm_in(p, box):
    return box is None or (box[0] <= p[0] <= box[2] and box[1] <= p[1] <= box[3])


def basemap_places(box=None, D=None, civic=False):
    """round 9 (S3 layer h, PLAN §Q9; Aras 11 Nov 18:36 "search all the places in maps, like dont use heritage
    building use the special name"): the named places a map labels, [(name, (x, y), cat, key)] in survey m, inside
    box when given, most important first. Every names-table landmark with "at" whose "cat" is her / sacred / culture
    (or has no "cat": the round 3-8 rows); "civic" rows only when civic is True or names their kind (a tuple of OSM
    values found in the row's "src", e.g. ("school",)); then the basemap's own names (REACH and named buildings, in
    the table's spelling) not yet listed. One row per name. A place is never labelled with a class word."""
    D = D if D is not None else basemap_load()
    N = globals().get("NAMES")
    rows = (N.get("landmarks") or {}) if isinstance(N, dict) else {}
    hr = globals().get("her_rank")
    got = []
    for key, row in rows.items():
        at, cat = row.get("at"), row.get("cat")
        if at is None or not row.get("name"):
            continue
        if cat == "civic":
            if not civic:
                continue
            if civic is not True and not any((u"=%s" % v) in (row.get("src") or u"") for v in civic):
                continue
        elif cat is not None and cat not in BM_CTX_NAME_CATS:
            continue
        p = (float(at[0]), float(at[1]))
        if not _bm_in(p, box):
            continue
        r_ = hr(row["name"], 3 if cat in (None, "her") else 4) if callable(hr) else 3
        got.append((r_, row.get("km") or 99, row["name"], p, cat, key))
    got.sort(key=lambda g: (g[0], g[1], g[2]))
    out, seen = [], set()
    for _r, _k, n, p, cat, key in got:
        if _bm_nk(n) not in seen:
            seen.add(_bm_nk(n))
            out.append((n, p, cat, key))
    for n, p in basemap_names(box, D):
        if _bm_nk(n) not in seen:
            seen.add(_bm_nk(n))
            out.append((n, p, None, None))
    return out


def basemap_mahalle(box=None, D=None):
    """round 9 (S3 layer c): the mahalle (neighbourhood) names [(name, (x, y), rings)] in survey m whose label point
    lies inside box; [] when the basemap file has no "mahalle" layer (the site board writes it from round 9 on)"""
    D = D if D is not None else basemap_load()
    out = []
    for r_ in ((D or {}).get("layers") or {}).get("mahalle") or []:
        n, p = r_[0], (float(r_[1][0]), float(r_[1][1]))
        if _bm_in(p, box):
            out.append((n, p, [[tuple(q) for q in R] for R in (r_[2] if len(r_) > 2 and r_[2] else [])]))
    return out


def basemap_bridge_names(box=None, D=None):
    """round 9 (S3 layer g): the bridge names [(name, (x, y), code)] in survey m (the names table's spelling, the
    bridge's middle); [] when the basemap file has no "bridge_names" layer (the site board writes it from round 9)"""
    D = D if D is not None else basemap_load()
    out = []
    for r_ in ((D or {}).get("layers") or {}).get("bridge_names") or []:
        n, p = r_[0], (float(r_[1][0]), float(r_[1][1]))
        if _bm_in(p, box):
            out.append((n, p, r_[2] if len(r_) > 2 else None))
    return out


def _bm_stream_label(L, box):
    """round 9 (S3 layer f): where the stream's name goes: the middle of the longest bank or course run inside box
    (survey m) and its direction in degrees (-90..90), or None"""
    import math as _m
    best = None
    runs = list(L.get("water_edge") or []) + [P for _k, P in L.get("waterways_out") or []]
    for P in runs:
        cur = []
        for q in list(P) + [None]:
            if q is not None and _bm_in(q, box):
                cur.append(q)
                continue
            if len(cur) >= 2:
                ln = sum(_m.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(cur, cur[1:]))
                if best is None or ln > best[0]:
                    best = (ln, list(cur))
            cur = []
    if not best:
        return None
    half, acc = best[0] / 2.0, 0.0
    for a, b in zip(best[1], best[1][1:]):
        d = _m.hypot(b[0] - a[0], b[1] - a[1])
        if acc + d >= half and d > 0:
            t = (half - acc) / d
            ang = _m.degrees(_m.atan2(b[1] - a[1], b[0] - a[0]))
            ang = ang - 180.0 if ang > 90.0 else (ang + 180.0 if ang < -90.0 else ang)
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), ang
        acc += d
    return None


def _bm_ctx_ring(D, box, opts):
    """round 9: the window the unmapped ground fills: opts["ring"], else box, else the basemap extent"""
    if opts.get("ring"):
        return [tuple(p) for p in opts["ring"]]
    if box:
        return [(box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])]
    return [tuple(p) for p in D.get("extent") or []] or None


def _bm_context_items(D, lay, box, split_buildings, scale_den=None, quiet=False, opts=None):
    """round 9 (S3, G9-4): basemap mode "context" = the map context layers a-j, bottom first in the G9-4 draw
    order: unmapped ground and land cover (e, "base_ground") -> terrain (i, "base_contours") -> buildings by fabric
    at their true footprint, 0.1 mm outline one step darker, never merged (d, "base_fills") -> streets in hierarchy
    on top (a, "base_outlines") -> the stream (f, "water") -> decks, covered course, bridges (g, "structures") ->
    names (b main streets, c mahalle, f "SELİNOS ÇAYI", g bridges, h places; "structures", so the stream never
    covers them). quiet=True is mode "keymap" (G9-5, PLAN S4): the same layers quieter (colours toward the paper,
    thinner streets, fills without outlines, no terrain, no names: the key map writes its own). opts: civic (False /
    True / OSM values, e.g. ("school",)), stream_name (default True), ring (the window, survey m), street_classes
    (the classes whose names are written, default ("main",)). Text items carry an 8th field: the angle (deg)."""
    opts = opts or {}
    L = D["layers"]
    out = []
    den = float(scale_den or 5000.0)
    paper = BM_KEY["paper"]
    ink = hue("ANN", "ink")

    def tag(t, layer, ctx, cls):
        out.append(_bm_tag(t, layer, ctx, cls))

    def fills(groups, col, ctx, cls, layer="base_ground", nonzero=True, chunk=300, edge=None, edge_mm=None):
        cur, cur_e = [], []

        def flush():
            if cur:
                tag(("fill", list(cur), col, 1.0, nonzero), layer, ctx, cls)
                for R in cur_e:
                    tag(("line", list(R) + [R[0]], edge, edge_mm, None, 1.0), layer, ctx, cls)
            del cur[:]
            del cur_e[:]
        for g in groups:
            g = [R for R in g if len(R) >= 3]
            if not g or not _bm_hit(g[0], box):
                continue
            cur.extend(g)
            if edge:
                cur_e.extend(g)
            if split_buildings or len(cur) >= chunk:
                flush()
        flush()

    def lc_col(cls):
        c = LC_HEX[cls]
        return _bm_mix(c, paper, BM_CTX_QUIET) if quiet else c

    def st_col(cls):
        c = str_hex(cls)
        return _bm_mix(c, paper, BM_CTX_QUIET) if quiet else c

    # (e) land cover: the unmapped ground under the whole window, then the satellite classes, then the mapped zones
    lc, zones = L.get("lc") or {}, L.get("zones") or []
    if lay["green"] or lay["trees"] or lay["fields"]:
        R0 = _bm_ctx_ring(D, box, opts)
        if R0:
            tag(("fill", [R0], BM_UNMAPPED, 1.0, True), "base_ground", "e", "unmapped")
    for on, cls in ((lay["green"], "grass"), (lay["green"], "shrub"), (lay["trees"], "trees"),
                    (lay["fields"], "farmland"), (lay["fields"], "orchard")):
        if on:
            fills(lc.get(cls) or [], lc_col(cls), "e", cls)
    if lay["fields"]:
        fills([z["rings"] for z in zones if z["kind"] == "agri"], lc_col("farmland"), "e", "farmland")
    if lay["green"]:
        fills([z["rings"] for z in zones if z["kind"] == "green" and z.get("sub") == "grass"], lc_col("grass"), "e",
              "grass")
        fills([z["rings"] for z in zones if z["kind"] == "green" and z.get("sub") not in ("grass", "wood")],
              lc_col("park"), "e", "park")
    if lay["trees"]:
        fills([z["rings"] for z in zones if z["kind"] == "green" and z.get("sub") == "wood"], lc_col("trees"), "e",
              "trees")
    # (i) terrain: the survey contours inside the frame, GLO-30 contours beyond it (same style)
    if lay["contours"] and not quiet:
        for key_ in ("contours", "contours_out"):
            for major, z, P in L.get(key_) or []:
                if len(P) >= 2 and _bm_hit(P, box):
                    tag(("line", P, BM_COL["contour"], BM_LW["contour"][1 if major else 0], None, 1.0),
                        "base_contours", "i", "contour")
    # (d) buildings: true footprint (holes kept, even-odd), the fabric colour, outline one step darker
    if lay["buildings"]:
        e_mm = BM_BLD_EDGE_MM if den <= 5000.0 else 0.5 * BM_BLD_EDGE_MM
        groups = {}
        for b in L.get("buildings") or []:
            cls = b.get("fabric") or "unsurveyed"
            cls = cls if cls in FAB_RANK else "unsurveyed"
            col = fab_hex(cls)
            if b.get("annex"):
                col = _bm_mix(col, paper, BM_KEY["annex"])
            if quiet:
                col = _bm_mix(col, paper, HUE_KEY["fabric_mix"])
            groups.setdefault((FAB_RANK[cls], cls, col), []).append(b["rings"])
        for k in sorted(groups):
            fills(groups[k], k[2], "d", k[1], layer="base_fills", nonzero=False,
                  edge=None if quiet else _bm_mix(k[2], ink, BM_BLD_EDGE_DARK), edge_mm=e_mm)
    # (a) streets on top of the buildings: street space (cased), then every class as a cased centreline, main on top
    if lay["streets"]:
        sw = BM_STR_W_KEY if quiet else BM_STR_W
        case = None if quiet else STR_CASING
        only = tuple(lay["streets"]) if isinstance(lay["streets"], (tuple, list)) else None   # e.g. ("main",)
        if only is None:
            fills(L.get("street_areas") or [], bm_key_col("road") if quiet else str_hex("lane"), "a", "area",
                  layer="base_outlines", nonzero=False, edge=case, edge_mm=STR_CASING_MM)
        rank = {"path": 0, "lane": 1, "secondary": 2, "main": 3}
        runs = [(cl, P, True) for cl, P in L.get("streets_in") or []] + \
               [(cl, P, False) for cl, P in L.get("streets_out") or []]
        runs = [r_ for r_ in runs if len(r_[1]) >= 2 and _bm_hit(r_[1], box) and sw.get(r_[0], sw["lane"]) > 0 and
                (only is None or r_[0] in only) and
                not (r_[2] and not quiet and r_[0] in ("lane", "path") and den <= BM_STR_LANE_DEN)]
        runs.sort(key=lambda r_: rank.get(r_[0], 1))
        if case:
            for cl, P, _i in runs:
                if cl != "path":
                    tag(("line", P, case, sw.get(cl, sw["lane"]) + 2.0 * STR_CASING_MM, None, 1.0), "base_outlines",
                        "a", cl)
        for cl, P, _i in runs:
            tag(("line", P, (case or st_col("lane")) if cl == "path" else st_col(cl), sw.get(cl, sw["lane"]), None,
                 1.0), "base_outlines", "a", cl)
    # (f) the stream: M5 water_plan where the script has it (not on key maps), else the p02 blue fill and bank line
    if lay["stream"]:
        wc, we = bm_key_col("water"), bm_key_col("water_edge")
        if callable(globals().get("water_plan")) and not quiet:
            ws = [g for g in L.get("water") or [] if g and len(g[0]) >= 3 and _bm_hit(g[0], box)]
            if ws:
                tag(("water", ws, [P for P in L.get("water_edge") or [] if len(P) >= 2 and _bm_hit(P, box)], 1.0),
                    "water", "f", "stream")
        else:
            fills(L.get("water") or [], wc, "f", "stream", layer="water", nonzero=False)
            for P in L.get("water_edge") or []:
                if len(P) >= 2 and _bm_hit(P, box):
                    tag(("line", P, we, BM_LW["water_edge"], None, 1.0), "water", "f", "stream")
        fills(L.get("water_out") or [], wc, "f", "stream", layer="water", nonzero=False)
        for kind, P in L.get("waterways_out") or []:
            if len(P) >= 2 and _bm_hit(P, box):
                tag(("line", P, wc, BM_LW["river_osm" if kind == "river" else "stream_osm"], None, 1.0), "water",
                    "f", "stream")
        # (g) decks, the covered course and the bridges over the stream
        fills([[R] for R in L.get("decks") or []], bm_key_col("road") if quiet else str_hex("lane"), "g", "deck",
              layer="structures")
        for P in L.get("covered") or []:
            if len(P) >= 2 and _bm_hit(P, box):
                tag(("line", P, we, BM_LW["covered"], list(BM_COVERED_DASH), 1.0), "structures", "f", "covered")
        for P in list(L.get("bridges") or []) + list(L.get("bridges_out") or []):
            if len(P) >= 2 and _bm_hit(P, box):
                tag(("line", P, bm_key_col("bridge"), BM_LW["bridge"], None, 1.0), "structures", "g", "bridge")
    # names (b, c, f, g, h): above the stream and the bridges; the page's free-spot placer sets them (4 pt floor)
    if lay.get("names") and not quiet:
        pt = BM_CTX_PT
        for n, p, a, cl, _ln in basemap_street_names(box, D, classes=tuple(opts.get("street_classes") or ("main",))):
            tag(("text", n, p, pt["street"] * BM_PT_MM, hue("CTX", 2), False, "MC", a), "structures", "b", "name")
        for n, p, _rs in basemap_mahalle(box, D):
            up = n.replace(u"i", u"İ").replace(u"ı", u"I").upper()        # Turkish capitals (İ, I)
            tag(("text", up, p, pt["mahalle"] * BM_PT_MM, HUE_KEY["street_names"], False, "MC", 0.0), "structures",
                "c", "name")
        if lay["stream"] and opts.get("stream_name", True):
            sl = _bm_stream_label(L, box)
            if sl:
                tag(("text", BM_STREAM_NAME, sl[0], pt["stream"] * BM_PT_MM, hue("WAT", 1), False, "MC", sl[1]),
                    "structures", "f", "name")
        for n, p, _c in basemap_bridge_names(box, D):
            tag(("text", n, p, pt["bridge"] * BM_PT_MM, hue_of(n, hue("CTX", 1)), False, "MC", 0.0), "structures",
                "g", "name")
        for n, p, cat, _k in basemap_places(box, D, civic=opts.get("civic", False)):
            r1 = hue_name(n, None, cat) == ("HER", 1)
            tag(("text", n, p, (pt["place_r1"] if r1 else pt["place"]) * BM_PT_MM, hue_of(n, hue("CTX", 1), cat),
                 False, "MC", 0.0), "structures", "h", cat or "place")
    return out


def basemap_context_log(page, map_id, items, study=None, log=None, names_drawn=None, no_room=None, D=None):
    """round 9 (G9-4 item 5, S7): the done-when lines of a context map, from its items (after ml_crop):
    `context <page> <map> layers <letters> (<n>/10)`, one FLAG per letter without data (with the file key it reads),
    `fabric <page> classes <n> (<classes>)`, and the names line `names <page> <map> n=<drawn> of <in window>` (in
    window = the place names (h) inside the map's window; drawn = names_drawn, default in window minus no_room) with
    `FLAG names <page> <map> no room (<n>): ...` when the placer found no room. study: the page draws the study line
    (None = the basemap has a study area). Lines go to log (default ML_LOG when included) and are returned."""
    have, sub = set(), set()
    fab, n_h = [], 0
    for it in items or ():
        c = getattr(it, "ctx", None)
        if not c:
            continue
        have.add(c)
        if it[0] == "text":
            sub.add(c + "_name")
            if c == "h":
                n_h += 1
        elif c == "d" and getattr(it, "cls", None) not in fab:
            fab.append(it.cls)
    if study is None:
        study = bool(basemap_study(D))
    if study:
        have.add("j")
    lets = [c for c, _w in BM_CTX_LETTERS if c in have]
    lines = [u"context %s %s layers %s (%d/10)" % (page, map_id, u"".join(lets) or u"-", len(lets))]
    for c, what in BM_CTX_LETTERS:
        if c not in have:
            lines.append(u"FLAG context %s %s layer %s (%s): no data in this window (%s)" % (page, map_id, c, what,
                                                                                           BM_CTX_SRC[c]))
    if "g" in have and "g_name" not in sub:
        lines.append(u"FLAG context %s %s layer g: bridges drawn without names (basemap.json layers bridge_names)" % (
            page, map_id))
    fab.sort(key=lambda k: FAB_RANK.get(k, 99))
    lines.append(u"fabric %s classes %d (%s)" % (page, len(fab), u", ".join(fab) or u"-"))
    nr = list(no_room or ())
    drawn = names_drawn if names_drawn is not None else max(0, n_h - len(nr))
    lines.append(u"names %s %s n=%d of %d" % (page, map_id, drawn, n_h))
    if nr:
        lines.append(u"FLAG names %s %s no room (%d): %s" % (page, map_id, len(nr), u", ".join(u"%s" % s for s in nr)))
    dst = log if log is not None else globals().get("ML_LOG", _BM_WARN)
    dst.extend(lines)
    return lines


def basemap_legend_rows(items, words=None):
    """round 9 (G9-4 item 3 "no unexplained white"): the legend rows of the context classes a map shows, in the
    order unmapped ground -> land cover -> building fabric -> streets -> stream -> bridges -> contours, as
    [(swatch, text)] for Ix.legend; swatch = dict(kind "fill" | "line", colour, stroke, width_pt, cat, rank), the
    colour as drawn (key maps: the quiet tone). words: {cls: text} over BM_CTX_WORDS / FAB_WORDS"""
    seen = {}
    for it in items or ():
        c, k = getattr(it, "ctx", None), getattr(it, "cls", None)
        if not c or not k or it[0] == "text" or (c, k) in seen:
            continue
        if it[0] == "line" and c == "a" and k != "path" and it[2] == STR_CASING:
            continue                                      # a street's casing line: the swatch is its class colour
        if it[0] == "fill":
            seen[(c, k)] = dict(kind="fill", colour=it[2], stroke=None, width_pt=0.0)
        elif it[0] == "line":
            seen[(c, k)] = dict(kind="line", colour=it[2], stroke=None, width_pt=round(float(it[3]) / BM_PT_MM, 3))
        elif it[0] == "water":
            seen[(c, k)] = dict(kind="fill", colour=bm_key_col("water"), stroke=None, width_pt=0.0)
    W = dict(BM_CTX_WORDS)
    W.update(FAB_WORDS)
    W.update(words or {})
    order = [("e", "unmapped", "CTX", 5)] + [("e", k, "LC", LC_RANK[k]) for k in
                                             ("trees", "orchard", "shrub", "park", "grass", "farmland")] + \
            [("d", k, "FAB", FAB_RANK[k]) for k in FAB_CLASSES] + \
            [("a", k, "STR", STR_RANK.get(k, 3)) for k in ("main", "secondary", "lane", "area", "path")] + \
            [("f", "stream", "WAT", 1), ("g", "bridge", "CTX", 1), ("i", "contour", "CTX", 3)]
    out = []
    for c, k, cat, rk in order:
        sw = seen.get((c, k))
        if sw:
            sw = dict(sw, cat=cat, rank=rk)
            out.append((sw, W.get(k, k)))
    return out


def _bm_items(D, mode, override, box, split_buildings, scale_den=None, opts=None):
    """basemap_items without the memo"""
    lay = basemap_layers(mode, override)
    if mode in ("context", "keymap"):                     # round 9 (S3, G9-4 / G9-5): layers a-j; key maps quieter
        return _bm_context_items(D, lay, box, split_buildings, scale_den, quiet=mode == "keymap", opts=opts)
    L = D["layers"]
    out = []
    outl = []          # round 4 (S2, CHK-3 §1.6): outlines (street, building, bridge edges) come after EVERY fill
    # round 5 (S2, G-R5-8): every item carries its map layer (_BmIt.layer): ground, houses and streets "base_fills",
    # contours "base_contours", outlines "base_outlines", the stream "water", decks / covered course / bridges
    # "structures" (map_draw draws "water" above every project tint, then "structures")

    def fills(groups, col, alpha=1.0, nonzero=True, chunk=300, layer="base_fills"):
        cur = []
        for g in groups:
            g = [R for R in g if len(R) >= 3]
            if not g or not _bm_hit(g[0], box):
                continue
            if split_buildings:
                out.append(_bm_tag(("fill", g, col, alpha, nonzero), layer))
                continue
            cur.extend(g)
            if len(cur) >= chunk:
                out.append(_bm_tag(("fill", cur, col, alpha, nonzero), layer))
                cur = []
        if cur:
            out.append(_bm_tag(("fill", cur, col, alpha, nonzero), layer))

    def lines(Ps, col, w, dash=None, alpha=1.0, outline=False, layer=None):
        for P in Ps:
            if len(P) >= 2 and _bm_hit(P, box):
                (outl if outline else out).append(_bm_tag(("line", P, col, w, list(dash) if dash else None, alpha),
                                                          layer or ("base_outlines" if outline else "base_fills")))
    key = mode == "keymap"

    # ground: tree cover, fields, parks / grass (satellite first, mapped areas over it)
    if key:                                               # round 5 (S2, G-R5-3): the p02 ground (draw_landuse_map
        if lay["green"]:                                  # order: satellite classes, then mapped zones)
            fills(L["lc"].get("grass", []), bm_key_col("grass"))
            fills(L["lc"].get("shrub", []), bm_key_col("shrub"))
        if lay["trees"]:
            fills(L["lc"].get("trees", []), bm_key_col("trees"))
        if lay["fields"]:
            fills(L["lc"].get("farmland", []), bm_key_col("farmland"))
            fills(L["lc"].get("orchard", []), bm_key_col("orchard"))
            fills([z["rings"] for z in L["zones"] if z["kind"] == "agri"], bm_key_col("agri"))
        if lay["green"]:
            fills([z["rings"] for z in L["zones"] if z["kind"] == "green" and z.get("sub") == "grass"],
                  bm_key_col("grass"))
            fills([z["rings"] for z in L["zones"] if z["kind"] == "green" and z.get("sub") not in ("grass", "wood")],
                  bm_key_col("park"))
        if lay["trees"]:
            fills([z["rings"] for z in L["zones"] if z["kind"] == "green" and z.get("sub") == "wood"],
                  bm_key_col("wood"))
    if not key and lay["trees"]:
        fills(L["lc"].get("trees", []), BM_COL["tree"])
    if not key and lay["fields"]:
        fills(L["lc"].get("farmland", []) + L["lc"].get("orchard", []), BM_COL["field"])
        fills([z["rings"] for z in L["zones"] if z["kind"] == "agri"], BM_COL["field"])
    if not key and lay["green"]:
        fills([z["rings"] for z in L["zones"] if z["kind"] == "green" and z.get("sub") != "wood"], BM_COL["park"])
    if not key and lay["trees"]:
        fills([z["rings"] for z in L["zones"] if z["kind"] == "green" and z.get("sub") == "wood"], BM_COL["tree"])
    # contours
    if lay["contours"]:
        cs = L["contours"]
        if lay["contours"] == "height":
            zs = [c[1] for c in cs if c[1] is not None]
            z0, z1 = (min(zs), max(zs)) if zs else (0.0, 1.0)
            for major, z, P in cs:
                col = _bm_ramp((z - z0) / max(1.0, z1 - z0)) if z is not None else BM_COL["contour"]
                lines([P], col, BM_LW["contour_topo"][1 if major else 0], layer="base_contours")
        else:
            for major, z, P in cs:
                lines([P], BM_COL["contour"], BM_LW["contour"][1 if major else 0], layer="base_contours")
    # streets
    st = lay["streets"]
    if st == "key":                                       # round 5 (S2): light street areas, no edges; main roads
        fills(L["street_areas"], bm_key_col("road"), nonzero=False)       # beyond the frame as light centrelines
        for cl, P in L["streets_out"]:
            if cl == "main":
                lines([P], bm_key_col("road_line"), BM_LW["main"])
    elif st == "muted":                                     # round 4 (S2): light fill, light closed edges, after fills
        fills(L["street_areas"], BM_MUTED["road"], nonzero=False)
        for cl, P in L["streets_out"]:
            lines([P], BM_MUTED["road_edge"], BM_LW[cl] * (1.6 if cl != "path" else 1.0))
        for g in L["street_areas"]:                       # every ring of a street area closed (no open survey run)
            lines([list(R) + [R[0]] for R in g if len(R) >= 3], BM_MUTED["road_edge"], BM_MUTED["lw"], outline=True)
    elif st is True or st == "faint":
        faint = st == "faint"
        fills(L["street_areas"], BM_FAINT["road"] if faint else BM_COL["road"], nonzero=False)
        for cl, P in L["streets_out"]:                    # beyond the frame: OpenStreetMap centrelines
            lines([P], BM_FAINT["road_line"] if faint else BM_COL["road"], BM_LW[cl] * (1.6 if cl != "path" else 1.0))
        if faint:                                         # round 4 (S2, CHK-3 §1.6): faint modes keep their edges
            for g in L["street_areas"]:
                lines([list(R) + [R[0]] for R in g if len(R) >= 3], BM_FAINT["road_line"], 0.08, outline=True)
        else:
            lines(L["street_edges"], BM_COL["road_edge"], BM_LW["road_edge"], outline=True)
    elif st:
        for cl, P in L["streets_in"] + L["streets_out"]:
            if cl in st:
                lines([P], BM_FAINT["road_line"] if cl != "main" else BM_COL["road_edge"], BM_LW[cl])
    # the stream: ONE drawing (the site board's water and its edge inside the frame, OpenStreetMap's course beyond).
    # M3 (30 Oct): drawn by M5 (common/water.py water_plan, page mm) when the script includes it: one "water" item
    # that basemap_draw hands to water_plan after the map's T (else the plain fill and edge, as before)
    if lay["stream"]:
        wc, we = (bm_key_col("water"), bm_key_col("water_edge")) if key else (BM_COL["water"], BM_COL["water_edge"])
        if callable(globals().get("water_plan")) and not key:
            ws = [g for g in L["water"] if g and len(g[0]) >= 3 and _bm_hit(g[0], box)]
            if ws:
                out.append(_bm_tag(("water", ws, [P for P in L["water_edge"] if len(P) >= 2 and _bm_hit(P, box)],
                                    1.0), "water"))
        else:
            fills(L["water"], wc, nonzero=False, layer="water")
            lines(L["water_edge"], we, BM_LW["water_edge"], layer="water")
        if st is True or st in ("faint", "muted", "key"):
            fills([[R] for R in L["decks"]], BM_MUTED["road"] if st == "muted" else
                  (BM_FAINT["road"] if st == "faint" else (bm_key_col("road") if st == "key" else BM_COL["road"])),
                  layer="structures")
        for P in L["covered"]:
            lines([P], we, BM_LW["covered"], BM_COVERED_DASH, outline=True, layer="structures")
        fills(L["water_out"], wc, nonzero=False, layer="water")
        for kind, P in L["waterways_out"]:
            lines([P], wc, BM_LW["river_osm" if kind == "river" else "stream_osm"], layer="water")
    # buildings
    bl = lay["buildings"]
    if bl == "fabric":                                    # round 5 (S2, G-R5-3): houses by urban fabric, fills only
        groups = {}
        for b in L["buildings"]:
            groups.setdefault(bm_fabric_col(b), []).append(b["rings"][:b.get("np", len(b["rings"]))])
        for col in sorted(groups):
            fills(groups[col], col)
    elif bl == "muted" and not callable(globals().get("bld_plan_items")):
        _BM_WARN.append(u"WARNING: basemap buildings 'muted' need common/buildings.py (M11): drawn as plain light "
                        u"fills with their outlines instead.")
        fills([b["rings"] for b in L["buildings"]], BM_MUTED["bld"])
        for bk in L.get("blocks") or []:
            lines([list(R) + [R[0]] for R in bk["rings"] if len(R) >= 3], BM_MUTED["bld_edge"], BM_MUTED["lw"],
                  outline=True)
    elif bl == "muted":                                   # round 4 (S2, G-R4-4): light houses, ONE closed outline per
        for it in bld_plan_items(L["buildings"], blocks=L.get("blocks"), scale_den=scale_den or 5000.0, box=box,
                                 roof="none", fill=BM_MUTED["bld"], edge=BM_MUTED["bld_edge"],   # block, no roof marks
                                 her_fill=BM_MUTED["her"], her_edge=BM_MUTED["her_edge"], lw=BM_MUTED["lw"]):
            (outl if it[0] == "line" else out).append(_bm_tag(it, "base_outlines" if it[0] == "line" else
                                                              "base_fills"))
    elif bl in ("plan", "plan_faint"):                      # M11: outline per block + roof reading, no stripes
        pf = globals().get("bld_plan_items")
        if callable(pf):
            faint = bl == "plan_faint"
            blocks = L.get("blocks")
            for it in pf(L["buildings"], blocks=blocks, scale_den=scale_den or 5000.0, box=box,
                         fill=BM_FAINT["bld_veryfaint"] if faint else None,
                         edge=BM_FAINT["road_line"] if faint else None,
                         roof_col=BM_FAINT["bld"] if faint else None,
                         her_fill=BM_COL["her"] if not faint else "F1E6E5",
                         her_edge=BM_COL["her_edge"] if not faint else "CDAAAA"):
                (outl if it[0] == "line" else out).append(_bm_tag(it, "base_outlines" if it[0] == "line" else
                                                                  "base_fills"))   # roof marks, outlines after fills
        else:
            _BM_WARN.append(u"WARNING: basemap buildings '{}' need common/buildings.py (M11): drawn faint "
                            u"instead.".format(bl))
            fills([b["rings"] for b in L["buildings"]], BM_FAINT["bld"])
    elif bl:
        if bl is True:
            fills([b["rings"] for b in L["buildings"] if not b.get("her")], BM_COL["bld"])
            fills([b["rings"] for b in L["buildings"] if b.get("her")], BM_COL["her"])
            for b in L["buildings"]:
                if b.get("her") or b.get("osm"):
                    lines([R + R[:1] for R in b["rings"][:b.get("np", len(b["rings"]))]],
                          BM_COL["her_edge"] if b.get("her") else BM_COL["bld_osm_edge"],
                          BM_LW["her_edge"] if b.get("her") else BM_LW["osm_edge"], outline=True)
            for bk in L.get("blocks") or []:                # round 4 (S2, CHK-3 §1.5): survey houses get their edge too
                if not bk.get("her"):
                    lines([list(R) + [R[0]] for R in bk["rings"] if len(R) >= 3], BM_COL["bld_osm_edge"],
                          BM_LW["osm_edge"], outline=True)
        else:
            fills([b["rings"] for b in L["buildings"]],
                  BM_FAINT["bld_veryfaint"] if bl == "veryfaint" else BM_FAINT["bld"])
    if lay["stream"] and key:                             # round 5 (S2): bridges over the blue stream (p02 order 18)
        lines(L["bridges"], bm_key_col("bridge"), BM_LW["bridge"], outline=True, layer="structures")
    elif lay["stream"] and (st is True or bl is True or bl == "plan"):
        lines(L["bridges"], BM_COL["ink"], BM_LW["bridge"], outline=True, layer="structures")
    elif lay["stream"] and bl == "muted":                 # round 4: bridges in the muted edge tone, a little heavier
        lines(L["bridges"], BM_MUTED["bld_edge"], 2.0 * BM_MUTED["lw"], outline=True, layer="structures")
    out.extend(outl)                                      # round 4 (S2): every outline after every fill
    # M3 (30 Oct): the study area (one outline, one style, on top of the base) and the place names
    if lay.get("study_area"):
        for it in basemap_study_items(D):
            if _bm_hit(it[1], box):
                out.append(_bm_tag(it, "base_outlines"))
    if lay.get("names"):
        for n, p in basemap_names(box, D):
            out.append(_bm_tag(("text", n, p, BM_NAME_MM, BM_MUTED["name"] if mode == "muted" else BM_COL["ink"],
                                False, "MC"), "base_names"))
    return out


def basemap_draw(items, T, fill_fn, line_fn, text_fn=None, water_opts=None):
    """draws items through the caller's page: T(p) survey m -> page point; fill_fn(rings, hex, alpha, nonzero);
    line_fn(pts, hex, width_mm, dash_mm, alpha); text_fn(s, (x, y), size_mm, hex, bold, align) (texts are left out
    without it). Returns the number of items drawn. M3 (30 Oct): a "water" item (the stream, when the script includes
    M5 common/water.py) is drawn by water_plan(ring in page mm, k, holes=its islands, **water_opts) through the same
    three functions (k = page mm per survey m, from T); if M5 fails, the plain fill and bank line (a WARNING in
    basemap_warnings())."""
    import math as _m
    n = 0
    for it in items:
        if it[0] == "fill":
            fill_fn([[T(p) for p in R] for R in it[1]], it[2], it[3], it[4])
        elif it[0] == "line":
            line_fn([T(p) for p in it[1]], it[2], it[3], it[4], it[5])
        elif it[0] == "text" and text_fn is not None:
            text_fn(it[1], T(it[2]), it[3], it[4], it[5], it[6])
        elif it[0] == "water":
            p0 = it[1][0][0][0][0], it[1][0][0][0][1]          # first point of the first ring of the first group
            a, b = T(p0), T((p0[0] + 100.0, p0[1]))
            k = _m.hypot(b[0] - a[0], b[1] - a[1]) / 100.0
            try:
                wp = globals()["water_plan"]                # M5 (common/water.py), present: _bm_items checked it
                for g in it[1]:
                    hs = [[T(p) for p in R] for R in g[1:] if len(R) >= 3]     # islands: open, untextured (A2 fix)
                    wl = wp([T(p) for p in g[0]], k, holes=hs, **(water_opts or {}))
                    for s_ in wl.shapes():
                        if s_[0] == "poly" and len(s_[1]) >= 3:
                            al = s_[5] if len(s_) > 5 and s_[5] is not None else 1.0
                            ho = [list(R) for R in (s_[6] if len(s_) > 6 and s_[6] else ())]
                            if s_[2]:
                                fill_fn([list(s_[1])] + ho, s_[2], al, not ho)          # even-odd with holes
                            if s_[3]:
                                line_fn(list(s_[1]) + [s_[1][0]], s_[3], s_[4] or 0.1, None, al)
                        elif s_[0] == "line" and len(s_[1]) >= 2:
                            line_fn(list(s_[1]), s_[2], s_[3], s_[4] if len(s_) > 4 else None, 1.0)
                        elif s_[0] == "text" and text_fn is not None:
                            text_fn(s_[1], (s_[2], s_[3]), s_[4], s_[5], s_[6] if len(s_) > 6 else False,
                                    s_[7] if len(s_) > 7 else "L")
            except Exception as ex_:
                _BM_WARN.append(u"WARNING: basemap: the M5 water drawing failed ({}: {}); the stream is drawn as the "
                                u"base map's own fill.".format(type(ex_).__name__, ex_))
                fill_fn([[T(p) for p in R] for g in it[1] for R in g], BM_COL["water"], 1.0, False)
                for P in it[2]:
                    line_fn([T(p) for p in P], BM_COL["water_edge"], BM_LW["water_edge"], None, 1.0)
        else:
            continue
        n += 1
    return n


# ------------------------------------------------------------------------------------------- key-map cut lines
def _bm_clip_convex(a, b, poly):
    """the part of segment a-b inside the convex polygon poly (any turn), or None"""
    t0, t1 = 0.0, 1.0
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = len(poly)
    s = sum((poly[(i + 1) % n][0] - poly[i][0]) * (poly[(i + 1) % n][1] + poly[i][1]) for i in range(n))
    ccw = s < 0
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        ex, ey = q[0] - p[0], q[1] - p[1]
        nx, ny = (-ey, ex) if ccw else (ey, -ex)          # inward normal
        den = nx * dx + ny * dy
        num = nx * (a[0] - p[0]) + ny * (a[1] - p[1])
        if abs(den) < 1e-12:
            if num < 0:
                return None
            continue
        t = -num / den
        if den > 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
        if t0 > t1:
            return None
    return (a[0] + dx * t0, a[1] + dy * t0), (a[0] + dx * t1, a[1] + dy * t1)


def basemap_cut_ids(ids, looks=None):
    """cuts for km_keymap / km_cut_items from the level module (common/levels.py, its data included before it): the ends
    and their names of each cut id; looks = {id: -1} to turn a marker round"""
    ends, labs = globals().get("level_ends"), globals().get("level_end_labels")
    if not callable(ends) or not callable(labs):
        raise RuntimeError("basemap_cut_ids needs the level module: include ../common/data/LEVELS.py and "
                           "../common/levels.py")
    out = []
    for cid in ids:
        a, b = ends(cid)
        out.append((a, b, labs(cid), (looks or {}).get(cid, 1)))
    return out


# M4 key map: in keymap.py (round 7 v4: km_keymap = SON page8 key map; the round 3 wrappers are gone)


# ------------------------------------------------------------------------------------------- writing (site board)
def _bm_r(P, nd=1):
    return [[round(p[0], nd), round(p[1], nd)] for p in P]


def _bm_clip_rect(P, closed, r):
    """P clipped to the axis-aligned rectangle r = (u0, v0, u1, v1) (frame-local): a polygon (Sutherland-Hodgman,
    one ring or None) or a polyline (its runs inside)"""
    u0, v0, u1, v1 = r
    if closed:
        R = list(P)
        for k_, lim, keep_ge in ((0, u0, True), (0, u1, False), (1, v0, True), (1, v1, False)):
            if not R:
                return None
            nxt = []
            for i in range(len(R)):
                p, q = R[i - 1], R[i]
                pin = p[k_] >= lim if keep_ge else p[k_] <= lim
                qin = q[k_] >= lim if keep_ge else q[k_] <= lim
                if qin:
                    if not pin:
                        t = (lim - p[k_]) / (q[k_] - p[k_])
                        nxt.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
                    nxt.append(q)
                elif pin:
                    t = (lim - p[k_]) / (q[k_] - p[k_])
                    nxt.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
            R = nxt
        return R if len(R) >= 3 else None
    runs, cur = [], []
    for a, b in zip(P, P[1:]):
        t0, t1 = 0.0, 1.0
        d = (b[0] - a[0], b[1] - a[1])
        ok = True
        for k_, lim, sgn in ((0, u0, 1), (0, u1, -1), (1, v0, 1), (1, v1, -1)):
            den = d[k_] * sgn
            num = (a[k_] - lim) * sgn
            if abs(den) < 1e-12:
                if num < 0:
                    ok = False
                    break
                continue
            t = -num / den
            if den > 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                ok = False
                break
        if not ok:
            if len(cur) > 1:
                runs.append(cur)
            cur = []
            continue
        p0 = (a[0] + d[0] * t0, a[1] + d[1] * t0)
        p1 = (a[0] + d[0] * t1, a[1] + d[1] * t1)
        if cur and (abs(cur[-1][0] - p0[0]) > 1e-9 or abs(cur[-1][1] - p0[1]) > 1e-9):
            if len(cur) > 1:
                runs.append(cur)
            cur = []
        if not cur:
            cur = [p0]
        cur.append(p1)
        if t1 < 1.0:
            runs.append(cur)
            cur = []
    if len(cur) > 1:
        runs.append(cur)
    return runs


def basemap_export(S, log=None):
    """SITE BOARD ONLY, once a run after the site model and its land cover are made (S = the site model; S.osm the
    parsed OpenStreetMap file): writes BASEMAP_FILE. Inside the analysis frame the site board's own layers (the
    ones p.06 draws), between the frame and the extent OpenStreetMap's, cut at the frame's edge so nothing is drawn
    twice; contours (survey, frame only) carry their height. Returns the path, or None (a WARNING in log)."""
    import time as _t
    log = log if log is not None else []
    # unchanged site model (same build_site key, S.site_key) = the file on disk is kept, not made again
    kf = BASEMAP_FILE + ".key"
    key = u"{}|{}|{}".format(BASEMAP_FORMAT, globals().get("SCRIPT_VERSION", ""), getattr(S, "site_key", None) or "")
    try:
        if getattr(S, "site_key", None) and _bm_os.path.isfile(BASEMAP_FILE) and _bm_os.path.isfile(kf):
            with open(kf, "r", encoding="utf-8") as fh:
                if fh.read().strip() == key:
                    log.append(u"Shared basemap unchanged (same site model): {} kept.".format(BASEMAP_FILE))
                    return BASEMAP_FILE
    except Exception:
        pass
    try:
        F = S.F
        loc = lambda p: F.local(p[0], p[1])
        wld = lambda q: F.world(q[0], q[1])
        fr = (F.u0, F.v0, F.u1, F.v1)
        us = [loc(p)[0] for _, p in BASEMAP_REACH] + [F.u0, F.u1]
        vs = [loc(p)[1] for _, p in BASEMAP_REACH] + [F.v0, F.v1]
        ex = (min(us) - BASEMAP_MARGIN, min(vs) - BASEMAP_MARGIN, max(us) + BASEMAP_MARGIN, max(vs) + BASEMAP_MARGIN)
        # the ring between frame and extent as four rectangles that do not overlap (frame-local)
        ring = [(ex[0], ex[1], ex[2], fr[1]), (ex[0], fr[3], ex[2], ex[3]),
                (ex[0], fr[1], fr[0], fr[3]), (fr[2], fr[1], ex[2], fr[3])]

        def outside_poly(P):
            Q = [loc(p) for p in P]
            res = []
            for r in ring:
                c = _bm_clip_rect(Q, True, r)
                if c:
                    res.append(_bm_r([wld(q) for q in c]))
            return res

        def outside_line(P):
            Q = [loc(p) for p in P]
            return [_bm_r([wld(q) for q in run]) for r in ring for run in _bm_clip_rect(Q, False, r)]

        def in_frame_name(u):
            u_, v_ = loc((u["cx"], u["cy"]))
            return fr[0] <= u_ <= fr[2] and fr[1] <= v_ <= fr[3]

        def in_ring(p):
            u, v = loc(p)
            return ex[0] <= u <= ex[2] and ex[1] <= v <= ex[3] and not (fr[0] <= u <= fr[2] and fr[1] <= v <= fr[3])
        L = dict(lc={}, zones=[], contours=[], street_areas=[], street_edges=[], streets_in=[], streets_out=[],
                 water=[], water_edge=[], decks=[], covered=[], water_out=[], waterways_out=[], buildings=[],
                 bridges=[], blocks=[], study=[], names=[], street_names=[])
        sn_best = {}                                      # round 4 (S2, G-R4-9 U55): street name -> longest run
        unnamed = []                                      # round 5 (S2, A11): survey names with no names-table row

        def street_name(tags, P, cl):
            nm_ = ((tags or {}).get("name") or u"").strip()
            if not nm_ or cl == "path" or len(P) < 2:
                return
            Ln = sum(_bm_math.hypot(b_[0] - a_[0], b_[1] - a_[1]) for a_, b_ in zip(P, P[1:]))
            if nm_ not in sn_best or Ln > sn_best[nm_][0]:
                sn_best[nm_] = (Ln, cl, P)
        mains = set(globals().get("MAIN_ROADS") or ("motorway", "trunk", "primary", "secondary", "tertiary"))
        peds = set(globals().get("PED") or ("footway", "path", "pedestrian", "steps", "cycleway", "bridleway",
                                             "track", "corridor"))
        skip = set(globals().get("SKIP_HW") or ("proposed", "construction", "platform", "bus_stop", "elevator"))
        ccls = lambda hw: "path" if hw in peds else ("main" if hw in mains else "lane")
        # ---- inside the frame: the site board's layers
        lcf = globals().get("r28e_lc")
        for key in ("trees", "farmland", "orchard", "grass", "shrub"):       # round 5 (S2): grass, shrub for key maps
            try:
                groups = lcf(S, key) if callable(lcf) else [[P] for P in (getattr(S, "lc", None) or {}).get(key) or []]
            except Exception:
                groups = [[P] for P in (getattr(S, "lc", None) or {}).get(key) or []]
            L["lc"][key] = [[_bm_r(P) for P in g if len(P) >= 3] for g in groups]
        for z in getattr(S, "zones", None) or []:
            if z["kind"] in ("green", "agri"):
                L["zones"].append(dict(kind=z["kind"], sub=z.get("sub"), rings=[_bm_r(P) for P in z["Ps"] + z["Hs"]]))
        z_at = getattr(S, "z_at", None)
        for major, P in getattr(S, "contours", None) or []:
            z = None
            if callable(z_at):
                try:
                    zs = sorted(z_at(p[0], p[1]) for p in P[::max(1, len(P) // 9)])
                    z = round(zs[len(zs) // 2], 1)     # round 3 (B2, P11.1 relief): median to 0.1 m (was 5 m steps)
                except Exception:
                    z = None
            L["contours"].append([bool(major), z, _bm_r(P)])
        for rg in getattr(S, "road_net", None) or []:
            L["street_areas"].append([_bm_r(rg["P"])] + [_bm_r(H) for H in rg.get("H", [])])
        L["street_edges"] = [_bm_r(P) for P in getattr(S, "road_lines_net", None) or []] + \
            [_bm_r(r_["P"]) for r_ in S.roads if not r_.get("w")]
        L["streets_in"] = [[ccls((r_.get("tags") or {}).get("highway")), _bm_r(r_["P"])] for r_ in S.roads] + \
            [["path", _bm_r(r_["P"])] for r_ in getattr(S, "paths", None) or []]
        for r_ in S.roads:
            street_name(r_.get("tags"), r_["P"], ccls((r_.get("tags") or {}).get("highway")))
        L["water"] = [[_bm_r(wt["P"])] + [_bm_r(H) for H in wt.get("H", [])] for wt in S.water]
        L["water_edge"] = [_bm_r(P) for P in getattr(S, "water_outline", None) or []]
        L["decks"] = [_bm_r(P) for P in getattr(S, "decks", None) or []]
        L["covered"] = [_bm_r(P) for P in getattr(S, "covered", None) or []]
        L["bridges"] = [_bm_r(P) for P in getattr(S, "bridges", None) or []]
        # buildings: one outline per building (build_site merged its pieces: revision 30 Oct, G7) with its height,
        # and the blocks (buildings sharing a wall as ONE outline, S.blocks): the plan's outline layer, so no party
        # wall, survey tick or label split is ever drawn as a line
        idx_of = {}
        for i_u, u in enumerate(S.bld):
            parts = [_bm_r(P) for P in u["parts"] if len(P) >= 3]
            if parts:
                idx_of[i_u] = len(L["buildings"])
                tg = u.get("tags") or {}
                her = u.get("fabric") in ("monument", "sacred") or bool(tg.get("historic")) or \
                    tg.get("amenity") == "place_of_worship"
                L["buildings"].append(dict(rings=parts + [_bm_r(H) for H in (u.get("holes") or [])], np=len(parts),
                                           her=her, osm=u.get("src") in ("osm", "osm+label"),
                                           h=round(float(u.get("h") or 0.0), 2), floors=int(u.get("floors") or 0),
                                           fabric=u.get("fabric") or "regular", annex=bool(u.get("annex"))))
                if her and (u.get("name") or "").strip() and in_frame_name(u):
                    # round 5 (S2, A11): only names the names table records, in its one spelling (place_label);
                    # a survey name with no table row is left out and listed (never print an unchecked name)
                    pl = globals().get("place_label")
                    raw, pc = u["name"].strip(), (u["cx"], u["cy"])
                    nm_ = pl(raw, pc) if callable(pl) else None
                    if nm_ and nm_ not in [n_ for n_, _ in L["names"]]:
                        L["names"].append([nm_, [round(u["cx"], 1), round(u["cy"], 1)]])
                    elif not nm_ and raw not in unnamed:
                        unnamed.append(raw)
        blocks = getattr(S, "blocks", None)
        if blocks is None and callable(globals().get("bld_blocks")):
            blocks = bld_blocks(S.bld)
        for bk in blocks or []:
            mem = [idx_of[i] for i in bk.get("units", []) if i in idx_of]
            L["blocks"].append(dict(rings=[_bm_r(bk["outer"])] + [_bm_r(H) for H in bk.get("holes") or []],
                                    her=bool(mem) and all(L["buildings"][i]["her"] for i in mem)))
        L["study"] = [_bm_r(P) for P in (getattr(S, "r28_study", None) or globals().get("R28_STUDY_COPY") or [])]
        pl = globals().get("place_label")                 # round 5 (S2, A11): REACH literals by the table's spelling
        L["names"] = [[(pl(n, p) if callable(pl) else None) or n, [round(p[0], 1), round(p[1], 1)]]
                      for n, p in BASEMAP_REACH] + L["names"]
        if unnamed:
            log.append(u"FLAG basemap names not in the names table, left out ({}): {} [ask Aras for the spelling and a "
                       u"source]".format(len(unnamed), u", ".join(unnamed[:20])))
        n_in = len(L["buildings"])
        # ---- the ring between frame and extent: OpenStreetMap
        osm = getattr(S, "osm", None)
        n_out = 0
        if osm:
            Pj = osm.get("P")
            zc = globals().get("zone_class")
            chain = globals().get("chain_segments")
            for refs, tags in osm["ways"].values():
                if len(refs) < 2:
                    continue
                P = [p for p in (Pj(r) for r in refs) if p]
                if len(P) < 2:
                    continue
                closed = refs[0] == refs[-1] and len(P) >= 4
                if "building" in tags:
                    if closed:
                        c = (sum(p[0] for p in P[:-1]) / (len(P) - 1), sum(p[1] for p in P[:-1]) / (len(P) - 1))
                        if in_ring(c):
                            her = bool(tags.get("historic")) or tags.get("amenity") == "place_of_worship" or \
                                tags.get("building") in ("mosque", "church", "synagogue", "temple")
                            lv = tags.get("building:levels")
                            try:
                                lv = int(float(lv)) if lv else 0
                            except ValueError:
                                lv = 0
                            L["buildings"].append(dict(rings=[_bm_r(P[:-1])], np=1, her=her, osm=True, h=0.0,
                                                       floors=lv))
                            L["blocks"].append(dict(rings=[_bm_r(P[:-1])], her=her))
                            n_out += 1
                    continue
                hw = tags.get("highway")
                if hw and hw not in skip and tags.get("area") != "yes":
                    runs_ = outside_line(P)
                    L["streets_out"].extend([ccls(hw), run] for run in runs_)
                    for run in runs_:
                        street_name(tags, run, ccls(hw))
                    continue
                ww = tags.get("waterway")
                if ww in ("river", "stream", "canal"):
                    L["waterways_out"].extend(["river" if ww == "river" else "stream", run] for run in outside_line(P))
                    continue
                if closed:
                    if tags.get("natural") == "water" or tags.get("waterway") == "riverbank":
                        L["water_out"].extend([R] for R in outside_poly(P[:-1]))
                        continue
                    k = zc(tags) if callable(zc) else None
                    if k and k[0] in ("green", "agri"):
                        rs = outside_poly(P[:-1])
                        if rs:
                            L["zones"].append(dict(kind=k[0], sub=k[1], rings=rs))
            for mem, tags in osm.get("rels") or []:
                if tags.get("type") != "multipolygon" or "building" in tags or tags.get("ref:whc") or \
                        not callable(zc) or not callable(chain):
                    continue
                k = zc(tags)
                if not k or k[0] not in ("green", "agri"):
                    continue
                outer = []
                for ref, role in mem:
                    if role != "inner" and ref in osm["ways"]:
                        P = [p for p in (Pj(r) for r in osm["ways"][ref][0]) if p]
                        if len(P) >= 2:
                            outer.append([(p[0], p[1]) for p in P])
                for c in chain(outer, 0.05):
                    if len(c) >= 4:
                        rs = outside_poly(c[:-1] if c[0] == c[-1] else c)
                        if rs:
                            L["zones"].append(dict(kind=k[0], sub=k[1], rings=rs))
        else:
            log.append(u"WARNING: shared basemap: no OpenStreetMap in the site model, so it ends at the analysis frame.")
        stl = globals().get("street_label")               # round 5 (S2): the table's spelling where it has the street
        for nm_, (Ln, cl, P) in sn_best.items():           # the label point: the run's middle, along its direction
            half, acc = Ln / 2.0, 0.0
            for a_, b_ in zip(P, P[1:]):
                d_ = _bm_math.hypot(b_[0] - a_[0], b_[1] - a_[1])
                if acc + d_ >= half and d_ > 1e-9:
                    t_ = (half - acc) / d_
                    ang = _bm_math.degrees(_bm_math.atan2(b_[1] - a_[1], b_[0] - a_[0]))
                    L["street_names"].append([stl(nm_) if callable(stl) else nm_, [round(a_[0] + (b_[0] - a_[0]) * t_, 1),
                                                    round(a_[1] + (b_[1] - a_[1]) * t_, 1)], round(ang, 1), cl,
                                              round(Ln, 1)])
                    break
                acc += d_
        corners = lambda b: [_bm_r([wld(q)])[0] for q in ((b[0], b[1]), (b[2], b[1]), (b[2], b[3]), (b[0], b[3]))]
        out = dict(format=BASEMAP_FORMAT, source=u"{} · {}".format(globals().get("SCRIPT_VERSION", "site board"),
                                                                  _t.strftime("%Y-%m-%d %H:%M")),
                   frame=_bm_r(globals().get("SITE_FRAME_LK") or [wld(q) for q in ((fr[0], fr[1]), (fr[2], fr[1]),
                                                                                    (fr[2], fr[3]), (fr[0], fr[3]))]),
                   extent=corners(ex), reach=[[n, list(p)] for n, p in BASEMAP_REACH], layers=L,
                   note=u"survey m (0.1 m); inside the analysis frame the site board's layers (survey, OpenStreetMap, "
                        u"ESA WorldCover 2021), beyond it OpenStreetMap (Data/bergama_osm.osm, ODbL); contours from "
                        u"the survey, frame only, height = the terrain at their points to the nearest 5 m")
        _bm_os.makedirs(_bm_os.path.dirname(BASEMAP_FILE), exist_ok=True)
        with open(BASEMAP_FILE, "w", encoding="utf-8") as fh:
            _bm_json.dump(out, fh, ensure_ascii=False, separators=(",", ":"))
        for k_ in list(_BM_MEMO):
            if k_ == BASEMAP_FILE or (isinstance(k_, tuple) and k_[0] == "items"):
                _BM_MEMO.pop(k_, None)
        if getattr(S, "site_key", None):
            with open(kf, "w", encoding="utf-8") as fh:
                fh.write(key)
        log.append(u"Shared basemap written ({}): {:,} buildings in the frame, {:,} beyond it, {:,} contours, extent "
                   u"{:,.0f} x {:,.0f} m.".format(BASEMAP_FILE, n_in, n_out, len(L["contours"]), ex[2] - ex[0],
                                                 ex[3] - ex[1]))
        return BASEMAP_FILE
    except Exception as ex_:
        import traceback as _tb
        log.append(u"WARNING: the shared basemap was not written ({}):\n{}".format(ex_, _tb.format_exc()))
        return None


# ---- round 4 (S2, 1 Nov 2026): the study clip, the map-layer draw order and the key-map module ride with the basemap,
# so every script that includes basemap.py has them (never include them a second time)
# ---- Study clip (round 4 S2, 1 Nov 2026; G-R4-4 "proposals clipped to the study area", U40, S14; PLAN §4.3) --------
# ONE clip to the study area (calisma_alan of Bergama_Altlik.3dm, two closed parts worked as one area) for every
# proposal a script draws or exports: nothing designed outside it ("we cant do any adjustments outside the study
# area", U40). Clip at the SOURCE (where a proposal is generated) so every page that reads it inherits the clip.
# Included by common/basemap.py (its last lines): every script that includes basemap.py has these functions; do not
# include this file again. Geometry: survey m; rings = [[(x, y), ...], ...] (closed implicitly).
# Counts: every call with page= adds what it removed to SC_COUNT[page]; map_layers.map_draw prints it in the G-R4-4
# done-when line "layers base→project ok, n_outside_clipped <n>"; sc_lines_log() gives the per-page lines.
#   sc_rings(D=None, areas=None)                        the study rings (areas dict values, else the basemap's study)
#   sc_inside(p, rings, margin_m=0.0)                   point inside (margin_m > 0: at least that far inside)
#   sc_points(items, rings, get=None, r_frac=0.0, page=None)    keep point symbols inside (their crown too)
#   sc_lines(P, rings, page=None)                       polyline -> its runs inside (exact edge crossings)
#   sc_rings_clip(R, rings, page=None)                  polygon ∩ study (Greiner-Hormann, non-convex) -> [rings]
#   sc_items(items, rings, page=None)                   basemap-format items clipped ("fill", "line", "text")
#   sc_cell_mask(G, V, rings=None)                      bytearray per grid cell (masterplan Grid) inside the study
#   sc_lines_log()                                      "study clip <page>: n_outside_clipped=<n> (points a, lines
#                                                       b, rings c)" per page, then emptied
import math as _sc_m

SC_COUNT = {}                       # page -> dict(points=, lines=, rings=) removed this run
SC_EPS = 1e-9


def _sc_add(page, kind, n):
    if page is None or n <= 0:
        return
    c = SC_COUNT.setdefault(page, dict(points=0, lines=0, rings=0))
    c[kind] += n


def sc_count(page):
    """n_outside_clipped of a page this run (points + lines + rings removed or cut)"""
    c = SC_COUNT.get(page) or {}
    return int(c.get("points", 0) + c.get("lines", 0) + c.get("rings", 0))


def sc_rings(D=None, areas=None):
    """the study area as rings (survey m): the values of an areas dict (the masterplan's calisma_alan parts, as
    read from Bergama_Altlik.3dm), else basemap_study(D) (the basemap file's study layer, or a script's recorded
    copy); [] when neither exists (then every clip keeps everything and logs a FLAG once)"""
    if areas:
        R = areas.values() if isinstance(areas, dict) else areas
        return [[(float(p[0]), float(p[1])) for p in r] for r in R if len(r) >= 3]
    st = basemap_study(D) if callable(globals().get("basemap_study")) else []
    if not st:
        SC_COUNT.setdefault(u"_flag", dict(points=0, lines=0, rings=0))
    return [[(float(p[0]), float(p[1])) for p in r] for r in st if len(r) >= 3]


def _sc_open(r):
    return r[:-1] if len(r) > 1 and abs(r[0][0] - r[-1][0]) < SC_EPS and abs(r[0][1] - r[-1][1]) < SC_EPS else r


def _sc_pip(x, y, R):
    c, n = False, len(R)
    j = n - 1
    for i in range(n):
        xi, yi, xj, yj = R[i][0], R[i][1], R[j][0], R[j][1]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi:
            c = not c
        j = i
    return c


def _sc_dist(p, R):
    best = float("inf")
    n = len(R)
    for i in range(n):
        a, b = R[i], R[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dy * dy
        t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2)) if L2 > 0 else 0.0
        best = min(best, _sc_m.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy))
    return best


def sc_inside(p, rings, margin_m=0.0):
    """True when p lies inside one of the study rings (the parts are separate areas: inside ANY); margin_m > 0: and
    at least margin_m from that ring's outline; margin_m < 0: or within -margin_m outside it. No rings: True."""
    if not rings:
        return True
    for R in rings:
        R = _sc_open(R)
        ins = _sc_pip(p[0], p[1], R)
        if margin_m == 0.0:
            if ins:
                return True
        elif margin_m > 0.0:
            if ins and _sc_dist(p, R) >= margin_m:
                return True
        elif ins or _sc_dist(p, R) <= -margin_m:
            return True
    return False


def sc_points(items, rings, get=None, r_frac=0.0, page=None):
    """the point items inside the study area. get(item) -> (x, y) or (x, y, r) (default: the item itself, a point or
    (x, y, r)); r_frac: the share of a symbol's radius that must lie inside too (1.0 = the whole crown inside, 0 =
    its centre). Removed items are counted for the page. Returns the kept items (same objects, same order)."""
    if not rings:
        return list(items)
    get = get or (lambda it: it)
    kept, n = [], 0
    for it in items:
        q = get(it)
        r = float(q[2]) if len(q) > 2 and q[2] is not None else 0.0
        if sc_inside((q[0], q[1]), rings, margin_m=r * r_frac):
            kept.append(it)
        else:
            n += 1
    _sc_add(page, "points", n)
    return kept


def _sc_seg_ts(a, b, rings):
    """the parameters t in (0, 1) where segment a-b crosses any study ring edge"""
    ts = []
    dx, dy = b[0] - a[0], b[1] - a[1]
    for R in rings:
        R = _sc_open(R)
        n = len(R)
        for i in range(n):
            p, q = R[i], R[(i + 1) % n]
            ex, ey = q[0] - p[0], q[1] - p[1]
            den = dx * ey - dy * ex
            if abs(den) < 1e-15:
                continue
            t = ((p[0] - a[0]) * ey - (p[1] - a[1]) * ex) / den
            s = ((p[0] - a[0]) * dy - (p[1] - a[1]) * dx) / den
            if SC_EPS < t < 1.0 - SC_EPS and -SC_EPS <= s <= 1.0 + SC_EPS:
                ts.append(t)
    return sorted(ts)


def sc_lines(P, rings, page=None):
    """a polyline (survey m) -> its runs inside the study area: every segment split at its exact crossings of the
    study outlines (not a vertex test), the pieces whose middle lies inside kept and joined where they touch.
    A polyline with a part outside counts once for the page. Returns [run, ...] (each >= 2 points)."""
    P = [tuple(p[:2]) for p in P]
    if not rings or len(P) < 2:
        return [P] if len(P) >= 2 else []
    runs, cur, cut = [], [], False
    for a, b in zip(P, P[1:]):
        ts = [0.0] + _sc_seg_ts(a, b, rings) + [1.0]
        for t0, t1 in zip(ts, ts[1:]):
            if t1 - t0 < 1e-12:
                continue
            tm = 0.5 * (t0 + t1)
            pa = (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0)
            pb = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
            if sc_inside((a[0] + (b[0] - a[0]) * tm, a[1] + (b[1] - a[1]) * tm), rings):
                if cur and abs(cur[-1][0] - pa[0]) < 1e-7 and abs(cur[-1][1] - pa[1]) < 1e-7:
                    cur.append(pb)
                else:
                    if len(cur) >= 2:
                        runs.append(cur)
                    cur = [pa, pb]
            else:
                cut = True
                if len(cur) >= 2:
                    runs.append(cur)
                cur = []
    if len(cur) >= 2:
        runs.append(cur)
    if cut:
        _sc_add(page, "lines", 1)
    return runs


# ---- Greiner-Hormann polygon intersection (subject ∩ clip; both simple, any shape) ----------------------------------
class _ScNode(object):
    __slots__ = ("x", "y", "nxt", "prv", "inter", "entry", "nb", "alpha", "seen")

    def __init__(self, x, y, inter=False, alpha=0.0):
        self.x, self.y = x, y
        self.nxt = self.prv = self.nb = None
        self.inter, self.entry, self.alpha, self.seen = inter, False, alpha, False


def _sc_list(R):
    nodes = [_ScNode(p[0], p[1]) for p in R]
    n = len(nodes)
    for i in range(n):
        nodes[i].nxt = nodes[(i + 1) % n]
        nodes[i].prv = nodes[i - 1]
    return nodes


def _sc_next_orig(v):
    v = v.nxt
    while v.inter:
        v = v.nxt
    return v


def _sc_gh(S, C, union=False):
    """S ∩ C as rings, or None when a vertex lies on the other's edge (the caller perturbs and retries). round 6 (S1,
    G6-5): union=True gives S ∪ C instead (the same walk with every entry flag flipped; the key map's one study
    outline, keymap.km_study_ring); parts that never cross come back as they are (the outer one when one holds the
    other)"""
    sl, cl = _sc_list(S), _sc_list(C)
    hits = []
    for i, s0 in enumerate(sl):
        s1 = sl[(i + 1) % len(sl)]
        for j, c0 in enumerate(cl):
            c1 = cl[(j + 1) % len(cl)]
            dx, dy = s1.x - s0.x, s1.y - s0.y
            ex, ey = c1.x - c0.x, c1.y - c0.y
            den = dx * ey - dy * ex
            if abs(den) < 1e-15:
                continue
            a = ((c0.x - s0.x) * ey - (c0.y - s0.y) * ex) / den
            b = ((c0.x - s0.x) * dy - (c0.y - s0.y) * dx) / den
            if -1e-9 <= a <= 1.0 + 1e-9 and -1e-9 <= b <= 1.0 + 1e-9:
                if a < 1e-7 or a > 1.0 - 1e-7 or b < 1e-7 or b > 1.0 - 1e-7:
                    return None                           # degenerate (vertex on an edge)
                hits.append((i, a, j, b, s0.x + dx * a, s0.y + dy * a))
    if not hits and union:
        if _sc_pip(S[0][0], S[0][1], C):
            return [list(C)]
        if _sc_pip(C[0][0], C[0][1], S):
            return [list(S)]
        return [list(S), list(C)]
    if not hits:
        if _sc_pip(S[0][0], S[0][1], C):
            return [list(S)]
        if _sc_pip(C[0][0], C[0][1], S):
            return [list(C)]
        return []
    # insert the intersections into both lists, sorted by alpha along each edge
    by_s, by_c = {}, {}
    for h in hits:
        i, a, j, b, x, y = h
        ns, nc = _ScNode(x, y, True, a), _ScNode(x, y, True, b)
        ns.nb, nc.nb = nc, ns
        by_s.setdefault(i, []).append(ns)
        by_c.setdefault(j, []).append(nc)
    for base, groups in ((sl, by_s), (cl, by_c)):
        for i, grp in groups.items():
            grp.sort(key=lambda nd: nd.alpha)
            v, end = base[i], base[(i + 1) % len(base)]
            for nd in grp:
                nd.prv, nd.nxt = v, end
                v.nxt = nd
                end.prv = nd
                v = nd
    # entry / exit flags
    for start, other in ((sl[0], C), (cl[0], S)):
        status = not _sc_pip(start.x, start.y, other)    # True: the next intersection is an entry
        if union:
            status = not status                          # round 6: flipped flags walk the outside (S ∪ C)
        v = start
        while True:
            if v.inter:
                v.entry = status
                status = not status
            v = v.nxt
            if v is start:
                break
    # trace: from an unvisited intersection, forward along an entry, backward along an exit, switch lists at each
    # intersection, until the walk reaches a visited one (the start)
    out = []
    for h0 in [nd for grp in by_s.values() for nd in grp]:
        if h0.seen:
            continue
        ring, v, guard = [(h0.x, h0.y)], h0, 0
        while True:
            v.seen = True
            v.nb.seen = True
            fwd = v.entry                                # the direction is the starting intersection's
            while True:
                v = v.nxt if fwd else v.prv
                ring.append((v.x, v.y))
                if v.inter:
                    break
            v = v.nb
            guard += 1
            if v.seen or guard > 10000:
                break
        if len(ring) > 1 and abs(ring[0][0] - ring[-1][0]) < 1e-9 and abs(ring[0][1] - ring[-1][1]) < 1e-9:
            ring.pop()
        if len(ring) >= 3:
            out.append(ring)
    return out


def _sc_poly_and(S, C):
    """S ∩ C, perturbing S by a hair when a vertex falls on an edge (at most 6 tries)"""
    S = [tuple(p[:2]) for p in _sc_open(S)]
    C = [tuple(p[:2]) for p in _sc_open(C)]
    for k in range(6):
        r = _sc_gh(S, C)
        if r is not None:
            return r
        d = 1e-6 * (k + 1)
        S = [(p[0] + d * ((i * 7919) % 13 - 6) / 6.0, p[1] + d * ((i * 104729) % 11 - 5) / 5.0)
             for i, p in enumerate(S)]
    # last resort: keep the ring when its centre lies inside (logged by the caller's count)
    cx = sum(p[0] for p in S) / len(S)
    cy = sum(p[1] for p in S) / len(S)
    return [S] if _sc_pip(cx, cy, C) else []


def _sc_area(R):
    n = len(R)
    return 0.5 * sum(R[i][0] * R[(i + 1) % n][1] - R[(i + 1) % n][0] * R[i][1] for i in range(n))


def sc_rings_clip(R, rings, page=None):
    """a polygon (one ring, survey m) ∩ the study area: [ring, ...] (the study parts are separate: one result per
    part it reaches; Greiner-Hormann, non-convex both ways). A polygon that loses any area counts once for the page;
    one wholly outside returns []."""
    R = [tuple(p[:2]) for p in _sc_open(list(R))]
    if not rings or len(R) < 3:
        return [R] if len(R) >= 3 else []
    out = []
    for S in rings:
        out += [r for r in _sc_poly_and(R, S) if abs(_sc_area(r)) > 1e-6]
    a0 = abs(_sc_area(R))
    a1 = sum(abs(_sc_area(r)) for r in out)
    if a0 - a1 > max(1e-6, 1e-6 * a0):
        _sc_add(page, "rings", 1)
    return out


def sc_items(items, rings, page=None):
    """basemap-format items (common/basemap.py head) clipped to the study area: "fill" -> each ring through
    sc_rings_clip (holes clipped the same way, so an even-odd fill keeps them), "line" -> sc_lines runs, "text" ->
    kept only when its point is inside; "water" and anything else pass unchanged (they are base, not proposals).
    Returns the new item list."""
    if not rings:
        return list(items)
    out = []
    for it in items:
        k = it[0]
        if k == "fill":
            rs = [r for R in it[1] if len(R) >= 3 for r in sc_rings_clip(R, rings, page)]
            if rs:
                out.append(("fill", rs) + tuple(it[2:]))
        elif k == "line":
            for run in sc_lines(it[1], rings, page):
                out.append(("line", run) + tuple(it[2:]))
        elif k == "text":
            if sc_inside(it[2], rings):
                out.append(it)
            else:
                _sc_add(page, "points", 1)
        else:
            out.append(it)
    return out


def sc_cell_mask(G, V=None, rings=None):
    """a bytearray over the masterplan Grid G (G.nx x G.ny): 1 where the cell's centre lies in the study area
    (rings, else V.study); every grid-traced proposal requires mask[n] (PLAN §3 CHK-7 call sites)"""
    rings = rings if rings is not None else (getattr(V, "study", None) or sc_rings())
    m = bytearray(G.nx * G.ny)
    for R in rings or ():
        for n in G.poly_cells([tuple(p[:2]) for p in _sc_open(list(R))]):
            m[n] = 1
    return m


def sc_lines_log():
    """this run's per-page clip lines, then emptied: "study clip <page>: n_outside_clipped=<n> (points a, lines b,
    rings c)"; a FLAG line when no study area was found"""
    out = []
    for pg in sorted(SC_COUNT):
        c = SC_COUNT[pg]
        if pg == u"_flag":
            out.append(u"FLAG study clip: no study area (calisma_alan) in the basemap file or the script: nothing was "
                       u"clipped (run the site board once)")
            continue
        out.append(u"study clip %s: n_outside_clipped=%d (points %d, lines %d, rings %d)"
                   % (pg, c["points"] + c["lines"] + c["rings"], c["points"], c["lines"], c["rings"]))
    SC_COUNT.clear()
    return out
# ---- Map layers (round 4 S2, 1 Nov 2026; G-R4-4 "base map back, our drawings in front", D9 tint; PLAN §4.3) ---------
# ONE draw-order function for every map, plan and axo (p02, p06, p08, p10, p12, p16, p17, p20, p21, p22 and every key
# map): the base map muted, light and at the bottom; our drawings saturated and on top; the study line in its own
# layer above the project fills; proposals clipped to the study area at draw time too (study_clip.py) and counted.
# Included by common/basemap.py (its last lines, after study_clip.py); do not include it again.
# Items: the basemap format (common/basemap.py head), survey m (or already projected, e.g. an axo: then T = identity).
# Round 5 (S2, 1 Nov 2026; G-R5-8 "water drawn above every zone tint", G-R5-10 "base muted and cropped"): two layers
# after the project tints, "water" (the base stream) and "structures" (decks, covered course, bridges over it); a flat
# base list is filed by each item's layer (basemap _BmIt) so the stream lands in "water"; a base dict's "base_water"
# is drawn as "water" too; map_draw logs `zones <page> over_water_area <m2>, unlabeled_fields <n>`; ml_base crops.
#   ML_LAYERS                                   the 15 layers, bottom first
#   ml_base(box, scale_den, D=None, contours=False, names=False, override=None, crop=True)  the muted base (basemap
#                                               "muted"), cut to box (round 5, G-R5-10)
#   ml_crop(items, ring)                        round 5: items cut to a convex ring (survey m): fills, lines, water
#   ml_layer_of(item)                           round 5: the ML layer a base item belongs to
#   ml_tint(rings, colour=None, alpha=None, study=None, page=None)    D9 footprint tint items (clipped to the study)
#   ml_study_items(rings=None, D=None)          the study-area line items (BM_STUDY_LINE, one style everywhere)
#   map_draw(page, T, fill_fn, line_fn, text_fn, base, project, study=None, clip=True, order_fn=None, log=None,
#            water_opts=None, study_line=True, legend_cols=None, water_ok=None)
#                                               draws base -> project strictly in ML_LAYERS order; logs the done-when
#                                               line "layers base→project ok, n_outside_clipped <n> (<page>)" and
#                                               round 5 "zones <page> over_water_area <m2>, unlabeled_fields <n>"
# round 5 (S2, G-R5-8; PLAN §3 draw order: base fills -> tints / zone fields -> WATER -> structures over water ->
# planting -> people -> labels): "water" and "structures" follow "proj_tint"; the old names keep their places so
# stage lists that check the order (water board p12) still pass
ML_LAYERS = ("base_ground", "base_contours", "base_fills", "base_water", "base_outlines", "base_names",
             "proj_tint", "water", "structures", "proj_water", "proj_lines", "proj_vegetation", "study", "proj_marks",
             "proj_labels")
ML_BASE_LAYERS = ("base_ground", "base_contours", "base_fills", "base_water", "base_outlines", "base_names", "water",
                  "structures")
ML_PROJ_LAYERS = ("proj_tint", "proj_water", "proj_lines", "proj_vegetation", "study", "proj_marks", "proj_labels")
ML_FIELD_LAYERS = ("proj_lines", "proj_vegetation", "proj_marks")   # fills here are drawn above the stream
# D9 (Aras 1 Nov, U52 "çok hafif izdüşüm ... transparan çok hafif bir renkle"): the proposal footprint tint, very
# light and transparent, on every plan that shows proposals (p08, p10 plans, p12, p16, p17, p21, p22)
ML_TINT = "5C7A86"                  # palette reference slate (library/examples/palettes)
ML_TINT_ALPHA = 0.16
ML_NAME_MM = 2.12                   # base names 6 pt (the booklet minimum, G-R4-1), BM_MUTED["name"] tone
ML_NO_CLIP = ("proj_labels",)       # labels are placed by the text placer and may sit just outside the line
ML_LOG = []                         # this run's map_draw lines (a page script appends them to its log)


def ml_base(box, scale_den, D=None, contours=None, names=None, override=None, crop=True, mode="context", ring=None,
            civic=False, stream_name=True):
    """the base of a map. Round 9 (S3, G9-4; A1 C2): mode "context" (the default) = the map context layers a-j
    (basemap mode "context": land cover over the whole window, terrain, buildings by fabric, streets in hierarchy on
    top, the stream and "SELİNOS ÇAYI", bridges and their names, main street / mahalle / place names), every item
    tagged .layer / .ctx / .cls; log it with basemap_context_log and list it with basemap_legend_rows. mode "muted"
    = the round 4 muted base (G-R4-4): contours=True adds the contours coloured to the relief, names=True the pale
    6 pt names. contours / names None = the mode's own setting (context: both on; muted: both off). The study line
    is NOT in it (map_draw draws it in its own layer). box = (x0, y0, x1, y1) survey m; scale_den = the map's
    1:scale_den; ring = the map's window as a convex ring in survey m (e.g. frames_r9 r9_window on the frame axes):
    the unmapped ground fills it and crop cuts to it (default: the box). civic = False / True / OSM values (e.g.
    ("school",)): the civic rows of the names table this map names (only where it names buildings of that kind);
    stream_name=False on p3. Returns basemap items (bottom first), [] without basemap data. Round 5 (G-R5-10):
    crop=True cuts every item to the window, so nothing of the base runs past the drawing's window."""
    ov = {}
    if contours is not None:
        ov["contours"] = ("height" if mode == "muted" else True) if contours else False
    if names is not None:
        ov["names"] = bool(names)
    ov.update(override or {})
    opts = dict(civic=civic if isinstance(civic, bool) else tuple(civic), stream_name=bool(stream_name))
    if ring:
        opts["ring"] = tuple((round(float(p[0]), 3), round(float(p[1]), 3)) for p in ring)
    its = basemap_items(mode, ov, box=box, D=D, scale_den=scale_den, opts=opts)
    if mode == "muted":
        its = [_bm_tag(("text", it[1], it[2], ML_NAME_MM, BM_MUTED["name"], False, it[6]), "base_names")
               if it[0] == "text" else it for it in its]
    if crop and (ring or box):
        its = ml_crop(its, [tuple(p) for p in ring] if ring else
                      [(box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])])
    return its

def _ml_clip_poly(R, ring):
    """ring R cut to the convex ring (Sutherland-Hodgman, any turn); [] when nothing is left"""
    n = len(ring)
    ccw = sum((ring[(i + 1) % n][0] - ring[i][0]) * (ring[(i + 1) % n][1] + ring[i][1]) for i in range(n)) < 0
    out = list(R)
    for i in range(n):
        a, b = ring[i], ring[(i + 1) % n]
        ex, ey = b[0] - a[0], b[1] - a[1]

        def side(p):
            c = ex * (p[1] - a[1]) - ey * (p[0] - a[0])
            return c if ccw else -c
        if not out:
            return []
        nxt = []
        for j in range(len(out)):
            p, q = out[j - 1], out[j]
            sp, sq = side(p), side(q)
            if sq >= 0:
                if sp < 0:
                    t = sp / (sp - sq)
                    nxt.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
                nxt.append(q)
            elif sp >= 0:
                t = sp / (sp - sq)
                nxt.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
        out = nxt
    return out if len(out) >= 3 else []


def _ml_inside_convex(P, ring):
    n = len(ring)
    ccw = sum((ring[(i + 1) % n][0] - ring[i][0]) * (ring[(i + 1) % n][1] + ring[i][1]) for i in range(n)) < 0
    for i in range(n):
        a, b = ring[i], ring[(i + 1) % n]
        for p in P:
            c = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
            if (c if ccw else -c) < 0:
                return False
    return True


def _ml_retag(src, t):
    lay = getattr(src, "layer", None)          # round 9: the context letter and class travel with the layer
    return _bm_tag(t, lay, getattr(src, "ctx", None), getattr(src, "cls", None)) if lay else t


def ml_crop(items, ring):
    """round 5 (S2, G-R5-10): basemap items cut to the convex ring (survey m, e.g. a key map's turned frame):
    fills ring by ring (a ring wholly inside is kept as it is), lines run by run, the "water" item ring by ring,
    texts kept when their point is inside. Each item keeps its map layer."""
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    bb = (min(xs), min(ys), max(xs), max(ys))

    def rings_cut(Rs):
        out = []
        for R in Rs:
            if len(R) < 3:
                continue
            if _ml_inside_convex(R, ring):
                out.append(R)
                continue
            rx, ry = [p[0] for p in R], [p[1] for p in R]
            if max(rx) < bb[0] or min(rx) > bb[2] or max(ry) < bb[1] or min(ry) > bb[3]:
                continue
            c = _ml_clip_poly(R, ring)
            if c:
                out.append(c)
        return out
    out = []
    for it in items:
        if it[0] == "fill":
            rs = rings_cut(it[1])
            if rs:
                out.append(_ml_retag(it, ("fill", rs) + tuple(it[2:])))
        elif it[0] == "line":
            P = it[1]
            if _ml_inside_convex(P, ring):
                out.append(it)
                continue
            for a, b in zip(P, P[1:]):
                ab = _bm_clip_convex(a, b, ring)
                if ab:
                    out.append(_ml_retag(it, ("line", [ab[0], ab[1]]) + tuple(it[2:])))
        elif it[0] == "water":
            gs = []
            for g in it[1]:
                c = rings_cut([g[0]])
                if c:
                    gs.append(c + rings_cut(g[1:]))
            if gs:
                es = []
                for P in it[2]:
                    for a, b in zip(P, P[1:]):
                        ab = _bm_clip_convex(a, b, ring)
                        if ab:
                            es.append([ab[0], ab[1]])
                out.append(_ml_retag(it, ("water", gs, es) + tuple(it[3:])))
        elif it[0] == "text":
            if _ml_inside_convex([it[2]], ring):
                out.append(it)
        else:
            out.append(it)
    return out


def ml_layer_of(it):
    """round 5 (S2, G-R5-8): the map layer of a base item: its own (basemap _BmIt.layer), else by kind (the stream
    item and the base water tones -> "water", texts -> "base_names", the rest "base_fills")"""
    lay = getattr(it, "layer", None)
    if lay in ML_BASE_LAYERS:
        return "water" if lay == "base_water" else lay
    if it[0] == "water":
        return "water"
    if it[0] == "text":
        return "base_names"
    wc = (BM_COL["water"], BM_COL["water_edge"], BM_KEY["water"], BM_KEY["water_edge"])
    if it[0] in ("fill", "line") and it[2] in wc:
        return "water"
    return "base_fills"


def _ml_pip(x, y, R):
    ins = False
    j = len(R) - 1
    for i in range(len(R)):
        xi, yi = R[i]
        xj, yj = R[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi:
            ins = not ins
        j = i
    return ins


def _ml_over_water(fills, water, T=None, n=12):
    """round 5 (S2, G-R5-8): the area (m², or page mm² when the items are already projected) of fills that lie
    over the water rings, estimated on an n x n grid per fill ring (even-odd inside both)"""
    if not fills or not water:
        return 0.0
    wb = [(R, (min(p[0] for p in R), min(p[1] for p in R), max(p[0] for p in R), max(p[1] for p in R)))
          for R in water if len(R) >= 3]
    area = 0.0
    for it in fills:
        for R in it[1]:
            if len(R) < 3:
                continue
            x0, y0 = min(p[0] for p in R), min(p[1] for p in R)
            x1, y1 = max(p[0] for p in R), max(p[1] for p in R)
            if not any(not (b[2] < x0 or b[0] > x1 or b[3] < y0 or b[1] > y1) for _, b in wb):
                continue
            dx, dy = (x1 - x0) / n, (y1 - y0) / n
            hit = 0
            for i in range(n):
                for j in range(n):
                    x, y = x0 + (i + 0.5) * dx, y0 + (j + 0.5) * dy
                    if _ml_pip(x, y, R) and any(b[0] <= x <= b[2] and b[1] <= y <= b[3] and _ml_pip(x, y, W)
                                                for W, b in wb):
                        hit += 1
            area += hit * dx * dy
    return area


def ml_tint(rings, colour=None, alpha=None, study=None, page=None):
    """D9: the light transparent footprint of what we change (channel setbacks, ponds, basins, terraces, store, new
    paths) as fill items, one per ring, clipped to the study rings (study_clip sc_rings_clip) when study is given.
    rings: [ring, ...] survey m (or page mm with study=None). Put them in map_draw's "proj_tint" layer."""
    col, a = colour or ML_TINT, ML_TINT_ALPHA if alpha is None else alpha
    out = []
    for R in rings or ():
        if len(R) < 3:
            continue
        for r in (sc_rings_clip(R, study, page) if study else [R]):
            out.append(("fill", [r], col, a, True))
    return out


def ml_study_items(rings=None, D=None):
    """the study-area outline as line items, ONE style everywhere (BM_STUDY_LINE: violet long-dash-dot, U18/U19);
    rings default = the basemap's study area"""
    st = BM_STUDY_LINE
    rings = rings if rings is not None else basemap_study(D)
    return [("line", list(R) + [R[0]], st["colour"], st["width_mm"], list(st["dash_mm"]), 1.0)
            for R in rings or () if len(R) >= 3]


def map_draw(page, T, fill_fn, line_fn, text_fn, base, project, study=None, clip=True, order_fn=None, log=None,
             water_opts=None, study_line=True, legend_cols=None, water_ok=None):
    """THE draw order of every map (G-R4-4 done-when). page: the booklet page id ("p21"); T(p) survey m -> page
    point (identity for items already projected); fill_fn / line_fn / text_fn as basemap_draw. base: the base items
    (ml_base, in their own order) or {base layer: items}; project: {layer: items} or [(layer, items)] with layers
    from ML_PROJ_LAYERS ("proj_tint", "proj_water", "proj_lines", "proj_vegetation", "proj_marks", "proj_labels");
    study: the study rings (sc_rings): with clip=True every project item except labels is clipped to them
    (sc_items) and counted; the study line goes in the "study" layer (study_line=False leaves it out, e.g. a key map
    that draws its own). order_fn(layer): called before each layer is drawn (the site board's page order numbers:
    base 2-28, tint 30-39, project 40-59, marks 60-69). Draws strictly in ML_LAYERS order, whatever order the
    caller listed. Returns dict(n_base, n_project, n_outside_clipped, layers) and logs (ML_LOG and log) "layers
    base→project ok, n_outside_clipped <n> (<page>)".
    Round 5 (S2, G-R5-8): the base stream is drawn in "water", above "proj_tint" (a flat base list is filed by
    ml_layer_of; a base dict's "base_water" goes to "water"), decks / covered course / bridges in "structures". Logs
    `zones <page> over_water_area <m2>, unlabeled_fields <n>`: over_water_area = fills in proj_lines /
    proj_vegetation / proj_marks (drawn above the stream) over the base water, minus fills whose colour is in
    water_ok (fields in the water by design: widened stream, wetland, sub-hub, spillway, reed arms); unlabeled_fields
    = tint and field fills whose colour is not in legend_cols (the legend's swatch colours; "n/a" + a FLAG when the
    page passes none). A count above 0 is a WARNING line (the run goes on)."""
    if isinstance(base, dict):
        bad = [k for k in base if k not in ML_BASE_LAYERS]
        if bad:
            raise ValueError(u"map_draw %s: base layer(s) %s unknown: use %s" % (page, bad, ", ".join(ML_BASE_LAYERS)))
        bd = {}
        for k in ML_BASE_LAYERS:
            if base.get(k):
                bd.setdefault("water" if k == "base_water" else k, []).extend(base[k])
        base_l = [(k, bd[k]) for k in ML_BASE_LAYERS if bd.get(k)]
    else:
        bd = {}
        for it in base or []:
            bd.setdefault(ml_layer_of(it), []).append(it)
        base_l = [(k, bd[k]) for k in ML_BASE_LAYERS if bd.get(k)]
    proj = {}
    for k, its in (project.items() if isinstance(project, dict) else (project or [])):
        if k not in ML_PROJ_LAYERS or k == "study":
            raise ValueError(u"map_draw %s: project layer %r unknown: use %s" % (page, k, ", ".join(
                l_ for l_ in ML_PROJ_LAYERS if l_ != "study")))
        proj.setdefault(k, []).extend(its or [])
    if study and clip:
        for k in list(proj):
            if k not in ML_NO_CLIP:
                proj[k] = sc_items(proj[k], study, page)
    if study and study_line:
        proj["study"] = ml_study_items(study)
    n_out = sc_count(page)                               # this page's clips this run: at the source + here
    nb = npj = 0
    drawn = []
    for layer in ML_LAYERS:
        its = dict(base_l).get(layer) if layer in ML_BASE_LAYERS else proj.get(layer)
        if not its:
            continue
        if order_fn is not None:
            order_fn(layer)
        n = basemap_draw(its, T, fill_fn, line_fn, text_fn, water_opts)
        drawn.append(layer)
        if layer in ML_BASE_LAYERS:
            nb += n
        else:
            npj += n
    ok = all(ML_LAYERS.index(a) < ML_LAYERS.index(b) for a, b in zip(drawn, drawn[1:]))
    line = (u"layers base→project %s, n_outside_clipped %d (%s: %s)"
            % (u"ok" if ok else u"FLAG out of order", n_out, page, u", ".join(drawn)))
    ML_LOG.append(line)
    if log is not None:
        log.append(line)
    # round 5 (S2, G-R5-8): the zones done-when line
    wrings = basemap_water_rings(dict(base_l).get("water") or [])
    wrings += [R for it in dict(base_l).get("water") or [] if it[0] == "fill" and it[2] not in
               (BM_COL["water"],) for R in it[1] if len(R) >= 3]
    ok_c = set(str(c).upper() for c in (water_ok or ()))
    above = [it for k in ML_FIELD_LAYERS for it in proj.get(k) or []
             if it[0] == "fill" and str(it[2]).upper() not in ok_c]
    ow = _ml_over_water(above, wrings)
    tints = [it for k in ("proj_tint",) + ML_FIELD_LAYERS for it in proj.get(k) or [] if it[0] == "fill"]
    if legend_cols is None:
        nu = u"n/a"
    else:
        lc = set(str(c).upper() for c in legend_cols)
        nu = sum(1 for it in tints if str(it[2]).upper() not in lc)
    zl = u"zones %s over_water_area %d, unlabeled_fields %s" % (page, int(round(ow)), nu)
    extra = []
    if ow > 0.5 or (nu != u"n/a" and nu > 0):
        extra.append(u"WARNING %s zones over_water_area %d, unlabeled_fields %s" % (page, int(round(ow)), nu))
    if nu == u"n/a" and tints:
        extra.append(u"FLAG zones %s: no legend colours passed, unlabeled fields not counted" % page)
    for l_ in [zl] + extra:
        ML_LOG.append(l_)
        if log is not None:
            log.append(l_)
    return dict(n_base=nb, n_project=npj, n_outside_clipped=n_out, layers=drawn, over_water_area=ow,
                unlabeled_fields=nu)


def ml_lines_log():
    """this run's map_draw lines, then emptied"""
    out = list(ML_LOG)
    del ML_LOG[:]
    return out
# ---- Key maps, cut symbol, north arrow (round 4 S2, 1 Nov 2026; G-R4-9, R01, U02 U31 U50 U51 U55 U60) -----------------
# ONE key-map module: the page's cuts in the R01 symbol in red (an end bar with an open triangle standing on it
# pointing the way the section looks, a dash-dot line between), the main street and place names, ONE north arrow (the
# arrow and "N", no plate, U31 U51). Included by common/basemap.py (its last lines, after map_layers.py); do not
# include it again. History: round 4 v1 (R01 red), round 5 v2 (base mode "keymap", items for the booklet), round 6 v3
# (closed study rings, gaps between cut marks), round 7 v4 below. Items: the basemap format (common/basemap.py head).
# Key-map mm: origin at the key map's lower-left, y up.
# ROUND 7 (S1, 5 Nov 2026; G7-3, BRIEF D2 exception; PLAN §4.3): v4 = SON page8's key map REUSED (Aras 08:59 "AND
# REPLACE THE KEYMAPS", 09:00 "no reuse the old keymap"): _t3_sec_key (1d6f866 p07_09_movement.py:1556-1727) on keymap
# v2, made callable with (page, cuts, frame w x h). Where round 6's v3 differed, SON page8 wins: the map on the site
# frame's own axes (no turn to the corridor), names 6B645B 6 pt (4 pt floor), frame line INK2 0.15 mm on white, the
# north arrow 4 mm OUTSIDE the frame in a 9 mm column, a heading above, base "keymap" as is (round 6's strong recolour
# gone). Its only fix: the study outline = closed rings, never clipped (the frame's content holds every ring).
# The frame is the page's SON key-map frame EXACTLY (no fitting of the frame; one uniform scale fills it). Removed:
# km_map, km_texts, _km_strong, _km_axis_deg, KM_CUT_PLAN, the round 3 wrappers basemap_cut_items / keymap_items.
#   km_keymap(page, cuts=None, w_mm=None, h_mm=None, heading=None, zooms=None, log=None, cut_ids=None, looks=None,
#             north_side="right", extra_names=None, D=None)       THE call (cuts: registry ids and / or explicit cuts)
#   km_draw_to(km, X, fill_fn, line_fn, text_fn)    draw on a board / page;  km_export_items(km, page, item_id)
#   km_log(page)                                     `keymap <page> module cuts=<ids> study_closed=1 parts=<n>`
#   km_cut_items(cuts, scale_den, frame=None, style=None, text_mm=None)    R01 cut symbols as items (survey m)
#   km_cut_marks(cuts, den, frame=None, gap_mm=1.5, T=None, box_mm=None, page=None, log=None, per_cut=False)
#   km_study_ring(D=None, rings=None)                the study outline: closed rings, overlapping parts unioned
#   km_street_names(D, T, obstacles, vb=..., ...)    the street / place names, placed clear of obstacles
#   km_draw(km, X, ...) / km_items(km, page, item_id, priority)   the drawing and export behind km_draw_to /
#                                                    km_export_items
#   north_items(x, y, ang_rad=0.0, size_mm=6.0, colour="2C2219")   THE north arrow (page mm, y up)
# Also includes the round 6 shared tables and marks (one include for every script that has basemap.py):
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
# ---- Plan annotations (round 6 S1, 4 Nov 2026; G6-4; PLAN.md §2.4, §2.8) -------------------------------------------
# The marks on every PLAN except key maps (Aras 4 Nov 09:32, refs/targets/r06_R01 poster: "much cleaner and keeps the
# drawings clean"): a section cut = a small filled triangle (2.0 mm) + its letter at each end, just outside the
# drawing's frame, with a short dashed stub (4 mm) on the cut's line and NO line across the plan; a level = a tiny
# crosshair 1.6 mm + "+0.00" at 5 pt (round 7); a view mark = a small open triangle + a short name; the north arrow plain and
# solid, no box. Replaces the red / grey cut lines across plans of rounds 3-5 (KM_CUT_PLAN, km_cut_items on plans).
# Included by common/keymap.py (every script that includes basemap.py has it). Page mm, y up. Every function returns
# its items (the basemap format: "fill" / "line" / "text") and, when X is given, draws them through it:
#   X = (fill_fn, line_fn, text_fn) as basemap_draw takes them, in page mm; T = survey m -> page mm (None: the
#   points are page mm already); frame = the drawing's frame (x0, y0, x1, y1) page mm.
#   an_cut(X, a_xy, b_xy, letter, frame, T, look=1, names=None)   the two end marks of one cut
#   an_level(X, xy, value_m, T)                                    one level mark (value in m, 2 decimals)
#   an_view(X, xy, dir_deg, name, frame, T)                        one view mark
#   an_north(X, xy, north_deg, size_mm=6)                          the north arrow
#   an_name(X, xy, text, T=None, page=None)                        a small name inside its area (round 7)
#   an_list(X, frame, rows, page=None)                             a list in the side column (round 7)
#   an_log(page, n_cuts=None, n_levels=None, log=None)             `annot <page> <kind> <n>` per kind
# ROUND 7 (S1, 5 Nov 2026; G7-2, PLAN §4.4; target refs/targets/r06_R01 poster): an_level is now a tiny crosshair +
# "+0.00" (was a quartered circle); an_name and an_list added (names small inside their area, lists in the side
# column); an_cut, an_view, an_north unchanged. Every plan except key maps and the masterplan page uses these only.
import math as _an_m

AN_CUT = dict(tri_mm=2.0, stub_mm=4.0, gap_mm=1.0, stub_lw=0.18, dash=(0.8, 0.5), text_mm=2.12)   # 6 pt letters
AN_LEVEL = dict(d_mm=1.6, lw=0.12, text_mm=1.764, gap_mm=0.6)          # round 7: crosshair 1.6 mm, "+0.00" 5 pt
AN_NAME = dict(text_mm=1.764, colour="2C2219")                         # round 7: names inside their area, 5 pt
AN_LIST = dict(text_mm=1.764, lead=1.35, key_gap_mm=1.0, colour="2C2219")   # round 7: side-column list, 5 pt
AN_VIEW = dict(tri_mm=2.0, lw=0.18, text_mm=1.764, gap_mm=0.8)
AN_COUNT = {}                          # page -> {"cuts": n, "levels": n, "views": n, "names": n, "lists": n}
AN_LOG = []


def _an_col(name):
    t = globals().get("HUE_ANN")
    return (t or {}).get(name) or {"cut": "8E8F8A", "ink": "2C2219"}[name]


def _an_out(items, X):
    if X:
        fill_fn, line_fn, text_fn = (tuple(X) + (None, None, None))[:3]
        basemap_draw(items, lambda p: p, fill_fn, line_fn, text_fn)
    return items


def _an_add(page, kind):
    if page is not None:
        c = AN_COUNT.setdefault(page, {"cuts": 0, "levels": 0, "views": 0, "names": 0, "lists": 0})
        c[kind] += 1


def _an_frame_hits(a, b, frame):
    """where the endless line through a, b crosses the frame rectangle: the two points (lowest t first) or None"""
    x0, y0, x1, y1 = frame
    ux, uy = b[0] - a[0], b[1] - a[1]
    ts = []
    for v, p0, d in ((x0, a[0], ux), (x1, a[0], ux)):
        if abs(d) > 1e-12:
            t = (v - p0) / d
            y = a[1] + uy * t
            if y0 - 1e-9 <= y <= y1 + 1e-9:
                ts.append(t)
    for v, p0, d in ((y0, a[1], uy), (y1, a[1], uy)):
        if abs(d) > 1e-12:
            t = (v - p0) / d
            x = a[0] + ux * t
            if x0 - 1e-9 <= x <= x1 + 1e-9:
                ts.append(t)
    if len(ts) < 2:
        return None
    t0, t1 = min(ts), max(ts)
    if t1 - t0 < 1e-9:
        return None
    return (a[0] + ux * t0, a[1] + uy * t0), (a[0] + ux * t1, a[1] + uy * t1)


def an_cut(X, a_xy, b_xy, letter, frame, T=None, look=1, names=None, page=None):
    """the G6-4 cut mark of one section: a_xy, b_xy = the cut's ends (end1 = the section's left end, look +1 = the
    viewer stands so end1 is on the left, as km_cut_items); letter "A" -> ends "A" and "A'" (names = (n1, n2) to give
    both). At each place where the cut's line leaves the frame: a dashed stub stub_mm long outward (gap_mm off the
    frame), at its outer end a filled triangle tri_mm pointing the way the section looks, the letter beyond it along
    the line. Nothing is drawn across the plan. Returns the items (page mm); a cut whose line misses the frame
    returns [] with a WARNING in AN_LOG."""
    a = T(a_xy) if T else tuple(a_xy)
    b = T(b_xy) if T else tuple(b_xy)
    hit = _an_frame_hits(a, b, frame)
    n1, n2 = names or (letter, letter + u"'")
    if hit is None:
        AN_LOG.append(u"WARNING %s annot cut %s: its line misses the drawing frame, no mark drawn" % (page or u"", n1))
        return []
    p1, p2 = hit
    if (p1[0] - a[0]) * (b[0] - a[0]) + (p1[1] - a[1]) * (b[1] - a[1]) > (p2[0] - a[0]) * (b[0] - a[0]) + \
            (p2[1] - a[1]) * (b[1] - a[1]):
        p1, p2 = p2, p1                                  # p1 on end1's side
    L = _an_m.hypot(p2[0] - p1[0], p2[1] - p1[1])
    ux, uy = (p2[0] - p1[0]) / L, (p2[1] - p1[1]) / L
    fx, fy = -uy * look, ux * look                       # the way the section looks (as km_cut_items)
    st, ink, grey = AN_CUT, _an_col("ink"), _an_col("cut")
    out = []
    for p, nm, sg in ((p1, n1, -1.0), (p2, n2, 1.0)):
        s0 = (p[0] + ux * sg * st["gap_mm"], p[1] + uy * sg * st["gap_mm"])
        s1 = (p[0] + ux * sg * (st["gap_mm"] + st["stub_mm"]), p[1] + uy * sg * (st["gap_mm"] + st["stub_mm"]))
        out.append(("line", [s0, s1], grey, st["stub_lw"], list(st["dash"]), 1.0))
        h = st["tri_mm"]
        tri = [(s1[0] + ux * h * 0.5, s1[1] + uy * h * 0.5), (s1[0] - ux * h * 0.5, s1[1] - uy * h * 0.5),
               (s1[0] + fx * h * 0.87, s1[1] + fy * h * 0.87)]
        out.append(("fill", [tri], ink, 1.0, True))
        off = h * 0.5 + 0.6 + st["text_mm"] * 0.45 * max(1, len(nm))
        out.append(("text", nm, (s1[0] + ux * sg * off, s1[1] + uy * sg * off), st["text_mm"], ink, True, "MC"))
    _an_add(page, "cuts")
    return _an_out(out, X)


def an_level(X, xy, value_m, T=None, page=None):
    """the G7-2 level mark (round 7; poster r06_R01): a tiny crosshair AN_LEVEL d_mm across at xy (two hairlines,
    no circle, no fill), its value "+0.00" (m, 2 decimals, signed) at 5 pt to the right. Returns the items (page
    mm)."""
    c = T(xy) if T else tuple(xy)
    st, ink = AN_LEVEL, _an_col("ink")
    r = st["d_mm"] / 2.0
    out = [("line", [(c[0] - r, c[1]), (c[0] + r, c[1])], ink, st["lw"], None, 1.0),
           ("line", [(c[0], c[1] - r), (c[0], c[1] + r)], ink, st["lw"], None, 1.0)]
    v = u"%+.2f" % float(value_m)
    out.append(("text", v, (c[0] + r + st["gap_mm"], c[1]), st["text_mm"], ink, False, "ML"))
    _an_add(page, "levels")
    return _an_out(out, X)


def an_view(X, xy, dir_deg, name, frame=None, T=None, page=None):
    """the G6-4 view mark: a small open triangle at xy pointing dir_deg (degrees, counter-clockwise from page east),
    the short name behind it (away from where it looks). A mark inside the frame is moved onto the frame's edge
    behind it, so the mark stays outside the drawing. Returns the items (page mm)."""
    c = T(xy) if T else tuple(xy)
    st, ink = AN_VIEW, _an_col("ink")
    ux, uy = _an_m.cos(_an_m.radians(dir_deg)), _an_m.sin(_an_m.radians(dir_deg))
    if frame and frame[0] < c[0] < frame[2] and frame[1] < c[1] < frame[3]:
        hit = _an_frame_hits(c, (c[0] + ux, c[1] + uy), frame)
        if hit:
            c = hit[0]                                   # the edge behind the mark
            c = (c[0] - ux * (st["gap_mm"] + st["tri_mm"]), c[1] - uy * (st["gap_mm"] + st["tri_mm"]))
    h = st["tri_mm"]
    tip = (c[0] + ux * h * 0.5, c[1] + uy * h * 0.5)
    bl = (c[0] - ux * h * 0.5 - uy * h * 0.5, c[1] - uy * h * 0.5 + ux * h * 0.5)
    br = (c[0] - ux * h * 0.5 + uy * h * 0.5, c[1] - uy * h * 0.5 - ux * h * 0.5)
    out = [("line", [tip, bl, br, tip], ink, st["lw"], None, 1.0)]
    off = h * 0.5 + st["gap_mm"] + st["text_mm"] * 0.3 * max(1, len(name))
    out.append(("text", name, (c[0] - ux * off, c[1] - uy * off), st["text_mm"], ink, False, "MC"))
    _an_add(page, "views")
    return _an_out(out, X)


def an_north(X, xy, north_deg, size_mm=6.0):
    """the G6-4 north arrow: keymap.north_items (a plain solid arrowhead on a shaft and "N", no plate or box) with its
    foot at xy, north turned north_deg (degrees, counter-clockwise from page-up). Placed by the caller outside the
    drawing. Returns the items (page mm)."""
    return _an_out(north_items(xy[0], xy[1], ang_rad=_an_m.radians(north_deg), size_mm=size_mm,
                               colour=_an_col("ink")), X)


def an_name(X, xy, text, T=None, page=None):
    """the G7-2 name (round 7): a small name (AN_NAME, 5 pt, regular) centred at xy inside its area (the caller
    gives a point inside the area it names). Returns the items (page mm); the booklet moves it if it hits."""
    c = T(xy) if T else tuple(xy)
    out = [("text", u"%s" % text, c, AN_NAME["text_mm"], AN_NAME["colour"], False, "MC")]
    _an_add(page, "names")
    return _an_out(out, X)


def an_list(X, frame, rows, page=None):
    """the G7-2 side-column list (round 7): rows top-down from the top-left of frame (x0, y0, x1, y1) page mm, y up;
    a row = "text" or (key, text): the key bold (a number or letter matching a mark on the plan), the text after it
    (AN_LIST, 5 pt, line pitch 1.35). Every row is drawn: rows below the frame's bottom stay (never dropped) with a
    WARNING in AN_LOG. Returns the items (page mm)."""
    st = AN_LIST
    x0, y0, x1, y1 = frame
    pitch = st["text_mm"] * st["lead"]
    fmw = globals().get("fm_width")
    out = []
    y = y1 - 0.5 * st["text_mm"]
    for r in rows:
        key, txt = (r[0], r[1]) if isinstance(r, (tuple, list)) else (None, r)
        x = x0
        if key is not None and u"%s" % key:
            k = u"%s" % key
            out.append(("text", k, (x, y), st["text_mm"], st["colour"], True, "ML"))
            kw = fmw(k, st["text_mm"] / 0.352778, bold=True) if callable(fmw) else 0.6 * st["text_mm"] * len(k)
            x += kw + st["key_gap_mm"]
        out.append(("text", u"%s" % txt, (x, y), st["text_mm"], st["colour"], False, "ML"))
        y -= pitch
    if y + pitch - 0.5 * st["text_mm"] < y0:
        AN_LOG.append(u"WARNING %s annot list: %d rows reach %.1f mm below the frame bottom (all drawn)"
                      % (page or u"", len(rows), y0 - (y + pitch - 0.5 * st["text_mm"])))
    _an_add(page, "lists")
    return _an_out(out, X)


def an_log(page, n_cuts=None, n_levels=None, log=None):
    """round 7: one line per kind, `annot <page> <kind> <n>` (cut, level, view, name, list); counts default to what
    the an_* functions drew for page this run (n_cuts / n_levels override). Returns the lines joined by newlines."""
    c = dict(AN_COUNT.get(page) or {})
    if n_cuts is not None:
        c["cuts"] = n_cuts
    if n_levels is not None:
        c["levels"] = n_levels
    lns = [u"annot %s %s %d" % (page, k[:-1], c.get(k, 0)) for k in ("cuts", "levels", "views", "names", "lists")]
    lg = log if log is not None else AN_LOG
    lg.extend(lns)
    return u"\n".join(lns)
# ---- Collect, clean, hold: the numbered elements 1-11 and their places (round 6 S1, 4 Nov 2026; PLAN.md §2.8, §5) --
# ONE source for the numbers of the water chain, so p11 (Collect, clean, hold), p12 (the proposals in section,
# "1-11 as in Collect, clean, hold"), p17 (the plant ladder) and p20 (the masterplan) give the same element the same
# number (BRIEF §6 rows 11, 12, 20; P7). Numbering = the 28 Oct chain, the one Aras judged best:
# -> f93d84b:src/bergama_water_board/code.py:724-737 (CHAIN). Places = the zone base zones (dicts with "code",
# "ring" survey m, "study_area"), as the water board p11 map picks them -> src/bergama_water_board/pages/
# p12_system.py:552 (_p12_pick), 1611-1617 (the winter store point), 1851-1868 (the step markers).
# Included by common/keymap.py (every script that includes basemap.py has it).
#   CCH_STEPS                      {n: (name, zone code or None)} for n = 1..11
#   cch_points(zones, area="aras", log=None)   {n: (x, y) survey m or None, "store": xy, "spill": xy}
#   cch_name(n)                    the element's short name
CCH_STEPS = {
    1: (u"Stream in · mostly winter", None),                       # the upstream entry (CCH_ENTRY)
    2: (u"Reed beds clean it", "WT"),
    3: (u"Terraces hold street + roof runoff", "WS"),
    4: (u"Planted basins store winter water", "store"),            # the winter store: middle of WS + WT
    5: (u"Spillway: overflow back to the stream", "WD"),
    6: (u"Summer strip 4 m x 0.30 m", None),                       # in the bed: no zone of its own
    7: (u"Strip waters the bank planting", "WP"),
    8: (u"Floods spread onto terraces", "WA"),
    9: (u"People on the raised dry top", "DG"),
    10: (u"The clean stream leaves the site", None),               # the downstream end (CCH_EXIT)
    11: (u"Existing farmland outside the site", None),             # outside the study area: a page arrow, no point
}
# the chain's two ends, survey m: the surveyed cut centres of the upstream entry and the downstream end (as
# p12_system.py P12_PLACES, from masterplan parts/02b_detail.py CUT_AT = water board CUTS)
CCH_ENTRY = (29693.022, 32569.176)
CCH_EXIT = (30991.856, 31039.404)
CCH_LOG = []


def cch_name(n):
    return CCH_STEPS[int(n)][0]


def _cch_cen(R):
    """the area centroid of a ring (the water board's _p12_cen)"""
    a = cx = cy = 0.0
    n = len(R)
    for i in range(n):
        (xa, ya), (xb, yb) = R[i][:2], R[(i + 1) % n][:2]
        f = xa * yb - xb * ya
        a += f
        cx += (xa + xb) * f
        cy += (ya + yb) * f
    if abs(a) < 1e-12:
        return (sum(p[0] for p in R) / n, sum(p[1] for p in R) / n)
    return (cx / (3.0 * a), cy / (3.0 * a))


def cch_points(zones, area="aras", log=None):
    """the place of each numbered element (survey m): the centroid of the first zone of its code in `area` (a
    study_area prefix; None = any area); 4 = the winter store = the mean centroid of every WS and WT zone of that
    area (as the p11 map's HOLD point); 1 / 10 = the chain's entry / exit points; 6 and 11 have no place (None: a
    page draws them as a strip / arrow or leaves them out). Also "store" (= 4) and "spill" (= 5). Logs
    `cch points <found>/<11> missing=<numbers>`; a number whose zone is missing is None, never guessed."""
    log = log if log is not None else CCH_LOG

    def pick(code):
        return [z for z in zones or () if z.get("code") == code and z.get("ring") and
                (area is None or (z.get("study_area") or u"").startswith(area))]
    out = {}
    for n, (_nm, code) in CCH_STEPS.items():
        if code is None or code == "store":
            out[n] = None
            continue
        zs = pick(code)
        out[n] = _cch_cen(zs[0]["ring"]) if zs else None
    up = pick("WS") + pick("WT")
    out[4] = (sum(_cch_cen(z["ring"])[0] for z in up) / len(up), sum(_cch_cen(z["ring"])[1] for z in up) / len(up)) \
        if up else None
    out[1], out[10] = CCH_ENTRY, CCH_EXIT
    out["store"], out["spill"] = out[4], out[5]
    miss = [n for n in CCH_STEPS if out[n] is None and n not in (6, 11)]
    log.append(u"cch points %d/11 missing=%s" % (sum(1 for n in CCH_STEPS if out[n] is not None),
                                                 u",".join(str(n) for n in miss) or u"-"))
    return out
import math as _km_m

# R01 in red (G-R4-9): line 0.5 mm dash-dot; end bar 2.4 mm along the line at each end, the open triangle standing on
# it (base = the bar, height tri_h, apex the way the section looks), the end name beyond the bar. Sizes: drawing rules
# of PLAN §4.5 (the triangle's base is the bar so it never overhangs it).
# Round 9 (S4, G9-5 b; PLAN.md §spec S4): the line SOLID (dash None), 0.5 mm C0392B, open triangle each end.
KM_CUT = dict(colour="C0392B", lw=0.5, dash=None, end_bar=2.4, bar_lw=0.6, tri_h=2.1, tri_lw=0.35,
              text_mm=2.47, gap_mm=0.8)
KM_NAMES = dict(streets=("main",), n_streets=4, places=True, n_places=6, size_mm=4.0 * 0.352778, colour="A4A1A3",
                bold=False, pad_mm=0.6)     # round 9 (S4, G9-5 a): small and light, 4 pt A4A1A3 (HUE_KEY street_names)
KM_NAMES_MIN = 4.0 * 0.352778    # round 7: a name with no room at 6 pt tries 4 pt (the floor), never smaller
KM_MIN_L = 1.0           # mm: round 6 (from the site board's T3_KEY_MIN_L): a cut's line between its end bars at least
#                          this long on the key map (a street is 10-20 m wide, under 2 mm at a key map's scale)
KM_GAP = 1.5             # mm: round 6 (G6-5 "gaps"): neighbouring cut marks keep at least this apart
KM_SHRINK = (1.0, 0.75, 0.55)      # round 6: symbol sizes tried when two marks would touch
KM_ZOOM = dict(colour="C0392B", lw=0.35)       # zoom / window frames on a key map: the cut red, solid
KM_FRAME = dict(colour="7A6E60", lw=0.15)      # round 7 (G7-3): SON page8's frame line (site board INK2 0.15 mm)
KM_PAPER = "FFFFFF"      # round 7: SON page8 fills the map's rectangle white under the base
KM_NA = 9.0              # mm: the north box (round 9, A1 C8: INSIDE the frame's top-right corner, min(KM_NA, 0.9 h))
KM_NORTH_MM = 4.0        # mm: SON page8's north arrow height (na_h)
KM_HEAD = dict(size_mm=7.5 * 0.352778, colour="4A3F35", gap_mm=1.5)   # SON page8 heading: 7.5 pt bold INK, 1.5 mm gap
KM_PAD = 1.0             # mm: inner pad between the frame and the content (round 6 fitted map's pad)
KM_MARGIN = 0.02         # share of the content added on each side (round 6 fitted map's margin)
KM_LOG = []
KM_LEG = dict(w_mm=4.0, h_mm=2.4, pt=5.0)   # round 9 (S4, G9-5 d): the one key-map legend: swatch 4 x 2.4 mm, text 5 pt


class _KmMain(tuple):
    """round 9 (S4): a cut's main line among its symbol items (reads as the plain tuple everywhere)"""
    pass


def km_cut_items(cuts, scale_den, frame=None, style=None, text_mm=None):
    """R01 cut symbols (G-R4-9) as items in survey m. cuts = [(end1, end2, (name1, name2)[, look])] (as
    basemap_cut_ids gives them: end1 = the section's left end, look +1 = the viewer stands so end1 is on the left,
    -1 the other way); scale_den: the key map's 1:scale_den (mm sizes -> m); frame: a convex polygon the symbols stay
    inside (the line is cut to it and pulled in so bars and names fit). Per cut: the dash-dot line end to end, at each
    end the bar and the open triangle pointing the look direction, the end's name beyond the bar (bold)."""
    st = dict(KM_CUT)
    st.update(style or {})
    tm = text_mm or st["text_mm"]
    m = scale_den / 1000.0                               # survey m per key-map mm
    col = st["colour"]
    out = []
    for c in cuts:
        a, b, names = c[0], c[1], c[2]
        look = c[3] if len(c) > 3 and isinstance(c[3], (int, float)) else 1   # v32 (L1): a look given as text = +1
        L0 = _km_m.hypot(b[0] - a[0], b[1] - a[1])
        if L0 < 1e-6:
            continue
        ux, uy = (b[0] - a[0]) / L0, (b[1] - a[1]) / L0
        if frame:
            ab = _bm_clip_convex(a, b, frame)
            if ab is None:
                continue
            a, b = ab
            pull = (st["gap_mm"] + tm * 0.6 * max(len(names[0]), len(names[1]), 1)) * m
            L = _km_m.hypot(b[0] - a[0], b[1] - a[1])
            if L <= 2.0 * pull + 2.0 * st["end_bar"] * m:   # 2 Nov fix: too short for its end names: no longer
                n0 = names[0]                                 # dropped; drawn without them, its first name beside
                names = (u"", u"")                            # the middle (km_keymap's id label goes on the other side)
                pull = st["gap_mm"] * m
                mx_, my_ = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
                if L <= 2.0 * pull + 2.0 * st["end_bar"] * m:   # shorter than the symbol: its least length, centred
                    hl = pull + st["end_bar"] * m + 0.5 * m
                    a, b = (mx_ - ux * hl, my_ - uy * hl), (mx_ + ux * hl, my_ + uy * hl)
                if n0:
                    off_ = tm * 1.2 * m
                    out.append(("text", n0, (mx_ + uy * off_, my_ - ux * off_), tm, col, True, "MC"))
            a = (a[0] + ux * pull, a[1] + uy * pull)
            b = (b[0] - ux * pull, b[1] - uy * pull)
        fx, fy = -uy * look, ux * look                   # the way the section looks
        out.append(_KmMain(("line", [a, b], col, st["lw"], list(st["dash"]) if st.get("dash") else None, 1.0)))
        bar, th = st["end_bar"] * m, st["tri_h"] * m
        for p, nm, sgn in ((a, names[0], -1.0), (b, names[1], 1.0)):
            q = (p[0] - ux * sgn * bar, p[1] - uy * sgn * bar)          # the bar runs from the end inward
            out.append(("line", [p, q], col, st["bar_lw"], None, 1.0))
            mid = ((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0)
            tri = [p, q, (mid[0] + fx * th, mid[1] + fy * th), p]
            out.append(("line", tri, col, st["tri_lw"], None, 1.0))      # open triangle standing on the bar
            off = (st["gap_mm"] + tm * 0.3 * max(1, len(nm))) * m     # beyond the end, clear of the bar
            t = (p[0] + ux * sgn * off, p[1] + uy * sgn * off)
            if nm:
                out.append(("text", nm, t, tm, col, True, "MC"))
    return out


def _km_box_hit(b, boxes, pad=0.0):
    for o in boxes:
        if not (b[2] + pad <= o[0] or b[0] - pad >= o[2] or b[3] + pad <= o[1] or b[1] - pad >= o[3]):
            return True
    return False


def _km_seg_hit(b, segs, pad):
    x0, y0, x1, y1 = b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad
    for p, q in segs:
        L = _km_m.hypot(q[0] - p[0], q[1] - p[1])
        n = max(1, int(L / 0.4))
        for i in range(n + 1):
            x, y = p[0] + (q[0] - p[0]) * i / n, p[1] + (q[1] - p[1]) * i / n
            if x0 <= x <= x1 and y0 <= y <= y1:
                return True
    return False


def km_street_names(D, T, obstacles, vb=None, frame_mm=None, segs=(), Tinv=None, names=None, extra_names=None,
                    page=None, log=None):
    """round 6 (S1, G6-5), round 7 (G7-3: SON page8's names, KM_NAMES 6B645B 6 pt, else KM_NAMES_MIN 4 pt): the
    key map's names: the main streets (OpenStreetMap names by the names table's spelling, street_label), the names
    table's key-map places (keymap_places), then extra_names [(name, xy)]; each placed at its point or the nearest
    of six spots clear of obstacles (key-map mm boxes; the placed names are added to it), segs (key-map mm
    segments) and the frame (frame_mm = (w, h)); a name with no free place is set on its point at 4 pt and logged
    (the booklet moves it; never left out). T / Tinv: survey
    m <-> key-map mm; vb: the survey box the names are taken from. Returns dict(items (survey m text items), labels
    (dicts as km_keymap's), label_boxes)."""
    log = log if log is not None else KM_LOG
    nm_st = dict(KM_NAMES)
    nm_st.update(names or {})
    pg = page or u""
    w_mm, h_mm = frame_mm
    boxes = obstacles
    fmw = globals().get("fm_width")
    pt_of = lambda mm: mm / 0.352778
    label_boxes, labels = [], []
    cand = []
    stl = globals().get("street_label")
    if nm_st.get("streets"):
        for n, p, _a, _cl, _ln in basemap_street_names(vb, D, classes=tuple(nm_st["streets"]))[:4 * nm_st["n_streets"]]:
            cand.append((stl(n) if callable(stl) else n, p, "street"))
    if nm_st.get("places"):
        kp = globals().get("keymap_places")
        if callable(kp):
            for n, p, _k in kp(vb):
                cand.append((n, p, "place"))
        else:
            log.append(u"FLAG keymap %s: common/names.py not included: no place names (never a raw survey name)" % pg)
    for n, p in extra_names or ():
        cand.append((n, tuple(p), "extra"))
    if cand and not callable(fmw):
        raise RuntimeError(u"km_keymap needs common/font_metrics.py (round 4 S1: fm_width) included before it is "
                           u"called: text widths come from the real font only")
    sz = nm_st["size_mm"]
    pad_n = nm_st["pad_mm"]
    name_items, placed, seen_n = [], {"street": 0, "place": 0, "extra": 0}, set()
    lim = {"street": nm_st["n_streets"], "place": nm_st["n_places"], "extra": 10 ** 6}
    for n, p, kind in cand:
        if placed[kind] >= lim[kind] or n in seen_n:
            continue
        x, y = T(p)
        if not (0.0 <= x <= w_mm and 0.0 <= y <= h_mm):
            continue
        ok = None
        for sz_ in [sz] + ([KM_NAMES_MIN] if sz > KM_NAMES_MIN + 1e-6 else []):   # round 7: 6 pt, else the 4 pt floor
            w = fmw(n, pt_of(sz_), bold=nm_st["bold"])
            for dx, dy in ((0.0, 0.0), (0.0, sz_ * 1.1), (0.0, -sz_ * 1.1), (w / 2.0 + 1.0, 0.0),
                           (-w / 2.0 - 1.0, 0.0), (0.0, sz_ * 2.2), (0.0, -sz_ * 2.2)):
                b = (x + dx - w / 2.0, y + dy - sz_ / 2.0, x + dx + w / 2.0, y + dy + sz_ / 2.0)
                if b[0] < pad_n or b[1] < pad_n or b[2] > w_mm - pad_n or b[3] > h_mm - pad_n:
                    continue
                if _km_box_hit(b, boxes, pad_n) or _km_seg_hit(b, segs, pad_n):
                    continue
                ok = b
                break
            if ok is not None:
                break
        if ok is None:                                    # 4 Nov (Aras 19:17 "not drawing ... is not a solution"):
            ok = (x - w / 2.0, y - sz_ / 2.0, x + w / 2.0, y + sz_ / 2.0)   # set on its point (4 pt), handed to the
            ok = (max(pad_n, min(ok[0], w_mm - pad_n - w)), max(pad_n, min(ok[1], h_mm - pad_n - sz_)))   # booklet,
            ok = (ok[0], ok[1], ok[0] + w, ok[1] + sz_)                     # which moves it off whatever it hits
            log.append(u"keymap %s: name '%s' set on its point (no free place here; the booklet places it)" % (pg, n))
        seen_n.add(n)
        boxes.append(ok)
        label_boxes.append((n, ok))
        placed[kind] += 1
        name_items.append(("text", n, Tinv(((ok[0] + ok[2]) / 2.0, (ok[1] + ok[3]) / 2.0)), sz_, nm_st["colour"],
                           nm_st["bold"], "MC"))
        labels.append(dict(string=n, kind=kind, anchor=(x, y), box=ok, size_mm=sz_, colour=nm_st["colour"],
                           bold=nm_st["bold"]))
    return dict(items=name_items, labels=labels, label_boxes=label_boxes)


def km_draw(km, X, fill_fn, line_fn, text_fn, water_opts=None, page=None, log=None, frame=True):
    """draws a km_keymap (PLAN §3 order: paper, base, WATER, structures, the study line, the red cuts, names, then the
    frame line, the north arrow (round 9: inside the frame's top-right corner) and the heading above the frame): X(q) key-map mm -> page point (e.g. lambda q: (x0 + q[0], y0 + q[1]), or a
    y-down flip). frame=False leaves out the paper, the frame line and the arrow (a caller that draws its own).
    text_fn=None draws no text (the booklet places the labels from km_items). Returns map_draw's dict."""
    T = km["T"]
    if frame:
        basemap_draw(km["frame_items"][:1], X, fill_fn, line_fn, None)
    r = map_draw(page or u"key", lambda p: X(T(p)), fill_fn, line_fn, text_fn, km["base"],
                 {"proj_marks": [it for it in km["cuts"] if it[0] != "text"],
                  "proj_labels": [it for it in km["cuts"] if it[0] == "text"] + km["names"]},
                 study=km.get("study_rings"), clip=False, log=log, water_opts=water_opts)
    if frame:
        basemap_draw(km["frame_items"][1:] + km["north"] + list(km.get("heading_items") or ()), X, fill_fn, line_fn,
                     text_fn)
    return r


def km_items(km, page=None, item_id=None, priority=5):
    """round 5 (S2, G-R5-12; PLAN §4 item schema v1, Aras's addendum 1 Nov 22:37 point 3): the key map as items for
    the booklet: one "drawing" (layers of shapes in key-map mm, y up, origin lower-left; texts left out), one "text"
    item per label (names and cut labels, role "label", with its anchor in the drawing and the module's placement as
    hint_box), one "keymap" item (cut ids, looks, zooms, names, fill, rotation). Round 7 (G7-3): the drawing is the
    frame EXACTLY (w_mm x h_mm); the north arrow is its own "drawing" item "<id>.north" (role "north", outside=True,
    anchor = its lower-left in the key map's mm, outside the frame) and the heading a "text" item "<id>.head" (role
    "heading", anchor = its left middle above the frame); the "N" is a label of kind "north" anchored outside too. Shapes: {"type": "poly", "rings",
    "fill", "opacity", "nonzero"} and {"type": "line", "pts", "stroke", "width_pt", "dash_pt", "opacity"}."""
    pg = page if page is not None else km.get("page")
    did = item_id or (u"keymap_%s" % (pg or u"key"))
    layers, cur = [], {"name": None}

    def layer(name):
        cur["name"] = name
        layers.append(dict(z=len(layers), name=name, shapes=[]))

    def fill_fn(rings, col, alpha, nonzero):
        if cur["name"] is None:
            layer("base")
        layers[-1]["shapes"].append(dict(type="poly", rings=[[[round(p[0], 3), round(p[1], 3)] for p in R]
                                                             for R in rings], fill=col, opacity=alpha,
                                         nonzero=bool(nonzero), grp=u"keymap/%s" % cur["name"]))   # round 9: G6-9

    def line_fn(pts, col, w_mm, dash_mm, alpha):
        if cur["name"] is None:
            layer("base")
        layers[-1]["shapes"].append(dict(type="line", pts=[[round(p[0], 3), round(p[1], 3)] for p in pts],
                                         stroke=col, width_pt=round(w_mm / 0.352778, 3),
                                         dash_pt=[round(d_ / 0.352778, 3) for d_ in dash_mm] if dash_mm else None,
                                         opacity=alpha, grp=u"keymap/%s" % cur["name"]))           # round 9: G6-9
    T = km["T"]
    layer("paper")
    basemap_draw(km["frame_items"][:1], lambda q: q, fill_fn, line_fn, None)
    map_draw(u"%s key map" % (pg or u""), T, fill_fn, line_fn, None, km["base"],
             {"proj_marks": [it for it in km["cuts"] if it[0] != "text"]}, study=km.get("study_rings"),
             clip=False, order_fn=layer)
    layer("frame")
    basemap_draw(km["frame_items"][1:], lambda q: q, fill_fn, line_fn, None)
    nb = km.get("north_box") or (km["w_mm"], 0.0, km["w_mm"] + KM_NA, KM_NA)
    layer("north")                                       # round 9 (A1 C8): the north arrow inside the frame's top-right
                                                         # corner, still its own item (outside=True = BK routing)
    basemap_draw([it for it in km["north"] if it[0] != "text"], lambda q: (q[0] - nb[0], q[1] - nb[1]), fill_fn,
                 line_fn, None)
    nlay = layers.pop()
    nlay["z"] = 0
    for sh_ in nlay["shapes"]:
        sh_["grp"] = u"keymap/north"
    layers = [L_ for L_ in layers if L_["shapes"]]
    for i, L_ in enumerate(layers):
        L_["z"] = i
    w, h = km["w_mm"], km["h_mm"]
    out = [dict(id=did, page=pg, kind="drawing", role="keymap", priority=priority, group=did, units="mm",
                axes=u"key-map mm, origin lower-left, y up", size_mm=[round(w, 2), round(h, 2)], extent=[0.0, 0.0,
                                                                                                    round(w, 2),
                                                                                                    round(h, 2)],
                scale_pref=None, scale_den=round(km["scale_den"]), scale_bar=False, north_deg=km["north_deg"],
                layers=layers, keep_areas=[[0.0, 0.0, round(w, 2), round(h, 2)]], anchors={})]
    nw, nh = nb[2] - nb[0], nb[3] - nb[1]
    out.append(dict(id=u"%s.north" % did, page=pg, kind="drawing", role="north", priority=priority, group=did,
                    units="mm", axes=u"mm, origin lower-left, y up", size_mm=[round(nw, 2), round(nh, 2)],
                    extent=[0.0, 0.0, round(nw, 2), round(nh, 2)], scale_pref=None, scale_den=None, scale_bar=False,
                    north_deg=None, layers=[nlay], keep_areas=[[0.0, 0.0, round(nw, 2), round(nh, 2)]], anchors={},
                    anchor=dict(drawing=did, point=[round(nb[0], 2), round(nb[1], 2)]), outside=True))
    for t in km.get("heading_items") or ():               # round 7: the heading above the frame (SON page8)
        hb = km.get("heading_box")
        out.append(dict(id=u"%s.head" % did, page=pg, kind="text", role="heading", priority=priority, group=did,
                        string=t[1], label_kind="heading",
                        anchor=dict(drawing=did, point=[round(t[2][0], 2), round(t[2][1], 2)]),
                        hint_box=[round(v, 2) for v in hb] if hb else None, size_pt=round(t[3] / 0.352778, 2),
                        min_pt=4.0, bold=True, colour=t[4], short_forms=[], side_list_ok=False, justify=False,
                        grp=u"keymap/labels"))
    texts = [dict(string=t[1], kind="north", anchor=t[2], box=None, size_mm=t[3], colour=t[4], bold=t[5])
             for t in km["north"] if t[0] == "text"]
    for i, lb in enumerate(km["labels"] + texts):
        out.append(dict(id=u"%s.t%d" % (did, i), page=pg, kind="text", role="label", priority=priority, group=did,
                        string=lb["string"], label_kind=lb["kind"],
                        anchor=dict(drawing=did, point=[round(lb["anchor"][0], 2), round(lb["anchor"][1], 2)]),
                        hint_box=[round(v, 2) for v in lb["box"]] if lb["box"] else None,
                        size_pt=round(lb["size_mm"] / 0.352778, 2), min_pt=4.0, bold=bool(lb["bold"]),
                        colour=lb["colour"], short_forms=[], side_list_ok=False, justify=False,
                        grp=u"keymap/labels"))
    out.append(dict(id=u"%s.km" % did, page=pg, kind="keymap", role="keymap", priority=priority, group=did,
                    drawing=did, cuts=[dict(id=c, look=km["looks"].get(c, 1)) for c in km["cut_ids"]],
                    zooms=list(km["zoom_ids"]), names=[lb["string"] for lb in km["labels"] if lb["kind"] != "cut"],
                    fill=round(km["fill"], 3), rotation_deg=km["rotation_deg"], missing=list(km["missing"]),
                    classes=list(km.get("classes") or ()), roads=int(km.get("roads") or 0)))
    return out


def north_items(x, y, ang_rad=0.0, size_mm=6.0, colour="2C2219"):
    """THE north arrow (G-R4-9, U31 U51): only the arrow and "N", no plate or box behind it, as items in page mm
    (y up): a slim filled arrowhead on a short shaft, size_mm tall, "N" above its tip; (x, y) = the shaft's foot;
    ang_rad = north's turn from page-up, counter-clockwise. Draw with basemap_draw(items, lambda p: p, ...)."""
    c, s_ = _km_m.cos(ang_rad), _km_m.sin(ang_rad)

    def R(px, py):
        return (x + px * c - py * s_, y + px * s_ + py * c)
    h = size_mm
    hw = 0.22 * h
    head = [R(0.0, h), R(-hw, 0.55 * h), R(0.0, 0.66 * h), R(hw, 0.55 * h)]
    tm = max(2.12, 0.42 * h)                             # "N" at least 6 pt
    return [("line", [R(0.0, 0.0), R(0.0, 0.62 * h)], colour, max(0.18, 0.04 * h), None, 1.0),
            ("fill", [head], colour, 1.0, True),
            ("text", u"N", R(0.0, h + 0.75 * tm), tm, colour, True, "MC")]


# ---- round 6 (S1, 4 Nov 2026; G6-5): v3 ------------------------------------------------------------------------------
KM_STUDY_LOG = {}        # page -> (n rings, closed: 1/0) of its last key map


def km_study_ring(D=None, rings=None):
    """the study area (calisma_alan, "two closed parts worked as one") as the key map draws it: closed rings, survey
    m, the parts that overlap or cross unioned into one outline (study_clip._sc_gh union, perturbed and retried like
    _sc_poly_and when a vertex falls on an edge), holes of the union left out, parts that never meet kept as their
    own closed rings (the 25 Oct recorded copy's two parts are ~249 m apart: two rings; nothing is drawn between them
    that the survey does not hold). rings default = basemap_study(D)."""
    R0 = [[tuple(p[:2]) for p in _sc_open(R)] for R in (rings if rings is not None else basemap_study(D)) or ()
          if len(R) >= 3]
    out = []
    for R in R0:
        cur = R
        rest = []
        for Q in out:
            got = None
            S_ = list(cur)
            for k in range(6):
                got = _sc_gh(S_, Q, union=True)
                if got is not None:
                    break
                d = 1e-6 * (k + 1)
                S_ = [(p[0] + d * ((i * 7919) % 13 - 6) / 6.0, p[1] + d * ((i * 104729) % 11 - 5) / 5.0)
                      for i, p in enumerate(S_)]
            if got is None:
                rest.append(Q)                           # no clean union: both stay
                continue
            if len(got) == 2 and [tuple(p) for p in got[1]] == [tuple(p) for p in Q] and \
                    [tuple(p) for p in got[0]] == [tuple(p) for p in S_]:
                rest.append(Q)                           # apart: both stay, each closed
                continue
            cur = max(got, key=lambda G: abs(_sc_area(G)))      # the outer ring; holes left out
        out = rest + [cur]
    return out


def _km_seg_dist(p, q, r, t):
    """the least distance between segments pq and rt"""
    def pd(a, b, c):
        dx, dy = c[0] - b[0], c[1] - b[1]
        L = dx * dx + dy * dy
        u = 0.0 if L < 1e-18 else max(0.0, min(1.0, ((a[0] - b[0]) * dx + (a[1] - b[1]) * dy) / L))
        return _km_m.hypot(a[0] - b[0] - u * dx, a[1] - b[1] - u * dy)
    d1 = (q[0] - p[0], q[1] - p[1])
    d2 = (t[0] - r[0], t[1] - r[1])
    den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) > 1e-18:
        a = ((r[0] - p[0]) * d2[1] - (r[1] - p[1]) * d2[0]) / den
        b = ((r[0] - p[0]) * d1[1] - (r[1] - p[1]) * d1[0]) / den
        if 0.0 <= a <= 1.0 and 0.0 <= b <= 1.0:
            return 0.0
    return min(pd(p, r, t), pd(q, r, t), pd(r, p, q), pd(t, p, q))


def km_cut_marks(cuts, den, frame=None, gap_mm=None, T=None, box_mm=None, page=None, log=None, per_cut=False,
                 obstacles=(), segs=()):
    """round 6 (S1, G6-5; from the site board's _t3_sec_key, the p08 target): the key map's cuts, bold red across
    (km_cut_items, R01), cuts = [(end1, end2, (name1, name2), look)] survey m, den = the key map's 1:den. Each cut
    lengthened about its middle to KM_MIN_L between its end bars where it is shorter on the map; neighbouring marks
    kept gap_mm (KM_GAP) apart: a mark that would touch an earlier one is drawn smaller (KM_SHRINK), else drawn
    with a WARNING line; end names that would touch another cut, a name or leave the map (T survey m -> key-map mm,
    box_mm = (w, h)) become ONE name beside the cut's middle (3.5-12 mm out, either side; none free = WARNING, set at
    the first spot). Returns the items (survey m), or per cut a list of items (per_cut=True). Round 9 (S4, G9-5 b,
    H3 §2): the size test checks the end symbols only; a cut parallel to an earlier one and closer than gap_mm is
    drawn aside by the missing distance (a log line); a cut whose line crosses an earlier cut's line is broken gap_mm
    each side of the crossing (a WARNING line); names keep clear of obstacles (key-map mm boxes, e.g. the north box)
    and segs (key-map mm segments, e.g. the study line) as well."""
    log = log if log is not None else KM_LOG
    gap = KM_GAP if gap_mm is None else float(gap_mm)
    m = den / 1000.0
    Tm = T or (lambda p: (p[0] / m, p[1] / m))
    fmw = globals().get("fm_width")
    pg = page or u""

    def tbox(it):
        x, y = Tm(it[2])
        w = fmw(it[1], it[3] / 0.352778, bold=it[5]) if callable(fmw) else 0.6 * it[3] * len(it[1])
        return (x - w / 2.0, y - it[3] / 2.0, x + w / 2.0, y + it[3] / 2.0)

    def segs_of(its):
        out_ = []
        for it in its:
            if it[0] == "line":
                P = [Tm(p) for p in it[1]]
                out_ += list(zip(P, P[1:]))
        return out_

    def inside(b):
        if not box_mm:
            return True
        return b[0] >= 0.6 and b[1] >= 0.6 and b[2] <= box_mm[0] - 0.6 and b[3] <= box_mm[1] - 0.6

    def cross_t(p, q, r, t):
        """round 9: the share along p-q where it crosses r-t, or None"""
        d1, d2 = (q[0] - p[0], q[1] - p[1]), (t[0] - r[0], t[1] - r[1])
        dn = d1[0] * d2[1] - d1[1] * d2[0]
        if abs(dn) < 1e-12:
            return None
        u_ = ((r[0] - p[0]) * d2[1] - (r[1] - p[1]) * d2[0]) / dn
        v_ = ((r[0] - p[0]) * d1[1] - (r[1] - p[1]) * d1[0]) / dn
        return u_ if 0.0 <= u_ <= 1.0 and 0.0 <= v_ <= 1.0 else None
    min_l = (2.0 * KM_CUT["end_bar"] + KM_MIN_L) * m
    done, done_segs, tboxes = [], [], list(obstacles or ())
    done_main, extra = [], list(segs or ())
    for c in cuts:
        a, b, nm = tuple(c[0]), tuple(c[1]), tuple(c[2])
        look = c[3] if len(c) > 3 and isinstance(c[3], (int, float)) else 1
        L0 = _km_m.hypot(b[0] - a[0], b[1] - a[1]) or 1e-6
        ux, uy = (b[0] - a[0]) / L0, (b[1] - a[1]) / L0
        if L0 < min_l:
            cx_, cy_ = 0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1])
            a, b = (cx_ - 0.5 * min_l * ux, cy_ - 0.5 * min_l * uy), (cx_ + 0.5 * min_l * ux, cy_ + 0.5 * min_l * uy)
        pa, pb = Tm(a), Tm(b)                            # round 9: parallel and too close to an earlier cut: aside
        for ea, eb, enm in done_main:
            if cross_t(pa, pb, ea, eb) is not None:
                continue
            d_ = _km_seg_dist(pa, pb, ea, eb)
            v1, v2 = (pb[0] - pa[0], pb[1] - pa[1]), (eb[0] - ea[0], eb[1] - ea[1])
            cs_ = abs(v1[0] * v2[0] + v1[1] * v2[1]) / max(1e-9, _km_m.hypot(*v1) * _km_m.hypot(*v2))
            if d_ >= gap or cs_ < 0.98:
                continue
            sh_ = (gap - d_ + 0.1) * m
            best = None
            for sgn in (1.0, -1.0):
                a2 = (a[0] - sgn * uy * sh_, a[1] + sgn * ux * sh_)
                b2 = (b[0] - sgn * uy * sh_, b[1] + sgn * ux * sh_)
                d2 = _km_seg_dist(Tm(a2), Tm(b2), ea, eb)
                if best is None or d2 > best[0]:
                    best = (d2, a2, b2)
            a, b = best[1], best[2]
            pa, pb = Tm(a), Tm(b)
            log.append(u"keymap %s cut %s drawn %.1f mm aside (parallel to cut %s, gap %.1f mm)"
                       % (pg, nm[0], gap - d_ + 0.1, enm, gap))
        its, sg, crowd = None, None, False
        for k in KM_SHRINK:
            st = dict(end_bar=KM_CUT["end_bar"] * k, tri_h=KM_CUT["tri_h"] * k)
            its = km_cut_items([(a, b, nm, look)], den, frame=frame, style=st)
            sg = segs_of(its)
            sy = segs_of([it for it in its if not isinstance(it, _KmMain)])   # round 9: the end symbols only
            if not any(_km_seg_dist(p, q, r, t) < gap for p, q in sy for r, t in done_segs):
                if k != 1.0:
                    log.append(u"keymap %s cut %s drawn at %.0f %% size (gap to its neighbour)" % (pg, nm[0], k * 100))
                break
        else:                                        # v32 (L1, LAYOUT_PLAN §3.2-5): marks closer than the gap keep
            crowd = True                             # their smallest size and their NAMES are pushed apart (no WARNING)
            log.append(u"keymap %s cut %s closer than %.1f mm to a neighbour: drawn at %.0f %% size, its name pushed "
                       u"clear of the neighbour" % (pg, nm[0], gap, KM_SHRINK[-1] * 100))
        mains = [it for it in its if isinstance(it, _KmMain)]   # round 9: crossings break this cut's line
        if mains:
            P0, P1 = mains[0][1][0], mains[0][1][-1]
            q0, q1 = Tm(P0), Tm(P1)
            Lmm = _km_m.hypot(q1[0] - q0[0], q1[1] - q0[1]) or 1e-6
            ts = []
            for ea, eb, enm in done_main:
                t_ = cross_t(q0, q1, ea, eb)
                if t_ is not None:
                    ts.append(t_)
                    log.append(u"WARNING keymap %s cuts %s and %s cross: the line of %s is broken %.1f mm each side "
                               u"of the crossing" % (pg, enm, nm[0], nm[0], gap))
            if ts:
                dt, keep, s0 = gap / Lmm, [], 0.0
                for t_ in sorted(ts):
                    if t_ - dt > s0:
                        keep.append((s0, t_ - dt))
                    s0 = max(s0, t_ + dt)
                if s0 < 1.0:
                    keep.append((s0, 1.0))
                lp = lambda f: (P0[0] + (P1[0] - P0[0]) * f, P0[1] + (P1[1] - P0[1]) * f)
                its = [_KmMain(("line", [lp(f0), lp(f1)]) + tuple(mains[0][2:])) for f0, f1 in keep] + \
                      [it for it in its if not isinstance(it, _KmMain)]
            done_main.append((q0, q1, nm[0]))
        others = list(done_segs) + extra
        tx = [tbox(it) for it in its if it[0] == "text"]
        if tx and (crowd or not all(inside(bb) and not _km_box_hit(bb, tboxes, 0.6) and not _km_seg_hit(bb, others, 0.6)
                          for bb in tx)):
            its = [it for it in its if it[0] != "text"]
            nx, ny = -(b[1] - a[1]) / L0, (b[0] - a[0]) / L0
            mid = (0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1]))
            got = None
            for strict in (True, False):                 # clear of every cut line first, else of the texts only
                for off in (3.5, 5.0, 6.5, 8.0, 10.0, 12.0, 15.0, 18.0, 22.0):   # v32: further out before giving up
                    for sgn in (-1.0, 1.0):
                        it = ("text", nm[0], (mid[0] + sgn * nx * off * m, mid[1] + sgn * ny * off * m),
                              KM_CUT["text_mm"], KM_CUT["colour"], True, "MC")
                        bb = tbox(it)
                        if inside(bb) and not _km_box_hit(bb, tboxes, 0.6) and not (
                                strict and _km_seg_hit(bb, others + sg, 0.6)):
                            got = (it, bb)
                            break
                    if got:
                        break
                if got:
                    if not strict:
                        log.append(u"keymap %s: the name of cut %s crosses another cut's line (no clear place)"
                                   % (pg, nm[0]))
                    break
            if got is None:
                log.append(u"keymap %s: the name of cut %s set at its first spot (no free place here; the booklet "
                           u"places it)" % (pg, nm[0]))
                it = ("text", nm[0], (mid[0] - nx * 3.5 * m, mid[1] - ny * 3.5 * m), KM_CUT["text_mm"],
                      KM_CUT["colour"], True, "MC")
                got = (it, tbox(it))
            its.append(got[0])
            tx = [got[1]]
            log.append(u"keymap %s: cut %s named once beside its middle (its end names had no room)" % (pg, nm[0]))
        tboxes += tx
        done_segs += sg
        done.append(its)
    return done if per_cut else [it for its in done for it in its]


def _km_frame_deg(P):
    """round 7 (S1, G7-3): the site frame's own axis as SON page8 drew it (selinus_board Frame: the direction of the
    frame polygon's longest edge, degrees counter-clockwise from east, turned into (-90, 90]); 0.0 without a frame"""
    if not P or len(P) < 2:
        return 0.0
    best, ang = -1.0, 0.0
    for i in range(len(P)):
        q0, q1 = P[i], P[(i + 1) % len(P)]
        L = _km_m.hypot(q1[0] - q0[0], q1[1] - q0[1])
        if L > best:
            best, ang = L, _km_m.atan2(q1[1] - q0[1], q1[0] - q0[0])
    while ang > _km_m.pi / 2:
        ang -= _km_m.pi
    while ang <= -_km_m.pi / 2:
        ang += _km_m.pi
    return _km_m.degrees(ang)


def km_keymap(page, cuts=None, w_mm=None, h_mm=None, heading=None, zooms=None, log=None, cut_ids=None, looks=None,
              north_side="right", extra_names=None, D=None, names=None, frame_key=None, **legacy):
    """round 7 (S1, G7-3; PLAN §4.3): THE key map of every page = SON page8's "Where each street is cut" (_t3_sec_key,
    1d6f866 src/selinus_board/pages/p07_09_movement.py:1556-1727, on keymap v2 89097ee), callable with a page's cuts
    and its SON key-map frame. As SON page8: the map on the site frame's own axes (basemap_frame = site_alan, the
    longest edge along the page, no other turn); base mode "keymap" (green ground, houses by urban fabric, the stream
    blue, roads); the cuts in red R01 (km_cut_marks: end bars, triangles, end names or one name beside the middle,
    gaps between neighbours); main street and place names in 6B645B at SON's 6 pt, 4 pt where 6 pt finds no room
    (never smaller, never left out: a name with no free place is set on its point for the booklet); frame line INK2
    0.15 mm on white; the north arrow (4 mm, no plate) OUTSIDE the frame in a KM_NA column at the right (north_side
    "left": at the left); the heading 7.5 pt bold above the frame. Only fix (G7-3): the study area = closed rings
    (km_study_ring), never clipped: the map's content is every study ring plus the cuts and zooms, one uniform scale
    so that content fills w_mm x h_mm (pad KM_PAD, margin 2 %), the base cut to the frame.
    page: booklet page id ("p08"); cuts: a list of cut registry ids / zoom ids (strings, levels.py) and explicit cuts
    [(end1, end2, (name1, name2), look[, id])] survey m, mixed as needed (cut_ids: the same ids, round 6 name);
    w_mm x h_mm: the SON key-map frame of the page (PLAN §3, H4 §3) = the map's frame EXACTLY (one missing: from the
    content's aspect; both missing: 80 mm wide, WARNING); heading: the text above the frame (None = none); zooms {id:
    polygon survey m}: window frames in red; looks {id: +1/-1} for registry cuts; extra_names [(name, xy)].
    names (masterplan v45): KM_NAMES overrides for km_street_names, e.g. dict(streets=(), places=False) = no street or
    place names; None = KM_NAMES. Legacy options of round 6 (box, scale_den, rotate, fit, margin, pad_mm, legend_box,
    north ...) are ignored
    with a log line. Returns dict(base, study, cuts, names, items, box, scale_den, T, Tinv (survey m <-> key-map mm,
    origin lower-left, y up), drawn, missing, label_boxes, labels, w_mm, h_mm, study_rings, study_ring,
    study_closed, rotation_deg, rotation, north_deg, fill, frame, frame_items, north (key-map mm items, outside the
    frame), north_box, heading_items, heading_box, looks, zoom_ids, cut_ids, cuts_all, page). Logs
    `keymap <page> 1:<den> axes=<deg> frame=<w>x<h> fill=<f> cuts=<ids>` and km_log's `keymap <page> module ...`.
    Round 9 (S4, G9-5; A1 C7, C8): base = mode "keymap" = the context layers drawn quieter (every street class, land
    cover, buildings by fabric, the stream); names 4 pt A4A1A3; cuts solid, crossings broken, parallel cuts aside;
    the north arrow INSIDE the frame's top-right corner (north_side is ignored), its box kept clear by cut labels and
    names; every exported shape tagged keymap/<layer> (G6-9). frame_key = an R9_FRAMES key ("p04.2"): w_mm x h_mm
    from frames_r9 when not given. Adds km["classes"] (the base classes shown, for km_legend) and km["roads"] (the
    street lines drawn; km_log logs `keymap <page> roads n=<n> cuts <labels>`)."""
    log = log if log is not None else KM_LOG
    pg = u"%s" % (page or u"")
    for k in sorted(legacy):
        log.append(u"keymap %s: option %s ignored (round 7: SON page8 look, frame = w x h)" % (pg, k))
    D = D if D is not None else basemap_load()
    if frame_key and not (w_mm and h_mm) and callable(globals().get("r9_wh")):
        w_mm, h_mm = r9_wh(frame_key)                    # round 9: the key map drawn at its R9 frame size (fit = 1)
    ids, xcuts = list(cut_ids or ()), []
    for c in cuts or ():
        (ids if isinstance(c, str) else xcuts).append(c)
    if not ids and not xcuts and page is not None and callable(globals().get("level_registry_all")):
        ids = [e["id"] for e in level_registry_all(str(page))]
    cut_l, wins, drawn, missing, seen = [], [], [], [], set()
    win_fn = globals().get("level_window")
    for cid in ids:
        if zooms and cid in zooms:
            wins.append((cid, [tuple(p) for p in zooms[cid]]))
            drawn.append(cid)
            continue
        try:
            c = basemap_cut_ids([cid], looks)[0]
            ek = (round(c[0][0], 1), round(c[0][1], 1), round(c[1][0], 1), round(c[1][1], 1))
            if ek not in seen:                           # the crossings of one cut share one line
                seen.add(ek)
                cut_l.append((cid, c))
            drawn.append(cid)
            continue
        except Exception:
            pass
        try:
            w = win_fn(cid) if callable(win_fn) else None
            if w:
                wins.append((cid, [tuple(p) for p in w]))
                drawn.append(cid)
                continue
        except Exception:
            pass
        missing.append(cid)
        log.append(u"WARNING %s keymap '%s' is neither a cut of the registry nor a zoom passed in: not drawn."
                   % (pg, cid))
    for zid, w in (zooms or {}).items():                 # zooms passed in but not named in cuts: drawn too
        if zid not in drawn:
            wins.append((zid, [tuple(p) for p in w]))
            drawn.append(zid)
    for c in xcuts:                                      # explicit cuts (street cuts R1-R4 ...)
        cid = c[4] if len(c) > 4 and c[4] else c[2][0]
        cut_l.append((cid, (tuple(c[0]), tuple(c[1]), tuple(c[2]), c[3] if len(c) > 3 else 1)))
        drawn.append(cid)
    study = km_study_ring(D)
    cont = [p for R in study for p in R] + [p for _, c in cut_l for p in c[:2]] + [p for _, w in wins for p in w]
    if not cont:
        cont = list(basemap_extent(D) or [])
    if not cont:
        raise ValueError(u"key map %s: nothing to frame (no basemap data, no cuts)" % pg)
    # SON page8: the site frame's own axes (the p07 maps' View), north turned to match
    fr = basemap_frame(D) if D else None
    if not fr:
        log.append(u"WARNING %s keymap: no site frame in the basemap data: drawn north up" % pg)
    phi = -_km_frame_deg(fr)
    cph, sph = _km_m.cos(_km_m.radians(phi)), _km_m.sin(_km_m.radians(phi))
    bx0 = _bm_bb(cont)
    c0 = ((bx0[0] + bx0[2]) / 2.0, (bx0[1] + bx0[3]) / 2.0)

    def rot(p):
        dx, dy = p[0] - c0[0], p[1] - c0[1]
        return (dx * cph - dy * sph, dx * sph + dy * cph)

    def unrot(q):
        return (q[0] * cph + q[1] * sph + c0[0], -q[0] * sph + q[1] * cph + c0[1])
    rx0, ry0, rx1, ry1 = _bm_bb([rot(p) for p in cont])
    cw, ch = max(rx1 - rx0, 1.0), max(ry1 - ry0, 1.0)  # the content, m
    bw, bh = cw * (1.0 + 2.0 * KM_MARGIN), ch * (1.0 + 2.0 * KM_MARGIN)
    pad = KM_PAD
    if not w_mm and not h_mm:
        w_mm = 80.0
        log.append(u"WARNING %s keymap frame: no w x h given, drawn 80 mm wide" % pg)
    if not h_mm:
        h_mm = bh * (w_mm - 2.0 * pad) / bw + 2.0 * pad
    if not w_mm:
        w_mm = bw * (h_mm - 2.0 * pad) / bh + 2.0 * pad
    w_mm, h_mm = float(w_mm), float(h_mm)
    den = max(bw * 1000.0 / max(1.0, w_mm - 2.0 * pad), bh * 1000.0 / max(1.0, h_mm - 2.0 * pad))
    s = 1000.0 / den
    rcx, rcy = (rx0 + rx1) / 2.0, (ry0 + ry1) / 2.0

    def T(p):
        r = rot(p)
        return ((r[0] - rcx) * s + w_mm / 2.0, (r[1] - rcy) * s + h_mm / 2.0)

    def Tinv(q):
        return unrot(((q[0] - w_mm / 2.0) / s + rcx, (q[1] - h_mm / 2.0) / s + rcy))
    frame = [Tinv((0.0, 0.0)), Tinv((w_mm, 0.0)), Tinv((w_mm, h_mm)), Tinv((0.0, h_mm))]
    vb = _bm_bb(frame)
    base = basemap_items("keymap", box=vb, D=D, scale_den=den) if D else []
    base = ml_crop(base, frame) if base else []
    if D and D.get("format") != BASEMAP_FORMAT:
        log.append(u"FLAG keymap %s: basemap format %s has no urban fabric per house: one house tone until the site "
                   u"board writes format %d" % (pg, D.get("format"), BASEMAP_FORMAT))
    st_items = ml_study_items(study)
    # round 9 (A1 C8, H3 C8): the north arrow inside the frame's top-right corner, plain ink, set before the cuts so
    # their labels and the names keep clear of its box
    a_n = _km_m.radians(phi)
    n_box = min(KM_NA, 0.9 * h_mm)
    ncx, ncy = w_mm - 0.5 * n_box, h_mm - 0.5 * n_box
    n_size = min(KM_NORTH_MM, 0.5 * n_box)
    half = 0.5 * (n_size + 0.75 * max(2.12, 0.42 * n_size))
    north_its = north_items(ncx + half * _km_m.sin(a_n), ncy - half * _km_m.cos(a_n), ang_rad=a_n, size_mm=n_size,
                            colour=hue("ANN", "ink"))
    north_box = (w_mm - n_box, h_mm - n_box, w_mm, h_mm)
    st_segs = []
    for it in st_items:
        if it[0] == "line":
            P = [T(p) for p in it[1]]
            st_segs += list(zip(P, P[1:]))
    cut_items = []
    marks = km_cut_marks([c for _, c in cut_l], den, frame=frame, T=T, box_mm=(w_mm, h_mm), page=pg, log=log,
                         per_cut=True, obstacles=[north_box], segs=st_segs)
    nm_fn = globals().get("level_name")
    for (cid, c), its in zip(cut_l, marks):
        try:
            name = nm_fn(cid) if callable(nm_fn) else cid
        except Exception:
            name = cid
        name = (u"%s" % name).split("-")[0]              # a crossing row (S5-2) is labelled by its cut (S5)
        if not its:
            log.append(u"WARNING %s keymap cut %s too short inside the frame: not drawn" % (pg, cid))
        elif name not in c[2][0] and name not in c[2][1]:   # end names that do not say the id: the id too
            a, b = c[0], c[1]
            L0 = _km_m.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
            nx, ny = -(b[1] - a[1]) / L0, (b[0] - a[0]) / L0
            q = ((a[0] + b[0]) / 2.0 + nx * KM_CUT["text_mm"] * 1.2 / s, (a[1] + b[1]) / 2.0 + ny * KM_CUT["text_mm"]
                 * 1.2 / s)
            its.append(("text", name, q, KM_CUT["text_mm"], KM_CUT["colour"], True, "MC"))
        cut_items += its
    for cid, w in wins:
        cut_items.append(("line", list(w) + [w[0]], KM_ZOOM["colour"], KM_ZOOM["lw"], None, 1.0))
        x0, y0, x1, y1 = _bm_bb([T(p) for p in w])
        cut_items.append(("text", cid, Tinv((x0 + KM_CUT["text_mm"] * 0.9, y1 + KM_CUT["text_mm"] * 0.8)),
                          KM_CUT["text_mm"], KM_CUT["colour"], True, "MC"))
    fmw = globals().get("fm_width")
    pt_of = lambda mm: mm / 0.352778
    segs, boxes, label_boxes, labels = [], [], [], []
    for it in cut_items + st_items:
        if it[0] == "line":
            P = [T(p) for p in it[1]]
            segs += list(zip(P, P[1:]))
    for it in cut_items:
        if it[0] == "text":
            x, y = T(it[2])
            w = fmw(it[1], pt_of(it[3]), bold=it[5]) if callable(fmw) else 0.6 * it[3] * len(it[1])
            b = (x - w / 2.0, y - it[3] / 2.0, x + w / 2.0, y + it[3] / 2.0)
            boxes.append(b)
            label_boxes.append((it[1], b))
            labels.append(dict(string=it[1], kind="cut", anchor=(x, y), box=b, size_mm=it[3], colour=it[4],
                               bold=it[5]))
    boxes.append(north_box)                              # round 9: names keep clear of the north box
    heading_items, heading_box = [], None
    if heading:
        hs = KM_HEAD["size_mm"]
        yh = h_mm + KM_HEAD["gap_mm"] + 0.5 * hs
        heading_items = [("text", u"%s" % heading, (0.0, yh), hs, KM_HEAD["colour"], True, "ML")]
        hw = fmw(u"%s" % heading, pt_of(hs), bold=True) if callable(fmw) else 0.6 * hs * len(heading)
        heading_box = (0.0, yh - 0.5 * hs, hw, yh + 0.5 * hs)
    nr = km_street_names(D, T, boxes, vb=vb, frame_mm=(w_mm, h_mm), segs=segs, Tinv=Tinv, names=names,
                         extra_names=extra_names, page=pg, log=log)   # masterplan v45: names= passed (None = as before)
    labels += nr["labels"]
    label_boxes += nr["label_boxes"]
    fill = min(1.0, (cw * s) * (ch * s) / max(1e-9, (w_mm - 2.0 * pad) * (h_mm - 2.0 * pad)))
    rot_out = round(phi, 1)
    log.append(u"keymap %s 1:%.0f axes=%.1f frame=%.1fx%.1f fill=%.2f cuts=%s"
               % (pg, den, rot_out, w_mm, h_mm, fill, u",".join(cid for cid, _ in cut_l) or u"-"))
    if log is not KM_LOG:
        KM_LOG.append(log[-1])
    frame_mm = [(0.0, 0.0), (w_mm, 0.0), (w_mm, h_mm), (0.0, h_mm)]
    frame_items = [("fill", [frame_mm], KM_PAPER, 1.0, True),
                   ("line", frame_mm + [frame_mm[0]], KM_FRAME["colour"], KM_FRAME["lw"], None, 1.0)]
    KM_STUDY_LOG[page] = (len(study), 1 if study else 0)
    km = dict(base=base, study=st_items, cuts=cut_items, names=nr["items"],
              items=list(base) + st_items + cut_items + nr["items"], box=(vb[0], vb[1], vb[2], vb[3]),
              scale_den=den, T=T, Tinv=Tinv, drawn=drawn, missing=missing, label_boxes=label_boxes, labels=labels,
              w_mm=w_mm, h_mm=h_mm, study_rings=study, study_ring=study, study_closed=1 if study else 0,
              rotation_deg=rot_out, rotation=rot_out, north_deg=rot_out, fill=fill, frame=frame,
              frame_items=frame_items, north=north_its, north_box=north_box, heading_items=heading_items,
              heading_box=heading_box, looks=dict(looks or {}), zoom_ids=[cid for cid, _ in wins],
              cut_ids=[cid for cid, _ in cut_l], page=page)
    km["cuts_all"] = list(km["cut_ids"])
    km["classes"] = sorted(set(getattr(it, "cls", None) for it in base
                               if getattr(it, "ctx", None) in ("a", "d", "e", "f", "g") and getattr(it, "cls", None)))
    km["roads"] = sum(1 for it in base if getattr(it, "ctx", None) == "a" and it[0] == "line")
    km_log(page, km, log)
    return km


def km_draw_to(km, X, fill_fn, line_fn, text_fn, **kw):
    """round 6: draws a km_keymap on a board / page (km_draw: paper, base, water, study line whole and unclipped, red
    cuts, names, frame line, north arrow); X(q) key-map mm -> page point"""
    return km_draw(km, X, fill_fn, line_fn, text_fn, **kw)


def km_export_items(km, page=None, item_id=None, priority=5):
    """round 6: a km_keymap as booklet items (km_items: drawing, labels, keymap item)"""
    return km_items(km, page=page, item_id=item_id, priority=priority)


def km_log(page, km=None, log=None):
    """`keymap <page> module cuts=<ids> study_closed=<1|0> parts=<n>` (the G6-5 done-when line; study_closed=1 =
    every study ring drawn whole and closed). A page with no study data logs study_closed=0 with a WARNING."""
    n, closed = KM_STUDY_LOG.get(page, (0, 0))
    ids = u",".join((km or {}).get("cut_ids") or []) or u"-"
    ln = u"keymap %s module cuts=%s study_closed=%d parts=%d" % (page, ids, closed, n)
    lg = log if log is not None else KM_LOG
    lg.append(ln)
    nr_ = int((km or {}).get("roads") or 0)              # round 9 (S4, G9-5 done-when): the roads line
    lg.append(u"keymap %s roads n=%d cuts %s" % (page, nr_, ids))
    if km is not None and nr_ == 0:
        lg.append(u"WARNING %s keymap roads n=0: no street drawn (basemap.json layers streets_in / streets_out)" % page)
    if not closed:
        lg.append(u"WARNING %s keymap: no study outline (no basemap study layer and no recorded copy)" % page)
    if lg is not KM_LOG:
        KM_LOG.append(ln)
    return ln


# ---- round 9 (S4, 11 Nov 2026; BRIEF G9-5 d, PLAN.md §spec S4): THE key-map legend, one function for every page ----
def km_legend(kind_set, cuts=True, level=True, level_text=None, words=None):
    """the one key-map legend: the same rows in the same order on every page: study area (the closed violet
    dash-dot) · cut line + open triangle = the view direction (when the key map has cuts) · level, m above sea
    (level=False: none; level_text: the page's own words for it) · then only the base classes this key map shows,
    in the quiet tones it draws them: building fabric classes, woods, fields, grass and open ground, street, the
    stream. kind_set = a km_keymap dict (its "classes" and "cut_ids") or a set of base classes; cuts = the cut labels,
    or True / False. Returns [(swatch, text)] for Ix.legend; every swatch carries w_mm 4 and h_mm 2.4 (KM_LEG), a
    "group" (its legend heading) and, for base classes, its hue table cat / rank. Texts are set at KM_LEG pt 5."""
    if isinstance(kind_set, dict):
        ks = set(kind_set.get("classes") or ())
        if cuts is True:
            cuts = list(kind_set.get("cut_ids") or ())
    else:
        ks = set(kind_set or ())
    N = globals().get("NAMES")
    stream_w = ((N.get("places") or {}).get("stream") if isinstance(N, dict) else None) or u"Selinos stream"
    W = dict(study=globals().get("R28_STUDY_NAME") or u"Study area",
             cut=u"cut line · the triangle looks the way the section is drawn",
             level=level_text or u"level, m above sea", trees=u"Woods", fields=u"Fields",
             open=u"Grass and open ground", street=u"Street", stream=stream_w)
    W.update(FAB_WORDS)
    W.update(words or {})
    paper = BM_KEY["paper"]
    sz = dict(w_mm=KM_LEG["w_mm"], h_mm=KM_LEG["h_mm"])
    pt_ = lambda mm: round(mm / 0.352778, 3)
    q = lambda h: _bm_mix(h, paper, BM_CTX_QUIET)
    st = globals().get("R28_STUDY_LINE") or BM_STUDY_LINE
    rows = [(dict(sz, kind="dash", colour=st["colour"], width_pt=pt_(st["width_mm"]),
                  dash_pt=[pt_(v) for v in st["dash_mm"]], group=u"annotations"), W["study"])]
    if cuts:
        rows.append((dict(sz, kind="line", colour=KM_CUT["colour"], width_pt=pt_(KM_CUT["lw"]), mark="triangle",
                          group=u"annotations"), W["cut"]))
    if level:
        rows.append((dict(sz, kind="line", colour=hue("ANN", "ink"), group=u"annotations"), W["level"]))
    for c in FAB_CLASSES:
        if c in ks:
            rows.append((dict(sz, kind="fill", colour=_bm_mix(fab_hex(c), paper, HUE_KEY["fabric_mix"]), cat="FAB",
                              rank=FAB_RANK[c], group=HUE_NAMES["FAB"]), W[c]))
    if "trees" in ks:
        rows.append((dict(sz, kind="fill", colour=q(LC_HEX["trees"]), cat="LC", rank=1, group=HUE_NAMES["LC"]),
                     W["trees"]))
    if ks & set(("farmland", "orchard")):
        rows.append((dict(sz, kind="fill", colour=q(LC_HEX["farmland"]), cat="LC", rank=4, group=HUE_NAMES["LC"]),
                     W["fields"]))
    if ks & set(("grass", "shrub", "park")):
        rows.append((dict(sz, kind="fill", colour=q(LC_HEX["grass"]), cat="LC", rank=3, group=HUE_NAMES["LC"]),
                     W["open"]))
    if ks & set(("main", "secondary", "lane", "area", "path")):
        rows.append((dict(sz, kind="line", colour=q(str_hex("main")), width_pt=pt_(BM_STR_W_KEY["main"]), cat="STR",
                          rank=1, group=HUE_NAMES["STR"]), W["street"]))
    if "stream" in ks:
        rows.append((dict(sz, kind="fill", colour=bm_key_col("water"), cat="WAT", rank=1, group=HUE_NAMES["WAT"]),
                     W["stream"]))
    return rows


def km_legend_export(ix, km, page=None, item_id=None, level=True, level_text=None, words=None, group=None):
    """round 9 (S4): the key map's legend as one Ix legend item "<keymap id>_legend" (the R9_FRAMES legend id, e.g.
    sb_sec_keymap_p04_legend), its texts role "legend" at KM_LEG pt; item_id = the key map's id (as km_export_items
    got it). Logs `legend <page> hues=table r9`. Returns the legend id."""
    pg = page if page is not None else km.get("page")
    did = item_id or (u"keymap_%s" % (pg or u"key"))
    ents = []
    for sw, t in km_legend(km, True, level, level_text, words):
        tid = ix.text(pg, t, "legend", size_pt=KM_LEG["pt"], group=group or did)
        if tid is not None:
            ents.append((sw, tid))
    lid = ix.legend(pg, did, ents, id=u"%s_legend" % did, group=group or did)
    hue_log(pg)
    return lid

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
# v7 (round 4, S1 modules): real font widths, the ONE text placer, the ONE marker. v9 (round 5, C1): the ONE warning
# sink first (text_place then logs into WN_LOG; nothing raises on text or layout)
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
#   round 9 (S1, G9-1; PLAN.md §spec S1): the glyph shape of mk_marker is an _MkText carrying .badge, the S1 badge
#       item {"role": "badge", "at": [x, y], "r_mm", "fill", "ring", "ring_mm", "text", "pt", "bold", "colour"}
#       (at = the disc centre in the shapes' units); the disc shape is an _MkDisc (.mk_badge = True). Ix.layer
#       (ix_r9) exports such a pair as ONE badge item, so the booklet draws disc + glyph and centres the glyph with
#       bk_centre. Every other reader sees the same plain tuples as before.
#   mk_badge(cx, cy, s, colour, ...) -> the badge dict alone (same arguments as mk_marker, no shapes)
#   mk_badge_at(b, k=1.0, origin=(0, 0)) -> a copy of badge b with "at" mapped x' = origin + k * x (drawing units)
#   mk_put(tp, shapes, name=None) -> the non-text shapes
#                                     registers the disc as a keep (kind "marker") and the glyph in the TextPage (it
#                                     may sit on its own disc only; give each marker its own name); the caller draws the returned disc shapes, the
#                                     TextPage draws the glyph
MK_MARGIN_MM = 0.45                    # clear ring round the glyph's ink box (G-R4-7 "keep a margin")
MK_PAPER = "FFFFFF"
MK_INK = "2C2219"                      # dark glyph on light discs (the north-arrow ink of PLAN §4.5)
MK_COLOURS = {}
MK_N = [0]                             # markers registered this run (unique keep names)


class _MkText(tuple):
    """round 9 (S1): a marker's glyph shape; .badge = the S1 badge item of its marker"""
    pass


class _MkDisc(tuple):
    """round 9 (S1): a marker's disc shape (.mk_badge = True: Ix exports it inside the badge item)"""
    pass


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
    d_ = _MkDisc(disc)
    d_.mk_badge = True
    t_ = _MkText(("text", s, x, base, size_mm, tc, True, "L"))
    t_.badge = dict(role="badge", at=[cx, cy], r_mm=round(r, 3), fill=disc[2], ring=disc[3] or None,
                    ring_mm=round(float(disc[4] or 0.0), 3), text=s, pt=float(size_pt), bold=True, colour=tc)
    shapes = [d_, t_]
    return shapes, (cx - out_r, cy - out_r, cx + out_r, cy + out_r), r


def mk_badge(cx, cy, s, colour, size_pt=7.0, r_min=None, style="solid", rim="FFFFFF", rim_mm=0.25, text_col=None):
    """round 9 (S1): the S1 badge item of a marker centred on (cx, cy), the same disc and colours as mk_marker"""
    return dict(mk_marker(cx, cy, s, colour, size_pt, r_min, style, rim, rim_mm, text_col)[0][1].badge)


def mk_badge_at(b, k=1.0, origin=(0.0, 0.0)):
    """round 9 (S1): badge b with its centre mapped into drawing units, x' = origin + k * x (as Ix.layer maps shapes;
    r_mm, ring_mm and pt stay print sizes)"""
    o = dict(b)
    o["at"] = [origin[0] + k * float(b["at"][0]), origin[1] + k * float(b["at"][1])]
    return o


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
            tp.put(s_[1], s_[2], s_[3], s_[4] * tp.unit_mm / TP_PT, True, s_[7] if len(s_) > 7 else "L", 0.0, nm,
                   "marker", s_[5], allow=(nm,))        # round 9: the shape's own align
    return disc
# ---- M11 (revision 30 Oct 2026, H-A): the building renderer, plan / axonometric / section ---------------------------
# G7 "buildings look like buildings": plan = the footprint outline + a roof reading (ridge and hips, or fall-line
# hatch), never loose stripes; axonometric = light volumes with roofs (idea R09); section = profiles with their real
# heights in m, roofs and openings. Also the merge that fixes the fake parcel division lines AT THE SOURCE (bld_merge,
# called by the site board's build_site and by basemap_export): pieces of one footprint that share an edge become ONE
# outline, so no survey tick, party-wall split or Voronoi cut is ever drawn as a line.
# Geometry: survey m in, items out in the basemap item format (common/basemap.py head):
#   ("fill", rings, hex, alpha, nonzero)   ("line", pts, hex, width_mm, dash_mm, alpha)
#   ("text", s, (x, y), size_mm, hex, bold, align)
# plan items are in survey m (draw them with basemap_draw and the map's T); axo items are already projected (the
# caller's proj); section items are in (s, z) m along the cut (the caller's section transform).
# A unit (building) is either a site board unit (parts, holes, h, floors) or a basemap building (rings, np, h, floors).
# Roof form: the survey records no roof shapes, so the plan and axo read every pitched building as a hipped tile roof
# at BLD_PITCH (the common Bergama roof; a drawing convention, never printed as data); a unit flagged roof="flat" (or
# with h >= BLD_FLAT_H) is drawn flat with a parapet.
BLD_PITCH = 30.0                    # degrees, hipped tile roofs (drawing convention)
BLD_FLAT_H = 1e9                    # m: units at or above this height drawn flat (off: no survey of roof forms)
BLD_STOREY = 3.0                    # m per storey where a unit gives no floor count
BLD_COL = dict(fill="ECE9E3", edge="7D756C", roof="A39A90", her_fill="EEDCDB", her_edge="AF7474",
               wall_lit="F7F5F1", wall_shade="DCD8D1", roof_lit="EAE5DE", roof_shade="CFC8BE", axo_line="7D756C",
               sec_fill="EEEBE6", sec_cut="2C2219", sec_line="7D756C", opening="FFFFFF", glass="9FB3BA",
               text="4A3F35")
BLD_LW = dict(block=0.18, roof=0.07, hatch=0.05, axo=0.08, sec_cut=0.30, sec_line=0.10, glass=0.08)
BLD_MIN_ROOF_MM = 1.6               # a roof mark only where the building is at least this wide on the page
BLD_HIP_MAX_W = 12.0                # m: axo hipped roofs take at most this width's rise; wider parts get a flat top
                                    # in the middle (drawing rule, round 4 S2: merged blocks never one giant roof)
BLD_EAVE_MIN_M = 2.0                # m: axo eaves at least this far above a footprint's highest corner (drawing rule)


# ------------------------------------------------------------------------------------------- small geometry
def _bld_area(P):
    n = len(P)
    return 0.5 * sum(P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1] for i in range(n))


def _bld_pip(x, y, P):
    c, n = False, len(P)
    j = n - 1
    for i in range(n):
        xi, yi, xj, yj = P[i][0], P[i][1], P[j][0], P[j][1]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi:
            c = not c
        j = i
    return c


def _bld_bb(P):
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    return min(xs), min(ys), max(xs), max(ys)


def _bld_inner(P):
    """a point strictly inside polygon P (its centroid when inside, else the middle of the first span of a scan
    line through it)"""
    A = _bld_area(P)
    n = len(P)
    if abs(A) > 1e-9:
        cx = sum((P[i][0] + P[(i + 1) % n][0]) * (P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1])
                 for i in range(n)) / (6.0 * A)
        cy = sum((P[i][1] + P[(i + 1) % n][1]) * (P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1])
                 for i in range(n)) / (6.0 * A)
        if _bld_pip(cx, cy, P):
            return cx, cy
    else:
        cy = sum(p[1] for p in P) / float(n)
    b = _bld_bb(P)
    for f in (0.5, 0.37, 0.63, 0.25, 0.75, 0.1, 0.9):
        y = b[1] + (b[3] - b[1]) * f
        xs = []
        for i in range(n):
            a, c = P[i], P[(i + 1) % n]
            if (a[1] > y) != (c[1] > y):
                xs.append(a[0] + (y - a[1]) * (c[0] - a[0]) / (c[1] - a[1]))
        xs.sort()
        if len(xs) >= 2 and xs[1] - xs[0] > 1e-6:
            return (xs[0] + xs[1]) / 2.0, y
    return P[0][0], P[0][1]


def _bld_unit(u):
    """(outlines, holes) of a site board unit or a basemap building"""
    if "parts" in u:
        return list(u["parts"]), list(u.get("holes") or [])
    R = u.get("rings") or []
    k = u.get("np", len(R))
    return list(R[:k]), list(R[k:])


def _bld_her(u):
    """a heritage building (basemap flag her, or a site board unit of fabric monument / sacred)"""
    return bool(u.get("her")) or u.get("fabric") in ("monument", "sacred")


def _bld_h(u):
    h = u.get("h")
    if h:
        return float(h)
    f = u.get("floors") or 1
    return BLD_STOREY * f


# ------------------------------------------------------------------------------------------- merge (G7 at the source)
def bld_merge(rings, holes=(), tol=0.03):
    """the outlines of pieces merged where they share an edge (also along part of an edge: T-junctions are split
    first), by cancelling every edge two pieces share: [(outline ccw, [holes cw])]. tol (m): points this close are
    one point. Pieces that only overlap (no shared edge) stay as they are."""
    import math as _m
    pts, grid = [], {}

    def vid(p):
        kx, ky = int(_m.floor(p[0] / tol)), int(_m.floor(p[1] / tol))
        for i in (kx - 1, kx, kx + 1):
            for j in (ky - 1, ky, ky + 1):
                for k in grid.get((i, j), ()):
                    q = pts[k]
                    if abs(q[0] - p[0]) <= tol and abs(q[1] - p[1]) <= tol:
                        return k
        pts.append((float(p[0]), float(p[1])))
        grid.setdefault((kx, ky), []).append(len(pts) - 1)
        return len(pts) - 1
    loops = []
    for R in rings:
        if len(R) >= 3:
            loops.append(list(R) if _bld_area(R) > 0 else list(R)[::-1])
    for H in holes:
        if len(H) >= 3:
            loops.append(list(H) if _bld_area(H) < 0 else list(H)[::-1])
    edges = []
    for R in loops:
        ids = [vid(p) for p in R]
        ids = [k for i, k in enumerate(ids) if k != ids[i - 1]] if len(ids) > 1 else ids
        for i in range(len(ids)):
            a, b = ids[i], ids[(i + 1) % len(ids)]
            if a != b:
                edges.append((a, b))
    C = 5.0                                              # T-junctions: points lying on another piece's edge
    vg = {}
    for k, p in enumerate(pts):
        vg.setdefault((int(_m.floor(p[0] / C)), int(_m.floor(p[1] / C))), []).append(k)
    cnt = {}
    for a, b in edges:
        pa, pb = pts[a], pts[b]
        dx, dy = pb[0] - pa[0], pb[1] - pa[1]
        L2 = dx * dx + dy * dy
        cand = []
        if L2 > (2.0 * tol) ** 2:
            Ln = _m.sqrt(L2)
            for i in range(int(_m.floor((min(pa[0], pb[0]) - tol) / C)), int(_m.floor((max(pa[0], pb[0]) + tol) / C)) + 1):
                for j in range(int(_m.floor((min(pa[1], pb[1]) - tol) / C)),
                               int(_m.floor((max(pa[1], pb[1]) + tol) / C)) + 1):
                    for k in vg.get((i, j), ()):
                        if k == a or k == b:
                            continue
                        p = pts[k]
                        t = ((p[0] - pa[0]) * dx + (p[1] - pa[1]) * dy) / L2
                        if t <= 1e-6 or t >= 1.0 - 1e-6:
                            continue
                        if abs((p[0] - pa[0]) * dy - (p[1] - pa[1]) * dx) / Ln <= tol:
                            cand.append((t, k))
        seq = [a] + [k for _, k in sorted(cand)] + [b]
        for s0, s1 in zip(seq, seq[1:]):
            if s0 != s1:
                cnt[(s0, s1)] = cnt.get((s0, s1), 0) + 1
    out = {}
    keep = [e for e, c in cnt.items() if c > cnt.get((e[1], e[0]), 0)]
    for a, b in keep:
        out.setdefault(a, []).append(b)
    used, res_loops = set(), []
    for a0, b0 in keep:
        if (a0, b0) in used:
            continue
        used.add((a0, b0))
        ring, prev, cur, ok = [a0], a0, b0, False
        for _ in range(len(keep) + 1):
            if cur == a0:
                ok = True
                break
            ring.append(cur)
            nxt = [n for n in out.get(cur, ()) if (cur, n) not in used]
            if not nxt:
                break
            if len(nxt) > 1:                             # a pinch point: the sharpest right turn keeps rings simple
                ix, iy = pts[cur][0] - pts[prev][0], pts[cur][1] - pts[prev][1]
                nxt.sort(key=lambda n: _m.atan2(ix * (pts[n][1] - pts[cur][1]) - iy * (pts[n][0] - pts[cur][0]),
                                                ix * (pts[n][0] - pts[cur][0]) + iy * (pts[n][1] - pts[cur][1])))
            used.add((cur, nxt[0]))
            prev, cur = cur, nxt[0]
        if ok and len(ring) >= 3:
            res_loops.append([pts[k] for k in ring])
    clean = []
    for R in res_loops:                                  # straight-through points go
        changed = True
        while changed and len(R) > 3:
            changed = False
            for i in range(len(R)):
                p, q, r = R[i - 1], R[i], R[(i + 1) % len(R)]
                dx, dy = r[0] - p[0], r[1] - p[1]
                L = _m.hypot(dx, dy)
                if L < 1e-9:
                    continue
                if abs((q[0] - p[0]) * dy - (q[1] - p[1]) * dx) / L <= tol * 0.5 and \
                        (q[0] - p[0]) * dx + (q[1] - p[1]) * dy > 0 and (r[0] - q[0]) * dx + (r[1] - q[1]) * dy > 0:
                    del R[i]
                    changed = True
                    break
        A = _bld_area(R)
        if abs(A) >= 0.05:
            clean.append((A, R))
    outs = [[A, R, []] for A, R in clean if A > 0]
    outs.sort(key=lambda o: o[0])
    for A, R in clean:
        if A < 0:
            x, y = _bld_inner(R[::-1])
            for o in outs:                               # the smallest outline holding it
                if _bld_pip(x, y, o[1]):
                    o[2].append(R)
                    break
    return [(R, H) for _, R, H in outs]


def bld_merge_unit(parts, holes=(), tol=0.03):
    """(parts, holes) of ONE building with its pieces merged into one outline per connected piece (the survey's
    party-wall ticks, extended across the face, are not building edges). The input comes back unchanged when the
    merge would change the area by more than 1 % (a piece overlapping another)."""
    A0 = sum(abs(_bld_area(P)) for P in parts) - sum(abs(_bld_area(H)) for H in holes)
    if len(parts) < 2 and not holes:
        return list(parts), list(holes)
    try:
        res = bld_merge(parts, holes, tol)
    except Exception:
        return list(parts), list(holes)
    A1 = sum(_bld_area(o) + sum(_bld_area(h) for h in hs) for o, hs in res)
    if not res or abs(A1 - A0) > 0.01 * max(A0, 1.0):
        return list(parts), list(holes)
    return [o for o, _ in res], [h for _, hs in res for h in hs]


def bld_blocks(units, tol=0.03):
    """the blocks: buildings that share a wall merged into ONE outline (the plan's outline layer; no party walls
    drawn as lines): [dict(outer, holes, units=[index], h=max height m)]. A block whose merged area exceeds its
    buildings' (a failed merge) falls back to its buildings' own outlines."""
    rings, holes = [], []
    for u in units:
        P_, H_ = _bld_unit(u)
        rings += P_
        holes += H_
    res = bld_merge(rings, holes, tol) if rings else []
    cells = {}
    C = 40.0
    for bi, (o, hs) in enumerate(res):
        b = _bld_bb(o)
        for i in range(int(b[0] // C), int(b[2] // C) + 1):
            for j in range(int(b[1] // C), int(b[3] // C) + 1):
                cells.setdefault((i, j), []).append(bi)
    members = {}
    lone = []
    for i, u in enumerate(units):
        P_, _ = _bld_unit(u)
        if not P_:
            continue
        P0 = max(P_, key=lambda P: abs(_bld_area(P)))
        x, y = _bld_inner(P0 if _bld_area(P0) > 0 else P0[::-1])
        hit = None
        for bi in sorted(cells.get((int(x // C), int(y // C)), ()), key=lambda k: _bld_area(res[k][0])):
            if _bld_pip(x, y, res[bi][0]):
                hit = bi
                break
        if hit is None:
            lone.append(i)
        else:
            members.setdefault(hit, []).append(i)
    out = []
    for bi, idx in members.items():
        o, hs = res[bi]
        A = _bld_area(o) + sum(_bld_area(h) for h in hs)
        A_u = sum(sum(abs(_bld_area(P)) for P in _bld_unit(units[i])[0]) -
                  sum(abs(_bld_area(H)) for H in _bld_unit(units[i])[1]) for i in idx)
        if A > 1.02 * A_u + 1.0:
            lone += idx
            continue
        out.append(dict(outer=o, holes=hs, units=sorted(idx), h=max(_bld_h(units[i]) for i in idx)))
    for i in lone:
        P_, H_ = _bld_unit(units[i])
        for P in P_:
            out.append(dict(outer=P if _bld_area(P) > 0 else P[::-1], holes=[], units=[i], h=_bld_h(units[i])))
        for k, H in enumerate(H_):
            out[-1]["holes"].append(H)
    return out


# ------------------------------------------------------------------------------------------- roof geometry
def bld_rect(P):
    """the minimum-area rectangle round P: (cx, cy, ux, uy, L, W), u along the long side (L >= W)"""
    import math as _m
    pts = sorted(set((round(p[0], 4), round(p[1], 4)) for p in P))
    if len(pts) < 3:
        return None

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    hull = lo[:-1] + hi[:-1]
    best = None
    for i in range(len(hull)):
        a, b = hull[i], hull[(i + 1) % len(hull)]
        L = _m.hypot(b[0] - a[0], b[1] - a[1])
        if L < 1e-9:
            continue
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        su = [p[0] * ux + p[1] * uy for p in hull]
        sv = [-p[0] * uy + p[1] * ux for p in hull]
        area = (max(su) - min(su)) * (max(sv) - min(sv))
        if best is None or area < best[0]:
            best = (area, ux, uy, min(su), max(su), min(sv), max(sv))
    if best is None:
        return None
    _, ux, uy, u0, u1, v0, v1 = best
    cu, cv = (u0 + u1) / 2.0, (v0 + v1) / 2.0
    cx, cy = cu * ux - cv * uy, cu * uy + cv * ux
    Lu, Lv = u1 - u0, v1 - v0
    if Lv > Lu:
        ux, uy, Lu, Lv = -uy, ux, Lv, Lu
    return cx, cy, ux, uy, Lu, Lv


def _bld_clip_seg(a, b, P):
    """the pieces of segment a-b inside polygon P"""
    ts = [0.0, 1.0]
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = len(P)
    for i in range(n):
        p, q = P[i], P[(i + 1) % n]
        ex, ey = q[0] - p[0], q[1] - p[1]
        den = dx * ey - dy * ex
        if abs(den) < 1e-12:
            continue
        t = ((p[0] - a[0]) * ey - (p[1] - a[1]) * ex) / den
        s = ((p[0] - a[0]) * dy - (p[1] - a[1]) * dx) / den
        if 0.0 < t < 1.0 and -1e-9 <= s <= 1.0 + 1e-9:
            ts.append(t)
    ts.sort()
    out = []
    for t0, t1 in zip(ts, ts[1:]):
        if t1 - t0 < 1e-6:
            continue
        tm = (t0 + t1) / 2.0
        if _bld_pip(a[0] + dx * tm, a[1] + dy * tm, P):
            out.append([(a[0] + dx * t0, a[1] + dy * t0), (a[0] + dx * t1, a[1] + dy * t1)])
    return out


def bld_roof_lines(P, mode="ridge", spacing=None):
    """the roof reading of one footprint P (survey m): segments [(a, b)] clipped to P. mode "ridge" = ridge + four
    hips of a hipped roof on the footprint's minimum rectangle; "hatch" = the same plus fall lines across the long
    planes every `spacing` m; "flat" = a parapet line inset 0.4 m; "none" = []"""
    if mode == "none":
        return []
    r = bld_rect(P)
    if r is None:
        return []
    cx, cy, ux, uy, L, W = r
    vx, vy = -uy, ux
    out = []
    if mode == "flat":
        k = 0.4
        if W > 2.5 * k:
            Q = [(cx + ux * su * (L / 2 - k) + vx * sv * (W / 2 - k), cy + uy * su * (L / 2 - k) + vy * sv * (W / 2 - k))
                 for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            for a, b in zip(Q, Q[1:] + Q[:1]):
                out += _bld_clip_seg(a, b, P)
        return out
    h = (L - W) / 2.0
    e1, e2 = (cx - ux * h, cy - uy * h), (cx + ux * h, cy + uy * h)
    segs = [(e1, e2)] if h > 0.05 else []
    for e, su in ((e1, -1), (e2, 1)):
        for sv in (-1, 1):
            segs.append((e, (cx + ux * su * L / 2 + vx * sv * W / 2, cy + uy * su * L / 2 + vy * sv * W / 2)))
    if mode == "hatch" and spacing and h > spacing:
        k = -h + spacing / 2.0
        while k < h:
            for sv in (-1, 1):
                a = (cx + ux * k, cy + uy * k)
                segs.append((a, (a[0] + vx * sv * W / 2, a[1] + vy * sv * W / 2)))
            k += spacing
    for a, b in segs:
        out += _bld_clip_seg(a, b, P)
    return out


def _bld_roof_mode(u, mode):
    if u.get("roof") == "flat" or _bld_h(u) >= BLD_FLAT_H:
        return "flat"
    return mode


# ------------------------------------------------------------------------------------------- plan
def bld_plan_items(units, blocks=None, scale_den=1000.0, roof="ridge", box=None, fill=None, edge=None,
                   roof_col=None, her_fill=None, her_edge=None, alpha=1.0, outline=True, hatch_mm=1.2, lw=None):
    """G7 plan: buildings as items (survey m): a light fill per building, the roof reading (ridge + hips; roof="hatch"
    adds fall lines every hatch_mm on the page; "none" leaves it out) where the building is at least BLD_MIN_ROOF_MM
    wide at 1:scale_den, and ONE outline per block (blocks: bld_blocks(units), made when not given): no line between
    buildings that share a wall. Heritage units (her=True) in their own tone. box (x0, y0, x1, y1): only what touches
    it. lw: the block outline width in mm (default BLD_LW["block"]; the round 4 muted base uses 0.12)."""
    fill, edge = fill or BLD_COL["fill"], edge or BLD_COL["edge"]
    lw_b = BLD_LW["block"] if lw is None else lw
    roof_col = roof_col or BLD_COL["roof"]
    her_fill, her_edge = her_fill or BLD_COL["her_fill"], her_edge or BLD_COL["her_edge"]
    mpm = scale_den / 1000.0                             # survey m per page mm

    def hit(P):
        if box is None:
            return True
        b = _bld_bb(P)
        return not (b[2] < box[0] or b[0] > box[2] or b[3] < box[1] or b[1] > box[3])
    out, chunk, chunk_h, roofs = [], [], [], []
    for u in units:
        P_, H_ = _bld_unit(u)
        P_ = [P for P in P_ if len(P) >= 3 and hit(P)]
        if not P_:
            continue
        (chunk_h if _bld_her(u) else chunk).extend(P_ + H_)
        if roof != "none":
            mode = _bld_roof_mode(u, roof)
            for P in P_:
                r = bld_rect(P)
                if r is None or r[5] / mpm < BLD_MIN_ROOF_MM:
                    continue
                roofs += bld_roof_lines(P, mode, hatch_mm * mpm)
        if len(chunk) >= 300:
            out.append(("fill", chunk, fill, alpha, True))
            chunk = []
    if chunk:
        out.append(("fill", chunk, fill, alpha, True))
    if chunk_h:
        out.append(("fill", chunk_h, her_fill, alpha, True))
    for a, b in roofs:
        out.append(("line", [a, b], roof_col, BLD_LW["roof"], None, alpha))
    if outline:
        if blocks is None:
            blocks = bld_blocks(units)
        her_idx = set(i for i, u in enumerate(units) if _bld_her(u))
        for bk in blocks:
            o = bk["outer"] if "outer" in bk else bk["rings"][0]
            hs = bk.get("holes") if "outer" in bk else bk["rings"][1:]
            if len(o) < 3 or not hit(o):
                continue
            col = her_edge if bk.get("her") or (bk.get("units") and all(i in her_idx for i in bk["units"])) else edge
            for R in [o] + list(hs or []):
                out.append(("line", list(R) + [R[0]], col, lw_b, None, alpha))
    return out


# ------------------------------------------------------------------------------------------- axonometric
def _bld_mix(a, b, t):
    pa = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    pb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join("%02X" % int(round(pa[i] + (pb[i] - pa[i]) * t)) for i in range(3))


def bld_axo_items(units, proj, view=(-0.70711, -0.70711), ground=None, pitch=BLD_PITCH, box=None, sun=(-0.6, 0.8),
                  cols=None, lw=None, roofs=True):
    """G7 axonometric (idea R09): light volumes with roofs, as page items. proj(x, y, z) -> (X, Y) page mm (the
    caller's axonometric); view = the horizontal direction from the scene TOWARDS the viewer (survey axes), used for
    which walls show and the drawing order (far first); ground(x, y) -> terrain m (else u["z0"] or 0); sun = the
    horizontal light direction (lit walls and roof planes lighter). Round 4 (S2): ground(x, y) is read at every
    corner (walls follow the slope), eaves = lowest corner + h (>= highest + BLD_EAVE_MIN_M); every pitched part gets
    a hipped roof = the planes of its minimum rectangle clipped to the footprint (pitch of at most BLD_HIP_MAX_W,
    flat top beyond), the walls rise to the roof at gable ends; flat units and parts with a courtyard a flat top."""
    import math as _m
    C = dict(BLD_COL)
    C.update(cols or {})
    lw = lw if lw is not None else BLD_LW["axo"]
    vx, vy = view
    sn = _m.hypot(*sun) or 1.0
    sx, sy = sun[0] / sn, sun[1] / sn
    jobs = []
    for u in units:
        P_, H_ = _bld_unit(u)
        for P in P_:
            if len(P) < 3:
                continue
            if box is not None:
                b = _bld_bb(P)
                if b[2] < box[0] or b[0] > box[2] or b[3] < box[1] or b[1] > box[3]:
                    continue
            P = P if _bld_area(P) > 0 else P[::-1]
            cx, cy = _bld_inner(P)
            jobs.append((cx * vx + cy * vy, u, P, cx, cy))
    jobs.sort(key=lambda j: j[0])                         # far first
    out = []
    t_p = _m.tan(_m.radians(pitch))
    for _, u, P, cx, cy in jobs:
        # round 4 (S2, CHK-4 P12.2): every wall stands on the ground at its own corners (no floating or sunk walls on
        # a slope); the eaves are h above the lowest corner, at least BLD_EAVE_MIN_M above the highest one
        zb = [ground(p[0], p[1]) for p in P] if ground else [float(u.get("z0") or 0.0)] * len(P)
        h = _bld_h(u)
        zt = max(min(zb) + h, max(zb) + BLD_EAVE_MIN_M)
        r = bld_rect(P)
        H_u = _bld_unit(u)[1]
        holes = [H for H in H_u if len(H) >= 3 and _bld_pip(H[0][0], H[0][1], P)]
        # round 4 (S2, CHK-4 P12.2): a hipped roof on EVERY pitched part (was: only where the footprint filled 80 %
        # of its rectangle): the roof planes of its minimum rectangle clipped to the footprint; a part wider than
        # BLD_HIP_MAX_W gets the pitch of that width and a flat top in the middle (a block of several houses never
        # reads as one giant roof); parts with a courtyard keep the flat top
        pitched = roofs and _bld_roof_mode(u, "ridge") != "flat" and r is not None and not holes
        planes = []
        if pitched:
            rcx, rcy, ux, uy, L, W = r
            wx, wy = -uy, ux
            e = min(W / 2.0, BLD_HIP_MAX_W / 2.0)

            def at(su, sv):
                return (rcx + ux * su + wx * sv, rcy + uy * su + wy * sv)
            hl, hw = L / 2.0, W / 2.0
            planes = [([at(-hl, hw), at(hl, hw), at(hl - e, hw - e), at(-hl + e, hw - e)], (wx, wy)),
                      ([at(hl, -hw), at(-hl, -hw), at(-hl + e, -hw + e), at(hl - e, -hw + e)], (-wx, -wy)),
                      ([at(hl, hw), at(hl, -hw), at(hl - e, -hw + e), at(hl - e, hw - e)], (ux, uy)),
                      ([at(-hl, -hw), at(-hl, hw), at(-hl + e, hw - e), at(-hl + e, -hw + e)], (-ux, -uy))]
            if hw - e > 1e-3:
                planes.append(([at(-hl + e, -hw + e), at(hl - e, -hw + e), at(hl - e, hw - e), at(-hl + e, hw - e)],
                               None))

            def zr(x, y, _r=r):
                dx, dy = x - _r[0], y - _r[1]
                su, sv = dx * _r[2] + dy * _r[3], -dx * _r[3] + dy * _r[2]
                d = min(_r[5] / 2.0 - abs(sv), _r[4] / 2.0 - abs(su), e)
                return zt + t_p * max(0.0, d)
        else:
            def zr(x, y):
                return zt
        walls = []
        n = len(P)
        for i in range(n):
            p, q = P[i], P[(i + 1) % n]
            ex, ey = q[0] - p[0], q[1] - p[1]
            L_e = _m.hypot(ex, ey)
            if L_e < 1e-6:
                continue
            nx, ny = ey / L_e, -ex / L_e                 # outward (ccw outline)
            if nx * vx + ny * vy <= 1e-6:
                continue
            lit = nx * sx + ny * sy
            col = _bld_mix(C["wall_shade"], C["wall_lit"], max(0.0, min(1.0, 0.5 + 0.5 * lit)))
            ts = set([0.0, 1.0])                         # the wall top follows the roof (gable ends at notches)
            for pl, _nrm in planes:
                for sa, sb_ in _bld_clip_seg(p, q, pl):
                    for pt in (sa, sb_):
                        ts.add(round(((pt[0] - p[0]) * ex + (pt[1] - p[1]) * ey) / (L_e * L_e), 6))
            top = []
            for t_ in sorted(x_ for x_ in ts if -1e-9 <= x_ <= 1.0 + 1e-9):
                x_, y_ = p[0] + ex * t_, p[1] + ey * t_
                top.append(proj(x_, y_, zr(x_, y_)))
            mx, my = (p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0
            ring = [proj(p[0], p[1], zb[i]), proj(q[0], q[1], zb[(i + 1) % n])] + top[::-1]
            walls.append((mx * vx + my * vy, ring, col))
        walls.sort(key=lambda w: w[0])
        for _, ring, col in walls:
            out.append(("fill", [ring], col, 1.0, True))
            out.append(("line", ring + ring[:1], C["axo_line"], lw, None, 1.0))
        if pitched:
            rp = []
            for pl, nrm in planes:
                piece = _bld_clip_convex(P, pl)
                if len(piece) < 3 or abs(_bld_area(piece)) < 1e-4:
                    continue
                mx = sum(p_[0] for p_ in piece) / len(piece)
                my = sum(p_[1] for p_ in piece) / len(piece)
                if nrm is None:
                    col = C["roof_lit"]
                else:
                    lit = nrm[0] * sx + nrm[1] * sy
                    col = _bld_mix(C["roof_shade"], C["roof_lit"], max(0.0, min(1.0, 0.5 + 0.5 * lit)))
                rp.append((mx * vx + my * vy, [proj(x_, y_, zr(x_, y_)) for x_, y_ in piece], col))
            rp.sort(key=lambda w: w[0])
            for _, ring, col in rp:
                out.append(("fill", [ring], col, 1.0, True))
                out.append(("line", ring + ring[:1], C["axo_line"], lw, None, 1.0))
        else:
            top = [proj(p[0], p[1], zt) for p in P]
            hs = [[proj(p[0], p[1], zt) for p in H] for H in holes]
            out.append(("fill", [top] + hs, C["roof_lit"], 1.0, False))
            out.append(("line", top + top[:1], C["axo_line"], lw, None, 1.0))
    return out


def _bld_clip_convex(P, C_):
    """round 4 (S2): polygon P (any shape) clipped to the convex polygon C_ (Sutherland-Hodgman, either turn of C_)"""
    s_ = _bld_area(C_)
    sgn = 1.0 if s_ > 0 else -1.0
    out = list(P)
    m = len(C_)
    for i in range(m):
        a, b = C_[i], C_[(i + 1) % m]
        if not out:
            break

        def side(p):
            return sgn * ((b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]))
        inp, out = out, []
        for j in range(len(inp)):
            p, q = inp[j - 1], inp[j]
            sp, sq = side(p), side(q)
            if sq >= 0:
                if sp < 0:
                    t = sp / (sp - sq)
                    out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
                out.append(q)
            elif sp >= 0:
                t = sp / (sp - sq)
                out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
    return out


# ------------------------------------------------------------------------------------------- section
def bld_section_profile(s0, s1, z0, h, floors=None, roof="gable", pitch=BLD_PITCH, depth_w=None, wall=0.3,
                        openings=True, label=False, label_mm=2.2, cols=None, lw=None, label_gap_m=1.5):
    """G7 section: ONE building cut between s0 and s1 (m along the section), ground z0 and eaves height h (m), as
    items in (s, z) m: the profile (light fill), the cut walls and floor slabs in ink with a window opening per floor
    in each cut wall (sill 0.90 m, head 2.10 m above the floor where the storey allows), the roof cut: "gable" (cut
    across the ridge: apex in the middle), "hip" (cut along the ridge: slopes of depth_w / 2 at both ends), "flat"
    (a 0.60 m parapet). label=True writes the real height "9.60 m" centred label_gap_m over the roof top (2
    decimals; run it through M2 lp_place when buildings stand close)."""
    import math as _m
    C = dict(BLD_COL)
    C.update(cols or {})
    lw = lw or BLD_LW
    if s1 < s0:
        s0, s1 = s1, s0
    w = s1 - s0
    if w <= 2.0 * wall or h <= 0.5:
        return []
    zt = z0 + h
    t = _m.tan(_m.radians(pitch))
    if roof == "flat":
        top = [(s1, zt), (s1, zt + 0.6), (s1 - wall, zt + 0.6), (s1 - wall, zt), (s0 + wall, zt), (s0 + wall, zt + 0.6),
               (s0, zt + 0.6), (s0, zt)]
        apex = zt + 0.6
    elif roof == "hip":
        run = min(w / 2.0, (depth_w or w) / 2.0)
        rise = t * run
        top = [(s1, zt), (s1 - run, zt + rise), (s0 + run, zt + rise), (s0, zt)]
        apex = zt + rise
    else:
        rise = t * w / 2.0
        top = [(s1, zt), ((s0 + s1) / 2.0, zt + rise), (s0, zt)]
        apex = zt + rise
    prof = [(s0, z0), (s1, z0)] + top
    out = [("fill", [prof], C["sec_fill"], 1.0, True)]
    nf = int(floors) if floors else max(1, int(round(h / BLD_STOREY)))
    st = h / float(nf)
    for k in range(1, nf + 1):                           # floor slabs (the top one under the roof)
        z = z0 + k * st
        out.append(("fill", [[(s0, z - 0.25), (s1, z - 0.25), (s1, z), (s0, z)]], C["sec_cut"], 1.0, True))
    for sa in (s0, s1 - wall):                           # cut walls, each storey with its window opening
        for k in range(nf):
            zf = z0 + k * st
            if openings and st >= 2.4:
                for za, zb in ((zf, zf + 0.9), (zf + 2.1, zf + st)):
                    if zb - za > 1e-3:
                        out.append(("fill", [[(sa, za), (sa + wall, za), (sa + wall, zb), (sa, zb)]], C["sec_cut"], 1.0,
                                    True))
                out.append(("line", [(sa + wall / 2.0, zf + 0.9), (sa + wall / 2.0, zf + 2.1)], C["glass"],
                            lw["glass"], None, 1.0))
            else:
                out.append(("fill", [[(sa, zf), (sa + wall, zf), (sa + wall, zf + st), (sa, zf + st)]], C["sec_cut"],
                            1.0, True))
    out.append(("line", list(top), C["sec_cut"], lw["sec_cut"], None, 1.0))
    out.append(("line", [(s0, z0), (s0, zt)], C["sec_line"], lw["sec_line"], None, 1.0))
    out.append(("line", [(s1, z0), (s1, zt)], C["sec_line"], lw["sec_line"], None, 1.0))
    if label:
        out.append(("text", u"{:.2f} m".format(h), ((s0 + s1) / 2.0, apex + label_gap_m), label_mm, C["text"], False,
                    "MC"))
    return out


def bld_section_items(a, b, units, ground=None, pitch=BLD_PITCH, label=False, openings=True, cols=None):
    """G7 section along the cut a -> b (survey m): every building the cut passes through, as bld_section_profile
    items in (s, z) m (s from a). ground(x, y) -> terrain m (else u["z0"] or 0). The roof is cut "gable" where the
    cut crosses the ridge (within 45 degrees of square to it), else "hip"; flat units flat. Heights are the units'
    own (u["h"], m)."""
    import math as _m
    L = _m.hypot(b[0] - a[0], b[1] - a[1])
    if L < 1e-6:
        return []
    dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    out = []
    for u in units:
        P_, _ = _bld_unit(u)
        for P in P_:
            bb = _bld_bb(P)
            if max(min(a[0], b[0]), bb[0]) > min(max(a[0], b[0]), bb[2]) + 1e-6 or \
                    max(min(a[1], b[1]), bb[1]) > min(max(a[1], b[1]), bb[3]) + 1e-6:
                continue
            ts = []
            n = len(P)
            for i in range(n):
                p, q = P[i], P[(i + 1) % n]
                ex, ey = q[0] - p[0], q[1] - p[1]
                den = dx * ey - dy * ex
                if abs(den) < 1e-12:
                    continue
                t = ((p[0] - a[0]) * ey - (p[1] - a[1]) * ex) / den
                s = ((p[0] - a[0]) * dy - (p[1] - a[1]) * dx) / den
                if -1e-9 <= s < 1.0 - 1e-9:
                    ts.append(t)
            ts.sort()
            r = bld_rect(P)
            across = r is None or abs(dx * r[2] + dy * r[3]) < 0.7071
            mode = _bld_roof_mode(u, "ridge")
            for t0, t1 in zip(ts[0::2], ts[1::2]):
                t0, t1 = max(0.0, t0), min(L, t1)
                if t1 - t0 < 1.0:
                    continue
                mx, my = a[0] + dx * (t0 + t1) / 2.0, a[1] + dy * (t0 + t1) / 2.0
                z0 = ground(mx, my) if ground else float(u.get("z0") or 0.0)
                out += bld_section_profile(t0, t1, z0, _bld_h(u), u.get("floors"),
                                           "flat" if mode == "flat" else ("gable" if across else "hip"), pitch,
                                           r[5] if r else None, openings=openings, label=label, cols=cols)
    return out
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
# ---- section language of the main site board (selinus_board draw_section_strip), shared by the water board and the
# agriculture alternatives (Aras 25 Oct 21:52: their sections drawn "such as we draw in the site sections"): the cut
# ground a shade darker than the page with a fine ink line, water hatched in blue from the bed to its surface, the
# channel above it in a pale wash, whole trees and plants at their stated size. One scale for x and y (Aras 22:02:
# "not stretch anything ever"). Pure geometry: each helper returns shapes, the script's sec_put() draws them.
# Round 5 (S3, section kit v2, G-R5-4.1/4.2): every cut material and the water ONE flat colour (SCT, SCT_WATER), the
# soil in lighter layers going down (SCT_SOIL), no hatch pattern drawn by any function here.
#   ("poly", ring, fill, stroke, lw)    ("line", pts, colour, lw)          page mm, y up


def _sec_mix(a, b, t):
    """hex a -> hex b by t (the board's mix(), on hex strings)."""
    pa = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    pb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join("%02X" % int(round(pa[i] + (pb[i] - pa[i]) * t)) for i in range(3))


# palette roles of the board's sections (selinus_board parts 01 and 14: slide khaki, paper, ink, the Selinus' blue)
SEC = dict(paper="F1EDDF", ink="4A3F35", ink2="7A6E60", khaki="BCB794", water="7FA4B3", hatch="3E7DAE",
           tree="7E8A57", pine="5F6B43", olive="8E9A6C", trunk="7A6E60", reed="8E9466", reed_head="B49A6C",
           lav="9F86C0", grass="8F9A68")
SEC["soil"] = _sec_mix(SEC["khaki"], SEC["paper"], 0.42)          # SEC_SOIL: the cut ground
SEC["channel"] = _sec_mix(SEC["water"], SEC["paper"], 0.5)        # SEC_CHANNEL: the water body
SEC["wash"] = _sec_mix(SEC["water"], SEC["paper"], 0.72)          # the channel above the water
SEC["crown"] = _sec_mix(SEC["tree"], SEC["paper"], 0.15)          # SEC_CROWN
SEC["crown_lt"] = _sec_mix(SEC["tree"], SEC["paper"], 0.45)
SEC["shrub"] = _sec_mix(SEC["olive"], SEC["paper"], 0.25)
SEC["beyond"] = _sec_mix(SEC["tree"], SEC["paper"], 0.62)         # things beyond the cut: paler
# round 4 (S2, G-R4-6): the greenery keys above (tree, pine, olive, reed, reed_head, lav, grass, crown, crown_lt, shrub,
# beyond) are NOT plant colours any more: every plant colour comes from plants.py pla_colours (S3). They stay only
# because plants.py (S3) and masterplan p24_detail.py:1836 (S8) still read them; those sessions remove the reads and
# the closing step deletes these keys. The legacy greenery helpers sec_tree / sec_shrub / sec_reeds / sec_tufts /
# sec_lavender were deleted here (no caller left).


def sec_hatch(ring, spacing, ang_deg=45.0):
    """The hatch lines of a closed ring (page mm) at ang_deg, spacing apart: [(p, q), ...] (even-odd scan)."""
    import math as _m
    a = _m.radians(ang_deg)
    ca, sa = _m.cos(a), _m.sin(a)
    R = [(ca * x + sa * y, -sa * x + ca * y) for x, y in ring]       # hatch direction along u
    vs = [p[1] for p in R]
    out = []
    k = _m.ceil(min(vs) / spacing)
    while k * spacing < max(vs):
        v = k * spacing
        us = []
        for i in range(len(R)):
            (u0, v0), (u1, v1) = R[i], R[(i + 1) % len(R)]
            if (v0 <= v < v1) or (v1 <= v < v0):
                us.append(u0 + (u1 - u0) * (v - v0) / (v1 - v0))
        us.sort()
        for j in range(0, len(us) - 1, 2):
            p = (ca * us[j] - sa * v, sa * us[j] + ca * v)
            q = (ca * us[j + 1] - sa * v, sa * us[j + 1] + ca * v)
            out.append((p, q))
        k += 1
    return out


def sec_ellipse(cx, cy, rx, ry, n=28):
    import math as _m
    return [(cx + rx * _m.cos(2 * _m.pi * i / n), cy + ry * _m.sin(2 * _m.pi * i / n)) for i in range(n)]


def sec_water(ring, spacing=0.6, lw=0.1):
    """A water body (ring, page mm). Round 5 (S3, G-R5-4.1, PLAN §3): ONE flat colour SCT_WATER["body"] and the
    surface line SCT_WATER["surface"] on top; no hatch (spacing / lw kept so old calls run, unused)."""
    sh = [("poly", ring, SCT_WATER["body"], None, 0.0)]
    top = max(p[1] for p in ring)
    xs = [p[0] for p in ring if abs(p[1] - top) < 1e-6]
    if len(xs) >= 2:
        sh.append(("line", [(min(xs), top), (max(xs), top)], SCT_WATER["surface"], SCT_WATER["surface_lw"]))
    return sh


# Round 5 (S3, G-R5-4.1, PLAN §3 "Section materials"): design values, solid colours only. Q100 / Q500 lines in the
# surface colour, dashed (water.py reads these).
SCT_WATER = dict(body="A2B6B5", surface="5C7A86", surface_lw=0.25, flood="5C7A86")


# ---- section parts (WO-T2b-3, 29 Oct 2026; section_style.py now includes this file): the river bank as it is at the
# cut (brief 02 §4): DSİ stone walls at 5.00 m, embankments at their surveyed angle, loose earth banks, railings and
# parapets; stone, concrete, earth and the gravel bed in their own hatch; terraces and steps cut into the bank.
# Real sizes in m placed by k (page mm per m); a bank's surface runs from its toe at the bed landward.

SCT_DSI_WALL_H_M = 5.00   # revision_2026-10-29/T1/levels/RESULT.md line 18: "DSİ stone walls at bed + 5.00 m" (Aras 28 Oct)

# material fills. Round 5 (S3, G-R5-4.1, U23-U25 "dont have hatches in the sections just give proper colours to the
# things that we cut"): every cut material ONE flat true colour (PLAN §3 design values); no hatch pattern anywhere.
# Material key = colour swatches (sct_material_key).
SCT = dict(stone="A4A1A3",                            # stone / masonry
           concrete="D5D3CE",                         # concrete / deck
           earth="C2A383",                            # = SCT_SOIL top layer (G-R5-4.2)
           gravel="B9B6AC",                           # gravel bed
           timber="9C8466",                           # timber deck
           line=SEC["ink2"],                          # joint lines (insets at 1:100-1:250 only, G-R5-5)
           cut=SEC["ink"])                            # the cut line
SCT_NAMES = dict(stone=u"Stone, masonry", concrete=u"Concrete", earth=u"Earth", gravel=u"Gravel bed",
                 timber=u"Timber deck", water=u"Water")
SCT_LOG = dict(solid=0, detail=0)                     # cut rings drawn flat / with inset joint detail this run


def sct_material_key(materials=("earth", "stone", "concrete", "gravel", "timber", "water")):
    """the material key of a section as colour swatches (G-R5-4.1: the hatch legend becomes a colour key):
    [(swatch dict for item_export Ix.legend, name)]"""
    out = []
    for m in materials:
        col = SCT_WATER["body"] if m == "water" else SCT[m]
        out.append((dict(kind="fill", colour=col, stroke=None), SCT_NAMES.get(m, m)))
    return out


def _sct_rnd(i, j):
    """A fixed pseudo-random number in [0, 1) for grid cell (i, j)."""
    import math as _m
    v = _m.sin(i * 12.9898 + j * 78.233) * 43758.5453
    return v - _m.floor(v)


def _sct_inside(ring, p):
    """Even-odd test: is page point p inside the ring."""
    x, y = p
    c = False
    n = len(ring)
    for i in range(n):
        (x0, y0), (x1, y1) = ring[i], ring[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < x0 + (x1 - x0) * (y - y0) / (y1 - y0):
            c = not c
    return c


def _sct_clip(ring, p, q):
    """The parts of segment p-q inside the ring: [(a, b), ...]."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    ts = [0.0, 1.0]
    n = len(ring)
    for i in range(n):
        (x0, y0), (x1, y1) = ring[i], ring[(i + 1) % n]
        ex, ey = x1 - x0, y1 - y0
        den = dx * ey - dy * ex
        if abs(den) < 1e-12:
            continue
        t = ((x0 - p[0]) * ey - (y0 - p[1]) * ex) / den
        s = ((x0 - p[0]) * dy - (y0 - p[1]) * dx) / den
        if 0.0 < t < 1.0 and 0.0 <= s <= 1.0:
            ts.append(t)
    ts.sort()
    out = []
    for a, b in zip(ts[:-1], ts[1:]):
        if b - a < 1e-9:
            continue
        m = (a + b) / 2.0
        if _sct_inside(ring, (p[0] + dx * m, p[1] + dy * m)):
            out.append(((p[0] + dx * a, p[1] + dy * a), (p[0] + dx * b, p[1] + dy * b)))
    return out


SCT_DETAIL_K = 4.0                    # page mm per m from which a ring gets real joints: 1:250 and larger (G-R5-5 insets)
SCT_COURSE_M = 0.50                   # stone course height (drawing rule, as water.py water_axo course_m; not surveyed)
SCT_BOARD_M = 0.14                    # deck board width (drawing rule, as sf_lane timber; not surveyed)


def sct_hatch_fill(ring, material, k, outline=None, lw=0.25, fill=True, hatch_lw=None):
    """A cut ring (page mm) in its material: stone, concrete, earth, gravel, timber or water. Round 5 (S3, G-R5-4.1):
    ONE flat colour (SCT), no hatch pattern; the name stays so every caller gets solid colours unchanged. At
    1:250 and larger (k >= SCT_DETAIL_K, the zoom insets, G-R5-5) stone shows its courses and timber its boards as
    real joints at drawing-rule sizes (SCT_COURSE_M, SCT_BOARD_M): construction lines, not a hatch. fill=False:
    nothing but the outline (the soil gradient under it is the fill). hatch_lw: kept for old calls, unused."""
    if material == "water":
        return sec_water(ring)
    if material not in SCT or material in ("line", "cut"):
        raise ValueError("sct_hatch_fill: unknown material %r" % material)
    sh = [("poly", ring, SCT[material], None, 0.0)] if fill else []
    SCT_LOG["solid"] += 1
    if fill and k >= SCT_DETAIL_K and material in ("stone", "timber"):
        SCT_LOG["detail"] += 1
        ln = _sec_mix(SCT[material], SEC["ink"], 0.35)
        if material == "stone":                   # bed joints every course, head joints staggered (real size)
            c = SCT_COURSE_M * k
            for p, q in sec_hatch(ring, c, 0.0):
                sh.append(("line", [p, q], ln, 0.06))
            ys = [p[1] for p in ring]
            xs = [p[0] for p in ring]
            import math as _m
            j = int(_m.floor(min(ys) / c))
            while j * c < max(ys):
                x = min(xs) + (0.5 * c if j % 2 else 0.0) + 1.6 * c
                while x < max(xs):
                    for a_, b_ in _sct_clip(ring, (x, j * c), (x, (j + 1) * c)):
                        sh.append(("line", [a_, b_], ln, 0.05))
                    x += 1.6 * c                  # stone length 0.80 m (drawing rule)
                j += 1
        else:                                     # deck boards: vertical joints SCT_BOARD_M apart
            for p, q in sec_hatch(ring, SCT_BOARD_M * k, 90.0):
                sh.append(("line", [p, q], ln, 0.04))
    if outline:
        sh.append(("poly", ring, None, outline, lw))
    return sh


# Soil v2 (round 5, S3, G-R5-4.2, U34/U36/U40/U56/U61/U65: "the top layer a lighter brown, each deeper layer lighter
# still; the layering logic stays"): drawing rules, not measured soil data. A topsoil band SCT_SOIL["top_m"] thick
# in layers[0] at the surface, then the other layers in equal bands following the surface down to the cut bottom,
# each lighter (PLAN §3 values). No hatch over the soil (G-R5-4.1). top / bottom / steps / hatch_lw kept for old reads.
SCT_SOIL = dict(layers=("C2A383", "D0B699", "DDC9B0", "E9DDCB"), top="C2A383", bottom="E9DDCB", top_m=0.30, steps=3,
                hatch_lw=0.053)


def sct_soil_gradient(surface, bottom_y, k):
    """G-R5-4.2 soil under a surface polyline (page mm, left to right) down to bottom_y: the topsoil band (SCT_SOIL
    top_m x k deep under every point of the surface) in layers[0], then one band per further layer, each parallel to
    the surface, lighter going down, the last reaching bottom_y. Opaque fills only, no strokes. Returns shapes."""
    S = [(float(x), float(y)) for x, y in surface]
    if len(S) < 2:
        return []
    t = SCT_SOIL["top_m"] * k
    cols = list(SCT_SOIL["layers"])
    n = len(cols) - 1
    b = float(bottom_y)

    def depth_at(y, f):                       # f = 0 at the topsoil's underside .. 1 at the cut bottom
        top = max(b, y - t)
        return top - (top - b) * f

    sh = [("poly", [(x, y) for x, y in S] + [(x, max(b, y - t)) for x, y in reversed(S)], cols[0], None, 0.0)]
    for i in range(n):
        fa, fb = i / float(n), (i + 1) / float(n)
        ring = [(x, depth_at(y, fa)) for x, y in S] + [(x, depth_at(y, fb)) for x, y in reversed(S)]
        sh.append(("poly", ring, cols[i + 1], None, 0.0))
    return sh


def sct_ground(surface, bottom_y, k, material="earth", lw=0.35):
    """Cut ground under a surface polyline (page mm, left to right) down to bottom_y: its solid material and the cut
    line. material "earth": the soil v2 layers (sct_soil_gradient, G-R5-4.2), no hatch (round 5)."""
    ring = list(surface) + [(surface[-1][0], bottom_y), (surface[0][0], bottom_y)]
    if material == "earth":
        return sct_soil_gradient(surface, bottom_y, k) + [("line", list(surface), SCT["cut"], lw)]
    return sct_hatch_fill(ring, material, k) + [("line", list(surface), SCT["cut"], lw)]


def sct_bed(x0, x1, bed_y, k, depth_m=1.0, material="gravel"):
    """The stream bed from x0 to x1 (page mm) as a cut band depth_m deep (drawing rule, not a surveyed depth)."""
    return sct_ground([(x0, bed_y), (x1, bed_y)], bed_y - depth_m * k, k, material)


def _sct_w(x, side, pts):
    """Local bank points (u landward from x, page y) -> page points."""
    return [(x + side * u, v) for u, v in pts]


def _sct_v_at(S, u):
    """Page y of a local surface S (u rising) at u; on a vertical face the upper end."""
    v = S[0][1] if u <= S[0][0] else S[-1][1]
    for (u0, v0), (u1, v1) in zip(S[:-1], S[1:]):
        if u1 > u0 and u0 <= u <= u1:
            v = v0 + (v1 - v0) * (u - u0) / (u1 - u0)
    return v


def _sct_terr(S, u0, steps, k, t):
    """Local: surface S with a flight of (rise_m, tread_m) steps cut in from u0 landward -> (new S, step rings)."""
    u, v = u0, _sct_v_at(S, u0)
    P, blocks = [(u, v)], []
    for rise, tread in steps:
        v2, u2 = v + rise * k, u + tread * k
        P += [(u, v2), (u2, v2)]
        blocks.append([(u, v - t), (u, v2), (u2, v2), (u2, v - t)])      # each step on its own bed, t below
        u, v = u2, v2
    g = _sct_v_at(S, u)
    if g > v + 1e-6:                          # ground still higher: a retaining face closes the flight
        blocks.append([(u, v - t), (u, g), (u + t, g), (u + t, v - t)])
    if abs(g - v) > 1e-6:
        P.append((u, g))
    S2 = [p for p in S if p[0] < u0 - 1e-9] + P + [p for p in S if p[0] > u + 1e-9]
    return S2, blocks


def sct_terraces(surface, x0, steps, side, k, t_m=0.15, material="concrete"):
    """Steps or terraces [(rise_m, tread_m), ...] cut into a bank surface from page x0, climbing landward (side +1 =
    to the right). Returns (new surface, step shapes); fill the ground under the new surface (sct_ground)."""
    xr = surface[0][0]
    S = [(side * (px - xr), py) for px, py in surface]
    S2, blocks = _sct_terr(S, side * (x0 - xr), steps, k, t_m * k)   # t_m: slab bed, drawing rule (not sourced)
    sh = []
    for b in blocks:
        sh += sct_hatch_fill(_sct_w(xr, side, b), material, k, SCT["cut"], 0.25)
    return _sct_w(xr, side, S2), sh


def _sct_need(p, name, kind):
    if p.get(name) is None:
        raise ValueError("sct_bank %s: %s is required (no sourced value)" % (kind, name))
    return float(p[name])


def sct_bank(kind, x, top_y, bed_y, side, k, **p):
    """One river bank at the cut: kind dsi_wall | embankment | earth | railing | parapet. x = toe (water face of a
    wall), side +1 = land to the right of x. Returns (shapes, surface: page points from the toe landward)."""
    import math as _m
    reach = p.get("reach_m", 4.0) * k        # drawing rule: land drawn 4 m behind the crest
    bot = bed_y - p.get("depth_m", 1.0) * k   # drawing rule: cut ground drawn 1 m below the bed
    sh = []
    if kind == "railing":                     # post with the handrail and mid rail in cut (symbols, no sourced sizes)
        h = _sct_need(p, "h_m", kind) * k
        r = max(0.35, 0.03 * k)
        sh = [("line", [(x, top_y), (x, top_y + h)], SCT["cut"], 0.25),
              ("poly", sec_ellipse(x, top_y + h, r, r, 10), SCT["cut"], None, 0.1),
              ("poly", sec_ellipse(x, top_y + h * 0.5, r * 0.6, r * 0.6, 8), SCT["cut"], None, 0.1)]
        return sh, []
    if kind == "parapet":                     # solid wall on the crest, from x landward
        h, t = _sct_need(p, "h_m", kind) * k, _sct_need(p, "t_m", kind) * k
        ring = [(0.0, top_y), (0.0, top_y + h), (t, top_y + h), (t, top_y)]
        sh = sct_hatch_fill(_sct_w(x, side, ring), p.get("material", "stone"), k, SCT["cut"], 0.35)
        return sh, _sct_w(x, side, [(0.0, top_y + h), (t, top_y + h)])
    if kind == "dsi_wall":                    # the DSİ stone wall; thickness t_m not sourced: required
        t = _sct_need(p, "t_m", kind) * k
        if top_y is None:
            top_y = bed_y + SCT_DSI_WALL_H_M * k
        wall = [(0.0, bed_y), (0.0, top_y), (t, top_y), (t, bed_y)]
        back = [(t, top_y), (t + reach, top_y), (t + reach, bot), (0.0, bot), (0.0, bed_y), (t, bed_y)]
        S = [(0.0, bed_y), (0.0, top_y), (t + reach, top_y)]
        sh += sct_hatch_fill(_sct_w(x, side, back), "earth", k)
        sh += sct_hatch_fill(_sct_w(x, side, wall), p.get("material", "stone"), k, SCT["cut"], 0.35)
        W = _sct_w(x, side, S)
        sh.append(("line", W, SCT["cut"], 0.35))
        return sh, W
    if kind in ("embankment", "earth"):       # angle_deg (toe to crest) or run_m required
        if p.get("run_m") is not None:
            run = float(p["run_m"]) * k
        else:
            run = (top_y - bed_y) / _m.tan(_m.radians(_sct_need(p, "angle_deg", kind)))
        if kind == "embankment":
            S = [(0.0, bed_y), (run, top_y), (run + reach, top_y)]
        else:                                 # loose earth: soft toe and rounded crest, same toe, crest and run
            n = 12
            S = [(run * i / n, bed_y + (top_y - bed_y) * (3 * (i / float(n)) ** 2 - 2 * (i / float(n)) ** 3))
                 for i in range(n + 1)] + [(run + reach, top_y)]
        blocks = []
        if p.get("steps"):
            S, blocks = _sct_terr(S, p.get("steps_from_m", 0.0) * k, p["steps"], k, p.get("step_t_m", 0.15) * k)
        sh += sct_hatch_fill(_sct_w(x, side, S + [(S[-1][0], bot), (0.0, bot)]), p.get("material", "earth"), k)
        if p.get("revet") and kind == "embankment" and not blocks:   # pitching on the slope, revet_t_m thick
            tt = _sct_need(p, "revet_t_m", kind) * k
            L = _m.hypot(run, top_y - bed_y)
            nx, ny = (top_y - bed_y) / L * tt, -run / L * tt              # into the bank
            ring = [(0.0, bed_y), (run, top_y), (run + nx, top_y + ny), (nx, bed_y + ny)]
            sh += sct_hatch_fill(_sct_w(x, side, ring), p["revet"], k, SCT["cut"], 0.2)
        for b in blocks:
            sh += sct_hatch_fill(_sct_w(x, side, b), p.get("step_material", "concrete"), k, SCT["cut"], 0.25)
        W = _sct_w(x, side, S)
        sh.append(("line", W, SCT["cut"], 0.35))
        return sh, W
    raise ValueError("sct_bank: unknown kind %r" % kind)


def sct_profile(left, right):
    """One cross-section line, left to right, from the left bank surface (side -1) and the right one (side +1)."""
    return list(reversed(left)) + list(right)


def sct_channel(profile, wl_y, spacing=0.6):
    """The water standing at page y wl_y in a profile (left to right): sec_water shapes, one per wet stretch."""
    sh, run = [], []
    P = list(profile)
    for i, a in enumerate(P):
        if a[1] < wl_y:
            if not run:
                if i > 0:
                    b = P[i - 1]
                    t = (wl_y - b[1]) / (a[1] - b[1])
                    run.append((b[0] + (a[0] - b[0]) * t, wl_y))
                else:
                    run.append((a[0], wl_y))
            run.append(a)
        elif run:
            b = P[i - 1]
            t = (wl_y - b[1]) / (a[1] - b[1])
            run.append((b[0] + (a[0] - b[0]) * t, wl_y))
            sh += sec_water(run, spacing)
            run = []
    if run:
        run.append((P[-1][0], wl_y))
        sh += sec_water(run, spacing)
    return sh
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
# ---- silhouette.py (round 5 S4, 1 Nov 2026; G-R5-4.4, G-R5-6, N1, D4): one small raster engine, pure Python 3 ------
# Used by figures.py (solid dark bodies of the library people) and plants.py (toned plant images). Included by
# plants.py (#@include), so every script that draws plants or people has it. No Rhino, no PIL; numpy only if present.
#   sil_png_size(path) -> (w, h) | None             PNG / JPEG pixel size from the header only
#   sil_png_read(path) -> (w, h, rgb bytes, n colours 1|3, alpha bytes | None) | None   (8/16 bit, not interlaced)
#   sil_png_write(path, w, h, rgb, alpha)           RGBA (or RGB) 8 bit PNG, filter 0
#   sil_body(rings_m, px_m, close_m, key) -> [ring m]   the filled outline of a pen drawing: rings rasterised,
#                                                   closed (dilate + erode close_m), holes filled, traced, smoothed
#   sil_alpha_body(path, h_m, px_m, close_m, thr) -> ([ring m], w_m)   the same from a PNG's alpha (feet = bottom row)
#   sil_tone(src, dst, shade, mid, light, keep, paper, fade) -> (ok, how)   a plant image toned to its species
#                                                   colours (luminance -> shade/mid/light ramp, keep = share of the
#                                                   photo's own colour kept, then faded toward the paper by fade)
# Bitmaps are lists of Python ints, one per row (bit i = column i), row 0 at the bottom (y up).
import os as _sil_os
import zlib as _sil_zlib
import struct as _sil_st

SIL_LOG = []
_SIL_BODY = {}          # key -> rings (m), one run
_SIL_PNG = {}           # path -> decoded PNG, one run


def sil_png_size(path):
    """(w, h) in pixels of a PNG or JPEG, read from the header; None if unreadable"""
    try:
        with open(path, "rb") as f:
            d = f.read(65536)
    except Exception:
        return None
    if d[:8] == b"\x89PNG\r\n\x1a\n" and d[12:16] == b"IHDR":
        return _sil_st.unpack(">II", d[16:24])
    if d[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(d):
            if d[i] != 0xFF:
                return None
            m = d[i + 1]
            if m in (0xC0, 0xC1, 0xC2):
                return (d[i + 7] << 8) | d[i + 8], (d[i + 5] << 8) | d[i + 6]
            i += 2 + ((d[i + 2] << 8) | d[i + 3])
    return None


def sil_png_read(path):
    """(w, h, rgb bytes, n colours 1|3, alpha bytes or None) of a PNG (8 or 16 bit, grey/RGB/palette, +alpha,
    not interlaced), or None. Rows top to bottom as in the file. Kept in memory for the run."""
    if path in _SIL_PNG:
        return _SIL_PNG[path]
    try:
        with open(path, "rb") as f:
            d = f.read()
    except Exception:
        return None
    if d[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    pos, idat, plte, trns, hdr = 8, [], None, None, None
    while pos + 8 <= len(d):
        n = _sil_st.unpack(">I", d[pos:pos + 4])[0]
        t, c = d[pos + 4:pos + 8], d[pos + 8:pos + 8 + n]
        pos += 12 + n
        if t == b"IHDR":
            hdr = _sil_st.unpack(">IIBBBBB", c[:13])
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
    raw = _sil_zlib.decompress(b"".join(idat))
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
    if bd == 16:
        out = out[0::2]
    n = w * h
    if ct == 3:
        pal = bytes(plte or b"") + b"\x00" * (768 - len(plte or b""))
        rgb = bytearray(n * 3)
        for k_ in range(3):
            rgb[k_::3] = bytes(out).translate(bytes(pal[3 * j + k_] for j in range(256)))
        alpha = bytes(out).translate(bytes(trns or b"") + b"\xff" * (256 - len(trns or b""))) if trns else None
        r = (w, h, bytes(rgb), 3, alpha)
    elif ct == 0:
        r = (w, h, bytes(out), 1, None)
    elif ct == 4:
        r = (w, h, bytes(out[0::2]), 1, bytes(out[1::2]))
    elif ct == 2:
        r = (w, h, bytes(out), 3, None)
    else:
        rgb = bytearray(n * 3)
        rgb[0::3], rgb[1::3], rgb[2::3] = out[0::4], out[1::4], out[2::4]
        r = (w, h, bytes(rgb), 3, bytes(out[3::4]))
    _SIL_PNG[path] = r
    return r


def sil_png_write(path, w, h, rgb, alpha=None):
    """writes an 8 bit RGB(A) PNG (rows top to bottom, filter 0); the folder is made"""
    if alpha is not None:
        px = bytearray(w * h * 4)
        px[0::4], px[1::4], px[2::4], px[3::4] = rgb[0::3], rgb[1::3], rgb[2::3], alpha
        bpp, ct = 4, 6
    else:
        px, bpp, ct = bytes(rgb), 3, 2
    stride = w * bpp
    raw = b"".join(b"\x00" + bytes(px[y * stride:(y + 1) * stride]) for y in range(h))

    def chunk(t, c):
        return _sil_st.pack(">I", len(c)) + t + c + _sil_st.pack(">I", _sil_zlib.crc32(t + c) & 0xffffffff)
    d = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", _sil_st.pack(">IIBBBBB", w, h, 8, ct, 0, 0, 0)) +
         chunk(b"IDAT", _sil_zlib.compress(raw, 6)) + chunk(b"IEND", b""))
    _sil_os.makedirs(_sil_os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(d)


# ---- bitmaps (rows of ints) -------------------------------------------------------------------------------------------
def _sil_fill_ring(rows, ring, x0, y0, px, W):
    """ORs the inside of one closed ring (m) into rows (even-odd scanline at each row's centre)"""
    n = len(ring)
    if n < 3:
        return
    ys = [p[1] for p in ring]
    r0 = max(0, int((min(ys) - y0) / px) - 1)
    r1 = min(len(rows) - 1, int((max(ys) - y0) / px) + 1)
    full = (1 << W) - 1
    for r in range(r0, r1 + 1):
        yc = y0 + (r + 0.5) * px
        xs = []
        for i in range(n):
            ax, ay = ring[i]
            bx, by = ring[(i + 1) % n]
            if (ay <= yc < by) or (by <= yc < ay):
                xs.append(ax + (yc - ay) * (bx - ax) / (by - ay))
        xs.sort()
        m = 0
        for a, b in zip(xs[0::2], xs[1::2]):
            c0 = max(0, int(round((a - x0) / px)))
            c1 = min(W, int(round((b - x0) / px)))
            if c1 <= c0 and b - a > 0:                  # a sliver thinner than a pixel still marks one
                c0 = min(W - 1, max(0, int((0.5 * (a + b) - x0) / px)))
                c1 = c0 + 1
            if c1 > c0:
                m |= ((1 << (c1 - c0)) - 1) << c0
        rows[r] |= m & full


def _sil_dilate(rows, W, r):
    full = (1 << W) - 1
    hz = []
    for v in rows:
        a = v
        for i in range(1, r + 1):
            a |= (v << i) | (v >> i)
        hz.append(a & full)
    H = len(rows)
    out = []
    for y in range(H):
        a = 0
        for yy in range(max(0, y - r), min(H, y + r + 1)):
            a |= hz[yy]
        out.append(a)
    return out


def _sil_erode(rows, W, r):
    full = (1 << W) - 1
    inv = [(~v) & full for v in rows]
    # outside the grid counts as empty: pad so the border erodes (the grid has a margin > r, so this never bites)
    d = _sil_dilate(inv, W, r)
    return [(~v) & full for v in d]


def _sil_fill_holes(rows, W):
    """every empty region not connected to the grid border becomes filled"""
    full = (1 << W) - 1
    H = len(rows)
    emp = [(~v) & full for v in rows]
    edge = 1 | (1 << (W - 1))
    ext = [emp[y] if y in (0, H - 1) else (emp[y] & edge) for y in range(H)]
    changed = True
    while changed:
        changed = False
        for y in list(range(H)) + list(range(H - 1, -1, -1)):
            a = ext[y]
            b = a | (a << 1) | (a >> 1)
            if y > 0:
                b |= ext[y - 1]
            if y < H - 1:
                b |= ext[y + 1]
            b &= emp[y]
            while True:                                 # run along the row at once
                c = (b | (b << 1) | (b >> 1)) & emp[y]
                if c == b:
                    break
                b = c
            if b != a:
                ext[y] = b
                changed = True
    return [full & ~e for e in ext]


def _sil_bits(v):
    i = 0
    while v:
        if v & 1:
            yield i
        v >>= 1
        i += 1


def _sil_trace(rows, W):
    """outer outlines (lattice points, counter-clockwise) of the filled cells; holes must be filled before"""
    H = len(rows)
    full = (1 << W) - 1
    nxt = {}

    def add(a, b):
        nxt.setdefault(a, []).append(b)
    for y in range(H):
        v = rows[y]
        if not v:
            continue
        below = rows[y - 1] if y > 0 else 0
        above = rows[y + 1] if y < H - 1 else 0
        for x in _sil_bits(v & ~below & full):
            add((x, y), (x + 1, y))
        for x in _sil_bits(v & ~(v >> 1) & full):           # right neighbour empty
            add((x + 1, y), (x + 1, y + 1))
        for x in _sil_bits(v & ~above & full):
            add((x + 1, y + 1), (x, y + 1))
        for x in _sil_bits(v & ~(v << 1) & full):           # left neighbour empty
            add((x, y + 1), (x, y))
    loops = []
    while nxt:
        start = next(iter(nxt))
        loop, cur, prev_d = [start], start, None
        while True:
            outs = nxt.get(cur)
            if not outs:
                break
            if len(outs) > 1 and prev_d is not None:        # a pinch: turn right first (keeps the parts apart)
                def turn(b, _c=cur, _d=prev_d):
                    d = (b[0] - _c[0], b[1] - _c[1])
                    return _d[0] * d[1] - _d[1] * d[0]       # < 0 right, 0 straight, > 0 left
                outs.sort(key=turn)
            b = outs.pop(0)
            if not outs:
                del nxt[cur]
            prev_d = (b[0] - cur[0], b[1] - cur[1])
            cur = b
            if cur == start:
                break
            loop.append(cur)
        if len(loop) >= 4:
            loops.append(loop)
    return loops


def _sil_area(P):
    return 0.5 * sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))


def _sil_dp(P, tol):
    """Douglas-Peucker on a closed ring"""
    if len(P) < 5:
        return P
    i_far = max(range(len(P)), key=lambda i: (P[i][0] - P[0][0]) ** 2 + (P[i][1] - P[0][1]) ** 2)

    def dp(Q):                                          # iterative (long staircases never hit the recursion limit)
        keep = [False] * len(Q)
        keep[0] = keep[-1] = True
        st = [(0, len(Q) - 1)]
        while st:
            i0, i1 = st.pop()
            if i1 - i0 < 2:
                continue
            (ax, ay), (bx, by) = Q[i0], Q[i1]
            L = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5 or 1e-9
            dm, im = -1.0, i0
            for i in range(i0 + 1, i1):
                d = abs((bx - ax) * (ay - Q[i][1]) - (ax - Q[i][0]) * (by - ay)) / L
                if d > dm:
                    dm, im = d, i
            if dm > tol:
                keep[im] = True
                st += [(i0, im), (im, i1)]
        return [q for q, k_ in zip(Q, keep) if k_]
    a = dp(P[:i_far + 1])
    b = dp(P[i_far:] + [P[0]])
    return a[:-1] + b[:-1]


def _sil_chaikin(P, n=2):
    for _ in range(n):
        Q = []
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            Q += [(0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]), (0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1])]
        P = Q
    return P


def _sil_outline(rows, W, x0, y0, px, close_px, min_px=6):
    """closed, hole-filled, traced and smoothed outlines (m) of a bitmap"""
    if close_px > 0:
        rows = _sil_erode(_sil_dilate(rows, W, close_px), W, close_px)
    rows = _sil_fill_holes(rows, W)
    out = []
    for L in _sil_trace(rows, W):
        if abs(_sil_area(L)) < min_px:
            continue
        P = _sil_chaikin(_sil_dp([(float(a), float(b)) for a, b in L], 0.6), 2)
        out.append([(x0 + a * px, y0 + b * px) for a, b in P])
    return out


def sil_body(rings_m, px_m=0.01, close_m=0.05, key=None):
    """the solid outline(s) of a drawing made of closed rings (m, y up): rasterised at px_m, closed by close_m
    (gaps between pen strokes up to about 2 x close_m fill), inner holes filled, outer edge traced and smoothed.
    Returns [ring (m)]; [] for nothing. key: memo for the run."""
    if key is not None and key in _SIL_BODY:
        return _SIL_BODY[key]
    pts = [p for r in rings_m for p in r]
    if not pts:
        return []
    cp = max(0, int(round(close_m / px_m)))
    pad = (cp + 3) * px_m
    x0, y0 = min(p[0] for p in pts) - pad, min(p[1] for p in pts) - pad
    W = int((max(p[0] for p in pts) + pad - x0) / px_m) + 1
    H = int((max(p[1] for p in pts) + pad - y0) / px_m) + 1
    rows = [0] * H
    for r in rings_m:
        _sil_fill_ring(rows, r, x0, y0, px_m, W)
    out = _sil_outline(rows, W, x0, y0, px_m, cp)
    if key is not None:
        _SIL_BODY[key] = out
    return out


def sil_alpha_body(path, h_m, px_m=0.01, close_m=0.02, thr=128):
    """([ring m], w_m): the solid outline of a cutout PNG from its alpha (alpha > thr), scaled so the image is h_m
    tall, feet = the bottom row at y 0, x centred. ([], 0) if unreadable or with no alpha."""
    key = ("alpha", path, round(h_m, 3), px_m, close_m, thr)
    if key in _SIL_BODY:
        return _SIL_BODY[key]
    r = sil_png_read(path)
    if not r or r[4] is None:
        SIL_LOG.append(u"silhouette: %s has no alpha" % _sil_os.path.basename(path))
        _SIL_BODY[key] = ([], 0.0)
        return _SIL_BODY[key]
    w, h, _rgb, _nc, al = r
    m_px = h_m / float(h)                                    # m per image pixel
    step = max(1, int(px_m / m_px))
    W, H = (w + step - 1) // step + 6, (h + step - 1) // step + 6
    rows = [0] * H
    for yy in range(0, h, step):
        ln = al[yy * w:(yy + 1) * w:step]
        v = 0
        for i, a in enumerate(ln):
            if a > thr:
                v |= 1 << (i + 3)
        rows[(h - 1 - yy) // step + 3] = v                   # image top row -> highest bitmap row
    px = m_px * step
    cp = max(0, int(round(close_m / px)))
    out = _sil_outline(rows, W, -(w * m_px) / 2.0 - 3 * px, -3 * px, px, cp)
    if out:                                                  # feet exactly on y 0
        y_min = min(p[1] for R in out for p in R)
        out = [[(a, b - y_min) for a, b in R] for R in out]
    _SIL_BODY[key] = (out, w * m_px)
    return _SIL_BODY[key]


# ---- the cutout library (Data/cutouts/cutouts.json; recovered from a936d62:src/common/figures.py:747-792, round 5) --------
# {"cutouts": {key: entry or [entries]}}, entry = {"file", "h_m" (true height of what the PNG shows, bottom edge =
# ground/feet), "kind", "facing" (-1 = looks left; default +1), "depth": {"1": file, "2": file}, ...}. Keys: plants =
# the plants.py species key ("olive"), people = "person_<pose>", "stall". Read once per run.
_SIL_CUT = {}


def sil_cut_dir():
    return _sil_os.path.join(_sil_os.path.expanduser("~"), "Downloads", "Bergama", "Data", "cutouts")


def sil_cut_library():
    """{key: [entry, ...]} from cutouts.json (entries whose file exists), {} when the folder or file is missing"""
    import json as _j
    if "lib" in _SIL_CUT:
        return _SIL_CUT["lib"]
    lib = {}
    p = _sil_os.path.join(sil_cut_dir(), "cutouts.json")
    try:
        with open(p, "r", encoding="utf-8") as fh:
            js = _j.load(fh)
        js = js.get("cutouts", js) if isinstance(js, dict) else {}
        for k_, v in js.items():
            vs = v if isinstance(v, list) else [v]
            ok = [e for e in vs if isinstance(e, dict) and e.get("file") and e.get("h_m") and
                  _sil_os.path.isfile(_sil_os.path.join(sil_cut_dir(), e["file"]))]
            if ok:
                lib[k_] = ok
        SIL_LOG.append(u"cutouts: %d keys from %s" % (len(lib), p))
    except Exception as ex:
        SIL_LOG.append(u"FLAG cutouts: %s not read (%s)" % (p, type(ex).__name__))
    _SIL_CUT["lib"] = lib
    return lib


# ---- toning (plants) ----------------------------------------------------------------------------------------------------
def _sil_hex(c):
    return [int(c[i:i + 2], 16) for i in (0, 2, 4)]


def sil_tone(src, dst, shade, mid, light, keep=0.25, paper="F1EDDF", fade=0.0):
    """writes dst: the PNG src toned to a species' colours. Each pixel's luminance (stretched between the 2nd and
    98th percentile of the opaque pixels) maps onto the ramp shade -> mid -> light; keep (0-1) of the photo's own
    colour is mixed back (flowers stay visible); then everything is mixed toward the paper by fade (depth). Alpha
    unchanged. With numpy: as above; without: the ramp from the green channel only (keep ignored).
    Returns (True, "numpy"|"lut") or (False, why)."""
    r = sil_png_read(src)
    if not r:
        return False, "unreadable PNG"
    w, h, rgb, nc, al = r
    S, M_, L_, P = _sil_hex(shade), _sil_hex(mid), _sil_hex(light), _sil_hex(paper)
    try:
        import numpy as _np
    except Exception:
        _np = None
    if _np is not None:
        a = _np.frombuffer(rgb, dtype=_np.uint8).reshape(-1, nc).astype(_np.float32)
        if nc == 1:
            a = _np.repeat(a, 3, axis=1)
        lum = 0.2126 * a[:, 0] + 0.7152 * a[:, 1] + 0.0722 * a[:, 2]
        op = lum if al is None else lum[_np.frombuffer(al, dtype=_np.uint8) > 128]
        if op.size < 10:
            op = lum
        lo, hi = _np.percentile(op, 2), _np.percentile(op, 98)
        t = _np.clip((lum - lo) / max(1.0, hi - lo), 0.0, 1.0)[:, None]
        S_, M2, L2 = (_np.array(c, dtype=_np.float32)[None, :] for c in (S, M_, L_))
        duo = _np.where(t < 0.5, S_ + (M2 - S_) * (t / 0.5), M2 + (L2 - M2) * ((t - 0.5) / 0.5))
        out = duo * (1.0 - keep) + a * keep
        out = out + (_np.array(P, dtype=_np.float32)[None, :] - out) * fade
        sil_png_write(dst, w, h, _np.clip(out + 0.5, 0, 255).astype(_np.uint8).tobytes(), al)
        return True, "numpy"
    g = rgb[1::3] if nc == 3 else rgb
    gs = sorted(g[::97]) or [0, 255]
    lo, hi = gs[int(0.02 * (len(gs) - 1))], gs[int(0.98 * (len(gs) - 1))]
    lut = [bytearray(256) for _ in range(3)]
    for v in range(256):
        t = min(1.0, max(0.0, (v - lo) / float(max(1, hi - lo))))
        for c in range(3):
            x = S[c] + (M_[c] - S[c]) * t / 0.5 if t < 0.5 else M_[c] + (L_[c] - M_[c]) * (t - 0.5) / 0.5
            x = x + (P[c] - x) * fade
            lut[c][v] = int(max(0, min(255, round(x))))
    out = bytearray(w * h * 3)
    for c in range(3):
        out[c::3] = bytes(g).translate(bytes(lut[c]))
    sil_png_write(dst, w, h, bytes(out), al)
    return True, "lut"
# ---- round 5 (S4, 1 Nov 2026; G-R5-6, D4, D10, N2 a): PLANT MODULE v3. Every pla_section / pla_plan / pla_axo /
# pla_bare / crop call draws the species from a real image per species x state (see "plant module v3" above
# pla_section), toned to its colours; the round 4 vector drawing below stays only as the counted, FLAGged fallback
# where no image exists yet (pla_missing), so the pages never go blank before the asset project delivers
# Data/plants/. Interfaces unchanged. silhouette.py (included above) holds the PNG reader/writer and the toning.
# ---- round 4 (S3, 1 Nov 2026; D1, D4, D6 states, D7, G-R4-5.2, G-R4-5.8, G-R4-6): ONE vector drawing per species for
# every plan, section, view, axo (pla_axo) and the p17 catalogue: white willow v2, print-quality crowns of two-tone
# leaf masses with gaps, a shrub/flower low layer (pla_low_section / pla_low_plan), season= on every call (None =
# general; month= alias), crops and cells in their season state. Colours = round 3 values, all pending
# research/plant_colours.md (PLA_COLOUR_SRC; log FLAG). No cutouts or high-res silhouettes for plants any more.
# ---- plants (WO-T2b-3, 29 Oct 2026): every species of the revised planting as ONE primitive with two matching views,
# pla_section() (silhouette on the ground) and pla_plan() (top-view crown): same crown width, form and colour. Crops
# as rows at their spacing. Common reed and water mint only inside lined, off-line cells (D2 a, D6), never free.
# Needs section_parts.py (SEC, sec_ellipse, sec_water, _sec_mix, sct_hatch_fill) included before this file.
# Data: revision_2026-10-29/T1/ecology/species.json "species_data" (S-numbers as there) and RESULT.md §A-B.
# Removed by D6 and not offered: yellow flag iris, oleander, broadleaf cattail, white poplar, fig, citrus (and elm).
# Drawing size rules (the sources give ranges or only a maximum; data comments only, never printed):
#   height h_m  = middle of the sourced mature range; half of it where only a maximum is sourced.
#   crown crown_m = middle of the sourced spread; half of a sourced maximum; where no spread is sourced,
#                 h_m x PLA_FORM_RATIO[form] (rule read from the crown words in species.json).
#   clear stem, trunk width, lobes and stem counts: form rules in _pla_sec (drawing rules).
#   ("poly", ring, fill, stroke, lw)    ("line", pts, colour, lw)          page mm, y up; k = page mm per m

PLA_FORM_RATIO = dict(dome=1.0, oval=0.7, weeping=0.7, gnarled=0.9, umbrella=0.55, feathery=0.8, clump=0.6,
                      tussock=1.0, mound=1.2)   # crown / height where no spread is sourced (drawing rule)

PLA_LEAF_SITE = [4, 5, 6, 7, 8, 9, 10, 11]   # leaf-out 16 Apr, leaf-fall 14 Nov: site Sentinel-2 2019-2025 for all
                                             # broadleaved deciduous crowns (selinus_board_v50 LEAF_DOY; RESULT §B)
PLA_ALL_YEAR = list(range(1, 13))

PLA_PURPLE = "8C7088"     # palette SCHEMES D1 institutional / D5 civic: loosestrife purple (RESULT §A "purple, Jun-Sep")
PLA_REMOVE = "8B3A3F"     # palette CORE accent: the 'remove' cross on giant reed
PLA_FIELD = "C6C08D"      # palette MASTERPLAN agriculture light: field ground
PLA_ROW = "948B49"        # palette MASTERPLAN agriculture mid: crop rows
PLA_WET = "CBEDE5"        # palette MASTERPLAN wetland light: lined cell in plan
PLA_BOLL = "FAF8F1"       # palette CORE road: cotton bolls
PLA_FRUIT = "BC6F45"      # palette SCHEMES D1 commercial: tomato fruit
# round 4 (S3, G-R4-6): the greenery colours plants.py read from section_parts SEC, copied here with the same values so
# that no greenery colour lives outside this module (SEC's greenery keys can go at closing). Pending research as all.
PLA_LAV = "9F86C0"        # = SEC lav: chaste tree / French lavender flowers
PLA_REED_HEAD = "B49A6C"  # = SEC reed_head: reed plumes, rush tufts, maize tassels
PLA_CROP_LEAF = "8F9A68"  # = SEC grass: cotton, maize, tomato leaves
PLA_TRUNK = "7A6E60"      # = SEC trunk: stems and trunks
PLA_BEYOND = _sec_mix("7E8A57", SEC["paper"], 0.62)   # = SEC beyond (tree 7E8A57 toward paper): giant reed


def _pla_c(fill, accent=None, stem=None):
    """The colour set of one species: fill, edge, lighter lobes, stem, accent (same in both views)."""
    return dict(fill=fill, edge=SEC["ink2"], lt=_sec_mix(fill, SEC["paper"], 0.35), stem=stem or PLA_TRUNK,
                accent=accent)


# one entry per species (species.json species_data + giant reed from the screening); h_range = sourced (lo, hi) m
PLA_SPECIES = {
    "plane": dict(name="Oriental plane", turkish="Doğu çınarı", latin="Platanus orientalis", layer="tree",
                  form="dome", foliage="deciduous (S26)", status="keep",
                  h_range=(None, 30.0), h_m=15.0,            # "up to 30 m" S68, S69
                  crown_m=15.0,                              # "wider than 8 metres" S70: form rule 1.0 x h (>= 8)
                  bloom=[4, 5], leaf=PLA_LEAF_SITE,          # Apr-May S69 (secondary)
                  colours=_pla_c("637F48")),                  # round 3 species colour (D7; ΔE00 >= 12.7); every colour: PLA_COLOUR_SRC
    "ash": dict(name="Narrow-leaved ash", turkish="Dişbudak", latin="Fraxinus angustifolia", layer="tree",
                form="oval", foliage="deciduous (S7)", status="keep",
                h_range=(None, 40.0), h_m=20.0,              # "40-45m" maximum S7 (lower figure)
                crown_m=14.0,                                # "dense, irregular and dome shaped" S7: rule 0.7 x h
                bloom=[], leaf=PLA_LEAF_SITE,                # "early spring or even in autumn" S7: no months
                colours=_pla_c("3E6C5D")),                # round 3: blue-green
    "willow": dict(name="White willow", turkish="Ak söğüt", latin="Salix alba", layer="tree",
                   form="weeping", foliage="deciduous (not quoted)", status="keep",
                   h_range=(None, 30.0), h_m=15.0,           # "up to 30 m" S4
                   crown_m=10.5,                             # crown not found: rule 0.7 x h
                   bloom=[], leaf=PLA_LEAF_SITE,             # "spring" catkins S4: no months
                   colours=_pla_c("A9B88A")),                   # round 3: silvery light green
    "olive": dict(name="Olive", turkish="Zeytin", latin="Olea europaea", layer="tree",
                  form="gnarled", foliage="evergreen (S72)", status="keep",
                  h_range=(8.0, 15.0), h_m=11.5,             # "8-15 m" S72
                  crown_m=10.35,                             # crown not found: rule 0.9 x h
                  bloom=[4], leaf=PLA_ALL_YEAR,              # full bloom 21-24 Apr, ends 29 Apr-1 May S73 (Ege Univ.)
                  colours=_pla_c("7D8C80")),                  # round 3: grey-green
    "stone_pine": dict(name="Stone pine", turkish="Fıstık çamı", latin="Pinus pinea", layer="tree",
                       form="umbrella", foliage="evergreen conifer (S74)", status="keep (processionary caterpillar)",
                       h_range=(25.0, 30.0), h_m=27.5,       # "25-30 m" S74
                       crown_m=15.1,                         # "umbrella-shaped ... flat and broad" S74: rule 0.55 x h
                       bloom=[], leaf=PLA_ALL_YEAR,          # pollen months not found
                       colours=_pla_c("31432E")),              # round 3: deep green
    "tamarisk": dict(name="Tamarisk", turkish="Ilgın", latin="Tamarix smyrnensis", layer="tree",
                     form="feathery", foliage="deciduous (S9b, genus)", status="keep (replaces oleander)",
                     h_range=(4.0, 15.0), h_m=9.5,           # "4-15 m" S9b (genus)
                     crown_m=7.6,                            # "broad, bushy" S9b: rule 0.8 x h
                     bloom=[], leaf=PLA_LEAF_SITE,           # bloom not found for T. smyrnensis
                     colours=_pla_c("9AA9B3")),                # round 3: glaucous blue-grey
    "chaste": dict(name="Chaste tree", turkish="Hayıt", latin="Vitex agnus-castus", layer="shrub",
                   form="multistem", foliage="deciduous (S58)", status="keep (replaces oleander, fig, citrus)",
                   h_range=(1.0, 3.0), h_m=2.0,              # "1-3 m" S58
                   crown_m=2.0,                              # "1.5-2.5 m" S67 (RHS, UK)
                   bloom=[6, 7, 8, 9], leaf=PLA_LEAF_SITE,   # "(Apr-)Jun-Sep" S58 (Crete); Apr-May occasional
                   colours=_pla_c("928955", PLA_LAV)),       # round 3: khaki; flower colour not sourced: section_style lav
    "rosemary": dict(name="Rosemary", turkish="Biberiye", latin="Salvia rosmarinus", layer="shrub",
                     form="mound", foliage="evergreen (S58, S71)", status="keep",
                     h_range=(0.5, 1.0), h_m=0.75,           # "50-100 cm" S58 (Crete)
                     crown_m=0.75,                           # "1.5-2.5 m" S71 for 1.5-2.5 m plants: scaled to h
                     bloom=[1, 2, 3, 4, 5], leaf=PLA_ALL_YEAR,  # "Jan-May, intermittently to Dec" S58
                     colours=_pla_c("5E6356")),                # round 3: dark grey-green
    "lavender": dict(name="French lavender", turkish="Karabaş otu", latin="Lavandula stoechas", layer="ground",
                     form="mound", foliage="evergreen (UNVERIFIED)", status="keep",
                     h_range=(0.3, 0.8), h_m=0.55,           # "30-80 cm" S58
                     crown_m=0.66,                           # crown not found: rule 1.2 x h
                     bloom=[3, 4, 5], leaf=[],               # "Mar-May" S58; evergreen unverified: no leaf months
                     colours=_pla_c("B6AFC3", PLA_LAV)),      # round 3: lilac grey; flowers as sec_lavender
    "loosestrife": dict(name="Purple loosestrife", turkish="Aklar otu", latin="Lythrum salicaria", layer="emergent",
                        form="clump", foliage="herbaceous perennial", status="keep, flower heads cut in Sep (D6)",
                        h_range=(0.3, 2.4), h_m=1.35,        # "0.3-2.4 m" S19
                        crown_m=0.75,                        # "5 feet (1.5 m) wide" mature S19: half the maximum
                        bloom=[6, 7, 8, 9], leaf=[],         # "June ... September" S19; cut Sep (D6)
                        colours=_pla_c("5C9D74", PLA_PURPLE)),     # round 3: fresh blue-green
    "soft_rush": dict(name="Soft rush", turkish="UNVERIFIED", latin="Juncus effusus", layer="emergent",
                      form="clump", foliage="not found", status="new (replaces iris and cattail)",
                      h_range=(0.5, 1.5), h_m=1.0,           # "5-15 dm tall" S59
                      crown_m=0.6,                           # "tufted, cespitose" S59: rule 0.6 x h
                      bloom=[5, 6, 7, 8], leaf=[],           # "late May-Aug, occasionally Sep" S59 (USA)
                      colours=_pla_c("7C9A2E")),               # round 3: rush green
    "rush": dict(name="Sharp rush", turkish="Kofa", latin="Juncus acutus", layer="emergent",
                 form="tussock", foliage="not found", status="keep, away from paths and the wading strip",
                 h_range=(0.6, 1.0), h_m=0.8,                # "(40-)60-100 cm" S65
                 crown_m=0.8,                                # "dense tussock" S60, S65: rule 1.0 x h
                 bloom=[], leaf=[],                          # "summer" S65 (NZ): no months
                 colours=_pla_c("515B26")),                # round 3: dark olive
    "reed": dict(name="Common reed", turkish="Kamış", latin="Phragmites australis", layer="emergent",
                 form="stand", foliage="deciduous (S2)", status="lined off-line basins only (D2 a): pla_reed_basin",
                 h_range=(None, 6.0), h_m=3.0,               # "may reach 20 feet (6 m)" S2 (booklet drew 1.9-2.2 m)
                 crown_m=None,                               # clonal stand, no crown
                 bloom=[7, 8, 9, 10, 11], leaf=[],           # "July to November" S2 (range-wide); plumes cut before Nov
                 colours=_pla_c("C2A873", PLA_REED_HEAD)),   # round 3: straw (ΔE00 12.4 to the free-planted species)
    "mint": dict(name="Water mint", turkish="Su nanesi", latin="Mentha aquatica", layer="emergent",
                 form="mound", foliage="deciduous (S57)", status="lined basin cells only (D6): pla_mint_cell",
                 h_range=(0.3, 0.8), h_m=0.55,               # "30-80 cm" S58
                 crown_m=0.75,                               # "spread 0.5-1 m" S57
                 bloom=[5, 6, 7, 8, 9], leaf=[],             # "May-Sep" S58
                 colours=_pla_c("5F9C9E")),                # round 3: blue mint green (ΔE00 12.8)
    "giant_reed": dict(name="Giant reed", turkish="Kargı", latin="Arundo donax", layer="emergent",
                       form="cane", foliage="not found", status="REMOVE (raises flood risk, S36)",
                       h_range=(None, None), h_m=None, crown_m=None,   # not in species_data: pass h_m and crown_m
                       bloom=[], leaf=[],
                       colours=_pla_c(PLA_BEYOND, PLA_REMOVE)),
}

# crops: row spacing only where sourced (library/research/crops_2026-10-24, card f506; no other spacing in library/)
PLA_CROPS = {
    "olive": dict(name="Olive orchard", row_m=7.0, plant_m=5.0,   # Kaya et al. 2017 Irrig. Drain. 66(5) p.821:
                  h_m=None, crown_m=None),     # Memecik "planted 5 × 7 m apart" (order of the pair not stated)
    "cotton": dict(name="Cotton", row_m=None, plant_m=None, h_m=None, crown_m=None),   # not found: pass spacing
    "maize": dict(name="Maize (corn)", row_m=None, plant_m=None, h_m=None, crown_m=None),   # not found
    "tomato": dict(name="Tomato (processing)", row_m=None, plant_m=None, h_m=None, crown_m=None),   # not found
}


def pla_months(key):
    """Sourced months (1-12) of a species: bloom, in leaf and flower-head cut (empty lists where not sourced)."""
    sp = PLA_SPECIES[key]
    return dict(bloom=list(sp["bloom"]), leaf=list(sp["leaf"]), cut=[9] if key == "loosestrife" else [])


# ---- round 4 (S3, D6, G-R4-6; PLAN §4.9, §2.1): seasons, states and colours ------------------------------------------
# Every plant call takes season= (None = the general state; "winter" Dec-Feb, "spring" Mar-May, "summer" Jun-Aug,
# "autumn" Sep-Nov); month= (1-12) is kept as an alias that maps to its season. The STATE of a species in a season
# comes from its sourced months only (leaf list, bloom list, flower heads cut; CHK5_6 §4): a deciduous species with no
# leaf month in the season is bare (winter: branches with open gaps, round 3 D7); spring = after leaf-out (fresh
# tint); autumn = before leaf-fall (warm tint); flowers where a bloom month falls in the season and is not a cut
# month. The general state = the species in leaf with its flowers (U69). COLOURS: the round 3 values are kept as they
# are (Aras 1 Nov 11:42, N2 halted till 2 Nov): none is sourced yet, every colour entry carries src = PLA_COLOUR_SRC
# and the log prints "FLAG plant colours pending research". Next round fills PLA_SPECIES colours, the two tints and
# the crop colours from research/plant_colours.md (one data edit here). Never alpha.
PLA_COLOUR_SRC = "pending research/plant_colours.md"
PLA_SEASONS = ("winter", "spring", "summer", "autumn")
PLA_SEASON_MONTHS = dict(winter=(12, 1, 2), spring=(3, 4, 5), summer=(6, 7, 8), autumn=(9, 10, 11))
PLA_SPRING = "B8C77A"      # fresh leaf tint (round 3 drawing rule, kept; colour pending research)
PLA_AUTUMN = "C29A55"      # autumn tint (round 3 drawing rule, kept; colour pending research)
PLA_TINT = dict(spring=PLA_SPRING, autumn=PLA_AUTUMN)
PLA_TINT_T = dict(spring=0.22, autumn=0.35)   # round 3 month tints (Apr .30 May .15 / Sep .15 Oct .35 Nov .55) averaged
PLA_SEASON = dict(season=None)   # pla_season(s): every plant call without season= / month= draws season s
PLA_BARE_DRAWN = set()
# where each species' STATES come from (colours: PLA_COLOUR_SRC for all); the S-numbers as in species.json
PLA_STATE_SRC = dict(
    plane="leaf: site Sentinel-2 leaf-out 16 Apr, leaf-fall 14 Nov (RESULT §B); bloom Apr-May S69",
    ash="leaf: site Sentinel-2; bloom 'early spring or even in autumn' S7 (no months: no flowers drawn)",
    willow="leaf: site Sentinel-2; catkins 'spring' S4 (no months: none drawn)",
    olive="evergreen S72; full bloom 21-24 Apr S73; harvest 6-14 Nov (Kaya 2017)",
    stone_pine="evergreen conifer S74",
    tamarisk="leaf: site Sentinel-2 (deciduous S9b, genus); bloom not sourced",
    chaste="leaf: site Sentinel-2 (deciduous S58); bloom (Apr-)Jun-Sep S58",
    rosemary="evergreen S58, S71; bloom Jan-May S58",
    lavender="evergreen UNVERIFIED; bloom Mar-May S58",
    loosestrife="herbaceous perennial; bloom Jun-Sep S19; heads cut Sep (D6); winter state not sourced",
    soft_rush="bloom late May-Aug S59; winter state not sourced",
    rush="bloom 'summer' S65 (no months); winter state not sourced",
    reed="deciduous S2; plumes Jul-Nov S2, cut before Nov S11",
    mint="deciduous S57; bloom May-Sep S58 (no flower colour)",
    giant_reed="remove (S36)",
)
PLA_SOURCES = dict((k_, dict((s_, dict(colour=PLA_COLOUR_SRC, state=PLA_STATE_SRC.get(k_, "")))
                             for s_ in (None,) + PLA_SEASONS)) for k_ in PLA_SPECIES)


def pla_season_of(season=None, month=None):
    """the season name of season= or month= (a month 1-12 maps to its season); None = the general state"""
    if season is not None:
        if season not in PLA_SEASONS:
            raise ValueError("plants: season is None or one of %s, not %r" % (", ".join(PLA_SEASONS), season))
        return season
    if month:
        m = int(month)
        for s_ in PLA_SEASONS:
            if m in PLA_SEASON_MONTHS[s_]:
                return s_
        raise ValueError("plants: month %r is not 1-12" % month)
    return None


def pla_season(season=None):
    """sets the season (a name, or a month 1-12 = its season; None = general) every plant call without its own
    season= / month= draws in; returns the previous season (pla_season(old) restores it)"""
    old = PLA_SEASON["season"]
    if isinstance(season, (int, float)) and not isinstance(season, bool):
        PLA_SEASON["season"] = pla_season_of(month=season) if season else None
    else:
        PLA_SEASON["season"] = pla_season_of(season or None)
    return old


def _pla_s(season=None, month=None):
    """the season of one call: its own season= / month=, else the one set by pla_season"""
    if season is not None or month:
        return pla_season_of(season, month)
    return PLA_SEASON["season"]


def _pla_deciduous(sp):
    return sp["foliage"].startswith("deciduous") and bool(sp["leaf"])


def pla_state(key, season=None):
    """the sourced state of species `key` in a season: dict(bare, tint, bloom, season) (PLA_STATE_SRC)"""
    sp = PLA_SPECIES[key]
    if season is None:
        return dict(bare=False, tint=None, bloom=bool(sp["colours"].get("accent")), season=None)
    ms = PLA_SEASON_MONTHS[season]
    cut = pla_months(key)["cut"]
    dec = _pla_deciduous(sp)
    bare = dec and not any(m in sp["leaf"] for m in ms)
    tint = season if dec and not bare and season in PLA_TINT else None
    bloom = any(m in sp["bloom"] and m not in cut for m in ms)
    return dict(bare=bare, tint=tint, bloom=bloom, season=season)


def pla_colours(key, season=None, beyond=False, layer=0, month=None):
    """THE plant colour call (G-R4-6): the colour set of species `key` in `season` (None = general; month= alias):
    fill (lit face), shade (mass body), lt (light fleck), edge, stem, bark, accent (flowers; None out of bloom; giant
    reed keeps its 'remove' cross), plus bare (draw the winter structure), bloom, season and src (the colour source:
    PLA_COLOUR_SRC until research/plant_colours.md). beyond / layer: paler beyond the cut and with depth (fig_fade).
    Opaque colours only."""
    sp = PLA_SPECIES[key]
    s_ = _pla_s(season, month)
    st = pla_state(key, s_)
    c = dict(sp["colours"])
    if st["tint"]:
        c["fill"] = _sec_mix(c["fill"], PLA_TINT[st["tint"]], PLA_TINT_T[st["tint"]])
        c["lt"] = _sec_mix(c["fill"], SEC["paper"], 0.35)
    if key != "giant_reed" and c.get("accent") and not st["bloom"]:
        c["accent"] = None
    c["shade"] = _sec_mix(c["fill"], c["edge"], 0.25)
    if beyond:
        c = dict((k_, _sec_mix(v, SEC["paper"], 0.55) if v else v) for k_, v in c.items())
    c = _pla_layer_cols(c, layer)
    bark = _sec_mix(sp["colours"]["fill"], sp["colours"]["stem"] or PLA_TRUNK, 0.6)   # species-tinted twigs
    if beyond:
        bark = _sec_mix(bark, SEC["paper"], 0.55)
    c["bark"] = _pla_layer_cols(dict(b=bark), layer)["b"]
    c.update(bare=st["bare"], bloom=st["bloom"], season=s_, src=PLA_COLOUR_SRC)
    return c


def pla_colour(key, month=None, beyond=False, layer=0, season=None):
    """round 3 name, kept for its callers: = pla_colours(key, season, beyond, layer, month)"""
    return pla_colours(key, season, beyond=beyond, layer=layer, month=month)


def _pla_status(bare_key=None):
    """keeps the one plants status line in PLA_LOG: "plants: no alpha; bare n species (keys)" """
    if bare_key:
        PLA_BARE_DRAWN.add(bare_key)
    ln = u"plants: no alpha; bare %d species%s" % (len(PLA_BARE_DRAWN), (u" (%s)" % u", ".join(sorted(PLA_BARE_DRAWN)))
                                                    if PLA_BARE_DRAWN else u"")
    for i, s_ in enumerate(PLA_LOG):
        if s_.startswith(u"plants: no alpha"):
            PLA_LOG[i] = ln
            return
    PLA_LOG.append(ln)


# bare branch architecture per form (drawing rules): clear stem (fraction of h), main limbs (count, spread deg),
# upward pull, child count, length ratio, pendulous whips
PLA_BARE_FORM = dict(
    dome=dict(lo=0.30, limbs=4, spread=110.0, up=0.15, kids=(2, 3), ratio=(0.62, 0.76)),
    oval=dict(lo=0.30, limbs=3, spread=55.0, up=0.45, kids=(2, 3), ratio=(0.64, 0.78)),
    feathery=dict(lo=0.0, limbs=4, spread=45.0, up=0.35, kids=(2, 2), ratio=(0.60, 0.72)),
    multistem=dict(lo=0.0, limbs=5, spread=70.0, up=0.40, kids=(2, 2), ratio=(0.55, 0.70)),
)


def _pla_bare_sec(form, x, gy, h, w, k, c, seed=0):
    """winter section of a deciduous tree: trunk and recursive branches as tapering lines inside the crown
    envelope, the open gaps between them showing (D7); the willow's winter state is _pla_willow2_sec(bare=True)"""
    import math as _m
    F = PLA_BARE_FORM.get(form, PLA_BARE_FORM["dome"])
    H, R = h * k, w / 2.0 * k
    rnd = _pla_rng(seed * 13 + 5)
    col = c["bark"]
    tw = max(0.12, h / 60.0 * k)
    lo = F["lo"] * H
    ex, ey = x, gy + lo + 0.5 * (H - lo) if lo else gy + 0.55 * H
    erx, ery = R, (0.5 * (H - lo) if lo else 0.45 * H)
    D = 3 if H < 8.0 else (4 if H < 20.0 else 5)
    sh = []

    def inside(px, py):
        return py <= gy + H and ((px - ex) / erx) ** 2 + ((py - ey) / ery) ** 2 <= 1.0 or py < ey and abs(px - ex) <= erx

    def grow(px, py, ang, L, wd, d):
        tx, ty = px + L * _m.cos(ang), py + L * _m.sin(ang)
        n_ = 0
        while not inside(tx, ty) and n_ < 6:
            L *= 0.8
            tx, ty = px + L * _m.cos(ang), py + L * _m.sin(ang)
            n_ += 1
        j = 0.08 * L * (rnd() - 0.5)
        mx, my = px + 0.5 * L * _m.cos(ang) - j * _m.sin(ang), py + 0.5 * L * _m.sin(ang) + j * _m.cos(ang)
        sh.append(("line", [(px, py), (mx, my), (tx, ty)], col, max(0.05, wd)))
        if d >= D:
            return
        nk = F["kids"][0] + (1 if rnd() < 0.4 and F["kids"][1] > F["kids"][0] else 0)
        for i in range(nk):
            off = (i - 0.5 * (nk - 1)) / max(1.0, 0.5 * (nk - 1) + 0.5) * _m.radians(28.0 + 14.0 * rnd())
            a = ang + off
            a = a + F["up"] * (_m.pi / 2.0 - a) * 0.5        # pull toward upright
            r_ = F["ratio"][0] + (F["ratio"][1] - F["ratio"][0]) * rnd()
            grow(tx, ty, a, L * r_, wd * 0.62, d + 1)

    if lo:                                           # trunk up to the first fork, tapering
        fy = gy + lo + 0.08 * (H - lo)
        sh.append(("poly", [(x - tw, gy), (x + tw, gy), (x + 0.6 * tw, fy), (x - 0.6 * tw, fy)], col, None, 0.0))
        base, L0 = (x, fy), 0.42 * (H - lo)
    else:                                            # stems from the ground
        base, L0 = (x, gy), 0.50 * H
    nl = F["limbs"]
    for i in range(nl):
        t = (i / float(nl - 1)) - 0.5 if nl > 1 else 0.0
        a = _m.pi / 2.0 + _m.radians(F["spread"]) * t + _m.radians(10.0) * (rnd() - 0.5)
        grow(base[0] + (0.15 * tw * t if lo else 0.12 * R * t), base[1], a, L0 * (0.85 + 0.25 * rnd()),
             (1.1 * tw if lo else 0.5 * tw), 1)
    return sh


def _pla_bare_plan(cx, cy, r, c, seed=0):
    """winter plan of a deciduous crown: main branches radiating and forking, open between them, the trunk dot"""
    import math as _m
    rnd = _pla_rng(seed * 17 + 3)
    col = c["bark"]
    sh = []

    def grow(px, py, ang, L, wd, d):
        tx, ty = px + L * _m.cos(ang), py + L * _m.sin(ang)
        if _m.hypot(tx - cx, ty - cy) > r:
            s_ = r / _m.hypot(tx - cx, ty - cy)
            tx, ty = cx + (tx - cx) * s_, cy + (ty - cy) * s_
        sh.append(("line", [(px, py), (tx, ty)], col, max(0.05, wd)))
        if d < 3:
            for o in (-0.45, 0.4):
                grow(tx, ty, ang + o + 0.2 * (rnd() - 0.5), L * 0.62, wd * 0.6, d + 1)
    n = 5 + int(rnd() * 2.999)
    for i in range(n):
        grow(cx, cy, 2 * _m.pi * (i + 0.3 * rnd()) / n, 0.45 * r, max(0.08, 0.05 * r), 1)
    sh.append(("poly", sec_ellipse(cx, cy, max(0.2, 0.06 * r), max(0.2, 0.06 * r), 10), col, None, 0.0))
    return sh


def _pla_bare_draw(key, sp, x, g, h, w, k, c, seed, plan=False):
    """the winter structure of a species (willow v2 skeleton or the form's branch architecture), counted bare"""
    _pla_status(key)
    if key == "willow":
        return _pla_willow2_plan(x, g, w / 2.0 * k, c, seed, bare=True) if plan else \
            _pla_willow2_sec(x, g, h, w, k, c, seed, bare=True)
    if plan:
        return _pla_bare_plan(x, g, w / 2.0 * k, c, seed)
    return _pla_bare_sec(sp["form"], x, g, h, w, k, c, seed)


def pla_bare(key, x, gy, k, h_m=None, crown_m=None, beyond=False, seed=0, layer=0, month=None, plan=False,
             season=None):
    """D7 winter tree: species `key` without leaves as its branch structure with the open gaps between branches, in
    its species-tinted bark colour, true size (section: ground at (x, gy); plan=True: crown centred on (x, gy) page
    mm), paler beyond / with depth. season / month default winter. Opaque lines and the trunk only. Returns shapes."""
    sp = _pla_get(key)
    h, w = _pla_size(key, sp, h_m, crown_m)
    if h_m is not None:
        h = pla_height_ok(key, h)
    s_ = _pla_s(season, month) or "winter"
    c = pla_colours(key, s_, beyond=beyond, layer=layer)
    _pla_count(key, s_)
    c0 = pla_colours(key, s_)
    if plan:
        img = _pla_img_draw(key, s_, "top", x, gy, h, w, k, c0, seed, beyond, 0, True) or \
            _pla_missing_draw(key, s_, "top", x, gy, w, w, k)
        return img if img is not None else _pla_bare_draw(key, sp, x, gy, h, w, k, c, seed, plan=True)
    sc = globals()["fig_depth"](layer)[0] if layer and globals().get("fig_depth") else 1.0
    g = gy(x) if callable(gy) else gy
    img = _pla_img_draw(key, s_, "side", x, g, h, w, k * sc, c0, seed, beyond, layer, True) or \
        _pla_missing_draw(key, s_, "side", x, g, h, w, k * sc)
    return img if img is not None else _pla_bare_draw(key, sp, x, g, h, w, k * sc, c, seed)


def _pla_rnd(i, s=0):
    """A fixed pseudo-random number in [0, 1)."""
    import math as _m
    v = _m.sin(i * 12.9898 + s * 78.233) * 43758.5453
    return v - _m.floor(v)


def _pla_crown(cx, cy, rx, up, dn, seed=0, wob=0.08, n=40):
    """A lobed crown outline: rx each side, up above and dn below cy; its widest points stay at cx +- rx."""
    import math as _m
    L = 2 * (3 + int(_pla_rnd(seed, 1) * 3))       # even lobe count: full width kept at a = 0 and pi
    out = []
    for i in range(n):
        a = 2 * _m.pi * i / n
        f = 1.0 - wob * _m.sin(L * a / 2.0) ** 2
        s = _m.sin(a)
        out.append((cx + rx * f * _m.cos(a), cy + (up if s > 0 else dn) * f * s))
    return out


# ---- round 4 (S3, D4, G-R4-6): print-quality crowns. Every crown = several overlapping, irregular leaf masses with
# open gaps between them; each mass in tones of its species (shade body with a fine edge, lit face toward the upper
# left, a small light fleck); trunk and main limbs drawn first so they show in the gaps. Plan and section are built
# from the same masses. Counts, sizes, offsets and the light direction are drawing rules, not data.
def _pla_mass(mx, my, rx, up, dn, c, seed, wob=0.2, edge=True):
    """one leaf mass centred (mx, my), rx each side, up above, dn below: shade body, lit face, light fleck"""
    sh = [("poly", _pla_crown(mx, my, rx, up, dn, seed, wob), c["shade"], c["edge"] if edge else None,
           0.06 if edge else 0.0)]
    sh.append(("poly", _pla_crown(mx - 0.12 * rx, my + 0.10 * up, 0.74 * rx, 0.78 * up, 0.55 * dn, seed + 1, wob),
               c["fill"], None, 0.0))
    sh.append(("poly", _pla_crown(mx - 0.30 * rx, my + 0.34 * up, 0.30 * rx, 0.30 * up, 0.24 * dn, seed + 2, wob),
               c["lt"], None, 0.0))
    return sh


def _pla_cloud(cx, cy, rx, ry, n, c, seed, wob=0.2, size=0.46, flat=1.0):
    """a crown of n leaf masses inside the ellipse (cx, cy, rx, ry) (page mm), the upper masses first so the lower
    ones overlap them; returns (shapes, masses [(x, y, rx, ry)])"""
    rnd = _pla_rng(seed * 19 + 7)
    pts = _pla_marks_in(cx, cy, (1.0 - 1.1 * size) * rx, (1.0 - 1.1 * size) * ry, n, rnd)
    ms = []
    for i, (px, py) in enumerate(pts):
        f = 0.82 + 0.36 * rnd()
        ms.append((px, py, size * rx * f, size * ry * f * flat, i))
    ms.sort(key=lambda m_: -m_[1])
    sh = []
    for px, py, mrx, mry, i in ms:
        sh += _pla_mass(px, py, mrx, mry, 0.85 * mry, c, seed * 7 + 3 * i, wob)
    return sh, [(m_[0], m_[1], m_[2], m_[3]) for m_ in ms]


# ---- white willow v2 (round 4, D1, S3): ONE drawing for every section, plan, axo, the p17 catalogue and winter, from
# the p17 catalogue photo (Commons "A big white willow tree (Salix alba) at the bay of lake Juojärvi in Tuusniemi,
# Finland, 2018 September": a massive leaning trunk forking low into heavy spreading limbs). One skeleton
# (_pla_willow2_skel): a stout leaning trunk, four arching limbs, two branches per limb, twigs. In leaf: a leaf mass at
# every branch end (_pla_mass), open gaps where the limbs show, the weeping fringe hanging from each mass. Winter: the
# same skeleton bare with fine hanging whips. Height: drawing size 15 m inside the sourced "up to 30.00 m" [35];
# crown 0.7 x h (rule: no sourced width, flagged). Proportions are drawing rules. Replaces the round 3 willow
# (its section, plan, mass table and the bare "weeping" whips), all deleted.
PLA_WILLOW_LIMBS = ((-0.72, 0.60), (-0.30, 0.84), (0.18, 0.90), (0.68, 0.64))   # limb tips (dx / R, y / H)


def _pla_willow2_skel(x, gy, H, R, seed):
    """the willow skeleton in section, page mm, mirrored on odd seeds: (trunk ring, branches [(pts, lw)],
    ends [(x, y, depth)], twigs [(pts, lw)])"""
    import math as _m
    rnd = _pla_rng(seed * 7 + 11)
    s = -1.0 if seed % 2 else 1.0
    tw = max(0.2, H / 36.0)                         # stout trunk: 1/18 of the height wide at the foot (rule)
    fx, fy = x + s * 0.12 * R, gy + 0.24 * H        # the low fork the trunk leans to
    trunk = [(x - 1.35 * tw, gy), (x + 1.35 * tw, gy), (x + tw + s * 0.04 * R, gy + 0.10 * H),
             (fx + 0.8 * tw, fy), (fx - 0.8 * tw, fy), (x - tw + s * 0.04 * R, gy + 0.10 * H)]

    def cx_(v):
        return max(x - 0.97 * R, min(x + 0.97 * R, v))
    br, ends, twigs = [], [], []
    for dx, ty in PLA_WILLOW_LIMBS:
        lx = cx_(x + s * dx * R * (0.94 + 0.12 * rnd()))
        ly = min(gy + ty * H * (0.95 + 0.08 * rnd()), gy + 0.93 * H)
        mx, my = 0.5 * (fx + lx), 0.5 * (fy + ly) + 0.06 * H     # limbs arch upward
        br.append(([(fx, fy), (mx, my)], 1.1 * tw))
        br.append(([(mx, my), (lx, ly)], 0.65 * tw))
        ends.append((lx, ly, 1))
        o = 1.0 if lx >= fx else -1.0
        px, py = mx + 0.6 * (lx - mx), my + 0.6 * (ly - my)
        for ax, ay in ((0.18, -0.08), (-0.12, 0.10)):           # one branch out and down, one up and in
            bx = cx_(lx + o * ax * R * (0.8 + 0.4 * rnd()))
            by = min(gy + 0.96 * H, ly + ay * H * (0.8 + 0.4 * rnd()))
            br.append(([(px, py), (0.5 * (px + bx), 0.5 * (py + by) + 0.02 * H), (bx, by)], 0.35 * tw))
            ends.append((bx, by, 2))
    for ex, ey, _d in ends:                         # twigs: two or three short ones from every end
        for j in range(2 + int(rnd() * 1.999)):
            a = 1.2 + 0.75 * j + 0.4 * rnd()
            L = (0.07 + 0.06 * rnd()) * R
            twigs.append(([(ex, ey), (cx_(ex + L * (1.0 if j % 2 else -1.0) * abs(_m.cos(a))),
                                     min(gy + H, ey + 0.6 * L))], 0.06))
    return trunk, br, ends, twigs


def _pla_willow2_sec(x, gy, h, w, k, c, seed=0, bare=False):
    """white willow v2 in section, h tall and w wide (m), ground at (x, gy) page mm; bare = the winter state"""
    H, R = h * k, w / 2.0 * k
    trunk, br, ends, twigs = _pla_willow2_skel(x, gy, H, R, seed)
    rnd = _pla_rng(seed * 5 + 3)
    col = c["bark"] if bare else c["stem"]
    sh = [("poly", trunk, col, None, 0.0)] + [("line", p, col, max(0.06, lw)) for p, lw in br]
    if bare:                                        # winter: twigs and fine hanging whips, open gaps between them
        sh += [("line", p, col, lw) for p, lw in twigs]
        for p, _lw in twigs:
            tx, ty = p[-1]
            yb = max(gy + 0.15 * H, ty - (0.15 + 0.15 * rnd()) * H)
            o = 1.0 if tx >= x else -1.0
            sh.append(("line", [(tx, ty), (tx + o * 0.02 * R, 0.5 * (ty + yb)), (tx + o * 0.03 * R, yb)], col, 0.05))
        return sh
    strand = _sec_mix(c["shade"], c["edge"], 0.35)
    ms = []
    for i, (ex, ey, d) in enumerate(ends):
        f = 0.85 + 0.30 * rnd()
        mrx = (0.24 if d == 1 else 0.18) * R * f
        up = (0.11 if d == 1 else 0.09) * H * f
        ey = min(ey, gy + H - up)
        ms.append((ex, ey, mrx, up, i))
    ms.sort(key=lambda m_: -m_[1])                  # upper masses first: the lower ones overlap them
    for mx, my, mrx, up, i in ms:
        sh += _pla_mass(mx, my, mrx, up, 0.8 * up, c, seed * 13 + 3 * i, 0.22)
        n_ = max(4, int(mrx / max(0.3, 0.04 * R)))   # the weeping fringe hanging from the mass
        for j in range(n_):
            t = -0.85 + 1.7 * (j + 0.5 * rnd()) / n_
            px = mx + t * mrx
            top = my - 0.55 * up * (1.0 - t * t) ** 0.5
            yb = max(gy + 0.18 * H, top - (0.10 + 0.15 * rnd()) * H)
            lean = (0.02 + 0.02 * rnd()) * R * (1.0 if px >= x else -1.0)
            if j % 2 == 0:
                wd = 0.05 * mrx + 0.05
                sh.append(("poly", [(px - wd, top), (px + wd, top), (px + lean + 0.15 * wd, yb),
                                    (px + lean - 0.15 * wd, yb)], c["shade"] if j % 4 == 0 else c["fill"], None, 0.0))
            else:
                sh.append(("line", [(px, top), (px + 0.5 * lean, 0.5 * (top + yb)), (px + lean, yb)], strand, 0.06))
    return sh


def _pla_willow2_plan(cx, cy, r, c, seed=0, bare=False):
    """white willow v2 from above, crown radius r (page mm) on (cx, cy): the same four limbs and their branches
    radiating, a leaf mass at every end (outer first, the crown top last), strand ticks round the rim; bare = winter"""
    import math as _m
    rnd = _pla_rng(seed * 5 + 9)
    a0 = 2 * _m.pi * rnd()
    col = c["bark"] if bare else c["stem"]
    lw0 = max(0.10, 0.05 * r)
    sh, ends = [], []
    for i in range(4):
        a = a0 + 2 * _m.pi * (i / 4.0 + 0.10 * (rnd() - 0.5))
        lx, ly = cx + 0.62 * r * _m.cos(a), cy + 0.62 * r * _m.sin(a)
        sh.append(("line", [(cx, cy), (lx, ly)], col, lw0))
        ends.append((lx, ly, 1, a))
        for o in (-0.38, 0.38):
            b = a + o + 0.1 * (rnd() - 0.5)
            bx, by = lx + 0.24 * r * _m.cos(b), ly + 0.24 * r * _m.sin(b)
            sh.append(("line", [(lx, ly), (bx, by)], col, 0.6 * lw0))
            ends.append((bx, by, 2, b))
    if bare:
        for ex, ey, _d, a in ends:
            for o in (-0.3, 0.3):
                sh.append(("line", [(ex, ey), (ex + 0.08 * r * _m.cos(a + o), ey + 0.08 * r * _m.sin(a + o))], col,
                           0.06))
        sh.append(("poly", sec_ellipse(cx, cy, max(0.2, 0.06 * r), max(0.2, 0.06 * r), 10), col, None, 0.0))
        return sh
    for ex, ey, d, a in sorted(ends, key=lambda e_: -e_[2]):     # outer branch ends first
        mr = (0.26 if d == 1 else 0.20) * r * (0.85 + 0.3 * rnd())
        sh += _pla_mass(ex, ey, mr, mr, mr, c, seed * 11 + int(100 * a), 0.22)
        if d == 2:                                  # the fringe seen from above: short ticks past the mass
            for j in range(4):
                b = a + 0.35 * (j - 1.5)
                p0 = (ex + 0.75 * mr * _m.cos(b), ey + 0.75 * mr * _m.sin(b))
                sh.append(("line", [p0, (p0[0] + 0.12 * r * _m.cos(b), p0[1] + 0.12 * r * _m.sin(b))], c["shade"],
                           0.07))
    sh += _pla_mass(cx, cy, 0.30 * r, 0.30 * r, 0.30 * r, c, seed + 7, 0.2)
    return sh


# tree crowns per form (drawing rules): clear stem / h, masses in section, masses in plan, mass size, flatness, limbs
PLA_CROWN = dict(dome=(0.30, 9, 7, 0.44, 1.0, 4), oval=(0.28, 8, 6, 0.46, 1.0, 3),
                 gnarled=(0.30, 7, 6, 0.46, 0.85, 3), umbrella=(0.65, 8, 7, 0.36, 0.80, 4),
                 feathery=(0.0, 9, 8, 0.38, 1.0, 4))


def _pla_tree_sec(form, x, gy, h, w, k, c, seed=0):
    """a tree in section (round 4, D4): trunk and main limbs, then the crown of overlapping two-tone leaf masses
    with open gaps (_pla_cloud); h tall, w crown wide (m), ground at (x, gy) page mm"""
    lo_f, n, _np, size, flat, nl = PLA_CROWN[form]
    H, R = h * k, w / 2.0 * k
    st = c["stem"]
    tw = max(0.15, h / 60.0 * k)                    # half trunk width: trunk 1/30 of the height (rule)
    sh = []
    if form == "feathery":                          # tamarisk: slender stems from the ground into an airy crown
        cy, ry = gy + 0.62 * H, 0.38 * H
        for i in range(4):
            t = (i - 1.5) / 1.5
            sh.append(("line", [(x + t * 0.05 * R, gy), (x + t * 0.25 * R, gy + 0.35 * H),
                                (x + t * 0.55 * R, cy)], st, max(0.08, 0.6 * tw)))
    else:
        yb = gy + lo_f * H
        y0 = yb - 0.05 * (gy + H - yb)              # the crown starts a little below the first fork
        cy, ry = 0.5 * (y0 + gy + H), 0.5 * (gy + H - y0)
        if form == "gnarled":                       # olive: two twisting stems
            for s_ in (-1, 1):
                sh.append(("poly", [(x + s_ * 0.2 * tw, gy), (x + s_ * 1.6 * tw, gy),
                                    (x + s_ * (0.35 * R + 0.5 * tw), cy), (x + s_ * (0.35 * R - 0.5 * tw), cy)],
                           st, None, 0.0))
        else:
            lean = 0.03 * H if form == "umbrella" else 0.0
            sh.append(("poly", [(x - tw, gy), (x + tw, gy), (x + lean + 0.6 * tw, yb), (x + lean - 0.6 * tw, yb)],
                       st, None, 0.0))
        for i in range(nl):                         # main limbs into the crown, a side branch on each
            t = (2.0 * i / (nl - 1) - 1.0) if nl > 1 else 0.0
            ex, ey = x + 0.72 * R * t, cy + 0.45 * ry * (1.0 - abs(t))
            sh.append(("line", [(x, yb), (0.5 * (x + ex), 0.5 * (yb + ey) + 0.1 * ry), (ex, ey)], st,
                       max(0.08, 0.7 * tw)))
            o = 1.0 if t >= 0 else -1.0
            sh.append(("line", [(0.5 * (x + ex), 0.5 * (yb + ey) + 0.1 * ry),
                                (0.5 * (x + ex) + o * 0.2 * R, min(gy + H, ey + 0.4 * ry))], st, max(0.06, 0.4 * tw)))
    cl, ms = _pla_cloud(x, cy, R, ry, n, c, seed, size=size, flat=flat)
    sh += cl
    if form == "feathery":                          # hanging wisps under the masses
        for mx, my, mrx, mry in ms:
            for d in (-0.5, 0.0, 0.5):
                px, py = mx + d * mrx, my - 0.7 * mry
                sh.append(("line", [(px, py), (px + 0.04 * (px - x), py - 0.09 * H)], c["edge"], 0.06))
    return sh


def _pla_sec(form, x, gy, h, w, k, c, seed=0):
    """Section of one form, h tall and w crown wide (m), ground at (x, gy) page mm (round 4: print quality, D4)."""
    H, R = h * k, w / 2.0 * k
    f, e, ac = c["fill"], c["edge"], c.get("accent")
    sh = []
    if form == "weeping":                           # white willow v2 (D1)
        return _pla_willow2_sec(x, gy, h, w, k, c, seed)
    if form in PLA_CROWN:
        return _pla_tree_sec(form, x, gy, h, w, k, c, seed)
    rnd = _pla_rng(seed * 29 + 5)
    if form == "multistem":                         # chaste tree: stems fanning from the ground, a mass on each
        heads = ((-0.68, 0.58), (-0.36, 0.70), (0.0, 0.76), (0.34, 0.69), (0.68, 0.57))
        for dx, cy_ in heads:
            sh.append(("line", [(x + dx * 0.1 * R, gy), (x + dx * 0.55 * R, gy + 0.4 * cy_ * H),
                                (x + dx * R, gy + cy_ * H)], c["stem"], 0.15))
        for i, (dx, cy_) in sorted(enumerate(heads), key=lambda t_: -t_[1][1]):
            up = 0.22 * H * (0.9 + 0.2 * rnd())
            sh += _pla_mass(x + dx * R, gy + cy_ * H, 0.32 * R, up, 0.85 * up, c, seed * 5 + i, 0.16)
        if ac:                                      # flower spikes upright from the top of each mass
            for dx, cy_ in heads:
                top = gy + (cy_ + 0.20) * H
                for d in (-0.12, 0.0, 0.12):
                    px = x + (dx + d) * R
                    sh.append(("line", [(px, top - 0.14 * H), (px + 0.02 * R, top + 0.04 * H)], ac, 0.3))
        return sh
    if form == "mound":                             # lavender, rosemary, water mint: overlapping low masses
        for i, d in enumerate((-0.45, 0.42, 0.0)):
            up = (0.62 if d == 0.0 else 0.52) * H * (0.9 + 0.2 * rnd())
            sh += _pla_mass(x + d * R, gy + 0.36 * H, (0.52 if d == 0.0 else 0.50) * R, up, 0.36 * H, c,
                            seed * 3 + i, 0.12)
        if ac:                                      # flower spikes above the mound, a bract head on each
            for d in (-0.55, -0.25, 0.05, 0.32, 0.58):
                px, top = x + d * R, gy + (0.95 + 0.12 * rnd()) * H
                sh.append(("line", [(px, gy + 0.70 * H), (px + 0.05 * d * R, top)], c["stem"], 0.08))
                sh.append(("poly", sec_ellipse(px + 0.05 * d * R, top, 0.05 * R + 0.08, 0.08 * H + 0.1, 8), ac,
                           None, 0.0))
        else:                                       # needle-leaf strokes in the edge tone
            for d in (-0.55, -0.25, 0.05, 0.35, 0.6):
                sh.append(("line", [(x + d * R, gy + 0.45 * H), (x + d * R * 1.05, gy + 0.78 * H)], e, 0.07))
        return sh
    if form in ("clump", "tussock", "cane"):        # rushes and loosestrife: stems from one base; giant reed: canes
        n = dict(clump=15, tussock=23, cane=7)[form]
        for i in range(n):
            t = i / float(n - 1)
            hh = H * (0.80 + 0.20 * _pla_rnd(i, seed + 3))
            bx, tx = x + (2 * t - 1) * R * 0.15, x + (2 * t - 1) * R
            col = f if i % 3 else c["shade"]        # two tones through the clump
            if form == "clump":                     # soft arch
                mx = bx + (tx - bx) * 0.35
                sh.append(("line", [(bx, gy), (mx, gy + 0.55 * hh), (tx, gy + hh)], col, 0.12))
                if ac and i % 2 == 0:               # loosestrife flower spike on the upper stem
                    sh.append(("line", [(mx + (tx - mx) * 0.3, gy + 0.69 * hh), (tx, gy + hh)], ac, 0.35))
            else:
                sh.append(("line", [(bx, gy), (tx, gy + hh)], col, 0.15 if form == "cane" else 0.1))
                if form == "cane":                  # leaf blades along the cane
                    for j in range(1, 5):
                        py = gy + hh * j / 5.0
                        px = bx + (tx - bx) * j / 5.0
                        s_ = 1 if (i + j) % 2 else -1
                        sh.append(("line", [(px, py), (px + s_ * 0.35 * R, py - 0.06 * hh)], f, 0.1))
        if form == "cane" and ac:                   # marked for removal
            sh.append(("line", [(x - R, gy), (x + R, gy + H)], ac, 0.35))
            sh.append(("line", [(x - R, gy + H), (x + R, gy)], ac, 0.35))
        return sh
    raise ValueError("_pla_sec: unknown form %r" % form)


def _pla_plan(form, cx, cy, w, k, c, seed=0):
    """Top view of one form, crown w wide (m), centre (cx, cy) page mm: the same masses as the section (round 4)."""
    import math as _m
    r = w / 2.0 * k
    f, e, ac = c["fill"], c["edge"], c.get("accent")
    sh = []
    if form == "weeping":                           # white willow v2 (D1)
        return _pla_willow2_plan(cx, cy, r, c, seed)
    if form in PLA_CROWN:
        _lo, _n, n, size, _fl, nl = PLA_CROWN[form]
        for i in range(nl + 1):                     # limbs, seen in the gaps between the masses
            a = 2 * _m.pi * (i / float(nl + 1) + 0.2 * _pla_rnd(seed, 5))
            sh.append(("line", [(cx, cy), (cx + 0.7 * r * _m.cos(a), cy + 0.7 * r * _m.sin(a))], c["stem"],
                       max(0.08, 0.04 * r)))
        cl, _ms = _pla_cloud(cx, cy, r, r, n, c, seed, size=size + 0.04)
        sh += cl
        if form == "umbrella":                      # needle tufts round the flat crown
            for i in range(30):
                a = 2 * _m.pi * i / 30.0
                sh.append(("line", [(cx + 0.80 * r * _m.cos(a), cy + 0.80 * r * _m.sin(a)),
                                    (cx + 0.98 * r * _m.cos(a), cy + 0.98 * r * _m.sin(a))], c["lt"], 0.08))
        elif form == "feathery":                    # feathery sprays at the rim
            for i in range(24):
                a = 2 * _m.pi * i / 24.0
                sh.append(("line", [(cx + 0.82 * r * _m.cos(a), cy + 0.82 * r * _m.sin(a)),
                                    (cx + 0.82 * r * _m.cos(a + 0.12), cy + 0.82 * r * _m.sin(a + 0.12))], e, 0.07))
        return sh
    if form == "multistem":                         # five heads, as in section
        for i in range(5):
            a = 2 * _m.pi * (i / 5.0 + 0.05)
            hx, hy = cx + 0.55 * r * _m.cos(a), cy + 0.55 * r * _m.sin(a)
            sh += _pla_mass(hx, hy, 0.45 * r, 0.45 * r, 0.45 * r, c, seed + i, 0.12)
            if ac:
                for d in ((-0.15, 0.1), (0.12, 0.18), (0.0, -0.12)):
                    sh.append(("poly", sec_ellipse(hx + d[0] * r, hy + d[1] * r, 0.07 * r + 0.05, 0.07 * r + 0.05, 8),
                               ac, None, 0.0))
        return sh
    if form == "mound":
        for i, (dx, dy, s_) in enumerate(((-0.35, -0.2, 0.62), (0.32, -0.15, 0.6), (0.0, 0.25, 0.62))):
            sh += _pla_mass(cx + dx * r, cy + dy * r, s_ * r, s_ * r, s_ * r, c, seed + i, 0.1)
        for i in range(6):
            a = 2 * _m.pi * (i / 6.0 + _pla_rnd(seed, 6))
            px, py = cx + 0.5 * r * _m.cos(a), cy + 0.5 * r * _m.sin(a)
            if ac:
                sh.append(("poly", sec_ellipse(px, py, 0.12 * r, 0.12 * r, 8), ac, None, 0.0))
            else:
                sh.append(("line", [(px, py), (px + 0.2 * r * _m.cos(a), py + 0.2 * r * _m.sin(a))], e, 0.07))
        return sh
    if form in ("clump", "tussock", "cane"):        # stems seen from above: a starburst in two tones
        n = dict(clump=15, tussock=23, cane=9)[form]
        for i in range(n):
            a = 2 * _m.pi * (i / float(n) + 0.3 * _pla_rnd(i, seed))
            ll = r * (0.8 + 0.2 * _pla_rnd(i, seed + 2))
            sh.append(("line", [(cx, cy), (cx + ll * _m.cos(a), cy + ll * _m.sin(a))], f if i % 3 else c["shade"],
                       0.12))
            if ac and form == "clump" and i % 2 == 0:
                sh.append(("poly", sec_ellipse(cx + ll * _m.cos(a), cy + ll * _m.sin(a), 0.08 * r + 0.1,
                                               0.08 * r + 0.1, 8), ac, None, 0.0))
        if form == "cane" and ac:
            d = r * 0.7
            sh += [("line", [(cx - d, cy - d), (cx + d, cy + d)], ac, 0.35),
                   ("line", [(cx - d, cy + d), (cx + d, cy - d)], ac, 0.35)]
        return sh
    raise ValueError("_pla_plan: unknown form %r" % form)


def _pla_get(key):
    if key not in PLA_SPECIES:
        raise ValueError("plants: unknown species %r (removed by D6, or not in species.json)" % key)
    if key in ("reed", "mint"):
        raise ValueError("plants: %s grows only in lined cells: use pla_reed_basin / pla_mint_cell" % key)
    return PLA_SPECIES[key]


def _pla_size(key, sp, h_m, crown_m):
    h, w = h_m or sp["h_m"], crown_m or sp["crown_m"]
    if h is None or w is None:
        raise ValueError("plants: %s has no sourced size: pass h_m and crown_m" % key)
    return h, w


PLA_LOG = []
# round 4 (S3) counters for the log lines (pla_log_lines): plants drawn per species / crop, species per season
PLA_COUNT = {}
PLA_SEASON_KEYS = {}


def _pla_count(key, season):
    PLA_COUNT[key] = PLA_COUNT.get(key, 0) + 1
    PLA_SEASON_KEYS.setdefault(season or "general", set()).add(key)


def pla_log_lines():
    """the plant log lines of this run (sec_look_lines prints them): willow v2 drawn n; plants drawn by species;
    plants season=<season> species n (one per season drawn; 'general' = no season); FLAG plant colours pending
    research (n species: every species and crop, until research/plant_colours.md fills the colours)"""
    wf = sorted(set(v for (k_, _s, _v), v in PLA_IMG_FILE.items() if k_ == "willow"))
    out = [u"willow v3 image=%s (drawn %d)" % (u", ".join(wf) if wf else
                                               u"none (pending Data/plants/willow_<state>_side.png)",
                                               PLA_COUNT.get("willow", 0)),
           u"plants drawn by species: " + (u", ".join(u"%s %d" % kv for kv in sorted(PLA_COUNT.items())) or u"none")]
    by = {}
    for sk, src in PLA_SRC.items():                       # round 5: species x state (x view) per image source
        by.setdefault(src or "vector_fallback", set()).add(sk)
    out.append(u"plants source=" + u", ".join(u"%s %d" % (k_, len(v)) for k_, v in sorted(by.items())) +
               u" species×state" if by else u"plants source=none drawn")
    miss = sorted(by.get("vector_fallback", set()) | by.get("placeholder", set()))
    if miss:
        out.append(u"FLAG plants without image %d species×state (view): %s" % (
            len(miss), u", ".join(u"%s %s (%s)" % m for m in miss[:40]) + (u" ..." if len(miss) > 40 else u"")))
    if PLA_TONE_LOG:
        out.append(u"plants toned: " + u", ".join(u"%s %d" % kv for kv in sorted(PLA_TONE_LOG.items())))
    for s_ in ("general",) + PLA_SEASONS:
        if s_ in PLA_SEASON_KEYS:
            out.append(u"plants season=%s species %d" % (s_, len(PLA_SEASON_KEYS[s_])))
    n = len(PLA_SPECIES) + len([c_ for c_ in PLA_CROPS if c_ != "olive"])
    out.append(u"FLAG plant colours pending research (%d species): %s" % (n, PLA_COLOUR_SRC))
    return out


def pla_height_ok(key, h_m):
    """h_m (m) moved into the species' sourced range (G6; T1: the olive was drawn 5.0 m against 8-15 m); a change is
    logged once per species and value"""
    lo, hi = PLA_SPECIES[key]["h_range"]
    v = h_m
    if lo is not None and v < lo:
        v = lo
    if hi is not None and v > hi:
        v = hi
    if v != h_m:
        msg = u"Plants: %s asked at %.2f m, drawn %.2f m (sourced %s-%s m)" % (key, h_m, v, lo or "", hi or "")
        if msg not in PLA_LOG:
            PLA_LOG.append(msg)
    return v


def _pla_layer_cols(c, layer):
    f = globals().get("fig_fade")
    if not layer or f is None:
        return c
    return dict((k_, f(v, layer) if v else v) for k_, v in c.items())


# ---- round 5 (S4, G-R5-6, D4, D10, N2 a; PLAN §3 Plants): plant module v3, every plant from a real image ---------------
# One image per species x state (states: general, spring, summer, autumn, winter), cut out and toned to the
# species' colours (pla_colours: the colours stay "pending research/plant_colours.md" until that file arrives; one
# data edit then re-tones every image, because the toned copies are cached under a key that holds the colours).
# Where an image comes from, first found wins (side views; plan views use 1 only):
#   1. asset_png  Downloads/Bergama/Data/plants/<key>_<state>_<view>.png (view side | top; the asset-library project
#                 delivers them: handover/ASSET_PROMPT_plants.md; transparent, plant standing on the bottom edge).
#                 A seasonal state with no own file but a <key>_general_ file uses that one tinted for the season
#                 (never for a bare winter state).
#   2. cutout     Data/cutouts/<species key> (watercolour sheet, species assigned by look, in leaf only: CHK-4 §4.2)
#   3. hires      Data/assets_hires.json PhyloPic silhouettes (plane, plane_bare, ash, olive, stone_pine, maize,
#                 tomato; plane and ash are stand-in species: CHK-4 §4.1), flat in the species colour
#   4. none       pla_missing("vector") = the round 4 drawing (default, so no page goes blank; counted and FLAGged),
#                 pla_missing("placeholder") = a labelled dashed box (the D4 sample sheet shows what is missing)
# Images keep their own proportions (never stretched): height = the species' drawing height, width from the image.
# pla_images(False) turns raster images off for pages that cannot place images (CHK-3 §3.5: site board p02/p03,
# masterplan p17/p24): hires silhouettes and the fallback are used there.
# Logs (pla_log_lines): "plants source=<image> species×state n" per source, "willow v3 image=<file>|none",
# "FLAG plants without image ..." while any species x state has none.
PLA_IMG = dict(on=True, missing="vector")
PLA_IMG_TONE_KEEP = 0.25          # share of the photo's own colour kept when toning (0.45 in bloom): drawing rule
PLA_IMG_HIRES = dict(plane=("plane", "plane_bare"), ash=("ash", None), olive=("olive", "olive"),
                     stone_pine=("stone_pine", "stone_pine"), maize=("maize", None), tomato=("tomato", None))
PLA_SRC = {}                      # (key, state, view) -> source of the last drawing ("asset_png", "cutout", ...)
PLA_IMG_FILE = {}                 # (key, state, view) -> file used
PLA_TONE_LOG = {}                 # "numpy" / "lut" / failure -> count


def pla_img_dir():
    import os as _o
    return _o.path.join(_o.path.expanduser("~"), "Downloads", "Bergama", "Data", "plants")


def pla_images(on=True):
    """raster plant images on (True) or off (False: hires silhouettes and the fallback only); returns the old value"""
    old = PLA_IMG["on"]
    PLA_IMG["on"] = bool(on)
    return old


def pla_missing(mode="vector"):
    """what is drawn where no image exists: "vector" (round 4 drawing, FLAGged) or "placeholder" (labelled box)"""
    old = PLA_IMG["missing"]
    PLA_IMG["missing"] = "placeholder" if mode == "placeholder" else "vector"
    return old


def _pla_img_find(key, state, view, bare):
    """(source, ref) of the image for key x state x view: ("asset_png", path) / ("cutout", entries) / ("hires", key)
    / (None, None). state None = general."""
    import os as _o
    st = state or "general"
    if PLA_IMG["on"]:
        d = pla_img_dir()
        for s_ in [st] + ([] if (bare or st == "general") else ["general"]):
            f = _o.path.join(d, "%s_%s_%s.png" % (key, s_, view))
            if _o.path.isfile(f):
                return "asset_png", f
        if view == "side" and not bare:
            lib = sil_cut_library().get(key)
            if lib:
                return "cutout", lib
    if view == "side":
        hk = PLA_IMG_HIRES.get(key, (None, None))[1 if bare else 0]
        hl = globals().get("hr_library")
        if hk and hl and hk in hl():
            return "hires", hk
    return None, None


def _pla_toned(path, c, fade, keep):
    """the toned copy of an image (cached under Downloads/Bergama/cached/plants_toned/), or the image itself"""
    import os as _o
    import hashlib as _h
    try:
        stt = _o.stat(path)
        sig = "%s|%d|%d|%s|%s|%s|%.3f|%.2f|v3" % (path, stt.st_size, int(stt.st_mtime), c["shade"], c["fill"], c["lt"],
                                                 fade, keep)
        root = bg_cache("plants_toned") if "bg_cache" in globals() else _o.path.join(
            _o.path.expanduser("~"), "Downloads", "Bergama", "cached", "plants_toned")
        dst = _o.path.join(root, _h.md5(sig.encode("utf-8")).hexdigest()[:16] + ".png")
        if _o.path.isfile(dst):
            return dst
        ok, how = sil_tone(path, dst, c["shade"], c["fill"], c["lt"], keep, SEC["paper"], fade)
        PLA_TONE_LOG[how] = PLA_TONE_LOG.get(how, 0) + 1
        return dst if ok else path
    except Exception as ex:
        PLA_TONE_LOG["failed " + type(ex).__name__] = PLA_TONE_LOG.get("failed " + type(ex).__name__, 0) + 1
        return path


def _pla_fade(beyond, layer):
    f = fig_depth(layer)[1] if layer and globals().get("fig_depth") else 0.0
    return 1.0 - (1.0 - (0.55 if beyond else 0.0)) * (1.0 - f)


def _pla_img_draw(key, state, view, x, g, h, w, k, c0, seed, beyond, layer, bare):
    """the image drawing of one plant (section: ground at (x, g); plan: crown centred on (x, g)), or None.
    c0 = the species' colours at layer 0, not beyond (pla_colours); h, w in m; k page mm per m (layer-scaled)."""
    src, ref = _pla_img_find(key, state, view, bare)
    sk = (key, state or "general", view)
    if src is None:
        PLA_SRC[sk] = PLA_SRC.get(sk) or None
        return None
    fade = _pla_fade(beyond, layer)
    flip = bool(seed % 2)                                 # variety: mirrored every other plant
    if src == "hires":
        fill = c0["bark"] if bare else c0["fill"]
        if fade > 0:
            fill = _sec_mix(fill, SEC["paper"], fade)
        sh = hr_side(ref, x, g, k, h, w_m=None, fill=fill, edge=None, lw=0.0, facing=-1 if flip else 1)
        if sh:
            PLA_SRC[sk], PLA_IMG_FILE[sk] = src, "assets_hires.json:" + ref
        return sh
    if src == "cutout":
        import os as _o
        e = ref[int(seed) % len(ref)]
        path = _o.path.join(sil_cut_dir(), e["file"])
    else:
        path = ref
    px = sil_png_size(path)
    if not px or not px[1]:
        return None
    keep = 0.45 if c0.get("bloom") else PLA_IMG_TONE_KEEP
    tp = _pla_toned(path, c0, fade, keep)
    PLA_SRC[sk], PLA_IMG_FILE[sk] = src, _o_base(path)
    if view == "top":
        W = w * k
        H = W * px[1] / float(px[0])
        return [("image", x - W / 2.0, g - H / 2.0, W, H, tp, None, flip, None)]
    H = h * k
    W = H * px[0] / float(px[1])
    return [("image", x - W / 2.0, g, W, H, tp, None, flip, None)]


def _o_base(p):
    import os as _o
    return _o.path.basename(p)


def _pla_placeholder(key, state, view, x, g, h, w, k):
    """a labelled dashed box where no image exists (pla_missing("placeholder"); the D4 sample sheet)"""
    W = max(w * k, 4.0)
    H = (h * k) if view == "side" else W
    y0 = g if view == "side" else g - H / 2.0
    ring = [(x - W / 2.0, y0), (x + W / 2.0, y0), (x + W / 2.0, y0 + H), (x - W / 2.0, y0 + H), (x - W / 2.0, y0)]
    sz = 1.6
    return [("line", ring, "8E8F8A", 0.2, [1.0, 0.8]),
            ("text", u"no image", x, y0 + H / 2.0 + 0.2, sz, "8B2D2D", True, "C"),
            ("text", u"%s %s" % (key, state or "general"), x, y0 + H / 2.0 - 1.8, sz, "8B2D2D", False, "C")]


def _pla_missing_draw(key, state, view, x, g, h, w, k):
    """None (draw the round 4 vector) or the placeholder; counts the species x state as without image"""
    sk = (key, state or "general", view)
    if PLA_IMG["missing"] == "placeholder":
        PLA_SRC[sk] = "placeholder"
        return _pla_placeholder(key, state, view, x, g, h, w, k)
    PLA_SRC[sk] = "vector_fallback"
    return None



# round 5 (S4, BRIEF G-R5-6 row A1): every greenery colour of the other scripts' local palettes comes from here (S6-S9
# replace their own SEC/BM_COL/ICO_PAL/COL/... greenery values by pla_green(role)); pending research like all.
def pla_green(role):
    """a greenery colour by role: tree, tree_wet, tree_dry, shrub, flower, grass, meadow, crop, field, row,
    wetland, reed, trunk (hex, from the species colours of this module)"""
    f = lambda k_: PLA_SPECIES[k_]["colours"]["fill"]
    t = dict(tree=f("plane"), tree_wet=f("willow"), tree_dry=f("olive"), shrub=f("chaste"), flower=PLA_LAV,
             grass=PLA_CROP_LEAF, meadow=_sec_mix(PLA_CROP_LEAF, SEC["paper"], 0.45), crop=PLA_CROP_LEAF,
             field=PLA_FIELD, row=PLA_ROW, wetland=PLA_WET, reed=PLA_REED_HEAD, trunk=PLA_TRUNK)
    if role not in t:
        raise KeyError("pla_green: role %r; known: %s" % (role, ", ".join(sorted(t))))
    return t[role]


def pla_section(key, x, gy, k, h_m=None, crown_m=None, beyond=False, seed=0, hires=True, style="b", layer=0,
                detail=True, month=None, season=None):
    """A species in section at true size: ground at (x, gy) page mm (gy may be a function of x). h_m outside the
    sourced range is moved into it (pla_height_ok). layer: D9 depth layer (0 true size; 1, 2 smaller and paler).
    Round 4 (S3, D4, G-R4-6): ONE vector drawing per species everywhere (print quality: two-tone leaf masses with
    gaps, trunk and limbs); `hires` and `style` are accepted and no longer change the drawing (no cutouts, no
    high-res silhouettes). season (None = general; month= alias) = the season's state and colours (pla_colours), a
    deciduous species out of leaf drawn bare. detail: leaf texture and flower marks (_pla_detail). Never alpha."""
    sp = _pla_get(key)
    h, w = _pla_size(key, sp, h_m, crown_m)
    if h_m is not None:
        h = pla_height_ok(key, h)
    g = gy(x) if callable(gy) else gy
    s_ = _pla_s(season, month)
    _pla_status()
    _pla_count(key, s_)
    c = pla_colours(key, s_, beyond=beyond, layer=layer)
    sc = globals()["fig_depth"](layer)[0] if layer and globals().get("fig_depth") else 1.0
    k = k * sc
    img = _pla_img_draw(key, s_, "side", x, g, h, w, k, pla_colours(key, s_), seed, beyond, layer, c["bare"])
    if img is None:                                     # round 5: no image -> placeholder or the round 4 drawing
        img = _pla_missing_draw(key, s_, "side", x, g, h, w, k)
    if img is not None:
        return img
    if c["bare"]:
        return _pla_bare_draw(key, sp, x, g, h, w, k, c, seed)
    sh = _pla_sec(sp["form"], x, g, h, w, k, c, seed)
    if detail:
        sh += _pla_detail(key, sp["form"], x, g, h, w, k, c, seed)
    return sh


def pla_plan(key, cx, cy, k, crown_m=None, beyond=False, seed=0, distinct=True, style="b", month=None, season=None):
    """The same species from above: crown crown_m wide (m) centred on (cx, cy) page mm, built from the same masses
    and colours as its section; distinct: the species' own mark on top (no two species share a plan symbol, M6).
    season (month= alias) = the season's colours, deciduous out of leaf = bare branches. Always opaque."""
    sp = _pla_get(key)
    w = crown_m or sp["crown_m"]
    if w is None:
        raise ValueError("plants: %s has no sourced crown: pass crown_m" % key)
    s_ = _pla_s(season, month)
    _pla_status()
    _pla_count(key, s_)
    c = pla_colours(key, s_, beyond=beyond)
    img = _pla_img_draw(key, s_, "top", cx, cy, sp["h_m"] or w, w, k, pla_colours(key, s_), seed, beyond, 0, c["bare"])
    if img is None:                                     # round 5: no top-view image -> placeholder or round 4 drawing
        img = _pla_missing_draw(key, s_, "top", cx, cy, w, w, k)
    if img is not None:
        return img
    if c["bare"]:
        return _pla_bare_draw(key, sp, cx, cy, sp["h_m"] or w, w, k, c, seed, plan=True)
    sh = _pla_plan(sp["form"], cx, cy, w, k, c, seed)
    return sh + (_pla_plan_mark(key, cx, cy, w / 2.0 * k, c, seed) if distinct else [])


def pla_axo(key, x, y, k, h_m=None, crown_m=None, beyond=False, seed=0, layer=0, season=None, month=None,
            detail=False):
    """A species standing in an axo (p12, D1 'one drawing everywhere'): the section drawing of the module set upright
    at the projected base point (x, y) page mm, k = page mm per m of height at that point (a billboard, as an axo
    tree is drawn). Same willow v2 / species drawing as every section. Returns shapes (y up)."""
    return pla_section(key, x, y, k, h_m=h_m, crown_m=crown_m, beyond=beyond, seed=seed, layer=layer,
                       detail=detail, season=season, month=month)


# round 4 (S3, D4, D6): crop states by season from the sourced crop calendars (TAGEM region 28, PLA_CROP_SRC):
# cotton sown mid-Apr, to 21 Oct; maize sown Apr III / 1 May, to 2 Sep (TAGEM to Eki I); tomato (processing) planted
# Apr II / 15 May, to 27 Aug; olive orchard evergreen, harvest 6-14 Nov. Reading taken (drawing states, not data):
# spring = young plants; summer = grown (tomato with fruit, harvest to Aug); autumn = cotton ripe with open bolls
# (harvest to 21 Oct), maize and tomato harvested (stubble); winter = bare field; general = the crop in its character.
PLA_CROP_SRC = ("library/research/crops_2026-10-24/bergama_crops_irrigation_v1.md:388-400, 426-441 (TAGEM region 28);"
                " olive harvest :258 (Kaya 2017)")
PLA_CROP_STATE = dict(
    cotton=dict(general="ripe", winter="bare", spring="seedling", summer="growing", autumn="ripe"),
    maize=dict(general="growing", winter="bare", spring="seedling", summer="growing", autumn="harvested"),
    tomato=dict(general="fruit", winter="bare", spring="seedling", summer="fruit", autumn="harvested"),
    olive=dict(general="tree", winter="tree", spring="tree", summer="tree", autumn="tree"))


def pla_crop_state(crop, season=None, month=None):
    """the drawn state of a crop in a season: tree / bare / seedling / growing / ripe / fruit / harvested"""
    return PLA_CROP_STATE[crop][_pla_s(season, month) or "general"]


def _pla_crop_cols(beyond=False):
    """the crop leaf colours (one set for cotton, maize, tomato; pending research like all plant colours)"""
    c = _pla_c(PLA_CROP_LEAF)
    c["shade"] = _sec_mix(c["fill"], c["edge"], 0.25)
    if beyond:
        c = dict((k_, _sec_mix(v, SEC["paper"], 0.55) if v else v) for k_, v in c.items())
    return c


def _pla_crop_size(crop, h_m, crown_m):
    if crop == "olive":                         # orchard trees kept to their in-row spacing (rule); h by the olive ratio
        w = crown_m or PLA_CROPS["olive"]["plant_m"]
        return pla_height_ok("olive", h_m or w / PLA_FORM_RATIO["gnarled"]), w   # G6: never below the sourced 8 m
    if h_m is None or crown_m is None:
        raise ValueError("plants: %s plant size is not sourced: pass h_m and crown_m" % crop)
    return h_m, crown_m


def _pla_crop_sec(crop, x, gy, h, w, k, i, beyond, state="growing", season=None):
    """One crop plant in section, in its season's state (bare: nothing; harvested: stubble; seedling: young)."""
    if crop == "olive":
        c = pla_colours("olive", season, beyond=beyond)
        img = _pla_img_draw("olive", season, "side", x, gy, h, w, k, pla_colours("olive", season), i, beyond, 0, False)
        if img is None:
            img = _pla_missing_draw("olive", season, "side", x, gy, h, w, k)
        return img if img is not None else _pla_sec("gnarled", x, gy, h, w, k, c, i)
    c = _pla_crop_cols(beyond)
    if state == "bare":
        return []
    if state != "harvested":                     # round 5: crop image (asset png / hires), else placeholder / vector
        hh, ww = (0.30 * h, 0.40 * w) if state == "seedling" else (h, w)
        c0 = _pla_crop_cols(False)
        img = _pla_img_draw(crop, season, "side", x, gy, hh, ww, k, c0, i, beyond, 0, False)
        if img is None:
            img = _pla_missing_draw(crop, season, "side", x, gy, hh, ww, k)
        if img is not None:
            return img
    if state == "harvested":                    # stubble: short cut stems (rule 12 % of the height)
        return [("line", [(x + d * w * k * 0.3, gy), (x + d * w * k * 0.32, gy + 0.12 * h * k)], PLA_ROW, 0.1)
                for d in (-0.5, 0.0, 0.5)]
    if state == "seedling":                     # young plant (drawing rule: 30 % height, 40 % width)
        h, w = 0.30 * h, 0.40 * w
    H, R = h * k, w / 2.0 * k
    if crop == "maize":                         # stalk, arching leaves in two tones, tassel when grown
        sh = [("line", [(x, gy), (x, gy + H)], c["shade"], 0.2)]
        for j in range(1, 7):
            py, s_ = gy + H * (0.15 + 0.11 * j), (1 if j % 2 else -1)
            sh.append(("line", [(x, py), (x + s_ * R * 0.6, py + 0.08 * H), (x + s_ * R, py - 0.02 * H)],
                       c["fill"] if j % 2 else c["shade"], 0.14))
        if state != "seedling":
            sh.append(("line", [(x, gy + 0.92 * H), (x, gy + H)], PLA_REED_HEAD, 0.35))
        return sh
    if crop == "cotton":                        # small branched bush (two masses), open bolls when ripe
        sh = [("line", [(x, gy), (x, gy + 0.5 * H)], c["stem"], 0.12)]
        sh += _pla_mass(x - 0.35 * R, gy + 0.55 * H, 0.6 * R, 0.4 * H, 0.3 * H, c, i, 0.15)
        sh += _pla_mass(x + 0.35 * R, gy + 0.6 * H, 0.6 * R, 0.38 * H, 0.3 * H, c, i + 5, 0.15)
        if state == "ripe":
            for d, e_ in ((-0.5, 0.6), (0.1, 0.85), (0.55, 0.55)):
                sh.append(("poly", sec_ellipse(x + d * R, gy + e_ * H, 0.1 * R + 0.1, 0.1 * R + 0.1, 8), PLA_BOLL,
                           c["edge"], 0.05))
        return sh
    if crop == "tomato":                        # low sprawling plant (two masses), fruit in summer
        sh = _pla_mass(x - 0.3 * R, gy + 0.3 * H, 0.7 * R, 0.6 * H, 0.3 * H, c, i, 0.15)
        sh += _pla_mass(x + 0.35 * R, gy + 0.28 * H, 0.65 * R, 0.55 * H, 0.28 * H, c, i + 5, 0.15)
        if state == "fruit":
            for d, e_ in ((-0.45, 0.35), (0.2, 0.5), (0.6, 0.3)):
                sh.append(("poly", sec_ellipse(x + d * R, gy + e_ * H, 0.08 * R + 0.1, 0.08 * R + 0.1, 8), PLA_FRUIT,
                           None, 0.0))
        return sh
    raise ValueError("plants: unknown crop %r" % crop)


def pla_crop_rows(crop, x0, x1, gy, k, spacing=None, h_m=None, crown_m=None, beyond=False, season=None, month=None):
    """Crop plants along a cut from x0 to x1 (page mm), spacing m apart (the row spacing for a cut across the rows;
    sourced default only for olive), centred in the stretch; gy a number or a function of x. season (month= alias):
    the crop's state that season (pla_crop_state; winter = bare ground: no plants)."""
    if crop not in PLA_CROPS:
        raise ValueError("plants: unknown crop %r" % crop)
    sp = spacing or PLA_CROPS[crop]["row_m"]
    if sp is None:
        raise ValueError("plants: %s row spacing is not sourced: pass spacing (m)" % crop)
    s_ = _pla_s(season, month)
    state = pla_crop_state(crop, s_)
    _pla_count("crop_" + crop, s_)
    h, w = _pla_crop_size(crop, h_m, crown_m)
    n = int((x1 - x0) / (sp * k) + 1e-9)
    off = ((x1 - x0) - n * sp * k) / 2.0
    sh = []
    for i in range(n + 1):
        x = x0 + off + i * sp * k
        sh += _pla_crop_sec(crop, x, gy(x) if callable(gy) else gy, h, w, k, i, beyond, state, s_)
    return sh


def _pla_ring(rr):
    """A ring from a ring or an (x0, y0, x1, y1) rectangle (page mm)."""
    if len(rr) == 4 and not isinstance(rr[0], (tuple, list)):
        x0, y0, x1, y1 = rr
        return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return list(rr)


def pla_crop_plan(crop, ring_or_rect, k, row_spacing=None, plant_spacing=None, ang_deg=0.0, crown_m=None,
                  field=True, season=None, month=None):
    """A field or orchard block in plan: rows at row_spacing (m) at ang_deg; with plant_spacing, single plants along
    each row (true crown with crown_m or for olive, else a fixed 0.25 mm dot). Sourced defaults only for olive.
    season (month= alias): bare / harvested fields show their furrows only, young crops small dots."""
    import math as _m
    if crop not in PLA_CROPS:
        raise ValueError("plants: unknown crop %r" % crop)
    ring = _pla_ring(ring_or_rect)
    rs = row_spacing or PLA_CROPS[crop]["row_m"]
    ps = plant_spacing or PLA_CROPS[crop]["plant_m"]
    if rs is None:
        raise ValueError("plants: %s row spacing is not sourced: pass row_spacing (m)" % crop)
    s_ = _pla_s(season, month)
    state = pla_crop_state(crop, s_)
    _pla_count("crop_" + crop, s_)
    cc = _pla_crop_cols()
    sh = [("poly", ring, PLA_FIELD, None, 0.1)] if field else []
    w = crown_m or (PLA_CROPS["olive"]["plant_m"] if crop == "olive" else None)   # olive: crown = in-row spacing
    oc = pla_colours("olive", s_) if crop == "olive" else None
    for i, (p, q) in enumerate(sec_hatch(ring, rs * k, ang_deg)):
        if ps is None or state in ("bare", "harvested"):
            sh.append(("line", [p, q], PLA_ROW, 0.08 if state in ("bare", "harvested") else 0.15))
            continue
        L = _m.hypot(q[0] - p[0], q[1] - p[1])
        if L < 1e-6:
            continue
        ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
        n = int(L / (ps * k) + 1e-9)
        s0 = (L - n * ps * k) / 2.0
        for j in range(n + 1):
            px, py = p[0] + ux * (s0 + j * ps * k), p[1] + uy * (s0 + j * ps * k)
            if crop == "olive":
                sh += _pla_plan("gnarled", px, py, w, k, oc, i * 31 + j)
            elif w and state != "seedling":
                r = w / 2.0 * k
                sh += _pla_mass(px, py, r, r, r, cc, i * 31 + j, 0.12, edge=False)
            else:
                sh.append(("poly", sec_ellipse(px, py, 0.125, 0.125, 8), cc["fill"], None, 0.0))
    return sh


def _pla_lined(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m, media_m, wl_y):
    """A lined, off-line cell in section: walls with a raised kerb, liner closing floor and walls (RESULT §A D2:
    liner on floor and walls, kerb above the rim: our inference there), optional gravel media and water.
    Returns (shapes, planting y)."""
    if kerb_h_m is None:
        raise ValueError("plants: kerb_h_m is required (kerb height not sourced)")
    t, top = kerb_t_m * k, rim_y + kerb_h_m * k
    sh = []
    for a, b in ((x0 - t, x0), (x1, x1 + t)):
        sh += sct_hatch_fill([(a, bed_y), (a, top), (b, top), (b, bed_y)], "concrete", k, SCT["cut"], 0.25)
    sh += sct_hatch_fill([(x0 - t, bed_y - t), (x1 + t, bed_y - t), (x1 + t, bed_y), (x0 - t, bed_y)], "concrete", k,
                         SCT["cut"], 0.25)
    g = bed_y
    if media_m:
        g = bed_y + media_m * k
        sh += sct_hatch_fill([(x0, bed_y), (x1, bed_y), (x1, g), (x0, g)], "gravel", k)
    if wl_y is not None and wl_y > g:
        sh += sec_water([(x0, g), (x1, g), (x1, wl_y), (x0, wl_y)])
    return sh, g


def _pla_liner(x0, x1, bed_y, rim_y, k, kerb_h_m):
    top = rim_y + kerb_h_m * k
    return [("line", [(x0, top), (x0, bed_y), (x1, bed_y), (x1, top)], SEC["ink"], 0.4)]


def pla_reed_basin(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m=0.15, media_m=None, wl_y=None, h_m=None, step_m=None,
                   season=None, month=None):
    """Common reed in a lined, root-contained, off-line basin (D2 a) in section: inside x0-x1, floor bed_y, rim rim_y
    (page mm). kerb_t_m 0.15 m and floor slab = drawing rule; stems step_m apart in two tones; plumes only in the
    season's state (Jul-Nov S2, cut before Nov S11; general: with plumes)."""
    sp = PLA_SPECIES["reed"]
    sh, g = _pla_lined(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m, media_m, wl_y)
    h = h_m or sp["h_m"]
    st = (step_m or 1.0 / 3.0) * k              # 9 seedlings/m² (Korkusuz et al. 2004, S20) = 1/3 m apart
    s_ = _pla_s(season, month)
    _pla_count("reed", s_)
    c = pla_colours("reed", s_)
    i, x = 0, x0 + st / 2.0
    while x < x1:
        hh = h * k * (0.8 + 0.2 * _pla_rnd(i, 5))
        lean = 0.04 * hh * (1 if i % 2 else -1)
        sh.append(("line", [(x, g), (x + lean, g + hh)], c["fill"] if i % 3 else c["shade"], 0.12))
        if i % 3 == 0 and c["accent"]:          # plume
            ry = 0.2 * k + 0.2
            sh.append(("poly", sec_ellipse(x + lean, g + hh - ry, 0.06 * k + 0.1, ry, 10), c["accent"], None, 0.0))
        x += st
        i += 1
    return sh + _pla_liner(x0, x1, bed_y, rim_y, k, kerb_h_m)


def pla_mint_cell(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m=0.15, media_m=None, wl_y=None, h_m=None, crown_m=None,
                  season=None, month=None):
    """Water mint only in a lined basin cell (D6) in section, same build as pla_reed_basin; mounds side by side in
    the season's colours."""
    sp = PLA_SPECIES["mint"]
    sh, g = _pla_lined(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m, media_m, wl_y)
    h, w = h_m or sp["h_m"], crown_m or sp["crown_m"]
    s_ = _pla_s(season, month)
    _pla_count("mint", s_)
    c = pla_colours("mint", s_)
    n = max(1, int((x1 - x0) / (w * k)))
    for i in range(n):
        sh += _pla_sec("mound", x0 + (i + 0.5) * (x1 - x0) / n, g, h, min(w, (x1 - x0) / n / k), k, c, i)
    return sh + _pla_liner(x0, x1, bed_y, rim_y, k, kerb_h_m)


def pla_cell_plan(kind, ring_or_rect, k, kerb_t_m=0.15, season=None, month=None):
    """A lined cell in plan, kind 'reed' or 'mint': wet ground, the kerb as a band kerb_t_m wide, the plants in the
    season's colours."""
    if kind not in ("reed", "mint"):
        raise ValueError("pla_cell_plan: kind is 'reed' or 'mint'")
    ring = _pla_ring(ring_or_rect)
    sp = PLA_SPECIES[kind]
    s_ = _pla_s(season, month)
    _pla_count(kind, s_)
    c = pla_colours(kind, s_)
    sh = [("poly", ring, PLA_WET, None, 0.1)]
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    if kind == "reed":                          # stems on the 1/3 m grid, never denser than 0.9 mm on the page
        d = max(0.9, k / 3.0)
        for i in range(int((max(xs) - min(xs)) / d) + 1):
            for j in range(int((max(ys) - min(ys)) / d) + 1):
                px = min(xs) + (i + 0.5 * (j % 2) + 0.25) * d
                py = min(ys) + (j + 0.5) * d
                if _sct_inside(ring, (px, py)):
                    sh.append(("line", [(px - 0.2 * d, py - 0.25 * d), (px + 0.2 * d, py + 0.25 * d)],
                               c["fill"] if (i + j) % 3 else c["shade"], 0.1))
    else:
        w = sp["crown_m"] * k
        for i in range(int((max(xs) - min(xs)) / w) + 1):
            for j in range(int((max(ys) - min(ys)) / w) + 1):
                px, py = min(xs) + (i + 0.5) * w, min(ys) + (j + 0.5) * w
                if _sct_inside(ring, (px, py)):
                    sh += _pla_plan("mound", px, py, sp["crown_m"] * 0.9, k, c, i * 7 + j)
    sh.append(("poly", ring, None, SCT["line"], max(0.15, kerb_t_m * k)))
    return sh


# ---- purpose tags (G9, M6; H-B 30 Oct 2026): what each plant group does. From the species roles of the water board
# (SPECIES.py role: shade, hold the bank, clean, scent, flower, harvest) mapped onto M6's six words, plus plain
# riparian ecology (marked "?" in PLA_PURPOSE_UNSURE: not from a project source; check before printing as a claim).
PLA_TAGS = ("wind", "noise", "shade", "corridor", "cleaning", "perception")
PLA_PURPOSE = {
    "plane": ("shade", "corridor"),
    "ash": ("shade", "corridor"),
    "willow": ("shade", "cleaning", "corridor"),
    "olive": ("shade", "perception"),
    "stone_pine": ("shade", "wind", "perception"),
    "tamarisk": ("shade", "wind", "corridor"),
    "chaste": ("perception", "corridor"),
    "rosemary": ("perception",),
    "lavender": ("perception",),
    "loosestrife": ("cleaning", "perception", "corridor"),
    "soft_rush": ("cleaning", "corridor"),
    "rush": ("cleaning", "corridor"),
    "reed": ("cleaning", "noise", "corridor"),
    "mint": ("cleaning", "perception"),
}
PLA_PURPOSE_UNSURE = {   # tags assigned from general ecology, not from a project source
    "plane": ("corridor",), "ash": ("corridor",), "willow": ("corridor",), "olive": ("perception",),
    "stone_pine": ("shade", "wind", "perception"), "tamarisk": ("wind", "corridor"), "chaste": ("corridor",),
    "loosestrife": ("corridor",), "soft_rush": ("corridor",), "rush": ("cleaning", "corridor"),
    "reed": ("noise", "corridor"),
}


def pla_purpose(key, sure_only=False):
    """the purpose tags of a species (PLA_TAGS words); sure_only drops the ones from general ecology"""
    t = PLA_PURPOSE.get(key, ())
    return tuple(x for x in t if not (sure_only and x in PLA_PURPOSE_UNSURE.get(key, ())))


# ---- ecological bands (G9): t = 0 at the water's edge (wet, low) to 1 on the dry upper ground (high). Each species
# grows around its niche centre (t, half width, weight): drawing rules from the species' habitat words in
# species.json (emergent / bank / dry slope), not measured distances. Reed and water mint: lined cells only (D2, D6).
PLA_NICHE = {
    "soft_rush": (0.04, 0.12, 1.0), "loosestrife": (0.10, 0.14, 0.9), "rush": (0.14, 0.12, 0.6),
    "willow": (0.24, 0.17, 0.8), "tamarisk": (0.36, 0.22, 0.7), "ash": (0.46, 0.20, 0.6), "plane": (0.52, 0.20, 0.5),
    "chaste": (0.55, 0.24, 0.8), "olive": (0.80, 0.20, 0.6), "rosemary": (0.86, 0.17, 0.8), "lavender": (0.90, 0.15, 0.8),
    "stone_pine": (0.92, 0.12, 0.3),
}


def _pla_canopy(key):
    return PLA_SPECIES[key]["layer"] == "tree"


def _pla_pick(t, rnd, keys, mix, canopy):
    """a species for band position t (weighted by niche), or None for an open gap"""
    import math as _m
    ws = []
    for k_ in keys:
        if _pla_canopy(k_) != canopy:
            continue
        tc, hw, w0 = PLA_NICHE[k_]
        w = (mix.get(k_, w0) if isinstance(mix, dict) else w0) * _m.exp(-((t - tc) / hw) ** 2)
        if w > 0.02:
            ws.append((k_, w))
    tot = sum(w for _k, w in ws)
    if tot < 0.12:                                 # nothing at home here: leave the ground open
        return None
    r = rnd() * tot
    for k_, w in ws:
        r -= w
        if r <= 0:
            return k_
    return ws[-1][0]


def _pla_size_var(key, rnd):
    """(h, crown) of one plant: the drawing size x 0.88-1.08, kept inside the sourced height range"""
    sp = PLA_SPECIES[key]
    f = 0.88 + 0.20 * rnd()
    return pla_height_ok(key, sp["h_m"] * f), sp["crown_m"] * f


def _pla_keys(mix):
    # round 4 (D1, PLAN §4.9): mix=None no longer draws the willow; it is planted only where a mix names it
    keys = list(mix) if mix else [k_ for k_ in PLA_NICHE if k_ != "willow"]
    bad = [k_ for k_ in keys if k_ not in PLA_NICHE]
    if bad:
        raise ValueError("plants scatter: %s not free-planted (cells only, removed or unknown)" % ", ".join(bad))
    return keys


def pla_scatter_section(x0, x1, gy, k, t0=0.0, t1=1.0, mix=None, seed=0, layer=0, style="b", density=1.0,
                        hires=True, avoid=None, detail=True, month=None, season=None, water=None):
    """a mixed, naturalistic planting along a cut from x0 to x1 (page mm), ground gy (number or function of x): the
    band position runs from t0 at x0 to t1 at x1 (0 = water's edge, 1 = dry upper ground; or pass t0 as a function
    of x). Canopy trees and the low layer are spaced independently (crowns overlap, shrubs stand under tree edges),
    each gap random and never equal to the one before (no rows, no repeated clusters). mix: species keys (list) or
    {key: weight}. avoid: [(xa, xb)] page mm where nothing is planted (paths, water, steps). water: page y (or a
    function of x) of the water: where the ground lies under it only emergent species grow. season (month= alias):
    pla_section. Returns (shapes,
    placed [(key, x, h_m, crown_m)]), drawn tall first so the low layer reads in front."""
    keys = _pla_keys(mix)
    rnd = _pla_rng(seed * 7 + 3)
    sc = globals()["fig_depth"](layer)[0] if layer and globals().get("fig_depth") else 1.0
    K = k * sc

    def tt(x):
        if callable(t0):
            return t0(x)
        return t0 + (t1 - t0) * (x - x0) / float(max(1e-9, x1 - x0))

    def blocked(x, key):
        if any(a <= x <= b for a, b in (avoid or ())):
            return True
        if water is None or PLA_SPECIES[key]["layer"] == "emergent":
            return False
        g_ = gy(x) if callable(gy) else gy
        return g_ < (water(x) if callable(water) else water)
    placed = []
    for canopy in (True, False):
        x, last_gap = x0 + rnd() * 1.5 * K, None
        while x < x1:
            key = _pla_pick(tt(x), rnd, keys, mix, canopy)
            if key is None or blocked(x, key):
                x += (0.8 + rnd()) * K
                continue
            h, w = _pla_size_var(key, rnd)
            placed.append((key, x, h, w))
            f = 0.85 if canopy else 0.75
            gap = f * w * (0.7 + 1.1 * rnd()) / max(0.2, density) * K
            if last_gap is not None and abs(gap - last_gap) < 0.15 * gap:     # never an even rhythm
                gap *= 1.35 if rnd() > 0.5 else 0.72
            last_gap = gap
            x += max(0.3 * K, gap)
    placed.sort(key=lambda p_: -p_[2])
    sh = []
    for i, (key, x, h, w) in enumerate(placed):
        sh += pla_section(key, x, gy, k, h_m=h, crown_m=w, seed=seed + i, hires=hires, style=style, layer=layer,
                          detail=detail, month=month, season=season)
    return sh, placed


# ---- round 4 (S3, D7, G-R4-5.2): the low layer of shrubs and flowers. Only the sourced species already in the
# booklet (D7): chaste tree, rosemary, French lavender, purple loosestrife, soft rush, placed by wetness band
# (PLA_NICHE: loosestrife and soft rush at the water, chaste tree on the moist ground, rosemary and lavender on the
# dry tops). Every section gets one (BRIEF G-R4-5.2), and every undefined planted area in plan (pla_low_plan).
PLA_LOW = ("chaste", "rosemary", "lavender", "loosestrife", "soft_rush")


def pla_low_section(x0, x1, gy, k, t0=0.0, t1=1.0, seed=0, layer=0, density=1.2, avoid=None, water=None,
                    season=None, month=None, mix=None, detail=True):
    """the shrub and flower layer along a cut x0..x1 (page mm), band t0 -> t1 (0 = water's edge, 1 = dry top; or t0
    a function of x), mixed by wetness, never in rows (pla_scatter_section with the PLA_LOW species or `mix`, a
    subset); water / avoid as there. Returns (shapes, placed [(key, x, h_m, crown_m)])."""
    return pla_scatter_section(x0, x1, gy, k, t0, t1, mix=mix or PLA_LOW, seed=seed, layer=layer, density=density,
                               avoid=avoid, detail=detail, month=month, season=season, water=water)


def pla_low_plan(ring, k, gradient, seed=0, density=1.2, avoid=None, season=None, month=None, mix=None, max_n=3000):
    """the shrub and flower layer in an undefined planted area in plan (ring page mm; gradient as pla_scatter_plan),
    the PLA_LOW species (or `mix`, a subset) by wetness. Returns (shapes, placed [(key, x, y, crown_m)])."""
    return pla_scatter_plan(ring, k, gradient, mix=mix or PLA_LOW, seed=seed, density=density, avoid=avoid,
                            max_n=max_n, month=month, season=season)


# ---- G9 mixed groups in section (R2-A 31 Oct 2026) -------------------------------------------------------------------
# Drawing rules (not data): a group is 5-16 m wide with 2-12 m open gaps between groups (both / density), canopy
# trees step 35-75 % of a crown apart (crowns overlap), each plant's height = its drawing size x 0.70-1.10 kept
# inside the sourced range (pla_height_ok); the low layer stands under and around the tree edges.
PLA_GROUP = dict(group_m=(5.0, 16.0), gap_m=(2.0, 12.0), step=(0.35, 0.75), size=(0.70, 1.10))


def _pla_group_size(key, rnd):
    sp = PLA_SPECIES[key]
    lo, hi = PLA_GROUP["size"]
    f = lo + (hi - lo) * rnd()
    return pla_height_ok(key, sp["h_m"] * f), sp["crown_m"] * f


def _pla_other(t, rnd, keys, mix, canopy, not_key):
    """a species other than not_key for band position t (None if nothing else grows here)"""
    for _i in range(8):
        k_ = _pla_pick(t, rnd, keys, mix, canopy)
        if k_ is not None and k_ != not_key:
            return k_
    return None


def pla_group_section(x0, x1, gy, k, t0=0.0, t1=1.0, mix=None, seed=0, layers=(2, 1, 0), style="a", density=1.0,
                      avoid=None, hires=True, detail=True, ground=None, water=None, month=None, season=None):
    """G9 planting in section: mixed groups, never rows. Along x0..x1 (page mm), band t0 -> t1 (0 = water's edge,
    1 = dry upper ground; or t0 = a function of x), each depth layer of `layers` (D9, back first: 2, 1, 0) gets
    groups at irregular places; in a group the canopy trees overlap their crowns and the low layer (shrubs,
    emergent, ground) stands under and around them; species interpenetrate by band (wet to dry, low to high: the
    niche weights of PLA_NICHE) and a group always holds two or more species and three or more plants (never one
    species standing alone, never an identical cluster: sizes and gaps vary). Each plant: a varied height inside its
    sourced range, a cutout variant picked by its seed (style a), mirrored on odd seeds, seated on the lowest ground
    under its base (G14 sf_seat_x). ground = {layer: gy} gives a depth layer its own ground (else gy); water = page
    y or function of x: where the ground lies under the water only emergent species grow; avoid = [(xa, xb)] page
    mm kept free (paths, steps, lanes). Returns (shapes back to front, placed [(key, x, h_m, crown_m, layer)],
    groups [(layer, xa, xb, [keys], purpose tags)]): use groups to say what each group does (G9) and placed for
    sf_assert_g6."""
    keys = _pla_keys(mix)
    rnd = _pla_rng(seed * 11 + 5)
    seat = globals().get("sf_seat_x")
    gfn = globals().get("_sf_fn")

    def tt(x):
        if callable(t0):
            return t0(x)
        return t0 + (t1 - t0) * (x - x0) / float(max(1e-9, x1 - x0))

    def blocked(x):
        return any(a <= x <= b for a, b in (avoid or ()))
    sh, placed, groups, n = [], [], [], 0
    for layer in layers:
        g_ = (ground or {}).get(layer, gy)
        g_ = gfn(g_) if gfn else g_
        sc = globals()["fig_depth"](layer)[0] if layer and globals().get("fig_depth") else 1.0
        K = k * sc

        def wet(x):
            if water is None:
                return False
            w_ = water(x) if callable(water) else water
            return (g_(x) if callable(g_) else g_) < w_

        def ok(key, x):
            return not blocked(x) and (not wet(x) or PLA_SPECIES[key]["layer"] == "emergent")
        x = x0 + rnd() * PLA_GROUP["gap_m"][1] * 0.5 * K
        while x < x1:
            gw = (PLA_GROUP["group_m"][0] + (PLA_GROUP["group_m"][1] - PLA_GROUP["group_m"][0]) * rnd()) * K
            xa, xb = x, min(x1, x + gw)
            mem = []
            xx = xa + 0.1 * rnd() * gw                     # canopy: overlapping crowns
            while xx < xb:
                key = _pla_pick(tt(xx), rnd, keys, mix, True)
                if key is not None and mem and all(m[0] == key for m in mem) and rnd() < 0.6:
                    key = _pla_other(tt(xx), rnd, keys, mix, True, key) or key
                if key is None or not ok(key, xx):
                    xx += (0.6 + rnd()) * K
                    continue
                h, w = _pla_group_size(key, rnd)
                mem.append((key, xx, h, w, True))
                xx += (PLA_GROUP["step"][0] + (PLA_GROUP["step"][1] - PLA_GROUP["step"][0]) * rnd()) * w * K
            nl = 2 + int(rnd() * 4.999)                     # low layer: 2-6, under and around the crowns
            for _i in range(nl):
                xl = xa - 0.1 * gw + 1.2 * gw * rnd()
                if xl < x0 or xl > x1:
                    continue
                key = _pla_pick(tt(xl), rnd, keys, mix, False)
                if key is None or not ok(key, xl):
                    continue
                h, w = _pla_group_size(key, rnd)
                mem.append((key, xl, h, w, False))
            sp = set(m[0] for m in mem)
            if len(sp) == 1 and mem:                       # one species alone: add another that grows here
                for _i in range(3):
                    xl = xa + gw * rnd()
                    for canopy in (False, True):
                        key = _pla_other(tt(xl), rnd, keys, mix, canopy, mem[0][0])
                        if key is not None and ok(key, xl) and xl <= x1:
                            h, w = _pla_group_size(key, rnd)
                            mem.append((key, xl, h, w, canopy))
                            break
                    if len(set(m[0] for m in mem)) > 1:
                        break
            if len(mem) >= 3 and len(set(m[0] for m in mem)) >= 2:
                mem.sort(key=lambda m: -m[2])              # tall first: the low layer reads in front
                ks = sorted(set(m[0] for m in mem))
                tags = sorted(set(t_ for k_ in ks for t_ in pla_purpose(k_, sure_only=True)))
                groups.append((layer, xa, xb, ks, tags))
                for key, xp, h, w, canopy in mem:
                    half = (0.12 if canopy else 0.35) * w * K
                    gyp = seat(g_, xp, half) if seat else (g_(xp) if callable(g_) else g_)
                    sh += pla_section(key, xp, gyp, k, h_m=h, crown_m=w, seed=seed * 1000 + n, hires=hires,
                                      style=style, layer=layer, detail=detail, month=month, season=season)
                    placed.append((key, xp, h, w, layer))
                    n += 1
            x = xb + (PLA_GROUP["gap_m"][0] + (PLA_GROUP["gap_m"][1] - PLA_GROUP["gap_m"][0]) * rnd()) / \
                max(0.2, density) * K
    if not groups:
        msg = u"Plants: no mixed group fits %s (a group needs two or more species growing in its band)" % (
            u", ".join(keys))
        if msg not in PLA_LOG:
            PLA_LOG.append(msg)
    return sh, placed, groups


def _pla_rng(seed):
    s = [int(seed * 2654435761 + 97) & 0x7fffffff]

    def r():
        s[0] = (s[0] * 1103515245 + 12345) & 0x7fffffff
        return s[0] / float(0x7fffffff)
    return r


def _pla_seg_d(p, a, b):
    import math as _m
    dx, dy = b[0] - a[0], b[1] - a[1]
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 < 1e-12 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
    return _m.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def _pla_grad_fn(gradient, k):
    """t(x, y) from a function, or from {"wet": polyline page mm, "width_m": band width}: distance to the wet line
    over the band width, 0..1"""
    if callable(gradient):
        return gradient
    wet, wd = gradient["wet"], float(gradient["width_m"]) * k

    def f(x, y):
        d = min(_pla_seg_d((x, y), a, b) for a, b in zip(wet[:-1], wet[1:]))
        return max(0.0, min(1.0, d / wd))
    return f


def _pla_rowlike(c, pts, d_lim):
    """True when c continues a straight, evenly spaced line of two neighbours (a row in the making)"""
    import math as _m
    near = sorted((q for q in pts if _m.hypot(q[0] - c[0], q[1] - c[1]) < d_lim),
                  key=lambda q: (q[0] - c[0]) ** 2 + (q[1] - c[1]) ** 2)[:8]     # the 8 nearest are enough
    for b in near:
        dbc = _m.hypot(c[0] - b[0], c[1] - b[1])
        for a in near:
            if a is b:
                continue
            dab = _m.hypot(b[0] - a[0], b[1] - a[1])
            if dab < 1e-9 or abs(dab - dbc) > 0.2 * dbc:
                continue
            u = ((b[0] - a[0]) / dab, (b[1] - a[1]) / dab)
            v = ((c[0] - b[0]) / dbc, (c[1] - b[1]) / dbc)
            if u[0] * v[0] + u[1] * v[1] > 0.985:        # within about 10 degrees of straight on
                return True
    return False


def pla_scatter_plan(ring, k, gradient, mix=None, seed=0, density=1.0, avoid=None, max_n=3000, month=None,
                     season=None):
    """a mixed planting in plan inside ring (page mm): Poisson-disc style dart throwing, canopy trees first then the
    low layer, each species picked by its niche at t = gradient(x, y) (a function, or {"wet": polyline, "width_m":
    m}); same-layer plants keep 0.8 x (r1 + r2) apart, shrubs may stand under tree edges (0.3 x), candidates that
    would extend a straight evenly spaced line are thrown away: no rows, grids, axes or repeated clusters. avoid:
    rings (page mm) left empty. month: seasonal colours / bare (pla_plan). Returns (shapes, placed [(key, x, y,
    crown_m)]); canopy crowns drawn opaque over the low layer (round 3 D7: no alpha anywhere)."""
    import math as _m
    keys = _pla_keys(mix)
    rnd = _pla_rng(seed * 11 + 5)
    tf = _pla_grad_fn(gradient, k)
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    bx0, by0, bw, bh = min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)
    area = abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(ring, ring[1:] + ring[:1]))) / 2.0
    placed = {True: [], False: []}
    grids = {True: {}, False: {}}
    rmax = {c_: max([PLA_SPECIES[k_]["crown_m"] * 1.08 / 2.0 * k for k_ in keys if _pla_canopy(k_) == c_] or [0.5 * k])
            for c_ in (True, False)}

    def cell(c_, x, y):
        s_ = 2.0 * rmax[c_]
        return int(_m.floor(x / s_)), int(_m.floor(y / s_))

    def near(c_, x, y, dist):
        s_ = 2.0 * rmax[c_]
        n = int(_m.ceil(dist / s_))
        i0, j0 = cell(c_, x, y)
        out = []
        for i in range(i0 - n, i0 + n + 1):
            for j in range(j0 - n, j0 + n + 1):
                out += grids[c_].get((i, j), ())
        return out
    total = 0
    for canopy in (True, False):
        r_typ = (sum(PLA_SPECIES[k_]["crown_m"] for k_ in keys if _pla_canopy(k_) == canopy) /
                 max(1, sum(1 for k_ in keys if _pla_canopy(k_) == canopy))) / 2.0 * k
        if r_typ <= 0:
            continue
        tries = int(min(30000, 6.0 * density * area / (_m.pi * r_typ * r_typ) + 50))
        for _i in range(tries):
            if total >= max_n:
                break
            x, y = bx0 + rnd() * bw, by0 + rnd() * bh
            if not _sct_inside(ring, (x, y)) or any(_sct_inside(a, (x, y)) for a in (avoid or ())):
                continue
            key = _pla_pick(tf(x, y), rnd, keys, mix, canopy)
            if key is None:
                continue
            h, w = _pla_size_var(key, rnd)
            r = w / 2.0 * k
            ok = True
            for (qx, qy, qr, _qk) in near(canopy, x, y, 0.8 * (r + rmax[canopy])):
                if _m.hypot(qx - x, qy - y) < 0.8 * (r + qr) / max(0.3, density) ** 0.5:
                    ok = False
                    break
            if ok and not canopy:
                for (qx, qy, qr, _qk) in near(True, x, y, 0.3 * (r + rmax[True])):
                    if _m.hypot(qx - x, qy - y) < 0.3 * (r + qr):
                        ok = False
                        break
            if ok and canopy:
                for (qx, qy, qr, _qk) in near(False, x, y, 0.3 * (r + rmax[False])):
                    if _m.hypot(qx - x, qy - y) < 0.3 * (r + qr):
                        ok = False
                        break
            if ok and _pla_rowlike((x, y), [(q[0], q[1]) for q in near(canopy, x, y, 3.0 * (r + rmax[canopy]))],
                                   3.0 * (r + rmax[canopy])):
                ok = False
            if not ok:
                continue
            e = (x, y, r, key)
            placed[canopy].append(e)
            grids[canopy].setdefault(cell(canopy, x, y), []).append(e)
            total += 1
    sh, out = [], []
    for canopy in (False, True):
        for i, (x, y, r, key) in enumerate(placed[canopy]):
            sh += pla_plan(key, x, y, k, crown_m=2.0 * r / k, seed=seed + i * 3 + (7 if canopy else 0), month=month,
                           season=season)
            out.append((key, x, y, 2.0 * r / k))
    return sh, out


# ---- field / orchard tile (D7 a, D2 a): one texture + one representative symbol in the middle of the area ----------
def _pla_inner_point(ring):
    """a point well inside the ring: the grid point farthest from the edge (12 x 12 search)"""
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    best, bd = None, -1.0
    for i in range(1, 12):
        for j in range(1, 12):
            p = (min(xs) + (max(xs) - min(xs)) * i / 12.0, min(ys) + (max(ys) - min(ys)) * j / 12.0)
            if not _sct_inside(ring, p):
                continue
            d = min(_pla_seg_d(p, a, b) for a, b in zip(ring, ring[1:] + ring[:1]))
            if d > bd:
                best, bd = p, d
    return best or (sum(xs) / len(xs), sum(ys) / len(ys))


def pla_field_tile(ring_or_rect, k, crop="olive", symbol_mm=None, seed=0, fill=None, texture=True, season=None,
                   month=None):
    """a farm or orchard area simplified (D7 a, r3 #31): the field fill, an even scatter of short furrow marks (one
    texture, no rows) and ONE symbol of the crop in the middle, drawn at print quality in the crop's season state
    (olive: the olive plan symbol; other crops: a two-tone crop tuft, bolls / fruit when ripe, stubble when
    harvested, bare furrows in winter). symbol_mm = the symbol's width on the page (default the true olive crown 5 m
    x k, at least 6 mm: a symbol, not to scale). Returns shapes."""
    import math as _m
    if crop not in PLA_CROPS:
        raise ValueError("plants: unknown crop %r" % crop)
    ring = _pla_ring(ring_or_rect)
    s_ = _pla_s(season, month)
    state = pla_crop_state(crop, s_)
    _pla_count("crop_" + crop, s_)
    sh = [("poly", ring, fill or PLA_FIELD, None, 0.1)]
    if texture:
        rnd = _pla_rng(seed + 17)
        xs, ys = [p[0] for p in ring], [p[1] for p in ring]
        d = 1.6                                      # page mm between marks (texture, not a size)
        nx, ny = int((max(xs) - min(xs)) / d) + 1, int((max(ys) - min(ys)) / d) + 1
        for i in range(nx):
            for j in range(ny):
                px = min(xs) + (i + 0.15 + 0.7 * rnd()) * d
                py = min(ys) + (j + 0.15 + 0.7 * rnd()) * d
                if not _sct_inside(ring, (px, py)):
                    continue
                a = _m.radians(20.0 + 40.0 * rnd())
                L = 0.35 + 0.3 * rnd()
                sh.append(("line", [(px, py), (px + L * _m.cos(a), py + L * _m.sin(a))], PLA_ROW, 0.08))
    cx, cy = _pla_inner_point(ring)
    sm = symbol_mm or max(6.0, PLA_CROPS["olive"]["plant_m"] * k)
    if crop == "olive":
        oc = pla_colours("olive", s_)
        sh += _pla_plan("gnarled", cx, cy, sm / k, k, oc, seed)
        sh += _pla_plan_mark("olive", cx, cy, sm / 2.0, oc, seed)
        return sh
    r = sm / 2.0
    if state in ("bare", "harvested"):              # furrows (and stubble ticks when harvested)
        for j in (-1, 0, 1):
            sh.append(("line", [(cx - r, cy + 0.35 * j * r), (cx + r, cy + 0.35 * j * r)], PLA_ROW, 0.25))
            if state == "harvested":
                for i in range(-3, 4):
                    px = cx + 0.28 * i * r
                    sh.append(("line", [(px, cy + 0.35 * j * r), (px + 0.05 * r, cy + 0.35 * j * r + 0.14 * r)],
                               PLA_ROW, 0.12))
        return sh
    cc = _pla_crop_cols()
    if state == "seedling":
        r *= 0.5
    for i, (dx, dy, s_m) in enumerate(((-0.35, -0.2, 0.6), (0.32, -0.15, 0.58), (0.0, 0.25, 0.6))):
        sh += _pla_mass(cx + dx * r, cy + dy * r, s_m * r, s_m * r, s_m * r, cc, seed + i, 0.12)
    acc = {"ripe": PLA_BOLL, "fruit": PLA_FRUIT}.get(state)
    if crop == "maize" and state == "growing":
        acc = PLA_REED_HEAD                          # tassels
    if acc:
        for i in range(6):
            a = 2 * _m.pi * (i / 6.0 + 0.08)
            sh.append(("poly", sec_ellipse(cx + 0.55 * r * _m.cos(a), cy + 0.55 * r * _m.sin(a), 0.14 * r, 0.14 * r, 8),
                       acc, cc["edge"] if acc == PLA_BOLL else None, 0.05 if acc == PLA_BOLL else 0.0))
    return sh


# ---- species detail (M6 style b: "detailed from the species' photo"): leaf texture and flower marks in the crown, and
# a mark per species in plan so that no two species share a symbol. Mark sizes are page-mm conventions eased with
# the crown size; colours only from the species' own set (flower colours: only where the species row has one).
def _pla_marks_in(cx, cy, rx, ry, n, rnd):
    """n points spread inside an ellipse (jittered sunflower spiral: even, never a grid)"""
    import math as _m
    out = []
    for i in range(n):
        rr = _m.sqrt((i + 0.5) / n)
        a = i * 2.39996 + 0.6 * rnd()
        out.append((cx + rx * rr * _m.cos(a), cy + ry * rr * _m.sin(a)))
    return out


def _pla_detail(key, form, x, gy, h, w, k, c, seed):
    """leaf texture / flower marks of one species in section, over its _pla_sec silhouette"""
    import math as _m
    rnd = _pla_rng(seed * 3 + 1)
    H, R = h * k, w / 2.0 * k
    if R < 0.8:                                     # too small on the page for a texture
        return []
    lo = dict(dome=0.3, oval=0.3, weeping=0.25, gnarled=0.3, umbrella=0.65, feathery=0.55).get(form, 0.0) * H
    cx, cy = x, gy + lo + (H - lo) * (0.55 if form != "mound" else 0.45)
    rx, ry = 0.62 * R, 0.30 * (H - lo) if form != "umbrella" else 0.24 * (H - lo)   # round 4: on the masses, not gaps
    m = max(0.25, min(1.2, 0.045 * R))              # mark length, page mm
    n = int(max(6, min(70, (_m.pi * rx * ry) / (m * m * 9.0))))
    e, lt, ac = c["edge"], c["lt"], c.get("accent")
    sh = []
    pts = _pla_marks_in(cx, cy, rx, ry, n, rnd)
    for i, (px, py) in enumerate(pts):
        if key == "plane":                          # palmate leaves: three short spokes
            for a in (90.0, 30.0, 150.0):
                r_ = _m.radians(a + 20.0 * rnd())
                sh.append(("line", [(px, py), (px + m * _m.cos(r_), py + m * _m.sin(r_))], e, 0.06))
        elif key == "ash":                          # pinnate leaves: a stalk with leaflet pairs
            a = _m.radians(70.0 + 40.0 * rnd())
            ux, uy = _m.cos(a), _m.sin(a)
            sh.append(("line", [(px, py), (px + 1.4 * m * ux, py + 1.4 * m * uy)], e, 0.05))
            for t in (0.45, 0.9):
                bx_, by_ = px + t * 1.4 * m * ux, py + t * 1.4 * m * uy
                sh.append(("line", [(bx_ - 0.35 * m * uy, by_ + 0.35 * m * ux), (bx_ + 0.35 * m * uy, by_ - 0.35 * m * ux)],
                           e, 0.05))
        elif key == "willow":                       # round 3: its streamers and strands are the texture (marks
            pass                                    # spread over the envelope would float in the gaps, G14)
        elif key == "olive":                        # small lance leaves, silver above, dark below
            a = _m.radians(rnd() * 180.0)
            col = lt if i % 3 else e
            sh.append(("line", [(px, py), (px + 0.9 * m * _m.cos(a), py + 0.9 * m * _m.sin(a))], col, 0.08))
        elif key == "stone_pine":                   # needle tufts on the flat crown
            if py > cy - 0.2 * ry:
                for a in (60.0, 90.0, 120.0):
                    r_ = _m.radians(a)
                    sh.append(("line", [(px, py), (px + 0.8 * m * _m.cos(r_), py + 0.8 * m * _m.sin(r_))], lt, 0.05))
        elif key == "tamarisk":                     # scale-leaf sprays: fine stipple
            sh.append(("poly", sec_ellipse(px, py, 0.12 * m + 0.05, 0.12 * m + 0.05, 6), e, None, 0.1))
        elif key == "rosemary":                     # needle leaves
            a = _m.radians(45.0 + 90.0 * (i % 2))
            sh.append(("line", [(px, py), (px + 0.7 * m * _m.cos(a), py + 0.7 * m * _m.sin(a))], e, 0.06))
        elif key in ("lavender", "chaste", "loosestrife") and ac:
            if i % 2 == 0:                          # flowers in the species' own accent
                sh.append(("poly", sec_ellipse(px, py, 0.18 * m + 0.06, 0.28 * m + 0.08, 8), ac, None, 0.1))
        elif key == "soft_rush":                    # brown flower tufts on the side of the stems, near the top
            if py > cy and i % 3 == 0:
                sh.append(("poly", sec_ellipse(px, py, 0.25 * m + 0.08, 0.2 * m + 0.06, 8), PLA_REED_HEAD, None, 0.1))
        elif key == "rush":                         # sharp stem tips
            if py > cy and i % 2 == 0:
                sh.append(("line", [(px, py), (px, py + 0.8 * m)], e, 0.05))
        elif key == "mint":                         # small rounded leaves
            sh.append(("poly", sec_ellipse(px, py, 0.22 * m + 0.05, 0.18 * m + 0.05, 8), lt, None, 0.1))
    return sh


def _pla_plan_mark(key, cx, cy, r, c, seed):
    """the species' own mark on its plan symbol (M6: every species distinct in plan)"""
    import math as _m
    rnd = _pla_rng(seed * 5 + 2)
    e, lt, ac = c["edge"], c["lt"], c.get("accent")
    m = max(0.2, 0.18 * r)
    sh = []
    if key == "plane":                              # palmate stars
        for (px, py) in _pla_marks_in(cx, cy, 0.6 * r, 0.6 * r, 5, rnd):
            for a in (90.0, 18.0, 162.0, 234.0, 306.0):
                ra = _m.radians(a)
                sh.append(("line", [(px, py), (px + 0.5 * m * _m.cos(ra), py + 0.5 * m * _m.sin(ra))], e, 0.06))
    elif key == "ash":                              # pinnate marks
        for (px, py) in _pla_marks_in(cx, cy, 0.55 * r, 0.55 * r, 4, rnd):
            sh.append(("line", [(px - 0.6 * m, py), (px + 0.6 * m, py)], e, 0.06))
            for t in (-0.3, 0.1, 0.5):
                sh.append(("line", [(px + t * m, py - 0.25 * m), (px + t * m, py + 0.25 * m)], e, 0.05))
    elif key == "olive":                            # silver leaf speckle
        for (px, py) in _pla_marks_in(cx, cy, 0.75 * r, 0.75 * r, 9, rnd):
            sh.append(("poly", sec_ellipse(px, py, 0.12 * m + 0.05, 0.12 * m + 0.05, 6), lt, None, 0.1))
    elif key == "stone_pine":                       # dark ring inside the rim tufts
        sh.append(("poly", sec_ellipse(cx, cy, 0.55 * r, 0.55 * r, 30), None, e, 0.08))
    elif key == "willow":                           # narrow lance leaves, pale side up
        for (px, py) in _pla_marks_in(cx, cy, 0.6 * r, 0.6 * r, 8, rnd):
            a = _m.radians(rnd() * 180.0)
            sh.append(("line", [(px, py), (px + 0.7 * m * _m.cos(a), py + 0.7 * m * _m.sin(a))], lt, 0.06))
    elif key == "tamarisk":                         # stipple
        for (px, py) in _pla_marks_in(cx, cy, 0.7 * r, 0.7 * r, 14, rnd):
            sh.append(("poly", sec_ellipse(px, py, 0.06 * m + 0.04, 0.06 * m + 0.04, 6), e, None, 0.1))
    elif key == "rosemary":                         # needle crosses
        for (px, py) in _pla_marks_in(cx, cy, 0.6 * r, 0.6 * r, 6, rnd):
            sh += [("line", [(px - 0.3 * m, py - 0.3 * m), (px + 0.3 * m, py + 0.3 * m)], e, 0.05),
                   ("line", [(px - 0.3 * m, py + 0.3 * m), (px + 0.3 * m, py - 0.3 * m)], e, 0.05)]
    elif key == "soft_rush":                        # an open centre and brown tufts on a ring
        sh.append(("poly", sec_ellipse(cx, cy, 0.25 * r, 0.25 * r, 14), SEC["paper"], None, 0.1))
        for i in range(6):
            a = 2 * _m.pi * (i / 6.0 + 0.1)
            sh.append(("poly", sec_ellipse(cx + 0.55 * r * _m.cos(a), cy + 0.55 * r * _m.sin(a), 0.1 * r + 0.05,
                                           0.1 * r + 0.05, 6), PLA_REED_HEAD, None, 0.1))
    elif key == "rush":                             # spiny tips across the ray ends
        for i in range(8):
            a = 2 * _m.pi * (i / 8.0)
            px, py = cx + 0.9 * r * _m.cos(a), cy + 0.9 * r * _m.sin(a)
            sh.append(("line", [(px - 0.2 * m * _m.sin(a), py + 0.2 * m * _m.cos(a)),
                                (px + 0.2 * m * _m.sin(a), py - 0.2 * m * _m.cos(a))], e, 0.05))
    elif key == "mint":                             # small round leaves
        for (px, py) in _pla_marks_in(cx, cy, 0.6 * r, 0.6 * r, 5, rnd):
            sh.append(("poly", sec_ellipse(px, py, 0.14 * r, 0.14 * r, 8), None, e, 0.05))
    # chaste, lavender, loosestrife: their accent flowers (in _pla_plan) already set them apart
    return sh
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
# v9 (round 5, G-R5-12): the item export (needs bergama_paths, grid, warn above)
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
    "p13.6": _r9(58, 42, 348, 54, "S", ("p15_season_winter",), series="p13", r8=487, est=250, rigid=True),
    "p13.17W": _r9(58, 96, 348, 3, "T", ("p15_animals_winter",), new=True),
    "p13.8": _r9(14, 101, 42, 57, "T", ("p15_col_spring",), new=True),
    "p13.9": _r9(58, 101, 348, 54, "S", ("p15_season_spring",), series="p13", r8=487, est=250, rigid=True),
    "p13.17S": _r9(58, 155, 348, 3, "T", ("p15_animals_spring",), new=True),
    "p13.11": _r9(14, 160, 42, 57, "T", ("p15_col_summer",), new=True),
    "p13.12": _r9(58, 160, 348, 54, "S", ("p15_season_summer",), series="p13", r8=487, est=250, rigid=True),
    "p13.17U": _r9(58, 214, 348, 3, "T", ("p15_animals_summer",), new=True),
    "p13.14": _r9(14, 219, 42, 57, "T", ("p15_col_autumn",), new=True),
    "p13.15": _r9(58, 219, 348, 54, "S", ("p15_season_autumn",), series="p13", r8=487, est=250, rigid=True),
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
#                  priority=1, group=None, fit=None, title=None, focus=None, frame=None, series=None)
#         round 9 (S6): focus (x0, y0, x1, y1) drawing units = the area an M map must show (the booklet fits it; the
#         extent is the context window around it, frames_r9 r9_window); frame = its R9_FRAMES key ("p07.1"; frame_mm
#         [w, h] is added when frames_r9 is included); series = the name its series shares (one scale, ADDENDUM §0.6)
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
#         width_pt, dash_pt, file); text = a string (made a legend text item) or a text id. Round 9 (S6): a swatch
#         may carry cat, rank (hue table r9) and badge (the bubble text); they are copied onto the entry too
#   round 9 (S1, G9-1; PLAN.md §spec S1, S6): bubbles and tags are booklet-drawn, their text centred by bk_centre:
#   ix.badge(page, b, drawing=None, at=None, priority=5, group=None, id=None) -> id
#         b = the S1 badge dict (marker_r9 mk_badge / an _MkText .badge: at, r_mm, fill, ring, ring_mm, text, pt,
#         bold, colour); at overrides b["at"] (drawing units). A text item role "badge" with those keys. A marker's
#         shapes passed to ix.layer become one badge item by themselves (the disc poly is kept, tagged badge_disc,
#         so a booklet that does not draw badges yet still shows it)
#   ix.tag(page, string, drawing=None, at=None, box_mm=None, fill=None, ring=None, ring_mm=0.0, size_pt=None,
#          bold=True, colour=None, priority=5, group=None, id=None) -> id     a plate / card head: role "tag"
#   ix_scale_token(item_id) -> u"{scale:<id>}"    a text, legend or list entry the booklet fills with that drawing's
#         printed scale label (ADDENDUM §0.7); sf_strip_widths leaves it as it is
#   ix.list(page, drawing, texts, numbered=True, anchors=None, id=None, group=None)   ordered text rows
#   ix.levels(page, drawing, levels, side="R", id=None, group=None)
#         levels = [(name, z_m)] (z on the drawing's y axis, m a.s.l. for sections); the booklet draws the level
#         markers (PLAN §3, Aras's sketch U04) and their "+43.71" values beside the drawing
#   ix.inset(page, parent, window, child, factor, id=None)   child = a drawing id of the zoom; window in parent units
#   (round 7 S1: ix.keymap removed, no callers; key maps come from common/keymap.py km_keymap + km_export_items)
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
                     proj_marks="annotations", proj_labels="labels", farms="fields", numbers="labels", chart="other",
                     base_fills="buildings", base_outlines="roads", structures="roads", paper="ground", frame="frame",
                     north="annotations")   # round 9 (A1 C7): the map / key-map layers that went to "other"
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
                 "badge", "source", "tag")                 # round 9 (S1): "tag" = plates, tags, card heads
IX_BADGE_KEYS = ("r_mm", "fill", "ring", "ring_mm", "text", "pt", "bold", "colour")   # round 9 (S1)


def ix_scale_token(item_id):
    """round 9 (S6, ADDENDUM §0.7): the token the booklet replaces with drawing item_id's printed scale label"""
    return u"{scale:%s}" % item_id


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
                priority=1, group=None, fit=None, title=None, focus=None, frame=None, series=None):
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
        if focus is not None:                              # round 9 (S6): the area an M map must show
            D["focus"] = [_ix_r(v) for v in focus]
        if frame is not None:                              # round 9 (S6): its R9_FRAMES key (+ the frame's mm)
            D["frame"] = u"%s" % frame
            wh = r9_wh(frame) if "r9_wh" in globals() else None
            if wh:
                D["frame_mm"] = [_ix_r(wh[0]), _ix_r(wh[1])]
        if series is not None:                             # round 9 (S6): one scale per series (ADDENDUM §0.6)
            D["series"] = u"%s" % series
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
            if getattr(s, "mk_badge", False):             # round 9 (S1): a marker's disc, also inside its badge
                sh["badge_disc"] = True
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
        b = getattr(s, "badge", None)
        if b:                                              # round 9 (S1): a marker's glyph -> ONE badge item
            self.badge(D["page"], b, drawing=D["id"], at=(o[0] + k * float(b["at"][0]), o[1] + k * float(b["at"][1])),
                       group=D.get("group"))
            return
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
             min_pt=None, box=None):
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
        if box:                                            # v45 (masterplan): a label box, e.g. dict(fill, alpha, stroke)
            it["box"] = dict(box)
        return it["id"]

    def badge(self, page, b, drawing=None, at=None, priority=5, group=None, id=None):
        """round 9 (S1): one bubble: a text item role "badge" carrying the S1 badge keys; the booklet draws the disc
        (fill, ring, ring_mm, r_mm) and centres the glyph on `at` with bk_centre"""
        p = at if at is not None else b.get("at")
        tid = self.text(page, b["text"], "badge", drawing=drawing, at=p, size_pt=b.get("pt"), bold=b.get("bold", True),
                        colour=b.get("colour"), positions=["=MC"], priority=priority, group=group, id=id)
        if tid is None:
            return None
        it = [x for x in self.d["pages"][page or "any"] if x["id"] == tid][-1]
        for k_ in IX_BADGE_KEYS:
            if k_ in b:
                it[k_] = _ix_r(b[k_]) if isinstance(b[k_], float) else b[k_]
        it["at"] = None if p is None else [_ix_r(p[0]), _ix_r(p[1])]
        return tid

    def tag(self, page, string, drawing=None, at=None, box_mm=None, fill=None, ring=None, ring_mm=0.0, size_pt=None,
            bold=True, colour=None, priority=5, group=None, id=None):
        """round 9 (S1): a plate / tag / card head: a text item role "tag" with box_mm [w, h] (None = the booklet
        sizes it to the text), fill, ring, ring_mm; the booklet draws the box and centres the text with bk_centre"""
        tid = self.text(page, string, "tag", drawing=drawing, at=at, size_pt=size_pt, bold=bold, colour=colour,
                        positions=["=MC"], priority=priority, group=group, id=id)
        if tid is None:
            return None
        it = [x for x in self.d["pages"][page or "any"] if x["id"] == tid][-1]
        it.update(box_mm=None if box_mm is None else [_ix_r(box_mm[0]), _ix_r(box_mm[1])], fill=fill, ring=ring,
                  ring_mm=_ix_r(ring_mm or 0.0))
        return tid

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
                e_ = dict(swatch=dict(sw), text=tid)
                for k_ in ("cat", "rank", "badge"):        # round 9 (S6): hue table category, rank, bubble text
                    if k_ in sw:
                        e_[k_] = sw[k_]
                ents.append(e_)
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
# v10 (round 6): common/hues.py (G6-6) and common/annot.py (G6-4) come in through basemap.py above (S1_done.md:
# "never include them again")

# v9: the Arial files font_metrics measures with (no PDF is written any more)
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


def text_w(s, size, bold=False):
    """v7 (round 4, G-R4-1): the width (mm) of s at size pt from the real Arial metrics (font_metrics.fm_width; the
    Helvetica estimate table is gone)"""
    return fm_width(s, size, bold)

PAGE_MARGINS = (14.0, 12.0, 14.0, 12.0)   # v7 (G-R4-1): (left, top, right, bottom) mm of the old sheet (the recorder's
                                          # TextPage answers "is this spot free" with them; nothing is checked here)
CL_LOG = []                           # v7: this run's map_draw / key-map lines (printed in the log)
TRIG_WHY = [None]                     # v7: what started this run (trig_should_run), printed in the log
CL_SCALES = list(globals().get("SF_SCALES") or R28_SCALES)   # v9: the Bergama scale list (PLAN §3 SF_SCALES)
CL_IX = [None]                        # v9: this run's item export (Ix)
CL_ITEMS_LOG = []                     # v9: one line per exported drawing / key map


class Page:
    """v9 (round 5 S9, G-R5-12; replaces the sheet Page and write_pdf): the same drawing calls as the round 4 sheet
    Page (rect / poly / path / line / text / keep / free / tgroup), but nothing is written: every shape is RECORDED
    as a common shape tuple in page mm, y up (("poly", rings, fill, stroke, lw, dash, None, alpha), ("line", pts,
    colour, lw, dash, cap), ("text", s, x, y, size_mm, colour, bold, align, role)); cl_drawing() turns a box of it
    into one item drawing. A TextPage still answers "is this spot free" so markers and names start where v8.2 put
    them; it is never checked here and nothing raises (the booklet's layout check reports hits as warnings)."""
    def __init__(self, w=420.0, h=297.0, name=None):
        self.w, self.h, self.shapes = w, h, []
        self.tp = TextPage(name or u"record", (0.0, 0.0, w, h), y_down=False, pad=0.6, margins=PAGE_MARGINS)
        self.tg = None                            # the open text group (lines of one word block may touch)
        self.grp = None                           # v10 (G6-9): the open element group (kind, element id)
        self.grps = []                            # v10: the group of each recorded shape (same index as shapes)
        self.grp_n = {}                           # v10: element counter per kind (auto ids "<kind> <n>")
        self.anc = {}                             # v11 (L7): shape index -> (ax, ay, positions) of an anchored name
        self.bdg = {}                             # v13 (round 9 S1, c1): text index -> the marker's S1 badge dict
        self.bdisc = set()                        # v13: shape indices of marker discs (exported badge_disc)
        self.tagd = {}                            # v13 (S1): text index -> dict(box_mm, centre) of a chip's text (tag)
    def group(self, kind, eid=None):
        """v10 (round 6, G6-9, PLAN §2.9): `with pg.group(kind, eid):` every shape recorded inside is one element
        of that kind (kinds as common/item_export.py: trees, buildings, people, plants, water, ground, roads,
        paths, fields, heritage, hubs, annotations, cuts, levels, labels, legend, keymap, frame, other); eid None =
        the next number of that kind. Nested calls: the inner one wins; the outer comes back after it."""
        pg_ = self

        class _G(object):
            def __enter__(s_):
                s_.prev = pg_.grp
                n_ = pg_.grp_n[kind] = pg_.grp_n.get(kind, 0) + 1
                pg_.grp = (kind, eid if eid is not None else u"%s %d" % (kind, n_))
                return pg_.grp
            def __exit__(s_, *a_):
                pg_.grp = s_.prev
                return False
        return _G()
    def _rec(self, sh):
        self.shapes.append(sh)
        self.grps.append(self.grp)
    def tgroup(self, start=True):
        """v7: start (or with False end) one text group: the runs of one line / lines of one paragraph"""
        self.tg = self.tp._group() if start else None
        return self.tg
    def keep(self, geom, kind="keep", name=None, line=None):
        """v7: an obstacle no text may touch (a box, an area or a line, page mm)"""
        return self.tp.keep(geom, kind, name, line)
    def free(self, box, allow=()):
        """v7: True when box (page mm) is clear of every text and keep (bar allow) and inside the margins"""
        return self.tp._free(box, allow)
    def rect(self, x, y, w, h, fill=None, stroke=None, lw=0.2):
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill, stroke, lw, True)
    def poly(self, P, fill=None, stroke=None, lw=0.2, closed=False, dash=None):
        self.path([P], fill, stroke, lw, closed, dash)
    def path(self, rings, fill=None, stroke=None, lw=0.2, closed=True, dash=None, mul=False, cap=1, alpha=None):
        """several rings in one path (a fill is even-odd, so holes stay open); alpha = the fill's opacity (v9: the
        D9 tint keeps its colour and opacity, so the houses read through; v8.2 multiplied it in the PDF)"""
        rs = [[(float(p[0]), float(p[1])) for p in R] for R in rings if len(R) >= 2]
        if not rs:
            return
        rf = [R for R in rs if len(R) >= 3]
        if fill and rf:
            one = bool(stroke) and closed
            self._rec(("poly", rf, fill, stroke if one else None, lw if one else 0.0,
                       tuple(dash) if (one and dash) else None, None, alpha))
            if one:
                return
        if stroke:
            for R in rs:
                Q = R + [R[0]] if closed and len(R) >= 3 else R
                self._rec(("line", Q, stroke, lw, tuple(dash) if dash else None, cap))
    def line(self, P, col, lw=0.25, dash=None, mul=False, cap=1): self.path([P], None, col, lw, False, dash, mul, cap)
    def text(self, s, x, y, size, col="4A3F35", bold=False, align="L", name=None, allow=(), role="label"):
        """one line of text, size pt, baseline (x, y), align L / C / R; registered in the TextPage (real box) and
        recorded with its role ("marker" = a glyph on its own disc: exported as a badge)"""
        if not s or not s.strip():
            return
        self.tp.put(s, x, y, size, bold, align, 0.0, name, role, col, allow, self.tg, emit=False)
        self._rec(("text", s, float(x), float(y), size * IX_PT, col, bool(bold), align or "L", role))


def cl_clip_ring(R, b):
    """v9: ring R cut to the box b (x0, y0, x1, y1) (Sutherland-Hodgman); [] when nothing is left"""
    out = [tuple(p[:2]) for p in R]
    for edge in range(4):
        if not out:
            return []
        inp, out = out, []

        def ins(p):
            return (p[0] >= b[0], p[1] >= b[1], p[0] <= b[2], p[1] <= b[3])[edge]

        def cut(p, q):
            if edge in (0, 2):
                x = b[0] if edge == 0 else b[2]
                t = (x - p[0]) / ((q[0] - p[0]) or 1e-12)
                return (x, p[1] + t * (q[1] - p[1]))
            y = b[1] if edge == 1 else b[3]
            t = (y - p[1]) / ((q[1] - p[1]) or 1e-12)
            return (p[0] + t * (q[0] - p[0]), y)
        for i in range(len(inp)):
            p, q = inp[i - 1], inp[i]
            if ins(q):
                if not ins(p):
                    out.append(cut(p, q))
                out.append(q)
            elif ins(p):
                out.append(cut(p, q))
    return out if len(out) >= 3 else []


def cl_bbox(pg, pad=0.8):
    """v9: the box (page mm) of everything recorded on pg (texts by their real Arial width), pad mm round it: the
    extent of a scale-free diagram"""
    xs, ys = [], []
    for s_ in pg.shapes:
        if s_[0] == "poly":
            for R in s_[1]:
                xs += [p[0] for p in R]
                ys += [p[1] for p in R]
        elif s_[0] == "line":
            xs += [p[0] for p in s_[1]]
            ys += [p[1] for p in s_[1]]
        elif s_[0] == "text":
            w_ = text_w(s_[1], s_[4] / IX_PT, s_[6])
            xa = s_[2] - (w_ if s_[7] == "R" else (w_ / 2.0 if s_[7] == "C" else 0.0))
            xs += [xa, xa + w_]
            ys += [s_[3] - 0.25 * s_[4], s_[3] + 0.8 * s_[4]]
    if not xs:
        return (0.0, 0.0, 1.0, 1.0)
    return (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)


CL_COMPASS = ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]


def cl_north_deg(f):
    """v9: where true north points in a drawing on the site frame's axes, in degrees counter-clockwise from the
    drawing's +y (the key-map module's north_deg convention; the frame's u axis runs at f["ang"] from survey +x)"""
    return round(-math.degrees(f["ang"]), 2)


def cl_drawing(ix, did, page, pg, box, den=None, origin_m=(0.0, 0.0), dkind="diagram", north_deg=None, group=None,
               priority=5, title=None, layer=None, focus=None, frame=None, fixed_text=False):
    """v9 (round 5 S9, G-R5-12; the idea of the masterplan's mpx_drawing): ONE item drawing from the part box (x0, y0,
    x1, y1 page mm) of the recorder pg. den given: a true-scale drawing in m (x_d = origin_m + (x_mm - x0) x den /
    1000, the site frame's axes for the maps), scale_pref = the Bergama list (the booklet picks one); den None: a
    scale-free diagram in mm (extent = the box size) with a fit range whose lower end keeps its smallest word at
    >= 4 pt. Shapes are cut to the box; each recorded text inside the box becomes an anchored label (first position
    = exactly where it was recorded, then the 8 compass spots), a marker glyph a badge (only its own spot); texts
    outside the box are left out and counted. Returns the drawing dict.
    v13 (round 9 S1 / S6, c1, d4): a marker glyph recorded by cl_marker goes out as ONE badge item (ix.badge, its
    disc poly tagged badge_disc), a cl_tag chip text as ONE tag item (ix.tag, box_mm, its box stays geometry);
    focus (drawing units) and frame (R9_FRAMES key) ride on the drawing (Ix.drawing); fixed_text=True gives every
    text only its own spot (the p09 cards: the booklet must not move a card's lines onto each other)."""
    x0, y0, x1, y1 = [float(v) for v in box]
    bdg = dict((id(pg.shapes[i_]), b_) for i_, b_ in (getattr(pg, "bdg", None) or {}).items() if i_ < len(pg.shapes))
    bds = set(id(pg.shapes[i_]) for i_ in (getattr(pg, "bdisc", None) or ()) if i_ < len(pg.shapes))
    tgd = dict((id(pg.shapes[i_]), d_) for i_, d_ in (getattr(pg, "tagd", None) or {}).items() if i_ < len(pg.shapes))
    anc = getattr(pg, "anc", None) or {}
    aid = dict((id(pg.shapes[i_]), a_) for i_, a_ in anc.items() if i_ < len(pg.shapes))
    inb = lambda x_, y_: x0 - 0.01 <= x_ <= x1 + 0.01 and y0 - 0.01 <= y_ <= y1 + 0.01
    # v11 (L7): an anchored name belongs to the drawing its ANCHOR is in (wherever it was recorded)
    texts = [s_ for s_ in pg.shapes if s_[0] == "text" and
             (inb(*aid[id(s_)][:2]) if id(s_) in aid else inb(s_[2], s_[3]))]
    n_out = sum(1 for s_ in pg.shapes if s_[0] == "text") - len(texts)
    if den:
        k = float(den) / 1000.0
        ext = (origin_m[0], origin_m[1], origin_m[0] + (x1 - x0) * k, origin_m[1] + (y1 - y0) * k)
        D = ix.drawing(did, page, ext, scale_pref=CL_SCALES, units="m", dkind=dkind, north_deg=north_deg,
                       scale_bar=True, priority=priority, group=group or did, title=title, focus=focus, frame=frame)
        org = (origin_m[0] - x0 * k, origin_m[1] - y0 * k)
    else:
        k = 1.0
        pts = [s_[4] / IX_PT for s_ in texts]
        lo = max(0.5, 4.0 / min(pts)) if pts else 0.5        # D1: no word under 4 pt after the booklet's fit
        D = ix.drawing(did, page, (0.0, 0.0, x1 - x0, y1 - y0), units="mm", dkind=dkind, scale_bar=False,
                       priority=priority, group=group or did, title=title, fit=(math.ceil(lo * 100.0) / 100.0, 2.0),
                       frame=frame)
        org = (-x0, -y0)
    shapes, runs = [], []                                 # v10 (G6-9): runs of shapes of one element group, in order
    gs = list(getattr(pg, "grps", None) or [])
    gs += [None] * (len(pg.shapes) - len(gs))
    for s_, g_ in zip(pg.shapes, gs):
        out_ = []
        if s_[0] == "poly":
            rs = [r for r in (cl_clip_ring(R, (x0, y0, x1, y1)) for R in s_[1]) if len(r) >= 3]
            if rs:
                if id(s_) in bds:                         # v13 (S1): a marker's disc, also inside its badge item
                    d_ = _MkDisc(("poly", rs) + tuple(s_[2:]))
                    d_.mk_badge = True
                    out_.append(d_)
                else:
                    out_.append(("poly", rs) + tuple(s_[2:]))
        elif s_[0] == "line":
            for _f, Q in clip_runs(s_[1], (x0, y0, x1, y1)):
                if len(Q) >= 2:
                    out_.append(("line", Q) + tuple(s_[2:]))
        if out_:
            shapes += out_
            g_ = g_ or ("other", None)
            if runs and runs[-1][0] == g_:
                runs[-1][1].extend(out_)
            else:
                runs.append((g_, out_))
    tg = dict((id(s_), g_) for s_, g_ in zip(pg.shapes, gs))
    n_un = 0
    for g_, sh_ in runs:                                  # one layer per element run, tagged through ix_group
        with cl_ix_group(g_[0], g_[1]):
            ix.layer(D, layer or dkind, sh_, k=k, origin=org)
        n_un += len(sh_) if g_[1] is None else 0
    n_bdg = n_tag = 0
    for s_ in texts:
        al = s_[7] if s_[7] in ("L", "C", "R") else "L"
        badge = s_[8] == "marker"
        g_ = tg.get(id(s_)) or ("labels", None)
        a_ = aid.get(id(s_))
        if id(s_) in bdg:                                 # v13 (S1, c1): the marker's glyph -> ONE badge item
            with cl_ix_group(g_[0], g_[1]):
                ix.badge(page, mk_badge_at(bdg[id(s_)], k, org), drawing=D["id"], group=D["group"], priority=2)
            n_bdg += 1
            continue
        if id(s_) in tgd:                                 # v13 (S1): a chip's text -> ONE tag item, centred
            t_ = tgd[id(s_)]
            with cl_ix_group(g_[0], g_[1]):
                ix.tag(page, s_[1], drawing=D["id"], at=(org[0] + k * t_["at"][0], org[1] + k * t_["at"][1]),
                       box_mm=t_["box_mm"], fill=None, size_pt=s_[4] / IX_PT, bold=s_[6], colour=s_[5],
                       group=D["group"], priority=3)
            n_tag += 1
            continue
        if a_ and not badge:                              # v11 (L7): anchored on its point, the booklet picks the spot
            at_, pos_ = (org[0] + k * a_[0], org[1] + k * a_[1]), list(a_[2]) or CL_COMPASS
        else:
            at_, pos_ = (org[0] + k * s_[2], org[1] + k * s_[3]), ["=" + al] + ([] if (badge or fixed_text) else
                                                                                CL_COMPASS)
        with cl_ix_group(g_[0], g_[1]):
            ix.text(page, s_[1], "badge" if badge else "label", drawing=D["id"],
                    at=at_, size_pt=s_[4] / IX_PT, bold=s_[6], colour=s_[5],
                    positions=pos_, group=D["group"], priority=2 if badge else 5)
    kinds = set(g_[0] for g_, _s in runs) | set((tg.get(id(s_)) or ("labels",))[0] for s_ in texts)
    CL_GROUPS.setdefault(page, [0, set(), 0])
    CL_GROUPS[page][0] += len(runs) + len(texts)
    CL_GROUPS[page][1] |= kinds
    CL_GROUPS[page][2] += n_un
    CL_ITEMS_LOG.append(u"items %s %s: %d shapes, %d labels (%d badges, %d tags)%s%s" % (
        page, D["id"], len(shapes), len(texts), n_bdg, n_tag, (u" · drawn at 1:%s, %.0f x %.0f m" % (fmt(den), ext[2] - ext[0],
                                                                                   ext[3] - ext[1])) if den else
        u" · mm %.0f x %.0f" % (x1 - x0, y1 - y0), (u" · %d text(s) of other boxes" % n_out) if n_out else u""))
    return D


CL_GROUPS = {}                           # v10 (G6-9): page -> [elements, kinds, untagged shapes] for the groups line


class _ClNoGroup(object):
    def __enter__(self):
        return None
    def __exit__(self, *a_):
        return False


def cl_ix_group(kind, eid):
    """v10 (round 6, G6-9): the shared item_export context `ix_group(kind, eid)` (PLAN §2.8, S2) around one export
    call, so every primitive it writes carries grp "<kind>/<element id>"; eid None = untagged, kind "other" (the
    booklet then logs one WARNING per drawing). Without ix_group in this build (S2 not merged yet) nothing is
    tagged and the groups line says so."""
    f_ = globals().get("ix_group")
    if f_ is None:
        return _ClNoGroup()
    return f_(kind, eid) if eid is not None else f_("other", None)


def cl_groups_log():
    """v10 (G6-9): `groups <page> kinds=<n> elements=<n> untagged=<n>` per page (PLAN §2.9)"""
    out = []
    for page, (n_, ks, un) in sorted(CL_GROUPS.items()):
        out.append(u"groups %s kinds=%d elements=%d untagged=%d%s" % (
            page, len(ks), n_, un, u"" if "ix_group" in globals() else u" · FLAG ix_group missing: not tagged"))
    return out


CL_SW_BOX = (6.0, 2.6)                   # v9: the legend sample's box (mm), as v8.2's legend rows drew it


def cl_sw(draw):
    """v9: a legend sample of v8.2 (draw(pg, box), e.g. sw_fill / sw_line / sw_mark) -> an Ix legend swatch dict:
    the sample is drawn into a small recorder and read back: only lines -> "line" / "dash"; with a marker glyph ->
    "dot" (+ "label" = the glyph); else "fill" (its first fill colour). The full sample rides along as "shapes"
    (schema shape dicts in swatch mm, y up from its lower-left corner) so the booklet can draw it true."""
    W, H = CL_SW_BOX
    pg = Page(60.0, 40.0, u"swatch")
    b = (20.0, 20.0, 20.0 + W, 20.0 + H)
    try:
        draw(pg, b)
    except Exception as ex:
        wn_warn(None, "legend", u"a legend sample was not drawn (%s: %s)" % (type(ex).__name__, ex))
        return dict(kind="fill", colour=None)
    ix = CL_IX[0]
    sh = [s_ for s_ in pg.shapes if s_[0] != "text"]
    tx = [s_ for s_ in pg.shapes if s_[0] == "text"]
    shapes = [d_ for d_ in (ix._shape(s_, 1.0, (-b[0], -b[1])) for s_ in sh) if d_ is not None] if ix else []
    for d_ in shapes:
        d_.pop("_stripes", None)
    polys = [s_ for s_ in sh if s_[0] == "poly"]
    lines = [s_ for s_ in sh if s_[0] == "line"]
    if lines and not polys:
        L_ = lines[0]
        out = dict(kind="dash" if L_[4] else "line", colour=L_[2], width_pt=round((L_[3] or 0.25) / IX_PT, 3),
                   dash_pt=[round(v / IX_PT, 3) for v in L_[4]] if L_[4] else None)
    else:
        f_ = next((p_ for p_ in polys if p_[2]), None)
        out = dict(kind="dot" if tx else "fill", colour=f_[2] if f_ else None, stroke=next(
            (p_[3] for p_ in polys if p_[3]), None))
    if tx:
        out["label"] = u"".join(t_[1] for t_ in tx)
    bd_ = [b_ for _i, b_ in sorted((getattr(pg, "bdg", None) or {}).items())]
    if bd_:                                               # v13 (round 9 c3, S6): a marker sample = a bubble: the
        out["badge"] = bd_[0]["text"]                     # booklet draws disc + number with bk_centre
        out["bubble"] = dict((k_, bd_[0][k_]) for k_ in IX_BADGE_KEYS if k_ in bd_[0])
    elif tx and polys:                                    # v13 (S1): a letter chip sample (grows-from W/E/A/H)
        f_ = next((p_ for p_ in polys if p_[2]), None)
        out["tag"] = dict(text=out["label"], fill=f_[2] if f_ else None, colour=tx[0][5], pt=round(tx[0][4] / IX_PT, 2),
                          bold=bool(tx[0][6]))
    out["shapes"] = shapes
    out["box_mm"] = [W, H]
    return out


# ------------------------------------------------------------------ live numbers
def _load(paths):
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
            return d, time.strftime("%d %b %H:%M", time.localtime(os.path.getmtime(p)))
        except Exception:
            pass
    return None, None

def bed_depth():
    """"1.0-2.3 m": the bed below the banks over the survey cuts, from the site board's results (v40); "" if absent."""
    d, _ = _load(BD_FILES)
    try:
        a, b = float(d["bed_below_banks_min_m"]), float(d["bed_below_banks_max_m"])
        return "%.1f-%.1f m" % (a, b) if b > a else "%.1f m" % a
    except Exception:
        return ""


def live():
    """farm lands from the water balance results; walking potential on the spine from the site board"""
    d, t = _load(WB_FILES)
    lands = (d or {}).get("lands") or {}       # v5 (M10): no typed fallback
    wb_src = ("water balance results of " + t) if d else "FLAG: water balance results not found: p.09's farm areas and p.08's stream row are left out"
    mv_path = bg_result(*MV_FILE)              # v9 (C10, CHK01B §D2): the vote of THIS run's site board file
    mv, t2 = _load([mv_path])
    mv_src = ("site board movement of " + t2) if mv else "run the site board once to compute the walking potential"
    votes, vote_src, sides = spine_votes(mv, mv_src)     # v6.2: common/city_spine.py (the masterplan votes the same way)
    mv_fresh, mv_when = bg_this_run(mv_path)
    if mv and not mv_fresh:                    # the board's vote file is older than this chain's Button press
        wn_warn("p09", "stale", u"the spine's bank vote reads the site board's city_link_movement.json %s, older than "
                u"this chain's Button press (the site board did not write it in this run): %s" % (mv_when, mv_path))
    # v1.8 (FIGURE_CONFLICTS.md §2): the spine length = the masterplan's drawn pieces (edge + deck + over), read live;
    # none printed when the masterplan has not run (was a typed "about 660 m", the K4-K5 chainage)
    mp_path = bg_result(*MP_FILE)              # v9 (C10): the corridor the plans inherit from the masterplan
    mp, t3 = _load([mp_path])
    mp_fresh, mp_when = bg_this_run(mp_path)
    if not mp_fresh:
        wn_warn("p09", "stale", u"the corridor (spine, hub squares, road changes) from masterplan_results.json is not "
                u"from this chain run (%s): %s" % (mp_when, mp_path))
    try:
        spine_m = sum(float(v) for v in mp["options"]["A"]["spine_m"].values())
    except Exception:
        spine_m = None
    mp_src = ("masterplan results of " + t3) if spine_m else ""
    try:                                       # v5 (p.09): the masterplan's streamside walks over the whole project
        walks = [[tuple(p) for p in w_["P"]] for w_ in mp["options"]["A"]["walks"] if len(w_.get("P") or []) >= 2]
    except Exception:
        walks = []
    try:                                       # v6 (p.09 hub plans): the spine on the real edge, piece by piece
        mp_spine = [(s_.get("kind", "edge"), [tuple(p) for p in s_["P"]]) for s_ in mp["options"]["A"]["spine"]
                    if len(s_.get("P") or []) >= 2]
    except Exception:
        mp_spine = []
    # v2: page 1's plan context and page 2's walking radius from the site board (v46+), each with a flagged fallback
    ctx, t4 = _load(CTX_FILES)
    ctx_src = ("Context: site board city_context.json of %s (survey buildings, typed as the sections' building types; "
               "OSM streets by highway class; survey water; bridges K1-K6, s62; OSM shop points, same tags as the "
               "shop counts)" % t4) if ctx else ""
    fw, t5 = _load(FW_FILES)                   # v4: the site board's half of the framework (busiest streets, spines)
    mpmv = (mp or {}).get("movement") if isinstance((mp or {}).get("movement"), dict) else None
    return dict(lands=lands, wb_src=wb_src, mv=mv, mv_src=mv_src, votes=votes, vote_src=vote_src, sides=sides,
                spine_m=spine_m, mp_src=mp_src, walks=walks, mp_spine=mp_spine,
                mp_when=u"corridor from the masterplan: %s (%s)" % (mp_path, mp_when),     # v9 (C10): logged
                mv_when=u"bank vote from the site board: %s (%s)" % (mv_path, mv_when),
                river_month=(d or {}).get("river_month_m3"),     # v5 (p.08 calendar): the stream's mean monthly flow
                ctx=ctx, ctx_src=ctx_src, fw=fw, mpmv=mpmv,
                hub_sq=[h_ for h_ in ((mp or {}).get("hub_squares") or []) if isinstance(h_, dict)],   # v7 (P10.6)
                fw_note=("framework: site board of %s" % t5) if fw else
                "FLAG: no movement_framework.json (run the site board v51+): p.08 shows the main spine as the shop street",
                mp_note=("" if mpmv else "FLAG: no masterplan movement (masterplan_results.json): p09's hub plans have "
                         "no road changes, crossings, sub-hubs or bus line") +
                ("" if (mp or {}).get("hub_squares") else "\nFLAG: no hub_squares in masterplan_results.json (run the "
                 "masterplan v38 once): p09's plans have no hub squares"),
                ctx_note=("plan context: site board of " + t4) if ctx else
                "FLAG: no city_context.json (run the site board v46 first): page 1's plan has no context and its shops "
                "cover only the old central window; page 2's reach uses 800 m")

def fmt(v): return "{:,.0f}".format(v)

# v10 (round 6, G6-6, PLAN §2.6 PUB "people groups by headcount"): one hue, darker = more people (visitors 433,000 >
# residents 11,002 > students 1,825-1,925, who_rows); was CC9A52 / 8B3A3F / 5C7A86, a hue each
GROUP = dict(L=("Locals", hue("PUB", 2)), T=("Visitors", hue("PUB", 1)), S=("Students", hue("PUB", 3)))   # v4: T = visitors
GROWS = dict(W="water", E="stream edge", A="agriculture", H="heritage")
GROW_C = dict(W=hue("WAT", 2), E=hue("WAT", 3), A=hue("AGR", 2), H=hue("HER", 2))   # v1.6 letter chips; v10: G6-6 table
SPINE_C = hue("MOV", 1)                  # v10 (G6-6): the streamside spine = movement r1 (was BC6F45)
SOFT = ((1.0, 0.36), (0.6, 0.18), (0.28, 0.0))   # v2: a soft band: (width share, paler by) of its three strokes
REACH_RIM = 1.2                           # v3 (MIRAQUA 28 Oct, P10.1): mm of the reach rim showing above and below the
                                          # page 2 stream band (the reach classes of R28_REACH, drawn under the band)
# v3 (MIRAQUA 28 Oct, G11 / F13): crops and plants by their printed names, "English (Turkish)" as the shared table
# common/plant_photos.py PLANTS (maize prints "Corn (Mısır)"); keys as the water balance writes them
CROP_NAME = {"cotton": u"Cotton (Pamuk)", "maize": u"Corn (Mısır)", "corn": u"Corn (Mısır)",
             "tomato": u"Tomato (Domates)", "olive": u"Olive (Zeytin)"}
PLANE_NAME = u"Oriental plane (Doğu çınarı)"


SRC_KEY = []                         # v1.6: the sources this page cites (v9: in order of their first mark)
PAGE_SRC = {}                        # v9: page id ("p08", "p09") -> its sources (ix.source rows, cl_items)


def cite(src):
    """v1.6 (water board v1.6 method): a source mark. v9 (round 5, G-R5-12): "{src:<key>}" (CL_SRC_KEY), which the
    booklet turns into its Sources page number; the source goes into this page's list (ix.source in cl_items)."""
    if not src or src in CITE_OFF or src not in PUB_SRC:   # v3 (F5) + v4 (D13): public sources only get a mark
        return ""
    if src not in SRC_KEY:
        SRC_KEY.append(src)
    return "{src:%s}" % CL_SRC_KEY[src]


def fit(pg, s, x, y, size, w, col, bold=False, align="L"):
    """v1.6: one line of keywords, shrunk until it fits w mm; v1.11: never below 7 pt (labels >= 7 pt at A3)"""
    while text_w(s, size, bold) > w and size > 7.0:
        size = max(7.0, size - 0.25)
    pg.text(s, x, y, size, col, bold, align)


def cl_wrap(s, size, w, bold=False):
    """v6 (P09.2): the words of s in lines no wider than w mm at size pt (a single longer word keeps its own line).
    v7 (G-R4-2, P08.3): no widow: a one-word last line takes the last word(s) of the line above while that line keeps
    at least two words (logged when it cannot)"""
    out, cur = [], ""
    for wd in s.split():
        t_ = (cur + " " + wd) if cur else wd
        if cur and text_w(t_, size, bold) > w:
            out.append(cur)
            cur = wd
        else:
            cur = t_
    out += [cur] if cur else []
    if len(out) > 1 and len(out[-1].split()) < 2:
        a_ = out[-2].split()
        if len(a_) >= 3:
            out[-2], out[-1] = u" ".join(a_[:-1]), a_[-1] + u" " + out[-1]
        else:
            BM_NOTE.append(u"FLAG widow kept (too few words to move): %s" % s[:60])
    return out


def cl_para(pg, s, x, y, size, w, col, bold=False, lead=None):
    """v6 (P09.2): s wrapped to w mm from baseline y down, line pitch lead (default 1.25 x the type size); returns the
    baseline under the last line (where the next text starts), so nothing is set on a fixed pitch"""
    lead = lead or 1.25 * size * 0.3528
    pg.tgroup()                                           # v7: the lines of one paragraph form one text group
    for ln in cl_wrap(s.strip(), size, w, bold):
        pg.text(ln, x, y, size, col, bold)
        y -= lead
    pg.tgroup(False)
    return y


def cl_marker(pg, cx, cy, s, col, size_pt=7.0, r_min=None, style="solid", name=None, allow=()):
    """v7 (round 4, G-R4-7): the shared marker (common/marker.py mk_marker: the glyph centred on its visible ink box,
    the circle sized to the glyph, colour = the element it names) drawn on pg: the disc first (a keep no other text
    may touch), then the glyph through pg.text (it may sit on its own disc and on the keeps in allow, e.g. its map).
    Returns (outer box, radius)."""
    shapes, box, r_ = mk_marker(cx, cy, s, col, size_pt, r_min, style)
    MK_N[0] += 1
    nm = name or u"marker %d" % MK_N[0]
    for sh in shapes:
        if sh[0] == "poly":
            n0 = len(pg.shapes)
            pg.poly(list(sh[1]), fill=sh[2] or None, stroke=sh[3] or None, lw=sh[4] or 0.2, closed=True)
            pg.bdisc.update(range(n0, len(pg.shapes)))   # v13 (S1, c1): exported as badge_disc
            pg.keep(sh[1], "marker", nm)
    for sh in shapes:
        if sh[0] == "text":
            n0 = len(pg.shapes)
            pg.text(sh[1], sh[2], sh[3], size_pt, sh[5], True, "L", name=nm, allow=(nm,) + tuple(allow),
                    role="marker")
            if len(pg.shapes) > n0 and getattr(sh, "badge", None):
                pg.bdg[len(pg.shapes) - 1] = dict(sh.badge)   # v13 (S1, c1): kept for cl_drawing's ix.badge
    return box, r_


def cl_tag(pg, s, x, y, w, h, fill, col, size_pt=7.0, bold=True):
    """v13 (round 9 S1, G9-1; H4 §1c): a chip / tile: the box (x, y lower-left, w x h page mm) filled, its text
    recorded at the box's centre on the ink box (as cl_text_mm "MC") and marked as a tag, so cl_drawing exports
    it as ONE tag item (box_mm, centre) that the booklet centres with bk_centre; the box stays geometry"""
    pg.rect(x, y, w, h, fill=fill)
    ix0, iy0, ix1, iy1 = fm_ink_box(s, size_pt, bold)
    cx, cy = x + w / 2.0, y + h / 2.0
    n0 = len(pg.shapes)
    pg.text(s, cx - (ix0 + ix1) / 2.0, cy - (iy0 + iy1) / 2.0, size_pt, col, bold, "L")
    if len(pg.shapes) > n0:
        pg.tagd[len(pg.shapes) - 1] = dict(box_mm=[w, h], at=[cx, cy])


def cl_marker_free(pg, cx, cy, s, col, size_pt=7.0, frame=None, allow=(), name=None, lead=False, rings=(2.2, 3.2, 4.4),
                   on_point=True):
    """v7 (G-R4-7, no marker on a marker): a marker on its point (cx, cy) when its box is free there (on_point=False:
    never on it, e.g. beside a key map's frame), else the
    nearest free spot round it (rings x its radius, 8 directions, inside frame) with a hairline from the point to
    the disc; on its point anyway when nothing is free (the collision test then names it). Returns (box, centre)."""
    _s, box0, r_ = mk_marker(cx, cy, s, col, size_pt)
    cand = ([(cx, cy)] if on_point else []) + [(cx + f_ * r_ * math.cos(a_ * math.pi / 4.0), cy + f_ * r_ * math.sin(a_ * math.pi / 4.0))
                         for f_ in rings for a_ in (0, 2, 4, 6, 1, 3, 5, 7)]
    for q in cand:
        b = (q[0] - (box0[2] - cx), q[1] - (box0[3] - cy), q[0] + (box0[2] - cx), q[1] + (box0[3] - cy))
        if frame and not (frame[0] <= b[0] and b[2] <= frame[2] and frame[1] <= b[1] and b[3] <= frame[3]):
            continue
        if pg.free(b, allow):
            break
    else:
        q = (cx, cy)
    if lead and math.hypot(q[0] - cx, q[1] - cy) > r_ + 0.3:
        d_ = math.hypot(q[0] - cx, q[1] - cy)
        pg.line([(cx, cy), (q[0] - (q[0] - cx) / d_ * r_, q[1] - (q[1] - cy) / d_ * r_)], col, 0.15)
    box, _r = cl_marker(pg, q[0], q[1], s, col, size_pt, name=name, allow=allow)
    return box, q


def cl_place(pg, s, at, size, col, bold=False, r=0.8, frame=None, allow=(), positions=TP_POSITIONS):
    """v11 (L7, Aras 4 Nov 19:18 "scripts just produce ... booklet ... places them"): a name of a point or line at
    (at) on a map, handed to the booklet as an ANCHORED label: anchor = at, positions = the compass codes round it;
    the booklet's pl_label finds the spot (move, short form, number + side list, smaller), so no name is ever left
    out here and no free-spot test is made. Recorded at the first compass spot inside frame (else the first one),
    only so the item has a size. Returns its box (always)."""
    tp = pg.tp
    got = None
    for code in positions:
        x, y, al = tp._at(code, s, at, size, bold, r + 0.8)
        b = tp._box(s, x, y, size, bold, al, 0.0)
        if got is None:
            got = (x, y, al, b)
        if not frame or (frame[0] <= b[0] and b[2] <= frame[2] and frame[1] <= b[1] and b[3] <= frame[3]):
            got = (x, y, al, b)
            break
    x, y, al, b = got
    n0 = len(pg.shapes)
    pg.text(s, x, y, size, col, bold, al, allow=allow)
    if len(pg.shapes) > n0:
        pg.anc[len(pg.shapes) - 1] = (float(at[0]), float(at[1]), list(positions))
        CL_HANDED[0] += 1
    return b


CL_HANDED = [0]                          # v11 (L7): names handed to the booklet as anchored labels


def sw_fill(col, edge=None):
    """v5: a legend sample (cl_legend / key_flow "draw"): a filled patch"""
    return lambda pg, b: pg.rect(b[0], b[1], b[2] - b[0], b[3] - b[1], fill=col, stroke=edge, lw=0.15)


def sw_line(col, lw, dash=None, arrow=False):
    """v5: a legend sample: a line across the swatch (with an arrowhead for a flow)"""
    def f_(pg, b):
        ym = (b[1] + b[3]) / 2.0
        pg.line([(b[0], ym), (b[2] - (1.4 if arrow else 0.0), ym)], col, lw, dash=dash)
        if arrow:
            arrow_head(pg, (b[0], ym), (b[2] + 0.4, ym), col, 1.9)
    return f_


def sw_mark(fn):
    """v5: a legend sample: fn(pg, x, y) drawn at the swatch's centre"""
    return lambda pg, b: fn(pg, (b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0)


def disc(pg, x, y, r, fill=None, stroke=None, lw=0.2):
    pg.poly([(x + r * math.cos(a * math.pi / 12), y + r * math.sin(a * math.pi / 12)) for a in range(24)],
            fill=fill, stroke=stroke, lw=lw, closed=True)


def icon(pg, kind, x, y, sz):
    """v1.6 (after water board v1.7 icon()): a pictogram in the square (x, y - sz)-(x + sz, y), drawn on a 10 x 10
    grid. Graphic only."""
    if kind in ICO_OF:                                   # v4 (02 §2): the shared icon set where it has the symbol
        put_shapes(pg, ico_draw(ICO_OF[kind], x + sz / 2.0, y - sz / 2.0, sz))
        return
    u = sz / 10.0
    lw = 0.07 * sz
    ink, ink2, wat, wd, acc, st, pap = C["ink"], C["ink2"], C["water"], C["water_deep"], C["accent"], C["structure"], C["white"]

    def P(pts):
        return [(x + a * u, y - sz + b * u) for a, b in pts]

    def R(a0, b0, a1, b1, fill=None, stroke=None):
        pg.poly(P([(a0, b0), (a1, b0), (a1, b1), (a0, b1)]), fill=fill, stroke=stroke, lw=lw, closed=True)

    def D(a, b, r, fill=None, stroke=None):
        disc(pg, x + a * u, y - sz + b * u, r * u, fill, stroke, lw)

    def person(a, col):
        D(a, 8.0, 1.25, col)
        pg.poly(P([(a - 1.6, 0.6), (a - 1.6, 5.4), (a - 0.9, 6.4), (a + 0.9, 6.4), (a + 1.6, 5.4), (a + 1.6, 0.6)]),
                fill=col, closed=True)

    def X(a0, b0, a1, b1):
        pg.line(P([(a0, b0), (a1, b1)]), acc, lw * 1.4)
        pg.line(P([(a0, b1), (a1, b0)]), acc, lw * 1.4)

    if kind == "road":                                   # the road crosses the water once
        R(0, 3.6, 10, 6.4, wat)
        R(3.6, 0, 6.4, 10, ink2)
        for b in (0.8, 3.0, 5.2, 7.4):
            pg.line(P([(5, b), (5, b + 1.2)]), C["white"], lw * 0.6)
    elif kind == "front":                                # buildings turn their backs to the water
        R(0, 0.4, 10, 2.6, wat)
        for a in (0.4, 3.6, 6.8):
            R(a, 4.0, a + 2.8, 8.6, pap, ink)
        X(7.0, 0.2, 9.8, 3.2)
    elif kind == "bank":                                 # the bank cut off from the city
        R(0, 0.4, 4.2, 2.6, wat)
        R(4.2, 0.4, 5.4, 7.0, ink2)
        R(5.4, 5.8, 10, 7.0, st)
        X(6.2, 1.2, 9.4, 4.4)
    elif kind == "deep":                                 # the bed deep between walls
        pg.poly(P([(0, 9), (2.6, 9), (2.6, 1.2), (7.4, 1.2), (7.4, 9), (10, 9), (10, 0), (0, 0)]), fill=st, closed=True)
        R(2.6, 1.2, 7.4, 2.4, wat)
        pg.line(P([(5, 8.6), (5, 3.0)]), ink, lw)
        pg.poly(P([(4.2, 3.9), (5, 2.6), (5.8, 3.9)]), fill=ink, closed=True)
    elif kind == "flood":                                # a cut with two flood levels
        pg.poly(P([(0, 8), (2, 8), (3.4, 1.0), (6.6, 1.0), (8, 8), (10, 8), (10, 0), (0, 0)]), fill=st, closed=True)
        pg.poly(P([(2.3, 6.5), (3.4, 1.0), (6.6, 1.0), (7.7, 6.5)]), fill=wat, closed=True)
        pg.line(P([(1.2, 7.4), (8.8, 7.4)]), wd, lw, dash=(0.8 * u, 0.6 * u))
    elif kind == "sewage":                               # a pipe dripping into the water
        R(0, 0.4, 10, 2.6, wat)
        R(0, 6.0, 5.6, 8.2, ink2)
        R(5.0, 5.6, 6.0, 8.6, ink)
        D(6.6, 4.0, 0.65, "7A6448")
        D(7.4, 3.0, 0.5, "7A6448")
    elif kind == "arch":                                 # a Roman arch
        R(0.6, 0.4, 9.4, 1.2, ink2)
        pg.poly(P([(1.2, 1.2), (1.2, 7.0), (2.4, 8.8), (5, 9.6), (7.6, 8.8), (8.8, 7.0), (8.8, 1.2), (6.8, 1.2),
                   (6.8, 5.6), (5, 7.2), (3.2, 5.6), (3.2, 1.2)]), fill=acc, closed=True)
    elif kind in ("visitor", "resident", "student", "walker"):
        person(4.0, ink)
        if kind == "visitor":                            # a camera
            R(6.4, 4.0, 9.8, 6.4, ink2)
            D(8.1, 5.2, 0.7, C["white"])
        elif kind == "resident":                         # a house
            R(6.4, 0.6, 9.6, 3.8, pap, ink)
            pg.poly(P([(6.0, 3.6), (8.0, 5.8), (10.0, 3.6)]), fill=ink2, closed=True)
        elif kind == "student":                          # a cap
            pg.poly(P([(1.6, 9.2), (4.0, 10.0), (6.4, 9.2), (4.0, 8.4)]), fill=wd, closed=True)
            R(7.0, 1.0, 9.8, 4.6, pap, ink)
        else:                                            # no count
            pg.text("?", x + 8.0 * u, y - sz + 1.0 * u, 9.0 * u / 0.3528 * 0.8, acc, True, "C")
    elif kind == "bed":                                  # a bed
        R(0.6, 3.0, 9.4, 5.0, st)
        R(0.6, 5.0, 3.4, 6.8, pap, ink)
        R(0.6, 1.0, 1.4, 8.0, ink)
        R(8.6, 1.0, 9.4, 5.0, ink)
    elif kind == "stall":                                # a market stall
        pg.poly(P([(0.4, 6.0), (1.6, 9.0), (8.4, 9.0), (9.6, 6.0)]), fill=acc, closed=True)
        R(1.2, 0.4, 2.0, 6.0, ink)
        R(8.0, 0.4, 8.8, 6.0, ink)
        R(1.2, 3.0, 8.8, 4.0, ink2)
    elif kind == "hide":                                 # a stretched hide
        pg.poly(P([(2, 1), (1, 3), (2, 5), (1, 7), (2.4, 9.2), (5, 8.4), (7.6, 9.2), (9, 7), (8, 5), (9, 3), (8, 1),
                   (5, 1.8)]), fill="A0784F", closed=True)
    elif kind == "slot":                                 # a square with a slot onto the water below
        R(0, 4.0, 10, 9.0, st)
        R(3.0, 5.8, 7.0, 7.2, wat)
        R(0, 0.4, 10, 2.6, wat)
        pg.line(P([(5, 5.4), (5, 3.0)]), ink, lw)
    elif kind == "olive":                                # an olive tree
        R(4.5, 0.4, 5.5, 4.4, ink2)
        D(5.0, 6.2, 3.4, C["green_mid"])
        for a, b in ((3.8, 6.8), (6.0, 5.4), (5.4, 7.8)):
            D(a, b, 0.5, ink)
    elif kind == "bench":                                # a shaded seat
        D(5.0, 7.6, 2.4, C["green_mid"])
        R(4.6, 3.4, 5.4, 5.4, ink2)
        R(1.0, 2.6, 9.0, 3.4, ink)
        R(1.6, 0.4, 2.4, 2.6, ink)
        R(7.6, 0.4, 8.4, 2.6, ink)
    elif kind == "reed":                                 # reeds in a basin
        R(0, 0, 10, 2.2, wat)
        for k_ in range(5):
            a = 1.6 + k_ * 1.7
            t = 6.6 + (k_ % 2) * 2.2
            pg.line(P([(a, 0.8), (a + 0.3, t)]), C["green_deep"], lw)
            R(a - 0.25, t - 1.8, a + 0.85, t + 0.2, C["field"])
    elif kind == "calendar":                             # a calendar page, Jul-Sep marked
        R(0.6, 0.6, 9.4, 8.6, pap, ink)
        R(0.6, 7.0, 9.4, 8.6, ink2)
        for i in range(12):
            a, b = 1.3 + (i % 4) * 2.0, 5.0 - (i // 4) * 2.0
            R(a, b, a + 1.4, b + 1.3, acc if i in (6, 7, 8) else C["faint"])
    elif kind == "nofix":                                # no post fixed in the bed
        R(0, 0.4, 10, 2.6, wat)
        R(4.4, 1.6, 5.6, 8.0, ink2)
        X(2.0, 2.0, 8.0, 8.6)
    elif kind == "stamp":                                # an approval stamp
        D(5.0, 5.0, 4.2, None, wd)
        pg.line(P([(2.8, 5.2), (4.4, 3.4), (7.4, 6.8)]), wd, lw * 1.4)
    elif kind == "crest":                                # occupied floors above the crest line
        R(2.4, 4.0, 7.6, 8.0, pap, ink)
        pg.poly(P([(2.0, 7.8), (5.0, 9.8), (8.0, 7.8)]), fill=ink2, closed=True)
        pg.line(P([(0, 2.6), (10, 2.6)]), wd, lw, dash=(0.8 * u, 0.6 * u))
        pg.line(P([(9.0, 2.8), (9.0, 3.8)]), ink, lw * 0.7)
    elif kind == "car":                                  # v4 (R29): a car, the framework's driving mode
        pg.poly(P([(0.6, 2.0), (9.4, 2.0), (9.4, 4.6), (7.4, 4.8), (6.0, 7.2), (3.0, 7.2), (1.8, 4.8), (0.6, 4.6)]),
                fill=wd, closed=True)
        D(2.8, 1.8, 1.2, ink)
        D(7.2, 1.8, 1.2, ink)
    elif kind == "bus":                                  # v1.11: a bus (the existing stops of the hubs)
        R(0.6, 1.8, 9.4, 9.2, wd)
        R(1.4, 5.4, 8.6, 8.2, C["white"])
        D(2.6, 1.6, 1.1, ink)
        D(7.4, 1.6, 1.1, ink)
    elif kind == "plane":                                # v1.11: a plane tree, broad crown (D8)
        R(4.4, 0, 5.6, 4.4, ink2)
        D(2.9, 6.2, 2.5, C["green_mid"])
        D(7.1, 6.2, 2.5, C["green_mid"])
        D(5.0, 7.4, 2.6, C["green_deep"])
    elif kind == "farm":                                 # a field fed by water
        pg.poly(P([(0, 0.6), (6.8, 0.6), (10, 5.4), (3.2, 5.4)]), fill=C["field"], closed=True)
        R(1.0, 7.0, 6.4, 8.6, wat)
        pg.line(P([(6.4, 7.8), (9.2, 7.8)]), wd, lw)
        pg.poly(P([(8.6, 8.6), (9.8, 7.8), (8.6, 7.0)]), fill=wd, closed=True)

def group_dots(pg, x, y, who, r=1.3):
    for i, k in enumerate("LTS"):
        cx = x + i * (2 * r + 1.0)
        ring = [(cx + r * math.cos(a * math.pi / 8), y + r * math.sin(a * math.pi / 8)) for a in range(16)]
        pg.poly(ring, fill=GROUP[k][1] if k in who else C["white"], stroke=GROUP[k][1], lw=0.25, closed=True)

def shop_figures():
    """v1.7: the page 1 shop figures from the counts above. Covered reach = the 100 m bins whose middle lies between
    CH cov0 and cov1 (the covered 200 m: 700-900 m); per 100 buildings = the open stream's 0-30 m band, as chart B."""
    bins = [n for c, n in SHOPS_PER_100M if CH["cov0"] <= c + 50 <= CH["cov1"]]
    cov = sum(bins)
    tot = sum(n for c, n in SHOPS_PER_100M)
    nb, ns = OPEN_BAND[0]
    return dict(covered_reach=cov, by_stream=tot, covered_pct=int(round(100.0 * cov / tot)), covered_of="%d of %d" % (cov, tot),
                covered_reach_m=100 * len(bins), open_0_30m_buildings=nb, open_0_30m_shops=ns,
                open_0_30m_per_100_buildings=int(round(100.0 * ns / nb)))

# ------------------------------------------------------------------ v1.11: layout numbers (the sheet and its booklet crops)
# v1.11 (Aras 27 Oct 11:07 "looks scattered"): page 1 reads top left to bottom right in numbered panels: (1) the plan,
# large, the focal point; (2) and (3) the two charts that prove it, stacked beside it; (4) seven reasons as pictogram
# tiles; (5) who comes and (6) walking potential, the smallest, at the bottom. White page, no source footer.
# v2 (Aras 27 Oct 17:34, booklet Prompt 3): the plan is the whole site frame at 1:10,000 on the frame's own axes (one
# scale, frame and north with the site board's movement maps), a band across the top with its key beside it; the two
# charts side by side under it.
PLAN_DEN = 10000                         # v2: 1:10,000, x and y alike; v4: the framework diagram (FW_MAP)
CTX_FILES = [os.path.join(bg_cache("selinus_board"), "city_context.json")]   # v2: written by selinus_board v46+
SITE_FRAME = [(29388.015, 32540.503), (31220.325, 30364.153), (31625.069, 30704.915), (29792.759, 32881.264)]  # = the
# site board's SITE_FRAME_LK (site_alan): the plan's frame when the context file is missing
ROAD_CLS = {"main": (0.45, C["ink2"], None, "main road"), "secondary": (0.3, C["ink2"], None, "secondary road"),
            "lane": (0.15, C["structure"], None, "lane"), "path": (0.15, C["structure"], (0.6, 0.5), "footway")}
ROAD_ORDER = ("main", "secondary", "lane", "path")          # v2: streets by OSM class (the board's MV_CLASS), light
HOME_TYPES = [("old town", "old town house"), ("planned low-rise", "planned low-rise house"),
              ("apartment block", "apartment block"), ("small / shack", "small house / shack"),
              ("shop below", "shop below, home above"), ("other", "other building")]   # the sections' building types
PLAN_BOX = {}                            # v2: the plan's rectangle as drawn (v9: p08's map box, page mm)
# v4: P1_MAP, P1_KEY, P1_A, P1_B, P1_WHO, P1_WALK are gone with the shops plan, the charts, who comes and walking
# potential (page 1 is the framework: FW_MAP, WHO_BOX, P1_TILES further down)
# v5 (revision 30 Oct 2026, p.09): page 2 = the whole study area on one map across the top (its legend beside it, scale
# bar and north arrow under it), the five bridge places as cards under it with the same badges as on the map (no
# leaders), then the flood rule, which bank and the producers' market along the bottom
# v6 (round 3, D1, P09.1): the overview map is p.08's; page 2 zooms into each bridge place: a row of plans at one
# scale in stream order (hub_plan_layout), each hub's card under its plan(s), the key under the cards
# v7 (round 4, P10.1-P10.4, spec S5): key map at the left of the plan row, plans 70 mm high, then their legend, then the
# hub cards in five columns, then the three bottom panels 8 mm lower than before
# v9 (round 5 S9): no sheet: P2_PLAN / P2_PLAN_W only set the scale the windows are recorded at (hub_plan_layout);
# the other numbers place each block on its own recorder (the booklet lays the page out); P2_KEY, P2_TITLE_Y,
# P2_LEG_TOP, P2_CARD_WT (cards now one width), P2_CARD_BOT and P2_PLAN_MIN_W are gone
P2_PLAN = (74.0, 251.0, 70.0, 4.0)       # page 2 hub plans: x, top y, height, gap between plans (mm)
P2_PLAN_W = 332.0                        # the row's width (x 74-406)
P2_PLAN_MARGIN = 20.0                    # m round a window's points (a drawing rule, not data)
# v10 (round 6, BRIEF §6 row 9 U16 U17, PLAN §3 P-10): ONE page 9 = SON page9 as base + page10's plan row. The frames
# (plan_findings/frames_p09-13.md new page 9, % of the A3 page -> mm, 1 % x = 4.2 mm, 1 % y = 2.97 mm): spine map
# [3,13 48x12]; each plan above its hub card's column, the five columns 18.2 % wide with 0.5 % gaps (SON page9 card
# columns x 3.3 / 22.0 / 40.8 / 59.6 / 78.4), plans 15.8 % high; the bottom band y 74-92.5: flood rule [3,76 46x17],
# which bank [51,74 29x18], market [82,74 15x18]. Drawing rules for the recorders; the booklet places by frame.
P9_MAP = (201.6, 35.6)                   # mm: the spine map's frame (w, h)
P9_COL_W = 76.4                          # mm: one hub column (card and its plan(s))
P9_COL_GAP = 2.0                         # mm: between two columns, and between the transit hub's two plans
P9_PLAN_H = 46.9                         # mm: the plans' height
P9_FLOOD = (193.2, 50.5)                 # mm: the flood rule's frame (w, h)
CL_HEAD_MM = 5.0                         # v13 (round 9 d5): a C frame's heading row (7 pt heading + 2 mm gap), mm;
                                         # the chart below it is drawn at frame w x (h - CL_HEAD_MM) (design value)
SK_SOIL = "CDBF9F"                       # v10 (SKETCH language, BRIEF §3, r06_S02): flat beige soil (f93d84b SKETCH_SRC SOIL)
SK_LINE = ("2C2219", 0.9)                # thick black ground line: the text ink 2C2219 (PLAN §2.6 ANN), mm
P2_CARD_GAP = 6.0                        # page 2: gutter between the hub cards
P2_LOW = 76.0                            # page 2: the title line of the three bottom panels
P2_FLOOD = (14.0, 64.0, 19.0)            # page 2 flood rule: x, first (highest) level's y, row step
P2_BANK = (216.0, 65.0, 12.0)            # page 2 which bank: x, first row y, row step
SPINE_SIMPLIFY_M = 2.5                   # v7 (P10.5): the spine line simplified to this (m) and runs under
SPINE_MIN_M = 8.0                        # this long in a plan dropped (no stubs): drawing rules, not data
SQ_EDGE = hue("PUB", 2)                  # v7 (P10.6): the hub square's edge; v10 (G6-6): public life r2 (was 9C7440)
SQ_FILL = hue("PUB", 3)                  # v10 (G6-6): the hub square's fill, public life r3 (was the D9 slate tint),
SQ_ALPHA = 0.35                          # transparent (alpha <= 0.35, PLAN §5 U28): the houses read through
P2_MARKET = grid_x(11)                   # page 2 producers' market: x (M1 column 11)
# v3 (MIRAQUA 28 Oct, G8): the study area on page 1's plan: calisma_alan of Bergama_Altlik.3dm (25 Oct 08:25, survey
# m), two parts worked as one, the recorded copy the site board (R28_STUDY_COPY) and masterplan (CALISMA_COPY) keep
CL_STUDY = [
    [(29696.903, 32800.562), (29872.423, 32572.84), (29880.693, 32496.334), (29818.865, 32475.301), (29825.821, 32398.074), (29923.185, 32344.348), (29904.985, 32311.252), (29997.056, 32290.092), (30053.417, 32139.667), (30004.049, 32108.006), (29954.803, 32210.611), (29792.114, 32247.062), (29761.684, 32302.735), (29754.016, 32451.383), (29678.437, 32447.696), (29632.398, 32496.591), (29665.339, 32526.253), (29612.859, 32696.506), (29600.496, 32719.394)],
    [(30178.18, 31923.887), (30138.072, 31887.655), (30257.694, 31773.217), (30389.686, 31405.252), (30701.152, 30991.252), (30840.053, 31053.865), (31044.852, 30781.877), (31014.2, 30757.409), (31373.442, 30493.066), (31453.175, 30560.194), (31332.978, 30864.179), (31012.679, 31323.349), (30737.856, 31286.66), (30712.87, 31331.891), (30556.09, 31450.103), (30454.629, 31577.301), (30434.156, 31607.332), (30313.613, 31812.92)],
]

def stream_ref():
    """v1.9: (points, covered flag per segment) of the masterplan's stream reference line (STREAM_REF). v4: unpacked
    once per run (the two maps and the spine line all read it)."""
    if not _SREF:
        R_ = json.loads(zlib.decompress(base64.b64decode("".join(STREAM_REF))).decode("utf-8"))
        _SREF.append(([tuple(p) for p in R_["P"]], [bool(c) for c in R_["covered"]]))
    return _SREF[0]


_SREF = []


def clip_seg(a, b, win):
    """v1.9: the part of segment a-b inside win (x0, y0, x1, y1), or None (Liang-Barsky)."""
    t0, t1 = 0.0, 1.0
    dx, dy = b[0] - a[0], b[1] - a[1]
    for p_, q_ in ((-dx, a[0] - win[0]), (dx, win[2] - a[0]), (-dy, a[1] - win[1]), (dy, win[3] - a[1])):
        if p_ == 0:
            if q_ < 0:
                return None
            continue
        r_ = q_ / p_
        if p_ < 0:
            t0 = max(t0, r_)
        else:
            t1 = min(t1, r_)
        if t0 > t1:
            return None
    return (a[0] + t0 * dx, a[1] + t0 * dy), (a[0] + t1 * dx, a[1] + t1 * dy)


def clip_runs(P, win, flags=None):
    """v1.9: the polyline P cut to win as runs [(flag, points)]; a new run starts where it leaves win or the flag
    changes."""
    runs = []
    for i, (a, b) in enumerate(zip(P, P[1:])):
        cs = clip_seg(a, b, win)
        if cs is None:
            continue
        f_ = flags[i] if flags else None
        if runs and runs[-1][0] == f_ and math.hypot(runs[-1][1][-1][0] - cs[0][0], runs[-1][1][-1][1] - cs[0][1]) < 1e-6:
            runs[-1][1].append(cs[1])
        else:
            runs.append((f_, [cs[0], cs[1]]))
    return runs



def site_frame(ctx):
    """v2: the site frame's axes (cx, cy, ang, u0, v0, w, h; survey m): the site board's (city_context.json), else
    from SITE_FRAME as the board computes it (the angle of its longest side, its centre)."""
    f = (ctx or {}).get("frame")
    if f:
        return f
    P = SITE_FRAME
    cx, cy = sum(p[0] for p in P) / 4.0, sum(p[1] for p in P) / 4.0
    i = max(range(4), key=lambda j: math.hypot(P[(j + 1) % 4][0] - P[j][0], P[(j + 1) % 4][1] - P[j][1]))
    ang = math.atan2(P[(i + 1) % 4][1] - P[i][1], P[(i + 1) % 4][0] - P[i][0])
    while ang > math.pi / 2:
        ang -= math.pi
    while ang <= -math.pi / 2:
        ang += math.pi
    c, s = math.cos(-ang), math.sin(-ang)
    L_ = [(c * (x - cx) - s * (y - cy), s * (x - cx) + c * (y - cy)) for x, y in P]
    u0, v0 = min(q[0] for q in L_), min(q[1] for q in L_)
    return dict(cx=cx, cy=cy, ang=ang, u0=u0, v0=v0, w=max(q[0] for q in L_) - u0, h=max(q[1] for q in L_) - v0)


def tint_hex(h, t):
    """v2: hex colour h faded t of the way to white"""
    return "".join("%02X" % int(round(int(h[i:i + 2], 16) + (255 - int(h[i:i + 2], 16)) * t)) for i in (0, 2, 4))


def cl_text_mm(pg, s, q, size_mm, hx, bold=False, align="L", allow=()):
    """v7: a text item of the shared modules (basemap / keymap format: size in mm, align L / C / R / MC) through
    pg.text (so it is registered); "MC" = q is the middle of the ink"""
    pt = size_mm / 0.3528
    if align == "MC":
        ix0, iy0, ix1, iy1 = fm_ink_box(s, pt, bold)
        pg.text(s, q[0] - (ix0 + ix1) / 2.0, q[1] - (iy0 + iy1) / 2.0, pt, hx, bold, "L", allow=allow)
    else:
        pg.text(s, q[0], q[1], pt, hx, bold, align if align in ("L", "C", "R") else "L", allow=allow)


CL_LAYER_KIND = dict(base_ground="ground", base_contours="ground", base_fills="buildings", base_water="water",
                     base_outlines="buildings", base_names="labels", water="water", structures="paths",
                     proj_tint="ground", proj_water="water", proj_lines="paths", proj_vegetation="trees",
                     study="annotations", proj_marks="hubs", proj_labels="labels")   # v10 (G6-9): map layer -> kind


def cl_kind_of(layer, hx):
    """v10 (round 6, G6-9): the element kind of one base / project map shape: by its colour where the base map names
    it (houses, heritage, streets, green, fields, water), else by its map layer (CL_LAYER_KIND)"""
    h_ = str(hx or u"").upper()
    for tab in (BM_COL, BM_FAINT, BM_MUTED, BM_KEY):
        for k_, v_ in tab.items():
            if isinstance(v_, str) and v_.upper() == h_:
                for key_, kind_ in (("her", "heritage"), ("bld", "buildings"), ("road", "roads"), ("water", "water"),
                                    ("tree", "trees"), ("wood", "trees"), ("park", "plants"), ("grass", "plants"),
                                    ("shrub", "plants"), ("field", "fields"), ("farm", "fields"), ("agri", "fields"),
                                    ("orchard", "fields"), ("contour", "ground"), ("name", "labels")):
                    if k_.startswith(key_):
                        return kind_
    return CL_LAYER_KIND.get(layer, "other")


def cl_draw_fns(pg, allow=()):
    """v7 (G-R4-4): (fill_fn, line_fn, text_fn, order_fn) for basemap_draw / map_draw on this sheet's page: a
    colour's alpha = faded towards the white page; the D9 tint layer ("proj_tint") is laid over the base by
    multiplying (transparent: the houses read through, U52); nonzero fills ring by ring (even-odd would open white
    notches where rings overlap, CHK-3); texts through pg.text (registered; allow = the map they may sit on)"""
    st = dict(layer=None)

    def col(hx, alpha):
        return tint_hex(hx, 1.0 - (1.0 if alpha is None else max(0.0, min(1.0, float(alpha)))))

    def fill_fn(rings, hx, alpha, nonzero):
        rs = [R_ for R_ in rings if len(R_) >= 3]
        tint = st["layer"] == "proj_tint"                 # v9: the tint keeps its colour and opacity (no multiply)
        for grp in ([[R_] for R_ in rs] if nonzero else [rs]):
            if grp:
                with pg.group(cl_kind_of(st["layer"], hx)):   # v10 (G6-9): each fill its own element
                    if tint:
                        pg.path(grp, fill=hx, alpha=1.0 if alpha is None else float(alpha))
                    else:
                        pg.path(grp, fill=col(hx, alpha))

    def line_fn(pts, hx, w_mm, dash_mm, alpha):
        if len(pts) >= 2:
            d_ = (tuple(dash_mm) if isinstance(dash_mm, (list, tuple)) else (dash_mm, dash_mm)) if dash_mm else None
            with pg.group(cl_kind_of(st["layer"], hx)):
                pg.line(pts, col(hx, alpha), w_mm, dash=d_)

    def text_fn(s_, q, size_mm, hx, bold, align):
        with pg.group("labels"):
            if st["layer"] in ("structures", "base_names"):   # v13 (round 9 Q9, g1): a base name (street, mahalle,
                nm_ = place_label(s_) or s_               # stream, bridge, place) in the table's spelling, handed to
                n0 = len(pg.shapes)                       # the booklet ANCHORED on its point (v11 L7: never left out)
                cl_text_mm(pg, nm_, q, size_mm, hx, bold, "MC", allow)
                if len(pg.shapes) > n0:
                    pg.anc[len(pg.shapes) - 1] = (float(q[0]), float(q[1]), ["=MC"] + CL_COMPASS)
                    CL_HANDED[0] += 1
            else:
                cl_text_mm(pg, s_, q, size_mm, hx, bold, align, allow)

    def order_fn(layer):
        st["layer"] = layer
    return fill_fn, line_fn, text_fn, order_fn


def cl_study():
    """v7 (G-R4-4): the study area rings (survey m): the basemap's (sc_rings), else the recorded copy CL_STUDY"""
    try:
        R_ = sc_rings()
    except Exception:
        R_ = []
    return R_ or [[tuple(p) for p in R] for R in CL_STUDY]


CL_LAST_BASE = [[]]                      # v13 (round 9): the base items of the last cl_map call (context log, legend)


def cl_map(pg, page, T, sbox, den, project, base_extra=(), clip=True, allow=(), legend_cols=None, water_ok=None,
           ring=None):
    """v7 (G-R4-4; replaces bm_draw): one map through THE draw order (map_draw): the muted base of the box sbox
    (survey m) at 1:den (ml_base: light houses with closed outlines, streets, the stream) + base_extra (e.g. the
    covered course), then project {layer: items} (proj_tint multiplied, proj_lines, proj_vegetation, proj_marks),
    the study line, clipped to the study area when clip. The caller clips the PDF to its window and draws markers
    and labels after it (they are the top layers). Returns (n base items, the study rings).
    v9 (round 5, G-R5-8): the stream is drawn above the tints (map_draw's "water" layer); legend_cols (the legend's
    fill colours) and water_ok (fills in the water by design) go to map_draw for its zones line.
    v13 (round 9 G9-4, A1 C2, cause b2): ml_base's default mode "context" (layers a-j); ring = the map's window as a
    survey-m ring (frame_ring of r9_window), which the unmapped ground fills and the base is cut to; the base's own
    covered course is left out when base_extra draws ours (one dashed line, the legend's); base names go to the
    booklet anchored (cl_draw_fns). The base items are kept in CL_LAST_BASE[0] for basemap_context_log and
    basemap_legend_rows."""
    try:
        base = ml_base(sbox, den, ring=ring)
        if base_extra:
            base = [it for it in base if not (getattr(it, "ctx", None) == "f" and getattr(it, "cls", None) == "covered")]
    except Exception as ex_:
        BM_NOTE.append("basemap not read: %s: %s" % (type(ex_).__name__, ex_))
        base = []
    if not base:
        BM_NOTE.append("FLAG: no basemap data (run the site board v59 once): the maps draw only the study area")
    BM_NOTE.extend(basemap_warnings())
    CL_LAST_BASE[0] = list(base)
    study = cl_study()
    fill_fn, line_fn, text_fn, order_fn = cl_draw_fns(pg, allow)
    map_draw(page, T, fill_fn, line_fn, text_fn, list(base) + list(base_extra), project, study=study, clip=clip,
             order_fn=order_fn, log=CL_LOG, legend_cols=legend_cols, water_ok=water_ok)
    return len(base), study


# ------------------------------------------------------------------ v4: the shared basemap, the spine line, pictograms
BM_NOTE = []                             # v4: basemap / hand-off notes for the log


def frame_T(f, ox, oy, den, u0=None, v0=None):
    """v4: survey m -> page mm on the site frame's own axes (the north of every movement map), 1:den, the point
    (u0, v0) of the frame's local axes (default its lower-left corner) at (ox, oy)"""
    k = 1000.0 / den
    c, s = math.cos(-f["ang"]), math.sin(-f["ang"])
    u0 = f["u0"] if u0 is None else u0
    v0 = f["v0"] if v0 is None else v0
    return lambda p: (ox + (c * (p[0] - f["cx"]) - s * (p[1] - f["cy"]) - u0) * k,
                      oy + (s * (p[0] - f["cx"]) + c * (p[1] - f["cy"]) - v0) * k)


def frame_uv(f, p):
    c, s = math.cos(-f["ang"]), math.sin(-f["ang"])
    return (c * (p[0] - f["cx"]) - s * (p[1] - f["cy"]), s * (p[0] - f["cx"]) + c * (p[1] - f["cy"]))


def frame_box(f, u0, v0, u1, v1):
    """the survey bounding box of the frame-axes window (u0, v0)-(u1, v1): the basemap's cull box"""
    c, s = math.cos(f["ang"]), math.sin(f["ang"])
    P = [(f["cx"] + c * u - s * v, f["cy"] + s * u + c * v) for u in (u0, u1) for v in (v0, v1)]
    return (min(p[0] for p in P), min(p[1] for p in P), max(p[0] for p in P), max(p[1] for p in P))


def frame_ring(f, u0, v0, u1, v1):
    """v13 (round 9): the frame-axes window (u0, v0)-(u1, v1) as a survey-m ring (the basemap's window, ml_base ring)"""
    c, s = math.cos(f["ang"]), math.sin(f["ang"])
    return [(f["cx"] + c * u - s * v, f["cy"] + s * u + c * v) for u, v in ((u0, v0), (u1, v0), (u1, v1), (u0, v1))]


CL_FOCUS_PAD = 30.0                      # m round the study area and the hubs: v12's p09 rule (drawing rule, not data)


def cl_focus(f, hubs, extra=(), pad=CL_FOCUS_PAD):
    """v13 (round 9 ADDENDUM §0.1, cause d4): an M map's content box on the site frame's axes (m): the study area,
    the hubs (and extra survey points), pad m round them; the context fills the rest of the frame"""
    uv = [frame_uv(f, p) for R in cl_study() for p in R] + [frame_uv(f, hb["xy"]) for hb in hubs] + \
         [frame_uv(f, p) for p in extra]
    return (min(q[0] for q in uv) - pad, min(q[1] for q in uv) - pad, max(q[0] for q in uv) + pad,
            max(q[1] for q in uv) + pad)


def cl_r9_scale(f, key, focus):
    """v13 (round 9 ADDENDUM §0, PLAN §cause d4): the scale and context window of an M map for frame key (R9_FRAMES):
    Tfit of the focus box in the frame, the label rule (r9_label, R8's true scale from the frame row), den = the true
    scale T the map is drawn at, win = r9_window (frame axes, m), ring / sbox = the same window in survey m"""
    fr = r9_frame(key) or {}
    Tfit = r9_tfit(focus, key)
    lab = r9_label(Tfit, fr.get("r8"))
    win = r9_window(focus, key)
    return dict(Tfit=Tfit, lab=lab, den=float(lab["T"]), win=win, ring=frame_ring(f, *win),
                sbox=frame_box(f, *win), key=key)


def pl_offset(Q, d):
    """the polyline Q moved d to its left (survey m or page mm)"""
    out, n = [], len(Q)
    for i in range(n):
        a, b = Q[max(0, i - 1)], Q[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1.0
        out.append((Q[i][0] - dy / ln * d, Q[i][1] + dx / ln * d))
    return out


def ref_chain():
    """v6: (points, cumulative chainage m) of the stream reference line (STREAM_REF), in its own direction"""
    P, _c = stream_ref()
    cum = [0.0]
    for a, b in zip(P, P[1:]):
        cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    return P, cum


def ref_s(P, cum, q):
    """v6 (was spine_line's own): the chainage on P (cum) of the point of P nearest q (survey m)"""
    best = None
    for i, (a, b) in enumerate(zip(P, P[1:])):
        dx, dy = b[0] - a[0], b[1] - a[1]
        l2 = dx * dx + dy * dy or 1e-9
        t = max(0.0, min(1.0, ((q[0] - a[0]) * dx + (q[1] - a[1]) * dy) / l2))
        d = math.hypot(a[0] + dx * t - q[0], a[1] + dy * t - q[1])
        if best is None or d < best[0]:
            best = (d, cum[i] + t * (cum[i + 1] - cum[i]))
    return best[1]


def ref_at(P, cum, s):
    """v6 (was spine_line's own): the point at chainage s on P (cum)"""
    for i in range(1, len(P)):
        if cum[i] >= s:
            t = (s - cum[i - 1]) / max(cum[i] - cum[i - 1], 1e-9)
            return (P[i - 1][0] + (P[i][0] - P[i - 1][0]) * t, P[i - 1][1] + (P[i][1] - P[i - 1][1]) * t)
    return P[-1]


def spine_line(L):
    """v4: the streamside spine as a line (survey m): the masterplan's stream reference line (STREAM_REF) from K4 to
    K5, each piece of SPINE moved its offset_m to the bank the vote picked (L["sides"]; NE = the left of the
    downstream direction), piece B on the stream over the covered reach. [(piece id, points)] upstream first; once
    per run (L["spine_line"])."""
    if L.get("spine_line") is not None:
        return L["spine_line"]
    P, cum = ref_chain()
    flip = ref_s(P, cum, SPINE[0]["frm"]) > ref_s(P, cum, SPINE[-1]["to"])
    if flip:                                              # the reference line runs downstream from K4 here
        P = P[::-1]
        cum = [cum[-1] - c_ for c_ in cum[::-1]]
    out = []
    for pc in SPINE:
        s0, s1 = ref_s(P, cum, pc["frm"]), ref_s(P, cum, pc["to"])
        if s1 < s0:
            s0, s1 = s1, s0
        Q = [ref_at(P, cum, s0)] + [P[i] for i in range(len(P)) if s0 < cum[i] < s1] + [ref_at(P, cum, s1)]
        bank = L["sides"].get(pc["id"], "over")
        d = float(pc.get("offset_m") or 0.0) * (1.0 if bank == "NE" else (-1.0 if bank == "SW" else 0.0))
        out.append((pc["id"], pl_offset(Q, d) if d else Q))
    L["spine_line"] = out
    return out


def corridor_line(L):
    """v6 (round 3, P08.1, D1: the project arrow runs the whole corridor): the project corridor as a line (survey m):
    the stream reference line (STREAM_REF) between the upstream and the downstream end of the study area
    (calisma_alan: basemap_study(), else the recorded copy CL_STUDY), the ends = the lowest and highest chainage of
    the study area's corners projected onto the line; upstream first (K4 before K5). dict(P, s0, s1, m) once per run
    (L["corridor"]), None when no study area is known."""
    if "corridor" in L:
        return L["corridor"]
    try:
        study = basemap_study()
    except Exception:
        study = []
    study = study or [[tuple(p) for p in R] for R in CL_STUDY]
    P, cum = ref_chain()
    ss = [ref_s(P, cum, p) for R in study for p in R]
    if not ss:
        L["corridor"] = None
        return None
    s0, s1 = min(ss), max(ss)
    Q = [ref_at(P, cum, s0)] + [P[i] for i in range(len(P)) if s0 < cum[i] < s1] + [ref_at(P, cum, s1)]
    if ref_s(P, cum, HUB_PTS["K4"]) > ref_s(P, cum, HUB_PTS["K5"]):
        Q = Q[::-1]                                       # the line runs upstream here: turn it round
    L["corridor"] = dict(P=Q, s0=s0, s1=s1, m=s1 - s0)
    BM_NOTE.append("p.08 corridor: the project arrow runs %d m along the stream (study area from chainage %d to %d m "
                   "of the stream reference line)" % (int(round(s1 - s0)), int(round(s0)), int(round(s1))))
    return L["corridor"]


def water_span(q, d, rings, half=40.0):
    """v6 (P09.1): the stretch of a crossing across the water at q (survey m) along d (unit, across the stream): the
    two points where the line q +- half x d meets the water polygon's edges nearest q on either side (rings: the
    basemap's water rings, survey m); None when the polygon does not hold q between two edges"""
    a = (q[0] - d[0] * half, q[1] - d[1] * half)
    ex, ey = 2.0 * d[0] * half, 2.0 * d[1] * half
    ts = []
    for R in rings:
        for p, r in zip(R, R[1:] + R[:1]):
            fx, fy = r[0] - p[0], r[1] - p[1]
            den = ex * fy - ey * fx
            if abs(den) < 1e-12:
                continue
            gx, gy = p[0] - a[0], p[1] - a[1]
            t = (gx * fy - gy * fx) / den
            u = (gx * ey - gy * ex) / den
            if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
                ts.append(t)
    lo = [t for t in ts if t < 0.5]
    hi = [t for t in ts if t > 0.5]
    if not lo or not hi:
        return None
    t0, t1 = max(lo), min(hi)
    return (a[0] + ex * t0, a[1] + ey * t0), (a[0] + ex * t1, a[1] + ey * t1)


def stream_dir(q):
    """v4: the unit direction of the stream reference line nearest q (for a crossing's bar across it)"""
    P, _c = stream_ref()
    best = None
    for a, b in zip(P, P[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        l2 = dx * dx + dy * dy or 1e-9
        t = max(0.0, min(1.0, ((q[0] - a[0]) * dx + (q[1] - a[1]) * dy) / l2))
        d = math.hypot(a[0] + dx * t - q[0], a[1] + dy * t - q[1])
        if best is None or d < best[0]:
            ln = math.sqrt(l2)
            best = (d, (dx / ln, dy / ln))
    return best[1] if best else (1.0, 0.0)


def put_shapes(pg, shapes):
    """v4: house shapes of the shared modules (icons.py: ("poly", ring, fill, stroke, lw) / ("line", pts, colour,
    lw), page mm, hex) onto this sheet's page"""
    for s_ in shapes or []:
        if s_[0] == "poly" and len(s_[1]) >= 3:
            pg.poly(list(s_[1]), fill=s_[2] or None, stroke=s_[3] or None, lw=s_[4] or 0.2, closed=True)
        elif s_[0] == "line" and len(s_[1]) >= 2:
            pg.line(list(s_[1]), s_[2], s_[3])


# v4 (02 §2): the sheet's pictograms come from the shared icon set where it has one (common/icons.py ico_draw);
# icon() keeps its own drawings only for what the set does not hold (road, frontage, bank, bus, car, rules ...)
ICO_OF = dict(plane="tree", stall="market", bench="seating", reed="reeds", olive="olive", arch="heritage",
              farm="field", slot="viewpoint", deep="depth", flood="high_water", sewage="sewage", calendar="sun",
              visitor="people", resident="people", student="people", walker="walk", walk="walk")


def arrow_head(pg, a, b, col, size):
    """v4: a filled arrowhead at b pointing from a"""
    dx, dy = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(dx, dy) or 1.0
    ux, uy = dx / ln, dy / ln
    pg.poly([b, (b[0] - ux * size - uy * size * 0.5, b[1] - uy * size + ux * size * 0.5),
             (b[0] - ux * size + uy * size * 0.5, b[1] - uy * size - ux * size * 0.5)], fill=col, closed=True)


# v7 (G-R4-7): the hubs are numbered markers in the colour of their kind (one table, mk_register / mk_colour)
# v10 (G6-6, PLAN §2.6 PUB): the main transit hub r1, a walking hub r2, the gateway existing context r2, the
# project's places r3 (was 495338 / 8B3A3F / 847E75 and the spine's BC6F45: a hue each)
HUB_COL = dict(walk=hue("PUB", 2), transit=hue("PUB", 1), hidden=hue("PUB", 1), gateway=hue("CTX", 2))
mk_register("cl_hub", HUB_COL)
mk_register("cl_place", {"place": hue("PUB", 3)})       # the project's places
# v10 (round 6, SON page9 = the target, BRIEF §5): each hub's code, the same on p08, the spine map, the plans' headings
# and its card (c493fac HUB_CODE; T = the main transit hub, İstiklal Meydanı + Kızıl Avlu)
HUB_CODE = {"K4": "K4", "K3": "K3", u"İstiklal": "T", "K5": "K5", "K6": "K6"}


def hub_code(hb):
    """v10: a hub's code (HUB_CODE: K4, K3, T, K5, K6), the glyph of its marker on every map and card"""
    return HUB_CODE.get(hb["id"], hb["id"])


def hub_no(hb):
    """v7 (P10.2): a hub's locator number, 1-5 upstream to downstream (HUBS order), the same on p08, p10's key map,
    its plans and its card"""
    return [h_["id"] for h_ in HUBS].index(hb["id"]) + 1


def hub_col(hb):
    """v7: the marker colour of a hub (its kind; the main transit hub its own)"""
    return mk_colour("cl_hub", "transit" if hb.get("transit") else hb["kind"])


# ------------------------------------------------------------------ page 1 (booklet p.08): the framework diagram
# v4 (T3a WO-T3a-5, package B, D8 b): ONE framework diagram tells the movement story of pp.07-09: shops and use,
# the hidden stream, movement today, the proposals (refs R27-R30, ideas only). It is drawn here because this script
# runs after the site board and before the masterplan: it reads the board's half live (movement_framework.json:
# the busiest streets on foot and by car, the commercial spines, the civic constellations; city_context.json: the
# frame, the shops, the walking radius), holds its own half (spine, hubs, bus stops, shops figures, stream line)
# and the masterplan's proposal (masterplan_results.json "movement": roads by change, crossings, the town line;
# the last run's, as for the spine length).
FW_FILES = [os.path.join(bg_cache("selinus_board"), "movement_framework.json")]   # v4: written by selinus_board v51+
FW_MAP = (14.0, 197.0)                   # page 1 framework: the lower-left corner of the site frame (284.5 x 52.9 mm)
WHO_BOX = (14.0, 178.0, 392.0)           # page 1 who comes and when: x, title y, width (v7: spec S5)
P1_TILES = (14.0, 18.0, 392.0, 35.0)     # page 1 seven reasons: x, y (bottom), w, tile height
BUS_C = hue("MOV", 1)                    # v4 (R29): the bus line's colour; v10 (G6-6): movement r1, dashed (was 633131)
BUS_DASH = (1.2, 0.8)                    # v10: the later bus line dashed, so it reads apart from the r1 streets
# v9 (round 5, P08.2, Aras U06 "get rid of this line"): the project corridor line along the stream is no longer drawn
# (CORRIDOR_LW / CORRIDOR_BAR gone; corridor_line() stays for its length, it is drawn nowhere)
SHOP_C = hue("MOV", 1)                   # v7 (P08.1): today's shop streets, 1.4 mm; v10 (G6-6): movement r1 (was B5832F)
SHOP_LW = 1.4
JUNCTION_C = hue("MOV", 1)               # v10 (G6-6): the one place the main road meets the stream (was C accent)
# v9 (round 5, P08.1, Aras U06 + S03 "primary / secondary"): a shop street of lower rank (fewer shops in the site
# board's ranking) in the project palette's 8B2D2D (PLAN §3), thinner: it reads as the lesser street, and its dark
# red stands well apart from the stream's blues (5C7A86 / A2B6B5) and the ochre street; drawing rules, not data
SHOP2_C = hue("MOV", 2)                  # v10 (G6-6): movement r2 (was 8B2D2D; 8B2D2D leaves every page, P-5)
SHOP2_LW = 0.8
# v9 (P08.1 "they should continue to the extents"): a shop street is carried on along the OpenStreetMap street
# centrelines of the shared basemap (streets_in, the site board's OSM roads) to the map's edge: from each free end
# the straightest piece that starts within CL_EXT_TOL m of it (OSM pieces share their nodes), never turning more than
# CL_EXT_TURN degrees, at most CL_EXT_STEPS pieces; footways are not followed. Drawing rules, not data.
CL_EXT_TOL = 3.0
CL_EXT_TURN = 40.0
CL_EXT_STEPS = 80
# v5 (revision 30 Oct 2026, p.08 ①): the masterplan's road changes as solid lines in one width family ((colour, width
# mm)); "kept" roads are no change and are not drawn
# v10 (G6-6, PLAN §2.6 MOV: pedestrian r1, calmed r2, shared r3; relocated r2, thinner): one hue for the street changes
ROAD_STYLE = {"calmed": (hue("MOV", 2), 0.9), "pedestrian": (hue("MOV", 1), 1.2), "shared": (hue("MOV", 3), 0.9),
              "relocated": (hue("MOV", 2), 0.6)}
ROAD_WORD = {"calmed": "road calmed", "pedestrian": "street made pedestrian", "shared": "shared street",
             "relocated": "road relocated"}
# v5 (p.08 ②, G5): the seasons behind the calendar as soft tones of the palette (name, months, colour faded 88 %)
SEASONS_CL = ((u"winter", (12, 1, 2), "91ADB4"), (u"spring", (3, 4, 5), "8C9969"), (u"summer", (6, 7, 8), "CC9A52"),
              (u"autumn", (9, 10, 11), "B5832F"))
MON = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def cl_street_walk(e, d, nets, out_fn, used, grid):
    """v9 (P08.1): from the point e (survey m) heading d, the OSM street pieces (nets) that carry the street on: at
    each step the piece through e (a vertex within CL_EXT_TOL) whose next point turns least from d, taken to its end;
    stops at the map's edge (out_fn), when no piece turns less than CL_EXT_TURN, or after CL_EXT_STEPS. grid =
    {(cell x, cell y): [(piece, vertex)]} on CL_EXT_TOL cells (only the cells round e are searched). Returns the
    points after e ([] = none)."""
    out = []
    for _i in range(CL_EXT_STEPS):
        if out_fn(e):
            break
        dl = math.hypot(d[0], d[1]) or 1.0
        du = (d[0] / dl, d[1] / dl)
        best = None
        gx, gy = int(math.floor(e[0] / CL_EXT_TOL)), int(math.floor(e[1] / CL_EXT_TOL))
        near = [qv for a_ in (gx - 1, gx, gx + 1) for b_ in (gy - 1, gy, gy + 1) for qv in grid.get((a_, b_), ())]
        for qi, i in near:
            Q = nets[qi]
            p = Q[i]
            if qi in used or math.hypot(p[0] - e[0], p[1] - e[1]) > CL_EXT_TOL:
                continue
            for nxt in (Q[i + 1:], Q[:i][::-1]):
                q = next((r for r in nxt if math.hypot(r[0] - e[0], r[1] - e[1]) > 1.0), None)
                if q is None:
                    continue
                vx, vy = q[0] - e[0], q[1] - e[1]
                c_ = max(-1.0, min(1.0, (vx * du[0] + vy * du[1]) / (math.hypot(vx, vy) or 1.0)))
                turn = math.degrees(math.acos(c_))
                if best is None or turn < best[0]:
                    best = (turn, qi, list(nxt))
        if best is None or best[0] > CL_EXT_TURN:
            break
        used.add(best[1])
        prev = e
        out += best[2]
        e = out[-1]
        for r in reversed(out[:-1]):                      # the last direction, from a point at least 1 m back
            if math.hypot(r[0] - e[0], r[1] - e[1]) > 1.0:
                prev = r
                break
        d = (e[0] - prev[0], e[1] - prev[1])
    return out


def cl_street_extend(runs, f, label=None, win=None):
    """v9 (round 5, P08.1, Aras U06 "they should continue to the extents"): a shop street's runs (survey m; one OSM
    way each, clipped to the site frame by the site board) joined end to end, then each free end that stops inside
    the map carried on along the OpenStreetMap street centrelines (the shared basemap's streets_in, footways left
    out) to the map's edge (cl_street_walk). Returns runs + the pieces added; logged with the metres added."""
    if not runs:
        return runs
    try:
        D = basemap_load()
        lay_ = (D or {}).get("layers") or {}
        nets = [[tuple(p) for p in P] for cl, P in list(lay_.get("streets_in") or []) +
                (list(lay_.get("streets_out") or []) if win else [])   # v13: beyond the frame too
                if cl != "path" and len(P) >= 2]
    except Exception:
        nets = []
    if not nets:
        BM_NOTE.append(u"FLAG p08: no basemap street centrelines (run the site board once): the shop street %s is "
                       u"drawn as the board wrote it, not carried on to the map's edge" % (label or u""))
        return runs

    def uv_in(q, m):
        u, v = frame_uv(f, q)
        return f["u0"] + m < u < f["u0"] + f["w"] - m and f["v0"] + m < v < f["v0"] + f["h"] - m
    if win:                                               # v13 (round 9 d4): the map's edge = its context window
        def uv_in(q, m):
            u, v = frame_uv(f, q)
            return win[0] + m < u < win[2] - m and win[1] + m < v < win[3] - m
    out_fn = lambda q: not uv_in(q, 3.0)                  # at (within 3 m of) or past the map's edge
    grid = {}
    for qi, Q in enumerate(nets):
        for i, p in enumerate(Q):
            grid.setdefault((int(math.floor(p[0] / CL_EXT_TOL)), int(math.floor(p[1] / CL_EXT_TOL))), []).append((qi, i))
    dist = lambda a, b: math.hypot(a[0] - b[0], a[1] - b[1])
    chains = [list(R) for R in runs]
    merged = True
    while merged:                                         # the street's ways joined where they share an end
        merged = False
        for i in range(len(chains)):
            for j in range(i + 1, len(chains)):
                a, b = chains[i], chains[j]
                if dist(a[-1], b[0]) < CL_EXT_TOL:
                    chains[i] = a + b[1:]
                elif dist(a[-1], b[-1]) < CL_EXT_TOL:
                    chains[i] = a + b[::-1][1:]
                elif dist(a[0], b[-1]) < CL_EXT_TOL:
                    chains[i] = b + a[1:]
                elif dist(a[0], b[0]) < CL_EXT_TOL:
                    chains[i] = b[::-1] + a[1:]
                else:
                    continue
                del chains[j]
                merged = True
                break
            if merged:
                break
    own = set((round(p[0]), round(p[1])) for R in runs for p in R)
    used = set(qi for qi, Q in enumerate(nets) if (round(Q[0][0]), round(Q[0][1])) in own and
               (round(Q[-1][0]), round(Q[-1][1])) in own)   # the street's own ways are not followed again
    added, m_ = [], 0.0
    for ci, R in enumerate(chains):
        if len(R) < 2:
            continue
        for Q in (R, R[::-1]):
            e = Q[-1]
            if out_fn(e) or any(dist(e, p) < CL_EXT_TOL for cj, R2 in enumerate(chains) if cj != ci for p in R2):
                continue                                  # at the edge already, or a branch end on the same street
            prev = next((r for r in reversed(Q[:-1]) if dist(r, e) > 1.0), Q[0])
            ext = cl_street_walk(e, (e[0] - prev[0], e[1] - prev[1]), nets, out_fn, used, grid)
            if ext:
                piece = [e] + ext
                added.append(piece)
                m_ += sum(dist(a, b) for a, b in zip(piece, piece[1:]))
    BM_NOTE.append(u"p08 shop street %s: %d end(s) carried on along OpenStreetMap street centrelines towards the "
                   u"map's edge, %d m added (before the cut to the map)" % (label or u"", len(added), int(round(m_))))
    return runs + added


def framework_map(pg, L):
    """v7 (round 4, P08.1-P08.3, G-R4-1/2/4/7/9/11; spec S5): the whole corridor on the site frame at 1:10,000 on the
    frame's axes, through THE draw order (cl_map / map_draw): the muted base; the study area tinted D9 (the project's
    ground: the houses read through); TODAY the shop streets (movement_framework.json spines, else the main spine)
    on a white casing; the study line; then the hubs as numbered markers 1-5 (the p10 numbers, colour = hub kind),
    the one place the main road meets the stream; the names of the stream and the shop streets where a free spot is
    next to them (else they stand in the legend only).
    v9 (round 5 S9, P08.1-P08.3, G-R5-8/12): recorded on pg (the recorder), exported by p08_items as one true-scale
    drawing; P08.1: the streets ranked by their shops (the site board's ranking: most shops first): the first in ochre
    (SHOP_C), the others in SHOP2_C, thinner, each carried on to the map's edge (cl_street_extend); P08.2: no project
    corridor line along the stream; no north arrow, scale bar, neatline, heading or legend drawn (the booklet's: the
    drawing's north_deg and scale_bar; the heading, legend rows and shops note are returned as items). Returns
    dict(box (page mm), f (site frame), rows [(sample draw, words)], head, shops).
    v13 (round 9 G9-4, ADDENDUM §0, PLAN §cause b2 / d4, frame p08.2 292 x 58 mm): an M map: the focus = the study
    area + the hubs + the junction, 30 m round (cl_focus); drawn at the §0 true scale T of that focus in p08.2
    (cl_r9_scale: Tfit, label L, T = max(Tfit, L)) over the context window r9_window (focus grown to the frame's
    aspect x 1.3), base = basemap mode "context" (layers a-j to the window's edge, names anchored in the table's
    spelling); the shop streets carried on to the window's edge; the stream's name = the base's "SELİNOS ÇAYI" (v12's
    own "Selinos stream" label is gone). Also returns den, sc (scale dict), focus, window and base (items)."""
    mx, my = FW_MAP
    ctx = L.get("ctx") or {}
    fw = L.get("fw") or {}
    f = site_frame(ctx)
    hubs = hub_list()
    focus = cl_focus(f, hubs, extra=[(30058.0, 32047.0)])
    sc = cl_r9_scale(f, "p08.2", focus)
    den = sc["den"]
    wu0, wv0, wu1, wv1 = sc["win"]
    T = frame_T(f, mx, my, den, wu0, wv0)
    k = 1000.0 / den
    fw_, fh_ = (wu1 - wu0) * k, (wv1 - wv0) * k
    box_ = (mx, my, mx + fw_, my + fh_)
    PLAN_BOX["fw"] = box_
    inside = lambda q: mx <= q[0] <= mx + fw_ and my <= q[1] <= my + fh_
    frame = (mx + 1.0, my + 1.0, mx + fw_ - 1.0, my + fh_ - 1.0)
    MAP = "map p08"
    head = (u"The whole corridor · the shop streets, the hidden stream and the project from end to end " +
            cite(SRC_MAIN) + u" " + cite(SRC_SHOPS)).strip()
    pg.keep(box_, "map", MAP)
    sbox = sc["sbox"]
    # base extra: the stream hidden under the town (the reference line's covered pieces), dashed
    P, cov = stream_ref()
    covered = [("line", R_, C["water_deep"], 0.8, [1.6, 0.9], 1.0) for c_, R_ in clip_runs(P, sbox, cov) if c_]
    # TODAY: the shop streets (not a proposal: drawn whole, not clipped)
    spines = fw.get("spines") or [dict(label=landmark_name("bankalar_caddesi") + u" - " +
                                       landmark_name("kinik_caddesi"), runs=[MAIN_SPINE])]
    if not fw.get("spines"):
        BM_NOTE.append("FLAG: no movement_framework.json (site board v51+): the main spine stands in for the shop "
                       "streets")
    # v9 (P08.1): ranked by their shops (the site board's corr_primary order, most shops first; ties keep it)
    ranked = sorted(spines, key=lambda g: -float(g.get("shops") or 0.0))
    lines, runs_ = [], []
    for i in range(len(ranked) - 1, -1, -1):              # the lesser streets first, the first-ranked on top
        g = ranked[i]
        col, lw_ = (SHOP_C, SHOP_LW) if i == 0 else (SHOP2_C, SHOP2_LW)
        rs = cl_street_extend([[tuple(p) for p in R_] for R_ in g["runs"] if len(R_) >= 2], f, g.get("label"),
                              win=sc["win"])
        runs_ += rs
        lines += [("line", R_, C["white"], lw_ + 0.5, None, 1.0) for R_ in rs]
        lines += [("line", R_, col, lw_, None, 1.0) for R_ in rs]
        BM_NOTE.append(u"p08 shop street %d: %s, %s shops (site board), %s" % (
            i + 1, g.get("label"), g.get("shops", u"?"), u"ochre" if i == 0 else SHOP2_C))
    study = cl_study()
    nb, study = cl_map(pg, "p08", T, sbox, den, {"proj_tint": ml_tint(study), "proj_lines": lines},
                       base_extra=covered, clip=False, legend_cols=[ML_TINT], ring=sc["ring"])
    base = CL_LAST_BASE[0]
    named = set(name_key(place_label(it[1]) or it[1]) for it in base if it[0] == "text")
    # our lines are keeps for the labels (no name on a shop street)
    for R_ in runs_:
        pg.keep([T(p) for p in R_], "line", "shop street")
    # the marks on top: the junction, then the hubs, numbered as on p10
    jx, jy = T((30058.0, 32047.0))                          # Kınık Caddesi over the covered stream (stop 3's place)
    with pg.group("annotations", u"main road meets the stream"):
        disc(pg, jx, jy, 1.2, JUNCTION_C, C["white"], 0.3)
    pg.keep((jx - 1.4, jy - 1.4, jx + 1.4, jy + 1.4), "marker", "junction")
    for hb in hubs:
        hx, hy = T(hb["xy"])
        if inside((hx, hy)):
            with pg.group("hubs", u"hub " + hub_code(hb)):
                cl_marker_free(pg, hx, hy, hub_code(hb), hub_col(hb), 7.0, frame=frame, allow=(MAP,),
                               name="hub %d" % hub_no(hb))
    # names next to their own line, where free (else in the legend only); v9: through the names table
    for g in spines:
        if not g.get("label") or g["label"] == "an unnamed street":
            continue
        if name_key(street_label(g["label"])) in named:   # v13: the base names it already (layer b), once
            continue
        Q = [q for q in (T(p) for p in max(g["runs"], key=len)) if inside(q)]
        if len(Q) > 1:
            with pg.group("labels", u"name " + street_label(g["label"])):
                cl_place(pg, street_label(g["label"]), Q[len(Q) // 2], CL_AN_PT, AN_NAME["colour"], False, 1.2,
                         frame, (MAP,))           # v12 (G7-2): names small, annotation set (common/annot.py AN_NAME)
    # v13 (G9-4 f): the stream's name is the base's "SELİNOS ÇAYI" (layer f), so v12's own label is not set here
    # the legend rows (an Ix legend beside the map: the booklet places it); v13: the context classes follow
    # (basemap_legend_rows in p08_items), the stream's fill row among them
    rows = []
    rows.append((sw_line(C["water_deep"], 0.8, (1.6, 0.9)), place_name("stream") + ", covered"))
    rows.append((lambda p_, b: (p_.rect(b[0], b[1], b[2] - b[0], b[3] - b[1], fill=tint_hex(ML_TINT, 1.0 - ML_TINT_ALPHA)),
                                sw_line(BM_STUDY_LINE["colour"], BM_STUDY_LINE["width_mm"],
                                        tuple(BM_STUDY_LINE["dash_mm"]))(p_, b)),
                 "study area: the project's ground"))
    for i, g in enumerate(ranked):                        # v9 (P08.1): one row per rank
        nm_ = street_label(g["label"]) if g.get("label") and g["label"] != "an unnamed street" else u""
        rows.append((sw_line(SHOP_C, SHOP_LW) if i == 0 else sw_line(SHOP2_C, SHOP2_LW),
                     (u"shop street today" + (u"" if i == 0 else u", fewer shops") + (u": " + nm_ if nm_ else u""))))
    rows.append((sw_mark(lambda p_, x, y: disc(p_, x, y, 1.1, JUNCTION_C, C["white"], 0.3)),
                 "the main road meets the stream, covered"))
    for hb in hubs:
        kd = "walking hub" if hb["kind"] == "walk" else ("main transit hub" if hb["transit"] else
                                                         ("gateway" if hb["kind"] == "gateway" else "hub"))
        rows.append((sw_mark(lambda p_, x, y, hb=hb: cl_marker(p_, x, y, hub_code(hb), hub_col(hb), 7.0,
                                                               name="legend hub %d" % hub_no(hb))),
                     u"%s = %s · %s" % (hub_code(hb), hb["title"], kd)))   # v10: the code explained
    # the shops figure: one headline value and one line (G4), as one note with its value bold
    sf = shop_figures()
    shops = (u"**%d of %d shops** by the stream sit on the covered %d m, where the main road meets it" % (
        sf["covered_reach"], sf["by_stream"], sf["covered_reach_m"]))
    BM_NOTE.append(u"p08 corridor map: focus %.0f x %.0f m, window %.0f x %.0f m at 1:%s (%.0f x %.0f mm)" % (
        focus[2] - focus[0], focus[3] - focus[1], wu1 - wu0, wv1 - wv0, fmt(den), fw_, fh_))
    return dict(box=box_, f=f, rows=rows, head=head, shops=shops, den=den, sc=sc, focus=focus, window=sc["win"],
                base=base)


def who_rows():
    """v4 (G7): who the project brings, by group: (group key, name, figure, low, high, what the figure counts, public
    sources) from the research (WHO): visitors, residents, students (the two vocational schools together)"""
    return [("T", u"Visitors", u"433,000", 433000, 433000, u"visits to Bergama in 2023", (SRC_WHO_T,)),
            ("L", u"Residents", u"11,002", 11002, 11002, u"in the 7 mahalles by the stream, 2025", (SRC_WHO_L,)),
            ("S", u"Students", u"1,825-1,925", 1425 + 400, 1425 + 500, u"at Bergama's two vocational schools, 2024-25",
             (SRC_WHO_S1, SRC_WHO_S2))]


def act_months(a):
    """v5: the months (1-12) a place of the project is open: the summer bed events July to September only (the bed
    is dry then: the flood rule, FLOOD), every other place all year"""
    return (7, 8, 9) if a is EVENTS else tuple(range(1, 13))


def who_panel(pg, L):
    """v5 (revision 30 Oct 2026, p.08 ②, refs R03 + R05 as ideas, G5): who comes to the stream across the year, on
    one month axis over soft season tones. On top the Selinos stream's mean monthly flow (water balance results,
    live, no number: why the bed opens only in summer). Per group (visitors, residents, students; its figure with
    its public source): a strip of the places open to the group each month (bar height, the number where it
    changes) with a figure standing on each run of the year (R05), then one row per place in a light icon badge
    (R03): open all year = a light bar, in season only = a full bar, the weekly market = one tick a week. Only the
    script's data: no visitor seasons, term dates or hours (none is sourced in the repo; listed in the log). The key
    under it (key_flow) and one line of conclusion, made from the same data, on the title line.
    v9 (round 5 S9, P08.3, G-R5-12): the chart only is recorded on pg (exported by p08_items as one chart drawing in
    mm, sized by the booklet); its heading, the conclusion (a note) and the key (legend rows) are returned as items:
    dict(head, note, rows)."""
    x0, ty, W = WHO_BOX
    x1 = x0 + W
    head = u"Who comes to the stream, and when"
    ax0, ax1 = 178.0, x1                                  # the month axis (mm)
    mw = (ax1 - ax0) / 12.0
    MX = lambda m: ax0 + (m - 1) * mw                     # left edge of month m
    PITCH, STRIP, GAP = 3.4, 6.5, 2.4                    # v7 (spec S5): rows 3.4 mm apart, names 7.5 pt
    acts = FUNCS + [EVENTS]
    groups = who_rows()
    try:
        river = [float(v) for v in L.get("river_month")] if len(L.get("river_month") or []) == 12 else None
    except Exception:
        river = None
    if not river:
        BM_NOTE.append("FLAG: no monthly stream flow (water balance results river_month_m3): p.08's calendar has no "
                       "stream row")
    yh = ty - 7.0                                         # month names
    ys = yh - 2.4                                         # top of the rows
    river_h = 6.0 if river else 0.0
    mine_of = dict((g[0], [a for a in acts if g[0] in a["who"]]) for g in groups)
    blk = dict((g_, max(11.0, STRIP + 1.0 + PITCH * len(mine_of[g_]))) for g_ in mine_of)
    # v13 (round 9 d5, BRIEF G9-2 C, frame p08.4 392 x 113 with its heading): the chart box = the frame less the
    # heading row; the rows' pitch, strips, gaps and the stream row stretch so the plot fills its height (text keeps
    # its size); never squeezed below v12's spacing (a taller chart is a WARNING)
    wh_ = r9_wh("p08.4") or (W, 113.0)
    Hc = wh_[1] - CL_HEAD_MM
    nat = river_h + sum(blk[g_] + GAP for g_ in blk)
    room = Hc - (ty - ys)
    sv = max(1.0, room / nat) if nat > 0 else 1.0
    if room < nat - 0.05:
        wn_warn("p08", "cl_p08_who fit", u"who comes chart needs %.1f mm, frame gives %.1f (text kept at size)" % (
            nat + ty - ys, Hc), log=CL_LOG)
    PITCH, STRIP, GAP, river_h = PITCH * sv, STRIP * sv, GAP * sv, river_h * sv
    blk = dict((g_, max(11.0 * sv, STRIP + 1.0 * sv + PITCH * len(mine_of[g_]))) for g_ in mine_of)
    yb = ys - river_h - sum(blk[g_] + GAP for g_ in blk)
    CL_LOG.append(u"chart p08 cl_p08_who %.0f x %.1f mm (frame p08.4 %.0f x %.0f less the heading row), rows x %.3f" % (
        W, ty - yb, wh_[0], wh_[1], sv))
    for nm, ms, col in SEASONS_CL:                        # G5: the seasons as soft tones behind every row
        for m in ms:
            pg.rect(MX(m), yb, mw, ys - yb, fill=tint_hex(col, 0.88))
        pg.text(nm, (MX(1) + mw) if nm == u"winter" else (MX(ms[0]) + 1.5 * mw), yh + 3.6, 7, C["ink2"], True, "C")
    for i, m_ in enumerate(MON):
        pg.text(m_, MX(i + 1) + mw / 2.0, yh, 7, C["ink2"], False, "C")
    for i in range(13):
        pg.line([(ax0 + i * mw, ys), (ax0 + i * mw, yb)], C["white"], 0.25)
    y = ys
    if river:                                             # the stream: water in the bed, month by month
        rmax = max(river) or 1.0
        put_shapes(pg, ico_draw("stream", x0 + 3.0, y - 3.0, 5.0))
        pg.text("Selinos stream", x0 + 7.5, y - 3.8, 9, C["ink"], True)
        fit(pg, "water in the bed", 120.5, y - 3.8, 7, ax0 - 122.0, C["ink2"])
        for m in range(1, 13):
            pg.rect(MX(m) + 0.8, y - river_h + 0.4, mw - 1.6, max(0.2, (river_h - 1.2) * river[m - 1] / rmax),
                    fill=C["water"])
        y -= river_h
    nglob = max([1] + [sum(1 for a in mine_of[g_] if m in act_months(a)) for g_ in mine_of for m in range(1, 13)])
    for g_, name, big, lo, hi, what, srcs in groups:
        mine = mine_of[g_]
        col = GROUP[g_][1]
        pg.line([(x0, y - GAP / 2.0), (x1, y - GAP / 2.0)], C["faint"], 0.2)
        top = y - GAP
        put_shapes(pg, ico_draw("people", x0 + 3.0, top - 3.0, 5.6, ink=col, accent=col))
        pg.text(name, x0 + 7.5, top - 3.6, 9, C["ink"], True)
        pg.text(big, x0 + 9.5 + text_w(name, 9, True), top - 3.6, 9, col, True)
        # v10 (G6-8, SON page8 pairs "Visitors 433,000 / visits to B" x "[10]" (and [11], [12])): the source mark is
        # its own text, right of the group's whole two-line block, so no box of one sits on the other
        cs_ = " ".join(c_ for c_ in (cite(s_) for s_ in srcs) if c_)
        fit(pg, what, x0 + 7.5, top - 7.2, 7, 84.0, C["ink2"])
        if cs_:
            bw_ = max(text_w(name, 9, True) + 2.0 + text_w(big, 9, True), text_w(what, 7))   # v12 (L6): the line as set (fit never < 7 pt)
            pg.text(cs_, x0 + 7.5 + bw_ + 1.5, top - 7.2, 7, C["ink2"])
        # the strip: how many places are open to the group each month; a figure on each run of the year (R05)
        n_m = [sum(1 for a in mine if m in act_months(a)) for m in range(1, 13)]
        sb = top - STRIP
        hmax = STRIP - 3.4                                # room for the number and the figure on the bars
        fit(pg, "places open to them", 120.5, sb + 0.6, 7, ax0 - 122.0, C["ink2"])
        for m in range(1, 13):
            pg.rect(MX(m) + 0.3, sb, mw - 0.6, hmax * n_m[m - 1] / float(nglob), fill=tint_hex(col, 0.3))
        runs, s0 = [], 1
        for m in range(2, 14):
            if m == 13 or n_m[m - 1] != n_m[s0 - 1]:
                runs.append((s0, m - 1))
                s0 = m
        for a_, b_ in runs:
            h_ = hmax * n_m[a_ - 1] / float(nglob)
            pg.text(str(n_m[a_ - 1]), MX(a_) + 1.0, sb + h_ + 0.5, 7, col, True)
            put_shapes(pg, ico_draw("people", (MX(a_) + MX(b_ + 1)) / 2.0, sb + h_ + 1.7, 3.2, ink=col, accent=col))
        # one row per place: a light icon badge (R03), all year light, in season full, the market one tick a week
        ry = sb - 1.0 - PITCH / 2.0
        for a in mine:
            ic = a["icon"]
            pg.rect(116.0, ry - 1.3, 2.6, 2.6, fill=tint_hex(col, 0.8))
            if ic in ICO_OF:
                put_shapes(pg, ico_draw(ICO_OF[ic], 117.3, ry, 2.2, ink=col))
            else:
                icon(pg, ic, 116.2, ry + 1.1, 2.2)
            fit(pg, a["name"], 120.5, ry - 0.95, 7.5, ax0 - 122.0, C["ink"])
            ms = act_months(a)
            if a.get("n") == 5:                           # the producers' market: one day a week (Wednesdays)
                for wk in range(52):
                    xw = ax0 + (wk + 0.5) * (ax1 - ax0) / 52.0
                    pg.line([(xw, ry - 0.9), (xw, ry + 0.9)], col, 0.45)
            elif len(ms) < 12:
                pg.rect(MX(ms[0]) + 0.3, ry - 1.0, len(ms) * mw - 0.6, 2.0, fill=col)
            else:
                pg.rect(ax0 + 0.3, ry - 0.7, 12 * mw - 0.6, 1.4, fill=tint_hex(col, 0.62))
            ry -= PITCH
        y = top - blk[g_]
    # one line of conclusion from the same data, right-aligned on the title line
    seas = [a for a in acts if len(act_months(a)) < 12]
    concl = None
    if seas:
        ms = act_months(seas[0])
        low = bool(river) and (min(range(12), key=lambda i: river[i]) + 1) in ms
        concl = (u"the **dry bed** adds %s, %s-%s%s" % (seas[0]["name"].lower(), MON[ms[0] - 1], MON[ms[-1] - 1],
                                                       u", when the stream runs lowest" if low else u""))
        concl = concl[:1].upper() + concl[1:]
    # the key under the calendar (key_flow, G1)
    gc = GROUP["L"][1]

    def sw_bars(p_, b):
        for i in range(3):
            p_.rect(b[0] + i * 2.1, b[1], 1.7, (b[3] - b[1]) * (0.45 + 0.27 * i), fill=tint_hex(gc, 0.3))

    def sw_ticks(p_, b):
        for i in range(4):
            p_.line([(b[0] + 0.6 + i * 1.6, b[1] + 0.3), (b[0] + 0.6 + i * 1.6, b[3] - 0.3)], gc, 0.45)
    ent = [(sw_bars, "places open to the group that month"),
           (sw_mark(lambda p_, x, y: put_shapes(p_, ico_draw("people", x, y, 2.8, ink=gc, accent=gc))),
            "the group at the stream"),
           (lambda p_, b: p_.rect(b[0], b[1] + 0.6, b[2] - b[0], 1.4, fill=tint_hex(gc, 0.62)), "open all year"),
           (sw_fill(gc), "open in season only"), (sw_ticks, "market day, once a week")]
    if river:
        ent.append((lambda p_, b: [p_.rect(b[0] + i * 2.1, b[1], 1.7, (b[3] - b[1]) * (1.0 - 0.4 * i),
                                           fill=C["water"]) for i in range(3)], "Selinos stream: mean monthly flow"))
    return dict(head=head, note=concl, rows=ent,          # v9: the key is a legend item (the booklet sets it)
                box=(x0, min(yb, ty - Hc), x1, ty))       # v13 (d5): the exported chart box, the frame's size


def reasons_tiles(pg):
    """the seven reasons the stream edge has no spine (v1.6 tiles, kept): pictogram, one figure, keywords"""
    rx, ry, rw, rh = P1_TILES
    tx = rx                                               # v9: no step marker (this block is not in the booklet)
    pg.text("SEVEN REASONS THE STREAM EDGE HAS NO SPINE", tx, ry + rh + 3.5, 9, C["ink"], True)
    tw_ = rw / 7.0
    for i, (ic, head, big, kws, src) in enumerate(REASONS):
        if ic == "deep" and not big:
            big = bed_depth()
        x = rx + i * tw_                                  # v6 (G17): no frame round a tile; whitespace parts them
        icon(pg, ic, x + 2.5, ry + rh - 2.5, 9)
        fit(pg, big, x + 13.5, ry + rh - 10, 13, tw_ - 18.5, C["accent"], True)
        fit(pg, head, x + 2.5, ry + rh - 17.5, 7, tw_ - 7.5, C["ink"], True)
        for j, k in enumerate(kws):
            fit(pg, k, x + 2.5, ry + rh - 22.0 - j * 3.6, 7, tw_ - 7.5, C["ink"])
        c_ = cite(src)
        if c_:
            pg.text(c_, x + 2.5, ry + 2.5, 7, C["ink2"], True)


# ------------------------------------------------------------------ v1.11: the bridge places (history D2 D3 D8 D10)
# The 8 stops regrouped into bridge clusters (history_phase1/DECISIONS.md D2, D3; PHASE2_SPEC §3). Aras 27 Oct 12:05
# ("Both"): the MAIN TRANSIT HUB is İstiklal Meydanı + Kızıl Avlu (the town lines 651/652/653 stop there), K3, K4, K5
# are WALKING hubs, each a dry hub square at street level above Q500 with plane trees (D8) and a floodable sub-hub
# down in the bed (D10), linked on foot by the spine; a town line extended to K4 (e.g. 651) is a proposed later step;
# K6 is the gateway out. MAIN_TRANSIT_HUB = "bridges" draws K3, K4, K5 as the transit hubs instead (the earlier
# reading); "İstiklal" is Aras's decision. The switch MAIN_TRANSIT_HUB is at the top of the file.
# Points in survey m: bridges h01 §0/§5 (s62); İstiklal Meydanı = h01 §5 P16 label; Kızıl Avlu = h01 §5 P02.
HUB_PTS = dict(K4=(29846.0, 32278.0), K3=(30037.0, 32122.0), IST=(29990.0, 32030.5), RED=(30245.0, 31962.0),
               K5=(30294.0, 31792.0), K6=(30647.0, 31252.0))
# Existing bus stops: OSM highway=bus_stop nodes of bergama_osm.osm (extract of 28 Jul 2026, the commercial spine
# thread's 3_project_data_used/data), converted with the h01 §0 formula (x = 30037.01 + (lon - 27.18127) x 86,361;
# y = 32121.57 + (lat - 39.123302) x 111,320; +-10-30 m), calculated 27 Oct 2026: (OSM node, x, y, lines).
# Lines = the OSM route=bus relations holding the node; the same as ESHOT's official stop list (h03 Q1, research
# library/research/history_hubs_2026-10-27/ lines 30-35, s124 s126), except İstiklal Meydanı where the official list
# also has 831-833 (h03 [U]: shown as OSM, the conflict in the notes). The distance is computed in hub_list().
BUS_STOPS = {
    "Camikebir Caddesi": ("2295927910", 29841.0, 32243.7, "831 832 833"),
    "Tabak Köprüsü": ("641990846", 30017.4, 32106.8, "831 832 833"),
    "İstiklal Meydanı": ("12278806082", 29995.4, 32019.8, "651 652 653"),
    "Kızıl Avlu": ("12278806081", 30245.0, 32020.1, "651 652 653"),
    "Üç Kemer Köprüsü": ("12279023948", 30296.4, 31696.7, "656 831-833"),
    "Bergama Sanayi": ("12278806069", 30575.0, 31232.4, "8 lines"),
}
# trips: h03 Q1 (research lines 36-40, s125, ESHOT timetables, TARIFE_ID 1 = weekday): 651 54 departures, 656 12,
# 831 / 832 / 833 2-3 trips each way; K6 stop 23127 lines from research line 35.
# Stops per cluster (n = FUNCS / EVENTS): 1 Tabaklar Hamamı bazaar -> K4 (H4); 7 the reed basins of the upstream entry
# -> K4, the first hub downstream of it; 6 study terraces (ch 620) -> K3, 89 m from K3 and 153 m from K4 along the
# stream; 2 workshops -> K3 (H3 tanning reach); 3 junction square over the covered reach + 4 Kızıl Avlu terrace -> the
# İstiklal Meydanı + Kızıl Avlu cluster (H2: the covered reach and its Kızıl Avlu tunnel mouths); 5 market -> K5;
# 8 summer bed events -> the in-bed sub-hubs of K3, K4, K5 (D10).
# v6 (G16, D9): titles are the real names (common/names.py); the short name in "later" sits under its full name
HUBS = [
    dict(id="K4", title=bridge_name("K4"), pt="K4", ch=CH["K4"], kind="walk", role=landmark_name("ulucami") + u" + " + landmark_name("tabaklar_hamami"),
         bus=[("Camikebir Caddesi", "K4")], trips="today 831-833 only · 2-3 trips a day each way",
         later=u"later step: a town line (e.g. 651) extended to " + bridge_name("K4", short=True), stops=[7, 1]),
    dict(id="K3", title=bridge_name("K3"), pt="K3", ch=CH["K3"], kind="walk", role="the tanning reach: craft",
         bus=[("Tabak Köprüsü", "K3")], trips="831-833 only · 2-3 trips a day each way", stops=[6, 2]),
    dict(id="İstiklal", title=landmark_name("istiklal_meydani") + u" + " + landmark_name("kizil_avlu"), pt="IST", ch=752, kind="hidden",
         role="the covered reach", bus=[("İstiklal Meydanı", "IST"), ("Kızıl Avlu", "RED")],
         trips="651: 54 departures a weekday, every 15-20 min", stops=[3, 4]),
    dict(id="K5", title=bridge_name("K5"), pt="K5", ch=CH["K5"], kind="walk", role="producers' market",
         bus=[("Üç Kemer Köprüsü", "K5")], trips="656: 12 a weekday · 831-833: 2-3", stops=[5]),
    dict(id="K6", title=bridge_name("K6"), pt="K6", ch=CH["K6"], kind="gateway", role="gateway out of town",
         bus=[("Bergama Sanayi", "K6")], trips="643 644 651 652 653 656 836 936", stops=[]),
]
SRC_BUS = ("OpenStreetMap contributors, extract of 28 Jul 2026 (bus stops); ESHOT open data (lines and weekday "
           "trips)")                               # v4 (D13): the public sources only
SRC_HUBS = "Hubs: history decisions D2 D3 D8 D10 and Aras 27 Oct 12:05 (history_phase1/DECISIONS.md)"
SRC_PLANE = ("Plane trees: Ottoman squares with plane trees (h02, ICOMOS s13 p281); drought-sensitive, watered "
             "(h03 Q4)")
SRC_HIDDEN = u"Covered reach: Kızıl Avlu twin tunnels (h02 E01); the stream under İstiklal Meydanı (h02 E02)"
# v3 (MIRAQUA 28 Oct, F5: booklet sources are public online only): these sources name only our own files, boards,
# runs or decisions, so the sheet prints no [n] for them (cite() gives ""); the run-provenance sources (site board
# movement, context and bank vote, water balance results, the reach method) are no longer cited at their calls
CITE_OFF = (SRC_WHO, SRC_TABAK, SRC_HUBS, SRC_WET, SRC_HIDDEN, SRC_BANK, SRC_BED)
# v4 (D13, Aras 29 Oct 18:56: credit only publicly available sources): who the project brings, by group (research
# library/research/city_link_2026-10-24, its public sources), and the only sources the sheet numbers (PUB_SRC)
SRC_WHO_T = "Anadolu Ajansı, 16 Jun 2024 (NTV; haber7, 17 Jun 2024): 433,000 visitors to Bergama in 2023"
SRC_WHO_L = "TÜİK, Adrese Dayalı Nüfus Kayıt Sistemi (ADNKS) 2025: the 7 mahalles by the stream"
SRC_WHO_S1 = "Ege Üniversitesi Bergama MYO, unit activity report 2025: 1,425 students in 2024/25"
SRC_WHO_S2 = "mahalligundem.com, 01 Aug 2025: 400 to 500 students at DEÜ Bergama MYO"
PUB_SRC = (SRC_RULES, SRC_SHOPS, SRC_MAIN, SRC_BUS, SRC_WHO_T, SRC_WHO_L, SRC_WHO_S1, SRC_WHO_S2)
# v9 (round 5, G-R5-12): each public source's key in items.json "sources" (texts cite it as {src:<key>})
CL_SRC_KEY = {SRC_RULES: "cl_rules", SRC_SHOPS: "cl_osm_shops", SRC_MAIN: "cl_osm", SRC_BUS: "cl_bus",
              SRC_WHO_T: "cl_who_visitors", SRC_WHO_L: "cl_who_residents", SRC_WHO_S1: "cl_who_ege_myo",
              SRC_WHO_S2: "cl_who_deu_myo"}


def is_transit(hb):
    """v1.11: is this the main transit hub (MAIN_TRANSIT_HUB)?"""
    return (hb["id"] == "İstiklal") == (MAIN_TRANSIT_HUB == "İstiklal") and hb["kind"] != "gateway"


def hub_list():
    """v1.11: the hubs with their bus stops and distances (calculated: straight line, survey m)"""
    out = []
    for hb in HUBS:
        stops = []
        for name, ref in hb["bus"]:
            nid, sx, sy, lines = BUS_STOPS[name]
            rx, ry = HUB_PTS[ref]
            stops.append(dict(name=name, osm_node=nid, xy=[sx, sy], m=int(round(math.hypot(sx - rx, sy - ry))),
                              lines=lines, from_point=ref))
        out.append(dict(hb, bus_stops=stops, xy=list(HUB_PTS[hb["pt"]]), transit=is_transit(hb)))
    return out


def hub_glyph(pg, kind, x, y, w, h):
    """v1.11: a hub as a small section in the box (x, y - h)-(x + w, y): the dry hub square at street level above
    Q500 with its plane tree, steps down to the sub-hub in the bed beside the water strip (D10); the hidden stream
    square over its culvert; the gateway as a road out. Graphic only. v7: stop 8 as the shared marker."""
    ux, uy = w / 10.0, h / 8.0
    P = lambda pts: [(x + a * ux, y - h + b * uy) for a, b in pts]
    if kind == "walk":
        pg.poly(P([(0, 0), (0, 5.6), (4.2, 5.6), (4.2, 4.65), (4.75, 4.65), (4.75, 3.7), (5.3, 3.7), (5.3, 2.75),
                   (5.85, 2.75), (5.85, 1.8), (8.0, 1.8), (8.0, 0.8), (10, 0.8), (10, 0)]), fill=C["structure"], closed=True)
        pg.poly(P([(8.0, 0.8), (10, 0.8), (10, 1.5), (8.0, 1.5)]), fill=C["water"], closed=True)
        pg.line(P([(0, 5.6), (4.2, 5.6)]), C["green_deep"], 0.8)
        pg.line(P([(5.85, 1.8), (8.0, 1.8)]), C["water_deep"], 0.8)
        pg.line(P([(4.2, 5.0), (10, 5.0)]), C["water_deep"], 0.3, dash=(0.8, 0.6))     # Q500 below the square
        icon(pg, "plane", x + 0.4 * ux, y - h + 8.0 * uy, 2.4 * uy)
        cl_marker(pg, x + 6.9 * ux, y - h + 3.6 * uy, str(EVENTS["n"]), mk_colour("cl_place", "place"), 6.5)  # stop 8
    elif kind == "hidden":
        pg.poly(P([(0, 0), (0, 5.6), (10, 5.6), (10, 0)]), fill=C["structure"], closed=True)
        pg.poly(P([(3.2, 0.6), (7.2, 0.6), (7.2, 2.6), (6.4, 3.4), (4.0, 3.4), (3.2, 2.6)]), fill=C["water_light"], closed=True)
        pg.poly(P([(3.2, 0.6), (7.2, 0.6), (7.2, 1.3), (3.2, 1.3)]), fill=C["water"], closed=True)
        pg.line(P([(0, 5.6), (10, 5.6)]), C["ink"], 0.6)
        pg.line(P([(2.0, 5.95), (8.4, 5.95)]), C["water_deep"], 0.9)                   # the water line in the paving
    else:
        pg.poly(P([(0, 2.6), (7.0, 2.6), (7.0, 4.4), (0, 4.4)]), fill=C["ink2"], closed=True)
        pg.poly(P([(7.0, 1.6), (10, 3.5), (7.0, 5.4)]), fill=C["accent"], closed=True)


def hub_card(pg, hb, x, ytop, w, head=True, gs=1.0):
    """v1.11 / v5 / v6 / v7 (round 4, P10.3 P10.4, G-R4-1/7/11): one bridge place in its column under the plans'
    legend, no frame: its locator marker (the number on the key map and over its plan(s)) and real name, its role,
    its existing bus stops (metres to the hub), the later step, the trips, its levels (the dry hub over the sub-hub in
    the bed, the hidden square, or the gateway) as a glyph with its keys, and its places, numbered as on the plan,
    with who they serve, what they grow from and their keywords. v7: bigger type (name 10.5 pt, rows 8 pt, keywords
    7.5 pt) and glyph (24 x 15 mm) in a wider column; laid out from the top by the real line heights.
    v9 (round 5 S9, P10.3 "one per hub, same structure"): every hub's diagram has the same rows in the same order,
    in the same width (p09_items): code + name, role, bus stop(s) with metres, (later step), trips, the levels glyph
    with its keys (v9: the gateway too: its road-out glyph, "GATEWAY OUT" / "no hub square"), then its places (none at
    the gateway). Recorded on its own recorder; exported as one diagram grouped with its plan window.
    v11 (L7, one box per drawing): head=False draws no code disc and no name; p09_items exports them as the card's
    badge + heading (drawing = the card), so the booklet sets them in the box's head row.
    v13 (round 9 BRIEF p9 + U17, PLAN §cause d5 / f4, H4 §1c / §5): the card BODY of a boxed card: gs = the hub
    drawing's (levels glyph) uniform growth (p09_items picks the largest that fills the card's 102 mm); each bus
    stop on one row: name, its lines (BUS_STOPS, when they fit beside it) and the metres; the grows-from chips as
    tags (cl_tag, letter centred); three element groups "card <code> bus" / "drawing" / "places" (the parts the
    booklet's box holds). Returns dict(y = the baseline under the last line, parts = [(part, y top, y bottom)])."""
    tr = hb["transit"]
    code = hub_code(hb)
    y = ytop - 3.6
    parts = []
    if head:
        _b, r_ = cl_marker(pg, x + 2.0, y + 1.1, code, hub_col(hb), 7.5, name="card hub %d" % hub_no(hb))
        tx = x + 2.0 + r_ + 1.4
        pg.tgroup()
        for ln in cl_wrap(hb["title"], 10.5, x + w - tx, True):
            pg.text(ln, tx, y, 10.5, C["ink"], True)
            y -= 4.6
        pg.tgroup(False)
    y0_ = y + 3.6
    with pg.group("hubs", u"card %s bus" % code):
        role = ("MAIN TRANSIT HUB · " if tr else ("walking hub · " if hb["kind"] == "walk" else "")) + hb["role"]
        y = cl_para(pg, role, x, y - 0.3, 8, w, C["accent"] if tr else C["ink2"], tr) - 0.8
        for st in hb["bus_stops"]:
            icon(pg, "bus", x, y + 2.9, 3.6)
            dist = "%d m" % st["m"]
            dw = text_w(dist, 8.5, True)
            pg.text(dist, x + w, y, 8.5, SPINE_C, True, "R")
            room = w - 6.8 - dw                           # v13 (BRIEF p9 "bus line + distance on one row")
            nw_ = text_w(st["name"], 8, True)
            lines_ = (st.get("lines") or u"").strip()
            if lines_ and nw_ + 2.0 + text_w(lines_, 7) <= room:
                pg.text(lines_, x + w - dw - 2.0, y, 7, C["ink2"], False, "R")
            elif lines_:
                BM_NOTE.append(u"p09 card %s: bus lines %s left off the stop row (no room beside %s)" % (
                    code, lines_, st["name"]))
            fit(pg, st["name"], x + 4.8, y, 8, room, C["ink"], True)
            y -= 4.4
        if hb.get("later"):                                # the proposed town-line extension, in accent
            y = cl_para(pg, hb["later"], x + 4.8, y, 7.5, w - 4.8, C["accent"], True)
        y = cl_para(pg, hb["trips"], x + 4.8, y, 7.5, w - 4.8, C["ink2"]) - 1.6
    parts.append(("bus", y0_, y + 1.6))
    gw, gh = 24.0 * gs, 15.0 * gs                          # the levels: a small section with its keys beside it
    yd_ = y + 2.6
    with pg.group("hubs", u"card %s drawing" % code):
        hub_glyph(pg, hb["kind"], x, y + 2.6, gw, gh)      # v9 (P10.3): every hub, the gateway its road out
        if hb["kind"] == "walk":
            kws = [("DRY HUB", True), ("street level, above Q500", False), ("SUB-HUB in the bed", True),
                   ("open Jul-Sep · shut in floods " + cite(SRC_WET), False)]
        elif hb["kind"] == "hidden":
            kws = [("HIDDEN STREAM SQUARE", True), ("water line in the paving over the culvert " + cite(SRC_HIDDEN),
                                                    False),
                   (landmark_name("kizil_avlu").replace(u"i", u"İ").upper() + u" TUNNEL MOUTHS", True),
                   ("a viewing edge", False)]
        else:                                              # v8.2's "GATEWAY OUT · no hub square", as keys
            kws = [("GATEWAY OUT", True), ("no hub square", False)]
        ky = y
        for j, (s_, b_) in enumerate(kws):
            if j and b_:
                ky -= 0.8
            ky = cl_para(pg, s_.strip(), x + gw + 2.0, ky, 7.5, w - gw - 2.0, C["ink"], b_, lead=3.2)
    y = min(y + 2.6 - gh, ky + 3.2 - 0.6) - 4.4
    parts.append(("drawing", yd_, y + 4.4))
    yp_ = y + 3.6
    with pg.group("hubs", u"card %s places" % code):
        for n in hb["stops"]:
            f = [g for g in FUNCS + [EVENTS] if g["n"] == n][0]
            cl_marker(pg, x + 2.4, y + 1.0, str(n), mk_colour("cl_place", "place"), 7.0, r_min=2.2,
                      name="card place %d" % n)
            nx = x + 6.2
            y = cl_para(pg, f["name"], nx, y, 8, x + w - nx, C["ink"], True, lead=3.5)
            cy = y + 1.0                                   # who it serves (dots) and what it grows from (chips)
            group_dots(pg, nx + 1.1, cy, f["who"], r=1.1)
            gx = nx + 9.8
            for g_ in f["grows"]:                          # v13 (S1, H4 §1c): the chip = a tag, letter centred
                cl_tag(pg, g_, gx, cy - 1.4, 3.2, 2.8, GROW_C[g_], C["white"], 7.0)
                gx += 3.7
            y -= 3.8
            words = f["kw"][0] + " · " + f["kw"][1] + (" " + cite(f["src"]) if f.get("src") else "")
            if n == 7:                                     # the entry lies upstream of the hub (chainage, calculated)
                words += " · about %d m upstream of %s" % (int(round((CH["K4"] - FUNCS[6]["ch"]) / 10.0) * 10),
                                                           bridge_name("K4", short=True))
            y = cl_para(pg, words.strip(), nx, y, 7.5, x + w - nx, C["ink"], lead=3.2) - 1.8
    if hb["stops"]:
        parts.append(("places", yp_, y + 1.8))
    return dict(y=y, parts=parts)


# v13 (round 9 BRIEF p9, U17, PLAN §cause d5 / f4; frames p09.5a-e 76 x 102 mm): the boxed hub card. The booklet draws
# the thin grey frame on the frame's mm, the header bar (CARD_BAR_MM) in the hub's colour, the K-tile (a tag) and the
# name (heading) in the head row; the producer draws the body under them at the frame's size. Design values (U17).
CARD_PAD = 1.6                           # mm: the body's inset from the grey frame
CARD_BAR_MM = 1.2                        # mm: the coloured bar across the card's top (U17)
CARD_HEAD_MM = 6.4                       # mm: the head row under the bar (K-tile + name)
CARD_TILE = (5.2, 3.8)                   # mm: the K-tile (w, h)
CARD_TILE_PT, CARD_NAME_PT = 6.5, 8.5    # pt: the tile's code, the name (stepped to 7.5 when it does not fit)
CARD_FRAME = (GRID_INK["rule"], 0.3)     # the grey frame (hex, pt) the booklet draws (H4 §5: B0AC9C, about 0.3 pt)
CARD_KEYS_MIN = 30.0                     # mm: the glyph's keys keep at least this width, so the glyph grows to w - 32
CARD_GS_MAX = 3.0                        # the hub drawing grows at most 3 x (24 x 15 mm -> 72 x 45 mm)


def hub_card_fit(hb, bw, bh):
    """v13 (round 9 d5, BRIEF p9 "the hub drawing in each card grows into the space"): the largest growth gs of the
    hub drawing (levels glyph) at which the card body (width bw) stays within bh mm, by bisection on scratch
    recorders; never below 1 (text and drawing at their v12 sizes). Returns (gs, used mm at gs, used mm at 1)."""
    def used(g):
        n0 = len(BM_NOTE)
        pg_ = Page(420, 297, u"card fit")
        hub_card(pg_, hb, 14.0, 250.0, bw, head=False, gs=g)
        del BM_NOTE[n0:]                                  # a trial's notes are the real draw's: logged once there
        return 250.0 - cl_bbox(pg_, pad=0.0)[1]
    u1 = used(1.0)
    hi = max(1.0, min(CARD_GS_MAX, (bw - 2.0 - CARD_KEYS_MIN) / 24.0))
    if u1 >= bh or hi <= 1.0:
        return 1.0, u1, u1
    if used(hi) <= bh:
        return hi, used(hi), u1
    lo = 1.0
    for _i in range(14):
        mid = 0.5 * (lo + hi)
        if used(mid) <= bh:
            lo = mid
        else:
            hi = mid
    return lo, used(lo), u1


# ------------------------------------------------------------------ page 2: the bridge places in plan, hub by hub
HUB_SQ_ID = dict(K4="K4", K3="K3", IST=u"İstiklal", RED=u"Kızıl Avlu", K5="K5", K6="K6")   # window -> masterplan hub id


def hub_windows(L, hubs):
    """v6 (P09.1, D1): one plan window per hub point, in stream order (the transit hub has two: İstiklal Meydanı and
    Kızıl Avlu): dict(hub, ref = its HUB_PTS key, anchor, name = the place name printed over the plan, no = the
    hub's locator number, stops = its places that have a position [(n, xy)] (each to the nearest window of its
    hub), subs = the sub-hub crossings (stepping stones named after the hub, masterplan_results.json "movement"; v7:
    else the hub square's sub-hub), sq = the masterplan's hub square (v7, P10.6), pts = what the window must hold)"""
    M = L.get("mpmv") or {}
    sq_of = dict((h_.get("id"), h_) for h_ in L.get("hub_sq") or [])
    wins = []
    for hb in hubs:
        for ref in [hb["pt"]] + (["RED"] if hb["id"] == u"İstiklal" else []):
            q = tuple(HUB_PTS[ref])
            nm = landmark_name("istiklal_meydani") if ref == "IST" else (
                landmark_name("kizil_avlu") if ref == "RED" else None)
            wins.append(dict(hub=hb, ref=ref, anchor=q, stops=[], subs=[], pts=[q], name=nm, no=hub_no(hb),
                             sq=sq_of.get(HUB_SQ_ID.get(ref))))
    for w in wins:
        hb = w["hub"]
        w["pts"] += [tuple(st["xy"]) for st in hb["bus_stops"] if st["from_point"] == w["ref"]]
        if w["ref"] == hb["pt"]:
            for c_ in M.get("crossings") or []:
                if c_.get("kind") == "stepping stones" and c_.get("xy") and \
                        str(c_.get("name", "")).split()[-1:] == [hb["id"]]:
                    w["subs"].append(tuple(c_["xy"]))
            sh = (w["sq"] or {}).get("sub_hub")
            if not w["subs"] and sh and sh.get("c"):
                w["subs"].append(tuple(sh["c"]))
        w["pts"] += w["subs"]
        for R_ in (w["sq"] or {}).get("rings") or []:
            w["pts"] += [tuple(p) for p in R_]
    for hb in hubs:
        mine = [w for w in wins if w["hub"] is hb]
        for n in hb["stops"]:
            f_ = [g for g in FUNCS if g["n"] == n and g.get("xy")]
            if f_:
                q = tuple(f_[0]["xy"])
                w = min(mine, key=lambda w_: math.hypot(w_["anchor"][0] - q[0], w_["anchor"][1] - q[1]))
                w["stops"].append((n, q))
                w["pts"].append(q)
    return wins


def hub_plan_layout(f, wins):
    """v6 (P09.1) / v9 (P10.2: one scale) / v10 (round 6, PLAN §3 P-10, U17): the plans sit in the hub cards'
    columns, each above its own card, all at ONE scale. Each window must hold its points (the hub point, its bus
    stops, the sub-hub crossing, the masterplan's hub square, its places) with P2_PLAN_MARGIN round them on the site
    frame's axes; den = the largest standard scale (CL_SCALES) at which every window's own extent fits its column
    share (P9_COL_W, or half of it less P9_COL_GAP for a hub with two windows, the transit hub's İstiklal Meydanı and
    Kızıl Avlu) and P9_PLAN_H. Then every window is widened to its full share and to P9_PLAN_H at that same scale,
    centred on its own points: more of the town is shown, nothing is stretched (P-10 "windows widened to the column
    width at the same scale"). Sets each window's box (page mm, on its own recorder), u0, v0 (frame axes, m),
    size_m, den; returns den."""
    x0, top = P2_PLAN[0], P2_PLAN[1]
    per = {}
    for w in wins:
        per[w["no"]] = per.get(w["no"], 0) + 1
    ext = []
    for w in wins:
        uv = [frame_uv(f, p) for p in w["pts"]]
        ext.append((min(q[0] for q in uv) - P2_PLAN_MARGIN, max(q[0] for q in uv) + P2_PLAN_MARGIN,
                    min(q[1] for q in uv) - P2_PLAN_MARGIN, max(q[1] for q in uv) + P2_PLAN_MARGIN))
        n_ = per[w["no"]]
        w["share_mm"] = (P9_COL_W - P9_COL_GAP * (n_ - 1)) / float(n_)
    for den in CL_SCALES:
        k = 1000.0 / den
        if all((e[1] - e[0]) * k <= w["share_mm"] and (e[3] - e[2]) * k <= P9_PLAN_H for w, e in zip(wins, ext)):
            break
    else:
        BM_NOTE.append("FLAG: p09 hub windows: no standard scale fits the hub columns; recorded at 1:%s" % fmt(den))
    k = 1000.0 / den
    Hm = P9_PLAN_H / k
    for w, e in zip(wins, ext):
        Wm = w["share_mm"] / k
        uc, vc = (e[0] + e[1]) / 2.0, (e[2] + e[3]) / 2.0
        w["u0"], w["v0"] = uc - Wm / 2.0, vc - Hm / 2.0
        w["box"], w["den"], w["size_m"] = (x0, top - P9_PLAN_H, x0 + w["share_mm"], top), den, (Wm, Hm)
    BM_NOTE.append(u"p09 windows: %d windows at 1:%s, each its column share (%s mm) x %.1f mm, centred on its own "
                   u"points (+%.0f m margin)" % (len(wins), fmt(den), u", ".join("%.1f" % w["share_mm"] for w in wins),
                                                 P9_PLAN_H, P2_PLAN_MARGIN))
    return den


def frame_xy(f, u, v):
    """v7: the survey point of the frame-axes point (u, v)"""
    c, s = math.cos(f["ang"]), math.sin(f["ang"])
    return (f["cx"] + c * u - s * v, f["cy"] + s * u + c * v)


def dp_simplify(P, tol):
    """v7 (P10.5): the polyline P simplified (Douglas-Peucker) to tol (same units): no wiggle left along the edge"""
    if len(P) < 3:
        return list(P)
    a, b = P[0], P[-1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(dx, dy) or 1e-9
    i_, dmax = 0, -1.0
    for i in range(1, len(P) - 1):
        d = abs((P[i][0] - a[0]) * dy - (P[i][1] - a[1]) * dx) / ln
        if d > dmax:
            i_, dmax = i, d
    if dmax <= tol:
        return [a, b]
    return dp_simplify(P[:i_ + 1], tol)[:-1] + dp_simplify(P[i_:], tol)


def spine_runs(L):
    """v7 (P10.5: no squiggle, one continuous purposeful line): the streamside spine as runs (survey m): the
    masterplan's spine pieces (edge, deck, over; else the city link's own spine line, flagged), joined where one ends
    within 3 m of the next one's start, simplified to SPINE_SIMPLIFY_M; once per run (L["spine_runs"])"""
    if L.get("spine_runs") is not None:
        return L["spine_runs"]
    pcs = L.get("mp_spine") or [("over" if pid == "B" else "edge", R_) for pid, R_ in spine_line(L)]
    if not L.get("mp_spine"):
        BM_NOTE.append("FLAG: no masterplan spine pieces (masterplan_results.json): p09's plans draw the city link's "
                       "own spine line")
    runs = []
    for _kd, R_ in pcs:
        R_ = [tuple(p) for p in R_]
        if len(R_) < 2:
            continue
        if runs and math.hypot(runs[-1][-1][0] - R_[0][0], runs[-1][-1][1] - R_[0][1]) < 3.0:
            runs[-1] += R_[1:]
        elif runs and math.hypot(runs[-1][-1][0] - R_[-1][0], runs[-1][-1][1] - R_[-1][1]) < 3.0:
            runs[-1] += R_[::-1][1:]
        else:
            runs.append(list(R_))
    L["spine_runs"] = [dp_simplify(R_, SPINE_SIMPLIFY_M) for R_ in runs]
    return L["spine_runs"]


def _cl_gh_minus(S, C):
    """v9.2: S minus C as rings (Greiner-Hormann as _sc_gh, with S's entry flags inverted so the walk keeps the parts
    of S outside C and runs along C's edge inside S); None when a vertex lies on the other's edge (caller perturbs)"""
    sl, cl = _sc_list(S), _sc_list(C)
    hits = []
    for i, s0 in enumerate(sl):
        s1 = sl[(i + 1) % len(sl)]
        for j, c0 in enumerate(cl):
            c1 = cl[(j + 1) % len(cl)]
            dx, dy = s1.x - s0.x, s1.y - s0.y
            ex, ey = c1.x - c0.x, c1.y - c0.y
            den = dx * ey - dy * ex
            if abs(den) < 1e-15:
                continue
            a = ((c0.x - s0.x) * ey - (c0.y - s0.y) * ex) / den
            b = ((c0.x - s0.x) * dy - (c0.y - s0.y) * dx) / den
            if -1e-9 <= a <= 1.0 + 1e-9 and -1e-9 <= b <= 1.0 + 1e-9:
                if a < 1e-7 or a > 1.0 - 1e-7 or b < 1e-7 or b > 1.0 - 1e-7:
                    return None
                hits.append((i, a, j, b, s0.x + dx * a, s0.y + dy * a))
    if not hits:
        if _sc_pip(S[0][0], S[0][1], C):
            return []                                     # wholly in the water
        return [list(S)]                                  # clear of it (a water ring wholly inside S is left as is)
    by_s, by_c = {}, {}
    for i, a, j, b, x, y in hits:
        ns, nc = _ScNode(x, y, True, a), _ScNode(x, y, True, b)
        ns.nb, nc.nb = nc, ns
        by_s.setdefault(i, []).append(ns)
        by_c.setdefault(j, []).append(nc)
    for base, groups in ((sl, by_s), (cl, by_c)):
        for i, grp in groups.items():
            grp.sort(key=lambda nd: nd.alpha)
            v, end = base[i], base[(i + 1) % len(base)]
            for nd in grp:
                nd.prv, nd.nxt = v, end
                v.nxt = nd
                end.prv = nd
                v = nd
    for start, other, inv in ((sl[0], C, True), (cl[0], S, False)):
        status = not _sc_pip(start.x, start.y, other)
        if inv:
            status = not status                           # S: walk forward where it LEAVES the water
        v = start
        while True:
            if v.inter:
                v.entry = status
                status = not status
            v = v.nxt
            if v is start:
                break
    out = []
    for h0 in [nd for grp in by_s.values() for nd in grp]:
        if h0.seen:
            continue
        ring, v, guard = [(h0.x, h0.y)], h0, 0
        while True:
            v.seen = True
            v.nb.seen = True
            fwd = v.entry
            while True:
                v = v.nxt if fwd else v.prv
                ring.append((v.x, v.y))
                if v.inter:
                    break
            v = v.nb
            guard += 1
            if v.seen or guard > 10000:
                break
        if len(ring) > 1 and abs(ring[0][0] - ring[-1][0]) < 1e-9 and abs(ring[0][1] - ring[-1][1]) < 1e-9:
            ring.pop()
        if len(ring) >= 3:
            out.append(ring)
    return out


def cl_ring_minus(R, C):
    """v9.2: one ring minus one water ring: [ring, ...]; perturbs R by a hair when a vertex falls on an edge (as
    _sc_poly_and); after 6 tries R is kept whole (the zones line then still reports it)"""
    S = [tuple(p[:2]) for p in _sc_open(list(R))]
    C = [tuple(p[:2]) for p in _sc_open(list(C))]
    if len(S) < 3 or len(C) < 3:
        return [S] if len(S) >= 3 else []
    for k in range(6):
        r = _cl_gh_minus(S, C)
        if r is not None:
            return [x for x in r if abs(_sc_area(x)) > 1e-6]
        d = 1e-6 * (k + 1)
        S = [(p[0] + d * ((i * 7919) % 13 - 6) / 6.0, p[1] + d * ((i * 104729) % 11 - 5) / 5.0)
             for i, p in enumerate(S)]
    return [S]


def cl_items_off_water(items, water, keep_cols=()):
    """v9.2 (run warning "WARNING p10 zones over_water_area"): the fill items of a project layer cut back to the
    water's edge: each ring minus every water ring (survey m) it reaches, so no field is filled over the stream;
    fills whose colour is in keep_cols (in the water by design, e.g. the stepping stones) and every non-fill item
    pass unchanged. Clipping only: nothing is moved or added."""
    if not water:
        return list(items)
    keep = set(str(c).upper() for c in keep_cols or ())
    wb = [(W, (min(p[0] for p in W), min(p[1] for p in W), max(p[0] for p in W), max(p[1] for p in W)))
          for W in water if len(W) >= 3]
    out = []
    for it in items:
        if it[0] != "fill" or str(it[2]).upper() in keep:
            out.append(it)
            continue
        rs = []
        for R in it[1]:
            pcs = [R] if len(R) >= 3 else []
            for W, b in wb:
                nxt = []
                for P in pcs:
                    x0, y0 = min(p[0] for p in P), min(p[1] for p in P)
                    x1, y1 = max(p[0] for p in P), max(p[1] for p in P)
                    nxt += cl_ring_minus(P, W) if not (b[2] < x0 or b[0] > x1 or b[3] < y0 or b[1] > y1) else [P]
                pcs = nxt
            rs += pcs
        if rs:
            out.append(("fill", rs) + tuple(it[2:]))
    return out




def hub_plan(pg, L, f, w):
    """v6 / v7 (round 4, P10.2 P10.5 P10.6, G-R4-1/4/7; spec S5): one bridge place in plan at the row's scale on
    the site frame's axes, clipped to its window with a 0.25 pt neatline, through THE draw order (cl_map): the muted
    base and the covered course dashed; the D9 tint of the masterplan's hub square with its edge (P10.6); the road
    changes and the later town bus line; the streamside spine as ONE simplified solid line (P10.5; runs shorter than
    SPINE_MIN_M in the window dropped; the streamside walks are not drawn: their loose stubs); the hub square's trees;
    footbridges and the sub-hub stepping stones spanning the water; the study line; proposals clipped to the study
    area. On top: the existing bus stops, the hub's locator marker, the places (markers in the place colour, nudged
    clear of each other), the summer bed events at the sub-hub; landmark names where a spot is free. Over the plan:
    its locator number and real name (P10.2). Returns the set of things drawn (for the legend).
    v9 (round 5 S9, P10.2, G-R5-8/12): recorded on its own recorder and exported by p09_items as one true-scale
    drawing (cl_drawing cuts it to the window); its number and name are a heading item, no neatline is drawn."""
    x0, y0, x1, y1 = w["box"]
    den = w["den"]
    k = 1000.0 / den
    m_mm = den / 1000.0
    T = frame_T(f, x0, y0, den, w["u0"], w["v0"])
    sbox = frame_box(f, w["u0"], w["v0"], w["u0"] + (x1 - x0) / k, w["v0"] + (y1 - y0) / k)
    inside = lambda q: x0 <= q[0] <= x1 and y0 <= q[1] <= y1
    frame = (x0 + 0.8, y0 + 0.8, x1 - 0.8, y1 - 0.8)
    MAP = "plan %s %s" % (w["no"], w["ref"])
    M = L.get("mpmv") or {}
    hb = w["hub"]
    seen = set()
    # v9: its locator number and real name over the plan are a heading item (p09_items), not drawn here
    pg.keep(w["box"], "map", MAP)
    # base extra: the covered course
    P, cov = stream_ref()
    covered = [("line", R_, C["water_deep"], 0.8, [1.6, 0.9], 1.0) for c_, R_ in clip_runs(P, sbox, cov) if c_]
    if covered:
        seen.add("covered")
    study = cl_study()
    proj = dict(proj_tint=[], proj_lines=[], proj_vegetation=[], proj_marks=[])
    trees_ = []
    sq = w.get("sq") or {}
    rings = [[tuple(p) for p in R_] for R_ in sq.get("rings") or [] if len(R_) >= 3]
    if rings:                                             # P10.6: the masterplan's hub square, tinted (D9) + its edge
        proj["proj_tint"] += ml_tint(rings, colour=SQ_FILL, alpha=SQ_ALPHA)
        proj["proj_lines"] += [("line", R_ + [R_[0]], SQ_EDGE, 0.35, None, 1.0) for R_ in rings]
        tr_ = max(1.2 * m_mm, 3.5)                        # a crown >= 1.2 mm across on the page (drawing rule)
        for i_, q in enumerate(sq.get("trees") or []):    # v9.1 (G-R5-6): the plant module's plane, not a 16-gon
            trees_.append(cl_plane_plan(q, 2.0 * tr_, i_))   # v10 (G6-9/10): drawn after the map, one group each
        seen.add("square")
        if sq.get("trees"):
            seen.add("trees")
    for rd in M.get("roads") or []:
        ch, R_ = rd.get("change", "kept"), rd.get("xy") or []
        if ch in ROAD_STYLE and len(R_) >= 2:
            col_, lw_ = ROAD_STYLE[ch]
            proj["proj_lines"] += [("line", [tuple(p) for p in R_], C["white"], lw_ + 0.6, None, 1.0),
                                   ("line", [tuple(p) for p in R_], col_, lw_, None, 1.0)]
            if any(inside(T(p)) for p in R_):
                seen.add("road_" + ch)
    for rt in M.get("routes") or []:
        R_ = rt.get("xy") or []
        if len(R_) >= 2:
            Q = pl_offset([tuple(p) for p in R_], 1.0 * m_mm)
            proj["proj_lines"] += [("line", Q, C["white"], 1.1, None, 1.0), ("line", Q, BUS_C, 0.5, list(BUS_DASH), 1.0)]
            if any(inside(T(p)) for p in Q):
                seen.add("bus")
    for R_ in spine_runs(L):                              # P10.5: one solid line; no stub under SPINE_MIN_M
        for run in sc_lines(R_, study, "p09") if study else [R_]:
            vis = sum(math.hypot(b_[0] - a_[0], b_[1] - a_[1]) for _c, Q in clip_runs([T(p) for p in run],
                                                                                       (x0, y0, x1, y1))
                      for a_, b_ in zip(Q, Q[1:])) * m_mm
            if vis >= SPINE_MIN_M:
                proj["proj_lines"] += [("line", run, C["white"], 1.8, None, 1.0), ("line", run, SPINE_C, 1.2, None, 1.0)]
                seen.add("spine")
    try:
        wring = basemap_water_rings(basemap_items("base", box=sbox, scale_den=den))
    except Exception:
        wring = []
    for c_ in M.get("crossings") or []:
        q, kd = c_.get("xy"), c_.get("kind")
        if not q or kd not in ("footbridge", "stepping stones") or not inside(T(q)):
            continue
        d_ = stream_dir(q)
        nrm = (-d_[1], d_[0])
        sp = water_span(q, nrm, wring) or ((q[0] - nrm[0] * 14.0, q[1] - nrm[1] * 14.0),
                                           (q[0] + nrm[0] * 14.0, q[1] + nrm[1] * 14.0))
        if kd == "stepping stones":
            n_ = max(3, int(math.hypot(sp[1][0] - sp[0][0], sp[1][1] - sp[0][1]) / (1.4 * m_mm)))
            rs = 0.45 * m_mm
            for i in range(n_):
                t_ = (i + 0.5) / n_
                sx, sy = sp[0][0] + (sp[1][0] - sp[0][0]) * t_, sp[0][1] + (sp[1][1] - sp[0][1]) * t_
                ring_ = [(sx + rs * math.cos(a_ * math.pi / 6.0), sy + rs * math.sin(a_ * math.pi / 6.0)) for a_ in range(12)]
                proj["proj_marks"] += [("fill", [ring_], C["ink"], 1.0, True),
                                       ("line", ring_ + [ring_[0]], C["white"], 0.15, None, 1.0)]
            seen.add("stones")
        else:
            proj["proj_marks"] += [("line", list(sp), C["white"], 1.4, None, 1.0), ("line", list(sp), C["ink"], 0.8, None, 1.0)]
            seen.add("footbridge")
    try:                                                  # v9.2: the stream's rings exactly as map_draw finds them
        wl_ = [it for it in list(ml_base(sbox, den)) + list(covered) if ml_layer_of(it) == "water"]
        wr_ = basemap_water_rings(wl_) + [R_ for it in wl_ if it[0] == "fill" and it[2] not in (BM_COL["water"],)
                                          for R_ in it[1] if len(R_) >= 3]
    except Exception as ex_:
        BM_NOTE.append("FLAG p09 %s: water rings not read (%s: %s): fields not cut to the water edge"
                       % (MAP, type(ex_).__name__, ex_))
        wr_ = []
    for k_ in ML_FIELD_LAYERS:                            # v9.2: no field filled over the stream (clip only)
        if proj.get(k_):
            proj[k_] = cl_items_off_water(proj[k_], wr_, keep_cols=[C["ink"]])
    nb, _st = cl_map(pg, "p09", T, sbox, den, proj, base_extra=covered, clip=True,   # v9: cut to the window on export
                     legend_cols=[ML_TINT, SQ_FILL, C["green_mid"], C["ink"]] + sorted(CL_TREE_COLS),
                     water_ok=[C["ink"]])                 # stones: in the bed; v9.1: + the plane's own colours
    # v10 (round 6, G6-9 + G6-10): each hub-square tree its own group, named by its species (the masterplan's
    # planes, PLANE_NAME, source SRC_PLANE); drawn over the map's project layers, under the markers
    for i_, its_ in enumerate(trees_):
        with pg.group("trees", u"tree %s %d · %s" % (w["key"] if "key" in w else w["no"], i_ + 1, PLANE_NAME)):
            for it in its_:
                if it[0] == "fill":
                    pg.path([[T(p_) for p_ in R_] for R_ in it[1]], fill=it[2])
                elif it[0] == "line":
                    pg.line([T(p_) for p_ in it[1]], it[2], it[3])
    CL_TREES[0] += len(trees_)

    if nb:
        seen.add("base")
    # on top (inside the clip): the existing bus stops, the hub, the places, the bed events
    for st in hb["bus_stops"]:
        if st["from_point"] != w["ref"]:
            continue
        sx, sy = T(st["xy"])
        if inside((sx, sy)):
            disc(pg, sx, sy, 1.0, C["white"], C["water_deep"], 0.3)
            pg.keep((sx - 1.2, sy - 1.2, sx + 1.2, sy + 1.2), "marker", "stop %s" % st["name"])
            seen.add("stop")
    hx, hy_ = T(w["anchor"])
    with pg.group("hubs", u"hub " + hub_code(hb)):
        cl_marker_free(pg, hx, hy_, hub_code(hb), hub_col(hb), 7.0, frame=frame, allow=(MAP,), name="hub " + MAP)
    seen.add("hub_" + ("transit" if hb["transit"] else hb["kind"]))
    for n, q in w["stops"]:
        px, py = T(q)
        if inside((px, py)):
            cl_marker_free(pg, px, py, str(n), mk_colour("cl_place", "place"), 7.0, frame=frame, allow=(MAP,),
                           name="place %d %s" % (n, MAP))
            seen.add("place")
    for q in w["subs"]:
        px, py = T(q)
        if inside((px, py)):
            cl_marker_free(pg, px, py, str(EVENTS["n"]), mk_colour("cl_place", "place"), 7.0, frame=frame,
                           allow=(MAP,), name="events %s" % MAP)
            seen.add("events")
    try:
        names = basemap_names(sbox)
    except Exception:
        names = []
    skip = [s_.lower() for s_ in (hb["title"], landmark_name("istiklal_meydani"), landmark_name("kizil_avlu"),
                                  u"Köprü")]
    for nm_, q in names:                                  # landmarks inside the plan, where a spot is free
        px, py = T(q)
        if inside((px, py)) and not any(s_ in nm_.lower() for s_ in skip):
            with pg.group("labels", u"name " + nm_):     # v11 (L7): every landmark name handed to the booklet
                cl_place(pg, nm_, (px, py), 7, C["ink2"], False, 0.6, frame, (MAP,))
    return seen


SPINE_WALK_C = hue("MOV", 3)              # v10 (G6-6): the masterplan's streamside walks, movement r3
MAIN_ROAD_C = hue("MOV", 2)               # v10 (G6-6): the main road Bankalar - Kınık Cd., movement r2


def spine_map(pg, L, hubs, f):
    """v10 (round 6, BRIEF §5 + §6 row 9, PLAN §4: SON page9 = c493fac page_spine, the map part restored on today's
    draw order): the whole study area on one map on the site frame's axes, at the largest standard scale at which
    the study area and the hubs fit P9_MAP (recorded at it; the booklet prints the true scale with its bar): the
    muted base through cl_map (the covered course dashed, the study line), the masterplan's streamside walks across
    the whole project thin (how the spine carries on), the main road, the streamside spine K4-K5 bold with an
    arrowhead at each end; on top the existing bus stops, the hubs as markers with their codes (HUB_CODE, as on the
    cards) and the places as numbered markers (as on the cards), the stream's name where a spot is free. No legend,
    north arrow, scale bar or neatline here (the booklet's: legend in the side column, G6-4). Every element in its
    own group (G6-9). Returns dict(box, den, seen (the legend keys drawn)).
    v13 (round 9 G9-4, ADDENDUM §0, cause b2 / d4, frame p09.2 292 x 56 mm): an M map like p08: focus = the study
    area + the hubs, 30 m round (v12's box, cl_focus); drawn at the §0 true scale of that focus in p09.2
    (cl_r9_scale; v12's fixed 1:10,000 and its SON-frame WARNING are gone) over the context window r9_window, base
    mode "context"; the stream named by the base's "SELİNOS ÇAYI". Also returns sc, focus, window and base."""
    study = cl_study()
    focus = cl_focus(f, hubs)
    sc = cl_r9_scale(f, "p09.2", focus)
    u0w, v0w, u1w, v1w = sc["win"]
    den = sc["den"]
    k = 1000.0 / den
    x0, y0 = 14.0, 150.0
    mw_, mh_ = (u1w - u0w) * k, (v1w - v0w) * k
    T = frame_T(f, x0, y0, den, u0w, v0w)
    box_ = (x0, y0, x0 + mw_, y0 + mh_)
    frame = (x0 + 1.0, y0 + 1.0, x0 + mw_ - 1.0, y0 + mh_ - 1.0)
    inside = lambda q: frame[0] <= q[0] <= frame[2] and frame[1] <= q[1] <= frame[3]
    MAP = "map p09"
    pg.keep(box_, "map", MAP)
    sbox = sc["sbox"]
    seen = set()
    P, cov = stream_ref()
    covered = [("line", R_, C["water_deep"], 0.8, [1.6, 0.9], 1.0) for c_, R_ in clip_runs(P, sbox, cov) if c_]
    if covered:
        seen.add("covered")
    lines = []
    walks = L.get("walks") or []
    if not walks:
        BM_NOTE.append("FLAG: no masterplan streamside walks (masterplan_results.json, option A): p09's spine map "
                       "shows the spine K4-K5 only")
    for W_ in walks:
        lines.append(("line", [tuple(p) for p in W_], SPINE_WALK_C, 0.5, None, 1.0))
        seen.add("walks")
    for R_ in [MAIN_SPINE]:
        lines.append(("line", [tuple(p) for p in R_], MAIN_ROAD_C, 0.7, None, 1.0))
        seen.add("main_road")
    allp = []
    for _pid, R_ in spine_line(L):
        allp += list(R_) if not allp else list(R_[1:])
    if len(allp) >= 2:
        lines += [("line", allp, C["white"], 2.2, None, 1.0), ("line", allp, SPINE_C, 1.4, None, 1.0)]
        seen.add("spine")
    nb, _st = cl_map(pg, "p09", T, sbox, den, {"proj_lines": lines}, base_extra=covered, clip=False,
                     legend_cols=[ML_TINT], ring=sc["ring"])
    base = CL_LAST_BASE[0]
    if nb:
        seen.add("base")
    if len(allp) >= 2:
        Q = [T(p) for p in allp]
        with pg.group("paths", u"streamside spine K4-K5"):
            arrow_head(pg, Q[1], Q[0], SPINE_C, 2.6)
            arrow_head(pg, Q[-2], Q[-1], SPINE_C, 2.6)
        pg.keep(Q, "line", "spine")
    # on top: the existing bus stops, the hubs (codes), the places (numbers as on the cards)
    for hb in hubs:
        for st in hb["bus_stops"]:
            sx, sy = T(st["xy"])
            if inside((sx, sy)):
                with pg.group("hubs", u"bus stop " + st["name"]):
                    disc(pg, sx, sy, 0.9, C["white"], C["water_deep"], 0.3)
                pg.keep((sx - 1.1, sy - 1.1, sx + 1.1, sy + 1.1), "marker", "stop %s" % st["name"])
                seen.add("stop")
    for hb in hubs:
        for ref in [hb["pt"]] + (["RED"] if hb["id"] == u"İstiklal" else []):
            hx, hy = T(HUB_PTS[ref])
            if inside((hx, hy)):
                with pg.group("hubs", u"hub %s %s" % (hub_code(hb), ref)):
                    cl_marker_free(pg, hx, hy, hub_code(hb), hub_col(hb), 7.0, frame=frame, allow=(MAP,),
                                   name="spine hub %s %s" % (hub_code(hb), ref))
                seen.add("hub_" + ("transit" if hb["transit"] else hb["kind"]))
    for f_ in FUNCS:
        if f_.get("xy"):
            px, py = T(f_["xy"])
            if inside((px, py)):
                with pg.group("hubs", u"place %d %s" % (f_["n"], f_["name"])):
                    cl_marker_free(pg, px, py, str(f_["n"]), mk_colour("cl_place", "place"), 6.5, frame=frame,
                                   allow=(MAP,), name="spine place %d" % f_["n"])
                seen.add("place")
    # v13 (G9-4 f): the stream's name is the base's "SELİNOS ÇAYI" (layer f), so v12's own label is not set here
    BM_NOTE.append(u"p09 spine map: focus %.0f x %.0f m, window %.0f x %.0f m at 1:%s, %.0f x %.0f mm (frame p09.2)" % (
        focus[2] - focus[0], focus[3] - focus[1], u1w - u0w, v1w - v0w, fmt(den), mw_, mh_))
    return dict(box=box_, den=den, seen=seen, u0=u0w, v0=v0w, sc=sc, focus=focus, window=sc["win"], base=base)


def p09_legend_rows(seen, cards=False):
    """v10 (round 6, PLAN §3 P-10 "one merged legend in the side column"): the spine map's rows (SON page9) and the
    plans' rows (p10_legend_rows), each once, grouped by category (common/hues.py legend_group when it reads the
    category of a row, else this order: water, movement, public life, people groups, grows-from chips).
    v13 (round 9 p09.3 / p09.6, U17): cards=False = the side legend (the spine map's rows; the context classes are
    added by p09_items, so the stream's fill row is theirs); cards=True = the card key line under the cards (SON
    page9's "who · grows from · bed events" line): the people groups, the grows-from chips and the summer bed events"""
    pc = mk_colour("cl_place", "place")
    ent = []
    if "covered" in seen and not cards:
        ent.append((sw_line(C["water_deep"], 0.8, (1.6, 0.9)), place_name("stream") + ", covered", "WAT", 2))
    if not cards:
        ent.append((sw_line(BM_STUDY_LINE["colour"], BM_STUDY_LINE["width_mm"], tuple(BM_STUDY_LINE["dash_mm"])),
                    "study area", "ANN", 0))
    if cards:
        seen = set(s_ for s_ in seen if s_ == "events")   # the card key line: only its own rows below
    if "spine" in seen:
        ent.append((sw_line(SPINE_C, 1.4, arrow=True), "streamside spine, K4 to K5", "MOV", 1))
    if "main_road" in seen:
        ent.append((sw_line(MAIN_ROAD_C, 0.7), u"main road: " + landmark_name("bankalar_caddesi") + u" - " +
                    landmark_name("kinik_caddesi"), "MOV", 2))
    if "walks" in seen:
        ent.append((sw_line(SPINE_WALK_C, 0.5), "streamside walks, whole project", "MOV", 3))
    for ch, rk in (("pedestrian", 1), ("calmed", 2), ("relocated", 2), ("shared", 3)):
        if "road_" + ch in seen:
            ent.append((sw_line(ROAD_STYLE[ch][0], ROAD_STYLE[ch][1]), ROAD_WORD[ch], "MOV", rk))
    if "bus" in seen:
        ent.append((sw_line(BUS_C, 0.5, BUS_DASH), "town bus line, later step", "MOV", 1))
    if "footbridge" in seen:
        ent.append((sw_mark(lambda p_, x, y: p_.line([(x, y - 1.2), (x, y + 1.2)], C["ink"], 0.8)), "new footbridge",
                    "MOV", 1))
    if "stones" in seen:
        ent.append((sw_mark(lambda p_, x, y: [disc(p_, x + d_, y, 0.45, C["ink"]) for d_ in (-1.6, 0.0, 1.6)]),
                    "sub-hub crossing: stepping stones", "MOV", 2))
    for hb in ([] if cards else hub_list()):              # v10 (Aras 4 Nov 18:28 "explain those hub codes"): one
        kd = "transit" if hb["transit"] else hb["kind"]  # row per hub: its code = its bridge / place (names table)
        word = {"transit": u"main transit hub", "walk": u"walking hub", "gateway": u"gateway out of town"}.get(kd, u"hub")
        ent.append((sw_mark(lambda p_, x, y, hb=hb: cl_marker(p_, x, y, hub_code(hb), hub_col(hb), 7.0,
                                                               name="legend hub " + hub_code(hb))),
                    u"%s = %s · %s" % (hub_code(hb), hb["title"], word),
                    "PUB" if kd != "gateway" else "CTX", 1 if kd == "transit" else 2))
    if "square" in seen:
        ent.append((lambda p_, b: p_.rect(b[0], b[1], b[2] - b[0], b[3] - b[1], fill=tint_hex(SQ_FILL, 1.0 - SQ_ALPHA),
                                          stroke=SQ_EDGE, lw=0.35), "dry hub square (masterplan)", "PUB", 3))
    if not cards:
        ent.append((sw_mark(lambda p_, x, y: cl_marker(p_, x, y, "1", pc, 7.0, name="legend place")),
                    "place, numbered as on its card", "PUB", 3))
    if "events" in seen:
        ent.append((sw_mark(lambda p_, x, y: cl_marker(p_, x, y, str(EVENTS["n"]), pc, 7.0, name="legend events")),
                    EVENTS["name"].lower().capitalize() + ", Jul-Sep, at the sub-hub in the bed", "PUB", 3))
    if "stop" in seen:
        ent.append((sw_mark(lambda p_, x, y: disc(p_, x, y, 1.0, C["white"], C["water_deep"], 0.3)),
                    "existing bus stop (card: metres to the hub)", "CTX", 2))
    if "trees" in seen:
        ent.append((sw_mark(lambda p_, x, y: disc(p_, x, y, 1.0, pla_colours("plane")["fill"])),
                    (u"its trees: " + PLANE_NAME + u", watered from storage " + cite(SRC_PLANE)).strip(), "GRN", 1))
    for g_, rk in ((("T", 1), ("L", 2), ("S", 3)) if cards else ()):
        ent.append((sw_mark(lambda p_, x, y, c=GROUP[g_][1]: disc(p_, x, y, 1.0, c)), GROUP[g_][0], "PUB", rk))
    for g_ in ("WEAH" if cards else ""):                  # v13 (S1): the chip's letter centred (cl_tag)
        ent.append((lambda p_, b, g_=g_: cl_tag(p_, g_, b[0] + 1.0, b[1] - 0.2, 3.0, 2.6, GROW_C[g_], C["white"], 7.0),
                    u"grows from " + GROWS[g_], {"W": "WAT", "E": "WAT", "A": "AGR", "H": "HER"}[g_], 2))
    try:                                                  # G6-6: by category, then rank (common/hues.py)
        ann_ = [e_ for e_ in ent if e_[2] == "ANN"]       # the study line is an annotation, not a category: first
        rest_ = [e_ for e_ in ent if e_[2] != "ANN"]
        lg_ = legend_group([dict(cat=e_[2], rank=e_[3], i=i_) for i_, e_ in enumerate(rest_)])
        ent = ann_ + [rest_[d_["i"]] for d_ in lg_]
    except Exception as ex_:
        wn_warn(None, "legend", u"p09 legend not sorted by category (%s: %s)" % (type(ex_).__name__, ex_))
    try:
        if not cards:
            hue_log("p09", log=CL_LOG)
    except Exception:
        CL_LOG.append(u"legend p09 hues=table rows=%d" % len(ent))
    return [(e_[0], e_[1]) for e_ in ent]


def p10_flood(pg, L):
    """v1.6 / v7 (the flood rule as a stair of its three levels, highest first, each level's rules on its step) /
    v10 (round 6, BRIEF §3 last row + §6 row 9 U16): language SKETCH (it explains an idea: what may stand on each
    level), r06_S02 traits: not to scale; flat beige soil (SK_SOIL) as one stair under a thick black ground line
    (SK_LINE); the water as a flat blue band in the bed; short captions. Enlarged to its page 9 frame P9_FLOOD (the
    U16 "empty half") with the text kept at 7-8 pt: steps 18 mm wide, rows 15 mm apart, the rules' column from
    120 mm. Recorded on pg (a diagram in mm); returns its heading."""
    fx, fy0, fst = 14.0, 64.0, 15.0
    nf, sw_ = len(FLOOD), 18.0
    yb_ = fy0 - (nf - 1) * fst - 8.0
    tx_, rx = fx + nf * sw_ + 5.0, fx + 120.0
    rw = fx + P9_FLOOD[0] - rx - 6.0                       # the rules' text width
    prof = [(fx, yb_)]                                     # the stair: bank top (left) down to the bed (right)
    for i in range(nf):
        t_ = fy0 - i * fst + 3.0
        prof += [(fx + i * sw_, t_), (fx + (i + 1) * sw_, t_)]
    prof.append((fx + nf * sw_, yb_))
    with pg.group("ground", u"flood rule soil"):
        pg.poly(prof, fill=SK_SOIL, closed=True)
    bed_t = fy0 - (nf - 1) * fst + 3.0
    with pg.group("water", u"flood rule bed water"):
        pg.rect(fx + (nf - 1) * sw_, bed_t, sw_, 1.6, fill=hue("WAT", 3))
    with pg.group("ground", u"flood rule ground line"):
        pg.line(prof[1:-1], SK_LINE[0], SK_LINE[1])
    for i in range(nf):
        j = nf - 1 - i                                    # its FLOOD row: the bank top first
        lev, wet, rules, wsrc = FLOOD[j]
        y = fy0 - i * fst
        t_ = y + 3.0
        with pg.group("labels", u"flood rule %s" % lev):
            pg.line([(fx + (i + 1) * sw_ + 0.8, t_), (tx_ - 1.0, t_)], C["ink2"], 0.2, dash=(0.6, 0.5))
            pg.text(lev, tx_, y + 1.2, 8, C["ink"], True)
            for jj, kk in enumerate(wet):
                fit(pg, (kk + (" " + cite(wsrc) if jj == len(wet) - 1 else "")).strip(), tx_, y - 2.4 - jj * 3.2, 7,
                    rx - tx_ - 3.0, C["ink2"])
            for jj, (ic, kk) in enumerate(rules):
                icon(pg, ic, rx, y + 4.0 - jj * 4.8, 4.2)
                fit(pg, kk, rx + 6.0, y + 1.2 - jj * 4.8, 7, rw, C["ink"])
    CL_LOG.append(u"section p09 flood SKETCH (r06_S02 traits: beige soil, thick ground line, flat water)")
    return (u"What stands where: the flood rule " + cite(SRC_RULES)).strip()


def p10_bank(pg, L):
    """v1.6 / v7 (booklet p.10 (3)): which bank the spine takes, per piece, from this run's vote. v9: recorded on pg
    (a diagram in mm); returns its heading.
    v13 (round 9 d5, BRIEF G9-2 C, frame p09.8 110 x 66 mm with its heading): drawn at the frame's size: the chart
    box = 110 x (66 - CL_HEAD_MM) mm, the rows spread over its height (row step and bar thickness grow, text keeps
    its size), the bars' lengths set to the width (home floors 39 mm, 3+ floors the rest, as v12's 38 : 22).
    Returns (heading, the chart box in page mm)."""
    # (3) which bank: per piece a glyph of the bank the spine takes, then paired bars NE / SW (people = home floors,
    # modern = buildings of 3+ floors, within 250 m)
    wh_ = r9_wh("p09.8") or (110.0, 66.0)
    W, Hc = wh_[0], wh_[1] - CL_HEAD_MM
    bkx, ytop = P2_BANK[0], P2_LOW                       # the recorder's chart box: left x, top y (page mm, y up)
    n_ = max(1, len(SPINE))
    HEAD_R, FOOT_R = 5.0, 5.0                             # mm: the column heads' row, the footnote's row
    bst = (Hc - HEAD_R - FOOT_R) / float(n_)              # the row step (v12: 12 mm)
    sv = max(1.0, bst / 12.0)                             # bars and offsets grow with the rows (C: plot fills)
    COL_F, LEN_F = 28.0, 39.0                             # home floors: bar start, longest bar (mm)
    COL_M = COL_F + LEN_F + 12.0                          # 3+ floors: bar start (room for "NE 597" after the bar)
    LEN_M = max(10.0, W - COL_M - 9.0)                    # its longest bar (room for "SW 31")
    pg.text("home floors", bkx + COL_F, ytop - 3.2, 7, C["ink2"], True)
    fit(pg, "buildings of 3+ floors", bkx + COL_M, ytop - 3.2, 7, W - COL_M, C["ink2"], True)
    fmax = max([1.0] + [float(L["votes"][pc["id"]][b]["people_floors"]) for pc in SPINE for b in ("NE", "SW")])
    mmax = max([1.0] + [float(L["votes"][pc["id"]][b]["modern_3plus"]) for pc in SPINE for b in ("NE", "SW")])
    for r_, pc in enumerate(SPINE):
        rc = ytop - HEAD_R - r_ * bst - 3.0 * sv          # the row's centre line
        v = L["votes"][pc["id"]]
        bank, why = bank_of(v)
        auto = pc.get("side") == "auto"
        side = bank if auto else "over"
        pg.text(pc["id"], bkx, rc - 1.2, 9, SPINE_C if auto else C["ink"], True)
        gx0, gx1 = bkx + 6.0, bkx + 20.0                  # the glyph: the stream, the spine on its bank
        pg.rect(gx0, rc - 0.9 * sv, gx1 - gx0, 1.8 * sv, fill=C["water"])
        pg.text("NE", gx1 + 0.8, rc + 1.0 * sv, 7, C["ink2"])           # v7: 6 -> 7 pt (G-R4-1 minimum on p.10)
        pg.text("SW", gx1 + 0.8, rc - 3.1 * sv, 7, C["ink2"])
        ys_ = {"NE": rc + 2.3 * sv, "SW": rc - 2.3 * sv}.get(side, rc)
        pg.line([(gx0, ys_), (gx1, ys_)], C["white"], 1.8)
        pg.line([(gx0, ys_), (gx1, ys_)], SPINE_C, 1.2)
        for j, b in enumerate(("NE", "SW")):
            by_ = rc + 0.4 * sv - j * 2.9 * sv
            col = SPINE_C if (auto and b == bank) else C["structure"]
            fw = LEN_F * float(v[b]["people_floors"]) / fmax
            mw = LEN_M * float(v[b]["modern_3plus"]) / mmax
            pg.rect(bkx + COL_F, by_, max(fw, 0.3), 2.2 * sv, fill=col)
            pg.text("%s %s" % (b, fmt(v[b]["people_floors"])), bkx + COL_F + 1 + fw, by_ + 0.4 * sv, 7, C["ink"])
            pg.rect(bkx + COL_M, by_, max(mw, 0.3), 2.2 * sv, fill=col)
            pg.text("%s %d" % (b, v[b]["modern_3plus"]), bkx + COL_M + 1 + mw, by_ + 0.4 * sv, 7, C["ink"])
        verdict = ({"NE": "north-east bank", "SW": "south-west bank"}[bank] if auto else "over the covered stream")
        pg.text(verdict, gx0, rc - 6.3 * sv, 7.5, SPINE_C if auto else C["ink"], True)
        fit(pg, why if auto else "reaches both", bkx + 40, rc - 6.3 * sv, 7, W - 41.0, C["ink2"])
    pg.text("floors: proxy for residents", bkx, ytop - Hc + 1.5, 7, C["ink2"])
    CL_LOG.append(u"chart p09 cl_p10_bank %.0f x %.0f mm (frame p09.8 less the heading row), rows %.1f mm" % (
        W, Hc, bst))
    return u"Which bank the spine takes · within 250 m", (bkx, ytop - Hc, bkx + W, ytop)


def p10_market(pg, L):
    """v5 / v7 (booklet p.10): the producers' market with the two farm areas this page prints (M10 facts), read
    live. v9: recorded on pg (a diagram in mm); returns its heading."""
    # the producers' market: the farm areas that feed it (M10: printed on this page only), read live
    ln = L["lands"]
    mkx = P2_MARKET
    mkw = 406.0 - mkx
    mk = [g for g in FUNCS if g["n"] == 5][0]
    fit(pg, mk["where"], mkx, P2_LOW - 4.6, 7, mkw, C["ink2"])
    fit(pg, "fed by the stored water", mkx, P2_LOW - 8.2, 7, mkw, C["ink2"])
    yy = P2_LOW - 16.0
    for key in ("cropland_ha", "orchard_ha"):
        if not fact_prints_on(key, "9"):
            continue
        s_ = fact_text(key)
        if not s_:
            BM_NOTE.append("FLAG: %s not read (run the water balance first): left off p09's market" % key)
            continue
        fit(pg, s_, mkx, yy, 11, mkw, SPINE_C, True)
        yy -= 4.4
        if key == "cropland_ha":
            crops = [CROP_NAME.get(c_.strip().lower(), c_.strip())
                     for c_ in str(ln.get("cropland_crops", "")).split(",") if c_.strip()]
            rows_, cur = [], ""
            for c_ in crops:
                t_ = (cur + ", " + c_) if cur else c_
                if cur and text_w(t_, 7) > mkw:
                    rows_.append(cur + ",")
                    cur = c_
                else:
                    cur = t_
            rows_ += [cur] if cur else []
            for s2 in rows_[:2]:
                fit(pg, s2, mkx, yy, 7, mkw, C["ink2"])
                yy -= 3.0
        yy -= 3.0
    icon(pg, "farm", mkx, yy, 8)
    return u"Producers' market"


CL_AN_PT = 5.0                           # v12 (G7-2, round 7): map names = the annotation set's 5 pt (annot.py AN_NAME)
CL_TREES = [0]                           # v10 (G6-10): hub-square trees drawn this run (all one species: planes)
CL_TREE_COLS = set()                     # v9.1: the colours the hub-square planes were drawn in (legend check)


def cl_plane_plan(q, crown_m, seed):
    """v9.1 (round 5 fix, G-R5-6, CLOSING_CHECK §2 row 10): one hub-square tree (the masterplan's planes) from the
    plant module: pla_plan("plane") at (q) survey m with k = 1 (the module's mm = metres here), its masses, colours
    and plan mark as on every other drawing; vector only (an image or placeholder answer falls back to the module's
    own vector drawing). Returns map items ("fill", rings, hex, alpha, nonzero) / ("line", pts, hex, w mm, dash, a)."""
    sh = pla_plan("plane", q[0], q[1], 1.0, crown_m=crown_m, seed=seed)
    if not any(s_[0] == "poly" for s_ in sh):
        c_ = pla_colours("plane")
        sh = _pla_plan(PLA_SPECIES["plane"]["form"], q[0], q[1], crown_m, 1.0, c_, seed) + \
            _pla_plan_mark("plane", q[0], q[1], crown_m / 2.0, c_, seed)
    out = []
    for s_ in sh:
        if s_[0] == "poly" and s_[1]:
            rings = [list(s_[1])] if isinstance(s_[1][0][0], (int, float)) else [list(R_) for R_ in s_[1]]
            if s_[2]:
                out.append(("fill", rings, s_[2], 1.0, True))
                CL_TREE_COLS.add(u"%s" % s_[2])
            if len(s_) > 3 and s_[3]:
                out += [("line", R_ + [R_[0]], s_[3], (s_[4] if len(s_) > 4 and s_[4] else 0.08), None, 1.0)
                        for R_ in rings]
        elif s_[0] == "line" and len(s_[1]) >= 2:
            out.append(("line", list(s_[1]), s_[2], (s_[3] if len(s_) > 3 and s_[3] else 0.08), None, 1.0))
    return out




def p08_items(ix, L):
    """v4 (D8 b) / v9 (round 5 S9, G-R5-12; was page_framework): booklet p08 as items, no page: the title and the
    intro; the corridor map (framework_map, one true-scale drawing in m on the site frame's axes, north_deg, scale
    chosen by the booklet) with its heading, legend and the shops note (group cl_p08_corridor); who comes to the
    stream and when (who_panel, one chart drawing in mm) with its heading, note and legend (group cl_p08_who).
    The seven reasons (reasons_tiles) are not exported: they are not on the booklet page (PLAN.py p08 rows)."""
    page = "p08"
    SRC_KEY[:] = []
    ix.text(page, u"The stream joins the town where the shops already are", "title", id="cl_p08_title", priority=1)
    ix.text(page, u"shops on **two streets** · the stream **hidden** where the main road meets it · the project: "
            u"**one corridor** along the stream, **hubs** at the bridges", "intro", id="cl_p08_intro", priority=1)
    pg = Page(420, 297, "p08")
    fm = framework_map(pg, L)
    f = fm["f"]
    sc = fm["sc"]                                         # v13 (round 9 d4): an M map, context window + focus
    D = cl_drawing(ix, "cl_p08_corridor", page, pg, fm["box"], den=fm["den"], origin_m=fm["window"][:2],
                   dkind="plan", north_deg=cl_north_deg(f), group="cl_p08_corridor", priority=2, layer="map",
                   focus=fm["focus"], frame="p08.2")
    D["rec_den"] = int(round(fm["den"]))                  # v13: the true scale it is drawn at, and its printed label
    D["label_den"] = sc["lab"]["L"]
    ix.text(page, fm["head"], "heading", drawing=D["id"], id="cl_p08_corridor_head", group=D["group"], priority=2)
    ix.legend(page, D["id"], [(cl_sw(dr), wd) for dr, wd in fm["rows"]] + basemap_legend_rows(fm["base"]),
              id="cl_p08_corridor_legend", group=D["group"])   # v13 (G9-4 item 3): the context classes too
    ix.text(page, fm["shops"], "note", drawing=D["id"], id="cl_p08_shops", group=D["group"], priority=3)
    pw = Page(420, 297, "p08 who")
    wp = who_panel(pw, L)
    D2 = cl_drawing(ix, "cl_p08_who", page, pw, wp["box"], dkind="chart", group="cl_p08_who", priority=4,
                    layer="chart", frame="p08.4")         # v13 (d5): exactly the frame's chart box
    ix.text(page, wp["head"], "heading", drawing=D2["id"], id="cl_p08_who_head", group=D2["group"], priority=4)
    if wp.get("note"):
        ix.text(page, wp["note"], "note", drawing=D2["id"], id="cl_p08_who_note", group=D2["group"], priority=5)
    ix.legend(page, D2["id"], [(cl_sw(dr), wd) for dr, wd in wp["rows"]], id="cl_p08_who_legend", group=D2["group"])
    CL_LOG.extend(r9_scale_line(page, "p08.2", sc["Tfit"], sc["lab"]))   # v13 (ADDENDUM §0.9)
    CL_LOG.append(u"FLAG names survey 'Çırçır fab.' labels not in the table (2)")   # NAMES_r9.md: logged once per part
    basemap_context_log(page, "cl_p08_corridor", fm["base"], study=True, log=CL_LOG, no_room=[])   # G9-4 item 5
    try:                                                  # v10: G6-6 / G6-4 log lines (PLAN §2.4, §2.6)
        hue_log(page, log=CL_LOG)
        an_log(page, 0, 0, log=CL_LOG)
    except Exception as ex_:
        CL_LOG.append(u"FLAG p08 hue_log / an_log not read (%s: %s)" % (type(ex_).__name__, ex_))
    PAGE_SRC[page] = list(SRC_KEY)


def p09_items(ix, L):
    """v10 (round 6, BRIEF §6 row 9 U16 U17, PLAN §2.2 + §3 P-10; was p10_items): ONE page p09 = SON page9 as base
    + page10's plan row. The title and the intro; (1) the spine map across the study area (spine_map, restored from
    c493fac page_spine; cl_p09_spine) and ONE merged legend (p09_legend_rows; cl_p09_legend, side column); the
    plans' heading and one plan per bridge place (hub_plan; ids cl_p10_win_<key>, 3a/3b kept), all at one scale,
    each widened to its hub column (hub_plan_layout) and headed by the hub's code and real name; one card per hub
    (hub_card; cl_p09_card_<1-5>, the booklet's frame ids) under its plan(s), one column width P9_COL_W; (2) the flood rule (SKETCH), (3)
    which bank and the producers' market. No key map (PLAN §2.5 P-2: the spine map locates every hub; windows are
    not cuts). Every drawing's elements grouped (G6-9)."""
    page = "p09"
    SRC_KEY[:] = []
    ix.text(page, u"The streamside spine, hub by hub", "title", id="cl_p09_title", priority=1)
    ix.text(page, u"five **bridge places** on existing bus stops · walking hubs with a **sub-hub in the bed** · one "
            u"transit hub", "intro", id="cl_p09_intro", priority=1)
    hubs = hub_list()
    f = site_frame(L.get("ctx") or {})
    # (1) the spine map
    pm = Page(420, 297, "p09 spine")
    sm = spine_map(pm, L, hubs, f)
    D = cl_drawing(ix, u"cl_p09_spine", page, pm, sm["box"], den=sm["den"], origin_m=(sm["u0"], sm["v0"]),
                   dkind="plan", north_deg=cl_north_deg(f), group=u"cl_p09_spine", priority=2, layer="map",
                   focus=sm["focus"], frame="p09.2")      # v13 (round 9 d4): an M map, context window + focus
    D["rec_den"] = int(round(sm["den"]))                  # v13: the true scale it is drawn at, and its printed label
    D["label_den"] = sm["sc"]["lab"]["L"]
    CL_LOG.extend(r9_scale_line(page, "p09.2", sm["sc"]["Tfit"], sm["sc"]["lab"]))   # v13 (ADDENDUM §0.9)
    basemap_context_log(page, u"cl_p09_spine", sm["base"], study=True, log=CL_LOG, no_room=[])   # G9-4 item 5
    ix.text(page, (u"The spine across the study area, hub by hub " + cite(SRC_BUS)).strip(), "heading",
            drawing=D["id"], id=u"cl_p09_spine_head", group=D["group"], priority=2)
    # the plans
    wins = hub_windows(L, hubs)
    for w in wins:                                        # the window's key: the hub number, a / b when it has two
        mine = [w2 for w2 in wins if w2["no"] == w["no"]]
        w["key"] = str(w["no"]) + (u"" if len(mine) == 1 else u"abcdef"[mine.index(w)])
    den = hub_plan_layout(f, wins)
    ix.text(page, (u"The bridge places in plan, upstream to downstream " + cite(SRC_BUS)).strip(), "heading",
            id="cl_p09_windows_head", group="cl_p09_windows", priority=3)
    seen, grp = set(sm["seen"]), {}                       # v13: the side legend = the spine map's rows only (the
    for w in wins:                                        # plan windows are not on the round 9 page: PAGE_TABLE p09)
        pg = Page(420, 297, "p09 " + w["key"])
        hub_plan(pg, L, f, w)
        wid = u"cl_p10_win_" + w["key"]
        g_ = grp.setdefault(w["no"], wid)                 # the hub's group = its first window's id
        D = cl_drawing(ix, wid, page, pg, w["box"], den=w["den"], origin_m=(w["u0"], w["v0"]), dkind="plan",
                       north_deg=cl_north_deg(f), group=g_, priority=3, layer="map")
        D["window_m"] = [round(w["size_m"][0], 1), round(w["size_m"][1], 1)]
        D["rec_den"] = w["den"]
        D["column"] = hubs.index(w["hub"]) + 1            # v10 (P-10): the hub column it sits above (1-5)
        ix.text(page, u"%s %s" % (hub_code(w["hub"]), w["name"] or w["hub"]["title"]), "heading", drawing=D["id"],
                id=wid + u"_head", group=g_, priority=3)
    BM_NOTE.append("p09 hub plans: %d windows recorded at 1:%s in stream order (%s); streamside walks not drawn "
                   "(P10.5)" % (len(wins), fmt(den), ", ".join(w["name"] or w["hub"]["title"] for w in wins)))
    with cl_ix_group("legend", u"p09 legend"):
        ix.legend(page, u"cl_p09_spine", [(cl_sw(dr), wd) for dr, wd in p09_legend_rows(seen)] +   # v11.1: swatch
                  basemap_legend_rows(sm["base"]), id="cl_p09_legend", group=u"cl_p09_spine")   # v13: + context
    with cl_ix_group("legend", u"p09 card key"):          # v13 (p09.6, U17): the card key line under the cards
        ix.legend(page, None, [(cl_sw(dr), wd) for dr, wd in p09_legend_rows(set(["events"]), cards=True)],
                  id="cl_p09_card_key", group=u"cl_p09_cards")
    n_cards = 0
    for hb in hubs:                                       # v13 (round 9 BRIEF p9, U17; d5, f4): one boxed card each
        code, no_ = hub_code(hb), hub_no(hb)
        fk = u"p09.5" + u"abcde"[no_ - 1]                 # frames p09.5a-e = cards 1-5 (K4, K3, T, K5, K6)
        cw, chh = r9_wh(fk) or (76.0, 102.0)
        bw = cw - 2.0 * CARD_PAD
        bh = chh - CARD_BAR_MM - CARD_HEAD_MM - CARD_PAD
        gs, used, used1 = hub_card_fit(hb, bw, bh)
        pg = Page(420, 297, "p09 card")
        with pg.group("hubs", u"card " + code):
            hc = hub_card(pg, hb, 14.0, 250.0, bw, head=False, gs=gs)
        X0, YT = 14.0 - CARD_PAD, 250.0 + CARD_BAR_MM + CARD_HEAD_MM
        YB = min(YT - chh, cl_bbox(pg, pad=0.0)[1] - CARD_PAD)   # taller only when the body overflows (WARNING)
        if used1 > bh + 0.05:
            wn_warn(page, u"card %s fit" % code, u"card body needs %.1f mm, frame gives %.1f (text kept at size)" % (
                used1, bh), log=CL_LOG)
        cid = u"cl_p09_card_%d" % no_
        Dc = cl_drawing(ix, cid, page, pg, (X0, YB, X0 + cw, YT), dkind="diagram",   # S9 frame ids 1-5
                        group=grp.get(no_), priority=4, layer="diagram", frame=fk, fixed_text=True)
        hh_ = YT - YB                                     # the card's height in drawing mm (y up from its foot)
        hcol = hub_col(hb)
        kd = "transit" if hb["transit"] else hb["kind"]
        cat, rk = ("CTX", 2) if kd == "gateway" else ("PUB", 1 if kd == "transit" else 2)
        tcx, tcy = CARD_PAD + CARD_TILE[0] / 2.0, hh_ - CARD_BAR_MM - CARD_HEAD_MM / 2.0
        npt = CARD_NAME_PT
        nx = CARD_PAD + CARD_TILE[0] + 1.4
        if text_w(hb["title"], npt, True) > cw - CARD_PAD - nx:
            npt = 7.5
            if text_w(hb["title"], npt, True) > cw - CARD_PAD - nx:
                wn_warn(page, u"card %s head" % code, u"name %r wider than the head row at 7.5 pt" % hb["title"],
                        log=CL_LOG)
        ix0, iy0, ix1, iy1 = fm_ink_box(hb["title"], npt, True)
        with cl_ix_group("hubs", u"card " + code):        # v13 (f4): the head row's parts, drawn by the booklet
            ix.tag(page, code, drawing=Dc["id"], at=(tcx, tcy), box_mm=list(CARD_TILE), fill=hcol, ring=None,
                   size_pt=CARD_TILE_PT, bold=True, colour=mk_text_colour(hcol), group=Dc["group"], id=cid + u"_no",
                   priority=1)
            ix.text(page, hb["title"], "heading", drawing=Dc["id"], at=(nx, tcy - (iy0 + iy1) / 2.0), size_pt=npt,
                    bold=True, colour=GRID_INK["ink"], positions=["=L"], id=cid + u"_head", group=Dc["group"],
                    priority=1)
        Dc["card"] = dict(frame=fk, w_mm=round(cw, 2), h_mm=round(hh_, 2), code=code, title=hb["title"], colour=hcol,
                          cat=cat, rank=rk, bar_mm=CARD_BAR_MM, head_mm=CARD_HEAD_MM, pad_mm=CARD_PAD,
                          frame_colour=CARD_FRAME[0], frame_pt=CARD_FRAME[1], tile=cid + u"_no", head=cid + u"_head",
                          drawing_grow=round(gs, 3),
                          parts=[dict(part=nm_, box=[round(CARD_PAD, 2), round(yb_ - YB, 2), round(CARD_PAD + bw, 2),
                                                     round(yt_ - YB, 2)]) for nm_, yt_, yb_ in hc["parts"]])
        n_cards += 1 if hc["parts"] else 0
        CL_LOG.append(u"card p09 %s %s: body %.0f x %.0f mm, used %.1f mm (%d %%), hub drawing x %.2f, parts %s" % (
            code, fk, bw, bh, used, int(round(100.0 * used / max(bh, 1e-6))), gs,
            u", ".join(nm_ for nm_, _a, _b in hc["parts"])))
    CL_LOG.append(u"p09 cards n=%d parts exported" % n_cards)
    for fn, did, pr, fk in ((p10_flood, u"cl_p10_flood", 6, "p09.7"), (p10_bank, u"cl_p10_bank", 7, "p09.8"),
                            (p10_market, u"cl_p10_market", 8, "p09.9")):
        pg = Page(420, 297, "p09 " + did)
        with pg.group("other", did):
            res = fn(pg, L)
        head, bx_ = res if isinstance(res, tuple) else (res, None)   # v13: the bank chart returns its frame box
        Db = cl_drawing(ix, did, page, pg, bx_ or cl_bbox(pg), dkind="diagram", group=did, priority=pr,
                        layer="diagram", frame=fk)
        ix.text(page, head, "heading", drawing=Db["id"], id=did + u"_head", group=did, priority=pr)
    try:
        an_log(page, 0, 0, log=CL_LOG)                    # G6-4: no cuts or levels on these plans
    except Exception as ex_:
        CL_LOG.append(u"annot p09 cuts=0 levels=0 · FLAG an_log not read (%s)" % type(ex_).__name__)
    CL_LOG.append(u"trees p09 species=1 generic=0 · %d hub-square trees, all %s (masterplan; base-map trees are "
                  u"green areas, not single trees)" % (CL_TREES[0], PLANE_NAME))
    PAGE_SRC[page] = list(SRC_KEY)

# ------------------------------------------------------------------ build and run
def results(L=None):
    # v1.11: + "hubs" (the bridge places with their bus stops, PHASE2_SPEC §4 fields + lines) and each function's hub;
    # every earlier key stays (the site board and the masterplan read spine, spine_banks, functions, main_spine)
    hub_of = dict((n, hb["id"]) for hb in HUBS for n in hb["stops"])
    hubs = [dict(name=hb["title"], bridge=hb["id"], xy=hb["xy"], bus_stop=hb["bus_stops"][0]["name"],
                 bus_stop_m=hb["bus_stops"][0]["m"], sub_hub=hb["kind"] == "walk", kind=hb["kind"],
                 main_transit_hub=hb["transit"], plane_trees=hb["kind"] == "walk", stops=hb["stops"],
                 bus_stops=hb["bus_stops"], trips=hb["trips"], later=hb.get("later"), ch=hb["ch"]) for hb in hub_list()]
    return dict(spine_banks=(L or {}).get("sides"), bank_votes=(L or {}).get("votes"), bank_vote_source=(L or {}).get("vote_src"),
                script="bergama_city_link_v10.py", version=VERSION, run_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                spine=SPINE, functions=[dict([(k, f.get(k)) for k in ("n", "name", "where", "xy", "stage", "who", "grows", "ch", "bank")] +
                                             [("hub", "sub-hubs" if f["n"] == 8 else hub_of.get(f["n"]))])
                                        for f in FUNCS + [EVENTS]],
                chainage=CH, main_spine=MAIN_SPINE, shops=shop_figures(), hubs=hubs, main_transit_hub=MAIN_TRANSIT_HUB,
                hubs_source=SRC_HUBS + "; " + SRC_BUS,
                note="survey coordinates (m); spine offsets are schematic for the movement network")

# ------------------------------------------------------------------ v9: items for the booklet (G-R5-12)
# v1.8-v8.2 wrote an A3 sheet PDF and booklet/blocks.json crops of it (booklet_export): gone in v9 (round 5,
# addendum 1 Nov 22:37 point 2: no sheet PDF, no preview, no crops); the booklet composes p08 and p10 from items.json.
def cl_items(L):
    """v9 (round 5 S9, G-R5-12; was build(dir_), CHK-12: a top-level `build` read as the Button input): booklet p08
    and p09 as items (p08_items, p09_items; v10: p09 = SON page9 + page10's plans) in one Ix, every public source the pages cite as an ix.source row (one
    "source" item per page and key), saved to cached/booklet/Bergama_city_link_analysis/items.json; then
    city_link_results.json (same keys) in cached/Bergama_city_link_analysis/. Returns the Ix."""
    ix = Ix(CL_FOLDER, "bergama_city_link", VERSION)
    CL_IX[0] = ix
    del CL_ITEMS_LOG[:]
    PAGE_SRC.clear()
    p08_items(ix, L)
    p09_items(ix, L)
    for page, srcs in sorted(PAGE_SRC.items()):
        for src in srcs:
            key = CL_SRC_KEY[src]
            if key not in ix.d["sources"]:
                ix.source(key, src, None)
            ix._item(page, "source", u"src_%s_%s" % (page, key), "source", 9, None, key=key)
    ix.save()
    os.makedirs(RES_DIR, exist_ok=True)                   # cached/ (C2: nothing goes to output/)
    with open(os.path.join(RES_DIR, OUT_JSON), "w", encoding="utf-8") as f:
        json.dump(results(L), f, ensure_ascii=False, indent=1)
    return ix


def main():
    """v9 / v10: read the live inputs, export p08 + p09 as items, write city_link_results.json; the log = its head, "<n>
    warnings" + every WARNING line on top (wn_compose), then the run's lines. Nothing is written to output/ (C2)."""
    t0 = time.time()
    wn_reset()                                            # v9 (C1): one warning sink per run
    tp_log_lines()                                        # no text lines left from an earlier run
    BM_NOTE[:] = []
    del CL_LOG[:]                                         # v7: this run's map_draw / key-map lines
    CL_GROUPS.clear()                                     # v10 (G6-9)
    CL_TREES[0] = 0                                       # v10 (G6-10)
    CL_HANDED[0] = 0                                      # v11 (L7)
    del R9_LOG[:]                                         # v13 (round 9): frames_r9 FLAG lines of this run
    L = live()
    ix = cl_items(L)
    lines = [u"%s  %s" % (os.path.join(RES_DIR, OUT_JSON), time.strftime("%H:%M:%S")), ix.summary(),
             u"figures: %s; %s; %s" % (L["wb_src"], L["mv_src"], L["ctx_note"]), L["mp_when"], L["mv_when"],
             u"trigger: " + (TRIG_WHY[0] or "-")]
    lines += CL_ITEMS_LOG + CL_LOG + cl_groups_log() + list(R9_LOG)
    lines.append(u"names handed to the booklet: %d (anchored on their points; left out here: 0)" % CL_HANDED[0])
    lines += [n_ for n_ in [L.get("fw_note"), L.get("mp_note")] + sorted(set(BM_NOTE)) if n_]
    lines.append(u"open points (not drawn): market edge, decks and stall sizes (masterplan); hub plane-tree irrigation "
                 u"from storage (water board); ridership at the bus stops (none found, h03); the sub-hub's bed edges and "
                 u"the terraces are not in masterplan_results.json (p09 draws the hub squares, their trees and the "
                 u"stepping stones)")
    head = [u"city link %s · %s · %.1f s" % (VERSION, time.strftime("%Y-%m-%d %H:%M:%S"), time.time() - t0)]
    return u"\n".join(wn_compose(tp_log_lines() + lines, head))

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


def done_text(ran, ok, secs):
    """The done output: kept until the next run (this Rhino session)."""
    return ("done " if ok else "ERROR ") + time.strftime("%H:%M:%S") + ".%02d" % int((time.time() % 1) * 100) + \
        " · %.0f s" % secs if ran else None


_gh = "ghenv" in globals()
if _gh:
    import scriptcontext as _sc
    try: _ik = ":" + str(ghenv.Component.InstanceGuid)   # 25 Oct 10:29: each component keeps its own log and done
    except Exception: _ik = ""
    _pressed, _why, _btn = trig_should_run("bergama_city_link_chain")   # v7 (round 4 S1): one trigger file
    TRIG_WHY[0] = _why
    if _pressed:
        _t0 = time.time()
        try:
            _res = main()
        except Exception as _ex:   # 25 Oct: the error goes into the log panel, the old log never stays
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-600:])
        _sc.sticky["bergama_city_link_log" + _ik] = write_log(_res)
        _sc.sticky["bergama_city_link_log_status" + _ik] = ("ERROR" if _sc.sticky["bergama_city_link_log" + _ik].startswith("ERROR") else time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky["bergama_city_link_log_done" + _ik] = done_text(True, not _sc.sticky["bergama_city_link_log_status" + _ik].startswith("ERROR"), time.time() - _t0)
        _sc.sticky["bergama_city_link_log_ver" + _ik] = VERSION
    if _sc.sticky.get("bergama_city_link_log_ver" + _ik) != VERSION:   # v2 (Aras 27 Oct 15:35): a newly pasted version
        for _s in ("", "_status", "_done"):                              # shows itself at once, idle, without the old
            _sc.sticky.pop("bergama_city_link_log" + _s + _ik, None)      # run's time or log
    done = _sc.sticky.get("bergama_city_link_log_done" + _ik, "idle")   # 25 Oct 10:20: stays after the run; wire into the next script's run (one-click chain)
    log = _sc.sticky.get("bergama_city_link_log" + _ik, "Press the Button to export the items to " + bg_booklet(CL_FOLDER))
    print(log)               # 25 Oct 12:10: the canvas's log output is Grasshopper's "out" (printed text): print the log
    try: ghenv.Component.Message = "CityLink " + VERSION + " · " + _sc.sticky.get("bergama_city_link_log_status" + _ik, "idle")   # Aras 25 Oct 09:44
    except Exception: pass
else:
    print(write_log(main()))
