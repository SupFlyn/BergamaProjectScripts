# -*- coding: utf-8 -*-
"""Bergama Group 6: SECTIONS v1.6 (14 Nov 2026; v1.6: the look of Aras 14 Nov 09:46-10:03 UTC, see LOOK_V16 below; v1.5: all sections on ONE page of one PDF, Aras 14 Nov 09:42 UTC "produce all those sections in a single pdf", 09:42:59 "merge
all cuts into a single page": stacked top to bottom in line order, same scale, left edges aligned). Rules: scripts/_template/SCRIPT_STANDARD.md.
Aras 12 Nov 2026 10:43-10:46 UTC: "create these kind of sections and make them creatable by section lines"; "show the
contexts on those sections"; "like the buildings in background, if there is a road you should show the road"; "we had a
like texture band beneath it ... include those as a thin line"; "these gonna be our new sections they gonna be generic
and we'll produce our 12 sections from those".

ONE generic section per section line, in the look of the 27 Oct detail section (his image: S4, both banks, 1:500):
stippled earth, heavy cut line, reeds, iris, meadow, trees, people, light-blue water, the blue level lines Q500, Q100 and
the Oct-Dec high end, a thin material band under the cut, a scale bar. New script; the cut, TIN and water-level method
are SectionFromLine v1.1's (kept as they were checked on S4), the drawing pieces are the 27 Oct detail engine, now in its
own file Data/bergama_sections_engine.py.
  lines    in this order: lines wired to section_line (named L1, L2 ...); else the curves on the open model's layer
           "section_lines" (each named by its object name, else S1, S2 ...); else the 12 lines N1-A ... N6-B of
           Data/section_lines.json (survey coordinates, from his section lines layer v3 of 11 Nov)
  window   half_width m either side of where the line crosses the stream centreline (default 100 m), never past the
           line's own ends
  ground   a TIN of the open file's survey heights within 60 m of the line, cut every 0.25 m
  water    Manning normal depth on this cut (n 0.050, Chow 1959), bed slope from the lowest bed height per 25 m bin 300 m
           up and down the centreline; flows DSI Q100 205.2 / Q500 263.33 m3/s and the Oct-Dec gauge flow 0.423 m3/s
           (research/rain_river_levels). Summer strip 4.0 m x 0.30 m at the bed low point (design).
  context  from cached/basemap/basemap.json (the site step's layers): buildings the line cuts and buildings up to
           BACK_M behind it (looking direction), each at its own floor count x storey height on the survey ground, flat
           topped (the survey holds no roof forms); roads = the street areas the line crosses, and street centrelines
           crossed between two survey road edges (YOL_SOSE / YOL_BORDUR) within 12 m. A building without a height in
           the basemap is not drawn (counted in the log). Grey tones of the context are drawing values (ours).
  planting by rule (design intention, ours): reeds and iris on the wet bed, meadow above, survey trees within 3 m.
  NO design of terraces, steps or decks: the plan holds no levels. On S4 only (the 27 Oct cut wired as a line) the
  engine's designed banks are drawn.

Component: Rhino 8 > Grasshopper > Python 3 Script (the board builder places it from the cloud kit).
  input  run           Button (or the previous script's done text)
  input  section_line  Line list: lines picked in Rhino (survey coordinates); none = the 12 node sections
  input  scale         sheet scale 1:n (default 500)
  input  half_width    m drawn either side of the stream (default 100)
  output log / done    as every Bergama script
Reads  ~/Downloads/Bergama/Data/bergama_sections_engine.py, Data/section_lines.json, Data/selinos_centreline.json,
       ~/Downloads/Bergama/cached/bergama_basemap/basemap_layers.json + streets.json (press Basemap first; else the old
       cached/basemap/basemap.json), the open Rhino model's survey layers (read once per press)
Writes ~/Downloads/Bergama/output/bergama_sections/Sections.pdf          ONE page, every line stacked top to bottom (1:scale, PDF layers)
       ~/Downloads/Bergama/cached/bergama_sections/sections.json         every cut's numbers
       ~/Downloads/Bergama/logs/bergama_sections_log.txt
"""
import os, re, time, json, math, bisect, glob, random

# ---- SETTINGS ----
VERSION = "v1.29.1"   # v1.29.1: FLAG when the survey bed low point lies more than 15 m from the centreline crossing (N2-A: 37 m); v1.29 v1.29 (Aras 12:10 "review the drawings yourself and compare with the examples", liked_2026-11-12 B05 kent kesitleri / WHY_WE_LIKED defaults 5 and 9): no clouds, a near-white sky, his Archicad context toned back as ghost lines and pale fills so the cut, our proposals and the trees lead; our canopy colours unchanged; ground unchanged (Aras 10:35); v1.28.6 v1.28.6 (read of the v1.28.5 run: N2-B had a glazed canopy room on the stream bed; that cut has no water levels): no glazed rooms on a cut whose flood level is unknown (open bays with planters instead); v1.28.5 v1.28.5 (AcBuild v1.7 / SectionsAC v1.11 ground bands 10-400+ m): his Archicad ground bands drawn far to near together with the survey bands, toned by depth to 400 m; v1.28.4 v1.28.4 (read of the v1.28.2 run: N1-B houses floating over a hill the survey does not reach; N4-A hall cut as bare lines): Archicad "ground" pieces (his terrain behind, from SectionsAC) drawn as far ground bands under his houses; Kızıl Avlu on the cut drawn here again (brick, poché); v1.28.3 v1.28.3 (AcBuild v1.6 builds the canopies in Archicad): canopies behind the cut drawn here only where the cut has no Archicad background; the cut canopy stays ours; v1.28.2 v1.28.2 (Aras 10:00-10:02 "The bottom area is closed" / "Some closed areas underneath", his canopy elevation): on the cut the deck on a low stone plinth; closed glazed rooms in every other bay between the Y columns, up to the louvres, only where the floor is at least Q500 + 0.60 m; timber planters in the open bays; v1.28.1 v1.28.1 (read of the v1.27.2 run: N1-N4 had no ground bands and no trees behind): v1.27.1 had skipped every item behind the cut once an Archicad view existed; now only the drawn houses and the hall are skipped; v1.28 v1.28 (Aras 15 Nov 09:52 "draw our canopies much better like designed ones", his canopy reference): canopies as designed roofs: folded triangle-facet skin running out to knife edges, a timber louvre layer under it following the folds (slats on the cut), Y-shaped steel columns under the valleys on a regular bay, a timber deck under the roof on the cut; heights as v1.26; v1.27.2 v1.27.2 (section_lines v4: N5 / N6 moved): an Archicad background whose length L differs from the cut by more than 1 m is stale and left out (logged as no Archicad background); v1.27.1 v1.27.1 (Archicad thread, AcBuild v1.5 / SectionsAC v1.9): an Archicad background with no pieces (N6-B: nothing behind) means no houses, not a FLAG; Kızıl Avlu from Archicad wherever the cut has an Archicad view (AcBuild builds it from the same outline, 19 m walls), drawn here only where it has none; S4 from its own Archicad section; v1.27 v1.27 (Aras 15 Nov 08:33 "if we already have all the drawing in archicad why dont we just take every elevation from there"): no drawn houses at all, behind or cut; every house comes from his Archicad section (SectionsAC background cache); Kızıl Avlu stays drawn until it is in the Archicad model; a cut with no Archicad view yet is logged and shows no houses; v1.26 v1.26 (tree_canopy_heights_v1.md, library/research, 15 Nov; defaults via the coordinator): his trees at the mature-height midpoint of the Van den Berk ranges (stone pine 20, plane 32.5, ash 17.5, willow 22.5, olive 7.5 m), tamarisk 4 m (Ferns), sourced, not Türkiye-specific; canopy valley underside at least 2.30 m clear (DfT Inclusive Mobility 2021 s.3.2) and at least Q500 + 0.60 m (EA 600 mm applied to Q500), ridge 1.8 m above the valley (design assumption, UNVERIFIED); v1.25 (Aras 06:57 "changing those backgrounds with real archicad elevations"): where SectionsAC v1.5 has written cached/bergama_archicad/background/<cut>.json (registered in s / z m), the houses behind are his Archicad elevations from it (ground bands first, then the elevations, then the asset trees); else the drawn houses; v1.24.1 (Aras 06:57 "like you were drawing it few instances back buildings had windows and shutters"): the background houses exactly as v1.17-v1.19 drew them (windows, shutters, sills, balconies, cornice, tiles, chimneys; their fade too), on the v1.24 layered ground with the asset trees; v1.24 (Aras 06:50-06:51 "you already have more decent section background ... u used to have"): the view behind the cut restored from the board sections he liked (selinus_board v67.1 sa_scene / sa_render, booklet p04-05 "Sections across the stream"): the survey ground seen at 10 depths (5-118 m) as layered profiles paler with distance, the houses behind on their own survey ground among them (detailed type elevations again, faded 0.12-0.82 with distance), his asset trees in between, all far to near; v1.23 (Aras 06:49 "tree's from the asset files for god's sake"): every tree, on and behind the cut, is his asset-library cutout of its species (Data/cutouts: plane, ash, stone_pine ...), behind the cut in the library's own depth tones (_d1 from 40 m, _d2 from 100 m); no drawn tree symbols; v1.22 (read of v1.21 on master.svg): rosemary left out of the trees, each tree drawn by its species in his layer (stone pine umbrella, plane broad, ash oval), trees found up to 200 m behind (N6 had none within 120 m), his water stairs (begum_su_merdiven) cut as stepped terraces, yuruyus/circulation as promenade; v1.21 (Aras 06:19 UTC: master.svg is the masterplan, read by MasterplanBase v1.5; its PLANTING layer holds his trees): the trees on and behind the cut are his planted trees (crown size from the plan, height ASSUMED 1.3 x crown, 5-14 m); the green-area tree rows only when the plan has no planting layer; v1.20.1 (600 dpi read of v1.20: Kızıl Avlu behind N3-A a heavy blank pink block): the hall toned lighter like the silhouettes, brick courses at every scale (1 m, or 2 m where 1 m prints under 0.4 mm); v1.20 (Aras 15 Nov 06:08 "the background houses looks awful there is no tree's" / "take the our masterplan SVG directly"): trees behind the cut in elevation, the survey tree symbols up to TREE_BACK_M behind (height ASSUMED) and a row along each green area of his masterplan SVG (MasterplanBase cache) behind the cut (design intent); background houses as clean flat silhouettes toned by distance (no window dots, chimneys, plinths, tiles); v1.19.1 (Aras 15 Nov 06:00 "four seasons one cut doesnt have any context" / 05:59 "left wall looks weird"): S4 finds its survey houses up to S4_BACK_M behind (only 1 within 200 m there), a house behind that overlaps the channel is trimmed to the bank instead of dropped, retaining walls on a slope drawn as cut walls held in the ground with a flush coping (no free-standing box), path slabs with a hairline edge, "green" labelled "Green"; v1.19 (Aras 15 Nov 05:57 UTC "our canopies are triangle shaped ... many triangles pulled into together"): canopies drawn as folded triangle plates, folds where his plan's canopy triangle corners fall along the cut, facets toned alternately, posts at the valleys; canopy triangles behind merged into one canopy; v1.18.2: Kızıl Avlu reads as the brick hall (brick courses, cut wall ends in poché 1.2 m thick, ASSUMED; no windows drawn: the source places them only vaguely); v1.18.1: Kızıl Avlu main hall from the masterplan outline, walls 19 m (Wikipedia "Red Basilica": "Its walls still survive up to a height of 19 metres"), drawn as a roofless brick mass; the S4 log line says only the low point is the engine's; v1.18 (Aras 15 Nov 04:58 UTC "All defaults are fine"): proposals outlined in the accent C07A2E, S4 drawn from the B19 masterplan (parts cached for the seasons page), N4-A moved 22.6 m onto the Red Hall (section_lines.json); v1.17.4 v1.17.4: S4 bed and strip from the engine's own low point (they came from the cut drawn before it); v1.17.3 v1.17.3 (error review of v1.17.2): no plan wall inside the channel, seat walls start on the ground, decks 0.25 m clear, near-coincident dashed levels merged, existing ground a fine light dashed hairline; v1.17.2 v1.17.2 (fresh review of v1.17): canopy trunks on the ground and branches meeting the shell, overlapping canopies / pavilions thinned (nearer first), deck balustrade as rail and posts (the glass box read as a tank); v1.17.1 v1.17.1: the cut line drawn whole (an end trim had dropped most of it since v1.6.13); v1.17 v1.17 (two independent reviews of v1.16): the cut line on top of the ground skin (it lay hidden), butt ends; clouds under the frame top and off the ground; land-use band 2.8 mm, words 1.7 mm, street lighter; scale bar in the title line (cells give the drawing ~6 mm more height); v1.16.1 v1.16.1: land-use band words one size on every cut (they ran 1.6-3.3 mm); v1.16 v1.16 (600 dpi read of the v1.15.2 PDF): one-line titles and a tighter band / scale bar (drawings larger), bridges at bank level (N2-A on the bed), seat walls where the ground is flat, water ripples only inside water, thinner water surface; v1.15.2: v1.15.2: sheet fix (KeyError on the smallest scale, v1.15.1 crashed before the PDF and the cache); v1.15.1 v1.15.1: dashed water levels 0.1 mm, water surface line and wall outlines thin at small scales (600 dpi read of the v1.14 PDF); v1.15 v1.15 (Aras 21:33 "do a proper check"): each cut on the A3 sheet at its own largest scale, fitted to its cell (the sheet was about 60 % empty), titles one size, cut line heavier (0.4-0.6 mm); v1.14 v1.14 (Aras 21:31 "please remove these kind of showings"): no floating text labels with dashed leader lines over the cuts (Road, Canopy, Building n floors, ...); cut houses drawn like the background houses, light (Aras 21:32); v1.13 (Aras 21:26 "drawings flows out fix that"): every fill cut at the cut frame, clouds / cutouts / circles crossing it left out; v1.12 (recheck of v1.11 output): footbridges only on cuts that cross the stream; canopy edge thin at small scales; v1.11: masterplan read right (no 2.1 km2 texture frame as "green", open lines only for walls, kopruler = bridges), plan trees 12-20 m apart, drawing lines cut at the frame; v1.10: channel walls only to the bank ground + a 0.9 m parapet (Aras 16:23); masterplan spans merged per kind, a progress file logs/bergama_sections_progress.txt (v1.9 ran > 17 min); v1.9 (Aras 14 Nov 16:12-16:13): section_lines.json v2: per node A square to the stream and B along the bank crossing it, both from frame edge to frame edge (drawn whole), looking different ways; v1.8 (Aras 14 Nov 15:38-15:41): the sections are the masterplan in 3D: every piece of his plan the cut crosses (MasterplanBase cache of B19_setB_layers259.svg) drawn as a designed form (stepped terraces as the finished ground, promenade and cycle paving, retaining walls, boulders, water decks, lens footbridges, saddle-shell canopies on steel trees, sedum-roof pavilions; canopies and pavilions behind the cut in elevation), heights design intent; v1.7 (Aras 14 Nov 15:25-15:35): all 12 cuts on ONE A3 landscape sheet, no 1:x printed; planting drawn at 1:75 and scaled to the page (true proportions), no soil root hairs; cut houses as plain silhouettes; houses behind more detailed (plinth, tiles, chimney, sills, glazing bars, shutters, balconies, door hood) and up to 200 m behind
CUT_HOUSE_DIST_M = 60.0   # v1.14: cut houses toned like a house 60 m behind (light, quiet; drawing value, ours)
LEVEL_LW = 0.1   # v1.15: dashed water levels as hairlines (mm)
ACCENT = "C07A2E"   # v1.18: the project accent = our intervention (DIAGRAM_STYLE), Aras 15 Nov 04:58 UTC
RED_HALL_KEY = u"Kizil_Avlu_outline"   # v1.18.1: MasterplanBase layer holding the Kızıl Avlu main hall outline
RED_HALL_MIN_M2 = 1000.0   # only the hall rings (about 1250-1300 m2); the round towers (about 146 m2) have no sourced height
RED_HALL_H_M = 19.0        # Wikipedia "Red Basilica": "Its walls still survive up to a height of 19 metres (62 ft)"
RED_HALL_FILL, RED_HALL_EDGE = "D9B8A6", "A9877A"
RED_HALL_WALL_M = 1.2      # cut wall ends: thickness ASSUMED (drawing only; no sourced figure)
RED_HALL_POCHE = "8E5A48"  # the cut brick   # brick, toned light like the houses
S4_FROM_B19 = True   # v1.18 (Aras 15 Nov 04:58 UTC): S4 drawn from his masterplan like the 12 cuts, not the 27 Oct engine design
CALLOUTS = False   # v1.14: leader-line labels over the cuts left out (Aras 21:31 UTC)
GH_LABEL = "Sections"
OUT_FOLDER = "bergama_sections"
LOG_NAME = "bergama_sections_log.txt"
GH_INPUTS = {"section_line": "line list", "scale": "int 50..2000 = 500", "half_width": "int 20..400 = 100"}
SECTION_LAYER = "section_lines"   # the model layer his own section lines sit on (object name = section name)
SEASON = "autumn"          # the one drawing per line: Q500, Q100 and the Oct-Dec high end, as in his image
# v1.3, Aras 12 Nov 19:10 UTC: "for storey height you got the data look for it". The project's own values (site board
# scripts/selinus_board_v67.py: FLOOR_H = 3.0 and STOREY = {"religious": 5.0, "institutional": 3.5, "industrial": 4.5},
# printed on its sheets as "Storey heights 3.0 m; civic 3.5, sacred 5.0, industry 4.5"): typical values, not measured.
# The Basemap cache tells heritage / sacred outlines from the rest, so those take 5.0 m and every other building
# 3.0 m; civic (3.5) and industry (4.5) are not told apart in the cache yet and are drawn at 3.0 m.
STOREY_M = 3.0             # m per floor, every building that is not heritage / sacred
STOREY_HERITAGE_M = 5.0    # m per floor, the Basemap's heritage outlines (sacred and heritage)
S4_BACK_M = 500.0          # v1.19.1: S4 (open edge of town) looks for its survey houses this far behind (8 there, 1 within 200 m)
BACK_M = 200.0             # v1.7 (Aras 15:28 "there is no houses at the background"): 200 m; v1.6: 120 m; buildings up to this far behind the cut are drawn as background (was 30 m)
ROAD_EDGE_M = 12.0         # a street centreline crossing counts as a road between survey edges this close to it
ROAD_T = 0.25              # m, drawn thickness of the road surface
BLD_FILL, BLD_EDGE, BLD_CUT_FILL = "F1EFEA", "9A948C", "E2DFD8"   # context greys (drawing values, ours)
ROAD_FILL = "6E6B66"       # existing road surface (drawing value, ours; the engine's red asphalt is the design's)
BAND_H = 2.0               # mm, the thin material band

SURVEY_LAYERS = ["NOKTA_TAKEOMETRI", "NOKTA_POLIGON", "NOKTA_NIRENGI", "EGRI_1M", "EGRI_2M", "EGRI_5M", "EGRI_10M", "EGRI_ARA", "SEV_UST", "SEV_ALT",
                 "HIDRO_DERE_SULU"]
MARK_LAYERS = {"SEV_UST": "bank top", "SEV_ALT": "bank toe", "HIDRO_DERE_SULU": "stream line", "YOL_SOSE": "road edge",
               "YOL_BORDUR": "kerb"}
TREE_LAYERS = ["SEMBOL_TEK_AGAC", "SEMBOL_YPDKN_AGAC", "SEMBOL_YAP_DOKMEYEN"]
CORRIDOR_M = 60.0          # survey heights this close to the line build the TIN
# v1.2 (first Rhino run, 12 Nov: N2-A, N3-A, N3-B not drawn, "only 18 survey heights within 60 m"): in the old town
# the survey has almost no height points (counted in Bergama_Altlik.3dm within 60 m of N2-A: 0 tacheometric points,
# 22 traverse points on NOKTA_POLIGON, which v1.1 did not read). Now the traverse and triangulation points are read
# too, and where fewer than HEIGHTS_WANT heights lie in the corridor it is widened step by step (CORRIDOR_STEPS);
# the cut is drawn from HEIGHTS_MIN heights on, with a FLAG line that says how thin its ground is.
CORRIDOR_STEPS = (60.0, 100.0, 150.0)
HEIGHTS_WANT, HEIGHTS_MIN = 50, 8
DS = 0.25                  # drawn profile step, m
HYD_HALF, HYD_DS = 200.0, 0.5   # hydraulic cut: 200 m either side of the stream crossing, 0.5 m steps (research)
CHANNEL_M = 40.0           # the bed low point is the lowest ground within this distance of the crossing
MAX_LEN_M = 200.0          # a longer line is drawn 100 m either side of its stream crossing (FLAG)
N_MANNING = 0.050          # worst-case roughness, gravel-cobble bed (Chow 1959; research A3s)
SLOPE_HALF, SLOPE_BIN = 300.0, 25.0
SA_BANDS = (5.0, 10.0, 16.0, 24.0, 34.0, 46.0, 60.0, 76.0, 95.0, 118.0)   # v1.24: m, the ground behind seen at these
#                                    depths (copied from selinus_board v67.1 SA_BANDS, the board sections Aras liked)
BAND_GROUND, BAND_EDGE = "CFCAB0", "A9A38B"   # v1.24: nearest band (the cut ground's family); paler with depth
TREE_BACK_M = 200.0        # v1.20: survey trees / masterplan green this far behind the cut drawn in elevation
TREE_SURVEY_H_M = 7.5      # v1.20: survey tree symbols carry no height: 7.5 m ASSUMED (as the cut's survey trees)
TREE_FILL, TREE_EDGE = "9EAA8C", "7C8770"   # v1.20: tree silhouettes behind (flat, toned to the sky with distance)
HOUSE_SILHOUETTE = False    # v1.20: False = the v1.7 detailed houses
HOUSE_SIL, HOUSE_SIL_ROOF = "DEDBD3", "CCC7BD"   # v1.20: background house silhouette wall / roof
TREE_NEAR_M = 3.0          # survey tree symbols this close to the line are drawn on it
OBLIQUE_DEG = 20.0         # a cut further than this off square to the stream: FLAG (flow area overstated)
STRIP_W, STRIP_D = 4.0, 0.30    # summer water strip (design, case.md s.4)
WET_BAND_M = 1.0           # planting by rule: reeds / iris on ground up to this height above the bed (design, ours)
# flows, m3/s: DSI design floods (Danistay 6. D. E.2021/9521 K.2023/4193, as cited on the water board) and the
# area-scaled gauge flows WY2016-2021 (research/rain_river_levels/tables/A3s_monthly_mean_depth_surveyed_sections.csv,
# A3s_levels_by_event_surveyed_sections.csv: Jan via Ilica 3.36, Apr via Ilica 0.752, Dec via Komurcu 0.423,
# highest daily mean 6 Jan 2017 43.9)
Q100, Q500 = 205.2, 263.33
SEASON_WATER = {   # (Q, filled?, label with %+.2f and %.2f)
    "winter": [(3.36, True, u"Jan-Feb mean %+.2f (%.2f m, calculated)"),
               (43.9, False, u"highest day 6 Jan 2017 %+.2f (%.2f m, calculated)")],
    "spring": [(0.752, True, u"Mar-Apr, low end %+.2f (%.2f m, calculated)"),
               (3.36, False, u"high end of Jan-Apr %+.2f (%.2f m, calculated)")],
    "summer": [],
    "autumn": [(0.423, True, u"Oct-Dec high end %+.2f (%.2f m, calculated)")],
}
SEASONS_ORDER = ("winter", "spring", "summer", "autumn")
STRIP_HELD = {"winter": False, "spring": True, "summer": True, "autumn": True}   # engine SEASONS strip_held
S4_WINDOW = (538.0, 652.0)      # the engine's design of both banks (SECTIONS 1-1' s 538-598, 2-2' s 652-588)

# ---- Bergama folders (Aras 24 Oct 08:28 + 27 Oct 11:07; SCRIPT_STANDARD §9). Every script uses ONLY these. ----
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")


def bg_output(name):
    return os.path.join(BERGAMA_ROOT, "output", name)


def bg_cache(name):
    return os.path.join(BERGAMA_ROOT, "cached", name)


def bg_booklet(name):
    return os.path.join(BERGAMA_ROOT, "cached", "booklet", name)


def bg_logs(*sub):
    return os.path.join(BERGAMA_ROOT, "logs", *sub)


DATA_DIR = os.path.join(BERGAMA_ROOT, "Data")
OUT_DIR = bg_output(OUT_FOLDER)
CACHE_DIR = bg_cache(OUT_FOLDER)
LOG_DIR = bg_logs()


# ================================================================ the engine (27 Oct look)
def load_engine(log):
    p = os.path.join(DATA_DIR, "bergama_sections_engine.py")
    with open(p, encoding="utf-8") as f:
        txt = f.read()
    ns = {"__name__": "bergama_sections_engine"}
    exec(compile(txt, "bergama_sections_engine", "exec"), ns)
    log.append(u"engine: %s read from %s" % (ns.get("VERSION"), p))
    return ns


def load_basemap(log):
    """the context (survey m): buildings with heights, street areas, street centrelines; {} if missing.
    v1.1: read from the Basemap script's caches (cached/bergama_basemap/basemap_layers.json: closed building
    outlines + the survey's floor counts; streets.json: the street bands); a building's height = its floor count x
    STOREY_M (the project's storey height, an assumption, not a survey height). Only when that cache is missing, the
    old site board's cached/basemap/basemap.json is read as before."""
    p = os.path.join(bg_cache("bergama_basemap"), "basemap_layers.json")
    if os.path.isfile(p):
        try:
            with open(p, encoding="utf-8") as f:
                J = json.load(f)
            B, n_out = [], 0
            for key in ("buildings", "heritage"):
                rings = [P for cl, P in J.get("layers", {}).get(key, []) if cl and len(P) >= 3]
                fls = (J.get("floors") or {}).get(key) or []
                for i, r in enumerate(rings):
                    n_out += 1
                    fl = int(fls[i]) if i < len(fls) else 0
                    xs, ys = [q[0] for q in r], [q[1] for q in r]
                    B.append((min(xs), min(ys), max(xs), max(ys), r, fl * (STOREY_HERITAGE_M if key == "heritage" else STOREY_M), fl))
            A = []
            ps = os.path.join(bg_cache("bergama_basemap"), "streets.json")
            if os.path.isfile(ps):
                with open(ps, encoding="utf-8") as f:
                    for cl, r in json.load(f).get("layers", {}).get("streets", []):
                        if len(r) >= 3:
                            xs, ys = [q[0] for q in r], [q[1] for q in r]
                            A.append((min(xs), min(ys), max(xs), max(ys), r))
            else:
                log.append(u"FLAG context: %s not found: no road surfaces drawn; press Basemap once" % ps)
            log.append(u"context: %s (%s): %d building outlines, %d with a floor count (height = floors x %.1f m, heritage and "
                       u"sacred x %.1f m: the site board's typical storey heights); %d street bands" % (
                           p, J.get("made_by", u"?"), n_out, sum(1 for b_ in B if b_[6] > 0), STOREY_M, STOREY_HERITAGE_M,
                           len(A)))
            return {"buildings": B, "areas": A, "streets": []}
        except Exception as ex:
            log.append(u"FLAG context: %s not read (%s); trying the old site board's cache" % (p, type(ex).__name__))
    p = os.path.join(bg_cache("basemap"), "basemap.json")
    try:
        with open(p, encoding="utf-8") as f:
            L = json.load(f).get("layers", {})
    except Exception as ex:
        log.append(u"FLAG context: %s not read (%s): no buildings or roads drawn; press Basemap once"
                   % (p, type(ex).__name__))
        return {}
    B = []
    for b in L.get("buildings", []):
        r = (b.get("rings") or [[]])[0]
        if len(r) >= 3:
            xs, ys = [q[0] for q in r], [q[1] for q in r]
            B.append((min(xs), min(ys), max(xs), max(ys), r, float(b.get("h") or 0.0), int(b.get("floors") or 0)))
    A = []
    for r in L.get("street_areas", []):
        if len(r) >= 3:
            xs, ys = [q[0] for q in r], [q[1] for q in r]
            A.append((min(xs), min(ys), max(xs), max(ys), r))
    Sx = [st[1] for st in L.get("streets_in", []) if len(st) > 1 and len(st[1]) >= 2]
    log.append(u"context: %s: %d buildings, %d street areas, %d street lines" % (p, len(B), len(A), len(Sx)))
    return {"buildings": B, "areas": A, "streets": Sx}


def context_for(C, BM, tin, ox, oy, lg):
    """C.bld = [(s0, s1, base z, height, cut?, distance behind, floors)], C.roads = [(s0, s1)], C.streets = [s]"""
    C.bld, C.roads, C.streets = [], [], []
    if not BM:
        return
    w0, w1 = C.window
    pa, pb = C.xy(w0), C.xy(w1)
    reach = S4_BACK_M if C.is_s4 else BACK_M            # v1.19.1
    pad = reach + 5.0
    box = (min(pa[0], pb[0]) - pad, min(pa[1], pb[1]) - pad, max(pa[0], pb[0]) + pad, max(pa[1], pb[1]) + pad)
    no_h = 0
    for x0, y0, x1, y1, r, h, fl in BM["buildings"]:
        if x1 < box[0] or x0 > box[2] or y1 < box[1] or y0 > box[3]:
            continue
        so = [C.su(q[0], q[1]) for q in r]
        omin, omax = min(o for _, o in so), max(o for _, o in so)
        if omax <= 0.0 or omin > reach:
            continue
        is_cut = omin < 0.0
        if is_cut:
            xs = []
            for (sa, oa), (sb, ob) in zip(so, so[1:] + so[:1]):
                if (oa < 0.0) != (ob < 0.0):
                    xs.append(sa + (sb - sa) * (0.0 - oa) / (ob - oa))
            if len(xs) < 2:
                continue
            a, b = min(xs), max(xs)
        else:
            a, b = min(q[0] for q in so), max(q[0] for q in so)
        a, b = max(a, w0), min(b, w1)
        if b - a < 0.5:
            continue
        if h <= 0.0:                                   # v1.8 (N6 drew no houses behind): no floor count in the
            no_h += 1                                  # data = drawn as 1 floor (ASSUMED, counted in the log)
            h, fl = STOREY_M, 1
        cx, cy = sum(q[0] for q in r) / len(r), sum(q[1] for q in r) / len(r)
        zb = None if is_cut else tin.z(cx - ox, cy - oy)
        C.bld.append((a, b, zb, h, is_cut, max(0.0, omin), fl))
    C.bld.sort(key=lambda t: -t[5])
    # v1.24: the ground behind at SA_BANDS depths (TIN), one profile per depth, None where the TIN does not reach
    C.bands = []
    nx, ny = -C.u[1], C.u[0]
    for d_ in SA_BANDS:
        prof_ = []
        s = w0
        while s <= w1 + 1e-9:
            px, py = C.xy(s)
            prof_.append((s, tin.z(px + nx * d_ - ox, py + ny * d_ - oy)))
            s += 2.0
        C.bands.append((d_, prof_))
    # v1.20: the survey trees behind on their survey ground (TIN), height assumed
    C.trees_back = [(s_, d_, tin.z(x_ - ox, y_ - oy), TREE_SURVEY_H_M, u"survey")
                    for s_, d_, x_, y_ in getattr(C, "trees_back_xy", [])]
    # v1.6: the ground behind the cut (booklet p22 "Ground behind the cut"): per station the highest survey ground
    # 10 ... BACK_M m behind the line (TIN; stations the TIN does not reach are left out)
    nx, ny = -C.u[1], C.u[0]
    C.back = []
    s = w0
    while s <= w1 + 1e-9:
        px, py = C.xy(s)
        zs = [tin.z(px + nx * d - ox, py + ny * d - oy) for d in range(10, int(BACK_M) + 1, 10)]
        zs = [z for z in zs if z is not None]
        C.back.append((s, max(zs) if zs else None))
        s += 2.0
    iv = []
    for x0, y0, x1, y1, r in BM["areas"]:
        if x1 < box[0] or x0 > box[2] or y1 < box[1] or y0 > box[3]:
            continue
        xs = sorted(t * C.L for t in (seg_cross(C.A, C.B, p, q) for p, q in zip(r, r[1:] + r[:1])) if t is not None)
        for a, b in zip(xs[0::2], xs[1::2]):
            a, b = max(a, w0), min(b, w1)
            if b - a >= 0.5:
                iv.append((a, b))
    edges = sorted(m[0] for m in C.marks if m[1] in ("road edge", "kerb"))
    for pl in BM["streets"]:
        for p, q in zip(pl[:-1], pl[1:]):
            if max(p[0], q[0]) < box[0] or min(p[0], q[0]) > box[2] or max(p[1], q[1]) < box[1] or min(p[1], q[1]) > box[3]:
                continue
            t = seg_cross(C.A, C.B, p, q)
            if t is None or not (w0 <= t * C.L <= w1):
                continue
            sc = t * C.L
            if any(a - 0.5 <= sc <= b + 0.5 for a, b in iv):
                continue
            le = [e for e in edges if sc - ROAD_EDGE_M <= e < sc]
            ri = [e for e in edges if sc < e <= sc + ROAD_EDGE_M]
            if le and ri and ri[0] - le[-1] >= 1.5:
                iv.append((le[-1], ri[0]))
            else:
                C.streets.append(sc)
    iv.sort()
    for a, b in iv:
        if C.roads and a <= C.roads[-1][1] + 0.3:
            C.roads[-1] = (C.roads[-1][0], max(C.roads[-1][1], b))
        else:
            C.roads.append((a, b))
    C.streets = [x for x in sorted(C.streets) if not any(a - 0.5 <= x <= b + 0.5 for a, b in C.roads)]
    lg.append(u"context %s: %d building(s) cut, %d behind within %.0f m, %d without a floor count drawn as 1 floor (assumed); %d road(s) %s; %d "
              u"street line(s) without survey edges (marked, no width)" % (
                  C.name, sum(1 for t in C.bld if t[4]), sum(1 for t in C.bld if not t[4]), reach, no_h, len(C.roads),
                  u", ".join(u"%.1f-%.1f m" % r for r in C.roads), len(C.streets)))


# ================================================================ survey from the open Rhino model
def _layer_objs(doc, name):
    idx = doc.Layers.FindByFullPath(name, -1)
    if idx < 0:
        for lay in doc.Layers:
            if not lay.IsDeleted and lay.Name == name:
                idx = lay.Index
                break
    if idx < 0:
        return []
    return list(doc.Objects.FindByLayer(doc.Layers[idx]) or [])


def _curve_pts(rg, g):
    try:
        ok, pl = g.TryGetPolyline()
        if ok:
            return [(p.X, p.Y, p.Z) for p in pl]
    except Exception:
        pass
    try:
        ts = g.DivideByLength(1.0, True) or []
        pts = [g.PointAt(t) for t in ts]
        if g.IsClosed is False and pts:
            pts.append(g.PointAtEnd)
        return [(p.X, p.Y, p.Z) for p in pts]
    except Exception:
        return []


def read_survey(box, log):
    """{layer: [polyline [(x, y, z)], ...]} (points as one-point polylines) inside box (x0, y0, x1, y1)"""
    import Rhino
    rg = Rhino.Geometry
    doc = Rhino.RhinoDoc.ActiveDoc
    out, cnt = {}, {}
    for name in SURVEY_LAYERS + list(MARK_LAYERS) + TREE_LAYERS:
        if name in out:
            continue
        L = []
        for o in _layer_objs(doc, name):
            g = o.Geometry
            if isinstance(g, rg.Point):
                p = g.Location
                if box[0] <= p.X <= box[2] and box[1] <= p.Y <= box[3]:
                    L.append([(p.X, p.Y, p.Z)])
            elif isinstance(g, rg.Curve):
                b = g.GetBoundingBox(True)
                if b.Max.X < box[0] or b.Min.X > box[2] or b.Max.Y < box[1] or b.Min.Y > box[3]:
                    continue
                if isinstance(g, rg.ArcCurve) and g.IsCircle():          # a symbol drawn as a circle: its centre
                    c = g.Arc.Center
                    L.append([(c.X, c.Y, c.Z)])
                    continue
                P = _curve_pts(rg, g)
                if P:
                    L.append(P)
            elif isinstance(g, rg.InstanceReferenceGeometry):            # a symbol block: its insertion point
                p = g.Xform * rg.Point3d(0.0, 0.0, 0.0)
                if box[0] <= p.X <= box[2] and box[1] <= p.Y <= box[3]:
                    L.append([(p.X, p.Y, p.Z)])
        out[name] = L
        cnt[name] = len(L)
    log.append(u"survey read: " + u", ".join(u"%s %d" % kv for kv in sorted(cnt.items())))
    return out


def delaunay(xy):
    """triangles (index triples) of 2D points (Grasshopper's Delaunay, as the engine's re-cut uses it)"""
    import Grasshopper.Kernel.Geometry as GKG
    nodes = GKG.Node2List()
    for x, y in xy:
        nodes.Append(GKG.Node2(x, y))
    return [(f.A, f.B, f.C) for f in GKG.Delaunay.Solver.Solve_Faces(nodes, 1)]


class Tin(object):
    def __init__(self, pts):
        self.p = pts                       # [(x, y, z)] (local coordinates)
        self.t = delaunay([(p[0], p[1]) for p in pts])
        self.cell = {}
        for t in self.t:
            xs = [pts[i][0] for i in t]
            ys = [pts[i][1] for i in t]
            for i in range(int(min(xs) // 5), int(max(xs) // 5) + 1):
                for j in range(int(min(ys) // 5), int(max(ys) // 5) + 1):
                    self.cell.setdefault((i, j), []).append(t)

    def z(self, x, y):
        P = self.p
        for (ia, ib, ic) in self.cell.get((int(x // 5), int(y // 5)), ()):
            a, b, c = P[ia], P[ib], P[ic]
            det = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
            if abs(det) < 1e-12:
                continue
            l1 = ((b[1] - c[1]) * (x - c[0]) + (c[0] - b[0]) * (y - c[1])) / det
            l2 = ((c[1] - a[1]) * (x - c[0]) + (a[0] - c[0]) * (y - c[1])) / det
            l3 = 1.0 - l1 - l2
            if min(l1, l2, l3) >= -1e-9:
                return l1 * a[2] + l2 * b[2] + l3 * c[2]
        return None


def fill_gaps(Z):
    """stations outside the TIN take the nearest station's height; None when nothing was cut"""
    idx = [i for i, z in enumerate(Z) if z is not None]
    if not idx:
        return None, len(Z)
    out = list(Z)
    miss = 0
    for i, z in enumerate(Z):
        if z is None:
            j = min(idx, key=lambda k: abs(k - i))
            out[i] = Z[j]
            miss += 1
    return out, miss


# ================================================================ the stream centreline, slope and levels
def load_centreline(log):
    p = os.path.join(DATA_DIR, "selinos_centreline.json")
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    CL = [tuple(q) for q in d["points"]]
    cum = [0.0]
    for a, b in zip(CL[:-1], CL[1:]):
        cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    log.append(u"centreline: %d points, %.0f m (%s)" % (len(CL), cum[-1], p))
    return CL, cum


def cl_project(CL, cum, x, y):
    """(distance, chainage, unit direction) of the nearest centreline point"""
    best = None
    for i in range(len(CL) - 1):
        ax, ay = CL[i]
        bx, by = CL[i + 1]
        ex, ey = bx - ax, by - ay
        l2 = ex * ex + ey * ey
        t = 0.0 if l2 < 1e-12 else max(0.0, min(1.0, ((x - ax) * ex + (y - ay) * ey) / l2))
        d = math.hypot(ax + t * ex - x, ay + t * ey - y)
        if best is None or d < best[0]:
            L = math.sqrt(l2) or 1.0
            best = (d, cum[i] + t * L, (ex / L, ey / L))
    return best


def seg_cross(p, q, a, b):
    """parameter t on p-q where it crosses a-b, or None"""
    rx, ry = q[0] - p[0], q[1] - p[1]
    sx, sy = b[0] - a[0], b[1] - a[1]
    den = rx * sy - ry * sx
    if abs(den) < 1e-12:
        return None
    t = ((a[0] - p[0]) * sy - (a[1] - p[1]) * sx) / den
    u = ((a[0] - p[0]) * ry - (a[1] - p[1]) * rx) / den
    return t if (0.0 <= t <= 1.0 and 0.0 <= u <= 1.0) else None


def stream_crossing(CL, A, B):
    """distance along A-B where the line crosses the centreline (the first crossing), or None"""
    L = math.hypot(B[0] - A[0], B[1] - A[1])
    best = None
    for a, b in zip(CL[:-1], CL[1:]):
        t = seg_cross(A, B, a, b)
        if t is not None and (best is None or t < best):
            best = t
    return None if best is None else best * L


def bed_slope(CL, cum, ch0, survey, log):
    """research method: lowest bed height per 25 m bin within 300 m of chainage ch0 (stream-line vertices within 30 m
    of the centreline, tacheometric points within 12 m), straight line fitted; (slope, bins) or (None, bins)"""
    keep = [i for i in range(len(CL) - 1) if cum[i + 1] >= ch0 - SLOPE_HALF - 60.0 and cum[i] <= ch0 + SLOPE_HALF + 60.0]
    CL = CL[keep[0]:keep[-1] + 2]
    cum = cum[keep[0]:keep[-1] + 2]
    bed = []
    for pl in survey.get("HIDRO_DERE_SULU", []):
        for p in pl:
            if p[2] > 1.0:
                d, s, _ = cl_project(CL, cum, p[0], p[1])
                if d < 30.0 and abs(s - ch0) < SLOPE_HALF:
                    bed.append((s, p[2]))
    for pl in survey.get("NOKTA_TAKEOMETRI", []):
        p = pl[0]
        if p[2] > 1.0:
            d, s, _ = cl_project(CL, cum, p[0], p[1])
            if d < 12.0 and abs(s - ch0) < SLOPE_HALF:
                bed.append((s, p[2]))
    bx, bz = [], []
    a = ch0 - SLOPE_HALF
    while a < ch0 + SLOPE_HALF:
        inb = [q for q in bed if a <= q[0] < a + SLOPE_BIN]
        if inb:
            q = min(inb, key=lambda r: r[1])
            bx.append(q[0])
            bz.append(q[1])
        a += SLOPE_BIN
    if len(bx) < 4:
        log.append(u"FLAG slope: only %d bed bins within %.0f m (need 4): no water levels on this cut" % (
            len(bx), SLOPE_HALF))
        return None, len(bx)
    n = float(len(bx))
    mx, mz = sum(bx) / n, sum(bz) / n
    sxx = sum((x - mx) ** 2 for x in bx)
    sxz = sum((x - mx) * (z - mz) for x, z in zip(bx, bz))
    return -sxz / sxx, len(bx)


def hydraulics(u, z, h):
    """area and wetted perimeter of the water at level h connected to the lowest ground within CHANNEL_M of u = 0
    (research levels.py: walls at the cut ends when the water spills past them)"""
    mid = [i for i in range(len(u)) if abs(u[i]) <= CHANNEL_M]
    i0 = min(mid, key=lambda i: z[i])
    a = i0
    while a > 0 and z[a - 1] < h:
        a -= 1
    b = i0
    while b < len(z) - 1 and z[b + 1] < h:
        b += 1
    spill = a == 0 or b == len(z) - 1
    A = Pw = 0.0
    for k in range(max(a - 1, 0), min(b + 1, len(z) - 1)):
        u1, u2, z1, z2 = u[k], u[k + 1], z[k], z[k + 1]
        d1, d2 = h - z1, h - z2
        if d1 <= 0 and d2 <= 0:
            continue
        if d1 > 0 and d2 > 0:
            A += (d1 + d2) / 2 * (u2 - u1)
            Pw += math.hypot(u2 - u1, z2 - z1)
        else:
            t = d1 / (d1 - d2)
            if d1 > 0:
                A += d1 * t * (u2 - u1) / 2
                Pw += math.hypot(t * (u2 - u1), t * (z2 - z1))
            else:
                A += d2 * (1 - t) * (u2 - u1) / 2
                Pw += math.hypot((1 - t) * (u2 - u1), (1 - t) * (z2 - z1))
    if spill:
        Pw += max(h - z[a], 0) + max(h - z[b], 0)
    return A, Pw, spill


def level_for(u, z, Q, slope):
    """Manning normal depth: the level h at which (1/n) A R^(2/3) S^(1/2) = Q (bisection, 60 steps)"""
    zb = min(z[i] for i in range(len(u)) if abs(u[i]) <= CHANNEL_M)
    lo, hi = zb, zb + 15.0
    spill = False
    for _ in range(60):
        h = (lo + hi) / 2
        A, Pw, spill = hydraulics(u, z, h)
        q = A * (A / Pw) ** (2.0 / 3.0) * math.sqrt(slope) / N_MANNING if Pw > 0 else 0.0
        if q < Q:
            lo = h
        else:
            hi = h
    return hi, spill


# ================================================================ one cut
class Cut(object):
    """one section line: survey-coordinate ends A, B; s = metres from A along A-B; drawn left (A) to right (B)"""

    def __init__(self, n, A, B, src, name=None):
        self.n, self.A, self.B, self.src = n, A, B, src
        self.name = name or u"L%d" % n
        self.survey = None
        self.bld, self.roads, self.streets = [], [], []
        self.L = math.hypot(B[0] - A[0], B[1] - A[1])
        self.u = ((B[0] - A[0]) / self.L, (B[1] - A[1]) / self.L)
        self.is_s4 = False
        self.notes = []

    def xy(self, s):
        return (self.A[0] + self.u[0] * s, self.A[1] + self.u[1] * s)

    def su(self, x, y):
        dx, dy = x - self.A[0], y - self.A[1]
        return dx * self.u[0] + dy * self.u[1], -dx * self.u[1] + dy * self.u[0]


def compass(dx, dy):
    a = (math.degrees(math.atan2(dx, dy)) + 360.0) % 360.0          # 0 = north (survey y), clockwise
    return ("north", "north-east", "east", "south-east", "south", "south-west", "west",
            "north-west")[int((a + 22.5) // 45) % 8]


def build_cut(C, CL, cum, E, log, BM=None):
    """C.prof (s0, DS, Z), C.window, C.s_th, C.z_th, C.levels, C.marks, C.trees"""
    lg = C.notes
    x_c = stream_crossing(CL, C.A, C.B)
    C.cross = x_c
    if C.is_s4:
        w0, w1 = S4_WINDOW
    elif C.L > MAX_LEN_M and x_c is not None:
        w0, w1 = max(0.0, x_c - MAX_LEN_M / 2), min(C.L, x_c + MAX_LEN_M / 2)
        lg.append(u"line %d (%s) is %.0f m long: drawn %.0f-%.0f m (%.0f m either side of the stream)" % (
            C.n, C.name, C.L, w0, w1, MAX_LEN_M / 2))
    elif C.L > MAX_LEN_M:
        w0, w1 = 0.0, MAX_LEN_M
        lg.append(u"FLAG line %d is %.0f m long and does not cross the stream: its first %.0f m drawn" % (
            C.n, C.L, MAX_LEN_M))
    else:
        w0, w1 = 0.0, C.L
    C.window = (w0, w1)
    h0, h1 = (x_c - HYD_HALF, x_c + HYD_HALF) if x_c is not None else (w0, w1)
    a0, a1 = min(w0, h0), max(w1, h1)
    pa, pb = C.xy(a0), C.xy(a1)
    pad = max(CORRIDOR_STEPS[-1], SLOPE_HALF + 20.0 if x_c is not None else 0.0)
    box = (min(pa[0], pb[0]) - pad, min(pa[1], pb[1]) - pad, max(pa[0], pb[0]) + pad, max(pa[1], pb[1]) + pad)
    survey = C.survey if getattr(C, "survey", None) is not None else read_survey(box, log)
    C.survey = survey
    # ---- TIN of the heights in the corridor
    ox, oy = C.A
    for cor in CORRIDOR_STEPS:
        pts = {}
        count = {}
        for name in SURVEY_LAYERS:
            for pl in survey.get(name, []):
                for p in pl:
                    if p[2] <= 1.0:
                        continue
                    s, off = C.su(p[0], p[1])
                    if a0 - 5.0 <= s <= a1 + 5.0 and abs(off) <= cor:
                        pts[(round(p[0] - ox, 2), round(p[1] - oy, 2))] = p[2]
                        count[name] = count.get(name, 0) + 1
        if len(pts) >= HEIGHTS_WANT:
            break
    if len(pts) < HEIGHTS_MIN:
        raise RuntimeError(u"line %d: only %d survey heights within %.0f m: is Bergama_Altlik.3dm open and the line "
                           u"on the site?" % (C.n, len(pts), cor))
    if len(pts) < HEIGHTS_WANT or cor > CORRIDOR_STEPS[0]:
        log.append(u"FLAG line %d: thin ground: %d survey heights within %.0f m of the line (%s); the ground line "
                   u"between them is a straight fill, not surveyed" % (C.n, len(pts), cor, u", ".join(
                       u"%s %d" % kv for kv in sorted(count.items()))))
    keys = list(pts)
    tin = Tin([(k[0], k[1], pts[k]) for k in keys])
    lg.append(u"TIN line %d: %d heights (%s), %d triangles" % (C.n, len(pts), u", ".join(
        u"%s %d" % kv for kv in sorted(count.items())), len(tin.t)))

    def cut(s0, s1, ds):
        n = int(round((s1 - s0) / ds))
        Z = []
        for i in range(n + 1):
            x, y = C.xy(s0 + i * ds)
            Z.append(tin.z(x - ox, y - oy))
        return fill_gaps(Z)
    Z, miss = cut(w0, w1, DS)
    if Z is None:
        raise RuntimeError(u"line %d: the TIN does not reach the line" % C.n)
    if miss:
        lg.append(u"FLAG line %d: %d of %d stations outside the survey TIN took the nearest height" % (C.n, miss, len(Z)))
    C.prof = (w0, DS, Z)
    if C.is_s4:
        pz = E["PROFILE_Z"]
        d = [abs(E["prof_z"](C.prof, E["PROFILE_S0"] + i * E["PROFILE_DS"]) - pz[i]) for i in range(len(pz))
             if w0 <= E["PROFILE_S0"] + i * E["PROFILE_DS"] <= w1]
        lg.append(u"S4 check: the re-cut differs from the engine's embedded profile by at most %.3f m" % max(d))
    # ---- bed low point, slope, levels
    C.levels, C.slope = {}, None
    rng_ = [i for i in range(len(Z)) if x_c is None or abs(w0 + i * DS - x_c) <= CHANNEL_M]
    i_th = min(rng_ or range(len(Z)), key=lambda i: Z[i])
    C.s_th, C.z_th = w0 + i_th * DS, Z[i_th]
    if x_c is not None and abs(C.s_th - x_c) > 15.0:   # v1.29.1 (node thread: N2-A bed 37 m off the centreline)
        lg.append(u"FLAG line %d: the survey bed low point (s %.1f) is %.0f m from the stream centreline crossing (s %.1f); "
                  u"the channel follows the survey, the masterplan follows the centreline" % (C.n, C.s_th, abs(C.s_th - x_c), x_c))
    if C.is_s4:                                     # the engine's surveyed low point and strip, so S4 stays 1:1
        lg.append(u"S4 bed low point: re-cut s %.2f %+.2f, engine s %.2f %+.2f (only this low point is the engine's; the rest is drawn from the B19 masterplan)" % (
            C.s_th, C.z_th, E["_THALWEG0"][0], E["_THALWEG0"][1]))
        # v1.17.4 (seasons thread: S4's strip / bed came from N6-B): draw_cut overwrites E["THALWEG"] per cut, so
        # the engine's own S4 low point is kept apart at load
        C.s_th, C.z_th = E["_THALWEG0"]
    if x_c is None:
        lg.append(u"FLAG line %d does not cross the stream centreline: no water levels, no strip" % C.n)
        C.look = compass(-C.u[1], C.u[0])
    else:
        xc, yc = C.xy(x_c)
        d_, ch, t_ = cl_project(CL, cum, xc, yc)
        ang = math.degrees(math.acos(min(1.0, abs(C.u[0] * t_[0] + C.u[1] * t_[1]))))
        C.angle = 90.0 - ang
        if abs(C.angle) > OBLIQUE_DEG:
            lg.append(u"FLAG line %d crosses the stream %.0f deg off square: the flow area is overstated, the levels "
                      u"low" % (C.n, abs(C.angle)))
        lk = (-C.u[1], C.u[0])
        dot = lk[0] * t_[0] + lk[1] * t_[1]
        C.look = compass(*lk) + (u" (downstream)" if dot > 0.7 else u" (upstream)" if dot < -0.7 else u"")
        S, nb = bed_slope(CL, cum, ch, survey, lg)
        C.slope, C.chainage = S, ch
        if S is not None and S > 0:
            hu, hz = [], []
            Zh, _m = cut(h0, h1, HYD_DS)
            for i, z in enumerate(Zh):
                hu.append(h0 + i * HYD_DS - x_c)
                hz.append(z)
            zb = min(hz[i] for i in range(len(hu)) if abs(hu[i]) <= CHANNEL_M)
            for key, Q in (("q100", Q100), ("q500", Q500)):
                h, sp = level_for(hu, hz, Q, S)
                C.levels[key] = (h, sp)
            for sea, ws in SEASON_WATER.items():
                for Q, fill, lab in ws:
                    h, sp = level_for(hu, hz, Q, S)
                    C.levels[(sea, Q)] = (h, sp)
            lg.append(u"levels line %d: chainage %.0f m, bed slope %.2f %% (%d bins), bed %+.2f; Q100 %+.2f, Q500 "
                      u"%+.2f (Manning n %.3f)%s" % (
                          C.n, ch, 100 * S, nb, zb, C.levels["q100"][0], C.levels["q500"][0], N_MANNING,
                          u"; Q500 spills past the 400 m cut" if C.levels["q500"][1] else u""))
        elif S is not None:
            lg.append(u"FLAG line %d: the fitted bed rises downstream (%.2f %%): no water levels" % (C.n, 100 * S))
    # ---- survey crossings and trees
    C.marks = []
    for name, what in MARK_LAYERS.items():
        for pl in survey.get(name, []):
            for a, b in zip(pl[:-1], pl[1:]):
                t = seg_cross(C.A, C.B, a, b)
                if t is not None and w0 <= t * C.L <= w1:
                    C.marks.append((t * C.L, what))
    C.marks.sort()
    C.trees = []
    for name in TREE_LAYERS:
        for pl in survey.get(name, []):
            p = pl[0]
            s, off = C.su(p[0], p[1])
            if w0 + 2.0 <= s <= w1 - 2.0 and abs(off) <= TREE_NEAR_M:
                C.trees.append(s)
    C.trees.sort()
    C.trees_back_xy = []                               # v1.20: survey trees behind the cut (s, distance, x, y)
    for name in TREE_LAYERS:
        for pl in survey.get(name, []):
            p = pl[0]
            s, off = C.su(p[0], p[1])
            if w0 + 1.0 <= s <= w1 - 1.0 and TREE_NEAR_M < off <= TREE_BACK_M:
                C.trees_back_xy.append((s, off, p[0], p[1]))
    lg.append(u"survey on line %d: %s; trees within %.0f m: %d" % (C.n, u", ".join(
        u"%s %d" % (w, sum(1 for m in C.marks if m[1] == w)) for w in sorted(set(MARK_LAYERS.values()))),
        TREE_NEAR_M, len(C.trees)))
    context_for(C, BM, tin, ox, oy, lg)
    if ac_background(C.name, C.L) is None:                   # v1.27: houses come only from Archicad (v1.27.1: an empty file = no houses there)
        lg.append(u"FLAG line %d (%s): no Archicad background yet: no houses drawn on this cut" % (C.n, C.name))


# ================================================================ the section surface and its contents
class Sec(object):
    """the engine's Sec, for one cut: s (m from A) -> page x, level -> page y; d holds the planting and design lists"""

    def __init__(self, E, C, sea):
        self.E, self.C = E, C
        w0, w1 = C.window
        self.prof = C.prof
        self.dir = 1.0
        self.lo, self.hi = w0, w1
        self.X0 = self.Y0 = 0.0
        self.K = E["K"]
        self.has_strip = C.cross is not None and C.slope is not None
        self.strip = (C.s_th - STRIP_W / 2, C.s_th + STRIP_W / 2, STRIP_D) if self.has_strip else (-1e9, -1e9, 0.0)
        self.zb = C.z_th - STRIP_D - 1.9
        self.d = dict(key=u"sfl%d" % C.n, s_from=w0, s_to=w1, grass=[], lavender=[], iris=[], reeds=[], shrubs=[],
                      trees=[], callouts=[], rails=[], regrade=(w1, w1))
        self.banks = []          # engine Sec objects of the S4 design banks
        self.flats = []
        self.steps = []
        self.design = []         # (s from, s to) under the design
        left, right = [], []
        if C.is_s4 and not S4_FROM_B19:
            for dsec in E["SECTIONS"]:
                b = E["Sec"](dsec, self.prof)
                self.banks.append(b)
                ra, rb = dsec["regrade"]
                k = [i for i, p in enumerate(b.V) if abs(p[0] - rb) < 1e-9][0]
                pts = b.V[:k + 1]
                if b.dir < 0:
                    right = pts[::-1]
                else:
                    left = pts
                self.design.append(tuple(sorted((dsec["s_from"], rb))))
                for kk in ("grass", "lavender", "iris", "reeds", "shrubs", "trees", "callouts"):
                    self.d[kk] += list(dsec.get(kk, []))
                self.flats += [(sa, sb, z, mat, lab) for sa, sb, z, mat, lab in b.flats]
            self.d["rails"] = [(s, side) for dsec in E["SECTIONS"] for s, side in dsec["rails"]]
            self.d["balcony"] = E["SECTIONS"][1].get("balcony")
            self.d["pergola"] = E["SECTIONS"][1].get("pergola")
        self.V = self._surface(left, right)
        self.walled = None
        self.roads = list(C.roads)
        self.channel = (C.s_th, C.s_th)
        if not C.is_s4 and WALL_BED[0] <= C.z_th <= WALL_BED[1]:
            self._wall_channel()
        mp_surface(self)                                    # v1.8: the plan's terraces become the ground
        if not C.is_s4 or S4_FROM_B19:
            self._rule_planting(sea)
        mp_planting(self)

    def _wall_channel(self):
        """v1.6.2: the walled town reach as a walled channel (run 2 drew 0.6 m posts standing on the pre-wall survey
        slope): on each side the wall stands where the survey ground first reaches the wall top (bed + WALL_H_M, REPORT
        s.2) within WALL_SEARCH_M of the bed low point, else DSI_BED_W / 2 from it; between the walls a flat bed at the
        bed level (the summer strip kept); the wall face is vertical from the bed to max(ground there, wall top)"""
        C = self.C
        zt, top = C.z_th, C.z_th + WALL_H_M
        ends = []
        for sg in (-1.0, 1.0):
            e = None
            d = 0.5
            while d <= WALL_SEARCH_M:
                x = C.s_th + sg * d
                if not (self.lo < x < self.hi):
                    break
                if self.ex(x) >= top - 0.5:
                    e = x
                    break
                d += 0.5
            ends.append(e if e is not None else C.s_th + sg * DSI_BED_W / 2.0)
        sL, sR = ends
        if sR - sL < 6.0:
            return
        sa, sb, dep = self.strip
        V = [p for p in self.V if p[0] < sL - 1e-6]
        V += [(sL, self.ex(sL)), (sL, zt)]
        for p in self.V:
            if sL < p[0] < sR and sa - 1e-6 <= p[0] <= sb + 1e-6:
                V.append(p)                                  # the summer strip in the bed
        V += [(sR, zt), (sR, self.ex(sR))]
        V += [p for p in self.V if p[0] > sR + 1e-6]
        self.V = V
        self._xs = None
        # v1.10 (Aras 16:23 "u sure that there is walls like that"): the wall retains the bank, so its top is the bank
        # ground beside it (plus a parapet when drawn), never bed + 5 m standing free above a lower bank
        self.walled = (sL, sR, self.ex(sL - WALL_T_M - 0.5), self.ex(sR + WALL_T_M + 0.5))
        C.notes.append(u"line %d: walled channel s %.1f-%.1f m (%.1f m wide), bed %+.2f, wall tops %+.2f / %+.2f "
                       u"(REPORT s.2: 5.0 m above the bed; the survey bank here is pre-wall)" % (
                           C.n, sL, sR, sR - sL, zt, self.walled[2], self.walled[3]))

    def X(self, s):
        return self.X0 + (s - self.lo) * self.K

    def Y(self, z):
        return self.Y0 + (z - self.zb) * self.K

    def P(self, s, z):
        return (self.X(s), self.Y(z))

    def ex(self, s):
        return self.E["prof_z"](self.prof, s)

    def _surface(self, left, right):
        w0, w1 = self.lo, self.hi
        a = left[-1][0] if left else w0
        b = right[0][0] if right else w1
        mid = []
        n = int(round((b - a) / DS))
        for i in range(n + 1):
            mid.append((a + (b - a) * i / max(n, 1), None))
        V = list(left)
        sa, sb, dep = self.strip
        for s, _ in mid:
            if sa < s < sb:
                continue
            if left and s <= a + 1e-9:
                continue
            if right and s >= b - 1e-9:
                continue
            if V and V[-1][0] < sa and s > sb:            # the strip: a 4 m low-flow channel 0.30 m into the bed
                zt = self.C.z_th
                V += [(sa, self.ex(sa)), (sa, zt - dep), (sb, zt - dep), (sb, self.ex(sb))]
            V.append((s, self.ex(s)))
        V += list(right)
        return V

    def surf(self, s):
        V = self.V
        best = None
        xs = getattr(self, "_xs", None)
        if xs is None:
            xs = [p[0] for p in V]
            self._xs = xs = xs if all(xs[i] <= xs[i + 1] + 1e-9 for i in range(len(xs) - 1)) else False
        if xs:
            i0 = max(0, bisect.bisect_left(xs, s - 1e-6) - 2)
            i1 = min(len(V) - 1, bisect.bisect_right(xs, s + 1e-6) + 1)
        else:
            i0, i1 = 0, len(V) - 1
        for i in range(i0, i1):
            a, b = V[i], V[i + 1]
            lo_, hi_ = sorted((a[0], b[0]))
            if lo_ - 1e-9 <= s <= hi_ + 1e-9:
                if abs(b[0] - a[0]) < 1e-9:
                    z = min(a[1], b[1])
                else:
                    z = a[1] + (b[1] - a[1]) * (s - a[0]) / (b[0] - a[0])
                best = z if best is None else min(best, z)
        return best if best is not None else self.ex(s)

    def built(self, s):
        """on a road or inside a building the line cuts: no planting, no people"""
        C = self.C
        return (any(a <= s <= b for a, b in C.roads) or any(t[4] and t[0] <= s <= t[1] for t in C.bld)
                or any(a <= s <= b for a, b in getattr(C, "mp_hard", ())))

    def _rule_planting(self, sea):
        """design intention (ours): reeds and iris on the wet bed (up to WET_BAND_M above the bed, never in the strip),
        meadow grass above it; survey trees on ground above Q100 (drawn at the engine's plane size)"""
        C, d = self.C, self.d
        wet = C.z_th + WET_BAND_M
        sa, sb, _ = self.strip
        # v1.6 (fix 1): wet planting only in the channel = the one run of ground within WET_BAND_M of the bed that holds
        # the bed low point (v1.4 put reeds on every low flat, N3-A / N3-B across 200 m, over roads and in front of houses)
        ch0 = ch1 = C.s_th
        while ch0 - 0.5 >= self.lo and self.surf(ch0 - 0.5) <= wet and C.s_th - ch0 < CHANNEL_M:
            ch0 -= 0.5
        while ch1 + 0.5 <= self.hi and self.surf(ch1 + 0.5) <= wet and ch1 - C.s_th < CHANNEL_M:
            ch1 += 0.5
        if WALL_BED[0] <= C.z_th <= WALL_BED[1] and ch1 - ch0 > WALL_MAX_W:
            # v1.6.1: in the walled town reach a low flat wider than WALL_MAX_W is not the channel (run 2: walls 62 m
            # and 80 m apart on N3-A / N3-B): the channel is the DSI 20 m bed (SYGM 2019 summary p.75, measure 155:
            # 20 m x 3.00 m planned channel; bank-depth REPORT s.1) centred on the bed low point
            ch0, ch1 = C.s_th - DSI_BED_W / 2.0, C.s_th + DSI_BED_W / 2.0
            C.notes.append(u"line %d: the low flat at the bed is wider than %.0f m: channel = the DSI %.0f m bed" % (
                C.n, WALL_MAX_W, DSI_BED_W))
        if self.walled:
            ch0, ch1 = self.walled[0], self.walled[1]
        self.channel = (ch0, ch1)
        # v1.6.7 (check of run 4: N3-A / N5-A roads ran down the bank into the bed): no road surface in the channel
        gaps = [(ch0 - WALL_T_M - 0.5, ch1 + WALL_T_M + 0.5)] + [(t[0], t[1]) for t in C.bld if t[4]]
        rd = list(C.roads)
        for g0, g1 in gaps:                               # v1.6.10: and clear of the walls and the cut buildings
            rd = [r for a, b in rd for r in ((a, min(b, g0)), (max(a, g1), b)) if r[1] - r[0] > 0.5]
        self.roads = rd
        runs, cur, kind = [], None, None
        s = self.lo
        while s <= self.hi + 1e-9:
            if sa - 0.4 <= s <= sb + 0.4 or self.built(s):
                k = None
            else:
                k = "wet" if (self.surf(s) <= wet and ch0 <= s <= ch1) else "dry"
            if k != kind:
                if cur is not None and kind is not None:
                    runs.append((cur, s, kind))
                cur, kind = s, k
            s += 0.5
        if kind is not None and cur is not None:
            runs.append((cur, self.hi, kind))
        n_r = 0
        for a, b, k in runs:
            if b - a < 0.8:
                continue
            if k == "dry":
                d["grass"].append((a, b))
                continue
            x = a
            while x < b - 0.5:                                 # reeds 3 m, iris 1.2 m, alternating
                y = min(b, x + (3.0 if n_r % 2 == 0 else 1.2))
                if n_r % 2 == 0:
                    d["reeds"].append((x, y, 2.0))
                else:
                    d["iris"].append((x, y))
                n_r += 1
                x = y
        q100 = C.levels.get("q100", (None,))[0]
        wet = []
        for s in C.trees:
            if q100 is None or self.surf(s) >= q100:
                d["trees"].append((s, 3.9, 7.5, "plane"))
            else:
                wet.append(s)
        if wet:                                           # v1.4: one log line per section, not one per tree
            C.notes.append(u"line %d: %d survey tree(s) not drawn, they stand below Q100 (at s %s m)" % (
                C.n, len(wet), u", ".join(u"%.1f" % s for s in wet)))
        if d["reeds"]:                                    # v1.6.7: away from the strip's label (same x lost one)
            # v1.6.13: anchored at the reed end farthest from the strip (its label sat on the strip's: N3-B, N5-A)
            r_s = max((x for r in d["reeds"] for x in (r[0] + 0.3, r[1] - 0.3)), key=lambda x: abs(x - C.s_th))
            d["callouts"].append((r_s, None, u"Common reed (Kamış)"))
        if d["iris"]:
            far = [C.s_th] + [c[0] for c in d["callouts"]]
            i_s = max((x for r in d["iris"] for x in (r[0] + 0.2, r[1] - 0.2)),
                      key=lambda x: min(abs(x - f) for f in far))
            d["callouts"].append((i_s, None, u"Yellow flag iris (Sarı süsen)"))
        if d["grass"]:
            g0 = max(d["grass"], key=lambda r: abs(r[1] - r[0]))
            d["callouts"].append(((g0[0] + g0[1]) / 2, None, u"Meadow, native grasses"))
        for s, _r, _h, _k in d["trees"][:3]:
            d["callouts"].append((s, None, u"Tree"))
        if self.has_strip:
            d["callouts"].append((C.s_th, None, u"Summer water strip 4.0 × 0.30 m"))
        for a, b in self.roads:
            d["callouts"].append(((a + b) / 2, None, u"Road"))
        for x in C.streets:
            d["callouts"].append((x, None, u"Street"))
        cut_ = [(t[0], t[1]) for t in C.bld if t[4]]
        back = [t for t in C.bld if not t[4] and not (t[0] < ch1 + 1.0 and t[1] > ch0 - 1.0)
                and sum(max(0.0, min(t[1], y) - max(t[0], x)) for x, y in cut_) <= 0.5 * (t[1] - t[0])]
        if back:
            t = max(back, key=lambda t: t[1] - t[0])
            d["callouts"].append(((t[0] + t[1]) / 2, (t[2] if t[2] is not None else self.ex((t[0] + t[1]) / 2)) + t[3],
                                  u"Buildings behind the cut"))
        for t in C.bld:
            if t[4]:
                d["callouts"].append(((t[0] + t[1]) / 2, self.ex((t[0] + t[1]) / 2) + t[3],
                                      u"Building, %d floor%s" % (t[6], u"" if t[6] == 1 else u"s") if t[6] and t[6] > 0 else u"Building"))


class _Bank(object):
    """an S4 design bank seen through the combined section: its own flats, steps, stair, dir and regrade, the
    combined surface and page mapping"""

    def __init__(self, S, b):
        self.S, self.b = S, b
        self.flats, self.steps, self.dir, self.d = b.flats, b.steps, b.dir, b.d
        self.stair = getattr(b, "stair", None)

    def __getattr__(self, k):
        return getattr(self.S, k)


def people_for(S, sea_key, E):
    """S4: the engine's people of both banks for the season; other cuts: walkers on dry, gentle ground every ~9 m"""
    if S.C.is_s4 and not S4_FROM_B19:
        for dsea in E["SEASONS"]:
            if dsea["key"] == sea_key:
                return (list(dsea["people"].get("1", [])) + list(dsea["people"].get("2", [])),
                        list(dsea["bikes"].get("1", [])) + list(dsea["bikes"].get("2", [])))
        return [], []
    out = []
    kinds = (0, 1, 2, 4, 3)
    s = S.lo + 4.0
    n = 0
    while s < S.hi - 4.0:
        g = S.surf(s)
        ch = getattr(S, "channel", (S.C.s_th, S.C.s_th))
        q100 = S.C.levels.get("q100", (None,))[0]
        if abs(S.surf(s + 0.5) - S.surf(s - 0.5)) < 0.25 and not any(t[4] and t[0] - 1.5 <= s <= t[1] + 1.5
                                                                     for t in S.C.bld) \
                and not ch[0] - 1.5 <= s <= ch[1] + 1.5 and (q100 is None or g >= q100):
            out.append((s, kinds[n % len(kinds)], n % 2 == 1))
            n += 1
            s += 9.0
        else:
            s += 1.0
        _ = g
    return out, []


def joined(S, z):
    """v1.6.7 (check of run 4: Q lines ran over whole banks at ground height, water past the wall): the stretch of
    the cut where water at level z stands, joined to the bed low point; a wall holds it while z is below its top"""
    C = S.C
    if S.surf(C.s_th) >= z:
        return None
    wl = getattr(S, "walled", None)
    ends = []
    for sg in (-1.0, 1.0):
        s = C.s_th
        while S.lo < s + sg * 0.1 < S.hi and S.surf(s + sg * 0.1) < z:
            if wl and z <= (wl[2] if sg < 0 else wl[3]) and not wl[0] <= s + sg * 0.1 <= wl[1]:
                break
            s += sg * 0.1
        ends.append(s)
    return ends[0], ends[1]


def joined_level(E, pg, S, z, label, dash, colour=None, fill=False, line=True):
    """the engine's level_line (and water) limited to the joined stretch: s_from / s_to and the surface held to it"""
    j = joined(S, z)
    if not j:
        return
    keep = (S.d["s_from"], S.d["s_to"], S.V, getattr(S, "_xs", None))
    S.d["s_from"], S.d["s_to"] = j
    try:
        if fill:
            S.V = [(j[0], max(S.surf(j[0]), z))] + [p for p in keep[2] if j[0] < p[0] < j[1]] + \
                  [(j[1], max(S.surf(j[1]), z))]
            S._xs = None
            E["water"](pg, S, z)
            S.V, S._xs = keep[2], keep[3]
        if line:
            if colour is None:
                E["level_line"](pg, S, z, label, dash)
            else:
                E["level_line"](pg, S, z, label, dash, colour=colour)
    finally:
        S.d["s_from"], S.d["s_to"], S.V, S._xs = keep


def season_water(C, sea):
    """[(level, filled, label, dash)] of the season on this cut"""
    out = []
    for Q, fill, lab in SEASON_WATER[sea]:
        lv = C.levels.get((sea, Q))
        if lv:
            out.append((lv[0], fill, lab % (lv[0], lv[0] - C.z_th), None if fill else [1.6, 0.6, 0.3, 0.6]))
    return out


def _in_ring(x, y, ring):
    """v1.16: point in polygon (even-odd)"""
    inside = False
    for i in range(len(ring)):
        (ax, ay), (bx, by) = ring[i - 1], ring[i]
        if (ay > y) != (by > y) and x < ax + (y - ay) * (bx - ax) / (by - ay):
            inside = not inside
    return inside


def _clip_x(ring, x0, x1):
    """a closed ring cut to x0 <= x <= x1 (Sutherland-Hodgman, two vertical edges)"""
    for edge, inside in ((x0, lambda q: q[0] >= x0), (x1, lambda q: q[0] <= x1)):
        if not ring:
            return []
        out = []
        for i, q in enumerate(ring):
            p_ = ring[i - 1]
            if inside(q):
                if not inside(p_):
                    t = (edge - p_[0]) / (q[0] - p_[0])
                    out.append((edge, p_[1] + (q[1] - p_[1]) * t))
                out.append(q)
            elif inside(p_):
                t = (edge - p_[0]) / (q[0] - p_[0])
                out.append((edge, p_[1] + (q[1] - p_[1]) * t))
        ring = out
    return ring


def draw_cut(E, C, sea, den, x_left, y_top, with_text=True):
    """one season of one cut on a new engine Page at 1:den; returns (page, S, bottom y)"""
    E["K"] = 1000.0 / den
    _ENGINE_K[0] = E["K"]
    E["SEA"] = dict(E["SEASON_LOOK"][sea])
    S = Sec(E, C, sea)
    E["STRIP"] = S.strip if S.has_strip else (-1e9, -1e9, 0.0)
    E["THALWEG"] = (C.s_th, C.z_th)
    pg = E["Page"](u"sfl%d_%s" % (C.n, sea), u"")
    d = S.d
    size = 2.65
    K = E["K"]
    q100 = C.levels.get("q100", (None,))[0]
    q500 = C.levels.get("q500", (None,))[0]
    tops = [S.surf(t[0]) + t[2] for t in d["trees"]] + [max(z for _, z in S.V) + 1.9]
    tops += [(t[2] if t[2] is not None else S.ex((t[0] + t[1]) / 2)) + t[3] + 0.5 for t in C.bld]
    if d.get("pergola"):
        tops.append(E["DRY"] + max(p[2] for p in d["pergola"]["plates"]) + 0.1)
    tops += [(t[2] if t[2] is not None else S.ex((t[0] + t[1]) / 2)) + t[3] + roof_rise(t[1] - t[0], t[6]) + 0.5
             for t in C.bld if not t[4]]
    tops += [max(t[2] if t[2] is not None else -99.0, S.ex(t[0])) + t[3] + 0.3          # v1.20: trees behind
             for t in getattr(C, "trees_back", []) if S.lo <= t[0] <= S.hi]
    z_top = max(tops) + SKY_ABOVE_M
    S.z_top_ = z_top                                    # v1.24: the bands behind stop under the frame top
    S.X0 = x_left
    # v1.6.13: callouts whose anchors lie closer than 8 mm keep the first in importance order (strip, reed, iris,
    # buildings, the rest); a merged two-name label ran over its row (N3-B)
    pri = tuple(MP_LABEL.values()) + (u"Summer water", u"Common reed", u"Yellow flag", u"Building")   # v1.11: the
    #                                                   masterplan's proposals named first
    items = []
    for s_, z_, t_ in sorted(d["callouts"] if (with_text and CALLOUTS) else [],
                             key=lambda c: next((i for i, w in enumerate(pri) if c[2].startswith(w)), len(pri))):
        if not any(abs(s_ - o[0]) * K < 8.0 for o in items):
            items.append((s_, z_, t_))
    items.sort(key=lambda c: c[0])
    # v1.6.12: placed with 20 % wider text (the engine's text_w runs short: N3-B labels ran into each other)
    placed = E["place_labels"](S, [(S.X(s) + 0.002 * i, 0.0, txt) for i, (s, z, txt) in enumerate(items)],
                               size * 1.2) if items else []
    rows = (max(p["row"] for p in placed) + 1) if placed else 0
    gap = size * 2 * 1.25 + 3.0
    title_h = 7.0 if with_text else 0.0                # v1.16: one title line (was 16 mm), more room for the drawing
    label_h = rows * gap + (4.0 if rows else 0.0)
    S.Y0 = y_top - title_h - label_h - (z_top - S.zb) * K - (2.0 if with_text else 0.0)
    by_x = dict((round(S.X(s) + 0.002 * i, 3), (s, z)) for i, (s, z, txt) in enumerate(items))
    for p in placed:
        s, z = by_x[round(p["x"], 3)]
        p["y"] = S.Y(S.surf(s) + 0.02 if z is None else z)
    if with_text:
        pg.text(u"SECTION %s" % C.name, x_left, y_top - 4.5, 3.6, E["INK"], bold=True, layer="title")
        pg.text(u"SCALE 1:%d" % den, x_left, y_top - 11.5, 3.6, E["INK"], layer="title")
        pg.text(u"both banks · looking %s" % C.look, x_left + 30.0, y_top - 4.5, 2.0, E["INK2"], layer="title")
    # v1.6 back to front: sky and clouds, the ground behind the cut, the houses behind (far to near), then the cut
    sky(pg, S, C, z_top)
    if not getattr(C, "bands", None):                   # v1.24: the depth bands replace the single band
        back_ground(pg, S, C)
    # v1.6.7 (check of run 4): everything inside the frame; no house behind drawn over the channel (it read as
    # standing in the stream); a house behind stands at least on the cut ground in front of it (half-buried houses
    # with the road across their windows); cut buildings rise from the ground line (not from the frame bottom)
    ch = S.channel
    cuts_ = [(t[0], t[1]) for t in C.bld if t[4]]

    def _cover(a, b, spans):
        return sum(max(0.0, min(b, y) - max(a, x)) for x, y in spans) / max(b - a, 1e-6)
    # v1.6.10 (check of run 5): far to near; on the highest cut ground of its span (N1-B / N5-A windows buried on
    # slopes); none mostly behind a cut building (N5-B roof sat on a cut box)
    # v1.20: houses and trees behind drawn together, far to near
    back_ = [t for t in C.bld] + [(s_, k_, z_, h_, False, d_, -2) for s_, d_, z_, h_, k_ in getattr(C, "trees_back", [])]
    back_ += [(k_, None, None, 0.0, False, d_ + 0.01, -3) for k_, (d_, pr_) in enumerate(getattr(C, "bands", []))]
    acb = C.acb_ = ac_background(C.name, C.L)                         # v1.25: the Archicad elevations, when SectionsAC wrote them
    if acb:                                             # v1.28.5: his Archicad ground bands interleaved with ours by depth
        back_ += [(i_, None, None, 0.0, False, float(pc.get("d") or 150.0), -5) for i_, pc in enumerate(acb)
                  if pc.get("kind") == "ground"]
        back_ = sorted([t for t in back_ if t[6] in (-3, -5)], key=lambda t: -t[5]) + [(0, None, None, 0.0, False, 0.0, -4)] \
            + sorted([t for t in back_ if t[6] == -2], key=lambda t: -t[5])
    else:
        back_ = sorted(back_, key=lambda t: -t[5])
    for a, b, zb_, h, is_cut, dist, fl in back_:
        if fl == -4:                                    # v1.25: his Archicad houses behind, through the cut's map
            for pc in acb:
                if pc.get("kind") == "ground":
                    continue
                rings = [[S.P(q[0], min(q[1], getattr(S, "z_top_", q[1]))) for q in r] for r in pc.get("rings", []) if len(r) >= 2]
                if not rings:
                    continue
                col = (pc.get("colour") or H_EDGE).lstrip("#").upper()
                if len(col) == 6 and col not in AC_OURS:  # v1.29: context as ghost lines and pale fills, ours stays
                    col = _mix(col, SKY_LOW, AC_GHOST + (0.15 if pc.get("kind") == "fill" else 0.0))
                if pc.get("kind") == "fill":
                    pg.poly([r for r in rings if len(r) >= 3], fill=col, stroke=None, layer="houses behind")
                else:
                    for r in rings:
                        pg.line(r, col, float(pc.get("lw") or 0.05), layer="houses behind")
            continue
        if (fl >= 0 or (fl == -1 and acb is not None)) and not is_cut:   # v1.28.1: only houses (bands / trees stay)  # v1.27: no drawn houses behind; v1.27.1: nor the hall once Archicad has the cut
            continue
        if fl == -5:                                    # v1.28.5: an Archicad ground band (AcBuild v1.7), toned by depth
            pc = acb[a]
            f_ = 0.35 + 0.51 * min(1.0, dist / 400.0)
            rings = [[S.P(q[0], min(q[1], getattr(S, "z_top_", q[1]) - 0.5)) for q in r] for r in pc.get("rings", []) if len(r) >= 3]
            if rings:
                pg.poly(rings, fill=_mix(BAND_GROUND, SKY_LOW, f_), stroke=_mix(BAND_EDGE, SKY_LOW, f_), lw=0.05,
                        layer="ground behind")
            continue
        if fl == -3:                                    # v1.24: a ground band behind (drawn before what stands on it)
            band_behind(pg, S, C.bands[a][1], dist)
            continue
        if fl == -2:                                    # a tree behind
            if not (S.lo + 2.0 <= a <= S.hi - 2.0) or ch[0] - 1.0 < a < ch[1] + 1.0 or _cover(a - 1.0, a + 1.0, cuts_) > 0.5:
                continue
            tree_behind(pg, S, a, max(zb_ if zb_ is not None else -99.0, S.surf(a)), h, dist, b.split(u":")[-1])
            continue
        a, b = max(a, S.lo + EAVE_M), min(b, S.hi - EAVE_M)
        if a < ch[1] + 1.0 and b > ch[0] - 1.0:        # v1.19.1: trimmed to the wider bank side, not dropped
            a, b = max((a, ch[0] - 1.0), (ch[1] + 1.0, b), key=lambda t: t[1] - t[0])
            if b - a < 3.0:
                continue
        if is_cut or b - a < 0.5 or _cover(a, b, cuts_) > 0.5:
            continue
        n_ = max(2, int((b - a) / 0.5))
        # v1.6.13: on the highest cut ground of its span (lowest buried N1 houses, highest alone stood on stilts),
        # the gap below filled with the ground-behind tone as a terrace, so the house neither floats nor sinks
        gs = [(a + (b - a) * i / n_) for i in range(n_ + 1)]
        g_ = [S.surf(x) for x in gs]
        # v1.6.14: the terrace at most TERRACE_M high (N1-A grew a 7 m plinth on the steep slope)
        base = max(zb_ if zb_ is not None else -99.0, min(max(g_), min(g_) + TERRACE_M))
        if getattr(C, "bands", None) and zb_ is not None:   # v1.24: on its own survey ground among the bands
            house(pg, S, a, b, zb_, h, fl, dist)
            continue
        pg.poly([[S.P(x, min(S.surf(x), base)) for x in gs] + [S.P(b, base), S.P(a, base)]], fill=BACK_FILL, stroke=None,
                layer="ground behind")
        house(pg, S, a, b, base, h, fl, dist)
    mp_structures(pg, S, C, True)                       # v1.8: canopies / pavilions behind the cut
    done_ = []
    for a, b, zb_, h, is_cut, dist, fl in C.bld:
        a, b = max(a, S.lo), min(b, S.hi)
        if fl >= 0:  # v1.28.4: the cut hall is ours again (Archicad drew it as bare lines)                  # v1.27: cut houses from the Archicad section only (v1.27.1: the hall too)
            continue
        if is_cut and b - a > 0.3 and _cover(a, b, done_) <= 0.5:
            done_.append((a, b))
            base = min(S.ex(a), S.ex(b))
            n_ = max(2, int((b - a) / DS))
            ring = [S.P(a + (b - a) * i / n_, S.surf(a + (b - a) * i / n_)) for i in range(n_ + 1)]
            # v1.14 (Aras 21:32 "When i meant silouhettes i meant the ones like in the backgroudn"): a cut house is drawn
            # like the houses behind (wall, roof, window rows, cornice) as a quiet light elevation, its foot hidden
            # under the cut ground
            house(pg, S, a, b, base, h, fl, CUT_HOUSE_DIST_M)
            if fl == -1:                                # v1.18.2: the hall's cut wall ends in poché
                for x0_ in (a, b - RED_HALL_WALL_M):
                    pg.poly([[S.P(x0_, base - 1.0), S.P(x0_ + RED_HALL_WALL_M, base - 1.0),
                              S.P(x0_ + RED_HALL_WALL_M, base + h), S.P(x0_, base + h)]],
                            fill=RED_HALL_POCHE, stroke=None, layer="context buildings")
            pg.poly([ring + [S.P(b, base - 1.0), S.P(a, base - 1.0)]], fill=GROUND_FILL, stroke=None,
                    layer="context buildings")
    for s, r_, h, kind in d["trees"]:
        g = S.surf(s)
        if q500 is not None and g < q500 - 1e-6 and C.is_s4:
            continue
        X, Y = S.P(s, g)
        key_ = kind if kind in (u"plane", u"ash", u"stone_pine", u"olive", u"tamarisk") else "plane"   # v1.23: his species
        if not cutout(pg, key_, X, Y, h * K, int(s * 7) % 6, (int(s) % 2) == 1, "trees"):
            E["veg_tree"](pg, X, Y, h * K, 2 * r_ * K, (d["key"], round(s, 2)))
    people, bikes = people_for(S, sea, E)
    bal = d.get("balcony")
    on_bal = []
    if bal:
        lo_b, hi_b = min(bal["s0"], bal["s1"]), max(bal["s0"], bal["s1"])
        on_bal = [(p[0], 5, p[2]) for p in people if p[1] == 3 and lo_b <= p[0] <= hi_b]
        people = [p for p in people if not (p[1] == 3 and lo_b <= p[0] <= hi_b)]
    if d.get("pergola"):
        E["pergola"](pg, S, d["pergola"])
    if bal:
        E["balcony"](pg, S, bal, on_bal)
    if q500 is not None:
        joined_level(E, pg, S, q500, u"Q500 %+.2f (calculated on this cut)" % q500, [2.0, 1.0])
        joined_level(E, pg, S, q100, u"Q100 %+.2f (calculated on this cut)" % q100, [0.8, 0.8])
    sw = season_water(C, sea)
    for z, fill_, lab, dash in sw:
        if not fill_:
            joined_level(E, pg, S, z, lab, dash, colour=E["WATER_LINE"])
    ground_fill(pg, S)                                  # v1.6: solid fill (booklet p22), no stipple, no hatch
    n0 = len(pg.items)
    E["soft_ground"](pg, S)
    # v1.7 (Aras 15:28): no root hairs (fixed 1-3 mm lines, too long at node scales)
    pg.items[n0:] = [it for it in pg.items[n0:] if not (it[0] == "line" and it[-2] == "soft ground")]
    town_walls(pg, S, C)
    for b in S.banks:
        E["walls_and_slabs"](pg, _Bank(S, b))
    E["existing_ground"](pg, S)
    for a, b in S.roads:                               # the road surface on the ground line
        a, b = max(a, S.lo), min(b, S.hi)                  # v1.8: inside the frame
        if b - a < 0.2:
            continue
        n = max(2, int((b - a) / DS))
        top = [(a + (b - a) * i / n) for i in range(n + 1)]
        ring = [S.P(x, S.surf(x)) for x in top] + [S.P(x, S.surf(x) - ROAD_T) for x in reversed(top)]
        pg.poly([ring], fill=ROAD_FILL, stroke=None, layer="context roads")
    mp_ground(pg, S, C)                                 # v1.8: paving, terrace nosings, walls, boulders
    def _plants(pg_):
        for a, b in d["grass"]:
            a, b = max(a, S.lo + 0.1), min(b, S.hi - 0.1)               # v1.6.7: blades stay inside the frame
            if b > a:
                E["tufts"](pg_, S, a, b)
        for a, b in d["lavender"]:
            E["lavender"](pg_, S, a, b)
        for s, h, w in d["shrubs"]:
            E["shrub"](pg_, S, s, h, w)
        for a, b, h in d["reeds"]:
            E["reeds"](pg_, S, a, b, h)
        for a, b in d["iris"]:
            E["iris"](pg_, S, a, b)
    at_plant_scale(E, pg, S, _plants)
    filled = [w for w in sw if w[1]]
    for z, fill_, lab, dash in filled:
        joined_level(E, pg, S, z, lab, None, colour=E["FLOOD"], fill=True)
    held = STRIP_HELD[sea] and S.has_strip
    if held:
        joined_level(E, pg, S, C.z_th, u"continuous strip %+.2f, 0.30 m (design)" % C.z_th, None,
                     colour=E["FLOOD"], fill=True, line=not filled)
    wl = max([C.z_th if held else -99.0] + [w[0] for w in filled])
    mp_structures(pg, S, C, False)                      # v1.8: the plan's structures on the cut, over the water
    for s, kind, flip in people:
        g = S.surf(s)
        if g < wl + 0.02 and kind != 8:
            continue                                        # never a person in the water (Aras 31 Oct 11:28)
        if not cutout(pg, PEOPLE_KEYS[kind % len(PEOPLE_KEYS)], *S.P(s, g), h_mm=None, n=kind, flip=flip,
                      layer="people"):
            E["figure"](pg, S, s, kind, flip)
    for s, flip in bikes:
        E["bike"](pg, S, s, flip)
    for s, side in d["rails"]:
        E["handrail"](pg, S, s + side * 0.15, S.surf(s + side * 0.3))
    if with_text and placed:
        E["callouts"](pg, S, placed, S.Y(z_top) + 6.0, size)
    spread_levels(E, pg, S, short=True)
    # v1.11 (run of v1.10: a stub still ran past the right frame edge on N5-B): drawing lines cut at the frame
    x0_, x1_ = S.X(S.lo), S.X(S.hi)
    keep = ("title", "callouts", "levels", "text", "landuse", "land use")
    out_ = []
    water_rings_ = [r for it in pg.items if it[0] == "poly" and it[6] == "water" for r in it[1]]
    for it in pg.items:
        # v1.15 (review of the v1.14 PDF at 600 dpi: the stacked 0.25 mm dashed flood levels read as a row of blue
        # blobs across N2-A): dashed water levels as hairlines (DIAGRAM_STYLE v2: higher levels dashed 0.10)
        if it[0] == "line" and it[5] == "levels" and it[4]:
            it = it[:3] + (LEVEL_LW,) + it[4:]
        # v1.15.1: the 0.3 mm water surface line drawn thinner at small scales (thick blue bars on N4-A / N6-A)
        if it[0] == "line" and it[5] == "water" and it[3] >= 0.25:
            it = it[:3] + (min(it[3], 0.05 + 0.1 * S.K),) + it[4:]     # v1.16: thinner still (0.2 mm on N2-A)
        # v1.16 (600 dpi read of v1.15.2: ripples under a thin water sheet fell into the ground on N2-A): a ripple
        # stays only inside a water fill
        if it[0] == "line" and it[5] == "water" and it[3] <= 0.09 and it[2] == E["FLOOD"]:
            mx, my = (it[1][0][0] + it[1][-1][0]) / 2.0, (it[1][0][1] + it[1][-1][1]) / 2.0
            if not any(_in_ring(mx, my, r) for r in water_rings_):
                continue
        # v1.13 (Aras 21:26 "drawings flows out fix that"): fills cut at the frame too, clouds / cutouts / circles
        # that cross it left out
        if it[0] == "poly" and it[6] not in keep and not all(x0_ <= q[0] <= x1_ for r in it[1] for q in r):
            rings = [_clip_x(r, x0_, x1_) for r in it[1]]
            rings = [r for r in rings if len(r) >= 3]
            if rings:
                out_.append((it[0], rings) + tuple(it[2:]))
            continue
        if it[0] == "circle" and it[7] not in keep:
            if x0_ <= it[1] - it[3] and it[1] + it[3] <= x1_:
                out_.append(it)
            continue
        if it[0] == "image" and it[9] not in keep:
            if x0_ <= it[1] and it[1] + it[3] <= x1_:
                out_.append(it)
            continue
        if it[0] != "line" or it[5] in keep or all(x0_ <= q[0] <= x1_ for q in it[1]):
            out_.append(it)
            continue
        run_ = []
        for qa, qb in zip(it[1][:-1], it[1][1:]):
            ta, tb = 0.0, 1.0
            dx = qb[0] - qa[0]
            if abs(dx) > 1e-9:
                t0, t1 = sorted(((x0_ - qa[0]) / dx, (x1_ - qa[0]) / dx))
                ta, tb = max(0.0, t0), min(1.0, t1)
            elif not (x0_ <= qa[0] <= x1_):
                ta, tb = 1.0, 0.0
            if ta > tb:
                if len(run_) >= 2:
                    out_.append((it[0], run_) + tuple(it[2:]))
                run_ = []
                continue
            pa = (qa[0] + dx * ta, qa[1] + (qb[1] - qa[1]) * ta)
            pb = (qa[0] + dx * tb, qa[1] + (qb[1] - qa[1]) * tb)
            if not run_ or run_[-1] != pa:
                if len(run_) >= 2:
                    out_.append((it[0], run_) + tuple(it[2:]))
                run_ = [pa]
            run_.append(pb)
        if len(run_) >= 2:
            out_.append((it[0], run_) + tuple(it[2:]))
    # v1.17 (two independent reviews of v1.16: "there is no cut line"): the cut line was drawn before the ground
    # skin (grass strip, existing ground, roads, paving) and lay under it; it now goes on top of them
    skin = ("poche", "soft ground", "existing ground", "context roads", "proposal ground", "walls", "ground behind")
    cut_ = [it for it in out_ if it[0] == "line" and it[5] == "cut line"]
    rest = [it for it in out_ if not (it[0] == "line" and it[5] == "cut line")]
    lyr = lambda it: it[{"poly": 6, "line": 5, "circle": 7, "text": 8, "image": 9}.get(it[0], 0)]
    last = max([i for i, it in enumerate(rest) if lyr(it) in skin] or [len(rest) - 1])
    out_ = rest[:last + 1] + cut_ + rest[last + 1:]
    # v1.17.3 (review of v1.17.2): two dashed water levels less than 0.6 mm apart read as one smeared line: the
    # lower is left out where they overlap; the existing (pre-design) ground as a fine light dashed hairline
    lv_ = [it for it in out_ if it[0] == "line" and it[5] == "levels" and it[4] and len(it[1]) == 2]
    drop_ = set()
    for i_, p_ in enumerate(lv_):
        for q_ in lv_:
            if q_ is p_ or id(q_) in drop_:
                continue
            dy = q_[1][0][1] - p_[1][0][1]
            ov = min(max(p_[1][0][0], p_[1][1][0]), max(q_[1][0][0], q_[1][1][0])) - \
                max(min(p_[1][0][0], p_[1][1][0]), min(q_[1][0][0], q_[1][1][0]))
            if 0.0 < dy < 0.6 and ov > 0.0:
                drop_.add(id(p_))
                break
    out_ = [it for it in out_ if id(it) not in drop_]
    out_ = [(it[:2] + ("A39E95", 0.1, [0.6, 0.45]) + it[5:]) if it[0] == "line" and it[5] == "existing ground" else it
            for it in out_]
    # v1.18 (Aras 15 Nov 04:58 UTC, "All defaults are fine": orange accent on our proposals): every line and outline
    # of the plan's proposals in the accent C07A2E (behind the cut toned toward the sky), fills unchanged
    def _acc(it):
        lay = it[5] if it[0] == "line" else it[6] if it[0] == "poly" else None
        if lay not in ("proposal structures", "proposal behind", "proposal ground"):
            return it
        col = ACCENT if lay != "proposal behind" else _mix(ACCENT, SKY_LOW, 0.35)
        if it[0] == "line":
            return it[:2] + (col,) + it[3:]
        return it[:3] + (col,) + it[4:] if it[3] else it
    out_ = [_acc(it) for it in out_]
    pg.items[:] = out_
    y_band = S.Y(S.zb) - 3.0
    if with_text:
        landuse_band(pg, S, y_band - LU_H, LU_H)          # v1.6: the land-use band of the 27 Oct site board p04-05
        y_band -= LU_H + 1.0
        # v1.17 (taller drawings: the bar under the band took ~6 mm of every 40 mm cell): the scale bar moves up into
        # the title line, right-aligned to the drawing
        bar = 10.0 if den <= 500 else 50.0              # scale bar beside the drawing (SCRIPT_STANDARD s.8)
        xb, yb = S.X(S.hi) - bar * K - 14.0, y_top - 3.0
        pg.line([(xb, yb), (xb + bar * K, yb)], E["INK"], 0.3, layer="title")
        for i in (0.0, 0.5, 1.0):
            pg.line([(xb + bar * K * i, yb), (xb + bar * K * i, yb + 1.2)], E["INK"], 0.2, layer="title")
        pg.text(u"0", xb, yb - 2.6, 2.0, E["INK"], align="C", layer="title")
        pg.text(u"%d m" % bar, xb + bar * K, yb - 2.6, 2.0, E["INK"], align="C", layer="title")
        pg.text(u"1:%d" % den, xb + bar * K + 5.0, yb - 0.6, 2.0, E["INK2"], align="L", layer="title")
    return pg, S, y_band


# ================================================================ v1.6 look (Aras 14 Nov 2026)
# LOOK_V16. Aras 14 Nov 09:46 UTC: keep the v1.4 ground skin ("the part that is attached": road band, grass strip with
# tufts). 09:56: ground and background from page 22 of the round 5 booklet (Bergama_booklet_A3 (1).pdf: section D1-D1'
# drawn by MasterPlan v40 p24 detail, common/section_frame.py sf_sky / sf_back_house), "remove the hatches ... keep the
# solid fill"; background houses more detailed, at their real positions. 09:56 + 10:01: the river bed as in the newest
# research (research/bank_depth_2026-10-28/REPORT.md s.2; walled town reach 5.0 m above the bed, Aras 28 Oct 14:12).
# 09:57: people and trees from the asset library (Data/cutouts, style a). 10:01: the land-use band of the site board
# p04-05 (Bergama_booklet_A3 (2).pdf; site board p45_strip, words P45_STRIP_WORD). Colours: read off his two images of
# p22 and p04 (drawing values).
GROUND_FILL = "D2CEB4"             # p22 cut ground, solid
BACK_FILL = "E4E0CF"               # p22 "Ground behind the cut" (soil mixed toward the paper)
SKY_LOW, SKY_TOP = "F8FAFA", "ECF2F4"   # v1.29: paler (liked B05 / D12: near-white sky)
SKY_CLOUDS = False                 # v1.29: no clouds (liked-examples default 9: "no birds, clouds, cars")
AC_GHOST = 0.45                    # v1.29: his Archicad context toned toward the sky (B05: city as ghost hairlines)
AC_OURS = ("F5F3EE", "A9794B", "4F5559", "B9CDD3", "B8B2A6")   # our canopy palette: never ghosted
SKY_ABOVE_M = 6.0                  # m of sky above the highest roof / tree
CLOUD = "FFFFFF"
SILHOUETTE = "CFCABF"              # v1.7: cut buildings as a plain silhouette (drawing value, ours)
INK_CUT = "4A3F35"                 # p22 cut line colour (the cut buildings' outline)
H_WALL, H_ROOF, H_EDGE, H_GLASS, H_SHADE = "EEEBE1", "C2BBB0", "B1ABA0", "9AA3A6", "D8D5CC"
H_FADE = 0.7                       # the farthest houses (BACK_M) mixed this far toward the sky
ROOF_PITCH_DEG = 30.0              # hipped tiled roof (drawing rule: the survey holds no roof forms)
EAVE_M = 0.4
FLAT_ROOF_FLOORS = 4               # 4 floors and more: a flat concrete roof with a 0.6 m parapet (drawing rule)
WIN_W, WIN_H, WIN_SILL, WIN_STEP = 1.2, 1.4, 0.9, 3.0     # m, window rows per floor (drawing rule)
WALL_BED = (55.5, 73.5)            # the walled town reach by bed level (REPORT s.2: upstream entry +73.1 ... Uc Kemer +55.6)
WALL_H_M, WALL_T_M, WALL_FILL = 5.0, 0.6, "BDB6A6"
PARAPET_M = 0.9                    # v1.10: a low parapet on the channel wall (drawing rule, ours)
WALL_MAX_W = 30.0                  # m: v1.6.1: a wider low flat is not the walled channel
WALL_SEARCH_M = 20.0               # m from the bed low point: v1.6.2 the wall stands where the ground reaches its top
DSI_BED_W = 20.0                   # m: DSI planned channel width (SYGM 2019 summary p.75, measure 155)
# v1.6.15, Aras 14 Nov 15:23 UTC: "dont give sources in the brackets dont give sources in the drawings at all" /
# "no sources for nothing": no source or method words in any drawn text (they stay in the log)
LEVEL_LABELS = False               # v1.6.8, Aras 14 Nov 13:01 UTC: "remove these markings we gonna have a new diagram
#                                    for that": no level sign / value stack; the water lines and fills stay
TERRACE_M = 2.5                    # m: the highest ground-tone terrace under a house behind (v1.6.13 / .14)
LU_H = 2.8                         # mm, the land-use band (v1.17: was 4.0; it outweighed the drawings)
LU = {"open": ("D9D6BE", u"open ground"), "street": ("8F8A80", u"street"), "stream": ("7FA4B3", u"stream"),
      "building": ("B9B2A2", u"building"), "wall": ("8E8578", u"wall")}
PEOPLE_KEYS = ("person_walk", "person_stand", "person_stand", "person_walk", "person_sit_step")
_CUT = {}


def _mix(a, b, t):
    a_, b_ = [int(a[i:i + 2], 16) for i in (0, 2, 4)], [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join("%02X" % int(round(x + (y - x) * t)) for x, y in zip(a_, b_))


def roof_rise(w, fl):
    if fl and fl >= FLAT_ROOF_FLOORS:
        return 0.6
    return min(3.5, (w / 2.0 + EAVE_M) * math.tan(math.radians(ROOF_PITCH_DEG)))


def sky(pg, S, C, z_top):
    """p22 sky: a soft vertical gradient from the lowest ground to the top, and a few white clouds (seeded per cut)"""
    import random as _r
    x0, x1 = S.X(S.lo), S.X(S.hi)
    zl = min(z for _, z in S.V)
    n = 10
    for i in range(n):
        za, zb_ = zl + (z_top - zl) * i / n, zl + (z_top - zl) * (i + 1) / n
        pg.poly([[(x0, S.Y(za)), (x1, S.Y(za)), (x1, S.Y(zb_)), (x0, S.Y(zb_))]], fill=_mix(SKY_LOW, SKY_TOP, i / (n - 1.0)),
                stroke=None, layer="sky")
    if not SKY_CLOUDS:
        return
    rg = _r.Random(u"%s" % C.name)
    span = x1 - x0
    for k in range(max(2, int(span / 70.0))):
        cx = x0 + span * (k + 0.2 + 0.6 * rg.random()) / max(2, int(span / 70.0))
        cy = S.Y(z_top) - (6.5 + 4.0 * rg.random())   # v1.17: the cloud tops stay under the frame top
        w = 10.0 + 10.0 * rg.random()
        g_hi = max(S.surf(min(S.hi, max(S.lo, S.lo + (cx - w / 2 - x0 + w * t) / S.K)))
                   for t in (0.0, 0.25, 0.5, 0.75, 1.0))
        if cy - 1.0 < S.Y(g_hi) + 3.0:               # v1.17: no cloud resting on the ground (N4-A, N6-A)
            rg.random(); rg.random(); rg.random(); rg.random(); rg.random(); rg.random()
            continue
        for j in range(6):
            t = j / 5.0
            r_ = (1.6 + 1.8 * math.sin(math.pi * t)) * (0.8 + 0.4 * rg.random())
            pg.circle(cx - w / 2 + w * t, cy + r_ * 0.45, r_, fill=CLOUD, layer="sky")
        pg.poly([[(cx - w / 2 - 1.0, cy), (cx + w / 2 + 1.0, cy), (cx + w / 2 + 1.0, cy + 1.2),
                  (cx - w / 2 - 1.0, cy + 1.2)]], fill=CLOUD, stroke=None, layer="sky")


def ac_background(name, L=None):
    """v1.25: the pieces of cached/bergama_archicad/background/<cut>.json (SectionsAC v1.5: [{kind fill|line, rings
    [[[s, z], ...]], colour, lw}] in survey s / absolute z m); [] when missing or unreadable"""
    p = os.path.join(bg_cache("bergama_archicad"), "background", u"%s.json" % name)
    try:
        with open(p, encoding="utf-8") as f:
            J = json.load(f)
    except Exception:
        return None                                     # v1.27.1: None = no Archicad view; [] = a view with no houses
    if L is not None and isinstance(J, dict) and J.get("L") is not None and abs(float(J["L"]) - L) > 1.0:
        return None                                     # v1.27.2: stale (cut redrawn since SectionsAC wrote it)
    pcs = J.get("pieces", J) if isinstance(J, dict) else J
    return [pc for pc in pcs if isinstance(pc, dict)] if isinstance(pcs, list) else []


def band_behind(pg, S, prof, d):
    """v1.24 (selinus_board v67.1 sa_render 'band'): the survey ground d m behind the cut, one fill per run of known
    heights from its profile down to the frame bottom, toned toward the sky with depth (0.35-0.86), a fine top edge"""
    f = 0.35 + 0.51 * min(1.0, d / SA_BANDS[-1])
    col, ecol = _mix(BAND_GROUND, SKY_LOW, f), _mix(BAND_EDGE, SKY_LOW, f)
    run = []
    for s, z in prof + [(None, None)]:
        if s is not None and z is not None and S.lo <= s <= S.hi:
            run.append((s, min(z, getattr(S, "z_top_", z) - 0.5)))
            continue
        if len(run) >= 2:
            top = [S.P(s_, z_) for s_, z_ in run]
            pg.poly([top + [S.P(run[-1][0], S.zb), S.P(run[0][0], S.zb)]], fill=col, stroke=None, layer="ground behind")
            pg.line(top, ecol, 0.05, layer="ground behind")
        run = []


def back_ground(pg, S, C):
    """p22 ground behind the cut: the highest survey ground up to BACK_M behind the line, a pale solid fill"""
    pts = [(s, z) for s, z in getattr(C, "back", []) if z is not None and S.lo <= s <= S.hi]
    if len(pts) < 2:
        return
    ring = [S.P(s, max(z, S.surf(s))) for s, z in pts] + [S.P(pts[-1][0], S.zb), S.P(pts[0][0], S.zb)]
    pg.poly([ring], fill=BACK_FILL, stroke=None, layer="ground behind")


def tree_behind(pg, S, s, base, h, dist, sp=u""):
    """v1.20: a tree behind the cut; v1.23: his asset cutout of its species in the library's depth tone (the drawn
    silhouette below only when the library is missing)"""
    key_ = sp if sp in (u"plane", u"ash", u"stone_pine", u"olive", u"tamarisk") else u"plane"
    dep_ = 0 if dist < 40.0 else (1 if dist < 100.0 else 2)
    X_, Y_ = S.P(s, base)
    if cutout(pg, key_, X_, Y_, h * S.K, int(s * 7) % 6, (int(s) % 2) == 1, "houses behind", dep_):
        return
    t = H_FADE * min(1.0, dist / BACK_M)               # v1.24.1: the v1.17-v1.19 fade again (Aras 06:57)
    fill, edge = _mix(TREE_FILL, SKY_LOW, t), _mix(TREE_EDGE, SKY_LOW, t)
    rg = random.Random(u"tb%.1f%.1f" % (s, dist))
    pg.line([S.P(s, base), S.P(s, base + 0.45 * h)], edge, max(0.04, 0.12 * S.K), layer="houses behind")
    cz, rx, ry = base + 0.62 * h, 0.3 * h * (0.85 + 0.3 * rg.random()), 0.36 * h
    if u"pine" in sp:                                   # v1.22: stone pine, a flat umbrella crown on a tall trunk
        cz, rx, ry = base + 0.8 * h, 0.42 * h, 0.17 * h
        pg.line([S.P(s, base + 0.45 * h), S.P(s, cz)], edge, max(0.04, 0.1 * S.K), layer="houses behind")
    elif u"plane" in sp:                                # plane: broad round crown
        cz, rx, ry = base + 0.6 * h, 0.38 * h, 0.36 * h
    elif u"ash" in sp:                                  # ash: upright oval crown
        cz, rx, ry = base + 0.64 * h, 0.24 * h, 0.34 * h
    ring = []
    for k in range(18):
        a_ = 2 * math.pi * k / 18
        f = 0.9 + 0.12 * rg.random()
        ring.append(S.P(s + rx * f * math.cos(a_), cz + ry * f * math.sin(a_)))
    pg.poly([ring], fill=fill, stroke=edge, lw=0.04, layer="houses behind")


def house(pg, S, a, b, base, h, fl, dist):
    """one house behind the cut at its real place (s a-b), base and height: wall, roof with eaves (hipped; flat with a
    parapet from FLAT_ROOF_FLOORS floors), a window row per floor, a door, toned toward the sky with distance"""
    t = H_FADE * min(1.0, dist / BACK_M)               # v1.24.1: the v1.17-v1.19 fade again (Aras 06:57)
    if fl == -1:                                        # v1.18.1: the Kızıl Avlu hall, roofless brick walls
        pg.poly([[S.P(a, base - 1.0), S.P(b, base - 1.0), S.P(b, base + h), S.P(a, base + h)]],
                fill=_mix(RED_HALL_FILL, SKY_LOW, max(t, 0.3)), stroke=_mix(RED_HALL_EDGE, SKY_LOW, max(t, 0.3)),
                lw=0.12 if dist < 40 else 0.08, layer="houses behind")
        st_ = 1.0 if S.K >= 0.4 else 2.0                # Wikipedia: "Its walls were built entirely of red bricks"
        if st_ * S.K >= 0.4:
            z_ = base + st_
            while z_ < base + h - 0.2:                  # brick courses, a texture (not counted courses)
                pg.line([S.P(a, z_), S.P(b, z_)], _mix(RED_HALL_EDGE, SKY_LOW, min(0.85, max(t, 0.3) + 0.25)), 0.03,
                        layer="houses behind")
                z_ += st_
        return
    if HOUSE_SILHOUETTE:                                # v1.20 (Aras 06:08 "the background houses looks awful"):
        wall, roof, edge = _mix(HOUSE_SIL, SKY_LOW, t), _mix(HOUSE_SIL_ROOF, SKY_LOW, t), _mix(H_EDGE, SKY_LOW, t)
        top = base + h                                  # flat silhouettes: wall + roof, one hairline, no detail
        pg.poly([[S.P(a, base - 1.0), S.P(b, base - 1.0), S.P(b, top), S.P(a, top)]], fill=wall, stroke=edge,
                lw=0.05, layer="houses behind")
        if fl and fl >= FLAT_ROOF_FLOORS:
            pg.poly([[S.P(a, top), S.P(b, top), S.P(b, top + 0.4), S.P(a, top + 0.4)]], fill=roof, stroke=edge,
                    lw=0.05, layer="houses behind")
        else:
            rise = roof_rise(b - a, fl)
            run = rise / math.tan(math.radians(ROOF_PITCH_DEG))
            ra, rb = a - EAVE_M * 0.5, b + EAVE_M * 0.5
            r0, r1 = min(ra + run, (ra + rb) / 2.0), max(rb - run, (ra + rb) / 2.0)
            pg.poly([[S.P(ra, top), S.P(rb, top), S.P(r1, top + rise), S.P(r0, top + rise)]], fill=roof, stroke=edge,
                    lw=0.05, layer="houses behind")
        return
    wall, roof, edge = _mix(H_WALL, SKY_LOW, t), _mix(H_ROOF, SKY_LOW, t), _mix(H_EDGE, SKY_LOW, t)
    glass, shade = _mix(H_GLASS, SKY_LOW, t), _mix(H_SHADE, SKY_LOW, t)
    K = S.K
    lw = 0.12 if dist < 40 else 0.08
    top = base + h
    pg.poly([[S.P(a, base - 1.0), S.P(b, base - 1.0), S.P(b, top), S.P(a, top)]], fill=wall, stroke=edge, lw=lw,
            layer="houses behind")
    w = b - a
    rise = ra = rb = 0.0
    if fl and fl >= FLAT_ROOF_FLOORS:
        pg.poly([[S.P(a - 0.1, top), S.P(b + 0.1, top), S.P(b + 0.1, top + 0.6), S.P(a - 0.1, top + 0.6)]],
                fill=shade, stroke=edge, lw=lw, layer="houses behind")
    else:
        rise = roof_rise(w, fl)
        run = rise / math.tan(math.radians(ROOF_PITCH_DEG))
        ra, rb = a - EAVE_M, b + EAVE_M
        ridge = [(min(ra + run, (ra + rb) / 2.0), top + rise), (max(rb - run, (ra + rb) / 2.0), top + rise)]
        pg.poly([[S.P(ra, top), S.P(rb, top), S.P(*ridge[1]), S.P(*ridge[0])]], fill=roof, stroke=edge, lw=lw,
                layer="houses behind")
        pg.poly([[S.P(a, top), S.P(b, top), S.P(b, top - 0.25), S.P(a, top - 0.25)]], fill=shade, stroke=None,
                layer="houses behind")                                       # the eave's shadow on the wall
    if w * K < 2.0:
        return
    # v1.7 (Aras 15:35 "more detailed background buildings"): a plinth, roof tiles and a chimney, each house its own
    # window size and bay rhythm, sills, glazing bars, shutters on low houses, balconies on blocks, a door with a hood
    # (drawing rules, ours: the survey gives floors and outline only); fine parts only where they print 0.3 mm or more
    rg = random.Random(u"%.1f" % a)
    dark = _mix(edge, wall, 0.35)
    ww = WIN_W * (0.8 + 0.35 * rg.random())
    step = WIN_STEP * (0.85 + 0.3 * rg.random())
    fine = ww * K >= 0.8
    pg.poly([[S.P(a, base - 1.0), S.P(b, base - 1.0), S.P(b, base + 0.5), S.P(a, base + 0.5)]], fill=shade,
            stroke=None, layer="houses behind")                                   # plinth
    if not (fl and fl >= FLAT_ROOF_FLOORS):
        if rise * K >= 2.0 and dist < 80:                                         # tile courses
            for k_ in range(1, int(rise / 0.5)):
                z_ = top + k_ * 0.5
                dx = (z_ - top) / math.tan(math.radians(ROOF_PITCH_DEG))
                if ra + dx < rb - dx:
                    pg.line([S.P(ra + dx, z_), S.P(rb - dx, z_)], edge, 0.04, layer="houses behind")
        if w >= 7.0 and rg.random() < 0.6:                                        # chimney
            cx_ = a + w * (0.25 + 0.5 * rg.random())
            pg.poly([[S.P(cx_ - 0.3, top + rise * 0.4), S.P(cx_ + 0.3, top + rise * 0.4), S.P(cx_ + 0.3, top + rise + 0.8),
                      S.P(cx_ - 0.3, top + rise + 0.8)]], fill=roof, stroke=edge, lw=lw * 0.7, layer="houses behind")
    nfl = max(1, int(fl or round(h / STOREY_M)))
    fh = h / nfl
    nwin = max(1, int((w - 1.0) // step))
    x0 = a + (w - (nwin - 1) * step) / 2.0
    shutters = nfl <= 2 and fine and rg.random() < 0.6
    balcony = nfl >= 3 and fine
    for i in range(nfl):
        zf = base + i * fh
        if i > 0:
            pg.line([S.P(a, zf), S.P(b, zf)], shade, 0.05, layer="houses behind")
        for j in range(nwin):
            cx = x0 + j * step
            if i == 0 and j == nwin // 2 and w >= 5.0:                         # the door with its hood
                pg.poly([[S.P(cx - 0.5, zf), S.P(cx + 0.5, zf), S.P(cx + 0.5, zf + 2.2), S.P(cx - 0.5, zf + 2.2)]],
                        fill=dark, stroke=None, layer="houses behind")
                if fine:
                    pg.poly([[S.P(cx - 0.8, zf + 2.3), S.P(cx + 0.8, zf + 2.3), S.P(cx + 0.8, zf + 2.45),
                              S.P(cx - 0.8, zf + 2.45)]], fill=edge, stroke=None, layer="houses behind")
                continue
            tall = balcony and i > 0 and j % 2 == 0
            zs = zf + (0.05 if tall else min(WIN_SILL, fh * 0.3))
            wh = min(2.2, fh * 0.75) if tall else min(WIN_H, fh * 0.5)
            pg.poly([[S.P(cx - ww / 2, zs), S.P(cx + ww / 2, zs), S.P(cx + ww / 2, zs + wh),
                      S.P(cx - ww / 2, zs + wh)]], fill=glass, stroke=None, layer="houses behind")
            if not fine:
                continue
            pg.line([S.P(cx, zs), S.P(cx, zs + wh)], wall, 0.05, layer="houses behind")          # glazing bar
            if tall:                                                                               # balcony
                pg.poly([[S.P(cx - ww / 2 - 0.4, zf - 0.15), S.P(cx + ww / 2 + 0.4, zf - 0.15),
                          S.P(cx + ww / 2 + 0.4, zf), S.P(cx - ww / 2 - 0.4, zf)]], fill=edge, stroke=None,
                        layer="houses behind")
                pg.line([S.P(cx - ww / 2 - 0.4, zf + 1.0), S.P(cx + ww / 2 + 0.4, zf + 1.0)], dark, 0.06,
                        layer="houses behind")
                for k_ in range(5):
                    xk = cx - ww / 2 - 0.4 + (ww + 0.8) * k_ / 4.0
                    pg.line([S.P(xk, zf), S.P(xk, zf + 1.0)], dark, 0.04, layer="houses behind")
                continue
            pg.poly([[S.P(cx - ww / 2 - 0.1, zs - 0.12), S.P(cx + ww / 2 + 0.1, zs - 0.12), S.P(cx + ww / 2 + 0.1, zs),
                      S.P(cx - ww / 2 - 0.1, zs)]], fill=edge, stroke=None, layer="houses behind")  # sill
            if shutters:
                for sd in (-1, 1):
                    xo = cx + sd * (ww / 2 + 0.05)
                    pg.poly([[S.P(xo, zs), S.P(xo + sd * ww * 0.45, zs), S.P(xo + sd * ww * 0.45, zs + wh),
                              S.P(xo, zs + wh)]], fill=shade, stroke=edge, lw=0.03, layer="houses behind")


def ground_fill(pg, S):
    """the cut ground: p22's solid fill (no hatch, no stipple) under the v1.4 cut line"""
    V = S.V
    ring = [S.P(*p) for p in V] + [S.P(V[-1][0], S.zb), S.P(V[0][0], S.zb)]
    pg.poly([ring], fill=GROUND_FILL, stroke=None, layer="poche")
    # v1.8 (run of v1.7): only inside the frame (a 2 mm stub ran past the right edge, N5 / N6), points closer than
    # 0.3 mm merged and the width eased with the scale (the summer strip and wall corners read as a black scribble
    # at 1:2000 and smaller)
    x0, x1 = S.X(S.lo), S.X(S.hi)
    pts = []
    for p in V:
        q = S.P(*p)
        if x0 - 1e-6 <= q[0] <= x1 + 1e-6 and (not pts or math.hypot(q[0] - pts[-1][0], q[1] - pts[-1][1]) >= 0.3):
            pts.append(q)
    if len(pts) < 2:
        return
    # v1.17.1 (600 dpi read of v1.17: on N2-A the cut line ran only 42 mm, in the channel): the v1.6.13 end trim
    # popped every point closer than 1.5 mm to the next, so most of the line was dropped; removed (butt ends now)
    # v1.17 (two reviews of v1.16: round black caps at the frame ends): butt ends, no inset
    pg.line(pts, S.E["INK"], min(0.6, max(0.4, 0.1 + 0.25 * S.K)), layer="cut line", cap=0)   # v1.15: the cut line about 3x every other line (DIAGRAM_STYLE v2, long river sections)


def town_walls(pg, S, C):
    """the walled town reach (REPORT s.2, Aras 28 Oct 14:12: walls pinned 5.0 m above the bed): a stone wall at both
    channel edges where the cut's bed lies in WALL_BED; the survey bank there is pre-wall"""
    if not getattr(S, "walled", None):
        return
    sL, sR, tL, tR = S.walled
    C.walls = []
    for s, side, top in ((sL, -1, tL), (sR, 1, tR)):
        sa, sb = sorted((s, s + side * WALL_T_M))
        pg.poly([[S.P(sa, C.z_th - 0.6), S.P(sb, C.z_th - 0.6), S.P(sb, top + PARAPET_M), S.P(sa, top + PARAPET_M)]],
                fill=WALL_FILL, stroke=INK_CUT, lw=min(0.3, max(0.04, 0.15 * S.K)), layer="walls")   # v1.15: thin at sheet scale (dark stubs on N2)
        C.walls.append((sa, sb))


def cutout(pg, key, X, Y, h_mm=None, n=0, flip=False, layer="people", depth=0):
    """one asset-library cutout (Data/cutouts/cutouts.json) standing at page (X, Y); h_mm None = its true h_m at the
    page scale; False when the library or the file is missing (the caller then draws the engine's vector)"""
    lib = _CUT.get("lib")
    if lib is None:
        lib = {}
        try:
            with open(os.path.join(DATA_DIR, "cutouts", "cutouts.json"), encoding="utf-8") as f:
                js = json.load(f).get("cutouts", {})
            for k, v in js.items():
                vs = v if isinstance(v, list) else [v]
                lib[k] = [e for e in vs if os.path.isfile(os.path.join(DATA_DIR, "cutouts", e.get("file", "")))]
        except Exception:
            lib = {}
        _CUT["lib"] = lib
    es = lib.get(key) or []
    if not es:
        return False
    e = es[n % len(es)]
    f_ = (e.get("depth") or {}).get(str(depth)) if depth else None     # v1.23: the library's depth tones
    p = os.path.join(DATA_DIR, "cutouts", f_ if f_ and os.path.isfile(os.path.join(DATA_DIR, "cutouts", f_)) else e["file"])
    sz = _CUT.get(p)
    if sz is None:
        with open(p, "rb") as f:
            hd = f.read(24)
        sz = _CUT[p] = (int.from_bytes(hd[16:20], "big"), int.from_bytes(hd[20:24], "big"))
    h = h_mm if h_mm is not None else e["h_m"] * _ENGINE_K[0]
    w = h * sz[0] / float(sz[1])
    fl = bool(flip) != (e.get("facing", 1) == -1 and False)
    pg.items.append(("image", X - w / 2.0, Y, w, h, p, None, fl, None, layer))
    return True


def landuse_band(pg, S, y, h):
    """the site board's land-use band (p04-05): one tile per run of what the cut crosses, its word inside"""
    C = S.C
    ch = getattr(S, "channel", (C.s_th, C.s_th))
    runs, cur = [], None
    s = S.lo
    while s < S.hi - 1e-9:
        e = min(S.hi, s + 0.5)
        m = (s + e) / 2.0
        if any(a <= m <= b for a, b in getattr(C, "walls", [])):
            k = "wall"
        elif ch[0] <= m <= ch[1]:                        # v1.6.7: the channel before streets (N3-A street in the bed)
            k = "stream"
        elif any(a <= m <= b for a, b in getattr(S, "roads", C.roads)):
            k = "street"
        elif any(t[4] and t[0] <= m <= t[1] for t in C.bld):
            k = "building"
        else:
            k = "open"
        if cur and cur[2] == k:
            cur[1] = e
        else:
            cur = [s, e, k]
            runs.append(cur)
        s = e
    for a, b, k in runs:
        x0, x1 = S.X(a) + 0.2, S.X(b) - 0.2
        if x1 - x0 < 0.2:
            continue
        col, word = LU[k]
        pg.poly([[(x0, y), (x1, y), (x1, y + h), (x0, y + h)]], fill=col, stroke=None, layer="band")
        tw = text_w_any(word, 1.7, False)
        if tw + 1.0 <= x1 - x0:
            pg.text(word, (x0 + x1) / 2.0, y + h / 2.0 - 0.6, 1.7, "FFFFFF" if k in ("street", "wall") else "3A352E",
                    align="C", layer="band")


def spread_levels(E, pg, S, short=False, gap=2.6):
    """v1.1: the level texts (engine level_line puts them on the cut's right end, over the design) move just right of
    the cut, top to bottom in level order, at least gap mm apart, each with a thin tick from the cut end"""
    lv = [it for it in pg.items if it[0] == "text" and it[8] == "levels"]
    if not lv:
        return
    x_end = S.X(S.hi)

    def _sign(it):                                       # the engine's level sign (triangle + bar) at the cut end
        # v1.6.8: anywhere (v1.6.7 ends the water lines at the joined stretch, so the signs no longer sit at x_end)
        if it[0] == "poly" and it[6] == "levels" and len(it[1]) == 1 and len(it[1][0]) == 3:
            return True
        if it[0] == "line" and it[5] == "levels" and len(it[1]) == 2 and abs(it[1][1][0] - it[1][0][0]) <= 1.7:
            return abs(it[1][1][1] - it[1][0][1]) < 1e-6
        return False
    pg.items = [it for it in pg.items if not (it[0] == "text" and it[8] == "levels") and not _sign(it)]
    if not LEVEL_LABELS:
        return
    # v1.6 (fix 2): the texts sit just right of where the water lines end (the channel), not at the cut's far end
    ends = [max(p[0] for p in it[1]) for it in pg.items if it[0] == "line" and it[5] == "levels" and len(it[1]) == 2
            and abs(it[1][0][1] - it[1][1][1]) < 1e-6]
    starts = [min(p[0] for p in it[1]) for it in pg.items if it[0] == "line" and it[5] == "levels" and len(it[1]) == 2
              and abs(it[1][0][1] - it[1][1][1]) < 1e-6]
    if ends:
        x_end = min(x_end, max(ends))
    # v1.6.7 (check of run 4: labels past the frame, struck through by the bank, people on them): the stack goes
    # right of the water lines, or left of them when it would leave the frame; it rises clear of the ground (+2 m:
    # a person) over its own width
    rows = [(it, it[1].split(u" (")[0] if short else it[1]) for it in sorted(lv, key=lambda t: -t[3])]
    tw = max(text_w_any(t, it[4], it[6]) for it, t in rows) + 3.4
    right = x_end + 3.0 + tw <= S.X(S.hi) - 0.5 or not starts
    x_tick = x_end if right else min(starts)
    xr = x_tick + 3.0 if right else x_tick - 3.0 - tw
    xr = max(S.X(S.lo) + 0.5, xr)
    s0, s1 = S.lo + (xr - S.X0) / S.K, S.lo + (xr + tw - S.X0) / S.K
    n_ = max(2, int((s1 - s0) / 0.5))
    y_clear = S.Y(max(S.surf(s0 + (s1 - s0) * i / n_) for i in range(n_ + 1)) + 2.0) + 0.6
    y_prev = None
    for it, txt in rows:
        y0 = it[3] - 0.6
        y = max(y0, y_clear + gap * (len(rows) - 1)) if y_prev is None else min(y0, y_prev - gap)
        y = max(y, y_clear) if y_prev is None or y_prev - gap >= y_clear else y_prev - gap
        y_prev = y
        pg.line([(x_tick + (0.3 if right else -0.3), y0), ((xr - 0.5) if right else (xr + tw + 0.5), y)], it[5],
                0.08, layer="levels")
        X = xr + 1.3                                     # the level sign beside its value
        pg.poly([[(X - 1.3, y + 1.9), (X + 1.3, y + 1.9), (X, y)]], fill=None, stroke=it[5], lw=0.2, layer="levels")
        pg.line([(X - 0.8, y - 0.6), (X + 0.8, y - 0.6)], it[5], 0.2, layer="levels")
        pg.text(txt, xr + 3.4, y - 0.4, it[4], it[5], bold=it[6], align="L", layer="levels")


def band(E, pg, S, y, h=9.0):
    """the material band under the cut (the engine's swatches, no widths): design flats on S4, else bed gravel, the
    strip and native vegetation by the rule planting"""
    C = S.C
    items = [(min(sa, sb), max(sa, sb), mat, lab) for sa, sb, z, mat, lab in S.flats]
    items += [(a, b, "road", u"Road") for a, b in C.roads]        # "road": the engine's plain grey swatch
    items += [(t[0], t[1], "concrete", u"Kızıl Avlu" if t[6] == -1 else u"Building") for t in C.bld if t[4]]
    if C.is_s4 and not S4_FROM_B19:                 # the engine's own band of both banks
        for b_ in S.banks:
            ra, rb = b_.d["regrade"]
            items.append((min(ra, rb), max(ra, rb), "gravel", u"Stream gravel"))
            items += [(min(a, b), max(a, b), m, l) for a, b, m, l in b_.d["band_more"]]
    covered = sorted((a, b) for a, b, m, l in items)
    wet = C.z_th + WET_BAND_M
    s, cur = S.lo, None
    sa_, sb_, _ = S.strip
    while s < S.hi - 1e-9:
        e = min(S.hi, s + 0.5)
        m = (s + e) / 2
        if any(a - 1e-6 <= m <= b + 1e-6 for a, b in covered):
            k = None
        elif sa_ <= m <= sb_:
            k = ("water", u"Summer water strip")
        elif S.surf(m) <= wet or any(a <= m <= b for a, b in S.design):
            k = ("gravel", u"Stream gravel")
        else:
            k = ("veg", u"Native vegetation")
        if k is not None:
            if cur and cur[2] == k[0] and cur[3] == k[1] and abs(cur[1] - s) < 1e-6:
                cur = (cur[0], e, k[0], k[1])
            else:
                if cur:
                    items.append(cur)
                cur = (s, e, k[0], k[1])
        else:
            if cur:
                items.append(cur)
            cur = None
        s = e
    if cur:
        items.append(cur)
    items.sort(key=lambda t: t[0])
    merged = []
    for a, b, mat, lab in items:
        if merged and merged[-1][3] == lab and abs(merged[-1][1] - a) < 0.6:
            merged[-1] = (merged[-1][0], b, mat, lab)
        else:
            merged.append((a, b, mat, lab))
    drop = 0.0
    for j, (a, b, mat, lab) in enumerate(merged):
        x0, x1 = S.X(a), S.X(b)
        if x1 - x0 < 0.3:
            continue
        E["swatch"](pg, x0, x1, y, h, mat, S.d["key"])
        if x1 - x0 < 6.0:
            continue                                     # too short for a name: the swatch alone
        lines = E["wrap"](lab, max(6, int((x1 - x0 + 4.0) / 1.1)))
        y0 = y - 2.8 - (drop if j % 2 else 0.0)
        for i, l in enumerate(lines):
            pg.text(l, (x0 + x1) / 2, y0 - i * 2.6, 2.0, E["INK2"], align="C", layer="band")
        if j % 2 == 0:
            drop = len(lines) * 2.6 + 0.6


# ================================================================ PDF (vector, layers as PDF layers)
PT = 25.4 / 72.0
_TR = {u"Ğ": 129, u"ğ": 141, u"İ": 143, u"ı": 144, u"Ş": 157, u"ş": 158, u"–": 150, u"—": 151, u"’": 146,
       u"‘": 145, u"“": 147, u"”": 148, u"•": 149, u"€": 128}
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"


def _pdf_txt(s):
    out = bytearray()
    for ch in s:
        c = _TR.get(ch)
        if c is None:
            o = ord(ch)
            c = o if (32 <= o < 127 or 160 <= o < 256) else 63
        if c in (40, 41, 92):
            out += b"\\"
        out.append(c)
    return bytes(out)


def _col(h):
    h = (h or "000000").lstrip("#")
    return "%.3f %.3f %.3f" % (int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0)


def _f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def _item_layer(it):
    t = it[0]
    return it[6] if t == "poly" else it[5] if t == "line" else it[7] if t == "circle" else it[9] if t == "image" else it[8]


def _png(path):
    """(w, h, rgb bytes, alpha bytes or None) of an 8-bit RGBA / RGB PNG (common/write_pdf.py _wp_png, cut down)"""
    import zlib
    import struct
    with open(path, "rb") as f:
        d = f.read()
    pos, idat, hdr = 8, [], None
    while pos + 8 <= len(d):
        n = struct.unpack(">I", d[pos:pos + 4])[0]
        t, c = d[pos + 4:pos + 8], d[pos + 8:pos + 8 + n]
        pos += 12 + n
        if t == b"IHDR":
            hdr = struct.unpack(">IIBBBBB", c[:13])
        elif t == b"IDAT":
            idat.append(c)
        elif t == b"IEND":
            break
    w, h, bd, ct = hdr[:4]
    if bd != 8 or ct not in (2, 6) or hdr[6]:
        return None
    bpp = 4 if ct == 6 else 3
    raw = zlib.decompress(b"".join(idat))
    stride = w * bpp
    out = bytearray(h * stride)
    prev = bytearray(stride)
    i = 0
    for yy in range(h):
        ft = raw[i]
        ln = bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        if ft == 1:
            for x in range(bpp, stride):
                ln[x] = (ln[x] + ln[x - bpp]) & 255
        elif ft == 2:
            for x in range(stride):
                ln[x] = (ln[x] + prev[x]) & 255
        elif ft == 3:
            for x in range(stride):
                ln[x] = (ln[x] + (((ln[x - bpp] if x >= bpp else 0) + prev[x]) >> 1)) & 255
        elif ft == 4:
            for x in range(stride):
                a = ln[x - bpp] if x >= bpp else 0
                b = prev[x]
                c = prev[x - bpp] if x >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                ln[x] = (ln[x] + (a if pa <= pb and pa <= pc else (b if pb <= pc else c))) & 255
        out[yy * stride:(yy + 1) * stride] = ln
        prev = ln
    if ct == 2:
        return w, h, bytes(out), None
    rgb = bytearray(w * h * 3)
    rgb[0::3], rgb[1::3], rgb[2::3] = out[0::4], out[1::4], out[2::4]
    return w, h, bytes(rgb), bytes(out[3::4])


def _image_obj(path, add):
    """the PDF XObject id of a PNG (alpha as SMask), or None"""
    import zlib
    try:
        r_ = _png(path)
    except Exception:
        r_ = None
    if not r_:
        return None
    w, h, rgb, al = r_
    sm = ""
    if al is not None:
        a = zlib.compress(al, 6)
        sid = add(("<< /Type /XObject /Subtype /Image /Width %d /Height %d /ColorSpace /DeviceGray /BitsPerComponent 8 "
                   "/Filter /FlateDecode /Length %d >>\nstream\n" % (w, h, len(a))).encode("latin-1") + a + b"\nendstream")
        sm = " /SMask %d 0 R" % sid
    c = zlib.compress(rgb, 6)
    return add(("<< /Type /XObject /Subtype /Image /Width %d /Height %d /ColorSpace /DeviceRGB /BitsPerComponent 8%s "
                "/Filter /FlateDecode /Length %d >>\nstream\n" % (w, h, sm, len(c))).encode("latin-1") + c + b"\nendstream")


def write_pdf(path, pages, title):
    """pages: [(w_mm, h_mm, items)] engine Page items, page mm, y up"""
    objs = []

    def add(b):
        objs.append(b)
        return len(objs)
    layers = []
    for _, _, items in pages:
        for it in items:
            ly = _item_layer(it)
            if ly not in layers:
                layers.append(ly)
    ocg = dict((ly, add(("<< /Type /OCG /Name (%s) >>" % _pdf_txt(u"%s" % ly).decode("latin-1")).encode("latin-1")))
               for ly in layers)
    f_r = add(("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding << /Type /Encoding /BaseEncoding "
               "/WinAnsiEncoding %s >> >>" % _DIFF).encode())
    f_b = add(("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding << /Type /Encoding /BaseEncoding "
               "/WinAnsiEncoding %s >> >>" % _DIFF).encode())
    alphas = {}
    images = {}
    pages_id = len(objs) + 1 + 2 * len(pages) + 50          # placeholder, set below
    kids = []
    content_ids = []
    for w, h, items in pages:
        k = 72.0 / 25.4
        A = ["%s 0 0 %s 0 0 cm" % (_f(k), _f(k)), "1 J 1 j"]
        cur = None
        for it in items:
            t = it[0]
            ly = _item_layer(it)
            if ly != cur:
                if cur is not None:
                    A.append("EMC")
                A.append("/OC /oc%d BDC" % ocg[ly])
                cur = ly
            if t == "poly":
                rings, fill, stroke, lw, dash, _ly, join, stripes, alpha = it[1:10]
                if not fill and not stroke:
                    continue
                A.append("q")
                if alpha is not None and alpha < 0.999:
                    a = round(alpha * 20) / 20.0
                    alphas[a] = 1
                    A.append("/GA%d gs" % int(a * 100))
                pth = []
                for r in rings:
                    pth.append("%s %s m" % (_f(r[0][0]), _f(r[0][1])))
                    pth += ["%s %s l" % (_f(p[0]), _f(p[1])) for p in r[1:]]
                    pth.append("h")
                A += pth
                if fill:
                    A.append("%s rg" % _col(fill))
                if stroke:
                    A.append("%s RG %s w" % (_col(stroke), _f(lw or 0.1)))
                    A.append(("[%s] 0 d" % " ".join(_f(v) for v in dash)) if dash else "[] 0 d")
                A.append("B" if (fill and stroke) else "f" if fill else "S")
                A.append("Q")
            elif t == "line":
                pts, stroke, lw, dash, _ly, cap = it[1:7]
                A.append("q %s RG %s w %d J" % (_col(stroke), _f(lw or 0.1), {0: 0, 1: 1, 2: 2}.get(cap, 1)))
                A.append(("[%s] 0 d" % " ".join(_f(v) for v in dash)) if dash else "[] 0 d")
                A.append("%s %s m" % (_f(pts[0][0]), _f(pts[0][1])))
                A += ["%s %s l" % (_f(p[0]), _f(p[1])) for p in pts[1:]]
                A.append("S Q")
            elif t == "circle":
                cx, cy, r, fill, stroke, lw = it[1:7]
                c = 0.5523 * r
                A.append("q")
                A.append("%s %s m %s %s %s %s %s %s c %s %s %s %s %s %s c %s %s %s %s %s %s c %s %s %s %s %s %s c h" % tuple(
                    _f(v) for v in (cx + r, cy, cx + r, cy + c, cx + c, cy + r, cx, cy + r, cx - c, cy + r, cx - r, cy + c,
                                    cx - r, cy, cx - r, cy - c, cx - c, cy - r, cx, cy - r, cx + c, cy - r, cx + r,
                                    cy - c, cx + r, cy)))
                if fill:
                    A.append("%s rg" % _col(fill))
                if stroke:
                    A.append("%s RG %s w" % (_col(stroke), _f(lw or 0.1)))
                A.append("B" if (fill and stroke) else "f" if fill else "S")
                A.append("Q")
            elif t == "image":
                x, y, wi, hi, ipath, _a, flip = it[1:8]
                oid = images.get(ipath)
                if oid is None:
                    oid = images[ipath] = _image_obj(ipath, add) or 0
                if oid:
                    A.append("q %s 0 0 %s %s %s cm /Im%d Do Q" % (_f(-wi if flip else wi), _f(hi),
                                                               _f(x + wi if flip else x), _f(y), oid))
            elif t == "text":
                s, x, y, size, color, bold, align = it[1:8]
                wmm = text_w_any(s, size, bold)
                x0 = x - {"L": 0.0, "C": wmm / 2.0, "R": wmm}.get(align, 0.0)
                pt = size / PT
                A.append("BT /%s %s Tf %s rg %s 0 0 %s %s %s Tm (" % ("F2" if bold else "F1", _f(pt), _col(color),
                                                                     _f(PT), _f(PT), _f(x0), _f(y)))
                A.append(None)
                A[-1] = _pdf_txt(s)
                A.append(") Tj ET")
        if cur is not None:
            A.append("EMC")
        body = bytearray()
        for a in A:
            if isinstance(a, bytes):
                body += a
            else:
                body += a.encode("latin-1") + (b"" if a.endswith("(") else b"\n")
        cid = add(b"<< /Length %d >>\nstream\n" % len(body) + bytes(body) + b"\nendstream")
        content_ids.append((cid, w, h))
    gs = " ".join("/GA%d << /Type /ExtGState /ca %s /CA %s >>" % (int(a * 100), _f(a), _f(a)) for a in sorted(alphas))
    props = " ".join("/oc%d %d 0 R" % (i, i) for i in ocg.values())
    xo = " ".join("/Im%d %d 0 R" % (i, i) for i in images.values() if i)
    res = add(("<< /Font << /F1 %d 0 R /F2 %d 0 R >> /ExtGState << %s >> /Properties << %s >> /XObject << %s >> >>" % (
        f_r, f_b, gs, props, xo)).encode("latin-1"))
    pages_id = len(objs) + len(content_ids) + 1
    for cid, w, h in content_ids:
        kids.append(add(("<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %s %s] /Contents %d 0 R /Resources %d 0 R >>" % (
            pages_id, _f(w / PT), _f(h / PT), cid, res)).encode()))
    assert add(("<< /Type /Pages /Kids [%s] /Count %d >>" % (" ".join("%d 0 R" % k for k in kids), len(kids))).encode()) \
        == pages_id
    oc = " ".join("%d 0 R" % i for i in ocg.values())
    cat = add(("<< /Type /Catalog /Pages %d 0 R /OCProperties << /OCGs [%s] /D << /Order [%s] /ON [%s] >> >> >>" % (
        pages_id, oc, oc, oc)).encode())
    info = add(b"<< /Title (" + _pdf_txt(title) + b") /Producer (Bergama Sections) >>")
    out = bytearray(b"%PDF-1.5\n%\xe2\xe3\xcf\xd3\n")
    offs = []
    for i, b in enumerate(objs):
        offs.append(len(out))
        out += b"%d 0 obj\n" % (i + 1) + b + b"\nendobj\n"
    x = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for o in offs:
        out += b"%010d 00000 n \n" % o
    out += b"trailer\n<< /Size %d /Root %d 0 R /Info %d 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, cat, info, x)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "wb") as f:
            f.write(bytes(out))
    except PermissionError:                                   # open in a viewer: a timed name
        path = path[:-4] + time.strftime("_%H%M%S") + ".pdf"
        with open(path, "wb") as f:
            f.write(bytes(out))
    return path


_ENGINE_W = []
_ENGINE_K = [2.0]


def text_w_any(s, size, bold):
    if _ENGINE_W:
        return _ENGINE_W[0](s, size, bold)
    return 0.5 * size * len(s)


def items_bbox(items):
    xs, ys = [], []
    for it in items:
        t = it[0]
        if t == "poly":
            for r in it[1]:
                xs += [p[0] for p in r]
                ys += [p[1] for p in r]
        elif t == "line":
            xs += [p[0] for p in it[1]]
            ys += [p[1] for p in it[1]]
        elif t == "circle":
            xs += [it[1] - it[3], it[1] + it[3]]
            ys += [it[2] - it[3], it[2] + it[3]]
        elif t == "text":
            w = text_w_any(it[1], it[4], it[6])
            x0 = it[2] - {"L": 0.0, "C": w / 2.0, "R": w}.get(it[7], 0.0)
            xs += [x0, x0 + w]
            ys += [it[3] - 0.3 * it[4], it[3] + it[4]]
        elif t == "image":
            xs += [it[1], it[1] + it[3]]
            ys += [it[2], it[2] + it[4]]
    return min(xs), min(ys), max(xs), max(ys)


# ================================================================ booklet items (bergama-items/1)
def _lines_in():
    g = globals()
    v = g.get("section_line")
    if v is None:
        return []
    if not isinstance(v, (list, tuple)):
        v = [v]
    out = []
    for ln in v:
        try:
            if hasattr(ln, "From"):
                a, b = ln.From, ln.To
            elif hasattr(ln, "PointAtStart"):
                a, b = ln.PointAtStart, ln.PointAtEnd
            else:
                continue
            if math.hypot(b.X - a.X, b.Y - a.Y) > 1.0:
                out.append(((a.X, a.Y), (b.X, b.Y)))
        except Exception:
            pass
    return out


def model_lines(log):
    """the curves on layer section_lines of the open model (Aras 12 Nov 10:53 UTC: "i will give the section lines in
    .3dm"): [(name, A, B)], the name = the object's name, else S1, S2 ... in the layer's order"""
    try:
        import Rhino
        doc = Rhino.RhinoDoc.ActiveDoc
        out = []
        for o in _layer_objs(doc, SECTION_LAYER):
            g = o.Geometry
            if not isinstance(g, Rhino.Geometry.Curve):
                continue
            a, b = g.PointAtStart, g.PointAtEnd
            if math.hypot(b.X - a.X, b.Y - a.Y) <= 1.0:
                continue
            nm = (o.Attributes.Name or u"").strip() or u"S%d" % (len(out) + 1)
            out.append((nm, (a.X, a.Y), (b.X, b.Y)))
        if out:
            log.append(u"section_line: nothing wired: %d line(s) read from the model layer %s (%s)" % (
                len(out), SECTION_LAYER, u", ".join(n for n, _, _ in out)))
        return out
    except Exception as ex:
        log.append(u"FLAG model layer %s not read (%s)" % (SECTION_LAYER, type(ex).__name__))
        return []


def named_lines(log):
    """the node sections of Data/section_lines.json: [(name, A, B)]"""
    p = os.path.join(DATA_DIR, "section_lines.json")
    try:
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        out = [(k, tuple(v[0]), tuple(v[1])) for k, v in sorted(d["lines"].items())]
        log.append(u"section_line: nothing wired: %d named lines read from %s" % (len(out), p))
        return out
    except Exception as ex:
        log.append(u"FLAG section lines: %s not read (%s)" % (p, type(ex).__name__))
        return []


NODE_SCALES = (500, 1000, 1500, 2000, 2500, 3000)   # 500: the four-seasons cut (14 Nov 13:24)


def _r2(o):
    """mm to 0.01 (the 348 MB cuts.json of the first v1.6.4 run was mostly float digits)"""
    if isinstance(o, float):
        return round(o, 2)
    if isinstance(o, (list, tuple)):
        return [_r2(v) for v in o]
    return o


def cut_cache(E, C):
    """v1.6.4 (Aras 12:38 UTC "don't ever do the same job twice ... cache it"): the cut drawn once more at each
    node-page scale, unshifted, so the node pages read cached/bergama_sections/cuts.json instead of redoing it"""
    items, k0, S = {}, E.get("K"), None
    for d in NODE_SCALES:
        prog(u"%s: draw 1:%d" % (C.name, d))
        pg, S, _y = draw_cut(E, C, SEASON, d, 0.0, 0.0)
        # v1.6.9 (four-seasons thread, Aras 13:06 UTC: the season cuts reuse this base with other assets): the page
        # mapping, so a reader places its own assets: x = X0 + (s - lo) * K, y = Y0 + (z - zb) * K (mm)
        items[str(d)] = dict(bbox=[round(v, 2) for v in items_bbox(pg.items)], items=_r2(pg.items),
                             map=dict(X0=round(S.X0, 3), Y0=round(S.Y0, 3), K=S.K, lo=S.lo, zb=round(S.zb, 3)))
    E["K"] = k0
    ppl = people_for(S, SEASON, E)[0]
    return dict(items=items, z_th=round(C.z_th, 3), window=list(C.window),
                season=SEASON, layers_season=[u"water", u"levels", u"planting", u"people", u"trees", u"callouts"],
                surface=_r2(S.V), channel=_r2(list(S.channel)), walled=_r2(list(S.walled)) if S.walled else None,
                strip=_r2(list(S.strip)) if S.has_strip else None,
                planting=dict((k, _r2(S.d[k])) for k in (u"grass", u"reeds", u"iris", u"trees")),
                people=[[round(q[0], 2), q[1], bool(q[2])] for q in ppl],
                levels=dict((k if isinstance(k, str) else u"%s|%s" % k, [round(v[0], 3), v[1]])
                            for k, v in C.levels.items()),
                bld=[dict(s=[round(t[0], 2), round(t[1], 2)], h=t[3], cut=t[4], behind_m=round(t[5], 1))
                     for t in C.bld],
                roads=[[round(a, 2), round(b, 2)] for a, b in C.roads], trees=[round(t, 2) for t in C.trees],
                notes=list(C.notes),
                # v1.18 (seasons thread): the masterplan parts on the cut line, in s order (s from the line's A end)
                parts=[[round(a_, 2), round(b_, 2), MP_LABEL.get(k_, k_)]
                       for k_, a_, b_, dist_, cut_ in sorted(getattr(C, "mp", []), key=lambda t: t[1]) if cut_])


A3 = (420.0, 297.0)                # mm, landscape: Aras 14 Nov 15:25-15:27 UTC "fit every drawing into A3's like the
#                                    scale is not important" / "everything that we have in slide 2 gonna be single
#                                    landscape A3 this applies to everything"
A3_MARGIN, A3_GAP, A3_TITLE = 10.0, 5.0, 10.0
A3_DENS = (500, 750, 1000, 1250, 1500, 2000, 2500, 3000, 4000, 5000)
A3_GRIDS = ((4, 3), (3, 4), (2, 6))   # columns x rows; cuts in reading order, the A/B pair of a node side by side


def _scale_it(it, f, o=(0.0, 0.0), lw=False):
    """item scaled by f about the point o; lw=True scales the line widths too"""
    t, ox, oy = it[0], o[0], o[1]
    if t == "poly":
        it = (t, [[(ox + (p[0] - ox) * f, oy + (p[1] - oy) * f) for p in r] for r in it[1]]) + tuple(it[2:])
        return it[:4] + (max(0.02, it[4] * f),) + it[5:] if lw and it[3] else it
    if t == "line":
        it = (t, [(ox + (p[0] - ox) * f, oy + (p[1] - oy) * f) for p in it[1]]) + tuple(it[2:])
        return it[:3] + (max(0.02, it[3] * f),) + it[4:] if lw else it
    if t == "circle" and lw:
        return (t, ox + (it[1] - ox) * f, oy + (it[2] - oy) * f, it[3] * f) + tuple(it[4:])
    if t == "circle":
        return (t, it[1] * f, it[2] * f, it[3] * f) + tuple(it[4:])
    if t == "text":
        return (t, it[1], it[2] * f, it[3] * f, it[4] * f) + tuple(it[5:])
    if t == "image":
        return (t, it[1] * f, it[2] * f, it[3] * f, it[4] * f) + tuple(it[5:])
    return it


# ================================================================ v1.8 the masterplan in section (Aras 14 Nov 15:38-15:41)
# "please take these from the masterplan that i have given you anything that concerns masterplans that should use it";
# "sections should be 3Dified version of the masterplan"; "if things that we have drawn does not have a 3D version of
# them like canopies be creative with them"; "feel free to invent there for our proposals"; "things that you propose
# should look like competition buildings or canopies ... designed by starchitects"; "make them as detailed as you can".
# The plan pieces come from the MasterplanBase cache (his B19_setB_layers259.svg in survey m, built once by the slide 2
# chain); each layer the cut crosses is given a designed section form (DESIGN INTENT, ours: the plan holds no levels).
# The existing context stays survey data.
MP_CACHE = os.path.join(BERGAMA_ROOT, "cached", "bergama_masterplanbase", "masterplan.json")   # MasterplanBase v1
MP_KIND = {"teras": "terrace", "iskele_kenari": "deck", "kanopi": "canopy", "teras_-_canopy": "canopy",
           "desings": "pavilion", "kopruler": "bridge", "istinaat": "wall", "yuruyus": "walk", "normal": "walk",
           "yol_kenar": "walk", "path": "bridge", "duzenlenmis": "plaza", "yeni": "cycle", "bisiklet": "cycle", "circulation": "walk",
           "kesin_yesil": "green", "belki_yesil": "green", "su_bitkii": "reeds", "tas": "stones"}
MP_MAX_M2 = 100000.0              # m2: a bigger "piece" is a sheet / texture frame, not a plan element
MP_TREES = []                      # v1.21: his planted trees (x, y, crown m) from the plan's PLANTING layer, filled by mp_load
MP_CANOPY_PTS = []                 # v1.19: every corner of the plan's canopy triangles (survey m), filled by mp_load
TREE_H_M = {"stone_pine": 20.0, "plane": 32.5, "ash": 17.5, "willow": 22.5, "olive": 7.5, "tamarisk": 4.0}
#   v1.26: mature height, m = midpoint of Van den Berk (stone pine "15 - 25 m", plane "30 - 35 m", ash "15-20 m",
#   willow "20 - 25 (30) m", olive "5 - 10 m"); tamarisk "up to 4 metres tall" (Ferns, T. smyrnensis); sourced in
#   library/research/tree_canopy_heights_v1.md, not Türkiye-specific
CANOPY_CLEAR_M = 2.30        # v1.26: DfT Inclusive Mobility 2021 s.3.2 "Generally, this should be a minimum of 2300mm"
CANOPY_Q500_M = 0.60         # v1.26: EA floors "at least 600 millimetres ... above the estimated flood level", applied to Q500
CANOPY_RISE_M = 1.80         # v1.26: ridge above valley, DESIGN ASSUMPTION (no source sets a ridge, UNVERIFIED)
CANOPY_SKIN_M, CANOPY_LOUVRE_M, CANOPY_SLAT_M = 0.10, 0.30, 0.30   # v1.28: skin, louvre depth, slat spacing (design intent, ours)
CANOPY_Y_FORK, CANOPY_Y_ARM_M, CANOPY_DECK_M = 0.6, 2.5, 0.12      # v1.28: Y fork at 60 % of the height, arm reach, deck (design intent)
CANOPY_PLINTH_M, CANOPY_MULLION_M, CANOPY_PLANTER_M = 0.45, 1.5, 2.4  # v1.28.2: stone plinth, glazing bay, planter length (design intent, ours)
P_STONE = "B8B2A6"                                                  # v1.28.2: plinth stone
CANOPY_LO, CANOPY_HI, CANOPY_T = 3.6, 5.4, 0.15   # m: valley / ridge above the ground, plate thickness (design intent, ours)
MP_BEHIND_M = 60.0                 # m: canopies and pavilions this far behind the cut are drawn in elevation
MP_LABEL = {"terrace": u"Stepped terraces", "deck": u"Water deck", "canopy": u"Canopy", "pavilion": u"Pavilion",
            "bridge": u"Footbridge", "wall": u"Retaining wall", "walk": u"Promenade", "plaza": u"Square",
            "cycle": u"Cycle path", "green": u"Green"}
HARD = ("terrace", "deck", "walk", "plaza", "cycle", "pavilion")
RISE_M, SEAT_TREAD_M = 0.45, 0.9   # terrace seat steps (design)
P_CONC, P_CONC_LT, P_TIMBER, P_STEEL = "BDB7AA", "D9D4C8", "A9794B", "4F5559"
P_GLASS, P_SHELL, P_GREEN, P_PAVE, P_CYCLE = "B9CDD3", "F5F3EE", "8E9E6A", "C9C0AE", "B3735A"


def prog(msg):
    """v1.10: one progress line, written at once (the log is written only at the end; a slow run showed nothing)"""
    try:
        with open(os.path.join(BERGAMA_ROOT, "logs", "bergama_sections_progress.txt"), "a", encoding="utf-8") as f:
            f.write(u"%s %s\n" % (time.strftime("%H:%M:%S"), msg))
    except Exception:
        pass


def mp_load(log):
    """{layer id: [(closed, [(x, y), ...]), ...]} in survey m from the MasterplanBase cache; {} when missing"""
    try:
        with open(MP_CACHE, encoding="utf-8") as f:
            J = json.load(f)
    except (IOError, OSError, ValueError) as ex:
        log.append(u"FLAG masterplan: no MasterplanBase cache (%s): the sections show the survey only" % ex)
        return {}
    # MasterplanBase v1: {"layers": {"a/b/c": [[kind, fill, stroke, width_m, [[x, y], ...]], ...]}}; the innermost id
    # names the thing; kind r = ring, l = open line, a = clip outline of a picture group (its area), s = a loose stamp
    # v1.11 (run of v1.10: "green" covered every cut with a tree row): a picture group's clip outline counts only
    # where the layer has no drawn ring (kesin_yesil's 316 texture clips include the whole 2.1 km2 sheet), any piece
    # over MP_MAX_M2 is a frame, open lines only for walls; kopruler/* = bridges
    out = {}
    del MP_CANOPY_PTS[:]
    del MP_TREES[:]
    raw_t = []
    for key, pieces in J.get("layers", {}).items():
        lid = u"kopruler" if key.startswith(u"kopruler") else key.split("/")[-1]
        if key.startswith(u"begum_su_merdiven/outline"):   # v1.22: his water stairs = stepped terraces
            lid = u"teras"
        if u"planting" in key.lower():                  # v1.21: each closed symbol piece = one tree (centre, crown)
            if u"rosemary" in key.lower():              # v1.22: a shrub, not a tree
                continue
            sp = key.split("/")[-1].lower().replace(u"trees_", u"")
            for p in pieces:
                q = p[4]
                if p[0] in ("r", "a", "s") and len(q) >= 3:
                    xs, ys = [v[0] for v in q], [v[1] for v in q]
                    dia = max(max(xs) - min(xs), max(ys) - min(ys))
                    rnd = min(max(xs) - min(xs), max(ys) - min(ys)) / max(dia, 1e-6)
                    if 1.0 <= dia <= 25.0 and rnd >= 0.6:      # round symbols only (no planted strips)
                        raw_t.append(((max(xs) + min(xs)) / 2.0, (max(ys) + min(ys)) / 2.0, dia, sp))
            continue
        if lid not in MP_KIND:
            continue
        if MP_KIND[lid] == "canopy":                    # v1.19: the triangle corners (rings and open edges)
            MP_CANOPY_PTS.extend(tuple(q) for p in pieces if p[0] in ("r", "l") for q in p[4])
        has_r = any(p[0] == "r" for p in pieces)
        for p in pieces:
            r = [tuple(q) for q in p[4]]
            if len(r) < 2 or p[0] == "s" or (p[0] == "a" and has_r) or (p[0] == "l" and MP_KIND[lid] != "wall"):
                continue
            if p[0] != "l" and abs(sum(r[i][0] * r[i - 1][1] - r[i - 1][0] * r[i][1] for i in range(len(r)))) / 2.0 > MP_MAX_M2:
                continue
            out.setdefault(lid, []).append((p[0] != "l", r))
    cells = {}                                          # v1.21: one tree per 1.5 m (symbol parts merged, largest kept)
    for x, y, dia, sp in sorted(raw_t, key=lambda t: -t[2]):
        k = (int(x // 1.5), int(y // 1.5))
        if any((k[0] + i, k[1] + j) in cells for i in (-1, 0, 1) for j in (-1, 0, 1)):
            continue
        cells[k] = (x, y, dia, sp)
    MP_TREES.extend(cells.values())
    log.append(u"tree heights (mature, m): %s, Van den Berk midpoints / Ferns, sourced, not Türkiye-specific; canopy "
               u"valley underside >= ground + %.2f (DfT) and >= Q500 + %.2f (EA), ridge + %.1f m DESIGN ASSUMPTION "
               u"(UNVERIFIED)" % (u", ".join(u"%s %.1f" % kv for kv in sorted(TREE_H_M.items())), CANOPY_CLEAR_M,
                                  CANOPY_Q500_M, CANOPY_RISE_M))
    log.append(u"masterplan trees: %d from the PLANTING layer (%d symbol pieces)%s" % (
        len(MP_TREES), len(raw_t), u"" if MP_TREES else u": none, the green areas get tree rows (design)"))
    log.append(u"masterplan: %s, %s" % (MP_CACHE, u", ".join(u"%s %d" % (k, len(v)) for k, v in sorted(out.items()))))
    return out


def red_hall_load(log):
    """v1.18.1: the Kızıl Avlu main hall outline(s) from the MasterplanBase cache as basemap buildings with fl = -1
    (drawn as the roofless Roman hall), height RED_HALL_H_M; overlapping rings kept once (the largest)"""
    try:
        with open(MP_CACHE, encoding="utf-8") as f:
            J = json.load(f)
    except (IOError, OSError, ValueError):
        return []
    rings = []
    for key, pieces in J.get("layers", {}).items():
        if RED_HALL_KEY not in key:
            continue
        for p in pieces:
            r = [tuple(q) for q in p[4]]
            if p[0] != "r" or len(r) < 3:
                continue
            ar = abs(sum(r[i][0] * r[i - 1][1] - r[i - 1][0] * r[i][1] for i in range(len(r)))) / 2.0
            if ar >= RED_HALL_MIN_M2:
                rings.append((ar, r))
    out, cs = [], []
    for ar, r in sorted(rings, key=lambda t: -t[0]):
        cx, cy = sum(q[0] for q in r) / len(r), sum(q[1] for q in r) / len(r)
        if any(math.hypot(cx - a, cy - b) < 15.0 for a, b in cs):
            continue
        cs.append((cx, cy))
        xs, ys = [q[0] for q in r], [q[1] for q in r]
        out.append((min(xs), min(ys), max(xs), max(ys), r, RED_HALL_H_M, -1))
    log.append(u"Kızıl Avlu: %d hall outline(s) from the masterplan, walls %.0f m (Wikipedia, Red Basilica); "
               u"round towers left out (no sourced height)" % (len(out), RED_HALL_H_M))
    return out


def mp_for(C, MP):
    """C.mp = [(kind, s0, s1, distance behind, cut?)]: the plan pieces the line cuts (even-odd spans of closed rings,
    crossing points of open lines) and canopies / pavilions up to MP_BEHIND_M behind it"""
    C.mp = []
    if not hasattr(C, "trees_back"):                    # v1.20 (context_for sets it when the basemap is there)
        C.trees_back = []
    w0, w1 = C.window
    for lid, pieces in MP.items():
        kind = MP_KIND[lid]
        for closed, r in pieces:
            if len(r) < 2:
                continue
            so = [C.su(q[0], q[1]) for q in r]
            segs = list(zip(so, so[1:] + so[:1])) if closed else list(zip(so[:-1], so[1:]))
            xs = sorted(sa + (sb - sa) * (0.0 - oa) / (ob - oa) for (sa, oa), (sb, ob) in segs if (oa < 0.0) != (ob < 0.0))
            if not closed:
                C.mp += [(kind, x - 0.3, x + 0.3, 0.0, True) for x in xs if w0 < x < w1]
                continue
            for a, b in zip(xs[0::2], xs[1::2]):
                a, b = max(a, w0), min(b, w1)
                if b - a > 0.3:
                    C.mp.append((kind, a, b, 0.0, True))
            if not xs and kind == "green" and closed and not MP_TREES:     # v1.20 (v1.21: only without his planting): a tree row along his green area behind the cut
                omin = min(o for _, o in so)
                a, b = max(min(s for s, _ in so), w0), min(max(s for s, _ in so), w1)
                if 0.0 < omin <= TREE_BACK_M and b - a > 4.0:
                    rg = random.Random(u"g%.1f%.1f" % (a, omin))
                    x = a + 2.0 + 4.0 * rg.random()
                    while x < b - 1.5:                  # trees 9-15 m apart, 7-11 m tall (design intent, ours)
                        C.trees_back.append((x, omin + 1.5, None, 7.0 + 4.0 * rg.random(), u"plan"))
                        x += 9.0 + 6.0 * rg.random()
            if not xs and kind in ("canopy", "pavilion"):
                omin = min(o for _, o in so)
                a, b = max(min(s for s, _ in so), w0), min(max(s for s, _ in so), w1)
                if 0.0 < omin <= MP_BEHIND_M and b - a > 1.0:
                    C.mp.append((kind, a, b, omin, False))
    # v1.10 (the v1.8 / v1.9 runs ran > 17 min): overlapping pieces of one kind on the cut merged into one span
    cut_, rest = {}, [t for t in C.mp if not t[4]]
    for t in sorted(t for t in C.mp if t[4]):
        m = cut_.setdefault(t[0], [])
        if m and t[1] <= m[-1][2] + 0.3:
            m[-1] = (t[0], m[-1][1], max(m[-1][2], t[2]), 0.0, True)
        else:
            m.append(t)
    # v1.19: the canopy triangles behind the cut merged into one canopy per overlapping run (nearest distance kept)
    back_c, rest2 = [], [t for t in rest if t[0] != "canopy"]
    for t in sorted(t for t in rest if t[0] == "canopy"):
        if back_c and t[1] <= back_c[-1][2] + 0.3:
            back_c[-1] = ("canopy", back_c[-1][1], max(back_c[-1][2], t[2]), min(back_c[-1][3], t[3]), False)
        else:
            back_c.append(t)
    rest = rest2 + back_c
    C.mp = rest + [t for v in cut_.values() for t in v]
    # v1.21: his planted trees: within TREE_NEAR_M + 1 m of the line on the cut, else behind up to TREE_BACK_M
    C.trees_plan_cut = []
    for x_, y_, dia_, sp_ in MP_TREES:
        s_, o_ = C.su(x_, y_)
        if not (w0 + 1.0 <= s_ <= w1 - 1.0):
            continue
        h_ = TREE_H_M.get(sp_, min(14.0, max(5.0, 1.3 * dia_)))   # v1.26: sourced mature height by species
        if abs(o_) <= TREE_NEAR_M + 1.0:
            C.trees_plan_cut.append((s_, dia_ / 2.0, h_, sp_))
        elif 0.0 < o_ <= TREE_BACK_M:
            C.trees_back.append((s_, o_, None, h_, u"plan:" + sp_))
    # v1.19: the folds = the canopy triangle corners near the line (from 20 m in front to MP_BEHIND_M behind), as s
    C.folds = sorted(s_ for s_, o_ in (C.su(q[0], q[1]) for q in MP_CANOPY_PTS) if -20.0 <= o_ <= MP_BEHIND_M and w0 <= s_ <= w1)
    C.mp.sort(key=lambda t: (-t[3], t[1]))
    C.notes.append(u"line %d trees behind: %d survey symbols (height %.1f m assumed), %d from his plan; %d of his trees on the cut" % (
        C.n, sum(1 for t in getattr(C, "trees_back", []) if t[4] == u"survey"), TREE_SURVEY_H_M,
        sum(1 for t in getattr(C, "trees_back", []) if t[4].startswith(u"plan")), len(getattr(C, "trees_plan_cut", []))))
    C.mp_hard = [(t[1], t[2]) for t in C.mp if t[4] and t[0] in HARD]
    n = {}
    for t in C.mp:
        n[t[0]] = n.get(t[0], 0) + 1
    C.notes.append(u"line %d masterplan pieces on the cut: %s (forms and heights: design intent, ours)" % (
        C.n, u", ".join(u"%s %d" % kv for kv in sorted(n.items())) or u"none"))


def mp_surface(S):
    """the terraces the plan draws on this cut become the finished ground: seat steps of RISE_M stepping down toward
    the stream from the plan edge's survey level to the summer water (design intent)"""
    C = S.C
    for kind, a, b, dist, cut in getattr(C, "mp", []):
        if kind != "terrace" or not cut:
            continue
        down = 1.0 if abs(b - C.s_th) < abs(a - C.s_th) else -1.0     # the end nearer the stream is the low end
        hi_s, lo_s = (a, b) if down > 0 else (b, a)
        z_hi, z_lo = S.ex(hi_s), max(S.ex(lo_s), C.z_th + 0.3)
        if z_hi - z_lo < RISE_M:
            continue
        if S.walled and a < S.walled[1] and b > S.walled[0]:
            continue                                                    # never inside the walled channel
        n = max(1, min(int((z_hi - z_lo) / RISE_M), int(abs(b - a) / 0.6)))
        r_, t_ = (z_hi - z_lo) / n, abs(b - a) / n
        pts = []
        for i in range(n):
            s0, z0 = hi_s + down * i * t_, z_hi - i * r_
            pts += [(s0, z0), (s0 + down * t_, z0), (s0 + down * t_, z0 - r_)]
        if down < 0:
            pts.reverse()
        V = [p for p in S.V if p[0] < a - 1e-6] + [(a, S.surf(a))] + pts + [(b, S.surf(b))]
        S.V = V + [p for p in S.V if p[0] > b + 1e-6]
        S._xs = None
        S.d.setdefault("mp_steps", []).append((a, b, n, r_, t_, down, z_hi))


def _sh(pg, ring, fill, layer, stroke=None, lw=0.08):
    pg.poly([ring], fill=fill, stroke=stroke, lw=lw, layer=layer)


def mp_ground(pg, S, C):
    """paving, cycle path, square, terrace nosings and benches, retaining walls, boulders: on the finished ground"""
    K = S.K
    for kind, a, b, dist, cut in getattr(C, "mp", []):
        if not cut:
            continue
        n = max(2, int((b - a) / 0.5))
        top = [a + (b - a) * i / n for i in range(n + 1)]
        if kind in ("walk", "plaza", "cycle"):
            col, th = (P_CYCLE, 0.12) if kind == "cycle" else (P_PAVE, 0.25)
            _sh(pg, [S.P(x, S.surf(x)) for x in top] + [S.P(x, S.surf(x) - th) for x in reversed(top)], col,
                "proposal ground", INK_CUT, 0.05)              # v1.19.1: hairline edge (read as a dark slab on S4)
            if 0.6 * K >= 0.6:                                              # paving joints
                for x in top[1:-1]:
                    pg.line([S.P(x, S.surf(x)), S.P(x, S.surf(x) - th)], INK_CUT, 0.04, layer="proposal ground")
        elif kind == "wall":
            m = (a + b) / 2.0
            ch_ = getattr(S, "channel", None)
            if ch_ and ch_[0] + 0.5 < m < ch_[1] - 0.5:    # v1.17.3: no plan wall standing in the channel (N5-A)
                continue
            zl, zh = min(S.ex(m - 1.5), S.ex(m + 1.5)), max(S.ex(m - 1.5), S.ex(m + 1.5))
            # v1.16 (600 dpi read: free-standing dark posts on flat ground): where the ground holds no step the
            # plan's wall is a 0.45 m seat wall; the outline thin at sheet scales
            # v1.19.1 (Aras 05:59 "left wall looks weird", S4 s 570: a 0.9 m box standing free on the slope): on a
            # slope the wall is cut, held in the ground from below the low side to a coping flush with the high side
            up = 0.15 if zh - zl >= 0.3 else 0.45
            zb_w = zl - 0.8 if zh - zl >= 0.3 else min(S.surf(m - 0.35), S.surf(m + 0.35))   # v1.17.3: a seat wall
            #                                            starts on the ground (its foot showed under the cut line, N2-A)
            _sh(pg, [S.P(m - 0.35, zb_w), S.P(m + 0.35, zb_w), S.P(m + 0.35, zh + up), S.P(m - 0.35, zh + up)],
                WALL_FILL, "proposal ground", INK_CUT, min(0.25, max(0.04, 0.12 * K)))
            _sh(pg, [S.P(m - 0.45, zh + up), S.P(m + 0.45, zh + up), S.P(m + 0.45, zh + up + 0.12),
                     S.P(m - 0.45, zh + up + 0.12)], P_CONC_LT, "proposal ground")            # coping
        elif kind == "stones":
            rg = random.Random(u"%.1f" % a)
            x = a + 0.4
            while x < b - 0.4:
                r_ = 0.25 + 0.35 * rg.random()
                cx, cy = S.P(x, S.surf(x))
                pg.poly([[(cx + r_ * K * math.cos(t) * 1.3, cy + r_ * K * (0.75 * math.sin(t) + 0.45))
                          for t in [k * math.pi / 8 for k in range(16)]]], fill="9C968A", stroke="6E675E", lw=0.04,
                        layer="proposal ground")
                x += 2 * r_ + 0.3 + 1.2 * rg.random()
    for a, b, n, r_, t_, down, z_hi in S.d.get("mp_steps", []):
        for i in range(n):                                              # precast nosing on every riser, a timber
            s0 = (a if down > 0 else b) + down * (i + 1) * t_         # bench top on every second tread
            z0 = z_hi - (i + 1) * r_
            _sh(pg, [S.P(s0 - 0.12 * down, z0 - 0.0), S.P(s0, z0), S.P(s0, z0 + r_), S.P(s0 - 0.12 * down, z0 + r_)],
                P_CONC_LT, "proposal ground", INK_CUT, 0.06)
            if i % 2 == 0 and t_ >= SEAT_TREAD_M * 0.6:
                zt = z0 + r_
                _sh(pg, [S.P(s0 - down * t_ * 0.85, zt), S.P(s0 - down * 0.15, zt), S.P(s0 - down * 0.15, zt + 0.06),
                         S.P(s0 - down * t_ * 0.85, zt + 0.06)], P_TIMBER, "proposal ground")


def _canopy(pg, S, a, b, g, fade, layer, rg, folds=()):
    """v1.28 (Aras 15 Nov 09:52 "draw our canopies much better like designed ones", his canopy reference): a folded
    roof of triangle facets (a fold wherever one of his plan's canopy triangle corners falls along the cut, every ~6 m
    where none does; ridges and valleys alternating, facets toned alternately), a thin light skin that runs out to
    knife edges, a timber louvre layer under the skin following every fold (slats seen on the cut, a timber band
    behind), a Y-shaped steel column under each valley on a regular bay, a timber deck on the ground under the roof
    (on the cut); heights from v1.26 (valley underside >= ground + 2.30, >= Q500 + 0.60; ridge + 1.8 m ASSUMED)"""
    K = S.K
    fs = []
    for x in folds:
        if a + 1.0 < x < b - 1.0 and (not fs or x - fs[-1] >= 1.5):
            fs.append(x)
    if not fs:
        n_ = max(1, int(round((b - a) / 6.0)))
        fs = [a + (b - a) * k / (n_ + 1) for k in range(1, n_ + 1)] if b - a > 4.0 else []
    xs = [a] + fs + [b]
    q5_ = (S.C.levels.get("q500") or (None,))[0] if hasattr(S.C, "levels") else None
    v_ = max(g + CANOPY_CLEAR_M, (q5_ + CANOPY_Q500_M) if q5_ is not None else -1e9) + CANOPY_T   # v1.26: valley top
    zs = [v_ + (CANOPY_RISE_M if k % 2 == 0 else 0.0) for k in range(len(xs))]
    CANOPY_LO_ = v_ - g
    shell, steel = _mix(P_SHELL, SKY_LOW, fade), _mix(P_STEEL, SKY_LOW, fade)
    shade = _mix(_mix(P_SHELL, P_STEEL, 0.3), SKY_LOW, fade)
    louv = _mix(_mix(P_TIMBER, P_SHELL, 0.35), SKY_LOW, fade)
    slat = _mix(P_TIMBER, SKY_LOW, fade)
    edge_lw = max(0.04, min(0.12, 0.1 * K))
    SK, LV = CANOPY_SKIN_M, CANOPY_LOUVRE_M
    n_f = len(xs) - 1

    def th(k, end):                                                     # skin thickness: knife edges at the two ends
        return 0.03 if (k == 0 and not end) or (k == n_f - 1 and end) else SK

    for k in range(n_f):                                                 # the facets: louvre band, then the skin
        x0, x1, z0, z1 = xs[k], xs[k + 1], zs[k], zs[k + 1]
        t0, t1 = th(k, False), th(k, True)
        l0, l1 = (LV if t0 >= SK else 0.0), (LV if t1 >= SK else 0.0)
        if l0 or l1:
            _sh(pg, [S.P(x0, z0 - t0), S.P(x1, z1 - t1), S.P(x1, z1 - t1 - l1), S.P(x0, z0 - t0 - l0)], louv, layer)
            if fade == 0.0:                                              # slats seen on the cut (one tick per
                n_s = int((x1 - x0) / max(CANOPY_SLAT_M, 0.7 / max(K, 1e-6)))   # 0.7 mm where 0.30 m prints finer)
                for m in range(1, n_s):
                    f_ = m / float(n_s)
                    xm, zm = x0 + (x1 - x0) * f_, z0 - t0 + (z1 - t1 - z0 + t0) * f_
                    lm = l0 + (l1 - l0) * f_
                    if lm > 0.05:
                        pg.line([S.P(xm, zm), S.P(xm, zm - lm)], slat, max(0.03, 0.05 * K), layer=layer)
        _sh(pg, [S.P(x0, z0), S.P(x1, z1), S.P(x1, z1 - t1), S.P(x0, z0 - t0)],
            shell if k % 2 == 0 else shade, layer, steel, edge_lw)

    def under(x):                                                        # the louvre underside at x
        k = max(0, min(n_f - 1, [i for i in range(n_f) if xs[i] <= x][-1] if x >= xs[0] else 0))
        f_ = (x - xs[k]) / max(xs[k + 1] - xs[k], 1e-6)
        return zs[k] + (zs[k + 1] - zs[k]) * f_ - SK - LV

    cols, last = [], None
    for k in range(1, n_f):                                              # Y columns under the valleys, >= 5 m apart
        x, z = xs[k], zs[k]
        if z - g > CANOPY_LO_ + 0.01 or (last is not None and x - last < 5.0):
            continue
        last = x
        cols.append(k)
    if not cols:                                                         # no valley: one Y at mid-span
        cols = [None]
    ch = getattr(S, "channel", None) or (1e9, -1e9)
    on_cut = fade == 0.0
    PL = CANOPY_PLINTH_M if on_cut else 0.0

    def dry(x):                                                          # outside the channel
        return not (ch[0] - 0.5 < x < ch[1] + 0.5)

    def floor(x):                                                        # top of the deck (cut) or the ground
        return S.surf(x) + ((PL + CANOPY_DECK_M) if dry(x) else 0.0)

    if on_cut:                                                           # v1.28.2: stone plinth, timber deck on top
        n_ = max(2, int((b - a) / 0.5))
        run = [((a + (b - a) * i / n_), S.surf(a + (b - a) * i / n_)) if dry(a + (b - a) * i / n_) else None
               for i in range(n_ + 1)]
        seg = []
        for p in run + [None]:
            if p is not None:
                seg.append(p)
                continue
            if len(seg) >= 2:
                _sh(pg, [S.P(x_, z_ + PL) for x_, z_ in seg] + [S.P(x_, z_ - 0.3) for x_, z_ in reversed(seg)],
                    P_STONE, layer, _mix(P_STONE, P_STEEL, 0.4), 0.04)
                for f_ in (0.35, 0.7):                                   # stone courses
                    pg.line([S.P(x_, z_ + PL * f_) for x_, z_ in seg], _mix(P_STONE, P_STEEL, 0.35), 0.03, layer=layer)
                _sh(pg, [S.P(x_, z_ + PL + CANOPY_DECK_M) for x_, z_ in seg] + [S.P(x_, z_ + PL) for x_, z_ in reversed(seg)],
                    P_TIMBER, layer)
            seg = []
    cx_ = [xs[k] if k is not None else (a + b) / 2.0 for k in cols]
    q5_ = (S.C.levels.get("q500") or (None,))[0] if hasattr(S.C, "levels") else None
    glass = _mix(P_GLASS, SKY_LOW, fade)
    mull = _mix(P_STEEL, SKY_LOW, fade)
    for i in range(len(cx_) - 1):                                        # v1.28.2: closed glazed rooms, every other bay
        x0, x1 = cx_[i] + 0.6, cx_[i + 1] - 0.6
        if i % 2 or x1 - x0 < 2.0 or not (dry(x0) and dry(x1)):
            continue
        f0, f1 = floor(x0), floor(x1)
        if q5_ is None or min(f0, f1) < q5_ + CANOPY_Q500_M:              # rooms only above Q500 + 0.60 (EA); v1.28.6:
            #                                            none on a cut with no water levels (the flood level is unknown there)
            continue
        n_ = max(2, int((x1 - x0) / 1.0))
        top = [(x0 + (x1 - x0) * j / n_) for j in range(n_ + 1)]
        _sh(pg, [S.P(x, under(x) - 0.05) for x in top] + [S.P(x1, f1), S.P(x0, f0)], glass, layer, mull, 0.04)
        n_m = max(1, int((x1 - x0) / max(CANOPY_MULLION_M, 0.9 / max(K, 1e-6))))
        for j in range(1, n_m):                                          # mullions
            x = x0 + (x1 - x0) * j / n_m
            pg.line([S.P(x, floor(x)), S.P(x, under(x) - 0.05)], mull, max(0.03, 0.05 * K), layer=layer)
        if on_cut:
            pg.line([S.P(x0, f0 + 1.1), S.P(x1, f1 + 1.1)], mull, 0.03, layer=layer)   # transom
    if on_cut:                                                           # v1.28.2: timber planters in the open bays
        bays = [(cx_[i], cx_[i + 1], i) for i in range(len(cx_) - 1)] or [(a, b, 1)]
        for x0, x1, i in bays:
            if len(cx_) > 1 and i % 2 == 0 and q5_ is not None and min(floor(x0 + 0.6), floor(x1 - 0.6)) >= q5_ + CANOPY_Q500_M:
                continue                                                 # (a glazed bay)
            xm = (x0 + x1) / 2.0
            w = min(CANOPY_PLANTER_M, 0.4 * (x1 - x0))
            if w < 0.8 or not dry(xm - w / 2) or not dry(xm + w / 2):
                continue
            f_ = max(floor(xm - w / 2), floor(xm + w / 2))
            _sh(pg, [S.P(xm - w / 2, f_), S.P(xm + w / 2, f_), S.P(xm + w / 2, f_ + 0.6), S.P(xm - w / 2, f_ + 0.6)],
                P_TIMBER, layer, _mix(P_TIMBER, P_STEEL, 0.4), 0.03)
            _sh(pg, [S.P(xm - w / 2 + 0.1, f_ + 0.6), S.P(xm + w / 2 - 0.1, f_ + 0.6),
                     S.P(xm + w / 4, f_ + 1.1), S.P(xm - w / 4, f_ + 1.15)], P_GREEN, layer)
    for k, x in zip(cols, cx_):
        gx = floor(x)
        if k is not None:
            w = min(CANOPY_Y_ARM_M, 0.35 * (xs[k] - xs[k - 1]), 0.35 * (xs[k + 1] - xs[k]))
        else:
            w = min(CANOPY_Y_ARM_M, 0.25 * (b - a))
        zt = under(x)
        zf = gx + CANOPY_Y_FORK * (zt - gx)
        pg.line([S.P(x, gx), S.P(x, zf)], steel, max(0.05, 0.22 * K), layer=layer)          # the trunk
        for sgn in (-1.0, 1.0):                                                              # the two arms
            xa = x + sgn * w
            pg.line([S.P(x, zf), S.P(xa, under(xa))], steel, max(0.04, 0.16 * K), layer=layer)


def _pavilion(pg, S, a, b, g, fade, layer, rg, towards):
    """a competition pavilion: a timber-and-glass hall under a sedum roof blade that sweeps up toward the stream and
    cantilevers 4 m past the glass, on slender columns, vertical fins (design intent, ours)"""
    K = S.K
    lo_h, hi_h = 4.2, 7.5
    ga, gb = a + (b - a) * 0.12, b - (b - a) * 0.12
    def zr(x):
        t = (x - a) / max(b - a, 1e-6)
        t = t if towards > 0 else 1 - t
        return g + lo_h + (hi_h - lo_h) * t ** 1.6
    glass, steel, green = _mix(P_GLASS, SKY_LOW, fade), _mix(P_STEEL, SKY_LOW, fade), _mix(P_GREEN, SKY_LOW, fade)
    shell, timber = _mix(P_SHELL, SKY_LOW, fade), _mix(P_TIMBER, SKY_LOW, fade)
    _sh(pg, [S.P(ga, g), S.P(gb, g), S.P(gb, zr(gb) - 0.5), S.P(ga, zr(ga) - 0.5)], glass, layer, steel, 0.08)
    x = ga
    while x < gb - 0.1:                                                  # fins
        if 1.2 * K >= 0.6:
            pg.line([S.P(x, g), S.P(x, zr(x) - 0.5)], timber, max(0.04, 0.12 * K), layer=layer)
        x += 1.2
    n = max(6, int((b - a) / 0.5))
    xs = [a + (b - a) * i / n for i in range(n + 1)]
    _sh(pg, [S.P(x, zr(x)) for x in xs] + [S.P(x, zr(x) - 0.45) for x in reversed(xs)], shell, layer,
        _mix(INK_CUT, SKY_LOW, fade), 0.12)
    _sh(pg, [S.P(x, zr(x) + 0.12) for x in xs] + [S.P(x, zr(x)) for x in reversed(xs)], green, layer)
    c = ga + 0.3
    while c < gb:                                                        # slender columns
        pg.line([S.P(c, g), S.P(c, zr(c) - 0.45)], steel, max(0.04, 0.2 * K), layer=layer)
        c += 6.0
    _sh(pg, [S.P(a, g - 0.15), S.P(b, g - 0.15), S.P(b, g), S.P(a, g)], P_CONC, layer)


def _bridge(pg, S, a, b, layer):
    """a footbridge as a thin lens: a 0.35 m timber deck on a shallow steel lens 1.2 m deep at mid-span, blade posts
    and a handrail (design intent, ours)"""
    K = S.K
    # v1.16 (600 dpi read of v1.15.2: N2-A's bridge lay on the stream bed, its plan ends being inside the channel):
    # the deck at the higher bank top within 8 m of each end, the span run out until it lands on the bank
    zl = max(S.ex(a - 0.5 * k) for k in range(17))
    zr = max(S.ex(b + 0.5 * k) for k in range(17))
    z = max(zl, zr) + 0.2
    for _ in range(30):
        if S.ex(a) >= z - 0.4 or a - 0.5 < S.lo:
            break
        a -= 0.5
    for _ in range(30):
        if S.ex(b) >= z - 0.4 or b + 0.5 > S.hi:
            break
        b += 0.5
    n = max(8, int((b - a) / 0.5))
    xs = [a + (b - a) * i / n for i in range(n + 1)]
    low = [z - 0.35 - 1.2 * math.sin(math.pi * i / n) for i in range(n + 1)]
    _sh(pg, [S.P(x, z) for x in xs] + [S.P(x, l_) for x, l_ in reversed(list(zip(xs, low)))], P_STEEL, layer, INK_CUT,
        min(0.2, max(0.04, 0.1 * K)))
    _sh(pg, [S.P(a, z), S.P(b, z), S.P(b, z - 0.12), S.P(a, z - 0.12)], P_TIMBER, layer)
    pg.line([S.P(a, z + 1.1), S.P(b, z + 1.1)], P_STEEL, max(0.05, 0.06 * K), layer=layer)
    x = a
    while x <= b and 1.5 * K >= 0.4:
        pg.line([S.P(x, z), S.P(x, z + 1.1)], P_STEEL, 0.04, layer=layer)
        x += 1.5


def _deck(pg, S, a, b, layer):
    """a water deck cantilevered from the bank: timber on a tapering steel bracket, glass balustrade (design intent)"""
    K = S.K
    z = max(S.surf(a), S.surf(b)) + 0.25                # v1.17.3: the deck clear above the ground (sunk on N1-B)
    _sh(pg, [S.P(a, z), S.P(b, z), S.P(b, z - 0.12), S.P(a, z - 0.6)], P_STEEL, layer, INK_CUT, 0.15)
    _sh(pg, [S.P(a, z), S.P(b, z), S.P(b, z - 0.08), S.P(a, z - 0.08)], P_TIMBER, layer)
    # v1.17.2 (review of v1.17: the glass balustrade box read as a water tank): a top rail on thin posts
    pg.line([S.P(a, z + 1.1), S.P(b, z + 1.1)], P_STEEL, max(0.04, 0.06 * K), layer=layer)
    x = a
    while x <= b + 1e-6:
        pg.line([S.P(x, z), S.P(x, z + 1.1)], P_STEEL, max(0.03, 0.04 * K), layer=layer)
        x += max(1.2, 1.0 / max(K, 1e-6))


def mp_structures(pg, S, C, behind):
    """canopies, pavilions (behind the cut: in elevation, toned with distance; on the cut: in front), bridges, decks"""
    drawn = []
    for kind, a, b, dist, cut in sorted(getattr(C, "mp", []), key=lambda t: (t[4] is False, t[3])):
        if behind == cut:
            continue
        # v1.17.2 (review of v1.17: 3-8 canopies overlapping on N2-B / N5-B): a canopy or pavilion whose span is
        # mostly covered by one already drawn (nearer first) is left out
        if behind and kind == "canopy" and getattr(C, "acb_", None) is not None:
            continue                                    # v1.28.3: canopies behind come from Archicad (AcBuild v1.6)
        if kind in ("canopy", "pavilion"):
            if any(min(b, y) - max(a, x) > 0.3 * (b - a) for x, y in drawn):
                continue
            drawn.append((a, b))
        rg = random.Random(u"%s%.1f" % (kind, a))
        fade = H_FADE * min(1.0, dist / BACK_M) if not cut else 0.0
        layer = "proposal behind" if not cut else "proposal structures"
        g = max(S.surf((a + b) / 2.0), S.ex((a + b) / 2.0)) if cut else (max(S.surf(a), S.surf(b)))
        towards = 1.0 if C.s_th > (a + b) / 2.0 else -1.0
        if kind == "canopy":
            _canopy(pg, S, a, b, g, fade, layer, rg, getattr(C, "folds", []))
        elif kind == "pavilion":
            _pavilion(pg, S, a, b, g, fade, layer, rg, towards)
        elif cut and kind == "bridge" and C.cross is not None:     # v1.12: only where the cut crosses the
            #                                            stream (a B cut along the bank met the bridge on land)
            _bridge(pg, S, a, b, layer)
        elif cut and kind == "deck":
            _deck(pg, S, a, b, layer)


def mp_planting(S):
    """the plan's green and water planting on the cut: meadow, a tree every ~9 m on 'kesin yesil' (sure green), reeds
    on 'su bitkii' (design intent)"""
    d = S.d
    for kind, a, b, dist, cut in getattr(S.C, "mp", []):
        if not cut:
            continue
        if kind == "green":
            d["grass"].append((a, b))
            rg = random.Random(u"t%.1f" % a)
            x = a + 3.0 + 5.0 * rg.random() if not MP_TREES else b    # v1.21: his own trees when the plan has them
            while x < b - 3.0:                                  # trees 12-20 m apart, 7-11 m tall (design)
                d["trees"].append((x, 3.0, 7.0 + 4.0 * rg.random(), 0))
                x += 12.0 + 8.0 * rg.random()
        elif kind == "reeds":
            d["reeds"].append((a, b, 2.0))
    for s_, r_, h_, sp_ in getattr(S.C, "trees_plan_cut", []):   # v1.21: his trees on the cut (v1.23: species)
        d["trees"].append((s_, r_, h_, sp_))
    for kind in set(k for k, a, b, dist, cut in getattr(S.C, "mp", []) if cut and k in MP_LABEL):
        a, b = max(((t[1], t[2]) for t in S.C.mp if t[0] == kind and t[4]), key=lambda r: r[1] - r[0])
        d["callouts"].append(((a + b) / 2.0, None, MP_LABEL[kind]))


PLANT_DEN = 75.0                   # v1.7: the engine's planting pieces are sized for 1:75 (engine SCALE)


def at_plant_scale(E, pg, S, draw):
    """v1.7 (Aras 15:28 "the grass is too long please be careful about the proportions", 15:34 node sections): the
    planting drawn at the engine's own 1:75 and scaled down as a whole to the page scale, so culms, blades, plumes and
    their spacing keep true proportions (they were fixed page mm: a reed mass filled the stream at 1:1000-3000)"""
    K, k75 = S.K, 1000.0 / PLANT_DEN
    if K >= k75 * 0.999:
        draw(pg)
        return
    tmp = E["Page"](u"plants", u"")
    E["K"] = S.K = _ENGINE_K[0] = k75
    try:
        draw(tmp)
    finally:
        E["K"] = S.K = _ENGINE_K[0] = K
    o = (S.X0, S.Y0)
    pg.items += [_scale_it(it, K / k75, o, lw=True) for it in tmp.items]


def a3_sheet(E, cuts, log):
    """v1.7: all cuts on ONE A3 landscape sheet: the grid and the one scale (the largest that lets every cut fit its
    cell) chosen together; a cut still too big at the smallest scale is scaled down to its cell and its scale texts
    say the scale it prints at"""
    W, H = A3
    size = {}

    def fits(C, d, cw, ch):
        if (C.name, d) not in size:
            b = items_bbox(draw_cut(E, C, SEASON, d, 0.0, 0.0)[0].items)
            size[(C.name, d)] = (b[2] - b[0], b[3] - b[1])
        w, h = size[(C.name, d)]
        return w <= cw and h <= ch
    # v1.15 (Aras 21:33 "do a proper check of the drawings and sections ... needs a lot of to improve"; the v1.14 sheet
    # left about 60 % of the A3 empty with every cut at one small common scale): each cut gets its own scale, the
    # largest that fits its cell, then is fitted to the cell exactly; the grid is the one that prints the cuts largest
    def pick(C, cw, ch):
        d = A3_DENS[-1]                                 # from the smallest scale up (the cheap draws first);
        fits(C, d, cw, ch)                              # v1.15.2: its size measured even when nothing larger fits
        for d_ in reversed(A3_DENS[:-1]):               # stop at the first that no longer fits (run time, v1.14 284 s)
            if not fits(C, d_, cw, ch):
                break
            d = d_
        w, h = size[(C.name, d)]
        return d, min(cw / w, ch / h)
    best = None
    for nc, nr in A3_GRIDS:
        if nc * nr < len(cuts):
            continue
        cw = (W - 2 * A3_MARGIN - (nc - 1) * A3_GAP) / nc
        ch = (H - 2 * A3_MARGIN - A3_TITLE - (nr - 1) * A3_GAP) / nr
        picks = [pick(C, cw, ch) for C in cuts]
        score = sum(f_ / d_ for d_, f_ in picks)
        if best is None or score > best[0]:
            best = (score, nc, nr, cw, ch, picks)
    _, nc, nr, cw, ch, picks = best
    items = [("text", u"SECTIONS N1-A ... N6-B · both banks", A3_MARGIN, H - A3_MARGIN - 5.0, 5.0, E["INK"], True,
              "L", "title", None, None)]
    dens = []
    for i, C in enumerate(cuts):
        den = picks[i][0]
        pg = draw_cut(E, C, SEASON, den, 0.0, 0.0)[0]
        b = items_bbox(pg.items)
        w, h = b[2] - b[0], b[3] - b[1]
        f = min(cw / w, ch / h)
        # no 1:x printed (Aras 15:25 "the scale is not important"); the scale bar in metres stays true when scaled
        its = [_shift(it, -b[0], -b[1]) for it in pg.items
               if not (it[0] == "text" and re.match(u"^(SCALE )?1:[0-9]", it[1]))]
        # v1.15: titles keep one size on every cut (N1-A printed its title smaller than the rest)
        its = [(_scale_it(it, f) if not (it[0] == "text" and it[8] in ("title", "band")) else   # v1.16.1: band words too
                (it[0], it[1], it[2] * f, it[3] * f) + tuple(it[4:])) for it in its]
        dens.append(int(round(den / f / 50.0) * 50))
        log.append(u"%s: drawn at 1:%d, fitted x%.2f to its A3 cell (prints at about 1:%d)" % (C.name, den, f, dens[-1]))
        col, row = i % nc, i // nc
        x0 = A3_MARGIN + col * (cw + A3_GAP)
        y0 = H - A3_MARGIN - A3_TITLE - (row + 1) * ch - row * A3_GAP
        items += [_shift(it, x0, y0 + (ch - h * f)) for it in its]
    den = max(dens)
    log.append(u"one A3 landscape sheet, %d x %d grid, cells %.0f x %.0f mm, 1:%d, %d cut(s)" % (
        nc, nr, cw, ch, den, len(cuts)))
    return den, [(W, H, items)]


def main():
    global MAX_LEN_M
    t0 = time.time()
    log = []
    E = load_engine(log)
    E["_DRY0"] = E["DRY"]
    E["_THALWEG0"] = tuple(E["THALWEG"])                # v1.17.4: the engine's S4 low point, before any cut
    _ENGINE_W[:] = [E["text_w"]]
    den = int(globals().get("scale") or 500)
    MAX_LEN_M = 2.0 * float(globals().get("half_width") or 100)
    CL, cum = load_centreline(log)
    wired = _lines_in()
    s4a, s4b = E["S4_A"], E["S4_B"]
    lines = [(u"L%d" % (i + 1), a, b) for i, (a, b) in enumerate(wired)] or named_lines(log) or model_lines(log)   # v1.9: the json v2 first
    if not wired:                                       # v1.9 (Aras 16:12 "Section should cross all of the zone
        MAX_LEN_M = 1e9                                 # area"): the node cuts are drawn whole, frame edge to edge
    if not lines:
        lines = [(u"S4", s4a, s4b)]
        log.append(u"no lines: S4 (the 27 Oct cut) drawn")
    cuts = []
    for i, (name, a, b) in enumerate(lines):
        C = Cut(i + 1, a, b, name, name)
        for (p, q) in ((a, b), (b, a)):
            if math.hypot(p[0] - s4a[0], p[1] - s4a[1]) < 1.0 and math.hypot(q[0] - s4b[0], q[1] - s4b[1]) < 1.0:
                C = Cut(i + 1, s4a, s4b, u"S4", u"S4")
                C.is_s4 = True
        cuts.append(C)
    if not any(C.is_s4 for C in cuts):                  # v1.10 (four-seasons page, Aras 16:37 wants the S4 look
        C = Cut(len(cuts) + 1, s4a, s4b, u"S4", u"S4")  # back): S4 cached every run, not on the sheet
        C.is_s4, C.cache_only = True, True
        cuts.append(C)
    BM = load_basemap(log)
    MP = mp_load(log)                                   # v1.8: the masterplan (MasterplanBase cache)
    if BM:                                              # v1.18.1: the Kızıl Avlu hall (the basemap has no outline)
        BM["buildings"] = list(BM["buildings"]) + red_hall_load(log)
    # the survey is read ONCE for all lines (build once, Aras 29 Oct): the box holds every line's corridor
    pad = max(CORRIDOR_STEPS[-1], SLOPE_HALF + 20.0) + HYD_HALF
    xs = [p[0] for C in cuts for p in (C.A, C.B)]
    ys = [p[1] for C in cuts for p in (C.A, C.B)]
    survey = read_survey((min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad), log)
    res = []
    pages = []
    node_cache = {}
    os.makedirs(OUT_DIR, exist_ok=True)
    for C in cuts:
        try:
            C.survey = survey
            prog(u"%s: build" % C.name)
            build_cut(C, CL, cum, E, log, BM)
            prog(u"%s: built (%d buildings, window %.0f m); masterplan" % (C.name, len(C.bld), C.window[1] - C.window[0]))
            mp_for(C, MP if (not C.is_s4 or S4_FROM_B19) else {})   # v1.18: S4 from his masterplan too
            prog(u"%s: %d masterplan spans" % (C.name, len(C.mp)))
            if not getattr(C, "cache_only", False):
                pages.append(C)
        except Exception as ex:
            import traceback as _tb
            log.append(u"FLAG section %s not drawn: %s: %s | %s" % (C.name, type(ex).__name__, ex,
                                                                    u" / ".join(_tb.format_exc()[-500:].splitlines())))
            log += C.notes
            continue
        log += C.notes
        node_cache[C.name] = cut_cache(E, C)
        res.append(dict(name=C.name, A=list(C.A), B=list(C.B), window=list(C.window), look=C.look,
                        bed_low=[round(C.s_th, 2), round(C.z_th, 2)], slope=C.slope,
                        levels=dict((k if isinstance(k, str) else u"%s %.3g m3/s" % k, round(v[0], 2))
                                    for k, v in C.levels.items()),
                        marks=[[round(s_, 2), w_] for s_, w_ in C.marks], trees=[round(s_, 2) for s_ in C.trees],
                        roads=[[round(a, 2), round(b_, 2)] for a, b_ in C.roads],
                        buildings=[dict(s=[round(t[0], 2), round(t[1], 2)], h=t[3], cut=t[4], behind_m=round(t[5], 1))
                                   for t in C.bld]))
    if pages:
        den, pages = a3_sheet(E, pages, log)
        p = write_pdf(os.path.join(OUT_DIR, u"Sections.pdf"), pages,
                      u"Sections %s, both banks" % u", ".join(r_["name"] for r_ in res))
        log.append(u"%s  %s" % (p, time.strftime("%H:%M:%S")))
        write_review(p, log)
    else:
        log.append(u"FLAG no section drawn: no PDF written")
    os.makedirs(CACHE_DIR, exist_ok=True)
    pj = os.path.join(CACHE_DIR, "sections.json")
    with open(pj, "w", encoding="utf-8") as f:
        json.dump(dict(version=VERSION, run=time.strftime("%Y-%m-%d %H:%M:%S"), scale=den, cuts=res), f,
                  ensure_ascii=False, indent=1)
    log.append(u"%s  %s" % (pj, time.strftime("%H:%M:%S")))
    # one file per cut (cuts/<name>.json: the page items per scale) so a node page loads only its own two;
    # cuts.json = the index with everything else
    cd = os.path.join(CACHE_DIR, "cuts")
    os.makedirs(cd, exist_ok=True)
    for f_ in glob.glob(os.path.join(cd, "*.json")):
        os.remove(f_)
    for nm, e in node_cache.items():
        with open(os.path.join(cd, u"%s.json" % nm), "w", encoding="utf-8") as f:
            json.dump(e.pop("items"), f, ensure_ascii=False, separators=(",", ":"))
        e["items_file"] = u"cuts/%s.json" % nm
    pc = os.path.join(CACHE_DIR, "cuts.json")
    with open(pc, "w", encoding="utf-8") as f:
        json.dump(dict(version=VERSION, run=time.strftime("%Y-%m-%d %H:%M:%S"), season=SEASON,
                       origin=u"draw_cut(E, C, SEASON, den, 0, 0): x right, y up, mm; bbox = [x0, y0, x1, y1]; "
                              u"items_file (next to this file) = {scale: {bbox, items}}",
                       cuts=node_cache), f, ensure_ascii=False)
    log.append(u"%s (%d cut(s) x scales %s, for the node pages)  %s" % (
        pc, len(node_cache), u"/".join(str(d) for d in NODE_SCALES), time.strftime("%H:%M:%S")))
    flags = [l for l in log if l.startswith(u"FLAG")]
    return u"%s\n%s %s, %d of %d section(s) drawn, %d FLAG line(s), %.1f s" % (
        u"\n".join(log), GH_LABEL, VERSION, len(res), len(cuts), len(flags), time.time() - t0)


# v1.6.2, Aras 14 Nov 10:44 UTC: "all scripts should produce PNG's aswell which should be optimized for your viewing":
# the review tiles next to the PDF (one band per cut, trimmed to ink, 200 ppi, tiles <= 1560 px wide)
def write_review(pdf, log):
    """the review PNGs by the shared writer pc_review of Data/bergama_pages_common.py (v3: the WHOLE page, never
    cropped, Aras 14 Nov 11:26 UTC) into output/bergama_sections/review/"""
    out = os.path.join(OUT_DIR, "review")
    cp = os.path.join(DATA_DIR, "bergama_pages_common.py")
    try:
        ns = {"__name__": "bergama_pages_common", "__file__": cp}
        with open(cp, encoding="utf-8") as f:
            exec(compile(f.read(), cp, "exec"), ns)
        ns["pc_review"](pdf, out, log)
    except Exception as ex:
        log.append(u"FLAG review PNGs not written: %s could not run (%s: %s); refresh the kit" % (
            cp, type(ex).__name__, ex))


def _shift(it, dx, dy):
    t = it[0]
    if t == "poly":
        return (t, [[(p[0] + dx, p[1] + dy) for p in r] for r in it[1]]) + tuple(it[2:])
    if t == "line":
        return (t, [(p[0] + dx, p[1] + dy) for p in it[1]]) + tuple(it[2:])
    if t == "circle":
        return (t, it[1] + dx, it[2] + dy) + tuple(it[3:])
    if t == "text":
        return (t, it[1], it[2] + dx, it[3] + dy) + tuple(it[4:])
    if t == "image":
        return (t, it[1] + dx, it[2] + dy) + tuple(it[3:])
    return it


# ---- Grasshopper wiring (same in every script) ----
def chain_fire(v, key):
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
    return ("done " if ok else "ERROR ") + time.strftime("%H:%M:%S") + ".%02d" % int((time.time() % 1) * 100) + \
        " · %.0f s" % secs if ran else None


def write_log(text):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, LOG_NAME), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    return text


if "ghenv" in globals():
    import scriptcontext as _sc
    _k = "bergama_" + OUT_FOLDER
    try:
        _k += ":" + str(ghenv.Component.InstanceGuid)   # noqa: F821
    except Exception:
        pass
    _pressed = any(v is True for k, v in list(globals().items())
                   if not k.startswith("_") and isinstance(v, bool) and k not in ("True", "False", "done")) or \
        any(chain_fire(v, _k + "_chain") for k, v in list(globals().items()) if not k.startswith("_") and k != "done" and isinstance(v, str))
    if _pressed:
        _t0 = time.time()
        try:
            _res = main()
        except Exception as _ex:
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-900:])
        _sc.sticky[_k + "_log"] = write_log(_res)
        _sc.sticky[_k + "_status"] = ("ERROR" if _res.startswith("ERROR") else
                                      time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky[_k + "_done"] = done_text(True, not _res.startswith("ERROR"), time.time() - _t0)
        _sc.sticky[_k + "_ver"] = VERSION
    if _sc.sticky.get(_k + "_ver") != VERSION:
        for _s in ("_log", "_status", "_done"):
            _sc.sticky.pop(_k + _s, None)
    done = _sc.sticky.get(_k + "_done", "idle")
    log = _sc.sticky.get(_k + "_log", "Press the Button to export to " + OUT_DIR)
    print(log)
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(_k + "_status", "idle")  # noqa: F821
    except Exception:
        pass
