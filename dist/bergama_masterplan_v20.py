# -*- coding: utf-8 -*-
"""BERGAMA MASTERPLAN v20 (2026-10-25): Group 6's proposal (the zones, their programme and the water links) drawn
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
  3. Press the Button. One press writes all six PDFs and masterplan_results.json into the folder
     Downloads/Bergama/output/bergama_masterplan (24 Oct, Aras rule); a second press writes them again. With a Boolean Toggle on rhino_bake set to True,
     the press also bakes the six sheets into Rhino under layer MP11, beside everything else in the file and beside
     each other, never on top of each other or of the survey (a press replaces the last bake).
  INPUTS (any name case; text, number or panel)
    run          Button (v20; any input name works; a plain Button)
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

NEW IN v20 (Aras 25 Oct 18:37, A3 booklet; SCRIPT_STANDARD §8): the sheet and masterplan_results.json are unchanged.
  The press also writes the booklet's drawings into output/bergama_masterplan/booklet/: c1_s1 and c1_s2 (the whole
  site in two equal halves with 50 m overlap, centred, turned so the stream runs left to right, 1:5,000), c3_a and c3_b (north-up
  1:1,000 windows on the upstream entry and on K5 with Demeter's Garden), each a text-free vector PDF drawn at its
  booklet frame's size, plus blocks.json (every word as a label) and results.json (scales, windows, places). Option
  A only; the streamside spine in E0B67D; the area with no programme yet is plain ground. A booklet error is logged
  and never stops the sheet.
NEW IN v19 (Aras 25 Oct 16:41-16:42: "get rid of alternative 3. And do the changes to alternative one"; "that script
  gonna be producing just a single alternative"; "with the curvy selection ... it should be A"). ONE sheet per press:
  the masterplan, option A (Aras 16:43: option A project-wide, B dropped; the option input is ignored). Alternatives 2 and 3 are gone (draw_masterplan and the
  functions only it used removed); the sections WHAT IT DRAWS above describe the older alternatives.
  The one sheet = alternative 1 with v18's changes: the zones are alternative 2's freely grown pieces (overlaps
  darken) in alternative 1's tones with alternative 1's darker commons on top; the main and riverside spines are
  broad zones; the river band is named PROMENADE (Aras: "find a proper catchy singleword name"), its functions
  scattered on it as keywords (his words of 16:39). Without alternative 3 there are no link arrows and no stop
  roundels on any sheet (the programme diagram rule: no arrows). masterplan_results.json is written for option A.
NEW IN v18 (Aras 25 Oct 16:35-16:36: "combine both alt1 and alt2 on masterplan ... seeable on top of eachother";
  "alternative2s zoning is really really good"; "roads should become zones"; "river zoning is really good i want
  something like that with volume however on a different colour and sits on top of river and goes inline with
  river"). Alternative 3 only; alternatives 1 and 2 are unchanged.
  * The zones are alternative 2's freely grown pieces (growth unchanged), overlapping so the colour darkens where
    they meet, in the same light tones as alternative 1, with alternative 1's darker commons on top. The hand
    outline, verge band and code patterns of the zones are gone (zone_pattern, hand_outline removed).
  * The main spine and the riverside spine are no longer lines: each is one broad zone grown SPINE_ZONE_M either
    side of the same route (city link's data, unchanged), its edge wandering like alternative 2's pieces; the
    deck reaches are part of the zone. Names on the fills.
  * RIVERSIDE FUNCTION AND CIRCULATION (Aras 16:39: "it a function/circulation area. There'll be viewpoints,
    terraces, walkpaths, ramps etc. ... cafes etc. will be located"; his words are its keywords): one broad zone grown RIVER_BAND_M beyond the stream and bank
    lines and the water strip, along the whole corridor, in sage (palette reference 89986A), drawn over the river
    with a soft shadow and an outline for volume. Option A liquid edge, option B faceted (form rule).
  * Widths are graphic defaults, not data. Walks unchanged (to be reworked with Aras). Legend: the new zones added.
NEW IN v17 (Aras 25 Oct 14:40: "we want it as a legend in the diagram itself ... i wanted a graphical explanation"):
  every sheet gets a legend band under the drawing: drawn samples (zone swatches with their pattern and outline,
  context and survey fills, walk and spine lines, the link arrows, a stop roundel) with plain names, and only what
  that sheet draws (collected while drawing, LEG). No hex codes. This replaces the 18 Oct "no legend" rule for the
  masterplan sheets. Alternative 3's old one-line key of arrows, walks and spines (top right) is folded into it;
  the north arrow stays. Nothing else changed.
NEW IN v16 (Aras 25 Oct 11:28, studio brief for 26.10.2026: "a 1/1000 scale master plan covering the Selinos
  Corridor"): the default scale is 1:1,000 (was 1:2,000), so alternative 3 (all of site_alan, 2,845 x 529 m) prints
  about 2.87 x 0.58 m. Every sheet now carries its scale: a 0-50-100-200 m bar and "1:1,000" right of the option
  line (this replaces "no scale" of 18 Oct 19:36 for the masterplan sheets, because the brief asks for the scale).
  Nothing else changed.
NEW IN v15 (Aras 25 Oct 10:07: "Every plan and analysis and drawing we do is to be in site_alan and for indivual proposals we can
  zoom in."): alternative 3 (the whole masterplan) covers exactly the analysis range, layer site_alan (built-in copy
  SITE_COPY when the file has none), turned so its long side runs left to right; the survey is drawn over all of it.
  Alternatives 1 and 2 are the zoomed pages, one per part of calisma_alan; their margin is the input zoom_m (was
  ring_m, which still works).
NEW IN v14 (Aras 25 Oct 09:34-09:35): the same names in every script: the Button goes into an input named run, the log comes out of an output named log, and the log file is Downloads/Bergama/logs/bergama_masterplan_log.txt (next to cached/ and output/), overwritten by each press.

NEW IN v13 (2026-10-25, Aras 08:03-08:18): DEMETER'S GARDEN, Begum's idea alone (card i01). Zone base v7's zones DG 1
and DG 2 (layer INT_ZONE_DG, south-west bank either side of K5) are named DEMETER'S GARDEN on the fill, with the
keywords of her PDF (olives, stone pine, aromatics, seasonal beds, cafe, water collection basin) and, under the name,
a very small "idea: Begum" credit. Tones: the agriculture family. Reads bergama_zone_base_v7.py first. Nothing else
changed.

NEW IN v12 (2026-10-25, Aras 07:59-08:05: one file, Bergama_Altlik.3dm; "we are working the whole calisma_alan
together now"; "Make sure our proposals stays inside of calisma_alan")
  * Working areas = the curves on layer calisma_alan of the open file (an open outline with ends under 5 m apart counts
    as closed), else the copy CALISMA_COPY (Bergama_Altlik.3dm, 25 Oct). One shared area in two parts: north (UPSTREAM
    ENTRY TO K4 BRIDGE) and south (K5 BRIDGE TO DOWNSTREAM END); no split by person. Alternatives 1 and 2 show the two
    parts side by side; each part has one commons (HUB: the two old commons readings of that part merged, a design
    reading, edit freely). A zone keeps its sourced keywords (NAMES, SUBS, SIG) through its user text study_area.
  * Nothing is cut (Aras 08:10-08:11: small differences do not matter; lines that nearly match count as overlapping,
    the larger area is the true one). Walks, spine and strip are drawn continuous (207 of 4,211 m of walk lie just
    outside; WALK_CLIP = True would cut them); a zone more than SNAP_M (15 m) outside calisma_alan is listed in the log. A zone with corners
    outside calisma_alan is listed in the log (zone base v6 bakes them clipped; this flags later edits).

NEW IN v11 (Thread 5 of the 22 Oct batch, "Masterplan: detail and unity"; notes batch_2026-10-22/thread5_masterplan/)
  * Riverside walks on both banks wherever the survey leaves room, recomputed from the open file on every press
    (river_walks below: the channel edge, then the ground free of buildings behind it; buildings the zone base
    clears do not block). Three kinds: BANK WALK (car-free), STREET WALK (the footway of a surveyed street on the
    edge), BED WALK (no room on the bank, bed at least BED_MIN_W wide: a +1 m terrace in the bed, closed in floods;
    Thread 4 flood rule). Form rule: option A follows the edge, option B is straight facets.
  * The riverside spine of bergama_city_link (Thread 4), read live from
    Downloads/Bergama/output/Bergama_city_link_analysis/city_link_results.json (fallback: the embedded copy), drawn
    on the real edge, on the bank city link chose by data (spine_banks): on the bank walk where there is one, dashed where the bank has no room (a deck is needed),
    and on the street over the covered reach, where it meets the MAIN SPINE (Bankalar - Kınık Caddesi, OpenStreetMap,
    converted with the h01 formula, +-10-30 m). The eight stops as numbered roundels (alternative 3).
  * More detail on alternative 3: the survey's single trees (SEMBOL_TEK_AGAC), channel tops (SEV_SEVUST) and bank
    tops (SEV_UST) with the bank lines; walks and both spines on alternatives 1 and 2 as well.
  * Unity: masterplan_results.json (walks, spine, stops, riverside_walk_m2 per option) for the other scripts; the
    water balance (v2.1) reads riverside_walk_m2 from it instead of its 17,694 m2 placeholder.

NEW IN v10 (Aras 24 Oct 05:48-05:52; MERGE_PLAN.md sections 3, 5, 6 Q14 / Q16, 7)
  * One script, one press, three alternatives per option (above), each its own single-page PDF; the opacity is a
    setting (input opacity); a 100 % opaque white base under every lower-opacity piece in all three alternatives,
    so the site, land cover and context never mix with the zones: only the zones overlap each other.
  * Owner names replaced by stage and place names; working-area outlines and owner colours removed everywhere.
  * v2.3's four per-person sheets and its board are folded into alternatives 1 and 2 (one page each with the four
    working areas): the per-person sheets showed the same pieces and words again, only zoomed.
  * v9's raster sheet (PNG, Photoshop layers, area register, manifest, sheet band) is replaced by the vector page;
    its zones, link rules (link_check, WATER_STEPS), arrow snapping and bold v1.2 arrows are kept in vector.
  * Fixed: the zone base fallback looked for ZONE_DATA, which zone base v5 does not have (it is BASE_DATA), so the
    fallback never worked; the palette file's tones (under "masterplan" > "colours") were never read; a settings
    input could be taken for the Button; the boardwalk's word (PATH_WORDS) was never written.
  * Optional Rhino bake behind the rhino_bake toggle (off by default).

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

VERSION = "bergama_masterplan v20 (2026-10-25)"
SHORT = "v20"
BUTTON_WORDS = ("build", "bake", "run", "go", "press", "button", "start", "out")
SETTINGS = ("rhino_bake", "opacity", "scale", "zoom_m", "ring_m", "option", "zone_base")   # never taken for the Button
OPACITY = 0.5                         # opacity of the lower-opacity pieces (Aras 05:51: a setting; 0.5 his example)
RING_M = 30.0                         # nearest ring (programme CONTEXT §3.2: inferred, not a sourced number)
BOARD_SCALE = 1000.0                  # v16: studio brief 26 Oct, "1/1000 scale master plan" (was 2000, v2.3's board scale)
_SCALE = [BOARD_SCALE]               # v16: the scale of this press, for the scale bar in sheet_head
_ALPHA = [OPACITY]                   # v17: the opacity of this press, for the legend swatches
_BK = {}                             # v20: what the booklet drawings reuse from the sheet (option A)
BOARD_MAX_W = 4000.0                  # a board of the four working areas wider than this goes into two rows (mm)
LINE_STEP_M = 1.0                     # survey lines are cut at the ring to this step
OUT_FOLDER = "bergama_masterplan"
OUT_NAME = "Bergama_masterplan_v20_{}.pdf"     # v19: one sheet per option
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
         ("begum_alan", "GR", None): u"DRY TOP", ("nil_alan", "WP", None): u"RIVERSIDE PLANTING",
         ("calisma_alan", "DG", None): u"DEMETER'S GARDEN"}   # v13: Begum's idea (card i01)
SUBS = [  # (working-area layer, code, tier, only for: None / "A" / "B" / a working-area key, keywords)
    ("aras_alan", "WS", "D", None, [u"WINTER RAIN", u"STEPPED", u"SEATING"]),
    ("aras_alan", "GR", "D", None, [u"SHADE", u"WALK", u"CAFE"]),
    ("aras_alan", "WT", "F", None, [u"CLEANING", u"DE-ODOUR", u"RUNOFF"]),
    ("aras_alan", "WD", "W", None, [u"OVERFLOW", u"RETURN"]),
    ("begum_alan", "WA", "W", None, [u"WATER STRIP", u"STEPPING STONES", u"WEIRS", u"PLAZA", u"REED"]),
    ("begum_alan", "WA", "F", None, [u"WATER STEPS", u"SEATING", u"TAMARIX"]),
    ("begum_alan", "GR", "D", None, [u"BRIDGE VIEW", u"KIOSK", u"SHADE", u"LAVENDER"]),
    ("nil_alan", "WP", "F", None, [u"CLEAN RIVER", u"FLOOD-PROOF", u"ODOUR-FREE", u"WILLOW"]),
    ("calisma_alan", "DG", "D", None, [u"OLIVES", u"STONE PINE", u"AROMATICS", u"SEASONAL BEDS", u"CAFE",
                                       u"WATER COLLECTION BASIN"]),   # v13: Begum's PDF, verbatim words
]
REMOVE_WORDS = [u"CLEARED"]
# the common piece where the functions of a working area meet: name + what it gathers. A design reading of the
# sourced words above (Aras 19:27, campus reference), not data; edit freely.
HUB = {"calisma_alan[0]": (u"WATER AND HERITAGE COMMONS", [u"COLLECT", u"CLEAN", u"HOLD", u"K4 BRIDGE", u"PLAZA"]),
       "calisma_alan[1]": (u"AMPHIBIOUS RIVER COMMONS", [u"K5 BRIDGE", u"WATER", u"GIVE BACK", u"WALK", u"GREEN"])}
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
KIND_WORD = {"river": u"RIVER", "housing": u"RESIDENTIAL", "park": u"PARK", "heritage": u"HERITAGE"}
PATH_WORDS = {"nil_alan": [u"FLOODABLE DECK"]}
ROUND_M = 9.0                  # corner rounding of the cleared-building outlines, m (graphic)
CREDIT_DG = u"idea: Beg\u00fcm"                 # v13: Demeter's Garden is Begum's idea alone (Aras 25 Oct 08:03)
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
    base = {"faces": {}, "lines": [], "streets": [], "streams": [], "contours": [], "contours10": [], "banks": []}
    for role, max_a in (("park", 400000.0), ("pond", 50000.0), ("housing", 30000.0), ("building", 30000.0),
                        ("heritage", 30000.0)):
        polys = [P for P in survey.get(role, []) if inR(P)]
        base["faces"][role] = [F for F in faces(polys, max_area=max_a) if any(nr.within(p[0], p[1]) for p in F)]
    for role in ("road", "kerb"):
        for P in survey.get(role, []):
            if inR(P):
                base["streets"] += cut_runs(P, nr.within)
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
    "river": (1.00, u"RIVER"),
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
RIVER_BAND_M = 15.0          # v18: the river corridor reaches this far beyond the stream / bank lines, m (graphic default)
SPINE_ZONE_M = 10.0          # v18: a spine zone reaches this far either side of its route, m (graphic default)
BAND_E = 0.6                 # v18: how much the broad zones' edges wander (alternative 2's growth, 0-1)
RIVER_BAND_TONE = ("C4CCB5", "89986A", "3C4733")   # v18: sage, palette reference 89986A (light = mixed 1:1 with white)
RIVER_BAND_NAME = u"PROMENADE"   # v19: one catchy word for Aras's "function/circulation area" (16:39, 16:41)
RIVER_BAND_WORDS = [u"VIEWPOINTS", u"TERRACES", u"WALK PATHS", u"RAMPS", u"CAFES"]   # his words, 16:39
PIECE_TONE = {"river": ("91ADB4", "5D7F8D", "32525F"), "street": ("E6E3DC", "CFCCC5", "847E75"),
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
        if z["code"] == "DG":                        # v13: the very small credit under the name
            lines.append((CREDIT_DG, max(1.2, sz * 0.25), False))
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
            pg.text(word, x, y + dy + 0.06 * size, size, colour, bold=True, align="C", halo=COL["white"])
            taken.append(b)
            return True
    return False


def open_rest(A, zones, nr):
    """The point of a working area farthest from its edges and its zones (where it has no programme yet)."""
    best, bd = None, -1.0
    bxa = bbox(A)
    for i in range(28):
        for j in range(28):
            x = bxa[0] + (i + 0.5) / 28 * (bxa[2] - bxa[0])
            y = bxa[1] + (j + 0.5) / 28 * (bxa[3] - bxa[1])
            if not nr.inside(x, y) or any(pip(x, y, z["P"]) for z in zones):
                continue
            d = min([seg_dist(x, y, A[q], A[(q + 1) % len(A)]) for q in range(0, len(A), max(1, len(A) // 200))] +
                    [math.hypot(x - z["q"][0], y - z["q"][1]) for z in zones])
            if d > bd:
                best, bd = (x, y), d
    return best


def no_programme(pg, xy, taken):
    if not xy:
        return
    x, y = xy
    lines = [(u"NO PROGRAMME YET", 4.0, True)]
    w, h = block_size(lines)
    b = (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    if not any(hit(b, t) for t in taken):
        draw_block(pg, lines, b[0], b[3], COL["ink2"], COL["white"])
        taken.append(b)


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


# ================================================================ zone patterns (masterplan v9 5b; graphic only)
def draw_area(spec, opt, alt, D, base, pz, scale, alpha, A, CL=None):
    """One working area of alternative 1 (partition, darker commons) or 2 (free pieces that overlap) -> Page."""
    key, place, idea = spec
    k = 1000.0 / scale
    R = base["R"]
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
    # ---- the pieces: context and the commons opaque (white seams); programme pieces at the opacity on white
    for pc in pz:                                        # v17: the legend's entries
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
    # v19: context opaque; alternative 2's free zone pieces on one white base; the promenade and the spine zones;
    # the free pieces' light fill at the opacity (overlaps darken); alternative 1's commons opaque on top
    for pc in sorted(ctx, key=lambda q: q["e"]):
        pg.poly(pc["TPs"], fill=pc["tones"][0], stroke=W_, lw=0.5)
    fr = [q for q in pz if q["kind"] == "free"]
    for pc in fr:
        pg.poly(pc["TPs"], fill=W_, stroke=W_, lw=0.5)
    G = Grid(R, base["near"], BAND_CELLS)
    CLc = clip_city(CL, base["near"].within) if CL is not None else None
    RB = [[T(p) for p in L_] for L_ in grow_band(G, base["streams"] + base["banks"],
                                                  [s_["P"] for s_ in D.strips], RIVER_BAND_M, 101, opt)]
    if RB:
        leg("river_band")
        lt, md, dk = RIVER_BAND_TONE
        pg.poly([[(x + 0.8, y - 0.8) for x, y in L_] for L_ in RB], fill=dk, alpha=0.22)   # shadow: volume
        pg.poly(RB, fill=lt, alpha=0.85)
        pg.poly(RB, stroke=dk, lw=0.35)
    SZ = []
    if CLc is not None:
        for nm_, lines_, ni in ((u"MAIN SPINE", CLc["mains"] if "mains" in CLc else [CLc["main"]], 102),
                                (u"RIVERSIDE SPINE", [s_["P"] for s_ in CLc["spine"]], 103)):
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
        z["TP"] = max(pc["TPs"], key=lambda r_: abs(area2(r_)))
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
    # ---- words: the commons first, the promenade and spine zones, then each zone (largest first), cleared, context
    for pc in [q for q in pz if q["kind"] == "hub"]:
        hub_words(pg, max(pc["TPs"], key=lambda r_: abs(area2(r_))), pc["name"], pc["words"], W_, taken,
                  pc["tones"][0])
    for nm_, TPs in ([(RIVER_BAND_NAME, RB)] if RB else []) + SZ:   # v18-v19: names and keywords on the fills
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
        for TP in sorted(pc["TPs"], key=lambda r_: -abs(area2(r_)))[:3]:
            word_in(pg, TP, wd, (2.6, 2.2, 1.8), pc["tones"][2], taken, pad=0.8)
    for p in paths:
        for w_ in PATH_WORDS.get(p.get("own"), []):
            word_along(pg, p["TP"], w_, 2.2, COL["path"], taken, dw, dh)
    if key == "calisma_alan[1]":                         # the open rest of the area: marked, not filled in
        xy = open_rest(A, zones, base["near"])
        no_programme(pg, T(xy) if xy else None, taken)
    # ---- the panel: place and idea over the plan (no owner names, no working-area outline)
    W = M + dw + M
    H = M + HEAD + dh + M
    sh = Page(W, H)
    sh.poly([rect(0, 0, W, H)], fill=COL["paper"])
    sh.clip([rect(M, M, M + dw, M + dh)])
    blit(sh, pg, M, M)
    sh.unclip()
    for txt, size, y in ((place, 8.0, H - M - 8.0), (idea, 4.0, H - M - 14.0)):
        sh.text(txt, M, y, min(size, size * dw / max(text_w(txt, size, True), 1e-6)), COL["ink_dark"], bold=True)
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

# ================================================================ v20: the A3 booklet assets (SCRIPT_STANDARD §8)
# Four drawings for the booklet (booklet/ASSET_SPEC.md), drawn natively at their frame's size, option A only, with
# no text in the PDFs: every word is a label in booklet/blocks.json (set as live text by the assembler).
#   c1_s1 / c1_s2  the whole site (site_alan) in two equal halves (BK_OVERLAP_M overlap), centred, turned so
#                  the stream runs left to right, at 1:5,000 if it fits the frame, else the largest standard scale
#   c3_a / c3_b    north-up 1:1,000 windows (frame size in m): the upstream entry's cleaning and holding chain, and
#                  K5 with Demeter's Garden (1:1,250 when the window cannot hold the garden and the bridge)
# The same layers as the sheet (option A's freely grown zones at the opacity setting, the commons, the promenade,
# the streamside spine in E0B67D, walks, stops) over the survey's buildings (grey) and heritage (pale red). The
# area with no programme yet is plain ground (Aras 25 Oct 20:02). Booklet words: "stream", never "river", for the
# Selinos (Aras 20:02). Label sizes 7.5 pt, key labels 8.5 pt; label boxes never overlap or leave the frame.
BK_FRAMES = {"c1_s1": (392.0, 116.0), "c1_s2": (392.0, 116.0), "c3_a": (194.0, 176.0), "c3_b": (194.0, 176.0)}
BK_STD_SCALES = (1000.0, 1250.0, 2000.0, 2500.0, 5000.0, 10000.0, 20000.0)
BK_C1_SCALE = 5000.0                 # wanted scale of the whole-site halves
BK_WIN_SCALE = 1000.0                # the 1:1,000 windows
BK_OVERLAP_M = 50.0                  # the two halves share this much at the middle of the site
BK_LBL, BK_KEY = 7.5, 8.5            # pt: labels, key labels (zone names)
BK_GAP = 0.4                         # mm kept between label boxes
BK_INK, BK_INK2 = "4A3F35", "6B645B"  # booklet ink and caption ink (design-language.md)
BK_SPINE = "E0B67D"                  # the streamside spine on every frame (Aras 20:02: sand)
BK_PROGRAMME = {u"REED BASINS": [u"cleaning · de-odour · runoff"],      # the plan's keyword lines (SUBS, cut to 30
                u"RETENTION TERRACES": [u"winter rain · stepped · seats"],  # characters a line)
                u"SPILLWAY": [u"overflow · return"],
                u"SHADED WALK": [u"shade · walk · cafe"],
                u"BED": [u"water strip · stepping stones", u"weirs · plaza · reed"],
                u"FLOOD TERRACE": [u"water steps · seats · tamarix"],
                u"DRY TOP": [u"bridge view · kiosk · lavender"],
                u"DEMETER'S GARDEN": [u"olives · pine · aromatics", u"seasonal beds · cafe · basin"],
                RIVER_BAND_NAME: [u"viewpoints · terraces · ramps"]}
BK_C3 = {"c3_a": dict(area="calisma_alan[0]", names=(u"REED BASINS", u"RETENTION TERRACES", u"SPILLWAY",
                                                      u"SHADED WALK"), stops=(7,),
                      caption=u"Upstream entry: collect, clean, hold", bridge=u"K4"),
         "c3_b": dict(area="calisma_alan[1]", names=(u"BED", u"FLOOD TERRACE", u"DRY TOP", u"DEMETER'S GARDEN"),
                      stops=(5, 8), caption=u"K5 bridge and Demeter's Garden", bridge=u"K5")}
BK_WALK_VAL = u"{{val:bergama_masterplan/masterplan_results.json:options.A.walk_m_by_bank_and_class.{} bank|0}}"


def bk_word(s):
    """Booklet wording: the Selinos is a stream (Aras 25 Oct 20:02)."""
    return s.replace(u"RIVERSIDE", u"STREAMSIDE").replace(u"RIVER", u"STREAM").replace(u"riverside", u"streamside")


def bk_lum(c):
    v = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in hex_rgb(c)]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]


def bk_contrast(a, b):
    la, lb = sorted((bk_lum(a), bk_lum(b)))
    return (lb + 0.05) / (la + 0.05)


def bk_on(fill):
    """Label colour on a fill: white where it reads (WCAG 4.5:1), else the booklet ink."""
    return "FFFFFF" if bk_contrast("FFFFFF", fill) >= 4.5 else BK_INK


class BkBox(object):
    """A rectangle as the 'near' test of prep_base and Grid."""

    def __init__(self, R):
        self.R = R

    def inside(self, x, y):
        R = self.R
        return R[0] <= x <= R[2] and R[1] <= y <= R[3]

    within = inside


class BkFrame(object):
    """One booklet drawing: the page (y up), its labels (top-left, y down to the baseline) and its legend."""

    def __init__(self, W, H, F, k):
        self.W, self.H, self.F, self.k = W, H, F, k
        self.pg = Page(W, H)
        self.labels, self.boxes, self.avoid, self.legend, self.missing = [], [], [], [], []

    def T(self, P):
        return [self.F(p) for p in P]

    def tl(self, p):
        x, y = self.F(p)
        return x, self.H - y

    def leg(self, kind, colour, label):
        if all(e["label"] != label for e in self.legend):
            self.legend.append({"kind": kind, "colour": colour, "label": label})

    def lbox(self, s, x, yb, size, bold, anchor):
        w = text_w(s, size * PT, bold)
        x0 = x - (w / 2 if anchor == "C" else w if anchor == "R" else 0.0)
        m = size * PT
        return (x0, yb - 0.72 * m, x0 + w, yb + 0.21 * m)

    def free(self, b, gap=BK_GAP):
        if b[0] < 0.3 or b[1] < 0.3 or b[2] > self.W - 0.3 or b[3] > self.H - 0.3:
            return False
        return not any(hit(b, o, gap) for o in self.boxes + self.avoid)

    def put(self, text, x, yb, size=BK_LBL, bold=False, anchor="L", colour=BK_INK, shown=None):
        """One label (shown = the text as it will print, for its width: a {val:} mark resolved)."""
        self.boxes.append(self.lbox(shown or text, x, yb, size, bold, anchor))
        self.labels.append({"x": round(x, 2), "y": round(yb, 2), "text": text, "size": size, "bold": bool(bold),
                            "anchor": anchor, "colour": colour})

    def block_dims(self, lines):
        """lines [(text, size, bold, shown)] -> (w, h, [baseline offsets from the block top])."""
        w, y, base = 0.0, 0.0, []
        for i, (s, sz, bd, sh) in enumerate(lines):
            m = sz * PT
            y += 0.72 * m if i == 0 else 1.18 * m
            base.append(y)
            w = max(w, text_w(sh or s, m, bd))
        return w, y + 0.21 * lines[-1][1] * PT, base

    def put_block(self, lines, x0, y0, colour):
        w, h, base = self.block_dims(lines)
        for (s, sz, bd, sh), yb in zip(lines, base):
            self.put(s, x0, y0 + yb, sz, bd, "L", colour, sh)

    def place(self, lines, anchor, colour=BK_INK, inside=None, min_d=2.0, max_d=60.0, leader=True,
              fill_colour=None):
        """A label block next to anchor (top-left mm): inside ring `inside` (top-left mm) when it fits there, else
        on a free spot round the anchor with a leader. Returns the box or None."""
        w, h, base = self.block_dims(lines)
        if inside:
            ring_ = thin(inside, 300)
            for x, y in inside_spots(ring_, 22)[:220]:
                b = (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
                if self.free(b) and box_in(ring_, (b[0] - 0.6, b[1] - 0.6, b[2] + 0.6, b[3] + 0.6)):
                    self.put_block(lines, b[0], b[1], bk_on(fill_colour) if fill_colour else colour)
                    return b
        ax, ay = anchor
        for d in [0.0] * (min_d <= 0) + [min_d, min_d + 2, min_d + 4, min_d + 7, min_d + 11, min_d + 16, 24, 32, 42,
                                         max_d]:
            if d > max_d:
                break
            for i in range(24):
                a = math.radians(i * 15.0 + 7.5) if d > 0 else 0.0
                cx = ax + math.cos(a) * (d + w / 2)
                cy = ay - math.sin(a) * (d + h / 2)
                b = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
                if not self.free(b):
                    continue
                self.put_block(lines, b[0], b[1], colour)
                if leader and d > 0:
                    qx, qy = min(max(ax, b[0]), b[2]), min(max(ay, b[1]), b[3])
                    if math.hypot(qx - ax, qy - ay) > 1.2:
                        self.pg.line([(ax, self.H - ay), (qx, self.H - qy)], BK_INK2, 0.15)
                        self.pg.circle(ax, self.H - ay, 0.45, fill=BK_INK2)
                return b
        self.missing.append(lines[0][0] + u" (no free spot)")
        return None


def bk_scale(span_w, span_h, W, H, want):
    """The wanted scale if the span (m) fits W x H mm, else the largest standard scale that does."""
    for s in [want] + [s_ for s_ in BK_STD_SCALES if s_ > want]:
        if span_w * 1000.0 / s <= W and span_h * 1000.0 / s <= H:
            return s
    return BK_STD_SCALES[-1]


def bk_anchors(BK):
    """Named places (world m): the bridges K4, K3, K5 and the Red Hall are city link's surveyed spine anchors (K4 =
    piece A's start, K3 its end, Red Hall = piece C's start, K5 its end); K6 lies city link's K5-K6 chainage downstream
    of K5 on the stream line. Each bridge snaps to the nearest surveyed bridge (YOL_KOPRU) within 60 m."""
    spec, CL = BK["spec"], BK["CL"]
    sp = dict((pc.get("id"), pc) for pc in spec.get("spine", []))
    out = {}
    for nm, (pid, end) in ((u"K4", ("A", "frm")), (u"K3", ("A", "to")), (u"RED HALL", ("C", "frm")),
                           (u"K5", ("C", "to"))):
        if pid in sp and sp[pid].get(end):
            out[nm] = tuple(sp[pid][end])
    ref = CL["W"]["ref"]
    s = arclen(ref)
    ch = spec.get("chainage") or {}
    if u"K5" in out and "K5" in ch and "K6" in ch:
        c5, _ = chain_at(ref, out[u"K5"])
        out[u"K6"], _ = at_len(ref, s, c5 + float(ch["K6"]) - float(ch["K5"]))
    mids = [((B[0][0] + B[-1][0]) / 2.0, (B[0][1] + B[-1][1]) / 2.0) for B in BK["survey"].get("bridge", [])]
    for nm in (u"K4", u"K3", u"K5", u"K6"):
        if nm in out and mids:
            m = min(mids, key=lambda q: math.hypot(q[0] - out[nm][0], q[1] - out[nm][1]))
            if math.hypot(m[0] - out[nm][0], m[1] - out[nm][1]) <= 60.0:
                out[nm] = m
    return out


def bk_seen(P, cb, ring_=True):
    """Page polyline / ring P shows inside the page rectangle cb (x0, y0, x1, y1)."""
    if any(cb[0] <= x <= cb[2] and cb[1] <= y <= cb[3] for x, y in P):
        return True
    if not ring_ or len(P) < 3:
        return False
    pb = bbox(P)
    if not hit(pb, cb):
        return False
    return any(pip(cb[0] + (cb[2] - cb[0]) * i / 4.0, cb[1] + (cb[3] - cb[1]) * j / 4.0, P)
               for i in range(5) for j in range(5))


def bk_layers(fr, BK, base, keys, RB, SP, clip, fine):
    """The drawing of one frame (no words): survey context, zones, commons, promenade, spine, stream, bridges,
    walks; only what shows in the frame (and only that in its legend). fine = the 1:1,000 windows (line weights of
    the sheet), else the 1:5,000 halves (lighter)."""
    pg, W_ = fr.pg, COL["white"]
    alpha = BK["alpha"]
    cb = bbox(clip)
    T = lambda P: fr.T(P)
    seen_rings = lambda loops: [R_ for R_ in (T(L_) for L_ in loops) if bk_seen(R_, cb)]
    seen_lines = lambda P: bk_seen(P, cb, False)
    pg.poly([clip], fill=W_)
    pg.clip([clip])
    fc = base["faces"]
    rings = seen_rings([F_ for role in ("building", "housing") for F_ in fc.get(role, [])])
    if rings:
        pg.poly(rings, fill=COL["bld"])
        fr.leg("fill", COL["bld"], u"building")
    rings = seen_rings(fc.get("heritage", []))
    if rings:
        pg.poly(rings, fill=COL["her"], stroke=COL["her_edge"], lw=0.1)
        fr.leg("fill", COL["her"], u"heritage building")
    pz = [pc for key in keys for pc in BK["pzs"].get(key, [])]
    free = [(pc, seen_rings(pc["loops"])) for pc in pz if pc["kind"] == "free"]
    free = [(pc, R_) for pc, R_ in free if R_]
    hubs = [(pc, seen_rings(pc["loops"])) for pc in pz if pc["kind"] == "hub"]
    hubs = [(pc, R_) for pc, R_ in hubs if R_]
    RBs = seen_rings(RB or [])
    SPs = seen_rings(SP or [])
    for pc, R_ in free:
        pg.poly(R_, fill=W_, stroke=W_, lw=0.3 if fine else 0.15)
    if RBs:
        lt, md, dk = RIVER_BAND_TONE
        s_ = 0.8 if fine else 0.3
        pg.poly([[(x + s_, y - s_) for x, y in L_] for L_ in RBs], fill=dk, alpha=0.22)
        pg.poly(RBs, fill=lt, alpha=0.85)
        pg.poly(RBs, stroke=dk, lw=0.35 if fine else 0.15)
        fr.leg("fill", mix(W_, lt, 0.85), RIVER_BAND_NAME.lower())
    for pc, R_ in free:
        pg.poly(R_, fill=zone_tones(pc["zone"])[0], alpha=alpha)
    for pc, R_ in free:
        fr.leg("fill", mix(W_, zone_tones(pc["zone"])[0], alpha), bk_zone_legend(pc["zone"]))
    for pc, R_ in hubs:
        pg.poly(R_, fill=piece_tone(pc)[0], stroke=W_, lw=0.3 if fine else 0.15)
        fr.leg("fill", piece_tone(pc)[0], u"commons")
    if SPs:
        pg.poly(SPs, fill=BK_SPINE)
        fr.leg("fill", BK_SPINE, u"streamside spine")
    for P in base["streams"]:
        P = T(P)
        if seen_lines(P):
            pg.line(P, COL["river_mid"], 0.22 if fine else 0.12)
    for s_ in BK["D"].strips:
        P = T(s_["P"])
        if bk_seen(P, cb):
            pg.poly([P], fill=COL["river"], stroke=COL["river_dark"], lw=0.2 if fine else 0.1)
            fr.leg("fill", COL["river"], u"water strip")
    for ck, lw, dash, P in base["lines"]:
        P = T(P)
        if ck == "ink" and seen_lines(P):                  # bridges
            pg.line(P, COL["ink"], 0.35 if fine else 0.25)
    ref = BK["CL"]["W"]["ref"]
    for s0, s1 in BK["covered"]:
        P = T(ref_between(ref, s0, s1))
        if seen_lines(P):
            pg.line(P, COL["river_dark"], 0.5 if fine else 0.3, [1.2, 0.8], cap=0)
            fr.leg("line", COL["river_dark"], u"stream, covered reach")
    for x in BK["CL"]["W"]["runs"]:
        P = T(x["F"])
        if not seen_lines(P):
            continue
        pg.line(P, W_, 1.5 if fine else 0.7)
        if x["cls"] == "bank":
            pg.line(P, COL["walk"], 0.7 if fine else 0.35)
            fr.leg("line", COL["walk"], u"bank walk, car-free")
        elif x["cls"] == "street":
            pg.line(P, COL["walk"], 0.7 if fine else 0.35, [2.2, 0.8] if fine else [1.2, 0.5], cap=0)
            fr.leg("line", COL["walk"], u"street walk")
        else:
            pg.line(P, COL["river_dark"], 0.7 if fine else 0.35, [0.5, 0.6] if fine else [0.35, 0.4], cap=0)
            fr.leg("line", COL["river_dark"], u"bed walk, closed in floods")
    pg.unclip()


def bk_zone_legend(z):
    if z["code"] == "WA":
        return u"flood terrace" if z["tier"] == "F" else u"bed"
    nm = bk_word(name_of(z, z.get("own", "")))
    return {u"SHADED WALK": u"dry top, shaded walk", u"DRY TOP": u"dry top, shaded walk",
            u"DEMETER'S GARDEN": u"Demeter's Garden"}.get(nm, nm.lower())


def bk_stops(fr, BK, want, r, inside):
    """Stops as numbered accent dots (the number is a label)."""
    for n, nm, xy, how in BK["CL"]["stops"]:
        if want is not None and n not in want:
            continue
        x, y = fr.F(xy)
        if not inside(x, y):
            continue
        fr.pg.circle(x, y, r + 0.35, fill=COL["white"])
        fr.pg.circle(x, y, r, fill=COL["accent"])
        fr.leg("dot", COL["accent"], u"stop")
        yt = fr.H - y
        fr.put(str(n), x, yt + 0.255 * BK_LBL * PT, BK_LBL, True, "C", "FFFFFF")
        fr.avoid.append((x - r - 0.2, yt - r - 0.2, x + r + 0.2, yt + r + 0.2))


def bk_north(fr, x, y, ang):
    """North arrow at (x, y) page mm (y up), pointing at angle ang (rad, from page +x); 'N' is a label."""
    L = 7.0
    dx, dy = math.cos(ang), math.sin(ang)
    tip = (x + dx * L / 2, y + dy * L / 2)
    tail = (x - dx * L / 2, y - dy * L / 2)
    nx, ny = -dy, dx
    fr.pg.poly([[tip, (tail[0] + nx * 1.6, tail[1] + ny * 1.6), (x - dx * 1.2, y - dy * 1.2)]], fill=COL["ink_dark"])
    fr.pg.poly([[tip, (x - dx * 1.2, y - dy * 1.2), (tail[0] - nx * 1.6, tail[1] - ny * 1.6)]], fill=COL["white"],
               stroke=COL["ink_dark"], lw=0.15)
    lx, ly = tip[0] + dx * 2.6, fr.H - (tip[1] + dy * 2.6)
    fr.put(u"N", lx, ly + 0.255 * BK_LBL * PT, BK_LBL, True, "C", BK_INK)
    fr.avoid.append((min(tip[0], tail[0]) - 1.8, fr.H - max(tip[1], tail[1]) - 1.8,
                     max(tip[0], tail[0]) + 1.8, fr.H - min(tip[1], tail[1]) + 1.8))


def bk_scale_bar(fr, x, y, scale, marks):
    """Scale bar at (x, y) page mm (left end, y up): ink and white blocks; its numbers are labels below it."""
    k = 1000.0 / scale
    for i, (a, b) in enumerate(zip(marks[:-1], marks[1:])):
        fr.pg.poly([rect(x + a * k, y, x + b * k, y + 1.0)], fill=COL["ink_dark"] if i % 2 == 0 else COL["white"],
                   stroke=COL["ink_dark"], lw=0.12)
    yb = fr.H - y + 3.4
    for i, m_ in enumerate(marks):
        num = u"{:,.0f}".format(m_)
        if i == len(marks) - 1:                          # the unit after the last number, the number on its tick
            fr.put(num + u" m", x + m_ * k - text_w(num, BK_LBL * PT) / 2.0, yb, BK_LBL, False, "L", BK_INK)
        else:
            fr.put(num, x + m_ * k, yb, BK_LBL, False, "C", BK_INK)
    fr.avoid.append((x - 1.0, fr.H - y - 2.0, x + marks[-1] * k + 1.0, fr.H - y + 0.5))


def bk_context(BK):
    """Shared data of the four frames: whole-site base and bands, the covered reach, named places."""
    P, cov = stream_ref()
    sP = arclen(P)
    runs, a = [], None
    for i, c in enumerate(cov):
        if c and (i == 0 or not cov[i - 1]):
            a = sP[i]
        if c and (i == len(cov) - 1 or not cov[i + 1]):
            runs.append((a, sP[i + 1]))
    BK["covered"] = [max(runs, key=lambda r_: r_[1] - r_[0])] if runs else []
    BK["places"] = bk_anchors(BK)


def booklet_export(folder, BK):
    """v20: the four booklet drawings (option A) + booklet/blocks.json + booklet/results.json."""
    bk = BkBlocks(folder, u"MasterPlan", SHORT)
    bk_context(BK)
    V0 = View(BK["areas"], 0.0, 1.0, frame=BK["site"])      # the sheet's whole-site view, 1 m = 1 unit
    site_W, site_H = V0.W, V0.H
    places = BK["places"]
    u_mid = site_W / 2.0                                 # the split: two strips of equal length
    halves = {"c1_s1": (0.0, min(site_W, u_mid + BK_OVERLAP_M / 2.0)),
              "c1_s2": (max(0.0, u_mid - BK_OVERLAP_M / 2.0), site_W)}
    Wc, Hc = bk_frame("bergama_masterplan/c1_s1", *BK_FRAMES["c1_s1"])
    scale1 = bk_scale(max(b - a for a, b in halves.values()), site_H, Wc, Hc, BK_C1_SCALE)
    res = {"script": "bergama_masterplan_v20.py", "version": VERSION, "option": "A", "frames": {}}
    # ---- whole-site base and broad zones (the sheet's growth, on one corridor-wide grid)
    baseS = prep_base(BK["survey"], V0, V0.bb, full=True)
    G = Grid(V0.bb, V0, BAND_CELLS)
    RB_S = grow_band(G, baseS["streams"] + baseS["banks"], [s_["P"] for s_ in BK["D"].strips], RIVER_BAND_M, 101, "A")
    SP_S = grow_band(G, [s_["F"] for s_ in BK["CL"]["spine"]], [], SPINE_ZONE_M, 103, "A")
    # ---- the two 1:1,000 windows (chosen first: the halves outline them)
    wins = {}
    for bid in ("c3_a", "c3_b"):
        Ww, Hw = bk_frame("bergama_masterplan/" + bid, *BK_FRAMES[bid])
        wins[bid] = bk_window(BK, bid, Ww, Hw)
    # ---- C1: the halves
    for bid in ("c1_s1", "c1_s2"):
        W, H = bk_frame("bergama_masterplan/" + bid, *BK_FRAMES[bid])
        k = 1000.0 / scale1
        u0, u1 = halves[bid]
        dw, dh = (u1 - u0) * k, site_H * k
        x0 = (W - dw) / 2.0                                   # each strip centred in its frame
        y0 = (H - dh) / 2.0

        def F(p, u0=u0, x0=x0, y0=y0, k=k):
            u, v = V0.T(p)
            return x0 + (u - u0) * k, y0 + v * k
        fr = BkFrame(W, H, F, k)
        clip = rect(x0, y0, x0 + dw, y0 + dh)
        bk_layers(fr, BK, baseS, ("calisma_alan[0]", "calisma_alan[1]"), RB_S, SP_S, clip, False)
        for wid, w_ in wins.items():                          # the 1:1,000 windows, outlined
            pts = [fr.F(p) for p in w_["corners"]]
            if all(x0 - 0.5 <= x <= x0 + dw + 0.5 for x, y in pts):
                fr.pg.poly([pts], stroke=COL["accent"], lw=0.25)
                w_["on"] = (bid, pts)
        ins = lambda x, y: x0 <= x <= x0 + dw and y0 <= y <= y0 + dh
        bk_stops(fr, BK, None, 1.9, ins)
        ang = math.atan2(V0.uv((0.0, 1.0))[1] - V0.uv((0.0, 0.0))[1], V0.uv((0.0, 1.0))[0] - V0.uv((0.0, 0.0))[0])
        bk_north(fr, 12.0, y0 + 20.0, ang)                   # same corner on both strips: bottom left
        bk_scale_bar(fr, 5.0, y0 + 6.0, scale1, (0.0, 50.0, 100.0, 200.0))
        xm = x0 + (u_mid - u0) * k                           # where the other strip takes over (page mm)
        own = (lambda x: x < xm) if bid == "c1_s1" else (lambda x: x >= xm)
        bk_c1_words(fr, BK, bid, wins, (x0, H - y0 - dh, x0 + dw, H - y0), own)
        name = bid + ".pdf"
        write_pdf(fr.pg, bk.path(name), u"Bergama masterplan booklet " + bid)
        bk.drawing(bid, name, fr.labels, caption=u"Whole site, " + (u"upstream" if bid == "c1_s1" else u"downstream")
                   + u" half", scale_den=scale1, legend=fr.legend)
        res.setdefault("labels_not_drawn", {})[bid] = fr.missing
        res["frames"][bid] = {"scale_den": scale1, "w_mm": W, "h_mm": H, "from_m": round(u0, 1), "to_m": round(u1, 1),
                              "overlap_m": BK_OVERLAP_M}
    # ---- C3: the windows
    for bid in ("c3_a", "c3_b"):
        w_ = wins[bid]
        W, H, sc_, R = w_["W"], w_["H"], w_["scale"], w_["R"]
        k = 1000.0 / sc_

        def F(p, R=R, k=k):
            return (p[0] - R[0]) * k, (p[1] - R[1]) * k
        fr = BkFrame(W, H, F, k)
        Rm = (R[0] - 40.0, R[1] - 40.0, R[2] + 40.0, R[3] + 40.0)
        nr = BkBox(Rm)
        base = prep_base(BK["survey"], nr, Rm, full=True)
        Gw = Grid(Rm, nr, BAND_CELLS)
        RB = grow_band(Gw, base["streams"] + base["banks"], [s_["P"] for s_ in BK["D"].strips], RIVER_BAND_M, 101, "A")
        SP = grow_band(Gw, [s_["F"] for s_ in BK["CL"]["spine"]], [], SPINE_ZONE_M, 103, "A")
        bk_layers(fr, BK, base, ("calisma_alan[0]", "calisma_alan[1]"), RB, SP, rect(0.0, 0.0, W, H), True)
        if bid == "c3_a":
            bk_arrows(fr, BK)
        bk_stops(fr, BK, BK_C3[bid]["stops"], 2.3, lambda x, y: 0 <= x <= W and 0 <= y <= H)
        bk_north(fr, W - 6.0, H - 8.0, math.pi / 2.0)
        bk_scale_bar(fr, W - 6.0 - 50.0 * k, 5.0, sc_, (0.0, 10.0, 20.0, 50.0))
        bk_c3_words(fr, BK, bid, RB)
        name = bid + ".pdf"
        write_pdf(fr.pg, bk.path(name), u"Bergama masterplan booklet " + bid)
        bk.drawing(bid, name, fr.labels, caption=BK_C3[bid]["caption"], scale_den=sc_, legend=fr.legend)
        res.setdefault("labels_not_drawn", {})[bid] = fr.missing
        res["frames"][bid] = {"scale_den": sc_, "w_mm": W, "h_mm": H, "centre_xy": [round((R[0] + R[2]) / 2, 1),
                              round((R[1] + R[3]) / 2, 1)], "window_m": [round(R[2] - R[0], 1), round(R[3] - R[1], 1)]}
    res["places_xy"] = dict((k_, [round(v[0], 1), round(v[1], 1)]) for k_, v in sorted(places.items()))
    with open(bk.path("results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    return bk.save()


def bk_window(BK, bid, W, H):
    """The north-up window of a C3 frame: centred on what it shows (c3_a: the reed basins, retention terraces,
    spillway and the commons of the upstream entry; c3_b: the K5 bridge, moved just enough to hold Demeter's
    Garden), at 1:1,000, else 1:1,250 when the garden and the bridge do not fit together."""
    spec = BK_C3[bid]
    zs = [z for z in BK["D"].zones if z["area"] == spec["area"]]
    if bid == "c3_a":
        pts = [p for z in zs if name_of(z, z.get("own", "")) in spec["names"] for p in z["P"]]
        if not pts:
            pts = [p for z in zs for p in z["P"]]
        b = bbox(pts)
        c = ((b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0)
        sc_ = BK_WIN_SCALE
    else:
        k5 = BK["places"].get(u"K5")
        dg = [p for z in zs if z["code"] == "DG" for p in z["P"]]
        c, sc_ = k5 or inner_pt(BK["areas"][spec["area"]]), BK_WIN_SCALE
        if dg and k5:
            b = bbox(dg + [k5])
            for s_ in (BK_WIN_SCALE, 1250.0):
                ww, hh = W * s_ / 1000.0, H * s_ / 1000.0
                if b[2] - b[0] <= ww - 20.0 and b[3] - b[1] <= hh - 20.0:
                    sc_ = s_
                    cx = min(max(k5[0], b[2] - ww / 2 + 10.0), b[0] + ww / 2 - 10.0)
                    cy = min(max(k5[1], b[3] - hh / 2 + 10.0), b[1] + hh / 2 - 10.0)
                    c = (cx, cy)
                    break
    ww, hh = W * sc_ / 1000.0, H * sc_ / 1000.0
    R = (c[0] - ww / 2, c[1] - hh / 2, c[0] + ww / 2, c[1] + hh / 2)
    return {"W": W, "H": H, "scale": sc_, "R": R, "corners": [(R[0], R[1]), (R[2], R[1]), (R[2], R[3]), (R[0], R[3])]}


def bk_arrows(fr, BK):
    """The water links of the zone base (collect, clean, hold, return) as the sheet's bold hand arrows."""
    for i, L in enumerate(BK["D"].links):
        if L["kind"] != "water":
            continue
        P = fr.T(L["P"])
        if not any(0 <= x <= fr.W and 0 <= y <= fr.H for x, y in P):
            continue
        fr.pg.clip([rect(0.0, 0.0, fr.W, fr.H)])
        link_arrow(fr.pg, P, "water", L["heads"], 3 + i)
        fr.pg.unclip()
        fr.leg("line", link_cols("water")[0], u"water moves (arrow)")
        Pt = [(x, fr.H - y) for x, y in P]
        for a, b in zip(Pt, Pt[1:]):
            n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / 2.0))
            for j in range(n + 1):
                x, y = a[0] + (b[0] - a[0]) * j / n, a[1] + (b[1] - a[1]) * j / n
                fr.avoid.append((x - 1.2, y - 1.2, x + 1.2, y + 1.2))


def bk_ring_tl(fr, L_):
    return [(x, fr.H - y) for x, y in fr.T(L_)]


def bk_best(fr, loops, cb):
    """Of world rings, the one showing most inside cb (top-left mm), cut to cb; None when none shows."""
    best, ba = None, 20.0
    for L_ in loops:
        R_ = bk_clip_ring(bk_ring_tl(fr, L_), cb)
        if len(R_) >= 3 and abs(area2(R_)) > ba:
            best, ba = R_, abs(area2(R_))
    return best


def bk_zone_loops(BK, z):
    """The zone's free-piece rings (world m), else its own outline."""
    for key in ("calisma_alan[0]", "calisma_alan[1]"):
        for pc in BK["pzs"].get(key, []):
            if pc["kind"] == "free" and pc["zone"] is z:
                return pc["loops"]
    return [z["P"]]


def bk_clip_ring(R, cb):
    """A ring cut to the rectangle cb = (x0, y0, x1, y1) (Sutherland-Hodgman on the four sides)."""
    def cut(P, inside, inter):
        out = []
        for i in range(len(P)):
            a, b = P[i - 1], P[i]
            if inside(b):
                if not inside(a):
                    out.append(inter(a, b))
                out.append(b)
            elif inside(a):
                out.append(inter(a, b))
        return out
    P = list(R)
    for ax, lim, keep_lo in ((0, cb[0], False), (0, cb[2], True), (1, cb[1], False), (1, cb[3], True)):
        if not P:
            break

        def inside(p, ax=ax, lim=lim, keep_lo=keep_lo):
            return p[ax] <= lim if keep_lo else p[ax] >= lim

        def inter(a, b, ax=ax, lim=lim):
            t = (lim - a[ax]) / ((b[ax] - a[ax]) or 1e-12)
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        P = cut(P, inside, inter)
    return P


def bk_c1_words(fr, BK, bid, wins, cb, own):
    """The words of a whole-site half (plan C1): places, bridges, the commons, the gardens, the spine, the walk
    lengths, the windows of page C3, 'continues'. Each word goes on the half whose side of the split holds its
    place (own(x): page x on this half's side), next to it, with a leader where it cannot sit on it. cb = the drawn
    rectangle (top-left mm)."""
    places, ref = BK["places"], BK["CL"]["W"]["ref"]

    def at(p):
        x, y = fr.tl(p)
        return (x, y) if cb[0] <= x <= cb[2] and cb[1] <= y <= cb[3] and own(x) else None

    def one(text, p, bold=True, colour=BK_INK, shown=None):
        a = at(p) if p is not None else None
        if a is not None:
            fr.place([(text, BK_LBL, bold, shown)], a, colour, min_d=1.5)

    def area(text, loops, colour, fill=None):
        """A name on its piece: the half holding the centre of its largest ring writes it."""
        if not loops:
            return
        c = inner_pt(max(loops, key=lambda r_: abs(area2(r_))))
        if at(c) is None:
            return
        R_ = bk_best(fr, loops, cb)
        if R_:
            fr.place([(text, BK_LBL, True, None)], inner_pt(R_), colour, inside=R_, min_d=1.5, fill_colour=fill)
    pin = [p for p in ref if bk_in(fr, p, cb)]
    one(u"UPSTREAM ENTRY", pin[0] if pin else None)
    one(u"DOWNSTREAM END", pin[-1] if pin else None)
    for nm, lab in ((u"K4", u"K4"), (u"K3", u"K3"), (u"RED HALL", u"RED HALL"), (u"K5", u"K5 ÜÇ KEMER"),
                    (u"K6", u"K6")):
        one(lab, places.get(nm))
    if BK["covered"]:
        s0, s1 = BK["covered"][0]
        q, _ = at_len(ref, arclen(ref), (s0 + s1) / 2.0)
        one(u"COVERED REACH", q)
    for key in ("calisma_alan[0]", "calisma_alan[1]"):
        for pc in BK["pzs"].get(key, []):
            if pc["kind"] == "hub":
                area(bk_word(pc["name"]), pc["loops"], BK_INK, piece_tone(pc)[0])
                break
    for code, nm in (("DG", u"DEMETER'S GARDEN"), ("WP", u"STREAMSIDE PLANTING")):
        zs = [z for z in BK["D"].zones if z["code"] == code]
        if zs:
            area(nm, [L_ for z in zs for L_ in bk_zone_loops(BK, z)], zone_tones(zs[0])[2])
    edge = [s_ for s_ in BK["CL"]["spine"] if s_["kind"] == "edge"]
    if edge:
        s_ = max(edge, key=lambda e: arclen(e["F"])[-1])
        q, _ = at_len(s_["F"], arclen(s_["F"]), arclen(s_["F"])[-1] / 2.0)
        one(u"STREAMSIDE SPINE", q, colour=MP["centre"][2])
    for bank in ("NE", "SW"):
        runs = [x for x in BK["CL"]["W"]["runs"] if x["bank"] == bank and x["cls"] == "bank"]
        if runs:
            x = max(runs, key=lambda r_: r_["m"])
            q, _ = at_len(x["F"], arclen(x["F"]), arclen(x["F"])[-1] / 2.0)
            m_ = BK["CL"]["W"]["stats"].get(bank + " bank", 0.0)
            one(bank + u" bank walk " + BK_WALK_VAL.format(bank) + u" m", q, bold=False,
                shown=u"{} bank walk {:,.0f} m".format(bank, m_), colour=COL["walk"])
    for wid, w_ in sorted(wins.items()):
        if w_.get("on", (None,))[0] != bid:
            continue
        pts = [(x, fr.H - y) for x, y in w_["on"][1]]
        c = (sum(p[0] for p in pts) / 4.0, min(p[1] for p in pts))
        fr.place([(u"1:{:,.0f} window, page C3".format(w_["scale"]), BK_LBL, False, None)], c, COL["accent"],
                 min_d=1.0)
    yc = (cb[1] + cb[3]) / 2.0
    fr.place([(u"continues", BK_LBL, False, None)], (cb[2] if bid == "c1_s1" else cb[0], yc), BK_INK2, min_d=1.0,
             leader=False)


def bk_in(fr, p, cb):
    x, y = fr.tl(p)
    return cb[0] <= x <= cb[2] and cb[1] <= y <= cb[3]


def bk_c3_words(fr, BK, bid, RB):
    """The words of a 1:1,000 window (plan C3): zone names with their keyword lines on the fills (a leader where a
    block does not fit its fill), the commons, the promenade, the bridge."""
    spec = BK_C3[bid]
    W, H = fr.W, fr.H
    cb = (0.0, 0.0, W, H)
    br = BK["places"].get(spec["bridge"])
    x, y = fr.tl(br) if br else (-1.0, -1.0)
    if 0 <= x <= W and 0 <= y <= H:
        fr.place([(spec["bridge"] + u" BRIDGE", BK_LBL, True, None)], (x, y), BK_INK, min_d=2.0)
    else:
        fr.missing.append(spec["bridge"] + u" BRIDGE (outside the window)")
    key = spec["area"]
    for pc in BK["pzs"].get(key, []):
        if pc["kind"] == "hub":
            R_ = bk_best(fr, pc["loops"], cb)
            if R_:
                fr.place([(bk_word(pc["name"]), BK_KEY, True, None)], inner_pt(R_), BK_INK, inside=R_,
                         fill_colour=piece_tone(pc)[0], min_d=2.0)
            else:
                fr.missing.append(bk_word(pc["name"]) + u" (outside the window)")
    for nm in spec["names"]:
        zs = [z for z in BK["D"].zones if z["area"] == key and bk_word(name_of(z, z.get("own", ""))) == nm]
        R_ = bk_best(fr, [L_ for z in zs for L_ in bk_zone_loops(BK, z)], cb)
        if not R_:
            fr.missing.append(nm + u" (outside the window)")
            continue
        lines = [(nm, BK_KEY, True, None)] + [(s_, BK_LBL, False, None) for s_ in BK_PROGRAMME.get(nm, [])]
        fr.place(lines, inner_pt(R_), zone_tones(zs[0])[2], inside=R_, min_d=2.0)
    R_ = bk_best(fr, RB or [], cb)
    if R_:
        lines = [(RIVER_BAND_NAME, BK_KEY, True, None)] + [(s_, BK_LBL, False, None)
                                                            for s_ in BK_PROGRAMME[RIVER_BAND_NAME]]
        fr.place(lines, inner_pt(R_), RIVER_BAND_TONE[2], inside=R_, min_d=2.0)
def make_board(opt, alt, pages):
    """The four working areas side by side (two rows when wider than BOARD_MAX_W) under the sheet's title."""
    M, HEAD, G = 14.0, 24.0, 10.0
    rows = [pages]
    if sum(p.W for p in pages) + G * (len(pages) - 1) + 2 * M > BOARD_MAX_W:
        rows = [pages[:2], pages[2:]]
    W = max(sum(p.W for p in r_) + G * (len(r_) - 1) for r_ in rows) + 2 * M
    H = sum(max(p.H for p in r_) for r_ in rows) + G * (len(rows) - 1) + 2 * M + HEAD
    bd = Page(W, H)
    bd.poly([rect(0, 0, W, H)], fill=COL["paper"])
    sheet_head(bd, M, H - M, alt, opt)
    y = H - M - HEAD
    for r_ in rows:
        x = M
        hr = max(p.H for p in r_)
        for p in r_:
            blit(bd, p, x, y - p.H)
            x += p.W + G
        y -= hr + G
    return add_legend(bd, alt, _ALPHA[0], M)            # v17


# ================================================================ v17: the legend band (only what the sheet draws)
LEG = {}                       # what the sheet being drawn uses: key -> sample data (reset for every sheet)
LEG_ZONE = [("WS", u"WATER STORAGE · RETENTION TERRACES"), ("WT", u"CLEANING · REED BASINS"),
            ("WD", u"CLEAN WATER BACK · SPILLWAY"), ("WA", u"AMPHIBIOUS · BED"),
            ("WAF", u"AMPHIBIOUS · FLOOD TERRACE"), ("WP", u"RIVERSIDE PLANTING"),
            ("GR", u"GREEN · SHADED WALK, DRY TOP"), ("DG", u"DEMETER'S GARDEN"), ("WI", u"AGRICULTURE"),
            ("CH", u"HERITAGE"), ("MC", u"CENTRE"), ("HO", u"HOUSING"), ("CV", u"CIVIC"), ("SR", u"SPORT"),
            ("PA", u"SERVICE")]
LEG_CTX = [("river", u"RIVER"), ("street", u"STREET"), ("park", u"PARK"), ("heritage", u"HERITAGE BUILDING"),
           ("housing", u"HOUSING"), ("building", u"OTHER BUILDING"), ("cleared", u"CLEARED GROUND")]
LEG_SW, LEG_SH, LEG_ROW, LEG_TS, LEG_HS, LEG_GAP = 22.0, 8.0, 11.0, 3.4, 4.0, 14.0   # sizes, mm


def leg(key, val=True):
    LEG.setdefault(key, val)


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
    for nm_ in (u"MAIN SPINE", u"RIVERSIDE SPINE"):
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
            (("s", "street"), u"STREET EDGE", line_sw((COL["road_edge"], 0.3, None, None))),
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
        lines.append((u"RIVERSIDE SPINE", line_sw((COL["spine"], band, None, 0.75))))
    if ("spine", "deck") in LEG:
        lines.append((u"RIVERSIDE SPINE · DECK, NO ROOM ON THE BANK", line_sw((COL["spine"], band, [1.4, 0.9], 0.75))))
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
            (u"WALKS AND SPINES", lines), (u"LINKS", links)]


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


def sheet_head(pg, x, y_top, alt, opt):
    pg.text(u"BERGAMA · GROUP 6 · " + ALT_TEXT[alt], x, y_top - 7.0, 7.0, COL["ink_dark"], bold=True)
    pg.text(OPTION_TEXT[opt], x, y_top - 13.0, 3.4, COL["ink"], bold=True)
    pg.text(CREDIT, x, y_top - 18.0, 2.6, COL["ink"])
    scale_bar(pg, x + 170.0, y_top - 13.0, _SCALE[0])


def scale_bar(pg, x, y, scale):
    """v16: 0-50-100-200 m bar (ink and white blocks) and the scale as text, at the print scale 1:scale."""
    k = 1000.0 / scale                                    # page mm per metre
    marks = (0.0, 50.0, 100.0, 200.0)
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
    return {"runs": out, "covered": covered, "stats": stats, "ref": P}

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
    return {"W": W, "spine": sp, "main": [tuple(p) for p in spec["main_spine"]], "stops": stop_points(spec, D, areas),
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
            word_along(pg, max(edge, key=lambda P: arclen(P)[-1]), u"RIVERSIDE SPINE", 2.6, COL["spine_dark"],
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
            pg.text(nm.upper(), bx, by, 2.1, COL["ink_dark"], bold=True, halo=COL["white"])
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
    out = {"script": "bergama_masterplan_v20.py", "version": VERSION,
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
        if opt == "A" and CL is not None:                # v20: what the booklet drawings reuse
            _BK.clear()
            _BK.update(areas=areas, site=site, survey=survey, D=D, CL=CL, pzs=pzs, alpha=alpha)
        for alt in (1,):                                 # v19: the one sheet
            name = OUT_NAME.format(opt, alt)
            t0 = time.time()
            LEG.clear()                                  # v17: the legend lists only this sheet's entries
            try:
                pg = make_board(opt, alt, [draw_area(spec, opt, alt, D, bases[spec[0]], pzs[spec[0]], scale,
                                                     alpha, areas[spec[0]], CL) for spec in AREAS])
                path = save(pg, folder, name, u"Bergama masterplan v20 option {} (opacity {:.2f}, "
                                              u"1:{:,.0f})".format(opt, alpha, scale))
                files.append(path)
                pages.append((opt, alt, pg))
                lines.append(u"{}  {}  {:.1f} s".format(os.path.basename(path),
                                                       datetime.datetime.now().strftime("%H:%M:%S"), time.time() - t0))
            except Exception as ex:
                import traceback
                lines.append(u"{}  NOT WRITTEN ({}: {})".format(name, type(ex).__name__, ex))
                warn.append(traceback.format_exc()[-480:])
    if CLs:                                              # v11: what the other scripts read
        try:
            with open(os.path.join(folder, RESULTS_NAME), "w", encoding="utf-8") as f:
                json.dump(city_results(CLs), f, ensure_ascii=False, indent=1)
            lines.append(u"{}  {}".format(RESULTS_NAME, datetime.datetime.now().strftime("%H:%M:%S")))
        except Exception as ex:
            lines.append(u"{}  NOT WRITTEN ({}: {})".format(RESULTS_NAME, type(ex).__name__, ex))
    if _BK:                                              # v20: the A3 booklet drawings; never breaks the sheet
        try:
            _BK["spec"] = city_link()[0]
            booklet_export(folder, _BK)
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
ZONE_COPY = (
    "eNq0fVurdt1R5V+R7zp5mOdD7tJgN9K2itp4ESREDE0gRonxwm78771G1RhVa+8gtB3MB2Ez3rWeNY9VNatG1fzZ//nh17/411/+9oef/PDn//S7X/3j"
    "b37+05/85E/+7K9//jc//es//suf//Pvfvurf/rhRz/8xQ8/+dnP2l2jfUb7UW+7r8/ef/uj38NWYH0bNr9g/tz47BlY8+f6F6wb1j67J2ZQ/ewaUD2G"
    "lc8637B2Pyt/rl7Dzme9fs5+r+3Pyt9r07D1yRY3f3V+VsteVMPGZ716ZtDTifH919rnvFriWP3cS+z58xCrM7C9DCvPiAU2DKv3M/Ldar2oJ3tbniYY"
    "tj8nIG9xXZ/Lx/r9nEWsnMD8zfkMGKHzuf6F8cxTYMN6UfunB1T8sZaPPSPrjz2tTMxXRS2fUgNr1rpyPicxn7KyNRV41ZD1GfmUfaDM90e3jWYZ7z4U"
    "/7H+qSv7YA0uLRt3nhVoWH1aFEPCd8un5TB1YOs+f6zA1jbs+eHEbOzWfdq5YypqN2zlmi2+yNad7xlzaDy/EZgNO7Ayv2M9upHvNk0PvnAMehZR/lz1"
    "1pXPHNliTMU6uXvQs2XYiQ2PEbDfO88ay1Ep/tyzyE6OaCNWcuRtCazzrLKRM+TffVbZ19WzTv+0kUvAH3tWmX5u+fZZp74xn4zz9HsGhrW99n02fkDV"
    "WrxProH5uY49KzCgY1/dTydaYNuxZ356YP7V3WPDA/Ofazl4z7sG1c+6CVkndgkxg5YAWvczs1/FxmSdT3arWb/W/oyeXbVfW+sZ6sC2fXXNkCjYZNaJ"
    "Nd77Zzr2Zdh9TBbkcu4fx2oO8eUsLsibwKZ1Yz6yJRejIU8ncn0ex3aMCeSd7ZS5PicVTRnESkr85c/N+OrorgXWHLG2H8wGYPbUW0OP9U8JyLo1s6sP"
    "dG3U59Mi7bvJYZ8ldcD8DPvCgGgNbDVipQfmjz2r7iRkPzf25/WUdWs8k3jz1/zVGUIGmEHjk23zKXx6PPPXhmPtjXVvW/3M9q1fECz51WpfhXrIb7gY"
    "wzqoidnvYZu+nrPfwzp9/Z4tiWeFt9d3bSYey6Dmu8N/75md/bW3vYaMeaDj2LOI9InlS+wxAnZCPhOPERAGxHZ1vGAEzMC2tQ5GgEbqWan+7szl+YhA"
    "G4HHCjh87lkMpsmASdxNquj1mAadTX4Wl+/jllLhwe4lJuXzLMvr30ij51nR3t2WG29KfDzmgj4B9UJIOmpCDQF7LIjLXfFsQt9lD6ZF8GzVtohp4J8t"
    "7dIdlkYNzHftg0mSr8qheqwPDd8jNlzOPli5gfmKf8wPfddEjmGP6KuBuQB9MIn3B/OhemwS6VWIMBvSxyY5IzD2rcd0PNh0rMXwAfNv1FjMwLwtqR3x"
    "ezZ+JbXjg3V77jFedj7nYuUxXk4LrBi0YpE+3fBZK9A5gc1JrATkSu+xaCRCHqz4qz1MgWdEj7cEQjIwX/SPRSNz68EGnpuP9XLz3W7QCckFWV8N22GD"
    "J7Zy4GnTz8d40fp+MBvQedMIe7Dr3+ihRZ9usCnPds5x2gaVbMrwLTkfq0SPPTLuEIrOLpcX8zFUYqlslyvzMVSkRR/lactxwlDRoFxXLMB6Yt7ix1DR"
    "yeTRz4eQNinUuLX4sV1k0T3afg5isix2d5tpPgbNEjY4oCfNtz1di87HyNEq29zgwCon47FGpj/3bDkOy6bZDExrZW/fpfMxhgaH6jF4zEScjzUk4fVg"
    "ZxPj/OAvh1JVbyr0id9NzD+xc4M/2PV3VxgcTwt8lDdUVGLTsDxN4V3/Rg/5jW/YEDxjm5CpyLnzNIXmTWIlf677Z0uO3nXbZz6zLC2MEbBPPCskZvcR"
    "d/YuVlKOlEMrTCSzIA17LYztlulcr0WgycAOzknzV1+9oPE7V+4CYDYoj3he+dyxEYAtlS22jj3SvmeD7dcepRAN0YJ/dEdJzBryqBjtKawZx7K9z9rq"
    "/oUUoUeS4VF3gjq32aMVJZGxHTqxeJVmw3w0qiToswv9uQfTqetQWc9x4sxxNOwjF+gjEXwPPJhm7FIxz0e7S+Y9Mqc1YlKutyU2+I1HXglSUyDWJjEN"
    "3p0UXI+hoe4+2J3EpDQvDXFgmh+cDxsxiel71OQZihTieRDTor1+Zp8jt8/luRMY9wCOry59HqNwBHT8C00CCSdfDl7VIAPzLfVgZQTmWwWnSD1H18t8"
    "7ETaesB8/dipLzA7Zs/HThz6vWd52YQ/duIMyE7F8zETZz7miqWH5gd2/Of6R50dbnXO3nScAua65jEdX5grll4Sm+wFHEgB2QljPqZjfHXpsa2VB8xb"
    "8piOgW3Kj8d0nBqUQ+3wmIlb37i+RVuc7eEiGda61mOcYKE41uQXgMslsMHmPRbPJFQEDUJhS8LP4yrkwai74Q4KjDseniRiRQYNPE6BUbPCMzUJUeTD"
    "geUL4PmDX22Vevp5nAc7+MhcRD+YZuLpdtNzWjtmWBNT62CA+7snhhOjPYmpZ80PBfPpDa1fQK5Xay7FRifDrEvHeGCHkBp33N6cdcagw71ofX2Geqlx"
    "Vw3ukuTAhr/bJPGBuSR/MI5TL2xvjS32QG721JCfwFzRPktIo/6s8e5Ybjs4Tm2ZlPAUwL9qFveEU+0EZj6b+Sx7reJna5lDdj47Zp7A+Htddgr8uv5z"
    "TaIc7l8fAIiMFdgWVtTb5WsHfjYi262PARGnhhw3fMcjCndA5rMCFD92/QPjxlF0P5LKdvGABObP4eRLqOqx5oJy3Nywj8xsi5h256AqG3fEMMFTcIkV"
    "YdNX53j0CA86e/BwBkxNHptNaRKA0F/+a49hwM7CjbCJacEOLp0Bk5mT8+jXOYnRnt2z+pIdj4bcifngwY7Wu43vnhPjPqnMx6OFaQsDsyMcMI3KYzqY"
    "vT1OWH3AbKGMR9NLUsyp555/PIHx93r01ywWYjxiApv+bpNGBuYjf+IIt2EAOVZkHAGzDT92SPfHdDKVN2Dq7cCWDQtsM332uqE6HoP2BDT9sRlrGwfl"
    "Zlh4boH5iD5YIUS3wNhhWAHbjjXtAZyu/M1nR7MhMB39q+GjAWb+yLFudGJR440VBtOGeUqockgeK7YYtENSPtDxx8JJvZ9/toM4sKLWUQcMOBXVErqG"
    "h53aHHsa6vsHp3R+dle3oYad8InRvQeMhjqw61jqcjhYO7F4bnDwnlGUOMIx4xKTCH1mb/h3S+yCzVMisKbfY9BgPJOsFa8jEjCJXywkg05IlUN//rCl"
    "FZhvNHg42Q2s1UmsJGaHzvGsaE3Hs867Y1NCz86GBg05woCdS6zp5zrlxbNZtS+OG7QD+3wn5L2onxfkb8qnZJB9dKTi1o89wkpKFVvVugpj+2Y7CEVP"
    "1VwYvSMw356P1JQARVetIbBma2AuAh5pTXveMFsoIxVNYiVnh/7iAdd0DqcLaZip2WSz8Ab0UA6nt6WH/3kjZOHYzL4N18mjj7C/DkMGA8pU/VjuRR+9"
    "KS6zD8Nho0d8AJgdJAaUvbCjtpSPuqa919KKehSAr4CWM3QZIhxmxRCrlJYtPCX70UUuy1qaQpcuJWCSyFdD1WassiuJhCgph8DcQYb1kI0P5qK2RXAO"
    "mAUcBixaQpNr77EeV2Iu4GCW7sBc1MLerInZz8GQfL1rTalp08ODZSuj7hBdOtYB0+q7ww8wA+ZgD6z7c1NOcgyBncNGDc8QsOHfeA1B+1xCNUfZ7OHx"
    "mINakM8M+aw9BuHqgbkVUsNRgNmdhGKNXgqukkezBzObbjw2oizYZ025wCwvKUU3xnhsRAnMB7OWlPCMYSnzEyO3Gj1yAyZiYj6gOBqu2Brm0x4lfNqG"
    "GVRyV03/RL8RKI6f63fHuoDtsQxbofgfzNRDvzk/8Ch0w0YYOoc+8o6JWjEqpnA7bLMW2PDnqo72wK5/I1ULtqS15YSnDZhJuY4XZkxaFSZ74NJs6Ccl"
    "EGy8a9iSX98WgWMzDIJL3dLhlczFsrwtPQ5KD2aqvps4Dsx0EDCN/SVLoZ+ai7S6lOtQeDsxG6t9Y+tWm8meTkRriX1hR+DFWuxvBrHEemYthoF1cgTs"
    "qzCwXiM1iL1Gzzr2GAs1l/zxx9JyfDCfSFhYKzDT/R0WVo/J9QW0gn4BzHZpX9k1bBd79zGYZi4009b9sZ1emAmbDld2bjU7K3WYbif3lT8XjpsH4s+1"
    "MO4fzEcA8djcfd6Skkpouaepz1x6h5GxPncuUR6M+8S+ydbZBD1mSGy17aZOn3kwRG/993o4biRE+mw5UiQCdPgMR46yP1fy964rxP6YHSu3kA/BiGie"
    "bSGDxHvJZfGYGLkqfM2O9V7bpjb7mKnSqrvp+hi5tpu7lfpIY+o21+AdgdUU3tufSw0OGe/PvQR19zMAMFk79Db2fnPLd25v46wkZp3tO7c3LeXewwNp"
    "2voQK/mcnSl6D5pPbu/HYNGSejAXhY/B0l8b0t9tKX6Kn+/6Y7C08U109RJnw1tcXfeW4vvSx9XfVkcxN3Rv4SDFZ31jPAbGS/r45Lbx7poPS0vPCmZj"
    "EytpsPisgXOVRkf150paCYPStt63lWAGS38sB22XuzwIBiysju0uzQ7fUkAuQx7DQb/msQQgPBleHvH7Y0n0gLZ/csgnceDQ9Z/vMn6AXWEcplPoMexV"
    "ttRBgNAfC1sKmNlIvYa3/sApe4nR9gFm/sz+WBIcufNofOtVOTIuALlagbNJrzKwBSxat9zHh9bNGc9ddqKMgKKzt8YnOJhD+gJYjB3tF7RYIzyysxzP"
    "rRVrg6Jpjc7WTye0VwyxnTxsRcTsHC0cGfYPFospzDyZDO1lv7ljEWtT7pLLOMfzXyyJxd30QCFQFtv7LP+exqpL92ebyPS7ZGoAC6NWs9PSQIIbSzux"
    "5fLnNtlxyrwjd/FOG356W27oLdj1mxLg9XtuIPWaW3b68QlYnDGm3m1hX14ZevA7tsB8RMEnHYF530Dbyn3n4uORliVHWUK1fYdujuh2fyNEdAgAWroQ"
    "76F76JOCGjiJNamLEPm0dKFWXkcWN9XgKswRKI1q6rxm6FDB7RxRn91x0pDqHiiEvpyJ2QEfenWkbnBraNaU+SQHQE/XFKA+8jNoFKYepeNv/2bAgaKS"
    "OsRVJmyG1MpuIs60hiDzZYPI4oIOubRVXpC/ehXJTBUCM+elfjqxm5azmyVws6U1sBctqZW/dycNrvmysI8Ms7QQfHPA+ZVDwN9bqb4bpehjENb2bZgf"
    "w/GluywcB+x+O1jD6IzlwhgYjNM8VLrmf2zY2C/DZReIh6+j9qRJnCdy1/twn+VxuR0a3TvXIw3s13qcfgyGEZ8CyPUlwssBxSGh5p6Pw0TLL/iqgLcr"
    "dwYPSj0PNmR+4GAzE3P1e2b4ErGDeE7a9Vv/z5cN5BvjnMQ6N8bLUX6pRbCK0szzhQJL5AQ2eVIcr+0zeaKURw/nn8aTZ8s15mauSew86+jUenP7GLuz"
    "m6T7etZ5H4LJoehJSLbzjzcl/ZfAdM7uX49JwNIGd4cWgsFpp7k3p+QxRL6H8hIVxb0biNOmVHCvNsJJr4Pook/hLY0aXQ8ljeYi7KQ17C69x7KYqePc"
    "YfQKgcmcG2m82HrqxGKIF33TMIbSxPOQUg0XqQWX6KRZqUTky4k14SaeeYEC8QGur/V63ZEK0/AG5P4tRCx3YOHLqvnclB8sDgiX/qi3saHgETISoiXu"
    "RHx75I68eSM/uznCLbhqYeCadzCtkkEn4k4DJJyNL8+dx1JgMKT93eXjbC9VNugLLbkorvyjOx2VHiaCHzX3mI9e7+H8N8cMsZc/odBVO3OfmDyBS7el"
    "c8e0KrCT7jL3vvX1Pv+zyTs+i1PyJBau6SWX7snvLg4VLJA82C96sOXZ0Fkf2M0Duy9jeL9fPoFNL/muX30HY2TU9mhpg0NSv7nzRoZBD6n28NjP9Ex7"
    "mGTsfJeG1HgZJTEEYPm8PN3fQww7AxEnP1EVwyjffBGIddRXNybDJC2b7B7xx9YIT8507grCLuF3mGrKSb/DoCt5ph0Fz5miRyMDCgoytYxPFAWjbo3I"
    "jkf8VnoK4DhrCniNCCj1qsDYicDTqAqgRcxqCtKZYNOTg3ic5NueanF6bbbk4GOm6LgKz9kkpsndXc3bcZ547Ak2ZcdI7arvHpEXYJwo+BifLVwr60Z8"
    "k+5RQHL64Y3J+KYk95ITemcAZNGDhtioPrEWN/jOA5V1UqHWHnFQ30I7ss4QL/UY8haVfovxiwCvvEBgHx/GgaWUYCpWxYbzOZe2O3IaEM5l104svUUO"
    "BkLSkt7PsvHROxHbWRJnJ5fZqoyXJi0UsWaX1CdV8JKmPhF/RlRzEJIj0KKaDNRr8026PRHQl7pFWHOKDDAisO4DenK+kbhxSS6IALyTcIyXMCPuP8Rp"
    "kFEPzkAV92EE38DDKebUSl4CiRQ6soGVuETCWEFzGIQ0FZNHBHA6JC0GU53GzXj+oEcSHJGRXA1STla0DpHNQcqJVNogSQxYMDgUZLoZdhk8PwOTDTJ4"
    "igP7Jakp9tn5iokooxCY1MjgQQz0Gi2LQc0HTPLX3I6k6+gEo9w2YDcZNs6SeoVxuuiJjwkX727yn0rSZDqFN7ATTJ9NztFMqC1ykzSP0LOdHCZF2R5s"
    "dHKdSj7nTNaXAdeHTyR4UtqPndQU8Kl2cpguSVdSkL2Ti1l7LOROR+1M/xtoUk7HBYluJp2qkSc2k4q1yTCbgZRLbppWQBc9s6YQaDT1jE5Xk2I2yM6T"
    "5G5b9MT6Saqb88RaumlbkP3SRdHo4AHFUFsPbMMm2mHS83xFZX6r0fiEBYutcH5aEj3Qo0MsaIwvBqS2MhJGKjFtqmccfZCfxrfgLB7xKYPY6HTXNqNj"
    "VTzBlsyuyvSS+fJ6VfFTW+QCgGPp/NSW5DFw8CqxYEAWdeLkc2K4v6LtxRkib0Lp5Trp6Wouot/3GqYAiKKT2E3yaBO3VUu7MEFv9uDLG/H0kCqrDW/O"
    "WFJqV75LrmzkOxmRdZOhuwJy2n9PAwnO20vC70yu7BUxWNsi+LOg2yXm/EnETZK26+T40d9YF5f5xfjdokG/MJ9w2KYjiMaevgA29wzicl9ih9/kRi+y"
    "zUtQqMU/V24FCNmN3HVlFshXC0x5tXBUXmLBKxc5/MGU6nOV6TJrkrm73q2R9KeoE7CV1HWx7c+L4n7Jyhcn/ZAbPpuWGRjzsxMTrfxEZkHI/CX7H8R/"
    "0dRP9Cyz3B9ToU8mDagXh34WYMp0geXRmG/QIkHAabAzKwQc+lSQqqDUVZB4OjMalDl0vBoAII0xmFODuRDKczmM4iFnouVzvjFWyZ+rr3yLmdhlXsbr"
    "G64JYcjlZ5XRETktdPkh82NkizsTRPr81jHk6QbkzFikm+wYp6KslBGQCwFY0om5KNuv3ArylZANo/TLQ+8WEml6Pue7dvccu5GJOfM1i0rgUVLYYZIi"
    "En3yE0obKgn1ruyinOzITFLq2GmZwaR8Zvy5mf2kXXEKZ9FIaZkipKwrzew+7NkJWoplyFRmcem7oAA2YsosReaSksJmZmK5xjyvVCeGToApzQPnis5k"
    "tNoiK8yTJmAjJ+ZyC2krPTLKXDYiyj0i8cy1KLxuKxLUXFHBrZF5bIsZdVo/iymewLS4n+Xl2xsutsTc9LuZ67N45AemPQpSqLL7RmL8RpaOgA/8ELv5"
    "XGQQKvM1saj1kK+GiWTJ7Jd5iz2fY7pkye7SDbAslyW7sZkbqVHGDlMK5Q1oDKVa7sCWsjRLZhV6mQT4JXOUPc+3ROGARQI3ckOV1IzJGMwhVXbSOplr"
    "2l9Y5KRm4qIndsPfmN/oizmuSpVbpK4iP/aub92oceQH5unPNfhFNpGHOb2RHztZxSF9jsjJPMovfmWlMoW5yMJeOgUjXXlkVqonhSMi3yNvmKnTLVNL"
    "i+tvpE5rmCdz+YAp42uylgcw6a+5lbI9VHcAKdHje8Z2ZE7PzKYm+/Cd7T1JDlhpTyI729OLkSk+Iovb05rbzueaMsBTWYHyspiN3gMqgm4mlHttA9iO"
    "NZPMN/PdpdUH3fPIi5e0MUebcuXzOR8VBFZfieybafbS1kMZ4JlnBcyzmvvM0gA30/tHfjfLAKzEVC4gajTcLCvQ8rnWWX6g5e91VimoryZfVjOo+eq4"
    "rHrwwrz4xMgMzHGzhkLLpkSthZbPZUmG17uXpRuUHohvHFZ4WK8mL1aH2NmWoioSSl8c9HStl+E1TpauKFmngM9FVrhlHhLSahkMh1vFjCyscKYqa2QR"
    "BR9lbJybdS8a63QozRGE6856HlGAgVaGJf9npSMvU7Dqu5aSbw5w1M7XSkcQCjEdJBmZ8EissSzJzno4Lm7Wqw5T8VoQEFmv0jeL1VB6lsjx6gMv+2m4"
    "zx/qso6v9ZCgaUsW8NnCbpa5UfWWW79VyIGC79/qAaWDMV/NVM1+VfgljjJZhGd/6Zgn/O/XalRRn8eeaYn5Bt/3XQ/IK1qc1zTSBwHsNexeI+S8VigD"
    "2marZQ2rysI8O0ti+ao4afGDCdFZ5ycKaXTu+ZMJscNTFe0Uko+xxSd/jqYnDjU7K7P4Qr4lFzyJ2Dgk3cSiSpIymxN7yYbBskbpE7RvDBZs6on5Xr6Z"
    "JgySB+s/vSrOuL6GCy8faywnNXNAz2HZqZmDNzvLU80cZNbJ6lmHhXRbOyevwFZXWazxdW5xZi9ZYMcrrz3YzSJjUXcrRrmyyZljPiprcd0cJ0+l28k6"
    "t8WjYl+vCj61sijYq2bbrCweNlN+3KUaYy/ZU1WLbOawH9UsWzmNU6XNcsoOi6K9asn4eNY8pgyyC+C1kmQYjBfBuxXjuT6VNdti2BeL1rWWi2JFWbj5"
    "gn6vehzNXfjoojbNymJ0sc1WFq17YVHcbicUNfC+Y0h1Hl+q5OzMiM5OPAbCfBXTUYW+dy9UyW/mJ6Li38yeRWXA5wj1tz/64R9++btf/PAT1Bz8u1/+"
    "+oef/PCnf/43P/6vz//9kZUb/KO/+uu//JO/+OFHP/zq759/++mPf/qXP/2rHxv24/qg//y7f/n7f/35L377y+cnfvjFb3/xzz//xa9/8ZvnH/73P/7m"
    "lw/0Nz/827/96D9UzxDUQjIVVxIamXXYkd8wAnPmVomo+AHdoBNr4gzSTdRzlwJz3ltpsigPvIJOpKwy0k+l+uqZB3EqYzw9HfzAzJnfblSaOpWsXmBc"
    "uaeyplC7wRw+lVyJhtPWIUauREM8owdmqx6YxqUyaaaBskaIwbV2I88AmFme7UYhtPPsuy6MGxDY9aYEHf9U+qcawvfCrp9T2i3Z5OuypYGsQgzeZ0JF"
    "EI3qdkJHAuOryU1tzZ3P7URlm4NN689NaZfTGBMGxuPbQdKTjdQJT+tpTEEBJoZpY2JXO1GB7DybtgxiGgLQo/0bTfbPaeS7t6x8dzpr/7UTDqoDCvYi"
    "Jo7ts5WLty84jMBsIq3SCiGGtlvGIU/3amgNiY/6NbIVgXEAuku5tiM3+CDss4hpZ6jIX0OYegdmfghgWrX9qiGT/oADU09QEVbduG9wv/CzKhwKTMM+"
    "eExrO7jZeM6nG3HYGb+3NSY8leK7dxObIzA7y2A41RareKEhvtG1EVPRYljMyga2Voze4czWG2N8he0eWD1aKTemp29iMT9dKzSSmjDbLi/ODG5zJ98K"
    "WDS5UF6c3PPdsypa8uiwGBv3T+yB40vghNmA5e7jjq2X20K7Ud1vTOqyXXsDc3l0bu7G4WcvCAGt7Eb2KzCR1s0vQAEyT+zu2yho+gysVwqk2lMyCLst"
    "MMm36H9JMUh75VSSwCEue2IUqztWXmVmObCbYvBQSq/Eeqc0DzHIqgHQBJIBVSzwErVZIKWdLF+CCgRp7glXsCdPaIIrTdV7YI0KraRicX5tiWolUEBU"
    "mlGIEJjnar0UaRVfN8ueQfE5CTFzDIE597FEKA1KczHRQE0pR7rwhmQs5MH0LNQGXe3cx1rz5+jJNGz9xy2R//LH/+1//o+f//fx71kjf/fL//Uv/2Dm"
    "yM/K3/5BFonYBW3nXA3piR3usTNY6Mgwzt8sVLM7wmpnst4KMO266TxVQFJtlq1lWNCszpS6MyYQMRImW8YKzqTXEBgZX2cy2AgsvkEx8UCyeSbdQG1H"
    "5ZujGgqGrcCOxH0hxGiMfYGrC3UFCclyUwlBYBL2IE3p1a4vkKhonSVEo8/GhMO+jhoXdKKzYio6nb9nx0ykZt81h0SCA3wqDbHW9HaysXVVELPMgdHr"
    "dx5lWKUAA7nSf1ome2mUIkXvqL6YYfo1FrkEJsN1M6HcvuoQKGv6hOQ1qs1p1E8PTCPCA+wxbaZR4qAfqSvw1IUNGk87iMUHVcIcqyHqD2v1tiyOccRl"
    "bMGOP1b6j5Cs6kO3eUO9DD1HBycwfhXcUBviKLh7lIDbEARgx5jhCkjtUNZZQziCH4A53IhpSVwWl20raKUHFvcgphkD13gRk3V2XUJ+ga4nEdirPpy3"
    "yIhZYcfeIptwRUm4W8hyAaZXB617EACFMZbdMsH1KuqPcYrnGEG2sTvENrfYChP9FuacA4vnyHzGlHHf3coiIsAo7m6lGwsYWWzAXNljVei5pq0ddtet"
    "Xcui6tBzqwyqHXGiW2V47Sh3B+wK02NLVmtUQL+qm2U/N4ixcJR9tgVGMzNO4rfS1wyMVtZtRdsx/Mq3xd4r+VzNYeZh/4rCg+mgyX9b1yoItzww30BL"
    "0bjb6CrDwjh6dfJMtiIgcsOUW1EG4sLi888G0+eCV+OfDTVw29Hmi3juRe0sX5ChzID57Caz9qLw7yJG0/jCvPW2ROWP25v2WjhyLgp02DDPOEpfsL6F"
    "CWLeNCDaY7drMc+gN14Uo+p6latgsAIHMAZi7qCxZE3h7+maAmDxbtewVMqkq8JTgKZ+jnx6jFQJ6AqiiXatNCExDd5gTioGnrbSRTVFTcZWS7QlUc2S"
    "vwdrg5AGYEbHIsh2wUjhsqiBHEk4LbxJroKtHjZkDtoVK2qRXRBIJPaoWS7KgbevohDY1nPaGLBJNlsneQE2qzq2Atp6TIsbgcfJMVk9sKNxou1yUft8"
    "a9wD0hxqC6yac62ZWIwJAqNmBXa0FLVkl9YJrKnErHFzfxI5vhIjNHeXW/dtzniKCRZtSsFfUMz95yNv4i5pX8QyhS2qixklty7UhGMRAb6iGgCr6tah"
    "JTAirnkhqxox2lV3k6TbhvTv3eRBA+JS36yP1FBDjV3dTJoHpqnZDCG0EU4eYD6FIyr63O0F2lumPlwV2wUWj7FqVBuROXK37PQsVgTMV5N5Ioh5pcQ2"
    "ImJ0D2uUAmsB+UkgiXMXngPHotz5PbylBBi9LcBcp/SUTkezDbcLocFjsFXWC4yvRgT3Hhaybz2C3Y/ZS1UGf0VAPpw93PEXbjZrXVco/h6vUdt6HBeu"
    "8mtab9kvHaB7kwsFmLtpepztrrhvrUdUBZjr46wBf41gbljqwMvqpq1FOX5gvmRbDsAl0bq14PYC873eIo8LGH9v5HdZhaGBoBCQL4qsVADMtyx4ETMx"
    "23lZjtMw/znV1LxKimpZst0w+wTiG2oxaZKtxiUd9zIo12qEkoH56aVGnjIwn8caIU1gbm/WOJfeKwFSg8IFzKFgel1VZWpm7BFj+KGVkz+3qFJhPAoj"
    "VxhYdO1QL5SwroH5SJU0h+FR8eeGnGbAfKhg8KLJvTz/o/+qeOEVh1xtFZIngXl0rBWeSxyahEo+5bZC4Q51zDpWL+ubAmOyaL0MtjlmgrbenV/laqwq"
    "ZknMf492Pn9vGzZs5fGzxyBaX46dTax8bXG97d2LZRCdTQ4Nf7O8HzNVWQ+3GYfJse2LLIeuWombhKphM/tVXc7Ww/Q0ftbfZWYwW2f9P6QcvMcYWTMn"
    "xsQh6iOHzFaom8ETYKw/XDcZfI4dx7aLN2C8KaBulgMHRgdm3TObwjND1dkc2HI9WHFwJuR1QKs8DoAOB2C3XCikk1TdIuPY6cQ0P5VJ9BX+CD4HD5i1"
    "eLG0ITAtFBx+a2DmOaiLdBdgJO1WqHV9Y/gxAlg9gZnTpS4v6AzIa0/WlcuzstADsPjqUktGttjTSusiRckhn23YsiMwn8bVYpfVpU6QSEfMm1Ji8CqT"
    "Jeu8n4RMCAIqJ1vnGL3a7IV9AhVHE+O7TBvyMTGTvML+ynGa/i7LyDrmmwAuuR3jbnqgTjoFHTPrqE4mZTtmdIWK/KaAzIlRYcLn1PpSEQ2e0+0YuWtf"
    "sOlRT75rnxjUcPyGjR7SlmouFRuCQY4pu2HLEQyClkPg7aN/hmvFvovISs64L3kVaXTM9F7tdCYDY43X2leujMPV0ld+l2WYq26oe7BGI6wq89cxO3LW"
    "PkL+NlphwIqe400YtdOfDoz6tnZe5uCYN6+GdMQJ+xLTDm/u3au9hCSEmTGJaYM3smdruzGTTfugnVhUjcm2VRksjvkmBVtxBOYSs+XCbTwi1Tbz93iF"
    "REVItAVmxzVgmrXOujpVRdGBVffPV92x45jvybZjT3ZJ/nZCQ4C/cNnfcwMrGpejNl+uPrAbdrRvX87Gqx8uvHqPVaUS4JjdFkM6tQhui+kwGw6LZd7A"
    "7ACAhaYhaF6Kw9bjjjUwY92eWD8+G6qV7+vscBuUXI2b0Py+au1Ot1jdk1CIzEMZMuhScswXrfLGfQPxueaWmWM+tcM93A5VQSel7V2UDTP37aEI6TMF"
    "sIuVFXr0jd3c3qdSJGkB4BODoiuENys5QsSFJKTHFJJw9MB8AyG/JiAfz9k01xgTyd/QSiyUADldcoh92U16EyhUGmX8DcjlkS4y8xlz+21uPYao4pK2"
    "CcgVCxJ4883QZz1f3dKFawTmC3b13//qYoKmty4UdUwF6x+aQr8xAN68dVI7bOnbG8ZfZR5sVckan7ImI2StkPC+A3CgD0VAa6h9Uof4etrkQjhWL02k"
    "WJ6sFFIVMnEzx6dsk5fh5pAvHhhmKzDXNXuF8XvTptOAgsRD06+nXSbopvnGPpzoamFuCazL/rL8tqzQgLqgswIrsl9XGpd70s6VXi0MylUr2xwYf+91"
    "qKHzDFiY5jNt7pPvyjSXaiy8Gg4W/Hp9otPSz8eGP8aqCWydDgnSFYXlkHGYyMeOjhyvx3wB3J4/t6hU7/jkOMXZZ+UQ5xnp9ZzOUr83xsq+ZlMWz2sl"
    "x2npqBdnOLmKS4tVwaNu6bHCytBRcnzydHF5ME2k8/ga77FcAI65LY9qPKqeT/16QAJ046TKA3L6oe2+Lx3Cb2DuOqvhX77M9gZ0EuORXrcT4AjuR+ua"
    "bkLcYyMPwUmsX3oS5Di6tEVajVSCq1RKeCbkTryUJa2+/DArvRo9ITk/FDu4K30kLZ8LX8oba/S5tPyEe45xZV8LbMmtk84K94e0Vy/IlTQvUTo6PFhk"
    "5lZgzsLLKnrAWpPHaobfxJvSM+KjykbwgO3012w6yla6a6qcbDNdQu7G7CN9LjVddi2dYvxEZAvBoeZLqgddGM44j8D2SG0B1ulQfLn2Gl2R8szADTDo"
    "siwjMP/qKOGeZIKXeUBHuCKPnKfxc6xyCB+rHELHLyMBpOGEA3TSPUtqPRyl9ADHpUpXCZzA5P462mVjpTNWFDxcDpWe3UNIrl14gOmyDgfwpuNspCsS"
    "CZTygIcfm8IJ3nON0+almsA0KFuLYtb0nne6J+NSrrvJKwek0NsW62m2WBSbZx5gCpRsEd9wLA2fvYuPvDIMvn0XAjPd4irfgsiDpmexYgiwmVhjzELh"
    "16XNPTP4uEgjm0E4BNQUFNEOWNp4MwoHX6uCoyBbYj52KwrJXN052FbcwmeREYV7Aut07SJ6NCP0chV5WhmzUbh0ZGynDdEGIlLk/s8VRUgRZGJ86kQ4"
    "Ymo8V8ZKEO9SHF1hoUnFa7H1GjE1BrJuxtTkAl4342esEgss4mcsMGtB5BWBwYjzK3g9RGHNnBsEGo8Cy9oYMPU1AjfjlosjdX8vvBnXFFkYVJiGYPDO"
    "CgsN3oiqKtKoUN6Qy3/FNfQI0iriJwe1MoKAidTQeW0elsCJkC/nrEcsq28FS2Or6E5qQBFBnux+EJMAVYUZpRhA89Rzctp3SbIVBZstvq1Ye7wbQWXl"
    "3SM0PjRKERovCpau/DnFrVcK/CZC0IorzRG639/muokjlbUsLeofpISZ7ADxPDTsLThMUeIEmCgdctk32VS7BU+hf0TWktpuooNlOC7IEZmGBWLFJr1Y"
    "S71Kju/IAgVPY5CsLGlXt5hfcRmksUNEak5iyRYUX1BzV0R7VI6k2YWfwWfx2d8Z21aigPGha3BmiKXcLSeJZDsoOEHVm0nVmSJrlaT07GASjqADHRGz"
    "SmJFcxN0IAVfdwatYCCLvqNhL1WUw0jfBlspuCt3BKvpxtK5gdX5VbSBENUlFsXsv6Jcp2g7YQi+3/WMHkCiYc0UlDfpWuqEKLOqFmqknGR6FRF6lHZg"
    "SQ5axMEbG2JwioV4i5iJoXmP6nbanPXACqdW7HKVIwS2g/vmOmbH9cnnLDETZ1DkpohFyV6W+bSjICXIelyKyfw+yjvZSecNU2nv7EPRmojLVUEvdP7R"
    "jlvEQU28yjlQX7d4K/skhXGKH3WS6jhETT1JYYw2h3gC59JF0Y6rAMHN7GqziqJvEb23aBUnWAqvxIalE9OOMnln8cYew3pgVe8GrXVpgnZwIhdP1W3L"
    "MDhrZOvEB1/91eIT9Nd4VRkBsDOEaR3DoaQECDUFV0Jo5MUlx5UQMVI9yL5bXRNlc/I0D0yzoRpu1o0VJOMd3R3BRd4SoZqNqeyEvAzkWO0c5Y+MwIoW"
    "rvjOg2Ryw3pypUdifyj7u/0nsb97gbsOa7NC7tNrUXlTuGF0INXlUZMKXbArMT9BGkb/HrBrz5VLT4OF5JZBrHkMzBN2DCsrMPiyKnRGF+b0xQqdsUZg"
    "fG7KJW9hxE2sBgQtU6EyWj52rWely0lrkUp/NdxAwLa/W+VXrtvzVytUxgrIHoN2WHrVDMBqbFmOyfajcT13yzMI7DrGu66ADR93YBrP7Su9mnrgAGwv"
    "U1ahHuL3dmIMisInCJ1aoR/iOc8xN4yRKTgA2Y0mLx0cgKcR4wDg5DoJ0REK/99ZxJp+buRzDFaZr68bVhl5rrzzxSCOJ9J5KqGuhhjr2CD6geHqG/4B"
    "3kD5YODkCJvCKnSWQYw/AFr2Ueg4tvdagN4gBgwqaTAVOi4e4045J0Kx9XaOpu57BzZM7NaTPIN63Xo0TDN7B2cMuX0tMF8V4EnpOQvM1XO63K+VlxhU"
    "aEMtWeRIGpQrlrWmK5ThCmjZm/sqcGr8DYPOG7r25t4KNVW3WOqR6HPIn5pijwCa1g7R+h3zyd9d9AQ4RG2QthyZRjfxptWcLm5/qEatarhNDdNV6sC0"
    "qiEvvHFwpfpUr62WwJXq37CqPcQaF11GJOBM9bW5poI+xt8ZxHolRml3Vvi34VC9ixjFHTylhRADgfCUlk6MU92qBxYNY9fgFg2MQVi4RflupwcWLtBC"
    "RB1jMMOwqce8FK9hoxHj/K+udQinKMcpJEIju9wwRojNKUoofi361STZgfmvVclE+Ek7IfW0FYqcVSTrzXW6iTEOBswndl6JMKOw2eTMo+UPrNvIzR0T"
    "gaCnPxfBMaPEWcfmFEMJrth6iMV3O8XOHNrEwEwXHV1WAWyoLU2cGmCmZI6V3Qls+++V/L3J74KVOgLzyRgnMU/Nr8jeit9blLtjKY7YmiejPNhUaA0+"
    "YBdkY4g40DzHsiJ7dfITyMR0rEmOwQVcDjH9XHfnZUVGq6aNFUwN057qw1U+Mlq3sMnPllg/3S1Uw6owp75WJL5S4MPf2wkt/ZqXsjZscOBRokUYrYDm"
    "5SQM0hdG4zrrR7FVOHJbJ6YGDy/MZJjWGdxFl1hfgV1h8Q3PUKmnRzCokQ5v2BR2KEJ1Eygw93xWS9/lZNAYNWwE5MgU683o0sL0lBfEqkjopXYD5hI0"
    "OAjwu3aHekit2akYestXvWp19cxvYtPFUa8hK+ek/OhF2qKRSF8t4fwG5s+1I8sIntfi2A55NCWP2o4hnofCB/tjBjZtW7SIwcJD6xZZG6JGAbNewK3j"
    "yPKcuorkXdpPRqC34Ww1JnFVvhkETM+CMKzEHK7ONVavqGHG+LdP4M4nNnhx7FQnxCFbTXVHc9fyqa6sJAtI5lNdMp/MS+pYGMvmhiDEFbE906cicVcL"
    "Z1duxDqiudtpe9WSeU9g5xDTvG53FxpWhA19o0Un9tTvVdFczBfViUm870XxWYv4K3Z8O8TiGxJ38E4Rci9FRTavdhgsHXu17I9+zU9xBpWAtg0Aorgc"
    "ulM4hyUX0+GmKyP6fypVjy6rd+zaVJcmHhsS7v2xKuoYcusrIc3+6ZxXlR0E5oVqq93asQKD36raNRvC/ILaald/qSVeb8SwkpidAewaKb3rKfXVrowS"
    "dnzG/MKtwLa3pccaA5f+ENMG4E2A1S/aIVbzu7LSeA2ntY+R78a7FQ27O75xO/srBc+7NGxcYjZ0DipFq+IcCgAM84nuTmGyDc7KSYshXdSfJQghGOat"
    "RaDunskNVNKGOENTOcVnBeY6H2fcFVPuG6jsz8yFUbmQY+k1qgqVd+Q6W9oXN9fjICb1dgrPH1VHMisxwR26eu4L7Xh1Fu6uS8mgzm5Z7yoC6Tv0SPao"
    "Y0gZbpJRKQQktm7Iiip5N0KkVMlAdWHz5FZPPuY5z4ZJLu5CDVBvykVK+3pTjB8KslbCLmJtS8Okd3kRhMl7Hskth7VKLZwU2p3qY6Rsd0umpb24BocO"
    "xmQNzHV7G9lkLxVvikz23Wq0M1qQaUz3bCpBCZ+lRdF26p4qHXU0FavosSCmA/PHesrZeflcjxO4pSoO6nyZS/O43upBFLMssv7dqqDnB8bHqKnyL+2W"
    "dsI0GDR4ag+rYi1iWha4EE6GluTCHLQ0+hGD3zLOwhA8aRuFqVnDhJKVSneYJ5cRC1vuysCtaWpK+4w8+oydBrNE2XCOkRnWZPWbXdmJSWFanhcxGUyD"
    "Rz8r7BbmbKE5r1WGEnwy8SUqhs6bQzknsKGrDgJpabNfPcR23zyYjx4GWZeSHiP60GX0jaDt4iDgggdF0vLAcHlMaXmE0MmFbgkcNYZOODpZdfngdEuQ"
    "YzxFBbUcx5mlE9PeecThwUryA4Zo5wFMr8bh6IZIsTtleXbbiflG0QXDjlWdBUeeydyRAAP72zFtjtB4ze86tiNotGRzSczXEW/pGLk/CQ2dhhNy7THz"
    "0NPmR2frugNqPJZHO7zctB3oNa1Nbr+Vi6lJFK3g/9mxXE6OG6f3Qi/KnOEeuIMeGE1rPdzDYjC4B+IQkiyuizba2jEgdXJ9qT6C+z1cTCCQ3MM/svTu"
    "DseKz/5Ka8luraVvqYSfZsndJDFZ5OOIDAd4fcIrJaFbNPm6qIgeo0lMXy30tmV+DJxNrjuWXOvwSblKWDd8MqVzae4S81A6j607vKPwe/m87rQ0WafB"
    "MGnsov6Hq84YiYsOPamEUqjYd4/9BRecnIHx2UIFjfjyCKzJtyjNWwq9KIh8zXDzufcKRv395vrbsWGBLTk+OT/AJv2jtQfkB9zT3o81uVvrDsxX8Ynd"
    "CS/kkfN2BzTl5JWrHg5M+odHDT/nlm953PSGygc902s6jzza+6urFiTW/s1lfFs6Vzs3lF35HS5tPtcjCmMV2hk0iDGOYMCIAMa51M93ZIDgKOCQI3A2"
    "98Wdnxle/oB2BgP8+AU3cwYNGKsI3V6tcB2x3jMIsYjJDX2co+qxlBqYQi7lRpjDV+3NyUDxua3QzM6wSWUIpyZWFNXJiIvb1DckKiIzW9jagdXLuFE7"
    "EdVZwu4IrHXGnNaKiJC5RBGbGhklGpUxLA38pnVjFVQy6rQUJisnI1GH4bQyImDFtujka4T4SehmrCuieIq67ZLBvp1YU6BQ62f5nTwWUBzrWxSvtnD3"
    "L0+OMOxmVJC/12NYoBOsLXXETltWXdSgZ7f8/0Zc5/9Dva36B0VcmzYnLhWUtAc2hVEA4v7lTUxH1Ev3sF002ALbjs1wcFyaYrhUUL6Gu/TdyCFDVTgz"
    "z3DRYJy0j5uiuFVwJLb8uRpGFu8cr7hVUPb+pcsEtwpyZ6N8nJ/Id6Q1dimLLZYEsMoT/o7t2Zl3XO2qwcRMfuKqwaNvMDYHjB4NYLY4947sMNSUG/5c"
    "/8yAfFh2OPmszJxBNXvhdVsNq8J8yeGiwR6I92GFV8Zq0VkfRKgE5tSMuteWVATmc7aW5sxq1hk0tVS6DAhcFnjULatvUHEH4LkBdX+1vbHlLalvzLxo"
    "uLTvaHbobMYNffEJqgDcxiesFq4A0DYSM3mPm/f4ierHJ1y8R1kH6BDiUuy10dmEuw+E0eWBe/eon4Adf64phN+rtsqMU1ZnWcKKm/fUELepgPC4B8gs"
    "CtzFpxfpycBVfEcfOFw34+SrtBRwFd+cgV1/N7yy3cl+BlH8d95lVnE7n9r7mMqCNCRwO9t8jQgR9kanvF3YdwLzJTwiWtd51Zph8Vkt9REHlG5OccOK"
    "DnfAfBf3m7/HA+rOszIw33X9SAwD86no4aruzA+tqMq8AvLN2SPA2punX1QUed4rsOpYJP0Bs9gXikZrV+iwtHv47nrb7Fovb8xXWQu/DzAzolHSWgKF"
    "l9zVrZuFHXNB21Zs2kaNhVLaS0PgDN2624iF0fx+lWrX3a3AfOu1sNx6cyvVCn1z7fXCTQC3VAvMpRE8Wny1V5cV9Wgld22pmlIGaaf2azXSHjtCPoQ0"
    "jeAFOzZlLfa+OD9Vh/TeeXJBiXRNY/cCPIbpMS9JU1FdPX7tUlDUrgNTH15/p27L+SbmfFTD1FWWpq87wwadXhBAtJT66Nw/6fXsrMNvmMSHAnioLy8Z"
    "OOhXiprzwBa1UTmy7vrQei8n9u3Q4oZIF7YpK0vYrcB8gZbwhwMzUwkV9qPNm1oF1t13KBS3YQbpnGY/ZrOIEhn5AV8AOIiNr41bKv/qmB16VpYGQcfM"
    "Q4qLCGYPzAx3XFjwwqb/ns4BgGzc141oErDuWORCA7ONjHvoXuPuLamyxw3yx8p72O3AhGscYvUY47+uTCK0AbCvnleDPT2o4vKIWD1+92XFJRPRYk+3"
    "rbiMQrM4eazwy9SI+eXLhtHO7l6WrOK6C83FZOgM12JoAUxSitaJyGGfXk634poNdQPhVEJVX/Aq4BU3dNB/36fzbFZWFekKkuJyjxXQmYRko83L/ifh"
    "py8e3oExpNHB4PCfiygRsOOfHWFpwC09iLFxy/csLi2R9Fh+4YthsuQWvU248ERDtxiIx8UoKzFfFLsoiglsDmIaJzjcrRfrxv5cfiFNtRuzZr5r07N2"
    "jsDwYV/hW+8ky9a1oogMsOY/FwY4sOLv9lifli1tWDhv+/LKdHWp5iCHxYZgvbrWufBmGtvLSyxW3LWT427SCFfySOUtLwdV10xbc/EciCt+1gvz51KV"
    "La/RUXEhVX99wyAltVvj/Ks1VwqDWric6JxvA4WLj3OgvMVD4dm+KI5xw4Oe4iFwqZQasO2SYgRZsi96YO3KIXX/+robI9t2uQPs1g/HtltudmMKf217"
    "Lo9hMqtsVRpWY/539203gt7UN133dpHQCMycLXbhDvu1ydrDxTyST9tLn9WV9JTO9D3DGA/se+vdLTpB34dLogdPApiZI3aR1grs+jdSG+3LJdbDh9Dl"
    "MsFlXRpkYxMaFiVkDPN3m1wrhnn7IuDd9+UO7TXH4HIn9xSC24seV1xOJtso2txOaHMF91fbCjkA899rESTIcWkRneybvjnc2SaLaW/KrZbGy96UeS1l"
    "/ibLEVfPvTAfZxwCWmB2MMH1divn0iwLXIM3E3MxXfM8DMygqP1kkHWt5tF3+6UvFbf0ncR8K9cWOmRL79c8EGxaubgdMFeQ2SS4RDBW5OWKLME16Mcz"
    "uCruJJTBfXjSt3sK+Qlea1pxn+HQc42rpeRR93SujBIuxg5l7L8X3OeOdBJC2myiOOC6RfX2yKIp4doF5vI34/tdnk27vVFNuRqCPGGCVjyIaWPdQkOi"
    "hKO9XzfMVwkKY7+MMuJySa1bVu2ruIRSx5DrZJCZnkhAZtTj+sqRGF9dsUQvlWZch+nYFabJuBRLuF5TEg2YQQoLdjmt7ALPm1+YhkU9KGDbW1fCYYNS"
    "ChhPu190fesFBvsEZvENu9c0v2GGFO5EDcwLDVbcnRq/50WiKu5dXTnIZv7PE7UcDDOohdwLKKL5BnlLomabfdXGbkfxEWuxY6laYy72igV6/VKvints"
    "ZZjJb4/7bgPzbOGKe3Elfu7iSO105FxGX+duOY8k5sxdw66/Hn6fls5AiH4cYFxSo5Afget9pzAymHAN8BVG3iAwan5g3g1EzCox6nm7VVgYCbBzhSdv"
    "2BWnhk2dRQfrdBhGrTYKxRnuN94BnU2IszHkQMPVyD2x46+2/Ozh5ltB4QNmlBZg5Qa2vbtFR5HBq5UqbngeeteTdCtugk7Izux2YXRLzEZe1yV+eU7l"
    "e+zXbFDmyIGnp2DOcN0CO451HTGsxTYCM7jXo3gloTqTeTwK1f+c5f2uqXW7lTy/YeY+bjS/+a6PclhiL2hmz/yS1IqL1Hdi07GuTWpNNqhR21hnbfWM"
    "mqvML7ypc0QMZcgjievg+WOs2V5xazwlNzAfp74Tq5RIfSn2MHihVcVl9WR5DPgfHYv4JbDr7/ZYPZWpAcCqnvPg+kTtL32W1sDsNYazbg5xV12iwZLt"
    "D1SkCkfVqujyNY96KeBRv4MNbl40wzDaTcNcSYZFRtJofhYFVHZAyx8LhtBo5FzNlku2de+XbqYFNDhMLU7PwKb/XOzZNtTgrvPKaJMipanOFyBfTa3J"
    "6QvMJVSLjLRB9sK0QlYBmQk265XpB8w1Vw3+52g0rWaN9BZgrmnqemPNsRnz32i+zTrev2dHkVl7fnf5gXIm3RWYSyM4qfTc9lPhrCW7xtDiLHFAHY0J"
    "XrNEistoZKfNsmMdy9M4EZ3QNy51g65odMznu+g4PszYNkh6H5Cv7BIl7EYno3yWOHqPLtVQwtcK7BDSIus83Y9746PD3xz35Bfs9sQHCufr6H4RumES"
    "WZ2clgHO6g3MlP64wS8ZnYphPDpXOqrTcQtMYrFz6Mbt0ToK7XGbLOQhz+UAd5UdGwyFDBiAN7A1iVVhHpYeJ/y2gKZjYfsDuwaF43bgwGm/diJhEJg5"
    "KIZukXfMNCMwaTIU0bMxBtU0se7f6CFSrZqmYU0BB2Dmyhmn6hgyxEIbJ/ceMiPs97YiKYDMHzXsrpfAzKYfOKqOwMyFOHBcSszsirGjBuQYdEqPPfL3"
    "pr4RlXmB2dIeu2XzKAbGrrK4h3yNA4nXNTDbZiNINmPwsDfWycc8zf/BgqE6Bj0NQ2VDHDNzZqwIzo5BivJY4ZEAZtblWF2m2uBt3A/WdOgfKCTYiNHy"
    "G6yc8mA1TCalc4wVdviYdvNtHTO8L2PSMAVWV2C+M3BdM5f3dFk7YM6odX7VpmFVX9jckPjHHpjZ0vYb+sTRu+FWQAt8Tc1gvAKb/t1wEI7FQ+bQJdaO"
    "zUZMcnCRm4Ah0yJgCZxqQ7sD83fhlJqBmeUHrARkZF6bZa69RbYUVoPsXN6WUEeG+4D5OsNizXe7vxtelCHiru3NxHwIRgtVIE8dxMTrG8ebXHIIurNC"
    "TIrtwMxEgrDTtC2/FKlCKEq2LidkQu7GKA/XfCNrkg67dsMwZSIOuxPDoCb3JXZE8a/WEFSLUUFgeswjGKaI9NRhe1uIlUU6FlSd5O+6bEeLfHLsalsA"
    "LTgVEBw+iy3X+yb9GphGfbP3LRifY5OPisZJ0Gy6tEe6riBftjDJ7l25ZnvKVcicxpEr2QlBKztmh2IMul5dXlfWJkedxZFsEjsxmtdfXXGsW5s6qe+w"
    "NpbUI0oLBeSirN/Q3YuxPmASR4tZI1h1J5/zT4z6yal2oT+a3JImJCcXuw4IiwEM0wi5dNrm5nk953Mx1vv3fFWE0xgr8SzuWZnqS7phXHkggfVBUVFy"
    "YfvgzRarkyYtpJFM30XiFaSWFtSibwPSreY29oFCxttKUSFpeXuImSFBO0OQLcljacLJzBf80XZgLnlmRO1N0E6pgZsCuUld7MAKtUqZId+lfHYPLUCl"
    "Fz5y0xaLykxbYI5UcKEu+ksRBkS9mpbqJCnVVlvqMhezKw/T031qY51PakZfEytMy1loC0IS1MBc7u6SSpU0+LFjxY6rV8NbCmwcmhovXe4aZY80NSSf"
    "shq/rcBOE0e+iUE6zrCbXQJzFQBi1Ays07BqL1Oj0QCTtB+ba+LUN7Y7DbqW5gztzR4HCSiwRQNR62n4rZZmSMq6Hn4nqBmhPS0mlzwnytGbtbVp074w"
    "t65PHmrCorsp8RGnGTSvW1qDfK69Ddiw1tNG9k17h2TqkJ69QZeCYIozghYUDHOdJcIGLXnm6Gn8H55W6uuMoBOMtEU/edDR+uk7zkMyjvrWsSlC25DW"
    "7ooqNX+OkmymmxqYOxVLxOGgJNyBCFf4CIyHv4jFjt55Oi9BQDI91Hlw1O7utD5wwNS4d3LygEnO9ErHU4konh0TJw+x8vZ0vxHHDruyLbsX+bNDcc9j"
    "p/t2aq5bpA3rkC3x26lEZ406zMA6z+zldbAlFC0mq2bqZhrH3BVeI8fQLQC6D/Ru8zUAz0PJE/ZadFCUfNXPya3FWmkMm8Df0eLA7o7lFg54YIsOFSl9"
    "ZJJMOl7GyydQ5bMZ4WNw/1SGxMyPcekW6i+XSqdHScZrG3KpVe2f5jcoGCQ9gNy1Qd/WCO+RT2zvMerw1VRiOoOw6rh51MJTJk8EeF89fGDuKekR+hnV"
    "q/wZpmN89dK+5snT2acuOot66tU66S9Gnn0NjH62NOkrc5Nm5vwDc39xv+G1qZ2+4axSAIxu0JffrtNvN2psApCbKn2eI72PS65RCWXehGwu1JrP0SMb"
    "NEHzXMr9ett3bCl2be/SmSuzuTJNfY4TkrAypxSOYLl3aqNHfwapG5iHV2bUfbCuLTqgX5iv7xkEbhuWSYf2y9dKT/jOp9JjPr49tsN844Uj5pMvOXYe"
    "m1ol11nzTbXqJ0fT/cVZvwS+YfchLlGEAUX8QbrBymAxTiGrTOVb5opcZnip3ZW3UjsWv+/Q4iiS0oXKYZ3wqrtNNleKz8JUghmM41HkLYU9syLW4htg"
    "13BbFgXmdmrQ0hjMyGr3g7c6WQiqf48F4Vg0I2a0FL5STPhKVqJicGIMVSU5xtLTGSLrGapyTbhDHiPMtRldE2HiyjO6k3IKj+BWZG5H1My9/g8m7sZd"
    "igeWjOHS3YPo3+9ByTa6zOuY6SzrLOVtIceWwTp3Np/I2bPmHYYwa8bvOiOdJTvbDyOiZQXmW/HcN7YZYH296kv2vgLRtAbnbREUvyfCugqnA1L0t+fP"
    "MdY7g0CBr15GmFc+NxWJPtlZ96LfiCJhUOZlAFzMbhWYstj5DKwqFl8yEu1kPVurGTu+32L7CJ5XcgBElb6VzMQyMgJeSNIosW0R23cSSUki0bkkh5Sg"
    "LKPsVxWToQZ9wBl3IOrXoB44B6ck5e5MNSWZeajW0MiqCJqBWG0lZG8/LDsEQoZIH6clSUO0aCSxLZI5xBfh7Y1G+lDQ+oivB3l4gqXhnK4atwgAc6ZF"
    "DQ85MEEKKIP0scg/mS8iCGkqr18rjWyWmq/WStaLWJJK0lqZv99Z9twYM6/POkmjxcnWuCaLDJwVnXWaSms531WknORin0oeSBs5eM072yIgCMjOTuAR"
    "Rc88zLHaTkgsvBaBcmC9kb408rlJltNMyHmIvWa/ejKpzuvVQxZWSaxvsrXaqylNTK9cPcESE1vr0L8JNpkIFMcreToTLVeKs79GSebYJbVo1BAs+7g/"
    "EkS5koQrIlp3e5P3NKIaoXHdLjFt+T3JwRojSEnDWTUjfGAg3W1h2o0oazvIEqwrMN8BcB8Fr8838ohsU9D/VtAQa9IEL+mKQUW9HKZxQs4skYdHUCqM"
    "iWiMyBIkSXrjAAU1k5kMK7PIgTl1cEZIFPRHp9jOyMEFtgmdQHzpzBE6dK0keuaP7Uk+aE9+pW+JmSx2Xrhr9NKWjXNenjmgkod5SFet+ZyrgZVaalGt"
    "gP6an7iHLFmJWYzcJps2XmUVs7VmTOwSUS09Sn2dJPH2nJzg+uYnghMcTNdDinXk+ANqoh2f7KwL8h3VFvraSXau59uM7ZmDxxAmCNUyItakpHiRsdeg"
    "zttJreNlysbt1vZcUgzpLOpGIyYmPQ2ayyDLXAS0xRgmsJsk8E7S+kz6+Ojits9gmZN635IXT5tpmTQM0ro35URJQmA+BCcTv+BBFPc+mOwMToKjLzLc"
    "bMnbl3U5G4cvfVTg4/s6O5mXNau+kflb0287sxSC1gPz7XJOcFZn4XScKwkyCyXIjfJmlhpwmbnQ53esJb+/sCmZr22faEyYKPmuEyIzD9uap1yLV/Pc"
    "yrkrROhk4TLkbryGoCrHI57zYtqWCxK/515ppIzEZ72WuGWblMx6iKQUWTTAOnNXWj43lPcyvn7V0mPy1cIsmp0Duphsc3JMvCBVuZkwwzQNS/w5mc6x"
    "v+cMbaZm1qQoj8WMrtrf+SzlW0rTmKxRVaOGHnKLPPGrzky3iXyrqL/W/Y4Iz7fakeU0CUXqCvsKF8eNnKkdCV0jcquYbnVe6VZM1EpubvfK7JYxprMZ"
    "TIJDTLvMLqdktpnmsCs/CizmSBkbm4lqOhAhBNiI3YCYbpdyoTNRq4Wno3dW5UTGXAmoCxIbXZUmLdmuRtbbUVKe6LC829GS92SSKTsOyXmZMDeZCqiN"
    "2JWY2TNFtPP0i9TCmr/myxXO0BfGTMWaDfEsup6pcNVV+e6pBCw/kfmRmfS3LtMoowv0nSHdcrySAzfTMmekEHpu4EirEjYnEz9fyYeN+aGy99p55ZZm"
    "zqNSUGfmWvo0jEyWaszHQpZrjyxSzzYeqktjCahEIiGTnn1k1kojNGVzj8y9swVETEZWI48cCb1aD03jC4kyIwPXDgHATmbveub7jBLKyPL1WnQZ4OuV"
    "FCtgOnvUnanKsqmr6ufNmenLKxKfTyQl+0K3IpeBMcl5x4qoTPhCtnUJqF5C2hDwQl4mamvwUKetMqF7tMBcfq3crZUpQEgQ1xI2qhoTyUtiTcnld0f6"
    "9l3MQZcuqdp0FnUNjL+3MpWaHAykvktw1qLfy8y9ytoxSKWP3yvcdvtLsrpvnh1SB6XnK1P633nuTPyPTHot9z3eCfe+pOCuylz9wxoEMuWLsj7ftQom"
    "c2HfNQ2m6hIkabzQyQ4s6hewNu6OSt0oX2DmMkouyCQvDNGgNINM7aI5O+IRdN5CbpCGvfCAg+oPcpqU8qocUQPLChMzqjpEJQrVSVMV7n2iKtI9LPSA"
    "/MssMOFa90S9cWDFSzQW1TG6rJlt0B9evaP9p1XvMCrHJKskiCZc5oizKICxaYUarzQZJE40iRC46rYg8iLXPVImDzGFNFQT1cIxeo5rEJhCJHuT1Ie8"
    "JHFZDnkBLW4pH8qbQoxG4Umc4g8xRcsPjVrEbcRNPDQkEbeRN/jQygOm8PYRLS2tkHEYb0Dc5ibmofGaLKpD4jViOXLMHwo2xG1E0D08Ao2aoaMjwmKN"
    "NEtgHo+uyUk6XmMS3n0F+w6TEYGVgJz0BOd+QB7bLef9ptNKyo6YE+5BsC8gWYHu9TO5fEpS5c9kAL2MIH3IYWi5FOosk8Tgo1dwReWV4KNXlICX8FTz"
    "0Y/AbFFZ/ocG4PgCghNYBKnDEtruGHbs0sJ2t3VgZjlbegrbhzynblhQkK7fk2uQQljXUyPh2lUI+HJ6LKWILb4khVqSjVoy3REId68CG5dcILh7FRG6"
    "foGPYfrq9vMKPMAalMsisOYBXoFtQuJfXCZBwgMs2imG0X7ubIWrENf3sTsRwjA6tDBahYjr2zCdSFIFZJLY0tsusabPdlnnwMwc65lrjvC/Tbf5ME9g"
    "278RJzaE//lcuOGBmbVv6Xz6BsvMWdLkCsz2lCVD6vdI1rLMwh6Yne/hsNvq7vbtAo8dZRxoAiYbum4Kc8x/rmdTrisjS7G9gW3/ucg6c+q8YXF5PTBf"
    "Uys4fGAYmJsCmCB38vYs2wfIBJI5cYSRuG7OMw5ypekKh825gfm6WDO+MPXqkI8TpAPv2IrUNCMiGBTloSfvDzes6DHm5MCF09VXUr+6bpl0zHgAcOFQ"
    "TIOwsIXxscZUGLh1KKXBVxiE6JafygSBp2f0wHyEM6HJsj0GsSZscuvNOLaBxGBHZXh6tEAbCYbm/VFTWFHOyiLo9+j563nnAjD2VpQEcB3My2fOH362"
    "sziZ+RYS8wU1I80LZAdz0sCToPnp2qMjDHAQIHxPjeDCAPMmj7CWjBVhXRsR8QTmE4ljVD7n+xvHLf0eSwH3rPgz+9C7Qag09oS3pcYC6jxbwJmgKepe"
    "OALOBEr92RmNM2eCMPIzrZ6LMGbQwnNwRmAWCIeXQLug0w8LN0EMCwPhwCQJB4M95ifg7w2eD3DaVzdGS6zpua53IwsDRAmfth5MeJAiXCr3nPLBHB4c"
    "n/XqTogWB0gRZsPZKVs/5w7RnszgqQIgwDRB8KxdYtovk3zPnuRjYL5uW1TVA0/CtVcLvy54Ei4JWhwuwJTwRdAi/jrn0jdyn8IR622OEsmgT/hIJZvI"
    "chUdC34NUhrNIgJWZ2AuMuxOzMAcinr3YGOYuYujuxbQZF4/juk0naZI/nZ0X4H5Wm5RwxSYhV5wdNe+Wowq4phOI8EYHzZUNa7P8AxOw9Yb8wUe5YwA"
    "uciouUYXSy1ZMTI9Rz43Dsdq8mKdIjvM3sBcvZao0DGX1nIJUjIw/0aJM7HRT2wmS5ydpxj4dtZUd8liAlb03aVvRC7FVFypl6ikZXm8m5jEklWuMyzy"
    "K8AtmYOYVvh2h5qdP/nqluQrTa49y2QmpNHbPAADK4RYcQzHVNkwqqXZzTgiRu5yz9SzqXoPPe9qA+tj6Tkt0ROdCCcIWB+jE5NNdJoGKpwMU7X3gdHM"
    "BuYmddwqACaI7QycmK8w0jSByZo4NKeAcQR0qQBO0dFiv+IDB2a1g8UwW5Y1nYe1o63o4wjMnCLtBs1h8rrOisKSGrtDFwgKUErY6liA6xropQO2/bma"
    "HTuuNHA1gxbK8erhdjPDDcjMSVy58MLMJMKVC7KUD4PIduXCCsyclLhKQfvnUoXj2gRNz2UCe0uHBzBzKeCOBOmHy8AD7kOQnYhL6hyLKB8wMwnsChA9"
    "R38Mbj+Ib7D8sl1hqfZNX2Z2DaWeYy5oXC8JjNTsloxwq/ywiHFdXN5YaNei+LAYZ4YQ7SnQYxohzjfYMe0KI8SEvJYXtoEIM/RrU8+xfrh9oRHbHLvw"
    "jIHMktAhdvNVKiWQVOITXD0gqdih1zD+XuUlTIbx9yrTbgxj/yu9JvaNE9jpassgNj/r26BUv4zWsKbmOdGu7ZG/xvJ/wIZepSrETRQ3oH0J6amrD8Qd"
    "GsB8u4eLEqyVXglRLi5Z5y3YfSCymGlhtwmPwMxGtAvaOSJNIwdGQWI+IiuKgixdYYZ7KNjVRnYrrpxQ9xtvHrBrKGpgvhCRQaaf23quSfQuVbwHVvQc"
    "0/ftxns2D3bWIMbHOok5gKilQXlZk1jVc92DI8AYWV66VMAwjh5qS9ogr1DJS2atYeyaYmPAtt5lDM2uv5iBnUNMrzJPxG6P4quDnmtgXRiTfO1GDHZN"
    "qQl2QxUhnuXtIisOFJJtrWdT5doANSKkiIBn4lt7RnwPfBQfkxmnGOOysAtUIEvlClvmilpNraphF8YwoM1iNKRuTfb51ocVlCvrKiFt9kGHNNZTvzFy"
    "g9CJ8e2XKzGWxPlocc4bM1iFSep0XsEGTB/t5NzZHVstVhO7P+WLwKpz5bHCbwWsaO/UGytWP9dbrmtCErE4F+hNntaWWP/YnRq5xvNGyzsPsMW2MPWi"
    "bY16zn+jIxBSoZ7AuLWDS4dtvCslyk6Mkq3k7/E0aRfqBOTCaEdpxqX7DyEBWw2sTgrPkG0kztllPynczjetwMshTE+ekIqV6nSekKeVWrelJC7SxGeH"
    "rPftuuOeSKgEH05YiCNUh4ud5ApD7YxO7M5QT13vhnriadWwHequXmEt1GL9/o1yNE43VftOjH5faOMqa2Sl1nYryKqnhXZvei60O0OpLbLyYSoMdSNs"
    "BfrvDdNnSSyx5tWwRo6eC+OL5W/ay6+Iaw8usRH2TphZK8yiK3OMOwqYC0WYaGFRHVlyLbFBSAehy4xNuzurBeaG1wl6szGdK43Kmhj7sLQ852Vw1e8A"
    "SyPw0HA9+ZyLqHOyZ11G6g231WXWDOzlHXbmkVktk1xlwGB+rxvYODLT00bluSKiBrBvr8x+mfOX13e0vGh6Xq3a5ALBXt46gMj+vjxK23nmZbt3Hntu"
    "Hg/Wt9ObroJ4HxkPM4PtuLniKDR1LNUon6GjbzoCT9dno56QEfTj6BsHOndel7hUeVqOJDGdhlVMsCcPHAdJd1iUqCuGA6dHF0qY3ziYxnM6wSPjQb8X"
    "p+ah7644rO2uw2Xw/abqRwLrO07XQ8/Jy71pVwDT7CrvHZ6D8ESw2otVlL/fT/qR/DN13zo8EeEUif6eOPmsmLZI3Jy8baEn6QqOCA91WAn4wNz3nQVv"
    "5tJQZW4fHBvG4zOmwg3Mm5d3TVoCzqSD5uRzdLzElXrA3ClSX0M1eIavryHoLjOM+rEC89BWve/n3MeAa+DSP0OvVXyVBezM43UDK3SM3fT20Jc3w7++"
    "yLLoVoYovEdr05cXDi/SW+AHlMhcWt/tvp1l7m1toavgo/OB6lGMEj4/X3s9owmTCb3GrZrha6QrVMWl4ZKkszVSpOG6NBUETAJjtnTytnSP8rmMf4gY"
    "CSwcv1efjTJv5pWVc1m/N3g4BTZHOHmnMDm8Bu9dsfrmNZzGPt99phN6uFOgZ6rhFJMPzm9tl8G0E2Aag0EhDMe5pk1FzHveSOdZgnS6h7O6qG9x/TMc"
    "5743eq7HzpqpVjF9BuYxpaybBke8u5JHeuS6s5oRTqgJ8dVI4odf35s3cpV2BVHteBAYQwwrff3OQ7eoyA6IkZKoYIuwA6Md6UznjdBGYc3ARgZydgRK"
    "It6zEvPFMqMKlwVjmmJKGchROKqOgNxnHHX4rNDaZSRLMbUMKUVCOCJPLoGtrHZgRRE06fDGQ6bF3kZEvIYwDVQjRQyxPIWAmpYoDsYBuZBfqlmAeFxn"
    "sFAufbHmrC50i4gfw5tdJjAwhjJzTyFVtxO7GVT0GUMZjYDKZWRUr1aWnQB2M5bpPu688mTWrbhlFN228muK0baIoGYodwX2+yHf8QoN1wzSRgg5YrkK"
    "NJcM7zIe3TOUS66KZZrcCCBfhrdHQi4t9/pk6Nk14Y6Ky8Bc4u1IXLVQ9mCkPaLlvFXEkmoiML4Zt5d8Kn6tmGXonAizbzID9M1CbzEwLa+iYNDLVVq0"
    "N4+ycWchDRgkBcWgYFItchnG+kYgQCbcTKJBJ19CCr5IgZ4oVw+siJKhxSk2mxXSDW6ELxzk883Aav9KBLGyCuSLqOrG5cEbXBOVDLhHTJjwdxkRhCyV"
    "oJVsCpO7kgjCzD5L80xKig/AzXpmlxfaWlLrCTpLC7JNsF58c2YRYBBmnPz1KponSx+YSE6w6id5Pz35N17CIvMnx2UOE7CEnIYGhuEI2o+Xp4HFXQMb"
    "oirVxPhuJBsMxQGM5hTQFhsq2EsMK1hB0oC8UE652RIWO4nq00CcvwYbMn+siM81g+F0RftSQvYhexn0ME3s2aKqZemLw3q6oJspDf44HQOstBOI0/xq"
    "lhM6JH0aGa4mn2uQNHeTHjbIrXtx0rxQX94uD4zswrhLfRxVFGvhAgPfzllpLWt6KDPvTS+8XiWnxb2aYP75kLRQa2ANXlIaaxIJfYBbViBUEXqUotCW"
    "YEFyQI99/x/mbf7Zn/zpv3fh2m9+9WsjbP4hbE2krnkgZwTt365BuMTkx5vylI4oCIp0tuFYKDGks3VCdLosxmJGONSX64gWV9kiuc19bihtQ8eMLnP2"
    "G32JsW4SbvQdepcMDlzpK8+m3QZGjA4RZLx51G6EKwEZb02YXPG6Yq/lZcZIg/P29ZvvsngJbv/lTkcenMdsekTbkQdnKxE3AsubZGwtwyKUtzaTtltP"
    "3+YmaRIYxfPalKe4OVg+y81MxNYzBoY1q+cUUgDJuglzCGnHnZAm1jhxwvQcc+QMI8SSXYBoT3naGjGN/JE/KauxAfNR7uGcWaZJiXVhpHS2LCa8DtMz"
    "gcm9eeTxzYu07UobgyIkiwy1QqjugDhnRacMYO7Zi5p6ltvmUKT/rsPSDS1lADBfti0imZYDZx1rwWm1a3msdS0d8pdZbnZ78A7Ml0Brb8yntkV9bkug"
    "83dL/h7ZFbg/WD7Vyyqpdn9wC8zDb3UnpuVYV/6e/Kc1HdLgrU5iipeAcWptqTmR16/ZwZ3CCgOBDl+JKWB2FR2tcd3LtpsCiFEi474m35E1Kpgi0Y7d"
    "aNq5W3ccGjaIyQ8KTO/y6i77PUIsS2GQfo7JLsB4rERanb7AlYesuniMvUVWnU+4Vbch1rgfX71VNRhg9Pch08739xsbmtzwpSCFbtXv32AZUmsfe1uZ"
    "sWFdG4GpyRQ1dlGafzbOlciEa4R6DcjlAEq+8LEmSViDGQbMww0Iges5nvvtKugRGJ8LDrzdALeIqXmNZYJaiTxWy5mzJpdIvQLmIY0SRg6S5lxeJH0c"
    "mG+1EtVekEjn2qXEtXmeXGdYyfYtxtdKFIz3W/AerOb9t1uFq+3eY7WZh+F6owKO37RnWBwlkIbH3wvDbCsNzm455krr3PbA9HsojODPRXoPcu7MlgJG"
    "W2rTuwCIotVy7joxTWVn9rZhepXF679g17euYRyWQQ6ZfYMQifE1C69Y2p0wChFLu9OrQ+96mQODOGkqpGcd46DA2VWFsRfj1Qvt5kF1YJg+wRqG9g32"
    "YnKLW/NaYILoZrT7Nn0AcodPan9gJAXsyTJYNavRADMthFuoqV6QUNc6sboD297k8HUho84ilriZmioCmP/eyfWIapvWvqxDCGz4c3FD5Z5MGLDrqtUW"
    "np5xXfVObPq7kTK2J8vl4Lpqrb3JSC6uq74BbYeqHGBI2zPtUpOmD2xVYjwVI5XPth+uq6aJAcy3y45Cvkjv89ndYckjvc+HHuZ7YiaCcOf00LsMd+Eu"
    "6aXveh12XBut3QfbU5jW7SINBPdGsxeLxXLsdmlCDOUD0urerOkHTL+GArqCOD2bqs9eZR9Yotc+oF9jLdJqzxMjCwDtleTaK7GmT7DsBDBtDGVJAZPE"
    "REyXo6TZOayRD4yKHkl7exOToD6M7L1HWGVcgG09xysq7fZvDjuvODJIj/HCAsNqYLfqE5wKReKsKcIYDrImE7oUlztycCxpTwOlubhkLtkgz8COJqMJ"
    "q5Q+WYQMGCco6p3sy6LXwGpAPu55P982kWjYiV5c2g24I1yW0yVFtlp56cDMQK0r+GL7kpZZrdBvYL5FV2Sl7MtEhboiJxiYT+6KCNa+rARVsQc5pCqu"
    "VVfUlwfm0mzGFRVb+ZV1xr2iB1ahQZtb6hQWKgdEP8ApdG/XufLNztbN8FydwrrXdQaL7hReHAZs6xssTGZYJSaVMUX8OyL51SzWd6oaHLy/U1kPwr7K"
    "V2tTX5fE1oHHJlqsnyMpA9jQcyxZCWzqG4ufjbycU6X38nLDU7XgIenVFDJTgdHsPI3OsS9YpXh7vQsjTt/lvj26QcWap+d6fpdL+TQGl97DAroNIarv"
    "05i4AKwk5tIXmefsLoIIBsW+BeT7cYaqProNuc44PgA7/omaLSbNsaJ68gjMezZujgCrHFcEdE5gQ1hJ7Di2ZV+dzpvT6oj7d4C5+obfhO/iHOvPRZF8"
    "YGxL8MZO53VqdYTBfzqP73Wost9Blok/FqGV00lqql2VXE7nma/2yMk4nQYwsOgFoxe1h+v3dCn+HvH40+lKqT3ujT7iCNZ0h5zBBKOatUzP8Is1DdKr"
    "fjmbQRw7hOi2MP0aM0HsC+zZYLlhYJTJR7dWAFt696q3cumeWfLn+NSs+uom/eKgVHcVtANz2dNVB+Iow+UNMd3T3uR8TXpM7JvCWGjCBlMNoXekZqF7"
    "YHpMq2ke/Vy4ls70817tcXctIE7DkOfr0O9X03UDyMVsjyPWWZW/FvEWQPMSq/kYRySuAj5KC6moBdcCc3nXoj4LMN+yLSq2niXrOi8rB+bSo0X6CDCX"
    "qS1lNNgO/o2oj33ElKjpqAHm+rdFDTpgPlIWUiRGdkdtUZkQmG9tHKXVPjqTa43YFzAflxrXjJzF9LJaU/iqVhewou+6q7siLugI6DIOKap1tqwy1PHR"
    "Yzo61nDBHaXlA+Nx4FhNU2KSMVvGQY1T0tm8XxtY03elfYBx4DdrFBnG7x5yomveiX4Ocxbe30Aa/RTGb5yevycZcHgzsbWZEIkcb4jhv5rFH89hHU9r"
    "yQns6teq3iUDvppfh9jlMoN7iKN3Gf4EptbdoumuOv2cK5OhRsGxc1n2p2Y1J2CLkJp8tQtKlFw/VxIfqfo9sLOIqRvXCdW1qEbcUWpHLVE3EZgfQ0Aa"
    "E0ZSdC1h1ANzVZsFSo+udqwloj3Arv9eDVULe9OWD4J9MzCTAwVZ54nZsi335Lt++3Gx1JKAbMWXm7oHjkl/Lgy6ywsGyx356nWJXDI36MIq9a82ject"
    "vBIZGFXjLT495cYs3sILIIAVQrw2r+RlobfwvFbMW0yM7O5y487KW3hJXsk6uLeQA28YW1KZ5WcYe1FpSdvv6TnapcCasP7Rz3W9Si4KMC6BW2diS8+t"
    "eJWS8dadX+AyvnBBalA4AJW2tUF8rNFzXvJKhIvUkPoda+5q+/Iu00Bs3CcxnjqtecJI5yrpZgF217eBl3uwnKAFX2Vzl3PzOVY7LCfSVG5jeZJi5SgC"
    "s8MeME1G422c5YTxfxuDO+VE1hMwkxYFuWAOdRarKCcId8AWITqGbieBoJwgRl2ruGpYxNRvZ2JNOaGWgdmxs+y4z/Z2hvPKjgsQbqczqyTl4yJGRCia"
    "MrkLMhHsdp4wy46w1eX1EWWP/LXjx31gGqehAdgRWLyDaUTFKqQSa26rA6NxcYfWxY7yjHcwsebLc1PNi3DHHeujV7WkBo8XwLTicREKW1fVuqtfC618"
    "cfhoxDQocDaub73VfTEl71+5vOfMIC5GHJcEcewmy1zYF/QmIztfWsJ6gDaeepfXhFtnCWkn5z10l8YlIPUVScz+heCt3cVKj8BqYtdnp8ZMwLPgLQ7H"
    "PDCOXYotFPQCtBTdA+L7bgUfDZhLrRXZ41fGZcnbd+7ibcvAJD8W02HLCmoIMF/tK7g2wFxurbgXFZjLt9XemFkMZdUcASZ5lVXev+ejB8epvktbrYB/"
    "NwPz9T6jEgsw/0ZQ/K5Yx2VGDcer28vKjNve72IyVJkth29xgU7lKVxk49jCm3Hd8lVF2jKCQX8VWgfGQ93dvMGujFDnd7NaSUnywt3kDpchv9BlhnVJ"
    "6sLddJmXETmoF4H1S0yiZ/M+0jLipoy7d2KSFZubdqz8BE9JwLSlVEUcGE3fe0hiBiY9fbRpR/jj7mGBFWCM/txDPgSwrudohpcR2VrA/OciNeAe6t8R"
    "MaKrskhlhKEPzJVU3rh3z9FXo8bOVf4zMA3euWpJcNuB+eIeccHglRO19JvfZS0DYHQjXxgo9m6Pq4WuGSiGhc8PmFs+PW49vXLKlh41hQzzd1PAXWbi"
    "lh4HB8P899oXzNtX3+/68gaTINtiVm1Bhmc+5yIpKerAfKc1HfjvZYWM0pTrfK/ssmQ1XbmMS0srFIElfy4OGFcZN6VF3fR7JRpaRG6vrl0vNcrb3kuv"
    "GjCJfV0gUWpU7L+XzCFgWgVXKhgpw1yjl7ezAbNXH2NeA1CVxvdgVY8t2hEPxis5gPmSfzCPdAByofdAJASXqpP8g2mDx2XFDyYppWPxA/HmUkC+9B5M"
    "9lbVvXsPdnlKAMuBLa6MQxW7BDswt4bgxeVn/y9tb9er63FcB/4VgtdHG/39oTs6pD1EGFKgmAgeIxCUWBgYUJSB41xkBvnv81bVWquevQ9tSZ7khthc"
    "p/t9uqu7q6vrsyKQt1TqH19/QkdX5ObgfwbDqPRY9C6xkJ48UljInJVpbGIIAxiGXOMVF0MX5I0KU3c5FPu4bJG9Ir2KE2wLiweLwnwCi99jLqvAoi+r"
    "ozyxpuXOvqyBGVgMubxr98JiG413fWO7JXQ/YVdmM1sL372bQw5nVN/lawtrgTGra+yaT3GQxhB04hMNJ9434YiujNH2bV6iL7PmOna8nXkRcX3C7yhY"
    "LL8RLvXOiiemhirmzsVJ0RZqX8fQtUW6keD/xMLP2DHOLHTrDnEkbYLGhwlMnQ8JW/y5ja7Mo+JcbRGrbHY5OLqPO5ecG9jCSCy9MDH+Xg/XD8cwkt6x"
    "PIeeGs7ESwfG9Yky2Q4VfmG6GBr3LpanR4Y8x+oUtn3JTsl2UQTQsTKELd8Cpq7i8A6We1MF6Vj3Dbq3OAPKaTvWsu/28e3kbz2cQVxEmfl7sZP3ELdI"
    "rItLIcDFBaOdvxcnw3L05+/F4sry6Fis2qJVI8bsc1vn2W44nVeetH5wDCyzbY6l+/gWU1AEFn2HmI319TEr+duDVqpEFWOO36OXv8sL8dkixopYIH9b"
    "FAzFq5J9ipcK+dSIpPDxomG7CA51rAAKpbM/kCpWcnTsW5mdXLIaPmJT5hOL/IyOdcxsLGJNZwPhWo4NYicxTm1cUGoiyMVl69EAsesMLyvHOOTZsCFn"
    "0WwRnebYIhZplR3rxKZ7jThWBF2nyrjiopNnaFxernPj+A3xacug1QGNLSx28ti6CibnasSZwm58YWk3roJdNpYY8ArB2x/mE0NBpKA/4Hmlof61P/Rv"
    "YrGTB7UjjsUeGDRwOxaMelTdrquC244ifrYqTni/YlSr4vT1pIFh/g1ztvoMW+8wH3OfogvyarmKZeSY48Lp1GI75mvbmbDAX53BRy11QxXWYngSJVbU"
    "3nNVFFdoNaxa2+IX9sL1FWopOKzIi+iqMvKpNUCVRgWrP56D17QuvrIWeE1jbkN/oMfJaI1X3zo4kIon8Oc+hlx1+PCsdA0ir8hdwS9a0Y27W2IN0zAd"
    "kGP1igR7YGPUq6ltCA6VdY1ckxUjrnn5IzWx6zw1lHhqObb4iYvLrx7tqRM6LccoJ54C4US1EFxxF/uxbu2B48ksXSPLz56wFDjGbYYaS67NvexK3lBn"
    "DmXg0qh5rA5FrMrwScd6YLkdDxe8NonKZ2LLmxNqtjvRrohlHjKgKp5kkA+53OdngR3d9eqqIq6BOZRMRF+1OK+eo4t24x3mFC1wcAzI17HQBBCYE0Cp"
    "1Z5di94eyIUWNojEzBwR5guOeMUhNcsHb9ITsYJuSaHkYCX11qew1gxBK6AuufNEMLRbknhaThRycisUt7KJtONTWKvI+K/HfDiEpYCJym1fFJNuJ3Z0"
    "A90RPU/yQfMwB8StbQ7mn8LgRl5xN39s5wciCArGOmDhleFGvZNYUPOwtLFbl24FFg93t0LFShwdAbNWrQtssW+Pbey2REBRps8tjpdY+BY7NhM7xDBb"
    "N7BFXyqd3Q5XKjCItoZFs8Z7wCDMgvJBhV3IoSpoBk1oUnLMd+JREpSwEX4Ka+3iOC7Gsbc+cEF1U55ls2j1INwNCcywUhOLdlQlx8/54qh4VGC+X3fL"
    "2UeWFbdhP/v6xHZ5fiOwdZ5jiSGbAPsYsn8jBVjDoivsgo74/WGm/pmYi9xn6aVYEd3q7gl4KRqGdqxHHlbd+EQh33GLsLebrPYRVmf/rhWbAuHrwIgn"
    "U267tb92YGB35hQQlDeXMH5jg/JzZbsTizZZBNz9E2IxJusuux+Dv3aOMhW7v0NpwMCLaouwf8cgH5mvROzPSW/R8KmIIXdts4Ynv2Gdv+fJ6xzi2iJc"
    "3F1qFocXWk3HWmLXd/LUA8jcRRYxfSKyK7hzz5nCzgbG1egFp3tcDdlySCxgBdO1DLtOPvMyTyxWd2ztoM5dIBWzY8GjVcTYsTikSkEQmI9v6Pn9wJiE"
    "6tmXMXLxjRgfozsC8yUyETbH7JLP6VcMo4cbRnh4JeaPO/ME6znmoGlfz+82p32fz/EBY3Hn6Ot07l3bpUdtCfd749ntELHNZ25zLA38oV1x0R5Jt9x/"
    "b5DOHSehMTmMY7ElG3UrFYXk3eMQO6NPrFqTktB9yxYwjXjHg8J8Hwfb4Wl85D3kDnexMxodvd0xr0dfJvN3/73gLZaqHJQakNgN4y4YHfxB2l73G4xr"
    "sxWNZbgJ1iFuqgFFl7mELnbF684wfnVD3Kh83ZmjY0ys6kY3J8lgQPWIKMNLxrtvKufAl6xhRVDwEBNM2azi0NcpRm3nmhjkLXPrDEGlDt2Ps2GD1uQ1"
    "ZjGNeek9XmdYlRwr2TcYRqUvwRMr1Eg45mQvVzzTvuHfLUdknw0buex34/P5mgyQv9fi95hjIebmW6+MZ7vgwaVrc8/qOmH3ix4PWsV3a44vvHfdy7qt"
    "9+3MG7tmO2ek7sndciz7U3iB4xXocwss75LpnpvufD455Mi+Gc7snNqIZQs/eGEusJu/vHbLfIvRFR0+5PV2N33eTBP6OsM020iQXLIuj3ufuxbTIwHw"
    "iRUOcx4xgJ9b0A8ZhF9b4eXsEOm0IizW4w944SBVk2NsFi9Fj1wASVaE73mAA6m5IvWCY5NdPeGFQ/x9CEQWLoEnsGGHGPfELhxbCl07soRF+MUW5ne1"
    "11EiFilAPHRjVmGxOB4yDKy7rcQxXsK7k5pFUveOCnkeRQJtpUVg+Gc3i8kgjgQY74Y9QJS98xOQurfqqD+xqSOwB4a3H2QZIMHOvbij/I3H28zsW+P3"
    "6jvsU0TvPLq6lLTXfX7CT+he5zkUYPs5ZBdP91rPqVUfnhJwxjSi3SDDNO2wE3nlvWICd2BM8uxYbAIVyIh4KB/yzBtzRySTR2vxuRPZETzOa7NZ5Pxx"
    "jPzSMiI6VRSw4CFcPomZm/tUNpNOwYLEgA3tAVQxcgwTOyMhihZnsmuXuB9pwxFgByjcAB3DtJCjwyFeoYdcYTYN+PL8uKsNsMhOF7F+gBr23axiRreD"
    "VZrnzhDmLNrr8/ETYX3zCEPKoRafc4FROkAiSI9YVLuoQhNRjFuYay0s2pEvgLuxj4eY293g2uYR0YXtaLbeEvLns5c7JHawPa1ORxOGkeQ79uLp6eGe"
    "Q1iw41H1eLgwY2z5DXhYrb89Lcr0gblGyqJR+QK4EVfnUavc2xcGKYtu1VguGFyn96qH87Zox9gwx9BX77tWIrWMB9r2KyyuGhNbNzBc6Ba4i1WzEOTY"
    "BSp87qHK/lLYjdZ1D2kGJpuFhT7H7dgkYVuIdHDHxtB9D6+O3dd42XgUNiE8Py1aexIrxGBYtLhnyEMeS36JAeo4Lo2Vhj3+P06VvdXYdbpfTGCYrWWV"
    "EQaK1nAhCwzQyU9MYhebpTGdsKdAYE8ovy1TwgSEsSGiPEK88U1LzBs/Ji2NYXcC43jtzw2ss10ktfFw85vYJQaRzvJCBGtozMzqWJygJj18a1FD08Ph"
    "l6Dgb002OktHgSHTpdcxH3Fl3VaH4sSb0pgjubiS6s7RhYbDsgaImhd7oibV2+XPkfla+owQNxQSECk1/FTYfklsBVYfXYNMtv2wnfhMtPQKkHEaCgx5"
    "GgYwFcv3EZ8oFMAMCgGk5CQ6hY2Sk7BUiJ8iH8TiV2Gf87wRgGBwMIjU7HjnWMoJcB5L+RKbU7U9PF2MP5ssXQXuLU81s4FB2PQ0NR0Y3quW4qYfYhje"
    "4IiZRtaT6Cx8FRet5d6J3fkYyQg7vUEQmC27z67ANJCLZnTIrA3lsx0bxGDqMgzifJuwkBg5C9tRnldt6xc2cE7yqdIm3C18KdhuYXcW2RHajDw3jnHI"
    "c3N8Q3SaMCC/+72Lg1L0/GtT6zP4TLQc75Pz5e95un1g5LILT8ytbBGevX0Qq8Q6bqlStWlXJ62K5rEGpDJT/U9hbvS2tCi4uz0J+/wU6VM4D3s3tE+R"
    "ZYXnbEWcgGdj4Z6i8WxdeexE2vRPkd2Fe9QMagdYIRYV6TwzjGgFB4HIKgMsShlERhq0c/Xrp8hcwzXfsLZbdhzy/A2dlGXb4fh2VPRzrGIsO9xcI8UP"
    "oIHpykvek6S7wsMyBunnooxVZBHiUMK7KzCQDwVyAsOJOeFz7RhGcjxFe3wBi2vC6gQGs2BDKjPkKQIWZUwdI6H8kQeMXO+snOxmu/3GrtACeXJt0QmT"
    "OLgcDeP5u3E5et4jjI7SqmHcUheCimPsCrcbx0ATuBDG7yW2+XuVv8cteqRibwjleTdbUxosUgoUpRzqa0EMPjbrpKRyD6aml0O7UDVZwiku940EEp6s"
    "CnKU5eouFxhEXcNmfIJCvOXvLp8iGxYI5QWUopUuL68v/CnybUHssSzfLm4sxT845ve55eo67Bo5Wj2nF94rXpBqAcML3bJ8u3hg+cAqJ4GHneUNgxq1"
    "I0+l5xfrxBYmtpk8ydNe4/cqBede4MNjec0uKXCxFptOrpHP+lOkRIOiwYtdb2CQmy2dtUtShoGbeR2xCqwSi8wDgWEoNVIuR19AOzQjBmFwFS4y/lVi"
    "sPobBlWGJakWhvvL0lQPjpiL0RqJUrjJvPb6AQa50eq8YdEK3UEsd3VjXxIeWYIC4+/t2FKsaRPV6hZ/jT3xJvKRcBY3Zwv2Zpmr24fJdvgBOOkwWRoY"
    "PLMdlqc3LgWrRkTm6mi3RagOs61h5QqL1WF4tUPBBpdkeq9sGCsrlZRh/QIrgmJeeRb7wDY2V5TEomMl5Sx4KKZfKOV6ImufgpfWE+b3uaU1HIJiCed+"
    "Novln8w771hcyaaeyM/uaCe9g2Gx2U17wN9b2NimIhUUvGhWzR6WbKtYQ/ZEL0OrWKOl5ukc8raxDNiusvGSNcBGFCx3DEKJZcD2J6eVrAGdRmTR9JI1"
    "uFMsA3bs4SG9mGXAbgcYd+Ig8QZjQqKQ5wRGXmnRFhsYZoZk5V4B53J0l81YmczTXePnmnb2rPwsE7l5uuvGvpVY59RkNLF014UYefSMaD7H8HDsEw4e"
    "hpHPTnhVWDkejS+imh3DvWqYP+tWv/ndg77p/dUnzN5RP0mYi6GGcU95EuxPUc0HSosegfdetglv/U4J1jA8CQ2Lr8p1xSCMbuiwrMqR5KJR+F1dSk8v"
    "rRsYawwH5pTqJUcHo6BX+BEUgkA7Dygabd2gy3MceYWemeNwTd6Sxc2gWDAV2vTk3rHdm3xZPOF3/JzkcsP8lWj1c7jxVlRLR0EyYFDTWwUdUThK2EVV"
    "HSzO4qXq9xKwDWZRkRPCE3mj2dKRMmZdgUH0t6zdIVZY8CyGtytkiDp1924Y+qxID/fYjkIqUbhnCjtsx2vLnNWinaxflrg7ZLLaRaoNxycr8MOV3Ss4"
    "fs0jZVAjxuFdiNvpDWbJvOMIVKlsLOn3Jlm43c1/pJN6++NQcq9sOPXbatSa0z3A1A7OBra6RRSNDWQ2zKRy4SbYuRrxkrD0N02r1rmBxmN12Y4neW0M"
    "pcmo3lFrNGrVLW2gmG7LK26Byq3pmjYbwPrEUnXCysY5oPxh7z8eF1JlTUhlpt5rwhYxCpwL1oCVmkbHKs7tucJik7aUmazS1wEbeLTr4BaPnyNTuXmq"
    "YhZdGgRPrV/BuMoRFpeh++0LA/PZfOl0r80HFioG17FHH+x3hSHSi6vdZCK6CfYHnve4bVbh7SUbgZcvIHbE9HF5jbyodGEM8ZrJtWVqZL9/cAXLc9nu"
    "qQYI2gO/4njJl7wKccnnmTIHcLYbR1drA0QuMC6/Kh8uu6ljz46U+/JCl/rZLv5BbKaAsCiqDMkR+0CkoZQfmXscmimBbEBXgkqITEMWXMNC8EvDh8k4"
    "IYAV8ePBoz3lI2bi0ZrAKOK6qwsEtZFiVDyuZk8hD+ZUE/x4xswYsYDdKyx23WRiHccGZEuOuFN1Mre2RL9vlFSPkAp59kgSDN3HKtnv4BGx6lNi3BVC"
    "tIZxcKyXPN4NaxTdeR+9zlVcl2uJA/bNV8R+SygovKRxMBk3xOh182EBh1h/42zJ8/FQ2VVvwQ7tu2G8panfXZsZbaMSz8AzV48cqmvc0qw3U8hGO6fr"
    "qdnxbOZ3Gxm0PaVvvt74vNbr7fHk1iuvQ7BSkLy/JDHmIfKZa/rlWK5epnFZKMmgv2CFURSoB3xxd7GFukkrBU8ZVthOb+4F0Xfn06SCHe+eT24YxR0D"
    "+SreefZrXa/6zS/wCq28Vm3EghqhK7XBFI2P1AuX9OTlW/gc2FN6mBPi7J6pwTngFFsWvajlBQULV8ysYweKmJoKkRAt98nf4/tFxQdRVRy6npVKlxBx"
    "j+z/roip0BylviZkrfPQw0Dla8opbtrS2U5mKS80Tv0kmXtpuPBSy+h1wKVjO1JiXaoANQ24bHuy8lSUhRx5i7SR9+DdZJlRUhdXDjBwd9Ptxea+OqSu"
    "A1xUDaf+MAS/K+8j0zMOqpClZ6y4Gq9C+RqqWjsmbenFPOwbTWpQNiupLA254qbZ5KzEqBc8M6dGLbVFODRgLZW5wQeYkyYKL1LBTeMfKu05BuHNNMix"
    "lZUJxzXNg+2o3dwHd5wS/7jmeqtvargvMRoh9nrjQlKfb64unFkbUpgTShV65ZKVIU17PFcspDw18rGlHpaADcuHYVSE02HIrAgzNfyhtLAUUFWWgNtg"
    "qaiJhWR5FZVilgV8l77mjSE96yo+xjAYG66GvGARtRI4SzaOu2CX6Wn3CE+B0tLeQtt0edg9Fqz9doLTBtNph7rvzTdmdNxp+oG5asmhYDXYsMtOs5FM"
    "bFvmL8uDQvsnLfYTMoPbRLfMX4XYTnPaISbT2aQF8NFu0LR5tPNmz+9SsT5xbg2rXWbBwTHj8jLzIdptbYIBHfL2bKqyRk4abXmCxoapuCzqpN24eUk/"
    "mUA3IRpXRugGjfI3jafhWVWUEsCMrOH0Yiu0ZYzthIZsthjw1FEeJS3K96O5l/UsHcMXlgzv/fDnJHGbSfmQTjwEfdMsnGa9rvmnOawvmk9zbTueem4/"
    "Tyy2aJXQ1agy9foEW4bxTRM9XRT6wNpWPUUNi7mZ74fs7OFDUxWW7Lb3TQeCI2zI0WAJCz+Ymlulw0nUnvEJwYEgz3eHT6x5QTw8CMJYbA4UVZizH3O0"
    "oNHR3qkLThorPRKCoubpka4Rgz4kvDXN0+LCX0YuFBsntymq2xw8wqjctvZeA1M2F5+ejiWxQuavMeWAEm547Yotmx6LGA2vjY4FNlA5whQgUy40lx3l"
    "QrPhdCklnTnkXCJDfjuCltx7suOVG5A+IDegrmHsdCDSYKG8NkejuoDx0NYC9tZlbUnHpa5wJfNvitOYysfG4CfDuI0Lj5SHF8iHagHigbcD3OHORfoW"
    "WDC9lsJIl6wNV7Apz63Y7V1CnWHhzNL1JnQPL3qb8dCay8GEVxr9SkwgrPBeo5G09GBRGS3sTmQNznBDvmaxFCNFutLo+acgZcMWffB4Jxc6bI/+xGIt"
    "xnj2javGTABLfm/wQhSLNt8HehKObBZOFeM83e2Ca42rM2sueA2Ojg83v0lnynXkIhjEm+3p1Hgm3TrTITL82Keee+44uYHtdLpE3ylf/iunU0Uue2UH"
    "+rUyZO9WeJgqXuSWbLXlTAonWYnw9eDZ7sUVpnxT6V9LV8oDue/pc3voMDMVKGner5VY3/KSDcfmmWF8p8NxZYrHmNPtIjZaOuceYKcLgydyBkQd+hGu"
    "kj7BF7ECpkgbwiYgRkXuix21FANcN5d2dS3FRtIJd3buwhqxk1iQYCm9i2HwgJZ5wTE6Xo/PMDlLOEZH7p7fiDHLiJuf3fU55LhVdoZcacj73dTgyj4U"
    "NrVPuq33/RHLaJh94A+3M5BmIzZgP3y2ObN83Zof96ZDfrp7x310WsYGwEPD4gBqYnFGPSJcLuWIDcgYnB2WXQtwYLjIpnRgTjVHIQQhgFgwb1f4wW4M"
    "vrgKXQCWUZDrJnYVG6E4EO7QRT/mdD+qEvXPlZu5VUToiCtRXyiqDFsK8IgDaa+uJiwuh3x1eUEEBq5kCEmsomfyUqTJZNCLolQuRndlFTUMn5BCxqJZ"
    "QlK7MsZa1Es4q92RcUnwhDJMcToLV+aVacaT9S/E8zRBsWmvhPWKSjJe6EEhPjCCW3gQQzwmWe3lRRUVERhtdN83s6ikx691BC9x482F+OPCWrUonIBg"
    "KAVrLUSu242dI45owrKeWMTrWYD1eE8AC9YqSagICCuspROYgr8+QvRRcGgglGxks3ERhjZXjngiXO1BzwjVqhkv4WESCIm7GTMVsaf1JAXw/LFwPYVq"
    "wWpg2CPUzdfWwv/ILydjVFuy7gnTh0cidgXxIbIxQ9AHfDEN48kYcOjy6g9T4YQRSd1y25rNYyN6kgEIA/klDGNwzeiI91QxPY+AjEh6c8RpipS8Ctq8"
    "wiImt+mpaFGWEWLXVsaAQk1zlC/eozYjBLIxj51BEUreFBDfNdtH1O/iSE5G8y5+4eq0dO7lXjIyljkCupRNHnt6EQW7BfkTywo9UG6wF2BHAG3Pdgq0"
    "ZaxfYlORaPSQ8VIPOZSIT1Q5g/juRCCwgpIhO1vAcMkhL8QVP5qtjfjjkkNRnDJPOB+3Z0hd/cAkd1c65lh8dM8hL8ZWj/5hyGayyu/WjVjtrZhfF54t"
    "pFtbYCD4diqBjBc86Agl55ayR8NCGPqdGZJcEcJ+6ocQcVPELIWSI2A/w6MbdJ8enb8Vwl4ngvgpX7Sd2FaUfMxsypBnwfT1AuPJbYM5BrSVUV7P0w6Q"
    "7VkgRWcqgqFY/wGI0kUrkZ1iKheLZROI0PIpdz2vdrCAUXKkYcOSInA31o1JqAq8JzaIZVyZAqJGWKiXmUjIxTDLxcBNWyMFnkEMOapc2dWfaRciX8Hq"
    "WtnK1V7JqK12ABJF8Br1IpfIJ0Ge53UCkHdCGSCQe8fyU9QHFp+4OhfCHrktamcOjKK7QL+3FYPg2EH+jAeG3BvvppY5OnJqFdk9nkNZSAKiIcNmcfbR"
    "nq3wjLacIj2TW8R1aKUd+oeEF0feRV4CoSO7CV98FbvsdB2BikRfhwnPPR3HZTaWvT4kFTGPYiU3iRDqI1tRLTw8JnNuZWMBdrS2lsllMJPNVsYX/N4V"
    "q7VHOjHecYWh28rJ74lm4htpjLGENHFCTeicSlzTmHuHuZvueWOKnpa5ceKqVrUBT6ETIsdlaRLPtBM7+TLPtifkOYDUlZLEbZm3p+PCuJnY7kJRd9Im"
    "4HmAkHuIiYYulKuGXUH4QqYtQiFcT2/EJE0XdvpzM2PfhSe3pUZiyiyT55lCKVMZxbxuZp+6yDRlYmg2yyRNOzElc6qJMedTebQ7yA3FdJEHHgM35dCC"
    "XMeea+rRTimpHr+XqavqR+wqsyhna5mwWs4tUkjW+pwvMno1JS08F9kDM4rLMCQXG5lILFzt7yO97jlM8rUyTxXM6LdmmsWj3GdH2+LMTKWmzw7kB218"
    "VJfTE2JKxdOYJK4qYeZher6mtIimkajIEVczk9oENJVvjQjTam1mLHwknNuLv9+V6m9Pjk0h82UzF5rntFHWOCW6q0oudwhxChv8zrCVWEXaPCYHcy98"
    "YEowGEVXI73eVT68iyx83NorGIUn5ptKpBdpA02ercI6oNuVg+9W5P5bgmZ8IFMLrygcG1kDq7BK7GaaP7frWcbBI+gcJCbcCTF9IROyrplpDme2UzrE"
    "mV9Q2sRZP2L7HcY0jPPxDaZrnENYpLgdmSFwTeTkHQqgKPSZszSRj6SGkRBxJFe0GP6GVJTk4wu5a9Ohy6DOrJg1cynGwTb3rCmsDuTdbJmbUek+ldax"
    "MvOo5CXLlEmI2fYm3FOvCuN5gk7mLL3K7BnZFR+pTSeTNapWgCcKRbvMBTgHfi2zVU446hlG0lmI4ULmVSZyZSiiYV0ZUCMl72TksOVJDVbM2gaeTvUi"
    "sSsT/A3m7Z0ySlkm1qaksCMzti4kj+UtNrid5lae3aE0qfLh9qywF9hR8thIh5kRCoYFh1klc9bCPmbYukpGGwfF1rILW0yV2zJnbUVG3ZLNgtWvzMk8"
    "Wmbj1SxaZu19fFbZfdfj9zayAM/sG3x9naRow4otRfZ6JYGK7MNPjFmKH7+nbMYr56asx+vRbiE7MpNQGoYkyiebxTne+5HddzB3M7NXD4holuOZ52kw"
    "k6bJrYIqU0sraW8BoY7umH7fmM76mcgYGbNb5pUONnaSJWRO6szdzSfuTd8gS3u9mQn8KmM2hrsylbPSgz/ST9fQa13ls7E83YLIEtrNROXcno2TkOef"
    "ZwefwGZmEQ+GdWTitGzjIbEc6aYMKwMYc6u3cHz1ihFd+czZijlYlfb8KhSjMPncVb0px4IT35pfiDgJg5hPuEHIvJmAyGsjNCSDV/7+iyvwZrbaigRy"
    "lkeeck1FSKLlm+eRNbPsQl56JuL1eAPkrye3t9fxQZr7ku2Q+l66FceUIv++wyKV/nrXN1Luz8SUmn99xHqm5lff5Mb1sCTAkthaURu1FOVDMmyi6kBL"
    "KCp0lJTIa8QcewkD7mQrIzFQ/kAkZf0zFdSLPPwXJRYeqf43Szbs/q4kQOT3vx9LJ+itXrx+H2pWFFVxEKQqAapjcbJ6hMpdSENiM0cdC90DsFdjh6g+"
    "BZrJCGf0xicuhSPzOdos2pFYFOWxlMVdlTK83LthUwU1ooJKkwuZ7YYo6tXkFGK7ZrB+CIt/3agpaRBr8tyDamqtZZGWg2pIJmhPlQoZLFuiAi8s2dd6"
    "tluo6SQVsB+cqIjWRpYtmSiZ01So9CJFjvMcFYeJ8HnnTfruiIKHRXmrHYut0o6K3FzWtjP2d4RFhbWeJfosse5BcZiZvxeFb/qDBqi90fsTUk2amZ9V"
    "7ZqZn41aPX1l9ZWBU9AflVY6qgX2xzR6FCvqDNd1aLIsz00s6s+MprpeZnpiiaCaWNQtGSyVfm9lAScqLKMSDuscsethYbOR5bTOYd2knRWCWE5snKyb"
    "tFDVideIX4uo/XRVKc9ekRcYy44dzfZmAaP2Nj+UoTqcxSycmF32CxALLu2bGCsebtaLsUpXKhsVNXksh9NWeamoeCgB3MWTmMSsqrWjclWTcecu7cRh"
    "yfpau6OynVJMuaDUUZlLha5YNmuq0ubdLKc2u0i3WVRxdpXxWyhWbSI7R7fCPzuqhC2V9Yp6mXNqb1u2iImiY10Quu6sV4Z6y4apxhprIJrUPITFRpkq"
    "+mlYfGJlpcm1URx0VRXOWhtFzFbT8VmoS2vPp9WERa2dNZ7tgsprJlnIptdSsbMFBrK2NlmEc/nTm0Uv14qSPObcWlVhDVUBS5ZEm1iL3VS5c40ssvcs"
    "9sbafh/rzinRctS7q8BU2K3GTvEwPhXZU4HGkjX7UAJwa2XnQR2praJrk7x8qx64Pb5ixdzBQYUHgy1s5pSI+oSL2FYdw8G+qmNYcSVthHFHkYr14RPj"
    "ol6ZVNH+Wu6AWHRtcP0f1SgtiJmTJZ3GZJXBreODWh+OfV4rMuvODdZzsnZNtScvibcF1cnPbpWtHJwFV7tf/twRX+iX5S2P+pqfWEdBTlYw66zsZn45"
    "U1hrLOZ5VWkzjtSpKrLXVxRQNK+QLNIZa3Za1vecEN9O18Vl91pFRdKh0qBxR1nuysSCoGdp5/UG+UhVjxyL9T65QEgTFUrKm+VMFwqwzqx6OljQlfXp"
    "Gm+kW3XTtMMir01jaQeC1FW1b9OQVZQDVj3XBQrckbVbBwsTJ09pqv07NLXWWNR4qr6jyV4bmGraFogCD6xebCDru1VKF0POwoB1sx5u1kytjzFzJetM"
    "bA1V+g1WYyKQ6gEXTq1n3eDKrhpelIF3qkyVIQ6R8w4ROcsVD1WuLAdlEJWayHXkbEbJwsqUEeM6lsl1HDotZbJI8FClvDLeSDteyqWjnJy92RIT3W/L"
    "ss4X1aTJuUrDZFXZr1RIUVfl6A1DzekDtaXbIUKqv1eXN5IPhj1oC+ssk60Rl1gxw+7IgtULJbZZKv5eFgCnOtIxlNjWDojiEyjtvZcwjGU9sY5C4YI2"
    "u2Yl++u1CtwQx4L3FlnUULL8qIY3yrjXHMjMguo7a4cXlplfV7XIK6vbqxZ5+Lu4CbirTjqq1s8sgF45EroIuMXuXGCnZm33GB6NNG4pDJrUrUr2B+XJ"
    "DetTZeZRyX6rzHzEML+DonpO9LyqbY8C9Tur0UfEVGBYxRN6ixgJCLpxohxDX7s7Pgx443H2rtli4XnaBtwsvOb7Ee/B5aH/YViU+XMs7b7xunDjPmi3"
    "G5f75IjBzA1bSxiWVlVuzeJNaA1BUXm+MSuPG9BjeRp9wh3zW8+8Fth3hfLFvRtwNxgWFe/dI19YHJXGuE435vv73JwqShW2DjAexxUpl9whA9U8DTMd"
    "r/ttHH4DwqX5d0BsNCwo366O7VrYLL0828VW7qyD5E4J0bfr7jIs5tF7jsXViO7ikkiNVlNQD7HEPJX0Y2H4dc8nMoFI6OH+URAFzHMjoMvDOCPpmkMc"
    "RVgaIvM9JmBq9wUMT0R3eanA2DPU7+Hixa7cioaxHcqVG4blmu6/Ha0wAXvJcSCQys0PyFVqhqFOr7sLASJni+SL74Y7VvaEsGBOSpvTwv1kzkyH0+r8"
    "uchtERgoN1CEOgoECFNX/hzqnPsnQJKB8rZVxix30/J7zCeG7dXxpKvKhBO1Hhqwic92zrbqYPeNfTNaNsPb18sSdGFlASOTdaXHp3D8w3vjIKeTOwiS"
    "Ah27dbCASTi0Rdetg9hFvK0lM2EzZnu0Zshy5T6NvFJ6wyGejNR0LCj62jIaXtQJijT/gvwhURWI4O57sbaTorB7+fnEpsoUuzdgfHWJKzZo2cyJF1LA"
    "QVETdwCGVG5YEHQeXaCNLGEy3bD7TQaLWajYFG6YGxBHwnNtr2uOpGL3WO4BtkOxZcPIZGuUencIg6tQC3pXTAKVUh3j7V5RXdw/C9rVgcmavZKf6Nig"
    "XgEQWMt2rQormizbVRJKVY/NjTfGp2CHcPc9wKB0MLfgJgzQxlU+WQbOvYzjAp3SOp0ywQbm1W40Xe78MDzLn0oScF+UDqnisRom2MV0q27G0jC8VbVr"
    "SxRICX/0KiyunpXXQokgxyhgcIShHX143Jc7ID1VNnyTHEOJeXMDD+HAct0MYXEylGLOXciDIy8GoToWzS7VE+597rPY9B1zzJttFrNwX/YTGEPRHYvR"
    "KbkBClF8Qr59YhD8DbtdWIm+dL10n/waGEuIuT9/jb6b8oeFB/jr3DDsKQ9U8IXcEnssyCFumw0XiygTsQDhLO8zsc82k1N5CAamdvIT4cgXfYk1ToOR"
    "wxH5wd/DEbIIkcvvcnH3wR41XQkWyP7k1CCpGVYAgQB74YBvcS4LaYmDtvWw36hv4Nhm3/A+DSKzb1isHRvsW0Nk2CsngTrsjqHZumDTm17ejsVLYtNT"
    "xIN/9NlNbEeNbB8y1mwt7Nq98xuLi7G1aGtCBvVYHWHYF4ha8RgmfEIqi40kwR5gxa1i6spPEYcFKcegOKJHUp+FU4UgLQdKx2L7HFkgDAtue4YO1aqQ"
    "GI+uJcNa9F06VavgGpFF2bFgU0eKQMNiOx5aujyizBWBFilXBYWcbw8yDNnEwWjGhNceBBd8wE6moDiPZgDhzy1c1Z6bAhhMRBYByF8buIPvysF17NDL"
    "DLRRx+EA4xbw+gyfIvCQR35ASeflFDAUr7sAjNtsQE/tGMYCT5PAMGSrslCJYYEsIvPwG9jyFrm5Pn634YlwtxZy1GzHhRwlf69iP/YLSd8w9EXl58Dw"
    "jb7Bp57Y4uJu8ZA+cfwetOoz+MUVv+jkZlcaUw+2JaW4uPCv9zDQdoVhJWX8siDfYASXr44Nl/soAMFPRABjFHsQ5PyyFYbOIor6U8TBcq4tAhgj/pbt"
    "oCnxCN8tzDmcRwyz3Y694sHGVViLdotEaZGvxsOZyUFaeNt5KDTPXovgNQ+Zrl2YQ7Xo/KC6nmOwuBgWs6iVwpkFyPfAmuhpWsrAZDWxgHuXLixAfBAr"
    "/MbU7rG3+gRGHl/xyLYQdE6j4r1nGE9GDbuJl47AUGrkYnIMwtRGOHpEtGMoFe+9d1gFRZ99Ixg5sIBMXcWf41VQTmJcxwKDpY8YMytRdMUxyN2eiqID"
    "4xVUoB92jO3wbHVsCCv8Lq+5Einf4htsF3nrYiz8Pffyi2lEM8uWsjkUsDPDSnRFfJMnWukT0GIz7tpKnynHMJKT7VZIk1a0A2fUsAYIr0VLDeM3laUv"
    "SMiPXqNnlUOx2o0VNT3RzI52zGzl2AiMFVUdi8GZhgZQf7ufWLJD0IqeyN7pUOzE9BRYKGPrySAgN1u2HEzhPjFX93jCiS0s1rAzNVEk5PmE1BdVkHMo"
    "T6/BucIUbVk42A5e6J7Vg584kSnMs4TgpHja+Oira8XzSH2K5CRQblkKqtjZXRKnpaoKjteZnDtSWl1gnT+HV0fzuDlgofY3aLIrHhOO4RMbbyzD8Gsm"
    "GQ9C6GpSFjHItJb7a/DnIPhYjrBYxsGayp5dzG8LwzjbHameHCNRNrRbLf0iLOtcnG3LCiPIxQODLrtWLPdg7RNPdheMcXQdgBVJfR27iQUFLEkioIOd"
    "N+jo7Wn3ZnyCAayenm8Dgi7TsvgFQxmMMorMfsSg4LEE3C2wQ7ZtWQFHjORShbKQrsixldi4wF7v4v/46cv/8vt/+t2Xv/x/v/zD7/7T7//w5S+//O6H"
    "3/zir1//+eI3X/30zY9f/PqnH7/91ZefvvyHv3/921e/+P7b737h0C/aC/xv//Tf//5//PZ3//j71y98+cd/+MNvf/eH3/3xhf8///WPv38hv/nyf/7P"
    "T/bL/+P3//j63x/+73/6h//6x99+9ctffvv9T7/9P3/4/pvf/ubXr9a/+vKXf/d37XoNuxfp2lyIf2/XAmht87RZECr3wnrk9WqzorjtC2shqLXZEBz5"
    "wswJpRvWYdF6YcWLVDdPEnwdsreZkaStEiK9tYp6qG2G6fhnqPT1j3/7i59++NUXP37z0zff//TtD99/8SLWj1/9m29+TVrVj/T53T/+7r99INDXf5JA"
    "f/Pjg0BwmW9z4qXxwm7FxGm0seFfZ6UvAkE5/Tlxf2ZKv/4/vvr6m69fy/7dv/1fO4ff/PSYg+VzmTaOg2j2wGJBD7yZDYt8eI755g1sN2B9COvRF8fy"
    "hbXw+nRsDmHG+xwr+D1zGduOoRhYYCV+D/nGDdv+IHlhRbumLWyRE5o4g0Lgf+0aOHgaNrB/N8wnhoVJ5YWhGIlh1eWfFwbfMcPChPjCRjC/F1bD5PfC"
    "WigNDAstzAurb2y2sCt2ya4RPPvaATf0VYYNUM9sIfhsDVvWC1uJhQ+6Y4W/F+5JLyyS4BpU/KnwgkaINYFVn8WCf+cLs1xXxGpiJfo2nn7PlXaANUEt"
    "mlXt7bJBvAU/vsD2AtaPsMV2LdtNYjWxwb5lCYv1XkULWTzkxqGTUBvA9hUW671CTgI0Aa2WWAM2c2YV0MhJFP7aqJ9j/fOu7TEQYSMxDrg+2nGuNds1"
    "Tja/2tjsSSY2K+0D6ebVhiobG4p6XGCbWK4Om538xGSzk59YbPcg+2K7nUTZapfT2Gy3cn0O262e2CL3zW/cSuyxG9WuatcWths7MbYbXVhlO3Ikw9hO"
    "i3vABgzLbzS2a/mNznYtD1VXO0GDzXQeDw7BhO4H5xFQOQkJyy+wZ0kkWp0QvALbhPL3N5ud/MAhlLM/apazv4B2Tv6y2e7JZQCRu5corxfYFFYJ1YTY"
    "TEzGjSUB5Qcam438QuPgRrK7uBgmhDhgbCeexbt8Ht15JbJpBpYclc3ag8uyWctPLLar+YnFdjUJsNUuKbDZriQFDtuVHMuJdltXsrnWD2I5vqt2eYNg"
    "MbZ2gN0ghB6XippVYQ0Qd4BBbMYdUEsw7bnfshUOBBTigQ1+dOXYBtuRAdQIVw1sJraJZd/F0Y2c12K7kX03hzdyYvsA69n3sF1PoojuPfuK7u3o4i6E"
    "RkIkVKvCKqdWs2slCWr2bZxazb6NUyvZt3PIJft2DrlkX+z4h/xRwXhgeAAkLLuuCuxk17WIZV9cAyu3T+U1sCSEmrapE8u+oPIKO1hgl0NeKTIVQjMh"
    "DlmbqpHKS4JfbaTyyk3VSOWVm6rhAp5LvKY2Unnlpmqk8hKvqS2p3LMvh9dXQsKyq6jcsquo3LKvqNyy7+aQa/YVlWv2FZVrFyYqlythlVSmCFJ7Upks"
    "CUkzAkso1nuKI1nuj0Ysu4LI8y0/ChpPSSW1k8YzBfNOGkf13YAmEDEpvszmTCbVSeL5ls0Wx7sS2xzvyq6b482xHY53ZtfD8fKNhHCqwPRAKEBGvhkK"
    "xyshf5C+M9nWSAL37CsC9+wrAvfsKwq3x1uFI27Zd5CeLfsSEtsaSeKaXUXiml1F45J9ReOSVBGNS/YFkUeyrUEij+Rbg1LJSL41QeWRbGuSyiPZ1iSV"
    "hyTfOknlfDvXSSqPZFuTVB7JtqhcMef+mxiHvD6+HA3LvoRmdp0c8syui0Oe2XVxyCP7bg6ZIhIqUAeWfQ+H3LOvqNyzr6gsvrVEZbGtlVQW21pJ5dYT"
    "45Br9m1c8Jp9ReWafUXlmhBHXLKriFyyq6BEYsA9udYijXtyrUUa97ccL0SLrucqCnoHll1B4i6utUjhnmxrkcLIGRCaiEIoEY53JRYPXcOyZ+V4l6DG"
    "8c7s2jjemV07x8v3Vt0kcE++tUngnnxrU3zrybd2krhn38Uh9+wrEvfsKxpL3NpJ45Z9ReOWfUXkmn1FZIrmVW/JnozrJJnFuE6SuWRfkblkX9C5JeM6"
    "pHNLxnVI55biuvskO3SyK8jcknEdkrkl4zokc9OTvVKLa1j2BZlbMq5DMrdkXIdkbsm4DsncknHxodiScemh2KRXrZdUbsm4LqncknFdUrkl47qkckvG"
    "dZPKPfs2jqVnX1G5d2GEWnYVlVt2FZVbdhWVcyQics2uInLNriJyTYgDLtlVNC7ZVc0SifHW1IMWkriKb7VCElfyrVZI4Sq+1Qo0VLPqTdgKKVzfUoMK"
    "AlfxrVZI4Cq+ZZXhCCXC8a7EJse7sufkeKkpaHrrpTrSMA54Zt/NAc/suznikX0Phzeyr5plV5GYz0SLC+eQybeQfz6wKkw0btlXNKYOudWkccu+InLN"
    "viJyzb6CsquoXLKrqFyy6+SQS2rMQeUittUqqVzEtszJoRPLvqDyQ6FfSeUivtXqm5o9FPULGNlWa6RyEdtqjVQuYlsWas8hr+xbOWQqH1ojlVM73Bqp"
    "XMS3WoOmfhbxLYuDINQT4pBHdp0c8siuk0Me2VdU7tlXVO7ZV1Tu2VdUTuhwxC27slXLZiJyk9FENCbXaj1pTK7VetK4JsTxlrTBNNKpZFeRuAgKCo/7"
    "NN8MQiOhRUxQEHjc5FodBB43uVYHgccV1+qgr9los+vmV3d2DfqOVGa3DgKPVGa3/sZmK7teDlhsa4DC4ybbGqDwuMm2Big8Ur/dBkg8rtRbbYDE4ybb"
    "GiCxZyBOExmH3LMvu/bsKhr37Coit+wqIottjSRyy76ics2+sYvHTbY1kso1+x6Or2RfNivZ9XJmsjlOUvkk2+Jbz7AhDFQ+eiY2vvVGqscb33rj5J7i"
    "W2+kfrxNvKhHKsjbhGHGsOwbOguk0wV0Aa3EJptR89DmG2chDjWh9x8nOdR84yQoWLUJvf9IpXmL6PrAZmL8xMiJXbbrSZTLdto/KwnfE+JQqGWwpLuk"
    "Z8t2ontN+6/oLn60oPUcRyYTsxOznbbK8ujgwHJ4Q+0SimYP2/GCQWzslJkWd/x+mqcX2+k245twpNK8Lby7R2rNDWO7nd84apcQm62kwGWzlRS4bCfT"
    "9uZi7OQrfCqOTe1To8GS5UiAsRmF67ZhDhupIZfRfqSGvMFgO7a2wCbz2XkhbTCf1IU3vh2Z0Q/YJZY/N9m3pPfAZLuSE1scSclvgCGtXG6+J8dK4YX2"
    "ypFK7kZ75VjJBegWMNZbNsNZWbLFN5orx8pb5MQ7fqw88Ada1bHywB+YnUfqrtuBPXmsXNnD22FpZfnoHKmmbofHZ+XpPjw+S4/xRgPmSJ10owVzrLwJ"
    "+BI1LIdMqKbHx+SIaw5lcsQ5ksUR8+3T+DY17OFUEiOZuYwHzghj5jLCrjlmygd8ro7UIRvGdjsndjuxpDFO2UzZkm9Yw2Zik5ggtprZqnIkuuMvV3Hm"
    "Ybzkgqn3NYyT1ZLdNw5YK8aH7kgVr5x0xpTFwKpksa/u6UvOOPPo8fU7UnfbLqwXY6aUR6voSD1tu1zbkRcwn8QW2pkExdqOPGaXd9fIBwHfyWPkAl3o"
    "h8d4LhDus5GiGd7OIxWrjcbTMZ7+TOEfNVKJap7vjVj6RxV+omc7zuLhRlU5uvZoRgq0bNfYt2a7RgrURztOo2S7zuGVj+5bI923Ol7jBmUzbIKuxTBs"
    "E+vCsAn605Ns8vf2o90BtrIdrswuDoecio5RJu4F5nLDWnqmcXwj221ObWQ7fpYvp05L7kg1onseA2vZjl9t2exyZuRcvZAPdHKuTiXA6En3qLD9wlrS"
    "PbyXA8t2uIFTw9crjO8jfdA6lQWWOSfbNfblE1juf57SMzH2XTlm7JVUyfXKu7qJKXUakEfTPdIrRamo6gtoAeqPZuzakgThmGZY9p3sW3Nqk31rkmCx"
    "b8l2i31LkiAWKDVhnTqKUSXsd9qjR5WRsVdsnyoBrlNt8cJ2zuywa34BN3/VVdBptR5VrKZXbp/UU3WqN0bV46437p8qXYFhHF7PdpV9yfl74/5JN7xO"
    "NchIxVKnydsC2Vdi7Fsf7S4wCli9cf9UitOd2hL6iAO7wMRX6Os4iph8pwqF2QKAse9OEmD/lOQrjfsntTkWoQ5oJgUWu86cGe6g1NJYpm1C2Wyza08C"
    "bLbLwR0gLeeF3ZPef71x96T3H1I6OVZyXpd9S34ibqWern6dmpt+Jfx02uh7akd6x/YxrAqr7EuBtXdsn55qj04VD+MOAovtg/AEQOyq3U2tT795kXbs"
    "np6qi95xU/VUU3Qa/fuV1gsVUx1r2W6wb0sSDPatSYLJvjWnNtm35DwEZbPYPpb+ISkQ26fTs90gIicnFqolRo8AY7ud7eJB3k/u7Y7901MNYBj7zmx3"
    "2XcmAS77jiQA9k8+8Dv1Uv3kpTm4f05emoP750jx06mrMiwhdtX2pvqqn5RW6KrQ85FuWPRNd+lOlVbPF3kf3D/pxdbpat23lMmdLg09X99WwLcTy6kN"
    "9l1JAg5lZbPJrjMpMNk1ISIjJ7bYsycBsHvyAR3JOxxqOS9sn61XlmFsV7Mdts+WcqRTj8ayVMAOsZwYts+S1duwQezR7gCj1qNT4db1DO6Tu2fl7p7c"
    "PUvieacOri+J531y++Sbt084eBvWhTX2HdkuXkY9/bBQwcsxvpZQwSuwmhj7SiSkr0ZfeWlObp98zfbJ7aPXbIf7Rl+5uSd3z0yRkC4dPR2iOtR8febe"
    "ntw++XDt9PLo6erUofrrMwVCxrT0mVt7cvvM3NszLi8fUULsmjM97DkSw+aZubcnN0/6IRnGvtrcVBoa1hNjXzFuahJ9ywir7CvGvfCu7uk41Kld7Okk"
    "hErhgSU0AIl1092k59vT9wyxHHJn35VT6+y7csiDfWdObbDvzCEPDnnk1Cb75vAmu/ac2WTXlkNe9X2glmPsW3PIi31rTm2zb8khb/YtOTXsqXScMY5A"
    "KJEB6OSID3s+iHwJ5YAvuz5ofNlV1yN8ZPrjRbk9mUVgNTF2FYkR0mFQIuwpClNB2ntSmCEovec+pn9NT3+TTqWpYS0x9i05YnCo9CPpmxwqfUY6/XB6"
    "e8uhhHjN8tzAJrCdQxmHWA55su/KoUz2XTmUyb4ziYdN1t5ydNhjLW9CamF7+mn4TUwsh7LZt+WQN/u2pN5h35pDPuz7oPJh35JDvuz7oHLYlHrNfbzh"
    "SN8fz8cDXVDPOKlOL6EuDwkTgoDsbAUela9HKnD74/XIEBTDEuLY5qMZx5ZQmKJ6TSZ9YBLpVXubKt1ec28fMqOqV83hPkk3hX64T6rEProb9fRI6IhT"
    "6fUtqbb4++XRikMrgrAh0s+gM3alF231AzVgL881CHVPL481CC1gL89FYM9cA/CX8lwDyDtFa8Awup5RZJ06317eHhA/MBKrHNpIaAPq2axx8j0hjq09"
    "mnFsTVDn2Gp+oXPyEr3h79RLCifUArebwgm1wC0t8f2GXNNuCicMNmwZL9apGG6Pd+UF02hXNL+xQVpGgXWqiltayfuFltCwhNh1PLryAz0/GsrE9ngt"
    "Usvc0lrdL+x07ebV98BKfjdUAS0DrTpjeVoGPfcL5WR7PASptW6Ph+CFYYnlFYCx786xqGvS+H5sNujy1fJd6SoFYltYSNnt8JQMune1DAQbBbJOyxiy"
    "Ae2xQVcQl6fkr3F5akIiZ8ueh1uMN8So4KKPXTHoA9UyTnHQaemx2weDR3oqdFzVSI5QhYkPcQsM6UeSCQ8pB1IPOQaPdpNEbfaFyfufhJp511NoN/sU"
    "ZTguxYKqs09p4Yau/6kdNWgMNCltCdObjzqTccmvj3btLBSVU7UwqWY3RoLfmzVVOtyhs0ofRmXibDRmiHu6Fyf1gVfYoS6Rz7HZafiqen2bfy91k+T2"
    "U648TdfJZDTGQ6E8Ow2zKU4YRqXwizf8TCj+v/num6++//W33//NFz9+883XX/zVV6+//6LEAn/9p4Pyv34E5SsQvr9zczp858lszdn0mX54HZzEnirp"
    "mLWIncQmszHs7NvZbma7SuzhXXb7B8G/MeLItu/64CT3EK5blZAvA399oxQpa2xJaVPO5uThPRX/KM4UwtH54Aj+EFSqXkOpWLYwCjIEuQ9LZVMkClbo"
    "6FrqQZEeM26Y8SGqq6VDVIXD4uOWsDg53RIZnUfO/AidK2Kv/UOQ4YMz18KL7eiA1MIbNh2EKi12LTWDCrRsGVZbC4RB1KjEUIKFpz+LRd1NYI+Ys5C4"
    "3GHlA+3WM5YooIzfmrwkZ/p24y3Y8lFvzvdIKXIeXuFMM6INq7tqPH1nOyD5BTDgrvWnBx/EkP50kVtsV9PHCZJDy758DJsXaP3gamKb/uEZMYC1NO+H"
    "CNdKuv9dnLF68xFBM2lNfzhZ+iweIE1fcSrqftop4ht1PS1JMWbW8Hqq+Osj0Qd5BZOVPdXFtT0VnmHSqfUdtoilrjBeF7WmFEPda61P/WE8OWpL/ftg"
    "MpX2VD/HSa4Za9Dpi1i7ngkDy1vzwT5yZg8tcKjn6nhqVeOGreM54lBH1vSY6OTSVSGGvUPrUjOMM1PmPBSoLRftYYQC8TIUvLd4ItaH2r/CzatmvoDO"
    "WNl6n1ZcMBB51KprS+dhfqGVfNVzIK2k4rHl7n7YAzexx89B8Kypju2QTtpjVzAPS6tP41Jj39M/WIhaWmKfQuv62TxKv/7Vt99995uv/vYvubb/jIRJ"
    "X+W1bRl+XTBpp1IcstTcLia3JQvKQZHS1q50Bof6gXalmrKM0064xoyVloAJj4JeZHA9jHLrpXP7W1Jn38TdqncAK1GQpfUqF33LuOxmr169WNXPEO6v"
    "vvn6n6XZf/r9//Xf/4sT7e/Kf/zX0a0XL+X3GoKVKogS06Xg3ehp9Ql5xrtm+cwHoVB9WzpztQpLbp1KfVpgofWs4glNQMjZV+DnUxkhb1Ao5asn8wIU"
    "lj5LxMzfanFaLMHy/gBtZZg2qAPiF2u8ZutWebqCgD1PQUwIQ7VkcQk1QGxlRVVsp1R5IluRQRuEp80jFCEfnpcO0A6qNkuOAmiFt2Fj/ViDIh3kC5PA"
    "Z7WbemDyzLXaTe0jRveUtuWpeOkWbxiO9fXkWI7txBoxGXStCM4ixnZMVGIY3rZWFyX6HoVfnVvQ7uh9ZpU30E4hGlZlY3zEVmE7uS8ez2Hg2KZawWog"
    "xFCUI8igIJUl4WYzKIGMMXDICzGnzUuAA9sY8gPb8NppXixNQ66fYScx9r1QtbQlTxErejM+wxbHJ/JdJmd6YnXk7xGbMAe3jD6xXRVjZt0C23x4Bnv+"
    "P2DH63c3S8XIPXrioLQmK6dVRfQ92mTNS0gZu7zer5+KB9RwUKpOxYHzQ6vaFF4VOLDOFbsHEbbvsPBgbrXn0ELktQy49T1kiXIfrZzklmOXU7/Y7fVK"
    "RrdiijuwlYMDL7ldkz+NP5fUvVgFT1qc2P0Mm/g55QYxaOGjJNxdmEN9cpgCPjQ/Qo3CiVc2BdQTahNY6fr9mLwlentggB5dY6JbzvCXW9ozrXcwxMJ2"
    "77CDruKbFZx6i7tGGatm+ffbR2g8of7hbigF90zRNVbCs7MylOY5sKHiVF5Z2KGjy6EMXG0PHp9QSbYfv1WzI2jWp1pVOGlZgRtkvjbMm7WbN01EzFg5"
    "H06JwcNeWaj/Cemg/W+QDiyjIuxnbSkFz2EusWbkv8qyeDqYLAWoGtqjtuSDbNUz3AbYMi2XVRlxybPNwUf0gWxhrJM2wAu/X795fjYN5V9/98MPXzP1"
    "JOnS/0y6/PVfln3ywr+mWYg+RwizTZtN91HlZZHhI5ae06U+wwaJgLDW9kgqcGFENSqMn53xj199++tvvv7i6x//9ouffvjVX7oV/sVklT9+8+9++A/f"
    "/PY//+H3rx/5+4ec3aFRtYSr4J1nRAUGX+rxMxjuEsP2ZrspbPwM1rl1ZvZ1U6lfpyAkvCrabtTKHYaKvcOgVG5LaUGs3EvjZ/dM8f4zDCa7tsRUvQYM"
    "MQoyTLLQVsl2D+zRbjZgRZ+dA4diZNfFQ7H651jJdrdh39x8uMQ2lOHx0J3bZYKpzLExElvIf07x+qNpXP/9t999/e33f5OJb//qm7/59//ut/92/CJ2"
    "yS/+xNPkX7PNChzGjclALWWYm4ANW0zvijeqMajPsUP9lWFFT0H9XHxiS91oyW7dJmPY4+eCB26lT3mHnY/D20qGxXo3IUMDWvzsoguBZeIdC7t2tc+x"
    "kslsQQFlUzvMkuYHYybb+QxDgKNPN7HD6ULt8cCqvmuKzornQfsZrG99d1Q+QdrnmMgCc7Y9BUbLa8XHfJSiw5fjQMSfugfQTNawC1vtE9r8QDrTJbak"
    "47lI7NhOZoOy8qMHg+NHozj6OwjBAG2nC+NFnl7DaLy+JXwZvF1i/Wewqr5IU3xI4YztSmzmZ+FY76vYNAlXS/hO0X0CaFH5e+Hj5O+W/TlG89iFY5Fx"
    "xrs/x2a2i8muzEZdCvfi6yz8/+Mz7V/NZz7Te/j73TKsWxlKVBBpSG9WrW4e6vxY9n5LJ2+F6Q6hSGXmWAE0ogSPFatDXnfDNqBBaLInq/bZI6pFz8Ky"
    "BvbWKhsYctMb5gUaT1fRAU/e34BBi2HJ+zcxzgHsv5qiC+n0G6I7HOM3esPw3LEGGKp5Ggb51bL3e3GhQ/dVw+LU1NNVZcKy93vCdsPYNYornS6tkUEX"
    "0OBAwlbqGOoDecZ8hwYS7HvO+wuoEquR+92uN8ye9WMO7b2G9ahNduhQZRhqA3t5vCrsxCcqyyBaMvtdgXH2Y5GahbUzTLzz4iZWDO9yeCeKAJ6mqgMh"
    "SDmWq8MijYahYoHd3V6F+rStb8yof+6XPoZieWYuMNRZaawW6SLTBRZ2ScdQss0kCy+MZ7X1Bj87sUFNb8TPohyfYSTp9LdPPa2xKEKb4XpW7S3APTtR"
    "i+O0yqogJviAKiyeYVAQvhXWNXPRyrvWy+JArjRxKGm3IqTGMZTLNCx+rm6WCXApwieRBUVMQozR1ZWfRUlOv0G3sIAGlYz+VvFJVNVEMObbJrAuyMtY"
    "nKoSCyaTeKUhuysv292oZhRPiMA2CrHZ3cvzvlHi02UD9N0RCOYYt8BucfDKYcU6g7wshmGVP9fxCbuOr7DYeGWzLrXLPT48qrhf2Am5y6fGobCkhlEK"
    "nz2R3j2IN4TNCRpzv1ttsAuMQz4FO6qqJJphsRlNgUsKhIuUY5oumYo9rIewurGlyEJ2lHk2iCxqLzDaxspKBmHPVpZysTs5vtpUY94IhZPcciQj1qJ1"
    "bcbNq8eyh9QP62NG16qljWursfaXQbXiwNfcFZ1MgNfWujzwKqBiOy9ulaYKKo3lgQ27Q7s22Kr5+TRt+Nh5XeVbG0v3GqZDgHJlTx7KOnHGa8kFVifT"
    "7yzbYZgXzDm9Z98WPK8PEd5y3Q9gZDQLlZBcmSCmcnkfoaiIayIqsDPFo0bD/cYraaJGthuLdrI8YmQDMzzi/f5tJ1kosXOT1Q7c8ePBkikekHPBMcex"
    "lVihUNKuboJG7OrCCG5uNi/dK8FCx6AAMg4/MHRjHv4+S457GRZCV3eeF/OxusCz6m6MPTZUR83v0A2MJ2AMSjiHirioLwOM+240SF8qJ9hGxIeGkHYl"
    "CQRTnSr961VyHKqsLudlfZy+s6XcEqWPDzPvQSCJX+vZdWMJLXHllHgTfHEO3YwdF4Nlje2C4v6YuetghHeMrLLzQratNiSRBa9kxvPAMJSbwhGluSzx"
    "6rYnp8BSaWbDglesKn7Xblyhq7LskwmWXkrZqmLPnQKoT2N13QJmFNjA7pFAG1xr5d1ouWp8GkuFgAyr8d2lzd4GGKjxlitpOxgoXjIBlZjF4aXSwBTW"
    "YWEpl9xjEir5Y9W54toyBtmExR2wq7h2DXdaxygf1khcUb3ke2JxUswChLVADk7HuC28zJpjKghthhEvPGkV6VtiwY32lMwYOXyrFbNf+VDxsmxW9L4n"
    "FttsJ4MyN40NbBOr2GZbRa68hp5/40h9blhsMxZ6eWGoVeKPJgp5hY8QszEIil12WNvSiv4NIHwdlIVNZkU7iU1ssjPFP8rEJjtT12Dh/XGS9xS96FTI"
    "07DagHG8LUpRnnNyDpVDudrbBWVlDeMRLQUs6koAM7tSiJG3YjO6WekAwjY2LOS528jxzOgT98dtZFtuG/KZ3c53qdX5jJ13LQzxT1gCxr/wSK7/aj8B"
    "c3nw3WrVZiEB9OLZ6qoVlsUh6WELdwj8xSC/nPfSWhmGX5ukUC/h5uNYacJ29KX4aD4V/tC0grF9CfPjZYVgJ6AVx8HrwHZhGEkhl+wlHqR7quhdR8mb"
    "anVbwdUMiwFPPSq6FQ/x+VuhAEHO6DZTxBt2o7K41W0dXZgLJ1a4FW85cwzxh9b2l5mwaNZ4fjvKDlRz9oV8athqwAqghvm7P7GwmP+4fLb1SBpfd17E"
    "BjnzM9dmXByG+SPVXaA5uIH5j0nhzLAgADPAGDZBgNHfEvJag+7IzdGh7PBmHonAYiSV5VZ73Zg/A/wDi/l3lYfvxpr9Ewy9DszZhkc2cSiRGKjuzoqZ"
    "ndzfwyCbsCBAn3xl9AYp273RhjCv0re7zm9vqGbpnlxbWFCgy+LXYaio7mt4hflQmoqyd3gFV8+H1ITFCWib3KqzHKpnE5vCggJt6YAiDV/1XHlbWJCg"
    "Dd7YvUWgaHVXTUBRudwdkKugIIDNkKPbIEArvBINCwJ4OlxgKJkY2YWFubplp4dSbxGKUz0H9hUWFKgsOds9jMahyfrrnUVyPb89CGXBTD682qkJ6B2K"
    "JK++sIQFAar0Gb23N0Iw+XaW9fXKLBgdsijUnU/y3nGLe3khDi+i6qtXdurCggJlsZBk7xMUKJOKj97JBcvgo69bQK1DUkoY5AKaYRzJBgGKVF8dMYc1"
    "arEKCwKYIZ2E8rTXdV0VyDTIJX4rvEpO5lkhHNt01eoIsqlWUBUiRh+RQMmxIsjnb+VTIbb3EZ631cqiQqg2bMVQOoXlPtwbrHoh0ynI528VSiHcdmND"
    "zTF5jRnmBPAKpVeYcwGvUAoIZawNIiuzJ4//3Nk54omJnSXmy+eSVS0ljQeKzVvV0iFoxM91vhX7CDNStaKlZMgDemMrWso7ekCesKqlZNKWkNAgc9jK"
    "Zi48WdVSXo0jQiTryjrwhrmeYrFeX2D+BTNJZFd/pHnR0ux6o2sXixoXRHnJ1DxRI+yhjpVsd2Ioehn3Gem3qlUohabbMNcPWTVSyNSGebFSL0cKis6K"
    "RVtbd/JEOeW1lo7eBEe22qMrsRV9h8SeCTnTao+exGKfLanD+gzNj0FlCPJX+rInWWKurlyr5DSiQEVdLH0WmPPQxWJahsGgsKbUPIa5gnHNpU0wN4bM"
    "8iuBxZBncpB5YshTTzyDxgBWEoszP5vY9PRMdy+o6l6ZF2fZLNHAFh6ly8KhpjAniu2tIcjfbmtsXTbm9+YjGUvndlXsgTG1lVekfHphUqX1FSmVXlgX"
    "h1+Rs+iFqZCxYScwFcrti+s9JHCZN0x8omhtl/ue1eURpoLiFHT5RvUFe8rqWzuZGrLVVVPcsDikXS/GviZGwhwCgcVQejJC28C+pXqjO1RfEyejV11A"
    "ZvXzLcCovMDiRCKmM6AgSnss0MY6ti2Ja8W7bzXVGTcozk9LsdG04j6SNiTmwGnxhfVcx4P1aVLXGBbMlm7qht1g+01lqw1yYW0xpiOwOBf15NJGqKZj"
    "WNqNp/CqW0u7C0ZiloIjLDhIzYtq1xhJlY2qUz2/atfS7gqiuL+YsNgqteJl3TfU6ctChYYw13OsciWq7XiZWRlfnijTMPuAC/UoBsVxLynU7w7WY28q"
    "zmFg/kUqHcPilJWUmXakoXlhjaL0hvJ3laqV2JEI+YWpQHXfkVzEMd6iO7Jy1HlvkhjX3rwyjPUdZTtfmGpFGzYDy4fYjnQBL2xS4dD34TeGRMSNDTUZ"
    "DmBYlKd4YU3yll2f0bfqkjteUc8h7pRT+HOFz0TzqbR9N4/MgIb5C3Oeo+vH3CP8C2frWMBj9oWl0HRgyjIMup9+hnspvbBkFidyEVUrGsxr7+BesWLA"
    "ZKtncix5zI7X36lWC5j3wIG8YRg394m6stVqAXOHnqhTW60YMIl83DP1BZ2c2QVV9s6ZXazZ3pqZKV/i55ZmxmrzVjOYrOxCHrSawRjda/WCKLvr0ruR"
    "Ma5aGWHe0zd86R3j1rsdW888wPkJnAyrLcyFvBDXrbYwX3YmuXrfJaWTYX5urd4wh4JTMFP/2eGPUa20MN/7Ji8HJntHt80PiI+9u/mFLn50ocZlGWGD"
    "UKbdSwEfYa548Sq6nFiUd6kq0hqY68C97GcV5izEaz7G740S/nbVy/0tYbFV5iQLGSXiHauX9arCRny3c18Y5rOwIBL+XKRNdKwMYc7hVGgjsBuf0PNs"
    "FDzPPCn+EuYjHhIbR4HZwvNtV2Euv3mm5iMsjvyYZKyjTGy9oYenYTG8QW8Fg/yF4YlCia1gKqPy9WzQip6Ft9kokTqnKuFgYAMQdoVBwbb64a4YqKtb"
    "PXGZoOCgfXFXGBak8wxcwG48MDxOfgoLPmNOhsCiJGn1SPyE4oAy44phsPp6sPAS5rKQJ7fAUEy/1YBBthoRrlMtDg33qkGx3dvWKiI8q1pg7FjCYmZt"
    "8oCOCmvETKHEMBckZ3pDDItldkhvmIEybI6xZ9Q5qx572oWdGJ1O2agbN1K9fOwNlMOqHnfIvvHutohF7hOTYnxwdWlTVFjCZ3o0GOYijgdPop0Ffccn"
    "hobSoBexAM1ZhcVa1EbpbTToGi18FI/CgWIpL0xBV4OKq1kLZV/DXC6d5VJ+HRY87GNO8cWw2FLmmAAIesVZFu9kw1xEnkWqu9EoRxR5ugwk539h0h+M"
    "Br3vNG5whd0YXqOcOxqE0FkqT61twhhd7lpTSFVgEGmGp794YePKO8swF/3GlQp29Eju8MK2mEqPaJQXtmgfHEj3+sKkRzfsRN9BxdrwhwCwKsif1MPv"
    "OmDQZYzbRAHkIHxhlXLJsOO/HSvi5shAV8dRLN7owbiGtCUD6cgcElGg0R2mLRHk0uUwZYmgG5BiQwYyJb2wwdfk6DDTjdOpoxr9guynUQAxzKWIcSo3"
    "VMfFNVJXMgYurrGvLqmBi2tsKWDHwFkZKbwY5l/dS5fUiEzGjvGSGnBYGltGL8NidHvwOW2Yj25LszzMZh4/J6uSYRhdfeMX4J44GBcXmA9uSW9nkN8M"
    "wxySOC9ILkNSikEzui6xngGJcSwpgcbA6puQ0gTFXl8Dj6sxotTFC+o6nSNyoL2wRinfsBM/l/xzQLAcq7wl5L82FfUzqHgaqSUZA7LmmHKmMywOmMko"
    "WIfJAzvlOWdYrI1FrGxhznrHzHthVhxOFgkMLAgw6Tvqf8WQqwgwGwgwiwgwGw6YySiY7ewgwDhUKxu2Ats6xDPyxlZbgLGFjWiXQsocIPIYuqVn5Map"
    "trF2Ys61bU9yuecCqYa040FJYLylLcg3+hbdPhOSqh3Bzt87aOdZzYT5UMx+QxJAKnXWcoTFEWCqzhe2wsHaMYj0hvkmYK5Fg8h5e5eItyqYVlcUs+3M"
    "Fp+o+uxqbEetkG3q+LWiM7tgqrELQr/GA9qOePaCj4hhQ9AKaOe8JnZjU1i08a9+8Vny51PAZTwduLCygeF1bnzubhCAl/6+2Ho9b8t9sZONnoLGBnSy"
    "K1eHl9Y+uFH61mbcoUMePffxhvrZuTc/CgWlYXcIC87L3OOGRaJO33eaxOTelteUYa1ib1M+3lE0yzHNAvZqOxdzCwvea15S/G7D2g45tQyqcQzjWdkR"
    "lOxnlJx2RyCHn+UhKPa21dvCzy3eW+PSpDPoxjdYiC8wcLgqbrYiAaNzH96NCz48zkswtcVb2rydmrAg1dSbc1CpaPyAF+GCZWqkrtn37SK37cLAWY/Y"
    "lI7GlPp+UNXqB7jqoC1AvFgX3J7tsGoo0AQPBm8FFlt+dTH+VbCr1nhLqEzcZzy48+a9R6qYD1YHdpNJxQoZuUcys4qrdSfP4wWcUOE13cVBx8Vtzl1r"
    "1dcvbv26hE0IB6UJim/ufDd76WnIFTsvgkL5Q0y/g3RbxpBBI4eduNF0KQUX2I8LCEYTP/tV996BZFUTCmHTHH3zunV1z3BtWF63HcLbScxVzSbk8cyP"
    "i8145FfsVyWFRkk5B4LvyeffOLhvz5YgaeYvSq8UOMfGfXbyQI5QvJgsXCXlbIrMJWWhBYhPszEx2XT/8bu4QyrXxKDiN+F9pUS3Ifc/pLeY633MK/LP"
    "+ztC8+qY633Mq4faxd8lV+JmvOBKTqzFG77kio0oH+rYTVk4FHmlUSM/6KJpj6udWKgYymNiYHn2WOPMkATSH3ojZfVQyJb9FP3Pxrvx8UTAoy5n5lns"
    "+Q7V62J1PGEf75JWgXFqJmRcPH85tc73ZboPuOCx8JzmmbLU3BPP7pmvpsrnOe9C2vvtad8T61AAaGYdyoP6mBlcd0yhkO+80Be3x8xwTRmmmcEcZiqL"
    "k8/QA2WHJoZTa0oRTQwWVleeLGHQ2TwmBmHalTFHr+TdqLS5wjpUO01P7kOtUBUUU+05LxRmc0yvf65sz3k1rmzPiTWubM/NiOKEru/iZqQXjCeuT2xC"
    "e9YTCo1Al2f9QOlN18bVxEJrmWbDQZdXV+6lniQUqOOdjiXUwKYrrMJCHTf6W6pxDjWP1ChZnoEODaWWgss4lu481Hl2jaeGHGW0qko2hkoplB0MCw8s"
    "1D3jivKoVl5VCjiw0OPMmtqtCArziuNDEFTNXYSvG8dnpgKggvuaWjn1bGNA+0xBvy5qs7de2Ih9dW02Rc6KtZ0yQg166ZpyXAQYUCgtRT6MOqDfXFVS"
    "fUWEkenfbyoVY6+Y98CWQjK2oxl9u7BJUwDFvAqznpsMZio9By0LqQhdtEBQLDP34ANLhQgfDjNm0JAetEKbvWtqc+FwbgaShGAz6alWJdffQyKDaX03"
    "TDXcembO3DDpUJaueJyY6UcK6EsbzNFDpFwo4PfVQhaaKk5qGssBRU++swvufTN0kYmUExQ4TU+MEnmA3EZ2PmjWz8NQsXGvHHkeuKL+wDRHGbQsWBuO"
    "PBlc7z9p/ptpHrgwE8q0gHA8syY+TBBx7936NFVM2Csp1ZdBO2mXkr/ThCkPRsPC4HRTXVp4icgry8woobi9CmEwLCZmns1LlppLi+0RtGDXpShQ6MhR"
    "ytM+FC4lRd7mhs0KEzM1eQUvWzNF09p9YZs1kzWN4i8s3KhKeluZaZkmcNkSIyTEDOU1zWHhveau7WlJ27C7PyxuqwKjlfRueg/IVNMRKO2mfTpE3ihn"
    "6y4AOw2CdcFVgGZSV/XCpWANYaPD84A+bRc3kHkozDRNwo9BBrwBt6J60tBHH5V639Iguho8KtoHI+lqaf69CLQ0Bw26vFw61TS9TdwQu4DR8+KGtGE+"
    "IDT/WtK0AV+R096bes2nhH4hly6CXjhWWHi+NWkz3Zx86ckyhbmA4B4vR1iTZ0yVxTp8iHqTA9Y59NLpMp2eA9dEU5ZUWcXDR8XkvSFsLHj4lLSoVzgC"
    "0Qvi4C2+3PlSWKcTEb0qDkLvFkuGhR0//AszuNzt/fBcWukqEH4bJvILghOVnsmGwWFqUKQzz4Mz4Ww1BPmL1Xyy6FJ+etzT5rtFV7ATVdncx6ulvwMc"
    "wWq6QJQBh7GSrhJwZ9Nd6y4V8DWjy/YpcNacUlIaNjdc1+iGesIyuWb6Hu2L9TJF5xAWjnrz4S1zsRfnlmfmPnRxS7feTf7xcN6jO4o7+e10W9l0Brzp"
    "3nLgNFjTNSbYmynN+3t3meUJA+VqE85MJkUkNunTKFeWCdetJfO8efMs+kjOxMKJaKXD4e4cy2NuHfPdRY77G0Ho5sNZ058pWPJWxKy7PS36hKZ71ITr"
    "KP0iNjwF1n44JdH9cycbpA7NPFZH+ngterZyyCsUlSslC/Msi6NnkkVLr7QDf1oe0cXTfQq9glcUgHFXXDmqrXDKOi393iCYmmcvabyg3XEH4PTyCxZ6"
    "5tOjL/bekVBrHoLBy85+ehdWOSi3dEyUH3Ni4ap17tNHMjwOncEKG3CfXuldOeFlnQ6XcU/fTr5AzZu7bF/5dMa1Yg4yicG1O/nivBjvXemFCt2OeZQ/"
    "nFXDLfEqH4BhfcNDne7zM54X5scuV98dV6j5u5Plz0V/d6mMDRuT7vNLfrh3wfOeJLZon0lv/Cu/3jvptT/T/7fTu1+ewxFsVHa69faIMyjSs5kj8jmI"
    "KZADdOQK9tgDjSQyDzsmQlXE5NSaTswF8QhVZg53st4IjRjpjB1BWTUXckTxaw+14AU3Qo4y6KYPeARv1SW5x3RqC8Ec6aBeO2I+eE0PmJIsNiT94hHg"
    "IuuKudTPjfATckureD2AUdgYUIRuf0Snd/9FgAu54OgZCEMHp9EYCCM3GMNGRWANb317qh8G4CxhfTBQR/ENB+E8vKTNNLYQ9jMf0RIV0UEKF8ETe3dl"
    "ibDoiyBUTxEM1Y4cuxnMMRGoxL3YF/anpeY+whDklJ51HaYUL7qWESntILZKkTBIfhDVm4RF5ErP6Vroc0X8Fvk29VZexESBNZPRYP1DSM5oIjHqIDt2"
    "FfUTAx7SPhoWW3sM8V5qoyykrWdgEQLOMnCjhR3SIuRKxi5hvMpwaTFO4yK6bmd81GUQ3swwKkQSFjln05MlCn0IaxfxgI+Irj2Bkc+YA01FKCGn26IA"
    "aoQcnowkGwxNbAo4i7UwXckWVhjpyIuwVRy0ucWSTcU4ESV5MkhudkRYMuauIWWHBWKSBvXG4i56LVi0XhxHs7VmVN9g9CdHUhGvvzMK3bDgvkux+RZM"
    "GJRfM6P/EFrjwalTwYku6O8lL78OH69t13+GP56LiFgNBQ40eynnj4VORrtdMiQS3HzLNtdrQ4Dhlu+NYTHbDC/3wM4FTDND/PLeKZlXmBj3znDaSray"
    "3RT5LwcSz/8tgcSm7Qs10VxPDWAoMOaQ0nLB8erhuTgRQmUGqP7BaDoVITr4PBiZ7spMLGFrGUdqa1Pw0LJY0moapkB77GzZ+GiloB4KObndIkFvuTGg"
    "6Bhbdt5OnWXK7m71HsD6/LMzma4/czn+kkymYQ8NpVBpUm2tS2uYIpzC0AZiUY8VqZXdEg2ZxKwxV2ZYrMdFtKaZMGmHPPANupJ7zYI46DH4epr92flO"
    "+59JmK//9D79VRLGUqw7jypTIV2WYv0ENvjsuhQQDAPvNsyfU4Zttmuhuixmlr3CRgUGe7xhzkMN22zndZ1e0KIS/lKOMIwQMhaUKUcDw/xBUBSjfunR"
    "VtL16fZILOkYdsFFXbgXdngBGebym2FYt8tkbYap7wmhtkyZgG8/nJiiAG6H7GcYidzhkFCWdLcXdUcdG02Y608M24LiE0tOp5dRsWWJQxjm96NhIFSH"
    "75tBO7EeP0dnrdshmhukX0OgqGHjCHOR07DNAYfXgkF3CqqBdb5/LGf/rsA010qadLKvS5mmpNXAsB5DoZ/nbZE42SGoYwxzucQwLmO7pJ0i9y/EnLIm"
    "37oGVWIkQNsc8eT1c5tWcXJ1GrJoGQQh9NI3t6zc2g0u8IbxRFk8+gW2qjDQWI+Ja1J6tJPIbVidwBpnFqyrMJFqQG0B2/w5WNiKB6gJ69GXeqvbKneF"
    "VD6GDTbjkrUoLOUYl6xBZ1GWHNkNqx0YlqzC3aqsPD31hjbGMLKZGuXLHIO60DBXy5ddKEZ4xYcFjNuihkmjMI+oQZCZDIMEe+vCzLYywxjmviZly7hy"
    "KxRNhnGrVCili5xTvYjBBcTNWKO8j2M8PhV+rYaReC+sxs9Jf2R1K9YFVrew1oB1toNXn2HctagG5thiuwLOsBX6ZVgHhHfNRQr0FyZXssvYCMPwawWi"
    "jkHQ5FwmEjEMWkQr9xAceSsIzbDBT8BCYKUiLj/BQ1W0QEOHwPKhACJDLvAcNKxPYXGmzAsO0AiRyKA1hJUDDGrUW/obm90uCMsoU9ItUc7RMY2EbHDP"
    "HAk8ZQ1LiL+mgUShSsdEEoRrGobVscobcfua3/UU1g4wMN8TBRMcwj4xCKdHBn+vbzKAzSsMiy3B9lzeW1tXsmFYbemyzp1cbeVNM2w0YHjuWgIgHEcl"
    "fjIs7sEtHbQlD7ob2KrCgoVu8TfDCiAcKctFNPnZe4VhVyhkyHIbhXhgCtMhDKf70BwfqZKATUEVCA6ZJVlaDRiuX8OCC25xS0vaBCZwcSUbBB4gq4Gl"
    "e8LmkSOhp4UChFvFskdtYlDunIP4ecOwy47bc4HtLazxsyCTictO4SO/AMNc0VYytZYlwWIzjHdBjVG6gjCdeThmL7n6z74Tvvqr77754sdv/8M3P/76"
    "26+/+eJX3331/U+PLMqf5Wb/4z/84S8vkJmC8UtUi0ihYMi+fI7ZUXIsZMBaRjgSOzOPN7NjtnyOxaXomM0z7oYhzIRvx0Lt+MLCruLYacJ6jIVaN8fK"
    "AcbPbj/9cZ1dYSOGQi8rx+oAttk3pBa/ResUNiuwOYSx2eWIp+v//KLuTdjcwHYV1nx49Np6QXHQHRpXmEmyjonIkTTLRYu2hRVAi5OIKCsXXsoU1g+w"
    "MYSVBexwFlFaMgSkJmwMYKsKqzEUxHa8oEip4VC/wiagfQTVGAkKThoWxn/H5hI2F7A7hbUYycJ9Wq2A2e3Adhe2YnRUYTnWK7CJWfRQOjl2Ba0YHl3U"
    "HOsb2DrCQLyL2+6FbRLvQshwDMRjzjHHYuexarhhkWPBsZXY9Gn0qsNiSlhiXMge8TiOncSWT7fz7eJYJ7a6sBIYjYsvbODw9a4DiQqRjp3EamCMFHCe"
    "FidInnWOYR556HvnPGbOo3EeM+fRsJR95TyaGxwdW4mVwLY2fY/soY6NxAaxkxjW4+R6RJEWx1ZiMzBmrHKsTWD/X3tXslvXkWR/hbveWEJm5LzkM6kB"
    "pkWDlEvoRUEQqlwoo9UtQzbQv983Ik5EPImPkygaBlorAgeX7+bNITLGExUYaR27YDMwFYY1uYAk1RjVcA9M91XNvq9oQqLV7PuKNNVVsBlYln1ayeUD"
    "t5I1zPYuDYglb3AkmAr1an2WNqzjeFTLKRdMhUutfj6UGEyg4YiKh2pVbpmb/OkOr0bQJVhrwEyQkt61GxaHnK0/QCaqWaToz1nmjmCYlPE0HtOBWDw0"
    "c2tBXZ46fVuQycw6XdxSwaVRQ6JTwc8Z9WrmhoNLXuol5oLp4LiZd3FMr9K2t7KEy6BlF0pkO7llF3zay3mD6Gl1RNdQKsUc08uVqzuWY7oSHh3YsCRO"
    "6sTt43zqtL2xYHbR83Wkv9dixErEJJiNmEuMJ7DVHdM9yyHUeK4VYHb2sqT/bhC8vILold5Mdc3SuFKWgnM1l2MqGdr0OdY66Q1avrGzHQr3RGXu/rjs"
    "uTUcU6HXUwxYadEEs4OcBw58zz7iAQXG3UkbphnGG0Yx4o7d3kP+5o473SsiBdMZ6ODe2yA7POyMro41fay6UsP0iwXYdCjJBLATxyag4q7uzaUbm+Yy"
    "Kb27dBNtDphJhVyw2r27VNDu0xsUq1hwX3haqmC6F/v0azmTfdiM5SHsk24JC4KRYnEYhUEf2AhM9SZr9AOd2rAWmK7ZsES9DVP7csMyfNyCVcNGYHrv"
    "DTIVjh0CBjWHGpDliP5UHM80cRTZ8g+sKVbhJBJMxfOovhBpYCGEn9+xLisxrHBasGJYH47pprDGRIx1HNnR/ZpJHRKVbdruWFZs+FWWmniYBOuBqQYn"
    "xX2OkWF2XaYKAcqmX2AqjsaKd2iDa8F6YHpdzhTvKPiOmeI71HEv2AxMJcMMdToRtHiOK03H9JxNcqmStBZfMF+PjOtykh+MlPVgzL0lzyqjZrHbMmXs"
    "p1l9PyWoUbO6mE0JahSn8AWmxyJIBRe65wk2AuuKeTkbY6p+TC/7kraShpljZ5n6MZ1WQ7pDDmAjMNXsp9M1LfadGNYC0/09nYiLMf2MZb4EhlQznW6H"
    "S29MmYLlBjZj1TC4ZxhTjW550iC32tQ7ZLk3ctkO5WzU7JiqH5xMbTNVsbKL3D+n6bWJ+4um6hBG4rnJjOUCbNrHFhuJxx0Z0/uc676WY3roOWHKoQSk"
    "GUQ2Jy2WzEy21WPJCMd2eSqtfLe+wcnoGOuA2nRIDYc1Yjoz1JQ1LXC+0PVXsEmO6U5ZXskuq7e+s22p2FzqJ2ECjeaQ+olScqftBLWonJDpmHqsknMa"
    "8d5SL07yVgqMqfMsGVHLcn9Ssmw23tGSyMOQ+XsnKCpYZpTAyDDzlvOpUcw7e6yJogBpbhqYhhVY9jmk7rRklSxyfjsg/4Zm3+BFx4xpzCM5K5F0963A"
    "ZmBN584Tc5fl+crNgf3JLitxY6UZawGHb/J+KirTgFlIZpJNQKy2pEACMz/7ROoa36UWbZoWDM2WBCRNeSug6ZD6xbNnzTKmIdicfc9OTbRKQd8r94EM"
    "mGthumMa5OREfHwrJwTLgFlhCUwd49lzpOVuasDs5A1UZ7PqZAKZXZ8FmO2UYY7m7Gd7KPkmIxYYGAPhjex8YGuAM4jVRFvFAXI2xmwVB1q2iHraHKsV"
    "mC2jNbdhzMKyA7VRrD2bEBxaGyV6d3YIk2cOWtFFBqCyHFPvcQ5JbjSDbFBkG7HFW8kzhUQvAmQRrmH7ju0dGzDBB045phhVUMl5mRhSN6sYY45p7J8o"
    "5tjCsuT0K8uYHMVWbI5paITdYDa8hFNLzrvHmM57dPcRBVXmnQ1ehfrCtAcxFWMNkEW5uwXmyRNSWFXWEF8USohKrf87PBTIccwCzC79PmzePXOPMf25"
    "+TSewrRPl0a927R7wdzq3aZ9udTm4G4FZtkK1j5IXCg2OrRbY8wuWmkj8p26aUxUdIssFr/LO1LjUnB0MKayonjtPGMZkJ1jTpAe35kDyrHa4KS3OHK3"
    "TI9oUMSmnAYMS+yATva/3uxCzMAMzIeX7b3eCGt1E28lbvgOmrQUjfRWT/a5PWYvIcOkRNy8o36TMZODDYmP7Ii0A9TQgkycmA5pALtMjyw2NIthzILf"
    "0q4GmCUTgEg4RfErm/O6L4rHX8Tqz8AszNtsT9XYF0wvQcC6Q3r9VueFEP+DjKSGZGioq0vRU2lZblmqnlrJfo8FyNasWTCUveLTMc0mqZ6lx64VlXne"
    "e4khvWpr5GswpYKO2IlVlvH8MGYnvhGuqeqcXozpFV9DzzcOa8b6dEzVg+qUU4xpYLYaWT67pXTnuUNNMN151csJGFP5Vj3cuCwjPEXqG2OYZOPR5eCQ"
    "QqnsW46svU6lC/3CIBc9MMh1cX588va3d3/8O/K/pMuPBu6WpRZw4E5P7KyRbgC2WAnARzqVZfW4AEBbBD7srvQnnJxkSfPqc5pwksxw2Gqkxvt2SHZY"
    "Q8DNfPRJmdoSNw+yE5bARcJTbme9gn8naSH1jXO+Oz++OHlzfPZDdGV99fLsyU/Hr188eWho8c3x69OLt7//8fHX32Lek9TBS9v7YXq1BHQGMOgeIh4y"
    "MOTiJaSsbViHxErIWBOI7DFdsg1zBmrGmmFYM8ak+XcOTkTGpPNzzl4jIJj+r5cMC7aA+ZDRIT5np9KT4FIRzIszJAY1gMF4kViVfEfyXB+ZAkDQ+nj2"
    "9HOT1+EzVhswGzIo7ASD0JaQWwWW7X81o3vDvAcAY9I7nbESmE5f8qQGxqTTdQ56aZGugCAqGSJ9hfsmkvZ9E6g4gh8zz1aSaGUGVodjZM+l7hgG52oa"
    "Y2MAIxuJpnxumBOyiGDuwGpgdQFLDg0dipsbIqsLsGyvVbtswzyfSuR3B+brqGFiSkymS46xaBDMtmPVYrENM4pFBKIFqdWhKpBnsSWU0wjWHGK/q0DJ"
    "3jl0/dPy/HjGZEoYyw5VHa6bpYz1AqzEzw19rsZIlNxUsG6/J7qCQHZ4qjYV2zCn5WKMCrAyHSv6sXEYK9p8M1aXY20BS/GOob+XTRNMkJaCmWCo6l3Y"
    "MK8fS3XZWNx8ZazKWswV70UD88SursCmYS3eoSs74zQ2tQ82zF1sknrRgNk0cxmJfG9whCd0gxSsxf+2DCxe0SoguNMSmALlFdCZJdt5AaN4rthzNi2t"
    "Ylq8AxtDGR9mJ6ppXxWdlOHYqJi8Fs81n+TqmL51pf3nsi3QshGrH0IW0jYLdC3BAhrYFiYXmITEMLsvmrrTZOvBrcMYRlJiikmUQ8FW/G+yHe8zkFXm"
    "M2b3QMs2OmeYY8wO2ox/xaT0/ccwFE88Sy3bCfKqV15u7O4Rv6cEHSJBqMfu6cB67CjIgeXCvKltIViPzW0iL404BBWYixUcFhaXfiAlPKJS1Y+j3o3i"
    "Wo9jW01GjzjegFb8K0R5Cck4cR959qTIqIobpKxP5ZvcPj3E4Gd3VDeB74TmImeH3Xg9xLFdli3kcbbnVlwC+D0nghLFftmFHJhf8DkwysD2L6RhysGK"
    "i6tAiag57rcBzDZPraZHeb6wGDKuu1TH9Nty3n8uGTaa3+c6L9ntLbGzuulM07FSgNVQIsiwHhpDtt/zeSEVl6KXBURQ31L5/LES0+c/V/ysxGvjeFcc"
    "ecZG/F61/10xZNUPPBlOsEXAWo6pmsBCo1GVgSO0h7T1s/M3TzaN/c2RKNRHl68vXv4U6vr35xcXL0/OL54IflVp/8eHjx9//eeHj3cs6Dp7+eqHt//7"
    "7o9fPprOTkvKo/mLm3UM3LCseb7ExEn5cDkP23NH24+eH71+cXr0/dnp8avLzao72h1vfy6333//6//81/agvu6+g0IIgJhVSW6jDWtqcRGzY6VDY3px"
    "enZydPHzq/Nnzx5vZFXpWakVJNZsGEpXiHnQ1sFsTxkF1hgDu/zp5dnZm+P/fOiAUA9CTPQmB4oxVSObJEbcNp7d8fc/2KBkWe87ot9++fDb+1/2hrTU"
    "/CYn2uPVm3oSqqo/B8bElqqNQ0YW48AbbhvIv95/+PDPGMfMylBA3Ga+61rNpKEf4kbutA5uo5fPX3y6VFHNh/Hoi+47L5PvLhZCZM06ro7xwHhQMmeD"
    "0SrPB0wMCJAreF6d2hg0fVXafP2JE6NVn2OBT3WPJ3Z/jI8zMZ8cJmQRWh1E9fKtFtVr154lFYjPTk9PLmU0e26uLz/e6ntS527LT8PxqPHRIh75RxnS"
    "7lo3D61uFycLPrmvN4ypBvh8My3L0r0tDdtYNDGFkZhQGzY1nZtaRayYZSp8MEywWiAvprZcIeG/74otJbmgQugSzWcKhjp3+c0lsAUM/zsTdDSuwS4Q"
    "kwv6E9f/N7wDhQukbK6QXeqwJyZxTfpeZlARZVk61gBT0gxieiabgSTGuxPTMNTFRy6T19p9dYLdk+OL48vr9IF3H9/9/pkX7829l3dy8g/J9KGuj8XU"
    "Un2H2O+Jqa8wj1iU5gFM+7Ns2PQlQjuR7X+LOsX5HZpvTdxNGdtgohyKuPyd8v1nZnf6/Ocf3/5Qr5udvdri9PcHzVDVnILtK8k2NueoioeHjLB6w3gS"
    "eEcQuidv0IT9QKWpE2nDlnYHISKn3kugbaAcsS5J/hVFNBrYSLKzKJ1k7H4cWhyimxbEsfkVGnXbXgG6SB6KspFvQ4GtyJhGErYR+9Fhz7UMhTpMHp4B"
    "w7jYaj14reiR1qqkbLzkK4wV/hC5W6aktSpmtHFjeWc/Wogvj+UVaoT2hLyr4RjNHTzfSzpof/FktDts3PygyaAFJoAxPT1E6IQ6uKNKdGOa1qLKyv4H"
    "Qp7M1GvPcbphRz+EGhyu2o2IHcGfkSex2IRniti7IXMrRulDJ40ebdKqNWmUJkPTmw8UbfrgHJ2s7UrRH/OMwRnajGW/hEnNVJcSw6HhmRzSx1Sw5pkc"
    "zKQnC0PNi+MYkyAuY3Ar9ITmHaxCVrx26howqQmyaoS5mtdA2lqS8zZowx3yMlJhja9Y59bvvzAcY7pmI18NMt1/OZiuT0LlxD4hTEFD+g2LLY/PNqt9"
    "NaeulppU5Kaq9ybnpepUGtX835t8VaMqMYsX6gwKadV16l4pn4uUkDKWzaOVhWtQIGOvyUJXNOVfrUJyG2nWlNiRjRZhG4rmUCTWiCxpvTRLE43cx6YB"
    "Kolb6kZjgkHZP+Kxe8ii0QMXTYsOL/eNeW1VSkJfjLs+a+dKYhIWwp1StMUY8U4t0DtIqwKIKctxR02LHDRr/aI6C9+MzIQ6l2uQYhgz76tpHUqATkxL"
    "POgam+IJ2xQXp69PN2X5/JXZOJfXFmUeULpObp2g4HHZRsppMuZuMT2U0zblw5n6GBPEbr4Ku37CVfPZ5B74pMsXxyenJ0f7geCv8w1vXu+7kZYqfuyx"
    "SfCLkLJAi45svhLSLp5kdEHsPiFV61tFo3vGbKUq+OzYTCA4gJhRA/+L5kiHn7Oek4zpKSJnLuJ3aD9AYqptMzuKkkoTc2hPvIO0YJyYfPoGe0ucTBeb"
    "tRWepjtP9rPbJ/tkb7IPzU7WLhXEBP1tb+SyAEKifnAWD22Y8Ezd+QPuIBKO900M5TohMopNPv5avL2pmRB+ak5IeIQW2P9YJHSpL9iwYRaa6HFq8YE5"
    "kDGYIiWh4lS9PyITimYA3Eyi9VUMiCskWlL8JC5h73Qphrxp7K7Yd+RSVOdITcpCQzm4cyXvTWyCFr5zUv55YsUUaXycSCkRtMzcIs1tDHWUB/EH53R2"
    "eUfQOXAurTrZp1O4ck6KOLspTzu0Um0g9kQKuwM5DWR9TTeMj5vaDuD7ZayaPaEFyGx2aC2ImJIZbygIb7HZAVNEyp0nsAGv2tJEtG1/gUdxw4ZykIin"
    "DYdhSuWaYGiLwxgOF2v6Zuo2+KN5b05gogbALBrYh0jS/QRbWiMvXr+m+5DZQICRXXVSfk94rmL6OAIrv9eSXZOS8mlGJcxuSdOV/+X+bRWmnJl8rEFU"
    "Xw6S97K1SP6cnAniRGUzA7UTxYbt/V7HmDMyMRjTJEDBCpYXfZUpr9gZU9tYbBiia3iH7LRV3IheyiezYZrZoJZrNSgN32gZ+9EMV36ZRFr4Z20kyuCx"
    "YeDW1+fEB5uHx7RTMsiSY7nKQFNnhldNcIqW/FivHrjiCKgc0eXxraSprBvm7QakokCfc8pAqc6S81i8SZUUz8nMlUhDyPBlZen6cYvEokeQWKyLaJPP"
    "bdMMl8yoTNswX70JGh05Odj8pLXYG9RMLZgZYWC2YVz3y6oWkBF5M9aednM7ZGhFWgu1nXVJrbkr/16547w8u5/etipkYCsmKcZCnhixzmO3U8YpZh9R"
    "ccVWT11FIz3+YCRx8e9B5xur44vZyUB3Z9a761a4Uc27OP3x/G+nb//x/pftR/YjK8XEtbWM4btaKexkqesBzGRzNRcTP9ccqwewYlunxf+q96x332HN"
    "rgT4dxQTh/InGEH09epDoQRR2sHpDFXiCoZkwj3fHmPZMHM8Z7vZegSc9rG959Tzxunc/tpWcShq/Gu3Q9HLVSzFc+qcbeZmFCVJt6FfOry91A/LKUbN"
    "bS4dCS/kdartBeu0P788O9lL291z4ekuuc3f+iXbLGnthQiZhus5abdWwboZRkgcZAF1FZvunWalxVVM/zl9hRUYq5mYMrC9n1MZOKrFDz7B5ufDG25o"
    "8HOqxQ6XiyjOlcfScBsWvnOySO4nWAozEDMwfFaycqnqwWghdq5gDcrNSOHb1+ogwcy/G1j293KoUrHhcnsfK8PfW7PFAOgq5tMygU1y5Ssh8ZBm8ZOb"
    "MsTsNKWA7wE8NhFqYSh/Dg17gasOe5hrkCyzdZJnC6xBcZ3kL61CH/AJhLQs/vxJHqVaE9hojk3DZmDlAJb9f2HgT5vh7oGrwFq8NkMVs6p4/QiatlP8"
    "PgHUISsY0inpff/acYzIsZEhGde4irV4Tj+2hx8Hhc16kh8mZ+iL5cwVW4wVSKnXmDObFsaqrFSiTM7YhNOfNAjMIS+4F1n75nDBLF5mxoq7EClO54xK"
    "Ihrk18wK5VAD2Cqn8EbjOST78/8iIY9vFoGKt+sjoaCRwRl3TBKdWjBOwh23qIj1a/jJr0xkSWDRZPJsa9hTB9oTmUquvQaSNRJZ0YJC+wlx1nHz5iIa"
    "MGBWhGjEos3HVnGWeiPV4zZo3rpNCR65aaC1vcNlLW0Z117rx4Z+oNZQl3vhLvQedkblw02a0d84RU/hhbarZUbj3aVNYZvXt0uLbzRntVQHrhhEu8E8"
    "vDlesoZ5Rkid0D24BQseO6C1sVGn6A9hHOjJM7C5dQFVNCqwfhOEOjl2ohlb/J/IMr77xjL+V2IZ331jGb+Dy3uPZZwryrQsjJtQ3ZkL0ojCUcZF11j1"
    "j8oPubuWOH2hSK56+4Q7VP45PWS3qrY/vRhw960Y8J7FgLuvUAy4u60YcFoxoFXbaY9FyYe2bP+CIAVnonuW/VQfv9QVtasFLzmKW6zgZUYhh5aeLO9v"
    "k9DoWov39jBLHI9kbcvpHl8Q+P5a2dq7G7J9D6SiSURHokESKn6kbO3dPbO12SU6EdQ7nEL+1dK1bxoa05NKBIy1PdgsBc53dJX++unaNw2ItPMocZfv"
    "eji/8DHytXf3zte+dUxflq+9+2vla+/+MvnauxvytdvUrgqSFO1WiSRjScfBP3FaVA2TLlOVXWFQWT8d4ePMyuep0VcTfCSBW9lFmGFhPmpu9J3HVC1b"
    "h6+c+qgp5KLRnTzfy/hDoVLmCEszPwVaeIkPG9hA33pJnrbnClqRLe+LRwQyFHbFH97+pz+ebjvtPy6Pnm8ax+krux9Pnh9dvRHfvf/19/9+9yX9fvY/"
    "krPcYPF6K3BOXu71s+6HoCtUzJ4r1hHRixIli6Cim2K3XFBlVpbn8HuEAJB0cVye1bisUyYsI04t1S505M1syToccx9CcKbJz2F0MNuhCUofxhEfIW17"
    "uecixeBmtkZyPhDt07bXWy5VfD+zx3T/ueYYeYsz7UTJboPl7dHQI8+YTaXPX0VLTGsRmLs1Dx3XxKtu2CD0wA2y+/9wCnbfTsG3UxAb5O//B6oZPNQ="
)


# STREAM_REF (v11): the Selinos reference line from the frame's north-west end to the Ilıca Deresi confluence, with a
# covered flag per segment. OpenStreetMap "Selinos Çayı" (extract of 28 Jul 2026, traffic package bergama_osm.osm)
# converted with the h01 §0 formula (x = 30037.01 + (lon - 27.18127) x 86,361; y = 32121.57 + (lat - 39.123302) x
# 111,320; +-10-30 m), then moved onto the middle of the survey channel (HIDRO_DERE_SULU / walls; median of 21
# stations, 2 m apart) and thinned to 10 m. Covered = OSM tunnel / culvert ways. Calculated 24 Oct 2026, Thread 5.
STREAM_REF = (
    "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"
)

# MAIN_SPINE (v11): Bankalar Caddesi + Kınık Caddesi (OSM "secondary" ways, same extract and formula, +-10-30 m),
# from Bankalar's south end to Kınık Caddesi east of the frame's K5-K6 reach; used when city_link_results.json has no
# main_spine.
MAIN_SPINE = [[29756.1, 31655.4], [29777.7, 31668.2], [29793.7, 31679.4], [29806.4, 31691.6], [29813.1, 31702.3], [29819.3, 31712.8], [29828.2, 31728.8], [29852.9, 31760.3], [29869.5, 31780.3], [29880.9, 31808.0], [29885.0, 31824.8], [29896.2, 31862.5], [29901.7, 31880.7], [29908.9, 31905.2], [29916.1, 31928.8], [29919.2, 31939.1], [29929.8, 31960.8], [29944.8, 31984.6], [29951.9, 31990.3], [29956.3, 31993.2], [29992.8, 32017.4], [29995.4, 32019.8], [29998.6, 32022.6], [30005.0, 32029.4], [30032.5, 32038.3], [30084.6, 32056.0], [30089.7, 32057.7], [30092.6, 32056.5], [30096.2, 32055.0], [30138.7, 32039.0], [30153.1, 32036.3], [30235.7, 32021.9], [30245.0, 32020.1], [30269.2, 32015.6], [30274.2, 32014.5], [30278.7, 32012.8], [30281.9, 32010.3], [30285.0, 32007.1], [30308.8, 31981.0], [30310.4, 31979.3], [30317.5, 31972.1], [30331.6, 31957.6], [30373.7, 31924.2], [30399.9, 31903.0], [30432.4, 31879.5], [30499.5, 31831.0], [30545.8, 31800.5], [30562.8, 31796.3], [30574.8, 31795.5], [30598.1, 31797.7], [30626.3, 31799.4], [30663.0, 31801.6], [30682.2, 31803.0], [30709.6, 31804.9], [30718.5, 31805.5], [30741.5, 31803.1], [30767.5, 31791.6], [30786.2, 31779.9], [30813.0, 31760.8], [30824.8, 31752.4], [30889.1, 31700.8], [30978.8, 31622.0], [30993.4, 31611.0], [31007.0, 31604.5], [31023.2, 31601.7]]

# CITY_LINK_COPY (v11): the riverside spine, its banks (spine_banks) and stops of bergama_city_link v1.1 (24 Oct 09:15); used when Downloads/Bergama/output/Bergama_city_link_analysis/city_link_results.json is missing.
CITY_LINK_COPY = '{"spine_banks": {"A": "SW", "B": "over", "C": "SW"}, "spine": [{"id": "A", "name": "Ulu Cami to K3 bank walk", "frm": [29846.0, 32278.0], "to": [30037.0, 32122.0], "side_ref": [29844.2, 32313.3], "offset_m": 15.0, "side": "auto", "catch_m": 250.0}, {"id": "B", "name": "Junction over the covered reach", "frm": [30037.0, 32122.0], "to": [30238.7, 31931.2], "side_ref": null, "offset_m": 0.0}, {"id": "C", "name": "Red Hall to Üç Kemer bank walk", "frm": [30238.7, 31931.2], "to": [30294.0, 31792.0], "side_ref": [30245.0, 31962.0], "offset_m": 15.0, "side": "auto", "catch_m": 250.0}], "functions": [{"n": 1, "name": "Bank bazaar", "xy": [29890.4, 32243.6], "stage": null}, {"n": 2, "name": "Parchment and leather workshops", "xy": [30062.0, 32106.0], "stage": null}, {"n": 3, "name": "Junction square", "xy": [30058.0, 32047.0], "stage": null}, {"n": 4, "name": "Red Hall water terrace", "xy": [30238.7, 31931.2], "stage": null}, {"n": 5, "name": "Producers\' market", "xy": [30294.0, 31792.0], "stage": null}, {"n": 6, "name": "Study terraces", "xy": [29941.0, 32200.0], "stage": null}, {"n": 7, "name": "Clean-water classroom", "xy": null, "stage": "entry"}, {"n": 8, "name": "Summer bed events", "xy": null, "stage": null}]}'

# WALK_COPY (v11): river_walks() run on the course survey "Bergama Müdahele Alanları" (17 Oct) with each option's
# cleared buildings from ZONE_COPY, 24 Oct 2026; used only when the open file has no stream or bank layers.
WALK_COPY = (
    "eNrsvUuvNb1y3/ddznjhQfNOepYEmQYBMshA0CCxNUrgALKdieDvnv5fqrjeIx2cDSs6kqx3srhRuy9sNpssFqvq93d/+B/+8O/+7g9/+1/+43/6w7/7q7"
    "/7w//5f/zH/+sP/+4P/8v//IfPH/79//3KJPn84X96/13K+nU+pRz81sLf/ut5fyd/N37bw9/KX/638b+N/+3Pr/L+Vv52/k7+bvwO/nfwv6P/qu/v5O/G"
    "73z4W/nL/07+d/K/6/nV3t/K387fyd+N383/bv5387+b/93873l+9fe38rfzd/6a7+9+n7E+5a1Pfdorr8945fVZv9b7e37tTy1oh1rwpLXgWWpBfWrFNW"
    "utOP5tpff4t5XeI+vBkY3XbI2/A8e39daktoOzevk13t+Gc/vAuX3hXh0tXwdaoL7t8x7zts8rHwfXmQXnTp41edbkWQtvpL4tU/7684f/9X2Pf1XPfJtx"
    "nk+r630jq/31x7LWIHvfVcrKewmI5q81UzRD9oyU9UFZ/5aNStnbGa6Ip76tcL4ux1Pr27tKylahbPwa97ilc9uvcY/bOve9/z3u8Ny3n/Yr4qlvB24jH/"
    "bplI1fZaas6NT2q1zRoqi8x9+78rC3Bzzzjxrg7RvPStnD2769plbLHrfx25+a7/G+vsF7vD3Nt3h7/EbbzfM+xEnZMylbbytatn71Qtn4dXzbt0+wQefb"
    "laN6Y/zah7L3eXrKSqPsyeq9vaqhKhMfhkVvh5Jo/hpxalUbz/dbmjVlhbfd6FqWvS2lc99eliI+xPtdrpIidpT5frEpwwAC0W9u0PkMb1ce7VaEN3g7eb"
    "8VbjzuHRjibb8yvlkcN1fKxvBx0XkGui9l79CyUubj3n/ubDtWD13hivgQ7xuO7vmK1HTvq+v37agm7x+9pmzwTbD5883yDgMfZYr4Bcx3tOy3o7B/zncc"
    "bbc78Q7vAFtHdrvD2r1Db70fj497B4hzu2f1uU/77XeMc9v9LHr1uT3u8XYUyjB8RHfv+lTmO7w9KeIYAFFz22G46pS9LRa3xXAJUXu7rkXvCKHD6v3w3j"
    "GabfdOPHHT44d9Z6TmdlrvtyjZfbEYEiXr2SirvX9SVnNY4HQC0Ts9xWEYlyB7B/s87P0+WeN39NgrZeqfmCb8YBuzHES32Xf5VXmL5507fDlMVux2z8yu"
    "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"
    "6q9/A1vsHqg="
)


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
