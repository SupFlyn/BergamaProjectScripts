# -*- coding: utf-8 -*-
"""BERGAMA WATER BOARD v4 (2026-10-28; first written as v1.8, 2026-10-25; v1.8 VISUAL FIRST, Aras 17:00/17:05: sentences become pictogram chips, big-figure
callouts on the charts, a visual species card grid and season matrix; sources as [n] in the footer key; layout and look of v1.3/v1.6 kept): the water of Group 6's project on one A0 board: how much, when, how high,
how it is cleaned, held and released.

HOW TO RUN
  Rhino 8 > Grasshopper > a "Python 3 Script" component. Paste this file in, wire a plain Button into any input
  (build, run, go ...). One press writes the board (option A, storage as cubes); a second press writes it again. Nothing
  is baked into Rhino. The log is kept after the Button is released (output log; pdf = the paths) and written to
  Downloads/Bergama/logs/bergama_water_board_log.txt (v1.3).
    Bergama_water_board_v6_A_cubes.pdf      option A (organic forms only where the project meets the water)
  The plant photos are fetched once from Wikipedia / Wikimedia Commons (open licences only) into
  Downloads/Bergama/cached/plant_photos/ (v3: shared with the agriculture alternatives) and read from there afterwards;
  offline, each photo is a labelled empty frame and the board is written as usual.
  The board is one A0 landscape page (1189 x 841 mm), vector (the plant photos excepted), whole-string Arial text (v4: embedded).
  Open Bergama_Altlik.3dm (25 Oct; the course survey works the same) first if you have it: the S4 detail then cuts its ground again
  from the survey heights; without it the embedded survey profile is used (the log says which).

WHAT IT MERGES (Thread 1 of the 22 Oct batch, plan batch_2026-10-22/thread1_merge_audit/MERGE_PLAN.md; Aras's
answers 24 Oct 05:48-05:52). Every drawing below keeps all the content of its parts; the old scripts are retired.
  title + chain   "who does what": ARAS -> BEGÜM K4 -> BEGÜM K5 -> NİL, one way, with arrows (Q6). From water loop v2
                  (stage texts, routes, key plan, close-ups) and pr1 v3.1 form plans; elements numbered 1-11 as the
                  old cards, and the same numbers on every drawing.
  W1 the year of the water: rain and open-water evaporation (water case panel 2), river flow and rain on the study
                  areas (panel 3), mean water depth by month (rain_river A3_year charts), Sentinel-2 greenness with
                  leaf-out and leaf-fall (plant analysis panel 7), season brackets (water loop "year of the loop").
  W2 river height: five surveyed channel cuts (v1.1; flat downstream end large, DSİ's planned channel beside it at
                  the same scale, the other four at one shared scale) with the crossed roads and cards 8-9; the S4 detail of the flat downstream end (detail section v2,
                  1:75 sheet per season) at 1:200 with every season's water as a level line, and the season table.
  W3 concept sections: pr1 v3.1 idea sketches (upstream entry, K4) with the elements numbered (cards 2-9) and
                  the planting bands by days under water (plant analysis panel 8).
  W4 storage: two alternatives (Q5): the cubes (water loop v2) or the to-scale chart (water case panel 4).
  W6 cleaning: water case panels 1 and 5 (sewage, greywater gaps, reed-bed removal, coliforms).
  W7 where the clean water goes: water case panel 6, card 11 and the farmland pictogram (water loop).
  decision row: "What the figures support" (water case).
  Not repeated: rain and river totals print once (W1); species once (W3); Q100 / Q500 once per cut (W2).

DATA RULES
  Every figure is Group 6's, copied with its source from the scripts above (their sources: case.md, research/
  rain_river_levels README and tables, research/water_data README, DATA_REGISTER, CONCEPT_RECORD v2.4, the plant
  data pack bergama_plant_data_v1.json) and printed with its label: measured, published, calculated or design value.
  Settled 24 Oct (CONFLICTS.md, this account wins): one-way loop, nothing pumped back; a continuous regulated strip
  (no weir pools); the strip's own storage 26,675 / at least 83,060 m³ (its losses only: its outflow goes on to the
  farms, water balance v2); Q500 from DSİ.

NEW IN v5 (revision 29 Oct 2026, step T3b; a feature change, so the next whole number):
  * p.12 (pages/p12_system.py): one axonometric water map (collect, clean, hold, give back, to the farms) with volumes
    read live from the water balance, a round plan zoom of the upstream entry, the remaining analysis beside it.
  * pp.14-15 (pages/p14_15_s4.py): the S4 pair rebuilt on the level module (bed +42.48), S4-only key maps, seasonal
    plants, space types, recorded fauna, one rectangular view per season, water and rain as graphics.
  * Core: only public sources are printed (public_src() in cite()); no status words; the shared modules (levels,
    basemap, plants, icons) included; build_board calls the page functions p12_page, p14_page, p15_page.
v6.1 (bugfix, revision 29 Oct T5 fix pass, Aras 22:08): p.12's reed pilot figure cites its public paper (Korkusuz et
  al. 2004, Turk. J. Eng. Env. Sci. 28; was "published" + a register code, which left it without a source); p.12 prints
  the HOLD volume and the strip's summer volume only from the live water balance results (WB_LIVE), never from the
  built-in default, and logs it; p.18 aquifer line without "ratio calculated". Output: Bergama_water_board_v6_1_A_cubes.pdf.
v6 (revision 29 Oct, T4a, a feature change): p.17 planting and water on two pages (pages/p17_planting.py: p17_page =
  wb_plants, the plans + water spaces + catalogue; p17b_page = wb_plants_b, the F1-F4 sections at 1:500, in row 3 beside
  the concept sections); p.18 icons and olive block (pages/p18_farms.py); D6 in data/SPECIES.py and PLANT_SITES; the
  old p.17 panel constants removed.
  Output: Bergama_water_board_v6_A_cubes.pdf.

NEW IN v4 (MIRAQUA 28 Oct, booklet revision v4; a feature change, so the next whole number):
  * p.14 seasons: one scale, 1:500, with a scale bar; a THE SEASON column (climate measured, water balance, plants
    designed) and FEEL · HEAR · TOUCH with bold keywords; compact season tags; the panel fits under the S4 key map.
  * p.15 north-east bank: THROUGH THE YEAR under the cut: a lane for each band of the bank, the users as see-through
    bands (how busy: design assumption), the season water and the winter flood reach, free time, the in-bed sub-hub
    and the Kermes week; the four season strips go; the summer strip reads 400 cm × 0.30 m.
  * pp.14-15: the people are common/figures.py silhouettes, the Kermes stall in thin lines.
  * p.16 plants: the photos from common/plant_photos (an empty frame says why); the keywords of where and why bold.
  * K4 cut: "right bank 2.1 m (survey, before the DSİ walls)"; the DSİ cut cites SYGM 2019 Yönetici Özeti p.75,
    measure 155 (bank depth research 28 Oct §4).
  * Decision panel: "THEN THE FARMS". Footer: version and palette only. Bold keywords in every context line.
  * Sources: no [n] for our own research notes on pp.14-16 (the activities read as design). Arial embedded (G3).
  Output: Bergama_water_board_v4_A_cubes.pdf.

NEW IN v3.2 (bugfix, Aras 27 Oct, booklet Prompt 8 "final fault check"; pages as booklet v17 numbers them):
  * p.13 "Collect, clean, hold": "design storage" sits over its own cube (it lay on the first-fill cube); the storage
    figures' rows share the column's spare height and the cubes sit level with the middle of the list, so the column
    ends level with the cleaning tiles (about 70 mm were empty under the cubes, P4's open item); same scale, same words.
  * p.16 north-east bank: the survey marks are left out, as on the season rows (their 4.5 pt labels lay on each other).
  * p.17 plants: the band labels over the S4 cut no longer lie on each other (French lavender / tamarisk); the WHY HERE
    row "odour: no plant measured" goes (no data: the rule the odour tile went by in v2); the day classes are no longer
    also sent as the page's footer legend (the WHY HERE key on the panel shows them).
  * p.18 what the figures support: "10^2-10^5 CFU/100 ml" reads "100-100,000 CFU/100 ml", as the coliform tile does.
NEW IN v3.1 (bugfix, Aras 27 Oct 17:35, booklet Prompt 6 "water, part 3", p.23: "the Total use 198.01 hm³ a year value
is missing on its bar, and hm³ renders as hm"): each aquifer bar carries its value on the bar (white, at its end; outside
only when it does not fit); m² and m³ are written as a raised small 2 or 3 (0.6 x the size: the same width as the ²/³
glyph, so nothing moves), which every PDF viewer shows; the ²/³ glyph of the unembedded Helvetica was dropped in some.
NEW IN v3 (Aras 27 Oct 17:34, booklet Prompt 5 "water, part 2"; a feature change, so the next whole number):
  * p.20 four seasons (wb_s4_seasons): one row a season between divider lines, the S4 cut at 1:250 standing on its
    row's divider, all four on one x so the bank lines up, between the season column and FEEL · HEAR · TOUCH (which
    takes the width left); the panel moves to the wider middle cell and fills it (the A3 page's width); no scale bar.
  * p.21 north-east bank (wb_s4_ne): drawn at 1:250 itself (it was drawn at 1:200 and shrunk to about 1:250, so its
    words printed under 7.5 pt); the scale is said once, in the caption; the left cell of row 2. The chain stays in cm
    (300 + 400 + 300 + 400 + 450 + 1100 + 255 + 2595 + 400 = 6200 cm = 62.0 m, s 652 to 590 on S4).
  * p.22 plants (wb_plants): names "English (Turkish)", no Latin (cards, band labels, S4 callouts); ten photo cards
    (the nine plants and giant reed, the one to take out), every photo 28 x 21 mm, fetched by src/common/plant_photos.py;
    the panel fits 371 x 170 mm (the site board's July shade strip goes under it on the page); the WHY HERE shade line
    points to that strip; no scale bar under the bands.
NEW IN v2 (Aras 27 Oct 17:34, booklet Prompt 4 "water, part 1"; a feature change, so the next whole number):
  * "Collect, clean, hold" (wb_system): the three tiles without data go (data honesty rule: no "NO DATA" tiles):
    water quality measured (no measurement of the Selinos in any source the project holds, research/water_data
    README "Still needed" 4), streamside greywater (no volume, no route in any source) and odour cut by plants (no source
    measures it). No estimate replaces them: each would rest on an unknown, not on a figure. The rest re-grid with no
    holes: WHY WE CLEAN 2 x 2, HOW 2 x 2 (reed beds, bed area, then the coliforms a wetland leaves, then UV, so the
    reason for UV sits before it); the tiles grow (the same fit as before) and the rows share what height is left,
    so the column ends level with the cubes' box, no gap at the bottom.
  * "How the stream behaves" (wb_water) stays on this board; the booklet now takes it from the water balance sheet
    (v3), where it leads the water balance page.
  * the text under the component shows a newly pasted version at once, idle (Aras 27 Oct 15:35).
NEW IN v1.14 (Aras 27 Oct 11:07, booklet v9 review; PHASE2_SPEC): visual first, fewer words, nothing overlapping.
  * p.11-14 -> two panels: "wb_water" = how the water behaves (the year on one month axis, the five surveyed cuts and
    DSİ's channel at one round scale, what each level allows (W / F / D), the Roman tunnels' capacity against DSİ's
    Q500) and "wb_system" = what we do with it (the chain as pictograms along one stream ribbon, the storage cubes
    largest, why and how we clean as small tiles). No personal names on the chain (stations by place).
  * p.20 seasons: each season's row = water state, the in-bed sub-hub open/closed (open months computed from this
    board's year calendar), what people do (activity labels and pictograms), and FEEL / HEAR / TOUCH pictograms
    (design intentions, ours); month strip with the Kermes and "the Roman tunnels at work" season.
  * p.21 north-east bank: widths in cm from the drawing's own surfaces; under the cut, one strip a season on the same
    x: the fixed terraces stay, the water and what people do there change, with the same FEEL / HEAR / TOUCH layer.
  * p.22 plants: nine species kept (most used in the design or most useful), bands on the S4 cut, where on site and
    why, with photos fetched once from Wikipedia / Wikimedia Commons (credited in the [n] key; offline = a labelled
    empty frame). Crop wb_plants is sized to share the page with the site board's tree-cover map.
  * every panel: no source lines or footers on the drawings ([n] marks kept), labels at 7 pt or more.
NEW IN v1.13 (Aras 26 Oct 08:27, booklet p.14 "too lean information wise"): the storage panel's eight figures and
their keywords are drawn 1.8 x larger (they printed at about 3 pt beside the cubes); nothing else changed.

OLDER VERSIONS: their notes are in HISTORY.md (repo SupFlyn/BergamaProjectScripts, src/bergama_water_board/).

HOW WE KNOW IT WORKS: after a press, the text under the component reads "v3.2 · HH:MM · N s", the log lists the PDF with
its time and the lines "p.20 S4 seasons: 1:250", "p.21 S4 north-east bank: 1:250" and "p.22 plants: ... photos 10 of 10";
the PDF opens as one A0 page.
"""

import os
import json
import math
import re
import time
import zlib
import tempfile
import datetime
import types as _types

import Rhino
import scriptcontext as sc

VERSION = "bergama_water_board v6.1 (2026-10-29)"
SHORT = "v6.1"
BUTTON_WORDS = ("build", "bake", "run", "go", "press", "button", "start")
BOARD_W, BOARD_H = 1189.0, 841.0     # A0 landscape, mm
M = 14.0                             # board margin, mm
OPTIONS = ("A",)                     # v1.7: option A only (organic only where the project meets the water), Aras 16:43
STORAGE_STYLES = ("cubes",)          # v1.6: cubes only (Aras 25 Oct 13:12; the chart is gone)
CUBE_SCALE = 1000.0                  # the storage cubes' scale, still written to results.json "storage" (v5, T3b: p.12
#                                      draws no cubes panel any more; the design store is a cube at the water map's scale)
OUT_FOLDER = "bergama_water_board"
OUT_NAME = "Bergama_water_board_v6_1_{}_{}.pdf"
LOG_NAME = "bergama_water_board_log.txt"
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

PHI, PSI = 32.9, 36.2                # axonometric of the storage cubes and the farm pictogram (water loop v2 view)

COL = {
    "sheet": "F4F3EE", "paper": "EFEDE6", "faint": "D8D5CC", "structure": "B0AC9C", "ink2": "847E75",
    "ink": "4A3F35", "ink_dark": "2C2219", "white": "FFFFFF", "lane": "FAF8F1",
    "river": "91ADB4", "river_mid": "5D7F8D", "river_dark": "32525F", "bank": "C1D3DB",
    "lit": "D7D3C2", "shade": "BFBBAB", "edge3d": "949081", "ground": "E4E1D6", "soil": "CFC6B2",
    "soil_dk": "B5AA93", "accent": "8B3A3F",
    "aras_alan": "5C48A2", "begum_alan": "7F3902", "nil_alan": "107C73",
}
MP = {"storage": ("CBD9F8", "92A3C9", "3E4C6E"), "discharge": ("90C5D2", "4B92A3", "1B535E"),
      "wetland": ("CBEDE5", "8DB8AF", "2D564E"), "amphibious": ("C1D3DB", "889EA8", "3C5159"),
      "agriculture": ("C6C08D", "948B49", "534E25"), "park": ("DFEBC0", "A7B67F", "49522B")}
BAND_BLUE = ["90C5D2", "4B92A3", "3C5159", "1B535E"]
# the water case panels' colours (bergama_water_case v1.1)
C = {"sheet": "E2E0D4", "paper": "FAF8F1", "faint": "D8D5CC", "structure": "B0AC9C", "ink2": "847E75",
     "ink": "4A3F35", "dark": "2C2219", "white": "FFFFFF", "w1": "C1D3DB", "w2": "91ADB4", "w3": "5D7F8D",
     "w4": "32525F", "d1": "90C5D2", "d2": "4B92A3", "d3": "1B535E", "acc": "8B3A3F", "agri": "948B49",
     "wet": "2D564E", "wet1": "8DB8AF"}

# ---------------------------------------------------------------- sources (short names printed on the board)
RR = u"rain_river_levels/README"
WD = u"water_data/README"
REG = u"DATA_REGISTER"
CR = u"CONCEPT_RECORD v2.4"
CM = u"case.md"
CONCEPT = (u"The loop runs one way, with the river: the water is cleaned and held at Aras's upstream end, a continuous "
           u"strip keeps clean water in the bed all summer and feeds the planting along the way, floods spread onto "
           u"terraces, and Nil's downstream end lets the clean river leave the site, for the existing farmland on the "
           u"slopes outside it. Nothing is pumped back upstream.",
           u"Aras 2026-10-18 14:29; ideas.txt l.6, 12, 18, 24, 26; " + CR + u" D8")
CONCEPT_CHIPS = [("rain", u"STREAM IN"), ("reed", u"CLEAN ONCE · UPSTREAM END"), ("cube", u"HOLD WINTER WATER"),
                 ("strip", u"SUMMER STRIP · FEEDS PLANTING"), ("spread", u"FLOODS ONTO TERRACES"),
                 ("out", u"LEAVES CLEAN · DOWNSTREAM END · FARMS OUTSIDE"), ("noback", u"NO PUMPING BACK")]

# ---------------------------------------------------------------- the year (Group 6's tables)
MONTHS = [u"Jan", u"Feb", u"Mar", u"Apr", u"May", u"Jun", u"Jul", u"Aug", u"Sep", u"Oct", u"Nov", u"Dec"]
WY = [9, 10, 11, 0, 1, 2, 3, 4, 5, 6, 7, 8]          # water-year order Oct-Sep (the DSİ gauges' year)
# A1_monthly_climate.csv: rain measured (WMO 1991-2020 normals, MGM 17742); open-water evaporation calculated
# (Hargreaves, FAO-56, x 1.05)
RAIN = [95.76, 86.33, 64.42, 54.19, 30, 16.08, 7.88, 4.5, 17.11, 59.34, 80.83, 103.16]
EVAP = [32.7, 43.3, 76.8, 115.0, 164.3, 192.3, 205.5, 182.8, 130.6, 83.1, 46.0, 30.6]
# A2_rain_to_river_monthly_m3.csv: natural flow past the site (calculated from DSİ gauges 2016-2021, area-scaled)
RIVER = [7073107, 4466564, 3692654, 2319752, 917943, 427462, 154468, 39136, 37531, 208432, 513967, 1101169]
# A2: rain on the roofs and ground of the four study areas together (calculated)
AREAS_RAIN = [23772, 21431, 15992, 13452, 7447, 3993, 1957, 1117, 4247, 14731, 20065, 25609]
# A3s_monthly_mean_depth_surveyed_sections.csv (v1.1): mean depth above the bed by month (m), via Kömürcü and via
# Ilıca, on the surveyed cross-sections (calculated, worst roughness n 0.050). Below about 0.3 m the depth depends on the
# bed's shape between survey points, which is interpolated: indicative only.
DEPTH = {
    "up": ([0.508, 0.497, 0.459, 0.399, 0.292, 0.215, 0.144, 0.087, 0.056, 0.146, 0.187, 0.279],
           [0.632, 0.505, 0.433, 0.351, 0.212, 0.161, 0.095, 0.040, 0.079, 0.132, 0.221, 0.273]),
    "k4": ([0.216, 0.211, 0.196, 0.172, 0.134, 0.103, 0.074, 0.051, 0.037, 0.075, 0.092, 0.129],
           [0.272, 0.214, 0.185, 0.155, 0.102, 0.081, 0.054, 0.030, 0.047, 0.070, 0.106, 0.126]),
    "k5": ([0.246, 0.241, 0.223, 0.197, 0.148, 0.111, 0.076, 0.048, 0.032, 0.078, 0.098, 0.142],
           [0.309, 0.244, 0.212, 0.176, 0.110, 0.085, 0.052, 0.023, 0.044, 0.071, 0.114, 0.139]),
    "down": ([0.250, 0.246, 0.232, 0.211, 0.177, 0.134, 0.092, 0.058, 0.040, 0.093, 0.118, 0.174],
             [0.301, 0.249, 0.222, 0.195, 0.132, 0.103, 0.063, 0.029, 0.053, 0.085, 0.137, 0.172]),
    "flat": ([0.175, 0.171, 0.158, 0.138, 0.104, 0.078, 0.053, 0.033, 0.022, 0.054, 0.068, 0.101],
             [0.222, 0.174, 0.149, 0.122, 0.076, 0.059, 0.036, 0.015, 0.030, 0.049, 0.080, 0.098]),
}
STRIP_DEPTH = 0.30                   # design value (rain_river README §4)
# Sentinel-2 NDVI, monthly medians 2019-2025 (bergama_plant_data_v1.json: ndvi.by_class; phenology)
NDVI = [(u"riparian strip, 0-30 m of the Selinos", "8B3A3F", 0.7, None,
         [0.288, 0.262, 0.31, 0.325, 0.27, 0.235, 0.259, 0.239, 0.234, 0.246, 0.283, 0.271]),
        (u"rest of the site frame", "847E75", 0.45, [1.0, 0.7],
         [0.185, 0.182, 0.188, 0.192, 0.185, 0.159, 0.158, 0.151, 0.15, 0.167, 0.188, 0.186]),
        (u"deciduous trees (CLC+)", "8FA05A", 0.45, None,
         [0.38, 0.355, 0.433, 0.477, 0.516, 0.507, 0.559, 0.542, 0.515, 0.516, 0.457, 0.366]),
        (u"broadleaved evergreen trees (CLC+)", "8A9478", 0.45, None,
         [0.681, 0.677, 0.637, 0.605, 0.538, 0.497, 0.493, 0.484, 0.498, 0.564, 0.591, 0.661])]
LEAF_ON, LEAF_OFF = 106, 318         # day of the year, deciduous pixels, double-logistic fit (phenology)
VOL_SEALED, VOL_UNSEALED, VOL_FIRST = 26675.0, 83060.0, 3539.0   # m³ (A6_strip_storage.csv; case.md §4)


# ---------------------------------------------------------------- Grasshopper: Button, kept log
def _gh_inputs():
    names = None
    try:
        names = set()
        for p_ in ghenv.Component.Params.Input:                      # noqa: F821 (ghenv exists in Grasshopper)
            for a_ in ("VariableName", "NickName", "Name"):
                v_ = getattr(p_, a_, None)
                if v_:
                    names.add(str(v_))
    except Exception:
        names = None
    out = {}
    for k_, v_ in list(globals().items()):
        if k_.startswith("__") or (names is not None and k_ not in names):
            continue
        if isinstance(v_, (_types.ModuleType, _types.FunctionType, _types.BuiltinFunctionType, type)):
            continue
        out[k_] = v_
    return out


_GH_IN = _gh_inputs()
_T_START = time.time()


def upstream_done(name):
    """v1.6 (as masterplan v16, 25 Oct 12:10): the done text of the script wired into input `name`, read from Rhino's
    memory (sticky) when the wire brings Null. Keys: "done:<guid>" or "...:<guid>_done" (template scripts)."""
    try:
        import scriptcontext as _scx
        for p_ in ghenv.Component.Params.Input:                          # noqa: F821
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


def chain_fire(v, key, name=None):
    """25 Oct 10:20 (one-click chain): the previous script's done output is a text "done HH:MM:SS.ss ..." that stays
    after the Button is released; each NEW text fires this script once (the Button still works as before)."""
    if isinstance(v, (list, tuple)):
        v = next((x for x in v if str(x).startswith("done ")), None)
    s = str(v) if v is not None else ""
    if not s.startswith("done ") and name:
        s = upstream_done(name) or ""
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



def to_bool(v):
    if isinstance(v, (list, tuple)):
        return any(to_bool(x) for x in v)
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v != 0
    return str(v).strip().lower() in ("true", "yes", "1", "on")


def button_state():
    """(name, pressed) of the Button input: any input whose name is a button word, else any input fed by a
    Button, else any input at all."""
    names = list(_GH_IN)
    for k_ in names:
        if "".join(c for c in k_.lower() if c.isalpha()) in BUTTON_WORDS:
            return k_, to_bool(_GH_IN[k_])
    try:
        for p_ in ghenv.Component.Params.Input:                      # noqa: F821
            for src_ in p_.Sources:
                if "button" in type(src_.Attributes.GetTopLevel.DocObject).__name__.lower():
                    nm = str(p_.NickName or p_.Name)
                    return nm, to_bool(_GH_IN.get(nm, False))
    except Exception:
        pass
    if names:
        return names[0], to_bool(_GH_IN[names[0]])
    return None, False


# 25 Oct (Aras 09:55): remembered for this Rhino session only (sticky); no temp state file. The one copy on disk is
# the log in Downloads/Bergama/logs/, read back only if the session lost the last log.
def _key(k):
    try:
        return "{}:{}".format(k, ghenv.Component.InstanceGuid)      # noqa: F821
    except Exception:
        return k


def mem_get(k, default=None):
    kk = _key(k)
    try:
        if kk in sc.sticky:
            return sc.sticky[kk]
    except Exception:
        pass
    if k == "last":
        try:
            with open(os.path.join(LOG_DIR, LOG_NAME), encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return default


def mem_set(k, v):
    try:
        sc.sticky[_key(k)] = v
    except Exception:
        pass


GH_LABEL = "WaterBoard"                                # Aras 25 Oct 09:44: name under the component


def gh_status(text):
    """The text under the component: name, version, then the time of the last run and its length (or idle)."""
    try:
        ghenv.Component.Message = GH_LABEL + " " + text              # noqa: F821
    except Exception:
        pass


def gh_message(level, text):
    try:
        import Grasshopper
        lv = {"error": Grasshopper.Kernel.GH_RuntimeMessageLevel.Error,
              "warning": Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning}[level]
        ghenv.Component.AddRuntimeMessage(lv, text[:500])            # noqa: F821
    except Exception:
        pass


# ---------------------------------------------------------------- palette file (newer colours win)


# ---------------------------------------------------------------- text metrics, page and PDF writer (water loop v2)
_MCH = u' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
_MW0 = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556, 556, 556,
        556, 556, 556, 556, 556, 278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278,
        500, 667, 556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469,
        556, 333, 556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500,
        278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584]
_MW1 = [278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556, 556, 556,
        556, 556, 556, 556, 556, 333, 333, 584, 584, 584, 611, 975, 722, 722, 722, 722, 667, 611, 778, 722, 278,
        556, 722, 611, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 333, 278, 333, 584,
        556, 333, 556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889, 611, 611, 611, 611, 389, 556,
        333, 611, 556, 778, 556, 556, 500, 389, 280, 389, 584]
_W = [dict(zip(_MCH, _MW0)), dict(zip(_MCH, _MW1))]
_WX = {u"·": 278, u"³": 333, u"²": 333, u"µ": 556, u"§": 556, u"İ": 278, u"ı": 278, u"–": 556, u"°": 400}
PT = 25.4 / 72.0
CAP = 0.716


def text_w(s, size, bold=False):
    w = _W[1 if bold else 0]
    return sum(w.get(c, _WX.get(c, 600 if c.isupper() else 556)) for c in s) / 1000.0 * size


def wrap(s, size, width, bold=False):
    out, cur = [], ""
    for wd in s.split():
        t = (cur + " " + wd).strip()
        if cur and text_w(t, size, bold) > width:
            out.append(cur)
            cur = wd
        else:
            cur = t
    if cur:
        out.append(cur)
    return out


# ---------------------------------------------------------------- page and PDF writer (v1; see-through fills as bergama_diagrams v1.8)
class Page(object):
    def __init__(self, W, H):
        self.W, self.H, self.items = W, H, []

    def poly(self, rings, fill=None, stroke=None, lw=0.1, dash=None, stripes=None, layer=None, alpha=None):
        """alpha: opacity 0-1 of fill and stroke (steps of 0.05; None = opaque). layer: unused (tree block API)."""
        rings = [r for r in rings if len(r) >= 3]
        if rings:
            self.items.append(("poly", rings, fill, stroke, lw, dash, stripes, alpha))

    def line(self, pts, stroke, lw=0.1, dash=None, cap=1, layer=None):
        if len(pts) >= 2:
            self.items.append(("line", pts, stroke, lw, dash, cap))

    def circle(self, cx, cy, r, fill=None, stroke=None, lw=0.1):
        self.items.append(("circle", cx, cy, r, fill, stroke, lw))

    def text(self, s, x, y, size, color, bold=False, align="L", mat=None, halo=None):
        if s and mat is None and any(ch in SUP for ch in s):    # v3.1: m² / m³ as a raised small digit (see SUP)
            runs = sup_runs(s)
            ws = [text_w(t, size * (SUP_K if up else 1.0), bold) for t, up in runs]
            x -= {"L": 0.0, "C": sum(ws) / 2.0, "R": sum(ws)}[align]
            for (t, up), w_ in zip(runs, ws):
                self.items.append(("text", t, x, y + (size * SUP_UP if up else 0.0), size * (SUP_K if up else 1.0), color,
                                   bold, "L", None, halo))
                x += w_
        elif s:
            self.items.append(("text", s, x, y, size, color, bold, align, mat, halo))


# v3.1 (Aras 27 Oct, Prompt 6: "hm³ renders as hm"): ² and ³ are drawn as the digit at 0.6 x the size, raised 0.28 x the
# size (the digit is then as wide as the ²/³ glyph, 333/1000): the unembedded Helvetica's ²/³ was missing in some viewers
SUP = {u"²": u"2", u"³": u"3"}
SUP_K, SUP_UP = 0.6, 0.28


def sup_runs(s):
    """v3.1: s cut into (text, raised) runs at ² and ³, which become a plain 2 or 3"""
    out, cur = [], u""
    for ch in s:
        if ch in SUP:
            if cur:
                out.append((cur, False))
            out.append((SUP[ch], True))
            cur = u""
        else:
            cur += ch
    if cur:
        out.append((cur, False))
    return out


def hex_rgb(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0)


_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"


def pdf_str(s):
    out = bytearray()
    for ch in s:
        if ch in _ENC_EXTRA:
            out.append(_ENC_EXTRA[ch])
            continue
        try:
            b = ch.encode("cp1252")
        except Exception:
            b = b"?"
        if b in (b"\x9e",):
            b = b"?"
        out += b
    s2 = bytes(out).replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")
    return b"(" + s2 + b")"


def _f(v):
    s = "{:.3f}".format(v).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def page_stream(pg):
    o = []
    A = o.append
    A("2.834646 0 0 2.834646 0 0 cm 1 J 1 j")
    cur = {}

    def col(c, stroke):
        k = "S" if stroke else "f"
        if cur.get(k) == c:
            return
        cur[k] = c
        r, g, b = hex_rgb(c)
        A("{} {} {} {}".format(_f(r), _f(g), _f(b), "RG" if stroke else "rg"))

    def path(pts, close):
        A("{} {} m".format(_f(pts[0][0]), _f(pts[0][1])))
        for p in pts[1:]:
            A("{} {} l".format(_f(p[0]), _f(p[1])))
        if close:
            A("h")

    def lw_dash(lw, dash, cap=1):
        A("{} w {} J 1 j [{}] 0 d".format(_f(lw), cap, " ".join(_f(d) for d in (dash or []))))

    for it in pg.items:
        kind = it[0]
        if kind == "poly":
            _, rings, fill, stroke, lw, dash, stripes, alpha = it
            if alpha is not None and alpha < 0.975:                 # see-through: an ExtGState of write_pdf
                A("q /A{:02d} gs".format(max(1, int(round(alpha * 20)))))
                cur.clear()
            if fill:
                col(fill, False)
            if stroke:
                col(stroke, True)
                lw_dash(lw, dash)
            for r in rings:
                path(r, True)
            A("B*" if fill and stroke else ("f*" if fill else "S"))
            if stripes:                       # (colour, spacing mm, width mm[, angle deg, wavy])
                sc_, sp_, w_ = stripes[:3]
                ang = math.radians(stripes[3] if len(stripes) > 3 else 45.0)
                wavy = len(stripes) > 4 and stripes[4]
                A("q")
                for r in rings:
                    path(r, True)
                A("W* n")
                col(sc_, True)
                lw_dash(w_, None, 1)
                dx_, dy_ = math.cos(ang), math.sin(ang)
                nx_, ny_ = -dy_, dx_
                allp = [p for r in rings for p in r]
                ns = [p[0] * nx_ + p[1] * ny_ for p in allp]
                ds = [p[0] * dx_ + p[1] * dy_ for p in allp]
                s_ = min(ns)
                while s_ < max(ns):
                    if wavy:
                        t_, pts_ = min(ds), []
                        while t_ <= max(ds) + 0.5:
                            o_ = s_ + sp_ * 0.22 * math.sin(t_ * 2.0 * math.pi / 3.2)
                            pts_.append((dx_ * t_ + nx_ * o_, dy_ * t_ + ny_ * o_))
                            t_ += 0.5
                        path(pts_, False)
                    else:
                        A("{} {} m {} {} l".format(_f(dx_ * min(ds) + nx_ * s_), _f(dy_ * min(ds) + ny_ * s_),
                                                   _f(dx_ * max(ds) + nx_ * s_), _f(dy_ * max(ds) + ny_ * s_)))
                    s_ += sp_
                A("S Q")
                cur.pop("S", None)
            if alpha is not None and alpha < 0.975:
                A("Q")
                cur.clear()
        elif kind == "line":
            _, pts, stroke, lw, dash, cap = it
            col(stroke, True)
            lw_dash(lw, dash, cap)
            path(pts, False)
            A("S")
        elif kind == "circle":
            _, cx, cy, r, fill, stroke, lw = it
            kk = 0.5523 * r
            if fill:
                col(fill, False)
            if stroke:
                col(stroke, True)
                lw_dash(lw, None)
            A("{} {} m".format(_f(cx + r), _f(cy)))
            for (a1, a2, a3) in (((cx + r, cy + kk), (cx + kk, cy + r), (cx, cy + r)),
                                 ((cx - kk, cy + r), (cx - r, cy + kk), (cx - r, cy)),
                                 ((cx - r, cy - kk), (cx - kk, cy - r), (cx, cy - r)),
                                 ((cx + kk, cy - r), (cx + r, cy - kk), (cx + r, cy))):
                A("{} {} {} {} {} {} c".format(_f(a1[0]), _f(a1[1]), _f(a2[0]), _f(a2[1]), _f(a3[0]), _f(a3[1])))
            A("h " + ("B" if fill and stroke else ("f" if fill else "S")))
        elif kind == "text":
            _, s, x, y, size, color, bold, align, mat, halo = it
            w = text_w(s, size, bold)
            reps = [(halo, True), (color, False)] if halo else [(color, False)]
            for c_, hal in reps:
                if hal:
                    r_, g_, b_ = hex_rgb(c_)
                    A("q {} {} {} RG {} w 1 j 1 Tr".format(_f(r_), _f(g_), _f(b_), _f(size * 0.16)))
                else:
                    col(color, False)
                    A("0 Tr")
                _text_ops(A, s, x, y, size, bold, align, mat, w)
                if hal:
                    A("Q")
    return "\n".join(o).encode("latin-1")


def _text_ops(A, s, x, y, size, bold, align, mat, w):
    if mat is None:
        dx = {"L": 0.0, "C": -w / 2, "R": -w}[align]
        A("BT /F{} {} Tf 1 0 0 1 {} {} Tm".format(2 if bold else 1, _f(size), _f(x + dx), _f(y)))
    else:
        (a, b), (c, d) = mat
        f = {"L": 0.0, "C": -w / 2 / size, "R": -w / size}[align]
        A("BT /F{} 1 Tf {} {} {} {} {} {} Tm".format(2 if bold else 1, _f(a * size), _f(b * size), _f(c * size),
                                                    _f(d * size), _f(x + f * a * size), _f(y + f * b * size)))
    A(pdf_str(s).decode("latin-1") + " Tj ET")


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


def write_pdf(pg, path, title):
    objs = []

    def add(b):
        objs.append(b)
        return len(objs)
    font = pdf_fonts(add, ("R", "B"))                     # G2/G3 28 Oct: Arial embedded (common/pdf_fonts.py)
    gs = [add("<< /Type /ExtGState /ca {0} /CA {0} >>".format(_f(i / 20.0)).encode("latin-1")) for i in range(1, 20)]
    gs_res = " ".join("/A{:02d} {} 0 R".format(i + 1, o_) for i, o_ in enumerate(gs))
    pages_id = add(b"")
    data = zlib.compress(page_stream(pg), 6)
    cid = add(b"<< /Length " + str(len(data)).encode() + b" /Filter /FlateDecode >>\nstream\n" + data +
              b"\nendstream")
    kid = add("<< /Type /Page /Parent {} 0 R /MediaBox [0 0 {} {}] /Contents {} 0 R /Resources << /Font "
              "<< /F1 {} 0 R /F2 {} 0 R >> /ExtGState << {} >> >> >>".format(pages_id, _f(pg.W / PT), _f(pg.H / PT), cid,
                                                                                    font[0], font[1], gs_res).encode("latin-1"))
    objs[pages_id - 1] = "<< /Type /Pages /Kids [{} 0 R] /Count 1 >>".format(kid).encode("latin-1")
    cat = add("<< /Type /Catalog /Pages {} 0 R >>".format(pages_id).encode("latin-1"))
    info = add(b"<< /Title " + pdf_str(title) + b" /Producer " + pdf_str(VERSION) + b" >>")
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offs = []
    for i, b in enumerate(objs):
        offs.append(len(out))
        out += "{} 0 obj\n".format(i + 1).encode() + b + b"\nendobj\n"
    x = len(out)
    out += "xref\n0 {}\n0000000000 65535 f \n".format(len(objs) + 1).encode()
    for o_ in offs:
        out += "{:010d} 00000 n \n".format(o_).encode()
    out += "trailer\n<< /Size {} /Root {} 0 R /Info {} 0 R >>\nstartxref\n{}\n%%EOF\n".format(
        len(objs) + 1, cat, info, x).encode()
    with open(path, "wb") as fh:
        fh.write(bytes(out))

# ============================================================ TREES (self-contained: copy this block as it is)
# Trees in the style of Nil's reference (18 Oct 2026: an isometric water-system diagram with layered, see-through
# canopies), drawn as architectural entourage (fine branches, translucent leaf clusters), not as cartoon blobs. Needs only `math` and a page object with
#     poly(rings, fill=hex, stroke=hex or None, lw=mm, layer=str, alpha=0-1 or None)   rings: [[(X, Y), ...], ...]
#     line(pts, stroke_hex, lw_mm, layer=str)
# draw_tree(pg, P, k, x, y, r, top, style) draws one tree: P(x, y, z) -> page (X, Y) in mm for a parallel
# (orthographic) view with z up, k = page mm per model metre. Light comes from the upper left of the page, as on the
# buildings. Size and height are the data's: crown radius r and top height `top` (m above the ground); the crown starts
# at TREE_CROWN_LO(top), the analyses' convention in selinus_board (crown_lo: 35 % of the top, at least 1.5 m), so the
# crown is an upright ellipsoid r wide and top - lo high (a crown never flatter than half its radius), filled with leaf
# clusters near its surface. Branches and clusters are drawn from (x, y) alone, so the same tree looks the same on every
# page and run.
# Draw trees far to near (painter's order). The colours are the group palette's greens (palette v1.3):
#     tree  (deciduous)             green_mid 727A4E, green_light 8C9969, light = mix(8C9969, road FAF8F1, 0.35)
#     olive (evergreen broadleaf)   mix(727A4E, ink2 847E75, 0.4), mix(8C9969, structure B0AC9C, 0.45), its light
#     pine  (needle-leaved)         green_deep 495338, green_mid 727A4E, mix(727A4E, 8C9969, 0.6)
#     context (pale, not the topic) mix(BCC2A6, 8C9969, 0.3), CONTEXT_3D tree BCC2A6, mix(BCC2A6, FAF8F1, 0.45)
# (mix = the palette's OKLab mix). Shadows: green_deep (context: structure) at 10-16 %.
TREE_STYLES = {
    "tree":    dict(dark="727A4E", mid="8C9969", light="B1BA97", trunk="5B5147", shadow="495338", shadow_a=0.10,
                    lobes=1.0),
    "olive":   dict(dark="797C5E", mid="9CA280", light="BCBFA6", trunk="5B5147", shadow="495338", shadow_a=0.10,
                    lobes=1.0),
    "pine":    dict(dark="495338", mid="727A4E", light="818C5E", trunk="5B5147", shadow="495338", shadow_a=0.12,
                    lobes=1.3),                                    # needles: more, finer leaf clusters
    "context": dict(dark="ADB694", mid="BCC2A6", light="D7DAC7", trunk="A39E90", shadow="B0AC9C", shadow_a=0.16,
                    lobes=1.0),
}
TREE_ALPHA = (0.62, 0.68)                # opacity of the leaf clusters behind and in front of the branches
TREE_MIN_MM = 0.25                       # smallest crown radius drawn on the page, mm


def TREE_CROWN_LO(top):
    return max(1.5, 0.35 * top)


def _tree_rand(x, y):
    """A small repeatable random stream from the tree's position (the same in every Python)."""
    s = [(int(round(x * 100.0)) * 73856093 ^ int(round(y * 100.0)) * 19349663) & 0x7FFFFFFF or 1]

    def nxt():
        s[0] = (s[0] * 1103515245 + 12345) & 0x7FFFFFFF
        return s[0] / 2147483648.0
    return nxt


def tree_shadow(pg, P, k, x, y, r, style, layer="tree_shadows"):
    """The crown's footprint on the ground, pushed to the lower right (light from the upper left). Draw all shadows
    on the ground first (draw_tree(..., shadow=False) then), so no shadow lies over a building."""
    A = max(TREE_MIN_MM, r * k)
    if A < 0.45:
        return
    sh = [P(x + 0.9 * r * math.cos(t), y + 0.9 * r * math.sin(t), 0.0) for t in [2.0 * math.pi * i / 28 for i in range(28)]]
    pg.poly([[(p[0] + 0.30 * A, p[1] - 0.08 * A) for p in sh]], fill=style["shadow"], stroke=None, layer=layer,
            alpha=style["shadow_a"])


def _tree_view(P, k):
    """Rows of the parallel view (page mm per metre / k) and the unit vector pointing away from the viewer."""
    o = P(0.0, 0.0, 0.0)
    e = [P(1.0, 0.0, 0.0), P(0.0, 1.0, 0.0), P(0.0, 0.0, 1.0)]
    u = [(p[0] - o[0]) / k for p in e]
    v = [(p[1] - o[1]) / k for p in e]
    c = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    return u, v, (-c[0], -c[1], -c[2])


def _tree_blob(cx, cy, R, rnd, m):
    """A leaf cluster: a round patch R mm across with a ragged, leafy edge."""
    ph = rnd() * 6.283
    return [(cx + R * (0.80 + 0.28 * rnd()) * math.cos(ph + 6.283 * i / m),
             cy + R * (0.80 + 0.28 * rnd()) * math.sin(ph + 6.283 * i / m)) for i in range(m)]


def draw_tree(pg, P, k, x, y, r, top, style, layer="trees", alpha=TREE_ALPHA, shadow=True):
    """Architectural entourage tree: a fine trunk and branch structure inside a crown built from many see-through
    leaf clusters, lit from the upper left, back clusters behind the branches and front clusters over them."""
    rnd = _tree_rand(x, y)
    st = style
    lo = TREE_CROWN_LO(top)
    a = max(0.5 * r, (top - lo) / 2.0)                     # vertical half-height of the crown
    zc = top - a
    A = r * k                                              # crown half-width on the page, mm
    u, v, d = _tree_view(P, k)
    if A < 0.45:                                           # a speck on the corridor pages: two small clusters
        c = P(x, y, zc)
        R = max(TREE_MIN_MM, A)
        for i in range(2):
            pg.poly([_tree_blob(c[0] + (i - 0.5) * 0.4 * R, c[1] + (0.5 - i) * 0.2 * R, R * (0.95 - 0.2 * i), rnd, 9)],
                    fill=st["mid"] if i else st["dark"], stroke=None, layer=layer, alpha=0.8)
        return
    if shadow:
        tree_shadow(pg, P, k, x, y, r, st, layer)
    full = A >= 1.2
    tw = min(0.30, max(0.06, 0.055 * A))                   # trunk line, mm
    # ---- branch structure (3D points, projected)
    lines = [((x, y, 0.0), (x, y, lo + 0.25 * a), tw)]
    if full:
        nb = 3 + int(rnd() * 3)
        for i in range(nb):
            t = 6.283 * (i + 0.6 * rnd()) / nb
            fr = 0.55 + 0.3 * rnd()
            end = (x + fr * r * math.cos(t), y + fr * r * math.sin(t), zc + (0.1 + 0.4 * rnd()) * a)
            base = (x, y, lo + (0.1 + 0.4 * rnd()) * a)
            lines.append((base, end, tw * 0.55))
            mid = tuple(base[j] + 0.55 * (end[j] - base[j]) for j in range(3))
            for _ in range(2):                             # twigs end inside the crown (70 % of its size at most)
                t2 = t + (rnd() - 0.5) * 1.6
                ez = rnd() * 0.6
                eh = 0.7 * math.sqrt(1.0 - ez * ez)
                lines.append((mid, (x + eh * r * math.cos(t2), y + eh * r * math.sin(t2), zc + 0.7 * ez * a),
                              max(0.04, tw * 0.3)))
    # ---- leaf clusters near the crown's surface, sorted far to near
    n = int(min(36, max(6, 4 + 3.0 * A)) * st.get("lobes", 1.0))
    cl = []
    for _ in range(n):
        ct, phi_ = 2.0 * rnd() - 1.0, 6.283 * rnd()
        sq = math.sqrt(max(0.0, 1.0 - ct * ct))
        f = 0.55 + 0.35 * rnd()
        q = (x + f * r * sq * math.cos(phi_), y + f * r * sq * math.sin(phi_), zc + f * a * ct)
        depth = sum(d[j] * (q[j] - (x, y, zc)[j]) for j in range(3))
        pp = P(*q)
        du, dv = (pp[0] - P(x, y, zc)[0]) / A, (pp[1] - P(x, y, zc)[1]) / max(1e-9, A)
        lit = -0.6 * du + 0.8 * dv - 0.5 * depth / max(r, a)
        cl.append((depth, pp, lit, (0.30 + 0.14 * rnd()) * A * st.get("blob", 1.0)))
    cl.sort(key=lambda c_: -c_[0])
    m = 16 if A > 3.0 else (12 if full else 9)
    back = [c_ for c_ in cl if c_[0] > 0.0]
    front = [c_ for c_ in cl if c_[0] <= 0.0]

    def blobs(lst, al):
        for _, pp, lit, R in lst:
            col = st["light"] if lit > 0.45 else (st["dark"] if lit < -0.25 else st["mid"])
            pg.poly([_tree_blob(pp[0], pp[1], R, rnd, m)], fill=col, stroke=None, layer=layer, alpha=al)
    blobs(back, alpha[0])
    for p0, p1, w in lines:
        pg.line([P(*p0), P(*p1)], st["trunk"], w, layer=layer)
    blobs(front, alpha[1])


# ============================================================ end of TREES


# ---------------------------------------------------------------- composing the board from drawn parts
# Every drawing is drawn on its own Page at its natural size (page mm), then placed on the board at one uniform
# scale that fits its box (place). Text, lines and dashes scale with it, as a reduced print does.
def items_bbox(items):
    xs, ys = [], []
    for it in items:
        k = it[0]
        if k == "poly":
            for r in it[1]:
                xs += [p[0] for p in r]
                ys += [p[1] for p in r]
        elif k == "line":
            xs += [p[0] for p in it[1]]
            ys += [p[1] for p in it[1]]
        elif k == "circle":
            _, cx, cy, r = it[:4]
            xs += [cx - r, cx + r]
            ys += [cy - r, cy + r]
        elif k == "text":
            _, s, x, y, size, color, bold, align, mat, halo = it
            w = text_w(s, size, bold)
            f = {"L": 0.0, "C": -0.5, "R": -1.0}.get(align, 0.0)
            (a, b), (c, d) = mat if mat else ((1.0, 0.0), (0.0, 1.0))
            for u, v in ((f * w, -0.25 * size), ((f + 1) * w, -0.25 * size), (f * w, CAP * size),
                         ((f + 1) * w, CAP * size)):
                xs.append(x + a * u + c * v)
                ys.append(y + b * u + d * v)
    if not xs:
        return (0.0, 0.0, 0.0, 0.0)
    return (min(xs), min(ys), max(xs), max(ys))


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
    return out


def place(pg, part, box, max_s=1.0, align="C", log=None, name=""):
    """Puts part (a Page) into box (x0, y0, x1, y1) at the largest scale up to max_s that fits, centred (align C) or
    at the top left (align TL). Returns (scale, placed bbox)."""
    b = items_bbox(part.items)
    bw, bh = max(b[2] - b[0], 1e-6), max(b[3] - b[1], 1e-6)
    s = min(max_s, (box[2] - box[0]) / bw, (box[3] - box[1]) / bh)
    if align == "TL":
        dx, dy = box[0] - s * b[0], box[3] - s * b[3]
    else:
        dx = (box[0] + box[2]) / 2.0 - s * (b[0] + b[2]) / 2.0
        dy = (box[1] + box[3]) / 2.0 - s * (b[1] + b[3]) / 2.0
    pg.items += xform(part.items, s, dx, dy)
    small = min([it[4] for it in part.items if it[0] == "text"] or [9.0]) * s
    if log is not None and small < 1.25:
        log.append(u"NOTE {}: placed at {:.0%} of its drawn size; smallest text {:.1f} mm".format(name, s, small))
    return s, (dx + s * b[0], dy + s * b[1], dx + s * b[2], dy + s * b[3])


def spread(ys, gap, lo=None, hi=None):
    """Label heights pushed apart to at least `gap` (in the order given, which must be rising), kept under hi."""
    out = []
    for y in ys:
        out.append(max(y, out[-1] + gap) if out else (y if lo is None else max(lo, y)))
    if hi is not None and out and out[-1] > hi:
        d = out[-1] - hi
        out = [y - d for y in out]
        for i in range(len(out) - 2, -1, -1):
            out[i] = min(out[i], out[i + 1] - gap)
    return out


# ---------------------------------------------------------------- drawing helpers (page mm, y up)
def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


# section_style names (SEC, sec_*) now live in section_parts.py (29 Oct 2026, WO-T2b-3); this keeps old includes working.
# ---- section language of the main site board (selinus_board draw_section_strip), shared by the water board and the
# agriculture alternatives (Aras 25 Oct 21:52: their sections drawn "such as we draw in the site sections"): the cut
# ground a shade darker than the page with a fine ink line, water hatched in blue from the bed to its surface, the
# channel above it in a pale wash, whole trees and plants at their stated size. One scale for x and y (Aras 22:02:
# "not stretch anything ever"). Pure geometry: each helper returns shapes, the script's sec_put() draws them.
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
    """A water body (ring, page mm): channel blue, 45-degree blue hatch, the water line on top (as draw_stream)."""
    sh = [("poly", ring, SEC["channel"], None, 0.1)]
    sh += [("line", [p, q], SEC["hatch"], lw) for p, q in sec_hatch(ring, spacing)]
    top = max(p[1] for p in ring)
    xs = [p[0] for p in ring if abs(p[1] - top) < 1e-6]
    if len(xs) >= 2:
        sh.append(("line", [(min(xs), top), (max(xs), top)], SEC["hatch"], 0.3))
    return sh


def sec_tree(x, gy, h, r, k, tone="crown", lo=None):
    """A whole tree in section at its stated size: h tall, crown r wide each side (m), k page mm per m, ground at
    (x, gy). Trunk to the crown base (35 % of the top, at least 1.5 m: the board's crown_lo), crown as overlapping
    lobes in two tones, a few branches."""
    import math as _m
    lo = max(1.5, 0.35 * h) if lo is None else lo
    lo = min(lo, h * 0.6)
    tw = max(0.12, 0.05 * r * k)
    cy = gy + (lo + (h - lo) / 2.0) * k
    rx, ry = r * k, max(0.5 * r, (h - lo) / 2.0) * k            # a crown never flatter than half its radius (board)
    sh = [("poly", [(x - tw, gy), (x + tw, gy), (x + tw * 0.6, gy + lo * k + ry * 0.4),
                    (x - tw * 0.6, gy + lo * k + ry * 0.4)], SEC["trunk"], None, 0.1)]
    col = SEC.get(tone, SEC["crown"])
    lobes = [(0.0, 0.0, 1.0, 1.0), (-0.42, -0.18, 0.62, 0.7), (0.44, -0.12, 0.6, 0.72), (-0.2, 0.36, 0.6, 0.6),
             (0.26, 0.3, 0.58, 0.62)]
    for i, (dx, dy, fx, fy) in enumerate(lobes):
        sh.append(("poly", sec_ellipse(x + dx * rx, cy + dy * ry, fx * rx, fy * ry, 24),
                   col if i == 0 else (SEC["crown_lt"] if i % 2 else col), SEC["ink2"] if i == 0 else None, 0.08))
    for s_, ang in ((-1, 50.0), (1, 40.0), (-1, 70.0)):
        a = _m.radians(ang)
        b0 = (x, gy + lo * k)
        sh.append(("line", [b0, (x + s_ * _m.cos(a) * rx * 0.55, gy + lo * k + _m.sin(a) * ry * 0.9)], SEC["trunk"],
                   max(0.08, tw * 0.6)))
    return sh


def sec_shrub(x, gy, h, w, k, col=None):
    """A shrub h tall, w wide (m): a dome on the ground with a lighter top lobe."""
    rx, ry = w / 2.0 * k, h / 2.0 * k
    return [("poly", sec_ellipse(x, gy + ry, rx, ry, 24), col or SEC["shrub"], SEC["ink2"], 0.06),
            ("poly", sec_ellipse(x - rx * 0.25, gy + ry * 1.2, rx * 0.45, ry * 0.4, 16), SEC["crown_lt"], None, 0.1)]


def sec_reeds(x0, x1, gy, h, k, step=0.35):
    """Reeds h tall (m) from x0 to x1 (page mm); gy(x) = ground y. Stems with seed heads."""
    sh, i = [], 0
    x = x0
    while x <= x1:
        hh = h * (0.78 + 0.22 * ((i * 7) % 5) / 4.0) * k
        g = gy(x)
        lean = 0.12 * hh * (1 if i % 2 else -1) * 0.3
        sh.append(("line", [(x, g), (x + lean, g + hh)], SEC["reed"], 0.12))
        if i % 3 == 0:
            sh.append(("poly", sec_ellipse(x + lean, g + hh, 0.18 * k * 0.6 + 0.12, 0.45 * k * 0.6 + 0.25, 10),
                       SEC["reed_head"], None, 0.1))
        x += step * k
        i += 1
    return sh


def sec_tufts(x0, x1, gy, h, k, step=0.25, col=None):
    """Grass and meadow tufts h tall (m) from x0 to x1 (page mm)."""
    sh, i = [], 0
    x = x0
    while x <= x1:
        g = gy(x)
        hh = h * k * (0.7 + 0.3 * ((i * 3) % 4) / 3.0)
        for d in (-0.35, 0.0, 0.35):
            sh.append(("line", [(x, g), (x + d * hh * 0.6, g + hh * (1.0 - abs(d) * 0.4))], col or SEC["grass"], 0.1))
        x += step * k
        i += 1
    return sh


def sec_lavender(x0, x1, gy, k, h=0.5):
    """Lavender mounds about h tall (m) with flower spikes."""
    sh = []
    w = 0.8 * k
    x = x0 + w / 2.0
    while x <= x1 - w / 2.0 + 1e-6:
        g = gy(x)
        sh += sec_shrub(x, g, h, 0.8, k, col=_sec_mix(SEC["olive"], SEC["paper"], 0.1))
        for d in (-0.25, 0.0, 0.25):
            sh.append(("line", [(x + d * w, g + h * k * 0.8), (x + d * w * 1.3, g + h * k * 1.3)], SEC["lav"], 0.25))
        x += w
    return sh


# ---- section parts (WO-T2b-3, 29 Oct 2026; section_style.py now includes this file): the river bank as it is at the
# cut (brief 02 §4): DSİ stone walls at 5.00 m, embankments at their surveyed angle, loose earth banks, railings and
# parapets; stone, concrete, earth and the gravel bed in their own hatch; terraces and steps cut into the bank.
# Real sizes in m placed by k (page mm per m); a bank's surface runs from its toe at the bed landward.

SCT_DSI_WALL_H_M = 5.00   # revision_2026-10-29/T1/levels/RESULT.md line 18: "DSİ stone walls at bed + 5.00 m" (Aras 28 Oct)

# material fills (palette v1.4, palette/bergama_palette.py; lines in the section_style inks)
SCT = dict(stone=_sec_mix("B0AC9C", "EFEDE6", 0.35),   # CORE structure toward CORE paper
           concrete="D8D5CC",                         # CORE faint
           earth=SEC["soil"],                         # section_style cut ground
           gravel="CFCCC5",                           # CORE street
           line=SEC["ink2"],                          # VARIANTS 0.0 ink2: hatch lines
           cut=SEC["ink"])                            # CORE ink: the cut line


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


def sct_hatch_fill(ring, material, k, outline=None, lw=0.25):
    """A cut ring (page mm) in its material's fill and standard hatch: stone, concrete, earth, gravel or water."""
    import math as _m
    if material == "water":
        return sec_water(ring)
    if material not in ("stone", "concrete", "earth", "gravel"):
        raise ValueError("sct_hatch_fill: unknown material %r" % material)
    g = max(0.7, min(1.4, k / 5.0))           # patterns are page-mm conventions (1:200 size), eased with k; no real sizes
    ln = SCT["line"]
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    sh = [("poly", ring, SCT[material], None, 0.1)]
    if material == "stone":                   # coursed masonry: bed joints and staggered head joints
        c = 1.4 * g
        for p, q in sec_hatch(ring, c, 0.0):
            sh.append(("line", [p, q], ln, 0.08))
        j = int(_m.floor(min(ys) / c))
        while j * c < max(ys):
            i = int(_m.floor(min(xs) / (2 * c))) - 1
            while (2 * i + (j % 2)) * c <= max(xs):
                x = (2 * i + (j % 2)) * c
                for a, b in _sct_clip(ring, (x, j * c), (x, (j + 1) * c)):
                    sh.append(("line", [a, b], ln, 0.08))
                i += 1
            j += 1
    elif material == "concrete":              # aggregate: dots and small open triangles
        d = 1.1 * g
        for i in range(int(_m.floor(min(xs) / d)), int(_m.floor(max(xs) / d)) + 1):
            for j in range(int(_m.floor(min(ys) / d)), int(_m.floor(max(ys) / d)) + 1):
                px, py = (i + _sct_rnd(i, j)) * d, (j + _sct_rnd(j, i + 7)) * d
                if not _sct_inside(ring, (px, py)):
                    continue
                if (i + j) % 3 == 0:
                    s, a = 0.28 * g, _sct_rnd(i + 3, j) * 6.283
                    tri = [(px + s * _m.cos(a + t * 2.094), py + s * _m.sin(a + t * 2.094)) for t in range(3)]
                    sh.append(("line", tri + [tri[0]], ln, 0.07))
                else:
                    sh.append(("poly", sec_ellipse(px, py, 0.09 * g, 0.09 * g, 6), ln, None, 0.1))
    elif material == "earth":                 # earth: broken 45-degree hatch
        dash, gap = 0.9 * g, 0.55 * g
        for p, q in sec_hatch(ring, 1.3 * g, 45.0):
            L = _m.hypot(q[0] - p[0], q[1] - p[1])
            if L < 1e-6:
                continue
            ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
            s = 0.0
            while s < L:
                e = min(L, s + dash)
                sh.append(("line", [(p[0] + ux * s, p[1] + uy * s), (p[0] + ux * e, p[1] + uy * e)], ln, 0.07))
                s = e + gap
    else:                                     # gravel: small rounded stones, open
        d = 0.9 * g
        for i in range(int(_m.floor(min(xs) / d)), int(_m.floor(max(xs) / d)) + 1):
            for j in range(int(_m.floor(min(ys) / d)), int(_m.floor(max(ys) / d)) + 1):
                px, py = (i + 0.2 + 0.6 * _sct_rnd(i, j)) * d, (j + 0.2 + 0.6 * _sct_rnd(j, i + 3)) * d
                r = (0.14 + 0.16 * _sct_rnd(i + 5, j + 1)) * g
                if _sct_inside(ring, (px, py)):
                    sh.append(("poly", sec_ellipse(px, py, r, r * 0.8, 8), None, ln, 0.06))
    if outline:
        sh.append(("poly", ring, None, outline, lw))
    return sh


def sct_ground(surface, bottom_y, k, material="earth", lw=0.35):
    """Cut ground under a surface polyline (page mm, left to right) down to bottom_y: hatch and the cut line."""
    ring = list(surface) + [(surface[-1][0], bottom_y), (surface[0][0], bottom_y)]
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
# v5 (revision 29 Oct, T3b): the shared modules the pages call (T2a levels + basemap, T2b plants + icons); plants after
# section_style (it includes section_parts)
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


def _pla_c(fill, accent=None, stem=None):
    """The colour set of one species: fill, edge, lighter lobes, stem, accent (same in both views)."""
    return dict(fill=fill, edge=SEC["ink2"], lt=_sec_mix(fill, SEC["paper"], 0.35), stem=stem or SEC["trunk"],
                accent=accent)


# one entry per species (species.json species_data + giant reed from the screening); h_range = sourced (lo, hi) m
PLA_SPECIES = {
    "plane": dict(name="Oriental plane", turkish="Doğu çınarı", latin="Platanus orientalis", layer="tree",
                  form="dome", foliage="deciduous (S26)", status="keep",
                  h_range=(None, 30.0), h_m=15.0,            # "up to 30 m" S68, S69
                  crown_m=15.0,                              # "wider than 8 metres" S70: form rule 1.0 x h (>= 8)
                  bloom=[4, 5], leaf=PLA_LEAF_SITE,          # Apr-May S69 (secondary)
                  colours=_pla_c(SEC["crown"])),             # section_style SEC crown
    "ash": dict(name="Narrow-leaved ash", turkish="Dişbudak", latin="Fraxinus angustifolia", layer="tree",
                form="oval", foliage="deciduous (S7)", status="keep",
                h_range=(None, 40.0), h_m=20.0,              # "40-45m" maximum S7 (lower figure)
                crown_m=14.0,                                # "dense, irregular and dome shaped" S7: rule 0.7 x h
                bloom=[], leaf=PLA_LEAF_SITE,                # "early spring or even in autumn" S7: no months
                colours=_pla_c(_sec_mix("727A4E", SEC["paper"], 0.15))),   # CORE green_mid
    "willow": dict(name="White willow", turkish="Ak söğüt", latin="Salix alba", layer="tree",
                   form="weeping", foliage="deciduous (not quoted)", status="keep",
                   h_range=(None, 30.0), h_m=15.0,           # "up to 30 m" S4
                   crown_m=10.5,                             # crown not found: rule 0.7 x h
                   bloom=[], leaf=PLA_LEAF_SITE,             # "spring" catkins S4: no months
                   colours=_pla_c(_sec_mix("8C9969", SEC["paper"], 0.3))),  # CORE green_light, silvered
    "olive": dict(name="Olive", turkish="Zeytin", latin="Olea europaea", layer="tree",
                  form="gnarled", foliage="evergreen (S72)", status="keep",
                  h_range=(8.0, 15.0), h_m=11.5,             # "8-15 m" S72
                  crown_m=10.35,                             # crown not found: rule 0.9 x h
                  bloom=[4], leaf=PLA_ALL_YEAR,              # full bloom 21-24 Apr, ends 29 Apr-1 May S73 (Ege Univ.)
                  colours=_pla_c(SEC["olive"])),             # section_style SEC olive
    "stone_pine": dict(name="Stone pine", turkish="Fıstık çamı", latin="Pinus pinea", layer="tree",
                       form="umbrella", foliage="evergreen conifer (S74)", status="keep (processionary caterpillar)",
                       h_range=(25.0, 30.0), h_m=27.5,       # "25-30 m" S74
                       crown_m=15.1,                         # "umbrella-shaped ... flat and broad" S74: rule 0.55 x h
                       bloom=[], leaf=PLA_ALL_YEAR,          # pollen months not found
                       colours=_pla_c(SEC["pine"])),         # section_style SEC pine
    "tamarisk": dict(name="Tamarisk", turkish="Ilgın", latin="Tamarix smyrnensis", layer="tree",
                     form="feathery", foliage="deciduous (S9b, genus)", status="keep (replaces oleander)",
                     h_range=(4.0, 15.0), h_m=9.5,           # "4-15 m" S9b (genus)
                     crown_m=7.6,                            # "broad, bushy" S9b: rule 0.8 x h
                     bloom=[], leaf=PLA_LEAF_SITE,           # bloom not found for T. smyrnensis
                     colours=_pla_c(_sec_mix("8C9969", SEC["paper"], 0.45))),  # CORE green_light, pale
    "chaste": dict(name="Chaste tree", turkish="Hayıt", latin="Vitex agnus-castus", layer="shrub",
                   form="multistem", foliage="deciduous (S58)", status="keep (replaces oleander, fig, citrus)",
                   h_range=(1.0, 3.0), h_m=2.0,              # "1-3 m" S58
                   crown_m=2.0,                              # "1.5-2.5 m" S67 (RHS, UK)
                   bloom=[6, 7, 8, 9], leaf=PLA_LEAF_SITE,   # "(Apr-)Jun-Sep" S58 (Crete); Apr-May occasional
                   colours=_pla_c(SEC["shrub"], SEC["lav"])),  # flower colour not sourced: section_style lav
    "rosemary": dict(name="Rosemary", turkish="Biberiye", latin="Salvia rosmarinus", layer="shrub",
                     form="mound", foliage="evergreen (S58, S71)", status="keep",
                     h_range=(0.5, 1.0), h_m=0.75,           # "50-100 cm" S58 (Crete)
                     crown_m=0.75,                           # "1.5-2.5 m" S71 for 1.5-2.5 m plants: scaled to h
                     bloom=[1, 2, 3, 4, 5], leaf=PLA_ALL_YEAR,  # "Jan-May, intermittently to Dec" S58
                     colours=_pla_c(_sec_mix("495338", SEC["paper"], 0.35))),  # CORE green_deep
    "lavender": dict(name="French lavender", turkish="Karabaş otu", latin="Lavandula stoechas", layer="ground",
                     form="mound", foliage="evergreen (UNVERIFIED)", status="keep",
                     h_range=(0.3, 0.8), h_m=0.55,           # "30-80 cm" S58
                     crown_m=0.66,                           # crown not found: rule 1.2 x h
                     bloom=[3, 4, 5], leaf=[],               # "Mar-May" S58; evergreen unverified: no leaf months
                     colours=_pla_c(_sec_mix(SEC["olive"], SEC["paper"], 0.1), SEC["lav"])),  # as sec_lavender
    "loosestrife": dict(name="Purple loosestrife", turkish="Aklar otu", latin="Lythrum salicaria", layer="emergent",
                        form="clump", foliage="herbaceous perennial", status="keep, flower heads cut in Sep (D6)",
                        h_range=(0.3, 2.4), h_m=1.35,        # "0.3-2.4 m" S19
                        crown_m=0.75,                        # "5 feet (1.5 m) wide" mature S19: half the maximum
                        bloom=[6, 7, 8, 9], leaf=[],         # "June ... September" S19; cut Sep (D6)
                        colours=_pla_c(SEC["grass"], PLA_PURPLE)),
    "soft_rush": dict(name="Soft rush", turkish="UNVERIFIED", latin="Juncus effusus", layer="emergent",
                      form="clump", foliage="not found", status="new (replaces iris and cattail)",
                      h_range=(0.5, 1.5), h_m=1.0,           # "5-15 dm tall" S59
                      crown_m=0.6,                           # "tufted, cespitose" S59: rule 0.6 x h
                      bloom=[5, 6, 7, 8], leaf=[],           # "late May-Aug, occasionally Sep" S59 (USA)
                      colours=_pla_c(SEC["reed"])),          # section_style SEC reed
    "rush": dict(name="Sharp rush", turkish="Kofa", latin="Juncus acutus", layer="emergent",
                 form="tussock", foliage="not found", status="keep, away from paths and the wading strip",
                 h_range=(0.6, 1.0), h_m=0.8,                # "(40-)60-100 cm" S65
                 crown_m=0.8,                                # "dense tussock" S60, S65: rule 1.0 x h
                 bloom=[], leaf=[],                          # "summer" S65 (NZ): no months
                 colours=_pla_c(_sec_mix(SEC["reed"], "495338", 0.3))),   # SEC reed toward CORE green_deep
    "reed": dict(name="Common reed", turkish="Kamış", latin="Phragmites australis", layer="emergent",
                 form="stand", foliage="deciduous (S2)", status="lined off-line basins only (D2 a): pla_reed_basin",
                 h_range=(None, 6.0), h_m=3.0,               # "may reach 20 feet (6 m)" S2 (booklet drew 1.9-2.2 m)
                 crown_m=None,                               # clonal stand, no crown
                 bloom=[7, 8, 9, 10, 11], leaf=[],           # "July to November" S2 (range-wide); plumes cut before Nov
                 colours=_pla_c(SEC["reed"], SEC["reed_head"])),
    "mint": dict(name="Water mint", turkish="Su nanesi", latin="Mentha aquatica", layer="emergent",
                 form="mound", foliage="deciduous (S57)", status="lined basin cells only (D6): pla_mint_cell",
                 h_range=(0.3, 0.8), h_m=0.55,               # "30-80 cm" S58
                 crown_m=0.75,                               # "spread 0.5-1 m" S57
                 bloom=[5, 6, 7, 8, 9], leaf=[],             # "May-Sep" S58
                 colours=_pla_c(SEC["grass"])),              # section_style SEC grass
    "giant_reed": dict(name="Giant reed", turkish="Kargı", latin="Arundo donax", layer="emergent",
                       form="cane", foliage="not found", status="REMOVE (raises flood risk, S36)",
                       h_range=(None, None), h_m=None, crown_m=None,   # not in species_data: pass h_m and crown_m
                       bloom=[], leaf=[],
                       colours=_pla_c(SEC["beyond"], PLA_REMOVE)),
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


def _pla_cols(sp, beyond):
    c = dict(sp["colours"])
    if beyond:                                  # beyond the cut: paler (as SEC beyond)
        c = dict((k_, _sec_mix(v, SEC["paper"], 0.55) if v else v) for k_, v in c.items())
    return c


def _pla_sec(form, x, gy, h, w, k, c, seed=0):
    """Section silhouette of one form, h tall and w crown wide (m), ground at (x, gy) page mm."""
    import math as _m
    H, R = h * k, w / 2.0 * k
    f, e, lt, st, ac = c["fill"], c["edge"], c["lt"], c["stem"], c.get("accent")
    sh = []
    if form in ("dome", "oval", "weeping", "gnarled", "umbrella"):
        lo = dict(dome=0.3, oval=0.3, weeping=0.25, gnarled=0.3, umbrella=0.65)[form] * H   # clear stem (rule)
        tw = max(0.15, h / 60.0 * k)            # half trunk width: trunk 1/30 of the height (rule)
        yb, yt = gy + lo, gy + H
        Hc = yt - yb
        if form == "gnarled":                   # two twisting stems
            for s_ in (-1, 1):
                sh.append(("poly", [(x + s_ * 0.2 * tw, gy), (x + s_ * 1.6 * tw, gy),
                                    (x + s_ * (0.35 * R + tw * 0.5), yb + 0.3 * Hc),
                                    (x + s_ * (0.35 * R - tw * 0.5), yb + 0.3 * Hc)], st, None, 0.1))
        else:
            lean = 0.03 * H if form == "umbrella" else 0.0
            sh.append(("poly", [(x - tw, gy), (x + tw, gy), (x + lean + tw * 0.6, yb + 0.4 * Hc),
                                (x + lean - tw * 0.6, yb + 0.4 * Hc)], st, None, 0.1))
        if form == "weeping":                   # the hanging curtain behind the crown
            c0 = yb + 0.45 * Hc
            sh.append(("poly", [(x - R, c0), (x - 0.9 * R, gy + 0.2 * H), (x + 0.9 * R, gy + 0.2 * H), (x + R, c0)],
                       lt, None, 0.1))
        if form == "gnarled":                   # low and wide: three irregular masses
            for cx_, cy_, rx_, up_, i in ((x - 0.5 * R, yb + 0.4 * Hc, 0.5 * R, 0.4 * Hc, 0),
                                          (x + 0.5 * R, yb + 0.45 * Hc, 0.5 * R, 0.4 * Hc, 1),
                                          (x, yb + 0.62 * Hc, 0.55 * R, 0.38 * Hc, 2)):
                dn_ = cy_ - yb if i < 2 else 0.38 * Hc
                sh.append(("poly", _pla_crown(cx_, cy_, rx_, up_, dn_, seed + i, 0.18), f, e, 0.08))
        else:
            fr = dict(dome=(0.3, 0.06), oval=(0.5, 0.08), weeping=(0.45, 0.05), umbrella=(0.35, 0.04))[form]
            c0 = yb + fr[0] * Hc
            sh.append(("poly", _pla_crown(x, c0, R, yt - c0, c0 - yb, seed, fr[1]), f, e, 0.08))
            for i, (dx, dy, s_) in enumerate(((-0.4, 0.3, 0.32), (0.35, 0.15, 0.3), (-0.05, 0.6, 0.26))):
                sh.append(("poly", _pla_crown(x + dx * R, c0 + dy * (yt - c0), s_ * R, s_ * (yt - c0) * 0.8,
                                              s_ * (yt - c0) * 0.6, seed + i + 1, 0.1), lt, None, 0.1))
        if form == "weeping":                   # strands
            for i in range(9):
                xs = x - 0.85 * R + i * 1.7 * R / 8.0
                s_ = -1 if xs < x else 1
                yh = gy + (0.2 + 0.08 * _pla_rnd(i, seed)) * H
                y0 = yb + 0.3 * Hc
                sh.append(("line", [(xs, y0), (xs + s_ * 0.04 * R, (y0 + yh) / 2.0), (xs + s_ * 0.06 * R, yh)], e, 0.1))
        if form in ("dome", "oval"):            # a few branches
            for s_, a in ((-1, 55.0), (1, 45.0), (1, 75.0)):
                r_ = _m.radians(a)
                sh.append(("line", [(x, yb + 0.3 * Hc), (x + s_ * _m.cos(r_) * R * 0.5, yb + (0.3 + 0.4 * _m.sin(r_))
                                                         * Hc)], st, max(0.08, tw * 0.5)))
        return sh
    if form == "feathery":                      # tamarisk: slender stems, an airy crown, hanging wisps
        for i in range(4):
            sh.append(("line", [(x + (i - 1.5) * 0.04 * R, gy), (x + (i - 1.5) * 0.3 * R, gy + 0.55 * H)], st, 0.15))
        c0 = gy + 0.55 * H
        ring = _pla_crown(x, c0, R, 0.45 * H, 0.4 * H, seed, 0.14)
        sh.append(("poly", ring, f, None, 0.1))
        for i in range(0, len(ring), 2):
            px, py = ring[i]
            if py > c0 - 0.3 * H:
                sh.append(("line", [(px, py), (px + (px - x) * 0.04, py - 0.1 * H)], e, 0.08))
        return sh
    if form == "multistem":                     # chaste tree: stems fanning from the ground, heads at their ends
        heads = ((-0.7, 0.6, 0.25), (-0.35, 0.68, 0.27), (0.0, 0.72, 0.28), (0.35, 0.66, 0.27), (0.7, 0.58, 0.25))
        for dx, cy_, ry_ in heads:
            sh.append(("line", [(x + dx * 0.1 * R, gy), (x + dx * R, gy + cy_ * H)], st, 0.15))
        for i, (dx, cy_, ry_) in enumerate(heads):
            sh.append(("poly", _pla_crown(x + dx * R, gy + cy_ * H, 0.3 * R, ry_ * H, ry_ * H * 0.8, seed + i, 0.12),
                       f, e, 0.06))
        if ac:
            for dx, cy_, ry_ in heads:
                top = gy + (cy_ + ry_) * H
                sh.append(("line", [(x + dx * R, top - 0.14 * H), (x + dx * R, top - 0.01 * H)], ac, 0.3))
        return sh
    if form == "mound":                         # lavender, rosemary, water mint: a low dome on the ground
        sh.append(("poly", _pla_crown(x, gy + 0.35 * H, R, 0.65 * H, 0.35 * H, seed, 0.1), f, e, 0.06))
        if ac:                                  # flower spikes in the top of the mound
            for d in (-0.5, -0.2, 0.15, 0.45):
                sh.append(("line", [(x + d * R, gy + 0.72 * H), (x + d * R * 1.1, gy + 0.97 * H)], ac, 0.25))
        else:
            for d in (-0.55, -0.25, 0.05, 0.35, 0.6):
                sh.append(("line", [(x + d * R, gy + 0.35 * H), (x + d * R * 1.05, gy + 0.7 * H)], lt, 0.1))
        return sh
    if form in ("clump", "tussock", "cane"):    # rushes and loosestrife: stems from one base; giant reed: canes
        n = dict(clump=13, tussock=21, cane=7)[form]
        for i in range(n):
            t = i / float(n - 1)
            hh = H * (0.82 + 0.18 * _pla_rnd(i, seed + 3))
            bx, tx = x + (2 * t - 1) * R * 0.15, x + (2 * t - 1) * R
            if form == "clump":                 # soft arch
                mx = bx + (tx - bx) * 0.35
                sh.append(("line", [(bx, gy), (mx, gy + 0.55 * hh), (tx, gy + hh)], f, 0.12))
                if ac and i % 2 == 0:           # loosestrife flower spike on the upper stem
                    sh.append(("line", [(mx + (tx - mx) * 0.3, gy + 0.69 * hh), (tx, gy + hh)], ac, 0.35))
            else:
                sh.append(("line", [(bx, gy), (tx, gy + hh)], f, 0.15 if form == "cane" else 0.1))
                if form == "cane":              # leaf blades along the cane
                    for j in range(1, 5):
                        py = gy + hh * j / 5.0
                        px = bx + (tx - bx) * j / 5.0
                        s_ = 1 if (i + j) % 2 else -1
                        sh.append(("line", [(px, py), (px + s_ * 0.35 * R, py - 0.06 * hh)], f, 0.1))
        if form == "cane" and ac:               # marked for removal
            sh.append(("line", [(x - R, gy), (x + R, gy + H)], ac, 0.35))
            sh.append(("line", [(x - R, gy + H), (x + R, gy)], ac, 0.35))
        return sh
    raise ValueError("_pla_sec: unknown form %r" % form)


def _pla_scallop(cx, cy, r, m, depth, n=72):
    """A scalloped circle of radius r (its bumps reach r), m bumps."""
    import math as _m
    return [(cx + r * (1.0 - depth * _m.sin(m * a / 2.0) ** 2) * _m.cos(a),
             cy + r * (1.0 - depth * _m.sin(m * a / 2.0) ** 2) * _m.sin(a))
            for a in [2 * _m.pi * i / n for i in range(n)]]


def _pla_plan(form, cx, cy, w, k, c, seed=0):
    """Top view of one form, crown w wide (m), centre (cx, cy) page mm."""
    import math as _m
    r = w / 2.0 * k
    f, e, lt, st, ac = c["fill"], c["edge"], c["lt"], c["stem"], c.get("accent")
    sh = []
    dot = ("poly", sec_ellipse(cx, cy, max(0.2, 0.04 * r), max(0.2, 0.04 * r), 10), st, None, 0.1)
    if form in ("dome", "oval"):
        m, dp, s_ = (10, 0.1, 0.3) if form == "dome" else (16, 0.06, 0.22)
        sh.append(("poly", _pla_scallop(cx, cy, r, m, dp), f, e, 0.08))
        for i in range(3 if form == "dome" else 4):
            a = 2 * _m.pi * (i / (3.0 if form == "dome" else 4.0) + _pla_rnd(seed, 4))
            sh.append(("poly", _pla_scallop(cx + 0.45 * r * _m.cos(a), cy + 0.45 * r * _m.sin(a), s_ * r, 6, 0.12),
                       lt, None, 0.1))
        return sh + [dot]
    if form == "weeping":
        sh.append(("poly", _pla_scallop(cx, cy, r, 24, 0.04), f, e, 0.08))
        for i in range(20):
            a = 2 * _m.pi * i / 20.0
            sh.append(("line", [(cx + 0.25 * r * _m.cos(a), cy + 0.25 * r * _m.sin(a)),
                                (cx + 0.95 * r * _m.cos(a), cy + 0.95 * r * _m.sin(a))], e, 0.08))
        return sh + [dot]
    if form == "gnarled":                       # three masses, as in section
        for i in range(3):
            a = 2 * _m.pi * (0.25 + i / 3.0)
            sh.append(("poly", _pla_crown(cx + 0.45 * r * _m.cos(a), cy + 0.45 * r * _m.sin(a), 0.55 * r, 0.55 * r,
                                          0.55 * r, seed + i, 0.18), f, e, 0.08))
        return sh + [dot]
    if form == "umbrella":                      # flat disc with needle tufts at the rim
        sh.append(("poly", _pla_scallop(cx, cy, r, 30, 0.03), f, e, 0.08))
        for i in range(30):
            a = 2 * _m.pi * i / 30.0
            sh.append(("line", [(cx + 0.75 * r * _m.cos(a), cy + 0.75 * r * _m.sin(a)),
                                (cx + 0.96 * r * _m.cos(a), cy + 0.96 * r * _m.sin(a))], lt, 0.1))
        return sh + [dot]
    if form == "feathery":
        sh.append(("poly", _pla_crown(cx, cy, r, r, r, seed, 0.14), f, None, 0.1))
        for i in range(28):
            a = 2 * _m.pi * i / 28.0
            sh.append(("line", [(cx + 0.82 * r * _m.cos(a), cy + 0.82 * r * _m.sin(a)),
                                (cx + 0.82 * r * _m.cos(a + 0.12), cy + 0.82 * r * _m.sin(a + 0.12))], e, 0.08))
        return sh + [dot]
    if form == "multistem":                     # five heads, as in section
        for i in range(5):
            a = 2 * _m.pi * (i / 5.0 + 0.05)
            hx, hy = cx + 0.55 * r * _m.cos(a), cy + 0.55 * r * _m.sin(a)
            sh.append(("poly", _pla_crown(hx, hy, 0.45 * r, 0.45 * r, 0.45 * r, seed + i, 0.12), f, e, 0.06))
            if ac:
                sh.append(("poly", sec_ellipse(hx, hy, 0.08 * r, 0.08 * r, 8), ac, None, 0.1))
        return sh
    if form == "mound":
        sh.append(("poly", _pla_crown(cx, cy, r, r, r, seed, 0.1), f, e, 0.06))
        for i in range(6):
            a = 2 * _m.pi * (i / 6.0 + _pla_rnd(seed, 6))
            px, py = cx + 0.5 * r * _m.cos(a), cy + 0.5 * r * _m.sin(a)
            if ac:
                sh.append(("poly", sec_ellipse(px, py, 0.12 * r, 0.12 * r, 8), ac, None, 0.1))
            else:
                sh.append(("line", [(px, py), (px + 0.2 * r * _m.cos(a), py + 0.2 * r * _m.sin(a))], lt, 0.1))
        return sh
    if form in ("clump", "tussock", "cane"):    # stems seen from above: a starburst
        n = dict(clump=13, tussock=21, cane=9)[form]
        for i in range(n):
            a = 2 * _m.pi * (i / float(n) + 0.3 * _pla_rnd(i, seed))
            ll = r * (0.8 + 0.2 * _pla_rnd(i, seed + 2))
            sh.append(("line", [(cx, cy), (cx + ll * _m.cos(a), cy + ll * _m.sin(a))], f, 0.12))
            if ac and form == "clump" and i % 2 == 0:
                sh.append(("poly", sec_ellipse(cx + ll * _m.cos(a), cy + ll * _m.sin(a), 0.08 * r + 0.1,
                                               0.08 * r + 0.1, 8), ac, None, 0.1))
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


def pla_section(key, x, gy, k, h_m=None, crown_m=None, beyond=False, seed=0):
    """A species in section at true size: ground at (x, gy) page mm (gy may be a function of x)."""
    sp = _pla_get(key)
    h, w = _pla_size(key, sp, h_m, crown_m)
    return _pla_sec(sp["form"], x, gy(x) if callable(gy) else gy, h, w, k, _pla_cols(sp, beyond), seed)


def pla_plan(key, cx, cy, k, crown_m=None, beyond=False, seed=0):
    """The same species from above: crown crown_m wide (m) centred on (cx, cy) page mm, same form and colour."""
    sp = _pla_get(key)
    w = crown_m or sp["crown_m"]
    if w is None:
        raise ValueError("plants: %s has no sourced crown: pass crown_m" % key)
    return _pla_plan(sp["form"], cx, cy, w, k, _pla_cols(sp, beyond), seed)


def _pla_crop_size(crop, h_m, crown_m):
    if crop == "olive":                         # orchard trees kept to their in-row spacing (rule); h by the olive ratio
        w = crown_m or PLA_CROPS["olive"]["plant_m"]
        return h_m or w / PLA_FORM_RATIO["gnarled"], w
    if h_m is None or crown_m is None:
        raise ValueError("plants: %s plant size is not sourced: pass h_m and crown_m" % crop)
    return h_m, crown_m


def _pla_crop_sec(crop, x, gy, h, w, k, i, beyond):
    """One crop plant in section."""
    if crop == "olive":
        return _pla_sec("gnarled", x, gy, h, w, k, _pla_cols(PLA_SPECIES["olive"], beyond), i)
    H, R = h * k, w / 2.0 * k
    c = _pla_cols(dict(colours=_pla_c(SEC["grass"])), beyond)
    if crop == "maize":                         # stalk, arching leaves, tassel
        sh = [("line", [(x, gy), (x, gy + H)], c["fill"], 0.2)]
        for j in range(1, 7):
            py, s_ = gy + H * (0.15 + 0.11 * j), (1 if j % 2 else -1)
            sh.append(("line", [(x, py), (x + s_ * R * 0.6, py + 0.08 * H), (x + s_ * R, py - 0.02 * H)], c["fill"],
                       0.12))
        sh.append(("line", [(x, gy + 0.92 * H), (x, gy + H)], SEC["reed_head"], 0.35))
        return sh
    if crop == "cotton":                        # small branched bush with open bolls
        sh = [("line", [(x, gy), (x, gy + 0.5 * H)], c["stem"], 0.12),
              ("poly", _pla_crown(x, gy + 0.55 * H, R, 0.45 * H, 0.3 * H, i, 0.15), c["fill"], c["edge"], 0.06)]
        for d, e_ in ((-0.5, 0.6), (0.1, 0.85), (0.55, 0.55)):
            sh.append(("poly", sec_ellipse(x + d * R, gy + e_ * H, 0.1 * R + 0.1, 0.1 * R + 0.1, 8), PLA_BOLL,
                       c["edge"], 0.05))
        return sh
    if crop == "tomato":                        # low sprawling plant with fruit
        sh = [("poly", _pla_crown(x, gy + 0.3 * H, R, 0.7 * H, 0.3 * H, i, 0.15), c["fill"], c["edge"], 0.06)]
        for d, e_ in ((-0.45, 0.35), (0.2, 0.5), (0.6, 0.3)):
            sh.append(("poly", sec_ellipse(x + d * R, gy + e_ * H, 0.08 * R + 0.1, 0.08 * R + 0.1, 8), PLA_FRUIT,
                       None, 0.1))
        return sh
    raise ValueError("plants: unknown crop %r" % crop)


def pla_crop_rows(crop, x0, x1, gy, k, spacing=None, h_m=None, crown_m=None, beyond=False):
    """Crop plants along a cut from x0 to x1 (page mm), spacing m apart (the row spacing for a cut across the rows;
    sourced default only for olive), centred in the stretch; gy a number or a function of x."""
    if crop not in PLA_CROPS:
        raise ValueError("plants: unknown crop %r" % crop)
    sp = spacing or PLA_CROPS[crop]["row_m"]
    if sp is None:
        raise ValueError("plants: %s row spacing is not sourced: pass spacing (m)" % crop)
    h, w = _pla_crop_size(crop, h_m, crown_m)
    n = int((x1 - x0) / (sp * k) + 1e-9)
    off = ((x1 - x0) - n * sp * k) / 2.0
    sh = []
    for i in range(n + 1):
        x = x0 + off + i * sp * k
        sh += _pla_crop_sec(crop, x, gy(x) if callable(gy) else gy, h, w, k, i, beyond)
    return sh


def _pla_ring(rr):
    """A ring from a ring or an (x0, y0, x1, y1) rectangle (page mm)."""
    if len(rr) == 4 and not isinstance(rr[0], (tuple, list)):
        x0, y0, x1, y1 = rr
        return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return list(rr)


def pla_crop_plan(crop, ring_or_rect, k, row_spacing=None, plant_spacing=None, ang_deg=0.0, crown_m=None,
                  field=True):
    """A field or orchard block in plan: rows at row_spacing (m) at ang_deg; with plant_spacing, single plants along
    each row (true crown with crown_m or for olive, else a fixed 0.25 mm dot). Sourced defaults only for olive."""
    import math as _m
    if crop not in PLA_CROPS:
        raise ValueError("plants: unknown crop %r" % crop)
    ring = _pla_ring(ring_or_rect)
    rs = row_spacing or PLA_CROPS[crop]["row_m"]
    ps = plant_spacing or PLA_CROPS[crop]["plant_m"]
    if rs is None:
        raise ValueError("plants: %s row spacing is not sourced: pass row_spacing (m)" % crop)
    sh = [("poly", ring, PLA_FIELD, None, 0.1)] if field else []
    w = crown_m or (PLA_CROPS["olive"]["plant_m"] if crop == "olive" else None)   # olive: crown = in-row spacing
    for i, (p, q) in enumerate(sec_hatch(ring, rs * k, ang_deg)):
        if ps is None:
            sh.append(("line", [p, q], PLA_ROW, 0.15))
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
                sh += _pla_plan("gnarled", px, py, w, k, _pla_cols(PLA_SPECIES["olive"], False), i * 31 + j)
            elif w:
                sh.append(("poly", _pla_crown(px, py, w / 2.0 * k, w / 2.0 * k, w / 2.0 * k, i * 31 + j, 0.12),
                           SEC["grass"], SEC["ink2"], 0.05))
            else:
                sh.append(("poly", sec_ellipse(px, py, 0.125, 0.125, 8), PLA_ROW, None, 0.1))
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


def pla_reed_basin(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m=0.15, media_m=None, wl_y=None, h_m=None, step_m=None):
    """Common reed in a lined, root-contained, off-line basin (D2 a) in section: inside x0-x1, floor bed_y, rim rim_y
    (page mm). kerb_t_m 0.15 m and floor slab = drawing rule; stems step_m apart."""
    sp = PLA_SPECIES["reed"]
    sh, g = _pla_lined(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m, media_m, wl_y)
    h = h_m or sp["h_m"]
    st = (step_m or 1.0 / 3.0) * k              # 9 seedlings/m² (Korkusuz et al. 2004, S20) = 1/3 m apart
    c = sp["colours"]
    i, x = 0, x0 + st / 2.0
    while x < x1:
        hh = h * k * (0.8 + 0.2 * _pla_rnd(i, 5))
        lean = 0.04 * hh * (1 if i % 2 else -1)
        sh.append(("line", [(x, g), (x + lean, g + hh)], c["fill"], 0.12))
        if i % 3 == 0:                          # plume (cut before seed release in Nov, S11)
            ry = 0.2 * k + 0.2
            sh.append(("poly", sec_ellipse(x + lean, g + hh - ry, 0.06 * k + 0.1, ry, 10), c["accent"], None, 0.1))
        x += st
        i += 1
    return sh + _pla_liner(x0, x1, bed_y, rim_y, k, kerb_h_m)


def pla_mint_cell(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m=0.15, media_m=None, wl_y=None, h_m=None, crown_m=None):
    """Water mint only in a lined basin cell (D6) in section, same build as pla_reed_basin; mounds side by side."""
    sp = PLA_SPECIES["mint"]
    sh, g = _pla_lined(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m, media_m, wl_y)
    h, w = h_m or sp["h_m"], crown_m or sp["crown_m"]
    n = max(1, int((x1 - x0) / (w * k)))
    for i in range(n):
        sh += _pla_sec("mound", x0 + (i + 0.5) * (x1 - x0) / n, g, h, min(w, (x1 - x0) / n / k), k,
                       sp["colours"], i)
    return sh + _pla_liner(x0, x1, bed_y, rim_y, k, kerb_h_m)


def pla_cell_plan(kind, ring_or_rect, k, kerb_t_m=0.15):
    """A lined cell in plan, kind 'reed' or 'mint': wet ground, the kerb as a band kerb_t_m wide, the plants."""
    import math as _m
    if kind not in ("reed", "mint"):
        raise ValueError("pla_cell_plan: kind is 'reed' or 'mint'")
    ring = _pla_ring(ring_or_rect)
    sp = PLA_SPECIES[kind]
    sh = [("poly", ring, PLA_WET, None, 0.1)]
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    if kind == "reed":                          # stems on the 1/3 m grid, never denser than 0.9 mm on the page
        d = max(0.9, k / 3.0)
        c = sp["colours"]["fill"]
        for i in range(int((max(xs) - min(xs)) / d) + 1):
            for j in range(int((max(ys) - min(ys)) / d) + 1):
                px = min(xs) + (i + 0.5 * (j % 2) + 0.25) * d
                py = min(ys) + (j + 0.5) * d
                if _sct_inside(ring, (px, py)):
                    sh.append(("line", [(px - 0.2 * d, py - 0.25 * d), (px + 0.2 * d, py + 0.25 * d)], c, 0.1))
    else:
        w = sp["crown_m"] * k
        for i in range(int((max(xs) - min(xs)) / w) + 1):
            for j in range(int((max(ys) - min(ys)) / w) + 1):
                px, py = min(xs) + (i + 0.5) * w, min(ys) + (j + 0.5) * w
                if _sct_inside(ring, (px, py)):
                    sh += _pla_plan("mound", px, py, sp["crown_m"] * 0.9, k, sp["colours"], i * 7 + j)
    sh.append(("poly", ring, None, SCT["line"], max(0.15, kerb_t_m * k)))
    return sh
# ---- the booklet's one icon set (02_SHARED_SYSTEMS §2, WO-T2b-1): every symbol drawn on one 24-unit square grid,
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
}

ICO_NAMES = tuple(ICO_COL.keys())


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
def bergama_data(name, _c={}):
    """Built-in data kept in Downloads/Bergama/Data/bergama_water_board_data.py (Aras 25 Oct 21:29, scripts shortened): runs its
    section `name` here, as if it were written in this place. The file is read once per run; a missing file or one
    from another version of this script stops the script with a message saying which file to copy."""
    import os as _os, hashlib as _hl
    if not _c:
        p_ = _os.path.join(_os.path.expanduser("~"), "Downloads", "Bergama", "Data", "bergama_water_board_data.py")
        if not _os.path.isfile(p_):
            raise RuntimeError("Data file missing: copy bergama_water_board_data.py from the run kit's Data folder into " + _os.path.dirname(p_))
        with open(p_, encoding="utf-8", newline="") as f_:
            for part_ in f_.read().split("\n#@@ ")[1:]:
                k_, _, b_ = part_.partition("\n")
                _c[k_] = b_
    b_ = _c.get(name)
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != {'LEVELS': 'a217c1d07ff06bcb3cd55255c619aa7c', 'CUTS': '34548cb4690d944460505d2cd484311f', 'SPECIES': 'b3a8e35120cba4e926a9a4fad2c63ab1', 'SKETCH_SRC': 'e84f58206f857080352e1723882a3930', 'DETAIL_SRC': '87908363d2a4d472bbfcbd0320614960'}.get(name):
        raise RuntimeError("Data file bergama_water_board_data.py is not the one made with this script version (part " + name +
                           "): copy it again from the same run kit as the script")
    exec(compile(b_, "bergama_water_board_data.py:" + name, "exec"), globals())


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
    """the row dict of cut (crossing) cid; KeyError naming the known ids"""
    for r in _lv_rows():
        if r["id"] == cid:
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
    "detailed": dict(stream=True, streets=True, buildings=True, green=True, trees=True, fields=True, contours=True),
    "simple": dict(stream=True, streets="faint", buildings="faint", green=False, trees=False, fields=False,
                   contours=False),
    "minimal": dict(stream=True, streets=("main", "lane"), buildings="veryfaint", green=False, trees=False,
                    fields=False, contours=False),
    "topographic": dict(stream=True, streets=False, buildings="faint", green=False, trees=False, fields=False,
                        contours="height"),
}
_BM_MEMO = {}


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
    basemap_layers("minimal", {"streets": ("main",), "buildings": False}) for D5 Sound b (stream + main roads)"""
    if mode not in BASEMAP_MODES:
        raise ValueError(u"basemap mode '{}' unknown: one of {}".format(mode, ", ".join(sorted(BASEMAP_MODES))))
    lay = dict(BASEMAP_MODES[mode])
    for k, v in (override or {}).items():
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


def basemap_items(mode="detailed", override=None, box=None, D=None, split_buildings=False):
    """the basemap of a drawing as items (bottom first; see the head of this file), in survey m. mode: "detailed",
    "simple", "minimal", "topographic" (02 §1); override: layer changes for this drawing (basemap_layers); box =
    (x0, y0, x1, y1) survey m: only what touches it (the caller clips to its frame); split_buildings=True gives
    every building its own fill item (for a page that fills even-odd only; default: nonzero fills in chunks).
    [] without data."""
    D = D if D is not None else basemap_load()
    if not D:
        return []
    # the same request in one run is made once and copied (Aras 29 Oct 19:18: build once, cache, copy the layers)
    mk = ("items", id(D), mode, repr(sorted((override or {}).items())), tuple(box) if box else None,
          bool(split_buildings))
    if mk in _BM_MEMO:
        return list(_BM_MEMO[mk])
    _BM_MEMO[mk] = _bm_items(D, mode, override, box, split_buildings)
    return list(_BM_MEMO[mk])


def _bm_items(D, mode, override, box, split_buildings):
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
    # the stream: ONE drawing (the site board's water and its edge inside the frame, OpenStreetMap's course beyond)
    if lay["stream"]:
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
    if bl:
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
    if lay["stream"] and (st is True or bl is True):
        lines(L["bridges"], BM_COL["ink"], BM_LW["bridge"])
    return out


def basemap_draw(items, T, fill_fn, line_fn, text_fn=None):
    """draws items through the caller's page: T(p) survey m -> page point; fill_fn(rings, hex, alpha, nonzero);
    line_fn(pts, hex, width_mm, dash_mm, alpha); text_fn(s, (x, y), size_mm, hex, bold, align) (texts are left out
    without it). Returns the number of items drawn."""
    n = 0
    for it in items:
        if it[0] == "fill":
            fill_fn([[T(p) for p in R] for R in it[1]], it[2], it[3], it[4])
        elif it[0] == "line":
            line_fn([T(p) for p in it[1]], it[2], it[3], it[4], it[5])
        elif it[0] == "text" and text_fn is not None:
            text_fn(it[1], T(it[2]), it[3], it[4], it[5], it[6])
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

        def in_ring(p):
            u, v = loc(p)
            return ex[0] <= u <= ex[2] and ex[1] <= v <= ex[3] and not (fr[0] <= u <= fr[2] and fr[1] <= v <= fr[3])
        L = dict(lc={}, zones=[], contours=[], street_areas=[], street_edges=[], streets_in=[], streets_out=[],
                 water=[], water_edge=[], decks=[], covered=[], water_out=[], waterways_out=[], buildings=[],
                 bridges=[])
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
        for u in S.bld:
            parts = [_bm_r(P) for P in u["parts"] if len(P) >= 3]
            if parts:
                L["buildings"].append(dict(rings=parts + [_bm_r(H) for H in (u.get("holes") or [])], np=len(parts),
                                           her=u.get("fabric") in ("monument", "sacred"),
                                           osm=u.get("src") in ("osm", "osm+label")))
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
                            L["buildings"].append(dict(rings=[_bm_r(P[:-1])], np=1, her=her, osm=True))
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


def sec_put(pg, shapes):
    """Draws section_style shapes on this board's Page."""
    for sh in shapes:
        if sh[0] == "poly":
            pg.poly([sh[1]], fill=sh[2], stroke=sh[3], lw=sh[4])
        else:
            pg.line(sh[1], sh[2], sh[3])


def arrow(pg, P, col, lw, head=2.2, dash=None):
    """A polyline with a filled head at its end."""
    if len(P) < 2:
        return
    (x0, y0), (x1, y1) = P[-2], P[-1]
    L = math.hypot(x1 - x0, y1 - y0)
    if L < 1e-6:
        return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    if L > head * 1.1 or len(P) > 2:
        body = list(P[:-1]) + [(x1 - ux * head * 0.8, y1 - uy * head * 0.8)]
        pg.line(body, col, lw, dash, cap=0)
    bx, by = x1 - ux * head, y1 - uy * head
    w = head * 0.45
    pg.poly([[(x1, y1), (bx - uy * w, by + ux * w), (bx + uy * w, by - ux * w)]], fill=col)


# The masterplan's regular hand-drawn link arrow, as water loop v1.2 draws it (bergama_masterplan_v8 G: marker shaft
# 2.0 mm, barbs 5.84 mm at 38 deg and 1.6 mm, serifs 2.8 mm at 0.4 mm, wobble 0.175 mm over 15 mm; Aras 18 Oct 15:38;
# the standard since 24 Oct, CONFLICTS.md row 5), in paper mm.
HA = dict(shaft=2.0, barb=5.84, ang=38.0, barb_w=1.6, serif=2.8, serif_w=0.4, over=0.64, amp=0.175, wav=15.2)


def hand_arrow(pg, P, kind="water", small=1.0, cols=None):
    """A bold hand arrow along P: water in the river tones, high water (flood) lighter and dashed; cols = (shaft, head)
    for another colour (v1.12: the red closing arrow of the decision loop)."""
    shaft_c, head_c = cols or ((MP["amphibious"][1], MP["amphibious"][2]) if kind == "flood" else
                               (MP["discharge"][1], MP["discharge"][2]))
    seg = [math.hypot(P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1]) for i in range(len(P) - 1)]
    Lt = sum(seg)
    if Lt < 1e-6:
        return
    k = min(small, Lt / (HA["barb"] * 2.0))
    barb, bw, aw = HA["barb"] * k, HA["barb_w"] * max(0.6, k), HA["shaft"] * max(0.6, k)

    def at(t):                                   # point and unit direction at arc length t
        for i, d in enumerate(seg):
            if t <= d or i == len(seg) - 1:
                u = min(max(t / max(d, 1e-9), 0.0), 1.0)
                ux, uy = (P[i + 1][0] - P[i][0]) / max(d, 1e-9), (P[i + 1][1] - P[i][1]) / max(d, 1e-9)
                return (P[i][0] + ux * d * u, P[i][1] + uy * d * u), (ux, uy)
            t -= d
    seed = int(abs(P[0][0] * 7.3 + P[0][1] * 3.1 + P[-1][0] * 1.7)) % 997
    ph1, ph2 = seed * 0.37, seed * 0.91
    n = max(2, int((Lt - barb * 0.25) / 0.5) + 1)
    sh = []
    for j in range(n):
        t = (Lt - barb * 0.25) * j / (n - 1)
        (x, y), (ux, uy) = at(t)
        w = HA["amp"] * 0.5 * (math.sin(2 * math.pi * t / HA["wav"] + ph1) +
                               0.6 * math.sin(2 * math.pi * t / (HA["wav"] * 0.43) + ph2))
        sh.append((x - uy * w, y + ux * w))
    pg.line(sh, shaft_c, aw, [1.6, 0.9] if kind == "flood" else None, cap=1)
    (tx, ty), _ = at(Lt)
    (bx, by), _ = at(max(0.0, Lt - barb * 0.8))
    d = math.hypot(tx - bx, ty - by) or 1.0
    dx, dy = (tx - bx) / d, (ty - by) / d
    for sg in (1, -1):
        a = math.radians(HA["ang"]) * sg
        vx, vy = dx * math.cos(a) - dy * math.sin(a), dx * math.sin(a) + dy * math.cos(a)
        ex, ey = tx - vx * barb, ty - vy * barb
        pg.line([(tx + vx * HA["over"] * k, ty + vy * HA["over"] * k), (ex, ey)], head_c, bw, cap=1)
        h = HA["serif"] * k / 2
        pg.line([(ex - vy * h, ey + vx * h), (ex + vy * h, ey - vx * h)], head_c, HA["serif_w"], cap=1)


def node(pg, x, y, n, opt, r=3.2):
    """Element number (the old card numbers, 1-11, on every drawing): a roundel in A, a square in B."""
    d = COL["river_dark"] if n != 10 else COL["ink"]
    if opt == "A":
        pg.circle(x, y, r, fill=COL["white"], stroke=d, lw=0.3)
        pg.circle(x, y, r * 0.74, fill=d)
    else:
        s = r * 0.92
        pg.poly([[(x - s, y - s), (x + s, y - s), (x + s, y + s), (x - s, y + s)]], fill=COL["white"], stroke=d,
                lw=0.3)
        s *= 0.74
        pg.poly([[(x - s, y - s), (x + s, y - s), (x + s, y + s), (x - s, y + s)]], fill=d)
    fs = r * (0.82 if n < 10 else 0.66)
    pg.text(str(n), x, y - fs * CAP / 2, fs, COL["white"], bold=True, align="C")
    return (x - r, y - r, x + r, y + r)


def para(pg, x, y, w, text, size, colour, bold=False, lh=1.28):
    for ln in wrap(text, size, w, bold):
        y -= size * lh
        pg.text(ln, x, y, size, colour, bold=bold)
    return y
# v4 (MIRAQUA 28 Oct, PLAN §2): the round's shared definitions (styles, units, figures, label placing)
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
# ---- P19.2 / P15.2 (MIRAQUA round 28 Oct 2026): ONE set of architectural human figures ---------------------------
# Silhouettes at true scale (an adult 1.75 m) for every section and diagram that shows people (pp.14, 15, 19 and the
# p.15 occupancy diagram), replacing the stick figures and pictograms. Each pose is a skeleton (joints in metres,
# feet at y = 0, facing +x); fig_polys() turns it into filled outlines: a round-ended band per limb, the torso, the
# head. Draw every outline of a figure filled in one opaque colour (the section's ink or a lane colour), no stroke:
# the overlaps then read as one silhouette. Coordinates in metres; the caller scales them like the drawing.
FIG_LIMB = dict(arm=0.085, fore=0.07, thigh=0.15, shin=0.105, foot=0.07, neck=0.10)
FIG_POSES = {
    # standing, seen from the front
    "stand": dict(head=(0.0, 1.635, 0.105), torso=[(-0.2, 1.46), (0.2, 1.46), (0.17, 1.2), (0.155, 0.93), (-0.155, 0.93), (-0.17, 1.2)],
                  limbs=[("arm", (-0.185, 1.42), (-0.215, 1.13)), ("fore", (-0.215, 1.13), (-0.225, 0.84)),
                         ("arm", (0.185, 1.42), (0.215, 1.13)), ("fore", (0.215, 1.13), (0.225, 0.84)),
                         ("thigh", (-0.085, 0.95), (-0.095, 0.5)), ("shin", (-0.095, 0.5), (-0.095, 0.07)),
                         ("foot", (-0.095, 0.035), (-0.16, 0.035)),
                         ("thigh", (0.085, 0.95), (0.095, 0.5)), ("shin", (0.095, 0.5), (0.095, 0.07)),
                         ("foot", (0.095, 0.035), (0.16, 0.035)), ("neck", (0.0, 1.44), (0.0, 1.54))]),
    # walking, side view
    "walk": dict(head=(0.035, 1.635, 0.105), torso=[(-0.1, 1.45), (0.11, 1.45), (0.12, 1.2), (0.1, 0.92), (-0.12, 0.92), (-0.12, 1.2)],
                 limbs=[("thigh", (0.0, 0.95), (-0.09, 0.53)), ("shin", (-0.09, 0.53), (-0.27, 0.13)),
                        ("foot", (-0.29, 0.1), (-0.13, 0.035)),
                        ("thigh", (0.0, 0.95), (0.13, 0.52)), ("shin", (0.13, 0.52), (0.19, 0.08)),
                        ("foot", (0.15, 0.035), (0.33, 0.035)),
                        ("arm", (0.0, 1.41), (-0.1, 1.15)), ("fore", (-0.1, 1.15), (-0.17, 0.9)),
                        ("arm", (0.0, 1.41), (0.1, 1.15)), ("fore", (0.1, 1.15), (0.2, 0.92)),
                        ("neck", (0.0, 1.44), (0.02, 1.54))]),
    # standing, side view, pointing / watching forward
    "watch": dict(head=(0.03, 1.635, 0.105), torso=[(-0.11, 1.45), (0.11, 1.45), (0.12, 1.2), (0.1, 0.92), (-0.12, 0.92), (-0.12, 1.2)],
                  limbs=[("thigh", (0.0, 0.95), (0.02, 0.5)), ("shin", (0.02, 0.5), (0.0, 0.08)),
                         ("foot", (-0.03, 0.035), (0.16, 0.035)),
                         ("thigh", (-0.02, 0.95), (-0.06, 0.5)), ("shin", (-0.06, 0.5), (-0.08, 0.08)),
                         ("foot", (-0.11, 0.035), (0.08, 0.035)),
                         ("arm", (0.0, 1.41), (0.02, 1.13)), ("fore", (0.02, 1.13), (0.05, 0.86)),
                         ("arm", (0.02, 1.41), (0.22, 1.42)), ("fore", (0.22, 1.42), (0.45, 1.5)),
                         ("neck", (0.0, 1.44), (0.02, 1.54))]),
    # sitting on a step or bench (seat at 0.45 m under the hip), side view
    "sit": dict(head=(0.03, 1.215, 0.105), torso=[(-0.1, 1.03), (0.11, 1.03), (0.12, 0.8), (0.11, 0.48), (-0.12, 0.48), (-0.12, 0.8)],
                limbs=[("thigh", (0.0, 0.52), (0.44, 0.52)), ("shin", (0.44, 0.52), (0.47, 0.08)),
                       ("foot", (0.44, 0.035), (0.62, 0.035)),
                       ("arm", (0.0, 0.99), (0.08, 0.74)), ("fore", (0.08, 0.74), (0.3, 0.62)),
                       ("neck", (0.0, 1.02), (0.02, 1.12))]),
    # crouching at the edge, a hand down to the water, side view
    "touch": dict(head=(0.36, 1.0, 0.105), torso=[(0.12, 0.98), (0.3, 0.9), (0.24, 0.66), (0.02, 0.42), (-0.12, 0.5), (-0.02, 0.8)],
                  limbs=[("thigh", (-0.04, 0.47), (0.24, 0.5)), ("shin", (0.24, 0.5), (0.14, 0.08)),
                         ("foot", (0.1, 0.035), (0.29, 0.035)),
                         ("arm", (0.2, 0.9), (0.36, 0.64)), ("fore", (0.36, 0.64), (0.48, 0.3)),
                         ("neck", (0.22, 0.92), (0.3, 0.96))]),
    # wading: short steps, arms out for balance, side view
    "wade": dict(head=(0.03, 1.635, 0.105), torso=[(-0.11, 1.45), (0.11, 1.45), (0.12, 1.2), (0.1, 0.92), (-0.12, 0.92), (-0.12, 1.2)],
                 limbs=[("thigh", (0.0, 0.95), (0.07, 0.51)), ("shin", (0.07, 0.51), (0.1, 0.08)),
                        ("foot", (0.06, 0.035), (0.24, 0.035)),
                        ("thigh", (0.0, 0.95), (-0.05, 0.51)), ("shin", (-0.05, 0.51), (-0.12, 0.09)),
                        ("foot", (-0.15, 0.04), (0.02, 0.035)),
                        ("arm", (0.0, 1.41), (0.15, 1.2)), ("fore", (0.15, 1.2), (0.32, 1.12)),
                        ("arm", (0.0, 1.41), (-0.15, 1.2)), ("fore", (-0.15, 1.2), (-0.3, 1.1)),
                        ("neck", (0.0, 1.44), (0.02, 1.54))]),
    # cycling (bike way), side view; wheels as rings
    "bike": dict(head=(0.3, 1.56, 0.105), torso=[(0.05, 1.42), (0.23, 1.46), (0.18, 1.2), (-0.12, 0.95), (-0.26, 1.02), (-0.08, 1.28)],
                 limbs=[("thigh", (-0.2, 0.98), (0.12, 0.8)), ("shin", (0.12, 0.8), (0.02, 0.38)),
                        ("foot", (-0.02, 0.36), (0.12, 0.36)),
                        ("arm", (0.15, 1.42), (0.3, 1.2)), ("fore", (0.3, 1.2), (0.45, 1.06)),
                        ("neck", (0.18, 1.44), (0.26, 1.5)),
                        ("frame", (-0.55, 0.34), (-0.2, 0.9)), ("frame", (-0.2, 0.9), (0.0, 0.34)),
                        ("frame", (0.0, 0.34), (-0.55, 0.34)), ("frame", (-0.2, 0.9), (0.42, 0.92)),
                        ("frame", (0.0, 0.34), (0.42, 0.92)), ("frame", (0.42, 0.92), (0.55, 0.34)),
                        ("frame", (0.42, 0.92), (0.46, 1.06))],
                 rings=[(-0.55, 0.34, 0.34), (0.55, 0.34, 0.34)]),
}
FIG_ORDER = ("stand", "walk", "watch", "sit", "touch", "wade", "bike")


def _fig_band(p, q, w, n=5):
    """the outline of a band of width w from p to q with round ends"""
    import math as _m
    dx, dy = q[0] - p[0], q[1] - p[1]
    a = _m.atan2(dy, dx)
    r = w / 2.0
    out = []
    for c, a0 in ((q, a - _m.pi / 2), (p, a + _m.pi / 2)):
        for i in range(n + 1):
            t = a0 + _m.pi * i / n
            out.append((c[0] + r * _m.cos(t), c[1] + r * _m.sin(t)))
    return out


def _fig_circle(cx, cy, r, n=16):
    import math as _m
    return [(cx + r * _m.cos(2 * _m.pi * i / n), cy + r * _m.sin(2 * _m.pi * i / n)) for i in range(n)]


def fig_polys(pose, height=1.75, facing=1):
    """filled outlines of one figure, in metres, feet at (0, 0): pose = a FIG_POSES key; height 1.75 = adult (a child
    about 1.15, the head kept a little larger); facing -1 = mirrored (looking left)"""
    P = FIG_POSES[pose]
    k = height / 1.75
    hk = k ** 0.7 / k if k < 1.0 else 1.0               # a child's head is relatively larger
    f = 1.0 if facing >= 0 else -1.0

    def T(pt):
        return (f * pt[0] * k, pt[1] * k)
    out = [[T(p) for p in P["torso"]]]
    for kind, p, q in P["limbs"]:
        w = FIG_LIMB.get(kind, 0.035)
        out.append(_fig_band(T(p), T(q), w * k))
    for cx, cy, r in P.get("rings", ()):
        ring = _fig_circle(cx, cy, r, 20)
        for i in range(len(ring)):
            out.append(_fig_band(T(ring[i]), T(ring[(i + 1) % len(ring)]), 0.035 * k, 2))
    hx, hy, hr = P["head"]
    out.append(_fig_circle(f * hx * k, hy * k, hr * k * hk))
    return out


# ---- A1 scale figures (29 Oct 2026, Aras: family A1 "gestural pen", the R20 language) --------------------------------
# ONE figure API for every drawing: fig_side / fig_top / fig_meta. Shapes are house shapes ("poly", ring, fill, stroke,
# lw) in the caller's units (k units per metre, y up), feet at (x, y). Two sources:
#  1. the curated A1 library (24 figures of the R20 sheet and Studio Articulation Sketchy Human Figures 2 + 3) read
#     from Downloads/Bergama/Data/figures_A1.json. Licences forbid redistributing those drawings, so they are NOT in
#     this public repo; the file ships in the run kit's Data/ folder (project library/figures_A1/).
#  2. figures drawn here in the same pen language for the poses the sets lack (wade, sit_step, bike, adult_child,
#     stall, railing, olive, touch, and every plan view). Each one is posed by its contact: the step, rail, counter,
#     water or branch it touches is a parameter, and the limbs are solved to reach it.
# Adult 1.70 m. Body proportions = Drillis & Contini (1966) segment ratios of stature (as reproduced in Winter,
# Biomechanics and Motor Control of Human Movement, Fig. 4.1; page not re-checked): FIG_DC below.
# No library file -> the drawn figures stand in for stand/walk/watch/lean/sit_chair (never nothing).
FIG_A1_H = 1.70
FIG_A1_INK = "2B2B2B"
FIG_A1_PEN = 0.019              # m: pen width = the median stroke of the curated library at 1.70 m
FIG_PEN_MIN_MM = 0.10           # page mm: no figure line prints thinner (small scales get an outline)
FIG_DC = dict(chin=0.870, shoulder=0.818, elbow=0.630, wrist=0.485, hip=0.530, knee=0.285, ankle=0.039,
              upper_arm=0.186, forearm=0.146, hand=0.108, thigh=0.245, shank=0.246, foot=0.152,
              shoulder_w=0.259, hip_w=0.191)
FIG_CHILD_H = 1.15              # m, the project's child figure (fig_polys docstring)
FIG_BIKE = dict(wheel_r=0.336,  # 622 mm rim (ISO 5775 "700C") + 2 x 25 mm tyre = 672 mm: calculated
                wheelbase=1.00, crank=0.17, bb_h=0.27)  # drawing values (typical city bike), not sourced
FIG_LOG = []
_FIG_LIB = {}


def fig_library():
    """the curated A1 library (dict id -> figure) or {} when Downloads/Bergama/Data/figures_A1.json is missing"""
    import os as _o
    import json as _j
    if "lib" in _FIG_LIB:
        return _FIG_LIB["lib"]
    lib = {}
    root = _o.path.join(_o.path.expanduser("~"), "Downloads", "Bergama", "Data")
    for p in (_o.path.join(root, "figures_A1.json"), _o.path.join(root, "figures", "figures_A1.json")):
        if _o.path.exists(p):
            try:
                with open(p, "r") as fh:
                    lib = _j.load(fh).get("figures", {})
                FIG_LOG.append(u"Figures: %d A1 figures from %s" % (len(lib), p))
                break
            except Exception as ex:
                FIG_LOG.append(u"Figures: %s unreadable (%s); drawn figures used" % (p, type(ex).__name__))
    if not lib:
        FIG_LOG.append(u"Figures: Data/figures_A1.json not found; drawn A1 figures used for every pose")
    _FIG_LIB["lib"] = lib
    return lib


def _fa_rand(seed):
    s = [int(seed * 7919 + 17) & 0x7fffffff]

    def r():
        s[0] = (s[0] * 1103515245 + 12345) & 0x7fffffff
        return s[0] / float(0x7fffffff) - 0.5
    return r


def _fa_smooth(P, n=2):
    for _ in range(n):
        if len(P) < 3:
            return P
        Q = [P[0]]
        for a, b in zip(P[:-1], P[1:]):
            Q += [(0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]), (0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1])]
        Q.append(P[-1])
        P = Q
    return P


def _fa_stroke(P, rnd, w=FIG_A1_PEN, over=0.06, wob=0.008, smooth=True):
    """one pen stroke through P (m) as a closed ring: a little overshoot at both ends, a slight wobble, the width
    tapering to a third at the ends (the expanded-brush look of the A1 sets)"""
    import math as _m
    P = [(p[0] + wob * rnd(), p[1] + wob * rnd()) for p in P]
    if len(P) >= 2:
        for i0, i1 in ((0, 1), (-1, -2)):
            a, b = P[i0], P[i1]
            d = _m.hypot(a[0] - b[0], a[1] - b[1]) or 1.0
            e = over * (0.6 + rnd())
            P[i0] = (a[0] + (a[0] - b[0]) * e, a[1] + (a[1] - b[1]) * e)     # overshoot = e x the end segment
    if smooth:
        P = _fa_smooth(P)
    n = len(P)
    if n < 2:
        return None
    L, R = [], []
    for i in range(n):
        a, b = P[max(0, i - 1)], P[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = _m.hypot(dx, dy) or 1.0
        t = i / float(n - 1)
        h = 0.5 * w * (0.33 + 0.67 * _m.sin(_m.pi * t) ** 0.5)
        L.append((P[i][0] - dy / d * h, P[i][1] + dx / d * h))
        R.append((P[i][0] + dy / d * h, P[i][1] - dx / d * h))
    return L + R[::-1]


def _fa_oval(cx, cy, rx, ry, rnd, gap=0.9, a0=1.9, w=FIG_A1_PEN):
    """an open pen oval (head, wheel): starts at a0 rad, stops gap rad short of closing"""
    import math as _m
    n = 16
    P = [(cx + rx * _m.cos(a0 + (2 * _m.pi - gap) * i / n), cy + ry * _m.sin(a0 + (2 * _m.pi - gap) * i / n))
         for i in range(n + 1)]
    return _fa_stroke(P, rnd, w, over=0.02, wob=0.004, smooth=False)


def _fa_ik(a, b, l1, l2, bend):
    """2-link reach from a to b (segment lengths l1, l2): the middle joint, bent to the side bend (+1 left of a->b);
    out of reach -> straight towards b"""
    import math as _m
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = _m.hypot(dx, dy) or 1e-9
    if d >= l1 + l2:
        return (a[0] + dx / d * l1, a[1] + dy / d * l1), (a[0] + dx / d * (l1 + l2), a[1] + dy / d * (l1 + l2))
    c = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)
    t = _m.acos(max(-1.0, min(1.0, c)))
    a0 = _m.atan2(dy, dx) + bend * t
    return (a[0] + l1 * _m.cos(a0), a[1] + l1 * _m.sin(a0)), b


class _FaBody(object):
    """a side-view body facing +x, h tall: joints from FIG_DC; hip/shoulder positions set by the pose"""

    def __init__(self, h=FIG_A1_H, hip=None, lean=0.0):
        import math as _m
        self.h, D = h, FIG_DC
        self.L = dict((k, v * h) for k, v in D.items())
        self.hip = hip or (0.0, D["hip"] * h)
        t = (D["shoulder"] - D["hip"]) * h
        self.sho = (self.hip[0] + t * _m.sin(lean), self.hip[1] + t * _m.cos(lean))
        self.lean = lean
        hh = (1.0 - D["shoulder"]) * h
        self.hr = (0.040 * h, 0.060 * h)      # the A1 head: a small upright oval; its top at stature when upright
        self.head = (self.sho[0] + 0.45 * hh * _m.sin(lean) + 0.02 * h,
                     self.sho[1] + (hh - self.hr[1]) * _m.cos(lean))

    def leg(self, ankle, bend=1):
        return _fa_ik(self.hip, ankle, self.L["thigh"], self.L["shank"], bend)

    def arm(self, hand, bend=-1, s=None):
        return _fa_ik(s or self.sho, hand, self.L["upper_arm"], self.L["forearm"] + 0.3 * self.L["hand"], bend)


def _fa_clip(P, cut_y):
    """the part of polyline P above cut_y (from its first point down)"""
    if cut_y is None:
        return P
    Q = []
    for a, b in zip(P[:-1], P[1:]):
        if a[1] < cut_y:
            break
        Q.append(a)
        if b[1] < cut_y:
            t = (a[1] - cut_y) / (a[1] - b[1])
            Q.append((a[0] + t * (b[0] - a[0]), cut_y))
            return Q
    else:
        Q.append(P[-1])
    return Q


def _fa_off(P, d):
    """P offset sideways by d (left of its direction), point by point"""
    import math as _m
    out = []
    for i in range(len(P)):
        a, b = P[max(0, i - 1)], P[min(len(P) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = _m.hypot(dx, dy) or 1.0
        dd = d[i] if isinstance(d, (list, tuple)) else d
        out.append((P[i][0] - dy / n * dd, P[i][1] + dx / n * dd))
    return out


def _fa_draw(B, legs, arms, rnd, w=FIG_A1_PEN, hatch=True, hem=None, coat=0.0, cut_y=None):
    """pen strokes of one body in the R20 manner: small open head oval; the coat as two contour strokes falling from
    the neck over round shoulders to the hem, a hem/belt stroke overshooting both sides; each leg as two contour
    strokes tapering to the ankle with a short foot tick; arms as single strokes; one-sided diagonal hatch on the
    back. legs/arms: [(knee, ankle)], [(elbow, hand)]. cut_y: nothing below it (water)."""
    import math as _m
    out = []
    hx, hy = B.head
    out.append(_fa_oval(hx, hy, B.hr[0], B.hr[1], rnd, w=w))
    s, p = B.sho, B.hip
    c, sn = _m.cos(B.lean), _m.sin(B.lean)
    dep = 0.095 * B.h                                   # half chest depth, side view
    hem_y = hem if hem is not None else p[1] - coat
    neck = (s[0] - 0.02 * sn + 0.01, s[1] + 0.035 * B.h * c)

    def T(u, v):                                        # torso frame: u across (+ = front), v up from the hip
        return (p[0] + u * c + v * sn, p[1] - u * sn + v * c)
    tl = (s[1] - p[1]) / max(c, 0.3)
    hv = (hem_y - p[1]) / max(c, 0.3)
    back = [neck, T(-0.75 * dep, tl - 0.01), T(-1.0 * dep, tl - 0.10), T(-0.95 * dep, 0.45 * tl), T(-0.92 * dep, hv)]
    front = [(neck[0] + 0.03, neck[1] - 0.01), T(0.70 * dep, tl - 0.03), T(0.95 * dep, tl - 0.16), T(0.80 * dep, 0.45 * tl),
             T(0.90 * dep, hv)]
    out += [_fa_stroke(back, rnd, w), _fa_stroke(front, rnd, w * 0.85)]
    out.append(_fa_stroke([T(-1.15 * dep, hv + 0.01), T(1.20 * dep, hv - 0.005)], rnd, w * 0.9, over=0.12))
    if hatch:
        for i in range(5):
            v = tl - 0.12 - (tl - 0.12 - hv) * (0.12 + 0.17 * i)
            a0 = T(-0.88 * dep, v)
            out.append(_fa_stroke([a0, (a0[0] + 0.08, a0[1] + 0.12)], rnd, w * 0.6, over=0.0, wob=0.003, smooth=False))
    for e, hnd in arms:
        out.append(_fa_stroke([(s[0] + 0.01, s[1] - 0.03), e, hnd], rnd, w))
    lw0 = 0.055 * B.h                                   # half leg width at the hip
    for i, (kn, an) in enumerate(legs):
        P = [p, kn, an]
        for side in ((1, -1) if i == 0 else (-1,)):     # the far leg: its back contour only
            Q = _fa_off(P, [side * lw0, side * 0.6 * lw0, side * 0.12 * lw0])
            Q = _fa_clip(Q, cut_y)
            if len(Q) >= 2:
                out.append(_fa_stroke(Q, rnd, w * (1.0 if side > 0 else 0.85)))
        if cut_y is None or an[1] > cut_y:
            out.append(_fa_stroke([(an[0] - 0.02, an[1] - B.L["ankle"] * 0.6), (an[0] + 0.6 * B.L["foot"], an[1] - B.L["ankle"])],
                                  rnd, w, over=0.1, smooth=False))
    return [r for r in out if r]


def _fa_side(pose, seed=0, **p):
    """(rings in m, feet at (0, 0), facing +x; anchors) of a drawn pose"""
    import math as _m
    rnd = _fa_rand(seed + 3)
    H = p.get("h_m", FIG_A1_H)
    D = FIG_DC
    an = {}
    if pose in ("stand", "watch", "walk", "wade"):
        st = 0.0 if pose in ("stand", "watch") else 0.32 * H * (0.7 if pose == "wade" else 1.0)
        B = _FaBody(H, lean=0.03 if pose == "walk" else 0.0)
        A = D["ankle"] * H
        legs = [B.leg((0.5 * st, A)), B.leg((-0.5 * st, A))]
        w_ = D["wrist"] * H
        if pose == "watch":
            arms = [B.arm((0.05, w_)), B.arm((0.42 * H * 0.6, D["shoulder"] * H + 0.02))]
        elif pose == "wade":
            arms = [B.arm((0.20, w_ + 0.10)), B.arm((-0.12, w_ + 0.08))]
        else:
            arms = [B.arm((0.18 * st, w_)), B.arm((-0.25 * st, w_))]
        cut = None
        if pose == "wade":
            cut = p.get("depth_m", D["knee"] * H)
            an["water_y"] = cut
        R = _fa_draw(B, legs, arms, rnd, coat=0.05, cut_y=cut)
        if cut is not None:                         # the water closing round the legs: two short ripple strokes
            for lx_ in (-0.5 * st, 0.5 * st):
                R.append(_fa_stroke([(lx_ - 0.14, cut), (lx_ + 0.16, cut)], rnd, FIG_A1_PEN * 0.7, over=0.1))
        return R, an
    if pose == "sit_step":
        seat = p.get("seat_h", 0.45)                # step riser the figure sits on (m above the tread the feet rest on)
        hip = (0.0, seat + 0.09)                    # hip joint about 9 cm above the seat (drawing value)
        B = _FaBody(H, hip=hip, lean=0.10)
        A = D["ankle"] * H
        kn, ank = B.leg((0.40 * H * 0.62, A), bend=1)
        legs = [(kn, ank), B.leg((0.36 * H * 0.62, A), bend=1)]
        arms = [B.arm((kn[0] - 0.04, kn[1] - 0.02)), B.arm((kn[0] - 0.10, kn[1] - 0.06))]
        R = _fa_draw(B, legs, arms, rnd, hem=seat + 0.02)
        an.update(seat_x=0.15, seat_y=seat)         # the step nosing: under the thighs, in front of the hip
        return R, an
    if pose == "touch":                             # crouching at the edge, one hand down to the water
        A = D["ankle"] * H
        hip = (-0.12, 0.30 * H * 0.75)
        B = _FaBody(H, hip=hip, lean=0.85)
        legs = [B.leg((0.12, A), bend=1), B.leg((0.02, A), bend=1)]
        reach = p.get("reach_y", -0.10)             # hand height (m; below the feet = over the edge)
        arms = [B.arm((B.sho[0] + 0.25, reach), bend=1), B.arm((hip[0] + 0.30, hip[1] + 0.05))]
        an["hand"] = arms[0][1]
        return _fa_draw(B, legs, arms, rnd, hatch=False, coat=0.0), an
    if pose in ("stall", "railing", "olive"):
        A = D["ankle"] * H
        if pose == "railing":
            rh = p.get("rail_h", 1.10)
            sh_y = rh + D["upper_arm"] * H * 0.92     # forearms flat on the rail, upper arm nearly vertical
            t = (D["shoulder"] - D["hip"]) * H
            lean = _m.acos(max(0.4, min(1.0, (sh_y - D["hip"] * H) / t)))
            B = _FaBody(H, lean=lean)
            el = (B.sho[0] + 0.05, rh + 0.02)
            hand = (el[0] + D["forearm"] * H + 0.04, rh + 0.03)
            arms = [(el, hand), ((el[0] - 0.03, el[1] - 0.01), (hand[0] - 0.05, hand[1] - 0.01))]
            legs = [B.leg((-0.04, A)), B.leg((-0.16, A))]
            an.update(rail_x=el[0] + 0.12, rail_y=rh)
            return _fa_draw(B, legs, arms, rnd, coat=0.04), an
        if pose == "stall":
            ch = p.get("counter_h", 0.90)
            B = _FaBody(H, lean=0.12)
            arms = [B.arm((B.sho[0] + 0.48, ch + 0.06), bend=-1), B.arm((-0.02, D["wrist"] * H))]
            legs = [B.leg((0.06, A)), B.leg((-0.12, A))]
            an.update(counter_x=0.30, counter_y=ch)
            R = _fa_draw(B, legs, arms, rnd, coat=0.06)
            bx, by = arms[1][1]                     # a market bag in the other hand
            R.append(_fa_stroke([(bx - 0.10, by), (bx - 0.12, by - 0.30), (bx + 0.12, by - 0.31), (bx + 0.10, by)], rnd,
                                FIG_A1_PEN * 0.8, over=0.05))
            return R, an
        bh = p.get("branch_h", 1.90)                # olive picking: both hands up to the branch (top reach ~1.92 m)
        B = _FaBody(H, lean=-0.06)
        rl = (D["upper_arm"] + D["forearm"] + 0.3 * D["hand"]) * H
        top = B.sho[1] + (max(0.0, rl ** 2 - 0.32 ** 2)) ** 0.5
        hy = min(bh, top)
        arms = [B.arm((B.sho[0] + 0.32, hy), bend=-1), B.arm((B.sho[0] + 0.22, hy - 0.06), bend=-1)]
        legs = [B.leg((0.10, A)), B.leg((-0.14, A))]
        an.update(hand_x=arms[0][1][0], hand_y=arms[0][1][1], reached=arms[0][1][1] >= bh - 0.02)
        return _fa_draw(B, legs, arms, rnd, coat=0.04), an
    if pose == "bike":
        F = FIG_BIKE
        r, wb, cr, bb = F["wheel_r"], F["wheelbase"], F["crank"], F["bb_h"]
        rear, front, bbp = (-0.5 * wb, r), (0.5 * wb, r), (-0.05, bb)
        legl = (D["thigh"] + D["shank"]) * H
        # saddle: the leg reaches 96 % of its length to the lowest pedal (nearly straight at the bottom of the stroke)
        hip = (bbp[0] - 0.24, bb - cr + 0.04 + _m.sqrt((0.96 * legl) ** 2 - 0.24 ** 2))
        bar = (front[0] - 0.12, hip[1] + 0.06)
        B = _FaBody(H, hip=hip, lean=0.62)
        out = [_fa_oval(rear[0], rear[1], r, r, rnd, gap=0.5, a0=0.3), _fa_oval(front[0], front[1], r, r, rnd, gap=0.5, a0=3.4)]
        out += [_fa_stroke(P, rnd, FIG_A1_PEN * 0.75, over=0.04) for P in (
            [rear, bbp, (hip[0] + 0.02, hip[1] - 0.08)], [(hip[0] + 0.02, hip[1] - 0.10), (bar[0] - 0.05, bar[1] - 0.10), front],
            [bbp, (bar[0] - 0.05, bar[1] - 0.10)], [rear, (hip[0] + 0.02, hip[1] - 0.10)],
            [(hip[0] - 0.10, hip[1] - 0.04), (hip[0] + 0.10, hip[1] - 0.03)], [(bar[0] - 0.05, bar[1] - 0.10), bar])]
        ang = 0.5
        pa = (bbp[0] + cr * _m.cos(ang), bbp[1] - cr * _m.sin(ang) * 1.0)
        pb = (bbp[0] - cr * _m.cos(ang), bbp[1] + cr * _m.sin(ang))
        legs = [B.leg((pa[0] - 0.05, pa[1] + 0.04), bend=1), B.leg((pb[0] - 0.05, pb[1] + 0.04), bend=1)]
        arms = [B.arm(bar, bend=-1)]
        out += _fa_draw(B, legs, arms, rnd, hatch=False, coat=0.0)
        an.update(length=wb + 2 * r)
        return [o for o in out if o], an
    if pose == "adult_child":                       # walking hand in hand: the hands meet where both reach
        ch = p.get("child_h", FIG_CHILD_H)
        A = FIG_DC["ankle"]
        Ba = _FaBody(H, lean=0.03)
        st = 0.30 * H
        hand = (0.20, D["wrist"] * H + 0.06)
        legs = [Ba.leg((0.5 * st, A * H)), Ba.leg((-0.5 * st, A * H))]
        R = _fa_draw(Ba, legs, [Ba.arm(hand, bend=-1), Ba.arm((-0.12, D["wrist"] * H))], rnd, coat=0.05)
        Bc = _FaBody(ch, hip=(0.42, D["hip"] * ch), lean=0.02)
        stc = 0.30 * ch
        legs = [Bc.leg((0.42 + 0.5 * stc, A * ch)), Bc.leg((0.42 - 0.5 * stc, A * ch))]
        R += _fa_draw(Bc, legs, [Bc.arm(hand, bend=1), Bc.arm((0.46, D["wrist"] * ch))], _fa_rand(seed + 11),
                      w=FIG_A1_PEN * 0.85, hatch=False, coat=0.03)
        an.update(hand=hand, child_h=ch)
        return R, an
    return None, an


def _fa_top(pose, seed=0, **p):
    """plan figures, m, centred on (0, 0), heading +x: open shoulder oval, small head oval, one-sided hatch"""
    rnd = _fa_rand(seed + 5)
    H = p.get("h_m", FIG_A1_H)
    sw, dp = FIG_DC["shoulder_w"] * H, 0.15 * H

    def one(cx, cy, s=1.0, hatch=True):
        o = [_fa_oval(cx, cy, 0.5 * dp * s, 0.5 * sw * s, rnd, gap=0.7, a0=2.4),
             _fa_oval(cx + 0.03 * s, cy, 0.07 * s, 0.065 * s, rnd, gap=1.0, a0=0.5)]
        if hatch:
            for i in range(3):
                y = cy - 0.12 * s + 0.08 * s * i
                o.append(_fa_stroke([(cx - 0.10 * s, y), (cx - 0.04 * s, y + 0.06 * s)], rnd, FIG_A1_PEN * 0.6, over=0.0, smooth=False))
        return o
    if pose in ("stand", "watch"):
        R = one(0.0, 0.0)
    elif pose == "walk":
        R = one(0.0, 0.0) + [_fa_stroke([(0.18, 0.08), (0.30, 0.09)], rnd), _fa_stroke([(-0.20, -0.08), (-0.10, -0.08)], rnd)]
    elif pose in ("sit", "sit_step", "sit_chair"):
        t = FIG_DC["thigh"] * H
        R = one(-0.05, 0.0) + [_fa_stroke([(0.02, 0.09), (0.02 + t, 0.10)], rnd), _fa_stroke([(0.02, -0.09), (0.02 + t, -0.10)], rnd)]
    elif pose == "bike":
        F = FIG_BIKE
        L = 0.5 * F["wheelbase"]
        R = one(-0.05, 0.0, hatch=False) + [_fa_stroke([(-L - F["wheel_r"], 0.0), (-L + F["wheel_r"], 0.0)], rnd, FIG_A1_PEN * 1.6),
                                            _fa_stroke([(L - F["wheel_r"], 0.0), (L + F["wheel_r"], 0.0)], rnd, FIG_A1_PEN * 1.6),
                                            _fa_stroke([(-L, 0.0), (L - 0.12, 0.0)], rnd, FIG_A1_PEN * 0.8),
                                            _fa_stroke([(L - 0.12, -0.24), (L - 0.12, 0.24)], rnd, FIG_A1_PEN * 0.8)]
    elif pose == "adult_child":
        ch = p.get("child_h", FIG_CHILD_H) / H
        R = one(0.0, 0.20) + one(0.0, -0.22, s=ch, hatch=False) + [_fa_stroke([(0.02, 0.0), (0.04, -0.06)], rnd, FIG_A1_PEN * 0.8)]
    else:
        return None
    return [r for r in R if r]


FIG_DRAWN_SIDE = ("stand", "walk", "watch", "wade", "sit_step", "touch", "stall", "railing", "olive", "bike", "adult_child")
FIG_DRAWN_TOP = ("stand", "watch", "walk", "sit", "sit_step", "sit_chair", "bike", "adult_child")
FIG_POSE_ALIAS = {"sit": "sit_step"}


def _fig_pick(pose, pick):
    lib = fig_library()
    if pose in lib:
        return lib[pose]
    ids = sorted(k for k, f in lib.items() if f.get("pose") == pose)
    return lib[ids[pick % len(ids)]] if ids else None


def fig_meta(pose, facing=1, pick=0, **p):
    """anchors of a figure in m relative to its feet (x mirrored for facing -1): wade water_y; sit_step seat_x,
    seat_y; railing rail_x, rail_y; stall counter_x, counter_y; olive hand_x, hand_y, reached; touch hand;
    adult_child hand, child_h; bike length; lean (library) ledge_y_m. Use them to place the step, rail, counter or
    water the figure touches."""
    pose = FIG_POSE_ALIAS.get(pose, pose)
    f = None if pose in ("wade", "sit_step", "touch", "stall", "railing", "olive", "bike", "adult_child") else _fig_pick(pose, pick)
    an = dict(f.get("anchor") or {}) if f else _fa_side(pose, pick, **p)[1]
    s = 1.0 if facing >= 0 else -1.0
    for k_ in list(an):
        v = an[k_]
        if k_.endswith("_x"):
            an[k_] = s * v
        elif isinstance(v, tuple):
            an[k_] = (s * v[0], v[1])
    return an


def fig_side(pose, x, y, k, facing=1, ink=None, pick=None, mm_per_m=None, pen_min_mm=FIG_PEN_MIN_MM, **p):
    """side-view figure, feet at (x, y), k units per m, facing -1 = mirrored. pose: a library id (e.g.
    "a1_group_child"), a library pose (stand, walk, watch, lean, sit_chair; pick (default: from x, y) = which one, cycling),
    or a drawn pose (wade depth_m, sit_step seat_h, touch reach_y, stall counter_h, railing rail_h, olive branch_h,
    bike, adult_child child_h = hand in hand; the library's family group is "a1_group_child"). Library figures face as drawn (their "facing" in the file); facing flips them so they
    look the asked way. mm_per_m: printed page mm per metre (default k, the house convention); where the pen
    (0.019 m) would print thinner than pen_min_mm, every stroke gets an outline of the difference (lw in page mm).
    Returns house shapes ("poly", ring, ink, stroke, lw)."""
    pose = FIG_POSE_ALIAS.get(pose, pose)
    ink = ink or FIG_A1_INK
    if pick is None:                                   # variety: the place picks the figure, the same every run
        pick = int(abs(x * 7.31 + y * 3.17) * 10.0) % 997
    rings, flip = None, 1.0 if facing >= 0 else -1.0
    drawn_only = ("wade", "sit_step", "touch", "stall", "railing", "olive", "bike", "adult_child")
    if pose not in drawn_only:
        f = _fig_pick(pose, pick)
        if f:
            rings = f["rings"]
            if f.get("facing", 0) < 0:
                flip = -flip
    if rings is None:
        rings = _fa_side(pose if pose in FIG_DRAWN_SIDE else ("watch" if pose == "lean" else "stand"), pick, **p)[0]
    if not rings:                                      # never nothing: the legacy silhouette
        rings = fig_polys(pose if pose in FIG_POSES else "stand", FIG_A1_H, 1)
    add = max(0.0, pen_min_mm - FIG_A1_PEN * (mm_per_m or k))
    return [("poly", [(x + flip * px * k, y + py * k) for px, py in r], ink, ink if add > 0 else None, add)
            for r in rings]


def fig_top(pose, x, y, k, ang=0.0, ink=None, pick=0, mm_per_m=None, pen_min_mm=FIG_PEN_MIN_MM, **p):
    """plan figure centred on (x, y), heading ang (radians, 0 = +x), k units per m: stand, watch, walk, sit,
    sit_step, sit_chair, bike, adult_child (child_h). Same pen and mm_per_m rule as fig_side."""
    import math as _m
    ink = ink or FIG_A1_INK
    rings = _fa_top(FIG_POSE_ALIAS.get(pose, pose), pick, **p) or _fa_top("stand", pick)
    ca, sa = _m.cos(ang), _m.sin(ang)
    add = max(0.0, pen_min_mm - FIG_A1_PEN * (mm_per_m or k))
    return [("poly", [(x + (px * ca - py * sa) * k, y + (px * sa + py * ca) * k) for px, py in r], ink,
             ink if add > 0 else None, add) for r in rings]
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


def lp_leader_end(b, p):
    """the point of box b nearest p (where a leader from p meets the label)"""
    return (min(max(p[0], b[0]), b[2]), min(max(p[1], b[1]), b[3]))


def label_spot(ax, ay, w, h, taken, bounds=None, segs=(), pad=0.5,
               rings=(0.8, 2.5, 5.0, 8.0, 12.0, 17.0, 24.0), n_ang=16):
    """a free box w x h near (ax, ay): (box, leader) or None. taken: placed boxes and symbol boxes; segs: important
    lines [(p, q)] a label may not sit on. leader = True when the box sits off the point (draw a thin leader)."""
    import math as _m

    def free(b):
        if bounds and not (bounds[0] <= b[0] and b[2] <= bounds[2] and bounds[1] <= b[1] and b[3] <= bounds[3]):
            return False
        if any(lp_hit(b, t, pad) for t in taken):
            return False
        return not any(_lp_seg_box(p, q, b) for p, q in segs)

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
                if any(_lp_seg_box((ax, ay), e, t) for t in taken
                       if not (t[0] <= ax <= t[2] and t[1] <= ay <= t[3])):     # the point's own symbol is passed
                    continue
            return b, far
    return None


def place_labels_all(items, taken, bounds=None, segs=(), sizes=(1.0, 0.9), pad=0.5):
    """items: dicts with x, y (anchor), wh (function size_factor -> (w, h)), rank (0 = must show, 1 = may be
    dropped). Places rank 0 first, then rank 1, each nearest its point. Returns {index: (box, leader, size_factor)}
    for the placed ones; dropped rank-1 labels are left out (the caller may list them in a key). taken grows."""
    out = {}
    order = sorted(range(len(items)), key=lambda i: items[i].get("rank", 0))
    for i in order:
        it = items[i]
        got = None
        for f in sizes:
            w, h = it["wh"](f)
            got = label_spot(it["x"], it["y"], w, h, taken, bounds, segs, pad)
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
                if not any(lp_hit(b, t, pad) for t in taken) and not any(_lp_seg_box(p, q, b) for p, q in segs):
                    got = (b, True, sizes[-1])
                    break
        if got:
            taken.append(got[0])
            out[i] = got
    return out


SRC_KEY = []                       # v1.6: sources printed as [n] on the drawings; the numbered key is in the footer


# v5 (revision 29 Oct, D13 + Aras 18:56 "just source if it is available publicly"): only the public parts of a source
# text are printed; parts naming our own files, notes, cards, chats or people, and parts whose value is our own
# (calculated, assumed, interpolated, estimated, design) are dropped; status words are never printed
SRC_INTERNAL = re.compile(u"Aras|Begüm|Nil\\b|README|CONCEPT_RECORD|DATA_REGISTER|case\\.md|ideas\\.txt|\\.md\\b|\\.json|\\.csv|"
                          u"\\bcard\\b|\\bh0\\d|thread|\\b\\d\\d:\\d\\d\\b|default|design|zone base|Group 6|D\\d+\\b|"
                          u"history_phase|library/|v\\d+\\.\\d+ table|arithmetic", re.I)
SRC_OWN = re.compile(u"^\\s*(calculated|assumed|interpolated|estimated|design)", re.I)
SRC_WORD = re.compile(u"^\\s*(measured|published|official)[ ,:;]+", re.I)


def public_src(src):
    """v5: the publicly available part of a source text, or None when nothing public is left."""
    keep = []
    for part in (src or u"").split(u";"):
        if not part.strip() or SRC_OWN.match(part) or SRC_INTERNAL.search(part):
            continue
        part = SRC_WORD.sub(u"", part).strip()
        if part:
            keep.append(part)
    return u"; ".join(keep) or None


def cite(src):
    """v1.6: the number of a source in the footer key, as "[n]". v5: "" when the source has no public part (D13)."""
    src = public_src(src)
    if not src:
        return u""
    if src not in SRC_KEY:
        SRC_KEY.append(src)
    return u"[{}]".format(SRC_KEY.index(src) + 1)


def frame(pg, box, title, sub=None):
    """A drawing's panel on the board: white ground, a coloured rule on top, the title and one line under it.
    Returns the box left for the drawing."""
    x0, y0, x1, y1 = box
    pg.poly([rect(x0, y0, x1, y1)], fill=COL["white"], stroke=COL["faint"], lw=0.25)
    pg.poly([rect(x0, y1 - 1.2, x1, y1)], fill=MP["discharge"][1])
    pg.text(title, x0 + 4.0, y1 - 7.6, 4.0, COL["ink_dark"], bold=True)
    y = y1 - 9.0
    if sub:
        for ln in wrap(sub, 2.0, x1 - x0 - 8.0)[:2]:
            y -= 2.6
            pg.text(ln, x0 + 4.0, y, 2.0, COL["ink2"])
    return (x0 + 4.0, y0 + 3.0, x1 - 4.0, y - 2.5)


def fit(fn, x, y, w, h, pad=4.0, lo=0.5, hi=3.0):
    """The largest size factor s (steps of 0.05) at which fn(pg, x, y, w, h, s) stays inside its box."""
    best = lo
    s = lo
    while s <= hi:
        if fn(Page(1, 1), x, y, w, h, s) < y - h + pad:
            break
        best = s
        s += 0.05
    return best


# ---------------------------------------------------------------- the chain: what happens to the water, one way (Q6)
# v1.14 (Aras 27 Oct 11:07 "replace text with diagrams"; booklet rule: no personal names): one stream ribbon, the
# elements 1-11 as numbered roundels on it, a pictogram and a few words under each, grouped by place.
FS_MIN = 2.65                        # v1.14: the least text size on a booklet panel, mm (7.5 pt printed 1:1 on A3)
# v5 (revision 29 Oct, T3b WO-T3b-2): the chain ribbon is gone (p.12 is one water map now); its logic stays as the five
# steps the map numbers, one row each beside it: (step, icons.py icon, verb, how in keywords)
CHAIN = [
    (1, "rain", u"COLLECT", u"winter stream water and street + roof runoff, at the upstream entry"),
    (2, "reeds", u"CLEAN", u"once, in lined reed basins; the whole reach then runs clean"),
    (3, "storage", u"HOLD", u"winter water in the ground, for the dry summer, at most a year"),
    (4, "stream", u"GIVE BACK", u"clean water back to the stream; a summer strip keeps the bed wet"),
    (5, "stream_out", u"TO THE FARMS", u"the clean stream leaves the site for the farms outside; nothing is pumped back"),
]
CHAIN_SRC = (u"Aras 2026-10-18 14:29 (one way, cleaned once at the upstream end, no treatment at the downstream end), "
             u"14:49 and 15:02 (no farmland inside the site); strip: design values, " + RR + u" §4; minimum flow: "
             u"\"at least 10 %\" of the 10-year mean, HES water-use-rights regulation Art. 15/1, RG 15.06.2019 no. "
             u"30802; spillway: " + RR + u" §4 fail-safes; " + CR + u" D8; Demeter's Garden: card i01")


# ---------------------------------------------------------------- W1  the year of the water (Q2: bars, lines, brackets)
# One month axis in the DSİ water-year order (Oct-Sep), four rows that share it, the season brackets under them.
YEAR_SRC = [
    (u"rain, mm a month", u"measured, WMO 1991-2020 normals, MGM 17742 Bergama; 619.6 mm a year"),
    (u"open-water evaporation, mm a month", u"calculated, Hargreaves (FAO-56) x 1.05; " + RR + u" A1"),
    (u"stream past the site, million m³ a month", u"calculated, natural flow from measured DSİ gauges 2016-2021 "
                                                  u"(D04A053, D04A063), area-scaled to 101 km²; " + RR + u" A2"),
    (u"rain on the study areas' roofs and ground, thousand m³", u"calculated, survey roofs x C 0.95, rest x C 0.50; " +
     RR + u" A2"),
    (u"mean water depth in the bed, m", u"calculated, Manning n 0.050 (rough bed) on the surveyed channel; line = "
                                        u"wetter gauge, band = the two gauges; " + RR + u" A3"),
    (u"greenness (NDVI)", u"Sentinel-2 L2A, median of every clear scene of the month 2019-2025; classes CLC+ 2021; "
                          u"bergama_plant_data_v1.json"),
]


def draw_year(opt, W=369.0):
    """v1.14 (p.11-14 -> 2 pages, "replace text with diagrams"): one month axis in the water-year order, three rows
    that share it (rain against evaporation, the stream past the site, the depth in the bed), the key figures at the
    right, the three seasons of the water as brackets under the months. All words at FS_MIN or more."""
    pg = Page(0, 0)
    fs = FS_MIN
    lx, gx = 0.0, 38.0
    rx = W - 68.0
    gw = rx - 5.0 - gx
    mw = gw / 12.0

    def X(i):
        return gx + (i + 0.5) * mw

    def label(y_top, text, srcs):
        para(pg, lx, y_top + fs, gx - 4.0, text + u" " + u"".join(cite(s_) for s_ in srcs), fs, COL["ink"], bold=True)

    def grid(y0, h, vmax, ticks, fmt):
        for t in ticks:
            yy = y0 + h * t / vmax
            pg.line([(gx, yy), (gx + gw, yy)], COL["faint"], 0.12)
            pg.text(fmt(t), gx - 1.2, yy - fs * 0.35, fs, COL["ink2"], align="R")
        pg.line([(gx, y0), (gx + gw, y0)], COL["ink2"], 0.25)
    winter = set(WY.index(m) for m in (11, 0, 1, 2, 3))
    dry = set(WY.index(m) for m in (6, 7, 8))
    # ---- row 1: rain (dark where it beats evaporation) against open-water evaporation
    y0, h = -22.0, 18.0
    label(y0 + h, u"rain · evaporation, mm a month", (YEAR_SRC[0][1], YEAR_SRC[1][1]))
    grid(y0, h, 220.0, (0, 100, 200), lambda t: str(t))
    for i, m in enumerate(WY):
        x = gx + i * mw
        hr, he = h * RAIN[m] / 220.0, h * EVAP[m] / 220.0
        pg.poly([rect(x + 0.12 * mw, y0, x + 0.48 * mw, y0 + hr)], fill=C["d3"] if RAIN[m] > EVAP[m] else C["w2"])
        pg.poly([rect(x + 0.52 * mw, y0, x + 0.88 * mw, y0 + he)], fill=C["structure"])
    yk = y0 + h
    for colr, t in ((C["d3"], u"rain > evaporation: Nov-Feb"), (C["w2"], u"rain"), (C["structure"], u"evaporation")):
        pg.poly([rect(rx, yk - fs * 0.9, rx + 4.0, yk)], fill=colr)
        pg.text(t, rx + 5.5, yk - fs * 0.85, fs, COL["ink"])
        yk -= fs * 1.45
    figs(pg, rx, yk - 0.6, [(u"619.6 mm", u"rain a year"), (u"1,303 mm", u"evaporation")], 66.0, 3.6, fs)
    # ---- row 2: the stream past the site, million m³ a month (dark = Dec-Apr, pale = Jul-Sep)
    y0 = y0 - h - 9.0
    label(y0 + h, u"the stream past the site, million m³ a month", (YEAR_SRC[2][1],))
    for i, m in enumerate(WY):
        x = gx + i * mw
        hh = max(0.25, h * RIVER[m] / 7.5e6)
        c = MP["discharge"][2] if i in winter else (COL["faint"] if i in dry else MP["discharge"][0])
        pg.poly([rect(x + 0.15 * mw, y0, x + 0.85 * mw, y0 + hh)], fill=c)
        pg.text(u"{:.2f}".format(RIVER[m] / 1e6), x + 0.5 * mw, y0 + hh + 0.7, fs, C["w4"], align="C")
    pg.line([(gx, y0), (gx + gw, y0)], COL["ink2"], 0.25)
    yy = figs(pg, rx, y0 + h + 2.0, [(u"21 Mm³", u"a year past the site"), (u"89 %", u"of it Dec-Apr (dark)")],
              66.0, 3.6, fs)
    figs(pg, rx, yy - 1.0, [(u"1/{:.0f}".format(sum(RIVER) / float(sum(AREAS_RAIN))),     # 1/136: rain on the
                             u"local rain on the study areas " + cite(YEAR_SRC[3][1]))], 66.0, 3.6, fs,  # areas / stream
         C["w3"])
    # ---- row 3: mean depth in the bed, m (calculated on the surveyed cuts)
    y0, h = y0 - 20.0 - 10.0, 20.0
    label(y0 + h, u"mean depth in the bed, m", (YEAR_SRC[4][1],))
    vmax = 0.68

    def Yd(v):
        return y0 + h * min(v, vmax) / vmax
    grid(y0, h, vmax, (0.0, 0.3, 0.6), lambda t: u"{:.1f}".format(t))
    pg.line([(gx, Yd(STRIP_DEPTH)), (gx + gw, Yd(STRIP_DEPTH))], MP["storage"][2], 0.35, dash=[0.5, 0.7])
    pg.text(u"strip 0.30 m all year (design)", gx + gw - 1.0, Yd(STRIP_DEPTH) + 0.8, fs, MP["storage"][2],
            bold=True, align="R")
    series = [(u"upstream entry", ("up",), MP["discharge"][1], 0.45, [1.2, 0.6]),
              (u"K4 · K5 · downstream reach", ("k4", "k5", "down"), "3C5159", 0.45, None),
              (u"flat downstream end", ("flat",), MP["discharge"][2], 0.8, None)]
    ly = y0 + h
    for lab, keys, colr, lw, dash in series:
        lo = [min(DEPTH[k][g][WY[i]] for k in keys for g in (0, 1)) for i in range(12)]
        hi = [max(DEPTH[k][g][WY[i]] for k in keys for g in (0, 1)) for i in range(12)]
        pg.poly([[(X(i), Yd(hi[i])) for i in range(12)] + [(X(i), Yd(lo[i])) for i in range(11, -1, -1)]],
                fill=colr, alpha=0.15)
        pg.line([(X(i), Yd(hi[i])) for i in range(12)], colr, lw, dash=dash)
        pg.line([(rx, ly - fs * 0.45), (rx + 6.0, ly - fs * 0.45)], colr, max(lw, 0.4), dash=dash)
        pg.text(lab, rx + 7.5, ly - fs * 0.8, fs, COL["ink"])
        ly -= fs * 1.45
    pg.text(u"Jul-Sep: a few cm or dry", rx, ly - fs * 1.1, fs, C["d3"], bold=True)
    for i, m in enumerate(WY):
        pg.text(MONTHS[m], X(i), y0 - fs * 1.4, fs, COL["ink"], bold=i in winter, align="C")
    # ---- the three seasons of the water as brackets under the months
    yb = y0 - fs * 1.4 - 3.0

    def bracket(runs, kind, txt, src, colour, row):
        y = yb - row * 6.4
        for a_, b_ in runs:
            xa, xb = gx + a_ * mw + 1.0, gx + (b_ + 1) * mw - 1.0
            pg.line([(xa, y + 1.2), (xa, y), (xb, y), (xb, y + 1.2)], colour, 0.35)
        xa = gx + runs[0][0] * mw + 1.0
        icon(pg, kind, xa, y - 0.6, 4.4)
        pg.text(txt + u" " + cite(src), xa + 5.6, y - 3.9, fs, colour, bold=True)
    bracket([(2, 6)], "cube", u"DEC-APR · 89 % of the flow · storage fills · high water", u"calculated; " + RR + u" §0",
            MP["discharge"][2], 0)
    bracket([(7, 11), (0, 0)], "strip", u"MAY-OCT · worst case no inflow · strip on stored water",
            u"calculated case; " + CM + u" §4", MP["storage"][2], 1)
    bracket([(9, 11)], "sun", u"JUL-SEP · trickle or dry bed", u"calculated; " + CM + u" §3", COL["ink2"], 2)
    return pg


# ---------------------------------------------------------------- W2a  river height at the channel cuts (Q3)
# rain_river A3_section charts (one per cut) and pr1's flood sections (the same cuts, with the crossed roads), as one
# drawing (v1.10: all six at one true scale, Aras 22:02 "not stretch anything ever"). v1.1 (Aras 24 Oct 09:03, "find the factual
# and correct number"): each cut is now the surveyed cross-section of the main survey, not a trapezoid with borrowed
# widths; depths: worst roughness n 0.050 (rain_river_levels/tables/A3s_levels_by_event_surveyed_sections.csv).
EVENTS = [u"Jan-Feb mean (wettest month)", u"highest day 2016-2021", u"gauge record peak, area-scaled",
          u"Q100 (DSİ)", u"Q500 (DSİ)"]
LEVEL_COL = ["91ADB4", "6F95A3", "5D7F8D", "3C5159", "1B535E"]
bergama_data("CUTS")
SECT_SRC = (u"Water levels calculated (v1.1, 24 Oct): Manning normal depth on each surveyed cross-section, n 0.050 (Chow "
            u"1959, gravel-cobble bed, worst case), bed slope fitted on the surveyed bed 300 m either side, on DSİ Q100 "
            u"205.2 / Q500 263.3 m³/s (Danıştay 6. D. 2021/9521 E.) and the measured DSİ gauge flows 2016-2021, "
            u"area-scaled. Ground: TIN of the main survey (Bergama Müdahele Alanları (1).dxf: spot heights, contours, "
            u"bank and stream lines). Tables: " + RR + u" A3s. Road widths and distances: "
            u"survey road edges measured on each cut.")


# v1.12 (Aras 26 Oct, p.15: "show only the bed/channel part of each cut, at true proportions; use the freed space for
# what each level means for the design"): every cut cropped to the channel, one round scale for all six, no vertical
# exaggeration, and a level key with the design meaning of each line, from the settled sources only.
SECT_DENS = (100, 200, 250, 500, 1000, 2000)    # round scales 1:n, largest first: the first at which the panel fits
SECT_BOX = (375.0, 222.0)                       # the panel, mm (booklet p.15 prints it about 1:1 on A3)
SECT_MARGIN = 4.0                               # m of ground kept outside where Q500 meets it, either side
SECT_FS = FS_MIN                                # labels, mm (v1.14: 7.5 pt on the booklet page)
SECT_TITLE = 3.5                                # cut titles, mm
LEVEL_SHORT = [u"Jan-Feb", u"max day", u"record", u"Q100", u"Q500"]
LV_ZONES = CR + u" §5.2: three flood zones W (wet bed) / F (flood terraces) / D (dry top), proposal on the calculated levels"
LV_DESIGN = (CR + u" §3.6: design flood inside a settlement = the larger of Q100 + freeboard and Q500 (Flood and Sediment "
             u"Control Regulation 2019 Art. 10, EN-A5); nothing may reduce the channel's Q500 capacity")
LV_STORE = RR + u" §4 fail-safes, " + CR + u" §5.4: storage above the Q500 line or flood-proof"
LV_DSI = RR + u" §3 check against the official plan: the DSİ 20 x 3 m channel carries Q100 at 2.87 m"
LV_RULE = (u"city link flood rule (city link research §0 Q6 / Part G): Taşkın ve Rüsubat Kontrolü Yön. Art. 17(1), "
           u"4(1)(n), 6(2); Planlı Alanlar İmar Yön. Art. 5(10)")
LEVEL_MEAN = [  # per EVENTS line: (zone letter or None, design meaning in keywords, sources). Nothing here is new design.
    ("W", u"zone W, wet bed: floods every winter · only anchored stone, gravel, stepping stones, low weirs · nothing "
          u"fixed narrows the bed (17/1) · stalls and events Jul-Sep only", (LV_ZONES, LV_RULE)),
    ("W", u"top of zone W = the normal winter water · above it zone F: floods only", (LV_ZONES,)),
    ("F", u"zone F, flood terraces: floodable stone terraces, seating steps, flood-tolerant planting · paths closed in "
          u"floods · low stone seats only with DSİ approval", (LV_ZONES, LV_RULE)),
    ("F", u"DSİ's 20 x 3 m channel holds it at 2.87 m · + freeboard = design-flood test · bank top: 6 m service road "
          u"kept clear · occupied floors at DSİ crest + 1.50 m", (LV_DSI, LV_DESIGN, LV_RULE)),
    ("D", u"design flood · zone D only above it: pavilions, cafés, kiosks, olive, lavender · storage above it or "
          u"flood-proof · nothing cuts its capacity", (LV_DESIGN, LV_ZONES, LV_STORE)),
]
ZONE_COL = {"W": "91ADB4", "F": "A9B57F", "D": "D9CC8E"}


def cut_crop(cut):
    """First and last ground index kept: SECT_MARGIN m outside where the highest level (Q500) meets the ground."""
    a, b = cut["ext"][4]
    n = len(cut["ground"])
    if cut.get("bed") is None:          # DSİ's design trapezoid: drawn whole, it has no long banks to drop
        return 0, n - 1
    i0 = max(0, int(math.floor(a - SECT_MARGIN - cut["u0"])))
    i1 = min(n - 1, int(math.ceil(b + SECT_MARGIN - cut["u0"])))
    return i0, i1


def cut_roads(cut):
    """Roads named in the cut's notes: [(farthest distance m, "left"/"right", "38" or "42-52")]."""
    out = []
    for kind, t in cut["tags"]:
        if kind != "road":
            continue
        parts = [p.strip() for p in t.split(u"·")]
        off = [p for p in parts if p.endswith(u" m off")]
        side = [p for p in parts if p.endswith(u" bank")]
        if off and side:
            d = off[0][:-6].strip()
            try:
                out.append((float(d.split(u"-")[-1]), side[0].split()[0], d))
            except ValueError:
                pass
    return out


def break_mark(pg, X, ya, yb):
    """A section break line: vertical with a small zigzag in the middle, where the ground is cut away."""
    ym = (ya + yb) / 2.0
    pg.line([(X, ya), (X, ym - 0.9), (X - 0.8, ym - 0.35), (X + 0.8, ym + 0.35), (X, ym + 0.9), (X, yb)], COL["ink"],
            0.18)


def side_arrow(pg, x_tip, y, sgn):
    """A small arrow 4 mm long pointing out of the drawing (sgn -1 = to the left), its tip at x_tip."""
    pg.line([(x_tip - sgn * 4.0, y), (x_tip - sgn * 0.8, y)], COL["ink2"], 0.25)
    pg.poly([[(x_tip, y), (x_tip - sgn * 1.2, y + 0.6), (x_tip - sgn * 1.2, y - 0.6)]], fill=COL["ink2"])


def draw_cut(pg, x0, y_top, cut, kx, opt, fs=SECT_FS, w_txt=None):
    """One surveyed channel cut, cropped to the channel (cut_crop), at kx mm per m both ways (true proportions):
    ground, the five event levels across the width each covers, a level ladder at the right; returns its bottom y."""
    g, dep, ext = cut["ground"], cut["dep"], cut["ext"]
    i0, i1 = cut_crop(cut)
    xl, xr = float(cut["u0"] + i0), float(cut["u0"] + i1)
    top = max(dep) + 0.8
    ladder = spread([d * kx for d in dep], fs * 1.3, lo=0.0)        # ladder baselines over the bed, mm
    above = max(top * kx, ladder[-1] + fs * CAP)
    pg.text(cut["name"], x0, y_top - SECT_TITLE * CAP, SECT_TITLE, COL["ink_dark"], bold=True)
    y_draw = y_top - SECT_TITLE * (CAP + 0.25) - 3.0                 # top of the drawing zone, clear of the title
    k4 = cut["key"] == "k4"
    r = 3.1                             # element roundels: numeral >= 2.5 mm
    if k4:                              # cards 8 and 9 in a row above the drawing (at true scale they would overlap)
        y_draw -= 2 * r + 2.0
    oy = y_draw - above
    ox = x0 - xl * kx

    def T(x, y):
        return (ox + x * kx, oy + y * kx)
    X0, X1 = ox + xl * kx, ox + xr * kx
    for t in range(1, int(top) + 1):
        pg.line([T(xl, t), T(xr, t)], COL["faint"], 0.1)
    pts = [T(cut["u0"] + i, min(g[i], top)) for i in range(i0, i1 + 1)]
    pg.poly([pts + [T(xr, -0.6), T(xl, -0.6)]], fill=SEC["soil"])          # v1.10: the site board's cut ground
    a, b = ext[0]                                         # the wettest month's water, hatched from the bed
    wr = [T(cut["u0"] + i, min(g[i], dep[0])) for i in range(i0, i1 + 1) if a - 0.5 <= cut["u0"] + i <= b + 0.5]
    if len(wr) >= 2:
        sec_put(pg, sec_water([(wr[0][0], T(0, dep[0])[1])] + wr + [(wr[-1][0], T(0, dep[0])[1])], 0.5, 0.06))
    pg.line(pts, COL["ink"], 0.3)
    if i0 > 0:                          # the long flat bank is cropped away here
        break_mark(pg, X0, oy - 0.6 * kx - 0.8, pts[0][1] + 1.2)
    if i1 < len(g) - 1:
        break_mark(pg, X1, oy - 0.6 * kx - 0.8, pts[-1][1] + 1.2)
    for i, d in enumerate(dep):
        c = LEVEL_COL[i]
        a, b = max(ext[i][0], xl), min(ext[i][1], xr)
        pg.line([T(a, d), T(b, d)], c, 0.7 if i >= 3 else 0.45)
        yl = oy + ladder[i]
        pg.line([T(b, d), (X1 + 1.2, yl + fs * 0.3), (X1 + 2.2, yl + fs * 0.3)], c, 0.15)
        pg.text(u"{:.2f} {}".format(d, LEVEL_SHORT[i]), X1 + 2.6, yl, fs, c if i else C["w3"], bold=i >= 3)
    if k4:                              # cards 8 and 9: the low right-bank ground floods in Q100 / Q500; above Q500 stays dry
        terr = 2.08                      # the right-bank terrace, m above the bed (survey, this cut)
        u8 = next((cut["u0"] + i for i in range(i0, i1 + 1) if g[i] <= terr + 0.05), xl + 6.0)
        p8, p9 = T(u8, terr), T(xl + 1.0, dep[4] + 0.35)
        yn = y_draw + r + 1.0
        x9 = X0 + r
        x8 = max(p8[0], x9 + 2 * r + 2.0)
        for n_, xn, p in ((9, x9, p9), (8, x8, p8)):
            pg.line([(xn, yn - r), p], COL["river_dark"], 0.18)
            pg.circle(p[0], p[1], 0.35, fill=COL["river_dark"])
            node(pg, xn, yn, n_, opt, r)
        pg.text(u"8 flood terrace · 9 raised dry top, above Q500", x8 + r + 1.5, yn - fs * CAP / 2.0, fs,
                COL["river_dark"], bold=True)
    y = oy - 0.6 * kx - 1.6 - fs * CAP
    roads = dict((s, (dmax, d)) for dmax, s, d in cut_roads(cut))
    if cut.get("bed") is not None:      # seen looking upstream: the right bank (+u negative) on the left of the page
        lab_r, lab_l = u"right bank", u"left bank"
        if "right" in roads and roads["right"][0] > -xl:    # the road lies on the cropped-away bank: an arrow to it
            side_arrow(pg, X0, y + fs * CAP / 2.0, -1)
            lab_r = u"road {} m · right bank".format(roads["right"][1])
            pg.text(lab_r, X0 + 5.0, y, fs, COL["ink2"], bold=True)
        else:
            pg.text(lab_r, X0, y, fs, COL["ink2"], bold=True)
        if "left" in roads and roads["left"][0] > xr:
            side_arrow(pg, X1, y + fs * CAP / 2.0, 1)
            pg.text(u"left bank · road {} m".format(roads["left"][1]), X1 - 5.0, y, fs, COL["ink2"], bold=True,
                    align="R")
        else:
            pg.text(lab_l, X1, y, fs, COL["ink2"], bold=True, align="R")
        y -= fs * 1.5
    else:                               # DSİ's design channel: its size, under it (v1.14: its chip became this line)
        pg.text(u"20 m bed · 3 m deep " + cite(DSI_SRC), X0, y, fs, COL["ink2"], bold=True)
        y -= fs * 1.5
    w_txt = w_txt or (X1 - X0 + 20.0)                # v1.14: only the notes on how the floods spread stay (chips)
    tags = [t for t in cut["tags"] if t[0] in ("over", "spread")]
    return chips(pg, x0, y + fs * 0.6, tags, fs, w_txt) if tags else y


DSI_SRC = (u"SYGM 2019 Yönetici Özeti p.75, measure 155 (North Aegean flood management plan): 20.00 m bed, 3.00 m "
           u"deep, 3,720 m; depths on the design trapezoid, walls above 3 m taken as vertical")   # v4 (28 Oct, bank-depth REPORT §4.4)
ZONES = [  # v1.14: what each level allows, as three zones (keywords of LEVEL_MEAN, its sources)
    ("W", u"WET BED", (0, 1), u"floods every winter · stone, gravel, stepping stones · nothing fixed narrows the bed · "
                              u"events Jul-Sep", (LV_ZONES, LV_RULE)),
    ("F", u"FLOOD TERRACES", (2, 3), u"floodable terraces, seating steps · closed in floods · 6 m service road on the "
                                     u"bank top", (LV_ZONES, LV_RULE, LV_DSI)),
    ("D", u"DRY TOP · above Q500", (4,), u"pavilions, cafés, kiosks, olive, lavender · storage above Q500 or "
                                         u"flood-proof", (LV_DESIGN, LV_ZONES, LV_STORE)),
]
TUNNEL_SRC = (u"h02 §2.3 (library/research/selinos_site_history_inaccessible_edges_v1.md): Red Hall twin tunnels, "
              u"Roman Imperial; capacity 360 m³/s (s24: Wikipedia 'Pergamon Bridge', citing Grewe & Öziş 1994, "
              u"Antike Welt 25(4)) vs 720 m³/s (s67: Öziş 2015, Environmental Processes 2:559-573), marked [U] "
              u"conflicting there, possibly one tube vs both")
DSI_Q_SRC = (u"DSİ Q100 205.20 / Q500 263.33 m³/s for the town section, Danıştay 6. D. E.2021/9521 K.2023/4193 "
             u"(h02 s22)")


def draw_level_key(pg, x, y, w, kx):
    """v1.14: what each level allows, as three zone blocks side by side (zone colour, the levels in it as line
    samples, keywords). Returns the bottom y."""
    fs = SECT_FS
    bw = (w - 2 * 4.0) / 3.0
    low = y
    for i, (z, name, lv, words, srcs) in enumerate(ZONES):
        bx = x + i * (bw + 4.0)
        pg.poly([rect(bx, y - 6.0, bx + bw, y)], fill=ZONE_COL[z])
        pg.text(z, bx + 2.0, y - 4.6, 3.6, COL["ink_dark"], bold=True)
        pg.text(name, bx + 8.0, y - 4.4, 3.2, COL["ink_dark"], bold=True)
        yy = y - 6.0 - fs * 1.4
        for k in lv:
            pg.line([(bx, yy + fs * 0.35), (bx + 7.0, yy + fs * 0.35)], LEVEL_COL[k], 0.7 if k >= 3 else 0.45)
            pg.text(EVENTS[k], bx + 9.0, yy, fs, LEVEL_COL[k] if k else C["w3"], bold=True)
            yy -= fs * 1.35
        yy = para(pg, bx, yy + fs * 1.0, bw, words + u" " + u"".join(cite(s_) for s_ in srcs), fs, COL["ink"])
        low = min(low, yy)
    return low - 1.0


def draw_tunnels(pg, x, y, w):
    """v1.14 (history H2, spec §3 p.12): the Roman tunnels under the Red Hall as a precedent: what they carry against
    today's design flood, on one m³/s scale; both published capacities, as the sources disagree. Returns bottom y."""
    fs = SECT_FS
    icon(pg, "tunnel", x, y, 9.0)
    para(pg, x + 11.0, y + 0.4, w - 11.0, u"ROMAN TUNNELS UNDER THE RED HALL: THEY ALREADY CARRY THE FLOODS", 3.2,
         COL["ink_dark"], bold=True)
    rows = [(u"DSİ Q100 today", 205.20, LEVEL_COL[3], None, DSI_Q_SRC),
            (u"DSİ Q500 today", 263.33, LEVEL_COL[4], None, DSI_Q_SRC),
            (u"Roman tunnels", 360.0, "8B6B4A", None, TUNNEL_SRC),
            (u"or", 720.0, "8B6B4A", ("C9B79C", 0.9, 0.25), TUNNEL_SRC)]
    lab_w = max(text_w(r[0], fs, True) for r in rows) + 2.0
    gx, gw = x + lab_w, w - lab_w - text_w(u"263.33 m³/s [99]", fs) - 3.0
    yy = y - 12.0
    for lab, v, colr, stripes, src in rows:
        pg.text(lab, gx - 2.0, yy - fs * 0.9, fs, COL["ink"], bold=True, align="R")
        pg.poly([rect(gx, yy - 3.0, gx + gw * v / 720.0, yy)], fill=COL["white"] if stripes else colr,
                stroke=colr, lw=0.25, stripes=stripes)
        t = (u"{:.2f}".format(v) if v % 1 else u"{:.0f}".format(v)) + u" m³/s " + cite(src)
        pg.text(t, gx + gw * v / 720.0 + 1.5, yy - fs * 0.9, fs, COL["ink"])
        yy -= 4.4
    pg.text(u"sources differ: one tube or both?", gx, yy - fs * 0.6, fs, COL["ink2"])
    return yy - fs * 1.6


def scale_bar(pg, x, y, kx, den):
    """0-5-10-20 m bar at kx mm per m, its scale and the drawing rule beside it. Returns bottom y."""
    fs = SECT_FS
    for a, b, f in ((0, 5, COL["ink"]), (5, 10, COL["white"]), (10, 20, COL["ink"])):
        pg.poly([rect(x + a * kx, y - 1.2, x + b * kx, y)], fill=f, stroke=COL["ink"], lw=0.15)
    for m in (0, 5, 10, 20):
        pg.text(u"{}".format(m), x + m * kx, y - 1.2 - 1.0 - fs * CAP, fs, COL["ink2"], align="C")
    pg.text(u"m", x + 20 * kx + 2.0, y - 1.2 - 1.0 - fs * CAP, fs, COL["ink2"])
    pg.text(u"1:{:,.0f} · true proportions · cut {:.0f} m outside Q500 {}".format(den, SECT_MARGIN, cite(SECT_SRC)),
            x + 20 * kx + 7.0, y - 1.2 - fs * 0.6, fs, COL["ink2"])
    return y - 1.2 - 1.0 - fs * 1.2


def sect_layout(opt, den):
    """The six cropped cuts at 1:den, upstream to downstream, two per row (each row about the same width), then the
    level key and the scale bar."""
    kx = 1000.0 / den
    pg = Page(0, 0)
    by = dict((c["key"], c) for c in CUTS)
    rows = [("up", "k4"), ("k5", "down"), ("flat", "dsi")]
    y, right = 0.0, 0.0
    for row in rows:
        x, low = 0.0, y
        for key in row:
            if key not in by:
                continue
            cut = by[key]
            i0, i1 = cut_crop(cut)
            n0 = len(pg.items)
            draw_cut(pg, x, y, cut, kx, opt, SECT_FS, max((i1 - i0) * kx + 20.0, 95.0))
            bb = items_bbox(pg.items[n0:])
            x = bb[2] + 12.0
            low = min(low, bb[1])
            right = max(right, bb[2])
        y = low - 7.0
    y = scale_bar(pg, 0.0, y + 2.0, kx, den) - 3.0          # v1.14: the scale under the cuts, then the key
    w = max(right, 300.0)
    draw_level_key(pg, 0.0, y, w * 0.62, kx)
    draw_tunnels(pg, w * 0.62 + 6.0, y, w * 0.38 - 6.0)
    return pg


def draw_sections(opt, box=SECT_BOX):
    """The five surveyed cuts and DSİ's planned channel, cropped to the channel, at the largest round scale of SECT_DENS
    at which the panel fits box (w, h), with the level key. Returns (page, scale denominator)."""
    pg = None
    for den in SECT_DENS:
        pg = sect_layout(opt, den)
        bb = items_bbox(pg.items)
        if bb[2] - bb[0] <= box[0] and bb[3] - bb[1] <= box[1]:
            break
    return pg, float(den)


SECT_K = 4.0                         # v1.10: every cut at 1:250 across and up (4 mm per m), one shared scale
CUTS_DEN = [None]                    # the scale the six cuts end at on the sheet (read by results.json)


# ---------------------------------------------------------------- W2b  the S4 detail (folded in from bergama_detail_section v2)
# The 1:75 detail of the two banks at the flat downstream end (board section line S4) is drawn by its own engine
# (DETAIL_SRC at the end of this file, the detail section v2 code without its PDF writer and Grasshopper part), at
# DETAIL_SCALE, with every season's water as a level line instead of one sheet per season (Q3). The season sheets'
# texts become the season table beside it.
DETAIL_SCALE = 200.0                 # 1:200 on the board (the engine's own sheet was 1:75)
_DET = []
_DET_PROF = []                       # the S4 ground profile used (survey re-cut from the open file, or embedded)


def detail_engine():
    """The detail-section engine, run once in its own namespace, drawing at DETAIL_SCALE. Its level lines are drawn
    without their texts (at 1:200 they would lie on top of each other) and listed in _LV for the level ladder; its
    right-hand level chain spreads its texts apart."""
    if _DET:
        return _DET[0]
    ns = {"__name__": "bergama_detail_engine"}
    exec(compile(DETAIL_SRC, "bergama_detail_engine", "exec"), ns)
    ns["SCALE"] = DETAIL_SCALE
    ns["K"] = 1000.0 / DETAIL_SCALE
    ns["_LV"] = []

    def level_line(pg, S, z, label, dash, colour=ns["FLOOD"]):
        s_l, s_r = S.d["s_from"], S.d["s_to"]
        n = int(abs(s_r - s_l) / 0.1)
        run, runs = [], []
        for i in range(n + 1):
            s = s_l + (s_r - s_l) * i / n
            if z > S.surf(s) + 0.01:
                run.append(S.P(s, z))
            elif run:
                runs.append(run)
                run = []
        if run:
            runs.append(run)
        for r in runs:
            if len(r) >= 2:
                pg.line([r[0], r[-1]], colour, 0.25, dash=dash, layer="levels")
        X, Y = S.P(s_r, z)
        X -= 3.0
        pg.poly([[(X - 1.3, Y + 1.9), (X + 1.3, Y + 1.9), (X, Y)]], fill=None, stroke=colour, lw=0.2, layer="levels")
        ns["_LV"].append((z, label, colour, dash))

    def vdims(pg, S, levels, x):
        lv = sorted(set(round(z, 3) for z, _ in levels))
        names = dict((round(z, 3), n_) for z, n_ in levels)
        ys = [S.Y(z) for z in lv]
        ly = spread(ys, FS_MIN * 1.3)                       # v1.14: 7.5 pt (was 1.6 mm, 2.1 mm apart)
        pg.line([(x, ys[0]), (x, ys[-1])], ns["DIM"], 0.12, layer="dimensions")
        for z, Y, Yl in zip(lv, ys, ly):
            pg.line([(x - 6.0, Y), (x + 1.2, Y)], ns["DIM"], 0.08, layer="dimensions")
            pg.line([(x - 0.8, Y - 0.8), (x + 0.8, Y + 0.8)], ns["DIM"], 0.2, layer="dimensions")
            pg.line([(x + 1.2, Y), (x + 3.0, Yl + 0.5), (x + 4.0, Yl + 0.5)], ns["GREY"], 0.08, layer="dimensions")
            pg.text("%+.2f %s" % (z, names[z]), x + 4.4, Yl - 0.1, FS_MIN, ns["GREY"], layer="dimensions")
    ns["level_line"] = level_line
    ns["vdims"] = vdims
    r28_people(ns)                    # v4 (MIRAQUA 28 Oct, P19.2): the people of pp.14-15 as common/figures.py silhouettes
    _DET.append(ns)
    return ns


def s4_profile(E, log=None):
    """The S4 ground (survey re-cut from the open file, else the embedded survey profile), once per press."""
    if _DET_PROF:
        return _DET_PROF[0]
    prof = None
    try:
        r = E["rhino_inputs"](log if log is not None else [])
        if r and r[1] is not None:
            prof = r[1]
    except Exception as ex:
        if log is not None:
            log.append(u"S4 ground from the open file not read ({}); the embedded survey profile is used".format(ex))
    if prof is None:
        prof = (E["PROFILE_S0"], E["PROFILE_DS"], E["PROFILE_Z"])
    _DET_PROF[:] = [prof]
    return prof


BK_GROW = 1.45                       # room kept round each label for the booklet (its words reset at >= 7.5 pt)


def level_ladder(pg, entries, x_line, x_text, fs, boxes=None, lo=None):
    """Water levels at the right of a section: [(page y, text, colour, bold)], texts spread apart, leaders from the
    level's end at x_line."""
    entries = sorted(entries, key=lambda e: e[0])
    ly = spread([e[0] - fs * 0.35 for e in entries], fs * 1.25 * BK_GROW, lo=lo)
    for (y, t, colour, bold), yl in zip(entries, ly):
        pg.line([(x_line, y), (x_text - 2.0, yl + fs * 0.35), (x_text - 0.6, yl + fs * 0.35)], colour, 0.12)
        pg.text(t, x_text, yl, fs, colour, bold=bold)
        if boxes is not None:
            boxes.append((x_text, yl - fs * 0.3, x_text + text_w(t, fs, bold) * BK_GROW, yl + fs * BK_GROW))


# v5 (revision 29 Oct, T3b WO-T3b-4): pp.14-15 are drawn whole by pages/p14_15_s4.py from the level module (D4 b) and
# its own tables (P14_*, P15_*); the core keeps only the seasons, their months and the open months of the gravel bed.
# The detail engine (detail_engine, s4_profile) stays for p.17 and results.json only.
SEAS = ("winter", "spring", "summer", "autumn")
S4_MONTHS = {"winter": u"Dec-Feb", "spring": u"Mar-May", "summer": u"Jun-Aug", "autumn": u"Sep-Nov"}
S4_MONTH_IDX = {"winter": (11, 0, 1), "spring": (2, 3, 4), "summer": (5, 6, 7), "autumn": (8, 9, 10)}
# D10 (history_phase1/DECISIONS.md): the in-bed sub-hub opens in the months this board's own year calendar gives the
# bed to people: outside Dec-Apr (89 % of the year's flow, RIVER) and with rain below open-water evaporation
# (RAIN < EVAP, no surplus month). Computed: May-Oct.
SUBHUB_OPEN = [m for m in range(12) if m not in (11, 0, 1, 2, 3) and RAIN[m] < EVAP[m]]


# ---- v4 (MIRAQUA 28 Oct 2026): the water board's part of the round (revision_2026-10-28/PLAN.md, row WB) ----------
# Bold keywords in running text (G5), the scale bar (PLAN §2: standard scales, a bar beside every orthogonal drawing),
# the shared silhouettes of common/figures.py for the detail engine's people (r28_fig, r28_people). v5 (revision
# 29 Oct, T3b WO-T3b-4): THE SEASON, the occupancy diagram and their tables are gone; pp.14-15 are drawn whole by
# pages/p14_15_s4.py.


# ---------------------------------------------------------------- G5: text with **bold** keywords
def r28_words(s, bold=False):
    """s with '**' switching bold on and off, as words [[(text, bold), ...]] (a word is what lies between spaces; a
    '**' inside a word splits it into pieces)"""
    words, glue = [], False
    for i, part in enumerate(s.split(u"**")):
        b = bold != (i % 2 == 1)
        for j, pc in enumerate(part.split(u" ")):
            if j:
                glue = False
            if pc:
                if glue and words:
                    words[-1].append((pc, b))
                else:
                    words.append([(pc, b)])
                glue = True
    return words


def r28_runs(words):
    """one line of words as runs [(text, bold)], neighbouring pieces of one weight joined"""
    runs = []
    for k, wd in enumerate(words):
        for j, (t, b) in enumerate(wd):
            if k and not j:
                t = u" " + t
            if runs and runs[-1][1] == b:
                runs[-1] = (runs[-1][0] + t, b)
            else:
                runs.append((t, b))
    return runs


def r28_draw_runs(pg, runs, x, y, size, colour, kcol=None, halo=None):
    for t, b in runs:
        pg.text(t, x, y, size, (kcol or colour) if b else colour, bold=b, halo=halo)
        x += text_w(t, size, b)
    return x


def r28_lines(s, size, width, bold=False):
    """s wrapped to width as lines of runs"""
    out, cur, cw = [], [], 0.0
    sp = text_w(u" ", size)
    for wd in r28_words(s, bold):
        ww = sum(text_w(t, size, b) for t, b in wd)
        if cur and cw + sp + ww > width:
            out.append(r28_runs(cur))
            cur, cw = [wd], ww
        else:
            cw += (sp if cur else 0.0) + ww
            cur.append(wd)
    if cur:
        out.append(r28_runs(cur))
    return out


def r28_para(pg, x, y, w, s, size, colour, bold=False, lh=1.28, kcol=None, halo=None):
    """para() with **bold** keywords (G5): wrapped to w from the top y; returns the bottom y"""
    for runs in r28_lines(s, size, w, bold):
        y -= size * lh
        r28_draw_runs(pg, runs, x, y, size, colour, kcol, halo)
    return y


# ---------------------------------------------------------------- PLAN §2: the scale bar of an orthogonal drawing
R28_BAR = {200: (0, 2, 5, 10), 250: (0, 2, 5, 10), 500: (0, 5, 10, 20), 1000: (0, 10, 20, 50)}   # its marks, m


def r28_bar_box(x, y, den, fs=None, below=True):
    """the box (x0, y0, x1, y1) that r28_scale_bar takes when drawn from (x, y)"""
    fs = fs or FS_MIN
    t = R28_BAR.get(int(round(den)), (0, 5, 10, 20))
    x1 = x + t[-1] * 1000.0 / den
    lab = text_w(u"1:{:,.0f}".format(den), fs)
    if below:
        return (x - 1.0, y - fs * 1.3 - 0.2, max(x1 + 3.5, x + lab), y + 2.0 + fs * CAP + 0.2)
    return (x - 1.0, y - fs * 0.3, x1 + 4.0 + lab, y + 2.0 + fs * CAP + 0.2)


def r28_scale_bar(pg, x, y, den, fs=None, below=True, colour=None):
    """the scale bar of a drawing at 1:den from (x, y): ink and white segments 1.2 mm high, the marks in m over them,
    "1:den" under the bar (below) or after it. Returns its box."""
    fs = fs or FS_MIN
    ink = colour or COL["ink"]
    k = 1000.0 / den
    t = R28_BAR.get(int(round(den)), (0, 5, 10, 20))
    for i in range(len(t) - 1):
        pg.poly([rect(x + t[i] * k, y, x + t[i + 1] * k, y + 1.2)], fill=ink if i % 2 == 0 else COL["white"],
                stroke=ink, lw=0.12)
    for i, v in enumerate(t):
        pg.text(u"{}{}".format(v, u" m" if i == len(t) - 1 else u""), x + v * k, y + 2.0, fs, ink, align="C")
    lab = u"1:{:,.0f}".format(den)
    if below:
        pg.text(lab, x, y - fs * 1.05, fs, ink)
    else:
        pg.text(lab, x + t[-1] * k + 4.0, y, fs, ink)
    return r28_bar_box(x, y, den, fs, below)


# ---------------------------------------------------------------- P19.2: one figure set (common/figures.py)
R28_SEAT = 0.445                     # the sit pose's seat over its feet, m (common/figures.py: thigh 0.52 less half of it)
R28_CHILD = 1.15                     # a child, m (common/figures.py)
R28_ASSET_POSE = {  # the detail engine's traced people (DETAIL_SRC FIGS) as poses of common/figures.py: (pose, extra)
    "I_walker_flood_wall": ("walk", None), "I_woman_with_bag": ("walk", None), "J_woman_walking": ("walk", None),
    "I_photographer": ("watch", None), "J_man_and_child": ("walk", "child"), "J_photographer_balcony": ("watch", None),
    "J_woman_on_steps": ("stand", None), "I_child_on_sand": ("touch", "small"), "J_person_seated": ("sit", "edge"),
    "J_person_sitting": ("sit", "stool"), "J_cyclist_cheering": ("bike", None), "I_cyclist_waving": ("bike", None)}


def r28_fig(pg, pose, x, y, k, colour, facing=1, height=1.75, layer="people"):
    """one silhouette of common/figures.py with its feet at (x, y), k mm per m, filled in one opaque colour, no
    stroke, one poly per outline (the pages fill even-odd); on this board's Page or the detail engine's. Returns its
    box."""
    xs, ys = [], []
    for ring in fig_polys(pose, height, facing):
        pts = [(x + px * k, y + py * k) for px, py in ring]
        xs += [p[0] for p in pts]
        ys += [p[1] for p in pts]
        pg.poly([pts], fill=colour, stroke=None, layer=layer)
    return (min(xs), min(ys), max(xs), max(ys))


def r28_people(E):
    """the detail engine's people (draw_asset, which figure() and balcony() call) and cyclists (bike) drawn as the
    shared silhouettes, in the engine's colours and layers, at the scale it draws at (E["K"] at the call); a seated
    figure is anchored at its seat (it sits on an edge). The traced assets are no longer decoded."""
    def draw_asset(pg, key, X, Y, height_mm=None, flip=False, layer="entourage", tone=None):
        pose, extra = R28_ASSET_POSE.get(key, ("stand", None))
        k = E["K"]
        f = -1 if flip else 1
        col = tone or E["FIG"]
        if extra == "edge":
            Y -= R28_SEAT * k
        r28_fig(pg, pose, X, Y, k, col, f, R28_CHILD if extra == "small" else 1.75, layer)
        if extra == "child":
            r28_fig(pg, "walk", X + f * 0.5 * k, Y, k, col, f, R28_CHILD, layer)
        elif extra == "stool":
            for a in (-0.12, 0.2):
                pg.poly([rect(X + f * (a - 0.02) * k, Y, X + f * (a + 0.02) * k, Y + R28_SEAT * k)], fill=col,
                        stroke=None, layer=layer)
            pg.poly([rect(X - f * 0.16 * k, Y + (R28_SEAT - 0.04) * k, X + f * 0.24 * k, Y + R28_SEAT * k)], fill=col,
                    stroke=None, layer=layer)

    def bike(pg, S, s, flip):
        X, Y = S.P(s, S.surf(s))
        r28_fig(pg, "bike", X, Y, E["K"], E["FIG"], -1 if flip else 1, 1.75, "people")
    E["draw_asset"] = draw_asset
    E["bike"] = bike




# ---------------------------------------------------------------- W3a  concept sections (pr1 v3.1 idea sketches)
# SKETCH_SRC (end of this file) is pr1's sketch code; it runs in its own namespace and draws page items in pr1's
# order. The element numbers come from node() of this board.
_SK = []


def sketch_engine():
    if not _SK:
        ns = {"__name__": "pr1_sketches", "_tree_rand": _tree_rand}   # reeds use the trees' random stream
        exec(compile(SKETCH_SRC, "pr1_sketches", "exec"), ns)
        _SK.append(ns)
    return _SK[0]


SK_SRC = dict(  # v1.8: the sketches' sources, as in proposal sections v3
    levels=RR + u" v1.1 table: levels calculated on the surveyed channel cuts (Manning, main survey TIN)",
    rain=u"water_data/README: MGM 17742 normals 1991-2020, seasonal shares of the year's rain (arithmetic)",
    concept=CR + u" (Q1: east channel wall kept, default)", tiers=u"Aras's concept text: tiers, level 1 / 2 / 3",
    garden=u"card i01: Demeter's Garden, Begüm's idea, page and crop list (zones DG 1-2)",
    zones=u"zone base ZONES.md: WP 1-2 and the floodable boardwalk",
    plants=u"DATA_REGISTER PL-11, PL-12: olive and lavender, waterlogging", gauges=u"DSİ gauge yearbooks 2016-2021",
    survey=u"main survey: road edges YOL_SOSE")


def draw_concept(which, opt):
    """which: "up" (upstream entry) or "k4"; opt: form A (organic at the water) or B (no curves)."""
    E = sketch_engine()
    E["FORM"] = opt
    del E["ZP"][:]
    E["ORDER"][0] = 0

    def NODE(o, x, y, n):
        tmp = Page(0, 0)
        node(tmp, o[0] + x, o[1] + y, n, opt, 2.6)
        for it in tmp.items:
            E["_put"](it, E["Z_TEXT"])
    E["NODE"] = NODE
    E["CITE"] = lambda k: cite(SK_SRC[k])           # v1.8: source numbers [n] inside the sketches (proposal sections v3)
    (E["concept_aras_sketch"] if which == "up" else E["concept_begum_sketch"])()
    pg = Page(0, 0)
    pg.items = [it for _, _, it in sorted(E["ZP"], key=lambda e: (e[0], e[1]))]
    return pg


# ---------------------------------------------------------------- W3b  planting bands (plant analysis panel 8)
# PROPOSAL from the concept "Selinos water calendar" v1 §9 (second account), species evidence from the concept and
# research file 04; band A now carries the continuous strip (CONFLICTS.md row 2: no held pools).
C_PL = dict(green_deep="495338", green_mid="727A4E", accent="8B3A3F", ink="4A3F35", ink2="847E75", structure="B0AC9C")


def para_at(pg, s, x, y, size, width, color=None, lead=1.32, bold=False):
    """Wrapped text from the baseline y downwards (the plant board's para); returns the y below the last line."""
    for ln in wrap(s, size, width, bold):
        pg.text(ln, x, y, size, color or C_PL["ink"], bold=bold)
        y -= size * lead
    return y


PLANT_BANDS = [  # code, name, Dutch ecotope, wet days a year, indicative depth, research-04 zone (this board's matching)
    ("A", u"Strip and bed (continuous strip)", u"geulen/strangen; ondiep water", u"permanent", u"1.0–2.0 m (geul), 1.0 m", "Z1"),
    ("B", u"Marsh band", u"riet/moerasruigte", u"150–365 d/yr", u"0.5–1.0 m", "Z1–Z2"),
    ("C", u"Willow band", u"zachthoutooibos/struweel", u"50–150 d/yr", u"0.5–1.0 m", "Z2–Z3"),
    ("D", u"Wet meadow", u"nat grasland", u"10–150 d/yr", u"0.5–1.0 m", "Z2–Z3"),
    ("E", u"Dry meadow / hardwood", u"droog grasland; hardhoutooibos", u"0.5–10 d/yr; 0.5–50 d/yr", u"0.5 m", "Z3"),
    ("F", u"Urban terraces", u"(none)", u"extreme events only", u"—", "Z4"),
]
BAND_COL = {"A": "91ADB4", "B": "9DB7A8", "C": "A9B57F", "D": "C9D1A4", "E": "D9CC8E", "F": "D8D5CC"}
BAND_SOURCE = (u"Bands: Rijkswaterstaat memo 'Hydrologische randvoorwaarden van de ecotopen in PAGW rivieren' "
               u"(RWS-ZN, v1.0, 2 Feb 2023, concept), pp. 8–16, as used in the concept v1 §9.1. The memo "
               u"calls these ranges, not fixed limits. Z1–Z4 = bank zones of research file 04 (its own reading).")
# species: band, latin, local name, evidence (quoted or summarised from the named file, with its source), flag
bergama_data("SPECIES")


# W3b band -> its days a year under water (RWS ranges, PLANT_BANDS); A is the strip itself (permanent)
BAND_DAYS = {"B": (150.0, 365.0), "C": (50.0, 150.0), "D": (10.0, 150.0), "E": (0.5, 50.0), "F": (0.0, 0.5)}






# ---------------------------------------------------------------- p.22: plant photos (Wikipedia / Commons)
# v3: the fetching moved to src/common/plant_photos.py, shared with the agriculture alternatives, so a plant shows the
# same photo, at the same 28 x 21 mm, wherever the booklet names it (cache: Downloads/Bergama/cached/plant_photos/).
# No network (or any failure) = a labelled empty frame; the board never fails on a photo.
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
# later press. Only CC BY, CC BY-SA, CC0 and public-domain files are used. A photo Aras puts into the cache folder
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


def photo_free(lic):
    """True for an open licence: CC BY / CC BY-SA (any version), CC0, public domain."""
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


def fitz_add_photos(path, photos, page_h=297.0):
    """The photos put into a written PDF with PyMuPDF: photos = [(page index, x0, y0, x1, y1 mm, y up from the page
    foot, jpeg path)]; each JPEG fills its frame, cut to the frame's proportions about its centre (never stretched).
    The file is saved in place. Returns how many were placed."""
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
            iw, ih = float(info[0]), float(info[1])
            tmp = fitz.open()
            tp = tmp.new_page(width=iw, height=ih)
            tp.insert_image(tp.rect, stream=data)
            a = (x1 - x0) / (y1 - y0)
            cw, ch = (ih * a, ih) if iw / ih > a else (iw, iw / a)
            doc[pi].show_pdf_page(fitz.Rect(x0 * K, (page_h - y1) * K, x1 * K, (page_h - y0) * K), tmp, 0,
                                  clip=fitz.Rect((iw - cw) / 2.0, (ih - ch) / 2.0, (iw + cw) / 2.0, (ih + ch) / 2.0))
            tmp.close()
            n += 1
        except Exception:
            continue
    if n:
        t_ = path + ".tmp"
        doc.save(t_, garbage=3, deflate=True)
        doc.close()
        os.replace(t_, path)
    else:
        doc.close()
    return n
PHOTOS = []                          # (x0, y0, x1, y1 board mm, y up, jpeg path): embedded after the PDF is written


def pdf_add_images(path, imgs):
    """v1.14: the plant photos put into the written board PDF as an incremental update (src/common/write_pdf has no
    images and is shared by every script, so it is left as it is): the page's old content is wrapped in q ... Q and a
    new content stream draws each JPEG clipped to its frame, cover-fitted (no stretch). imgs: [(x0, y0, x1, y1 mm, y up,
    jpeg path)]. Returns how many were embedded."""
    import re
    ok = []
    for x0, y0, x1, y1, p in imgs:
        try:
            with open(p, "rb") as f:
                d = f.read()
            info = jpeg_info(d)
            if info:
                ok.append((x0, y0, x1, y1, d, info))
        except Exception:
            pass
    if not ok:
        return 0
    with open(path, "rb") as f:
        pdf = f.read()
    m = re.search(rb"\n(\d+) 0 obj\n(<< /Type /Page /Parent .*?)\nendobj", pdf, re.S)
    tr = re.findall(rb"trailer\n<< /Size (\d+) /Root (\d+) 0 R /Info (\d+) 0 R >>\nstartxref\n(\d+)", pdf)[-1]
    size, root, info_, prev = [int(v) for v in tr]
    pid, pdict = int(m.group(1)), m.group(2).decode("latin-1")
    objs = []

    def add(b):
        objs.append(b)
        return size + len(objs) - 1
    q_id = add(b"<< /Length 1 >>\nstream\nq\nendstream")
    names, ops = [], ["Q q 2.834646 0 0 2.834646 0 0 cm"]
    for i, (x0, y0, x1, y1, d, (w, h, nc)) in enumerate(ok):
        oid = add(("<< /Type /XObject /Subtype /Image /Width {} /Height {} /ColorSpace /{} /BitsPerComponent 8 "
                   "/Filter /DCTDecode /Length {} >>\nstream\n".format(w, h, "DeviceRGB" if nc == 3 else "DeviceGray",
                                                                       len(d))).encode("latin-1") + d + b"\nendstream")
        names.append("/Ph{} {} 0 R".format(i + 1, oid))
        fw, fh = x1 - x0, y1 - y0
        k = max(fw / float(w), fh / float(h))            # cover the frame, keep the photo's proportions
        iw, ih = w * k, h * k
        ops.append("q {} {} {} {} re W n {} 0 0 {} {} {} cm /Ph{} Do Q".format(
            _f(x0), _f(y0), _f(fw), _f(fh), _f(iw), _f(ih), _f(x0 + (fw - iw) / 2.0), _f(y0 + (fh - ih) / 2.0), i + 1))
    ops.append("Q")
    st = zlib.compress("\n".join(ops).encode("latin-1"), 6)
    d_id = add(b"<< /Length " + str(len(st)).encode() + b" /Filter /FlateDecode >>\nstream\n" + st + b"\nendstream")
    cm = re.search(r"/Contents (\d+) 0 R", pdict)
    newp = pdict.replace(cm.group(0), "/Contents [{} 0 R {} 0 R {} 0 R]".format(q_id, cm.group(1), d_id), 1)
    newp = newp.replace("/Resources << ", "/Resources << /XObject << {} >> ".format(" ".join(names)), 1)
    out = bytearray(pdf)
    if not out.endswith(b"\n"):
        out += b"\n"
    offs = []
    for i, b in enumerate(objs):
        offs.append(len(out))
        out += "{} 0 obj\n".format(size + i).encode() + b + b"\nendobj\n"
    p_off = len(out)
    out += "{} 0 obj\n".format(pid).encode() + newp.encode("latin-1") + b"\nendobj\n"
    x = len(out)
    out += "xref\n0 1\n0000000000 65535 f \n{} 1\n{:010d} 00000 n \n{} {}\n".format(pid, p_off, size,
                                                                                  len(objs)).encode()
    for o_ in offs:
        out += "{:010d} 00000 n \n".format(o_).encode()
    out += "trailer\n<< /Size {} /Root {} 0 R /Info {} 0 R /Prev {} >>\nstartxref\n{}\n%%EOF\n".format(
        size + len(objs), root, info_, prev, x).encode()
    with open(path, "wb") as fh_:
        fh_.write(bytes(out))
    return len(ok)


# ---------------------------------------------------------------- v1.14 p.22: the plants panel
PLANT_SITES = [  # v6 (T4a WO-T4a-2, p.17 plans): the water spaces, numbered on the plans (R35), in water order:
    # (number, zone code (zone base; ARM = the masterplan's side arm), name, plants.py species planted there). D2:
    # common reed only in the lined basin cells; D6: no iris, water mint only in lined cells; the side arm carries
    # rushes and loosestrife (it is not lined, so no common reed)
    (1, "WT", u"Reed basins, lined", ("reed", "mint")),
    (2, "WD", u"Spillway, clean water back", ("soft_rush",)),
    (3, "GR", u"Shaded walk", ("plane",)),
    (4, "WS", u"Rain terraces", ("olive", "rosemary", "lavender")),
    (5, "STRIP", u"Summer strip", ("soft_rush", "loosestrife")),
    (6, "WP", u"Widened stream and wetland", ("willow", "tamarisk", "chaste", "ash", "soft_rush", "loosestrife")),
    (7, "ARM", u"Side arm", ("soft_rush", "loosestrife")),
]


PHOTO_ON = [True]                    # the photos are fetched / read on a press (set False to leave the frames empty)


# ---------------------------------------------------------------- W4, W6, W7 and the decision row (bergama_water_case v1.1)
# Group 6's tables: A6_strip_storage.csv, A7, DATA_REGISTER rows as named.
# A6_strip_storage.csv: storage needed (m³): (bed, width) -> (measured 2016-2021, -30.7 %, -30.7 % + no inflow May-Oct)
WINTER_FLOW = 18653245          # A7: natural flow Dec-Apr at the site (m³, calculated)
# v1.1: storage design, strip draw and olive need from the water balance (Thread 2), never typed in: its results file
# (written on every run of bergama_water_balance_v2.py), else the default-lands copy of 24 Oct 08:21 (research/
# water_balance/water_balance_results_default.json).
WB_FILES = [os.path.join(bg_cache("Bergama_water_balance_analysis"), "water_balance_results.json"),   # 27 Oct: cached/
            os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "output", "Bergama_water_balance_analysis",
                         "water_balance_results.json"),
            os.path.join(os.path.expanduser("~"), "Downloads", "Bergama_water_balance_analysis",
                         "water_balance_results.json")]
WB_DEFAULT = dict(design=dict(central_range_m3=[350000, 375000], central_range_pct_1in5_dry=[99.2, 99.7]),
                  strip_m3_per_year=23462, net_irrigation_mm=dict(olive=dict(dry5=720.1)))
DRIP_EFF = 0.90                 # water balance v2 (FAO Training Manual 4 ch.3)


def wb_results():
    for p in WB_FILES:
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f), u"water balance results of " + time.strftime(
                    "%d %b %H:%M", time.localtime(os.path.getmtime(p)))
        except Exception:
            pass
    return WB_DEFAULT, u"water balance default lands, 24 Oct"


WB, WB_SRC = wb_results()
WB_LIVE = WB is not WB_DEFAULT          # v6.1: False = the built-in default; p.12 then prints no storage figures
try:
    WB_STORE = tuple(WB["design"]["central_range_m3"])
    WB_PCT = tuple(WB["design"]["central_range_pct_1in5_dry"])
    WB_STRIP = float(WB["strip_m3_per_year"])
    OLIVE_M3_HA = WB["net_irrigation_mm"]["olive"]["dry5"] / DRIP_EFF * 10.0     # m³/ha at the intake, 1-in-5 dry year
except Exception:
    WB, WB_SRC, WB_LIVE = WB_DEFAULT, u"water balance default lands, 24 Oct", False
    WB_STORE, WB_PCT = (350000, 375000), (99.2, 99.7)
    WB_STRIP, OLIVE_M3_HA = 23462.0, 720.1 / DRIP_EFF * 10.0
MIN_FLOW = 1001453              # A7: minimum flow kept in the stream Dec-Apr (m³)
# EN-D1 (Vymazal 2010): removal %, published: BOD5, solids, total P, total N, NH4-N
WETLAND = [(u"Horizontal subsurface flow", (75, 75, 50, 43, 39)), (u"Vertical flow", (90, 89, 56, 43, 73)),
           (u"Free water surface", (74, 77, 34, 45, 48))]
WETLAND_KEYS = [u"BOD5", u"Solids", u"Total P", u"Total N", u"NH4-N"]

# v1.6 (Aras 25 Oct 13:12 "too much text too little visual"): the water case's text panels as pictogram tiles,
# (pictogram, heading, key figure, short line, source); every fact and figure of v1.3's sentences is kept.
# v5 (revision 29 Oct, T3b WO-T3b-2): p.12's tiles became one water map + a column beside it (G7). WHY_T: the two
# published facts kept as pictogram rows (icons.py names); the rainwater-tank and "so the stream is cleaned" tiles are
# gone (the map's COLLECT and CLEAN carry them). (icon, heading, key figure, short line, source)
WHY_T = [
    ("sewage", u"SEWAGE IN THE STREAM", u"3 km + 500 m",
     u"new İZSU sewer + connections, Feb 2024 · against odour, flies",
     u"published, İZSU via Gerçek İzmir 28 Feb 2024; " + REG + u" SE-22"),
    ("treatment", u"TOWN TREATMENT PLANT", u"14,304 m³ a day",
     u"treated, to the Bakırçay, not the Selinos", u"published, TMMOB 2023 citing İZSU; " + WD)]
# HOW_T: what the planting removes, as bars (icon, plant, nutrient, bars (label, %, printed), source). D2 a: the reed
# figure only as the pilot result (slag 88 %, gravel 58 %), reed only in lined cells; D6: loosestrife "TN > 60 %", no P.
# The bed-area tile (Vymazal 2010) is left out; the coliform and UV tiles are the column's coliform chart (COLIFORM).
HOW_T = [
    ("reeds", u"common reed, pilot", u"lined cells · NH4-N", ((u"slag", 88, u"88 %"), (u"gravel", 58, u"58 %")),
     u"Korkusuz et al. 2004, Turk. J. Eng. Env. Sci. 28, aj.tubitak.gov.tr/engineering/issues/muh-04-28-5/"
     u"muh-28-5-6-0406-12.pdf"),          # v6.1: the pilot's public paper (DATA_REGISTER PL-09, confirmed)
    ("plants", u"purple loosestrife", u"TN", ((u"", 60, u"> 60 %"),), None)]
# v2 (Aras 27 Oct, Prompt 4, data honesty): the tiles "water quality measured", "streamside greywater" and "odour cut
# by plants" (all NO DATA) are gone; no source holds a figure for them and an estimate would rest on an unknown.
# v5 (T3b): shorter labels for p.12's chart; the internal register codes out of the sources (D13)
COLIFORM = [  # (label, low, high, colour key, source); 0 = the limit is zero
    (u"left after a planted wetland", 1e2, 1e5, "d2", u"published, reviews 2005 and 2020"),
    (u"reuse class B · orchards", 200, 200, "acc", u"published, 2010 wastewater reuse communiqué"),
    (u"reuse class A · parks", 0, 0, "acc", u"published, 2010 wastewater reuse communiqué"),
    (u"drinking water · E. coli", 0, 0, "acc", u"published, Ministry of Health")]
GOES_T = [
    ("out", u"THE CLEAN STREAM LEAVES THE SITE", None,
     u"-> existing farmland on the slopes outside · no farm channel inside",
     u"design decision, Aras 2026-10-18 14:49, 15:02"),
    ("olive", u"OLIVES HERE, 1-IN-5 DRY YEAR, DRIP", u"{:,.0f} m³ per ha".format(OLIVE_M3_HA),
     u"so 10,000 m³ of stored water serves {:.2f} ha".format(10000.0 / OLIVE_M3_HA),
     u"calculated, FAO-56 soil water balance for Bergama, 34 water years; " + WB_SRC),
    ("plant", u"THE PLANT'S TREATED WATER, 120 SUMMER DAYS", u"about {:,.0f} ha".format(
        round(14304 * 120 / OLIVE_M3_HA / 5.0) * 5),
     u"of olives from 1.72 million m³", u"calculated from 14,304 m³/day; " + WB_SRC),
    ("drought", u"NORTH AEGEAN BASIN: FARMS GET", u"75 % · 29 %",
     u"of demand · normal year · very severe drought",
     u"published, North Aegean water allocation plan 2025; " + REG + u" CL-21"),
    ("nodrink", u"NOT FOR DRINKING", u"arsenic > 10 µg/L",
     u"groundwater · drinking needs 0 E. coli/100 ml · none of it for drinking", u"published, Somay & Gemici 2015; " +
     REG + u" EN-E3")]
AQUIFER = [(u"Groundwater potential", 45.4), (u"Total use", 198.01)]   # hm³/yr, Lower Bakırçay, official (2018)
DECISION = [
    (u"KEEP SEWAGE OUT", u"İZSU sewer (SE-22)"),
    (u"CLEAN AT THE UPSTREAM END", u"reed beds at the entry · whole reach clean"),
    # v3.2 (Aras 27 Oct, Prompt 8): was "10^2-10^5" (no superscript), now as the coliform tile on p.13
    (u"DISINFECT WHERE PEOPLE TOUCH IT", u"wetlands leave 100-100,000 CFU/100 ml · class A: 0"),
    (u"HOLD WINTER WATER", u"{:,.0f}-{:,.0f} m³ incl. strip = {:.1f}-{:.1f} % of Dec-Apr flow".format(
        WB_STORE[0], WB_STORE[1], 100.0 * WB_STORE[0] / WINTER_FLOW, 100.0 * WB_STORE[1] / WINTER_FLOW)),
    (u"KEEP THE STRIP ALIVE", u"clean water all summer · feeds the planting (D8)"),
    (u"THEN THE FARMS", u"farms outside (class B) · 10,000 m³ = {:.2f} ha olives · aquifer used 4.4 x".format(   # v4 (F6)
        10000.0 / OLIVE_M3_HA)),
    (u"NOT FOR DRINKING", u"arsenic > 10 µg/L · stored rain not listed for drinking")]




def icon(pg, kind, x, y, sz):
    """v1.6: a pictogram in the square (x, y - sz)-(x + sz, y), drawn on a 10 x 10 grid. Graphic only."""
    u = sz / 10.0
    lw = 0.07 * sz

    def P(pts):
        return [(x + a * u, y - sz + b * u) for a, b in pts]

    def R(a0, b0, a1, b1):
        return P([(a0, b0), (a1, b0), (a1, b1), (a0, b1)])

    def drop(a, b, r, col):
        pg.poly([P([(a - r * 0.85, b + r * 0.45), (a, b + r * 2.2), (a + r * 0.85, b + r * 0.45)])], fill=col)
        pg.circle(x + a * u, y - sz + b * u, r * u, fill=col)

    ink, ink2, w1, w2, w3, d3, acc, agri = C["dark"], C["ink2"], C["w1"], C["w2"], C["w3"], C["d3"], C["acc"], C["agri"]
    if kind in ("sewage", "sewer_x"):
        pg.poly([R(0, 0.4, 10, 2.6)], fill=w2)
        pg.poly([R(0, 6.0, 5.6, 8.2)], fill=ink2)
        pg.poly([R(5.0, 5.6, 6.0, 8.6)], fill=ink)
        if kind == "sewage":
            drop(6.6, 3.6, 0.65, "7A6448")
            drop(7.4, 1.4, 0.5, "7A6448")
        else:
            pg.line(P([(6.6, 2.8), (9.6, 9.0)]), acc, lw * 1.4)
            pg.line(P([(6.6, 9.0), (9.6, 2.8)]), acc, lw * 1.4)
    elif kind == "gauge":
        pg.poly([P([(3.2, 5.0), (3.2, 2.2), (4.1, 1.2), (5.9, 1.2), (6.8, 2.2), (6.8, 5.0)])], fill=w1)
        pg.line(P([(3, 9.4), (3, 2.0), (4, 0.8), (6, 0.8), (7, 2.0), (7, 9.4)]), ink, lw)
        pg.text(u"?", x + 5.0 * u, y - sz + 5.6 * u, 3.6 * u, acc, bold=True, align="C")
    elif kind == "house":
        pg.poly([R(1.0, 0.6, 6.4, 5.8)], fill=COL["white"], stroke=ink, lw=lw)
        pg.poly([P([(0.2, 5.6), (3.7, 9.2), (7.2, 5.6)])], fill=ink2)
        pg.poly([R(3.0, 0.6, 4.4, 3.4)], fill=ink2)
        drop(8.4, 1.6, 0.9, w3)
        pg.text(u"?", x + 8.4 * u, y - sz + 5.2 * u, 3.0 * u, acc, bold=True, align="C")
    elif kind == "plant":
        pg.poly([R(0, 0.6, 4.2, 6.6)], fill=ink2)
        pg.poly([R(1.0, 6.6, 1.8, 9.0)], fill=ink2)
        pg.circle(x + 6.4 * u, y - sz + 3.0 * u, 1.7 * u, fill=w2, stroke=d3, lw=lw * 0.6)
        pg.circle(x + 8.9 * u, y - sz + 3.0 * u, 1.1 * u, fill=w2, stroke=d3, lw=lw * 0.6)
    elif kind == "tank":
        pg.poly([P([(0, 6.6), (3.8, 9.8), (7.6, 6.6)])], fill=ink2)
        pg.poly([R(0.8, 0.6, 6.8, 6.6)], fill=COL["white"], stroke=ink, lw=lw)
        pg.line(P([(7.4, 6.8), (8.6, 6.8), (8.6, 4.4)]), ink, lw)
        pg.poly([R(7.0, 0.6, 10.0, 4.2)], fill=w2, stroke=d3, lw=lw * 0.6)
    elif kind == "reed":
        pg.poly([R(0, 0, 10, 2.2)], fill=w2)
        for k_ in range(5):
            a = 1.6 + k_ * 1.7
            t = 6.6 + (k_ % 2) * 2.2
            pg.line(P([(a, 0.8), (a + 0.3, t)]), C["wet"], lw)
            pg.poly([R(a - 0.25, t - 1.8, a + 0.85, t + 0.2)], fill=agri)
    elif kind == "area":
        pg.poly([R(0.6, 0.6, 9.4, 9.4)], stroke=ink, lw=lw)
        for t in (3.53, 6.47):
            pg.line(P([(0.6, t), (9.4, t)]), ink2, lw * 0.5)
            pg.line(P([(t, 0.6), (t, 9.4)]), ink2, lw * 0.5)
        pg.circle(x + 5.0 * u, y - sz + 6.6 * u, 0.9 * u, fill=ink)
        pg.poly([R(4.3, 3.2, 5.7, 5.5)], fill=ink)
    elif kind == "nose":
        for k_ in range(3):
            a = 2.4 + k_ * 2.6
            pg.line(P([(a + (0.7 if j % 2 else -0.7), 0.8 + j * 1.6) for j in range(6)]), ink2, lw)
        pg.text(u"?", x + 8.8 * u, y - sz + 0.6 * u, 3.0 * u, acc, bold=True, align="C")
    elif kind == "uv":
        for k_ in range(8):
            a = math.radians(k_ * 45.0)
            pg.line(P([(5 + 3.0 * math.cos(a), 5 + 3.0 * math.sin(a)), (5 + 4.6 * math.cos(a), 5 + 4.6 * math.sin(a))]),
                    d3, lw)
        pg.circle(x + 5.0 * u, y - sz + 5.0 * u, 2.5 * u, fill=C["d2"])
        pg.text(u"UV", x + 5.0 * u, y - sz + 4.3 * u, 1.9 * u, COL["white"], bold=True, align="C")
    elif kind == "olive":
        pg.poly([R(4.5, 0.4, 5.5, 4.4)], fill=ink2)
        pg.circle(x + 5.0 * u, y - sz + 6.2 * u, 3.4 * u, fill=agri)
        for a, b in ((3.8, 6.8), (6.0, 5.4), (5.4, 7.8)):
            pg.circle(x + a * u, y - sz + b * u, 0.5 * u, fill=ink)
    elif kind == "farm":
        pg.poly([P([(0, 0.6), (6.8, 0.6), (10, 5.4), (3.2, 5.4)])], fill=agri)
        for t in (1.8, 3.0, 4.2):
            f = (t - 0.6) / 4.8
            pg.line(P([(0.6 + 3.2 * f, t), (6.8 + 3.2 * f - 0.6, t)]), MP["agriculture"][2], lw * 0.6)
        pg.poly([R(1.0, 7.0, 6.4, 8.6)], fill=w2)
        arrow(pg, P([(5.6, 7.8), (9.6, 7.8)]), d3, lw, 1.8 * u)
    elif kind == "out":
        pg.poly([R(0, 6.2, 6.0, 8.4)], fill=w2)
        arrow(pg, P([(0.6, 7.3), (9.8, 7.3)]), d3, lw * 1.3, 2.0 * u)
        pg.poly([P([(1.2, 0.6), (7.6, 0.6), (10, 4.4), (3.6, 4.4)])], fill=agri)
    elif kind == "drought":
        pg.poly([R(0.8, 0.6, 3.6, 0.6 + 7.5)], fill=C["d2"])                     # 75 % of 10 units
        pg.poly([R(4.6, 0.6, 7.4, 0.6 + 2.9)], fill=C["d2"])                     # 29 %
        pg.line(P([(0.3, 0.6), (8.0, 0.6)]), ink, lw * 0.6)
        pg.circle(x + 8.6 * u, y - sz + 8.6 * u, 1.2 * u, fill=acc)
    elif kind == "nodrink":
        pg.poly([P([(3.3, 5.0), (3.7, 1.2), (6.3, 1.2), (6.7, 5.0)])], fill=w1)
        pg.line(P([(3.0, 9.0), (3.6, 0.8), (6.4, 0.8), (7.0, 9.0)]), ink, lw)
        pg.line(P([(1.2, 8.8), (8.8, 1.2)]), acc, lw * 1.4)
        pg.line(P([(1.2, 1.2), (8.8, 8.8)]), acc, lw * 1.4)
    elif kind == "cube":
        pg.poly([P([(5, 9.8), (9.2, 7.6), (5, 5.4), (0.8, 7.6)])], fill=MP["storage"][0])
        pg.poly([P([(0.8, 7.6), (5, 5.4), (5, 0.4), (0.8, 2.6)])], fill=MP["storage"][1])
        pg.poly([P([(5, 5.4), (9.2, 7.6), (9.2, 2.6), (5, 0.4)])], fill=MP["storage"][2])
    elif kind == "strip":
        pg.poly([R(0, 3.6, 10, 6.4)], fill=w2)
        arrow(pg, P([(0.8, 5.0), (9.4, 5.0)]), COL["white"], lw, 1.8 * u)
        for a in (1.5, 4.5, 7.5):
            pg.line(P([(a, 6.4), (a + 0.3, 8.8)]), C["wet"], lw * 0.8)
    # ---- v1.8 (visual first): pictograms for the chips that replace sentences
    elif kind == "rain":
        for a, b, r in ((3.4, 6.6, 2.0), (5.8, 7.3, 2.4), (7.8, 6.3, 1.6)):
            pg.circle(x + a * u, y - sz + b * u, r * u, fill=w1)
        pg.poly([R(1.4, 4.6, 9.4, 6.4)], fill=w1)
        for a in (2.6, 5.0, 7.4):
            pg.line(P([(a, 3.6), (a - 0.6, 1.0)]), w3, lw)
    elif kind == "sun":
        for k_ in range(8):
            a = math.radians(k_ * 45.0)
            pg.line(P([(5 + 3.2 * math.cos(a), 5 + 3.2 * math.sin(a)), (5 + 4.6 * math.cos(a), 5 + 4.6 * math.sin(a))]),
                    "B08F3A", lw)
        pg.circle(x + 5.0 * u, y - sz + 5.0 * u, 2.4 * u, fill="D9B756")
    elif kind == "drop":
        drop(5.0, 2.6, 2.3, w3)
    elif kind == "slope":
        pg.poly([P([(0.4, 1.0), (9.6, 1.0), (9.6, 5.4)])], fill=C["structure"])
        arrow(pg, P([(8.4, 6.8), (1.4, 3.4)]), d3, lw, 1.8 * u)
    elif kind == "road":
        pg.poly([R(0, 3.0, 10, 7.0)], fill=ink2)
        for a in (0.6, 4.0, 7.4):
            pg.line(P([(a, 5.0), (a + 2.0, 5.0)]), COL["white"], lw * 0.8)
    elif kind == "points":
        for a, b in ((1.6, 2.4), (3.8, 6.2), (5.4, 3.0), (7.4, 7.4), (8.6, 2.2)):
            pg.circle(x + a * u, y - sz + b * u, 0.75 * u, fill=ink)
    elif kind == "spread":
        pg.poly([R(1.6, 1.0, 8.4, 3.6)], fill=w2)
        arrow(pg, P([(4.2, 6.2), (0.4, 6.2)]), d3, lw, 1.6 * u)
        arrow(pg, P([(5.8, 6.2), (9.6, 6.2)]), d3, lw, 1.6 * u)
    elif kind == "over":
        pg.poly([R(0, 0.6, 4.0, 4.6)], fill=C["structure"])
        pg.poly([R(0, 4.6, 10, 6.4)], fill=w2)
        pg.poly([R(4.0, 0.6, 10, 4.6)], fill=w2)
        arrow(pg, P([(2.0, 6.8), (2.0, 9.6)]), d3, lw, 1.4 * u)
    elif kind in ("flag", "warn"):
        pg.poly([P([(5.0, 9.4), (0.6, 1.0), (9.4, 1.0)])], fill=acc)
        pg.text(u"!", x + 5.0 * u, y - sz + 2.0 * u, 5.2 * u, COL["white"], bold=True, align="C")
    elif kind == "flood":
        pg.poly([R(0, 0.6, 10, 5.0)], fill=w2)
        for a in (2.4, 5.0, 7.6):
            pg.line(P([(a, 2.0), (a + 0.3, 9.2)]), C["wet"], lw)
            pg.poly([R(a - 0.2, 7.4, a + 0.9, 9.4)], fill=agri)
    elif kind == "clean":
        drop(5.0, 2.0, 2.6, w3)
        pg.line(P([(3.4, 4.4), (4.6, 3.2), (6.8, 5.8)]), COL["white"], lw * 1.2)
    elif kind == "dry":
        pg.poly([R(0, 0.6, 10, 2.8)], fill=C["structure"])
        for a in (2.0, 5.4, 8.0):
            pg.line(P([(a, 2.8), (a + 0.6, 1.8), (a + 0.1, 0.9)]), ink, lw * 0.6)
        pg.circle(x + 6.2 * u, y - sz + 6.6 * u, 2.2 * u, fill="D9B756")
    elif kind == "days":
        pg.poly([R(1.0, 0.8, 9.0, 8.2)], fill=COL["white"], stroke=ink, lw=lw * 0.7)
        pg.poly([R(1.0, 6.6, 9.0, 8.2)], fill=d3)
        for a in (2.8, 5.0, 7.2):
            for b in (2.4, 4.6):
                pg.circle(x + a * u, y - sz + b * u, 0.55 * u, fill=ink2)
    elif kind == "native":
        pg.poly([P([(2.6, 6.2), (5.0, 0.6), (7.4, 6.2)])], fill=d3)
        pg.circle(x + 5.0 * u, y - sz + 6.4 * u, 2.6 * u, fill=d3)
        pg.circle(x + 5.0 * u, y - sz + 6.4 * u, 1.0 * u, fill=COL["white"])
    elif kind == "scent":
        for k_ in range(3):
            a = 2.4 + k_ * 2.6
            pg.line(P([(a + (0.7 if j % 2 else -0.7), 0.8 + j * 1.6) for j in range(6)]), agri, lw)
    elif kind == "person":
        pg.circle(x + 5.0 * u, y - sz + 8.2 * u, 1.3 * u, fill=ink2)
        pg.poly([P([(3.4, 6.4), (6.6, 6.4), (6.2, 3.4), (5.6, 0.6), (4.4, 0.6), (3.8, 3.4)])], fill=ink2)
    elif kind == "noback":
        arrow(pg, P([(9.4, 5.0), (0.8, 5.0)]), ink2, lw, 2.0 * u)
        pg.line(P([(3.0, 8.4), (7.0, 1.6)]), acc, lw * 1.4)
        pg.line(P([(3.0, 1.6), (7.0, 8.4)]), acc, lw * 1.4)
    elif kind == "pin":
        pg.circle(x + 5.0 * u, y - sz + 5.0 * u, 2.0 * u, fill=acc)
    # ---- v1.14: what people do, feel, hear and touch (p.20-21), plants and the tunnels (p.11, p.22)
    # v4 (MIRAQUA 28 Oct, P19.2 / P15.2): the people pictograms sit, walk, wade, child and the stall are gone: people
    # are common/figures.py silhouettes (r28_fig)
    elif kind == "watch":                                   # an eye: look, keep back
        pg.poly([P([(0.6, 5.0), (2.6, 7.2), (5.0, 8.0), (7.4, 7.2), (9.4, 5.0), (7.4, 2.8), (5.0, 2.0), (2.6, 2.8)])],
                fill=COL["white"], stroke=ink, lw=lw)
        pg.circle(x + 5.0 * u, y - sz + 5.0 * u, 1.8 * u, fill=w3)
        pg.circle(x + 5.0 * u, y - sz + 5.0 * u, 0.8 * u, fill=ink)
    elif kind in ("awe", "joy", "calm", "curious"):         # faces: the feeling we design for
        pg.circle(x + 5.0 * u, y - sz + 5.0 * u, 4.4 * u, fill="F3E6BF", stroke=ink, lw=lw * 0.8)
        if kind == "calm":
            for a in (3.4, 6.6):
                pg.line(P([(a - 0.8, 6.0), (a + 0.8, 6.0)]), ink, lw)
        else:
            for a in (3.4, 6.6):
                pg.circle(x + a * u, y - sz + 6.0 * u, (0.75 if kind == "awe" else 0.55) * u, fill=ink)
        if kind == "awe":
            pg.circle(x + 5.0 * u, y - sz + 3.0 * u, 1.0 * u, fill=ink)
        elif kind == "curious":
            pg.line(P([(4.2, 3.2), (5.8, 3.2)]), ink, lw)
            pg.line(P([(5.8, 7.6), (7.4, 8.2)]), ink, lw * 0.8)
        else:
            d_ = 1.2 if kind == "joy" else 0.5
            pg.line(P([(3.0 + 4.0 * i / 8.0, 3.6 - d_ * math.sin(math.pi * i / 8.0)) for i in range(9)]), ink, lw)
    elif kind in ("snd1", "snd2", "snd3"):                  # loudness we expect: 1 soft, 3 loud (no measurement)
        pg.poly([P([(0.6, 3.8), (2.4, 3.8), (4.8, 1.6), (4.8, 8.4), (2.4, 6.2), (0.6, 6.2)])], fill=ink2)
        for i in range(int(kind[-1])):
            r_ = 1.8 + 1.5 * i
            pg.line(P([(5.2 + r_ * math.cos(t), 5.0 + r_ * math.sin(t)) for t in [-0.8 + 0.2 * j for j in range(9)]]),
                    d3, lw)
    elif kind == "hand":
        pg.poly([R(2.6, 0.6, 7.2, 5.2)], fill="E9C9A6", stroke=ink, lw=lw * 0.5)
        for a, t in ((2.7, 8.2), (3.9, 9.2), (5.1, 9.2), (6.3, 8.4)):
            pg.poly([R(a, 4.8, a + 1.0, t)], fill="E9C9A6", stroke=ink, lw=lw * 0.5)
        pg.poly([P([(7.2, 2.4), (9.2, 4.8), (8.6, 5.6), (7.2, 4.2)])], fill="E9C9A6", stroke=ink, lw=lw * 0.5)
    elif kind == "foot":
        pg.poly([P([(3.4, 0.6), (6.0, 0.8), (6.8, 3.6), (6.4, 6.4), (4.0, 6.8), (3.0, 4.0)])], fill="E9C9A6",
                stroke=ink, lw=lw * 0.5)
        for a, b, r_ in ((3.6, 8.0, 0.8), (5.1, 8.6, 0.7), (6.4, 8.2, 0.6), (7.4, 7.2, 0.5)):
            pg.circle(x + a * u, y - sz + b * u, r_ * u, fill="E9C9A6", stroke=ink, lw=lw * 0.5)
    elif kind == "gravel":
        for a, b, r_ in ((2.0, 2.0, 1.2), (4.6, 1.6, 1.0), (7.4, 2.2, 1.4), (3.2, 4.2, 0.9), (6.0, 4.0, 1.1),
                         (8.4, 4.6, 0.8)):
            pg.circle(x + a * u, y - sz + b * u, r_ * u, fill=C["structure"], stroke=ink2, lw=lw * 0.4)
        pg.circle(x + 5.0 * u, y - sz + 7.6 * u, 1.6 * u, fill="E9C9A6")
    elif kind == "tunnel":                                  # the Red Hall twin vaults, seen from the mouth
        for a in (0.4, 5.4):
            pg.poly([P([(a, 0.6)] + [(a + 2.1 + 2.1 * math.cos(math.pi - math.pi * j / 10.0),
                                      5.4 + 2.8 * math.sin(math.pi * j / 10.0)) for j in range(11)] + [(a + 4.2, 0.6)])],
                    fill=COL["white"], stroke=ink, lw=lw)
            pg.poly([R(a + 0.3, 0.6, a + 3.9, 2.6)], fill=w2)
    elif kind in ("hub_open", "hub_closed"):                # the in-bed sub-hub: open at low water, shut in floods
        pg.poly([P([(0.4, 0.6), (9.6, 0.6), (9.6, 2.2), (7.4, 2.2), (7.4, 3.8), (5.2, 3.8), (5.2, 5.4), (0.4, 5.4)])],
                fill=C["structure"])
        if kind == "hub_open":
            pg.line(P([(5.8, 8.0), (7.2, 6.6), (9.6, 9.4)]), "5E8A3A", lw * 1.6)
        else:
            pg.poly([R(0.0, 0.6, 10.0, 4.6)], fill=w2, alpha=0.8)
            pg.line(P([(6.2, 6.4), (9.4, 9.6)]), acc, lw * 1.6)
            pg.line(P([(6.2, 9.6), (9.4, 6.4)]), acc, lw * 1.6)
    elif kind == "tree":
        pg.poly([R(4.5, 0.4, 5.5, 4.4)], fill="5B5147")
        for a, b, r_ in ((3.4, 6.0, 2.6), (6.6, 6.0, 2.6), (5.0, 7.6, 2.6)):
            pg.circle(x + a * u, y - sz + b * u, r_ * u, fill=TREE_STYLES["tree"]["mid"])
    elif kind == "lav":
        for a in (2.4, 5.0, 7.6):
            pg.line(P([(5.0, 0.6), (a, 6.4)]), "727A4E", lw)
            pg.poly([R(a - 0.6, 6.2, a + 0.6, 9.4)], fill="9F86C0")


def chips(pg, x, y, items, fs, w=None, colour=None, bold=False):
    """v1.8 (visual first): pictogram chips [(pictogram, keyword)] in a row from the top y, wrapped at width w.
    Returns the bottom y."""
    ic, gap = fs * 1.6, fs * 1.5
    cx, cy = x, y
    for kind, t in items:
        tw = ic + fs * 0.45 + text_w(t, fs, bold)
        if w and cx > x and cx + tw > x + w:
            cx, cy = x, cy - ic - fs * 0.6
        icon(pg, kind, cx, cy, ic)
        pg.text(t, cx + ic + fs * 0.45, cy - ic * 0.5 - fs * 0.36, fs, colour or C["ink"], bold=bold)
        cx += tw + gap
    return cy - ic


def figs(pg, x, y, items, w, big=3.0, small=1.55, colour=None):
    """v1.8: callouts: a big figure with a keyword under it, side by side in width w; items [(figure, keyword)].
    Returns the bottom y."""
    cw = w / float(len(items))
    low = y
    for i, (f, k) in enumerate(items):
        xx = x + i * cw
        pg.text(f, xx, y - big, big, colour or C["d3"], bold=True)
        yy = y - big - small * 1.35
        for ln in wrap(k, small, cw - 1.5):
            pg.text(ln, xx, yy, small, C["ink"])
            yy -= small * 1.3
        low = min(low, yy)
    return low


def tiles(pg, x, y, w, items, s, cols=2, extra=0.0):
    """v1.6: facts as tiles: pictogram, heading, the key figure large, a short line and its source number.
    items = [(pictogram, heading, figure or None, line, source)]. Returns the bottom y. v2: extra = mm added to every
    row's height, the content centred in it (draw_cleaning fills its column with no gap at the bottom)."""
    fh, fb, ft = 2.5 * s, 4.4 * s, 2.15 * s
    ic, pad, g = 10.0 * s, 2.2 * s, 2.4 * s
    tw = (w - (cols - 1) * g) / cols
    txw = tw - ic - 3 * pad
    lay = []
    for kind, head, big, line, src in items:
        L = (wrap(head, fh, txw, True), wrap(big, fb, txw, True) if big else [],
             wrap(line + (u" " + cite(src) if src else u""), ft, txw))
        hh = pad * 2 + len(L[0]) * fh * 1.25 + len(L[1]) * fb * 1.18 + len(L[2]) * ft * 1.28 + (fh * 0.3 if L[1] else 0)
        lay.append((kind, big, L, max(hh, ic + 2 * pad)))
    yy = y
    for r0 in range(0, len(lay), cols):
        row = lay[r0:r0 + cols]
        rh = max(t[3] for t in row) + extra
        for c_, (kind, big, L, _) in enumerate(row):
            tx = x + c_ * (tw + g)
            pg.poly([rect(tx, yy - rh, tx + tw, yy)], fill=C["paper"], stroke=C["faint"], lw=0.2)
            icon(pg, kind, tx + pad, yy - pad - extra / 2.0, ic)
            lx, ly = tx + 2 * pad + ic, yy - pad - extra / 2.0
            for ln in L[0]:
                ly -= fh * 1.25
                pg.text(ln, lx, ly, fh, C["dark"], bold=True)
            if L[1]:
                ly -= fh * 0.3
            for ln in L[1]:
                ly -= fb * 1.18
                pg.text(ln, lx, ly, fb, C["acc"] if big == u"NO DATA" else C["d3"], bold=True)
            for ln in L[2]:
                ly -= ft * 1.28
                pg.text(ln, lx, ly, ft, C["ink"])
        yy -= rh + g
    return yy + g




DEC_ICONS = ["sewer_x", "reed", "uv", "cube", "strip", "farm", "nodrink"]


LOOP_BACK = u"next winter: new stream water refills the storage · one way, nothing pumped back"


# ---------------------------------------------------------------- W4 cubes and the farm pictogram (water loop v2)
SLAB_T_M = 10.0                      # pictogram slab thickness, graphic only


class BoxView(object):
    """Axonometric view for things not on the site: plan axes turned by ang, k mm per m (water loop v2)."""

    def __init__(self, theta, ang, k, ox, oy):
        self.t, self.p, self.ang, self.k, self.ox, self.oy = math.radians(theta), math.radians(PHI), ang, k, ox, oy

    def __call__(self, u, v, z):
        x = u * math.cos(self.ang) - v * math.sin(self.ang)
        y = u * math.sin(self.ang) + v * math.cos(self.ang)
        d = x * math.cos(self.t) + y * math.sin(self.t)
        return (self.ox + (x * math.sin(self.t) - y * math.cos(self.t)) * self.k,
                self.oy + (d * math.sin(self.p) + z * math.cos(self.p)) * self.k)

    def visible(self, nu, nv):
        x = nu * math.cos(self.ang) - nv * math.sin(self.ang)
        y = nu * math.sin(self.ang) + nv * math.cos(self.ang)
        return x * -math.cos(self.t) + y * -math.sin(self.t) > 1e-9, (x * math.sin(self.t) - y * math.cos(self.t)) < 0




# ---------------------------------------------------------------- the board (A0 landscape, one page)
def load_palette(dirs, log):
    for d in dirs:
        for p in (os.path.join(d, "bergama_palette.py"), os.path.join(d, "palette", "bergama_palette.py")):
            if not os.path.isfile(p):
                continue
            try:
                m = _types.ModuleType("bergama_palette")
                exec(compile(open(p, encoding="utf-8").read(), p, "exec"), m.__dict__)
                for k in ("paper", "faint", "structure", "ink2", "ink"):
                    COL[k] = m.CORE.get(k, COL[k])
                for k, a in MP.items():
                    e = m.MASTERPLAN.get(k)
                    if e:
                        MP[k] = (e["light"], e["mid"], e["dark"])
                riv = m.MASTERPLAN.get("river")
                if riv:
                    COL["river"], COL["river_mid"], COL["river_dark"] = riv["light"], riv["mid"], riv["dark"]
                for k in ("aras_alan", "begum_alan", "nil_alan"):
                    COL[k] = m.STUDY_AREA.get(k, {}).get("line", COL[k])
                log.append(u"Palette read from " + p)
                return u"palette {} (version {})".format(os.path.basename(p), getattr(m, "VERSION", "?"))   # 25 Oct: no local path on the sheet
            except Exception as ex:
                log.append(u"WARNING: palette file {} not read ({}); embedded v1.4 colours used".format(p, ex))
    return u"embedded palette v1.4 colours"


def boxed(fn):
    """A water case panel drawn with 4 mm side padding instead of its own 10 mm."""
    return lambda pg, x, y, w, h, s: fn(pg, x - 6.0, y, w + 12.0, h, s)


def fit_draw(pg, fn, box, hi=1.6):
    x0, y0, x1, y1 = box
    s = fit(fn, x0, y1, x1 - x0, y1 - y0, 2.0, 0.5, hi)
    fn(pg, x0, y1, x1 - x0, y1 - y0, s)
    return s


def draw_title(pg, x0, y0, x1, y1, opt, storage):
    pg.text(u"Water Loop", x0, y1 - 12.0, 12.0, COL["ink_dark"], bold=True)
    pg.text(u"HOW MUCH · WHEN · HOW HIGH · CLEAN · HOLD · GIVE BACK", x0, y1 - 18.0, 2.9, MP["discharge"][2], bold=True)
    pg.text((u"PanelReview1A · organic forms only where the project meets the water" if opt == "A" else
             u"PanelReview1B · no organic forms anywhere") +
            u" · storage as cubes",
            x0, y1 - 22.5, 2.4, COL["ink"])
    tx = x0 + 330.0
    y = chips(pg, tx, y1 - 1.0, CONCEPT_CHIPS, 2.6, 470.0, COL["ink"], True)    # v1.8: was the CONCEPT paragraph
    pg.text(u"one way, with the stream " + cite(CONCEPT[1]), tx, y - 3.0, 2.0, COL["ink2"])
    pg.line([(x0, y0), (x1, y0)], COL["structure"], 0.3)


def draw_footer(pg, x0, y0, x1, pal_line):
    """v1.14: no source lines on the sheet (Aras 27 Oct: "delete ... source footers"); the numbered key goes to the
    booklet's blocks.json (sheet_sources) and the log. v4 (MIRAQUA 28 Oct, G1): no project or course line; the
    version and the palette only (outside every booklet crop)."""
    pg.text(u"{} · {}".format(VERSION, pal_line), x0, y0 + 3.0, 1.9, COL["ink2"])


BK_CROPS = []                        # v1.10: (id, (x0, y0, x1, y1) board mm y up, scale_den, legend, drop) per panel


def crop_add(cid, bb, den=None, legend=None, drop=None, pad=1.0):
    BK_CROPS.append((cid, (bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad), den, legend or [], drop or []))


def drawn(pg, fn):
    """Runs fn() (which draws onto pg) and returns the bbox of what it added."""
    n0 = len(pg.items)
    fn()
    return items_bbox(pg.items[n0:])


# v1.12 (Aras 26 Oct 07:06): every diagram carries a short context line, inside its panel's crop. v1.14: shorter.
# v4 (MIRAQUA 28 Oct, G5): one or two **bold** keywords in each (context() sets them)
CONTEXT = {
    "water": u"The Selinos brings its water in **winter** and almost none in summer, and in a flood it rises {} m above "
             u"the bed. So winter water is held, and nothing fixed may **narrow the bed**.",
    "system": u"**One way**, with the stream: cleaned once at the upstream entry, winter water **held** in the ground "   # v5 (T3b): p.12's conclusion
              u"for the dry summer, the stream given back clean to the **farms** downstream. Nothing is pumped back.",
    "concept": u"The idea in section at the upstream entry and at K4: the **problem** on site and the **one move** that "
               u"answers it. Numbers as in the chain.",
    "farms": u"Where the clean water ends up: **farmland outside** the site, easing an aquifer used 4.4 times its "
             u"potential. **Never drinking water**.",
    "seasons": u"One cut, one viewpoint, four seasons: the **water level** decides what the place becomes, which "
               u"**plants** are in leaf or flower, and which **animals** are about.",
    "ne": u"The north-east bank of S4: **seat steps** and a **raised promenade** over Q500 stay; the planting follows "
          u"the **days under water**, the use follows the months.",
}
CTX_FS = FS_MIN                      # context line size, mm (7.5 pt when the panel prints 1:1 on A3)
#                                      (booklet v15: 392 x 243 mm less the strip, two captions and the row gap; v1.14: 377 x 195)


def context(pg, x, y, w, key, *args):
    """The panel's context line from its top y; returns the box (x0, y0, x1, y1) it took. v4: **bold** keywords (G5)."""
    yy = r28_para(pg, x, y, w, CONTEXT[key].format(*args), CTX_FS, COL["ink"])
    return (x, yy - CTX_FS * 0.3, x + w, y)


def union(*bbs):
    return (min(b[0] for b in bbs), min(b[1] for b in bbs), max(b[2] for b in bbs), max(b[3] for b in bbs))


def build_board(opt, storage, parts, pal_line, log):
    """v1.14 (Aras 27 Oct 11:07): a 3 x 3 grid of A3-page panels, each one booklet page at about 1:1, drawings at their
    own round scale:
      row 1  how the water behaves (p.11) · what we do with it (p.12) · where the clean water goes (p.23)
      row 2  S4 north-east bank (p.15) · four seasons on one cut (p.14, the wider middle cell) · planting and water A (p.17)
      row 3  the idea in section, upstream entry and K4 (not in the booklet) · planting and water B, the sections (p.17)"""
    pg = Page(BOARD_W, BOARD_H)
    pg.poly([rect(0, 0, BOARD_W, BOARD_H)], fill=COL["sheet"])
    del BK_CROPS[:]
    del PHOTOS[:]
    X0, X1, G = M, BOARD_W - M, 6.0
    y_title = BOARD_H - M - 26.0
    draw_title(pg, X0, y_title, X1, BOARD_H - M, opt, storage)
    ch = 252.0
    cws = [377.0, 395.0, 377.0]               # the middle column a little wider (v3: the four seasons at 1:250 fill it)
    cws[1] = X1 - X0 - 2 * G - cws[0] - cws[2]

    def cell(c, r, title, span=None):
        x0 = X0 + sum(cws[:c]) + c * G
        y1 = y_title - G - r * (ch + G)
        b = frame(pg, (x0, y1 - ch, x0 + (span or cws[c]), y1), title)
        return (b[0], b[1] + 1.0, b[2], b[3] - 1.0)

    def fits(part, w, h):
        pb = items_bbox(part.items)
        return pb[2] - pb[0] <= w and pb[3] - pb[1] <= h

    # row 1 -------------------------------------------------------------- p.11 how the water behaves
    b = cell(0, 0, u"HOW THE WATER BEHAVES · the year, and how high the stream rises")
    q5 = [c_["dep"][4] for c_ in CUTS if c_.get("bed") is not None]
    cb = context(pg, b[0], b[3], b[2] - b[0], "water", u"{:.1f}-{:.1f}".format(min(q5), max(q5)))
    _, by = place(pg, parts["year"], (b[0], b[1], b[2], cb[1] - 3.0), 1.0, "TL", log, "year of the water")
    box = (b[0], b[1], b[2], by[1] - 5.0)
    part, den = draw_sections(opt, (box[2] - box[0], box[3] - box[1]))
    s, bs = place(pg, part, box, 1.0, "TL", log, "stream height")
    if s < 0.999:
        log.append(u"NOTE: the stream-height cuts are printed at {:.0f} % of 1:{:,.0f}".format(100 * s, den))
    log.append(u"p.11: the cuts at 1:{:,.0f}".format(den / s))
    CUTS_DEN[0] = den / s
    crop_add("wb_water", union(cb, by, bs), den / s)
    # p.12 (v5, revision 29 Oct, T3b): pages/p12_system.py draws the whole panel (the water map and what stays beside
    # it) and returns its crops [(crop id, bbox, scale denominator or None)]
    b = cell(1, 0, P12_TITLE)
    for cid_, bb_, den_ in p12_page(pg, b, opt, storage, log):
        crop_add(cid_, bb_, den_)
    # p.23 where the clean water goes, over the seven steps the figures support (no content change in v1.14)
    b = cell(2, 0, u"WHERE THE CLEAN WATER GOES (10, 11) · and what the figures support")
    cb = context(pg, b[0], b[3], b[2] - b[0], "farms")
    yf = cb[1] - 3.0
    split = b[0] + (b[2] - b[0]) * 0.64
    bt = drawn(pg, lambda: fit_draw(pg, boxed(draw_farms_text), (b[0], yf - 112.0, split, yf)))
    _, bp = place(pg, parts["farm"], (split + 3.0, yf - 112.0, b[2], yf), 1.4, "C", log, "farm pictogram")
    crop_add("wb_farms", union(cb, bt, bp))
    yd = min(bt[1], bp[1]) - 5.0
    dw, dh = b[2] - b[0], yd - b[1]
    crop_add("wb_decision", drawn(pg, lambda: draw_decision(pg, b[0], yd, dw, dh,
                                                              fit(draw_decision, b[0], yd, dw, dh, 1.0, 0.5, 1.2))))
    # row 2 -------------------------------------------------------------- pp.14-15, the S4 pair
    # v5 (revision 29 Oct, T3b): pages/p14_15_s4.py draws both panels whole (p.14 in the wider middle cell, p.15 in the
    # left one) and returns their crops [(crop id, bbox, scale denominator or None)]
    for c_, r_, title_, fn_ in ((1, 1, P14_TITLE, p14_page), (0, 1, P15_TITLE, p15_page)):
        b = cell(c_, r_, title_)
        for cid_, bb_, den_ in fn_(pg, b, opt, log):
            crop_add(cid_, bb_, den_)
    # p.17 (v6, revision 29 Oct, T4a): pages/p17_planting.py draws page A (the plans, water spaces, catalogue) whole and
    # returns its crops [(crop id, bbox, scale denominator or None)]; page B (the sections) sits in row 3
    b = cell(2, 1, P17_TITLE)
    for cid_, bb_, den_ in p17_page(pg, b, opt, log):
        crop_add(cid_, bb_, den_)
    # row 3 -------------------------------------------------------------- the idea in section (not in the booklet), p.17 B
    # v6: the two concept sections take the first two columns; the third holds p.17's page B (the sections at 1:500)
    for j, (key, title) in enumerate((("concept_up", u"THE IDEA IN SECTION · upstream entry"),
                                      ("concept_k4", u"THE IDEA IN SECTION · K4 bridge"))):
        bx = cell(j, 2, title)
        cb = context(pg, bx[0], bx[3], bx[2] - bx[0], "concept") if j == 0 else (bx[0], bx[3], bx[0], bx[3])
        _, bu = place(pg, parts[key], (bx[0], bx[1], bx[2], cb[1] - 3.0), 1.6, "C", log, key)
        crop_add("wb_" + key, union(cb, bu) if j == 0 else bu)
    b = cell(2, 2, P17B_TITLE)
    for cid_, bb_, den_ in p17b_page(pg, b, opt, log):
        crop_add(cid_, bb_, den_)
    draw_footer(pg, X0, 1.5, X1, pal_line)
    return pg


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


# ---------------------------------------------------------------- A3 booklet (v1.10; booklet/CROP_SPEC.md, Aras 25 Oct 21:47)
# The booklet shows this board's own drawings: one crop per panel of the sheet (the rects build_board records in
# BK_CROPS from its own layout), and results.json with the figures the booklet reads. Nothing is drawn twice.
BK_CAPTIONS = {
    "wb_water": u"How the water behaves: the year, and how high the stream rises",
    "wb_system": u"What we do with it: collect, clean, hold, give back",
    "wb_concept_up": u"Upstream entry: the idea in section", "wb_concept_k4": u"K4: the idea in section",
    "wb_s4_seasons": u"S4 through the seasons", "wb_s4_ne": u"S4 north-east bank and the year",
    "wb_plants": u"Planting and water: where each plant goes",
    "wb_plants_b": u"Planting and water in section: four cuts, the species and their year",
    "wb_farms": u"Where the clean water goes", "wb_decision": u"What the figures support"}


BK_FIXED = ("wb_s4_seasons", "wb_s4_ne", "wb_plants", "wb_plants_b")   # v3 (Prompt 5): laid out as their booklet page, at 1:1


def res_s4_cut():
    """The S4 cut in the form of CUTS: ground every 1 m above the bed low point, bed, the highest day, Q100 and Q500
    and their wet widths, the road edges; levels as the S4 detail prints them."""
    E = detail_engine()
    prof = _DET_PROF[0] if _DET_PROF else (E["PROFILE_S0"], E["PROFILE_DS"], E["PROFILE_Z"])
    bed = E["THALWEG"][1]
    s0, s1 = 548, 660
    g = [E["prof_z"](prof, float(s)) - bed for s in range(s0, s1 + 1)]
    hd = next(w[0] for s in E["SEASONS"] if s["key"] == "winter" for w in s["water"] if "highest" in w[2]) - bed
    dep = (None, hd, None, E["Q100"] - bed, E["Q500"] - bed)
    i0 = min(range(len(g)), key=lambda i: g[i])
    ext = [None] * 5
    for k in (1, 3, 4):
        a = b = i0
        while a > 0 and g[a - 1] < dep[k]:
            a -= 1
        while b < len(g) - 1 and g[b + 1] < dep[k]:
            b += 1
        ext[k] = (s0 + a - 0.5, s0 + b + 0.5)
    road = [s for s, what, z in E["SURVEY_MARKS"] if what.startswith("road edge")]
    return dict(key="s4", bed=bed, u0=s0, ground=g, dep=dep, ext=ext, road=(min(road), max(road)) if road else None)


def res_bank_top(g, i0, step):
    """(toe, crest) index of the bank going out from the bed at i0 in direction step: a steep rise (0.15 m or more
    per metre, 0.5 m or more in all) with level or falling ground behind it (the next 5 m within 0.15 m of its top);
    the crest is the highest point of that top. None if the cut shows none."""
    i, toe = i0, None
    while 0 <= i + step < len(g):
        if g[i + step] - g[i] >= 0.15:
            toe = i if toe is None else toe
        elif toe is not None:
            behind = [j for j in range(i, i + 6 * step, step) if 0 <= j < len(g)]
            if g[i] - g[toe] >= 0.5 and len(behind) == 6 and max(g[j] for j in behind) - g[i] <= 0.15:
                return toe, max(behind, key=lambda j: g[j])
            toe = None
        i += step
    return None


def bk_results():
    """The figures the booklet reads (same keys as v1.9's results.json)."""
    res = {"script": GH_LABEL, "version": SHORT}
    d_jul = RAIN[6] - EVAP[6]
    tot = float(sum(RIVER))
    res["year"] = {"rain_mm_year": round(sum(RAIN), 1), "evaporation_mm_year": round(sum(EVAP), 1),
                   "july_rain_minus_evaporation_mm": round(d_jul, 1),
                   "surplus_months": [MONTHS[m] for m in WY if RAIN[m] > EVAP[m]],
                   "stream_m3_year": int(sum(RIVER)),
                   "stream_dec_apr_pct": round(100.0 * sum(RIVER[m] for m in (11, 0, 1, 2, 3)) / tot, 1),
                   "stream_jul_sep_m3_month": [RIVER[m] for m in (6, 7, 8)]}
    dates = {}
    for doy, nm in ((LEAF_OFF, "leaf_fall"), (LEAF_ON, "leaf_out")):
        dd = datetime.date(2021, 1, 1) + datetime.timedelta(days=doy - 1)
        dates[nm] = u"{} {}".format(dd.day, MONTHS[dd.month - 1])
    res["greenness"] = {"july_riparian": NDVI[0][4][6], "july_rest_of_frame": NDVI[1][4][6],
                        "leaf_out": dates["leaf_out"], "leaf_fall": dates["leaf_fall"]}
    cuts = {c["key"]: c for c in CUTS}
    cuts["s4"] = res_s4_cut()
    res["cuts"] = {}
    for key in ("up", "k4", "k5", "down", "s4", "flat"):
        cut = cuts[key]
        g, u0, dep, ext = cut["ground"], cut["u0"], cut["dep"], cut["ext"]
        i0 = min(range(len(g)), key=lambda i: g[i])
        info = {"bed": round(cut["bed"], 2), "highest_day_m": round(dep[1], 2), "q100_m": round(dep[3], 2),
                "q500_m": round(dep[4], 2), "q100_level": round(cut["bed"] + dep[3], 2),
                "q500_level": round(cut["bed"] + dep[4], 2)}
        for step, side in ((-1, "right"), (1, "left")):
            bt = res_bank_top(g, i0, step)
            if not bt:
                continue
            toe, tp = bt
            flooded = False
            for lev in (3, 4):
                a, b = ext[lev]
                reach = (a - u0) if step < 0 else (b - u0)
                if dep[lev] > g[tp] + 0.005 and (reach - tp) * step > 0.5:
                    flooded = True
            if flooded:
                info["over_%s_bank_q500_m" % side] = round(dep[4] - g[tp], 2)
                info["%s_bank_top_m" % side] = round(g[tp], 2)
        res["cuts"][key] = info
    res["cuts_scale"] = u"1:{:,.0f} across and up".format(CUTS_DEN[0] or 1000.0 / SECT_K)
    mix = u"orchard olive + cropland cotton"
    try:
        v_seal = float(WB["today_strip_storage"][mix]["storage_m3"])
    except Exception:
        v_seal = VOL_SEALED
    try:
        v_cut = float(WB["design"]["storage_m3"])
    except Exception:
        v_cut = float(WB_STORE[1])
    res["storage"] = {"first_fill_m3": VOL_FIRST, "strip_sealed_m3": v_seal, "strip_unsealed_m3": VOL_UNSEALED,
                      "cut_off_m3": v_cut, "edges_m": [round(v ** (1.0 / 3.0), 1) for v in
                                                       (VOL_FIRST, v_seal, VOL_UNSEALED, v_cut)],
                      "scale": u"1:{:,.0f}".format(CUBE_SCALE)}
    res["cleaning"] = {"removal_pct": {nm: dict(zip(WETLAND_KEYS, vals)) for nm, vals in WETLAND},
                       "wetland_coliforms_per_100ml": [COLIFORM[0][1], COLIFORM[0][2]],
                       "class_b_limit": COLIFORM[1][1], "class_a_limit": 0}
    E = detail_engine()
    res["seasons"] = {}
    for key in ("winter", "spring", "summer", "autumn"):
        sea = [s for s in E["SEASONS"] if s["key"] == key][0]
        res["seasons"][key] = {"water_m_above_bed": [round(w[0] - E["THALWEG"][1], 2) for w in sea["water"]],
                               "strip_held": sea["strip_held"]}
    return res


def booklet_export(folder, pdf_path, log):
    """Writes output/<folder>/booklet/: blocks.json (one crop per panel of the sheet) and results.json."""
    bk = BkBlocks(folder, GH_LABEL, SHORT)
    name = os.path.basename(pdf_path)
    for cid, (x0, y0, x1, y1), den, legend, drop in BK_CROPS:
        r = (max(0.0, x0), max(0.0, BOARD_H - y1), min(BOARD_W, x1), min(BOARD_H, BOARD_H - y0))
        bk.crop(cid, name, r, caption=BK_CAPTIONS.get(cid, u""),
                scale_den=round(den) if den else None, legend=legend, drop=drop)
        if cid in BK_FIXED:                          # v3: printed at 1:1 on its A3 page (booklet v15 keeps "bk_w")
            bk.d["blocks"][cid]["bk_w"] = round(r[2] - r[0], 3)
    with open(bk.path("results.json"), "w", encoding="utf-8") as f:
        json.dump(bk_results(), f, ensure_ascii=False, indent=1)
    # v1.14: the sheet prints no source key any more; the [n] marks of its crops refer to this list (booklet sources
    # page; same key as the city link's)
    bk.d["sheet_sources"] = {"0": [u"[{}] {}".format(i + 1, k) for i, k in enumerate(SRC_KEY)]}
    bk.save()
    log.append(u"booklet: {} crops of {}, results.json".format(len(BK_CROPS), name))


# ---------------------------------------------------------------- run
def out_folder(doc):
    # v1 24 Oct: all files under Downloads/Bergama/ (Aras rule); was next to the .3dm / .gh, else Documents
    return bg_output(OUT_FOLDER)                    # final PDFs only (27 Oct)


DATA_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "Data")   # 25 Oct: every data file here


def search_dirs(doc):
    ds = []
    for p in (getattr(doc, "Path", None),):
        if p:
            ds.append(os.path.dirname(p))
    try:
        g = ghenv.Component.OnPingDocument().FilePath                # noqa: F821
        if g:
            ds.append(os.path.dirname(g))
    except Exception:
        pass
    more = []
    for d in ds:
        more += [d, os.path.dirname(d), os.path.dirname(os.path.dirname(d))]
    return [d for i, d in enumerate(more) if d and d not in more[:i]]


def build_all(doc, log):
    pal_line = load_palette([DATA_DIR] + search_dirs(doc), log) if doc is not None else u"embedded palette v1.4 colours"
    folder = out_folder(doc)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    files = []
    for opt in OPTIONS:
        parts = {"year": draw_year(opt), "concept_up": draw_concept("up", opt), "concept_k4": draw_concept("k4", opt),
                 "farm": draw_farm_picto(opt)}
        for st in STORAGE_STYLES:
            t0 = time.time()
            pg = build_board(opt, st, parts, pal_line, log)
            path = os.path.join(folder, OUT_NAME.format(opt, st))
            try:
                write_pdf(pg, path, u"Bergama water board {} {} {}".format(SHORT, opt, st))
            except (IOError, OSError):
                path = path.replace(".pdf", datetime.datetime.now().strftime("_%H%M%S.pdf"))
                write_pdf(pg, path, u"Bergama water board {} {} {}".format(SHORT, opt, st))
                log.append(u"(the old PDF was open in another program, so a new name was used)")
            try:                                    # v1.14: the plant photos; never breaks the board
                n_ = pdf_add_images(path, PHOTOS)
                if n_:
                    log.append(u"plant photos embedded: {}".format(n_))
            except Exception as ex_:
                log.append(u"plant photos not embedded: {}: {}".format(type(ex_).__name__, ex_))
            files.append(path)
            log.append(u"{}  {}  {:.1f} s".format(os.path.basename(path), datetime.datetime.now().strftime("%H:%M:%S"),
                                                   time.time() - t0))
    return folder, files


# p.12 the water system (split from code.py on 29 Oct 2026). v5 (revision 29 Oct 2026, T3b WO-T3b-2, package C items
# 1-4): ONE diagrammatic map replaces the chain ribbon, the storage cubes and the cleaning tiles. An axonometric of the
# site (the shared basemap, survey m -> page through _p12_axo) carries the project's verbs where they happen (collect,
# clean, hold, give back, to the farms; idea of R03), the volumes and yearly flows as figures on the drawing (R04; read
# live from water_balance_results.json = WB, never typed in), the programme as icons along the strip (R05, icons.py)
# and ONE circular zoom: the upstream entry as a PLAN at 1:2,000 with its scale bar and north arrow (not a perspective).
# Positions come only from project data: the Option A zones and water links of the zone base (the water balance v6
# writes them to its results, key "zones"), the Selinos line and the four places of P12_PLACES. What the map makes
# redundant is gone (the cubes, the IN/OUT lines, the tiles); what stays sits beside it (G7): the logic in five rows,
# the coliform chart, the plants' removal bars (D2, D6), why we clean, one short conclusion.

P12_TITLE = u"CLEANED ONCE, HELD OVER WINTER, GIVEN BACK CLEAN TO THE FARMS · one way, with the stream"

# the Selinos line, survey m, upstream first: agriculture data/GEO.py "selinos" as proposal sections PS_KEY_SELINOS,
# thinned to 2 m (Douglas-Peucker); only the flow direction and the arrows use it (the water itself is the basemap's)
P12_SELINOS = [
    (29642.6, 32739.4), (29633.1, 32660.6), (29643.3, 32638.1), (29671.3, 32612.4), (29710.7, 32540.0),
    (29769.1, 32480.8), (29784.7, 32450.4), (29789.1, 32431.9), (29777.7, 32369.0), (29781.7, 32325.3),
    (29795.2, 32299.4), (29822.6, 32279.6), (29865.9, 32271.5), (29920.8, 32274.0), (29974.1, 32261.0),
    (29985.8, 32252.3), (30000.2, 32215.9), (30005.5, 32176.9), (30022.8, 32126.7), (30052.7, 32087.9),
    (30148.1, 31931.0), (30200.4, 31867.1), (30275.6, 31802.4), (30345.9, 31706.8), (30378.4, 31640.0),
    (30405.5, 31555.5), (30444.1, 31464.0), (30493.0, 31382.7), (30593.4, 31294.4), (30682.7, 31240.2),
    (30753.5, 31180.3), (30833.2, 31152.0), (30935.6, 31090.4), (30987.4, 31044.7), (31015.8, 31010.8),
    (31137.6, 30847.4), (31154.8, 30764.8), (31158.1, 30761.4), (31242.2, 30700.3), (31308.9, 30668.1),
    (31393.4, 30634.5)]
# the four places of the project's chain, survey m: the upstream entry and downstream reach = the surveyed cut centres
# (masterplan parts/02b_detail.py CUT_AT = water board CUTS); K4, K5 = the bridges (site board BRIDGES_K)
P12_PLACES = [(u"UPSTREAM ENTRY", (29693.022, 32569.176)), (u"K4 · ULUCAMİ ÖNÜ", (29846.40, 32277.71)),
              (u"K5 · ÜÇ KEMER", (30293.63, 31792.25)), (u"DOWNSTREAM END", (30991.856, 31039.404))]
P12_ROT = -12.0                      # the axonometric: the plan turned 12 deg clockwise ...
P12_SIN, P12_COS = 0.62, 0.785       # ... and seen from 38 deg above (depth x sin, heights x cos; one scale)
P12_DET_DEN = 2000.0                 # the round zoom: the upstream entry in plan at 1:2,000
P12_DET_R = 46.0                     # its radius, mm (92 m on site)
P12_COL_W = 112.0                    # the column beside the map, mm
P12_ZONE = {"WS": MP["storage"], "WT": MP["wetland"], "WD": MP["discharge"], "GR": MP["park"],
            "WA": MP["amphibious"], "WP": ("ABBBAE", "748878", "3B4D3F"), "DG": MP["agriculture"]}
P12_STEP_COL = {1: MP["discharge"][1], 2: MP["wetland"][2], 3: MP["storage"][2], 4: MP["discharge"][2],
                5: MP["agriculture"][2]}


# ---------------------------------------------------------------- small geometry (page mm unless said)
def _p12_get(*path):
    """a value of the water balance results (WB) by its keys, None when it is not there"""
    d = WB
    for k in path:
        try:
            d = d[k]
        except (KeyError, IndexError, TypeError):
            return None
    return d


def _p12_area(R):
    return abs(sum(R[i][0] * R[(i + 1) % len(R)][1] - R[(i + 1) % len(R)][0] * R[i][1] for i in range(len(R)))) / 2.0


def _p12_cen(R):
    """the area centroid of a ring"""
    a = cx = cy = 0.0
    n = len(R)
    for i in range(n):
        (xa, ya), (xb, yb) = R[i], R[(i + 1) % n]
        f = xa * yb - xb * ya
        a += f
        cx += (xa + xb) * f
        cy += (ya + yb) * f
    if abs(a) < 1e-9:
        return (sum(p[0] for p in R) / n, sum(p[1] for p in R) / n)
    return (cx / (3.0 * a), cy / (3.0 * a))


def _p12_bbox(P):
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    return (min(xs), min(ys), max(xs), max(ys))


def _p12_lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def _p12_lr(a, b, p):
    """> 0 when p lies left of a -> b"""
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def _p12_clip_ring(R, C):
    """the ring R clipped to the convex counter-clockwise polygon C (Sutherland-Hodgman); [] when nothing is left"""
    out = list(R)
    for i in range(len(C)):
        a, b = C[i], C[(i + 1) % len(C)]
        inp, out = out, []
        if not inp:
            return []
        p = inp[-1]
        fp = _p12_lr(a, b, p)
        for q in inp:
            fq = _p12_lr(a, b, q)
            if fq >= 0.0:
                if fp < 0.0:
                    out.append(_p12_lerp(p, q, fp / (fp - fq)))
                out.append(q)
            elif fp >= 0.0:
                out.append(_p12_lerp(p, q, fp / (fp - fq)))
            p, fp = q, fq
    return out if len(out) >= 3 else []


def _p12_clip_line(P, C):
    """the pieces of the polyline P inside the convex counter-clockwise polygon C (Cyrus-Beck, segment by segment)"""
    pieces, cur = [], None
    for i in range(len(P) - 1):
        p, q = P[i], P[i + 1]
        t0, t1, ok = 0.0, 1.0, True
        for j in range(len(C)):
            a, b = C[j], C[(j + 1) % len(C)]
            fp, fq = _p12_lr(a, b, p), _p12_lr(a, b, q)
            if fp < 0.0 and fq < 0.0:
                ok = False
                break
            if fp < 0.0:
                t0 = max(t0, fp / (fp - fq))
            elif fq < 0.0:
                t1 = min(t1, fp / (fp - fq))
        if not ok or t0 > t1:
            cur = None
            continue
        a_, b_ = _p12_lerp(p, q, t0), _p12_lerp(p, q, t1)
        if cur is not None and t0 == 0.0:
            cur.append(b_)
        else:
            cur = [a_, b_]
            pieces.append(cur)
        if t1 < 1.0:
            cur = None
    return pieces


def _p12_clipper(C, inner):
    """a clip region: the convex polygon C (counter-clockwise) and a box surely inside it (no clipping needed there)"""
    return dict(C=C, bb=_p12_bbox(C), inner=inner)


def _p12_cring(R, K):
    b, o, i_ = _p12_bbox(R), K["bb"], K["inner"]
    if b[2] < o[0] or b[0] > o[2] or b[3] < o[1] or b[1] > o[3]:
        return []
    if i_[0] <= b[0] and b[2] <= i_[2] and i_[1] <= b[1] and b[3] <= i_[3]:
        return list(R)
    return _p12_clip_ring(R, K["C"])


def _p12_cline(P, K):
    b, o, i_ = _p12_bbox(P), K["bb"], K["inner"]
    if b[2] < o[0] or b[0] > o[2] or b[3] < o[1] or b[1] > o[3]:
        return []
    if i_[0] <= b[0] and b[2] <= i_[2] and i_[1] <= b[1] and b[3] <= i_[3]:
        return [list(P)]
    return _p12_clip_line(P, K["C"])


def _p12_hull(P):
    """convex hull, counter-clockwise (monotone chain)"""
    P = sorted(set(P))
    if len(P) < 3:
        return P

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in P:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(hi) >= 2 and cr(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def _p12_len(P):
    return sum(math.hypot(P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1]) for i in range(len(P) - 1))


def _p12_along(P, d):
    """the point and the unit direction at arc length d along the polyline P"""
    for i in range(len(P) - 1):
        L = math.hypot(P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1])
        if d <= L or i == len(P) - 2:
            if L < 1e-9:
                return P[i], (1.0, 0.0)
            t = max(0.0, min(1.0, d / L))
            return _p12_lerp(P[i], P[i + 1], t), ((P[i + 1][0] - P[i][0]) / L, (P[i + 1][1] - P[i][1]) / L)
        d -= L
    return P[-1], (1.0, 0.0)


def _p12_circle_pts(cx, cy, r, n=72):
    return [(cx + r * math.cos(2.0 * math.pi * i / n), cy + r * math.sin(2.0 * math.pi * i / n)) for i in range(n)]


def _p12_put(pg, shapes):
    """icons.py / plants.py shapes onto the page (the core's sec_put)"""
    sec_put(pg, shapes)


def _p12_step(pg, n, x, y, size=4.2):
    """the numbered step marker n (icons.py ico_step) centred on (x, y); returns its box"""
    sh, (ax, ay), th, cap = ico_step(x, y, size, "solid", P12_STEP_COL.get(n))
    _p12_put(pg, sh)
    pg.text(str(n), ax, ay - cap / 2.0, cap / CAP, th, bold=True, align="C")
    return (x - size / 2.0, y - size / 2.0, x + size / 2.0, y + size / 2.0)


def _p12_arrow(pg, a, b, col, lw=0.45, minlen=6.0, dash=None, head=1.8):
    """an arrow along a -> b (page), drawn at least minlen mm long about its middle (a project link is often a few
    metres: at the map's scale it is lengthened, never turned)"""
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    if L < 1e-6:
        return None
    if L < minlen:
        m, f = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0), minlen / L / 2.0
        a, b = (m[0] - (b[0] - a[0]) * f, m[1] - (b[1] - a[1]) * f), (m[0] + (b[0] - a[0]) * f, m[1] + (b[1] - a[1]) * f)
    arrow(pg, [a, b], col, lw, head, dash)
    return (a, b)


def _p12_bar(pg, x, y, den, marks=(0, 20, 50, 100)):
    """the scale bar of the plan zoom from (x, y): ink and white segments 1.2 mm high, marks in m over them; box"""
    k = 1000.0 / den
    for i in range(len(marks) - 1):
        pg.poly([rect(x + marks[i] * k, y, x + marks[i + 1] * k, y + 1.2)], fill=COL["ink"] if i % 2 == 0 else COL["white"],
                stroke=COL["ink"], lw=0.12)
    for i, v in enumerate(marks):
        pg.text(u"{}{}".format(v, u" m" if i == len(marks) - 1 else u""), x + v * k, y + 2.0, FS_MIN, COL["ink"], align="C")
    return (x - 2.0, y - 0.2, x + marks[-1] * k + 6.0, y + 2.0 + FS_MIN)


def _p12_north(pg, x, y, d, L=7.0):
    """a north arrow at (x, y) pointing along the unit page direction d; returns its box"""
    tip = (x + d[0] * L, y + d[1] * L)
    arrow(pg, [(x, y), tip], COL["ink"], 0.3, 2.0)
    pg.text(u"N", tip[0] + d[0] * 1.6, tip[1] + d[1] * 1.6 - FS_MIN * CAP / 2.0, FS_MIN, COL["ink"], bold=True, align="C")
    xs, ys = [x, tip[0] + d[0] * 3.5], [y, tip[1] + d[1] * 3.5]
    return (min(xs) - 2.5, min(ys) - 2.5, max(xs) + 2.5, max(ys) + 2.5)


# ---------------------------------------------------------------- the data: zones and links, figures
def _p12_zones(log):
    """the Option A zones and water links (survey m) from the water balance's results, key "zones" (v6)"""
    z = _p12_get("zones")
    if not z or not z.get("zones"):
        log.append(u"p.12: water_balance_results.json has no zones (run the water balance v6): the map shows the "
                   u"stream, the places and the flows only")
        return [], []
    log.append(u"p.12: zones from the water balance ({})".format(z.get("source", u"?")))
    zs = [dict(q, ring=[tuple(p) for p in q["ring"]]) for q in z["zones"] if len(q.get("ring") or []) >= 3]
    return zs, [dict(q, P=[tuple(p) for p in q["P"]]) for q in z.get("links") or [] if len(q.get("P") or []) >= 2]


def _p12_pick(zones, code, area=None, label=None):
    return [z for z in zones if z["code"] == code and (area is None or (z.get("study_area") or u"").startswith(area))
            and (label is None or label in (z.get("label") or u""))]


def _p12_figures(zones):
    """every figure the map prints, from the water balance results (None = left out)"""
    f = {}
    take, site = _p12_get("design", "river_take_m3_per_year"), _p12_get("site_catch_m3_per_year")
    f["collect"] = (take, site)
    wt = _p12_pick(zones, "WT")
    f["reed_m2"] = sum(z.get("m2") or _p12_area(z["ring"]) for z in wt) if wt else None
    f["store"] = WB_STORE if WB_LIVE else None          # v6.1: never the built-in default
    left = _p12_get("design", "river_left_pct")
    f["left"] = tuple(left) if left else None
    mix = _p12_get("design", "mix")
    f["farms"] = _p12_get("cutoff", mix, "central", "delivered_m3_per_year") if mix else None
    ha = [_p12_get("lands", "cropland_ha"), _p12_get("lands", "orchard_ha")]
    f["farm_ha"] = sum(ha) if None not in ha else None
    s2 = _p12_get("lands", "strip_m2")
    f["strip"] = (s2 / 4.0, s2 * STRIP_DEPTH, WB_STRIP) if s2 and WB_LIVE else None      # 400 cm wide (the strip's design)
    return f


# ---------------------------------------------------------------- labels on the map (G4: never on each other)
def _p12_wh(spec):
    ic = 7.0 if spec.get("icon") else 0.0
    ws = [text_w(spec["head"], 3.2, True)]
    if spec.get("big"):
        ws.append(text_w(spec["big"], 3.8, True))
    ws += [text_w(s, FS_MIN) for s in spec.get("small", ())]
    h = 3.2 * 1.3 + (3.8 * 1.25 if spec.get("big") else 0.0) + len(spec.get("small", ())) * FS_MIN * 1.3 + 0.4
    return ic + max(ws) + 0.8, max(h, ic)


def _p12_label(pg, b, spec):
    """a map label in its box b: the icon on the left, the step and verb, the figure, the keywords"""
    x = b[0]
    if spec.get("icon"):
        _p12_put(pg, ico_draw(spec["icon"], b[0] + 3.0, b[3] - 3.2, 6.0))
        x += 7.0
    col = spec.get("col") or COL["ink_dark"]
    y = b[3] - 3.2 * CAP - 0.4
    pg.text(spec["head"], x, y, 3.2, col, bold=True)
    if spec.get("big"):
        y -= 3.8 * 1.22
        pg.text(spec["big"], x, y, 3.8, COL["ink_dark"], bold=True)
    for s in spec.get("small", ()):
        y -= FS_MIN * 1.3
        pg.text(s, x, y, FS_MIN, COL["ink"])


def _p12_place(pg, specs, taken, bounds, segs, log):
    """places and draws the labels of specs (anchor x, y) beside their points, on a thin leader when off it"""
    rings = (1.5, 4.0, 7.0, 11.0, 16.0, 22.0, 30.0, 40.0, 52.0, 66.0)
    for sp in specs:
        w, h = _p12_wh(sp)
        got = label_spot(sp["x"], sp["y"], w, h, taken, bounds, segs, 0.8, rings, 24) or \
            label_spot(sp["x"], sp["y"], w, h, taken, bounds, (), 0.8, rings, 24)
        if not got:
            log.append(u"p.12: no room on the map for the label '{}'".format(sp["head"]))
            continue
        b = got[0]
        taken.append(b)
        e = lp_leader_end(b, (sp["x"], sp["y"]))
        d = math.hypot(e[0] - sp["x"], e[1] - sp["y"])
        if d > 1.2:
            r0 = sp.get("r0", 0.0)
            s0 = (sp["x"] + (e[0] - sp["x"]) * r0 / d, sp["y"] + (e[1] - sp["y"]) * r0 / d)
            pg.line([s0, e], COL["ink2"], 0.18)
            if not r0:
                pg.circle(sp["x"], sp["y"], 0.45, fill=COL["ink2"])
        _p12_label(pg, b, sp)


# ---------------------------------------------------------------- the axonometric map
def _p12_axo(pts, area, margins):
    """T(p, z=0) survey m -> page mm for the map, its inverse at z = 0, and k (page mm per m): the plan turned by
    P12_ROT and seen from above at the angle of P12_SIN / P12_COS, one scale, fitted into area less the margins
    (left, right, bottom, top)"""
    rho = math.radians(P12_ROT)
    c, s = math.cos(rho), math.sin(rho)
    cx, cy = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
    U = [((p[0] - cx) * c - (p[1] - cy) * s, ((p[0] - cx) * s + (p[1] - cy) * c) * P12_SIN) for p in pts]
    u0, u1 = min(u for u, w in U), max(u for u, w in U)
    w0, w1 = min(w for u, w in U), max(w for u, w in U)
    ml, mr, mb, mt = margins
    W, H = area[2] - area[0] - ml - mr, area[3] - area[1] - mb - mt
    k = min(W / max(u1 - u0, 1.0), H / max(w1 - w0, 1.0))
    ox = area[0] + ml + (W - (u1 - u0) * k) / 2.0 - u0 * k
    oy = area[1] + mb + (H - (w1 - w0) * k) / 2.0 - w0 * k

    def T(p, z=0.0):
        u = (p[0] - cx) * c - (p[1] - cy) * s
        v = (p[0] - cx) * s + (p[1] - cy) * c
        return (ox + u * k, oy + (v * P12_SIN + z * P12_COS) * k)

    def Ti(X, Y):
        u, v = (X - ox) / k, (Y - oy) / k / P12_SIN
        return (cx + u * c + v * s, cy - u * s + v * c)
    return T, Ti, k


def _p12_base(pg, items, T, K):
    """the shared basemap items through T, clipped to K"""
    def fill(rings, col, alpha, nonzero):
        rr = [r for r in (_p12_cring(R, K) for R in rings) if r]
        if rr:
            pg.poly(rr, fill=col, alpha=alpha if alpha is not None and alpha < 0.999 else None)

    def line(pts, col, w, dash, alpha):
        for piece in _p12_cline(pts, K):
            pg.line(piece, col, w, dash)
    return basemap_draw(items, T, fill, line)


def _p12_map(pg, ga, zones, links, f, log):
    """the axonometric water map in the area ga (page mm); returns what the labels and the zoom need"""
    key = list(P12_SELINOS) + [p for _, p in P12_PLACES]
    for z in zones:
        key += z["ring"]
    T, Ti, k = _p12_axo(key, ga, (12.0, 16.0, 16.0, 12.0))
    log.append(u"p.12: the water map at about 1:{:,.0f} (a diagram: no scale bar)".format(1000.0 / k))
    K = _p12_clipper([(ga[0], ga[1]), (ga[2], ga[1]), (ga[2], ga[3]), (ga[0], ga[3])], ga)
    # the shared basemap (02 §1): minimal mode (stream, main and lane streets, very faint buildings) with the fields on,
    # so the farms the water goes to read
    D = basemap_load(log=log)
    if D:
        cs = [Ti(ga[0], ga[1]), Ti(ga[2], ga[1]), Ti(ga[2], ga[3]), Ti(ga[0], ga[3])]
        sb = _p12_bbox(cs)
        _p12_base(pg, basemap_items("minimal", {"fields": True}, box=sb, D=D, split_buildings=True), T, K)
    # the zones of the project, flat on the ground
    for z in zones:
        if z["code"] == "STRIP":
            continue
        tones = P12_ZONE.get(z["code"], (COL["faint"], COL["structure"]))
        rr = _p12_cring([T(p) for p in z["ring"]], K)
        if rr:
            pg.poly([rr], fill=tones[0], stroke=tones[1], lw=0.15, alpha=0.9)
    for z in zones:                                      # the summer strip over everything: the line the page follows
        if z["code"] == "STRIP":
            rr = _p12_cring([T(p) for p in z["ring"]], K)
            if rr:
                pg.poly([rr], fill=MP["discharge"][1], stroke=MP["discharge"][2], lw=0.12)
    # the flow: the Selinos line dashed, a chevron every 22 mm pointing downstream
    S = [T(p) for p in P12_SELINOS]
    for piece in _p12_cline(S, K):
        pg.line(piece, MP["discharge"][2], 0.22, [1.0, 0.8])
    Ls = _p12_len(S)
    d = 30.0
    while d < Ls - 20.0:
        (px, py), (ux, uy) = _p12_along(S, d)
        pg.poly([[(px + ux * 1.4, py + uy * 1.4), (px - ux * 1.0 - uy * 1.1, py - uy * 1.0 + ux * 1.1),
                  (px - ux * 1.0 + uy * 1.1, py - uy * 1.0 - ux * 1.1)]], fill=MP["discharge"][2])
        d += 22.0
    segs = [(S[i], S[i + 1]) for i in range(len(S) - 1)]
    taken = []
    # the stream comes in (hand arrow on the first 16 mm) and leaves for the farms (beyond the last point)
    hand_arrow(pg, [_p12_along(S, t)[0] for t in (0.0, 4.0, 8.0, 12.0, 16.0)], "water", 0.8)
    (ex, ey), (ux, uy) = S[-1], _p12_along(S, Ls)[1]
    room = min([(ga[2] - 3.0 - ex) / ux if ux > 1e-6 else 99.0, (ey - ga[1] - 3.0) / -uy if uy < -1e-6 else 99.0,
                (ga[3] - 3.0 - ey) / uy if uy > 1e-6 else 99.0, (ex - ga[0] - 3.0) / -ux if ux < -1e-6 else 99.0])
    Lf = max(6.0, min(16.0, room - 5.0))              # room left for the step marker beyond the tip
    farm_tip = (ex + ux * Lf, ey + uy * Lf)
    hand_arrow(pg, [(ex - ux * 2.0, ey - uy * 2.0), farm_tip], "water", 0.8, (MP["agriculture"][1], MP["agriculture"][2]))
    segs.append(((ex, ey), farm_tip))
    # HOLD: the design store as a cube at the map's own scale, below the upstream entry's terraces and basins (dashed:
    # in the ground), an arrow down into it
    up = _p12_pick(zones, "WS", "aras") + _p12_pick(zones, "WT", "aras")
    hold = (sum(_p12_cen(z["ring"])[0] for z in up) / len(up), sum(_p12_cen(z["ring"])[1] for z in up) / len(up)) \
        if up else P12_PLACES[0][1]
    e = max(f["store"]) ** (1.0 / 3.0) if f["store"] else 0.0
    cube_b = None
    if e > 0.0:
        P = lambda i, j, l: T((hold[0] + (i - 0.5) * e, hold[1] + (j - 0.5) * e), -l * e)
        hull = _p12_hull([P(i, j, l) for i in (0, 1) for j in (0, 1) for l in (0, 1)])
        pg.poly([hull], fill=MP["storage"][0], alpha=0.55)
        for a_, b_ in (((0, 0, 0), (1, 0, 0)), ((1, 0, 0), (1, 1, 0)), ((1, 1, 0), (0, 1, 0)), ((0, 1, 0), (0, 0, 0)),
                       ((0, 0, 1), (1, 0, 1)), ((1, 0, 1), (1, 1, 1)), ((1, 1, 1), (0, 1, 1)), ((0, 1, 1), (0, 0, 1)),
                       ((0, 0, 0), (0, 0, 1)), ((1, 0, 0), (1, 0, 1)), ((1, 1, 0), (1, 1, 1)), ((0, 1, 0), (0, 1, 1))):
            pg.line([P(*a_), P(*b_)], MP["storage"][2], 0.22, [0.9, 0.6])
        cube_b = _p12_bbox(hull)
        arrow(pg, [T(hold), T(hold, -0.55 * e)], MP["storage"][2], 0.4, 1.5)
    # the links of the project (zone base INT_LINK_*): flood onto the terraces (dashed), clean water to the planting,
    # people down to the bed; the upstream entry's links are drawn at their true length in the round zoom
    for ln in links:
        a, b = T(ln["P"][0]), T(ln["P"][-1])
        if ln.get("kind") == "flood":
            r = _p12_arrow(pg, a, b, MP["amphibious"][2], 0.4, 6.0, [1.0, 0.6])
        elif ln.get("kind") == "people":
            r = _p12_arrow(pg, a, b, COL["accent"], 0.3, 4.5, [0.6, 0.5], 1.4)
        elif u"PLANTING" in (ln.get("label") or u""):
            r = _p12_arrow(pg, a, b, P12_ZONE["WP"][2], 0.4, 6.0)
        else:
            r = None
        if r:
            segs.append(r)
    # the round zoom's place on the map: the survey circle it shows, seen in the axonometric (an ellipse), dashed
    det = _p12_pick(zones, "WT", "aras") + _p12_pick(zones, "WS", "aras") + _p12_pick(zones, "WD", "aras") + \
        _p12_pick(zones, "GR", "aras")
    if det:
        bb = _p12_bbox([p for z in det for p in z["ring"]])
        dc = ((bb[0] + bb[2]) / 2.0, (bb[1] + bb[3]) / 2.0)
    else:
        dc = P12_PLACES[0][1]
    Rm = P12_DET_R * P12_DET_DEN / 1000.0
    ell = [T(p) for p in _p12_circle_pts(dc[0], dc[1], Rm, 48)]
    pg.line(ell + ell[:1], COL["ink"], 0.25, [0.8, 0.6])
    # the steps: a numbered marker where each happens
    wt, ws, wd = _p12_pick(zones, "WT", "aras"), _p12_pick(zones, "WS", "aras"), _p12_pick(zones, "WD", "aras")
    at = {1: T(_p12_cen(ws[0]["ring"])) if ws else T(P12_PLACES[0][1]),
          2: T(_p12_cen(wt[0]["ring"])) if wt else None,
          3: ((cube_b[0] + cube_b[2]) / 2.0, cube_b[1]) if cube_b else None,
          4: T(_p12_cen(wd[0]["ring"])) if wd else None,
          5: (farm_tip[0] + ux * 3.2, farm_tip[1] + uy * 3.2)}
    for n in (1, 2, 4, 5):
        if at[n]:
            taken.append(_p12_step(pg, n, at[n][0], at[n][1], 3.6))
    if cube_b:
        taken.append(cube_b)
    nd = (T((hold[0], hold[1] + 100.0))[0] - T(hold)[0], T((hold[0], hold[1] + 100.0))[1] - T(hold)[1])
    nl = math.hypot(*nd)
    return dict(T=T, k=k, S=S, segs=segs, taken=taken, at=at, dc=dc, ell=ell, hold=hold, e=e,
                nd=(nd[0] / nl, nd[1] / nl))


def _p12_map_labels(pg, ga, M, zones, f, log):
    """the verbs with their figures (R03, R04), the programme icons along the strip (R05) and the places"""
    T, at, taken, segs = M["T"], M["at"], M["taken"], M["segs"]
    specs = []
    take, site = f["collect"]
    if at[1]:
        sm = []
        if take is not None:
            sm.append(u"{:,.0f} m³ from the winter stream".format(take))
        if site is not None:
            sm.append(u"{:,.0f} m³ street + roof runoff".format(site))
        specs.append(dict(x=at[1][0], y=at[1][1], r0=1.8, icon="rain", head=u"1 COLLECT", col=P12_STEP_COL[1],
                          big=u"{:,.0f} m³ a year".format((take or 0) + (site or 0)) if sm else None, small=sm))
    if at[2]:
        specs.append(dict(x=at[2][0], y=at[2][1], r0=1.8, icon="reeds", head=u"2 CLEAN", col=P12_STEP_COL[2],
                          big=u"{:,.0f} m² of reed basins".format(f["reed_m2"]) if f["reed_m2"] else None,
                          small=[u"lined, root-contained · cleaned once,", u"then the whole reach runs clean"]))
    if at[3]:
        specs.append(dict(x=at[3][0], y=at[3][1], icon="storage", head=u"3 HOLD", col=P12_STEP_COL[3],
                          big=u"{:,.0f}-{:,.0f} m³".format(*f["store"]) if f["store"] else None,
                          small=[u"winter water held in the ground,", u"at most a year · cube at the map's scale"]))
    if at[4]:
        sm = [u"spillway: overflow back to the stream"]
        if f["left"]:
            sm.append(u"of its winter flow · driest year {:.0f} %".format(math.floor(f["left"][0])))
        specs.append(dict(x=at[4][0], y=at[4][1], r0=1.8, icon="stream", head=u"4 GIVE BACK", col=P12_STEP_COL[4],
                          big=u"{:.0f} % stays in the stream".format(math.floor(f["left"][1])) if f["left"] else None,
                          small=sm[::-1] if f["left"] else sm))
    sm = [u"the clean stream leaves the site"]
    if f["farm_ha"]:
        sm.append(u"for {:.1f} ha of farms outside it".format(f["farm_ha"]))
    specs.append(dict(x=at[5][0], y=at[5][1], r0=1.8, icon="stream_out", head=u"5 TO THE FARMS", col=P12_STEP_COL[5],
                      big=u"{:,.0f} m³ a year".format(f["farms"]) if f["farms"] else None, small=sm))
    # the summer strip, on its longest piece between K4 and K5
    st = sorted(_p12_pick(zones, "STRIP", "begum"), key=lambda z: -_p12_area(z["ring"]))
    if st and f["strip"]:
        c0 = _p12_cen(st[0]["ring"])
        p0 = min(st[0]["ring"], key=lambda p: (p[0] - c0[0]) ** 2 + (p[1] - c0[1]) ** 2)
        q = T(p0)
        specs.append(dict(x=q[0], y=q[1], icon="water", head=u"SUMMER STRIP", col=MP["discharge"][2],
                          big=u"400 × {:.0f} cm · {:,.0f} m".format(STRIP_DEPTH * 100.0, f["strip"][0]),
                          small=[u"first fill {:,.0f} m³ · {:,.0f} m³ a summer".format(f["strip"][1], f["strip"][2]),
                                 u"clean water in the bed all summer"]))
    fl = _p12_pick(zones, "WA", "begum_alan[1]", u"FLOOD") or _p12_pick(zones, "WA", "begum", u"FLOOD")
    if fl:
        q = T(_p12_cen(fl[0]["ring"]))
        specs.append(dict(x=q[0], y=q[1], icon="high_water", head=u"HIGH WATER", col=MP["amphibious"][2],
                          small=[u"spreads onto the flood terraces"]))
    # the programme along the strip (R05): what people do where, from the zones
    for code, area, lab, ic, words in (("GR", "begum_alan[0]", None, "people", [u"raised dry top · steps to the bed"]),
                                       ("GR", "begum_alan[1]", None, "people", [u"raised dry top · steps to the bed"]),
                                       ("DG", None, None, "olive", [u"olives, aromatics, beds"]),
                                       ("WP", None, None, "plants", [u"fed by the clean stream"]),
                                       ("GR", "aras", None, "shade", [u"along the basins"])):
        zz = _p12_pick(zones, code, area, lab)
        if not zz:
            continue
        cs = [_p12_cen(z["ring"]) for z in zz]
        q = T((sum(c[0] for c in cs) / len(cs), sum(c[1] for c in cs) / len(cs)))
        head = {"DG": u"DEMETER'S GARDEN", "WP": u"STREAMSIDE PLANTING"}.get(code, u"DRY TOP" if ic == "people"
                                                                            else u"SHADED WALK")
        specs.append(dict(x=q[0], y=q[1], icon=ic, head=head, col=COL["ink_dark"], small=words))
    _p12_place(pg, specs, taken, ga, segs, log)
    # the places, in small capitals, last (they may sit farther off)
    pl = [dict(x=T(p)[0], y=T(p)[1], head=nm, col=COL["ink2"]) for nm, p in P12_PLACES]
    _p12_place(pg, pl, taken, ga, segs, log)


# ---------------------------------------------------------------- the round zoom: the upstream entry in plan, 1:2,000
def _p12_detail(pg, ga, M, zones, links, log):
    """the upstream entry as a plan at 1:2,000 in a circle, in the empty corner of the map farthest from the stream;
    its links at true length, the zones named, the steps numbered as on the map; the scale bar and north arrow
    under it; the dashed lines to its ellipse on the map"""
    R, den = P12_DET_R, P12_DET_DEN
    kd = 1000.0 / den
    dc = M["dc"]
    pts = M["S"] + [M["at"][n] for n in M["at"] if M["at"][n]]
    cands = [(ga[2] - R - 2.0, ga[3] - R - 2.0), (ga[0] + R + 2.0, ga[1] + R + 16.0),
             (ga[2] - R - 2.0, (ga[1] + ga[3]) / 2.0 + 10.0)]
    ccx, ccy = max(cands, key=lambda c: min(math.hypot(p[0] - c[0], p[1] - c[1]) for p in pts))
    Td = lambda p: (ccx + (p[0] - dc[0]) * kd, ccy + (p[1] - dc[1]) * kd)
    C = _p12_circle_pts(ccx, ccy, R, 96)
    h = R * 0.70
    K = _p12_clipper(C, (ccx - h, ccy - h, ccx + h, ccy + h))
    # the dashed connectors from the map's ellipse to the circle (drawn first, under the white disc)
    ec = ((min(p[0] for p in M["ell"]) + max(p[0] for p in M["ell"])) / 2.0,
          (min(p[1] for p in M["ell"]) + max(p[1] for p in M["ell"])) / 2.0)
    dx, dy = ccx - ec[0], ccy - ec[1]
    dl = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / dl, dx / dl
    re = max(abs(nx * (p[0] - ec[0]) + ny * (p[1] - ec[1])) for p in M["ell"])
    for sg in (1, -1):
        pg.line([(ec[0] + nx * re * sg, ec[1] + ny * re * sg), (ccx + nx * R * sg, ccy + ny * R * sg)], COL["ink2"], 0.2,
                [0.8, 0.6])
    pg.poly([C], fill=COL["white"])
    D = basemap_load(log=log)
    if D:
        Rm = R / kd
        _p12_base(pg, basemap_items("simple", None, box=(dc[0] - Rm, dc[1] - Rm, dc[0] + Rm, dc[1] + Rm), D=D,
                                    split_buildings=True), Td, K)
    up = [z for z in zones if (z.get("study_area") or u"").startswith("aras")]
    for z in zones:
        Q = [Td(p) for p in z["ring"]]
        if z["code"] == "STRIP":
            continue
        inside = all(math.hypot(p[0] - ccx, p[1] - ccy) < R - 0.3 for p in Q)
        if z["code"] == "WT" and inside:              # D2 a: common reed only in lined, root-contained cells
            _p12_put(pg, pla_cell_plan("reed", Q, kd))
            continue
        tones = P12_ZONE.get(z["code"], (COL["faint"], COL["structure"]))
        rr = _p12_cring(Q, K)
        if rr:
            pg.poly([rr], fill=tones[0], stroke=tones[1], lw=0.2)
    for z in zones:
        if z["code"] == "STRIP":
            rr = _p12_cring([Td(p) for p in z["ring"]], K)
            if rr:
                pg.poly([rr], fill=MP["discharge"][1], stroke=MP["discharge"][2], lw=0.12)
    taken = []
    segs = []
    for ln in links:                                  # the links at their true length (1:2,000)
        a, b = Td(ln["P"][0]), Td(ln["P"][-1])
        if max(math.hypot(p[0] - ccx, p[1] - ccy) for p in (a, b)) > R - 3.0:
            continue
        col = {"flood": MP["amphibious"][2], "people": COL["accent"]}.get(ln.get("kind"), MP["discharge"][2])
        arrow(pg, [a, b], col, 0.5, 1.8, [0.8, 0.5] if ln.get("kind") == "people" else None)
        segs.append((a, b))
    # the steps where they happen: 1 the stream and the held runoff into the basins, 2 the basins, 4 back to the stream
    lk = dict((ln.get("label") or u"", ln) for ln in links)
    marks = []
    for n, lab, end in ((1, u"RIVER INTO THE CLEANSING BASINS", 0), (1, u"HELD RUNOFF INTO THE CLEANSING BASINS", 0),
                        (4, u"CLEAN WATER BACK TO THE RIVER", -1)):
        if lab in lk:
            p = Td(lk[lab]["P"][end])
            if math.hypot(p[0] - ccx, p[1] - ccy) < R - 3.0:
                marks.append((n, p))
    wt = [z for z in up if z["code"] == "WT"]
    if wt:
        marks.append((2, Td(_p12_cen(wt[0]["ring"]))))
    for n, p in marks:
        taken.append(_p12_step(pg, n, p[0], p[1], 3.2))
    # zone names, inside the circle
    names = {"WT": u"REED BASINS, LINED", "WS": u"RETENTION TERRACES", "WD": u"SPILLWAY", "GR": u"SHADED WALK"}
    specs = []
    for z in up:
        if z["code"] in names:
            c = Td(_p12_cen(z["ring"]))
            if math.hypot(c[0] - ccx, c[1] - ccy) < R - 4.0:
                specs.append(dict(x=c[0], y=c[1], head=u"", small=[names[z["code"]]]))
    for sp in specs:
        w = text_w(sp["small"][0], FS_MIN) + 0.6
        got = label_spot(sp["x"], sp["y"], w, FS_MIN * 1.25, taken, (ccx - h, ccy - h, ccx + h, ccy + h), segs, 0.5,
                         (1.0, 3.0, 6.0, 10.0, 15.0), 24)
        if not got:
            log.append(u"p.12: the zoom has no room for '{}'".format(sp["small"][0]))
            continue
        b = got[0]
        taken.append(b)
        if got[1]:
            e = lp_leader_end(b, (sp["x"], sp["y"]))
            pg.line([(sp["x"], sp["y"]), e], COL["ink2"], 0.15)
        pg.text(sp["small"][0], b[0] + 0.3, b[1] + FS_MIN * 0.3, FS_MIN, COL["ink_dark"], bold=True)
    pg.poly([C], stroke=COL["ink"], lw=0.35)
    # caption, scale bar and north arrow, flush under the circle (SCRIPT_STANDARD §8: a bar beside every plan)
    yb = ccy - R - 4.0
    pg.text(u"UPSTREAM ENTRY · plan 1:{:,.0f}".format(den), ccx - R, yb, 3.0, COL["ink_dark"], bold=True)
    bb = _p12_bar(pg, ccx - R, yb - 6.5, den)
    nb = _p12_north(pg, ccx + R - 4.0, yb - 6.5, (0.0, 1.0), 5.0)
    log.append(u"p.12: the round zoom (upstream entry) in plan at 1:{:,.0f}".format(den))
    return (ccx - R - 0.5, min(bb[1], nb[1]), ccx + R + 0.5, ccy + R + 0.5)


# ---------------------------------------------------------------- beside the map (G7): the logic, two charts, why
def _p12_head(pg, x, y, w, title, sub=None):
    """a block head of the column: a hairline, the title (the takeaway), one keyword line; returns the y under it"""
    pg.line([(x, y), (x + w, y)], COL["structure"], 0.3)
    size = 3.8
    while size > 3.0 and text_w(title, size, True) > w:
        size -= 0.1
    y -= 3.8 * CAP + 1.6
    pg.text(title, x, y, size, COL["ink_dark"], bold=True)
    if sub:
        y -= FS_MIN * 1.45
        pg.text(sub, x, y, FS_MIN, COL["ink2"])
    return y - 3.0


def _p12_logic(pg, x, y, w):
    """the system's logic: the five steps of the map, one row each (marker, icon, verb, how), joined by the flow"""
    y = _p12_head(pg, x, y, w, u"THE LOGIC, IN ONE DIRECTION", u"numbers as on the map")
    rh = 10.2
    for i, (n, ic, verb, how) in enumerate(CHAIN):
        cy = y - rh / 2.0 + 1.0
        if i:
            pg.line([(x + 2.4, cy + rh - 2.0), (x + 2.4, cy + 2.6)], P12_STEP_COL[n], 0.35)
            pg.poly([[(x + 2.4, cy + 2.2), (x + 1.5, cy + 3.6), (x + 3.3, cy + 3.6)]], fill=P12_STEP_COL[n])
        _p12_step(pg, n, x + 2.4, cy, 4.4)
        _p12_put(pg, ico_draw(ic, x + 10.0, cy, 7.0))
        pg.text(verb, x + 15.5, cy + 0.6, 3.4, P12_STEP_COL[n], bold=True)
        lines = wrap(how, FS_MIN, w - 15.5)[:2]
        for j, ln in enumerate(lines):
            pg.text(ln, x + 15.5, cy - 3.0 - j * FS_MIN * 1.25, FS_MIN, COL["ink"])
        y -= rh
    return y


def _p12_coliforms(pg, x, y, w):
    """G7: the coliform figures as a chart on one log axis (left after a wetland against the reuse limits), and
    the move they lead to (UV where people touch the water)"""
    y = _p12_head(pg, x, y, w, u"NOT CLEAN ENOUGH TO TOUCH WITHOUT UV",
                  u"coliform bacteria per 100 ml, log scale")
    lx = x + 44.0                                     # the zero column, then 1 .. 100,000
    a0, a1 = lx + 7.0, x + w - 6.0
    pos = lambda v: a0 + (a1 - a0) * math.log10(max(v, 1.0)) / 5.0
    rows = [(COLIFORM[0][0], COLIFORM[0][1], COLIFORM[0][2], MP["wetland"][1], COLIFORM[0][4])] + \
           [(lab, lo, hi, C["acc"], src) for lab, lo, hi, _, src in COLIFORM[1:]]
    top = y + 1.0
    for i, (lab, lo, hi, col, src) in enumerate(rows):
        yy = y - i * 5.2
        pg.text(lab, x, yy - 0.9, FS_MIN, COL["ink"])
        c = cite(src)
        if c:
            pg.text(c, x + text_w(lab, FS_MIN) + 0.8, yy - 0.9, FS_MIN, COL["ink2"])
        if hi <= 0:                                   # a zero limit: a dot in the zero column
            pg.circle(lx + 3.0, yy, 0.9, fill=col)
        elif lo == hi:                                # a limit: a tick
            pg.poly([rect(pos(lo) - 0.35, yy - 1.6, pos(lo) + 0.35, yy + 1.6)], fill=col)
            pg.text(u"{:,.0f}".format(lo), pos(lo) + 1.2, yy - 0.9, FS_MIN, col, bold=True)
        else:                                         # a range: a bar
            pg.poly([rect(pos(lo), yy - 1.5, pos(hi), yy + 1.5)], fill=col)
            pg.text(u"{:,.0f}-{:,.0f}".format(lo, hi), pos(lo) + 1.0, yy - 0.9, FS_MIN, COL["white"], bold=True)
    yb = y - (len(rows) - 1) * 5.2 - 3.6
    pg.line([(lx, yb), (a1, yb)], COL["ink2"], 0.2)
    for v, s in ((0, u"0"), (1, u"1"), (100, u"100"), (10000, u"10,000"), (100000, u"100,000")):
        xx = lx + 3.0 if v == 0 else pos(v)
        pg.line([(xx, yb), (xx, top)], COL["faint"], 0.15)
        pg.text(s, xx, yb - FS_MIN * 1.25, FS_MIN, COL["ink2"], align="C")
    pg.line([(lx + 6.0, yb + 0.9), (lx + 7.0, yb - 0.9)], COL["ink2"], 0.2)   # the break between 0 and 1
    y = yb - FS_MIN * 1.25 - 5.0
    _p12_put(pg, ico_draw("uv", x + 3.5, y + 0.4, 7.0))
    pg.text(u"UV where people touch the water", x + 9.0, y + 0.8, 3.4, COL["ink_dark"], bold=True)
    pg.text(u"class A reuse (parks, water people touch) allows 0", x + 9.0, y - 2.8, FS_MIN, COL["ink"])
    return y - 5.6


def _p12_plants(pg, x, y, w):
    """G7: what the planting removes, as bars on one 0-100 % axis (D2: the reed figure only as the pilot result;
    D6: loosestrife TN > 60 %, no P)"""
    y = _p12_head(pg, x, y, w, u"WHAT THE PLANTING TAKES OUT", u"share of the nutrient removed")
    bx0, bx1 = x + 44.0, x + w - 14.0
    for ic, name, what, bars, src in HOW_T:
        _p12_put(pg, ico_draw(ic, x + 3.0, y - 1.6 - 1.4 * (len(bars) - 1), 6.0))
        pg.text(name, x + 7.5, y - 0.9, FS_MIN, COL["ink_dark"], bold=True)
        c = cite(src) if src else u""
        pg.text(what + (u" " + c if c else u""), x + 7.5, y - 0.9 - FS_MIN * 1.25, FS_MIN, COL["ink2"])
        for j, (lab, v, s) in enumerate(bars):
            yy = y - j * 4.6
            pg.poly([rect(bx0, yy - 1.3, bx1, yy + 1.3)], fill=COL["paper"])
            pg.poly([rect(bx0, yy - 1.3, bx0 + (bx1 - bx0) * v / 100.0, yy + 1.3)], fill=MP["wetland"][1])
            if s.startswith(u">"):                    # an open end: at least this much
                xe = bx0 + (bx1 - bx0) * v / 100.0
                pg.poly([[(xe, yy - 1.3), (xe + 2.2, yy), (xe, yy + 1.3)]], fill=MP["wetland"][1])
            if lab:
                pg.text(lab, bx0 + 1.0, yy - 0.9, FS_MIN, COL["white"], bold=True)
            pg.text(s, bx1 + 1.2, yy - 0.9, FS_MIN, COL["ink_dark"], bold=True)
        y -= max(len(bars) * 4.6, FS_MIN * 2.6) + 2.4
    return y


def _p12_why(pg, x, y, w):
    """why we clean here: the two published facts as pictogram rows (icon, figure, keywords)"""
    y = _p12_head(pg, x, y, w, u"WHY THE STREAM NEEDS CLEANING")
    for ic, head, big, short, src in WHY_T:
        _p12_put(pg, ico_draw(ic, x + 3.5, y - 2.2, 7.0))
        pg.text(big, x + 9.5, y - 1.0, 3.8, COL["ink_dark"], bold=True)
        tx = x + 9.5 + text_w(big, 3.8, True) + 2.0
        pg.text(head, tx, y - 1.0, FS_MIN, COL["ink2"], bold=True)
        c = cite(src)
        pg.text(short + (u" " + c if c else u""), x + 9.5, y - 1.0 - FS_MIN * 1.4, FS_MIN, COL["ink"])
        y -= 9.4
    return y


def _p12_column(pg, cb):
    """the column beside the map (G7): the logic, the two charts, why; the conclusion at its foot. The blocks share
    the column's height (equal gaps), measured on a dry run first"""
    x, y0, x1, y1 = cb
    w = x1 - x
    blocks = (_p12_logic, _p12_coliforms, _p12_plants, _p12_why)
    dry = Page(1, 1)
    hs = []
    yy = y1
    for fn in blocks:
        yn = fn(dry, x, yy, w)
        hs.append(yy - yn)
        yy = yn
    end = r28_para(dry, x, 0.0, w, CONTEXT["system"], 3.2, COL["ink"], kcol=COL["ink_dark"])
    hc = -end + 1.0
    gap = max(3.0, min(14.0, (y1 - y0 - sum(hs) - hc) / float(len(blocks))))
    y = y1
    for fn in blocks:
        y = fn(pg, x, y, w) - gap
    pg.line([(x, y0 + hc + 1.5), (x + w, y0 + hc + 1.5)], COL["structure"], 0.3)
    r28_para(pg, x, y0 + hc, w, CONTEXT["system"], 3.2, COL["ink"], kcol=COL["ink_dark"])


# ---------------------------------------------------------------- the page
def p12_page(pg, box, opt, storage, log):
    """v5 (revision 29 Oct, T3b WO-T3b-2): the whole p.12 panel in box (page mm, y up): the axonometric water map with
    its round plan zoom on the left, the column beside it on the right. Returns [(crop id, bbox, scale den or None)]."""
    x0, y0, x1, y1 = box
    zones, links = _p12_zones(log)
    f = _p12_figures(zones)
    if not WB_LIVE:                                      # v6.1
        log.append("p.12: no water_balance_results.json: HOLD volume and strip figures left out (run the water balance first)")
    xs = x1 - P12_COL_W
    ga = (x0, y0, xs - 7.0, y1)
    n0 = len(pg.items)
    M = _p12_map(pg, ga, zones, links, f, log)
    M["taken"].append(_p12_detail(pg, ga, M, zones, links, log))
    for nx_, ny_ in ((ga[0] + 5.0, ga[1] + 4.0), (ga[2] - 6.0, ga[1] + 4.0), (ga[0] + 5.0, ga[3] - 12.0)):
        if not any(lp_hit((nx_ - 3.0, ny_ - 3.0, nx_ + 9.0, ny_ + 10.0), t) for t in M["taken"]):
            break                                     # the map's north arrow in a free corner
    M["taken"].append(_p12_north(pg, nx_, ny_, M["nd"]))
    _p12_map_labels(pg, ga, M, zones, f, log)
    _p12_column(pg, (xs, y0, x1, y1))
    return [("wb_system", items_bbox(pg.items[n0:]), None)]
# p.14-15 the S4 pair (v5, revision 29 Oct 2026, T3b WO-T3b-4, package D; split from code.py and
# parts/r28_occupancy.py on 29 Oct 2026, rebuilt). ONE S4 for both pages: the existing levels from the level module
# (D4 b: bed +42.48; bed width, bank tops, the two level shelves, Q100, Q500) with our proposal on them; planting by the
# rule (D6: purple loosestrife + soft rush, no iris; D2: no reed in the open bed), each plant from plants.py in that
# month's state; the p.20 planting bands with their days under water folded into p.15 (D9 a).
#   p.14 (p14_page): four rows, a season each: rain and water as a small graphic, the cut at 1:500 with its plants in
#        the season's state, a line a month of plant states under it, the type of space it becomes named on it, one
#        rectangular view from the same viewpoint in every season, the animals on record that season.
#   p.15 (p15_page): the north-east bank at 1:250 with widths, levels and planting bands (days under water), and the
#        year on one month axis (R31: a row of pictograms per user group, bars on one time axis; plants in leaf and
#        flower).
# build_board calls P14_TITLE, P15_TITLE, p14_page(pg, box, opt, log), p15_page(pg, box, opt, log).

P14_TITLE = u"S4 THROUGH THE SEASONS · the water level decides what the place becomes"
P15_TITLE = u"S4 NORTH-EAST BANK · the terraces stay, their use follows the months"

# ---------------------------------------------------------------- the cut: levels from the level module, our proposal
# m across S4 from the bed's low point (north-east +, as the level table's shelves), levels m a.s.l. The bed starts where
# the north-east shelf starts and is the table's width wide; where the table gives no bank angle a loose earth bank is
# drawn at P14_EARTH_RUN. The proposal: a lined summer strip in the bed, the north-east shelf as a gravel flood terrace
# with a floodable lower walk, seat steps up to a raised promenade over Q500, its earth fill down to today's bank top.
P14_EARTH_RUN = 2.0                  # loose earth bank, m run per m rise (drawing rule)
P14_STRIP = (-3.5, 0.5)              # the summer strip (400 cm wide, STRIP_DEPTH deep) beside the north-east bank
P14_LINER = 0.15                     # its concrete liner, m
P14_PROM = 47.60                     # the raised promenade, over Q500
P14_STEPS = (8, 0.80)                # seat steps from the flood terrace up to the promenade: number, tread m
P14_PROM_W = (7.0, 3.0)              # promenade and bike lane, m
P14_FILL_RUN = 3.0                   # the promenade's earth fill down to today's bank top, m run per m rise
P14_WALK = (21.0, 24.0)              # the floodable lower walk on the flood terrace, m across
P14_SLAB = 0.25                      # paving and step slabs, m
P14_GRAVEL = 0.50                    # gravel under the bed, m
P14_POCHE = 1.00                     # cut ground drawn under the strip floor, m
P14_RANGE = (-46.0, 52.0)            # p.14: the whole cut, street to street
P15_RANGE = (-5.0, 52.0)             # p.15: the north-east bank from the strip
P14_DEN, P15_DEN = 500.0, 250.0      # standard scales of the two cuts
P14_SHEET_M = 0.10                   # a mean depth over this covers the gravel bed as one sheet of water; under it the
#                                      bed lies open and only the lined strip holds water (DEPTH, flat reach)
P14_SEA_MONTH = {"winter": 1, "spring": 4, "summer": 7, "autumn": 10}   # the month each cut and view shows (1-12)
P14_PLANTS = [  # the planting on S4 (D6, D2), sizes inside plants.py's sourced ranges, trees at about ten years:
    # (species, m across, height m, crown m)
    ("plane", -38.5, 12.0, 12.0), ("ash", -35.0, 12.0, 8.4), ("tamarisk", -29.0, 5.0, 4.5),
    ("chaste", -26.8, 3.0, 2.5), ("loosestrife", -25.7, 1.5, 1.0), ("soft_rush", -24.4, 1.0, 0.6),
    ("soft_rush", -18.0, 1.0, 0.6), ("soft_rush", -11.5, 1.0, 0.6), ("soft_rush", -6.0, 1.0, 0.6),
    ("soft_rush", 1.5, 1.0, 0.6), ("loosestrife", 2.4, 1.5, 1.0), ("willow", 3.9, 10.0, 7.0),
    ("chaste", 10.5, 3.0, 2.5), ("tamarisk", 16.0, 5.0, 4.5), ("chaste", 26.2, 3.0, 2.5),
    ("plane", 37.0, 12.0, 12.0)]
P14_SPACES = {  # what the place becomes that season, named on the cut: (zone of _p14_geo, name)
    "winter": [("bed", u"FLOOD CHANNEL"), ("terrace", u"FLOOD TERRACE")],
    "spring": [("bed", u"SHALLOW STREAM"), ("terrace", u"WET MEADOW")],
    "summer": [("strip", u"WADING STRIP"), ("market", u"MARKET GROUND"), ("prom", u"SHADED TERRACE")],
    "autumn": [("gravel", u"OPEN GRAVEL BED"), ("steps", u"SUN STEPS")],
}
P14_SPACE_COL = {"bed": "1B535E", "strip": "1B535E", "gravel": "6B5B2E", "terrace": "6B5B2E", "market": "5E4B8B",
                 "steps": "6B5B2E", "prom": "2D564E"}
P14_PEOPLE = {  # who is there, doing what, at the spot it happens: (pose, m across, facing, height m, depth in the view m)
    "winter": [("watch", 34.0, -1, 1.75, 14.0), ("walk", 38.6, 1, 1.75, 16.0), ("bike", 42.0, -1, 1.75, 20.0),
               ("walk", -37.0, 1, 1.75, 28.0)],
    "spring": [("walk", 22.6, -1, 1.75, 6.0), ("touch", 0.8, -1, 1.15, 12.0), ("stand", 1.9, -1, 1.75, 12.5),
               ("walk", 38.0, 1, 1.75, 16.0)],
    "summer": [("wade", -1.4, 1, 1.75, 13.0), ("wade", -2.6, -1, 1.15, 15.0), ("sit", 29.0, -1, 1.75, 8.0),
               ("stand", 8.9, -1, 1.75, 10.0), ("walk", 14.6, 1, 1.75, 9.0), ("walk", 38.8, -1, 1.75, 17.0)],
    "autumn": [("walk", -9.0, 1, 1.75, 16.0), ("walk", -10.2, 1, 1.15, 16.5), ("sit", 30.8, -1, 1.75, 9.0),
               ("walk", -37.5, -1, 1.75, 28.0)],
}
P14_STALLS = {"summer": [(7.0, 11.0), (12.8, 11.0)]}   # Kermes stalls on the flood terrace: (m across, view depth m)
_P14_GEO = []


def _p14_lv(key, side=None):
    v = level("S4", key, side)
    if v is None:
        raise RuntimeError(u"S4: '{}' {} is missing in the level module (common/data/LEVELS.py)".format(key, side or u""))
    return v


def _p14_terrace(side):
    """(from m, to m, level) of S4's level shelf on side, from the level module"""
    for t in level_cut("S4").get("terraces") or []:
        if t.get("side") == side:
            lv = t.get("level")
            return float(t["from_m"]), float(t["to_m"]), round(float(lv["value"] if isinstance(lv, dict) else lv), 2)
    raise RuntimeError(u"S4: no {} shelf in the level module".format(side))


def _p14_geo():
    """The S4 cut, once a run: the levels (bed, q100, q500, ne_top, sw_top, shelf, sfl = strip floor, base), the profile
    "prof" [(s, z)] street to street, its segments "segs" [((s, z), (s, z), surface)], today's north-east bank "today",
    the zones {name: (s0, s1)}, the step rise."""
    if _P14_GEO:
        return _P14_GEO[0]
    bed, q100, q500 = _p14_lv("bed"), _p14_lv("q100"), _p14_lv("q500")
    width = _p14_lv("bed_width_cm") / 100.0
    ne_top, sw_top = _p14_lv("top", "NE"), _p14_lv("top", "SW")
    ne0, ne1, shelf = _p14_terrace("NE")
    sw0, sw1, sw_z = _p14_terrace("SW")
    b1 = ne0
    b0 = b1 - width
    st0, st1 = P14_STRIP
    sfl = bed - STRIP_DEPTH
    t0 = b1 + (shelf - bed) * P14_EARTH_RUN
    n, tread = P14_STEPS
    rise = (P14_PROM - shelf) / n
    p0 = ne1 + (n - 1) * tread
    p1 = p0 + P14_PROM_W[0]
    p2 = p1 + P14_PROM_W[1]
    p3 = p2 + (P14_PROM - ne_top) * P14_FILL_RUN
    pts, segs = [], []

    def add(s, z, tag=None):
        if pts and tag:
            segs.append((pts[-1], (s, z), tag))
        pts.append((s, z))
    add(P14_RANGE[0], sw_z)
    add(-sw1, sw_z, "road")
    add(-sw0 - 0.6, sw_z, "path")
    add(-sw0, sw_top, "crest")
    add(b0, bed, "slope_sw")
    add(st0, bed, "gravel")
    add(st0, sfl, "strip_side")
    add(st1, sfl, "strip")
    add(st1, bed, "strip_side")
    add(b1, bed, "gravel")
    add(t0, shelf, "slope_ne")
    add(P14_WALK[0], shelf, "terrace")
    add(P14_WALK[1], shelf, "walk")
    add(ne1, shelf, "terrace")
    for j in range(n):
        add(ne1 + j * tread, shelf + (j + 1) * rise, "riser")
        if j < n - 1:
            add(ne1 + (j + 1) * tread, shelf + (j + 1) * rise, "tread")
    add(p1, P14_PROM, "prom")
    add(p2, P14_PROM, "bike")
    add(p3, ne_top, "fill")
    add(P14_RANGE[1], ne_top, "street")
    ss = [p[0] for p in pts]
    if any(b < a - 1e-9 for a, b in zip(ss[:-1], ss[1:])):
        raise RuntimeError(u"S4: the levels give a cut that runs backwards ({}); check P14_* against levels.py".format(
            u", ".join(u"{:.2f}".format(s) for s in ss)))
    G = dict(bed=bed, q100=q100, q500=q500, ne_top=ne_top, sw_top=sw_top, shelf=shelf, sfl=sfl, rise=rise,
             width=width, base=sfl - P14_POCHE, prof=pts, segs=segs, b0=b0, b1=b1,
             dmax=max(_p14_depth(m) for m in range(12)),
             today=[(ne1, shelf), (ne1 + (ne_top - shelf) * P14_EARTH_RUN, ne_top), (P14_RANGE[1], ne_top)],
             zones=dict(bed=(b0, b1), gravel=(b0, st0), strip=(st0, st1), toe=(b1, t0), terrace=(t0, ne1),
                        market=(t0 + 2.0, P14_WALK[0] - 1.0), walk=P14_WALK, steps=(ne1, p0), prom=(p0, p1),
                        bike=(p1, p2), fill=(p2, p3), sw_slope=(-sw0, b0), sw_path=(-sw1, -sw0)))
    _P14_GEO.append(G)
    return G


def _p14_surf(s):
    """the ground of the cut at s (at a riser the upper one)"""
    pts = _p14_geo()["prof"]
    best = None
    for (a, za), (b, zb) in zip(pts[:-1], pts[1:]):
        if b > a and a - 1e-9 <= s <= b + 1e-9:
            z = za + (zb - za) * (s - a) / (b - a)
            best = z if best is None else max(best, z)
    if best is None:
        return pts[0][1] if s < pts[0][0] else pts[-1][1]
    return best


def _p14_wet(z, s0, s1, step=0.05):
    """the stretches from s0 to s1 whose ground lies under the level z: [(a, b)]"""
    out, a, s = [], None, s0
    n = int((s1 - s0) / step) + 1
    for i in range(n + 1):
        s = min(s1, s0 + i * step)
        if _p14_surf(s) < z - 1e-6:
            if a is None:
                a = s
        elif a is not None:
            out.append((a, s))
            a = None
    if a is not None:
        out.append((a, s1))
    return out


def _p14_depth(m):
    """the mean depth in the bed in month m (0 = Jan) on the flat reach (DEPTH): the higher of the two gauge routes"""
    return max(DEPTH["flat"][0][m], DEPTH["flat"][1][m])


def _p14_sea_depth(sea):
    ms = S4_MONTH_IDX[sea]
    return sum(_p14_depth(m) for m in ms) / float(len(ms))


def _p14_band_code(s, z):
    """the planting band (PLANT_BANDS code) of the ground at s, z by how often water reaches it: A the strip, B under
    the highest monthly mean water, C up to the flood terrace, D up to Q100, E up to Q500, F above"""
    G = _p14_geo()
    if G["zones"]["strip"][0] <= s <= G["zones"]["strip"][1]:
        return "A"
    if z <= G["bed"] + G["dmax"] + 1e-6:
        return "B"
    if z < G["shelf"] - 1e-6:
        return "C"
    if z <= G["q100"]:
        return "D"
    if z <= G["q500"]:
        return "E"
    return "F"


# ---------------------------------------------------------------- page helpers: clipping, shapes, plants, people
def _p14_clip_ring(ring, r):
    """ring clipped to the rectangle r = (x0, y0, x1, y1) (Sutherland-Hodgman), or None"""
    out = list(ring)
    for i in range(4):
        if len(out) < 3:
            return None

        def ins(p, i=i):
            return (p[0] >= r[0], p[1] >= r[1], p[0] <= r[2], p[1] <= r[3])[i]

        def cut(p, q, i=i):
            if i in (0, 2):
                t = (r[i] - p[0]) / (q[0] - p[0])
                return (r[i], p[1] + t * (q[1] - p[1]))
            t = (r[i] - p[1]) / (q[1] - p[1])
            return (p[0] + t * (q[0] - p[0]), r[i])
        inp, out = out, []
        prev = inp[-1]
        for cur in inp:
            if ins(cur):
                if not ins(prev):
                    out.append(cut(prev, cur))
                out.append(cur)
            elif ins(prev):
                out.append(cut(prev, cur))
            prev = cur
    return out if len(out) >= 3 else None


def _p14_clip_line(pts, r):
    """the runs of the polyline pts inside the rectangle r (Liang-Barsky)"""
    runs, cur = [], []
    for p, q in zip(pts[:-1], pts[1:]):
        t0, t1, ok = 0.0, 1.0, True
        dx, dy = q[0] - p[0], q[1] - p[1]
        for pp, qq in ((-dx, p[0] - r[0]), (dx, r[2] - p[0]), (-dy, p[1] - r[1]), (dy, r[3] - p[1])):
            if abs(pp) < 1e-12:
                if qq < 0:
                    ok = False
                    break
            elif pp < 0:
                t0 = max(t0, qq / pp)
            else:
                t1 = min(t1, qq / pp)
        if not ok or t0 > t1:
            if cur:
                runs.append(cur)
                cur = []
            continue
        a, b = (p[0] + t0 * dx, p[1] + t0 * dy), (p[0] + t1 * dx, p[1] + t1 * dy)
        if cur and abs(cur[-1][0] - a[0]) < 1e-9 and abs(cur[-1][1] - a[1]) < 1e-9:
            cur.append(b)
        else:
            if cur:
                runs.append(cur)
            cur = [a, b]
    if cur:
        runs.append(cur)
    return runs


def _p14_clip_items(items, r):
    """this board's page items cut to the rectangle r (a view or a key map stays inside its frame)"""
    out = []
    for it in items:
        if it[0] == "poly":
            rings = [c for c in (_p14_clip_ring(rg, r) for rg in it[1]) if c]
            if rings:
                out.append(("poly", rings) + tuple(it[2:]))
        elif it[0] == "line":
            for run in _p14_clip_line(it[1], r):
                out.append(("line", run) + tuple(it[2:]))
        elif it[0] == "circle":
            if r[0] <= it[1] <= r[2] and r[1] <= it[2] <= r[3]:
                out.append(it)
        elif it[0] == "text":
            if r[0] <= it[2] <= r[2] and r[1] <= it[3] <= r[3]:
                out.append(it)
    return out


def _p14_ell(cx, cy, rx, ry, rot=0.0, n=22):
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    out = []
    for i in range(n):
        t = 2.0 * math.pi * i / n
        u, v = rx * math.cos(t), ry * math.sin(t)
        out.append((cx + u * c - v * s, cy + u * s + v * c))
    return out


def _p14_band(pts, w):
    """a band w wide along the polyline pts, as one ring"""
    left, right = [], []
    for i, p in enumerate(pts):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L * w / 2.0, dx / L * w / 2.0
        left.append((p[0] + nx, p[1] + ny))
        right.append((p[0] - nx, p[1] - ny))
    return left + right[::-1]


def _p14_fig(pg, pose, x, y, k, colour, facing=1, height=1.75):
    """ONE place for the people of pp.14-15 while figures.py is paused: the legacy silhouettes (fig_polys through
    r28_fig), feet at (x, y), k mm per m; a seated figure is passed with its seat at y. Swap the new set in here."""
    if pose == "sit":
        y -= R28_SEAT * k
    return r28_fig(pg, pose, x, y, k, colour, facing, height)


def _p14_stall(pg, x, y, k, colour, roof=None):
    """a Kermes market stall, its base centred at (x, y), k mm per m: two posts, a counter, a pitched awning (filled
    with roof, else in thin lines). Returns its box."""
    a, b, h = x - 1.2 * k, x + 1.2 * k, 2.1 * k
    lw = max(0.08, 0.05 * k)
    awn = [(a - 0.25 * k, y + h), (x, y + h + 0.45 * k), (b + 0.25 * k, y + h)]
    for xx in (a, b):
        pg.line([(xx, y), (xx, y + h)], colour, lw)
    if roof:
        pg.poly([awn], fill=roof, stroke=colour, lw=lw)
        pg.poly([rect(a, y + 0.75 * k, b, y + 0.95 * k)], fill=roof, stroke=colour, lw=lw)
    else:
        pg.line(awn, colour, lw)
        pg.line([(a, y + 0.85 * k), (b, y + 0.85 * k)], colour, lw)
    return (a - 0.25 * k, y, b + 0.25 * k, y + h + 0.45 * k)


P14_BARE = "DCD6C8"                  # a bare crown
P14_BARE_EDGE = "B0AC9C"
P14_BLOOM = "C97FA0"                 # in flower: one colour for every species, as in the calendars
P14_LEAF = "9DB46F"                  # in leaf, on the key


def _p14_state(key, month):
    """a species in month (1-12), from plants.py's sourced months: "cut" (loosestrife heads), "bloom", "leaf", "bare",
    or None when no leaf months are sourced and it is not in flower"""
    m = pla_months(key)
    if month in m["cut"]:
        return "cut"
    if month in m["bloom"]:
        return "bloom"
    if m["leaf"]:
        return "leaf" if month in m["leaf"] else "bare"
    return None


def _p14_cell(pg, x0, y0, x1, y1, st, leaf=None):
    """one calendar cell of a plant state"""
    r = rect(x0, y0, x1, y1)
    if st == "leaf":
        pg.poly([r], fill=leaf or P14_LEAF)
    elif st == "bloom":
        pg.poly([r], fill=P14_BLOOM)
    elif st == "bare":
        pg.poly([r], fill=COL["white"], stroke=P14_BARE_EDGE, lw=0.1)
    elif st == "cut":
        pg.poly([r], fill=COL["white"], stroke=P14_BLOOM, lw=0.1, stripes=(P14_BLOOM, 0.55, 0.1, 45.0))


def _p14_plant(pg, key, x, gy, k, month, h=None, cw=None, seed=0):
    """a species in section at true size (plants.py) as it is that month (1-12): a bare crown see-through, flowers
    only in its flowering months, loosestrife without its heads once they are cut"""
    c = PLA_SPECIES[key]["colours"]
    st = _p14_state(key, month)
    fol = (c.get("fill"), c.get("lt"))
    acc = c.get("accent")
    for sh in pla_section(key, x, gy, k, h, cw, False, seed):
        if sh[0] == "poly":
            fill = sh[2]
            if st == "bare" and fill in fol:
                pg.poly([sh[1]], fill=P14_BARE, stroke=c.get("stem"), lw=0.06, alpha=0.6)
                continue
            if acc and fill == acc and st != "bloom":
                if st in ("cut", "bare"):
                    continue
                fill = c.get("fill")
            pg.poly([sh[1]], fill=fill, stroke=sh[3], lw=sh[4])
        elif not (acc and sh[2] == acc and st != "bloom"):
            pg.line(sh[1], sh[2], sh[3])


# ---------------------------------------------------------------- the animals on record (T1 ecology, GBIF)
# fauna.json (T1/ecology, H-ecology 29 Oct): species recorded near Bergama with the months that have records, from the
# GBIF occurrence search (eBird, iNaturalist, the Odonata atlas) in the town and basin boxes; reptiles under Squamata /
# Testudines. Fish: none on record in GBIF, so none are drawn. Order = the order shown; colours body, wing, light,
# bill, legs; h = size m.
P14_FAUNA = [
    dict(key="grey_heron", name=u"Grey heron", kind="heron", m=set(range(1, 13)), h=0.95,
         c=("9AA0A4", "5E676D", "F2F0EA", "D4A93C", "8A7D5A")),
    dict(key="white_stork", name=u"White stork", kind="stork", m={3, 4, 5, 6, 7, 8, 9}, h=1.0,
         c=("FFFFFF", "2C2219", "FFFFFF", "C8432F", "C8432F")),
    dict(key="kingfisher", name=u"Common kingfisher", kind="kingfisher", m={7, 8, 10, 11, 12}, h=0.17,
         c=("2A86B8", "1F5E86", "D9792B", "2C2219", "C8432F")),
    dict(key="barn_swallow", name=u"Barn swallow", kind="swallow", m={4, 5, 6, 7, 8, 9, 10}, h=0.2,
         c=("22304D", "22304D", "F1E7D8", "A33A2A", "22304D")),
    dict(key="little_egret", name=u"Little egret", kind="heron", m=set(range(1, 13)), h=0.6,
         c=("FFFFFF", "E9E6DE", "FFFFFF", "2C2219", "2C2219")),
    dict(key="black_stork", name=u"Black stork", kind="stork", m={1, 3, 4, 5, 6, 7, 9, 10, 11, 12}, h=1.0,
         c=("2F2A26", "2F2A26", "FFFFFF", "C8432F", "C8432F")),
    dict(key="white_wagtail", name=u"White wagtail", kind="songbird", m={1, 2, 3, 4, 5, 8, 10, 11, 12}, h=0.18,
         c=("8E9296", "2C2219", "FFFFFF", "2C2219", "2C2219")),
    dict(key="grey_wagtail", name=u"Grey wagtail", kind="songbird", m={8, 9, 10, 11}, h=0.18,
         c=("7D858C", "2C2219", "E8C94A", "2C2219", "C9B9A0")),
    dict(key="caspian_turtle", name=u"Western Caspian turtle", kind="turtle", m={2, 4, 5, 6, 8, 10}, h=0.2,
         c=("5B6236", "3A3F23", "D2C98E", "7E8450", "7E8450")),
    dict(key="marsh_frog", name=u"Marsh frog", kind="frog", m={2, 5, 7}, h=0.1,
         c=("7E9A4A", "4E6230", "DDD8A8", "2C2219", "4E6230")),
    dict(key="red_veined_darter", name=u"Red-veined darter", kind="dragonfly", m={8, 9}, h=0.07,
         c=("C2412D", "7A2418", "E8EEF0", "2C2219", "2C2219")),
    dict(key="banded_demoiselle", name=u"Banded demoiselle", kind="damselfly", m={8}, h=0.07,
         c=("2E6F8E", "1F3A4A", "C8D6DC", "1F3A4A", "1F3A4A")),
    dict(key="green_toad", name=u"European green toad", kind="toad", m={4, 8, 11}, h=0.1,
         c=("A7A47E", "5F7A45", "E4DFC8", "2C2219", "5F7A45")),
    dict(key="dice_snake", name=u"Dice snake", kind="snake", m={7}, h=0.08,
         c=("7D7A5C", "3F3C2C", "C9C3A0", "2C2219", "3F3C2C")),
    dict(key="tree_frog", name=u"Eastern tree frog", kind="frog", m={4}, h=0.05,
         c=("7DBA4A", "4F8A2E", "EAF0C8", "2C2219", "4F8A2E")),
]
P14_BIRDS = ("heron", "stork", "kingfisher", "swallow", "songbird")
P14_FAUNA_N = (7, 3)                 # animals shown a season at most, of them not birds at most
P14_FOOT = {"heron": 0.44, "stork": 0.46, "kingfisher": 0.27, "songbird": 0.2, "turtle": 0.1, "frog": 0.17,
            "toad": 0.17, "snake": 0.1}  # the pictogram's feet under its centre, x its size
P14_FAUNA_SRC = [u"Imani J et al. (2026). EOD – eBird Observation Dataset. Cornell Lab of Ornithology. "
                 u"https://doi.org/10.15468/aomfnb, accessed via GBIF.org 2026-10-29",
                 u"iNaturalist contributors (2026). iNaturalist Research-grade Observations. "
                 u"https://doi.org/10.15468/ab3s5x, accessed via GBIF.org 2026-10-29",
                 u"Boudot J, van Grunsven R (2021). Atlas of the dragonflies and damselflies of West and Central Asia. "
                 u"Version 1.4. https://doi.org/10.15468/gt3j2u, accessed via GBIF.org 2026-10-29"]


def _p14_fauna_for(sea):
    """the animals with records in the season's months: birds first, at most P14_FAUNA_N"""
    ms = set(m + 1 for m in S4_MONTH_IDX[sea])
    on = [f for f in P14_FAUNA if f["m"] & ms]
    rest = [f for f in on if f["kind"] not in P14_BIRDS][:P14_FAUNA_N[1]]
    return [f for f in on if f["kind"] in P14_BIRDS][:P14_FAUNA_N[0] - len(rest)] + rest


def _p14_fauna(pg, key, x, y, size, facing=1):
    """ONE place for the animal pictograms of pp.14-15 (figures.py, which will hold them, is paused): the P14_FAUNA
    animal key drawn in a size-mm square centred on (x, y), head to the left (facing -1: to the right), simple flat
    shapes in its own colours. Swap the new set in here."""
    fa = [f for f in P14_FAUNA if f["key"] == key][0]
    body, wing, light, bill, legs = fa["c"]
    kind = fa["kind"]
    lw = max(0.05, size / 70.0)
    white = body.upper() == "FFFFFF"
    dark = "2C2219"

    def T(u, v):
        return (x + u * size * facing, y + v * size)

    def P(pts, fill, edge=False, alpha=None):
        pg.poly([[T(u, v) for u, v in pts]], fill=fill, stroke=COL["ink2"] if edge else None, lw=lw, alpha=alpha)

    def E(cx, cy, rx, ry, rot, fill, edge=False, alpha=None):
        P(_p14_ell(cx, cy, rx, ry, rot), fill, edge, alpha)

    def B(pts, w, fill, edge=False):
        P(_p14_band(pts, w), fill, edge)

    def L(pts, colour, w):
        pg.line([T(u, v) for u, v in pts], colour, max(0.05, w * size))
    if kind == "heron":
        L([(0.04, -0.06), (0.02, -0.44)], legs, 0.022)
        L([(0.1, -0.06), (0.13, -0.44)], legs, 0.022)
        E(0.1, 0.0, 0.21, 0.1, -18, body, white)
        E(0.15, 0.02, 0.15, 0.065, -18, wing, white)
        P([(0.27, -0.05), (0.38, -0.13), (0.25, -0.1)], wing, white)
        B([(-0.06, 0.04), (-0.13, 0.14), (-0.08, 0.24), (-0.14, 0.33)], 0.05, light, True)
        E(-0.16, 0.36, 0.055, 0.04, 0, light, True)
        if not white:
            L([(-0.15, 0.38), (-0.03, 0.42)], dark, 0.015)
        P([(-0.2, 0.37), (-0.43, 0.34), (-0.2, 0.34)], bill)
    elif kind == "stork":
        L([(0.0, -0.06), (-0.02, -0.46)], legs, 0.024)
        L([(0.08, -0.06), (0.11, -0.46)], legs, 0.024)
        E(0.06, 0.02, 0.23, 0.11, -10, body, white)
        E(0.15, 0.0, 0.17, 0.075, -10, wing, white)
        if not white:
            E(0.0, -0.05, 0.12, 0.04, -10, light)
        B([(-0.1, 0.07), (-0.17, 0.27)], 0.07, body, white)
        E(-0.18, 0.3, 0.055, 0.045, 0, body, white)
        P([(-0.21, 0.32), (-0.46, 0.21), (-0.2, 0.28)], bill)
    elif kind == "kingfisher":
        L([(-0.4, -0.27), (0.42, -0.27)], "8B6B4A", 0.03)
        L([(0.0, -0.13), (0.0, -0.27)], legs, 0.02)
        B([(0.2, -0.05), (0.33, -0.22)], 0.06, wing)
        E(0.04, -0.04, 0.17, 0.12, 35, light)
        E(0.1, 0.02, 0.15, 0.09, 35, body)
        E(-0.1, 0.14, 0.1, 0.095, 0, body)
        E(-0.12, 0.1, 0.05, 0.035, 0, light)
        P([(-0.18, 0.17), (-0.46, 0.12), (-0.18, 0.11)], bill)
    elif kind == "swallow":
        P([(0.0, 0.03), (0.14, 0.36), (0.3, 0.4), (0.12, 0.0)], body)
        P([(0.0, -0.03), (0.12, -0.34), (0.27, -0.38), (0.12, 0.0)], wing)
        P([(0.18, 0.03), (0.47, 0.11), (0.26, 0.0), (0.47, -0.11), (0.18, -0.03)], body)
        E(0.0, 0.0, 0.21, 0.06, 0, body)
        E(0.02, -0.025, 0.13, 0.03, 0, light)
        E(-0.2, 0.0, 0.065, 0.055, 0, body)
        E(-0.23, -0.025, 0.035, 0.025, 0, bill)
    elif kind == "songbird":
        L([(0.0, -0.07), (-0.02, -0.2)], legs, 0.015)
        L([(0.05, -0.07), (0.05, -0.2)], legs, 0.015)
        B([(0.14, 0.0), (0.46, 0.09)], 0.05, wing)
        E(0.02, -0.01, 0.18, 0.09, 8, light, True)
        E(0.06, 0.03, 0.15, 0.065, 8, body)
        E(-0.15, 0.1, 0.075, 0.07, 0, body)
        E(-0.15, 0.04, 0.05, 0.04, 0, wing)
        P([(-0.21, 0.11), (-0.3, 0.1), (-0.21, 0.08)], bill)
    elif kind == "turtle":
        E(0.2, -0.08, 0.07, 0.04, 20, legs)
        E(-0.17, -0.08, 0.07, 0.04, -20, legs)
        B([(0.3, -0.03), (0.4, -0.08)], 0.04, legs)
        B([(-0.26, 0.0), (-0.36, 0.03)], 0.08, legs)
        E(-0.4, 0.03, 0.07, 0.05, 10, legs)
        L([(-0.45, 0.045), (-0.33, 0.02)], light, 0.012)
        P([(0.3 * math.cos(math.pi * i / 16.0), -0.04 + 0.24 * math.sin(math.pi * i / 16.0)) for i in range(17)],
          body, True)
        P(rect(-0.31, -0.08, 0.31, -0.04), light)
        for u_ in (-0.12, 0.0, 0.12):
            L([(u_, -0.04), (u_ * 1.2, 0.17 - abs(u_) * 0.5)], wing, 0.012)
        L([(-0.25, 0.08), (0.25, 0.08)], wing, 0.012)
    elif kind in ("frog", "toad"):
        E(0.12, -0.07, 0.17, 0.07, -8, wing)
        B([(0.04, -0.14), (0.34, -0.15)], 0.04, wing)
        E(0.0, 0.0, 0.26, 0.13, 12, body)
        E(-0.02, -0.06, 0.2, 0.05, 8, light)
        E(-0.2, 0.06, 0.1, 0.08, 0, body)
        B([(-0.12, -0.04), (-0.17, -0.16)], 0.04, body)
        spots = ((0.04, 0.07), (0.13, 0.03), (-0.05, 0.04))
        if kind == "toad":
            spots += ((0.0, 0.11), (0.17, 0.08), (-0.1, 0.1), (0.09, -0.01))
        for u_, v_ in spots:
            E(u_, v_, 0.025, 0.02, 0, wing)
        E(-0.2, 0.14, 0.045, 0.045, 0, light, True)
        E(-0.21, 0.14, 0.02, 0.02, 0, dark)
    elif kind == "dragonfly":
        for cy_, rot in ((0.17, 10), (-0.17, -10)):
            E(-0.2, cy_, 0.06, 0.2, rot, light, True, 0.8)
        for cy_, rot in ((0.18, -12), (-0.18, 12)):
            E(-0.08, cy_, 0.07, 0.21, rot, light, True, 0.8)
        B([(-0.12, 0.0), (0.46, 0.0)], 0.05, body)
        E(-0.2, 0.0, 0.08, 0.05, 0, wing)
        E(-0.32, 0.0, 0.05, 0.055, 0, body)
    elif kind == "damselfly":
        E(0.12, 0.07, 0.26, 0.045, 3, light, True, 0.8)
        E(0.16, 0.07, 0.1, 0.04, 3, wing, False, 0.85)
        B([(-0.1, 0.0), (0.48, 0.03)], 0.03, body)
        E(-0.17, 0.0, 0.07, 0.04, 0, body)
        E(-0.27, 0.01, 0.04, 0.04, 0, wing)
    else:                                                  # snake
        pts = [(-0.38, 0.02), (-0.25, 0.12), (-0.07, -0.04), (0.12, 0.1), (0.3, -0.04), (0.46, 0.0)]
        B(pts, 0.07, body)
        for u_, v_ in pts[1:-1]:
            E(u_, v_, 0.025, 0.02, 0, wing)
        E(-0.42, 0.02, 0.06, 0.04, 0, body)


def skyline(items, x0, x1, step=1.0):
    """Highest drawn point (page y) in every step-wide column from x0 to x1 (lines sampled along their length)."""
    n = int((x1 - x0) / step) + 2
    top = [-1e9] * n

    def put(x, y):
        i = int((x - x0) / step)
        if 0 <= i < n and y > top[i]:
            top[i] = y

    def seg(p, q):
        m = max(1, int(abs(q[0] - p[0]) / step) + 1)
        for j in range(m + 1):
            t = j / float(m)
            put(p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    for it in items:
        if it[0] == "poly":
            for r in it[1]:
                for i in range(len(r)):
                    seg(r[i], r[(i + 1) % len(r)])
        elif it[0] == "line":
            for i in range(len(it[1]) - 1):
                seg(it[1][i], it[1][i + 1])
        elif it[0] == "circle":
            put(it[1], it[2] + it[3])
    return lambda a, b: max(top[max(0, int((a - x0) / step)):max(1, int((b - x0) / step) + 1)] or [-1e9])


def sky_labels(pg, labs, items, x_lo, x_hi, y_cap, fs, boxes=None):
    """Short labels set in the open sky over a section, each as low as it fits above everything drawn under it and
    clear of the other labels, with a thin leader to its anchor. labs = [(ax, ay, [lines], colour, bold)]."""
    sky = skyline(items, x_lo - 60.0, x_hi + 60.0)
    boxes = boxes if boxes is not None else []
    lead = fs * 1.25
    for ax, ay, lines, colour, bold in sorted(labs, key=lambda t: t[0]):
        w = max(text_w(t, fs, bold) for t in lines) * BK_GROW + 0.8
        h = lead * len(lines) * BK_GROW
        best = None
        for x0 in (ax - 1.0, ax - w + 1.0, ax - w / 2.0):
            x0 = max(x_lo, min(x0, x_hi - w))
            y = max(sky(x0, x0 + w) + 1.2, ay + 1.5)
            while y + h < y_cap + 30.0:
                if not any(x0 < b[2] and b[0] < x0 + w and y < b[3] and b[1] < y + h for b in boxes):
                    break
                y += 0.5
            if best is None or y < best[1]:
                best = (x0, y)
        x0, y = best
        boxes.append((x0, y, x0 + w, y + h))
        for i, t in enumerate(lines):
            pg.text(t, x0 + 0.4, y + h - BK_GROW * lead * (i + 0.8), fs, colour, bold=bold)
        lx = min(max(ax, x0 + 0.6), x0 + w - 0.6)
        pg.line([(ax, ay), (lx, y - 0.3)], COL["ink2"], 0.1)
        pg.circle(ax, ay, 0.35, fill=COL["ink"])
    return boxes


def r28_mix(a, b, t):
    """hex colour a taken t of the way to b"""
    return u"".join(u"%02X" % int(round(int(a[i:i + 2], 16) * (1.0 - t) + int(b[i:i + 2], 16) * t)) for i in (0, 2, 4))


def occ_spans(ms):
    """the months ms (0 = Jan) as spans [(first, end)] along the year: Dec-Feb gives (0, 2) and (11, 12)"""
    out, m = [], 0
    while m < 12:
        if m in ms:
            n = m
            while n + 1 < 12 and (n + 1) in ms:
                n += 1
            out.append((m, n + 1))
            m = n + 1
        else:
            m += 1
    return out


# ---------------------------------------------------------------- the key map: S4 only, basemap "topographic"
P14_KEY = (130.0, 22.0)              # p.14: the key map's room (top right), mm; a key map states no scale, so it fills it


def _p14_keymap(pg, box, log=None):
    """the S4 key map at the top right of box (x0, y0, x1, y1): the analysis frame turned along its long side, upstream
    at the left, the shared basemap in its topographic mode (02 §1), ONLY the S4 cut with its look triangles and end
    names (D11), a north arrow at its left. Returns the box it took (the box's top edge when there is no basemap)."""
    x0, y0, x1, y1 = box
    fr = basemap_frame()
    if not fr:
        if log is not None:
            log.append(u"pp.14-15 key map: no basemap data (run the site board v51+ once); pages drawn without it")
        return (x1, y1, x1, y1)
    cx, cy = sum(p[0] for p in fr) / len(fr), sum(p[1] for p in fr) / len(fr)
    e1 = (fr[1][0] - fr[0][0], fr[1][1] - fr[0][1])
    e2 = (fr[2][0] - fr[1][0], fr[2][1] - fr[1][1])
    u = e1 if math.hypot(*e1) >= math.hypot(*e2) else e2
    L = math.hypot(*u)
    u = (u[0] / L, u[1] / L)
    if (fr[0][0] - cx) * u[0] + (fr[0][1] - cy) * u[1] > 0:      # the upstream end at the left
        u = (-u[0], -u[1])
    v = (-u[1], u[0])
    us = [(p[0] - cx) * u[0] + (p[1] - cy) * u[1] for p in fr]
    vs = [(p[0] - cx) * v[0] + (p[1] - cy) * v[1] for p in fr]
    na = 9.0                                                      # room for the north arrow
    den = max((max(us) - min(us)) * 1000.0 / (x1 - x0 - na), (max(vs) - min(vs)) * 1000.0 / (y1 - y0))
    k = 1000.0 / den
    ox, oy = x1 - max(us) * k, y1 - max(vs) * k

    def T(p):
        return (ox + ((p[0] - cx) * u[0] + (p[1] - cy) * u[1]) * k, oy + ((p[0] - cx) * v[0] + (p[1] - cy) * v[1]) * k)
    R = (ox + min(us) * k, oy + min(vs) * k, ox + max(us) * k, oy + max(vs) * k)
    sbox = (min(p[0] for p in fr), min(p[1] for p in fr), max(p[0] for p in fr), max(p[1] for p in fr))
    sp = Page(0, 0)

    def fade(hx, alpha):
        return hx if alpha is None or alpha >= 0.999 else r28_mix(hx, "FFFFFF", 1.0 - max(0.0, float(alpha)))

    def fill_fn(rings, hx, alpha, nonzero):
        sp.poly([r_ for r_ in rings if len(r_) >= 3], fill=fade(hx, alpha))

    def line_fn(pts, hx, w_mm, dash_mm, alpha):
        d_ = None
        if dash_mm:
            d_ = list(dash_mm) if isinstance(dash_mm, (list, tuple)) else [dash_mm, dash_mm]
        sp.line(pts, fade(hx, alpha), w_mm, dash=d_)

    def text_fn(s, xy, size_mm, hx, bold=False, align="L"):
        sp.text(s, xy[0], xy[1], max(size_mm, FS_MIN), hx, bold=bold, align=(str(align or u"L")[:1]).upper())
    try:
        items = basemap_items("topographic", box=sbox, split_buildings=True)
        cut = basemap_cut_items(basemap_cut_ids(["S4"]), den, text_mm=FS_MIN)
        pg.poly([rect(*R)], fill=COL["white"])
        basemap_draw(list(items) + list(cut), T, fill_fn, line_fn, text_fn)
    except Exception as ex:
        if log is not None:
            log.append(u"pp.14-15 key map not drawn: {}: {}".format(type(ex).__name__, ex))
        return (x1, y1, x1, y1)
    pg.items += _p14_clip_items(sp.items, R)
    pg.poly([rect(*R)], fill=None, stroke=COL["ink2"], lw=0.2)
    nx, ny = u[1], v[1]                                           # survey north in the page
    n_ = math.hypot(nx, ny) or 1.0
    nx, ny = nx / n_, ny / n_
    ax, ay = R[0] - na / 2.0, R[3] - 6.0
    px, py = -ny, nx
    tip, tail = (ax + nx * 3.0, ay + ny * 3.0), (ax - nx * 3.0, ay - ny * 3.0)
    pg.poly([[tip, (tail[0] + px * 1.4, tail[1] + py * 1.4), (ax - nx * 1.4, ay - ny * 1.4),
              (tail[0] - px * 1.4, tail[1] - py * 1.4)]], fill=COL["ink_dark"])
    pg.text(u"N", tip[0] + nx * 2.2, tip[1] + ny * 2.2 - FS_MIN * 0.35, FS_MIN, COL["ink_dark"], bold=True, align="C")
    return (R[0] - na, R[1], R[2], R[3])


# ---------------------------------------------------------------- the cut, drawn (pp.14 and 15)
P14_LOOK = {  # each season's colours in the views, and its water on the cuts
    "winter": dict(sky="DCE3E6", far="B3B8AA", grass="A3A98A", gravel="BBB4A2", water="86AEBC"),
    "spring": dict(sky="E3EDF0", far="B4C497", grass="98B46C", gravel="CEC6B3", water="96BCC8"),
    "summer": dict(sky="F3EFE2", far="CCC198", grass="CBBD84", gravel="DDD4BE", water="8CBBC8"),
    "autumn": dict(sky="ECE5D7", far="BFB18A", grass="B7A676", gravel="D5CCB6", water="90B5C1"),
}
P14_FIG = "4F453C"                   # the people in the views


def _p14_cut(pg, x0, yb, k, rng, sea, month, people=True):
    """the S4 cut from rng[0] to rng[1] (m across) at k mm per m, rng[0] at x0 and its base (G["base"]) at yb, as it is
    in sea: the cut ground (earth, the gravel bed, the concrete strip liner, walk, steps and promenade), the plants in
    month's state, the season's water (a sheet over the bed, else the strip full), Q100 / Q500 in winter, the season's
    people and the Kermes stalls. Returns (X, Y): m across -> page x, level -> page y."""
    G = _p14_geo()
    s0, s1 = rng
    zb = G["base"]

    def X(s):
        return x0 + (s - s0) * k

    def Y(z):
        return yb + (z - zb) * k
    clip = (X(s0), -1e9, X(s1), 1e9)

    def put(ring_m, mat):
        r_ = _p14_clip_ring([(X(s), Y(z)) for s, z in ring_m], clip)
        if r_:
            sec_put(pg, sct_hatch_fill(r_, mat, k, None, 0.1))
    bed, sfl, shelf, zn = G["bed"], G["sfl"], G["shelf"], G["zones"]
    st0, st1 = zn["strip"]
    lt = P14_LINER
    pts = [(s0, _p14_surf(s0))] + [p for p in G["prof"] if s0 < p[0] < s1] + [(s1, _p14_surf(s1))]
    put(pts + [(s1, zb), (s0, zb)], "earth")
    for a, b in ((G["b0"], st0 - lt), (st1 + lt, G["b1"])):
        put([(a, bed), (b, bed), (b, bed - P14_GRAVEL), (a, bed - P14_GRAVEL)], "gravel")
    t0, t1 = zn["terrace"]
    put([(t0, shelf), (t1, shelf), (t1, shelf - 0.3), (t0, shelf - 0.3)], "gravel")
    put([(st0 - lt, bed), (st0 - lt, sfl - lt), (st1 + lt, sfl - lt), (st1 + lt, bed), (st1, bed), (st1, sfl),
         (st0, sfl), (st0, bed)], "concrete")
    w0, w1 = P14_WALK
    put([(w0, shelf), (w1, shelf), (w1, shelf - 0.2), (w0, shelf - 0.2)], "concrete")
    e0, p0 = zn["steps"]
    put([p for p in G["prof"] if e0 - 1e-9 <= p[0] <= p0 + 1e-9 and p[1] >= shelf - 1e-9] +
        [(p0, P14_PROM - 0.35), (e0, shelf - 0.35)], "concrete")
    p2 = zn["bike"][1]
    put([(p0, P14_PROM), (p2, P14_PROM), (p2, P14_PROM - P14_SLAB), (p0, P14_PROM - P14_SLAB)], "concrete")
    pg.line([(X(s), Y(z)) for s, z in pts], COL["ink_dark"], 0.3)
    b0_, b1_ = max(zn["bike"][0], s0), min(zn["bike"][1], s1)
    if b1_ > b0_:
        pg.line([(X(b0_), Y(P14_PROM) + 0.25), (X(b1_), Y(P14_PROM) + 0.25)], "B98A74", 0.5)
    for i, (key, s, h, cw) in enumerate(P14_PLANTS):
        if s0 + 0.5 <= s <= s1 - 0.5:
            _p14_plant(pg, key, X(s), Y(_p14_surf(s)), k, month, h, cw, i)
    depth = _p14_sea_depth(sea)
    if depth >= P14_SHEET_M:
        zw = bed + depth
        wet = _p14_wet(zw, s0, s1)
    else:
        zw = bed
        wet = [(max(st0, s0), min(st1, s1))] if st1 > s0 and st0 < s1 else []
    for a, b in wet:
        ring = [(X(a), Y(zw))] + [(X(s), Y(z)) for s, z in G["prof"] if a < s < b] + [(X(b), Y(zw))]
        pg.poly([ring], fill=P14_LOOK[sea]["water"], alpha=0.85)
        pg.line([(X(a), Y(zw)), (X(b), Y(zw))], C["w3"], 0.2)
    if sea == "winter":
        for zq in (G["q100"], G["q500"]):
            for a, b in _p14_wet(zq, s0, s1):
                pg.line([(X(a), Y(zq)), (X(b), Y(zq))], C["w4"], 0.18, dash=[1.2, 0.7])
    if people:
        for pose, s, face, h, d in P14_PEOPLE.get(sea, []):
            if s0 + 1.0 <= s <= s1 - 1.0:
                _p14_fig(pg, pose, X(s), Y(_p14_surf(s)), k, COL["ink"], face, h)
        for s, d in P14_STALLS.get(sea, []):
            if s0 + 1.5 <= s <= s1 - 1.5:
                _p14_stall(pg, X(s), Y(_p14_surf(s)), k, P15_GROUP_COL["kermes"], "D9CFE6")
    return X, Y


def _p14_cal_band(pg, X, ytop, sea, rng):
    """under a season's cut: a line a month of the season (the first month on top), a cell under each plant in its
    state that month (plants.py's sourced months), the months named at the left"""
    ms = [m + 1 for m in S4_MONTH_IDX[sea]]
    hh = 1.15
    for i in range(len(ms) + 1):
        pg.line([(X(rng[0]), ytop - i * hh), (X(rng[1]), ytop - i * hh)], COL["faint"], 0.08)
    pg.text(S4_MONTHS[sea], X(rng[0]) + 0.4, ytop - hh * len(ms) / 2.0 - FS_MIN * 0.35, FS_MIN, COL["ink2"])
    for key, s, h, cw in P14_PLANTS:
        if rng[0] <= s <= rng[1]:
            for i, m in enumerate(ms):
                st = _p14_state(key, m)
                if st:
                    _p14_cell(pg, X(s) - 0.75, ytop - (i + 1) * hh + 0.12, X(s) + 0.75, ytop - i * hh - 0.12, st,
                              PLA_SPECIES[key]["colours"].get("fill"))


# ---------------------------------------------------------------- the view: the same spot in every season (p.14)
P14_EYE = (22.5, 1.60)               # the viewpoint of every view: on the lower walk (m across S4), eye height m
P14_VIEW = (0.26, 0.62, 0.55)        # focal length x the view's width; the vanishing point's x, y as shares of the view
P14_SURF = {"road": "B4AFA2", "street": "B4AFA2", "path": "CEC7B5", "crest": "A7A08F", "strip_side": "B8B2A4",
            "walk": "D9D4C7", "riser": "A9A394", "tread": "DCD7CA", "prom": "E4DFD2", "bike": "B98A74"}


def _p14_surf_col(tag, look):
    if tag in P14_SURF:
        return P14_SURF[tag]
    if tag in ("slope_sw", "slope_ne", "fill"):
        return look["grass"]
    if tag == "terrace":
        return r28_mix(look["gravel"], look["grass"], 0.45)
    if tag == "strip":
        return r28_mix(look["gravel"], "6F6A5E", 0.25)
    return look["gravel"]


def _p14_view(pg, box, sea):
    """one rectangular view, the same in every season: a one-point perspective up the Selinos stream from the lower
    walk (P14_EYE), the S4 cut carried along the stream, the water at the season's level, the plants as they are that
    month, the season's people and up to three of its animals. Faces turned away are left out, the rest is laid far to
    near; everything is cut to the rectangle."""
    x0, y0, x1, y1 = box
    G = _p14_geo()
    month = P14_SEA_MONTH[sea]
    look = P14_LOOK[sea]
    W, H = x1 - x0, y1 - y0
    f = P14_VIEW[0] * W
    vx, vy = x0 + P14_VIEW[1] * W, y0 + P14_VIEW[2] * H
    sc = P14_EYE[0]
    zc = _p14_surf(sc) + P14_EYE[1]

    def pr(s, z, d):
        return (vx + f * (s - sc) / d, vy + f * (z - zc) / d)
    sp = Page(0, 0)
    sp.poly([rect(x0, vy, x1, y1)], fill=look["sky"])
    sp.poly([rect(x0, y0, x1, vy)], fill=look["far"])
    dn, df = 0.6, 4000.0
    pts = G["prof"]
    segs = ([((pts[0][0] - 800.0, pts[0][1]), pts[0], "road")] + list(G["segs"]) +
            [(pts[-1], (pts[-1][0] + 800.0, pts[-1][1]), "street")])
    draws = []
    for a, b, tag in segs:
        if -(b[1] - a[1]) * (sc - a[0]) + (b[0] - a[0]) * (zc - a[1]) <= 1e-9:
            continue                                              # turned away from the eye
        key = 0.0 if a[0] <= sc <= b[0] else min(abs(a[0] - sc), abs(b[0] - sc))
        draws.append((key, a, b, tag))
    depth = _p14_sea_depth(sea)
    if depth >= P14_SHEET_M:
        zw = G["bed"] + depth
        wet = _p14_wet(zw, G["b0"] - 2.0, G["b1"] + 6.0)
    else:
        zw = G["bed"]
        wet = [G["zones"]["strip"]]
    for a, b in wet:
        key = 0.0 if a <= sc <= b else min(abs(a - sc), abs(b - sc))
        draws.append((key - 1e-3, (a, zw), (b, zw), "water"))
    draws.sort(key=lambda t: -t[0])
    edge = r28_mix(look["far"], COL["ink_dark"], 0.35)
    for key, a, b, tag in draws:
        colr = look["water"] if tag == "water" else _p14_surf_col(tag, look)
        sp.poly([[pr(a[0], a[1], dn), pr(b[0], b[1], dn), pr(b[0], b[1], df), pr(a[0], a[1], df)]], fill=colr,
                stroke=colr, lw=0.05)
        if tag == "water":
            for i, d in enumerate((5.0, 7.5, 11.0, 16.0, 23.0, 33.0, 48.0)):
                m_ = a[0] + (b[0] - a[0]) * (0.25 + 0.5 * ((i * 0.37) % 1.0))
                hw = (b[0] - a[0]) * 0.1
                sp.line([pr(m_ - hw, zw, d), pr(m_ + hw, zw, d)], COL["white"], 0.12)
        elif tag in ("tread", "riser", "walk", "prom", "crest", "strip_side", "bike"):
            for p_ in (a, b):
                sp.line([pr(p_[0], p_[1], dn), pr(p_[0], p_[1], 400.0)], edge, 0.07)
            if tag == "prom":
                for d in range(3, 90, 3):
                    sp.line([pr(a[0], a[1], float(d)), pr(b[0], b[1], float(d))], edge, 0.04)
    spr = []
    for i, (key, s, h, cw) in enumerate(P14_PLANTS):
        tall = h >= 6.0
        step = 13.0 if tall else (7.0 if h >= 2.0 else 3.5)
        dvis = (sc - s) * P14_VIEW[0] / P14_VIEW[1] if s < sc else (s - sc) * P14_VIEW[0] / (1.0 - P14_VIEW[1])
        d = max(dvis * 0.9, 9.0 if tall else 2.5) + (i % 3) * step / 3.0
        j = 0
        while d < (110.0 if tall else (60.0 if h >= 2.0 else 35.0)):
            spr.append((d, "plant", (key, s + ((j * 7 + i) % 5 - 2) * 0.15, h, cw, i * 31 + j)))
            d += step
            j += 1
    for pose, s, face, h, d in P14_PEOPLE.get(sea, []):
        spr.append((d, "fig", (pose, s, face, h)))
    for s, d in P14_STALLS.get(sea, []):
        spr.append((d, "stall", s))
    fa = _p14_fauna_for(sea)                                      # a wading bird, a flying or perched one, one more
    wad = [a for a in fa if a["kind"] in ("heron", "stork")]
    fly = [a for a in fa if a["kind"] in ("swallow", "kingfisher", "songbird")]
    oth = [a for a in fa if a["kind"] not in P14_BIRDS]
    if wad:
        spr.append((17.0, "animal", (wad[0], -8.0, None)))
    if fly:
        spr.append((10.0, "animal", (fly[0], 12.0, zc + 2.2) if fly[0]["kind"] == "swallow" else (fly[0], 0.9, None)))
    if oth:
        at = {"turtle": (0.7, None, 11.0), "frog": (1.2, None, 10.0), "toad": (3.0, None, 9.0),
              "snake": (2.0, None, 10.0), "dragonfly": (-1.5, G["bed"] + 0.8, 9.0),
              "damselfly": (-0.8, G["bed"] + 0.6, 9.0)}.get(oth[0]["kind"], (1.2, None, 10.0))
        spr.append((at[2], "animal", (oth[0], at[0], at[1])))
    spr.sort(key=lambda t: -t[0])
    for d, kind, data in spr:
        k = f / d
        if kind == "plant":
            key, s, h, cw, seed = data
            x, y = pr(s, _p14_surf(s), d)
            _p14_plant(sp, key, x, y, k, month, h, cw, seed)
        elif kind == "fig":
            pose, s, face, h = data
            x, y = pr(s, _p14_surf(s), d)
            _p14_fig(sp, pose, x, y, k, P14_FIG, face, h)
        elif kind == "stall":
            x, y = pr(data, _p14_surf(data), d)
            _p14_stall(sp, x, y, k, P15_GROUP_COL["kermes"], "D9CFE6")
        else:
            a_, s, z = data
            sz = max(a_["h"] * k * 1.3, 3.2)
            if z is None:
                x, y = pr(s, _p14_surf(s), d)
                y += P14_FOOT.get(a_["kind"], 0.0) * sz
            else:
                x, y = pr(s, z, d)
            _p14_fauna(sp, a_["key"], x, y, sz, 1)
    pg.items += _p14_clip_items(sp.items, box)
    pg.poly([rect(x0, y0, x1, y1)], fill=None, stroke=COL["ink2"], lw=0.2)


# ---------------------------------------------------------------- p.14
P14_COLS = (36.0, 21.0, 46.0, 3.0)   # the season column, the level ladder, the animals column, the gap, mm
P14_RAIN_MAX = 110.0                 # rain, mm a month, at the top of the small bars
P14_DEPTH_MAX = 0.25                 # water, m, that fills the small channel


def _p14_season_tag(pg, x, ytop, w, h, sea):
    """the season's name and months, then a month each: its rain (MGM normals, RAIN) as a bar and the mean water depth
    in the bed (DEPTH) in a small channel, the values on them"""
    fs = FS_MIN
    w -= 2.0
    pg.poly([rect(x, ytop - 0.9, x + w, ytop)], fill=BAND_BLUE[SEAS.index(sea)])
    pg.text(sea.upper(), x, ytop - 5.6, 4.2, COL["ink_dark"], bold=True)
    pg.text(S4_MONTHS[sea], x, ytop - 5.6 - fs * 1.4, fs, COL["ink2"], bold=True)
    cw = w / 3.0
    rh = max(5.0, min(12.0, h - 30.0))
    yr = ytop - 5.6 - fs * 1.4 - 1.6 - fs - 0.6 - rh
    pg.line([(x, yr), (x + w, yr)], COL["ink2"], 0.1)
    for i, m in enumerate(S4_MONTH_IDX[sea]):
        cx = x + (i + 0.5) * cw
        bh = rh * min(1.0, RAIN[m] / P14_RAIN_MAX)
        pg.poly([rect(cx - cw * 0.22, yr, cx + cw * 0.22, yr + bh)], fill=C["w3"])
        pg.text(u"{:.0f}".format(RAIN[m]), cx, yr + bh + 0.6, fs, C["w4"], align="C")
        pg.text(MONTHS[m], cx, yr - fs * 1.1, fs, COL["ink2"], align="C")
        gh, gw = 3.6, cw * 0.36
        yc = yr - fs * 1.1 - 1.4
        t = min(1.0, _p14_depth(m) / P14_DEPTH_MAX)
        ww = gw * 0.55 + gw * 0.45 * t
        pg.poly([[(cx - gw * 0.55, yc - gh), (cx + gw * 0.55, yc - gh), (cx + ww, yc - gh + gh * t),
                  (cx - ww, yc - gh + gh * t)]], fill=C["w2"])
        pg.line([(cx - gw, yc), (cx - gw * 0.55, yc - gh), (cx + gw * 0.55, yc - gh), (cx + gw, yc)], COL["ink"], 0.2)
        pg.text(u"{:.2f}".format(_p14_depth(m)), cx, yc - gh - fs * 1.05, fs, C["w4"], align="C")


def _p14_animals(pg, x, ytop, w, h, sea):
    """the animals on record that season: pictogram and name, one under the other"""
    sel = _p14_fauna_for(sea)
    if not sel:
        return
    pitch = min(6.6, h / float(len(sel)))
    sz = min(6.0, pitch - 0.5)
    for i, fa in enumerate(sel):
        cy = ytop - pitch * (i + 0.5)
        _p14_fauna(pg, fa["key"], x + sz / 2.0, cy, sz)
        pg.text(fa["name"], x + sz + 1.5, cy - FS_MIN * 0.35, FS_MIN, COL["ink_dark"])


def _p14_state_key(pg, x, y):
    """the plant states as drawn samples, one line from the top y; returns its bottom y"""
    fs = FS_MIN
    yy = y - fs * 1.1
    t = u"plants, under each cut a line a month:"
    pg.text(t, x, yy, fs, COL["ink2"])
    xx = x + text_w(t, fs) + 2.0
    for st, word in (("leaf", u"in leaf"), ("bloom", u"in flower"), ("bare", u"bare"), ("cut", u"heads cut")):
        _p14_cell(pg, xx, yy - 0.2, xx + 3.2, yy + fs * 0.75, st)
        pg.text(word, xx + 4.2, yy, fs, COL["ink"])
        xx += 4.2 + text_w(word, fs) + 3.5
    return yy - fs * 0.5


def _p14_plant_key(pg, x, ytop, w, h):
    """the species on the cuts, a small silhouette (May) and the name each, in one row w wide from x; returns the
    bottom y"""
    cw = w / float(len(P15_PLANT_ROWS))
    for i, key in enumerate(P15_PLANT_ROWS):
        hh, cr = [(h_, c_) for k_, s_, h_, c_ in P14_PLANTS if k_ == key][0]
        kk = (h - 1.0) / max(hh, cr)
        xx = x + i * cw
        _p14_plant(pg, key, xx + cr * kk / 2.0 + 0.3, ytop - h + 0.5, kk, 5, hh, cr)
        pg.text(PLA_SPECIES[key]["name"], xx + cr * kk + 1.6, ytop - h / 2.0 - FS_MIN * 0.35, FS_MIN, COL["ink"])
    return ytop - h


def p14_page(pg, box, opt, log):
    """p.14, the four seasons of S4 (package D), drawn whole into box (x0, y0, x1, y1), page mm: the context line and
    the plant-state key, the S4 key map at the top right, the column heads, then a row a season (rain and water, the
    cut at 1:500 with its levels at the right, the view, the animals), the scale bar flush with the cuts' column.
    Returns its crops [(crop id, bbox, scale denominator)]."""
    x0, y0, x1, y1 = box
    n0 = len(pg.items)
    fs = FS_MIN
    G = _p14_geo()
    k = 1000.0 / P14_DEN
    wa, wl, wd, gap = P14_COLS
    kb = _p14_keymap(pg, (x1 - P14_KEY[0], y1 - P14_KEY[1], x1, y1), log)
    cb = context(pg, x0, y1, kb[0] - x0 - 8.0, "seasons")
    yk = _p14_state_key(pg, x0, cb[1] - 1.0)
    yk = _p14_plant_key(pg, x0, yk - 1.0, kb[0] - x0 - 8.0, 9.0)
    yh = min(kb[1], yk) - 2.5
    wb = (P14_RANGE[1] - P14_RANGE[0]) * k
    xa, xb = x0, x0 + wa + gap
    xl = xb + wb + 0.5
    xv = xl + wl + gap
    xd = x1 - wd
    wv = xd - gap - xv
    if wv < 50.0 and log is not None:
        log.append(u"WARNING: p.14 views only {:.0f} mm wide (panel {:.0f} mm)".format(wv, x1 - x0))
    heads = [(xa, u"RAIN · WATER", u"mm a month " + cite(YEAR_SRC[0][1]) + u" · m deep"),
             (xb, u"THE CUT S4–S4', SOUTH-WEST TO NORTH-EAST · 1:500",
              u"what the place becomes · its plants, a line a month under it"),
             (xv, u"VIEW UPSTREAM FROM THE LOWER WALK", u"the same spot in every season"),
             (xd, u"ANIMALS ON RECORD", u"GBIF " + u"".join(cite(s_) for s_ in P14_FAUNA_SRC))]
    for hx, t1, t2 in heads:
        pg.text(t1, hx, yh - fs, fs, COL["ink_dark"], bold=True)
        pg.text(t2, hx, yh - fs * 2.3, fs, COL["ink2"])
    yt = yh - fs * 2.3 - 2.0
    rh = (yt - y0 - (fs * 1.3 + 2.4 + fs * CAP) - 1.5) / 4.0
    for i, sea in enumerate(SEAS):
        rt = yt - i * rh
        rbot = rt - rh
        pg.line([(x0, rt), (x1, rt)], COL["faint"], 0.25)
        _p14_season_tag(pg, xa, rt - 1.0, wa, rh - 2.0, sea)
        yb = rbot + 5.0
        sp = Page(0, 0)
        X, Y = _p14_cut(sp, xb, yb, k, P14_RANGE, sea, P14_SEA_MONTH[sea])
        pg.items += sp.items
        _p14_cal_band(pg, X, yb - 0.8, sea, P14_RANGE)
        d = _p14_sea_depth(sea)
        lv = [(Y(G["bed"]), u"{:+.2f} bed".format(G["bed"]), COL["ink"], False)]
        if d >= P14_SHEET_M:
            lv.append((Y(G["bed"] + d), u"{:+.2f} water".format(G["bed"] + d), C["w4"], True))
        else:
            lv.append((Y(G["sfl"]), u"{:+.2f} strip".format(G["sfl"]), C["w4"], True))
        if sea == "winter":
            lv += [(Y(G["q100"]), u"{:+.2f} Q100".format(G["q100"]), C["w4"], True),
                   (Y(G["q500"]), u"{:+.2f} Q500".format(G["q500"]), C["w4"], True)]
        level_ladder(pg, lv, xl, xl + 3.5, fs, None, lo=yb)
        labs = []
        for zone, name in P14_SPACES[sea]:
            a, b = G["zones"][zone]
            sm = (a + b) / 2.0
            zz = _p14_surf(sm)
            if zone in ("bed", "gravel", "strip") and d >= P14_SHEET_M:
                zz = max(zz, G["bed"] + d)
            labs.append((X(sm), Y(zz) + 0.3, [name], P14_SPACE_COL[zone], True))
        sky_labels(pg, labs, sp.items, xb, xb + wb, rt - 1.5, fs)
        _p14_view(pg, (xv, rbot + 1.2, xv + wv, rt - 1.2), sea)
        _p14_animals(pg, xd, rt - 1.2, wd, rh - 2.4, sea)
    pg.line([(x0, yt - 4 * rh), (x1, yt - 4 * rh)], COL["faint"], 0.25)
    r28_scale_bar(pg, xb, y0 + fs * 1.3 + 0.4, P14_DEN)
    bb = items_bbox(pg.items[n0:])
    if log is not None:
        log.append(u"p.14 S4 seasons: cuts 1:{:,.0f}, rows {:.1f} mm, views {:.0f} mm wide, panel {:.0f} x {:.0f} mm; "
                   u"S4 bed {:+.2f}, width {:,.0f} cm (level module)".format(P14_DEN, rh, wv, bb[2] - bb[0],
                                                                              bb[3] - bb[1], G["bed"],
                                                                              G["width"] * 100.0))
    return [("wb_s4_seasons", bb, P14_DEN)]


# ---------------------------------------------------------------- p.15
P15_KEY = (120.0, 30.0)
P15_GROUPS = [("locals", u"locals", "CC9A52"), ("tourists", u"tourists", "8B3A3F"), ("students", u"students", "5C7A86"),
              ("kermes", u"Kermes visitors", "5E4B8B")]   # the city link's groups (pp.08, 10) + the Kermes
P15_GROUP_COL = dict((g_, c_) for g_, _, c_ in P15_GROUPS)
P15_KERMES = (5 + 28.5 / 30.0, 6 + 5.0 / 31.0)            # 29 Jun-5 Jul in months from 1 Jan (the 90th Kermes, 2026)
P15_USE = [  # who uses the north-east bank, doing what, how much each month Jan-Dec (0 none - 3 busy: our programme,
    # from the season cuts); None = the Kermes week only: (group, pose, height m, keywords, months)
    ("locals", "walk", 1.75, u"walk the promenade", (2, 2, 2, 2, 3, 3, 3, 3, 3, 2, 2, 2)),
    ("locals", "watch", 1.75, u"watch the floods", (3, 3, 1, 1, 0, 0, 0, 0, 0, 0, 1, 3)),
    ("locals", "sit", 1.75, u"sit on the seat steps", (1, 1, 1, 2, 2, 2, 3, 3, 2, 2, 1, 1)),
    ("locals", "touch", 1.15, u"children at the water's edge", (0, 0, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0)),
    ("locals", "wade", 1.75, u"wade in the summer strip", (0, 0, 0, 1, 1, 2, 3, 3, 1, 0, 0, 0)),
    ("locals", "walk", 1.75, u"walk the open gravel bed", (0, 0, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0)),
    ("tourists", "walk", 1.75, u"walk the promenade", (0, 0, 1, 1, 2, 2, 2, 2, 2, 1, 0, 0)),
    ("tourists", "wade", 1.75, u"cool their feet in the strip", (0, 0, 0, 0, 0, 1, 2, 2, 0, 0, 0, 0)),
    ("students", "sit", 1.75, u"meet on the seat steps", (1, 1, 2, 2, 2, 1, 0, 0, 1, 2, 2, 1)),
    ("kermes", "stand", 1.75, u"Kermes stalls on the terrace", None),
]
P15_PLANT_ROWS = ("plane", "ash", "willow", "tamarisk", "chaste", "loosestrife", "soft_rush")
P15_SAY = (u"**Winter and spring** give the bed to the stream; **summer and autumn** give it to people: wading, the "
           u"Kermes market, walking the gravel. The seat steps and the raised promenade are used **all year**.")
P15_BAND_SRC = (u"Rijkswaterstaat (2023). Hydrologische randvoorwaarden van de ecotopen in PAGW rivieren, memo, "
                u"pp. 8-16")
P15_LABEL_W = 78.0                   # the chart's label column, mm


def _p15_days(code):
    if code == "A":
        return u"under water all year"
    lo, hi = BAND_DAYS[code]
    if lo <= 0.0:
        return u"under {:g} days a year".format(hi)
    return u"{:g}–{:g} days a year".format(lo, hi)


def _p15_year(pg, x0, ytop, x1, ybot, log=None):
    """THE YEAR ON ONE MONTH AXIS (R31's idea: a row of pictograms a user group, everyone's activities as bars on one
    time axis): the seasons as p.14 names them, the water (when the stream covers the bed, when the strip runs on stored
    water, when the gravel bed is open), who and when (bar thickness = how busy), the plants in leaf and in flower
    (plants.py), one short conclusion. Fills x0..x1 from ytop down to ybot."""
    fs = FS_MIN
    xa = x0 + P15_LABEL_W
    mw = (x1 - xa) / 12.0
    tx = x0 + 24.0

    def X(t):
        return xa + t * mw
    wet = [m for m in range(12) if _p14_depth(m) >= P14_SHEET_M]
    water = [(u"stream covers the bed", "flood", wet, C["w2"]),
             (u"strip runs on stored water", "strip", [m for m in range(12) if m not in wet], "7FAFC0"),
             (u"gravel bed open to people", "hub_open", list(SUBHUB_OPEN), "D9C79A")]
    say_h = 3.2 * 1.28 * 2 + 2.5
    head_h = fs * 2.6 + 1.2
    blk = fs * 1.6
    nrow = len(water) + len(P15_USE) + len(P15_PLANT_ROWS)
    rh = (ytop - ybot - head_h - say_h - 3 * blk) / nrow
    if rh < 3.4 and log is not None:
        log.append(u"WARNING (D9): p.15 THE YEAR has {:.1f} mm a row, under 3.4: the pair needs more room".format(rh))
    rh = max(3.0, min(6.5, rh))
    yend = ytop - head_h - 3 * blk - nrow * rh
    tint = {"winter": "EDF1F2", "spring": "F0F3E8", "summer": "F7F3E5", "autumn": "F4EEE5"}
    for sea in SEAS:
        for m in S4_MONTH_IDX[sea]:
            pg.poly([rect(X(m), yend, X(m + 1), ytop - fs * 1.3)], fill=tint[sea])
        for a_, b_ in occ_spans(list(S4_MONTH_IDX[sea])):
            pg.text(sea, X((a_ + b_) / 2.0), ytop - fs, fs, COL["ink2"], bold=True, align="C")
    for m in range(12):
        pg.text(MONTHS[m], X(m + 0.5), ytop - fs * 2.3, fs, COL["ink_dark"], align="C")
    for m in range(13):
        pg.line([(X(m), ytop - fs * 1.3), (X(m), yend)], COL["white"], 0.35)
    y = [ytop - head_h]

    def title(t):
        pg.text(t, x0, y[0] - fs * 1.15, fs, COL["ink_dark"], bold=True)
        pg.line([(x0, y[0] - blk + 0.2), (x1, y[0] - blk + 0.2)], COL["faint"], 0.15)
        y[0] -= blk

    def label(words):
        pg.text(words, tx + rh + 0.4, y[0] - rh / 2.0 - fs * 0.35, fs, COL["ink"])

    def bar(a_, b_, colour, frac, alpha=None):
        c_ = y[0] - rh / 2.0
        pg.poly([rect(X(a_) + 0.25, c_ - rh * frac / 2.0, X(b_) - 0.25, c_ + rh * frac / 2.0)], fill=colour,
                alpha=alpha)
    title(u"WATER")
    for words, ic, ms, colour in water:
        icon(pg, ic, tx, y[0] - 0.3, rh - 0.6)
        label(words)
        for a_, b_ in occ_spans(ms):
            bar(a_, b_, colour, 0.55)
        y[0] -= rh
    title(u"WHO, AND WHEN · bar thickness = how busy")
    names = dict((g_, n_) for g_, n_, _ in P15_GROUPS)
    last = None
    for g_, pose, h, words, vals in P15_USE:
        col = P15_GROUP_COL[g_]
        if g_ != last:
            pg.text(names[g_], x0, y[0] - rh / 2.0 - fs * 0.35, fs, col, bold=True)
            last = g_
        pg.poly([rect(tx, y[0] - rh + 0.3, tx + rh - 0.6, y[0] - 0.3)], fill=col)
        kk = (rh - 1.4) / 1.75
        yf = y[0] - rh + 0.6
        _p14_fig(pg, pose, tx + (rh - 0.6) / 2.0, yf + (R28_SEAT * kk if pose == "sit" else 0.0), kk, COL["white"], 1, h)
        label(words)
        if vals is None:
            bar(P15_KERMES[0], P15_KERMES[1], col, 0.85)
            pg.text(u"29 Jun–5 Jul", X(P15_KERMES[1]) + 0.8, y[0] - rh / 2.0 - fs * 0.35, fs, col, bold=True)
        else:
            m = 0
            while m < 12:
                v, n = vals[m], m
                while n + 1 < 12 and vals[n + 1] == v:
                    n += 1
                if v > 0:
                    bar(m, n + 1, col, 0.25 + 0.2 * v, 0.5 + 0.15 * v)
                m = n + 1
        y[0] -= rh
    pg.text(u"PLANTS", x0, y[0] - fs * 1.15, fs, COL["ink_dark"], bold=True)
    xx = x0 + text_w(u"PLANTS", fs, True) + 3.0
    for st, word in (("leaf", u"in leaf"), ("bloom", u"in flower"), ("cut", u"heads cut")):
        _p14_cell(pg, xx, y[0] - fs * 1.15 - 0.2, xx + 3.2, y[0] - fs * 1.15 + fs * 0.75, st)
        pg.text(word, xx + 4.0, y[0] - fs * 1.15, fs, COL["ink"])
        xx += 4.0 + text_w(word, fs) + 3.0
    pg.line([(x0, y[0] - blk + 0.2), (x1, y[0] - blk + 0.2)], COL["faint"], 0.15)
    y[0] -= blk
    for key in P15_PLANT_ROWS:
        sp_ = PLA_SPECIES[key]
        h, cw = [(h_, c_) for k_, s_, h_, c_ in P14_PLANTS if k_ == key][0]
        kk = (rh - 0.8) / max(h, cw)
        _p14_plant(pg, key, tx + (rh - 0.6) / 2.0, y[0] - rh + 0.4, kk, 5, h, cw)
        label(sp_["name"])
        mo = pla_months(key)
        for a_, b_ in occ_spans([m - 1 for m in mo["leaf"]]):
            bar(a_, b_, sp_["colours"].get("fill") or P14_LEAF, 0.3)
        for a_, b_ in occ_spans([m - 1 for m in mo["bloom"] if m not in mo["cut"]]):
            bar(a_, b_, P14_BLOOM, 0.62)
        for m in mo["cut"]:
            c_ = y[0] - rh / 2.0
            _p14_cell(pg, X(m - 1) + 0.25, c_ - rh * 0.31, X(m) - 0.25, c_ + rh * 0.31, "cut")
        y[0] -= rh
    r28_para(pg, x0, y[0] - 1.5, x1 - x0, P15_SAY, 3.2, COL["ink_dark"])


def p15_page(pg, box, opt, log):
    """p.15, the north-east bank of S4 (package D), drawn whole into box (x0, y0, x1, y1), page mm: the context line,
    the S4 key map at the top right, the bank at 1:250 in summer (plants named on it, today's bank dashed) with its
    widths in cm and planting bands under it, the levels and the bands' days under water at its right (the p.20 ladder,
    D9 a), the scale bar flush left under it, then the year on one month axis. Returns its crops."""
    x0, y0, x1, y1 = box
    n0 = len(pg.items)
    fs = FS_MIN
    G = _p14_geo()
    k = 1000.0 / P15_DEN
    s0, s1 = P15_RANGE
    ws = (s1 - s0) * k
    kb = _p14_keymap(pg, (x1 - P15_KEY[0], y1 - P15_KEY[1], x1, y1), log)
    cb = context(pg, x0, y1, min(ws, kb[0] - x0 - 6.0), "ne")
    ztop = max(_p14_surf(s) + h for _, s, h, _ in P14_PLANTS if s0 <= s <= s1)
    yb = cb[1] - 10.0 - (ztop - G["base"]) * k
    sp = Page(0, 0)
    X, Y = _p14_cut(sp, x0, yb, k, P15_RANGE, "summer", P14_SEA_MONTH["summer"])
    pg.items += sp.items
    pg.line([(X(s), Y(z)) for s, z in G["today"] if s <= s1], COL["ink2"], 0.2, dash=[1.0, 0.6])
    labs, done = [], set()
    for key, s, h, cw in P14_PLANTS:
        if s0 + 0.5 <= s <= s1 and key not in done:
            done.add(key)
            t = PLA_SPECIES[key]["name"] + (u", heads cut in Sep" if key == "loosestrife" else u"")
            labs.append((X(s), Y(_p14_surf(s) + h * 0.75), [t], COL["ink_dark"], False))
    sky_labels(pg, labs, sp.items, x0, x0 + ws, cb[1] - 1.0, fs)
    # widths, cm, with the parts' names
    zn = G["zones"]
    dims = [(zn["strip"], u"strip"), ((zn["strip"][1], G["b1"]), u""), (zn["toe"], u"bank"),
            ((zn["terrace"][0], P14_WALK[0]), u"flood terrace"), (zn["walk"], u"lower walk"),
            ((P14_WALK[1], zn["terrace"][1]), u""), (zn["steps"], u"seat steps"), (zn["prom"], u"promenade"),
            (zn["bike"], u"bike lane"), (zn["fill"], u"fill")]
    yd = yb - 3.2
    xs_ = [X(a) for (a, b), _ in dims] + [X(dims[-1][0][1])]
    pg.line([(xs_[0], yd), (xs_[-1], yd)], C["acc"], 0.15)
    for x_ in xs_:
        pg.line([(x_ - 0.6, yd - 0.6), (x_ + 0.6, yd + 0.6)], C["acc"], 0.2)
    for (a, b), name in dims:
        w_ = X(b) - X(a)
        t = u"{:,.0f}".format(round((b - a) * 100.0))
        if text_w(t, fs) < w_ - 0.8:
            pg.text(t, (X(a) + X(b)) / 2.0, yd + 0.7, fs, C["acc"], align="C")
        if name and text_w(name, fs) < w_ + 2.0:
            pg.text(name, (X(a) + X(b)) / 2.0, yd - fs * 1.15, fs, COL["ink"], align="C")
    pg.text(u"cm", xs_[-1] + 1.2, yd - fs * 0.35, fs, C["acc"])
    # the planting bands along the cut (where water reaches the ground how often)
    yt_b, hb = yd - fs * 1.15 - 1.6, 3.0
    runs, s, step = [], s0, 0.1
    while s < s1 - 1e-9:
        c_ = _p14_band_code(s + step / 2.0, _p14_surf(s + step / 2.0))
        if runs and runs[-1][0] == c_:
            runs[-1][2] = s + step
        else:
            runs.append([c_, s, s + step])
        s += step
    for c_, a, b in runs:
        pg.poly([rect(X(a), yt_b - hb, X(min(b, s1)), yt_b)], fill=BAND_COL[c_])
        if X(b) - X(a) > 3.0:
            pg.text(c_, (X(a) + X(b)) / 2.0, yt_b - hb + 0.55, fs, COL["ink_dark"], bold=True, align="C")
    bar = r28_scale_bar(pg, x0, yt_b - hb - 1.6 - (2.0 + fs * CAP + 0.2), P15_DEN)
    # at the right: the levels, and the bands with their days under water (the p.20 ladder, D9 a)
    xr = x0 + ws + 4.0
    bands = [("A", G["sfl"], G["bed"]), ("B", G["bed"], G["bed"] + G["dmax"]),
             ("C", G["bed"] + G["dmax"], G["shelf"]), ("D", G["shelf"], G["q100"]), ("E", G["q100"], G["q500"]),
             ("F", G["q500"], P14_PROM)]
    for c_, lo, hi in bands:
        pg.poly([rect(xr, Y(lo), xr + 3.0, Y(hi))], fill=BAND_COL[c_], stroke=COL["white"], lw=0.1)
    levels = sorted([(G["sfl"], u"strip floor"), (G["bed"], u"bed"), (G["shelf"], u"flood terrace"),
                     (G["ne_top"], u"bank today"), (G["q100"], u"Q100"), (G["q500"], u"Q500"),
                     (P14_PROM, u"promenade")])
    ys = spread([Y(z) - fs * 0.35 for z, _ in levels], fs * 1.25)
    for (z, name), yl in zip(levels, ys):
        pg.line([(xr - 1.0, Y(z)), (xr + 4.0, Y(z)), (xr + 5.5, yl + fs * 0.35), (xr + 6.2, yl + fs * 0.35)],
                COL["ink2"], 0.1)
        pg.text(u"{:+.2f} {}".format(z, name), xr + 6.6, yl, fs, C["w4"] if name[0] == u"Q" else COL["ink"])
    xc2 = xr + 6.6 + max(text_w(u"{:+.2f} {}".format(z, n_), fs) for z, n_ in levels) + 4.0
    bn = dict((b_[0], b_[1]) for b_ in PLANT_BANDS)
    bn["A"] = u"summer strip"
    ys2 = spread([(Y(lo) + Y(hi)) / 2.0 - fs * 0.35 for _, lo, hi in bands], fs * 1.3)
    for (c_, lo, hi), yl in zip(bands, ys2):
        pg.poly([rect(xc2, yl - 0.4, xc2 + 3.2, yl + fs * 0.85)], fill=BAND_COL[c_])
        pg.text(c_, xc2 + 1.6, yl, fs, COL["ink_dark"], bold=True, align="C")
        pg.text(u"{} · {}".format(bn[c_], _p15_days(c_)), xc2 + 4.2, yl, fs, COL["ink"])
    pg.text(u"LEVELS · PLANTING BANDS, days under water " + cite(P15_BAND_SRC), xr, max(ys[-1], ys2[-1]) + fs * 2.2,
            fs, COL["ink_dark"], bold=True)
    _p15_year(pg, x0, bar[1] - 3.0, x1, y0, log)
    bb = items_bbox(pg.items[n0:])
    if log is not None:
        log.append(u"p.15 S4 north-east bank 1:{:,.0f} and the year: panel {:.0f} x {:.0f} mm{}".format(
            P15_DEN, bb[2] - bb[0], bb[3] - bb[1], u"" if bb[1] >= y0 - 0.5 else
            u" (WARNING D9: {:.1f} mm below the cell: the pair does not fit two pages)".format(y0 - bb[1])))
    return [("wb_s4_ne", bb, P15_DEN)]
# p.17 planting and water (water board v6, revision 29 Oct 2026, T4a WO-T4a-2, package F "Page 17"; D2, D6, D9 a: the
# p.20 ladder folds into this page and pp.14-15). Two booklet pages, built from project data only:
#   page A (p17_page, crop wb_plants): the PLAN. A key strip of the analysis frame (basemap "topographic", the two plan
#        windows, the hubs; no cut lines: page A draws no section) and two plan windows at one standard scale on the
#        shared basemap (streets, buildings, fields): the upstream entry (reed basins, spillway, shaded walk, rain
#        terraces, summer strip) and the lower reach (widened stream and wetland, side arm, summer strip). Every
#        species as its top-view crown at true size (plants.py pla_plan, the same size as in the sections), every
#        water space numbered (R35), July shade hours on the bed and the water spaces (site board shade_july.json),
#        the cut lines F1-F4 of page B. Under them the numbered list and the species catalogue (R36: photo, silhouette
#        and crown from the primitives, foliage, height, water, role; sourced values only, species.json + plants.py).
#   page B (p17b_page, crop wb_plants_b): the SECTIONS at 1:500, each with its zone labels on vertical lines, levels
#        from the level module, people by activity (_p17_fig), a scale bar: F2 rain terraces + reed basins (new line,
#        LEVELS "F2"), F4 side arm (new line, LEVELS "F4"), F1 the stream at the inflow on the W1 line with the reed
#        basins beyond, F3 the widened stream on the S4 line with the planting bands and their days under water (the
#        S4 band section folded in; the S4 geometry and plants are p.14's own, _p14_geo / P14_PLANTS, so the cut is the
#        same everywhere). A key map with ONLY F1-F4, the bloom / leaf calendar (one month axis), giant reed: remove.
# build_board calls P17_TITLE, P17B_TITLE, p17_page(pg, box, opt, log), p17b_page(pg, box, opt, log); each returns
# [(crop id, bbox, scale denominator)].

P17_TITLE = u"PLANTING AND WATER · where each plant goes around the water spaces"
P17B_TITLE = u"PLANTING AND WATER IN SECTION · four cuts, the species and their year"
P17_W = 377.0                        # the most a page takes, mm (the booklet's A3 panel at 1:1)
P17_SAY = (u"**Wet to dry, low to high**: rushes and loosestrife at the water, willow and tamarisk on the banks that "
           u"flood, shade trees and olives on the dry tops. **Common reed and water mint** only in lined basins the "
           u"flood bypasses.")
P17B_SAY = (u"Each cut shows the **water**, the **planting band** each species needs, and **what surrounds it**: "
            u"streets, walks, terraces.")
# sizes drawn (m): (height, crown) as p.14 draws S4 (trees at about ten years, inside plants.py's sourced ranges); the
# others plants.py's own (None). The plan, the sections and the catalogue use these, so a crown and its tree agree.
P17_SIZE = {"plane": (12.0, 12.0), "ash": (12.0, 8.4), "willow": (10.0, 7.0), "tamarisk": (5.0, 4.5),
            "chaste": (3.0, 2.5), "loosestrife": (1.5, 1.0), "soft_rush": (1.0, 0.6), "olive": (5.0, 5.0),
            "lavender": (None, None), "rosemary": (None, None)}
P17_CAT = ("reed", "mint", "soft_rush", "loosestrife", "willow", "tamarisk", "chaste", "ash", "plane", "olive",
           "rosemary", "lavender")   # the catalogue, wet to dry
P17_DENS = (1000.0, 2000.0, 2500.0, 5000.0)   # the plan windows: the first standard scale at which both fit
P17_BAR = {1000.0: (0, 10, 20, 50), 2000.0: (0, 20, 50, 100), 2500.0: (0, 20, 50, 100), 5000.0: (0, 50, 100, 200)}
P17_SEC_DEN = 500.0                  # every section
P17_FS, P17_HEAD = FS_MIN, 3.4       # label and heading sizes, mm
P17_FIG = "4F453C"                   # people
P17_WATER = "8CBBC8"                 # summer water in the sections and the strip in plan
P17_ZONE = {"WT": ("CBEDE5", "8DB8AF"), "WD": ("C1D3DB", "889EA8"), "GR": ("E9E3D2", "B0AC9C"),
            "WS": ("E6DFC6", "B5AA93"), "WP": ("DCE9D2", "A7B67F"), "ARM": ("B9D7DE", "5D7F8D"),
            "STRIP": (P17_WATER, "4B92A3"), "WIDEN": ("D3E4E8", "889EA8")}
P17_SHADE = ((2.0, "E6DCC6", u"under 2 h"), (5.0, "CDBF9F", u"2-5 h"), (99.0, "A99A78", u"over 5 h"))
P17_BASIN = dict(kerb_h=0.30, depth=1.10, media=0.80, kerb_t=0.15)   # lined basin cell: drawing values (no source)
P17_ARM_W = 3.0                      # the side arm, m either side of its line (masterplan R28DT_ARM_M)
# the side arm the F4 cut crosses, survey m, while the masterplan writes no corridor geometry: its middle part read off
# the masterplan plan (p.23, georeferenced on the analysis frame, +-5 m); masterplan_results.json "corridor" "arms"
# replaces it when present (log line otherwise)
P17_ARM_FALLBACK = [(30666.1, 31215.0), (30680.9, 31177.7), (30722.8, 31141.0), (30768.4, 31113.1),
                    (30804.0, 31090.5), (30834.3, 31057.9), (30869.1, 31026.4), (30894.6, 31025.7),
                    (30918.6, 31043.1)]
P17_ROWS_L = 45.0                    # plan: the planting bands of a cut repeat this far up and down the stream, m


# ---------------------------------------------------------------- small helpers
def _p17_put(pg, shapes):
    sec_put(pg, shapes)


def _p17_fig(pg, pose, x, y, k, facing=1, view="side", h_m=1.70, col=None, **p):
    """ONE place for the people of p.17 (common/figures.py): side view feet at (x, y) or top view centred there, k mm
    per m. "sit" = the library's sit_chair."""
    ink = col or P17_FIG
    if view == "top":
        sh = fig_top(pose, x, y, k, ink=ink)
    else:
        sh = fig_side("sit_chair" if pose == "sit" else pose, x, y, k, facing, ink=ink, h_m=h_m, **p)
    _p17_put(pg, sh)


def _p17_size(key):
    h, w = P17_SIZE.get(key, (None, None))
    sp = PLA_SPECIES[key]
    return (h or sp["h_m"]), (w or sp["crown_m"])


def _p17_sec_plant(pg, key, x, gy, k, seed=0, beyond=False):
    h, w = _p17_size(key)
    _p17_put(pg, pla_section(key, x, gy, k, h_m=h, crown_m=w, beyond=beyond, seed=seed))


def _p17_plan_plant(pg, key, x, y, k, seed=0):
    _p17_put(pg, pla_plan(key, x, y, k, crown_m=_p17_size(key)[1], seed=seed))


def _p17_rnd(i, s=0):
    """a fixed jitter 0-1 (the same every run)"""
    v = math.sin(i * 12.9898 + s * 78.233) * 43758.5453
    return v - math.floor(v)


def _p17_pip(p, ring):
    x, y, ins = p[0], p[1], False
    n = len(ring)
    for i in range(n):
        (xa, ya), (xb, yb) = ring[i], ring[(i + 1) % n]
        if (ya > y) != (yb > y) and x < xa + (y - ya) * (xb - xa) / (yb - ya):
            ins = not ins
    return ins


def _p17_cen(R):
    return (sum(p[0] for p in R) / len(R), sum(p[1] for p in R) / len(R))


def _p17_half(ring, a, n):
    """ring clipped to the half plane (p - a) . n >= 0 (Sutherland-Hodgman, one edge)"""
    def f(p):
        return (p[0] - a[0]) * n[0] + (p[1] - a[1]) * n[1]
    out = []
    for i in range(len(ring)):
        p, q = ring[i - 1], ring[i]
        fp, fq = f(p), f(q)
        if fq >= 0:
            if fp < 0:
                t = fp / (fp - fq)
                out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
            out.append(q)
        elif fp >= 0:
            t = fp / (fp - fq)
            out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
    return out if len(out) >= 3 else None


def _p17_seg_d(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 < 1e-12 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def _p17_line_d(p, P):
    return min(_p17_seg_d(p, a, b) for a, b in zip(P[:-1], P[1:])) if len(P) > 1 else 1e9


def _p17_along(P, d):
    """point and unit direction at arc length d along the polyline P (clamped)"""
    acc = 0.0
    for a, b in zip(P[:-1], P[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L < 1e-9:
            continue
        if acc + L >= d or b is P[-1]:
            t = max(0.0, min(1.0, (d - acc) / L))
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        acc += L
    a, b = P[-2], P[-1]
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    return b, ((b[0] - a[0]) / L, (b[1] - a[1]) / L)


def _p17_cross(a, b, P):
    """where the segment a-b crosses the polyline P first: (point, arc length along P) or None"""
    acc = 0.0
    for p, q in zip(P[:-1], P[1:]):
        L = math.hypot(q[0] - p[0], q[1] - p[1])
        d1 = (b[0] - a[0], b[1] - a[1])
        d2 = (q[0] - p[0], q[1] - p[1])
        den = d1[0] * d2[1] - d1[1] * d2[0]
        if abs(den) > 1e-12:
            w = (p[0] - a[0], p[1] - a[1])
            t = (w[0] * d2[1] - w[1] * d2[0]) / den
            s = (w[0] * d1[1] - w[1] * d1[0]) / den
            if 0.0 <= t <= 1.0 and 0.0 <= s <= 1.0:
                return (a[0] + d1[0] * t, a[1] + d1[1] * t), acc + s * L
        acc += L
    return None


def _p17_text_box(s, x, y, fs, bold=False, align="L"):
    w = text_w(s, fs, bold)
    x0 = x - {"L": 0.0, "C": w / 2.0, "R": w}[align]
    return (x0, y - fs * 0.3, x0 + w, y + fs * CAP)


def _p17_badge(pg, n, x, y, size=3.6, colour=None):
    """a numbered water-space badge (icons.py ico_step) centred on (x, y); its box"""
    sh, (ax, ay), th, cap = ico_step(x, y, size, "solid", colour or MP["discharge"][2])
    _p17_put(pg, sh)
    pg.text(str(n), ax, ay - cap / 2.0, cap / CAP, th, bold=True, align="C")
    return (x - size / 2.0, y - size / 2.0, x + size / 2.0, y + size / 2.0)


def _p17_north(pg, x, y, d, L=6.0):
    """north arrow at (x, y) along the unit page direction d; its box"""
    tip = (x + d[0] * L, y + d[1] * L)
    arrow(pg, [(x, y), tip], COL["ink"], 0.3, 1.8)
    pg.text(u"N", tip[0] + d[0] * 1.8, tip[1] + d[1] * 1.8 - P17_FS * CAP / 2.0, P17_FS, COL["ink"], bold=True,
            align="C")
    return (min(x, tip[0]) - 3.0, min(y, tip[1]) - 3.0, max(x, tip[0]) + 3.0, max(y, tip[1]) + 3.5)


# ---------------------------------------------------------------- data, read once a run
_P17_MEMO = {}


def _p17_zones():
    """the Option A zones (survey m) from the water balance results "zones": [dict(code, label, ring, ...)]"""
    if "zones" not in _P17_MEMO:
        z = _p12_get("zones") or {}
        _P17_MEMO["zones"] = [dict(q, ring=[tuple(p) for p in q["ring"]]) for q in z.get("zones") or []
                              if len(q.get("ring") or []) >= 3]
    return _P17_MEMO["zones"]


def _p17_mp(log):
    """masterplan_results.json (the masterplan's cache folder), read once; {} when missing (logged)"""
    if "mp" not in _P17_MEMO:
        d = {}
        for fn in (os.path.join(bg_cache("bergama_masterplan"), "masterplan_results.json"),
                   os.path.join(bg_output("bergama_masterplan"), "masterplan_results.json")):
            try:
                with open(fn, "r", encoding="utf-8") as f:
                    d = json.load(f)
                break
            except Exception:
                continue
        if not d:
            log.append(u"p.17: no masterplan_results.json: hubs from the four chain places, side arm from its p.23 line")
        _P17_MEMO["mp"] = d
    return _P17_MEMO["mp"]


def _p17_hubs(log):
    """[(name, (x, y))] the hubs of the masterplan's movement, else K4 and K5 of the chain"""
    hs = ((_p17_mp(log).get("movement") or {}).get("hubs")) or []
    out = [(h.get("name") or u"", tuple(h["xy"])) for h in hs if h.get("xy")]
    return out or [(n, p) for n, p in P12_PLACES if n.startswith(u"K")]


def _p17_arms(log):
    """the side arms (survey m polylines): masterplan_results.json "corridor" "arms" (a later masterplan writes it),
    else the one read off p.23 that F4 crosses"""
    co = _p17_mp(log).get("corridor") or {}
    arms = [[tuple(p) for p in (a.get("P") if isinstance(a, dict) else a)] for a in co.get("arms") or []]
    if arms:
        return arms
    if "arm_log" not in _P17_MEMO:
        _P17_MEMO["arm_log"] = 1
        log.append(u"p.17: the masterplan writes no corridor geometry: the side arm is the one read off p.23 (+-5 m)")
    return [list(P17_ARM_FALLBACK)]


def _p17_widen(log):
    co = _p17_mp(log).get("corridor") or {}
    return [[tuple(p) for p in (w.get("ring") if isinstance(w, dict) else w)] for w in co.get("widen") or []]


def _p17_shade(log):
    """(cells [(x, y, hours)], daylight h, cell m) from the site board's shade_july.json, read once; None (one log
    line)"""
    if "shade" not in _P17_MEMO:
        r = None
        fn = os.path.join(bg_output("selinus_board"), "shade_july.json")
        try:
            with open(fn, "r", encoding="utf-8") as f:
                d = json.load(f)
            cells = [(float(c[0]), float(c[1]), float(c[2])) for c in (d.get("map") or {}).get("cells") or []]
            if cells:
                r = (cells, float(d.get("daylight_h") or 0.0), float((d.get("map") or {}).get("cell_m") or 5.0))
        except Exception:
            r = None
        if r is None:
            log.append(u"p.17: no shade_july.json ({}): the plans are drawn without July shade (run the site board v51+ "
                       u"with its environment analyses)".format(fn))
        _P17_MEMO["shade"] = r
    return _P17_MEMO["shade"]


def _p17_s4_pt(s):
    """the S4 point s m across the stream from where S4 crosses the Selinos line (north-east +), survey m"""
    if "s4" not in _P17_MEMO:
        a, b = level_ends("S4")
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        c = _p17_cross(a, b, P12_SELINOS)
        _P17_MEMO["s4"] = ((c[0] if c else ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)), u)
    o, u = _P17_MEMO["s4"]
    return (o[0] + u[0] * s, o[1] + u[1] * s)


def _p17_cut_pt(cid, t):
    """the point t m along a level cut from its first end, survey m"""
    a, b = level_ends(cid)
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    return (a[0] + (b[0] - a[0]) * t / L, a[1] + (b[1] - a[1]) * t / L)


def _p17_lv(cid, key, side=None):
    v = level(cid, key, side)
    if v is None:
        raise RuntimeError(u"{}: '{}' {} is missing in the level module (common/data/LEVELS.py)".format(
            cid, key, side or u""))
    return v


def _p17_ground(cid):
    """the surveyed ground of a T4a cut [(m along, m a.s.l.)] (LEVELS row field "ground")"""
    g = (level_cut(cid).get("ground") or {}).get("value") or []
    if len(g) < 2:
        raise RuntimeError(u"{}: no ground profile in the level module".format(cid))
    return [(float(t), float(z)) for t, z in g]


def _p17_interp(P, t):
    if t <= P[0][0]:
        return P[0][1]
    for (a, za), (b, zb) in zip(P[:-1], P[1:]):
        if a <= t <= b:
            return za + (zb - za) * (t - a) / ((b - a) or 1.0)
    return P[-1][1]


# ---------------------------------------------------------------- page A: the plan windows
# the plants of each cut (m along the cut from its first end; S4: p.14's own list, m across from the bed), repeated in
# plan as rows along the stream P17_ROWS_L either side of the cut, at the same offset from the Selinos line
P17_F1_PLANTS = [("plane", 6.0), ("plane", 16.0), ("loosestrife", 23.4), ("soft_rush", 29.6), ("loosestrife", 30.4),
                 ("soft_rush", 53.9), ("ash", 63.0)]
P17_F4_PLANTS = [("ash", 16.0), ("plane", 22.0), ("loosestrife", 25.8), ("soft_rush", 34.2), ("ash", 41.0),
                 ("tamarisk", 50.0), ("chaste", 55.5), ("willow", 64.0), ("chaste", 69.5), ("soft_rush", 75.0),
                 ("soft_rush", 85.6), ("loosestrife", 92.0), ("soft_rush", 112.8), ("chaste", 117.5),
                 ("tamarisk", 122.5), ("plane", 137.0)]


def _p17_axis(R):
    """centre, long axis u, its normal v and the half extents along u and v of a ring (principal axes)"""
    c = _p17_cen(R)
    sxx = sum((p[0] - c[0]) ** 2 for p in R)
    syy = sum((p[1] - c[1]) ** 2 for p in R)
    sxy = sum((p[0] - c[0]) * (p[1] - c[1]) for p in R)
    a = 0.5 * math.atan2(2.0 * sxy, sxx - syy)
    u, v = (math.cos(a), math.sin(a)), (-math.sin(a), math.cos(a))
    us = [(p[0] - c[0]) * u[0] + (p[1] - c[1]) * u[1] for p in R]
    vs = [(p[0] - c[0]) * v[0] + (p[1] - c[1]) * v[1] for p in R]
    return c, u, v, (min(us), max(us)), (min(vs), max(vs))


def _p17_frame_uv():
    """the analysis frame's long axis (upstream end at the left) and its normal, or None"""
    fr = basemap_frame()
    if not fr:
        return None
    cx, cy = _p17_cen(fr)
    e1 = (fr[1][0] - fr[0][0], fr[1][1] - fr[0][1])
    e2 = (fr[2][0] - fr[1][0], fr[2][1] - fr[1][1])
    u = e1 if math.hypot(*e1) >= math.hypot(*e2) else e2
    L = math.hypot(*u)
    u = (u[0] / L, u[1] / L)
    if (fr[0][0] - cx) * u[0] + (fr[0][1] - cy) * u[1] > 0:
        u = (-u[0], -u[1])
    return u, (-u[1], u[0])


def _p17_win_pts(key, log):
    """the survey points a plan window must hold"""
    pts = []
    zs = _p17_zones()
    if key == "A":
        for cid in ("F2", "W1"):
            pts += list(level_ends(cid))
        pts += [p for z in zs if z.get("study_area") == "aras_alan" and z["code"] != "STRIP" for p in z["ring"]]
    else:
        pts += list(level_ends("F4"))
        pts += [_p17_s4_pt(s) for s in P14_RANGE]
        pts += [p for z in zs if z["code"] == "WP" for p in z["ring"]]
        mid = _p17_cut_pt("F4", 0.5 * level("F4", "length_m"))
        pts += [p for a in _p17_arms(log) for p in a if math.hypot(p[0] - mid[0], p[1] - mid[1]) < 150.0]
    return pts


def _p17_win_fit(pts, den, pad=8.0):
    """the best turn for a window at 1:den: (w mm, h mm, u, v, centre, den) of north-up or along the frame, the smaller"""
    best = None
    k = 1000.0 / den
    turns = [((1.0, 0.0), (0.0, 1.0))]
    fu = _p17_frame_uv()
    if fu:
        turns.append(fu)
    for u, v in turns:
        us = [p[0] * u[0] + p[1] * u[1] for p in pts]
        vs = [p[0] * v[0] + p[1] * v[1] for p in pts]
        w, h = (max(us) - min(us) + 2 * pad) * k, (max(vs) - min(vs) + 2 * pad) * k
        c = ((min(us) + max(us)) / 2.0, (min(vs) + max(vs)) / 2.0)
        if best is None or w * h < best[0] * best[1] - 1e-6:
            best = (w, h, u, v, c, den)
    return best


def _p17_basemap_into(sp, items, T):
    def fill_fn(rings, hx, alpha, nonzero):
        sp.poly([r_ for r_ in rings if len(r_) >= 3], fill=hx, alpha=alpha if alpha is not None and alpha < 0.999 else None)

    def line_fn(pts, hx, w_mm, dash_mm, alpha):
        d_ = None
        if dash_mm:
            d_ = list(dash_mm) if isinstance(dash_mm, (list, tuple)) else [dash_mm, dash_mm]
        sp.line(pts, hx, w_mm, dash=d_)
    basemap_draw(items, T, fill_fn, line_fn)


def _p17_fill_rings(items):
    """the rings of the fill items of a basemap item list (survey m)"""
    out = []
    for it in items:
        if it[0] == "fill":
            out += [r for r in it[1] if len(r) >= 3]
    return out


def _p17_rows(sp, cid, plants, T, k, skip, n0=0):
    """the planting of a cut repeated in plan as rows along the Selinos line, P17_ROWS_L either side of the cut, at
    each plant's offset from the line; skip(p_survey, key) leaves a spot out"""
    a, b = level_ends(cid)
    c = _p17_cross(a, b, P12_SELINOS)
    if not c:
        return 0
    (cx, cy), d0 = c
    t0 = math.hypot(cx - a[0], cy - a[1])
    ux, uy = b[0] - a[0], b[1] - a[1]
    n = 0
    for i, (key, t) in enumerate(plants):
        off = t - t0
        cw = _p17_size(key)[1]
        step = max(1.3 * cw, 2.0)
        d = d0 - P17_ROWS_L
        j = 0
        while d <= d0 + P17_ROWS_L:
            (px, py), (dx, dy) = _p17_along(P12_SELINOS, d)
            nx, ny = -dy, dx
            if nx * ux + ny * uy < 0:
                nx, ny = -nx, -ny
            jit = (_p17_rnd(i * 97 + j, 3) - 0.5) * 0.3 * step
            q = (px + nx * (off + jit * 0.3), py + ny * (off + jit * 0.3))
            if not skip(q, key):
                X, Y = T(q)
                _p17_plan_plant(sp, key, X, Y, k, n0 + i * 31 + j)
                n += 1
            d += step + jit
            j += 1
    return n


def _p17_window(pg, x0, ytop, key, den, fit, log):
    """one plan window, its top-left at (x0, ytop): the basemap, the water spaces with their planting, July shade, the
    cut lines, the hubs and the numbered badges, frame, north arrow and scale bar under it. Returns (bbox, numbers)."""
    w, h, u, v, c = fit[:5]
    k = 1000.0 / den
    R = (x0, ytop - h, x0 + w, ytop)
    ox, oy = (R[0] + R[2]) / 2.0, (R[1] + R[3]) / 2.0

    def T(p):
        return (ox + ((p[0] * u[0] + p[1] * u[1]) - c[0]) * k, oy + ((p[0] * v[0] + p[1] * v[1]) - c[1]) * k)

    def Ti(X, Y):
        a_, b_ = (X - ox) / k + c[0], (Y - oy) / k + c[1]
        return (a_ * u[0] + b_ * v[0], a_ * u[1] + b_ * v[1])
    corners = [Ti(R[0], R[1]), Ti(R[2], R[1]), Ti(R[2], R[3]), Ti(R[0], R[3])]
    sb = (min(p[0] for p in corners), min(p[1] for p in corners), max(p[0] for p in corners),
          max(p[1] for p in corners))

    def inR(p):
        X, Y = T(p)
        return R[0] <= X <= R[2] and R[1] <= Y <= R[3]
    sp = Page(0, 0)
    sp.poly([rect(*R)], fill=COL["white"])
    D = basemap_load(log=log)
    bld, water = [], []
    if D:
        try:
            _p17_basemap_into(sp, basemap_items("detailed", {"trees": False, "green": False, "contours": False},
                                                box=sb, D=D, split_buildings=True), T)
            off = {"stream": False, "streets": False, "buildings": False, "green": False, "trees": False,
                   "fields": False, "contours": False}
            bld = _p17_fill_rings(basemap_items("detailed", dict(off, buildings=True), box=sb, D=D, split_buildings=True))
            water = _p17_fill_rings(basemap_items("detailed", dict(off, stream=True), box=sb, D=D))
        except Exception as ex:
            log.append(u"p.17 plan {}: basemap not drawn: {}: {}".format(key, type(ex).__name__, ex))
    zs = [z for z in _p17_zones() if any(inR(p) for p in z["ring"])]
    arms = [a for a in _p17_arms(log) if any(inR(p) for p in a)]
    widen = [r for r in _p17_widen(log) if any(inR(p) for p in r)]
    for r in widen:
        sp.poly([[T(p) for p in r]], fill=P17_ZONE["WIDEN"][0], stroke=P17_ZONE["WIDEN"][1], lw=0.1)
    for z in zs:                                         # the water spaces, flat (planting comes after the shade)
        if z["code"] in P17_ZONE and z["code"] != "WT":
            f_, s_ = P17_ZONE[z["code"]]
            sp.poly([[T(p) for p in z["ring"]]], fill=f_, stroke=s_, lw=0.12)
    for a in arms:
        P = [T(p) for p in a]
        sp.poly([_p14_band(P, 2.0 * P17_ARM_W * k)], fill=P17_ZONE["ARM"][0], stroke=P17_ZONE["ARM"][1], lw=0.12)
    # July shade on the bed and the water spaces (5 m cells, three classes)
    sh = _p17_shade(log)
    spaces = water + [z["ring"] for z in zs] + widen
    if sh:
        cells, day, cm = sh
        hc = cm / 2.0
        for x, y, hrs in cells:
            if not (sb[0] - cm <= x <= sb[2] + cm and sb[1] - cm <= y <= sb[3] + cm):
                continue
            q = (x, y)
            if not (any(_p17_pip(q, r) for r in spaces) or any(_p17_line_d(q, a) <= P17_ARM_W for a in arms)):
                continue
            col = next(cl for lim, cl, _ in P17_SHADE if hrs < lim)
            sp.poly([[T((x - hc, y - hc)), T((x + hc, y - hc)), T((x + hc, y + hc)), T((x - hc, y + hc))]], fill=col,
                    alpha=0.6)
    # the planting: lined basin cells, spillway rushes, shaded walk planes, rain terraces, the strip's edges,
    # the wetland, the side arm, the rows of the cuts
    taken_rings = []
    for z in zs:
        Rp = [T(p) for p in z["ring"]]
        code = z["code"]
        try:
            if code == "WT":
                cz, au, av, (a0, a1), _ = _p17_axis(Rp)
                cuts = [a0 + (a1 - a0) * f for f in (1.0 / 3.0, 2.0 / 3.0)]
                cells = []
                for i, kind in enumerate(("reed", "reed", "mint")):
                    rr = Rp
                    if i > 0:
                        rr = _p17_half(rr, (cz[0] + au[0] * cuts[i - 1], cz[1] + au[1] * cuts[i - 1]), au)
                    if rr and i < 2:
                        rr = _p17_half(rr, (cz[0] + au[0] * cuts[i], cz[1] + au[1] * cuts[i]), (-au[0], -au[1]))
                    if rr:
                        cells.append((kind, rr))
                for kind, rr in cells:
                    _p17_put(sp, pla_cell_plan(kind, rr, k, P17_BASIN["kerb_t"]))
                taken_rings.append(z["ring"])
            elif code == "WD":
                _p17_scatter(sp, Rp, ("soft_rush",), 1.6 * k, k, 11)
                taken_rings.append(z["ring"])
            elif code == "GR":
                cz, au, av, (a0, a1), _ = _p17_axis(Rp)
                cw = _p17_size("plane")[1] * k
                n = max(1, int((a1 - a0) / cw))
                for i in range(n):
                    s = a0 + (a1 - a0) * (i + 0.5) / n
                    p = (cz[0] + au[0] * s, cz[1] + au[1] * s)
                    if _p17_pip(p, Rp):
                        _p17_plan_plant(sp, "plane", p[0], p[1], k, 50 + i)
                taken_rings.append(z["ring"])
            elif code == "WS":
                cz, au, av, (a0, a1), (b0, b1) = _p17_axis(Rp)
                ang = math.degrees(math.atan2(au[1], au[0]))
                bb = b0 + 7.0 * k
                while bb < b1 - 1e-6:                        # terrace edges along the contours, 7 m apart
                    seg = [(cz[0] + au[0] * a0 * 1.2 + av[0] * bb, cz[1] + au[1] * a0 * 1.2 + av[1] * bb),
                           (cz[0] + au[0] * a1 * 1.2 + av[0] * bb, cz[1] + au[1] * a1 * 1.2 + av[1] * bb)]
                    for run in _p17_clip_seg(seg, Rp):
                        sp.line(run, "8C8170", 0.3)
                        L = math.hypot(run[1][0] - run[0][0], run[1][1] - run[0][1])
                        m = int(L / (1.5 * k))
                        for j in range(m):
                            t = (j + 0.5) / max(m, 1)
                            q = (run[0][0] + (run[1][0] - run[0][0]) * t + av[0] * 0.8 * k,
                                 run[0][1] + (run[1][1] - run[0][1]) * t + av[1] * 0.8 * k)
                            _p17_plan_plant(sp, "rosemary" if j % 2 else "lavender", q[0], q[1], k, 70 + j)
                    bb += 7.0 * k
                _p17_put(sp, pla_crop_plan("olive", Rp, k, row_spacing=7.0, plant_spacing=5.0, ang_deg=ang,
                                           crown_m=_p17_size("olive")[1], field=False))
                taken_rings.append(z["ring"])
            elif code == "STRIP":
                _p17_edge(sp, Rp, ("soft_rush", "loosestrife"), 2.5 * k, k, 90)
            elif code == "WP":
                _p17_wetland(sp, z["ring"], T, k, bld)
                taken_rings.append(z["ring"])
        except Exception as ex:
            log.append(u"p.17 plan {}: {} not planted: {}: {}".format(key, code, type(ex).__name__, ex))
    for a in arms:
        P = [T(p) for p in a]
        for side in (-1.0, 1.0):
            _p17_edge(sp, _p17_offset(P, side * (P17_ARM_W + 1.0) * k), ("soft_rush", "loosestrife"), 2.2 * k, k,
                      120 if side > 0 else 140, closed=False)

    def skip(q, key_):
        if any(_p17_pip(q, r) for r in bld) or any(_p17_pip(q, r) for r in taken_rings):
            return True
        if key_ not in ("soft_rush", "loosestrife") and any(_p17_line_d(q, a) <= P17_ARM_W + 0.5 for a in arms):
            return True
        return not inR(q)
    for cid, plants in (("W1", P17_F1_PLANTS), ("F4", P17_F4_PLANTS)):
        if inR(_p17_cut_pt(cid, 0.5 * level(cid, "length_m"))):
            _p17_rows(sp, cid, plants, T, k, skip, 200)
    if key == "B":
        a_, _b = level_ends("S4")
        t0 = math.hypot(_p17_s4_pt(0.0)[0] - a_[0], _p17_s4_pt(0.0)[1] - a_[1])
        _p17_rows(sp, "S4", [(key_, t0 + s) for key_, s, _h, _w in P14_PLANTS], T, k, skip, 400)
    # the cut lines of page B (F1 on W1, F3 on S4), dash-dot, their names at the ends
    taken = []
    for cid, nm in P17_CUTS:
        a, b = level_ends(cid)
        A, B = T(a), T(b)
        runs = _p14_clip_line([A, B], (R[0] + 1.0, R[1] + 1.0, R[2] - 1.0, R[3] - 1.0))
        for run in runs:
            sp.line(run, COL["ink_dark"], 0.3, dash=[2.4, 0.7, 0.4, 0.7])
            for (px, py), lab in ((run[0], nm), (run[-1], nm + u"'")):
                bx = _p17_text_box(lab, px, py + 0.8, P17_FS, True, "C")
                sp.text(lab, px, py + 0.8, P17_FS, COL["ink_dark"], bold=True, align="C")
                taken.append(bx)
    # hubs: the icon and the name
    for name, xy in _p17_hubs(log):
        if inR(xy):
            X, Y = T(xy)
            _p17_put(sp, ico_badge("hub", X, Y, 4.0))
            sp.text(name, X + 2.8, Y - P17_FS * 0.35, P17_FS, COL["ink_dark"], bold=True)
            taken.append((X - 2.0, Y - 2.0, X + 2.8 + text_w(name, P17_FS, True), Y + 2.0))
    # numbered badges, one per water space in the window
    nums = []
    for n, code, name, keys in PLANT_SITES:
        at = None
        if code == "ARM":
            if arms:
                at = T(_p17_along(arms[0], 0.5 * sum(math.hypot(q[0] - p[0], q[1] - p[1])
                                                     for p, q in zip(arms[0][:-1], arms[0][1:])))[0])
        else:
            cand = [z for z in zs if z["code"] == code]
            if cand:
                z = max(cand, key=lambda z_: len(z_["ring"]))
                if code == "STRIP":
                    inside = [T(p) for p in z["ring"] if inR(p)]
                    at = inside[len(inside) // 2] if inside else None
                else:
                    at = T(_p17_cen(z["ring"]))
        if at and R[0] + 3.0 <= at[0] <= R[2] - 3.0 and R[1] + 3.0 <= at[1] <= R[3] - 3.0:
            b_ = label_spot(at[0], at[1], 3.8, 3.8, taken, (R[0] + 1.0, R[1] + 1.0, R[2] - 1.0, R[3] - 1.0), (), 0.3,
                            rings=(0.0, 1.5, 3.0, 5.0, 8.0))
            if b_:
                (bx0, by0, bx1, by1), far = b_
                if far:
                    sp.line([at, lp_leader_end(b_[0], at)], COL["ink_dark"], 0.12)
                _p17_badge(sp, n, (bx0 + bx1) / 2.0, (by0 + by1) / 2.0)
                taken.append(b_[0])
                nums.append(n)
    pg.items += _p14_clip_items(sp.items, R)
    pg.poly([rect(*R)], fill=None, stroke=COL["ink2"], lw=0.2)
    # under it: the window's name, the scale bar, "1:den", the north arrow
    yb = R[1] - 4.0
    bb = _p12_bar(pg, R[0], yb, den, P17_BAR.get(den, (0, 20, 50, 100)))
    lab = u"{} · plan · 1:{:,.0f}".format(P17_WIN_NAME[key], den)
    xl = bb[2] + 3.0
    pg.text(lab, xl, yb, P17_FS, COL["ink"], bold=True)
    nd = (T((0.0, 100.0))[0] - T((0.0, 0.0))[0], T((0.0, 100.0))[1] - T((0.0, 0.0))[1])
    nl = math.hypot(*nd) or 1.0
    nb = _p17_north(pg, R[2] - 4.0, yb - 1.0, (nd[0] / nl, nd[1] / nl), 4.0)
    return (min(R[0], bb[0]), min(bb[1], nb[1], yb - 1.5), R[2], R[3]), nums


P17_WIN_NAME = {"A": u"Upstream entry", "B": u"Lower reach"}
P17_CUTS = [("W1", u"F1"), ("F2", u"F2"), ("S4", u"F3"), ("F4", u"F4")]   # the sections of page B: (level cut, name)


def _p17_clip_seg(seg, ring):
    """the parts of the segment seg inside ring (sampled every 1/200 of its length)"""
    (ax, ay), (bx, by) = seg
    out, cur = [], None
    n = 200
    for i in range(n + 1):
        t = i / float(n)
        p = (ax + (bx - ax) * t, ay + (by - ay) * t)
        if _p17_pip(p, ring):
            if cur is None:
                cur = [p, p]
            cur[1] = p
        elif cur is not None:
            out.append(cur)
            cur = None
    if cur is not None:
        out.append(cur)
    return [r for r in out if math.hypot(r[1][0] - r[0][0], r[1][1] - r[0][1]) > 0.5]


def _p17_scatter(sp, Rp, keys, step, k, seed):
    """plants of keys on a jittered grid step mm apart inside the page ring Rp"""
    xs, ys = [p[0] for p in Rp], [p[1] for p in Rp]
    i = 0
    y = min(ys) + step / 2.0
    while y < max(ys):
        x = min(xs) + step / 2.0 * (1 + (i % 2))
        while x < max(xs):
            q = (x + (_p17_rnd(i, seed) - 0.5) * step * 0.4, y + (_p17_rnd(i, seed + 1) - 0.5) * step * 0.4)
            if _p17_pip(q, Rp):
                _p17_plan_plant(sp, keys[i % len(keys)], q[0], q[1], k, seed + i)
            x += step
            i += 1
        y += step


def _p17_offset(P, d):
    """the polyline P (page) moved d mm to its left"""
    out = []
    for i, p in enumerate(P):
        a, b = P[max(i - 1, 0)], P[min(i + 1, len(P) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        out.append((p[0] - dy / L * d, p[1] + dx / L * d))
    return out


def _p17_edge(sp, P, keys, step, k, seed, closed=True):
    """plants of keys every step mm along the page polyline / ring P"""
    pts = list(P) + ([P[0]] if closed else [])
    L = sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(pts[:-1], pts[1:]))
    n = int(L / step)
    for i in range(n):
        (x, y), _ = _p17_along(pts, (i + 0.5) * step)
        _p17_plan_plant(sp, keys[i % len(keys)], x, y, k, seed + i)


def _p17_wetland(sp, ring, T, k, bld):
    """the floodable riverside planting (zone base WP) as bands by distance from the Selinos line: rush and loosestrife
    at the water, willow, tamarisk and chaste tree further out, ash on the dry edge (the section rule of F4)"""
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    i, step = 0, 4.5
    y = min(ys) + step / 2.0
    while y < max(ys):
        x = min(xs) + step / 2.0 * (1 + (i % 2))
        while x < max(xs):
            q = (x + (_p17_rnd(i, 21) - 0.5) * 1.8, y + (_p17_rnd(i, 22) - 0.5) * 1.8)
            if _p17_pip(q, ring) and not any(_p17_pip(q, r) for r in bld):
                d = _p17_line_d(q, P12_SELINOS)
                key = (("soft_rush", "loosestrife")[i % 2] if d < 30.0 else
                       (("willow", "tamarisk", "chaste")[i % 3] if d < 55.0 else "ash"))
                if key in ("willow", "tamarisk", "ash") and i % 2:
                    key = "chaste"
                X, Y = T(q)
                _p17_plan_plant(sp, key, X, Y, k, 300 + i)
            x += step
            i += 1
        y += step


def _p17_win_corners(fit):
    """the four survey corners of a window fitted by _p17_win_fit"""
    w, h, u, v, c, den = fit
    hw, hh = w / 2.0 * den / 1000.0, h / 2.0 * den / 1000.0
    return [((c[0] + a) * u[0] + (c[1] + b) * v[0], (c[0] + a) * u[1] + (c[1] + b) * v[1])
            for a, b in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))]


# ---------------------------------------------------------------- key maps (basemap "topographic", 02 §1)
def _p17_keymap(pg, box, cuts, wins, log):
    """the analysis frame along its long side in box (x0, y0, x1, y1), upstream at the left, the shared basemap in its
    topographic mode, the hubs, and either this page's cut lines ONLY (cuts: [(level cut, name)]) or the plan windows
    (wins: [(name, survey ring)]); a north arrow at its left. Returns its box, or None without basemap data."""
    x0, y0, x1, y1 = box
    fr = basemap_frame()
    fu = _p17_frame_uv()
    if not fr or not fu:
        log.append(u"p.17 key map: no basemap data (run the site board v51+ once)")
        return None
    u, v = fu
    cx, cy = _p17_cen(fr)
    us = [(p[0] - cx) * u[0] + (p[1] - cy) * u[1] for p in fr]
    vs = [(p[0] - cx) * v[0] + (p[1] - cy) * v[1] for p in fr]
    na = 8.0
    den = max((max(us) - min(us)) * 1000.0 / (x1 - x0 - na), (max(vs) - min(vs)) * 1000.0 / (y1 - y0))
    k = 1000.0 / den
    ox, oy = x0 + na - min(us) * k, y1 - max(vs) * k

    def T(p):
        return (ox + ((p[0] - cx) * u[0] + (p[1] - cy) * u[1]) * k, oy + ((p[0] - cx) * v[0] + (p[1] - cy) * v[1]) * k)
    R = (ox + min(us) * k, oy + min(vs) * k, ox + max(us) * k, oy + max(vs) * k)
    sbox = (min(p[0] for p in fr), min(p[1] for p in fr), max(p[0] for p in fr), max(p[1] for p in fr))
    sp = Page(0, 0)

    def text_fn(s, xy, size_mm, hx, bold=False, align="L"):
        sp.text(s, xy[0], xy[1], max(size_mm, FS_MIN), hx, bold=bold, align=(str(align or u"L")[:1]).upper())
    try:
        items = list(basemap_items("topographic", box=sbox, split_buildings=True))
        if cuts:
            items += list(basemap_cut_items([(level_ends(cid)[0], level_ends(cid)[1], (nm, nm + u"'"))
                                             for cid, nm in cuts], den, text_mm=FS_MIN))
        sp.poly([rect(*R)], fill=COL["white"])

        def fill_fn(rings, hx, alpha, nonzero):
            sp.poly([r_ for r_ in rings if len(r_) >= 3], fill=hx if alpha is None or alpha >= 0.999 else
                    r28_mix(hx, "FFFFFF", 1.0 - max(0.0, float(alpha))))

        def line_fn(pts, hx, w_mm, dash_mm, alpha):
            d_ = (list(dash_mm) if isinstance(dash_mm, (list, tuple)) else [dash_mm, dash_mm]) if dash_mm else None
            sp.line(pts, hx if alpha is None or alpha >= 0.999 else r28_mix(hx, "FFFFFF", 1.0 - max(0.0, float(alpha))),
                    w_mm, dash=d_)
        basemap_draw(items, T, fill_fn, line_fn, text_fn)
    except Exception as ex:
        log.append(u"p.17 key map not drawn: {}: {}".format(type(ex).__name__, ex))
        return None
    for name, ring in wins or []:
        P = [T(p) for p in ring]
        sp.poly([P], fill=None, stroke=COL["accent"], lw=0.35)
        xs, ys = [p[0] for p in P], [p[1] for p in P]
        sp.text(name, max(xs) + 0.8, max(ys) - FS_MIN, FS_MIN, COL["accent"], bold=True)
    for name, xy in _p17_hubs(log):
        X, Y = T(xy)
        sp.circle(X, Y, 0.7, fill=COL["ink_dark"])
    pg.items += _p14_clip_items(sp.items, R)
    pg.poly([rect(*R)], fill=None, stroke=COL["ink2"], lw=0.2)
    n_ = (u[1], v[1])
    nl = math.hypot(*n_) or 1.0
    nb = _p17_north(pg, R[0] - na / 2.0, R[3] - 7.0, (n_[0] / nl, n_[1] / nl), 3.5)
    return (min(R[0] - na, nb[0]), R[1], R[2], R[3])


# ---------------------------------------------------------------- page A: legend, numbered list, catalogue
def _p17_legend(pg, x, ytop, w, log):
    """drawn samples with plain names, only what the plans draw; returns the bottom y"""
    fs = P17_FS
    y = ytop
    pg.text(u"ON THE PLANS", x, y - fs, fs, COL["ink_dark"], bold=True)
    y -= fs * 1.9
    rows = [("cell", u"lined basin cell: reed, water mint"), ("WD", u"spillway"), ("GR", u"shaded walk"),
            ("WS", u"rain terraces, olive rows"), ("STRIP", u"summer strip"), ("WP", u"wetland planting"),
            ("ARM", u"side arm"), ("cut", u"section line (p.17 sections)"), ("hub", u"hub")]
    if _p17_shade(log):
        rows += [("shade", lab) for _, _, lab in P17_SHADE]
    for i, (kind, lab) in enumerate(rows):
        yy = y - fs * 0.15
        if kind == "cell":
            _p17_put(pg, pla_cell_plan("reed", (x, yy - 1.0, x + 6.0, yy + 2.2), 2.0, 0.15))
        elif kind == "cut":
            pg.line([(x, yy + 0.6), (x + 6.0, yy + 0.6)], COL["ink_dark"], 0.3, dash=[2.4, 0.7, 0.4, 0.7])
        elif kind == "hub":
            _p17_put(pg, ico_badge("hub", x + 3.0, yy + 0.6, 3.6))
        elif kind == "shade":
            col = [c_ for _, c_, l_ in P17_SHADE if l_ == lab][0]
            pg.poly([rect(x, yy - 1.0, x + 6.0, yy + 2.2)], fill=col, alpha=0.6)
        else:
            f_, s_ = P17_ZONE[kind]
            pg.poly([rect(x, yy - 1.0, x + 6.0, yy + 2.2)], fill=f_, stroke=s_, lw=0.12)
        t = lab if kind != "shade" else u"July shade " + lab
        pg.text(t, x + 7.5, y, fs, COL["ink"])
        y -= fs * 1.55
    y -= 0.6
    y = r28_para(pg, x, y + fs * 0.4, w, u"crowns at **true size** for each species", fs, COL["ink2"])
    return y


def _p17_list(pg, x, ytop, w, nums):
    """the numbered water spaces with what grows there (R35), in two columns; returns the bottom y"""
    fs = P17_FS
    items = [s for s in PLANT_SITES if s[0] in nums]
    cw = (w - 6.0) / 2.0
    half = (len(items) + 1) // 2
    low = ytop
    for col, part in enumerate((items[:half], items[half:])):
        y = ytop
        xx = x + col * (cw + 6.0)
        for n, code, name, keys in part:
            _p17_badge(pg, n, xx + 1.8, y - 1.8)
            s_ = u"**{}**: {}".format(name, u", ".join(PLA_SPECIES[k_]["name"].lower() if i_ else PLA_SPECIES[k_]["name"]
                                                       for i_, k_ in enumerate(keys)))
            y = min(y - 3.8, r28_para(pg, xx + 4.6, y + fs * 0.2, cw - 4.6, s_, fs, COL["ink"]) - 0.6)
        low = min(low, y)
    return low


def _p17_foliage(key):
    t = PLA_SPECIES[key].get("foliage") or u""
    if not t or u"not found" in t or u"UNVERIFIED" in t:
        return None
    return t.split(u" (")[0]


def _p17_height(key):
    lo, hi = PLA_SPECIES[key].get("h_range") or (None, None)
    if hi is None:
        return None
    f = lambda v: (u"{:.0f}".format(v) if abs(v - round(v)) < 1e-9 else u"{:.1f}".format(v))
    if lo is None:
        return u"up to {} m".format(f(hi))
    return u"{}-{} m".format(f(lo), f(hi))


P17_WATER_ICON = {"wet": "water", "moist": "drip", "dry": "drought"}
P17_ROLE_ICON = {"clean": "nutrients", "shade": "shade", "hold the bank": "high_water", "scent": "plants",
                 "flower": "plants", "harvest": "olive"}


def _p17_name(key):
    return plant_name(key) if key in PLANTS else u"{} ({})".format(PLA_SPECIES[key]["name"], PLA_SPECIES[key]["turkish"]) \
        if u"UNVERIFIED" not in PLA_SPECIES[key]["turkish"] else PLA_SPECIES[key]["name"]


def _p17_views(pg, key, x, y, w, h):
    """the species' section silhouette (left) and its top-view crown (right) at ONE size factor, in the box (x, y) -
    (x + w, y + h): the two views of one primitive"""
    half = (w - 1.0) / 2.0
    if key in ("reed", "mint"):
        tall = (PLA_SPECIES[key]["h_m"] or 1.0) + P17_BASIN["depth"] + P17_BASIN["kerb_h"]
        kk = min(h / tall, half / 2.4)
        fl = y + 0.2
        rim = fl + (P17_BASIN["depth"]) * kk
        fn = pla_reed_basin if key == "reed" else pla_mint_cell
        _p17_put(pg, fn(x + 0.4, x + half - 0.4, fl, rim, kk, P17_BASIN["kerb_h"], P17_BASIN["kerb_t"],
                        P17_BASIN["media"]))
        _p17_put(pg, pla_cell_plan(key, (x + half + 1.0, y + h / 2.0 - half / 2.0, x + w, y + h / 2.0 + half / 2.0),
                                   kk, P17_BASIN["kerb_t"]))
        return
    hh, cw = _p17_size(key)
    kk = min(h / hh, half / max(cw, 0.1))
    _p17_put(pg, pla_section(key, x + half / 2.0, y, kk, h_m=hh, crown_m=cw))
    _p17_put(pg, pla_plan(key, x + half + 1.0 + half / 2.0, y + h / 2.0, kk, crown_m=cw))


def _p17_card(pg, x, ytop, w, sp_, photo, photos):
    """one catalogue column (R36): photo, the two views, name with its sources, foliage and height, water, role.
    Returns the bottom y."""
    fs = P17_FS
    key = sp_["key"]
    path, credit = photo
    y = ytop
    pg.poly([rect(x, y - PHOTO_H, x + PHOTO_W, y)], fill=C["paper"], stroke=C["faint"], lw=0.2)
    if path:
        photos.append((x, y - PHOTO_H, x + PHOTO_W, y, path))
    y -= PHOTO_H + 1.2
    _p17_views(pg, key, x, y - 15.0, w, 15.0)
    y -= 16.5
    name = _p17_name(key) + u" " + cite(sp_["src"]) + (cite(credit) if credit else u"")
    y = para(pg, x, y, w, name, fs, COL["ink_dark"], bold=True) - 0.4
    fo, ht = _p17_foliage(key), _p17_height(key)
    t = u" · ".join(s_ for s_ in (fo, ht) if s_)
    if t:
        y = para(pg, x, y, w, t, fs, COL["ink"]) - 0.4
    wc, wt = sp_["water"]
    _p17_put(pg, ico_draw(P17_WATER_ICON[wc], x + 1.5, y - 2.45, 3.0))
    y = min(y - 3.3, para(pg, x + 3.6, y, w - 3.6, wt, fs, COL["ink"]) - 0.4)
    ix = x
    for r_ in sp_["role"]:
        _p17_put(pg, ico_draw(P17_ROLE_ICON.get(r_, "plants"), ix + 1.5, y - 2.45, 3.0))
        ix += 3.4
    y = min(y - 3.3, para(pg, ix + 0.4, y, w - (ix - x) - 0.4, u", ".join(sp_["role"]), fs, COL["river_dark"],
                          bold=True) - 0.4)
    return y


def _p17_catalogue(pg, x0, ybot, x1, log, measure=False):
    """the species, wet to dry, one column each, along the foot of page A; bottom-aligned at ybot. Returns its box."""
    sps = [s_ for k_ in P17_CAT for s_ in SPECIES if s_["key"] == k_]
    n = len(sps)
    gap = max(0.6, min(3.0, (x1 - x0 - n * PHOTO_W) / max(n - 1, 1)))
    w = PHOTO_W
    if "photos" not in _P17_MEMO:
        state = {}
        out = []
        for s_ in sps:
            p_ = (None, None)
            if PHOTO_ON[0] and s_["key"] in PLANTS:
                path, credit, why = plant_photo_of(s_["key"], log, state)
                p_ = (path, credit)
                if not path:
                    log.append(u"p.17 catalogue: no photo of {} ({})".format(s_["key"], why or u"not loaded"))
            elif s_["key"] not in PLANTS:
                log.append(u"p.17 catalogue: {} has no photo entry in common/plant_photos.py PLANTS".format(s_["key"]))
            out.append(p_)
        _P17_MEMO["photos"] = out
    photos = _P17_MEMO["photos"]
    hmax = max(-_p17_card(Page(0, 0), 0.0, 0.0, w, s_, (None, None), []) for s_ in sps)
    if measure:
        return (x0, ybot, x0 + n * w + (n - 1) * gap, ybot + hmax)
    ytop = ybot + hmax
    for i, (s_, p_) in enumerate(zip(sps, photos)):
        _p17_card(pg, x0 + i * (w + gap), ytop, w, s_, p_, PHOTOS)
    return (x0, ybot, x0 + n * w + (n - 1) * gap, ytop)


def p17_page(pg, box, opt, log):
    """page A (wb_plants): the conclusion and the key strip on top, the two plan windows with their legend, the
    numbered water spaces, the species catalogue along the foot. Returns [(crop id, bbox, den)]."""
    if _P17_MEMO.get("run") != id(pg):                  # a new run reads its data afresh
        _P17_MEMO.clear()
        _P17_MEMO["run"] = id(pg)
    x0, y0, x1, y1 = box
    W = min(x1 - x0, P17_W)
    x1 = x0 + W
    n0 = len(pg.items)
    G = 5.0
    LG = 56.0                                           # the legend column, mm
    # the plan windows: one standard scale for both, the first at which they fit beside the legend
    pa, pb = _p17_win_pts("A", log), _p17_win_pts("B", log)
    pick = None
    for den in P17_DENS:
        fa, fb = _p17_win_fit(pa, den), _p17_win_fit(pb, den)
        if fa[0] + fb[0] + 2 * G + LG <= W and max(fa[1], fb[1]) <= 104.0:
            pick = (den, fa, fb)
            break
    if pick is None:
        den = P17_DENS[-1]
        pick = (den, _p17_win_fit(pa, den), _p17_win_fit(pb, den))
        log.append(u"WARNING p.17: the plan windows do not fit at any standard scale; drawn at 1:{:,.0f}".format(den))
    den, fa, fb = pick
    # top row: the key strip (the frame, the two windows, the hubs) and the conclusion
    KH = 22.0
    kb = _p17_keymap(pg, (x0, y1 - KH, x0 + 5.38 * KH + 8.0, y1), None,
                     [(u"A", _p17_win_corners(fa)), (u"B", _p17_win_corners(fb))], log)
    xs = (kb[2] if kb else x0) + 6.0
    yc = r28_para(pg, xs, y1, x1 - xs, P17_SAY, P17_HEAD, COL["ink_dark"])
    ytop = min(y1 - KH, yc) - 6.0
    # the windows, side by side, the legend at the right
    pg.text(u"A", x0, ytop + 1.2, P17_HEAD, COL["accent"], bold=True)
    ba, na = _p17_window(pg, x0, ytop, "A", den, fa, log)
    pg.text(u"B", ba[2] + G, ytop + 1.2, P17_HEAD, COL["accent"], bold=True)
    bb_, nb = _p17_window(pg, ba[2] + G, ytop, "B", den, fb, log)
    ly = _p17_legend(pg, x1 - LG, ytop, LG, log)
    ybot = min(ba[1], bb_[1], ly) - 4.0
    # the numbered water spaces under the windows, the catalogue at the foot
    cb = _p17_catalogue(pg, x0, y0, x1, log, measure=True)
    yl = _p17_list(pg, x0, ybot, x1 - x0, set(na) | set(nb))
    if yl - 4.0 < cb[3]:
        log.append(u"WARNING p.17: the catalogue runs into the list by {:.0f} mm".format(cb[3] - yl + 4.0))
    _p17_catalogue(pg, x0, y0, x1, log)
    log.append(u"p.17 page A: plans 1:{:,.0f} ({} and {}), catalogue {} species, photos {}".format(
        den, u"north up" if fa[2] == (1.0, 0.0) else u"along the frame", u"north up" if fb[2] == (1.0, 0.0) else
        u"along the frame", len(P17_CAT), sum(1 for p_ in _P17_MEMO.get("photos", []) if p_[0])))
    return [("wb_plants", items_bbox(pg.items[n0:]), den)]


# ---------------------------------------------------------------- page B: the sections at 1:500
P17_WALL_T = 0.60                    # DSİ wall thickness drawn (no source; as p.04-05 and p.13 draw it)
P17_F1_BED = (22.1, 54.7)            # F1 on the W1 line: the bed between the walls, m from the SW end (the W1 width,
#                                      placed so the zone base's strip, 24.1-28.9 m on the line, lies in it)
P17_F1_STRIP = (24.1, 28.9)
P17_F2_RANGE = (36.0, 178.0)         # the part of F2 drawn, m along it
P17_F2_WALLS = (44.6, 67.7)          # F2: the bed between the DSİ walls (sample_cut.py: the survey's stream lines)
P17_F2_CELLS = [("reed", 77.9, 83.9), ("reed", 84.4, 90.4), ("mint", 90.9, 96.9)]   # basin cells in the zone WT
P17_F2_TERR = 7.0                    # rain terrace tread, m (the olive row spacing, plants.py PLA_CROPS)
P17_F4_RANGE = (12.0, 140.0)
P17_F4_BED = (73.7, 113.9)           # F4: the bed between the survey's two stream lines, m along the cut
P17_F3_RANGE = (-42.0, 48.0)         # F3 on S4: m across from the bed's low point (p.14's coordinates)
P17_GRAVEL = 0.50


def _p17_gz(prof, t):
    """the ground of a profile [(t, z)] at t (at a vertical step the upper one)"""
    best = None
    for (a, za), (b, zb) in zip(prof[:-1], prof[1:]):
        if b > a and a - 1e-9 <= t <= b + 1e-9:
            z = za + (zb - za) * (t - a) / (b - a)
            best = z if best is None else max(best, z)
    if best is None:
        return prof[0][1] if t < prof[0][0] else prof[-1][1]
    return best


def _p17_wet(prof, z, t0, t1, step=0.25):
    out, a = [], None
    n = int((t1 - t0) / step)
    for i in range(n + 1):
        t = t0 + i * step
        if _p17_gz(prof, t) < z - 1e-6:
            if a is None:
                a = t
        elif a is not None:
            out.append((a, t))
            a = None
    if a is not None:
        out.append((a, t1))
    return out


def _p17_section(spec, log):
    """one section at 1:500 from spec (see the builders), on its own Page: origin = (t0, zb); returns the Page.
    spec: rng, zb, prof [(t, z)], fills [(ring, material)], water [ring], plants [(key, t, seed)], cells [(kind, t0, t1,
    floor, rim)], beyond [(kind, t0, t1, floor, rim)], beyond_plants, people [(pose, t, facing, params)], zones
    [(t0, t1, text, chip colour or None)], levels [(z, text, colour, bold)], qlines [z], arrows [(pts, colour)],
    ends (left, right), caption."""
    k = 1000.0 / P17_SEC_DEN
    t0, t1 = spec["rng"]
    zb = spec["zb"]
    prof = spec["prof"]
    fs = P17_FS

    def X(t):
        return (t - t0) * k

    def Y(z):
        return (z - zb) * k

    def P(pts):
        return [(X(t), Y(z)) for t, z in pts]
    pg = Page(0, 0)
    W = X(t1)
    clip = (0.0, -1e9, W, 1e9)

    def put(ring_tz, mat):
        r_ = _p14_clip_ring(P(ring_tz), clip)
        if r_:
            _p17_put(pg, sct_hatch_fill(r_, mat, k, None, 0.1))
    # what stands beyond the cut, pushed back behind a veil
    if spec.get("beyond") or spec.get("beyond_plants"):
        bp = Page(0, 0)
        for kind, a, b, fl, rim in spec.get("beyond", []):
            fn = pla_reed_basin if kind == "reed" else pla_mint_cell
            _p17_put(bp, fn(X(a), X(b), Y(fl), Y(rim), k, P17_BASIN["kerb_h"], P17_BASIN["kerb_t"], P17_BASIN["media"]))
        for key, t, seed in spec.get("beyond_plants", []):
            _p17_sec_plant(bp, key, X(t), Y(_p17_gz(prof, t)), k, seed, beyond=True)
        pg.items += _p14_clip_items(bp.items, (0.0, Y(spec.get("beyond_z", zb)), W, 1e9))
        bb = items_bbox(bp.items) if bp.items else None
        if bb:
            pg.poly([rect(bb[0], bb[1], bb[2], bb[3])], fill=COL["white"], alpha=0.5)
    put(prof + [(t1, zb), (t0, zb)], "earth")
    for ring, mat in spec.get("fills", []):
        put(ring, mat)
    for ring in spec.get("water", []):
        r_ = _p14_clip_ring(P(ring), clip)
        if r_:
            pg.poly([r_], fill=P17_WATER, alpha=0.85)
            top = max(p[1] for p in r_)
            xs = [p[0] for p in r_ if abs(p[1] - top) < 1e-6]
            if len(xs) >= 2:
                pg.line([(min(xs), top), (max(xs), top)], C["w3"], 0.2)
    pg.line(P(prof), COL["ink_dark"], 0.3)
    for kind, a, b, fl, rim in spec.get("cells", []):
        fn = pla_reed_basin if kind == "reed" else pla_mint_cell
        _p17_put(pg, fn(X(a), X(b), Y(fl), Y(rim), k, P17_BASIN["kerb_h"], P17_BASIN["kerb_t"], P17_BASIN["media"]))
    for pts, colour in spec.get("arrows", []):
        arrow(pg, P(pts), colour, 0.3, 1.6, [0.9, 0.6])
    for key, t, seed in spec.get("plants", []):
        if t0 + 0.3 <= t <= t1 - 0.3:
            _p17_sec_plant(pg, key, X(t), Y(_p17_gz(prof, t)), k, seed)
    for pose, t, face, par in spec.get("people", []):
        if t0 + 0.8 <= t <= t1 - 0.8:
            par = dict(par or {})
            zf = par.pop("z", None)
            _p17_fig(pg, pose, X(t), Y(zf if zf is not None else _p17_gz(prof, t)), k, face, **par)
    for z in spec.get("qlines", []):
        for a, b in _p17_wet(prof, z, t0, t1):
            pg.line([(X(a), Y(z)), (X(b), Y(z))], C["w4"], 0.18, dash=[1.2, 0.7])
    # the zones on vertical lines over the drawing (R34), staggered on two rows where they meet
    top = items_bbox(pg.items)[3] + 3.0
    rows_end = [-1e9, -1e9]
    for a, b, text, chip in spec.get("zones", []):
        a, b = max(a, t0), min(b, t1)
        if b - a < 0.5:
            continue
        xa, xb = X(a), X(b)
        xm = (xa + xb) / 2.0
        cw = (fs * 1.7 + 0.8) if chip else 0.0
        tw = text_w(text, fs, True) + cw
        lx = min(max(xm - tw / 2.0, 0.0), W - tw)
        row = 0 if lx > rows_end[0] + 1.5 else 1
        if row == 1 and lx <= rows_end[1] + 1.5:
            lx = rows_end[1] + 1.5
        rows_end[row] = lx + tw
        yl = top + row * fs * 1.6
        for xv in (xa, xb):
            pg.line([(xv, yl - 0.6), (xv, Y(_p17_gz(prof, (xv / k) + t0)) + 0.4)], COL["ink2"], 0.1, dash=[0.5, 0.5])
        pg.line([(xa, yl - 0.6), (xb, yl - 0.6)], COL["ink2"], 0.12)
        if chip:
            pg.poly([rect(lx, yl - 0.2, lx + fs * 1.7, yl + fs * 0.95)], fill=BAND_COL.get(chip, chip))
            pg.text(chip, lx + fs * 0.85, yl + 0.1, fs, "FFFFFF", bold=True, align="C")
        pg.text(text, lx + cw, yl, fs, COL["ink_dark"], bold=True)
    ytop = top + (2 if rows_end[1] > -1e8 else 1) * fs * 1.6
    l_, r_ = spec.get("ends", (u"", u""))
    pg.text(l_, 0.0, ytop + 0.8, P17_HEAD, COL["ink_dark"], bold=True)
    pg.text(r_, W, ytop + 0.8, P17_HEAD, COL["ink_dark"], bold=True, align="R")
    # the levels at the right
    ent = [(Y(z), t, colr, bold) for z, t, colr, bold in spec.get("levels", [])]
    if ent:
        level_ladder(pg, ent, W + 0.8, W + 4.0, fs, lo=Y(zb))
    # under it: the caption and the scale bar
    yc = -fs * 1.6
    pg.text(spec["caption"], 0.0, yc, fs, COL["ink_dark"], bold=True)
    r28_scale_bar(pg, text_w(spec["caption"], fs, True) + 5.0, yc - 0.3, P17_SEC_DEN, fs, False)
    return pg


def _p17_lv_text(z, what):
    return u"{} {}".format(u_level(z), what)


def _p17_f2(log):
    """F2 across the stream, the spillway, the lined reed basins, the shaded walk and the rain terraces (LEVELS F2)"""
    bed, wt = _p17_lv("F2", "bed"), _p17_lv("F2", "top", "NE")
    q100, q500 = _p17_lv("F2", "q100"), _p17_lv("F2", "q500")
    g = _p17_ground("F2")
    t0, t1 = P17_F2_RANGE
    ws, wn = P17_F2_WALLS
    wtk = P17_WALL_T
    zone = dict((c_, (a_, b_)) for c_, a_, b_ in level_cut("F2").get("zones") or [])
    st0, st1 = zone.get("STRIP", (49.2, 54.0))
    sp0, sp1 = 68.3, zone.get("WD", (54.1, 75.4))[1]
    bt0, bt1 = zone.get("WT", (77.7, 97.1))
    gr0, gr1 = zone.get("GR", (115.6, 135.6))
    te0, te1 = zone.get("WS", (135.6, 177.6))
    gz = lambda t: _p17_interp(g, t)
    zp = round(max(gz(bt0 + i) for i in range(int(bt1 - bt0) + 1)), 2)     # the basin platform
    floor = zp - P17_BASIN["depth"]
    prof = []
    # south-west: the ground held up to the wall top behind the DSİ wall, the survey further out
    t, side = ws - wtk, []
    while t >= t0 - 1e-9:
        side.append((t, wt if gz(t) < wt and all(p[1] == wt for p in side) else gz(t)))
        t -= 2.0
    if side[-1][0] > t0:
        side.append((t0, wt if gz(t0) < wt and all(p[1] == wt for p in side) else gz(t0)))
    prof += side[::-1]
    prof += [(ws - wtk, wt), (ws, wt), (ws, bed), (st0, bed), (st0, bed - STRIP_DEPTH), (st1, bed - STRIP_DEPTH),
             (st1, bed), (wn, bed), (wn, wt), (wn + wtk, wt)]
    # the spillway trough from the basins down to the wall top, then the basin platform and the cells
    prof += [(sp0 + 0.3, wt), (sp0 + 0.3, wt - 0.45), (sp1 - 0.3, wt - 0.30), (sp1 - 0.3, wt), (sp1, wt),
             (bt0 - 0.3, zp), (bt0, zp)]
    cells = []
    for kind, a, b in P17_F2_CELLS:
        prof += [(a, zp), (a, floor + P17_BASIN["media"]), (b, floor + P17_BASIN["media"]), (b, zp)]
        cells.append((kind, a, b, floor, zp))
    prof += [(bt1, zp)]
    t = math.ceil(bt1 + 1.0)
    while t < te0:
        prof.append((t, gz(t)))
        t += 2.0
    # the rain terraces: level treads P17_F2_TERR wide at the mean ground of each, stone retaining walls
    fills, plants, people = [], [], []
    prev = gz(te0)
    prof.append((te0, prev))
    s, i = te0, 0
    while s + P17_F2_TERR <= te1 + 0.1:
        lv = round(sum(gz(s + j * 0.5) for j in range(int(P17_F2_TERR * 2) + 1)) / (int(P17_F2_TERR * 2) + 1), 2)
        prof += [(s, lv), (s + P17_F2_TERR, lv)]
        fills.append(([(s - 0.4, min(prev, lv) - 0.4), (s, min(prev, lv) - 0.4), (s, max(prev, lv)),
                       (s - 0.4, max(prev, lv))], "stone"))
        plants += [("rosemary", s + 0.8, 70 + i), ("lavender", s + 1.7, 80 + i), ("olive", s + 4.2, 90 + i)]
        prev, s, i = lv, s + P17_F2_TERR, i + 1
    prof.append((min(t1, s + 0.6), gz(min(t1, s + 0.6))))
    if prof[-1][0] < t1:
        prof.append((t1, gz(t1)))
    fills += [([(ws - wtk, wt), (ws, wt), (ws, bed - P17_GRAVEL), (ws - wtk, bed - P17_GRAVEL)], "stone"),
              ([(wn, wt), (wn + wtk, wt), (wn + wtk, bed - P17_GRAVEL), (wn, bed - P17_GRAVEL)], "stone"),
              ([(ws, bed), (st0 - 0.15, bed), (st0 - 0.15, bed - P17_GRAVEL), (ws, bed - P17_GRAVEL)], "gravel"),
              ([(st1 + 0.15, bed), (wn, bed), (wn, bed - P17_GRAVEL), (st1 + 0.15, bed - P17_GRAVEL)], "gravel"),
              ([(st0 - 0.15, bed), (st0 - 0.15, bed - STRIP_DEPTH - 0.15), (st1 + 0.15, bed - STRIP_DEPTH - 0.15),
                (st1 + 0.15, bed), (st1, bed), (st1, bed - STRIP_DEPTH), (st0, bed - STRIP_DEPTH), (st0, bed)],
               "concrete"),
              ([(sp0, wt), (sp0 + 0.3, wt), (sp0 + 0.3, wt - 0.45), (sp1 - 0.3, wt - 0.30), (sp1 - 0.3, wt),
                (sp1, wt), (sp1, wt - 0.5), (sp0, wt - 0.65)], "concrete"),
              ([(gr0 + 6.0, gz(gr0 + 6.0)), (gr1 - 6.0, gz(gr1 - 6.0)), (gr1 - 6.0, gz(gr1 - 6.0) - 0.2),
                (gr0 + 6.0, gz(gr0 + 6.0) - 0.2)], "concrete")]
    water = [[(st0, bed - STRIP_DEPTH), (st1, bed - STRIP_DEPTH), (st1, bed), (st0, bed)],
             [(sp0 + 0.3, wt - 0.45), (sp1 - 0.3, wt - 0.30), (sp1 - 0.3, wt - 0.15), (sp0 + 0.3, wt - 0.25)]]
    plants += [("loosestrife", st0 - 0.9, 1), ("soft_rush", st1 + 0.7, 2), ("soft_rush", wn - 0.8, 3)]
    t = bt1 + 2.0
    j = 0
    while t < gr0 - 1.0:
        plants.append(("lavender", t, 30 + j))
        t += 1.2
        j += 1
    plants += [("plane", gr0 + 3.0, 40), ("plane", gr1 - 3.0, 41)]
    people += [("walk", ws - 4.0, 1, None), ("wade", (st0 + st1) / 2.0, -1, {"depth_m": STRIP_DEPTH, "z": bed - STRIP_DEPTH}),
               ("adult_child", (gr0 + gr1) / 2.0 + 1.0, -1, {"child_h": 1.15}),
               ("olive", te0 + P17_F2_TERR * 2 + 5.4, -1, {"branch_h": 1.9})]
    # the spillway falls over the wall into the bed
    arrows = [([(sp0 + 0.2, wt - 0.2), (sp0 - 0.8, wt - 1.6), (sp0 - 1.2, bed + 0.4)], C["w3"])]
    zones = [(t0, ws - wtk, u"SW BANK", None), (ws, wn, u"STREAM BED · summer strip", None),
             (sp0, sp1, u"SPILLWAY", None), (bt0, bt1, u"REED BASINS · lined", None),
             (bt1, gr0, u"DRY BANK", None), (gr0, gr1, u"SHADED WALK", None), (te0, te1, u"RAIN TERRACES", None)]
    levels = [(bed, _p17_lv_text(bed, u"bed"), C["w4"], False), (q100, _p17_lv_text(q100, u"Q100"), C["w4"], False),
              (q500, _p17_lv_text(q500, u"Q500"), C["w4"], True), (wt, _p17_lv_text(wt, u"DSİ wall"), COL["ink"], False),
              (zp, _p17_lv_text(zp, u"basin rim"), COL["ink"], False)]
    return dict(rng=(t0, t1), zb=bed - P17_GRAVEL - 1.0, prof=prof, fills=fills, water=water, plants=plants,
                cells=cells, people=people, qlines=[q100, q500], arrows=arrows, zones=zones, levels=levels,
                ends=(u"F2", u"F2'"), caption=u"F2 · rain terraces, reed basins and the stream at the upstream entry")


def _p17_f4(log):
    """F4 across the side arm, the bank top, the widened bed with its strip and the street (LEVELS F4)"""
    bed = _p17_lv("F4", "bed")
    q100, q500 = _p17_lv("F4", "q100"), _p17_lv("F4", "q500")
    g = _p17_ground("F4")
    gz = lambda t: _p17_interp(g, t)
    t0, t1 = P17_F4_RANGE
    zone = dict((c_, (a_, b_)) for c_, a_, b_ in level_cut("F4").get("zones") or [])
    a0, a1 = zone.get("ARM", (27.0, 33.0))
    b0, b1 = P17_F4_BED
    st0, st1 = 86.7, 90.9                                # the zone base's strip on F4 (ZONE_COPY A-NIL-STRIP-2)
    zf = gz((a0 + a1) / 2.0) - 0.80                      # the side arm's floor: a 0.80 m channel (drawing value)
    zs = gz((st0 + st1) / 2.0)
    prof = []
    t = t0
    while t < a0:
        prof.append((t, gz(t)))
        t += 2.0
    prof += [(a0, gz(a0)), (a0 + 0.8, zf), (a1 - 0.8, zf), (a1, gz(a1))]
    t = math.ceil(a1 + 1.0)
    while t < st0:
        prof.append((t, gz(t)))
        t += 2.0
    prof += [(st0, zs), (st0, zs - STRIP_DEPTH), (st1, zs - STRIP_DEPTH), (st1, zs)]
    t = math.ceil(st1 + 1.0)
    while t < t1:
        prof.append((t, gz(t)))
        t += 2.0
    prof.append((t1, gz(t1)))
    fills = [([(b0, gz(b0)), (st0 - 0.15, zs), (st0 - 0.15, zs - P17_GRAVEL), (b0, gz(b0) - P17_GRAVEL)], "gravel"),
             ([(st1 + 0.15, zs), (b1, gz(b1)), (b1, gz(b1) - P17_GRAVEL), (st1 + 0.15, zs - P17_GRAVEL)], "gravel"),
             ([(st0 - 0.15, zs), (st0 - 0.15, zs - STRIP_DEPTH - 0.15), (st1 + 0.15, zs - STRIP_DEPTH - 0.15),
               (st1 + 0.15, zs), (st1, zs), (st1, zs - STRIP_DEPTH), (st0, zs - STRIP_DEPTH), (st0, zs)], "concrete"),
             ([(126.6, gz(126.6)), (132.0, gz(132.0)), (132.0, gz(132.0) - 0.3), (126.6, gz(126.6) - 0.3)], "concrete")]
    water = [[(st0, zs - STRIP_DEPTH), (st1, zs - STRIP_DEPTH), (st1, zs), (st0, zs)],
             [(a0 + 0.8 * 0.6, zf + 0.3), (a0 + 0.8, zf), (a1 - 0.8, zf), (a1 - 0.8 * 0.6, zf + 0.3)]]
    plants = [(key, t, 500 + i) for i, (key, t) in enumerate(P17_F4_PLANTS)]
    people = [("walk", 19.0, 1, None), ("watch", a1 + 1.6, -1, None),
              ("wade", (st0 + st1) / 2.0, 1, {"depth_m": STRIP_DEPTH, "z": zs - STRIP_DEPTH}),
              ("bike", 129.0, -1, None)]
    zones = [(t0, a0 - 1.0, u"OPEN GROUND", None), (a0 - 1.0, a1 + 1.0, u"SIDE ARM", None),
             (a1 + 1.0, 59.0, u"BANK TOP", None), (59.0, b0, u"SW BANK", None), (b0, b1, u"WIDENED BED · strip", None),
             (b1, 126.6, u"NE BANK", None), (126.6, t1, u"STREET", None)]
    levels = [(bed, _p17_lv_text(bed, u"bed"), C["w4"], False), (q100, _p17_lv_text(q100, u"Q100"), C["w4"], False),
              (q500, _p17_lv_text(q500, u"Q500"), C["w4"], True)]
    return dict(rng=(t0, t1), zb=bed - P17_GRAVEL - 1.0, prof=prof, fills=fills, water=water, plants=plants,
                people=people, qlines=[q100, q500], zones=zones, levels=levels, ends=(u"F4", u"F4'"),
                caption=u"F4 · the side arm and the widened stream, lower reach")


def _p17_f1(log):
    """F1 on the W1 line: the walled stream at the inflow, its strip with rush edges, the reed basins beyond"""
    bed, wt = _p17_lv("W1", "bed"), _p17_lv("W1", "top", "NE")
    q100, q500 = _p17_lv("W1", "q100"), _p17_lv("W1", "q500")
    L = _p17_lv("W1", "length_m")
    t0, t1 = 0.0, L
    ws, wn = P17_F1_BED
    st0, st1 = P17_F1_STRIP
    wtk = P17_WALL_T
    prof = [(t0, wt), (ws - wtk, wt), (ws, wt), (ws, bed), (st0, bed), (st0, bed - STRIP_DEPTH),
            (st1, bed - STRIP_DEPTH), (st1, bed), (wn, bed), (wn, wt), (wn + wtk, wt), (t1, wt)]
    fills = [([(ws - wtk, wt), (ws, wt), (ws, bed - P17_GRAVEL), (ws - wtk, bed - P17_GRAVEL)], "stone"),
             ([(wn, wt), (wn + wtk, wt), (wn + wtk, bed - P17_GRAVEL), (wn, bed - P17_GRAVEL)], "stone"),
             ([(st1 + 0.15, bed), (wn, bed), (wn, bed - P17_GRAVEL), (st1 + 0.15, bed - P17_GRAVEL)], "gravel"),
             ([(ws, bed), (st0 - 0.15, bed), (st0 - 0.15, bed - P17_GRAVEL), (ws, bed - P17_GRAVEL)], "gravel"),
             ([(st0 - 0.15, bed), (st0 - 0.15, bed - STRIP_DEPTH - 0.15), (st1 + 0.15, bed - STRIP_DEPTH - 0.15),
               (st1 + 0.15, bed), (st1, bed), (st1, bed - STRIP_DEPTH), (st0, bed - STRIP_DEPTH), (st0, bed)],
              "concrete")]
    water = [[(st0, bed - STRIP_DEPTH), (st1, bed - STRIP_DEPTH), (st1, bed), (st0, bed)]]
    plants = [(key, t, 600 + i) for i, (key, t) in enumerate(P17_F1_PLANTS)]
    bx0 = wn + wtk + 1.2
    beyond = [("reed", bx0, bx0 + 5.6, wt - P17_BASIN["depth"], wt),
              ("mint", bx0 + 6.2, min(t1 - 0.5, bx0 + 11.0), wt - P17_BASIN["depth"], wt)]
    people = [("walk", 11.0, 1, None), ("watch", wn + wtk + 0.6, -1, None)]
    arrows = [([((ws + wn) / 2.0 + 6.0, bed + 0.5), (wn - 1.0, wt - 0.6), (bx0 + 1.0, wt + 0.9)], C["w3"])]
    zones = [(t0, ws - wtk, u"SW BANK · plane shade", None), (ws, wn, u"STREAM BED · strip", None),
             (wn + wtk, t1, u"REED BASINS beyond", None)]
    levels = [(bed, _p17_lv_text(bed, u"bed"), C["w4"], False), (q100, _p17_lv_text(q100, u"Q100"), C["w4"], False),
              (q500, _p17_lv_text(q500, u"Q500"), C["w4"], True), (wt, _p17_lv_text(wt, u"DSİ wall"), COL["ink"], False)]
    return dict(rng=(t0, t1), zb=bed - P17_GRAVEL - 1.0, prof=prof, fills=fills, water=water, plants=plants,
                beyond=beyond, beyond_z=wt, people=people, qlines=[q100, q500], arrows=arrows, zones=zones, levels=levels,
                ends=(u"F1", u"F1'"), caption=u"F1 · the stream at the inflow, the reed basins beyond")


def _p17_f3(log):
    """F3 on the S4 line (p.14's own cut and planting, _p14_geo / P14_PLANTS): the planting bands by the days water
    covers the ground (PLANT_BANDS, RWS), both banks, in full leaf"""
    G = _p14_geo()
    t0, t1 = P17_F3_RANGE
    prof = [(t0, _p14_surf(t0))] + [p for p in G["prof"] if t0 < p[0] < t1] + [(t1, _p14_surf(t1))]
    bed, sfl, shelf, zn = G["bed"], G["sfl"], G["shelf"], G["zones"]
    st0, st1 = zn["strip"]
    lt = P14_LINER
    e0, p0 = zn["steps"]
    p2 = zn["bike"][1]
    w0, w1 = P14_WALK
    tt0, tt1 = zn["terrace"]
    fills = [([(G["b0"], bed), (st0 - lt, bed), (st0 - lt, bed - P14_GRAVEL), (G["b0"], bed - P14_GRAVEL)], "gravel"),
             ([(st1 + lt, bed), (G["b1"], bed), (G["b1"], bed - P14_GRAVEL), (st1 + lt, bed - P14_GRAVEL)], "gravel"),
             ([(tt0, shelf), (tt1, shelf), (tt1, shelf - 0.3), (tt0, shelf - 0.3)], "gravel"),
             ([(st0 - lt, bed), (st0 - lt, sfl - lt), (st1 + lt, sfl - lt), (st1 + lt, bed), (st1, bed), (st1, sfl),
               (st0, sfl), (st0, bed)], "concrete"),
             ([(w0, shelf), (w1, shelf), (w1, shelf - 0.2), (w0, shelf - 0.2)], "concrete"),
             ([p for p in G["prof"] if e0 - 1e-9 <= p[0] <= p0 + 1e-9 and p[1] >= shelf - 1e-9] +
              [(p0, P14_PROM - 0.35), (e0, shelf - 0.35)], "concrete"),
             ([(p0, P14_PROM), (p2, P14_PROM), (p2, P14_PROM - P14_SLAB), (p0, P14_PROM - P14_SLAB)], "concrete")]
    water = [[(st0, sfl), (st1, sfl), (st1, bed), (st0, bed)]]
    plants = [(key, s, 700 + i) for i, (key, s, h, cw) in enumerate(P14_PLANTS)]
    people = [("wade", (st0 + st1) / 2.0, 1, {"depth_m": bed - sfl, "z": sfl}),
              ("sit_step", e0 + 3 * P14_STEPS[1] + 0.3, -1, {"seat_h": G["rise"]}), ("walk", (p0 + zn["prom"][1]) / 2.0,
                                                                                    1, None)]
    # the bands: the ground's band code every 0.25 m, merged into runs; each run named on the vertical lines
    runs = []
    s = t0
    while s <= t1 + 1e-9:
        c_ = _p14_band_code(s, _p14_surf(s))
        if runs and runs[-1][0] == c_:
            runs[-1][2] = s
        else:
            runs.append([c_, s, s])
        s += 0.25
    bn = dict((b_[0], (b_[1], b_[3])) for b_ in PLANT_BANDS)
    zones, seen = [], set()
    for c_, a, b in runs:
        if b - a < 3.0:
            continue
        name, days = bn.get(c_, (u"", u""))
        lab = (name.split(u" (")[0].split(u" / ")[0].lower() if c_ not in seen else u"") + \
            (u" · " + days.replace(u" d/yr", u" d").replace(u"–", u"-").split(u";")[0] if c_ not in seen else u"")
        zones.append((a, b + 0.25, lab.strip(u" ·"), c_))
        seen.add(c_)
    levels = [(bed, _p17_lv_text(bed, u"bed"), C["w4"], False),
              (G["q100"], _p17_lv_text(G["q100"], u"Q100"), C["w4"], False),
              (G["q500"], _p17_lv_text(G["q500"], u"Q500"), C["w4"], True),
              (P14_PROM, _p17_lv_text(P14_PROM, u"promenade"), COL["ink"], False)]
    return dict(rng=(t0, t1), zb=G["base"], prof=prof, fills=fills, water=water, plants=plants, people=people,
                qlines=[G["q100"], G["q500"]], zones=zones, levels=levels, ends=(u"F3", u"F3'"),
                caption=u"F3 · the planting bands of the widened stream " + cite(P15_BAND_SRC))


# ---------------------------------------------------------------- page B: the calendar, giant reed, the page
P17_LEAF = "C9D7A6"                  # in leaf
P17_MONTHS = u"JFMAMJJASOND"


def _p17_calendar(pg, x, ytop, w, log):
    """the species of the catalogue on ONE month axis (R36): a bar where it is in leaf, a darker one where it flowers,
    a tick where its flower heads are cut; sourced months only (plants.py pla_months). Returns the bottom y."""
    fs = P17_FS
    lw_ = max(text_w(PLA_SPECIES[k_]["name"], fs) for k_ in P17_CAT) + 1.5
    cw = (w - lw_) / 12.0
    rh = fs * 1.3
    pg.text(u"THE YEAR OF EACH SPECIES", x, ytop - P17_HEAD, P17_HEAD, COL["ink_dark"], bold=True)
    y = ytop - P17_HEAD - 2.0
    for m in range(12):
        pg.text(P17_MONTHS[m], x + lw_ + (m + 0.5) * cw, y - fs, fs, COL["ink2"], bold=True, align="C")
    y -= fs * 1.5
    y0 = y
    for i, key in enumerate(P17_CAT):
        mo = pla_months(key)
        yy = y - i * rh
        pg.text(PLA_SPECIES[key]["name"], x, yy - rh + fs * 0.35, fs, COL["ink"])
        for m in mo.get("leaf") or []:
            pg.poly([rect(x + lw_ + (m - 1) * cw, yy - rh + 0.25, x + lw_ + m * cw, yy - 0.25)], fill=P17_LEAF)
        for m in mo.get("bloom") or []:
            pg.poly([rect(x + lw_ + (m - 1) * cw + 0.2, yy - rh * 0.72, x + lw_ + m * cw - 0.2, yy - rh * 0.28)],
                    fill=P14_BLOOM)
        for m in mo.get("cut") or []:
            xm = x + lw_ + (m - 0.5) * cw
            pg.line([(xm - 0.9, yy - rh + 0.4), (xm + 0.9, yy - 0.4)], COL["accent"], 0.3)
            pg.line([(xm - 0.9, yy - 0.4), (xm + 0.9, yy - rh + 0.4)], COL["accent"], 0.3)
    yb = y - len(P17_CAT) * rh
    for m in range(13):
        pg.line([(x + lw_ + m * cw, y0 + 0.4), (x + lw_ + m * cw, yb)], COL["faint"], 0.08)
    y = yb - fs * 1.5
    xx = x
    for kind, lab in (("leaf", u"in leaf"), ("bloom", u"in flower"), ("cut", u"flower heads cut")):
        if kind == "leaf":
            pg.poly([rect(xx, y - 0.3, xx + 4.0, y + fs * 0.8)], fill=P17_LEAF)
        elif kind == "bloom":
            pg.poly([rect(xx, y + 0.1, xx + 4.0, y + fs * 0.5)], fill=P14_BLOOM)
        else:
            pg.line([(xx + 1.1, y - 0.2), (xx + 2.9, y + fs * 0.8)], COL["accent"], 0.3)
            pg.line([(xx + 1.1, y + fs * 0.8), (xx + 2.9, y - 0.2)], COL["accent"], 0.3)
        pg.text(lab, xx + 5.0, y, fs, COL["ink"])
        xx += 5.0 + text_w(lab, fs) + 4.0
    return y - fs * 0.6


def _p17_remove(pg, x, ytop, w, log):
    """giant reed: its photo crossed, take it out and why (02 §5: only marked remove). Returns the bottom y."""
    fs = P17_FS
    key, words, src = SPECIES_REMOVE
    path, credit = None, None
    if PHOTO_ON[0] and key in PLANTS:
        path, credit, why = plant_photo_of(key, log, {})
    pg.poly([rect(x, ytop - PHOTO_H, x + PHOTO_W, ytop)], fill=C["paper"], stroke=C["faint"], lw=0.2)
    if path:
        PHOTOS.append((x, ytop - PHOTO_H, x + PHOTO_W, ytop, path))
    _p17_put(pg, ico_cross(x + PHOTO_W - 3.5, ytop - 3.5, 5.0, COL["accent"]))
    tx = x + PHOTO_W + 2.0
    y = para(pg, tx, ytop, w - PHOTO_W - 2.0, _p17_name(key) + u" " + cite(src) + (cite(credit) if credit else u""),
             fs, COL["ink_dark"], bold=True)
    y = r28_para(pg, tx, y - 0.4, w - PHOTO_W - 2.0, words, fs, COL["accent"])
    return min(y, ytop - PHOTO_H)


def _p17_place(pg, part, x, ytop):
    """a section Page put with its top-left at (x, ytop), at 1:1 (its scale is its own); returns its box"""
    b = items_bbox(part.items)
    dx, dy = x - b[0], ytop - b[3]
    pg.items += xform(part.items, 1.0, dx, dy)
    return (x, ytop - (b[3] - b[1]), x + b[2] - b[0], ytop)


def p17b_page(pg, box, opt, log):
    """page B (wb_plants_b): the conclusion and the key map (F1-F4 only) on top; F2 with giant reed beside it; F4 with
    the calendar beside it; F1 and F3 side by side. Every section at 1:500. Returns [(crop id, bbox, den)]."""
    if _P17_MEMO.get("run") != id(pg):                  # a new run reads its data afresh
        _P17_MEMO.clear()
        _P17_MEMO["run"] = id(pg)
    x0, y0, x1, y1 = box
    W = min(x1 - x0, P17_W)
    x1 = x0 + W
    n0 = len(pg.items)
    G = 5.0
    parts = {}
    for nm, fn in (("F2", _p17_f2), ("F4", _p17_f4), ("F1", _p17_f1), ("F3", _p17_f3)):
        try:
            parts[nm] = _p17_section(fn(log), log)
        except Exception as ex:
            log.append(u"WARNING p.17 section {} not drawn: {}: {}".format(nm, type(ex).__name__, ex))
            import traceback as _tb
            log.append(_tb.format_exc()[-600:])
    size = dict((nm, items_bbox(p_.items)) for nm, p_ in parts.items())
    wh = dict((nm, (b[2] - b[0], b[3] - b[1])) for nm, b in size.items())
    # top: the conclusion, the key map with this page's cuts only
    KW = 120.0
    kb = _p17_keymap(pg, (x1 - KW, y1 - KW / 5.38, x1, y1), P17_CUTS, None, log)
    yc = r28_para(pg, x0, y1, (kb[0] if kb else x1) - x0 - G, P17B_SAY, P17_HEAD, COL["ink_dark"])
    y = min(yc, kb[1] if kb else y1) - 5.0
    # row 1: F2, giant reed at its right
    if "F2" in parts:
        b2 = _p17_place(pg, parts["F2"], x0, y)
        yr = _p17_remove(pg, b2[2] + G, y, x1 - b2[2] - G, log)
        y = min(b2[1], yr) - 5.0
    # row 2: F4, the calendar at its right
    if "F4" in parts:
        b4 = _p17_place(pg, parts["F4"], x0, y)
        xcal = b4[2] + G
    else:
        b4, xcal = (x0, y, x0, y), x0
    yk = _p17_calendar(pg, xcal, y, x1 - xcal, log)
    y = min(b4[1], yk) - 5.0
    # row 3: F1 and F3 side by side, the room between them shared
    w1 = wh.get("F1", (0.0, 0.0))[0]
    w3 = wh.get("F3", (0.0, 0.0))[0]
    gap = max(G, W - w1 - w3)
    low = y
    if "F1" in parts:
        low = min(low, _p17_place(pg, parts["F1"], x0, y)[1])
    if "F3" in parts:
        low = min(low, _p17_place(pg, parts["F3"], x0 + w1 + gap if w1 else x0, y)[1])
    if low < y0 or w1 + w3 + G > W:
        log.append(u"WARNING p.17 page B: {:.0f} x {:.0f} mm, more than the {:.0f} x {:.0f} mm of the box".format(
            max(W, w1 + w3 + G), y1 - low, W, y1 - y0))
    log.append(u"p.17 page B: sections {} at 1:{:,.0f}".format(u", ".join(sorted(parts)), P17_SEC_DEN))
    return [("wb_plants_b", items_bbox(pg.items[n0:]), P17_SEC_DEN)]
# p.18 the farms and the decision (split from code.py on 29 Oct 2026)
# T4a (WO-T4a-3, 29 Oct): every pictogram from icons.py (02 §2, R19 quality bar), the 1-7 flow on ico_step markers,
# the farm block redrawn per 02 §4 (plants.py rows at the published olive spacing), people through _p18_fig only.

P18_TILE_ICONS = {"out": ("stream_out", "field"), "olive": ("olive",), "plant": ("treatment",), "drought": ("chart",),
                  "nodrink": ("not_drinkable",)}
P18_DEC_ICONS = [("sewage", True), ("reeds", False), ("uv", False), ("storage", False), ("stream", False),
                 ("field", False), ("not_drinkable", False)]     # (icon, crossed) for steps 1-7
P18_INTERNAL = re.compile(u"\\s*\\((?:D\\d+|[A-Z]{2}-[A-Z]?\\d+)\\)")   # register / decision codes, never printed (D13)
P18_OLIVE_ROW_M, P18_OLIVE_TREE_M = 7.0, 5.0     # plants.py: olive 5 x 7 m (Kaya 2017 p.821), 7 m between the rows
P18_BLOCK = (8, 10)                              # rows, trees per row: one 56 x 50 m block
P18_SOIL_M = 2.0                                 # soil shown under the field, graphic only
P18_BRANCH_M = 1.90                              # the branch the picker reaches (figures.py "olive" pose)


def _p18_put(pg, shapes):
    """icons.py / plants.py shapes onto the page (the core's sec_put)"""
    sec_put(pg, shapes)


def _p18_clean(t):
    return P18_INTERNAL.sub(u"", t)


def _p18_icon(pg, names, x, y, sz, cross=False):
    """icons.py pictogram(s) in the square (x, y - sz)-(x + sz, y): one icon fills it; a pair (the clean stream
    leaving + the field it goes to) sits on the square's diagonal, the water upper left, the field lower right"""
    if len(names) == 1:
        _p18_put(pg, ico_draw(names[0], x + sz / 2.0, y - sz / 2.0, sz))
    else:
        h = sz * 0.58
        _p18_put(pg, ico_draw(names[0], x + h / 2.0, y - h / 2.0, h))
        _p18_put(pg, ico_draw(names[1], x + sz - h / 2.0, y - sz + h / 2.0, h))
    if cross:
        _p18_put(pg, ico_cross(x + sz / 2.0, y - sz / 2.0, sz))


def _p18_tiles(pg, x, y, w, items, s, cols=2):
    """p.18's fact tiles (the core's tiles() layout) with icons.py pictograms: items = [(tile key, heading, figure or
    None, line, source)]; the source prints only its public part (cite). Returns the bottom y."""
    fh, fb, ft = 2.5 * s, 4.4 * s, 2.15 * s
    ic, pad, g = 10.0 * s, 2.2 * s, 2.4 * s
    tw = (w - (cols - 1) * g) / cols
    txw = tw - ic - 3 * pad
    lay = []
    for kind, head, big, line, src in items:
        c_ = cite(src) if src else u""
        L = (wrap(head, fh, txw, True), wrap(big, fb, txw, True) if big else [],
             wrap(_p18_clean(line) + (u" " + c_ if c_ else u""), ft, txw))
        hh = pad * 2 + len(L[0]) * fh * 1.25 + len(L[1]) * fb * 1.18 + len(L[2]) * ft * 1.28 + (fh * 0.3 if L[1] else 0)
        lay.append((kind, L, max(hh, ic + 2 * pad)))
    yy = y
    for r0 in range(0, len(lay), cols):
        row = lay[r0:r0 + cols]
        rh = max(t[2] for t in row)
        for c_, (kind, L, _) in enumerate(row):
            tx = x + c_ * (tw + g)
            pg.poly([rect(tx, yy - rh, tx + tw, yy)], fill=C["paper"], stroke=C["faint"], lw=0.2)
            _p18_icon(pg, P18_TILE_ICONS.get(kind, ("water",)), tx + pad, yy - pad, ic)
            lx, ly = tx + 2 * pad + ic, yy - pad
            for ln in L[0]:
                ly -= fh * 1.25
                pg.text(ln, lx, ly, fh, C["dark"], bold=True)
            if L[1]:
                ly -= fh * 0.3
            for ln in L[1]:
                ly -= fb * 1.18
                pg.text(ln, lx, ly, fb, C["d3"], bold=True)
            for ln in L[2]:
                ly -= ft * 1.28
                pg.text(ln, lx, ly, ft, C["ink"])
        yy -= rh + g
    return yy + g


def draw_farms_text(pg, x, y, w, h, s):
    fs = 2.6 * s
    lab_w = text_w(u"Groundwater potential", fs) + 4.0
    gx, top = x + 10.0 + lab_w, y - 4.0
    gw = w - 20.0 - lab_w - text_w(u"198.01 hm³ a year", fs, True) - 4.0
    bh = 3.6 * s
    for r, (lab, v) in enumerate(AQUIFER):
        yy = top - r * (bh + 2.4 * s)
        pg.text(lab, gx - 2.0, yy - bh * 0.5 - fs * 0.35, fs, C["ink"], align="R")
        pg.poly([rect(gx, yy - bh, gx + gw * v / 200.0, yy)], fill=C["w3"] if r == 0 else C["agri"])
        t, bw_ = u"{} hm³ a year".format(v), gw * v / 200.0
        if text_w(t, fs, True) + 3.0 <= bw_:          # v3.1 (Aras 27 Oct, Prompt 6): the value on its bar, at its end
            pg.text(t, gx + bw_ - 1.5, yy - bh * 0.5 - fs * 0.35, fs, C["white"], bold=True, align="R")
        else:
            pg.text(t, gx + bw_ + 2.0, yy - bh * 0.5 - fs * 0.35, fs, C["ink"], bold=True)
    yy = figs(pg, x + 10.0, top - 2 * (bh + 2.4 * s) - 1.0, [(u"use = {:.1f} x potential".format(198.01 / 45.4),
              u"Lower Bakırçay · farm water eases the aquifer " + cite(u"published, North Aegean drought management "
              u"plan 2018 (official); " + WD))], w - 20.0, 4.0 * s, 2.6 * s, C["acc"]) - 2.8 * s * 0.8
    # v6.1: "ratio calculated" taken out of the source above (no status words)
    return _p18_tiles(pg, x + 10.0, yy, w - 20.0, GOES_T, s, 2)


def draw_decision(pg, x, y, w, h, s):
    """v1.12 (Aras 26 Oct 07:06 and his sketch): the seven steps clockwise round a rectangle, 1-4 along the top, 5-7
    back along the bottom; the closing arrow (7 -> 1) in red says what really closes the loop: the next winter's
    stream, never a pump (the water runs one way). Returns the lowest y drawn."""
    steps = [(_p18_clean(t), _p18_clean(src)) for t, src in DECISION]
    n = len(steps)
    top_n = (n + 1) // 2
    gap, vg = 16.0 * s, 24.0 * s
    bw = (w - (top_n - 1) * gap) / top_n
    bh = 0.0
    for t, src in steps:                             # one height for every box: the tallest content
        bh = max(bh, 9.0 * s + len(wrap(t, 3.2 * s, bw - 8.0, True)) * 3.2 * s * 1.28 +
                 len(wrap(src, 2.5 * s, bw - 8.0)) * 2.5 * s * 1.28 + 3.0)
    yt = y                                           # top row: its boxes' top edge
    yb = y - bh - vg                                 # bottom row
    bot_x = [x + w - bw - (w - bw) * j / (n - top_n - 1) for j in range(n - top_n)] if n - top_n > 1 else [x]
    pos = [(x + i * (bw + gap), yt) for i in range(top_n)] + [(bot_x[j], yb) for j in range(n - top_n)]
    for i, (t, src) in enumerate(steps):
        bx, by = pos[i]
        pg.poly([rect(bx, by - bh, bx + bw, by)], fill=C["white"], stroke=C["d2"], lw=0.4)
        sz = 5.6 * s                                 # the step marker (icons.py ico_step), its number written in it
        sh, (ax, ay), th, cap = ico_step(bx + 3.0 + sz / 2.0, by - 1.6 - sz / 2.0, sz, "solid")
        _p18_put(pg, sh)
        pg.text(str(i + 1), ax, ay - cap / 2.0, cap / CAP, th, bold=True, align="C")
        nm, crossed = P18_DEC_ICONS[i] if i < len(P18_DEC_ICONS) else ("water", False)
        _p18_icon(pg, (nm,), bx + bw - 3.0 - 7.0 * s, by - 1.5, 7.0 * s, crossed)
        yy = para(pg, bx + 4.0, by - 8.5 * s, bw - 8.0, t, 3.2 * s, C["dark"], bold=True)
        para(pg, bx + 4.0, yy - 0.6, bw - 8.0, src, 2.5 * s, C["ink"])
    ym = yt - bh / 2.0
    for i in range(top_n - 1):                       # along the top, left to right
        hand_arrow(pg, [(pos[i][0] + bw + 2.0, ym), (pos[i + 1][0] - 2.0, ym)], small=0.7)
    xr = pos[top_n - 1][0] + bw / 2.0                # down the right side
    hand_arrow(pg, [(xr, yt - bh - 2.0), (xr, yb + 2.0)], small=0.7)
    ymb = yb - bh / 2.0
    for j in range(top_n, n - 1):                    # back along the bottom, right to left
        hand_arrow(pg, [(pos[j][0] - 2.0, ymb), (pos[j + 1][0] + bw + 2.0, ymb)], small=0.7)
    xl = pos[0][0] + bw / 2.0                        # the red closing arrow, up the left side
    hand_arrow(pg, [(xl, yb + 2.0), (xl, yt - bh - 2.0)], small=0.7, cols=(C["acc"], C["acc"]))
    para(pg, xl + 6.0, yt - bh - vg / 2.0 + 2.6 * s * 1.28, w * 0.42, LOOP_BACK, 2.6 * s, C["acc"], bold=True)
    pg.text(u"ONE WAY, WITH THE STREAM", x + w * 0.72, yt - bh - vg / 2.0 - 1.2 * s, 3.2 * s, C["d3"], bold=True,
            align="C")
    return yb - bh


def _p18_fig(pg, pose, x, y, k, colour, facing=1, h_m=1.70, **params):
    """ONE place for p.18's people: the figure library (common/figures.py fig_side), feet at (x, y), k mm per m,
    in one ink; params go to the drawn pose (olive: branch_h)"""
    _p18_put(pg, fig_side(pose, x, y, k, facing, ink=colour, mm_per_m=k, h_m=h_m, **params))


def _p18_olive_spots(shapes, crown_cols):
    """the tree centres pla_crop_plan drew (the centroids of its olive crowns, merged within 1 m), so the standing
    trees sit exactly on the plan's rows"""
    pts = []
    for sh in shapes:
        if sh[0] == "poly" and sh[2] in crown_cols and len(sh[1]) > 2:
            cx = sum(p[0] for p in sh[1]) / float(len(sh[1]))
            cy = sum(p[1] for p in sh[1]) / float(len(sh[1]))
            if all(math.hypot(cx - a, cy - b) > 1.0 for a, b in pts):
                pts.append((cx, cy))
    return pts


def _p18_gap(vals):
    q = sorted(set(round(v * 2.0) / 2.0 for v in vals))
    return min([q[i + 1] - q[i] for i in range(len(q) - 1)] or [0.0])


def draw_farm_picto(opt):
    """p.18 farm block (02 §4): the existing olive grove off the site as an axonometric in true proportion. The field,
    its rows and the crowns come from plants.py pla_crop_plan at the published olive spacing (5 m in the row, 7 m
    between rows); the crowns lie on the ground as their midday shade and every tree stands on its spot as its plants.py
    section silhouette at true size; a drip line runs along every row from a header fed by the clean stream water; one
    person picks at true height. A diagram (no scale bar): place() fits it to the panel."""
    pg = Page(0, 0)
    k = 1.2
    V = BoxView(PSI, 0.0, k, 0.0, 0.0)
    nr, nt = P18_BLOCK
    a, b = nt * P18_OLIVE_TREE_M, nr * P18_OLIVE_ROW_M
    sides = [((0, -1), (0, 0), (1, 0)), ((1, 0), (1, 0), (1, 1)), ((0, 1), (1, 1), (0, 1)), ((-1, 0), (0, 1), (0, 0))]
    for (nu, nv), (i0, j0), (i1, j1) in sides:
        vis, lit = V.visible(nu, nv)
        if vis:
            pg.poly([[V(i0 * a, j0 * b, 0), V(i1 * a, j1 * b, 0), V(i1 * a, j1 * b, -P18_SOIL_M),
                      V(i0 * a, j0 * b, -P18_SOIL_M)]], fill=COL["soil"] if lit else COL["soil_dk"],
                    stroke=COL["edge3d"], lw=0.15)
    pg.poly([[V(0, 0, 0), V(a, 0, 0), V(a, b, 0), V(0, b, 0)]], fill=MP["agriculture"][0], stroke=COL["edge3d"], lw=0.15)
    # the field from plants.py, in metres (k = 1), laid on the axonometric ground
    plan = pla_crop_plan("olive", [(0.0, 0.0), (a, 0.0), (a, b), (0.0, b)], 1.0, row_spacing=P18_OLIVE_ROW_M,
                         plant_spacing=P18_OLIVE_TREE_M)
    sp = PLA_SPECIES["olive"]
    crown = set(v for kk, v in sp["colours"].items() if kk != "stem" and isinstance(v, str) and v)
    spots = _p18_olive_spots(plan, crown)
    if len(spots) < 4:                               # fallback: the same grid, half a spacing in from the edges
        spots = [((j + 0.5) * P18_OLIVE_TREE_M, (i + 0.5) * P18_OLIVE_ROW_M) for i in range(nr) for j in range(nt)]
    for sh in plan:
        pts = [V(p[0], p[1], 0.0) for p in sh[1]]
        if sh[0] != "poly":
            pg.line(pts, sh[2], sh[3])
        elif sh[2] in crown:                         # the crown's footprint = its midday shade on the ground
            pg.poly([pts], fill=COL["shade"], stroke=None, alpha=0.6)
        else:
            pg.poly([pts], fill=sh[2], stroke=sh[3], lw=sh[4])
    # drip: one line along every row, from a header on the edge where the clean stream water arrives
    along_u = _p18_gap([p[1] for p in spots]) >= _p18_gap([p[0] for p in spots])
    rows = sorted(set(round((p[1] if along_u else p[0]) * 2.0) / 2.0 for p in spots))
    for r_ in rows:
        ln = [V(0.0, r_, 0.0), V(a, r_, 0.0)] if along_u else [V(r_, 0.0, 0.0), V(r_, b, 0.0)]
        pg.line(ln, C["w3"], 0.25)
    head = [V(0.0, 0.0, 0.0), V(0.0, b, 0.0)] if along_u else [V(0.0, 0.0, 0.0), V(a, 0.0, 0.0)]
    pg.line(head, C["d3"], 0.5)
    mid = (0.0, b / 2.0) if along_u else (a / 2.0, 0.0)
    tail = (mid[0] - 14.0, mid[1]) if along_u else (mid[0], mid[1] - 14.0)
    arrow(pg, [V(tail[0], tail[1], 0.0), V(mid[0], mid[1], 0.0)], C["d2"], 0.6, 2.2)
    tx, ty = V(tail[0], tail[1], 0.0)
    pg.text(u"clean stream water", tx, ty + 1.6, FS_MIN, C["d3"], bold=True, align="C")
    # the trees standing, and one person picking, drawn back to front
    kz = k * math.cos(math.radians(PHI))             # vertical metres on this axonometric
    items = [(V(u, v, 0.0), "t", i) for i, (u, v) in enumerate(spots)]
    fu, fv = min(spots, key=lambda p: V(p[0], p[1], 0.0)[1])
    fp = V(fu + (1.4 if along_u else 0.0), fv + (0.0 if along_u else 1.4), 0.0)
    items.append((fp, "f", -1 if fp[0] > V(fu, fv, 0.0)[0] else 1))
    for (px, py), kind, i in sorted(items, key=lambda t: -t[0][1]):
        if kind == "t":
            _p18_put(pg, pla_section("olive", px, py, k, h_m=sp["h_m"] * math.cos(math.radians(PHI)),
                                     crown_m=sp["crown_m"], seed=i))
        else:
            _p18_fig(pg, "olive", px, py, kz, C["dark"], facing=i, branch_h=P18_BRANCH_M)
    bb = items_bbox(pg.items)
    node(pg, bb[0] + 3.0, bb[3] + 8.0, 11, opt, 2.6)
    pg.text(u"EXISTING FARMLAND, OFF SITE", bb[0] + 7.0, bb[3] + 7.2, FS_MIN, COL["ink"], bold=True)
    pg.text(u"olives {:.0f} x {:.0f} cm · drip along every row".format(P18_OLIVE_TREE_M * 100, P18_OLIVE_ROW_M * 100),
            bb[0] + 7.0, bb[3] + 7.2 - FS_MIN * 1.35, FS_MIN, COL["ink"])
    return pg

def main():
    btn, on = button_state()
    pressed = (on and not mem_get("prev", False)) or chain_fire(_GH_IN.get(btn), "chain_seen", btn)
    globals()["_ran_now"] = pressed
    mem_set("prev", on)
    if not pressed and mem_get("ver") != SHORT:     # v2 (Aras 27 Oct 15:35): a newly pasted version shows itself at
        for k_, v_ in (("last", ""), ("status", ""), ("files", []), ("done", "idle")):   # once, idle, without the old
            mem_set(k_, v_)                                                              # run's time or log
    if pressed:
        mem_set("ver", SHORT)
    if not pressed:
        last = mem_get("last", "")
        gh_status(mem_get("status", "") or SHORT + " · idle")
        return (last if last else u"Idle. Press the Button to write the water board. ({})".format(VERSION)), \
            mem_get("files", [])
    t0 = time.time()
    log, err, folder, files = [], None, None, []
    try:
        folder, files = build_all(Rhino.RhinoDoc.ActiveDoc, log)
    except Exception as ex_:
        import traceback
        err = u"ERROR: {}: {}\n{}".format(type(ex_).__name__, ex_, traceback.format_exc())
    if folder and files and not err:                # v1.10: the booklet's crops of this sheet; never breaks it
        try:
            booklet_export(folder, files[0], log)
        except Exception as ex_:
            log.append(u"booklet not written: {}: {}".format(type(ex_).__name__, ex_))
    log += bg_tidy_output(OUT_FOLDER)               # 27 Oct: output/ = PDFs only
    secs = time.time() - t0
    head = [u"{} · total {:.0f} s".format(VERSION, secs), err or u"Output: {}".format(folder)]
    text = u"\n".join(head + log)
    status = u"{} · {}".format(SHORT, "ERROR" if err else time.strftime("%H:%M") + " · {:.0f} s".format(secs))
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, LOG_NAME), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    mem_set("last", text)
    mem_set("status", status)
    mem_set("files", files)
    gh_status(status)
    if err:
        gh_message("error", err)
    return text, files


# ================================================================ embedded engines
# SKETCH_SRC: pr1_drawings v3.1's concept sketches (SKETCH style) with a page-item layer instead of Rhino baking;
# owner names, working-area bars and figures printed elsewhere taken out (24 Oct). Run by sketch_engine().
bergama_data("SKETCH_SRC")

# DETAIL_SRC: bergama_detail_section v2's drawing code (its PDF writer and Grasshopper part left out; weir wording
# replaced by the continuous strip, CONFLICTS.md rows 1-2; no working-area bar). Run by detail_engine().
bergama_data("DETAIL_SRC")


try:
    _txt, _files = main()
except Exception as _ex:
    _txt, _files = u"ERROR: {}: {} ({})".format(type(_ex).__name__, _ex, VERSION), []
    gh_status(SHORT + " · ERROR")
    mem_set("last", _txt)   # 25 Oct: the error stays on the log after the Button is released
    mem_set("status", SHORT + " · ERROR")
log = _txt
print(_txt)                  # 25 Oct 12:10: the canvas's log output is Grasshopper's "out" (printed text): print the log
pdf = _files
if globals().get("_ran_now"):
    mem_set("done", done_text(True, "ERROR" not in str(mem_get("status", "")), time.time() - _T_START))
done = mem_get("done", "idle")   # 25 Oct 10:20: stays after the run; wire into the next script's run (one-click chain)
