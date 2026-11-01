# CURRENT VERSION: bergama_city_link_v9.py = v9 (round 5, session S9, 2 Nov 2026: "produce then compose" (G-R5-12): no sheet PDF, no crops; p08 and p10 exported as items for the booklet; P08.1-P08.3, P10.1-P10.4, C1, C2, C10, CHK-12; what changed: NEW IN v9 below; v8.2: p08 north arrow off the margin, p10 key names off the hub markers, flood lines 3.5 mm apart; v8.1 / v8: layout checks and text collisions are WARNING lines, the run goes on; v7: round 4 S5)
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
# Nothing is written to output/ (C2). How we know it ran: the component text reads "CityLink v9 · HH:MM · n s"; the
# log's head is "city link v9 · <time> · <s> s", then "<n> warnings" (= the WARNING lines listed right under it),
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

VERSION = "v9"  # v9 2 Nov (round 5 S9): items for the booklet, no sheet PDF (NEW IN v9 above); v8.2 1 Nov 22:10 (Aras 19:49): p08 north arrow off the margin, p10 key names off the hub markers, flood lines 3.5 mm apart; v8.1 1 Nov 21:40 (Aras 19:33): every layout check that stopped the run (text size, lines, column width, rows, legend room) is a WARNING line and an orange warning; 6.00 pt no longer counts as under 6.0; v8 1 Nov 20:55: text collisions are orange warnings with one WARNING line each, the run goes on (Aras 1 Nov 17:11 + 18:52); v7 (round 4, S5, 1 Nov 2026): p08 and p10 redrawn on the shared round 4 modules (see NEW IN v7); v6.5 fix 1 Nov 08:30: only the component's own inputs can start it (a True setting inside the script no longer does); v6.4 fix 1 Nov 08:20: chain trigger keyed to each solve (Rhino keeps globals), so the chain continues after ZoneBase; v6.3 fix 1 Nov: a pasted or rewired component no longer runs by itself (chain trigger notes the wire on its first solve)
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
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != {'STREAM_REF': '6462357102432c243b7a34f595c055c7', 'SHOPS_XY': '938d12716e4355018e4de86927b3b4ab', 'LEVELS': '3cc5394beb1de45118b6226d608a766b', 'NAMES': '0ec3cbab34964fea25289ca36d8bd453', 'FACTS': 'e402c1370c04b7b8df8f86c4eccbf011'}.get(name):
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
             "regular": "BCB794", "selfbuilt": "DCD5C2", "large": "FAF8F1", "construction": "E6E0C8"}
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
    """round 5 (S2): a basemap building's key-map colour by its urban fabric (format 2 "fabric"; "regular" when the
    file has none), annexes paler (the p02 rule), mixed BM_KEY['fabric_light'] toward the paper"""
    c = BM_FABRIC.get(b.get("fabric") or "regular", BM_FABRIC["regular"])
    if b.get("annex"):
        c = _bm_mix(c, BM_KEY["paper"], BM_KEY["annex"])
    return _bm_mix(c, BM_KEY["paper"], BM_KEY["fabric_light"] if light is None else light)


class _BmIt(tuple):
    """round 5 (S2, G-R5-8): a basemap item that knows its map layer (.layer, a map_layers ML_LAYERS name): reads as
    the plain tuple everywhere; map_draw files a flat base list by it, so the stream is drawn above every tint"""
    pass


def _bm_tag(t, layer):
    o = _BmIt(t)
    o.layer = layer
    return o


# contours coloured to the relief (G-R4-4, U48): green tones, lighter = lower (palette 3C4733 and its 89986A tints)
BM_HEIGHT_RAMP = ("C9D6B0", "A7B68C", "89986A", "3C4733")
BM_LW = dict(contour=(0.07, 0.13), contour_topo=(0.08, 0.14), water_edge=0.18, covered=0.30, bridge=0.30,
             road_edge=0.12, osm_edge=0.08, her_edge=0.12, main=0.45, lane=0.22, path=0.10, river_osm=0.6,
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


def basemap_items(mode="detailed", override=None, box=None, D=None, split_buildings=False, scale_den=None):
    """the basemap of a drawing as items (bottom first; see the head of this file), in survey m. mode: "detailed",
    "simple", "minimal", "topographic" (02 §1), "base", "key" (M3, 30 Oct); override: layer changes for this drawing,
    a dict or a list of the layers to show (basemap_layers); box = (x0, y0, x1, y1) survey m: only what touches it
    (the caller clips to its frame); split_buildings=True gives every building its own fill item (for a page that
    fills even-odd only; default: nonzero fills in chunks); scale_den: the drawing's scale (1:scale_den) for the
    M11 roof marks of buildings "plan" / "plan_faint" (default 1:5,000). [] without data."""
    D = D if D is not None else basemap_load()
    if not D:
        return []
    # the same request in one run is made once and copied (Aras 29 Oct 19:18: build once, cache, copy the layers)
    ov = sorted(override) if isinstance(override, (list, tuple, set, frozenset)) else sorted((override or {}).items())
    mk = ("items", id(D), mode, repr(ov), tuple(box) if box else None, bool(split_buildings), scale_den)
    if mk in _BM_MEMO:
        return list(_BM_MEMO[mk])
    _BM_MEMO[mk] = _bm_items(D, mode, override, box, split_buildings, scale_den)
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


def _bm_items(D, mode, override, box, split_buildings, scale_den=None):
    """basemap_items without the memo"""
    lay = basemap_layers(mode, override)
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
    """cuts for basemap_cut_items from the level module (common/levels.py, its data included before it): the ends
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


# M4 key map: keymap_items and basemap_cut_items moved to keymap.py (round 4 S2: R01 red symbol, names, muted base)


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


def _sc_gh(S, C):
    """S ∩ C as rings, or None when a vertex lies on the other's edge (the caller perturbs and retries)"""
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


def ml_base(box, scale_den, D=None, contours=False, names=False, override=None, crop=True):
    """the muted base of a map (G-R4-4): basemap mode "muted" = the stream (M5 water), light streets with closed
    edges, light houses with ONE closed outline per block, every outline after every fill; contours=True adds the
    contours coloured to the relief (green ramp, lighter = lower, U48); names=True the place names (6 pt, pale).
    The study line is NOT in it (map_draw draws it in its own layer). box = (x0, y0, x1, y1) survey m; scale_den =
    the map's 1:scale_den. Returns basemap items (bottom first), [] without basemap data. Round 5 (G-R5-10):
    crop=True cuts every item to box, so nothing of the base runs past the drawing's window."""
    ov = dict(contours="height" if contours else False, names=bool(names))
    ov.update(override or {})
    its = basemap_items("muted", ov, box=box, D=D, scale_den=scale_den)
    its = [_bm_tag(("text", it[1], it[2], ML_NAME_MM, BM_MUTED["name"], False, it[6]), "base_names")
           if it[0] == "text" else it for it in its]
    if crop and box:
        its = ml_crop(its, [(box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])])
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
    lay = getattr(src, "layer", None)
    return _bm_tag(t, lay) if lay else t


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
# ---- Key maps, cut symbol, north arrow (round 4 S2, 1 Nov 2026; G-R4-9, R01, U02 U31 U50 U51 U55 U60; PLAN §4.5) -----
# ONE key-map module: every cut line drawn with the R01 symbol in red (an end bar with an open triangle standing on it
# pointing the way the section looks, a dash-dot line between), in front of a muted base, with ONLY the page's cuts,
# the main street and place names (so the reader knows where it is), never over its legend; ONE north arrow (the
# arrow and "N", no plate, U31 U51). Included by common/basemap.py (its last lines, after map_layers.py); do not
# include it again. The old basemap_cut_items / keymap_items are thin wrappers at the end of this file.
# ROUND 5 (S2, 1 Nov 2026; G-R5-3, D3, D6, A11, U33 U36 U45 U67-U69; PLAN §3 "Key map"): v2. Drawn like the p02 map
# (basemap mode "keymap": green ground, houses by urban fabric, the stream blue, bridges), never the grey blob; the
# frame cut to the map (fitted, fill logged, >= 0.85); turned so the corridor runs along the frame's long side, the
# north arrow showing true north in a free corner; names only through the names table (street_label, keymap_places);
# exported as items for the booklet (km_items: drawing + text labels with anchors + keymap item; G-R5-12, Aras's
# addendum 1 Nov 22:37 point 3). Every page's key map calls km_map (p04, p05, p09, p10 locator, p13-14, p15, p16,
# p18, p19-20, p24; their page sessions S6-S10 switch the callers to km_items); scale_den keeps the round 4 contract.
#   KM_CUT, KM_NAMES, KM_FRAME, KM_CUT_PLAN      the cut symbol, the names switches, the frame line, plan cuts (D6)
#   km_cut_items(cuts, scale_den, frame=None, style=None, text_mm=2.47)      R01 cut symbols as items (survey m)
#   km_map(ids, w_mm=None, h_mm=None, zooms=None, page=None, names=None, legend_box=None, log=None, looks=None,
#          box=None, scale_den=None, extra_names=None, D=None, margin=None, rotate=None, fit=None, pad_mm=None,
#          base_mode="keymap", north=True)                                  a whole key map (survey m + its T)
#   km_draw(km, X, fill_fn, line_fn, text_fn, water_opts=None, page=None, log=None, frame=True)   draws it
#   km_items(km, page=None, item_id=None, priority=5)                       round 5: the key map as booklet items
#   km_texts(km)                                 its texts in key-map mm, for the page's TextPage (.put)
#   north_items(x, y, ang_rad=0.0, size_mm=6.0, colour="2C2219")           the north arrow (page mm, y up)
# Items: the basemap format (common/basemap.py head). Key-map mm: origin at the key map's lower-left, y up.
import math as _km_m

# R01 in red (G-R4-9): line 0.5 mm dash-dot; end bar 2.4 mm along the line at each end, the open triangle standing on
# it (base = the bar, height tri_h, apex the way the section looks), the end name beyond the bar. Sizes: drawing rules
# of PLAN §4.5 (the triangle's base is the bar so it never overhangs it).
KM_CUT = dict(colour="C0392B", lw=0.5, dash=(3.0, 0.8, 0.6, 0.8), end_bar=2.4, bar_lw=0.6, tri_h=2.1, tri_lw=0.35,
              text_mm=2.47, gap_mm=0.8)
KM_NAMES = dict(streets=("main",), n_streets=4, places=True, n_places=6, size_mm=2.12, colour="6B645B", bold=False,
                pad_mm=0.6)
KM_ZOOM = dict(colour="C0392B", lw=0.35)       # zoom / window frames on a key map: the cut red, solid
KM_FRAME = dict(colour="4A3F35", lw=0.25)      # round 5 (S2, D3): the key map's frame line (site board INK), hairline
# round 5 (S2, D6 a, U30): cut lines ON PLANS (not key maps): thin and muted, 0.25 pt 8E8F8A dashed (PLAN §3); pass
# as km_cut_items(..., style=KM_CUT_PLAN); key maps keep the red R01 KM_CUT. Dash, bar and triangle sizes: design values
KM_CUT_PLAN = dict(colour="8E8F8A", lw=0.0882, dash=(1.6, 0.8), end_bar=1.6, bar_lw=0.0882, tri_h=1.2, tri_lw=0.0882,
                   text_mm=1.59, gap_mm=0.6)
KM_LOG = []


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
        look = c[3] if len(c) > 3 else 1
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
            if L <= 2.0 * pull + 2.0 * st["end_bar"] * m:
                continue
            a = (a[0] + ux * pull, a[1] + uy * pull)
            b = (b[0] - ux * pull, b[1] - uy * pull)
        fx, fy = -uy * look, ux * look                   # the way the section looks
        out.append(("line", [a, b], col, st["lw"], list(st["dash"]), 1.0))
        bar, th = st["end_bar"] * m, st["tri_h"] * m
        for p, nm, sgn in ((a, names[0], -1.0), (b, names[1], 1.0)):
            q = (p[0] - ux * sgn * bar, p[1] - uy * sgn * bar)          # the bar runs from the end inward
            out.append(("line", [p, q], col, st["bar_lw"], None, 1.0))
            mid = ((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0)
            tri = [p, q, (mid[0] + fx * th, mid[1] + fy * th), p]
            out.append(("line", tri, col, st["tri_lw"], None, 1.0))      # open triangle standing on the bar
            off = (st["gap_mm"] + tm * 0.3 * max(1, len(nm))) * m     # beyond the end, clear of the bar
            t = (p[0] + ux * sgn * off, p[1] + uy * sgn * off)
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


def _km_axis_deg(P):
    """round 5 (S2): the direction (degrees, counter-clockwise from east) of the long axis of points P (principal
    axis of their spread); 0.0 when P has fewer than 3 points"""
    if len(P) < 3:
        return 0.0
    mx, my = sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P)
    sxx = sum((p[0] - mx) ** 2 for p in P)
    syy = sum((p[1] - my) ** 2 for p in P)
    sxy = sum((p[0] - mx) * (p[1] - my) for p in P)
    return _km_m.degrees(0.5 * _km_m.atan2(2.0 * sxy, sxx - syy))


def km_map(ids, w_mm=None, h_mm=None, zooms=None, page=None, names=None, legend_box=None, log=None, looks=None,
           box=None, scale_den=None, extra_names=None, D=None, margin=None, rotate=None, fit=None, pad_mm=None,
           base_mode="keymap", north=True):
    """THE key map (round 5 S2 v2: G-R5-3, D3, D6, A11; round 4 G-R4-9). Key-map mm: origin at the frame's lower-left,
    y up. ids: this page's cut ids (cut registry, levels.py) and zoom / window ids (zooms {id: polygon survey m}, else
    level_window(id)); none + page = every cut the registry draws on that page.
    Size and frame (D3 "a frame sized to the map"): with scale_den None (the usual call) the map is FITTED: w_mm /
    h_mm are the most the page offers (either may be None; both None = 80 mm wide), the scale fills that space and the
    frame is cut to the map plus pad_mm (default 1.0) and a margin (default 2 % of the content), so the map fills its
    frame; fit=False keeps the caller's w x h (map centred, round 4). scale_den given: the round 4 contract (fixed
    scale, the caller's frame or box; no turn).
    Turn (U68): rotate=None turns a fitted map so the corridor (the study area's long axis) runs along the frame's
    long side (portrait space: upright), north never pointing down; a number = that turn in degrees
    (counter-clockwise); False = north up. The north arrow shows true north (north=True: arrow only, in the freest
    corner).
    Base (U69 "just draw it like page 2"): basemap mode base_mode ("keymap" = the p02 look: green ground, houses by
    urban fabric, the stream blue, bridges), cut to the frame. Content: the study line, ONLY these cuts (R01 red,
    look direction), zoom frames, names: main streets (OpenStreetMap names by the names table's spelling,
    street_label) and the names table's key-map places (keymap_places: "at" + "km"; never a raw survey name), then
    extra_names; each placed clear of the cuts, their labels, the north arrow, legend_box and each other, else left
    out and logged. Labels are hints: km_items exports them with their anchors for the booklet to place (G-R5-12).
    Logs `keymap <page> fill=<x> rotation=<deg> cuts=<ids>` (fill = the content's box / the frame; WARNING below
    0.85 on a fitted map). Returns dict(base, study, cuts, names, items (survey m, in order), box, scale_den, T, Tinv,
    drawn, missing, label_boxes, w_mm, h_mm, study_rings, rotation_deg, north_deg, fill, frame (survey ring),
    frame_items, north (key-map mm items), labels [dict(string, kind, anchor, box, size_mm, colour, bold)], fitted,
    looks, zoom_ids, page)."""
    D = D if D is not None else basemap_load()
    log = log if log is not None else KM_LOG
    nm_st = dict(KM_NAMES)
    nm_st.update(names or {})
    pg = u"%s" % (page or u"")
    if not ids and page is not None and callable(globals().get("level_registry_all")):
        ids = [e["id"] for e in level_registry_all(str(page))]
    cuts, wins, drawn, missing, seen = [], [], [], [], set()
    win_fn = globals().get("level_window")
    for cid in ids or ():
        if zooms and cid in zooms:
            wins.append((cid, [tuple(p) for p in zooms[cid]]))
            drawn.append(cid)
            continue
        try:
            c = basemap_cut_ids([cid], looks)[0]
            ek = (round(c[0][0], 1), round(c[0][1], 1), round(c[1][0], 1), round(c[1][1], 1))
            if ek not in seen:                           # the crossings of one cut share one line
                seen.add(ek)
                cuts.append((cid, c))
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
    study = basemap_study(D)
    auto = not scale_den
    fit = auto if fit is None else (bool(fit) and auto)
    if margin is None:
        margin = 0.02 if fit else 0.06
    pad = 1.0 if pad_mm is None else float(pad_mm)
    if box is None:
        cont = [p for R in study for p in R] + [p for _, c in cuts for p in c[:2]] + [p for _, w in wins for p in w]
        if not cont:
            cont = list(basemap_extent(D) or [])
        if not cont:
            raise ValueError(u"key map %s: nothing to frame (no basemap data, no cuts)" % pg)
    else:
        cont = [(box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])]
    # the turn: the corridor along the frame's long side (U68)
    if rotate is None:
        if auto:
            bx_ = _bm_bb(cont)
            ax_pts = [p for R in study for p in R if bx_[0] <= p[0] <= bx_[2] and bx_[1] <= p[1] <= bx_[3]]
            th = _km_axis_deg(ax_pts if len(ax_pts) >= 3 else cont)
            portrait = bool(w_mm and h_mm and h_mm > w_mm)
            phi = (90.0 - th) if portrait else -th
        else:
            phi = 0.0
    else:
        phi = float(rotate or 0.0)
    if _km_m.cos(_km_m.radians(phi)) < -1e-9:            # north never points down the page
        phi += 180.0
    phi = (phi + 180.0) % 360.0 - 180.0
    cph, sph = _km_m.cos(_km_m.radians(phi)), _km_m.sin(_km_m.radians(phi))
    bx0 = _bm_bb(cont)
    c0 = ((bx0[0] + bx0[2]) / 2.0, (bx0[1] + bx0[3]) / 2.0)

    def rot(p):
        dx, dy = p[0] - c0[0], p[1] - c0[1]
        return (dx * cph - dy * sph, dx * sph + dy * cph)

    def unrot(q):
        return (q[0] * cph + q[1] * sph + c0[0], -q[0] * sph + q[1] * cph + c0[1])
    rc = [rot(p) for p in cont]
    rx0, ry0, rx1, ry1 = _bm_bb(rc)
    cw, ch = max(rx1 - rx0, 1.0), max(ry1 - ry0, 1.0)  # the content, m
    d = margin * max(cw, ch)
    bw, bh = cw + 2.0 * d, ch + 2.0 * d
    if fit:
        if not w_mm and not h_mm:
            w_mm = 80.0
        dens = []
        if w_mm:
            dens.append(bw * 1000.0 / max(1.0, w_mm - 2.0 * pad))
        if h_mm:
            dens.append(bh * 1000.0 / max(1.0, h_mm - 2.0 * pad))
        den = max(dens)
        w_mm, h_mm = bw * 1000.0 / den + 2.0 * pad, bh * 1000.0 / den + 2.0 * pad
    elif scale_den and (w_mm is None or h_mm is None):   # a fixed scale: the key map is the box at that scale
        den = float(scale_den)
        w_mm, h_mm = bw * 1000.0 / den, bh * 1000.0 / den
    else:
        den = float(scale_den) if scale_den else max(bw * 1000.0 / w_mm, bh * 1000.0 / h_mm)
    s = 1000.0 / den
    rcx, rcy = (rx0 + rx1) / 2.0, (ry0 + ry1) / 2.0

    def T(p):
        r = rot(p)
        return ((r[0] - rcx) * s + w_mm / 2.0, (r[1] - rcy) * s + h_mm / 2.0)

    def Tinv(q):
        return unrot(((q[0] - w_mm / 2.0) / s + rcx, (q[1] - h_mm / 2.0) / s + rcy))
    frame = [Tinv((0.0, 0.0)), Tinv((w_mm, 0.0)), Tinv((w_mm, h_mm)), Tinv((0.0, h_mm))]
    vb = _bm_bb(frame)
    if base_mode == "muted":
        base = ml_base(vb, den, D=D, crop=False) if D else []
    else:
        base = basemap_items(base_mode, box=vb, D=D, scale_den=den) if D else []
    base = ml_crop(base, frame) if base else []
    if D and D.get("format") != BASEMAP_FORMAT:
        log.append(u"FLAG keymap %s: basemap format %s has no urban fabric per house: one house tone until the site "
                   u"board writes format %d" % (pg, D.get("format"), BASEMAP_FORMAT))
    st_items = ml_study_items(study)
    cut_items = []
    for cid, c in cuts:
        its = km_cut_items([c], den, frame=frame)
        nm_fn = globals().get("level_name")
        try:
            name = nm_fn(cid) if callable(nm_fn) else cid
        except Exception:
            name = cid
        name = u"%s" % name
        name = name.split("-")[0]                        # a crossing row (S5-2) is labelled by its cut (S5)
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
    # the north arrow: arrow only (G-R4-9), in the first free corner (top right, top left, bottom right, bottom left)
    north_its, nsz = [], 5.0
    if north:
        best = None
        for fx, fy in ((1, 1), (0, 1), (1, 0), (0, 0)):
            cxn = (w_mm - pad - 0.9 * nsz) if fx else (pad + 0.9 * nsz)
            cyn = (h_mm - pad - 0.9 * nsz) if fy else (pad + 0.9 * nsz)
            nb = (cxn - 0.9 * nsz, cyn - 0.9 * nsz, cxn + 0.9 * nsz, cyn + 0.9 * nsz)
            if not _km_seg_hit(nb, segs, 0.3) and not _km_box_hit(nb, boxes, 0.3):
                best = (cxn, cyn, nb)
                break
        if best is None:
            cxn, cyn = w_mm - pad - 0.9 * nsz, h_mm - pad - 0.9 * nsz
            best = (cxn, cyn, (cxn - 0.9 * nsz, cyn - 0.9 * nsz, cxn + 0.9 * nsz, cyn + 0.9 * nsz))
            log.append(u"WARNING %s keymap north arrow: no free corner, set top right over the map" % pg)
        cxn, cyn, nb = best
        a = _km_m.radians(phi)
        foot = (cxn + _km_m.sin(a) * 0.5 * nsz, cyn - _km_m.cos(a) * 0.5 * nsz)    # the arrow centred on (cxn, cyn)
        north_its = north_items(foot[0], foot[1], ang_rad=a, size_mm=nsz * 0.75)
        boxes.append(nb)
    if legend_box:
        boxes.append(tuple(legend_box))
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
        raise RuntimeError(u"km_map needs common/font_metrics.py (round 4 S1: fm_width) included before it is "
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
        w = fmw(n, pt_of(sz), bold=nm_st["bold"])
        ok = None
        for dx, dy in ((0.0, 0.0), (0.0, sz * 1.1), (0.0, -sz * 1.1), (w / 2.0 + 1.0, 0.0), (-w / 2.0 - 1.0, 0.0),
                       (0.0, sz * 2.2), (0.0, -sz * 2.2)):
            b = (x + dx - w / 2.0, y + dy - sz / 2.0, x + dx + w / 2.0, y + dy + sz / 2.0)
            if b[0] < pad_n or b[1] < pad_n or b[2] > w_mm - pad_n or b[3] > h_mm - pad_n:
                continue
            if _km_box_hit(b, boxes, pad_n) or _km_seg_hit(b, segs, pad_n):
                continue
            ok = b
            break
        if ok is None:
            log.append(u"keymap %s: name '%s' left out (no free place)" % (pg, n))
            continue
        seen_n.add(n)
        boxes.append(ok)
        label_boxes.append((n, ok))
        placed[kind] += 1
        name_items.append(("text", n, Tinv(((ok[0] + ok[2]) / 2.0, (ok[1] + ok[3]) / 2.0)), sz, nm_st["colour"],
                           nm_st["bold"], "MC"))
        labels.append(dict(string=n, kind=kind, anchor=(x, y), box=ok, size_mm=sz, colour=nm_st["colour"],
                           bold=nm_st["bold"]))
    fill = (cw * s) * (ch * s) / max(1e-9, w_mm * h_mm)
    fill = min(1.0, fill)
    rot_out = round(phi, 1)
    log.append(u"keymap %s fill=%.2f rotation=%.1f cuts=%s" % (pg, fill, rot_out,
                                                               u",".join(cid for cid, _ in cuts) or u"-"))
    if fit and fill < 0.85:
        log.append(u"WARNING %s keymap fill %.2f below 0.85 (frame %.0f x %.0f mm)" % (pg, fill, w_mm, h_mm))
    if log is not KM_LOG:
        KM_LOG.append(log[-1])
    frame_mm = [(0.0, 0.0), (w_mm, 0.0), (w_mm, h_mm), (0.0, h_mm)]
    frame_items = [("fill", [frame_mm], bm_key_col("paper"), 1.0, True),
                   ("line", frame_mm + [frame_mm[0]], KM_FRAME["colour"], KM_FRAME["lw"], None, 1.0)]
    return dict(base=base, study=st_items, cuts=cut_items, names=name_items,
                items=list(base) + st_items + cut_items + name_items, box=(vb[0], vb[1], vb[2], vb[3]), scale_den=den,
                T=T, Tinv=Tinv, drawn=drawn, missing=missing, label_boxes=label_boxes, w_mm=w_mm, h_mm=h_mm,
                study_rings=study, rotation_deg=rot_out, north_deg=rot_out, fill=fill, frame=frame,
                frame_items=frame_items, north=north_its, labels=labels, fitted=fit, looks=dict(looks or {}),
                zoom_ids=[cid for cid, _ in wins], cut_ids=[cid for cid, _ in cuts], page=page)


def km_draw(km, X, fill_fn, line_fn, text_fn, water_opts=None, page=None, log=None, frame=True):
    """draws a km_map (PLAN §3 order: paper, base, WATER, structures, the study line, the red cuts, names, then the
    frame line and the north arrow): X(q) key-map mm -> page point (e.g. lambda q: (x0 + q[0], y0 + q[1]), or a
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
        basemap_draw(km["frame_items"][1:] + km["north"], X, fill_fn, line_fn, text_fn)
    return r


def km_items(km, page=None, item_id=None, priority=5):
    """round 5 (S2, G-R5-12; PLAN §4 item schema v1, Aras's addendum 1 Nov 22:37 point 3): the key map as items for
    the booklet: one "drawing" (layers of shapes in key-map mm, y up, origin lower-left; texts left out), one "text"
    item per label (names and cut labels, role "label", with its anchor in the drawing and the module's placement as
    hint_box), one "keymap" item (cut ids, looks, zooms, names, fill, rotation). Shapes: {"type": "poly", "rings",
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
                                         nonzero=bool(nonzero)))

    def line_fn(pts, col, w_mm, dash_mm, alpha):
        if cur["name"] is None:
            layer("base")
        layers[-1]["shapes"].append(dict(type="line", pts=[[round(p[0], 3), round(p[1], 3)] for p in pts],
                                         stroke=col, width_pt=round(w_mm / 0.352778, 3),
                                         dash_pt=[round(d_ / 0.352778, 3) for d_ in dash_mm] if dash_mm else None,
                                         opacity=alpha))
    T = km["T"]
    layer("paper")
    basemap_draw(km["frame_items"][:1], lambda q: q, fill_fn, line_fn, None)
    map_draw(u"%s key map" % (pg or u""), T, fill_fn, line_fn, None, km["base"],
             {"proj_marks": [it for it in km["cuts"] if it[0] != "text"]}, study=km.get("study_rings"),
             clip=False, order_fn=layer)
    layer("frame")
    basemap_draw(km["frame_items"][1:] + [it for it in km["north"] if it[0] != "text"], lambda q: q, fill_fn,
                 line_fn, None)
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
    texts = [dict(string=t[1], kind="north", anchor=t[2], box=None, size_mm=t[3], colour=t[4], bold=t[5])
             for t in km["north"] if t[0] == "text"]
    for i, lb in enumerate(km["labels"] + texts):
        out.append(dict(id=u"%s.t%d" % (did, i), page=pg, kind="text", role="label", priority=priority, group=did,
                        string=lb["string"], label_kind=lb["kind"],
                        anchor=dict(drawing=did, point=[round(lb["anchor"][0], 2), round(lb["anchor"][1], 2)]),
                        hint_box=[round(v, 2) for v in lb["box"]] if lb["box"] else None,
                        size_pt=round(lb["size_mm"] / 0.352778, 2), min_pt=4.0, bold=bool(lb["bold"]),
                        colour=lb["colour"], short_forms=[], side_list_ok=False, justify=False))
    out.append(dict(id=u"%s.km" % did, page=pg, kind="keymap", role="keymap", priority=priority, group=did,
                    drawing=did, cuts=[dict(id=c, look=km["looks"].get(c, 1)) for c in km["cut_ids"]],
                    zooms=list(km["zoom_ids"]), names=[lb["string"] for lb in km["labels"] if lb["kind"] != "cut"],
                    fill=round(km["fill"], 3), rotation_deg=km["rotation_deg"], missing=list(km["missing"])))
    return out


def km_texts(km):
    """the key map's texts in key-map mm for the page's TextPage: [(text, (x, y) centre, size_mm, bold, box)]"""
    out = []
    for it in km["cuts"] + km["names"]:
        if it[0] == "text":
            x, y = km["T"](it[2])
            box = next((b for t, b in km["label_boxes"] if t == it[1]), None)
            out.append((it[1], (x, y), it[3], it[5], box))
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


# ---- old names (round 3 callers; page sessions move to km_map / km_cut_items) -------------------------------------
def basemap_cut_items(cuts, scale_den, frame=None, inset_mm=3.0, tri_mm=2.6, text_mm=2.4, col=None, D=None):
    """round 3 name, now the R01 red symbol (G-R4-9): km_cut_items(cuts, scale_den, frame or the analysis frame).
    inset_mm, tri_mm and col are ignored (one symbol, one colour everywhere)."""
    return km_cut_items(cuts, scale_den, frame=frame or basemap_frame(D), text_mm=max(text_mm, 2.12))


def keymap_items(ids=(), scale_den=10000.0, box=None, zooms=None, mode="key", override=None, looks=None, D=None,
                 margin=0.06, text_mm=2.4, col=None, log=None, page=None):
    """round 3 name, now km_map at the caller's scale and box (mode, override, text_mm and col are ignored: the base is
    the muted one, the cuts R01 red): dict(items (survey m, in order), box, drawn, missing) as before"""
    km = km_map(ids, None, None, zooms=zooms, page=page, log=log, looks=looks, box=box, scale_den=scale_den, D=D,
                margin=margin, names=dict(streets=(), places=False))     # round 3 key maps had no names
    return dict(items=km["items"], box=km["box"], drawn=km["drawn"], missing=km["missing"])
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
#   ix.layer(D, name, shapes, z=None, k=1.0, origin=(0, 0))
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

    def layer(self, D, name, shapes, z=None, k=1.0, origin=(0.0, 0.0)):
        out, texts, hatch = [], 0, 0
        for s in shapes or ():
            if not s:
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

def fmt(v): return "{:,.0f}".format(v)

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
    nb, _st = cl_map(pg, "p10", T, sbox, den, proj, base_extra=covered, clip=True,   # v9: cut to the window on export
                     legend_cols=[ML_TINT, C["green_mid"], C["ink"]], water_ok=[C["ink"]])   # stones: in the bed

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
                script="bergama_city_link_v9.py", version=VERSION, run_time=time.strftime("%Y-%m-%d %H:%M:%S"),
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
