# r: numpy
"""
THE SELINUS SEAM  -  land-use board and technical analyses for Bergama, one Grasshopper component (v47)
Rhino 8 > Grasshopper > "Python 3 Script" component. No plugins. The technical analyses run on numpy: the first
line "# r: numpy" makes Rhino 8 install it on the first run (internet needed once).

NEW IN v47 (2026-10-27, Aras, booklet Prompt 5 task 3a, p.22 "Which plant goes where": "it is not a shading diagram"):
  * The shade engine (T3) also sums every minute the sun is up on all 31 days of July (crowns in leaf): the mean July
    day's hours in shade on the 1 m grid. Its stored shade is computed again once (method version shade 4 -> 5).
  * New drawing "06a Shade along the stream" (booklet crop drw_shade_strip, drawn for 392 mm on the booklet page, every
    word 7.5 pt): hours in shade on the mean July day at ground level on the left bank, the bed and the right bank,
    every 25 m on the tree crown cover chart's chainage (bed = open cells inside the stream's outline; banks = open
    cells within 15 m beyond the channel's edge), 2 h colour steps from sun to shade, each row's mean, the covered
    reaches hatched (no value), bridges as ticks; a context line and the method, labelled computed. Without shade
    results (no bergama_environment.json, or mode "drawings") it is left out and the log says p.22 shows the tree
    crown cover instead.
  * The tree-cover chart is now "TREE CROWN COVER · BANK BY BANK, EVERY 25 M" (crop drw_tree_cover, caption "Tree
    crown cover along the banks, every 25 m"): no shade claim in its context line, no section markers under it.

NEW IN v46 (2026-10-27, Aras 17:34, booklet Prompt 3 "movement and the city"):
  * Every movement map and the heritage loop at ONE scale: the whole site frame at 1:10,000 on the booklet page, on
    the frame's own axes (one north), in the masterplan's base and layer order (ground, green, water, buildings,
    bridges, roads); the scale bar (0-400 m, "m" beside it) and the north arrow sit UNDER each map, never on it.
  * How people use it (analysis, p.8): the proposed streamside spine and its stops are gone from the map, the legend
    and the notes; walking today and driving today are each a map of their own at the same scale under it.
  * The proposal (p.10) is drawn soft over the crisp base: walkable reach from the masterplan's hubs as a gradient
    along the streets, footways and new crossings (computed: Tobler slope, 100 m steps to the method's 800 m), the
    changed roads, truck route and bus routes as soft bands, crossings and hubs as fading fields (proposal tints
    multiply over the base: the PDF's blend mode).
  * Commercial spines (p.10): the caption in full under the scale bar (the bar covered it).
  * Writes cached/selinus_board/city_context.json: the light context of the city link's shops plan (homes by the
    sections' building types, streets by class, the stream, bridges K1-K6).

NEW IN v45 (2026-10-27, Aras 17:34, booklet Prompt 2 "site and stream edge"):
  * No section lines on any map (plan 01, how people use it, the movement maps): each sections page gets ONE key map
    instead (the whole site frame at 1:50,000, every cut thin, this page's cuts in ink with their names; booklet crops
    sec_sections_key_1 / _2, set in the booklet page's title band). The cuts lose their small locators and their own
    scale words (the page states 1:2,500 once; the cuts' scale search now starts at 1:2,500, as Aras asked); the
    building types under them are drawn at the cuts' scale.
  * Plan 01 for the booklet page beside the new site readings: K names 9 pt, C and photo numbers 7.5 pt, placed clear
    of each other on leaders where needed; scale bar (numbers 7 pt under it) and north arrow under the map, never on
    it; the stream's name 8 pt; its booklet legend leaves out what the readings key (ground and green, edge types).
  * New drawing "05c Site readings" (crop drw_site_readings): the six bank readings (accessible, visible, permeable,
    enclosed, disconnected, transformable) as bars and the site frame's land use as a ring with its key, in plan 01's
    colours (old p.4 folded into p.2).
  * New drawing "06b The stream edge and where we can build" (crop drw_edge_build; replaces "what meets the water"):
    the whole site frame at 1:5,000 in two stacked strips in the masterplan's tones, the edge type every 4 m on both
    banks, walls and embankments, the ground open to change hatched (open ground, parking and yards, loose grass or
    scrub, areas computed on the run), bridges K1-K6, photo viewpoints 1-8 with view cones from each photo's own
    compass bearing and focal length; the photos beside it with one-line captions; edge shares, walled and embanked.
  * The photos are numbered in the order they were taken (upstream to downstream) on every drawing.

NEW IN v44.1 (bugfix + laptop speed, Aras 27 Oct 16:24-16:27): the worker processes for terrain heights and section
drawings failed on Aras's PC ("SyntaxError: invalid syntax"), so that work ran on one core: the workers now put
Rhino's module folders AFTER their own Python's (a folder of Rhino's could hold a module of the same name that is not
Python 3), and the log names the file and line if a worker still fails. The text under the component shows the
pasted version at once (it showed a fixed "v40"), idle, without the old run's time. Output unchanged.

NEW IN v44 (2026-10-27, Aras 11:07, booklet pages 4-8; revision_2026-10-27/PHASE2_SPEC.md):
  * "What meets the water" (p.5): the site at the largest round booklet scale that fits an A3 page (cut into stacked
    pieces along its length, each piece cut to its own frame), photo viewpoints as 12 pt numbers on discs, bridges
    K1-K6 at 12 pt; the edge types' shares of the bank length and walled / embanked rings beside the map, in the same
    crop. Keyword captions under the site photos (the photo index's own words; Roman bridge K3 / K4 named).
  * How people use it (p.6): "walking / driving today" show only the 5 busiest named streets (the engine's street
    table), coloured and named, the rest grey; the change maps are gone. New drawings: the commercial spines
    (restored from v19-v32.1, "07 Commercial spines"), the masterplan's proposal (masterplan_results.json
    "movement": roads with their notes and index today -> with it, truck route, crossings, hubs by role, later bus
    routes; the movement engine run with it), the city heritage loop, and the walking effort (Tobler) proof map.
  * Sections (p.7-8): the building types under the last cuts at a round scale; callout words two characters apart;
    the historic city wall line and the covered stream marked where a cut crosses them; the cuts' scale words are
    the sheet's own (the booklet printed 1:4,136).
  * No placeholder drawing without section lines (logged); no "Analyses: survey + open data" line.

NEW IN v43 (2026-10-26, Aras 07:38): the site photos for the booklet go to Downloads/Bergama/cached/booklet_images/
  (no longer Downloads/Bergama/booklet_images/; the old folder is removed on the run). Nothing else changed.

NEW IN v42 (2026-10-26, Aras's deck review 07:06, pages 02, 07, 09-11):
  * Sections across the stream: every cut the survey's sec_lines layer holds (S1-S8) at ONE round scale, whole
    cuts in rows (two side by side where they fit), on at most two booklet pages ("Sections across the stream S1-.."
    drawings, booklet crops sec_sections_1 / sec_sections_2). The scale is the largest of 1:1,000 / 1:2,000 /
    1:2,500 / 1:5,000 at which they fit; a cut too long for a row is cropped to the part around the stream (at
    least 70 % of it kept, its title says so), never stretched. The old one-drawing-per-cut layout is gone.
  * New drawing "What meets the water" (p.07): the site plan with the edge types along both banks (built, street,
    walkable, planted, parking, loose), walled and embanked banks, bridges K1-K6, the cuts and the photo viewpoints
    numbered as under the photos; one bar of each edge type's share of the bank length. Booklet crop drw_edge_plan.
  * A context line (what it shows, why, what to take from it) under the title of plan 01, the tree cover, the edge
    plan and the cuts; their figures are computed on the run.
  * Booklet blocks: plan 01's crop carries "geo" (its frame corners in survey x, y and in crop mm) so the farms map
    can be laid on this plan.

NEW IN v41 (2026-10-26, Aras 06:35 "these lines in what is there looks weird"):
  * Plan 01 and every map with building outlines: the pale outline runs only round the outside of a footprint as
    the survey draws it; the lines where the script cuts one footprint into buildings along its party walls (long
    straight cuts, often crossing) are no longer drawn, so a block reads as one mass. Buildings, floors and every
    figure are unchanged.
  * Round scales only (Aras 06:35): the cross-sections and the long section along the spine are drawn at the round
    scale at or just below the one that fits (1:500, 1:1,000, 1:2,000, 1:2,500 ...), never 1:750.

NEW IN v40 (2026-10-25, Aras 21:38-21:52, booklet/CROP_SPEC.md: the booklet shows the sheets' own drawings):
  * Plan 01 "what is there": the URBAN FABRIC layer is back (the v28 / bergama_fabric_green v10 fabric map): every
    building by its fabric type (old town, planned apartment blocks, planned low-rise houses, small irregular houses
    and the survey's shacks, civic and industrial halls, under construction, monuments, mosques), the same rules and
    data (fabric_types), in palette v1.4 roles; its legend gives each type's share of the built footprint.
  * Plan 01: bridges K1-K6 as ticks across the stream, conflicts C1-C6 and photo viewpoints 1-8 as dots, each with a
    plain short label placed clear of the others (no white roundels or boxes). Plan 07: working-area names without
    the white box. Wording: "streamside spine"; no caveat words on the tables.
  * S1 axonometric: no contour lines; its callouts and stream words without white halos.
  * Booklet: the separate booklet drawings (A1-A7 frames) are gone. booklet/blocks.json lists one "crop" per panel
    of every sheet this board writes (Selinus_drawings, Selinus_sections, the axonometric, T1-T8: one per map), the
    panel's rectangle in mm on its sheet PDF, from the layout's own numbers, with caption, scale and legend.
    booklet/results.json keeps every key it had.
  * The stream's tree cover (drawing 06): each bank's distance bands named beside their rows, the stream between the
    banks with its covered reaches drawn on it and the bridges across it, a distance axis every 500 m, a drawn key.
  * Sections: the words at the water (stream width and depth, bed level, bank edges) in one band right under the cut
    ground, on short leaders; no caveat words on the drawing (they go to the log).
  * New drawing "Section along the spine": the masterplan's streamside spine as one long developed section, cut by
    the same section engine, at one scale for lengths and heights, the stops 1-8 marked above it.

OLDER VERSIONS: their notes are in HISTORY.md (repo SupFlyn/BergamaProjectScripts, src/selinus_board/).

DATA PRIORITY (v16: measured data only; nothing is drawn or analysed from a guess)
  1. The 1/1000 survey (halihazir DWG) open in this Rhino file: building footprints by type,
     surveyed floor counts, terrain (survey points, contours, spot heights), walls, slopes,
     stairs, bridges, stream banks, road edges, park boundaries, tree symbols, minaret symbols.
  2. Overture Maps places (bergama_places.geojson): shops, cafes, offices, heritage sites -> uses and monuments.
  3. OpenStreetMap (bergama_osm.osm): street names, footpaths, green areas, heritage tags,
     the Selinus centreline, and buildings missing from the survey.
  4. Published figures: KGM traffic counts (two-way AADT; heavy share = vehicles over 3.5 t from KGM's class counts,
     v22; KGM's printed truck share in brackets): 2023 provincial roads 35-04 section 1
     (3,087 vehicles/day, 17.46 % [8 %]) and 35-05 section 3 (4,069, 15.34 % [6 %]); 2024 state road 240-01 (D240)
     section 1 (22,053, 20.82 % [11 %]), section 2 (14,490, 21.58 % [13 %]) and section 3 (13,683, 21.39 % [15 %]);
     Red Basilica heights (hall walls 19 m, rotundas 18 m).
  Where a value was not measured it is derived from measurements only, and every sheet says how:
     floors of unlabelled buildings = the floor count shared by most of the 5 nearest surveyed buildings
       (tested on the 2,825 surveyed ones: same count 71 %, within one floor 96 %);
     street widths = surveyed road edge to road edge, else frontage to frontage; otherwise none (thin line);
     stream bed = surveyed bed levels, between them interpolated along the stream from the surveyed depths;
     roads without an official traffic count (v16.3): the EU GPG default flow of their street type, scaled by the
       nearest KGM count of the same type (DERIVED, listed on the sound sheet street type by street type).
  5. Technical analyses (bergama_environment.json, version 2): the PVGIS-SARAH2 typical meteorological year 2005-2020,
     every hour (EU JRC: sun from SARAH-2; air temperature, humidity, wind, long-wave sky and pressure from ERA5);
     PVGIS terrain horizons every 100 m over the frame; Landsat 8/9 surface temperature, the mean of every clear
     scene of each season; tree crowns from the Meta / WRI 1 m canopy height map, each with its leaf type
     (Copernicus CLC+ Backbone 2021, else its own Sentinel-2 seasonality) and the deciduous leaf-out and leaf-fall
     days measured on Sentinel-2 2019-2025 (16 April, 14 November).

PERIOD AVERAGES (v16): every technical map and section is an average over a period, never one moment.
  shade      hours out of the sun on the four key days (equinoxes, solstices) and on the mean day of the year,
             every minute the sun is up
  radiation  mean kWh/m2 per day of each season, from every hour of the typical year
  wind, air temperature, felt temperature (UTCI)   means over the hours of each season in the input hours window
             (daylight by default); UTCI also as the share of those hours in each heat-stress class
  surface heat   the mean of every clear Landsat scene of each season; sound   Lden (a yearly level)

INPUTS (rename on the component). Type hints are not needed (v16.1): every input works with "No Type Hint" and on
Item or List Access, and paths may be typed with or without quotes. On the first run the component sets itself up:
the section and noise inputs are switched to List Access and the missing inputs below and the "info" output are
added (press the button again after that).
  osm_path       str                 bergama_osm.osm (empty = Downloads/Bergama/Data/)
  places_path    str                 bergama_places.geojson (empty = Downloads/Bergama/Data/)
  section_lines  Curve, LIST ACCESS  any number of lines across the stream (Top view); one land-use section each.
                                     Empty = section placeholders on the pages
  run            bool                Button (v37; bake / build also work). The script does NOTHING until the button is pressed; each press
                                     reads the file, analyses and bakes once (styled vectors: hatches, curves, text;
                                     the technical sheets add their rendered maps as picture frames)
TECHNICAL SECTION INPUTS (Curve, LIST ACCESS, Top view; any number of lines each; drawn when run is technical/both):
  sound_sections  Lden and the day, evening and night levels in the plane of each line
  heat_sections   Landsat surface temperature along the ground, roofs and water under each line, four seasons
  shade_sections  hours out of the sun at every point of the plane: the four key days and the mean day of the year
  solar_sections  mean kWh/m2 per day of each season on the ground, the cut roofs and the cut facades
  wind_sections   mean wind speed at every height of the plane over each season's hours (input hours)
  air_sections    mean dry bulb at every height of the plane over each season's hours
  felt_sections   mean UTCI at every point of the plane over each season's hours
  (the same line may go into several inputs: its geometry, sky and wind shelter are computed once and shared)
OPTIONAL INPUTS:
  frame          Curve   closed rectangle (any rotation) = study area. Empty = the analysis range, SITE_FRAME_LK (v36)
                         (tightest rotated rectangle around its buildings and stream banks)
  layout         str     v33: no longer used; the button always builds the separate drawings (Aras Q13)
  title, subtitle, credit  str
  channel_depth  float   stream bed depth below the banks, if you measured it on site: overrides the depth
                         interpolated from the surveyed bed levels                (empty = from the survey)
  mode           str     (v37: was run) what the button builds: "drawings" (land-use pages, sections and drawings),
                         "technical" (only the analyses and their sections; needs env_path) or "both" (default when
                         env_path is given, v26; without it the land-use part only).
                         0 / 1 / 2 also work, so a Value List or slider can drive it
  environment    bool    (older switch) True = "both" when run is empty
  env_path       str     bergama_environment.json (version 2): weather year, terrain horizons, Landsat seasons,
                         tree crowns with their leaf types. Version 1 still works for sound, heat, shade and
                         radiation (wind, air and felt temperature need the hourly weather of version 2)
  focus          Curve   area for the radiation sheet (default v16.5: the whole frame; v16.4 took the densest
                         420 x 210 m stretch of the stream)
  noise_points   Point   (list) where you measured sound on site; noise_db: the LAeq values, same order
  noise_palette  str     sound band colours: empty = one graded run, pale green (quiet) to deep maroon (loud), each
                         band darker than the one before (default, v16.4); "brussels" (the colour order of the Brussels
                         noise map, green, yellow, red, then blue and violet, over 11 DIN-style 5 dB classes 35-80 dB(A):
                         not the Brussels classes or colours), "coloring" (Coloring Noise / DIN 45682
                         draft) or "din" (DIN 18005-2 classic)
  hours          str     the hours the wind, air and felt temperature means take: "daylight" (default, sun above
                         the horizon), "all" (day and night) or a local range such as "10-17" (added on first run)
  sheet_mm       float   printed page width in mm                              (406.4 = 16:9 at 16 in)
  texture        bool    trees, shadows, seams, hatching                       (True)
  spine, spine_car, bridges, car_closed   Curves (list)   v33: a proposal for the movement potential (drawing 07):
                         a walking spine (joins the streets it crosses), a street that also carries cars, footbridges
                         (joined at their ends), streets made car-free. attractors  Points (list): new destinations.
                         Nothing wired = today only
OUTPUTS:
  info        report: what was read, warnings, timings, what was reused from earlier runs
  drawings    frame rectangle of every baked page / drawing / sheet (also sent to "preview")
  names       their names, same order
  footprints  building footprints (survey coordinates)   floors / uses: per footprint, same order
  cuts        the land-use section lines actually used

WHAT GETS BAKED (layers LU_PAGES and LU_DRAWINGS, one Rhino group per drawing)
  pages:    01 the fabric: plan + legend, urban fabric (building types, monuments in colour), intensity,
               distribution, readings, networks; streets drawn at their surveyed width on every map
            02 the seam: thresholds with the section lines, the key question, the section index and key, sources
            03 ... the cuts, three sections a page (buildings at their floors and type, the bed at its surveyed
               level, behind the cut the buildings, ground and trees beyond)
  drawings: every drawing separately at a comfortable size, framed with a cutting margin
  technical (layer LU_TECH): T1 sound, T2 surface heat, T3 shade, T4 solar radiation, T5 wind, T6 air temperature
            (dry bulb), T7 felt temperature (UTCI), each analysis over a top view of the 3D site; under each sheet
            its sections, one sheet per line (T1.1, T1.2 ...), four strips at true scale. Maps and section pictures
            are also saved as PNG in "selinus_technical_maps" in Downloads/Bergama/output/selinus_board

KEPT BETWEEN RUNS: every analysis result is stored in Downloads/Bergama/cached/selinus_cache (and in Rhino's memory for the
session), found only by the fingerprint of everything it was computed from, so nothing stale is ever reused;
unchanged maps are not drawn again. The cache prunes itself (45 days, 3 GB).

Open the DWG in Rhino WITHOUT moving or scaling it (the georeference depends on its coordinates; the file units
may be metres or centimetres as long as the numbers were not scaled). Survey layers that were moved apart from the
buildings are put back in memory (reported in info). Line weights are print widths: run _PrintDisplay to see them.
Pictures (technical maps, section drawings) display rendered in every viewport, Wireframe included.
"""

# v16.7: the component's inputs, taken before anything else runs. Rhino 8 KEEPS the globals of the previous run, so a
# name this script defines (the function bake, a module) would otherwise stand in for an input that is not connected.
# Only the component's real input names are taken, and never a module, function or class.
import types as _types


def _gh_inputs():
    names = None
    try:
        names = set()
        for p_ in ghenv.Component.Params.Input:                      # noqa: F821 (ghenv exists in Grasshopper)
            for a_ in ("VariableName", "NickName", "Name"):
                v_ = getattr(p_, a_, None)
                if v_:
                    names.add(str(v_))
        if not names:
            names = None
    except Exception:
        names = None
    out = {}
    for k_, v_ in list(globals().items()):
        if k_.startswith("_") or (names is not None and k_ not in names):
            continue
        if isinstance(v_, (_types.ModuleType, _types.FunctionType, _types.BuiltinFunctionType, type)):
            continue
        out[k_] = v_
    return out


_GH_IN = _gh_inputs()
_T_START = __import__("time").time()


#@include ../../common/chain_fire.py


def done_text(ran, ok, secs):
    """The done output: kept until the next run (this Rhino session)."""
    return ("done " if ok else "ERROR ") + __import__('time').strftime("%H:%M:%S") + ".%02d" % int((__import__('time').time() % 1) * 100) + \
        " · %.0f s" % secs if ran else None


import os                                            # v35: used by the Downloads/Bergama paths before any later import
import math
import json
import random
import textwrap
import threading as _threading
import traceback
import xml.etree.ElementTree as ET
from zlib import crc32 as _zlib_crc

try:
    import System
    import Rhino
    import Rhino.Geometry as rg
    import scriptcontext as sc
    import System.Drawing as sd
    from System.Collections.Generic import List
    HAVE_RHINO = True
except Exception:
    HAVE_RHINO = False


# ============================================================ INPUTS
LOG = []
SCRIPT_VERSION = "selinus_board v47 (2026-10-27)"     # v27: the log's first line and the text under the component
SHORT_V = "v47"                                         # v44.1: the version under the component (was a fixed "v40")
DRAWING_TIMES = []                                  # v27: (drawing name, seconds) in the order they were made


_LIST_IN = ("section_lines", "sound_sections", "heat_sections", "shade_sections", "solar_sections", "wind_sections",
            "air_sections", "felt_sections", "noise_points", "noise_db",
            "spine", "spine_car", "bridges", "car_closed", "attractors")          # v33: the movement proposal


def _gh_flat(v):
    """v16.7: a Grasshopper data tree or nested list as one flat list."""
    if hasattr(v, "AllData") and callable(getattr(v, "AllData")):
        try:
            return [x for x in v.AllData()]
        except Exception:
            pass
    if hasattr(v, "Branches") and hasattr(v, "Paths"):
        try:
            return [x for br in v.Branches for x in br]
        except Exception:
            pass
    if isinstance(v, (list, tuple)):
        out = []
        for x in v:
            out += _gh_flat(x) if isinstance(x, (list, tuple)) else [x]
        return out
    try:
        if HAVE_RHINO and not isinstance(v, str) and hasattr(v, "__iter__") and hasattr(v, "Count") and \
                not hasattr(v, "PointAtStart") and not hasattr(v, "X"):
            return [x for x in v]                             # a .NET list
    except Exception:
        pass
    return v


def _gh_doc_geometry(gid):
    """The geometry of an object id: the Rhino file, then Grasshopper's own document (what an input with the default
    "ghdoc Object" type hint hands over), then rhinoscriptsyntax in both. None when no document has it."""
    docs = []
    try:
        docs.append(Rhino.RhinoDoc.ActiveDoc)
    except Exception:
        pass
    gd = globals().get("ghdoc")
    if gd is not None:
        docs.append(gd)
    for d_ in docs:
        try:
            o = d_.Objects.FindId(gid)
            if o is not None and getattr(o, "Geometry", None) is not None:
                return o.Geometry
        except Exception:
            pass
    try:
        import rhinoscriptsyntax as rs
        keep = sc.doc
        for d_ in reversed(docs):
            try:
                sc.doc = d_
                g = rs.coercegeometry(gid, False)
                if g is not None:
                    return g
            except Exception:
                pass
            finally:
                sc.doc = keep
    except Exception:
        pass
    return None


def gh_value(x):
    """v16.7: any one value an input can deliver, whatever its type hint (Nil leaves them at the default):
    Grasshopper wrappers (goo) are unwrapped, an object id (System.Guid, or its text) becomes the geometry it names,
    a Rhino object its geometry, a Point object its location, a Polyline a curve. Numbers, text and switches pass
    through and are read later by to_float / to_bool / str."""
    g = x
    for _ in range(3):
        if g is None or isinstance(g, (str, bool, int, float)):
            break
        if hasattr(g, "Value") and not any(hasattr(g, a_) for a_ in ("TryGetPolyline", "PointAtStart", "From", "X",
                                                                      "Geometry")):
            try:
                g = g.Value
                continue
            except Exception:
                break
        break
    if not HAVE_RHINO or g is None:
        return g
    gid = None
    try:
        if isinstance(g, System.Guid):
            gid = g
        elif isinstance(g, str) and len(g.strip()) in (36, 38) and g.count("-") == 4:
            gid = System.Guid(g.strip().strip("{}"))
    except Exception:
        gid = None
    if gid is not None:
        geo = _gh_doc_geometry(gid)
        if geo is None:
            LOG.append("WARNING: an input holds the object id {} but neither the Rhino file nor Grasshopper has that "
                       "object (re-pick it).".format(gid))
            return None
        g = geo
    try:
        if isinstance(g, Rhino.DocObjects.RhinoObject):
            g = g.Geometry
        if isinstance(g, rg.Point):
            return g.Location
        if isinstance(g, rg.Polyline):
            return rg.PolylineCurve(g)
    except Exception:
        pass
    return g


_STALE_IN = set()


def doc_layer_curves(word, closed=None):
    """v17: curves on the open Rhino file's layers whose name contains word (any case), for an input whose picked
    object is missing (a .gh opened beside another copy of the file): the survey keeps the frame on "site alan" and
    the section lines on "sec_lines"."""
    out = []
    try:
        doc_ = Rhino.RhinoDoc.ActiveDoc
        for o in doc_.Objects:
            try:
                lay = doc_.Layers[o.Attributes.LayerIndex]
                if word.lower().replace("_", " ") not in (lay.FullPath or lay.Name or "").lower().replace("_", " "):
                    continue
                g = o.Geometry
                if hasattr(g, "TryGetPolyline") and (closed is None or bool(g.IsClosed) == closed):
                    out.append(g)
            except Exception:
                pass
    except Exception:
        pass
    return out


def input_wired(name):
    """v20: whether the component's input of that name gets anything (a wire or picked objects), so an empty value
    means the picks were not found in this file."""
    try:
        for p_ in ghenv.Component.Params.Input:                      # noqa: F821 (ghenv exists in Grasshopper)
            if name in (str(getattr(p_, "NickName", "")), str(getattr(p_, "Name", ""))):
                return p_.SourceCount > 0 or bool(getattr(p_, "PersistentDataCount", 0))
    except Exception:
        pass
    return False


def picks_missing(name, value):
    """v20: a wired input that came out empty or held objects this file does not have."""
    return name in _STALE_IN or (not value and input_wired(name))


def inp(name, default):
    """An input by name, whatever its type hint and access: a single-value input that arrives as a list (List Access,
    or several items) gives its first item. v16.7: whatever the type hint (gh_value), from the component's own inputs
    only (_GH_IN), lists and data trees flattened."""
    v = _GH_IN.get(name)
    if v is not None:
        flat = _gh_flat(v)
        raw_ = flat if isinstance(flat, list) else [flat]
        v = [gh_value(x) for x in flat] if isinstance(flat, list) else gh_value(flat)
        got_ = v if isinstance(v, list) else [v]
        if any(r_ is not None and g_ is None for r_, g_ in zip(raw_, got_)):
            _STALE_IN.add(name)                          # v17: a picked object this Rhino file does not have
    if name not in _LIST_IN and isinstance(v, (list, tuple)):
        v = next((x for x in v if x is not None and not (isinstance(x, str) and not x.strip())), None)
    if v is None:
        return default
    if isinstance(v, str) and not v.strip():
        return default
    return v


def to_float(v, default=None, name=None):
    """A number from a GH input: numbers, "2,5" (decimal comma), "15:00" (the leading number); default otherwise
    (with a warning naming the input when it held something that is not a number)."""
    if v is None:
        return default
    if isinstance(v, bool):
        return float(v)
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if not s:
        return default
    t = s.replace(",", ".")
    try:
        return float(t)
    except ValueError:
        pass
    num_ = ""
    for ch in t:
        if ch.isdigit() or (ch in "+-." and (not num_ or ch == ".")):
            num_ += ch
        elif num_:
            break
    try:
        return float(num_)
    except ValueError:
        if name:
            LOG.append("WARNING: input {} = '{}' is not a number; {} used.".format(name, s, default))
        return default


def to_bool(v, default=False):
    """A switch from a GH input: True/False, numbers, or text such as "false", "0", "no", "yes"."""
    if v is None:
        return default
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v != 0
    s = str(v).strip().lower()
    if s in ("true", "yes", "y", "on", "1", "evet", "1.0"):
        return True
    if s in ("false", "no", "n", "off", "0", "0.0", "hayir", "hayır", "none", ""):
        return False
    return default


def clean_path(v, name):
    """A file path from a Panel or a File Path input: spaces and quotes removed; None (with a warning) when the file
    does not exist, so a wrong path never stops the build."""
    import os
    if v is None:
        return None
    s = str(v).strip().strip('"').strip("'").strip()
    if not s:
        return None
    s = os.path.expandvars(os.path.expanduser(s))
    if not os.path.isfile(s):
        LOG.append("WARNING: {}: no file at {} - check the path (it was ignored).".format(name, s))
        return None
    return s


DATA_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "Data")   # 25 Oct: every data file here


def data_file(name):
    """Downloads/Bergama/Data/<name> when it is there (used when the path input is empty), else None."""
    p = os.path.join(DATA_DIR, name)
    return p if os.path.isfile(p) else None


OSM_PATH = clean_path(inp("osm_path", None), "osm_path") or data_file("bergama_osm.osm")
PLACES_PATH = clean_path(inp("places_path", None), "places_path") or data_file("bergama_places.geojson")
SEC_IN = inp("section_lines", [])
try:
    SEC_IN = [c for c in SEC_IN if c is not None]
except TypeError:
    SEC_IN = [SEC_IN]
TSEC_KEYS = ["sound_sections", "heat_sections", "shade_sections", "solar_sections", "wind_sections", "air_sections",
             "felt_sections"]
TSEC_IN = {}
for _k in TSEC_KEYS:
    _v = inp(_k, [])
    try:
        TSEC_IN[_k] = [c for c in _v if c is not None]
    except TypeError:
        TSEC_IN[_k] = [_v]
TSEC = dict((k, []) for k in TSEC_KEYS)      # the same lines in survey coordinates (set by pipeline)
KNOWN_INPUTS = set(['spine', 'spine_car', 'bridges', 'car_closed', 'attractors', 'rhino_bake', 'mode', 'channel_depth', 'credit', 'env_path', 'environment', 'focus', 'frame', 'hour', 'hours', 'layout', 'noise_db', 'noise_palette', 'noise_points', 'osm_path', 'pdf', 'places_path', 'section_lines', 'sheet_mm', 'subtitle', 'texture', 'title', 'water_depth', 'water_levels'])          # v30: this script's named inputs (anything else may be the Button)
def _button_value():
    """The Button, on whatever input name or case it is wired (Aras's rule): "bake" first, then build / button /
    press / go in any case, then any other input that is not one of this script's named options and holds True or
    False."""
    known = KNOWN_INPUTS
    low = dict((k_.lower(), k_) for k_ in _GH_IN)
    for nm in ("run", "bake", "build", "button", "press", "go"):   # v37: run first
        if nm in low:
            return _GH_IN[low[nm]]
    for k_, v_ in _GH_IN.items():
        if k_.lower() not in known and isinstance(v_, bool):
            return v_
    return False


DO_BAKE = to_bool(_button_value())                     # v30: the Button on any input name
FRAME_IN = inp("frame", None)
FRAME_FROM_LAYER = [False]                            # v36: the frame came from layer site_alan (set per press)
TITLE = str(inp("title", "THE SELINUS SEAM"))
SUBTITLE = str(inp("subtitle", "Land use and the grain of Bergama along the Selinus: what stands, what opens, "
                               "and where the water meets the town"))
CREDIT = str(inp("credit", u"Group 6 · Aras Özkaymakcı · Begüm Arslan · Nil Çetin"))   # 25 Oct: spelt as on the other sheets
CH_DEPTH = to_float(inp("channel_depth", None), None, "channel_depth")   # None = from the surveyed bed levels
if CH_DEPTH is not None and not (0.0 < CH_DEPTH < 30.0):
    LOG.append("WARNING: channel_depth {} m is outside 0-30 m and was ignored.".format(CH_DEPTH))
    CH_DEPTH = None
_wd = to_float(inp("water_depth", None), None, "water_depth")
if _wd is not None:
    if 0.0 <= _wd < 10.0:
        WATER_DEPTH, WATER_SRC = _wd, "input"
    else:
        LOG.append("WARNING: water_depth {} m is outside 0-10 m and was ignored.".format(_wd))
WATER_LEVELS_IN = inp("water_levels", None)
SHEET_MM = to_float(inp("sheet_mm", 406.4), 406.4, "sheet_mm")
if not (50.0 <= SHEET_MM <= 5000.0):
    LOG.append("WARNING: sheet_mm {} is outside 50-5000 mm; 406.4 used.".format(SHEET_MM))
    SHEET_MM = 406.4
TEXTURE = to_bool(inp("texture", True), True)
PDF_EXPORT = to_bool(inp("pdf", True), True)            # v28: one vector PDF per drawing, 1:10,000
PDF_SCALE = 10000.0                                   # v28: 1 model metre = 1000 / PDF_SCALE mm on the page
BAKE_RHINO = to_bool(inp("rhino_bake", False), False)  # v31: a Boolean Toggle on rhino_bake; off (default) = PDFs only
PDF_LINE_SCALE = 1.0                                  # v28: multiplies every print line weight in the PDFs

FONT_TITLE = "Josefin Sans"
FONT_BODY = "Courier New"
# v16.5: the water in the stream. The survey has no water level, and no published depth or flow figure for the Selinus
# in Bergama was found. What is published: the Kestel dam (opened 1988) holds the stream's water upstream and much of
# it is led through a channel and tunnel into the neighbouring catchment (DAI TransPergMikro field notes, 2024);
# "Kestel Baraji'nin suyu tutmasi nedeniyle, Selinos Deresi'nin debisinin cok azalmis" and "icinden artik su akmayan"
# (Acik Radyo, Selinos restoration programme); household waste water ran into it until IZSU's 2024 sewer works
# (Gercek Izmir, 28 Feb 2024). So the water is drawn as a thin APPROXIMATE layer over the surveyed bed, labelled so;
# a measured depth (water_depth) or measured levels (water_levels: points on the water surface) replace it.
WATER_DEPTH_APPROX = 0.15                            # m above the bed: APPROXIMATE (low flow / standing water), not measured
WATER_DEPTH = WATER_DEPTH_APPROX                     # replaced by the water_depth input below
WATER_SRC = "approx"                                 # "approx", "input" or (per point) "measured"
WATER_PTS_USER = []                                  # water_levels input: (x, y, z of the water surface), user coordinates
MMU = 0.3


# ============================================================ PALETTE (slide colours)
def C(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def mix(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


BG = C("E6E0C8")        # 60 %  slide beige
KHAKI = C("BCB794")     # 30 %  slide khaki
PAPER = C("F1EDDF")     # void
ROADC = C("FAF8F1")     # streets: the lightest void
INK = C("4A3F35")
INK2 = C("7A6E60")
FAINT = C("DCD5C2")
BLUE_D = C("5E8494")
BLUE_L = C("B4CBD2")

CAT_ORDER = ["residential", "mixed", "commercial", "institutional", "religious",
             "industrial", "transport", "green", "agri", "vacant", "water"]
CAT = {
    "residential":   ("Residential fabric", C("D6C08F")),
    "mixed":         ("Mixed use · shop below, home above", C("CC9A52")),
    "commercial":    ("Commerce · the market floor", C("BC6F45")),
    "institutional": ("Civic & institutional", C("8C7088")),
    "religious":     ("Sacred & heritage", C("8A4650")),
    "industrial":    ("Workshops & industry", C("6F6A62")),
    "transport":     ("Movement & infrastructure", C("B9B2A1")),
    "green":         ("Green & open ground", C("8F9A68")),
    "agri":          ("Agricultural ground · fields and orchards", C("BDB57A")),
    "vacant":        ("Vacant · in transition", C("D9D2BE")),
    "water":         ("Water · the Selinus", C("7FA4B3")),
    "void":          ("Unbuilt ground", PAPER),
}
GREEN_SUB = {"wood": C("74804F"), "park": C("8F9A68"), "grass": C("ABB287")}
TREE_COLS = {"pine": C("5F6B43"), "olive": C("8E9A6C"), "tree": C("7E8A57"), "orchard": C("98A271")}
TREE_SHADOW = C("57603D")
INTENSITY = [C("E8DDBF"), C("D6C08F"), C("BC6F45"), C("7A3E3A")]

EDGE_ORDER = ["building", "street", "pedestrian", "green", "parking", "open"]
EDGE = {
    "building":   ("Built edge · backs to the water", INK, "built edges that turn their backs"),
    "street":     ("Street edge · seen, not touched", C("A39883"), "street edges, seen but not touched"),
    "pedestrian": ("Walkable edge · within reach", C("BC6F45"), "walkable edges within reach"),
    "green":      ("Planted edge · porous", C("74804F"), "planted, porous edges"),
    "parking":    ("Parking edge · waiting to change", C("CC9A52"), "parking edges waiting to change"),
    "open":       ("Loose edge · open to change", C("D6C08F"), "loose, undefined edges"),
}
EDGE_W = 1.5           # print weight (mm) of the stream-threshold edges on the thresholds map and in its legend (v16.3; was 0.7)
EDGE_MARK_W = 0.6       # the white wall / embankment dashes laid over them (was 0.28)
STOREY = {"religious": 5.0, "institutional": 3.5, "industrial": 4.5}
FLOOR_H = 3.0

# ============================================================ SURVEY (DWG) LAYERS - edit if your layer names differ
DWG = dict(
    bld={"BINA_MESKEN": "mesken", "BINA": "mesken", "BINA_RESMI": "resmi", "BINA_OKUL": "okul",
         "BINA_DINI_TESIS": "dini", "BINA_DINITESIS": "dini", "BINA_TARIHI": "tarihi",
         "BINA_HARABE": "harabe", "BINA_FABRIKA": "fabrika", "BINA_SERA": "sera",
         "BINA_SPOR_TESISLERI": "spor", "BINA_AKARYAKIT": "akaryakit", "BINA_INS_HALINDE": "insaat"},
    shed="BINA_SUNDURMA", door="BINA_KAPI", stairs="BINA_MERDIVEN",
    floors="YAZI_KAT_ADEDI", names="YAZI_YAPI", stream_names="YAZI_CAY_DERE",
    walls=["SINIR_DUVAR", "SINIR_HARAP_DUVAR", "SINIR_TARIHI_SUR"],
    fences=["SINIR_TEL", "SINIR_PARMAKLIK", "SINIR_CIT"],
    slopes=["SEV_SEV", "SEV_UST", "SEV_ALT", "SEV_SEVUST", "SEV_SEVALT"], slope_hatch="SEV_TARAMA",
    roads=["YOL_SOSE", "YOL_TOPRAK", "YOL_BORDUR"], bridges=["YOL_KOPRU"],
    banks=["HIDRO_DERE_SULU", "HIDRO_DERE_KURU"], water_misc=["HIDRO_HAVUZ", "HIDRO_GOL"],
    park="ORMAN_PARK_BAHCE",
    trees={"SEMBOL_YAP_DOKMEYEN": "pine", "SEMBOL_TEK_AGAC": "tree", "SEMBOL_YPDKN_AGAC": "tree",
           "SEMBOL_ZEYTINLIK": "olive", "SEMBOL_MEYVA_BAH": "orchard"},
    minarets="SEMBOL_MINARE",
    survey="NOKTA_TAKEOMETRI", contours=["EGRI_1M", "EGRI_2M", "EGRI_5M", "EGRI_10M", "EGRI_ARA"],
    spot_texts=["YAZI_POL_NOK_NUM_KOT"],
    zlines=["SEV_UST", "SEV_ALT", "HIDRO_DERE_SULU"],     # v33: bank tops, bank toes and stream lines carry heights
)
# v19: the group's study areas (closed curves, read only). v33: never drawn (Aras, batch 22 Oct): they only locate
# C5 and the photo areas; the drawings cover the site frame.
STUDY_LAYERS = ["aras_alan", "begum_alan", "nil_alan"]
STUDY_RAW = {}                                       # what read_rhino found on STUDY_LAYERS (set by the main block)
# v20: the frame and section lines selinos.gh picked in Nilnoktali-BERGAMA_layerekli.3dm (md5
# c7dcc5d18f8ea2092805edb84d0ecce7; layers 'site alan' and 'sec_lines'), in survey coordinates and in the .gh's
# order. Used only when a wired frame / section input finds nothing in the open file (the course file has neither).
SITE_FRAME_LK = [(29388.015, 32540.503), (31220.325, 30364.153), (31625.069, 30704.915), (29792.759, 32881.264)]   # v36: site_alan of Bergama_Altlik.3dm, made a rectangle 25 Oct (was the layerekli parallelogram)
SECTION_LINES_LK = [
    ((29545.7389380673, 32125.561640649055), (30167.094607046227, 32687.136735061496)),
    ((29806.59962708469, 31571.232676487103), (30610.920084888312, 32286.78803872231)),
    ((30366.36318893451, 31067.62662407853), (31210.537363115785, 31688.982293057452)),
    ((30616.354682576173, 30540.470648355884), (31489.513377759384, 31161.82631733481)),
    ((29455.902311876587, 32763.450197393668), (30154.568393700003, 32040.938166000004)),
    ((31571.80121771565, 30442.532979115742), (30689.178829950186, 31396.58325230568)),
]
_SITE_FALLBACK = {}                            # which inputs use them this run (set by the main block)
KIND_CAT = {"mesken": "residential", "resmi": "institutional", "okul": "institutional", "dini": "religious",
            "tarihi": "religious", "harabe": "religious", "fabrika": "industrial", "sera": "industrial",
            "spor": "institutional", "akaryakit": "transport", "insaat": "vacant"}
NAME_RULES = [("cami", "religious"), ("mescid", "religious"), ("türbe", "religious"), ("turbe", "religious"),
              ("hamam", "religious"), ("tarihi", "religious"), ("harabe", "religious"), ("müze", "institutional"),
              ("okul", "institutional"), ("lise", "institutional"), ("ilköğretim", "institutional"),
              ("kuran", "institutional"), ("belediye", "institutional"), ("müdürlü", "institutional"),
              ("hastane", "institutional"), ("dispanser", "institutional"), ("ptt", "institutional"),
              ("jandarma", "institutional"), ("salonu", "institutional"), ("lojman", "residential"),
              ("su dep", "transport"), ("sanayi", "industrial"), ("fabrika", "industrial"), ("depo", "industrial"),
              ("ambar", "industrial"), ("kereste", "industrial"), ("trafo", "transport"), ("garaj", "transport"),
              ("banka", "commercial"), ("büfe", "commercial"), ("otel", "commercial")]

# ============================================================ GEOREFERENCE (fitted on 417 matched buildings, rms 1.27 m)
# lon/lat -> TM27 (GRS80, CM 27E, k0 1, FE 500000) -> similarity -> survey drawing coordinates
GEO = dict(s=1.0001121171177874, th=-0.0015904735313230483, tx=-492593.7399912414, ty=-4299748.4497664515)
# Unique street / building / place labels of the original survey with their insertion points.
# The script finds them in your file and solves how the drawing was rotated, moved or scaled.
ALIGN_LAYERS = ["YAZI_CADDE_YOL", "YAZI_YAPI", "YAZI_YORE", "YAZI_UNSUR", "YAZI_CAY_DERE"]
#@include ../data/REF_LABELS.py

_A = 6378137.0
_F = 1 / 298.257222101
_E2 = _F * (2 - _F)
_EP2 = _E2 / (1 - _E2)


def tm27(lon, lat):
    phi = math.radians(lat)
    lam = math.radians(lon - 27.0)
    s, c, t = math.sin(phi), math.cos(phi), math.tan(phi)
    N = _A / math.sqrt(1 - _E2 * s * s)
    T, Cc, Aa = t * t, _EP2 * c * c, c * lam
    e4, e6 = _E2 * _E2, _E2 ** 3
    M = _A * ((1 - _E2 / 4 - 3 * e4 / 64 - 5 * e6 / 256) * phi
              - (3 * _E2 / 8 + 3 * e4 / 32 + 45 * e6 / 1024) * math.sin(2 * phi)
              + (15 * e4 / 256 + 45 * e6 / 1024) * math.sin(4 * phi) - (35 * e6 / 3072) * math.sin(6 * phi))
    x = N * (Aa + (1 - T + Cc) * Aa ** 3 / 6 + (5 - 18 * T + T * T + 72 * Cc - 58 * _EP2) * Aa ** 5 / 120)
    y = M + N * t * (Aa * Aa / 2 + (5 - T + 9 * Cc + 4 * Cc * Cc) * Aa ** 4 / 24
                     + (61 - 58 * T + T * T + 600 * Cc - 330 * _EP2) * Aa ** 6 / 720)
    return x + 500000.0, y


def tr_upper(t):
    """v21: Turkish capitals: i -> İ before upper() (Python turns i into I; ı already becomes I)."""
    return (t or "").replace("i", "İ").upper()


def to_dwg(lon, lat):
    E, N = tm27(lon, lat)
    c, s = math.cos(GEO["th"]), math.sin(GEO["th"])
    return (GEO["s"] * (c * E - s * N) + GEO["tx"], GEO["s"] * (s * E + c * N) + GEO["ty"])


# ============================================================ GEOMETRY HELPERS (pure python)
def shoelace(P):
    n = len(P)
    if n < 3:
        return 0.0, (P[0][0] if P else 0.0), (P[0][1] if P else 0.0)
    a = cx = cy = 0.0
    for i in range(n):
        x0, y0 = P[i]
        x1, y1 = P[(i + 1) % n]
        cr = x0 * y1 - x1 * y0
        a += cr
        cx += (x0 + x1) * cr
        cy += (y0 + y1) * cr
    if abs(a) < 1e-9:
        return 0.0, sum(p[0] for p in P) / n, sum(p[1] for p in P) / n
    return abs(a) / 2.0, cx / (3.0 * a), cy / (3.0 * a)


def signed_area(P):
    """Area with its sign: positive for a counter-clockwise ring (shoelace() returns the absolute area)."""
    n = len(P)
    return 0.5 * sum(P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1] for i in range(n)) if n >= 3 else 0.0


def ccw(P):
    """The ring counter-clockwise."""
    return list(P) if signed_area(P) >= 0.0 else list(reversed(P))


def interior_point(P):
    """A point strictly inside a simple ring of any shape (concave too): the middle of the widest inside span of a
    horizontal line through the ring, tried at several heights."""
    ys = [p[1] for p in P]
    y0, y1 = min(ys), max(ys)
    n = len(P)
    best = None
    for f in (0.5, 0.31, 0.69, 0.17, 0.83, 0.43, 0.57, 0.08, 0.92):
        yc = y0 + (y1 - y0) * f
        xs = []
        for i in range(n):
            (xa, ya), (xb, yb) = P[i], P[(i + 1) % n]
            if (ya <= yc) != (yb <= yc):
                xs.append(xa + (yc - ya) * (xb - xa) / (yb - ya))
        xs.sort()
        for k in range(0, len(xs) - 1, 2):
            w = xs[k + 1] - xs[k]
            if w > 1e-6 and (best is None or w > best[0]):
                best = (w, (xs[k] + xs[k + 1]) / 2.0, yc)
        if best is not None and best[0] > 0.05 * (max(p[0] for p in P) - min(p[0] for p in P) + 1e-9):
            break
    if best is None:
        return shoelace(P)[1], shoelace(P)[2]
    return best[1], best[2]


# ---- v17: the sound model's receiver code, ONE source for Rhino and for the worker processes that share its work
# (pip, convex_hull, screen_db, round_paths, lateral_db, the terrain read and NoiseModel's receiver methods are defined
# here, unchanged from v16.7). The worker processes run exactly this text, so every number they return is computed by
# the same code; see noise_par.
#@include ../data/NOISE_KERNEL.py
