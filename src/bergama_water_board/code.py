# -*- coding: utf-8 -*-
"""BERGAMA WATER BOARD v1.8 (2026-10-25; v1.8 VISUAL FIRST, Aras 17:00/17:05: sentences become pictogram chips, big-figure
callouts on the charts, a visual species card grid and season matrix; sources as [n] in the footer key; layout and look of v1.3/v1.6 kept): the water of Group 6's project on one A0 board: how much, when, how high,
how it is cleaned, held and released.

HOW TO RUN
  Rhino 8 > Grasshopper > a "Python 3 Script" component. Paste this file in, wire a plain Button into any input
  (build, run, go ...). One press writes both boards (v1.6: A and B, storage as cubes); a second press writes them again. Nothing is baked into
  Rhino. The log is kept after the Button is released (output log; pdf = the paths) and written to
  Downloads/Bergama/logs/bergama_water_board_log.txt (v1.3).
    Bergama_water_board_v1_6_A_cubes.pdf   PanelReview1A (organic forms only at the water's edge), storage as cubes
    Bergama_water_board_v1_6_B_cubes.pdf   PanelReview1B (no organic forms), storage as cubes
  Each is one A0 landscape page (1189 x 841 mm), all vector, whole-string Helvetica text.
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

NEW IN v1.7 (Aras 25 Oct 16:43: "the selection of A should be remember in the whole project so all scripts should drop B alternatives"): the board is made for option A only; one press writes
  option A's boards (no B). Nothing else changed.
NEW IN v1.6 (Aras 25 Oct 13:12: "v1.3 was fine about how it looks however it is too much text too little visual we want
more visual heavy output ... just the cube output is better so we can scrape the other part"): built from v1.3 (v1.4 and
v1.5 dropped), same layout and look, sections untouched.
  * Only the cubes boards (A and B): the to-scale storage chart and its note are gone; the note's figures (design storage,
    share of the farms' need, strip losses, seepage rates) moved onto the cubes panel, with the design storage drawn as a
    fourth cube at the same 1:1,000.
  * Text panels turned into pictogram tiles with the key figure large: WHY WE CLEAN (6 tiles), HOW FAR REED BEDS GET
    (4 tiles under the removal and coliform charts), WHERE THE CLEAN WATER GOES (5 tiles beside the aquifer bars); the
    decision row has a pictogram per step.
  * Sources: the long source lines of these panels, the chain and the river-height cuts now print as numbers [n]; the
    numbered key is in the footer, so no source is lost.
  * Chain input falls back to the upstream done text in Rhino's memory when the wire brings Null (as masterplan v16);
    the main function is main() (script standard §2).

NEW IN v1.3 (Aras 25 Oct 09:34-09:35): the same names in every script: the Button goes into an input named run, the log comes out of an output named log, and the log file is Downloads/Bergama/logs/bergama_water_board_log.txt (next to cached/ and output/), overwritten by each press.

NEW IN v1.2 (Aras 25 Oct 08:03-08:18): the chain's K5 box adds DEMETER'S GARDEN (Begum's idea alone, card i01): the
clean strip waters its olives, aromatics and seasonal beds, with a water collection basin by the bridge, and a very
small "(idea: Begum)" after the line. No demand or basin volume is drawn: her PDF gives none and only olive demand has
a source. Nothing else changed.

NEW IN v1.1 (Aras 24 Oct 09:03: "for numbers that are weak or disagree with each other correct with research and find
the factual and correct number and fix it accordingly"):
  * W2 river height: every cut is the surveyed cross-section of the main survey (Bergama Müdahele Alanları (1).dxf),
    not a trapezoid; no borrowed widths or K4 means; bed slope fitted on the surveyed bed. Q500 above the bed: upstream
    entry 3.30 m, K4 2.84 m, K5 2.79 m, downstream reach 2.33 m, flat end 1.54 m (over a 100 m wide floor).
  * S4 detail: one Q500, +46.19 on this cut (was +47.08 with a borrowed 0.21 % slope, and +49.28 from the 12.2 m
    trapezoid: both retired); every season's water is this cut's own.
  * Monthly depths (W1) and days under water on the surveyed sections.
  * Storage, farms and strip figures read from the water balance (Thread 2) results file, as the other scripts do.
  Working-area outlines are not drawn anywhere (batch rule, 22 Oct).

HOW WE KNOW IT WORKS: after a press, the text under the component reads "v1.1 · done N s" and the log lists the four
PDFs with their times; each PDF opens as one A0 page.
"""

import os
import json
import math
import time
import zlib
import tempfile
import datetime
import types as _types

import Rhino
import scriptcontext as sc

VERSION = "bergama_water_board v1.8 (2026-10-25)"
SHORT = "v1.8"
BUTTON_WORDS = ("build", "bake", "run", "go", "press", "button", "start")
BOARD_W, BOARD_H = 1189.0, 841.0     # A0 landscape, mm
M = 14.0                             # board margin, mm
OPTIONS = ("A",)                     # v1.7: option A only (organic only where the project meets the water), Aras 16:43
STORAGE_STYLES = ("cubes",)          # v1.6: cubes only (Aras 25 Oct 13:12; the chart is gone)
CUBE_SCALE = 1000.0                  # the storage cubes are drawn at 1:1,000 ...
CUBE_SCALES = (1000.0, 1250.0, 1500.0, 2000.0, 2500.0)   # ... v1.6: or the first of these at which they fit
OUT_FOLDER = "bergama_water_board"
OUT_NAME = "Bergama_water_board_v1_8_{}_{}.pdf"
LOG_NAME = "bergama_water_board_log.txt"
LOG_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "logs")   # Aras 25 Oct 09:34-09:35: every script's log here

CREDIT = u"Group 6 · Aras Özkaymakcı · Begüm Arslan · Nil Çetin"
COURSE = u"ARCH 4410 Architectural Design Studio V · Yaşar University · Fall 2026"
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
CONCEPT_CHIPS = [("rain", u"RIVER IN"), ("reed", u"CLEAN ONCE · UPSTREAM (ARAS)"), ("cube", u"HOLD WINTER WATER"),
                 ("strip", u"SUMMER STRIP · FEEDS PLANTING"), ("spread", u"FLOODS ONTO TERRACES"),
                 ("out", u"LEAVES CLEAN · DOWNSTREAM (NİL) · FARMS OUTSIDE"), ("noback", u"NO PUMPING BACK")]

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
ROUTE_IN = (u"Dec-Apr carries 89 % of the year's flow", u"calculated; " + RR + u" §0")
ROUTE_OUT = (u"worst case: no river inflow May-Oct", u"calculated case; " + CM + u" §4")


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
        if s:
            self.items.append(("text", s, x, y, size, color, bold, align, mat, halo))


#@include ../common/hex_rgb.py


_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"


#@include ../common/pdf_str.py


#@include ../common/_f.py


#@include ../common/page_stream.py


#@include ../common/_text_ops.py


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


def from_engine(items):
    """Items of the detail-section engine's Page (with layer and join fields) in this board's form."""
    out = []
    for it in items:
        k = it[0]
        if k == "poly":
            _, rings, fill, stroke, lw, dash, layer, join, stripes, alpha = it
            out.append(("poly", rings, fill, stroke, lw, dash, stripes, alpha))
        elif k == "line":
            _, pts, stroke, lw, dash, layer, cap = it
            out.append(("line", pts, stroke, lw, dash, cap))
        elif k == "circle":
            _, cx, cy, r, fill, stroke, lw, layer = it
            out.append(("circle", cx, cy, r, fill, stroke, lw))
        elif k == "text":
            _, s, x, y, size, color, bold, align, layer, mat, halo = it
            out.append(("text", s, x, y, size, color, bold, align, mat, halo))
    return out


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


def hand_arrow(pg, P, kind="water", small=1.0):
    """A bold hand arrow along P: water in the river tones, high water (flood) lighter and dashed."""
    shaft_c, head_c = (MP["amphibious"][1], MP["amphibious"][2]) if kind == "flood" else \
        (MP["discharge"][1], MP["discharge"][2])
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


SRC_KEY = []                         # v1.6: sources printed as [n] on the drawings; the numbered key is in the footer


def cite(src):
    """v1.6: the number of a source in the footer key, as "[n]"."""
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


def vbars(pg, x, y0, w, h, cats, series, vmax, ticks, fmt, unit, s):
    """Grouped vertical bars: series = [(name, colour, values)]. Returns the y under the legend."""
    fs = 2.4 * s
    for t in ticks:
        yy = y0 + h * t / vmax
        pg.line([(x, yy), (x + w, yy)], C["faint"], 0.15)
        pg.text(fmt(t), x - 1.5, yy - fs * 0.35, fs, C["ink2"], align="R")
    pg.text(unit, x, y0 + h + fs * 0.9, fs, C["ink2"])
    gw = w / len(cats)
    bw = gw * 0.78 / len(series)
    for i, c in enumerate(cats):
        for j, (_, col, vals) in enumerate(series):
            bx = x + i * gw + gw * 0.11 + j * bw
            pg.poly([rect(bx, y0, bx + bw * 0.92, y0 + h * min(vals[i], vmax) / vmax)], fill=col)
        pg.text(c, x + (i + 0.5) * gw, y0 - fs * 1.4, fs, C["ink"], align="C")
    pg.line([(x, y0), (x + w, y0)], C["ink2"], 0.25)
    lx, ly = x, y0 - fs * 3.4
    for name, col, _ in series:
        tw = text_w(name, fs)
        if lx + 2.4 * fs + tw > x + w and lx > x:
            lx, ly = x, ly - fs * 1.6
        pg.poly([rect(lx, ly, lx + 1.7 * fs, ly + 1.1 * fs)], fill=col)
        pg.text(name, lx + 2.3 * fs, ly + 0.1 * fs, fs, C["ink"])
        lx += 4.0 * fs + tw
    return ly - fs * 1.2


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


# ---------------------------------------------------------------- the chain: who does what, one way (Q6)
# Aras 24 Oct 05:48: "a small diagram such as ARAS DOES THIS, this connects to BEGÜM and BEGÜM does this, with arrows,
# clear and compact". It replaces the water loop's close-up plans, key plan and stage texts, and pr1's form plans:
# where the zones lie is the masterplan's drawing. The only drawing that names the owners (Q16).
DG_LINE = u"Demeter's Garden: strip waters olives, aromatics, beds · basin by the bridge"
CREDIT_DG = u"(idea: Beg\u00fcm)"              # v1.2: Begum's idea alone (Aras 25 Oct 08:03), kept very small
CHAIN = [
    (u"ARAS", "aras_alan", u"upstream entry", u"CLEANS · HOLDS · STORES",
     [(2, u"reed beds clean the inflow"), (3, u"terraces hold street + roof runoff"),
      (4, u"planted basins store winter water"), (5, u"spillway: overflow back to the river")]),
    (u"BEGÜM", "begum_alan", u"K4 bridge", u"LIVES WITH THE WATER",
     [(7, u"strip waters the bank planting"), (8, u"floods spread onto terraces"),
      (9, u"people on the raised dry top · Roman bridge kept")]),
    (u"BEGÜM", "begum_alan", u"K5 bridge", u"LIVES WITH THE WATER",
     [(7, u"bank planting on the strip"), (8, u"flood terraces"), (9, u"raised dry top"),
      (None, DG_LINE)]),
    (u"NİL", "nil_alan", u"downstream end", u"GIVES BACK",
     [(None, u"no treatment: arrives clean"), (10, u"clean river leaves the site"),
      (11, u"to existing farmland outside")]),
]
CHAIN_LINKS = [u"STRIP 4 m x 0.30 m · one way · river above the legal minimum flow · storage tops up May-Oct",
               u"strip and clean river", u"strip and clean river"]
CHAIN_SRC = (u"Aras 2026-10-18 14:29 (one way, cleaned once at the upstream end, no treatment at the downstream end), "
             u"14:49 and 15:02 (no farmland inside the site); strip: design values, " + RR + u" §4; minimum flow: "
             u"\"at least 10 %\" of the 10-year mean, HES water-use-rights regulation Art. 15/1, RG 15.06.2019 no. "
             u"30802; spillway: " + RR + u" §4 fail-safes; " + CR + u" D8")


def draw_chain(opt):
    pg = Page(0, 0)
    bw, bh, gap, x = 168.0, 40.0, 62.0, 62.0
    y1 = 0.0
    y0 = y1 - bh
    # 1: the river comes in
    node(pg, 4.0, y0 + bh * 0.55, 1, opt, 3.4)
    pg.text(u"RIVER INFLOW", 10.0, y0 + bh * 0.55 + 4.2, 2.4, COL["ink"], bold=True)
    chips(pg, 10.0, y0 + bh * 0.55 + 3.0, [("rain", u"catchment rain"), ("days", u"mostly winter")], 1.9, 46.0,
          COL["ink2"])
    hand_arrow(pg, [(10.0, y0 + bh * 0.35), (x - 2.0, y0 + bh * 0.35)])
    for i, (who, key, place_, verb, does) in enumerate(CHAIN):
        bx = x + i * (bw + gap)
        pg.poly([rect(bx, y0, bx + bw, y1)], fill=COL["white"], stroke=COL[key], lw=0.5)
        tw = text_w(who, 4.6, True)
        pg.poly([rect(bx, y1 - 8.0, bx + tw + 6.0, y1)], fill=COL[key])
        pg.text(who, bx + 3.0, y1 - 6.2, 4.6, COL["white"], bold=True)
        pg.text(place_, bx + tw + 9.0, y1 - 6.0, 2.6, COL[key], bold=True)
        pg.text(verb, bx + 3.0, y1 - 13.4, 3.4, COL["ink_dark"], bold=True)
        yy = y1 - 19.0
        for n_, t in does:
            if n_:
                node(pg, bx + 5.4, yy + 0.9, n_, opt, 2.5)
            pg.text(t, bx + 10.0, yy, 2.6, COL["ink"])
            if t == DG_LINE:                         # v1.2: the very small credit after the line
                pg.text(CREDIT_DG, bx + 11.0 + text_w(t, 2.6), yy, 1.3, COL["ink2"])
            yy -= 5.6
        if i < len(CHAIN) - 1:
            ax0, ax1 = bx + bw + 2.0, bx + bw + gap - 2.0
            hand_arrow(pg, [(ax0, y0 + bh * 0.62), (ax1, y0 + bh * 0.62)])
            if i == 0:
                node(pg, ax0 + 4.0, y0 + bh * 0.62 + 6.0, 6, opt, 2.3)
            para(pg, ax0 + 1.0, y0 + bh * 0.62 - 3.2, gap - 6.0, CHAIN_LINKS[i], 2.0, MP["discharge"][2], bold=True)
    ex = x + len(CHAIN) * (bw + gap) - gap + 2.0
    hand_arrow(pg, [(ex, y0 + bh * 0.62), (ex + 40.0, y0 + bh * 0.62)])
    node(pg, ex + 46.0, y0 + bh * 0.62, 11, opt, 3.4)
    pg.text(u"EXISTING FARMLAND", ex + 2.0, y0 + bh * 0.62 - 7.0, 2.4, COL["ink"], bold=True)
    chips(pg, ex + 2.0, y0 + bh * 0.62 - 8.2, [("out", u"outside the site"), ("flag", u"route not designed")], 1.9,
          50.0, COL["ink2"])
    pg.text(u"Sources: " + cite(CHAIN_SRC), x, y0 - 4.0, 1.8, COL["ink2"])
    return pg


# ---------------------------------------------------------------- W1  the year of the water (Q2: bars, lines, brackets)
# One month axis in the DSİ water-year order (Oct-Sep), four rows that share it, the season brackets under them.
YEAR_SRC = [
    (u"rain, mm a month", u"measured, WMO 1991-2020 normals, MGM 17742 Bergama; 619.6 mm a year"),
    (u"open-water evaporation, mm a month", u"calculated, Hargreaves (FAO-56) x 1.05; " + RR + u" A1"),
    (u"river past the site, million m³ a month", u"calculated, natural flow from measured DSİ gauges 2016-2021 "
                                                  u"(D04A053, D04A063), area-scaled to 101 km²; " + RR + u" A2"),
    (u"rain on the study areas' roofs and ground, thousand m³", u"calculated, survey roofs x C 0.95, rest x C 0.50; " +
     RR + u" A2"),
    (u"mean water depth in the bed, m", u"calculated, Manning n 0.050 (rough bed) on the surveyed channel; line = "
                                        u"wetter gauge, band = the two gauges; " + RR + u" A3"),
    (u"greenness (NDVI)", u"Sentinel-2 L2A, median of every clear scene of the month 2019-2025; classes CLC+ 2021; "
                          u"bergama_plant_data_v1.json"),
]


def wy_pos(doy):
    """Day of the year -> month position on the water-year axis (0 = start of October)."""
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    acc = 0
    for m, dd in enumerate(days):
        if doy <= acc + dd:
            return (m - 9) % 12 + (doy - acc - 0.5) / dd
        acc += dd
    return 11.99


def draw_year(opt):
    pg = Page(0, 0)
    lx, gx, mw = 0.0, 50.0, 19.0
    gw = 12 * mw
    rx = gx + gw + 6.0

    def X(i):
        return gx + (i + 0.5) * mw

    def row_label(y_top, i):
        t, s = YEAR_SRC[i]
        y = para(pg, lx, y_top + 1.0, 47.0, t, 2.3, COL["ink"], bold=True)
        para(pg, lx, y, 47.0, cite(s), 1.6, COL["ink2"])

    winter = set(WY.index(m) for m in (11, 0, 1, 2, 3))
    dry = set(WY.index(m) for m in (6, 7, 8))
    # ---- row 1: rain against open-water evaporation
    y0, h = -36.0, 32.0
    row_label(y0 + h, 0)
    para(pg, lx, y0 + 12.0, 47.0, YEAR_SRC[1][0], 2.3, COL["ink"], bold=True)
    para(pg, lx, y0 + 9.0, 47.0, cite(YEAR_SRC[1][1]), 1.6, COL["ink2"])
    vmax = 220.0
    for t in (0, 50, 100, 150, 200):
        yy = y0 + h * t / vmax
        pg.line([(gx, yy), (gx + gw, yy)], COL["faint"], 0.12)
        pg.text(str(t), gx - 1.2, yy - 0.6, 1.6, COL["ink2"], align="R")
    for i, m in enumerate(WY):
        x = gx + i * mw
        hr, he = h * RAIN[m] / vmax, h * EVAP[m] / vmax
        pg.poly([rect(x + 2.5, y0, x + 9.3, y0 + hr)], fill=C["w3"])
        pg.poly([rect(x + 9.7, y0, x + 16.5, y0 + he)], fill=C["structure"])
        pg.text(u"{:.0f}".format(RAIN[m]), x + 5.9, y0 + hr + 0.7, 1.4, C["w4"], align="C")
        if RAIN[m] > EVAP[m]:
            pg.text(u"+", x + 5.9, y0 + hr + 2.8, 3.0, C["d3"], bold=True, align="C")
    pg.line([(gx, y0), (gx + gw, y0)], COL["ink2"], 0.25)
    pg.poly([rect(rx, y0 + h - 3.0, rx + 4.0, y0 + h - 0.6)], fill=C["w3"])
    pg.text(u"rain", rx + 5.5, y0 + h - 2.6, 1.9, COL["ink"])
    pg.poly([rect(rx, y0 + h - 7.0, rx + 4.0, y0 + h - 4.6)], fill=C["structure"])
    pg.text(u"open-water evaporation", rx + 5.5, y0 + h - 6.6, 1.9, COL["ink"])
    pg.text(u"+ = rain > evaporation: Nov-Feb only", rx, y0 + h - 10.2, 1.7, C["d3"], bold=True)
    figs(pg, rx, y0 + h - 11.6, [(u"619.6 mm", u"rain a year"), (u"1,303 mm", u"evaporation a year"),
                                 (u"-197.6 mm", u"July")], 64.0)              # v1.8: was a sentence
    # ---- row 2: river flow past the site, and rain on the study areas (own scale)
    y0, h = y0 - 42.0, 30.0
    row_label(y0 + h, 2)
    for i, m in enumerate(WY):
        x = gx + i * mw
        hh = max(0.25, h * RIVER[m] / 7.5e6)
        c = MP["discharge"][2] if i in winter else (COL["faint"] if i in dry else MP["discharge"][0])
        pg.poly([rect(x + 3.0, y0, x + 16.0, y0 + hh)], fill=c)
        pg.text(u"{:.2f}".format(RIVER[m] / 1e6), x + 9.5, y0 + hh + 0.7, 1.4, C["w4"], align="C")
    pg.line([(gx, y0), (gx + gw, y0)], COL["ink2"], 0.25)
    figs(pg, rx, y0 + h + 1.0, [(u"21 Mm³", u"a year past the site"), (u"89 %", u"Dec-Apr (dark)")], 64.0)
    figs(pg, rx, y0 + h - 8.6, [(u"< 0.04 Mm³", u"Aug, Sep each"), (u"0-111 d", u"gauges dry a year (measured)")], 64.0,
         colour=COL["ink2"])
    ys = y0 - 11.0
    para(pg, lx, ys + 9.5, 47.0, YEAR_SRC[3][0], 1.9, COL["ink"], bold=True)
    para(pg, lx, ys + 3.4, 47.0, cite(YEAR_SRC[3][1]), 1.5, COL["ink2"])
    for i, m in enumerate(WY):
        x = gx + i * mw
        hh = 7.0 * AREAS_RAIN[m] / 26000.0
        pg.poly([rect(x + 6.0, ys, x + 13.0, ys + hh)], fill=C["w2"])
        pg.text(u"{:.1f}".format(AREAS_RAIN[m] / 1e3), x + 9.5, ys + hh + 0.6, 1.3, C["w3"], align="C")
    pg.line([(gx, ys), (gx + gw, ys)], COL["faint"], 0.2)
    figs(pg, rx, ys + 9.0, [(u"0.15 Mm³ = 1/136", u"of the river: the river, not local rain, fills the storage")],
         64.0, colour=C["w3"])
    # ---- row 3: mean depth in the bed
    y0, h = ys - 44.0, 34.0
    row_label(y0 + h, 4)
    vmax = 0.68

    def Yd(v):
        return y0 + h * min(v, vmax) / vmax
    for t in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6):
        pg.line([(gx, Yd(t)), (gx + gw, Yd(t))], COL["faint"], 0.12)
        pg.text(u"{:.1f}".format(t), gx - 1.2, Yd(t) - 0.6, 1.6, COL["ink2"], align="R")
    pg.line([(gx, Yd(STRIP_DEPTH)), (gx + gw, Yd(STRIP_DEPTH))], MP["storage"][2], 0.35, dash=[0.5, 0.7])
    pg.text(u"the strip: 0.30 m all year (design)", gx + gw - 1.0, Yd(STRIP_DEPTH) + 0.8, 1.7, MP["storage"][2],
            bold=True, align="R")
    series = [(u"upstream entry (narrow low-flow channel)", ("up",), MP["discharge"][1], 0.45, [1.2, 0.6]),
              (u"K4, K5 and the downstream reach (within 5 cm of each other)", ("k4", "k5", "down"), "3C5159", 0.45,
               None),
              (u"flat downstream end", ("flat",), MP["discharge"][2], 0.8, None)]
    ly = y0 + h - 1.5
    for lab, keys, colr, lw, dash in series:
        lo = [min(DEPTH[k][g][WY[i]] for k in keys for g in (0, 1)) for i in range(12)]
        hi = [max(DEPTH[k][g][WY[i]] for k in keys for g in (0, 1)) for i in range(12)]
        pg.poly([[(X(i), Yd(hi[i])) for i in range(12)] + [(X(i), Yd(lo[i])) for i in range(11, -1, -1)]],
                fill=colr, alpha=0.15)
        pg.line([(X(i), Yd(hi[i])) for i in range(12)], colr, lw, dash=dash)
        pg.line([(rx, ly + 0.6), (rx + 6.0, ly + 0.6)], colr, max(lw, 0.4), dash=dash)
        ly = para(pg, rx + 7.5, ly + 2.2, 57.0, lab, 1.8, COL["ink"]) - 2.4
    figs(pg, rx, ly - 0.5, [(u"Jul-Sep: few cm / dry", u"the strip needs stored water · low-flow depths indicative "
                                                       u"(bed interpolated)")], 64.0, big=2.6)
    # ---- row 4: greenness
    y0, h = y0 - 42.0, 32.0
    row_label(y0 + h, 5)

    def Yn(v):
        return y0 + h * v / 0.8
    for t in (0.0, 0.2, 0.4, 0.6, 0.8):
        pg.line([(gx, Yn(t)), (gx + gw, Yn(t))], COL["faint"], 0.12)
        pg.text(u"{:.1f}".format(t), gx - 1.2, Yn(t) - 0.6, 1.6, COL["ink2"], align="R")
    for doy, lab in ((LEAF_ON, u"leaf-out 16 Apr"), (LEAF_OFF, u"leaf-fall 14 Nov")):
        xx = gx + wy_pos(doy) * mw
        pg.line([(xx, y0), (xx, y0 + h)], "495338", 0.2, dash=[0.6, 0.6])
        pg.text(lab, xx + 0.8, y0 + h - 2.2, 1.5, "495338", halo="FFFFFF")
    ly = y0 + h - 1.5
    for lab, colr, lw, dash, v in NDVI:
        pg.line([(X(i), Yn(v[WY[i]])) for i in range(12)], colr, lw, dash=dash)
        pg.line([(rx, ly + 0.6), (rx + 6.0, ly + 0.6)], colr, max(lw, 0.4), dash=dash)
        ly = para(pg, rx + 7.5, ly + 2.2, 57.0, lab, 1.8, COL["ink"]) - 2.4
    figs(pg, rx, ly - 0.5, [(u"0.26 vs 0.16", u"July: riparian strip vs frame, greener every month · leaf dates: "
                                               u"deciduous pixels, fitted")], 64.0, big=2.6, colour="495338")
    for i, m in enumerate(WY):
        pg.text(MONTHS[m], X(i), y0 - 3.4, 2.0, COL["ink"], bold=i in winter, align="C")
    # ---- season brackets under the axis
    yb = y0 - 7.0

    def bracket(runs, kind, txt, src, colour, row):
        y = yb - row * 7.0
        for a, b in runs:
            xa, xb = gx + a * mw + 1.0, gx + (b + 1) * mw - 1.0
            pg.line([(xa, y + 1.2), (xa, y), (xb, y), (xb, y + 1.2)], colour, 0.35)
        xa = gx + runs[0][0] * mw + 1.0
        icon(pg, kind, xa, y - 0.6, 4.2)                     # v1.8: a pictogram per season bracket
        pg.text(txt + u" " + cite(src), xa + 5.4, y - 3.4, 1.9, colour, bold=True)
    bracket([(2, 6)], "cube", u"DEC-APR · 89 % of the flow · storage fills · high water on the terraces",
            u"calculated; " + RR + u" §0", MP["discharge"][2], 0)
    bracket([(7, 11), (0, 0)], "strip", u"WORST CASE · no inflow May-Oct · strip on stored water",
            u"calculated case; " + CM + u" §4", MP["storage"][2], 1)
    bracket([(9, 11)], "sun", u"JUL-SEP · trickle or dry bed", u"calculated; " + CM + u" §3", COL["ink2"], 2)
    return pg


# ---------------------------------------------------------------- W2a  river height at the channel cuts (Q3)
# rain_river A3_section charts (one per cut) and pr1's flood sections (the same cuts, with the crossed roads), as one
# drawing: the flat downstream end large, the others small (vertical x8). v1.1 (Aras 24 Oct 09:03, "find the factual
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
            u"bank and stream lines). Bridges, the Red Basilica tunnels and backwater are not modelled: levels just "
            u"upstream of them can be higher. Tables: " + RR + u" A3s. Summer (Jul-Sep): dry bed or a trickle. Road "
            u"widths and distances: survey road edges measured on each cut (the K4 road was 178 m away in pr1, wrong).")


def draw_cut(pg, x0, y_top, cut, wmax, fs, opt, kx):
    """One surveyed channel cut: ground, the five event levels across the width each covers, with their depths;
    returns its bbox bottom y. Horizontal kx mm per m; vertical 8 x the horizontal."""
    g, dep, ext = cut["ground"], cut["dep"], cut["ext"]
    xl, xr = float(cut["u0"]), float(cut["u0"] + len(g) - 1)
    ky = 8.0 * kx
    top = max(dep) + 0.8
    ox = x0 - xl * kx
    oy = y_top - fs * 4.2 - top * ky

    def T(x, y):
        return (ox + x * kx, oy + y * ky)
    pg.text(cut["name"], x0, y_top - fs * 1.2, fs * 1.25, COL["ink_dark"], bold=True)
    for t in range(0, int(top) + 1):
        pg.line([T(xl, t), T(xr, t)], COL["faint"], 0.1)
        pg.text(u"{} m".format(t), ox + xl * kx - 1.0, oy + t * ky - fs * 0.3, fs * 0.75, COL["ink2"], align="R")
    pts = [T(xl + i, min(h, top)) for i, h in enumerate(g)]
    pg.poly([pts + [T(xr, -0.6), T(xl, -0.6)]], fill=COL["structure"])
    pg.line(pts, COL["ink"], 0.3)
    ly = spread([oy + d * ky for d in dep], fs * 1.05)
    X1 = ox + xr * kx
    for i, d in enumerate(dep):
        c = LEVEL_COL[i]
        a, b = ext[i]
        pg.line([T(a, d), T(b, d)], c, 0.7 if i >= 3 else 0.45)
        pg.line([T(b, d), (X1 + 1.5, ly[i] + fs * 0.3), (X1 + 3.0, ly[i] + fs * 0.3)], c, 0.15)
        pg.text(u"{:.2f} m  {}".format(d, EVENTS[i]), X1 + 3.5, ly[i], fs * 0.85, c if i else C["w3"],
                bold=i >= 3)
    if cut["key"] == "k4":              # cards 8 and 9: the low right-bank ground floods in Q100 / Q500; above Q500 stays dry
        terr = 2.08                      # the right-bank terrace, m above the bed (survey, this cut)
        node(pg, ox + xl * kx + 3.5, oy + (terr + dep[4]) / 2.0 * ky, 8, opt, fs * 0.9)
        node(pg, ox + xl * kx + 3.5, oy + (dep[4] + 0.35) * ky, 9, opt, fs * 0.9)
        pg.text(u"8 flood terrace · 9 raised dry top, above Q500", ox + xl * kx + 3.5 + fs, oy + (dep[4] + 0.35) * ky
                + fs * 1.0, fs * 0.75, COL["river_dark"], bold=True)
    y = oy - 0.6 * ky - fs * 0.6
    if cut.get("bed") is not None:      # seen looking upstream: the right bank (+u negative) on the left of the page
        pg.text(u"right bank", ox + xl * kx, y - fs * 0.7, fs * 0.72, COL["ink2"], bold=True)
        pg.text(u"left bank", X1, y - fs * 0.7, fs * 0.72, COL["ink2"], bold=True, align="R")
        y -= fs * 1.1
    head = u"bed {:+.2f} · ".format(cut["bed"]) if cut.get("bed") is not None else u""
    y = para(pg, x0, y, wmax + 48.0, head + u"{:.0f} m across · vertical x8{}".format(
        xr - xl, u" · looking upstream" if cut.get("bed") is not None else u""), fs * 0.72, COL["ink2"])
    return chips(pg, x0, y - fs * 0.1, cut["tags"], fs * 0.72, wmax + 48.0) - fs * 0.5    # v1.8: notes as chips


def draw_sections(opt):
    """The flat end large with DSİ's planned channel under it at the same scale; the other four cuts in a 2 x 2
    grid at one shared scale (the widest fits 74 mm), so their sizes compare."""
    pg = Page(0, 0)
    flat, small, dsi = CUTS[0], CUTS[1:-1], CUTS[-1]
    k_big = 140.0 / (len(flat["ground"]) - 1)
    y_end = draw_cut(pg, 0.0, 0.0, flat, 140.0, 2.4, opt, k_big)
    y_end = draw_cut(pg, 0.0, y_end - 8.0, dsi, 140.0, 2.0, opt, k_big)
    k_small = 74.0 / max(len(c["ground"]) - 1 for c in small)
    x0, col_w = 205.0, 128.0
    y, y_row = 0.0, 0.0
    for i, cut in enumerate(small):
        c, r = i % 2, i // 2
        if c == 0 and r:
            y = y_row - 4.0
        yb = draw_cut(pg, x0 + c * col_w, y, cut, 74.0, 1.8, opt, k_small)
        y_row = yb if c == 0 else min(y_row, yb)
    pg.text(u"vertical x8 · flat end + DSİ channel: one scale · four small cuts: another · method " + cite(SECT_SRC),
            0.0, min(y_end, y_row) - 4.0, 1.7, COL["ink2"])
    return pg


# ---------------------------------------------------------------- W2b  the S4 detail (folded in from bergama_detail_section v2)
# The 1:75 detail of the two banks at the flat downstream end (board section line S4) is drawn by its own engine
# (DETAIL_SRC at the end of this file, the detail section v2 code without its PDF writer and Grasshopper part), at
# DETAIL_SCALE, with every season's water as a level line instead of one sheet per season (Q3). The season sheets'
# texts become the season table beside it.
DETAIL_SCALE = 200.0                 # 1:200 on the board (the engine's own sheet was 1:75)
_DET = []


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
        ly = spread(ys, 2.1)
        pg.line([(x, ys[0]), (x, ys[-1])], ns["DIM"], 0.12, layer="dimensions")
        for z, Y, Yl in zip(lv, ys, ly):
            pg.line([(x - 6.0, Y), (x + 1.2, Y)], ns["DIM"], 0.08, layer="dimensions")
            pg.line([(x - 0.8, Y - 0.8), (x + 0.8, Y + 0.8)], ns["DIM"], 0.2, layer="dimensions")
            pg.line([(x + 1.2, Y), (x + 3.0, Yl + 0.5), (x + 4.0, Yl + 0.5)], ns["GREY"], 0.08, layer="dimensions")
            pg.text("%+.2f %s" % (z, names[z]), x + 4.4, Yl - 0.1, 1.6, ns["GREY"], layer="dimensions")
    ns["level_line"] = level_line
    ns["vdims"] = vdims
    _DET.append(ns)
    return ns


def detail_levels(E):
    """Every season's water at this cut (the engine's SEASONS, this cut's own depths, v1.1), equal heights joined."""
    by_z = {}
    for sea in E["SEASONS"]:
        for z, fill_, lab, dash in sea["water"]:
            k = round(z, 2)
            t = u"{}: {}".format(sea["name"].capitalize(), (lab % z).replace(u"%+.2f" % z, u"").replace(u"  ", u" "))
            by_z.setdefault(k, []).append(t)
    return [(z, u"; ".join(ts)) for z, ts in sorted(by_z.items())]


def draw_detail(log):
    """Both banks of the S4 cut side by side, with one level ladder at the left."""
    E = detail_engine()
    notes = []
    prof = None
    try:
        r = E["rhino_inputs"](log)
        if r and r[1] is not None:
            prof = r[1]
    except Exception as ex:
        log.append(u"S4 ground from the open file not read ({}); the embedded survey profile is used".format(ex))
    if prof is None:
        prof = (E["PROFILE_S0"], E["PROFILE_DS"], E["PROFILE_Z"])
    E["SEA"].clear()
    E["SEA"].update(E["SEASON_LOOK"]["summer"])
    sea = dict(E["SEASONS"][2])             # summer: full leaf, the strip running, people at the water's edge
    sea["water"] = []
    pg = E["Page"]("detail", "S4")
    bed = E["THALWEG"][1]
    seasons = detail_levels(E)
    x, y_low = 0.0, 0.0
    for si, S in enumerate([E["Sec"](d, prof) for d in E["SECTIONS"]]):     # side by side: the board row is wide
        del E["_LV"][:]
        n0 = len(pg.items)
        y_end = E["draw_section"](pg, S, x, 0.0, notes, sea)
        for z, lab in seasons:
            E["level_line"](pg, S, z, lab, [0.6, 0.5], E["WATER_LINE"])
        x = items_bbox(from_engine(pg.items[n0:]))[2] + 14.0
        y_low = min(y_low, y_end)
        if si:                              # one ladder: both sections share the levels
            continue
        # level ladder left of the section: every water level with its height and what it is
        lv = sorted(E["_LV"], key=lambda e: e[0])
        xl = S.X0 - 4.0
        ys = [S.Y(z) for z, _, _, _ in lv]
        ly = spread(ys, 2.3)
        pg.line([(xl, min(ys)), (xl, max(ys))], E["GREY"], 0.12, layer="ladder")
        for (z, lab, colour, dash), Y, Yl in zip(lv, ys, ly):
            pg.line([(xl + 2.5, Y), (xl - 1.0, Y), (xl - 3.0, Yl + 0.6), (xl - 4.0, Yl + 0.6)], colour, 0.15,
                    layer="ladder")
            t = u"{:+.2f}  {}".format(z, lab.replace(u"%+.2f" % z, u"").replace(u"  ", u" ").strip(u" ,;"))
            pg.text(t, xl - 4.4, Yl, 1.7, colour if colour != E["WATER_LINE"] else E["FLOOD"], align="R",
                    layer="ladder")
    y = y_low - 8.0
    # v1.8 (visual first): the two note sentences as keywords; their full text is in the footer key
    pg.text(u"GROUND: survey, bed low point {:+.2f} {}  ·  WATER: calculated on this cut {}  ·  BUILT: design values "
            u"{}".format(bed, cite(u"survey TIN of spot heights, contours, bank and stream lines"), cite(
                u"Manning n 0.050 on the surveyed cross-section, bed slope 0.94 % fitted on the survey 300 m either side, "
                u"DSİ Q100 205.2 / Q500 263.3 m³/s, DSİ gauge flows 2016-2021 area-scaled; low-flow depths indicative "
                u"(bed interpolated)"), cite(u"levels, widths, walls, decks, rails, planting are design values; "
                u"entourage traced from the group's reference sections")), 0.0, y + 2.0, 1.7, E["GREY"], layer="notes")
    pg.text(u"+47.60 = Q500 + 1.41 m on this cut (was set at Q500 + 0.52 m when Q500 read +47.08)", 0.0, y - 0.8, 2.2,
            E["FLOOD"], bold=True, layer="notes")
    for n_ in notes:
        log.append(u"S4 detail: " + n_)
    out = Page(0, 0)
    out.items = from_engine(pg.items)
    return out


SEASON_VIS = {  # v1.8: the engine's season texts as keywords, every figure kept (river: calculated on this cut;
                # life: concept s.10.1, design; strip: case.md s.4, design)
    "winter": [("drop", u"Jan-Feb mean ≤ 0.43 m"), ("over", u"highest day 6 Jan 2017: 1.15 m"),
               ("cube", u"Dec-Apr 89 % of flow -> storage"),
               ("person", u"bed: flood channel, view only · marsh flooded, birds · terraces open between storms"),
               ("reed", u"plane bare, seed balls · reeds cut back · iris resting · lavender evergreen")],
    "spring": [("drop", u"Jan-Apr means 0.25-0.43 m · May 0.16-0.21 m"), ("strip", u"strip on the river · storage tops up"),
               ("person", u"strip + bed wet · marsh greens · boardwalk open · meadow, play"),
               ("reed", u"fresh leaves · reeds green · iris + lavender in flower")],
    "summer": [("drop", u"natural Jul-Sep 0.04-0.11 m · dry ~11 d a year"),
               ("strip", u"strip 4.0 x 0.30 m · on storage · one way"),
               ("person", u"wading 0.30 m · cooling · evening lights · lie-down lawn · feet in the water"),
               ("reed", u"full leaf · reed plumes · iris in leaf · last lavender · meadow drying")],
    "autumn": [("drop", u"Sep 0.05-0.07 m · Oct-Dec 0.11-0.20 m"),
               ("rain", u"design storm 137 mm in one day (28 Oct 2025, municipal, not MGM)"),
               ("strip", u"strip on the river after the first storms"),
               ("person", u"first-flush cleaning · events on the meadow · walk the gravel bed"),
               ("reed", u"plane turning · reeds gold · iris yellowing · lavender trimmed")]}
SEASON_SRC = u"S4 season texts of the detail section v2 (river: calculated on this cut; life: concept s.10.1, design; " \
             u"strip: case.md s.4, Aras 17 Oct 22:01, 19 Oct 07:43)"


def draw_season_table(E=None):
    """What each season brings at this cut, v1.8: a pictogram matrix (water, strip, life, plants) per season."""
    E = E or detail_engine()
    pg = Page(0, 0)
    cw, gap = 92.0, 8.0
    y_low, y_top = 0.0, 0.0
    for i, sea in enumerate(E["SEASONS"]):
        x = (i % 2) * (cw + gap)
        if i == 2:
            y_top = y_low - 7.0
        pg.poly([rect(x, y_top - 1.2, x + cw, y_top)], fill=BAND_BLUE[i % 4])
        icon(pg, {"winter": "rain", "spring": "flood", "summer": "sun"}.get(sea["key"], "rain"), x + cw - 7.0, y_top - 2.0, 6.0)
        pg.text(sea["name"], x, y_top - 8.0, 5.0, COL["ink_dark"], bold=True)
        pg.text(sea["months"], x + text_w(sea["name"], 5.0, True) + 3.0, y_top - 8.0, 2.4, COL["ink2"], bold=True)
        pg.text(sea["mode"].split(u"·", 1)[-1].strip().upper(), x, y_top - 12.5, 2.1, MP["discharge"][2], bold=True)
        y = y_top - 14.5
        for kind, t in SEASON_VIS[sea["key"]]:
            icon(pg, kind, x, y, 4.4)
            yy = y - 1.6
            for ln in wrap(t, 1.85, cw - 6.0):
                pg.text(ln, x + 6.0, yy, 1.85, COL["ink"])
                yy -= 2.4
            y = min(y - 5.4, yy - 0.6)
        y_low = min(y_low, y)
    pg.text(u"sources " + cite(SEASON_SRC), 0.0, y_low - 2.0, 1.6, COL["ink2"])
    return pg


# ---------------------------------------------------------------- W3a  concept sections (pr1 v3.1 idea sketches)
# SKETCH_SRC (end of this file) is pr1's sketch code; it runs in its own namespace and draws page items in pr1's
# order. The element numbers come from node() of this board.
_SK = []


#@include ../common/sketch_engine.py


SK_SRC = dict(  # v1.8: the sketches' sources, as in proposal sections v3
    levels=RR + u" v1.1 table: levels calculated on the surveyed river-height cuts (Manning, main survey TIN)",
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
CONCEPT_FILE = "concept/Selinos_riverfront_design_concept_v1.md"
C_PL = dict(green_deep="495338", green_mid="727A4E", accent="8B3A3F", ink="4A3F35", ink2="847E75", structure="B0AC9C")
DAYS_WET = (u"Days a year at or above each height at the flat downstream end (mean of WY2016-2021, surveyed "
            u"cross-section, calculated; below 0.3 m indicative): 0.10 m 144 d, 0.30 m 6 d, 0.50 m 1 d, 1.00 m 0 d; "
            u"bed dry (< 2 cm) about 34 d.")


def prect(pg, x, y, w, h, fill=None, stroke=None, lw=0.1):
    pg.poly([rect(x, y, x + w, y + h)], fill=fill, stroke=stroke, lw=lw)


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
               u"calls these ranges, not fixed limits. Band heights are PROVISIONAL: no level-duration curve of the "
               u"Selinos exists (concept §3). Z1–Z4 = bank zones of research file 04 (its own reading).")
# species: band, latin, local name, evidence (quoted or summarised from the named file, with its source), flag
#@include data/SPECIES.py
SPECIES_SRC = {"C": u"concept v1 §9.2", "R": u"research 04 species matrix", "C+R": u"concept v1 §9.2 + research 04"}


def draw_bands(opt, w=300.0, h=240.0):
    pg = Page(0, 0)
    x, y = 0.0, -h
    # v1.8: the intro sentence as chips; the reason ("no single plant takes both") stays as a keyword
    yb = chips(pg, x, y + h - 0.5, [("days", u"PROPOSAL · plants by days wet a year"),
                                    ("flag", u"no plant takes both deep water and a dry summer"),
                                    ("pin", u"schematic, not to scale " + cite(u"concept 'Selinos water calendar' v1 §9; "
                                                                             u"research file 04"))],
               2.0, w, C_PL["ink2"]) - 2.0
    # schematic bank: steps rising from the water rooms to the terraces
    dx0, dx1 = x + 2, x + w - 2
    by0 = yb - 62
    nb = len(PLANT_BANDS)
    bw = (dx1 - dx0) / nb
    levels = [0.0, 3.0, 7.0, 11.0, 16.0, 22.0]          # graphic steps only
    prof = []
    for i, b in enumerate(PLANT_BANDS):
        xa, xb = dx0 + i * bw, dx0 + (i + 1) * bw
        z = by0 + 8 + levels[i]
        prect(pg, xa, by0, bw, z - by0, fill=BAND_COL[b[0]])
        prof += [(xa, z), (xb, z)]
        pg.text(b[0], xa + bw / 2, by0 + 2.2, 4.2, "FFFFFF", bold=True, align="C")
        ty = by0 - 3.2
        pg.text(b[1], xa + 0.8, ty, 1.85, C_PL["ink"], bold=True)
        para_at(pg, b[3], xa + 0.8, ty - 2.6, 1.7, bw - 1.6, C_PL["green_deep"], bold=True)
        para_at(pg, u"depth {} · {}".format(b[4], b[5]), xa + 0.8, ty - 5.2, 1.45, bw - 1.6, C_PL["ink2"])
        # plant glyphs: type of planting only (no measured plant heights)
        gz = z
        if b[0] == "A":
            for j in range(4):
                pg.line([(xa + 3 + j * bw / 4, gz - 1.0), (xa + 3 + j * bw / 4 + 3.5, gz - 1.0)], "FFFFFF", 0.25)
        elif b[0] in ("B", "D"):
            n = 26 if b[0] == "B" else 40
            for j in range(n):
                xx = xa + 1.5 + (bw - 3) * j / (n - 1)
                hh = (6.5 if b[0] == "B" else 2.4) * (0.75 + 0.25 * math.sin(j * 1.7))
                pg.line([(xx, gz), (xx + 0.4 * math.sin(j), gz + hh)], C_PL["green_deep"] if b[0] == "B" else
                        C_PL["green_mid"], 0.18)
        elif b[0] in ("C", "E", "F"):
            spots = {"C": [(0.3, 2.6, 7.0), (0.72, 2.2, 6.0)], "E": [(0.35, 4.2, 12.0), (0.78, 3.4, 10.0)],
                     "F": [(0.6, 3.0, 9.0)]}[b[0]]
            for fx, r, top in spots:
                def P(px, py, pz, xa=xa, gz=gz):
                    return (xa + px, gz + pz * 1.0)
                draw_tree(pg, P, 1.0, fx * bw, 0.0, r, top, TREE_STYLES["tree" if b[0] != "F" else "olive"], shadow=False)
            if b[0] == "F":
                for j in range(int(bw // 3)):
                    pg.line([(xa + j * 3, gz), (xa + j * 3 + 1.5, gz)], C_PL["ink2"], 0.2)
    pg.line(prof, C_PL["ink"], 0.35)
    pg.text(u"SCHEMATIC · band heights PROVISIONAL · glyphs show the kind of planting, not plant heights",
            dx1, yb - 1.5, 1.6, C_PL["accent"], align="R")
    ty = by0 - 15.5
    pg.text(u"bands " + cite(BAND_SOURCE), x, ty, 1.45, C_PL["ink2"])
    # v1.8: DAYS_WET as a small bar chart (days a year at or above each height, flat downstream end)
    pg.text(u"DAYS WET A YEAR · FLAT END " + cite(DAYS_WET), x + 30.0, ty, 1.6, C_PL["green_deep"], bold=True)
    bx = x + 92.0
    for j, (hgt, d) in enumerate(((u"0.10 m", 144), (u"0.30 m", 6), (u"0.50 m", 1), (u"1.00 m", 0), (u"dry bed", 34))):
        xx = bx + j * 40.0
        pg.text(hgt, xx, ty, 1.6, C_PL["ink"], bold=True)
        pg.poly([rect(xx + 9.0, ty - 0.2, xx + 9.0 + max(0.4, 24.0 * d / 144.0), ty + 1.4)],
                fill=BAND_COL["A"] if j < 4 else BAND_COL["E"])
        pg.text(u"{} d".format(d), xx + 9.6 + 24.0 * d / 144.0, ty, 1.6, C_PL["green_deep"], bold=True)
    ty -= 4.0
    # v1.8: species as cards in three columns: band, name, evidence chips, flag pictogram; sources as [n]
    ncol, gx_ = 3, 3.0
    cw_ = (w - (ncol - 1) * gx_) / ncol
    rows = (len(SPECIES) + ncol - 1) // ncol
    rh = 7.4
    for k_, (band, lat, loc, ev, src_ev, flag, src) in enumerate(SPECIES):
        c_, r_ = k_ // rows, k_ % rows
        cx_, cy_ = x + c_ * (cw_ + gx_), ty - r_ * rh
        if band in BAND_COL:
            prect(pg, cx_, cy_ - 2.6, 4.2, 2.8, fill=BAND_COL[band])
            pg.text(band, cx_ + 2.1, cy_ - 2.0, 1.7, "FFFFFF", bold=True, align="C")
        else:
            pg.text(u"x", cx_ + 2.1, cy_ - 2.0, 1.9, C_PL["accent"], bold=True, align="C")
        pg.text(lat, cx_ + 5.5, cy_ - 2.0, 1.75, C_PL["ink"], bold=True)
        pg.text(loc + u" " + cite(src_ev + u" (" + SPECIES_SRC[src] + u")"), cx_ + 6.5 + text_w(lat, 1.75, True), cy_ - 2.0,
                1.5, C_PL["ink2"])
        chips(pg, cx_ + 5.5, cy_ - 2.9, ev, 1.5, cw_ - 26.0)
        if flag:
            hot = flag.isupper() or "TOXIC" in flag or "POISON" in flag or "REMOVE" in flag
            kind = "scent" if ("aromatic" in flag or "scent" in flag) else ("warn" if hot else "flag")
            fx = cx_ + cw_ - 22.0
            icon(pg, kind, fx, cy_ - 2.6, 2.6)
            para_at(pg, flag, fx + 3.2, cy_ - 4.4, 1.4, 19.0, C_PL["accent"] if hot else C_PL["ink2"], bold=hot, lead=1.2)
    pg.text(u"full sources " + cite(CONCEPT_FILE + u" §9; library/context/2026-10-19_research_vegetation/"
            u"04_plants_flood_drought_cleaning.md (POWO, FEIS, JRC Atlas, Song 2021, Schindler et al. 2022 ...); "
            u"Vetiver left out: not native (POWO)"), x, max(ty - rows * rh - 1.0, y + 4.2), 1.4, C_PL["ink2"])
    return pg


# ---------------------------------------------------------------- W4, W6, W7 and the decision row (bergama_water_case v1.1)
# Group 6's tables: A6_strip_storage.csv, A7, DATA_REGISTER rows as named.
# A6_strip_storage.csv: storage needed (m³): (bed, width) -> (measured 2016-2021, -30.7 %, -30.7 % + no inflow May-Oct)
WINTER_FLOW = 18653245          # A7: natural flow Dec-Apr at the site (m³, calculated)
# v1.1: storage design, strip draw and olive need from the water balance (Thread 2), never typed in: its results file
# (written on every run of bergama_water_balance_v2.py), else the default-lands copy of 24 Oct 08:21 (research/
# water_balance/water_balance_results_default.json).
WB_FILES = [os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "output", "Bergama_water_balance_analysis",
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
    return WB_DEFAULT, u"water balance default lands, 24 Oct (FLAG: results file not found in Downloads)"


WB, WB_SRC = wb_results()
try:
    WB_STORE = tuple(WB["design"]["central_range_m3"])
    WB_PCT = tuple(WB["design"]["central_range_pct_1in5_dry"])
    WB_STRIP = float(WB["strip_m3_per_year"])
    OLIVE_M3_HA = WB["net_irrigation_mm"]["olive"]["dry5"] / DRIP_EFF * 10.0     # m³/ha at the intake, 1-in-5 dry year
except Exception:
    WB, WB_SRC = WB_DEFAULT, u"water balance default lands, 24 Oct (FLAG: results file unreadable)"
    WB_STORE, WB_PCT = (350000, 375000), (99.2, 99.7)
    WB_STRIP, OLIVE_M3_HA = 23462.0, 720.1 / DRIP_EFF * 10.0
MIN_FLOW = 1001453              # A7: minimum flow kept in the stream Dec-Apr (m³)
# EN-D1 (Vymazal 2010): removal %, published: BOD5, solids, total P, total N, NH4-N
WETLAND = [(u"Horizontal subsurface flow", (75, 75, 50, 43, 39)), (u"Vertical flow", (90, 89, 56, 43, 73)),
           (u"Free water surface", (74, 77, 34, 45, 48))]
WETLAND_KEYS = [u"BOD5", u"Solids", u"Total P", u"Total N", u"NH4-N"]

# v1.6 (Aras 25 Oct 13:12 "too much text too little visual"): the water case's text panels as pictogram tiles,
# (pictogram, heading, key figure, short line, source); every fact and figure of v1.3's sentences is kept.
WHY_T = [
    ("sewage", u"SEWAGE WENT INTO THE SELINUS", u"3 km + 500 m",
     u"İZSU sewer + connections, Feb 2024 · against odour, flies · finished? not verified",
     u"published, İZSU via Gerçek İzmir 28 Feb 2024; " + REG + u" SE-22"),
    ("gauge", u"MEASURED WATER QUALITY OF THE SELINUS", u"NO DATA",
     u"in any source the project holds", WD + u", Still needed 4"),
    ("house", u"GREYWATER OF THE RIVERSIDE HOUSES", u"NO DATA",
     u"sinks, showers, laundry: no volume, no route in any source", u"not in the project's data"),
    ("plant", u"BERGAMA'S TREATMENT PLANT", u"14,304 m³ a day",
     u"treated -> Bakırçay, not the Selinus", u"published, TMMOB 2023 citing İZSU; " + WD),
    ("tank", u"RAINWATER TANKS", u"roofs only",
     u"garden + toilets only · not listed for drinking",
     u"published, ÇŞİDB guide 2025; rainwater regulation Art. 13, 16(1); " + REG + u" EN-E5, EN-A2"),
    ("reed", u"SO THE RIVER IS CLEANED", None,
     u"before people + plants use it (inferred) · first treatment designed here", REG + u" §2, row 'Is treatment necessary?'")]
HOW_T = [
    ("reed", u"REED-BED FIELD DATA", u"58-88 %", u"of NH4-N removed", u"published; " + REG + u" PL-09"),
    ("area", u"BED AREA PER PERSON EQUIVALENT", u"5 m² · 1-3 m²",
     u"horizontal · vertical flow · people served unknown: no bed size yet", u"published, Vymazal 2010; " + REG +
     u" EN-D2; population: gap"),
    ("nose", u"HOW MUCH ANY PLANT REDUCES ODOUR", u"NO DATA", u"no source measures it", REG + u" §2: gap"),
    ("uv", u"DISINFECT WHERE PEOPLE TOUCH IT", u"UV",
     u"water people touch + park irrigation · UV = the reuse method", u"inferred from EN-D3, EN-E1; EN-E2 published")]
COLIFORM = [  # (label, low, high, colour key, source); 0 = the limit is zero
    (u"Left after an emergent-plant wetland", 1e2, 1e5, "d2", u"published, reviews 2005 and 2020; EN-D3"),
    (u"Reuse class B limit (orchards, vineyards)", 200, 200, "acc", u"published, 2010 communiqué; EN-E1"),
    (u"Reuse class A limit (parks, raw-eaten crops)", 0, 0, "acc", u"published, 2010 communiqué; EN-E1"),
    (u"Drinking water limit (E. coli)", 0, 0, "acc", u"published, Ministry of Health; EN-E3")]
GOES_T = [
    ("out", u"THE CLEAN RIVER LEAVES THE SITE", None,
     u"-> existing farmland on the slopes outside · no farm channel inside · route not designed",
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
    (u"KEEP SEWAGE OUT", u"İZSU sewer (SE-22) · finished? check"),
    (u"CLEAN AT THE UPSTREAM END", u"reed beds at the entry · whole reach clean (Aras, 18 Oct)"),
    (u"DISINFECT WHERE PEOPLE TOUCH IT", u"wetlands leave 10^2-10^5 CFU/100 ml · class A: 0 (inferred)"),
    (u"HOLD WINTER WATER", u"{:,.0f}-{:,.0f} m³ incl. strip = {:.1f}-{:.1f} % of Dec-Apr flow".format(
        WB_STORE[0], WB_STORE[1], 100.0 * WB_STORE[0] / WINTER_FLOW, 100.0 * WB_STORE[1] / WINTER_FLOW)),
    (u"KEEP THE STRIP ALIVE", u"clean water all summer · feeds the planting (D8)"),
    (u"FARMS FIRST", u"farms outside (class B) · 10,000 m³ = {:.2f} ha olives · aquifer used 4.4 x".format(
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


def tiles(pg, x, y, w, items, s, cols=2):
    """v1.6: facts as tiles: pictogram, heading, the key figure large, a short line and its source number.
    items = [(pictogram, heading, figure or None, line, source)]. Returns the bottom y."""
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
        rh = max(t[3] for t in row)
        for c_, (kind, big, L, _) in enumerate(row):
            tx = x + c_ * (tw + g)
            pg.poly([rect(tx, yy - rh, tx + tw, yy)], fill=C["paper"], stroke=C["faint"], lw=0.2)
            icon(pg, kind, tx + pad, yy - pad, ic)
            lx, ly = tx + 2 * pad + ic, yy - pad
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


def _cleaning_why(pg, x, y, w, h, s):
    """v1.6: what goes into the river, as six tiles (was six paragraphs)."""
    return tiles(pg, x + 8.0, y - 2.0, w - 14.0, WHY_T, s * 0.9, 2)




def _cleaning_how(pg, x, y, w, h, s):
    fs = 2.4 * s
    cols = [C["wet1"], C["d2"], C["wet"]]
    ch = 26.0 * s
    cx, cw = x + 10.0 + 6.0 * s, w - 20.0 - 6.0 * s
    yb = vbars(pg, cx, y - 6.0 - ch, cw, ch, WETLAND_KEYS,
               [(nm, cols[i], vals) for i, (nm, vals) in enumerate(WETLAND)], 100.0, [0, 50, 100],
               lambda t: str(int(t)), u"% removed by constructed wetlands (published, Vymazal 2010; EN-D1)", s)
    top = yb - fs * 3.0
    pg.text(u"Coliforms per 100 ml, log scale", x + 10.0, top + fs * 0.4, fs * 1.1, C["ink"], bold=True)
    lab_w = max(max(text_w(c[0], fs), text_w(c[4], fs * 0.75)) for c in COLIFORM) + 4.0
    gx = x + 10.0 + lab_w
    gw = w - 20.0 - lab_w - text_w(u"100 - 100,000", fs, True) - 4.0
    rh = fs * 3.0
    for e in range(0, 7):
        xx = gx + gw * e / 6.0
        pg.line([(xx, top - 4 * rh), (xx, top - fs * 0.6)], C["faint"], 0.15)
        pg.text(u"1" if e == 0 else u"10^{}".format(e), xx, top - 4 * rh - fs * 1.2, fs * 0.85, C["ink2"],
                align="C")
    for r, (lab, lo, hi, ck, src) in enumerate(COLIFORM):
        yy = top - fs * 0.6 - r * rh
        pg.text(lab, gx - 2.0, yy - fs * 1.0, fs, C["ink"], align="R")
        pg.text(src, gx - 2.0, yy - fs * 2.0, fs * 0.75, C["ink2"], align="R")
        if hi <= 0:
            pg.poly([rect(gx - 0.6, yy - fs * 1.8, gx + 0.6, yy - fs * 0.3)], fill=C[ck])
            pg.text(u"0", gx + 2.0, yy - fs * 1.4, fs, C[ck], bold=True)
        elif lo == hi:
            xx = gx + gw * math.log10(lo) / 6.0
            pg.poly([rect(xx - 0.6, yy - fs * 1.8, xx + 0.6, yy - fs * 0.3)], fill=C[ck])
            pg.text(u"below {:,.0f}".format(lo), xx + 2.0, yy - fs * 1.4, fs, C[ck], bold=True)
        else:
            x0, x1 = gx + gw * math.log10(lo) / 6.0, gx + gw * math.log10(hi) / 6.0
            pg.poly([rect(x0, yy - fs * 1.6, x1, yy - fs * 0.5)], fill=C[ck])
            pg.text(u"100 - 100,000", x1 + 2.0, yy - fs * 1.4, fs, C["d3"], bold=True)
    return tiles(pg, x + 10.0, top - 4 * rh - fs * 2.6, w - 20.0, HOW_T, s * 0.9, 2)




def draw_cleaning(pg, x, y, w, h, s):
    """Why clean (sewage, greywater gaps) and how far reed beds get (removal, coliforms): water case panels 1 and 5
    side by side."""
    wl = w * 0.46
    a = _cleaning_why(pg, x - 4.0, y, wl + 4.0, h, s)
    b = _cleaning_how(pg, x + wl - 4.0, y, w - wl + 4.0, h, s)
    return min(a, b)


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
        pg.text(u"{} hm³ a year".format(v), gx + gw * v / 200.0 + 2.0, yy - bh * 0.5 - fs * 0.35, fs, C["ink"],
                bold=True)
    yy = figs(pg, x + 10.0, top - 2 * (bh + 2.4 * s) - 1.0, [(u"use = {:.1f} x potential".format(198.01 / 45.4),
              u"Lower Bakırçay · farm water eases the aquifer " + cite(u"published, North Aegean drought management "
              u"plan 2018 (official); ratio calculated; " + WD))], w - 20.0, 4.0 * s, 2.6 * s, C["acc"]) - 2.8 * s * 0.8
    return tiles(pg, x + 10.0, yy, w - 20.0, GOES_T, s, 2)




DEC_ICONS = ["sewer_x", "reed", "uv", "cube", "strip", "farm", "nodrink"]


def draw_decision(pg, x, y, w, h, s):
    pg.text(u"WHAT THE FIGURES SUPPORT", x, y - 7.0, 5.6, C["dark"], bold=True)
    n = len(DECISION)
    gap = 9.0
    bw = (w - (n - 1) * gap) / n
    low = y
    for i, (t, src) in enumerate(DECISION):
        bx = x + i * (bw + gap)
        pg.poly([rect(bx, y - h, bx + bw, y - 12.0)], fill=C["white"], stroke=C["d2"], lw=0.4)
        pg.text(str(i + 1), bx + 4.0, y - 14.0 - 6.0 * s, 6.0 * s, C["d3"], bold=True)
        icon(pg, DEC_ICONS[i], bx + bw - 4.0 - 8.0 * s, y - 13.0, 8.0 * s)          # v1.6: a pictogram per step
        yy = para(pg, bx + 4.0, y - 16.0 - 6.0 * s, bw - 8.0, t, 3.4 * s, C["dark"], bold=True)
        low = min(low, para(pg, bx + 4.0, yy - 1.0, bw - 8.0, src, 2.8 * s, C["ink"]))
        if i < n - 1:
            ym = y - 12.0 - (h - 12.0) / 2
            arrow(pg, [(bx + bw + 0.8, ym), (bx + bw + gap - 0.8, ym)], C["d3"], 0.6, 3.2)
    return low


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


def draw_cube(pg, V, u0, v0, e, tones, solid=True, dash=None):
    """A cube of edge e m standing at (u0, v0) in the view V: top, and the two sides facing the viewer."""
    P = lambda i, j, l: V(u0 + i * e, v0 + j * e, l * e)
    sides = [((0, -1), [(0, 0), (1, 0)]), ((1, 0), [(1, 0), (1, 1)]), ((0, 1), [(1, 1), (0, 1)]),
             ((-1, 0), [(0, 1), (0, 0)])]
    if solid:
        for (nu, nv), ((i0, j0), (i1, j1)) in sides:
            vis, lit = V.visible(nu, nv)
            if vis:
                pg.poly([[P(i0, j0, 0), P(i1, j1, 0), P(i1, j1, 1), P(i0, j0, 1)]], fill=tones[1] if lit else tones[2],
                        stroke=tones[2], lw=0.15, alpha=0.9)
        pg.poly([[P(0, 0, 1), P(1, 0, 1), P(1, 1, 1), P(0, 1, 1)]], fill=tones[0], stroke=tones[2], lw=0.15, alpha=0.9)
    else:
        for i0, j0, l0, i1, j1, l1 in ((0, 0, 0, 1, 0, 0), (1, 0, 0, 1, 1, 0), (1, 1, 0, 0, 1, 0), (0, 1, 0, 0, 0, 0),
                                       (0, 0, 1, 1, 0, 1), (1, 0, 1, 1, 1, 1), (1, 1, 1, 0, 1, 1), (0, 1, 1, 0, 0, 1),
                                       (0, 0, 0, 0, 0, 1), (1, 0, 0, 1, 0, 1), (1, 1, 0, 1, 1, 1), (0, 1, 0, 0, 1, 1)):
            pg.line([P(i0, j0, l0), P(i1, j1, l1)], tones[2], 0.25, dash=dash or [1.0, 0.7])
    pts = [P(i, j, l) for i in (0, 1) for j in (0, 1) for l in (0, 1)]
    return (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))


def draw_storage_cubes(opt):
    """The storage the strip needs, worst case, as cubes at 1:1,000 (calculated volumes), with IN and OUT."""
    pg = Page(0, 0)
    k = 1000.0 / CUBE_SCALE
    V = BoxView(PSI, 0.0, k, 0.0, 0.0)
    e3, e2, e1 = VOL_UNSEALED ** (1.0 / 3.0), VOL_SEALED ** (1.0 / 3.0), VOL_FIRST ** (1.0 / 3.0)
    draw_cube(pg, V, 0, 0, e2, MP["storage"], True)
    b3 = draw_cube(pg, V, 0, 0, e3, MP["storage"], False)
    b1 = draw_cube(pg, V, e3 + 14.0, 0, e1, MP["discharge"], True)
    e4 = WB_STORE[0] ** (1.0 / 3.0)                  # v1.6: the design storage (water balance), same 1:1,000
    b4 = draw_cube(pg, V, e3 + e1 + 28.0, 0, e4, MP["discharge"], False, [1.6, 0.8])
    pg.text(u"design storage", (b4[0] + b4[2]) / 2.0, b4[1] - 4.0, 1.8, COL["ink2"], align="C")
    node(pg, b3[0] + 2.0, b3[3] + 4.0, 4, opt, 2.4)
    tx = max(b3[2], b1[2], b4[2]) + 6.0
    lines = [("cube", u"{:,.0f} m³".format(VOL_SEALED), u"worst case · clay-sealed · solid cube · {:.1f} m edge".format(e2),
              u"calculated; " + RR + u" §4; 4 m strip, recirculated (one way not recalculated)"),
             ("cube", u"≥ {:,.0f} m³".format(VOL_UNSEALED), u"unsealed sand bed · dashed cube · {:.1f} m edge".format(e3),
              u"calculated; " + RR + u" §4"),
             ("strip", u"{:,.0f} m³".format(VOL_FIRST), u"first fill · 2,949 x 4 x 0.30 m · small cube · {:.1f} m".format(e1),
              u"design values 2,949 m x 4 m x 0.30 m; " + CM + u" §4"),
             ("days", u"≈ 1 %", u"of the driest year's flow · winter fills it · seal the strip",
              u"calculated; " + CM + u" (storage row)"),
             ("rain", u"IN", u"winter water from the basins · " + ROUTE_IN[0], ROUTE_IN[1]),
             ("strip", u"OUT", u"tops up the strip · " + ROUTE_OUT[0], ROUTE_OUT[1]),
             ("pin", u"?", u"where the storage sits: not decided", CR + u" 5.4"),
             ("cube", u"{:,.0f}-{:,.0f} m³".format(WB_STORE[0], WB_STORE[1]),
              u"design incl. strip · aquifer recharge · {:.0f}-{:.0f} % of farm need, 1-in-5 dry · {:.1f} m edge".format(
                  WB_PCT[0], WB_PCT[1], e4), WB_SRC),
             ("drop", u"≈ {:,.0f} m³/yr".format(WB_STRIP), u"losses only (one way, on to the farms) · evaporation + seepage "
              u"5 mm/d sealed / 25 mm/d unsealed · up to 10 x possible",
              u"calculated, sequent-peak over 2016-2021; seepage 25 mm/day = the bottom of FAO's sand range; " + RR +
              u" §4, A6; " + WB_SRC)]
    y = max(b3[3], b4[3]) + 6.0                       # v1.8: each line = pictogram + big figure + keywords + [n]
    for kind, big, t, src in lines:
        icon(pg, kind, tx, y, 5.0)
        pg.text(big, tx + 6.5, y - 3.6, 3.0, C["d3"], bold=True)
        lx = tx + 7.5 + text_w(big, 3.0, True)
        yy = y - 1.6
        for ln in wrap(t + u" " + cite(src), 1.9, 175.0 - (lx - tx)):
            pg.text(ln, lx, yy, 1.9, COL["ink"])
            yy -= 2.4
        y = min(y - 6.6, yy - 0.8)
    pg.text(u"cube edges = cube root of the volume, drawn at 1:{:,.0f}".format(CUBE_SCALE), b3[0], b3[1] - 4.0, 1.8,
            COL["ink2"])
    return pg


def tree_at(pg, P, k, x, y, opt, style="tree", r=3.0, top=8.0, shadow=False):
    draw_tree(pg, P, k, x, y, r, top, TREE_STYLES[style], shadow=shadow)


def draw_farm_picto(opt):
    """Existing farmland off the site: a pictogram (not its shape or size), olives in rows."""
    pg = Page(0, 0)
    k = 1.0
    V = BoxView(PSI, 0.0, k, 0.0, 0.0)
    a, b = 64.0, 40.0
    sides = [((0, -1), (0, 0), (1, 0)), ((1, 0), (1, 0), (1, 1)), ((0, 1), (1, 1), (0, 1)), ((-1, 0), (0, 1), (0, 0))]
    for (nu, nv), (i0, j0), (i1, j1) in sides:
        vis, lit = V.visible(nu, nv)
        if vis:
            pg.poly([[V(i0 * a, j0 * b, 0), V(i1 * a, j1 * b, 0), V(i1 * a, j1 * b, -SLAB_T_M),
                      V(i0 * a, j0 * b, -SLAB_T_M)]], fill=COL["soil"] if lit else COL["soil_dk"], stroke=COL["edge3d"],
                    lw=0.15)
    pg.poly([[V(0, 0, 0), V(a, 0, 0), V(a, b, 0), V(0, b, 0)]], fill=MP["agriculture"][0], stroke=COL["edge3d"], lw=0.15)
    for j in range(1, 4):
        pg.line([V(2, j * b / 4.0, 0), V(a - 2, j * b / 4.0, 0)], MP["agriculture"][1], 0.15)
    for u, v in [(i * a / 6.0 + 4.0, j * b / 4.0) for j in (3, 2, 1) for i in range(6)]:
        tree_at(pg, lambda x, y, z: V(x, y, z), k, u, v, opt, "olive", 2.4, 5.0, shadow=True)
    bb = items_bbox(pg.items)
    node(pg, bb[0] + 3.0, bb[3] + 4.0, 11, opt, 2.6)
    pg.text(u"EXISTING FARMLAND, OFF SITE", bb[0] + 7.0, bb[3] + 3.2, 2.4, COL["ink"], bold=True)
    pg.text(u"pictogram, not its shape or size", bb[0] + 7.0, bb[3] + 0.4, 1.8, COL["ink2"])
    return pg


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
    pg.text(u"one way, with the river " + cite(CONCEPT[1]), tx, y - 3.0, 2.0, COL["ink2"])
    pg.line([(x0, y0), (x1, y0)], COL["structure"], 0.3)


def draw_footer(pg, x0, y0, x1, pal_line, src_line):
    t = (u"measured = station/gauge · published = official/paper · calculated = our arithmetic · design value = chosen · "
         u"1-11 = the water's elements, same on every drawing. " + src_line)
    key = u"Sources by number: " + u"  ".join(u"[{}] {}".format(i + 1, k) for i, k in enumerate(SRC_KEY))
    n = len(wrap(t, 1.9, x1 - x0)) * 1.9 * 1.28 + len(wrap(key, 1.6, x1 - x0)) * 1.6 * 1.28
    y = para(pg, x0, y0 + 3.6 + n, x1 - x0, t, 1.9, COL["ink2"])    # v1.6: the numbered source key under it
    y = para(pg, x0, y, x1 - x0, key, 1.6, COL["ink2"])
    pg.text(u"{} · {} · {} · {}".format(CREDIT, COURSE, VERSION, pal_line), x0, y - 2.6, 1.9, COL["ink2"])


def build_board(opt, storage, parts, pal_line, log):
    pg = Page(BOARD_W, BOARD_H)
    pg.poly([rect(0, 0, BOARD_W, BOARD_H)], fill=COL["sheet"])
    X0, X1, G = M, BOARD_W - M, 4.0
    rows = [("title", 26.0), ("chain", 57.0), ("r1", 196.0), ("r2", 150.0), ("r3", 150.0), ("r4", 156.0),
            ("dec", 42.0)]
    y = BOARD_H - M
    Y = {}
    for k, h in rows:
        Y[k] = (y - h, y)
        y -= h + G
    draw_title(pg, X0, Y["title"][0], X1, Y["title"][1], opt, storage)
    # chain: who does what
    b = frame(pg, (X0, Y["chain"][0], X1, Y["chain"][1]), u"WHO DOES WHAT · one way, with the river")
    place(pg, parts["chain"], b, 1.4, "C", log, "chain")
    # row 1: the year | river height at the six cuts
    xs = X0 + 548.0
    b = frame(pg, (X0, Y["r1"][0], xs, Y["r1"][1]), u"THE YEAR OF THE WATER",
              u"Oct -> Sep, the gauges' water year · brackets = what the loop does")
    place(pg, parts["year"], b, 1.6, "C", log, "year of the water")
    b = frame(pg, (xs + G, Y["r1"][0], X1, Y["r1"][1]), u"HOW HIGH THE RIVER RISES",
              u"5 surveyed cuts + DSİ's planned channel · depth above the bed · worst-case roughness")
    place(pg, parts["sections"], b, 1.6, "C", log, "river height")
    # row 2: concept sections | planting bands
    xs = X0 + 700.0
    b = frame(pg, (X0, Y["r2"][0], xs, Y["r2"][1]), u"THE IDEA IN SECTION",
              u"problem -> one move · upstream entry, K4 · numbers as in the chain · schematic, relative levels, not to scale")
    half = (b[2] - b[0] - 6.0) / 2.0
    place(pg, parts["concept_up"], (b[0], b[1], b[0] + half, b[3]), 1.6, "C", log, "concept upstream")
    place(pg, parts["concept_k4"], (b[0] + half + 6.0, b[1], b[2], b[3]), 1.6, "C", log, "concept K4")
    b = frame(pg, (xs + G, Y["r2"][0], X1, Y["r2"][1]), u"PLANTING BANDS BY DAYS UNDER WATER (7)",
              u"proposal · band heights provisional · species + evidence")
    place(pg, parts["bands"], b, 1.6, "C", log, "planting bands")
    # row 3: the S4 detail | the seasons
    xs = X0 + 820.0
    b = frame(pg, (X0, Y["r3"][0], xs, Y["r3"][1]), u"THE FLAT DOWNSTREAM END IN DETAIL · S4 · 1:{:,.0f}".format(
        DETAIL_SCALE), u"one real cut, both banks · every season's water level · drawn: summer, strip, full leaf")
    s, _ = place(pg, parts["detail"], b, 1.0, "C", log, "S4 detail")
    if s < 0.999:
        log.append(u"NOTE: the S4 detail is printed at {:.0f} % of 1:{:,.0f}, so about 1:{:,.0f}".format(
            100 * s, DETAIL_SCALE, DETAIL_SCALE / s))
    b = frame(pg, (xs + G, Y["r3"][0], X1, Y["r3"][1]), u"THE SEASONS ON THIS CUT")
    place(pg, parts["seasons"], b, 1.6, "C", log, "seasons")
    # row 4: storage | cleaning | where the water goes
    w3 = (X1 - X0 - 2 * G) / 3.0
    # v1.6: the cubes at a true scale: the first of CUBE_SCALES at which they fit, printed at 100 % (v1.3 enlarged
    # them up to 1.8 x while saying 1:1,000)
    box4 = (X0, Y["r4"][0], X0 + w3, Y["r4"][1])
    t4 = u"HOW MUCH TO STORE FOR THE SUMMER STRIP (4)"
    b0 = frame(Page(1, 1), box4, t4, u"to scale: cubes at 1:1,000")
    for sc_ in CUBE_SCALES:
        globals()["CUBE_SCALE"] = sc_
        cp = draw_storage_cubes(opt)
        bb = items_bbox(cp.items)
        if bb[2] - bb[0] <= b0[2] - b0[0] and bb[3] - bb[1] <= b0[3] - b0[1]:
            break
    b = frame(pg, box4, t4, u"to scale: cubes at 1:{:,.0f}".format(CUBE_SCALE))
    cs, _ = place(pg, cp, b, 1.0, "C", log, "storage cubes")
    if cs < 0.999:
        log.append(u"NOTE: the storage cubes are printed at {:.0f} % of 1:{:,.0f}".format(100 * cs, CUBE_SCALE))
    b = frame(pg, (X0 + w3 + G, Y["r4"][0], X0 + 2 * w3 + G, Y["r4"][1]), u"WHY AND HOW WE CLEAN (2)",
              u"in -> reed beds remove -> what is left")
    fit_draw(pg, draw_cleaning, b)
    b = frame(pg, (X0 + 2 * (w3 + G), Y["r4"][0], X1, Y["r4"][1]), u"WHERE THE CLEAN WATER GOES (10, 11)",
              u"farms outside · aquifer · not for drinking")
    split = b[0] + (b[2] - b[0]) * 0.64
    fit_draw(pg, boxed(draw_farms_text), (b[0], b[1], split, b[3]))
    place(pg, parts["farm"], (split + 3.0, b[1], b[2], b[3]), 1.4, "C", log, "farm pictogram")
    # what the figures support
    x0, x1 = X0, X1
    y1 = Y["dec"][1]
    h = Y["dec"][1] - Y["dec"][0]
    draw_decision(pg, x0, y1, x1 - x0, h, fit(draw_decision, x0, y1, x1 - x0, h, 1.0, 0.5, 1.2))
    draw_footer(pg, X0, 1.5, X1, pal_line, parts["src"])
    return pg


# ---------------------------------------------------------------- run
def out_folder(doc):
    # v1 24 Oct: all files under Downloads/Bergama/ (Aras rule); was next to the .3dm / .gh, else Documents
    return os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "output", OUT_FOLDER)


DATA_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "Data")   # 25 Oct: every data file here


#@include ../common/search_dirs.py


def build_all(doc, log):
    pal_line = load_palette([DATA_DIR] + search_dirs(doc), log) if doc is not None else u"embedded palette v1.4 colours"
    folder = out_folder(doc)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    detail = draw_detail(log)                       # the same for both options
    seasons = draw_season_table()
    src_line = (u"Sources: " + CM + u", " + RR + u" and tables, " + WD + u", " + REG + u", " + CR +
                u", bergama_plant_data_v1.json; scripts merged: water loop v2, water case v1.1, rain_river charts, "
                u"pr1 drawings v3.1, detail section v2, plant analysis v1 (panels 7-8).")
    files = []
    for opt in OPTIONS:
        parts = {"chain": draw_chain(opt), "year": draw_year(opt), "sections": draw_sections(opt),
                 "concept_up": draw_concept("up", opt), "concept_k4": draw_concept("k4", opt),
                 "bands": draw_bands(opt), "detail": detail, "seasons": seasons,
                 "farm": draw_farm_picto(opt), "src": src_line}
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
            files.append(path)
            log.append(u"{}  {}  {:.1f} s".format(os.path.basename(path), datetime.datetime.now().strftime("%H:%M:%S"),
                                                   time.time() - t0))
    return folder, files


def main():
    btn, on = button_state()
    pressed = (on and not mem_get("prev", False)) or chain_fire(_GH_IN.get(btn), "chain_seen", btn)
    globals()["_ran_now"] = pressed
    mem_set("prev", on)
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
