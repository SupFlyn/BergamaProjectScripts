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

NEW IN v1.9 (25 Oct, A3 booklet, SCRIPT_STANDARD §8): after the board, one press also writes the booklet's drawings to
  output/bergama_water_board/booklet/ (one text-free vector PDF per frame, drawn at the frame's size, its words in
  blocks.json, the figures in results.json). The board is unchanged.
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

VERSION = "bergama_water_board v1.9 (2026-10-25)"
SHORT = "v1.9"
BUTTON_WORDS = ("build", "bake", "run", "go", "press", "button", "start")
BOARD_W, BOARD_H = 1189.0, 841.0     # A0 landscape, mm
M = 14.0                             # board margin, mm
OPTIONS = ("A",)                     # v1.7: option A only (organic only where the project meets the water), Aras 16:43
STORAGE_STYLES = ("cubes",)          # v1.6: cubes only (Aras 25 Oct 13:12; the chart is gone)
CUBE_SCALE = 1000.0                  # the storage cubes are drawn at 1:1,000 ...
CUBE_SCALES = (1000.0, 1250.0, 1500.0, 2000.0, 2500.0)   # ... v1.6: or the first of these at which they fit
OUT_FOLDER = "bergama_water_board"
OUT_NAME = "Bergama_water_board_v1_9_{}_{}.pdf"
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
        if s:
            self.items.append(("text", s, x, y, size, color, bold, align, mat, halo))


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


def write_pdf(pg, path, title):
    objs = []

    def add(b):
        objs.append(b)
        return len(objs)
    font = []
    for nm in ("Helvetica", "Helvetica-Bold"):
        font.append(add("<< /Type /Font /Subtype /Type1 /BaseFont /{} /Encoding << /Type /Encoding /BaseEncoding "
                        "/WinAnsiEncoding {} >> >>".format(nm, _DIFF).encode("latin-1")))
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
def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


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
CUTS = [  # the channel cut on the main survey: ground every 1 m (m above the bed low point), depths of EVENTS (m above the bed),
          # the width each level covers (from, to; m from the centreline, + = left bank looking downstream), notes
    dict(key="flat", name=u"4 · FLAT DOWNSTREAM END", bed=41.33, u0=-62,
         ground=[3.97, 3.92, 3.88, 3.84, 3.80, 3.78, 3.76, 3.74, 3.72, 3.42, 2.79, 2.16, 1.52, 0.95, 0.89, 0.82, 0.76, 0.70, 0.68, 0.66, 0.64, 0.61, 0.59, 0.57, 0.55, 0.52, 0.50, 0.48, 0.46, 0.44, 0.41, 0.39, 0.37, 0.35, 0.33, 0.32, 0.30, 0.29, 0.27, 0.26, 0.24, 0.23, 0.21, 0.20, 0.19, 0.17, 0.16, 0.14, 0.13, 0.11, 0.10, 0.08, 0.07, 0.06, 0.04, 0.03, 0.01, 0.00, 0.00, 0.01, 0.01, 0.02, 0.02, 0.02, 0.03, 0.03, 0.04, 0.04, 0.05, 0.05, 0.06, 0.06, 0.07, 0.07, 0.08, 0.08, 0.08, 0.09, 0.09, 0.10, 0.09, 0.11, 0.13, 0.16, 0.18, 0.21, 0.24, 0.26, 0.29, 0.32, 0.35, 0.38, 0.41, 0.43, 0.46, 0.49, 0.54, 0.59, 0.64, 0.70, 0.75, 0.80, 0.86, 0.91, 0.96, 1.02, 1.07, 1.12, 1.18, 1.23, 1.28, 1.34, 1.46, 1.65, 1.84, 2.03, 2.22, 2.41, 2.61, 2.80, 2.94, 3.06, 3.17, 3.29, 3.40],
         dep=(0.23, 0.69, 1.14, 1.38, 1.54),
         ext=[(-20.5, 23.5), (-44.0, 36.5), (-49.0, 45.0), (-49.5, 49.0), (-50.0, 50.0)],
         tags=[("slope", u"bed 1.09 %"), ("points", u"3 bed points within 25 m · floor interpolated"), ("spread", u"banks 114 m apart · floods wide and thin"),
               ("road", u"road 3.7 m wide · 52 m off · left bank"), ("pin", u"S4 detail: 280 m upstream")]),
    dict(key="up", name=u"1 · UPSTREAM ENTRY", bed=70.36, u0=-42,
         ground=[5.45, 5.24, 5.17, 5.11, 5.05, 4.99, 4.92, 4.86, 4.55, 4.18, 3.82, 3.45, 3.01, 2.57, 2.21, 2.14, 2.07, 2.00, 1.93, 1.86, 1.80, 1.73, 1.66, 1.59, 1.52, 1.45, 1.38, 1.32, 1.25, 1.19, 1.12, 1.06, 0.99, 0.93, 0.87, 0.80, 0.74, 0.67, 0.61, 0.54, 0.48, 0.41, 0.35, 0.29, 0.22, 0.16, 0.09, 0.03, 0.02, 0.39, 0.75, 1.10, 1.46, 1.82, 2.19, 2.54, 2.86, 3.16, 3.46, 3.75, 3.97, 4.05, 4.24, 4.46, 4.70, 4.94, 5.07, 5.08, 5.12, 5.14],
         dep=(0.64, 1.69, 2.57, 2.99, 3.30),
         ext=[(-4.0, 7.5), (-20.0, 10.5), (-28.5, 13.0), (-29.5, 14.0), (-30.5, 15.0)],
         tags=[("slope", u"bed 0.83 %"), ("points", u"73 bed points within 25 m"), ("road", u"road 6.5 m wide · 38 m off · right bank")]),
    dict(key="k4", name=u"2 · K4 BRIDGE", bed=64.77, u0=-80,
         ground=[3.06, 3.03, 3.01, 2.99, 2.96, 2.94, 2.92, 2.89, 2.87, 2.85, 2.82, 2.80, 2.78, 2.75, 2.73, 2.71, 2.68, 2.66, 2.64, 2.61, 2.59, 2.56, 2.54, 2.52, 2.49, 2.47, 2.45, 2.42, 2.40, 2.38, 2.35, 2.33, 2.31, 2.28, 2.26, 2.24, 2.21, 2.19, 2.17, 2.14, 2.12, 2.10, 2.07, 2.07, 2.07, 2.07, 2.07, 2.08, 2.08, 2.08, 2.08, 2.08, 2.08, 2.08, 2.08, 2.08, 2.08, 2.08, 2.08, 2.08, 1.77, 1.35, 0.93, 0.51, 0.14, 0.14, 0.13, 0.13, 0.12, 0.12, 0.12, 0.11, 0.11, 0.10, 0.10, 0.09, 0.09, 0.08, 0.08, 0.07, 0.07, 0.06, 0.06, 0.05, 0.05, 0.04, 0.04, 0.03, 0.03, 0.03, 0.02, 0.02, 0.14, 0.41, 0.68, 0.99, 1.94, 2.89, 3.84, 4.78, 5.73, 6.68, 7.63, 8.58, 9.53, 10.48, 10.87, 11.07, 11.27],
         dep=(0.28, 0.99, 1.83, 2.56, 2.84),
         ext=[(-16.0, 12.5), (-18.0, 15.0), (-20.0, 15.5), (-58.5, 16.5), (-70.5, 16.5)],
         tags=[("slope", u"bed 0.81 %"), ("flag", u"no stream/bank lines: spot heights + contours · 5 bed points"),
               ("over", u"right bank 2.1 m: street floods · Q100 0.2-0.4 m · Q500 0.5-0.7 m"),
               ("road", u"road 10-13 m wide · 42-52 m off · right bank")]),
    dict(key="k5", name=u"3 · K5 BRIDGE", bed=55.96, u0=-57,
         ground=[3.12, 3.11, 3.09, 3.08, 3.06, 3.05, 3.02, 2.97, 2.93, 2.89, 2.85, 2.80, 2.76, 2.72, 2.68, 2.63, 2.59, 2.55, 2.51, 2.46, 2.42, 2.38, 2.34, 2.29, 2.25, 2.20, 2.16, 2.11, 2.07, 1.99, 1.89, 1.78, 1.67, 1.56, 1.45, 1.36, 1.26, 1.17, 1.07, 0.95, 0.82, 0.69, 0.58, 0.47, 0.33, 0.19, 0.16, 0.13, 0.09, 0.06, 0.02, 0.00, 0.01, 0.02, 0.03, 0.05, 0.06, 0.07, 0.08, 0.09, 0.11, 0.12, 0.13, 0.14, 0.15, 0.17, 0.32, 1.03, 1.73, 2.43, 3.02, 3.60, 4.18, 4.73, 5.26, 5.77, 6.23, 6.66, 7.08, 7.43, 7.80, 8.09],
         dep=(0.31, 1.09, 1.95, 2.45, 2.79),
         ext=[(-12.5, 8.5), (-19.0, 10.0), (-27.5, 11.0), (-37.5, 12.0), (-45.5, 12.5)],
         tags=[("slope", u"bed 1.07 %"), ("points", u"12 bed points within 25 m"), ("spread", u"right bank rises gently: floods widen")]),
    dict(key="down", name=u"4 · DOWNSTREAM REACH", bed=45.67, u0=-42,
         ground=[4.61, 4.81, 5.00, 4.97, 4.66, 4.35, 4.05, 3.74, 3.44, 3.13, 2.83, 2.50, 2.15, 1.80, 1.45, 1.11, 0.76, 0.41, 0.06, 0.01, 0.02, 0.03, 0.05, 0.06, 0.08, 0.09, 0.10, 0.11, 0.12, 0.12, 0.13, 0.14, 0.15, 0.15, 0.16, 0.16, 0.16, 0.16, 0.16, 0.16, 0.16, 0.16, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.24, 0.43, 0.62, 0.80, 0.86, 0.91, 0.97, 1.02, 1.08, 1.13, 1.19, 1.24, 1.44, 1.81, 2.19, 2.56, 2.93, 3.35, 3.76, 4.06, 4.08, 4.08, 4.05, 4.02, 3.99, 3.95, 3.86],
         dep=(0.31, 0.96, 1.68, 2.05, 2.33),
         ext=[(-24.5, 6.0), (-26.5, 11.5), (-28.5, 18.5), (-29.5, 19.5), (-30.5, 20.0)],
         tags=[("slope", u"bed 0.98 %"), ("points", u"2 bed points within 25 m · bed interpolated"), ("road", u"road 5-9 m wide · 25-30 m off · left bank")]),
    dict(key="dsi", name=u"DSİ PLANNED CHANNEL 20 x 3 m", bed=None, u0=-16,
         ground=[3.0] * 7 + [0.0] * 19 + [3.0] * 7,
         dep=(0.22, 1.07, 2.20, 2.87, 3.39),
         ext=[(-10.0, 10.0)] * 5,
         tags=[("pin", u"20.00 m bed · 3.00 m deep · 3,720 m " + cite(u"SYGM North Aegean flood management plan 2019, p.75; depths on the design trapezoid, walls above 3 m taken as vertical"))]),
]
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
    _DET_PROF[:] = [prof]                   # v1.9: the booklet's S4 cuts use the same ground
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


def sketch_engine():
    if not _SK:
        ns = {"__name__": "pr1_sketches", "_tree_rand": _tree_rand}   # reeds use the trees' random stream
        exec(compile(SKETCH_SRC, "pr1_sketches", "exec"), ns)
        _SK.append(ns)
    return _SK[0]


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
SPECIES = [  # v1.8: band, latin, local name, evidence as pictogram chips (figures as in the files), its source, flag
    ("B", u"Typha angustifolia", u"narrow-leaf cattail", [("flood", u"70 cm water: 72 % biomass kept")], u"Song 2021", "", "C"),
    ("B", u"Phragmites australis", u"kamış / saz", [("flood", u"70 cm continuous: 100 % die"), ("clean", u"TN 41–44 %")],
     u"Song 2021; Turkish VF pilot, Korkusuz et al. 2004", u"spreads aggressively", "C+R"),
    ("B", u"Iris pseudacorus", u"sarı süsen", [("flood", u"flooded up to 6 months")], u"FEIS", u"POISONOUS", "R"),
    ("B", u"Juncus acutus", u"sharp rush", [("clean", u"Fe2+ 62 %")],
     u"Turkish HSSF wetland Kızılcaören, Aydın Temel et al. 2017", "", "R"),
    ("B", u"Mentha aquatica", u"su nanesi", [("clean", u"COD 71.3–91.4 % · BOD5 75.3–91.0 %")], u"HSSF wetland, Avelar 2012",
     u"aromatic (chemistry not verified)", "R"),
    ("C", u"Salix alba", u"ak söğüt", [("flood", u"inundation-tolerant"), ("days", u"50–150 d/yr")],
     u"JRC Atlas 'noticeably tolerant to inundation'; RWS 2023", "", "C+R"),
    ("C", u"Tamarix smyrnensis", u"ılgın", [("flood", u"long inundation (genus)"), ("native", u"native · İzmir")],
     u"JRC Atlas 'can survive prolonged periods of inundation'", "", "R"),
    ("C", u"Vitex agnus-castus", u"hayıt", [("dry", u"intermittent streams · 92D0")], u"Salinas & Cueto 2009",
     u"aromatic (not verified)", "R"),
    ("C", u"Nerium oleander", u"zakkum", [("dry", u"streams dry most of the year")], u"Salinas & Cueto 2009",
     u"HIGHLY TOXIC: not near play", "C+R"),
    ("D", u"Lythrum salicaria", u"aklar otu", [("flood", u"quite flood-tolerant"), ("clean", u"TN > 60 %")],
     u"FEIS 'quite flood tolerant'; Xie et al. 2021", "", "R"),
    ("D", u"Carex pendula, Juncus effusus", u"sedge, soft rush", [("flood", u"shallow-water banks (general)")],
     u"USDA NRCS TN-38", "", "R"),
    ("E", u"Fraxinus angustifolia", u"dişbudak", [("flood", u"temporary flooded lowlands")],
     u"JRC Atlas 'grows well ... in temporary flooded lowlands'", "", "R"),
    ("E", u"Populus alba", u"ak kavak", [("flood", u"waterlogged"), ("dry", u"to drought")],
     u"JRC Atlas 'tolerating from waterlogged to drought habitats'", u"root suckers", "R"),
    ("E", u"Platanus orientalis", u"çınar", [("dry", u"torrent gravels · drought-sensitive")],
     u"EUNIS G1.381; Velikova et al. 2018", "", "C+R"),
    ("E", u"Quercus robur, Ulmus laevis", u"oak, elm", [("days", u"oak 96 d/yr · elm ≤ 119 d/yr")],
     u"hardwood floodplain, Schindler et al. 2022", "", "C"),
    ("F", u"Lavandula stoechas", u"karabaş otu", [("flood", u"17 days flooded: survived"), ("dry", u"xerophyte")],
     u"RHS trial; RHS", u"scent layer", "R"),
    ("-", u"Arundo donax", u"kargı", [("warn", u"flood risk up · blocks watercourses, bridges")],
     u"Bruno et al. 2019 'increased flooding risk'", u"REMOVE, do not plant", "R"),
]
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
        with open(os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "output", "bergama_booklet",
                               "booklet_slots.json"), encoding="utf-8") as f:
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
    """Collects one script's booklet blocks and writes output/<folder>/booklet/blocks.json."""
    def __init__(self, out_dir, script, version):
        self.dir = os.path.join(out_dir, "booklet")
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


# ---------------------------------------------------------------- A3 booklet (v1.9; SCRIPT_STANDARD §8, booklet/ASSET_SPEC.md)
# One text-free vector PDF per booklet frame, drawn for the frame's own size (bk_frame), and every word as a label in
# booklet/blocks.json (the assembler sets them as live text). Figures come from this script's own tables and cuts.
# Booklet drawings are option A only. Words: the plan's labels; the site's watercourse is the Selinos "stream".
BK_SLOTS = {"b1_hero": (260.0, 176.0), "b1_side": (128.0, 176.0), "b2_hero": (260.0, 176.0), "b4_side": (128.0, 176.0),
            "b5_strip": (392.0, 56.0), "b5_hero": (260.0, 176.0), "c6_s1": (293.0, 56.0), "c6_s2": (293.0, 56.0),
            "c6_s3": (293.0, 56.0), "c6_s4": (293.0, 56.0), "c8_a": (194.0, 176.0)}
BK_PT, BK_KEY = 7.5, 9.5             # label sizes, pt (key labels up to 9.5)
BK_INK, BK_INK2, BK_ACC = "4A3F35", "6B645B", "8B3A3F"
_DET_PROF = []                       # the S4 ground profile draw_detail used (survey re-cut or embedded)


def bk_disp(s):
    """A label as the assembler prints it, for measuring: {src:..} -> [00], {val:..} -> a 7-figure number."""
    import re
    return re.sub(r"\{val:[^}]+\}", u"000,000", re.sub(r"\{src:[^}]+\}", u"[00]", s))


def bk_box(s, x, y, size, bold=False, align="L"):
    """The assembler's label box (mm, y down): baseline y, width measured at size pt."""
    w = text_w(bk_disp(s), size * PT, bold)
    bx = x - (w / 2.0 if align == "C" else w if align == "R" else 0.0)
    return (bx, y - size * PT * 0.72, bx + w, y + size * PT * 0.21)


def bk_hit(a, b, pad=0.0):
    return a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad


class BkPage(Page):
    """A booklet drawing at its frame's size. Geometry calls here take y DOWN from the top (as the labels do);
    text items carry their size in pt and become labels (never PDF text)."""

    def __init__(self, key):
        w, h = bk_frame(OUT_FOLDER + "/" + key, *BK_SLOTS[key])
        Page.__init__(self, w, h)
        self.key = key

    def ln(self, pts, col, lw=0.25, dash=None, cap=1):
        self.line([(x, self.H - y) for x, y in pts], col, lw, dash, cap)

    def pl(self, rings, fill=None, stroke=None, lw=0.2, dash=None, alpha=None):
        self.poly([[(x, self.H - y) for x, y in r] for r in rings], fill, stroke, lw, dash, None, None, alpha)

    def rc(self, x0, y0, x1, y1, fill=None, stroke=None, lw=0.2, alpha=None):
        self.pl([rect(x0, y0, x1, y1)], fill, stroke, lw, None, alpha)

    def ic(self, kind, x, y, sz):
        icon(self, kind, x, self.H - y, sz)

    def boxes(self):
        return [bk_box(it[1], it[2], self.H - it[3], it[4], it[6], it[7]) for it in self.items if it[0] == "text"]

    def fits(self, s, x, y, size=BK_PT, bold=False, align="L", pad=0.8):
        b = bk_box(s, x, y, size, bold, align)
        if b[0] < 0.4 or b[2] > self.W - 0.4 or b[1] < 0.4 or b[3] > self.H - 0.4:
            return False
        return not any(bk_hit(b, o, pad) for o in self.boxes())

    def lab(self, s, x, y, size=BK_PT, colour=BK_INK, bold=False, align="L"):
        self.text(s, x, self.H - y, size, colour, bold, align)
        return bk_box(s, x, y, size, bold, align)

    def lab_near(self, s, cands, size=BK_PT, colour=BK_INK, bold=False, anchor=None, lead=None):
        """The first candidate (x, y, align) where the label fits; a thin leader from the label to anchor."""
        pick = next((c for c in cands if self.fits(s, c[0], c[1], size, bold, c[2])), cands[0])
        b = self.lab(s, pick[0], pick[1], size, colour, bold, pick[2])
        if anchor:
            ex = min(max(anchor[0], b[0]), b[2])
            ey = b[3] + 0.4 if anchor[1] > b[3] else (b[1] - 0.4 if anchor[1] < b[1] else (b[1] + b[3]) / 2.0)
            if abs(ex - anchor[0]) + abs(ey - anchor[1]) > 1.0:
                self.ln([(ex, ey), anchor], lead or colour, 0.15)
        return b

    def finish(self):
        """Lines never under 0.1 mm."""
        out = []
        for it in self.items:
            if it[0] == "poly":
                it = it[:4] + (max(0.1, it[4]),) + it[5:]
            elif it[0] == "line":
                it = it[:3] + (max(0.1, it[3]),) + it[4:]
            elif it[0] == "circle":
                it = it[:6] + (max(0.1, it[6]),)
            out.append(it)
        self.items = out


def bk_check(labels, W, H):
    """What the assembler would log for this frame: overlapping labels, labels outside the frame, type too small."""
    probs, boxes = [], []
    for lb in labels:
        b = bk_box(lb["text"], lb["x"], lb["y"], lb["size"], lb["bold"], lb["anchor"])
        if any(bk_hit(b, o) for o in boxes):
            probs.append(u"labels overlap: " + lb["text"][:30])
        if b[0] < 0 or b[2] > W or b[1] < 0 or b[3] > H:
            probs.append(u"label outside the frame: " + lb["text"][:30])
        if lb["size"] < BK_PT:
            probs.append(u"label below 7.5 pt: " + lb["text"][:30])
        boxes.append(b)
    return probs


def bk_scalebar(pg, x1, y, metres, k):
    """Scale bar ending at x1 (mm), baseline y; two halves; its numbers are labels."""
    L = metres * k
    x0 = x1 - L
    pg.rc(x0, y - 1.6, x0 + L / 2.0, y - 0.4, fill=BK_INK)
    pg.rc(x0 + L / 2.0, y - 1.6, x1, y - 0.4, fill="FFFFFF", stroke=BK_INK, lw=0.15)
    pg.lab(u"0", x0 - 1.2, y, align="R", colour=BK_INK2)
    pg.lab(u"{:.0f} m".format(metres), x1 + 1.2, y, colour=BK_INK2)


def bk_months(pg, X, y):
    for i, m in enumerate(WY):
        pg.lab(MONTHS[m][0], X(i), y, colour=BK_INK2, align="C")


# ---------------------------------------------------------------- B1 hero: the year of the water
def bk_year(pg, res):
    H = pg.H
    gx0, gx1, rx = 16.0, 192.0, 198.0
    mw = (gx1 - gx0) / 12.0

    def X(i):
        return gx0 + (i + 0.5) * mw

    def grid(yb, h, vmax, ticks, fmt):
        for t in ticks:
            yy = yb - h * t / vmax
            pg.ln([(gx0, yy), (gx1, yy)], COL["faint"], 0.12)
            pg.lab(fmt(t), gx0 - 1.6, yy + 0.95, colour=BK_INK2, align="R")
        pg.ln([(gx0, yb), (gx1, yb)], COL["ink2"], 0.25)
    # ---- row 1: rain and open-water evaporation
    yb, h, vmax = 46.0, 35.0, 220.0
    pg.rc(gx0, 3.9, gx0 + 3.2, 6.0, fill=C["w3"])
    b = pg.lab(YEAR_SRC[0][0], gx0 + 4.4, 6.0, bold=True)
    pg.rc(b[2] + 6.0, 3.9, b[2] + 9.2, 6.0, fill=C["structure"])
    b = pg.lab(u"open-water evaporation", b[2] + 10.4, 6.0)
    pg.lab(u"+ = rain > evaporation", b[2] + 8.0, 6.0, colour=C["d3"], bold=True)
    grid(yb, h, vmax, (0, 100, 200), lambda t: u"{:.0f}".format(t))
    for i, m in enumerate(WY):
        x = gx0 + i * mw
        hr, he = h * RAIN[m] / vmax, h * EVAP[m] / vmax
        pg.rc(x + 0.12 * mw, yb - hr, x + 0.48 * mw, yb, fill=C["w3"])
        pg.rc(x + 0.52 * mw, yb - he, x + 0.88 * mw, yb, fill=C["structure"])
        if RAIN[m] > EVAP[m]:
            cx, cy = x + 0.30 * mw, yb - hr - 2.4
            pg.ln([(cx - 1.1, cy), (cx + 1.1, cy)], C["d3"], 0.4)
            pg.ln([(cx, cy - 1.1), (cx, cy + 1.1)], C["d3"], 0.4)
    jul = WY.index(6)
    x = gx0 + jul * mw
    d_jul = RAIN[6] - EVAP[6]
    yr, ye = yb - h * RAIN[6] / vmax, yb - h * EVAP[6] / vmax
    pg.ln([(x + 0.5 * mw, yr), (x + 0.5 * mw, ye)], BK_ACC, 0.35)
    for yy in (yr, ye):
        pg.ln([(x + 0.5 * mw - 1.0, yy), (x + 0.5 * mw + 1.0, yy)], BK_ACC, 0.35)
    pg.ln([(x + 0.5 * mw, ye - 0.6), (x + 0.5 * mw, 10.6), (rx - 1.0, 10.6)], BK_ACC, 0.15)
    pg.lab(u"July: {:.1f} mm".format(d_jul), rx, 11.6, colour=BK_ACC, bold=True)
    res["year"] = {"rain_mm_year": round(sum(RAIN), 1), "evaporation_mm_year": round(sum(EVAP), 1),
                   "july_rain_minus_evaporation_mm": round(d_jul, 1),
                   "surplus_months": [MONTHS[m] for m in WY if RAIN[m] > EVAP[m]]}
    # ---- row 2: the stream past the site
    yb, h, vmax = 98.0, 34.0, 7.5e6
    pg.lab(u"stream, million m³ a month", gx0, 58.0, bold=True)
    grid(yb, h, vmax, (0, 2e6, 4e6, 6e6), lambda t: u"{:.0f}".format(t / 1e6))
    win = set(WY.index(m) for m in (11, 0, 1, 2, 3))
    for i, m in enumerate(WY):
        x = gx0 + i * mw
        hh = max(0.25, h * RIVER[m] / vmax)
        pg.rc(x + 0.15 * mw, yb - hh, x + 0.85 * mw, yb, fill=MP["discharge"][2] if i in win else MP["discharge"][0])
    a, b_ = min(win), max(win)
    yk = yb - h * max(RIVER) / vmax - 2.2
    pg.ln([(gx0 + a * mw + 1.0, yk + 1.2), (gx0 + a * mw + 1.0, yk), (gx0 + (b_ + 1) * mw - 1.0, yk),
           (gx0 + (b_ + 1) * mw - 1.0, yk + 1.2)], MP["discharge"][2], 0.3)
    pg.lab(u"Dec-Apr: storage fills", gx0 + (b_ + 1) * mw + 1.5, yk + 1.0, colour=MP["discharge"][2], bold=True)
    dry = [WY.index(m) for m in (6, 7, 8)]
    yd = yb - h * max(RIVER[m] for m in (6, 7, 8)) / vmax - 3.0
    pg.ln([(gx0 + dry[0] * mw + 1.0, yd + 1.2), (gx0 + dry[0] * mw + 1.0, yd), (gx1 - 1.0, yd), (gx1 - 1.0, yd + 1.2)],
          BK_INK2, 0.3)
    pg.lab(u"Jul-Sep: trickle or dry bed", gx1 - 1.0, yd - 1.6, colour=BK_INK2, align="R")
    tot = float(sum(RIVER))
    res["year"].update({"stream_m3_year": int(sum(RIVER)),
                        "stream_dec_apr_pct": round(100.0 * sum(RIVER[m] for m in (11, 0, 1, 2, 3)) / tot, 1),
                        "stream_jul_sep_m3_month": [RIVER[m] for m in (6, 7, 8)]})
    # ---- row 3: mean depth in the bed
    yb, h, vmax = 157.0, 44.0, 0.7

    def Yd(v):
        return yb - h * min(v, vmax) / vmax
    pg.lab(u"mean depth in the bed, m", gx0, 109.0, bold=True)
    grid(yb, h, vmax, (0.0, 0.2, 0.4, 0.6), lambda t: u"{:.1f}".format(t))
    pg.ln([(gx0, Yd(STRIP_DEPTH)), (gx1, Yd(STRIP_DEPTH))], MP["storage"][2], 0.4, dash=[1.2, 0.8])
    pg.lab(u"strip {:.2f} m (design)".format(STRIP_DEPTH), gx1 - 1.0, Yd(STRIP_DEPTH) - 1.2, colour=MP["storage"][2],
           bold=True, align="R")
    series = [(u"upstream entry", ("up",), MP["discharge"][1], 0.5, [1.4, 0.7]),
              (u"K4 · K5 · downstream reach", ("k4", "k5", "down"), "3C5159", 0.5, None),
              (u"flat downstream end", ("flat",), MP["discharge"][2], 0.9, None)]
    ly = 116.0
    for lab, keys, colr, lw, dash in series:
        lo = [min(DEPTH[k][g][WY[i]] for k in keys for g in (0, 1)) for i in range(12)]
        hi = [max(DEPTH[k][g][WY[i]] for k in keys for g in (0, 1)) for i in range(12)]
        pg.pl([[(X(i), Yd(hi[i])) for i in range(12)] + [(X(i), Yd(lo[i])) for i in range(11, -1, -1)]],
              fill=colr, alpha=0.15)
        pg.ln([(X(i), Yd(hi[i])) for i in range(12)], colr, lw, dash=dash)
        pg.ln([(rx, ly - 0.9), (rx + 6.0, ly - 0.9)], colr, max(lw, 0.5), dash=dash)
        pg.lab(lab, rx + 7.5, ly)
        ly += 4.6
    pg.lab(u"low-flow depths indicative", rx, ly + 1.0, colour=BK_INK2)
    bk_months(pg, X, 163.5)


# ---------------------------------------------------------------- B1 side: greenness by month
def bk_ndvi(pg, res):
    gx0, gx1, yt, yb = 14.0, 124.0, 16.0, 156.0
    mw = (gx1 - gx0) / 12.0
    v0, v1 = 0.10, 0.35

    def X(i):
        return gx0 + (i + 0.5) * mw

    def Yn(v):
        return yb - (yb - yt) * (v - v0) / (v1 - v0)
    pg.lab(YEAR_SRC[5][0], gx0, 6.0, bold=True)
    for t in (0.1, 0.2, 0.3):
        pg.ln([(gx0, Yn(t)), (gx1, Yn(t))], COL["faint"], 0.12)
        pg.lab(u"{:.1f}".format(t), gx0 - 1.6, Yn(t) + 0.95, colour=BK_INK2, align="R")
    pg.ln([(gx0, yb), (gx1, yb)], COL["ink2"], 0.25)
    dates = {}
    for doy, word, nm in ((LEAF_OFF, u"leaf-fall", "leaf_fall"), (LEAF_ON, u"leaf-out", "leaf_out")):
        d = datetime.date(2021, 1, 1) + datetime.timedelta(days=doy - 1)
        dates[nm] = u"{} {}".format(d.day, MONTHS[d.month - 1])
        xx = gx0 + wy_pos(doy) * mw
        pg.ln([(xx, yt - 1.0), (xx, yb)], "495338", 0.25, dash=[0.8, 0.8])
        pg.lab(u"{} {}".format(word, dates[nm]), xx + 1.0, yt + 2.0, colour="495338")
    rip, rest = NDVI[0][4], NDVI[1][4]
    pg.ln([(X(i), Yn(rest[WY[i]])) for i in range(12)], COL["structure"], 0.6, dash=[1.2, 0.8])
    pg.ln([(X(i), Yn(rip[WY[i]])) for i in range(12)], "495338", 0.7)
    top3 = min(Yn(rip[WY[i]]) for i in range(3))
    pg.lab(u"riparian strip, 0-30 m", gx0 + 1.0, top3 - 3.0, colour="495338", bold=True)
    pg.lab(u"rest of the site frame", gx0 + 1.0, max(Yn(rest[WY[i]]) for i in range(3)) + 5.0, colour=BK_INK2)
    j = WY.index(6)
    ya, yb_ = Yn(rip[6]), Yn(rest[6])
    pg.ln([(X(j), ya + 1.4), (X(j), yb_ - 1.4)], BK_ACC, 0.35)
    for yy in (ya + 1.4, yb_ - 1.4):
        pg.ln([(X(j) - 1.0, yy), (X(j) + 1.0, yy)], BK_ACC, 0.35)
    pg.lab(u"July: {:.2f} vs {:.2f}".format(rip[6], rest[6]), X(j) - 1.8, (ya + yb_) / 2.0 + 1.0, colour=BK_ACC,
           bold=True, align="R")
    bk_months(pg, X, yb + 6.0)
    res["greenness"] = {"july_riparian": rip[6], "july_rest_of_frame": rest[6], "leaf_out": dates["leaf_out"],
                        "leaf_fall": dates["leaf_fall"]}


# ---------------------------------------------------------------- B2 hero: six surveyed cuts at one scale
BK_CUT_NAMES = {"up": u"upstream entry", "k4": u"K4 bridge", "k5": u"K5 bridge", "down": u"downstream reach",
                "s4": u"S4 cut", "flat": u"flat downstream end"}


def bk_s4_cut(res_log=None):
    """The S4 cut in the form of CUTS: ground every 1 m above the bed low point, bed, the three drawn levels and
    their wet widths, the road edges; levels as the S4 detail prints them."""
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


def bk_bank_top(g, i0, step):
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


def bk_cuts(pg, res):
    W, H = pg.W, pg.H
    k = 1000.0 / 1500.0                                 # 1:1,500 across, vertical x8
    ky = 8.0 * k
    cuts = {c["key"]: c for c in CUTS}
    cuts["s4"] = bk_s4_cut()
    order = [["up", "k4", "k5"], ["down", "s4", "flat"]]
    cw, rh = W / 3.0, (H - 10.0) / 2.0
    res["cuts"] = {}
    over_labels = []
    for r, row in enumerate(order):
        top = max(max(d for d in cuts[c]["dep"] if d is not None) for c in row) + 0.8
        y0 = r * rh + 4.0 + max(0.0, (rh - (9.0 + (top + 0.6) * ky + 19.0)) / 2.0)   # the row's content centred
        ybed = y0 + 9.0 + top * ky
        for c_, key in enumerate(row):
            cut = cuts[key]
            g, u0, dep, ext = cut["ground"], cut["u0"], cut["dep"], cut["ext"]
            wd = (len(g) - 1) * k
            xl = c_ * cw + (cw - wd) / 2.0

            def T(u, z):
                return (xl + (u - u0) * k, ybed - z * ky)
            pg.lab(BK_CUT_NAMES[key], xl, y0 + 4.0, size=8.5, bold=True)
            # ground
            top_pts = [T(u0 + i, min(z, top)) for i, z in enumerate(g)]
            pg.pl([top_pts + [T(u0 + len(g) - 1, -0.6), T(u0, -0.6)]], fill=COL["structure"])
            pg.ln(top_pts, COL["ink"], 0.3)
            i0 = min(range(len(g)), key=lambda i: g[i])
            # overtopping: Q100 / Q500 above the first bank top on either side
            info = {"bed": round(cut["bed"], 2), "highest_day_m": round(dep[1], 2), "q100_m": round(dep[3], 2),
                    "q500_m": round(dep[4], 2), "q100_level": round(cut["bed"] + dep[3], 2),
                    "q500_level": round(cut["bed"] + dep[4], 2)}
            for step, side in ((-1, "right"), (1, "left")):
                bt = bk_bank_top(g, i0, step)
                if not bt:
                    continue
                toe, tp = bt
                flooded = []
                for lev in (3, 4):
                    a, b = ext[lev]
                    reach = (a - u0) if step < 0 else (b - u0)
                    if dep[lev] > g[tp] + 0.005 and (reach - tp) * step > 0.5:
                        end = int(round(reach))
                        idx = list(range(tp, end + step, step))
                        idx = [i for i in idx if 0 <= i < len(g)]
                        ring = [T(u0 + i, dep[lev]) for i in idx] + [T(u0 + i, min(g[i], dep[lev])) for i in idx[::-1]]
                        pg.pl([ring], fill=BK_ACC, alpha=0.35)
                        flooded.append(lev)
                if flooded:
                    pg.ln([T(u0 + i, g[i]) for i in range(toe, tp + step, step)], BK_ACC, 0.9)
                    info["over_%s_bank_q500_m" % side] = round(dep[4] - g[tp], 2)
                    info["%s_bank_top_m" % side] = round(g[tp], 2)
                    xe = T(ext[4][0] if step < 0 else ext[4][1], 0)[0]
                    xt = T(u0 + tp, 0)[0]
                    over_labels.append((key, side, round(dep[4] - g[tp], 2), T(u0 + tp, dep[4]),
                                        (min(xe, xt), max(xe, xt)), y0))
            # levels
            for lev, colr, lw in ((1, LEVEL_COL[1], 0.4), (3, LEVEL_COL[3], 0.55), (4, LEVEL_COL[4], 0.7)):
                a, b = ext[lev]
                pg.ln([T(a, dep[lev]), T(b, dep[lev])], colr, lw)
            if cut.get("road"):
                ra, rb = cut["road"]
                za = max(g[int(round(ra - u0))], g[int(round(rb - u0))])
                pg.rc(T(ra, 0)[0], T(0, za)[1] - 0.9, T(rb, 0)[0], T(0, za)[1] - 0.1, fill=BK_INK)
                rx_ = (T(ra, 0)[0] + T(rb, 0)[0]) / 2.0
                pg.lab_near(u"road", [(rx_, ybed + 0.6 * ky + 3.8, "C"), (rx_, T(0, za)[1] + 4.6, "C")],
                            colour=BK_INK2, anchor=(rx_, T(0, za)[1] - 0.2), lead=BK_INK)
            base = ybed + 0.6 * ky
            if r == 0 and c_ == 0:
                pg.lab(u"right bank", xl, base + 3.8, colour=BK_INK2)
                pg.lab(u"left bank", xl + wd, base + 3.8, colour=BK_INK2, align="R")
            yy = base + 8.0
            for t, colr in ((u"bed {:+.2f}".format(cut["bed"]), BK_INK),
                            (u"highest day {:.2f} m".format(dep[1]), LEVEL_COL[1]),
                            (u"Q100 {:.2f} m ({:+.2f})".format(dep[3], cut["bed"] + dep[3]), LEVEL_COL[3]),
                            (u"Q500 {:.2f} m ({:+.2f})".format(dep[4], cut["bed"] + dep[4]), LEVEL_COL[4])):
                pg.lab(t, xl, yy, colour=colr, bold=t.startswith(u"Q"))
                yy += 3.5
            res["cuts"][key] = info
    for key, side, d, anc, (xa, xb), y0 in over_labels:
        t = u"over the {} bank".format(side) + (u" by {:.2f} m".format(d) if key == "s4" else u"")
        xm = (xa + xb) / 2.0
        pg.lab_near(t, [(xm, anc[1] - 3.0, "C"), (xa, anc[1] - 3.0, "L"), (xb, anc[1] - 3.0, "R"),
                        (xm, anc[1] - 6.5, "C"), (xa, y0 + 7.5, "L")], colour=BK_ACC, bold=True,
                    anchor=(xm, anc[1] + 0.8))
    bk_scalebar(pg, W - 12.0, H - 3.0, 50.0, k)
    res["cuts_scale"] = "1:1,500 across, vertical x8"


# ---------------------------------------------------------------- B4 side: storage cubes to scale
def bk_cubes(pg, res):
    W, H = pg.W, pg.H
    k = 1000.0 / 1250.0
    mix = u"orchard olive + cropland cotton"
    try:
        v_seal = float(WB["today_strip_storage"][mix]["storage_m3"])
    except Exception:
        v_seal = VOL_SEALED
    try:
        v_cut = float(WB["design"]["storage_m3"])
    except Exception:
        v_cut = float(WB_STORE[1])
    e1, e2, e3, e4 = [v ** (1.0 / 3.0) for v in (VOL_FIRST, v_seal, VOL_UNSEALED, v_cut)]

    def cube(e, tones, solid, dash=None):
        tmp = Page(0, 0)
        draw_cube(tmp, BoxView(PSI, 0.0, k, 0.0, 0.0), 0, 0, e, tones, solid, dash)
        return tmp

    def put(part, x, y_bottom):
        """Place a part (y up) with its bbox left at x and its bottom at y_bottom (y down); returns the bbox, y down."""
        bb = items_bbox(part.items)
        dx, dy = x - bb[0], (H - y_bottom) - bb[1]
        pg.items += xform(part.items, 1.0, dx, dy)
        return (x, y_bottom - (bb[3] - bb[1]), x + bb[2] - bb[0], y_bottom)
    nest = cube(e2, MP["storage"], True)
    nest.items += cube(e3, MP["storage"], False).items
    big = cube(e4, MP["discharge"], False, [1.6, 0.8])
    small = cube(e1, MP["discharge"], True)
    bb_big = put(big, 3.0, H - 10.0)
    bb_nest = put(nest, 3.0, bb_big[1] - 6.0)
    x_lab = bb_nest[2] + 4.0
    bb_small = put(small, x_lab, bb_nest[1] + (items_bbox(small.items)[3] - items_bbox(small.items)[1]))
    y = bb_small[1] + 3.0
    pg.lab(u"first fill {:,.0f} m³".format(VOL_FIRST), bb_small[2] + 2.5, bb_small[1] + 4.0, bold=True)
    pg.lab(u"strip: 2,949 m x 4 m x {:.2f} m".format(STRIP_DEPTH), bb_small[2] + 2.5, bb_small[1] + 7.6,
           colour=BK_INK2)
    y = max(bb_small[3], bb_small[1] + 8.0) + 8.0
    for t, bold, colr in ((u"strip, sealed bed {val:Bergama_water_balance_analysis/water_balance_results.json:"
                           u"today_strip_storage.orchard olive + cropland cotton.storage_m3|0} m³", True, BK_INK),
                          (u"unsealed bed: ≥ {:,.0f} m³".format(VOL_UNSEALED), True, BK_INK),
                          (u"worst case -30.7 % {src:mgm_2025_deficit}", False, BK_INK2),
                          (u"seepage 5 / 25 mm a day {src:fao_seepage}", False, BK_INK2)):
        pg.lab(t, x_lab, y, bold=bold, colour=colr)
        y += 3.8
    xb = bb_big[2] + 3.0
    pg.lab(u"cut-off {val:Bergama_water_balance_analysis/water_balance_results.json:design.storage_m3|0} m³",
           xb, bb_big[1] + 12.0, bold=True)
    bk_scalebar(pg, W - 10.0, H - 3.0, 20.0, k)
    res["storage"] = {"first_fill_m3": VOL_FIRST, "strip_sealed_m3": v_seal, "strip_unsealed_m3": VOL_UNSEALED,
                      "cut_off_m3": v_cut, "edges_m": [round(e, 1) for e in (e1, e2, e3, e4)], "scale": "1:1,250"}


# ---------------------------------------------------------------- B5 strip: one way, with the stream (pictograms)
BK_CHAIN = [("sewer_x", u"0 sewer: 3 km + 500 m {src:gercek_izmir_sewer}", u"completion not verified"),
            ("rain", u"1 stream in · mostly winter", None), ("reed", u"2 reed beds clean once", None),
            ("tank", u"3 terraces hold runoff", None), ("cube", u"4 basins hold winter water", None),
            ("over", u"5 spillway to the stream", None),
            ("strip", u"6 strip 4 m x {:.2f} m".format(STRIP_DEPTH), u"only above legal minimum flow"),
            ("flood", u"7 strip waters planting", None), ("spread", u"8 floods onto terraces", None),
            ("clean", u"10 clean stream leaves", None), ("farm", u"11 farmland outside", None)]


def bk_chain(pg, res):
    W, H = pg.W, pg.H
    n = len(BK_CHAIN)
    sw, sz, yi = W / n, 13.0, 9.5
    for i, (kind, t, sub) in enumerate(BK_CHAIN):
        cx = (i + 0.5) * sw
        pg.ic(kind, cx - sz / 2.0, yi, sz)
        if i % 2 == 0:
            pg.lab(t, cx, yi + sz + 6.0, align="C")
            if sub:
                pg.lab(sub, cx, yi + sz + 9.6, align="C", colour=BK_INK2)
        else:
            pg.lab(t, cx, yi - 3.2, align="C")
        if 0 < i < n - 1:
            arrow(pg, [(cx + sz / 2.0 + 1.5, H - yi - sz / 2.0), (cx + sw - sz / 2.0 - 1.5, H - yi - sz / 2.0)],
                  C["w3"], 0.6, 2.2)
    yr = H - 9.0
    xa, xb = 1.5 * sw, (n - 1.5) * sw
    pg.ln([(xa + 2.0, yr), (xb, yr)], BK_INK2, 0.35, dash=[1.2, 0.8])
    pg.pl([[(xa, yr), (xa + 2.4, yr - 1.0), (xa + 2.4, yr + 1.0)]], fill=BK_INK2)
    xm = (xa + xb) / 2.0
    pg.ln([(xm - 2.2, yr - 2.2), (xm + 2.2, yr + 2.2)], BK_ACC, 0.6)
    pg.ln([(xm - 2.2, yr + 2.2), (xm + 2.2, yr - 2.2)], BK_ACC, 0.6)
    pg.lab(u"no pumping back", xm + 4.0, yr + 1.0, colour=BK_ACC, bold=True)
    pg.lab(u"gravity · no pumps", xa - 3.0, yr + 1.0, colour=MP["discharge"][2], bold=True, align="R")


# ---------------------------------------------------------------- B5 hero: what reed beds remove, coliforms left
def bk_cleaning(pg, res):
    W, H = pg.W, pg.H
    x0, x1, yt, yb = 16.0, 150.0, 14.0, 128.0
    pg.lab(u"% removed", x0, 7.0, bold=True)
    for t in (0, 50, 100):
        yy = yb - (yb - yt) * t / 100.0
        pg.ln([(x0, yy), (x1, yy)], COL["faint"], 0.12)
        pg.lab(str(t), x0 - 1.6, yy + 0.95, colour=BK_INK2, align="R")
    cols = [C["wet1"], C["d2"], C["wet"]]
    gw = (x1 - x0) / len(WETLAND_KEYS)
    bw = gw * 0.78 / len(WETLAND)
    for i, nm in enumerate(WETLAND_KEYS):
        for j, (_, vals) in enumerate(WETLAND):
            bx = x0 + i * gw + gw * 0.11 + j * bw
            pg.rc(bx, yb - (yb - yt) * vals[i] / 100.0, bx + bw * 0.9, yb, fill=cols[j])
        pg.lab(u"solids" if nm == u"Solids" else nm.replace(u"Total", u"total"), x0 + (i + 0.5) * gw, yb + 5.0,
               align="C")
    pg.ln([(x0, yb), (x1, yb)], COL["ink2"], 0.25)
    for j, (nm, _) in enumerate(WETLAND):
        yy = yb + 15.0 + j * 4.6
        pg.rc(x0, yy - 2.4, x0 + 4.0, yy - 0.2, fill=cols[j])
        pg.lab(nm.lower() if j else nm[0].lower() + nm[1:], x0 + 5.5, yy)
    res["cleaning"] = {"removal_pct": {nm: dict(zip(WETLAND_KEYS, vals)) for nm, vals in WETLAND}}
    # coliforms, log scale 1 - 10^6 per 100 ml
    ax, yt2, yb2 = 176.0, 18.0, 150.0
    dec = (yb2 - yt2) / 6.0

    def Yl(v):
        return yb2 - dec * (math.log10(v) if v > 0 else 0.0)
    pg.lab(u"coliforms per 100 ml", ax - 12.0, 7.0, bold=True)
    for e in range(7):
        yy = Yl(10 ** e)
        pg.ln([(ax, yy), (W - 4.0, yy)], COL["faint"], 0.12)
        pg.lab(u"1" if e == 0 else (u"10" if e == 1 else u"10^{}".format(e)), ax - 1.6, yy + 0.95, colour=BK_INK2,
               align="R")
    pg.ln([(ax, yt2), (ax, yb2)], COL["ink2"], 0.25)
    lo, hi = COLIFORM[0][1], COLIFORM[0][2]
    pg.rc(ax + 3.0, Yl(hi), ax + 13.0, Yl(lo), fill=C["d2"])
    pg.lab(u"after a wetland: 10^{:.0f}-10^{:.0f} {{src:paraskevopoulos_2020}}".format(math.log10(lo), math.log10(hi)),
           ax + 16.0, (Yl(lo) + Yl(hi)) / 2.0 + 1.0, colour=C["d3"], bold=True)
    lim_b = COLIFORM[1][1]
    pg.ln([(ax, Yl(lim_b)), (W - 4.0, Yl(lim_b))], BK_ACC, 0.7)
    pg.lab(u"class B, orchards: below {:,.0f}".format(lim_b), ax + 16.0, Yl(lim_b) + 4.4, colour=BK_ACC, bold=True)
    pg.ln([(ax, yb2 - 0.5), (ax + 40.0, yb2 - 0.5)], BK_ACC, 1.0)
    pg.lab(u"class A, parks: 0 {src:reuse_classes_2010}", ax + 16.0, yb2 - 3.0, colour=BK_ACC, bold=True)
    res["cleaning"].update({"wetland_coliforms_per_100ml": [lo, hi], "class_b_limit": lim_b, "class_a_limit": 0})


# ---------------------------------------------------------------- C6: the S4 cut in each season
BK_SEASONS = [("c6_s1", "winter"), ("c6_s2", "spring"), ("c6_s3", "summer"), ("c6_s4", "autumn")]
BK_DROP_LAYERS = ("title", "levels", "callouts", "dimensions", "band", "survey", "text")


def bk_season(pg, res, key):
    E = detail_engine()
    W, H = pg.W, pg.H
    i = [s["key"] for s in E["SEASONS"]].index(key)
    sea = E["SEASONS"][i]
    prof = _DET_PROF[0] if _DET_PROF else (E["PROFILE_S0"], E["PROFILE_DS"], E["PROFILE_Z"])
    d = E["SECTIONS"][0]                                     # the south-west bank, the bed and the strip
    keep = (E["SCALE"], E["K"], dict(E["SEA"]))
    lay = {"poly": 6, "line": 5, "circle": 7}
    x0, y0, x1, y1 = 40.0, 2.0, W - 2.0, H - 2.0             # the cut's box (mm, y down); names at the left
    kk = 1.0                                                 # first pass at 1 mm per m, then as large as it fits
    try:
        E["SEA"].clear()
        E["SEA"].update(E["SEASON_LOOK"][key])
        for _ in range(2):
            E["K"] = kk
            E["SCALE"] = 1000.0 / kk
            tmp = E["Page"]("bk", key)
            E["draw_section"](tmp, E["Sec"](d, prof), 0.0, 0.0, [], sea)
            items = from_engine([it for it in tmp.items if it[0] in lay and it[lay[it[0]]] not in BK_DROP_LAYERS])
            bb = items_bbox(items)
            kk *= min((x1 - x0) / (bb[2] - bb[0]), (y1 - y0) / (bb[3] - bb[1])) * 0.995
    finally:
        E["SCALE"], E["K"] = keep[0], keep[1]
        E["SEA"].clear()
        E["SEA"].update(keep[2])
    s_ = min(1.0, (x1 - x0) / (bb[2] - bb[0]), (y1 - y0) / (bb[3] - bb[1]))
    dx = x0 - s_ * bb[0] + ((x1 - x0) - s_ * (bb[2] - bb[0])) / 2.0
    dy = (H - y1) - s_ * bb[1] + ((y1 - y0) - s_ * (bb[3] - bb[1])) / 2.0
    pg.items += xform(items, s_, dx, dy)
    pg.rc(0.0, 0.0, 34.0, 1.6, fill=BAND_BLUE[i])
    pg.lab(u"{} · {}".format(sea["name"], sea["months"].replace(u" ", u"")), 0.0, 8.5, size=BK_KEY, bold=True)
    pg.lab(u"S4 cut", 0.0, 13.5, colour=BK_INK2)
    res.setdefault("seasons", {})[key] = {"water_m_above_bed": [round(w[0] - E["THALWEG"][1], 2) for w in sea["water"]],
                                          "strip_held": sea["strip_held"]}


# ---------------------------------------------------------------- C8 a: where the clean water goes (pictograms)
def bk_farms(pg, res):
    W, H = pg.W, pg.H
    # row 1: the clean stream leaves the site for the farmland outside (the focal arrow)
    pg.pl([rect(4.0, 14.0, 66.0, 52.0)], stroke=BK_INK2, lw=0.3, dash=[1.4, 1.0])
    wave = [(6.0 + t * 0.5, 31.0 + 1.2 * math.sin(t * 0.5)) for t in range(0, 121)]
    pg.ln(wave, C["w3"], 1.6)
    pg.lab(u"no farm channel inside", 6.5, 48.5, colour=BK_INK2)
    arrow(pg, [(68.0, H - 31.0), (112.0, H - 31.0)], BK_ACC, 1.4, 5.0)
    pg.lab(u"clean stream leaves the site", 68.0, 26.0, colour=BK_ACC, bold=True)
    farm = draw_farm_picto("A")
    farm.items = [it for it in farm.items if it[0] not in ("text", "circle")]
    bb = items_bbox(farm.items)
    s_ = min((W - 118.0 - 3.0) / (bb[2] - bb[0]), 40.0 / (bb[3] - bb[1]))
    pg.items += xform(farm.items, s_, 118.0 - s_ * bb[0], (H - 52.0) - s_ * bb[1])
    pg.lab(u"farmland outside · route open", 118.0, 57.5, colour=MP["agriculture"][2], bold=True)
    # row 2: winter water into the alluvium, only if the boreholes allow it
    pg.ic("rain", 8.0, 66.0, 20.0)
    pg.rc(48.0, 82.0, 150.0, 104.0, fill=COL["soil"])
    r = _tree_rand(48.0, 82.0)
    for _ in range(140):
        pg.circle(48.5 + 101.0 * r(), H - (82.5 + 21.0 * r()), 0.25, fill=COL["soil_dk"])
    pg.ln([(48.0, 82.0), (150.0, 82.0)], COL["edge3d"], 0.3)
    arrow(pg, [(30.0, H - 76.0), (56.0, H - 76.0)], C["w3"], 0.8, 3.0)
    pg.ln([(56.0, 76.0), (126.0, 76.0)], C["w3"], 0.8, dash=[1.4, 0.9])
    for xx in (70.0, 98.0, 126.0):                          # dashed: only if the borehole tests accept it
        arrow(pg, [(xx, H - 76.0), (xx, H - 97.0)], C["w3"], 0.8, 3.0, dash=[1.4, 0.9])
    pg.lab(u"recharge, if tests accept", 153.0, 94.0, colour=C["d3"], bold=True)
    # row 3: the town's wastewater: treatment plant -> Bakırçay, not into the Selinos
    pg.ic("sewage", 8.0, 120.0, 20.0)
    arrow(pg, [(31.0, H - 130.0), (52.0, H - 130.0)], BK_INK2, 0.7, 2.6)
    pg.ic("plant", 55.0, 120.0, 20.0)
    arrow(pg, [(78.0, H - 130.0), (108.0, H - 130.0)], BK_INK2, 0.7, 2.6)
    pg.rc(110.0, 126.0, 190.0, 134.0, fill=C["w2"])
    pg.lab(u"treatment plant -> Bakırçay", 110.0, 140.5, colour=BK_INK)
    pg.ln([(65.0, 142.0), (65.0, 157.0)], BK_INK2, 0.5, dash=[1.2, 0.8])
    pg.pl([[(65.0, 158.5), (63.9, 156.0), (66.1, 156.0)]], fill=BK_INK2)
    pg.ln([(62.4, 147.2), (67.6, 152.4)], BK_ACC, 0.7)
    pg.ln([(62.4, 152.4), (67.6, 147.2)], BK_ACC, 0.7)
    pg.rc(30.0, 159.0, 100.0, 163.0, fill=C["w3"])
    pg.lab(u"not into the Selinos", 71.0, 151.0, colour=BK_ACC, bold=True)


# ---------------------------------------------------------------- the frames and their plan entries
BK_FRAMES = [
    ("b1_hero", bk_year, u"Oct -> Sep · mean year · natural flow, worst-case roughness", None,
     [("fill", C["w3"], u"Rain"), ("fill", C["structure"], u"Open-water evaporation"),
      ("fill", MP["discharge"][2], u"Stream flow, Dec-Apr"), ("fill", MP["discharge"][0], u"Stream flow, other months"),
      ("line", "3C5159", u"Mean depth in the bed")]),
    ("b1_side", bk_ndvi, u"Greener by the water every month {src:sentinel2} {src:clcplus}", None,
     [("line", "495338", u"Riparian strip"), ("line", COL["structure"], u"Rest of the site frame")]),
    ("b2_hero", bk_cuts, u"Depth above the bed · vertical x8 · looking upstream", 1500,
     [("fill", COL["structure"], u"Ground"), ("line", LEVEL_COL[1], u"Highest day 2016-2021"),
      ("line", LEVEL_COL[3], u"Q100"), ("line", LEVEL_COL[4], u"Q500"), ("fill", BK_ACC, u"Over the bank top")]),
    ("b4_side", bk_cubes, u"Cubes to scale 1:1,250 · edge = cube root of volume", 1250,
     [("fill", MP["storage"][1], u"Stored water, to scale")]),
    ("b5_strip", bk_chain, u"Our design: one way, with the stream", None,
     [("line", C["w3"], u"Water, one way")]),
    ("b5_hero", bk_cleaning, u"Reed beds clean, UV makes it safe to touch {src:vymazal_2010} {src:reuse_uv_2010}", None,
     []),                                                  # the three wetland types are labelled on the drawing
] + [(k_, (lambda s_: (lambda pg, res: bk_season(pg, res, s_)))(s_),
      u"{} on the downstream cut".format(s_.capitalize()), None, [("fill", BAND_BLUE[i_], s_)])
     for i_, (k_, s_) in enumerate(BK_SEASONS)] + [
    ("c8_a", bk_farms, u"Our design: farms outside, class B water", None,
     [("line", C["w3"], u"Clean stream water"), ("fill", MP["agriculture"][1], u"Farmland outside the site")])]


def booklet_export(folder, log):
    """Writes output/<folder>/booklet/: one text-free PDF per frame, blocks.json (labels, captions, legends) and
    results.json (the figures the drawings print). Problems go to the log; the sheets are already written."""
    bk = BkBlocks(folder, GH_LABEL, SHORT)
    res = {"script": GH_LABEL, "version": SHORT}
    for key, fn, cap, den, legend in BK_FRAMES:
        try:
            pg = BkPage(key)
            fn(pg, res)
            pg.finish()
            pg.items, labels = bk_take_text(pg.items, pg.H)
            for lb in labels:
                lb["size"] = round(lb["size"], 2)
            for p in bk_check(labels, pg.W, pg.H):
                log.append(u"booklet {}: {}".format(key, p))
            write_pdf(pg, bk.path(key + ".pdf"), u"Bergama water board {} booklet {}".format(SHORT, key))
            bk.drawing(key, key + ".pdf", labels, cap, den,
                       [{"kind": k_, "colour": c_, "label": l_} for k_, c_, l_ in legend])
        except Exception as ex:
            log.append(u"booklet {} not written: {}: {}".format(key, type(ex).__name__, ex))
    with open(bk.path("results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    bk.save()


# ---------------------------------------------------------------- run
def out_folder(doc):
    # v1 24 Oct: all files under Downloads/Bergama/ (Aras rule); was next to the .3dm / .gh, else Documents
    return os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "output", OUT_FOLDER)


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
    if folder and not err:                          # v1.9: the A3 booklet's drawings; never breaks the sheets
        try:
            booklet_export(folder, log)
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
SKETCH_SRC = r'''# The idea sketches of pr1_drawings v3.1 (concept sections, SKETCH style), run in their own namespace: pr1 baked them
# into Rhino; here the same calls make page items. The draw order is pr1's (bake order plus its lifts Z_*).
import math
ZP = []
ORDER = [0]
FORM = "A"
PEOPLE = True
NODE = None                                          # set by the board: the element numbers
CITE = None                                          # v3: set by the board: a source's number "[n]" (footer key)
ORIGIN = (0.0, 0.0)                                  # pr1 placed the sketches beside the site map; here at 0


def _hexc(c):
    return "%02X%02X%02X" % tuple(c)


def _put(item, z):
    ORDER[0] += 1
    ZP.append((ORDER[0] + z, ORDER[0], item))


def P(o, x, y):
    return (o[0] + x, o[1] + y)


def add_polyline(q):
    out = []
    for p in q:
        if not out or abs(p[0] - out[-1][0]) + abs(p[1] - out[-1][1]) > 1e-6:
            out.append((p[0], p[1]))
    return out if len(out) >= 2 else None


def keep(obj, sub, colour, width=None, dashed=False, alpha=None, z=0):
    if obj is None:
        return None
    _put(("line", obj, _hexc(colour), width if width else 0.13, [1.0, 0.7] if dashed else None, 1), z)
    return obj


def pline(o, pts, sub, colour, width=0.18, closed=False, dashed=False, z=0):
    q = [P(o, x, y) for x, y in pts]
    if closed and q[0] != q[-1]:
        q.append(q[0])
    return keep(add_polyline(q), sub, colour, width, dashed, z=z)


def fill(o, pts, sub, colour, alpha=None, boundary=True, z=0, hand_=None):
    if HAND[0] if hand_ is None else hand_:
        pts = hand_ring(pts, sub)
        boundary = False
    ring = [P(o, x, y) for x, y in pts]
    if len(ring) < 3:
        return None
    _put(("poly", [ring], _hexc(colour), None, 0.1, None, None, alpha), z)
    if boundary:
        pline(o, pts, sub, colour, 0.13, closed=True, z=z)
    return ring


def hatch_lines(o, pts, sub, colour, spacing=1.6, angle=45.0, width=None):
    width = LW_HATCH if width is None else width
    for p0, p1 in clip_segments(pts, spacing, angle):
        keep([P(o, *p0), P(o, *p1)], sub, colour, width)


def text(o, s, x, y, size_pt, colour=None, sub="text", just="left", bold=False, mask=None):
    colour = INK if colour is None else colour
    h = size_pt * 0.353
    for i, ln in enumerate(s.split("\n")):
        if ln.strip():
            q = P(o, x, y - i * h * 1.35)
            _put(("text", ln, q[0], q[1], h, _hexc(colour), bold, {"left": "L", "right": "R"}.get(just, "C"), None,
                  _hexc(mask) if mask else None), Z_TEXT)      # pr1's text mask: a halo in its colour


def _smooth(o, pts):
    """A Catmull-Rom curve through the points (pr1: Rhino's interpolated curve), as a fine polyline."""
    q = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(q) - 2):
        p0, p1, p2, p3 = q[i - 1], q[i], q[i + 1], q[i + 2]
        for k in range(8):
            t = k / 8.0
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
    out.append(pts[-1])
    return add_polyline([P(o, x, y) for x, y in out])


def title(o, h, s):
    text(o, s, 0, h + 4, 7.0, INK, "title", bold=True)

def hx(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

INK, INK2 = hx("4A3F35"), hx("847E75")
SOIL, STONE, ROAD = hx("CDBF9F"), hx("A4A1A3"), hx("3A3A3A")
W_SUM, W_WIN, W_EXT = hx("A9C3CC"), hx("7FA7B8"), hx("5C7A86")
REED, ACCENT, HERITAGE, WHITE = hx("89986A"), hx("BC6F45"), hx("8B2D2D"), (255, 255, 255)
CELL, FARM = hx("DFE6CF"), hx("E7E0C8")
def mix(a, b, t):
    """Plain RGB mix of two palette colours (t = share of b), for hatch and outline tones only."""
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))

SOIL_HATCH = mix(SOIL, INK, 0.30)      # earth hatch over the soil poché
STONE_HATCH = mix(STONE, INK, 0.35)    # masonry hatch, K4 bridge behind
REED_HEAD = mix(REED, INK, 0.35)       # reed plumes
FIGURE = INK2                          # scale figures
# line weights (print width, mm): what the section cuts is heaviest, what is seen beyond it is thin
LW_CUT, LW_PROFILE, LW_EDGE, LW_BEYOND, LW_FINE, LW_HATCH = 0.50, 0.35, 0.25, 0.13, 0.09, 0.05
Z_TREE, Z_LINE, Z_PEOPLE, Z_TEXT = 300000, 400000, 600000, 900000   # draw-order lifts: trees, lines, people, texts
def clip_segments(pts, spacing, angle):
    """The pieces of parallel lines (spacing, angle in degrees) that lie inside a closed outline."""
    segs = []
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)
    r = [(x * ca + y * sa, -x * sa + y * ca) for x, y in pts]       # outline turned so the hatch runs along x
    if r[0] != r[-1]:
        r.append(r[0])
    ys = [p[1] for p in r]
    k = int(math.floor(min(ys) / spacing)) + 1
    while k * spacing < max(ys):
        yy = k * spacing
        xs = sorted(x1 + (yy - y1) * (x2 - x1) / (y2 - y1) for (x1, y1), (x2, y2) in zip(r[:-1], r[1:])
                    if (y1 <= yy < y2) or (y2 <= yy < y1))
        for i in range(0, len(xs) - 1, 2):
            if xs[i + 1] - xs[i] > 0.05:
                p0 = (xs[i] * ca - yy * sa, xs[i] * sa + yy * ca)
                p1 = (xs[i + 1] * ca - yy * sa, xs[i + 1] * sa + yy * ca)
                segs.append((p0, p1))
        k += 1
    return segs

def notch(g, cuts):
    """Ground outline g with rectangular basins cut into its level stretches: cuts = [(x0, x1, y_top, depth)]."""
    out = list(g)
    for x0, x1, y, d in cuts:
        for i in range(len(out) - 1):
            (ax, ay), (bx, by) = out[i], out[i + 1]
            if abs(ay - y) < 1e-9 and abs(by - y) < 1e-9 and min(ax, bx) <= x0 and x1 <= max(ax, bx):
                ins = [(x0, y), (x0, y - d), (x1, y - d), (x1, y)]
                ins = ins if ax < bx else ins[::-1]
                ins = [p for p in ins if p != out[i] and p != out[i + 1]]
                out[i + 1:i + 1] = ins
                break
    return out

def surface_y(surface, x):
    """Height of the ground surface at x (on a vertical step: the lower of the two)."""
    ys = [ay + (by - ay) * (x - ax) / (bx - ax) for (ax, ay), (bx, by) in zip(surface[:-1], surface[1:])
          if bx != ax and min(ax, bx) <= x <= max(ax, bx)]
    return min(ys) if ys else None

def surface_between(surface, x0, x1, dy=0.0):
    """The surface from x0 to x1 (steps inside kept, risers at the two ends dropped), lifted by dy."""
    out = []
    for (ax, ay), (bx, by) in zip(surface[:-1], surface[1:]):
        if max(ax, bx) < x0 or min(ax, bx) > x1:
            continue
        if ax == bx:
            seg = [(ax, ay), (bx, by)]
        else:
            seg = []
            for x in (max(min(ax, bx), x0), min(max(ax, bx), x1)) if ax < bx else (min(max(ax, bx), x1), max(min(ax, bx), x0)):
                seg.append((x, ay + (by - ay) * (x - ax) / (bx - ax)))
        for q in seg:
            if not out or abs(q[0] - out[-1][0]) + abs(q[1] - out[-1][1]) > 1e-9:
                out.append(q)
    while len(out) > 2 and out[0][0] == out[1][0]:
        out.pop(0)
    while len(out) > 2 and out[-1][0] == out[-2][0]:
        out.pop()
    return [(x, y + dy) for x, y in out]

def reeds(o, x0, x1, y, h=3.5, plan=False):
    """Reed clumps at v2.8's spacing and height: a fan of thin arched blades of mixed height, a plume on every third
    clump. plan=True (form plans): a small tuft of radiating leaves seen from above."""
    rnd = _tree_rand(x0 + 0.37 * x1, y)
    n = max(3, int((x1 - x0) / 1.6))
    for i in range(n):
        x = x0 + (x1 - x0) * i / (n - 1)
        if plan:
            m = 6 + int(rnd() * 3)
            for j in range(m):
                t = 6.283 * (j + 0.4 * rnd()) / m
                L = h * 0.38 * (0.6 + 0.4 * rnd())
                keep([P(o, x, y), P(o, x + L * math.cos(t), y + L * math.sin(t))], "planting", REED, LW_FINE)
            continue
        nb = 5 + int(rnd() * 3)
        tall = None
        for j in range(nb):
            s = (j / (nb - 1.0) - 0.5) * 2.0 + (rnd() - 0.5) * 0.35       # -1 .. 1: leaning left .. right
            hh = h * (0.62 + 0.38 * rnd()) * (1.0 - 0.18 * abs(s))
            pts = [(x + 0.12 * s + s * hh * 0.42 * t * t, y + hh * (t - 0.10 * abs(s) * t * t)) for t in (0.0, 0.35, 0.7, 1.0)]
            keep(_smooth(o, pts), "planting", REED, LW_FINE)
            if tall is None or hh > tall[0]:
                tall = (hh, pts)
        if i % 3 == 1 and tall:                    # plume along the tallest blade's tip
            (ax, ay), (bx, by) = tall[1][-2], tall[1][-1]
            L = math.hypot(bx - ax, by - ay) or 1.0
            ux, uy = (bx - ax) / L, (by - ay) / L
            ln, wd = 0.30 * h, 0.05 * h
            cx, cy = bx + ux * ln * 0.5, by + uy * ln * 0.5
            fill(o, [(bx, by), (cx - uy * wd, cy + ux * wd), (bx + ux * ln, by + uy * ln), (cx + uy * wd, cy - ux * wd)],
                 "planting", REED_HEAD, boundary=False)

def bank(p, q, n=24):
    """Edge where the project meets the water: S-curve in form A, one straight facet in form B."""
    if FORM == "B":
        return [p, q]
    out = []
    for i in range(n):
        t = i / (n - 1.0)
        s = (1 - math.cos(t * math.pi)) / 2
        out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * s))
    return out

def road(o, x0, x1, y, label, ly=None, mask=None):
    fill(o, [(x0, y), (x1, y), (x1, y + 1.3), (x0, y + 1.3)], "road", ROAD)
    text(o, label, x0 + 1, ly if ly is not None else y - 2.5, 5.0, ROAD, "road", mask=mask)

def level_mark(o, x, y, colour, sub):
    """Level sign: a small open triangle standing point-down on the level line."""
    pline(o, [(x - 1.0, y + 1.7), (x + 1.0, y + 1.7), (x, y)], sub, colour, LW_BEYOND, closed=True, z=Z_LINE)

HAND_AMP = 0.18          # mm: sideways wobble of a hand line
HAND_WAV = 7.0           # mm: length of one wobble
HAND_OVER = 1.1          # mm: how far a stroke runs past its corner
HAND_FONT = ["Ink Free", "Segoe Print", "Comic Sans MS"]   # first one installed (Windows 10/11 ship Ink Free)
PEN_HAIR, PEN_FINE, PEN_MED, PEN_BOLD = 0.13, 0.20, 0.40, 0.70   # masterplan v9 pens (mm)
SKINK = hx("1E1E1E")                                 # fine-liner black: the line that carries the idea
SUN, SUN_RAY = hx("E8C64A"), hx("C9A227")           # the dry summer (Aras): marker yellow
HAND = [False]                                       # True while a part is drawn by hand (form plans: pline / fill wobble)
HAND_TEXT = [False]                                  # True while texts take the hand font and drop their masks
KHAKI, PAPER, BG_ = hx("BCB794"), hx("F1EDDF"), hx("E6E0C8")
SEC_POCHE = mix(KHAKI, PAPER, 0.62)                  # board: the cut ground
SEC_POCHE_BAND = mix(SEC_POCHE, KHAKI, 0.45)          # the band just under the surface, a little deeper
SEC_PAVE = mix(hx("BC6F45"), BG_, 0.12)              # board: walkable edge, terracotta
SEC_CHANNEL_HATCH = hx("3E7DAE")                     # board: the stream bed's blue hatch
SITE_WATER, SITE_WATER_D, SITE_FLOOD = hx("7FA4B3"), hx("5E8494"), hx("B4CBD2")   # board CAT water, BLUE_D, BLUE_L
FLOOD_WASH, FLOOD_ALPHA = hx("4F9BD9"), 0.09         # the design flood's reach up to Q500: one clear blue, see-through
                                                      # and so faint it takes a moment to see (Nil 17:59: "really really faint blue,
                                                      # almost indistinguishable ... should need a focus to see"); raise FLOOD_ALPHA = stronger
SITE_PEOPLE = mix(hx("7A6E60"), BG_, 0.1)            # board: SA_STYLE_BOARD people
SITE_TREE = (hx("B2C484"), hx("8CA466"), hx("688052"))   # board SA_TREE_PAL["tree"]: light, mid, shadow
SITE_TRUNK = hx("6E625A")                            # board SA_TRUNK
HOUSE_WALL, HOUSE_ROOF = hx("D9B98C"), hx("A86A55")  # board TYPO["traditional"] tone, TYPO_ROOF_C
SA_FIGS = [                                          # board SA_FIGS (m, 1.75 m tall), SA_HEAD
    [(-0.10, 0.0), (-0.06, 0.0), (-0.03, 0.82), (0.03, 0.82), (0.06, 0.0), (0.10, 0.0), (0.12, 0.85), (0.16, 1.38),
     (0.10, 1.47), (0.05, 1.50), (0.05, 1.53), (-0.05, 1.53), (-0.05, 1.50), (-0.10, 1.47), (-0.16, 1.38), (-0.12, 0.85)],
    [(-0.30, 0.0), (-0.24, 0.0), (-0.02, 0.78), (0.18, 0.0), (0.25, 0.0), (0.11, 0.86), (0.18, 1.12), (0.12, 1.40),
     (0.06, 1.48), (0.05, 1.53), (-0.05, 1.53), (-0.07, 1.47), (-0.14, 1.38), (-0.20, 1.10), (-0.12, 0.86)],
    [(-0.20, 0.0), (0.20, 0.0), (0.13, 0.62), (0.11, 1.08), (0.15, 1.36), (0.09, 1.45), (0.05, 1.49), (0.05, 1.52),
     (-0.05, 1.52), (-0.05, 1.49), (-0.09, 1.45), (-0.15, 1.36), (-0.11, 1.08), (-0.13, 0.62)],
    [(-0.11, 0.0), (-0.06, 0.0), (-0.02, 0.80), (0.04, 0.80), (0.08, 0.0), (0.13, 0.0), (0.12, 0.86), (0.30, 0.86),
     (0.30, 0.55), (0.40, 0.55), (0.40, 0.95), (0.17, 1.38), (0.10, 1.47), (0.05, 1.51), (0.05, 1.53), (-0.05, 1.53),
     (-0.05, 1.50), (-0.10, 1.47), (-0.16, 1.38), (-0.13, 0.86)],
]
SA_HEAD = (0.0, 1.64, 0.105)

import zlib as _zlib, random as _random
def _seed(*parts):
    return _zlib.crc32(repr([round(float(v), 2) if isinstance(v, float) else v for v in parts]).encode("utf-8")) & 0x7fffffff

def _densify(P, step):
    out = [P[0]]
    for a, b in zip(P[:-1], P[1:]):
        n = max(1, int(math.ceil(math.hypot(b[0] - a[0], b[1] - a[1]) / step)))
        out += [(a[0] + (b[0] - a[0]) * k / float(n), a[1] + (b[1] - a[1]) * k / float(n)) for k in range(1, n + 1)]
    return out

def _normals(a):
    out = []
    for i in range(len(a)):
        p, q = a[max(0, i - 1)], a[min(len(a) - 1, i + 1)]
        d = math.hypot(q[0] - p[0], q[1] - p[1]) or 1e-12
        out.append((-(q[1] - p[1]) / d, (q[0] - p[0]) / d))
    return out

def _noise(n, step, wav, rnd):
    """n values of smooth noise (std about 1), features about wav long (masterplan smooth_noise)."""
    k = max(2, int(math.ceil(n * step / wav)) + 3)
    ctrl = [rnd.gauss(0.0, 1.0) for _ in range(k)]
    out = []
    for j in range(n):
        x = j * step / wav
        i = min(int(x), k - 2)
        f = x - i
        f = f * f * (3 - 2 * f)
        out.append(ctrl[i] * (1 - f) + ctrl[i + 1] * f)
    return out

def hand(P, amp, wav, seed, closed=False, over=0.0):
    """A polyline as a hand draws it (masterplan hand_line): smooth sideways wobble of about amp (at most 2.2 amp),
    an overshoot of `over` at both ends of an open line; a closed ring starts at a random point."""
    a = [(float(p[0]), float(p[1])) for p in P]
    if len(a) < 2:
        return a
    rnd = _random.Random(seed)
    step = max(wav / 6.0, 1e-6)
    if closed:
        if math.hypot(a[0][0] - a[-1][0], a[0][1] - a[-1][1]) < 1e-9:
            a = a[:-1]
        k = rnd.randrange(len(a))
        a = a[k:] + a[:k] + [a[k]]
    a = _densify(a, step)
    if over > 0 and not closed:
        (x0, y0), (x1, y1) = a[0], a[1]
        d = math.hypot(x1 - x0, y1 - y0) or 1e-12
        s = (x0 - (x1 - x0) / d * over, y0 - (y1 - y0) / d * over)
        (x0, y0), (x1, y1) = a[-1], a[-2]
        d = math.hypot(x1 - x0, y1 - y0) or 1e-12
        a = [s] + a + [(x0 - (x1 - x0) / d * over, y0 - (y1 - y0) / d * over)]
    if amp > 0:
        w = [max(-2.2, min(2.2, v)) * amp for v in _noise(len(a), step, wav, rnd)]
        a = [(p[0] + n[0] * v, p[1] + n[1] * v) for p, n, v in zip(a, _normals(a), w)]
    return a

def _strokes(P, closed, turn=28.0):
    """A polyline split at its corners, as a hand draws it: one stroke per straight run."""
    P = list(P) + ([P[0]] if closed and P[0] != P[-1] else [])
    out = [[P[0]]]
    for i in range(1, len(P) - 1):
        a, b, c = P[i - 1], P[i], P[i + 1]
        t1, t2 = math.atan2(b[1] - a[1], b[0] - a[0]), math.atan2(c[1] - b[1], c[0] - b[0])
        out[-1].append(b)
        if abs((math.degrees(t2 - t1) + 180) % 360 - 180) > turn:
            out.append([b])
    out[-1].append(P[-1])
    return [s for s in out if len(s) > 1]

def _crosses(ring):
    """True when a closed ring crosses itself (a hatch from it would fail or fill wrongly)."""
    q = list(ring) + ([ring[0]] if ring[0] != ring[-1] else [])
    E = list(zip(q[:-1], q[1:]))
    box = [(min(a[0], b[0]), max(a[0], b[0]), min(a[1], b[1]), max(a[1], b[1])) for a, b in E]

    def o_(p, r, t):
        return (r[0] - p[0]) * (t[1] - p[1]) - (r[1] - p[1]) * (t[0] - p[0])
    m = len(E)
    for i in range(m):
        a, b = E[i]
        bi = box[i]
        for j in range(i + 2, m):
            if i == 0 and j == m - 1:
                continue
            bj = box[j]
            if bi[1] < bj[0] or bj[1] < bi[0] or bi[3] < bj[2] or bj[3] < bi[2]:
                continue
            c, d = E[j]
            if o_(a, b, c) * o_(a, b, d) < -1e-12 and o_(c, d, a) * o_(c, d, b) < -1e-12:
                return True
    return False

def hand_ring(pts, sub, amp=HAND_AMP, wav=HAND_WAV):
    """A closed outline drawn by hand; where the wobble would make it cross itself (narrow or sharp shapes), a smaller
    wobble, else the true outline."""
    sd = _seed(pts[0][0], pts[0][1], len(pts), sub)
    for k in (1.0, 0.5, 0.25):
        r = hand(pts, amp * k, wav, sd, closed=True)
        if not _crosses(r):
            return r
    return list(pts)

def sketch(o, pts, sub, colour, width=0.25, closed=False, over=HAND_OVER, amp=HAND_AMP, retrace=True, z=0,
           dashed=False):
    """Fine-liner line: each straight run its own stroke, wobbling and running past the corners; long runs are
    traced a second time, lighter and not quite end to end, as a sketch is."""
    for k, s in enumerate(_strokes(pts, closed)):
        sd = _seed(s[0][0], s[0][1], s[-1][0], s[-1][1], k, sub)
        q = hand(s, amp, HAND_WAV, sd, over=over)
        keep(add_polyline([P(o, *p) for p in q]), sub, colour, width, dashed, z=z)
        L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(s[:-1], s[1:]))
        if retrace and not dashed and L > 6.0:
            rnd = _random.Random(sd + 7)
            q = hand(s, amp * 1.6, HAND_WAV * 0.8, sd + 11, over=over * 0.5)
            i0, i1 = int(len(q) * 0.15 * rnd.random()), len(q) - int(len(q) * 0.25 * rnd.random())
            if i1 - i0 > 1:
                keep(add_polyline([P(o, *p) for p in q[i0:i1]]), sub, colour, width * 0.45, z=z)

def wash(o, poly, sub, colour, alpha=0.5, z=0):
    """Watercolour wash: a see-through fill whose edge wobbles a little past the true outline."""
    ring = hand_ring(poly, sub, HAND_AMP * 1.8, HAND_WAV * 1.6)
    return fill(o, ring, sub, colour, alpha=alpha, boundary=False, z=z, hand_=False)

def marker(o, poly, sub, colour, angle=55.0, spacing=0.75, thick=0.62, alpha=0.55, base=0.22, z=0):
    """Marker fill: parallel strokes laid side by side at a slant, each a little longer or shorter than the shape
    (and slightly turned), over a faint wash of the same colour: the key element of a sketch (example 4)."""
    if base:
        wash(o, poly, sub, colour, base, z)
    rnd = _random.Random(_seed(poly[0][0], poly[0][1], angle, sub))
    for p0, p1 in clip_segments(poly, spacing, angle):
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L = math.hypot(dx, dy)
        if L < 0.2:
            continue
        ux, uy = dx / L, dy / L
        a0, a1 = (rnd.random() - 0.35) * 0.9, (rnd.random() - 0.35) * 0.9
        tw = (rnd.random() - 0.5) * 0.35
        s = (p0[0] - ux * a0, p0[1] - uy * a0)
        e = (p1[0] + ux * a1 - uy * tw, p1[1] + uy * a1 + ux * tw)
        nx, ny = -uy * thick / 2, ux * thick / 2
        fill(o, [(s[0] + nx, s[1] + ny), (e[0] + nx, e[1] + ny), (e[0] - nx, e[1] - ny), (s[0] - nx, s[1] - ny)],
             sub, colour, alpha=alpha, boundary=False, z=z, hand_=False)

def band(surface, x0, x1, depth):
    """Polygons of a band `depth` under the ground surface from x0 to x1 (split at vertical steps)."""
    seg = surface_between(surface, x0, x1)
    pieces, cur = [], [seg[0]] if seg else []
    for q in seg[1:]:
        if abs(q[0] - cur[-1][0]) < 1e-9:
            pieces.append(cur)
            cur = [q]
        else:
            cur.append(q)
    if cur:
        pieces.append(cur)
    return [pc + [(x, y - depth) for x, y in pc[::-1]] for pc in pieces if len(pc) > 1]

def under_level(surface, x0, x1, level):
    """The space between the ground and a level, x0..x1 (what that level puts under water)."""
    bed = [(x, min(level, y)) for x, y in surface_between(surface, x0, x1)]
    return [(x0, level), (x1, level)] + bed[::-1] if len(bed) > 1 else None

def hand_arrow(o, a, b, colour, sub="arrows", width=0.55, head=2.2, z=Z_LINE, bend=0.0):
    """Link arrow in the masterplan v9 manner (head barbs at 38 deg), drawn as filled marker shapes so it reads at
    every zoom and in the viewport, where print widths do not show (Nil 18 Oct 17:55: "the outflow drainage is gone"):
    a hand-wobbled shaft `width` wide that tapers a little towards the tip (bend > 0 bows it), and a solid head."""
    pts = [a, b]
    if bend:
        m = ((a[0] + b[0]) / 2.0 - (b[1] - a[1]) * bend, (a[1] + b[1]) / 2.0 + (b[0] - a[0]) * bend)
        pts = [(a[0] * (1 - t) ** 2 + 2 * m[0] * t * (1 - t) + b[0] * t * t, a[1] * (1 - t) ** 2 + 2 * m[1] * t * (1 - t) + b[1] * t * t)
               for t in [i / 24.0 for i in range(25)]]
    t = math.atan2(b[1] - pts[-2][1], b[0] - pts[-2][0])
    hl = head * math.cos(math.radians(38))                 # the head's length along the shaft
    L = sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(pts[:-1], pts[1:]))
    shaft, acc = [pts[0]], 0.0
    for p, q in zip(pts[:-1], pts[1:]):
        d = math.hypot(q[0] - p[0], q[1] - p[1])
        if acc + d >= L - hl * 0.7:
            f = (L - hl * 0.7 - acc) / (d or 1e-12)
            shaft.append((p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f))
            break
        shaft.append(q)
        acc += d
    sh = hand(shaft, HAND_AMP * 0.5, HAND_WAV, _seed(a[0], a[1], b[0], b[1], sub))
    nm = _normals(sh)
    n = len(sh)
    w_ = [width * (1.0 - 0.3 * i / max(1, n - 1)) / 2.0 for i in range(n)]
    left = [(p[0] + v[0] * w, p[1] + v[1] * w) for p, v, w in zip(sh, nm, w_)]
    right = [(p[0] - v[0] * w, p[1] - v[1] * w) for p, v, w in zip(sh, nm, w_)]
    fill(o, left + right[::-1], sub, colour, boundary=False, z=z, hand_=False)
    tip = (b[0] + math.cos(t) * 0.2, b[1] + math.sin(t) * 0.2)
    wings = [(b[0] - head * math.cos(t + sg * math.radians(38)), b[1] - head * math.sin(t + sg * math.radians(38))) for sg in (1, -1)]
    notch_ = (b[0] - hl * 0.7 * math.cos(t), b[1] - hl * 0.7 * math.sin(t))
    fill(o, [tip, wings[0], notch_, wings[1]], sub, colour, boundary=False, z=z, hand_=False)

def sun(o, x, y, r=2.2):
    """The dry summer: a marker-yellow sun with short hand rays (as in Nil's SNFCC sketch)."""
    disc_ = [(x + r * math.cos(6.283 * i / 20), y + r * math.sin(6.283 * i / 20)) for i in range(20)]
    wash(o, disc_, "sun", SUN, 0.85, z=Z_LINE)
    sketch(o, disc_, "sun", SKINK, PEN_FINE, closed=True, over=0.0, amp=0.08, retrace=False, z=Z_LINE)
    for k in range(9):
        t = 6.283 * (k + 0.3) / 9
        sketch(o, [(x + 1.45 * r * math.cos(t), y + 1.45 * r * math.sin(t)), (x + 2.1 * r * math.cos(t), y + 2.1 * r * math.sin(t))],
               "sun", SKINK, PEN_FINE, over=0.0, amp=0.03, retrace=False, z=Z_LINE)

def cloud_rain(o, x, y, r=1.0):
    """v3: the wet winter, a hand cloud with three rain strokes, centred at (x, y)."""
    pts = []
    for i in range(28):
        a = 6.283 * i / 28
        k = 1.0 + 0.24 * max(0.0, math.sin(a)) * abs(math.sin(3 * a))
        pts.append((x + 1.6 * r * math.cos(a) * k, max(y - 0.5 * r, y + 0.85 * r * math.sin(a) * k)))
    wash(o, pts, "season", SITE_FLOOD, 0.85, z=Z_LINE)
    sketch(o, pts, "season", SKINK, PEN_FINE, closed=True, over=0.0, amp=0.05, retrace=False, z=Z_LINE)
    for dx in (-0.8, 0.0, 0.8):
        sketch(o, [(x + dx * r, y - 0.8 * r), (x + dx * r - 0.35 * r, y - 1.8 * r)], "season", SITE_WATER_D, PEN_FINE,
               over=0.0, amp=0.02, retrace=False, z=Z_LINE)

def failsafe_mark(o, x, y, r=1.4):
    """v3: the fail-safe mark, an accent ring with a step and the water spilling over it."""
    ring = [(x + r * math.cos(6.283 * i / 20), y + r * math.sin(6.283 * i / 20)) for i in range(20)]
    sketch(o, ring, "fail-safe", ACCENT, PEN_FINE, closed=True, over=0.0, amp=0.05, retrace=False, z=Z_LINE)
    sketch(o, [(x - 0.75 * r, y + 0.3 * r), (x - 0.1 * r, y + 0.3 * r), (x - 0.1 * r, y - 0.45 * r), (x + 0.75 * r, y - 0.45 * r)],
           "fail-safe", SKINK, PEN_FINE, over=0.0, amp=0.03, retrace=False, z=Z_LINE)
    hand_arrow(o, (x - 0.55 * r, y + 0.55 * r), (x + 0.25 * r, y - 0.15 * r), ACCENT, width=0.16, head=0.55, bend=-0.3)

def keyed(o, kind, s, x, y, size_pt, colour=None, sub="text", mask=None):
    """v3: a keyword callout led by a hand pictogram at its first line: "winter" (cloud and rain), "summer" (the
    sun) or "failsafe". The text starts a little to the right of x."""
    h = size_pt * 0.353
    cx, cy = x + 1.1 * h, y + 0.36 * h
    if kind == "winter":
        cloud_rain(o, cx, cy + 0.15 * h, 0.5 * h)
    elif kind == "summer":
        sun(o, cx, cy, 0.36 * h)
    elif kind == "failsafe":
        failsafe_mark(o, cx, cy, 0.62 * h)
    text(o, s, x + 2.4 * h, y, size_pt, colour, sub, mask=mask)

def tick_dim(o, x, y0, y1, colour=INK2):
    """Sketch dimension: a vertical line with slashed ticks at both ends (example 4); no figure."""
    sketch(o, [(x, y0), (x, y1)], "dimensions", colour, LW_BEYOND, over=0.9, retrace=False, z=Z_LINE)
    for y in (y0, y1):
        sketch(o, [(x - 0.9, y - 0.9), (x + 0.9, y + 0.9)], "dimensions", colour, LW_EDGE, over=0.0, retrace=False, z=Z_LINE)

def sketch_ground(o, g, sub="ground"):
    """Ground: the board's poché, solid (a see-through ground shows the viewport through it and the band under the
    surface then reads as a gap, Nil 18 Oct 17:46), a slightly deeper band under the surface, and short earth strokes
    just under the line (the surface line itself: drawn by the caller)."""
    surf = g[1:-1]
    wash(o, g, sub, SEC_POCHE, None)
    floor = min(p[1] for p in g)
    for pc in band(surf, surf[0][0], surf[-1][0], 3.0):
        pc = [(x, max(floor, y)) for x, y in pc]           # never below the drawn ground (low-flow channel)
        if not _crosses(pc):
            wash(o, pc, sub, SEC_POCHE_BAND, None)
    rnd = _random.Random(_seed(surf[0][0], surf[-1][0], len(surf)))
    for (ax, ay), (bx, by) in zip(surf[:-1], surf[1:]):
        L = math.hypot(bx - ax, by - ay)
        if L < 3.0 or abs(bx - ax) < 0.5 * L:
            continue
        n = int(L / 3.2)
        for k in range(n):
            t = (k + 0.3 + 0.4 * rnd.random()) / n
            x, y = ax + (bx - ax) * t, ay + (by - ay) * t - 0.7
            sketch(o, [(x, y), (x - 1.1, y - 1.1)], sub + " hatch", INK2, LW_HATCH * 2, over=0.0, amp=0.05, retrace=False)
    return surf

def sketch_tree(o, x, y, h):
    """Loose tree: a crown of washes in the board's tree greens, a scribbled outline and a trunk with two limbs."""
    rnd = _random.Random(_seed(x, y, h))
    cx, cy, rx, ry = x, y + 0.64 * h, 0.36 * h, 0.30 * h
    ph = [rnd.uniform(0, 6.3) for _ in range(3)]
    crown = []
    for q in range(36):                                  # board _sa_lumpy
        a = 6.283 * q / 36
        k = 1.0 + 0.12 * (math.sin(5 * a + ph[0]) + 0.6 * math.sin(8 * a + ph[1]) + 0.4 * math.sin(13 * a + ph[2])) / 2.0
        crown.append((cx + math.cos(a) * rx * k, cy + math.sin(a) * ry * k))
    for (sx, sy, col, al) in ((0.0, 0.0, SITE_TREE[1], 0.55), (-0.18, 0.2, SITE_TREE[0], 0.5), (0.2, -0.22, SITE_TREE[2], 0.35)):
        part = [(cx + (px - cx) * 0.62 + sx * rx, cy + (py - cy) * 0.62 + sy * ry) for px, py in crown]
        wash(o, part if al < 0.55 else crown, "planting", col, al, z=Z_TREE)
    sketch(o, crown, "planting", SITE_TREE[2], LW_FINE, closed=True, over=0.0, amp=0.25, retrace=False, z=Z_TREE)
    sketch(o, [(x, y), (x + 0.15, cy - 0.1 * h)], "planting", SITE_TRUNK, LW_EDGE, over=0.0, retrace=False, z=Z_TREE)
    for s in (-1, 1):
        sketch(o, [(x + 0.1, cy - 0.25 * h), (x + s * 0.22 * h, cy + 0.05 * h)], "planting", SITE_TRUNK, LW_FINE,
               over=0.0, retrace=False, z=Z_TREE)

def sketch_person(o, x, y, h=4.5, kind=0, flip=False):
    """Board scale figure (SA_FIGS) at the drawing's figure height h."""
    s = h / 1.745
    sg = -1.0 if flip else 1.0
    if not PEOPLE:
        return
    fill(o, [(x + sg * bx * s, y + by * s) for bx, by in SA_FIGS[kind % len(SA_FIGS)]], "people", SITE_PEOPLE,
         alpha=0.9, boundary=False, z=Z_PEOPLE, hand_=False)
    hx_, hy_, hr = SA_HEAD
    fill(o, [(x + sg * hx_ * s + hr * s * math.cos(6.283 * i / 12), y + hy_ * s + hr * s * math.sin(6.283 * i / 12))
             for i in range(12)], "people", SITE_PEOPLE, alpha=0.9, boundary=False, z=Z_PEOPLE, hand_=False)

def sketch_house(o, x0, x1, y, wall=6.0, pipe=False):
    """Context: an old town house beyond the street (board TYPO "traditional": stone base, hipped tile roof, deep
    eaves), generic, not surveyed. pipe=True adds the downpipe that takes its roof water to the street."""
    ev, rise = 0.9, 2.6
    body = [(x0, y), (x1, y), (x1, y + wall), (x0, y + wall)]
    roof = [(x0 - ev, y + wall), (x1 + ev, y + wall), (x1 - 2.2, y + wall + rise), (x0 + 2.2, y + wall + rise)]
    wash(o, body, "context", HOUSE_WALL, 0.45)
    marker(o, roof, "context", HOUSE_ROOF, angle=-35.0, spacing=0.6, thick=0.5, alpha=0.45, base=0.25)
    sketch(o, body, "context", INK2, LW_FINE, closed=True)
    sketch(o, roof, "context", INK2, LW_FINE, closed=True)
    sketch(o, [(x0, y + 1.0), (x1, y + 1.0)], "context", INK2, LW_HATCH * 2, over=0.4, retrace=False)
    for wx in (x0 + 0.28 * (x1 - x0), x0 + 0.62 * (x1 - x0)):
        sketch(o, [(wx, y + 2.2), (wx + 1.3, y + 2.2), (wx + 1.3, y + 4.6), (wx, y + 4.6)], "context", INK2, LW_HATCH * 2,
               closed=True, over=0.3, retrace=False)
    if pipe:
        sketch(o, [(x1 + 0.6, y + wall), (x1 + 0.6, y + 0.3)], "context", SITE_WATER_D, LW_EDGE, over=0.0, retrace=False)

def rain(o, x0, x1, y0, y1, n=14):
    rnd = _random.Random(_seed(x0, x1, y0, y1))
    for _ in range(n):
        x, y = x0 + rnd.random() * (x1 - x0), y0 + rnd.random() * (y1 - y0)
        sketch(o, [(x, y), (x - 0.5, y - 1.6)], "rain", SITE_WATER_D, LW_FINE, over=0.0, amp=0.04, retrace=False)

def water_body(surface, xs, level):
    """The water standing at `level` around x = xs: from where the ground on the left rises through the level to
    where it does on the right (banks, walls, the low-flow channel), following the bed in between. So the water always
    meets its banks (Nil 18 Oct 17:55: the water did not meet the left bank)."""
    k = None
    for i, ((ax, ay), (bx, by)) in enumerate(zip(surface[:-1], surface[1:])):
        if ax != bx and min(ax, bx) <= xs <= max(ax, bx):
            y = ay + (by - ay) * (xs - ax) / (bx - ax)
            if y < level and (k is None or y < k[1]):
                k = (i, y)
    if k is None:
        return None

    def cross(p, q):                                  # p under the level, q at or over it
        if abs(q[1] - p[1]) < 1e-12:
            return (q[0], level)
        t = (level - p[1]) / (q[1] - p[1])
        return (p[0] + (q[0] - p[0]) * t, level)
    i = k[0]
    left, right = [], []
    j = i
    while j >= 0 and surface[j][1] < level:
        left.append(surface[j])
        j -= 1
    left.append(cross(left[-1] if left else (xs, k[1]), surface[j]) if j >= 0 else (surface[0][0], level))
    j = i + 1
    while j < len(surface) and surface[j][1] < level:
        right.append(surface[j])
        j += 1
    right.append(cross(right[-1] if right else (xs, k[1]), surface[j]) if j < len(surface) else (surface[-1][0], level))
    bed = left[::-1] + right
    out = []
    for p in bed:
        if not out or abs(p[0] - out[-1][0]) + abs(p[1] - out[-1][1]) > 1e-9:
            out.append(p)
    return out                                        # first and last point on the level, the bed between

def water_level(o, surface, xs, level, colour, bed_hatch=False, line=True):
    """Water at `level` around xs, cut exactly to the ground (solid), a hand surface line; bed_hatch: the board's blue
    hatch over the stream bed."""
    pts = water_body(surface, xs, level)
    if not pts or len(pts) < 3:
        return None
    fill(o, pts, "water", colour, boundary=False, hand_=False)
    if bed_hatch:
        hatch_lines(o, pts, "water", SEC_CHANNEL_HATCH, 1.1, 45.0, PEN_HAIR)
    if line:
        sketch(o, [pts[0], pts[-1]], "water lines", SITE_WATER_D, PEN_FINE, over=0.0, retrace=False, z=Z_LINE)
    return pts

def concept_aras_sketch():
    HAND_TEXT[0] = True
    try:
        _concept_aras_sketch()
    finally:
        HAND_TEXT[0] = False

def _concept_aras_sketch():
    """PROBLEM: the bed is dry in summer, the winter runoff leaves the streets. MOVE: the bank becomes a cascade that
    holds the winter water, cleans it in reed basins and gives it back to the summer river."""
    o, w = ORIGIN, 200
    title(o, 82, "UPSTREAM ENTRY · collect, clean and hold · form " + FORM)
    g = [(0, 8), (0, 64), (34, 64), (34, 52), (68, 52), (68, 40), (102, 40), (102, 28), (130, 28)] + bank((130, 28), (140, 12))[1:] + \
        [(170, 12), (170, 28), (w, 28), (w, 8)]
    basins = ((40, 52), (74, 40), (108, 28))
    # the summer strip runs in a low-flow channel cut into the bed (v2.8: 150-160, 2.2 deep)
    gs = sketch_ground(o, notch(g, [(x0, x0 + 22, y, 5) for x0, y in basins] + [(150, 160, 12, 2.2)]))
    # winter: rain on the old town's roofs and street (context house generic, not surveyed)
    rain(o, 6, 33, 67.5, 73.5, 16)
    sketch_house(o, 15, 27, 65.3, wall=5.0, pipe=True)
    road(o, 0, 30, 64, "ROAD " + CITE("survey") + "\nschematic", ly=61.5, mask=SOIL)
    # Q500's reach first (solid wash), so the basins' water and reeds stay on top of it
    for pc in [under_level(gs, 102, w, 31.5)]:
        if pc:
            wash(o, pc, "flood", FLOOD_WASH, FLOOD_ALPHA)
    # the move: the cascade of reed basins (marker band = what holds and cleans the water)
    for x0, y in basins:
        water_level(o, gs, x0 + 11, y - 0.4, W_WIN)
        reeds(o, x0 + 1, x0 + 21, y - 5, 3.2)
    for pc in band(gs, 34, 130, 1.6):
        marker(o, pc, "terraces", SUN, angle=60.0, spacing=0.7, thick=0.6, alpha=0.5, base=0.0)
    sketch_tree(o, 65, 52, 9); sketch_tree(o, 99, 40, 7)    # on the strips between the basins, above Q500's reach
    # summer: the river (dry bed today) gets the clean water back
    water_level(o, gs, 155, 19, W_WIN, bed_hatch=True)
    water_level(o, gs, 155, 12, W_EXT, line=False)
    sun(o, 188, 58)
    sketch_person(o, 13, 65.3, kind=1); sketch_person(o, 70.8, 40)               # never inside water or the Q500 reach
    sketch(o, gs, "ground lines", SKINK, PEN_BOLD, z=Z_LINE)                      # the cut: the gesture
    keyed(o, "winter", "winter flow", 172, 24, 5.6, W_EXT, "water")
    keyed(o, "summer", "low-flow strip\nregulated release\ntoday: dry bed", 172, 19, 5.6, W_EXT, "water")
    sketch(o, [(102, 31.5), (w, 31.5)], "flood lines", HERITAGE, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_LINE)
    level_mark(o, 123.8, 31.5, HERITAGE, "flood lines")
    # v3 fix (audit problem 3): the surveyed ARAS cut keeps Q500 inside the banks (rain_river_levels README v1.1
    # line 21); the lowest terrace floods only if it is set below that level
    text(o, "Q500 +73.66 m · 3.30 m · inside the banks " + CITE("levels") + "\nlowest terrace floods only if set below it",
         126, 35.6, 5.0, HERITAGE, "flood")
    hand_arrow(o, (8, 72), (44, 56), SITE_WATER_D, bend=0.12)
    keyed(o, "winter", "street + roof runoff · Nov-Feb 59.1 % of rain " + CITE("rain") + "\nreed basins clean it with river water",
          6, 77.4, 5.8)
    hand_arrow(o, (126, 31), (150, 20), SITE_WATER_D, bend=-0.15)
    keyed(o, "summer", "regulated release · continuous strip\nJun-Sep 7.4 % of rain " + CITE("rain") + "\nriver below runs clean",
          109, 47, 5.8)
    for a, b in (((64, 49), (66, 44)), ((98, 37), (100, 32)), ((130, 26), (141, 18))):
        hand_arrow(o, a, b, ACCENT, width=0.4, head=1.5, bend=-0.2)
    keyed(o, "failsafe", "FAIL-SAFE\nfull basin: spills to the next\nlast basin: into the channel\nflood flow bypasses the reeds\ngravity · no pumps",
          2, 31, 5.8, ACCENT, mask=SOIL)
    text(o, "hold in winter,\ngive back in summer", 46, 21, 8.0, SKINK, "idea")
    for n_, x_, y_ in ((2, 51, 56), (3, 65, 56), (4, 85, 44), (5, 143, 22), (6, 155, 24)):
        NODE(o, x_, y_, n_)

def concept_begum_sketch():
    HAND_TEXT[0] = True
    try:
        _concept_begum_sketch()
    finally:
        HAND_TEXT[0] = False

def _concept_begum_sketch():
    """PROBLEM: the design flood runs over today's bank top. MOVE: the street level D is raised above it and the steps
    under it let the river climb: W wet every winter, F only in big floods, D never. K4 stays as it is."""
    o, w = (ORIGIN[0], ORIGIN[1] - 110), 200
    title(o, 82, "K4 BRIDGE · amphibious heritage threshold · form " + FORM)
    cx, cy = 120.0, 11.9                                           # the v2.8 arc through (98,14) (120,34) (142,14)
    r = math.hypot(98 - cx, 14 - cy)
    t0, t1 = math.atan2(14 - cy, 142 - cx), math.atan2(14 - cy, 98 - cx)
    arc = [(cx + r * math.cos(t0 + (t1 - t0) * i / 30.0), cy + r * math.sin(t0 + (t1 - t0) * i / 30.0)) for i in range(31)]
    sketch(o, arc, "K4 bridge (existing)", STONE_HATCH, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_TREE)  # behind
    text(o, "K4 Roman bridge behind\nexisting · kept untouched", 104, 45, 5.4, INK2)
    g = [(0, 8), (0, 62), (40, 62), (40, 50), (62, 50), (62, 40), (84, 40), (84, 30), (90, 30)] + bank((90, 30), (100, 14))[1:] + \
        [(150, 14), (150, 62), (w, 62), (w, 8)]
    gs = sketch_ground(o, notch(g, [(118, 132, 14, 2.5)]))     # summer strip: low-flow channel (v2.8: 118-132, 2.5)
    wall = [(150, 14), (154, 14), (154, 62), (150, 62)]
    marker(o, wall, "wall", STONE, angle=45.0, spacing=0.55, thick=0.5, alpha=0.55, base=0.35)
    text(o, "east: existing channel wall kept\ndefault · Q1 " + CITE("concept"), 156, 65, 5.4)
    # the river climbing the steps: every winter (W), the design flood (F), never D
    fl = under_level(gs, 40, 150, 52)
    if fl:
        wash(o, fl, "flood", FLOOD_WASH, FLOOD_ALPHA)
    water_level(o, gs, 125, 33, W_WIN, bed_hatch=True)
    water_level(o, gs, 125, 14, W_EXT, line=False)
    keyed(o, "winter", "every winter: bed under water", 156, 31.8, 5.6, W_EXT, "water")
    keyed(o, "summer", "continuous strip · regulated\ntoday: dry, pools", 156, 15.3, 5.6, W_EXT, "water")
    for x0, x1, y, lab in ((0, 40, 62, "dry top · in use all year"), (40, 84, 50, "flood terraces · out of\nservice only in big floods"),
                           (84, 100, 30, "bed + lowest\nstep · wet\nin winter")):
        for pc in band(gs, x0, x1, 1.5):
            marker(o, pc, "tiers", SUN, angle=60.0, spacing=0.7, thick=0.6, alpha=0.5, base=0.0)
        text(o, lab, x0 + 1, y - 3.0, 5.8, mask=SOIL)
    reeds(o, 102, 148, 14, 4.5)
    road(o, 0, 16, 62, "ROAD " + CITE("survey") + "\nK4 deck: traffic\nschematic", ly=54.5, mask=SOIL)
    sketch_tree(o, 24, 62, 9)                               # only on D: F floods in big floods, W every winter
    sketch_person(o, 31, 62, kind=1); sketch_person(o, 35, 62, kind=2, flip=True); sketch_person(o, 195, 62)  # on dry D / east
    sketch(o, gs, "ground lines", SKINK, PEN_BOLD, z=Z_LINE)                      # the cut: the gesture
    sketch(o, wall, "wall lines", SKINK, PEN_BOLD, closed=True, z=Z_LINE)
    sketch(o, [(40, 52), (150, 52)], "flood lines", W_EXT, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_LINE)
    tick_dim(o, 43, 52, 62, SKINK)                                                # D: raised clear of the flood
    hand_arrow(o, (138, 34.5), (138, 50.5), SITE_WATER_D, width=0.45, head=1.8)  # the river climbs in big floods
    level_mark(o, 146, 52, W_EXT, "flood lines")
    text(o, "Q500 over today's bank top\nK4 cut " + CITE("levels") + "\ndry top raised above it", 156, 51, 5.6, W_EXT, "water")
    text(o, "the river may climb the steps,\nthe street stays above Q500", 6, 31, 8.0, SKINK, "idea")
    text(o, "tiers " + CITE("tiers") + ": level 1 floods yearly · 2 only in 10-year storms\n"
         "level 3 street: dry, only if set above Q500", 2, 5.5, 5.2, INK2)
    for n_, x_, y_ in ((6, 125, 18), (7, 110, 22), (8, 73, 44), (9, 6, 67)):
        NODE(o, x_, y_, n_)

'''

# DETAIL_SRC: bergama_detail_section v2's drawing code (its PDF writer and Grasshopper part left out; weir wording
# replaced by the continuous strip, CONFLICTS.md rows 1-2; no working-area bar). Run by detail_engine().
DETAIL_SRC = r'''import math
import os
import random
import tempfile
import time
import json
import zlib

VERSION = "bergama_detail_section v2 (2026-10-19)"
SCRIPT = "bergama_detail_section_v2.py"
SCALE = 75.0                         # 1:75
K = 1000.0 / SCALE                   # page mm per metre
PAGE_W, PAGE_H = 1189.0, 841.0       # A0 landscape; grown if the drawing needs more
FIGURES_IN_FLOOD_REACH = True        # Nil 19 Oct: people on the terraces below the Q500 line too (never in water)
OUT_NAME = "Bergama_detail_section_S4_seasons_1to75.pdf"   # one page per season

# ---------------------------------------------------------------- the cut (survey)
S4_ID = "54d75849-9e70-41b1-8760-c001a59940dd"
S4_A = (30616.354683, 30540.470648)
S4_B = (31489.513378, 31161.826317)
# ground along S4 (TIN of the survey, see header), every 0.25 m from s 520 to 700
PROFILE_S0, PROFILE_DS = 520.0, 0.25
PROFILE_Z = [47.40, 47.40, 47.39, 47.39, 47.39, 47.38, 47.38, 47.37, 47.37, 47.36, 47.36, 47.35, 47.35, 47.34, 47.34, 47.33, 47.33, 47.32, 47.32, 47.32, 47.31, 47.31, 47.30, 47.30, 47.29, 47.29, 47.28, 47.28, 47.27, 47.27, 47.26, 47.26, 47.25, 47.25, 47.25, 47.24, 47.24, 47.23, 47.23, 47.22, 47.22, 47.21, 47.21, 47.20, 47.20, 47.19, 47.19, 47.18, 47.18, 47.18, 47.17, 47.17, 47.16, 47.16, 47.15, 47.15, 47.14, 47.14, 47.13, 47.13, 47.13, 47.13, 47.13, 47.12, 47.12, 47.12, 47.12, 47.12, 47.11, 47.11, 47.11, 47.11, 47.11, 47.11, 47.10, 47.10, 47.10, 47.10, 47.10, 47.10, 47.10, 47.09, 47.09, 47.09, 47.09, 47.09, 47.09, 47.09, 47.09, 47.09, 47.10, 47.10, 47.10, 47.10, 47.11, 47.11, 47.11, 47.12, 47.12, 47.12, 47.12, 47.13, 47.13, 47.13, 47.14, 47.14, 47.14, 47.14, 47.15, 47.15, 47.15, 47.15, 47.16, 47.16, 47.16, 47.17, 47.16, 47.16, 47.15, 47.14, 47.14, 47.13, 47.12, 47.11, 47.11, 47.10, 47.09, 47.09, 47.08, 47.07, 47.07, 47.06, 47.06, 47.06, 47.06, 47.06, 47.06, 47.07, 47.08, 47.09, 47.10, 47.11, 47.12, 47.13, 47.14, 47.15, 47.16, 47.17, 47.18, 47.19, 47.20, 47.21, 47.22, 47.23, 47.24, 47.25, 47.26, 47.27, 47.29, 47.30, 47.31, 47.32, 47.34, 47.35, 47.37, 47.39, 47.38, 47.36, 47.34, 47.31, 47.29, 47.27, 47.25, 47.23, 47.21, 47.19, 47.17, 47.14, 47.10, 47.07, 47.04, 47.00, 46.97, 46.94, 46.90, 46.87, 46.83, 46.80, 46.77, 46.73, 46.70, 46.67, 46.63, 46.60, 46.56, 46.53, 46.50, 46.46, 46.43, 46.40, 46.36, 46.33, 46.29, 46.26, 46.23, 46.19, 46.15, 46.12, 46.08, 46.03, 45.93, 45.84, 45.75, 45.65, 45.56, 45.47, 45.37, 45.28, 45.19, 45.09, 45.00, 44.91, 44.81, 44.72, 44.63, 44.53, 44.44, 44.35, 44.25, 44.16, 44.06, 44.04, 44.03, 44.02, 44.01, 44.01, 44.00, 43.99, 43.98, 43.98, 43.97, 43.96, 43.95, 43.95, 43.94, 43.93, 43.92, 43.92, 43.91, 43.90, 43.89, 43.89, 43.88, 43.87, 43.86, 43.86, 43.85, 43.84, 43.83, 43.83, 43.82, 43.81, 43.80, 43.80, 43.79, 43.78, 43.77, 43.77, 43.76, 43.75, 43.74, 43.74, 43.73, 43.72, 43.71, 43.71, 43.70, 43.69, 43.68, 43.68, 43.67, 43.66, 43.65, 43.65, 43.64, 43.63, 43.62, 43.61, 43.59, 43.59, 43.60, 43.61, 43.62, 43.63, 43.64, 43.66, 43.67, 43.68, 43.69, 43.70, 43.71, 43.72, 43.73, 43.74, 43.75, 43.77, 43.78, 43.79, 43.80, 43.81, 43.82, 43.83, 43.84, 43.85, 43.87, 43.88, 43.89, 43.90, 43.91, 43.92, 43.93, 43.94, 43.95, 43.97, 43.98, 43.99, 44.00, 44.01, 44.02, 44.03, 44.04, 44.05, 44.07, 44.08, 44.09, 44.10, 44.11, 44.12, 44.13, 44.14, 44.15, 44.17, 44.18, 44.19, 44.20, 44.21, 44.22, 44.23, 44.24, 44.25, 44.26, 44.27, 44.28, 44.29, 44.30, 44.31, 44.32, 44.33, 44.34, 44.35, 44.36, 44.37, 44.38, 44.39, 44.40, 44.41, 44.42, 44.43, 44.44, 44.45, 44.46, 44.47, 44.48, 44.48, 44.49, 44.49, 44.49, 44.50, 44.50, 44.51, 44.51, 44.51, 44.52, 44.52, 44.53, 44.53, 44.53, 44.54, 44.54, 44.54, 44.55, 44.55, 44.56, 44.56, 44.56, 44.57, 44.57, 44.58, 44.58, 44.58, 44.61, 44.73, 44.84, 44.96, 45.07, 45.19, 45.30, 45.42, 45.53, 45.64, 45.64, 45.64, 45.64, 45.64, 45.64, 45.64, 45.63, 45.63, 45.63, 45.63, 45.63, 45.63, 45.63, 45.63, 45.63, 45.62, 45.62, 45.62, 45.62, 45.62, 45.62, 45.62, 45.62, 45.62, 45.61, 45.61, 45.61, 45.64, 45.66, 45.69, 45.72, 45.75, 45.77, 45.80, 45.83, 45.86, 45.89, 45.91, 45.94, 45.97, 46.00, 45.96, 45.91, 45.86, 45.83, 45.83, 45.83, 45.83, 45.83, 45.83, 45.84, 45.84, 45.85, 45.85, 45.86, 45.86, 45.87, 45.87, 45.88, 45.89, 45.89, 45.90, 45.90, 45.91, 45.91, 45.92, 45.92, 45.93, 45.93, 45.94, 45.94, 45.95, 45.95, 45.96, 45.96, 45.97, 45.97, 45.98, 45.98, 45.99, 45.99, 46.00, 46.01, 46.02, 46.03, 46.05, 46.06, 46.07, 46.08, 46.09, 46.10, 46.11, 46.13, 46.14, 46.15, 46.16, 46.17, 46.18, 46.19, 46.21, 46.22, 46.23, 46.24, 46.25, 46.26, 46.27, 46.28, 46.30, 46.31, 46.32, 46.33, 46.34, 46.35, 46.36, 46.37, 46.38, 46.39, 46.40, 46.41, 46.42, 46.43, 46.44, 46.45, 46.46, 46.47, 46.48, 46.49, 46.50, 46.51, 46.52, 46.53, 46.54, 46.55, 46.56, 46.57, 46.57, 46.58, 46.58, 46.58, 46.58, 46.57, 46.57, 46.56, 46.56, 46.56, 46.55, 46.55, 46.55, 46.54, 46.54, 46.54, 46.53, 46.53, 46.52, 46.52, 46.52, 46.52, 46.52, 46.53, 46.53, 46.53, 46.54, 46.54, 46.54, 46.54, 46.55, 46.55, 46.55, 46.56, 46.56, 46.56, 46.57, 46.57, 46.57, 46.58, 46.58, 46.58, 46.59, 46.59, 46.59, 46.59, 46.60, 46.60, 46.60, 46.61, 46.61, 46.61, 46.62, 46.62, 46.62, 46.63, 46.63, 46.63, 46.64, 46.63, 46.63, 46.62, 46.61, 46.60, 46.59, 46.59, 46.58, 46.56, 46.55, 46.54, 46.52, 46.51, 46.50, 46.48, 46.47, 46.46, 46.44, 46.43, 46.42, 46.40, 46.39, 46.38, 46.36, 46.35, 46.34, 46.33, 46.31, 46.30, 46.29, 46.27, 46.26, 46.25, 46.23, 46.24, 46.25, 46.26, 46.28, 46.29, 46.31, 46.32, 46.33, 46.35, 46.36, 46.38, 46.39, 46.40, 46.42, 46.43, 46.45, 46.46, 46.47, 46.48, 46.49, 46.49, 46.50, 46.51, 46.52, 46.53, 46.53, 46.54, 46.55, 46.56, 46.57, 46.58, 46.58, 46.59, 46.60, 46.61, 46.62, 46.62, 46.63, 46.64, 46.65, 46.66, 46.66, 46.67, 46.68, 46.69, 46.70, 46.70, 46.71, 46.72, 46.73, 46.74, 46.75, 46.75, 46.76, 46.77, 46.78, 46.79, 46.79, 46.80, 46.82, 46.83, 46.84, 46.84, 46.84, 46.84, 46.83, 46.83, 46.83, 46.83, 46.82, 46.82, 46.82, 46.81, 46.81, 46.81, 46.81, 46.80, 46.80, 46.80, 46.80, 46.80, 46.79, 46.79]
SURVEY_MARKS = [   # (s, what, z or None): crossings of survey lines with S4 and spot heights within 4 m of it
    (549.48, "railing (SINIR_PARMAKLIK)", None),
    (561.86, "bank top (SEV_UST)", None),
    (570.97, "bank toe (SEV_ALT)", None),
    (619.95, "bank toe (SEV_ALT)", None),
    (626.06, "road edge (YOL_SOSE)", None),
    (629.99, "road edge (YOL_SOSE)", None),
    (555.05, "spot height", 46.84),
    (561.93, "spot height", 47.45),
    (571.12, "spot height", 46.21),
    (592.03, "spot height", 43.58),
    (633.49, "spot height", 45.80),
]
THALWEG = (592.03, 43.59)           # lowest ground on the cut (TIN), the bed's low point
Q100, Q500 = 45.84, 46.19           # v1.1: calculated on the surveyed cross-section at this cut (water board W2 note)
STRIP = (590.0, 594.0, 0.30)        # summer water strip: s from, s to, depth (design, case.md section 4)
DRY = 47.60                         # raised walk / promenade / balcony level (design; 1.41 m above Q500 since v1.1)

# ---------------------------------------------------------------- the four seasons (one page each)
# Climate per season: case.md section 1 (rain = WMO normals 1991-2020, MGM 17742, measured; open-water evaporation =
# Hargreaves x 1.05, calculated). River depths: case.md L13-L15 and section 3 (DSI gauges D04A053 Ilica + D04A063 Komurcu,
# WY2016-2021, area-scaled to the Selinos, Manning n 0.050). v1.1: the depths are this cut's own, on its surveyed
# cross-section (rain_river_levels/tables/A3s_*, A4s_*), above its bed low point (+43.59). Operating modes and life on the bands: Selinos riverfront
# design concept v1 (concept/Selinos_riverfront_design_concept_v1.md sections 5.4 and 10.1): DESIGN, ASSUMED/PROVISIONAL.
# water: (level, fill?, label, dash or None) - filled = the water body drawn; not filled = a level line only.
SEASONS = [
    dict(key="winter", name="WINTER", months="DEC - FEB", mode="WINTER · the river runs, storage fills",
         climate=["Rain 285.2 mm (46.0 % of 619.6 mm), 25.1 rain days, mean 7.6 C (measured, WMO 1991-2020).",
                  "Rain minus open-water evaporation +178.7 mm: the only surplus season (calculated, case.md s.1)."],
         river=["Jan-Feb monthly mean up to 0.43 m above the bed on this cut (calculated): +%.2f drawn." % (THALWEG[1] + 0.43),
                "Highest day 2016-2021, 6 Jan 2017: 1.15 m on this cut (calculated): +%.2f line." % (THALWEG[1] + 1.15),
                "Winter water goes into storage (Dec-Apr carries 89 % of the flow, calculated, rain_river README s.0)."],
         life=["Bed: flood channel, viewing only. Marsh: flooded, bird habitat. Terraces open between",
               "storms (concept s.10.1, design). People watch the river from the terrace edges and the balcony."],
         plants="Plane tree bare with its seed balls; reeds cut back after October; iris resting; lavender mound evergreen.",
         water=[(THALWEG[1] + 0.43, True, "Jan-Feb mean %+.2f (0.43 m)", None),
                (THALWEG[1] + 1.15, False, "highest day 6 Jan 2017 %+.2f (1.15 m)", [1.6, 0.6, 0.3, 0.6])],
         strip_held=False,
         people={"1": [(546.6, 0, True), (553.2, 3, False), (556.4, 4, True), (563.4, 1, False), (569.4, 4, False),
                       (570.5, 3, False)],
                 "2": [(647.6, 0, False), (640.6, 1, False), (627.0, 1, False), (618.2, 3, True), (604.4, 4, True),
                       (606.6, 11, True)]},
         bikes={"1": [], "2": [(650.6, True)]}),
    dict(key="spring", name="SPRING", months="MAR - MAY", mode="SPRING · the river runs, storage full by the end of April",
         climate=["Rain 148.6 mm (24.0 %), 17.2 rain days, mean 15.0 C (measured, WMO 1991-2020).",
                  "Rain minus open-water evaporation -207.5 mm: the deficit starts (calculated, case.md s.1)."],
         river=["Jan-Apr monthly means 0.25-0.43 m above the bed on this cut (calculated): Mar-Apr drawn at the",
                "low end 0.25 m (+%.2f), the high end as a line; May 0.16-0.21 m (calculated)." % (THALWEG[1] + 0.25),
                "The strip runs on the river while there is enough flow; storage tops up (design, water loop)."],
         life=["Strip and bed with water again. Marsh greens up, boardwalk open; flowering",
               "meadow and play (concept s.10.1, design). Children and parents at the water's edge."],
         plants="Fresh leaves; reeds green up from the cut stubble; yellow iris and lavender in flower.",
         water=[(THALWEG[1] + 0.25, True, "Mar-Apr, low end of the range %+.2f (0.25 m)", None),
                (THALWEG[1] + 0.43, False, "high end of the Jan-Apr range %+.2f (0.43 m)", [0.4, 0.6])],
         strip_held=True,
         people={"1": [(538.9, 2, False), (546.6, 0, True), (547.6, 1, False), (553.2, 3, False), (555.6, 0, False),
                       (563.0, 1, True), (564.2, 3, False), (569.6, 4, False), (580.2, 3, False), (582.6, 4, False),
                       (583.4, 7, False)],
                 "2": [(647.6, 0, False), (646.4, 2, True), (640.6, 1, False), (635.0, 2, False), (630.0, 0, True),
                       (618.2, 3, True), (599.4, 7, True), (601.0, 11, True), (604.0, 2, True)]},
         bikes={"1": [(543.0, False)], "2": [(650.6, True)]}),
    dict(key="summer", name="SUMMER", months="JUN - AUG", mode="SUMMER · the strip runs on stored water",
         climate=["Rain 28.5 mm (4.6 %), 5.9 rain days, mean 26.5 C (measured, WMO 1991-2020).",
                  "Rain minus open-water evaporation -552.2 mm: the deepest deficit (calculated, case.md s.1)."],
         river=["Natural river Jul-Sep: monthly means 0.04-0.11 m on this cut, a trickle (calculated, indicative: bed",
                "interpolated); bed dry (< 2 cm) about 11 days a year. Drawn: the continuous regulated water strip 4.0 x 0.30 m, topped up from",
                "storage and flowing one way downstream (design, case.md s.4; Aras 17 Oct 22:01, 19 Oct 07:43)."],
         life=["All bands open; the strip used: wading at 0.30 m, cooling, evening lights; dry meadow",
               "as a lie-down lawn (concept s.10.1, design). People sit at the strip edge with their feet in the water."],
         plants="Full leaf; reeds at full height, first plumes; iris in leaf; last lavender spikes; meadow drying.",
         water=[],
         strip_held=True,
         people={"1": [(538.9, 2, False), (546.6, 0, True), (547.6, 1, False), (553.2, 3, False), (555.6, 0, False),
                       (556.4, 4, True), (563.0, 1, True), (564.2, 3, False), (581.5, 9, False), (585.6, 10, False),
                       (588.2, 7, False), (589.85, 8, False)],
                 "2": [(647.6, 0, False), (646.4, 2, True), (640.6, 1, False), (635.0, 2, False), (630.0, 0, True),
                       (627.0, 1, False), (618.2, 3, True), (594.15, 8, False), (595.6, 7, True), (597.4, 4, True),
                       (600.5, 3, True)]},
         bikes={"1": [(543.0, False)], "2": [(650.6, True)]}),
    dict(key="autumn", name="AUTUMN", months="SEP - NOV", mode="AUTUMN · storage low until the rains return",
         climate=["Rain 157.3 mm (25.4 %), 14.1 rain days, mean 17.7 C (measured, WMO 1991-2020).",
                  "Rain minus open-water evaporation -102.5 mm; Nov turns to surplus (calculated, case.md s.1)."],
         river=["Sep 0.05-0.07 m; Oct-Dec monthly means 0.11-0.20 m above the bed on this cut (calculated):",
                "the high end 0.20 m drawn (+%.2f). Design storm 137 mm in one day" % (THALWEG[1] + 0.20),
                "(28 Oct 2025, municipal figure, not MGM-confirmed). The strip runs on the river again after the first storms."],
         life=["First-flush cleaning and maintenance of the strip; marsh seed heads, cut back after October;",
               "events on the meadow after the reset (concept s.10.1, design). People walk the gravel bed to the water."],
         plants="Plane leaves turning; reeds gold with seed heads; iris leaves yellowing; lavender trimmed.",
         water=[(THALWEG[1] + 0.20, True, "Oct-Dec high end %+.2f (0.20 m)", None)],
         strip_held=True,
         people={"1": [(538.9, 2, False), (547.6, 1, False), (553.2, 3, False), (556.4, 4, True), (563.0, 1, True),
                       (569.6, 3, False), (582.0, 2, False), (586.4, 0, False), (588.4, 4, False)],
                 "2": [(647.6, 0, False), (640.6, 1, False), (630.0, 0, True), (618.2, 3, True), (595.4, 3, True),
                       (597.8, 2, True), (602.0, 0, True)]},
         bikes={"1": [(543.0, False)], "2": [(650.6, True)]}),
]
DAYS_WET = "Days a year at or above each height on this cut (mean WY2016-2021, calculated; below 0.3 m indicative): " \
           "0.10 m 278 d, 0.30 m 69 d, 0.50 m 9 d, 1.00 m under 1 d; bed dry (< 2 cm) about 11 d."

# ---------------------------------------------------------------- the design (all design values)
# surfaces: (s from, s to, level, material, swatch label) left to right as drawn
SECTIONS = [
    dict(key="1", title="SECTION 1-1'", side="SOUTH-WEST BANK", s_from=538.0, s_to=598.0, look="looking north-west (upstream)",
         surfaces=[(538.0, 542.0, 47.15, "veg", "Native vegetation"),
                   (542.0, 544.0, 47.15, "asphalt", "Coloured asphalt"),
                   (544.0, 548.0, 47.15, "concrete", "Concrete walkway"),
                   (548.0, 551.0, 47.20, "lavender", "Lavender bed"),
                   (551.0, 554.0, DRY, "concrete", "Concrete walkway"),
                   (554.0, 557.0, 46.70, "deck", "Wooden deck"),
                   (557.0, 561.0, 45.80, "veg", "Native vegetation"),
                   (561.0, 565.0, 44.90, "deck", "Wooden deck"),
                   (565.0, 571.0, 44.20, "veg", "Native vegetation")],
         regrade=(571.0, 578.0),            # gravel slope from the last terrace down to the existing bed
         band_more=[(571.0, 590.0, "gravel", "River gravel"), (590.0, 594.0, "water", "Summer water strip")],
         rails=[(554.0, -1), (565.0, -1)],   # (s, side of the post: -1 = just left of s) single posts at edges
         trees=[(541.0, 3.9, 7.5, "plane")],
         shrubs=[(558.2, 1.3, 1.1), (559.9, 1.5, 1.2), (566.3, 1.7, 1.4), (568.2, 1.9, 1.5), (570.0, 1.5, 1.2)],
         grass=[(538.0, 542.0), (557.0, 561.0), (565.0, 571.0)],
         lavender=[(548.2, 550.8)],
         reeds=[(573.5, 576.5, 1.9), (580.0, 588.5, 2.2), (595.0, 598.0, 2.0)],
         iris=[(576.5, 580.0), (588.5, 589.6)],
         callouts=[(540.0, None, "Greenery and planters (plane tree)"),
                   (543.0, None, "Bike way"),
                   (546.0, None, "Concrete walkway"),
                   (549.5, None, "Lavender bed above the bank top"),
                   (552.4, None, "Raised walk +47.60 above Q500"),
                   (553.85, DRY + 1.10, "Handrail corten steel"),
                   (555.5, None, "Multilevel walkway platforms"),
                   (559.0, None, "Flood- and drought-tolerant planting"),
                   (563.2, None, "Floodable boardwalk, open deck"),
                   (568.0, None, "Tamarix and Vitex terrace"),
                   (582.0, None, "Reeds and iris at the bed edge"),
                   (592.0, None, "Summer water strip 4.0 x 0.30 m")]),
    dict(key="2", title="SECTION 2-2'", side="NORTH-EAST BANK", s_from=652.0, s_to=588.0, look="looking south-east (downstream)",
         surfaces=[(652.0, 649.0, DRY, "asphalt", "Coloured asphalt"),
                   (649.0, 645.0, DRY, "concrete", "Concrete walkway"),
                   (645.0, 642.0, DRY, "veg", "Native vegetation"),
                   (642.0, 638.0, DRY, "concrete", "Concrete walkway"),
                   ("steps", 638.0, 633.5, DRY, 45.35, 5, "concrete", "Concrete steps"),
                   (633.5, 622.5, 45.35, "concrete", "Concrete walkway")],
         regrade=(622.5, 619.95),
         band_more=[(619.95, 594.0, "gravel", "River gravel"), (594.0, 590.0, "water", "Summer water strip")],
         rails=[],
         balcony=dict(s0=638.0, s1=617.0, top=DRY, thick=0.35, columns=(631.0, 624.0)),
         pergola=dict(posts=(649.6, 645.4), plates=[(650.6, 644.6, 3.20), (648.4, 643.2, 3.55)]),
         trees=[(643.5, 3.9, 7.5, "plane")],
         shrubs=[(644.5, 1.0, 0.8), (642.4, 0.9, 0.7), (621.3, 1.2, 1.0)],
         grass=[(645.0, 642.0), (622.5, 619.95)],
         lavender=[],
         reeds=[(619.5, 612.0, 2.2), (607.0, 600.0, 1.9)],
         iris=[(612.0, 609.0), (596.5, 595.0)],
         callouts=[(650.5, None, "Bike way"),
                   (648.0, DRY + 3.55, "Shading structures"),
                   (646.4, None, "Walkway"),
                   (643.5, None, "Greenery and planters"),
                   (640.0, None, "Promenade +47.60 above Q500"),
                   (636.0, None, "Amphitheatre toward the river"),
                   (628.0, None, "Floodable lower walk"),
                   (625.0, DRY + 1.10, "Handrail corten steel"),
                   (619.0, DRY, "Balcony towards the river (beyond the cut)"),
                   (624.0, 46.40, "Column support"),
                   (610.0, None, "Reeds and iris at the bed edge"),
                   (592.0, None, "Summer water strip 4.0 x 0.30 m")]),
]

# ---------------------------------------------------------------- colours (reference language)
INK = "1E1E1E"
INK2 = "5A5A5A"
GREY = "8C8C8C"
DIM = "D0342C"            # the reference's red dimension strings
STIPPLE = "6E6E6E"
CONCRETE = "E3E2DE"
CONCRETE_DOT = "9A9893"
ASPHALT = "A5473C"
DECK = "C8A27A"
DECK_DARK = "8A6A48"
CORTEN = "6B4A36"
WATER = "CFE6F1"
WATER_LINE = "7DB3D3"
FLOOD = "3F86B8"
FIG = "3B3B3B"             # the reference's figure grey-black
GREEN_LINE = "8DAA5C"
GREEN_FILL = "D3E3B1"
REED = "A7A57C"
REED_HEAD = "B49A6C"
LAV = "9F86C0"
IRIS = "6E8F4A"
IRIS_FLOWER = "D9B640"
TEAL = "107C73"           # NIL working area (scripts/study_area_style.md)
TREE_STYLE_REF = dict(dark="9FBA6E", mid="BCD192", light="DCE8C0", trunk="7B8B57", shadow="9FBA6E", shadow_a=0.0,
                      lobes=2.6, blob=0.55)   # the reference's light green, through the v1.8 tree: finer clusters


# ================================================================ traced entourage from Nil's reference
ASSET_B64 = (
    "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"
    "6bxEbtLyZoncRNRLuprnv9qXbycvMSxca+peON5dWx8xLEaJWkHE1mcMi4H4HU14+ZvWFOm8ROzQ8uafGB2t1NNLG25B+w96/C671GaXmirDfc"
    "bCGCU6yyiRW4bGtEA6K3laKc+kpkznkuf8Ew2mlWgwrdTTSxtuQfsPEpYERHJKNCTyeolvnmzwEdGH6JQvb8nFJTqUlfIS3fKlSy7jTwShViII"
    "tVJPL224Be0/6LX+CL8/0ZVbGv0zGuJTEK2CRsmlS0z6htvdLugW5JLuljxvKT3RLelc8uzI0wraBc2Cxj964i9S/kbXe3dGFwhGQy+sjA7uw1"
    "3QLcglnZc8vZSX6JZ0XljspTxBo6Be0tU8/9U+vpvlX6DB12m2Ijjf+W7eBd2CpPXBRl/e1Civa02RzuW93bS8U9/UTXlUrLz9Jc9/tW//4Wre"
    "hT94FnbmIazH5GreBZ2CbkknTOePVwrlJbrlS5dcyGy8Cxr/t6zHt6D9B2XrO3mA/y8YoE9B+5/s0E0YoP9/c0Xvgm5BLulGyXP8Kd1LPa2wWP"
    "+L09r/oIwFMMmXHLzOExzMQ/iZkw/VhYN+6Lsx+HSJjrA1r8LkvMAlfwvHtBW0CuN0rWeit3vt4FXdwm08wJ78+Fi7cCmTBXkXdAtySWclTyvl"
    "JbolnUues5RHNArqJV3N81/t24iv+dhSd+FcHYy2CQ7dHoy6GUV9F3QLckk3Sp6jlDeUsRjpXPLspTyiUVD/B2/sLWj/QclSRI48oiH8QhfcPK"
    "Pwse6CKlerS7pe8uylvES3pPPCMNv+ySk7Cur/4JS9Be0/SOIN579Ag7L4bMXTYwpr5S6oMlpK6+8uee5S3taaIp1Lnl7Kc/EmVNRLuprnv9qX"
    "r5xeGPt6YZTrws6YnEn0BdgF3YKEydBHyXP8YQhswt+X6VzyvKU8olFQL+lqnv9qn/q5/LimtjC1US/ehf3tMV1NaFd2Qbcgl3Sz5DlLeYluSe"
    "eS5yrlLfE0UdRLuprnv9q3VdOTbHdAounZQzU9wuK2/8HpJpoepDslz1PKS3RLOtH07FnKKxFVBfV/cM/dgvYfpLteL7tCL7teL7teL7tQ5VHr"
    "ZdfrZdfrZdfrZdfrZdfrZdcbpbxRdr1Rdr1edr2/PHH7D0pL8/YxSsk6XPSzfFxinUydYB0bykT1h59sBFeaMIshz1nKS3RLOuE8203LEzQK6i"
    "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"
    "Q="
)
PX_PER_M = 46.0 / 1.75              # the reference's adult walker: 46 px tall = 1.75 m
_ASSETS = []


def assets():
    if not _ASSETS:
        import base64
        _ASSETS.append(json.loads(zlib.decompress(base64.b64decode("".join(ASSET_B64))).decode("utf-8")))
    return _ASSETS[0]


def draw_asset(pg, key, X, Y, height_mm=None, flip=False, layer="entourage", tone=None):
    """A traced asset with its anchor (feet / base) at page (X, Y). height_mm None = the reference's own size at
    1:75; tone = one colour for every layer (None = the traced colours)."""
    A = assets()[key]
    ax, ay = A["anchor"]
    h0 = A["bbox"][3] - A["bbox"][1]
    s = (height_mm / h0) if height_mm else K / PX_PER_M
    fx = -1.0 if flip else 1.0
    for fill, op, loops in A["layers"]:
        rings = [[(X + fx * (x - ax) * s, Y + (ay - y) * s) for x, y in loop] for loop in loops]
        pg.poly(rings, fill=tone or fill, stroke=None, layer=layer, alpha=op)


# ================================================================ reused blocks (copied unchanged from bergama_diagrams_v1_8.py)
# ============================================================ TEXT METRICS (Helvetica = Arial metrics)
_MCH = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~€‚ƒ„…†‡ˆ‰Š‹ŒŽ‘’“”•–—˜™š›œžŸ\xa0¡¢£¤¥¦§¨©ª«¬\xad®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĞğİıŞş'
_MW0 = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556, 333, 556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584, 556, 222, 556, 333, 1000, 556, 556, 333, 1000, 667, 333, 1000, 611, 222, 222, 333, 333, 350, 556, 1000, 333, 1000, 500, 333, 944, 500, 667, 278, 333, 556, 556, 556, 556, 260, 556, 333, 737, 370, 556, 584, 333, 737, 552, 400, 549, 333, 333, 333, 576, 537, 333, 333, 333, 365, 556, 834, 834, 834, 611, 667, 667, 667, 667, 667, 667, 1000, 722, 667, 667, 667, 667, 278, 278, 278, 278, 722, 722, 778, 778, 778, 778, 778, 584, 778, 722, 722, 722, 722, 667, 667, 611, 556, 556, 556, 556, 556, 556, 889, 500, 556, 556, 556, 556, 278, 278, 278, 278, 556, 556, 556, 556, 556, 556, 556, 549, 611, 556, 556, 556, 556, 500, 556, 500, 778, 556, 278, 278, 667, 500]
_MW1 = [278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 333, 333, 584, 584, 584, 611, 975, 722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722, 611, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 333, 278, 333, 584, 556, 333, 556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889, 611, 611, 611, 611, 389, 556, 333, 611, 556, 778, 556, 556, 500, 389, 280, 389, 584, 556, 278, 556, 500, 1000, 556, 556, 333, 1000, 667, 333, 1000, 611, 278, 278, 500, 500, 350, 556, 1000, 333, 1000, 556, 333, 944, 500, 667, 278, 333, 556, 556, 556, 556, 280, 556, 333, 737, 370, 556, 584, 333, 737, 552, 400, 549, 333, 333, 333, 576, 556, 333, 333, 333, 365, 556, 834, 834, 834, 611, 722, 722, 722, 722, 722, 722, 1000, 722, 667, 667, 667, 667, 278, 278, 278, 278, 722, 722, 778, 778, 778, 778, 778, 584, 778, 722, 722, 722, 722, 667, 667, 611, 556, 556, 556, 556, 556, 556, 889, 556, 556, 556, 556, 556, 278, 278, 278, 278, 611, 611, 611, 611, 611, 611, 611, 549, 611, 611, 611, 611, 611, 556, 611, 556, 778, 611, 278, 278, 667, 556]
_W = [dict(zip(_MCH, _MW0)), dict(zip(_MCH, _MW1))]
PT = 25.4 / 72.0                      # mm per point
CAP = 0.716                           # cap height / em (Arial, Helvetica)


def text_w(s, size_mm, bold=False):
    w = _W[1 if bold else 0]
    return sum(w.get(c, 556) for c in s) / 1000.0 * size_mm


def area2(P):
    return sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P))) / 2.0


def pip(x, y, P):
    c = False
    j = len(P) - 1
    for i in range(len(P)):
        if (P[i][1] > y) != (P[j][1] > y) and x < (P[j][0] - P[i][0]) * (y - P[i][1]) / (P[j][1] - P[i][1]) + P[i][0]:
            c = not c
        j = i
    return c
# ============================================================ PAGE (vector items in mm, y up)
class Page(object):
    def __init__(self, pid, title):
        self.pid, self.title, self.items = pid, title, []

    def poly(self, rings, fill=None, stroke=None, lw=0.1, dash=None, layer="drawing", join=1, stripes=None, alpha=None):
        """alpha: opacity 0-1 of fill and stroke (PDF only, in steps of 0.05; None = opaque)."""
        rings = [r for r in rings if len(r) >= 3]
        if rings:
            self.items.append(("poly", rings, fill, stroke, lw, dash, layer, join, stripes, alpha))

    def line(self, pts, stroke, lw=0.1, dash=None, layer="drawing", cap=1):
        if len(pts) >= 2:
            self.items.append(("line", pts, stroke, lw, dash, layer, cap))

    def circle(self, cx, cy, r, fill=None, stroke=None, lw=0.1, layer="drawing"):
        self.items.append(("circle", cx, cy, r, fill, stroke, lw, layer))

    def text(self, s, x, y, size, color, bold=False, align="L", layer="text", mat=None, halo=None):
        """size = em in mm; align L, C or R on the baseline; mat = 2 x 2 text matrix (columns: text x and y axes per
        mm of em) for words lying in a drawing plane."""
        if s:
            self.items.append(("text", s, x, y, size, color, bold, align, layer, mat, halo))


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


# ================================================================ profile
def prof_z(prof, s):
    s0, ds, Z = prof
    f = (s - s0) / ds
    i = int(math.floor(f))
    if i < 0:
        return Z[0]
    if i >= len(Z) - 1:
        return Z[-1]
    t = f - i
    return Z[i] * (1 - t) + Z[i + 1] * t


def wrap(s, n):
    out, cur = [], ""
    for w in s.split():
        if cur and len(cur) + 1 + len(w) > n:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(cur)
    return out


class Sec(object):
    """One section: s along S4 -> page x, level -> page y (true 1:75)."""

    def __init__(self, d, prof):
        self.d, self.prof = d, prof
        self.dir = 1.0 if d["s_to"] > d["s_from"] else -1.0
        self.lo, self.hi = min(d["s_from"], d["s_to"]), max(d["s_from"], d["s_to"])
        self.zb = THALWEG[1] - STRIP[2] - 1.9           # bottom of the poche
        self.X0 = self.Y0 = 0.0
        self.build_surface()

    def X(self, s):
        return self.X0 + (s - self.d["s_from"]) * self.dir * K

    def Y(self, z):
        return self.Y0 + (z - self.zb) * K

    def P(self, s, z):
        return (self.X(s), self.Y(z))

    def ex(self, s):
        return prof_z(self.prof, s)

    def build_surface(self):
        """Finished surface as (s, z) vertices in drawing order (left to right), vertical steps at wall lines."""
        d = self.d
        V = []
        self.steps = []          # (s, z_hi, z_lo, high side: -1 left / +1 right in drawing order)
        self.flats = []          # (s_a, s_b, z, material, label)
        prev = None
        for srf in d["surfaces"]:
            if srf[0] == "steps":
                _, sa, sb, za, zb, n, mat, lab = srf
                if prev is not None and abs(prev - za) > 1e-6:
                    V.append((sa, za))
                tr = (sb - sa) / n
                rz = (zb - za) / n
                for i in range(n):
                    V.append((sa + i * tr, za + i * rz))
                    V.append((sa + (i + 1) * tr, za + i * rz))
                V.append((sb, zb))
                self.flats.append((sa, sb, None, mat, lab))
                self.stair = (sa, sb, za, zb, n)
                prev = zb
                continue
            sa, sb, z, mat, lab = srf
            if prev is not None and abs(prev - z) > 1e-6:
                self.steps.append((sa, max(prev, z), min(prev, z), -1 if prev > z else 1))
            V.append((sa, z))
            V.append((sb, z))
            self.flats.append((sa, sb, z, mat, lab))
            prev = z
        ra, rb = d["regrade"]
        V.append((rb, self.ex(rb)))
        n = int(abs(d["s_to"] - rb) / 0.25)
        for i in range(1, n + 1):
            s = rb + (d["s_to"] - rb) * i / n
            V.append((s, self.ex(s)))
        # summer strip: a 4 m low-flow channel cut 0.30 m into the bed at the low point; water flush with the bed
        a, b, dep = STRIP
        W = []
        for p in V:
            if min(a, b) < p[0] < max(a, b):
                continue
            W.append(p)
        out = []
        for i, p in enumerate(W):
            out.append(p)
            if i + 1 < len(W):
                q = W[i + 1]
                lo_, hi_ = sorted((p[0], q[0]))
                if lo_ <= min(a, b) and hi_ >= max(a, b):
                    e1, e2 = (a, b) if self.dir > 0 else (b, a)
                    zt = THALWEG[1]
                    out += [(e1, self.ex(e1)), (e1, zt - dep), (e2, zt - dep), (e2, self.ex(e2))]
        self.V = out
        self.design_end = rb

    def surf(self, s):
        """Surface level at s (the lower side at a vertical step)."""
        V = self.V
        best = None
        for i in range(len(V) - 1):
            a, b = V[i], V[i + 1]
            lo_, hi_ = sorted((a[0], b[0]))
            if lo_ - 1e-9 <= s <= hi_ + 1e-9:
                if abs(b[0] - a[0]) < 1e-9:
                    z = min(a[1], b[1])
                else:
                    z = a[1] + (b[1] - a[1]) * (s - a[0]) / (b[0] - a[0])
                best = z if best is None else min(best, z)
        return best if best is not None else self.ex(s)


# ================================================================ drawing pieces
def rng(*parts):
    return random.Random(zlib.crc32(repr(parts).encode("utf-8")) & 0x7fffffff)


def poche(pg, S):
    """Earth: white, a heavy cut line on top, stipple and pebbles that thin out with depth (as in the reference)."""
    V = S.V
    ring = [S.P(*p) for p in V] + [S.P(V[-1][0], S.zb), S.P(V[0][0], S.zb)]
    pg.poly([ring], fill="FFFFFF", stroke=None, layer="poche")
    r = rng("poche", S.d["key"])
    x0, x1 = sorted((S.X(S.d["s_from"]), S.X(S.d["s_to"])))
    n = int((x1 - x0) * 26.0)
    for _ in range(n):
        s = S.lo + r.random() * (S.hi - S.lo)
        top = S.surf(s)
        z = S.zb + r.random() * (top - S.zb)
        dep = top - z
        keep = (0.22 + 0.78 * math.exp(-dep / 0.9)) * min(1.0, (z - S.zb) / 1.2)
        if r.random() > keep or dep < 0.05:
            continue
        X, Y = S.P(s, z)
        if r.random() < 0.06 and dep > 0.18:                       # pebble
            R = 0.25 + r.random() * 0.55
            m = 4 + int(r.random() * 3)
            ph = r.random() * 6.28
            pts = [(X + R * (0.7 + 0.5 * r.random()) * math.cos(ph + 6.283 * i / m),
                    Y + R * 0.8 * (0.7 + 0.5 * r.random()) * math.sin(ph + 6.283 * i / m)) for i in range(m)]
            pg.poly([pts], fill=None, stroke=STIPPLE, lw=0.09, layer="poche")
        else:
            R = 0.10 + r.random() * (0.18 + 0.22 * math.exp(-dep / 1.5))
            pg.circle(X, Y, R, fill=("4A4A4A", "6E6E6E", "9A9A9A")[int(r.random() * 3)], layer="poche")
    pg.line([S.P(*p) for p in V], INK, 0.5, layer="cut line")


SOIL = "E9E3CF"                     # soft planting ground: a warm, slightly darker tone than the white earth poche
SOIL_DOT = ("B3A386", "C9BC9F", "9C8D70")
SOIL_DEPTH = 0.40                   # topsoil under planting, m (design value)


def soft_ground(pg, S):
    """A soft topsoil layer under every planted stretch (grass, lavender, shrubs, reeds, iris): it follows the finished
    surface, has a soft wavy underside and a fine soil grain; walls and slabs are drawn over it."""
    d = S.d
    spans = [tuple(sorted(x[:2])) for x in d["grass"] + d["lavender"] + d["iris"]]
    spans += [tuple(sorted(x[:2])) for x in d["reeds"]]
    spans += [(s - w / 2.0, s + w / 2.0) for s, h, w in d["shrubs"]]
    spans = sorted((max(a, S.lo), min(b, S.hi)) for a, b in spans if min(b, S.hi) > max(a, S.lo))
    merged = []
    for a, b in spans:
        if merged and a <= merged[-1][1] + 0.3:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    lo_w, hi_w = sorted(STRIP[:2])
    out = []
    for a, b in merged:                                 # never under the water strip
        if b <= lo_w or a >= hi_w:
            out.append((a, b))
        else:
            if a < lo_w:
                out.append((a, lo_w))
            if b > hi_w:
                out.append((hi_w, b))
    r = rng("soil", d["key"])
    for a, b in out:
        n = max(2, int((b - a) / 0.1))
        ss = [a + (b - a) * i / n for i in range(n + 1)]
        top = [S.P(s, S.surf(s)) for s in ss]
        ph = r.random() * 6.28
        bot = []
        for i, s in enumerate(ss):
            t_ = min(1.0, min(s - a, b - s) / 0.6)          # the layer thins out at its ends
            dep = SOIL_DEPTH * (0.35 + 0.65 * t_) * (1.0 + 0.12 * math.sin(ph + s * 2.3) + 0.06 * math.sin(s * 7.1))
            bot.append(S.P(s, S.surf(s) - dep))
        ring = top + bot[::-1]
        pg.poly([ring], fill=SOIL, stroke=None, layer="soft ground")
        xs = [p[0] for p in ring]
        ys = [p[1] for p in ring]
        area = abs(area2(ring))
        for _ in range(int(area * 1.6)):
            X = min(xs) + r.random() * (max(xs) - min(xs))
            Y = min(ys) + r.random() * (max(ys) - min(ys))
            if pip(X, Y, ring):
                pg.circle(X, Y, 0.06 + r.random() * 0.12, fill=SOIL_DOT[int(r.random() * 3)], layer="soft ground")
        for i in range(0, len(top) - 1, 3):                 # a few root hairs just under the surface
            if r.random() < 0.35:
                X, Y = top[i]
                pg.line([(X, Y - 0.3), (X + (r.random() - 0.5) * 1.2, Y - 1.0 - r.random() * 2.0)], "A39577", 0.05,
                        layer="soft ground")


def concrete(pg, S, ring_m, layer="concrete"):
    ring = [S.P(s, z) for s, z in ring_m]
    pg.poly([ring], fill=CONCRETE, stroke=INK, lw=0.35, layer=layer)
    xs = [p[0] for p in ring]
    ys = [p[1] for p in ring]
    r = rng("conc", round(xs[0], 2), round(ys[0], 2))
    area = abs(area2(ring)) if len(ring) > 2 else 0.0
    for _ in range(int(area * 0.9)):
        X = min(xs) + r.random() * (max(xs) - min(xs))
        Y = min(ys) + r.random() * (max(ys) - min(ys))
        if pip(X, Y, ring):
            R = 0.08 + r.random() * 0.1
            pg.poly([[(X - R, Y - R), (X + R, Y - R), (X, Y + R)]], fill=CONCRETE_DOT, stroke=None, layer=layer)


def walls_and_slabs(pg, S):
    t = 0.30                                    # wall thickness (design)
    for s, zh, zl, side in S.steps:
        if zh - zl < 0.15:                      # a kerb, not a wall
            continue
        # wall on the high side of the step, drawn left to right in drawing order
        sgn = -S.dir if side < 0 else S.dir     # towards the high side, in s
        a, b = s, s + sgn * t
        concrete(pg, S, [(a, zh), (b, zh), (b, zl - 0.55), (a, zl - 0.55)])
        f0, f1 = s + sgn * (t + 0.35), s - sgn * 0.55
        concrete(pg, S, [(f0, zl - 0.55), (f1, zl - 0.55), (f1, zl - 0.85), (f0, zl - 0.85)])
    for sa, sb, z, mat, lab in S.flats:
        if z is None:                           # amphitheatre steps: a stepped concrete slab
            a, b, za, zb, n = S.stair
            tr, rz = (b - a) / n, (zb - za) / n
            top = []
            for i in range(n):
                top += [(a + i * tr, za + i * rz), (a + (i + 1) * tr, za + i * rz)]
            top.append((b, zb))
            concrete(pg, S, top + [(b, zb - 0.30), (a, za - 0.30)])     # stair slab, straight soffit
            continue
        if mat == "concrete":
            concrete(pg, S, [(sa, z), (sb, z), (sb, z - 0.18), (sa, z - 0.18)])
        elif mat == "asphalt":
            pg.poly([[S.P(sa, z), S.P(sb, z), S.P(sb, z - 0.08), S.P(sa, z - 0.08)]], fill=ASPHALT, stroke=INK,
                    lw=0.25, layer="asphalt")
            concrete(pg, S, [(sa, z - 0.08), (sb, z - 0.08), (sb, z - 0.25), (sa, z - 0.25)])
        elif mat == "deck":
            pg.poly([[S.P(sa, z), S.P(sb, z), S.P(sb, z - 0.06), S.P(sa, z - 0.06)]], fill=DECK, stroke=INK,
                    lw=0.25, layer="deck")
            n = max(2, int(abs(sb - sa) / 0.6))
            for i in range(n + 1):
                s = sa + (sb - sa) * (0.04 + 0.92 * i / n)
                X, Y = S.P(s, z - 0.06)
                pg.poly([[(X - 0.55, Y), (X + 0.55, Y), (X + 0.55, Y - 1.6), (X - 0.55, Y - 1.6)]], fill=DECK_DARK,
                        stroke=None, layer="deck")
            concrete(pg, S, [(sa, z - 0.18), (sb, z - 0.18), (sb, z - 0.38), (sa, z - 0.38)])
    # terrace edges below the level of the decks are retained by the walls; edge of the regraded bank: stone toe
    ra, rb = S.d["regrade"]
    zr = S.surf(ra + (rb - ra) * 0.02)
    concrete(pg, S, [(ra, zr), (ra + (rb - ra) * 0.08, zr), (ra + (rb - ra) * 0.08, zr - 0.5), (ra, zr - 0.5)])


BEYOND = "A3A3A3"                   # lines of things standing beyond the cut
BEYOND_FILL = "F5F5F3"
BEYOND_CORTEN = "C4A794"
BEYOND_FIG = "9A9A9A"
OAK = "B88A5A"


def _rrect(x0, y0, x1, y1, rad, n=3):
    """Rounded rectangle (handrail profile)."""
    pts = []
    for cx, cy, a0 in ((x1 - rad, y1 - rad, 0.0), (x0 + rad, y1 - rad, 90.0), (x0 + rad, y0 + rad, 180.0),
                       (x1 - rad, y0 + rad, 270.0)):
        for k_ in range(n + 1):
            a = math.radians(a0 + 90.0 * k_ / n)
            pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return pts


def handrail(pg, S, s, z):
    """Railing cut by the section (it runs along the river): corten flat-bar post 60 x 15 on a base plate with two
    anchors, corten saddle and oak handrail 70 x 45 (top +1.10 m), bottom rail 40 x 40 at +0.10 m (design values)."""
    X, Y = S.P(s, z)
    k = K
    w = 0.06 * k
    pg.poly([[(X - 0.10 * k, Y), (X + 0.10 * k, Y), (X + 0.10 * k, Y + 0.02 * k), (X - 0.10 * k, Y + 0.02 * k)]],
            fill=CORTEN, stroke=INK, lw=0.05, layer="handrail")                       # base plate 200 x 20
    for dx in (-0.065, 0.065):                                                         # chemical anchors
        pg.line([(X + dx * k, Y), (X + dx * k, Y - 0.12 * k)], INK2, 0.08, dash=[0.3, 0.2], layer="handrail")
    pg.poly([[(X - w / 2, Y + 0.02 * k), (X + w / 2, Y + 0.02 * k), (X + w * 0.4, Y + 1.03 * k),
              (X - w * 0.4, Y + 1.03 * k)]], fill=CORTEN, stroke=INK, lw=0.06, layer="handrail")
    pg.poly([[(X - 0.025 * k, Y + 1.03 * k), (X + 0.025 * k, Y + 1.03 * k), (X + 0.025 * k, Y + 1.055 * k),
              (X - 0.025 * k, Y + 1.055 * k)]], fill=CORTEN, stroke=INK, lw=0.04, layer="handrail")   # saddle
    pg.poly([_rrect(X - 0.035 * k, Y + 1.055 * k, X + 0.035 * k, Y + 1.10 * k, 0.012 * k)], fill=OAK, stroke=INK,
            lw=0.06, layer="handrail")                                                 # oak handrail, cut
    pg.poly([[(X - 0.02 * k, Y + 0.08 * k), (X + 0.02 * k, Y + 0.08 * k), (X + 0.02 * k, Y + 0.12 * k),
              (X - 0.02 * k, Y + 0.12 * k)]], fill=CORTEN, stroke=INK, lw=0.04, layer="handrail")   # bottom rail


def railing_elevation(pg, S, s0, s1, z, beyond=False, layer="handrail"):
    """Railing seen in elevation (parallel to the section plane): posts at most 1.5 m apart, side-fixed to the slab edge
    with a plate and two bolts, corten flat-bar balusters every 0.11 m, bottom rail at +0.10 m, corten top flat bar
    under an oak handrail, top +1.10 m (design values). beyond = drawn light, as standing behind the cut."""
    k = K
    fill = BEYOND_CORTEN if beyond else CORTEN
    line = BEYOND if beyond else INK
    oak = "DCC7AE" if beyond else OAK
    a, b = sorted((S.X(s0), S.X(s1)))
    y0 = S.Y(z)
    yb0, yb1 = y0 + 0.08 * k, y0 + 0.12 * k
    yt0, yt1 = y0 + 0.99 * k, y0 + 1.04 * k
    n_bal = int((b - a) / (0.11 * k))
    for i in range(1, n_bal):                                                          # balusters 12 x 40
        x = a + (b - a) * i / n_bal
        pg.line([(x, yb1), (x, yt0)], fill, 0.16, layer=layer, cap=0)
    pg.poly([[(a, yb0), (b, yb0), (b, yb1), (a, yb1)]], fill=fill, stroke=line, lw=0.05, layer=layer)
    n = max(1, int(math.ceil((b - a) / (1.5 * k))))
    for i in range(n + 1):
        x = a + (b - a) * i / n
        x = min(max(x, a + 0.03 * k), b - 0.03 * k)
        pg.poly([[(x - 0.03 * k, y0 - 0.22 * k), (x + 0.03 * k, y0 - 0.22 * k), (x + 0.03 * k, yt0),
                  (x - 0.03 * k, yt0)]], fill=fill, stroke=line, lw=0.06, layer=layer)    # post 60 x 15
        pg.poly([[(x - 0.06 * k, y0 - 0.24 * k), (x + 0.06 * k, y0 - 0.24 * k), (x + 0.06 * k, y0 - 0.02 * k),
                  (x - 0.06 * k, y0 - 0.02 * k)]], fill=None, stroke=line, lw=0.05, layer=layer)  # side plate
        for yy in (y0 - 0.07 * k, y0 - 0.19 * k):
            pg.circle(x, yy, 0.18, fill="D9D4CC" if not beyond else "EEEEEE", stroke=line, lw=0.03, layer=layer)
    pg.poly([[(a - 0.05 * k, yt0), (b + 0.05 * k, yt0), (b + 0.05 * k, yt1), (a - 0.05 * k, yt1)]], fill=fill,
            stroke=line, lw=0.05, layer=layer)                                         # top flat bar
    pg.poly([_rrect(a - 0.08 * k, yt1, b + 0.08 * k, y0 + 1.10 * k, 0.015 * k)], fill=oak, stroke=line, lw=0.07,
            layer=layer)                                                               # oak handrail
    pg.line([(a - 0.06 * k, y0 + 1.07 * k), (b + 0.06 * k, y0 + 1.07 * k)], "9C7448" if not beyond else "CDB89E",
            0.04, layer=layer)                                                         # grain line


def balcony(pg, S, b, people):
    """The balcony stands just beyond the cut (as in the reference's J-J'): light 'beyond' lines, drawn before the
    cut so the amphitheatre steps, the earth and the people on the lower walk lie over it. People on the balcony stand
    behind its near railing: drawn light, then the railing over them."""
    s0, s1, top, th = b["s0"], b["s1"], b["top"], b["thick"]
    for c in b["columns"]:
        g = S.surf(c)
        pg.poly([[S.P(c - 0.15, top - th), S.P(c + 0.15, top - th), S.P(c + 0.15, g), S.P(c - 0.15, g)]],
                fill=BEYOND_FILL, stroke=BEYOND, lw=0.12, layer="balcony (beyond)")
    pg.poly([[S.P(s0, top - 0.06), S.P(s1, top - 0.06), S.P(s1, top - th), S.P(s0, top - th)]], fill=BEYOND_FILL,
            stroke=BEYOND, lw=0.12, layer="balcony (beyond)")
    pg.poly([[S.P(s0, top), S.P(s1, top), S.P(s1, top - 0.06), S.P(s0, top - 0.06)]], fill="E9DCCB", stroke=BEYOND,
            lw=0.1, layer="balcony (beyond)")
    for s, kind, flip in people:
        X, Y = S.P(s, top)
        draw_asset(pg, FIGS[kind % len(FIGS)], X, Y, flip=flip, layer="people (beyond)", tone=BEYOND_FIG)
    railing_elevation(pg, S, s0, s1, top, beyond=True, layer="balcony (beyond)")


def pergola(pg, S, p):
    for s in p["posts"]:
        X, Y = S.P(s, S.surf(s))
        h = max(pl[2] for pl in p["plates"]) * K
        pg.poly([[(X - 0.6, Y), (X + 0.6, Y), (X + 0.6, Y + h), (X - 0.6, Y + h)]], fill="FFFFFF", stroke=INK, lw=0.25,
                layer="shading")
    for a, b, h in p["plates"]:
        z = S.surf(p["posts"][0]) + h
        pg.poly([[S.P(a, z), S.P(b, z), S.P(b, z + 0.1), S.P(a, z + 0.1)]], fill="F4F4F2", stroke=INK, lw=0.25,
                layer="shading")


def water_rings(S, z):
    """The water body at level z: the finished surface (strip included) clipped below z, closed along z."""
    V = S.V
    runs, cur = [], []
    for i, p in enumerate(V):
        below = p[1] < z - 1e-9
        if i > 0:
            q = V[i - 1]
            if (q[1] < z - 1e-9) != below:
                f = (z - q[1]) / (p[1] - q[1])
                c = (q[0] + f * (p[0] - q[0]), z)
                if below:
                    cur = [c]
                else:
                    cur.append(c)
                    runs.append(cur)
                    cur = []
        if below:
            if not cur:
                cur = [(p[0], z)]
            cur.append(p)
    if cur:
        cur.append((V[-1][0], z))
        runs.append(cur)
    return [[S.P(s, zz) for s, zz in r] for r in runs if len(r) >= 3]


def water(pg, S, z, alpha=0.62):
    """Water at level z: light blue, see-through (stems and the bed show under it), hatch, firm surface line."""
    for ring in water_rings(S, z):
        pg.poly([ring], fill=WATER, stroke=None, layer="water", alpha=alpha)
        ys = [p[1] for p in ring]
        y = min(ys) + 0.7
        while y < max(ys) - 0.3:                                   # horizontal hatch inside the water
            xs = []
            for k_ in range(len(ring)):
                p, q = ring[k_], ring[(k_ + 1) % len(ring)]
                if (p[1] - y) * (q[1] - y) < 0:
                    xs.append(p[0] + (y - p[1]) * (q[0] - p[0]) / (q[1] - p[1]))
            xs.sort()
            for m in range(0, len(xs) - 1, 2):
                if xs[m + 1] - xs[m] > 1.0:
                    pg.line([(xs[m] + 0.4, y), (xs[m + 1] - 0.4, y)], WATER_LINE, 0.1, layer="water")
            y += 0.7
        top = [p for p in ring if abs(p[1] - max(ys)) < 1e-6]
        if len(top) >= 2:
            x0, x1 = min(p[0] for p in top), max(p[0] for p in top)
            pg.line([(x0, max(ys)), (x1, max(ys))], FLOOD, 0.3, layer="water")
            r = rng("ripple", round(x0, 1))
            x = x0 + 1.0
            while x < x1 - 2.0:                                     # small ripples under the surface
                L = 0.8 + r.random() * 1.6
                pg.line([(x, max(ys) - 0.45 - r.random() * 0.5), (x + L, max(ys) - 0.45 - r.random() * 0.5)],
                        FLOOD, 0.08, layer="water")
                x += L + 1.0 + r.random() * 2.0


def level_line(pg, S, z, label, dash, colour=FLOOD):
    """A water level drawn only where it stands above the surface, with its sign and text at the right end."""
    s_l, s_r = S.d["s_from"], S.d["s_to"]
    n = int(abs(s_r - s_l) / 0.1)
    run = []
    runs = []
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
    pg.line([(X - 0.8, Y - 0.6), (X + 0.8, Y - 0.6)], colour, 0.2, layer="levels")
    pg.text(label, X - 2.5, Y + 0.6, 2.0, colour, align="R", layer="levels")


# ================================================================ VEGETATION (procedural, high detail; page mm, y up)
# Every plant is built from many small vector pieces: tapered branches and twigs, single leaves (pointed, lobed or
# narrow, each with a midrib on the larger ones), grass and reed blades as tapered curved strips, seed heads of many
# grains. Light comes from the upper left: leaves there are lighter, leaves inside and lower right darker. Colours are
# the reference's light greens. A plant is the same on every run (seeded by its position).
LEAF_TONES = ["E4EDC6", "D3E2A6", "C1D48C", "ABC173", "93AA5E", "7B9450"]   # light .. deep
LEAF_EDGE = "6E8646"
BARK = ("C9CAB8", "A3A690", "6F735F")                                          # light, mid, dark bark
GRASS_TONES = ["B9CC83", "A2B96C", "8BA35A", "C9D99A", "748D49"]
REED_TONES = ["B9B98E", "A6A97A", "C7C59B", "8F9468"]
SEED_TONES = ["C2A779", "AE9165", "D4BD92"]
LAV_TONES = ["8E74B5", "A48CC6", "7A62A0", "B9A6D6"]
STRAW = ["D3C59C", "C2B48A", "DDD2AE", "AE9F78"]
# How the plants look in each season (general habit of the species: Platanus orientalis, Tamarix and Vitex are
# deciduous, Lavandula stoechas is evergreen; reeds cut back after October as in concept s.10.1). Drawing values.
SEASON_LOOK = {
    "winter": dict(tree_leaf=0.0, tree_tones=LEAF_TONES, seed_balls=True, shrub_leaf=0.10,
                   shrub_tones=["C9C3A0", "B7B08B", "A39C78"], grass_tones=GRASS_TONES, reed_h=0.32, reed_tones=STRAW,
                   reed_leaf=0.0, plume=0.0, iris_h=0.35, iris_flower=0.0, iris_tones=["7F8F5A", "8E9A66", "9AA372"],
                   lav_spikes=0),
    "spring": dict(tree_leaf=0.80, tree_tones=["EEF4CF", "E0EDB2", "CFE29A", "BCD585", "A6C46F", "8FAF5C"],
                   seed_balls=False, shrub_leaf=0.85, shrub_tones=["EEF4CF", "DCEBAE", "C8DD93", "B2CE7B", "98B964"],
                   grass_tones=["C4D88A", "ADC774", "96B060", "D3E4A3", "7F9B4E"], reed_h=0.62,
                   reed_tones=["B4C98A", "A3BB78", "C3D59C", "8FAA66"], reed_leaf=0.8, plume=0.0, iris_h=1.0,
                   iris_flower=0.85, iris_tones=["6E8F4A", "7FA057", "5F7E40", "8FB066"], lav_spikes=7),
    "summer": dict(tree_leaf=1.0, tree_tones=LEAF_TONES, seed_balls=False, shrub_leaf=1.0, shrub_tones=LEAF_TONES,
                   grass_tones=["D8CC9A", "C9BB84", "A9B573", "C2C78E", "93A363"], reed_h=1.0, reed_tones=REED_TONES,
                   reed_leaf=1.0, plume=0.35, iris_h=1.0, iris_flower=0.0,
                   iris_tones=["6E8F4A", "7FA057", "5F7E40", "8FB066"], lav_spikes=3),
    "autumn": dict(tree_leaf=0.70, tree_tones=["F1E2B0", "E6CF8C", "D9B86C", "C99E55", "B08445", "8E6B3A"],
                   seed_balls=True, shrub_leaf=0.65, shrub_tones=["E8D9A2", "D6C083", "C2A86A", "A8A066", "8E9458"],
                   grass_tones=["C9C08C", "B4B47E", "9FAA6C", "D1C79A", "8C9B5E"], reed_h=1.0,
                   reed_tones=["D3C08A", "C2AE78", "B49F6C", "A8A27A"], reed_leaf=0.7, plume=0.95, iris_h=0.85,
                   iris_flower=0.0, iris_tones=["A3A266", "B7AE70", "8E9A5E", "C2B478"], lav_spikes=0),
}
SEA = dict(SEASON_LOOK["summer"])


def _bez(p0, p1, p2, n):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / float(n) for i in range(n + 1)]]


def _strip(path, w0, w1, tip=True):
    """A tapered strip along a path (blade, stem, branch): width w0 at the base to w1 (0 = pointed) at the end."""
    L, R = [], []
    n = len(path)
    for i, p in enumerate(path):
        a = path[min(i + 1, n - 1)]
        b = path[max(i - 1, 0)]
        dx, dy = a[0] - b[0], a[1] - b[1]
        d = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / d, dx / d
        t = i / float(n - 1)
        w = (w0 + (w1 - w0) * t) / 2.0
        L.append((p[0] + nx * w, p[1] + ny * w))
        R.append((p[0] - nx * w, p[1] - ny * w))
    return L + R[::-1]


def _leaf(cx, cy, size, ang, kind, r):
    """One leaf, size = length in mm. kind 0 pointed oval, 1 three-lobed (plane), 2 narrow (willow-like)."""
    ca, sa = math.cos(ang), math.sin(ang)
    pts = []
    if kind == 1:
        prof = [(0.0, 0.0), (0.18, 0.22), (0.30, 0.42), (0.42, 0.30), (0.55, 0.38), (0.72, 0.20), (1.0, 0.0)]
    elif kind == 2:
        prof = [(0.0, 0.0), (0.2, 0.09), (0.5, 0.12), (0.8, 0.07), (1.0, 0.0)]
    else:
        prof = [(0.0, 0.0), (0.15, 0.20), (0.45, 0.28), (0.75, 0.18), (1.0, 0.0)]
    wob = 0.85 + 0.3 * r.random()
    side = [(u * size, v * size * wob) for u, v in prof]
    for u, v in side + [(u, -v * (0.9 + 0.2 * r.random())) for u, v in side[-2:0:-1]]:
        pts.append((cx + u * ca - v * sa, cy + u * sa + v * ca))
    return pts


def _tone(lit, r, tones=LEAF_TONES):
    k = (1.0 - lit) * (len(tones) - 1) + (r.random() - 0.5) * 1.6
    return tones[max(0, min(len(tones) - 1, int(round(k))))]


def veg_tree(pg, X, Y, h, w, seed, flip=False, leaf_mm=None, layer="trees"):
    """Broadleaf tree (plane-tree habit): tapered trunk, 4 orders of branches, about 2,000-3,000 leaves on the twig
    tips, back leaves darker, front leaves lighter and sparser so the branch structure reads through the crown."""
    r = rng("tree", seed)
    fx = -1.0 if flip else 1.0
    lo = 0.36 * h
    branches, tips = [], []

    cx, cy = X, Y + lo + (h - lo) * 0.52
    ax, ay = w / 2.0, (h - lo) * 0.52

    def inside(px, py):
        return ((px - cx) / ax) ** 2 + ((py - cy) / ay) ** 2

    def grow(x, y, ang, length, width, depth):
        n = 5
        bend = (r.random() - 0.5) * 0.35
        ex, ey = x + math.cos(ang) * length, y + math.sin(ang) * length
        for _ in range(12):                                     # twigs end inside the crown, never poke out
            if inside(ex, ey) <= 0.78:
                break
            length *= 0.85
            ex, ey = x + math.cos(ang) * length, y + math.sin(ang) * length
        mx = (x + ex) / 2 + math.cos(ang + 1.57) * length * bend * 0.25
        my = (y + ey) / 2 + math.sin(ang + 1.57) * length * bend * 0.25
        path = _bez((x, y), (mx, my), (ex, ey), n)
        branches.append((path, width, width * 0.62, depth))
        if depth >= 3:
            for q in path[2:]:
                tips.append((q[0], q[1], depth - 1))
        if depth >= 5 or length < 0.025 * h:
            tips.append((ex, ey, depth))
            return
        k = 2 + (1 if r.random() < 0.55 else 0)
        for i in range(k):
            sp = (0.42 + 0.25 * r.random()) * (1 if i % 2 else -1) * (1.0 if i < 2 else 0.4)
            na = ang + sp + (r.random() - 0.5) * 0.25
            na = max(0.15, min(math.pi - 0.15, na))           # nothing grows downwards
            grow(ex, ey, na, length * (0.68 + 0.14 * r.random()), width * 0.62, depth + 1)
        tips.append((ex, ey, depth))

    # trunk to the crown base, then the main limbs
    tw = max(1.1, 0.04 * w)
    trunk = _bez((X, Y), (X + fx * 0.04 * w, Y + lo * 0.5), (X - fx * 0.02 * w, Y + lo), 8)
    branches.append((trunk, tw, tw * 0.78, 0))
    for i in range(5):
        a = math.pi / 2 + (i - 2) * 0.30 + (r.random() - 0.5) * 0.15
        grow(X - fx * 0.02 * w, Y + lo, a, (h - lo) * (0.30 + 0.10 * r.random()), tw * 0.70, 1)
    # leaves: around every tip and along the outer branches, inside the crown envelope (an upright ellipse)
    size = leaf_mm or max(0.5, 0.022 * h)
    leaves = []
    for (tx, ty, d) in tips:
        n = 22 if d >= 4 else (10 if d >= 3 else 4)
        for _ in range(n):
            px = tx + r.gauss(0, size * 2.2)
            py = ty + r.gauss(0, size * 1.8) + size * 0.5
            e = inside(px, py)
            if e > 1.0 + 0.08 * r.random():
                continue
            depth = r.random()                                  # 0 = front, 1 = back
            if r.random() > SEA["tree_leaf"]:
                continue
            lit = 0.5 + 0.35 * (-(px - cx) * fx / ax + (py - cy) / ay) / 2 - 0.25 * depth + 0.4 * (1 - e) * 0
            leaves.append((depth, px, py, lit))
    leaves.sort(key=lambda q: -q[0])
    back = [q for q in leaves if q[0] > 0.45]
    front = [q for q in leaves if q[0] <= 0.45 and r.random() < 0.8]

    def draw_leaves(lst, al, dark):
        for depth, px, py, lit in lst:
            ang = r.random() * 6.283
            sz = size * (0.75 + 0.5 * r.random())
            kind = 1 if r.random() < 0.35 else 0
            col = _tone(max(0.0, min(1.0, lit - dark)), r, SEA["tree_tones"])
            leaf = _leaf(px, py, sz, ang, kind, r)
            edge = LEAF_EDGE if sz > 2.2 and r.random() < 0.5 else None
            pg.poly([leaf], fill=col, stroke=edge, lw=0.04, layer=layer, alpha=al)
            if sz > 2.6 and r.random() < 0.6:                  # midrib
                pg.line([(px, py), (px + math.cos(ang) * sz * 0.85, py + math.sin(ang) * sz * 0.85)], LEAF_EDGE, 0.04,
                        layer=layer)

    draw_leaves(back, 0.88, 0.25)
    for path, w0, w1, d in sorted(branches, key=lambda b: b[3]):
        ring = _strip(path, w0, w1)
        pg.poly([ring], fill=BARK[0], stroke=BARK[2], lw=0.06 if d < 2 else 0.04, layer=layer)
        if d <= 1:                                              # bark streaks on trunk and main limbs
            for k_ in range(3):
                off = (k_ - 1) * w0 * 0.22
                pg.line([(p[0] + off, p[1]) for p in path[1:-1]], BARK[1], 0.05, layer=layer)
    draw_leaves(front, 0.82, -0.05)
    if SEA["seed_balls"]:                                       # plane seed balls hang on through winter
        rb_ = rng("balls", seed)
        for (tx, ty, d) in tips:
            if d >= 4 and rb_.random() < 0.10:
                L = size * (1.2 + rb_.random())
                pg.line([(tx, ty), (tx + rb_.gauss(0, 0.3), ty - L)], BARK[2], 0.05, layer=layer)
                pg.circle(tx, ty - L - 0.45, 0.45, fill="8A6F4D", stroke="5E4A33", lw=0.04, layer=layer)


def veg_shrub(pg, X, Y, h, w, seed, kind=0, layer="planting"):
    """Shrub: 5-9 woody stems fanning from the base, 300-700 small leaves on a domed crown (kind 2 = narrow leaves,
    tamarisk / vitex habit)."""
    r = rng("shrub", seed)
    stems = []
    ns = 5 + int(r.random() * 5)
    for i in range(ns):
        a = math.pi / 2 + (i - (ns - 1) / 2.0) * (1.1 / ns) + (r.random() - 0.5) * 0.15
        L = h * (0.65 + 0.3 * r.random())
        end = (X + math.cos(a) * L * 0.9 * (w / h), Y + math.sin(a) * L)
        mid = (X + (end[0] - X) * 0.4, Y + (end[1] - Y) * 0.55)
        path = _bez((X + (r.random() - 0.5) * w * 0.08, Y), mid, end, 6)
        stems.append(path)
    size = max(0.9, 0.11 * h) if kind != 2 else max(1.1, 0.13 * h)
    n = int(140 + 5.5 * w * h / (size * size) * 0.5)
    n = min(n, 900)
    cx, cy = X, Y + h * 0.55
    leaves = []
    for _ in range(n):
        t = r.random()
        st = stems[int(r.random() * len(stems))]
        j = int((0.35 + 0.65 * t) * (len(st) - 1))
        px = st[j][0] + r.gauss(0, size * 1.3)
        py = st[j][1] + r.gauss(0, size * 1.1)
        if py < Y + h * 0.12 or r.random() > SEA["shrub_leaf"]:
            continue
        lit = 0.55 + 0.35 * (-(px - cx) / (w / 2) + (py - cy) / (h / 2)) / 2
        leaves.append((r.random(), px, py, lit))
    leaves.sort(key=lambda q: -q[0])
    for path in stems:
        pg.poly([_strip(path, max(0.18, 0.012 * w), 0.06)], fill=BARK[1], stroke=None, layer=layer)
    for depth, px, py, lit in leaves:
        lk = 2 if kind == 2 else (1 if r.random() < 0.2 else 0)
        sz = size * (0.7 + 0.6 * r.random())
        pg.poly([_leaf(px, py, sz, r.random() * 6.283, lk, r)], fill=_tone(max(0, min(1, lit - 0.3 * depth)), r, SEA["shrub_tones"]),
                stroke=LEAF_EDGE if r.random() < 0.25 else None, lw=0.03, layer=layer, alpha=0.9)


def veg_blade(pg, X, Y, length, ang, width, curl, col, layer="planting"):
    ex, ey = X + math.cos(ang) * length, Y + math.sin(ang) * length
    mx = X + math.cos(ang) * length * 0.5 + math.cos(ang - 1.57) * curl * length
    my = Y + math.sin(ang) * length * 0.5 + math.sin(ang - 1.57) * curl * length
    pg.poly([_strip(_bez((X, Y), (mx, my), (ex, ey), 6), width, 0.0)], fill=col, stroke=None, layer=layer)


def shrub(pg, S, s, h, w):
    X, Y = S.P(s, S.surf(s))
    veg_shrub(pg, X, Y, h * K, w * K, (S.d["key"], round(s, 2)), kind=2 if (h <= 1.6 and s % 2 > 1) else 0)


def tufts(pg, S, s0, s1, h=0.35, colour=None, step=0.35, seed="g"):
    """Meadow grass: dense tapered blades in five greens, clumps of 9-15 blades, short blades filling between."""
    r = rng("tuft", seed, round(s0, 2))
    n = max(1, int(abs(s1 - s0) / (step * 0.55)))
    for i in range(n):
        s = s0 + (s1 - s0) * (i + 0.5 + (r.random() - 0.5) * 0.7) / n
        X, Y = S.P(s, S.surf(s))
        for j in range(9 + int(r.random() * 7)):
            L = h * K * (0.45 + 0.75 * r.random())
            a = math.pi / 2 + (r.random() - 0.5) * 1.3
            veg_blade(pg, X + (r.random() - 0.5) * 1.2, Y, L, a, 0.28 + 0.2 * r.random(), (r.random() - 0.5) * 0.25,
                      SEA["grass_tones"][int(r.random() * len(SEA["grass_tones"]))])


def lavender(pg, S, s0, s1):
    """Lavandula stoechas: grey-green needle leaves in a low mound, flower spikes of many small purple florets."""
    r = rng("lav", round(s0, 2))
    n = max(1, int(abs(s1 - s0) / 0.42))
    for i in range(n):
        s = s0 + (s1 - s0) * (i + 0.5) / n
        X, Y = S.P(s, S.surf(s))
        for j in range(26):
            a = math.pi / 2 + (r.random() - 0.5) * 2.0
            veg_blade(pg, X + (r.random() - 0.5) * 2, Y, (0.18 + 0.2 * r.random()) * K, a, 0.22,
                      (r.random() - 0.5) * 0.2, ["A7B596", "93A383", "BCC7AE"][int(r.random() * 3)])
        for j in range(SEA["lav_spikes"]):
            a = math.pi / 2 + (r.random() - 0.5) * 0.9
            L = (0.32 + 0.16 * r.random()) * K
            ex, ey = X + math.cos(a) * L, Y + math.sin(a) * L
            pg.line([(X, Y), (ex, ey)], "8C9B78", 0.07, layer="planting")
            for k_ in range(9):
                t = 0.72 + 0.28 * k_ / 8.0
                fx_, fy_ = X + math.cos(a) * L * t, Y + math.sin(a) * L * t
                pg.poly([_leaf(fx_ - 0.25, fy_, 0.55, a + (0.6 if k_ % 2 else -0.6), 0, r)],
                        fill=LAV_TONES[int(r.random() * len(LAV_TONES))], stroke=None, layer="planting")
            pg.poly([_leaf(ex, ey, 0.9, a + 0.5, 0, r), _leaf(ex, ey, 0.9, a - 0.5, 0, r)][:1],
                    fill="C7B6E0", stroke=None, layer="planting")


def reeds(pg, S, s0, s1, h):
    """Phragmites: tapered culms, 5-7 long arching leaves each, plumes of 40-60 grains hanging to one side."""
    r = rng("reed", round(s0, 2))
    n = max(2, int(abs(s1 - s0) / 0.2))
    for i in range(n):
        s = s0 + (s1 - s0) * (i + r.random()) / n
        X, Y = S.P(s, S.surf(s))
        H = h * SEA["reed_h"] * (0.7 + 0.35 * r.random()) * K
        lean = (r.random() - 0.5) * 0.18
        top = (X + lean * H, Y + H)
        culm = _bez((X, Y), (X + lean * H * 0.3, Y + H * 0.5), top, 8)
        pg.poly([_strip(culm, 0.38, 0.12)], fill=SEA["reed_tones"][int(r.random() * 4)], stroke=None,
                layer="planting")
        if SEA["reed_h"] < 0.4:                                 # cut stubble: a flat cut top
            pg.line([(top[0] - 0.25, top[1]), (top[0] + 0.25, top[1])], STRAW[3], 0.08, layer="planting")
        for j in range(5 + int(r.random() * 3)):
            if r.random() > SEA["reed_leaf"]:
                continue
            t = 0.12 + 0.7 * j / 7.0
            p = culm[int(t * (len(culm) - 1))]
            side = 1 if (j + i) % 2 else -1
            a = math.pi / 2 - side * (0.5 + 0.5 * r.random())
            veg_blade(pg, p[0], p[1], (0.35 + 0.25 * r.random()) * K, a, 0.55, side * (0.18 + 0.12 * r.random()),
                      SEA["reed_tones"][int(r.random() * 4)] if SEA["plume"] > 0.9 else
                      GRASS_TONES[int(r.random() * len(GRASS_TONES))])
        if r.random() < SEA["plume"]:                           # plume
            side = 1 if r.random() < 0.5 else -1
            for k_ in range(40 + int(r.random() * 20)):
                t = r.random()
                gx = top[0] + side * (0.15 + 1.6 * t) + r.gauss(0, 0.45)
                gy = top[1] - 0.2 - 3.2 * t * t - r.random() * 1.2
                pg.poly([_leaf(gx, gy, 0.55 + 0.3 * r.random(), -math.pi / 2 + side * 0.5 + r.gauss(0, 0.3), 2, r)],
                        fill=SEED_TONES[int(r.random() * 3)], stroke=None, layer="planting")


def iris(pg, S, s0, s1):
    """Iris pseudacorus: fans of 7-10 sword leaves, yellow flowers of three falls and three standards."""
    r = rng("iris", round(s0, 2))
    n = max(1, int(abs(s1 - s0) / 0.4))
    for i in range(n):
        s = s0 + (s1 - s0) * (i + 0.5) / n
        X, Y = S.P(s, S.surf(s))
        for j in range(7 + int(r.random() * 4)):
            a = math.pi / 2 + (j - 4) * 0.11 + (r.random() - 0.5) * 0.08
            veg_blade(pg, X + (j - 4) * 0.25, Y, SEA["iris_h"] * (0.55 + 0.35 * r.random()) * K, a, 0.75,
                      (r.random() - 0.5) * 0.08, SEA["iris_tones"][int(r.random() * len(SEA["iris_tones"]))])
        if r.random() < SEA["iris_flower"]:
            fx_, fy_ = X + (r.random() - 0.5) * 2.5, Y + (0.75 + 0.2 * r.random()) * K
            pg.line([(X, Y), (fx_, fy_)], "6E8F4A", 0.12, layer="planting")
            for k_ in range(3):
                pg.poly([_leaf(fx_, fy_, 1.5, -0.5 - k_ * 1.05 + 0.2, 0, r)], fill="E2C246", stroke="B8952A", lw=0.03,
                        layer="planting")
                pg.poly([_leaf(fx_, fy_, 1.0, 1.2 + k_ * 0.35, 0, r)], fill="F0D66A", stroke=None, layer="planting")


FIGS = ["I_walker_flood_wall", "I_woman_with_bag", "J_woman_walking", "I_photographer", "J_man_and_child",
        "J_photographer_balcony", "J_woman_on_steps", "I_child_on_sand", "J_person_seated", "J_person_sitting",
        "J_cyclist_cheering", "I_cyclist_waving"]          # traced from the reference (J_person_seated = the sitting
#                                                   figure without its chair, anchored at the seat: sits on an edge)


def figure(pg, S, s, kind, flip, z=None):
    g = S.surf(s) if z is None else z
    X, Y = S.P(s, g)
    draw_asset(pg, FIGS[kind % len(FIGS)], X, Y, flip=flip, layer="people", tone=FIG)


def bike(pg, S, s, flip):
    g = S.surf(s)
    X, Y = S.P(s, g)
    k = K
    sg = -1.0 if flip else 1.0
    R = 0.34 * k
    for dx in (-0.55, 0.55):
        pg.circle(X + sg * dx * k, Y + R, R, fill=None, stroke=FIG, lw=0.3, layer="people")
    pg.line([(X - sg * 0.55 * k, Y + R), (X, Y + R), (X + sg * 0.35 * k, Y + 0.85 * k), (X + sg * 0.55 * k, Y + R)],
            FIG, 0.35, layer="people")
    pg.line([(X - sg * 0.1 * k, Y + 0.8 * k), (X, Y + R)], FIG, 0.35, layer="people")
    body = [(-0.18, 0.80), (0.02, 0.80), (0.30, 1.20), (0.40, 1.48), (0.30, 1.52), (0.20, 1.40), (0.36, 0.90),
            (0.10, 0.62), (0.0, 0.40), (-0.06, 0.42), (0.04, 0.68), (-0.10, 0.95), (0.02, 1.45), (-0.10, 1.45)]
    pg.poly([[(X + sg * bx * k, Y + by * k) for bx, by in body]], fill=FIG, stroke=None, layer="people")
    pg.circle(X + sg * 0.30 * k, Y + 1.66 * k, 0.105 * k, fill=FIG, layer="people")




def existing_ground(pg, S):
    """The survey ground, dashed, where the design departs from it by more than 5 cm."""
    s_l, s_r = S.d["s_from"], S.d["s_to"]
    n = int(abs(s_r - s_l) / 0.25)
    run, runs = [], []
    for i in range(n + 1):
        s = s_l + (s_r - s_l) * i / n
        if abs(S.ex(s) - S.surf(s)) > 0.05 and min(S.d["s_from"], S.d["s_to"]) <= s:
            run.append(S.P(s, S.ex(s)))
        elif run:
            runs.append(run)
            run = []
    if run:
        runs.append(run)
    for r in runs:
        if len(r) >= 2:
            pg.line(r, INK2, 0.18, dash=[1.2, 0.8], layer="existing ground")


def survey_marks(pg, S, notes):
    for s, what, z in SURVEY_MARKS:
        if not (S.lo <= s <= S.hi):
            continue
        if z is None:
            X, Y = S.P(s, S.ex(s))
            pg.poly([[(X - 0.9, Y - 1.6), (X + 0.9, Y - 1.6), (X, Y)]], fill=GREY, stroke=None, layer="survey")
            pg.text("%s %.2f" % (what, s), X, Y - 3.6, 1.6, GREY, align="C", layer="survey")
        else:
            X, Y = S.P(s, z)
            pg.line([(X - 0.8, Y), (X + 0.8, Y)], GREY, 0.15, layer="survey")
            pg.line([(X, Y - 0.8), (X, Y + 0.8)], GREY, 0.15, layer="survey")
            pg.text("%.2f" % z, X + 1.0, Y + 0.6, 1.6, GREY, layer="survey")


# ================================================================ callouts, dimensions, band
def place_labels(S, items, size):
    """Rows for the callouts: no overlaps, no leader through a label (greedy, left to right)."""
    placed = []
    for x, y_anchor, txt in sorted(items, key=lambda t: t[0]):
        lines = wrap(txt, 18)
        w = max(text_w(l, size) for l in lines) + 2.0
        for row in range(8):
            x0, x1 = x - w / 2, x + w / 2
            ok = True
            for p in placed:
                if p["row"] == row and not (x1 < p["x0"] or x0 > p["x1"]):
                    ok = False
                if p["row"] > row and x0 - 0.8 <= p["x"] <= x1 + 0.8:
                    ok = False
                if p["row"] < row and p["x0"] - 0.8 <= x <= p["x1"] + 0.8:
                    ok = False
            if ok:
                placed.append(dict(x=x, y=y_anchor, x0=x0, x1=x1, row=row, lines=lines))
                break
    return placed


def callouts(pg, S, placed, ybase, size):
    gap = size * 2 * 1.25 + 3.0
    for p in placed:
        yl = ybase + p["row"] * gap
        for i, l in enumerate(p["lines"]):
            pg.text(l, p["x"], yl + (len(p["lines"]) - 1 - i) * size * 1.2, size, INK, align="C", layer="callouts")
        pg.line([(p["x"], yl - 1.2), (p["x"], p["y"])], INK2, 0.1, dash=[0.5, 0.5], layer="callouts")
        pg.circle(p["x"], p["y"], 0.45, fill=INK, layer="callouts")


def dims(pg, S, y):
    """Bottom chain: the design widths in mm (red), ticks at every boundary."""
    bounds = []
    for sa, sb, z, mat, lab in S.flats:
        bounds += [sa, sb]
    ra, rb = S.d["regrade"]
    bounds += [rb, STRIP[0], STRIP[1]]
    bounds = sorted(set(round(b, 3) for b in bounds if S.lo <= b <= S.hi), key=lambda b: S.X(b))
    xs = [S.X(b) for b in bounds]
    pg.line([(xs[0], y), (xs[-1], y)], DIM, 0.12, layer="dimensions")
    for X in xs:
        pg.line([(X - 0.8, y - 0.8), (X + 0.8, y + 0.8)], DIM, 0.2, layer="dimensions")
        pg.line([(X, y - 1.2), (X, y + 1.2)], DIM, 0.1, layer="dimensions")
    for i in range(len(bounds) - 1):
        mm = abs(bounds[i + 1] - bounds[i]) * 1000.0
        pg.text("%d" % round(mm), (xs[i] + xs[i + 1]) / 2, y + 1.0, 1.9, DIM, align="C", layer="dimensions")


def vdims(pg, S, levels, x):
    """Right chain: level differences in mm, thin red lines from each level, absolute levels beside the ticks."""
    lv = sorted(set(round(z, 3) for z, _ in levels))
    names = dict((round(z, 3), n) for z, n in levels)
    ys = [S.Y(z) for z in lv]
    pg.line([(x, ys[0]), (x, ys[-1])], DIM, 0.12, layer="dimensions")
    for z, Y in zip(lv, ys):
        pg.line([(x - 6.0, Y), (x + 1.2, Y)], DIM, 0.08, layer="dimensions")
        pg.line([(x - 0.8, Y - 0.8), (x + 0.8, Y + 0.8)], DIM, 0.2, layer="dimensions")
        pg.text("%+.2f %s" % (z, names[z]), x + 12.0, Y - 0.6, 1.6, GREY, layer="dimensions")
    for i in range(len(lv) - 1):
        pg.text("%d" % round((lv[i + 1] - lv[i]) * 1000), x + 1.5, (ys[i] + ys[i + 1]) / 2 - 0.7, 1.9, DIM,
                layer="dimensions")


def swatch(pg, x0, x1, y, h, mat, seed):
    ring = [(x0, y), (x1, y), (x1, y + h), (x0, y + h)]
    r = rng("sw", seed, round(x0, 2))
    base = {"veg": "6F8F45", "asphalt": ASPHALT, "concrete": "C9C8C3", "deck": "A97E52", "lavender": "8C7AA8",
            "gravel": "B9B1A2", "water": "9CC7DE"}.get(mat, "CCCCCC")
    pg.poly([ring], fill=base, stroke=None, layer="band")
    area = (x1 - x0) * h
    if mat in ("veg", "lavender"):
        for _ in range(int(area * 1.2)):
            X, Y = x0 + r.random() * (x1 - x0), y + r.random() * h
            col = ["4E6B30", "8DAE5E", "B6CF86", "3E5626"][int(r.random() * 4)]
            if mat == "lavender" and r.random() < 0.35:
                col = "B9A3D8"
            R = 0.25 + r.random() * 0.45
            pg.poly([_tree_blob(X, Y, R, r.random, 6)], fill=col, stroke=None, layer="band")
    elif mat == "deck":
        yy = y + 0.9
        while yy < y + h:
            pg.line([(x0, yy), (x1, yy)], "7E5A38", 0.15, layer="band")
            yy += 1.8
        for _ in range(int(area * 0.15)):
            X, Y = x0 + r.random() * (x1 - x0), y + r.random() * h
            pg.line([(X, Y), (min(x1, X + 3 + r.random() * 6), Y)], "8E6A45", 0.08, layer="band")
    elif mat in ("asphalt", "concrete", "gravel"):
        cols = {"asphalt": ["7E3029", "C46A5B", "93413A"], "concrete": ["AFAEA8", "DDDCD7", "9C9B95"],
                "gravel": ["8E8573", "D2CBBE", "A49A86"]}[mat]
        for _ in range(int(area * (2.5 if mat == "gravel" else 3.0))):
            X, Y = x0 + r.random() * (x1 - x0), y + r.random() * h
            R = 0.12 + r.random() * (0.5 if mat == "gravel" else 0.18)
            pg.poly([_tree_blob(X, Y, R, r.random, 5)], fill=cols[int(r.random() * 3)], stroke=None, layer="band")
    elif mat == "water":
        yy = y + 0.8
        while yy < y + h:
            pg.line([(x0, yy), (x1, yy)], "6FA7C8", 0.12, layer="band")
            yy += 1.4


def band(pg, S, y, h=9.0):
    items = [(sa, sb, mat, lab) for sa, sb, z, mat, lab in S.flats] + list(S.d["band_more"])
    ra, rb = S.d["regrade"]
    items.append((ra, rb, "gravel", "River gravel"))
    items.sort(key=lambda t: S.X(t[0]) + S.X(t[1]))
    merged = []
    for a, b, mat, lab in items:                               # neighbours with the same label become one swatch
        if merged and merged[-1][3] == lab and abs(S.X(merged[-1][1]) - S.X(a)) < 0.5:
            merged[-1] = (merged[-1][0], b, mat, lab)
        else:
            merged.append((a, b, mat, lab))
    for a, b, mat, lab in merged:
        x0, x1 = sorted((S.X(a), S.X(b)))
        swatch(pg, x0, x1, y, h, mat, S.d["key"])
        for i, l in enumerate(wrap(lab, max(8, int((x1 - x0) / 1.4)))):
            pg.text(l, (x0 + x1) / 2, y - 3.6 - i * 2.6, 2.0, INK2, align="C", layer="band")


# ================================================================ one section
def draw_section(pg, S, x_left, y_top, notes, sea):
    d = S.d
    size = 2.3
    # vertical extents
    tops = [S.surf(t[0]) + t[2] for t in d["trees"]] + [DRY + 1.1]
    if d.get("pergola"):
        tops.append(DRY + max(p[2] for p in d["pergola"]["plates"]) + 0.1)
    z_top = max(tops)
    items = []
    for s, z, txt in d["callouts"]:
        items.append((s, z, txt))
    S.X0 = x_left
    # labels first (rows), positions in page x need X0 only
    tmp = [(S.X(s), 0.0, txt) for s, z, txt in items]
    placed = place_labels(S, tmp, size)
    rows = max(p["row"] for p in placed) + 1
    gap = size * 2 * 1.25 + 3.0
    title_h = 16.0
    label_h = rows * gap + 4.0
    S.Y0 = y_top - title_h - label_h - (z_top - S.zb) * K - 6.0
    # anchors in page y
    by_x = {}
    for s, z, txt in items:
        by_x[round(S.X(s), 3)] = (s, z)
    for p in placed:
        s, z = by_x[round(p["x"], 3)]
        if z is None:
            z = S.surf(s) + 0.02
        p["y"] = S.Y(z)
    # title
    pg.text(d["title"] + "  " + d["side"], x_left, y_top - 6.0, 5.0, INK, bold=True, layer="title")
    pg.text("SCALE 1:%.0f" % SCALE, x_left, y_top - 11.5, 3.6, INK, layer="title")
    pg.text("S4 · s %.0f-%.0f m · %s" % (d["s_from"], d["s_to"], d["look"]), x_left + 34.0, y_top - 11.5, 2.0,
            INK2, layer="title")              # board v1.8: "ground: survey, built: design" is in the notes line
    # back to front
    for s, r_, h, kind in d["trees"]:
        g = S.surf(s)
        if g < Q500 - 1e-6:
            notes.append("Section %s: tree at s %.1f skipped, it would stand below the Q500 line." % (d["key"], s))
            continue
        X, Y = S.P(s, g)
        veg_tree(pg, X, Y, h * K, 2 * r_ * K, (d["key"], round(s, 2)), flip=(S.dir < 0))
    people = list(sea["people"].get(d["key"], []))
    bal = d.get("balcony")
    on_bal = []
    if bal:
        for p in people:
            if p[1] == 3 and min(bal["s0"], bal["s1"]) <= p[0] <= max(bal["s0"], bal["s1"]):
                on_bal.append((p[0], 5, p[2]))
        people = [p for p in people if not (p[1] == 3 and min(bal["s0"], bal["s1"]) <= p[0] <= max(bal["s0"], bal["s1"]))]
    if d.get("pergola"):
        pergola(pg, S, d["pergola"])
    if bal:
        balcony(pg, S, bal, on_bal)
    level_line(pg, S, Q500, "Q500 %+.2f (calculated on this cut)" % Q500, [2.0, 1.0])
    level_line(pg, S, Q100, "Q100 %+.2f (calculated on this cut)" % Q100, [0.8, 0.8])
    filled = [w for w in sea["water"] if w[1]]
    for z, fill_, lab, dash in sea["water"]:
        if not fill_:
            level_line(pg, S, z, lab % z, dash, colour=WATER_LINE)
    poche(pg, S)
    soft_ground(pg, S)
    walls_and_slabs(pg, S)
    existing_ground(pg, S)
    survey_marks(pg, S, notes)
    for a, b in d["grass"]:
        tufts(pg, S, a, b)
    for a, b in d["lavender"]:
        lavender(pg, S, a, b)
    for s, h, w in d["shrubs"]:
        shrub(pg, S, s, h, w)
    for a, b, h in d["reeds"]:
        reeds(pg, S, a, b, h)
    for a, b in d["iris"]:
        iris(pg, S, a, b)
    # the season's water over the bed and the plant feet (see-through), then the people, then the cut railings
    for z, fill_, lab, dash in filled:
        water(pg, S, z)
        level_line(pg, S, z, lab % z, None, colour=FLOOD)
    if sea["strip_held"]:
        water(pg, S, THALWEG[1])
        if not filled:
            level_line(pg, S, THALWEG[1], "continuous strip %+.2f, 0.30 m (design)" % THALWEG[1], None, colour=FLOOD)
    wl = max([THALWEG[1] if sea["strip_held"] else -99.0] + [w[0] for w in filled])
    for s, kind, flip in people:
        g = S.surf(s)
        if g < wl + 0.02 and kind != 8:
            notes.append("%s, section %s: person at s %.1f left out, the ground there is under water." % (
                sea["name"], d["key"], s))
            continue
        if g < Q500 and not FIGURES_IN_FLOOD_REACH:
            continue
        figure(pg, S, s, kind, flip)
    for s, flip in sea["bikes"].get(d["key"], []):
        if S.surf(s) >= Q500 or FIGURES_IN_FLOOD_REACH:
            bike(pg, S, s, flip)
    for s, side in d["rails"]:
        handrail(pg, S, s + side * 0.15 * S.dir, S.surf(s + side * 0.3 * S.dir))
    # callouts
    ybase = S.Y(z_top) + 6.0
    callouts(pg, S, placed, ybase, size)
    # dimensions and the material band
    yd = S.Y(S.zb) - 5.0
    dims(pg, S, yd)
    band(pg, S, yd - 15.0)
    x_r = S.X(d["s_to"]) + 8.0
    lv = [(THALWEG[1], "bed low point (survey)"), (THALWEG[1] - STRIP[2], "strip bottom (design)")]
    lv += [(w[0], "water, %s (calculated)" % sea["key"]) for w in sea["water"]]
    for sa, sb, z, mat, lab in S.flats:
        if z is not None:
            lv.append((z, "design"))
    lv.append((DRY + 1.10, "handrail top (design)"))
    if d.get("pergola"):
        lv.append((DRY + max(p[2] for p in d["pergola"]["plates"]), "shading top (design)"))
    vdims(pg, S, lv, x_r)
    return yd - 15.0 - 9.0


# ================================================================ Rhino side (only when run inside Rhino)
def rhino_inputs(log):
    """S4 from the open file and a fresh cut of the survey ground along it. None where missing."""
    try:
        import Rhino
        import System
    except Exception:
        return None, None, None
    doc = Rhino.RhinoDoc.ActiveDoc
    if doc is None:
        return None, None, None
    A, B = S4_A, S4_B
    found = "embedded coordinates"
    try:
        o = doc.Objects.FindId(System.Guid(S4_ID))
        cands = [o] if o is not None else []
        for L in doc.Layers:
            if L.Name.lower() == "sec_lines" and not L.IsDeleted:
                cands += list(doc.Objects.FindByLayer(L) or [])
        for o in cands:
            c = o.Geometry
            if not hasattr(c, "PointAtStart"):
                continue
            p, q = c.PointAtStart, c.PointAtEnd
            for (u, v) in (((p.X, p.Y), (q.X, q.Y)), ((q.X, q.Y), (p.X, p.Y))):
                if math.hypot(u[0] - A[0], u[1] - A[1]) < 1.0 and math.hypot(v[0] - B[0], v[1] - B[1]) < 1.0:
                    A, B, found = u, v, "the open file (sec_lines)"
                    break
            if found != "embedded coordinates":
                break
    except Exception as e:
        log.append("S4 search failed (%s); embedded coordinates used." % e)
    log.append("Section line S4 taken from %s." % found)
    L = math.hypot(B[0] - A[0], B[1] - A[1])
    ux, uy = (B[0] - A[0]) / L, (B[1] - A[1]) / L

    def su(x, y):
        return (x - A[0]) * ux + (y - A[1]) * uy, -(x - A[0]) * uy + (y - A[1]) * ux

    # ---- survey points along the cut
    names = ["NOKTA_TAKEOMETRI", "EGRI_1M", "EGRI_2M", "EGRI_ARA", "SEV_UST", "SEV_ALT", "HIDRO_DERE_SULU"]
    pts = {}
    count = {}
    try:
        for Ly in doc.Layers:
            if Ly.IsDeleted or Ly.Name not in names:
                continue
            for o in doc.Objects.FindByLayer(Ly) or []:
                g = o.Geometry
                P = []
                if isinstance(g, Rhino.Geometry.Point):
                    P = [g.Location]
                elif isinstance(g, Rhino.Geometry.Curve):
                    ok, pl = g.TryGetPolyline()
                    if ok:
                        P = list(pl)
                    else:
                        nc = g.ToNurbsCurve()
                        P = [cp.Location for cp in nc.Points] if nc.Degree == 1 else \
                            [g.PointAt(t) for t in g.DivideByLength(1.0, True)]
                for p in P:
                    if p.Z <= 1.0:
                        continue
                    s, off = su(p.X, p.Y)
                    if 480.0 <= s <= 740.0 and abs(off) <= 60.0:
                        pts[(round(p.X, 2), round(p.Y, 2))] = p.Z
                        count[Ly.Name] = count.get(Ly.Name, 0) + 1
    except Exception as e:
        log.append("Reading survey heights failed: %s" % e)
    prof = None
    if len(pts) >= 100:
        try:
            import Grasshopper.Kernel.Geometry as GKG
            keys = list(pts.keys())
            nodes = GKG.Node2List()
            for (x, y) in keys:
                nodes.Append(GKG.Node2(x - A[0], y - A[1]))
            faces = GKG.Delaunay.Solver.Solve_Faces(nodes, 1)
            tris = []
            for f in faces:
                a, b, c = keys[f.A], keys[f.B], keys[f.C]
                tris.append((a, b, c))
            Z = []
            s0, ds, n = PROFILE_S0, PROFILE_DS, len(PROFILE_Z)
            cell = {}
            for t in tris:
                xs = [p[0] for p in t]
                ys = [p[1] for p in t]
                for i in range(int(min(xs) // 5), int(max(xs) // 5) + 1):
                    for j in range(int(min(ys) // 5), int(max(ys) // 5) + 1):
                        cell.setdefault((i, j), []).append(t)
            miss = 0
            for i in range(n):
                s = s0 + i * ds
                x, y = A[0] + ux * s, A[1] + uy * s
                z = None
                for (a, b, c) in cell.get((int(x // 5), int(y // 5)), []):
                    det = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
                    if abs(det) < 1e-12:
                        continue
                    l1 = ((b[1] - c[1]) * (x - c[0]) + (c[0] - b[0]) * (y - c[1])) / det
                    l2 = ((c[1] - a[1]) * (x - c[0]) + (a[0] - c[0]) * (y - c[1])) / det
                    l3 = 1.0 - l1 - l2
                    if min(l1, l2, l3) >= -1e-9:
                        z = l1 * pts[a] + l2 * pts[b] + l3 * pts[c]
                        break
                if z is None:
                    miss += 1
                    z = PROFILE_Z[i]
                Z.append(z)
            dmax = max(abs(Z[i] - PROFILE_Z[i]) for i in range(n))
            prof = (s0, ds, Z)
            log.append("Ground cut again from the open file: %d survey heights (%s); largest difference from the "
                       "embedded profile %.3f m%s." % (len(pts), ", ".join("%s %d" % kv for kv in sorted(count.items())),
                                                       dmax, (", %d stations outside the TIN kept embedded" % miss) if miss else ""))
        except Exception as e:
            log.append("Ground re-cut failed (%s); embedded profile used." % e)
    else:
        log.append("Survey height layers not found in the open file (%d heights); embedded profile used "
                   "(cut from Nil's survey DXF)." % len(pts))
    return (A, B), prof
'''


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
