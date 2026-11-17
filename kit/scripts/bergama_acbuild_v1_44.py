# -*- coding: utf-8 -*-
"""Bergama Group 6: ACBUILD v1 (14 Nov 2026): the node sections' 3D context built in Archicad through Tapir.

What Aras asked (14 Nov 2026, 15:41-15:43 UTC): "maybe redrawing them in archicad via tapir and taking elevations etc
there would make much more sense"; "i want the background to be taken from archicad cuz your sections etc. look really
really undetailed and add our sauce on it like ground hatches etc. lets try both"; "our scripts should be connected
nontheless like tapir should take the latest info from grasshopper".

What it does (run in Rhino 8, in Bergama_Altlik.3dm, with Archicad open on a project and the Tapir add-on loaded):
  1. reads the LATEST caches, nothing re-derived: Sections (cached/bergama_sections/sections.json: every cut's line
     A -> B), MapBase (cached/bergama_mapbase/mapbase.json: buildings, fabric, floors as bld_x), and the survey heights
     of the open Rhino model through the Sections script's own read_survey / Tin (loaded as a library);
  2. sends to Archicad over its JSON port (no pip installs): per cut a rectangle A -> B x BACK_M behind it (the side
     the section looks at, as the Sections script draws its houses behind) and every building in it:
       terrain   one Mesh per cut from the survey contours and spot heights        layer "BG terrain"
       walls     one wall per footprint edge, floors x storey height + plinth      layer "BG buildings"
       windows   a row per floor on walls that face a cut (WIN_* = the Sections drawing rule, not surveyed)
       roofs     hipped 30 deg below FLAT_FLOORS floors, else a flat slab + parapet  layer "BG buildings"
       slabs     a floor slab per storey in the buildings a cut line crosses         layer "BG buildings"
       markers   two registration blocks per cut at A (0.4 m) and B (0.8 m)        layer "BG reg"
       sections  N1-A ... N6-B (kept between runs), depth BACK_M, vector shadows, shaded materials, distant area
       views     View Map folder "Bergama sections" with one view per section
  3. publishes the publisher set PUB_SET (made once by hand, see FLAG text) to cached/bergama_archicad/dwg/ as DWG,
     read next by the SectionsAC page script.
Each run deletes the elements of the previous run first (their ids are in cached/bergama_archicad/acbuild.json); the
sections and views are kept so the publisher set stays valid.

Storey heights (typical values, not measured; the project's rule): 3.0 m; civic 3.5; sacred and heritage 5.0;
industry 4.5. A building without a recorded floor count is left out (as the Sections script does), logged.
Proposed buildings and canopies: v2, from the MasterplanBase cache once the slide 2 thread writes it.

Reads  ~/Downloads/Bergama/cached/bergama_sections/sections.json, cached/bergama_mapbase/mapbase.json,
       scripts/bergama_sections_v*.py (newest, as a library), the open Rhino model's survey layers
Writes ~/Downloads/Bergama/cached/bergama_archicad/acbuild.json (+ dwg/ via the publisher set),
       logs/bergama_acbuild_log.txt
Works when: the log's first line is "TAPIR OK <version>" and Archicad's Navigator shows the 12 sections.
"""
import os, re, json, math, time, glob

VERSION = "v1.44"   # v1.44 (Aras 16 Nov 11:37-11:40 "columns should be travelling two floors they should be linked by the upper floor", "single beam travelling all across the grid"): house walls and frame columns one per storey (floor slab top to the next slab / roof), beams one per span between columns; windows, doors and balconies on their own storey's wall; (Aras 16 Nov 11:37 "proper ways of drawing ... to give the calculations right in the end and make it more properly displayed"): every Bergama building material gets an Archicad connection priority (MAT_PRIO: structure over masonry over screed over insulation over finishes; ground and water lowest), so junctions of walls, slabs, columns, beams and the ground clean up by material; (Aras 16 Nov 11:36 "why not meshes for bodies like water and such ?"): the river water is one Mesh body per river outline (was 5 m slab cells stepping down the river): its top = the season water level down the river, points every WATER_CELL_M, its body down to under the bed; the river bed body cuts it, so water stands only above the bed; (Aras 16 Nov 11:35 "you do have the real floor count information of somekind"): the survey's own floor-count labels (YAZI_KAT_ADEDI, 11,261 texts) give each footprint they stand in its floor count (was: the MapBase count, 7,131 houses without one); (Aras 11:25 "the stairs should follow the real survey data where possible") the survey building stairs (BINA_MERDIVEN, 17,392 step-edge lines with their heights) are grouped into flights and built tread by tread (Slab tool, top = the surveyed step height, down to the ground, cutting it); (Aras 16 Nov 11:33 "nothing should sink into ground if something is in ground it MUST use solid element operations"): every element that reaches below the surveyed ground cuts it: house walls whose foot is under the ground (uphill sides), survey kerbs and walls (dropped in v1.32 for speed; the tile index makes them cheap now), boulders and reed beds (ground and river bed), tree trunks; the log counts every kind; (Aras 16 Nov 11:32 "also roads should be the same way so does the pavement around it"): road and park cells are Mesh-tool bodies whose top is the surveyed ground (points every TOWN_PT_M, town blocks as holes), 0.30 m under its lowest point, and they cut the ground (SEO; was a slab shaped by the terrain); pavements from the survey kerb lines: a Slab-tool strip from each kerb piece to the nearest building face on its side (at most PAV_MAX_M, ASSUMED), top = kerb top, PAV_T_M build-up (ASSUMED); it cuts the ground and the road under it; (Aras 16 Nov 11:31 "3D should look like a real life site"): the materials outside his legend take the textured Archicad surfaces of the project (REAL_SURF: stucco, brick, concrete, clay roof tiles, asphalt, grass, earth, gravel, foliage, bark, water); his legend materials keep his colours; tree crowns foliage, trunks bark, water cells water; (Aras 16 Nov 11:31 "river sohuld be a proper river bed drawing with solid element operations rather than setting a slab and calling it a day"): a river bed body per river outline (Mesh tool, gravel): its top = the channel: the thalweg of each river section line (Sections cache z_th, linear between them down the river) at the centreline (Data/selinos_centreline.json), rising to the surveyed ground at his outline (parabolic cross-section ASSUMED), never above the surveyed ground; it cuts every ground tile upwards (SEO), so the ground opens into a real channel; plinths and terraces cut it, it cuts the water; the water cells reach down to the bed; (Aras 16 Nov 11:21 "sections dont cut trough the meshes"; found 11:31: v1.41 gave every Bergama material the cut fill "Solid + Dot & Dashed" in pen 1 (the first fill named "solid"), so cuts drew a pattern, not a hatch): each material gets the Archicad fill of what it is (ground Earth, concrete Structural Concrete, brick Common Brick, stone Rubble / Cut Stone, insulation Rigid Insulation, timber Wood ...), others the solid Foreground fill; (Aras 11:30 "give me a override that show those walls as a single solid hatch") the graphic override rule "Bergama - walls as one solid poche" (walls: cut fill Foreground solid, pen 21, no skin separators) in the combination "Bergama - solid walls"; (Aras 16 Nov 11:30 UTC "try to use generic composites like slum houses should have a one slum house composite, planned low rise need a composite that is for itself ... do good educated guesses accordingly what is highly used in turkey"): Archicad composites per MapBase fabric (regular = planned low-rise RC frame + hollow brick + EPS, block = apartment RC frame + AAC + EPS, selfbuilt = gecekondu pumice block, traditional = rubble stone + lime plaster (masonry: no RC frame), large = public RC frame + AAC + EPS), RC floor, clay-tile pitched roof and gravel flat roof composites; rafts, columns and beams in reinforced concrete; every layer thickness ASSUMED (educated guess of common Turkish practice, no source); the survey trees (SEMBOL_TEK_AGAC single trees, SEMBOL_YPDKN_AGAC / SEMBOL_YAP_DOKMEYEN evergreens) built as trunk + crown (heights ASSUMED); Aras 16 Nov 11:18 UTC "those rafts should connect columns and that columns should be connected by beams and etc.", "so the structures would be realistic"): every framed survey house (not the sacred / monument / Kizil Avlu masonry) gets a reinforced-concrete frame: Column-tool columns standing on its raft at every footprint corner, where a FRAME_SP_M grid line meets the footprint and at the grid crossings inside, full house height; Beam-tool beams under every floor slab and the roof along every footprint edge and every grid line inside (sizes and grid ASSUMED); centred in the wall thickness (ASSUMED: the walls lie inside the footprint line); Aras 16 Nov 11:16 UTC "the houses should sit on the ground they need to use solid element operations for cleaner looks and their foundation should be simplified raft foundation", "so the structures would be realistic"): every survey house stands on a raft (mat) foundation: one Slab-tool slab on its footprint, top = ground floor (survey ground at the centroid), bottom RAFT_T_M (ASSUMED) under the lowest survey ground under the footprint, so no side floats; it cuts the ground upwards (SEO, no ground inside the house); the walls start on the raft (were 1 m into the ground), the raft is the ground-floor slab; Aras 16 Nov 11:12 UTC "i dont want any gaps in the topography": ground tiles with no survey point of their own are filled from the survey triangulation; Aras 16 Nov 11:05-11:08 UTC "is it foolproof ?", "i do switch a lot between pc's", "i dont want to run two apps at the same time", "i'll be doing hand edits it needs to be safe from them"): the record of what AcBuild made lives in the pln itself: every element it makes carries Element ID "BGA-<fingerprint>@<3D box in cm>", so any PC, copy or recovery file finds its elements without the local cache; only elements with a BGA- Element ID are ever deleted (elements Aras draws are never touched; v1.34-v1.43 deleted every unrecorded wall, slab, roof ...); an element whose 3D box moved more than EDIT_TOL_M since AcBuild made it is hand-edited: locked, never deleted or replaced, and nothing new of its kind is made on it (FLAG count); the first v1.44 pass stamps the elements this PC's cache records; the survey is read from Rhino once and cached (cached/bergama_survey/survey.json with the ground triangles), so without Rhino AcBuild runs as plain Python with only Archicad open (python bergama_acbuild_v1_44.py); a Rhino model not in metres or a survey extent over 50 km stops the run; v1.43 (Aras 16 Nov 10:57 UTC "every slab should be drawn with slab tool, every column with column tool every roof is with roof tool"): the node buildings' folded roof facets are single-plane Roof-tool roofs (were meshes; a mesh only where Archicad refuses the roof, FLAG); a house roof Archicad refuses as a hipped roof is tried again as a single-plane Roof-tool roof before the slab fallback; bridge piers (Ulucami, Uc Kemer, new bridges) are Wall-tool piers (were stacked slabs), still cutting the ground; v1.42 (coordinator for Aras 16 Nov 09:50 UTC "build the whole site through Tapir at real 1:1", new empty Archicad file): WHOLE_SITE: everything inside the survey contour extent is built (was: the cut rectangles only): the ground as one gap-free surface of SITE_TILE_M tiles (shared edge points, control point every 10 m where no survey height) wherever the survey has heights, every survey building, the whole town ground, kerbs and walls; windows stay on the walls a section sees; ground tiles made in batches; solid element operations found through a tile index; its own cache folder (bergama_archicad_site, origin taken from bergama_archicad) and log; the project is neither saved nor published (Aras saves); v1.41 (Aras 15 Nov 23:50 section window: houses float, ground only a thin line): the ground is modelled again the full BACK_M behind each cut (GROUND_BEHIND_M = BACK_M) so the houses behind stand on their hillside; uncut surfaces filled in their own material colour, shaded (the hills read as a tone, not white blobs); the Bergama building materials get an explicit cut fill (solid fill, pen CUT_FILL_PEN, ASSUMED) as they were made with a cut surface only, so cut ground and cut walls drew no fill; v1.40 (runner 15 Nov 23:31: v1.38 said "model unchanged" and skipped its changes; its PDFs held almost nothing): the script version is part of the model fingerprint (a new version always goes through the element-by-element check, which keeps unchanged elements), and the distant area is off (everything in it is drawn with one fill and one pen); v1.39 (Aras 15 Nov 23:30 "why the outlines of the walls are not there for most"): uncut and distant elements draw with their own pens (the one uniform pen 81 / 102 is off), so every wall and roof edge keeps its own visible contour; v1.38 (Aras 15 Nov 23:13 "it is foreground/background issue ig. like get rid of those areas."): the ground is built only where a cut sees it cut (a strip from SIDE_M in front to GROUND_BEHIND_M behind each cut line) and under the river, in GROUND_TILE_M = 25 m tiles that still share their edge points; the hills behind a cut are no longer modelled, so nothing hides the buildings behind; his own section settings of 20:01 are back (uniform window-background fill, fade distant elements); v1.37 (Aras 15 Nov 23:10 "why these drawings look like this with white blobs over"): the ground behind a cut was filled with the window background (white) and, being a smooth mesh, had no outline, so the hills behind showed as white shapes hiding the houses; now uncut surfaces are filled with their own material colour, shaded, the distant-area option (always white in Archicad) is off, and the ground tiles carry the Sections ground colour; v1.36 (runner 15 Nov 23:05: partway through the v1.34 pass Archicad refused every new element, -2130312311 "Failed to create new ...", and every solid element operation): before each chunk the floor plan (story 0) is made the active window again, and a chunk Archicad refuses whole is tried once more after that; v1.35 (Aras 15 Nov 22:46 "get them as pdf", "dwg looks awful"): the Organizer / setup steps in the log say PDF; v1.34 (Aras 15 Nov 22:33 "archicad redraws take a lot of time can we have something faster ... not redrawing everything every single time"): every model element is kept by the hash of what it is made from; a pass makes only the elements whose data changed, deletes only the ones no longer wanted, makes solid element operations only for new elements and publishes only the sections whose line moved or that see a changed element; v1.33 (Aras 15 Nov 22:10 "move the node 6 to the building that is across the river": N6 now stands on an existing survey building): a survey building whose footprint lies more than COL_HALL_F inside a node building foot is left out (the node building takes its place); v1.32 (runner: the v1.31 publish stalled on its first section, Archicad 13 -> 21 GB in 10 min: one 2 km mesh with every survey point as the target of ~6000 solid element operations): the ground is the same one surface cut into GROUND_TILE_M tiles that share their edge points exactly (no gaps, one block to the eye), only tiles that touch a cut rectangle or the river; survey heights one per GROUND_SPOT_M m cell, control points every GROUND_GRID_M m where none; each solid element operation links an element only to the tile(s) it stands in; kerbs and survey walls no longer cut the ground (thousands of tiny operations)   # v1.31: v1.31 (Aras 15 Nov 21:19-21:20 "as you havent done solid element operations in archicad many of the drawings look weird. and ground has gaps in between", "it all should be one large block", "with many control points on it"): the ground is ONE terrain mesh over the whole survey box (every cut rectangle and the river; was 13 meshes per cut + 3 river meshes with gaps between them), its points every survey contour + spot height (one per 2 m cell) + a control point every GROUND_GRID_M m where the survey has none, a solid block GROUND_BASE_M m under its lowest point (was down to -5 m above sea level); solid element operations on that one ground for everything that stands in it: plinths, terraces, masterplan slabs, retaining walls (subtraction, as before), every building's ground slab (subtraction with upward extrusion: no ground inside a house), the Kızıl Avlu walls, bridge arches and piers, bank walls, kerbs and walls (subtraction), water (cut by the ground), road and park cells (shaped by the ground)   # v1.30: v1.30 (Aras 15 Nov 20:41 "what about roads ?", "and etc."): the existing town ground in the cut rectangles (where the terrain is): the MapBase street region (one region, the town blocks cut out as slab holes) and the parks as slabs in 20 m cells whose top the terrain shapes (SEO intersection), so they lie on the survey ground; survey kerbs, walls and ancient walls as Walls on the ground (heights ASSUMED); what the base map holds but is not built listed in the log   # v1.29: v1.29 (Aras 15 Nov 20:14-20:15 "build the selinos with everything in archicad like river bed, reed bed and everything like not a single beat skipped", "bridges and etc."): river bed mesh over his river outline (survey), water at each section line's own season level interpolated along the river (5 m cells, the ground cuts them by SEO), reed masses on his yosun rings (1.5 m ASSUMED), his stones and rocks of 1 m2 and more as boulders, his PLANTING_v13_1 trees as trunk Column + three crown slabs (heights ASSUMED), bank walls on his istinaat lines, his kopruler bridge outlines (picture-clip shapes too) as decks, the Ulucami and Üç Kemer bridges on their survey footprints with arches and piers (arch count / pier sizes ASSUMED, logged), piers under new bridges longer than 25 m; a layer audit of master.svg in the log; bridges / reeds / boulders no longer cut the terrain or get retaining walls; (runner, v1.18 rerun: 0 sections listed while 15 recorded, so all were remade and the Organizer step was undone) the floor plan is made the current window before the sections are listed, and 0 listed while some are recorded is treated as a listing failure (FLAG, recorded ones kept)   # v1.28: v1.28 (Aras 15 Nov 20:10 "also please solve these kinda collisions", his view: a hipped house inside the Kızıl Avlu walls): survey buildings overlapping the Kızıl Avlu hall by more than 10%% are left out (the hall stays), a footprint more than 50%% inside a bigger one is a duplicate and left out; counts logged; (Aras 20:10 "give both slabs and roofs to every building ... 3 storey ... 3 slabs") a floor slab per storey in every building (was: only the buildings a line cuts), flat roofs as 2 deg single-plane Roof-tool roofs   # v1.27 (Aras 15 Nov 20:07 "use solid element operations where necceseary"): every canopy plinth, node plinth and masterplan slab (terraces included) cuts the terrain mesh of each cut it stands in (Tapir CreateSolidElementLinks, subtraction); (Aras 20:08 "use retaining walls where neccesery") stone retaining walls along slab edges where the ground outside differs from the slab top by more than 0.60 m (ASSUMED)   # v1.26 (Aras 15 Nov 20:06 "dont do these kinda extereme angles keep it minimal like the second image"): fold rise 0.6 m (was 1.8 m), and no facet edge steeper than 8 deg (low corners on falling ground are raised to it, so every clearance still holds)   # v1.25 (Aras 15 Nov 20:05 "draw their roofs with roof tool columns with column tool, beams with beam tool etc. so intersections would look proper"): canopy facets = single-plane Roofs (pivot line through the low corner, slope of the facet plane), louvres = timber Beams (horizontal slats every 0.6 m under each facet); columns (Column tool), arms (Beam tool), plinths/decks/planters (Slab tool), glazed rooms (Wall + Window) as before; a facet Archicad refuses as a roof falls back to a mesh (FLAG)   # v1.24 (Aras 15 Nov 20:01 "use these settings for archicad sections"): his Section Selection Settings on every section (cut elements in their pens, uncut = uniform pen colour fill + line pen 81, fade distant elements on with line pen 102, no boundary contours); publishes once for the new settings   # v1.23 (Aras 15 Nov 20:00 "archicad is missing the ground in sections ... i want real 1:1 drawing in archicad"): the survey terrain mesh is built again, one per cut rectangle (10 m in front of the line to 200 m behind, survey contours + spot heights, solid with skirt), so every Archicad section has a cut ground and the hillside under its houses   # v1.22 (Aras 15 Nov 19:48 UTC "optimize the scripts to be much much faster", item 3 "run the Rhino-only slides alongside the Archicad steps"): run from the chain (__main__), the Rhino part (survey read, TIN) runs as before, then the Archicad part (pure Python + Tapir, no Rhino call) goes on in a background thread so Rhino is free for the next page script; the log reads "RUNNING ..." until it ends (same lines as before); a file cached/_chain/acbuild_foreground.txt keeps the old one-piece run; the Grasshopper button runs in one piece as before; v1.21 (v1.18 run 15 Nov 19:23 UTC: no bridge and no stepped terrace was built: his bridge outlines (kopruler path) and stepped-terrace outlines (begum su merdiven outline) are drawn without fill): those layers are built from their closed outlines (the outermost rings only, MasterplanBase v1.9 keeps the paint-less bridge rings); a bridge as a 0.50 m stone deck whose top is the highest survey ground under its outline (the banks it spans, not the river bed); BUILD_SIG geometry-9; v1.20   # v1.20 (Aras 15 Nov 19:18: the publisher set may be PDF): published PDFs count as the kept output   # v1.19 (Aras 15 Nov 19:09-19:11 UTC "1.2meter depth is fine however think it like 15x30 steps merge into single seating", "circulation wise"): his stepped terraces (begum su merdiven, the light stone picture) built as seating tiers stepping down to the river: each tier 1.20 m deep = four 30 cm treads merged, 0.48 m high = four 12 cm risers (Aras 19:13 "make the height of the steps is 12"; the 12 x 30 stair pitch kept), tiers cut from his own outline across the direction to the nearest point of his river outline (su_outline), lowest tier on the lowest survey ground of the piece, none above the highest; the stair aisles themselves are not placed (no aisle drawn in his masterplan); materials by each layer's own picture colour: teras = wood deck ("decks are wooden"), iskele kenari = grey paving CECFCE; v1.18 (Aras 15 Nov 18:12-18:17 UTC texture legend: "this stands for regular bridges", "historic buildings are in a shade of red", "our buildings are white blues are glasses", "these are decksn", "this is shading", "these are reed beds", "this is stepped terrace that goes into the river"): Archicad surfaces + building materials named "Bergama ..." in his legend colours (median colours sampled from his legend pictures), given to the elements as they are made: bridges (kopruler pieces) stone, stepped terraces (teras, begum su merdiven) light stone, decks (iskele kenari, canopy decks, planters, louvres) timber, reed beds (su bitkii) reed green, canopy facets white, Y columns grey frame, our buildings (node buildings, glazed rooms) white, historic buildings (sacred / monument houses, Kızıl Avlu) red; every glass surface of the project in his glass blue; an element Tapir refuses with a material is made again without it (FLAG); BUILD_SIG geometry-7 (one rebuild); v1.17 (Aras 15 Nov 17:24 UTC "any drawing that has building in it you should use the drawing that comes out of archicad"): the node building FLOOR PLANS from Archicad too: one Archicad story per floor of each node building (Tapir SetStories; story 0 kept, story level lines off in the sections), so each floor plan cuts its own building; a View Map view <N>-P<floor> per story, published with the sections (one-time Organizer step again), two registration squares (1.0 m and 0.5 m) 6 m off opposite corners of the building on every floor; BUILD_SIG geometry-6 (one rebuild); v1.16 (Aras 15 Nov 17:32 UTC "make sure archicad drawing is %100 pinpoint accurate to our masterplan"): his master.svg pieces inside the working area built in Archicad on his own points (slabs per layer, on the survey ground), canopies held within 0.05 m of his kanopi line, and an accuracy check after every build: each piece read back from Archicad and compared with master.svg, any point more than 5 cm off FLAGged, report in mp_accuracy.json; BUILD_SIG geometry-5 (one rebuild); v1.15 (Aras 15 Nov 17:27 UTC "draw these buildings in archicad and insert that drawing into all sections ... archicad is hella lot more detailed"): the context houses get more detail for the section elevations: a door on the ground floor of the longest wall a cut sees, windows on every wall a cut sees at any angle, balconies (slab + rail) on every other window bay of blocks of 3+ floors, a cornice band under every flat roof; a house with no recorded floor count is built as 1 floor (ASSUMED, logged) instead of left out; sizes are drawing rules, not surveyed; BUILD_SIG geometry-4 (one rebuild); v1.14 (Aras 15 Nov 17:24 UTC "any drawing that has building in it you should use the drawing that comes out of archicad"): the six node buildings built in Archicad as the node slides design them (placed by Perspectives, rooms from nodes common BUILD), each with a cut view <N>-BX and an elevation view <N>-BE in the "Bergama sections" folder (published with the sections); v1.13 = v1.13 (Aras 15 Nov 16:31-16:32 UTC "Make canopies top view match with masterplan", "Get structrual idea from the photo i have sent you and invent from there"): every canopy built on his own filled kanopi ring (no hull, no merging, outline within 0.25 m), facets by ear clipping with his fold ends on the outline, low / high vertices alternating round it, Y columns under the low vertices 1.2 m inside (4-10 m apart, arms toward the neighbouring vertices), plinth + deck bays between the columns; rooms and planters only where they fit inside; v1.12 (v1.11 publish run: 10.5 min for 13 DWGs): no vector sun shadows in the section views; a change of the view settings (SEC_SIG) publishes once even when the model is unchanged   # v1.11 (run of v1.10: the Archicad 29 API refused "CutPlane" too): sections listed through Tapir GetElementsByType (CutPlane)   # v1.10 (Aras 15 Nov 15:00 "you need to make archicad runs faster"): the model is rebuilt only when its inputs changed (buildings from MapBase, cut lines, masterplan canopies, Sections levels, BUILD_SIG) or Archicad holds other element counts; with the model and sections unchanged nothing is published either (the last DWGs are kept); model time logged; sections listed as element type CutPlane (v1.9 run: "Section" is not an API type)   # v1.9 (15 Nov: Archicad reopened from a recovery file: new GUIDs, the build doubled, 9 section views twice): the previous model is cleared by element type (windows, walls, slabs, roofs, meshes, columns, beams), not by recorded GUIDs; when the project\'s sections differ from the recorded ones, all sections and the "Bergama sections" View Map folder are made again (FLAG: refresh the publisher set)   # v1.8 (15 Nov: a refreshed publisher set held the whole project as PDF + DWG and Archicad hung an hour; the pln reopened without the build after a restart): the project is saved (Tapir SaveProject) before publishing, and only the set's items of our sections are published (selectedNavigatorItemIds); a set holding other items is not published whole   # v1.7 (Sections thread, run of v1.28.2: houses up the hill float, the survey TIN does not reach that hill): the ground behind each cut in depth bands (10-50, 50-100, 100-200, 200-400 m, 400 m to the farthest building), each the highest survey ground of the band raised to the base of every building standing in it, so every house has ground under it; written to acbuild.json cuts[].bands   # v1.6 (also: the ground-behind profile reaches 1000 m, as houses of other cuts beyond 200 m show in the sections); v1.6 (Aras 15 Nov 09:52-10:29 "draw our canopies much better like designed ones" / "Some closed areas underneath" / canopies in Archicad "yes please"): his master.svg canopies (kanopi layer) built as his reference: folded triangle-facet roof (meshes) with a timber louvre layer under it, Y steel columns (trunk + 2 arms) under the valleys on a 12 m bay, timber deck on a stone plinth bay by bay, a glazed room in every other bay where the floor is >= Q500 + 0.60 m, timber planters in the open bays; heights as Sections v1.28.2 (DfT 2.30 m clear, EA 0.60 m over Q500, ridge +1.8 m ASSUMED)   # v1.5 + Kızıl Avlu: the main hall outline(s) from the MasterplanBase cache (Sections library red_hall_load), roofless walls 19 m (Wikipedia, Red Basilica: "Its walls still survive up to a height of 19 metres"), no windows, no roof; v1.5 (15 Nov run 7: houses beyond the 200 m depth drawn as floating outlines): no marked distant area (only the 200 m behind each cut is drawn); publishing may take 30 min (the set grew)   # v1.4 v1.4 (15 Nov: Sections v1.18 moved the N4 lines): the Archicad origin is kept from the first run; a section whose line moved is deleted and made again on the new line (its view too), with a FLAG to refresh the publisher set   # v1.3 (run 4: houses 200 m behind stood in the sky, the hill under them was not drawn): per cut the ground behind (highest survey ground 10-200 m behind, every 2 m) written to acbuild.json for SectionsAC   # v1.2 (SectionsAC run 3: the DWGs held only the roofs = the one element type without a BG layer, so the BG layers are not shown in the views): every element on the tool default layers; registration blocks at -50 m (found by geometry); no terrain mesh (our ground is drawn instead)   # v1.1 (14 Nov run 1): mesh without layerIndex (Tapir schema), hipped roofs as one-level polyroofs, footprints cleaned (slab failures)
GH_LABEL = "AcBuild"
OUT_FOLDER = "bergama_archicad_site"   # v1.42: own cache (the sections project keeps bergama_archicad)
LOG_NAME = "bergama_acbuild_site_log.txt"
GH_INPUTS = {}
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
CACHE_DIR = os.path.join(BERGAMA_ROOT, "cached", OUT_FOLDER)
OUT_DIR = CACHE_DIR
DWG_DIR = os.path.join(CACHE_DIR, "dwg")
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
LIB_GLOB = os.path.join(BERGAMA_ROOT, "scripts", "bergama_sections_v*.py")

PORTS = range(19723, 19744)        # Archicad's JSON API ports (the first Archicad opened takes 19723)
SHADOWS = False                    # v1.12: vector sun shadows off in the section views (publish took 10.5 min)
SEC_SIG = "sections-aras-2026-11-15-pdf-strip-ownpens-nodistant"    # v1.12: change with the section view settings (forces one publish)
BUILD_SIG = "acbuild-geometry-tiles-1"   # v1.32: ground tiles; v1.31: one ground + SEO; v1.30: town ground; v1.29: the whole Selinos; v1.28: collisions; v1.27: SEO terrain cuts + retaining walls; v1.26: minimal folds; v1.25: canopies with Roof/Beam tools; v1.21: bridges + stepped terraces from outlines; v1.19: seating tiers; v1.18: materials; v1.17: building stories; v1.16: masterplan pieces; v1.15: house detail;   # v1.14: node buildings; v1.13 = v1.13: canopies on his outlines; v1.10: change when the element-making code changes (forces a rebuild)
CLEAR_TYPES = ["Window", "Door", "Wall", "Slab", "Roof", "Mesh", "Column", "Beam"]   # v1.9: what AcBuild makes
PUB_SET = "Bergama_Sections"       # publisher set name (made once by hand: DWG, the "Bergama sections" views)
VIEW_FOLDER = "Bergama sections"
BACK_M = 200.0                     # m behind the cut: the Sections script's BACK_M (v1.7)
VIEW_M = 1000.0                    # v1.6: the ground-behind profile reaches this far (run 9: houses of the other cuts
                                   # seen beyond 200 m floated over a 200 m profile in N1-B)
SIDE_M = 10.0                      # m in front of the line still modelled (the buildings the line cuts)
STOREY = {"sacred": 5.0, "monument": 5.0, "civic": 3.5, "industry": 4.5}   # else STOREY_M
STOREY_M = 3.0
INDUSTRY_TAGS = ("industrial", "warehouse", "factory", "manufacture")
FLAT_FLOORS = 4                    # Sections FLAT_ROOF_FLOORS: from 4 floors a flat roof with a 0.6 m parapet
ROOF_DEG, EAVE_M = 30.0, 0.4       # Sections ROOF_PITCH_DEG, EAVE_M (drawing rule)
WIN_W, WIN_H, WIN_SILL, WIN_STEP = 1.2, 1.4, 0.9, 3.0   # Sections drawing rule (not surveyed)
DOOR_W, DOOR_H = 1.0, 2.2          # v1.14: m, ground-floor door (drawing rule, not surveyed)
BAL_D, BAL_W, BAL_T, RAIL_H = 1.2, 1.8, 0.18, 1.0   # v1.14: m, balcony depth / width / slab / rail (drawing rule)
BAL_FLOORS = 3                     # v1.14: balconies on blocks from 3 floors
CORNICE_M, CORNICE_T = 0.25, 0.3   # v1.14: m, cornice projection / depth under a flat roof (drawing rule)
FRAME_SP_M = 5.0                   # v1.44: m, column grid of the house frames: ASSUMED (typical RC span, no source)
FRAME_COL_M = 0.30                 # v1.44: m, square column side: ASSUMED
FRAME_BEAM_W, FRAME_BEAM_H = 0.25, 0.40   # v1.44: m, beam width / depth under the slabs: ASSUMED
RAFT_T_M = 0.40                    # v1.44: m, raft foundation thickness under the lowest ground: ASSUMED (no source)
WALL_T, PLINTH = 0.3, 1.0          # m wall thickness; m the walls start below the ground at the centroid
GRID_M = 2.0                       # m: spot heights thinned to one per cell for the terrain mesh
REG_Z = -50.0                       # m above sea level: the registration blocks sit here (below every survey height)
SUN = (135.0, 35.0)                # deg azimuth to the cut plane, altitude: the shadow light (a drawing choice)
CHUNK = 400                        # elements per Tapir call
CACHE_CMDS = ("CreateSlabs", "CreateWalls", "CreateMeshes", "CreateColumns", "CreateBeams", "CreateRoofs",
              "CreateWindows", "CreateDoors")   # v1.34: model elements kept between passes by the hash of their data
KEEP = {}                          # v1.34: hash -> [guid] of the last pass, still in the model (main fills it)
ITEMS = []                         # v1.34: this pass [hash, guid, bbox Archicad m]
NEW_G = set()                      # v1.34: guids made in this pass
N_KEPT = [0]
LAYERS = ("BG terrain", "BG buildings", "BG reg")
MESH = True                        # v1.23 (Aras 15 Nov 20:00 "archicad is missing the ground"): the survey terrain is built
                                   # (v1.2-v1.22: off; SectionsAC colours it as ground and draws it under everything)


# ================================================================ Archicad over its JSON port
class AC(object):
    def __init__(self, log):
        import urllib.request
        self.rq, self.log, self.url = urllib.request, log, None
        for p in PORTS:
            try:
                r = self._post("http://127.0.0.1:%d" % p, {"command": "API.IsAlive"}, 2.0)
                if r.get("result", {}).get("isAlive"):
                    self.url = "http://127.0.0.1:%d" % p
                    break
            except Exception:
                continue
        if not self.url:
            raise RuntimeError(u"no Archicad found on ports 19723-19743: open Archicad with a project, then press again")

    def _post(self, url, body, timeout=600.0):
        req = self.rq.Request(url, json.dumps(body).encode("utf-8"), {"Content-Type": "application/json"})
        with self.rq.urlopen(req, timeout=timeout) as f:
            return json.loads(f.read().decode("utf-8"))

    def api(self, cmd, params=None, timeout=600.0):
        b = {"command": cmd}
        if params is not None:
            b["parameters"] = params
        r = self._post(self.url, b, timeout)
        if not r.get("succeeded"):
            raise RuntimeError(u"%s failed: %s" % (cmd, json.dumps(r.get("error"))[:300]))
        return r.get("result") or {}

    def t(self, name, params=None, timeout=600.0):
        p = {"addOnCommandId": {"commandNamespace": "TapirCommand", "commandName": name}}
        if params is not None:
            p["addOnCommandParameters"] = params
        r = self.api("API.ExecuteAddOnCommand", p, timeout).get("addOnCommandResponse") or {}
        if isinstance(r, dict) and r.get("error"):
            raise RuntimeError(u"Tapir %s: %s" % (name, json.dumps(r["error"])[:300]))
        return r

    def has(self, name):
        try:
            return bool(self.api("API.IsAddOnCommandAvailable", {"addOnCommandId": {
                "commandNamespace": "TapirCommand", "commandName": name}}).get("available"))
        except Exception:
            return False

    def create(self, name, key, items, what):
        """v1.34: an element whose data is the same as one of the last pass that is still in the model is kept (its
        guid returned, nothing sent to Archicad); only the others are made"""
        if name not in CACHE_CMDS:
            return self._create(name, key, items, what)
        import hashlib
        hs = [hashlib.sha1((name + json.dumps(it, sort_keys=True, default=str)).encode("utf-8")).hexdigest()
              for it in items]
        out, todo = [], []
        for i, h in enumerate(hs):
            g = KEEP[h[:16]].pop() if KEEP.get(h[:16]) else None   # v1.44: the fingerprint in the Element ID
            out.append(g)
            if not g:
                bb_ = _bbox(items[i]) if LOCKED_BB else None
                if bb_:                                   # v1.44: a hand-edited element of this kind stands here
                    cx_, cy_ = (bb_[0] + bb_[2]) / 2.0, (bb_[1] + bb_[3]) / 2.0
                    if any(t_ == TYPE_OF.get(name) and b_[0] <= cx_ <= b_[2] and b_[1] <= cy_ <= b_[3]
                           for t_, b_ in LOCKED_BB):
                        N_LOCKSKIP[0] += 1
                        continue
                todo.append(i)
        kept = len(items) - len(todo)
        N_KEPT[0] += kept
        if todo:
            new = self._create(name, key, [items[i] for i in todo], what)
            for i, g in zip(todo, new):
                out[i] = g
                if g:
                    NEW_G.add(g)
        if kept:
            self.log.append(u"%s: %d kept from the last pass (same data)" % (what, kept))
        for h, g, it in zip(hs, out, items):
            if g:
                ITEMS.append([h, g, _bbox(it)])
        return out

    def _create(self, name, key, items, what):
        """items in chunks; [(guid or None)] in input order; errors counted and logged once"""
        out, err = [], []
        lab = next((m for w, m in LABEL_MAT if what.startswith(w)), None)      # v1.18: his legend material
        plain = [dict((k, v) for k, v in it.items() if k != "_mat") if isinstance(it, dict) else it for it in items]
        if name in MAT_CMDS and MAT_ID:
            items = [dict(p_, buildingMaterialId=MAT_ID[m_]) if (m_ in MAT_ID and "buildingMaterialId" not in p_) else p_
                     for p_, m_ in zip(plain, [(it.get("_mat") or lab) if isinstance(it, dict) else None for it in items])]
        else:
            items = plain
        n_matfail = 0
        for i in range(0, len(items), CHUNK):
            part = items[i:i + CHUNK]
            for k_try in (0, 1):                     # v1.36: new elements go into the floor plan's database
                try:
                    self.t("ChangeWindow", {"windowType": "FloorPlan", "storyIndex": 0})
                except Exception:
                    pass
                try:
                    r = self.t(name, {key: part})
                    lst = r.get("elements") or r.get("elementIds") or []
                except Exception as ex:
                    lst = [{"error": {"message": u"%s" % ex}}] * len(part)
                if any(isinstance(e, dict) and (e.get("elementId") or {}).get("guid") for e in lst) or k_try:
                    break
                time.sleep(2.0)                      # v1.36: all refused: once more after the switch
            bad = [j for j, e in enumerate(lst) if not (isinstance(e, dict) and (e.get("elementId") or {}).get("guid"))]
            cb_ = [j for j in bad if isinstance(part[j], dict) and "compositeId" in part[j]]
            if cb_:                                   # v1.44: a composite refused: the same element, basic
                try:
                    r3 = self.t(name, {key: [dict(((k_, v_) for k_, v_ in part[j].items() if k_ != "compositeId"),
                                                  structureType="Basic") for j in cb_]})
                    for j, e in zip(cb_, r3.get("elements") or r3.get("elementIds") or []):
                        lst[j] = e
                    self.log.append(u"FLAG %s: %d refused with their composite, made basic" % (what, len(cb_)))
                except Exception:
                    pass
                bad = [j for j, e in enumerate(lst) if not (isinstance(e, dict) and (e.get("elementId") or {}).get("guid"))]
            if bad and any("buildingMaterialId" in part[j] for j in bad):            # v1.18: again without it
                n_matfail += len(bad)
                try:
                    r2 = self.t(name, {key: [plain[i + j] for j in bad]})
                    l2 = r2.get("elements") or r2.get("elementIds") or []
                    for j, e in zip(bad, l2):
                        lst[j] = e
                except Exception:
                    pass
            for e in lst:
                g = (e.get("elementId") or {}).get("guid") if isinstance(e, dict) else None
                out.append(g)
                if not g:
                    err.append(json.dumps(e)[:200])
        self.log.append(u"%s: %d made%s" % (what, sum(1 for g in out if g), u"" if not err else
                                                u"; FLAG %d failed, first: %s" % (len(err), err[0])))
        if n_matfail:
            self.log.append(u"FLAG %s: %d refused with the legend material, made again without it" % (what, n_matfail))
        return out


def _bbox(o):
    """v1.34: the plan box of every x, y in an element's data (Archicad m), or None"""
    xs, ys = [], []

    def w(v):
        if isinstance(v, dict):
            if isinstance(v.get("x"), (int, float)) and isinstance(v.get("y"), (int, float)):
                xs.append(v["x"])
                ys.append(v["y"])
            for u_ in v.values():
                w(u_)
        elif isinstance(v, list):
            for u_ in v:
                w(u_)
    w(o)
    return [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)] if xs else None


# ================================================================ v1.18: his texture legend as Archicad materials
# (Aras 15 Nov 18:12-18:17 UTC); colours = median colour of each legend picture he sent (or of its named part), hex
MAT = {"bridge_stone": ("Bergama bridge stone", "928D8B", "Matte", 0),       # 18:12 bridges (stone paving)
       "terrace_stone": ("Bergama stepped terrace stone", "E5DFD7", "Matte", 0),   # 18:15 stepped terrace
       "timber": ("Bergama timber deck", "BAA89A", "Matte", 0),             # 18:13 decks
       "rc": ("Bergama reinforced concrete", "A7A6A1", "Matte", 0),          # v1.44: composites (colours ASSUMED)
       "brick": ("Bergama hollow clay brick", "B0674F", "Matte", 0),
       "aac": ("Bergama aerated concrete block", "D9D6CE", "Matte", 0),
       "bims": ("Bergama pumice block", "9E9B94", "Matte", 0),
       "plaster": ("Bergama cement plaster", "ECE7DE", "Matte", 0),
       "lime": ("Bergama lime plaster", "E6DECF", "Matte", 0),
       "rubble": ("Bergama rubble stone", "8E8577", "Matte", 0),
       "eps": ("Bergama EPS insulation", "F1F1EC", "Matte", 0),
       "xps": ("Bergama XPS insulation", "A9C6D3", "Matte", 0),
       "rooftile": ("Bergama clay roof tile", "A0523A", "Matte", 0),
       "gravel": ("Bergama roof gravel", "B3ADA3", "Matte", 0),
       "screed": ("Bergama screed and floor finish", "C9C5BC", "Matte", 0),
       "rooftimber": ("Bergama roof timber", "9C7A55", "Matte", 0),
       "riverbed": ("Bergama river bed gravel", "9A9384", "Matte", 0),      # v1.44: colour ASSUMED
       "pavement": ("Bergama pavement (concrete pavers)", "B9B4AA", "Matte", 0),   # v1.44: colour ASSUMED
       "stair": ("Bergama stair (concrete, stone treads)", "A9A7A2", "Matte", 0),  # v1.44: colour ASSUMED
       "foliage": ("Bergama foliage", "5E7046", "Matte", 0),               # v1.44: tree crowns
       "bark": ("Bergama bark", "5B4A3A", "Matte", 0),                      # v1.44: tree trunks
       "water": ("Bergama water", "5C7A86", "Glass", 30),                   # v1.44: river water (palette 5C7A86)
       "reed": ("Bergama reed bed", "707D56", "Matte", 0),                  # 18:14 reed beds (the green blades)
       "shade_white": ("Bergama shading facet white", "F4F4F4", "Matte", 0),   # 18:14 shading facets
       "frame_grey": ("Bergama shading frame grey", "818282", "Matte", 0),     # 18:14 shading frame lines
       "our_white": ("Bergama our building white", "F7F7F7", "Matte", 0),     # 18:13 our buildings
       "heritage_red": ("Bergama historic red", "B56D61", "Matte", 0),       # 18:13 historic buildings (red roof)
       "quay_grey": ("Bergama quay paving grey", "CECFCE", "Matte", 0),
       "road": ("Bergama road surface", "8C8B87", "Matte", 0),             # v1.30: design colour (not in his legend)
       "park": ("Bergama park green", "A3B48C", "Matte", 0),             # v1.30: design colour (not in his legend)
       "ground": ("Bergama ground", "E4E0CF", "Matte", 0)}               # v1.37: the Sections ground fill (E4E0CF)               # v1.30: design colour (not in his legend)     # v1.19: iskele kenari's own picture        # 18:13 historic buildings (red roof)
CUT_FILL = {"bridge_stone": "Cut Stone", "terrace_stone": "Cut Stone", "timber": "Wood", "rc": "Structural Concrete",
            "brick": "Common Brick", "aac": "Lightweight Concrete", "bims": "Concrete Block", "plaster": "Plaster",
            "lime": "Plaster", "rubble": "Rubble", "eps": "Rigid Insulation", "xps": "Rigid Insulation",
            "rooftile": "Roof Tile", "gravel": "Gravel", "screed": "Lightweight Concrete", "rooftimber": "Wood",
            "reed": "Grass", "heritage_red": "Rubble", "quay_grey": "Cut Stone", "road": "Gravel", "park": "Grass",
            "ground": "Earth", "riverbed": "Gravel", "pavement": "Concrete Block", "stair": "Structural Concrete"}   # v1.44: material -> Archicad fill of its cut (the rest: solid Foreground)
REAL_SURF = {"plaster": "Stucco - White Rough", "lime": "Stucco - Beige Rough", "brick": "Brick - Red",
             "aac": "Concrete - 02", "bims": "Concrete - 04", "rc": "Concrete - 10", "rubble": "Stonework - 02",
             "rooftile": "Roof Tiles - Spanish 01", "gravel": "Concrete - 04", "screed": "Concrete - 02",
             "road": "Pavement - Asphalt Dark", "park": "Grass - Green", "ground": "Grass - Brown",
             "riverbed": "Stonework - 13", "foliage": "Foliage - Leaves Tree Small", "bark": "Bark - Deciduous",
             "water": "Water - Wavy", "pavement": "Stonework - 12", "stair": "Stone - Granite Gray", "eps": "Insulation - Solid Brown", "xps": "Insulation - Solid Brown",
             "rooftimber": "Wood - Pine Grained Horizontal"}   # v1.44: textured project surfaces (else the colour)
MAT_PRIO = {"rc": 900, "rubble": 850, "heritage_red": 850, "bridge_stone": 850, "brick": 600, "aac": 600, "bims": 600,
            "stair": 700, "terrace_stone": 700, "our_white": 700, "frame_grey": 900, "shade_white": 700, "timber": 500,
            "rooftimber": 500, "screed": 400, "pavement": 400, "quay_grey": 400, "road": 350, "rooftile": 300,
            "gravel": 300, "eps": 200, "xps": 200, "plaster": 100, "lime": 100, "riverbed": 80, "park": 60, "ground": 50,
            "reed": 40, "foliage": 30, "bark": 500, "water": 10}   # v1.44: Archicad connection priority (0-999)
SOLID_FILL = "Foreground"         # v1.44: Archicad's solid fill (Solid Fills folder)
GLASS = ("989BAD", 60)                         # 18:13 "blues are glasses": his glass blue, 60 % transparent (ours)
MAT_CMDS = ("CreateSlabs", "CreateWalls", "CreateMeshes", "CreateColumns", "CreateBeams", "CreateRoofs")
LABEL_MAT = (("canopy stone plinths", "terrace_stone"), ("canopy timber decks", "timber"), ("canopy planters", "timber"),
             ("canopy louvre layer", "timber"), ("canopy facet test", "shade_white"), ("canopy roof facets", "shade_white"),
             ("canopy Y column", "frame_grey"), ("canopy glazed rooms", "our_white"),
             ("node buildings: stone plinths", "terrace_stone"), ("node buildings", "our_white"),
             ("node roof facet test", "our_white"), ("node N4 platform columns", "our_white"))
PIECE_MAT = (("kopruler", "bridge_stone"), ("begum_su_merdiven", "terrace_stone"), ("teras", "timber"),
             ("iskele_kenari", "quay_grey"), ("su_bitkii", "reed"))   # v1.19: by the median colour of each layer's
# own picture in master.svg: teras BDAA9B = his wood (Aras 19:11 "decks are wooden"), begum su merdiven E8E2DA = the
# stepped-terrace stone, iskele kenari CECFCE = grey paving (not in his legend: his own picture colour), kopruler 898582    # his layer (any part of the key) -> material
TIER_D, TIER_H = 1.20, 0.48                    # v1.19: Aras 19:09 UTC 1.2 m deep; 19:13 "make the height of the steps is 12": 4 steps of 12 x 30 cm merged
TIER_KEYS = ("begum_su_merdiven",)            # v1.19: his stepped terraces into the river (light stone picture)
OUTLINE_LAYERS = ("kopruler", "begum_su_merdiven")   # v1.21: drawn as unfilled outlines in his file
TIER_N = [0, 0]                                # v1.19: tiers made, pieces stepped
RIVER_PTS = []                                 # v1.19: points of his river outline (su_outline), survey m
HERITAGE_FABS = ("sacred", "monument", u"Kızıl Avlu")
MAT_ID = {}                                    # material key -> building material guid (filled by setup_materials)
PIECE_KEY = {}                                 # id(piece outline) -> material key (site_pieces)


def _pid(ac):
    """v1.44: guid of the built-in Element ID property"""
    r = ac.api("API.GetPropertyIds", {"properties": [{"type": "BuiltIn", "nonLocalizedName": "General_ElementID"}]})
    return r["properties"][0]["propertyId"]["guid"]


def read_ids(ac, gs, pid):
    """v1.44: guid -> Element ID text"""
    out = {}
    for i in range(0, len(gs), 2000):
        part = gs[i:i + 2000]
        r = ac.api("API.GetPropertyValuesOfElements", {"elements": [{"elementId": {"guid": g}} for g in part],
                                                       "properties": [{"propertyId": {"guid": pid}}]}, 900.0)
        for g, e in zip(part, r.get("propertyValuesForElements") or []):
            try:
                out[g] = u"%s" % e["propertyValues"][0]["propertyValue"]["value"]
            except Exception:
                pass
    return out


def read_bb(ac, gs):
    """v1.44: guid -> 3D box (x0, y0, z0, x1, y1, z1), Archicad m"""
    out = {}
    for i in range(0, len(gs), 2000):
        part = gs[i:i + 2000]
        r = ac.api("API.Get3DBoundingBoxes", {"elements": [{"elementId": {"guid": g}} for g in part]}, 900.0)
        for g, e in zip(part, r.get("boundingBoxes3D") or []):
            b = (e or {}).get("boundingBox3D") if isinstance(e, dict) else None
            if b:
                out[g] = (b["xMin"], b["yMin"], b["zMin"], b["xMax"], b["yMax"], b["zMax"])
    return out


def parse_id(t):
    """v1.44: "BGA-<fingerprint 16>@<box in cm>" -> (fingerprint, box or None), else None"""
    if not t or not t.startswith(ID_PREFIX):
        return None
    h, _, b = t[len(ID_PREFIX):].partition("@")
    try:
        bb = tuple(int(x) / 100.0 for x in b.split(","))
    except Exception:
        bb = None
    return h[:16], (bb if bb and len(bb) == 6 else None)


def stamp(ac, pid, pairs):
    """v1.44: write "BGA-<fingerprint>@<its 3D box now>" into each element's Element ID; returns how many"""
    bbs = read_bb(ac, [g for g, h in pairs])
    vals = [{"elementId": {"guid": g}, "propertyId": {"guid": pid},
             "propertyValue": {"value": ID_PREFIX + h[:16] + (u"@" + u",".join(str(int(round(v * 100))) for v in bbs[g])
                                                              if g in bbs else u"")}} for g, h in pairs]
    n = 0
    for i in range(0, len(vals), 1000):
        try:
            r = ac.api("API.SetPropertyValuesOfElements", {"elementPropertyValues": vals[i:i + 1000]}, 900.0)
            n += sum(1 for e in (r.get("executionResults") or []) if isinstance(e, dict) and e.get("success"))
        except Exception:
            pass
    return n


def _read_extra(log):
    """v1.44: from the open Rhino survey: floor-count labels [value, x, y] (YAZI_KAT_ADEDI texts) and stair step edges
    [x0, y0, z0, x1, y1, z1] (BINA_MERDIVEN lines)"""
    import Rhino
    d = Rhino.RhinoDoc.ActiveDoc
    lab, st = [], []
    for nm, out in (("YAZI_KAT_ADEDI", lab), ("BINA_MERDIVEN", st)):
        li = d.Layers.FindByFullPath(nm, -1)
        if li < 0:
            log.append(u"FLAG survey layer %s not found" % nm)
            continue
        for o in d.Objects.FindByLayer(d.Layers[li]):
            g = o.Geometry
            if nm == "YAZI_KAT_ADEDI" and isinstance(g, Rhino.Geometry.TextEntity):
                t = (g.PlainText or u"").strip()
                if t.isdigit():
                    c = g.GetBoundingBox(True).Center
                    out.append([int(t), round(c.X, 3), round(c.Y, 3)])
            elif nm == "BINA_MERDIVEN" and isinstance(g, Rhino.Geometry.Curve):
                a, b = g.PointAtStart, g.PointAtEnd
                out.append([round(a.X, 3), round(a.Y, 3), round(a.Z, 3), round(b.X, 3), round(b.Y, 3), round(b.Z, 3)])
    log.append(u"survey extras: %d floor-count labels, %d stair step edges" % (len(lab), len(st)))
    return lab, st


def _in_rhino():
    """v1.44: True inside Rhino with a document open"""
    try:
        import Rhino
        return Rhino.RhinoDoc.ActiveDoc is not None
    except Exception:
        return False


def _tin_from(L_, pts, tri):
    """v1.44: the library's Tin from cached triangles (no Grasshopper needed)"""
    T = L_["Tin"].__new__(L_["Tin"])
    T.p, T.t, T.cell = pts, [tuple(t) for t in tri], {}
    for t in T.t:
        xs = [pts[i][0] for i in t]
        ys = [pts[i][1] for i in t]
        for i in range(int(min(xs) // 5), int(max(xs) // 5) + 1):
            for j in range(int(min(ys) // 5), int(max(ys) // 5) + 1):
                T.cell.setdefault((i, j), []).append(t)
    return T


def _rgb(h):
    return {"red": int(h[0:2], 16) / 255.0, "green": int(h[2:4], 16) / 255.0, "blue": int(h[4:6], 16) / 255.0}


# v1.44 (Aras 11:30 "generic composites ... educated guesses accordingly what is highly used in turkey"): skins from the
# outside / top in, thickness m: ALL ASSUMED (common Turkish practice, not surveyed, no source)
COMP = {
    "wall_regular": (u"Bergama wall - planned low-rise (RC frame, hollow brick, EPS)", "Wall",
                     [("Finish", "plaster", 0.03), ("Other", "eps", 0.05), ("Core", "brick", 0.19), ("Finish", "plaster", 0.02)]),
    "wall_block": (u"Bergama wall - apartment block (RC frame, AAC, EPS)", "Wall",
                   [("Finish", "plaster", 0.03), ("Other", "eps", 0.05), ("Core", "aac", 0.20), ("Finish", "plaster", 0.02)]),
    "wall_selfbuilt": (u"Bergama wall - self-built / gecekondu (pumice block)", "Wall",
                       [("Finish", "plaster", 0.02), ("Core", "bims", 0.15), ("Finish", "plaster", 0.02)]),
    "wall_traditional": (u"Bergama wall - traditional (rubble stone, lime plaster)", "Wall",
                         [("Finish", "lime", 0.03), ("Core", "rubble", 0.50), ("Finish", "lime", 0.02)]),
    "wall_large": (u"Bergama wall - large / public (RC frame, AAC, EPS)", "Wall",
                   [("Finish", "plaster", 0.03), ("Other", "eps", 0.06), ("Core", "aac", 0.25), ("Finish", "plaster", 0.02)]),
    "floor_rc": (u"Bergama floor - RC slab, screed", "Slab",
                 [("Finish", "screed", 0.05), ("Core", "rc", 0.18), ("Finish", "plaster", 0.02)]),
    "roof_tile": (u"Bergama roof - clay tile on timber", "Roof",
                  [("Finish", "rooftile", 0.03), ("Core", "rooftimber", 0.20), ("Finish", "plaster", 0.02)]),
    "roof_flat": (u"Bergama roof - gravel, XPS, RC", "Roof",
                  [("Finish", "gravel", 0.05), ("Other", "xps", 0.08), ("Finish", "screed", 0.05), ("Core", "rc", 0.12)]),
}
WALL_COMP = {"regular": "wall_regular", "block": "wall_block", "selfbuilt": "wall_selfbuilt",
             "traditional": "wall_traditional", "large": "wall_large"}   # MapBase fabric -> wall composite
FRAME_SKIP_FABS = ("traditional",)   # v1.44: traditional houses are load-bearing masonry: no RC frame (ASSUMED)
COMP_ID, COMP_T = {}, {}


def setup_composites(ac, log):
    """v1.44: the COMP composites (made or overwritten by name) from the Bergama building materials"""
    COMP_ID.clear(); COMP_T.clear()
    if not MAT_ID or not ac.has("CreateComposites"):
        log.append(u"FLAG composites not made (no materials or Tapir lacks CreateComposites): basic walls / slabs / roofs")
        return
    try:
        lt = ac.t("GetAttributesByType", {"attributeType": "Line"}).get("attributes") or []
        sol = next((a for a in lt if (a.get("name") or u"").lower().startswith("solid")), lt[0] if lt else None)
        data = []
        for k, (nm, use, sk) in COMP.items():
            if not all(m_ in MAT_ID for _t, m_, _d in sk):
                continue
            data.append(dict(name=nm, useWith=[use], skins=[dict(type=t_, buildingMaterialId={"attributeId": MAT_ID[m_]},
                                                                 framePen=1, thickness=d_) for t_, m_, d_ in sk],
                             separators=[dict(lineTypeId={"attributeId": sol["attributeId"]}, linePen=1)
                                         for _i in range(len(sk) + 1)]))
        ac.t("CreateComposites", {"overwriteExisting": True, "compositeDataArray": data})
        have = dict((a.get("name"), a) for a in (ac.t("GetAttributesByType", {"attributeType": "Composite"}).get(
            "attributes") or []))
        for k, (nm, use, sk) in COMP.items():
            if nm in have:
                COMP_ID[k] = have[nm]["attributeId"]
                COMP_T[k] = round(sum(d_ for _t, _m, d_ in sk), 3)
        log.append(u"composites (ASSUMED, common Turkish practice): %d of %d made: %s" % (
            len(COMP_ID), len(COMP), u"; ".join(u"%s %.2f m" % (COMP[k][0], COMP_T[k]) for k in COMP_ID)))
    except Exception as ex:
        log.append(u"FLAG composites not made (%s): basic walls / slabs / roofs" % ex)


def setup_override(ac, log):
    """v1.44 (Aras 11:30 "give me a override that show those walls as a single solid hatch"): rule + combination,
    made once (kept when they exist by name)"""
    try:
        have = ac.t("GetGraphicOverrideRules", {}).get("graphicOverrideRules") or []
        rid = next((r["graphicOverrideRuleId"] for r in have if r.get("name") == u"Bergama - walls as one solid poche"), None)
        if rid is None:
            fl_ = dict((a.get("name"), a) for a in (ac.t("GetAttributesByType", {"attributeType": "Fill"}).get(
                "attributes") or []))
            ft = {"cutFill": True, "coverFill": False, "draftingFill": False}
            r = ac.t("CreateGraphicOverrideRules", {"graphicOverrideRules": [dict(
                name=u"Bergama - walls as one solid poche", ruleGroupName=u"Bergama", criterion={"elementType": "Wall"},
                style=dict(fillType=fl_[SOLID_FILL]["attributeId"], fillTypeAppliesTo=ft, fillForegroundPen=21,
                           fillForegroundPenAppliesTo=ft, showSkinSeparators=False))]})
            rid = r["graphicOverrideRuleIds"][0]["graphicOverrideRuleId"]
            ac.t("CreateGraphicOverrideCombinations", {"graphicOverrideCombinations": [dict(
                name=u"Bergama - solid walls", graphicOverrideRuleIds=[{"graphicOverrideRuleId": rid}])]})
            log.append(u"graphic override: rule \"Bergama - walls as one solid poche\" in combination \"Bergama - solid "
                       u"walls\" made (walls cut as one solid fill, pen 21, no skin separators)")
    except Exception as ex:
        log.append(u"FLAG graphic override not made (%s)" % ex)


def _wt(b):
    """v1.44: wall thickness of a house: its composite's, else WALL_T"""
    k = WALL_COMP.get(b.get("fab"))
    return COMP_T.get(k, WALL_T) if b.get("fab") not in HERITAGE_FABS else WALL_T


def _wcomp(b):
    k = WALL_COMP.get(b.get("fab"))
    if b.get("fab") in HERITAGE_FABS or k not in COMP_ID:
        return {}
    return dict(structureType="Composite", compositeId=COMP_ID[k])


def _ccomp(k, t, basic=None):
    """v1.44: composite fields for a slab / roof, else a basic one of thickness t"""
    if k in COMP_ID:
        return dict(thickness=COMP_T[k], structureType="Composite", compositeId=COMP_ID[k])
    return dict(thickness=t, **({"structureType": basic} if basic else {}))


def setup_materials(ac, log):
    """v1.18: one surface + one building material per legend entry (made or overwritten by name), the project's glass
    surfaces turned to his glass blue; MAT_ID filled with the building material guids"""
    MAT_ID.clear()
    need = ("GetAttributesByType", "CreateSurfaces", "CreateBuildingMaterials")
    if not all(ac.has(c) for c in need):
        log.append(u"FLAG materials: Tapir lacks %s: elements keep the Archicad defaults" % u", ".join(
            c for c in need if not ac.has(c)))
        return

    def heads(ty):
        return dict((a.get("name"), a) for a in (ac.t("GetAttributesByType", {"attributeType": ty}).get("attributes") or []))
    try:
        ac.t("CreateSurfaces", {"overwriteExisting": True, "surfaceDataArray": [
            dict(name=nm, materialType=ty, surfaceColor=_rgb(h), transparency=tr, ambientReflection=60,
                 diffuseReflection=80, specularReflection=5) for nm, h, ty, tr in MAT.values()]})
        sf = heads("Surface")
        glass = [(n, a) for n, a in sf.items() if n and "glass" in n.lower()]
        if glass:
            ac.t("CreateSurfaces", {"overwriteExisting": True, "surfaceDataArray": [
                dict(attributeId=a["attributeId"], name=n, materialType="Glass", surfaceColor=_rgb(GLASS[0]),
                     transparency=GLASS[1]) for n, a in glass]})
        sn_ = lambda k, nm: REAL_SURF[k] if REAL_SURF.get(k) in sf else nm          # v1.44: textured where there is one
        bm = [dict(name=nm, cutSurfaceIndex=int(sf[sn_(k, nm)]["index"]), _k=k) for k, (nm, h, ty, tr) in MAT.items()
              if nm in sf]
        log.append(u"surfaces (v1.44, real look): %s" % u", ".join(u"%s -> %s" % (MAT[k][0], REAL_SURF[k])
                                                                    for k in MAT if REAL_SURF.get(k) in sf))
        fl_ = heads("Fill")                            # v1.41: an explicit cut fill (was: none, so cuts drew no fill)
        sol = fl_.get(SOLID_FILL) or next((a for n, a in fl_.items() if n and n.lower() == "solid fill"), None)
        try:
            if sol is None:
                raise ValueError("no solid fill attribute found")
            fi_ = lambda b_: fl_.get(CUT_FILL.get(b_["_k"])) or sol     # v1.44: the fill of what it is
            ac.t("CreateBuildingMaterials", {"overwriteExisting": True, "buildingMaterialDataArray": [
                dict(((k_, v_) for k_, v_ in b_.items() if k_ != "_k"), cutFillIndex=int(fi_(b_)["index"]),
                     cutFillPen=CUT_FILL_PEN, cutFillBackgroundPen=0, connPriority=MAT_PRIO.get(b_["_k"], 500))
                for b_ in bm]})
            log.append(u"materials: cut fills by material (%s), else %s, pen %d (v1.44)" % (
                u", ".join(u"%s %s" % (MAT[b_["_k"]][0], fi_(b_).get("name")) for b_ in bm), sol.get("name"), CUT_FILL_PEN))
        except Exception as ex:
            log.append(u"FLAG materials: cut fill not set (%s): cuts may draw no fill" % ex)
            ac.t("CreateBuildingMaterials", {"overwriteExisting": True, "buildingMaterialDataArray": [
                dict((k_, v_) for k_, v_ in b_.items() if k_ != "_k") for b_ in bm]})
        bh = heads("BuildingMaterial")
        for k, (nm, h, ty, tr) in MAT.items():
            if nm in bh:
                MAT_ID[k] = bh[nm]["attributeId"]
        log.append(u"materials (his legend): %d of %d made (%s); glass surfaces in his blue #%s: %s" % (
            len(MAT_ID), len(MAT), u", ".join(u"%s #%s" % (MAT[k][0], MAT[k][1]) for k in MAT_ID), GLASS[0],
            u", ".join(n for n, a in glass) or u"none found"))
        if len(MAT_ID) < len(MAT):
            log.append(u"FLAG materials: %s not made" % u", ".join(MAT[k][0] for k in MAT if k not in MAT_ID))
    except Exception as ex:
        log.append(u"FLAG materials not made (%s): elements keep the Archicad defaults" % ex)


# ================================================================ the data (caches + survey)
def load_lib(log):
    fs = sorted(glob.glob(LIB_GLOB), key=lambda p: [int(x) for x in re.findall(r"\d+", os.path.basename(p))])
    if not fs:
        raise RuntimeError(u"%s missing: refresh the kit" % LIB_GLOB)
    ns = {"__name__": "bergama_sections_lib"}
    with open(fs[-1], encoding="utf-8") as f:
        exec(compile(f.read(), fs[-1], "exec"), ns)
    log.append(u"library: %s (%s)" % (fs[-1], ns.get("VERSION")))
    return ns


def read_json(path, what, log):
    if not os.path.isfile(path):
        raise RuntimeError(u"%s not found: press %s first" % (path, what))
    with open(path, encoding="utf-8") as f:
        J = json.load(f)
    log.append(u"%s: %s (%s %s)" % (what, path, J.get("version"), J.get("run") or J.get("made")))
    return J


def storey(fab, btag):
    if fab in ("sacred", "monument"):
        return STOREY[fab]
    if btag in INDUSTRY_TAGS:
        return STOREY["industry"]
    if fab == "large":
        return STOREY["civic"]
    return STOREY_M


def frame(A, B):
    L = math.hypot(B[0] - A[0], B[1] - A[1])
    u = ((B[0] - A[0]) / L, (B[1] - A[1]) / L)
    n = (-u[1], u[0])                       # the side the cut looks at (Sections context_for: behind = +n)
    return L, u, n


def so(p, A, u, n):
    dx, dy = p[0] - A[0], p[1] - A[1]
    return dx * u[0] + dy * u[1], dx * n[0] + dy * n[1]


def area(P):
    return 0.5 * sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(P, P[1:] + P[:1]))


def clean(R):
    """footprint without repeated (< 5 cm) and straight-through (< 1 deg) points: Archicad refused such slabs (run 1)"""
    Q = []
    for p in R:
        if not Q or math.hypot(p[0] - Q[-1][0], p[1] - Q[-1][1]) >= 0.05:
            Q.append(p)
    while len(Q) > 3 and math.hypot(Q[0][0] - Q[-1][0], Q[0][1] - Q[-1][1]) < 0.05:
        Q.pop()
    k = True
    while k and len(Q) > 3:
        k = False
        for i in range(len(Q)):
            a, b, c = Q[i - 1], Q[i], Q[(i + 1) % len(Q)]
            cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
            la, lb = math.hypot(b[0] - a[0], b[1] - a[1]), math.hypot(c[0] - b[0], c[1] - b[1])
            if abs(cr) <= math.sin(math.radians(1.0)) * la * lb:
                Q.pop(i)
                k = True
                break
    return Q


# ================================================================ v1.6 canopies (Aras 15 Nov 09:52-10:29)
# "draw our canopies much better like designed ones ... implement this kind of desing with it's rules" (his reference:
# folded triangle-facet roof skin, timber louvre layer, Y-shaped steel columns, timber deck on a stone plinth);
# "Some closed areas underneath" (glazed rooms); "are those canopies gonna be implemented into archicad ?" / "yes please".
# Footprints: his master.svg kanopi layer (MasterplanBase cache); rules and heights = the Sections script's (v1.28.2):
CAN_KEYS = (u"kanopi", u"teras_-_canopy")
CAN_CLEAR_M = 2.30     # DfT Inclusive Mobility 2021 s.3.2 "Generally, this should be a minimum of 2300mm" (Sections v1.26)
CAN_Q500_M = 0.60      # EA: floors "at least 600 millimetres ... above the estimated flood level", applied to Q500 (v1.26)
CAN_RISE_M = 0.6      # ridge above valley: DESIGN ASSUMPTION, UNVERIFIED (Sections v1.26)
CAN_T, CAN_LOUVRE_M = 0.15, 0.30                  # skin plate, louvre depth (design intent, Sections v1.28)
CAN_Y_FORK, CAN_Y_ARM_M = 0.6, 2.5                # Y fork at 60 % of the column, arm reach (design intent, v1.28)
CAN_PLINTH_M, CAN_DECK_M = 0.45, 0.12             # stone plinth, timber deck (design intent, v1.28.2)
CAN_PLANTER_M = 2.4                               # planter length (design intent, v1.28.2)
CAN_BAY_M = 0.0                                   # v1.13: no fixed bay; the columns follow each outline (below)
CAN_OUT_TOL = 0.05                                # v1.16: 0.05 (pinpoint); v1.13: m, the built outline within this of his drawn kanopi line
CAN_COL_IN = 1.2                                  # v1.13: m, a column stands this far inside the outline (ours)
CAN_COL_MIN, CAN_COL_MAX = 4.0, 10.0              # v1.13: m, columns at least / a high vertex at most this far apart
CAN_EAVE_F = 0.6                                  # outline edge at valley + 0.6 x rise: folds to knife edges (ours)
CAN_GLASS_W, CAN_GLASS_STEP = 1.4, 1.5            # glazing panes, mullion step (design intent, v1.28.2 1.5 m)
SEO_OPS, SEO_TERR = [], []                        # v1.27: slabs that cut the terrain; terrain meshes (guid, cut)
EXTRA_OPS = []                                    # v1.31: (guid, operation, point Archicad m) more elements that cut the ground
GROUND_TILE_M = 25.0                              # v1.38: 25 m (v1.32: 150 m) so the ground can follow the cut strips
GROUND_BEHIND_M = 200.0                           # v1.38: m of ground kept behind each cut line (ASSUMED: enough for the cut face)
GROUND_SPOT_M = 4.0                               # v1.32: one survey height per this many m cell in the ground
GROUND_EDGE_M = 5.0                               # v1.32: tile edge points every this many m (the same on both tiles)
GROUND_GRID_M = 10.0                              # v1.31: a ground control point every this many m where no survey height
CUT_FILL_PEN = 1                                  # v1.41: pen of the cut fills (ASSUMED: pen 1 of his pen set)
GROUND_BASE_M = 3.0                               # v1.31: the ground block reaches this far under its lowest point
WHOLE_SITE = True                                 # v1.42: the whole survey extent, not only the cut rectangles
SITE_TILE_M = 50.0                                # v1.42: ground tile size in the whole-site build (fewer meshes)
SITE_BATCH = 40                                   # v1.42: ground tiles per Tapir call
SITE_BOX = []                                     # v1.42: survey extent (x0, y0, x1, y1), survey m
NO_SAVE_PUBLISH = True                            # v1.42: Aras saves the pln himself; nothing published
OLD_CACHE = os.path.join(BERGAMA_ROOT, "cached", "bergama_archicad", "acbuild.json")   # v1.42: origin from here
ID_PREFIX = "BGA-"                                # v1.44: Element ID of every element AcBuild makes
EDIT_TOL_M = 0.02                                 # v1.44: a 3D box moved more than this = hand-edited (locked)
SURVEY_CACHE = os.path.join(BERGAMA_ROOT, "cached", "bergama_survey", "survey.json")   # v1.44: survey without Rhino
PID = [None]                                      # v1.44: guid of the Element ID property
LOCKED_BB = []                                    # v1.44: (type, plan box) of the hand-edited elements
N_LOCKSKIP = [0]
N_RAFT = [0, 0.0]                                 # v1.44: rafts made, deepest raft below the floor (m)
N_TINONLY = [0]                                   # v1.44: ground tiles filled from the triangulation only
LINK_T = set()                                    # v1.44: targets of the solid element operations made this pass
TYPE_OF = {"CreateSlabs": "Slab", "CreateWalls": "Wall", "CreateMeshes": "Mesh", "CreateColumns": "Column",
           "CreateBeams": "Beam", "CreateRoofs": "Roof", "CreateWindows": "Window", "CreateDoors": "Door"}
ONE_GROUND = True                                 # v1.31: one terrain mesh (no per-cut / river meshes)


RET_MIN_M, RET_T_M, RET_FOOT_M, RET_SEG_M = 0.60, 0.30, 0.50, 4.0   # v1.27: retaining walls (threshold ASSUMED)


FLAT_ROOF_DEG = 2.0   # v1.28: fall of a "flat" roof built with the Roof tool (design intent)
COL_HALL_F, COL_DUP_F = 0.10, 0.50   # v1.28: footprint overlap shares that count as a collision (design rule)


def _overlap_frac(A, B, bxA, n=10):
    """v1.28: share of footprint A (sampled on an n x n grid in its box) that lies inside footprint B"""
    x0, y0, x1, y1 = bxA
    tot = hit = 0
    for i in range(n):
        for j in range(n):
            p = (x0 + (i + 0.5) * (x1 - x0) / n, y0 + (j + 0.5) * (y1 - y0) / n)
            if _inpoly(p, A):
                tot += 1
                hit += _inpoly(p, B)
    return float(hit) / tot if tot else 0.0


def _reg_ops(gs, data):
    """v1.27: remember the slabs made from data (guids gs) as operators that cut the terrain"""
    for g, d in zip(gs, data):
        if g:
            SEO_OPS.append((g, [(q["x"], q["y"]) for q in d.get("polygonCoordinates", [])], d.get("level")))
    return gs


CANOPY_REC = []                                   # per canopy: outline + heights, written to acbuild.json (SectionsAC colours)


def _dp(P, tol):
    """Douglas-Peucker on an open polyline"""
    if len(P) < 3:
        return list(P)
    a, b = P[0], P[-1]
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1e-9
    d = [abs((b[0] - a[0]) * (a[1] - p[1]) - (a[0] - p[0]) * (b[1] - a[1])) / L for p in P]
    i = max(range(1, len(P) - 1), key=lambda j: d[j])
    if d[i] <= tol:
        return [a, b]
    return _dp(P[:i + 1], tol)[:-1] + _dp(P[i:], tol)


def _clip(P, u, t0, t1):
    """polygon P clipped to t0 <= p.u <= t1 (Sutherland-Hodgman, two half-planes)"""
    for sgn, t in ((1.0, t0), (-1.0, -t1)):
        Q = []
        for i in range(len(P)):
            a, b = P[i - 1], P[i]
            fa = sgn * (a[0] * u[0] + a[1] * u[1]) - t
            fb = sgn * (b[0] * u[0] + b[1] * u[1]) - t
            if fa >= 0:
                Q.append(a)
            if (fa >= 0) != (fb >= 0):
                f = fa / (fa - fb)
                Q.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
        P = Q
        if len(P) < 3:
            return []
    return P


def _inpoly(p, P):
    c = False
    for a, b in zip(P, P[1:] + P[:1]):
        if (a[1] > p[1]) != (b[1] > p[1]) and p[0] < a[0] + (b[0] - a[0]) * (p[1] - a[1]) / (b[1] - a[1]):
            c = not c
    return c


def canopy_groups(log):
    """v1.13 (Aras 15 Nov 16:31 UTC "Make canopies top view match with masterplan"): one canopy per FILLED ring of his
    kanopi layer (MasterplanBase cache), the ring itself as the outline (no hull, no merging); his fold lines and
    facet edges inside it (unfilled rings, lines) kept with it: their ends on the outline become fold points.
    Returns [(outline ring, [fold points on the outline])]"""
    mp = os.path.join(BERGAMA_ROOT, "cached", "bergama_masterplanbase", "masterplan.json")
    if not os.path.isfile(mp):
        log.append(u"FLAG canopies: %s missing (press MasterplanBase): no canopies built" % mp)
        return []
    with open(mp, encoding="utf-8") as f:
        J = json.load(f)
    outl, inner = [], []
    for key, pieces in J.get("layers", {}).items():
        if key.split("/")[-1] not in CAN_KEYS:
            continue
        for p in pieces:
            q = [tuple(v) for v in p[4]]
            if p[0] == "r" and p[1] and len(q) >= 3 and abs(area(q)) >= 20.0:
                outl.append(q)
            elif p[0] in ("r", "l") and len(q) >= 2:
                inner.append(q)
    outl.sort(key=lambda R: -abs(area(R)))
    keep = []
    for R in outl:                                         # a filled ring inside a bigger one is a part of it
        if not any(all(_inpoly(v, K) for v in R[::max(1, len(R) // 8)]) for K in keep):
            keep.append(R)
    out = []
    for R in keep:
        H = clean(R[:-1] if R[0] == R[-1] else R)
        if area(H) < 0:
            H = H[::-1]
        folds = []
        for L in inner:
            for v in (L[0], L[-1]) + tuple(L[1:-1]):
                d = min(_seg_d(v, a, b) for a, b in zip(H, H[1:] + H[:1]))
                if d <= 0.6:
                    folds.append(v)
        out.append((H, folds))
    log.append(u"canopies: %d outlines = his filled kanopi rings as drawn (%d inner fold / facet lines)" % (
        len(out), len(inner)))
    return out


def _seg_d(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L2 = dx * dx + dy * dy
    f = 0.0 if L2 < 1e-12 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
    return math.hypot(p[0] - a[0] - f * dx, p[1] - a[1] - f * dy)


def _with_folds(H, folds, tol=0.6):
    """the outline (CCW) simplified to CAN_OUT_TOL, his fold ends inserted as vertices where they meet it"""
    R = _dp(H + [H[0]], CAN_OUT_TOL)[:-1] if len(H) > 4 else list(H)
    for v in folds:
        k = min(range(len(R)), key=lambda i: _seg_d(v, R[i], R[(i + 1) % len(R)]))
        a, b = R[k], R[(k + 1) % len(R)]
        if _seg_d(v, a, b) > tol or min(math.hypot(v[0] - q[0], v[1] - q[1]) for q in (a, b)) < 1.0:
            continue
        dx, dy = b[0] - a[0], b[1] - a[1]
        f = max(0.0, min(1.0, ((v[0] - a[0]) * dx + (v[1] - a[1]) * dy) / (dx * dx + dy * dy)))
        R.insert(k + 1, (a[0] + f * dx, a[1] + f * dy))
    return R


def _ears(R):
    """ear clipping of a simple CCW ring -> triangles (index triples); each step takes the ear with the widest
    smallest angle (no slivers), so a long strip folds across in zigzag triangles"""
    idx = list(range(len(R)))
    tris = []

    def ang(a, b, c):
        u, v = (a[0] - b[0], a[1] - b[1]), (c[0] - b[0], c[1] - b[1])
        n = math.hypot(*u) * math.hypot(*v)
        return math.acos(max(-1.0, min(1.0, (u[0] * v[0] + u[1] * v[1]) / n))) if n > 1e-12 else 0.0
    while len(idx) > 3:
        best = None
        for j in range(len(idx)):
            i0, i1, i2 = idx[j - 1], idx[j], idx[(j + 1) % len(idx)]
            a, b, c = R[i0], R[i1], R[i2]
            if (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) <= 1e-9:
                continue
            if any(_inpoly(R[k], [a, b, c]) for k in idx if k not in (i0, i1, i2)):
                continue
            q = min(ang(c, a, b), ang(a, b, c), ang(b, c, a))
            if best is None or q > best[0]:
                best = (q, j)
        if best is None:
            break
        j = best[1]
        tris.append((idx[j - 1], idx[j], idx[(j + 1) % len(idx)]))
        idx.pop(j)
    if len(idx) == 3:
        tris.append(tuple(idx))
    return tris


CAN_MAX_DEG = 8.0      # v1.26 (Aras 20:06 "dont do these kinda extereme angles keep it minimal"): steepest facet edge, deg (design intent)
CAN_SLAT_SP, CAN_SLAT_W, CAN_SLAT_H = 0.6, 0.05, 0.15   # v1.25: louvre slats every 0.6 m, 50 x 150 mm timber (design intent)


def _facet_roof(P, Z, axis):
    """v1.25: a triangle facet (plan points P, heights Z) as one single-plane Archicad roof: (pivot beg, pivot end,
    pivot height, slope angle rad, uphill unit vector, horizontal unit vector)"""
    (x1, y1), (x2, y2), (x3, y3) = P
    z1, z2, z3 = Z
    det = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
    if abs(det) < 1e-9:
        return None
    a = ((z2 - z1) * (y3 - y1) - (z3 - z1) * (y2 - y1)) / det
    b = ((x2 - x1) * (z3 - z1) - (x3 - x1) * (z2 - z1)) / det
    gl = math.hypot(a, b)
    if gl < 1e-4:                                     # flat facet: a minimal slope along the canopy axis
        gx, gy, ang = axis[0], axis[1], 1e-3
    else:
        gx, gy, ang = a / gl, b / gl, math.atan(gl)
    d = (gy, -gx)                                     # pivot direction: the plane rises on its left (Tapir)
    k = min(range(3), key=lambda i: Z[i])             # the pivot line through the lowest corner
    p0 = P[k]
    return (p0, (p0[0] + d[0] * 10.0, p0[1] + d[1] * 10.0), Z[k], ang, (gx, gy), d)


def _slats(P, Z, fr, sp):
    """v1.25: horizontal louvre slats under a facet: [(plan a, plan b, z)] every sp m (plan) up the slope"""
    p0, _p1, zk, ang, g, d = fr
    up = [(q[0] - p0[0]) * g[0] + (q[1] - p0[1]) * g[1] for q in P]
    out = []
    t = sp / 2.0
    while t < max(up) - 1e-6:
        pts = []
        for i in range(3):
            a, b = P[i], P[(i + 1) % 3]
            ua, ub = up[i], up[(i + 1) % 3]
            if (ua - t) * (ub - t) < 0:
                f = (t - ua) / (ub - ua)
                pts.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
        if len(pts) == 2 and math.hypot(pts[0][0] - pts[1][0], pts[0][1] - pts[1][1]) > 0.3:
            out.append((pts[0], pts[1], zk + t * math.tan(ang)))
        t += sp
    return out


def build_canopies(ac, miss, log, rects, inside, tin, ox, oy, z0, xy, q500_at, wet_at):
    """v1.13 (Aras 15 Nov 16:31-16:32 UTC "Make canopies top view match with masterplan", "Get structrual idea from the
    photo i have sent you and invent from there"): each canopy is built ON his drawn outline, so its top view is the
    masterplan's: the outline (simplified CAN_OUT_TOL m) with his fold ends on it is cut into triangle facets (ear
    clipping, widest angles), the vertices alternate low / high round the outline, so the skin folds across the
    strip like his reference; the structure follows that shape, no fixed bay: a Y steel column under every low
    vertex, CAN_COL_IN m inside the outline (none closer than CAN_COL_MIN m to another; a high vertex farther than
    CAN_COL_MAX m from every column gets one too), its two arms reaching toward the neighbouring outline vertices; the
    timber louvre layer under the same facets; stone plinth + timber deck = the outline cut into bays between the
    columns along the canopy's long axis (stepping with the ground); a glazed room in every other bay where the floor
    is >= Q500 + 0.60 and the room fits inside the outline, a timber planter in the others. Heights: low vertex
    underside >= deck + 2.30 (DfT) and >= Q500 + 0.60 (EA); high vertex + CAN_RISE_M (ASSUMED). Returns the new
    element guids."""
    made = []
    roofs, louvres, trunks, arms, plinths, decks, walls, rooms, planters = [], [], [], [], [], [], [], [], []
    roofs_r, roofs_m, slats = [], [], []                                    # v1.25: Roof-tool facets, Beam-tool louvres
    n_c = 0
    n_dev = []
    for H0, folds in canopy_groups(log):
        if not any(inside(q, r) for q in H0 for r in rects):
            continue
        H = _with_folds(H0, folds)
        if len(H) < 3:
            continue
        n_c += 1
        n_dev.append(max(min(_seg_d(p, a, b) for a, b in zip(H, H[1:] + H[:1])) for p in H0))
        cx, cy = sum(p[0] for p in H) / len(H), sum(p[1] for p in H) / len(H)
        sxx = sum((p[0] - cx) ** 2 for p in H); syy = sum((p[1] - cy) ** 2 for p in H)
        sxy = sum((p[0] - cx) * (p[1] - cy) for p in H)
        ang = 0.5 * math.atan2(2 * sxy, sxx - syy)
        u = (math.cos(ang), math.sin(ang))
        v = (-u[1], u[0])
        T = lambda p: (p[0] - cx) * u[0] + (p[1] - cy) * u[1]
        W = lambda p: (p[0] - cx) * v[0] + (p[1] - cy) * v[1]
        q5 = q500_at(cx, cy)
        gz = [tin.z(p[0] - ox, p[1] - oy) for p in H]
        gs = [g for g in gz if g is not None]
        if not gs:
            log.append(u"canopy %d: no survey ground under it: left out" % n_c)
            continue
        gz = [g if g is not None else min(gs) for g in gz]
        floor0 = lambda g: g + CAN_PLINTH_M + CAN_DECK_M
        low = [max(floor0(g) + CAN_CLEAR_M, (q5 + CAN_Q500_M) if q5 is not None else -1e9) + CAN_LOUVRE_M + CAN_T
               for g in gz]                                    # skin top at a low vertex
        hi_ = [k % 2 == 1 for k in range(len(H))]
        if len(H) % 2 == 1:
            hi_[-1] = False                                    # odd count: two low vertices meet at the start
        zv = [low[k] + (CAN_RISE_M if hi_[k] else 0.0) for k in range(len(H))]
        tris = list(_ears(H))
        tmax = math.tan(math.radians(CAN_MAX_DEG))      # v1.26 (Aras 20:06 "keep it minimal"): no facet edge steeper
        for _it in range(60):                           # than CAN_MAX_DEG; only raised, so every clearance holds
            ch = False
            for t3 in tris:
                for i_, j_ in ((t3[0], t3[1]), (t3[1], t3[2]), (t3[2], t3[0])):
                    dd = math.hypot(H[i_][0] - H[j_][0], H[i_][1] - H[j_][1]) * tmax
                    for a_, b_ in ((i_, j_), (j_, i_)):
                        if zv[a_] < zv[b_] - dd - 1e-4:
                            zv[a_] = zv[b_] - dd
                            ch = True
            if not ch:
                break
        CANOPY_REC.append(dict(ring=[[round(p[0], 2), round(p[1], 2)] for p in H0], ground=round(min(gs), 3),
                               floor=round(min(floor0(g) for g in gz), 3),
                               under=round(min(low) - CAN_T - CAN_LOUVRE_M, 3), top=round(max(zv), 3)))
        for t3 in tris:
            P3 = [H[k] for k in t3]
            if abs(area(P3)) < 0.3:
                continue
            roofs.append(dict(level=0.0, polygonCoordinates=[dict(xy(H[k]), z=round(zv[k] - z0, 3)) for k in t3]))
            louvres.append(dict(level=0.0, polygonCoordinates=[dict(xy(H[k]), z=round(zv[k] - z0 - CAN_T - CAN_LOUVRE_M, 3))
                                                               for k in t3]))
            fr = _facet_roof(P3, [zv[k] - CAN_T for k in t3], u)   # v1.25: roof underside = skin top - CAN_T
            if fr:
                roofs_r.append(dict(level=round(fr[2] - z0, 3), thickness=CAN_T, structureType="Basic",
                                    polygonCoordinates=[xy(q) for q in P3],
                                    pivotLine=dict(begCoordinate=xy(fr[0]), endCoordinate=xy(fr[1])),
                                    angle=round(fr[3], 5)))
                roofs_m.append(roofs[-1])
                for a_, b_, zs_ in _slats(P3, [zv[k] - CAN_T for k in t3], fr, CAN_SLAT_SP):
                    slats.append(dict(begCoordinate=xy(a_), endCoordinate=xy(b_),
                                      zCoordinate=round(zs_ - CAN_LOUVRE_M + CAN_SLAT_H - z0, 3),
                                      width=CAN_SLAT_W, height=CAN_SLAT_H))
        # Y columns: under the low vertices, pulled inside; then under high vertices left too far from any column
        cols = []

        def pull_in(k):
            a, b, c = H[k - 1], H[k], H[(k + 1) % len(H)]
            n1 = (-(b[1] - a[1]), b[0] - a[0]); n2 = (-(c[1] - b[1]), c[0] - b[0])   # inward normals (CCW ring)
            l1, l2 = math.hypot(*n1) or 1.0, math.hypot(*n2) or 1.0
            d = (n1[0] / l1 + n2[0] / l2, n1[1] / l1 + n2[1] / l2)
            ld = math.hypot(*d)
            if ld < 1e-6:
                return None
            p = (b[0] + d[0] / ld * CAN_COL_IN, b[1] + d[1] / ld * CAN_COL_IN)
            return p if _inpoly(p, H) else None
        for want_hi in (False, True):
            for k in range(len(H)):
                if hi_[k] != want_hi:
                    continue
                p = pull_in(k)
                if p is None:
                    continue
                dmin = min([math.hypot(p[0] - c[1][0], p[1] - c[1][1]) for c in cols] or [1e9])
                if (not want_hi and dmin >= CAN_COL_MIN) or (want_hi and dmin > CAN_COL_MAX):
                    cols.append((k, p))
        for k, base in cols:
            g = tin.z(base[0] - ox, base[1] - oy)
            g = gz[k] if g is None else g
            fl = floor0(g)
            under = zv[k] - CAN_T - CAN_LOUVRE_M
            hgt = under - fl
            if hgt < 1.0:
                continue
            fork = fl + CAN_Y_FORK * hgt
            trunks.append(dict(coordinates=dict(xy(base), z=round(fl - z0, 3)), height=round(fork - fl, 3),
                               circleBased=True, width=0.30))
            for nb_ in (H[k - 1], H[(k + 1) % len(H)]):        # arms toward the two neighbouring vertices
                dx, dy = nb_[0] - base[0], nb_[1] - base[1]
                L = math.hypot(dx, dy)
                if L < 0.5:
                    continue
                r_ = min(CAN_Y_ARM_M, 0.45 * L)
                end = (base[0] + dx / L * r_, base[1] + dy / L * r_)
                zz = under - 0.05
                arms.append(dict(begCoordinate=xy(base), endCoordinate=xy(end), zCoordinate=round(fork - z0, 3),
                                 slantAngle=round(math.atan2(zz - fork, r_), 4), width=0.22, height=0.22))
        # bays between the columns along the long axis: plinth + deck = the outline cut there
        ts = sorted(T(p) for _k, p in cols)
        cuts = []
        for t in ts:
            if not cuts or t - cuts[-1] >= 3.0:
                cuts.append(t)
        ta, tb = min(T(p) for p in H), max(T(p) for p in H)
        edges = [ta - 1.0] + [t for t in cuts if ta + 2.0 < t < tb - 2.0] + [tb + 1.0]
        HT = [(T(p), W(p)) for p in H]
        for b_ in range(len(edges) - 1):
            poly = _clip(HT, (1.0, 0.0), edges[b_], edges[b_ + 1])
            if len(poly) < 3:
                continue
            ring = [(cx + u[0] * t_ + v[0] * w_, cy + u[1] * t_ + v[1] * w_) for t_, w_ in poly]
            if area(ring) < 0:
                ring = ring[::-1]
            bx, by = sum(p[0] for p in ring) / len(ring), sum(p[1] for p in ring) / len(ring)
            gb = [tin.z(p[0] - ox, p[1] - oy) for p in ring]
            g = max([x for x in gb if x is not None] or gs)
            if wet_at(bx, by, g):
                continue                                       # in the water: no deck (Sections: plinth only where dry)
            pc = [xy(p) for p in clean(ring)]
            if len(pc) < 3:
                continue
            plinths.append(dict(level=round(g + CAN_PLINTH_M - z0, 3), thickness=CAN_PLINTH_M + 0.5, polygonCoordinates=pc))
            decks.append(dict(level=round(g + CAN_PLINTH_M + CAN_DECK_M - z0, 3), thickness=CAN_DECK_M, polygonCoordinates=pc))
            fl = floor0(g)
            t0_, t1_ = max(edges[b_], ta), min(edges[b_ + 1], tb)
            tm, wm = T((bx, by)), W((bx, by))
            P_ = lambda t, w: (cx + u[0] * t + v[0] * w, cy + u[1] * t + v[1] * w)
            hw = 0.0
            for s_ in (2.0, 1.6, 1.2, 0.8):                    # the widest room / planter that fits inside
                C4 = [P_(tm - 0.3 * (t1_ - t0_), wm - s_), P_(tm + 0.3 * (t1_ - t0_), wm - s_),
                      P_(tm + 0.3 * (t1_ - t0_), wm + s_), P_(tm - 0.3 * (t1_ - t0_), wm + s_)]
                if all(_inpoly(c, H) for c in C4):
                    hw = s_
                    break
            under_b = min(zv) - CAN_T - CAN_LOUVRE_M - 0.05
            if b_ % 2 == 0 and q5 is not None and fl >= q5 + CAN_Q500_M and t1_ - t0_ > 4.0 and hw >= 1.6:
                for a, c in zip(C4, C4[1:] + C4[:1]):          # glazed room: every other bay, above Q500 + 0.60
                    walls.append(dict(begCoordinate=xy(a), endCoordinate=xy(c), zCoordinate=round(fl - z0, 3),
                                      height=round(under_b - fl, 3), thickness=0.08, referenceLineLocation="Center"))
                    rooms.append((math.hypot(c[0] - a[0], c[1] - a[1]), under_b - fl))
            elif hw >= 0.8:                                    # timber planter in the open bay
                L_p = min(CAN_PLANTER_M, 0.4 * (t1_ - t0_))
                C4 = [P_(tm - L_p / 2, wm - 0.5), P_(tm + L_p / 2, wm - 0.5), P_(tm + L_p / 2, wm + 0.5), P_(tm - L_p / 2, wm + 0.5)]
                if all(_inpoly(c, H) for c in C4):
                    planters.append(dict(level=round(fl + 0.6 - z0, 3), thickness=0.6, polygonCoordinates=[xy(p) for p in C4]))
    if n_dev:
        log.append(u"canopy top view = his kanopi outlines: %d canopies, the built outline is at most %.2f m off his "
                   u"drawn line (simplified to %.2f m)" % (len(n_dev), max(n_dev), CAN_OUT_TOL))
    if not n_c:
        log.append(u"canopies: none inside the cut rectangles")
        return made
    # ---- to Archicad (each kind on its own, a refusal is logged and the rest goes on)
    # v1.25 (Aras 15 Nov 20:05 "draw their roofs with roof tool columns with column tool, beams with beam tool"):
    # each facet a single-plane Roof, the louvres timber Beams; meshes only where Archicad refuses a roof
    rg = ac.create("CreateRoofs", "roofsData", roofs_r, u"canopy roof facets (Roof tool, single-plane)") \
        if roofs_r and "CreateRoofs" not in miss else []
    made += [g for g in rg if g]
    bad = ([m for m, g in zip(roofs_m, rg) if not g] if rg else list(roofs_m)) + [m for m in roofs if m not in roofs_m]
    if bad and "CreateMeshes" not in miss:
        made += [g for g in ac.create("CreateMeshes", "meshesData", [dict(m, skirtType="SurfaceOnlyWithoutSkirt",
                                                                         skirtLevel=CAN_T) for m in bad],
                                      u"canopy facets Archicad refused as roofs (meshes instead)") if g]
        log.append(u"FLAG %d canopy facet(s) refused as roofs: built as meshes" % len(bad))
    try:
        made += [g for g in ac.create("CreateBeams", "beamsData", slats, u"canopy timber louvres (Beam tool)") if g]
    except Exception as ex:
        log.append(u"FLAG canopy louvres not made (%s)" % ex)
    if "CreateSlabs" not in miss:
        made += [g for g in _reg_ops(ac.create("CreateSlabs", "slabsData", plinths, u"canopy stone plinths"), plinths) if g]
        made += [g for g in ac.create("CreateSlabs", "slabsData", decks, u"canopy timber decks") if g]
        made += [g for g in ac.create("CreateSlabs", "slabsData", planters, u"canopy planters") if g]
    try:
        made += [g for g in ac.create("CreateColumns", "columnsData", trunks, u"canopy Y column trunks") if g]
    except Exception as ex:
        log.append(u"FLAG canopy columns not made (%s)" % ex)
    try:
        made += [g for g in ac.create("CreateBeams", "beamsData", arms, u"canopy Y column arms") if g]
    except Exception as ex:
        log.append(u"FLAG canopy column arms not made (%s)" % ex)
    if "CreateWalls" not in miss and walls:
        wg = ac.create("CreateWalls", "wallsData", walls, u"canopy glazed rooms (walls)")
        made += [g for g in wg if g]
        wins = []
        for g, (ln, h) in zip(wg, rooms):
            if not g or ln < CAN_GLASS_W + 0.4:
                continue
            nw = max(1, int((ln - 0.2) // CAN_GLASS_STEP))
            x0 = (ln - (nw - 1) * CAN_GLASS_STEP) / 2.0
            wins += [dict(ownerWallId={"guid": g}, width=CAN_GLASS_W, height=round(h - 0.25, 2), sillHeight=0.1,
                          centerOffset=round(x0 + j * CAN_GLASS_STEP, 2)) for j in range(nw)]
        if wins and "CreateWindows" not in miss:
            made += [g for g in ac.create("CreateWindows", "windowsData", wins, u"canopy glazing") if g]
    log.append(u"canopies built: %d (%d facets, %d Y columns, %d deck bays, %d glazed rooms, %d planters); valley "
               u"underside >= deck + %.2f m (DfT) and >= Q500 + %.2f m (EA), ridge + %.1f m ASSUMED; bay %.0f m (0 = by shape), "
               u"plinth %.2f m, deck %.2f m (design intent)" % (n_c, len(roofs), len(trunks), len(decks),
                                                                 len(walls) // 4, len(planters), CAN_CLEAR_M,
                                                                 CAN_Q500_M, CAN_RISE_M, CAN_BAY_M, CAN_PLINTH_M,
                                                                 CAN_DECK_M))
    return made


# ================================================================ v1.14: the node buildings (Aras 15 Nov 17:24 UTC
# "any drawing that has building in it you should use the drawing that comes out of archicad")
NB_FILE = os.path.join(BERGAMA_ROOT, "cached", "bergama_perspectives", "buildings.json")   # placement: Perspectives
NC_FILE = os.path.join(BERGAMA_ROOT, "Data", "bergama_nodes_common.py")                     # rooms: nodes common BUILD
NB_WALL_M, NB_PART_M, NB_SLAB_M = 0.30, 0.12, 0.30   # wall, partition, slab thickness (design intent)
NB_GLASS_SILL_M, NB_GLASS_HEAD_M = 0.10, 0.50        # glazed bays: sill above the floor, head below the next floor
NB_REG_IN, NB_REG_H, NB_REG_DZ = 0.5, 1.0, 3.0   # building-view registration blocks: centre in from the ends, height, above REG_Z
NB_PREG_M, NB_PREG_A = 6.0, (1.0, 0.5)              # v1.17: plan registration squares: m off the corners, sides (m)
NB_STORY_MIN = 0.5                                   # v1.17: m, a story this close above the one below is merged into it
NB_GAP_M = 3.0                                       # m: section / elevation lines start this far outside the building


def node_buildings(log):
    """the node buildings as the Perspectives script placed them (cached/bergama_perspectives/buildings.json: foot,
    centre, long axis u, cross axis w, L, D, bays, floors, storey, plinth, rise, ground, canopy) with their rooms from
    nodes common BUILD (read live). [] + FLAG when the placement is missing"""
    if not os.path.isfile(NB_FILE):
        log.append(u"FLAG node buildings: %s missing (press Perspectives first): no node buildings, no building views"
                   % NB_FILE)
        return []
    with open(NB_FILE, encoding="utf-8") as f:
        J = json.load(f).get("buildings") or {}
    NC = {"__name__": "bergama_nodes_common"}
    try:
        with open(NC_FILE, encoding="utf-8") as f:
            exec(compile(f.read(), NC_FILE, "exec"), NC)
    except Exception as ex:
        log.append(u"FLAG nodes common not read (%s): node buildings without rooms" % ex)
    BUILD = NC.get("BUILD") or {}
    out = []
    for nd in sorted(J):
        b = dict(J[nd], node=nd)
        b["floors"] = (BUILD.get(nd) or {}).get("floors") or []
        out.append(b)
    log.append(u"node buildings: %d placed by Perspectives (%s), rooms from nodes common %s" % (
        len(out), u", ".join(b["node"] for b in out), NC.get("NC_VERSION")))
    return out


def node_secs(NB):
    """per node building: <N>-BX = a cut across its depth at the middle looking along it, <N>-BE = its long
    elevation (a section line outside the long side looking at it): [(name, A, B, depth)]"""
    out = []
    for b in NB:
        c, u, w, L, D = b["c"], b["u"], b["w"], b["L"], b["D"]
        P = lambda t, s: (c[0] + u[0] * t + w[0] * s, c[1] + u[1] * t + w[1] * s)

        def look(A, B, want):                              # the order whose Archicad view side (+n) faces want
            _L, _u, n = frame(A, B)
            return (A, B) if n[0] * want[0] + n[1] * want[1] > 0 else (B, A)
        A, B = look(P(0.0, -D / 2 - NB_GAP_M), P(0.0, D / 2 + NB_GAP_M), u)
        out.append((u"%s-BX" % b["node"], A, B, round(L / 2.0 + NB_GAP_M, 2)))
        A, B = look(P(-L / 2 - NB_GAP_M, -D / 2 - NB_GAP_M), P(L / 2 + NB_GAP_M, -D / 2 - NB_GAP_M), w)
        out.append((u"%s-BE" % b["node"], A, B, round(D + 2 * NB_GAP_M, 2)))
    return out


def node_stories(NB, z0):
    """v1.17: one story per floor of every node building (level = its floor, as the elements are given) and its plan
    view: [(story name, level, node, floor j, view name)], sorted by level"""
    out = []
    for b in NB:
        zp = b["ground"] + b["plinth"]
        for j in range(1 if b.get("canopy") else max(1, int(b["nf"]))):
            out.append((u"%s floor %d" % (b["node"], j), round(zp + j * b["storey"] - z0, 3), b["node"], j,
                        u"%s-P%d" % (b["node"], j)))
    return sorted(out, key=lambda r: r[1])


def set_stories(ac, log, z0, ST):
    """v1.17: the project's stories = story 0 (kept) + the node building floors (merged when closer than
    NB_STORY_MIN); returns the plan views whose floor has its own story [(view, story name, level, node, j)]"""
    if not ST:
        return []
    if not ac.has("SetStories"):
        log.append(u"FLAG building floor plans: Tapir has no SetStories: plans drawn by the node scripts")
        return []
    st = (ac.t("GetStories").get("stories") or [])
    s0 = next((s_ for s_ in st if s_.get("index") == 0), None)
    keep = [dict(name=(s0 or {}).get("name") or u"Ground Floor", level=z0, dispOnSections=False)]
    views, last = [], z0
    for nm, lv, nd, j, vn in ST:
        if lv <= z0 + NB_STORY_MIN:
            log.append(u"FLAG %s at %+.2f m is not above story 0 (%+.2f m): no Archicad plan for it" % (nm, lv, z0))
            continue
        if lv - last >= NB_STORY_MIN:
            keep.append(dict(name=nm, level=lv, dispOnSections=False))
            last = lv
        views.append((vn, keep[-1]["name"], keep[-1]["level"], nd, j))
    r = ac.t("SetStories", {"stories": keep})
    if isinstance(r, dict) and r.get("success") is False:
        log.append(u"FLAG stories not set (%s): plans drawn by the node scripts" % json.dumps(r)[:160])
        return []
    log.append(u"stories: story 0 + %d node building floor(s) (%s), level lines off in the sections" % (
        len(keep) - 1, u", ".join(u"%s %+.2f" % (k["name"], k["level"]) for k in keep[1:])))
    return views


NB_ROOF_T = 0.25                                     # v1.43: m, node roof facet thickness (the old mesh skirt)


def build_nodes(ac, miss, log, xy, z0, NB):
    """the node buildings in Archicad (DESIGN, as the node slides and the perspectives): stone plinth, floor slabs,
    walls bay by bay (glazed every other bay, a window per storey), room partitions by area along the length, folded
    roof facets (meshes, as the canopies); N4 = the raised canopy platform (deck on columns, folded roof)"""
    made, plin, slabs, walls, glz, parts, facets, cols = [], [], [], [], [], [], [], []
    ffr = []                                          # v1.43: (plan points, heights) per facet, for the Roof tool
    for b in NB:
        c, u, w, L, D = b["c"], b["u"], b["w"], b["L"], b["D"]
        nb, nf, hs, PL, RISE = int(b["nb"]), max(1, int(b["nf"])), b["storey"], b["plinth"], b["rise"]
        P = lambda t, s: (c[0] + u[0] * t + w[0] * s, c[1] + u[1] * t + w[1] * s)
        zp = b["ground"] + PL
        foot = [P(-L / 2, -D / 2), P(L / 2, -D / 2), P(L / 2, D / 2), P(-L / 2, D / 2)]
        plin.append(dict(level=round(zp - z0, 3), thickness=round(PL + 0.5, 3), polygonCoordinates=[xy(q) for q in foot]))
        if b.get("canopy"):
            top = zp + hs
            slabs.append(dict(level=round(top - z0, 3), thickness=NB_SLAB_M, polygonCoordinates=[xy(q) for q in foot]))
            for k in range(nb + 1):
                for s in (-D / 2 + 0.4, D / 2 - 0.4):
                    q = P(-L / 2 + k * L / nb, s)
                    cols.append(dict(coordinates=dict(xy(q), z=round(zp - z0, 3)), height=round(top - NB_SLAB_M - zp, 3),
                                     circleBased=True, width=0.30))
                    cols.append(dict(coordinates=dict(xy(q), z=round(top - z0, 3)), height=2.3, circleBased=True,
                                     width=0.24))
            rz = top + 2.3
        else:
            top = zp + nf * hs
            for j in range(1, nf + 1):
                slabs.append(dict(level=round(zp + j * hs - z0, 3), thickness=NB_SLAB_M,
                                  polygonCoordinates=[xy(q) for q in foot]))
            for k in range(nb):
                t0_, t1_ = -L / 2 + k * L / nb, -L / 2 + (k + 1) * L / nb
                for s in (-D / 2, D / 2):
                    walls.append((dict(begCoordinate=xy(P(t0_, s)), endCoordinate=xy(P(t1_, s)),
                                       zCoordinate=round(zp - z0, 3), height=round(nf * hs, 3), thickness=NB_WALL_M,
                                       referenceLineLocation="Center"), (t1_ - t0_, nf, hs) if k % 2 else None))
            for t_ in (-L / 2, L / 2):
                walls.append((dict(begCoordinate=xy(P(t_, -D / 2)), endCoordinate=xy(P(t_, D / 2)),
                                   zCoordinate=round(zp - z0, 3), height=round(nf * hs, 3), thickness=NB_WALL_M,
                                   referenceLineLocation="Center"), None))
            for j, fl in enumerate(b.get("floors") or []):
                t_ = -L / 2
                for _n, a_ in fl[:-1]:
                    t_ += a_ / D
                    if t_ < L / 2 - 0.5:
                        parts.append(dict(begCoordinate=xy(P(t_, -D / 2)), endCoordinate=xy(P(t_, D / 2)),
                                          zCoordinate=round(zp + j * hs - z0, 3), height=round(hs - NB_SLAB_M, 3),
                                          thickness=NB_PART_M, referenceLineLocation="Center"))
            rz = top
        ax = [(-L / 2 + L * kk / (2.0 * nb), rz + (RISE if kk % 2 else 0.0)) for kk in range(2 * nb + 1)]
        for kk in range(2 * nb):                          # folded roof: valleys at bay ends, ridges at bay middles
            (ta, za), (tb, zb) = ax[kk], ax[kk + 1]
            for s in (-D / 2, D / 2):
                pa, pb, ma, mb = P(ta, s), P(tb, s), P(ta, 0.0), P(tb, 0.0)
                ffr.append(([pa, pb, mb], [rz, rz, zb]))      # v1.43: for the Roof tool
                ffr.append(([pa, mb, ma], [rz, zb, za]))
                facets.append(dict(level=0.0, polygonCoordinates=[dict(xy(pa), z=round(rz - z0, 3)),
                                                                   dict(xy(pb), z=round(rz - z0, 3)),
                                                                   dict(xy(mb), z=round(zb - z0, 3))]))
                facets.append(dict(level=0.0, polygonCoordinates=[dict(xy(pa), z=round(rz - z0, 3)),
                                                                   dict(xy(mb), z=round(zb - z0, 3)),
                                                                   dict(xy(ma), z=round(za - z0, 3))]))
    if not NB:
        return made
    if "CreateSlabs" not in miss:
        made += [g for g in _reg_ops(ac.create("CreateSlabs", "slabsData", plin, u"node buildings: stone plinths"), plin) if g]
        made += [g for g in ac.create("CreateSlabs", "slabsData", slabs, u"node buildings: floor and roof slabs") if g]
    if "CreateWalls" not in miss and walls:
        wg = ac.create("CreateWalls", "wallsData", [w_ for w_, _g in walls], u"node buildings: walls")
        made += [g for g in wg if g]
        wins = []
        for g, (_w, gl) in zip(wg, walls):
            if not g or not gl:
                continue
            ln, nf_, hs_ = gl
            wins += [dict(ownerWallId={"guid": g}, width=round(max(1.0, ln - 0.8), 2),
                          height=round(hs_ - NB_GLASS_SILL_M - NB_GLASS_HEAD_M, 2),
                          sillHeight=round(j * hs_ + NB_GLASS_SILL_M, 2), centerOffset=round(ln / 2.0, 2))
                     for j in range(nf_)]
        if wins and "CreateWindows" not in miss:
            made += [g for g in ac.create("CreateWindows", "windowsData", wins, u"node buildings: glazed bays") if g]
        if parts:
            made += [g for g in ac.create("CreateWalls", "wallsData", parts, u"node buildings: room partitions") if g]
    try:
        if cols:
            made += [g for g in ac.create("CreateColumns", "columnsData", cols, u"node N4 platform columns") if g]
    except Exception as ex:
        log.append(u"FLAG N4 platform columns not made (%s)" % ex)
    if facets and "CreateRoofs" not in miss:          # v1.43: Roof tool, one single-plane roof per facet
        rr_, mm_ = [], []
        for (P3, Z3), m_ in zip(ffr, facets):
            fr = _facet_roof(P3, [z_ - NB_ROOF_T for z_ in Z3], (1.0, 0.0))
            if fr and abs(area(P3)) >= 0.05:
                rr_.append(dict(level=round(fr[2] - z0, 3), thickness=NB_ROOF_T, structureType="Basic",
                                polygonCoordinates=[xy(q) for q in P3],
                                pivotLine=dict(begCoordinate=xy(fr[0]), endCoordinate=xy(fr[1])), angle=round(fr[3], 5)))
                mm_.append(m_)
        rg_ = ac.create("CreateRoofs", "roofsData", rr_, u"node buildings: folded roof facets (Roof tool, single-plane)") \
            if rr_ else []
        made += [g for g in rg_ if g]
        facets = [m_ for m_, g in zip(mm_, rg_) if not g] + [m_ for m_ in facets if m_ not in mm_]
        if facets:
            log.append(u"FLAG %d node roof facet(s) refused as roofs: built as meshes" % len(facets))
    if "CreateMeshes" not in miss and facets:
        ok = False
        for st in ("SurfaceOnlyWithoutSkirt", "SurfaceOnly", "SolidBodyWithSkirt"):
            g = ac.create("CreateMeshes", "meshesData", [dict(facets[0], skirtType=st, skirtLevel=0.25)],
                          u"node roof facet test (%s)" % st)
            if g and g[0]:
                made += g
                made += [g_ for g_ in ac.create("CreateMeshes", "meshesData",
                                                [dict(m, skirtType=st, skirtLevel=0.25) for m in facets[1:]],
                                                u"node buildings: folded roof facets") if g_]
                ok = True
                break
        if not ok:
            log.append(u"FLAG node roof facets refused by Archicad (meshes): flat roof slabs only")
    log.append(u"node buildings built (DESIGN): %s; %d plinths, %d slabs, %d walls, %d partitions, %d roof facets, "
               u"%d columns" % (u", ".join(u"%s %.0fx%.0f m" % (b["node"], b["L"], b["D"]) for b in NB), len(plin),
                                len(slabs), len(walls), len(parts), len(facets), len(cols)))
    return made


# ================================================================ v1.16: his masterplan in Archicad (Aras 15 Nov 17:32
# UTC "make sure archicad drawing is %100 pinpoint accurate to our masterplan"): every master.svg piece inside the
# working area as an Archicad slab on his own points (MasterplanBase cache, survey m), then read back and measured
MP_FILE = os.path.join(BERGAMA_ROOT, "cached", "bergama_masterplanbase", "masterplan.json")
WA_FILE = os.path.join(BERGAMA_ROOT, "cached", "bergama_basemap", "basemap_layers.json")   # calisma = working area
# his layer -> (slab thickness m, top above the ground m): DESIGN values for the model, the outline is his
MP_SLABS = {"teras": (0.40, 0.0), "begum_su_merdiven": (0.40, 0.0), "iskele_kenari": (0.25, 0.0),
            "normal": (0.15, 0.0), "path": (0.15, 0.0), "yeni": (0.10, 0.0), "yol_kenar": (0.15, 0.0),
            "kopruler": (0.50, 0.0), "istinaat": (0.40, 1.0), "kesin_yesil": (0.05, 0.0), "belki_yesil": (0.05, 0.0),
            "su_bitkii": (0.05, 0.0), "su": (0.05, 0.0), "ana_su": (0.05, 0.0),
            "begum_yesil": (0.05, 0.0), "Layer_49": (0.05, 0.0), "master": (0.05, 0.0), "bina_cerceve": (0.15, 0.0),
            "circulation": (0.15, 0.0), "rock": (0.30, 0.0)}   # v1.29: his other painted layers; rock = boulders (build_selinos)
MP_SKIP = ("kanopi", "teras_-_canopy", "desings", "existing_buildings", "builts2", "existing_roads", "heritage",
           "kizil_avlu", "PLANTING_v13_1")        # canopies + node buildings built above; context and trees not his
MP_TOL_M = 0.05                                    # FLAG a piece whose Archicad outline is further off than this
MP_MAX_M2 = 100000.0                               # his sheet / picture frames (pages common PC_MP_MAX_M2 order)
SITE_REC = []                                      # (guid, layer, ring) for the read-back


# ================================================================ v1.29 the whole Selinos (Aras 15 Nov 20:14-20:15 "build
# the selinos with everything in archicad like river bed, reed bed and everything like not a single beat skipped",
# "bridges and etc.")
WATER_CELL_M = 5.0          # m: the water surface is built in cells this size, each at the level interpolated along the river
REED_H_M = 1.5              # m: reed height above the water (or the ground where dry): ASSUMED, no source
ROCK_MIN_M2 = 1.0           # m2: his stone / rock pieces from this size are boulders; smaller ones are drawn texture
ROCK_H_MAX = 0.8            # m: boulder height = half the square root of its area, at most this: ASSUMED
TREE_SP = {"trees_plane": (18.0, 0.30, 0.50), "trees_ash": (15.0, 0.35, 0.40),        # (height m, crown bottom as a share
           "trees_stone_pine": (14.0, 0.60, 0.40), "trees_rosemary": (1.0, 0.0, 0.0)}  # of the height, trunk m): ASSUMED
HIST_BRIDGES = (                                     # survey bridge (pair of deck edge lines) nearest to the point
    (u"Ulucami bridge (Roman)", (29846.0, 32277.0), 2,
     u"2 arches ASSUMED: the survey length fits the 'Selinus bridge, 2 x 11.4 m' row of Wikipedia's "
     u"List of Roman bridges, but that row is not confirmed to be this bridge"),
    (u"Üç Kemer bridge", (30294.0, 31792.0), 3, u"3 arches from its name ('three arches')"))
BR_PIER_M = 1.5             # m: pier thickness between arches: ASSUMED
BR_DECK_M = 0.8             # m: deck + fill over the arch crown: ASSUMED
BR_SEG = 12                 # slabs per arch (the arch soffit in steps)
BR_SPAN_MAX = 25.0          # m: a new bridge longer than this gets piers at most this far apart: ASSUMED
BR_NEW_PIER_M = 1.0         # m: new bridge pier thickness: ASSUMED
BANK_WALL_T = 0.40          # m: bank wall (istinaat) thickness (his MP_SLABS value)
BANK_WALL_UP = 1.0          # m: bank wall top above the higher side where the two sides are level (MP_SLABS value)
SEL = {}                    # raw pieces kept by site_pieces for build_selinos
AUDIT = {}                  # layer -> [pieces, taken, status]
RIVER_MESH, WATER_OPS = [], []   # (guid, ring survey m); (guid, polygon Archicad m) water slabs cut by the ground


def _pip_fast(H, cell=5.0):
    """v1.29: point-in-polygon for a big ring: its edges bucketed in rows of cell m (ray to +x)"""
    y0 = min(q[1] for q in H)
    rows = {}
    for i in range(len(H)):
        a, b = H[i - 1], H[i]
        for r in range(int((min(a[1], b[1]) - y0) // cell), int((max(a[1], b[1]) - y0) // cell) + 1):
            rows.setdefault(r, []).append((a, b))

    def f(p):
        x, y = p[0], p[1]
        c = False
        for a, b in rows.get(int((y - y0) // cell), ()):
            if (a[1] > y) != (b[1] > y) and x < (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]) + a[0]:
                c = not c
        return c
    return f


def _audit_status(key):
    parts = key.split("/")
    for w, s in ((u"assets", u"not built: people, cars and pictures for the plan"),
                 (u"PLANTING_v13_1", u"built: trees (trunk + crown)"),
                 (u"agaclar-2", u"not built: drawn tree texture (the trees come from PLANTING_v13_1)"),
                 (u"Doldurma_renk", u"not built: fill colour texture"),
                 (u"existing_roads", u"not built: roads come from the survey (MapBase)"),
                 (u"existing_buildings", u"built from the MapBase survey footprints, not from this layer"),
                 (u"building_shadow", u"not built: drawn shadows"),
                 (u"builts2", u"built from the MapBase survey footprints, not from this layer"),
                 (u"Kizil_Avlu_outline_popped_the_reason_for_the_red_area", u"built: Kızıl Avlu hall walls"),
                 (u"heritage1", u"built from the MapBase survey footprints (historic red)"),
                 (u"kizil_avlu", u"built: Kızıl Avlu hall walls"),
                 (u"kanopi", u"built: canopies"), (u"desings", u"built: node buildings"),
                 (u"su_outline", u"built: river bed mesh + water at the section season's level"),
                 (u"ana_su", u"built: the same outline as su_outline (river bed + water)"),
                 (u"duzenlenmis", u"built: its filled ring as a 5 cm channel slab; its pictures are texture"),
                 (u"yosun", u"built: reed masses"), (u"bitki2", u"not built: one symbol, no outline"),
                 (u"tas", u"built: pieces of 1 m2 and more as boulders, smaller ones are texture"),
                 (u"kaya", u"built: pieces of 1 m2 and more as boulders, smaller ones are texture"),
                 (u"istinaat", u"built: bank walls along his lines"),
                 (u"png-2", u"not built: texture picture (its outline is built)"),
                 (u"png", u"not built: texture picture (its outline is built)"),
                 (u"begum_su_merdiven", u"built: seating tiers"),
                 (u"kopruler", u"built: bridge decks (+ arches or piers)")):
        if w in parts:
            return s
    return None


def _water_level_fn(rects, CJ, rings, log):
    """v1.29: water level along the river: one station per section line with levels (where the line crosses his river
    outline), the level of that section's own season (lowest flow of it), linear between stations"""
    st = []
    PIPS = [_pip_fast(R) for R in rings]
    for name, A, B, Ln, u, n in rects:
        c = CJ.get(name) or {}
        lv = c.get("levels") or {}
        ks = sorted(k for k in lv if k.startswith((c.get("season") or u"") + u"|"))
        if not ks or not rings:
            continue
        k = min(ks, key=lambda k_: float(k_.split(u"|")[1]))
        if not lv[k] or lv[k][0] is None:
            continue
        P = [(A[0] + u[0] * s, A[1] + u[1] * s) for s in [i * 1.0 for i in range(int(Ln) + 1)]]
        P = [p for p in P if any(f_(p) for f_ in PIPS)]
        if P:
            st.append(((sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P)), float(lv[k][0]), name, k))
    allr = [q for R in rings for q in R]
    if allr:                                               # stations in order down the river: along the line from its
        a_ = max(allr, key=lambda q: q[1] - q[0])          # north-west end to its south-east end (the Selinos runs NW-SE)
        b_ = max(allr, key=lambda q: q[0] - q[1])
        st.sort(key=lambda s_: (s_[0][0] - a_[0]) * (b_[0] - a_[0]) + (s_[0][1] - a_[1]) * (b_[1] - a_[1]))
    if st:
        log.append(u"water levels down the river (Sections cache, each line's own season, lowest flow): %s" % u", ".join(
            u"%s %s %.2f m" % (s_[2], s_[3], s_[1]) for s_ in st))
        up = [(p_[2], q_[2]) for p_, q_ in zip(st, st[1:]) if q_[1] > p_[1] + 0.05]
        if up:
            log.append(u"FLAG water: the Sections level rises downstream between %s (each line's level comes from its own "
                       u"bed): the water steps up there" % u", ".join(u"%s-%s" % x for x in up))
    else:
        log.append(u"FLAG water: no section line with levels crosses the river outline: no water built")

    def wl(x, y):
        if not st:
            return None
        if len(st) == 1:
            return st[0][1]
        best = None
        for (a, la, _n, _k), (b, lb, _n2, _k2) in zip(st, st[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L2 = dx * dx + dy * dy or 1e-9
            t = max(0.0, min(1.0, ((x - a[0]) * dx + (y - a[1]) * dy) / L2))
            d = math.hypot(x - a[0] - t * dx, y - a[1] - t * dy)
            if best is None or d < best[0]:
                best = (d, la + (lb - la) * t)
        return best[1]
    return wl


def _bridge_frames(log):
    """v1.29: the survey bridges (MapBase 'bridges': pairs of deck edge lines) as frames (centre, u, length, width)"""
    try:
        with open(WA_FILE, encoding="utf-8") as f:
            BL = [[tuple(q[:2]) for q in x[1]] for x in (json.load(f).get("layers", {}).get("bridges") or [])
                  if len(x[1]) >= 2]
    except Exception as ex:
        log.append(u"FLAG survey bridges not read (%s)" % ex)
        return []
    used, out = set(), []
    for i, a in enumerate(BL):
        if i in used:
            continue
        ma = ((a[0][0] + a[-1][0]) / 2, (a[0][1] + a[-1][1]) / 2)
        j = min((j for j in range(len(BL)) if j != i and j not in used),
                key=lambda j: math.hypot((BL[j][0][0] + BL[j][-1][0]) / 2 - ma[0], (BL[j][0][1] + BL[j][-1][1]) / 2 - ma[1]),
                default=None)
        if j is None:
            continue
        b = BL[j]
        mb = ((b[0][0] + b[-1][0]) / 2, (b[0][1] + b[-1][1]) / 2)
        if math.hypot(ma[0] - mb[0], ma[1] - mb[1]) > 15.0:
            continue
        used.update((i, j))
        L0 = math.hypot(a[-1][0] - a[0][0], a[-1][1] - a[0][1]) or 1e-9
        u = ((a[-1][0] - a[0][0]) / L0, (a[-1][1] - a[0][1]) / L0)
        n = (-u[1], u[0])
        c = ((ma[0] + mb[0]) / 2, (ma[1] + mb[1]) / 2)
        ts = [(p[0] - c[0]) * u[0] + (p[1] - c[1]) * u[1] for p in a + b]
        ws = [(p[0] - c[0]) * n[0] + (p[1] - c[1]) * n[1] for p in a + b]
        t0, t1 = min(ts), max(ts)
        c = (c[0] + u[0] * (t0 + t1) / 2, c[1] + u[1] * (t0 + t1) / 2)
        out.append(dict(c=c, u=u, n=n, L=t1 - t0, W=max(ws) - min(ws)))
    return out


RB_GRID_M = 2.5            # v1.44: m, bed surface points inside the river outline
RB_UNDER_M = 0.5            # v1.44: m, the bed body reaches this far under the lowest bed point (ASSUMED)
CL_FILE = os.path.join(BERGAMA_ROOT, "Data", "selinos_centreline.json")


def _bed_fn(rects, CJ, rings, gz, log):
    """v1.44: the river bed surface z(p) inside his outline: thalweg (Sections z_th per river line, linear down the
    river) at the centreline, parabolic up to the surveyed ground at the outline, never above the surveyed ground;
    None when no thalweg is known"""
    try:
        with open(CL_FILE, encoding="utf-8") as f_:
            CL = [tuple(p) for p in json.load(f_)["points"]]
    except Exception as ex:
        log.append(u"FLAG river bed: centreline not read (%s): the bed follows the survey only" % ex)
        return None
    ch = [0.0]
    for a, b in zip(CL, CL[1:]):
        ch.append(ch[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))

    def proj(p):                                          # (chainage, distance) of p on the centreline
        best = None
        for i, (a, b) in enumerate(zip(CL, CL[1:])):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L2 = dx * dx + dy * dy or 1e-9
            t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
            d = math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)
            if best is None or d < best[1]:
                best = (ch[i] + t * math.sqrt(L2), d)
        return best
    PIPS = [_pip_fast(R) for R in rings]
    st = []
    for name, A, B, Ln, u, n in rects:
        zt = (CJ.get(name) or {}).get("z_th")
        if zt is None:
            continue
        P = [(A[0] + u[0] * s_, A[1] + u[1] * s_) for s_ in [i * 1.0 for i in range(int(Ln) + 1)]]
        P = [p for p in P if any(f_(p) for f_ in PIPS)]
        if P:
            c = (sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P))
            st.append((proj(c)[0], float(zt), name))
    st.sort()
    if not st:
        log.append(u"FLAG river bed: no river section line with a thalweg (z_th) crosses his outline: the bed follows "
                   u"the survey only")
        return None
    log.append(u"river bed thalweg (Sections cache z_th, chainage on the centreline): %s" % u", ".join(
        u"%s ch %.0f m %.2f m" % (nm, c_, z_) for c_, z_, nm in st))

    def zth(c_):
        if len(st) == 1 or c_ <= st[0][0]:
            return st[0][1]
        if c_ >= st[-1][0]:
            return st[-1][1]
        for (ca, za, _a), (cb, zb, _b) in zip(st, st[1:]):
            if ca <= c_ <= cb:
                return za + (zb - za) * (c_ - ca) / ((cb - ca) or 1e-9)
        return st[-1][1]
    edge = {}                                             # outline vertices (every <= 2 m) with their survey height
    for R in rings:
        for a, b in zip(R, R[1:] + R[:1]):
            L_ = math.hypot(b[0] - a[0], b[1] - a[1])
            for k in range(max(1, int(L_ // 2.0))):
                q = (a[0] + (b[0] - a[0]) * k / max(1, int(L_ // 2.0)), a[1] + (b[1] - a[1]) * k / max(1, int(L_ // 2.0)))
                z = gz(q)
                if z is not None:
                    edge.setdefault((int(q[0] // 20), int(q[1] // 20)), []).append((q, z))

    def near_edge(p):
        i, j = int(p[0] // 20), int(p[1] // 20)
        for r in range(1, 6):
            c_ = [e for a in range(i - r, i + r + 1) for b in range(j - r, j + r + 1) for e in edge.get((a, b), [])]
            if c_:
                return min(((math.hypot(p[0] - q[0], p[1] - q[1]), z) for q, z in c_))
        return None

    def bed(p):
        g = gz(p)
        ne = near_edge(p)
        c_, dc = proj(p)
        if ne is None:
            return g
        de, ze = ne
        zt = min(zth(c_), ze)
        r = dc / ((dc + de) or 1e-9)
        z = zt + (ze - zt) * r * r                        # parabolic cross-section: ASSUMED
        return min(z, g) if g is not None else z
    return bed


def build_selinos(ac, miss, log, xy, z0, tin, ox, oy, rects, inside, contours, pts, CJ, SP):
    """v1.29: river bed mesh, water, reeds, boulders, trees, bank walls, historic bridges with arches, piers under the
    long new bridges; every size not in his drawing or the survey is ASSUMED (constants above)"""
    made = []
    del RIVER_MESH[:], WATER_OPS[:]
    gz = lambda p: tin.z(p[0] - ox, p[1] - oy)
    rings = SEL.get("river") or []
    # ---- v1.44: the river bed body per river outline: top = the channel (bed), cuts the ground upwards (SEO)
    bed = _bed_fn(rects, CJ, rings, gz, log)
    n_bp = 0
    if bed and MESH and "CreateMeshes" not in miss:
        for R in rings:
            H = clean(R)
            if len(H) < 3:
                continue
            bx = (min(q[0] for q in H), min(q[1] for q in H), max(q[0] for q in H), max(q[1] for q in H))
            pip = _pip_fast(H)
            edge_z = [gz(q) for q in H]
            if any(z is None for z in edge_z):
                edge_z = [z if z is not None else min(pts, key=lambda p: (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)[2]
                          for z, q in zip(edge_z, H)]
            inner = []
            x = bx[0] + RB_GRID_M / 2
            while x < bx[2]:
                y = bx[1] + RB_GRID_M / 2
                while y < bx[3]:
                    if pip((x, y)):
                        z = bed((x, y))
                        if z is not None:
                            inner.append(((x, y), z))
                    y += RB_GRID_M
                x += RB_GRID_M
            if not inner:
                continue
            zlo = min([z for _p, z in inner] + edge_z) - RB_UNDER_M
            m = dict(level=round(zlo - z0, 3), polygonCoordinates=[dict(xy(q), z=round(z - zlo, 3)) for q, z in zip(H, edge_z)],
                     sublines=[{"coordinates": [dict(xy(p), z=round(z - zlo, 3))]} for p, z in inner],
                     skirtType="SolidBodyWithSkirt", skirtLevel=0.1, ridges="AllSmooth", _mat="riverbed")
            g = ac.create("CreateMeshes", "meshesData", [m], u"river bed body (%d bed points)" % len(inner))
            if not g[0]:                                  # fewer points: every other one
                m["sublines"] = m["sublines"][::2]
                g = ac.create("CreateMeshes", "meshesData", [m], u"river bed body, half the bed points")
            if g[0]:
                made.append(g[0])
                RIVER_MESH.append((g[0], H))
                EXTRA_OPS.append((g[0], "SubtractionUpwards", [xy(q) for q in H]))   # the ground opens into the channel
                n_bp += len(inner)
        log.append(u"river bed: %d body mesh(es), %d bed points every %.1f m, bed = thalweg rising parabolically "
                   u"(ASSUMED) to the surveyed ground at his outline, never above the survey; body %.1f m under the "
                   u"lowest bed point (ASSUMED); each cuts the ground upwards (SEO)" % (
                       len(RIVER_MESH), n_bp, RB_GRID_M, RB_UNDER_M))
    if bed:                                               # the water reaches down to the bed
        gz0 = gz
        PIPR = [_pip_fast(R) for R in rings]
        gz = lambda p: (bed(p) if any(f_(p) for f_ in PIPR) else gz0(p))
    wl = _water_level_fn(rects, CJ, rings, log)
    water_mesh = False
    if bed and RIVER_MESH and MESH and "CreateMeshes" not in miss:   # v1.44: one water body per outline
        n_wm = 0
        for tg_, H in list(RIVER_MESH):
            vz = [wl(q[0], q[1]) for q in H]
            if any(v is None for v in vz):
                continue
            bx = (min(q[0] for q in H), min(q[1] for q in H), max(q[0] for q in H), max(q[1] for q in H))
            pip = _pip_fast(H)
            inner, x = [], bx[0] + WATER_CELL_M / 2
            while x < bx[2]:
                y = bx[1] + WATER_CELL_M / 2
                while y < bx[3]:
                    if pip((x, y)):
                        v = wl(x, y)
                        if v is not None:
                            inner.append(((x, y), v))
                    y += WATER_CELL_M
                x += WATER_CELL_M
            lo = min([bed(q) or v for q, v in zip(H, vz)] + [v for _p, v in inner]) - RB_UNDER_M - 0.5
            m = dict(level=round(lo - z0, 3), polygonCoordinates=[dict(xy(q), z=round(v - lo, 3)) for q, v in zip(H, vz)],
                     sublines=[{"coordinates": [dict(xy(p), z=round(v - lo, 3))]} for p, v in inner],
                     skirtType="SolidBodyWithSkirt", skirtLevel=0.05, ridges="AllSmooth", _mat="water")
            g = ac.create("CreateMeshes", "meshesData", [m], u"river water body (Mesh tool, season level)")
            if g[0]:
                made.append(g[0])
                EXTRA_LINKS.append(dict(targetId={"guid": g[0]}, operatorId={"guid": tg_}, operation="Subtraction"))
                n_wm += 1
        water_mesh = n_wm > 0
        log.append(u"water: %d Mesh bodies, top = the season level down the river (points every %.0f m), cut by the "
                   u"river bed body (SEO): water stands only above the bed" % (n_wm, WATER_CELL_M))
    # ---- water: cells of the river outline where the survey ground is below the level; the ground cuts them (SEO)
    water, n_dry = [], 0
    for R in ([] if water_mesh else rings):              # v1.44: cells only when no water body was made
        x0, y0 = min(q[0] for q in R), min(q[1] for q in R)
        x1, y1 = max(q[0] for q in R), max(q[1] for q in R)
        x = x0
        while x < x1:
            Bd = _clip(R, (1.0, 0.0), x, x + WATER_CELL_M)       # one band, then its cells
            y = min(q[1] for q in Bd) if Bd else y1
            yb = max(q[1] for q in Bd) if Bd else y1
            while y < yb:
                P = _clip(Bd, (0.0, 1.0), y, y + WATER_CELL_M)
                y += WATER_CELL_M
                if len(P) < 3 or abs(area(P)) < 0.5:
                    continue
                P = clean(P)
                if len(P) < 3:
                    continue
                c = (sum(q[0] for q in P) / len(P), sum(q[1] for q in P) / len(P))
                lv = wl(c[0], c[1])
                gs = [z for z in [gz(q) for q in P + [c]] if z is not None]
                if lv is None or not gs:
                    continue
                if min(gs) >= lv - 0.02:
                    n_dry += 1
                    continue
                water.append(dict(level=round(lv - z0, 3), thickness=round(max(0.05, lv - min(gs) + 0.1), 3),
                                  polygonCoordinates=[xy(q) for q in P], _mat="water"))
            x += WATER_CELL_M
    if water and "CreateSlabs" not in miss:
        gw = ac.create("CreateSlabs", "slabsData", water, u"river water (%.0f m cells at the season level)" % WATER_CELL_M)
        made += [g for g in gw if g]
        WATER_OPS.extend((g, [(q["x"], q["y"]) for q in d["polygonCoordinates"]]) for g, d in zip(gw, water) if g)
        log.append(u"water: %d wet cells, %d dry cells left out (ground above the level)" % (len(water), n_dry))
    # ---- reeds and boulders (his pieces)
    reeds, rocks = [], []
    for nm, R, H in SP:
        c = (sum(q[0] for q in H) / len(H), sum(q[1] for q in H) / len(H))
        gs = [z for z in [gz(q) for q in H + [c]] if z is not None]
        if not gs:
            continue
        g = min(gs)
        if nm == "su_bitkii":
            lv = wl(c[0], c[1])
            top = max(g, lv if lv is not None else g) + REED_H_M
            reeds.append(dict(level=round(top - z0, 3), thickness=round(top - g + 0.1, 3),
                              polygonCoordinates=[xy(q) for q in H], _mat="reed"))
        elif nm == "rock":
            h = min(ROCK_H_MAX, 0.5 * math.sqrt(abs(area(H))))
            rocks.append(dict(level=round(g + h - z0, 3), thickness=round(h + 0.2, 3),
                              polygonCoordinates=[xy(q) for q in H], _mat="bridge_stone"))
    if "CreateSlabs" not in miss:
        RP_ = [(tg_, _pip_fast(H_)) for tg_, H_ in RIVER_MESH]
        for lab_, dat_ in ((u"reed beds (%.1f m above the water, ASSUMED)" % REED_H_M, reeds),
                           (u"boulders (his stones / rocks of %.0f m2 and more)" % ROCK_MIN_M2, rocks)):
            if not dat_:
                continue
            g_ = ac.create("CreateSlabs", "slabsData", dat_, lab_)
            made += [g for g in g_ if g]
            for g, d in zip(g_, dat_):                    # v1.44: they cut the ground and the river bed
                if not g:
                    continue
                EXTRA_OPS.append((g, "Subtraction", d["polygonCoordinates"]))
                cq = (sum(q["x"] for q in d["polygonCoordinates"]) / len(d["polygonCoordinates"]) + ox,
                      sum(q["y"] for q in d["polygonCoordinates"]) / len(d["polygonCoordinates"]) + oy)
                EXTRA_LINKS.extend(dict(targetId={"guid": tg_}, operatorId={"guid": g}, operation="Subtraction")
                                   for tg_, f_ in RP_ if f_(cq))
    # ---- trees: his planting boxes (centre = position, the smaller side = crown width), trunk Column + crown slabs
    trunks, crowns, n_t = [], [], {}
    for sp, boxes in (SEL.get("trees") or {}).items():
        H_, cb, td = TREE_SP[sp]
        for B in boxes:
            c = (sum(q[0] for q in B) / len(B), sum(q[1] for q in B) / len(B))
            g = gz(c)
            if g is None:
                continue
            D = min(math.hypot(B[i][0] - B[i - 1][0], B[i][1] - B[i - 1][1]) for i in range(len(B)))
            n_t[sp] = n_t.get(sp, 0) + 1
            if td > 0:
                trunks.append(dict(coordinates=dict(xy(c), z=round(g - z0, 3)), height=round(H_ * cb + 0.5, 3),
                                   circleBased=True, width=td, _mat="bark"))
            zb = g + H_ * cb
            bands = ((0.0, 0.33, 0.7), (0.33, 0.67, 1.0), (0.67, 1.0, 0.6)) if sp != "trees_stone_pine" else \
                ((0.0, 0.5, 1.0), (0.5, 1.0, 0.75))           # stone pine: a flat umbrella
            for f0, f1, wf in bands:
                r = D * wf / 2.0
                oc = [(c[0] + r * math.cos(math.radians(22.5 + 45 * k)), c[1] + r * math.sin(math.radians(22.5 + 45 * k)))
                      for k in range(8)]
                top = zb + (g + H_ - zb) * f1
                crowns.append(dict(level=round(top - z0, 3), thickness=round(max(0.2, (g + H_ - zb) * (f1 - f0)), 3),
                                   polygonCoordinates=[xy(q) for q in oc], _mat="foliage"))
    if trunks and "CreateColumns" not in miss:
        g_ = ac.create("CreateColumns", "columnsData", trunks, u"tree trunks (Column tool)")
        made += [g for g in g_ if g]
        EXTRA_OPS.extend((g, "Subtraction", [d["coordinates"]]) for g, d in zip(g_, trunks) if g)   # v1.44
    if crowns and "CreateSlabs" not in miss:
        made += [g for g in ac.create("CreateSlabs", "slabsData", crowns, u"tree crowns (3 octagon slabs each)") if g]
    if n_t:
        log.append(u"trees (PLANTING_v13_1): %s; heights ASSUMED %s" % (
            u", ".join(u"%s %d" % kv for kv in sorted(n_t.items())),
            u", ".join(u"%s %.0f m" % (k, v[0]) for k, v in sorted(TREE_SP.items()))))
    # ---- bank walls along his istinaat lines: top = the higher ground either side (+1.0 m where level), footing 0.5 m
    bw = []
    for L_ in SEL.get("istinaat") or []:
        for a, b in zip(L_, L_[1:]):
            Ls = math.hypot(b[0] - a[0], b[1] - a[1])
            if Ls < 0.3:
                continue
            nx, ny = -(b[1] - a[1]) / Ls, (b[0] - a[0]) / Ls
            k_n = max(1, int(math.ceil(Ls / RET_SEG_M)))
            for k_ in range(k_n):
                p0 = (a[0] + (b[0] - a[0]) * k_ / k_n, a[1] + (b[1] - a[1]) * k_ / k_n)
                p1 = (a[0] + (b[0] - a[0]) * (k_ + 1) / k_n, a[1] + (b[1] - a[1]) * (k_ + 1) / k_n)
                m_ = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
                s1, s2 = gz((m_[0] + nx * 1.5, m_[1] + ny * 1.5)), gz((m_[0] - nx * 1.5, m_[1] - ny * 1.5))
                zs = [z for z in (s1, s2, gz(m_)) if z is not None]
                if not zs:
                    continue
                hi, lo = max(zs), min(zs)
                if hi - lo < 0.3:
                    hi = hi + BANK_WALL_UP
                lo -= RET_FOOT_M
                bw.append(dict(begCoordinate=xy(p0), endCoordinate=xy(p1), zCoordinate=round(lo - z0, 3),
                               height=round(hi - lo, 3), thickness=BANK_WALL_T, referenceLineLocation="Center",
                               _mat="bridge_stone"))
    if bw and "CreateWalls" not in miss:
        gw_ = ac.create("CreateWalls", "wallsData", bw, u"bank walls (his istinaat lines)")
        made += [g for g in gw_ if g]
        EXTRA_OPS.extend((g, "Subtraction", [d["begCoordinate"], d["endCoordinate"]]) for g, d in zip(gw_, bw) if g)        # v1.31
    # ---- bridges
    frames = _bridge_frames(log)
    hist = []
    for nm_b, p, k, why in HIST_BRIDGES:
        f = min(frames, key=lambda f_: math.hypot(f_["c"][0] - p[0], f_["c"][1] - p[1]), default=None)
        if f is None or math.hypot(f["c"][0] - p[0], f["c"][1] - p[1]) > 30.0:
            log.append(u"FLAG %s: no survey bridge within 30 m of its place: not built" % nm_b)
            continue
        hist.append(f)
        c, u, n, L, W = f["c"], f["u"], f["n"], f["L"], f["W"]
        at = lambda t, w: (c[0] + u[0] * t + n[0] * w, c[1] + u[1] * t + n[1] * w)
        rect = lambda t0, t1: [at(t0, -W / 2), at(t1, -W / 2), at(t1, W / 2), at(t0, W / 2)]
        ends = [z for z in (gz(at(-L / 2, 0)), gz(at(L / 2, 0))) if z is not None]
        bed = [z for z in (gz(at(-L / 2 + L * i / 20.0, 0)) for i in range(21)) if z is not None]
        if not ends or not bed:
            log.append(u"FLAG %s: outside the surveyed ground: not built" % nm_b)
            continue
        top, low = max(ends), min(bed)
        s = (L - (k - 1) * BR_PIER_M) / k
        rise = max(0.5, min(s / 2.0, top - BR_DECK_M - low))
        spring = top - BR_DECK_M - rise
        R_ = (s * s / 4.0 + rise * rise) / (2 * rise)
        parts, pw_ = [], []
        for a_ in range(k):
            t_a = -L / 2 + a_ * (s + BR_PIER_M)
            for j in range(BR_SEG):
                x0_, x1_ = t_a + s * j / BR_SEG, t_a + s * (j + 1) / BR_SEG
                ym = min(math.sqrt(max(0.0, R_ * R_ - (x_ - t_a - s / 2) ** 2)) - (R_ - rise) for x_ in (x0_, x1_))
                b_ = spring + ym
                parts.append(dict(level=round(top - z0, 3), thickness=round(max(0.3, top - b_), 3),
                                  polygonCoordinates=[xy(q) for q in rect(x0_, x1_)], _mat="bridge_stone"))
            if a_ < k - 1:                                 # v1.43: the pier with the Wall tool
                t_p = t_a + s + BR_PIER_M / 2.0
                pw_.append(dict(begCoordinate=xy(at(t_p, -W / 2)), endCoordinate=xy(at(t_p, W / 2)),
                                zCoordinate=round(low - 1.0 - z0, 3), height=round(top - low + 1.0, 3),
                                thickness=BR_PIER_M, referenceLineLocation="Center", _mat="bridge_stone"))
        if pw_ and "CreateWalls" not in miss:
            gw_ = ac.create("CreateWalls", "wallsData", pw_, u"%s: piers (Wall tool)" % nm_b)
            made += [g for g in gw_ if g]
            EXTRA_OPS.extend((g, "Subtraction", [d["begCoordinate"], d["endCoordinate"]]) for g, d in zip(gw_, pw_) if g)
        if "CreateSlabs" not in miss:
            gp_ = ac.create("CreateSlabs", "slabsData", parts, u"%s: arches (Slab tool)" % nm_b)
            made += [g for g in gp_ if g]
            EXTRA_OPS.extend((g, "Subtraction", d["polygonCoordinates"]) for g, d in zip(gp_, parts) if g)
        log.append(u"%s: survey deck %.1f x %.1f m, %d arches of %.1f m span, rise %.1f m (%s), deck top %.2f m on the "
                   u"higher bank, piers %.1f m and %.1f m deck over the crown ASSUMED" % (
                       nm_b, L, W, k, s, rise, u"semicircular" if rise >= s / 2 - 0.01 else u"segmental, the banks are low",
                       top, BR_PIER_M, BR_DECK_M) + u"; " + why)
    # new bridges (his kopruler pieces away from the historic ones): piers where longer than BR_SPAN_MAX
    piers, n_nb = [], 0
    for nm, R, H in SEL.get("bridges") or []:
        c = (sum(q[0] for q in H) / len(H), sum(q[1] for q in H) / len(H))
        if any(math.hypot(f["c"][0] - c[0], f["c"][1] - c[1]) < 25.0 for f in hist):
            continue
        e = max(((H[i - 1], H[i]) for i in range(len(H))),
                key=lambda ab: math.hypot(ab[1][0] - ab[0][0], ab[1][1] - ab[0][1]))
        Le = math.hypot(e[1][0] - e[0][0], e[1][1] - e[0][1]) or 1e-9
        u = ((e[1][0] - e[0][0]) / Le, (e[1][1] - e[0][1]) / Le)
        ts = [(q[0] - c[0]) * u[0] + (q[1] - c[1]) * u[1] for q in H]
        t0, t1 = min(ts), max(ts)
        gb = [z for z in [gz(q) for q in H] if z is not None]
        if not gb or t1 - t0 <= BR_SPAN_MAX:
            continue
        n_nb += 1
        top = max(gb) - 0.5                                # under his 0.50 m deck
        m = int(math.ceil((t1 - t0) / BR_SPAN_MAX))
        for i in range(1, m):
            t = t0 + (t1 - t0) * i / m
            P = _clip(H, u, t - BR_NEW_PIER_M / 2, t + BR_NEW_PIER_M / 2)
            if len(P) < 3:
                continue
            gp = [z for z in [gz(q) for q in P] if z is not None]
            if not gp or top - min(gp) < 0.8:
                continue
            ws_ = [(q[0] - c[0]) * -u[1] + (q[1] - c[1]) * u[0] for q in P]     # across the bridge
            cm_ = (c[0] + u[0] * t, c[1] + u[1] * t)
            piers.append(dict(begCoordinate=xy((cm_[0] - u[1] * min(ws_), cm_[1] + u[0] * min(ws_))),
                              endCoordinate=xy((cm_[0] - u[1] * max(ws_), cm_[1] + u[0] * max(ws_))),
                              zCoordinate=round(min(gp) - 1.0 - z0, 3), height=round(top - min(gp) + 1.0, 3),
                              thickness=BR_NEW_PIER_M, referenceLineLocation="Center", _mat="bridge_stone"))
    if piers and "CreateWalls" not in miss:                # v1.43: the Wall tool
        gp_ = ac.create("CreateWalls", "wallsData", piers, u"new bridge piers (Wall tool)")
        made += [g for g in gp_ if g]
        EXTRA_OPS.extend((g, "Subtraction", [d["begCoordinate"], d["endCoordinate"]]) for g, d in zip(gp_, piers) if g)
    log.append(u"new bridges longer than %.0f m: %d, piers %d (%.1f m thick, at most %.0f m apart, ASSUMED)" % (
        BR_SPAN_MAX, n_nb, len(piers), BR_NEW_PIER_M, BR_SPAN_MAX))
    return made


# ================================================================ v1.30 the existing town ground (Aras 15 Nov 20:41 "what
# about roads ?", "and etc."): the MapBase street region, parks, kerbs, walls and ancient walls in the cut rectangles
MB_FILE = os.path.join(BERGAMA_ROOT, "cached", "bergama_mapbase", "mapbase.json")
TOWN_CELL_M = 20.0          # m: the street region / parks are built in cells this size (each with its holes)
TOWN_UNDER_M = 0.30         # m: a road / park cell reaches this far under the lowest ground in it; the terrain then
#                             shapes its top (SEO intersection), so it lies on the survey ground
TOWN_HOLE_IN = 0.01         # m: a hole cut by a cell edge is kept this far inside it (Archicad needs holes inside)
KERB_H, KERB_T = 0.15, 0.15  # m: kerb height above the ground, thickness: ASSUMED
WALL_H, WALL_T = 1.50, 0.25  # m: survey walls (garden / yard walls) height, thickness: ASSUMED
HWALL_H, HWALL_T = 3.00, 1.00  # m: survey heritage (ancient) walls height, thickness: ASSUMED
TOWN_PT_M = 2.5             # v1.44: m, surveyed-ground points inside each road / park mesh
PAV_MAX_M = 5.0             # v1.44: m, widest pavement strip from a kerb to a building face: ASSUMED
PAV_NEAR_M = 8.0            # v1.44: m, a kerb with no building face this close on either side gets no pavement
PAV_T_M = 0.30              # v1.44: m, pavement build-up under its top (pavers, bedding, base): ASSUMED
EXTRA_LINKS = []            # v1.44: solid element operations made in the builders (road minus pavement)
LINE_SEG_M = 6.0            # m: walls and kerbs in pieces at most this long, each on its own ground
TOWN_OPS = []               # (guid, centre survey m): road and park cells shaped by the terrain


def _bands(R, x0, x1, c):
    """v1.30: R clipped to the x bands [x, x + c) from x0 to x1: {band index: polygon}"""
    out, k, x = {}, 0, x0
    while x < x1:
        P = _clip(R, (1.0, 0.0), x, x + c)
        if P:
            out[k] = P
        k, x = k + 1, x + c
    return out


SURVEY_TREE = {"SEMBOL_TEK_AGAC": ("single tree", 8.0, 0.35, 0.30, 5.0),          # v1.44: (kind, height m, crown
               "SEMBOL_YPDKN_AGAC": ("evergreen", 10.0, 0.25, 0.35, 4.0),       # bottom share, trunk m, crown m):
               "SEMBOL_YAP_DOKMEYEN": ("evergreen", 10.0, 0.25, 0.35, 4.0)}     # ALL ASSUMED (species not surveyed)


def build_survey_trees(ac, miss, log, xy, z0, tin, ox, oy, survey, bld):
    """v1.44: the survey's tree symbols as trunk Column + crown slabs; none inside a building or within 2 m of his
    planting"""
    made, trunks, crowns, n_, n_skip = [], [], [], {}, 0
    cell = {}
    for b in bld:
        R = b["ring"]
        for i in range(int(min(q[0] for q in R) // 20), int(max(q[0] for q in R) // 20) + 1):
            for j in range(int(min(q[1] for q in R) // 20), int(max(q[1] for q in R) // 20) + 1):
                cell.setdefault((i, j), []).append(R)
    plant = [(sum(q[0] for q in B) / len(B), sum(q[1] for q in B) / len(B)) for bx in (SEL.get("trees") or {}).values()
             for B in bx]
    for lay, (kind, H_, cb, td, D) in SURVEY_TREE.items():
        for pl in survey.get(lay) or []:
            if not pl:
                continue
            c = (sum(q[0] for q in pl) / len(pl), sum(q[1] for q in pl) / len(pl))
            if SITE_BOX and not (SITE_BOX[0] <= c[0] <= SITE_BOX[2] and SITE_BOX[1] <= c[1] <= SITE_BOX[3]):
                continue
            g = tin.z(c[0] - ox, c[1] - oy)
            if g is None or any(_inpoly(c, R) for R in cell.get((int(c[0] // 20), int(c[1] // 20)), [])) or \
                    any(math.hypot(c[0] - p[0], c[1] - p[1]) < 2.0 for p in plant):
                n_skip += 1
                continue
            n_[lay] = n_.get(lay, 0) + 1
            trunks.append(dict(coordinates=dict(xy(c), z=round(g - z0, 3)), height=round(H_ * cb + 0.5, 3),
                               circleBased=True, width=td, _mat="bark"))
            zb = g + H_ * cb
            bands = ((0.0, 0.33, 0.7), (0.33, 0.67, 1.0), (0.67, 1.0, 0.6)) if kind == "single tree" else \
                ((0.0, 0.4, 1.0), (0.4, 0.75, 0.7), (0.75, 1.0, 0.35))       # evergreen: a cone
            for f0, f1, wf in bands:
                r = D * wf / 2.0
                oc = [(c[0] + r * math.cos(math.radians(22.5 + 45 * k)), c[1] + r * math.sin(math.radians(22.5 + 45 * k)))
                      for k in range(8)]
                top = zb + (g + H_ - zb) * f1
                crowns.append(dict(level=round(top - z0, 3), thickness=round(max(0.2, (g + H_ - zb) * (f1 - f0)), 3),
                                   polygonCoordinates=[xy(q) for q in oc], _mat="foliage"))
    if trunks and "CreateColumns" not in miss:
        g_ = ac.create("CreateColumns", "columnsData", trunks, u"survey tree trunks (Column tool)")
        made += [g for g in g_ if g]
        EXTRA_OPS.extend((g, "Subtraction", [d["coordinates"]]) for g, d in zip(g_, trunks) if g)   # v1.44
    if crowns and "CreateSlabs" not in miss:
        made += [g for g in ac.create("CreateSlabs", "slabsData", crowns, u"survey tree crowns (3 octagon slabs each)") if g]
    log.append(u"survey trees: %s; %d left out (inside a building, within 2 m of his planting or off the survey); "
               u"heights / crowns ASSUMED: %s" % (u", ".join(u"%s %d" % kv for kv in sorted(n_.items())), n_skip,
                                                  u", ".join(u"%s %.0f m high, %.0f m crown" % (k, v[1], v[4])
                                                            for k, v in SURVEY_TREE.items())))
    return made


def build_survey_stairs(ac, miss, log, xy, z0, tin, ox, oy, segs):
    """v1.44: the survey building stairs: step-edge lines grouped into flights (parallel, ends within 0.8 m, height
    step 0.05-0.40 m); each tread = the band between one edge and the next higher one, top = its surveyed height,
    down to the surveyed ground; a lone edge or the top edge of a flight (the landing) is not built"""
    made = []
    S = []
    for x0, y0, z0_, x1, y1, z1 in segs:
        L_ = math.hypot(x1 - x0, y1 - y0)
        if L_ < 0.3 or (SITE_BOX and not (SITE_BOX[0] <= x0 <= SITE_BOX[2] and SITE_BOX[1] <= y0 <= SITE_BOX[3])):
            continue
        S.append(((x0, y0), (x1, y1), (z0_ + z1) / 2.0, ((x1 - x0) / L_, (y1 - y0) / L_)))
    cell = {}
    for i, (a, b, z, u) in enumerate(S):
        cell.setdefault((int((a[0] + b[0]) / 2 // 2), int((a[1] + b[1]) / 2 // 2)), []).append(i)
    par = list(range(len(S)))

    def fd(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i
    for i, (a, b, z, u) in enumerate(S):
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for j in cell.get((int(m[0] // 2) + di, int(m[1] // 2) + dj), []):
                    if j <= i:
                        continue
                    a2, b2, z2, u2 = S[j]
                    if abs(u[0] * u2[0] + u[1] * u2[1]) < 0.9 or not (0.03 <= abs(z2 - z) <= 0.40):
                        continue
                    m2 = ((a2[0] + b2[0]) / 2, (a2[1] + b2[1]) / 2)
                    if math.hypot(m2[0] - m[0], m2[1] - m[1]) <= 0.8:
                        par[fd(i)] = fd(j)
    G = {}
    for i in range(len(S)):
        G.setdefault(fd(i), []).append(i)
    tr, n_fl, n_lone = [], 0, 0
    for gi in G.values():
        if len(gi) < 2:
            n_lone += 1
            continue
        n_fl += 1
        gi.sort(key=lambda k: S[k][2])
        u0 = S[gi[0]][3]
        for k1, k2 in zip(gi, gi[1:]):
            a1, b1, z1, u1 = S[k1]
            a2, b2, z2, u2 = S[k2]
            if u1[0] * u0[0] + u1[1] * u0[1] < 0:
                a1, b1 = b1, a1
            if u2[0] * u0[0] + u2[1] * u0[1] < 0:
                a2, b2 = b2, a2
            P = [a1, b1, b2, a2]
            if abs(area(P)) < 0.05:
                continue
            gs = [g for g in (tin.z(q[0] - ox, q[1] - oy) for q in P) if g is not None]
            lo = min(gs + [z1 - 0.2]) - 0.1
            tr.append(dict(level=round(z1 - z0, 3), thickness=round(max(0.1, z1 - lo), 3),
                           polygonCoordinates=[xy(q) for q in P], _mat="stair"))
    if tr and "CreateSlabs" not in miss:
        g_ = ac.create("CreateSlabs", "slabsData", tr, u"survey stairs: treads (Slab tool)")
        made += [g for g in g_ if g]
        EXTRA_OPS.extend((g, "Subtraction", d["polygonCoordinates"]) for g, d in zip(g_, tr) if g)
    log.append(u"survey stairs (BINA_MERDIVEN): %d flights, %d treads at their surveyed heights, down to the ground and "
               u"cutting it; %d lone step edges not built (no second edge to give the tread depth)" % (n_fl, len(tr), n_lone))
    return made


def build_town(ac, miss, log, xy, z0, tin, ox, oy, rects, inside):
    """v1.30: the street region (one region with the town blocks as holes) and the parks as slabs per cell that the
    terrain shapes, kerbs and walls from the survey lines as Walls; only inside the cut rectangles (where the terrain is)"""
    made = []
    del TOWN_OPS[:]
    M = read_json(MB_FILE, "MapBase", log)
    if not M:
        log.append(u"FLAG town ground: MapBase cache missing: no roads built")
        return made
    gz = lambda p: tin.z(p[0] - ox, p[1] - oy)
    inr = lambda p: any(inside(p, r) for r in rects)
    allc = [(A[0] + n[0] * d + u[0] * s, A[1] + n[1] * d + u[1] * s)
            for _, A, B, Ln, u, n in rects for d in (-SIDE_M, BACK_M) for s in (0.0, Ln)]
    X0, Y0 = min(q[0] for q in allc), min(q[1] for q in allc)
    X1, Y1 = max(q[0] for q in allc), max(q[1] for q in allc)
    if WHOLE_SITE and SITE_BOX:                           # v1.42: the whole survey extent
        X0, Y0, X1, Y1 = SITE_BOX

    def near(R):
        return not (max(q[0] for q in R) < X0 or min(q[0] for q in R) > X1 or max(q[1] for q in R) < Y0 or
                    min(q[1] for q in R) > Y1)
    polys = M.get("polys") or {}
    st = [[tuple(q[:2]) for q in R] for R in (polys.get("street_net") or []) if len(R) >= 3]
    st = [R for R in st if near(R)]
    pk = [[tuple(q[:2]) for q in R] for R in (polys.get("parks") or []) if len(R) >= 3]
    pk = [R for R in pk if near(R)]
    # even-odd: a street ring inside an odd number of others is a hole (a town block)
    pips = [_pip_fast(R) for R in st]
    bxs = [(min(q[0] for q in R), min(q[1] for q in R), max(q[0] for q in R), max(q[1] for q in R)) for R in st]
    hole = []
    for i, R in enumerate(st):
        p = R[0]
        d = sum(1 for j in range(len(st)) if j != i and bxs[j][0] <= p[0] <= bxs[j][2] and bxs[j][1] <= p[1] <= bxs[j][3]
                and pips[j](p))
        hole.append(d % 2 == 1)
    c = TOWN_CELL_M
    nx = int(math.ceil((X1 - X0) / c))
    ny = int(math.ceil((Y1 - Y0) / c))
    data, cen, kinds = [], [], []
    n_cell = n_hole = 0
    for kind, rings, hl in (("road", st, hole), ("park", pk, [False] * len(pk))):
        BO = [_bands(R, X0, X1, c) for R in rings]
        for i in range(nx):
            for j in range(ny):
                x, y = X0 + i * c, Y0 + j * c
                cc = (x + c / 2, y + c / 2)
                if not any(inr(q) for q in (cc, (x, y), (x + c, y), (x, y + c), (x + c, y + c))):
                    continue
                outs, hls = [], []
                for k, R in enumerate(rings):
                    B = BO[k].get(i)
                    if not B:
                        continue
                    if hl[k]:
                        P = _clip(_clip(B, (1.0, 0.0), x + TOWN_HOLE_IN, x + c - TOWN_HOLE_IN), (0.0, 1.0),
                                  y + TOWN_HOLE_IN, y + c - TOWN_HOLE_IN)
                    else:
                        P = _clip(B, (0.0, 1.0), y, y + c)
                    if len(P) >= 3:
                        P = clean(P)
                    if len(P) >= 3 and abs(area(P)) > 0.05:
                        (hls if hl[k] else outs).append(P)
                for P in outs:
                    H_ = [h for h in hls if _inpoly(h[0], P)]
                    if abs(area(P)) - sum(abs(area(h)) for h in H_) < 1.0:
                        continue                           # a cell all town block: nothing to pave
                    gs = [z for z in [gz(q) for q in P + [cc]] if z is not None]
                    if not gs:
                        continue
                    low = min(gs) - TOWN_UNDER_M         # v1.44: a mesh body on the surveyed ground
                    zq = lambda q, gs=gs: (gz(q) if gz(q) is not None else min(gs))
                    d_ = dict(level=round(low - z0, 3), skirtType="SolidBodyWithSkirt", skirtLevel=0.05,
                              ridges="AllSmooth", polygonCoordinates=[dict(xy(q), z=round(zq(q) - low, 3)) for q in P],
                              _mat=kind)
                    sub_ = []
                    gx_ = x + TOWN_PT_M / 2
                    while gx_ < x + c:
                        gy_ = y + TOWN_PT_M / 2
                        while gy_ < y + c:
                            q = (gx_, gy_)
                            if _inpoly(q, P) and not any(_inpoly(q, h) for h in H_):
                                z_ = gz(q)
                                if z_ is not None:
                                    sub_.append({"coordinates": [dict(xy(q), z=round(z_ - low, 3))]})
                            gy_ += TOWN_PT_M
                        gx_ += TOWN_PT_M
                    if sub_:
                        d_["sublines"] = sub_
                    if H_:
                        d_["holes"] = [{"polygonCoordinates": [dict(xy(q), z=round(zq(q) - low, 3)) for q in h]} for h in H_]
                        n_hole += len(H_)
                    data.append(d_)
                    cen.append((sum(q[0] for q in P) / len(P), sum(q[1] for q in P) / len(P)))
                    kinds.append(kind)
                    n_cell += 1
    road_g = []
    if data and "CreateMeshes" not in miss:             # v1.44: Mesh-tool bodies that cut the ground
        g_ = ac.create("CreateMeshes", "meshesData", data, u"town ground: roads + parks on the surveyed ground (%.0f m cells)" % c)
        made += [g for g in g_ if g]
        EXTRA_OPS.extend((g, "Subtraction", [dict(x=q["x"], y=q["y"]) for q in d["polygonCoordinates"]])
                         for g, d in zip(g_, data) if g)
        road_g = [(g, [(q["x"] + ox, q["y"] + oy) for q in d["polygonCoordinates"]]) for g, d, k in zip(g_, data, kinds)
                  if g and k == "road"]
        log.append(u"town ground: %d road cells (%d town blocks cut out as holes), %d park cells: Mesh bodies, top = the "
                   u"surveyed ground every %.1f m, %.2f m under its lowest point; each cuts the ground (SEO)" % (
                       sum(1 for k in kinds if k == "road"), n_hole, sum(1 for k in kinds if k == "park"), TOWN_PT_M,
                       TOWN_UNDER_M))
    # ---- kerbs and walls (survey lines) as Walls on the ground, in pieces of at most LINE_SEG_M
    L = M.get("lines") or {}
    LN = M.get("lines_net") or {}
    walls, n_by = [], {}
    for key, src, h, t, mat in (("kerbs", LN.get("kerbs") or L.get("kerbs") or [], KERB_H, KERB_T, "bridge_stone"),
                                ("walls", L.get("walls") or [], WALL_H, WALL_T, "bridge_stone"),
                                ("heritage_walls", L.get("heritage_walls") or [], HWALL_H, HWALL_T, "heritage_red")):
        for pl in src:
            P = pl[1] if (len(pl) == 2 and isinstance(pl[0], bool)) else pl
            P = [tuple(q[:2]) for q in P if isinstance(q, (list, tuple)) and len(q) >= 2]
            for a, b in zip(P, P[1:]):
                Ls = math.hypot(b[0] - a[0], b[1] - a[1])
                if Ls < 0.3:
                    continue
                k_n = max(1, int(math.ceil(Ls / LINE_SEG_M)))
                for k_ in range(k_n):
                    p0 = (a[0] + (b[0] - a[0]) * k_ / k_n, a[1] + (b[1] - a[1]) * k_ / k_n)
                    p1 = (a[0] + (b[0] - a[0]) * (k_ + 1) / k_n, a[1] + (b[1] - a[1]) * (k_ + 1) / k_n)
                    m_ = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
                    if not inr(m_):
                        continue
                    zs = [z for z in (gz(p0), gz(p1)) if z is not None]
                    if not zs:
                        continue
                    lo = min(zs) - 0.3
                    walls.append(dict(begCoordinate=xy(p0), endCoordinate=xy(p1), zCoordinate=round(lo - z0, 3),
                                      height=round(max(zs) + h - lo, 3), thickness=t, referenceLineLocation="Center",
                                      _mat=mat))
                    n_by[key] = n_by.get(key, 0) + 1
    if walls and "CreateWalls" not in miss:
        gk_ = ac.create("CreateWalls", "wallsData", walls, u"kerbs + walls (survey lines)")
        made += [g for g in gk_ if g]
        EXTRA_OPS.extend((g, "Subtraction", [w_["begCoordinate"], w_["endCoordinate"]]) for g, w_ in zip(gk_, walls) if g)
        log.append(u"SEO: %d kerb / wall pieces cut the ground (v1.44, Aras 11:33)" % sum(1 for g in gk_ if g))
        # v1.32: kerbs and survey walls do not cut the ground (thousands of tiny operations stalled the publish)
    # ---- v1.44 pavements: from each survey kerb piece to the nearest building face on its side
    fc_ = {}
    for b_ in M.get("bld") or []:
        R_ = [tuple(q[:2]) for q in b_[0]]
        if len(R_) < 3:
            continue
        for i_ in range(int(min(q[0] for q in R_) // 20), int(max(q[0] for q in R_) // 20) + 1):
            for j_ in range(int(min(q[1] for q in R_) // 20), int(max(q[1] for q in R_) // 20) + 1):
                fc_.setdefault((i_, j_), []).append(R_)
    in_bld = lambda q: any(_inpoly(q, R_) for R_ in fc_.get((int(q[0] // 20), int(q[1] // 20)), []))
    pav, n_pskip = [], 0
    for w_ in walls:
        if w_.get("height", 0) > KERB_H + 1.0 or w_.get("thickness") != KERB_T:
            continue                                   # walls, not kerbs
        p0 = (w_["begCoordinate"]["x"] + ox, w_["begCoordinate"]["y"] + oy)
        p1 = (w_["endCoordinate"]["x"] + ox, w_["endCoordinate"]["y"] + oy)
        Ls = math.hypot(p1[0] - p0[0], p1[1] - p0[1]) or 1e-9
        nv = (-(p1[1] - p0[1]) / Ls, (p1[0] - p0[0]) / Ls)
        m_ = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
        best = None
        for sg in (1, -1):
            t_ = 0.5
            while t_ <= PAV_NEAR_M:
                if in_bld((m_[0] + nv[0] * sg * t_, m_[1] + nv[1] * sg * t_)):
                    if best is None or t_ < best[0]:
                        best = (t_, sg)
                    break
                t_ += 0.5
        if best is None or best[0] - 0.5 < 0.8:
            n_pskip += 1
            continue
        wd = min(best[0] - 0.25, PAV_MAX_M)
        o_ = (nv[0] * best[1] * wd, nv[1] * best[1] * wd)
        P_ = [p0, p1, (p1[0] + o_[0], p1[1] + o_[1]), (p0[0] + o_[0], p0[1] + o_[1])]
        zs = [z for z in (gz(q) for q in P_) if z is not None]
        zk = [z for z in (gz(p0), gz(p1)) if z is not None]
        if not zs or not zk:
            n_pskip += 1
            continue
        top = sum(zk) / len(zk) + KERB_H
        pav.append(dict(level=round(top - z0, 3), thickness=round(top - min(zs) + PAV_T_M - KERB_H, 3),
                        polygonCoordinates=[xy(q) for q in P_], _mat="pavement"))
    if pav and "CreateSlabs" not in miss:
        gp_ = ac.create("CreateSlabs", "slabsData", pav, u"pavements (Slab tool, kerb to building face)")
        made += [g for g in gp_ if g]
        EXTRA_OPS.extend((g, "Subtraction", d["polygonCoordinates"]) for g, d in zip(gp_, pav) if g)
        rb_ = [(g, R_, (min(q[0] for q in R_), min(q[1] for q in R_), max(q[0] for q in R_), max(q[1] for q in R_)))
               for g, R_ in road_g]
        for g, d in zip(gp_, pav):
            if not g:
                continue
            cq = (sum(q["x"] for q in d["polygonCoordinates"]) / 4.0 + ox, sum(q["y"] for q in d["polygonCoordinates"]) / 4.0 + oy)
            for rg_, R_, bx_ in rb_:
                if bx_[0] <= cq[0] <= bx_[2] and bx_[1] <= cq[1] <= bx_[3] and _inpoly(cq, R_):
                    EXTRA_LINKS.append(dict(targetId={"guid": rg_}, operatorId={"guid": g}, operation="Subtraction"))
        log.append(u"pavements: %d strips from the survey kerbs to the nearest building face (at most %.1f m, ASSUMED), "
                   u"top = kerb top (%.2f m), %.2f m build-up (ASSUMED); they cut the ground and the road; %d kerb "
                   u"pieces without a building face within %.0f m left without one" % (
                       sum(1 for g in gp_ if g), PAV_MAX_M, KERB_H, PAV_T_M, n_pskip, PAV_NEAR_M))
    log.append(u"kerbs + walls from the survey: %s pieces; heights ASSUMED: kerb %.2f m, wall %.1f m, ancient wall %.1f m"
               % (u", ".join(u"%s %d" % kv for kv in sorted(n_by.items())) or u"none", KERB_H, WALL_H, HWALL_H))
    log.append(u"base map not built: road_edges / town_edges (the street region's outline is the edge), stream_banks "
               u"(the designed bank walls are built), ponds (lines only, no outline), OpenStreetMap paths, walls and "
               u"waterways (survey lines are used), pavements, squares, car parks and steps (not told apart in the base "
               u"map: inside the street region), trees (his planting is built), contours (the terrain mesh)")
    return made


def _seg_dist(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def site_pieces(log):
    """[(layer, ring survey m)] of his masterplan: filled rings of the MP_SLABS layers whose middle lies in the
    working area, exactly his points (only repeats under 5 cm and straight-through points dropped, as Archicad needs)"""
    if not os.path.isfile(MP_FILE):
        log.append(u"FLAG masterplan: %s missing (press MasterplanBase): not built in Archicad" % MP_FILE)
        return []
    with open(MP_FILE, encoding="utf-8") as f:
        J = json.load(f)
    wa = []
    try:
        with open(WA_FILE, encoding="utf-8") as f:
            wa = [[tuple(q[:2]) for q in R] for R in (json.load(f).get("calisma") or []) if len(R) >= 3]
    except Exception as ex:
        log.append(u"FLAG working area not read (%s): his whole masterplan built" % ex)
    out, n_out, n_skip = [], 0, {}
    del RIVER_PTS[:]
    SEL.clear()
    SEL.update(river=[], trees={}, istinaat=[], bridges=[])
    AUDIT.clear()
    seen = set()                                           # v1.29: his file repeats some bridge pieces 4-7 times
    in_wa = lambda R_: not wa or any(_inpoly((sum(q[0] for q in R_) / len(R_), sum(q[1] for q in R_) / len(R_)), W)
                                     for W in wa)
    for key, pieces in J.get("layers", {}).items():
        parts = key.split("/")
        AUDIT[key] = [len(pieces), 0, _audit_status(key)]
        if "su_outline" in parts:                          # v1.29: river bed + water
            SEL["river"] += [[tuple(v[:2]) for v in p[4]] for p in pieces if p[0] == "r" and len(p[4]) >= 3 and
                             in_wa(p[4])]
            AUDIT[key][1] = len(SEL["river"])
        if "PLANTING_v13_1" in parts and parts[-1] in TREE_SP:   # v1.29: trees (picture boxes)
            SEL["trees"][parts[-1]] = [[tuple(v[:2]) for v in p[4]] for p in pieces if len(p[4]) >= 4 and in_wa(p[4])]
            AUDIT[key][1] = len(SEL["trees"][parts[-1]])
            continue
        if "istinaat" in parts:                            # v1.29: bank walls along his lines
            SEL["istinaat"] += [[tuple(v[:2]) for v in p[4]] for p in pieces if p[0] == "l" and len(p[4]) >= 2 and
                                in_wa(p[4])]
            AUDIT[key][1] = len(SEL["istinaat"])
            continue
        if "su_outline" in parts:                          # v1.19: his river outline, for the tier direction
            for p in pieces:
                RIVER_PTS.extend(tuple(v[:2]) for v in p[4])
        nm = next((p_ for p_ in reversed(parts) if p_ in MP_SLABS), None)
        if "kopruler" in parts:
            nm = "kopruler"                                # v1.21: every bridge piece is a bridge (0.50 m)
        if "tas" in parts or "kaya" in parts:
            nm = "rock"                                    # v1.29: his stones and rocks (boulders from ROCK_MIN_M2)
        if nm is None:
            if not any(p_ in MP_SKIP for p_ in parts):
                n_skip[parts[-1]] = n_skip.get(parts[-1], 0) + len(pieces)
            continue
        for p in pieces:
            R = [tuple(v[:2]) for v in p[4]]
            ol_ = nm in OUTLINE_LAYERS or any(p_ in OUTLINE_LAYERS for p_ in parts)   # v1.21: outline-only layers
            if p[0] not in ("r", "a") or (not p[1] and not (ol_ and (p[0] == "r" or nm == "kopruler"))) or len(R) < 3 or \
                    abs(area(R)) < (ROCK_MIN_M2 if nm == "rock" else 0.5) or abs(area(R)) > MP_MAX_M2:
                continue                                   # v1.29: his bridge picture-clip shapes count as outlines
            if p[0] == "a" and len(R) == 4:
                continue                                   # a picture's own rectangle (nodes common v8.2)
            c = (sum(q[0] for q in R) / len(R), sum(q[1] for q in R) / len(R))
            if wa and not any(_inpoly(c, W) for W in wa):
                n_out += 1
                continue
            H = clean(R[:-1] if R[0] == R[-1] else R)
            k_ = (nm, round(c[0], 1), round(c[1], 1), round(abs(area(R))))
            if len(H) >= 3 and k_ not in seen:
                seen.add(k_)
                AUDIT[key][1] += 1
                out.append((nm, R, H))
                PIECE_KEY[id(H)] = next((m_ for w_, m_ in PIECE_MAT if w_ in parts), None)   # v1.18
    drop = set()                                           # v1.21: outline layers: the outermost rings only
    for i, (n_i, R_i, H_i) in enumerate(out):
        if n_i not in OUTLINE_LAYERS:
            continue
        ci = (sum(q[0] for q in H_i) / len(H_i), sum(q[1] for q in H_i) / len(H_i))
        a_i = abs(area(H_i))
        if any(j != i and n_j == n_i and abs(area(H_j)) > a_i and _inpoly(ci, H_j) for j, (n_j, R_j, H_j) in enumerate(out)):
            drop.add(i)
    if drop:
        out = [o for i, o in enumerate(out) if i not in drop]
        log.append(u"outline layers (bridges, stepped terraces): %d inner rings inside a bigger one left out" % len(drop))
    SEL["bridges"] = [o for o in out if o[0] == "kopruler"]
    log.append(u"masterplan layer audit (master.svg via MasterplanBase; masterplan2.svg in the next pass): " + u"; ".join(
        u"%s %d piece(s), %d taken: %s" % (k, v[0], v[1], v[2] or (u"built: slabs" if v[1] else
                                                                     u"not built: no filled outline in the working area"))
        for k, v in sorted(AUDIT.items())))
    log.append(u"masterplan pieces for Archicad: %d in the working area (%s), %d outside it; not modelled: %s" % (
        len(out), u", ".join(u"%s %d" % (k, sum(1 for o in out if o[0] == k)) for k in sorted(set(o[0] for o in out))),
        n_out, u", ".join(u"%s %d" % kv for kv in sorted(n_skip.items())) or u"none"))
    return out


def build_site(ac, miss, log, xy, z0, tin, ox, oy, pieces):
    """his pieces as slabs on their exact outlines, top at the survey ground under their middle (+ MP_SLABS rise)"""
    del SITE_REC[:]
    TIER_N[:] = [0, 0]
    if not pieces or "CreateSlabs" in miss:
        return []
    data, keep, n_noz = [], [], 0
    zs_known = []
    for nm, R, H in pieces:
        c = (sum(q[0] for q in H) / len(H), sum(q[1] for q in H) / len(H))
        g = tin.z(c[0] - ox, c[1] - oy)
        if g is None:
            gs = [tin.z(q[0] - ox, q[1] - oy) for q in H]
            gs = [x for x in gs if x is not None]
            g = min(gs) if gs else None
        if g is None:
            n_noz += 1
            continue
        zs_known.append(g)
        th, up = MP_SLABS[nm]
        if nm == "kopruler":                               # v1.21: deck top = the highest ground under it (banks)
            gb = [tin.z(q[0] - ox, q[1] - oy) for q in H]
            gb = [x for x in gb if x is not None]
            g = max(gb) if gb else g
        if nm in TIER_KEYS and RIVER_PTS:                  # v1.19: seating tiers down to the river
            r = min(RIVER_PTS, key=lambda q: (q[0] - c[0]) ** 2 + (q[1] - c[1]) ** 2)
            d = math.hypot(c[0] - r[0], c[1] - r[1])
            if d > 0.01:
                u = ((c[0] - r[0]) / d, (c[1] - r[1]) / d)         # pointing away from the river
                ts = [q[0] * u[0] + q[1] * u[1] for q in H]
                gs = [tin.z(q[0] - ox, q[1] - oy) for q in H]
                gs = [x for x in gs if x is not None] or [g]
                lo, hi = min(gs), max(gs)
                k, t = 0, min(ts)
                while t < max(ts) - 0.05:
                    P = _clip(H, u, t, min(t + TIER_D, max(ts)))
                    if len(P) >= 3 and abs(area(P)) > 0.05:
                        top = min(lo + (k + 1) * TIER_H, max(hi, lo + TIER_H))
                        data.append(dict(level=round(top - z0, 3), thickness=round(max(0.4, top - lo + 0.4), 3),
                                         polygonCoordinates=[xy(q) for q in P], _mat=PIECE_KEY.get(id(H))))
                        keep.append(None)
                        TIER_N[0] += 1
                    k, t = k + 1, t + TIER_D
                TIER_N[1] += 1
                continue
        data.append(dict(level=round(g + up - z0, 3), thickness=th, polygonCoordinates=[xy(q) for q in H],
                         _mat=PIECE_KEY.get(id(H))))                       # v1.18: his legend material
        keep.append((nm, R))
    gs_ = ac.create("CreateSlabs", "slabsData", data, u"masterplan pieces (his outlines)")
    _reg_ops([None if (kp and kp[0] == "kopruler") else g_ for g_, kp in zip(gs_, keep)], data)   # v1.29: a bridge
    # deck spans the river: it neither cuts the bed nor gets retaining walls
    for g_, kp in zip(gs_, keep):
        if g_ and kp:                                      # v1.19: tiers are his outline cut, not checked whole
            SITE_REC.append((g_, kp[0], kp[1]))
    if TIER_N[1]:
        log.append(u"stepped terraces: %d pieces as %d seating tiers (%.2f m deep x %.2f m high = 4 steps of 12 x 30 cm "
                   u"merged, Aras 19:09 + 19:13 UTC), stepping down toward his river outline; stair aisles not placed" % (
                       TIER_N[1], TIER_N[0], TIER_D, TIER_H))
    elif any(n_ in TIER_KEYS for n_, _R, _H in pieces):
        log.append(u"FLAG stepped terraces built flat: no river outline (su_outline) in the MasterplanBase cache")
    if n_noz:
        log.append(u"masterplan: %d piece(s) outside the surveyed ground (no height): not built" % n_noz)
    return [g_ for g_ in gs_ if g_]


def site_accuracy(ac, log, ox, oy):
    """v1.16: every masterplan slab read back from Archicad; per piece the largest distance from one of his points to
    the Archicad outline (m); report per layer, FLAG over MP_TOL_M, written to cached/bergama_archicad/mp_accuracy.json"""
    if not SITE_REC:
        return
    if not ac.has("GetDetailsOfElements"):
        log.append(u"FLAG masterplan accuracy: Tapir has no GetDetailsOfElements: not measured")
        return
    res, n_read = [], 0

    def pts(o, acc):
        if isinstance(o, dict):
            if "x" in o and "y" in o and isinstance(o["x"], (int, float)):
                acc.append((o["x"] + ox, o["y"] + oy))
            for v in o.values():
                pts(v, acc)
        elif isinstance(o, list):
            for v in o:
                pts(v, acc)
    for i in range(0, len(SITE_REC), CHUNK):
        part = SITE_REC[i:i + CHUNK]
        try:
            d = ac.t("GetDetailsOfElements", {"elements": [{"elementId": {"guid": g}} for g, _n, _R in part]})
            lst = d.get("detailsOfElements") or []
        except Exception as ex:
            log.append(u"FLAG masterplan accuracy: read-back failed (%s)" % ex)
            return
        for (g, nm, R), det in zip(part, lst):
            P = []
            pts(det, P)
            if len(P) < 3:
                continue
            n_read += 1
            off = max(min(_seg_dist(p, P[j - 1], P[j]) for j in range(len(P))) for p in R)
            res.append((nm, g, off))
    by = {}
    for nm, g, off in res:
        by.setdefault(nm, []).append(off)
    bad = [(nm, g, off) for nm, g, off in res if off > MP_TOL_M]
    log.append(u"masterplan accuracy (Archicad vs master.svg, m): %s; %d of %d pieces read back" % (
        u"; ".join(u"%s n %d max %.3f mean %.3f" % (k, len(v), max(v), sum(v) / len(v)) for k, v in sorted(by.items())),
        n_read, len(SITE_REC)))
    if bad:
        log.append(u"FLAG masterplan accuracy: %d piece(s) more than %.2f m off his drawing, worst %s %.3f m" % (
            len(bad), MP_TOL_M, max(bad, key=lambda b: b[2])[0], max(b[2] for b in bad)))
    try:
        with open(os.path.join(CACHE_DIR, "mp_accuracy.json"), "w", encoding="utf-8") as f:
            json.dump(dict(version=VERSION, tol_m=MP_TOL_M, per_layer=dict((k, dict(n=len(v), max=max(v),
                                                                                     mean=sum(v) / len(v)))
                                                                           for k, v in by.items()),
                           over_tol=[dict(layer=nm, guid=g, off_m=round(off, 4)) for nm, g, off in bad]), f, indent=1)
    except Exception as ex:
        log.append(u"FLAG mp_accuracy.json not written (%s)" % ex)


# ================================================================ main
def main():
    t0 = time.time()
    SEO_OPS[:], SEO_TERR[:], CANOPY_REC[:], EXTRA_OPS[:] = [], [], [], []   # v1.27: fresh per run (a re-run in the same Rhino kept old ones)
    KEEP.clear(); ITEMS[:] = []; NEW_G.clear(); N_KEPT[0] = 0
    LOCKED_BB[:] = []; EXTRA_LINKS[:] = []; N_LOCKSKIP[0] = 0; N_TINONLY[0] = 0; N_RAFT[:] = [0, 0.0]; LINK_T.clear(); PID[0] = None             # v1.44          # v1.34: fresh per run
    log = []
    ac = AC(log)
    try:
        ver = ac.t("GetAddOnVersion").get("version", "?")
    except Exception as ex:
        raise RuntimeError(u"Archicad answers but Tapir does not (%s): install / load the Tapir add-on" % ex)
    log.insert(0, u"TAPIR OK %s (%s)" % (ver, ac.url))
    need = ["CreateMeshes", "CreateWalls", "CreateWindows", "CreateRoofs", "CreateSlabs", "CreateSections",
            "CreateLayers", "GetAttributesByType", "DeleteElements", "GetStories", "SetSectionsAndElevationsDetails",
            "GetNavigatorItemTree", "CreateViewMapFolder", "CreateViewsInViewMap", "GetPublisherSets",
            "PublishPublisherSet", "ChangeWindow"]
    miss = [c for c in need if not ac.has(c)]
    if miss:
        log.append(u"FLAG Tapir %s lacks %s: update Tapir (Archicad > Options > Add-On Manager, or the Tapir "
                   u"installer) for the full model; the steps that need them are skipped" % (ver, u", ".join(miss)))
    L_ = load_lib(log)
    S = read_json(os.path.join(BERGAMA_ROOT, "cached", "bergama_sections", "sections.json"), "Sections", log)
    M = read_json(os.path.join(BERGAMA_ROOT, "cached", "bergama_mapbase", "mapbase.json"), "MapBase", log)
    mpb = glob.glob(os.path.join(BERGAMA_ROOT, "cached", "bergama_masterplanbase*", "*.json"))
    log.append(u"MasterplanBase: %s (proposals come in AcBuild v2)" % (mpb[0] if mpb else u"not written yet"))
    cuts = [(c["name"], tuple(c["A"]), tuple(c["B"])) for c in S["cuts"]]
    if not cuts:
        raise RuntimeError(u"sections.json holds no cut: press Sections first")
    ox = round(sum(p[0] for _, a, b in cuts for p in (a, b)) / (2 * len(cuts)), -2)
    oy = round(sum(p[1] for _, a, b in cuts for p in (a, b)) / (2 * len(cuts)), -2)
    _pj = os.path.join(CACHE_DIR, "acbuild.json")
    if not os.path.isfile(_pj) and os.path.isfile(OLD_CACHE):
        _pj = OLD_CACHE                     # v1.42: the same origin as the sections project
    if os.path.isfile(_pj):                 # v1.4: one origin for the life of the Archicad project
        with open(_pj, encoding="utf-8") as f:
            _o = json.load(f).get("origin")
        if _o:
            ox, oy = float(_o[0]), float(_o[1])
    log.append(u"Archicad origin = survey (%.0f, %.0f); heights absolute (m above sea level)" % (ox, oy))
    xy = lambda p: {"x": round(p[0] - ox, 3), "y": round(p[1] - oy, 3)}

    # ---- rectangles, survey, buildings
    rects = []
    for name, A, B in cuts:
        Ln, u, n = frame(A, B)
        rects.append((name, A, B, Ln, u, n))
    allp = [(A[0] + n[0] * d + u[0] * s, A[1] + n[1] * d + u[1] * s)
            for _, A, B, Ln, u, n in rects for d in (-SIDE_M, BACK_M) for s in (0.0, Ln)]
    SP = site_pieces(log)                                 # v1.16: his masterplan pieces in the working area
    allp += [q for R in SEL.get("river") or [] for q in R]   # v1.29: the survey must cover the whole river
    SV = None                                             # v1.44: the survey cache when no Rhino
    if WHOLE_SITE and _in_rhino():
        import Rhino
        if Rhino.RhinoDoc.ActiveDoc.ModelUnitSystem != Rhino.UnitSystem.Meters:
            raise RuntimeError(u"the Rhino model is in %s, not metres: set Rhino to metres WITHOUT scaling, then import "
                               u"Bergama_Altlik.3dm again" % Rhino.RhinoDoc.ActiveDoc.ModelUnitSystem)
    elif WHOLE_SITE:
        if not os.path.isfile(SURVEY_CACHE):
            raise RuntimeError(u"no Rhino and no survey cache (%s): run AcBuild once in Rhino with Bergama_Altlik.3dm "
                               u"(in metres)" % SURVEY_CACHE)
        with open(SURVEY_CACHE, encoding="utf-8") as f:
            SV = json.load(f)
        log.append(u"survey from the cache %s (written %s from Rhino; no Rhino needed)" % (SURVEY_CACHE, SV.get("made")))
    if WHOLE_SITE:                                        # v1.42: the whole survey
        survey = SV["survey"] if SV else L_["read_survey"]((-1e12, -1e12, 1e12, 1e12), log)
        if not SV:                                        # v1.44: floor labels + stair edges (cached with the survey)
            survey["_labels"], survey["_stairs"] = _read_extra(log)
        cp_ = [p for nm_ in L_["SURVEY_LAYERS"] if nm_.startswith("EGRI") for pl in survey.get(nm_, []) for p in pl
               if p[2] > 1.0]
        box = (min(p[0] for p in cp_), min(p[1] for p in cp_), max(p[0] for p in cp_), max(p[1] for p in cp_))
        SITE_BOX[:] = list(box)
        if box[2] - box[0] > 50000.0 or box[3] - box[1] > 50000.0:   # v1.44: millimetres read as metres
            raise RuntimeError(u"the survey extent is %.0f x %.0f m: the Rhino model is not in metres (mm import?)" % (
                box[2] - box[0], box[3] - box[1]))
        log.append(u"WHOLE SITE: survey contour extent x %.1f..%.1f, y %.1f..%.1f (%.0f x %.0f m); survey points "
                   u"outside it left out" % (box[0], box[2], box[1], box[3], box[2] - box[0], box[3] - box[1]))
    else:
        box = (min(p[0] for p in allp), min(p[1] for p in allp), max(p[0] for p in allp), max(p[1] for p in allp))
        survey = L_["read_survey"](box, log)
    spots = {}
    for name in L_["SURVEY_LAYERS"]:
        for pl in survey.get(name, []):
            for p in pl:
                if p[2] > 1.0 and box[0] <= p[0] <= box[2] and box[1] <= p[1] <= box[3]:
                    spots[(int(p[0] // GRID_M), int(p[1] // GRID_M))] = p
    log.append(u"survey heights: %d (one per %.0f m cell)" % (len(spots), GRID_M))
    contours = [pl for name in L_["SURVEY_LAYERS"] if name.startswith("EGRI") for pl in survey.get(name, [])
                if len(pl) >= 2 and min(p[2] for p in pl) > 1.0]

    def inside_cut(p, r):
        s, o = so(p, r[1], r[4], r[5])
        return -1e-6 <= s <= r[3] + 1e-6 and -SIDE_M <= o <= BACK_M

    def inside(p, r):                                     # v1.42: the whole survey extent
        if WHOLE_SITE:
            return box[0] <= p[0] <= box[2] and box[1] <= p[1] <= box[3]
        return inside_cut(p, r)
    pts = list(spots.values())
    tp_ = [(p[0] - ox, p[1] - oy, p[2]) for p in pts]
    if SV and SV.get("n") == len(pts) and SV.get("origin") == [ox, oy] and SV.get("tri"):
        tin = _tin_from(L_, tp_, SV["tri"])               # v1.44: no Grasshopper
    elif SV:
        raise RuntimeError(u"the survey cache does not match (points or origin): run AcBuild once in Rhino")
    else:
        tin = L_["Tin"](tp_)
        if WHOLE_SITE:                                    # v1.44: cache for the Rhino-free runs
            try:
                os.makedirs(os.path.dirname(SURVEY_CACHE), exist_ok=True)
                with open(SURVEY_CACHE + ".tmp", "w", encoding="utf-8") as f:
                    json.dump(dict(made=time.strftime("%Y-%m-%d %H:%M:%S"), n=len(pts), origin=[ox, oy],
                                   survey=survey, tri=[list(t) for t in tin.t]), f)
                os.replace(SURVEY_CACHE + ".tmp", SURVEY_CACHE)
                log.append(u"survey cached for Rhino-free runs: %s (%d points, %d triangles)" % (
                    SURVEY_CACHE, len(pts), len(tin.t)))
            except Exception as ex:
                log.append(u"FLAG survey cache not written (%s)" % ex)
    zmin_all = min(p[2] for p in pts) if pts else 0.0
    bld, skipped = [], 0
    LB_ = {}                                              # v1.44: survey floor labels by 20 m cell
    for v_, lx_, ly_ in (survey.get("_labels") or []):
        LB_.setdefault((int(lx_ // 20), int(ly_ // 20)), []).append((v_, lx_, ly_))
    n_lab, n_labdiff = 0, 0
    for i, (b, x) in enumerate(zip(M["bld"], M.get("bld_x") or [[0, "", ""]] * len(M["bld"]))):
        ring = [tuple(q) for q in b[0]]
        if len(ring) >= 2 and ring[0] == ring[-1]:
            ring = ring[:-1]
        ring = clean(ring)
        if len(ring) < 3 or abs(area(ring)) < 4.0 or not any(inside(q, r) for q in ring for r in rects):
            continue
        fl = int(x[0] or 0)
        lv_ = [v_ for i_ in range(int(min(q[0] for q in ring) // 20), int(max(q[0] for q in ring) // 20) + 1)
               for j_ in range(int(min(q[1] for q in ring) // 20), int(max(q[1] for q in ring) // 20) + 1)
               for v_, lx_, ly_ in LB_.get((i_, j_), []) if _inpoly((lx_, ly_), ring)]
        if lv_:                                           # v1.44: the survey's own floor count wins
            n_lab += 1
            n_labdiff += int(fl > 0 and fl != max(lv_))
            fl = max(lv_)
        if fl <= 0:
            skipped += 1                          # v1.14: built as 1 floor (ASSUMED), not left out
            fl = 1
        cx, cy = sum(q[0] for q in ring) / len(ring), sum(q[1] for q in ring) / len(ring)
        zb = tin.z(cx - ox, cy - oy)
        if zb is None:
            near = min(pts, key=lambda p: (p[0] - cx) ** 2 + (p[1] - cy) ** 2) if pts else None
            zb = near[2] if near else zmin_all
        if area(ring) < 0:
            ring = ring[::-1]                     # counter-clockwise: the outward normal of edge a->b is (dy, -dx)
        cut_by = [r for r in rects if any(so(q, r[1], r[4], r[5])[1] < 0 for q in ring)
                  and any(so(q, r[1], r[4], r[5])[1] >= 0 for q in ring)
                  and any(0 <= so(q, r[1], r[4], r[5])[0] <= r[3] for q in ring)]
        bld.append(dict(ring=ring, fab=b[1], fl=fl, h=fl * storey(b[1], x[1] if len(x) > 1 else u""), z=zb,
                        cut=bool(cut_by), views=[r for r in rects if any(inside_cut(q, r) for q in ring)]))
    for x0_, y0_, x1_, y1_, ring, h_, _f in (L_["red_hall_load"](log) if "red_hall_load" in L_ else []):
        ring = clean([tuple(q) for q in ring])
        if len(ring) < 3 or not any(inside(q, r) for q in ring for r in rects):
            continue
        if area(ring) < 0:
            ring = ring[::-1]
        cx, cy = sum(q[0] for q in ring) / len(ring), sum(q[1] for q in ring) / len(ring)
        zb = tin.z(cx - ox, cy - oy)
        bld.append(dict(ring=ring, fab=u"Kızıl Avlu", fl=-1, h=h_, z=zb if zb is not None else zmin_all,
                        cut=False, views=[r for r in rects if any(inside_cut(q, r) for q in ring)]))
        log.append(u"Kızıl Avlu hall: %d points, walls %.0f m, base z %.1f m" % (len(ring), h_, bld[-1]["z"]))
    NB = node_buildings(log)                              # v1.14: the node buildings (placed by Perspectives)
    if NB:                                                # v1.33: a node building replaces the survey building under it
        n0 = len(bld)
        bld = [b for b in bld if b["fl"] < 0 or not any(_overlap_frac(b["ring"], [tuple(q[:2]) for q in nb["foot"]], (
            min(q[0] for q in b["ring"]), min(q[1] for q in b["ring"]), max(q[0] for q in b["ring"]),
            max(q[1] for q in b["ring"]))) > COL_HALL_F for nb in NB)]
        log.append(u"node buildings: %d survey building(s) under a node building left out (it takes their place)" % (
            n0 - len(bld)))
    # v1.28 (Aras 15 Nov 20:10 "also please solve these kinda collisions"): footprints that overlap
    bb_ = [(min(q[0] for q in b["ring"]), min(q[1] for q in b["ring"]), max(q[0] for q in b["ring"]),
            max(q[1] for q in b["ring"])) for b in bld]
    order = sorted(range(len(bld)), key=lambda i: (bld[i]["fl"] >= 0, -abs(area(bld[i]["ring"]))))  # halls first, then big
    keep_, drop_, n_hall, n_dup, n_touch = [], set(), 0, 0, 0
    for i in order:
        A_ = bld[i]
        for j in keep_:
            if bb_[i][0] > bb_[j][2] or bb_[j][0] > bb_[i][2] or bb_[i][1] > bb_[j][3] or bb_[j][1] > bb_[i][3]:
                continue
            f = _overlap_frac(A_["ring"], bld[j]["ring"], bb_[i])
            if bld[j]["fl"] < 0 and f > COL_HALL_F:      # a survey building inside the Kızıl Avlu hall: the hall stays
                drop_.add(i); n_hall += 1
                break
            if f > COL_DUP_F:                            # the same building drawn twice: the bigger one stays
                drop_.add(i); n_dup += 1
                break
            if f > 0.0:
                n_touch += 1
        if i not in drop_:
            keep_.append(i)
    if drop_:
        bld = [b for i, b in enumerate(bld) if i not in drop_]
    log.append(u"collisions: %d survey building(s) overlapping the Kızıl Avlu hall by more than %.0f%% left out (the hall "
               u"stays), %d duplicate footprint(s) (more than %.0f%% inside a bigger one) left out, %d small overlap(s) "
               u"kept" % (n_hall, COL_HALL_F * 100, n_dup, COL_DUP_F * 100, n_touch))
    log.append(u"floor counts: %d buildings take the survey's floor label (YAZI_KAT_ADEDI) standing in them (%d differ "
               u"from MapBase); storeys %.1f m (civic %.1f, sacred %.1f, industry %.1f: the project rule)" % (
                   n_lab, n_labdiff, STOREY_M, STOREY["civic"], STOREY["sacred"], STOREY["industry"]))
    log.append(u"buildings in the cut rectangles: %d (%d cut by a line); %d without a floor count built as 1 floor (ASSUMED)" % (
        len(bld), sum(1 for b in bld if b["cut"]), skipped))

    backs, deep, bands = {}, {}, {}
    for name, A, B, Ln, u, n in rects:                     # v1.3: the ground behind, from the same TIN
        # v1.6: as deep as the farthest building this cut sees (other cuts' houses show beyond 200 m), <= VIEW_M
        D = [so(q, A, u, n) for b in bld for q in b["ring"]]
        dm = min(VIEW_M, max([BACK_M] + [o_ for s_, o_ in D if 0.0 <= s_ <= Ln and o_ > 0]))
        deep[name] = dm
        prof, s = [], 0.0
        while s <= Ln + 1e-9:
            zs = [tin.z(A[0] + u[0] * s + n[0] * d - ox, A[1] + u[1] * s + n[1] * d - oy)
                  for d in list(range(10, int(BACK_M) + 1, 5)) + list(range(int(BACK_M) + 10, int(dm) + 1, 10))]
            zs = [z for z in zs if z is not None]
            prof.append([round(s, 2), round(max(zs), 2) if zs else None])
            s += 2.0
        backs[name] = prof
        # v1.7: depth bands, each raised to the bases of the buildings standing in it
        edges = [e for e in (10.0, 50.0, 100.0, 200.0, 400.0) if e < dm] + [dm]
        BB = []
        for b in bld:
            SO = [so(q, A, u, n) for q in b["ring"]]
            oc = sum(o_ for s_, o_ in SO) / len(SO)
            s0_, s1_ = max(0.0, min(s_ for s_, o_ in SO)), min(Ln, max(s_ for s_, o_ in SO))
            if oc > 0 and s1_ > s0_:
                BB.append((oc, s0_, s1_, b["z"]))
        bl = []
        for d0, d1 in zip(edges, edges[1:]):
            st = 5 if d1 <= BACK_M else 10
            ds = list(range(int(d0), int(d1) + 1, st)) or [int(d0)]
            pr_, s = [], 0.0
            while s <= Ln + 1e-9:
                zs = [tin.z(A[0] + u[0] * s + n[0] * d - ox, A[1] + u[1] * s + n[1] * d - oy) for d in ds]
                zs = [z for z in zs if z is not None] + [z_ for oc, a_, b_, z_ in BB if d0 <= oc < d1 and a_ <= s <= b_]
                pr_.append([round(s, 2), round(max(zs), 2) if zs else None])
                s += 2.0
            bl.append(dict(d=round((d0 + d1) / 2.0, 1), d0=d0, d1=d1, prof=pr_))
        bands[name] = bl
        backs[name] = [[pt[0], max([z_ for z_ in [pt[1]] + [b_["prof"][i][1] for b_ in bl] if z_ is not None] or [None])
                        if any(z_ is not None for z_ in [pt[1]] + [b_["prof"][i][1] for b_ in bl]) else None]
                       for i, pt in enumerate(prof)]
    log.append(u"ground behind: %d cut profiles (highest survey ground 10 m to the farthest building seen, every "
               u"2 m: %s)" % (len(backs), u", ".join(u"%s %.0f m" % kv for kv in sorted(deep.items()))))


    if _PH1 is not None:                                  # v1.22: the Rhino part is done; Rhino may go on
        _PH1.set()
    # ---- clear the previous run, stories, layers
    os.makedirs(CACHE_DIR, exist_ok=True)
    pj = os.path.join(CACHE_DIR, "acbuild.json")
    old = {}
    if os.path.isfile(pj):
        with open(pj, encoding="utf-8") as f:
            old = json.load(f)
    # v1.10 (Aras 15 Nov 15:00 "you need to make archicad runs faster"): the model is rebuilt only when its inputs
    # changed (buildings, cut lines, masterplan canopies, Sections levels, build code) or Archicad holds other counts
    import hashlib
    BSECS = node_secs(NB)
    hsrc = [VERSION, BUILD_SIG, MESH, [(nm, list(A), list(B)) for nm, A, B, Ln, u, n in rects], NB,
            [(b["ring"], b["fab"], b["fl"], b["h"], b["z"], b["cut"], [r[0] for r in b["views"]]) for b in bld],
            [(nm, [list(q) for q in R]) for nm, R, H in SP]]          # v1.16
    for fp in sorted(glob.glob(os.path.join(BERGAMA_ROOT, "cached", "bergama_masterplanbase*", "*.json"))) + [
            os.path.join(BERGAMA_ROOT, "cached", "bergama_sections", "cuts.json"), WA_FILE, MB_FILE]:
        try:
            with open(fp, "rb") as f:
                hsrc.append(hashlib.sha1(f.read()).hexdigest())
        except Exception:
            hsrc.append(None)
    sig = hashlib.sha1(json.dumps(hsrc, default=str, sort_keys=True).encode("utf-8")).hexdigest()

    def counts():
        c_ = {}
        for ty in CLEAR_TYPES:
            try:
                c_[ty] = len(ac.api("API.GetElementsByType", {"elementType": ty}).get("elements", []))
            except Exception:
                c_[ty] = -1
        return c_
    now = counts()
    reuse = bool(old.get("build_sig") == sig and old.get("counts") == now and old.get("elements"))
    tp = time.time()
    made = []
    if reuse:
        made = list(old["elements"])
        CANOPY_REC[:] = old.get("canopies") or []
        log.append(u"model unchanged since %s (same inputs, %s): not rebuilt" % (
            old.get("run"), u", ".join(u"%d %s" % (now[k], k) for k in CLEAR_TYPES)))
    else:
        log.append(u"model inputs changed or counts differ: rebuilt")
        setup_materials(ac, log)                           # v1.18: his texture legend
        setup_composites(ac, log)                          # v1.44: composites per house type
        setup_override(ac, log)                            # v1.44: walls as one solid poche (override)
    old_items = [it for it in (old.get("items") or []) if isinstance(it, list) and len(it) == 3]
    gtype, n_stray = {}, 0                                # v1.34: guid -> type of every element in the model

    def del_typed(gs, what):
        """v1.34: delete these guids, windows and doors before walls (CLEAR_TYPES order)"""
        n_ = 0
        for ty in CLEAR_TYPES:
            g_ = [g for g in gs if gtype.get(g) == ty]
            for i in range(0, len(g_), CHUNK):
                try:
                    ac.t("DeleteElements", {"elements": [{"elementId": {"guid": g}} for g in g_[i:i + CHUNK]]})
                    n_ += len(g_[i:i + CHUNK])
                except Exception as ex:
                    log.append(u"FLAG %s: %s elements not all deleted (%s)" % (what, ty, ex))
                    break
        return n_
    if not reuse and "DeleteElements" not in miss:
        # v1.34: the model is kept; an element of the last pass whose data comes again is kept as it is. Elements
        # the last pass did not record (a recovery file with new GUIDs, v1.9; a model from before v1.34) are deleted
        try:
            ac.t("ChangeWindow", {"windowType": "FloorPlan", "storyIndex": 0})
        except Exception:
            pass
        listed = True
        for ty in CLEAR_TYPES:
            try:
                for e in ac.api("API.GetElementsByType", {"elementType": ty}).get("elements", []):
                    if e.get("elementId"):
                        gtype[e["elementId"]["guid"]] = ty
            except Exception as ex:
                listed = False
                log.append(u"FLAG %s elements not listed (%s)" % (ty, ex))
        if listed:
            # v1.44: AcBuild's elements are the ones with a BGA- Element ID (in the pln: any PC, any copy); all
            # others are Aras's and never touched; a shape moved since AcBuild made it = hand-edited = locked
            try:
                PID[0] = _pid(ac)
                ids_ = read_ids(ac, list(gtype), PID[0])
            except Exception as ex:
                raise RuntimeError(u"Element IDs not read (%s): stopped before changing anything (a pass without "
                                   u"them would make every element twice)" % ex)
            own = {}
            for g, t_ in ids_.items():
                pr = parse_id(t_)
                if pr:
                    own[g] = pr
            if PID[0] and not own and old_items:          # first v1.44 pass: this PC's record of the last pass
                ad_ = [(it[1], it[0]) for it in old_items if it[1] in gtype]
                n_ad = stamp(ac, PID[0], ad_) if ad_ else 0
                own = dict((g, (h[:16], None)) for g, h in ad_)
                log.append(u"model: %d element(s) recorded by this PC's last pass given their BGA- Element ID (%d "
                           u"written)" % (len(ad_), n_ad))
            bbs_ = read_bb(ac, [g for g, pr in own.items() if pr[1]]) if own else {}
            n_ed = 0
            for g, (h16, bb0) in own.items():
                bb1 = bbs_.get(g)
                if bb0 and bb1 and max(abs(a_ - b_) for a_, b_ in zip(bb0, bb1)) > EDIT_TOL_M:
                    LOCKED_BB.append((gtype[g], (bb1[0], bb1[1], bb1[3], bb1[4])))
                    n_ed += 1
                    continue
                KEEP.setdefault(h16, []).append(g)
            log.append(u"model: %d AcBuild element(s) found by their Element ID; %d hand-edited (shape moved more than "
                       u"%.2f m) locked: never deleted or replaced; %d other element(s) are yours and never touched" % (
                           len(own) - n_ed, n_ed, EDIT_TOL_M, len(gtype) - len(own)))
        else:
            log.append(u"FLAG the model could not be listed: every element is made again on top")
    z0 = 0.0
    try:
        st = ac.t("GetStories")
        z0 = next((s_["level"] for s_ in st.get("stories", []) if s_.get("index") == 0), 0.0)
    except Exception as ex:
        log.append(u"FLAG stories not read (%s): story 0 taken at 0.00" % ex)
    log.append(u"story 0 at %+.2f m: element heights are given relative to it" % z0)
    PV = list(old.get("plan_views") or []) if reuse else []      # v1.17: [(view, story, level, node, j)]
    if not reuse:
        try:
            PV = set_stories(ac, log, z0, node_stories(NB, z0))
        except Exception as ex:
            log.append(u"FLAG stories not set (%s): plans drawn by the node scripts" % ex)
            PV = []
    PVN = dict((v[0], v[1]) for v in PV)                 # plan view -> story name
    lay = {}
    try:
        ac.t("CreateLayers", {"layerDataArray": [{"name": n_} for n_ in LAYERS], "overwriteExisting": False})
    except Exception as ex:
        log.append(u"layers: %s (kept the existing ones)" % ex)
    try:
        for a in ac.t("GetAttributesByType", {"attributeType": "Layer"}).get("attributes", []):
            if a.get("name") in LAYERS:
                lay[a["name"]] = int(a["index"])
    except Exception as ex:
        log.append(u"FLAG layer indexes not read (%s): elements go on the tool default layers" % ex)
    L = lambda n_: {}      # v1.2: default layers (the BG layers were hidden in the section views)

    if not reuse:
        # ---- v1.31 (Aras 21:19-21:20 "ground has gaps", "it all should be one large block", "with many control
        # points on it"); v1.32 (the v1.31 publish stalled): the one ground surface in GROUND_TILE_M tiles whose edge
        # points are the same on both sides (no gap), only tiles that touch a cut rectangle or the river
        gb = (box[0] + 1.0, box[1] + 1.0, box[2] - 1.0, box[3] - 1.0)
        zlo = min(p[2] for p in pts)
        base = zlo - z0 - GROUND_BASE_M + 1.0              # mesh level; every point at least 1 m above it

        def zr(z):
            return round(z - z0 - base, 3)

        def zat(c):
            z = tin.z(c[0] - ox, c[1] - oy)
            if z is None:
                z = min(pts, key=lambda p: (p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2)[2]
            return z
        spot = {}
        for p in pts:
            spot.setdefault((int(p[0] // GROUND_SPOT_M), int(p[1] // GROUND_SPOT_M)), p)
        spot = list(spot.values())
        have_ = set((int(p[0] // GROUND_GRID_M), int(p[1] // GROUND_GRID_M)) for p in spot)
        rpip_ = [_pip_fast(R) for R in SEL.get("river") or [] if len(R) >= 3]   # v1.38: under the river

        def strip_(q):                                    # v1.38: what a cut sees cut, not the hills behind it
            for nm_, A_, B_, Ln_, u_, n_ in rects:
                s_, o_ = so(q, A_, u_, n_)
                if -1.0 <= s_ <= Ln_ + 1.0 and -SIDE_M <= o_ <= GROUND_BEHIND_M:
                    return True
            return any(f_(q) for f_ in rpip_)
        T = SITE_TILE_M if WHOLE_SITE else GROUND_TILE_M
        tk_ = lambda p: (int((p[0] - gb[0]) // T), int((p[1] - gb[1]) // T))
        spot_ix, cont_ix = {}, {}                         # v1.42: survey heights and contour runs per tile
        for p in spot:
            spot_ix.setdefault(tk_(p), []).append(p)
        for pl in contours:
            run, k0 = [], None
            for p in pl:
                k1 = tk_(p)
                if k1 != k0 and run:
                    cont_ix.setdefault(k0, []).append(run)
                    run = []
                run.append(p)
                k0 = k1
            if run:
                cont_ix.setdefault(k0, []).append(run)
        PEND, CNT, TILE_IX = [], [0, 0, 0], {}

        def flush_():
            if not PEND:
                return
            gl = ac.create("CreateMeshes", "meshesData", [t_[0] for t_ in PEND],
                           u"ground tiles from %d,%d" % (PEND[0][5], PEND[0][6]))
            for (m, sub, nsc, nc, bb4, i, j), g0 in zip(PEND, gl):
                g = [g0]
                if not g0:                                # retry with the contour lines only
                    m["sublines"] = [s_ for s_ in sub if len(s_["coordinates"]) >= 2] or sub[:1]
                    g = ac.create("CreateMeshes", "meshesData", [m], u"ground tile %d,%d, contours only" % (i, j))
                made.extend(x for x in g if x)
                SEO_TERR.extend((x, ("tile",) + bb4) for x in g if x)
                for x in g:
                    if x:
                        TILE_IX.setdefault((i, j), []).append(x)
                CNT[0] += 1
                CNT[1] += len(sub) - nsc - nc
                CNT[2] += nc
            del PEND[:]
        nxt, nyt = int(math.ceil((gb[2] - gb[0]) / T)), int(math.ceil((gb[3] - gb[1]) / T))
        n_t = n_pts = n_ctl = 0
        for i in range(nxt):
            for j in range(nyt):
                x0, y0 = gb[0] + i * T, gb[1] + j * T
                x1, y1 = min(gb[2], x0 + T), min(gb[3], y0 + T)
                inb = lambda p, x0=x0, y0=y0, x1=x1, y1=y1: x0 <= p[0] <= x1 and y0 <= p[1] <= y1
                smp = [(x0 + (x1 - x0) * a / 6.0, y0 + (y1 - y0) * b / 6.0) for a in range(7) for b in range(7)]
                if WHOLE_SITE:                            # v1.42: wherever the survey has heights
                    if not spot_ix.get((i, j)) and not cont_ix.get((i, j)):
                        # v1.44 (Aras 16 Nov 11:12 "i dont want any gaps in the topography": v1.42/1.43 left out the
                        # 50 m tiles with no survey point of their own, along the river and in the east): such a tile
                        # is built too wherever the survey triangulation covers any part of it (heights from it)
                        if not any(tin.z(q[0] - ox, q[1] - oy) is not None for q in smp):
                            continue
                        N_TINONLY[0] += 1
                elif not any(strip_(q) for q in smp):
                    continue
                poly = []
                for (ax, ay), (bx_, by_) in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)),
                                              ((x0, y1), (x0, y0))):
                    L_ = math.hypot(bx_ - ax, by_ - ay)
                    k_n = max(1, int(round(L_ / GROUND_EDGE_M)))
                    for k_ in range(k_n):                  # the same edge points as the neighbouring tile
                        c = (ax + (bx_ - ax) * k_ / k_n, ay + (by_ - ay) * k_ / k_n)
                        poly.append(dict(xy(c), z=zr(zat(c))))
                sub = []
                for run in (cont_ix.get((i, j)) or []) if WHOLE_SITE else (
                        [p for p in pl if x0 < p[0] < x1 and y0 < p[1] < y1] for pl in contours):
                    run = [p for p in run if x0 < p[0] < x1 and y0 < p[1] < y1]
                    if len(run) >= 2:
                        sub.append({"coordinates": [dict(xy(p), z=zr(p[2])) for p in run]})
                nsc = len(sub)
                sub += [{"coordinates": [dict(xy(p), z=zr(p[2]))]} for p in (spot_ix.get((i, j)) or [] if WHOLE_SITE
                                                                              else spot) if x0 < p[0] < x1 and y0 < p[1] < y1]
                gx = x0 + GROUND_GRID_M / 2
                nc = 0
                while gx < x1:
                    gy = y0 + GROUND_GRID_M / 2
                    while gy < y1:
                        if (int(gx // GROUND_GRID_M), int(gy // GROUND_GRID_M)) not in have_:
                            z = tin.z(gx - ox, gy - oy)
                            if z is not None:
                                sub.append({"coordinates": [dict(xy((gx, gy)), z=zr(z))]})
                                nc += 1
                        gy += GROUND_GRID_M
                    gx += GROUND_GRID_M
                m = dict(level=round(base, 3), polygonCoordinates=poly, sublines=sub, skirtType="SolidBodyWithSkirt",
                         skirtLevel=GROUND_BASE_M, ridges="AllSmooth", _mat="ground")
                if not MESH or "CreateMeshes" in miss:
                    continue
                PEND.append((m, sub, nsc, nc, (x0, y0, x1, y1), i, j))    # v1.42: made in batches
                if len(PEND) >= (SITE_BATCH if WHOLE_SITE else 1):
                    flush_()
        flush_()
        n_t, n_pts, n_ctl = CNT
        log.append(u"ground: %d tile(s) with no survey point of their own filled from the survey triangulation (no gaps)" % N_TINONLY[0])
        log.append(u"ground: %d tiles of %.0f m sharing their edge points (one surface, no gaps), %d survey heights "
                   u"(one per %.0f m), %d control points (every %.0f m where none), block %.1f m under its lowest "
                   u"point (%.1f m)" % (n_t, T, n_pts, GROUND_SPOT_M, n_ctl, GROUND_GRID_M, GROUND_BASE_M, zlo))

        # ---- walls (+ windows on the walls a cut looks at)
        walls, wmeta = [], []
        for bi, b in enumerate(bld):
            top_extra = 0.6 if b["fl"] >= FLAT_FLOORS else 0.0
            R = b["ring"]
            for a, c in zip(R, R[1:] + R[:1]):
                ln = math.hypot(c[0] - a[0], c[1] - a[1])
                if ln < 0.3:
                    continue
                on = ((c[1] - a[1]) / ln, -(c[0] - a[0]) / ln)        # outward normal (ring counter-clockwise)
                faces = b["fl"] > 0 and any(on[0] * -r[5][0] + on[1] * -r[5][1] > 0.05 for r in b["views"])
                if b["fl"] < 0:                       # the hall: one wall, into the ground
                    flr_ = [(None, b["z"] - PLINTH, b["h"] + PLINTH + top_extra)]
                else:                                 # v1.44: one wall per storey, on the raft / floor slab
                    fh0 = b["h"] / b["fl"]
                    flr_ = [(k_, b["z"] + k_ * fh0, fh0 + (top_extra if k_ == b["fl"] - 1 else 0.0)) for k_ in range(b["fl"])]
                for k_, zb_, hh_ in flr_:
                    walls.append(dict(begCoordinate=xy(a), endCoordinate=xy(c), zCoordinate=round(zb_ - z0, 3),
                                      height=round(hh_, 3), thickness=_wt(b), referenceLineLocation="Outside",
                                      _mat="heritage_red" if b["fab"] in HERITAGE_FABS else None,
                                      **dict(_wcomp(b), **L("BG buildings"))))
                    wmeta.append((bi, ln, faces, a, c, on, k_))
        wg = ac.create("CreateWalls", "wallsData", walls, u"walls") if "CreateWalls" not in miss else []
        made += [g for g in wg if g]
        n_wsub = 0
        for g, mt, w_ in zip(wg, wmeta, walls):              # v1.31: the hall; v1.44: every wall whose foot is buried
            if not g:
                continue
            zg_ = [tin.z(q["x"], q["y"]) for q in (w_["begCoordinate"], w_["endCoordinate"])]
            if bld[mt[0]]["fl"] < 0 or any(z_ is not None and z_ > w_["zCoordinate"] + z0 + 0.02 for z_ in zg_):
                EXTRA_OPS.append((g, "Subtraction", [w_["begCoordinate"], w_["endCoordinate"]]))
                n_wsub += 1
        log.append(u"SEO: %d house / hall wall(s) with their foot under the surveyed ground cut it" % n_wsub)
        wins, doors, bals, rails = [], [], [], []
        door_wall = {}                                # v1.14: per building the longest wall a cut sees gets the door
        for g, (bi, ln, faces, a_, c_, on_, k_) in zip(wg, wmeta):
            if g and faces and k_ in (0, None) and ln >= DOOR_W + 2.0 and ln > door_wall.get(bi, (None, 0.0))[1]:
                door_wall[bi] = (g, ln)
        for g, (bi, ln, faces, a_, c_, on_, k_) in zip(wg, wmeta):
            if not g or not faces or ln < WIN_W + 1.0:
                continue
            b = bld[bi]
            fh = b["h"] / b["fl"]
            nw = max(1, int((ln - 1.0) // WIN_STEP))
            x0 = (ln - (nw - 1) * WIN_STEP) / 2.0
            has_door = door_wall.get(bi, (None,))[0] == g
            if has_door:
                doors.append(dict(ownerWallId={"guid": g}, width=DOOR_W, height=DOOR_H, sillHeight=0.0,
                                  centerOffset=round(ln / 2.0, 2)))
            u_ = ((c_[0] - a_[0]) / ln, (c_[1] - a_[1]) / ln)
            for i in ([k_] if k_ is not None else range(b["fl"])):   # v1.44: this storey's wall only
                for j in range(nw):
                    xo = x0 + j * WIN_STEP
                    if i == 0 and has_door and abs(xo - ln / 2.0) < (DOOR_W + WIN_W) / 2.0 + 0.3:
                        continue                      # the door's place on the ground floor
                    wins.append(dict(ownerWallId={"guid": g}, width=WIN_W, height=round(min(WIN_H, fh * 0.5), 2),
                                     sillHeight=round((0 if k_ is not None else i * fh) + min(WIN_SILL, fh * 0.3), 2),
                                     centerOffset=round(xo, 2)))
                    if b["fl"] >= BAL_FLOORS and i >= 1 and j % 2 == 0 and ln >= BAL_W + 1.0:
                        lv = round(b["z"] + i * fh - z0, 3)   # v1.14: a balcony on this window bay
                        m_ = (a_[0] + u_[0] * xo, a_[1] + u_[1] * xo)
                        p1 = (m_[0] - u_[0] * BAL_W / 2, m_[1] - u_[1] * BAL_W / 2)
                        p2 = (m_[0] + u_[0] * BAL_W / 2, m_[1] + u_[1] * BAL_W / 2)
                        q1 = (p1[0] + on_[0] * BAL_D, p1[1] + on_[1] * BAL_D)
                        q2 = (p2[0] + on_[0] * BAL_D, p2[1] + on_[1] * BAL_D)
                        bals.append(dict(level=lv, thickness=BAL_T, polygonCoordinates=[xy(p1), xy(p2), xy(q2), xy(q1)],
                                         **L("BG buildings")))
                        for e0, e1 in ((p1, q1), (q1, q2), (q2, p2)):
                            rails.append(dict(begCoordinate=xy(e0), endCoordinate=xy(e1), zCoordinate=lv,
                                              height=RAIL_H, thickness=0.05, referenceLineLocation="Center",
                                              **L("BG buildings")))
        if wins and "CreateWindows" not in miss:
            made += [g for g in ac.create("CreateWindows", "windowsData", wins, u"windows (walls facing a cut)") if g]
        if doors and ac.has("CreateDoors"):           # v1.14
            made += [g for g in ac.create("CreateDoors", "doorsData", doors, u"ground-floor doors") if g]
        elif doors:
            log.append(u"FLAG Tapir has no CreateDoors: %d ground-floor doors not made (update Tapir)" % len(doors))
        if bals and "CreateSlabs" not in miss:
            made += [g for g in ac.create("CreateSlabs", "slabsData", bals, u"balcony slabs (blocks of %d+ floors)"
                                          % BAL_FLOORS) if g]
        if rails and "CreateWalls" not in miss:
            made += [g for g in ac.create("CreateWalls", "wallsData", rails, u"balcony rails") if g]
        log.append(u"house detail (drawing rules, not surveyed): %d doors, %d windows, %d balconies; %d houses with no "
                   u"floor count built as 1 floor (ASSUMED)" % (len(doors), len(wins), len(bals), skipped))

        # ---- roofs and slabs
        roofs, flats, slabs = [], [], []
        ground_i, flats_n = [], []                    # v1.31
        for b in bld:
            if b["fl"] < 0:
                continue                              # Kızıl Avlu: the roofless Roman hall
            poly = [xy(q) for q in b["ring"]]
            top = round(b["z"] + b["h"] - z0, 3)
            if b["fl"] >= FLAT_FLOORS:
                # v1.28 (Aras 20:10 "give both slabs and roofs to every building"): the flat roof is a Roof-tool
                # single-plane roof, FLAT_ROOF_DEG fall from its longest edge (a slab only if Archicad refuses it)
                R0 = b["ring"]
                ka = max(range(len(R0)), key=lambda k_: math.hypot(R0[(k_ + 1) % len(R0)][0] - R0[k_][0],
                                                                   R0[(k_ + 1) % len(R0)][1] - R0[k_][1]))
                roofs.append(dict(level=top, polygonCoordinates=poly, **_ccomp("roof_flat", 0.3, "Basic"),
                                  pivotLine=dict(begCoordinate=xy(R0[ka]), endCoordinate=xy(R0[(ka + 1) % len(R0)])),
                                  angle=round(math.radians(FLAT_ROOF_DEG), 5)))
                R_ = b["ring"]                        # v1.14: a cornice band, the footprint pushed out CORNICE_M
                cor = []
                for k_ in range(len(R_)):
                    a2, v2, c2 = R_[k_ - 1], R_[k_], R_[(k_ + 1) % len(R_)]
                    l1, l2 = math.hypot(v2[0] - a2[0], v2[1] - a2[1]) or 1e-9, math.hypot(c2[0] - v2[0], c2[1] - v2[1]) or 1e-9
                    n1 = ((v2[1] - a2[1]) / l1, -(v2[0] - a2[0]) / l1)
                    n2 = ((c2[1] - v2[1]) / l2, -(c2[0] - v2[0]) / l2)
                    nx_, ny_ = n1[0] + n2[0], n1[1] + n2[1]
                    d_ = nx_ * n1[0] + ny_ * n1[1]
                    f_ = CORNICE_M / d_ if d_ > 0.3 else CORNICE_M
                    cor.append(xy((v2[0] + nx_ * f_, v2[1] + ny_ * f_)))
                flats.append(dict(level=round(top - CORNICE_T, 3), thickness=CORNICE_T, polygonCoordinates=cor,
                                  **L("BG buildings")))
            else:
                roofs.append(dict(level=top, polygonCoordinates=poly, eavesOverhang=EAVE_M, **dict(_ccomp("roof_tile", 0.25)),
                                  levels=[{"levelHeight": 20.0, "levelAngle": math.radians(ROOF_DEG)}]))   # polyroof (hip)
            fh = b["h"] / b["fl"]                     # v1.28 (Aras 20:10): a floor slab per storey in EVERY building
            # v1.44: the ground-floor slab is the raft: down to RAFT_T_M under the lowest ground under the footprint
            R0 = b["ring"]
            smp_ = list(R0) + [((R0[k_][0] + R0[k_ - 1][0]) / 2.0, (R0[k_][1] + R0[k_ - 1][1]) / 2.0)
                               for k_ in range(len(R0))] + [(sum(q[0] for q in R0) / len(R0), sum(q[1] for q in R0) / len(R0))]
            zg_ = [z_ for z_ in (tin.z(q[0] - ox, q[1] - oy) for q in smp_) if z_ is not None]
            zlo_ = min(zg_ + [b["z"]])
            N_RAFT[0] += 1
            N_RAFT[1] = max(N_RAFT[1], b["z"] - zlo_)
            slabs += [dict(level=round(b["z"] - z0, 3), thickness=round(b["z"] - zlo_ + RAFT_T_M, 3),
                           polygonCoordinates=poly, _mat=u"heritage_red" if b["fab"] in HERITAGE_FABS else u"rc",
                           **L("BG buildings"))]
            slabs += [dict(level=round(b["z"] + i * fh - z0, 3), polygonCoordinates=poly,
                           **dict(_ccomp("floor_rc", 0.25), **L("BG buildings"))) for i in range(1, b["fl"])]
            ground_i.append(len(flats_n) + len(slabs) - b["fl"])     # v1.31: index of its ground slab in slabs
        log.append(u"raft foundations: %d houses, top = ground floor (survey ground at the centroid), bottom %.2f m "
                   u"(ASSUMED) under the lowest survey ground under the footprint (deepest step %.2f m); each cuts the "
                   u"ground upwards (SEO)" % (N_RAFT[0], RAFT_T_M, N_RAFT[1]))
        if "CreateRoofs" not in miss and roofs:
            rg = ac.create("CreateRoofs", "roofsData", roofs, u"roofs (hipped + flat single-plane)")
            made += [g for g in rg if g]
            bad_ = [i_ for i_, g in enumerate(rg) if not g]   # v1.43: again as a single-plane Roof-tool roof
            if bad_:
                r2_ = []
                for i_ in bad_:
                    pc_ = roofs[i_]["polygonCoordinates"]
                    ka = max(range(len(pc_)), key=lambda k_: math.hypot(pc_[(k_ + 1) % len(pc_)]["x"] - pc_[k_]["x"],
                                                                       pc_[(k_ + 1) % len(pc_)]["y"] - pc_[k_]["y"]))
                    r2_.append(dict(level=roofs[i_]["level"], thickness=0.3, structureType="Basic", polygonCoordinates=pc_,
                                    pivotLine=dict(begCoordinate=pc_[ka], endCoordinate=pc_[(ka + 1) % len(pc_)]),
                                    angle=round(math.radians(FLAT_ROOF_DEG), 5)))
                g2_ = ac.create("CreateRoofs", "roofsData", r2_, u"roofs refused as hipped: single-plane Roof tool")
                for i_, g in zip(bad_, g2_):
                    if g:
                        rg[i_] = g
                        made.append(g)
            flats += [dict(level=r_["level"], thickness=0.3, polygonCoordinates=r_["polygonCoordinates"],
                           **L("BG buildings")) for r_, g in zip(roofs, rg) if not g]   # a roof Archicad refused: flat
        if "CreateSlabs" not in miss:
            gs_ = ac.create("CreateSlabs", "slabsData", flats + slabs, u"flat roofs + cut floor slabs")
            made += [g for g in gs_ if g]
            gsl_ = gs_[len(flats):]                   # v1.31: each building's ground slab cuts the ground above it
            sl_ = (flats + slabs)[len(flats):]
            EXTRA_OPS.extend((gsl_[i], "SubtractionUpwards", sl_[i]["polygonCoordinates"]) for i in ground_i
                             if 0 <= i < len(gsl_) and gsl_[i])

        # ---- v1.44 (Aras 11:18 "those rafts should connect columns and that columns should be connected by beams"):
        # a frame in every framed house: columns on the raft, beams under every floor slab and the roof
        fcols, fbeams, n_fh, n_fskip = [], [], 0, 0
        for b in bld:
            if b["fl"] <= 0 or b["fab"] in HERITAGE_FABS or b["fab"] in FRAME_SKIP_FABS:
                n_fskip += 1                          # masonry: the Roman hall, sacred and monument buildings
                continue
            R0 = b["ring"]
            n0_ = len(R0)
            Ri = []                                   # the footprint pulled in half a wall: the frame's centre line
            for k_ in range(n0_):
                a2, v2, c2 = R0[k_ - 1], R0[k_], R0[(k_ + 1) % n0_]
                l1 = math.hypot(v2[0] - a2[0], v2[1] - a2[1]) or 1e-9
                l2 = math.hypot(c2[0] - v2[0], c2[1] - v2[1]) or 1e-9
                n1 = ((v2[1] - a2[1]) / l1, -(v2[0] - a2[0]) / l1)
                n2 = ((c2[1] - v2[1]) / l2, -(c2[0] - v2[0]) / l2)
                nx_, ny_ = n1[0] + n2[0], n1[1] + n2[1]
                d_ = nx_ * n1[0] + ny_ * n1[1]
                f_ = (_wt(b) / 2.0) / d_ if d_ > 0.3 else _wt(b) / 2.0
                Ri.append((v2[0] - nx_ * f_, v2[1] - ny_ * f_))
            if abs(area(Ri)) < 4.0:
                continue
            ka = max(range(n0_), key=lambda k_: math.hypot(Ri[(k_ + 1) % n0_][0] - Ri[k_][0], Ri[(k_ + 1) % n0_][1] - Ri[k_][1]))
            ex_, ey_ = Ri[(ka + 1) % n0_][0] - Ri[ka][0], Ri[(ka + 1) % n0_][1] - Ri[ka][1]
            le_ = math.hypot(ex_, ey_) or 1e-9
            U_ = (ex_ / le_, ey_ / le_)
            W_ = (-U_[1], U_[0])
            o_ = Ri[ka]
            cT = lambda p: (p[0] - o_[0]) * U_[0] + (p[1] - o_[1]) * U_[1]
            cW = lambda p: (p[0] - o_[0]) * W_[0] + (p[1] - o_[1]) * W_[1]
            at_ = lambda t, w: (o_[0] + U_[0] * t + W_[0] * w, o_[1] + U_[1] * t + W_[1] * w)
            cp_ = list(Ri)                            # column points: corners, grid hits, grid crossings
            segs_ = [(Ri[k_], Ri[(k_ + 1) % n0_]) for k_ in range(n0_)]
            fam = []
            for crd, alo in ((cW, cT), (cT, cW)):     # grid lines along U (at w = c) and along W (at t = c)
                vs = [crd(p) for p in Ri]
                cs, c_ = [], min(vs) + FRAME_SP_M
                while c_ < max(vs) - 0.5:
                    cs.append(c_)
                    c_ += FRAME_SP_M
                fam.append(cs)
                for c_ in cs:
                    hit = []
                    for p, q in segs_:
                        vp, vq = crd(p), crd(q)
                        if (vp - c_) * (vq - c_) < 0:
                            r_ = (c_ - vp) / (vq - vp)
                            hit.append((p[0] + (q[0] - p[0]) * r_, p[1] + (q[1] - p[1]) * r_))
                    hit.sort(key=alo)
                    cp_ += hit
                    for k_ in range(0, len(hit) - 1, 2):
                        segs_.append((hit[k_], hit[k_ + 1]))
            for w_ in fam[0]:
                for t_ in fam[1]:
                    p = at_(t_, w_)
                    if _inpoly(p, Ri) and min(_seg_d(p, a_, c_) for a_, c_ in zip(Ri, Ri[1:] + Ri[:1])) > 0.5:
                        cp_.append(p)
            uq = []
            for p in cp_:
                if all(math.hypot(p[0] - q[0], p[1] - q[1]) > 0.5 for q in uq):
                    uq.append(p)
            n_fh += 1
            fhc_ = b["h"] / b["fl"]                   # v1.44: one column per storey, slab top to the slab above
            fcols += [dict(coordinates=dict(xy(p), z=round(b["z"] + k_ * fhc_ - z0, 3)), height=round(fhc_ - 0.25, 3),
                           circleBased=False, width=FRAME_COL_M, depth=FRAME_COL_M, _mat="rc")
                      for k_ in range(b["fl"]) for p in uq]
            fh_ = b["h"] / b["fl"]
            spans_ = []                               # v1.44 (Aras 11:37 "single beam travelling all across the grid"):
            for p, q in segs_:                        # every beam line split at each column on it: one beam per span
                Lq = math.hypot(q[0] - p[0], q[1] - p[1])
                if Lq < 0.3:
                    continue
                ts_ = sorted(set([0.0, 1.0] + [round(((c_[0] - p[0]) * (q[0] - p[0]) + (c_[1] - p[1]) * (q[1] - p[1])) / (Lq * Lq), 4)
                                               for c_ in uq if _seg_d(c_, p, q) < 0.05]))
                ts_ = [t_ for t_ in ts_ if 0.0 <= t_ <= 1.0]
                for t0_, t1_ in zip(ts_, ts_[1:]):
                    if (t1_ - t0_) * Lq >= 0.3:
                        spans_.append(((p[0] + (q[0] - p[0]) * t0_, p[1] + (q[1] - p[1]) * t0_),
                                       (p[0] + (q[0] - p[0]) * t1_, p[1] + (q[1] - p[1]) * t1_)))
            for i in range(1, b["fl"] + 1):           # under each floor slab and under the roof
                zt_ = round(b["z"] + i * fh_ - 0.25 - z0, 3)
                fbeams += [dict(begCoordinate=xy(p), endCoordinate=xy(q), zCoordinate=zt_, width=FRAME_BEAM_W,
                                height=FRAME_BEAM_H, _mat="rc") for p, q in spans_]
        if fcols and "CreateColumns" not in miss:
            t_ = ac.create("CreateColumns", "columnsData", fcols[:1], u"house frame columns (square test)")
            if not t_[0]:                             # Tapir took no square column: round ones of the same width
                log.append(u"FLAG house frame: square columns refused, made round (diameter %.2f m)" % FRAME_COL_M)
                fcols = [dict(((k_, v_) for k_, v_ in c_.items() if k_ != "depth"), circleBased=True) for c_ in fcols]
                made += [g for g in ac.create("CreateColumns", "columnsData", fcols, u"house frame columns (Column tool)") if g]
            else:
                made += [g for g in t_ if g]
                made += [g for g in ac.create("CreateColumns", "columnsData", fcols[1:], u"house frame columns (Column tool)")
                         if g]
        if fbeams and "CreateBeams" not in miss:
            made += [g for g in ac.create("CreateBeams", "beamsData", fbeams, u"house frame beams (Beam tool)") if g]
        log.append(u"house frames: %d houses, %d columns (%.2f m square, one per storey, slab to slab), %d beams (one per span) (%.2f x %.2f m "
                   u"under every floor slab and the roof, along the footprint and the %.1f m grid); sizes and grid ASSUMED; "
                   u"%d masonry (traditional, sacred, monument, Kizil Avlu) buildings without a frame" % (
                       n_fh, len(fcols), FRAME_COL_M, len(fbeams), FRAME_BEAM_W, FRAME_BEAM_H, FRAME_SP_M, n_fskip))

        # ---- v1.6 canopies (Q500 and the low water of the nearest cut, from the Sections cache)
        try:
            with open(os.path.join(BERGAMA_ROOT, "cached", "bergama_sections", "cuts.json"), encoding="utf-8") as f:
                CJ_ = json.load(f).get("cuts", {})
        except Exception:
            CJ_ = {}

        def near_cut(x, y):
            best = None
            for name, A, B, Ln, u, n in rects:
                s_, o_ = so((x, y), A, u, n)
                d_ = abs(o_) + max(0.0, -s_, s_ - Ln)
                if name in CJ_ and CJ_[name].get("levels") and (best is None or d_ < best[0]):
                    best = (d_, name)
            return CJ_[best[1]]["levels"] if best else {}

        def q500_at(x, y):
            lv = near_cut(x, y).get("q500")
            return lv[0] if lv else None

        def wet_at(x, y, g):
            lv = [v[0] for v in near_cut(x, y).values() if isinstance(v, list) and v and v[0] is not None]
            return bool(lv) and g < min(lv) + 0.3

        try:
            made += build_canopies(ac, miss, log, rects, inside, tin, ox, oy, z0, xy, q500_at, wet_at)
        except Exception as ex:
            import traceback
            log.append(u"FLAG canopies not built (%s: %s) %s" % (type(ex).__name__, ex, traceback.format_exc()[-400:]))
        try:                                              # v1.16: his masterplan pieces on his points
            made += build_site(ac, miss, log, xy, z0, tin, ox, oy, [p for p in SP if p[0] not in ("rock", "su_bitkii")])
            site_accuracy(ac, log, ox, oy)                # v1.16: read back + compare, FLAG over 5 cm
        except Exception as ex:
            import traceback
            log.append(u"FLAG masterplan pieces not built (%s: %s) %s" % (type(ex).__name__, ex,
                                                                          traceback.format_exc()[-400:]))
        try:                                              # v1.29: the whole Selinos
            made += build_selinos(ac, miss, log, xy, z0, tin, ox, oy, rects, inside, contours, pts, CJ_,
                                  [p for p in SP if p[0] in ("rock", "su_bitkii")])
        except Exception as ex:
            import traceback
            log.append(u"FLAG Selinos not built (%s: %s) %s" % (type(ex).__name__, ex, traceback.format_exc()[-400:]))
        try:                                              # v1.44: the survey stairs
            made += build_survey_stairs(ac, miss, log, xy, z0, tin, ox, oy, survey.get("_stairs") or [])
        except Exception as ex:
            import traceback
            log.append(u"FLAG survey stairs not built (%s: %s) %s" % (type(ex).__name__, ex, traceback.format_exc()[-400:]))
        try:                                              # v1.44: the survey trees
            made += build_survey_trees(ac, miss, log, xy, z0, tin, ox, oy, survey, bld)
        except Exception as ex:
            import traceback
            log.append(u"FLAG survey trees not built (%s: %s) %s" % (type(ex).__name__, ex, traceback.format_exc()[-400:]))
        try:                                              # v1.30: roads, parks, kerbs, walls
            made += build_town(ac, miss, log, xy, z0, tin, ox, oy, rects, inside)
        except Exception as ex:
            import traceback
            log.append(u"FLAG town ground not built (%s: %s) %s" % (type(ex).__name__, ex, traceback.format_exc()[-400:]))
        try:                                              # v1.14: the node buildings
            made += build_nodes(ac, miss, log, xy, z0, NB)
        except Exception as ex:
            import traceback
            log.append(u"FLAG node buildings not built (%s: %s) %s" % (type(ex).__name__, ex,
                                                                       traceback.format_exc()[-400:]))

        # ---- registration blocks: s = 0 (0.4 m) and s = L (0.8 m), REG_Z ... REG_Z + 0.5
        regs = []
        for name, A, B, Ln, u, n in rects:
            for s, w in ((0.0, 0.4), (Ln, 0.8)):
                c = (A[0] + u[0] * s, A[1] + u[1] * s)
                sq = [(c[0] + (u[0] * a_ + n[0] * b_) * w / 2, c[1] + (u[1] * a_ + n[1] * b_) * w / 2)
                      for a_, b_ in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
                regs.append(dict(level=round(REG_Z + 0.5 - z0, 3), thickness=0.5, polygonCoordinates=[xy(q) for q in sq],
                                 **L("BG reg")))
        # v1.14: the building views' own blocks, told apart by shape: 1.0 m tall (the river cuts' are 0.5 m), whole
        # inside the line: 0.4 m wide centred at s = 0.5 m, 0.8 m wide centred at s = L - 0.5 m, bottoms at REG_Z + 3
        for name, A, B, dp in BSECS:
            Ln, u, n = frame(A, B)
            for s, w in ((NB_REG_IN, 0.4), (Ln - NB_REG_IN, 0.8)):
                c = (A[0] + u[0] * s, A[1] + u[1] * s)
                sq = [(c[0] + (u[0] * a_ + n[0] * b_) * w / 2, c[1] + (u[1] * a_ + n[1] * b_) * w / 2)
                      for a_, b_ in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
                regs.append(dict(level=round(REG_Z + NB_REG_DZ + NB_REG_H - z0, 3), thickness=NB_REG_H,
                                 polygonCoordinates=[xy(q) for q in sq], **L("BG reg")))
        # v1.17: the plan views' squares on each building story: 1.0 m at (-L/2 - 6, -D/2 - 6), 0.5 m at (L/2 + 6,
        # D/2 + 6) in the building's own frame (u along, w across), sides along u and w
        NBD = dict((b["node"], b) for b in NB)
        for vn, stn, lv, nd, j in PV:
            b = NBD.get(nd)
            if not b:
                continue
            c, u, w, L_, D_ = b["c"], b["u"], b["w"], b["L"], b["D"]
            for sg, a_ in ((-1, NB_PREG_A[0]), (1, NB_PREG_A[1])):
                t0, s0 = sg * (L_ / 2 + NB_PREG_M), sg * (D_ / 2 + NB_PREG_M)
                sq = [(c[0] + u[0] * (t0 + da * a_ / 2) + w[0] * (s0 + db * a_ / 2),
                       c[1] + u[1] * (t0 + da * a_ / 2) + w[1] * (s0 + db * a_ / 2))
                      for da, db in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
                regs.append(dict(level=round(lv + 0.3, 3), thickness=0.3, polygonCoordinates=[xy(q) for q in sq],
                                 **L("BG reg")))
        if "CreateSlabs" not in miss:
            made += [g for g in ac.create("CreateSlabs", "slabsData", regs, u"registration blocks") if g]

    if not reuse and SEO_OPS and "CreateWalls" not in miss:
        # v1.27 (Aras 15 Nov 20:08 "use retaining walls where neccesery"): along every edge of a plinth, terrace or
        # masterplan slab where the surveyed ground just outside differs from the slab top by more than RET_MIN_M,
        # a stone retaining wall (RET_T_M thick, footing RET_FOOT_M below the lower side), in 4 m pieces that follow
        # the ground; edges that meet another slab are left open
        OPS = [(g_, [(q[0] + ox, q[1] + oy) for q in P_], lv_) for g_, P_, lv_ in SEO_OPS]   # survey coordinates
        boxes = [(min(q[0] for q in P), min(q[1] for q in P), max(q[0] for q in P), max(q[1] for q in P))
                 for _g, P, _lv in OPS]
        rw, rw_d = [], []
        for i_, (og, P, lv) in enumerate(OPS):
            if lv is None or len(P) < 3 or not any(inside(q, r) for q in P for r in rects):
                continue
            for a, b in zip(P, P[1:] + P[:1]):
                L_ = math.hypot(b[0] - a[0], b[1] - a[1])
                if L_ < 0.5:
                    continue
                nx, ny = -(b[1] - a[1]) / L_, (b[0] - a[0]) / L_
                mx, my = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
                if _inpoly((mx + nx * 0.5, my + ny * 0.5), P):
                    nx, ny = -nx, -ny                      # outward
                for k_ in range(max(1, int(math.ceil(L_ / RET_SEG_M)))):
                    f0, f1 = k_ / math.ceil(L_ / RET_SEG_M), (k_ + 1) / math.ceil(L_ / RET_SEG_M)
                    p0 = (a[0] + (b[0] - a[0]) * f0, a[1] + (b[1] - a[1]) * f0)
                    p1 = (a[0] + (b[0] - a[0]) * f1, a[1] + (b[1] - a[1]) * f1)
                    o = ((p0[0] + p1[0]) / 2.0 + nx * 0.6, (p0[1] + p1[1]) / 2.0 + ny * 0.6)
                    if any(j_ != i_ and bx[0] <= o[0] <= bx[2] and bx[1] <= o[1] <= bx[3] and _inpoly(o, OPS[j_][1])
                           for j_, bx in enumerate(boxes)):
                        continue                           # another slab there, no wall
                    gz_ = tin.z(o[0] - ox, o[1] - oy)
                    if gz_ is None:
                        continue
                    gz_ -= z0
                    if abs(gz_ - lv) <= RET_MIN_M:
                        continue
                    lo_, hi_ = min(gz_, lv) - RET_FOOT_M, max(gz_, lv)
                    sh = RET_T_M / 2.0
                    rw.append(dict(begCoordinate=xy((p0[0] + nx * sh, p0[1] + ny * sh)),
                                   endCoordinate=xy((p1[0] + nx * sh, p1[1] + ny * sh)), zCoordinate=round(lo_, 3),
                                   height=round(hi_ - lo_, 3), thickness=RET_T_M, referenceLineLocation="Center"))
                    rw_d.append(dict(polygonCoordinates=[xy(p0), xy(p1), xy((p1[0] + nx * RET_T_M, p1[1] + ny * RET_T_M)),
                                                         xy((p0[0] + nx * RET_T_M, p0[1] + ny * RET_T_M))], level=None))
        if rw:
            gw = ac.create("CreateWalls", "wallsData", rw, u"retaining walls (stone, %.2f m)" % RET_T_M)
            made += [g for g in gw if g]
            _reg_ops(gw, rw_d)                             # they cut the terrain too
            log.append(u"retaining walls: %d pieces where the ground outside a slab is more than %.2f m above or below "
                       u"its top (threshold ASSUMED: the 600 mm drop at which Approved Document K asks for guarding)"
                       % (sum(1 for g in gw if g), RET_MIN_M))
    dead_bb = []                                          # v1.34: boxes of the deleted elements (for publishing)
    if not reuse:
        left_ = set(g for v in KEEP.values() for g in v)   # last-pass elements this pass did not ask for again
        dead = [it for it in old_items if it[1] in left_]   # v1.44: left_ = AcBuild elements only (BGA- ids)
        if left_ and "DeleteElements" not in miss:
            log.append(u"model: %d AcBuild element(s) no longer wanted deleted; %d kept, %d made" % (
                del_typed(list(left_), u"changed elements"), N_KEPT[0], len(NEW_G)))
        if N_LOCKSKIP[0]:
            log.append(u"FLAG %d new element(s) not made: a hand-edited (locked) element of the same kind stands there "
                       u"(clear its Element ID to hand it back to AcBuild)" % N_LOCKSKIP[0])
        dead_bb = [it[2] for it in dead]

    def in_t(p, r):                                       # v1.32: a ground tile ("tile", x0, y0, x1, y1) or a cut
        if r is None:
            return True
        if r[0] == "tile":
            return r[1] - 0.5 <= p[0] <= r[3] + 0.5 and r[2] - 0.5 <= p[1] <= r[4] + 0.5
        return inside(p, r)
    if not reuse and SEO_TERR:
        # v1.27 (Aras 15 Nov 20:07 "use solid element operations where necceseary"): every plinth, terrace and
        # masterplan slab cuts the terrain mesh it stands in (Solid Element Operation, subtraction), so the cut ground
        # in a section stops at their faces instead of running through them
        def tl_(P):                                       # v1.42: ground tiles under the box of these survey points
            xs_, ys_ = [q[0] for q in P], [q[1] for q in P]
            i0, i1 = int((min(xs_) - 0.5 - gb[0]) // T), int((max(xs_) + 0.5 - gb[0]) // T)
            j0, j1 = int((min(ys_) - 0.5 - gb[1]) // T), int((max(ys_) + 0.5 - gb[1]) // T)
            return [g_ for a_ in range(i0, i1 + 1) for b_ in range(j0, j1 + 1) for g_ in TILE_IX.get((a_, b_), [])]

        def terr_at(P):
            if WHOLE_SITE:
                return tl_(P)
            return [tg for tg, r in SEO_TERR if any(in_t(q, r) for q in P)]
        links = [dict(targetId={"guid": tg}, operatorId={"guid": og}, operation="Subtraction")
                 for og, P, _lv in SEO_OPS if P for tg in terr_at([(q[0] + ox, q[1] + oy) for q in P])]
        # v1.29: plinths and terraces cut the river bed mesh too; the ground (cut terrains + river bed) cuts the water
        links += [dict(targetId={"guid": tg}, operatorId={"guid": og}, operation="Subtraction")
                  for tg, f_ in [(tg, _pip_fast(H)) for tg, H in RIVER_MESH] for og, P, _lv in SEO_OPS
                  if P and any(f_((q[0] + ox, q[1] + oy)) for q in P)]
        # v1.30: each road / park cell keeps only what lies inside the terrain (its top = the survey ground)
        links += [dict(targetId={"guid": g_}, operatorId={"guid": tg}, operation="Intersection")
                  for g_, c_ in TOWN_OPS for tg in terr_at([c_])]
        # v1.31 (Aras 21:19 "solid element operations"): building ground slabs (upward: no ground inside a house),
        # the Kızıl Avlu walls, bridge arches and piers, bank walls, kerbs and walls cut the ground
        links += [dict(targetId={"guid": tg}, operatorId={"guid": og}, operation=op)
                  for og, op, pa in EXTRA_OPS if pa for tg in terr_at([(q["x"] + ox, q["y"] + oy) for q in pa])]
        RPIP = [(tg, _pip_fast(H)) for tg, H in RIVER_MESH]
        for wg, P in WATER_OPS:
            c = (sum(q[0] for q in P) / len(P) + ox, sum(q[1] for q in P) / len(P) + oy)
            links += [dict(targetId={"guid": wg}, operatorId={"guid": tg}, operation="Subtraction")
                      for tg in ([] if RIVER_MESH else terr_at([c]))]   # v1.44: in the channel only the bed body cuts the water
            links += [dict(targetId={"guid": wg}, operatorId={"guid": tg}, operation="Subtraction")
                      for tg, f_ in RPIP if f_(c)]
        links += EXTRA_LINKS                              # v1.44: road minus pavement
        n_all = len(links)                                 # v1.34: a link between two kept elements is still there
        links = [l_ for l_ in links if l_["targetId"]["guid"] in NEW_G or l_["operatorId"]["guid"] in NEW_G]
        LINK_T.update(l_["targetId"]["guid"] for l_ in links)   # v1.44: their 3D box changes: stamped again
        log.append(u"solid element operations: %d of %d needed (the others join kept elements and are in the model)"
                   % (len(links), n_all))
        n_ok = 0
        try:
            ac.t("ChangeWindow", {"windowType": "FloorPlan", "storyIndex": 0})    # v1.36
        except Exception:
            pass
        for i in range(0, len(links), CHUNK):
            try:
                rr = ac.t("CreateSolidElementLinks", {"solidLinks": links[i:i + CHUNK]})
                n_ok += sum(1 for e in (rr.get("executionResults") or []) if isinstance(e, dict) and e.get("success"))
            except Exception as ex:
                log.append(u"FLAG solid element operations not made (%s)" % ex)
                break
        log.append(u"solid element operations: %d of %d (terrain + river bed cut by plinths, terraces and masterplan slabs; "
                   u"water cut by the ground; road and park cells shaped by the terrain)" % (
            n_ok, len(links)))
    if PID[0] and not reuse:                              # v1.44: the record goes into the pln
        hm_ = dict((it[1], it[0]) for it in ITEMS)
        pr_ = [(g, hm_[g]) for g in (set(NEW_G) | LINK_T) if g in hm_]
        log.append(u"Element IDs: %d of %d new / cut element(s) stamped BGA-<fingerprint>@<3D box>" % (
            stamp(ac, PID[0], pr_) if pr_ else 0, len(pr_)))
    log.append(u"model: %.0f s" % (time.time() - tp))
    # ---- sections (kept between runs)
    secs = old.get("sections") or {}
    fresh = set()                                         # v1.34: sections made or moved in this pass
    if "CreateSections" not in miss:
        # v1.9: the sections in the project must be exactly the ones recorded; else all are made again (15 Nov:
        # after a recovery the project held 21 views with 9 names twice and none of the recorded GUIDs)
        try:                                              # v1.29: the list reads the current window's database
            ac.t("ChangeWindow", {"windowType": "FloorPlan", "storyIndex": 0})
        except Exception:
            pass
        try:
            r_ = ac.t("GetElementsByType", {"elementType": "CutPlane"})     # v1.11: Tapir's list (the AC 29 API
            have = [e["elementId"]["guid"] for e in (r_.get("elements") or [])  # refuses "Section" and "CutPlane")
                    if isinstance(e, dict) and e.get("elementId")]
        except Exception as ex:
            have = None
            log.append(u"FLAG sections not listed (%s): kept as recorded" % ex)
        if have is not None and not have and secs:       # v1.29 (v1.18 rerun: 0 listed, 15 recorded, all remade)
            log.append(u"FLAG sections: 0 listed while %d are recorded: taken as a listing failure, the recorded sections "
                       u"are kept (nothing remade, the publisher set stays valid)" % len(secs))
            have = None
        if have is not None and (set(have) != set(secs.values()) or len(have) != len(secs)):
            try:
                vt = ac.t("GetNavigatorItemTree", {"navigatorMapId": "PublicViewMap"})
                ids = []

                def sub(o, inside):
                    if isinstance(o, dict):
                        here = inside or o.get("name") == VIEW_FOLDER
                        for k_, v in o.items():
                            if k_ != "navigatorItemId":
                                sub(v, here)
                        if here and o.get("navigatorItemId"):
                            ids.append(o["navigatorItemId"])        # children before their folder
                    elif isinstance(o, list):
                        for v in o:
                            sub(v, inside)
                sub(vt, False)
                if ids:
                    ac.t("DeleteNavigatorItems", {"navigatorItemIds": [{"navigatorItemId": x} for x in ids]})
                log.append(u"View Map: %d item(s) in \"%s\" deleted" % (len(ids), VIEW_FOLDER))
            except Exception as ex:
                log.append(u"FLAG View Map folder \"%s\" not cleared (%s): delete it by hand" % (VIEW_FOLDER, ex))
            if have:
                try:
                    ac.t("DeleteElements", {"elements": [{"elementId": {"guid": g}} for g in have]})
                except Exception as ex:
                    log.append(u"FLAG old sections not deleted (%s)" % ex)
            log.append(u"FLAG sections: %d in the project, %d recorded, so all were made again. In Archicad (Window > "
                       u"Palettes > Organizer), in the publisher set %s delete its items, drag the View Map folder "
                       u"\"%s\" in (format PDF), Ctrl+S, then press AcBuild again" % (
                           len(have), len(secs), PUB_SET, VIEW_FOLDER))
            secs, old["views"], old["view_folder"] = {}, {}, None
            old["remade"] = True                          # not published: the set points at the old views
        try:
            ac.t("ChangeWindow", {"windowType": "FloorPlan", "storyIndex": 0})
        except Exception as ex:
            log.append(u"floor plan not activated (%s)" % ex)
        moved = []
        if secs and ac.has("GetDetailsOfElements"):        # v1.4: a section whose line moved is made again
            nms = list(secs)
            try:
                det_ = ac.t("GetDetailsOfElements", {"elements": [{"elementId": {"guid": secs[k]}} for k in nms]})
                lst = det_.get("detailsOfElements") or []
            except Exception as ex:
                lst = []
                log.append(u"FLAG section lines not read back (%s): kept as they are" % ex)

            def find(o, key):
                if isinstance(o, dict):
                    if key in o and isinstance(o[key], dict) and "x" in o[key]:
                        return o[key]
                    for v in o.values():
                        r_ = find(v, key)
                        if r_:
                            return r_
                elif isinstance(o, list):
                    for v in o:
                        r_ = find(v, key)
                        if r_:
                            return r_
                return None
            want = dict((name, (xy(A), xy(B))) for name, A, B, Ln, u, n in rects)
            want.update((name, (xy(A), xy(B))) for name, A, B, dp in BSECS)   # v1.14: the building views too
            for k, d_ in zip(nms, lst):
                a_, b_ = find(d_, "startCoordinate"), find(d_, "endCoordinate")
                if k not in want:
                    continue
                if not (a_ and b_) or max(abs(a_["x"] - want[k][0]["x"]), abs(a_["y"] - want[k][0]["y"]),
                                          abs(b_["x"] - want[k][1]["x"]), abs(b_["y"] - want[k][1]["y"])) > 0.05:
                    moved.append(k)
            if moved:
                try:
                    ac.t("DeleteElements", {"elements": [{"elementId": {"guid": secs[k]}} for k in moved]})
                except Exception as ex:
                    log.append(u"FLAG moved sections not deleted (%s)" % ex)
                for k in moved:
                    fresh.add(k)
                    secs.pop(k, None)
                    (old.get("views") or {}).pop(k, None)
                log.append(u"FLAG sections %s: their lines moved, made again on the new lines. In Archicad (Window > "
                           u"Palettes > Organizer): in the publisher set %s delete its folder and drag the View Map "
                           u"folder \"%s\" in again (format PDF), then press AcBuild again" % (
                               u", ".join(moved), PUB_SET, VIEW_FOLDER))
        new = [(name, A, B) for name, A, B, Ln, u, n in rects if name not in secs]
        fresh.update(nm[0] for nm in new)
        if new:
            gs_ = ac.create("CreateSections", "sectionsData", [
                dict(startCoordinate=xy(A), endCoordinate=xy(B), depth=BACK_M, name=name, id=name)
                for name, A, B in new], u"sections")
            secs.update(dict((nm[0], g) for nm, g in zip(new, gs_) if g))
        newb = [(name, A, B, dp) for name, A, B, dp in BSECS if name not in secs]   # v1.14: the building views
        fresh.update(nm[0] for nm in newb)
        if newb:
            gs_ = ac.create("CreateSections", "sectionsData", [
                dict(startCoordinate=xy(A), endCoordinate=xy(B), depth=dp, name=name, id=name)
                for name, A, B, dp in newb], u"node building cut / elevation views")
            secs.update(dict((nm[0], g) for nm, g in zip(newb, gs_) if g))
        det = dict(horizontalRange="Limited", effectVectorShadow=SHADOWS, effectSunFrom3D=False, sunAzimuth=SUN[0],
                   sunAltitude=SUN[1], storyHandleAppearance="None",
                   # v1.24 (Aras 15 Nov 20:01, his Section Selection Settings): cut elements in their own pens;
                   # uncut = uniform pen colour fill (window background), one uncut line pen 81 (0.18 mm), no transparency;
                   # fade distant elements on, pen colour fill (window background), one line pen 102 (0.13 mm);
                   # no element contours at the section boundary
                   useElementPens=False, sectionLinePenIndex=21, sectionFillPenIndex=101, sectionFillBackgroundPenIndex=0,   # v1.44 (Aras 16 Nov 11:22 screenshot): uniform cut pens 21 / 101, background transparent
                   useUncutSurfaceFill=True, modelUncutSurfaceFillType="MaterialColorShaded",   # v1.41: own material colour (v1.38 PenColor = white over the hills)
                   modelUncutSurfaceFillBackgroundPenIndex=-1, useOneModelPen=True, modelPenIndex=81,   # v1.44: uniform uncut pens 81   # v1.39: own pens (pen 81 hid the wall edges)
                   transparent=False, effectVectorHatch=False,   # v1.44: no surface cover fill
                   markedDistantArea=True,   # v1.44 (Aras 11:22): fade distant elements on;                     # v1.40 useUncutSurfaceFillInDistantArea=True,
                   distantAreaUncutSurfaceFillBackgroundPenIndex=-1, useOneDistantAreaPen=False, distantAreaPenIndex=102,   # v1.39
                  
                   boundaryDisplayMode="NoContours")
        try:
            ac.t("SetSectionsAndElevationsDetails", {"elementsWithDetails": [
                {"elementId": {"guid": g}, "details": det} for g in secs.values()]})
            log.append(u"section settings (Aras 15 Nov): limited depth %.0f m, uncut own material colour, shaded (v1.41), own pens (v1.39), fade "
                       u"distant elements pen 102, no boundary contours" % BACK_M)
        except Exception as ex:
            det2 = dict((k, v) for k, v in det.items() if v != -1)     # v1.24: the window-background pen (-1) refused
            try:
                ac.t("SetSectionsAndElevationsDetails", {"elementsWithDetails": [
                    {"elementId": {"guid": g}, "details": det2} for g in secs.values()]})
                log.append(u"FLAG section settings set without the window-background fill pen (-1 refused: %s): in "
                           u"Archicad select the 13 section markers, Section Selection Settings > Model Appearance, "
                           u"Pen - Color Fill = Window Background (-1) for Uncut and Fade Distant Elements" % ex)
            except Exception as ex2:
                log.append(u"FLAG section settings not set (%s / %s): Archicad defaults used" % (ex, ex2))

    # ---- View Map views + publish
    views = old.get("views") or {}
    try:
        tree = ac.t("GetNavigatorItemTree", {"navigatorMapId": "ProjectMap"})
        found = {}

        def walk(o):
            if isinstance(o, dict):
                if o.get("name") in secs and "Section" in u"%s" % o.get("type") and o.get("navigatorItemId"):
                    found[o["name"]] = o["navigatorItemId"]
                if "Story" in u"%s" % o.get("type") and o.get("navigatorItemId"):     # v1.17: building floors
                    for vn, stn in PVN.items():
                        if o.get("name") == stn:
                            found[vn] = o["navigatorItemId"]
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(tree)
        have = set()                                      # v1.17: plan views already in the View Map (by name)
        if PVN:
            def walk_v(o):
                if isinstance(o, dict):
                    if o.get("name") in PVN:
                        have.add(o["name"])
                    for v in o.values():
                        walk_v(v)
                elif isinstance(o, list):
                    for v in o:
                        walk_v(v)
            walk_v(ac.t("GetNavigatorItemTree", {"navigatorMapId": "PublicViewMap"}))
        todo = [nm for nm in secs if nm in found and nm not in views] + [
            nm for nm in sorted(PVN) if nm in found and nm not in have]
        if todo:
            fid = old.get("view_folder") or ac.t("CreateViewMapFolder", {"folderName": VIEW_FOLDER})["navigatorItemId"]
            old["view_folder"] = fid
            r = ac.t("CreateViewsInViewMap", {"viewsData": [dict(navigatorItemId=found[nm], parentNavigatorItemId=fid,
                                                                  name=nm) for nm in todo]})
            log.append(u"View Map: %d view(s) made in \"%s\" (%s)" % (len(todo), VIEW_FOLDER, json.dumps(r)[:120]))
            views.update(dict((nm, True) for nm in todo))
    except Exception as ex:
        log.append(u"FLAG View Map views not made (%s)" % ex)
    published = False
    try:
        sets = [p.get("name") for p in ac.t("GetPublisherSets").get("publisherSets", [])]
        dw = [os.path.basename(x)[:-4] + ".dwg" for e_ in ("pdf",)      # v1.35: only PDFs count (v1.20: DWG too)
              for x in glob.glob(os.path.join(DWG_DIR, "**", "*." + e_), recursive=True)]
        # v1.34: which sections to publish: a section whose line is new or moved, that has no DWG, or whose view
        # (its line + SIDE_M in front, its depth behind) holds an element made or deleted in this pass; all of them
        # when the last publish did not finish, the view settings changed or unrecorded elements were deleted
        alln = list(secs) + list(PVN)
        has_dwg = lambda nm: any(x.startswith(nm + " ") or x == nm + ".dwg" for x in dw)
        if not old.get("published") or old.get("sec_sig") != SEC_SIG or n_stray or not old_items:
            pub = set(alln)
        else:
            chg = [bb for bb in dead_bb + [it[2] for it in ITEMS if it[1] in NEW_G] if bb]
            reg_ = {}
            for nm, A, B, Ln, u, n in rects:
                reg_[nm] = (A, B, max(SIDE_M, BACK_M))
            for nm, A, B, dp in BSECS:
                reg_[nm] = (A, B, dp)
            NBD_ = dict((b["node"], b) for b in NB)
            for vn, stn, lv, nd, j in PV:
                b = NBD_.get(nd)
                if b:
                    r_ = max(b["L"], b["D"]) / 2.0 + 10.0
                    reg_[vn] = (b["c"], b["c"], r_)
            pub = set(nm for nm in alln if nm in fresh or not has_dwg(nm) or nm not in reg_)
            for nm, (A, B, r_) in reg_.items():
                if nm in pub or nm not in alln:
                    continue
                a_, b_ = xy(A), xy(B)
                x0_, x1_ = min(a_["x"], b_["x"]) - r_, max(a_["x"], b_["x"]) + r_
                y0_, y1_ = min(a_["y"], b_["y"]) - r_, max(a_["y"], b_["y"]) + r_
                if any(bb[0] <= x1_ and bb[2] >= x0_ and bb[1] <= y1_ and bb[3] >= y0_ for bb in chg):
                    pub.add(nm)
        if NO_SAVE_PUBLISH:                               # v1.42
            log.append(u"not saved, not published (whole-site build: Aras saves the pln himself)")
        elif not old.get("remade") and old.get("published") and not pub:
            published = True
            log.append(u"not published: no section sees a change, the DWGs of the last pass kept")
        elif old.pop("remade", False):
            log.append(u"not published: the sections were made again (see the FLAG above)")
        elif PUB_SET in sets:
            os.makedirs(DWG_DIR, exist_ok=True)
            if ac.has("SaveProject"):                   # v1.8: the build survives a hang or a restart
                try:
                    ac.t("SaveProject", {})
                    log.append(u"Archicad project saved before publishing")
                except Exception as ex:
                    log.append(u"FLAG Archicad project not saved (%s): press Ctrl+S in Archicad" % ex)
            # v1.8: publish only the publisher-set items of our sections (15 Nov: the set held the whole
            # project as PDF and DWG and Archicad hung for an hour)
            pt = ac.t("GetNavigatorItemTree", {"navigatorMapId": "PublisherSets", "publisherSetName": PUB_SET})
            leaves = []

            def walk_p(o):
                if isinstance(o, dict):
                    kids = [v for k_, v in o.items() if isinstance(v, (list, dict)) and k_ != "navigatorItemId"]
                    if "navigatorItemId" in o and "name" in o:
                        sub = []
                        for v in kids:
                            sub += walk_p(v)
                        if not sub:
                            leaves.append(o)
                        return [o] + sub
                    out_ = []
                    for v in kids:
                        out_ += walk_p(v)
                    return out_
                if isinstance(o, list):
                    out_ = []
                    for v in o:
                        out_ += walk_p(v)
                    return out_
                return []
            walk_p(pt)

            def is_ours(it):
                tx = u" %s %s " % (it.get("uiId") or u"", it.get("name") or u"")
                return any(re.search(u"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(nm), tx) for nm in pub)
            ours = [it for it in leaves if is_ours(it)]
            log.append(u"publishing %d of %d section(s): %s" % (len(pub), len(alln), u", ".join(sorted(pub))))
            miss_b = [nm for nm in [b_[0] for b_ in BSECS if b_[0] in secs] + sorted(PVN) if not any(
                re.search(u"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(nm),
                          u" %s %s " % (it.get("uiId") or u"", it.get("name") or u"")) for it in leaves)]
            if miss_b:                                    # v1.14: one-time Organizer step for the building views
                log.append(u"FLAG ONE-TIME STEP in Archicad (the node building views): Window > Palettes > Organizer; "
                           u"left = View Map, right = Publisher Sets > %s; drag the View Map folder \"%s\" onto the "
                           u"set again (it now also holds %s); keep format PDF; Ctrl+S; then press AcBuild again" % (
                               PUB_SET, VIEW_FOLDER, u", ".join(miss_b)))
            log.append(u"publisher set \"%s\": %d item(s), %d of them our sections" % (PUB_SET, len(leaves), len(ours)))
            done = False
            if ours and len(ours) < len(leaves):
                try:
                    ac.t("PublishPublisherSet", {"publisherSetName": PUB_SET, "outputPath": DWG_DIR,
                                                 "selectedNavigatorItemIds": [{"navigatorItemId": it["navigatorItemId"]}
                                                                              for it in ours]}, 1800.0)
                    done = True
                    log.append(u"published the %d section item(s) of \"%s\" only" % (len(ours), PUB_SET))
                except Exception as ex:
                    log.append(u"FLAG the section items alone not published (%s): %d other item(s) in \"%s\" not "
                               u"published either. In Archicad (Window > Palettes > Organizer), open %s, delete "
                               u"everything except the \"%s\" views, format PDF, Ctrl+S, then press AcBuild again" % (
                                   ex, len(leaves) - len(ours), PUB_SET, PUB_SET, VIEW_FOLDER))
            elif ours:
                ac.t("PublishPublisherSet", {"publisherSetName": PUB_SET, "outputPath": DWG_DIR}, 1800.0)
                done = True
            else:
                log.append(u"FLAG no section item found in \"%s\" (%d item(s)): refresh it with the View Map folder "
                           u"\"%s\"" % (PUB_SET, len(leaves), VIEW_FOLDER))
            published = done
            if done:
                log.append(u"published \"%s\" -> %s (%d file(s))" % (PUB_SET, DWG_DIR, len(os.listdir(DWG_DIR))))
        else:
            log.append(u"FLAG ONE-TIME SETUP in Archicad: Navigator > Publisher Sets > New Publisher Set, name it %s; "
                       u"drag the View Map folder \"%s\" into it; Publish Properties: Save files, format PDF; then "
                       u"press AcBuild again (it publishes to %s)" % (PUB_SET, VIEW_FOLDER, DWG_DIR))
    except Exception as ex:
        log.append(u"FLAG not published (%s)" % ex)

    with open(pj, "w", encoding="utf-8") as f:
        json.dump(dict(version=VERSION, run=time.strftime("%Y-%m-%d %H:%M:%S"), tapir=ver, origin=[ox, oy],
                       story0=z0, reg=dict(z=REG_Z, start_w=0.4, end_w=0.8, layer="BG reg"), back_m=BACK_M,
                       cuts=[dict(name=nm, A=list(A), B=list(B), L=round(Ln, 3), back=backs.get(nm), bands=bands.get(nm))
                             for nm, A, B, Ln, u, n in rects],
                       building_views=[dict(name=nm, A=list(A), B=list(B), L=round(math.hypot(B[0] - A[0], B[1] - A[1]), 3),
                                            depth=dp, ground=next((b["ground"] for b in NB if nm.startswith(b["node"] + u"-")), None),
                                            gap=NB_GAP_M, reg=dict(z=REG_Z + NB_REG_DZ, h=NB_REG_H, s_in=NB_REG_IN, w=[0.4, 0.8]))
                                       for nm, A, B, dp in BSECS] + [
                           dict(name=vn, kind="plan", node=nd, floor=j, story=stn, level=lv,     # v1.17: floor plans
                                **dict((k_, (dict((b_["node"], b_) for b_ in NB).get(nd) or {}).get(k_))
                                       for k_ in ("c", "u", "w", "L", "D")),
                                reg=dict(off=NB_PREG_M, a=list(NB_PREG_A)))
                           for vn, stn, lv, nd, j in PV],
                       plan_views=PV,
                       sections=secs, views=views, view_folder=old.get("view_folder"), published=published,
                       dwg_dir=DWG_DIR, layers=list(LAYERS), canopies=CANOPY_REC, elements=made, build_sig=sig,
                       items=old_items if reuse else ITEMS, sec_sig=SEC_SIG,
                       counts=now if reuse else counts()), f,
                  ensure_ascii=False, indent=1)
    log.append(u"%s  %s" % (pj, time.strftime("%H:%M:%S")))
    flags = [l for l in log if l.startswith(u"FLAG") or u"FLAG" in l]
    return u"%s\n%s %s, %d elements, %d section(s), %d FLAG line(s), %.1f s" % (
        u"\n".join(log), GH_LABEL, VERSION, len(made), len(secs), len(flags), time.time() - t0)


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


_PH1 = None   # v1.22: a threading.Event set when main() no longer needs Rhino (background run only)


def _run_bg():
    """v1.22: main() in a background thread; returns once the Rhino part is done (or the run ended). The log file
    reads "RUNNING ..." until the thread writes the full log, as the one-piece run does"""
    global _PH1
    import threading
    fg = os.path.join(BERGAMA_ROOT, "cached", "_chain", "acbuild_foreground.txt")
    if os.path.isfile(fg):
        return write_log(_run())
    try:
        import scriptcontext as _scb
        st = _scb.sticky
    except Exception:
        st = {}
    th = st.get("bergama_acbuild_thread")
    if th is not None and th.is_alive():
        return u"ERROR: AcBuild is still running in the background (started %s): wait for its log" % st.get(
            "bergama_acbuild_started", u"?")
    _PH1 = threading.Event()
    t_ = time.strftime("%H:%M:%S")
    write_log(u"RUNNING %s %s in the background since %s (this file gets the full log when it ends)" % (
        GH_LABEL, VERSION, t_))

    def body():
        try:
            write_log(_run())
        finally:
            _PH1.set()
    th = threading.Thread(target=body, name="bergama_acbuild", daemon=True)
    st["bergama_acbuild_thread"], st["bergama_acbuild_started"] = th, t_
    th.start()
    _PH1.wait()
    if not th.is_alive():
        th.join()
        with open(os.path.join(LOG_DIR, LOG_NAME), encoding="utf-8") as f:
            return f.read()
    return (u"%s %s: Rhino part done at %s; the Archicad part goes on in the background (Rhino is free). Wait "
            u"until %s no longer starts with RUNNING before SectionsAC, Sections, Seasons, the node slides or "
            u"Perspectives" % (GH_LABEL, VERSION, time.strftime("%H:%M:%S"), os.path.join(LOG_DIR, LOG_NAME)))


def _run():
    try:
        return main()
    except Exception as _ex:
        import traceback as _tb
        return "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-900:])


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
        _res = _run()
        _sc.sticky[_k + "_log"] = write_log(_res)
        _sc.sticky[_k + "_status"] = ("ERROR" if _res.startswith("ERROR") else
                                      time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky[_k + "_done"] = done_text(True, not _res.startswith("ERROR"), time.time() - _t0)
        _sc.sticky[_k + "_ver"] = VERSION
    if _sc.sticky.get(_k + "_ver") != VERSION:
        for _s in ("_log", "_status", "_done"):
            _sc.sticky.pop(_k + _s, None)
    done = _sc.sticky.get(_k + "_done", "idle")
    log = _sc.sticky.get(_k + "_log", "Press the Button to build in Archicad")
    print(log)
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(_k + "_status", "idle")  # noqa: F821
    except Exception:
        pass
elif __name__ == "__main__":
    if _in_rhino():
        print(_run_bg())                                  # v1.22: the Archicad part in the background
    else:
        print(write_log(_run()))                          # v1.44: plain Python, only Archicad open
