# CURRENT VERSION: bergama_city_link_v9_1.py = v9.1 (fix 2 Nov: p10 hub-square trees drawn by the plant module, pla_plan "plane"); v9 (round 5, session S9, 2 Nov 2026: "produce then compose" (G-R5-12): no sheet PDF, no crops; p08 and p10 exported as items for the booklet; P08.1-P08.3, P10.1-P10.4, C1, C2, C10, CHK-12; what changed: NEW IN v9 below; v8.2: p08 north arrow off the margin, p10 key names off the hub markers, flood lines 3.5 mm apart; v8.1 / v8: layout checks and text collisions are WARNING lines, the run goes on; v7: round 4 S5)
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

VERSION = "v9.1"  # v9.1 fix 2 Nov (round 5 open rows, G-R5-6): the p10 hub-square planes come from common/plants.py (pla_plan) instead of 16-gon discs in the local green; v9 2 Nov (round 5 S9): items for the booklet, no sheet PDF (NEW IN v9 above); v8.2 1 Nov 22:10 (Aras 19:49): p08 north arrow off the margin, p10 key names off the hub markers, flood lines 3.5 mm apart; v8.1 1 Nov 21:40 (Aras 19:33): every layout check that stopped the run (text size, lines, column width, rows, legend room) is a WARNING line and an orange warning; 6.00 pt no longer counts as under 6.0; v8 1 Nov 20:55: text collisions are orange warnings with one WARNING line each, the run goes on (Aras 1 Nov 17:11 + 18:52); v7 (round 4, S5, 1 Nov 2026): p08 and p10 redrawn on the shared round 4 modules (see NEW IN v7); v6.5 fix 1 Nov 08:30: only the component's own inputs can start it (a True setting inside the script no longer does); v6.4 fix 1 Nov 08:20: chain trigger keyed to each solve (Rhino keeps globals), so the chain continues after ZoneBase; v6.3 fix 1 Nov: a pasted or rewired component no longer runs by itself (chain trigger notes the wire on its first solve)
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
#@include ../common/bergama_paths.py
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
#@include data/STREAM_REF.py
# v1.10 SHOPS_XY: shops on page 1's plan = OSM shop=* and amenity cafe/restaurant/fast_food/bar/pub/ice_cream (nodes,
# and buildings at the mean of their corners) of the same extract (28 Jul 2026, bergama_osm.osm of the commercial spine
# thread), converted with the h01 §0 formula (+-10-30 m), kept inside the v1.11 plan's 960 x 740 m window (survey x
# 29700-30660, y 31570-32310): 150 places (calculated 26 Oct 2026). v2: the plan covers the whole site frame and takes
# the site board's shop points (same OSM file and tags, city_context.json); these are its fallback (window only, logged)
#@include data/SHOPS_XY.py
#@include ../common/data/LEVELS.py
#@include ../common/levels.py
# v6 (round 3, G16 / D9): every printed bridge or place name from the one names table (bridge_name, place_name)
#@include ../common/data/NAMES.py
#@include ../common/names.py
# 1 Nov (v6.2): the spine, its bank vote and the stops live in common/city_spine.py (the masterplan builds them too)
#@include ../common/city_spine.py


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

#@include ../common/rgb.py
#@include ../common/r28_style.py
#@include ../common/units.py
#@include ../common/basemap.py
#@include ../common/grid.py
# v7 (round 4, S1 modules): real font widths, the ONE text placer, the ONE marker. v9 (round 5, C1): the ONE warning
# sink first (text_place then logs into WN_LOG; nothing raises on text or layout)
#@include ../common/warn.py
#@include ../common/font_metrics.py
#@include ../common/text_place.py
#@include ../common/marker.py
#@include ../common/buildings.py
#@include ../common/icons.py
#@include ../common/section_parts.py
#@include ../common/hires.py
#@include ../common/plants.py
#@include ../common/data/FACTS.py
#@include ../common/facts.py
# v9 (round 5, G-R5-12): the item export (needs bergama_paths, grid, warn above)
#@include ../common/item_export.py

# v9: the Arial files font_metrics measures with (no PDF is written any more)
#@include ../common/pdf_fonts.py


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
            self.shapes.append(("poly", rf, fill, stroke if one else None, lw if one else 0.0,
                                tuple(dash) if (one and dash) else None, None, alpha))
            if one:
                return
        if stroke:
            for R in rs:
                Q = R + [R[0]] if closed and len(R) >= 3 else R
                self.shapes.append(("line", Q, stroke, lw, tuple(dash) if dash else None, cap))
    def line(self, P, col, lw=0.25, dash=None, mul=False, cap=1): self.path([P], None, col, lw, False, dash, mul, cap)
    def text(self, s, x, y, size, col="4A3F35", bold=False, align="L", name=None, allow=(), role="label"):
        """one line of text, size pt, baseline (x, y), align L / C / R; registered in the TextPage (real box) and
        recorded with its role ("marker" = a glyph on its own disc: exported as a badge)"""
        if not s or not s.strip():
            return
        self.tp.put(s, x, y, size, bold, align, 0.0, name, role, col, allow, self.tg, emit=False)
        self.shapes.append(("text", s, float(x), float(y), size * IX_PT, col, bool(bold), align or "L", role))


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
               priority=5, title=None, layer=None):
    """v9 (round 5 S9, G-R5-12; the idea of the masterplan's mpx_drawing): ONE item drawing from the part box (x0, y0,
    x1, y1 page mm) of the recorder pg. den given: a true-scale drawing in m (x_d = origin_m + (x_mm - x0) x den /
    1000, the site frame's axes for the maps), scale_pref = the Bergama list (the booklet picks one); den None: a
    scale-free diagram in mm (extent = the box size) with a fit range whose lower end keeps its smallest word at
    >= 4 pt. Shapes are cut to the box; each recorded text inside the box becomes an anchored label (first position
    = exactly where it was recorded, then the 8 compass spots), a marker glyph a badge (only its own spot); texts
    outside the box are left out and counted. Returns the drawing dict."""
    x0, y0, x1, y1 = [float(v) for v in box]
    texts = [s_ for s_ in pg.shapes if s_[0] == "text" and x0 - 0.01 <= s_[2] <= x1 + 0.01 and
             y0 - 0.01 <= s_[3] <= y1 + 0.01]
    n_out = sum(1 for s_ in pg.shapes if s_[0] == "text") - len(texts)
    if den:
        k = float(den) / 1000.0
        ext = (origin_m[0], origin_m[1], origin_m[0] + (x1 - x0) * k, origin_m[1] + (y1 - y0) * k)
        D = ix.drawing(did, page, ext, scale_pref=CL_SCALES, units="m", dkind=dkind, north_deg=north_deg,
                       scale_bar=True, priority=priority, group=group or did, title=title)
        org = (origin_m[0] - x0 * k, origin_m[1] - y0 * k)
    else:
        k = 1.0
        pts = [s_[4] / IX_PT for s_ in texts]
        lo = max(0.5, 4.0 / min(pts)) if pts else 0.5        # D1: no word under 4 pt after the booklet's fit
        D = ix.drawing(did, page, (0.0, 0.0, x1 - x0, y1 - y0), units="mm", dkind=dkind, scale_bar=False,
                       priority=priority, group=group or did, title=title, fit=(math.ceil(lo * 100.0) / 100.0, 2.0))
        org = (-x0, -y0)
    shapes = []
    for s_ in pg.shapes:
        if s_[0] == "poly":
            rs = [r for r in (cl_clip_ring(R, (x0, y0, x1, y1)) for R in s_[1]) if len(r) >= 3]
            if rs:
                shapes.append(("poly", rs) + tuple(s_[2:]))
        elif s_[0] == "line":
            for _f, Q in clip_runs(s_[1], (x0, y0, x1, y1)):
                if len(Q) >= 2:
                    shapes.append(("line", Q) + tuple(s_[2:]))
    ix.layer(D, layer or dkind, shapes, k=k, origin=org)
    for s_ in texts:
        al = s_[7] if s_[7] in ("L", "C", "R") else "L"
        badge = s_[8] == "marker"
        ix.text(page, s_[1], "badge" if badge else "label", drawing=D["id"], at=(org[0] + k * s_[2], org[1] + k * s_[3]),
                size_pt=s_[4] / IX_PT, bold=s_[6], colour=s_[5], positions=["=" + al] + ([] if badge else CL_COMPASS),
                group=D["group"], priority=2 if badge else 5)
    CL_ITEMS_LOG.append(u"items %s %s: %d shapes, %d labels%s%s" % (
        page, D["id"], len(shapes), len(texts), (u" · drawn at 1:%s, %.0f x %.0f m" % (fmt(den), ext[2] - ext[0],
                                                                                   ext[3] - ext[1])) if den else
        u" · mm %.0f x %.0f" % (x1 - x0, y1 - y0), (u" · %d text(s) outside the box left out" % n_out) if n_out else u""))
    return D


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
        wn_warn("p10", "stale", u"the spine's bank vote reads the site board's city_link_movement.json %s, older than "
                u"this chain's Button press (the site board did not write it in this run): %s" % (mv_when, mv_path))
    # v1.8 (FIGURE_CONFLICTS.md §2): the spine length = the masterplan's drawn pieces (edge + deck + over), read live;
    # none printed when the masterplan has not run (was a typed "about 660 m", the K4-K5 chainage)
    mp_path = bg_result(*MP_FILE)              # v9 (C10): the corridor the plans inherit from the masterplan
    mp, t3 = _load([mp_path])
    mp_fresh, mp_when = bg_this_run(mp_path)
    if not mp_fresh:
        wn_warn("p10", "stale", u"the corridor (spine, hub squares, road changes) from masterplan_results.json is not "
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
                mp_note=("" if mpmv else "FLAG: no masterplan movement (masterplan_results.json): p.10's hub plans have "
                         "no road changes, crossings, sub-hubs or bus line") +
                ("" if (mp or {}).get("hub_squares") else "\nFLAG: no hub_squares in masterplan_results.json (run the "
                 "masterplan v38 once): p.10's plans have no hub squares"),
                ctx_note=("plan context: site board of " + t4) if ctx else
                "FLAG: no city_context.json (run the site board v46 first): page 1's plan has no context and its shops "
                "cover only the old central window; page 2's reach uses 800 m")

#@include ../common/fmt.py

GROUP = dict(L=("Locals", "CC9A52"), T=("Visitors", "8B3A3F"), S=("Students", "5C7A86"))   # v4: T = visitors (AA's word)
GROWS = dict(W="water", E="stream edge", A="agriculture", H="heritage")
GROW_C = dict(W=C["water_deep"], E=C["water"], A=C["green_mid"], H=C["accent"])   # v1.6 letter chips
SPINE_C = "BC6F45"
SOFT = ((1.0, 0.36), (0.6, 0.18), (0.28, 0.0))   # v2: a soft band: (width share, paler by) of its three strokes
REACH_RIM = 1.2                           # v3 (MIRAQUA 28 Oct, P10.1): mm of the reach rim showing above and below the
                                          # page 2 stream band (the reach classes of R28_REACH, drawn under the band)
# v3 (MIRAQUA 28 Oct, G11 / F13): crops and plants by their printed names, "English (Turkish)" as the shared table
# common/plant_photos.py PLANTS (maize prints "Corn (Mısır)"); keys as the water balance writes them
CROP_NAME = {"cotton": u"Cotton (Pamuk)", "maize": u"Corn (Mısır)", "corn": u"Corn (Mısır)",
             "tomato": u"Tomato (Domates)", "olive": u"Olive (Zeytin)"}
PLANE_NAME = u"Oriental plane (Doğu çınarı)"


SRC_KEY = []                         # v1.6: the sources this page cites (v9: in order of their first mark)
PAGE_SRC = {}                        # v9: page id ("p08", "p10") -> its sources (ix.source rows, cl_items)


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
            pg.poly(list(sh[1]), fill=sh[2] or None, stroke=sh[3] or None, lw=sh[4] or 0.2, closed=True)
            pg.keep(sh[1], "marker", nm)
    for sh in shapes:
        if sh[0] == "text":
            pg.text(sh[1], sh[2], sh[3], size_pt, sh[5], True, "L", name=nm, allow=(nm,) + tuple(allow),
                    role="marker")
    return box, r_


def cl_marker_free(pg, cx, cy, s, col, size_pt=7.0, frame=None, allow=(), name=None, lead=True, rings=(2.2, 3.2, 4.4),
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
    """v7 (round 4, G-R4-1; replaces lp_place / place_marks): a name beside its point at (at) on a map: the compass
    positions in reading order round it (r mm + 0.8 mm gap), the first one clear of every text and keep (bar allow)
    and inside frame; drawn there through pg.text. Returns its box, or None when no spot is free (the caller keeps
    the name in its legend or logs it; nothing is drawn over anything)."""
    tp = pg.tp
    for code in positions:
        x, y, al = tp._at(code, s, at, size, bold, r + 0.8)
        b = tp._box(s, x, y, size, bold, al, 0.0)
        if frame and not (frame[0] <= b[0] and b[2] <= frame[2] and frame[1] <= b[1] and b[3] <= frame[3]):
            continue
        if tp._free(b, allow):
            pg.text(s, x, y, size, col, bold, al, allow=allow)
            return b
    return None


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
P2_CARD_GAP = 6.0                        # page 2: gutter between the hub cards
P2_LOW = 76.0                            # page 2: the title line of the three bottom panels
P2_FLOOD = (14.0, 64.0, 19.0)            # page 2 flood rule: x, first (highest) level's y, row step
P2_BANK = (216.0, 65.0, 12.0)            # page 2 which bank: x, first row y, row step
SPINE_SIMPLIFY_M = 2.5                   # v7 (P10.5): the spine line simplified to this (m) and runs under
SPINE_MIN_M = 8.0                        # this long in a plan dropped (no stubs): drawing rules, not data
SQ_EDGE = "9C7440"                       # v7 (P10.6): the hub square's edge, as the masterplan draws it (p21)
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
                if tint:
                    pg.path(grp, fill=hx, alpha=1.0 if alpha is None else float(alpha))
                else:
                    pg.path(grp, fill=col(hx, alpha))

    def line_fn(pts, hx, w_mm, dash_mm, alpha):
        if len(pts) >= 2:
            d_ = (tuple(dash_mm) if isinstance(dash_mm, (list, tuple)) else (dash_mm, dash_mm)) if dash_mm else None
            pg.line(pts, col(hx, alpha), w_mm, dash=d_)

    def text_fn(s_, q, size_mm, hx, bold, align):
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


def cl_map(pg, page, T, sbox, den, project, base_extra=(), clip=True, allow=(), legend_cols=None, water_ok=None):
    """v7 (G-R4-4; replaces bm_draw): one map through THE draw order (map_draw): the muted base of the box sbox
    (survey m) at 1:den (ml_base: light houses with closed outlines, streets, the stream) + base_extra (e.g. the
    covered course), then project {layer: items} (proj_tint multiplied, proj_lines, proj_vegetation, proj_marks),
    the study line, clipped to the study area when clip. The caller clips the PDF to its window and draws markers
    and labels after it (they are the top layers). Returns (n base items, the study rings).
    v9 (round 5, G-R5-8): the stream is drawn above the tints (map_draw's "water" layer); legend_cols (the legend's
    fill colours) and water_ok (fills in the water by design) go to map_draw for its zones line."""
    try:
        base = ml_base(sbox, den)
    except Exception as ex_:
        BM_NOTE.append("basemap not read: %s: %s" % (type(ex_).__name__, ex_))
        base = []
    if not base:
        BM_NOTE.append("FLAG: no basemap data (run the site board v59 once): the maps draw only the study area")
    BM_NOTE.extend(basemap_warnings())
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
HUB_COL = dict(walk="495338", transit="8B3A3F", hidden="8B3A3F", gateway="847E75")   # C green_deep, accent, ink2
mk_register("cl_hub", HUB_COL)
mk_register("cl_place", {"place": SPINE_C})              # the project's places: the spine's colour


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
BUS_C = "633131"                         # v4 (R29): the bus line's colour (v6: on p.09's hub plans)
# v9 (round 5, P08.2, Aras U06 "get rid of this line"): the project corridor line along the stream is no longer drawn
# (CORRIDOR_LW / CORRIDOR_BAR gone; corridor_line() stays for its length, it is drawn nowhere)
SHOP_C = "B5832F"                        # v7 (P08.1): today's shop streets, ochre (palette autumn tone), 1.4 mm
SHOP_LW = 1.4
# v9 (round 5, P08.1, Aras U06 + S03 "primary / secondary"): a shop street of lower rank (fewer shops in the site
# board's ranking) in the project palette's 8B2D2D (PLAN §3), thinner: it reads as the lesser street, and its dark
# red stands well apart from the stream's blues (5C7A86 / A2B6B5) and the ochre street; drawing rules, not data
SHOP2_C = "8B2D2D"
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
ROAD_STYLE = {"calmed": ("B5832F", 0.9), "pedestrian": ("8B3A3F", 1.2), "shared": ("7F5B7B", 0.9),
              "relocated": ("C2603A", 0.9)}
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


def cl_street_extend(runs, f, label=None):
    """v9 (round 5, P08.1, Aras U06 "they should continue to the extents"): a shop street's runs (survey m; one OSM
    way each, clipped to the site frame by the site board) joined end to end, then each free end that stops inside
    the map carried on along the OpenStreetMap street centrelines (the shared basemap's streets_in, footways left
    out) to the map's edge (cl_street_walk). Returns runs + the pieces added; logged with the metres added."""
    if not runs:
        return runs
    try:
        D = basemap_load()
        nets = [[tuple(p) for p in P] for cl, P in ((D or {}).get("layers") or {}).get("streets_in") or []
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
    dict(box (page mm), f (site frame), rows [(sample draw, words)], head, shops)."""
    mx, my = FW_MAP
    ctx = L.get("ctx") or {}
    fw = L.get("fw") or {}
    f = site_frame(ctx)
    T = frame_T(f, mx, my, PLAN_DEN)
    k = 1000.0 / PLAN_DEN
    fw_, fh_ = f["w"] * k, f["h"] * k
    box_ = (mx, my, mx + fw_, my + fh_)
    PLAN_BOX["fw"] = box_
    inside = lambda q: mx <= q[0] <= mx + fw_ and my <= q[1] <= my + fh_
    frame = (mx + 1.0, my + 1.0, mx + fw_ - 1.0, my + fh_ - 1.0)
    MAP = "map p08"
    head = (u"The whole corridor · the shop streets, the hidden stream and the project from end to end " +
            cite(SRC_MAIN) + u" " + cite(SRC_SHOPS)).strip()
    pg.keep(box_, "map", MAP)
    sbox = frame_box(f, f["u0"], f["v0"], f["u0"] + f["w"], f["v0"] + f["h"])
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
        rs = cl_street_extend([[tuple(p) for p in R_] for R_ in g["runs"] if len(R_) >= 2], f, g.get("label"))
        runs_ += rs
        lines += [("line", R_, C["white"], lw_ + 0.5, None, 1.0) for R_ in rs]
        lines += [("line", R_, col, lw_, None, 1.0) for R_ in rs]
        BM_NOTE.append(u"p08 shop street %d: %s, %s shops (site board), %s" % (
            i + 1, g.get("label"), g.get("shops", u"?"), u"ochre" if i == 0 else SHOP2_C))
    study = cl_study()
    nb, study = cl_map(pg, "p08", T, sbox, PLAN_DEN, {"proj_tint": ml_tint(study), "proj_lines": lines},
                       base_extra=covered, clip=False, legend_cols=[ML_TINT])
    # our lines are keeps for the labels (no name on a shop street)
    for R_ in runs_:
        pg.keep([T(p) for p in R_], "line", "shop street")
    # the marks on top: the junction, then the hubs, numbered as on p10
    jx, jy = T((30058.0, 32047.0))                          # Kınık Caddesi over the covered stream (stop 3's place)
    disc(pg, jx, jy, 1.2, C["accent"], C["white"], 0.3)
    pg.keep((jx - 1.4, jy - 1.4, jx + 1.4, jy + 1.4), "marker", "junction")
    hubs = hub_list()
    for hb in hubs:
        hx, hy = T(hb["xy"])
        if inside((hx, hy)):
            cl_marker_free(pg, hx, hy, str(hub_no(hb)), hub_col(hb), 7.0, frame=frame, allow=(MAP,),
                           name="hub %d" % hub_no(hb))
    # names next to their own line, where free (else in the legend only); v9: through the names table
    for g in spines:
        if not g.get("label") or g["label"] == "an unnamed street":
            continue
        Q = [q for q in (T(p) for p in max(g["runs"], key=len)) if inside(q)]
        if len(Q) > 1:
            cl_place(pg, street_label(g["label"]), Q[len(Q) // 2], 7.5, C["ink"], True, 1.2, frame, (MAP,))
    for c_, R_ in sorted([r_ for r_ in clip_runs(P, sbox, cov) if not r_[0]], key=lambda r_: -len(r_[1])):
        Q = [q for q in (T(p) for p in R_) if inside(q)]
        if len(Q) > 1 and cl_place(pg, place_name("stream"), Q[len(Q) // 2], 7.5, C["water_deep"], True, 1.6, frame,
                                   (MAP,)):
            break
    # the legend rows (an Ix legend beside the map: the booklet places it)
    rows = []
    if nb:
        rows.append((sw_fill(BM_COL["water"], BM_COL["water_edge"]), place_name("stream")))
    rows.append((sw_line(C["water_deep"], 0.8, (1.6, 0.9)), place_name("stream") + ", covered"))
    rows.append((lambda p_, b: (p_.rect(b[0], b[1], b[2] - b[0], b[3] - b[1], fill=tint_hex(ML_TINT, 1.0 - ML_TINT_ALPHA)),
                                sw_line(BM_STUDY_LINE["colour"], BM_STUDY_LINE["width_mm"],
                                        tuple(BM_STUDY_LINE["dash_mm"]))(p_, b)),
                 "study area: the project's ground"))
    for i, g in enumerate(ranked):                        # v9 (P08.1): one row per rank
        nm_ = street_label(g["label"]) if g.get("label") and g["label"] != "an unnamed street" else u""
        rows.append((sw_line(SHOP_C, SHOP_LW) if i == 0 else sw_line(SHOP2_C, SHOP2_LW),
                     (u"shop street today" + (u"" if i == 0 else u", fewer shops") + (u": " + nm_ if nm_ else u""))))
    rows.append((sw_mark(lambda p_, x, y: disc(p_, x, y, 1.1, C["accent"], C["white"], 0.3)),
                 "the main road meets the stream, covered"))
    for hb in hubs:
        kd = "walking hub" if hb["kind"] == "walk" else ("main transit hub" if hb["transit"] else
                                                         ("gateway" if hb["kind"] == "gateway" else "hub"))
        rows.append((sw_mark(lambda p_, x, y, hb=hb: cl_marker(p_, x, y, str(hub_no(hb)), hub_col(hb), 7.0,
                                                               name="legend hub %d" % hub_no(hb))),
                     u"%s · %s" % (hb["title"], kd)))
    # the shops figure: one headline value and one line (G4), as one note with its value bold
    sf = shop_figures()
    shops = (u"**%d of %d shops** by the stream sit on the covered %d m, where the main road meets it" % (
        sf["covered_reach"], sf["by_stream"], sf["covered_reach_m"]))
    return dict(box=box_, f=f, rows=rows, head=head, shops=shops)


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
    yb = ys - river_h - sum(blk[g_] + GAP for g_ in blk)
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
        fit(pg, (what + " " + " ".join(cite(s_) for s_ in srcs)).strip(), x0 + 7.5, top - 7.2, 7, 92.0, C["ink2"])
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
    return dict(head=head, note=concl, rows=ent)          # v9: the key is a legend item (the booklet sets it)


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


def hub_card(pg, hb, x, ytop, w):
    """v1.11 / v5 / v6 / v7 (round 4, P10.3 P10.4, G-R4-1/7/11): one bridge place in its column under the plans'
    legend, no frame: its locator marker (the number on the key map and over its plan(s)) and real name, its role,
    its existing bus stops (metres to the hub), the later step, the trips, its levels (the dry hub over the sub-hub in
    the bed, the hidden square, or the gateway) as a glyph with its keys, and its places, numbered as on the plan,
    with who they serve, what they grow from and their keywords. v7: bigger type (name 10.5 pt, rows 8 pt, keywords
    7.5 pt) and glyph (24 x 15 mm) in a wider column; laid out from the top by the real line heights. Returns the
    baseline under the last line.
    v9 (round 5 S9, P10.3 "one per hub, same structure"): every hub's diagram has the same rows in the same order,
    in the same width (p10_items): number + name, role, bus stop(s) with metres, (later step), trips, the levels glyph
    with its keys (v9: the gateway too: its road-out glyph, "GATEWAY OUT" / "no hub square"), then its places (none at
    the gateway). Recorded on its own recorder; exported as one diagram grouped with its plan window."""
    tr = hb["transit"]
    y = ytop - 3.6
    _b, r_ = cl_marker(pg, x + 2.0, y + 1.1, str(hub_no(hb)), hub_col(hb), 7.5, name="card hub %d" % hub_no(hb))
    tx = x + 2.0 + r_ + 1.4
    pg.tgroup()
    for ln in cl_wrap(hb["title"], 10.5, x + w - tx, True):
        pg.text(ln, tx, y, 10.5, C["ink"], True)
        y -= 4.6
    pg.tgroup(False)
    role = ("MAIN TRANSIT HUB · " if tr else ("walking hub · " if hb["kind"] == "walk" else "")) + hb["role"]
    y = cl_para(pg, role, x, y - 0.3, 8, w, C["accent"] if tr else C["ink2"], tr) - 0.8
    for st in hb["bus_stops"]:
        icon(pg, "bus", x, y + 2.9, 3.6)
        dist = "%d m" % st["m"]
        dw = text_w(dist, 8.5, True)
        pg.text(dist, x + w, y, 8.5, SPINE_C, True, "R")
        fit(pg, st["name"], x + 4.8, y, 8, w - 6.8 - dw, C["ink"], True)
        y -= 4.4
    if hb.get("later"):                                    # the proposed town-line extension, in accent
        y = cl_para(pg, hb["later"], x + 4.8, y, 7.5, w - 4.8, C["accent"], True)
    y = cl_para(pg, hb["trips"], x + 4.8, y, 7.5, w - 4.8, C["ink2"]) - 1.6
    gw, gh = 24.0, 15.0                                    # the levels: a small section with its keys beside it
    hub_glyph(pg, hb["kind"], x, y + 2.6, gw, gh)          # v9 (P10.3): every hub, the gateway its road out
    if hb["kind"] == "walk":
        kws = [("DRY HUB", True), ("street level, above Q500", False), ("SUB-HUB in the bed", True),
               ("open Jul-Sep · shut in floods " + cite(SRC_WET), False)]
    elif hb["kind"] == "hidden":
        kws = [("HIDDEN STREAM SQUARE", True), ("water line in the paving over the culvert " + cite(SRC_HIDDEN),
                                                False),
               (landmark_name("kizil_avlu").replace(u"i", u"İ").upper() + u" TUNNEL MOUTHS", True),
               ("a viewing edge", False)]
    else:                                                  # v8.2's "GATEWAY OUT · no hub square", as keys
        kws = [("GATEWAY OUT", True), ("no hub square", False)]
    ky = y
    for j, (s_, b_) in enumerate(kws):
        if j and b_:
            ky -= 0.8
        ky = cl_para(pg, s_.strip(), x + gw + 2.0, ky, 7.5, w - gw - 2.0, C["ink"], b_, lead=3.2)
    y = min(y + 2.6 - gh, ky + 3.2 - 0.6) - 4.4
    for n in hb["stops"]:
        f = [g for g in FUNCS + [EVENTS] if g["n"] == n][0]
        cl_marker(pg, x + 2.4, y + 1.0, str(n), mk_colour("cl_place", "place"), 7.0, r_min=2.2,
                  name="card place %d" % n)
        nx = x + 6.2
        y = cl_para(pg, f["name"], nx, y, 8, x + w - nx, C["ink"], True, lead=3.5)
        cy = y + 1.0                                       # who it serves (dots) and what it grows from (chips)
        group_dots(pg, nx + 1.1, cy, f["who"], r=1.1)
        gx = nx + 9.8
        for g_ in f["grows"]:
            pg.rect(gx, cy - 1.4, 3.2, 2.8, fill=GROW_C[g_])
            pg.text(g_, gx + 1.6, cy - 0.9, 7, C["white"], True, "C")
            gx += 3.7
        y -= 3.8
        words = f["kw"][0] + " · " + f["kw"][1] + (" " + cite(f["src"]) if f.get("src") else "")
        if n == 7:                                         # the entry lies upstream of the hub (chainage, calculated)
            words += " · about %d m upstream of %s" % (int(round((CH["K4"] - FUNCS[6]["ch"]) / 10.0) * 10),
                                                       bridge_name("K4", short=True))
        y = cl_para(pg, words.strip(), nx, y, 7.5, x + w - nx, C["ink"], lead=3.2) - 1.8
    return y


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
    """v6 (P09.1) / v9 (round 5 S9, P10.2, Aras U38 "detay çizimlerinin genişleyip daralması okunmuyor"): ONE window
    size in metres for every hub, so the booklet can set the windows on one grid at one scale. Rule: each window must
    hold its points (the hub point, its bus stops, the sub-hub crossing, the masterplan's hub square, its places) with
    P2_PLAN_MARGIN round them on the site frame's axes; the size W x H = the widest and the tallest of those extents;
    each window is that size centred on the middle of its OWN points (not on the hub point alone: then one far bus
    stop would push every window out by its offset; the centre = the hub's extent centre, the hub point lies inside).
    The windows are recorded at one scale den (the v8.2 rule: the largest standard scale at which the row of
    windows fits the old sheet's plan row, P2_PLAN / P2_PLAN_W) only so their print-size marks (markers, stepping
    stones, crowns) have a size; the booklet picks the printed scale from the Bergama list. Sets each window's box
    (page mm, all at the same place on its own recorder), u0, v0 (frame axes, m), size_m, den; returns den."""
    x0, top, ph, gap = P2_PLAN
    ext = []
    for w in wins:
        uv = [frame_uv(f, p) for p in w["pts"]]
        ext.append((min(q[0] for q in uv) - P2_PLAN_MARGIN, max(q[0] for q in uv) + P2_PLAN_MARGIN,
                    min(q[1] for q in uv) - P2_PLAN_MARGIN, max(q[1] for q in uv) + P2_PLAN_MARGIN))
    Wm = max(e[1] - e[0] for e in ext)
    Hm = max(e[3] - e[2] for e in ext)
    n = len(wins)
    for den in R28_SCALES:
        k = 1000.0 / den
        if n * Wm * k + gap * (n - 1) <= P2_PLAN_W and Hm * k <= ph:
            break
    else:
        BM_NOTE.append("FLAG: p.10 hub windows: no standard scale fits the old plan row; recorded at 1:%s" % fmt(den))
    k = 1000.0 / den
    for w, e in zip(wins, ext):
        uc, vc = (e[0] + e[1]) / 2.0, (e[2] + e[3]) / 2.0
        w["u0"], w["v0"] = uc - Wm / 2.0, vc - Hm / 2.0
        w["box"], w["den"], w["size_m"] = (x0, top - Hm * k, x0 + Wm * k, top), den, (Wm, Hm)
    BM_NOTE.append(u"p10 windows: one size %.0f x %.0f m for all %d windows (the widest / tallest extent of a "
                   u"window's points + %.0f m margin, frame axes), each centred on its own points; recorded at 1:%s"
                   % (Wm, Hm, n, P2_PLAN_MARGIN, fmt(den)))
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
        BM_NOTE.append("FLAG: no masterplan spine pieces (masterplan_results.json): p.10's plans draw the city link's "
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
    v9 (round 5 S9, P10.2, G-R5-8/12): recorded on its own recorder and exported by p10_items as one true-scale
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
    # v9: its locator number and real name over the plan are a heading item (p10_items), not drawn here
    pg.keep(w["box"], "map", MAP)
    # base extra: the covered course
    P, cov = stream_ref()
    covered = [("line", R_, C["water_deep"], 0.8, [1.6, 0.9], 1.0) for c_, R_ in clip_runs(P, sbox, cov) if c_]
    if covered:
        seen.add("covered")
    study = cl_study()
    proj = dict(proj_tint=[], proj_lines=[], proj_vegetation=[], proj_marks=[])
    sq = w.get("sq") or {}
    rings = [[tuple(p) for p in R_] for R_ in sq.get("rings") or [] if len(R_) >= 3]
    if rings:                                             # P10.6: the masterplan's hub square, tinted (D9) + its edge
        proj["proj_tint"] += ml_tint(rings)
        proj["proj_lines"] += [("line", R_ + [R_[0]], SQ_EDGE, 0.35, None, 1.0) for R_ in rings]
        tr_ = max(1.2 * m_mm, 3.5)                        # a crown >= 1.2 mm across on the page (drawing rule)
        for i_, q in enumerate(sq.get("trees") or []):    # v9.1 (G-R5-6): the plant module's plane, not a 16-gon
            proj["proj_vegetation"] += cl_plane_plan(q, 2.0 * tr_, i_)
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
            proj["proj_lines"] += [("line", Q, C["white"], 1.1, None, 1.0), ("line", Q, BUS_C, 0.5, None, 1.0)]
            if any(inside(T(p)) for p in Q):
                seen.add("bus")
    for R_ in spine_runs(L):                              # P10.5: one solid line; no stub under SPINE_MIN_M
        for run in sc_lines(R_, study, "p10") if study else [R_]:
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
    nb, _st = cl_map(pg, "p10", T, sbox, den, proj, base_extra=covered, clip=True,   # v9: cut to the window on export
                     legend_cols=[ML_TINT, C["green_mid"], C["ink"]] + sorted(CL_TREE_COLS),
                     water_ok=[C["ink"]])                 # stones: in the bed; v9.1: + the plane's own colours

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
    cl_marker_free(pg, hx, hy_, str(w["no"]), hub_col(hb), 7.0, frame=frame, allow=(MAP,), name="hub " + MAP)
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
            if not cl_place(pg, nm_, (px, py), 7, C["ink2"], False, 0.6, frame, (MAP,)):
                BM_NOTE.append(u"p.10 plan %s: landmark name '%s' left out (no free spot)" % (w["no"], nm_))
    return seen


def p10_legend_rows(seen):
    """v7 / v9 (P10.3 v7: the plans' legend right under them, only what they draw, and the card keys): the rows
    [(sample draw, words)] of the windows' legend (an Ix legend item, set by the booklet beside the windows)"""
    pc = mk_colour("cl_place", "place")
    ent = []
    if "base" in seen:
        ent.append((sw_fill(BM_COL["water"], BM_COL["water_edge"]), place_name("stream")))
    ent.append((sw_line(BM_STUDY_LINE["colour"], BM_STUDY_LINE["width_mm"], tuple(BM_STUDY_LINE["dash_mm"])),
                "study area"))
    ent.append((sw_line(KM_ZOOM["colour"], KM_ZOOM["lw"] + 0.1), "key map: a plan's window"))
    if "covered" in seen:
        ent.append((sw_line(C["water_deep"], 0.8, (1.6, 0.9)), place_name("stream") + ", covered"))
    if "spine" in seen:
        ent.append((sw_line(SPINE_C, 1.2), "streamside spine"))
    if "square" in seen:
        ent.append((lambda p_, b: p_.rect(b[0], b[1], b[2] - b[0], b[3] - b[1], fill=tint_hex(ML_TINT, 1.0 - ML_TINT_ALPHA),
                                          stroke=SQ_EDGE, lw=0.35), "dry hub square (masterplan)"))
    if "trees" in seen:
        ent.append((sw_mark(lambda p_, x, y: disc(p_, x, y, 1.0, pla_colours("plane")["fill"])),   # v9.1
                    (u"its trees: " + PLANE_NAME + u", watered from storage " + cite(SRC_PLANE)).strip()))
    for ch in ("pedestrian", "calmed", "shared", "relocated"):
        if "road_" + ch in seen:
            ent.append((sw_line(ROAD_STYLE[ch][0], ROAD_STYLE[ch][1]), ROAD_WORD[ch]))
    if "bus" in seen:
        ent.append((sw_line(BUS_C, 0.5), "town bus line, later step"))
    if "footbridge" in seen:
        ent.append((sw_mark(lambda p_, x, y: p_.line([(x, y - 1.2), (x, y + 1.2)], C["ink"], 0.8)), "new footbridge"))
    if "stones" in seen:
        ent.append((sw_mark(lambda p_, x, y: [disc(p_, x + d_, y, 0.45, C["ink"]) for d_ in (-1.6, 0.0, 1.6)]),
                    "sub-hub crossing: stepping stones"))
    if "stop" in seen:
        ent.append((sw_mark(lambda p_, x, y: disc(p_, x, y, 1.0, C["white"], C["water_deep"], 0.3)),
                    "existing bus stop (card: metres to the hub)"))
    ent.append((sw_mark(lambda p_, x, y: cl_marker(p_, x, y, "1", HUB_COL["walk"], 7.0, name="legend walking hub")),
                "walking hub, numbered as on the key map"))
    ent.append((sw_mark(lambda p_, x, y: cl_marker(p_, x, y, "3", HUB_COL["transit"], 7.0, name="legend transit hub")),
                "main transit hub"))
    ent.append((sw_mark(lambda p_, x, y: cl_marker(p_, x, y, "5", HUB_COL["gateway"], 7.0, name="legend gateway")),
                "gateway out of town"))
    ent.append((sw_mark(lambda p_, x, y: cl_marker(p_, x, y, "1", pc, 7.0, name="legend place")),
                "place, numbered as on its card"))
    if "events" in seen:
        ent.append((sw_mark(lambda p_, x, y: cl_marker(p_, x, y, str(EVENTS["n"]), pc, 7.0, name="legend events")),
                    EVENTS["name"].lower().capitalize() + ", Jul-Sep, at the sub-hub in the bed"))
    for g_ in "LTS":
        ent.append((sw_mark(lambda p_, x, y, c=GROUP[g_][1]: disc(p_, x, y, 1.0, c)), GROUP[g_][0]))
    for g_ in "WEAH":
        ent.append((lambda p_, b, g_=g_: (p_.rect(b[0] + 1.0, b[1] - 0.2, 3.0, 2.6, fill=GROW_C[g_]),
                                          p_.text(g_, b[0] + 2.5, b[1] + 0.4, 7, C["white"], True, "C")),
                    u"grows from " + GROWS[g_]))
    return ent


def p10_flood(pg, L):
    """v1.6 / v7 (booklet p.10 (2)): the flood rule as a stair of its three levels (highest first), each level's
    rules on its step. v9: recorded on pg (a diagram in mm); returns its heading."""
    fx, fy0, fst = P2_FLOOD
    tone = (C["water"], C["water_light"], C["faint"])      # FLOOD order: bed, terrace, bank top
    nf, sw_ = len(FLOOD), 10.0
    yb_ = fy0 - (nf - 1) * fst - 8.0
    tx_, rx = fx + nf * sw_ + 4.0, fx + 100.0
    for i in range(nf):
        j = nf - 1 - i                                    # its FLOOD row: the bank top first
        lev, wet, rules, wsrc = FLOOD[j]
        y = fy0 - i * fst
        t_ = y + 3.0
        pg.rect(fx + i * sw_, yb_, sw_, t_ - yb_, fill=tone[j])
        pg.line([(fx + i * sw_, t_), (fx + (i + 1) * sw_, t_)], C["ink"], 0.4)
        if i < nf - 1:
            pg.line([(fx + (i + 1) * sw_, t_), (fx + (i + 1) * sw_, t_ - fst)], C["ink"], 0.4)
        pg.line([(fx + (i + 1) * sw_ + 0.8, t_), (tx_ - 1.0, t_)], C["ink2"], 0.2, dash=(0.6, 0.5))
        pg.text(lev, tx_, y + 1.2, 8, C["ink"], True)
        for jj, kk in enumerate(wet):
            fit(pg, (kk + (" " + cite(wsrc) if jj == len(wet) - 1 else "")).strip(), tx_, y - 2.4 - jj * 3.5, 7,
                rx - tx_ - 3.0, C["ink2"])
        for jj, (ic, kk) in enumerate(rules):
            icon(pg, ic, rx, y + 4.0 - jj * 4.8, 4.2)
            fit(pg, kk, rx + 6.0, y + 1.2 - jj * 4.8, 7, P2_BANK[0] - 8.0 - rx - 6.0, C["ink"])
    return (u"What stands where: the flood rule " + cite(SRC_RULES)).strip()


def p10_bank(pg, L):
    """v1.6 / v7 (booklet p.10 (3)): which bank the spine takes, per piece, from this run's vote. v9: recorded on pg
    (a diagram in mm); returns its heading."""
    # (3) which bank: per piece a glyph of the bank the spine takes, then paired bars NE / SW (people = home floors,
    # modern = buildings of 3+ floors, within 250 m)
    bkx, by0, bst = P2_BANK
    pg.text("home floors", bkx + 30, P2_LOW - 4.6, 7, C["ink2"], True)
    pg.text("buildings of 3+ floors", bkx + 84, P2_LOW - 4.6, 7, C["ink2"], True)
    fmax = max([1.0] + [float(L["votes"][pc["id"]][b]["people_floors"]) for pc in SPINE for b in ("NE", "SW")])
    mmax = max([1.0] + [float(L["votes"][pc["id"]][b]["modern_3plus"]) for pc in SPINE for b in ("NE", "SW")])
    for r_, pc in enumerate(SPINE):
        rc = by0 - r_ * bst
        v = L["votes"][pc["id"]]
        bank, why = bank_of(v)
        auto = pc.get("side") == "auto"
        side = bank if auto else "over"
        pg.text(pc["id"], bkx, rc - 1.2, 9, SPINE_C if auto else C["ink"], True)
        gx0, gx1 = bkx + 6.0, bkx + 23.0                  # the glyph: the stream, the spine on its bank
        pg.rect(gx0, rc - 0.9, gx1 - gx0, 1.8, fill=C["water"])
        pg.text("NE", gx1 + 0.8, rc + 1.0, 7, C["ink2"])           # v7: 6 -> 7 pt (G-R4-1 minimum on p.10)
        pg.text("SW", gx1 + 0.8, rc - 3.1, 7, C["ink2"])
        ys_ = {"NE": rc + 2.3, "SW": rc - 2.3}.get(side, rc)
        pg.line([(gx0, ys_), (gx1, ys_)], C["white"], 1.8)
        pg.line([(gx0, ys_), (gx1, ys_)], SPINE_C, 1.2)
        for j, b in enumerate(("NE", "SW")):
            by_ = rc + 0.4 - j * 2.9
            col = SPINE_C if (auto and b == bank) else C["structure"]
            fw = 34.0 * float(v[b]["people_floors"]) / fmax
            mw = 18.0 * float(v[b]["modern_3plus"]) / mmax
            pg.rect(bkx + 30, by_, max(fw, 0.3), 2.2, fill=col)
            pg.text("%s %s" % (b, fmt(v[b]["people_floors"])), bkx + 31 + fw, by_ + 0.4, 7, C["ink"])
            pg.rect(bkx + 84, by_, max(mw, 0.3), 2.2, fill=col)
            pg.text("%s %d" % (b, v[b]["modern_3plus"]), bkx + 85 + mw, by_ + 0.4, 7, C["ink"])
        verdict = ({"NE": "north-east bank", "SW": "south-west bank"}[bank] if auto else "over the covered stream")
        pg.text(verdict, gx0, rc - 6.3, 7.5, SPINE_C if auto else C["ink"], True)
        fit(pg, why if auto else "reaches both", bkx + 40, rc - 6.3, 7, P2_MARKET - 4.0 - bkx - 40, C["ink2"])
    pg.text("floors: proxy for residents", bkx, by0 - (len(SPINE) - 1) * bst - 11.0, 7, C["ink2"])
    return u"Which bank the spine takes · within 250 m"


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
            BM_NOTE.append("FLAG: %s not read (run the water balance first): left off p.10's market" % key)
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


def cl_keymap(ix, page, f, wins):
    """v9 (round 5 S9, P10.1, G-R5-3, Aras U38): the locator of p10 = THE key-map module: km_map fitted and turned
    (no scale_den), the study area and each plan window as a zoom frame labelled by its window key; km_items exported
    as they are (drawing in key-map mm, label texts, keymap item; ids registered in ix, anchors kept on the drawing).
    No own north arrow, neatline or scale (the map carries its turned north arrow; key maps have no scale bar). Offered
    space: the right column's width (PLAN §3, CL_KM_W). Returns the key map's drawing id (None when not made)."""
    zooms = {}
    for w in wins:
        Wm, Hm = w["size_m"]
        u0, v0 = w["u0"], w["v0"]
        zooms[w["key"]] = [frame_xy(f, u0, v0), frame_xy(f, u0 + Wm, v0), frame_xy(f, u0 + Wm, v0 + Hm),
                           frame_xy(f, u0, v0 + Hm)]
    try:
        km = km_map([w["key"] for w in wins], CL_KM_W, None, zooms=zooms, page=page, log=CL_LOG)
        its = km_items(km, page, item_id=u"cl_p10_keymap", priority=2)
    except Exception as ex_:
        ix.warn(page, "keymap", u"key map not exported (%s: %s)" % (type(ex_).__name__, ex_))
        return None
    did = None
    for it in its:
        it = dict(it)
        it["id"] = ix._id(it.get("id"), it.get("kind", "item"))
        it["page"] = page
        if it.get("kind") == "drawing" and did is None:
            did = it["id"]
        elif it.get("anchor") and did is not None:
            it["anchor"] = dict(it["anchor"], drawing=did)
        elif it.get("kind") == "keymap" and did is not None:
            it["drawing"] = did
        ix.d["pages"].setdefault(page, []).append(it)
    CL_ITEMS_LOG.append(u"items %s key map %s: %d items, frame %.0f x %.0f mm, windows %s" % (
        page, did, len(its), km["w_mm"], km["h_mm"], u", ".join(w["key"] for w in wins)))
    return did


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


CL_KM_W = 113.6                          # v9: mm the p10 key map may take at most: the right column (PLAN §3)


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
    D = cl_drawing(ix, "cl_p08_corridor", page, pg, fm["box"], den=PLAN_DEN, origin_m=(f["u0"], f["v0"]),
                   dkind="plan", north_deg=cl_north_deg(f), group="cl_p08_corridor", priority=2, layer="map")
    ix.text(page, fm["head"], "heading", id="cl_p08_corridor_head", group=D["group"], priority=2)
    ix.legend(page, D["id"], [(cl_sw(dr), wd) for dr, wd in fm["rows"]], id="cl_p08_corridor_legend",
              group=D["group"])
    ix.text(page, fm["shops"], "note", id="cl_p08_shops", group=D["group"], priority=3)
    pw = Page(420, 297, "p08 who")
    wp = who_panel(pw, L)
    D2 = cl_drawing(ix, "cl_p08_who", page, pw, cl_bbox(pw), dkind="chart", group="cl_p08_who", priority=4,
                    layer="chart")
    ix.text(page, wp["head"], "heading", id="cl_p08_who_head", group=D2["group"], priority=4)
    if wp.get("note"):
        ix.text(page, wp["note"], "note", id="cl_p08_who_note", group=D2["group"], priority=5)
    ix.legend(page, D2["id"], [(cl_sw(dr), wd) for dr, wd in wp["rows"]], id="cl_p08_who_legend", group=D2["group"])
    PAGE_SRC[page] = list(SRC_KEY)


def p10_items(ix, L):
    """v5-v7 / v9 (round 5 S9, P10.1-P10.4, G-R5-12; was page_spine): booklet p10 as items, no page. The title and
    the intro; the windows' heading; one plan window per bridge place (hub_windows, hub_plan_layout: ONE size in m,
    hub_plan; true scale, the same scale_pref, north_deg; id cl_p10_win_<key>, group = the first window of its hub,
    with a heading "<key> <name>"); the key map (cl_keymap, P10.1); the windows' legend (p10_legend_rows); one hub
    diagram per hub (hub_card, same structure and width, P10.3; id cl_p10_hub_<n>, group = its window's); the flood
    rule, which bank and the producers' market as diagrams in mm. Priorities follow the reading order; the layout
    is the booklet's (P10.4)."""
    page = "p10"
    SRC_KEY[:] = []
    ix.text(page, u"The streamside spine, hub by hub", "title", id="cl_p10_title", priority=1)
    ix.text(page, u"five **bridge places** on existing bus stops · walking hubs with a **sub-hub in the bed** · one "
            u"transit hub", "intro", id="cl_p10_intro", priority=1)
    hubs = hub_list()
    f = site_frame(L.get("ctx") or {})
    wins = hub_windows(L, hubs)
    den = hub_plan_layout(f, wins)
    for w in wins:                                        # the window's key: the hub number, a / b when it has two
        mine = [w2 for w2 in wins if w2["no"] == w["no"]]
        w["key"] = str(w["no"]) + (u"" if len(mine) == 1 else u"abcdef"[mine.index(w)])
    ix.text(page, (u"The bridge places in plan, upstream to downstream " + cite(SRC_BUS)).strip(), "heading",
            id="cl_p10_windows_head", group="cl_p10_windows", priority=2)
    seen, grp = set(), {}
    for w in wins:
        pg = Page(420, 297, "p10 " + w["key"])
        seen |= hub_plan(pg, L, f, w)
        wid = u"cl_p10_win_" + w["key"]
        g_ = grp.setdefault(w["no"], wid)                 # the hub's group = its first window's id
        D = cl_drawing(ix, wid, page, pg, w["box"], den=w["den"], origin_m=(w["u0"], w["v0"]), dkind="plan",
                       north_deg=cl_north_deg(f), group=g_, priority=3, layer="map")
        D["window_m"] = [round(w["size_m"][0], 1), round(w["size_m"][1], 1)]   # one size for all (P10.2)
        D["rec_den"] = w["den"]                           # the scale its print-size marks were recorded at
        ix.text(page, u"%s %s" % (w["key"], w["name"] or w["hub"]["title"]), "heading", id=wid + u"_head", group=g_,
                priority=3)
    BM_NOTE.append("p.10 hub plans: %d windows recorded at 1:%s in stream order (%s); streamside walks not drawn "
                   "(P10.5)" % (len(wins), fmt(den), ", ".join(w["name"] or w["hub"]["title"] for w in wins)))
    cl_keymap(ix, page, f, wins)
    ix.legend(page, None, [(cl_sw(dr), wd) for dr, wd in p10_legend_rows(seen)], id="cl_p10_legend",
              group="cl_p10_windows")
    cw = (392.0 - P2_CARD_GAP * (len(hubs) - 1)) / float(len(hubs))   # v9 (P10.3): one width for every hub diagram
    for hb in hubs:
        pg = Page(420, 297, "p10 hub")
        hub_card(pg, hb, 14.0, 250.0, cw)
        cl_drawing(ix, u"cl_p10_hub_%d" % hub_no(hb), page, pg, cl_bbox(pg), dkind="diagram",
                   group=grp.get(hub_no(hb)), priority=4, layer="diagram")
    for fn, did, pr in ((p10_flood, u"cl_p10_flood", 6), (p10_bank, u"cl_p10_bank", 7),
                        (p10_market, u"cl_p10_market", 8)):
        pg = Page(420, 297, "p10 " + did)
        head = fn(pg, L)
        cl_drawing(ix, did, page, pg, cl_bbox(pg), dkind="diagram", group=did, priority=pr, layer="diagram")
        ix.text(page, head, "heading", id=did + u"_head", group=did, priority=pr)
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
                script="bergama_city_link_v9_1.py", version=VERSION, run_time=time.strftime("%Y-%m-%d %H:%M:%S"),
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
    and p10 as items (p08_items, p10_items) in one Ix, every public source the pages cite as an ix.source row (one
    "source" item per page and key), saved to cached/booklet/Bergama_city_link_analysis/items.json; then
    city_link_results.json (same keys) in cached/Bergama_city_link_analysis/. Returns the Ix."""
    ix = Ix(CL_FOLDER, "bergama_city_link", VERSION)
    CL_IX[0] = ix
    del CL_ITEMS_LOG[:]
    PAGE_SRC.clear()
    p08_items(ix, L)
    p10_items(ix, L)
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
    """v9: read the live inputs, export p08 + p10 as items, write city_link_results.json; the log = its head, "<n>
    warnings" + every WARNING line on top (wn_compose), then the run's lines. Nothing is written to output/ (C2)."""
    t0 = time.time()
    wn_reset()                                            # v9 (C1): one warning sink per run
    tp_log_lines()                                        # no text lines left from an earlier run
    BM_NOTE[:] = []
    del CL_LOG[:]                                         # v7: this run's map_draw / key-map lines
    L = live()
    ix = cl_items(L)
    lines = [u"%s  %s" % (os.path.join(RES_DIR, OUT_JSON), time.strftime("%H:%M:%S")), ix.summary(),
             u"figures: %s; %s; %s" % (L["wb_src"], L["mv_src"], L["ctx_note"]), L["mp_when"], L["mv_when"],
             u"trigger: " + (TRIG_WHY[0] or "-")]
    lines += CL_ITEMS_LOG + CL_LOG
    lines += [n_ for n_ in [L.get("fw_note"), L.get("mp_note")] + sorted(set(BM_NOTE)) if n_]
    lines.append(u"open points (not drawn): market edge, decks and stall sizes (masterplan); hub plane-tree irrigation "
                 u"from storage (water board); ridership at the bus stops (none found, h03); the sub-hub's bed edges and "
                 u"the terraces are not in masterplan_results.json (p.10 draws the hub squares, their trees and the "
                 u"stepping stones)")
    head = [u"city link %s · %s · %.1f s" % (VERSION, time.strftime("%Y-%m-%d %H:%M:%S"), time.time() - t0)]
    return u"\n".join(wn_compose(tp_log_lines() + lines, head))

#@include ../common/trigger.py


#@include ../common/done_text.py


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
