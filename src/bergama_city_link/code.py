# bergama_city_link_v5.py (v5, 30 Oct: revision T5, p8 framework map + who calendar, p9 spine) · Thread 4 of the 22 Oct batch: connection to the city (the streamside spine and what it adds)
# Runs as delivered in: Grasshopper Python 3 component (press a Button wired to any input), Rhino 8 ScriptEditor
# (Python 3), or plain Python 3. Makes the folder Downloads/Bergama/output/Bergama_city_link_analysis by itself and saves
# ONE all-vector A3 PDF there (two pages) plus city_link_results.json:
#   1 THE STREAM JOINS THE TOWN WHERE THE SHOPS ALREADY ARE (booklet p.08, v4) the framework diagram of the
#                                                         movement pages on the shared simple basemap, who the project
#                                                         brings (G7), seven reasons
#   2 THE STREAMSIDE SPINE, HUB BY HUB                    (booklet p.09, v4) the spine on a map along the stream, the
#                                                         five bridge places as cards (bus stops, dry hub + sub-hub,
#                                                         stops), the flood rule, which bank, the producers' market
# city_link_results.json = the spine, the function sites and (v1.11) the hubs in survey coordinates. The site board (selinus_board v34,
# plan 07) reads it for the movement potential with the spine, and the masterplan (Thread 5) draws it.
# Read live on every run: the water balance results (farm areas for the producers' market) and the site board's
# movement result (walking potential on the spine), each with a flagged fallback.
# Notes for Aras: batch_2026-10-22/thread4_city_link/NOTES.md (every figure with its source).
import os, time, json, zlib, math, base64

VERSION = "v5"
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

# ------------------------------------------------------------------ the spine and the function sites (survey m)
# Anchors are surveyed points (h01 §0 and §5, source s62): K4 Ulucami Önü (29846,32278), K3 Tabak Köprüsü (30037,32122),
# P04 Red Hall south rotunda "Müze" (30238.7,31931.2), K5 Üç Kemer (30294,31792). side_ref = a surveyed point on the bank
# the piece runs on (P05 Ulu Cami; P02 Red Hall); offset_m = distance from the stream centreline (schematic, for the
# movement network only; Thread 5 draws the real edge). Piece B runs over the covered reach (offset 0), where the main
# spine (Kınık Caddesi) crosses the stream.
SPINE = [
    dict(id="A", name="Ulu Cami to K3 bank walk", frm=[29846.0, 32278.0], to=[30037.0, 32122.0], side_ref=[29844.2, 32313.3], offset_m=15.0, side="auto", catch_m=250.0),
    dict(id="B", name="Junction over the covered reach", frm=[30037.0, 32122.0], to=[30238.7, 31931.2], side_ref=None, offset_m=0.0),
    dict(id="C", name="Red Hall to Üç Kemer bank walk", frm=[30238.7, 31931.2], to=[30294.0, 31792.0], side_ref=[30245.0, 31962.0], offset_m=15.0, side="auto", catch_m=250.0),
]
# the main spine (Bankalar Caddesi + Kınık Caddesi, OSM "secondary" ways of the same extract, converted with the h01 §0
# formula, +-10-30 m), from Bankalar's south end east past the junction; the masterplan (v11) draws it (Thread 5)
MAIN_SPINE = [[29756.1, 31655.4], [29777.7, 31668.2], [29793.7, 31679.4], [29806.4, 31691.6], [29813.1, 31702.3], [29819.3, 31712.8], [29828.2, 31728.8], [29852.9, 31760.3], [29869.5, 31780.3], [29880.9, 31808.0], [29885.0, 31824.8], [29896.2, 31862.5], [29901.7, 31880.7], [29908.9, 31905.2], [29916.1, 31928.8], [29919.2, 31939.1], [29929.8, 31960.8], [29944.8, 31984.6], [29951.9, 31990.3], [29956.3, 31993.2], [29992.8, 32017.4], [29995.4, 32019.8], [29998.6, 32022.6], [30005.0, 32029.4], [30032.5, 32038.3], [30084.6, 32056.0], [30089.7, 32057.7], [30092.6, 32056.5], [30096.2, 32055.0], [30138.7, 32039.0], [30153.1, 32036.3], [30235.7, 32021.9], [30245.0, 32020.1], [30269.2, 32015.6], [30274.2, 32014.5], [30278.7, 32012.8], [30281.9, 32010.3], [30285.0, 32007.1], [30308.8, 31981.0], [30310.4, 31979.3], [30317.5, 31972.1], [30331.6, 31957.6], [30373.7, 31924.2], [30399.9, 31903.0], [30432.4, 31879.5], [30499.5, 31831.0], [30545.8, 31800.5], [30562.8, 31796.3], [30574.8, 31795.5], [30598.1, 31797.7], [30626.3, 31799.4], [30663.0, 31801.6], [30682.2, 31803.0], [30709.6, 31804.9], [30718.5, 31805.5], [30741.5, 31803.1], [30767.5, 31791.6], [30786.2, 31779.9], [30813.0, 31760.8], [30824.8, 31752.4], [30889.1, 31700.8], [30978.8, 31622.0], [30993.4, 31611.0], [31007.0, 31604.5], [31023.2, 31601.7]]
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

# chainage along the stream from the frame's north-west end: bridges from h02 card (s62): K4 467, K3 709, K5 1,126,
# K6 1,767 m; other places projected onto the K4-K3-K5-K6 chord here (calculated, about ±30 m)
CH = dict(K4=467, K3=709, K5=1126, K6=1767, cross=781, cov0=709, cov1=949)
# v1.6: source texts printed once in each page's numbered key (cite() gives their [n])
SRC_WET = "Days wet: research/rain_river_levels/README.md §3 (mean of water years 2016-2021)"
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
SRC_TABAK = ("h02 calls Tabaklar Hamamı 'opposite Ulu Cami on the right bank' (s32), but both survey points lie on the "
             "north-east bank [U]")
# v1.9: the page 1 main spine plan
SRC_MAIN = "OpenStreetMap contributors, extract of 28 Jul 2026: streets, the Selinos stream (covered pieces), bus stops"
SRC_STREAM = SRC_MAIN                    # v4 (D13): one public source line for the OSM layers
# who: L locals, T tourists, S students; grows: W water, E stream edge, A agriculture, H heritage
FUNCS = [
    dict(n=1, name="Bank bazaar", where="Tabaklar Hamamı", ch=522, bank="NE", xy=[29890.4, 32243.6], who="LT", grows="HE",
         icon="stall", kw=("Ottoman bazaar on this bank: Pabuççular Arastası", "stalls bring it back"), src="h02 s32"),
    dict(n=2, name="Parchment and leather workshops", where="Tannery quarter at K3", ch=737, bank="both", xy=[30062.0, 32106.0], who="TSL", grows="H",
         icon="hide", kw=("tanning named the stream · last master died 2026", "teach and sell the craft"), src="h02 s44 s45"),
    dict(n=3, name="Junction square", where="Kınık Caddesi over the covered stream", ch=781, bank="over", xy=[30058.0, 32047.0], who="LTS", grows="WEH",
         icon="slot", kw=("the one place the main road meets the stream", "a slot: view down to the water strip"), src=None),
    dict(n=4, name="Red Hall water terrace", where="Red Hall, Roman tunnels' outlet", ch=962, bank="NE", xy=[30238.7, 31931.2], who="TL", grows="HW",
         icon="arch", kw=("Red Hall reopens: target 2026", "its visitors step out onto the stream"), src="h02 s41"),
    dict(n=5, name="Producers' market", where="Üç Kemer bridge, Wednesdays", ch=1126, bank="spine", xy=[30294.0, 31792.0], who="LT", grows="A",
         icon="olive", kw=("food from fields on our stored water · olive oil", "Wednesdays · town producers' market: Saturdays"), src="h02 s25"),
    dict(n=6, name="Study terraces", where="Spine bank between K4 and K3", ch=620, bank="spine", xy=[29941.0, 32200.0], who="SL", grows="EW",
         icon="bench", kw=("shaded seats by the water strip", "for students · out of the street noise"), src=None),
    dict(n=7, name="Clean-water classroom", where="Reed basins, upstream entry", ch=200, bank="bed", xy=None, stage="entry", who="SL", grows="W",
         icon="reed", kw=("the cleaning basins as a lesson", "how the stream works"), src=None),
]
EVENTS = dict(n=8, name="Summer bed events", where="Dry bed beside the 4 m water strip", who="LT", grows="WE",
              icon="calendar", kw=("open-air events · Jul-Sep", "bed 3 cm or less · cleared by October"), src=SRC_WET)
# v1.6: kw = 2 keyword lines (were one "why" sentence); src = the source number in the page key; icon = the stop's pictogram
HERITAGE = [  # (chainage, bank, label, source) from h01 §5 (survey coordinates projected, calculated)
    (380, "NE", "Roman complex", "P12"), (444, "NE", "Ulu Cami 1398", "P05"), (522, "NE", "Tabaklar Hamamı", "P07"),
    (737, "NE", "Tannery quarter", "E07"), (752, "SW", "İstiklal Meydanı", "P16"), (887, "SW", "Yabets synagogue", "P14"),
    (962, "NE", "Red Hall (Kızıl Avlu)", "P02"), (1376, "NE", "Harap Camii", "P18")]

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
    ("road", "MAIN ROAD MEETS THE STREAM", "1 crossing", ("Bankalar - Kınık Caddesi", "only where the stream runs covered"), "OSM, calculated"),
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
                                             u"K4 before the DSİ walls (survey)"), SRC_FLOOD),
    ("sewage", "SEPTIC SEWAGE IN THE STREAM", "until 2024", ("odour", "flies"), "İZSU sewer, s59; E13"),
    ("arch", "RED HALL BUILT OVER THE STREAM", "AD 117-138", ("Ottoman bazaar still met it", "at Tabaklar Hamamı"), "h02 s13 s28; s32"),
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
                  u"K4 before the DSİ walls (survey)"),
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
#@include ../common/label_place.py
#@include ../common/basemap.py
#@include ../common/grid.py
#@include ../common/buildings.py
#@include ../common/icons.py
#@include ../common/data/FACTS.py
#@include ../common/facts.py

# ------------------------------------------------------------------ minimal vector PDF (mm units, Helvetica, whole strings)
_HW = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278] + [556] * 10 + \
      [278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
       667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556, 333, 556, 556, 500, 556, 556,
       278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334,
       260, 334, 584]

_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}   # Turkish letters in unused WinAnsi slots
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"

#@include ../common/text_w.py


#@include ../common/pdf_fonts.py

def tbox(s, x, y, size, bold=False, align="L"):
    """v1.11: the box (x0, y0, x1, y1) mm a line of text covers (baseline y; descender to cap height)"""
    w = text_w(s, size, bold)
    if align == "C":
        x -= w / 2
    elif align == "R":
        x -= w
    h = size * 0.3528
    return (x, y - 0.21 * h, x + w, y + 0.74 * h)


class Page:
    def __init__(self, w, h):
        self.w, self.h, self.ops = w, h, []
        self.boxes, self.clash = [], []           # v1.11: every text box; texts that overlap one set before (logged)
    def hit(self, b, pad=0.0):
        return any(b[0] < q[2] + pad and q[0] < b[2] + pad and b[1] < q[3] + pad and q[1] < b[3] + pad for q in self.boxes)
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
    def text(self, s, x, y, size, col="4A3F35", bold=False, align="L"):
        if not s:
            return
        b_ = tbox(s, x, y, size, bold, align)
        if self.hit(b_, -0.05):
            self.clash.append(s)
        self.boxes.append(b_)
        if align == "C": x -= text_w(s, size, bold) / 2
        elif align == "R": x -= text_w(s, size, bold)
        k = 72 / 25.4
        self.ops.append("BT /%s %.2f Tf %s %.2f %.2f Td (%s) Tj ET" % ("F2" if bold else "F1", size, self._c(col), x * k, y * k, self._enc(s)))
    def _enc(self, s):
        b = b"".join(bytes([_ENC_EXTRA[ch]]) if ch in _ENC_EXTRA else ch.encode("cp1252", "replace") for ch in s)   # 25 Oct: ı İ ğ Ğ ş Ş spelt right
        return b.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)").decode("latin-1")
    def text_rot(self, s, x, y, size, col="4A3F35", bold=False, ang=0.0):
        """v3 (MIRAQUA 28 Oct, P08.1): a line of text along a street, baseline from (x, y) at angle ang (radians);
        its boxes (one per short piece, so a slanted name blocks only its own strip) are recorded like text()'s"""
        bs = rot_boxes(s, x, y, size, bold, ang)
        if any(self.hit(b_, -0.05) for b_ in bs):
            self.clash.append(s)
        self.boxes += bs
        k, ca, sa = 72 / 25.4, math.cos(ang), math.sin(ang)
        self.ops.append("BT /%s %.2f Tf %s %.4f %.4f %.4f %.4f %.2f %.2f Tm (%s) Tj ET" % (
            "F2" if bold else "F1", size, self._c(col), ca, sa, -sa, ca, x * k, y * k, self._enc(s)))


def rot_boxes(s, x, y, size, bold, ang):
    """v3 (MIRAQUA 28 Oct, P08.1): the boxes a slanted line of text covers, one per piece about a letter height long"""
    w, h = text_w(s, size, bold), size * 0.3528
    ca, sa = math.cos(ang), math.sin(ang)
    n = max(1, int(w / max(h, 0.5)) + 1)
    out = []
    for i in range(n):
        P = [(x + ca * t - sa * v, y + sa * t + ca * v) for t in (w * i / n, w * (i + 1) / n) for v in (-0.21 * h, 0.74 * h)]
        out.append((min(p[0] for p in P), min(p[1] for p in P), max(p[0] for p in P), max(p[1] for p in P)))
    return out



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
    votes = dict((k, dict(v)) for k, v in BANK_VOTE.items())
    vote_src = "survey floor labels (built in, 24 Oct)"
    for v in (mv or {}).get("bank_votes") or []:
        if v.get("id") in votes:
            votes[v["id"]] = dict(NE=v["NE"], SW=v["SW"])
            vote_src = "site board buildings (" + mv_src + ")"
    sides = dict((pc["id"], bank_of(votes[pc["id"]])[0] if pc.get("side") == "auto" else "over") for pc in SPINE)
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
    # v2: page 1's plan context and page 2's walking radius from the site board (v46+), each with a flagged fallback
    ctx, t4 = _load(CTX_FILES)
    ctx_src = ("Context: site board city_context.json of %s (survey buildings, typed as the sections' building types; "
               "OSM streets by highway class; survey water; bridges K1-K6, s62; OSM shop points, same tags as the "
               "shop counts)" % t4) if ctx else ""
    fw, t5 = _load(FW_FILES)                   # v4: the site board's half of the framework (busiest streets, spines)
    mpmv = (mp or {}).get("movement") if isinstance((mp or {}).get("movement"), dict) else None
    return dict(lands=lands, wb_src=wb_src, mv=mv, mv_src=mv_src, votes=votes, vote_src=vote_src, sides=sides,
                spine_m=spine_m, mp_src=mp_src, walks=walks,
                river_month=(d or {}).get("river_month_m3"),     # v5 (p.08 calendar): the stream's mean monthly flow
                ctx=ctx, ctx_src=ctx_src, fw=fw, mpmv=mpmv,
                fw_note=("framework: site board of %s" % t5) if fw else
                "FLAG: no movement_framework.json (run the site board v51+): the framework has no busiest streets",
                mp_note=("" if mpmv else "FLAG: no masterplan movement (masterplan_results.json): the framework has no "
                         "road changes, crossings or bus line"),
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
    for i, part in enumerate(s.split("**")):
        if part:
            b_ = i % 2 == 1
            pg.text(part, x, y, size, (bold_col or C["ink"]) if b_ else col, b_)
            x += text_w(part, size, b_)
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


def step(pg, n, x, y):
    """v1.11: the reading-order number in front of a panel title (top left to bottom right); returns the title's x"""
    disc(pg, x + 2.6, y + 1.1, 2.6, C["accent"])
    pg.text(str(n), x + 2.6, y + 0.1, 8, C["white"], True, "C")
    return x + 6.8


DROPPED = []                         # v1.11: labels that found no free place (written to the log, never overlapped)


def along_label(pg, s, Q, size, col, frame, pts, avoid=(), lw=1.4, bold=True):
    """v3 (MIRAQUA 28 Oct, P08.1): the name s set along its own line Q (page mm, points inside the plan): on a run of
    Q at least as long as the name and straight to 0.6 mm, just beside the line (lw = the line's width), reading left
    to right, inside frame and clear of every word on the page; of those places the one over the fewest symbols (pts)
    and other lines (avoid: [(p, q)] segments), then the one nearest the middle of Q. False when no run fits (or every
    fit sits on more than three symbols): the caller then sets the name beside the line on a leader."""
    wt, h = text_w(s, size, bold), size * 0.3528
    L_ = [0.0]
    for a, b in zip(Q, Q[1:]):
        L_.append(L_[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    if L_[-1] < wt + 1.0:
        return False

    def at(t):
        for i in range(1, len(Q)):
            if L_[i] >= t:
                u = (t - L_[i - 1]) / max(L_[i] - L_[i - 1], 1e-9)
                return (Q[i - 1][0] + (Q[i][0] - Q[i - 1][0]) * u, Q[i - 1][1] + (Q[i][1] - Q[i - 1][1]) * u)
        return Q[-1]
    best, half, t = None, wt / 2.0 + 0.5, wt / 2.0 + 0.5
    while t <= L_[-1] - half:
        a, b = at(t - half), at(t + half)
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy)
        if ln >= wt + 0.5:
            ux, uy = dx / ln, dy / ln
            run = [a] + [q for q, lq in zip(Q, L_) if t - half < lq < t + half] + [b]
            if max(abs((q[0] - a[0]) * uy - (q[1] - a[1]) * ux) for q in run) <= 0.6:
                if ux < 0:                                     # read left to right
                    ux, uy = -ux, -uy
                ang, (nx, ny), m = math.atan2(uy, ux), (-uy, ux), at(t)
                for off in (lw / 2.0 + 0.5 + 0.21 * h, -(lw / 2.0 + 0.5 + 0.74 * h)):   # above the line, then below
                    x0_, y0_ = m[0] - ux * wt / 2.0 + nx * off, m[1] - uy * wt / 2.0 + ny * off
                    bs = rot_boxes(s, x0_, y0_, size, bold, ang)
                    if any(b_[0] < frame[0] or b_[1] < frame[1] or b_[2] > frame[2] or b_[3] > frame[3] for b_ in bs):
                        continue
                    if any(pg.hit(b_, 0.4) for b_ in bs):
                        continue
                    n = sum(1 for p in pts if any(b_[0] <= p[0] <= b_[2] and b_[1] <= p[1] <= b_[3] for b_ in bs))
                    n += 5 * sum(1 for p, q in avoid if any(_lp_seg_box(p, q, b_) for b_ in bs))
                    key = (n, abs(t - L_[-1] / 2.0))
                    if best is None or key < best[0]:
                        best = (key, x0_, y0_, ang)
        t += 1.0
    if best is None or best[0][0] > 3:
        return False
    pg.text_rot(s, best[1], best[2], size, col, bold, best[3])
    return True


def mark_wh(it):
    """v5 (revision 30 Oct 2026, M2): the box (w, h) mm of a map mark at size 1: a name ("text"), a callout of
    several lines, a hub badge or a numbered place ("roundel")"""
    k_ = it.get("kind", "text")
    if k_ == "text":
        return text_w(it["s"], it["size"], it.get("bold", True)), 0.95 * it["size"] * 0.3528
    if k_ == "callout":
        return (max(text_w(s, z, b) for s, z, c, b in it["lines"]),
                sum(1.2 * z * 0.3528 for s, z, c, b in it["lines"]))
    if k_ == "badge":
        return text_w(it["s"], BADGE_PT, True) + 2.4, 3.8
    return 3.8, 3.8


def draw_mark(pg, it, b, f):
    """v5: a mark of mark_wh() drawn in its placed box b at size factor f"""
    k_ = it.get("kind", "text")
    if k_ == "text":
        z = it["size"] * f
        pg.text(it["s"], b[0], b[1] + 0.21 * z * 0.3528, z, it.get("col", C["ink"]), it.get("bold", True))
    elif k_ == "callout":
        y_ = b[3]
        for s, z, c, bd in it["lines"]:
            z *= f
            pg.text(s, b[0], y_ - 0.85 * z * 0.3528, z, c, bd)
            y_ -= 1.2 * z * 0.3528
    elif k_ == "badge":
        hub_badge(pg, it["s"], b[0], b[1], it["fill"], b[3] - b[1])
    else:
        r_ = (b[2] - b[0]) / 2.0
        disc(pg, b[0] + r_, b[1] + r_, r_, C["ink"])
        z = max(6.0, 7.0 * f)
        pg.text(str(it["s"]), b[0] + r_, b[1] + r_ - 0.265 * z * 0.3528, z, C["white"], True, "C")


def place_marks(pg, items, frame, obstacles=(), lines=(), max_leader=10.0):
    """v5 (revision 30 Oct 2026, M2 lp_place, G3): the marks of a map (dicts: kind, s, at = target point, r = its
    radius mm, rank 0 must show / 1 may drop, lead = leader colour, + the kind's own fields) placed clear of every
    word already on the page, of the symbols (obstacles, boxes) and of the linework (lines, page polylines), inside
    frame; one short leader, never crossing another, where a mark sits off its target. A mark left off goes to
    DROPPED (the log). Returns the placed boxes (None where dropped)."""
    labs = []
    for it in items:
        w_, h_ = mark_wh(it)
        labs.append(dict(x=it["at"][0], y=it["at"][1], w=w_, h=h_, rank=it.get("rank", 0), r=it.get("r", 0.0)))
    got = lp_place(labs, list(pg.boxes) + list(obstacles), lines, frame, max_leader=max_leader)
    out = []
    for it, g in zip(items, got):
        if g is None:
            DROPPED.append(str(it.get("s") or it.get("lines", [("callout",)])[0][0]))
            out.append(None)
            continue
        if g["leader"]:
            pg.line([g["leader"][0], g["leader"][1]], it.get("lead", C["ink2"]), 0.2)
        draw_mark(pg, it, g["box"], g["size"])
        out.append(g["box"])
    return out


def sw_fill(col, edge=None):
    """v5: a legend sample (M2 Legend kind "draw"): a filled patch"""
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


def lg_draw(pg, lg, size_pt=None, max_h=None):
    """v5 (M2 Legend, G1): lays out a Legend of common/label_place.py beside its drawing and draws it: each row's
    sample by its draw function (kind "draw", draw=fn(pg, swatch box)), then its words. Returns the layout (its
    "box" is where the legend sits)."""
    lay = lg.layout(lambda s, pt, b: text_w(s, pt, b), size_pt, max_h)
    if lay.get("title"):
        s, x, y = lay["title"]
        pg.text(s, x, y, lay["size_pt"], C["ink"], True)
    for r in lay["rows"]:
        if r.get("draw"):
            r["draw"](pg, r["swatch"])
        pg.text(r["label"], r["text"][0], r["text"][1], r["size_pt"], C["ink"])
    return lay


def scale_bar(pg, x, y, den):
    """v5 (G1): the scale bar of a plan at 1:den (a standard scale, r28_scale): four segments from (x, y), 0 / middle
    / end in m under it, the scale after it; returns the x where it ends"""
    k = 1000.0 / den
    seg_m = 50.0 if den <= 5000 else (100.0 if den <= 10000 else 200.0)
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

def roundel(pg, x, y, n, r=3.2, col=None):
    ring = [(x + r * math.cos(a * math.pi / 12), y + r * math.sin(a * math.pi / 12)) for a in range(24)]
    pg.poly(ring, fill=col or C["ink"], closed=True)
    pg.text(str(n), x, y - 1.25, 9, C["white"], True, "C")

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
P2_MAP = (14.0, 256.0)                   # page 2 map: x, top y (its height follows the study area, at most P2_MAP_HMAX)
P2_MAP_W = grid_w(9)                     # mm the map may take (M1: nine columns; its legend from column 10)
P2_MAP_HMAX = 64.0
P2_CARD = (14.0, 392.0, 82.0, 2.4)       # page 2 hub cards: x, total w, h, gap (their top 12 mm under the map)
P2_LOW = 84.0                            # page 2: the title line of the three bottom panels
P2_FLOOD = (14.0, 72.0, 19.0)            # page 2 flood rule: x, first (highest) level's y, row step
P2_BANK = (216.0, 73.0, 12.0)            # page 2 which bank: x, first row y, row step
P2_MARKET = grid_x(11)                   # page 2 producers' market: x (M1 column 11)
# v3 (MIRAQUA 28 Oct, G8): the study area on page 1's plan: calisma_alan of Bergama_Altlik.3dm (25 Oct 08:25, survey
# m), two parts worked as one, the recorded copy the site board (R28_STUDY_COPY) and masterplan (CALISMA_COPY) keep
CL_STUDY = [
    [(29696.903, 32800.562), (29872.423, 32572.84), (29880.693, 32496.334), (29818.865, 32475.301), (29825.821, 32398.074), (29923.185, 32344.348), (29904.985, 32311.252), (29997.056, 32290.092), (30053.417, 32139.667), (30004.049, 32108.006), (29954.803, 32210.611), (29792.114, 32247.062), (29761.684, 32302.735), (29754.016, 32451.383), (29678.437, 32447.696), (29632.398, 32496.591), (29665.339, 32526.253), (29612.859, 32696.506), (29600.496, 32719.394)],
    [(30178.18, 31923.887), (30138.072, 31887.655), (30257.694, 31773.217), (30389.686, 31405.252), (30701.152, 30991.252), (30840.053, 31053.865), (31044.852, 30781.877), (31014.2, 30757.409), (31373.442, 30493.066), (31453.175, 30560.194), (31332.978, 30864.179), (31012.679, 31323.349), (30737.856, 31286.66), (30712.87, 31331.891), (30556.09, 31450.103), (30454.629, 31577.301), (30434.156, 31607.332), (30313.613, 31812.92)],
]
# v3 (MIRAQUA 28 Oct, P08.1): the two streets of MAIN_SPINE by their point ranges: Bankalar Caddesi from its south end
# to the junction by İstiklal Meydanı (point 23, 30005.0 / 32029.4), Kınık Caddesi from there east over the covered
# stream past Red Hall (as the v1.9 label anchors and stop 3 "Kınık Caddesi over the covered stream")
STREET_NAMES = ((u"Bankalar Caddesi", 0, 24), (u"Kınık Caddesi", 23, len(MAIN_SPINE)))

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


def north_arrow(pg, x, y, a, size=4.0):
    """v2: a north arrow centred on (x, y), size mm long, pointing at angle a (radians on the page); beside the scale
    bar, never on the plan"""
    q = size / 1.3
    ux, uy = math.cos(a), math.sin(a)
    R = lambda f_, g_: (x + ux * f_ - uy * g_, y + uy * f_ + ux * g_)
    tip, l_, m_, r_ = R(0.75 * q, 0.0), R(-0.5 * q, 0.38 * q), R(-0.22 * q, 0.0), R(-0.5 * q, -0.38 * q)
    pg.poly([tip, l_, m_], fill=C["ink"], closed=True)
    pg.poly([tip, m_, r_], fill=C["white"], closed=True)
    pg.poly([tip, l_, m_, r_], stroke=C["ink"], lw=0.15, closed=True)
    nx, ny = R(1.2 * q, 0.0)
    pg.text("N", nx, ny - 0.9, 7, C["ink"], True, "C")


# ------------------------------------------------------------------ v4: the shared basemap, the spine line, pictograms
def bm_draw(pg, T, box=None, mode="base", scale_den=None):
    """v4 (02 §1) / v5 (M3, revision 30 Oct 2026): the shared basemap (common/basemap.py, written by the site board,
    memoised per mode and box) through this sheet's page: T(p) survey m -> page mm; a layer's alpha = its colour
    faded towards the white page. Both maps take the faint "base" mode (buildings by block, faint streets, the
    stream, the ONE study-area outline); scale_den for the roof marks of the buildings. Without basemap data only
    the study-area outline is drawn (basemap_study's recorded copy). Returns the number of items drawn (0 = no
    basemap data, logged)."""
    def col(hx, alpha):
        return tint_hex(hx, 1.0 - (1.0 if alpha is None else max(0.0, min(1.0, float(alpha)))))

    def fill_fn(rings, hx, alpha, nonzero):
        rs = [R_ for R_ in rings if len(R_) >= 3]
        if rs:
            pg.path(rs, fill=col(hx, alpha))

    def line_fn(pts, hx, w_mm, dash_mm, alpha):
        if len(pts) >= 2:
            d_ = (tuple(dash_mm) if isinstance(dash_mm, (list, tuple)) else (dash_mm, dash_mm)) if dash_mm else None
            pg.line(pts, col(hx, alpha), w_mm, dash=d_)
    try:
        items = basemap_items(mode, box=box, scale_den=scale_den)
    except Exception as ex_:
        BM_NOTE.append("basemap not read: %s: %s" % (type(ex_).__name__, ex_))
        items = []
    if not items:
        BM_NOTE.append("FLAG: no basemap data (run the site board v51+ once): the maps draw only the study-area outline")
        try:
            basemap_draw(basemap_study_items(), T, fill_fn, line_fn)
        except Exception as ex_:
            BM_NOTE.append("study-area outline not drawn: %s: %s" % (type(ex_).__name__, ex_))
        return 0
    n = basemap_draw(items, T, fill_fn, line_fn)
    BM_NOTE.extend(basemap_warnings())
    return n


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


def spine_line(L):
    """v4: the streamside spine as a line (survey m): the masterplan's stream reference line (STREAM_REF) from K4 to
    K5, each piece of SPINE moved its offset_m to the bank the vote picked (L["sides"]; NE = the left of the
    downstream direction), piece B on the stream over the covered reach. [(piece id, points)] upstream first; once
    per run (L["spine_line"])."""
    if L.get("spine_line") is not None:
        return L["spine_line"]
    P, _cov = stream_ref()
    cum = [0.0]
    for a, b in zip(P, P[1:]):
        cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))

    def s_of(q):
        best = None
        for i, (a, b) in enumerate(zip(P, P[1:])):
            dx, dy = b[0] - a[0], b[1] - a[1]
            l2 = dx * dx + dy * dy or 1e-9
            t = max(0.0, min(1.0, ((q[0] - a[0]) * dx + (q[1] - a[1]) * dy) / l2))
            d = math.hypot(a[0] + dx * t - q[0], a[1] + dy * t - q[1])
            if best is None or d < best[0]:
                best = (d, cum[i] + t * (cum[i + 1] - cum[i]))
        return best[1]

    def at(s):
        for i in range(1, len(P)):
            if cum[i] >= s:
                t = (s - cum[i - 1]) / max(cum[i] - cum[i - 1], 1e-9)
                return (P[i - 1][0] + (P[i][0] - P[i - 1][0]) * t, P[i - 1][1] + (P[i][1] - P[i - 1][1]) * t)
        return P[-1]
    flip = s_of(SPINE[0]["frm"]) > s_of(SPINE[-1]["to"])
    if flip:                                              # the reference line runs downstream from K4 here
        P = P[::-1]
        cum = [cum[-1] - c_ for c_ in cum[::-1]]
    out = []
    for pc in SPINE:
        s0, s1 = s_of(pc["frm"]), s_of(pc["to"])
        if s1 < s0:
            s0, s1 = s1, s0
        Q = [at(s0)] + [P[i] for i in range(len(P)) if s0 < cum[i] < s1] + [at(s1)]
        bank = L["sides"].get(pc["id"], "over")
        d = float(pc.get("offset_m") or 0.0) * (1.0 if bank == "NE" else (-1.0 if bank == "SW" else 0.0))
        out.append((pc["id"], pl_offset(Q, d) if d else Q))
    L["spine_line"] = out
    return out


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


def ring(pg, x, y, r, col, lw, dash=None, n=72):
    pg.line([(x + r * math.cos(2 * math.pi * i / n), y + r * math.sin(2 * math.pi * i / n)) for i in range(n + 1)],
            col, lw, dash=dash)


def hub_mark(pg, x, y, kind, r=1.9):
    """v4: a hub on a map: walking hub = a ring, the main transit hub = a filled disc in a ring, the gateway = a small
    grey disc"""
    if kind == "transit":
        disc(pg, x, y, r + 0.5, C["white"])
        ring(pg, x, y, r, C["accent"], 0.5)
        disc(pg, x, y, r * 0.55, C["accent"])
    elif kind == "gateway":
        disc(pg, x, y, r * 0.7, C["ink2"], C["white"], 0.3)
    else:
        disc(pg, x, y, r + 0.4, C["white"])
        ring(pg, x, y, r, C["green_deep"], 0.55)


# ------------------------------------------------------------------ page 1 (booklet p.08): the framework diagram
# v4 (T3a WO-T3a-5, package B, D8 b): ONE framework diagram tells the movement story of pp.07-09: shops and use,
# the hidden stream, movement today, the proposals (refs R27-R30, ideas only). It is drawn here because this script
# runs after the site board and before the masterplan: it reads the board's half live (movement_framework.json:
# the busiest streets on foot and by car, the commercial spines, the civic constellations; city_context.json: the
# frame, the shops, the walking radius), holds its own half (spine, hubs, bus stops, shops figures, stream line)
# and the masterplan's proposal (masterplan_results.json "movement": roads by change, crossings, the town line;
# the last run's, as for the spine length).
FW_FILES = [os.path.join(bg_cache("selinus_board"), "movement_framework.json")]   # v4: written by selinus_board v51+
FW_MAP = (14.0, 190.0)                   # page 1 framework: the lower-left corner of the site frame (284.5 x 52.9 mm)
WHO_BOX = (14.0, 168.0, 392.0)           # page 1 who comes and when: x, title y, width
P1_TILES = (14.0, 18.0, 392.0, 35.0)     # page 1 seven reasons: x, y (bottom), w, tile height
WALK_C, CAR_C, BUS_C = "CC9A52", "5C7A86", "633131"   # v4 (R29): one colour per mode
# v5 (revision 30 Oct 2026, p.08 ①): the masterplan's road changes as solid lines in one width family ((colour, width
# mm)); "kept" roads are no change and are not drawn
ROAD_STYLE = {"calmed": ("B5832F", 0.9), "pedestrian": ("8B3A3F", 1.2), "shared": ("7F5B7B", 0.9),
              "relocated": ("C2603A", 0.9)}
ROAD_WORD = {"calmed": "road calmed", "pedestrian": "street made pedestrian", "shared": "shared street",
             "relocated": "road relocated"}
BADGE_PT = 7.5                           # v5 (p.09): the hub badges' type size
# v5 (p.09, G3): each hub's code, the same tag on the map and on its card (T = the main transit hub, İstiklal Meydanı
# + Kızıl Avlu)
HUB_CODE = {"K4": "K4", "K3": "K3", u"İstiklal": "T", "K5": "K5", "K6": "K6"}
# v5 (p.08 ②, G5): the seasons behind the calendar as soft tones of the palette (name, months, colour faded 88 %)
SEASONS_CL = ((u"winter", (12, 1, 2), "91ADB4"), (u"spring", (3, 4, 5), "8C9969"), (u"summer", (6, 7, 8), "CC9A52"),
              (u"autumn", (9, 10, 11), "B5832F"))
MON = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def page_framework(L):
    """v4 (D8 b): page 1, booklet p.08: the framework diagram on the shared simple basemap, the whole site frame at
    1:10,000 on the frame's axes (a diagram: no scale bar, the rings give the metres), its key beside it; who the
    project brings (G7) under it; the seven reasons as tiles at the bottom. The v3 shops plan, the two shop charts
    and the walking potential bars are gone (the framework holds the plan's story; D3 b: the bars said nothing)."""
    pg = Page(420, 297)
    SRC_KEY[:] = []
    header(pg, "THE STREAM JOINS THE TOWN WHERE THE SHOPS ALREADY ARE",
           "shops on **two streets** · the stream **hidden** where the main road meets it · **hubs** at the bridges "
           "tie both to a **streamside spine**")
    framework_map(pg, L)
    who_panel(pg, L)
    reasons_tiles(pg)
    PAGE_SRC[0] = list(SRC_KEY)
    return pg


def framework_map(pg, L):
    """v5 (revision 30 Oct 2026, p.08 ①, G1 G3 G5): the framework on the site frame at 1:10,000 in ONE graphic
    language on the shared faint base (M3 "base": buildings by block, faint streets, the stream, the study-area
    outline). TODAY = soft bands under, one width family (shop streets, the busiest driving and walking routes;
    drawn without multiply, so overlapping runs keep one tone instead of dark beads). THE PROJECT = crisp lines and
    round marks over (the streamside spine, the masterplan's road changes, the town bus line, new crossings, the hubs,
    the one place the main road meets the stream). Every element has its row in the legend beside the map (M2
    Legend); names and the shops callout placed by lp_place (M2), street and stream names along their lines; scale
    bar and north arrow under the map. Gone (read as noise): the civic zones (purple hatch), the reach rings, the
    "kept" roads, the use arrows, the mode pictograms on the map. Only data the scripts hold; a layer whose data is
    missing is left out (logged)."""
    mx, my = FW_MAP
    ctx = L.get("ctx") or {}
    fw = L.get("fw") or {}
    M = L.get("mpmv") or {}
    f = site_frame(ctx)
    T = frame_T(f, mx, my, PLAN_DEN)
    k = 1000.0 / PLAN_DEN
    fw_, fh_ = f["w"] * k, f["h"] * k
    box_ = (mx, my, mx + fw_, my + fh_)
    PLAN_BOX["fw"] = box_
    inside = lambda q: mx <= q[0] <= mx + fw_ and my <= q[1] <= my + fh_
    frame = (mx + 1.0, my + 1.0, mx + fw_ - 1.0, my + fh_ - 1.0)
    tx = step(pg, 1, mx, my + fh_ + 6.5)
    fit(pg, ("ONE FRAMEWORK · SHOPS, THE HIDDEN STREAM, MOVEMENT TODAY AND WHAT THE PROJECT CHANGES " +
             cite(SRC_MAIN) + " " + cite(SRC_SHOPS)).strip(), tx, my + fh_ + 6.5, 10, mx + fw_ - tx, C["ink"], True)
    KP = 72 / 25.4
    pg.ops.append("q %.2f %.2f %.2f %.2f re W n" % (mx * KP, my * KP, fw_ * KP, fh_ * KP))
    nb = bm_draw(pg, T, frame_box(f, f["u0"], f["v0"], f["u0"] + f["w"], f["v0"] + f["h"]), "base", PLAN_DEN)
    lines_ = []                                           # the linework labels keep off (M2)
    # TODAY: soft bands under
    spines = fw.get("spines") or [dict(label=u"Bankalar - Kınık Caddesi", runs=[MAIN_SPINE])]
    if not fw.get("spines"):
        BM_NOTE.append("FLAG: no movement_framework.json (site board v51+): the main spine stands in for the shop "
                       "streets, no busiest streets drawn")
    for g in spines:
        for R_ in g["runs"]:
            pg.line([T(p) for p in R_], tint_hex(SPINE_C, 0.55), 3.6)
    today = []
    for tag, colr, word in (("car", CAR_C, "today: busiest driving route"), ("walk", WALK_C,
                                                                            "today: busiest walking route")):
        sts = fw.get(tag) or []
        for st in sts:
            for R_ in st["runs"]:
                pg.line([T(p) for p in R_], tint_hex(colr, 0.55), 1.8)
        if sts:
            today.append((word, tint_hex(colr, 0.55)))
    # the stream hidden under the town (the reference line's covered pieces), dashed as the basemap's covered course
    P, cov = stream_ref()
    open_pts = []
    for c_, R_ in clip_runs(P, (-1e9, -1e9, 1e9, 1e9), cov):
        Q = [T(p) for p in R_]
        if c_:
            pg.line(Q, C["water_deep"], 1.0, dash=(1.6, 0.9))
        else:
            open_pts.append([q for q in Q if inside(q)])
        lines_.append(Q)
    # THE PROJECT: crisp lines over, each on a white casing
    road_seen = []
    for rd in M.get("roads") or []:
        ch = rd.get("change", "kept")
        R_ = rd.get("xy") or []
        if ch not in ROAD_STYLE or len(R_) < 2:
            continue
        col_, lw_ = ROAD_STYLE[ch]
        Q = [T(p) for p in R_]
        pg.line(Q, C["white"], lw_ + 0.6)
        pg.line(Q, col_, lw_)
        lines_.append(Q)
        if ch not in road_seen:
            road_seen.append(ch)
    bus_seen = False
    for rt in M.get("routes") or []:
        R_ = rt.get("xy") or []
        if len(R_) >= 2:
            Q = pl_offset([T(p) for p in R_], 1.0)
            pg.line(Q, C["white"], 1.1)
            pg.line(Q, BUS_C, 0.5)
            lines_.append(Q)
            bus_seen = True
    allq = []
    for pid, R_ in spine_line(L):
        Q = [T(p) for p in R_]
        allq += Q if not allq else Q[1:]
    if len(allq) >= 2:
        pg.line(allq, C["white"], 2.4)
        pg.line(allq, SPINE_C, 1.6)
        arrow_head(pg, allq[1], allq[0], SPINE_C, 3.0)
        arrow_head(pg, allq[-2], allq[-1], SPINE_C, 3.0)
        lines_.append(allq)
    obst, cross_seen = [], []
    for c_ in M.get("crossings") or []:
        q = c_.get("xy")
        kind = c_.get("kind", "footbridge")
        if not q or kind == "bridge kept":
            continue
        px, py = T(q)
        if not inside((px, py)):
            continue
        d_ = stream_dir(q)
        nx, ny = -d_[1], d_[0]
        a0, a1 = T((q[0] - nx * 14.0, q[1] - ny * 14.0)), T((q[0] + nx * 14.0, q[1] + ny * 14.0))
        if kind == "stepping stones":
            for t_ in (0.2, 0.5, 0.8):
                disc(pg, a0[0] + (a1[0] - a0[0]) * t_, a0[1] + (a1[1] - a0[1]) * t_, 0.42, C["ink"], C["white"], 0.15)
        else:
            pg.line([a0, a1], C["white"], 1.1)
            pg.line([a0, a1], C["ink"], 0.6)
        obst.append((px - 1.6, py - 1.6, px + 1.6, py + 1.6))
        if kind not in cross_seen:
            cross_seen.append(kind)
    pg.ops.append("Q")
    marks, hub_seen = [], []
    for hb in hub_list():                                 # the hubs over everything (İstiklal + Kızıl Avlu both)
        pts_ = [(hb["xy"], u"İstiklal Meydanı" if hb["kind"] == "hidden" else hb["title"].split(u" · ")[0])]
        if hb["id"] == u"İstiklal":
            pts_.append((list(HUB_PTS["RED"]), u"Kızıl Avlu"))
        for q, nm in pts_:
            hx, hy = T(q)
            if inside((hx, hy)):
                kind = "transit" if hb["transit"] else hb["kind"]
                hub_mark(pg, hx, hy, kind)
                obst.append((hx - 2.6, hy - 2.6, hx + 2.6, hy + 2.6))
                marks.append(dict(kind="text", s=nm, at=(hx, hy), size=8, r=2.4,
                                  col=C["accent"] if hb["transit"] else C["ink"]))
                if kind not in hub_seen:
                    hub_seen.append(kind)
    jx, jy = T((30058.0, 32047.0))                          # Kınık Caddesi over the covered stream (stop 3's place)
    disc(pg, jx, jy, 1.3, C["accent"], C["white"], 0.3)
    obst.append((jx - 1.8, jy - 1.8, jx + 1.8, jy + 1.8))
    pg.rect(mx, my, fw_, fh_, stroke=C["ink"], lw=0.25)
    # names along their own lines (streets, the stream), then the hubs and the shops callout by lp_place
    pts = [((b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0) for b in obst]
    segs = [sg for Q in lines_ for sg in zip(Q, Q[1:])]
    for g in spines:
        if not g.get("label") or g["label"] == "an unnamed street":
            continue
        Q = [q for q in (T(p) for p in max(g["runs"], key=len)) if inside(q)]
        if len(Q) > 1 and not along_label(pg, g["label"], Q, 8, C["accent"], frame, pts, segs, 3.6):
            marks.append(dict(kind="text", s=g["label"], at=Q[len(Q) // 2], size=8, col=C["accent"], rank=1))
    for Q in sorted([Q for Q in open_pts if len(Q) > 1], key=len, reverse=True)[:3]:
        if along_label(pg, "Selinos stream", Q, 8, C["water_deep"], frame, pts, [], 1.2):
            break
    sf = shop_figures()
    marks.append(dict(kind="callout", at=(jx, jy), r=1.3, lead=C["accent"],
                      lines=[("%d of %d shops" % (sf["covered_reach"], sf["by_stream"]), 12, C["accent"], True),
                             ("by the stream sit on the covered %d m, where the main road meets it" %
                              sf["covered_reach_m"], 7.5, C["ink"], False)]))
    place_marks(pg, marks, frame, obst, lines_, max_leader=14.0)
    north_arrow(pg, mx + 4.0, my - 6.0, math.atan2(math.cos(f["ang"]), math.sin(f["ang"])))
    scale_bar(pg, mx + 12.0, my - 6.5, PLAN_DEN)
    # the legend beside the map (G1): the base, today, the project, every element drawn
    lg = Legend(box_, side="right", gap=max(3.0, grid_x(10) - box_[2]), y_down=False, swatch=(6.0, 2.6))
    if nb:
        lg.add("Selinos stream", "draw", draw=sw_fill(BM_COL["water"], BM_COL["water_edge"]))
    lg.add("Selinos stream, covered", "draw", draw=sw_line(C["water_deep"], 1.0, (1.6, 0.9)))
    if nb:
        lg.add("buildings", "draw", draw=sw_fill(BM_FAINT["bld_veryfaint"], BM_FAINT["road_line"]))
    lg.add("study area", "draw", draw=sw_line(R28_STUDY_LINE["colour"], R28_STUDY_LINE["width_mm"],
                                              tuple(R28_STUDY_LINE["dash_mm"])))
    lg.add("today: shop street" if fw.get("spines") else "today: main shop street", "draw",
           draw=sw_line(tint_hex(SPINE_C, 0.55), 2.6))
    for word, colr in today:
        lg.add(word, "draw", draw=sw_line(colr, 1.8))
    if len(allq) >= 2:
        lg.add("streamside spine (walking flow)", "draw", draw=sw_line(SPINE_C, 1.4, arrow=True))
    for ch in ("pedestrian", "calmed", "shared", "relocated"):
        if ch in road_seen:
            lg.add(ROAD_WORD[ch], "draw", draw=sw_line(ROAD_STYLE[ch][0], ROAD_STYLE[ch][1]))
    if bus_seen:
        lg.add("town bus line to K4, later step", "draw", draw=sw_line(BUS_C, 0.5))
    if "footbridge" in cross_seen:
        lg.add("new footbridge", "draw", draw=sw_mark(lambda p_, x, y: p_.line([(x, y - 1.3), (x, y + 1.3)], C["ink"], 0.6)))
    if "stepping stones" in cross_seen:
        lg.add("new stepping stones", "draw",
               draw=sw_mark(lambda p_, x, y: [disc(p_, x + d_, y, 0.42, C["ink"]) for d_ in (-1.8, 0.0, 1.8)]))
    for kind, word in (("walk", "walking hub at a bridge"), ("transit", "main transit hub"),
                       ("hidden", "hub over the covered stream"), ("gateway", "gateway out of town")):
        if kind in hub_seen:
            lg.add(word, "draw", draw=sw_mark(lambda p_, x, y, kd=kind: hub_mark(p_, x, y, kd, 1.2)))
    lg.add("the main road meets the stream", "draw",
           draw=sw_mark(lambda p_, x, y: disc(p_, x, y, 1.1, C["accent"], C["white"], 0.3)))
    lay = lg_draw(pg, lg, max_h=fh_ + 12.0)
    PLAN_BOX["fw_key"] = lay["box"]


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
    under it (M2 Legend) and one line of conclusion, made from the same data, on the title line."""
    x0, ty, W = WHO_BOX
    x1 = x0 + W
    tx = step(pg, 2, x0, ty)
    pg.text("WHO COMES TO THE STREAM, AND WHEN", tx, ty, 9, C["ink"], True)
    ax0, ax1 = 178.0, x1                                  # the month axis (mm)
    mw = (ax1 - ax0) / 12.0
    MX = lambda m: ax0 + (m - 1) * mw                     # left edge of month m
    PITCH, STRIP, GAP = 2.9, 6.5, 2.4
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
            fit(pg, a["name"], 120.5, ry - 0.85, 7, ax0 - 122.0, C["ink"])
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
    # the key under the calendar (M2 Legend, G1)
    gc = GROUP["L"][1]

    def sw_bars(p_, b):
        for i in range(3):
            p_.rect(b[0] + i * 2.1, b[1], 1.7, (b[3] - b[1]) * (0.45 + 0.27 * i), fill=tint_hex(gc, 0.3))

    def sw_ticks(p_, b):
        for i in range(4):
            p_.line([(b[0] + 0.6 + i * 1.6, b[1] + 0.3), (b[0] + 0.6 + i * 1.6, b[3] - 0.3)], gc, 0.45)
    lg = Legend((x0, yb, x1, ys), side="below", gap=2.5, y_down=False, swatch=(6.0, 2.6))
    lg.add("places open to the group that month", "draw", draw=sw_bars)
    lg.add("the group at the stream", "draw",
           draw=sw_mark(lambda p_, x, y: put_shapes(p_, ico_draw("people", x, y, 2.8, ink=gc, accent=gc))))
    lg.add("open all year", "draw", draw=lambda p_, b: p_.rect(b[0], b[1] + 0.6, b[2] - b[0], 1.4,
                                                                fill=tint_hex(gc, 0.62)))
    lg.add("open in season only", "draw", draw=sw_fill(gc))
    lg.add("market day, once a week", "draw", draw=sw_ticks)
    if river:
        lg.add("Selinos stream: mean monthly flow", "draw",
               draw=lambda p_, b: [p_.rect(b[0] + i * 2.1, b[1], 1.7, (b[3] - b[1]) * (1.0 - 0.4 * i),
                                           fill=C["water"]) for i in range(3)])
    lay = lg_draw(pg, lg)
    PLAN_BOX["who"] = (x0, lay["box"][1] - 1.0, x1, ty + 4.0)


def reasons_tiles(pg):
    """the seven reasons the stream edge has no spine (v1.6 tiles, kept): pictogram, one figure, keywords"""
    rx, ry, rw, rh = P1_TILES
    tx = step(pg, 3, rx, ry + rh + 3.5)
    pg.text("SEVEN REASONS THE STREAM EDGE HAS NO SPINE", tx, ry + rh + 3.5, 9, C["ink"], True)
    tw_ = rw / 7.0
    for i, (ic, head, big, kws, src) in enumerate(REASONS):
        if ic == "deep" and not big:
            big = bed_depth()
        x = rx + i * tw_
        pg.rect(x, ry, tw_ - 3, rh, stroke=C["faint"], lw=0.3)
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
# Points in survey m: bridges h01 §0/§5 (s62); İstiklal Meydanı = h01 §5 P16 label; Red Hall = h01 §5 P02.
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
# stream; 2 workshops -> K3 (H3 tanning reach); 3 junction square over the covered reach + 4 Red Hall terrace -> the
# İstiklal Meydanı + Kızıl Avlu cluster (H2: the covered reach and its Red Hall tunnel mouths); 5 market -> K5;
# 8 summer bed events -> the in-bed sub-hubs of K3, K4, K5 (D10).
HUBS = [
    dict(id="K4", title="K4 · Ulucami Önü", pt="K4", ch=CH["K4"], kind="walk", role="Ulu Cami + Tabaklar Hamamı",
         bus=[("Camikebir Caddesi", "K4")], trips="today 831-833 only · 2-3 trips a day each way",
         later="later step: a town line (e.g. 651) extended to K4", stops=[7, 1]),
    dict(id="K3", title="K3 · Tabak Köprüsü", pt="K3", ch=CH["K3"], kind="walk", role="the tanning reach: craft",
         bus=[("Tabak Köprüsü", "K3")], trips="831-833 only · 2-3 trips a day each way", stops=[6, 2]),
    dict(id="İstiklal", title="İstiklal Meydanı + Kızıl Avlu", pt="IST", ch=752, kind="hidden",
         role="the covered reach", bus=[("İstiklal Meydanı", "IST"), ("Kızıl Avlu", "RED")],
         trips="651: 54 departures a weekday, every 15-20 min", stops=[3, 4]),
    dict(id="K5", title="K5 · Üç Kemer Köprüsü", pt="K5", ch=CH["K5"], kind="walk", role="producers' market",
         bus=[("Üç Kemer Köprüsü", "K5")], trips="656: 12 a weekday · 831-833: 2-3", stops=[5]),
    dict(id="K6", title="K6 · road bridge", pt="K6", ch=CH["K6"], kind="gateway", role="gateway out of town",
         bus=[("Bergama Sanayi", "K6")], trips="643 644 651 652 653 656 836 936", stops=[]),
]
SRC_BUS = ("OpenStreetMap contributors, extract of 28 Jul 2026 (bus stops); ESHOT open data (lines and weekday "
           "trips)")                               # v4 (D13): the public sources only
SRC_HUBS = "Hubs: history decisions D2 D3 D8 D10 and Aras 27 Oct 12:05 (history_phase1/DECISIONS.md)"
SRC_PLANE = ("Plane trees: Ottoman squares with plane trees (h02, ICOMOS s13 p281); drought-sensitive, watered "
             "(h03 Q4)")
SRC_HIDDEN = "Covered reach: Red Hall twin tunnels (h02 E01); the stream under İstiklal Meydanı (h02 E02)"
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
    square over its culvert; the gateway as a road out. Graphic only."""
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
        roundel(pg, x + 6.9 * ux, y - h + 3.6 * uy, 8, r=2.2)                         # stop 8: bed events
    elif kind == "hidden":
        pg.poly(P([(0, 0), (0, 5.6), (10, 5.6), (10, 0)]), fill=C["structure"], closed=True)
        pg.poly(P([(3.2, 0.6), (7.2, 0.6), (7.2, 2.6), (6.4, 3.4), (4.0, 3.4), (3.2, 2.6)]), fill=C["water_light"], closed=True)
        pg.poly(P([(3.2, 0.6), (7.2, 0.6), (7.2, 1.3), (3.2, 1.3)]), fill=C["water"], closed=True)
        pg.line(P([(0, 5.6), (10, 5.6)]), C["ink"], 0.6)
        pg.line(P([(2.0, 5.95), (8.4, 5.95)]), C["water_deep"], 0.9)                   # the water line in the paving
    else:
        pg.poly(P([(0, 2.6), (7.0, 2.6), (7.0, 4.4), (0, 4.4)]), fill=C["ink2"], closed=True)
        pg.poly(P([(7.0, 1.6), (10, 3.5), (7.0, 5.4)]), fill=C["accent"], closed=True)


def hub_fill(hb):
    """v5: a hub's colour: the main transit hub accent, the gateway grey, a walking hub green"""
    return C["accent"] if hb["transit"] else (C["ink2"] if hb["kind"] == "gateway" else C["green_deep"])


def hub_badge(pg, code, x, y, fill, h=3.8):
    """v5 (revision 30 Oct 2026, p.09, G3): a hub's code (HUB_CODE: K4, K3, T, K5, K6) on a filled tag, lower-left at
    (x, y): the same tag on the map and on the hub's card, so each card is found on the map without a leader;
    returns its width"""
    z = BADGE_PT * h / 3.8
    w = text_w(code, z, True) + 2.4 * h / 3.8
    pg.rect(x, y, w, h, fill=fill)
    pg.text(code, x + w / 2.0, y + h / 2.0 - 0.265 * z * 0.3528, z, C["white"], True, "C")
    return w


def hub_card(pg, hb, x, y0, w, h):
    """v1.11 / v5 (revision 30 Oct 2026, p.09 compact, G3 G4): one bridge place: its badge (the same tag as on the
    map) and name, its role, its existing bus stops (lines, metres), its two levels (or hidden square / gateway) and
    the places of its cluster, numbered as on the map, with who they serve and what they grow from. The flood depths
    are printed once on the page, on the flood rule."""
    y1 = y0 + h
    tr = hb["transit"]
    hf = hub_fill(hb)
    pg.rect(x, y0, w, h, stroke=C["faint"], lw=0.3)
    pg.rect(x, y1 - 1.4, w, 1.4, fill=hf)
    bw = hub_badge(pg, HUB_CODE.get(hb["id"], hb["id"]), x + 2.5, y1 - 7.6, hf)
    fit(pg, hb["title"], x + 4.0 + bw, y1 - 6.9, 11, w - 6.5 - bw, C["ink"], True)
    role = ("MAIN TRANSIT HUB · " if tr else ("walking hub · " if hb["kind"] == "walk" else "")) + hb["role"]
    fit(pg, role, x + 2.5, y1 - 11.0, 7.5, w - 5, C["accent"] if tr else C["ink2"], tr)
    yy = y1 - 17.0
    for st in hb["bus_stops"]:
        icon(pg, "bus", x + 2.5, yy + 3.4, 4.4)
        dist = "%d m" % st["m"]
        dw = text_w(dist, 9, True)
        lw_ = text_w(st["lines"], 7)
        pg.text(dist, x + w - 2.5, yy, 9, SPINE_C, True, "R")
        pg.text(st["lines"], x + w - 5.0 - dw, yy, 7, C["ink2"], False, "R")
        fit(pg, st["name"], x + 8.5, yy, 8, w - 14.0 - dw - lw_, C["ink"], True)
        yy -= 5.5
    if hb.get("later"):                                    # the proposed town-line extension: dashed bus, accent words
        pg.rect(x + 2.5, yy - 1.0, 4.4, 4.4, stroke=C["accent"], lw=0.3)
        fit(pg, hb["later"], x + 8.5, yy, 7, w - 11.0, C["accent"], True)
        yy -= 5.0
    fit(pg, hb["trips"], x + 8.5, yy + 0.6, 7, w - 11.0, C["ink2"])
    gy = y1 - 30.0 if not hb.get("later") and len(hb["bus_stops"]) < 2 else y1 - 35.0
    hub_glyph(pg, hb["kind"], x + 2.5, gy, 26.0, 18.0)
    kx = x + 31.0
    if hb["kind"] == "walk":
        kws = [("DRY HUB · street level, above Q500", True), (PLANE_NAME + " " + cite(SRC_PLANE), False),
               ("trees watered from storage", False), ("SUB-HUB in the bed", True),
               ("open Jul-Sep · shut in floods " + cite(SRC_WET), False)]
    elif hb["kind"] == "hidden":
        kws = [("HIDDEN STREAM SQUARE", True), ("water line in the paving " + cite(SRC_HIDDEN), False),
               ("over the culvert", False), ("RED HALL TUNNEL MOUTHS", True), ("a viewing edge", False)]
    else:
        kws = [("GATEWAY OUT", True), ("no hub square", False)]
    ky_ = gy - 0.5
    for j, (s, b_) in enumerate(kws):
        if j and b_:
            ky_ -= 1.2
        fit(pg, s.strip(), kx, ky_, 7.5 if b_ else 7, x + w - 2.0 - kx, C["ink"], b_)
        ky_ -= 3.2
    sy = gy - 22.0
    for n in hb["stops"]:
        f = [g for g in FUNCS + [EVENTS] if g["n"] == n][0]
        roundel(pg, x + 5.0, sy + 0.9, n, r=2.6)
        fit(pg, f["name"], x + 9.0, sy, 7.5, w - 11.0, C["ink"], True)
        fit(pg, f["kw"][0], x + 9.0, sy - 3.6, 7, w - 11.0, C["ink"])
        group_dots(pg, x + 10.2, sy - 6.4, f["who"], r=1.1)
        gx = x + 19.5
        for g_ in f["grows"]:
            pg.rect(gx, sy - 7.7, 3.0, 2.6, fill=GROW_C[g_])
            pg.text(g_, gx + 1.5, sy - 7.1, 7, C["white"], True, "C")
            gx += 3.4
        if n == 7:                                         # the entry lies upstream of the hub (chainage, calculated)
            pg.text("about %d m upstream of K4" % int(round((CH["K4"] - FUNCS[6]["ch"]) / 10.0) * 10), gx + 1.5,
                    sy - 7.3, 7, C["ink2"])
        fit(pg, f["kw"][1] + (" " + cite(f["src"]) if f.get("src") else ""), x + 9.0, sy - 10.8, 7, w - 11.0, C["ink"])
        sy -= 12.6

# ------------------------------------------------------------------ page 2: the streamside spine, hub by hub
def page_spine(L):
    """v5 (revision 30 Oct 2026, p.09, G1 G3 G4, D3): booklet p.09. (1) The whole study area (çalışma alanı) on one
    map on the shared faint base with its ONE outline (M3), on the site frame's axes at the largest standard scale
    that fits: the streamside spine K4-K5 bold and the masterplan's streamside walks across the whole project thin
    (how the spine carries on), the main road, the hubs as badges and the places as numbers, both placed by lp_place
    (M2) and matched on the cards (no leaders); its legend beside it, scale bar and north arrow under it. The five
    bridge places as compact cards. (2) The flood rule as a stair of its three levels, the rules on their step;
    (3) which bank: per piece a glyph of the bank it takes beside its paired bars; the producers' market with the
    two farm areas this page prints (M10 facts; the stored water's volume is p.10's)."""
    pg = Page(420, 297)
    SRC_KEY[:] = []                               # v1.6: each page has its own numbered key
    header(pg, "THE STREAMSIDE SPINE, HUB BY HUB",          # v2: no length (Prompt 3: reach, not a fixed line)
           "five **bridge places** on existing bus stops · walking hubs with a **sub-hub in the bed** · one transit hub")
    hubs = hub_list()
    ctx = L.get("ctx") or {}
    f = site_frame(ctx)
    try:
        study = basemap_study()
    except Exception:
        study = []
    study = study or [[tuple(p) for p in R] for R in CL_STUDY]
    uv = [frame_uv(f, p) for R in study for p in R] + [frame_uv(f, hb["xy"]) for hb in hubs]
    u0w, u1w = min(q[0] for q in uv) - 30.0, max(q[0] for q in uv) + 30.0
    v0w, v1w = min(q[1] for q in uv) - 30.0, max(q[1] for q in uv) + 30.0
    den = r28_scale(u1w - u0w, P2_MAP_W, v1w - v0w, P2_MAP_HMAX)
    k = 1000.0 / den
    x0, ytop = P2_MAP
    mw_, mh_ = (u1w - u0w) * k, (v1w - v0w) * k
    y0m = ytop - mh_
    T = frame_T(f, x0, y0m, den, u0w, v0w)
    box_ = (x0, y0m, x0 + mw_, ytop)
    frame = (x0 + 1.0, y0m + 1.0, x0 + mw_ - 1.0, ytop - 1.0)
    inside = lambda q: x0 <= q[0] <= x0 + mw_ and y0m <= q[1] <= ytop
    PLAN_BOX["spine"], PLAN_BOX["spine_den"] = box_, den
    tx = step(pg, 1, 14, ytop + 6.0)
    pg.text(("THE SPINE ACROSS THE STUDY AREA, HUB BY HUB · 1:%s " % fmt(den) + cite(SRC_BUS)).strip(), tx,
            ytop + 6.0, 9, C["ink"], True)
    KP = 72 / 25.4
    pg.ops.append("q %.2f %.2f %.2f %.2f re W n" % (x0 * KP, y0m * KP, mw_ * KP, mh_ * KP))
    nb = bm_draw(pg, T, frame_box(f, u0w, v0w, u1w, v1w), "base", den)
    lines_, open_pts = [], []
    P, cov = stream_ref()
    for c_, R_ in clip_runs(P, (-1e9, -1e9, 1e9, 1e9), cov):
        Q = [T(p) for p in R_]
        if c_:
            pg.line(Q, C["water_deep"], 1.0, dash=(1.6, 0.9))
        else:
            open_pts.append([q for q in Q if inside(q)])
        lines_.append(Q)
    walks = L.get("walks") or []
    if not walks:
        BM_NOTE.append("FLAG: no masterplan streamside walks (masterplan_results.json, option A): p.09 shows the "
                       "spine K4-K5 only")
    for W_ in walks:
        pg.line([T(p) for p in W_], tint_hex(SPINE_C, 0.4), 0.7)
    for _, R_ in clip_runs([tuple(p) for p in MAIN_SPINE], (-1e9, -1e9, 1e9, 1e9)):
        Q = [T(p) for p in R_]
        pg.line(Q, C["accent"], 0.8)
        lines_.append(Q)
    allq = []
    for pid, R_ in spine_line(L):
        Q = [T(p) for p in R_]
        allq += Q if not allq else Q[1:]
    if len(allq) >= 2:
        pg.line(allq, C["white"], 2.4)
        pg.line(allq, SPINE_C, 1.6)
        arrow_head(pg, allq[1], allq[0], SPINE_C, 3.0)
        arrow_head(pg, allq[-2], allq[-1], SPINE_C, 3.0)
        lines_.append(allq)
    pg.ops.append("Q")
    pg.rect(x0, y0m, mw_, mh_, stroke=C["ink"], lw=0.25)
    # the existing bus stops, then the hubs over them, then the places; badges and numbers placed by lp_place (M2)
    obst, marks, hub_seen, stop_seen = [], [], [], False
    hpts = []
    for hb in hubs:
        pts_ = [(hb["xy"], hb["bus_stops"][0])] + ([(list(HUB_PTS["RED"]), hb["bus_stops"][1])]
                                                   if len(hb["bus_stops"]) > 1 else [])
        for q, st in pts_:
            hx, hy = T(q)
            if not inside((hx, hy)):
                continue
            sx, sy = T(st["xy"])
            if inside((sx, sy)):
                disc(pg, sx, sy, 1.0, C["white"], C["water_deep"], 0.3)
                obst.append((sx - 1.2, sy - 1.2, sx + 1.2, sy + 1.2))
                stop_seen = True
            hpts.append((hb, hx, hy))
    for hb, hx, hy in hpts:
        kind = "transit" if hb["transit"] else hb["kind"]
        hub_mark(pg, hx, hy, kind, 1.5)
        obst.append((hx - 2.0, hy - 2.0, hx + 2.0, hy + 2.0))
        marks.append(dict(kind="badge", s=HUB_CODE.get(hb["id"], hb["id"]), fill=hub_fill(hb), at=(hx, hy), r=1.6))
        if kind not in hub_seen:
            hub_seen.append(kind)
    for f_ in FUNCS:                                      # the places of the project, numbered as on the cards
        if f_.get("xy"):
            px, py = T(f_["xy"])
            if inside((px, py)):
                disc(pg, px, py, 0.5, C["ink"])
                obst.append((px - 0.6, py - 0.6, px + 0.6, py + 0.6))
                marks.append(dict(kind="roundel", s=f_["n"], at=(px, py), r=0.5))
    for Q in sorted([Q for Q in open_pts if len(Q) > 1], key=len, reverse=True)[:3]:
        if along_label(pg, "Selinos stream", Q, 8, C["water_deep"], frame,
                       [((b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0) for b in obst], [], 1.2):
            break
    place_marks(pg, marks, frame, obst, lines_, max_leader=8.0)
    north_arrow(pg, x0 + 4.0, y0m - 6.0, math.atan2(math.cos(f["ang"]), math.sin(f["ang"])))
    scale_bar(pg, x0 + 12.0, y0m - 6.5, den)
    lg = Legend(box_, side="right", gap=max(3.0, grid_x(10) - box_[2]), y_down=False, swatch=(6.0, 2.6))
    if nb:
        lg.add("Selinos stream", "draw", draw=sw_fill(BM_COL["water"], BM_COL["water_edge"]))
    lg.add("Selinos stream, covered", "draw", draw=sw_line(C["water_deep"], 1.0, (1.6, 0.9)))
    if nb:
        lg.add("buildings", "draw", draw=sw_fill(BM_FAINT["bld_veryfaint"], BM_FAINT["road_line"]))
    lg.add("study area", "draw", draw=sw_line(R28_STUDY_LINE["colour"], R28_STUDY_LINE["width_mm"],
                                              tuple(R28_STUDY_LINE["dash_mm"])))
    if len(allq) >= 2:
        lg.add("streamside spine, K4 to K5", "draw", draw=sw_line(SPINE_C, 1.4, arrow=True))
    if walks:
        lg.add("streamside walks, whole project", "draw", draw=sw_line(tint_hex(SPINE_C, 0.4), 0.7))
    lg.add("main road: Bankalar - Kınık Cd.", "draw", draw=sw_line(C["accent"], 0.8))
    for kind, word in (("walk", "walking hub at a bridge"), ("transit", "main transit hub"),
                       ("hidden", "hub over the covered stream"), ("gateway", "gateway out of town")):
        if kind in hub_seen:
            lg.add(word, "draw", draw=sw_mark(lambda p_, x, y, kd=kind: hub_mark(p_, x, y, kd, 1.2)))
    lg.add("hub code, as on its card", "draw",
           draw=lambda p_, b: hub_badge(p_, "K4", b[0], b[1] - 0.3, C["green_deep"], 3.2))
    if stop_seen:
        lg.add("existing bus stop", "draw",
               draw=sw_mark(lambda p_, x, y: disc(p_, x, y, 1.0, C["white"], C["water_deep"], 0.3)))
    lg.add("place, numbered as on the cards", "draw",
           draw=sw_mark(lambda p_, x, y: (disc(p_, x, y, 1.3, C["ink"]),
                                          p_.text("1", x, y - 0.6, 6, C["white"], True, "C"))))
    lg_draw(pg, lg, max_h=mh_ + 8.0)
    # the five bridge places, under the map; each found on it by its badge
    cx_, cw_all, ch_, gap = P2_CARD
    cy0 = y0m - 12.0 - ch_
    PLAN_BOX["cards"] = (cx_, cy0, cw_all, ch_)
    cw = (cw_all - gap * (len(hubs) - 1)) / len(hubs)
    for i, hb in enumerate(hubs):
        hub_card(pg, hb, cx_ + i * (cw + gap), cy0, cw, ch_)
    ly = cy0 - 5.5                                        # the cards' key, under them
    lx = 14.0
    pg.text("who:", lx, ly, 7, C["ink2"], True); lx += text_w("who:", 7, True) + 2.0
    for g_ in "LTS":
        disc(pg, lx + 1.1, ly + 0.9, 1.1, GROUP[g_][1])
        pg.text(GROUP[g_][0], lx + 3.2, ly, 7, C["ink"]); lx += 3.2 + text_w(GROUP[g_][0], 7) + 3.5
    pg.text("grows from:", lx, ly, 7, C["ink2"], True); lx += text_w("grows from:", 7, True) + 2.0
    for g_ in "WEAH":
        pg.rect(lx, ly - 0.5, 3.0, 2.6, fill=GROW_C[g_])
        pg.text(g_, lx + 1.5, ly + 0.1, 7, C["white"], True, "C")
        pg.text(GROWS[g_], lx + 4.2, ly, 7, C["ink"]); lx += 4.2 + text_w(GROWS[g_], 7) + 3.5
    icon(pg, "bus", lx, ly + 2.6, 3.4)
    pg.text("existing stop: lines, metres " + cite(SRC_BUS), lx + 4.6, ly, 7, C["ink"])
    pg.text(("hubs linked on foot by the spine " + cite(SRC_HUBS)).strip(), 406, ly, 7, C["ink2"], False, "R")
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
            fit(pg, (kk + (" " + cite(wsrc) if jj == len(wet) - 1 else "")).strip(), tx_, y - 2.4 - jj * 3.0, 7,
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
        pg.text("NE", gx1 + 0.8, rc + 1.0, 6, C["ink2"])
        pg.text("SW", gx1 + 0.8, rc - 2.9, 6, C["ink2"])
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
            BM_NOTE.append("FLAG: %s not read (run the water balance first): left off p.09's market" % key)
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
                script="bergama_city_link_v5.py", version=VERSION, run_time=time.strftime("%Y-%m-%d %H:%M:%S"),
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
    crop("cl_framework", 0, px0 - 0.5, min(py0 - 11.5, kb[1] - 1.0), 406.0, py1 + 10.0,
         ("One framework: shops, the hidden stream, movement today and what the project changes " +
          mk(0, SRC_MAIN, SRC_SHOPS)).strip(), bk_w=406.0 - (px0 - 0.5))
    wb = PLAN_BOX.get("who") or (WHO_BOX[0], 62.0, WHO_BOX[0] + WHO_BOX[2], WHO_BOX[1] + 4.0)
    crop("cl_who", 0, wb[0] - 0.5, wb[1], wb[2] + 0.5, wb[3],
         ("Who comes to the stream, and when " + mk(0, SRC_WHO_T, SRC_WHO_L, SRC_WHO_S1, SRC_WHO_S2)).strip(),
         bk_w=wb[2] - wb[0] + 1.0)
    x0, y0, w, h = P1_TILES
    crop("cl_reasons", 0, x0, y0 - 1.0, x0 + w, y0 + h + 6.0, "Seven reasons the stream edge has no spine")
    # page 2 (booklet p.09): the whole study area map with its legend and scale bar (cl_spine), the hub cards with
    # their key (cl_hubs), the flood rule (cl_flood), which bank (cl_bank) and v5 the producers' market (cl_market)
    sb = PLAN_BOX.get("spine") or (P2_MAP[0], P2_MAP[1] - P2_MAP_HMAX, P2_MAP[0] + P2_MAP_W, P2_MAP[1])
    crop("cl_spine", 1, 14.0, sb[1] - 11.5, 406.0, sb[3] + 0.5,
         "The streamside spine across the study area, hub by hub", scale_den=PLAN_BOX.get("spine_den"))
    cx_, cy0, cw_all, ch_ = PLAN_BOX.get("cards") or (P2_CARD[0], sb[1] - 12.0 - P2_CARD[2], P2_CARD[1], P2_CARD[2])
    crop("cl_hubs", 1, cx_ - 0.5, cy0 - 7.5, cx_ + cw_all + 0.5, cy0 + ch_ + 0.5,
         "Five bridge places: transit hub, walking hubs with sub-hubs, gateway")
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
    # 25 Oct 10:19 (no double runs): the site board and masterplan ran BEFORE this script and drew the spine from the
    # last city_link_results.json (or their built-in copy). The bank choice comes from survey building counts, so it
    # only changes when the survey changes; if it did change, say so (one more press of the chain fixes the drawings).
    try:
        with open(bg_first([os.path.join(RES_DIR, OUT_JSON), os.path.join(dir_, OUT_JSON)]), "r", encoding="utf-8") as f:
            prev, prev_src = json.load(f).get("spine_banks"), "the last run"
    except Exception:
        prev = dict((pc["id"], bank_of(BANK_VOTE[pc["id"]])[0] if pc.get("side") == "auto" else "over") for pc in SPINE)
        prev_src = "the built-in copy"
    L["bank_note"] = ("" if prev == L["sides"] else
                      "\nWARNING: the spine bank changed from %s (%s -> %s): the site board and masterplan of this run drew "
                      "the old one; press the chain once more." % (prev_src, prev, L["sides"]))
    DROPPED[:] = []
    BM_NOTE[:] = []
    pages = [page_framework(L), page_spine(L)]            # v4 (D8 b): booklet p.08 and p.09
    write_pdf(pages, os.path.join(dir_, OUT_PDF))
    L["layout"] = ["p%d text over text: %s" % (i + 1, ", ".join(pg.clash)) for i, pg in enumerate(pages) if pg.clash] + \
        (["labels with no free place (left off): " + ", ".join(DROPPED)] if DROPPED else [])
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
    bk = "\nlayout: " + ("; ".join(L["layout"]) if L.get("layout") else "no text over text, every label placed")
    bk += "".join("\n" + n_ for n_ in [L.get("fw_note"), L.get("mp_note")] + sorted(set(BM_NOTE)) if n_)   # v4
    bk += "\nopen points (not on the sheet): market edge, decks and stall sizes (masterplan); hub plane-tree irrigation " \
          "from storage (water board); ridership at the bus stops (none found, h03)"
    try:                                           # v1.7: a booklet error never stops the sheets; it goes into the log
        n_ = booklet_export(OUT_DIR)
        bk += ("\nbooklet: " + n_) if n_ else ""
    except Exception as ex_:
        bk += "\nbooklet: ERROR %s: %s" % (type(ex_).__name__, ex_)
    bk += "".join("\n" + t_ for t_ in bg_tidy_output("Bergama_city_link_analysis"))   # 27 Oct: output/ = PDFs only
    t = time.strftime("%H:%M:%S")
    return "%s  %s\n%s  %s\nfigures: %s; %s; %s\ncity link %s, %.1f s%s%s" % (OUT_PDF, t, OUT_JSON, t, L["wb_src"], L["mv_src"], L["ctx_note"], VERSION, time.time() - t0, L.get("bank_note", ""), bk)

#@include ../common/chain_fire.py


#@include ../common/done_text.py


_gh = "ghenv" in globals()
if _gh:
    import scriptcontext as _sc
    try: _ik = ":" + str(ghenv.Component.InstanceGuid)   # 25 Oct 10:29: each component keeps its own log and done
    except Exception: _ik = ""
    _pressed = any(v is True for k, v in list(globals().items()) if not k.startswith("_") and isinstance(v, bool) and k not in ("True", "False", "done")) or \
        any(chain_fire(v, "bergama_city_link_log_chain") for k, v in list(globals().items()) if not k.startswith("_") and k != "done" and isinstance(v, str))
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
