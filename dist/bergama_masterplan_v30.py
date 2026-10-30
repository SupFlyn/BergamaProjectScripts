# -*- coding: utf-8 -*-
"""BERGAMA MASTERPLAN v30 (2026-10-30): Group 6's proposal (the zones, their programme and the water links) drawn
as the three alternatives Aras asked for (Q14, 24 Oct), so he can compare them. Merges bergama_masterplan v9 and
bergama_programme_diagrams puzzle v2.3 (MERGE_PLAN.md section 3, M1); both are retired. v11 (Thread 5 of the 22 Oct
batch): the riverside walks, the riverside spine on the real edge, the main spine, the eight stops and the trees.

NEW IN v30: assets_2 high-res silhouettes (Aras 30 Oct 06:11, a feature change): the detailed sections draw the
  PhyloPic trees (plane, ash, olive, stone pine) and crops (maize, tomato) of common/hires.py in each section's own
  colours, roots cut at the ground, uniform scale (needs Data/assets_hires.json; without it the old primitives). p.24
  sections D1 / D2.
    Bergama_masterplan_v30_A.pdf, Bergama_masterplan_v30_A_detail.pdf, Bergama_senses_A3.pdf.
NEW IN v29 (Aras 30 Oct "ok to use kermes photos"; a feature change): p.16 History shows a Kermes photo (DHA, 29 Jun
    2026, from Data/heritage_photos/photos.csv) with its credit line, like the other Commons photos. Output:
    Bergama_masterplan_v29_A.pdf, Bergama_masterplan_v29_A_detail.pdf, Bergama_senses_A3.pdf.
NEW IN v28.1 (bugfix, revision 29 Oct T5 fix pass, Aras 22:08): p.16 Sound and Smell no longer put reeds on the
    open side arms (D2: reed only in the lined basins) or water mint on the open bed (D6: mint only in lined cells);
    "Water mint" left the Smell key. Output: Bergama_masterplan_v28_1_A.pdf, Bergama_masterplan_v28_1_A_detail.pdf.
NEW IN v28 (revision 29 Oct, T4b: WO-T4b-1..3; a feature change, so the next whole number):
  * p.23: the analysis frame in two rows at 1:5,000, every numbered move as a short box on the map with an arrow,
    the riverside walk with its bike lane (Aras 29 Oct 21:04), a small legend in the side column; public sources only.
  * p.24: the 1:1,000 plans in an architectural plan language (lined reed cells, olive rows, paved squares, crowns at
    true width, walk + bike lane, stepping stones, footbridge decks, changed roads) and under each its section, D1 on
    the W1 line and D2 on the W3 line, from the level table and the survey's heights, zone lines above, people.
  * The open ground page (mp_max_area) and r28_open_ground.json are gone (p.22 merged into p.06, D1 a). The shared
    modules (levels, basemap, section parts, plants, icons) are included. Output: Bergama_masterplan_v28_A.pdf,
    Bergama_masterplan_v28_A_detail.pdf, Bergama_senses_A3.pdf.

NEW IN v27 (MIRAQUA 28 Oct, booklet revision v4; a feature change, so the next whole number):
  * p.23 masterplan: one strip of the whole analysis frame at 1:10,000 (G7), with the study-area outline (G8);
    markers coloured by group, a list under the strip by group (number, name, one line); the reasons and sources go
    to the booklet's sources page (plan_sources); the areas left as they are get a letter (P23.1-P23.3, G4).
  * p.21 open ground: the same strip and scale, its own colours, the study outline; one frame figure (150.52 ha,
    cells inside the frame only, G10), and the split adds up to it. Writes cached/bergama_masterplan/
    r28_open_ground.json for the site board's filter sheet (D1; the site board runs after the masterplan).
  * p.24 1:1,000 plans redrawn in the programme-diagram language: soft fade-out fields in the shared zone colours,
    one bold title per field with p.16's plants in small grey, a dot-and-colour legend, a faint grey survey, the study
    outline; the water route 1-4 as one line with arrowheads and numbered dots and a route key; levels only at the
    channel cuts (bed, Q100, Q500); plant codes, band letters, flood bands, spot heights, step sketches and the ochre
    rings and icons removed (P24.1-P24.5, F11).
  * NEW sheet Bergama_senses_A3.pdf "The senses and the water" (S1): six strips of the analysis frame at 1:20,000:
    zones, feeling, sound, smell, encounters and history, each with the study outline and the zone fields of p.24.
  * Speed: the frame figures take one pass over the grid, the plan is drawn once (no two halves), the detail windows
    need no second survey pass. Output: Bergama_masterplan_v27_A.pdf, Bergama_masterplan_v27_A_detail.pdf,
    Bergama_senses_A3.pdf.

NEW IN v26.2 (bugfix, Aras 28 Oct run: "no-intervention note not placed (no free spot in its area): 2.9 ha tree
  cover ..."): a no-intervention note that finds no free spot on two lines tries again with its reason on two lines
  (split at its comma), about half as wide. Output: Bergama_masterplan_v26_2_A.pdf, Bergama_masterplan_v26_2_A_detail.pdf.
NEW IN v26.1 (bugfix, Aras 27 Oct, booklet Prompt 8: final fault check of p.23, p.25, p.26):
  * m² and m³ are written as a raised small 2 or 3 (0.6 x the size, as wide as the ²/³ glyph, so nothing moves), as
    water board v3.1 does: the unembedded Helvetica's ²/³ glyph was dropped in some viewers ("hm³" read "hm").
  * The 1:1,000 windows (crops dt_upstream, dt_k5) are drawn for the booklet page at 1:1 (bk_w): both fit one row
    at 1:1,000 (194 + 4 + 194 mm = the page's 392 mm); their species are named "English (Turkish)" as the water
    board names them, no Latin (cattail, oak and elm: English only, no Turkish name in the project's sources); a
    species code goes into the legend only when its label is on the window; legend names in sentence case; the
    route's rough volumes (~ m³) say how they are made in the caption; ramps have no outline (proposals soft);
    spot levels, route numbers and the smaller planting labels at 7 pt (they printed at 6.3-6.8 pt at 1:1).
  * Scale bar numbers at 7 pt on p.23, p.25 and p.26 (were 5.7 pt), as the site board's on p.24.
  * The hidden-stream line is drawn with the water, under the buildings and bridges (water never over them), and is
    in a window's legend only when it runs through that window.
  * Callouts: "(h01 P12)" for the place register entry (it read like a page number); "open ground" no longer
    repeated in brackets.
  Output: Bergama_masterplan_v26_1_A.pdf, Bergama_masterplan_v26_1_A_detail.pdf, logs/ KML.

NEW IN v26 (Aras 27 Oct 17:35, booklet Prompt 7: masterplan, old p.15-17):
  * Layer order on every plan: water -> buildings -> bridges -> roads -> proposal -> labels. The stream no longer
    covers trees, bridges or the note numbers; survey bridges (YOL_KOPRU) are drawn. What exists is crisp, what
    we propose is soft (Prompt 7 rule 1): fading fields with haloes, translucent bands, no outlines, no fixed widths;
    the planting gradient in ten fainter steps, on open ground only.
  * The site frame (site_alan) as a very faint line along its edges.
  * Every area the plan leaves untouched (1 ha or more) says why, inside it: "NO INTERVENTION" + homes / heritage
    buildings / buildings and streets (survey building kinds), or the satellite's land cover (ESA WorldCover 2021,
    the site board's copy) and how far it lies from the water through open ground, or that no open way reaches the
    water within 200 m (Corridor.no_go). No data maps private plots, the heritage protection zone or the Q100 extent.
  * The old p.16 "Why each place" is gone: all numbered notes are callouts in the column beside the plan (badge, note,
    its reasons; reasons cut only when the column is full, logged; all in masterplan_results.json "notes").
  * Booklet pages drawn at 1:1 for the A3 page (crops mp_plan and mp_max_area, 392 x 238 mm, scale 1:5,000): both
    halves stacked at the top-left, the legend under them (existing / proposed), the column on the 12-column grid
    from 297 mm, scale bar and north arrow at its foot. The open ground is now at 1:5,000 too, with its figures as
    bars (frame split, by distance from the water, by satellite land cover).
  * Satellite check of the open ground (task 3): no imagery could be opened from the cloud (27 Oct 2026), so each
    press writes logs/bergama_masterplan_open_ground_check.kml: every open area of 0.25 ha or more, numbered OG n,
    those with no plant cover on the satellite first. Areas Aras finds built on go into OPEN_CHECK (02c_corridor.py)
    with the imagery and its date: they leave the open ground and the design, hatched on both maps.
  * Labels: no arrow glyphs (they printed as "?").
  Output: Bergama_masterplan_v26_A.pdf, Bergama_masterplan_v26_A_detail.pdf, logs/ KML.

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

NEW IN v24 (Aras 27 Oct 11:07, booklet v9 p15-16; revision_2026-10-27/PHASE2_SPEC.md; history D1-D12, H1-H7):
  * p15 redone as an ECOLOGICAL CORRIDOR (parts/02c_corridor.py): the whole site frame turned so the water runs left
    to right, two halves at 1:5,000 (crops mp_upstream, mp_downstream), each with a key column. The uses blend as a
    gradient (stepped translucent planting rings from the water, programme rings densest at the hubs: H1), no zone
    fills. Everything is placed by computation on the survey: maximum potential area (open ground, no building, no
    road; own proof panel, crop mp_max_area at 1:10,000), widened stream / reed side arms / kept reaches downstream
    from the open ground beside the bank, terraces on the survey contours upstream, forest corridor and tree-planted
    areas, hub squares (K3, K4, K5 walking hubs with bed sub-hubs and stepping stones; transit hub İstiklal Meydanı +
    Kızıl Avlu, switch MAIN_TRANSIT_HUB), canopied walkway with streamside seats, footbridges where a reach has no
    crossing for 300 m, viewing terrace by a computed sightline to the Trajaneum (H5), H2 hidden-stream line, H4, H6.
    Roads changed or kept from OSM classes and the site board's mark C3, each with its reason; truck route: no data
    (pending). Numbered notes on the map, short notes + stacked reasons (D11, D12) in the key; legend rebuilt.
  * masterplan_results.json gains "movement" (spec §4: roads, routes, truck_route, crossings, hubs with role).
  * p16: the 1:1,000 windows draw the same corridor with every element and species code named; no text block under
    the plan. No personal names on the sheets.
  Output: Bergama_masterplan_v25_A.pdf, Bergama_masterplan_v25_A_detail.pdf.

OLDER: v23 (Aras 26 Oct 07:06, deck review p.18-20; library/_index/revision_2026-10-26.md, R4):
  * No walk lines on any plan (p.19: "We work with zones only"): the bank / street / bed walks are no longer drawn
    on the sheet or the detail windows. They are still computed: masterplan_results.json and the water balance's
    riverside walk area are unchanged.
  * A context line under the scale bar of every panel, inside its booklet crop (global rule 4): upstream (p.18:
    why this plan, what the zones show), downstream (p.19), the upstream detail (the water route) and the K5 detail
    (p.20 right: why the amphibious stream commons sits with Demeter's Garden: what the two do together, why at K5,
    with the K5 cut's Q500 level from CUT_AT). Texts in MP_NOTE / dt_note (02b_detail.py). The detail windows give
    up the lines' height so each crop keeps the booklet frame's size and 1:1,000.
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

VERSION = "bergama_masterplan v30 (2026-10-30)"
SHORT = "v30"
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
OUT_NAME = "Bergama_masterplan_v30_{}.pdf"     # v19: one sheet per option
DETAIL_NAME = "Bergama_masterplan_v30_{}_detail.pdf"   # v21: the 1:1,000 detail sheet
LOG_NAME = "bergama_masterplan_log.txt"
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

RESULTS_NAME = "masterplan_results.json"   # v11: read by the water balance (riverside_walk_m2)
BAKE_ROOT = "MP11"                    # Rhino layer of the bake (rhino_bake = True)
BAKE_GAP = 0.10                       # gap between baked sheets and to the rest of the file (x the sheet's width)
OPTION_TEXT = {"A": u"OPTION A · organic only where the project meets the water",
               "B": u"OPTION B · no organic forms"}
ALT_TEXT = {1: u"MASTERPLAN · PROGRAMME"}   # v19: the one sheet

# working area key (survey layer, data key only), stage / place name on the drawing (Q16), idea (CONTEXT §4)
CALISMA_LAYER = "calisma_alan"
SITE_LAYER = "site_alan"                              # v15: analysis range = extent of alternative 3
SITE_COPY = [(29388.015, 32540.503), (31220.325, 30364.153), (31625.069, 30704.915), (29792.759, 32881.264)]   # v15: site_alan of Bergama_Altlik.3dm (rectangle 2,845 x 529 m, 25 Oct 08:25)
CLOSE_GAP = 5.0                                   # v12: m, an open outline closer than this counts as closed
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
# the common piece where the functions of a working area meet: name + what it gathers. A design reading of the
# sourced words above (Aras 19:27, campus reference), not data; edit freely.
HUB = {"calisma_alan[0]": (u"WATER AND HERITAGE COMMONS", [u"COLLECT", u"CLEAN", u"HOLD", u"K4 BRIDGE", u"PLAZA"]),
       "calisma_alan[1]": (u"AMPHIBIOUS STREAM COMMONS", [u"K5 BRIDGE", u"WATER", u"GIVE BACK", u"WALK", u"GREEN"])}
# v12: v11's four commons merged per part (WATER + HERITAGE; AMPHIBIOUS + RIVER), their words joined
# word-size factor per zone = how much it carries the working area's idea (three_ideas.md); a design reading.
# Upstream entry "Collect, clean and hold": the reed basins clean and the terraces hold; the spillway returns; the
# walk serves. K4 / K5 "Amphibious heritage threshold": the bed is the amphibious core, the terrace its edge, the dry
# top the view. Downstream end "Give back": the riverside planting is the idea.
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
        if s and any(ch in SUP for ch in s):             # v26.1: m² / m³ as a raised small digit (see SUP)
            runs = sup_runs(s)
            ws = [text_w(t, size * (SUP_K if up else 1.0), bold) for t, up in runs]
            x -= {"L": 0.0, "C": sum(ws) / 2.0, "R": sum(ws)}[align]
            for (t, up), w_ in zip(runs, ws):
                self.items.append(("text", t, x, y + (size * SUP_UP if up else 0.0), size * (SUP_K if up else 1.0),
                                   color, bold, "L", halo))
                x += w_
        elif s:
            self.items.append(("text", s, x, y, size, color, bold, align, halo))

    def clip(self, rings):
        self.items.append(("clip", rings))

    def unclip(self):
        self.items.append(("unclip",))

    def clipline(self, rings, pts, stroke, lw, alpha=None):
        """A line drawn only inside rings (the verge band inside a zone)."""
        if len(pts) >= 2:
            self.items.append(("clipline", rings, pts, stroke, lw, alpha))


# v26.1 (Aras 27 Oct, Prompt 8; water board v3.1's fix for "hm³ renders as hm"): ² and ³ are drawn as the digit at
# 0.6 x the size, raised 0.28 x the size (the digit is then as wide as the ²/³ glyph, 333/1000): the unembedded
# Helvetica's ²/³ was missing in some viewers
SUP = {u"²": u"2", u"³": u"3"}
SUP_K, SUP_UP = 0.6, 0.28


def sup_runs(s):
    """v26.1: s cut into (text, raised) runs at ² and ³, which become a plain 2 or 3"""
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
    font = pdf_fonts(add, ("R", "B"))                     # G2/G3 28 Oct: Arial embedded (common/pdf_fonts.py)
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
            role = ROLE_OF[path.split("::")[-1]]
            out.setdefault(role, []).append(P)
            if role in ("contour", "contour10"):          # v28: its height, for the p.24 sections' ground
                out.setdefault("contour_z", []).append((P, g.PointAtStart.Z))
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
            for nm in ("bergama_zone_base_v10.py", "bergama_zone_base_v9.py", "bergama_zone_base_v8.py", "bergama_zone_base_v7.py", "bergama_zone_base_v6.py", "bergama_zone_base_v5.py",
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


# ================================================================ the design of one option (v2.3)
def link_type(tag):
    """The meaning of an INT_LINK layer or user text link from its words (LINK_TYPES), or None."""
    tw = set(re.split(r"[^a-z0-9]+", tag.lower()))
    for k_, d_ in LINK_TYPES.items():
        if tw & set(d_["words"]):
            return k_
    return None

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
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != {'LEVELS': 'a217c1d07ff06bcb3cd55255c619aa7c', 'ZONE_COPY': '7c7d4a4a21af391460ac0701ae5e3902', 'STREAM_REF': '6462357102432c243b7a34f595c055c7', 'WALK_COPY': '1cd13819bdb905317ae04d7b1461f8dc', 'LC_EMBED': '240a8d1b17473e2447889cf7c9a0864b'}.get(name):
        raise RuntimeError("Data file bergama_masterplan_data.py is not the one made with this script version (part " + name +
                           "): copy it again from the same run kit as the script")
    exec(compile(b_, "bergama_masterplan_data.py:" + name, "exec"), globals())


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


# species / crops with a high-res silhouette (hires.py, assets_2 30 Oct): same genus stand-ins per GAPS.md A
PLA_HIRES = dict(plane="plane", ash="ash", olive="olive", stone_pine="stone_pine", maize="maize", tomato="tomato")


def _pla_hr(key, x, gy, h, w, c, seed):
    """the high-res silhouette in the species' own fill (this section's colours, paler beyond), mirrored on odd
    seeds; None -> the primitive"""
    return hr_side(PLA_HIRES.get(key), x, gy, 1.0, h, w, c["fill"], facing=-1 if seed % 2 else 1) if key in PLA_HIRES \
        else None


def pla_section(key, x, gy, k, h_m=None, crown_m=None, beyond=False, seed=0, hires=True):
    """A species in section at true size: ground at (x, gy) page mm (gy may be a function of x). hires: the high-res
    silhouette where the library has one (detailed sections); False for sketchy drawings and diagrams."""
    sp = _pla_get(key)
    h, w = _pla_size(key, sp, h_m, crown_m)
    g, c = gy(x) if callable(gy) else gy, _pla_cols(sp, beyond)
    sh = _pla_hr(key, x, g, h * k, w * k, c, seed) if hires else None
    return sh or _pla_sec(sp["form"], x, g, h, w, k, c, seed)


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
        c = _pla_cols(PLA_SPECIES["olive"], beyond)
        return _pla_hr("olive", x, gy, h * k, w * k, c, i) or _pla_sec("gnarled", x, gy, h, w, k, c, i)
    H, R = h * k, w / 2.0 * k
    c = _pla_cols(dict(colours=_pla_c(SEC["grass"])), beyond)
    sh = _pla_hr(crop, x, gy, H, 2.0 * R, c, i)
    if sh:
        return sh
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
# ---- high-res silhouettes (assets_2, Aras 30 Oct 2026): PhyloPic trees, crops and animals as filled vector rings,
# drawn only in the detailed (true-to-cut) sections and recoloured there with that section's own colours. The
# sketchy sections and diagrams keep their own drawing (an abstract set comes later).
# Library: Downloads/Bergama/Data/assets_hires.json (run kit Data/), built in the cloud by
# tools/assets2/build_hires.py from revision_2026-10-29/assets_2_2026-10/ (roots cut at the ground, height 1.0,
# ground / feet at y = 0, y up). Each part = one keyhole ring for the even-odd fill + its outer and hole rings for
# outlines. Uniform scale only (never stretched). No JSON on the PC -> callers fall back to their own drawing.
# The sources are listed once on the booklet's Sources page under ASSETS (Aras 30 Oct 06:20), never beside a drawing.

HR_LOG = []
_HR_LIB = {}


def hr_library():
    """the high-res library (dict key -> asset) or {} when Downloads/Bergama/Data/assets_hires.json is missing"""
    import os as _o
    import json as _j
    if "lib" in _HR_LIB:
        return _HR_LIB["lib"]
    lib = {}
    p = _o.path.join(_o.path.expanduser("~"), "Downloads", "Bergama", "Data", "assets_hires.json")
    if _o.path.exists(p):
        try:
            with open(p, "r") as fh:
                lib = _j.load(fh).get("lib", {})
            HR_LOG.append(u"High-res assets: %d from %s" % (len(lib), p))
        except Exception as ex:
            HR_LOG.append(u"High-res assets: %s unreadable (%s); own drawings used" % (p, type(ex).__name__))
    else:
        HR_LOG.append(u"High-res assets: Data/assets_hires.json not found; own drawings used")
    _HR_LIB["lib"] = lib
    return lib


def _hr_draw(a, T, fill, edge, lw):
    out = []
    for part in a.get("parts", []):
        out.append(("poly", [T(q) for q in part["fill"]], fill, None, 0.0))   # lw 0.0 marks a high-res fill
        if edge:
            for r in part["lines"]:
                pts = [T(q) for q in r]
                out.append(("line", pts + [pts[0]], edge, lw))
    return out


def hr_side(key, x, gy, k, h_m, w_m=None, fill="000000", edge=None, lw=0.08, facing=1):
    """house shapes of one high-res plant: ground at (x, gy) page mm, h_m tall (m), k page mm per m; when w_m is given
    and the silhouette would be wider, the whole drawing is scaled down until it is w_m wide (uniform). facing -1 =
    mirrored. None when the library or the key is missing."""
    a = hr_library().get(key) if key else None
    if not a or not h_m:
        return None
    s = h_m * k
    wd = float(a["x1"] - a["x0"])
    if w_m and wd * h_m > w_m:
        s = w_m / wd * k
    f = -1.0 if facing < 0 else 1.0
    return _hr_draw(a, lambda q: (x + f * q[0] * s, gy + q[1] * s), fill, edge, lw)


def hr_fauna(key, x, y, size, fill="000000", edge=None, lw=0.05, facing=1, foot=None):
    """house shapes of one high-res animal in a size-mm square centred on (x, y), head to the left (facing -1: to the
    right, PhyloPic draws most animals facing left; the library's face tells which way each one looks); with foot
    the feet sit foot x size below y (the pictograms' ground rule), otherwise the animal is centred. None when
    missing."""
    a = hr_library().get(key) if key else None
    if not a:
        return None
    wd = float(a["x1"] - a["x0"])
    s = size / max(wd, 1.0)
    cx = (a["x0"] + a["x1"]) / 2.0
    f = (-1.0 if facing < 0 else 1.0) * (-1.0 if a.get("face", 1) < 0 else 1.0)
    y0 = y - foot * size if foot is not None else y - s / 2.0
    return _hr_draw(a, lambda q: (x + f * (q[0] - cx) * s, y0 + q[1] * s), fill, edge, lw)


def hr_sources():
    """one line per asset used from the library, for the booklet's Sources page (ASSETS)"""
    out = []
    for key, a in sorted(hr_library().items()):
        out.append(u"%s silhouette, %s, PhyloPic (%s), %s" % (a.get("what", key), a.get("author", ""),
                                                              a.get("url", ""), a.get("licence", "")))
    return out
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


# ================================================================ grid and outlines (from the v2.3 puzzle; v24: the
# corridor's grid, Corridor in 02c_corridor.py, uses Grid, trace and smooth; the puzzle itself is gone)
MAX_CELLS = 170000           # grid cells per working area (cell size follows from it, at least 0.5 m)
RIVER_BAND_TONE = ("C4CCB5", "89986A", "3C4733")   # v18: sage, palette reference 89986A (light = mixed 1:1 with white)
RIVER_BAND_NAME = u"PROMENADE"   # v19: one catchy word for Aras's "function/circulation area" (16:39, 16:41)
PIECE_TONE = {"river": ("91ADB4", "5D7F8D", "32525F"), "street": ("CFCCC5", "847E75", "4A3F35"),   # v21: road role
              "park": ("DFEBC0", "A7B67F", "49522B"), "heritage": ("E4CAC9", "AF7474", "4C2528"),
              "building": ("D8D5CC", "B0AC9C", "847E75"), "housing": ("D9CDAE", "BFB08F", "594B2E"),
              "cleared": ("F6F4EE", "B0AC9C", "4A3F35")}


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


def block_size(lines):
    """lines: [(text, size, bold)] -> (w, h)."""
    w = max(text_w(s, sz, bd) for s, sz, bd in lines)
    h = sum(sz * 1.18 for s, sz, bd in lines)
    return w, h


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


def name_of(z, owner):
    for (o_, c_, t_), nm in NAMES.items():
        if o_ == owner and c_ == z["code"] and t_ in (None, z["tier"]):
            return nm
    return z["label"] or z["code"]


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
ROAD_TONE = ("CFCCC5", "847E75", "4A3F35")   # v21: palette v1.4 role "road": light lanes, mid streets, dark main roads
ROAD_LW = (0.22, 0.45)       # v21: street edge, main-road edge, mm (graphic)


# ================================================================ one plan panel (sheet and detail windows)# ---- A3 booklet assets (SCRIPT_STANDARD §8; booklet/ASSET_SPEC.md) ----
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
# ================================================================ v21: the 1:1,000 detail sheet and the booklet crops
# Aras 25 Oct 21:49 on the booklet's 1:1,000 page: "this should add more detail from what we have shown in
# masterplan". The detail sheet shows the two windows of the booklet's C3 page (upstream entry; K5 with Demeter's
# Garden) at 1:1,000 with what the whole plan cannot show, all from the project's data:
#   cuts      at the water board's surveyed channel cuts (the proposal sections stand on them) the bed level and
#             the DSI Q100 / Q500 levels with the width each covers there (CUT_AT); v25: no cut or section lines
#   route     the zone base's water links numbered in the order of the water route (ROUTE), with the areas the
#             script computes from the zone curves (no script computes a storage volume: left out, logged)
#   planting  band letters and species codes of the booklet's verified list (plan page C7 = water board v1.9
#             PLANT_BANDS / SPECIES) on the zones whose wetness tier they belong to (ZONE_PLANTING)
#   levels    survey spot heights (NOKTA_TAKEOMETRI) in the bed and on the bank tops, by the edges river_walks found
#   sketches  (Aras 21:57) terrace steps as a few strokes in the retention terraces and flood terraces, ramps as
#             wedges on the zone base's people-to-the-water links: zones and sketch marks, abstract, no dimensions
# Booklet (CROP_SPEC.md, Aras 21:47): the booklet's drawings are crops of the sheets; blocks.json holds one crop per
# panel (both halves of the masterplan sheet, both detail windows), results.json the frames and places.
# v27 (MIRAQUA 28 Oct, P24.1-P24.5, F11): the windows are drawn by r28_window_panel (parts/02e_r28_detail.py) in the
# fade-out programme language; of the list above they keep the cuts' bed and flood levels (no bands across the
# stream) and the water route with its areas and rough volumes. The planting codes, band letters, survey spot
# heights and sketches are gone (their tables with them).
DT_SCALE = 1000.0
DT_WINDOWS = [  # crop id, old booklet id, working area, sheet title, booklet caption, zone names the window must show
    ("dt_upstream", "c3_a", "calisma_alan[0]", u"UPSTREAM ENTRY · COLLECT, CLEAN, HOLD",
     u"Upstream entry: collect, clean, hold", (u"REED BASINS", u"RETENTION TERRACES", u"SPILLWAY", u"SHADED WALK")),
    ("dt_k5", "c3_b", "calisma_alan[1]", u"K5 BRIDGE · DEMETER'S GARDEN", u"K5 bridge and Demeter's Garden",
     (u"DEMETER'S GARDEN",))]
# CUT_AT: the water board's surveyed channel cuts (water board v1.9 CUTS, proposal sections v4 panels 1-4):
# number, name, centre (survey m) and span (u m, + = left bank looking downstream) from
# research/rain_river_levels/scripts/surveyed_sections/levels2_out.json (24 Oct); bed and DSI Q100 / Q500 levels (m,
# Manning n 0.050) and the width each covers (u from, to) as there (= water board CUTS bed + depth).
CUT_AT = [("1", u"UPSTREAM ENTRY", (29693.022, 32569.176), (-74.5, 85.5), 70.36, (73.35, -29.5, 14.0), (73.66, -30.5, 15.0)),
          ("2", u"K4 BRIDGE", (29959.774, 32264.566), (-21.0, 91.5), 64.77, (67.33, -58.5, 16.5), (67.61, -70.5, 16.5)),
          ("3", u"K5 BRIDGE", (30354.663, 31689.671), (-86.0, 64.5), 55.96, (58.41, -37.5, 12.0), (58.75, -45.5, 12.5)),
          ("4", u"DOWNSTREAM REACH", (30991.856, 31039.404), (-39.5, 26.5), 45.67, (47.72, -29.5, 19.5), (48.0, -30.5, 20.0))]
# The water route at the upstream entry (zone base links, by the zones they join): order and short words
ROUTE = [((None, "WT"), u"INTO {}", 1), (("WS", "WT"), u"FROM {}", 0), (("WT", "WD"), u"TO {}", 1),
         (("WD", None), u"BACK TO THE STREAM", None)]   # (from, to), words, which end's zone they name
ROUTE_SHORT = {u"RETENTION TERRACES": u"TERRACES"}
# v22 (Aras 26 Oct 06:27 "make them have calculated roughly"): rough volume on the water route = zone area x depth.
# Reed basins: 0.46 m, the water depth of EPA's worked example ("water depth = 0.46 meters (1.5 ft)"; vegetated
# depth "a few inches to two feet or more"), EPA 832-F-00-024 Free Water Surface Wetlands, Sep 2000. Terraces (Aras
# 06:32 picked): the water over them in the DSI Q100 flood = Q100 level at the nearest cut - (bed + TERRACE_UP).
STORE_DEPTH = {"WT": 0.46}
TERRACE_UP = 1.0                     # terrace level above the bed, m (the project's flood rule: "Terrace +1 m")
DT_CUT_ROOM = (70.0, 30.0)           # v28: m from the section's stream axis to the window's left/right and top/bottom edges


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
        cid = P24_CUTS.get(bid, (None,))[0]               # v28 (WO-T4b-3): the section's cut keeps DT_CUT_ROOM to the
        if cid:                                          # window's sides, so its section reaches both banks' land
            a_ = CUT_AT[{"W1": 0, "W3": 2}[cid]][2]
            mx, my = max(0.0, Wm / 2 - DT_CUT_ROOM[0]), max(0.0, Hm / 2 - DT_CUT_ROOM[1])
            c = (min(max(c[0], a_[0] - mx), a_[0] + mx), min(max(c[1], a_[1] - my), a_[1] + my))
        out.append({"id": bid, "old": old, "key": key, "title": title, "caption": cap,
                    "R": (c[0] - Wm / 2, c[1] - Hm / 2, c[0] + Wm / 2, c[1] + Hm / 2)})
    return out


def crop_legend(keys, alpha):
    """v24: a panel's legend for its booklet crop (drawn samples as colours + plain names): the corridor's symbols
    it draws (LEG_BOOK). v27 (MIRAQUA 28 Oct, P24.4): the 1:1,000 windows carry their own (sh.r28_leg, 02e)."""
    out = []

    def add(kind, colour, label):
        if all(e["label"] != label for e in out):
            out.append({"kind": kind, "colour": colour, "label": label})
    for key, nm, f in LEGEND_V24:
        if ("v24", key) in keys and key in LEG_BOOK:
            add(LEG_BOOK[key][0], LEG_BOOK[key][1], nm.lower() if nm.isupper() else nm)
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
    res = {"script": "bergama_masterplan_v28.py", "version": VERSION, "option": "A", "frames": {},
           "labels_not_drawn": {}, "places_xy": dict((k_, [round(v[0], 1), round(v[1], 1)])
                                                     for k_, v in sorted(plc.items()))}
    wd = dict((w["id"], w) for w in wins)
    drop = [r"^1:[\d,.]+$"]                               # the sheet's scale text: the booklet prints its own
    for pdf, sh, scale in sheets:
        for key, rc, p in sh.panels:
            bid, old, cap = p.bid
            sc_ = getattr(p, "scale", scale)              # v24: each panel its own round scale
            leg_ = crop_legend(p.pleg, _ALPHA[0]) if getattr(p, "pleg", None) else []   # v24: p15 halves: in the crop
            if getattr(p, "r28_leg", None):               # v27 (MIRAQUA 28 Oct, P24.4): the windows' dot legend
                leg_ = p.r28_leg
            bk.crop(bid, os.path.basename(pdf), rc, caption=cap, scale_den=sc_, legend=leg_, drop=drop)
            if getattr(p, "plan_sources", None):          # v27 (MIRAQUA 28 Oct, P23.2, N2): what the p.23 list no
                bk.d["plan_sources"] = res["plan_sources"] = p.plan_sources   # longer prints, for the sources page
            if bid in ("mp_plan", "mp_max_area", "dt_upstream", "dt_k5"):   # v26: drawn for the booklet page at 1:1
                bk.d["blocks"][bid]["bk_w"] = round(rc[2] - rc[0], 3)   # (its width there); v26.1: the 1:1,000
                # windows too (194 + 4 + 194 mm = the page's 392 mm), so p.26 prints them at 1:1,000 in one row
            fr = {"crop": bid, "scale_den": sc_, "w_mm": round(rc[2] - rc[0], 1), "h_mm": round(rc[3] - rc[1], 1)}
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
# ================================================================ v24: the ecological corridor (p15 + p16 redo)
# Aras 27 Oct 11:07 (revision_2026-10-27/PHASE2_SPEC.md §6 "p15", "p16"; history decisions D1-D12, H1-H7):
#   * the uses blend like a GRADIENT and read as an ECOLOGICAL CORRIDOR: stepped translucent rings of planting from the
#     water outward (denser at the water), and stepped translucent programme rings round the bridge hubs (densest at
#     the hubs, thinning between them: H1). No zone-by-zone fills.
#   * the empty surroundings are developed inside the MAXIMUM POTENTIAL AREA (spec §5 q1 default): the open ground of
#     the site frame (site_alan) with no survey building (BINA_*) and no survey road (YOL_SOSE / YOL_BORDUR, ROAD_BUF_M
#     either side of an edge line, as the v2.3 puzzle grows a street), on a CELL_M grid; shown as its own proof panel
#     (crop mp_max_area).
#   * every design move is computed from the survey / data, never placed by hand, and carries its stacked reasons
#     (D11) naming only analyses that are in the booklet (D12): max area panel, survey contours, water board cuts
#     (Q100 / Q500, p12) and chain (p13), the site board's edge plan (p5, bridges K1-K6, marks C1-C6), OSM road classes
#     (site board p6), history cards h01-h03 (H1-H7).
#   * notes on the map are numbered badges (measured, collision-checked, leader when moved) with the short notes and
#     their reasons in the key column beside the plan: no text overlaps another. v27 (MIRAQUA 28 Oct, P23.1-P23.2): the
#     badges in their group's colour, the list by group under the strip, the reasons on the sources page (02d).
# The proposal's movement (roads, truck route, crossings, hubs) is written to masterplan_results.json key "movement"
# (spec §4) for the site board's p6 proposal map.
MP_SCALE = 10000.0           # v27 (MIRAQUA 28 Oct, G7): the whole frame as ONE strip, 284.5 x 52.9 mm (1:5,000: 569 mm)
CELL_M = 3.0                 # grid of the max potential area, m
ROAD_BUF_M = 4.5             # a surveyed carriageway edge marks road this far either side (= STREET_M), m
DMAX_M = 200.0               # distance from the water computed this far, m
# v26 (Prompt 7 rule 1, proposals soft): ten fainter steps instead of five, so the gradient fades out with no edge
ECO_BANDS = (4.0, 8.0, 13.0, 18.0, 25.0, 32.0, 41.0, 50.0, 62.0, 75.0)   # m from the water (graphic, design reading)
ECO_ORGANIC = 18.0           # rings up to this far from the water are organic, further out faceted (form rule)
HUB_RINGS = (25.0, 45.0, 65.0, 85.0, 105.0, 125.0, 150.0, 175.0)        # m round a hub (H1; graphic, design reading)
ECO_A, HUB_A = 0.075, 0.085  # v26: opacity of one step (the steps add up: densest at the water / at the hubs)
HUB_CORRIDOR = 120.0         # programme rings stay within this far of the water, m
HUB_SQ_M = 28.0              # a hub square = open ground within this far of the bridge anchor, m (design value)
FOREST = (6.0, 32.0, 110.0, 9.0)     # forest corridor: from, to m from the water, at least m from a hub, spacing m
TREES = (32.0, 60.0, 70.0, 18.0)     # tree-planted area: the same (design values)
SEAT_STEP = ((100.0, 25.0), (220.0, 50.0))   # streamside seats: within m of a walking hub, one every m of walkway
FOOT_GAP_M = 300.0           # a reach this long without a crossing gets a footbridge (design value)
WIDEN_MIN, BRANCH_MIN, KEPT_MAX, FREE_MAX = 20.0, 55.0, 5.0, 90.0   # open ground beside the bank, m (design rules)
WIDEN_K, WIDEN_CAP, ARM_K, ARM_CAP = 0.4, 20.0, 0.7, 45.0          # widened edge / side arm: share of it, cap m
MOVE_RUN_M = 30.0            # shorter runs of one move are dropped, m
KEPT_SPACE_M = 150.0         # "kept" badges at least this far apart, m (graphic)
TERRACE_D = (4.0, 70.0)      # upstream terraces: contours this far from the water, m
# v26 (Prompt 7 tasks 2 and 4): the masterplan and the open ground are each ONE crop drawn for the booklet page at
# 1:1 (bergama_booklet panel area 392 x 238 mm); v27 (MIRAQUA 28 Oct, G7): each ONE strip at the top-left, the legend
# beside it from COL_X, the scale bar under it, the list / figures under them (parts/02d_r28_ground.py).
BK_W, BK_H = 392.0, 238.0    # mm: the booklet's panel area (A3 less margins and the caption line)
COL_X = 297.0                # mm from the panel's left edge: booklet grid column 10 (14 + 9 x 33 mm on the page)
KEY_MIN = 2.47               # key text floor, mm (7 pt); v27: KEY_TS (2.6) unused, removed
NI_BLOCK, NI_SHARE, NI_MIN_HA, NI_BUILT = 15.0, 0.9, 1.0, 0.4   # v26: no-intervention regions: block m, share of a
#   block the plan leaves untouched, smallest region ha, built share (buildings + streets) that makes it "built"
NI_ROAD_M = 6.0              # v26: a changed road or the hidden-stream line touches this far either side, m
# v26 (Prompt 7 task 3): the satellite check of the open ground. No imagery could be opened from the cloud where
# this version was written (Esri, Google, EOX and Sentinel Hub refused, 27 Oct 2026), so it is still to do: each
# press writes the open ground's outlines to logs/bergama_masterplan_open_ground_check.kml for Google Earth (and by
# number, in survey m, to cached/bergama_masterplan/open_ground_check.json). When Aras has checked them, fill in the
# imagery's name and date and the outlines of ground built on since the survey (survey m: the JSON's rings of the
# areas he names): they leave the open ground everywhere (the design moves with them) and show hatched on both
# maps; the caption then names the imagery and its date.
OPEN_CHECK = dict(imagery=None, date=None, built=[])
BT_CODE = {"housing": 1, "building": 2, "heritage": 3, "shed": 4}   # v26: building kind per cell; 5 = built since
LC_KEYS = ("farmland", "trees", "shrub", "grass", "orchard")        # v26: ESA WorldCover 2021 as the site board keys it
PLACE_TS = 4.3               # place names on the plans, mm (12.2 pt)
LAB_TS = 2.6                 # labels on the 1:1,000 windows, mm
BADGE_R, BADGE_TS = 1.95, 2.5
DT_PLAN = (194.0, 120.0)     # p.24 windows, mm at 1:1,000: one row, 194 + 4 + 194 = 392 mm (bk_w); v28: 120 mm high so
#                              each crop holds its plan and its section (D1, D2) under it in the 238 mm panel
ECO_COL, HUB_COL = "6F8A4E", "D9A35E"        # palette "tree" family darkened / "centre" family (graphic)
WATER_COL, WET_COL = COL["river"], "B7CFC8"
SQ_FILL, SQ_EDGE = "F4E6CC", "9C7440"
ROAD_CHANGE_COL = {"calmed": "B5832F", "pedestrian": "8B3A3F", "shared": "7F5B7B", "kept": "847E75",
                   "relocated": "C2603A", "later": "633131"}

# Bridges over the Selinos (site board BRIDGES_K = CONCEPT_RECORD 2.1, survey m)
BRIDGES_K = [("K1", (29628.35, 32630.87)), ("K2", (29604.93, 32622.02)), ("K3", (30037.01, 32121.57)),
             ("K4", (29846.40, 32277.71)), ("K5", (30293.63, 31792.25)), ("K6", (30646.94, 31251.65))]
# Hubs (D2, D3, D10; h03 Q1 + Aras 27 Oct 12:05 "Both"): id, bridge key (spec §4), anchor (survey m: H1 bridge
# anchors h01 §5 P06 P08 P09 P30; İstiklal = P16 label; Kızıl Avlu = P02), its OSM bus stop (name, survey m by the
# h01 §0 formula from bergama_osm.osm of 28 Jul 2026, +-10-30 m), river sub-hub in the bed (D10).
MAIN_TRANSIT_HUB = (u"İstiklal", u"Kızıl Avlu")   # Aras 12:05: the town lines stop here; switch: hub ids
HUBS = [(u"K4", "K4", (29846.0, 32278.0), u"Camikebir Caddesi", (29841.0, 32243.7), True),
        (u"K3", "K3", (30037.0, 32122.0), u"Tabak Köprüsü", (30017.4, 32106.8), True),
        (u"İstiklal", u"İstiklal", (29990.0, 32030.5), u"İstiklal Meydanı", (29995.4, 32019.8), False),
        (u"Kızıl Avlu", u"İstiklal", (30245.0, 31962.0), u"Kızıl Avlu", (30245.0, 32020.1), False),
        (u"K5", "K5", (30294.0, 31792.0), u"Üç Kemer Köprüsü", (30296.4, 31696.7), True),
        (u"K6", "K6", (30647.0, 31252.0), u"Bergama Sanayi", (30575.0, 31232.4), False)]
HUB_NAME = {u"K4": u"K4 · ULUCAMİ ÖNÜ", u"K3": u"K3 · TABAK", u"İstiklal": u"İSTİKLAL MEYDANI",
            u"Kızıl Avlu": u"KIZIL AVLU", u"K5": u"K5 · ÜÇ KEMER", u"K6": u"K6"}
# Places named on the plans (h01 §5 register; survey labels, m): Ulu Cami P05, Tabaklar Hamamı P07, Tabakhane E07
PLACES = [(u"ULU CAMİ", (29844.2, 32313.3)), (u"TABAKLAR HAMAMI", (29890.4, 32243.6)),
          (u"TABAKHANE", (30062.0, 32106.0)), (u"HARAP CAMİİ", (30435.7, 31584.6))]
# H5 (h03 Q3): Trajaneum centroid 39.1327803, 27.1832652 (OSM) -> survey by the h01 §0 formula (+-10-30 m)
TRAJANEUM = (30209.0, 33177.0)
ROMAN_WALL = (29800.2, 32362.3)      # H6: "Eski Kozak Yolu" label, Roman complex with ~120 m bank wall (P12, E10)
CRAFT_XY = (30062.0, 32106.0)        # H3: "Eski Tabakhane Sk." label (E07) = city link stop 2 (workshops)
# Roads (OSM bergama_osm.osm, 28 Jul 2026, highway class and name; survey m by the h01 §0 formula, +-10-30 m). Each
# change is read from data: the OSM class (site board p6 driving map), the site board mark C3 "K4: monument and
# traffic" (p5), and the OSM chainages of the car crossings along the stream (calculated). No traffic count exists
# on these streets (card t01: KGM counts only on 35-04, 35-05, D240): no "relocated" road.
ROADS = [
    dict(name=u"Bergama - Kozak Yolu", change="kept", note=u"kept: through road to Kozak",
         proof=u"OSM secondary (one 11.9 km way)",
         xy=[[29668.6, 32896.0], [29643.3, 32796.0], [29633.4, 32739.9], [29627.0, 32698.6], [29625.9, 32675.0],
             [29627.8, 32656.7], [29636.9, 32624.0], [29648.9, 32599.2], [29667.9, 32549.9], [29687.1, 32517.5],
             [29726.2, 32490.9], [29760.3, 32463.9], [29772.4, 32442.5], [29775.9, 32394.5], [29772.1, 32343.5],
             [29773.3, 32313.3], [29777.8, 32297.2], [29792.2, 32271.3]]),
    dict(name=u"Cami Kebir Caddesi + Ulucami Köprüsü", change="calmed", note=u"calmed: monument meets traffic at K4",
         proof=u"edge plan mark C3; OSM secondary",
         xy=[[29854.5, 32289.9], [29843.7, 32252.8], [29873.2, 32232.0], [29934.1, 32225.0], [29960.0, 32218.3],
             [29976.9, 32203.2], [30015.5, 32111.3]]),
    dict(name=u"Tabak Köprüsü", change="calmed", note=u"calmed: hub square and workshops at K3",
         proof=u"H1, H3 (h01/h02); OSM secondary", xy=[[30023.7, 32110.3], [30052.5, 32130.6]]),
    dict(name=u"Kınık Caddesi", change="kept", note=u"kept: main spine, shops",
         proof=u"city link main spine; OSM secondary",
         xy=[[29992.8, 32017.4], [30005.0, 32029.4], [30032.5, 32038.3], [30089.7, 32057.7], [30138.7, 32039.0]]),
    dict(name=u"Kızıl Avlu Çıkmazı", change="pedestrian", note=u"pedestrian: dead end over hidden stream",
         proof=u"OSM living_street, dead end; H2",
         xy=[[30144.3, 31986.1], [30123.6, 31988.0], [30099.4, 31997.7]]),
    dict(name=u"Üç Kemer Köprüsü", change="pedestrian", note=u"pedestrian: car crossings 190-230 m away",
         proof=u"OSM residential; OSM chainage of Kızıl Avlu Cd / next bridge (calc); H1",
         xy=[[30277.2, 31777.9], [30314.7, 31804.7]]),
    dict(name=u"Adnan Menderes Bulvarı", change="kept", note=u"kept: regional road İzmir-Soma at K6",
         proof=u"OSM primary; h02 E12", xy=[[30609.3, 31239.0], [30695.5, 31266.2]]),
    dict(name=u"bank street, lower reach", change="shared", note=u"shared: local bank street, stream widens",
         proof=u"OSM residential; open ground",
         xy=[[30713.4, 31260.3], [30730.6, 31243.9], [30800.4, 31198.6], [30862.6, 31166.0], [30923.9, 31135.4],
             [30975.8, 31095.9], [31012.3, 31057.8], [31062.1, 30994.1], [31143.6, 30884.2], [31192.5, 30817.8],
             [31216.8, 30791.6]])]
# Aras 12:05: a town-line extension to K4 as a PROPOSED LATER STEP, on the existing streets İstiklal stop -> Kınık Cd
# -> Cami Kebir Cd -> K4 stop (OSM ways 370936581, 1222988932, 371130159, as above)
TOWN_LINE = dict(name=u"town bus line to K4", change=u"proposed later: bus line 651 to K4",
                 note=u"later step: town line on to K4", proof=u"h03 Q1 (town lines stop at İstiklal); K4 stop 35 m",
                 xy=[[29995.4, 32019.8], [30005.0, 32029.4], [30032.5, 32038.3], [30084.6, 32056.0], [30089.7, 32057.7],
                     [30075.0, 32066.0], [30041.0, 32089.8], [30017.4, 32106.8], [30015.5, 32111.3], [29976.9, 32203.2],
                     [29960.0, 32218.3], [29934.1, 32225.0], [29873.2, 32232.0], [29841.0, 32243.7]])


class _All(object):
    """v24: every cell of the corridor grid is valid (Grid's 'near' test)."""

    def within(self, x, y):
        return True

    inside = within


def landcover_grid(G, uvP, V, warn):
    """v26: ESA WorldCover 2021 per grid cell: 1 + the index of its class in LC_KEYS, 0 = none of them (built-up,
    bare ground or water on the satellite). From the site board's built-in copy (LC_EMBED, survey m), each class
    filled even-odd (its rings keep the pixel boundaries, holes included)."""
    lc = bytearray(G.nx * G.ny)
    try:
        d = json.loads(zlib.decompress(base64.b64decode("".join(LC_EMBED))).decode("utf-8"))
    except Exception as ex:
        warn.append(u"land cover (ESA WorldCover 2021) not read ({}): no satellite reasons".format(ex))
        return lc
    for code, key in enumerate(LC_KEYS, 1):
        tog = bytearray(G.nx * G.ny)
        for r_ in d.get("rings", {}).get(key, []):
            if len(r_) >= 3 and hit(bbox(r_), V.bb):
                for n in G.poly_cells(uvP(r_)):
                    tog[n] ^= 1
        for n in range(len(tog)):
            if tog[n]:
                lc[n] = code
    return lc


class Corridor(object):
    """v24: the survey and the design of the whole site frame, computed once a press, in world (survey) m.
    F per grid cell: 0 open, 1 building, 2 road, 3 stream bed / water line. Dst: distance from the water through open
    ground (m). Everything the panels draw: bands, hub rings and squares, moves, terraces, trees, seats, crossings,
    roads, notes (numbered) and the movement record."""

    def __init__(self, V, survey, CL, D, spots, warn):
        self.V, self.D, self.CL, self.warn, self.spots = V, D, CL or {}, warn, spots or []
        G = self.G = Grid((V.u0, V.v0, V.u1, V.v1), _All(),
                          int((V.u1 - V.u0) * (V.v1 - V.v0) / (CELL_M * CELL_M)) + 1)
        N = self.N = G.nx * G.ny
        F = self.F = bytearray(N)
        uvP = lambda P: [V.uv(p) for p in P]
        inF = lambda P: any(V.inside(p[0], p[1]) for p in P)
        self.bld = {}
        bt = self.bt = bytearray(N)                                      # v26: building kind per cell (BT_CODE)
        for role in ("building", "housing", "heritage", "shed"):          # buildings: whole footprints (faces)
            polys = [P for P in survey.get(role, []) if inF(P)]
            self.bld[role] = faces(polys, max_area=30000.0) if polys else []
            for Fc in self.bld[role]:
                for n in G.poly_cells(uvP(Fc)):
                    F[n] = 1
                    bt[n] = BT_CODE[role]
        self.built_since = [ring(P) for P in OPEN_CHECK.get("built") or [] if len(P) >= 3]   # v26: satellite check
        for P in self.built_since:
            for n in G.poly_cells(uvP(P)):
                F[n] = 1
                bt[n] = 5
        self.bridges = [P for P in survey.get("bridge", []) if inF(P)]   # v26: survey bridges (YOL_KOPRU), drawn crisp
        self.lc = landcover_grid(G, uvP, V, warn)                        # v26: ESA WorldCover 2021 per cell
        self.roads = [P for role in ("road", "kerb") for P in survey.get(role, []) if inF(P)]
        r = max(1, int(round(ROAD_BUF_M / G.c)))
        nx, ny = G.nx, G.ny
        for P in self.roads:
            for n in G.line_cells(uvP(P)):
                i, j = n % nx, n // nx
                for dj in range(-r, r + 1):
                    for di in range(-r, r + 1):
                        ii, jj = i + di, j + dj
                        if di * di + dj * dj <= r * r + 1 and 0 <= ii < nx and 0 <= jj < ny and F[jj * nx + ii] == 0:
                            F[jj * nx + ii] = 2
        self.ref = self.CL.get("W", {}).get("ref") or stream_ref()[0]
        self.rows = [x for x in (self.CL.get("W", {}).get("rows") or [])
                     if not x["cov"] and x.get("NE") and x.get("SW") and V.inside(x["p"][0], x["p"][1])]
        for x in self.rows:                                              # the bed between the edges river_walks found
            t = x["SW"]["e"]
            while t <= x["NE"]["e"]:
                n = self.cell((x["p"][0] + x["n"][0] * t, x["p"][1] + x["n"][1] * t))
                if n is not None and F[n] != 1:
                    F[n] = 3
                t += G.c * 0.5
        self.streams = [P for P in survey.get("stream", []) if inF(P)]
        self.contours = [P for role in ("contour", "contour10") for P in survey.get(role, []) if inF(P)]
        self.contour_z = [(P, z) for P, z in survey.get("contour_z", []) if inF(P)]   # v28: p.24 section ground
        for P in self.streams:
            for n in G.line_cells(uvP(P)):
                if F[n] == 0:
                    F[n] = 3
        if not self.rows:
            warn.append(u"corridor: no stream edges from the survey (river_walks rows): no bed, widening or moves")
        pl28_frame_stats(self)                          # v27 (MIRAQUA 28 Oct, G10): cells inside the frame, its polygon area
        self.dist_water()
        self.hubs = []
        for hid, br, xy, stop, sxy, sub in HUBS:
            self.hubs.append({"id": hid, "bridge": br, "xy": xy, "stop": stop, "stop_xy": sxy, "sub": sub,
                              "role": "transit" if hid in MAIN_TRANSIT_HUB else "walking",
                              "stop_m": math.hypot(sxy[0] - xy[0], sxy[1] - xy[1])})
        self.prog = [h for h in self.hubs if h["id"] != u"K6"]           # K6 = gateway out (D2): no programme ring
        self.notes = []
        self.build()

    # ---- grid helpers
    def cell(self, p):
        """Grid cell of world point p, or None outside the frame."""
        u, v = self.V.uv(p)
        G = self.G
        i, j = int((u - G.x0) / G.c), int((v - G.y0) / G.c)
        if 0 <= i < G.nx and 0 <= j < G.ny:
            return j * G.nx + i
        return None

    def near_cells(self, xy, r):
        """Cells whose centre lies within r m of world point xy."""
        G = self.G
        u, v = self.V.uv(xy)
        out = []
        for j in range(max(0, int((v - r - G.y0) / G.c)), min(G.ny, int((v + r - G.y0) / G.c) + 1)):
            for i in range(max(0, int((u - r - G.x0) / G.c)), min(G.nx, int((u + r - G.x0) / G.c) + 1)):
                if math.hypot(G.x0 + (i + 0.5) * G.c - u, G.y0 + (j + 0.5) * G.c - v) <= r:
                    out.append(j * G.nx + i)
        return out

    def wxy(self, n):
        return self.V.xy(*self.G.xy(n))

    def dist_water(self):
        G, F = self.G, self.F
        nx, ny, c = G.nx, G.ny, G.c
        Dst = self.Dst = [1e9] * self.N
        hp = [(0.0, n) for n in range(self.N) if F[n] == 3]
        for _, n in hp:
            Dst[n] = 0.0
        heapq.heapify(hp)
        nb = [(1, 0, c), (-1, 0, c), (0, 1, c), (0, -1, c), (1, 1, c * 1.4142), (-1, 1, c * 1.4142),
              (1, -1, c * 1.4142), (-1, -1, c * 1.4142)]
        while hp:
            d, n = heapq.heappop(hp)
            if d > Dst[n] or d > DMAX_M:
                continue
            i, j = n % nx, n // nx
            for di, dj, w in nb:
                ii, jj = i + di, j + dj
                if 0 <= ii < nx and 0 <= jj < ny:
                    m = jj * nx + ii
                    if (F[m] == 0 or F[m] == 3) and d + w < Dst[m]:
                        Dst[m] = d + w
                        heapq.heappush(hp, (d + w, m))

    def dhub(self, p, hubs=None):
        return min([math.hypot(p[0] - h["xy"][0], p[1] - h["xy"][1]) for h in (hubs or self.prog)] or [1e9])

    def loops(self, cells, organic):
        """World loops of a cell set: organic (smoothed) at the water, faceted elsewhere (form rule)."""
        out = []
        for Lp in trace(self.G, set(cells)):
            Q = smooth(Lp, self.G.c * 0.9, 2 if organic else 0)
            if len(Q) >= 3 and abs(area2(Q)) > 6.0 * self.G.c * self.G.c:
                out.append([self.V.xy(u, v) for u, v in Q])
        return out

    def note(self, key, text, why, at):
        """A numbered note (numbers given after all are made, upstream first); same key = one note, more places."""
        for nt in self.notes:
            if nt["key"] == key:
                nt["at"] += list(at)
                return nt
        self.notes.append({"key": key, "text": text, "why": list(why), "at": list(at)})
        return self.notes[-1]

    # ---- the design
    def build(self):
        F, Dst, N = self.F, self.Dst, self.N
        open_ = lambda n: F[n] == 0 or F[n] == 3
        self.max_loops = self.loops([n for n in range(N) if open_(n)], False)
        self.road_loops = self.loops([n for n in range(N) if F[n] == 2], False)
        self.bare_loops = self.loops([n for n in range(N) if F[n] == 0 and self.lc[n] == 0], False)   # v26
        self.bed_loops = self.loops([n for n in range(N) if F[n] == 3], True)
        self.eco = [(t, self.loops([n for n in range(N) if F[n] == 0 and Dst[n] <= t], t <= ECO_ORGANIC))
                    for t in ECO_BANDS]                                  # v26: on open ground only, not the bed
        dh = [1e9] * N
        for n in range(N):
            if F[n] == 0 and Dst[n] <= HUB_CORRIDOR:
                dh[n] = self.dhub(self.wxy(n))
        self.dh = dh
        self.rings = [(r, self.loops([n for n in range(N) if dh[n] <= r], False)) for r in HUB_RINGS]
        for h in self.hubs:                                              # the dry hub squares (faceted)
            h["square"] = []
            if h["id"] in (u"K6", u"Kızıl Avlu"):
                continue
            cs = [n for n in self.near_cells(h["xy"], HUB_SQ_M) if F[n] == 0 and Dst[n] >= 4.0]
            h["square"] = self.loops(cs, False)
            h["trees"] = []
            for L_ in h["square"]:
                s = arclen(L_ + L_[:1])
                t = 0.0
                while t < s[-1]:
                    h["trees"].append(at_len(L_ + L_[:1], s, t)[0])
                    t += 9.0
            h["sub_xy"] = self.sub_hub(h["xy"]) if h["sub"] else None
        self.moves()
        self.terraces()
        self.planting()
        self.crossings()
        self.view_terrace()
        self.make_notes()
        self.no_go()

    def sub_hub(self, xy):
        """The bed station nearest a bridge anchor (within 60 m): its centre and both edges (D10 sub-hub)."""
        best = min(self.rows, key=lambda x: (x["p"][0] - xy[0]) ** 2 + (x["p"][1] - xy[1]) ** 2) if self.rows else None
        if best is None or math.hypot(best["p"][0] - xy[0], best["p"][1] - xy[1]) > 60.0:
            return None
        at = lambda t: (best["p"][0] + best["n"][0] * t, best["p"][1] + best["n"][1] * t)
        e0, e1 = best["SW"]["e"], best["NE"]["e"]
        return {"c": at((e0 + e1) / 2.0), "a": at(e0), "b": at(e1), "w": e1 - e0}

    def free_out(self, x, side, sg):
        """Open ground beyond a bank edge along the station's normal (m) and what stops it."""
        e, t = x[side]["e"], 1.0
        while t < FREE_MAX:
            n = self.cell((x["p"][0] + x["n"][0] * (e + sg * t), x["p"][1] + x["n"][1] * (e + sg * t)))
            if n is None:
                return t, "frame"
            if self.F[n] == 1:
                return t, "building"
            if self.F[n] == 2:
                return t, "road"
            t += self.G.c * 0.5
        return FREE_MAX, "open"

    def moves(self):
        """Widen, side arm (branch), kept: per bank station, from the open ground beside the edge (open ground). Widening
        and arms only from K5 downstream (spec: 'downstream'); kept everywhere (where we could not expand)."""
        self.widen, self.arms, self.kept = [], [], []
        ch5 = chain_at(self.ref, BRIDGES_K[4][1])[0] if self.ref else 0.0
        st = self.rows
        for side, sg in (("NE", 1.0), ("SW", -1.0)):
            raw = [self.free_out(x, side, sg) for x in st]
            fw = [_median([v[0] for v in raw[max(0, i - 4):i + 5]]) for i in range(len(raw))]
            cls = []
            for i, x in enumerate(st):
                down = x["ch"] >= ch5 + 20.0
                cls.append("kept_" + raw[i][1] if fw[i] < KEPT_MAX else
                           ("branch" if down and fw[i] >= BRANCH_MIN else ("widen" if down and fw[i] >= WIDEN_MIN else None)))

            def runs(pred):
                out, cur = [], []
                for i, x in enumerate(st):
                    if pred(cls[i]) and (not cur or x["ch"] - st[cur[-1]]["ch"] <= 3 * WALK_STEP):
                        cur.append(i)
                        continue
                    if len(cur) * WALK_STEP >= MOVE_RUN_M:
                        out.append(cur)
                    cur = [i] if pred(cls[i]) else []
                if len(cur) * WALK_STEP >= MOVE_RUN_M:
                    out.append(cur)
                return out
            at = lambda x, t: (x["p"][0] + x["n"][0] * t, x["p"][1] + x["n"][1] * t)
            for ix in runs(lambda c_: c_ in ("widen", "branch")):
                L = len(ix)
                inner, outer = [], []
                for a, i in enumerate(ix):
                    x, e = st[i], st[i][side]["e"]
                    tap = min(1.0, (a + 1) / 6.0, (L - a) / 6.0)
                    inner.append(at(x, e))
                    outer.append(at(x, e + sg * min(WIDEN_K * fw[i], WIDEN_CAP) * tap))
                ring_ = chaikin(inner + outer[::-1], 2, closed=True)
                mid = st[ix[L // 2]]
                self.widen.append({"ring": ring_, "at": at(mid, mid[side]["e"] + sg * 4.0),
                                   "fw": (min(fw[i] for i in ix), max(fw[i] for i in ix))})
            for ix in runs(lambda c_: c_ == "branch"):
                if len(ix) * WALK_STEP < 2 * MOVE_RUN_M:
                    continue
                L = len(ix)
                arm = []
                for a, i in enumerate(ix):
                    x, e = st[i], st[i][side]["e"]
                    tap = math.sin(math.pi * min(1.0, (a + 0.5) / 10.0, (L - a - 0.5) / 10.0) / 2.0)
                    arm.append(at(x, e + sg * min(ARM_K * fw[i], ARM_CAP) * tap))
                self.arms.append({"P": chaikin(arm, 2), "at": arm[L // 2]})
            for why in ("building", "road", "frame"):
                for ix in runs(lambda c_, w_=why: c_ == "kept_" + w_):
                    mid = st[ix[len(ix) // 2]]
                    self.kept.append({"why": why, "at": at(mid, mid[side]["e"] + sg * 2.0)})

    def terraces(self):
        """Upstream (from the frame's upstream end to K4, where the contours crowd): survey contours on open ground
        TERRACE_D from the water become terrace edges; each holds the rain that runs down to it (ticks toward the
        stream = down the valley side). Steepness = contour length per open hectare, upstream vs from K5 down."""
        V = self.V
        u4 = V.uv(BRIDGES_K[3][1])[0]
        u5 = V.uv(BRIDGES_K[4][1])[0]
        self.terr, per = [], {"up": [0.0, 0.0], "down": [0.0, 0.0]}

        def ok(x, y):
            n = self.cell((x, y))
            return n is not None and self.F[n] == 0 and TERRACE_D[0] <= self.Dst[n] <= TERRACE_D[1] and \
                V.uv((x, y))[0] < u4
        for P in self.contours:
            for r_ in cut_runs(P, ok, 2.0):
                if len(r_) >= 2 and arclen(r_)[-1] >= 15.0:
                    self.terr.append(r_)
            for a, b in zip(P, P[1:]):
                q = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)
                n = self.cell(q)
                if n is None or self.F[n] != 0:
                    continue
                u = V.uv(q)[0]
                k_ = "up" if u < u4 else ("down" if u > u5 else None)
                if k_:
                    per[k_][0] += math.hypot(b[0] - a[0], b[1] - a[1])
        G = self.G
        for n in range(self.N):
            if self.F[n] == 0:
                u = G.x0 + (n % G.nx + 0.5) * G.c
                k_ = "up" if u < u4 else ("down" if u > u5 else None)
                if k_:
                    per[k_][1] += G.c * G.c / 10000.0
        self.steep = dict((k_, v[0] / v[1] if v[1] > 0 else 0.0) for k_, v in per.items())

    def planting(self):
        """Forest corridor (dense) and tree-planted area (sparse) on open ground by distance from the water, away
        from the hubs (H1: programme at the hubs, planting between); jittered grid (deterministic)."""
        G, F, Dst = self.G, self.F, self.Dst
        self.forest, self.trees = [], []
        for (d0, d1, hmin, sp), out in ((FOREST, self.forest), (TREES, self.trees)):
            s = max(1, int(round(sp / G.c)))
            for j in range(0, G.ny, s):
                for i in range(0, G.nx, s):
                    jit = math.sin(i * 12.9898 + j * 78.233) * 43758.5453
                    jit = jit - math.floor(jit)
                    ii = min(G.nx - 1, i + int(jit * s))
                    n = j * G.nx + ii
                    if F[n] != 0 or not (d0 <= Dst[n] <= d1):
                        continue
                    p = self.wxy(n)
                    if self.dhub(p) >= hmin:
                        out.append(p)
        runs = [x for x in self.CL.get("W", {}).get("runs", []) if x.get("cls") == "bank" and len(x.get("F") or []) > 1]
        keep = []
        for x in runs:                                   # one canopied walkway per reach: the longer of two banks
            other = [y for y in runs if y["bank"] != x["bank"] and min(x["ch1"], y["ch1"]) - max(x["ch0"], y["ch0"]) >
                     0.5 * (x["ch1"] - x["ch0"]) and y["m"] > x["m"]]
            if not other:
                keep.append(x["F"])
        self.canopy = keep
        walk = [h for h in self.hubs if h["role"] == "walking" and h["id"] != u"K6"]
        self.seats = []
        for P in keep:
            s = arclen(P)
            t = 0.0
            while t < s[-1]:
                q = at_len(P, s, t)[0]
                d = self.dhub(q, walk)
                step = next((st_ for lim, st_ in SEAT_STEP if d <= lim), None)
                if step is None:
                    t += SEAT_STEP[-1][1]
                    continue
                self.seats.append(q)
                t += step

    def crossings(self):
        """Bridges kept (K1-K6 within 40 m of the stream line), footbridges where a reach without a
        crossing is longer than FOOT_GAP_M (at the open-ground station nearest the gap's middle, both landings open),
        stepping stones at each sub-hub."""
        ref = self.ref
        if not ref:
            self.cross, self.covered = [], []
            return
        s_ref = arclen(ref)
        ch = []
        for nm, xy in BRIDGES_K:
            c_, d_ = chain_at(ref, xy)
            if d_ <= 40.0:
                ch.append((c_, nm, xy))
        self.cross = [{"name": nm + u" bridge", "kind": "bridge kept", "xy": xy} for c_, nm, xy in ch]
        lo = min((chain_at(ref, p)[0] for p in self.V.P), default=0.0)
        hi = max((chain_at(ref, p)[0] for p in self.V.P), default=s_ref[-1])
        cov = stream_ref()[1]
        cs = sorted([lo] + [c_ for c_, _, _ in ch] + [min(hi, s_ref[-1])])
        rows = self.rows
        n_ft = 0
        for a, b in zip(cs, cs[1:]):
            gap = b - a
            if gap <= FOOT_GAP_M:
                continue
            k_ = int(math.ceil(gap / FOOT_GAP_M)) - 1
            for q in range(1, k_ + 1):
                target = a + gap * q / (k_ + 1.0)
                cand = [x for x in rows if abs(x["ch"] - target) <= gap / (2.0 * (k_ + 1))]
                cand.sort(key=lambda x: abs(x["ch"] - target))
                for x in cand:
                    if self.free_out(x, "NE", 1.0)[0] >= 4.0 and self.free_out(x, "SW", -1.0)[0] >= 4.0:
                        at = lambda t: (x["p"][0] + x["n"][0] * t, x["p"][1] + x["n"][1] * t)
                        A_, B_ = at(x["SW"]["e"] - 3.0), at(x["NE"]["e"] + 3.0)
                        n_ft += 1
                        self.cross.append({"name": u"footbridge {}".format(n_ft), "kind": "footbridge",
                                           "xy": ((A_[0] + B_[0]) / 2.0, (A_[1] + B_[1]) / 2.0), "P": [A_, B_],
                                           "gap": gap})
                        break
        for h in self.hubs:
            if h.get("sub_xy"):
                self.cross.append({"name": u"stepping stones " + h["id"], "kind": "stepping stones",
                                   "xy": h["sub_xy"]["c"], "P": [h["sub_xy"]["a"], h["sub_xy"]["b"]]})
        self.covered = [P for P in self.CL.get("W", {}).get("covered", [])] or \
            [[ref[i], ref[i + 1]] for i in range(len(ref) - 1) if i < len(cov) and cov[i]]

    def view_terrace(self):
        """H5 (D5; h03 Q3): the viewing terrace, sited by a computed sightline to the Trajaneum (TRAJANEUM). Method:
        candidates = open ground (no building, no road, not the bed) 4-40 m from the water between the frame's
        upstream end and K3; a candidate is clear when the straight line from it toward the Trajaneum crosses no
        survey building inside the site frame (plan check, 2D: no surveyed summit point, the acropolis height is
        uncertain 300/335/336 m, so no height-based visibility is computed); of the clear ones the terrace takes the
        highest ground (survey spot heights NOKTA_TAKEOMETRI within 12 m), else the one nearest K4. Beyond the frame
        the line is not checked."""
        self.terrace = None
        F, Dst, G = self.F, self.Dst, self.G
        u3 = self.V.uv(BRIDGES_K[2][1])[0]
        bk = {}
        for q in self.spots:                                  # spot heights bucketed in 12 m cells
            bk.setdefault((int(q[0] // 12.0), int(q[1] // 12.0)), []).append(q)
        best = None
        for n in range(0, self.N, 3):
            if F[n] != 0 or not (4.0 <= Dst[n] <= 40.0):
                continue
            if G.x0 + (n % G.nx + 0.5) * G.c > u3:
                continue
            p = self.wxy(n)
            dx, dy = TRAJANEUM[0] - p[0], TRAJANEUM[1] - p[1]
            L = math.hypot(dx, dy) or 1.0
            t, clear = G.c, True
            while t < 600.0:
                m = self.cell((p[0] + dx / L * t, p[1] + dy / L * t))
                if m is None:
                    break
                if F[m] == 1:
                    clear = False
                    break
                t += G.c
            if not clear:
                continue
            gx, gy = int(p[0] // 12.0), int(p[1] // 12.0)
            zs = [q[2] for di in (-1, 0, 1) for dj in (-1, 0, 1) for q in bk.get((gx + di, gy + dj), ())
                  if abs(q[0] - p[0]) <= 12.0 and abs(q[1] - p[1]) <= 12.0]
            k4 = math.hypot(p[0] - BRIDGES_K[3][1][0], p[1] - BRIDGES_K[3][1][1])
            score = (max(zs) if zs else -1e9, -k4)
            if best is None or score > best[0]:
                best = (score, p, max(zs) if zs else None, L)
        if best is not None:
            self.terrace = {"xy": best[1], "z": best[2], "d": best[3],
                            "dir": ((TRAJANEUM[0] - best[1][0]) / best[3], (TRAJANEUM[1] - best[1][1]) / best[3])}
        else:
            self.warn.append(u"viewing terrace: no open ground with a clear line to the Trajaneum (upstream of K3)")

    def make_notes(self):
        """The numbered notes: short note + stacked reasons (D11), each reason an analysis in the booklet (D12)."""
        V = self.V
        for h in self.hubs:
            hid = h["id"]
            sq = [inner_pt(max(h["square"], key=lambda L_: abs(area2(L_))))] if h.get("square") else [h["xy"]]
            stop = u"bus stop {} {:.0f} m".format(h["stop"], h["stop_m"])
            if h["role"] == "transit":
                txt = u"TRANSIT HUB · {}".format(HUB_NAME[hid])
                why = [u"town bus lines stop here (h03 Q1)", stop]
                why += [u"H2 culvert under the square: hidden-stream square", u"D8 plane trees, irrigated from storage"] \
                    if hid == u"İstiklal" else [u"H2 Red Hall tunnels"]
            elif hid == u"K6":
                txt, why = u"GATEWAY OUT · K6", [u"OSM primary road kept (h02 E12)", stop]
            else:
                txt = u"WALKING HUB · {} · DRY SQUARE{}".format(hid, u" + BED SUB-HUB" if h.get("sub_xy") else u"")
                # v26.1 (Prompt 8): the reason is the analysis' own name ("open ground (open ground)" read twice)
                why = [u"H1 Roman bridge", u"open ground", stop, u"D8 plane trees, irrigated from storage"]
                if h.get("sub_xy"):
                    why.append(u"sub-hub closes in floods (Q100/Q500 cuts)")
                if hid == u"K3":
                    why.insert(1, u"H3 tanning reach: workshops, education")
                if hid == u"K5":
                    why.insert(1, u"Demeter's Garden: Q500 stays in the banks at the K5 cut")
            self.note(("hub", hid), txt, why, sq)
        self.note(("h4",), u"STEP TO THE WATER FACING TABAKLAR HAMAMI", [u"H4 bath ruin 1.5 m from the stream"],
                  [PLACES[1][1]])
        self.note(("h6",), u"DECK OVER THE ROMAN BANK WALL", [u"H6 Roman complex, ~120 m bank wall (h01 P12)"],
                  [ROMAN_WALL])                          # v26.1: h01's place register P12 (it read like a page number)
        if self.terrace:
            z = u", highest clear ground +{:.1f} m".format(self.terrace["z"]) if self.terrace["z"] is not None else u""
            self.note(("view",), u"VIEWING TERRACE · TRAJANEUM {:,.0f} m".format(self.terrace["d"]),
                      [u"H5 computed sightline: no building on the line (site frame){}".format(z)], [self.terrace["xy"]])
        for z in self.D.zones:
            if z["code"] == "WT":
                self.note(("wt",), u"WATER CLEANED ONCE · REED BASINS",
                          [u"collect, clean, hold chain (water board)", u"clean-water classroom (city link stop 7)"],
                          [z["q"]])
        if self.terr:
            st = self.steep
            self.note(("terr",), u"TERRACES ON THE CONTOURS HOLD THE RAIN",
                      [u"survey contours: {:.0f} m/ha upstream, {:.0f} m/ha below K5".format(st.get("up", 0.0),
                                                                                        st.get("down", 0.0)),
                       u"overflow to the reed basins (collect, clean, hold)"],
                      [self.terr[len(self.terr) // 2][len(self.terr[len(self.terr) // 2]) // 2]])
        if self.covered:
            P = max(self.covered, key=lambda P: arclen(P)[-1])
            self.note(("cov",), u"NOTHING OPENED · WATER LINE IN THE PAVING",
                      [u"H2 covered reach, ~240 m without stream lines (h02 E01)"],
                      [at_len(P, arclen(P), arclen(P)[-1] / 2.0)[0]])
        if self.widen:
            lo, hi = min(w["fw"][0] for w in self.widen), max(w["fw"][1] for w in self.widen)
            self.note(("widen",), u"STREAM WIDENED: ROOM FOR WATER, WETLAND",
                      [u"open ground {:.0f}-{:.0f} m beside the bank (open ground)".format(lo, hi)],
                      [w["at"] for w in self.widen])
        if self.arms:
            self.note(("arm",), u"SIDE ARM: REED CHANNEL CLEANS THE RETURN",
                      [u"open ground >= {:.0f} m (open ground)".format(BRANCH_MIN), u"H7 downstream working edge (h02 E11)"],
                      [a["at"] for a in self.arms])
        for why, txt in (("building", u"KEPT: BUILDINGS STAND AT THE BANK"), ("road", u"KEPT: A ROAD RUNS AT THE BANK"),
                         ("frame", u"NOTHING PLACED: EDGE OF THE SITE FRAME")):
            at = []
            for k in self.kept:                          # one badge per KEPT_SPACE_M at most (legible plan)
                if k["why"] == why and all(math.hypot(k["at"][0] - q[0], k["at"][1] - q[1]) >= KEPT_SPACE_M for q in at):
                    at.append(k["at"])
            if at:
                self.note(("kept", why), txt, [u"less than {:.0f} m open (open ground)".format(KEPT_MAX)], at)
        ft = [c_ for c_ in self.cross if c_["kind"] == "footbridge"]
        if ft:
            self.note(("foot",), u"FOOTBRIDGE: {:.0f}+ m WITHOUT A CROSSING".format(FOOT_GAP_M),
                      [u"crossings K1-K6 (edge plan)", u"both landings open (open ground)"], [c_["xy"] for c_ in ft])
        for rd in ROADS + [TOWN_LINE]:
            P = rd["xy"]
            mid = at_len(P, arclen(P), arclen(P)[-1] / 2.0)[0]
            self.note(("road", rd["name"]), rd["note"].upper(), [rd["proof"]], [mid])
        self.notes.sort(key=lambda nt: min(V.uv(p)[0] for p in nt["at"]))
        for i, nt in enumerate(self.notes, 1):
            nt["n"] = i

    def no_go(self):
        """v26 (Prompt 7 task 1): the areas the plan leaves untouched, each with why, from the data only. Touched =
        the bed, the planting gradient (open ground up to ECO_BANDS[-1] m from the water), the programme rings, the
        reed basins and Demeter's Garden, and NI_ROAD_M either side of a changed road or the hidden-stream line. On
        NI_BLOCK m blocks: a block is untouched when NI_SHARE of its cells are; untouched blocks join (4-connected)
        into built ones (buildings and streets >= NI_BUILT of the block) and open ones; regions of NI_MIN_HA or more
        get a note. Why: built = the survey's building kinds (homes BINA_MESKEN, heritage, other) or built since the
        survey (satellite check); open = the ESA WorldCover 2021 classes of its open cells and how far it lies from
        the water through open ground (or that no open path reaches the water within DMAX_M m). No data maps private
        plots, the heritage protection zone or the Q100 flood extent as areas: those reasons are not used."""
        F, Dst, G, N, V = self.F, self.Dst, self.G, self.N, self.V
        nx, ny = G.nx, G.ny
        touch = bytearray(N)
        for n in range(N):
            if F[n] == 3 or (F[n] == 0 and (Dst[n] <= ECO_BANDS[-1] or self.dh[n] <= HUB_RINGS[-1])):
                touch[n] = 1
        for z in self.D.zones:
            if z["code"] in ("WT", "DG"):
                for n in G.poly_cells([V.uv(p) for p in z["P"]]):
                    touch[n] = 1
        r = max(1, int(round(NI_ROAD_M / G.c)))
        for P in [rd["xy"] for rd in ROADS + [TOWN_LINE] if rd["change"] != "kept"] + list(self.covered):
            for n in G.line_cells([V.uv(p) for p in P]):
                i, j = n % nx, n // nx
                for jj in range(max(0, j - r), min(ny, j + r + 1)):
                    for ii in range(max(0, i - r), min(nx, i + r + 1)):
                        touch[jj * nx + ii] = 1
        s = max(1, int(round(NI_BLOCK / G.c)))
        bx, by = (nx + s - 1) // s, (ny + s - 1) // s
        blk = {}
        for b in range(bx * by):
            i0, j0 = (b % bx) * s, (b // bx) * s
            cs = [j * nx + i for j in range(j0, min(ny, j0 + s)) for i in range(i0, min(nx, i0 + s))]
            if sum(1 for n in cs if not touch[n]) >= NI_SHARE * len(cs):
                blk[b] = "built" if sum(1 for n in cs if F[n] in (1, 2)) >= NI_BUILT * len(cs) else "open"
        nb4 = lambda b: ((b + 1) if b % bx + 1 < bx else -1, (b - 1) if b % bx else -1,
                         (b + bx) if b // bx + 1 < by else -1, (b - bx) if b // bx else -1)   # -1 = off the grid
        self.nogo, seen = [], set()
        what = {1: u"homes", 2: u"buildings", 3: u"heritage buildings", 4: u"sheds", 5: u"built since the survey"}
        lc_nm = {0: u"no plant cover", 1: u"cropland", 2: u"tree cover", 3: u"scrub", 4: u"grassland",
                 5: u"orchards"}                         # LC_KEYS order
        for b0 in sorted(blk):
            if b0 in seen:
                continue
            kind, reg, q = blk[b0], [], [b0]
            seen.add(b0)
            while q:                                     # the region: 4-connected blocks of the same kind
                b = q.pop()
                reg.append(b)
                for m in nb4(b):
                    if m >= 0 and m not in seen and blk.get(m) == kind:
                        seen.add(m)
                        q.append(m)
            cells = [j * nx + i for b in reg for j in range((b // bx) * s, min(ny, (b // bx) * s + s))
                     for i in range((b % bx) * s, min(nx, (b % bx) * s + s))]
            ha = len(cells) * G.c * G.c / 1e4
            if ha < NI_MIN_HA:
                continue
            if kind == "built":
                cnt = {}
                for n in cells:
                    if F[n] == 1:
                        cnt[self.bt[n]] = cnt.get(self.bt[n], 0) + 1
                tot = sum(cnt.values())
                top = max(cnt, key=cnt.get) if cnt else None
                if top is None:
                    why = u"streets (survey)"
                elif top == 5:
                    why = u"built since the survey (satellite check)"
                elif cnt[top] >= 0.5 * tot:
                    why = u"{} (survey)".format(what[top])
                else:
                    why = u"buildings and streets (survey)"
            else:
                cnt = {}
                op = [n for n in cells if F[n] == 0]
                for n in op:
                    cnt[self.lc[n]] = cnt.get(self.lc[n], 0) + 1
                ks = sorted(cnt, key=lambda k_: -cnt[k_])
                nm = lc_nm[ks[0]] if ks else u"open ground"
                if len(ks) > 1 and cnt[ks[0]] < 0.6 * len(op):
                    nm += u" and " + lc_nm[ks[1]]
                d = min([Dst[n] for n in op if Dst[n] < 1e8] or [None]) if op else None
                far = u"{:.0f} m from the water".format(10.0 * math.ceil(d / 10.0)) if d is not None else \
                    u"no open way to the water within {:.0f} m".format(DMAX_M)
                why = u"{} (satellite 2021), {}".format(nm, far)
            inreg = set(reg)                              # label spots: the blocks farthest inside, first
            dist, q = {}, []
            for b in reg:
                if any(m_ not in inreg for m_ in nb4(b)):
                    dist[b] = 0
                    q.append(b)
            for b in q:                                   # breadth first inward (q grows while it is walked)
                for m_ in nb4(b):
                    if m_ in inreg and m_ not in dist:
                        dist[m_] = dist[b] + 1
                        q.append(m_)
            spots = sorted(reg, key=lambda b: -dist.get(b, 0))[:24]
            at = [V.xy(G.x0 + ((b % bx) * s + s / 2.0) * G.c, G.y0 + ((b // bx) * s + s / 2.0) * G.c) for b in spots]
            self.nogo.append({"kind": kind, "why": why, "ha": ha, "at": at})
        self.nogo.sort(key=lambda r_: -r_["ha"])

    def movement(self):
        """masterplan_results.json "movement" (spec §4; survey coordinates)."""
        r2 = lambda p: [round(p[0], 1), round(p[1], 1)]
        roads = [{"name": rd["name"], "change": rd["change"], "note": rd["note"], "reason_proof": rd["proof"],
                  "xy": [r2(p) for p in rd["xy"]]} for rd in ROADS]
        routes = [{"name": TOWN_LINE["name"], "note": TOWN_LINE["note"], "later": True, "change": TOWN_LINE["change"],
                   "reason_proof": TOWN_LINE["proof"], "xy": [r2(p) for p in TOWN_LINE["xy"]]}]   # site board v44
        cross = []
        for c_ in self.cross:
            note = {"bridge kept": u"existing bridge kept", "stepping stones": u"sub-hub crossing, closes in floods",
                    "footbridge": u"{:.0f} m reach without a crossing".format(c_.get("gap", 0.0))}[c_["kind"]]
            cross.append({"name": c_["name"], "kind": c_["kind"], "note": note, "xy": r2(c_["xy"])})
        hubs = [{"name": HUB_NAME[h["id"]], "bridge": h["bridge"], "xy": r2(h["xy"]), "bus_stop": h["stop"],
                 "bus_stop_m": round(h["stop_m"], 0), "sub_hub": bool(h.get("sub_xy")), "role": h["role"]}
                for h in self.hubs]
        return {"roads": roads, "routes": routes, "truck_route": None, "crossings": cross, "hubs": hubs,
                "pending": [u"truck_route: no data names the truck route (no HGV tags in OSM, no KGM count on the "
                            u"streets by the stream, card t01)", u"bus line numbers per hub (only the later town line "
                            u"to K4 is named)"]}


# ================================================================ v24: drawing the corridor on a plan
def ticks_line(pg, P, colour, lw, every, size, side=1.0, alpha=None):
    """A line with short ticks every `every` mm to one side (terrace edges, pergola). v26: alpha (proposals)."""
    if len(P) < 2:
        return
    pg.line(P, colour, lw, alpha=alpha)
    s = arclen(P)
    t = every / 2.0
    while t < s[-1]:
        (x, y), (ux, uy) = at_len(P, s, t)
        pg.line([(x, y), (x - uy * size * side, y + ux * size * side)], colour, lw * 0.8, alpha=alpha)
        t += every


def soft_fill(pg, rings, colour, a, halo=0.6):
    """v26 (Prompt 7 rule 1): a proposed area as a fading field: a translucent fill and, outside its edge only
    (even-odd clip), a halo of translucent strokes thinning outward. No outline."""
    rings = [r_ for r_ in rings if len(r_) >= 3]
    if not rings:
        return
    pg.poly(rings, fill=colour, alpha=a)
    b = bbox([p for r_ in rings for p in r_])
    pg.clip([rect(b[0] - halo - 1.0, b[1] - halo - 1.0, b[2] + halo + 1.0, b[3] + halo + 1.0)] + rings)
    for f in (1.0, 0.66, 0.33):
        for r_ in rings:
            pg.line(r_ + r_[:1], colour, 2.0 * halo * f, alpha=a * 0.35)
    pg.unclip()


def soft_line(pg, P, colour, w, a):
    """v26 (Prompt 7 rule 1): a proposed line as a band densest along its middle, fading to its sides."""
    for f in (1.0, 0.62, 0.3):
        pg.line(P, colour, w * f, alpha=a * 0.4)


def icon(pg, kind, x, y, s):
    """Pictograms (page mm, centre x, y, size s)."""
    W_, ink = COL["white"], COL["ink_dark"]
    if kind == "cafe":
        pg.poly([rect(x - s * 0.35, y - s * 0.35, x + s * 0.25, y + s * 0.25)], fill=MP["centre"][2])
        pg.circle(x + s * 0.33, y - s * 0.05, s * 0.14, stroke=MP["centre"][2], lw=0.25)
    elif kind == "edu":
        pg.poly([[(x, y - s * 0.3), (x - s * 0.45, y - s * 0.15), (x - s * 0.45, y + s * 0.35), (x, y + s * 0.2)],
                 [(x, y - s * 0.3), (x + s * 0.45, y - s * 0.15), (x + s * 0.45, y + s * 0.35), (x, y + s * 0.2)]],
                fill=COL["accent_dark"])
    elif kind == "seat":
        pg.poly([rect(x - s * 0.4, y - s * 0.1, x + s * 0.4, y + s * 0.1)], fill=ink)
    elif kind == "transit":
        pg.poly([rect(x - s * 0.5, y - s * 0.5, x + s * 0.5, y + s * 0.5)], fill=COL["accent_dark"], stroke=W_, lw=0.3)
        pg.poly([rect(x - s * 0.28, y - s * 0.05, x + s * 0.28, y + s * 0.28)], fill=W_)
        pg.circle(x - s * 0.18, y - s * 0.25, s * 0.09, fill=W_)
        pg.circle(x + s * 0.18, y - s * 0.25, s * 0.09, fill=W_)
    elif kind == "walkhub":
        pg.poly([rect(x - s * 0.5, y - s * 0.5, x + s * 0.5, y + s * 0.5)], fill=SQ_EDGE, stroke=W_, lw=0.3)
        pg.circle(x, y + s * 0.22, s * 0.12, fill=W_)
        pg.line([(x, y + s * 0.08), (x, y - s * 0.3)], W_, 0.35)
    elif kind == "sub":
        pg.poly([[(x, y + s * 0.5), (x + s * 0.5, y), (x, y - s * 0.5), (x - s * 0.5, y)]], fill=COL["river_dark"],
                stroke=W_, lw=0.25)
    elif kind == "gate":
        pg.poly([[(x - s * 0.5, y + s * 0.45), (x + s * 0.5, y), (x - s * 0.5, y - s * 0.45), (x - s * 0.2, y)]],
                fill=COL["ink_dark"])
    elif kind == "view":
        pg.poly([[(x - s * 0.5, y - s * 0.3), (x + s * 0.5, y - s * 0.3), (x, y + s * 0.5)]], fill=COL["accent"])
    elif kind == "deck":
        pg.poly([rect(x - s * 0.5, y - s * 0.3, x + s * 0.5, y + s * 0.3)], fill=COL["histwall"], stroke=W_, lw=0.25)


# ================================================================ v24: the legend (rebuilt for the corridor)
def _sw_fill(fill, stroke=None, alpha=None, stripes=None):
    def f(pg, x, y, w, h):
        pg.poly([rect(x, y, x + w, y + h)], fill=fill, alpha=alpha, stripes=stripes)
        if stroke:
            pg.poly([rect(x, y, x + w, y + h)], stroke=stroke, lw=0.25)
    return f


def _sw_line(colour, lw, dash=None, alpha=None):
    def f(pg, x, y, w, h):
        pg.line([(x, y + h / 2), (x + w, y + h / 2)], colour, lw, dash, cap=0 if dash else 1, alpha=alpha)
    return f


def _sw_grad(colour):
    def f(pg, x, y, w, h):
        for i in range(4):
            pg.poly([rect(x + w * i / 8.0, y, x + w - w * i / 8.0, y + h)], fill=colour, alpha=0.18)
    return f


def _sw_soft(colour, a, stripes=None):
    """v26: a proposed area: fading field, no outline (as soft_fill)."""
    def f(pg, x, y, w, h):
        R = rect(x + 0.5, y + 0.4, x + w - 0.5, y + h - 0.4)
        soft_fill(pg, [R], colour, a, 0.4)
        if stripes:
            pg.poly([R], stripes=stripes, alpha=0.35)
    return f


def _sw_softline(colour, lw, a):
    """v26: a proposed line: band fading to its sides (as soft_line)."""
    def f(pg, x, y, w, h):
        soft_line(pg, [(x + 0.6, y + h / 2), (x + w - 0.6, y + h / 2)], colour, lw, a)
    return f


def _sw_icon(kind, s=2.4):
    def f(pg, x, y, w, h):
        icon(pg, kind, x + w / 2, y + h / 2, s)
    return f


def _sw_dots(colour, r, alpha):
    def f(pg, x, y, w, h):
        for i in range(4):
            pg.circle(x + w * (i + 0.5) / 4, y + h / 2, r, fill=colour, alpha=alpha)
    return f


def _sw_ticks(colour, lw, alpha=None):
    def f(pg, x, y, w, h):
        ticks_line(pg, [(x, y + h * 0.6), (x + w, y + h * 0.6)], colour, lw, 1.4, 0.7, -1.0, alpha=alpha)
    return f


# v26: short names (the legend runs in columns under the plan); EXISTING = the survey (crisp), the rest proposed (soft)
EXISTING = ("bed", "bld", "her", "since", "bridge", "street", "study")   # v27 (G8): the study area, not the frame
LEGEND_V24 = [
    ("bed", u"Stream bed", _sw_fill(WATER_COL)),
    ("bld", u"Building", _sw_fill(COL["bld"])),
    ("her", u"Heritage building", _sw_fill(COL["her"], COL["her_edge"])),
    ("since", u"Built since survey", _sw_fill(COL["bld"], stripes=(COL["ink_dark"], 0.8, 0.15, 45.0))),
    ("bridge", u"Bridge", _sw_line(COL["ink_dark"], 0.3)),
    ("street", u"Street edge", _sw_line(ROAD_TONE[1], 0.3)),
    ("study", R28_STUDY_NAME, _sw_line(R28_STUDY_LINE["colour"], R28_STUDY_LINE["width_mm"],
                                       list(R28_STUDY_LINE["dash_mm"]))),   # v27 (MIRAQUA 28 Oct, G8)
    ("eco", u"Planting gradient", _sw_grad(ECO_COL)),
    ("ring", u"Programme at hubs", _sw_grad(HUB_COL)),
    ("widen", u"Stream widened", _sw_soft(WET_COL, 0.85)),
    ("arm", u"Reed side arm", _sw_softline(COL["river_mid"], 1.6, 0.6)),
    ("reed", u"Reed basins", _sw_soft(WET_COL, 0.8, (COL["river_dark"], 0.9, 0.15, 90.0))),
    ("dg", u"Demeter's Garden", _sw_soft(MP["agriculture"][2], 0.16)),
    ("hidden", u"Hidden stream line", _sw_line(COL["river_mid"], 0.8, [1.6, 0.9], alpha=0.7)),
    ("terrace", u"Rain terrace", _sw_ticks(MP["storage"][2], 0.3, 0.7)),
    ("forest", u"Forest corridor", _sw_dots(COL["tree_mid"], 0.6, 0.6)),
    ("trees", u"Tree-planted area", _sw_dots(COL["tree"], 0.6, 0.4)),
    ("square", u"Hub square, trees", _sw_soft(SQ_EDGE, 0.22)),
    ("canopy", u"Canopied walkway", _sw_ticks(MP["centre"][2], 0.45, 0.6)),
    ("walkhub", u"Walking hub", _sw_icon("walkhub")),
    ("transit", u"Transit hub", _sw_icon("transit")),
    ("gate", u"Gateway out", _sw_icon("gate")),
    ("sub", u"Sub-hub in the bed", _sw_icon("sub")),
    ("stones", u"Stepping stones", _sw_dots(COL["ink2"], 0.45, 0.7)),
    ("foot", u"New footbridge", _sw_softline(COL["ink_dark"], 0.8, 0.8)),
    ("seat", u"Seats", _sw_icon("seat")),
    ("cafe", u"Cafe", _sw_icon("cafe")),
    ("edu", u"Education", _sw_icon("edu")),
    ("view", u"Viewing terrace", _sw_icon("view")),
    ("sight", u"Sightline", _sw_line(COL["accent"], 0.35, [1.4, 0.8], alpha=0.7)),
    ("deck", u"Deck, archaeology", _sw_icon("deck")),
    ("road_calmed", u"Road calmed", _sw_softline(ROAD_CHANGE_COL["calmed"], 1.6, 0.75)),
    ("road_pedestrian", u"Road pedestrian", _sw_softline(ROAD_CHANGE_COL["pedestrian"], 1.6, 0.75)),
    ("road_shared", u"Road shared", _sw_softline(ROAD_CHANGE_COL["shared"], 1.6, 0.75)),
    ("road_kept", u"Road kept", _sw_softline(ROAD_CHANGE_COL["kept"], 1.6, 0.75)),
    ("road_later", u"Bus line, later", _sw_line(ROAD_CHANGE_COL["later"], 0.6, [2.0, 1.0], alpha=0.6))]
# the same as booklet footer entries (fill / line / dot + plain name) for the 1:1,000 crops
LEG_BOOK = {"eco": ("fill", mix(COL["white"], ECO_COL, 0.4)), "ring": ("fill", mix(COL["white"], HUB_COL, 0.45)),
            "bed": ("fill", WATER_COL), "widen": ("fill", WET_COL), "reed": ("fill", WET_COL),
            "hidden": ("line", COL["river_mid"]), "terrace": ("line", MP["storage"][2]), "forest": ("dot", COL["tree_mid"]),
            "trees": ("dot", COL["tree"]), "square": ("fill", mix(COL["white"], SQ_EDGE, 0.22)),
            "sub": ("dot", COL["river_dark"]), "stones": ("dot", COL["ink2"]), "foot": ("line", COL["ink_dark"]),
            "canopy": ("line", MP["centre"][2]), "seat": ("line", COL["ink_dark"]), "cafe": ("fill", MP["centre"][2]),
            "edu": ("fill", COL["accent_dark"]), "view": ("dot", COL["accent"]), "deck": ("fill", COL["histwall"]),
            "transit": ("fill", COL["accent_dark"]), "walkhub": ("fill", SQ_EDGE),
            "road_calmed": ("line", ROAD_CHANGE_COL["calmed"]), "road_pedestrian": ("line", ROAD_CHANGE_COL["pedestrian"]),
            "road_shared": ("line", ROAD_CHANGE_COL["shared"]), "road_kept": ("line", ROAD_CHANGE_COL["kept"]),
            "road_later": ("line", ROAD_CHANGE_COL["later"]), "bld": ("fill", COL["bld"]), "her": ("fill", COL["her"]),
            "bridge": ("line", COL["ink_dark"]), "dg": ("fill", mix(COL["white"], MP["agriculture"][2], 0.16)),
            "sight": ("line", COL["accent"])}


def legend_v24_groups():
    """v24: the sheet band's legend group of the 1:1,000 detail sheet (what it draws)."""
    return [(u"CORRIDOR", [(nm, f) for key, nm, f in LEGEND_V24 if ("v24", key) in LEG])]


# v28 (revision 29 Oct): the booklet's p.23 is plan_page (pages/p23_plan.py); ground_page (p.21/22) is gone (D1 a).


# ================================================================ v26: the open ground for Google Earth (task 3)
OG_KML = u"bergama_masterplan_open_ground_check.kml"
OG_MIN_HA = 0.25                 # open areas this large or larger go on the check list
# the site board's lon/lat -> survey transform (selinus_board GEO of v29 and its tm27; exact per vertex)
SV_GEO = dict(s=1.0001121171177874, th=-0.0015904735313230483, tx=-492593.7399912414, ty=-4299748.4497664515)


def _sv_xy(lon, lat):
    a_, f_ = 6378137.0, 1 / 298.257222101
    e2 = f_ * (2 - f_)
    ep2 = e2 / (1 - e2)
    phi, lam = math.radians(lat), math.radians(lon - 27.0)
    s, c, t = math.sin(phi), math.cos(phi), math.tan(phi)
    Nn = a_ / math.sqrt(1 - e2 * s * s)
    T_, Cc, Aa = t * t, ep2 * c * c, c * lam
    e4, e6 = e2 * e2, e2 ** 3
    M = a_ * ((1 - e2 / 4 - 3 * e4 / 64 - 5 * e6 / 256) * phi
              - (3 * e2 / 8 + 3 * e4 / 32 + 45 * e6 / 1024) * math.sin(2 * phi)
              + (15 * e4 / 256 + 45 * e6 / 1024) * math.sin(4 * phi) - (35 * e6 / 3072) * math.sin(6 * phi))
    E = Nn * (Aa + (1 - T_ + Cc) * Aa ** 3 / 6 + (5 - 18 * T_ + T_ * T_ + 72 * Cc - 58 * ep2) * Aa ** 5 / 120) + 500000.0
    Nr = M + Nn * t * (Aa * Aa / 2 + (5 - T_ + 9 * Cc + 4 * Cc * Cc) * Aa ** 4 / 24
                       + (61 - 58 * T_ + T_ * T_ + 600 * Cc - 330 * ep2) * Aa ** 6 / 720)
    cs, sn = math.cos(SV_GEO["th"]), math.sin(SV_GEO["th"])
    return (SV_GEO["s"] * (cs * E - sn * Nr) + SV_GEO["tx"], SV_GEO["s"] * (sn * E + cs * Nr) + SV_GEO["ty"])


def lonlat(p, start):
    """v26: survey m -> (lon, lat), _sv_xy inverted by Newton steps from start (the previous point)."""
    lon, lat = start
    for _ in range(10):
        fx, fy = _sv_xy(lon, lat)
        ex, ey = p[0] - fx, p[1] - fy
        if abs(ex) < 1e-3 and abs(ey) < 1e-3:
            break
        ax, ay = _sv_xy(lon + 1e-5, lat)
        bx, by = _sv_xy(lon, lat + 1e-5)
        j11, j21, j12, j22 = (ax - fx) / 1e-5, (ay - fy) / 1e-5, (bx - fx) / 1e-5, (by - fy) / 1e-5
        det = j11 * j22 - j12 * j21
        lon += (j22 * ex - j12 * ey) / det
        lat += (-j21 * ex + j11 * ey) / det
    return lon, lat


def open_ground_kml(C, path, json_path):
    """v26 (Prompt 7 task 3): every open area (4-connected open cells) of OG_MIN_HA or more as a numbered polygon
    (OG n) for Google Earth, the ones whose open cells have no plant cover on ESA WorldCover 2021 for half or more
    first (most likely built on), then by size; json_path keeps the same areas in survey m by number (what goes
    into OPEN_CHECK["built"] once Aras has named the ones built on). Returns (areas, flagged)."""
    F, G, N, V = C.F, C.G, C.N, C.V
    nx, ny = G.nx, G.ny
    seen = bytearray(N)
    comps = []
    for n0 in range(N):
        if F[n0] != 0 or seen[n0]:
            continue
        comp, q = [], [n0]
        seen[n0] = 1
        while q:
            n = q.pop()
            comp.append(n)
            i, j = n % nx, n // nx
            for m in ((n + 1) if i + 1 < nx else -1, (n - 1) if i else -1, (n + nx) if j + 1 < ny else -1,
                      (n - nx) if j else -1):
                if m >= 0 and not seen[m] and F[m] == 0:
                    seen[m] = 1
                    q.append(m)
        ha = len(comp) * G.c * G.c / 1e4
        if ha >= OG_MIN_HA:
            bare = sum(1 for n in comp if C.lc[n] == 0) / float(len(comp))
            comps.append((bare >= 0.5, ha, bare, comp))
    comps.sort(key=lambda c_: (not c_[0], -c_[1]))
    pm, pts, ll, og = [], [], (27.18127, 39.123302), {}
    for i, (flag, ha, bare, comp) in enumerate(comps, 1):
        rings_ = []
        for Lp in trace(G, set(comp)):
            Q = smooth(Lp, G.c * 0.5, 0)
            if len(Q) >= 3:
                rings_.append([V.xy(u, v) for u, v in Q])
        if not rings_:
            continue
        outer = max(rings_, key=lambda R_: area2(R_))
        og[u"OG {}".format(i)] = {"ha": round(ha, 2), "no_plant_cover_pct": round(100.0 * bare),
                                 "rings_survey_m": [[[round(p[0], 2), round(p[1], 2)] for p in R_]
                                                    for R_ in [outer] + [R_ for R_ in rings_ if area2(R_) < 0]]}
        co = []
        for R_ in [outer] + [R_ for R_ in rings_ if area2(R_) < 0]:
            cs = []
            for p in R_ + R_[:1]:
                ll = lonlat(p, ll)
                cs.append(u"{:.7f},{:.7f},0".format(ll[0], ll[1]))
            co.append(u" ".join(cs))
        body = u"<outerBoundaryIs><LinearRing><coordinates>{}</coordinates></LinearRing></outerBoundaryIs>".format(co[0])
        body += u"".join(u"<innerBoundaryIs><LinearRing><coordinates>{}</coordinates></LinearRing></innerBoundaryIs>"
                         .format(c_) for c_ in co[1:])
        desc = u"{:.2f} ha open in the survey (no building, no road, not the stream bed); no plant cover on {:.0f} % " \
               u"of it on ESA WorldCover 2021. Built on, paved or fenced since? Note OG {} and what is there now, " \
               u"with the imagery date.".format(ha, 100.0 * bare, i)
        pm.append(u"<Placemark><name>OG {}</name><description>{}</description><styleUrl>#{}</styleUrl><Polygon>{}"
                  u"</Polygon></Placemark>".format(i, desc, u"flag" if flag else u"open", body))
        c_ = lonlat(inner_pt(outer), ll)
        pts.append(u"<Placemark><name>OG {}</name><styleUrl>#lab</styleUrl><Point><coordinates>{:.7f},{:.7f},0"
                   u"</coordinates></Point></Placemark>".format(i, c_[0], c_[1]))
    nflag = sum(1 for c_ in comps if c_[0])
    kml = (u'<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2"><Document>'
           u"<name>Bergama open ground: satellite check ({})</name><description>Open ground of the site frame "
           u"from the survey, {} areas of {:.2f} ha or more; red first = no plant cover on ESA WorldCover 2021 on half "
           u"or more of the area. Check each against the newest Google Earth imagery (History slider) and send back "
           u"the numbers built on since, with the imagery date.</description>"
           u'<Style id="flag"><LineStyle><color>ff2a2ad6</color><width>2.5</width></LineStyle><PolyStyle>'
           u"<color>402a2ad6</color></PolyStyle></Style>"
           u'<Style id="open"><LineStyle><color>ff2ad6d6</color><width>1.5</width></LineStyle><PolyStyle>'
           u"<fill>0</fill></PolyStyle></Style>"
           u'<Style id="lab"><IconStyle><scale>0.5</scale></IconStyle><LabelStyle><scale>0.9</scale></LabelStyle></Style>'
           u"<Folder><name>Open areas</name>{}</Folder><Folder><name>Numbers</name>{}</Folder></Document></kml>\n"
           ).format(SHORT, len(comps), OG_MIN_HA, u"".join(pm), u"".join(pts))
    with open(path, "w", encoding="utf-8") as f_:
        f_.write(kml)
    with open(json_path, "w", encoding="utf-8") as f_:
        json.dump(og, f_, ensure_ascii=False)
    C.og_check = {"n": len(comps), "flag": nflag, "file": OG_KML}
    return len(comps), nflag


# v27 (MIRAQUA 28 Oct, P24.1-P24.5): window_panel gone: the 1:1,000 windows are r28_window_panel (02e_r28_detail.py)
# ---- MIRAQUA round 28 Oct 2026 (masterplan v27): p.23 the masterplan (v28: the open ground page is gone); the frame
# area (G10) (worker MP-plan). Shared pieces: common/r28_style.py,
# common/units.py, common/label_place.py, common/figures.py (revision_2026-10-28/PLAN.md).
# v27 (MIRAQUA 28 Oct, MP-plan). Both pages are crops drawn for the booklet panel (BK_W x BK_H = 392 x 238 mm) at 1:1:
#   * G7: the whole analysis frame (site_alan, 2,845 x 529 m) as ONE strip at 1:10,000 (284.5 x 52.9 mm; 1:5,000 would
#     need 569 mm), the water left to right, at the top-left; no halves, no "continues below".
#   * G8: the study area (calisma_alan, both parts) in R28_STUDY_LINE on both, R28_STUDY_NAME in the legend; the strip's
#     edge is the analysis frame, named (R28_FRAME_NAME) only on p.21, where figures are counted over it.
#   * G10: ONE frame figure, the frame polygon's area; the grid counts only cells whose centre lies inside the frame
#     (pl28_frame_stats); every figure on p.21 and in r28_open_ground.json comes from that one count.
#   * P21.1: every open-ground category in its own R28_OPEN colour, the no-plant-cover hatch too; bars in the map's
#     colours.
#   * P23.1 / P23.2: the numbered markers in their R28_MARKERS group colour, placed by common/label_place.py (G4); the
#     list under the strip by group: coloured number, name, one short line. The reasons and source codes go to the
#     booklet's sources page (blocks.json and booklet/results.json "plan_sources"). The areas left as they are (no
#     intervention) get a grey letter on the plan and one line in the list (their two-line notes do not fit at
#     1:10,000).
PL28_TS, PL28_HEAD_TS = 2.65, 2.82   # booklet label 7.5 pt and kicker 8 pt (PLAN §2), mm
PL28_MARKS = (0.0, 100.0, 200.0, 500.0)   # the scale bar at 1:10,000, m (50 mm)
PL28_NI_R = 1.6                  # the letters of the areas left as they are, radius mm
PL28_HUB = {u"K4": u"K4 · Ulucami Önü", u"K3": u"K3 · Tabak", u"İstiklal": u"İstiklal Meydanı",
            u"Kızıl Avlu": u"Kızıl Avlu", u"K5": u"K5 · Üç Kemer", u"K6": u"K6"}   # list names (HUB_NAME, sentence case)
PL28_SRC_TAG = re.compile(u"\\s*\\((survey|satellite 2021|satellite check)\\)")   # source tags of the no-go reasons
PL28_SRC_NAME = {u"survey": u"survey (Bergama_Altlik.3dm)", u"satellite 2021": u"ESA WorldCover 2021",
                 u"satellite check": u"satellite check (OPEN_CHECK)"}


# v28 (revision 29 Oct, WO-T4b-1): ground_page (crop mp_max_area, the open ground page) is gone with p.22 (D1 a:
# merged into the site board's p.06), and with it r28_open_ground.json (no reader since site board v51).
# ---- MIRAQUA round 28 Oct 2026 (masterplan v27): p.24 the two 1:1,000 plans in the fade-out programme language (worker MP-detail). Shared pieces: common/r28_style.py,
# common/units.py, common/label_place.py, common/figures.py (revision_2026-10-28/PLAN.md).
# v27 (MIRAQUA 28 Oct, P24.1-P24.5, F11): the two 1:1,000 windows (crops dt_upstream, dt_k5; DT_WINDOWS, their frames,
# DT_SCALE, the scale bars and the crops kept) in the programme-diagram language of the references: p24_ref2 (faint
# grey plan, soft fields fading into each other, one big bold word per field, small grey words for the sub-spaces, a
# dot legend) and p24_ref1 (translucent overlaps that mix). Layers, bottom up: the survey as a faint grey underlay ->
# the programme fields (R28_ZONES, stepped translucent rings) -> terrace edges, canopied walk, stepping stones -> the
# water route 1-4 in one line language (line, arrowhead, numbered dot) -> study-area outline (G8) -> the levels at the
# channel cuts -> words (common/label_place, G4). Gone: the ochre programme rings and the hub and café pictograms
# (P24.3), plant codes and band letters (P24.4, F11), survey spot heights, terrace-step sketches and ramps (P24.5),
# the flood bands across the stream (F11: they read as cut lines).
# The programmes of the masterplan's data, each mapped to one R28_ZONES key (shared with the senses page, MP-senses):
#   reed      zone base WT (cleansing reed basins) and WD (spillway); the corridor's reed side arms
#   terraces  WS (dry-top retention terraces); the corridor's terrace edges on the contours (R28DT_TERR_M either side)
#   hub       the corridor's dry hub squares (K3, K4, K5, İstiklal); their programme rings (H1) are now its fade
#   subhub    the bed stations of the sub-hubs (R28DT_SUB_M[0] round the station line), fading along the amphibious
#             bed WA (tier W) within R28DT_SUB_M[1] of the station
#   demeter   DG (Demeter's Garden)
#   forest    the corridor's forest cells (FOREST), its tree-planted cells (TREES, one step lighter), GR (shaded walk,
#             raised dry top)
#   wetland   the corridor's widened stream; WA flood terrace (tier F); WP (floodable riverside planting)
#   cafe      R28DT_CAFE_M round the café points (the GR and DG zones, where v26 drew the café pictograms)
# Fields, steps and sizes are graphic (a design reading of the zones), never areas: the figures stay the zone curves'.
R28DT_STEP_M = 4.0                   # one fade step, m
R28DT_HALO, R28DT_INSET = 3, 2       # steps round a field (fading out) and inside it (denser to its core)
R28DT_A = 0.075                      # opacity of one step: they add up to about 0.37 at a field's core (G6: light)
R28DT_A_ZONE = {"forest": 0.06}      # the corridor's long background field a little lighter
R28DT_CAFE_M = 8.0                   # a café field: this far round its point, m
R28DT_SUB_M = (6.0, 60.0)            # sub-hub: this far either side of its station line; the bed within this far of it
R28DT_TERR_M = 4.0                   # terraces: this far either side of a terrace edge, m
R28DT_ARM_M = 3.0                    # reed side arm: this far either side of its line, m
R28DT_WET = ("reed", "wetland", "subhub")    # fields that may also fade over the bed (the others over open ground)
R28DT_ORDER = ("forest", "terraces", "wetland", "reed", "demeter", "hub", "subhub", "cafe")   # drawn in this order
R28DT_TS = dict(zone=4.2, place=3.5, label=2.65, small=2.47)   # mm at 1:1: 12, 10, 7.5, 7 pt (booklet type sizes)
R28DT_TITLE_MM2 = 60.0               # a field shows less than this on a window: no title there (mm², = m² at 1:1,000)
R28DT_ROUTE = dict((k_, c_) for k_, _, c_ in R28_MARKERS)["water"]   # the water route = p.23's water markers
R28DT_CODE = {("WT", None): "reed", ("WD", None): "reed", ("WS", None): "terraces", ("DG", None): "demeter",
              ("GR", None): "forest", ("WA", "F"): "wetland", ("WP", None): "wetland", ("WA", "W"): "subhub"}
# v28 (WO-T4b-3): R28DT_SUB is gone: p.24 names its species from common/plants.py (P24_SPECIES, pages/p24_detail.py).


def _r28_nb(c):
    return ((1, 0, c), (-1, 0, c), (0, 1, c), (0, -1, c), (1, 1, c * 1.4142), (-1, 1, c * 1.4142),
            (1, -1, c * 1.4142), (-1, -1, c * 1.4142))


def _r28_depth(C, K, dmax):
    """{cell: m} how deep each cell of set K lies inside it (from its edge cells, c / 2), up to dmax."""
    G = C.G
    nx, ny, c = G.nx, G.ny, G.c
    d, hp = {}, []
    for n in K:
        i, j = n % nx, n // nx
        if i == 0 or j == 0 or i == nx - 1 or j == ny - 1 or (n - 1) not in K or (n + 1) not in K or \
                (n - nx) not in K or (n + nx) not in K:
            d[n] = c * 0.5
            hp.append((c * 0.5, n))
    heapq.heapify(hp)
    nb = _r28_nb(c)
    while hp:
        dd, n = heapq.heappop(hp)
        if dd > d.get(n, 1e9):
            continue
        i, j = n % nx, n // nx
        for di, dj, w in nb:
            ii, jj = i + di, j + dj
            if 0 <= ii < nx and 0 <= jj < ny:
                m = jj * nx + ii
                e = dd + w
                if e <= dmax and m in K and e < d.get(m, 1e9):
                    d[m] = e
                    heapq.heappush(hp, (e, m))
    return d


def _r28_spread(C, base, allow):
    """{cell: strength}: the strongest of base[m] less one per R28DT_STEP_M from m, over cells allow(n); kept while
    it is 1 or more (the faintest step)."""
    G = C.G
    nx, ny = G.nx, G.ny
    v = dict(base)
    hp = [(-s, n) for n, s in base.items()]
    heapq.heapify(hp)
    nb = [(di, dj, w / R28DT_STEP_M) for di, dj, w in _r28_nb(G.c)]
    while hp:
        s, n = heapq.heappop(hp)
        s = -s
        if s < v.get(n, 0.0):
            continue
        i, j = n % nx, n // nx
        for di, dj, w in nb:
            ii, jj = i + di, j + dj
            if 0 <= ii < nx and 0 <= jj < ny:
                m = jj * nx + ii
                e = s - w
                if e >= 1.0 - 1e-6 and e > v.get(m, 0.0) + 1e-9 and (m in base or allow(m)):
                    v[m] = e
                    heapq.heappush(hp, (-e, m))
    return v


def _r28_loops(C, cells):
    """Smooth survey rings (m) of a cell set: outer rings counter-clockwise, holes clockwise (fill even-odd)."""
    out = []
    for Lp in trace(C.G, set(cells)):
        Q = smooth(Lp, C.G.c * 0.5, 2)
        if len(Q) >= 3 and abs(area2(Q)) > 4.0 * C.G.c * C.G.c:
            out.append([C.V.xy(u, v) for u, v in Q])
    return out


def r28_zone_strength(C):
    """{zone key: (own cells {cell: base}, strength {cell: s})} of every R28_ZONES field over the whole frame, on the
    corridor's grid, worked out once a press (kept on C). A zone's own cells are R28DT_HALO + 1 at its edge and up to
    R28DT_INSET more inside (one per R28DT_STEP_M of depth); its lighter part (tree-planted cells, the amphibious bed
    near a sub-hub) R28DT_HALO or less; round them the strength drops by one per R28DT_STEP_M over open ground (the
    water fields also over the bed). Fade step t = the cells of strength t or more."""
    got = getattr(C, "_r28_v", None)
    if got is not None:
        return got
    G, V, F, Dst, N = C.G, C.V, C.F, C.Dst, C.N
    core = dict((k_, set()) for k_, _, _ in R28_ZONES)
    light = dict((k_, {}) for k_, _, _ in R28_ZONES)
    cells_of = lambda P: G.poly_cells([V.uv(p) for p in P])

    def along(P, r):
        out = set()
        for p in densify(P, G.c * 0.5):
            out.update(C.near_cells(p, r))
        return out
    bed, other = [], set()
    for z in C.D.zones:
        key = R28DT_CODE.get((z["code"], z["tier"])) or R28DT_CODE.get((z["code"], None))
        if key == "subhub":
            bed.append(cells_of(z["P"]))
        elif key:
            core[key].update(cells_of(z["P"]))
        else:
            other.add(z["code"] + (z["tier"] or u""))
        if z["code"] in ("GR", "DG"):
            core["cafe"].update(C.near_cells(z["q"], R28DT_CAFE_M))
    if other:
        C.warn.append(u"p.24 fields: zone codes with no programme field (R28_ZONES): " + u", ".join(sorted(other)))
    r0, reach = R28DT_SUB_M
    for h in C.hubs:
        for L_ in h.get("square") or []:
            core["hub"].update(cells_of(L_))
        s = h.get("sub_xy")
        if not s:
            continue
        a, b = s["a"], s["b"]
        for n in C.near_cells(s["c"], math.hypot(b[0] - a[0], b[1] - a[1]) / 2.0 + r0):
            x, y = C.wxy(n)
            if seg_dist(x, y, a, b) <= r0:
                core["subhub"].add(n)
        for cs in bed:                                   # the amphibious bed near the station, fading along the bed
            for n in cs:
                x, y = C.wxy(n)
                d = math.hypot(x - s["c"][0], y - s["c"][1])
                if d < reach:
                    lv = float(R28DT_HALO - int(R28DT_HALO * d / reach))
                    if lv > light["subhub"].get(n, 0.0):
                        light["subhub"][n] = lv
    for w_ in C.widen:
        core["wetland"].update(cells_of(w_["ring"]))
    for a_ in C.arms:
        core["reed"].update(along(a_["P"], R28DT_ARM_M))
    for P in C.terr:
        core["terraces"].update(along(P, R28DT_TERR_M))
    dh = C.dh
    for n in range(N):                                   # the corridor's planting rule (Corridor.planting), per cell
        if F[n] != 0 or Dst[n] > TREES[1]:
            continue
        if FOREST[0] <= Dst[n] <= FOREST[1] and dh[n] >= FOREST[2]:
            core["forest"].add(n)
        elif TREES[0] <= Dst[n] and dh[n] >= TREES[2]:
            light["forest"][n] = float(R28DT_HALO)
    out = {}
    for key, _, _ in R28_ZONES:
        K, base = core[key], {}
        if K:
            dep = _r28_depth(C, K, R28DT_INSET * R28DT_STEP_M)
            for n in K:
                base[n] = R28DT_HALO + 1.0 + min(float(R28DT_INSET), dep.get(n, 1e9) / R28DT_STEP_M)
        for n, lv in light[key].items():
            if n not in base:
                base[n] = lv
        if not base:
            continue
        if key in R28DT_WET:
            allow = lambda m: F[m] == 0 or F[m] == 3
        else:
            allow = lambda m: F[m] == 0
        out[key] = (base, _r28_spread(C, base, allow))
    C._r28_v = out
    return out


def _r28_base_cols():
    """The faint survey underlay's tones, mixed from the base map colours (COL, as load_palette set them)."""
    return {"bed": mix(COL["white"], COL["river"], 0.30), "bld": mix(COL["white"], COL["bld"], 0.60)}


def detail_legend():
    """v27 (MIRAQUA 28 Oct, P24.1; was 02b_detail.py): the detail sheet's legend groups, only what its windows draw:
    the programme fields, the water route and levels, the survey underlay and the study area (G8)."""
    cl = _r28_base_cols()
    st = R28_STUDY_LINE

    def zone_sw(hx):
        def f(pg, x, y, w, h):
            for i in range(R28DT_HALO + 1 + R28DT_INSET):
                pg.circle(x + w / 2.0, y + h / 2.0, h * 0.5 * (1.0 - 0.14 * i), fill=hx, alpha=R28DT_A)
        return f

    def line_sw(colour, lw, dash=None, alpha=None):
        def f(pg, x, y, w, h):
            pg.line([(x, y + h / 2), (x + w, y + h / 2)], colour, lw, dash, cap=0 if dash else 1, alpha=alpha)
        return f

    def route_sw(pg, x, y, w, h):
        cy = y + h / 2
        pg.line([(x + 3.8, cy), (x + w - 1.6, cy)], R28DT_ROUTE, 0.6, cap=1)
        pg.poly([[(x + w, cy), (x + w - 1.8, cy + 0.76), (x + w - 1.8, cy - 0.76)]], fill=R28DT_ROUTE)
        pg.circle(x + 1.9, cy, 1.9, fill=R28DT_ROUTE)
        pg.text(u"1", x + 1.9, cy - R28DT_TS["small"] * 0.36, R28DT_TS["small"], COL["white"], bold=True, align="C")

    def cross_sw(pg, x, y, w, h):
        cx, cy = x + w / 2, y + h / 2
        pg.line([(cx - 1.4, cy), (cx + 1.4, cy)], COL["ink_dark"], 0.3)
        pg.line([(cx, cy - 1.4), (cx, cy + 1.4)], COL["ink_dark"], 0.3)

    def stones_sw(pg, x, y, w, h):
        for i in range(5):
            pg.circle(x + w * (i + 0.5) / 5, y + h / 2, 0.8, fill=COL["ink2"], alpha=0.7)

    def none_sw(pg, x, y, w, h):
        return None
    zones = [(lab, zone_sw(hx)) for key, lab, hx in R28_ZONES if ("r28z", key) in LEG]
    water = [(nm, f) for key, nm, f in (
        (("r28dt", "route"), u"Water route · step", route_sw),
        (("r28dt", "level"), u"Level at a channel cut (m): bed, Q100, Q500", cross_sw),
        (("r28dt", "terr"), u"Terrace edge on a contour", line_sw(R28_ZONE["terraces"][1], 0.3, None, 0.8)),
        (("r28dt", "canopy"), u"Canopied walk", line_sw(R28_ZONE["forest"][1], 0.3, [1.2, 0.9], 0.9)),
        (("r28dt", "stones"), u"Stepping stones", stones_sw),
        (("r28dt", "foot"), u"New footbridge", line_sw(COL["ink"], 0.5)),
        (("r28dt", "hidden"), u"Hidden stream line", line_sw(COL["river_mid"], 1.2, [1.6, 0.9], 0.7))) if key in LEG]
    if ("dt", "vol") in LEG:                             # v22: how the rough volumes are made
        water.append((u"~ m³ = rough volume, area × depth · reed basins 0.46 m · terraces: Q100 over bed +1 m "
                      u"at the nearest cut", none_sw))   # (sentence case, as this legend's other lines)
    surv = [(nm, f) for key, nm, f in (
        (("r28dt", "bed"), u"Stream bed", _sw_fill(cl["bed"])),
        (("r28dt", "contour"), u"Contour", line_sw(COL["contour10"], 0.3)),
        (("r28dt", "bld"), u"Building", _sw_fill(cl["bld"])),
        (("r28dt", "her"), u"Heritage building", _sw_fill(cl["bld"], COL["her_edge"])),
        (("r28dt", "since"), u"Built since the survey", _sw_fill(cl["bld"], stripes=(COL["ink2"], 0.8, 0.12, 45.0))),
        (("r28dt", "street"), u"Street edge", line_sw(COL["ink2"], 0.3, None, 0.4)),
        (("r28dt", "bridge"), u"Bridge", line_sw(COL["ink"], 0.4)),
        (("r28dt", "study"), R28_STUDY_NAME, line_sw(st["colour"], st["width_mm"], list(st["dash_mm"])))) if key in LEG]
    return [(u"PROGRAMME", zones), (u"WATER · LEVELS", water), (u"SURVEY", surv)]
# ---- MIRAQUA round 28 Oct 2026 (masterplan v27): S1 the senses and the water, a new A3 sheet after p.15 (worker MP-senses). Shared pieces: common/r28_style.py,
# common/units.py, common/label_place.py, common/figures.py (revision_2026-10-28/PLAN.md).

# ================================================================ v27 (MIRAQUA 28 Oct, S1): the senses and the water
# BRIEF v4 §3 (revision_2026-10-28/v4/BRIEF.md; PLAN §3 row S1): a new one-page A3 sheet, Bergama_senses_A3.pdf, with
# its own title, for the booklet right after "The S4 cut". Not analysis: what the fade-out programme areas give the
# senses, from the upstream entry to the downstream end, as SIX SEPARATE STRIPS on one page (never one stacked map):
# the base map (the stream and the fade-out zones, R28_ZONES) and five panels on the SAME strip frame, orientation
# and scale, so they compare side by side. G7: each strip is the whole analysis frame (site_alan) turned so the
# water runs left to right (the View of the corridor), at 1:20,000, the largest standard scale at which six strips
# fit the A3 page (1:10,000 strips are 52.9 mm tall: six need 317 mm of the 243 mm). G8: the calisma_alan outline in
# every strip (R28_STUDY_LINE), named in the base map's legend. Each panel in the language of its reference
# (v4/references): Feeling = emotion blots gathering at the hubs and thinning out (senses_ref1), Sound = one mark
# texture per source (ref5), Smell = contour rings round each source (ref4), Encounters = flow ribbons ending in
# vignettes watch / walk / touch / cross / remember (ref3), History = layered fade fields with one word (ref2); the
# zones as p.24's fade-out fields (p24_ref2, the same zone definitions and colours). Every source sits at a place of
# the masterplan's own data (hubs, sub-hubs, zones, bridges, roads, the corridor's moves, the water board's S4 cut);
# how strong each reads is a design reading (said on the sheet), never a measurement: no numbers on the panels.
SN_NAME = "Bergama_senses_A3.pdf"            # PLAN §3: fixed name, no version (the booklet's sheet page after p.15)
SN_TITLE = u"The senses and the water"
SN_KICKER = u"C   WATER   ·   WHAT WE DO WITH IT"   # the booklet's header line of p.15 (part C, stage "do")
SN_SCALE = 20000.0                           # every strip (R28_SCALES; see above)
SN_K = 1000.0 / SN_SCALE                     # page mm per survey m
SN_PW, SN_PH, SN_ML = 420.0, 297.0, 14.0     # the booklet's A3 page and margin (bergama_booklet PW, PH, ML)
SN_COLX = (14.0, 212.0)                      # the two cell columns: 6 booklet grid columns each (6 x 33 - 4 = 194 mm)
SN_ROWS = (34.0, 115.5, 197.0)               # cell tops, mm from the page top (the last cell ends at 273, the
SN_CW, SN_CH = 194.0, 76.0                   # booklet's footer rule is at 276: its footer stays free)
SN_TOP = 17.5                                # the strip frame's top below its cell's top, mm
SN_SIDE = 148.0                              # the cell's key column from the cell's left edge, mm (46 mm wide)
SN_PT = 25.4 / 72.0                          # mm per point
SN_TS = dict(kicker=8.0, title=24.0, panel=14.0, statement=9.5, label=7.5, small=7.0)   # pt: booklet T sizes
SN_INK, SN_INK2, SN_ACC, SN_RULE, SN_FRAME = "4A3F35", "6B645B", "8B3A3F", "B0AC9C", "D8D5CC"   # booklet colours
SN_DARK, SN_WATER, SN_WATER_MID = "2C2219", R28_OPEN["stream"], "5D7F8D"
# The water board's S4 cut (site board v48 05_build_terrain.py S4_WB, survey m): where its season rows put "Kermes
# stalls in the bed" and "feet in the strip"; the sheet takes the point where it crosses the stream line
SN_S4 = ((30616.354683, 30540.470648), (31489.513378, 31161.826317))
SN_ZONE_SHORT = {"reed": u"Reed basins", "terraces": u"Terraces", "hub": u"Hub squares", "subhub": u"Sub-hubs",
                 "demeter": u"Demeter's Garden", "forest": u"Forest corridor", "wetland": u"Wetland", "cafe": u"Café"}
# Feeling (senses_ref1's circular scale): four poles, active / passive up and down, positive / negative right and
# left; a mood's colour is its angle on the wheel (design readings). New colours for a new meaning, apart from each
# other (dE00 >= 26) and from the base map (>= 16)
SN_FEEL = ((0.0, "C7A43A"), (90.0, "D0663E"), (180.0, "8C68A6"), (270.0, "4C8DB8"))   # positive, active, negative, passive
SN_MOOD = {"lively": 45.0, "busy": 80.0, "play": 10.0, "calm": 305.0, "tense": 140.0, "hidden": 220.0}
# Sound (senses_ref5): one mark and colour per source, all palette v1.4 tones
SN_SOUND = (("water", u"Running water", "5D7F8D"), ("reeds", u"Reeds", R28_ZONE["reed"][1]),
            ("birds", u"Birds", COL["tree_mid"]), ("children", u"Children", "7F5B7B"),
            ("voices", u"Market · Kermes", "C2603A"), ("traffic", u"Traffic", SN_DARK), ("wind", u"Wind", SN_RULE))
# Smell (senses_ref4): each source in the colour of the zone it grows in where it is one, else palette v1.4
# v28.1 (D2, D6): reed beds = the lined basins only; water mint left out (it grows only in lined cells, not drawn here)
SN_SMELL = (("reeds", u"Reed beds", R28_ZONE["reed"][1]),
            ("lavender", u"French lavender", R28_ZONE["terraces"][1]),   # p.16's plant list (no rosemary there)
            ("demeter", u"Demeter's Garden", R28_ZONE["demeter"][1]), ("cafe", u"Café", R28_ZONE["cafe"][1]),
            ("olive", u"Olive harvest", MP["agriculture"][2]))
# Encounters (senses_ref3): (key, word, colour, figure pose); walk = reach on foot, touch = water, cross = crossings,
# remember = heritage (R28_REACH / R28_MARKERS), watch a deep blue apart from them (dE00 >= 16.8)
_SN_MK = dict((k, h) for k, _, h in R28_MARKERS)
SN_EXP = (("watch", u"Watch", "2F5F9E", "watch"), ("walk", u"Walk", R28_REACH[1][2], "walk"),
          ("touch", u"Touch", _SN_MK["water"], "touch"), ("cross", u"Cross", _SN_MK["crossings"], "wade"),
          ("remember", u"Remember", _SN_MK["heritage"], "stand"))
SN_HER = _SN_MK["heritage"]                  # History: the heritage colour (same meaning as p.23's markers)

# p.16 the senses and the water: senses_sheet and its sn_* helpers (split from parts/02e_r28_detail.py, parts/02f_r28_senses.py on 29 Oct 2026; moved unchanged)
# T4a (29 Oct 2026, WO-T4a-1, package E): the shared basemap (02 §1) under every strip, chosen per panel (D5) by
# P16_BASEMAP; the stream comes only from the basemap (never the corridor's own pieces); every strip is widened so its
# surroundings show and fills its cell (labels sit on the drawing); Encounters rebuilt as five lanes that meet at the
# hubs, Kermes and the flood zone; History with small photos beside its places. basemap.py and icons.py come from
# the masterplan core includes (T4b, v28).

# D5 (Aras 29 Oct): (mode, override) of the basemap per panel; senses_sheet(..., basemap={title: (mode, override)})
# changes a panel's choice for one run
P16_BASEMAP = {u"Zones": ("minimal", None),
               u"Feeling": ("minimal", {"streets": False, "buildings": False}),
               u"Sound": ("minimal", {"streets": ("main",), "buildings": False}),
               u"Smell": ("minimal", {"streets": False, "buildings": False}),
               u"Encounters": ("minimal", None),
               u"History": ("minimal", None)}
P16_STRIP_TOP = 10.5                         # mm: the strip's top below its cell's top (title, then the bridge ruler)
P16_STRIP_H = 62.0                           # mm: every strip's height (1,240 m across at 1:20,000; the cell is 76)
P16_PHOTO_DIR = os.path.join(DATA_DIR, "heritage_photos")   # the run kit's photo folder (p.21's contract)
P16_PHOTO_CSV = "photos.csv"
P16_PHOTO_W, P16_PHOTO_H = 22.0, 16.5        # mm: one History photo (4:3, cropped to fill)
# History photos: own site photos by file name (no credit, D13) first, else a photos.csv row whose place or file
# name holds an alias (Commons: its credit line is printed). v29 (Aras 30 Oct "ok to use kermes photos"): Kermes takes
# the DHA photo with its credit line.
P16_PLACES = (
    dict(key="hamam", cap=(u"Tabaklar Hamamı",), own=(u"tabaklar_hamami_1.jpg", u"tabaklar_hamami_2.jpg"),
         alias=(u"tabaklarhamami",)),
    dict(key="tabakhane", cap=(u"Tabakhane",), own=(u"tabakhane_1.jpg",), alias=(u"tabakhane",),
         notalias=(u"koprusu",)),
    dict(key="k3", cap=(u"Tabak Köprüsü", u"Roman bridge · K3"), own=(u"tabak_koprusu_1.jpg", u"tabak_koprusu_2.jpg"),
         alias=(u"tabakkoprusu",)),
    dict(key="k5", cap=(u"Üç Kemer Köprüsü", u"Roman bridge · K5"), own=(), alias=(u"uckemer",)),
    dict(key="tunnels", cap=(u"Kızıl Avlu", u"tunnels"), own=(), alias=(u"tunnel",)),
    dict(key="kermes", cap=(u"Kermes",), own=(), alias=(u"kermes",)))      # v29: DHA photo, credit printed
# Encounters: where the lines meet (kind, word, icon of common/icons.py), in the order they rank when two coincide
P16_MEET = (("hub", u"Hub", "hub"), ("kermes", u"Kermes", "market"), ("flood", u"Flood zone", "high_water"))
_P16_MEMO = {}


def r28_zone_fields(C):
    """[(zone key, rings)]: each R28_ZONES programme field over the whole frame (its own cells: core and lighter
    part, no fade), survey m, closed rings (fill even-odd), in R28_ZONES order; worked out once a press (kept on C).
    Shared helper: the senses page (MP-senses) builds its fade-out zones from the same fields."""
    got = getattr(C, "_r28_fields", None)
    if got is None:
        S = r28_zone_strength(C)
        got = [(k_, _r28_loops(C, list(S[k_][0]))) for k_, _, _ in R28_ZONES if k_ in S]
        got = [(k_, r_) for k_, r_ in got if r_]
        C._r28_fields = got
    return got


def sn_y(td):
    """mm from the page top -> page y (the sheet is drawn y up)"""
    return SN_PH - td


def sn_mm(pt):
    return pt * SN_PT


def sn_rich(pg, x, y, runs, pt, colour):
    """one line of [(text, bold)] runs (G5: the bold keywords inside a line); its width, mm"""
    size = sn_mm(pt)
    w0 = x
    for t, b in runs:
        pg.text(t, x, y, size, colour, bold=b)
        x += text_w(t, size, b)
    return x - w0


def sn_ring(cx, cy, r, seed=0, amp=0.0, n=40, lobes=(2, 3, 5)):
    """an organic closed ring round (cx, cy): radius r with a smooth wobble of about amp x r (the same seed gives
    the same wobble, so rings of one source read as contours)"""
    rnd = random.Random(seed)
    ph = [rnd.uniform(0.0, 2.0 * math.pi) for _ in lobes]
    out = []
    for i in range(n):
        a = 2.0 * math.pi * i / n
        k = 1.0 + sum(amp / (j + 1.0) * math.sin(L * a + p) for j, (L, p) in enumerate(zip(lobes, ph)))
        out.append((cx + r * k * math.cos(a), cy + r * k * math.sin(a)))
    return out


def sn_disc(c, r, n=20):
    return sn_ring(c[0], c[1], r, 0, 0.0, n)


def sn_normals(P):
    out = []
    for i in range(len(P)):
        a, b = P[max(0, i - 1)], P[min(len(P) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        out.append((-dy / L, dx / L))
    return out


def sn_band(P, w, taper=0.0):
    """the outline of a band of half-width w round polyline P (any units); taper = the share of the length over
    which each end narrows (0: square ends)"""
    Q = [tuple(P[0])] if P else []
    for p in P[1:]:
        if math.hypot(p[0] - Q[-1][0], p[1] - Q[-1][1]) > 1e-6:
            Q.append(tuple(p))
    if len(Q) < 2:
        return []
    s = arclen(Q)
    L = s[-1] or 1.0
    lt, rt = [], []
    for p, n_, t in zip(Q, sn_normals(Q), s):
        ww = w
        if taper > 0.0:
            f = min(1.0, t / (taper * L), (L - t) / (taper * L))
            ww = w * math.sqrt(max(0.0, math.sin(f * math.pi / 2.0)))
        lt.append((p[0] + n_[0] * ww, p[1] + n_[1] * ww))
        rt.append((p[0] - n_[0] * ww, p[1] - n_[1] * ww))
    return lt + rt[::-1]


def sn_along(P, step):
    """points every step along polyline P (same units)"""
    if len(P) < 2:
        return list(P)
    s = arclen(P)
    out, t = [], 0.0
    while t <= s[-1]:
        out.append(at_len(P, s, t)[0])
        t += step
    return out


def sn_spaced(pts, T, gap):
    """the points of pts at least gap page mm apart (first come first kept)"""
    out, at = [], []
    for p in pts:
        q = T(p)
        if all(math.hypot(q[0] - a[0], q[1] - a[1]) >= gap for a in at):
            out.append(p)
            at.append(q)
    return out


def sn_in(bb, box, m=0.0):
    return bb[2] >= box[0] - m and bb[0] <= box[2] + m and bb[3] >= box[1] - m and bb[1] <= box[3] + m


def sn_vcent(P):
    return (sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P))


def sn_T(V, x0, y0, u0=None, v0=None):
    """survey m -> page mm of a strip whose frame's lower-left corner is (x0, y0): the corridor's View (site_alan
    turned so the water runs left to right, the north-east bank on top) at 1:20,000; (u0, v0) = the widened frame's
    lower-left corner in the View (default the View's own)"""
    c_, s_, cx, cy = V.c, V.s, V.cx, V.cy
    u0 = V.u0 if u0 is None else u0
    v0 = V.v0 if v0 is None else v0

    def T(p):
        dx, dy = p[0] - cx, p[1] - cy
        return (x0 + (dx * c_ + dy * s_ - u0) * SN_K, y0 + (-dx * s_ + dy * c_ - v0) * SN_K)
    return T


def sn_page_ang(V, d):
    """page angle (radians) of the survey direction d in the strip"""
    return math.atan2(-d[0] * V.s + d[1] * V.c, d[0] * V.c + d[1] * V.s)


def sn_on_ref(G, q):
    """the point of the stream line nearest q"""
    ref = G["ref"]
    if q is None or len(ref) < 2:
        return q
    return at_len(ref, G["sref"], chain_at(ref, q)[0])[0]


def sn_ref_piece(G, q, half):
    """the stream line half m either side of the point nearest q"""
    ref, s = G["ref"], G["sref"]
    if q is None or len(ref) < 2:
        return []
    c, _ = chain_at(ref, q)
    return sub_line(ref, s, max(0.0, c - half), min(s[-1], c + half))


def sn_seg_cross(ref, a, b):
    """where segment a-b first crosses polyline ref, else None"""
    for p, q in zip(ref, ref[1:]):
        rx, ry, sx, sy = b[0] - a[0], b[1] - a[1], q[0] - p[0], q[1] - p[1]
        d = rx * sy - ry * sx
        if abs(d) < 1e-12:
            continue
        t = ((p[0] - a[0]) * sy - (p[1] - a[1]) * sx) / d
        u = ((p[0] - a[0]) * ry - (p[1] - a[1]) * rx) / d
        if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
            return (a[0] + t * rx, a[1] + t * ry)
    return None


# ---------------------------------------------------------------- the zones (ONE set with p.24)
def sn_zone_fields(C):
    """[(R28_ZONES key, [rings, survey m])] read from the masterplan's own design, as the plans draw it: reed basins
    = the zone base's WT zones + the corridor's reed side arms; terraces = WS zones + the terrace edges on the
    contours; hub squares = the corridor's dry hub squares; sub-hubs = the bed station at each hub (its width);
    Demeter's Garden = DG zones; forest corridor = the planting rule's band (FOREST: open ground 6-32 m from the
    water, 110 m or more from a hub); widened stream / wetland = the widened reaches; café = the café places of
    the plan (GR and DG zones). Used when MP-detail's r28_zone_fields (p.24) is not there."""
    out = {}

    def add(k, rings):
        out.setdefault(k, []).extend([R for R in rings if len(R) >= 3])
    for z in C.D.zones:
        if z["code"] == "WT":
            add("reed", [z["P"]])
        elif z["code"] == "WS":
            add("terraces", [z["P"]])
        elif z["code"] == "DG":
            add("demeter", [z["P"]])
        if z["code"] in ("GR", "DG"):
            add("cafe", [sn_disc(z["q"], 12.0)])
    for a in C.arms:
        add("reed", [sn_band(a["P"], 6.0, 0.15)])
    for P in C.terr:
        add("terraces", [sn_band(P, 4.0, 0.15)])
    for h in C.hubs:
        add("hub", h.get("square") or [])
        s = h.get("sub_xy")
        if s:
            add("subhub", [sn_disc(s["c"], max(8.0, s["w"] / 2.0))])
    add("wetland", [w["ring"] for w in C.widen])
    dh = getattr(C, "dh", None)
    if dh is not None:
        d0, d1, hmin, _ = FOREST
        F, Dst = C.F, C.Dst
        add("forest", C.loops([n for n in range(C.N) if F[n] == 0 and d0 <= Dst[n] <= d1 and dh[n] >= hmin], True))
    else:
        add("forest", [sn_disc(p, 9.0, 10) for p in C.forest])
    return [(k, out[k]) for k, _, _ in R28_ZONES if out.get(k)]


def sn_fields(C, warn):
    """(fields, source): MP-detail's r28_zone_fields(C) (p.24, 02e) when it gives valid rings, else sn_zone_fields"""
    f = globals().get("r28_zone_fields")
    if callable(f):
        try:
            got = [(k, [ring(list(R)) for R in rs if len(R) >= 3]) for k, rs in f(C) if k in R28_ZONE]
            got = [(k, [R for R in rs if len(R) >= 3]) for k, rs in got]
            got = [(k, rs) for k, rs in got if rs]
            if got:
                return got, u"r28_zone_fields"
        except Exception as ex:
            warn.append(u"senses sheet: r28_zone_fields not used ({}: {}); its own reading of the zones".format(
                type(ex).__name__, ex))
    return sn_zone_fields(C), u"own reading"


def sn_data(C, areas, warn):
    """everything the six strips draw, in survey m, read once from the corridor (C) and the working areas"""
    ref = [tuple(p) for p in (C.ref or [])]
    G = {"V": C.V, "ref": ref, "sref": arclen(ref) if len(ref) >= 2 else [0.0],
         "covered": [P for P in (C.covered or []) if len(P) >= 2], "bed": list(C.bed_loops or []),
         "streams": list(C.streams or []), "study": [ring(list(A)) for A in (areas or {}).values()],
         "bld": [P for role in ("building", "housing", "heritage", "shed") for P in C.bld.get(role, [])],
         "hubs": list(C.hubs), "hub": dict((h["id"], h) for h in C.hubs), "zones_raw": list(C.D.zones),
         "arms": list(C.arms), "terr": list(C.terr), "widen": list(C.widen), "forest": list(C.forest),
         "canopy": list(C.canopy), "cross": list(C.cross), "terrace": C.terrace}
    if not G["study"]:
        warn.append(u"senses sheet: no calisma_alan outline: the study area is not drawn")
    G["fields"], G["fields_src"] = sn_fields(C, warn)
    G["bath"] = next((xy for nm, xy in PLACES if u"TABAKLAR" in nm), None)
    G["kermes"] = sn_seg_cross(ref, SN_S4[0], SN_S4[1]) or sn_on_ref(G, sn_vcent(list(SN_S4)))
    _p16_frame(G, C.V)
    _p16_basemap(G, warn)
    G["traffic"] = [(rd["xy"], rd["change"]) for rd in ROADS
                    if u"Cami Kebir" in rd["name"] or u"Adnan Menderes" in rd["name"]]   # K4 and K6 (BRIEF §3)
    G["market"] = []
    try:                                                 # city link's stops: the bank bazaar, the producers' market
        for f_ in city_link()[0].get("functions", []):
            nm = (f_.get("name") or u"").lower()
            if f_.get("xy") and (u"bazaar" in nm or u"market" in nm):
                G["market"].append(tuple(f_["xy"]))
    except Exception:
        pass
    return G


# ---------------------------------------------------------------- the strip frame every panel shares
def _p16_frame(G, V):
    """T4a: the widened strip frame in the View (u0, v0, u1, v1), the same for all six strips: the analysis frame
    grown to the strip width the cell allows (SN_SIDE - 4 mm) and to P16_STRIP_H tall at 1:20,000, so the stream
    reads with its surroundings; G["bm_box"] = its survey bounding box (the basemap's cull box)"""
    sw0, sh0 = (V.u1 - V.u0) * SN_K, (V.v1 - V.v0) * SN_K
    pu = max(0.0, (SN_SIDE - 4.0 - sw0) / 2.0) / SN_K
    pv = max(0.0, (P16_STRIP_H - sh0) / 2.0) / SN_K
    fr = (V.u0 - pu, V.v0 - pv, V.u1 + pu, V.v1 + pv)
    G["fr"] = fr
    G["bm_box"] = tuple(bbox([V.xy(u, v) for u, v in ((fr[0], fr[1]), (fr[2], fr[1]), (fr[2], fr[3]),
                                                       (fr[0], fr[3]))]))


def _p16_basemap(G, warn):
    """T4a: the shared basemap's data, read once a run (common/basemap.py); None without it (the site board writes
    it): the strips are then drawn without stream, streets and buildings, and the log says so (one line)"""
    D = None
    try:
        D = basemap_load(log=[])
    except Exception as ex:
        warn.append(u"senses sheet: basemap not read ({}: {})".format(type(ex).__name__, ex))
    if not D:
        warn.append(u"senses sheet: no basemap data (Downloads/Bergama/cached/basemap/basemap.json, written by the "
                    u"site board): the strips are drawn without stream, streets and buildings")
    G["bm"] = D or None


def _p16_bm_items(G, choice):
    """the basemap items of one panel: choice = (mode, override) of P16_BASEMAP (memoised by basemap_items)"""
    if not G.get("bm"):
        return []
    mode, ov = choice if choice else ("minimal", None)
    try:
        return basemap_items(mode, ov, G["bm_box"], G["bm"], True)
    except Exception as ex:
        k = ("bm_err", mode, repr(ov))
        if k not in _P16_MEMO:
            _P16_MEMO[k] = 1
            G.setdefault("warn", []).append(u"senses sheet: basemap {} not drawn ({}: {})".format(
                mode, type(ex).__name__, ex))
        return []


def _p16_bm_draw(pg, items, T):
    """the basemap items through this page's calls (even-odd fills: buildings come split, one fill each)"""
    def fill(rings, hx, a, nz):
        pg.poly(rings, fill=hx, alpha=a)

    def line(pts, hx, w, dash, a):
        pg.line(pts, hx, w, list(dash) if dash else None, cap=0 if dash else 1, alpha=a)
    basemap_draw(items, T, fill, line)


def _p16_bm_style(items):
    """what the basemap items of a panel draw, for its key: {water, edge, covered, street, bld} -> (hex, width or
    alpha, dash); only the kinds present"""
    out = {}
    for it in items:
        if it[0] == "fill":
            if it[2] == BM_COL["water"]:
                out.setdefault("water", (it[2], it[3], None))
            elif it[2] in (BM_FAINT["bld_veryfaint"], BM_FAINT["bld"], BM_COL["bld"]):
                out.setdefault("bld", (it[2], it[3], None))
        elif it[0] == "line":
            if it[4]:
                if it[2] in (BM_COL["water_edge"], BM_COL["water"]):
                    out.setdefault("covered", (it[2], it[3], list(it[4])))
            elif it[2] == BM_COL["water_edge"]:
                out.setdefault("edge", (it[2], it[3], None))
            elif abs(it[3] - BM_LW["main"]) < 1e-6:
                out.setdefault("street", (it[2], it[3], None))
    return out


def _p16_shapes(pg, shapes):
    """house shapes of common/icons.py ("poly", ring, fill, stroke, lw) / ("line", pts, colour, lw) on the page"""
    for sh in shapes or ():
        if sh[0] == "poly":
            pg.poly([sh[1]], fill=sh[2], stroke=sh[3], lw=sh[4] if len(sh) > 4 else 0.1)
        elif sh[0] == "line":
            pg.line(sh[1], sh[2], sh[3] if len(sh) > 3 else 0.1)


def sn_cell(pg, G, cx, top, title, choice=None):
    """one cell: its title, the strip frame (the widened analysis frame at 1:20,000, P16_STRIP_H tall), the shared
    basemap of this panel (choice = (mode, override), D5; the stream only from the basemap) and the bridge ruler on
    the frame's top edge. Returns the cell (T, box, label room: labels sit on the drawing, off the stream line)."""
    V, fr = G["V"], G["fr"]
    sw, sh = (fr[2] - fr[0]) * SN_K, (fr[3] - fr[1]) * SN_K
    x0, y1 = cx, sn_y(top + P16_STRIP_TOP)
    box = (x0, y1 - sh, x0 + sw, y1)
    T = sn_T(V, box[0], box[1], fr[0], fr[1])
    size = sn_mm(SN_TS["panel"])
    yt = sn_y(top + 5.0)
    pg.text(title, cx, yt, size, SN_INK, bold=True)
    refp = [T(p) for p in G["ref"]]
    cell = {"x": cx, "top": top, "box": box, "T": T, "side": cx + SN_SIDE,
            "bounds": (box[0] + 0.6, box[1] + 0.6, box[2] - 0.6, box[3] - 0.6),
            "taken": [(cx, yt - size * 0.25, cx + text_w(title, size, True) + 1.0, yt + size * 0.8),
                      (cx + SN_SIDE - 2.0, sn_y(top + SN_CH), cx + SN_CW, sn_y(top))],
            "segs": list(zip(refp, refp[1:]))}
    items = _p16_bm_items(G, choice)
    cell["bm_style"] = _p16_bm_style(items)
    if items:
        pg.clip([rect(*box)])
        _p16_bm_draw(pg, items, T)
        pg.unclip()
    xs = {}
    for nm, xy in BRIDGES_K:                             # the ruler: a tick per bridge, its name above the frame
        x = T(xy)[0]
        if box[0] <= x <= box[2]:
            pg.line([(x, box[3]), (x, box[3] - 1.0)], SN_INK2, 0.2)
            xs[nm] = x
    labs = ([(u"K1·K2", (xs["K1"] + xs["K2"]) / 2.0)] if "K1" in xs and "K2" in xs else []) + \
        [(nm, xs[nm]) for nm in ("K3", "K4", "K5", "K6") if nm in xs]
    fs = sn_mm(SN_TS["small"])
    ruler = []
    for s, x in labs:
        w = text_w(s, fs)
        xl = min(max(x - w / 2.0, box[0]), box[2] - w)
        b = (xl - 0.3, box[3] + 0.6, xl + w + 0.3, box[3] + 1.0 + fs * 0.8)
        if any(lp_hit(b, t) for t in ruler):
            continue
        pg.text(s, xl, box[3] + 1.0, fs, SN_INK2)
        ruler.append(b)
    return cell


def sn_outline(pg, G, cell):
    """G8: the study area (calisma_alan, both parts) in R28_STUDY_LINE, then the frame's own hairline"""
    st, T, box = R28_STUDY_LINE, cell["T"], cell["box"]
    pg.clip([rect(*box)])
    for A in G["study"]:
        Q = [T(p) for p in A]
        if len(Q) >= 3:
            pg.line(Q + Q[:1], st["colour"], st["width_mm"], list(st["dash_mm"]), cap=0)
    pg.unclip()
    pg.poly([rect(*box)], stroke=SN_FRAME, lw=0.15)


def sn_place(pg, cell, labs, warn):
    """G4 (common/label_place.py): each word round its place ON the strip (T4a: the widened frame has room), never
    on the stream line or a panel's own lines (cell["segs"]) or boxes (cell["taken"]), on a thin leader when off
    it; "more" = further places the same word points to. A word with no room is logged."""
    items = []
    for L_ in labs:
        size, b = sn_mm(L_.get("pt", SN_TS["label"])), L_.get("bold", True)
        items.append(dict(x=L_["at"][0], y=L_["at"][1], rank=L_.get("rank", 0),
                          wh=lambda f, s=L_["s"], size=size, b=b: (text_w(s, max(size * f, sn_mm(SN_TS["small"])), b),
                                                                   max(size * f, sn_mm(SN_TS["small"])) * 0.95)))
    got = place_labels_all(items, cell["taken"], cell["bounds"], cell.get("segs", ()),
                           sizes=(1.0, SN_TS["small"] / SN_TS["label"]))
    for i, L_ in enumerate(labs):
        if i not in got:
            if L_.get("rank", 0) == 0:
                warn.append(u"senses sheet: no room for the word '{}'".format(L_["s"]))
            continue
        bx, leader, f = got[i]
        size = max(sn_mm(L_.get("pt", SN_TS["label"])) * f, sn_mm(SN_TS["small"]))   # never under 7 pt
        pg.text(L_["s"], bx[0], bx[1] + size * 0.2, size, L_.get("col", SN_INK), bold=L_.get("bold", True))
        for k, a in enumerate([L_["at"]] + list(L_.get("more", ()))):
            if leader or k > 0:
                pg.line([a, lp_leader_end(bx, a)], SN_INK2, 0.15)
                pg.circle(a[0], a[1], 0.3, fill=SN_INK2)


def _p16_fig(pg, pose, x, y, h, colour, facing=1):
    """p.16's ONE figure point: the figure library's side view (common/figures.py fig_side; adult 1.70 m), h mm
    tall on this diagram (pictogram size, not to scale), feet at (x, y), one colour. "sit" = sit_chair."""
    k = h / 1.70
    _p16_shapes(pg, fig_side({"sit": "sit_chair"}.get(pose, pose), x, y, k, facing, ink=colour))


def sn_key_row(pg, x, y, word, pt=None):
    size = sn_mm(pt or SN_TS["label"])
    pg.text(word, x, y - size * 0.35, size, SN_INK)


# ---------------------------------------------------------------- Zones: the base map (p24_ref2 fade-out fields)
def sn_field(pg, rings, colour, core=0.42, halo=(1.3, 0.9, 0.5), ha=0.12):
    """a fade-out field: a translucent core and, outside its edge only, steps fading outward (no outline)"""
    rings = [Q for Q in rings if len(Q) >= 3]
    m = halo[0] + 1.0
    for Q in rings:
        bb = bbox(Q)
        pg.clip([rect(bb[0] - m, bb[1] - m, bb[2] + m, bb[3] + m), Q])
        for w in halo:
            pg.line(Q + Q[:1], colour, 2.0 * w, alpha=ha)
        pg.unclip()
    for Q in rings:
        pg.poly([Q], fill=colour, alpha=core)


def sn_zones(pg, G, cell, warn):
    T, box = cell["T"], cell["box"]
    labs = []
    pg.clip([rect(*box)])
    for key, rings in G["fields"]:
        name, hx = R28_ZONE[key]
        Ps = [Q for Q in ([T(p) for p in R] for R in rings) if len(Q) >= 3 and sn_in(bbox(Q), box)]
        if not Ps:
            continue
        sn_field(pg, Ps, hx)
        for Q in Ps:                                     # the words stay off the fields' edges
            Qs = Q[::max(1, len(Q) // 24)] + Q[:1]
            cell["segs"].extend(zip(Qs, Qs[1:]))
        at = inner_pt(max(Ps, key=lambda Q: abs(area2(Q))))
        labs.append(dict(s=SN_ZONE_SHORT.get(key, name), at=at, col=mix(hx, SN_DARK, 0.5)))
    pg.unclip()
    sx, top = cell["side"], cell["top"]                  # key column: what the strips draw, north, scale bar
    st, bs = R28_STUDY_LINE, cell.get("bm_style", {})
    y = sn_y(top + 4.0)
    rows = [(R28_STUDY_NAME, "study"), (u"Stream", "water"), (u"Hidden stream", "covered"), (u"Main streets", "street"),
            (u"Bridge", "bridge"), (u"Buildings", "bld"), (u"Water flow", "flow")]
    for word, kind in rows:
        if kind in ("water", "covered", "street", "bld") and kind not in bs:
            continue                                     # the key lists only what the basemap drew
        if kind == "study":
            pg.line([(sx, y), (sx + 9.0, y)], st["colour"], st["width_mm"], list(st["dash_mm"]), cap=0)
        elif kind == "water":
            pg.poly([rect(sx, y - 0.9, sx + 9.0, y + 0.9)], fill=bs["water"][0], alpha=bs["water"][1])
            if "edge" in bs:
                for yy in (y - 0.9, y + 0.9):
                    pg.line([(sx, yy), (sx + 9.0, yy)], bs["edge"][0], bs["edge"][1])
        elif kind == "covered":
            pg.line([(sx, y), (sx + 9.0, y)], bs["covered"][0], bs["covered"][1], bs["covered"][2], cap=0)
        elif kind == "street":
            pg.line([(sx, y), (sx + 9.0, y)], bs["street"][0], bs["street"][1])
        elif kind == "bridge":
            pg.line([(sx + 4.5, y + 0.9), (sx + 4.5, y - 0.9)], SN_INK2, 0.2)
        elif kind == "bld":
            pg.poly([rect(sx, y - 0.9, sx + 9.0, y + 0.9)], fill=bs["bld"][0], alpha=bs["bld"][1])
        else:                                            # the water's direction in every strip (left to right)
            pg.line([(sx, y), (sx + 7.6, y)], SN_WATER_MID, 0.35)
            pg.poly([[(sx + 9.0, y), (sx + 7.2, y + 0.8), (sx + 7.2, y - 0.8)]], fill=SN_WATER_MID)
        sn_key_row(pg, sx + 11.0, y, word)
        y -= 4.6
    sn_north(pg, G["V"], sx + 4.0, sn_y(top + 46.0))
    sn_scale_bar(pg, sx, sn_y(top + 62.0), (0.0, 100.0, 250.0, 500.0))
    return labs


def sn_north(pg, V, ax, ay):
    """north arrow (survey +Y turned with the strips), tip toward north, 'N' beside it"""
    nu, nv = V.uv((V.cx, V.cy + 1.0))
    L = math.hypot(nu, nv) or 1.0
    nx_, ny_ = nu / L, nv / L
    tip = (ax + nx_ * 3.5, ay + ny_ * 3.5)
    pg.poly([[tip, (ax - ny_ * 1.6 - nx_ * 3.0, ay + nx_ * 1.6 - ny_ * 3.0), (ax - nx_ * 1.8, ay - ny_ * 1.8)]],
            fill=SN_DARK)
    pg.poly([[tip, (ax - nx_ * 1.8, ay - ny_ * 1.8), (ax + ny_ * 1.6 - nx_ * 3.0, ay - nx_ * 1.6 - ny_ * 3.0)]],
            fill="FFFFFF", stroke=SN_DARK, lw=0.15)
    pg.text(u"N", tip[0] + 1.2, tip[1] - 0.6, sn_mm(SN_TS["small"]), SN_DARK, bold=True)


def sn_scale_bar(pg, x, y, marks):
    """the strips' scale bar (m, G13), numbers at 7 pt, the scale beside it"""
    for i, (a, b) in enumerate(zip(marks[:-1], marks[1:])):
        pg.poly([rect(x + a * SN_K, y, x + b * SN_K, y + 1.2)], fill=SN_DARK if i % 2 == 0 else "FFFFFF",
                stroke=SN_DARK, lw=0.15)
    fs = sn_mm(SN_TS["small"])
    for m_ in marks:
        pg.text(u"{:,.0f}{}".format(m_, u" m" if m_ == marks[-1] else u""), x + m_ * SN_K, y + 2.2, fs, SN_INK,
                align="C")
    pg.text(u"1:{:,.0f}".format(SN_SCALE), x + marks[-1] * SN_K + 5.0, y - 0.1, sn_mm(SN_TS["label"]), SN_DARK,
            bold=True)


# ---------------------------------------------------------------- Feeling (senses_ref1: emotion blots)
def sn_mood_col(ang):
    st = sorted(SN_FEEL)
    st = st + [(360.0, st[0][1])]
    a = ang % 360.0
    for (a0, c0), (a1, c1) in zip(st, st[1:]):
        if a0 <= a <= a1:
            return mix(c0, c1, (a - a0) / ((a1 - a0) or 1.0))
    return st[0][1]


def sn_blot(pg, x, y, R, colour, veins, seed, dots=True):
    """a watercolour blot strongest at its centre and spreading out (stacked translucent organic discs), vein
    strokes running out from it (a mood that gathers) and a dot texture thinning outward"""
    rnd = random.Random(seed)
    for i in range(7):
        r = R * (1.0 - i * 0.12)
        pg.poly([sn_ring(x + rnd.uniform(-0.08, 0.08) * R, y + rnd.uniform(-0.08, 0.08) * R, r, seed * 31 + i,
                         0.22, 36)], fill=colour, alpha=0.08)
    dark = mix(colour, SN_DARK, 0.35)
    for j in range(veins):
        a = rnd.uniform(0.0, 2.0 * math.pi)
        L = R * rnd.uniform(0.9, 1.55)
        ph = rnd.uniform(0.0, 6.0)
        pts = [(x + math.cos(a + 0.35 * math.sin(t * 3.0 + ph) * t) * L * t,
                y + math.sin(a + 0.35 * math.sin(t * 3.0 + ph) * t) * L * t) for t in [k / 8.0 for k in range(9)]]
        for seg, w in ((pts[:4], 0.28), (pts[3:7], 0.17), (pts[6:], 0.09)):
            pg.line(seg, dark, w, alpha=0.6)
    if dots:
        for k in range(int(R * 9)):
            a, d = rnd.uniform(0.0, 2.0 * math.pi), R * 1.15 * rnd.random() ** 0.8
            pg.circle(x + math.cos(a) * d, y + math.sin(a) * d, 0.11, fill=SN_DARK, alpha=0.45)


def sn_feeling(pg, G, cell, warn):
    T, box = cell["T"], cell["box"]
    B = []                                               # (survey xy, mood, R mm, veins, figure)
    for z in G["zones_raw"]:
        if z["code"] == "WT":
            B.append((z["q"], "calm", 4.5, 0, "sit"))
    for p in sn_spaced([w["at"] for w in G["widen"]], T, 9.0):
        B.append((p, "calm", 5.5, 0, None))
    if G["covered"]:
        P = max(G["covered"], key=lambda P: arclen(P)[-1])
        B.append((at_len(P, arclen(P), arclen(P)[-1] / 2.0)[0], "hidden", 4.0, 0, None))
    for h in G["hubs"]:
        if h["id"] == u"K6":                             # gateway on the regional road (h02 E12)
            B.append((h["xy"], "tense", 3.4, 5, None))
        elif h["role"] == "transit":
            B.append((h["xy"], "busy", 4.2, 6, "stand"))
        else:
            B.append((h["xy"], "lively", 5.0, 7, "walk"))
        if h.get("sub_xy"):
            B.append((h["sub_xy"]["c"], "play", 3.0, 3, "wade"))
    for P, ch in G["traffic"]:                           # K4: monument meets traffic (edge plan mark C3)
        if ch != "kept" and len(P) >= 2:
            B.append((at_len(P, arclen(P), arclen(P)[-1] / 2.0)[0], "tense", 2.6, 4, None))
    labs, seen, figs = [], set(), []
    pg.clip([rect(*box)])
    for i, (p, mood, R, veins, pose) in sorted(enumerate(B), key=lambda e: -e[1][2]):
        x, y = T(p)
        if sn_in((x, y, x, y), box, 6.0):
            sn_blot(pg, x, y, R, sn_mood_col(SN_MOOD[mood]), veins, 11 + i)
    for p, mood, R, veins, pose in B:                    # pictograms (senses_ref1's black figures), not crowded
        x, y = T(p)
        if pose and sn_in((x, y, x, y), box) and all(math.hypot(x - a, y - b) >= 2.2 for a, b in figs):
            _p16_fig(pg, pose, x, y - 1.4, 2.8, SN_DARK)
            figs.append((x, y))
    pg.unclip()
    for p, mood, R, veins, pose in sorted(B, key=lambda e: -e[2]):
        x, y = T(p)
        if mood not in seen and sn_in((x, y, x, y), box):
            seen.add(mood)
            labs.append(dict(s=mood, at=(x, y), col=mix(sn_mood_col(SN_MOOD[mood]), SN_DARK, 0.45)))
    sx, top = cell["side"], cell["top"]                  # key column: the feeling wheel, gathers / thins out
    cx, cy, r = sx + 23.0, sn_y(top + 22.0), 8.5
    for i in range(72):
        a0, a1 = math.radians(5.0 * i), math.radians(5.0 * (i + 1))
        pg.line([(cx + r * math.cos(a0 + (a1 - a0) * t / 3.0), cy + r * math.sin(a0 + (a1 - a0) * t / 3.0))
                 for t in range(4)], sn_mood_col(5.0 * i + 2.5), 1.5, cap=0, alpha=0.85)
    fs = sn_mm(SN_TS["small"])
    pg.text(u"active", cx, cy + r + 1.6, fs, SN_INK, align="C")
    pg.text(u"passive", cx, cy - r - 1.6 - fs * 0.75, fs, SN_INK, align="C")
    pg.text(u"positive", cx + r + 1.8, cy - fs * 0.35, fs, SN_INK)
    pg.text(u"negative", cx - r - 1.8, cy - fs * 0.35, fs, SN_INK, align="R")
    y1, y2 = sn_y(top + 44.0), sn_y(top + 58.0)
    sn_blot(pg, sx + 5.0, y1, 3.0, sn_mood_col(SN_MOOD["lively"]), 6, 5)
    sn_key_row(pg, sx + 12.0, y1, u"Gathers")
    sn_blot(pg, sx + 5.0, y2, 3.6, sn_mood_col(SN_MOOD["calm"]), 0, 6)
    sn_key_row(pg, sx + 12.0, y2, u"Thins out")
    return labs


# ---------------------------------------------------------------- Sound (senses_ref5: a mark texture per source)
def sn_mark(pg, kind, x, y, colour, ang=0.0):
    ca, sa = math.cos(ang), math.sin(ang)

    def R(px, py):
        return (x + px * ca - py * sa, y + px * sa + py * ca)
    if kind == "water":
        pg.line([R(-0.9 + 0.225 * i, 0.16 * math.sin(i * math.pi / 2.0)) for i in range(9)], colour, 0.22)
    elif kind == "reeds":
        for i in range(4):
            dx = (i - 1.5) * 0.28
            pg.line([R(dx, 0.0), R(dx * 1.8, 1.15 + 0.15 * (i % 2))], colour, 0.18)
    elif kind == "birds":
        pg.line([R(-0.5, 0.32), R(-0.15, 0.0), R(0.0, 0.12), R(0.15, 0.0), R(0.5, 0.32)], colour, 0.2)
    elif kind == "children":
        pg.circle(x, y, 0.36, stroke=colour, lw=0.2)
    elif kind == "voices":
        for r in (0.35, 0.75, 1.15):
            pg.line([R(r * math.cos(math.radians(-50.0 + 10.0 * i)), r * math.sin(math.radians(-50.0 + 10.0 * i)))
                     for i in range(11)], colour, 0.2)
    elif kind == "traffic":
        pg.poly([[R(-0.5, -0.28), R(0.5, -0.28), R(0.5, 0.28), R(-0.5, 0.28)]], fill=colour)
    elif kind == "wind":
        pg.line([R(-2.6 + 0.65 * i, 0.35 * math.sin(i * 0.7)) for i in range(9)], colour, 0.45, alpha=0.7)


def sn_cluster(pg, kind, at, r, n, colour, rnd, spin=0.4):
    """n marks scattered within r mm of at (a source as senses_ref5 draws it)"""
    for i in range(n):
        a, d = rnd.uniform(0.0, 2.0 * math.pi), r * math.sqrt(rnd.random())
        sn_mark(pg, kind, at[0] + math.cos(a) * d, at[1] + math.sin(a) * d, colour, rnd.uniform(-spin, spin))


def sn_sound(pg, G, cell, warn):
    T, box, V = cell["T"], cell["box"], G["V"]
    col = dict((k, c) for k, _, c in SN_SOUND)
    rnd = random.Random(7)
    ref, s = G["ref"], G["sref"]
    cov = [(a, b) for P in G["covered"] for a, b in zip(P, P[1:])]
    pg.clip([rect(*box)])
    if len(ref) >= 2:                                    # running water: the open stream (the hidden reach is silent)
        t, k = 0.0, 0
        while t <= s[-1]:
            p, d = at_len(ref, s, t)
            x, y = T(p)
            if box[0] - 1.0 <= x <= box[2] + 1.0 and not any(seg_dist(p[0], p[1], a, b) < 12.0 for a, b in cov):
                ang = sn_page_ang(V, d)
                off = 0.55 if k % 2 else -0.55
                sn_mark(pg, "water", x - math.sin(ang) * off, y + math.cos(ang) * off, col["water"], ang)
            t += 2.0 / SN_K
            k += 1
    for z in G["zones_raw"]:                             # reeds: the lined reed basins only (v28.1, D2: the side
        if z["code"] == "WT":                            # arms are open channels with rush and loosestrife, no reed)
            sn_cluster(pg, "reeds", T(z["q"]), 2.2, 7, col["reeds"], rnd, 0.25)
    for p in sn_spaced(G["forest"], T, 3.5):             # birds: the forest corridor and the wetland
        x, y = T(p)
        sn_cluster(pg, "birds", (x, y + 0.8), 1.2, 2, col["birds"], rnd)
    for p in sn_spaced([w["at"] for w in G["widen"]], T, 6.0):
        x, y = T(p)
        sn_cluster(pg, "birds", (x, y + 1.2), 1.8, 4, col["birds"], rnd)
    kids = [h["sub_xy"]["c"] for h in G["hubs"] if h.get("sub_xy")] + \
        [h["xy"] for h in G["hubs"] if h["role"] == "walking" and h["id"] != u"K6"]
    for p in kids:                                       # children at the edge: the sub-hubs and the hub squares
        sn_cluster(pg, "children", T(p), 1.4, 4, col["children"], rnd)
    for p in G["market"] + ([G["kermes"]] if G["kermes"] else []):   # market and Kermes voices
        sn_cluster(pg, "voices", T(p), 1.5, 3, col["voices"], rnd, math.pi)
    for P, ch in G["traffic"]:                           # traffic at K4 (calmed) and K6 (kept): blocks along the road
        Q = [T(p) for p in P]
        if len(Q) < 2:
            continue
        sq = arclen(Q)
        t = 0.4
        while t <= sq[-1]:
            (x, y), (ux, uy) = at_len(Q, sq, t)
            sn_mark(pg, "traffic", x, y, col["traffic"], math.atan2(uy, ux))
            t += 1.1 if ch == "kept" else 2.2
    wind = ([G["terrace"]["xy"]] if G["terrace"] else []) + [w["at"] for w in G["widen"]] + \
        [z["q"] for z in G["zones_raw"] if z["code"] == "WP"]
    for p in sn_spaced(wind, T, 14.0):                   # wind: the open places (viewing terrace, widened stream)
        x, y = T(p)
        ang = sn_page_ang(V, at_len(ref, s, chain_at(ref, p)[0])[1]) if len(ref) >= 2 else 0.0
        for j in range(3):
            sn_mark(pg, "wind", x + (j - 1) * 1.2, y + (j - 1) * 1.3, col["wind"], ang)
    pg.unclip()
    sx, y = cell["side"], sn_y(cell["top"] + 5.0)        # key column: the playful key
    for key, word, c in SN_SOUND:
        if key in ("water", "traffic", "wind"):
            for j in range(3 if key != "wind" else 1):
                sn_mark(pg, key, sx + 1.4 + j * 3.0 if key != "wind" else sx + 4.5, y, c, 0.0)
        else:
            for j in range(3):
                sn_mark(pg, key, sx + 1.4 + j * 3.0, y - (0.5 if key == "reeds" else 0.0), c, 0.0)
        sn_key_row(pg, sx + 11.0, y, word)
        y -= 5.2
    return []


# ---------------------------------------------------------------- Smell (senses_ref4: contour rings)
def sn_smell(pg, G, cell, warn):
    T, box = cell["T"], cell["box"]
    col = dict((k, c) for k, _, c in SN_SMELL)
    S, dg = [], []                                       # (key, survey xy, rings, first radius mm, step mm)
    for z in G["zones_raw"]:
        c = z["code"]
        if c == "WT":
            S.append(("reeds", z["q"], 5, 0.9, 0.7))
        elif c == "WS":                                  # the terraces' dry band F (French lavender, rosemary)
            S.append(("lavender", z["q"], 5, 0.9, 0.7))
        elif c == "DG":                                  # herbs and greens (card i01)
            S.append(("demeter", sn_vcent(z["P"]), 5, 0.9, 0.75))
            dg += z["P"]
        if c in ("GR", "DG"):                            # the plan's café places
            S.append(("cafe", z["q"], 3, 0.6, 0.55))
    mids = [P[len(P) // 2] for P in G["terr"] if P]
    for p in sn_spaced(mids, T, 8.0)[:4]:
        S.append(("lavender", p, 4, 0.7, 0.6))
    if dg:                                               # olives in Demeter's Garden (card i01), harvested in Nov
        S.append(("olive", sn_vcent(dg), 6, 2.0, 1.1))
    pg.clip([rect(*box)])
    dots = []
    for i, (key, p, n, r0, dr) in enumerate(S):
        x, y = T(p)
        if not sn_in((x, y, x, y), box, r0 + n * dr):
            continue
        for k in range(n):
            Q = sn_ring(x, y, r0 + k * dr, 101 + i, 0.06 + 0.03 * k, 56)
            pg.line(Q + Q[:1], col[key], 0.16, alpha=0.9 - 0.55 * k / max(1.0, n - 1.0))
        dots.append((x, y, col[key]))
    for x, y, c in dots:
        pg.circle(x, y, 0.6, fill=c)
    pg.unclip()
    sx, y = cell["side"], sn_y(cell["top"] + 5.0)        # key column
    for key, word, c in SN_SMELL:
        for r in (1.1, 1.8):
            Q = sn_ring(sx + 2.4, y, r, 3, 0.08, 36)
            pg.line(Q + Q[:1], c, 0.16, alpha=0.8)
        pg.circle(sx + 2.4, y, 0.6, fill=c)
        sn_key_row(pg, sx + 7.0, y, word)
        y -= 6.0
    return []


# ---------------------------------------------------------------- Encounters (senses_ref3: flow ribbons)
def sn_spine_y(refp, x0, x1, step=0.5):
    """the stream line's y (page mm) every step mm from x0 to x1, smoothed: the ribbons' path"""
    n = int((x1 - x0) / step) + 1
    xs = [x0 + i * step for i in range(n)]
    bk = {}
    for p in (densify(refp, 0.3) if len(refp) >= 2 else []):
        if x0 - 3.0 <= p[0] <= x1 + 3.0:
            bk.setdefault(int(math.floor((p[0] - x0) / step)), []).append(p[1])
    ys = []
    for i in range(n):
        got = [y for k in range(i - 3, i + 4) for y in bk.get(k, ())]
        ys.append(sum(got) / len(got) if got else None)
    known = [y for y in ys if y is not None]
    if not known:
        return xs, None
    last = known[0]
    for i in range(n):                                   # gaps take the nearest known value
        if ys[i] is None:
            ys[i] = last
        last = ys[i]
    return xs, [sum(ys[max(0, i - 6):i + 7]) / len(ys[max(0, i - 6):i + 7]) for i in range(n)]


def sn_bez(a, b, c, d, t):
    m = 1.0 - t
    return (m ** 3 * a[0] + 3 * m * m * t * b[0] + 3 * m * t * t * c[0] + t ** 3 * d[0],
            m ** 3 * a[1] + 3 * m * m * t * b[1] + 3 * m * t * t * c[1] + t ** 3 * d[1])


def sn_rrect(x0, y0, x1, y1, r, n=6):
    out = []
    for cx, cy, a0 in ((x1 - r, y1 - r, 0.0), (x0 + r, y1 - r, 90.0), (x0 + r, y0 + r, 180.0), (x1 - r, y0 + r, 270.0)):
        for i in range(n + 1):
            a = math.radians(a0 + 90.0 * i / n)
            out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


def sn_wave(pg, x0, x1, y, colour, lw=0.3):
    pg.line([(x0 + (x1 - x0) * i / 16.0, y + 0.25 * math.sin(i * math.pi / 2.0)) for i in range(17)], colour, lw)


def sn_bubble(pg, x, y, key, word, colour, pose):
    """a vignette at a ribbon's end: an organic bubble, a figure of common/figures.py and one word"""
    w, h = 34.0, 11.0
    pg.poly([sn_rrect(x, y - h / 2.0, x + w, y + h / 2.0, 4.0)], fill="FFFFFF", stroke=colour, lw=0.35)
    fx, fy = x + 6.5, y - h / 2.0 + 1.8
    if key == "remember":                                # under a Roman arch
        pg.line([(fx + 3.4 + 2.6 * math.cos(math.radians(a)), fy + 2.6 * math.sin(math.radians(a)))
                 for a in range(0, 181, 15)], colour, 0.45, alpha=0.55)
    if key in ("touch", "cross"):
        sn_wave(pg, fx - 3.5, fx + 4.5, fy + (0.9 if key == "cross" else 0.0), SN_WATER_MID)
    else:
        pg.line([(fx - 3.5, fy), (fx + 6.5, fy)], SN_INK2, 0.2)
    _p16_fig(pg, pose, fx, fy, 7.0, colour)
    if key == "watch":                                   # the line of sight
        pg.line([(fx + 0.6, fy + 6.2), (fx + 5.6, fy + 5.4)], colour, 0.2, [0.6, 0.4], cap=0)
    size = sn_mm(SN_TS["label"])
    pg.text(word, x + 14.0, y - size * 0.35, size, mix(colour, SN_DARK, 0.3), bold=True)


def sn_exp_places(G):
    """where each way of meeting the water is strongest (the masterplan's places; design reading)"""
    hub = G["hub"]
    walk = [h["xy"] for h in G["hubs"] if h["role"] == "walking" and h["id"] != u"K6"]
    bk = dict(BRIDGES_K)
    pl = {"watch": ([G["terrace"]["xy"]] if G["terrace"] else []) + [z["q"] for z in G["zones_raw"] if z["code"] == "WT"],
          "walk": walk + [p for P in G["canopy"] for p in sn_along(P, 40.0)],
          "touch": [h["sub_xy"]["c"] for h in G["hubs"] if h.get("sub_xy")] + [G["bath"], G["kermes"]],
          "cross": [c_["xy"] for c_ in G["cross"]],
          "remember": [bk.get(k) for k in ("K3", "K4", "K5")] + [G["bath"], CRAFT_XY, ROMAN_WALL] +
          [hub[k]["xy"] for k in (u"İstiklal", u"Kızıl Avlu") if k in hub]}
    return dict((k, [p for p in v if p]) for k, v in pl.items())


def sn_meet_points(G, T, box):
    """T4a: where the experience lines meet, [(page x, set of P16_MEET kinds)] left to right: every hub, Kermes
    (at the S4 cut) and the flood zone (the widened reaches; without them the bed sub-hubs high water closes).
    Meeting points closer than 7 mm become one, named by all its kinds."""
    pts = [(T(h["xy"])[0], "hub") for h in G["hubs"] if h.get("xy")]
    if G["kermes"]:
        pts.append((T(G["kermes"])[0], "kermes"))
    fl = sn_spaced([w["at"] for w in G["widen"]], T, 9.0) or \
        [h["sub_xy"]["c"] for h in G["hubs"] if h.get("sub_xy")]
    pts += [(T(p)[0], "flood") for p in fl]
    rank = dict((k, i) for i, (k, _, _) in enumerate(P16_MEET))
    out = []
    for x, k in sorted(pts, key=lambda e: rank[e[1]]):
        if not (box[0] + 4.0 <= x <= box[2] - 4.0):
            continue
        near = [n for n in out if abs(n[0] - x) < 7.0]
        if near:
            near[0][1].add(k)
        else:
            out.append([x, set([k])])
    return sorted((x, ks) for x, ks in out)


def sn_encounters(pg, G, cell, warn):
    """T4a (package E, R23-R26): five experience lines, each in its own lane along the stream from the upstream edge
    to its vignette, never crossing another (the lane order is the vignettes' order); the lines draw together at the
    meeting points (hubs, Kermes, the flood zone), marked by a ring and a post of icons (R25), and part again in the
    same order; the places of each experience sit on its line as circles (R24, R26)."""
    T, box = cell["T"], cell["box"]
    x0, y0, x1, y1 = box
    step = 0.5
    xs, ys = sn_spine_y([T(p) for p in G["ref"]], x0, x1, step)
    if ys is None:
        ys = [(y0 + y1) / 2.0] * len(xs)
        warn.append(u"senses sheet: no stream line in the strip: the encounter lines run along its middle")
    n = len(ys)                                          # a calmer path for the lanes: 15 mm moving mean
    ys = [sum(ys[max(0, i - 15):i + 16]) / len(ys[max(0, i - 15):i + 16]) for i in range(n)]
    nodes = sn_meet_points(G, T, box)
    gap, keep, wp = 2.6, 0.24, 3.2                       # mm: lane spacing, share left at a meeting, pinch length
    pinch = [max([math.exp(-((x - nx) / wp) ** 2) for nx, _ in nodes] or [0.0]) for x in xs]
    m = len(SN_EXP)

    def lane_y(i, k):
        y = ys[k] + ((m - 1) / 2.0 - i) * gap * (1.0 - (1.0 - keep) * pinch[k])
        return min(max(y, y0 + 1.5), y1 - 1.5)

    def at_x(i, x):
        k = min(n - 1, max(0, int(round((x - x0) / step))))
        return lane_y(i, k)
    for nx, ks in nodes:                                 # the flood zone: a hatched cloud under the lines
        if "flood" in ks:
            ym = (at_x(0, nx) + at_x(m - 1, nx)) / 2.0
            pg.poly([sn_ring(nx, ym, gap * m * 0.5 + 1.6, 77, 0.18, 40, (3, 5))],
                    stripes=(SN_INK2, 0.45, 0.12, 0.0), alpha=0.8)
    pl = sn_exp_places(G)
    top = cell["top"]
    for i, (key, word, colour, pose) in enumerate(SN_EXP):
        C_ = [(x, lane_y(i, k)) for k, x in enumerate(xs)]
        bx, by = cell["side"] + 11.0, sn_y(top + 8.0 + 14.5 * i)
        ex, ey = C_[-1]
        fan = [sn_bez((ex, ey), (ex + 6.0, ey), (bx - 6.0, by), (bx, by), t / 24.0) for t in range(1, 25)]
        pg.line(C_ + fan, colour, 0.6, alpha=0.92)
        pg.circle(C_[0][0] + 0.6, C_[0][1], 0.6, fill=colour)          # where the line starts
        Cs = C_[::6] + C_[-1:]
        cell["segs"].extend(zip(Cs, Cs[1:]))
        sn_bubble(pg, bx, by, key, word, colour, pose)
        got = []                                         # its places: circles on its own line
        for x in sorted(T(p)[0] for p in pl.get(key, [])):
            if not (x0 + 2.0 <= x <= x1 - 2.0) or any(abs(x - nx) < 2.6 for nx, _ in nodes) or \
                    any(abs(x - g) < 3.0 for g in got):
                continue
            got.append(x)
            pg.circle(x, at_x(i, x), 0.95, fill=mix(colour, "FFFFFF", 0.55), stroke=colour, lw=0.3)
    labs, firsts = [], {}
    bs, pitch = 4.4, 5.2                                 # mm: icon plate, post pitch
    for nx, ks in nodes:                                 # the meeting points: a ring round the bundle, a post of icons
        ya, yb = at_x(0, nx), at_x(m - 1, nx)
        ym, r = (ya + yb) / 2.0, abs(ya - yb) / 2.0 + 1.2
        pg.circle(nx, ym, r, stroke=SN_DARK, lw=0.3)
        kinds = [k for k, _, _ in P16_MEET if k in ks]
        down = ym - r - 1.5 - pitch * len(kinds) >= y0 + 0.5
        sgn = -1.0 if down else 1.0
        end = ym + sgn * (r + 1.5 + pitch * (len(kinds) - 1) + bs / 2.0)
        pg.line([(nx, ym + sgn * r), (nx, end - sgn * bs / 2.0)], SN_INK2, 0.2)
        for j, k in enumerate(kinds):
            cy = ym + sgn * (r + 1.5 + bs / 2.0 + pitch * j)
            icon = [ic for kk, _, ic in P16_MEET if kk == k][0]
            try:
                _p16_shapes(pg, ico_badge(icon, nx, cy, bs, "circle", fill="FFFFFF", edge=SN_INK2))
            except Exception:
                pg.circle(nx, cy, bs / 2.0, fill="FFFFFF", stroke=SN_INK2, lw=0.2)
            cell["taken"].append((nx - bs / 2.0, cy - bs / 2.0, nx + bs / 2.0, cy + bs / 2.0))
            firsts.setdefault(k, []).append((nx, cy))
        cell["taken"].append((nx - r, ym - r, nx + r, ym + r))
    for k, word, _ in P16_MEET:                          # a word beside each plate (repeats may give way)
        for j, at in enumerate(firsts.get(k, ())):
            labs.append(dict(s=word, at=at, col=SN_INK, pt=SN_TS["small"], rank=0 if j == 0 else 1))
    return labs


# ---------------------------------------------------------------- History (senses_ref2: layered fade fields)
def sn_layers_round(pg, x, y, R, colour, seed, n=6, a=0.1):
    for k in range(n):
        pg.poly([sn_ring(x, y, R * (1.0 - k / float(n)), seed, 0.12, 40, (2, 3))], fill=colour, alpha=a)
    return (x, y)


def sn_layers_band(pg, P, W, colour, n=6, a=0.1):
    """layers along a page polyline, each narrower and shorter: darkest at the core"""
    s = arclen(P)
    L = s[-1]
    for k in range(n):
        cut = L * 0.22 * k / float(n)
        Q = sn_band(sub_line(P, s, cut, L - cut) if L > 2.0 * cut + 0.2 else P, W * (1.0 - k / float(n)), 0.35)
        if len(Q) >= 3:
            pg.poly([Q], fill=colour, alpha=a)
    return at_len(P, s, L / 2.0)[0]


def _p16_norm(s):
    """lower case, Turkish (and other) accents folded, letters and digits only ('Kızıl Avlu' -> 'kizilavlu')"""
    import unicodedata
    t = unicodedata.normalize("NFKD", (s or u"").replace(u"ı", u"i").replace(u"İ", u"I")).lower()
    return u"".join(c for c in t if c.isalnum() and not unicodedata.combining(c))


def _p16_jpeg(path):
    """(width px, height px, components, bytes) of a JPEG file read from its header, once a run; None if it is not
    a JPEG with 1 or 3 components (a PDF DCTDecode image)"""
    m = _P16_MEMO.setdefault("jpg", {})
    if path in m:
        return m[path]
    got = None
    try:
        with open(path, "rb") as fh:
            b = fh.read()
        i = 2 if b[:2] == b"\xff\xd8" else len(b)
        while i + 9 < len(b):
            if b[i] != 0xFF:
                break
            mk = b[i + 1]
            if mk == 0xFF:
                i += 1
                continue
            if mk == 0x01 or 0xD0 <= mk <= 0xD8:
                i += 2
                continue
            L = (b[i + 2] << 8) | b[i + 3]
            if mk in (0xC0, 0xC1, 0xC2):
                h, w, nc = (b[i + 5] << 8) | b[i + 6], (b[i + 7] << 8) | b[i + 8], b[i + 9]
                if w and h and nc in (1, 3):
                    got = (w, h, nc, b)
                break
            i += 2 + L
    except Exception:
        got = None
    m[path] = got
    return got


def _p16_photos(warn):
    """{P16_PLACES key: (path, credit line or None)} once a run, from P16_PHOTO_DIR (p.21's run-kit contract): own
    photos by file name (no credit, D13), else the first unused photos.csv row whose place or file name holds an
    alias (its credit line). v29: Kermes rows are used for Kermes. A missing folder: {} and one log line."""
    if "photos" in _P16_MEMO:
        return _P16_MEMO["photos"]
    d, out = P16_PHOTO_DIR, {}
    if not os.path.isdir(d):
        warn.append(u"senses sheet: no photo folder {}: History is drawn without photos".format(d))
        _P16_MEMO["photos"] = out
        return out

    def find(f):
        for p in (os.path.join(d, f), os.path.join(d, "own", os.path.basename(f)),
                  os.path.join(d, "photos", os.path.basename(f))):
            if os.path.isfile(p) and _p16_jpeg(p):
                return p
        return None
    own = set(_p16_norm(os.path.basename(f)) for pl in P16_PLACES for f in pl["own"])
    rows, cp = [], os.path.join(d, P16_PHOTO_CSV)
    if os.path.isfile(cp):
        try:
            import csv as _csv
            with open(cp, encoding="utf-8-sig", newline="") as fh:
                for r_ in _csv.DictReader(fh):
                    rows.append(dict((_p16_norm(k_), (v_ or u"").strip()) for k_, v_ in r_.items() if k_))
        except Exception as ex:
            warn.append(u"senses sheet: {} not read ({}): own photos only".format(cp, ex))
    used = set()
    for pl in P16_PLACES:
        got = None
        for f in pl["own"]:
            p = find(f)
            if p:
                got = (p, None)
                break
        for r_ in ([] if got else rows):
            fn = r_.get("file", u"")
            tx = _p16_norm(r_.get("place", u"")) + u"|" + _p16_norm(os.path.splitext(os.path.basename(fn))[0])
            if not fn or fn in used or not any(a in tx for a in pl["alias"]) or \
                    any(a in tx for a in pl.get("notalias", ())):
                continue
            p = find(fn)
            if p is None:
                continue
            used.add(fn)
            cr = r_.get("creditline") or r_.get("credit") or u""
            got = (p, None if _p16_norm(os.path.basename(fn)) in own or not cr else cr)
            break
        if got:
            out[pl["key"]] = got
    miss = [pl["cap"][0] for pl in P16_PLACES if pl["key"] not in out]
    if miss:
        warn.append(u"senses sheet: no photo for {} (named on the strip instead)".format(u", ".join(miss)))
    _P16_MEMO["photos"] = out
    return out


def _p16_photo_slots(keys_at, box, refp, capm, wide=None):
    """{key: (x, y, up)}: the lower-left corner of each photo, alternately above and below the stream (left to
    right), as near its place as the photos beside it allow, clear of the stream line by 4 mm, inside the strip;
    capm = the caption's room on the photo's outer side; wide = {key: caption width mm}"""
    W, H = P16_PHOTO_W, P16_PHOTO_H
    wide = wide or {}
    srt = sorted(keys_at, key=lambda e: e[1][0])
    out = {}
    for up in (True, False):
        lst = [e for i, e in enumerate(srt) if (i % 2 == 0) == up]
        xs, prev = [], box[0] + 1.0 - 2.5
        ws = [max(W, wide.get(k, 0.0)) for k, a in lst]   # a caption wider than its photo keeps its room
        for (k, a), wk in zip(lst, ws):
            x = max(a[0] - W / 2.0, prev + 2.5)
            xs.append(x)
            prev = x + wk
        if xs and xs[-1] + ws[-1] > box[2] - 1.0:
            d = xs[-1] + ws[-1] - (box[2] - 1.0)
            xs, prev = [x - d for x in xs], box[0] + 1.0 - 2.5
            for j in range(len(xs)):
                xs[j] = max(xs[j], prev + 2.5)
                prev = xs[j] + ws[j]
        for (k, a), x in zip(lst, xs):
            near = [q[1] for q in refp if x - 2.0 <= q[0] <= x + W + 2.0] + [a[1]]
            if up:
                y = min(max(near) + 4.0, box[3] - 1.0 - capm - H)
            else:
                y = max(min(near) - 4.0 - H, box[1] + 1.0 + capm)
            out[k] = (x, y, up)
    return out


def sn_history(pg, G, cell, warn):
    """layered heritage fields on the stream's places (senses_ref2) and, T4a, a small photo beside each place
    named (P16_PLACES; v29: Kermes too): own photos without credit, Commons photos numbered, their credit lines
    in the key column. The photos are embedded by _p16_save (the core's PDF writer draws no images)."""
    T, box = cell["T"], cell["box"]
    txt = COL["accent_dark"]
    labs, anchors = [], {}

    def field(q, half, R, seed):
        """a field along the stream line round q (half m either side), else a round one"""
        P = [T(p) for p in sn_ref_piece(G, q, half)] if half else []
        if len(P) >= 2 and arclen(P)[-1] > 0.5:
            return sn_layers_band(pg, P, R, SN_HER)
        x, y = T(q)
        return sn_layers_round(pg, x, y, R, SN_HER, seed)
    pg.clip([rect(*box)])
    ka = G["hub"].get(u"Kızıl Avlu")                     # the Red Hall tunnels: the covered reach under it (H2)
    if ka:
        best = None
        for P in G["covered"]:
            c, d = chain_at(P, ka["xy"])
            if d <= 150.0 and (best is None or d < best[0]):
                best = (d, P, c)
        if best:
            d, P, c = best
            Q = [T(p) for p in sub_line(P, arclen(P), max(0.0, c - 90.0), min(arclen(P)[-1], c + 90.0))]
            at = sn_layers_band(pg, Q, 1.6, SN_HER) if len(Q) >= 2 and arclen(Q)[-1] > 0.5 else \
                sn_layers_round(pg, T(ka["xy"])[0], T(ka["xy"])[1], 2.4, SN_HER, 31)
        else:
            at = sn_layers_round(pg, T(ka["xy"])[0], T(ka["xy"])[1], 2.4, SN_HER, 31)
        anchors["tunnels"] = at
    bk = dict(BRIDGES_K)
    for i, k in enumerate(("K3", "K5")):                 # the Roman bridges (h01 §5 P08, P09; K4 "Roman?", P06)
        if bk.get(k):
            x, y = T(bk[k])
            anchors[k.lower()] = sn_layers_round(pg, x, y, 2.3, SN_HER, 40 + i)
    if G["bath"]:                                        # Tabaklar Hamamı (H4)
        x, y = T(G["bath"])
        anchors["hamam"] = sn_layers_round(pg, x, y, 2.0, SN_HER, 50)
    anchors["tabakhane"] = field(CRAFT_XY, 70.0, 1.8, 60)   # Tabakhane (H3)
    if G["kermes"]:                                      # Kermes in the dry bed (h01 §2.8), at the S4 cut (v29: photo)
        anchors["kermes"] = field(G["kermes"], 90.0, 1.8, 70)
    pg.unclip()
    anchors = dict((k, a) for k, a in anchors.items() if sn_in((a[0], a[1], a[0], a[1]), box))
    ph = _p16_photos(warn)
    with_ph = [(k, anchors[k]) for k in (pl["key"] for pl in P16_PLACES) if k in anchors and k in ph]
    names = dict((pl["key"], pl["cap"]) for pl in P16_PLACES)
    rb = [anchors[k] for k in ("k3", "k5") if k in anchors and k not in ph]
    if rb:                                               # places without a photo keep their word on the strip
        labs.append(dict(s=u"Roman bridges", at=rb[0], more=rb[1:], col=txt))
    for k, s in (("hamam", u"Tabaklar Hamamı"), ("tabakhane", u"Tabakhane"), ("tunnels", u"Kızıl Avlu tunnels"),
                 ("kermes", u"Kermes")):                 # v29: Kermes keeps its word when it has no photo
        if k in anchors and k not in ph:
            labs.append(dict(s=s, at=anchors[k], col=txt))
    fs = sn_mm(SN_TS["small"])
    lh = fs * 1.2
    capm = 0.8 + 2.0 * lh
    W, H = P16_PHOTO_W, P16_PHOTO_H
    refp = [T(p) for p in G["ref"]]
    wide = dict((k, max(text_w(s + (u"  [9]" if ph[k][1] and j == len(names[k]) - 1 else u""), fs, j == 0)
                        for j, s in enumerate(names[k]))) for k, _ in with_ph)
    slots = _p16_photo_slots(with_ph, box, refp, capm, wide)
    credits = []
    for k, a in sorted(with_ph, key=lambda e: slots[e[0]][0]):
        x, y, up = slots[k]
        path, cr = ph[k]
        cap = list(names[k])
        if cr:                                           # Commons: numbered, its credit line in the key column
            credits.append(cr)
            cap[-1] = u"{}  [{}]".format(cap[-1], len(credits))
        pr = (x, y, x + W, y + H)
        e = lp_leader_end(pr, a)
        pg.line([a, e], SN_INK2, 0.15)
        pg.circle(a[0], a[1], 0.35, fill=SN_INK2)
        for j, s in enumerate(cap):
            yb = (y + H + 0.8 + (len(cap) - 1 - j) * lh + fs * 0.2) if up else (y - 0.8 - fs * 0.8 - j * lh)
            pg.text(s, x, yb, fs, txt if j == 0 else SN_INK2, bold=(j == 0))
        cy0, cy1 = (y + H, y + H + capm) if up else (y - capm, y)
        cell["taken"] += [pr, (x, cy0, x + max(W, max(text_w(s, fs, True) for s in cap)), cy1)]
        G.setdefault("imgs", []).append((path, (x, y, W, H)))
    sx, top = cell["side"], cell["top"]                  # key column: the heritage field, then the photo credits
    sn_layers_round(pg, sx + 4.5, sn_y(top + 5.0), 2.3, SN_HER, 40)
    sn_key_row(pg, sx + 11.0, sn_y(top + 5.0), u"Heritage place")
    if credits:
        y = sn_y(top + 13.0)
        pg.text(u"Photos", sx, y, fs, SN_INK, bold=True)
        for n_, cr in enumerate(credits):
            for j, s in enumerate(wrap(u"[{}] {}".format(n_ + 1, cr), fs, SN_CW - SN_SIDE - 1.0)):
                y -= lh
                pg.text(s, sx + (0.0 if j == 0 else 2.6), y, fs, SN_INK2)
            y -= 0.6
    return labs


# ---------------------------------------------------------------- the sheet's writer with photos (T4a)
def _p16_write_pdf(pg, path, title, imgs):
    """the core's write_pdf (parts/01) plus JPEG photos: imgs = [(path, (x, y, w, h) page mm)], each embedded once
    as a DCTDecode image XObject, drawn after the page's vector items (cropped to fill its slot, a hairline frame).
    Kept here because the core's writer draws no images (T4b may move image support into the core)."""
    objs = []

    def add(b):
        objs.append(b)
        return len(objs)
    font = pdf_fonts(add, ("R", "B"))
    gs = [add("<< /Type /ExtGState /ca {0} /CA {0} >>".format(_f(i / 100.0)).encode("latin-1")) for i in range(1, 100)]
    gs_res = " ".join("/A{:02d} {} 0 R".format(i + 1, o_) for i, o_ in enumerate(gs))
    xo, ops, names = [], [], {}
    for p_, (x, y, w, h) in imgs:
        j = _p16_jpeg(p_)
        if not j:
            continue
        iw, ih, nc, data = j
        if p_ not in names:
            oid = add("<< /Type /XObject /Subtype /Image /Width {} /Height {} /ColorSpace /{} /BitsPerComponent 8 "
                      "/Filter /DCTDecode /Length {} >>\nstream\n".format(
                          iw, ih, "DeviceRGB" if nc == 3 else "DeviceGray", len(data)).encode("latin-1") +
                      data + b"\nendstream")
            names[p_] = "/Im{}".format(len(names) + 1)
            xo.append("{} {} 0 R".format(names[p_], oid))
        a = iw / float(ih)
        dw, dh = (h * a, h) if a > w / h else (w, w / a)
        r_, g_, b_ = hex_rgb(SN_INK2)
        ops.append("q {} {} {} {} re W n {} 0 0 {} {} {} cm {} Do Q".format(
            _f(x), _f(y), _f(w), _f(h), _f(dw), _f(dh), _f(x - (dw - w) / 2.0), _f(y - (dh - h) / 2.0), names[p_]))
        ops.append("q {} {} {} RG 0.15 w {} {} {} {} re S Q".format(_f(r_), _f(g_), _f(b_), _f(x), _f(y), _f(w), _f(h)))
    pages_id = add(b"")
    body = page_stream(pg) + (("\n" + "\n".join(ops)).encode("latin-1") if ops else b"")
    data = zlib.compress(body, 6)
    cid = add(b"<< /Length " + str(len(data)).encode() + b" /Filter /FlateDecode >>\nstream\n" + data +
              b"\nendstream")
    kid = add("<< /Type /Page /Parent {} 0 R /MediaBox [0 0 {} {}] /Contents {} 0 R /Resources << /Font "
              "<< /F1 {} 0 R /F2 {} 0 R >> /ExtGState << {} >>{} >> >>".format(
                  pages_id, _f(pg.W / PT), _f(pg.H / PT), cid, font[0], font[1], gs_res,
                  " /XObject << {} >>".format(" ".join(xo)) if xo else "").encode("latin-1"))
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


def _p16_save(pg, folder, name, title, imgs):
    """the core's save() with _p16_write_pdf: a new name when the old file is open in another program"""
    path = os.path.join(folder, name)
    try:
        _p16_write_pdf(pg, path, title, imgs)
    except (IOError, OSError):
        path = os.path.join(folder, name.replace(".pdf", datetime.datetime.now().strftime("_%H%M%S.pdf")))
        _p16_write_pdf(pg, path, title, imgs)
    return path


# ---------------------------------------------------------------- the sheet
def senses_sheet(C, areas, folder, files, warn, basemap=None):
    """S1: writes Bergama_senses_A3.pdf into the masterplan's output folder (the masterplan's PDF writer, Arial
    embedded; with History photos _p16_save, the same writer plus JPEG images); returns the log line. Called once a
    press by build_all (a failure is only a warning there). basemap = {panel title: (mode, override)} changes
    P16_BASEMAP's choice (D5) for this run."""
    t0 = time.time()
    _P16_MEMO.clear()                                    # photos are read once a run
    bm = dict(P16_BASEMAP)
    bm.update(basemap or {})
    G = sn_data(C, areas, warn)
    G["warn"] = warn
    pg = Page(SN_PW, SN_PH)
    pg.poly([rect(0.0, 0.0, SN_PW, SN_PH)], fill="FFFFFF")
    pg.text(SN_KICKER, SN_ML, sn_y(12.0), sn_mm(SN_TS["kicker"]), SN_ACC, bold=True)   # the booklet's header band
    pg.text(SN_TITLE, SN_ML, sn_y(22.0), sn_mm(SN_TS["title"]), SN_INK, bold=True)
    pg.line([(SN_ML, sn_y(25.0)), (SN_PW - SN_ML, sn_y(25.0))], SN_RULE, 0.25 * SN_PT)
    sn_rich(pg, SN_ML, sn_y(30.5), [(u"The fade-out zones and the ", False), (u"senses", True),
                                    (u" · every strip ", False), (u"1:20,000", True)], SN_TS["statement"], SN_INK)
    cells = [(SN_COLX[0], SN_ROWS[0], u"Zones", sn_zones),
             (SN_COLX[1], SN_ROWS[0], u"Feeling", sn_feeling),
             (SN_COLX[0], SN_ROWS[1], u"Sound", sn_sound),
             (SN_COLX[1], SN_ROWS[1], u"Smell", sn_smell),
             (SN_COLX[0], SN_ROWS[2], u"Encounters", sn_encounters),
             (SN_COLX[1], SN_ROWS[2], u"History", sn_history)]
    for cx, top, title, layer in cells:
        cell = sn_cell(pg, G, cx, top, title, bm.get(title))
        labs, n0 = [], len(pg.items)
        try:
            labs = layer(pg, G, cell, warn) or []
        except Exception as ex:
            import traceback
            warn.append(u"senses sheet: panel {} not drawn ({}: {})".format(title, type(ex).__name__, ex))
            warn.append(traceback.format_exc()[-480:])
            open_ = sum(1 if it[0] == "clip" else -1 if it[0] == "unclip" else 0 for it in pg.items[n0:])
            for _ in range(max(0, open_)):               # close a clip the failed panel left open
                pg.unclip()
        sn_outline(pg, G, cell)
        sn_place(pg, cell, labs, warn)
    imgs = G.get("imgs") or []
    path = _p16_save(pg, folder, SN_NAME, SN_TITLE, imgs) if imgs else save(pg, folder, SN_NAME, SN_TITLE)
    files.append(path)
    return u"{}  {}  {:.1f} s (zones: {})".format(os.path.basename(path), datetime.datetime.now().strftime("%H:%M:%S"),
                                                  time.time() - t0, G["fields_src"])
# p.23 the plan: plan_page, the pl28_* functions and draw_corridor (split from parts/02_Design.py, parts/02b_detail.py, parts/02c_corridor.py, parts/02d_r28_ground.py on 29 Oct 2026; moved unchanged)
# v28 (revision 29 Oct, WO-T4b-2, package H "Page 23"): the map is the page. The analysis frame at 1:5,000 in two rows
# (upstream half on top, downstream half below; PL23_OVL m either side of the match line drawn in both), every layer
# of the corridor on both, the riverside walk as one route with the bike lane beside it (PL23_BIKE); each numbered
# move a short boxed text on the map by its place, on an arrow (R13 callouts, R14 numbered boxes); a side column
# holds the small legend, the moves with no room on the map and the areas left as they are. One strip at 1:10,000
# when two rows do not fit the crop. The perspective collage of R12 is left out (a script draws no photo collage).
PL23_SCALE = 5000.0          # the two rows
PL23_FALLBACK = 10000.0      # one strip when the two rows do not fit BK_W x BK_H
PL23_OVL = 25.0              # m either side of the match line drawn in both rows
PL23_MARK_H = 9.0            # mm: north arrow, scale bar and flow note under each row
PL23_GAP = 3.0               # mm between the first row's marks and the second row
PL23_SIDE_MIN = 80.0         # mm: the side column at least this wide
PL23_SIDE_GAP = 5.0          # mm between the map and the side column
PL23_MARKS = {5000.0: (0.0, 50.0, 100.0, 250.0), 10000.0: (0.0, 100.0, 200.0, 500.0)}   # scale bar, m (50 mm)
PL23_BOX_W = 46.0            # mm: a callout box at most this wide
PL23_NAME_TS = 3.2           # mm: place names on the 1:5,000 rows (9 pt)
PL23_RINGS = (3.0, 6.0, 10.0, 15.0, 21.0, 28.0, 36.0)   # mm: callout spots round a place, nearest first
PL23_WALK_COL, PL23_BIKE_COL = "4C2528", "5C7A86"         # palette references (library/examples/palettes)
PL23_BIKE = True             # the riverside walk carries a bike lane on its land side (Aras 29 Oct 21:04, decision card)


def draw_block(pg, lines, x0, y_top, colour, halo):
    y = y_top
    for s, sz, bd in lines:
        y -= sz * 1.0
        pg.text(s, x0, y, sz, colour, bold=bd, halo=halo)
        y -= sz * 0.18


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


def draw_corridor(pg, T, k, C, inP, taken, dw, dh):
    """Every layer of the corridor on plan page pg (T: world -> page mm, k: mm per m; inP: world point on this
    plan). Returns (legend keys used, note numbers placed). v27: the plan strips only (p.24's windows = 02e).
    v26 (Prompt 7 rules 1 and 5): the layers in the order water -> buildings -> bridges -> roads -> proposal ->
    labels (the paper is the ground; the planting is proposed, so it is a proposal tint); what exists (survey) is
    crisp, what we propose is soft: fading fields, haloes, translucent bands, no outlines."""
    used, placed = set(), []
    ink, ink2 = COL["ink_dark"], COL["ink2"]
    vis = lambda TPs: [Q for Q in TPs if hit(bbox(Q), (-2.0, -2.0, dw + 2.0, dh + 2.0))]
    TL = lambda Ls: vis([[T(p) for p in L_] for L_ in Ls])
    on = lambda Q: hit(bbox(Q), (0.0, 0.0, dw, dh))
    big = k >= 0.5                                       # the 1:1,000 windows
    fine = k < 0.15                                      # v27 (MIRAQUA 28 Oct, G7): the 1:10,000 strip (p.23)
    hal = 0.8 if big else 0.6                            # halo of a proposed area, mm
    # ---- water (survey): the bed between the surveyed edges, the stream lines
    Ps = TL(C.bed_loops)
    if Ps:
        pg.poly(Ps, fill=WATER_COL)
        used.add("bed")
    for P in C.streams:
        pg.line([T(p) for p in P], COL["river_mid"], 0.15)
    # v26.1 (Prompt 8): the hidden-stream line (proposal, soft) with the water, never over the buildings or bridges
    # above it; in the legend only where it is on this plan (a 1:1,000 window)
    for P in C.covered:
        Q = [T(p) for p in P]
        pg.line(Q, COL["river_mid"], 1.6 if big else 0.8, [1.6, 0.9], cap=0, alpha=0.7)
        if on(Q):
            used.add("hidden")
    # ---- buildings (survey); built on since the survey hatched (satellite check, OPEN_CHECK)
    for role, fill in (("building", COL["bld"]), ("housing", COL["bld"]), ("shed", COL["bld"]),
                       ("heritage", COL["her"])):
        Ps = TL(C.bld.get(role, []))
        if Ps:
            pg.poly(Ps, fill=fill, stroke=COL["her_edge"] if role == "heritage" else None, lw=0.1)
            used.add("bld" if role != "heritage" else "her")
    Ps = TL(C.built_since)
    if Ps:
        pg.poly(Ps, fill=COL["bld"], stripes=(ink, 0.8, 0.15, 45.0))
        used.add("since")
    # ---- bridges (survey YOL_KOPRU); a bridge of K1-K6 with no survey line within 25 m gets a mark
    for P in C.bridges:
        Q = [T(p) for p in P]
        if on(Q):
            pg.line(Q, ink, 0.5 if big else 0.3)
            used.add("bridge")
    for nm, xy in BRIDGES_K:
        if any(min(seg_dist(xy[0], xy[1], a, b) for a, b in zip(P, P[1:])) <= 25.0 for P in C.bridges):
            continue
        x, y = T(xy)
        if 0.0 <= x <= dw and 0.0 <= y <= dh:
            pg.poly([rect(x - 0.9, y - 0.9, x + 0.9, y + 0.9)], fill=ink)
            used.add("bridge")
    # ---- roads (survey street edges)
    for P in C.roads:
        Q = [T(p) for p in P]
        if on(Q):
            pg.line(Q, ROAD_TONE[1], 0.3 if big else (0.1 if fine else 0.18))   # v27: base recessive (G6)
            used.add("street")
    # ---- proposal, soft: the planting gradient from the water, the programme rings round the hubs
    for t, Ls in reversed(C.eco):
        Ps = TL(Ls)
        if Ps:
            pg.poly(Ps, fill=ECO_COL, alpha=ECO_A)
            used.add("eco")
    for r_, Ls in reversed(C.rings):
        Ps = TL(Ls)
        if Ps:
            pg.poly(Ps, fill=HUB_COL, alpha=HUB_A)
            used.add("ring")
    # ---- proposal, soft: widened stream, side arms, reed basins, Demeter's Garden, hidden-stream line
    Ps = TL([w["ring"] for w in C.widen])
    if Ps:
        soft_fill(pg, Ps, WET_COL, 0.85, hal)
        used.add("widen")
    for a in C.arms:
        Q = [T(p) for p in a["P"]]
        if on(Q):
            soft_line(pg, Q, COL["river_mid"], max(1.0, 6.0 * k), 0.6)
            used.add("arm")
    for z in C.D.zones:
        Q = [T(p) for p in z["P"]] if z["code"] in ("WT", "DG") else None
        if not Q or not on(Q):
            continue
        if z["code"] == "WT":
            soft_fill(pg, [Q], WET_COL, 0.8, hal)
            pg.poly([Q], stripes=(COL["river_dark"], 1.6 if big else 0.9, 0.15, 90.0), alpha=0.35)
            used.add("reed")
        else:
            soft_fill(pg, [Q], MP["agriculture"][2], 0.16, hal)
            used.add("dg")
    # ---- proposal, soft: terraces on the contours (upstream): edge + ticks toward the stream
    for P in C.terr:
        Q = [T(p) for p in P]
        if not on(Q):
            continue
        mid = P[len(P) // 2]
        c_, _ = chain_at(C.ref, mid)
        q, _ = at_len(C.ref, arclen(C.ref), c_)
        s = arclen(Q)
        (x, y), (ux, uy) = at_len(Q, s, s[-1] / 2.0)
        qx, qy = T(q)
        side = 1.0 if (-uy) * (qx - x) + ux * (qy - y) > 0 else -1.0
        ticks_line(pg, Q, MP["storage"][2], 0.45 if big else 0.3, 3.0 if big else 1.6, 1.2 if big else 0.6, side,
                   alpha=0.7)
        used.add("terrace")
    # ---- proposal, soft: forest corridor, tree-planted area
    for pts, a_, key in ((C.forest, 0.6, "forest"), (C.trees, 0.4, "trees")):
        r_ = 0.28 if fine else max(0.45, 2.8 * k)       # v27: 9 m apart = 0.9 mm at 1:10,000, dots stay apart
        for p in pts:
            x, y = T(p)
            if -1.0 <= x <= dw + 1.0 and -1.0 <= y <= dh + 1.0:
                pg.circle(x, y, r_, fill=COL["tree_mid"] if key == "forest" else COL["tree"], alpha=a_)
                used.add(key)
    # ---- proposal, soft: hub squares, plane trees, canopied walkway
    for h in C.hubs:
        Ps = TL(h.get("square") or [])
        if Ps:
            soft_fill(pg, Ps, SQ_EDGE, 0.22, hal)
            used.add("square")
            for p in h.get("trees", []):
                x, y = T(p)
                pg.circle(x, y, 0.4 if fine else max(0.7, 4.0 * k), fill="5E7A3A", alpha=0.6)
    for P in C.canopy:
        Q = [T(p) for p in P]
        if on(Q):
            ticks_line(pg, Q, MP["centre"][2], 0.6 if big else 0.45, 2.4 if big else 1.2, 1.0 if big else 0.5, 1.0,
                       alpha=0.6)
            used.add("canopy")
    # ---- v28 (WO-T4b-2): the riverside walk as one route (river_walks runs: bank walk and street footway solid, the
    # walk on a terrace in the bed dashed: it closes in floods), the bike lane beside it on its land side (PL23_BIKE)
    for x in (C.CL.get("W") or {}).get("runs") or []:
        Q = [T(p) for p in x.get("P") or []]
        if len(Q) < 2 or not on(Q):
            continue
        bed = x.get("cls") == "bed"
        pg.line(Q, PL23_WALK_COL, 0.8 if big else 0.5, [1.6, 0.6] if bed else None, cap=0 if bed else 1, alpha=0.85)
        used.add("walk_bed" if bed else "walk")
        if PL23_BIKE and not bed:
            ticks_line(pg, pl23_offset(Q, (1.2 if big else 0.75) * (1.0 if x.get("bank") == "NE" else -1.0)),
                       PL23_BIKE_COL, 0.25, 2.4, 0.5, 1.0 if x.get("bank") == "NE" else -1.0, alpha=0.9)
            used.add("bike")
    # ---- proposal, soft: roads changed (OSM) and the later town line
    for rd in ROADS + [TOWN_LINE]:
        Q = [T(p) for p in rd["xy"]]
        if not on(Q):
            continue
        ch = rd["change"] if rd["change"] in ROAD_CHANGE_COL else "later"
        if ch == "later":
            pg.line(Q, ROAD_CHANGE_COL["later"], 0.9 if big else 0.6, [2.0, 1.0], cap=0, alpha=0.6)
        else:
            soft_line(pg, Q, ROAD_CHANGE_COL[ch], 3.0 if big else (1.2 if fine else 1.6), 0.75)
        used.add("road_" + ch)
    # ---- proposal, soft: new crossings (footbridges, stepping stones)
    for c_ in C.cross:
        if c_["kind"] == "footbridge":
            soft_line(pg, [T(c_["P"][0]), T(c_["P"][1])], ink, 1.4 if big else 0.8, 0.8)
            used.add("foot")
        elif c_["kind"] == "stepping stones":
            A_, B_ = T(c_["P"][0]), T(c_["P"][1])
            for i in range(5):
                f = (i + 0.5) / 5.0
                pg.circle(A_[0] + (B_[0] - A_[0]) * f, A_[1] + (B_[1] - A_[1]) * f, 0.9 if big else 0.35,
                          fill=ink2, alpha=0.7)
            used.add("stones")
    s_ic = 3.0 if big else (1.8 if fine else 2.2)
    for p in C.seats:
        x, y = T(p)
        if 0.0 <= x <= dw and 0.0 <= y <= dh:
            icon(pg, "seat", x, y, s_ic * 0.8)
            used.add("seat")
    if C.terrace:                                         # the sightline toward the Trajaneum (off the plan)
        x, y = T(C.terrace["xy"])
        p2 = (C.terrace["xy"][0] + C.terrace["dir"][0] * 400.0, C.terrace["xy"][1] + C.terrace["dir"][1] * 400.0)
        x2, y2 = T(p2)
        pg.line([(x, y), (x2, y2)], COL["accent"], 0.35, [1.4, 0.8], cap=0, alpha=0.7)
        used.add("sight")
    # ---- pictograms: hubs, sub-hubs, cafes, education, viewing terrace, H4 step, H6 deck, gateway
    ic = []
    for h in C.hubs:
        ic.append(("transit" if h["role"] == "transit" else ("gate" if h["id"] == u"K6" else "walkhub"), h["xy"]))
        if h.get("sub_xy"):
            ic.append(("sub", h["sub_xy"]["c"]))
    for z in C.D.zones:
        if z["code"] in ("GR", "DG"):
            ic.append(("cafe", z["q"]))
        if z["code"] == "WT":
            ic.append(("edu", z["q"]))
        if z["code"] == "WS" or (z["code"] == "WA" and z["tier"] == "F"):
            ic.append(("seat", z["q"]))
    ic += [("edu", CRAFT_XY), ("deck", ROMAN_WALL), ("view", C.terrace["xy"]) if C.terrace else None]
    for it in [i_ for i_ in ic if i_]:
        x, y = T(it[1])
        if 0.0 <= x <= dw and 0.0 <= y <= dh:
            icon(pg, it[0], x, y, s_ic * (1.25 if it[0] in ("transit", "walkhub", "gate") else 1.0))
            taken.append((x - s_ic * 0.6, y - s_ic * 0.6, x + s_ic * 0.6, y + s_ic * 0.6))
            used.add(it[0])
    # ---- words: place names (large; v27: 7.5 pt on the 1:10,000 strip), (v27: the detail labels moved to 02e)
    names = [(HUB_NAME[h["id"]], h["xy"]) for h in C.hubs] + \
        [(nm, xy) for nm, xy in BRIDGES_K if nm in (u"K1", u"K2")] + PLACES
    for nm, xy in names:
        if inP(xy):
            place_label(pg, [(nm, PL28_TS if fine else (PL23_NAME_TS if k < 0.5 else PLACE_TS * 1.15), True)], T(xy),
                        taken, dw, dh, ink, d0=1.5, anywhere=False)   # v27: 7.5 pt on the 1:10,000 strip (G4); v28: 9 pt at 1:5,000
    if C.terrace and inP(C.terrace["xy"]):
        x, y = T(C.terrace["xy"])
        p2 = (C.terrace["xy"][0] + C.terrace["dir"][0] * 120.0, C.terrace["xy"][1] + C.terrace["dir"][1] * 120.0)
        x2, y2 = T(p2)
        place_label(pg, [(u"TRAJAN TAPINAĞI {:,.0f} m".format(C.terrace["d"]), LAB_TS, True)],   # v28: Turkish (G6)
                    (min(max(x2, 1.0), dw - 1.0), min(max(y2, 1.0), dh - 1.0)), taken, dw, dh, COL["accent"], d0=1.0)
    return used, placed                                  # v27: the detail windows' labels went (p.24 = 02e)


# ---------------------------------------------------------------- G10: one frame figure
def pl28_frame_stats(C):
    """v27 (MIRAQUA 28 Oct, G10): C.frame_m2 = the frame polygon's area (shoelace: 150.52 ha for site_alan, the figure
    the site board prints on p.02); C.inF = 1 for each grid cell whose centre lies inside the frame (the grid
    overshoots it by up to one cell on each axis, which made 151 ha); each such cell stands for frame area / cells
    inside (C.cell_m2, within 0.3 % of c x c), so C.stats {0 open, 1 building, 2 road, 3 bed: m2} adds up to the
    frame exactly. One pass over the grid (was four)."""
    G, V, F = C.G, C.V, C.F
    P = list(getattr(V, "frame_P", None) or V.P)          # build_all sets V.frame_P = site_alan
    inF = bytearray(C.N)
    for n in G.poly_cells([V.uv(p) for p in P]):
        inF[n] = 1
    C.frame_m2 = abs(area2(P))
    C.inF = inF
    C.cell_m2 = C.frame_m2 / float(inF.count(1) or 1)
    Fin = bytes(v if i else 9 for v, i in zip(F, inF))
    C.stats = dict((k_, Fin.count(k_) * C.cell_m2) for k_ in (0, 1, 2, 3))


# ---------------------------------------------------------------- G7 / G8: the strip and the study area
def pl28_strip(C, k):
    """v27 (G7): the whole analysis frame as ONE strip, the water left to right (View: the upstream end at u0): T
    (world -> strip mm, y up), inP (world point on the strip), its size dw x dh mm."""
    V = C.V

    def T(p):
        u, v = V.uv(p)
        return (u - V.u0) * k, (v - V.v0) * k

    def inP(p):
        u, v = V.uv(p)
        return V.u0 <= u <= V.u1 and V.v0 <= v <= V.v1
    return {"T": T, "inP": inP, "dw": (V.u1 - V.u0) * k, "dh": (V.v1 - V.v0) * k}


def pl28_study(C):
    """G8: the study area's outlines (calisma_alan, both parts; build_all sets V.study), survey m."""
    return [list(P) for P in (getattr(C.V, "study", None) or []) if len(P) >= 3]


def pl28_draw_study(pg, C, T):
    """G8: the study area outline in R28_STUDY_LINE (dash-dot) on a plan page; True when drawn."""
    st = R28_STUDY_LINE
    rs = pl28_study(C)
    for P in rs:
        Q = [T(p) for p in P]
        pg.line(Q + Q[:1], st["colour"], st["width_mm"], list(st["dash_mm"]), cap=0)
    return bool(rs)


def pl28_sw_study():
    """G8: the study area's legend sample."""
    return _sw_line(R28_STUDY_LINE["colour"], R28_STUDY_LINE["width_mm"], list(R28_STUDY_LINE["dash_mm"]))


def pl28_runs(sh, x, y, runs, size, colour):
    """One line of text in runs [(text, bold)] (G5: the bold keyword inside a line); returns its end x."""
    for t, bd in runs:
        if t:
            sh.text(t, x, y, size, colour, bold=bd)
            x += text_w(t, size, bd)
    return x


def pl28_marks(sh, C, x0, y0):
    """v27: the row under a strip, from (x0, y0) up (10 mm): the north arrow (survey +Y turned with the plan), the
    1:10,000 scale bar right beside it (SCRIPT_STANDARD §8: next to every orthogonal drawing) and which way the water
    flows."""
    V = C.V
    nu, nv = V.uv((V.cx, V.cy + 1.0))
    L = math.hypot(nu, nv) or 1.0
    nx_, ny_ = nu / L, nv / L
    ax, ay = x0 + 3.5, y0 + 5.0
    tip = (ax + nx_ * 3.5, ay + ny_ * 3.5)
    sh.poly([[tip, (ax - ny_ * 1.6 - nx_ * 3.0, ay + nx_ * 1.6 - ny_ * 3.0), (ax - nx_ * 1.8, ay - ny_ * 1.8)]],
            fill=COL["ink_dark"])
    sh.poly([[tip, (ax - nx_ * 1.8, ay - ny_ * 1.8), (ax + ny_ * 1.6 - nx_ * 3.0, ay - nx_ * 1.6 - ny_ * 3.0)]],
            fill=COL["white"], stroke=COL["ink_dark"], lw=0.15)
    sh.text(u"N", tip[0] + 1.2, tip[1] - 0.6, 2.6, COL["ink_dark"], bold=True)
    scale_bar(sh, x0 + 12.0, y0 + 2.0, MP_SCALE, PL28_MARKS)
    xs = x0 + 12.0 + PL28_MARKS[-1] * 1000.0 / MP_SCALE + 6.0 + text_w(u"1:{:,.0f}".format(MP_SCALE), 3.4, True) + 8.0
    pl28_runs(sh, xs, y0 + 2.0, [(u"the water flows ", False), (u"left to right", True),
                                 (u", the upstream entry at the left end", False)], PL28_TS, COL["ink2"])


def pl28_legend(sh, groups, x0, x1, y_top, y_min, ncols, warn, pitch=3.6):
    """v27: the legend in ncols columns from x0 to x1, top down from y_top to y_min: each group a bold head, then its
    drawn samples with plain names (only what the page draws); a head never ends a column; rows closer (to 3.0 mm)
    when they would not fit."""
    rows = []
    for head, items in groups:
        if items:
            rows += [(head, None)] + list(items)
    if not rows:
        return
    need = int(math.ceil(len(rows) / float(ncols))) + 1
    pitch = max(3.0, min(pitch, (y_top - y_min) / float(need)))
    R = max(2, int((y_top - y_min) / pitch))
    cols, cur = [], []
    for r_ in rows:
        if cur and (len(cur) >= R or (r_[1] is None and len(cur) >= R - 1)):
            cols.append(cur)
            cur = []
        cur.append(r_)
    cols.append(cur)
    if len(cols) > ncols:
        warn.append(u"legend: {} rows do not fit {} columns beside the strip".format(len(rows), ncols))
    cw = (x1 - x0) / float(ncols)
    for c, col in enumerate(cols):
        cx = x0 + c * cw
        for j, (nm, f) in enumerate(col):
            cy = y_top - j * pitch
            if f is None:
                sh.text(nm, cx, cy - 2.6, PL28_TS, COL["ink_dark"], bold=True)
                continue
            f(sh, cx, cy - 2.9, 6.0, 2.4)
            sh.text(nm, cx + 7.5, cy - 2.6, PL28_TS, COL["ink"])
            if text_w(nm, PL28_TS) > cw - 8.5:
                warn.append(u"legend name runs into the next column: {}".format(nm))


# ---------------------------------------------------------------- P23: markers, list, sources
def pl28_note_group(nt):
    """P23.1: the R28_MARKERS group of a numbered note: roads; hubs and transit (the later town bus line too); water
    and ecology (reed basins, terraces, hidden stream, widened stream, side arm, the edges kept); crossings
    (footbridges); heritage and views."""
    k = nt["key"]
    if k[0] == "road":
        return "hubs" if k[1] == TOWN_LINE["name"] else "roads"
    return {"hub": "hubs", "foot": "crossings", "h4": "heritage", "h6": "heritage", "view": "heritage"}.get(k[0], "water")


def pl28_note_entry(C, nt):
    """P23.2: (name, one short line) of a numbered note for the list, in plain words from the note's own data. No
    source codes: they go to the sources page with every reason, whole (pl28_plan_sources)."""
    k = nt["key"]
    less = u"less than {:.0f} m open".format(KEPT_MAX)
    if k[0] == "hub":
        h = next((h_ for h_ in C.hubs if h_["id"] == k[1]), {})
        nm = PL28_HUB.get(k[1], k[1])
        if h.get("role") == "transit":
            return nm + u" · transit hub", u"town bus lines stop here · " + (
                u"square over the culvert" if k[1] == u"İstiklal" else u"by the Red Hall tunnels")
        if k[1] == u"K6":
            return nm + u" · gateway out", u"the primary road is kept · bus stop {} {:.0f} m".format(
                h.get("stop", u""), h.get("stop_m", 0.0))
        extra = {u"K3": u" · workshops, education", u"K5": u" · Demeter's Garden"}.get(k[1], u"")
        sub = u", sub-hub in the bed" if h.get("sub_xy") else u""
        return nm + u" · walking hub", (u"dry square" if extra else u"dry square at the Roman bridge") + sub + extra
    if k[0] == "road":
        if k[1] == TOWN_LINE["name"]:
            return u"Town bus line to K4 · later step", u"on the existing streets from İstiklal to the K4 stop"
        rd = next((r_ for r_ in ROADS if r_["name"] == k[1]), None)
        if rd is not None:
            ch, _, rest = rd["note"].partition(u": ")
            return u"{}{} · {}".format(rd["name"][:1].upper(), rd["name"][1:], ch), rest
    if k[0] == "kept":
        return {"building": (u"Edge kept · buildings", u"buildings stand at the bank, " + less),
                "road": (u"Edge kept · road", u"a road runs at the bank, " + less),
                "frame": (u"Nothing placed", u"the edge of the analysis frame, " + less)}.get(
            k[1], (nt["text"][:1] + nt["text"][1:].lower(), less))
    if k[0] == "view" and C.terrace:
        return u"Viewing terrace", u"a clear sightline to Trajan Tapınağı, {:,.0f} m away".format(C.terrace["d"])
    if k[0] == "widen" and C.widen:
        lo, hi = min(w["fw"][0] for w in C.widen), max(w["fw"][1] for w in C.widen)
        return u"Stream widened", u"room for water and a wetland · {:.0f}-{:.0f} m open beside the bank".format(lo, hi)
    if k[0] == "foot":
        return u"Footbridge" + (u"s" if len(nt["at"]) > 1 else u""), \
            u"{:.0f}+ m of stream without a crossing · both landings open".format(FOOT_GAP_M)
    fixed = {"h4": (u"Step to the water", u"facing Tabaklar Hamamı, a bath ruin 1.5 m from the stream"),
             "h6": (u"Deck over the Roman bank wall", u"a Roman complex with a bank wall of about 120 m"),
             "wt": (u"Reed basins", u"the water is cleaned once · clean-water classroom"),
             "terr": (u"Rain terraces on the contours", u"they hold the rain · overflow to the reed basins"),
             "cov": (u"Hidden stream", u"nothing opened: the water line drawn in the paving"),
             "arm": (u"Side arm", u"a planted channel cleans the return water")}   # v28 (D2 a): reed only in lined basins
    return fixed.get(k[0], (nt["text"][:1] + nt["text"][1:].lower(), u""))


def pl28_letter(i):
    return u"abcdefghijklmnopqrstuvwxyz"[i] if i < 26 else str(i + 1)


def pl28_list_head(sh, lab, col, x, y, cw):
    """a group's head in the list: its name in its colour, bold, over a hairline; returns the y under it"""
    y -= PL28_HEAD_TS * 1.18
    sh.text(lab, x, y + PL28_HEAD_TS * 0.2, PL28_HEAD_TS, col, bold=True)
    y -= 1.3
    sh.line([(x, y), (x + cw, y)], col, 0.2, alpha=0.5)
    return y - 2.6


def pl28_list_nogo(sh, nis, x, y, cw):
    """the areas left as they are: grey letter, its size in ha (G13) in bold, why (its source tag goes to the
    sources page); returns the y under it"""
    y = pl28_list_head(sh, u"Left as it is · no intervention", COL["ink2"], x, y, cw)
    rn, tx = PL28_NI_R, x + 2 * BADGE_R + 2.2
    for lt, r_, ok in nis:
        sh.circle(x + BADGE_R, y - rn, rn, fill=COL["white"], stroke=COL["ink2"], lw=0.2)
        sh.text(lt, x + BADGE_R, y - rn - KEY_MIN * 0.36, KEY_MIN, COL["ink2"], bold=True, align="C")
        ha = u_area(r_["ha"] * 1e4, "ha")
        yy = y - PL28_TS * 1.18
        x1 = pl28_runs(sh, tx, yy + PL28_TS * 0.2, [(ha, True), (u" · ", False)], PL28_TS, COL["ink"])
        for i, s_ in enumerate(wrap(PL28_SRC_TAG.sub(u"", r_["why"]), PL28_TS, max(20.0, x + cw - x1))):
            if i:
                yy -= PL28_TS * 1.18
            sh.text(s_, x1, yy + PL28_TS * 0.2, PL28_TS, COL["ink2"])
        y = min(yy, y - 2 * rn) - 1.6
    return y


def pl28_src_kind(s):
    """N2 / F5 hint for the booklet's sources page: "public online" (OSM, its bus stops, ESA WorldCover, DSI, EPA),
    "project note" (history cards h01-h03, decisions D/H, register codes P/E), else "booklet analysis" (survey, open
    ground, edge plan, water board cuts, city link)."""
    if re.search(u"\\bOSM\\b|WorldCover|satellite 2021|\\bDSI\\b|\\bEPA\\b|bus stop", s):
        return u"public online"
    if re.search(u"\\b(h0\\d|H\\d|D\\d{1,2}|P\\d{2}|E\\d{2})\\b", s):
        return u"project note"
    return u"booklet analysis"


def pl28_plan_sources(ents, nis):
    """P23.2 / N2: what the page does not print, for the booklet's sources page, keyed by the marker numbers (and
    letters) on the masterplan page. v28 (revision 29 Oct, WO-T4b-2, D13): only the public sources (pl28_src_kind
    "public online"); a move or area with none keeps an empty list."""
    pub = lambda s_: pl28_src_kind(s_) == u"public online"
    return {"crop": "mp_plan", "heading": u"Masterplan: what each numbered move stands on",
            "markers": [{"n": nt["n"], "group": grp, "name": nm, "line": line,
                         "sources": [{"text": s_, "kind": u"public online"} for s_ in nt["why"] if pub(s_)]}
                        for nt, grp, nm, line, ok in ents],
            "left_as_is": [{"id": lt, "ha": round(r_["ha"], 2), "why": PL28_SRC_TAG.sub(u"", r_["why"]),
                            "sources": [n_ for n_ in (PL28_SRC_NAME.get(m_, m_)
                                                      for m_ in PL28_SRC_TAG.findall(r_["why"])) if pub(n_)]}
                           for lt, r_, ok in nis]}


# ---------------------------------------------------------------- v28 (WO-T4b-2): rows, route, callouts, side column
def pl23_offset(Q, d):
    """the polyline Q (page mm) moved d mm to its left (negative: to its right), each vertex along the normal of its
    neighbours' chord"""
    out, n = [], len(Q)
    for i in range(n):
        a, b = Q[max(0, i - 1)], Q[min(n - 1, i + 1)]
        ux, uy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(ux, uy) or 1.0
        out.append((Q[i][0] - uy / L * d, Q[i][1] + ux / L * d))
    return out


def pl23_rows(C, warn):
    """(scale, rows): two rows at PL23_SCALE when they fit the crop beside a PL23_SIDE_MIN side column, else one strip
    at PL23_FALLBACK. A row = {a, b: m from the frame's upstream end drawn; ea, eb: its own part (names, markers)}."""
    V = C.V
    L, Hm = V.u1 - V.u0, V.v1 - V.v0
    k = 1000.0 / PL23_SCALE
    w2, h2 = (L / 2.0 + PL23_OVL) * k, Hm * k
    if w2 <= BK_W - PL23_SIDE_MIN - PL23_SIDE_GAP and 2.0 * (h2 + PL23_MARK_H) + PL23_GAP <= BK_H:
        m = L / 2.0
        return PL23_SCALE, [dict(a=0.0, b=m + PL23_OVL, ea=0.0, eb=m), dict(a=m - PL23_OVL, b=L, ea=m, eb=L)]
    warn.append(u"masterplan page: two rows at 1:{:,.0f} ({:.0f} x {:.0f} mm each) do not fit the page: one strip at "
                u"1:{:,.0f}".format(PL23_SCALE, w2, h2, PL23_FALLBACK))
    return PL23_FALLBACK, [dict(a=0.0, b=L, ea=0.0, eb=L)]


def pl23_row_T(C, row, k, x0=0.0, y0=0.0):
    """(T, mine) of a row: T world -> page mm with the row's upstream end at x0 and the frame's foot at y0; mine(p) =
    the point lies in the row's own part of the frame"""
    V = C.V

    def T(p):
        u, v = V.uv(p)
        return (u - V.u0 - row["a"]) * k + x0, (v - V.v0) * k + y0

    def mine(p):
        u, v = V.uv(p)
        return V.u0 + row["ea"] <= u <= V.u0 + row["eb"] and V.v0 <= v <= V.v1
    return T, mine


def pl23_marks(sh, C, x0, y0, scale, runs):
    """the row under a map row, from (x0, y0) up: north arrow (survey +Y turned with the plan), the scale bar right
    beside it (SCRIPT_STANDARD §8) and a short note in runs [(text, bold)]"""
    V = C.V
    nu, nv = V.uv((V.cx, V.cy + 1.0))
    L = math.hypot(nu, nv) or 1.0
    nx_, ny_ = nu / L, nv / L
    ax, ay = x0 + 3.5, y0 + 5.0
    tip = (ax + nx_ * 3.5, ay + ny_ * 3.5)
    sh.poly([[tip, (ax - ny_ * 1.6 - nx_ * 3.0, ay + nx_ * 1.6 - ny_ * 3.0), (ax - nx_ * 1.8, ay - ny_ * 1.8)]],
            fill=COL["ink_dark"])
    sh.poly([[tip, (ax - nx_ * 1.8, ay - ny_ * 1.8), (ax + ny_ * 1.6 - nx_ * 3.0, ay - nx_ * 1.6 - ny_ * 3.0)]],
            fill=COL["white"], stroke=COL["ink_dark"], lw=0.15)
    sh.text(u"N", tip[0] + 1.2, tip[1] - 0.6, 2.6, COL["ink_dark"], bold=True)
    mk = PL23_MARKS.get(scale, PL28_MARKS)
    scale_bar(sh, x0 + 12.0, y0 + 2.0, scale, mk)
    xs = x0 + 12.0 + mk[-1] * 1000.0 / scale + 6.0 + text_w(u"1:{:,.0f}".format(scale), 3.4, True) + 8.0
    pl28_runs(sh, xs, y0 + 2.0, runs, PL28_TS, COL["ink2"])


def pl23_busy(C, T, half=1.4):
    """boxes (sheet mm) the callouts keep off: the stream bed edges and the proposals' lines (walk, canopy, side arms,
    roads changed, hidden stream, crossings) along their length; the small proposal areas (widened stream, reed
    basins, Demeter's Garden, hub squares) whole"""
    out = []
    lines = list(C.bed_loops) + list(C.covered) + list(C.canopy) + [a["P"] for a in C.arms] + \
        [x.get("P") or [] for x in (C.CL.get("W") or {}).get("runs") or []] + [rd["xy"] for rd in ROADS] + \
        [c_["P"] for c_ in C.cross]
    for P in lines:
        if len(P) >= 2:
            out += boxes_along([T(p) for p in P], half)
    rings = [w["ring"] for w in C.widen] + [z["P"] for z in C.D.zones if z["code"] in ("WT", "DG")] + \
        [L_ for h in C.hubs for L_ in (h.get("square") or [])]
    for R in rings:
        if len(R) >= 3:
            out.append(bbox([T(p) for p in R]))
    return out


def pl23_spot(x, y, w, h, taken, boxes, bounds, rings=PL23_RINGS):
    """a free w x h box round (x, y) inside bounds, off the taken boxes (only those within reach are tested), its
    arrow from the place never through a placed callout (boxes); the box or None"""
    R = rings[-1] + w + h
    near = [t for t in taken if t[2] > x - R and t[0] < x + R and t[3] > y - R and t[1] < y + R]
    for d in rings:
        for i in range(16):
            a = math.radians(i * 22.5 + 11.25)
            cx, cy = x + math.cos(a) * (d + w / 2.0), y + math.sin(a) * (d + h / 2.0)
            b = (cx - w / 2.0, cy - h / 2.0, cx + w / 2.0, cy + h / 2.0)
            if b[0] < bounds[0] or b[1] < bounds[1] or b[2] > bounds[2] or b[3] > bounds[3]:
                continue
            if any(lp_hit(b, t, 0.5) for t in near):
                continue
            e = lp_leader_end(b, (x, y))
            if any(_lp_seg_box((x, y), e, t) for t in boxes):
                continue
            return b
    return None


def pl23_box_lines(nm, line, w_max):
    """a callout's rows [(text, size, bold)] wrapped beside its number badge (name 7.5 pt bold, line 7 pt) and its
    box size (w, h), mm"""
    tw = w_max - 2 * BADGE_R - 2.4
    rows = [(s_, PL28_TS, True) for s_ in wrap(nm, PL28_TS, tw, True)] + \
        [(s_, KEY_MIN, False) for s_ in (wrap(line, KEY_MIN, tw) if line else [])]
    w = min(w_max, max(text_w(s_, sz, bd) for s_, sz, bd in rows) + 2 * BADGE_R + 2.4)
    h = max(2 * BADGE_R + 1.2, sum(sz * 1.18 for s_, sz, bd in rows) + 1.2)
    return rows, w, h


def pl23_badge(sh, cx, cy, n, col):
    sh.circle(cx, cy, BADGE_R + 0.25, fill=COL["white"])
    sh.circle(cx, cy, BADGE_R, fill=col)
    sh.text(str(n), cx, cy - BADGE_TS * 0.36, BADGE_TS, COL["white"], bold=True, align="C")


def pl23_box(sh, b, n, rows, col):
    """a callout: white box with a hairline in the move's group colour, the number badge top-left, the rows beside it"""
    sh.poly([rect(b[0], b[1], b[2], b[3])], fill=COL["white"], stroke=col, lw=0.25, alpha=0.94)
    pl23_badge(sh, b[0] + 0.6 + BADGE_R, b[3] - 0.6 - BADGE_R, n, col)
    x, y = b[0] + 2 * BADGE_R + 1.8, b[3] - 0.6
    for s_, sz, bd in rows:
        y -= sz
        sh.text(s_, x, y, sz, COL["ink"] if bd else COL["ink2"], bold=bd)
        y -= sz * 0.18


def pl23_arrow(sh, p, q, col):
    """an arrow from the box edge q to the place p, its small head at the place"""
    d = math.hypot(p[0] - q[0], p[1] - q[1])
    if d < 0.8:
        return
    ux, uy = (p[0] - q[0]) / d, (p[1] - q[1]) / d
    hl = min(1.3, d * 0.5)
    bx, by = p[0] - ux * hl, p[1] - uy * hl
    sh.line([q, (bx, by)], col, 0.2)
    sh.poly([[p, (bx - uy * hl * 0.4, by + ux * hl * 0.4), (bx + uy * hl * 0.4, by - ux * hl * 0.4)]], fill=col)


def pl23_callouts(sh, C, rws, taken):
    """P23.1 (R13, R14): every numbered move as a short boxed text on the map by its first place, on an arrow; its
    further places get the number badge alone. rws = [(T, mine, bounds)] per row (sheet mm). Returns (ents, nis):
    [[note, group, name, line, on the map]], [[letter, region, placed]]; moves with no room on the map are listed
    in the side column (pl23_side)."""
    mk = dict((k_, hx) for k_, lab, hx in R28_MARKERS)
    boxes, ents, nis = [], [], []
    for nt in sorted(C.notes, key=lambda nt_: nt_["n"]):
        grp = pl28_note_group(nt)
        nm, line = pl28_note_entry(C, nt)
        ent = [nt, grp, nm, line, False]
        ents.append(ent)
        col = mk[grp]
        rows, w, h = pl23_box_lines(nm, line, PL23_BOX_W)
        first = True
        for p in nt["at"]:
            rw = next((r_ for r_ in rws if r_[1](p)), None)
            if rw is None:
                continue
            T, _, bounds = rw
            x, y = T(p)
            if first:
                first = False
                b = pl23_spot(x, y, w, h, taken, boxes, bounds)
                if b is not None:
                    taken.append(b)
                    boxes.append(b)
                    pl23_box(sh, b, nt["n"], rows, col)
                    pl23_arrow(sh, (x, y), lp_leader_end(b, (x, y)), col)
                    ent[4] = True
                    continue
            s = 2 * BADGE_R + 0.5                         # a further place (or no room for the box): the badge
            b = (x - s / 2, y - s / 2, x + s / 2, y + s / 2)
            if any(lp_hit(b, t, 0.3) for t in taken if t[2] > x - 6 and t[0] < x + 6 and t[3] > y - 6 and t[1] < y + 6):
                b = pl23_spot(x, y, s, s, taken, boxes, bounds, rings=(1.0, 2.5, 5.0, 8.0))
                if b is None:
                    continue
            cx, cy = (b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0
            if math.hypot(cx - x, cy - y) > BADGE_R + 0.4:
                pl23_arrow(sh, (x, y), lp_leader_end(b, (x, y)), col)
            taken.append(b)
            pl23_badge(sh, cx, cy, nt["n"], col)
    rn = PL28_NI_R
    for i, r_ in enumerate(C.nogo):                       # the areas left as they are: a grey letter by their spot
        nis.append([pl28_letter(i), r_, False])
        for p in r_["at"]:
            rw = next((x_ for x_ in rws if x_[1](p)), None)
            if rw is None:
                continue
            T, _, bounds = rw
            x, y = T(p)
            b = pl23_spot(x, y, 2 * rn, 2 * rn, taken, boxes, bounds, rings=(0.0, 1.5, 3.5, 6.0, 9.0))
            if b is None:
                continue
            taken.append(b)
            cx, cy = (b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0
            if math.hypot(cx - x, cy - y) > rn + 0.4:
                sh.line([(x, y), lp_leader_end(b, (x, y))], COL["ink2"], 0.15)
            sh.circle(cx, cy, rn, fill=COL["white"], stroke=COL["ink2"], lw=0.2)
            sh.text(nis[-1][0], cx, cy - KEY_MIN * 0.36, KEY_MIN, COL["ink2"], bold=True, align="C")
            nis[-1][2] = True
            r_["placed"] = r_.get("placed", 0) + 1
            break
    return ents, nis


def pl23_hub_gaps(sh, C, rws, taken):
    """R14: along the walk, the distance between neighbouring bridge hubs (K4, K3, K5, K6) on the stream line, small
    and grey by the middle of the stretch; dropped where there is no room"""
    hs = [h for h in C.hubs if h["id"] in (u"K4", u"K3", u"K5", u"K6")]
    ch = sorted((chain_at(C.ref, h["xy"])[0], h["id"]) for h in hs)
    s = arclen(C.ref)
    for (c0, a), (c1, b) in zip(ch, ch[1:]):
        p = at_len(C.ref, s, (c0 + c1) / 2.0)[0]
        rw = next((r_ for r_ in rws if r_[1](p)), None)
        if rw is None:
            continue
        T, _, bounds = rw
        x, y = T(p)
        t_ = u"{} to {}: {:,.0f} m along the stream".format(a, b, c1 - c0)
        w, h = text_w(t_, KEY_MIN), KEY_MIN * 1.18
        bx = pl23_spot(x, y, w, h, taken, (), bounds, rings=(2.0, 4.0, 7.0))
        if bx is None:
            continue
        taken.append(bx)
        sh.text(t_, bx[0], bx[1] + KEY_MIN * 0.25, KEY_MIN, PL23_WALK_COL, halo=COL["white"])


def pl23_nogo_h(nis, cw):
    """the height pl28_list_nogo takes for these areas in a column cw mm wide, mm"""
    if not nis:
        return 0.0
    h = PL28_HEAD_TS * 1.18 + 1.3 + 2.6
    rn, tx = PL28_NI_R, 2 * BADGE_R + 2.2
    for lt, r_, ok in nis:
        x1 = tx + text_w(u_area(r_["ha"] * 1e4, "ha"), PL28_TS, True) + text_w(u" · ", PL28_TS)
        n = max(1, len(wrap(PL28_SRC_TAG.sub(u"", r_["why"]), PL28_TS, max(20.0, cw - x1))))
        h += max(n * PL28_TS * 1.18, 2 * rn) + 1.6
    return h


def pl23_side(sh, x0, x1, H, used, ents, nis, warn):
    """the side column from x0 to x1: on top the small legend (two columns, only what the page draws), under it the
    moves that found no room on the map (number, name, line), at its foot the areas left as they are"""
    cw = x1 - x0
    more = [e for e in ents if not e[4]]
    mk = dict((k_, hx) for k_, lab, hx in R28_MARKERS)
    lines_more = [(e,) + pl23_box_lines(e[2], e[3], cw)[:1] for e in more]
    h_more = (PL28_HEAD_TS * 1.18 + 3.9 + sum(sum(sz * 1.18 for s_, sz, bd in rows) + 1.8
                                                for e, rows in lines_more)) if more else 0.0
    h_nogo = pl23_nogo_h(nis, cw)
    leg_ = PL23_LEGEND + [(k_, nm, f) for k_, nm, f in LEGEND_V24 if k_ not in PL23_LEG_KEYS]
    groups = [(u"EXISTING · SURVEY", [(nm, f) for key, nm, f in leg_ if key in used and key in EXISTING]),
              (u"PROPOSED", [(nm, f) for key, nm, f in leg_ if key in used and key not in EXISTING])]
    n = sum(len(it) + 1 for _, it in groups if it)
    rows = int(math.ceil(n / 2.0)) + 1
    room = H - h_nogo - h_more - 4.0
    pitch = max(3.0, min(3.6, room / float(rows)))
    y_leg = H - rows * pitch
    pl28_legend(sh, groups, x0, x1, H, y_leg, 2, warn, pitch=pitch)
    y = y_leg - 2.0
    if more:
        y = pl28_list_head(sh, u"More moves", COL["ink2"], x0, y, cw)
        tx = x0 + 2 * BADGE_R + 2.2
        for e, rows_ in lines_more:
            pl23_badge(sh, x0 + BADGE_R, y - BADGE_R, e[0]["n"], mk[e[1]])
            yy = y
            for s_, sz, bd in rows_:
                yy -= sz * 1.18
                sh.text(s_, tx, yy + sz * 0.2, sz, COL["ink"] if bd else COL["ink2"], bold=bd)
            y = min(yy, y - 2 * BADGE_R) - 1.8
    if nis:
        if y < h_nogo + 1.0:
            warn.append(u"masterplan page: the side column runs {:.1f} mm over (legend, moves, areas left as they "
                        u"are)".format(h_nogo + 1.0 - y))
        pl28_list_nogo(sh, nis, x0, h_nogo + 1.0, cw)


# v28: the route's legend samples (before the core's LEGEND_V24 rows of the same key)
def _pl23_sw_bike():
    def f(pg, x, y, w, h):
        pg.line([(x, y + h * 0.3), (x + w, y + h * 0.3)], PL23_WALK_COL, 0.5, alpha=0.85)
        ticks_line(pg, [(x, y + h * 0.65), (x + w, y + h * 0.65)], PL23_BIKE_COL, 0.25, 1.6, 0.5, 1.0, alpha=0.9)
    return f


PL23_LEGEND = [("walk", u"Riverside walk", _sw_line(PL23_WALK_COL, 0.5, alpha=0.85)),
               ("walk_bed", u"Bed walk, shut in floods", _sw_line(PL23_WALK_COL, 0.5, [1.6, 0.6], 0.85)),
               ("bike", u"Bike lane beside the walk", _pl23_sw_bike()),
               ("arm", u"Planted side arm", _sw_softline(COL["river_mid"], 1.6, 0.6))]   # D2 a: not "reed"
PL23_LEG_KEYS = set(k_ for k_, _, _ in PL23_LEGEND)


# ---------------------------------------------------------------- the page
def plan_page(C, warn):
    """v28 (revision 29 Oct, WO-T4b-2, package H "Page 23"): the masterplan page (crop mp_plan, 392 x 238 mm). The
    analysis frame in two rows at 1:5,000 (pl23_rows; one 1:10,000 strip when they do not fit), upstream half on top,
    each with every layer of the corridor (draw_corridor: the walk and bike lane too), the study area outline, a
    dashed match line where the halves meet and its marks row (north arrow, scale bar, flow note). On the map: place
    names (Turkish), the numbered moves as short boxed texts on arrows and the letters of the areas left as they are
    (pl23_callouts), the distances between the bridge hubs along the walk (pl23_hub_gaps). The side column: small
    legend, moves with no room on the map, the areas left as they are (pl23_side). Public sources go to the sources
    page (sh.plan_sources -> plan_sources)."""
    scale, rows = pl23_rows(C, warn)
    k = 1000.0 / scale
    V = C.V
    W, H = BK_W, BK_H
    dh = (V.v1 - V.v0) * k
    sh = Page(W, H)
    sh.poly([rect(0, 0, W, H)], fill=COL["paper"])
    used, taken, rws, x_side = set(), [], [], 0.0
    y_top = H
    for i, row in enumerate(rows):
        dw = (row["b"] - row["a"]) * k
        x0, y0 = 0.0, y_top - dh
        T, mine = pl23_row_T(C, row, k)
        tk = [b for P in pl28_study(C) for b in boxes_along([T(p) for p in P + P[:1]], 1.2)]   # G4: names keep off it
        pg = Page(dw, dh)
        u_, _ = draw_corridor(pg, T, k, C, mine, tk, dw, dh)
        used |= u_
        if pl28_draw_study(pg, C, T):
            used.add("study")
        sh.clip([rect(x0, y0, x0 + dw, y0 + dh)])
        blit(sh, pg, x0, y0)
        sh.unclip()
        sh.poly([rect(x0, y0, x0 + dw, y0 + dh)], stroke=COL["ink2"], lw=0.25, alpha=0.45)   # the row's edge = the frame
        Ts, _ = pl23_row_T(C, row, k, x0, y0)
        taken += [(b[0] + x0, b[1] + y0, b[2] + x0, b[3] + y0) for b in tk]
        taken += [b for b in pl23_busy(C, Ts) if b[2] > x0 and b[0] < x0 + dw and b[3] > y0 and b[1] < y0 + dh]
        if len(rows) > 1:                                 # the match line where the halves meet
            xm = x0 + ((row["eb"] if i == 0 else row["ea"]) - row["a"]) * k
            sh.line([(xm, y0), (xm, y0 + dh)], COL["ink2"], 0.3, [1.6, 0.8], cap=0)
            t_ = u"match line · continues in the row below" if i == 0 else u"match line · from the row above"
            tw = text_w(t_, KEY_MIN)
            tx = xm - 1.2 - tw if i == 0 else xm + 1.2
            sh.text(t_, tx, y0 + dh - 3.4, KEY_MIN, COL["ink2"], halo=COL["white"])
            taken.append((tx, y0 + dh - 3.8, tx + tw, y0 + dh - 0.4))
            taken.append((xm - 0.8, y0, xm + 0.8, y0 + dh))
        rws.append((Ts, mine, (x0 + 0.8, y0 + 0.8, x0 + dw - 0.8, y0 + dh - 0.8)))
        if i == 0:
            runs = [(u"the water flows ", False), (u"left to right", True), (u", the upstream entry at the left end", False)]
        else:
            runs = [(u"downstream half · ", True), (u"the water flows left to right", False)]
        pl23_marks(sh, C, x0, y0 - PL23_MARK_H, scale, runs)
        x_side = max(x_side, dw)
        y_top = y0 - PL23_MARK_H - PL23_GAP
    if y_top + PL23_GAP < -0.5 or x_side > W - PL23_SIDE_MIN:
        warn.append(u"masterplan page: the map ({:.0f} x {:.0f} mm) runs over the {:.0f} x {:.0f} mm crop".format(
            x_side, H - y_top - PL23_GAP, W, H))
    ents, nis = pl23_callouts(sh, C, rws, taken)
    pl23_hub_gaps(sh, C, rws, taken)
    for nt, grp, nm, line, ok in ents:
        if not ok:
            warn.append(u"masterplan move {} has no room on the map: listed in the side column ({})".format(nt["n"], nm))
    pl23_side(sh, x_side + PL23_SIDE_GAP, W, H, used, ents, nis, warn)
    sh.crop = (0.0, 0.0, W, H)
    sh.key, sh.world, sh.scale, sh.pleg = "plan", bbox(C.V.P), scale, None
    sh.bid = ("mp_plan", "c1_s1", u"Masterplan: the ecological corridor of the whole {}".format(R28_FRAME_NAME.lower()))
    sh.plan_sources = pl28_plan_sources(ents, nis)
    C.ni_placed = sum(1 for r_ in C.nogo if r_.get("placed"))
    return sh
# p.24 the detail window panel: v28 (revision 29 Oct, WO-T4b-3) plan language + sections D1, D2 (split from parts/02_Design.py, parts/02b_detail.py, parts/02e_r28_detail.py, parts/03_make_board.py on 29 Oct 2026; moved unchanged)


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


def north_arrow(pg, x, y, h=7.0):
    """v21: north arrow (survey grid +Y) with its tip at (x, y), page mm; 'N' beside it."""
    pg.poly([[(x, y), (x - 1.8, y - h), (x, y - h * 0.72)]], fill=COL["ink_dark"])
    pg.poly([[(x, y), (x, y - h * 0.72), (x + 1.8, y - h)]], fill=COL["white"], stroke=COL["ink_dark"], lw=0.15)
    pg.text(u"N", x + 2.6, y - 3.2, 2.6, COL["ink_dark"], bold=True)


def panel_marks(sh, x, y, scale, marks):
    """v21: north arrow and scale bar in a panel's bottom margin (x, y = its left end, page mm)."""
    north_arrow(sh, x + 2.0, y + 8.0)
    scale_bar(sh, x + 12.0, y + 1.0, scale, marks)


def store_m3(z):
    """(rough volume m3, words) of a water-route zone, or None: reed basins area x 0.46 m; retention terraces area x
    the Q100 depth over them at the nearest channel cut."""
    if z["code"] in STORE_DEPTH:
        return z["m2"] * STORE_DEPTH[z["code"]], u""
    if z["code"] == "WS" and z.get("P"):
        cx = sum(p[0] for p in z["P"]) / len(z["P"])
        cy = sum(p[1] for p in z["P"]) / len(z["P"])
        num, nm, c, span, bed, q100, q500 = min(CUT_AT, key=lambda r: (r[2][0] - cx) ** 2 + (r[2][1] - cy) ** 2)
        return z["m2"] * max(0.0, q100[0] - (bed + TERRACE_UP)), u" in Q100"
    return None


def _r28_base(pg, C, T, R, segs):
    """v27 (P24.1, P24.2): the survey as a faint grey underlay: the bed, contours, stream lines, buildings (heritage
    with a thin outline), street edges; the bridges crisp (the base's only dark lines, kept free of words)."""
    cl = _r28_base_cols()
    Rm = (R[0] - 5.0, R[1] - 5.0, R[2] + 5.0, R[3] + 5.0)
    near = lambda Ls: [[T(p) for p in L_] for L_ in Ls if len(L_) >= 2 and hit(bbox(L_), Rm)]
    Ps = near(C.bed_loops)
    if Ps:
        pg.poly(Ps, fill=cl["bed"])
        leg(("r28dt", "bed"))
    for Q in near(C.contours):
        pg.line(Q, COL["contour10"], 0.12)
        leg(("r28dt", "contour"))
    for Q in near(C.streams):
        pg.line(Q, COL["river_mid"], 0.12, alpha=0.5)
    for role in ("building", "housing", "shed"):
        Ps = near(C.bld.get(role, []))
        if Ps:
            pg.poly(Ps, fill=cl["bld"])
            leg(("r28dt", "bld"))
    Ps = near(C.bld.get("heritage", []))
    if Ps:
        pg.poly(Ps, fill=cl["bld"], stroke=COL["her_edge"], lw=0.15)
        leg(("r28dt", "her"))
    Ps = near(C.built_since)
    if Ps:
        pg.poly(Ps, fill=cl["bld"], stripes=(COL["ink2"], 0.8, 0.12, 45.0))
        leg(("r28dt", "since"))
    for Q in near(C.roads):
        pg.line(Q, COL["ink2"], 0.15, alpha=0.4)
        leg(("r28dt", "street"))
    for Q in near(C.bridges):
        pg.line(Q, COL["ink"], 0.4)
        segs += list(zip(Q, Q[1:]))
        leg(("r28dt", "bridge"))


def _r28_wh(lines):
    """lines [(text, size, bold, colour)] -> (w, h), mm"""
    return max(text_w(s, sz, bd) for s, sz, bd, _ in lines), sum(sz * 1.18 for s, sz, bd, _ in lines)


def _r28_text(pg, lines, b, centre=False):
    y = b[3]
    for s, sz, bd, col in lines:
        y -= sz
        if centre:
            pg.text(s, (b[0] + b[2]) / 2.0, y, sz, col, bold=bd, align="C")
        else:
            pg.text(s, b[0], y, sz, col, bold=bd)
        y -= sz * 0.18


def _r28_free(b, taken, segs, bounds, pad):
    if not (bounds[0] <= b[0] and b[2] <= bounds[2] and bounds[1] <= b[1] and b[3] <= bounds[3]):
        return False
    return not any(lp_hit(b, t, pad) for t in taken) and not any(_lp_seg_box(p, q, b) for p, q in segs)


def _r28_spot(w, h, anchor, taken, segs, bounds, rank=0):
    """G4 (common/label_place): a free w x h box by anchor, (box, leader) or None; rank 0 always finds one."""
    got = place_labels_all([{"x": anchor[0], "y": anchor[1], "wh": lambda f: (w, h), "rank": rank}], taken, bounds,
                           segs, sizes=(1.0,), pad=0.5)
    return got[0][:2] if 0 in got else None


def _r28_label(pg, lines, anchor, taken, segs, bounds, rank=0, leader=True):
    """A word block beside its anchor, on a thin leader when it had to move off; its box or None (dropped)."""
    w, h = _r28_wh(lines)
    got = _r28_spot(w, h, anchor, taken, segs, bounds, rank)
    if got is None:
        return None
    b, far = got
    _r28_text(pg, lines, b)
    if far and leader:
        pg.line([anchor, lp_leader_end(b, anchor)], COL["ink2"], 0.15)
    return b


def _r28_title(pg, ring_, variants, taken, segs, bounds):
    """v27 (P24.1, P24.2): a field's title block, centred on the first free spot inside the field (its pole first),
    else beside the pole on a leader; the variants are tried in order (with the grey line, then without)."""
    spots = inside_spots(ring_, 12)
    for lines in variants:
        w, h = _r28_wh(lines)
        for x, y in spots:
            b = (x - w / 2.0, y - h / 2.0, x + w / 2.0, y + h / 2.0)
            if _r28_free(b, taken, segs, bounds, 0.6):
                _r28_text(pg, lines, b, True)
                taken.append(b)
                return b
    for lines in variants:
        b = _r28_label(pg, lines, spots[0], taken, segs, bounds, rank=0 if lines is variants[-1] else 1)
        if b:
            return b
    return None


def _r28_route_runs(order, L, a, b):
    """v27 (P24.2, G5): one water route step as text runs [(text, bold)]: the move, the zone in bold, its area and
    rough volume (v22-v26's figures and wording, sentence case)."""
    if order < len(ROUTE):
        words, end = ROUTE[order][1].capitalize(), ROUTE[order][2]   # "Into {}", "Back to the stream"
        z = (a, b)[end] if end is not None else None
        if z is None:
            w0, _, rest = words.partition(u" ")
            return [(w0, True), (u" " + rest, False)]
        nm = name_of(z, z.get("own", ""))
        nm = ROUTE_SHORT.get(nm, nm).lower()
        pre, _, post = words.partition(u"{}")
        runs = [(pre + u"the ", False), (nm, True)] + ([(post, False)] if post else [])
        runs.append((u" · " + u_area(z["m2"]), False))
        sv = store_m3(z)                                 # v22: rough volume, area x depth
        if sv:
            runs.append((u" · ~" + u_volume(round(sv[0], -1)) + sv[1], False))
            leg(("dt", "vol"))
        return runs
    t_ = (L["label"] or u"water").lower().replace(u"river", u"stream").capitalize()
    head, _, last = t_.rpartition(u" ")
    return [(head + u" ", False), (last, True)] if head else [(t_, True)]


# ================================================================ v28 (revision 29 Oct, WO-T4b-3): plan language and sections
# Package H "Page 24". The plan: an architectural plan language (R15 idea, not its style), every element with its own
# symbol and texture, at true size from the masterplan's own design: lined reed cells (plants module), terrace edges
# with ticks, Demeter's Garden as an olive orchard at its sourced 7 x 5 m spacing, paved hub squares with their
# planes, forest crowns at their true crown width, the riverside walk with its bike lane, stepping stones, footbridge
# decks, the changed roads by their change, the wetland of the widened stream; no round vignettes. Under each plan its
# section at the same 1:1,000: D1 on the W1 line, D2 on the W3 line (the cut lines may repeat, D11; p.13 draws them
# at 1:500 within the banks looking downstream, these run across the whole window looking upstream, with the zones
# from the water to the edge). The section's channel comes from the level table (common/levels.py: bed, bed width,
# wall and bank tops, Q100, Q500), the land beyond the banks from the survey's heights (spot heights near the line,
# the contours it crosses); along it every proposal the plan draws where the cut crosses it, paler where it stands
# beyond the cut in the view direction; a vertical line names each zone (R18 idea); banks, materials, roots and
# people from section_parts, plants and figures (R16, R17 idea).
P24_CUTS = {"dt_upstream": ("W1", u"D1"), "dt_k5": ("W3", u"D2")}
P24_HALF_M = 97.0            # the section reaches this far either side of the stream axis, m (half the window width)
P24_WALL_T = 0.60            # DSİ wall thickness, m: no sourced value; the 0.60 m of p.04-05 and p.13 (G2)
P24_RAIL_H = 1.10            # railing on a wall top, m: drawing value (as p.13)
P24_KERB_H = 0.15            # reed cell kerb above the ground, m: drawing value (as p.13)
P24_BASIN = (5.0, 1.5, 0.90, 0.50, 0.65)   # reed cell: length, gap, floor under the rim, media, water over the floor,
#                              m: drawing values (p.13's middle basin)
P24_FREEBOARD = 0.30         # a dry proposed floor sits this far above Q500, rounded up to 5 cm (p.13's rule)
P24_WALL_DG = 0.40           # Demeter's Garden's stone edge wall, m thick (as p.13)
P24_PAVE_T = 0.25            # paving of hub squares and streets in section, m (drawing value, as p.13)
P24_SPOT_M = 5.0             # survey spot heights this far from the cut line make its ground, m
P24_BEYOND_M = 150.0         # proposals this far beyond the cut, in the view direction, show paler in the section, m
P24_BELOW_M = 3.0            # cut ground drawn this far under the lowest point, m
P24_STEP_M = 0.5             # the section's sampling step, m
P24_MIN_RUN = 4.0            # zone runs shorter than this get no zone line, m
P24_TREE_M = 6.0             # forest and street trees this far from the cut line stand in the section, m
P24_BIKE = True              # the riverside walk carries a bike lane (Aras 29 Oct 21:04, decision card)
P24_BIKE_W = 2.0             # bike lane beside the walk in plan, m: drawing value
P24_STONE = (0.40, 1.20)     # stepping stone radius and spacing, m: drawing values
P24_LAB_ROWS = 4             # rows of zone names above a section
P24_SEC_MAX = 222.0          # mm: a crop (plan + section) taller than this does not fit the booklet page with its legend
P24_FLOOD, P24_FLOOD_A = "C1D3DB", 0.55   # the reach of Q500 in section (as p.13)
P24_BIKE_COL = "A9673F"      # the bike lane (palette centre family, darker)
P24_KEY = {("WT", None): "reed", ("WD", None): "spill", ("WS", None): "terraces", ("DG", None): "demeter",
           ("GR", None): "forest", ("WA", "F"): "wetland", ("WP", None): "wetland", ("WA", "W"): "subhub"}
P24_NAME = {"reed": u"REED BASINS, LINED", "spill": u"SPILLWAY", "terraces": u"RAIN TERRACES",
            "demeter": u"DEMETER'S GARDEN", "forest": u"FOREST CORRIDOR", "trees": u"TREE-PLANTED AREA",
            "wetland": u"WIDENED STREAM · WETLAND", "subhub": u"SUB-HUB IN THE BED", "hub": u"HUB SQUARE",
            "walk": u"WALK + BIKE LANE" if P24_BIKE else u"RIVERSIDE WALK", "street": u"STREET", "bld": u"BUILDING",
            "bed": u"SELINOS", "foot": u"FOOTBRIDGE", "stones": u"STEPPING STONES", "view": u"VIEWING TERRACE"}
# species named under a plan field's title (plants module names, "English (Turkish)"; D2: reed only in lined cells,
# D6: no iris, oleander, white poplar; water mint left out of the open ground)
P24_SPECIES = {"reed": ("reed",), "terraces": ("lavender",), "hub": ("plane",), "demeter": ("olive", "lavender"),
               "wetland": ("willow", "tamarisk", "loosestrife"), "forest": ("ash", "plane")}


def _p24_put(pg, shapes, alpha=None):
    """house shapes ("poly", ring(s), fill, stroke, lw) / ("line", pts, colour, lw) of the shared modules -> pg"""
    for s in shapes:
        if not s or len(s) < 3 or not s[1]:
            continue
        if s[0] == "poly":
            r = s[1]
            rings = r if isinstance(r[0][0], (list, tuple)) else [r]
            pg.poly(rings, fill=s[2], stroke=s[3] if len(s) > 3 else None,
                    lw=(s[4] if len(s) > 4 and s[4] else 0.1), alpha=alpha)
        elif s[0] == "line":
            pg.line(s[1], s[2], s[3] if len(s) > 3 and s[3] else 0.1, alpha=alpha)


def _p24_top(shapes):
    """the highest page y of house shapes (or None)"""
    ys = []
    for s in shapes:
        if s and len(s) >= 2 and s[1]:
            r = s[1]
            rings = r if isinstance(r[0][0], (list, tuple)) else [r]
            ys += [p[1] for R in rings for p in R]
    return max(ys) if ys else None


def _p24_sp(key):
    """a species' printed name, 'English (Turkish)', English alone where the Turkish name is unverified"""
    sp = PLA_SPECIES[key]
    tr = sp.get("turkish") or u""
    return sp["name"] if (not tr or u"UNVERIFIED" in tr) else u"{} ({})".format(sp["name"], tr)


def _p24_cross(c0, cd, p, q):
    """t (m along c0 + t * cd) where segment p-q crosses that line, or None"""
    sx, sy = q[0] - p[0], q[1] - p[1]
    den = cd[0] * sy - cd[1] * sx
    if abs(den) < 1e-12:
        return None
    wx, wy = p[0] - c0[0], p[1] - c0[1]
    s = (wx * cd[1] - wy * cd[0]) / den
    return (wx * sy - wy * sx) / den if -1e-9 <= s <= 1.0 + 1e-9 else None


def _p24_crossings(c0, cd, P, ta, tb):
    """every t in ta..tb where polyline P crosses the cut line"""
    out = []
    for p, q in zip(P, P[1:]):
        t = _p24_cross(c0, cd, p, q)
        if t is not None and ta <= t <= tb:
            out.append(t)
    return out


def _p24_tz(c0, cd, f, p):
    """(t along the cut, depth in the view direction f) of a survey point"""
    dx, dy = p[0] - c0[0], p[1] - c0[1]
    return dx * cd[0] + dy * cd[1], dx * f[0] + dy * f[1]


def _p24_zat(prof, t):
    """the profile's height at t (on a vertical step: the value of the first segment that holds t)"""
    if t <= prof[0][0]:
        return prof[0][1]
    for (t0, z0), (t1, z1) in zip(prof, prof[1:]):
        if t1 > t0 and t0 <= t <= t1:
            return z0 + (z1 - z0) * (t - t0) / (t1 - t0)
    return prof[-1][1]


def p24_ground(C, c0, cd, ta, tb):
    """[(t, z)] survey heights along the cut c0 + t * cd: spot heights (NOKTA_TAKEOMETRI) within P24_SPOT_M of the
    line, and the survey contours it crosses at their own height (the shared basemap's contours when the survey's
    lie flat); points closer than 1 m along the cut are averaged."""
    nx_, ny_ = -cd[1], cd[0]
    pts = []
    for x, y, z in C.spots:
        dx, dy = x - c0[0], y - c0[1]
        t = dx * cd[0] + dy * cd[1]
        if ta - 5.0 <= t <= tb + 5.0 and abs(dx * nx_ + dy * ny_) <= P24_SPOT_M:
            pts.append((t, z))
    cz = [(P, z) for P, z in getattr(C, "contour_z", []) if abs(z) > 1.0]
    if not cz:
        cz = [(P, z) for major, z, P in ((basemap_load() or {}).get("contours") or []) if z is not None]
    for P, z in cz:
        pts += [(t, z) for t in _p24_crossings(c0, cd, P, ta - 5.0, tb + 5.0)]
    pts.sort()
    out = []
    for t, z in pts:
        if out and t - out[-1][2] < 1.0:
            g = out[-1]
            g[0].append(t)
            g[1].append(z)
        else:
            out.append([[t], [z], t])
    return [(sum(a) / len(a), sum(b) / len(b)) for a, b, _ in out]


def p24_profile(C, cid, c0, cd, ta, tb, warn):
    """the cut line's ground today, left (SW, t < 0) to right (NE), as [[t, z]]: the bed at its level and width;
    DSİ walls at the level table's top with the land behind them at the wall top for 2 m; the other banks and all land
    beyond from the survey heights (p24_ground); flat at the bank top where the survey has none (logged)."""
    bed, hw = level(cid, "bed"), level(cid, "bed_width_cm") / 200.0
    sv = p24_ground(C, c0, cd, ta, tb)
    land, kinds, tops = {}, {}, {}
    for side, sg in (("SW", -1.0), ("NE", 1.0)):
        kinds[side] = (level_cut(cid).get(side) or {}).get("type")
        tops[side] = level(cid, "top", side)
        if kinds[side] == "dsi_wall":
            e = hw + P24_WALL_T + 2.0
            pts = [(sg * e, tops[side])] + [(t, z) for t, z in sv if sg * t > e]
        else:
            pts = [(sg * hw, bed)] + [(t, z) for t, z in sv if sg * t > hw + 1.0]
        if len(pts) == 1:
            pts.append((sg * (hw + 4.0), tops[side] if tops[side] is not None else bed))
            warn.append(u"section {}: no survey heights on the {} side: its land is drawn flat".format(cid, side))
        land[side] = sorted(pts)
    n = int((tb - ta) / P24_STEP_M)
    ts = [ta + i * P24_STEP_M for i in range(n + 1)] + [tb]
    prof = [[t, _p24_zat(land["SW"], t) if kinds["SW"] != "dsi_wall" or t < -(hw + P24_WALL_T + 2.0)
             else tops["SW"]] for t in ts if t < -hw]
    prof += [[-hw, tops["SW"]], [-hw, bed]] if kinds["SW"] == "dsi_wall" else [[-hw, bed]]
    prof += [[hw, bed], [hw, tops["NE"]]] if kinds["NE"] == "dsi_wall" else [[hw, bed]]
    prof += [[t, _p24_zat(land["NE"], t) if kinds["NE"] != "dsi_wall" or t > hw + P24_WALL_T + 2.0
              else tops["NE"]] for t in ts if t > hw]
    return prof, kinds, tops


def p24_zone(C, p):
    """what the masterplan puts at survey point p (a P24_NAME key) or None: its zones first, then the widened stream,
    the hub squares, buildings and roads of the survey grid"""
    for z in C.D.zones:
        k_ = P24_KEY.get((z["code"], z.get("tier") if z["code"] == "WA" else None))
        if k_ and pip(p[0], p[1], z["P"]):
            return k_
    if any(pip(p[0], p[1], w["ring"]) for w in C.widen):
        return "wetland"
    for h in C.hubs:
        if any(len(L_) >= 3 and pip(p[0], p[1], L_) for L_ in h.get("square") or []):
            return "hub"
    n = C.cell(p)
    if n is not None and C.F[n] in (1, 2):
        return "bld" if C.F[n] == 1 else "street"
    return None


def p24_runs(C, c0, cd, ta, tb, hw):
    """[[key, t0, t1]] the zones along the cut (bed = the bed width), from P24_STEP_M samples"""
    runs = []
    t = ta
    while t < tb:
        tm = min(tb, t + P24_STEP_M)
        u = (t + tm) / 2.0
        key = "bed" if abs(u) <= hw else p24_zone(C, (c0[0] + cd[0] * u, c0[1] + cd[1] * u))
        if key == "subhub" and abs(u) > hw:
            key = "wetland"
        if runs and runs[-1][0] == key:
            runs[-1][2] = tm
        else:
            runs.append([key, t, tm])
        t = tm
    return [r_ for r_ in runs if r_[0] is not None]


def _p24_set(prof, t0, t1, fn, hw):
    """z = fn(t, z) for the profile points in t0..t1 outside the bed (the bed and its wall faces, |t| <= hw, keep
    theirs)"""
    for p in prof:
        if t0 <= p[0] <= t1 and abs(p[0]) > hw + 1e-6:
            p[1] = fn(p[0], p[1])


def _p24_cut_in(prof, a, b, pts):
    """the profile with the points between a and b replaced by pts (left to right)"""
    return [p for p in prof if p[0] < a] + [list(q) for q in pts] + [p for p in prof if p[0] > b]


class P24Sec(object):
    """One section in print mm at 1:1,000 (k = 1 mm per m): x = (t - ta) k, y = (z - z0) k."""

    def __init__(self, ta, tb, z0):
        self.ta, self.tb, self.z0, self.k = ta, tb, z0, 1000.0 / DT_SCALE
        self.w = (tb - ta) * self.k
        self.pg = Page(self.w, 0.0)
        self.shapes = []                                 # what the plants and figures added (for the top)
        self.zl = []                                     # zone lines: (name, t, z of the ground, beyond)
        self.lv = []                                     # level words: (text, t, z)

    def X(self, t):
        return (t - self.ta) * self.k

    def Y(self, z):
        return (z - self.z0) * self.k

    def put(self, shapes, alpha=None):
        _p24_put(self.pg, shapes, alpha)
        self.shapes += shapes

    def plant(self, key, t, z, beyond=False, seed=0, **kw):
        self.put(pla_section(key, self.X(t), self.Y(z), self.k, beyond=beyond, seed=seed, **kw))

    def fig(self, pose, t, z, facing=1, **kw):
        self.put(fig_side(pose, self.X(t), self.Y(z), self.k, facing=facing, mm_per_m=self.k, **kw))

    def block(self, t0, t1, z0, z1, material):
        a, b = sorted((t0, t1))
        self.put(sct_hatch_fill([(self.X(a), self.Y(z0)), (self.X(b), self.Y(z0)), (self.X(b), self.Y(z1)),
                                 (self.X(a), self.Y(z1))], material, self.k, SCT["cut"], 0.2))


def p24_section(C, w, warn):
    """v28 (WO-T4b-3): the section under window w (P24_CUTS), as (Page, w mm, h mm, legend keys, words not placed);
    None when the window has no cut. Looks upstream: the SW bank on the left, as the plan reads it."""
    cid, name = P24_CUTS.get(w["id"], (None, None))
    if not cid:
        return None
    R = w["R"]
    E = level_ends(cid)
    c0 = CUT_AT[{"W1": 0, "W3": 2}[cid]][2]
    L = math.hypot(E[1][0] - E[0][0], E[1][1] - E[0][1]) or 1.0
    cd = ((E[1][0] - E[0][0]) / L, (E[1][1] - E[0][1]) / L)            # SW end -> NE end
    if level_end_labels(cid)[0] != u"SW":
        cd = (-cd[0], -cd[1])
    f = (-cd[1], cd[0])                                                # the view: the SW end on its left
    tin = [-P24_HALF_M, P24_HALF_M]
    for ax, lo, hi in ((0, R[0], R[2]), (1, R[1], R[3])):             # the cut line inside the window
        if abs(cd[ax]) > 1e-9:
            ts_ = sorted(((lo - c0[ax]) / cd[ax], (hi - c0[ax]) / cd[ax]))
            tin = [max(tin[0], ts_[0]), min(tin[1], ts_[1])]
    ta, tb = tin
    bed, hw = level(cid, "bed"), level(cid, "bed_width_cm") / 200.0
    q100, q500 = level(cid, "q100"), level(cid, "q500")
    if tb - ta < 2 * hw + 10.0:
        warn.append(u"section {}: the cut line has only {:.0f} m inside the window: not drawn".format(name, tb - ta))
        return None
    prof, kinds, tops = p24_profile(C, cid, c0, cd, ta, tb, warn)
    runs = p24_runs(C, c0, cd, ta, tb, hw)
    keys = set()
    # ---- the proposal in the ground: wetland benches (the bank cut back), the garden raised above Q500, hub squares
    # and streets flat, reed cells under one rim, terraces at the plan's terrace edges, the walk flat
    bench = bed + TERRACE_UP
    gf = math.ceil((q500 + P24_FREEBOARD) * 20.0) / 20.0
    gone = set()
    for key, t0, t1 in runs:
        if key == "wetland":
            _p24_set(prof, t0, t1, lambda t, z: min(z, bench), hw)
            for side, sg in (("SW", -1.0), ("NE", 1.0)):
                if kinds[side] == "dsi_wall" and min(abs(t0 - sg * hw), abs(t1 - sg * hw)) <= P24_WALL_T + 2.5:
                    gone.add(side)
        elif key == "demeter":
            _p24_set(prof, t0, t1, lambda t, z: max(z, gf), hw)
        elif key in ("hub", "street", "reed"):
            zs = [p[1] for p in prof if t0 <= p[0] <= t1 and abs(p[0]) > hw]
            if zs:
                zf = min(zs) if key == "reed" else sum(zs) / len(zs)
                _p24_set(prof, t0, t1, lambda t, z, zf=zf: zf, hw)
    for side in gone:                                     # the DSİ wall gives way to the wetland's soft toe
        sg = -1.0 if side == "SW" else 1.0
        prof = [p for p in prof if not (abs(p[0] - sg * hw) < 1e-6 and abs(p[1] - tops[side]) < 1e-6)]
        _p24_set(prof, min(sg * hw, sg * (hw + 2.0)), max(sg * hw, sg * (hw + 2.0)),
                 lambda t, z: bed + (bench - bed) * min(1.0, (abs(t) - hw) / 2.0), hw)
    terr = []
    for P in C.terr:                                      # the plan's terrace edges: a bench 4 m uphill of each
        for t in _p24_crossings(c0, cd, P, ta + 4.0, tb - 4.0):
            if abs(t) <= hw + 2.0:
                continue
            z0_ = _p24_zat(prof, t)
            sg = 1.0 if _p24_zat(prof, t + 3.0) > _p24_zat(prof, t - 3.0) else -1.0
            te = t + sg * R28DT_TERR_M
            zt = _p24_zat(prof, te)
            _p24_set(prof, min(t, te), max(t, te), lambda t_, z, z0_=z0_: z0_, hw)
            terr.append((t, te, z0_, zt, sg))
    walks = []
    for P in C.canopy:
        for t in _p24_crossings(c0, cd, P, ta + 2.0, tb - 2.0):
            if abs(t) > hw + 1.0:
                zw = _p24_zat(prof, t)
                _p24_set(prof, t - WALK_W / 2.0, t + WALK_W / 2.0, lambda t_, z, zw=zw: zw, hw)
                walks.append((t, zw))
    cells = []
    kt = 0.15
    ln, gap, dep, media, wl = P24_BASIN
    for key, t0, t1 in runs:
        if key != "reed":
            continue
        a = t0 + 1.0
        while a + ln <= t1 - 1.0:
            rim = _p24_zat(prof, a)
            prof = _p24_cut_in(prof, a - kt, a + ln + kt, [(a - kt, rim), (a - kt, rim - dep - kt),
                                                          (a + ln + kt, rim - dep - kt), (a + ln + kt, rim)])
            cells.append((a, a + ln, rim))
            a += ln + gap
    z0 = min([p[1] for p in prof] + [bed]) - P24_BELOW_M
    S = P24Sec(ta, tb, z0)
    X, Y, k = S.X, S.Y, S.k
    # ---- the reach of Q500 (wash) where it joins the stream, the Q100 and Q500 lines over it
    lo_, hi_ = 0.0, 0.0
    while lo_ > ta and _p24_zat(prof, lo_ - P24_STEP_M) < q500:
        lo_ -= P24_STEP_M
    while hi_ < tb and _p24_zat(prof, hi_ + P24_STEP_M) < q500:
        hi_ += P24_STEP_M
    if hi_ > lo_:
        n_ = int((hi_ - lo_) / P24_STEP_M)
        ring_ = [(X(lo_), Y(q500))] + [(X(lo_ + i * P24_STEP_M), Y(_p24_zat(prof, lo_ + i * P24_STEP_M)))
                                       for i in range(n_ + 1)] + [(X(hi_), Y(q500))]
        S.pg.poly([ring_], fill=P24_FLOOD, alpha=P24_FLOOD_A)
        for lv_, dash in ((q100, [1.2, 0.6]), (q500, [0.4, 0.4])):
            S.pg.line([(X(lo_), Y(lv_)), (X(hi_), Y(lv_))], COL["river_dark"], 0.2, dash, cap=0)
        S.lv.append((u"Q100 {} · Q500 {}".format(u_level(q100), u_level(q500)), hi_, q500))
        keys.add("flood")
    # ---- the cut ground, the bed, the walls kept (railings) or given way (today's wall dashed)
    S.put(sct_ground([(X(p[0]), Y(p[1])) for p in prof], 0.0, k))
    S.put(sct_bed(X(-hw), X(hw), Y(bed), k, depth_m=1.0))
    S.lv.append((u"bed " + u_level(bed), 0.0, bed))
    for side, sg in (("SW", -1.0), ("NE", 1.0)):
        if kinds[side] != "dsi_wall":                     # an earth bank: the survey draws it (its crest has no
            continue                                      # place on the cut in the level table, so no level word)
        a, b = sg * hw, sg * (hw + P24_WALL_T)
        ring_ = [(X(a), Y(bed)), (X(b), Y(bed)), (X(b), Y(tops[side])), (X(a), Y(tops[side]))]
        if side in gone:
            S.pg.poly([ring_], stroke=COL["ink2"], lw=0.15, dash=[0.8, 0.5])
            continue
        S.put(sct_hatch_fill(ring_, "stone", k, SCT["cut"], 0.3))
        S.put(sct_bank("railing", X((a + b) / 2.0), Y(tops[side]), Y(bed), -sg, k, h_m=P24_RAIL_H)[0])
        S.lv.append((u_level(tops[side]), b, tops[side] + P24_RAIL_H))
        keys.add("wall")
    # ---- what each zone holds: planting, paving, cells, the garden, people placed by what they do there
    near = lambda pts, d: [(t, i) for i, p in enumerate(pts) for t, dd in [_p24_tz(c0, cd, f, p)]
                           if ta + 2.0 <= t <= tb - 2.0 and abs(dd) <= d and abs(t) > hw + 1.0]
    for t, i in near(C.forest, P24_TREE_M):
        S.plant("ash" if i % 2 else "plane", t, _p24_zat(prof, t), seed=i)
        keys.add("forest")
    for t, i in near(C.trees, P24_TREE_M):
        S.plant("plane" if i % 2 else "ash", t, _p24_zat(prof, t), seed=50 + i)
        keys.add("forest")
    railed = False
    for side, sg in (("SW", -1.0), ("NE", 1.0)):         # one figure at a railing, looking into the channel
        if kinds[side] == "dsi_wall" and side not in gone and not railed:
            fc = 1 if sg < 0 else -1
            m_ = fig_meta("railing", facing=fc, rail_h=P24_RAIL_H)
            S.fig("railing", sg * (hw + P24_WALL_T / 2.0) - m_.get("rail_x", 0.0), tops[side], facing=fc,
                  rail_h=P24_RAIL_H)
            railed = True
    for key, t0, t1 in runs:
        ln_, tm = t1 - t0, (t0 + t1) / 2.0
        fc = 1 if tm < 0 else -1                          # people face the stream
        if key == "hub":
            zf = _p24_zat(prof, tm)
            S.block(t0, t1, zf - P24_PAVE_T, zf, "stone")
            hub_t = [t for h in C.hubs for t, i in near(h.get("trees") or [], P24_TREE_M)]
            for j, t in enumerate(hub_t or [tm]):
                S.plant("plane", t, zf, seed=70 + j)
            S.fig("sit_chair", tm - 2.0, zf, facing=fc)
            S.fig("stand", tm + 2.5, zf, facing=-fc)
            S.lv.append((u_level(zf), tm, zf))
        elif key == "street":
            zf = _p24_zat(prof, tm)
            S.block(t0, t1, zf - P24_PAVE_T, zf, "concrete")
            if ln_ >= 6.0:
                S.fig("walk", tm, zf, facing=fc)
        elif key == "demeter":
            ts_ = sorted((t0, t1), key=abs)
            te = ts_[0]                                   # the garden's stream-side edge: a stone wall
            sg = 1.0 if te > tm else -1.0
            S.block(te, te - sg * P24_WALL_DG, gf - 1.0, gf + 0.15, "stone")
            x0_, x1_ = X(min(t0, t1) + 1.5), X(max(t0, t1) - 1.5)
            if x1_ > x0_:
                S.put(pla_crop_rows("olive", x0_, x1_, Y(gf), k))
                n_ = int((x1_ - x0_) / (PLA_CROPS["olive"]["row_m"] * k) + 1e-9)
                t_o = min(t0, t1) + 1.5 + ((x1_ - x0_) - n_ * PLA_CROPS["olive"]["row_m"] * k) / 2.0 / k
                S.fig("olive", t_o + 1.3, gf, facing=-1)
            S.plant("lavender", te - sg * 1.2, gf, seed=81)
            S.lv.append((u_level(gf), tm, gf))
        elif key == "wetland" and abs(tm) > hw:
            z_ = lambda t: _p24_zat(prof, t)
            if ln_ >= 12.0:
                S.plant("willow", tm, z_(tm), seed=90)
            if ln_ >= 20.0:
                S.plant("tamarisk", t0 + ln_ / 4.0, z_(t0 + ln_ / 4.0), seed=91)
                S.plant("tamarisk", t1 - ln_ / 4.0, z_(t1 - ln_ / 4.0), seed=92)
            te = min((t0, t1), key=abs)
            sg = 1.0 if tm > 0 else -1.0
            for j in range(int(min(6.0, ln_ - 1.0) / 1.5)):
                t = te + sg * (0.75 + j * 1.5)
                S.plant("loosestrife" if j % 2 else "soft_rush", t, z_(t), seed=95 + j)
            if ln_ >= 8.0:
                S.fig("watch", te + sg * 3.0, z_(te + sg * 3.0), facing=-1 if sg > 0 else 1)
        elif key == "terraces":
            t = t0 + 1.25
            j = 0
            while t < t1 - 1.0:
                S.plant("lavender", t, _p24_zat(prof, t), seed=100 + j)
                t += 2.5
                j += 1
            if ln_ >= 8.0:
                S.fig("walk", tm, _p24_zat(prof, tm), facing=fc)
        elif key == "bld":
            zf = _p24_zat(prof, tm)
            S.pg.line([(X(t0), Y(zf) + 0.4), (X(t1), Y(zf) + 0.4)], COL["bld"], 0.8, cap=0)
    for a, b, rim in cells:                               # the lined reed cells (D2 a), above Q500 by their rim
        fl = rim - P24_BASIN[2]
        S.put(pla_reed_basin(X(a), X(b), Y(fl), Y(rim), k, P24_KERB_H, media_m=P24_BASIN[3],
                             wl_y=Y(fl + P24_BASIN[4])))
        keys.add("reed")
    if cells:
        a, b, rim = cells[0]
        S.fig("touch", a - 0.7, rim, facing=1)            # the clean-water classroom: a hand into the cell
        S.lv.append((u_level(cells[0][2]), (cells[0][0] + cells[-1][1]) / 2.0, cells[0][2]))
    for t, te, z0_, zt, sg in terr:                       # each terrace's riser, where the old ground stood higher
        if zt > z0_ + 0.05:
            S.block(te, te + sg * 0.15, z0_ - 0.3, zt, "concrete")
        keys.add("terraces")
    for j, (t, zw) in enumerate(walks):                   # the riverside walk, its bike lane
        S.fig("walk", t - 0.6, zw, facing=1 if j % 2 else -1)
        if P24_BIKE:
            S.fig("bike", t + 0.4, zw, facing=-1 if j % 2 else 1)
        S.zl.append((P24_NAME["walk"], t, zw, False))
        keys.add("walk")
    # ---- zone lines: one per run (bed = the stream), then what stands beyond the cut, paler
    for key, t0, t1 in runs:
        if key in P24_NAME and (t1 - t0 >= P24_MIN_RUN or key == "bed") and key != "walk":
            tm = (t0 + t1) / 2.0
            S.zl.append((P24_NAME[key], tm, _p24_zat(prof, tm), False))
    crossed = set(r_[0] for r_ in runs)
    seen = set()
    for z in C.D.zones:
        key = P24_KEY.get((z["code"], z.get("tier") if z["code"] == "WA" else None))
        if not key or key in crossed or key in seen or not z.get("P"):
            continue
        q = inner_pt(z["P"])
        t, d = _p24_tz(c0, cd, f, q)
        if 0.0 < d <= P24_BEYOND_M and ta + 3.0 <= t <= tb - 3.0 and R[0] <= q[0] <= R[2] and R[1] <= q[1] <= R[3]:
            seen.add(key)
            zz = _p24_zat(prof, t)
            sp_ = {"hub": "plane", "demeter": "olive", "wetland": "willow", "forest": "ash", "terraces": "lavender"}
            if key in sp_:
                S.plant(sp_[key], t, zz, beyond=True, seed=120 + len(seen))
            S.zl.append((P24_NAME[key], t, zz, True))
    for h in C.hubs:                                      # a hub square beyond: its planes, paler
        if "hub" in crossed or "hub" in seen:
            break
        for t_, i in [(t, i) for i, p in enumerate(h.get("trees") or []) for t, d in [_p24_tz(c0, cd, f, p)]
                      if 0.0 < d <= P24_BEYOND_M and ta + 3.0 <= t <= tb - 3.0]:
            S.plant("plane", t_, _p24_zat(prof, t_), beyond=True, seed=130 + i)
            if "hub" not in seen:
                S.zl.append((P24_NAME["hub"], t_, _p24_zat(prof, t_), True))
                seen.add("hub")
    for c_ in C.cross:                                    # footbridges and stepping stones beyond
        ts_ = [_p24_tz(c0, cd, f, p) for p in c_["P"]]
        if not all(0.0 < d <= P24_BEYOND_M for _, d in ts_):
            continue
        t1_, t2_ = sorted(t for t, _ in ts_)
        if t2_ < ta or t1_ > tb:
            continue
        t1_, t2_ = max(ta, t1_), min(tb, t2_)
        if c_["kind"] == "footbridge":
            zd = max(_p24_zat(prof, t1_), _p24_zat(prof, t2_))
            S.pg.line([(X(t1_), Y(zd)), (X(t2_), Y(zd))], COL["ink2"], 0.6, cap=0, alpha=0.6)
            S.zl.append((P24_NAME["foot"], (t1_ + t2_) / 2.0, zd, True))
        elif c_["kind"] == "stepping stones":
            t = max(t1_, -hw) + P24_STONE[1] / 2.0
            while t < min(t2_, hw):
                S.pg.circle(X(t), Y(bed) + P24_STONE[0] * k, P24_STONE[0] * k, fill=COL["ink2"], alpha=0.5)
                t += P24_STONE[1]
            S.zl.append((P24_NAME["stones"], 0.0, bed, True))
    if C.terrace:
        t, d = _p24_tz(c0, cd, f, C.terrace["xy"])
        if 0.0 < d <= P24_BEYOND_M and ta + 3.0 <= t <= tb - 3.0:
            zz = _p24_zat(prof, t)
            S.pg.line([(X(t - 2.0), Y(zz + 0.3)), (X(t + 2.0), Y(zz + 0.3))], COL["ink2"], 0.5, cap=0, alpha=0.6)
            S.zl.append((P24_NAME["view"], t, zz, True))
    # ---- words: the zone lines and names in rows above everything (R18 idea), the levels by their points
    top = max([_p24_top(S.shapes) or 0.0] + [Y(p[1]) for p in prof]) + 2.0
    rows = [[] for _ in range(P24_LAB_ROWS)]
    ts_lab, missing = KEY_MIN, []
    pitch = ts_lab * 1.45
    for nm, t, zz, beyond in sorted(S.zl, key=lambda z_: z_[1]):
        s_ = nm + (u" · BEYOND" if beyond else u"")
        wd = text_w(s_, ts_lab)
        x = min(max(X(t), wd / 2.0), S.w - wd / 2.0)
        r_ = next((i for i, row in enumerate(rows) if all(x - wd / 2.0 > b + 1.0 or x + wd / 2.0 < a - 1.0
                                                         for a, b in row)), None)
        if r_ is None:
            missing.append(s_)
            continue
        rows[r_].append((x - wd / 2.0, x + wd / 2.0))
        yl = top + r_ * pitch
        col = COL["ink2"] if beyond else COL["ink_dark"]
        S.pg.line([(X(t), Y(zz) + 0.3), (X(t), yl - 0.4)], col, 0.12, [0.6, 0.4] if beyond else None, cap=0)
        S.pg.text(s_, x, yl, ts_lab, col, bold=not beyond, align="C")
    h = top + (max([i + 1 for i, row in enumerate(rows) if row] or [0]) + 0.4) * pitch
    used = [r for row in rows for r in row]
    taken = [(a, top - 0.5, b, h) for a, b in used]
    for s_, t, al in ((name, ta, "L"), (name + u"'", tb, "R")):   # the cut's names, as on the plan
        x, y = X(t) + (0.6 if al == "L" else -0.6), Y(_p24_zat(prof, t)) + 1.2
        S.pg.text(s_, x, y, 3.4, COL["ink_dark"], bold=True, align=al)
        wd = text_w(s_, 3.4, True)
        taken.append((x if al == "L" else x - wd, y - 0.3, x + wd if al == "L" else x, y + 3.4))
    for s_, t, zz in S.lv:
        wd = text_w(s_, ts_lab)
        got = label_spot(X(t), Y(zz) + 1.2, wd, ts_lab * 1.1, taken, (0.0, 0.5, S.w, top - 0.5), (), 0.3)
        if got is None:
            missing.append(s_)
            continue
        b = got[0]
        S.pg.text(s_, b[0], b[1] + ts_lab * 0.2, ts_lab, COL["ink"])
        taken.append(b)
    keys.add("section")
    return S.pg, S.w, h, keys, missing


def p24_cut_on_plan(pg, w, T, taken, segs, bounds):
    """the section's line on the plan (only this window's cut): dash-dot across the window, a triangle at each end
    pointing the way the section looks (upstream), its names at the ends (D1, D1')."""
    cid, name = P24_CUTS.get(w["id"], (None, None))
    if not cid:
        return False
    R = w["R"]
    E = level_ends(cid)
    c0 = CUT_AT[{"W1": 0, "W3": 2}[cid]][2]
    L = math.hypot(E[1][0] - E[0][0], E[1][1] - E[0][1]) or 1.0
    cd = ((E[1][0] - E[0][0]) / L, (E[1][1] - E[0][1]) / L)
    if level_end_labels(cid)[0] != u"SW":
        cd = (-cd[0], -cd[1])
    f = (-cd[1], cd[0])                                  # the view (as p24_section): the SW end on its left
    tin = [-P24_HALF_M, P24_HALF_M]
    for ax, lo, hi in ((0, R[0], R[2]), (1, R[1], R[3])):
        if abs(cd[ax]) > 1e-9:
            ts_ = sorted(((lo - c0[ax]) / cd[ax], (hi - c0[ax]) / cd[ax]))
            tin = [max(tin[0], ts_[0]), min(tin[1], ts_[1])]
    A = T((c0[0] + cd[0] * tin[0], c0[1] + cd[1] * tin[0]))
    B = T((c0[0] + cd[0] * tin[1], c0[1] + cd[1] * tin[1]))
    ink = COL["ink_dark"]
    pg.line([A, B], ink, 0.35, [2.4, 0.8, 0.4, 0.8], cap=0)
    segs.append((A, B))
    s = 2.2
    for (x, y), nm in ((A, name), (B, name + u"'")):
        tip = (x + f[0] * s, y + f[1] * s)
        pg.poly([[tip, (x - cd[0] * s * 0.55, y - cd[1] * s * 0.55), (x + cd[0] * s * 0.55, y + cd[1] * s * 0.55)]],
                fill=ink)
        taken.append((x - s, y - s, x + s, y + s))
        _r28_label(pg, [(nm, R28DT_TS["place"], True, ink)], (x - f[0] * 1.5, y - f[1] * 1.5), taken, segs, bounds)
    return True


def _p24_offset(P, d):
    """polyline P (survey m) moved d m to its left (per-vertex normals)"""
    out = []
    for i, p in enumerate(P):
        a, b = P[max(0, i - 1)], P[min(len(P) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        out.append((p[0] - dy / L * d, p[1] + dx / L * d))
    return out


def _p24_land_side(C, P):
    """+1 when the land (away from the water) lies to the left of walk P, else -1 (the corridor's distance from the
    water a few metres either side of its middle)"""
    s = arclen(P)
    (x, y), (ux, uy) = at_len(P, s, s[-1] / 2.0)
    d = []
    for sg in (1.0, -1.0):
        n = C.cell((x - uy * 4.0 * sg, y + ux * 4.0 * sg))
        d.append(C.Dst[n] if n is not None and C.Dst[n] < 1e8 else 0.0)
    return 1.0 if d[0] >= d[1] else -1.0


def p24_plan(pg, C, w, T, inP, on, k, taken, segs, dw, dh):
    """v28 (WO-T4b-3): the window's proposal in the architectural plan language, each element its own symbol and
    texture at true size; returns [(field key, page rings)] for the titles."""
    ink, ink2, white = COL["ink_dark"], COL["ink2"], COL["white"]
    TP = lambda P: [T(p) for p in P]
    fields = []
    # ---- fields: wetland (widened stream and flood terraces), terraces, spillway, sub-hub bed, forest walk
    for z in C.D.zones:
        key = P24_KEY.get((z["code"], z.get("tier") if z["code"] == "WA" else None))
        Q = TP(z["P"]) if key else None
        if not Q or not on(Q):
            continue
        if key == "wetland":
            pg.poly([Q], fill=WET_COL, alpha=0.55, stripes=(COL["river_dark"], 1.4, 0.1, 0.0, True))
        elif key == "terraces":
            pg.poly([Q], fill=R28_ZONE["terraces"][1], alpha=0.18)
        elif key == "spill":
            pg.poly([Q], fill=COL["river"], alpha=0.6, stripes=(COL["river_dark"], 0.8, 0.1, 90.0))
        elif key == "subhub":
            pg.poly([Q], fill=R28_ZONE["subhub"][1], alpha=0.25)
        elif key == "forest":
            pg.poly([Q], fill=R28_ZONE["forest"][1], alpha=0.15)
        elif key == "reed":
            _p24_put(pg, pla_cell_plan("reed", Q, k))         # lined, root-contained cells (D2 a)
        elif key == "demeter":
            _p24_put(pg, pla_crop_plan("olive", Q, k, ang_deg=principal_angle(z["P"])))   # 7 x 5 m (Kaya 2017)
        fields.append((key, Q))
        leg(("p24", key))
    for wd in C.widen:
        Q = TP(wd["ring"])
        if on(Q):
            pg.poly([Q], fill=WET_COL, alpha=0.55, stripes=(COL["river_dark"], 1.4, 0.1, 0.0, True))
            fields.append(("wetland", Q))
            leg(("p24", "wetland"))
    for a in C.arms:                                      # planted side arm (no reed in the open bed, D2 a)
        Q = TP(a["P"])
        if on(Q):
            pg.line(Q, COL["river"], max(1.0, 6.0 * k), alpha=0.8)
            pg.line(Q, COL["river_dark"], 0.15, [0.6, 0.6], cap=0)
            leg(("p24", "arm"))
    # ---- hub squares: paving grid, their planes
    for h in C.hubs:
        for L_ in h.get("square") or []:
            Q = TP(L_)
            if len(Q) >= 3 and on(Q):
                pg.poly([Q], fill=SQ_FILL, stroke=SQ_EDGE, lw=0.2)
                pg.poly([Q], stripes=(SQ_EDGE, 2.0, 0.06, 0.0), alpha=0.6)
                pg.poly([Q], stripes=(SQ_EDGE, 2.0, 0.06, 90.0), alpha=0.6)
                fields.append(("hub", Q))
                leg(("p24", "hub"))
        for i, p in enumerate(h.get("trees") or []):
            if inP(p):
                x, y = T(p)
                _p24_put(pg, pla_plan("plane", x, y, k, seed=i), alpha=0.85)
                leg(("p24", "tree"))
    # ---- terrace edges: a line with ticks down toward the stream
    for P in C.terr:
        Q = TP(P)
        if on(Q):
            ticks_line(pg, Q, R28_ZONE["terraces"][1], 0.3, 1.6, 0.8, 1.0, alpha=0.9)
            segs += list(zip(Q, Q[1:]))
            leg(("p24", "terr"))
    # ---- trees at their true crown width: the forest corridor (ash, plane), the tree-planted area (paler)
    for pts, bey, key in ((C.forest, False, "forest_tree"), (C.trees, True, "forest_tree")):
        for i, p in enumerate(pts):
            if inP(p):
                x, y = T(p)
                _p24_put(pg, pla_plan("ash" if i % 2 else "plane", x, y, k, beyond=bey, seed=i), alpha=0.8)
                leg(("p24", "tree"))
    # ---- the riverside walk with its bike lane on the land side
    for P in C.canopy:
        Q = TP(P)
        if not on(Q) or len(P) < 2:
            continue
        pg.line(Q, ink2, WALK_W * k + 0.3, cap=0)
        pg.line(Q, white, WALK_W * k, cap=0)
        segs += list(zip(Q, Q[1:]))
        leg(("p24", "walk"))
        if P24_BIKE:
            sg = _p24_land_side(C, P)
            B = TP(_p24_offset(P, sg * (WALK_W + P24_BIKE_W) / 2.0))
            pg.line(B, P24_BIKE_COL, P24_BIKE_W * k, cap=0, alpha=0.55)
            pg.line(B, white, 0.12, [1.0, 1.0], cap=0)
            s = arclen(B)
            t = min(25.0 * k, s[-1] / 2.0)
            while t < s[-1]:
                (x, y), _ = at_len(B, s, t)
                _p24_put(pg, ico_draw("bike", x, y, 2.6, ink=P24_BIKE_COL))
                taken.append((x - 1.3, y - 1.3, x + 1.3, y + 1.3))
                t += 60.0 * k
            leg(("p24", "bike"))
    # ---- crossings: stepping stones (true size), footbridge decks (the walk's width)
    for c_ in C.cross:
        A_, B_ = c_["P"][0], c_["P"][1]
        if c_["kind"] == "stepping stones" and (inP(A_) or inP(B_)):
            L = math.hypot(B_[0] - A_[0], B_[1] - A_[1]) or 1.0
            n = max(2, int(L / P24_STONE[1]))
            for i in range(n):
                fr = (i + 0.5) / n
                x, y = T((A_[0] + (B_[0] - A_[0]) * fr, A_[1] + (B_[1] - A_[1]) * fr))
                pg.circle(x, y, max(0.3, P24_STONE[0] * k), fill=ink2)
            taken += boxes_along([T(A_), T(B_)], 1.0)
            leg(("p24", "stones"))
        elif c_["kind"] == "footbridge" and (inP(A_) or inP(B_)):
            ring_ = TP(_p24_offset([A_, B_], WALK_W / 2.0)) + list(reversed(TP(_p24_offset([A_, B_], -WALK_W / 2.0))))
            pg.poly([ring_], fill=white, stroke=ink, lw=0.25)
            segs += list(zip(ring_, ring_[1:] + ring_[:1]))
            leg(("p24", "foot"))
    # ---- the roads changed: a band in the change's colour with its marking (calmed: dashes; pedestrian: dots;
    # shared: ticks)
    for rd in ROADS:
        if rd["change"] not in ("calmed", "pedestrian", "shared"):
            continue
        Q = TP(rd["xy"])
        if not on(Q):
            continue
        col = ROAD_CHANGE_COL[rd["change"]]
        pg.line(Q, col, 7.0 * k, cap=0, alpha=0.28)
        if rd["change"] == "calmed":
            pg.line(Q, col, 0.25, [1.6, 1.2], cap=0)
        elif rd["change"] == "pedestrian":
            s = arclen(Q)
            t = 0.0
            while t <= s[-1]:
                (x, y), _ = at_len(Q, s, t)
                pg.circle(x, y, 0.3, fill=col)
                t += 1.6
        else:
            ticks_line(pg, Q, col, 0.25, 2.0, 1.0, 1.0)
        leg(("p24", "road_" + rd["change"]))
    # ---- the hidden stream; the viewing terrace and its sightline; cafés
    for P in C.covered:
        Q = TP(P)
        if on(Q):
            pg.line(Q, COL["river_mid"], 1.2, [1.6, 0.9], cap=0, alpha=0.7)
            leg(("p24", "hidden"))
    if C.terrace and inP(C.terrace["xy"]):
        x, y = T(C.terrace["xy"])
        p2 = (C.terrace["xy"][0] + C.terrace["dir"][0] * 400.0, C.terrace["xy"][1] + C.terrace["dir"][1] * 400.0)
        pg.line([(x, y), T(p2)], COL["accent"], 0.3, [1.4, 0.8], cap=0, alpha=0.7)
        _p24_put(pg, ico_draw("viewpoint", x, y, 3.2))
        taken.append((x - 1.6, y - 1.6, x + 1.6, y + 1.6))
        leg(("p24", "view"))
    for z in C.D.zones:
        if z["code"] in ("GR", "DG") and inP(z["q"]):
            x, y = T(z["q"])
            _p24_put(pg, ico_draw("cafe", x, y, 3.0))
            taken.append((x - 1.5, y - 1.5, x + 1.5, y + 1.5))
            leg(("p24", "cafe"))
    return fields


def r28_window_panel(C, w, areas, missing, warn):
    """v28 (revision 29 Oct, WO-T4b-3; package H "Page 24"): a 1:1,000 window, north up: the faint survey, the
    proposal in the architectural plan language (p24_plan), the water route 1-4, the study area, the section line
    (this window's only); one title per field, place names, small words. Under it its section (p24_section, D1 or
    D2) at the same scale. One crop: the plan with its north arrow and scale bar, the section with its own."""
    R = w["R"]
    k = 1000.0 / DT_SCALE
    dw, dh = (R[2] - R[0]) * k, (R[3] - R[1]) * k
    T = lambda p: ((p[0] - R[0]) * k, (p[1] - R[1]) * k)
    inP = lambda p: R[0] <= p[0] <= R[2] and R[1] <= p[1] <= R[3]
    on = lambda Q: hit(bbox(Q), (0.0, 0.0, dw, dh))
    _PLEG[0] = {}
    pg = Page(dw, dh)
    taken, segs, ts = [], [], R28DT_TS
    ink, ink1, ink2, white = COL["ink_dark"], COL["ink"], COL["ink2"], COL["white"]
    bounds = (1.0, 1.0, dw - 1.0, dh - 1.0)
    _r28_base(pg, C, T, R, segs)
    fields = p24_plan(pg, C, w, T, inP, on, k, taken, segs, dw, dh)
    # ---- the water route (P24.2): the zone base's water links in the route's order, one line language on top
    rc = R28DT_ROUTE
    steps, shapes = [], C.D.zones + C.D.strips
    for L in C.D.links:
        if L["kind"] != "water" or len(L["P"]) < 2 or not any(inP(p) for p in L["P"]):
            continue
        a, b = link_shapes(L, shapes)
        ab = (a["code"] if a and a in C.D.zones else None, b["code"] if b and b in C.D.zones else None)
        steps.append((next((i for i, st in enumerate(ROUTE) if st[0] == ab), len(ROUTE)), L, a, b))
    steps.sort(key=lambda s_: s_[0])
    dots, key_lines = [], []
    for n_, (order, L, a, b) in enumerate(steps, 1):
        P = [T(p) for p in L["P"]]
        s = arclen(P)
        if s[-1] < 0.5:
            continue
        hl = min(1.8, s[-1] * 0.45)                      # arrowhead length, mm
        (tx, ty), (ux, uy) = at_len(P, s, s[-1])
        bx, by = tx - ux * hl, ty - uy * hl
        pg.line(sub_line(P, s, 0.0, s[-1] - hl * 0.8), rc, 0.6, cap=1)
        pg.poly([[(tx, ty), (bx - uy * hl * 0.42, by + ux * hl * 0.42), (bx + uy * hl * 0.42, by - ux * hl * 0.42)]],
                fill=rc)
        segs += list(zip(P, P[1:]))
        dots.append((n_, P[0]))
        key_lines.append((n_, _r28_route_runs(order, L, a, b)))
        leg(("r28dt", "route"))
    r_ = 1.9
    for n_, (x, y) in dots:                              # the step's number at its start, nudged off when taken
        b = (x - r_, y - r_, x + r_, y + r_)
        far = False
        if not _r28_free(b, taken, (), bounds, 0.2):
            got = label_spot(x, y, 2 * r_, 2 * r_, taken, bounds, (), 0.2)
            if got:
                b, far = got
        cx, cy = (b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0
        if far:
            pg.line([(x, y), lp_leader_end(b, (x, y))], rc, 0.2)
        pg.circle(cx, cy, r_ + 0.25, fill=white)
        pg.circle(cx, cy, r_, fill=rc)
        pg.text(str(n_), cx, cy - ts["small"] * 0.36, ts["small"], white, bold=True, align="C")
        taken.append(b)
    # ---- G8: the study area where it crosses the window; the section line (D11: this window's cut only)
    st = R28_STUDY_LINE
    for A in (areas or {}).values():
        Q = [T(p) for p in list(A) + [A[0]]]
        if on(Q):
            pg.line(Q, st["colour"], st["width_mm"], list(st["dash_mm"]), cap=0)
            segs += list(zip(Q, Q[1:]))
            leg(("r28dt", "study"))
    if p24_cut_on_plan(pg, w, T, taken, segs, bounds):
        leg(("p24", "cut"))
    # ---- words (G4): place names, one title per field inside it (its species in small grey), the route key, then
    # the small words (dropped where there is no room)
    names = [(HUB_NAME[h["id"]], h["xy"]) for h in C.hubs] + \
        [(nm, xy) for nm, xy in BRIDGES_K if nm in (u"K1", u"K2")] + PLACES
    for nm, xy in names:
        if inP(xy) and not _r28_label(pg, [(nm, ts["place"], True, ink1)], T(xy), taken, segs, bounds):
            missing.append(nm)
    best = {}
    for key, Q in fields:
        vis = clip_ring(Q, (0.0, 0.0, dw, dh))
        if len(vis) >= 3 and abs(area2(vis)) >= R28DT_TITLE_MM2 and abs(area2(vis)) > abs(area2(best.get(key, [(0, 0)] * 3))):
            best[key] = vis
    fpts = [T(p) for p in C.forest if inP(p)]
    for key in R28DT_ORDER + ("spill",):
        if key not in best and not (key == "forest" and fpts):
            continue
        nm = R28_ZONE[key][0] if key in R28_ZONE else P24_NAME[key].capitalize()
        title = [(nm, ts["zone"], True, ink)]
        sub = [(_p24_sp(s_) + (u" · lined cells" if s_ == "reed" else u""), ts["small"], False, ink2)
               for s_ in P24_SPECIES.get(key, ())]
        if key in best:
            ok = _r28_title(pg, best[key], ([title + sub] if sub else []) + [title], taken, segs, bounds)
        else:                                             # the forest corridor is trees, not a field: by its middle tree
            fp = sorted(fpts)[len(fpts) // 2]
            ok = _r28_label(pg, title + sub, fp, taken, segs, bounds, rank=1) or \
                _r28_label(pg, title, fp, taken, segs, bounds, rank=1)
        if not ok:
            missing.append(nm)
    if key_lines:                                        # the route key (P24.2, G5): numbered dot, the step's words
        pitch, rr = 3.6, 1.5
        w_ = max([2 * rr + 1.2 + sum(text_w(t_, ts["label"], bd) for t_, bd in runs) for _, runs in key_lines] +
                 [text_w(u"Water route", ts["label"], True)])
        h_ = ts["label"] * 1.18 + 0.4 + pitch * len(key_lines)
        anc = (sum(p[0] for _, p in dots) / len(dots), sum(p[1] for _, p in dots) / len(dots)) if dots else \
            (dw / 2.0, dh / 2.0)
        got = _r28_spot(w_, h_, anc, taken, segs, bounds)
        if got:
            b = got[0]
            taken.append(b)
            y = b[3] - ts["label"]
            pg.text(u"Water route", b[0], y, ts["label"], ink, bold=True)
            y -= ts["label"] * 0.18 + 0.4
            for n_, runs in key_lines:
                cy = y - pitch / 2.0
                pg.circle(b[0] + rr, cy, rr, fill=rc)
                pg.text(str(n_), b[0] + rr, cy - ts["small"] * 0.36, ts["small"], white, bold=True, align="C")
                x = b[0] + 2 * rr + 1.2
                for t_, bd in runs:
                    pg.text(t_, x, cy - ts["label"] * 0.36, ts["label"], ink1, bold=bd)
                    x += text_w(t_, ts["label"], bd)
                y -= pitch
        else:
            missing.append(u"water route key")
    words = []
    for z in C.D.zones:
        if z["code"] == "WT":
            words.append((u"clean-water classroom", z["q"]))   # v24's education mark: city link stop 7
    if C.canopy:
        cp = [p for P in C.canopy for p in P if inP(p)]
        if cp:
            words.append((u"walk + bike lane" if P24_BIKE else u"riverside walk",
                          min(cp, key=lambda p: (T(p)[0] - dw / 2) ** 2 + (T(p)[1] - dh / 2) ** 2)))
    words += [(u"footbridge", c_["xy"]) for c_ in C.cross if c_["kind"] == "footbridge"]
    words += [(u"stepping stones", c_["xy"]) for c_ in C.cross if c_["kind"] == "stepping stones"]
    if C.terrace:
        words.append((u"viewing terrace", C.terrace["xy"]))
    words += [(u"step to the water", PLACES[1][1]), (u"deck on the Roman bank wall", ROMAN_WALL),
              (u"workshops", CRAFT_XY)]
    for rd in ROADS:
        if rd["change"] in ("pedestrian", "calmed", "shared"):
            P = rd["xy"]
            words.append((rd["change"] + (u" bridge" if u"Köprü" in rd["name"] else u" street"),
                          at_len(P, arclen(P), arclen(P)[-1] / 2.0)[0]))
    for s_, xy in words:
        if inP(xy) and not _r28_label(pg, [(s_, ts["small"], False, ink2)], T(xy), taken, segs, bounds, rank=1):
            missing.append(s_ + u" (no room)")
    # ---- the panel, bottom up: the section's scale bar row, the section, the plan's north arrow and scale bar, the
    # plan, its title (sheet only)
    M = 12.0
    sec = p24_section(C, w, warn)
    W = M + dw + M
    if sec:
        spg, sw_, shh, skeys, smiss = sec
        missing += smiss
        for k_ in skeys:
            leg(("p24s", k_))
        y_sec = 11.0
        y_mk = y_sec + shh + 3.0
    else:
        y_mk = 1.5
    y_pl = y_mk + 10.5
    H = y_pl + dh + 14.0
    sh = Page(W, H)
    sh.poly([rect(0, 0, W, H)], fill=COL["paper"])
    if sec:
        blit(sh, spg, M + (dw - sw_) / 2.0, y_sec)
        scale_bar(sh, M, 1.5, DT_SCALE, (0.0, 10.0, 20.0, 50.0))
        cid, nm = P24_CUTS[w["id"]]
        sh.text(u"Section {} {}' · from the stream to the edge, every zone of the plan above, looking upstream".format(
            nm, nm), M + 72.0, 1.7, ts["label"], COL["ink_dark"], bold=True)
    panel_marks(sh, M, y_mk, DT_SCALE, (0.0, 10.0, 20.0, 50.0))
    sh.clip([rect(M, y_pl, M + dw, y_pl + dh)])
    blit(sh, pg, M, y_pl)
    sh.unclip()
    sh.text(w["title"] + u" · 1:1,000", M, y_pl + dh + 5.0, 5.0, COL["ink_dark"], bold=True)
    sh.crop = (M, 0.5, M + dw, y_pl + dh)
    if y_pl + dh - 0.5 > P24_SEC_MAX:
        warn.append(u"detail {}: plan and section are {:.0f} mm high, more than the {:.0f} mm the booklet page holds "
                    u"with its legend".format(w["id"], y_pl + dh - 0.5, P24_SEC_MAX))
    sh.key, sh.world, sh.scale = w["key"], R, DT_SCALE
    pl = dict(_PLEG[0])
    sh.pleg, _PLEG[0] = pl, None
    sh.r28_leg = r28_crop_legend(pl)
    sh.bid = (w["id"], w["old"], w["caption"])
    return sh


def r28_crop_legend(keys):
    """v28 (WO-T4b-3): a window's booklet legend, only what its plan and section draw: one sample per symbol."""
    cl = _r28_base_cols()
    rows = ((("p24", "reed"), "fill", PLA_WET, u"Reed basins in lined cells"),
            (("p24", "terraces"), "fill", R28_ZONE["terraces"][1], u"Rain terraces"),
            (("p24", "terr"), "line", R28_ZONE["terraces"][1], u"Terrace edge, ticks downhill"),
            (("p24", "spill"), "fill", COL["river"], u"Spillway"),
            (("p24", "wetland"), "fill", WET_COL, u"Widened stream · wetland"),
            (("p24", "arm"), "line", COL["river"], u"Planted side arm"),
            (("p24", "subhub"), "fill", R28_ZONE["subhub"][1], u"Sub-hub in the bed"),
            (("p24", "forest"), "fill", R28_ZONE["forest"][1], u"Forest corridor"),
            (("p24", "tree"), "dot", SEC["crown"], u"Tree at its crown width"),
            (("p24", "demeter"), "fill", PLA_FIELD, u"Demeter's Garden · olive rows 7 × 5 m"),
            (("p24", "hub"), "fill", SQ_FILL, u"Hub square, paved"),
            (("p24", "cafe"), "dot", R28_ZONE["cafe"][1], u"Café"),
            (("p24", "walk"), "line", COL["ink2"], u"Riverside walk"),
            (("p24", "bike"), "line", P24_BIKE_COL, u"Bike lane"),
            (("p24", "stones"), "dot", COL["ink2"], u"Stepping stones"),
            (("p24", "foot"), "line", COL["ink_dark"], u"Footbridge deck"),
            (("p24", "road_calmed"), "line", ROAD_CHANGE_COL["calmed"], u"Street calmed"),
            (("p24", "road_pedestrian"), "line", ROAD_CHANGE_COL["pedestrian"], u"Street or bridge for walking"),
            (("p24", "road_shared"), "line", ROAD_CHANGE_COL["shared"], u"Street shared"),
            (("p24", "hidden"), "dash", COL["river_mid"], u"Hidden stream line"),
            (("p24", "view"), "dot", COL["accent"], u"Viewing terrace, sightline"),
            (("r28dt", "route"), "line", R28DT_ROUTE, u"Water route · step"),
            (("p24", "cut"), "dashdot", COL["ink_dark"], u"Section line, triangles look upstream"),
            (("p24s", "flood"), "fill", P24_FLOOD, u"Reach of Q500 (lines: Q100, Q500)"),
            (("p24s", "wall"), "fill", SCT["stone"], u"DSİ stone wall"),
            (("r28dt", "bed"), "fill", cl["bed"], u"Stream bed (survey)"),
            (("r28dt", "bld"), "fill", cl["bld"], u"Building (survey)"),
            (("r28dt", "study"), "dashdot", R28_STUDY_LINE["colour"], R28_STUDY_NAME))
    return [{"kind": kind, "colour": colour, "label": label} for key, kind, colour, label in rows if key in keys]


def leg(key, val=True):
    LEG.setdefault(key, val)
    if _PLEG[0] is not None:
        _PLEG[0].setdefault(key, val)
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
            (u"WALKS AND SPINES", lines), (u"LINKS", links)] + legend_v24_groups() + detail_legend()


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
    pg.text(OPTION_TEXT[opt], x, y_top - 13.0, 3.4, COL["ink"], bold=True)   # v24: no names, each panel its scale


def scale_bar(pg, x, y, scale, marks=(0.0, 50.0, 100.0, 200.0)):
    """v16: 0-50-100-200 m bar (ink and white blocks) and the scale as text, at the print scale 1:scale (v21: marks
    may be given: the detail windows use 0-10-20-50 m)."""
    k = 1000.0 / scale                                    # page mm per metre
    for i, (a, b) in enumerate(zip(marks[:-1], marks[1:])):
        pg.poly([rect(x + a * k, y, x + b * k, y + 1.2)], fill=COL["ink_dark"] if i % 2 == 0 else COL["white"],
                stroke=COL["ink_dark"], lw=0.15)
    for m_ in marks:                                      # v26.1 (Prompt 8): 7 pt (KEY_MIN), the booklet's floor and
        pg.text(u"{:.0f}{}".format(m_, u" m" if m_ == marks[-1] else u""), x + m_ * k, y + 2.2, KEY_MIN, COL["ink"],
                align="C")                                # the site board's scale bars on p.24 (was 2 mm = 5.7 pt)
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
    return {"runs": out, "covered": covered, "stats": stats, "ref": P, "rows": rows}   # v21; v24: rows for the corridor


# v11 constants (Thread 5)
SPINE_W_M = 6.0                # drawn width of the spines, m (graphic)
WALK_FACET_M = 4.0             # option B: walks as straight facets, Douglas-Peucker tolerance, m (graphic)
_BERGAMA = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
CITY_LINK_FILES = [os.path.join(bg_cache("Bergama_city_link_analysis"), "city_link_results.json"),   # 27 Oct: cached/
                   os.path.join(_BERGAMA, "output", "Bergama_city_link_analysis", "city_link_results.json")]


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


def city_results(CLs):
    """masterplan_results.json: what other scripts read (water balance: riverside_walk_m2)."""
    out = {"script": "bergama_masterplan_v26.py", "version": VERSION,
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


# ================================================================ link helpers
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
    V.frame_P, V.study = list(site), [areas[k_] for k_ in sorted(areas)]   # v27 (MIRAQUA 28 Oct, G10, G8): 02d
    bb = [bbox(A) for A in areas.values()] + [V.bb]
    R = (min(b[0] for b in bb) - ring_m - 5, min(b[1] for b in bb) - ring_m - 5,
         max(b[2] for b in bb) + ring_m + 5, max(b[3] for b in bb) + ring_m + 5)
    survey = read_survey(doc, R) if doc is not None else {}
    if not survey.get("building") and not survey.get("housing"):
        warn.append(u"no survey buildings (BINA_*) in the open file: the zones are drawn on plain paper")
    # ---- per option: the zones (file, else zone base file, else the embedded copy), the corridor, the sheets
    files, lines, pages = [], [], []
    sheets, wins, plc, missing = [], [], {}, {}           # v21: sheets for the booklet crops
    CLs, Cs = {}, {}
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
        C = None
        try:                                             # v24: the ecological corridor of the whole site frame
            t0 = time.time()
            spots_all = read_spots(doc, [V.bb]) if doc is not None else []
            C = Cs[opt] = Corridor(V, survey, CL, D, spots_all, warn)
            st_ = C.stats
            lines.append(u"option {}: max potential area: open {:.1f} ha, bed {:.1f} ha, buildings {:.1f} ha, roads "
                         u"{:.1f} ha; widened {} reaches, side arms {}, kept {}; terraces {} (contours {:.0f} m/ha "
                         u"upstream, {:.0f} below K5); crossings {}; viewing terrace {}; notes {}; {:.1f} s".format(
                             opt, st_[0] / 1e4, st_[3] / 1e4, st_[1] / 1e4, st_[2] / 1e4, len(C.widen), len(C.arms),
                             len(C.kept), len(C.terr), C.steep.get("up", 0.0), C.steep.get("down", 0.0),
                             len(C.cross), u"at {:.0f}, {:.0f}".format(*C.terrace["xy"]) if C.terrace else u"none",
                             len(C.notes), time.time() - t0))
            lines.append(u"option {}: no intervention: {} areas of {:.0f} ha or more ({})".format(
                opt, len(C.nogo), NI_MIN_HA, u"; ".join(u"{:.1f} ha {}".format(r_["ha"], r_["why"]) for r_ in C.nogo)))
        except Exception as ex:
            import traceback
            warn.append(u"option {}: corridor NOT computed ({}: {})".format(opt, type(ex).__name__, ex))
            warn.append(traceback.format_exc()[-480:])
        if C is not None and opt == "A":                 # v26: the open ground for the satellite check (Google Earth)
            try:
                os.makedirs(LOG_DIR, exist_ok=True)
                os.makedirs(bg_cache(OUT_FOLDER), exist_ok=True)
                n_, f_ = open_ground_kml(C, os.path.join(LOG_DIR, OG_KML),
                                         os.path.join(bg_cache(OUT_FOLDER), u"open_ground_check.json"))
                lines.append(u"logs/{}  {} open areas of {:.2f} ha or more, {} with no plant cover (satellite 2021) "
                             u"first  {}".format(OG_KML, n_, OG_MIN_HA, f_, datetime.datetime.now().strftime("%H:%M:%S")))
            except Exception as ex:
                lines.append(u"logs/{}  NOT WRITTEN ({}: {})".format(OG_KML, type(ex).__name__, ex))
        for alt in (1,):                                 # v19: the one sheet
            name = OUT_NAME.format(opt, alt)
            t0 = time.time()
            try:
                if C is None:
                    raise ValueError(u"no corridor computed (see the warnings)")
                panels = [plan_page(C, warn)]           # v28 (revision 29 Oct, D1 a): p.23 only; the open ground page is gone
                sc_mp = getattr(panels[0], "scale", MP_SCALE)
                lines.append(u"masterplan page: {} numbered moves on the plan (1:{:,.0f}); areas left as they are "
                             u"lettered {} of {}".format(len(C.notes), sc_mp, getattr(C, "ni_placed", 0), len(C.nogo)))
                for r_ in C.nogo:
                    if not r_.get("placed"):
                        warn.append(u"area left as it is not lettered on the plan (no free spot), only in the list: "
                                    u"{:.1f} ha {}".format(r_["ha"], r_["why"]))
                LEG.clear()                              # v24: the pages carry their own legend
                pg = make_board(opt, alt, panels)
                path = save(pg, folder, name, u"Bergama masterplan {} option {} (1:{:,.0f})".format(SHORT, opt,
                                                                                                    sc_mp))
                files.append(path)
                pages.append((opt, alt, pg))
                sheets.append((path, pg, sc_mp))
                lines.append(u"{}  {}  {:.1f} s".format(os.path.basename(path),
                                                       datetime.datetime.now().strftime("%H:%M:%S"), time.time() - t0))
            except Exception as ex:
                import traceback
                lines.append(u"{}  NOT WRITTEN ({}: {})".format(name, type(ex).__name__, ex))
                warn.append(traceback.format_exc()[-480:])
        if opt == "A" and CL is not None and C is not None:   # v21: the 1:1,000 detail sheet (option A)
            name = DETAIL_NAME.format(opt)
            t0 = time.time()
            LEG.clear()
            _SCALE[0] = DT_SCALE
            try:
                plc = places(city_link()[0], CL, survey)
                wins = detail_windows(D, plc, DT_PLAN)    # v24: no text block under the plan
                dpanels = []                              # v27 (MIRAQUA 28 Oct, P24.1-P24.5): the fade-out windows
                for w in wins:                            # (02e); no survey spot heights, so no second survey read
                    missing[w["id"]] = []
                    dpanels.append(r28_window_panel(C, w, areas, missing[w["id"]], warn))
                    for m_ in missing[w["id"]]:
                        warn.append(u"detail {}: label not placed: {}".format(w["id"], m_))
                pg = make_board(opt, 1, dpanels, title=u"MASTERPLAN · DETAIL 1:1,000")
                path = save(pg, folder, name, u"Bergama masterplan {} detail option {} (1:1,000)".format(SHORT, opt))
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
    if Cs.get("A") is not None:                          # v27 (MIRAQUA 28 Oct, S1): the senses sheet; a failure only warns
        try:
            lines.append(senses_sheet(Cs["A"], areas, folder, files, warn))
        except Exception as ex:
            import traceback
            warn.append(u"{}  NOT WRITTEN ({}: {})".format(SN_NAME, type(ex).__name__, ex))
            warn.append(traceback.format_exc()[-480:])
    if CLs:                                              # v11: what the other scripts read
        try:
            res_ = city_results(CLs)
            if "A" in Cs:                                # v24: the proposal's movement (spec §4), for the site board
                C_ = Cs["A"]
                res_["movement"] = C_.movement()
                r2 = lambda p: [round(p[0], 1), round(p[1], 1)]
                res_["notes"] = [{"n": nt["n"], "text": nt["text"], "why": nt["why"], "at": [r2(p) for p in nt["at"]]}
                                 for nt in sorted(C_.notes, key=lambda nt: nt["n"])]   # v26: every reason, in full
                res_["no_intervention"] = [{"kind": r_["kind"], "why": r_["why"], "ha": round(r_["ha"], 2),
                                            "at": r2(r_["at"][0])} for r_ in C_.nogo]
                res_["open_ground_check"] = {"imagery": OPEN_CHECK.get("imagery"), "date": OPEN_CHECK.get("date"),
                                             "built_since": len(C_.built_since),
                                             "kml": getattr(C_, "og_check", None)}
            os.makedirs(bg_cache(OUT_FOLDER), exist_ok=True)       # 27 Oct: results in cached/, output/ = PDFs only
            with open(os.path.join(bg_cache(OUT_FOLDER), RESULTS_NAME), "w", encoding="utf-8") as f:
                json.dump(res_, f, ensure_ascii=False, indent=1)
            lines.append(u"{}  {}".format(RESULTS_NAME, datetime.datetime.now().strftime("%H:%M:%S")))
        except Exception as ex:
            lines.append(u"{}  NOT WRITTEN ({}: {})".format(RESULTS_NAME, type(ex).__name__, ex))
    if sheets:                                           # v21: the booklet's crops of the sheets; never breaks them
        try:
            booklet_crops(folder, sheets, wins, plc, missing)
            lines.append(u"cached/booklet/{}/blocks.json  {} crops".format(OUT_FOLDER, sum(len(sh_.panels) for _, sh_, _ in sheets)))
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
        same = mem_get("ver", "") == VERSION        # v24.1 (Aras 27 Oct 15:35): a newly pasted version shows itself
        last = mem_get("last", "") if same else ""   # at once, idle, without the old run's time, log or warnings
        gh_status((mem_get("status", "") if same else "") or SHORT + " · idle")
        for w in (mem_get("warn", []) if same else []) or []:
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
    lines += bg_tidy_output(OUT_FOLDER)              # 27 Oct: output/ = PDFs only
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
    mem_set("ver", VERSION)
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

# LC_EMBED (v26): ESA WorldCover 2021 (CC BY 4.0) in survey coordinates, the site board's built-in copy
# (data/landcover/bergama_landcover_worldcover2021.json, zlib + base64): the no-intervention reasons and the
# open-ground figures read it.
bergama_data("LC_EMBED")


if Rhino is not None:
    try:
        _txt, _files = run()
    except Exception as _ex:
        _txt, _files = u"ERROR: {}: {} ({})".format(type(_ex).__name__, _ex, VERSION), []
        gh_status(SHORT + " · ERROR")
        mem_set("ver", VERSION)
        mem_set("last", _txt)   # 25 Oct: the error stays on the log after the Button is released
        mem_set("status", SHORT + " · ERROR")
    log = _txt
    print(_txt)              # 25 Oct 12:10: the canvas's log output is Grasshopper's "out" (printed text): print the log
    pdf = _files
    if globals().get("_ran_now"):
        mem_set("done", done_text(True, "ERROR" not in str(mem_get("status", "")), time.time() - _T_START))
    done = mem_get("done", "idle")   # 25 Oct 10:20: stays after the run; wire into the next script's run (one-click chain)
