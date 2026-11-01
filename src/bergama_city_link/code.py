# CURRENT VERSION: bergama_city_link_v8_2.py = v8.2 (1 Nov 2026: p08 north arrow off the margin, p10 key names off the hub markers, flood lines 3.5 mm apart; v8.1: every layout check that stopped the run (text size, lines, column width, rows, legend room) is a WARNING line and an orange warning; 6.00 pt no longer counts as under 6.0; v8: text collisions are orange warnings with one WARNING line each, the run goes on (Aras 1 Nov 17:11 + 18:52); v7: round 4 S5; what changed: the NEW IN / VERSION notes below)
# bergama_city_link_v6.py (v6, 31 Oct: round 3, p08 one corridor arrow over the whole study area + p09 hub plans; v5.1, 31 Oct: bugfix, rebuilt with the shared base map fix of 31 Oct: the stream (M5 water) no longer stops on "list - float"; v5, 30 Oct: revision T5, p8 framework map + who calendar, p9 spine) · Thread 4 of the 22 Oct batch: connection to the city (the streamside spine and what it adds)
# Runs as delivered in: Grasshopper Python 3 component (press a Button wired to any input), Rhino 8 ScriptEditor
# (Python 3), or plain Python 3. Makes the folder Downloads/Bergama/output/Bergama_city_link_analysis by itself and saves
# ONE all-vector A3 PDF there (two pages) plus city_link_results.json:
#   1 THE STREAM JOINS THE TOWN WHERE THE SHOPS ALREADY ARE (booklet p.08, v7) the whole corridor on the shared
#                                                         muted basemap (one project corridor line, end to end), who the
#                                                         project brings (G7), seven reasons
#   2 THE STREAMSIDE SPINE, HUB BY HUB                    (booklet p.10, v7) a key map + each bridge place in plan (stops,
#                                                         sub-hub crossing in the bed, crossings, bus stops, spine)
#                                                         with its card under it, the flood rule, which bank, the
#                                                         producers' market
# city_link_results.json = the spine, the function sites and (v1.11) the hubs in survey coordinates. The site board (selinus_board v34,
# plan 07) reads it for the movement potential with the spine; the masterplan builds the same spine from common/city_spine.py (v6.2).
# Read live on every run: the water balance results (farm areas for the producers' market) and the site board's
# movement result (walking potential on the spine), each with a flagged fallback.
# Notes for Aras: batch_2026-10-22/thread4_city_link/NOTES.md (every figure with its source).
import os, time, json, zlib, math, base64

VERSION = "v8.2"  # v8.2 1 Nov 22:10 (Aras 19:49): p08 north arrow off the margin, p10 key names off the hub markers, flood lines 3.5 mm apart; v8.1 1 Nov 21:40 (Aras 19:33): every layout check that stopped the run (text size, lines, column width, rows, legend room) is a WARNING line and an orange warning; 6.00 pt no longer counts as under 6.0; v8 1 Nov 20:55: text collisions are orange warnings with one WARNING line each, the run goes on (Aras 1 Nov 17:11 + 18:52); v7 (round 4, S5, 1 Nov 2026): p08 and p10 redrawn on the shared round 4 modules (see NEW IN v7); v6.5 fix 1 Nov 08:30: only the component's own inputs can start it (a True setting inside the script no longer does); v6.4 fix 1 Nov 08:20: chain trigger keyed to each solve (Rhino keeps globals), so the chain continues after ZoneBase; v6.3 fix 1 Nov: a pasted or rewired component no longer runs by itself (chain trigger notes the wire on its first solve)
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
OUT_DIR = bg_output("Bergama_city_link_analysis")            # final PDFs only (27 Oct)
RES_DIR = bg_cache("Bergama_city_link_analysis")             # 27 Oct: city_link_results.json (the board and masterplan read it)
OUT_PDF = "Bergama_city_link_A3.pdf"
OUT_JSON = "city_link_results.json"
WB_FILES = [os.path.join(bg_cache("Bergama_water_balance_analysis"), "water_balance_results.json"),   # 27 Oct: cached/
            os.path.join(BERGAMA, "output", "Bergama_water_balance_analysis", "water_balance_results.json"),
            os.path.join(os.path.expanduser("~"), "Downloads", "Bergama_water_balance_analysis", "water_balance_results.json")]
# 27 Oct: new places (cached/) first, then where older versions wrote them
MV_FILES = [os.path.join(bg_cache("selinus_board"), "city_link_movement.json"),          # written by selinus_board v34+
            os.path.join(BERGAMA, "output", "selinus_board", "city_link_movement.json")]
MP_FILES = [os.path.join(bg_cache("bergama_masterplan"), "masterplan_results.json"),      # v1.8: the drawn spine's length
            os.path.join(BERGAMA, "output", "bergama_masterplan", "masterplan_results.json")]
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
     [("road", "6 m service road kept clear"), ("crest", "occupied floors at DSİ crest + 1.50 m (5/10)")], SRC_FLOOD),
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
# v7 (round 4, S1 modules): real font widths, the ONE text placer (a collision raises), the ONE marker
#@include ../common/font_metrics.py
#@include ../common/text_place.py
#@include ../common/marker.py
#@include ../common/buildings.py
#@include ../common/icons.py
#@include ../common/data/FACTS.py
#@include ../common/facts.py

# ------------------------------------------------------------------ minimal vector PDF (mm units, Arial embedded, whole strings)
_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}   # Turkish letters in unused WinAnsi slots
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"

#@include ../common/pdf_fonts.py


def text_w(s, size, bold=False):
    """v7 (round 4, G-R4-1): the width (mm) of s at size pt from the real Arial metrics (font_metrics.fm_width; the
    Helvetica estimate table is gone)"""
    return fm_width(s, size, bold)

PAGE_MARGINS = (14.0, 12.0, 14.0, 12.0)   # v7 (G-R4-1): (left, top, right, bottom) mm kept free of text on the sheet
CL_LOG = []                           # v7: this run's "overlap ..." and "layers ..." lines (printed in the log)
TRIG_WHY = [None]                     # v7: what started this run (trig_should_run), printed in the log


class Page:
    """v7 (round 4, G-R4-1): one TextPage per page (pg.tp, y up, page mm, the round 4 booklet page id as its name):
    every pg.text is registered there with its real Arial box before it is drawn, every marker disc and map is a
    keep; pg.check_text() runs the collision test, which RAISES TextCollision (no sheet with a collision is written)"""
    def __init__(self, w, h, name=None):
        self.w, self.h, self.ops = w, h, []
        self.tp = TextPage(name, (0.0, 0.0, w, h), y_down=False, pad=0.6, margins=PAGE_MARGINS) if name else None
        self.tg = None                            # the open text group (lines of one word block may touch)
    def tgroup(self, start=True):
        """v7: start (or with False end) one text group: the runs of one line / lines of one paragraph"""
        self.tg = self.tp._group() if start and self.tp is not None else None
        return self.tg
    def keep(self, geom, kind="keep", name=None, line=None):
        """v7: an obstacle no text may touch (a box, an area or a line, page mm)"""
        return self.tp.keep(geom, kind, name, line) if self.tp is not None else None
    def free(self, box, allow=()):
        """v7: True when box (page mm) is clear of every text and keep (bar allow) and inside the margins"""
        return self.tp is None or self.tp._free(box, allow)
    def check_text(self):
        """v7: the page's collision test; logs "overlap <page> checked n, collisions k" and RAISES on any"""
        if self.tp is not None:
            self.tp.check(True, CL_LOG)
    def _c(self, h, stroke=False):
        r, g, b = rgb(h); return "%.3f %.3f %.3f %s" % (r, g, b, "RG" if stroke else "rg")
    def rect(self, x, y, w, h, fill=None, stroke=None, lw=0.2):
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill, stroke, lw, True)
    def poly(self, P, fill=None, stroke=None, lw=0.2, closed=False, dash=None):
        self.path([P], fill, stroke, lw, closed, dash)
    def path(self, rings, fill=None, stroke=None, lw=0.2, closed=True, dash=None, mul=False, cap=1):
        """several rings in one path; a fill uses even-odd, so holes stay open. v2: mul = laid over what is under it by
        multiplying (a proposal tint: the PDF blend mode, /GM in write_pdf); cap 0 = butt ends"""
        k = 72 / 25.4; o = ["q"] + (["/GM gs"] if mul else [])
        if fill: o.append(self._c(fill))
        if stroke: o.append(self._c(stroke, True)); o.append("%.3f w %d J 1 j" % (lw * k, cap))
        if dash: o.append("[%s] 0 d" % " ".join("%.2f" % (d_ * k) for d_ in dash))   # v3 (G8): any on/off pattern
        for P in rings:
            o.append("%.2f %.2f m" % (P[0][0] * k, P[0][1] * k))
            o += ["%.2f %.2f l" % (x * k, y * k) for x, y in P[1:]]
            if closed: o.append("h")
        o.append("B*" if fill and stroke else ("f*" if fill else "S")); o.append("Q")
        self.ops.append(" ".join(o))
    def line(self, P, col, lw=0.25, dash=None, mul=False, cap=1): self.path([P], None, col, lw, False, dash, mul, cap)
    def text(self, s, x, y, size, col="4A3F35", bold=False, align="L", name=None, allow=(), role="label"):
        """one line of text, size pt, baseline (x, y), align L / C / R. v7: registered in the page's TextPage first
        (real box; allow = keep names / kinds it may sit on, e.g. its own marker disc or the map it labels)"""
        if not s or not s.strip():
            return
        if self.tp is not None:
            self.tp.put(s, x, y, size, bold, align, 0.0, name, role, col, allow, self.tg, emit=False)
        if align == "C": x -= text_w(s, size, bold) / 2
        elif align == "R": x -= text_w(s, size, bold)
        k = 72 / 25.4
        self.ops.append("BT /%s %.2f Tf %s %.2f %.2f Td (%s) Tj ET" % ("F2" if bold else "F1", size, self._c(col), x * k, y * k, self._enc(s)))
    def _enc(self, s):
        b = b"".join(bytes([_ENC_EXTRA[ch]]) if ch in _ENC_EXTRA else ch.encode("cp1252", "replace") for ch in s)   # 25 Oct: ı İ ğ Ğ ş Ş spelt right
        return b.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)").decode("latin-1")


def write_pdf(pages, path):
    k = 72 / 25.4
    n = len(pages)
    objs = ["<< /Type /Catalog /Pages 2 0 R >>",
            "<< /Type /Pages /Kids [%s] /Count %d >>" % (" ".join("%d 0 R" % (5 + 2 * i) for i in range(n)), n),
            "", ""]
    extra, first = [], 5 + 2 * n                          # G2/G3 28 Oct: Arial embedded (common/pdf_fonts.py):

    def add(b):                                           # font file + descriptor go after the pages
        extra.append(b.decode("latin-1"))
        return first + len(extra) - 1
    fid = pdf_fonts(add, ("R", "B"))
    objs[2], objs[3] = extra[fid[0] - first], extra[fid[1] - first]   # the font dicts themselves stay objects 3, 4
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"); offs = []
    for i, o in enumerate(objs):
        offs.append(len(out)); out += ("%d 0 obj\n%s\nendobj\n" % (i + 1, o)).encode("latin-1")
    for i, pg in enumerate(pages):
        content = zlib.compress("\n".join(pg.ops).encode("latin-1"))
        offs.append(len(out))
        out += ("%d 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %.2f %.2f] /Resources << /Font << /F1 3 0 R /F2 4 0 R >> /ExtGState << /GM << /Type /ExtGState /BM /Multiply >> >> >> /Contents %d 0 R >>\nendobj\n"
                % (5 + 2 * i, pg.w * k, pg.h * k, 6 + 2 * i)).encode("latin-1")
        offs.append(len(out))
        out += ("%d 0 obj\n<< /Length %d /Filter /FlateDecode >>\nstream\n" % (6 + 2 * i, len(content))).encode("latin-1") + content + b"\nendstream\nendobj\n"
    for j, o in enumerate(extra):
        offs.append(len(out)); out += ("%d 0 obj\n%s\nendobj\n" % (first + j, o)).encode("latin-1")
    x = len(out)
    out += ("xref\n0 %d\n0000000000 65535 f \n" % (len(offs) + 1) + "".join("%010d 00000 n \n" % o for o in offs) +
            "trailer\n<< /Size %d /Root 1 0 R /Info << /Title (Bergama city link) >> >>\nstartxref\n%d\n%%%%EOF\n" % (len(offs) + 1, x)).encode("latin-1")
    with open(path, "wb") as f: f.write(out)


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
    mv, t2 = _load(MV_FILES)
    mv_src = ("site board movement of " + t2) if mv else "run the site board once to compute the walking potential"
    votes, vote_src, sides = spine_votes(mv, mv_src)     # v6.2: common/city_spine.py (the masterplan votes the same way)
    # v1.8 (FIGURE_CONFLICTS.md §2): the spine length = the masterplan's drawn pieces (edge + deck + over), read live;
    # none printed when the masterplan has not run (was a typed "about 660 m", the K4-K5 chainage)
    mp, t3 = _load(MP_FILES)
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


def header(pg, title, sub):
    """v1.11: a white page (Aras 27 Oct 11:07: the beige paper goes), the title and one keyword line. v3 (MIRAQUA
    28 Oct, F10 + G1): no big page number before the title and no "CONNECTION TO THE CITY · PAGE n OF 2 · GROUP 6"
    line (course / group lines go); title and keywords on the left margin; G5: the keyword line's **words** bold"""
    pg.rect(0, 0, 420, 297, fill=C["white"])
    pg.text(title, 14, 279, 22, C["ink"], True)
    rich(pg, sub, 14, 271.5, 11, C["ink2"])


def rich(pg, s, x, y, size, col, bold_col=None):
    """v3 (MIRAQUA 28 Oct, G5): one line with its **keywords** bold (runs split at "**", each run a live text);
    returns the end x"""
    pg.tgroup()                                           # v7: the runs of one line touch each other only
    for i, part in enumerate(s.split("**")):
        if part:
            b_ = i % 2 == 1
            pg.text(part, x, y, size, (bold_col or C["ink"]) if b_ else col, b_)
            x += text_w(part, size, b_)
    pg.tgroup(False)
    return x

SRC_KEY = []                         # v1.6: sources printed as [n] on the page
PAGE_SRC = {}                        # v1.11: page index -> its numbered sources (no footer on the sheet: blocks.json)


def cite(src):
    """v1.6 (water board v1.6 method): the number of a source in this page's key, as "[n]". v1.11: the key is no
    longer printed on the sheet (Aras 27 Oct: source footers go); it goes to booklet/blocks.json "sheet_sources"."""
    if not src or src in CITE_OFF or src not in PUB_SRC:   # v3 (F5) + v4 (D13): public sources only get a mark
        return ""
    if src not in SRC_KEY:
        SRC_KEY.append(src)
    return "[%d]" % (SRC_KEY.index(src) + 1)


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


def step(pg, n, x, y):
    """v1.11: the reading-order number in front of a panel title (top left to bottom right); returns the title's x.
    v7 (G-R4-7): the shared marker (glyph centred on its ink box)"""
    _b, r_ = cl_marker(pg, x + 2.6, y + 1.1, str(n), C["accent"], 8.0, r_min=2.6, name="step %d" % n)
    return x + 2.6 + r_ + 1.6


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


def cl_legend(pg, rows, x, ytop, w, size=7.0, lead=4.4, sw=6.0):
    """v7 (G-R4-3: the legend beside its drawing; replaces lg_draw / Legend): rows [(draw(pg, swatch box) or None,
    words)] stacked from the top baseline ytop - 2.6 down, each sample in a sw x 2.6 mm box, the words beside it
    wrapped to the column (no widow); returns the legend's box (x0, y0, x1, y1)"""
    y = ytop - 2.6
    tx = x + sw + 1.6
    for draw, words in rows:
        if draw:
            draw(pg, (x, y - 0.4, x + sw, y + 2.2))
        y = cl_para(pg, words, tx, y, size, x + w - tx, C["ink"], lead=size * 0.3528 * 1.2) - (lead - size * 0.3528 * 1.2)
    return (x, y + lead - 1.2, x + w, ytop)


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


def scale_bar(pg, x, y, den):
    """v5 (G1): the scale bar of a plan at 1:den (a standard scale, r28_scale): four segments from (x, y), 0 / middle
    / end in m under it, the scale after it; returns the x where it ends"""
    k = 1000.0 / den
    seg_m = scale_seg(den)                                # v6: 20 m segments on the hub plans
    for i_ in range(4):
        pg.rect(x + i_ * seg_m * k, y, seg_m * k, 1.2, fill=(C["ink"], C["white"])[i_ % 2])
    pg.rect(x, y, 4 * seg_m * k, 1.2, stroke=C["ink"], lw=0.15)
    pg.text("0", x, y - 3.2, 7, C["ink2"], False, "C")
    pg.text(fmt(2 * seg_m), x + 2 * seg_m * k, y - 3.2, 7, C["ink2"], False, "C")
    pg.text(fmt(4 * seg_m) + " m", x + 4 * seg_m * k - text_w(fmt(4 * seg_m), 7) / 2.0, y - 3.2, 7, C["ink2"])
    s_ = "1:%s" % fmt(den)
    pg.text(s_, x + 4 * seg_m * k + 9.0, y - 0.2, 7, C["ink2"])
    return x + 4 * seg_m * k + 9.0 + text_w(s_, 7)


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
PLAN_BOX = {}                            # v2: the plan's rectangle as drawn (for its booklet crop)
# v4: P1_MAP, P1_KEY, P1_A, P1_B, P1_WHO, P1_WALK are gone with the shops plan, the charts, who comes and walking
# potential (page 1 is the framework: FW_MAP, WHO_BOX, P1_TILES further down)
# v5 (revision 30 Oct 2026, p.09): page 2 = the whole study area on one map across the top (its legend beside it, scale
# bar and north arrow under it), the five bridge places as cards under it with the same badges as on the map (no
# leaders), then the flood rule, which bank and the producers' market along the bottom
# v6 (round 3, D1, P09.1): the overview map is p.08's; page 2 zooms into each bridge place: a row of plans at one
# scale in stream order (hub_plan_layout), each hub's card under its plan(s), the key under the cards
# v7 (round 4, P10.1-P10.4, spec S5): key map at the left of the plan row, plans 70 mm high, then their legend, then the
# hub cards in five columns, then the three bottom panels 8 mm lower than before
P2_TITLE_Y = 264.0                       # page 2 section 1 title baseline (scale bar and north arrow on the same line)
P2_KEY = (14.0, 181.0, 56.0, 70.0)       # page 2 key map: x, y (bottom), w, h (mm)
P2_PLAN = (74.0, 251.0, 70.0, 4.0)       # page 2 hub plans: x, top y, height, gap between plans (mm)
P2_PLAN_W = 332.0                        # the row's width (x 74-406)
P2_PLAN_MIN_W = 36.0                     # the narrowest plan (its name above it needs the width)
P2_PLAN_MARGIN = 20.0                    # m round a window's points (a drawing rule, not data)
P2_LEG_TOP = 177.0                       # page 2: the plans' legend, first baseline (right under the plans)
P2_CARD_GAP = 6.0                        # page 2: gutter between the hub cards
P2_CARD_WT = dict(walk=1.0, hidden=1.25, gateway=0.6)   # card widths in proportion (the transit card holds two stops)
P2_CARD_BOT = 83.0                       # page 2: the cards end here at the lowest
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


def north_arrow(pg, x, y, a, size=5.0):
    """v2: a north arrow beside the scale bar, never on the plan; a = north's direction on the page (radians from
    +x). v7 (G-R4-9): THE north arrow of common/keymap.py (north_items: the arrow and N only, no plate); (x, y) =
    the foot of its shaft"""
    fill_fn, line_fn, text_fn, _o = cl_draw_fns(pg)
    basemap_draw(north_items(x, y, a - math.pi / 2.0, size), lambda p: p, fill_fn, line_fn, text_fn)


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
        mul = st["layer"] == "proj_tint"
        for grp in ([[R_] for R_ in rs] if nonzero else [rs]):
            if grp:
                pg.path(grp, fill=col(hx, alpha), mul=mul)

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


def cl_map(pg, page, T, sbox, den, project, base_extra=(), clip=True, allow=()):
    """v7 (G-R4-4; replaces bm_draw): one map through THE draw order (map_draw): the muted base of the box sbox
    (survey m) at 1:den (ml_base: light houses with closed outlines, streets, the stream) + base_extra (e.g. the
    covered course), then project {layer: items} (proj_tint multiplied, proj_lines, proj_vegetation, proj_marks),
    the study line, clipped to the study area when clip. The caller clips the PDF to its window and draws markers
    and labels after it (they are the top layers). Returns (n base items, the study rings)."""
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
             order_fn=order_fn, log=CL_LOG)
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
CORRIDOR_LW = 0.8                        # v7 (P08.2): the project corridor: one line along the stream (mm) with a
CORRIDOR_BAR = 3.0                       # bar this long across each end (mm); drawing rules, not data
SHOP_C = "B5832F"                        # v7 (P08.1): today's shop streets, ochre (palette autumn tone), 1.4 mm
SHOP_LW = 1.4
NEATLINE = 0.25 * 25.4 / 72.0            # v6 (G17, D4): a map's neatline, 0.25 pt; no other frame anywhere
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


def page_framework(L):
    """v4 (D8 b): page 1, booklet p.08: the framework diagram on the shared basemap, the whole site frame at 1:10,000
    on the frame's axes, its key beside it; who the project brings (G7) under it; the seven reasons as tiles at the
    bottom (not in the booklet). v7 (round 4, P08.1): redrawn on the round 4 modules (spec S5); every text is
    registered and the page's collision test RAISES (G-R4-1)."""
    pg = Page(420, 297, "p08")
    SRC_KEY[:] = []
    header(pg, "THE STREAM JOINS THE TOWN WHERE THE SHOPS ALREADY ARE",
           "shops on **two streets** · the stream **hidden** where the main road meets it · the project: **one "
           "corridor** along the stream, **hubs** at the bridges")
    framework_map(pg, L)
    who_panel(pg, L)
    reasons_tiles(pg)
    pg.check_text()
    PAGE_SRC[0] = list(SRC_KEY)
    return pg


def framework_map(pg, L):
    """v7 (round 4, P08.1-P08.3, G-R4-1/2/4/7/9/11; spec S5): the whole corridor on the site frame at 1:10,000 on the
    frame's axes, through THE draw order (cl_map / map_draw): the muted base; the study area tinted D9 (the project's
    ground, multiplied: the houses read through); TODAY the shop streets (movement_framework.json spines, else the
    main spine) in ochre on a white casing; THE PROJECT one clean line along the stream from the study area's upstream
    end to its downstream end (corridor_line) with a bar across each end (P08.2: no band, no arrowheads); the study
    line; then the hubs as numbered markers 1-5 (the p10 numbers, colour = hub kind), the one place the main road
    meets the stream; the names of the stream and the shop streets where a free spot is next to them (else they stand
    in the legend only). Legend beside the map, top-aligned (G-R4-3): what is drawn, the corridor's length
    (calculated), the hubs by number and real name; the shops headline under it (no widow, P08.3); north arrow and
    scale bar under the map. PLAN_BOX "fw" / "fw_key" give the booklet crop."""
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
    tx = step(pg, 1, mx, my + fh_ + 6.5)
    fit(pg, ("THE WHOLE CORRIDOR · THE SHOP STREETS, THE HIDDEN STREAM AND THE PROJECT FROM END TO END " +
             cite(SRC_MAIN) + " " + cite(SRC_SHOPS)).strip(), tx, my + fh_ + 6.5, 10, mx + fw_ - tx, C["ink"], True)
    pg.keep(box_, "map", MAP)
    sbox = frame_box(f, f["u0"], f["v0"], f["u0"] + f["w"], f["v0"] + f["h"])
    m_mm = PLAN_DEN / 1000.0                              # survey m per page mm
    # base extra: the stream hidden under the town (the reference line's covered pieces), dashed
    P, cov = stream_ref()
    covered = [("line", R_, C["water_deep"], 0.8, [1.6, 0.9], 1.0) for c_, R_ in clip_runs(P, sbox, cov) if c_]
    # TODAY: the shop streets (not a proposal: drawn whole, not clipped)
    spines = fw.get("spines") or [dict(label=landmark_name("bankalar_caddesi") + u" - " +
                                       landmark_name("kinik_caddesi"), runs=[MAIN_SPINE])]
    if not fw.get("spines"):
        BM_NOTE.append("FLAG: no movement_framework.json (site board v51+): the main spine stands in for the shop "
                       "streets")
    runs_ = [[tuple(p) for p in R_] for g in spines for R_ in g["runs"] if len(R_) >= 2]
    lines = [("line", R_, C["white"], SHOP_LW + 0.5, None, 1.0) for R_ in runs_] + \
            [("line", R_, SHOP_C, SHOP_LW, None, 1.0) for R_ in runs_]
    # THE PROJECT: one corridor line, the study area's whole length along the stream, a bar across each end
    cor = corridor_line(L)
    if cor and len(cor["P"]) >= 2:
        Q = cor["P"]
        lines.append(("line", Q, C["white"], CORRIDOR_LW + 0.5, None, 1.0))
        lines.append(("line", Q, SPINE_C, CORRIDOR_LW, None, 1.0))
        for a_, b_ in ((Q[0], Q[1]), (Q[-1], Q[-2])):
            ln = math.hypot(b_[0] - a_[0], b_[1] - a_[1]) or 1.0
            nx, ny = -(b_[1] - a_[1]) / ln * CORRIDOR_BAR / 2.0 * m_mm, (b_[0] - a_[0]) / ln * CORRIDOR_BAR / 2.0 * m_mm
            lines.append(("line", [(a_[0] - nx, a_[1] - ny), (a_[0] + nx, a_[1] + ny)], SPINE_C, CORRIDOR_LW, None,
                          1.0))
    else:
        BM_NOTE.append("FLAG: no study area (basemap or CL_STUDY): p.08 has no project corridor")
    KP = 72 / 25.4
    pg.ops.append("q %.2f %.2f %.2f %.2f re W n" % (mx * KP, my * KP, fw_ * KP, fh_ * KP))
    study = cl_study()
    nb, study = cl_map(pg, "p08", T, sbox, PLAN_DEN, {"proj_tint": ml_tint(study), "proj_lines": lines},
                       base_extra=covered, clip=False)
    pg.ops.append("Q")
    pg.rect(mx, my, fw_, fh_, stroke=C["ink"], lw=NEATLINE)
    # our lines are keeps for the labels (no name on the corridor or a shop street)
    for R_ in runs_:
        pg.keep([T(p) for p in R_], "line", "shop street")
    if cor:
        pg.keep([T(p) for p in cor["P"]], "line", "corridor")
    # the marks on top: the junction, then the hubs, numbered as on p10
    jx, jy = T((30058.0, 32047.0))                          # Kınık Caddesi over the covered stream (stop 3's place)
    disc(pg, jx, jy, 1.2, C["accent"], C["white"], 0.3)
    pg.keep((jx - 1.4, jy - 1.4, jx + 1.4, jy + 1.4), "marker", "junction")
    hubs = hub_list()
    seen = []
    for hb in hubs:
        hx, hy = T(hb["xy"])
        if inside((hx, hy)):
            cl_marker_free(pg, hx, hy, str(hub_no(hb)), hub_col(hb), 7.0, frame=frame, allow=(MAP,),
                           name="hub %d" % hub_no(hb))
            kd = "transit" if hb["transit"] else hb["kind"]
            if kd not in seen:
                seen.append(kd)
    # names next to their own line, where free (else in the legend only)
    named = []
    for g in spines:
        if not g.get("label") or g["label"] == "an unnamed street":
            continue
        Q = [q for q in (T(p) for p in max(g["runs"], key=len)) if inside(q)]
        if len(Q) > 1 and cl_place(pg, g["label"], Q[len(Q) // 2], 7.5, C["ink"], True, 1.2, frame, (MAP,)):
            named.append(g["label"])
    for c_, R_ in sorted([r_ for r_ in clip_runs(P, sbox, cov) if not r_[0]], key=lambda r_: -len(r_[1])):
        Q = [q for q in (T(p) for p in R_) if inside(q)]
        if len(Q) > 1 and cl_place(pg, place_name("stream"), Q[len(Q) // 2], 7.5, C["water_deep"], True, 1.6, frame,
                                   (MAP,)):
            break
    north_arrow(pg, mx + 6.5, my - 9.0, math.atan2(math.cos(f["ang"]), math.sin(f["ang"])), 5.0)   # v8.2: its N
    scale_bar(pg, mx + 13.0, my - 6.5, PLAN_DEN)          # was on the page margin (Aras 1 Nov 19:49): 4 mm right
    # the legend beside the map, top-aligned with it (G-R4-3)
    rows = []
    if nb:
        rows.append((sw_fill(BM_COL["water"], BM_COL["water_edge"]), place_name("stream")))
    rows.append((sw_line(C["water_deep"], 0.8, (1.6, 0.9)), place_name("stream") + ", covered"))
    rows.append((lambda p_, b: (p_.rect(b[0], b[1], b[2] - b[0], b[3] - b[1], fill=tint_hex(ML_TINT, 1.0 - ML_TINT_ALPHA)),
                                sw_line(BM_STUDY_LINE["colour"], BM_STUDY_LINE["width_mm"],
                                        tuple(BM_STUDY_LINE["dash_mm"]))(p_, b)),
                 "study area: the project's ground"))
    if cor:
        def sw_corridor(p_, b):
            ym = (b[1] + b[3]) / 2.0
            p_.line([(b[0] + 0.4, ym), (b[2] - 0.4, ym)], SPINE_C, CORRIDOR_LW)
            for x_ in (b[0] + 0.4, b[2] - 0.4):
                p_.line([(x_, ym - 1.3), (x_, ym + 1.3)], SPINE_C, CORRIDOR_LW)
        rows.append((sw_corridor, u"the project corridor along the stream, %s m" % fmt(int(round(cor["m"] / 10.0)) * 10)))
    rows.append((sw_line(SHOP_C, SHOP_LW), u"shop streets today: " + u", ".join(
        g["label"] for g in spines if g.get("label") and g["label"] != "an unnamed street")))
    rows.append((sw_mark(lambda p_, x, y: disc(p_, x, y, 1.1, C["accent"], C["white"], 0.3)),
                 "the main road meets the stream, covered"))
    for hb in hubs:
        kd = "walking hub" if hb["kind"] == "walk" else ("main transit hub" if hb["transit"] else
                                                         ("gateway" if hb["kind"] == "gateway" else "hub"))
        rows.append((sw_mark(lambda p_, x, y, hb=hb: cl_marker(p_, x, y, str(hub_no(hb)), hub_col(hb), 7.0,
                                                               name="legend hub %d" % hub_no(hb))),
                     u"%s · %s" % (hb["title"], kd)))
    lx = box_[2] + 5.5
    lb = cl_legend(pg, rows, lx, box_[3], 406.0 - lx)
    # the shops figure: one headline value and one line under the legend (G4), wrapped without a widow (P08.3)
    sf = shop_figures()
    hy = lb[1] - 5.6
    pg.text("%d of %d shops" % (sf["covered_reach"], sf["by_stream"]), lx, hy, 12, C["accent"], True)
    ye = cl_para(pg, "by the stream sit on the covered %d m, where the main road meets it" % sf["covered_reach_m"],
                 lx, hy - 4.8, 7.5, 406.0 - lx, C["ink"])
    PLAN_BOX["fw_key"] = (lx, ye, 406.0, box_[3])
    return []


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
    under it (key_flow) and one line of conclusion, made from the same data, on the title line."""
    x0, ty, W = WHO_BOX
    x1 = x0 + W
    tx = step(pg, 2, x0, ty)
    pg.text("WHO COMES TO THE STREAM, AND WHEN", tx, ty, 9, C["ink"], True)
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
    if seas:
        ms = act_months(seas[0])
        low = bool(river) and (min(range(12), key=lambda i: river[i]) + 1) in ms
        concl = (u"the **dry bed** adds %s, %s-%s%s" % (seas[0]["name"].lower(), MON[ms[0] - 1], MON[ms[-1] - 1],
                                                       u", when the stream runs lowest" if low else u""))
        concl = concl[:1].upper() + concl[1:]
        wc = sum(text_w(p_, 8, i % 2 == 1) for i, p_ in enumerate(concl.split("**")))
        rich(pg, concl, x1 - wc, ty, 8, C["ink2"])
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
    ke = key_flow(pg, ent, x0, yb - 4.6, x1)              # v7: the key in one flowing row under the calendar
    PLAN_BOX["who"] = (x0, ke + 2.6, x1, ty + 4.0)


def reasons_tiles(pg):
    """the seven reasons the stream edge has no spine (v1.6 tiles, kept): pictogram, one figure, keywords"""
    rx, ry, rw, rh = P1_TILES
    tx = step(pg, 3, rx, ry + rh + 3.5)
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
    baseline under the last line."""
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
    if hb["kind"] in ("walk", "hidden"):                   # the levels: a small section with its keys beside it
        gw, gh = 24.0, 15.0
        hub_glyph(pg, hb["kind"], x, y + 2.6, gw, gh)
        if hb["kind"] == "walk":
            kws = [("DRY HUB", True), ("street level, above Q500", False), ("SUB-HUB in the bed", True),
                   ("open Jul-Sep · shut in floods " + cite(SRC_WET), False)]
        else:
            kws = [("HIDDEN STREAM SQUARE", True), ("water line in the paving over the culvert " + cite(SRC_HIDDEN),
                                                    False),
                   (landmark_name("kizil_avlu").replace(u"i", u"İ").upper() + u" TUNNEL MOUTHS", True),
                   ("a viewing edge", False)]
        ky = y
        for j, (s_, b_) in enumerate(kws):
            if j and b_:
                ky -= 0.8
            ky = cl_para(pg, s_.strip(), x + gw + 2.0, ky, 7.5, w - gw - 2.0, C["ink"], b_, lead=3.2)
        y = min(y + 2.6 - gh, ky + 3.2 - 0.6) - 4.4
    else:
        y = cl_para(pg, "GATEWAY OUT · no hub square", x, y, 8, w, C["ink"], True) - 1.6
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


def scale_seg(den):
    """v6: the segment length (m) of a scale bar at 1:den (four segments)"""
    return 20.0 if den <= 2500 else (50.0 if den <= 5000 else (100.0 if den <= 10000 else 200.0))


def hub_plan_layout(f, wins):
    """v6 (P09.1): one scale for the row of plans: the largest standard scale (R28_SCALES) at which every window holds
    its points with P2_PLAN_MARGIN round them on the site frame's axes, each at least P2_PLAN_MIN_W wide, side by
    side within the row and the plans' height (P2_PLAN); the width left over is shared out in proportion (more
    context round each place). Sets each window's box (page mm), u0, v0 (frame axes, m) and den; returns den."""
    x0, top, ph, gap = P2_PLAN
    ext = []
    for w in wins:
        uv = [frame_uv(f, p) for p in w["pts"]]
        ext.append((min(q[0] for q in uv) - P2_PLAN_MARGIN, max(q[0] for q in uv) + P2_PLAN_MARGIN,
                    min(q[1] for q in uv) - P2_PLAN_MARGIN, max(q[1] for q in uv) + P2_PLAN_MARGIN))
    avail = P2_PLAN_W - gap * (len(wins) - 1)
    for den in R28_SCALES:
        k = 1000.0 / den
        ws = [max(P2_PLAN_MIN_W, (e[1] - e[0]) * k) for e in ext]
        if sum(ws) <= avail and all((e[3] - e[2]) * k <= ph for e in ext):
            break
    else:
        BM_NOTE.append("FLAG: p.10 hub plans: no standard scale holds every hub's places in the row; drawn at 1:%s, "
                       "some places fall outside their plan" % fmt(den))
    sw_ = sum(ws)
    ws = [w_ * avail / sw_ for w_ in ws]
    x = x0
    for w, e, w_ in zip(wins, ext, ws):
        uc, vc = (e[0] + e[1]) / 2.0, (e[2] + e[3]) / 2.0
        w["u0"], w["v0"] = uc - w_ / 2.0 / k, vc - ph / 2.0 / k
        w["box"], w["den"] = (x, top - ph, x + w_, top), den
        x += w_ + gap
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
    its locator number and real name (P10.2). Returns the set of things drawn (for the legend)."""
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
    # over the plan: its locator number and real name (P10.2)
    hy = y1 + 2.6
    _b, r_ = cl_marker(pg, x0 + 2.0, hy + 1.0, str(w["no"]), hub_col(hb), 7.0, name="head " + MAP)
    nx = x0 + 2.0 + r_ + 1.2
    nm = w["name"] or hb["title"]
    lns = cl_wrap(nm, 8, x1 - nx, True)
    if len(lns) > 2 and hb["pt"] in ("K3", "K4", "K5", "K6"):
        lns = cl_wrap(bridge_name(hb["pt"], short=True), 8, x1 - nx, True)
    pg.tgroup()
    for i, ln in enumerate(lns):
        pg.text(ln, nx, hy + 3.4 * (len(lns) - 1 - i), 8, C["ink"], True)
    pg.tgroup(False)
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
        for q in sq.get("trees") or []:
            proj["proj_vegetation"].append(("fill", [[(q[0] + tr_ * math.cos(a_ * math.pi / 8.0),
                                                       q[1] + tr_ * math.sin(a_ * math.pi / 8.0)) for a_ in range(16)]],
                                            C["green_mid"], 1.0, True))
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
    KP = 72 / 25.4
    pg.ops.append("q %.2f %.2f %.2f %.2f re W n" % (x0 * KP, y0 * KP, (x1 - x0) * KP, (y1 - y0) * KP))
    nb, _st = cl_map(pg, "p10", T, sbox, den, proj, base_extra=covered, clip=True)
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
    pg.ops.append("Q")
    pg.rect(x0, y0, x1 - x0, y1 - y0, stroke=C["ink"], lw=NEATLINE)
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


def hub_keymap(pg, f, wins):
    """v7 (round 4, P10.1 P10.2, G-R4-4/7/9; spec S5): the key map of p10 at the left of the plan row (P2_KEY), north
    up, a diagram (no scale bar): the shared km_map (muted base, the study line, the main street and place names
    placed clear of each other), each plan window as a red frame (KM_ZOOM, the R01 red) and one locator marker per
    hub next to its frame(s) (the number over its plan and on its card), drawn through map_draw. A title over it."""
    kx, ky, kw, kh = P2_KEY
    MAP = "keymap p10"
    study = cl_study()
    polys = []
    for w in wins:
        x0, y0, x1, y1 = w["box"]
        k = 1000.0 / w["den"]
        u0, v0 = w["u0"], w["v0"]
        u1, v1 = u0 + (x1 - x0) / k, v0 + (y1 - y0) / k
        polys.append((w, [frame_xy(f, u0, v0), frame_xy(f, u1, v0), frame_xy(f, u1, v1), frame_xy(f, u0, v1)]))
    pts = [p for R_ in study for p in R_] + [p for _w, Q in polys for p in Q]
    bx0, by0 = min(p[0] for p in pts), min(p[1] for p in pts)
    bx1, by1 = max(p[0] for p in pts), max(p[1] for p in pts)
    d_ = 0.06 * max(bx1 - bx0, by1 - by0)
    pg.text("Where each plan is", kx, P2_PLAN[1] + 2.6, 8, C["ink"], True)
    km = km_map([], kw, kh, box=(bx0 - d_, by0 - d_, bx1 + d_, by1 + d_), log=BM_NOTE)
    X = lambda q: (kx + q[0], ky + q[1])
    T = lambda p: X(km["T"](p))
    frames = [("line", Q + [Q[0]], KM_ZOOM["colour"], KM_ZOOM["lw"] + 0.1, None, 1.0) for _w, Q in polys]
    KP = 72 / 25.4
    pg.ops.append("q %.2f %.2f %.2f %.2f re W n" % (kx * KP, ky * KP, kw * KP, kh * KP))
    pg.keep((kx, ky, kx + kw, ky + kh), "map", MAP)
    fill_fn, line_fn, text_fn, order_fn = cl_draw_fns(pg, (MAP,))
    mk_at = []                                            # v8.2 (Aras 1 Nov 19:49: names under the hub 4 marker):
    for w, Q in polys:                                    # a name within 5 mm of a hub marker's place is left out
        cs_ = [T(((Q2[0][0] + Q2[2][0]) / 2.0, (Q2[0][1] + Q2[2][1]) / 2.0)) for w2, Q2 in polys if w2["no"] == w["no"]]
        mk_at.append((sum(c_[0] for c_ in cs_) / len(cs_), sum(c_[1] for c_ in cs_) / len(cs_)))
    names_ = []
    for it in km["names"]:
        c_ = T(it[2])
        hw_, hh_ = text_w(it[1], it[3] / 0.3528) / 2.0 + 5.0, it[3] / 2.0 + 5.0
        if any(abs(c_[0] - m_[0]) < hw_ and abs(c_[1] - m_[1]) < hh_ for m_ in mk_at):
            BM_NOTE.append(u"key map p10: name '{}' left out (on a hub marker)".format(it[1]))
            continue
        names_.append(it)
    map_draw("p10 key", T, fill_fn, line_fn, text_fn, km["base"], {"proj_marks": frames, "proj_labels": names_},
             study=km.get("study_rings") or study, clip=False, order_fn=order_fn, log=CL_LOG)
    frame = (kx + 0.8, ky + 0.8, kx + kw - 0.8, ky + kh - 0.8)
    done = []
    for w, Q in polys:                                    # one marker per hub, beside its frame(s)
        if w["no"] in done:
            continue
        done.append(w["no"])
        cs = [T(((Q2[0][0] + Q2[2][0]) / 2.0, (Q2[0][1] + Q2[2][1]) / 2.0)) for w2, Q2 in polys if w2["no"] == w["no"]]
        ax, ay = sum(c_[0] for c_ in cs) / len(cs), sum(c_[1] for c_ in cs) / len(cs)
        cl_marker_free(pg, ax, ay, str(w["no"]), hub_col(w["hub"]), 6.5, frame=frame, allow=(MAP,),
                       name="key hub %d" % w["no"], on_point=False)
    pg.ops.append("Q")
    pg.rect(kx, ky, kw, kh, stroke=C["ink"], lw=NEATLINE)


def key_flow(pg, entries, x0, y, x1, size=7.0, lead=4.4, sw=5.0):
    """v6 (G1, P09.1): a key in flowing rows under its drawings: entries [(draw(pg, swatch box) or None, words)] left
    to right from (x0, baseline y), a new row where the next entry would pass x1; returns the baseline under the
    last row. v7: rows 4.4 mm apart (markers in the samples)"""
    x = x0
    for draw, s_ in entries:
        w_ = (sw + 1.4 if draw else 0.0) + text_w(s_, size)
        if x > x0 and x + w_ > x1:
            x, y = x0, y - lead
        if draw:
            draw(pg, (x, y - 0.4, x + sw, y + 2.0))
            x += sw + 1.4
        pg.text(s_, x, y, size, C["ink"])
        x += text_w(s_, size) + 4.0
    return y - lead


def page_spine(L):
    """v5 / v6 / v7 (round 4, P10.1-P10.6, G-R4-1/2/3/4/7/9/11; spec S5): booklet p.10, the sheet page shown whole.
    (1) The key map (hub_keymap) at the left of a row of plans at one scale in stream order (hub_windows,
    hub_plan_layout, hub_plan), each with its locator number and name over it; one scale bar and north arrow on the
    title line; (2) the plans' legend right under them (P10.3: nothing between a drawing and its legend), then the
    hub cards in five columns (hub_card, numbered as the key map); (3) the flood rule as a stair of its three
    levels; which bank; the producers' market with the two farm areas this page prints (M10 facts). No frames
    (G17). Every text is registered; the page's collision test RAISES (G-R4-1)."""
    pg = Page(420, 297, "p10")
    SRC_KEY[:] = []                               # v1.6: each page has its own numbered key
    header(pg, "THE STREAMSIDE SPINE, HUB BY HUB",          # v2: no length (Prompt 3: reach, not a fixed line)
           "five **bridge places** on existing bus stops · walking hubs with a **sub-hub in the bed** · one transit hub")
    hubs = hub_list()
    f = site_frame(L.get("ctx") or {})
    wins = hub_windows(L, hubs)
    den = hub_plan_layout(f, wins)
    PLAN_BOX["spine_den"] = den
    tx = step(pg, 1, 14.0, P2_TITLE_Y)
    pg.text(("THE BRIDGE PLACES IN PLAN, UPSTREAM TO DOWNSTREAM · 1:%s " % fmt(den) + cite(SRC_BUS)).strip(), tx,
            P2_TITLE_Y, 9, C["ink"], True)
    sx_ = 406.0 - (4 * scale_seg(den) * 1000.0 / den + 9.0 + text_w("1:%s" % fmt(den), 7))
    scale_bar(pg, sx_, P2_TITLE_Y, den)                   # one scale bar and north arrow for the row (G1)
    north_arrow(pg, sx_ - 6.0, P2_TITLE_Y - 2.5, math.atan2(math.cos(f["ang"]), math.sin(f["ang"])), 5.0)
    seen = set()
    for w in wins:
        seen |= hub_plan(pg, L, f, w)
    hub_keymap(pg, f, wins)
    BM_NOTE.append("p.10 hub plans: %d plans at 1:%s in stream order (%s); streamside walks not drawn (P10.5)" % (
        len(wins), fmt(den), ", ".join(w["name"] or w["hub"]["title"] for w in wins)))
    # (2) the plans' legend right under them (P10.3), only what they draw, and the card keys
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
        ent.append((sw_mark(lambda p_, x, y: disc(p_, x, y, 1.0, C["green_mid"])),
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
    ke = key_flow(pg, ent, 14.0, P2_LEG_TOP, 406.0)
    # the cards, in five columns under the legend (P10.3, P10.4), numbered as the key map and the plans
    ytop = ke + 4.4 - 4.0
    wts = [P2_CARD_WT.get("hidden" if hb["kind"] == "hidden" else hb["kind"], 1.0) for hb in hubs]
    unit = (392.0 - P2_CARD_GAP * (len(hubs) - 1)) / sum(wts)
    cx, lowest = 14.0, ytop
    for hb, wt in zip(hubs, wts):
        cw = wt * unit
        yl = hub_card(pg, hb, cx, ytop, cw)
        if yl + 2.4 < P2_CARD_BOT:
            BM_NOTE.append("FLAG: p.10 card %s runs %.1f mm below its space (G2)" % (hb["title"], P2_CARD_BOT - yl - 2.4))
        lowest = min(lowest, yl)
        cx += cw + P2_CARD_GAP
    PLAN_BOX["hubs"] = (14.0, lowest, 406.0, P2_TITLE_Y + 4.0)

    # (2) the flood rule as a stair of its three levels (highest first), each level's rules on its step
    fx, fy0, fst = P2_FLOOD
    tx = step(pg, 2, fx, P2_LOW)
    pg.text("WHAT STANDS WHERE: THE FLOOD RULE " + cite(SRC_RULES), tx, P2_LOW, 9, C["ink"], True)
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
    # (3) which bank: per piece a glyph of the bank the spine takes, then paired bars NE / SW (people = home floors,
    # modern = buildings of 3+ floors, within 250 m)
    bkx, by0, bst = P2_BANK
    tx = step(pg, 3, bkx, P2_LOW)
    pg.text("WHICH BANK THE SPINE TAKES · WITHIN 250 M", tx, P2_LOW, 9, C["ink"], True)
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
    # the producers' market: the farm areas that feed it (M10: printed on this page only), read live
    ln = L["lands"]
    mkx = P2_MARKET
    mkw = 406.0 - mkx
    mk = [g for g in FUNCS if g["n"] == 5][0]
    pg.text("PRODUCERS' MARKET", mkx, P2_LOW, 9, C["ink"], True)
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
    PLAN_BOX["market"] = (mkx, yy - 9.0, 406.0, P2_LOW + 4.0)
    pg.check_text()                               # v7 (G-R4-1): any text collision on p.10 RAISES
    PAGE_SRC[1] = list(SRC_KEY)
    return pg


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
                script="bergama_city_link_v7.py", version=VERSION, run_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                spine=SPINE, functions=[dict([(k, f.get(k)) for k in ("n", "name", "where", "xy", "stage", "who", "grows", "ch", "bank")] +
                                             [("hub", "sub-hubs" if f["n"] == 8 else hub_of.get(f["n"]))])
                                        for f in FUNCS + [EVENTS]],
                chainage=CH, main_spine=MAIN_SPINE, shops=shop_figures(), hubs=hubs, main_transit_hub=MAIN_TRANSIT_HUB,
                hubs_source=SRC_HUBS + "; " + SRC_BUS,
                note="survey coordinates (m); spine offsets are schematic for the movement network")

# ------------------------------------------------------------------ v1.8: A3 booklet = crops of this sheet (booklet/CROP_SPEC.md)
#@include ../common/booklet_assets.py

BK_DROP = [r"^\[\d+(,\d+)*\]$"]                      # the sheet's source numbers: the booklet has its own source list


def booklet_export(out_dir):
    """v1.8 (Aras 25 Oct 21:47): one crop per panel of the two sheet pages in booklet/blocks.json; the assembler cuts
    each rect out of the sheet PDF. Rects come from the layout numbers P1_* / P2_* (mm, y up here; written y down).
    v1.11: the booklet shows both pages whole (PLAN.py p9 / p17); the crops follow the new layout; the sources the
    [n] marks refer to are in "sheet_sources" (the sheet no longer prints them)."""
    bk = BkBlocks(out_dir, "CityLink", VERSION)
    H = 297.0

    def crop(bid, page, x0, y0, x1, y1, caption, legend=None, scale_den=None, drop=None, bk_w=None):
        bk.crop(bid, OUT_PDF, (x0, H - y1, x1, H - y0), caption=caption, scale_den=scale_den, legend=legend, page=page,
                drop=BK_DROP + (drop or []))
        if bk_w:                                   # v3: drawn for the booklet page at 1:1 (its width there), as the
            bk.d["blocks"][bid]["bk_w"] = round(bk_w, 3)   # masterplan's mp_plan: the booklet keeps its scale
    mk = lambda p_, *ss: " ".join("[%d]" % (PAGE_SRC[p_].index(s_) + 1) for s_ in ss if s_ in PAGE_SRC.get(p_, []))
    # v5 (revision 30 Oct 2026): page 1 (booklet p.08) = the framework with its legend beside it and its scale bar
    # under it (cl_framework, drawn at 1:1 for the booklet width, bk_w), who comes and when (cl_who: calendar and its
    # key) and the reasons (cl_reasons). The legends are drawn on the sheet next to their drawings (G1), so the crops
    # carry none of their own.
    px0, py0, px1, py1 = PLAN_BOX.get("fw") or (FW_MAP[0], FW_MAP[1], FW_MAP[0] + 284.5, FW_MAP[1] + 52.9)
    kb = PLAN_BOX.get("fw_key") or (px1, py0, 406.0, py1)
    crop("cl_framework", 0, px0 - 0.5, min(py0 - 11.5, kb[1] - 1.0), 406.0, py1 + 10.0,   # v6: the whole corridor
         ("The whole corridor: the shop streets, the hidden stream and the project from end to end " +
          mk(0, SRC_MAIN, SRC_SHOPS)).strip(), bk_w=406.0 - (px0 - 0.5))
    wb = PLAN_BOX.get("who") or (WHO_BOX[0], 62.0, WHO_BOX[0] + WHO_BOX[2], WHO_BOX[1] + 4.0)
    crop("cl_who", 0, wb[0] - 0.5, wb[1], wb[2] + 0.5, wb[3],
         ("Who comes to the stream, and when " + mk(0, SRC_WHO_T, SRC_WHO_L, SRC_WHO_S1, SRC_WHO_S2)).strip(),
         bk_w=wb[2] - wb[0] + 1.0)
    x0, y0, w, h = P1_TILES
    crop("cl_reasons", 0, x0, y0 - 1.0, x0 + w, y0 + h + 6.0, "Seven reasons the stream edge has no spine")
    # page 2 (booklet p.10, shown whole): v6 the hub plans with their cards and key (cl_hubs; the overview map
    # cl_spine is gone, D1; v7: with the key map at its left, the legend under the plans and the cards under it),
    # the flood rule (cl_flood), which bank (cl_bank) and v5 the producers' market (cl_market). Ids unchanged (S9).
    hb_ = PLAN_BOX.get("hubs") or (14.0, P2_CARD_BOT, 406.0, P2_TITLE_Y + 4.0)
    crop("cl_hubs", 1, hb_[0] - 0.5, hb_[1], hb_[2] + 0.5, hb_[3],
         "Five bridge places in plan, upstream to downstream, and what each holds", scale_den=PLAN_BOX.get("spine_den"))
    fx, fy0, fst = P2_FLOOD
    crop("cl_flood", 1, fx - 1.0, fy0 - (len(FLOOD) - 1) * fst - 10.0, P2_BANK[0] - 4.0, P2_LOW + 5.0,
         "What stands where: the flood rule")
    bkx, by0, bst = P2_BANK
    crop("cl_bank", 1, bkx - 0.5, by0 - (len(SPINE) - 1) * bst - 14.0, P2_MARKET - 3.0, P2_LOW + 5.0,
         "Which bank: home floors and 3+ floor buildings within 250 m")
    mb = PLAN_BOX.get("market") or (P2_MARKET, 30.0, 406.0, P2_LOW + 4.0)
    crop("cl_market", 1, mb[0] - 0.5, mb[1], mb[2] + 0.5, mb[3] + 1.0, "The producers' market")
    bk.d["sheet_sources"] = dict((str(p), ["[%d] %s" % (i + 1, s) for i, s in enumerate(v)]) for p, v in sorted(PAGE_SRC.items()))
    bk.save()
    return ""

def build(dir_):
    L = live()
    # 25 Oct 10:19 (no double runs): the site board ran BEFORE this script and drew the spine from the last
    # city_link_results.json (or its built-in copy); v6.2: the masterplan builds the spine itself (common/city_spine.py).
    # The bank choice comes from survey building counts, so it only changes when the survey changes; if it did, say so.
    try:
        with open(bg_first([os.path.join(RES_DIR, OUT_JSON), os.path.join(dir_, OUT_JSON)]), "r", encoding="utf-8") as f:
            prev, prev_src = json.load(f).get("spine_banks"), "the last run"
    except Exception:
        prev = dict((pc["id"], bank_of(BANK_VOTE[pc["id"]])[0] if pc.get("side") == "auto" else "over") for pc in SPINE)
        prev_src = "the built-in copy"
    L["bank_note"] = ("" if prev == L["sides"] else
                      "\nWARNING: the spine bank changed from %s (%s -> %s): the site board of this run drew "
                      "the old one; press the chain once more." % (prev_src, prev, L["sides"]))
    BM_NOTE[:] = []
    del CL_LOG[:]                                         # v7: this run's overlap / layer lines
    tp_log_lines()                                        # v8.1: no WARNING lines left from an earlier run
    pages = [page_framework(L), page_spine(L)]            # v4 (D8 b) / v7: booklet p.08 and p.10
    write_pdf(pages, os.path.join(dir_, OUT_PDF))
    os.makedirs(RES_DIR, exist_ok=True)
    with open(os.path.join(RES_DIR, OUT_JSON), "w", encoding="utf-8") as f:
        json.dump(results(L), f, ensure_ascii=False, indent=1)
    return L

def main():
    t0 = time.time()
    os.makedirs(OUT_DIR, exist_ok=True)
    try:
        L = build(OUT_DIR)
    except PermissionError:
        return "The PDF is open in another program. Close it and press again: " + os.path.join(OUT_DIR, OUT_PDF)
    bk = "\ntrigger: " + (TRIG_WHY[0] or "-")                 # v7 (round 4 S1)
    bk += "".join("\n" + n_ for n_ in CL_LOG + tp_log_lines())   # v8.1: + the layout WARNING lines
    bk += "".join("\n" + n_ for n_ in [L.get("fw_note"), L.get("mp_note")] + sorted(set(BM_NOTE)) if n_)   # v4
    bk += "\nopen points (not on the sheet): market edge, decks and stall sizes (masterplan); hub plane-tree irrigation " \
          "from storage (water board); ridership at the bus stops (none found, h03); the sub-hub's bed edges and the " \
          "terraces are not in masterplan_results.json (p.10 draws the hub squares, their trees and the stepping stones)"
    try:                                           # v1.7: a booklet error never stops the sheets; it goes into the log
        n_ = booklet_export(OUT_DIR)
        bk += ("\nbooklet: " + n_) if n_ else ""
    except Exception as ex_:
        bk += "\nbooklet: ERROR %s: %s" % (type(ex_).__name__, ex_)
    bk += "".join("\n" + t_ for t_ in bg_tidy_output("Bergama_city_link_analysis"))   # 27 Oct: output/ = PDFs only
    t = time.strftime("%H:%M:%S")
    return "%s  %s\n%s  %s\nfigures: %s; %s; %s\ncity link %s, %.1f s%s%s" % (OUT_PDF, t, OUT_JSON, t, L["wb_src"], L["mv_src"], L["ctx_note"], VERSION, time.time() - t0, L.get("bank_note", ""), bk)

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
        _sc.sticky["bergama_city_link_log_status" + _ik] = ("ERROR" if _sc.sticky["bergama_city_link_log" + _ik].startswith(("ERROR", "The PDF is open")) else time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky["bergama_city_link_log_done" + _ik] = done_text(True, not _sc.sticky["bergama_city_link_log_status" + _ik].startswith("ERROR"), time.time() - _t0)
        _sc.sticky["bergama_city_link_log_ver" + _ik] = VERSION
    if _sc.sticky.get("bergama_city_link_log_ver" + _ik) != VERSION:   # v2 (Aras 27 Oct 15:35): a newly pasted version
        for _s in ("", "_status", "_done"):                              # shows itself at once, idle, without the old
            _sc.sticky.pop("bergama_city_link_log" + _s + _ik, None)      # run's time or log
    done = _sc.sticky.get("bergama_city_link_log_done" + _ik, "idle")   # 25 Oct 10:20: stays after the run; wire into the next script's run (one-click chain)
    log = _sc.sticky.get("bergama_city_link_log" + _ik, "Press the Button to export to " + OUT_DIR)
    print(log)               # 25 Oct 12:10: the canvas's log output is Grasshopper's "out" (printed text): print the log
    try: ghenv.Component.Message = "CityLink " + VERSION + " · " + _sc.sticky.get("bergama_city_link_log_status" + _ik, "idle")   # Aras 25 Oct 09:44
    except Exception: pass
else:
    print(write_log(main()))
