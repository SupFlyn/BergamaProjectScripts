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

NEW IN v1.13 (Aras 26 Oct 08:27, booklet p.14 "too lean information wise"): the storage panel's eight figures and
their keywords are drawn 1.8 x larger (they printed at about 3 pt beside the cubes); nothing else changed.

NEW IN v1.12 (Aras's booklet review, 26 Oct 07:06): the sheet is a 3 x 3 grid of panels, each the size of one A3
booklet page, so each booklet page is one panel at about 1:1 (drawings whole, at their own round scale):
  * every panel opens with a short context line (what it shows, why, what to take from it), inside its booklet crop;
  * who does what: one continuous stream ribbon with the four stations on it (was three boxes in a row, cut in three);
  * what the figures support: the seven steps clockwise round a rectangle, the red closing arrow = the next winter's
    stream refilling the storage (one way, nothing pumped back);
  * the S4 seasons: one row a season stacked at 1:250 (one crop), titles clear of their colour bars, less soil under
    the cut, the scale bar once;
  * the S4 north-east bank: the same bank at 1:200 in winter with its water and Q100 / Q500 added under the summer cut;
  * the six cuts cropped to the bed with what each level means; the planting bands in the hand-sketch language of the
    concept sections, the species as one list with each warning on its own row.
NEW IN v1.11 (Aras 26 Oct 06:35 "we dont want scales like 1:7329 ... they need to be round numbers"): every drawing
on the sheet takes the largest ROUND scale at which it fits: the six cuts 1:250 / 1:500 / 1:1,000 / 1:2,000 (was up
to 1:400), the S4 seasons 1:250 / 1:500 / 1:1,000, the planting bands 1:200 / 1:250 / 1:500 / 1:1,000, the storage
cubes 1:1,000 / 1:2,000 / 1:2,500 / 1:5,000 (was 1:1,250 or 1:1,500).
NEW IN v1.10 (Aras 25 Oct 21:47-22:02: the booklet = crops of the sheet; no caveat notes; "not stretch anything ever"):
  * Booklet: the separate booklet drawings are gone; output/bergama_water_board/booklet/blocks.json lists one crop per
    panel of this board (rects from the board's own layout) and results.json keeps v1.9's keys.
  * Caveat notes removed from the sheet (labels kept); "stream", never "river", in every visible word.
  * W2 stream height: the six cuts at one true scale, 1:250 across and up (was vertical x8).
  * S4: one row per season (south-west bank and bed, 1:250, drawn by the detail engine in that season's look) with its
    water levels and depths, the season's words on the drawing and one kind of detail per row (winter flood levels,
    spring planting bands + species, summer levels + widths, autumn materials); the north-east bank stays at 1:200.
  * W3b planting bands: drawn on the surveyed S4 ground at 1:250 in the site board's section language (src/common/
    section_style.py): days a year under water along the ground (this cut's own figures), Q100 / Q500, whole plants,
    the bands A-F as bars under the classes their days overlap.
OLDER VERSIONS: their notes are in HISTORY.md (repo SupFlyn/BergamaProjectScripts, src/bergama_water_board/).

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

VERSION = "bergama_water_board v1.13 (2026-10-26)"
SHORT = "v1.13"
BUTTON_WORDS = ("build", "bake", "run", "go", "press", "button", "start")
BOARD_W, BOARD_H = 1189.0, 841.0     # A0 landscape, mm
M = 14.0                             # board margin, mm
OPTIONS = ("A",)                     # v1.7: option A only (organic only where the project meets the water), Aras 16:43
STORAGE_STYLES = ("cubes",)          # v1.6: cubes only (Aras 25 Oct 13:12; the chart is gone)
CUBE_SCALE = 1000.0                  # the storage cubes are drawn at 1:1,000 ...
CUBE_SCALES = (1000.0, 2000.0, 2500.0, 5000.0)   # ... v1.6: or the first of these at which they fit (v1.11: round)
OUT_FOLDER = "bergama_water_board"
OUT_NAME = "Bergama_water_board_v1_13_{}_{}.pdf"
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
CONCEPT_CHIPS = [("rain", u"STREAM IN"), ("reed", u"CLEAN ONCE · UPSTREAM (ARAS)"), ("cube", u"HOLD WINTER WATER"),
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
ROUTE_OUT = (u"worst case: no stream inflow May-Oct", u"calculated case; " + CM + u" §4")


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


#@include ../common/section_style.py


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
CHAIN = [
    (u"ARAS", "aras_alan", u"upstream entry", u"CLEANS · HOLDS · STORES",
     [(2, u"reed beds clean the inflow"), (3, u"terraces hold street + roof runoff"),
      (4, u"planted basins store winter water"), (5, u"spillway: overflow back to the stream")]),
    (u"BEGÜM", "begum_alan", u"K4 bridge", u"LIVES WITH THE WATER",
     [(7, u"strip waters the bank planting"), (8, u"floods spread onto terraces"),
      (9, u"people on the raised dry top · Roman bridge kept")]),
    (u"BEGÜM", "begum_alan", u"K5 bridge", u"LIVES WITH THE WATER",
     [(7, u"bank planting on the strip"), (8, u"flood terraces"), (9, u"raised dry top"),
      (None, DG_LINE)]),
    (u"NİL", "nil_alan", u"downstream end", u"GIVES BACK",
     [(None, u"no treatment: arrives clean"), (10, u"clean stream leaves the site"),
      (11, u"to existing farmland outside")]),
]
CHAIN_LINKS = [u"STRIP 4 m x 0.30 m · one way · stream above the legal minimum flow · storage tops up May-Oct",
               u"strip and clean stream", u"strip and clean stream"]
CHAIN_SRC = (u"Aras 2026-10-18 14:29 (one way, cleaned once at the upstream end, no treatment at the downstream end), "
             u"14:49 and 15:02 (no farmland inside the site); strip: design values, " + RR + u" §4; minimum flow: "
             u"\"at least 10 %\" of the 10-year mean, HES water-use-rights regulation Art. 15/1, RG 15.06.2019 no. "
             u"30802; spillway: " + RR + u" §4 fail-safes; " + CR + u" D8")


def draw_chain(opt):
    """v1.12 (Aras 26 Oct 07:06 "don't divide the who does what chain into three rows ... one continuous diagram"): one
    stream ribbon from the inflow (1) to the farmland (11), the four stations hung on it in water order, above and
    below it in turn, so the whole chain fits one A3 page as one piece."""
    pg = Page(0, 0)
    W, rh = 372.0, 4.6                       # ribbon length and half its width, mm
    bw, stem = 128.0, 7.0
    sx = [24.0, 98.0, 172.0, 246.0]          # where each station meets the ribbon
    fs, fv, fw = 2.6, 3.2, 4.4
    lines = max(len(c[4]) for c in CHAIN)
    bh = 9.0 + fv + 3.0 + lines * 4.9 + 1.5
    # the stream: one ribbon, one way, ending in an arrow head at the farmland
    pg.poly([[(0.0, -rh), (W - 9.0, -rh), (W - 9.0, -rh - 2.6), (W, 0.0), (W - 9.0, rh + 2.6), (W - 9.0, rh),
              (0.0, rh)]], fill=MP["discharge"][0], stroke=MP["discharge"][1], lw=0.3)
    node(pg, 5.0, 0.0, 1, opt, 3.4)
    pg.text(u"STREAM INFLOW", 0.0, -rh - 5.0, 2.8, COL["ink"], bold=True)
    chips(pg, 0.0, -rh - 6.2, [("rain", u"catchment rain"), ("days", u"mostly winter")], 2.3, 70.0, COL["ink2"])
    # the strip along the ribbon: what links one station to the next, written in the water
    node(pg, sx[0] + 9.0, 0.0, 6, opt, 2.6)
    lx = [sx[0] + 13.0, sx[1] + 50.0, sx[2] + 50.0]
    for i, t in enumerate(CHAIN_LINKS):
        if i == 0:
            t = t.replace(u"STRIP ", u"")
        pg.text(t, lx[i], -fs * 0.36, 2.2, MP["discharge"][2], bold=True)
    for i, (who, key, place_, verb, does) in enumerate(CHAIN):
        up = i % 2 == 0
        x0 = sx[i] - 14.0
        y0, y1 = (rh + stem, rh + stem + bh) if up else (-rh - stem - bh, -rh - stem)
        pg.line([(sx[i], rh if up else -rh), (sx[i], y0 if up else y1)], COL[key], 0.6)
        pg.circle(sx[i], rh if up else -rh, 1.1, fill=COL[key])
        pg.poly([rect(x0, y0, x0 + bw, y1)], fill=COL["white"], stroke=COL[key], lw=0.5)
        tw = text_w(who, fw, True)
        pg.poly([rect(x0, y1 - 8.0, x0 + tw + 6.0, y1)], fill=COL[key])
        pg.text(who, x0 + 3.0, y1 - 6.0, fw, COL["white"], bold=True)
        pg.text(place_, x0 + tw + 9.0, y1 - 5.8, fs, COL[key], bold=True)
        pg.text(verb, x0 + 3.0, y1 - 13.2, fv, COL["ink_dark"], bold=True)
        yy = y1 - 13.2 - fv - 2.2
        for n_, t in does:
            if n_:
                node(pg, x0 + 5.4, yy + 0.9, n_, opt, 2.4)
            pg.text(t, x0 + 10.0, yy, fs, COL["ink"])
            yy -= 4.9
    # 10-11: the clean stream leaves the site for the farmland outside
    node(pg, W - 18.0, rh + 12.0, 11, opt, 3.4)
    pg.text(u"EXISTING FARMLAND", W - 22.0, rh + 19.0, 2.8, COL["ink"], bold=True, align="R")
    chips(pg, W - 70.0, rh + 10.0, [("out", u"outside the site")], 2.3, 60.0, COL["ink2"])
    pg.text(u"Sources: " + cite(CHAIN_SRC), 0.0, -rh - 22.0, 2.0, COL["ink2"])
    return pg


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
    figs(pg, rx, ys + 9.0, [(u"0.15 Mm³ = 1/136", u"of the stream: the stream, not local rain, fills the storage")],
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
    figs(pg, rx, ly - 0.5, [(u"Jul-Sep: few cm / dry", u"the strip needs stored water")], 64.0, big=2.6)
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
SECT_FS = 2.5                                   # labels, mm
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
    head = u"bed {:+.2f} · ".format(cut["bed"]) if cut.get("bed") is not None else u""
    w_txt = w_txt or (X1 - X0 + 20.0)
    if cut.get("bed") is not None:
        y = para(pg, x0, y + fs * 1.28, w_txt, head + u"{:.0f} of {:.0f} m shown · looking upstream".format(
            xr - xl, len(g) - 1.0), fs, COL["ink2"])
    tags = [t for t in cut["tags"] if t[0] not in ("points", "flag")]       # v1.10: no survey caveats on the sheet
    return chips(pg, x0, y - 1.2, tags, fs, w_txt)     # v1.8: notes as chips


def draw_level_key(pg, x, y, w, kx):
    """What each level means for the design: a ladder of sample lines (Q500 at the top) with the W / F / D zone bar at
    the left, the depth range on the five surveyed cuts, and the meaning in keywords with its sources. Returns bottom y."""
    fs = SECT_FS
    pg.text(u"WHAT EACH LEVEL MEANS FOR THE DESIGN", x, y - 3.2 * CAP, 3.2, COL["ink_dark"], bold=True)
    pg.text(u"depth over the bed on the five surveyed cuts · DSİ = the planned channel", x + text_w(
        u"WHAT EACH LEVEL MEANS FOR THE DESIGN", 3.2, True) + 4.0, y - 3.2 * CAP, fs, COL["ink2"])
    y -= 3.2 + 3.0
    surveyed = [c for c in CUTS if c.get("bed") is not None]
    dsi = [c for c in CUTS if c["key"] == "dsi"]
    xs, xn, xr_, xm = x + 9.0, x + 22.0, x + 72.0, x + 112.0
    rows = []
    for i in range(len(EVENTS) - 1, -1, -1):
        zone, mean, srcs = LEVEL_MEAN[i]
        y0 = y
        lo, hi = min(c["dep"][i] for c in surveyed), max(c["dep"][i] for c in surveyed)
        rng = u"{:.2f}-{:.2f} m".format(lo, hi) + (u" · DSİ {:.2f}".format(dsi[0]["dep"][i]) if dsi else u"")
        pg.line([(xs, y - fs * 0.35), (xs + 10.0, y - fs * 0.35)], LEVEL_COL[i], 0.7 if i >= 3 else 0.45)
        pg.text(EVENTS[i], xn, y - fs * CAP, fs, LEVEL_COL[i] if i else C["w3"], bold=True)
        pg.text(rng, xr_, y - fs * CAP, fs, COL["ink2"])
        yy = para(pg, xm, y + fs * (1.28 - CAP), x + w - xm,
                  mean + u" " + u"".join(cite(s) for s in srcs), fs, COL["ink"])
        y = min(y - fs * 1.28, yy) - 2.2
        rows.append((zone, y0, y))
    # the zone bar: one colour block per zone over its rows, the letter on it
    for zone in ("D", "F", "W"):
        zr = [(a, b) for z, a, b in rows if z == zone]
        if not zr:
            continue
        ya, yb = max(a for a, _ in zr) , min(b for _, b in zr) + 1.0
        pg.poly([rect(x, yb, x + 5.0, ya)], fill=ZONE_COL[zone])
        pg.text(zone, x + 2.5, (ya + yb) / 2.0 - 3.0 * CAP / 2.0, 3.0, COL["ink_dark"], bold=True, align="C")
    return y


def scale_bar(pg, x, y, kx, den):
    """0-5-10-20 m bar at kx mm per m, its scale and the drawing rule beside it. Returns bottom y."""
    fs = SECT_FS
    for a, b, f in ((0, 5, COL["ink"]), (5, 10, COL["white"]), (10, 20, COL["ink"])):
        pg.poly([rect(x + a * kx, y - 1.2, x + b * kx, y)], fill=f, stroke=COL["ink"], lw=0.15)
    for m in (0, 5, 10, 20):
        pg.text(u"{}".format(m), x + m * kx, y - 1.2 - 1.0 - fs * CAP, fs, COL["ink2"], align="C")
    pg.text(u"m", x + 20 * kx + 2.0, y - 1.2 - 1.0 - fs * CAP, fs, COL["ink2"])
    pg.text(u"1:{} · true proportions, no vertical exaggeration · each cut cropped {:.0f} m outside Q500 (break "
            u"marks) · method {}".format(den, SECT_MARGIN, cite(SECT_SRC)), x + 20 * kx + 7.0, y - 1.2, fs, COL["ink2"])
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
    y = draw_level_key(pg, 0.0, y, max(right, 300.0), kx) - 2.0
    scale_bar(pg, 0.0, y, kx, den)
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
S4_DENS = (250.0, 500.0, 1000.0)     # the S4 season rows: the first scale at which all four fit their cells (v1.11: round)


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


def engine_section(E, d, prof, sea_key, scale, skip_z=(), drop=(), poche=None):
    """One S4 bank drawn by the detail engine at 1:scale in the look of one season. Level lines at the heights in
    skip_z are left out; items on the layers in drop are left out; poche = depth of the cut soil under the strip, m
    (v1.12; None = the engine's 1.9 m). Returns (board items, the engine's Sec)."""
    keep = (E["SCALE"], E["K"], dict(E["SEA"]), E["level_line"])
    lay = {"poly": 6, "line": 5, "circle": 7, "text": 8}
    orig = E["level_line"]

    def ll(pg, S, z, label, dash, colour=E["FLOOD"]):
        if any(abs(z - q) < 1e-6 for q in skip_z):
            return
        orig(pg, S, z, label, dash, colour)
    try:
        E["SCALE"], E["K"] = scale, 1000.0 / scale
        E["level_line"] = ll
        E["SEA"].clear()
        E["SEA"].update(E["SEASON_LOOK"][sea_key])
        sea = [s for s in E["SEASONS"] if s["key"] == sea_key][0]
        pg = E["Page"]("s4", sea_key)
        S = E["Sec"](d, prof)
        if poche is not None:
            S.zb = E["THALWEG"][1] - E["STRIP"][2] - poche
        E["draw_section"](pg, S, 0.0, 0.0, [], sea)
    finally:
        E["SCALE"], E["K"] = keep[0], keep[1]
        E["SEA"].clear()
        E["SEA"].update(keep[2])
        E["level_line"] = keep[3]
    k = 1000.0 / scale                      # S keeps this drawing's scale after the engine's K is set back
    S.X = lambda s_: S.X0 + (s_ - d["s_from"]) * S.dir * k
    S.Y = lambda z_: S.Y0 + (z_ - S.zb) * k
    S.P = lambda s_, z_: (S.X(s_), S.Y(z_))
    return from_engine([it for it in pg.items if it[lay[it[0]]] not in drop]), S


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


BK_GROW = 1.45                       # room kept round each label for the booklet (its words reset at >= 7.5 pt)


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


S4_SCALE = 250.0                     # v1.10: the season rows of the S4 cut (south-west bank), 1:250
S4_NE_SCALE = 200.0                  # the north-east bank, 1:200 (as the v1.9 detail)
S4_FS = 2.2                          # label size on the season rows, mm
S4_POCHE = 0.9                       # v1.12: soil drawn under the strip on the season rows, m (the engine's is 1.9)
# v1.10 (Aras 21:51, "in page 19 we can get into more detail"): each season row carries its own water and a few season
# words where they happen (from the S4 season texts of the detail section v2), and one kind of detail: winter the
# flood levels, spring the planting bands and species, summer the levels and widths, autumn the materials.
S4_SEASON = {
    "winter": dict(head=u"storage fills", water=[u"Jan-Feb mean", u"highest day 2017"],
                   words=[(586.0, None, u"marsh flooded · birds"), (563.0, None, u"terraces open between storms"),
                          (541.0, 50.6, u"plane bare, seed balls")]),
    "spring": dict(head=u"storage full by end of April", water=[u"Mar-Apr low end", u"Jan-Apr high end"],
                   words=[(563.0, None, u"boardwalk open"), (592.0, None, u"strip on the stream")]),
    "summer": dict(head=u"strip runs on stored water", water=[],
                   words=[(589.85, None, u"wading 0.30 m · feet in water")]),
    "autumn": dict(head=u"storage low until the rains", water=[u"Oct-Dec high end"],
                   words=[(582.0, 45.6, u"reeds gold · seed heads"), (592.0, None, u"first-flush cleaning")],
                   extra=u"design storm 137 mm a day"),
}
S4_MONTHS = {"winter": u"Dec-Feb", "spring": u"Mar-May", "summer": u"Jun-Aug", "autumn": u"Sep-Nov"}
# spring: the planting band (W3b letters) and species of each planted part of the south-west bank: the species the
# design names there (detail section v2 callouts), as listed in SPECIES
S4_PLANTING = [(541.0, 50.0, [u"E · Platanus orientalis"]), (549.5, None, [u"F · Lavandula stoechas"]),
               (568.2, 45.6, [u"C · Tamarix smyrnensis", u"C · Vitex agnus-castus"]),
               (582.5, 45.2, [u"B · reeds, Iris pseudacorus"]), (559.0, 46.9, [u"flood- + drought-tolerant"])]


def draw_s4_season(key, log=None, scale=None, bar=True):
    """One season of the S4 cut, south-west bank and bed, at 1:250: the season's water hatched and its levels at the
    right, the season's words on the drawing, and that row's detail (see S4_SEASON). v1.12: a shallower soil cut and the
    scale bar only where bar is set (the last row), so the four rows fit one A3 page at 1:250 with room between them."""
    scale = scale or S4_SCALE
    E = detail_engine()
    prof = s4_profile(E, log)
    d = E["SECTIONS"][0]
    bed, q100, q500 = E["THALWEG"][1], E["Q100"], E["Q500"]
    skip = () if key == "winter" else (q100, q500)
    items, S = engine_section(E, d, prof, key, scale, skip, ("title", "callouts", "dimensions", "band", "survey",
                                                              "text"), S4_POCHE)
    pg = Page(0, 0)
    pg.items = items
    sea = [s for s in E["SEASONS"] if s["key"] == key][0]
    info = S4_SEASON[key]
    fs = S4_FS
    xl, xr = S.X(d["s_from"]), S.X(d["s_to"])
    bb = items_bbox(items)
    y_cap = bb[3]
    boxes = []
    # left: the season, its months and what the storage does
    cx = xl - 44.0
    pg.poly([rect(cx, y_cap - 2.4, cx + 30.0, y_cap - 1.4)], fill=BAND_BLUE[["winter", "spring", "summer",
                                                                            "autumn"].index(key)])
    pg.text(sea["name"], cx, y_cap - 8.6, 5.0, COL["ink_dark"], bold=True)     # v1.12: clear of the colour bar
    pg.text(S4_MONTHS[key], cx, y_cap - 12.8, fs, COL["ink2"], bold=True)
    pg.text(info["head"], cx, y_cap - 16.4, fs, MP["discharge"][2], bold=True)
    if info.get("extra"):
        pg.text(info["extra"], cx, y_cap - 19.8, fs, MP["discharge"][2])
    # right: the season's water and (winter) the flood levels, with their height above the bed low point
    lv = [(S.Y(bed), u"{:+.2f} · bed low point".format(bed), COL["ink"], False)]
    names = info["water"]
    for i, w in enumerate(sea["water"]):
        lv.append((S.Y(w[0]), u"{:+.2f} · {:.2f} m · {}".format(w[0], w[0] - bed, names[i] if i < len(names) else u""),
                   E["FLOOD"], i == 0))
    if sea["strip_held"] and not [w for w in sea["water"] if w[1]]:
        lv.append((S.Y(bed) + 0.01, u"strip {:.1f} m x {:.2f} m".format(abs(E["STRIP"][1] - E["STRIP"][0]),
                                                                    E["STRIP"][2]), E["FLOOD"], True))
    if key == "winter":
        lv += [(S.Y(q100), u"{:+.2f} · {:.2f} m · Q100".format(q100, q100 - bed), E["FLOOD"], True),
               (S.Y(q500), u"{:+.2f} · {:.2f} m · Q500".format(q500, q500 - bed), E["FLOOD"], True)]
    level_ladder(pg, lv, xr + 0.5, xr + 6.0, fs, boxes, lo=bb[1] + 1.0)
    labs = []
    for s, z, t in info["words"]:
        labs.append((S.X(s), S.Y(z if z is not None else S.surf(s) + 0.05), [t], COL["ink"], False))
    if key == "winter":
        labs.append((S.X(552.5), S.Y(E["DRY"]), [u"raised walk {:+.2f}".format(E["DRY"]),
                                                 u"{:.2f} m above Q500".format(E["DRY"] - q500)], E["FLOOD"], True))
    elif key == "spring":
        for s, z, ts in S4_PLANTING:
            labs.append((S.X(s), S.Y(z if z is not None else S.surf(s) + 0.3), ts, "495338", True))
    elif key == "summer":
        seen = set()
        for sa, sb, z, mat, lab in S.flats:
            if z is None or round(z, 2) in seen or abs(z - 47.20) < 1e-6:
                continue
            seen.add(round(z, 2))
            sa, sb = max(((a_, b_) for a_, b_, z_, m_, l_ in S.flats if z_ is not None and abs(z_ - z) < 1e-6),
                         key=lambda t: (abs(t[1] - t[0]), t[0]))     # its widest part (ties: the one nearer the bed)
            sm = (sa + sb) / 2.0
            X, Y = S.P(sm, z)
            pg.poly([[(X - 0.9, Y + 1.5), (X + 0.9, Y + 1.5), (X, Y)]], fill=None, stroke=COL["ink"], lw=0.15)
            labs.append((X, Y + 1.5, [u"{:+.2f}".format(z)], COL["ink"], True))
        bt = [m for m in E["SURVEY_MARKS"] if m[1] == "spot height" and abs(m[0] - 561.93) < 0.01]
        if bt:
            labs.append((S.X(bt[0][0]), S.Y(bt[0][2]), [u"survey bank top {:+.2f}".format(bt[0][2])], COL["ink2"],
                         False))
        # widths: the design's surfaces, the regraded bank, the bed and the strip, in metres under the cut
        bounds = sorted(set(round(b, 3) for sa, sb, z, mat, lab in S.flats for b in (sa, sb)) |
                        {round(d["regrade"][1], 3), E["STRIP"][0], E["STRIP"][1], round(d["s_to"], 3)})
        bounds = [b for b in bounds if S.lo <= b <= S.hi]
        yd = S.Y(S.zb) - 3.5
        pg.line([(S.X(bounds[0]), yd), (S.X(bounds[-1]), yd)], E["DIM"], 0.12)
        for b in bounds:
            pg.line([(S.X(b) - 0.6, yd - 0.6), (S.X(b) + 0.6, yd + 0.6)], E["DIM"], 0.2)
        for a, b in zip(bounds[:-1], bounds[1:]):
            pg.text(u"{:.1f}".format(b - a), (S.X(a) + S.X(b)) / 2.0, yd - 3.0, fs * 0.9, E["DIM"], align="C")
        pg.text(u"m", S.X(bounds[-1]) + 1.5, yd - 3.0, fs * 0.9, E["DIM"])
    elif key == "autumn":
        best = {}
        for sa, sb, z, mat, lab in S.flats:
            if z is None:
                continue
            if lab not in best or abs(sb - sa) > abs(best[lab][1] - best[lab][0]):
                best[lab] = (sa, sb, z)
        for lab, (sa, sb, z) in best.items():
            sm = (sa + sb) / 2.0
            labs.append((S.X(sm), S.Y(z + 0.02), [lab.lower()], "6B4A36", False))
        labs.append((S.X(574.5), S.Y(S.surf(574.5) + 0.02), [u"stream gravel"], "6B4A36", False))
        labs.append((S.X(553.85), S.Y(E["DRY"] + 1.10), [u"handrail corten steel"], "6B4A36", False))
    sky_labels(pg, labs, items, xl, xr + 60.0, y_cap, fs, boxes)
    if not bar:
        return pg
    # scale bar, 10 m
    k = 1000.0 / scale
    yb = S.Y(S.zb) - (8.5 if key == "summer" else 3.0)
    x0 = xl
    pg.poly([rect(x0, yb, x0 + 5.0 * k, yb + 0.8)], fill=COL["ink"])
    pg.poly([rect(x0 + 5.0 * k, yb, x0 + 10.0 * k, yb + 0.8)], fill=COL["white"], stroke=COL["ink"], lw=0.12)
    pg.text(u"10 m · 1:{:,.0f}".format(scale), x0 + 10.0 * k + 1.5, yb, fs * 0.85, COL["ink2"])
    return pg


def draw_s4_ne(log):
    """The north-east bank of the S4 cut at 1:200, summer, with the engine's callouts, widths, materials and levels,
    and the flood levels at its left."""
    E = detail_engine()
    prof = s4_profile(E, log)
    keep = (E["SCALE"], E["K"])
    E["SCALE"], E["K"] = S4_NE_SCALE, 1000.0 / S4_NE_SCALE
    try:
        E["SEA"].clear()
        E["SEA"].update(E["SEASON_LOOK"]["summer"])
        sea = dict(E["SEASONS"][2])
        pg = E["Page"]("detail", "S4")
        S = E["Sec"](E["SECTIONS"][1], prof)
        del E["_LV"][:]
        notes = []
        E["draw_section"](pg, S, 0.0, 0.0, notes, sea)
        lv = sorted(E["_LV"], key=lambda e: e[0])
        xl = S.X0 - 4.0
        ys = [S.Y(z) for z, _, _, _ in lv]
        ly = spread(ys, 2.3)
        for (z, lab, colour, dash), Y, Yl in zip(lv, ys, ly):
            pg.line([(xl + 2.5, Y), (xl - 1.0, Y), (xl - 3.0, Yl + 0.6), (xl - 4.0, Yl + 0.6)], colour, 0.15,
                    layer="ladder")
            t = u"{:+.2f}  {}".format(z, lab.replace(u"%+.2f" % z, u"").replace(u"(calculated on this cut)", u"")
                                       .replace(u"(design)", u"").replace(u"  ", u" ").strip(u" ,;"))
            pg.text(t, xl - 4.4, Yl, 1.7, colour if colour != E["WATER_LINE"] else E["FLOOD"], align="R",
                    layer="ladder")
    finally:
        E["SCALE"], E["K"] = keep
    for n_ in notes:
        log.append(u"S4 detail: " + n_)
    out = Page(0, 0)
    out.items = from_engine([it for it in pg.items if it[0] != "text" or it[8] != "title"])   # the frame names it
    return out


def draw_s4_ne_winter(log):
    """v1.12 (Aras 26 Oct 07:06, p.28 "too much empty space ... enlarge or add content"): the same north-east bank at the
    same 1:200 in its winter look, with the winter water and Q100 / Q500 as level lines and their levels at the right: which of its surfaces the floods reach (this cut's own levels)."""
    E = detail_engine()
    prof = s4_profile(E, log)
    d = E["SECTIONS"][1]
    bed, q100, q500 = E["THALWEG"][1], E["Q100"], E["Q500"]
    items, S = engine_section(E, d, prof, "winter", S4_NE_SCALE, (), ("title", "callouts", "dimensions", "band",
                                                                      "survey", "text"), S4_POCHE)
    pg = Page(0, 0)
    pg.items = items
    sea = [s_ for s_ in E["SEASONS"] if s_["key"] == "winter"][0]
    xr = max(S.X(d["s_from"]), S.X(d["s_to"]))
    lv = [(S.Y(bed), u"{:+.2f} · bed low point".format(bed), COL["ink"], False)]
    names = S4_SEASON["winter"]["water"]
    for i, w in enumerate(sea["water"]):
        lv.append((S.Y(w[0]), u"{:+.2f} · {}".format(w[0], names[i] if i < len(names) else u""), E["FLOOD"], i == 0))
    lv += [(S.Y(q100), u"{:+.2f} · Q100".format(q100), E["FLOOD"], True),      # depths over the bed: the seasons'
           (S.Y(q500), u"{:+.2f} · Q500".format(q500), E["FLOOD"], True)]      # winter row (the same cut)
    level_ladder(pg, lv, xr + 0.5, xr + 6.0, S4_FS, None, lo=items_bbox(items)[1] + 1.0)
    return pg


def s4_days(E):
    """S4's days a year at or above each height (the detail section's DAYS_WET, this cut's own): [(m, days, under)],
    and the days the bed is dry."""
    import re as _re
    t = E["DAYS_WET"]
    rows = [(float(h), int(n), bool(u)) for h, u, n in _re.findall(r"(\d+\.\d+) m (under )?(\d+) d", t)]
    m = _re.search(r"about (\d+) d", t)
    return rows, (int(m.group(1)) if m else None)


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
CONCEPT_FILE = "concept/Selinos_riverfront_design_concept_v1.md"
C_PL = dict(green_deep="495338", green_mid="727A4E", accent="8B3A3F", ink="4A3F35", ink2="847E75", structure="B0AC9C")

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
               u"calls these ranges, not fixed limits. Z1–Z4 = bank zones of research file 04 (its own reading).")
# species: band, latin, local name, evidence (quoted or summarised from the named file, with its source), flag
#@include data/SPECIES.py
SPECIES_SRC = {"C": u"concept v1 §9.2", "R": u"research 04 species matrix", "C+R": u"concept v1 §9.2 + research 04"}


BANDS_DENS = (200.0, 250.0, 500.0, 1000.0)   # v1.11 round; v1.10: the planting bands on the S4 ground, the first of these scales that fits
BANDS_S = (566.0, 634.0)             # the part of S4 drawn: both banks and the bed, to the north-east road (m along S4)
# W3b band -> its days a year under water (RWS ranges, PLANT_BANDS); A is the strip itself (permanent)
BAND_DAYS = {"B": (150.0, 365.0), "C": (50.0, 150.0), "D": (10.0, 150.0), "E": (0.5, 50.0), "F": (0.0, 0.5)}
DAYS_COL = ["1B535E", "4B92A3", "90C5D2", "C1D3DB", "E4EEF0", "F4F3EE"]   # wettest -> dry


def s4_classes(E):
    """The S4 ground split by how many days a year the water reaches it (the cut's own figures): [(h_lo, h_hi, days
    lo, days hi, label)] by height above the bed low point; the last two: up to Q500, above it."""
    rows, _dry = s4_days(E)
    bed, q500 = E["THALWEG"][1], E["Q500"]
    out, prev_h, prev_d = [], 0.0, 365.0
    for h, n, under in rows:
        lo = 0.0 if under else float(n)
        out.append((prev_h, h, lo if not under else 0.0, prev_d,
                    (u"> {} d".format(n) if not out else (u"{}-{} d".format(n, int(prev_d)) if not under else
                                                         u"< {} d".format(int(prev_d))))))
        prev_h, prev_d = h, (float(n) if not under else 1.0)
    out.append((prev_h, q500 - bed, 0.0, 1.0, u"< 1 d"))
    out.append((q500 - bed, 99.0, 0.0, 0.0, u"above Q500"))
    return out


BANDS_FS, BANDS_HEAD = 2.5, 3.4      # v1.12: label and heading size (mm; printed about 1:1 on A3)
BANDS_LIST_W = 360.0                 # v1.12: the species list's least width (mm), two columns


def _bands_bar(S, xa, xb, y, h, colour):
    """A bar of the day strip or a band, filled by hand (a light wobble only: the bars are read against each other)."""
    r = S["hand_ring"]([(xa, y), (xb, y), (xb, y + h), (xa, y + h)], "bars", 0.08)
    S["fill"]((0.0, 0.0), r, "bars", S["hx"](colour), alpha=0.95, boundary=False, hand_=False)


def _bands_shrub(S, x, y, h, w):
    """Hand-drawn shrub (page mm): a dome h tall, w wide on the ground at (x, y), washes and a loose outline."""
    o = (0.0, 0.0)
    dome = [(x + w / 2.0 * math.cos(math.pi * i / 14.0), y + h * math.sin(math.pi * i / 14.0) ** 0.7) for i in range(15)]
    S["wash"](o, dome, "planting", S["SITE_TREE"][1], 0.6, z=S["Z_TREE"])
    S["wash"](o, [(x - w * 0.12 + (px - x) * 0.5, y + (py - y) * 0.55 + h * 0.3) for px, py in dome], "planting",
              S["SITE_TREE"][0], 0.5, z=S["Z_TREE"])
    S["sketch"](o, dome, "planting", S["SITE_TREE"][2], S["LW_FINE"], closed=True, over=0.0, amp=0.12, retrace=False,
                z=S["Z_TREE"])


def _bands_tufts(S, x0, x1, gy, h):
    """Meadow tufts h tall (page mm) from x0 to x1, gy(x) = ground y: three short hand strokes each."""
    o, x, i = (0.0, 0.0), x0, 0
    while x <= x1:
        g = gy(x)
        hh = h * (0.7 + 0.3 * ((i * 3) % 4) / 3.0)
        for d in (-0.4, 0.0, 0.4):
            S["sketch"](o, [(x, g), (x + d * hh * 0.6, g + hh * (1.0 - abs(d) * 0.4))], "planting", S["REED"],
                        S["LW_FINE"], over=0.0, amp=0.03, retrace=False, z=S["Z_TREE"])
        x += 1.25
        i += 1


def _bands_lavender(S, x0, x1, gy, k, h=0.5):
    """Lavender mounds about h tall (m) with flower spikes, 0.8 m apart (as sec_lavender), drawn by hand."""
    o, w = (0.0, 0.0), 0.8 * k
    x = x0 + w / 2.0
    while x <= x1 - w / 2.0 + 1e-6:
        g = gy(x)
        mound = [(x + w / 2.0 * math.cos(math.pi * i / 10.0), g + h * k * math.sin(math.pi * i / 10.0)) for i in range(11)]
        S["wash"](o, mound, "planting", S["hx"](SEC["olive"]), 0.6, z=S["Z_TREE"])
        for d in (-0.25, 0.0, 0.25):
            S["sketch"](o, [(x + d * w, g + h * k * 0.8), (x + d * w * 1.3, g + h * k * 1.4)], "planting",
                        S["hx"](SEC["lav"]), 0.3, over=0.0, amp=0.02, retrace=False, z=S["Z_TREE"])
        x += w


def _bands_chip(pg, code, x, y, fs):
    """A band's letter in its colour (x: remove), top-left at (x, y); returns its width."""
    w, h = fs * 1.7, fs * 1.3
    if code in BAND_COL:
        prect(pg, x, y - h, w, h, fill=BAND_COL[code])
        pg.text(code, x + w / 2.0, y - h + fs * 0.32, fs, "FFFFFF", bold=True, align="C")
    else:
        prect(pg, x, y - h, w, h, stroke=C_PL["accent"], lw=0.2)
        pg.text(u"x", x + w / 2.0, y - h + fs * 0.3, fs, C_PL["accent"], bold=True, align="C")
    return w


def draw_bands(opt, den=None):
    """W3b v1.12 (Aras 26 Oct: one drawing, the hand-sketched language of the upstream entry, p.23): the planting
    bands A-F on the surveyed S4 ground, where the water reaches it for that many days a year (this cut's own
    figures), drawn by the sketch engine; under it the day classes and which band fits each; then the species as one
    list in two columns, each warning on its own species' row."""
    E = detail_engine()
    S = sketch_engine()
    del S["ZP"][:]
    S["ORDER"][0] = 0
    S["HAND"][0] = False
    o = (0.0, 0.0)
    prof = s4_profile(E)
    bed, q100, q500 = E["THALWEG"][1], E["Q100"], E["Q500"]
    den = den or BANDS_DENS[0]
    k = 1000.0 / den
    fs, fh = BANDS_FS, BANDS_HEAD
    s0, s1 = BANDS_S
    zb = bed - 1.0
    pg = Page(0, 0)

    def P(s, z):
        return ((s - s0) * k, (z - zb) * k)

    def gz(s):
        return E["prof_z"](prof, s)

    def gy_x(x):
        return P(0, gz(s0 + x / k))[1]

    def flush():
        pg.items += [it for _, _, it in sorted(S["ZP"], key=lambda e: (e[0], e[1]))]
        del S["ZP"][:]
    ss = [s0 + 0.25 * i for i in range(int((s1 - s0) / 0.25) + 1)]
    cls = s4_classes(E)

    def cl(s):
        h = gz(s) - bed
        return next(i for i, c in enumerate(cls) if h < c[1] or i == len(cls) - 1)
    runs = []
    for s in ss:
        c = cl(s)
        if runs and runs[-1][0] == c:
            runs[-1][2] = s
        else:
            runs.append([c, s, s])
    W = P(s1, 0)[0]
    # ground: the engine's poché and earth strokes on the survey every 1 m (the hand line), the day classes as a
    # marker band under the surface, the base flow (bed to the 0.10 m line) and the faint Q500 reach
    surf = [P(s0 + i, gz(s0 + i)) for i in range(int(s1 - s0) + 1)]
    gs = S["sketch_ground"](o, [(0.0, 0.0)] + surf + [(W, 0.0)], "ground")
    for c, a, b in runs:
        for pc in S["band"](gs, P(a, 0)[0], min(W, P(b + 0.25, 0)[0]), 2.4):
            S["wash"](o, pc, "days", S["hx"](DAYS_COL[c]), 0.9)
    yq5 = P(0, q500)[1]
    pc = S["under_level"](gs, 0.0, W, yq5)
    if pc:
        S["wash"](o, pc, "flood", S["FLOOD_WASH"], 0.12)
    S["water_level"](o, gs, P(E["THALWEG"][0], 0)[0], P(0, bed + cls[0][1])[1], S["W_WIN"], bed_hatch=True)
    # plants: each day class gets the band(s) whose days overlap it most (B reeds, C shrubs, D meadow, E trees, F
    # lavender), at the design's sizes on S4 (reeds 2.2 m, Tamarix / Vitex shrubs 1.9 m, plane 7.5 m)
    rd = max(r[2] for r in E["SECTIONS"][0]["reeds"]) * k
    sh_ = E["SECTIONS"][0]["shrubs"][3]
    tr = E["SECTIONS"][0]["trees"][0]
    tag = {}                                                  # band -> (x, top y) of its first plant, for its label
    for c, a, b in runs:
        xa, xb = P(a, 0)[0], P(b, 0)[0]
        if c in (0, 1) and xb - xa > 1.5:
            n = max(1, int((xb - xa - 1.2) / 4.8))
            for j in range(n):
                x0_ = xa + 0.6 + (xb - xa - 1.2) * j / n
                x1_ = xa + 0.6 + (xb - xa - 1.2) * (j + 1) / n
                S["reeds"](o, x0_, x1_, gy_x((x0_ + x1_) / 2.0) - 0.2, rd)
            if c == 0:
                tag.setdefault("B", ((xa + xb) / 2.0, gy_x((xa + xb) / 2.0) + rd))
        if c in (1, 2) and xb - xa > 6.0:
            for f in (0.3, 0.75):
                x_ = P(a + (b - a) * f, 0)[0]
                _bands_shrub(S, x_, gy_x(x_) - 0.2, sh_[1] * k, sh_[2] * k)
                tag.setdefault("C", (x_, gy_x(x_) + sh_[1] * k))
        if c == 2 and xb - xa > 2.0:
            _bands_tufts(S, xa + 0.4, xb - 0.4, gy_x, 0.35 * k)
            if xa > P(E["THALWEG"][0], 0)[0]:                 # the north-east meadow, clear of the reeds
                tag.setdefault("D", ((xa + xb) / 2.0, gy_x((xa + xb) / 2.0) + sh_[1] * k))
        if c == 3 and b - a >= 2.0:
            x_ = P((a + b) / 2.0, 0)[0]
            S["sketch_tree"](o, x_, gy_x(x_) - 0.2, tr[2] * k)
            tag.setdefault("E", (x_, gy_x(x_) + tr[2] * k * 0.96))
        if c == 4 and xb - xa > 4.0:
            _bands_lavender(S, xa + 1.0, min(xb - 1.0, xa + 6.0 * k), gy_x, k)
            tag.setdefault("F", (xa + 3.0 * k, gy_x(xa + 3.0 * k) + 0.6 * k))
    x_ = P(s0 + 2.0, 0)[0]
    S["sketch_person"](o, x_, gy_x(x_), 1.75 * k)                # scale figure on the south-west bank, above Q500
    S["sketch"](o, gs, "ground lines", S["SKINK"], S["PEN_BOLD"], z=S["Z_LINE"])   # the cut: the gesture
    flush()
    # level lines where the water stands over the ground: the day heights, Q100, Q500 (hand lines, dashed); their
    # figures in a ladder at the right
    lv = []
    for i, (hl, hh, dlo, dhi, lab) in enumerate(cls[:-2]):
        lv.append((bed + hh, u"{:.2f} m · {}".format(hh, (u"{} d".format(int(dlo)) if dlo else u"< 1 d")),
                   C["w3"], [0.6, 0.5], 0.2))
    lv += [(q100, u"Q100 · {:.2f} m".format(q100 - bed), "1B535E", [1.6, 0.6], 0.3),
           (q500, u"Q500 · {:.2f} m".format(q500 - bed), "1B535E", [2.4, 0.8], 0.3)]
    xr = W + 1.0
    ent = []
    for z, t, colr, dash, lw in lv:
        run = [s for s in ss if gz(s) < z]
        if run:
            a_, b_ = P(run[0], z), P(run[-1], z)
            pg.line(S["hand"]([a_, b_], 0.1, S["HAND_WAV"], S["_seed"](a_[0], z)), colr, lw, dash=dash)
            if b_[0] < xr - 0.5:
                pg.line([b_, (xr, b_[1])], colr, 0.08, dash=[0.3, 0.6])
            if z in (q100, q500):
                xm = P(s0 + (19.0 if z == q100 else 22.5), 0)[0]
                mk = [(xm - 1.0, b_[1] + 1.7), (xm + 1.0, b_[1] + 1.7), (xm, b_[1]), (xm - 1.0, b_[1] + 1.7)]
                pg.line(mk, colr, 0.15)
        ent.append((P(0, z)[1], t, colr, z in (q100, q500)))
    level_ladder(pg, ent, xr, xr + 5.0, fs, lo=P(0, bed)[1] - 1.0)
    # labels in the sky: the band each plant stands for, the two banks, the idea
    names = {"B": u"reeds", "C": u"shrubs", "D": u"meadow", "E": u"trees", "F": u"lavender"}
    for code in sorted(tag):
        x_, top = tag[code]
        y_ = max(top, yq5) + 2.6
        cw_ = fs * 1.7 + 0.8 + text_w(names[code], fs)
        x_ = min(max(x_ - cw_ / 2.0, 0.0), W - cw_)
        _bands_chip(pg, code, x_, y_ + fs * 1.05, fs)
        pg.text(names[code], x_ + fs * 1.7 + 0.8, y_, fs, C_PL["ink"])
    ytop = P(0, gz(s0))[1] + 1.75 * k + 3.0
    pg.text(u"south-west bank", 0.0, ytop, fs, COL["ink2"])
    pg.text(u"north-east bank · road", W, P(0, gz(s1))[1] + 3.0 * k, fs, COL["ink2"], align="R")
    pg.text(u"the bands follow the days under water", 0.0, ytop + fh * 2.2, fh, "1E1E1E", bold=True)
    # under the cut: the day classes along the ground, then one bar per band over the classes its days overlap
    y = -fs * 1.8
    pg.text(u"days a year under water on S4 " + cite(E["DAYS_WET"]), 0.0, y, fs, COL["ink2"])
    y -= 1.6 + 3.2
    for c, a, b in runs:
        xa, xb = P(a, 0)[0], P(min(s1, b + 0.25), 0)[0]
        _bands_bar(S, xa, xb, y, 3.2, DAYS_COL[c])
    flush()
    seen = set()
    for c, a, b in sorted(runs, key=lambda r: -(r[2] - r[1])):
        xa, xb = P(a, 0)[0], P(min(s1, b + 0.25), 0)[0]
        if c in seen or xb - xa < text_w(cls[c][4], fs, True) + 1.0:
            continue
        seen.add(c)
        pg.text(cls[c][4], (xa + xb) / 2.0, y - fs * 1.3, fs, COL["ink"], bold=True, align="C")
    y -= fs * 1.3 + 2.0
    for code, name, eco, days, depth, zone in PLANT_BANDS:
        segs = []
        for c, a, b in runs:
            lo_, hi_ = cls[c][2], cls[c][3]
            if code == "A":
                ok = c == 0
            elif code == "F":
                ok = c >= len(cls) - 2
            else:
                blo, bhi = BAND_DAYS[code]
                ok = lo_ < bhi and blo < hi_
            if ok:
                segs.append((P(a, 0)[0], P(min(s1, b + 0.25), 0)[0]))
        y -= fs * 1.25
        x_ = segs[0][0] if segs else 0.0
        t = u"{} · {}".format(name.split(u" (")[0].lower(), days.replace(u" d/yr", u" d"))
        x_ = min(x_, W - text_w(code, fs, True) - 1.0 - text_w(t, fs))
        pg.text(code, x_, y, fs, COL["ink"], bold=True)
        pg.text(t, x_ + text_w(code, fs, True) + 1.0, y, fs, COL["ink"])
        y -= 1.0 + 2.2
        for xa, xb in segs:
            _bands_bar(S, xa, xb, y, 2.2, BAND_COL[code])
        y -= 1.2
    flush()
    # scale bar 10 m and the bands' source
    yb = y - 3.0
    pg.poly([rect(0.0, yb, 5.0 * k, yb + 1.0)], fill=COL["ink"])
    pg.poly([rect(5.0 * k, yb, 10.0 * k, yb + 1.0)], fill=COL["white"], stroke=COL["ink"], lw=0.12)
    pg.text(u"10 m · 1:{:,.0f} · S4, looking upstream".format(den), 10.0 * k + 2.0, yb, fs, COL["ink2"])
    pg.text(u"bands " + cite(BAND_SOURCE), W, yb, fs, COL["ink2"], align="R")
    _BANDS_DRAWING[:] = [items_bbox(pg.items)]          # the section and its bars (the booklet's crop of page 29)
    # species: one list in two columns under it, grouped by band: letter, name, local name [n], its warning on the
    # same line, the evidence chips under it
    bx0, _, bx1, _ = _BANDS_DRAWING[0]
    bx1 = max(bx1, bx0 + BANDS_LIST_W)                  # the list keeps its width at every scale (no wrapped chips)
    ncol, gx_ = 2, 10.0
    cw_ = (bx1 - bx0 - (ncol - 1) * gx_) / ncol
    rows = (len(SPECIES) + ncol - 1) // ncol
    rh = 9.6
    ty = yb - 9.0
    pg.text(u"species by band · evidence · care", bx0, ty, fh, C_PL["ink"], bold=True)
    ty -= 3.0
    for k_, (band, lat, loc, ev, src_ev, flag, src) in enumerate(SPECIES):
        c_, r_ = k_ // rows, k_ % rows
        cx_, cy_ = bx0 + c_ * (cw_ + gx_), ty - r_ * rh
        if r_ and SPECIES[k_ - 1][0] != band:
            pg.line([(cx_, cy_ + 0.9), (cx_ + cw_, cy_ + 0.9)], C["faint"], 0.2)
        tx = cx_ + _bands_chip(pg, band, cx_, cy_ - 0.2, fs) + 1.6
        yl = cy_ - 2.9
        pg.text(lat, tx, yl, 2.8, C_PL["ink"], bold=True)
        tx += text_w(lat, 2.8, True) + 1.5
        t = loc + u" " + cite(src_ev + u" (" + SPECIES_SRC[src] + u")")
        pg.text(t, tx, yl, fs, C_PL["ink2"])
        tx += text_w(t, fs) + 3.0
        ye = cy_ - 4.3
        ev = [(a_, t_.replace(u"\u2264", u"up to")) for a_, t_ in ev]   # the PDF font has no "less or equal" sign
        chips(pg, cx_ + fs * 1.7 + 1.6, ye, ev, fs, cw_ - fs * 1.7 - 1.6)
        if flag:
            hot = flag.isupper() or "TOXIC" in flag or "POISON" in flag or "REMOVE" in flag
            kind = "scent" if ("aromatic" in flag or "scent" in flag) else ("warn" if hot else "flag")
            need = 3.6 + text_w(flag, fs, hot)
            fy = cy_
            if tx + need > cx_ + cw_:                        # no room on the name's line: after the evidence chips
                tx = cx_ + fs * 1.7 + 1.6 + sum(fs * 1.6 + fs * 0.45 + text_w(t_, fs) + fs * 1.5 for _, t_ in ev)
                fy = ye - 0.6
            icon(pg, kind, tx, fy - 0.1, 3.0)
            pg.text(flag, tx + 3.6, fy - 2.9, fs, C_PL["accent"] if hot else C_PL["ink2"], bold=hot)
    pg.text(u"full sources " + cite(CONCEPT_FILE + u" §9; library/context/2026-10-19_research_vegetation/"
            u"04_plants_flood_drought_cleaning.md (POWO, FEIS, JRC Atlas, Song 2021, Schindler et al. 2022 ...); "
            u"Vetiver left out: not native (POWO)"), bx0, ty - rows * rh - 2.5, fs, C_PL["ink2"])
    return pg


_BANDS_DRAWING = []                  # bbox of the W3b section part (page mm of its own Page), for the crop


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
    return WB_DEFAULT, u"water balance default lands, 24 Oct"


WB, WB_SRC = wb_results()
try:
    WB_STORE = tuple(WB["design"]["central_range_m3"])
    WB_PCT = tuple(WB["design"]["central_range_pct_1in5_dry"])
    WB_STRIP = float(WB["strip_m3_per_year"])
    OLIVE_M3_HA = WB["net_irrigation_mm"]["olive"]["dry5"] / DRIP_EFF * 10.0     # m³/ha at the intake, 1-in-5 dry year
except Exception:
    WB, WB_SRC = WB_DEFAULT, u"water balance default lands, 24 Oct"
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
    ("sewage", u"SEWAGE WENT INTO THE SELINOS", u"3 km + 500 m",
     u"İZSU sewer + connections, Feb 2024 · against odour, flies",
     u"published, İZSU via Gerçek İzmir 28 Feb 2024; " + REG + u" SE-22"),
    ("gauge", u"MEASURED WATER QUALITY OF THE SELINOS", u"NO DATA",
     u"in any source the project holds", WD + u", Still needed 4"),
    ("house", u"GREYWATER OF THE STREAMSIDE HOUSES", u"NO DATA",
     u"sinks, showers, laundry: no volume, no route in any source", u"not in the project's data"),
    ("plant", u"BERGAMA'S TREATMENT PLANT", u"14,304 m³ a day",
     u"treated -> Bakırçay, not the Selinos", u"published, TMMOB 2023 citing İZSU; " + WD),
    ("tank", u"RAINWATER TANKS", u"roofs only",
     u"garden + toilets only · not listed for drinking",
     u"published, ÇŞİDB guide 2025; rainwater regulation Art. 13, 16(1); " + REG + u" EN-E5, EN-A2"),
    ("reed", u"SO THE STREAM IS CLEANED", None,
     u"before people + plants use it · first treatment designed here", REG + u" §2, row 'Is treatment necessary?'")]
HOW_T = [
    ("reed", u"REED-BED FIELD DATA", u"58-88 %", u"of NH4-N removed", u"published; " + REG + u" PL-09"),
    ("area", u"BED AREA PER PERSON EQUIVALENT", u"5 m² · 1-3 m²",
     u"horizontal · vertical flow", u"published, Vymazal 2010; " + REG + u" EN-D2"),
    ("nose", u"HOW MUCH ANY PLANT REDUCES ODOUR", u"NO DATA", u"no source measures it", REG + u" §2: gap"),
    ("uv", u"DISINFECT WHERE PEOPLE TOUCH IT", u"UV",
     u"water people touch + park irrigation · UV = the reuse method", u"inferred from EN-D3, EN-E1; EN-E2 published")]
COLIFORM = [  # (label, low, high, colour key, source); 0 = the limit is zero
    (u"Left after an emergent-plant wetland", 1e2, 1e5, "d2", u"published, reviews 2005 and 2020; EN-D3"),
    (u"Reuse class B limit (orchards, vineyards)", 200, 200, "acc", u"published, 2010 communiqué; EN-E1"),
    (u"Reuse class A limit (parks, raw-eaten crops)", 0, 0, "acc", u"published, 2010 communiqué; EN-E1"),
    (u"Drinking water limit (E. coli)", 0, 0, "acc", u"published, Ministry of Health; EN-E3")]
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
    (u"DISINFECT WHERE PEOPLE TOUCH IT", u"wetlands leave 10^2-10^5 CFU/100 ml · class A: 0"),
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


LOOP_BACK = u"next winter: new stream water refills the storage · one way, nothing pumped back"


def draw_decision(pg, x, y, w, h, s):
    """v1.12 (Aras 26 Oct 07:06 and his sketch): the seven steps clockwise round a rectangle, 1-4 along the top, 5-7
    back along the bottom; the closing arrow (7 -> 1) in red says what really closes the loop: the next winter's
    stream, never a pump (the water runs one way). Returns the lowest y drawn."""
    n = len(DECISION)
    top_n = (n + 1) // 2
    gap, vg = 16.0 * s, 24.0 * s
    bw = (w - (top_n - 1) * gap) / top_n
    bh = 0.0
    for t, src in DECISION:                          # one height for every box: the tallest content
        bh = max(bh, 9.0 * s + len(wrap(t, 3.2 * s, bw - 8.0, True)) * 3.2 * s * 1.28 +
                 len(wrap(src, 2.5 * s, bw - 8.0)) * 2.5 * s * 1.28 + 3.0)
    yt = y                                           # top row: its boxes' top edge
    yb = y - bh - vg                                 # bottom row
    bot_x = [x + w - bw - (w - bw) * j / (n - top_n - 1) for j in range(n - top_n)] if n - top_n > 1 else [x]
    pos = [(x + i * (bw + gap), yt) for i in range(top_n)] + [(bot_x[j], yb) for j in range(n - top_n)]
    for i, (t, src) in enumerate(DECISION):
        bx, by = pos[i]
        pg.poly([rect(bx, by - bh, bx + bw, by)], fill=C["white"], stroke=C["d2"], lw=0.4)
        pg.text(str(i + 1), bx + 3.0, by - 7.0 * s, 6.0 * s, C["d3"], bold=True)
        icon(pg, DEC_ICONS[i], bx + bw - 3.0 - 7.0 * s, by - 1.5, 7.0 * s)
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


STORE_K = 1.8                        # v1.13 (Aras 26 Oct 08:27 "page 14 looks too lean"): storage words 1.8 x larger


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
             ("cube", u"{:,.0f}-{:,.0f} m³".format(WB_STORE[0], WB_STORE[1]),
              u"design incl. strip · aquifer recharge · {:.0f}-{:.0f} % of farm need, 1-in-5 dry · {:.1f} m edge".format(
                  WB_PCT[0], WB_PCT[1], e4), WB_SRC),
             ("drop", u"≈ {:,.0f} m³/yr".format(WB_STRIP), u"losses only (one way, on to the farms) · evaporation + seepage "
              u"5 mm/d sealed / 25 mm/d unsealed · up to 10 x possible",
              u"calculated, sequent-peak over 2016-2021; seepage 25 mm/day = the bottom of FAO's sand range; " + RR +
              u" §4, A6; " + WB_SRC)]
    y = max(b3[3], b4[3]) + 6.0                       # v1.8: each line = pictogram + big figure + keywords + [n]
    f = STORE_K                                       # v1.13: the figures and keywords read on the booklet page
    for kind, big, t, src in lines:
        icon(pg, kind, tx, y, 5.0 * f)
        pg.text(big, tx + 6.5 * f, y - 3.6 * f, 3.0 * f, C["d3"], bold=True)
        lx = tx + 7.5 * f + text_w(big, 3.0 * f, True)
        yy = y - 1.6 * f
        for ln in wrap(t + u" " + cite(src), 1.9 * f, 175.0 - (lx - tx)):
            pg.text(ln, lx, yy, 1.9 * f, COL["ink"])
            yy -= 2.4 * f
        y = min(y - 6.6 * f, yy - 0.8 * f)
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
    pg.text(u"one way, with the stream " + cite(CONCEPT[1]), tx, y - 3.0, 2.0, COL["ink2"])
    pg.line([(x0, y0), (x1, y0)], COL["structure"], 0.3)


def draw_footer(pg, x0, y0, x1, pal_line, src_line):
    t = (u"measured = station/gauge · published = official/paper · calculated = our arithmetic · design value = chosen · "
         u"1-11 = the water's elements, same on every drawing. " + src_line)
    key = u"Sources by number: " + u"  ".join(u"[{}] {}".format(i + 1, k) for i, k in enumerate(SRC_KEY))
    n = len(wrap(t, 1.9, x1 - x0)) * 1.9 * 1.28 + len(wrap(key, 1.6, x1 - x0)) * 1.6 * 1.28
    y = para(pg, x0, y0 + 3.6 + n, x1 - x0, t, 1.9, COL["ink2"])    # v1.6: the numbered source key under it
    y = para(pg, x0, y, x1 - x0, key, 1.6, COL["ink2"])
    pg.text(u"{} · {} · {} · {}".format(CREDIT, COURSE, VERSION, pal_line), x0, y - 2.6, 1.9, COL["ink2"])


BK_CROPS = []                        # v1.10: (id, (x0, y0, x1, y1) board mm y up, scale_den, legend, drop) per panel


def crop_add(cid, bb, den=None, legend=None, drop=None, pad=1.0):
    BK_CROPS.append((cid, (bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad), den, legend or [], drop or []))


def drawn(pg, fn):
    """Runs fn() (which draws onto pg) and returns the bbox of what it added."""
    n0 = len(pg.items)
    fn()
    return items_bbox(pg.items[n0:])


# v1.12 (Aras 26 Oct 07:06): every diagram carries a short context line: what it shows, why it is here, what to take
# from it. Each is drawn inside its panel's crop, so the booklet page shows it with the drawing.
CONTEXT = {
    "year": u"One water year, October to September, on one month axis: rain, evaporation, flow and depth. The stream "
            u"carries its water in winter and almost none in summer, so winter water has to be held.",
    "cuts": u"Five surveyed cuts and DSİ's planned channel, cropped to the bed, true scale. How high each flood reaches, "
            u"and what each level means for what we build there.",
    "chain": u"The water's path through the three working areas, one way with the stream: cleaned once at the upstream "
             u"entry, lived with along the way, released clean downstream.",
    "storage": u"The volumes the summer strip needs, as cubes to scale. Winter flow fills the storage; the strip draws "
               u"on it through the dry months.",
    "concept": u"The idea in section at the upstream entry and at K4: the problem on site and the one move that answers "
               u"it. Numbers as in the chain.",
    "farms": u"Where the clean water ends up: farmland outside the site, easing an aquifer used 4.4 times its "
             u"potential. Never drinking water.",
    "seasons": u"One cut, S4's south-west bank, through the year: what the water, the plants and people do in each "
               u"season. Read down from the winter floods to the autumn wait for rain.",
    "ne": u"The other bank of S4 in detail: materials, levels and widths in summer, and below it the same bank under "
          u"its winter water and flood levels.",
    "bands": u"Plants are set by how many days a year water covers the ground on S4: the lower the ground, the wetter "
             u"the band. The species list under it gives each band's plants and their evidence.",
}
CTX_FS = 2.6                         # context line size, mm (about 7.4 pt when the panel prints 1:1 on A3)


def context(pg, x, y, w, key):
    """The panel's context line from its top y; returns the box (x0, y0, x1, y1) it took."""
    yy = para(pg, x, y, w, CONTEXT[key], CTX_FS, COL["ink"])
    return (x, yy - CTX_FS * 0.3, x + w, y)


def union(*bbs):
    return (min(b[0] for b in bbs), min(b[1] for b in bbs), max(b[2] for b in bbs), max(b[3] for b in bbs))


def build_board(opt, storage, parts, pal_line, log):
    """v1.12 (Aras 26 Oct 07:06 review of the booklet): a 3 x 3 grid of panels, each the size of one A3 booklet page,
    so every page of the booklet is one panel at about 1:1: drawings whole, at their own round scale, filling the page.
      row 1  the year · how high the stream rises · who does what + why and how we clean
      row 2  storage · the idea in section · where the clean water goes + the seven steps
      row 3  the S4 cut through the year · S4 north-east bank · planting bands + species"""
    pg = Page(BOARD_W, BOARD_H)
    pg.poly([rect(0, 0, BOARD_W, BOARD_H)], fill=COL["sheet"])
    del BK_CROPS[:]
    X0, X1, G = M, BOARD_W - M, 6.0
    y_title = BOARD_H - M - 26.0
    draw_title(pg, X0, y_title, X1, BOARD_H - M, opt, storage)
    ch = 252.0
    cws = [377.0, 395.0, 377.0]               # the middle column a little wider: the S4 north-east bank is 389 mm at 1:200
    cws[1] = X1 - X0 - 2 * G - cws[0] - cws[2]

    def cell(c, r, title):
        x0 = X0 + sum(cws[:c]) + c * G
        y1 = y_title - G - r * (ch + G)
        b = frame(pg, (x0, y1 - ch, x0 + cws[c], y1), title)
        return (b[0], b[1] + 1.0, b[2], b[3] - 1.0)

    def fits(part, w, h):
        pb = items_bbox(part.items)
        return pb[2] - pb[0] <= w and pb[3] - pb[1] <= h

    # row 1 -------------------------------------------------------------- the year
    b = cell(0, 0, u"THE YEAR OF THE WATER · Oct -> Sep, the gauges' water year")
    cb = context(pg, b[0], b[3], b[2] - b[0], "year")
    _, bb = place(pg, parts["year"], (b[0], b[1], b[2], cb[1] - 3.0), 1.6, "C", log, "year of the water")
    crop_add("wb_year", union(cb, bb))
    # how high the stream rises: one round scale for the six cuts, the largest that fits (v1.10-v1.11)
    b = cell(1, 0, u"HOW HIGH THE STREAM RISES · 5 surveyed cuts + DSİ's planned channel")
    cb = context(pg, b[0], b[3], b[2] - b[0], "cuts")
    box = (b[0], b[1], b[2], cb[1] - 3.0)
    part, den = draw_sections(opt, (box[2] - box[0], box[3] - box[1]))
    s, bb = place(pg, part, box, 1.0, "TL", log, "stream height")       # v1.12: right under its context line
    if s < 0.999:
        log.append(u"NOTE: the stream-height cuts are printed at {:.0f} % of 1:{:,.0f}".format(100 * s, den))
    crop_add("wb_cuts", union(cb, bb), den / s, drop=[r"method \[\d+\]"])
    CUTS_DEN[0] = den / s
    # who does what (one continuous chain) over why and how we clean
    b = cell(2, 0, u"COLLECT, CLEAN, HOLD · who does what, one way with the stream (1-11)")
    cb = context(pg, b[0], b[3], b[2] - b[0], "chain")
    _, bb = place(pg, parts["chain"], (b[0], b[3] - 112.0, b[2], cb[1] - 3.0), 1.0, "C", log, "chain")
    crop_add("wb_chain", union(cb, bb), drop=[r"^Sources:"])
    cl = (b[0], b[1], b[2], b[3] - 116.0)
    crop_add("wb_cleaning", drawn(pg, lambda: fit_draw(pg, draw_cleaning, (cl[0] + 4.0, cl[1], cl[2], cl[3]))))
    # row 2 -------------------------------------------------------------- storage cubes at a round scale (v1.6, v1.11)
    t4 = u"HOW MUCH TO STORE FOR THE SUMMER STRIP (4)"
    b = cell(0, 1, t4)
    cb = context(pg, b[0], b[3], b[2] - b[0], "storage")
    box = (b[0], b[1], b[2], cb[1] - 3.0)
    for sc_ in CUBE_SCALES:
        globals()["CUBE_SCALE"] = sc_
        cp = draw_storage_cubes(opt)
        if fits(cp, box[2] - box[0], box[3] - box[1]):
            break
    cs, bb = place(pg, cp, box, 1.0, "C", log, "storage cubes")
    if cs < 0.999:
        log.append(u"NOTE: the storage cubes are printed at {:.0f} % of 1:{:,.0f}".format(100 * cs, CUBE_SCALE))
    crop_add("wb_storage", union(cb, bb), CUBE_SCALE / cs)
    # the idea in section: upstream entry over K4
    b = cell(1, 1, u"THE IDEA IN SECTION · problem -> one move · numbers as in the chain")
    cb = context(pg, b[0], b[3], b[2] - b[0], "concept")
    hh = (cb[1] - 3.0 - b[1] - 6.0) / 2.0
    _, bu = place(pg, parts["concept_up"], (b[0], cb[1] - 3.0 - hh, b[2], cb[1] - 3.0), 1.6, "C", log,
                  "concept upstream")
    crop_add("wb_concept_up", union(cb, bu))
    _, bk = place(pg, parts["concept_k4"], (b[0], b[1], b[2], b[1] + hh), 1.6, "C", log, "concept K4")
    crop_add("wb_concept_k4", bk)
    # where the clean water goes, over the seven steps the figures support
    b = cell(2, 1, u"WHERE THE CLEAN WATER GOES (10, 11) · and what the figures support")
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
    # row 3 -------------------------------------------------------------- the S4 cut through the year, one row a season
    seas = ("winter", "spring", "summer", "autumn")
    b = cell(0, 2, u"THE S4 CUT THROUGH THE YEAR · SOUTH-WEST BANK AND BED")
    gap_r = 3.0
    for den in S4_DENS:                       # one scale for the four rows, the largest at which they stack in the panel
        s4 = dict((k_, draw_s4_season(k_, log, den, k_ == "autumn")) for k_ in seas)
        bbs = [items_bbox(s4[k_].items) for k_ in seas]
        wmax = max(q[2] - q[0] for q in bbs)
        if wmax <= b[2] - b[0] - 40.0 and sum(q[3] - q[1] for q in bbs) + 3 * gap_r <= b[3] - b[1]:
            break
    xc = b[0] + wmax + 4.0                    # the context line in the column at the right of the rows
    cb = context(pg, xc, b[3], b[2] - xc, "seasons")
    y = b[3]
    seen = []
    for key, q in zip(seas, bbs):
        s, bb = place(pg, s4[key], (b[0], y - (q[3] - q[1]), b[0] + wmax, y), 1.0, "TL", log, "S4 " + key)
        seen.append(bb)
        y -= q[3] - q[1] + gap_r
    crop_add("wb_s4_seasons", union(cb, *seen), den)
    # the north-east bank: summer (the engine's callouts, materials, widths), then winter with the flood levels
    b = cell(1, 2, u"S4 · NORTH-EAST BANK · 1:{:,.0f} · summer and winter".format(S4_NE_SCALE))
    cb = context(pg, b[0], b[3], b[2] - b[0], "ne")
    hs = []
    y = cb[1] - 3.0
    left = min(items_bbox(parts[k_].items)[0] for k_ in ("detail", "detail_w"))   # one x for the bank in both rows
    for part, head in ((parts["detail"], u"SUMMER · full leaf, the strip running"),
                       (parts["detail_w"], u"WINTER · the water and the floods on the same bank")):
        pg.text(head, b[0], y - 3.2, 3.2, COL["ink_dark"], bold=True)
        pb = items_bbox(part.items)
        xa = b[0] + pb[0] - left
        s, bb = place(pg, part, (xa, y - 5.0 - (pb[3] - pb[1]), max(b[2], xa + pb[2] - pb[0]), y - 5.0), 1.0, "TL",
                      log, "S4 north-east bank")
        if s < 0.999:
            log.append(u"NOTE: the S4 north-east bank is printed at {:.0f} % of 1:{:,.0f}".format(100 * s,
                                                                                                   S4_NE_SCALE))
        hs.append(bb)
        y = bb[1] - 6.0
    crop_add("wb_s4_ne", union(cb, *hs), S4_NE_SCALE / s)
    # planting bands on the S4 ground, the species under them
    b = cell(2, 2, u"PLANTING BANDS BY DAYS UNDER WATER (7) · species + evidence")
    cb = context(pg, b[0], b[3], b[2] - b[0], "bands")
    box = (b[0], b[1], b[2], cb[1] - 3.0)
    for den in BANDS_DENS:                    # v1.10: the largest of these scales at which it fits
        part = draw_bands(opt, den)
        pb = items_bbox(part.items)
        if fits(part, box[2] - box[0], box[3] - box[1]):
            break
    s, bb = place(pg, part, box, 1.0, "TL", log, "planting bands")
    if s < 0.999:
        log.append(u"NOTE: the planting bands are printed at {:.0f} % of 1:{:,.0f}".format(100 * s, den))
    sb = _BANDS_DRAWING[0]                     # the section and its bars, without the species cards
    crop_add("wb_bands", union(cb, (bb[0] + (sb[0] - pb[0]) * s, bb[1] + (sb[1] - pb[1]) * s,
                                    bb[0] + (sb[2] - pb[0]) * s, bb[1] + (sb[3] - pb[1]) * s)), den / s,
             [{"kind": "fill", "colour": DAYS_COL[i], "label": c[4]} for i, c in enumerate(s4_classes(detail_engine()))],
             [r"^days a year under water", r"^bands \[\d+\]"])
    crop_add("wb_species", (bb[0], bb[1], bb[2], bb[1] + (sb[1] - pb[1]) * s - 1.5))
    draw_footer(pg, X0, 1.5, X1, pal_line, parts["src"])
    return pg


#@include ../common/booklet_assets.py


# ---------------------------------------------------------------- A3 booklet (v1.10; booklet/CROP_SPEC.md, Aras 25 Oct 21:47)
# The booklet shows this board's own drawings: one crop per panel of the sheet (the rects build_board records in
# BK_CROPS from its own layout), and results.json with the figures the booklet reads. Nothing is drawn twice.
BK_CAPTIONS = {
    "wb_chain": u"Who does what: one way, with the stream", "wb_year": u"The year of the water, Oct -> Sep",
    "wb_cuts": u"How high the stream rises at six cuts", "wb_concept_up": u"Upstream entry: the idea in section",
    "wb_concept_k4": u"K4: the idea in section", "wb_bands": u"Planting bands by days under water, S4",
    "wb_species": u"Species by planting band", "wb_s4_seasons": u"S4, south-west bank, winter to autumn",
    "wb_s4_ne": u"S4, north-east bank, summer and winter",
    "wb_storage": u"How much to store, cubes to scale", "wb_cleaning": u"Why and how we clean",
    "wb_farms": u"Where the clean water goes", "wb_decision": u"What the figures support"}


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
    with open(bk.path("results.json"), "w", encoding="utf-8") as f:
        json.dump(bk_results(), f, ensure_ascii=False, indent=1)
    bk.save()
    log.append(u"booklet: {} crops of {}, results.json".format(len(BK_CROPS), name))


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
    detail = draw_s4_ne(log)                        # v1.10: the north-east bank; the seasons are the south-west rows
    src_line = (u"Sources: " + CM + u", " + RR + u" and tables, " + WD + u", " + REG + u", " + CR +
                u", bergama_plant_data_v1.json; scripts merged: water loop v2, water case v1.1, rain_river charts, "
                u"pr1 drawings v3.1, detail section v2, plant analysis v1 (panels 7-8).")
    files = []
    for opt in OPTIONS:
        parts = {"chain": draw_chain(opt), "year": draw_year(opt),
                 "concept_up": draw_concept("up", opt), "concept_k4": draw_concept("k4", opt),
                 "detail": detail, "detail_w": draw_s4_ne_winter(log),
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
    if folder and files and not err:                # v1.10: the booklet's crops of this sheet; never breaks it
        try:
            booklet_export(folder, files[0], log)
        except Exception as ex_:
            log.append(u"booklet not written: {}: {}".format(type(ex_).__name__, ex_))
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
