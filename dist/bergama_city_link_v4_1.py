# bergama_city_link_v4.py · Thread 4 of the 22 Oct batch: connection to the city (the streamside spine and what it adds)
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

VERSION = "v4.1"
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
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != {'STREAM_REF': '6462357102432c243b7a34f595c055c7', 'SHOPS_XY': '938d12716e4355018e4de86927b3b4ab', 'LEVELS': '86d74f065d5084a6a48e2a041f6b920b', 'FACTS': 'e402c1370c04b7b8df8f86c4eccbf011'}.get(name):
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


def level_ends(cid):
    """((x1, y1), (x2, y2)): the cut's two ends in survey m, unprimed end first"""
    (a, b) = _lv_ends_row(cid)["ends"]["value"]
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
R28_STUDY_LINE = dict(colour="262626", width_mm=0.45, dash_mm=(3.0, 0.8, 0.4, 0.8))   # dash-dot, print mm

# G7: one strip per map; standard scales only (SCRIPT_STANDARD §8)
R28_SCALES = (200, 250, 500, 1000, 2000, 2500, 5000, 10000, 20000)


def r28_scale(length_m, avail_mm, height_m=0.0, avail_h_mm=1e9):
    """the largest standard scale (smallest denominator) at which length_m x height_m fits avail_mm x avail_h_mm"""
    for d in R28_SCALES:
        if length_m * 1000.0 / d <= avail_mm and height_m * 1000.0 / d <= avail_h_mm:
            return d
    return R28_SCALES[-1]


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
# ---- G4 (MIRAQUA round 28 Oct 2026): labels never overlap each other, symbols or important linework ----------------
# Geometry only (page mm, any y direction): the caller measures its text and draws. Order of tries for each label:
# the spots round its point, then farther out on a thin leader (the leader may not cross a placed label), then the
# same at the smaller sizes in `sizes`; a label still without a spot is dropped if its rank allows it (secondary
# labels), else it gets the nearest free spot anywhere in bounds, on a leader. Boxes are (x0, y0, x1, y1).
def lp_hit(a, b, pad=0.0):
    return a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad


def _lp_seg_box(p, q, b):
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


def lp_seg_cross(p, q, r, s):
    """True when segments p-q and r-s cross (touching at a shared end point does not count)"""
    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    for a in (p, q):
        for b in (r, s):
            if abs(a[0] - b[0]) < 1e-9 and abs(a[1] - b[1]) < 1e-9:
                return False
    d1, d2, d3, d4 = orient(r, s, p), orient(r, s, q), orient(p, q, r), orient(p, q, s)
    return d1 * d2 < 0 and d3 * d4 < 0


class LpSegIndex(object):
    """M2: important linework (polylines, page mm) in buckets, so a label tests only the lines near it; pass it as
    `segs` to label_spot / place_labels_all instead of a list"""
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


def _lp_near(segs, b):
    return segs.near(b) if hasattr(segs, "near") else segs


def lp_leader_end(b, p):
    """the point of box b nearest p (where a leader from p meets the label)"""
    return (min(max(p[0], b[0]), b[2]), min(max(p[1], b[1]), b[3]))


def label_spot(ax, ay, w, h, taken, bounds=None, segs=(), pad=0.5,
               rings=(0.8, 2.5, 5.0, 8.0, 12.0, 17.0, 24.0), n_ang=16, leaders=None, max_leader=None):
    """a free box w x h near (ax, ay): (box, leader) or None. taken: placed boxes and symbol boxes; segs: important
    lines [(p, q)] (or an LpSegIndex) a label may not sit on. leader = True when the box sits off the point (draw a
    thin leader). M2 (30 Oct): leaders = the leaders placed so far [(p, q)]: a new leader may not cross one;
    max_leader (mm): no leader longer than this (G3: short leaders)."""
    import math as _m

    def free(b):
        if bounds and not (bounds[0] <= b[0] and b[2] <= bounds[2] and bounds[1] <= b[1] and b[3] <= bounds[3]):
            return False
        if any(lp_hit(b, t, pad) for t in taken):
            return False
        if leaders and any(_lp_seg_box(p, q, b) for p, q in leaders):
            return False
        return not any(_lp_seg_box(p, q, b) for p, q in _lp_near(segs, b))

    for i_r, d in enumerate(rings):
        for i in range(n_ang):
            a = 2 * _m.pi * (i + 0.5) / n_ang
            cx, cy = ax + _m.cos(a) * (d + w / 2.0), ay + _m.sin(a) * (d + h / 2.0)
            b = (cx - w / 2.0, cy - h / 2.0, cx + w / 2.0, cy + h / 2.0)
            if not free(b):
                continue
            far = i_r >= 2
            if far:
                e = lp_leader_end(b, (ax, ay))
                if max_leader is not None and _m.hypot(e[0] - ax, e[1] - ay) > max_leader:
                    continue
                if any(_lp_seg_box((ax, ay), e, t) for t in taken
                       if not (t[0] <= ax <= t[2] and t[1] <= ay <= t[3])):     # the point's own symbol is passed
                    continue
                if leaders and any(lp_seg_cross((ax, ay), e, p, q) for p, q in leaders):
                    continue
            return b, far
    return None


def place_labels_all(items, taken, bounds=None, segs=(), sizes=(1.0, 0.9), pad=0.5, leaders=None,
                     max_leader=None):
    """items: dicts with x, y (anchor), wh (function size_factor -> (w, h)), rank (0 = must show, 1 = may be
    dropped). Places rank 0 first, then rank 1, each nearest its point. Returns {index: (box, leader, size_factor)}
    for the placed ones; dropped rank-1 labels are left out (the caller may list them in a key). taken grows.
    M2 (30 Oct): leaders (a list, grows) = leaders placed so far: no two leaders cross; max_leader (mm) = the
    longest leader allowed (a rank-0 label that finds no spot within it takes the nearest free spot as before)."""
    import math as _m
    out = {}
    leaders = leaders if leaders is not None else []
    order = sorted(range(len(items)), key=lambda i: items[i].get("rank", 0))
    for i in order:
        it = items[i]
        got = None
        for f in sizes:
            w, h = it["wh"](f)
            got = label_spot(it["x"], it["y"], w, h, taken, bounds, segs, pad, leaders=leaders,
                             max_leader=max_leader)
            if got:
                got = (got[0], got[1], f)
                break
        if got is None and it.get("rank", 0) == 0 and bounds:
            w, h = it["wh"](sizes[-1])
            cands = []
            gx = bounds[0]
            while gx + w <= bounds[2]:
                gy = bounds[1]
                while gy + h <= bounds[3]:
                    cands.append((gx, gy))
                    gy += 2.0
                gx += 2.0
            cands.sort(key=lambda c: (c[0] + w / 2.0 - it["x"]) ** 2 + (c[1] + h / 2.0 - it["y"]) ** 2)
            for gx, gy in cands:
                b = (gx, gy, gx + w, gy + h)
                if not any(lp_hit(b, t, pad) for t in taken) and \
                        not any(_lp_seg_box(p, q, b) for p, q in _lp_near(segs, b)):
                    e = lp_leader_end(b, (it["x"], it["y"]))
                    if any(lp_seg_cross((it["x"], it["y"]), e, p, q) for p, q in leaders):
                        continue
                    got = (b, True, sizes[-1])
                    break
        if got:
            taken.append(got[0])
            if got[1]:
                leaders.append(((it["x"], it["y"]), lp_leader_end(got[0], (it["x"], it["y"]))))
            out[i] = got
    return out


def lp_place(labels, obstacles=(), lines=(), bounds=None, pad=0.6, max_leader=10.0, sizes=(1.0, 0.9, 0.8)):
    """M2, the one call a page makes for its labels (G3): features + labels in, placed labels out, none overlapping
    another label, a symbol (obstacles) or the linework (lines). Page mm, any y direction.
      labels    dicts: x, y = the target point; w, h = the label's box at size 1 (or wh = f -> (w, h)); rank 0 = must
                show, 1 = may be dropped; r = the target's radius in mm (a symbol or a dot; 0 = a point): a leader
                starts on its edge, so it visibly touches the target
      obstacles boxes (x0, y0, x1, y1) of symbols, other drawings, legends (they are not changed)
      lines     polylines (page mm) a label may not sit on (streets, banks, cut lines), or an LpSegIndex
    Returns a list in the labels' order: None (a rank-1 label dropped: list it in the legend) or dict(box, size,
    leader) with leader = None or ((x, y) on the target's edge, (x, y) on the label box): short (<= max_leader
    where any spot allows), never crossing another leader or a label."""
    import math as _m
    segs = lines if hasattr(lines, "near") else LpSegIndex(polylines=lines)
    taken = list(obstacles)
    its = []
    for L in labels:
        if "wh" in L:
            its.append(dict(L))
        else:
            w0, h0 = L["w"], L["h"]
            its.append(dict(L, wh=(lambda f, w0=w0, h0=h0: (w0 * f, h0 * f))))
    leaders = []
    got = place_labels_all(its, taken, bounds, segs, sizes, pad, leaders, max_leader)
    out = []
    for i, L in enumerate(labels):
        g = got.get(i)
        if g is None:
            out.append(None)
            continue
        box, far, f = g
        lead = None
        if far:
            e = lp_leader_end(box, (L["x"], L["y"]))
            r = float(L.get("r", 0.0))
            d = _m.hypot(e[0] - L["x"], e[1] - L["y"])
            s0 = (L["x"] + (e[0] - L["x"]) * r / d, L["y"] + (e[1] - L["y"]) * r / d) if r > 0 and d > r else \
                (L["x"], L["y"])
            lead = (s0, e)
        out.append(dict(box=box, size=f, leader=lead))
    return out


# ------------------------------------------------------------------------------------------- M2 legends and markers
class Legend(object):
    """M2: a legend that can only exist attached to its drawing's frame (G1: next to its drawing, aligned to it, never
    at the page bottom). Numbered markers exist only through marker(), which makes their legend entry at the same
    time (G3: no number without its explanation).
      lg = Legend(frame, side="right")          frame = (x0, y0, x1, y1) of the drawing, page mm
      lg.add("Selinos stream", kind="fill", colour="91ADB4")    kinds: fill, line, dash, dot, icon, hatch, marker
      n = lg.marker("Kermes market")            -> "1": draw n on the map; the legend lists "1  Kermes market"
      L = lg.layout(measure)                    measure(s, size_pt, bold) -> mm
    L = dict(box, rows=[dict(entry, swatch=(x0, y0, x1, y1), text=(x, baseline_y), size_pt)], title=(s, x, y) or None,
    taken=box): the caller draws each swatch by its kind and the text at text; box joins the label obstacles.
    side: "right" / "left" (top-aligned beside the frame, more columns when taller than the frame), "below" /
    "above" (left-aligned to the frame, as many columns as its width holds), "inside_tl" / "inside_tr" /
    "inside_bl" / "inside_br" (in a corner of the frame, on a paper plate: draw L["plate"] first)."""
    SIDES = ("right", "left", "below", "above", "inside_tl", "inside_tr", "inside_bl", "inside_br")

    def __init__(self, frame, side="right", gap=3.0, y_down=True, title=None, style="legend", swatch=(4.0, 2.6),
                 col_gap=4.0):
        if not frame or len(frame) != 4 or frame[2] <= frame[0] or frame[3] <= frame[1]:
            raise ValueError("a legend needs its drawing's frame (x0, y0, x1, y1): it is never placed on its own")
        if side not in self.SIDES:
            raise ValueError("legend side %r: one of %s" % (side, ", ".join(self.SIDES)))
        self.frame, self.side, self.gap, self.y_down, self.title = tuple(frame), side, gap, y_down, title
        self.style, self.swatch, self.col_gap = style, swatch, col_gap
        self.entries, self._n = [], 0

    def add(self, label, kind="fill", **sample):
        """an entry: label + its sample (colour, width, dash, icon name, hatch ...): the entry dict"""
        for e in self.entries:
            if e["label"] == label and e.get("kind") == kind:
                return e
        e = dict(sample, label=label, kind=kind)
        self.entries.append(e)
        return e

    def marker(self, label, prefix="", **sample):
        """a numbered (or prefix-lettered) marker and its legend entry, made together: returns the marker text"""
        for e in self.entries:
            if e.get("kind") == "marker" and e["label"] == label:
                return e["marker"]
        self._n += 1
        m = "%s%d" % (prefix, self._n)
        self.entries.append(dict(sample, label=label, kind="marker", marker=m))
        return m

    def layout(self, measure, size_pt=None, max_h=None):
        """the placed legend (see the class doc)"""
        s0, b0, lead, col = grid_style(self.style) if "grid_style" in globals() else (7.0, False, 4.0, "4A3F35")
        size = size_pt or s0
        lead = lead * size / s0
        sw, sh = self.swatch
        tx = sw + 1.5                                      # text start after the swatch
        ent_w = max([tx + measure(e["label"], size, False) for e in self.entries] or [0.0])
        tw = measure(self.title, size, True) if self.title else 0.0
        f = self.frame
        fw, fh = f[2] - f[0], f[3] - f[1]
        n = len(self.entries)
        th = lead if self.title else 0.0
        if self.side in ("right", "left") or self.side.startswith("inside"):
            avail = (max_h or fh) - th
            nrow = max(1, min(n, int((avail + 1e-6) // lead))) if n else 0
            ncol = max(1, -(-n // nrow)) if nrow else 1
        else:
            ncol = max(1, min(n, int((fw + self.col_gap) // (ent_w + self.col_gap)))) if n else 1
            nrow = -(-n // ncol) if n else 0
        W = max(tw, ncol * ent_w + (ncol - 1) * self.col_gap)
        H = th + nrow * lead
        pad = 1.5 if self.side.startswith("inside") else 0.0
        # the box in y-down terms first (top = the frame's visual top)
        if self.side == "right":
            x0, top = f[2] + self.gap, 0.0
        elif self.side == "left":
            x0, top = f[0] - self.gap - W, 0.0
        elif self.side == "below":
            x0, top = f[0], fh + self.gap
        elif self.side == "above":
            x0, top = f[0], -self.gap - H
        else:
            right = self.side.endswith("r")
            bottom = self.side[-2] == "b"
            x0 = f[2] - pad - W if right else f[0] + pad
            top = fh - pad - H if bottom else pad
        Y = (lambda t: f[1] + t) if self.y_down else (lambda t: f[3] - t)

        def box(x_0, t0, x_1, t1):
            a, b = Y(t0), Y(t1)
            return (x_0, min(a, b), x_1, max(a, b))
        rows = []
        for i, e in enumerate(self.entries):
            c, r = i // nrow, i % nrow
            ex = x0 + c * (ent_w + self.col_gap)
            t = top + th + r * lead
            mid = t + lead * 0.5
            sw_box = box(ex, mid - sh / 2.0, ex + sw, mid + sh / 2.0)
            base = Y(mid + size * GRID_PT_ * 0.35)
            rows.append(dict(e, swatch=sw_box, text=(ex + tx, base), size_pt=size))
        out = dict(box=box(x0 - pad, top - pad, x0 + W + pad, top + H + pad), rows=rows, size_pt=size, colour=col,
                   title=(self.title, x0, Y(top + lead * 0.75)) if self.title else None)
        out["taken"] = out["box"]
        out["plate"] = out["box"] if self.side.startswith("inside") else None
        return out


GRID_PT_ = 25.4 / 72.0                                    # mm per pt (the legend's baseline offset)
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
BASEMAP_FORMAT = 1
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
# topographic mode: contours coloured by height, very faint (palette references 5C7A86 -> 89986A -> 70754C -> 4C2528,
# each mixed 55 % towards white; low = blue-grey, high = dark brown)
BM_HEIGHT_RAMP = ("ADBCC2", "C4CAB1", "B7B9A2", "A39092")
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
}
# M3 layer list -> switches: basemap_layers accepts these names too (buildings, streets, water, topography,
# study_area, names; green, trees, fields as before)
BM_LAYER_ALIAS = dict(water="stream", topography="contours")
BM_STUDY_LINE = dict(colour="262626", width_mm=0.45, dash_mm=(3.0, 0.8, 0.4, 0.8))   # = R28_STUDY_LINE
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
        if not isinstance(d, dict) or d.get("format") != BASEMAP_FORMAT:
            if log is not None:
                log.append(u"WARNING: {} is of another format: the shared basemap is left out (run the site board "
                           u"once).".format(p))
            d = None
        elif log is not None:
            log.append(u"Shared basemap: {} ({}).".format(p, d.get("source", "")))
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


def _bm_items(D, mode, override, box, split_buildings, scale_den=None):
    """basemap_items without the memo"""
    lay = basemap_layers(mode, override)
    L = D["layers"]
    out = []

    def fills(groups, col, alpha=1.0, nonzero=True, chunk=300):
        cur = []
        for g in groups:
            g = [R for R in g if len(R) >= 3]
            if not g or not _bm_hit(g[0], box):
                continue
            if split_buildings:
                out.append(("fill", g, col, alpha, nonzero))
                continue
            cur.extend(g)
            if len(cur) >= chunk:
                out.append(("fill", cur, col, alpha, nonzero))
                cur = []
        if cur:
            out.append(("fill", cur, col, alpha, nonzero))

    def lines(Ps, col, w, dash=None, alpha=1.0):
        for P in Ps:
            if len(P) >= 2 and _bm_hit(P, box):
                out.append(("line", P, col, w, list(dash) if dash else None, alpha))

    # ground: tree cover, fields, parks / grass (satellite first, mapped areas over it)
    if lay["trees"]:
        fills(L["lc"].get("trees", []), BM_COL["tree"])
    if lay["fields"]:
        fills(L["lc"].get("farmland", []) + L["lc"].get("orchard", []), BM_COL["field"])
        fills([z["rings"] for z in L["zones"] if z["kind"] == "agri"], BM_COL["field"])
    if lay["green"]:
        fills([z["rings"] for z in L["zones"] if z["kind"] == "green" and z.get("sub") != "wood"], BM_COL["park"])
    if lay["trees"]:
        fills([z["rings"] for z in L["zones"] if z["kind"] == "green" and z.get("sub") == "wood"], BM_COL["tree"])
    # contours
    if lay["contours"]:
        cs = L["contours"]
        if lay["contours"] == "height":
            zs = [c[1] for c in cs if c[1] is not None]
            z0, z1 = (min(zs), max(zs)) if zs else (0.0, 1.0)
            for major, z, P in cs:
                col = _bm_ramp((z - z0) / max(1.0, z1 - z0)) if z is not None else BM_COL["contour"]
                lines([P], col, BM_LW["contour_topo"][1 if major else 0])
        else:
            for major, z, P in cs:
                lines([P], BM_COL["contour"], BM_LW["contour"][1 if major else 0])
    # streets
    st = lay["streets"]
    if st is True or st == "faint":
        faint = st == "faint"
        fills(L["street_areas"], BM_FAINT["road"] if faint else BM_COL["road"], nonzero=False)
        for cl, P in L["streets_out"]:                    # beyond the frame: OpenStreetMap centrelines
            lines([P], BM_FAINT["road_line"] if faint else BM_COL["road"], BM_LW[cl] * (1.6 if cl != "path" else 1.0))
        if not faint:
            lines(L["street_edges"], BM_COL["road_edge"], BM_LW["road_edge"])
    elif st:
        for cl, P in L["streets_in"] + L["streets_out"]:
            if cl in st:
                lines([P], BM_FAINT["road_line"] if cl != "main" else BM_COL["road_edge"], BM_LW[cl])
    # the stream: ONE drawing (the site board's water and its edge inside the frame, OpenStreetMap's course beyond).
    # M3 (30 Oct): drawn by M5 (common/water.py water_plan, page mm) when the script includes it: one "water" item
    # that basemap_draw hands to water_plan after the map's T (else the plain fill and edge, as before)
    if lay["stream"]:
        if callable(globals().get("water_plan")):
            ws = [g for g in L["water"] if g and len(g[0]) >= 3 and _bm_hit(g[0], box)]
            if ws:
                out.append(("water", ws, [P for P in L["water_edge"] if len(P) >= 2 and _bm_hit(P, box)], 1.0))
        else:
            fills(L["water"], BM_COL["water"], nonzero=False)
            lines(L["water_edge"], BM_COL["water_edge"], BM_LW["water_edge"])
        if st is True or st == "faint":
            fills([[R] for R in L["decks"]], BM_FAINT["road"] if st == "faint" else BM_COL["road"])
        for P in L["covered"]:
            lines([P], BM_COL["water_edge"], BM_LW["covered"], BM_COVERED_DASH)
        fills(L["water_out"], BM_COL["water"], nonzero=False)
        for kind, P in L["waterways_out"]:
            lines([P], BM_COL["water"], BM_LW["river_osm" if kind == "river" else "stream_osm"])
    # buildings
    bl = lay["buildings"]
    if bl in ("plan", "plan_faint"):                        # M11: outline per block + roof reading, no stripes
        pf = globals().get("bld_plan_items")
        if callable(pf):
            faint = bl == "plan_faint"
            blocks = L.get("blocks")
            out.extend(pf(L["buildings"], blocks=blocks, scale_den=scale_den or 5000.0, box=box,
                          fill=BM_FAINT["bld_veryfaint"] if faint else None,
                          edge=BM_FAINT["road_line"] if faint else None,
                          roof_col=BM_FAINT["bld"] if faint else None,
                          her_fill=BM_COL["her"] if not faint else "F1E6E5",
                          her_edge=BM_COL["her_edge"] if not faint else "CDAAAA"))
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
                          BM_LW["her_edge"] if b.get("her") else BM_LW["osm_edge"])
        else:
            fills([b["rings"] for b in L["buildings"]],
                  BM_FAINT["bld_veryfaint"] if bl == "veryfaint" else BM_FAINT["bld"])
    if lay["stream"] and (st is True or bl is True or bl == "plan"):
        lines(L["bridges"], BM_COL["ink"], BM_LW["bridge"])
    # M3 (30 Oct): the study area (one outline, one style, on top of the base) and the place names
    if lay.get("study_area"):
        for it in basemap_study_items(D):
            if _bm_hit(it[1], box):
                out.append(it)
    if lay.get("names"):
        for n, p in basemap_names(box, D):
            out.append(("text", n, p, BM_NAME_MM, BM_COL["ink"], False, "MC"))
    return out


def basemap_draw(items, T, fill_fn, line_fn, text_fn=None, water_opts=None):
    """draws items through the caller's page: T(p) survey m -> page point; fill_fn(rings, hex, alpha, nonzero);
    line_fn(pts, hex, width_mm, dash_mm, alpha); text_fn(s, (x, y), size_mm, hex, bold, align) (texts are left out
    without it). Returns the number of items drawn. M3 (30 Oct): a "water" item (the stream, when the script includes
    M5 common/water.py) is drawn by water_plan(ring in page mm, k, **water_opts) through the same three functions
    (k = page mm per survey m, from T); if M5 fails, the plain fill and bank line (a WARNING in basemap_warnings())."""
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
            p0 = it[1][0][0][0], it[1][0][0][1]
            a, b = T(p0), T((p0[0] + 100.0, p0[1]))
            k = _m.hypot(b[0] - a[0], b[1] - a[1]) / 100.0
            try:
                wp = globals()["water_plan"]                # M5 (common/water.py), present: _bm_items checked it
                for g in it[1]:
                    wl = wp([T(p) for p in g[0]], k, **(water_opts or {}))
                    for s_ in wl.shapes():
                        if s_[0] == "poly" and len(s_[1]) >= 3:
                            al = s_[5] if len(s_) > 5 and s_[5] is not None else 1.0
                            if s_[2]:
                                fill_fn([list(s_[1])], s_[2], al, True)
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


def basemap_cut_items(cuts, scale_den, frame=None, inset_mm=3.0, tri_mm=2.6, text_mm=2.4, col=None, D=None):
    """the section lines of ONE page's key map (D11: only that page's cuts) as items, kept inside the frame: a line
    per cut, an architectural triangle at each end pointing the way the section looks, the end's name beyond it.
    cuts = [(end1, end2, (name1, name2)[, look])], survey m, end1 = the section's left end; look = +1 (default:
    the viewer stands so end1 is on the left, end2 on the right) or -1 (the other way). scale_den: the key map's
    scale (1:scale_den) for the mm sizes; frame: the polygon to stay in (default the analysis frame), the ends are
    pulled in by inset_mm so the markers and names stay inside it. With the level module, basemap_cut_ids() makes
    cuts from cut ids."""
    frame = frame or basemap_frame(D)
    col = col or BM_COL["cut"]
    m = scale_den / 1000.0                               # survey m per print mm
    out = []
    for c in cuts:
        a, b, names = c[0], c[1], c[2]
        look = c[3] if len(c) > 3 else 1
        L0 = _bm_math.hypot(b[0] - a[0], b[1] - a[1])
        if L0 < 1e-6:
            continue
        ux, uy = (b[0] - a[0]) / L0, (b[1] - a[1]) / L0
        if frame:
            ab = _bm_clip_convex(a, b, frame)
            if ab is None:
                continue
            a, b = ab
        pull = inset_mm * m + tri_mm * m                    # room for the marker and the name inside the frame
        L = _bm_math.hypot(b[0] - a[0], b[1] - a[1])
        if L <= 2.0 * pull:
            continue
        a = (a[0] + ux * pull, a[1] + uy * pull)
        b = (b[0] - ux * pull, b[1] - uy * pull)
        fx, fy = -uy * look, ux * look                      # the way the section looks (left normal of end1 -> end2)
        out.append(("line", [a, b], col, BM_LW["cut"], [3.0, 0.8], 1.0))
        h = tri_mm * m
        for p, nm, sgn in ((a, names[0], -1.0), (b, names[1], 1.0)):
            out.append(("fill", [[(p[0] - ux * h * 0.5, p[1] - uy * h * 0.5),     # the triangle stands on the
                                  (p[0] + ux * h * 0.5, p[1] + uy * h * 0.5),     # line's end, its apex the way
                                  (p[0] + fx * h, p[1] + fy * h)]], col, 1.0, True))   # the section looks
            out.append(("line", [(p[0] - ux * h * 0.6, p[1] - uy * h * 0.6), (p[0] + ux * h * 0.6, p[1] + uy * h * 0.6)],
                        col, BM_LW["cut"] * 1.6, None, 1.0))
            q = (p[0] + ux * sgn * (h * 0.6 + text_mm * m * 0.9) - fx * text_mm * m * 0.2,
                 p[1] + uy * sgn * (h * 0.6 + text_mm * m * 0.9) - fy * text_mm * m * 0.2)
            out.append(("text", nm, q, text_mm, col, True, "MC"))
    return out


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


# ------------------------------------------------------------------------------------------- M4 key map
def keymap_items(ids=(), scale_den=10000.0, box=None, zooms=None, mode="key", override=None, looks=None, D=None,
                 margin=0.06, text_mm=2.4, col=None, log=None, page=None):
    """M4: the key map of a page = a small M3 extract that ALWAYS shows the study-area outline and EVERY cut or zoom
    id passed, each labelled. ids: cut ids of the cut registry (common/levels.py, level_ends / level_end_labels) or
    zoom ids; a zoom id is looked up in zooms {id: polygon survey m} first, then in the registry's level_window(id)
    when the level module has it. box (survey m) defaults to the study area + every cut and zoom, widened by margin.
    page = a booklet page number: with no ids, every cut the registry draws on that page (level_registry_all).
    Each cut is labelled with its registry name (level_name: F1 -> W1) where its end names do not already say it.
    Returns dict(items (survey m; draw with basemap_draw and the key map's T, clipped to box), box, drawn=[ids],
    missing=[ids]); a missing id is logged (WARNING), never left out silently."""
    import math as _m
    if not ids and page is not None and callable(globals().get("level_registry_all")):
        ids = [e["id"] for e in level_registry_all(str(page))]
    D = D if D is not None else basemap_load()
    col = col or BM_COL["cut"]
    log = log if log is not None else _BM_WARN
    cuts, wins, drawn, missing = [], [], [], []
    seen_ends = set()
    win_fn = globals().get("level_window")
    for cid in ids:
        if zooms and cid in zooms:
            wins.append((cid, [tuple(p) for p in zooms[cid]]))
            drawn.append(cid)
            continue
        try:
            c = basemap_cut_ids([cid], looks)[0]
            ek = (round(c[0][0], 1), round(c[0][1], 1), round(c[1][0], 1), round(c[1][1], 1))
            if ek not in seen_ends:                       # the crossings of one cut (S5-1 .. S5-3) share one line
                seen_ends.add(ek)
                cuts.append((cid, c))
            drawn.append(cid)
            continue
        except Exception:
            pass
        try:
            if callable(win_fn):
                w = win_fn(cid)
                if w:
                    wins.append((cid, [tuple(p) for p in w]))
                    drawn.append(cid)
                    continue
        except Exception:
            pass
        missing.append(cid)
        log.append(u"WARNING: key map: '{}' is neither a cut of the registry nor a zoom passed in: not drawn.".format(cid))
    study = basemap_study(D)
    if box is None:
        pts = [p for R in study for p in R] + [p for _, c in cuts for p in c[:2]] + [p for _, w in wins for p in w]
        if not pts:
            ext = basemap_extent(D) or []
            pts = list(ext)
        if pts:
            x0, y0, x1, y1 = _bm_bb(pts)
            d = margin * max(x1 - x0, y1 - y0, 1.0)
            box = (x0 - d, y0 - d, x1 + d, y1 + d)
    items = basemap_items(mode, override, box=box, D=D, scale_den=scale_den) if D else []
    if not (D and basemap_layers(mode, override).get("study_area")):
        items += basemap_study_items(D)                  # the outline is always there, whatever the layers
    if box is not None:
        frame = [(box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])]
    else:
        frame = None
    m = scale_den / 1000.0
    for cid, c in cuts:
        its = basemap_cut_items([c], scale_den, frame=frame, text_mm=text_mm, col=col, D=D)
        items += its
        nm_fn = globals().get("level_name")
        try:
            name = nm_fn(cid) if callable(nm_fn) else cid
        except Exception:
            name = cid
        name = str(name).split("-")[0]                    # a crossing row (S5-2) is labelled by its cut (S5)
        if name not in c[2][0] and name not in c[2][1]:   # end names that do not say the id ("SW" / "NE"): the id too
            a, b = c[0], c[1]
            L0 = _m.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
            nx, ny = -(b[1] - a[1]) / L0, (b[0] - a[0]) / L0
            q = ((a[0] + b[0]) / 2.0 + nx * text_mm * m * 1.2, (a[1] + b[1]) / 2.0 + ny * text_mm * m * 1.2)
            items.append(("text", name, q, text_mm, col, True, "MC"))
    for cid, w in wins:
        items.append(("line", list(w) + [w[0]], col, BM_LW["cut"], None, 1.0))
        x0, y0, x1, y1 = _bm_bb(w)
        items.append(("text", cid, (x0 + text_mm * m * 0.9, y1 + text_mm * m * 0.8), text_mm, col, True, "MC"))
    return dict(items=items, box=box, drawn=drawn, missing=missing)


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
                 bridges=[], blocks=[], study=[], names=[])
        mains = set(globals().get("MAIN_ROADS") or ("motorway", "trunk", "primary", "secondary", "tertiary"))
        peds = set(globals().get("PED") or ("footway", "path", "pedestrian", "steps", "cycleway", "bridleway",
                                             "track", "corridor"))
        skip = set(globals().get("SKIP_HW") or ("proposed", "construction", "platform", "bus_stop", "elevator"))
        ccls = lambda hw: "path" if hw in peds else ("main" if hw in mains else "lane")
        # ---- inside the frame: the site board's layers
        lcf = globals().get("r28e_lc")
        for key in ("trees", "farmland", "orchard"):
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
                    z = round(zs[len(zs) // 2] / 5.0) * 5.0
                except Exception:
                    z = None
            L["contours"].append([bool(major), z, _bm_r(P)])
        for rg in getattr(S, "road_net", None) or []:
            L["street_areas"].append([_bm_r(rg["P"])] + [_bm_r(H) for H in rg.get("H", [])])
        L["street_edges"] = [_bm_r(P) for P in getattr(S, "road_lines_net", None) or []] + \
            [_bm_r(r_["P"]) for r_ in S.roads if not r_.get("w")]
        L["streets_in"] = [[ccls((r_.get("tags") or {}).get("highway")), _bm_r(r_["P"])] for r_ in S.roads] + \
            [["path", _bm_r(r_["P"])] for r_ in getattr(S, "paths", None) or []]
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
                                           h=round(float(u.get("h") or 0.0), 2), floors=int(u.get("floors") or 0)))
                if her and (u.get("name") or "").strip() and in_frame_name(u):
                    L["names"].append([u["name"].strip(), [round(u["cx"], 1), round(u["cy"], 1)]])
        blocks = getattr(S, "blocks", None)
        if blocks is None and callable(globals().get("bld_blocks")):
            blocks = bld_blocks(S.bld)
        for bk in blocks or []:
            mem = [idx_of[i] for i in bk.get("units", []) if i in idx_of]
            L["blocks"].append(dict(rings=[_bm_r(bk["outer"])] + [_bm_r(H) for H in bk.get("holes") or []],
                                    her=bool(mem) and all(L["buildings"][i]["her"] for i in mem)))
        L["study"] = [_bm_r(P) for P in (getattr(S, "r28_study", None) or globals().get("R28_STUDY_COPY") or [])]
        L["names"] = [[n, [round(p[0], 1), round(p[1], 1)]] for n, p in BASEMAP_REACH] + L["names"]
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
                    L["streets_out"].extend([ccls(hw), run] for run in outside_line(P))
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


def grid_page_counter(n, total):
    """the page counter, computed: "07/23" (n of total pages)"""
    return "%02d/%02d" % (int(n), int(total))


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
                   roof_col=None, her_fill=None, her_edge=None, alpha=1.0, outline=True, hatch_mm=1.2):
    """G7 plan: buildings as items (survey m): a light fill per building, the roof reading (ridge + hips; roof="hatch"
    adds fall lines every hatch_mm on the page; "none" leaves it out) where the building is at least BLD_MIN_ROOF_MM
    wide at 1:scale_den, and ONE outline per block (blocks: bld_blocks(units), made when not given): no line between
    buildings that share a wall. Heritage units (her=True) in their own tone. box (x0, y0, x1, y1): only what touches
    it."""
    fill, edge = fill or BLD_COL["fill"], edge or BLD_COL["edge"]
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
                out.append(("line", list(R) + [R[0]], col, BLD_LW["block"], None, alpha))
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
    horizontal light direction (lit walls and roof planes lighter). Pitched units get a hipped roof on their
    minimum rectangle when the footprint fills >= 80 % of it, else a flat top; flat units a flat top."""
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
    for _, u, P, cx, cy in jobs:
        z0 = ground(cx, cy) if ground else float(u.get("z0") or 0.0)
        h = _bld_h(u)
        zt = z0 + h
        walls = []
        n = len(P)
        for i in range(n):
            p, q = P[i], P[(i + 1) % n]
            ex, ey = q[0] - p[0], q[1] - p[1]
            L = _m.hypot(ex, ey)
            if L < 1e-6:
                continue
            nx, ny = ey / L, -ex / L                     # outward (ccw outline)
            if nx * vx + ny * vy <= 1e-6:
                continue
            lit = nx * sx + ny * sy
            col = _bld_mix(C["wall_shade"], C["wall_lit"], max(0.0, min(1.0, 0.5 + 0.5 * lit)))
            mx, my = (p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0
            walls.append((mx * vx + my * vy, [proj(p[0], p[1], z0), proj(q[0], q[1], z0), proj(q[0], q[1], zt),
                                              proj(p[0], p[1], zt)], col))
        walls.sort(key=lambda w: w[0])
        for _, ring, col in walls:
            out.append(("fill", [ring], col, 1.0, True))
            out.append(("line", ring + ring[:1], C["axo_line"], lw, None, 1.0))
        r = bld_rect(P)
        pitched = roofs and _bld_roof_mode(u, "ridge") != "flat" and r is not None and \
            abs(_bld_area(P)) >= 0.8 * r[4] * r[5]
        if pitched:
            rcx, rcy, ux, uy, L, W = r
            wx, wy = -uy, ux
            rise = _m.tan(_m.radians(pitch)) * W / 2.0
            hh = (L - W) / 2.0
            c4 = [(rcx + ux * su * L / 2 + wx * sv * W / 2, rcy + uy * su * L / 2 + wy * sv * W / 2)
                  for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            r1, r2 = (rcx - ux * hh, rcy - uy * hh), (rcx + ux * hh, rcy + uy * hh)
            planes = [([c4[0], c4[1], r2, r1], (-wx, -wy)), ([c4[2], c4[3], r1, r2], (wx, wy)),
                      ([c4[3], c4[0], r1], (-ux, -uy)), ([c4[1], c4[2], r2], (ux, uy))]
            rp = []
            for pl, (nx, ny) in planes:
                pts3 = [(x, y, zt if (x, y) in c4 else zt + rise) for x, y in pl]
                mx = sum(p[0] for p in pl) / len(pl)
                my = sum(p[1] for p in pl) / len(pl)
                lit = nx * sx + ny * sy
                col = _bld_mix(C["roof_shade"], C["roof_lit"], max(0.0, min(1.0, 0.5 + 0.5 * lit)))
                rp.append((mx * vx + my * vy, [proj(*p3) for p3 in pts3], col))
            rp.sort(key=lambda w: w[0])
            for _, ring, col in rp:
                out.append(("fill", [ring], col, 1.0, True))
                out.append(("line", ring + ring[:1], C["axo_line"], lw, None, 1.0))
        else:
            top = [proj(p[0], p[1], zt) for p in P]
            hs = [[proj(p[0], p[1], zt) for p in H] for H in H_ if len(H) >= 3 and _bld_pip(H[0][0], H[0][1], P)]
            out.append(("fill", [top] + hs, C["roof_lit"], 1.0, False))
            out.append(("line", top + top[:1], C["axo_line"], lw, None, 1.0))
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


def _ico_colours(name, ink, accent, second):
    """Token -> hex for one icon: ink, c1 (accent overrides), c2 (second overrides; None = c1 mixed to paper)."""
    d1, d2 = ICO_COL[name]
    c1 = accent or ICO_PAL[d1]
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

# ------------------------------------------------------------------ minimal vector PDF (mm units, Helvetica, whole strings)
_HW = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278] + [556] * 10 + \
      [278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
       667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556, 333, 556, 556, 500, 556, 556,
       278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334,
       260, 334, 584]

_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}   # Turkish letters in unused WinAnsi slots
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"

def text_w(s, size, bold=False):
    w = sum(_HW[ord(ch) - 32] if 32 <= ord(ch) < 127 else 556 for ch in s)
    return w / 1000.0 * size * (1.06 if bold else 1.0) * 0.3528      # size in pt -> width in mm


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


def _pf_metrics(data):
    """widths of codes 32-255 (1000 units per em) and the descriptor numbers, read from the TrueType tables"""
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
                script="bergama_city_link_v4.py", version=VERSION, run_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                spine=SPINE, functions=[dict([(k, f.get(k)) for k in ("n", "name", "where", "xy", "stage", "who", "grows", "ch", "bank")] +
                                             [("hub", "sub-hubs" if f["n"] == 8 else hub_of.get(f["n"]))])
                                        for f in FUNCS + [EVENTS]],
                chainage=CH, main_spine=MAIN_SPINE, shops=shop_figures(), hubs=hubs, main_transit_hub=MAIN_TRANSIT_HUB,
                hubs_source=SRC_HUBS + "; " + SRC_BUS,
                note="survey coordinates (m); spine offsets are schematic for the movement network")

# ------------------------------------------------------------------ v1.8: A3 booklet = crops of this sheet (booklet/CROP_SPEC.md)
# ---- A3 booklet assets (SCRIPT_STANDARD §8; booklet/ASSET_SPEC.md) ----
# Each booklet frame = one text-free vector PDF drawn at the frame's size + its words as labels in blocks.json.
# The assembler (bergama_booklet) sets every label as live text in the booklet font, never below 7 pt.
BK_MIN_PT = 7.5                              # labels and captions on the booklet (brief: 7-8 pt, minimum 7)
BK_CAPTION_MM = 5.0                          # caption line under every drawing frame


def bk_frame(key, w_default, h_default):
    """(w, h) mm a drawing for asset key "<folder>/<block>" is drawn at: the assembler's booklet_slots.json if it has
    run once, else the defaults given (the plan's frame size). h excludes the caption line."""
    try:
        import json as _j
        with open(bg_first([os.path.join(bg_booklet(""), "booklet_slots.json"),        # 27 Oct: cached/booklet/
                            os.path.join(bg_output("bergama_booklet"), "booklet_slots.json")]), encoding="utf-8") as f:
            s = _j.load(f)[key]
        return float(s["w_mm"]), float(s["h_mm"]) - BK_CAPTION_MM
    except Exception:
        return float(w_default), float(h_default) - BK_CAPTION_MM


def bk_take_text(items, H):
    """Page items (poly/line/circle/text tuples, y up from the bottom, mm) -> (items without text, labels).
    Labels: x, y in mm from the top-left (y to the baseline), size raised to BK_MIN_PT, colour hex."""
    keep, labels = [], []
    for it in items:
        if it[0] != "text":
            keep.append(it)
            continue
        _, s, x, y, size, color, bold, align = it[:8]
        labels.append({"x": round(x, 2), "y": round(H - y, 2), "text": s, "size": max(float(size), BK_MIN_PT),
                       "bold": bool(bold), "anchor": align or "L", "colour": color if isinstance(color, str) else "4A3F35"})
    return keep, labels


class BkBlocks(object):
    """Collects one script's booklet blocks and writes cached/booklet/<folder>/blocks.json (27 Oct, Aras: output/ holds
    final PDFs only; was output/<folder>/booklet/). out_dir = the script's output folder; its name is the folder key."""
    def __init__(self, out_dir, script, version):
        self.dir = bg_booklet(os.path.basename(os.path.normpath(out_dir)))
        os.makedirs(self.dir, exist_ok=True)
        self.d = {"script": script, "version": version, "sources": {}, "blocks": {}}

    def path(self, name):
        return os.path.join(self.dir, name)

    def source(self, key, text, url):
        """A public source: used in any text as {src:key}; numbered once for the whole booklet."""
        self.d["sources"][key] = {"text": text, "url": url}

    def drawing(self, bid, pdf_name, labels, caption="", scale_den=None, legend=None):
        self.d["blocks"][bid] = {"type": "drawing", "pdf": pdf_name, "page": 0, "labels": labels, "caption": caption,
                                 "scale_den": scale_den, "legend": legend or []}

    def crop(self, bid, pdf_name, rect_mm, caption="", scale_den=None, legend=None, page=0, drop=None):
        """A booklet drawing taken from this script's own sheet (Aras 25 Oct 21:47: the booklet shows the sheet's
        drawing, re-laid): pdf_name = the sheet PDF in this script's output folder, rect_mm = (x0, y0, x1, y1) of the
        panel in mm from the sheet page's top-left (y down), scale_den = the sheet's scale at 1:1 print (None if not to
        scale). The assembler scales the crop to its frame and resets the sheet's words inside it as live labels;
        drop = regexes of sheet texts not to carry."""
        self.d["blocks"][bid] = {"type": "crop", "pdf": pdf_name, "page": page,
                                 "rect_mm": [round(float(v), 2) for v in rect_mm], "caption": caption,
                                 "scale_den": scale_den, "legend": legend or [], "drop": drop or []}

    def tiles(self, bid, tiles):
        self.d["blocks"][bid] = {"type": "tiles", "tiles": tiles}

    def text(self, bid, heading="", body="", bullets=None):
        self.d["blocks"][bid] = {"type": "text", "heading": heading, "body": body, "bullets": bullets or []}

    def save(self):
        import json as _j
        p = os.path.join(self.dir, "blocks.json")
        with open(p, "w", encoding="utf-8") as f:
            _j.dump(self.d, f, ensure_ascii=False, indent=1)
        return p

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

def chain_fire(v, key):
    """25 Oct 10:20 (one-click chain): the previous script's done output is a text "done HH:MM:SS.ss ..." that stays
    after the Button is released; each NEW text fires this script once (the Button still works as before)."""
    if isinstance(v, (list, tuple)):
        v = next((x for x in v if x is not None), None)
    s = str(v) if v is not None else ""
    if not s.startswith("done "):
        return False
    try:
        import scriptcontext as _scx
        try:
            key = key + ":" + str(ghenv.Component.InstanceGuid)              # noqa: F821
        except Exception:
            pass
        if _scx.sticky.get(key) == s:
            return False
        _scx.sticky[key] = s
        return True
    except Exception:
        return False


def done_text(ran, ok, secs):
    """The done output: kept until the next run (this Rhino session)."""
    return ("done " if ok else "ERROR ") + time.strftime("%H:%M:%S") + ".%02d" % int((time.time() % 1) * 100) + \
        " · %.0f s" % secs if ran else None


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
