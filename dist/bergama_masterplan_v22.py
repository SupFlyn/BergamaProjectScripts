# -*- coding: utf-8 -*-
"""BERGAMA MASTERPLAN v22 (2026-10-26): Group 6's proposal (the zones, their programme and the water links) drawn
as the three alternatives Aras asked for (Q14, 24 Oct), so he can compare them. Merges bergama_masterplan v9 and
bergama_programme_diagrams puzzle v2.3 (MERGE_PLAN.md section 3, M1); both are retired. v11 (Thread 5 of the 22 Oct
batch): the riverside walks, the riverside spine on the real edge, the main spine, the eight stops and the trees.

WHAT IT DRAWS (one page per alternative and zone-base option: 3 x 2 = six PDFs per press)
  Alternative 1  the programme puzzle of v2.3: every space of each working area (zones, river, streets, housing,
                 parks, heritage, other buildings, cleared ground) is one piece grown on one grid, the more extrovert
                 the more liquid; short keywords scattered inside the pieces, word size by significance (table SIG);
                 the darker COMMONS piece where three (else two) programme pieces meet (table HUB); context words
                 (RIVER, RESIDENTIAL, PARK, HERITAGE) instead of a legend. The four working areas side by side on one
                 page at one scale. The programme pieces are drawn at the opacity setting on a white base; the
                 commons stays darker (drawn opaque).
  Alternative 2  the same puzzle, but every programme piece grows on its own (no piece stops another) and all of
                 them are drawn at the opacity setting on one white base, so where pieces overlap the colour darkens
                 by itself. No separate commons piece: its name and words sit where most pieces overlap.
  Alternative 3  masterplan and programme in one drawing: the whole corridor along the river (upstream entry on the
                 left, downstream end on the right), the masterplan's zones in its hand-marker language (white base,
                 light fill at the opacity setting so overlaps darken, verge band, the code's pattern, bold broken
                 hand outline), the water strip, the survey context (contours, buildings, streets, parks, stream,
                 historic wall, bridges), the bold hand-drawn link arrows coloured by type (water dark water-blue,
                 high water dashed water-blue with dark heads, people to the water red with two heads), and on the
                 zones the programme keywords and the darker commons of alternative 1.
  Places, not people (Q16): UPSTREAM ENTRY, K4 BRIDGE, K5 BRIDGE, DOWNSTREAM END. No working-area outlines: a working
  area only sets what a zoomed page covers (the area and zoom_m round it); alternative 3 covers site_alan.
  No callouts, scale, m², notes or bridge labels (Aras 18 Oct 19:36). All vector, whole-string Helvetica text.

HOW TO USE
  1. Open Bergama_Altlik.3dm in Rhino 8 (v12; any survey file works). Bake the zones with bergama_zone_base_v9 (layers
     Option_A::INT_* and Option_B::INT_*) and edit them as you like.
  2. Grasshopper > "Python 3 Script" component: paste this file and wire a plain Button into any input (build, out,
     run ...). Every other input is optional.
  3. Press the Button. One press writes the sheet, the 1:1,000 detail sheet (v21), masterplan_results.json and
     booklet/ (blocks.json, results.json) into the folder
     Downloads/Bergama/output/bergama_masterplan (24 Oct, Aras rule); a second press writes them again. With a Boolean Toggle on rhino_bake set to True,
     the press also bakes the six sheets into Rhino under layer MP11, beside everything else in the file and beside
     each other, never on top of each other or of the survey (a press replaces the last bake).
  INPUTS (any name case; text, number or panel)
    run          Button (v21; any input name works; a plain Button)
    rhino_bake   Boolean Toggle: bake the sheets into Rhino as well (default False)
    opacity      opacity of the lower-opacity pieces, 0-1 or 1-100 % (default OPACITY = 0.5, Aras's example value)
    scale        print scale 1:scale of all three alternatives (default 1000 since v16: studio brief of 26 Oct)
    zoom_m       margin round each zoomed working-area page (alternatives 1 and 2), m (default 30; ring_m also works)
    option       "both" (default), "A" or "B"
    zone_base    path of bergama_zone_base_v5.py or its .json (only used when the file has no Option_X::INT_ zones)
  OUTPUTS  log: the log of the last press (kept after the Button is released); pdf: the paths. The text under
           the component shows the version and the total time.

DATA RULES
  * Zones, strip, arrows, cleared buildings and paths are read as bergama_zone_base_v5 bakes them: curves on
    Option_A::INT_* / Option_B::INT_* with user text label, id, study_area, zone (tier W/F/D) and link. Fallbacks, in
    this order, for an option with no such curves: the zone_base input; bergama_zone_base_v5.py (its BASE_DATA) or
    its .json next to the .3dm / .gh or in their scripts folder; the copy embedded below (ZONE_COPY, made from zone
    base v5's BASE_DATA, md5 c1f667e7eae0a000d4d80078a433427d: only the kinds drawn here, coordinates rounded to
    1 cm). A file that cannot be read is skipped. A balloon on the component says which source was used.
  * Working areas (v12): the curves on calisma_alan of the open file, worked as one area in two parts; else the
    copy CALISMA_COPY (Bergama_Altlik.3dm, 25 Oct). Survey context: the layers in ROLE_OF; none found = the zones on plain paper.
  * Every zone size is a placeholder (zone base v5, user text basis). Keywords are CONTEXT §4's sourced words
    (v2.3 tables NAMES, SUBS); SIG and HUB are design readings, not data. Piece growth, opacity, patterns, the hand
    wobble and the arrow snapping are graphic only; the areas stay the zone curves.
  * Assumptions, stated: OPACITY 0.5 is Aras's example value, not a decided one; north on alternative 3 is the
    survey grid's +Y (no true north without selinus_board); alternative 2 names the commons where most pieces
    overlap.

NEW IN v22 (Aras 26 Oct, Rhino log "detail dt_upstream: label not placed: 4 BACK TO THE STREAM"): the water
  route's labels on the detail sheet are never left out. When no spot round the numbered marker is free,
  place_label tries round points along the route, then the free spot nearest the marker anywhere on the panel
  (2 mm grid), with a thin leader; still no overlap with another label. Other labels and the main sheet unchanged.
  Rough volumes (Aras 26 Oct 06:27): the route labels of the reed basins and retention terraces add
  "~ m³" = zone area x depth (reed basins 0.46 m, EPA 832-F-00-024, 2000; terraces 0.30 m, design depth);
  the method is a line in the detail legend.
  Output: Bergama_masterplan_v22_A.pdf, Bergama_masterplan_v22_A_detail.pdf.
OLDER VERSIONS: their notes are in HISTORY.md (repo SupFlyn/BergamaProjectScripts, src/bergama_masterplan/).

HOW WE KNOW IT WORKS: after a press the text under the component reads "v11 · done N s" and the log lists the six
PDFs with their times; each opens as one page. Before delivery (24 Oct): py_compile and pyflakes clean, and a mock
run with the course survey and zone base v5's data wrote all six PDFs, which were rendered and looked at.

Code reused (same project): Button, memory, log, PDF writer, geometry, puzzle and labels of programme diagrams
v2.3 (from bergama_water_loop v2.0); link types and rules, palette tones, hand line and arrow sizes of masterplan v9;
the vector hand arrow of bergama_water_board v1.
"""

import os
import re
import json
import math
import time
import zlib
import heapq
import base64
import random
import tempfile
import datetime
import types as _types

try:
    import Rhino
    import Rhino.Geometry as rg
    import scriptcontext as sc
except ImportError:                                                  # outside Rhino (test harness)
    Rhino = rg = None
    sc = _types.SimpleNamespace(sticky={})

VERSION = "bergama_masterplan v22 (2026-10-26)"
SHORT = "v22"
BUTTON_WORDS = ("build", "bake", "run", "go", "press", "button", "start", "out")
SETTINGS = ("rhino_bake", "opacity", "scale", "zoom_m", "ring_m", "option", "zone_base")   # never taken for the Button
OPACITY = 0.5                         # opacity of the lower-opacity pieces (Aras 05:51: a setting; 0.5 his example)
RING_M = 30.0                         # nearest ring (programme CONTEXT §3.2: inferred, not a sourced number)
BOARD_SCALE = 1000.0                  # v16: studio brief 26 Oct, "1/1000 scale master plan" (was 2000, v2.3's board scale)
_SCALE = [BOARD_SCALE]               # v16: the scale of this press, for the scale bar in sheet_head
_ALPHA = [OPACITY]                   # v17: the opacity of this press, for the legend swatches
BOARD_MAX_W = 4000.0                  # a board of the four working areas wider than this goes into two rows (mm)
LINE_STEP_M = 1.0                     # survey lines are cut at the ring to this step
OUT_FOLDER = "bergama_masterplan"
OUT_NAME = "Bergama_masterplan_v22_{}.pdf"     # v19: one sheet per option
DETAIL_NAME = "Bergama_masterplan_v22_{}_detail.pdf"   # v21: the 1:1,000 detail sheet
LOG_NAME = "bergama_masterplan_log.txt"
LOG_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "logs")   # Aras 25 Oct 09:34-09:35: every script's log here

RESULTS_NAME = "masterplan_results.json"   # v11: read by the water balance (riverside_walk_m2)
BAKE_ROOT = "MP11"                    # Rhino layer of the bake (rhino_bake = True)
BAKE_GAP = 0.10                       # gap between baked sheets and to the rest of the file (x the sheet's width)
CREDIT = u"Group 6 · Aras Özkaymakcı · Begüm Arslan · Nil Çetin"
OPTION_TEXT = {"A": u"OPTION A · organic only where the project meets the water",
               "B": u"OPTION B · no organic forms"}
ALT_TEXT = {1: u"MASTERPLAN · PROGRAMME"}   # v19: the one sheet

# working area key (survey layer, data key only), stage / place name on the drawing (Q16), idea (CONTEXT §4)
AREAS = [("calisma_alan[0]", u"UPSTREAM ENTRY TO K4 BRIDGE", u""),          # v12: one shared working area, north part
         ("calisma_alan[1]", u"K5 BRIDGE TO DOWNSTREAM END", u"")]          # south part (Aras 25 Oct 08:05)
CALISMA_LAYER = "calisma_alan"
SITE_LAYER = "site_alan"                              # v15: analysis range = extent of alternative 3
SITE_COPY = [(29388.015, 32540.503), (31220.325, 30364.153), (31625.069, 30704.915), (29792.759, 32881.264)]   # v15: site_alan of Bergama_Altlik.3dm (rectangle 2,845 x 529 m, 25 Oct 08:25)
CLOSE_GAP = 5.0                                   # v12: m, an open outline closer than this counts as closed
SPINE_OUTSIDE_OK = True                           # v12: the riverside spine (city link) may leave calisma_alan
SNAP_M = 15.0                                     # v12: m, a proposal this close to calisma_alan counts as on it
WALK_CLIP = False                                 # v12: Aras 08:10: the walk outside calisma_alan (207 of 4,211 m in
                                                  # the copy) is too small to matter: walks drawn continuous
CALISMA_COPY = [                                   # v12: calisma_alan of Bergama_Altlik.3dm (25 Oct 08:25: closed, ends snapped onto site_alan), survey m
    [(29696.903, 32800.562), (29872.423, 32572.84), (29880.693, 32496.334), (29818.865, 32475.301), (29825.821, 32398.074), (29923.185, 32344.348), (29904.985, 32311.252), (29997.056, 32290.092), (30053.417, 32139.667), (30004.049, 32108.006), (29954.803, 32210.611), (29792.114, 32247.062), (29761.684, 32302.735), (29754.016, 32451.383), (29678.437, 32447.696), (29632.398, 32496.591), (29665.339, 32526.253), (29612.859, 32696.506), (29600.496, 32719.394)],
    [(30178.18, 31923.887), (30138.072, 31887.655), (30257.694, 31773.217), (30389.686, 31405.252), (30701.152, 30991.252), (30840.053, 31053.865), (31044.852, 30781.877), (31014.2, 30757.409), (31373.442, 30493.066), (31453.175, 30560.194), (31332.978, 30864.179), (31012.679, 31323.349), (30737.856, 31286.66), (30712.87, 31331.891), (30556.09, 31450.103), (30454.629, 31577.301), (30434.156, 31607.332), (30313.613, 31812.92)],
]


# ---------------------------------------------------------------- colours (palette.json 1.4 "masterplan" tones)
COL = {
    "paper": "FFFFFF", "ink": "4A3F35", "ink2": "847E75", "ink_dark": "2C2219", "white": "FFFFFF",
    "bld": "D8D5CC", "bld_edge": "B0AC9C", "her": "E4CAC9", "her_edge": "AF7474", "park": "DFEBC0",
    "road": "CFCCC5", "road_edge": "B0AC9C", "contour": "E2E0D4", "contour10": "D2CFC2",
    "river": "91ADB4", "river_mid": "5D7F8D", "river_dark": "32525F", "histwall": "895152", "path": "847E75",
    "accent": "8B3A3F", "accent_dark": "633131", "verge": "A3AD8B", "tree": "8C9969", "tree_mid": "727A4E",
    "walk": "3C4733", "spine": "E0B67D", "spine_dark": "604826",   # v11: walk = palette reference 3C4733; spines =
}                                                                   # the masterplan's "centre" tones
# programme family per zone code (masterplan v9 ZONE_CODES) and its (light, mid, dark) tones
CODE_FAMILY = {"WS": "storage", "WD": "discharge", "WT": "wetland", "WP": "planting", "WA": "amphibious",
               "WI": "agriculture", "CH": "heritage", "MC": "centre", "HO": "housing", "CV": "civic", "GR": "park",
               "SR": "sport", "PA": "service", "DG": "agriculture"}   # v13: DG = Demeter's Garden
MP = {"storage": ("CBD9F8", "92A3C9", "3E4C6E"), "discharge": ("90C5D2", "4B92A3", "1B535E"),
      "wetland": ("CBEDE5", "8DB8AF", "2D564E"), "planting": ("ABBBAE", "748878", "3B4D3F"),
      "amphibious": ("C1D3DB", "889EA8", "3C5159"), "agriculture": ("C6C08D", "948B49", "534E25"),
      "heritage": ("E4CAC9", "AF7474", "4C2528"), "centre": ("E0B67D", "AA8148", "604826"),
      "housing": ("F3E7CD", "BFB08F", "594B2E"), "civic": ("AE90AA", "7F5B7B", "452842"),
      "park": ("DFEBC0", "A7B67F", "49522B"), "sport": ("E4B8A1", "B58063", "68432F"),
      "service": ("A8A49C", "767167", "3E3A31")}

# ---------------------------------------------------------------- the words (CONTEXT §4, verbatim; nothing else)
# Keywords cut from the sourced sub-programme labels of CONTEXT §4 (Nil 18:25: "just use keywords"); nothing added
NAMES = {("aras_alan", "WS", None): u"RETENTION TERRACES", ("aras_alan", "GR", None): u"SHADED WALK",
         ("aras_alan", "WT", None): u"REED BASINS", ("aras_alan", "WD", None): u"SPILLWAY",
         ("begum_alan", "WA", "W"): u"BED", ("begum_alan", "WA", "F"): u"FLOOD TERRACE",
         ("begum_alan", "GR", None): u"DRY TOP", ("nil_alan", "WP", None): u"STREAMSIDE PLANTING",
         ("calisma_alan", "DG", None): u"DEMETER'S GARDEN"}   # v13: Begum's idea (card i01)
SUBS = [  # (working-area layer, code, tier, only for: None / "A" / "B" / a working-area key, keywords)
    ("aras_alan", "WS", "D", None, [u"WINTER RAIN", u"STEPPED", u"SEATING"]),
    ("aras_alan", "GR", "D", None, [u"SHADE", u"WALK", u"CAFE"]),
    ("aras_alan", "WT", "F", None, [u"CLEANING", u"DE-ODOUR", u"RUNOFF"]),
    ("aras_alan", "WD", "W", None, [u"OVERFLOW", u"RETURN"]),
    ("begum_alan", "WA", "W", None, [u"WATER STRIP", u"STEPPING STONES", u"WEIRS", u"PLAZA", u"REED"]),
    ("begum_alan", "WA", "F", None, [u"WATER STEPS", u"SEATING", u"TAMARIX"]),
    ("begum_alan", "GR", "D", None, [u"BRIDGE VIEW", u"KIOSK", u"SHADE", u"LAVENDER"]),
    ("nil_alan", "WP", "F", None, [u"CLEAN STREAM", u"FLOOD-PROOF", u"ODOUR-FREE", u"WILLOW"]),
    ("calisma_alan", "DG", "D", None, [u"OLIVES", u"STONE PINE", u"AROMATICS", u"SEASONAL BEDS", u"CAFE",
                                       u"WATER COLLECTION BASIN"]),   # v13: Begum's PDF, verbatim words
]
REMOVE_WORDS = [u"CLEARED"]
# the common piece where the functions of a working area meet: name + what it gathers. A design reading of the
# sourced words above (Aras 19:27, campus reference), not data; edit freely.
HUB = {"calisma_alan[0]": (u"WATER AND HERITAGE COMMONS", [u"COLLECT", u"CLEAN", u"HOLD", u"K4 BRIDGE", u"PLAZA"]),
       "calisma_alan[1]": (u"AMPHIBIOUS STREAM COMMONS", [u"K5 BRIDGE", u"WATER", u"GIVE BACK", u"WALK", u"GREEN"])}
# v12: v11's four commons merged per part (WATER + HERITAGE; AMPHIBIOUS + RIVER), their words joined
# word-size factor per zone = how much it carries the working area's idea (three_ideas.md); a design reading.
# Upstream entry "Collect, clean and hold": the reed basins clean and the terraces hold; the spillway returns; the
# walk serves. K4 / K5 "Amphibious heritage threshold": the bed is the amphibious core, the terrace its edge, the dry
# top the view. Downstream end "Give back": the riverside planting is the idea.
SIG = {("aras_alan", "WT", None): 1.0, ("aras_alan", "WS", None): 1.0, ("aras_alan", "WD", None): 0.7,
       ("aras_alan", "GR", None): 0.55,
       ("begum_alan", "WA", "W"): 1.0, ("begum_alan", "WA", "F"): 0.75, ("begum_alan", "GR", None): 0.6,
       ("nil_alan", "WP", None): 1.0, ("calisma_alan", "DG", None): 0.9}
HUB_SIG = 1.25                 # the commons: above every zone
STEPS = (1.0, 0.85, 0.72, 0.6, 0.5, 0.42, 0.35)   # sizes tried, largest first, when a word does not fit
HUB_R_M = (24.0, 16.0, 10.0)   # meeting distance tried, m (graphic)
HUB_MAX = 0.35                 # the common piece takes at most this share of the programme pieces
HUB_MIN_M2 = 150.0             # smaller common fragments are dropped
KIND_WORD = {"river": u"STREAM", "housing": u"RESIDENTIAL", "park": u"PARK", "heritage": u"HERITAGE"}
PATH_WORDS = {"nil_alan": [u"FLOODABLE DECK"]}
ROUND_M = 9.0                  # corner rounding of the cleared-building outlines, m (graphic)
DROPPED = ("FARM CHANNEL", "ORCHARD", "FARMLAND")   # no farmland or farm channel inside the site (CONTEXT §2)

# ---------------------------------------------------------------- links (masterplan v9, from ideas.txt)
# Link arrows by MEANING (Aras 2026-10-18: "it should stand for something crucial in the design"); the layer's tag
# word or the user text link names the type. None = the arrow's end is in no zone: the river (or open ground).
LINK_TYPES = {
    "water": dict(words=("water", "su", "chain"), heads=1, key=u"WATER", src="ideas.txt lines 6, 12, 26"),
    "people": dict(words=("people", "access", "insan", "erisim", "city"), heads=2, key=u"PEOPLE TO THE WATER",
                   src="ideas.txt main goal, lines 16-17"),
    "flood": dict(words=("flood", "taskin", "seasonal", "highwater"), heads=1, key=u"HIGH WATER",
                  src="ideas.txt lines 8, 18, 26"),
}
# The water route's allowed steps (from code -> to code) and the brief's reason for each; any other step is a warning
WATER_STEPS = {
    (None, "WS"): "the river's extra water is stored (line 6)",
    (None, "WT"): "river water is treated when needed (line 6)",
    (None, "WP"): "plants feed and regulate the river (line 7)",
    ("WP", None): "plants feed and regulate the river (line 7)",
    ("WS", "WI"): "extra water is first spent on agriculture (line 26; drainage feeds orchards, line 12)",
    ("WS", "WT"): "then the excess goes to treatment (line 26)",
    ("WS", "WD"): "storage discharges (line 6)",
    ("WS", None): "storage raises the river when needed (line 6)",
    ("WT", "HO"): "treated water to the city mains or drinking water (line 26)",
    ("WT", "MC"): "treated water to the city mains or drinking water (line 26)",
    ("WT", "CV"): "treated water to the city mains or drinking water (line 26)",
    ("WT", "PA"): "treated water to the city mains (line 26)",
    ("WT", "WD"): "treated water is discharged (line 6)",
    ("WT", None): "treated water back to the river (line 6)",
    ("WD", None): "discharge back to the river (line 6)",
    ("WD", "WI"): "the drainage channel feeds orchards and farmland (line 12)",
    (None, "WD"): "the river feeds a channel by gravity, downstream, for the farms (lines 12, 26)",
}
FLOOD_TO = ("WA", "WS", "WD", "WT")                  # zones meant to take high water (ideas.txt lines 8, 18 and 26)
CITY_CODES = ("CH", "MC", "HO", "CV", "GR", "SR", "PA")
WATER_SIDE = ("WS", "WD", "WT", "WP", "WA", "WI")
SNAP_IN_M = 2.0                # masterplan v7: an arrow starts / ends this far inside the zones it joins (m)
MIN_LINK_MM = 7.0              # masterplan v7: shortest arrow on the sheet (mm)
SHORT_LINK_M = 60.0            # masterplan v6: water / flood links up to this long also get a water band (m)
# The masterplan's bold hand-drawn arrow (v8 / v9 G, as water loop v1.2 and the water board draw it; the standard
# since 24 Oct): marker shaft 2.0 mm, barbs 5.84 mm at 38 deg and 1.6 mm, serifs 2.79 mm at 0.4 mm, barb overshoot
# 0.64 mm, shaft wobble 0.175 mm over 15.2 mm; paper mm.
HA = dict(shaft=2.0, barb=5.84, ang=38.0, barb_w=1.6, serif=2.79, serif_w=0.4, over=0.64, amp=0.175, wav=15.24)

# survey layers (last part of the layer path) and what they are on the base
BUILDING_LAYERS = ("BINA_RESMI", "BINA_OKUL", "BINA_DINITESIS", "BINA_DINI_TESIS", "BINA_FABRIKA",
                   "BINA_INS_HALINDE", "BINA_SPOR_TESISLERI", "BINA")
ROLE_OF = dict([(n, "building") for n in BUILDING_LAYERS] + [("BINA_MESKEN", "housing"),
    ("BINA_TARIHI", "heritage"), ("BINA_HARABE", "heritage"), ("BINA_SUNDURMA", "shed"),
    ("YOL_SOSE", "road"), ("YOL_BORDUR", "kerb"), ("YOL_KOPRU", "bridge"), ("HIDRO_DERE_SULU", "stream"),
    ("HIDRO_HAVUZ", "pond"), ("HIDRO_GOL", "pond"), ("SEV_UST", "bank_top"), ("SEV_ALT", "bank"),
    ("SEV_SEVUST", "chan_top"), ("SEMBOL_TEK_AGAC", "tree"),
    ("ORMAN_PARK_BAHCE", "park"), ("SINIR_DUVAR", "wall"), ("SINIR_TARIHI_SUR", "histwall"), ("EGRI_5M", "contour"),
    ("EGRI_10M", "contour10")])


# ================================================================ Grasshopper inputs, memory, status (v2.3)
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
    """25 Oct 12:10: the done text of the script wired into input `name`, read from Rhino's memory (sticky) instead of
    the wire: on Aras's canvas ZoneBase's done reached MasterPlan as Null after a bake. Keys: "done:<guid>" (zone base,
    masterplan, water board) or "...:<guid>_done" (template scripts)."""
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
    if isinstance(v, (list, tuple)):                 # several wires (e.g. a Button and a done): take the done text
        v = next((x for x in v if str(x).startswith("done ")), None)
    s = str(v) if v is not None else ""
    if not s.startswith("done ") and name:                 # 12:10: Null on the wire: read the done text from memory
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


def _letters(s):
    return "".join(c for c in str(s).lower() if c.isalpha())


def button_state():
    """(name, pressed) of the Button input: an input whose name is a button word, else an input fed by a Button,
    else any input that is not one of the settings (v10: a settings input is never taken for the Button)."""
    names = [k_ for k_ in _GH_IN if k_.lower() not in SETTINGS]
    for k_ in names:
        if _letters(k_) in BUTTON_WORDS:
            return k_, to_bool(_GH_IN[k_])
    try:
        for p_ in ghenv.Component.Params.Input:                      # noqa: F821
            nm = str(p_.NickName or p_.Name)
            if nm.lower() in SETTINGS:
                continue
            for src_ in p_.Sources:
                if "button" in type(src_.Attributes.GetTopLevel.DocObject).__name__.lower():
                    return nm, to_bool(_GH_IN.get(nm, False))
    except Exception:
        pass
    if names:
        return names[0], to_bool(_GH_IN[names[0]])
    return None, False


def inp(name, default=None):
    for k_, v_ in _GH_IN.items():
        if k_.lower() == name.lower():
            if isinstance(v_, (list, tuple)):
                v_ = next((x for x in v_ if x is not None and str(x).strip()), None)
            if v_ is None or not str(v_).strip():
                return default
            return v_
    return default


def inp_num(name, default, warn=None):
    v = inp(name, None)
    if v is None:
        return default
    try:
        f = float(str(v).strip().replace(",", ".").rstrip("%"))
        if f > 0:
            return f
    except Exception:
        pass
    if warn is not None:
        warn.append(u"input {} = '{}' is not a positive number: {:g} was used".format(name, v, default))
    return default


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


def mem_set(k, v, persist=True):
    try:
        sc.sticky[_key(k)] = v
    except Exception:
        pass


GH_LABEL = "MasterPlan"                                # Aras 25 Oct 09:44: name under the component


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


# ================================================================ geometry (water loop v2 / v2.3)
def area2(P):
    a = 0.0
    for i in range(len(P)):
        x0, y0 = P[i][0], P[i][1]
        x1, y1 = P[(i + 1) % len(P)][0], P[(i + 1) % len(P)][1]
        a += x0 * y1 - x1 * y0
    return a / 2.0


def ring(P):
    P = [(float(p[0]), float(p[1])) for p in P]
    if len(P) > 1 and abs(P[0][0] - P[-1][0]) < 1e-9 and abs(P[0][1] - P[-1][1]) < 1e-9:
        P = P[:-1]
    return P


def pip(x, y, P):
    ins = False
    j = len(P) - 1
    for i in range(len(P)):
        xi, yi = P[i][0], P[i][1]
        xj, yj = P[j][0], P[j][1]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi:
            ins = not ins
        j = i
    return ins


def seg_dist(px, py, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = dx * dx + dy * dy
    t = 0.0 if L == 0 else max(0.0, min(1.0, ((px - a[0]) * dx + (py - a[1]) * dy) / L))
    return math.hypot(px - a[0] - t * dx, py - a[1] - t * dy)


def inner_pt(P, n=18):
    """A point well inside a ring (the grid point farthest from its edges)."""
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    step = max(1, len(P) // 120)
    E = [(P[i], P[(i + step) % len(P)]) for i in range(0, len(P), step)]
    best, bd = None, -1.0
    for i in range(n):
        for j in range(n):
            x = min(xs) + (i + 0.5) / n * (max(xs) - min(xs))
            y = min(ys) + (j + 0.5) / n * (max(ys) - min(ys))
            if not pip(x, y, P):
                continue
            d = min(seg_dist(x, y, a, b) for a, b in E)
            if d > bd:
                best, bd = (x, y), d
    return best or (sum(xs) / len(xs), sum(ys) / len(ys))


def bbox(P):
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    return (min(xs), min(ys), max(xs), max(ys))


def hit(a, b, pad=0.0):
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])


def chaikin(P, n=3, closed=False):
    for _ in range(n):
        Q = [] if closed else [P[0]]
        m = len(P) if closed else len(P) - 1
        for i in range(m):
            a, b = P[i], P[(i + 1) % len(P)]
            Q += [(0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]),
                  (0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1])]
        P = Q if closed else Q + [P[-1]]
    return P


def principal_angle(P):
    cx, cy = sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P)
    sxx = sum((p[0] - cx) ** 2 for p in P)
    syy = sum((p[1] - cy) ** 2 for p in P)
    sxy = sum((p[0] - cx) * (p[1] - cy) for p in P)
    return math.degrees(0.5 * math.atan2(2 * sxy, sxx - syy))


def thin(P, n=120):
    return P[::max(1, len(P) // n)]


def seg_closest(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / max(dx * dx + dy * dy, 1e-12)
    t = max(0.0, min(1.0, t))
    return (a[0] + t * dx, a[1] + t * dy)


def closest_pair(A, B):
    """Closest points between two rings (or a point and a ring); returns (point on A, point on B, distance)."""
    best = (A[0], B[0], 1e18)
    for X, Y, flip in ((A, B, False), (B, A, True)):
        if len(Y) < 2:
            continue
        for p in X:
            for i in range(len(Y)):
                q = seg_closest(p, Y[i], Y[(i + 1) % len(Y)])
                d = math.hypot(q[0] - p[0], q[1] - p[1])
                if d < best[2]:
                    best = (q, p, d) if flip else (p, q, d)
    return best


def mix(c1, c2, t):
    a, b = hex_rgb(c1), hex_rgb(c2)
    return "".join("{:02X}".format(int(round(255 * (a[i] + (b[i] - a[i]) * t)))) for i in range(3))


def densify(P, step):
    out = [tuple(P[0])]
    for a, b in zip(P[:-1], P[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(1, int(math.ceil(L / step)))
        for j in range(1, n + 1):
            t = j / float(n)
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    return out


def arclen(P):
    s = [0.0]
    for a, b in zip(P[:-1], P[1:]):
        s.append(s[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    return s


def at_len(P, s, t):
    """Point and unit direction at arc length t along P (s = arclen(P))."""
    t = max(0.0, min(s[-1], t))
    for i in range(len(P) - 1):
        if t <= s[i + 1] or i == len(P) - 2:
            d = max(s[i + 1] - s[i], 1e-12)
            u = (t - s[i]) / d
            ux, uy = (P[i + 1][0] - P[i][0]) / d, (P[i + 1][1] - P[i][1]) / d
            return (P[i][0] + (P[i + 1][0] - P[i][0]) * u, P[i][1] + (P[i + 1][1] - P[i][1]) * u), (ux, uy)
    return tuple(P[-1]), (1.0, 0.0)


def sub_line(P, s, t0, t1):
    """The part of polyline P between arc lengths t0 and t1."""
    a, _ = at_len(P, s, t0)
    b, _ = at_len(P, s, t1)
    return [a] + [tuple(P[i]) for i in range(len(P)) if t0 < s[i] < t1] + [b]


# ================================================================ text metrics (Helvetica = Arial metrics, v2.3)
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


# ================================================================ page and PDF writer (v2.3; v10: alpha in 1 %
# steps on lines and circles too, clipping)
class Page(object):
    def __init__(self, W, H):
        self.W, self.H, self.items = W, H, []

    def poly(self, rings, fill=None, stroke=None, lw=0.1, dash=None, stripes=None, alpha=None):
        """alpha: opacity 0-1 of fill and stroke (None = opaque). stripes: (colour, spacing, width[, angle, wavy])."""
        rings = [r for r in rings if len(r) >= 3]
        if rings:
            self.items.append(("poly", rings, fill, stroke, lw, dash, stripes, alpha))

    def line(self, pts, stroke, lw=0.1, dash=None, cap=1, alpha=None):
        if len(pts) >= 2:
            self.items.append(("line", pts, stroke, lw, dash, cap, alpha))

    def circle(self, cx, cy, r, fill=None, stroke=None, lw=0.1, alpha=None):
        self.items.append(("circle", cx, cy, r, fill, stroke, lw, alpha))

    def text(self, s, x, y, size, color, bold=False, align="L", halo=None):
        if s:
            self.items.append(("text", s, x, y, size, color, bold, align, halo))

    def clip(self, rings):
        self.items.append(("clip", rings))

    def unclip(self):
        self.items.append(("unclip",))

    def clipline(self, rings, pts, stroke, lw, alpha=None):
        """A line drawn only inside rings (the verge band inside a zone)."""
        if len(pts) >= 2:
            self.items.append(("clipline", rings, pts, stroke, lw, alpha))


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


def _gs(alpha):
    """The ExtGState name of an opacity (1 % steps), or None when opaque."""
    if alpha is None or alpha >= 0.995:
        return None
    return "/A{:02d}".format(max(1, min(99, int(round(alpha * 100)))))


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

    def push(alpha):
        g = _gs(alpha)
        if g:
            A("q {} gs".format(g))
            cur.clear()
        return g

    def pop(g):
        if g:
            A("Q")
            cur.clear()

    for it in pg.items:
        kind = it[0]
        if kind == "poly":
            _, rings, fill, stroke, lw, dash, stripes, alpha = it
            g = push(alpha)
            if fill or stroke:
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
                cur.clear()
            pop(g)
        elif kind == "line":
            _, pts, stroke, lw, dash, cap, alpha = it
            g = push(alpha)
            col(stroke, True)
            lw_dash(lw, dash, cap)
            path(pts, False)
            A("S")
            pop(g)
        elif kind == "circle":
            _, cx, cy, r, fill, stroke, lw, alpha = it
            g = push(alpha)
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
            pop(g)
        elif kind == "clip":
            A("q")
            for r in it[1]:
                path(r, True)
            A("W* n")
            cur.clear()
        elif kind == "unclip":
            A("Q")
            cur.clear()
        elif kind == "clipline":
            _, rings, pts, stroke, lw, alpha = it
            A("q")
            for r in rings:
                path(r, True)
            A("W* n")
            cur.clear()
            g = push(alpha)
            col(stroke, True)
            lw_dash(lw, None, 1)
            path(pts, False)
            A("S")
            pop(g)
            A("Q")
            cur.clear()
        elif kind == "text":
            _, s, x, y, size, color, bold, align, halo = it
            w = text_w(s, size, bold)
            reps = [(halo, True), (color, False)] if halo else [(color, False)]
            for c_, hal in reps:
                if hal:
                    r_, g_, b_ = hex_rgb(c_)
                    A("q {} {} {} RG {} w 1 j 1 Tr".format(_f(r_), _f(g_), _f(b_), _f(size * 0.16)))
                else:
                    col(color, False)
                    A("0 Tr")
                dx = {"L": 0.0, "C": -w / 2, "R": -w}[align]
                A("BT /F{} {} Tf 1 0 0 1 {} {} Tm".format(2 if bold else 1, _f(size), _f(x + dx), _f(y)))
                A(pdf_str(s).decode("latin-1") + " Tj ET")
                if hal:
                    A("Q")
                    cur.clear()
    return "\n".join(o).encode("latin-1")


def write_pdf(pg, path, title):
    objs = []

    def add(b):
        objs.append(b)
        return len(objs)
    font = []
    for nm in ("Helvetica", "Helvetica-Bold"):
        font.append(add("<< /Type /Font /Subtype /Type1 /BaseFont /{} /Encoding << /Type /Encoding /BaseEncoding "
                        "/WinAnsiEncoding {} >> >>".format(nm, _DIFF).encode("latin-1")))
    gs = [add("<< /Type /ExtGState /ca {0} /CA {0} >>".format(_f(i / 100.0)).encode("latin-1")) for i in range(1, 100)]
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


def _move(pts, dx, dy):
    return [(x + dx, y + dy) for x, y in pts]


def blit(dst, src, dx, dy):
    """Copy the items of page src into page dst, moved by (dx, dy)."""
    for it in src.items:
        kd = it[0]
        if kd == "poly":
            dst.items.append((kd, [_move(r_, dx, dy) for r_ in it[1]]) + tuple(it[2:]))
        elif kd == "line":
            dst.items.append((kd, _move(it[1], dx, dy)) + tuple(it[2:]))
        elif kd == "circle":
            dst.items.append((kd, it[1] + dx, it[2] + dy) + tuple(it[3:]))
        elif kd == "text":
            dst.items.append((kd, it[1], it[2] + dx, it[3] + dy) + tuple(it[4:]))
        elif kd == "clip":
            dst.items.append((kd, [_move(r_, dx, dy) for r_ in it[1]]))
        elif kd == "unclip":
            dst.items.append(it)
        elif kd == "clipline":
            dst.items.append((kd, [_move(r_, dx, dy) for r_ in it[1]], _move(it[2], dx, dy)) + tuple(it[3:]))


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


# ================================================================ reading the open Rhino file (v2.3)
def curve_pts(g):
    try:
        if isinstance(g, rg.LineCurve):
            return [(g.PointAtStart.X, g.PointAtStart.Y), (g.PointAtEnd.X, g.PointAtEnd.Y)]
        res = g.TryGetPolyline()
        pl = res[1] if isinstance(res, tuple) and res[0] else None
        if pl is not None:
            return [(p.X, p.Y) for p in pl]
        n = int(max(12, min(400, g.GetLength() / 1.0)))
        ts = g.DivideByCount(n, True)
        P = [(g.PointAt(t).X, g.PointAt(t).Y) for t in ts]
        if g.IsClosed:
            P.append(P[0])
        return P
    except Exception:
        return []


def objects_on(doc, pred):
    for lay in doc.Layers:
        if lay.IsDeleted or not pred(lay.FullPath):
            continue
        for o in doc.Objects.FindByLayer(lay) or []:
            yield lay.FullPath, o


def read_areas(doc):
    """v12: {calisma_alan[0] (north), calisma_alan[1] (south)} from layer calisma_alan; {} when it holds none."""
    found = []
    for path, o in objects_on(doc, lambda p: p.split("::")[-1].lower() == CALISMA_LAYER):
        g = o.Geometry
        if isinstance(g, rg.Curve) and (g.IsClosed or g.PointAtStart.DistanceTo(g.PointAtEnd) <= CLOSE_GAP):
            P = ring(curve_pts(g))
            if len(P) >= 3:
                found.append(P)
    return calisma_from(found)


def read_site(doc):
    """v15: the largest closed outline on layer site_alan, else the built-in copy SITE_COPY."""
    found = []
    if doc is not None:
        for path, o in objects_on(doc, lambda p: p.split("::")[-1].lower() == SITE_LAYER):
            g = o.Geometry
            if isinstance(g, rg.Curve) and (g.IsClosed or g.PointAtStart.DistanceTo(g.PointAtEnd) <= CLOSE_GAP):
                P = ring(curve_pts(g))
                if len(P) >= 3:
                    found.append(P)
    return (max(found, key=lambda P: abs(area2(P))), True) if found else (list(SITE_COPY), False)


def calisma_from(found):
    """v12: the two largest outlines, north first, counter-clockwise."""
    big = sorted(found, key=lambda P: -abs(area2(P)))[:2]
    big = sorted(big, key=lambda P: -max(p[1] for p in P))
    out = {}
    for i, P in enumerate(big):
        out["calisma_alan[{}]".format(i)] = P if area2(P) > 0 else P[::-1]
    return out


def in_work(p, areas):
    """v12: True when point p lies inside the working area (any part of calisma_alan)."""
    return any(pip(p[0], p[1], A) for A in areas.values())


def off_work(p, areas):
    """v12: 0 inside the working area, else the distance from p to its nearest outline, m."""
    if in_work(p, areas):
        return 0.0
    best = float("inf")
    for A in areas.values():
        for a, b in zip(A, A[1:] + A[:1]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L2 = dx * dx + dy * dy
            t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2)) if L2 > 0 else 0.0
            best = min(best, math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy))
    return best


def clip_runs(runs, areas):
    """v12: the walk runs cut to the working area, at the runs' vertex resolution."""
    out = []
    for x in runs:
        cur = []
        for p in list(x["P"]) + [None]:
            if p is not None and in_work(p, areas):
                cur.append(tuple(p))
                continue
            if len(cur) >= 2:
                y = dict(x)
                y["P"] = cur
                y["m"] = arclen(cur)[-1]
                out.append(y)
            cur = []
    return out


def read_survey(doc, R):
    """{role: [polyline]} of the survey layers touching rectangle R."""
    out = {}
    for path, o in objects_on(doc, lambda p: p.split("::")[-1] in ROLE_OF):
        g = o.Geometry
        if not isinstance(g, rg.Curve):
            continue
        bb = g.GetBoundingBox(True)
        if bb.Max.X < R[0] or bb.Min.X > R[2] or bb.Max.Y < R[1] or bb.Min.Y > R[3]:
            continue
        P = curve_pts(g)
        if len(P) >= 2:
            out.setdefault(ROLE_OF[path.split("::")[-1]], []).append(P)
    return out


SPOT_LAYER = "NOKTA_TAKEOMETRI"       # v21: the survey's spot heights (tacheometry points, m)


def read_spots(doc, rects):
    """v21: [(x, y, z)] of the survey's spot heights (SPOT_LAYER points) inside any of the rectangles."""
    out = []
    for path, o in objects_on(doc, lambda p: p.split("::")[-1] == SPOT_LAYER):
        g = o.Geometry
        q = getattr(g, "Location", None)
        if q is None or abs(q.Z) < 1e-6:
            continue
        if any(R[0] <= q.X <= R[2] and R[1] <= q.Y <= R[3] for R in rects):
            out.append((q.X, q.Y, q.Z))
    return out


def item_kind(lay):
    if lay.startswith("INT_ZONE_"):
        return "ZONE"
    if lay.startswith("INT_WATER"):
        return "WATER"
    if lay.startswith("INT_LINK_"):
        return "LINK"
    if lay.startswith("INT_REMOVE"):
        return "REMOVE"
    if lay.startswith("INT_ROAD_path") or lay.startswith("INT_PATH"):
        return "PATH"
    return None


def read_items(doc, opt):
    """Zones, strips, arrows, cleared buildings and paths of one option (Option_X::INT_ ...), with their user text
    (the keys zone base v5 writes)."""
    parent = "Option_" + opt + "::"
    items = []
    for path, o in objects_on(doc, lambda p: p.startswith(parent + "INT_")):
        lay = path[len(parent):].split("::")[0]
        if item_kind(lay) is None or not isinstance(o.Geometry, rg.Curve):
            continue
        P = curve_pts(o.Geometry)
        if len(P) < 2:
            continue
        a = o.Attributes
        meta = {}
        for k in ("label", "id", "study_area", "zone", "link"):
            v = a.GetUserString(k)
            if v:
                meta[k] = v
        if "label" not in meta and a.Name:
            meta["label"] = a.Name
        items.append({"layer": parent + lay, "P": [list(p) for p in P], "meta": meta})
    return items


def _decode_block(txt, name):
    """The JSON held as a zlib + base64 string block NAME = ( "..." "..." ) in a script's text."""
    i = txt.index(name + " = (")
    j = txt.index(")", i + len(name) + 4)
    return json.loads(zlib.decompress(base64.b64decode("".join(re.findall(r'"([^"]*)"', txt[i + len(name) + 4:j]))))
                      .decode("utf-8"))


def zone_base_items(path):
    """The zone items of bergama_zone_base_v5.py (its BASE_DATA; v2.3 looked for ZONE_DATA, which v5 does not have)
    or of a .json holding them."""
    txt = open(path, encoding="utf-8").read()
    if path.lower().endswith(".json"):
        data = json.loads(txt)
    else:
        data = None
        for nm in ("BASE_DATA", "ZONE_DATA"):
            if nm + " = (" in txt:
                data = _decode_block(txt, nm)
                break
        if data is None:
            raise ValueError("no BASE_DATA block")
    if isinstance(data, dict):
        data = data.get("items") or data.get("BASE_DATA") or data.get("ZONE_DATA") or []
    return [it for it in data if isinstance(it, dict) and "layer" in it and "P" in it and
            item_kind(it["layer"].split("::")[-1]) is not None]


def zone_base_file(doc, warn):
    """(path, items) of the first readable zone base: the zone_base input, else bergama_zone_base_v5.py or its .json
    next to the .3dm / .gh (and their scripts folders); (None, []) when there is none."""
    cands = []
    v = inp("zone_base")
    if v is not None:
        cands.append(str(v).strip().strip('"'))
    for d in search_dirs(doc):
        for sub in ("", "scripts"):
            for nm in ("bergama_zone_base_v9.py", "bergama_zone_base_v8.py", "bergama_zone_base_v7.py", "bergama_zone_base_v6.py", "bergama_zone_base_v5.py",
                       "zone_base_v5_embedded_data.json"):
                cands.append(os.path.join(d, sub, nm))
    for k, p in enumerate(cands):
        if not os.path.isfile(p):
            if k == 0 and v is not None:
                warn.append(u"zone_base: no file at {}; looked elsewhere".format(p))
            continue
        try:
            items = zone_base_items(p)
            if items:
                return p, items
            warn.append(u"zone base file {} holds no zones in the expected form (layer, P, meta)".format(p))
        except Exception as ex:
            warn.append(u"zone base file {} not read ({}: {})".format(p, type(ex).__name__, ex))
    return None, []


def embedded_items():
    """The zone copy embedded below (zone base v5's BASE_DATA, the kinds drawn here)."""
    return json.loads(zlib.decompress(base64.b64decode("".join(ZONE_COPY))).decode("utf-8"))


def load_palette(dirs, warn):
    """Newer tones from palette/palette.json ("masterplan" > "colours" > key > light, mid, dark; v2.3 read the top
    level, where palette.json 1.4 has no tones, so the file was never used)."""
    for d in dirs:
        for p in (os.path.join(d, "palette.json"), os.path.join(d, "palette", "palette.json")):
            if not os.path.isfile(p):
                continue
            try:
                with open(p, encoding="utf-8") as f:
                    m = json.load(f)
                c = (m.get("masterplan") or {}).get("colours") or m.get("colours") or {}
                for k in MP:
                    if k in c:
                        MP[k] = (c[k]["light"], c[k]["mid"], c[k]["dark"])
                if "building" in c:
                    COL["bld"], COL["bld_edge"] = c["building"]["light"], c["building"]["mid"]
                if "river" in c:
                    COL["river"], COL["river_mid"], COL["river_dark"] = (c["river"]["light"], c["river"]["mid"],
                                                                         c["river"]["dark"])
                if "accent" in c:
                    COL["accent"], COL["accent_dark"] = c["accent"]["mid"], c["accent"]["dark"]
                if "verge" in c:
                    COL["verge"] = c["verge"]["light"]
                if "heritage" in c:
                    COL["her"], COL["her_edge"] = c["heritage"]["light"], c["heritage"]["mid"]
                return p
            except Exception as ex:
                warn.append(u"palette file {} not read ({}); the embedded tones were used".format(p, ex))
    return None


def out_folder(doc):
    # v10 24 Oct: all files under Downloads/Bergama/ (Aras rule); was next to the .3dm / .gh, else Documents
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


# ================================================================ the design of one option (v2.3)
def link_type(tag):
    """The meaning of an INT_LINK layer or user text link from its words (LINK_TYPES), or None."""
    tw = set(re.split(r"[^a-z0-9]+", tag.lower()))
    for k_, d_ in LINK_TYPES.items():
        if tw & set(d_["words"]):
            return k_
    return None


def link_check(kind, a, b):
    """'' when an arrow of `kind` from zone code a to zone code b (None = the river or no zone) follows the brief's
    logic, else what is wrong (masterplan v9)."""
    nm = lambda c_: c_ or "the river (no zone)"
    if kind == "water":
        if (a, b) in WATER_STEPS:
            return ""
        return ("{} -> {} is not a step of the water route (river -> WS storage -> WI agriculture / WT treatment -> "
                "city or back to the river, ideas.txt lines 6, 12 and 26)").format(nm(a), nm(b))
    if kind == "flood":
        if a in (None, "WA") and b in FLOOD_TO:
            return ""
        return ("a high-water arrow runs from the river (no zone, or an amphibious bed WA) into a zone that takes "
                "water ({}); this one runs {} -> {}").format("/".join(FLOOD_TO), nm(a), nm(b))
    if kind == "people":
        w_ = lambda c_: c_ is None or c_ in WATER_SIDE
        if (w_(a) and b in CITY_CODES) or (w_(b) and a in CITY_CODES):
            return ""
        return ("a river-city link joins the water side (a W zone or the river) with a city zone ({}); this one "
                "runs {} -> {}").format("/".join(CITY_CODES), nm(a), nm(b))
    return ""


class Design(object):
    def __init__(self, items, areas, warn, opt):
        self.zones, self.strips, self.links, self.removes, self.paths = [], [], [], [], []
        for it in items:
            lay = it["layer"].split("::")[-1]
            kind = item_kind(lay)
            m = it.get("meta") or {}
            P = [(float(p[0]), float(p[1])) for p in it["P"]]
            if kind is None or len(P) < 2:
                continue
            lab = (m.get("label") or "").upper()
            if kind in ("ZONE", "WATER", "REMOVE"):
                P = ring(P)
                if len(P) < 3:
                    continue
                if area2(P) < 0:
                    P = P[::-1]
                q = inner_pt(P)
                sa = next((k for k, A in areas.items() if pip(q[0], q[1], A)), None)    # v12: the calisma part
                own = (m.get("study_area") or "").split("[")[0]                      # v12: whose words it keeps
                z = {"P": P, "q": q, "area": sa, "own": own, "label": lab, "id": str(m.get("id", "")),
                     "tier": (m.get("zone") or "").upper()[:1], "m2": abs(area2(P)),
                     "code": lay.replace("INT_ZONE_", "")[:2].upper() if kind == "ZONE" else ""}
                if kind == "ZONE" and any(w in lab for w in DROPPED):
                    continue                     # no farmland or farm channel inside the site (CONTEXT §2)
                {"ZONE": self.zones, "WATER": self.strips, "REMOVE": self.removes}[kind].append(z)
            elif kind == "PATH":
                sa = next((k for k, A in areas.items() if any(pip(p[0], p[1], A) for p in P)), None)
                self.paths.append({"P": P, "area": sa, "own": (m.get("study_area") or "").split("[")[0],
                                   "label": lab or u"PATH"})
            else:
                lk = link_type(m.get("link") or lay[len("INT_LINK_"):]) or "other"
                self.links.append({"P": P, "kind": lk, "label": lab,
                                   "heads": LINK_TYPES[lk]["heads"] if lk in LINK_TYPES else 1})


def zone_tones(z):
    lt, md, dk = MP.get(CODE_FAMILY.get(z["code"], "park"))
    if z["code"] == "WA" and z["tier"] == "F":
        lt = mix(lt, COL["white"], 0.5)
    return lt, md, dk


# ================================================================ the base of a drawing (v2.3)
class Near(object):
    """Fast 'inside the working area' and 'within r m of it' tests (edges bucketed in r-sized cells)."""

    def __init__(self, P, r):
        self.P, self.r = P, r
        self.c = c = max(r, 10.0)
        self.cells, self.memo = {}, {}
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            for gi in range(int(math.floor(min(a[0], b[0]) / c)), int(math.floor(max(a[0], b[0]) / c)) + 1):
                for gj in range(int(math.floor(min(a[1], b[1]) / c)), int(math.floor(max(a[1], b[1]) / c)) + 1):
                    self.cells.setdefault((gi, gj), []).append((a, b))
        self.bb = bbox(P)

    def inside(self, x, y):
        b = self.bb
        if x < b[0] or x > b[2] or y < b[1] or y > b[3]:
            return False
        k = (int(math.floor(x / self.c)), int(math.floor(y / self.c)))
        if k not in self.cells:                          # no edge crosses this cell: one answer for all of it
            if k not in self.memo:
                self.memo[k] = pip(x, y, self.P)
            return self.memo[k]
        return pip(x, y, self.P)

    def within(self, x, y):
        b, r = self.bb, self.r
        if x < b[0] - r or x > b[2] + r or y < b[1] - r or y > b[3] + r:
            return False
        gi, gj = int(math.floor(x / self.c)), int(math.floor(y / self.c))
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for a, e in self.cells.get((gi + di, gj + dj), ()):
                    if seg_dist(x, y, a, e) <= r:
                        return True
        return self.inside(x, y)


class View(object):
    """Alternative 3: the corridor of all working areas turned so its long axis runs left to right, the upstream
    entry on the left (the water runs left to right), plus the ring. Graphic: north is shown by an arrow."""

    def __init__(self, areas, ring_m, k, frame=None):
        pts = list(frame) if frame else [p for A in areas.values() for p in A]   # v15: frame = site_alan
        self.cx, self.cy = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
        a = math.radians(principal_angle(pts))
        self.c, self.s = math.cos(a), math.sin(a)
        if "calisma_alan[0]" in areas and "calisma_alan[1]" in areas:     # v12: north part = upstream
            up = sum(self.uv(p)[0] for p in areas["calisma_alan[0]"]) / len(areas["calisma_alan[0]"])
            dn = sum(self.uv(p)[0] for p in areas["calisma_alan[1]"]) / len(areas["calisma_alan[1]"])
            if up > dn:
                self.c, self.s = -self.c, -self.s
        U = [self.uv(p) for p in pts]
        self.u0, self.u1 = min(u for u, v in U) - ring_m, max(u for u, v in U) + ring_m
        self.v0, self.v1 = min(v for u, v in U) - ring_m, max(v for u, v in U) + ring_m
        self.k = k
        self.W, self.H = (self.u1 - self.u0) * k, (self.v1 - self.v0) * k
        corners = [self.xy(u, v) for u, v in ((self.u0, self.v0), (self.u1, self.v0), (self.u1, self.v1),
                                              (self.u0, self.v1))]
        self.P = corners
        self.bb = bbox(corners)

    def uv(self, p):
        dx, dy = p[0] - self.cx, p[1] - self.cy
        return dx * self.c + dy * self.s, -dx * self.s + dy * self.c

    def xy(self, u, v):
        return self.cx + u * self.c - v * self.s, self.cy + u * self.s + v * self.c

    def T(self, p):
        u, v = self.uv(p)
        return (u - self.u0) * self.k, (v - self.v0) * self.k

    def inside(self, x, y):
        u, v = self.uv((x, y))
        return self.u0 <= u <= self.u1 and self.v0 <= v <= self.v1

    within = inside


def faces(polys, snap=0.02, max_area=30000.0):
    """Closed footprints from loose survey segments: the bounded faces of the planar graph (shared walls of row
    houses work; courtyards come out as faces too and are cut out by the even-odd fill)."""
    key = lambda p: (int(round(p[0] / snap)), int(round(p[1] / snap)))
    segs = [(a, b) for P in polys for a, b in zip(P[:-1], P[1:])]
    ends, G = {}, 5.0                                    # T-junctions: split a segment where another one ends on it
    for a, b in segs:
        for p in (a, b):
            ends.setdefault((int(p[0] // G), int(p[1] // G)), {})[key(p)] = p
    split = []
    for a, b in segs:
        ka, kb = key(a), key(b)
        L2 = (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
        if L2 < snap * snap:
            continue
        on = []
        for gi in range(int(min(a[0], b[0]) // G), int(max(a[0], b[0]) // G) + 1):
            for gj in range(int(min(a[1], b[1]) // G), int(max(a[1], b[1]) // G) + 1):
                for kp, p in ends.get((gi, gj), {}).items():
                    if kp in (ka, kb):
                        continue
                    t = ((p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])) / L2
                    if 0.0 < t < 1.0 and seg_dist(p[0], p[1], a, b) <= snap:
                        on.append((t, p))
        pts = [a] + [p for t, p in sorted(on)] + [b]
        split += list(zip(pts[:-1], pts[1:]))
    pos, adj = {}, {}
    for a, b in split:
        ka, kb = key(a), key(b)
        if ka == kb:
            continue
        pos.setdefault(ka, a)
        pos.setdefault(kb, b)
        adj.setdefault(ka, set()).add(kb)
        adj.setdefault(kb, set()).add(ka)
    stack = [k for k, s in adj.items() if len(s) < 2]
    while stack:                                         # loose ends cannot bound a face
        k = stack.pop()
        s = adj.pop(k, None)
        for n in s or ():
            t = adj.get(n)
            if t is not None:
                t.discard(k)
                if len(t) < 2:
                    stack.append(n)
    order, idx = {}, {}
    for k, s in adj.items():
        x, y = pos[k]
        order[k] = sorted(s, key=lambda n: math.atan2(pos[n][1] - y, pos[n][0] - x))
        idx[k] = dict((n, i) for i, n in enumerate(order[k]))
    used, out = set(), []
    for u in order:
        for v in order[u]:
            if (u, v) in used:
                continue
            R, a, b = [], u, v
            while (a, b) not in used and len(R) < 20000:
                used.add((a, b))
                R.append(pos[a])
                nb = order[b]
                a, b = b, nb[(idx[b][a] - 1) % len(nb)]
            if 0.5 < area2(R) < max_area:
                out.append(R)
    return out


def cut_runs(P, test, step=LINE_STEP_M):
    """The parts of polyline P where test(x, y) holds, sampled every `step` m."""
    runs, run = [], []
    for i in range(len(P) - 1):
        a, b = P[i], P[i + 1]
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
        for j in range(n + (1 if i == len(P) - 2 else 0)):
            t = j / float(n)
            p = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
            if test(p[0], p[1]):
                run.append(p)
            else:
                if len(run) >= 2:
                    runs.append(run)
                run = []
    if len(run) >= 2:
        runs.append(run)
    return runs


def prep_base(survey, nr, R, full=False):
    """The survey within test nr (a working area's ring, or the corridor of alternative 3) inside rectangle R:
    footprints as faces (whole when any corner is within), street and stream lines and the line work drawn on top,
    cut at the edge; full = also contours and bank lines (alternative 3)."""
    inR = lambda P: any(R[0] <= p[0] <= R[2] and R[1] <= p[1] <= R[3] for p in P)
    base = {"faces": {}, "lines": [], "streets": [], "streams": [], "contours": [], "contours10": [], "banks": [],
            "streets_all": []}
    for role, max_a in (("park", 400000.0), ("pond", 50000.0), ("housing", 30000.0), ("building", 30000.0),
                        ("heritage", 30000.0)):
        polys = [P for P in survey.get(role, []) if inR(P)]
        base["faces"][role] = [F for F in faces(polys, max_area=max_a) if any(nr.within(p[0], p[1]) for p in F)]
    for role in ("road", "kerb"):
        for P in survey.get(role, []):
            if inR(P):
                base["streets"] += cut_runs(P, nr.within)
                base["streets_all"].append(P)           # v21: the whole street network of the drawing
    styles = {"histwall": ("histwall", 0.30, [1.2, 0.5]), "stream": ("river_mid", 0.22, None),
              "bridge": ("ink", 0.35, None)}
    for role in ("stream", "histwall", "bridge"):
        ck, lw, dash = styles[role]
        for P in survey.get(role, []):
            if inR(P):
                for r_ in cut_runs(P, nr.within):
                    base["lines"].append((ck, lw, dash, r_))
                    if role == "stream":
                        base["streams"].append(r_)
    if full:
        for role, key in (("contour", "contours"), ("contour10", "contours10"), ("bank", "banks"),
                          ("bank_top", "banks"), ("chan_top", "banks")):
            for P in survey.get(role, []):
                if inR(P):
                    base[key] += cut_runs(P, nr.within, 2.0)
    base["near"], base["R"] = nr, R
    return base


# ================================================================ links between shapes (v2.3)
def link_shapes(L, shapes, near=30.0):
    """The shape (zone or strip) a link starts in and the one it ends in (holding the end, else nearest)."""
    def at(e, skip=None):
        for z in shapes:
            if z is not skip and pip(e[0], e[1], z["P"]):
                return z
        best, bd = None, near
        for z in shapes:
            if z is skip:
                continue
            d = min(seg_dist(e[0], e[1], a, b) for a, b in zip(thin(z["P"]), thin(z["P"])[1:] + thin(z["P"])[:1]))
            if d < bd:
                best, bd = z, d
        return best
    a = at(L["P"][0])
    return a, at(L["P"][-1], skip=a)


# ================================================================ the flowing puzzle (v2.3; Nil 2026-10-18 19:00)
# Every space of the working area and its ring is one puzzle piece, grown on one grid from its surveyed or zone
# base shape. A piece spreads beyond its shape by GROW_M x its extroversion, with a front that wanders more the more
# extrovert it is (liquid); introvert pieces keep their shape (solid). Housing is closed: nothing enters it except the
# streets, which reach into it slowly. Where the zone base links two zones, the giving zone sends a tongue into the
# receiving one, so the pieces interlock. Graphic reading only: extroversion values are set in EXTRO, not measured.
# v10 (alternative 2): every programme piece is also grown on its own ("free"), so pieces overlap where they reach
# into each other; the cells most of them cover ("meet") carry the commons' words.

EXTRO = {  # kind: (extroversion 0 introvert ... 1 extrovert, legend)
    "river": (1.00, u"STREAM"),
    "W": (0.95, u"WET BED ZONES"), "F": (0.80, u"FLOOD TERRACE ZONES"), "D": (0.65, u"DRY TOP ZONES"),
    "cleared": (0.55, u"CLEARED GROUND"),
    "street": (0.60, u"STREETS"),
    "park": (0.50, u"PARKS"),
    "heritage": (0.30, u"HERITAGE"),
    "building": (0.12, u"OTHER BUILDINGS"),
    "housing": (0.00, u"HOUSING"),
}
FEED_BONUS = 0.08            # per zone base link a zone gives: the feeding zone flows outward more
GROW_M = 12.0                # how far the most extrovert piece spreads beyond its shape, m (graphic)
STREET_M = 4.5               # a street grows this far from its surveyed kerb / road lines, m (fills the carriageway)
HOUSING_CLOSE_M = 1.0        # housing grows this far: closes the gaps between joined houses into one solid block
TONGUE_M = 28.0              # longest tongue a giving zone sends into the zone it feeds, m
MAX_CELLS = 170000           # grid cells per working area (cell size follows from it, at least 0.5 m)
BAND_CELLS = 600000          # v18: grid cells of the corridor-wide grid of the broad zones of alternative 3
SPINE_ZONE_M = 10.0          # v18: a spine zone reaches this far either side of its route, m (graphic default)
BAND_E = 0.6                 # v18: how much the broad zones' edges wander (alternative 2's growth, 0-1)
RIVER_BAND_TONE = ("C4CCB5", "89986A", "3C4733")   # v18: sage, palette reference 89986A (light = mixed 1:1 with white)
RIVER_BAND_NAME = u"PROMENADE"   # v19: one catchy word for Aras's "function/circulation area" (16:39, 16:41)
RIVER_BAND_WORDS = [u"VIEWPOINTS", u"TERRACES", u"WALK PATHS", u"RAMPS", u"CAFES"]   # his words, 16:39
PIECE_TONE = {"river": ("91ADB4", "5D7F8D", "32525F"), "street": ("CFCCC5", "847E75", "4A3F35"),   # v21: road role
              "park": ("DFEBC0", "A7B67F", "49522B"), "heritage": ("E4CAC9", "AF7474", "4C2528"),
              "building": ("D8D5CC", "B0AC9C", "847E75"), "housing": ("D9CDAE", "BFB08F", "594B2E"),
              "cleared": ("F6F4EE", "B0AC9C", "4A3F35")}
FADE_RING = 0.55             # pieces in the ring (outside the working area) are mixed this much with white


def _noise(i):
    """A smooth wandering field for piece i (three crossing waves, deterministic)."""
    r = [math.sin((i + 1) * 12.9898 + j * 78.233) * 43758.5453 for j in range(9)]
    r = [x - math.floor(x) for x in r]
    W = [(2 * math.pi / (17.0 + 9.0 * r[0]), r[1] * 6.283, r[2] * 6.283),
         (2 * math.pi / (29.0 + 11.0 * r[3]), r[4] * 6.283, r[5] * 6.283),
         (2 * math.pi / (43.0 + 13.0 * r[6]), r[7] * 6.283, r[8] * 6.283)]
    D = [(math.cos(t), math.sin(t), w, ph) for w, t, ph in W]
    return lambda x, y: sum(math.sin(w * (cx * x + cy * y) + ph) for cx, cy, w, ph in D) / 3.0


class Grid(object):
    def __init__(self, R, nr, cells=MAX_CELLS):
        self.c = c = max(0.5, math.sqrt((R[2] - R[0]) * (R[3] - R[1]) / float(cells)))
        self.x0, self.y0 = R[0], R[1]
        self.nx, self.ny = int((R[2] - R[0]) / c) + 1, int((R[3] - R[1]) / c) + 1
        self.valid = bytearray(self.nx * self.ny)
        self.inside = bytearray(self.nx * self.ny)
        for j in range(self.ny):
            y = self.y0 + (j + 0.5) * c
            for i in range(self.nx):
                x = self.x0 + (i + 0.5) * c
                if nr.within(x, y):
                    self.valid[j * self.nx + i] = 1
                    if nr.inside(x, y):
                        self.inside[j * self.nx + i] = 1

    def xy(self, n):
        return self.x0 + (n % self.nx + 0.5) * self.c, self.y0 + (n // self.nx + 0.5) * self.c

    def poly_cells(self, P):
        """Cells whose centre lies in ring P (scanline)."""
        out = []
        b = bbox(P)
        j0, j1 = max(0, int((b[1] - self.y0) / self.c)), min(self.ny - 1, int((b[3] - self.y0) / self.c) + 1)
        E = list(zip(P, P[1:] + P[:1]))
        for j in range(j0, j1 + 1):
            y = self.y0 + (j + 0.5) * self.c
            xs = sorted(a[0] + (y - a[1]) * (e[0] - a[0]) / (e[1] - a[1]) for a, e in E
                        if (a[1] > y) != (e[1] > y))
            for k in range(0, len(xs) - 1, 2):
                i0 = max(0, int(math.ceil((xs[k] - self.x0) / self.c - 0.5)))
                i1 = min(self.nx - 1, int(math.floor((xs[k + 1] - self.x0) / self.c - 0.5)))
                out += range(j * self.nx + i0, j * self.nx + i1 + 1)
        return out

    def line_cells(self, P):
        out = set()
        for a, b in zip(P[:-1], P[1:]):
            n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / (self.c * 0.5)))
            for t in range(n + 1):
                x, y = a[0] + (b[0] - a[0]) * t / n, a[1] + (b[1] - a[1]) * t / n
                i, j = int((x - self.x0) / self.c), int((y - self.y0) / self.c)
                if 0 <= i < self.nx and 0 <= j < self.ny:
                    out.add(j * self.nx + i)
        return out


def zone_extro(z, n_out):
    return min(1.0, EXTRO.get(z["tier"] or "D", EXTRO["D"])[0] + FEED_BONUS * n_out)


def puzzle(base, D, key):
    """Grow all pieces of one working area on one grid -> list of pieces with their outline loops (world m): the
    partition (context, zone and hub pieces) and, for alternative 2, the free zone pieces and their meeting cells."""
    G = Grid(base["R"], base["near"])
    zones = [z for z in D.zones if z["area"] == key]
    strips = [s for s in D.strips if any(base["near"].within(p[0], p[1]) for p in thin(s["P"], 60))]
    removes = [r for r in D.removes if r["area"] == key]
    pieces = []

    def piece(kind, e, g, zone=None):
        pieces.append({"kind": kind, "e": e, "g": g, "zone": zone, "seeds": {}, "noise": _noise(len(pieces))})
        return pieces[-1]

    def seed(pc, cells, cost):
        s = pc["seeds"]
        for n in cells:
            if G.valid[n] and cost < s.get(n, 1e9):
                s[n] = cost
    gives = {}
    for L in D.links:
        a, b = link_shapes(L, zones + strips)
        if a is not None and b is not None and a is not b:
            gives.setdefault(id(a), []).append((b, L))
    fc = base["faces"]
    hs = piece("housing", EXTRO["housing"][0], HOUSING_CLOSE_M)
    for F in fc.get("housing", []):
        seed(hs, G.poly_cells(F), -hs["g"])
    bl = piece("building", EXTRO["building"][0], HOUSING_CLOSE_M)
    for F in fc.get("building", []):
        seed(bl, G.poly_cells(F), -bl["g"])
    for kind in ("heritage", "park"):
        e = EXTRO[kind][0]
        pc = piece(kind, e, e * GROW_M * 0.5)
        for F in fc.get(kind, []):
            seed(pc, G.poly_cells(F), -pc["g"])
    st = piece("street", EXTRO["street"][0], STREET_M)
    for P in base["streets"]:
        seed(st, G.line_cells(P), -st["g"])
    rv = piece("river", EXTRO["river"][0], EXTRO["river"][0] * GROW_M)
    for s in strips:
        seed(rv, G.poly_cells(s["P"]), -rv["g"])
    for P in base["streams"]:
        seed(rv, G.line_cells(P), -rv["g"] * 0.6)
    for F in fc.get("pond", []):
        seed(rv, G.poly_cells(F), -rv["g"] * 0.5)
    for r in removes:
        pc = piece("cleared", EXTRO["cleared"][0], EXTRO["cleared"][0] * GROW_M * 0.4)
        seed(pc, G.poly_cells(r["P"]), -pc["g"])
    zp = {}
    for z in zones:
        e = zone_extro(z, len(gives.get(id(z), [])))
        pc = piece("zone", e, e * GROW_M, z)
        seed(pc, G.poly_cells(z["P"]), -pc["g"])
        zp[id(z)] = pc
    for s in strips:
        zp[id(s)] = rv
    for z in zones + strips:                             # the giving zone reaches into the zone it feeds
        src = zp.get(id(z))
        for b, L in gives.get(id(z), []):
            TA, TB = thin(z["P"]), thin(b["P"])
            p, q, d = closest_pair(TA, TB)
            pa, pb = inner_pt(TA, 10), inner_pt(TB, 10)
            u = (pb[0] - pa[0], pb[1] - pa[1]) if d < 0.5 else (q[0] - p[0], q[1] - p[1])
            Lu = math.hypot(u[0], u[1]) or 1.0
            u = (u[0] / Lu, u[1] / Lu)
            ext = [x * u[0] + y * u[1] for x, y in TB]
            ln = min(TONGUE_M, 0.45 * (max(ext) - min(ext)))
            line = [(p[0] - u[0] * 3.0, p[1] - u[1] * 3.0), (q[0] + u[0] * ln, q[1] + u[1] * ln)]
            seed(src, G.line_cells(line), -src["g"] - 2.0)
    # ---- multi-source growth (Dijkstra on the grid): the lowest cost claims the cell
    N = G.nx * G.ny
    best = [1e18] * N
    lab = [-1] * N
    prot = bytearray(N)
    for n in hs["seeds"]:
        prot[n] = 1
    hp = []
    for li, pc in enumerate(pieces):
        for n, c0 in pc["seeds"].items():
            if c0 < best[n]:
                best[n], lab[n] = c0, li
    for n in range(N):
        if lab[n] >= 0:
            hp.append((best[n], n, lab[n]))
    heapq.heapify(hp)
    c, nx = G.c, G.nx
    nbr = [(1, 0, c), (-1, 0, c), (0, 1, c), (0, -1, c), (1, 1, c * 1.4142), (-1, 1, c * 1.4142),
           (1, -1, c * 1.4142), (-1, -1, c * 1.4142)]
    amp = [0.8 * pc["e"] for pc in pieces]
    street_i, housing_i = pieces.index(st), pieces.index(hs)
    while hp:
        cost, n, li = heapq.heappop(hp)
        if cost > best[n] or lab[n] != li:
            continue
        i, j = n % nx, n // nx
        x, y = G.xy(n)
        f = 1.0 + amp[li] * pieces[li]["noise"](x, y)
        for di, dj, w in nbr:
            ii, jj = i + di, j + dj
            if ii < 0 or jj < 0 or ii >= nx or jj >= G.ny:
                continue
            m = jj * nx + ii
            if not G.valid[m]:
                continue
            step = w * f
            if prot[m] and li != housing_i:
                if li != street_i:
                    continue                             # housing is closed to everything but the streets
                step *= 3.0
            nc = cost + step
            if nc < best[m] and nc <= 0.0:
                best[m], lab[m] = nc, li
                heapq.heappush(hp, (nc, m, li))
    # ---- the commons: programme cells within reach of 3 (else 2) programme pieces become one darker piece
    fn = [li for li, pc in enumerate(pieces) if pc["kind"] == "zone"]
    if len(fn) >= 2 and key in HUB:
        rv_i = pieces.index(rv)
        layers = int(HUB_R_M[0] / c) + 1
        dist = {}
        for li in fn + [rv_i]:
            d = bytearray([255]) * N
            fr = [n for n in range(N) if lab[n] == li]
            for n in fr:
                d[n] = 0
            for L_ in range(1, layers + 1):
                nf = []
                for n in fr:
                    i, j = n % nx, n // nx
                    for di, dj, _w in nbr:
                        ii, jj = i + di, j + dj
                        if 0 <= ii < nx and 0 <= jj < G.ny:
                            m = jj * nx + ii
                            if d[m] == 255:
                                d[m] = L_
                                nf.append(m)
                fr = nf
            dist[li] = d
        prog = [n for n in range(N) if lab[n] in fn and G.inside[n]]
        hub = []
        for need in (3, 2):
            for r_m in HUB_R_M:
                r = int(r_m / c)
                hub = [n for n in prog if sum(1 for li in dist if dist[li][n] <= r) >= need]
                if hub and len(hub) <= HUB_MAX * len(prog):
                    break
                hub = []
            if hub:
                break
        if hub:
            fam = {}
            for n in hub:
                f_ = MP[CODE_FAMILY.get(pieces[lab[n]]["zone"]["code"], "park")][1]
                fam[f_] = fam.get(f_, 0) + 1
            tot = float(sum(fam.values()))
            rgb = [sum(hex_rgb(f_)[q] * v for f_, v in fam.items()) / tot for q in range(3)]
            md = "".join("{:02X}".format(int(round(255 * x))) for x in rgb)
            dk = mix(md, COL["ink_dark"], 0.45)
            pieces.append({"kind": "hub", "e": 0.9, "zone": None, "tone": (dk, md, COL["white"]),
                           "name": HUB[key][0], "words": HUB[key][1]})
            hi = len(pieces) - 1
            for n in hub:
                lab[n] = hi
    # ---- v10, alternative 2: every programme piece grown on its own (same costs, housing still closed)
    free = {}
    for li in fn:
        bst = dict(pieces[li]["seeds"])
        hq = [(c0, n) for n, c0 in bst.items()]
        heapq.heapify(hq)
        while hq:
            cost, n = heapq.heappop(hq)
            if cost > bst.get(n, 1e18):
                continue
            i, j = n % nx, n // nx
            x, y = G.xy(n)
            f = 1.0 + amp[li] * pieces[li]["noise"](x, y)
            for di, dj, w in nbr:
                ii, jj = i + di, j + dj
                if ii < 0 or jj < 0 or ii >= nx or jj >= G.ny:
                    continue
                m = jj * nx + ii
                if not G.valid[m] or prot[m]:
                    continue
                nc = cost + w * f
                if nc <= 0.0 and nc < bst.get(m, 1e18):
                    bst[m] = nc
                    heapq.heappush(hq, (nc, m))
        free[li] = set(bst)
    cnt = {}
    for li, S_ in free.items():
        for n in S_:
            if G.inside[n]:
                cnt[n] = cnt.get(n, 0) + 1
    meet = []
    for need in (3, 2):
        meet = [n for n, v in cnt.items() if v >= need]
        if len(meet) * c * c >= HUB_MIN_M2:
            break
        meet = []
    # ---- outlines: one set of loops per piece and side (in the working area / in the ring)
    groups = {}
    for n in range(N):
        if lab[n] >= 0:
            groups.setdefault((lab[n], 1 if pieces[lab[n]]["kind"] in ("zone", "hub") else G.inside[n]),
                              []).append(n)
    out = []
    for li, pc in enumerate(pieces):
        for ins in (1, 0):
            cells = groups.get((li, ins))
            if not cells:
                continue
            loops = trace(G, set(cells))
            tol, it = (c * 0.6, 0) if pc["e"] < 0.2 else (c * 0.9, 2 if pc["e"] < 0.5 else 4)   # solid .. liquid
            loops = [smooth(Lp, tol, it) for Lp in loops if len(Lp) >= 4]
            loops = [Lp for Lp in loops if len(Lp) >= 3 and abs(area2(Lp)) >
                     (HUB_MIN_M2 if pc["kind"] == "hub" else 2.0 * c * c)]
            if loops:
                out.append({"kind": pc["kind"], "e": pc["e"], "zone": pc["zone"], "inside": bool(ins),
                            "loops": loops, "m2": len(cells) * c * c, "tone": pc.get("tone"),
                            "name": pc.get("name"), "words": pc.get("words")})
    for li, S_ in free.items():
        pc = pieces[li]
        loops = [smooth(Lp, c * 0.9, 2 if pc["e"] < 0.5 else 4) for Lp in trace(G, S_) if len(Lp) >= 4]
        loops = [Lp for Lp in loops if len(Lp) >= 3 and abs(area2(Lp)) > 2.0 * c * c]
        if loops:
            out.append({"kind": "free", "e": pc["e"], "zone": pc["zone"], "inside": True, "loops": loops,
                        "m2": len(S_) * c * c})
    if meet and key in HUB:
        fam = {}
        for n in meet:
            for li, S_ in free.items():
                if n in S_:
                    f_ = MP[CODE_FAMILY.get(pieces[li]["zone"]["code"], "park")][1]
                    fam[f_] = fam.get(f_, 0) + 1
        tot = float(sum(fam.values()))
        md = "".join("{:02X}".format(int(round(255 * sum(hex_rgb(f_)[q] * v for f_, v in fam.items()) / tot)))
                     for q in range(3))
        loops = [smooth(Lp, c * 0.9, 2) for Lp in trace(G, set(meet)) if len(Lp) >= 4]
        loops = [Lp for Lp in loops if len(Lp) >= 3 and abs(area2(Lp)) > HUB_MIN_M2]
        if loops:
            out.append({"kind": "meet", "e": 0.9, "zone": None, "inside": True, "loops": loops,
                        "m2": len(meet) * c * c, "tone": (mix(md, COL["ink_dark"], 0.45), md, COL["white"]),
                        "name": HUB[key][0], "words": HUB[key][1]})
    return out


def grow_band(G, lines, polys, g, ni, opt):
    """v18: one broad zone grown on grid G from lines and shapes (world m), up to g m out, its edge wandering like
    alternative 2's pieces (noise ni) -> outer loops, holes filled; option A liquid, option B faceted."""
    N = G.nx * G.ny
    best = [1e18] * N
    cells = set()
    for P in lines:
        cells |= G.line_cells(P)
    for P in polys:
        cells.update(G.poly_cells(P))
    hp = [(-g, n) for n in cells if G.valid[n]]
    for _, n in hp:
        best[n] = -g
    heapq.heapify(hp)
    nz, amp, c, nx = _noise(ni), 0.8 * BAND_E, G.c, G.nx
    nbr = [(1, 0, c), (-1, 0, c), (0, 1, c), (0, -1, c), (1, 1, c * 1.4142), (-1, 1, c * 1.4142),
           (1, -1, c * 1.4142), (-1, -1, c * 1.4142)]
    while hp:
        cost, n = heapq.heappop(hp)
        if cost > best[n]:
            continue
        i, j = n % nx, n // nx
        x, y = G.xy(n)
        f = 1.0 + amp * nz(x, y)
        for di, dj, w in nbr:
            ii, jj = i + di, j + dj
            if ii < 0 or jj < 0 or ii >= nx or jj >= G.ny:
                continue
            m = jj * nx + ii
            nc = cost + w * f
            if G.valid[m] and nc < best[m] and nc <= 0.0:
                best[m] = nc
                heapq.heappush(hp, (nc, m))
    S = set(n for n in range(N) if best[n] <= 0.0)
    loops = [Lp for Lp in trace(G, S) if len(Lp) >= 4 and area2(Lp) > 0.0]
    loops = [dp(Lp, c * 3.0) if opt == "B" else smooth(Lp, c * 0.9, 4) for Lp in loops]
    return [Lp for Lp in loops if len(Lp) >= 3 and abs(area2(Lp)) > 50.0 * c * c]


def trace(G, S):
    """Outline loops of a cell set (cell edges, the set on the left; holes come out clockwise)."""
    c, nx, x0, y0 = G.c, G.nx, G.x0, G.y0
    nxt = {}
    for n in S:
        i, j = n % nx, n // nx
        if (j - 1) * nx + i not in S or j == 0:
            nxt.setdefault((i, j), []).append((i + 1, j))
        if i + 1 >= nx or j * nx + i + 1 not in S:
            nxt.setdefault((i + 1, j), []).append((i + 1, j + 1))
        if (j + 1) * nx + i not in S:
            nxt.setdefault((i + 1, j + 1), []).append((i, j + 1))
        if i == 0 or j * nx + i - 1 not in S:
            nxt.setdefault((i, j + 1), []).append((i, j))
    loops = []
    while nxt:
        start = next(iter(nxt))
        Lp, p, prev = [], start, None
        while True:
            outs = nxt.get(p)
            if not outs:
                break
            if len(outs) > 1 and prev is not None:       # pinch corner: turn left first (keeps loops simple)
                dx, dy = p[0] - prev[0], p[1] - prev[1]
                left = (p[0] - dy, p[1] + dx)
                q = left if left in outs else outs[0]
            else:
                q = outs[0]
            outs.remove(q)
            if not outs:
                del nxt[p]
            Lp.append((x0 + p[0] * c, y0 + p[1] * c))
            prev, p = p, q
            if p == start:
                break
        if len(Lp) >= 4:
            loops.append(Lp)
    return loops


def dp(P, tol):
    """Douglas-Peucker on a closed loop (drops the cell staircase)."""
    if len(P) < 5:
        return P
    k = max(range(len(P)), key=lambda i: (P[i][0] - P[0][0]) ** 2 + (P[i][1] - P[0][1]) ** 2)

    def run(Q):
        keep = [0, len(Q) - 1]
        st = [(0, len(Q) - 1)]
        while st:
            a, b = st.pop()
            dmax, im = 0.0, None
            for i in range(a + 1, b):
                d = seg_dist(Q[i][0], Q[i][1], Q[a], Q[b])
                if d > dmax:
                    dmax, im = d, i
            if im is not None and dmax > tol:
                keep.append(im)
                st += [(a, im), (im, b)]
        return [Q[i] for i in sorted(keep)]
    A_ = run(P[:k + 1])
    B_ = run(P[k:] + P[:1])
    return A_[:-1] + B_[:-1]


def smooth(P, tol, it):
    Q = [((P[i][0] + P[(i + 1) % len(P)][0]) / 2, (P[i][1] + P[(i + 1) % len(P)][1]) / 2) for i in range(len(P))]
    Q = dp(Q, tol)
    return chaikin(Q, it, closed=True) if len(Q) >= 3 else Q


def piece_tone(pc):
    if pc["kind"] in ("hub", "meet"):
        return pc["tone"]
    if pc["kind"] in ("zone", "free"):
        return zone_tones(pc["zone"])
    lt, md, dk = PIECE_TONE[pc["kind"]]
    if not pc["inside"]:
        lt = mix(lt, COL["white"], FADE_RING)
    return lt, md, dk



# ================================================================ words inside pieces (v2.3)
def box_in(TP, b, vb=None):
    """Box b lies inside ring TP (9 sample points inside, no ring vertex inside the box)."""
    for x in (b[0], (b[0] + b[2]) / 2, b[2]):
        for y in (b[1], (b[1] + b[3]) / 2, b[3]):
            if not pip(x, y, TP):
                return False
    for p in (vb if vb is not None else TP):
        if b[0] < p[0] < b[2] and b[1] < p[1] < b[3]:
            return False
    return True


def box_clear(b, avoid):
    """v10: box b keeps off the rings in avoid (the commons drawn over the zones of alternative 3)."""
    for A_ in avoid:
        ab = A_[1]
        if not hit(b, ab):
            continue
        for x in (b[0], (b[0] + b[2]) / 2, b[2]):
            for y in (b[1], (b[1] + b[3]) / 2, b[3]):
                if pip(x, y, A_[0]):
                    return False
        for p in A_[0]:
            if b[0] < p[0] < b[2] and b[1] < p[1] < b[3]:
                return False
    return True


def inside_spots(TP, n=16):
    bx = bbox(TP)
    pole = inner_pt(TP)
    S = []
    for i in range(n):
        for j in range(n):
            x = bx[0] + (i + 0.5) / n * (bx[2] - bx[0])
            y = bx[1] + (j + 0.5) / n * (bx[3] - bx[1])
            if pip(x, y, TP):
                S.append((x, y))
    S.sort(key=lambda p: (p[0] - pole[0]) ** 2 + (p[1] - pole[1]) ** 2)
    return [pole] + S


def spread(spots, placed):
    """Spots ordered so a word lands as far as possible from the words already in its piece."""
    if not placed:
        return spots
    return sorted(spots, key=lambda p: -min((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 for q in placed))


def block_size(lines):
    """lines: [(text, size, bold)] -> (w, h)."""
    w = max(text_w(s, sz, bd) for s, sz, bd in lines)
    h = sum(sz * 1.18 for s, sz, bd in lines)
    return w, h


def draw_block(pg, lines, x0, y_top, colour, halo):
    y = y_top
    for s, sz, bd in lines:
        y -= sz * 1.0
        pg.text(s, x0, y, sz, colour, bold=bd, halo=halo)
        y -= sz * 0.18


def fit_inside(TP, spots, lines, taken, pad=0.6, avoid=()):
    w, h = block_size(lines)
    bx = bbox(TP)
    if w + 2 * pad > bx[2] - bx[0] or h + 2 * pad > bx[3] - bx[1]:
        return None
    for (x, y) in spots:
        b = (x - w / 2 - pad, y - h / 2 - pad, x + w / 2 + pad, y + h / 2 + pad)
        if any(hit(b, t) for t in taken):
            continue
        if box_in(TP, b) and (not avoid or box_clear(b, avoid)):
            return b
    return None


def subs_for(z, owner, key, opt):
    rows = [r for r in SUBS if r[0] == owner and r[1] == z["code"]]
    if z["tier"]:
        rows = [r for r in rows if r[2] == z["tier"]] or ([] if len(set(r[2] for r in rows)) > 1 else rows)
    elif len(set(r[2] for r in rows)) > 1:
        rows = []
    out = []
    for r in rows:
        if r[3] in (None, opt, key):
            out += r[4]
    return out


def name_of(z, owner):
    for (o_, c_, t_), nm in NAMES.items():
        if o_ == owner and c_ == z["code"] and t_ in (None, z["tier"]):
            return nm
    return z["label"] or z["code"]


def sig_of(z, owner):
    return next((v for (o_, c_, t_), v in SIG.items() if o_ == owner and c_ == z["code"] and t_ in (None, z["tier"])),
                0.6)


def zone_words(pg, z, TP, owner, key, opt, taken, seen, avoid=(), halo=None):
    """The zone's keyword name (size by SIG) and its sourced keywords scattered inside TP; what does not fit at the
    smallest size is left out (v2.3: no callouts)."""
    dk = zone_tones(z)[2]
    TPs = thin(TP, 300)
    spots = inside_spots(TPs)
    placed = []
    f = sig_of(z, owner)
    bw = max(18.0, (bbox(TPs)[2] - bbox(TPs)[0]) * 0.8)
    for sz in [7.5 * f * t for t in STEPS]:
        lines = [(s_, sz, True) for s_ in wrap(name_of(z, owner), sz, bw, True)]
        b = fit_inside(TPs, spots, lines, taken, avoid=avoid)
        if b:
            draw_block(pg, lines, b[0] + 0.6, b[3] - 0.6, dk, halo)
            taken.append(b)
            placed.append(((b[0] + b[2]) / 2, (b[1] + b[3]) / 2))
            break
    kind_key = (key, z["code"], z["tier"])
    words = subs_for(z, owner, key, opt) if kind_key not in seen else []
    seen.add(kind_key)
    for w_ in words:
        for sz in [3.4 * f * t for t in STEPS]:
            b = fit_inside(TPs, spread(spots, placed), [(w_, sz, False)], taken, pad=1.0 * sz, avoid=avoid)
            if b:
                pg.text(w_, b[0] + 1.0 * sz, b[1] + 1.0 * sz + 0.06 * sz, sz, dk, halo=halo)
                taken.append(b)
                placed.append(((b[0] + b[2]) / 2, (b[1] + b[3]) / 2))
                break


def hub_words(pg, TP, name, words, colour, taken, halo):
    """The commons' name (large) and what it gathers, inside its piece. v10: a name that fits nowhere inside is
    written centred on the piece with a halo (v2.3 left it out, so the commons often had no name)."""
    TP = thin(TP, 300)
    spots = inside_spots(TP, 20)
    placed = []
    for sz in [8.0 * HUB_SIG * t for t in STEPS]:
        lines = [(s_, sz, True) for s_ in wrap(name, sz, max(18.0, (bbox(TP)[2] - bbox(TP)[0]) * 0.8), True)]
        b = fit_inside(TP, spots, lines, taken)
        if b:
            draw_block(pg, lines, b[0] + 0.6, b[3] - 0.6, colour, None)
            taken.append(b)
            placed.append(((b[0] + b[2]) / 2, (b[1] + b[3]) / 2))
            break
    else:
        best = None
        for sz in [8.0 * HUB_SIG * t for t in STEPS[3:]]:
            lines = [(s_, sz, True) for s_ in wrap(name, sz, 30.0, True)]
            w, h = block_size(lines)
            for x, y in spots[:60]:
                b = (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
                if not any(hit(b, t) for t in taken):
                    best = (lines, b, (x, y))
                    break
            if best:
                break
        if best is None:
            x, y = spots[0]
            best = (lines, (x - w / 2, y - h / 2, x + w / 2, y + h / 2), (x, y))
        draw_block(pg, best[0], best[1][0], best[1][3], colour, halo)
        taken.append(best[1])
        placed.append(best[2])
    for w_ in words:
        for sz in [3.4 * HUB_SIG * t for t in STEPS]:
            b = fit_inside(TP, spread(spots, placed), [(w_, sz, True)], taken, pad=1.0 * sz)
            if b:
                pg.text(w_, b[0] + 1.0 * sz, b[1] + 1.0 * sz + 0.06 * sz, sz, colour, bold=True)
                taken.append(b)
                placed.append(((b[0] + b[2]) / 2, (b[1] + b[3]) / 2))
                break


def word_in(pg, TP, word, sizes, colour, taken, pad=0.5, bold=True):
    """One word inside ring TP at the largest size that fits."""
    TP = thin(TP, 300)
    for sz in sizes:
        b = fit_inside(TP, inside_spots(TP), [(word, sz, bold)], taken, pad=pad)
        if b:
            pg.text(word, b[0] + pad, b[1] + pad + 0.06 * sz, sz, colour, bold=bold)
            taken.append(b)
            return True
    return False


def word_along(pg, TP, word, size, colour, taken, W, H):
    """v10: a word beside a path (PATH_WORDS: v2.3 had them but never wrote them), at the first free spot along it."""
    s = arclen(TP)
    w = text_w(word, size, True)
    for f in (0.5, 0.35, 0.65, 0.2, 0.8):
        (x, y), _ = at_len(TP, s, s[-1] * f)
        for dy in (1.6, -1.6 - size):
            b = (x - w / 2 - 0.5, y + dy - 0.5, x + w / 2 + 0.5, y + dy + size + 0.5)
            if b[0] < 0 or b[1] < 0 or b[2] > W or b[3] > H or any(hit(b, t) for t in taken):
                continue
            pg.text(word, x, y + dy + 0.06 * size, size, colour, bold=True, align="C")   # v21: no halo
            taken.append(b)
            return True
    return False


def soft(P, r=ROUND_M, step=1.5):
    """Rounded outline (cleared buildings, v2.3): every corner rounded (up to r m, at most 45 % of each side), then
    one smoothing pass. Graphic only."""
    if len(P) < 3:
        return P
    Q = [P[0]]
    for p in P[1:]:                                      # drop vertices closer than 2 m: corners made of tiny steps
        if math.hypot(p[0] - Q[-1][0], p[1] - Q[-1][1]) >= 2.0:
            Q.append(p)
    if len(Q) < 3:
        return P
    out = []
    for i in range(len(Q)):
        a, b, c = Q[i - 1], Q[i], Q[(i + 1) % len(Q)]
        la, lc = math.hypot(a[0] - b[0], a[1] - b[1]), math.hypot(c[0] - b[0], c[1] - b[1])
        d = min(r, 0.45 * la, 0.45 * lc)
        if d < 0.05:
            out.append(b)
            continue
        p0 = (b[0] + (a[0] - b[0]) * d / la, b[1] + (a[1] - b[1]) * d / la)
        p2 = (b[0] + (c[0] - b[0]) * d / lc, b[1] + (c[1] - b[1]) * d / lc)
        n = max(2, int(d / step))
        for j in range(n + 1):                           # quadratic Bezier through the corner
            t = j / float(n)
            out.append(((1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * b[0] + t * t * p2[0],
                        (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * b[1] + t * t * p2[1]))
    return chaikin(out, 1, closed=True)


# ================================================================ the hand-marker line (masterplan v9, pure Python)
def normals(P):
    """Unit left normals at each vertex (averaged over the two segments)."""
    n = len(P)
    T = []
    for i in range(n):
        a, b = P[max(0, i - 1)], P[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        T.append((-dy / L, dx / L))
    return T


def smooth_noise(n, step, wav, rnd):
    """n values of smooth random noise (std about 1) sampled every `step`, with features about `wav` long."""
    k = max(2, int(math.ceil(n * step / max(wav, 1e-9))) + 3)
    ctrl = [rnd.gauss(0.0, 1.0) for _ in range(k)]
    out = []
    for i in range(n):
        x = i * step / max(wav, 1e-9)
        j = min(int(x), k - 2)
        f = x - j
        f = f * f * (3 - 2 * f)
        out.append(ctrl[j] * (1 - f) + ctrl[j + 1] * f)
    return out


def hand_line(P, amp, wav, seed, closed=False, over=0.0):
    """A polyline as a hand would draw it: a smooth sideways wobble of about amp (never more than 2.2 amp), an
    overshoot of over at both ends (a closed ring starts at a random point and runs over past its start). Graphic
    only: areas are never computed from this."""
    P = [tuple(p) for p in P]
    if len(P) < 2:
        return P
    rnd = random.Random(seed)
    step = max(wav / 6.0, 1e-6)
    if closed:
        if math.hypot(P[0][0] - P[-1][0], P[0][1] - P[-1][1]) < 1e-9:
            P = P[:-1]
        k = rnd.randrange(len(P))
        P = P[k:] + P[:k] + [P[k]]
    P = densify(P, step)
    if over > 0 and len(P) >= 2:
        if closed:
            s = arclen(P)
            P = P + [p for p, t in zip(P[1:], s[1:]) if t <= over]
        else:
            (x0, y0), (x1, y1) = P[0], P[1]
            L0 = math.hypot(x0 - x1, y0 - y1) or 1.0
            (x2, y2), (x3, y3) = P[-1], P[-2]
            L1 = math.hypot(x2 - x3, y2 - y3) or 1.0
            P = [(x0 + (x0 - x1) / L0 * over, y0 + (y0 - y1) / L0 * over)] + P + \
                [(x2 + (x2 - x3) / L1 * over, y2 + (y2 - y3) / L1 * over)]
    if amp > 0:
        w = [max(-2.2, min(2.2, v)) * amp for v in smooth_noise(len(P), step, wav, rnd)]
        N = normals(P)
        P = [(p[0] + n[0] * d, p[1] + n[1] * d) for p, n, d in zip(P, N, w)]
    return P


def link_cols(kind):
    """(shaft, head) colours of a link arrow (masterplan v9 link_cols): water dark water-blue; high water
    water-blue with dark heads; people to the water and untyped links in the accent red."""
    if kind == "water":
        return COL["river_dark"], COL["river_dark"]
    if kind == "flood":
        return COL["river_mid"], COL["river_dark"]
    return COL["accent"], COL["accent_dark"]


def link_arrow(pg, P, kind, heads, seed):
    """The bold hand-drawn link arrow along P (page mm), its head at the end (both ends when heads = 2); the head
    shrinks on a short arrow, the pen never does (masterplan v9)."""
    shaft_c, head_c = link_cols(kind)
    s = arclen(P)
    Lt = s[-1]
    if Lt < 1e-6:
        return
    k = min(1.0, Lt / (HA["barb"] * (3.2 if heads == 2 else 2.0)))
    barb = HA["barb"] * k
    inset = barb * 0.25
    sh = sub_line(P, s, inset if heads == 2 else 0.0, Lt - inset)
    sh = hand_line(sh, HA["amp"], HA["wav"], seed)
    if kind == "flood":
        pg.line(sh, shaft_c, HA["shaft"], [1.6, 0.9], cap=0)
    else:
        pg.line(sh, shaft_c, HA["shaft"], cap=1)
    ends = [(Lt, max(0.0, Lt - barb * 0.8))] + ([(0.0, min(Lt, barb * 0.8))] if heads == 2 else [])
    for t_tip, t_back in ends:
        (tx, ty), _ = at_len(P, s, t_tip)
        (bx, by), _ = at_len(P, s, t_back)
        d = math.hypot(tx - bx, ty - by) or 1.0
        dx, dy = (tx - bx) / d, (ty - by) / d
        for sg in (1, -1):
            a = math.radians(HA["ang"]) * sg
            vx, vy = dx * math.cos(a) - dy * math.sin(a), dx * math.sin(a) + dy * math.cos(a)
            ex, ey = tx - vx * barb, ty - vy * barb
            pg.line([(tx + vx * HA["over"] * k, ty + vy * HA["over"] * k), (ex, ey)], head_c, HA["barb_w"], cap=1)
            h = HA["serif"] * k / 2
            pg.line([(ex - vy * h, ey + vx * h), (ex + vy * h, ey - vx * h)], head_c, HA["serif_w"], cap=1)


def boxes_along(P, half):
    """Boxes along a line (page mm): what words keep off."""
    s = arclen(P)
    out = []
    t = 0.0
    while t <= s[-1]:
        (x, y), _ = at_len(P, s, t)
        out.append((x - half, y - half, x + half, y + half))
        t += half
    return out


# ================================================================ v21: roads, panel marks, ring clipping
ROAD_MAIN_M = 14.0           # v21: a surveyed street edge this close to a main road line (OSM) is a main-road edge, m
ROAD_TONE = ("CFCCC5", "847E75", "4A3F35")   # v21: palette v1.4 role "road": light lanes, mid streets, dark main roads
ROAD_LW = (0.22, 0.45)       # v21: street edge, main-road edge, mm (graphic)


class LineNear(object):
    """v21: 'within r m of any of these polylines' (segments bucketed in r-sized cells)."""

    def __init__(self, lines, r):
        self.r, self.c, self.g = r, max(r, 5.0), {}
        for P in lines:
            for a, b in zip(P, P[1:]):
                for gi in range(int(math.floor(min(a[0], b[0]) / self.c)), int(math.floor(max(a[0], b[0]) / self.c)) + 1):
                    for gj in range(int(math.floor(min(a[1], b[1]) / self.c)), int(math.floor(max(a[1], b[1]) / self.c)) + 1):
                        self.g.setdefault((gi, gj), []).append((a, b))

    def within(self, x, y):
        gi, gj = int(math.floor(x / self.c)), int(math.floor(y / self.c))
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for a, b in self.g.get((gi + di, gj + dj), ()):
                    if seg_dist(x, y, a, b) <= self.r:
                        return True
        return False


class BoxNear(object):
    """v21: a rectangle as the 'near' test of prep_base and Grid (the detail windows)."""

    def __init__(self, R):
        self.R = R

    def inside(self, x, y):
        R = self.R
        return R[0] <= x <= R[2] and R[1] <= y <= R[3]

    within = inside


def clip_ring(R, cb):
    """A ring cut to the rectangle cb = (x0, y0, x1, y1) (Sutherland-Hodgman on the four sides)."""
    P = list(R)
    for ax, lim, keep_lo in ((0, cb[0], False), (0, cb[2], True), (1, cb[1], False), (1, cb[3], True)):
        if not P:
            break
        out = []
        for i in range(len(P)):
            a, b = P[i - 1], P[i]
            ia = a[ax] <= lim if keep_lo else a[ax] >= lim
            ib = b[ax] <= lim if keep_lo else b[ax] >= lim
            if ib != ia:
                t = (lim - a[ax]) / ((b[ax] - a[ax]) or 1e-12)
                out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
            if ib:
                out.append(b)
        P = out
    return P


def draw_roads(pg, T, streets, mains):
    """v21: the surveyed street edges (YOL_SOSE, YOL_BORDUR) as one outlined network over the zones: the edges of
    the main roads (within ROAD_MAIN_M of a main road line) in the road role's dark tone and heavier."""
    near = LineNear(mains, ROAD_MAIN_M) if mains else None
    for P in streets:
        runs = [(P, False)]
        if near is not None:
            runs = [(r_, True) for r_ in cut_runs(P, near.within, 1.0)] + \
                   [(r_, False) for r_ in cut_runs(P, lambda x, y: not near.within(x, y), 1.0)]
        for r_, main in runs:
            leg(("road", "main" if main else "street"))
            pg.line([T(p) for p in r_], ROAD_TONE[2] if main else ROAD_TONE[1], ROAD_LW[1] if main else ROAD_LW[0])


def north_arrow(pg, x, y, h=7.0):
    """v21: north arrow (survey grid +Y) with its tip at (x, y), page mm; 'N' beside it."""
    pg.poly([[(x, y), (x - 1.8, y - h), (x, y - h * 0.72)]], fill=COL["ink_dark"])
    pg.poly([[(x, y), (x, y - h * 0.72), (x + 1.8, y - h)]], fill=COL["white"], stroke=COL["ink_dark"], lw=0.15)
    pg.text(u"N", x + 2.6, y - 3.2, 2.6, COL["ink_dark"], bold=True)


def panel_marks(sh, x, y, scale, marks):
    """v21: north arrow and scale bar in a panel's bottom margin (x, y = its left end, page mm)."""
    north_arrow(sh, x + 2.0, y + 8.0)
    scale_bar(sh, x + 12.0, y + 1.0, scale, marks)


# ================================================================ one plan panel (sheet and detail windows)
def draw_area(spec, opt, alt, D, base, pz, scale, alpha, A, CL=None, win=None, detail=None, title=None):
    """One working area (v19: the freely grown zones, the commons, the promenade, the spine zones) -> Page.
    v21: win = (x0, y0, x1, y1) world rectangle of a 1:1,000 detail window (base then covers the window);
    detail(pg, T, k, taken, dw, dh, avoid) draws the window's detail before the words (avoid: the commons' rings,
    where its labels do not go); title replaces the place name.
    The panel's drawing + its bottom margin (north arrow, scale bar) is sh.crop (page mm, y up)."""
    key, place, idea = spec
    k = 1000.0 / scale
    R = win or base["R"]
    _PLEG[0] = {}                                        # v21: this panel's legend keys (its booklet crop)
    M, HEAD = 12.0, 20.0
    dw, dh = (R[2] - R[0]) * k, (R[3] - R[1]) * k
    zones = sorted([z for z in D.zones if z["area"] == key], key=lambda z: -z["m2"])
    removes = [r for r in D.removes if r["area"] == key]
    paths = [p for p in D.paths if p["area"] == key]
    pg = Page(dw, dh)
    T = lambda p: ((p[0] - R[0]) * k, (p[1] - R[1]) * k)
    for pc in pz:
        pc["tones"] = piece_tone(pc)
        pc["TPs"] = [[T(p) for p in Lp] for Lp in pc["loops"]]
    ctx = [pc for pc in pz if pc["kind"] not in ("zone", "hub", "free", "meet")]
    W_ = COL["white"]
    vis = lambda TPs: [V_ for V_ in (clip_ring(T_, (0.0, 0.0, dw, dh)) for T_ in TPs) if len(V_) >= 3]   # v21
    for pc in pz:                                        # v17: the legend's entries
        if not vis(pc["TPs"]):                           # v21: only what shows in this panel
            continue
        if pc["kind"] == "free":
            leg_zone(pc["zone"])
        elif pc["kind"] == "hub":
            LEG.setdefault("hub", [])
            if pc["tones"][0] not in LEG["hub"]:
                LEG["hub"].append(pc["tones"][0])
        elif pc["kind"] in PIECE_TONE:
            leg(("ctx", pc["kind"]))
    for ck, lw, dash, P in base["lines"]:
        leg(("line", ck))
    if removes:
        leg("cleared")
    if paths:
        leg("path")
    if win is not None:                                  # v21: the survey under the whole window (the puzzle
        fc = base["faces"]                               # covers only the working area and its ring)
        pg.poly([[T(p) for p in F] for role in ("building", "housing") for F in fc.get(role, [])], fill=COL["bld"])
        pg.poly([[T(p) for p in F] for F in fc.get("heritage", [])], fill=COL["her"], stroke=COL["her_edge"], lw=0.1)
        pg.poly([[T(p) for p in F] for F in fc.get("park", [])], fill=COL["park"])
    # v19: context opaque; alternative 2's free zone pieces on one white base; the promenade and the spine zones;
    # the free pieces' light fill at the opacity (overlaps darken); alternative 1's commons opaque on top
    for pc in sorted(ctx, key=lambda q: q["e"]):
        pg.poly(pc["TPs"], fill=pc["tones"][0], stroke=W_, lw=0.5)
    fr = [q for q in pz if q["kind"] == "free"]
    for pc in fr:
        pg.poly(pc["TPs"], fill=W_, stroke=W_, lw=0.5)
    G = Grid(R, base["near"], BAND_CELLS)
    CLc = clip_city(CL, base["near"].within) if CL is not None else None
    cb = (-2.0, -2.0, dw + 2.0, dh + 2.0)
    RB = [[T(p) for p in L_] for L_ in (CL or {}).get("prom", [])]          # v21: the promenade beside the stream
    RB = [L_ for L_ in RB if hit(bbox(L_), cb)]
    if RB:
        leg("river_band")
        lt, md, dk = RIVER_BAND_TONE
        pg.poly([[(x + 0.8, y - 0.8) for x, y in L_] for L_ in RB], fill=dk, alpha=0.22)   # shadow: volume
        pg.poly(RB, fill=lt, alpha=0.85)
        pg.poly(RB, stroke=dk, lw=0.35)
    SZ = []
    if CLc is not None:
        for nm_, lines_, ni in ((u"MAIN SPINE", CLc["mains"] if "mains" in CLc else [CLc["main"]], 102),
                                (u"STREAMSIDE SPINE", [s_["P"] for s_ in CLc["spine"]], 103)):
            TPs = [[T(p) for p in L_] for L_ in grow_band(G, lines_, [], SPINE_ZONE_M, ni, opt)]
            if TPs:
                leg(("spinezone", nm_))
                pg.poly(TPs, fill=MP["centre"][0], alpha=alpha)
                SZ.append((nm_, TPs))
    for pc in fr:
        pg.poly(pc["TPs"], fill=pc["tones"][0], alpha=alpha)
    for pc in [q for q in pz if q["kind"] == "hub"]:
        pg.poly(pc["TPs"], fill=pc["tones"][0], stroke=W_, lw=0.5)
    for ck, lw, dash, P in base["lines"]:
        pg.line([T(p) for p in P], COL[ck], lw, dash)
    for z in list(zones):                                # the words go into the zone's own (free) piece
        pc = next((q for q in pz if q["kind"] == "free" and q["zone"] is z), None) or \
            next((q for q in pz if q["kind"] == "zone" and q["zone"] is z), None)
        if pc is None or not pc["TPs"]:
            zones.remove(z)
            continue
        V_ = vis(pc["TPs"])                              # v21: words on the part that shows in the panel
        if not V_:
            zones.remove(z)
            continue
        z["TP"] = max(V_, key=lambda r_: abs(area2(r_)))
    taken = []
    for r in removes:
        r["TP"] = [T(p) for p in soft(r["P"])]
        pg.poly([r["TP"]], stroke=COL["ink2"], lw=0.3, dash=[0.9, 0.6])
    for p in paths:
        p["TP"] = [T(q) for q in p["P"]]
        pg.line(p["TP"], W_, 1.9)
        pg.line(p["TP"], COL["path"], 1.0, [1.0, 0.35], cap=0)
    if CLc is not None:                                  # v11: walks (v19: the spines are zones above)
        draw_city(pg, T, CLc, k, spines=False)
    draw_roads(pg, T, base.get("streets_all", base["streets"]), [CL["main"]] if CL is not None and CL.get("main")
               else [])                                  # v21: the street network over the whole panel
    if detail is not None:                               # v21: the detail window's own layers and labels
        detail(pg, T, k, taken, dw, dh, [V_ for q in pz if q["kind"] == "hub" for V_ in vis(q["TPs"])])
    # ---- words: the commons first, the promenade and spine zones, then each zone (largest first), cleared, context
    for pc in [q for q in pz if q["kind"] == "hub"]:
        if not vis(pc["TPs"]):
            continue
        hub_words(pg, max(vis(pc["TPs"]), key=lambda r_: abs(area2(r_))), pc["name"], pc["words"], W_, taken,
                  None)                                  # v21: no haloed labels on maps
    RBc = [clip_ring(L_, (0.0, 0.0, dw, dh)) for L_ in RB]          # v21: words on the visible part only
    RBc = [L_ for L_ in RBc if len(L_) >= 3]
    for nm_, TPs in ([(RIVER_BAND_NAME, RBc)] if RBc else []) + SZ:   # v18-v19: names and keywords on the fills
        TP_ = max(TPs, key=lambda r_: abs(area2(r_)))
        dk_ = RIVER_BAND_TONE[2] if nm_ == RIVER_BAND_NAME else MP["centre"][2]
        word_in(pg, TP_, nm_, (4.0, 3.4, 2.8), dk_, taken)
        for w_ in (RIVER_BAND_WORDS if nm_ == RIVER_BAND_NAME else []):
            for TP2 in sorted(TPs, key=lambda r_: -abs(area2(r_)))[:3]:
                if word_in(pg, TP2, w_, (2.6, 2.2, 1.8), dk_, taken):
                    break
    seen = set()
    for z in zones:
        zone_words(pg, z, z["TP"], z.get("own", ""), key, opt, taken, seen)
    for r in removes:
        word_in(pg, r["TP"], REMOVE_WORDS[0], (2.3, 1.8, 1.5), COL["ink"], taken)
    for pc in ctx:                                       # context pieces carry their own word (no legend)
        wd = KIND_WORD.get(pc["kind"])
        if not wd or not pc["inside"]:
            continue
        for TP in sorted(vis(pc["TPs"]), key=lambda r_: -abs(area2(r_)))[:3]:
            word_in(pg, TP, wd, (2.6, 2.2, 1.8), pc["tones"][2], taken, pad=0.8)
    for p in paths:
        for w_ in PATH_WORDS.get(p.get("own"), []):
            word_along(pg, p["TP"], w_, 2.2, COL["path"], taken, dw, dh)
    # ---- the panel: place over the plan (no owner names, no working-area outline); v21: north arrow and scale
    # bar in the bottom margin, inside the panel's crop
    W = M + dw + M
    H = M + HEAD + dh + M
    sh = Page(W, H)
    sh.poly([rect(0, 0, W, H)], fill=COL["paper"])
    sh.clip([rect(M, M, M + dw, M + dh)])
    blit(sh, pg, M, M)
    sh.unclip()
    txt = title or place
    sh.text(txt, M, H - M - 8.0, min(8.0, 8.0 * dw / max(text_w(txt, 8.0, True), 1e-6)), COL["ink_dark"], bold=True)
    if idea and not title:
        sh.text(idea, M, H - M - 14.0, min(4.0, 4.0 * dw / max(text_w(idea, 4.0, True), 1e-6)), COL["ink_dark"],
                bold=True)
    panel_marks(sh, M, 1.5, scale, (0.0, 10.0, 20.0, 50.0) if win is not None else (0.0, 50.0, 100.0, 200.0))
    sh.crop = (M, 0.5, M + dw, M + dh)
    sh.key, sh.world = key, R
    sh.pleg, _PLEG[0] = _PLEG[0], None
    return sh
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
# ================================================================ v21: the 1:1,000 detail sheet and the booklet crops
# Aras 25 Oct 21:49 on the booklet's 1:1,000 page: "this should add more detail from what we have shown in
# masterplan". The detail sheet shows the two windows of the booklet's C3 page (upstream entry; K5 with Demeter's
# Garden) at 1:1,000 with what the whole plan cannot show, all from the project's data:
#   cuts      the water board's surveyed channel cuts (the proposal sections stand on them) and the site board's
#             section lines crossing the window, named; at a cut its bed level and the DSI Q100 / Q500 levels with
#             the width each covers on the cut (CUT_AT)
#   route     the zone base's water links numbered in the order of the water route (ROUTE), with the areas the
#             script computes from the zone curves (no script computes a storage volume: left out, logged)
#   planting  band letters and species codes of the booklet's verified list (plan page C7 = water board v1.9
#             PLANT_BANDS / SPECIES) on the zones whose wetness tier they belong to (ZONE_PLANTING)
#   levels    survey spot heights (NOKTA_TAKEOMETRI) in the bed and on the bank tops, by the edges river_walks found
#   sketches  (Aras 21:57) terrace steps as a few strokes in the retention terraces and flood terraces, ramps as
#             wedges on the zone base's people-to-the-water links: zones and sketch marks, abstract, no dimensions
# Booklet (CROP_SPEC.md, Aras 21:47): the booklet's drawings are crops of the sheets; blocks.json holds one crop per
# panel (both halves of the masterplan sheet, both detail windows), results.json the frames and places.
DT_SCALE = 1000.0
DT_FRAME = (194.0, 176.0)            # mm: the booklet's C3 frame (booklet_slots.json when the assembler has run)
DT_WINDOWS = [  # crop id, old booklet id, working area, sheet title, booklet caption, zone names the window must show
    ("dt_upstream", "c3_a", "calisma_alan[0]", u"UPSTREAM ENTRY · COLLECT, CLEAN, HOLD",
     u"Upstream entry: collect, clean, hold", (u"REED BASINS", u"RETENTION TERRACES", u"SPILLWAY", u"SHADED WALK")),
    ("dt_k5", "c3_b", "calisma_alan[1]", u"K5 BRIDGE · DEMETER'S GARDEN", u"K5 bridge and Demeter's Garden",
     (u"DEMETER'S GARDEN",))]
MP_CROPS = {"calisma_alan[0]": ("mp_upstream", "c1_s1", u"Masterplan, upstream entry to K4 bridge"),
            "calisma_alan[1]": ("mp_downstream", "c1_s2", u"Masterplan, K5 bridge to downstream end")}
# CUT_AT: the water board's surveyed channel cuts (water board v1.9 CUTS, proposal sections v4 panels 1-4):
# number, name, centre (survey m) and span (u m, + = left bank looking downstream) from
# research/rain_river_levels/scripts/surveyed_sections/levels2_out.json (24 Oct); bed and DSI Q100 / Q500 levels (m,
# Manning n 0.050) and the width each covers (u from, to) as there (= water board CUTS bed + depth).
CUT_AT = [("1", u"UPSTREAM ENTRY", (29693.022, 32569.176), (-74.5, 85.5), 70.36, (73.35, -29.5, 14.0), (73.66, -30.5, 15.0)),
          ("2", u"K4 BRIDGE", (29959.774, 32264.566), (-21.0, 91.5), 64.77, (67.33, -58.5, 16.5), (67.61, -70.5, 16.5)),
          ("3", u"K5 BRIDGE", (30354.663, 31689.671), (-86.0, 64.5), 55.96, (58.41, -37.5, 12.0), (58.75, -45.5, 12.5)),
          ("4", u"DOWNSTREAM REACH", (30991.856, 31039.404), (-39.5, 26.5), 45.67, (47.72, -29.5, 19.5), (48.0, -30.5, 20.0))]
# The site board's section lines S1-S6 (selinus_board v39 SECTION_LINES_LK, its names in this order), survey m
SITE_SECTIONS = [((29545.739, 32125.562), (30167.095, 32687.137)), ((29806.600, 31571.233), (30610.920, 32286.788)),
                 ((30366.363, 31067.627), (31210.537, 31688.982)), ((30616.355, 30540.471), (31489.513, 31161.826)),
                 ((29455.902, 32763.450), (30154.568, 32040.938)), ((31571.801, 30442.533), (30689.179, 31396.583))]
# The water route at the upstream entry (zone base links, by the zones they join): order and short words
ROUTE = [((None, "WT"), u"INTO {}", 1), (("WS", "WT"), u"FROM {}", 0), (("WT", "WD"), u"TO {}", 1),
         (("WD", None), u"BACK TO THE STREAM", None)]   # (from, to), words, which end's zone they name
ROUTE_SHORT = {u"RETENTION TERRACES": u"TERRACES"}
# Planting (booklet page C7 / water board v1.9 bands A-F and species): band letters and species codes per zone, by
# the zone's wetness (bed and reed basins wet most of the year: B; flood terrace: C; terraces: C and E; dry tops: E
# and F). A design reading of the bands; only species of the verified list.
SPECIES_CODE = [("Ty", u"Typha angustifolia"), ("Ph", u"Phragmites australis"), ("Me", u"Mentha aquatica"),
                ("Sa", u"Salix alba"), ("Ta", u"Tamarix smyrnensis"), ("Vi", u"Vitex agnus-castus"),
                ("Po", u"Populus alba"), ("Fr", u"Fraxinus angustifolia"), ("Pl", u"Platanus orientalis"),
                ("La", u"Lavandula stoechas")]
BAND_NAME = {"A": u"A STRIP AND BED · PERMANENT", "B": u"B MARSH · 150-365 D A YEAR", "C": u"C WILLOW · 50-150 D",
             "D": u"D WET MEADOW · 10-150 D", "E": u"E DRY MEADOW · 0.5-50 D", "F": u"F TERRACES · EXTREME ONLY"}
ZONE_PLANTING = {("WT", None): ("B", ("Ty", "Ph", "Me")), ("WA", "W"): ("B", ("Ty", "Ph", "Me")),
                 ("WA", "F"): ("C", ("Sa", "Ta")), ("WS", None): ("CE", ("Vi", "Po", "Fr")),
                 ("GR", None): ("EF", ("Pl", "La"))}
STEP_M = 4.0                         # spacing of the terrace step strokes, m (sketch)
RAMP_W = (3.0, 1.2)                  # ramp wedge width at the top and at the water, m (sketch)
SPOT_GAP_M, SPOT_BANK_M = 30.0, 10.0   # spot levels at least this far apart; bank top = within this of the edge
SPOT_MAX = (6, 8)                    # at most this many bed / bank spot levels per window
# v22 (Aras 26 Oct 06:27 "make them have calculated roughly"): rough volume on the water route = zone area x depth.
# Reed basins: 0.46 m, the water depth of EPA's worked example ("water depth = 0.46 meters (1.5 ft)"; vegetated
# depth "a few inches to two feet or more"), EPA 832-F-00-024 Free Water Surface Wetlands, Sep 2000. Terraces: 0.30 m,
# our design depth (no source sets it).
STORE_DEPTH = {"WT": 0.46, "WS": 0.30}
DT_TS = 2.6                          # detail label size, mm (7.4 pt at 1:1; the booklet sets them at 7.5 pt)


def places(spec, CL, survey):
    """Named places (world m): K4, K3, the Red Hall and K5 are city link's surveyed spine anchors (K4 = piece A's
    start, K3 its end, Red Hall = piece C's start, K5 its end), each bridge snapped to the nearest surveyed bridge
    (YOL_KOPRU) within 60 m."""
    sp = dict((pc.get("id"), pc) for pc in spec.get("spine", []))
    out = {}
    for nm, (pid, end) in ((u"K4", ("A", "frm")), (u"K3", ("A", "to")), (u"RED HALL", ("C", "frm")),
                           (u"K5", ("C", "to"))):
        if pid in sp and sp[pid].get(end):
            out[nm] = tuple(sp[pid][end])
    mids = [((B[0][0] + B[-1][0]) / 2.0, (B[0][1] + B[-1][1]) / 2.0) for B in survey.get("bridge", [])]
    for nm in (u"K4", u"K3", u"K5"):
        if nm in out and mids:
            m = min(mids, key=lambda q: math.hypot(q[0] - out[nm][0], q[1] - out[nm][1]))
            if math.hypot(m[0] - out[nm][0], m[1] - out[nm][1]) <= 60.0:
                out[nm] = m
    return out


def detail_windows(D, plc, frame):
    """[{id, old, key, title, caption, R}] north-up windows of frame (mm) x DT_SCALE: centred on the zones it must
    show (and the cut in it), for K5 on the bridge moved just enough to hold Demeter's Garden and the cut."""
    Wm, Hm = frame[0] * DT_SCALE / 1000.0, frame[1] * DT_SCALE / 1000.0
    out = []
    for bid, old, key, title, cap, names in DT_WINDOWS:
        zs = [z for z in D.zones if z["area"] == key and name_of(z, z.get("own", "")) in names]
        pts = [p for z in zs for p in z["P"]] or [p for z in D.zones if z["area"] == key for p in z["P"]]
        if not pts:
            continue
        b = bbox(pts)
        c = ((b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0)
        if bid == "dt_k5" and plc.get(u"K5"):
            k5 = plc[u"K5"]
            cut = [x[2] for x in CUT_AT if x[1] == u"K5 BRIDGE"]
            need = bbox(pts + [k5] + cut)
            c = (min(max(k5[0], need[2] - Wm / 2 + 10.0), need[0] + Wm / 2 - 10.0),
                 min(max(k5[1], need[3] - Hm / 2 + 10.0), need[1] + Hm / 2 - 10.0))
        out.append({"id": bid, "old": old, "key": key, "title": title, "caption": cap,
                    "R": (c[0] - Wm / 2, c[1] - Hm / 2, c[0] + Wm / 2, c[1] + Hm / 2)})
    return out


def place_label(pg, lines, anchor, taken, W, H, colour, d0=1.2, leader=True, avoid=(), more=(), anywhere=False):
    """A label block [(text, size, bold)] on a free spot round anchor (page mm, y up), off the rings in avoid, with
    a thin leader when it sits off the anchor. v22: then round each point of more (e.g. along the route), and with
    anywhere the free spot nearest anchor on the whole panel (2 mm grid). Returns its box or None."""
    w, h = block_size(lines)
    ax, ay = anchor
    on = 0.0 <= ax <= W and 0.0 <= ay <= H              # v22: the leader goes to anchor only when it is on the panel

    def free(b):
        return not (b[0] < 0.8 or b[1] < 0.8 or b[2] > W - 0.8 or b[3] > H - 0.8 or
                    any(hit(b, t, 0.4) for t in taken) or (avoid and not box_clear(b, avoid)))

    def put(b, px, py, far):
        draw_block(pg, lines, b[0], b[3], colour, None)
        taken.append(b)
        if leader and far:
            qx, qy = min(max(px, b[0]), b[2]), min(max(py, b[1]), b[3])
            pg.line([(px, py), (qx, qy)], COL["ink2"], 0.15)
        return b

    for k_, (px, py) in enumerate([anchor] + list(more)):
        for d in (d0, d0 + 2.0, d0 + 4.0, d0 + 7.0, d0 + 11.0, d0 + 16.0, 24.0, 32.0):
            for i in range(16):
                a = math.radians(i * 22.5 + 11.25)
                cx, cy = px + math.cos(a) * (d + w / 2), py + math.sin(a) * (d + h / 2)
                b = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
                if free(b):
                    return put(b, ax, ay, d > 3.0 or k_ > 0) if on or k_ == 0 else put(b, px, py, d > 3.0)
    if anywhere:                                         # v22: last, any free spot on the panel, nearest first
        cs = [(x_ * 2.0, y_ * 2.0) for x_ in range(int(W / 2.0) + 1) for y_ in range(int(H / 2.0) + 1)]
        for cx, cy in sorted(cs, key=lambda c_: (c_[0] - ax) ** 2 + (c_[1] - ay) ** 2):
            b = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
            if free(b):
                return put(b, ax, ay, True) if on else put(b, cx, cy, False)
    return None


def _normal_at(ref, q):
    """Unit normal (left of the flow) of STREAM_REF at the point nearest q."""
    s = arclen(ref)
    c, _ = chain_at(ref, q)
    _, t = at_len(ref, s, c)
    return (-t[1], t[0]), t


def _boxes_line(P, half, taken):
    taken += boxes_along(P, half)


def detail_overlay(win, D, CL, spots, plc, missing, warn):
    """The detail of one window, drawn by draw_area before the words (see the head of this part)."""
    R = win["R"]
    inR = lambda p, m=0.0: R[0] - m <= p[0] <= R[2] + m and R[1] - m <= p[1] <= R[3] + m
    ref = CL["W"]["ref"]
    shapes = D.zones + D.strips

    def f(pg, T, k, taken, dw, dh, hubs=()):
        ink, ink2 = COL["ink_dark"], COL["ink2"]
        av = [(r_, bbox(r_)) for r_ in hubs]
        # ---- sketches: terrace steps in the terrace zones, ramps on the people-to-the-water links (under the rest)
        for z in D.zones:
            if not (z["code"] == "WS" or (z["code"] == "WA" and z["tier"] == "F")) or not any(inR(p) for p in z["P"]):
                continue
            n, t = _normal_at(ref, z["q"])
            ext = [(p[0] - z["q"][0]) * n[0] + (p[1] - z["q"][1]) * n[1] for p in z["P"]]
            alo = [(p[0] - z["q"][0]) * t[0] + (p[1] - z["q"][1]) * t[1] for p in z["P"]]
            o = min(ext) + STEP_M / 2.0
            i = 0
            while o < max(ext):
                L_ = [(z["q"][0] + n[0] * o + t[0] * a, z["q"][1] + n[1] * o + t[1] * a)
                      for a in (min(alo) - 2.0, max(alo) + 2.0)]
                for r_ in cut_runs(L_, lambda x, y: pip(x, y, z["P"]), 0.5):
                    if len(r_) >= 2 and math.hypot(r_[-1][0] - r_[0][0], r_[-1][1] - r_[0][1]) > 3.0:
                        P = hand_line([T(p) for p in (r_[0], r_[-1])], 0.25, 8.0, 31 + i, over=0.6)
                        pg.line(P, zone_tones(z)[2], 0.3, alpha=0.75)
                        leg(("dt", "steps"))
                o += STEP_M
                i += 1
        for i, L in enumerate(D.links):
            if L["kind"] != "people" or not any(inR(p) for p in L["P"]):
                continue
            P = [T(p) for p in L["P"]]
            (ax, ay), (bx, by) = P[0], P[-1]
            d = math.hypot(bx - ax, by - ay) or 1.0
            ux, uy = (bx - ax) / d, (by - ay) / d
            nx, ny = -uy, ux
            w0, w1 = RAMP_W[0] * k / 2.0, RAMP_W[1] * k / 2.0
            ring_ = [(ax + nx * w0, ay + ny * w0), (bx + nx * w1, by + ny * w1), (bx - nx * w1, by - ny * w1),
                     (ax - nx * w0, ay - ny * w0)]
            pg.poly([ring_], fill=ink2, alpha=0.2)
            pg.poly([ring_], stroke=ink2, lw=0.25)
            for j in (1, 2, 3):                          # chevrons down the slope
                cx, cy = ax + ux * d * j / 4.0, ay + uy * d * j / 4.0
                ww = (w0 + (w1 - w0) * j / 4.0) * 0.8
                pg.line([(cx - ux * 1.0 + nx * ww, cy - uy * 1.0 + ny * ww), (cx, cy),
                         (cx - ux * 1.0 - nx * ww, cy - uy * 1.0 - ny * ww)], ink2, 0.25)
            taken.append(bbox(ring_))
            leg(("dt", "ramp"))
        # ---- the cuts: water board channel cuts (with their levels) and the site board's section lines
        cut_lab = []
        for num, nm, c, span, bed, q100, q500 in CUT_AT:
            if not inR(c):
                continue
            n, t = _normal_at(ref, c)
            at = lambda u: (c[0] + n[0] * u, c[1] + n[1] * u)
            for lv, lw, colr in ((q500, 2.2, COL["river_mid"]), (q100, 2.2, COL["river_dark"])):
                pg.line([T(at(lv[1])), T(at(lv[2]))], colr, lw, cap=0, alpha=0.45)
            leg(("dt", "q"))
            P = [T(at(span[0])), T(at(span[1]))]
            pg.line(P, ink, 0.35, [4.0, 1.0, 0.6, 1.0], cap=0)
            for e_, sg in ((P[0], 1.0), (P[1], -1.0)):     # view markers: filled triangles looking downstream
                tx, ty = T((c[0] + t[0], c[1] + t[1]))
                ox, oy = T(c)
                vx, vy = tx - ox, ty - oy
                L_ = math.hypot(vx, vy) or 1.0
                vx, vy = vx / L_, vy / L_
                pg.poly([[(e_[0] + vx * 2.6, e_[1] + vy * 2.6), (e_[0] - vy * 1.3, e_[1] + vx * 1.3),
                          (e_[0] + vy * 1.3, e_[1] - vx * 1.3)]], fill=ink)
            x0, y0 = T(c)
            pg.line([(x0 - 0.9, y0 - 0.9), (x0 + 0.9, y0 + 0.9)], COL["river_dark"], 0.3)
            pg.line([(x0 - 0.9, y0 + 0.9), (x0 + 0.9, y0 - 0.9)], COL["river_dark"], 0.3)
            _boxes_line(P, 0.8, taken)
            leg(("dt", "cut"))
            inside = [p for p in P if 0 <= p[0] <= dw and 0 <= p[1] <= dh]
            cut_lab.append(([(u"SECTION {} · {}".format(num, nm), DT_TS, True),
                             (u"bed +{:.2f}".format(bed), DT_TS, False),
                             (u"Q100 +{:.2f} · Q500 +{:.2f}".format(q100[0], q500[0]), DT_TS, False)],
                            inside[0] if inside else (min(max(x0, 2.0), dw - 2.0), min(max(y0, 2.0), dh - 2.0))))
        for i, (a, b) in enumerate(SITE_SECTIONS):
            P = [T(p) for p in cut_runs([a, b], lambda x, y: inR((x, y)), 2.0)[0]] \
                if cut_runs([a, b], lambda x, y: inR((x, y)), 2.0) else []
            if len(P) < 2:
                continue
            pg.line(P, ink2, 0.3, [4.0, 1.0, 0.6, 1.0], cap=0)
            _boxes_line(P, 0.8, taken)
            leg(("dt", "site"))
            end = max(P, key=lambda p: p[1])
            cut_lab.append(([(u"SITE SECTION S{}".format(i + 1), DT_TS, True)],
                            (min(max(end[0], 2.0), dw - 2.0), min(max(end[1], 2.0), dh - 2.0))))
        # ---- the water route: the zone base's water links, numbered in the route's order
        steps = []
        for L in D.links:
            if L["kind"] != "water" or not any(inR(p) for p in L["P"]):
                continue
            a, b = link_shapes(L, shapes)
            ab = (a["code"] if a and a in D.zones else None, b["code"] if b and b in D.zones else None)
            order = next((i for i, st in enumerate(ROUTE) if st[0] == ab), len(ROUTE))
            steps.append((order, L, a, b, ab))
        steps.sort(key=lambda s_: s_[0])
        route_lab = []
        for n_, (order, L, a, b, ab) in enumerate(steps, 1):
            P = [T(p) for p in L["P"]]
            link_arrow(pg, P, "water", L["heads"], 3 + n_)
            leg(("link", "water"))
            _boxes_line(P, 1.2, taken)
            if order < len(ROUTE):
                end = ROUTE[order][2]
                z = (a, b)[end] if end is not None else None
                nm = ROUTE_SHORT.get(name_of(z, z.get("own", "")), name_of(z, z.get("own", ""))) if z else u""
                txt = ROUTE[order][1].format(nm)
                if z is not None:
                    txt += u" {:,.0f} m²".format(z["m2"])
                    if z["code"] in STORE_DEPTH:             # v22: rough volume, area x depth
                        txt += u" · ~{:,.0f} m³".format(round(z["m2"] * STORE_DEPTH[z["code"]], -1))
                        leg(("dt", "vol"))
            else:
                txt = (L["label"] or u"WATER").replace(u"RIVER", u"STREAM")
            s = arclen(P)
            (mx, my), _ = at_len(P, s, s[-1] / 2.0)
            pg.circle(mx, my, 2.2, fill=COL["white"])
            pg.circle(mx, my, 1.9, fill=COL["river_dark"])
            pg.text(str(n_), mx, my - 0.85, 2.4, COL["white"], bold=True, align="C")
            taken.append((mx - 2.2, my - 2.2, mx + 2.2, my + 2.2))
            leg(("dt", "route"))
            route_lab.append(([(u"{} {}".format(n_, txt), DT_TS, True)], (mx, my),   # v22: + spots along the route
                              [at_len(P, s, s[-1] * f_)[0] for f_ in (0.3, 0.7, 0.1, 0.9, 0.0, 1.0)]))
        # ---- survey spot levels: lowest in the bed, highest on the bank tops (edges of river_walks)
        rows = [r for r in (CL["W"].get("rows") or []) if r.get("NE") and r.get("SW") and inR(r["p"], 60.0)]
        bed, bank = [], []
        for q in spots:
            if not inR(q, -2.0) or not rows:
                continue
            r = min(rows, key=lambda r_: (r_["p"][0] - q[0]) ** 2 + (r_["p"][1] - q[1]) ** 2)
            if math.hypot(r["p"][0] - q[0], r["p"][1] - q[1]) > 40.0:
                continue
            t_ = (q[0] - r["p"][0]) * r["n"][0] + (q[1] - r["p"][1]) * r["n"][1]
            e1, e0 = r["NE"]["e"], r["SW"]["e"]
            if e0 <= t_ <= e1:
                bed.append(q)
            elif e1 < t_ <= e1 + SPOT_BANK_M or e0 - SPOT_BANK_M <= t_ < e0:
                bank.append(q)
        spot_lab = []
        for pts, low, mx_, colr, kind in ((bed, True, SPOT_MAX[0], COL["river_dark"], "spot_bed"),
                                          (bank, False, SPOT_MAX[1], COL["ink_dark"], "spot_bank")):
            kept = []
            for q in sorted(pts, key=lambda q: q[2] if low else -q[2]):
                if len(kept) >= mx_:
                    break
                if all(math.hypot(q[0] - p[0], q[1] - p[1]) >= SPOT_GAP_M for p in kept):
                    kept.append(q)
            for q in kept:
                x, y = T(q)
                pg.line([(x - 0.7, y), (x + 0.7, y)], colr, 0.25)
                pg.line([(x, y - 0.7), (x, y + 0.7)], colr, 0.25)
                taken.append((x - 0.8, y - 0.8, x + 0.8, y + 0.8))
                leg(("dt", kind))
                spot_lab.append(([(u"+{:.2f}".format(q[2]), DT_TS * 0.85, False)], (x, y), colr))
        # ---- labels: cuts, route, bridge, planting codes, spot levels (zone words follow in draw_area)
        for lines, anc in cut_lab:
            if not place_label(pg, lines, anc, taken, dw, dh, ink, avoid=av):
                missing.append(lines[0][0])
        for lines, anc, along in route_lab:              # v22: never left out (Aras 26 Oct: 4 BACK TO THE STREAM)
            if not place_label(pg, lines, anc, taken, dw, dh, COL["river_dark"], d0=2.6, avoid=av, more=along,
                               anywhere=True):
                missing.append(lines[0][0])
        for nm in (u"K4", u"K5"):                         # (not when the commons' keywords already name it)
            if plc.get(nm) and inR(plc[nm]) and nm + u" BRIDGE" not in HUB.get(win["key"], (u"", []))[1]:
                if not place_label(pg, [(nm + u" BRIDGE", DT_TS, True)], T(plc[nm]), taken, dw, dh, ink, d0=2.0,
                                   avoid=av):
                    missing.append(nm + u" BRIDGE")
        for z in D.zones:
            pl = ZONE_PLANTING.get((z["code"], z["tier"])) or ZONE_PLANTING.get((z["code"], None))
            if not pl or not any(inR(p) for p in z["P"]):
                continue
            TP = z["TP"] if z.get("area") == win["key"] and z.get("TP") else [T(p) for p in z["P"]]
            TP = clip_ring(TP, (0.0, 0.0, dw, dh))
            txt = u"{} · {}".format(u" ".join(pl[0]), u" ".join(pl[1]))
            b_ = None
            if len(TP) >= 3:
                TPs = thin(TP, 300)
                for sz in (DT_TS, DT_TS * 0.85):
                    b_ = fit_inside(TPs, inside_spots(TPs), [(txt, sz, False)], taken, pad=0.4, avoid=av)
                    if b_:
                        pg.text(txt, b_[0] + 0.4, b_[1] + 0.4 + 0.06 * sz, sz, zone_tones(z)[2])
                        taken.append(b_)
                        break
            if b_:
                for b_ in pl[0]:
                    leg(("band", b_))
                for c_ in pl[1]:
                    leg(("sp", c_))
            else:
                missing.append(txt + u" (" + name_of(z, z.get("own", "")) + u")")
        for lines, anc, colr in spot_lab:
            place_label(pg, lines, anc, taken, dw, dh, colr, d0=0.6, leader=False, avoid=av)
    return f


def detail_legend():
    """v21: the detail sheet's legend groups (only what it draws): its layers, the planting bands, species codes."""
    W_ = COL["white"]

    def line_sw(*specs):
        def f(pg, x, y, w, h):
            for c_, lw, dash, a_ in specs:
                pg.line([(x, y + h / 2), (x + w, y + h / 2)], c_, lw, dash, cap=0 if dash else 1, alpha=a_)
        return f

    def cross_sw(colr):
        def f(pg, x, y, w, h):
            cx, cy = x + w / 2, y + h / 2
            pg.line([(cx - 1.4, cy), (cx + 1.4, cy)], colr, 0.3)
            pg.line([(cx, cy - 1.4), (cx, cy + 1.4)], colr, 0.3)
        return f

    def steps_sw(pg, x, y, w, h):
        for i in range(4):
            yy = y + h * (i + 0.5) / 4
            pg.line([(x + 1.0, yy), (x + w - 1.0, yy)], MP["storage"][2], 0.3, alpha=0.75)

    def ramp_sw(pg, x, y, w, h):
        R_ = [(x, y + h * 0.1), (x + w, y + h * 0.35), (x + w, y + h * 0.65), (x, y + h * 0.9)]
        pg.poly([R_], fill=COL["ink2"], alpha=0.2)
        pg.poly([R_], stroke=COL["ink2"], lw=0.25)

    def route_sw(pg, x, y, w, h):
        pg.circle(x + w / 2, y + h / 2, 3.0, fill=COL["river_dark"])
        pg.text(u"1", x + w / 2, y + h / 2 - 1.2, 3.4, W_, bold=True, align="C")

    det = []
    for key, name, f in ((("dt", "cut"), u"SECTION · CHANNEL CUT", line_sw((COL["ink_dark"], 0.35, [4.0, 1.0, 0.6, 1.0], None))),
                         (("dt", "site"), u"SITE SECTION · SITE BOARD", line_sw((COL["ink2"], 0.3, [4.0, 1.0, 0.6, 1.0], None))),
                         (("dt", "q"), u"Q500 / Q100 WIDTH ON THE CUT",
                          line_sw((COL["river_mid"], 2.2, None, 0.45), (COL["river_dark"], 1.0, None, 0.45))),
                         (("dt", "route"), u"WATER ROUTE · STEP", route_sw),
                         (("dt", "spot_bed"), u"SPOT LEVEL · BED (m)", cross_sw(COL["river_dark"])),
                         (("dt", "spot_bank"), u"SPOT LEVEL · BANK TOP (m)", cross_sw(COL["ink_dark"])),
                         (("dt", "steps"), u"TERRACE STEPS", steps_sw),
                         (("dt", "ramp"), u"RAMP", ramp_sw)):
        if key in LEG:
            det.append((name, f))

    def none_sw(pg, x, y, w, h):
        return None
    if ("dt", "vol") in LEG:                             # v22: how the rough volumes are made
        det.append((u"~ m³ = ROUGH VOLUME, AREA × DEPTH · REED BASINS 0.46 m (EPA 2000) · TERRACES 0.30 m (DESIGN)", none_sw))
    bands = [(BAND_NAME[b_], none_sw) for b_ in "ABCDEF" if ("band", b_) in LEG]
    sp = [(u"{}  {}".format(c_, nm), none_sw) for c_, nm in SPECIES_CODE if ("sp", c_) in LEG]
    return [(u"DETAIL", det), (u"PLANTING BANDS · DAYS WET", bands), (u"SPECIES", sp)]


def crop_legend(keys, alpha):
    """v21: a panel's legend for its booklet crop (drawn samples as colours + plain names)."""
    W_ = COL["white"]
    out = []

    def add(kind, colour, label):
        if all(e["label"] != label for e in out):
            out.append({"kind": kind, "colour": colour, "label": label})
    for code, name in LEG_ZONE:
        if ("zone", code) in keys:
            z = {"code": "WA" if code == "WAF" else code, "tier": "F" if code == "WAF" else "D"}
            add("fill", mix(W_, zone_tones(z)[0], alpha), name.split(u" · ")[-1].lower())
    if "river_band" in keys:
        add("fill", mix(W_, RIVER_BAND_TONE[0], 0.85), RIVER_BAND_NAME.lower())
    for nm_ in (u"MAIN SPINE", u"STREAMSIDE SPINE"):
        if ("spinezone", nm_) in keys:
            add("fill", mix(W_, MP["centre"][0], alpha), nm_.lower())
    if ("ctx", "river") in keys:
        add("fill", PIECE_TONE["river"][0], u"stream")
    if ("road", "main") in keys:
        add("line", ROAD_TONE[2], u"main road")
    if ("road", "street") in keys or ("ctx", "street") in keys:
        add("line", ROAD_TONE[1], u"street")
    if ("walk", "bank") in keys:
        add("line", COL["walk"], u"bank walk, car-free")
    for key, kind, colour, label in ((("dt", "cut"), "line", COL["ink_dark"], u"section"),
                                     (("dt", "q"), "line", COL["river_mid"], u"Q500 width on the cut"),
                                     (("dt", "route"), "dot", COL["river_dark"], u"water route step"),
                                     (("dt", "spot_bed"), "dot", COL["river_dark"], u"spot level, bed"),
                                     (("dt", "spot_bank"), "dot", COL["ink_dark"], u"spot level, bank top"),
                                     (("dt", "steps"), "line", MP["storage"][2], u"terrace steps"),
                                     (("dt", "ramp"), "fill", mix(W_, COL["ink2"], 0.2), u"ramp")):
        if key in keys:
            add(kind, colour, label)
    return out


def booklet_crops(folder, sheets, wins, plc, missing):
    """v21: booklet/blocks.json (one crop per panel of every sheet) and booklet/results.json (as v20's keys:
    script, version, option, frames under the old booklet ids, labels_not_drawn, places_xy)."""
    bk = BkBlocks(folder, u"MasterPlan", SHORT)
    for old in ("c1_s1.pdf", "c1_s2.pdf", "c3_a.pdf", "c3_b.pdf"):   # v20's separate drawings: now crops
        try:
            os.remove(bk.path(old))
        except OSError:
            pass
    res = {"script": "bergama_masterplan_v22.py", "version": VERSION, "option": "A", "frames": {},
           "labels_not_drawn": {}, "places_xy": dict((k_, [round(v[0], 1), round(v[1], 1)])
                                                     for k_, v in sorted(plc.items()))}
    wd = dict((w["id"], w) for w in wins)
    drop = [r"^1:[\d,.]+$"]                               # the sheet's scale text: the booklet prints its own
    for pdf, sh, scale in sheets:
        for key, rc, p in sh.panels:
            bid, old, cap = p.bid
            bk.crop(bid, os.path.basename(pdf), rc, caption=cap, scale_den=scale, legend=crop_legend(p.pleg, _ALPHA[0]),
                    drop=drop)
            fr = {"crop": bid, "scale_den": scale, "w_mm": round(rc[2] - rc[0], 1), "h_mm": round(rc[3] - rc[1], 1)}
            if bid in wd:
                R = wd[bid]["R"]
                fr.update(centre_xy=[round((R[0] + R[2]) / 2, 1), round((R[1] + R[3]) / 2, 1)],
                          window_m=[round(R[2] - R[0], 1), round(R[3] - R[1], 1)])
            else:                                         # the masterplan panel's world extent (survey x, m)
                R = p.world
                fr.update(from_m=round(R[0], 1), to_m=round(R[2], 1), overlap_m=0.0)
            res["frames"][old] = fr
            res["labels_not_drawn"][old] = missing.get(bid, [])
    with open(bk.path("results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    return bk.save()
def make_board(opt, alt, pages, title=None):
    """The working areas side by side (two rows when wider than BOARD_MAX_W) under the sheet's title. v21: the
    result's .panels = [(key, crop rect in page mm from the top-left, y down)] for the booklet's crops."""
    M, HEAD, G = 14.0, 24.0, 10.0
    rows = [pages]
    if sum(p.W for p in pages) + G * (len(pages) - 1) + 2 * M > BOARD_MAX_W:
        rows = [pages[:2], pages[2:]]
    W = max(sum(p.W for p in r_) + G * (len(r_) - 1) for r_ in rows) + 2 * M
    H = sum(max(p.H for p in r_) for r_ in rows) + G * (len(rows) - 1) + 2 * M + HEAD
    bd = Page(W, H)
    bd.poly([rect(0, 0, W, H)], fill=COL["paper"])
    sheet_head(bd, M, H - M, alt, opt, title)
    y = H - M - HEAD
    at = []
    for r_ in rows:
        x = M
        hr = max(p.H for p in r_)
        for p in r_:
            blit(bd, p, x, y - p.H)
            at.append((p, x, y - p.H))
            x += p.W + G
        y -= hr + G
    sh = add_legend(bd, alt, _ALPHA[0], M)               # v17
    dy = sh.H - bd.H                                     # the legend band added under the board
    sh.panels = []
    for p, x, y0 in at:
        c = getattr(p, "crop", None)
        if c:
            x0, x1, yb, yt = x + c[0], x + c[2], y0 + dy + c[1], y0 + dy + c[3]
            sh.panels.append((getattr(p, "key", None), (x0, sh.H - yt, x1, sh.H - yb), p))
    return sh


# ================================================================ v17: the legend band (only what the sheet draws)
LEG = {}                       # what the sheet being drawn uses: key -> sample data (reset for every sheet)
LEG_ZONE = [("WS", u"WATER STORAGE · RETENTION TERRACES"), ("WT", u"CLEANING · REED BASINS"),
            ("WD", u"CLEAN WATER BACK · SPILLWAY"), ("WA", u"AMPHIBIOUS · BED"),
            ("WAF", u"AMPHIBIOUS · FLOOD TERRACE"), ("WP", u"STREAMSIDE PLANTING"),
            ("GR", u"GREEN · SHADED WALK, DRY TOP"), ("DG", u"DEMETER'S GARDEN"), ("WI", u"AGRICULTURE"),
            ("CH", u"HERITAGE"), ("MC", u"CENTRE"), ("HO", u"HOUSING"), ("CV", u"CIVIC"), ("SR", u"SPORT"),
            ("PA", u"SERVICE")]
LEG_CTX = [("river", u"STREAM"), ("street", u"STREET"), ("park", u"PARK"), ("heritage", u"HERITAGE BUILDING"),
           ("housing", u"HOUSING"), ("building", u"OTHER BUILDING"), ("cleared", u"CLEARED GROUND")]
LEG_SW, LEG_SH, LEG_ROW, LEG_TS, LEG_HS, LEG_GAP = 22.0, 8.0, 11.0, 3.4, 4.0, 14.0   # sizes, mm


_PLEG = [None]                 # v21: the legend keys of the panel being drawn (its booklet crop's legend)


def leg(key, val=True):
    LEG.setdefault(key, val)
    if _PLEG[0] is not None:
        _PLEG[0].setdefault(key, val)


def leg_zone(z):
    leg(("zone", "WAF" if z["code"] == "WA" and z["tier"] == "F" else z["code"]), z["tier"])


def legend_groups(alt, alpha):
    """[(heading, [(name, draw(pg, x, y, w, h))])] of what LEG holds, in a fixed order."""
    W_ = COL["white"]

    def zone_sw(code, tier):
        def f(pg, x, y, w, h):
            z = {"code": code, "tier": tier, "id": "legend", "q": (0.0, 0.0)}
            lt, md, dk = zone_tones(z)
            TP = rect(x, y, x + w, y + h)
            pg.poly([TP], fill=W_)
            pg.poly([TP], fill=lt, alpha=alpha)
            pg.poly([TP], stroke=COL["ink2"], lw=0.15)
        return f

    def fill_sw(fill, stroke=None, lw=0.15, dash=None, alpha_=None):
        def f(pg, x, y, w, h):
            pg.poly([rect(x, y, x + w, y + h)], fill=fill, alpha=alpha_)
            pg.poly([rect(x, y, x + w, y + h)], stroke=stroke or COL["ink2"], lw=lw, dash=dash)
        return f

    def line_sw(*specs):                                   # (colour, lw, dash, alpha) drawn in order
        def f(pg, x, y, w, h):
            for c_, lw, dash, a_ in specs:
                pg.line([(x, y + h / 2), (x + w, y + h / 2)], c_, lw, dash, cap=0 if dash else 1, alpha=a_)
        return f

    zones = []
    for code, name in LEG_ZONE:
        if ("zone", code) in LEG:
            zones.append((name, zone_sw("WA" if code == "WAF" else code, LEG[("zone", code)])))
    for (k_, code), tier in sorted([(k_, v) for k_, v in LEG.items() if k_[0] == "zone"
                                    and k_[1] not in dict(LEG_ZONE)]):
        zones.append((code, zone_sw(code, tier)))
    if "hub" in LEG:
        tones = LEG["hub"]

        def hub_sw(pg, x, y, w, h):
            n = len(tones)
            for i, t_ in enumerate(tones):
                pg.poly([rect(x + w * i / n, y, x + w * (i + 1) / n, y + h)], fill=t_)
        zones.append((u"COMMONS · WHERE THE PROGRAMMES MEET", hub_sw))
    zl = [code for code, _ in LEG_ZONE if ("zone", code) in LEG]
    if len(zl) >= 2:
        a_, b_ = [zone_tones({"code": "WA" if c_ == "WAF" else c_, "tier": "F" if c_ == "WAF" else "D"})[0]
                  for c_ in zl[:2]]

        def ov_sw(pg, x, y, w, h):
            r1, r2 = rect(x, y, x + w * 0.62, y + h), rect(x + w * 0.38, y, x + w, y + h)
            pg.poly([r1], fill=W_)
            pg.poly([r2], fill=W_)
            pg.poly([r1], fill=a_, alpha=alpha)
            pg.poly([r2], fill=b_, alpha=alpha)
        zones.append((u"OVERLAP · SHARED USE (DARKER)", ov_sw))
    if "river_band" in LEG:
        def rb_sw(pg, x, y, w, h):
            lt, md, dk = RIVER_BAND_TONE
            pg.poly([rect(x + 0.8, y - 0.8, x + w + 0.8, y + h - 0.8)], fill=dk, alpha=0.22)
            pg.poly([rect(x, y, x + w, y + h)], fill=lt, alpha=0.85)
            pg.poly([rect(x, y, x + w, y + h)], stroke=dk, lw=0.35)
        zones.append((RIVER_BAND_NAME, rb_sw))
    for nm_ in (u"MAIN SPINE", u"STREAMSIDE SPINE"):
        if ("spinezone", nm_) in LEG:
            zones.append((nm_, fill_sw(mix(W_, MP["centre"][0], alpha))))
    if "strip" in LEG:
        zones.append((u"NEW WATER STRIP", fill_sw(COL["river"], COL["river_dark"], 0.3, [1.2, 0.7])))
    if "cleared" in LEG:
        zones.append((u"BUILDING CLEARED", fill_sw(W_, COL["ink2"], 0.3, [0.9, 0.6])))

    ctx = []
    for kind, name in LEG_CTX:
        if ("ctx", kind) in LEG:
            ctx.append((name, fill_sw(PIECE_TONE[kind][0])))
    surv = [(("s", "contour"), u"CONTOURS", line_sw((COL["contour10"], 0.3, None, None))),
            (("s", "park"), u"EXISTING PARK", fill_sw(COL["park"])),
            (("s", "pond"), u"POND", fill_sw(COL["river"])),
            (("road", "main"), u"MAIN ROAD", line_sw((ROAD_TONE[2], ROAD_LW[1], None, None))),     # v21
            (("road", "street"), u"STREET EDGE", line_sw((ROAD_TONE[1], ROAD_LW[0], None, None))),
            (("s", "building"), u"BUILDING", fill_sw(COL["bld"], COL["bld_edge"])),
            (("s", "heritage"), u"HERITAGE BUILDING", fill_sw(COL["her"], COL["her_edge"])),
            (("s", "tree"), u"TREE", None),
            (("line", "river_mid"), u"STREAM AND BANK LINES", line_sw((COL["river_mid"], 0.3, None, None))),
            (("line", "histwall"), u"HISTORIC WALL", line_sw((COL["histwall"], 0.3, [1.2, 0.5], None))),
            (("line", "ink"), u"BRIDGE", line_sw((COL["ink"], 0.5, None, None)))]
    for key, name, f in surv:
        if key in LEG:
            if f is None:
                def f(pg, x, y, w, h):
                    for i in range(3):
                        pg.circle(x + w * (i + 0.5) / 3, y + h / 2, h * 0.3, fill=COL["tree"], alpha=0.85)
            ctx.append((name, f))

    lines = []
    if ("walk", "bank") in LEG:
        lines.append((u"BANK WALK · CAR-FREE", line_sw((W_, 1.5, None, None), (COL["walk"], 0.7, None, None))))
    if ("walk", "street") in LEG:
        lines.append((u"STREET WALK", line_sw((W_, 1.5, None, None), (COL["walk"], 0.7, [2.2, 0.8], None))))
    if ("walk", "bed") in LEG:
        lines.append((u"BED WALK · CLOSED IN FLOODS",
                      line_sw((W_, 1.5, None, None), (COL["river_dark"], 0.7, [0.5, 0.6], None))))
    band = max(1.6, SPINE_W_M * 1000.0 / _SCALE[0])
    if "main" in LEG:
        lines.append((u"MAIN SPINE", line_sw((COL["spine"], band * 1.25, None, 0.55),
                                             (COL["spine_dark"], 0.35, None, None))))
    if ("spine", "edge") in LEG or ("spine", "over") in LEG:
        lines.append((u"STREAMSIDE SPINE", line_sw((COL["spine"], band, None, 0.75))))
    if ("spine", "deck") in LEG:
        lines.append((u"STREAMSIDE SPINE · DECK", line_sw((COL["spine"], band, [1.4, 0.9], 0.75))))
    if "path" in LEG:
        lines.append((u"PATH", line_sw((W_, 1.9, None, None), (COL["path"], 1.0, [1.0, 0.35], None))))

    links = []
    for kd in ("water", "flood", "people", "other"):
        if ("link", kd) in LEG:
            name = {"water": u"WATER MOVES", "flood": u"HIGH WATER SPREADS", "people": u"PEOPLE TO THE WATER",
                    "other": u"LINK"}[kd]

            def f(pg, x, y, w, h, kd=kd):
                link_arrow(pg, [(x, y + h / 2), (x + w, y + h / 2)], kd,
                           LINK_TYPES[kd]["heads"] if kd in LINK_TYPES else 1, 3)
            links.append((name, f))
    if "stop" in LEG:
        def f(pg, x, y, w, h):
            pg.circle(x + w / 2, y + h / 2, 2.65, fill=W_)
            pg.circle(x + w / 2, y + h / 2, 2.3, fill=COL["accent"])
            pg.text(u"1", x + w / 2, y + h / 2 - 1.0, 2.8, W_, bold=True, align="C")
        links.append((u"STOP", f))
    return [(u"ZONES", zones), (u"AROUND THE ZONES", ctx),
            (u"WALKS AND SPINES", lines), (u"LINKS", links)] + detail_legend()      # v21: detail sheet groups


def add_legend(sh, alt, alpha, M):
    """sh with a legend band under it: one column per group, wrapped into rows at the sheet width."""
    cols = []
    for head, items in legend_groups(alt, alpha):
        if items:
            w = LEG_SW + 3.0 + max([text_w(n, LEG_TS, True) for n, _ in items] +
                                   [text_w(head, LEG_HS, True) - LEG_SW - 3.0])
            cols.append((head, items, w))
    if not cols:
        return sh
    rows, cur, cw = [], [], 0.0
    for c in cols:
        if cur and cw + c[2] > sh.W - 2 * M:
            rows.append(cur)
            cur, cw = [], 0.0
        cur.append(c)
        cw += c[2] + LEG_GAP
    rows.append(cur)
    hs = [LEG_HS + 4.0 + max(len(c[1]) for c in r_) * LEG_ROW for r_ in rows]
    LH = sum(hs) + 6.0 * (len(rows) - 1) + M
    pg = Page(sh.W, sh.H + LH)
    pg.poly([rect(0, 0, pg.W, pg.H)], fill=COL["paper"])
    blit(pg, sh, 0.0, LH)
    y = LH
    for r_, h in zip(rows, hs):
        x = M
        for head, items, w in r_:
            pg.text(head, x, y - LEG_HS, LEG_HS, COL["ink_dark"], bold=True)
            yy = y - LEG_HS - 4.0
            for name, f in items:
                f(pg, x, yy - LEG_SH, LEG_SW, LEG_SH)
                pg.text(name, x + LEG_SW + 3.0, yy - LEG_SH / 2 - LEG_TS * 0.35, LEG_TS, COL["ink"], bold=True)
                yy -= LEG_ROW
            x += w + LEG_GAP
        y -= h + 6.0
    return pg


def sheet_head(pg, x, y_top, alt, opt, title=None):
    pg.text(u"BERGAMA · GROUP 6 · " + (title or ALT_TEXT[alt]), x, y_top - 7.0, 7.0, COL["ink_dark"], bold=True)
    pg.text(OPTION_TEXT[opt], x, y_top - 13.0, 3.4, COL["ink"], bold=True)
    pg.text(CREDIT, x, y_top - 18.0, 2.6, COL["ink"])
    scale_bar(pg, x + 170.0, y_top - 13.0, _SCALE[0])


def scale_bar(pg, x, y, scale, marks=(0.0, 50.0, 100.0, 200.0)):
    """v16: 0-50-100-200 m bar (ink and white blocks) and the scale as text, at the print scale 1:scale (v21: marks
    may be given: the detail windows use 0-10-20-50 m)."""
    k = 1000.0 / scale                                    # page mm per metre
    for i, (a, b) in enumerate(zip(marks[:-1], marks[1:])):
        pg.poly([rect(x + a * k, y, x + b * k, y + 1.2)], fill=COL["ink_dark"] if i % 2 == 0 else COL["white"],
                stroke=COL["ink_dark"], lw=0.15)
    for m_ in marks:
        pg.text(u"{:.0f}{}".format(m_, u" m" if m_ == marks[-1] else u""), x + m_ * k, y + 2.2, 2.0, COL["ink"],
                align="C")
    pg.text(u"1:{:,.0f}".format(scale), x + marks[-1] * k + 6.0, y - 0.1, 3.4, COL["ink_dark"], bold=True)


# ================================================================ v11: the riverside walks (Thread 5)
# Survey-based, recomputed on every press from the open file (the copy of the course survey's results is the
# fallback). From the stream's reference line (STREAM_REF), every WALK_STEP m, a line square to the stream finds
# the channel edge on each bank and how much ground is free of buildings behind it:
#   edge   the outermost water line / channel top (HIDRO_DERE_SULU, SEV_SEVUST) within EDGE_WATER m; else the bank
#          top (SEV_UST) within EDGE_TOP m; else the nearest wall or building within EDGE_WALL m (masonry banks)
#   free   from the edge to the first building outline (BINA_* except sheds; buildings the zone base clears are
#          ignored)
#   class  bank walk     free >= WALK_W + WALK_CLEAR, no street on it
#          street walk   the same, but a surveyed carriageway edge (YOL_SOSE / YOL_BORDUR) lies on it: the walk
#                        is the footway of an existing street
#          bed walk      no room on the bank, but the channel is at least BED_MIN_W wide: the walk drops to a
#                        terrace in the bed beside the water strip; it closes in floods (flood rule, Thread 4)
#          none          no room on the bank and a narrow channel
# Over the covered reach (STREAM_REF's tunnel pieces, joined across open gaps under COVER_JOIN m) there are no
# bank walks: the riverside spine runs on the street over the stream there. Runs shorter than WALK_MIN_RUN m are
# dropped, gaps up to WALK_GAP m inside one class are closed; edge distances are smoothed over 5 stations.
# Graphic and design values, not data: WALK_W (the water balance's 3 m riverside walk), WALK_CLEAR, BED_MIN_W.
WALK_STEP = 2.0
WALK_W = 3.0
WALK_CLEAR = 0.5
BED_MIN_W = 10.0               # 4 m water strip + 3 m walk + 3 m to spare (design rule)
EDGE_WATER, EDGE_TOP, EDGE_WALL = 45.0, 90.0, 35.0
WALK_SEARCH = 60.0
WALK_MIN_RUN = 25.0
WALK_GAP = 10.0
COVER_JOIN = 60.0
WALK_WIN, WALK_JUMP = 15, 6.0        # stations and m: an edge this far off its neighbours is a stray line
WALK_ROLES = dict(water=("stream", "chan_top"), top=("bank_top",), obst=("building", "housing", "heritage"),
                  wall=("wall",), road=("road", "kerb"))


class SegGrid(object):
    """Segments bucketed in C-m cells; crossings of a ray with them."""

    def __init__(self, lines, skip=None, c=10.0):
        self.c, self.g = c, {}
        for P in lines:
            for a, b in zip(P, P[1:]):
                a, b = (a[0], a[1]), (b[0], b[1])
                if skip is not None and skip(((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)):
                    continue
                for gx in range(int(math.floor(min(a[0], b[0]) / c)), int(math.floor(max(a[0], b[0]) / c)) + 1):
                    for gy in range(int(math.floor(min(a[1], b[1]) / c)), int(math.floor(max(a[1], b[1]) / c)) + 1):
                        self.g.setdefault((gx, gy), []).append((a, b))

    def cross(self, p, u, t0, t1):
        """Sorted parameters t in [t0, t1] where the ray p + t u crosses a segment."""
        c = self.c
        n = int(abs(t1 - t0) / (c / 2.0)) + 2
        cells = set()
        for k in range(n + 1):
            t = t0 + (t1 - t0) * k / float(n)
            x, y = p[0] + u[0] * t, p[1] + u[1] * t
            gx, gy = int(math.floor(x / c)), int(math.floor(y / c))
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    cells.add((gx + dx, gy + dy))
        out, seen = [], set()
        for cell in cells:
            for a, b in self.g.get(cell, ()):
                if (a, b) in seen:
                    continue
                seen.add((a, b))
                ex, ey = b[0] - a[0], b[1] - a[1]
                den = u[0] * ey - u[1] * ex
                if abs(den) < 1e-12:
                    continue
                wx, wy = a[0] - p[0], a[1] - p[1]
                t = (wx * ey - wy * ex) / den
                v = (wx * u[1] - wy * u[0]) / den
                if t0 <= t <= t1 and 0.0 <= v <= 1.0:
                    out.append(t)
        return sorted(out)


def stream_ref():
    """(points, covered flag per segment) of the reference line, the covered reach joined across short gaps."""
    R_ = json.loads(zlib.decompress(base64.b64decode("".join(STREAM_REF))).decode("utf-8"))
    P = [tuple(p) for p in R_["P"]]
    cov = list(R_["covered"])
    L = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(P, P[1:])]
    idx = [i for i, c in enumerate(cov) if c]
    for i, j in zip(idx, idx[1:]):
        if j - i > 1 and sum(L[i + 1:j]) < COVER_JOIN:
            for k in range(i + 1, j):
                cov[k] = True
    return P, cov


def walk_stations(P, cov, step):
    """(point, unit tangent, covered, chainage m) every step m along P."""
    out, s0 = [], 0.0
    for i, (a, b) in enumerate(zip(P, P[1:])):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L < 1e-9:
            continue
        n = max(1, int(L // step))
        t = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        for k in range(n):
            f = k / float(n)
            out.append(((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f), t, cov[i], s0 + L * f))
        s0 += L
    return out


def _median(v):
    v = sorted(v)
    return v[len(v) // 2]


def river_walks(survey, removes=()):
    """{"runs": [{"bank", "cls", "P", "m", "ch0", "ch1"}], "covered": [P], "stats": {...}} from the survey roles.
    removes: polygons of the buildings the zone base clears (their outlines do not block a walk)."""
    rm = [r for r in removes if len(r) >= 3]
    skip = (lambda q: any(pip(q[0], q[1], r) for r in rm)) if rm else None
    G = dict((k, SegGrid([P for role in roles for P in survey.get(role, [])], skip if k == "obst" else None))
             for k, roles in WALK_ROLES.items())
    P, cov = stream_ref()
    st = walk_stations(P, cov, WALK_STEP)
    rows = []
    for p, t, cv, ch in st:
        nl = (-t[1], t[0])                                # left of the flow: the north-east bank
        row = {"p": p, "n": nl, "cov": cv, "ch": ch}
        rows.append(row)
        if cv:
            continue
        w = G["water"].cross(p, nl, -EDGE_WATER, EDGE_WATER)
        if len(w) >= 2:                                   # the channel between its outermost water lines
            row["NE"], row["SW"] = {"e": w[-1], "water": True}, {"e": w[0], "water": True}
            row["width"] = w[-1] - w[0]
            continue
        for key, lim in (("top", EDGE_TOP), ("wall", EDGE_WALL)):
            x = G["top"].cross(p, nl, -lim, lim) if key == "top" else \
                G["obst"].cross(p, nl, -lim, lim) + G["wall"].cross(p, nl, -lim, lim)
            pos, neg = [v for v in x if v > 0.5], [v for v in x if v < -0.5]
            if pos and neg:
                row["NE"], row["SW"] = {"e": min(pos), "water": False}, {"e": max(neg), "water": False}
                row["width"] = min(pos) - max(neg)
                break
    # edges: drop jumps (more than WALK_JUMP m off the median of WALK_WIN stations), then smooth over 5
    for side, sg in (("NE", 1.0), ("SW", -1.0)):
        E = [r[side]["e"] if r.get(side) else None for r in rows]
        for i, r in enumerate(rows):
            if E[i] is None:
                continue
            near = [E[j] for j in range(max(0, i - WALK_WIN // 2), min(len(rows), i + WALK_WIN // 2 + 1)) if E[j] is not None]
            if abs(E[i] - _median(near)) > WALK_JUMP:
                r[side] = None
        E = [r[side]["e"] if r.get(side) else None for r in rows]
        for i, r in enumerate(rows):
            if E[i] is None:
                continue
            r[side]["e"] = _median([E[j] for j in range(max(0, i - 2), min(len(rows), i + 3)) if E[j] is not None])
        for r in rows:
            s = r.get(side)
            if not s:
                continue
            p, nl, e = r["p"], r["n"], s["e"]
            ob = sorted(sg * x - sg * e for x in G["obst"].cross(p, nl, *sorted((e, e + sg * WALK_SEARCH)))
                        if sg * x - sg * e > 0.05)
            s["free"] = ob[0] if ob else WALK_SEARCH
            s["street"] = bool(G["road"].cross(p, nl, *sorted((e, e + sg * (WALK_W + 1.0)))))
            if s["free"] >= WALK_W + WALK_CLEAR:
                s["cls"] = "street" if s["street"] else "bank"
                s["pos"] = e + sg * (WALK_CLEAR + WALK_W / 2.0)
            elif r.get("width", 0.0) >= BED_MIN_W:
                s["cls"] = "bed"
                s["pos"] = e - sg * (WALK_W / 2.0 + WALK_CLEAR)
            else:
                s["cls"] = None
    # runs of one class per bank
    runs = []
    for side, sg in (("NE", 1.0), ("SW", -1.0)):
        cur = None
        for r in rows + [None]:
            s = r.get(side) if r else None
            c = s["cls"] if s else None
            if cur and (r is None or c != cur["cls"] or r["ch"] - cur["ch1"] > WALK_STEP * 1.5):
                runs.append(cur)
                cur = None
            if c:
                q = (r["p"][0] + r["n"][0] * s["pos"], r["p"][1] + r["n"][1] * s["pos"])
                if cur is None:
                    cur = {"bank": side, "cls": c, "P": [], "C": [], "ch0": r["ch"]}
                cur["P"].append(q)
                cur["C"].append(r["ch"])
                cur["ch1"] = r["ch"]
    # close short gaps inside one class, drop short runs
    out = []
    for side in ("NE", "SW"):
        rs = sorted([x for x in runs if x["bank"] == side], key=lambda x: x["ch0"])
        merged = []
        for x in rs:
            y = merged[-1] if merged else None
            if y and y["cls"] == x["cls"] and x["ch0"] - y["ch1"] <= WALK_GAP + WALK_STEP:
                y["P"] += x["P"]
                y["C"] += x["C"]
                y["ch1"] = x["ch1"]
            else:
                merged.append(x)
        out += [x for x in merged if x["ch1"] - x["ch0"] >= WALK_MIN_RUN]
    for x in out:
        x["m"] = arclen(x["P"])[-1] if len(x["P"]) > 1 else 0.0
    covered, cur = [], None
    for (a, b), c in zip(zip(P, P[1:]), cov):
        if c:
            if cur is None:
                cur = [a]
            cur.append(b)
        elif cur:
            covered.append(cur)
            cur = None
    if cur:
        covered.append(cur)
    stats = {}
    for x in out:
        k = x["bank"] + " " + x["cls"]
        stats[k] = stats.get(k, 0.0) + x["m"]
    return {"runs": out, "covered": covered, "stats": stats, "ref": P, "rows": rows}   # v21: rows for the promenade


# ================================================================ v21: the promenade beside the stream
# Aras 25 Oct 21:38: "promenade is just too thick that it covers the whole river however it should be alongside
# river like covering %10 on left and %10 on right and rest should extend to the roadside". At every station of
# river_walks (WALK_STEP m along STREAM_REF), on each bank: from PROM_IN x the stream's width inside the water edge
# (the edge river_walks found) out to the first surveyed street edge (YOL_SOSE / YOL_BORDUR) within PROM_SEARCH_M;
# a standing building (BINA_*, not cleared by the zone base) met first stops it there; with neither within
# PROM_SEARCH_M it ends PROM_FREE_M out. No band over the covered reach. The outer edge is a running median over
# PROM_WIN stations; option A's water edge wanders (organic only where the project meets the water).
PROM_IN = 0.10               # share of the stream's width the band reaches over the water (Aras: "%10")
PROM_SEARCH_M = 60.0         # the roadside is looked for this far beyond the water edge, m
PROM_FREE_M = 15.0           # no street or building within PROM_SEARCH_M: the band's width beyond the edge, m (graphic)
PROM_MIN_M = 1.0             # narrowest band beyond the edge (a street right at the water), m (graphic)
PROM_WIN = 9                 # stations of the running median of the outer edge
PROM_MIN_RUN = 12.0          # shorter runs are dropped, m
PROM_SLOPE = 0.6             # the outer edge widens at most this much per m along the stream (hugs the roadside)


def promenade(W, survey, removes, opt):
    """v21: the promenade's rings (world m), one per bank and run, and {"m2", "street_pct"} for the log."""
    rows = W.get("rows") or []
    if not rows:
        return [], {}
    rm = [r for r in removes if len(r) >= 3]
    skip = (lambda q: any(pip(q[0], q[1], r) for r in rm)) if rm else None
    Gr = SegGrid([P for role in WALK_ROLES["road"] for P in survey.get(role, [])])
    Go = SegGrid([P for role in WALK_ROLES["obst"] for P in survey.get(role, [])], skip)
    nz = _noise(101)
    loops, n_st, n_all = [], 0, 0
    for side, sg in (("NE", 1.0), ("SW", -1.0)):
        V = []
        for r in rows:
            s = r.get(side)
            if r["cov"] or not s or not r.get("width"):
                V.append(None)
                continue
            p, nl, e = r["p"], r["n"], s["e"]
            lo, hi = sorted((e, e + sg * PROM_SEARCH_M))
            st_ = [sg * x - sg * e for x in Gr.cross(p, nl, lo, hi)]
            ob_ = [sg * x - sg * e for x in Go.cross(p, nl, lo, hi)]
            st_ = [v for v in st_ if v > 0.3]
            ob_ = [v for v in ob_ if v > 0.05]
            n_all += 1
            if st_ and (not ob_ or min(st_) <= min(ob_)):
                n_st += 1
            out = min(st_ + ob_) if st_ or ob_ else PROM_FREE_M
            V.append([e, r["width"], max(PROM_MIN_M, out)])
        runs, cur = [], []
        for i, v in enumerate(V + [None]):
            if v is None:
                if len(cur) * WALK_STEP >= PROM_MIN_RUN:
                    runs.append(cur)
                cur = []
            else:
                cur.append(i)
        for ix in runs:
            n = len(ix)
            for j in (1, 2):                             # width and outer edge: running median
                raw = [V[i][j] for i in ix]
                h = PROM_WIN // 2
                for a, i in enumerate(ix):
                    V[i].append(_median(raw[max(0, a - h):a + h + 1]))
            for seq in (ix, ix[::-1]):                   # the outer edge widens gently, narrows to the street
                for a, b in zip(seq, seq[1:]):
                    V[b][4] = min(V[b][4], V[a][4] + PROM_SLOPE * WALK_STEP)
            inner, outer = [], []
            for i in ix:
                r = rows[i]
                e, w, o = V[i][0], V[i][3], V[i][4]
                p, nl = r["p"], r["n"]
                f = 1.0 + (0.45 * nz(p[0], p[1]) if opt == "A" else 0.0)
                t_in = e - sg * PROM_IN * w * f
                t_out = e + sg * o
                inner.append((p[0] + nl[0] * t_in, p[1] + nl[1] * t_in))
                outer.append((p[0] + nl[0] * t_out, p[1] + nl[1] * t_out))
            if n < 3:
                continue
            outer = walk_form(outer, "B") if opt == "B" else \
                [outer[0]] + [tuple(sum(outer[j][c] for j in range(a - 2, a + 3)) / 5.0 for c in (0, 1))
                              for a in range(2, n - 2)] + [outer[-1]]
            inner = walk_form(inner, opt)
            Lp = inner + outer[::-1]
            Lp = chaikin(Lp, 2, closed=True) if opt == "A" else Lp
            if area2(Lp) < 0:
                Lp = Lp[::-1]
            loops.append(Lp)
    m2 = sum(abs(area2(L_)) for L_ in loops)
    return loops, {"m2": m2, "street_pct": 100.0 * n_st / max(1, n_all)}

# v11 constants (Thread 5)
SPINE_W_M = 6.0                # drawn width of the spines, m (graphic)
WALK_FACET_M = 4.0             # option B: walks as straight facets, Douglas-Peucker tolerance, m (graphic)
TREE_MIN_MM = 0.9              # smallest drawn tree, mm (graphic)
_BERGAMA = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
CITY_LINK_FILES = [os.path.join(_BERGAMA, "output", "Bergama_city_link_analysis", "city_link_results.json")]


def dp_open(P, tol):
    """Douglas-Peucker on an open line."""
    if len(P) < 3:
        return list(P)
    keep, st = [0, len(P) - 1], [(0, len(P) - 1)]
    while st:
        a, b = st.pop()
        dmax, im = 0.0, None
        for i in range(a + 1, b):
            d = seg_dist(P[i][0], P[i][1], P[a], P[b])
            if d > dmax:
                dmax, im = d, i
        if im is not None and dmax > tol:
            keep.append(im)
            st += [(a, im), (im, b)]
    return [P[i] for i in sorted(keep)]


def walk_form(P, opt):
    """Form rule (Aras 16 Oct): option A follows the river edge (a soft line, organic only where the project meets
    the water); option B is straight facets (Douglas-Peucker at WALK_FACET_M)."""
    if len(P) < 3:
        return list(P)
    if opt == "B":
        return dp_open(P, WALK_FACET_M)
    Q = [P[0]] + [tuple(sum(P[j][c] for j in range(i - 2, i + 3)) / 5.0 for c in (0, 1))
                  for i in range(2, len(P) - 2)] + [P[-1]]
    return dp_open(Q, 0.4)


def chain_at(P, q):
    """Chainage (m) along P of the point of P nearest q, and that distance."""
    best, s0 = (None, 1e18), 0.0
    for a, b in zip(P, P[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L > 1e-9:
            t = max(0.0, min(1.0, ((q[0] - a[0]) * (b[0] - a[0]) + (q[1] - a[1]) * (b[1] - a[1])) / (L * L)))
            d = math.hypot(a[0] + (b[0] - a[0]) * t - q[0], a[1] + (b[1] - a[1]) * t - q[1])
            if d < best[1]:
                best = (s0 + L * t, d)
        s0 += L
    return best


def ref_between(P, s0, s1):
    """The piece of P between chainages s0 < s1."""
    s = arclen(P)
    return sub_line(P, s, max(0.0, s0), min(s[-1], s1))


def city_link():
    """(spec, source) of the riverside spine: city_link_results.json of bergama_city_link (Thread 4), read live;
    else the copy embedded here (CITY_LINK_COPY). main_spine (the
    Bankalar - Kınık Caddesi line) from the file if it has one, else MAIN_SPINE below."""
    spec, src = None, None
    for p in CITY_LINK_FILES:
        try:
            with open(p, "r", encoding="utf-8") as fh:
                spec = json.load(fh)
            src = u"city link file of " + time.strftime("%d %b %H:%M", time.localtime(os.path.getmtime(p)))
            break
        except Exception:
            continue
    if spec is None:
        spec, src = json.loads(CITY_LINK_COPY), u"copy embedded in this script (city link file not found)"
    if not spec.get("main_spine"):
        spec["main_spine"] = MAIN_SPINE
    return spec, src


def spine_on_edge(spec, W):
    """The riverside spine on the real edge -> [{"id", "name", "kind", "P"}], kind edge (on the bank walk),
    deck (no room on the bank: a deck over the bed is needed, straight between the walk's ends) or over (on the
    street over the covered reach). Each piece runs between the chainages of its two anchors on STREAM_REF, on the
    bank city link decided by data (spine_banks: NE / SW / over; Thread 4, 24 Oct 09:14); without spine_banks, on
    the bank its side_ref stands on."""
    ref = W["ref"]
    banks = spec.get("spine_banks") or {}
    out = []
    for pc in spec.get("spine", []):
        s0, d0 = chain_at(ref, pc["frm"])
        s1, d1 = chain_at(ref, pc["to"])
        if s0 is None or s1 is None:
            continue
        if s1 < s0:
            s0, s1 = s1, s0
        name = pc.get("name", pc.get("id", ""))
        sb = banks.get(pc.get("id"))
        if sb == "over" or (sb not in ("NE", "SW") and (not pc.get("side_ref") or float(pc.get("offset_m", 0) or 0) <= 0)):
            out.append({"id": pc.get("id"), "name": name, "kind": "over", "P": ref_between(ref, s0, s1)})
            continue
        if sb in ("NE", "SW"):
            bank = sb
        else:
            r = pc["side_ref"]
            sr, _ = chain_at(ref, r)
            q, t = at_len(ref, arclen(ref), sr)
            bank = "NE" if t[0] * (r[1] - q[1]) - t[1] * (r[0] - q[0]) > 0 else "SW"
        pts = sorted([(c, p) for x in W["runs"] if x["bank"] == bank for c, p in zip(x["C"], x["P"])
                      if s0 <= c <= s1], key=lambda cp: cp[0])
        run_, last = [], None
        for c, p in pts:
            if last is not None and c - last[0] > WALK_GAP + WALK_STEP:
                if len(run_) > 1:
                    out.append({"id": pc.get("id"), "name": name, "kind": "edge", "P": run_})
                out.append({"id": pc.get("id"), "name": name, "kind": "deck", "P": [last[1], p]})
                run_ = []
            run_.append(p)
            last = (c, p)
        if len(run_) > 1:
            out.append({"id": pc.get("id"), "name": name, "kind": "edge", "P": run_})
        if not pts:                                       # no walk at all on that bank: the anchors, straight
            out.append({"id": pc.get("id"), "name": name, "kind": "deck", "P": [tuple(pc["frm"]), tuple(pc["to"])]})
    return out


def stop_points(spec, D, areas):
    """[(n, name, (x, y), placed_by)] of the spine's stops. A stop without xy is placed by a stated rule: stage
    "entry" -> the reed basins (largest WT zone) of the upstream entry, else that area's inner point; stop 8 (summer
    bed events) -> the largest bed zone (WA, tier W). Placement rules are graphic, not data."""
    out = []
    for f in spec.get("functions", []):
        n, nm = f.get("n"), f.get("name", "")
        if f.get("xy"):
            out.append((n, nm, (float(f["xy"][0]), float(f["xy"][1])), "city link"))
            continue
        cand = []
        if f.get("stage") == "entry":
            cand = [z for z in D.zones if z.get("own") == "aras_alan" and z["code"] == "WT"]
            if not cand and "calisma_alan[0]" in areas:
                out.append((n, nm, inner_pt(areas["calisma_alan[0]"]), "upstream entry, inner point"))
                continue
        else:
            cand = [z for z in D.zones if z["code"] == "WA" and z["tier"] == "W"]
        if cand:
            z = max(cand, key=lambda z: z["m2"])
            out.append((n, nm, z["q"], "largest " + ("reed basin" if f.get("stage") == "entry" else "bed zone")))
    return out


def city_layer(opt, D, areas, survey, warn):
    """Everything Thread 5 adds for one option: walks, the spine on the edge, the main spine, the stops."""
    W, src_w = None, u"survey of the open file"
    if survey.get("stream") or survey.get("chan_top") or survey.get("bank_top"):
        try:
            W = river_walks(survey, [r["P"] for r in D.removes])
        except Exception as ex:
            warn.append(u"option {}: the riverside walks were not computed ({}: {}); the embedded copy is "
                        u"used".format(opt, type(ex).__name__, ex))
    if W is None or not W["runs"]:
        cp = json.loads(zlib.decompress(base64.b64decode("".join(WALK_COPY))).decode("utf-8"))[opt]
        W = {"runs": cp["runs"], "covered": cp["covered"], "ref": stream_ref()[0], "stats": {}}
        for x in W["runs"]:
            x["P"] = [tuple(p) for p in x["P"]]
            x["m"] = arclen(x["P"])[-1] if len(x["P"]) > 1 else 0.0
            k_ = x["bank"] + " " + x["cls"]
            W["stats"][k_] = W["stats"].get(k_, 0.0) + x["m"]
        src_w = u"copy embedded in this script (from the course survey, 24 Oct)"
        warn.append(u"option {}: no stream / bank layers in the open file: the riverside walks are the embedded "
                    u"copy".format(opt))
    spec, src_c = city_link()
    sp = spine_on_edge(spec, W)
    if areas and WALK_CLIP:                              # v12: walks only inside calisma_alan (off, Aras 08:10)
        W["runs"] = clip_runs(W["runs"], areas)
        W["stats"] = {}
        for x in W["runs"]:
            k_ = x["bank"] + " " + x["cls"]
            W["stats"][k_] = W["stats"].get(k_, 0.0) + x["m"]
    for x in W["runs"]:
        x["F"] = walk_form(x["P"], opt)
    for s in sp:
        s["F"] = walk_form(s["P"], opt) if s["kind"] == "edge" else s["P"]
    m2 = sum(x["m"] for x in W["runs"]) * WALK_W
    prom, pst = promenade(W, survey, [r["P"] for r in D.removes], opt)       # v21
    if not prom:
        warn.append(u"option {}: no promenade drawn (no stream edges from the survey)".format(opt))
    return {"prom": prom, "prom_stats": pst, "W": W, "spine": sp, "main": [tuple(p) for p in spec["main_spine"]], "stops": stop_points(spec, D, areas),
            "src_walks": src_w, "src_city": src_c, "walk_m2": m2,
            "spine_m": dict((k_, sum(arclen(s["P"])[-1] for s in sp if s["kind"] == k_)) for k_ in ("edge", "deck", "over"))}


def draw_city(pg, T, CL, k, taken=None, stops=False, W_=None, H_=None, spines=True):
    """The main spine and the riverside spine (broad bands), the walks by class, and (alternative 3) the stops.
    T: world -> page; k: page mm per m."""
    tp = lambda P: [T(p) for p in P]
    band = max(1.6, SPINE_W_M * k)
    for M_ in ((CL["mains"] if "mains" in CL else [CL["main"]]) if spines else []):   # v18: spines=False, zones
        leg("main")
        pg.line(tp(M_), COL["spine"], band * 1.25, alpha=0.55)
        pg.line(tp(M_), COL["spine_dark"], 0.35)
    for s in (CL["spine"] if spines else []):
        leg(("spine", s["kind"]))
        if s["kind"] == "deck":
            pg.line(tp(s["F"]), COL["spine"], band, [1.4, 0.9], cap=0, alpha=0.75)
        else:
            pg.line(tp(s["F"]), COL["spine"], band, alpha=0.75)
    for x in CL["W"]["runs"]:
        leg(("walk", x["cls"]))
        P = tp(x["F"])
        pg.line(P, COL["white"], 1.5)
        if x["cls"] == "bank":
            pg.line(P, COL["walk"], 0.7)
        elif x["cls"] == "street":
            pg.line(P, COL["walk"], 0.7, [2.2, 0.8], cap=0)
        else:
            pg.line(P, COL["river_dark"], 0.7, [0.5, 0.6], cap=0)
    if taken is None:
        return
    for s in CL["spine"]:
        if s["kind"] == "deck":
            taken += boxes_along(tp(s["F"]), 1.5)
    if W_ is not None and spines:
        mp_ = tp(CL["main"])
        word_along(pg, mp_, u"MAIN SPINE", 2.6, COL["spine_dark"], taken, W_, H_)
        edge = [tp(s["F"]) for s in CL["spine"] if s["kind"] != "deck"]
        if edge:
            word_along(pg, max(edge, key=lambda P: arclen(P)[-1]), u"STREAMSIDE SPINE", 2.6, COL["spine_dark"],
                       taken, W_, H_)
    if not stops:
        return
    r = 2.3
    for n, nm, xy, how in CL["stops"]:
        x, y = T(xy)
        if W_ is not None and not (0 <= x <= W_ and 0 <= y <= H_):
            continue
        leg("stop")
        pg.circle(x, y, r + 0.35, fill=COL["white"])
        pg.circle(x, y, r, fill=COL["accent"])
        pg.text(str(n), x, y - 1.0, 2.8, COL["white"], bold=True, align="C")
        taken.append((x - r, y - r, x + r, y + r))
        w = text_w(nm.upper(), 2.1, True)
        for bx, by in ((x + r + 0.8, y - 0.8), (x - r - 0.8 - w, y - 0.8), (x - w / 2, y + r + 0.8),
                       (x - w / 2, y - r - 3.0)):
            b = (bx - 0.4, by - 0.4, bx + w + 0.4, by + 2.5)
            if W_ is not None and (b[0] < 0 or b[2] > W_ or b[1] < 0 or b[3] > H_):
                continue
            if any(hit(b, t) for t in taken):
                continue
            pg.text(nm.upper(), bx, by, 2.1, COL["ink_dark"], bold=True)
            taken.append(b)
            break


def clip_city(CL, test):
    """A copy of CL cut to test(x, y) (alternatives 1 and 2: a working area and its ring)."""
    cut = lambda P: cut_runs(P, test, 1.0)
    return {"main": None, "mains": cut(CL["main"]),
            "spine": [dict(s, F=F) for s in CL["spine"] for F in cut(s["F"])],
            "W": {"runs": [dict(x, F=F) for x in CL["W"]["runs"] for F in cut(x["F"])]}, "stops": []}


def city_results(CLs):
    """masterplan_results.json: what other scripts read (water balance: riverside_walk_m2)."""
    out = {"script": "bergama_masterplan_v22.py", "version": VERSION,
           "run_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
           "note": "survey coordinates (m); walk width %.1f m (design value); lengths calculated from the survey" % WALK_W,
           "options": {}}
    for opt, CL in CLs.items():
        W = CL["W"]
        out["options"][opt] = {
            "riverside_walk_m2": round(CL["walk_m2"], 0),
            "walk_m_by_bank_and_class": dict((k_, round(v, 0)) for k_, v in sorted(W["stats"].items())),
            "spine_m": dict((k_, round(v, 0)) for k_, v in CL["spine_m"].items()),
            "walks": [{"bank": x["bank"], "cls": x["cls"], "m": round(x["m"], 1),
                       "P": [[round(p[0], 2), round(p[1], 2)] for p in x["F"]]} for x in W["runs"]],
            "spine": [{"id": s["id"], "name": s["name"], "kind": s["kind"],
                       "P": [[round(p[0], 2), round(p[1], 2)] for p in s["F"]]} for s in CL["spine"]],
            "stops": [{"n": n, "name": nm, "xy": [round(xy[0], 2), round(xy[1], 2)], "placed_by": how}
                      for n, nm, xy, how in CL["stops"]],
            "sources": {"walks": CL["src_walks"], "city_link": CL["src_city"]}}
    return out


# ================================================================ link helpers (the puzzle's tongues)
def inset(p, q, z):
    """Point p on zone z's edge, moved SNAP_IN_M into z, away from q (which lies outside z)."""
    for tx, ty in ((p[0] - q[0], p[1] - q[1]), (z["q"][0] - p[0], z["q"][1] - p[1])):
        L = math.hypot(tx, ty)
        if L > 1e-9:
            c = (p[0] + tx / L * SNAP_IN_M, p[1] + ty / L * SNAP_IN_M)
            if pip(c[0], c[1], z["P"]):
                return c
    return p


# ================================================================ Rhino bake (only with rhino_bake = True)
def _flat(c, alpha):
    """A fill's colour as it shows on white paper (the bake has no opacity)."""
    return c if alpha is None or alpha >= 0.995 else mix(COL["white"], c, alpha)


def _rgb(c):
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def bake_page(rs, pg, layer, x0, y0, s):
    """The vectors of one sheet as curves, solid hatches and text on layer, at x0 + page mm x s. White fills (the
    paper and the white base) and the pattern stripes are left out; colours are flattened on white."""
    P3 = lambda p: (x0 + p[0] * s, y0 + p[1] * s, 0.0)
    ids = []

    def keep(i, colour, width=None):
        if i:
            rs.ObjectColor(i, _rgb(colour))
            if width is not None:
                rs.ObjectPrintWidth(i, width)
            ids.append(i)

    def curve(pts, closed):
        Q = [P3(p) for p in pts] + ([P3(pts[0])] if closed else [])
        return rs.AddPolyline(Q) if len(Q) >= 2 else None

    for it in pg.items:
        kd = it[0]
        if kd == "poly":
            _, rings, fill, stroke, lw, dash, stripes, alpha = it
            cs = [c for c in (curve(r_, True) for r_ in rings) if c]
            if fill and fill.upper() != "FFFFFF" and cs:
                for h in rs.AddHatches(cs, "Solid") or []:
                    keep(h, _flat(fill, alpha))
            if stroke and stroke.upper() != "FFFFFF":
                for c in cs:
                    keep(c, _flat(stroke, alpha), lw)
            elif cs:
                rs.DeleteObjects(cs)
        elif kd in ("line", "clipline"):
            pts, stroke, lw = (it[1], it[2], it[3]) if kd == "line" else (it[2], it[3], it[4])
            if stroke.upper() != "FFFFFF":
                keep(curve(pts, False), stroke, lw)
        elif kd == "circle":
            _, cx, cy, r, fill, stroke, lw, alpha = it
            c = rs.AddCircle(P3((cx, cy)), r * s)
            if fill and c:
                for h in rs.AddHatches([c], "Solid") or []:
                    keep(h, _flat(fill, alpha))
            if stroke:
                keep(c, stroke, lw)
            elif c:
                rs.DeleteObject(c)
        elif kd == "text":
            _, t, x, y, size, colour, bold, align, halo = it
            keep(rs.AddText(t, P3((x, y)), size * s, "Arial", 1 if bold else 0, {"L": 1, "C": 2, "R": 4}[align]),
                 colour)
    if ids:
        rs.ObjectLayer(ids, layer)
    return len(ids)


def bake_pages(doc, pages, scale):
    """Bake the sheets into Rhino under BAKE_ROOT::<option>_alt<n>, at their print scale, to the right of
    everything else in the file and side by side (never on top of each other or of the survey). The last bake is
    deleted first."""
    import rhinoscriptsyntax as rs
    rs.EnableRedraw(False)
    try:
        for lay in list(rs.LayerNames() or []):
            if lay == BAKE_ROOT or lay.startswith(BAKE_ROOT + "::"):
                old = rs.ObjectsByLayer(lay)
                if old:
                    rs.DeleteObjects(old)
        try:
            u = Rhino.RhinoMath.UnitScale(Rhino.UnitSystem.Meters, doc.ModelUnitSystem)
        except Exception:
            u = 1.0
        s = scale / 1000.0 * u                                # model units per mm on the sheet
        x, y0 = 0.0, 0.0
        try:
            bb = doc.Objects.BoundingBox
            if bb.IsValid:
                x, y0 = bb.Max.X, bb.Min.Y
        except Exception:
            pass
        x += BAKE_GAP * pages[0][2].W * s
        n = 0
        for opt, alt, pg in pages:
            lay = u"{}::{}_alt{}".format(BAKE_ROOT, opt, alt)
            if not rs.IsLayer(lay):
                rs.AddLayer(lay)
            n += bake_page(rs, pg, lay, x, y0, s)
            x += pg.W * s * (1.0 + BAKE_GAP)
    finally:
        rs.EnableRedraw(True)
    return u"Rhino bake: layer {}, {} sheets side by side right of the file's content, {} objects  {}".format(
        BAKE_ROOT, len(pages), n, datetime.datetime.now().strftime("%H:%M:%S"))


# ================================================================ one press
def save(pg, folder, name, title):
    path = os.path.join(folder, name)
    try:
        write_pdf(pg, path, title)
    except (IOError, OSError):                       # the old file is open in another program: a new name
        path = os.path.join(folder, name.replace(".pdf", datetime.datetime.now().strftime("_%H%M%S.pdf")))
        write_pdf(pg, path, title)
    return path


def opacity_input(warn):
    v = inp("opacity", None)
    if v is None:
        return OPACITY
    try:
        f = float(str(v).strip().replace(",", ".").rstrip("%"))
        if f > 1.0:
            f /= 100.0                              # given in per cent
        if 0.0 < f <= 1.0:
            return max(0.05, f)
    except Exception:
        pass
    warn.append(u"input opacity = '{}' is not 0-1 or 1-100 %: {:g} was used".format(v, OPACITY))
    return OPACITY


def option_input():
    return ("A",)                                        # v19: option A only, project-wide (Aras 25 Oct 16:43)


def build_all(doc, warn):
    """Read, draw and write. Returns (folder, files, log lines, pages)."""
    folder = out_folder(doc)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    scale = inp_num("scale", BOARD_SCALE, warn)
    _SCALE[0] = scale                                    # v16: for the scale bar on every sheet
    ring_m = inp_num("zoom_m", None, warn)                      # v15: margin of the zoomed pages (alternatives 1-2)
    if ring_m is None:
        ring_m = inp_num("ring_m", RING_M, warn)
    alpha = opacity_input(warn)
    _ALPHA[0] = alpha                                    # v17: for the legend swatches
    if doc is not None:
        load_palette([DATA_DIR] + search_dirs(doc), warn)
    # ---- working areas (extents only), survey, base of each drawing
    areas = read_areas(doc) if doc is not None else {}
    if len(areas) < 2:                                   # v12: calisma_alan of Bergama_Altlik.3dm, built in
        areas = calisma_from([ring(list(P)) for P in CALISMA_COPY])
        warn.append(u"no calisma_alan outlines in the open file: the built-in copy (Bergama_Altlik.3dm, 25 Oct) "
                    u"was used")
    site, site_found = read_site(doc)
    if not site_found:
        warn.append(u"no site_alan outline in the open file: the built-in copy (Bergama_Altlik.3dm, 25 Oct) was used")
    V = View(areas, 0.0, 1000.0 / scale, frame=site)            # v15: alternative 3 = exactly site_alan
    bb = [bbox(A) for A in areas.values()] + [V.bb]
    R = (min(b[0] for b in bb) - ring_m - 5, min(b[1] for b in bb) - ring_m - 5,
         max(b[2] for b in bb) + ring_m + 5, max(b[3] for b in bb) + ring_m + 5)
    survey = read_survey(doc, R) if doc is not None else {}
    if not survey.get("building") and not survey.get("housing"):
        warn.append(u"no survey buildings (BINA_*) in the open file: the zones are drawn on plain paper")
    bases = {}
    for key, place, idea in AREAS:
        b = bbox(areas[key])
        bases[key] = prep_base(survey, Near(areas[key], ring_m),
                               (b[0] - ring_m, b[1] - ring_m, b[2] + ring_m, b[3] + ring_m))
    # ---- per option: the zones (file, else zone base file, else the embedded copy), then the three alternatives
    files, lines, pages = [], [], []
    sheets, wins, plc, missing = [], [], {}, {}           # v21: sheets for the booklet crops
    CLs = {}
    zb = None
    for opt in option_input():
        its = read_items(doc, opt) if doc is not None else []
        if not its:
            if zb is None:
                zb = zone_base_file(doc, warn)
            its = [i for i in zb[1] if i["layer"].startswith("Option_" + opt + "::")]
            src = zb[0]
            if not its:
                its = [i for i in embedded_items() if i["layer"].startswith("Option_" + opt + "::")]
                src = u"the copy of zone base v5 embedded in this script"
            warn.append(u"option {}: no Option_{}::INT_ zones in the open file; {} was used".format(opt, opt, src))
        D = Design(its, areas, warn, opt)
        out_z = [z["id"] or z["label"] for z in D.zones if any(off_work(p, areas) > SNAP_M for p in z["P"])]
        if out_z:                                        # v12: proposals on calisma_alan (within SNAP_M counts as on it)
            warn.append(u"option {}: zone(s) more than {:.0f} m outside calisma_alan: {}".format(
                opt, SNAP_M, ", ".join(out_z)))
        try:                                             # v11: walks, the spine on the edge, stops
            CLs[opt] = city_layer(opt, D, areas, survey, warn)
            CL = CLs[opt]
            st_ = CL["W"]["stats"]
            lines.append(u"option {}: walks {} (m); spine on the edge {:.0f} m, no room {:.0f} m, over the covered "
                         u"reach {:.0f} m; riverside walks {:,.0f} m2 ({}; {})".format(
                             opt, ", ".join(u"{} {:.0f}".format(k_, v_) for k_, v_ in sorted(st_.items())),
                             CL["spine_m"]["edge"], CL["spine_m"]["deck"], CL["spine_m"]["over"], CL["walk_m2"],
                             CL["src_walks"], CL["src_city"]))
            if CL.get("prom_stats"):                     # v21
                lines.append(u"option {}: promenade {:,.0f} m2 beside the stream; it reaches a street edge at {:.0f} % "
                             u"of the bank stations".format(opt, CL["prom_stats"]["m2"], CL["prom_stats"]["street_pct"]))
        except Exception as ex:
            import traceback
            CL = None
            warn.append(u"option {}: walks and spine NOT drawn ({}: {})".format(opt, type(ex).__name__, ex))
            warn.append(traceback.format_exc()[-480:])
        pzs = {}
        for key, place, idea in AREAS:
            try:
                pzs[key] = puzzle(bases[key], D, key)
            except Exception as ex:
                pzs[key] = []
                warn.append(u"option {}: the puzzle of {} failed ({}: {})".format(opt, place, type(ex).__name__, ex))
        for alt in (1,):                                 # v19: the one sheet
            name = OUT_NAME.format(opt, alt)
            t0 = time.time()
            LEG.clear()                                  # v17: the legend lists only this sheet's entries
            try:
                panels = [draw_area(spec, opt, alt, D, bases[spec[0]], pzs[spec[0]], scale, alpha, areas[spec[0]], CL)
                          for spec in AREAS]
                for p_ in panels:                        # v21: each panel is a booklet crop
                    p_.bid = MP_CROPS[p_.key]
                pg = make_board(opt, alt, panels)
                path = save(pg, folder, name, u"Bergama masterplan v22 option {} (opacity {:.2f}, "
                                              u"1:{:,.0f})".format(opt, alpha, scale))
                files.append(path)
                pages.append((opt, alt, pg))
                sheets.append((path, pg, scale))
                lines.append(u"{}  {}  {:.1f} s".format(os.path.basename(path),
                                                       datetime.datetime.now().strftime("%H:%M:%S"), time.time() - t0))
            except Exception as ex:
                import traceback
                lines.append(u"{}  NOT WRITTEN ({}: {})".format(name, type(ex).__name__, ex))
                warn.append(traceback.format_exc()[-480:])
        if opt == "A" and CL is not None:                # v21: the 1:1,000 detail sheet (option A)
            name = DETAIL_NAME.format(opt)
            t0 = time.time()
            LEG.clear()
            _SCALE[0] = DT_SCALE
            try:
                plc = places(city_link()[0], CL, survey)
                wins = detail_windows(D, plc, bk_frame("bergama_masterplan/dt_upstream", *DT_FRAME))
                spots = read_spots(doc, [w["R"] for w in wins]) if doc is not None else []
                if not spots:
                    warn.append(u"no survey spot heights ({}) in the detail windows: no spot levels".format(SPOT_LAYER))
                dpanels = []
                for w in wins:
                    spec = next(a_ for a_ in AREAS if a_[0] == w["key"])
                    Rm = (w["R"][0] - 40.0, w["R"][1] - 40.0, w["R"][2] + 40.0, w["R"][3] + 40.0)
                    missing[w["id"]] = []
                    p_ = draw_area(spec, opt, 1, D, prep_base(survey, BoxNear(Rm), Rm), pzs[w["key"]], DT_SCALE,
                                   alpha, areas[w["key"]], CL, win=w["R"],
                                   detail=detail_overlay(w, D, CL, spots, plc, missing[w["id"]], warn),
                                   title=w["title"] + u" · 1:1,000")
                    p_.bid = (w["id"], w["old"], w["caption"])
                    dpanels.append(p_)
                    for m_ in missing[w["id"]]:
                        warn.append(u"detail {}: label not placed: {}".format(w["id"], m_))
                pg = make_board(opt, 1, dpanels, title=u"MASTERPLAN · DETAIL 1:1,000")
                path = save(pg, folder, name, u"Bergama masterplan v22 detail option {} (1:1,000)".format(opt))
                files.append(path)
                pages.append((opt, "detail", pg))
                sheets.append((path, pg, DT_SCALE))
                lines.append(u"{}  {}  {:.1f} s".format(os.path.basename(path),
                                                       datetime.datetime.now().strftime("%H:%M:%S"), time.time() - t0))
            except Exception as ex:
                import traceback
                lines.append(u"{}  NOT WRITTEN ({}: {})".format(name, type(ex).__name__, ex))
                warn.append(traceback.format_exc()[-480:])
            _SCALE[0] = scale
    if CLs:                                              # v11: what the other scripts read
        try:
            with open(os.path.join(folder, RESULTS_NAME), "w", encoding="utf-8") as f:
                json.dump(city_results(CLs), f, ensure_ascii=False, indent=1)
            lines.append(u"{}  {}".format(RESULTS_NAME, datetime.datetime.now().strftime("%H:%M:%S")))
        except Exception as ex:
            lines.append(u"{}  NOT WRITTEN ({}: {})".format(RESULTS_NAME, type(ex).__name__, ex))
    if sheets:                                           # v21: the booklet's crops of the sheets; never breaks them
        try:
            booklet_crops(folder, sheets, wins, plc, missing)
            lines.append(u"booklet/blocks.json  {} crops".format(sum(len(sh_.panels) for _, sh_, _ in sheets)))
        except Exception as ex:
            import traceback
            lines.append(u"booklet  NOT WRITTEN ({}: {})".format(type(ex).__name__, ex))
            warn.append(traceback.format_exc()[-480:])
    return folder, files, lines, pages, scale


def run():
    btn, on = button_state()
    try:
        was = bool(sc.sticky.get(_key("prev"), False))
    except Exception:
        was = False
    pressed = (on and not was) or chain_fire(_GH_IN.get(btn), "chain_seen", btn)
    globals()["_ran_now"] = pressed
    mem_set("prev", on, persist=False)
    if not pressed:
        last = mem_get("last", "")
        gh_status(mem_get("status", "") or SHORT + " · idle")
        for w in mem_get("warn", []) or []:
            gh_message("warning", w)
        return (last if last else u"Idle. Press the Button to write the masterplan. ({})".format(VERSION)), \
            mem_get("files", [])
    t0 = time.time()
    warn, err, folder, files, lines = [], None, None, [], []
    doc = Rhino.RhinoDoc.ActiveDoc if Rhino is not None else None
    try:
        folder, files, lines, pages, scale = build_all(doc, warn)
        if to_bool(inp("rhino_bake", False)) and pages:
            try:
                lines.append(bake_pages(doc, pages, scale))
            except Exception as ex_:
                lines.append(u"Rhino bake NOT DONE ({}: {})".format(type(ex_).__name__, ex_))
    except Exception as ex_:
        import traceback
        err = u"ERROR: {}: {}".format(type(ex_).__name__, ex_)
        warn.append(traceback.format_exc()[-480:])
    secs = time.time() - t0
    head = [u"{} · total {:.0f} s".format(VERSION, secs), err or u"Output: {}".format(folder)]
    text = u"\n".join(head + lines)
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
    mem_set("warn", warn)
    gh_status(status)
    for w in warn:
        gh_message("warning", w)
    if err:
        gh_message("error", err)
    return text, files


# ================================================================ embedded copies (fallbacks; see DATA RULES)
# ZONE_COPY: zone base v5 BASE_DATA (md5 c1f667e7eae0a000d4d80078a433427d), only the items drawn here (INT_ZONE,
# INT_WATER, INT_LINK, INT_REMOVE, INT_ROAD_path of Option_A and Option_B) with user text label, id, study_area,
# zone and link, coordinates rounded to 1 cm; v13 adds zone base v7's DG 1 / DG 2; JSON, zlib + base64 (json md5
# 81615ea37596b7b954663a368020b9a5).
def bergama_data(name, _c={}):
    """Built-in data kept in Downloads/Bergama/Data/bergama_masterplan_data.py (Aras 25 Oct 21:29, scripts shortened): runs its
    section `name` here, as if it were written in this place. The file is read once per run; a missing file or one
    from another version of this script stops the script with a message saying which file to copy."""
    import os as _os, hashlib as _hl
    if not _c:
        p_ = _os.path.join(_os.path.expanduser("~"), "Downloads", "Bergama", "Data", "bergama_masterplan_data.py")
        if not _os.path.isfile(p_):
            raise RuntimeError("Data file missing: copy bergama_masterplan_data.py from the run kit's Data folder into " + _os.path.dirname(p_))
        with open(p_, encoding="utf-8", newline="") as f_:
            for part_ in f_.read().split("\n#@@ ")[1:]:
                k_, _, b_ = part_.partition("\n")
                _c[k_] = b_
    b_ = _c.get(name)
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != {'ZONE_COPY': '7c7d4a4a21af391460ac0701ae5e3902', 'STREAM_REF': '6462357102432c243b7a34f595c055c7', 'WALK_COPY': '1cd13819bdb905317ae04d7b1461f8dc'}.get(name):
        raise RuntimeError("Data file bergama_masterplan_data.py is not the one made with this script version (part " + name +
                           "): copy it again from the same run kit as the script")
    exec(compile(b_, "bergama_masterplan_data.py:" + name, "exec"), globals())


bergama_data("ZONE_COPY")


# STREAM_REF (v11): the Selinos reference line from the frame's north-west end to the Ilıca Deresi confluence, with a
# covered flag per segment. OpenStreetMap "Selinos Çayı" (extract of 28 Jul 2026, traffic package bergama_osm.osm)
# converted with the h01 §0 formula (x = 30037.01 + (lon - 27.18127) x 86,361; y = 32121.57 + (lat - 39.123302) x
# 111,320; +-10-30 m), then moved onto the middle of the survey channel (HIDRO_DERE_SULU / walls; median of 21
# stations, 2 m apart) and thinned to 10 m. Covered = OSM tunnel / culvert ways. Calculated 24 Oct 2026, Thread 5.
bergama_data("STREAM_REF")

# MAIN_SPINE (v11): Bankalar Caddesi + Kınık Caddesi (OSM "secondary" ways, same extract and formula, +-10-30 m),
# from Bankalar's south end to Kınık Caddesi east of the frame's K5-K6 reach; used when city_link_results.json has no
# main_spine.
MAIN_SPINE = [[29756.1, 31655.4], [29777.7, 31668.2], [29793.7, 31679.4], [29806.4, 31691.6], [29813.1, 31702.3], [29819.3, 31712.8], [29828.2, 31728.8], [29852.9, 31760.3], [29869.5, 31780.3], [29880.9, 31808.0], [29885.0, 31824.8], [29896.2, 31862.5], [29901.7, 31880.7], [29908.9, 31905.2], [29916.1, 31928.8], [29919.2, 31939.1], [29929.8, 31960.8], [29944.8, 31984.6], [29951.9, 31990.3], [29956.3, 31993.2], [29992.8, 32017.4], [29995.4, 32019.8], [29998.6, 32022.6], [30005.0, 32029.4], [30032.5, 32038.3], [30084.6, 32056.0], [30089.7, 32057.7], [30092.6, 32056.5], [30096.2, 32055.0], [30138.7, 32039.0], [30153.1, 32036.3], [30235.7, 32021.9], [30245.0, 32020.1], [30269.2, 32015.6], [30274.2, 32014.5], [30278.7, 32012.8], [30281.9, 32010.3], [30285.0, 32007.1], [30308.8, 31981.0], [30310.4, 31979.3], [30317.5, 31972.1], [30331.6, 31957.6], [30373.7, 31924.2], [30399.9, 31903.0], [30432.4, 31879.5], [30499.5, 31831.0], [30545.8, 31800.5], [30562.8, 31796.3], [30574.8, 31795.5], [30598.1, 31797.7], [30626.3, 31799.4], [30663.0, 31801.6], [30682.2, 31803.0], [30709.6, 31804.9], [30718.5, 31805.5], [30741.5, 31803.1], [30767.5, 31791.6], [30786.2, 31779.9], [30813.0, 31760.8], [30824.8, 31752.4], [30889.1, 31700.8], [30978.8, 31622.0], [30993.4, 31611.0], [31007.0, 31604.5], [31023.2, 31601.7]]

# CITY_LINK_COPY (v11): the riverside spine, its banks (spine_banks) and stops of bergama_city_link v1.1 (24 Oct 09:15); used when Downloads/Bergama/output/Bergama_city_link_analysis/city_link_results.json is missing.
CITY_LINK_COPY = '{"spine_banks": {"A": "SW", "B": "over", "C": "SW"}, "spine": [{"id": "A", "name": "Ulu Cami to K3 bank walk", "frm": [29846.0, 32278.0], "to": [30037.0, 32122.0], "side_ref": [29844.2, 32313.3], "offset_m": 15.0, "side": "auto", "catch_m": 250.0}, {"id": "B", "name": "Junction over the covered reach", "frm": [30037.0, 32122.0], "to": [30238.7, 31931.2], "side_ref": null, "offset_m": 0.0}, {"id": "C", "name": "Red Hall to Üç Kemer bank walk", "frm": [30238.7, 31931.2], "to": [30294.0, 31792.0], "side_ref": [30245.0, 31962.0], "offset_m": 15.0, "side": "auto", "catch_m": 250.0}], "functions": [{"n": 1, "name": "Bank bazaar", "xy": [29890.4, 32243.6], "stage": null}, {"n": 2, "name": "Parchment and leather workshops", "xy": [30062.0, 32106.0], "stage": null}, {"n": 3, "name": "Junction square", "xy": [30058.0, 32047.0], "stage": null}, {"n": 4, "name": "Red Hall water terrace", "xy": [30238.7, 31931.2], "stage": null}, {"n": 5, "name": "Producers\' market", "xy": [30294.0, 31792.0], "stage": null}, {"n": 6, "name": "Study terraces", "xy": [29941.0, 32200.0], "stage": null}, {"n": 7, "name": "Clean-water classroom", "xy": null, "stage": "entry"}, {"n": 8, "name": "Summer bed events", "xy": null, "stage": null}]}'

# WALK_COPY (v11): river_walks() run on the course survey "Bergama Müdahele Alanları" (17 Oct) with each option's
# cleared buildings from ZONE_COPY, 24 Oct 2026; used only when the open file has no stream or bank layers.
bergama_data("WALK_COPY")


if Rhino is not None:
    try:
        _txt, _files = run()
    except Exception as _ex:
        _txt, _files = u"ERROR: {}: {} ({})".format(type(_ex).__name__, _ex, VERSION), []
        gh_status(SHORT + " · ERROR")
        mem_set("last", _txt)   # 25 Oct: the error stays on the log after the Button is released
        mem_set("status", SHORT + " · ERROR")
    log = _txt
    print(_txt)              # 25 Oct 12:10: the canvas's log output is Grasshopper's "out" (printed text): print the log
    pdf = _files
    if globals().get("_ran_now"):
        mem_set("done", done_text(True, "ERROR" not in str(mem_get("status", "")), time.time() - _T_START))
    done = mem_get("done", "idle")   # 25 Oct 10:20: stays after the run; wire into the next script's run (one-click chain)
