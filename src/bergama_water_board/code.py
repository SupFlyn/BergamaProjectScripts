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
v7: assets_2 high-res silhouettes (Aras 30 Oct 06:11, a feature change): the detailed sections draw the PhyloPic trees
  (plane, ash, olive, stone pine) and crops (maize, tomato) of common/hires.py in each section's own colours, roots
  cut at the ground, uniform scale (needs Data/assets_hires.json; without it the old primitives). pp.14-15 also draw
  the recorded animals as PhyloPic silhouettes in their own colours (P14_HR; wagtails + green toad keep their
  pictograms) and the bare plane in its leafless silhouette; p.17 sections and cards; p.18 axonometric keeps its
  primitives. Output: Bergama_water_board_v7_A_cubes.pdf.
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

VERSION = "bergama_water_board v7 (2026-10-30)"
SHORT = "v7"
BUTTON_WORDS = ("build", "bake", "run", "go", "press", "button", "start")
BOARD_W, BOARD_H = 1189.0, 841.0     # A0 landscape, mm
M = 14.0                             # board margin, mm
OPTIONS = ("A",)                     # v1.7: option A only (organic only where the project meets the water), Aras 16:43
STORAGE_STYLES = ("cubes",)          # v1.6: cubes only (Aras 25 Oct 13:12; the chart is gone)
CUBE_SCALE = 1000.0                  # the storage cubes' scale, still written to results.json "storage" (v5, T3b: p.12
#                                      draws no cubes panel any more; the design store is a cube at the water map's scale)
OUT_FOLDER = "bergama_water_board"
OUT_NAME = "Bergama_water_board_v7_{}_{}.pdf"
LOG_NAME = "bergama_water_board_log.txt"
#@include ../common/bergama_paths.py
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
#@include ../common/_gh_inputs.py


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


#@include ../common/done_text.py



#@include ../common/to_bool.py


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
#@include ../common/_key.py


#@include ../common/mem_get.py


#@include ../common/mem_set.py


GH_LABEL = "WaterBoard"                                # Aras 25 Oct 09:44: name under the component


#@include ../common/gh_status.py


#@include ../common/gh_message.py


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


#@include ../common/wrap.py


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


#@include ../common/hex_rgb.py


_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"


#@include ../common/pdf_str.py


#@include ../common/_f.py


#@include ../common/page_stream.py


#@include ../common/_text_ops.py


#@include ../common/pdf_fonts.py


#@include ../common/write_pdf.py

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


#@include ../common/_tree_rand.py


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
#@include ../common/items_bbox.py


#@include ../common/xform.py


#@include ../common/place.py


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
#@include ../common/rect.py


#@include ../common/section_style.py
# v5 (revision 29 Oct, T3b): the shared modules the pages call (T2a levels + basemap, T2b plants + icons); plants after
# section_style (it includes section_parts)
#@include ../common/plants.py
#@include ../common/hires.py
#@include ../common/icons.py
#@include ../common/data/LEVELS.py
#@include ../common/levels.py
#@include ../common/basemap.py


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


#@include ../common/node.py


#@include ../common/para.py
# v4 (MIRAQUA 28 Oct, PLAN §2): the round's shared definitions (styles, units, figures, label placing)
#@include ../common/r28_style.py
#@include ../common/units.py
#@include ../common/figures.py
#@include ../common/label_place.py


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
#@include data/CUTS.py
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


#@include parts/r28_occupancy.py


# ---------------------------------------------------------------- W3a  concept sections (pr1 v3.1 idea sketches)
# SKETCH_SRC (end of this file) is pr1's sketch code; it runs in its own namespace and draws page items in pr1's
# order. The element numbers come from node() of this board.
_SK = []


#@include ../common/sketch_engine.py


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
#@include data/SPECIES.py


# W3b band -> its days a year under water (RWS ranges, PLANT_BANDS); A is the strip itself (permanent)
BAND_DAYS = {"B": (150.0, 365.0), "C": (50.0, 150.0), "D": (10.0, 150.0), "E": (0.5, 50.0), "F": (0.0, 0.5)}






# ---------------------------------------------------------------- p.22: plant photos (Wikipedia / Commons)
# v3: the fetching moved to src/common/plant_photos.py, shared with the agriculture alternatives, so a plant shows the
# same photo, at the same 28 x 21 mm, wherever the booklet names it (cache: Downloads/Bergama/cached/plant_photos/).
# No network (or any failure) = a labelled empty frame; the board never fails on a photo.
#@include ../common/plant_photos.py
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
#@include ../common/load_palette.py


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


#@include ../common/booklet_assets.py


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


#@include ../common/search_dirs.py


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


#@include pages/p12_system.py
#@include pages/p14_15_s4.py
#@include pages/p17_planting.py
#@include pages/p18_farms.py

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
#@include data/SKETCH_SRC.py

# DETAIL_SRC: bergama_detail_section v2's drawing code (its PDF writer and Grasshopper part left out; weir wording
# replaced by the continuous strip, CONFLICTS.md rows 1-2; no working-area bar). Run by detail_engine().
#@include data/DETAIL_SRC.py


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
