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

VERSION = "v1.88"   # v1.88 (Aras 20 Nov 09:50-10:03, effort High: "fix roads and streets ... retry with a different approach", "just draw the landscape underneath it ... both are constructed in the same space it shouldnt", "same two object shouldn't be constructed in the same area", "you are mixing a lot of areas for what they are in the masterplan", "you are drawing road outlines as walls", "two walls in the same place", "slab extends to the outer face of the walls", "these lamps are wrong", canopy "walls are everywhere"): GROUND COVERS: every surface area (his masterplan surface layers in his drawing order, the survey roads + parks, the bank zones) is one set of non-overlapping pieces (the one he drew on top wins), each a Mesh body draped on the surveyed ground, and the ground mesh is lowered under every piece (no overlap, no solid element operation; needs shapely); his surface layers are no longer flat thin slabs; no kerb walls on the road edges; survey walls step with the slope (were metres-high flat-topped walls); a side shared by two houses gets one wall (the taller house's); the house ground slab ends at the inner wall face; canopy louvre slats fixed to the roof underside; survey lamp points within 3.2 m merged into one lamp, Archicad's Street Lamp turned to the nearest road; rosemary as Shrubs. v1.87 (Aras 19 Nov 09:21-09:22 "you need to have a slab and you should use it in core top and with core outside you need to turn those walls into house walls ... every wall should go from bottom link to top link core top's"): house walls are composite with their reference line on the core's outside face (the footprint pulled in by the outer skins, so the plaster face stays on the outline and the core lines meet at the corners), drawn so the body lies inside (side read from one test wall); floor slabs are composite with their reference plane on the core top; every storey wall runs from the core top of the slab below to the core top of the slab above. v1.86 (Aras 19 Nov 09:20 "run intersact command for every intersection": Archicad's Auto-Intersection is switched on at the start, so every junction is intersected as it is made; "their height changes ever so slightly so intersect command doest works"): every ground-floor wall of a house starts at the same height, the lowest ground under any of its sides (was each side at its own ground), so all walls of a storey share base and top and Archicad intersects them. v1.85 (Aras 19 Nov 09:16 "something is wrong with house drawings aswell please fix those aswell": wall layers showing at every corner, a line at every floor, a loose band at the roof): house walls on centre reference lines pulled in half a wall from the footprint, so they lie inside it and their lines meet at the corners (were outside-face lines); floor slabs and the flat roof inside the walls (were on the footprint, their edges on the facade); no cornice band. v1.84 (Aras 19 Nov 09:12-09:13 "respect the site_alan everywhere ... if something is half out half in dont draw it. It needs to be in the area +%90 so you can draw it with the cutted plane"): every element sent to Archicad is measured against site_alan: under 90 % inside (area, length or point) it is not made; 90 % or more, slabs / meshes are cut and walls / beams trimmed at the edge; houses the same on their footprint. v1.83 (Aras 19 Nov 09:00-09:06): ground heights only where the drawn ground would otherwise be more than +-0.30 m off the survey ("+-30 or even 40 should be fine"); road + park skins raised by the most the ground mesh can fold between its points, so the ground no longer covers them ("roads still dissappear under ground"), on the ground's own heights, in cells of 200 m that are quartered only where Archicad refuses one ("make the road parking surfaces larger"), cut to site_alan; one Railing per balcony ("balcony rails as one railing per balcony"; windows as they are); the real 3D library trees Tree Model Detailed / Pine Tree Model / Fronded Tree variable ("use rather high poly real 3d trees"); our node buildings + canopies built in the site file ("buildings and areas from our masterplan is not built": Bergama_buildings.pln never existed); houses off the modelled ground left out ("goes out of the topography"); road, park and pavement bodies, steep / thin / tiny road pieces handled ("with real thickness"). v1.82 (Aras 19 Nov 08:49 "can we do anything to make scripts run faster", "i dont want any quality loss with the changes"): the same model, faster: Archicad's Suspend Groups is on while old elements are deleted (v1.78 lost and rebuilt 3953 kept walls, 1666 windows and 26 doors when house-group members were deleted), and a "time by step" log line shows where the minutes go. (v1.80 / v1.81 withdrawn by Aras.) v1.79 (v1.78 run 19 Nov: the embedded GDL library call timed out after 15 min and all 803 trees were left out): Archicad's own library trees are now picked in every case (a plant word required, the species word at a word start, else the most detailed generic broadleaf / conifer / shrub of its group); the embedded AcBuild parts are not sent again when the project already holds them with the same scripts, and are used after a timed-out call if they arrived; a wall whose 3D box moved less than 0.60 m (Archicad trims walls at junctions with remade neighbours) is no longer locked as hand-edited (v1.78 locked 548 elements). v1.78 (Aras 19 Nov 07:22-07:25 "dont draw roads like this", "just draw them from outlines not like whole ground and just elevated where the part of the road is", "draw the roads properly", not slabs: they might collide with the houses' slabs): roads + parks are ONE Mesh-tool skin per outline (town blocks as holes) lying on the ground AS ARCHICAD BUILT IT (were 50 m cells lifted by the tile error, up to 0.6 m); no slab, no SEO. (07:20 "many of the houses are not closed off", 07:26 "Many of those houses misses walls and etc."; v1.77 kept 1551 roofs but only 588 were in the model): every element of the pass is looked up in the model after the old ones are deleted and again at the end; any that vanished is made again and FLAGged by type. (07:29 "Check the script for such gaps aswell"): house outlines tidied before anything is built: an edge under 0.30 m used to be skipped (a gap in the walls), now it is merged into its neighbours; spikes removed; a v1.76 corner move that would make the outline cross itself (Archicad then refused its roof / slabs) is not made. (07:20 07:21 "tree's are really bad as assets find something more detailed more proper looking"): walls (kerbs, survey walls, bank walls, retaining walls) are no longer broken where the ground under them changes height (LINE_RISE_M off): one wall per straight run; trees: the most detailed tree / shrub of Archicad's own loaded library matching each species (by name) is placed instead of AcBuild's simple GDL tree, which stays only where no library part matches. v1.77 (Aras 19 Nov 06:43 "join them aswell as long as lines are connected archicad does to connection itself"): T-junctions too: a kerb / survey wall line end that stops within SNAP_M of another such line (not at its end) is moved onto that line, so the reference lines touch and Archicad makes the joint. v1.76 (Aras 19 Nov 05:52 "make sure that script doesnt constructs items on top of each other", "items shouldn't collide", "their construction line (like the blue line) must always connect each other"): no collisions: overlapping survey houses no longer kept as they are (the smaller one's corners that lie inside its neighbour are moved onto the neighbour's wall line), no tree / furniture / person / car inside a house or on top of another object (trunks at least TREE_GAP_M apart, other objects by their own size), no kerb / survey wall / retaining wall piece through a house, no kerb on a bank wall line; reference lines meet: retaining walls mitred at their corners (were offset edge by edge, leaving gaps), kerb / survey wall ends within SNAP_M of another end joined to one point. v1.75 (Aras 18 Nov 13:23 UTC "also check other drawing rules such as these and make them correctly drawn", "like everything"): each historic bridge (Ulucami, Üç Kemer) is ONE element, a GDL object made for it with its real arch curves, piers and deck in one stone body (was up to 36 stacked slabs per arch + pier walls; the old way stays only as a fallback); road / park ground skins in 50 m cells, the ground tile size (were 20 m cells: about 6x fewer meshes). v1.74 (Aras 18 Nov 13:22 UTC, decision card: "Yes, wall down to ground"): on a slope the ground-floor wall of each house side now runs down to 5 cm under the surveyed ground at that side (its ends and middle), covering the grey raft edge, so the facade reads as one composite wall down to the ground; its door and windows keep their heights above the floor. v1.73 (Aras 18 Nov 13:20 UTC "multiple stacks on the walls should be it's own composite instead of different walls stacked", "these goes for anything that is composite"): the canopy stone plinth and timber deck, two slabs stacked on the same outline, are now ONE composite slab (Bergama floor - canopy: timber deck on stone plinth); walls, floors and roofs were composites already. v1.72 (Aras 18 Nov 13:17 UTC "this applies per story like if a object is divided into two different stories they should be divided"): one element per straight run WITHIN each storey: house walls one per side per storey again (v1.70 had them raft to eaves), frame columns one per storey again (v1.71 had them raft to roof), node building walls (long sides with their glass bays as windows, and ends) now one per side per storey (were full height). v1.71 (Aras 18 Nov 13:15 UTC "not just for that house for every single drawing"): the one-wall-per-straight-run rule also for the bank walls on his istinaat lines and the retaining walls along plinths / terraces / masterplan slabs, node building long walls (one wall per side, the glass bays as windows in it), house frame beams (one beam per grid line, not per span) and columns (one per grid point, raft to roof, not per storey); 13:16 "these apply for slabs, walls, beams and etc.": their 4 m test pieces next to each other become ONE wall (new wall only where its top would change by more than LINE_RISE_M or where a piece is not needed). v1.70 (Aras 18 Nov 13:12 UTC "draw a single wall or slab where you can", "there are a million walls"): one wall per straight side: house footprints drop survey points that lie within STRAIGHT_TOL_M of the line between their neighbours (the same footprint for walls, slabs, raft and roof), and each side is ONE wall from the raft to the eaves (was one wall per storey; windows stay per storey); survey kerbs / walls: straight runs merged the same way, no 6 m chopping (LINE_SEG_M off), new piece only where the ground rises more than 0.30 m along it (was 0.10 m). v1.69 (Aras 18 Nov 13:09-13:11 UTC "roads and bridges are fucked", "look at these roads"): roads were flat black (Archicad surface "Pavement - Asphalt Dark") with the ground poking through: roads now take the plain road grey 8C8B87 (no texture), and each road / park skin sits over the 50 m ground tile by that tile's own measured deviation from the survey (+3 cm), so the tile no longer shows through; bridges: arch soffits in 36 steps (was 12), and his bridge outline over a historic bridge (Ulucami, Üç Kemer) is no longer built as a second flat deck on top of the arches (it floated at the highest bank height). v1.68 (Aras 18 Nov 13:07 UTC "please add all the objects back trees and all and dont do the trees with slabs"): GDL objects on again (GDL_OBJECTS True: trees per species, street furniture, people, cars, made in the embedded library as in v1.62); trees are ONLY GDL objects: a tree whose object could not be made is left out and flagged, never built as trunk + crown slabs, and the old slab trees are deleted as leftovers. v1.67 (Aras 18 Nov 13:02 UTC "you'll also add everything that has been removed troughout the process right ?"): the per-section ground meshes are back (SECTION_BANDS True): the v1.65 test showed they were not why 3D hung (the solid links were), so the sections get their seamless ground again; their kerb / wall cuts follow the v1.66 rule (only near the section line). v1.66 (Aras 18 Nov 12:57-12:58 UTC: with all ~29,400 solid links removed the whole-site 3D opens after reopening; "seo off was the way to go", "keep that in mind troughout the next edits", "it is as little as possible"): solid element operations ONLY where they show: within SEO_CORR_M of a section line (the cut faces), the river bed bodies opening the ground into the channel, the river water cut by its bed, and the section slots; all other links (buried feet, plinths, kerbs, trunks, pavements away from the cuts: hidden inside the ground in 3D) are not made, and AcBuild's own older ones are removed. v1.65 (Aras 18 Nov 12:34 UTC: 3D stuck "Processing Elements" even with every BGA layer hidden; 12:35 "we can redraw it if needed"): TEST: no per-section ground meshes (SECTION_BANDS False): the 13 meshes (120,923 heights) and their cuts are deleted by this run, the v1.56 ground strips + slots come back on the section lines, section views go back to "BGA - all". v1.64: solid links that AcBuild made earlier but no longer wants (e.g. the v1.44-v1.60 kerb / wall cuts in the 50 m tiles, which v1.61 moved to the section grounds) are removed from the model; before, they stayed and kept the reopened 3D heavy. v1.63 (Aras 18 Nov 12:11 UTC "no dont bake objects the file is heavy enough"): no GDL objects at all (GDL_OBJECTS False): trees stay trunk + crown slabs as built so far, no street furniture, people or cars. v1.62 (Aras 18 Nov 11:50 UTC "what about the objects ?"): on 18 Nov every GDL object was refused ("The library part 'Bergama Olive.gsm' is not editable ... only a library part loaded from a writable file can be modified"), so trees stayed slab trees and there was no street furniture, people or cars; the objects are now made inside the project's embedded library with their scripts in one step (Tapir CreateLibraryParts, named "BGA <kind>"), the old folder route only as a fallback. v1.61 (Aras 18 Nov 11:42 UTC "i want to inspect whole 3d model"; full 3D ran 30+ min on one core): the ~16,000 survey kerb / wall pieces cut only the section views' own ground meshes (hidden in 3D), no longer the 50 m tiles that 3D shows, so most of the ~50,000 solid element operations drop out of 3D while the sections stay clean (no edge lines, Aras 11:43); in 3D their buried foot is inside the ground and unseen. v1.60 (Aras 18 Nov 10:27 UTC: only .bat files stay in Downloads\Bergama, everything else moves to Downloads\Bergama\Project Files): the root is "Project Files" when it holds scripts\, else Downloads\Bergama as before. v1.59 (Aras 18 Nov 09:56-09:58 UTC, N1-A PDF "this is fucked", "shaded is drawn semi properly", "thise vertical lines is still there"): uncut fill back to material colour, shaded (with the uniform pen colour fill Archicad drew the uncut walls and hills as white with no outlines, so only the window frames showed); the section views' own layer combination ("BGA - section <name>", tiles hidden) and override combination are now set on every run on every section view already in the View Map (v1.58 set them only on views it made, so a file with views from an earlier run kept the tiles and their seams). v1.58 (Aras 18 Nov 08:44 UTC "sections do draw each line between ground cells why is that ? Cant we fix that ? While keeping the file workable"): every 50 m ground tile is its own mesh and Archicad draws each mesh's outline, so the sections showed the tile grid on the ground behind the cut. Each of the 12 site sections now gets one ground mesh of its own over everything it sees (the cut line to 200 m behind, with the tiles' own heights inside it, so the same accuracy), on a hidden layer "BGA Ground view <name>"; its view uses the layer combination "BGA - section <name>" (tiles and the other views' ground hidden), so the section sees one seamless ground; plan, 3D and the other views keep the tiles; the v1.56 strips + slots are only made where a view mesh could not be. v1.57 (Aras 18 Nov 08:17 UTC: his Model Appearance screenshot; "use tree objects as 3D object according to the tree type"; "can we decrease both drawing time"; "i dont want some detail to get lost"): section uncut fill = uniform pen colour fill, non-shaded, window background, uncut pen 81 (also ends Illustrator's "unknown shading type"); fade distant = uncut fill on, uniform pen 102, window background; willow and tamarisk get their own 3D tree objects (were the general deciduous one); on a PC with more than 64 GB RAM the solid element operations go 200 per call (was 50) and the Element ID / layer calls 2000 per call; progress lines in the labelling step; nothing is left out. v1.56 (Aras 18 Nov 07:48 UTC "please make tree's out of objects also there are a lot of section drawing errors ... unkown shading type error when opening with illustrator"): the GDL objects are made, then the libraries reloaded and their scripts set again (18 Nov: "No loaded library part 'Bergama Olive.gsm'"); a section record from another project (0 sections listed and 0 AcBuild elements found in the open file) is dropped, so the sections and their View Map items are made fresh (18 Nov: 25 old sections looked for, View Map "Failed to clone"); the section settings stay Aras's own (16 Nov 11:22 screenshot: uncut Surface - Color Fill, Shaded); section stray lines (his N1-A PDF, 18 Nov): one ground strip per section line in a slot cut out of the 50 m tiles by a hidden slab (no tile seams), kerb / wall pieces short enough on slopes to rise at most 0.10 m (no tall posts), road / park cells and pavements as skins on the ground (no flat-bottomed boxes), cut survey houses drawn as one grey fill with pen 81 by the override combination "Bergama - sections" set on the section views. v1.55 (Aras 18 Nov 06:00 UTC "is there any patch have been missed ... optimizing the file for lower resource usage"): Element IDs are written with Tapir's own command first (the Archicad API call wants a typed value and refused all 23,052 on 17 Nov; it is now only the fallback, with its typed value), a GDL object that is not made logs Archicad's reason, the house frame line no longer calls every context house "masonry". v1.54 (Aras 17 Nov 13:55 UTC "yes please"): survey houses back in the site file (part "houses"), parts left to the other file logged as such (not "kept"), Element ID stamping falls back to Tapir and logs its error, the bridge loop no longer shadows bed(), the ground grid thinned to the heights the 8 m grid cannot give within the tile tolerance. v1.53 (Aras 17 Nov 12:33 UTC "auto save of the file"): the project is saved at the end of every run. v1.52 (Aras 17 Nov 12:16 UTC "make this bergama_Site file as the site file only, our canopies and our own buildings should be linked to it that way it would be easier to edit the buildings by hand and take drawings out of these"): two Archicad files from one script, chosen by the open project's name: Bergama_site.pln = the site (terrain, river, streets, survey houses, trees, furniture, his masterplan landscape pieces: terraces, seating tiers, bridges, bank walls) WITHOUT our canopies and node buildings; Bergama_buildings.pln (any name with "building") = ONLY our canopies + node buildings, same origin (taken from the site file's record), to be hotlinked into the site file at 0,0 (File > External Content > Place Hotlink, once by hand); each file has its own cache folder; solid element operations only between elements of the same file (the canopy plinths no longer cut the site ground); v1.51 (17 Nov 15:07-15:11 local: the v1.50 run built every element, then Archicad crashed in the solid element operations with 4.4 GB RAM free, before anything was labelled): the elements are labelled (BGA Element IDs), put on their layers and grouped FIRST, the project is saved (Tapir SaveProject; Aras gives the project a file name once), and only then the solid element operations are made, 50 per call with the RAM guard and a progress line each; the ones not made are kept in cached/bergama_archicad_site/seo_pending.json and the next run (in the reopened saved pln) makes them; the cut elements are labelled again and the project saved again at the end; v1.50 (17 Nov 14:56 local: Archicad 30 crashed at walls 7951-8100 while its 3D window was regenerating, and v1.49 then retried every chunk for minutes): when Archicad stops answering (connection refused / reset) the run stops at once with an ERROR (the launcher's red window), naming the step; v1.49 (option A for the Desktop's 24 GB, the v1.48 run stopped by its RAM guard at 14:44 with Archicad at 12 GB): CONTEXT_FRAMES = False: the existing survey houses get no RC columns / beams (inside their walls, invisible at site scale; about half of all elements); every house keeps its raft; the frames made so far are deleted as no longer wanted; a RAM-guard stop now stamps the elements made so far with their BGA Element ID before it ends (v1.48 stamped only at the end of a full pass, so its stopped run left its elements unlabelled: start that project fresh); v1.48 (Aras 17 Nov 11:10 UTC: Claude app, Rhino and Archicad crashed on the Desktop, 24 GB RAM; "something wrong with MCP connection"): run it standalone with only Archicad open (run_acbuild.bat: plain Python, survey from cached/bergama_survey/survey.json, no Rhino, no MCP); Tapir chunks 150 elements (was 400) and ground tiles 15 per call (was 40); a RAM guard before every Tapir call: under MIN_FREE_GB = 3 GB free it waits 120 s, then stops cleanly (FLAG; the next run resumes through the BGA IDs); logs/bergama_acbuild_progress.txt gets one line per call as it happens (the main log is only written at the end), so a crash leaves its last step on disk; v1.47 (Aras 17 Nov 09:58-10:37 UTC "just use latest masterplan version", "base of off that masterplan only": his laptop-Desktop masterplan.svg of 15 Nov 19:06, md5 9a344ff22724396ed846b31b9d2d633e, placed as Data/assets/plan/masterplan.svg -> MasterplanAI -> master.svg -> MasterplanBase -> masterplan.json, the only masterplan AcBuild reads): its layers checked against AcBuild: araba_yolu and doldrurma (were not built) now built on "BGA ? unsure" layers; his planting willows, olives and tamarisks (were skipped: no size) built as GDL trees (olive 5 m sourced; willow 10 m, tamarisk 4 m ASSUMED, FLAG); "normal" unsure layer dropped (not in the file); v1.46 (Aras 17 Nov 09:54 UTC "do the things that you need to do": research pack v3 R1-R10 folded in, Data/research_pack_v3_combined_2026-11-16.md): beams 0.25 x 0.54 m (TBDY 7.4.1.1, 3 x slab; was 0.40), columns 0.30 m confirmed (TBDY 7.3.1.1); pitched roofs 18.3 deg = 33 % (Bergama KAIP 6.5.16; was 30 deg); traditional houses get KAIP windows 0.80 x 1.60 m and doors 1.20 x 2.20 m; balcony rail 1.10 m (Planli Alanlar Md. 38(1)); pavement build-up 0.27 m (SECONDARY); ancient walls 4.0 m (press); plane 30 m, stone pine 15 m (vdberk lower end); kerb, garden wall, olive height, seating 12 x 30 now sourced; everything NOT FOUND stays ASSUMED; v1.45 (Aras 16 Nov 11:46-12:06 UTC): ONLY the site_alan square is built (MapBase frame; "i dont want anything that would be a burden to the pc and process out of the site_alan"): ground tiles clipped to it, buildings, streets, river, trees and objects inside it, everything AcBuild made outside it deleted; the ground per tile as coarse as the survey allows within +-2 % of the tile's height range (never under 0.05 m) on a 8 / 4 / 2 / 1 m grid of survey-TIN heights, every deviation logged ("keep it at the sweet spot"); pavements are Mesh-tool skins sewn to the road meshes at the kerb ("multiple meshes sewed together"); bank zones: grass skins between the survey top- and toe-of-slope lines (SEV_UST / SEV_ALT), cutting the ground; every tree (his planting, the survey trees, every survey olive symbol) a simplified real-life GDL object per species ("not cartoon ... sweet spot"); street furniture in 3D from the survey symbols (lamps, fountains, bus stops, statues, monuments, flag poles, minarets) as GDL objects; people and cars from his assets layer (shapes grouped and sorted by size); every element on a BGA layer of its part, layer combinations, one group per house, a per-part rebuild switch (cached/bergama_archicad_site/parts.txt); survey stairs on "BGA Stairs * existing (survey)"; sizes of objects ASSUMED; v1.44 (Aras 16 Nov 11:37-11:40 "columns should be travelling two floors they should be linked by the upper floor", "single beam travelling all across the grid"): house walls and frame columns one per storey (floor slab top to the next slab / roof), beams one per span between columns; windows, doors and balconies on their own storey's wall; (Aras 16 Nov 11:37 "proper ways of drawing ... to give the calculations right in the end and make it more properly displayed"): every Bergama building material gets an Archicad connection priority (MAT_PRIO: structure over masonry over screed over insulation over finishes; ground and water lowest), so junctions of walls, slabs, columns, beams and the ground clean up by material; (Aras 16 Nov 11:36 "why not meshes for bodies like water and such ?"): the river water is one Mesh body per river outline (was 5 m slab cells stepping down the river): its top = the season water level down the river, points every WATER_CELL_M, its body down to under the bed; the river bed body cuts it, so water stands only above the bed; (Aras 16 Nov 11:35 "you do have the real floor count information of somekind"): the survey's own floor-count labels (YAZI_KAT_ADEDI, 11,261 texts) give each footprint they stand in its floor count (was: the MapBase count, 7,131 houses without one); (Aras 11:25 "the stairs should follow the real survey data where possible") the survey building stairs (BINA_MERDIVEN, 17,392 step-edge lines with their heights) are grouped into flights and built tread by tread (Slab tool, top = the surveyed step height, down to the ground, cutting it); (Aras 16 Nov 11:33 "nothing should sink into ground if something is in ground it MUST use solid element operations"): every element that reaches below the surveyed ground cuts it: house walls whose foot is under the ground (uphill sides), survey kerbs and walls (dropped in v1.32 for speed; the tile index makes them cheap now), boulders and reed beds (ground and river bed), tree trunks; the log counts every kind; (Aras 16 Nov 11:32 "also roads should be the same way so does the pavement around it"): road and park cells are Mesh-tool bodies whose top is the surveyed ground (points every TOWN_PT_M, town blocks as holes), 0.30 m under its lowest point, and they cut the ground (SEO; was a slab shaped by the terrain); pavements from the survey kerb lines: a Slab-tool strip from each kerb piece to the nearest building face on its side (at most PAV_MAX_M, ASSUMED), top = kerb top, PAV_T_M build-up (ASSUMED); it cuts the ground and the road under it; (Aras 16 Nov 11:31 "3D should look like a real life site"): the materials outside his legend take the textured Archicad surfaces of the project (REAL_SURF: stucco, brick, concrete, clay roof tiles, asphalt, grass, earth, gravel, foliage, bark, water); his legend materials keep his colours; tree crowns foliage, trunks bark, water cells water; (Aras 16 Nov 11:31 "river sohuld be a proper river bed drawing with solid element operations rather than setting a slab and calling it a day"): a river bed body per river outline (Mesh tool, gravel): its top = the channel: the thalweg of each river section line (Sections cache z_th, linear between them down the river) at the centreline (Data/selinos_centreline.json), rising to the surveyed ground at his outline (parabolic cross-section ASSUMED), never above the surveyed ground; it cuts every ground tile upwards (SEO), so the ground opens into a real channel; plinths and terraces cut it, it cuts the water; the water cells reach down to the bed; (Aras 16 Nov 11:21 "sections dont cut trough the meshes"; found 11:31: v1.41 gave every Bergama material the cut fill "Solid + Dot & Dashed" in pen 1 (the first fill named "solid"), so cuts drew a pattern, not a hatch): each material gets the Archicad fill of what it is (ground Earth, concrete Structural Concrete, brick Common Brick, stone Rubble / Cut Stone, insulation Rigid Insulation, timber Wood ...), others the solid Foreground fill; (Aras 11:30 "give me a override that show those walls as a single solid hatch") the graphic override rule "Bergama - walls as one solid poche" (walls: cut fill Foreground solid, pen 21, no skin separators) in the combination "Bergama - solid walls"; (Aras 16 Nov 11:30 UTC "try to use generic composites like slum houses should have a one slum house composite, planned low rise need a composite that is for itself ... do good educated guesses accordingly what is highly used in turkey"): Archicad composites per MapBase fabric (regular = planned low-rise RC frame + hollow brick + EPS, block = apartment RC frame + AAC + EPS, selfbuilt = gecekondu pumice block, traditional = rubble stone + lime plaster (masonry: no RC frame), large = public RC frame + AAC + EPS), RC floor, clay-tile pitched roof and gravel flat roof composites; rafts, columns and beams in reinforced concrete; every layer thickness ASSUMED (educated guess of common Turkish practice, no source); the survey trees (SEMBOL_TEK_AGAC single trees, SEMBOL_YPDKN_AGAC / SEMBOL_YAP_DOKMEYEN evergreens) built as trunk + crown (heights ASSUMED); Aras 16 Nov 11:18 UTC "those rafts should connect columns and that columns should be connected by beams and etc.", "so the structures would be realistic"): every framed survey house (not the sacred / monument / Kizil Avlu masonry) gets a reinforced-concrete frame: Column-tool columns standing on its raft at every footprint corner, where a FRAME_SP_M grid line meets the footprint and at the grid crossings inside, full house height; Beam-tool beams under every floor slab and the roof along every footprint edge and every grid line inside (sizes and grid ASSUMED); centred in the wall thickness (ASSUMED: the walls lie inside the footprint line); Aras 16 Nov 11:16 UTC "the houses should sit on the ground they need to use solid element operations for cleaner looks and their foundation should be simplified raft foundation", "so the structures would be realistic"): every survey house stands on a raft (mat) foundation: one Slab-tool slab on its footprint, top = ground floor (survey ground at the centroid), bottom RAFT_T_M (ASSUMED) under the lowest survey ground under the footprint, so no side floats; it cuts the ground upwards (SEO, no ground inside the house); the walls start on the raft (were 1 m into the ground), the raft is the ground-floor slab; Aras 16 Nov 11:12 UTC "i dont want any gaps in the topography": ground tiles with no survey point of their own are filled from the survey triangulation; Aras 16 Nov 11:05-11:08 UTC "is it foolproof ?", "i do switch a lot between pc's", "i dont want to run two apps at the same time", "i'll be doing hand edits it needs to be safe from them"): the record of what AcBuild made lives in the pln itself: every element it makes carries Element ID "BGA-<fingerprint>@<3D box in cm>", so any PC, copy or recovery file finds its elements without the local cache; only elements with a BGA- Element ID are ever deleted (elements Aras draws are never touched; v1.34-v1.43 deleted every unrecorded wall, slab, roof ...); an element whose 3D box moved more than EDIT_TOL_M since AcBuild made it is hand-edited: locked, never deleted or replaced, and nothing new of its kind is made on it (FLAG count); the first v1.44 pass stamps the elements this PC's cache records; the survey is read from Rhino once and cached (cached/bergama_survey/survey.json with the ground triangles), so without Rhino AcBuild runs as plain Python with only Archicad open (python bergama_acbuild_v1_44.py); a Rhino model not in metres or a survey extent over 50 km stops the run; v1.43 (Aras 16 Nov 10:57 UTC "every slab should be drawn with slab tool, every column with column tool every roof is with roof tool"): the node buildings' folded roof facets are single-plane Roof-tool roofs (were meshes; a mesh only where Archicad refuses the roof, FLAG); a house roof Archicad refuses as a hipped roof is tried again as a single-plane Roof-tool roof before the slab fallback; bridge piers (Ulucami, Uc Kemer, new bridges) are Wall-tool piers (were stacked slabs), still cutting the ground; v1.42 (coordinator for Aras 16 Nov 09:50 UTC "build the whole site through Tapir at real 1:1", new empty Archicad file): WHOLE_SITE: everything inside the survey contour extent is built (was: the cut rectangles only): the ground as one gap-free surface of SITE_TILE_M tiles (shared edge points, control point every 10 m where no survey height) wherever the survey has heights, every survey building, the whole town ground, kerbs and walls; windows stay on the walls a section sees; ground tiles made in batches; solid element operations found through a tile index; its own cache folder (bergama_archicad_site, origin taken from bergama_archicad) and log; the project is neither saved nor published (Aras saves); v1.41 (Aras 15 Nov 23:50 section window: houses float, ground only a thin line): the ground is modelled again the full BACK_M behind each cut (GROUND_BEHIND_M = BACK_M) so the houses behind stand on their hillside; uncut surfaces filled in their own material colour, shaded (the hills read as a tone, not white blobs); the Bergama building materials get an explicit cut fill (solid fill, pen CUT_FILL_PEN, ASSUMED) as they were made with a cut surface only, so cut ground and cut walls drew no fill; v1.40 (runner 15 Nov 23:31: v1.38 said "model unchanged" and skipped its changes; its PDFs held almost nothing): the script version is part of the model fingerprint (a new version always goes through the element-by-element check, which keeps unchanged elements), and the distant area is off (everything in it is drawn with one fill and one pen); v1.39 (Aras 15 Nov 23:30 "why the outlines of the walls are not there for most"): uncut and distant elements draw with their own pens (the one uniform pen 81 / 102 is off), so every wall and roof edge keeps its own visible contour; v1.38 (Aras 15 Nov 23:13 "it is foreground/background issue ig. like get rid of those areas."): the ground is built only where a cut sees it cut (a strip from SIDE_M in front to GROUND_BEHIND_M behind each cut line) and under the river, in GROUND_TILE_M = 25 m tiles that still share their edge points; the hills behind a cut are no longer modelled, so nothing hides the buildings behind; his own section settings of 20:01 are back (uniform window-background fill, fade distant elements); v1.37 (Aras 15 Nov 23:10 "why these drawings look like this with white blobs over"): the ground behind a cut was filled with the window background (white) and, being a smooth mesh, had no outline, so the hills behind showed as white shapes hiding the houses; now uncut surfaces are filled with their own material colour, shaded, the distant-area option (always white in Archicad) is off, and the ground tiles carry the Sections ground colour; v1.36 (runner 15 Nov 23:05: partway through the v1.34 pass Archicad refused every new element, -2130312311 "Failed to create new ...", and every solid element operation): before each chunk the floor plan (story 0) is made the active window again, and a chunk Archicad refuses whole is tried once more after that; v1.35 (Aras 15 Nov 22:46 "get them as pdf", "dwg looks awful"): the Organizer / setup steps in the log say PDF; v1.34 (Aras 15 Nov 22:33 "archicad redraws take a lot of time can we have something faster ... not redrawing everything every single time"): every model element is kept by the hash of what it is made from; a pass makes only the elements whose data changed, deletes only the ones no longer wanted, makes solid element operations only for new elements and publishes only the sections whose line moved or that see a changed element; v1.33 (Aras 15 Nov 22:10 "move the node 6 to the building that is across the river": N6 now stands on an existing survey building): a survey building whose footprint lies more than COL_HALL_F inside a node building foot is left out (the node building takes its place); v1.32 (runner: the v1.31 publish stalled on its first section, Archicad 13 -> 21 GB in 10 min: one 2 km mesh with every survey point as the target of ~6000 solid element operations): the ground is the same one surface cut into GROUND_TILE_M tiles that share their edge points exactly (no gaps, one block to the eye), only tiles that touch a cut rectangle or the river; survey heights one per GROUND_SPOT_M m cell, control points every GROUND_GRID_M m where none; each solid element operation links an element only to the tile(s) it stands in; kerbs and survey walls no longer cut the ground (thousands of tiny operations)   # v1.31: v1.31 (Aras 15 Nov 21:19-21:20 "as you havent done solid element operations in archicad many of the drawings look weird. and ground has gaps in between", "it all should be one large block", "with many control points on it"): the ground is ONE terrain mesh over the whole survey box (every cut rectangle and the river; was 13 meshes per cut + 3 river meshes with gaps between them), its points every survey contour + spot height (one per 2 m cell) + a control point every GROUND_GRID_M m where the survey has none, a solid block GROUND_BASE_M m under its lowest point (was down to -5 m above sea level); solid element operations on that one ground for everything that stands in it: plinths, terraces, masterplan slabs, retaining walls (subtraction, as before), every building's ground slab (subtraction with upward extrusion: no ground inside a house), the Kızıl Avlu walls, bridge arches and piers, bank walls, kerbs and walls (subtraction), water (cut by the ground), road and park cells (shaped by the ground)   # v1.30: v1.30 (Aras 15 Nov 20:41 "what about roads ?", "and etc."): the existing town ground in the cut rectangles (where the terrain is): the MapBase street region (one region, the town blocks cut out as slab holes) and the parks as slabs in 20 m cells whose top the terrain shapes (SEO intersection), so they lie on the survey ground; survey kerbs, walls and ancient walls as Walls on the ground (heights ASSUMED); what the base map holds but is not built listed in the log   # v1.29: v1.29 (Aras 15 Nov 20:14-20:15 "build the selinos with everything in archicad like river bed, reed bed and everything like not a single beat skipped", "bridges and etc."): river bed mesh over his river outline (survey), water at each section line's own season level interpolated along the river (5 m cells, the ground cuts them by SEO), reed masses on his yosun rings (1.5 m ASSUMED), his stones and rocks of 1 m2 and more as boulders, his PLANTING_v13_1 trees as trunk Column + three crown slabs (heights ASSUMED), bank walls on his istinaat lines, his kopruler bridge outlines (picture-clip shapes too) as decks, the Ulucami and Üç Kemer bridges on their survey footprints with arches and piers (arch count / pier sizes ASSUMED, logged), piers under new bridges longer than 25 m; a layer audit of master.svg in the log; bridges / reeds / boulders no longer cut the terrain or get retaining walls; (runner, v1.18 rerun: 0 sections listed while 15 recorded, so all were remade and the Organizer step was undone) the floor plan is made the current window before the sections are listed, and 0 listed while some are recorded is treated as a listing failure (FLAG, recorded ones kept)   # v1.28: v1.28 (Aras 15 Nov 20:10 "also please solve these kinda collisions", his view: a hipped house inside the Kızıl Avlu walls): survey buildings overlapping the Kızıl Avlu hall by more than 10%% are left out (the hall stays), a footprint more than 50%% inside a bigger one is a duplicate and left out; counts logged; (Aras 20:10 "give both slabs and roofs to every building ... 3 storey ... 3 slabs") a floor slab per storey in every building (was: only the buildings a line cuts), flat roofs as 2 deg single-plane Roof-tool roofs   # v1.27 (Aras 15 Nov 20:07 "use solid element operations where necceseary"): every canopy plinth, node plinth and masterplan slab (terraces included) cuts the terrain mesh of each cut it stands in (Tapir CreateSolidElementLinks, subtraction); (Aras 20:08 "use retaining walls where neccesery") stone retaining walls along slab edges where the ground outside differs from the slab top by more than 0.60 m (ASSUMED)   # v1.26 (Aras 15 Nov 20:06 "dont do these kinda extereme angles keep it minimal like the second image"): fold rise 0.6 m (was 1.8 m), and no facet edge steeper than 8 deg (low corners on falling ground are raised to it, so every clearance still holds)   # v1.25 (Aras 15 Nov 20:05 "draw their roofs with roof tool columns with column tool, beams with beam tool etc. so intersections would look proper"): canopy facets = single-plane Roofs (pivot line through the low corner, slope of the facet plane), louvres = timber Beams (horizontal slats every 0.6 m under each facet); columns (Column tool), arms (Beam tool), plinths/decks/planters (Slab tool), glazed rooms (Wall + Window) as before; a facet Archicad refuses as a roof falls back to a mesh (FLAG)   # v1.24 (Aras 15 Nov 20:01 "use these settings for archicad sections"): his Section Selection Settings on every section (cut elements in their pens, uncut = uniform pen colour fill + line pen 81, fade distant elements on with line pen 102, no boundary contours); publishes once for the new settings   # v1.23 (Aras 15 Nov 20:00 "archicad is missing the ground in sections ... i want real 1:1 drawing in archicad"): the survey terrain mesh is built again, one per cut rectangle (10 m in front of the line to 200 m behind, survey contours + spot heights, solid with skirt), so every Archicad section has a cut ground and the hillside under its houses   # v1.22 (Aras 15 Nov 19:48 UTC "optimize the scripts to be much much faster", item 3 "run the Rhino-only slides alongside the Archicad steps"): run from the chain (__main__), the Rhino part (survey read, TIN) runs as before, then the Archicad part (pure Python + Tapir, no Rhino call) goes on in a background thread so Rhino is free for the next page script; the log reads "RUNNING ..." until it ends (same lines as before); a file cached/_chain/acbuild_foreground.txt keeps the old one-piece run; the Grasshopper button runs in one piece as before; v1.21 (v1.18 run 15 Nov 19:23 UTC: no bridge and no stepped terrace was built: his bridge outlines (kopruler path) and stepped-terrace outlines (begum su merdiven outline) are drawn without fill): those layers are built from their closed outlines (the outermost rings only, MasterplanBase v1.9 keeps the paint-less bridge rings); a bridge as a 0.50 m stone deck whose top is the highest survey ground under its outline (the banks it spans, not the river bed); BUILD_SIG geometry-9; v1.20   # v1.20 (Aras 15 Nov 19:18: the publisher set may be PDF): published PDFs count as the kept output   # v1.19 (Aras 15 Nov 19:09-19:11 UTC "1.2meter depth is fine however think it like 15x30 steps merge into single seating", "circulation wise"): his stepped terraces (begum su merdiven, the light stone picture) built as seating tiers stepping down to the river: each tier 1.20 m deep = four 30 cm treads merged, 0.48 m high = four 12 cm risers (Aras 19:13 "make the height of the steps is 12"; the 12 x 30 stair pitch kept), tiers cut from his own outline across the direction to the nearest point of his river outline (su_outline), lowest tier on the lowest survey ground of the piece, none above the highest; the stair aisles themselves are not placed (no aisle drawn in his masterplan); materials by each layer's own picture colour: teras = wood deck ("decks are wooden"), iskele kenari = grey paving CECFCE; v1.18 (Aras 15 Nov 18:12-18:17 UTC texture legend: "this stands for regular bridges", "historic buildings are in a shade of red", "our buildings are white blues are glasses", "these are decksn", "this is shading", "these are reed beds", "this is stepped terrace that goes into the river"): Archicad surfaces + building materials named "Bergama ..." in his legend colours (median colours sampled from his legend pictures), given to the elements as they are made: bridges (kopruler pieces) stone, stepped terraces (teras, begum su merdiven) light stone, decks (iskele kenari, canopy decks, planters, louvres) timber, reed beds (su bitkii) reed green, canopy facets white, Y columns grey frame, our buildings (node buildings, glazed rooms) white, historic buildings (sacred / monument houses, Kızıl Avlu) red; every glass surface of the project in his glass blue; an element Tapir refuses with a material is made again without it (FLAG); BUILD_SIG geometry-7 (one rebuild); v1.17 (Aras 15 Nov 17:24 UTC "any drawing that has building in it you should use the drawing that comes out of archicad"): the node building FLOOR PLANS from Archicad too: one Archicad story per floor of each node building (Tapir SetStories; story 0 kept, story level lines off in the sections), so each floor plan cuts its own building; a View Map view <N>-P<floor> per story, published with the sections (one-time Organizer step again), two registration squares (1.0 m and 0.5 m) 6 m off opposite corners of the building on every floor; BUILD_SIG geometry-6 (one rebuild); v1.16 (Aras 15 Nov 17:32 UTC "make sure archicad drawing is %100 pinpoint accurate to our masterplan"): his master.svg pieces inside the working area built in Archicad on his own points (slabs per layer, on the survey ground), canopies held within 0.05 m of his kanopi line, and an accuracy check after every build: each piece read back from Archicad and compared with master.svg, any point more than 5 cm off FLAGged, report in mp_accuracy.json; BUILD_SIG geometry-5 (one rebuild); v1.15 (Aras 15 Nov 17:27 UTC "draw these buildings in archicad and insert that drawing into all sections ... archicad is hella lot more detailed"): the context houses get more detail for the section elevations: a door on the ground floor of the longest wall a cut sees, windows on every wall a cut sees at any angle, balconies (slab + rail) on every other window bay of blocks of 3+ floors, a cornice band under every flat roof; a house with no recorded floor count is built as 1 floor (ASSUMED, logged) instead of left out; sizes are drawing rules, not surveyed; BUILD_SIG geometry-4 (one rebuild); v1.14 (Aras 15 Nov 17:24 UTC "any drawing that has building in it you should use the drawing that comes out of archicad"): the six node buildings built in Archicad as the node slides design them (placed by Perspectives, rooms from nodes common BUILD), each with a cut view <N>-BX and an elevation view <N>-BE in the "Bergama sections" folder (published with the sections); v1.13 = v1.13 (Aras 15 Nov 16:31-16:32 UTC "Make canopies top view match with masterplan", "Get structrual idea from the photo i have sent you and invent from there"): every canopy built on his own filled kanopi ring (no hull, no merging, outline within 0.25 m), facets by ear clipping with his fold ends on the outline, low / high vertices alternating round it, Y columns under the low vertices 1.2 m inside (4-10 m apart, arms toward the neighbouring vertices), plinth + deck bays between the columns; rooms and planters only where they fit inside; v1.12 (v1.11 publish run: 10.5 min for 13 DWGs): no vector sun shadows in the section views; a change of the view settings (SEC_SIG) publishes once even when the model is unchanged   # v1.11 (run of v1.10: the Archicad 29 API refused "CutPlane" too): sections listed through Tapir GetElementsByType (CutPlane)   # v1.10 (Aras 15 Nov 15:00 "you need to make archicad runs faster"): the model is rebuilt only when its inputs changed (buildings from MapBase, cut lines, masterplan canopies, Sections levels, BUILD_SIG) or Archicad holds other element counts; with the model and sections unchanged nothing is published either (the last DWGs are kept); model time logged; sections listed as element type CutPlane (v1.9 run: "Section" is not an API type)   # v1.9 (15 Nov: Archicad reopened from a recovery file: new GUIDs, the build doubled, 9 section views twice): the previous model is cleared by element type (windows, walls, slabs, roofs, meshes, columns, beams), not by recorded GUIDs; when the project\'s sections differ from the recorded ones, all sections and the "Bergama sections" View Map folder are made again (FLAG: refresh the publisher set)   # v1.8 (15 Nov: a refreshed publisher set held the whole project as PDF + DWG and Archicad hung an hour; the pln reopened without the build after a restart): the project is saved (Tapir SaveProject) before publishing, and only the set's items of our sections are published (selectedNavigatorItemIds); a set holding other items is not published whole   # v1.7 (Sections thread, run of v1.28.2: houses up the hill float, the survey TIN does not reach that hill): the ground behind each cut in depth bands (10-50, 50-100, 100-200, 200-400 m, 400 m to the farthest building), each the highest survey ground of the band raised to the base of every building standing in it, so every house has ground under it; written to acbuild.json cuts[].bands   # v1.6 (also: the ground-behind profile reaches 1000 m, as houses of other cuts beyond 200 m show in the sections); v1.6 (Aras 15 Nov 09:52-10:29 "draw our canopies much better like designed ones" / "Some closed areas underneath" / canopies in Archicad "yes please"): his master.svg canopies (kanopi layer) built as his reference: folded triangle-facet roof (meshes) with a timber louvre layer under it, Y steel columns (trunk + 2 arms) under the valleys on a 12 m bay, timber deck on a stone plinth bay by bay, a glazed room in every other bay where the floor is >= Q500 + 0.60 m, timber planters in the open bays; heights as Sections v1.28.2 (DfT 2.30 m clear, EA 0.60 m over Q500, ridge +1.8 m ASSUMED)   # v1.5 + Kızıl Avlu: the main hall outline(s) from the MasterplanBase cache (Sections library red_hall_load), roofless walls 19 m (Wikipedia, Red Basilica: "Its walls still survive up to a height of 19 metres"), no windows, no roof; v1.5 (15 Nov run 7: houses beyond the 200 m depth drawn as floating outlines): no marked distant area (only the 200 m behind each cut is drawn); publishing may take 30 min (the set grew)   # v1.4 v1.4 (15 Nov: Sections v1.18 moved the N4 lines): the Archicad origin is kept from the first run; a section whose line moved is deleted and made again on the new line (its view too), with a FLAG to refresh the publisher set   # v1.3 (run 4: houses 200 m behind stood in the sky, the hill under them was not drawn): per cut the ground behind (highest survey ground 10-200 m behind, every 2 m) written to acbuild.json for SectionsAC   # v1.2 (SectionsAC run 3: the DWGs held only the roofs = the one element type without a BG layer, so the BG layers are not shown in the views): every element on the tool default layers; registration blocks at -50 m (found by geometry); no terrain mesh (our ground is drawn instead)   # v1.1 (14 Nov run 1): mesh without layerIndex (Tapir schema), hipped roofs as one-level polyroofs, footprints cleaned (slab failures)
GH_LABEL = "AcBuild"
OUT_FOLDER = "bergama_archicad_site"   # v1.42: own cache (the sections project keeps bergama_archicad)
LOG_NAME = "bergama_acbuild_site_log.txt"
GH_INPUTS = {}
_BG = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
BERGAMA_ROOT = os.path.join(_BG, "Project Files") if os.path.isdir(os.path.join(_BG, "Project Files", "scripts")) else _BG   # v1.60
CACHE_DIR = os.path.join(BERGAMA_ROOT, "cached", OUT_FOLDER)
OUT_DIR = CACHE_DIR
DWG_DIR = os.path.join(CACHE_DIR, "dwg")
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
LIB_GLOB = os.path.join(BERGAMA_ROOT, "scripts", "bergama_sections_v*.py")

PORTS = range(19723, 19744)        # Archicad's JSON API ports (the first Archicad opened takes 19723)
SHADOWS = False                    # v1.12: vector sun shadows off in the section views (publish took 10.5 min)
SEC_SIG = "sections-aras-2026-11-15-pdf-strip-ownpens-nodistant"    # v1.12: change with the section view settings (forces one publish)
BUILD_SIG = "acbuild-geometry-tiles-1"   # v1.32: ground tiles; v1.31: one ground + SEO; v1.30: town ground; v1.29: the whole Selinos; v1.28: collisions; v1.27: SEO terrain cuts + retaining walls; v1.26: minimal folds; v1.25: canopies with Roof/Beam tools; v1.21: bridges + stepped terraces from outlines; v1.19: seating tiers; v1.18: materials; v1.17: building stories; v1.16: masterplan pieces; v1.15: house detail;   # v1.14: node buildings; v1.13 = v1.13: canopies on his outlines; v1.10: change when the element-making code changes (forces a rebuild)
CLEAR_TYPES = ["Window", "Door", "Wall", "Slab", "Roof", "Mesh", "Column", "Beam", "Object", "Railing"]   # v1.83: + Railing   # v1.9: what AcBuild makes
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
ROOF_DEG, EAVE_M = 18.3, 0.4       # v1.46: 18.3 deg = 33 %, the Bergama KAIP 6.5.16 cap for the historic core, inside
                                   # Marsilya tile 30-35 % (Ozyigit) (research pack v3 R9; was 30 deg = 58 %, steeper
                                   # than every source); eave 0.40 m still ASSUMED (R9: NOT FOUND)
WIN_W, WIN_H, WIN_SILL, WIN_STEP = 1.2, 1.4, 0.9, 3.0   # Sections drawing rule (not surveyed; R9: NOT FOUND outside the core)
DOOR_W, DOOR_H = 1.0, 2.2          # v1.14: m, ground-floor door (drawing rule; R9: exit door clear width 0.80-1.20 m, fire reg. Md. 33(5)(b))
# v1.46 traditional houses (historic core, Bergama KAIP, research pack v3 R9): window narrow side >= 0.80 m, long side
# <= 1.60 m, ratio 1/1.7-1/2 (6.5.14) -> 0.80 x 1.60 (ratio 1/2, chosen within the limits; height still capped at half
# the storey); door width >= 1.20 m, height <= 2.40 m (6.5.13) -> 1.20 x 2.20
WIN_W_TRAD, WIN_H_TRAD, DOOR_W_TRAD, DOOR_H_TRAD = 0.80, 1.60, 1.20, 2.20
BAL_D, BAL_W, BAL_T, RAIL_H = 1.2, 1.8, 0.18, 1.10  # v1.14: m, balcony depth / width / slab / rail; v1.46: rail 1.10 m
                                   # (Planli Alanlar Md. 38(1) railing >= 1.10 m, research pack v3 R4 / R9); depth,
                                   # width ASSUMED (national limits NOT FOUND; balconies are on blocks, not the core)
BAL_FLOORS = 3                     # v1.14: balconies on blocks from 3 floors
HOUSE_CORNICE = False   # v1.85
CORNICE_M, CORNICE_T = 0.25, 0.3   # v1.14: m, cornice projection / depth under a flat roof (drawing rule)
FRAME_SP_M = 5.0                   # v1.44: m, column grid of the house frames: ASSUMED (typical RC span, no source)
FRAME_COL_M = 0.30                 # v1.44: m, square column side; v1.46: = TBDY 7.3.1.1 minimum side 300 mm (via ideCAD, SECONDARY, research pack v3 R2)
FRAME_BEAM_W, FRAME_BEAM_H = 0.25, 0.54   # v1.46: width = TBDY 7.4.1.1 minimum 250 mm; depth = 3 x the 0.18 m floor
                                   # slab (TBDY 7.4.1.1: >= 300 mm and >= 3 x slab, <= 3.5 x width = 0.875 m; via ideCAD,
                                   # SECONDARY, R2); was 0.40 (below the rule). The 0.18 m slab itself stays ASSUMED
RAFT_T_M = 0.40                    # v1.44: m, raft foundation thickness under the lowest ground: ASSUMED (no source)
WALL_T, PLINTH = 0.3, 1.0          # m wall thickness; m the walls start below the ground at the centroid
GRID_M = 2.0                       # m: spot heights thinned to one per cell for the terrain mesh
REG_Z = -50.0                       # m above sea level: the registration blocks sit here (below every survey height)
SUN = (135.0, 35.0)                # deg azimuth to the cut plane, altitude: the shadow light (a drawing choice)
CHUNK = 150                        # elements per Tapir call (v1.48: was 400; the Desktop has 24 GB RAM, the laptop 96 GB)
MIN_FREE_GB = 3.0                  # v1.48: free RAM below this before a Tapir call = wait, then a clean stop (FLAG)
WAIT_FREE_S = 120                  # v1.48: s to wait for RAM to come back before stopping
PROGRESS_FILE = os.path.join(BERGAMA_ROOT, "logs", "bergama_acbuild_progress.txt")   # v1.60


class ArchicadGone(RuntimeError):
    """v1.50: Archicad no longer answers on its port (crashed or closed)"""


def _ac_gone(ex):
    """v1.50: True when the error means nothing listens on Archicad's port any more"""
    s = (u"%s %s" % (type(ex).__name__, ex)).lower()
    return any(k in s for k in (u"connectionrefused", u"connection refused", u"actively refused", u"winerror 10061",
                                u"connectionreset", u"forcibly closed", u"winerror 10054", u"remotedisconnected"))


class LowMemoryStop(RuntimeError):
    """v1.48: raised when free RAM stays under MIN_FREE_GB; a rerun picks up where this one stopped"""


def _free_gb():
    """v1.48: free physical RAM in GB (Windows GlobalMemoryStatusEx; None elsewhere)"""
    try:
        import ctypes

        class _MS(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
        m = _MS()
        m.dwLength = ctypes.sizeof(_MS)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
        return m.ullAvailPhys / 1073741824.0
    except Exception:
        return None


def _total_gb():
    """v1.57: total physical RAM in GB (Windows; None elsewhere)"""
    try:
        import ctypes

        class _MS(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
        m = _MS()
        m.dwLength = ctypes.sizeof(_MS)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
        return m.ullTotalPhys / 1073741824.0
    except Exception:
        return None


BIG_RAM = (_total_gb() or 0) > 64.0               # v1.57: the laptop (96 GB) takes bigger batches; the Desktop (24 GB) not
LABEL_CHUNK = 2000 if BIG_RAM else 500            # v1.57: Element ID values per call (was 500)
LAYER_CHUNK = 2000 if BIG_RAM else 1000           # v1.57: layer changes per call (was 1000)


def _progress(text):
    """v1.48: one line per Tapir chunk, written at once, so a crash still leaves the last step on disk"""
    try:
        with open(PROGRESS_FILE, "a", encoding="utf-8") as f:
            f.write(u"%s  %s\n" % (time.strftime("%H:%M:%S"), text))
    except Exception:
        pass


def _ram_guard(what):
    """v1.48: wait for free RAM, else stop cleanly (every element made so far keeps its BGA ID, so the next run resumes)"""
    if _STOPPED:                             # a stop already happened: no more waiting, stop every later call at once
        raise LowMemoryStop(_STOPPED[0])
    fr = _free_gb()
    if fr is None or fr >= MIN_FREE_GB:
        return fr
    _progress(u"low RAM %.1f GB free before %s: waiting up to %d s" % (fr, what, WAIT_FREE_S))
    t0 = time.time()
    while time.time() - t0 < WAIT_FREE_S:
        time.sleep(10)
        fr = _free_gb()
        if fr is not None and fr >= MIN_FREE_GB:
            return fr
    _STOPPED.append(u"free RAM %.1f GB stayed under %.1f GB before %s: stopped cleanly; close other apps and run "
                    u"again, or list fewer parts in parts.txt" % (fr or 0.0, MIN_FREE_GB, what))
    _progress(u"FLAG " + _STOPPED[0])
    try:                                     # v1.49: stamp what this pass made, so the next run resumes (v1.48 did not)
        if _AC and PID[0]:
            pr_ = [(it[1], it[0]) for it in ITEMS if it[1] in NEW_G]
            n_ = stamp(_AC[0], PID[0], pr_) if pr_ else 0
            _progress(u"stop: %d of %d element(s) made in this pass stamped with their BGA Element ID" % (n_, len(pr_)))
    except Exception as ex:
        _progress(u"FLAG stop: elements not stamped (%s): close this project without saving and start fresh" % ex)
    raise LowMemoryStop(_STOPPED[0])


_STOPPED = []                              # v1.48: the low-RAM stop message, once it happened
_AC = []                                   # v1.49: the Archicad connection (for the stamp at a stop)
CACHE_CMDS = ("CreateSlabs", "CreateWalls", "CreateMeshes", "CreateColumns", "CreateBeams", "CreateRoofs",
              "CreateWindows", "CreateDoors", "CreateObjects")   # v1.34: model elements kept between passes by the hash of their data
KEEP = {}                          # v1.34: hash -> [guid] of the last pass, still in the model (main fills it)
ITEMS = []                         # v1.34: this pass [hash, guid, bbox Archicad m]
NEW_G = set()                      # v1.34: guids made in this pass
STEP_T = {}                        # v1.82: step / Tapir command -> seconds spent (log only)
SRC_OF = {}                        # v1.78: guid -> (command, key, item, what) of this pass (to make a vanished element again)
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
        _AC[:] = [self]                                   # v1.49

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
        t0_ = time.time()                                 # v1.82: time per Tapir command (log only)
        try:
            return self._t(name, params, timeout)
        finally:
            if not name.startswith("Create"):
                k_ = u"Tapir " + name
                STEP_T[k_] = STEP_T.get(k_, 0.0) + time.time() - t0_

    def _t(self, name, params=None, timeout=600.0):
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
        """v1.82: timed per step (log only); v1.83: the site_alan rule (_in_site) on every element first"""
        t0_ = time.time()
        try:
            keep_ix, items2 = _in_site(name, items, what, self.log)
            if len(keep_ix) == len(items):
                return self._create_kept(name, key, items2, what)
            res_ = self._create_kept(name, key, items2, what) if items2 else []
            out_ = [None] * len(items)                    # refused-like None for the ones left out
            for k_, g_ in zip(keep_ix, res_):
                out_[k_] = g_
            return out_
        finally:
            STEP_T[what] = STEP_T.get(what, 0.0) + time.time() - t0_

    def _create_kept(self, name, key, items, what):
        """v1.34: an element whose data is the same as one of the last pass that is still in the model is kept (its
        guid returned, nothing sent to Archicad); only the others are made"""
        if name not in CACHE_CMDS:
            return self._create(name, key, items, what)
        import hashlib
        hs = [hashlib.sha1((name + json.dumps(it, sort_keys=True, default=str)).encode("utf-8")).hexdigest()
              for it in items]
        out, todo, n_out = [], [], 0
        prt = part_of(what)                               # v1.45
        for i, h in enumerate(hs):
            g = KEEP[h[:16]].pop() if KEEP.get(h[:16]) else None   # v1.44: the fingerprint in the Element ID
            out.append(g)
            if not g and ((PARTS and prt not in PARTS) or (SCOPE[0] == "site" and prt == "buildings" and not SITE_BUILDINGS)):
                # v1.45: this part is not rebuilt in this pass; v1.52: our buildings live in their own file
                n_out += 1                                # v1.54: not built here, so not "kept"
                continue
            if not g:
                bb_ = _bbox(items[i]) if LOCKED_BB else None
                if bb_:                                   # v1.44: a hand-edited element of this kind stands here
                    cx_, cy_ = (bb_[0] + bb_[2]) / 2.0, (bb_[1] + bb_[3]) / 2.0
                    if any(t_ == TYPE_OF.get(name) and b_[0] <= cx_ <= b_[2] and b_[1] <= cy_ <= b_[3]
                           for t_, b_ in LOCKED_BB):
                        N_LOCKSKIP[0] += 1
                        continue
                todo.append(i)
        kept = len(items) - len(todo) - n_out             # v1.54: only elements found in the model by Element ID
        N_KEPT[0] += kept
        if todo:
            new = self._create(name, key, [items[i] for i in todo], what)
            for i, g in zip(todo, new):
                out[i] = g
                if g:
                    NEW_G.add(g)
        if kept:
            self.log.append(u"%s: %d kept from the last pass (same data, found in the model by Element ID)" % (what, kept))
        if n_out:                                         # v1.54
            self.log.append(u"%s: %d not built in this file (part \"%s\" %s)" % (
                what, n_out, prt, u"lives in Bergama_buildings.pln" if SCOPE[0] == "site" and prt == "buildings"
                else u"not rebuilt in this pass (rebuild switch)"))
        for h, g, it in zip(hs, out, items):
            if g:
                ITEMS.append([h, g, _bbox(it)])
                PART_G[g] = prt                           # v1.45
                SRC_OF[g] = (name, key, it, what)         # v1.78
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
            fr_ = _ram_guard(what)                   # v1.48
            _progress(u"%s: %s %d-%d of %d (free RAM %s GB)" % (what, name, i + 1, i + len(part), len(items),
                                                                 u"?" if fr_ is None else u"%.1f" % fr_))
            for k_try in (0, 1):                     # v1.36: new elements go into the floor plan's database
                try:
                    self.t("ChangeWindow", {"windowType": "FloorPlan", "storyIndex": 0})
                except Exception:
                    pass
                try:
                    r = self.t(name, {key: part})
                    lst = r.get("elements") or r.get("elementIds") or []
                except Exception as ex:
                    if _ac_gone(ex):                  # v1.50: Archicad closed / crashed: stop now, no futile retries
                        _progress(u"FLAG Archicad stopped answering during %s (%s)" % (what, ex))
                        raise ArchicadGone(u"Archicad stopped answering during %s, %s %d-%d of %d (%s). It has "
                                           u"most likely crashed: restart it with a new empty project and run "
                                           u"again" % (what, name, i + 1, i + len(part), len(items), ex))
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
             "park": "Grass - Green", "ground": "Grass - Brown",
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
    prt = None
    if "-" in h:                                          # v1.45: "BGA-<part>-<fingerprint>@<box>"
        prt, h = h.rsplit("-", 1)
    return h[:16], (bb if bb and len(bb) == 6 else None), prt


def stamp(ac, pid, pairs):
    """v1.44: write "BGA-<fingerprint>@<its 3D box now>" into each element's Element ID; returns how many"""
    _progress(u"Element IDs: reading %d 3D boxes" % len(pairs))   # v1.57
    bbs = read_bb(ac, [g for g, h in pairs])
    vals = [{"elementId": {"guid": g}, "propertyId": {"guid": pid},
             "propertyValue": {"value": ID_PREFIX + (PART_G[g] + u"-" if PART_G.get(g) else u"") + h[:16] + (u"@" + u",".join(str(int(round(v * 100))) for v in bbs[g])
                                                              if g in bbs else u"")}} for g, h in pairs]
    n = 0
    for i in range(0, len(vals), LABEL_CHUNK):
        part, ok = vals[i:i + LABEL_CHUNK], 0
        _progress(u"Element IDs %d-%d of %d" % (i + 1, i + len(part), len(vals)))   # v1.57
        try:                                              # v1.55: Tapir first (it takes {"value": text})
            r = ac.t("SetPropertyValuesOfElements", {"elementPropertyValues": part}, 900.0)
            res = r.get("executionResults") or []
            ok = sum(1 for e in res if isinstance(e, dict) and e.get("success"))
            if not ok and not STAMP_ERR[0]:
                STAMP_ERR[0] = u"Tapir: %s" % json.dumps(res[:1] or r)[:300]
        except Exception as ex:
            STAMP_ERR[0] = STAMP_ERR[0] or u"Tapir: %s" % ex
        if not ok:                                        # v1.55: the Archicad API wants a typed string value
            try:
                pt_ = [dict(v_, propertyValue=dict(type="string", status="normal", value=v_["propertyValue"]["value"]))
                       for v_ in part]
                r = ac.api("API.SetPropertyValuesOfElements", {"elementPropertyValues": pt_}, 900.0)
                res = r.get("executionResults") or []
                ok = sum(1 for e in res if isinstance(e, dict) and e.get("success"))
                if not ok and u"API" not in STAMP_ERR[0]:
                    STAMP_ERR[0] += u" | API: %s" % json.dumps(res[:1] or r)[:300]
            except Exception as ex:
                if u"API" not in STAMP_ERR[0]:
                    STAMP_ERR[0] += u" | API: %s" % ex
        n += ok
    return n


STAMP_ERR = [u""]                                 # v1.54: first reason a stamp failed (logged as a FLAG)


def stamp_log(log, n, total, what):
    """v1.54: the stamp count, plus a FLAG with the reason when some failed"""
    log.append(u"Element IDs: %d of %d %s" % (n, total, what))
    if n < total:
        log.append(u"FLAG Element IDs: %d not stamped (%s): the next run cannot recognise them and makes them "
                   u"again" % (total - n, STAMP_ERR[0] or u"no reason given"))


SYM_LAYERS = ("SEMBOL_ZEYTINLIK", "SEMBOL_CAD_SOKAK_LAM", "SEMBOL_CESME", "HIDRO_CESME", "SEMBOL_DURAK",
              "SEMBOL_HEYKEL", "SEMBOL_ABIDE", "SEMBOL_BAYRAK_DIREGI", "SEMBOL_MINARE", "HIDRO_HAVUZ")
SYM_POLY = ("HIDRO_HAVUZ",)                         # v1.45: read as outlines
SYM_READ = [None]


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
    sym = {}                                              # v1.45: symbol positions [x, y, angle] per layer
    for nm in SYM_LAYERS:
        li = d.Layers.FindByFullPath(nm, -1)
        if li < 0:
            continue
        out = sym.setdefault(nm, [])
        for o in d.Objects.FindByLayer(d.Layers[li]):
            g = o.Geometry
            if isinstance(g, Rhino.Geometry.InstanceReferenceGeometry):
                p = g.Xform * Rhino.Geometry.Point3d(0.0, 0.0, 0.0)
                out.append([round(p.X, 3), round(p.Y, 3), round(math.atan2(g.Xform.M10, g.Xform.M00), 4)])
            elif isinstance(g, Rhino.Geometry.Point):
                out.append([round(g.Location.X, 3), round(g.Location.Y, 3), 0.0])
            elif isinstance(g, Rhino.Geometry.Curve) and nm in SYM_POLY:
                pl = [g.PointAt(g.Domain.T0 + (g.Domain.T1 - g.Domain.T0) * k / 24.0) for k in range(25)]
                out.append([[round(q.X, 3), round(q.Y, 3)] for q in pl])
            elif isinstance(g, Rhino.Geometry.Curve):
                c = g.GetBoundingBox(True).Center
                out.append([round(c.X, 3), round(c.Y, 3), 0.0])
    log.append(u"survey symbols: %s" % u", ".join(u"%s %d" % (k, len(v)) for k, v in sorted(sym.items())))
    SYM_READ[0] = sym
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


def _clip_convex(P, C):
    """v1.45: polygon P clipped to the convex polygon C (Sutherland-Hodgman)"""
    if not P or len(C) < 3:
        return list(P)
    sg = 1.0 if area(C) > 0 else -1.0
    out = list(P)
    for a, b in zip(C, C[1:] + C[:1]):
        inp, out = out, []
        if not inp:
            break
        side = lambda p: sg * ((b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])) >= -1e-9
        for p, q in zip(inp, inp[1:] + inp[:1]):
            sp_, sq_ = side(p), side(q)
            if sp_:
                out.append(p)
            if sp_ != sq_:
                dx, dy = q[0] - p[0], q[1] - p[1]
                den = (b[0] - a[0]) * dy - (b[1] - a[1]) * dx
                if abs(den) > 1e-12:
                    t = ((b[0] - a[0]) * (a[1] - p[1]) - (b[1] - a[1]) * (a[0] - p[0])) / den
                    out.append((p[0] + dx * t, p[1] + dy * t))
    return out


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
    "floor_canopy": (u"Bergama floor - canopy: timber deck on stone plinth", "Slab",   # v1.73: was two slabs
                     [("Finish", "timber", 0.12), ("Core", "terrace_stone", 0.95)]),   # = CAN_DECK_M, CAN_PLINTH_M + 0.5
    "floor_rc": (u"Bergama floor - RC slab, screed", "Slab",
                 [("Finish", "screed", 0.05), ("Core", "rc", 0.18), ("Finish", "plaster", 0.02)]),
    "roof_tile": (u"Bergama roof - clay tile on timber", "Roof",
                  [("Finish", "rooftile", 0.03), ("Core", "rooftimber", 0.20), ("Finish", "plaster", 0.02)]),
    "roof_flat": (u"Bergama roof - gravel, XPS, RC", "Roof",
                  [("Finish", "gravel", 0.05), ("Other", "xps", 0.08), ("Finish", "screed", 0.05), ("Core", "rc", 0.12)]),
}
WALL_COMP = {"regular": "wall_regular", "block": "wall_block", "selfbuilt": "wall_selfbuilt",
             "traditional": "wall_traditional", "large": "wall_large"}   # MapBase fabric -> wall composite
CONTEXT_FRAMES = False   # v1.49 (Desktop 24 GB: the v1.48 run hit 12 GB at 9,600 of 45,853 columns): no RC columns /
                         # beams inside the existing survey houses (hidden in their walls); rafts stay; True = v1.48
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


CUT_HOUSE_GREY = 0.68             # v1.56: the background house walls in Aras's N1-A PDF (18 Nov) read #AAAAAA-#B1B1B1
SEC_COMBO = u"Bergama - sections"  # v1.56: graphic override combination set on every section view


def setup_cut_house_override(ac, log):
    """v1.56 (Aras 18 Nov 07:59 "sectioning the houses look weird"; standing rule: cut houses drawn like the background
    houses): in the section views the cut survey houses (envelope + structure layers, rafts included) get one grey
    "Background" fill and the thin uncut line pen 81, so they read as grey silhouettes, not as cut construction"""
    try:
        have = ac.t("GetGraphicOverrideRules", {}).get("graphicOverrideRules") or []
        nm_ = u"Bergama - cut houses as background"
        rid = next((r["graphicOverrideRuleId"] for r in have if r.get("name") == nm_), None)
        if rid is None:
            fl_ = dict((a.get("name"), a) for a in (ac.t("GetAttributesByType", {"attributeType": "Fill"}).get(
                "attributes") or []))
            ft = {"cutFill": True, "coverFill": False, "draftingFill": False}
            r = ac.t("CreateGraphicOverrideRules", {"graphicOverrideRules": [dict(
                name=nm_, ruleGroupName=u"Bergama",
                criterion={"or": [{"layer": LAYER_NAME["houses"]}, {"layer": LAYER_NAME["structure"]}]},
                style=dict(fillType=fl_[u"Background"]["attributeId"], fillTypeAppliesTo=ft,
                           fillBackgroundColor=dict(red=CUT_HOUSE_GREY, green=CUT_HOUSE_GREY, blue=CUT_HOUSE_GREY),
                           fillBackgroundPenAppliesTo=ft, lineMarkerTextPen=81, showSkinSeparators=False))]})
            rid = r["graphicOverrideRuleIds"][0]["graphicOverrideRuleId"]
        cb_ = [c_ for c_ in (ac.t("GetGraphicOverrideCombinations", {}).get("graphicOverrideCombinations") or [])
               if c_.get("name") == SEC_COMBO] if ac.has("GetGraphicOverrideCombinations") else []
        if not cb_:
            ac.t("CreateGraphicOverrideCombinations", {"graphicOverrideCombinations": [dict(
                name=SEC_COMBO, graphicOverrideRuleIds=[{"graphicOverrideRuleId": rid}])]})
        log.append(u"graphic override (v1.56): rule \"%s\" (cut houses: one grey fill, pen 81) in combination \"%s\"" % (
            nm_, SEC_COMBO))
        return True
    except Exception as ex:
        log.append(u"FLAG cut-house override not made (%s): the cut houses keep their cut fills" % ex)
        return False


def _wt(b):
    """v1.44: wall thickness of a house: its composite's, else WALL_T"""
    k = WALL_COMP.get(b.get("fab"))
    return COMP_T.get(k, WALL_T) if b.get("fab") not in HERITAGE_FABS else WALL_T


def _inset(R, d):
    """v1.85: the counter-clockwise ring R pulled in by d (mitred corners, as the frame's centre line)"""
    out = []
    n = len(R)
    for k in range(n):
        a, v, c = R[k - 1], R[k], R[(k + 1) % n]
        l1 = math.hypot(v[0] - a[0], v[1] - a[1]) or 1e-9
        l2 = math.hypot(c[0] - v[0], c[1] - v[1]) or 1e-9
        n1 = ((v[1] - a[1]) / l1, -(v[0] - a[0]) / l1)
        n2 = ((c[1] - v[1]) / l2, -(c[0] - v[0]) / l2)
        nx, ny = n1[0] + n2[0], n1[1] + n2[1]
        dd = nx * n1[0] + ny * n1[1]
        f = d / dd if dd > 0.3 else d
        out.append((v[0] - nx * f, v[1] - ny * f))
    return out


def _wcomp(b):
    k = WALL_COMP.get(b.get("fab"))
    if b.get("fab") in HERITAGE_FABS or k not in COMP_ID:
        return {}
    return dict(structureType="Composite", compositeId=COMP_ID[k])


WALL_SIDE = [None]                                  # v1.87: "fwd" / "rev": which way a CoreOutside wall is drawn


def _core_out(b):
    """v1.87: a composite house wall: thickness of its skins outside the core (m), else None"""
    k = WALL_COMP.get(b.get("fab"))
    if b.get("fab") in HERITAGE_FABS or k not in COMP_ID or k not in COMP:
        return None
    t = 0.0
    for typ, _m, th in COMP[k][2]:
        if typ == "Core":
            return t
        t += th
    return None


def _scr_t():
    """v1.87: the floor slab's skins over its core (m): 0 for a basic slab"""
    if "floor_rc" not in COMP_ID:
        return 0.0
    t = 0.0
    for typ, _m, th in COMP["floor_rc"][2]:
        if typ == "Core":
            return t
        t += th
    return 0.0


PARTY_D_M, PARTY_OVER = 0.45, 0.80   # v1.88: sides closer than this, overlapping this share of the shorter: one wall


def _party_skip(bld):
    """v1.88: {(house, side)} whose wall is left out: a neighbour has a parallel side within PARTY_D_M along at least
    PARTY_OVER of its length, and the neighbour is taller (or as tall and listed first), so the shared side is built once"""
    E, ix = [], {}
    for bi, b in enumerate(bld):
        if b["fl"] < 0:
            continue
        R = b["ring"]
        for ei, (a, c) in enumerate(zip(R, R[1:] + R[:1])):
            L_ = math.hypot(c[0] - a[0], c[1] - a[1])
            if L_ < 0.3:
                continue
            k = len(E)
            E.append((bi, ei, a, c, L_, ((c[0] - a[0]) / L_, (c[1] - a[1]) / L_)))
            m = ((a[0] + c[0]) / 2.0, (a[1] + c[1]) / 2.0)
            ix.setdefault((int(m[0] // 10.0), int(m[1] // 10.0)), []).append(k)
    skip = set()
    for k, (bi, ei, a, c, L_, u) in enumerate(E):
        m = ((a[0] + c[0]) / 2.0, (a[1] + c[1]) / 2.0)
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for k2 in ix.get((int(m[0] // 10.0) + di, int(m[1] // 10.0) + dj), ()):
                    bj, ej, a2, c2, L2, u2 = E[k2]
                    if bj == bi or abs(u[0] * u2[1] - u[1] * u2[0]) > 0.17:
                        continue                          # same house, or not parallel (10 degrees)
                    if abs((m[0] - a2[0]) * u2[1] - (m[1] - a2[1]) * u2[0]) > PARTY_D_M:
                        continue
                    t0 = (a[0] - a2[0]) * u2[0] + (a[1] - a2[1]) * u2[1]
                    t1 = (c[0] - a2[0]) * u2[0] + (c[1] - a2[1]) * u2[1]
                    ov = min(max(t0, t1), L2) - max(min(t0, t1), 0.0)
                    if ov < PARTY_OVER * L_:                 # of its own length (a longer side keeps its wall)
                        continue
                    hi, hj = bld[bi]["h"], bld[bj]["h"]
                    if hj > hi + 0.01 or (abs(hj - hi) <= 0.01 and bj < bi):
                        skip.add((bi, ei))
    return skip


def _wall_side(ac, xy, a, c, on, b, log):
    """v1.87: one test wall a->c (counter-clockwise ring) with its reference line on the core's outside face: its 3D box
    says on which side Archicad puts the body; "fwd" when inside the house, else "rev" (drawn c->a); deleted again"""
    side = "rev"                                      # Archicad's rule when it can't be read: body right of a->c
    try:
        g = (ac.create("CreateWalls", "wallsData", [dict(begCoordinate=xy(a), endCoordinate=xy(c), zCoordinate=0.0,
                                                         height=1.0, thickness=_wt(b), referenceLineLocation="CoreOutside",
                                                         **_wcomp(b))], u"test wall side") or [None])[0]
        if g:
            bb = read_bb(ac, [g]).get(g)
            ac.t("DeleteElements", {"elements": [{"elementId": {"guid": g}}]})
            if bb:
                m_ = xy(((a[0] + c[0]) / 2.0, (a[1] + c[1]) / 2.0))
                d_ = ((bb[0] + bb[3]) / 2.0 - m_["x"]) * -on[0] + ((bb[1] + bb[4]) / 2.0 - m_["y"]) * -on[1]
                side = "fwd" if d_ > 0 else "rev"
                log.append(u"house walls: core-outside reference line, body %s of the line when drawn "
                           u"counter-clockwise (test wall, %.3f m inward): drawn %s" % (
                               "inside" if d_ > 0 else "outside", d_, "counter-clockwise" if side == "fwd" else "clockwise"))
                return side
        log.append(u"FLAG house walls: test wall not read, drawn clockwise (Archicad puts the body right of the line)")
    except Exception as e:
        log.append(u"FLAG house walls: test wall failed (%s), drawn clockwise" % e)
    return side


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
ADAPTIVE_GROUND = True                            # v1.45: grid by the accuracy (Aras 11:55 "-%2 +%2")
GROUND_GRIDS = (8.0, 4.0, 2.0, 1.0)               # v1.45: m, tried coarse to fine
GROUND_TOL_F = 0.0                                # v1.83: 0 (was +-2 % of the tile's height range, up to 0.6 m on steep tiles): one tolerance everywhere
GROUND_TOL_MIN = 0.30                             # v1.83 (Aras 19 Nov 09:01 "you can go even further than +-10cm", "+-30 or even 40 should be fine ig"): m, every ground height within +-0.30 m of the survey (one figure; 0.40 is a one-line change)
SEO_CORR_M = 3.0   # v1.66: m each side of a section line where solid links are kept (ASSUMED: covers the cut face)
SEC_R = []         # v1.66: section lines (A, B) in survey m
OP_PTS = {}        # v1.66: operator guid -> footprint points (survey m) for links that carry none
SECTION_BANDS = True   # v1.67 back on (v1.65 TEST had it off) (was True in v1.58-v1.64)                              # v1.58: one ground mesh per site section view (no tile grid behind the cut)
BAND_EDGE_M = 2.0                                 # v1.58: m between the edge heights of a view mesh
BAND_OK = {}                                      # v1.58: section name -> its view ground mesh guid
SECTION_STRIPS = True                             # v1.56: one ground strip per section line (no tile seams in the cut)
STRIP_W_M, STRIP_STEP_M = 1.0, 1.0                # v1.56: strip width; height points along it every 1 m
GROUND_THIN = True                                # v1.54: keep a finer grid height only where the 8 m grid misses it
GROUND_EDGE_M = 1.0                               # v1.32: tile edge points every this many m (the same on both tiles)
GROUND_GRID_M = 10.0                              # v1.31: a ground control point every this many m where no survey height
CUT_FILL_PEN = 1                                  # v1.41: pen of the cut fills (ASSUMED: pen 1 of his pen set)
GROUND_BASE_M = 3.0                               # v1.31: the ground block reaches this far under its lowest point
WHOLE_SITE = True                                 # v1.42: the whole survey extent, not only the cut rectangles
SITE_TILE_M = 50.0                                # v1.42: ground tile size in the whole-site build (fewer meshes)
SEO_TODO = []                                     # v1.51: solid element operations of this pass (made after the save)
LINKS_OK = set()                                  # v1.59: "target|operator|operation" of every link made
SEO_ERR = [u""]                                   # v1.59: Archicad's first reason a link was not made
SEO_CHUNK = 200 if BIG_RAM else 50   # v1.57;                                    # v1.51: links per Tapir call (was CHUNK 400 / 150 in one go)
SEO_PENDING = os.path.join(BERGAMA_ROOT, "cached", "bergama_archicad_site", "seo_pending.json")   # v1.51: left over


FOUND_OWN = [-1]                                  # v1.56: AcBuild elements found in the open file at the start
SCOPE = ["site"]                                  # v1.52: "site" or "buildings" (set from the open project's name)
SITE_BUILDINGS = True                             # v1.83 (Aras 19 Nov 09:05 "buildings and areas from our masterplan is not
                                                  # built"): our node buildings + canopies are built in the site file too
                                                  # (Bergama_buildings.pln was never made, so they were built nowhere)


def _set_scope(ac, log):
    """v1.52 (Aras 17 Nov 12:16 UTC "make this bergama_Site file as the site file only, our canopies and our own
    buildings should be linked to it"): a project whose name holds "building" builds ONLY our canopies and node
    buildings (Bergama_buildings.pln, hotlinked into the site file); any other name builds the site WITHOUT them.
    Each file keeps its own cache folder (its own record, sections, leftovers)"""
    global CACHE_DIR, SEO_PENDING
    nm_ = u""
    try:
        r_ = ac.t("GetProjectInfo")
        nm_ = (r_.get("projectName") or r_.get("projectPath") or u"") if isinstance(r_, dict) else u""
    except Exception as ex:
        log.append(u"FLAG project name not read (%s): built as the site file" % ex)
    SCOPE[0] = "buildings" if u"building" in nm_.lower() else "site"
    if SCOPE[0] == "buildings":
        CACHE_DIR = os.path.join(BERGAMA_ROOT, "cached", "bergama_archicad_buildings")
        SEO_PENDING = os.path.join(CACHE_DIR, "seo_pending.json")
    os.makedirs(CACHE_DIR, exist_ok=True)
    log.append(u"scope (v1.52): %s file (project \"%s\"): %s; cache %s" % (
        SCOPE[0], nm_ or u"untitled", u"only our canopies + node buildings (hotlink this file into the site file)"
        if SCOPE[0] == "buildings" else u"the site without our canopies + node buildings (they come as a hotlink "
        u"of Bergama_buildings.pln)", CACHE_DIR))
    _progress(u"scope: %s (project %s)" % (SCOPE[0], nm_ or u"untitled"))


def _save(ac, log, when):
    """v1.51: save the open project (it needs a file name: Aras saves the empty project once with Save As)"""
    try:
        ac.t("SaveProject", {}, 1800.0)
        log.append(u"Archicad project saved (%s)" % when)
        _progress(u"project saved (%s)" % when)
        return True
    except Exception as ex:
        if _ac_gone(ex):
            raise ArchicadGone(u"Archicad stopped answering while saving (%s): %s" % (when, ex))
        log.append(u"FLAG Archicad project not saved (%s: %s): give the project a file name once (File > Save As), "
                   u"then the build saves it itself" % (when, ex))
        _progress(u"FLAG project not saved (%s)" % when)
        return False


SITE_BATCH = 15                                  # v1.42: ground tiles per Tapir call (v1.48: was 40, 24 GB Desktop)
SITE_BOX = []                                     # v1.42: survey extent (x0, y0, x1, y1), survey m
NO_SAVE_PUBLISH = True                            # v1.42: Aras saves the pln himself; nothing published
OLD_CACHE = os.path.join(BERGAMA_ROOT, "cached", "bergama_archicad", "acbuild.json")   # v1.42: origin from here
HOUSE_ALL_IN = True                               # v1.83 (Aras 19 Nov 09:06 "some roads buildings and etc. goes out of the
                                                  # topography"): a house is built only when every corner is on the ground
N_OFFGROUND = [0]                                 # v1.83: houses left out for that
SITE_POLY = []                                    # v1.45: the site_alan square (survey m), everything is clipped to it
LIB_DIR = os.path.join(BERGAMA_ROOT, "archicad", "BergamaLib")    # v1.45: AcBuild's own GDL objects
LIBN = {}                                         # v1.45: object kind -> library part name (empty: no objects)
N_NOTREE = [0]                                    # v1.68: trees left out (no GDL object of their kind)
TILE_ERR = {}                                     # v1.69: ground tile (i, j) -> its max deviation from the survey (m)
TILE_G = [0.0, 0.0, 50.0]                         # v1.69: tile grid origin x, y and size
BUILT_PICK = {}                                   # v1.78: ground tile (i, j) -> the grid step it was built from (m)
BUILT_KEPT = set()                                # v1.78: (step, ix, iy) finer-grid heights sent to Archicad
BUILT_ZG = [None]                                 # v1.78: the grid-height function of the ground pass


def _zb(q, tin, ox, oy):
    """v1.78 (Aras 19 Nov 07:22 "dont draw roads like this", "just draw them from outlines not like whole ground and
    just elevated where the part of the road is"): the height of the ground AS ARCHICAD BUILT IT at q (the tile's grid,
    thinned heights replaced by the 8 m grid as in the ground pass), so a road lies on the ground that is drawn, not on
    the finer survey (the v1.69-v1.77 skins floated up to the tile's error, 0.6 m)"""
    zg = BUILT_ZG[0]
    k = (int((q[0] - TILE_G[0]) // TILE_G[2]), int((q[1] - TILE_G[1]) // TILE_G[2]))
    s_ = BUILT_PICK.get(k)
    if zg is None or s_ is None:
        return tin.z(q[0] - ox, q[1] - oy)
    g8 = GROUND_GRIDS[0]

    def node(ix, iy):
        z = zg(s_, ix, iy)
        if z is None or s_ >= g8 or not GROUND_THIN or (s_, ix, iy) in BUILT_KEPT:
            return z
        fx8, fy8 = ix * s_ / g8, iy * s_ / g8
        jx, jy = int(math.floor(fx8)), int(math.floor(fy8))
        zc = [zg(g8, jx, jy), zg(g8, jx + 1, jy), zg(g8, jx, jy + 1), zg(g8, jx + 1, jy + 1)]
        if any(v is None for v in zc):
            return z
        u, v = fx8 - jx, fy8 - jy
        return zc[0] * (1 - u) * (1 - v) + zc[1] * u * (1 - v) + zc[2] * (1 - u) * v + zc[3] * u * v
    fx, fy = (q[0] - TILE_G[0]) / s_, (q[1] - TILE_G[1]) / s_
    ix, iy = int(math.floor(fx)), int(math.floor(fy))
    zc = [node(ix, iy), node(ix + 1, iy), node(ix, iy + 1), node(ix + 1, iy + 1)]
    if any(v is None for v in zc):
        return tin.z(q[0] - ox, q[1] - oy)
    u, v = fx - ix, fy - iy
    return zc[0] * (1 - u) * (1 - v) + zc[1] * u * (1 - v) + zc[2] * (1 - u) * v + zc[3] * u * v
# v1.83 (Aras 19 Nov 09:12 "respect the site_alan everywhere like dont draw anything outside it ... if something is half
# out half in dont draw it. It needs to be in the area +%90 so you can draw it with the cutted plane"): every element sent
# to Archicad is measured against site_alan: its share inside (area for slabs / meshes, length for walls / beams, the
# point for objects / columns); under SITE_SHARE_MIN it is not made, at or over it, slabs and meshes are cut at the
# site_alan edge and walls / beams trimmed to it. Section helpers (registration blocks, slots, strips, view grounds)
# and elements with no plan points (windows, doors) are not touched.
SITE_SHARE_MIN = 0.90
SITE_TOL_M = 0.05                                 # m, a point this close outside the site_alan edge counts as inside
ORIGIN = [0.0, 0.0]
SITE_EXEMPT = ("registration", "section", "ground view", "ground strips", "ground tile", "test")
SITE_DROP = {}                                    # what -> elements left out by the rule


def _clip_z(P, C):
    """P [(x, y, z|None)] clipped to the convex CCW polygon C [(x, y)], z interpolated along the cut edges"""
    out = list(P)
    n = len(C)
    sgn = 1.0 if area(C) > 0 else -1.0
    for i in range(n):
        a, b = C[i], C[(i + 1) % n]
        f = lambda p: sgn * ((b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]))
        inp, out = out, []
        for j in range(len(inp)):
            p, q = inp[j], inp[(j + 1) % len(inp)]
            fp, fq = f(p), f(q)
            if fp >= 0:
                out.append(p)
            if (fp >= 0) != (fq >= 0):
                t = fp / (fp - fq)
                z = None if p[2] is None or q[2] is None else p[2] + (q[2] - p[2]) * t
                out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t, z))
        if not out:
            return []
    return out


def _seg_clip(a, b, C):
    """the part of segment a-b inside the convex polygon C, or None"""
    t0, t1 = 0.0, 1.0
    sgn = 1.0 if area(C) > 0 else -1.0
    for i in range(len(C)):
        p, q = C[i], C[(i + 1) % len(C)]
        f = lambda r: sgn * ((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]))
        fa, fb = f(a), f(b)
        if fa < 0 and fb < 0:
            return None
        if fa < 0:
            t0 = max(t0, fa / (fa - fb))
        elif fb < 0:
            t1 = min(t1, fa / (fa - fb))
    if t1 <= t0:
        return None
    return ((a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1))


def _in_site(name, items, what, log):
    """v1.83: (indices kept, items as sent) under the site_alan rule"""
    if not SITE_POLY or not items or any(w_ in (what or u"").lower() for w_ in SITE_EXEMPT):
        return list(range(len(items))), items
    C = [(q[0] - ORIGIN[0], q[1] - ORIGIN[1]) for q in SITE_POLY]
    cx_, cy_ = sum(q[0] for q in C) / len(C), sum(q[1] for q in C) / len(C)
    d_ = min(abs((b[0] - a[0]) * (cy_ - a[1]) - (b[1] - a[1]) * (cx_ - a[0])) / max(1e-9, math.hypot(b[0] - a[0], b[1] - a[1]))
             for a, b in zip(C, C[1:] + C[:1]))
    f_ = 1.0 + SITE_TOL_M / max(d_, 1.0)                 # site_alan grown by about SITE_TOL_M: points on its edge count in
    C = [(cx_ + (q[0] - cx_) * f_, cy_ + (q[1] - cy_) * f_) for q in C]
    ins = lambda p: _inpoly(p, C)
    keep, out = [], []
    for k, it in enumerate(items):
        if not isinstance(it, dict):
            keep.append(k)
            out.append(it)
            continue
        pc = it.get("polygonCoordinates")
        if isinstance(pc, list) and len(pc) >= 3 and all(isinstance(v, dict) and "x" in v for v in pc):
            P = [(v["x"], v["y"], v.get("z")) for v in pc]
            a0 = abs(area([p[:2] for p in P]))
            if all(ins(p[:2]) for p in P):
                keep.append(k)
                out.append(it)
                continue
            Q = _clip_z(P, C)
            a1 = abs(area([p[:2] for p in Q])) if len(Q) >= 3 else 0.0
            if a0 <= 0 or a1 / a0 < SITE_SHARE_MIN:
                SITE_DROP[what] = SITE_DROP.get(what, 0) + 1
                continue
            it2 = dict(it)
            it2["polygonCoordinates"] = [dict(x=round(p[0], 3), y=round(p[1], 3), **({"z": round(p[2], 3)} if p[2] is not None else {}))
                                         for p in Q]
            Qx = [p[:2] for p in Q]
            if it.get("holes"):
                it2["holes"] = [h for h in it["holes"] if all(_inpoly((v["x"], v["y"]), Qx)
                                                               for v in (h.get("polygonCoordinates") or []))]
            if it.get("sublines"):
                it2["sublines"] = [sl for sl in it["sublines"] if all(_inpoly((v["x"], v["y"]), Qx)
                                                                       for v in (sl.get("coordinates") or []))]
            keep.append(k)
            out.append(it2)
            continue
        bc, ec = it.get("begCoordinate"), it.get("endCoordinate")
        if isinstance(bc, dict) and isinstance(ec, dict) and "x" in bc and "x" in ec:
            a_, b_ = (bc["x"], bc["y"]), (ec["x"], ec["y"])
            if ins(a_) and ins(b_):
                keep.append(k)
                out.append(it)
                continue
            L0 = math.hypot(b_[0] - a_[0], b_[1] - a_[1])
            sg = _seg_clip(a_, b_, C)
            L1 = math.hypot(sg[1][0] - sg[0][0], sg[1][1] - sg[0][1]) if sg else 0.0
            if L0 <= 0 or L1 / L0 < SITE_SHARE_MIN:
                SITE_DROP[what] = SITE_DROP.get(what, 0) + 1
                continue
            it2 = dict(it)
            it2["begCoordinate"] = dict(bc, x=round(sg[0][0], 3), y=round(sg[0][1], 3))
            it2["endCoordinate"] = dict(ec, x=round(sg[1][0], 3), y=round(sg[1][1], 3))
            keep.append(k)
            out.append(it2)
            continue
        cd = it.get("coordinates")
        pts = [cd] if isinstance(cd, dict) else (cd if isinstance(cd, list) else [])
        pts = [(v["x"], v["y"]) for v in pts if isinstance(v, dict) and "x" in v and "y" in v]
        if pts and sum(1 for p in pts if ins(p)) < SITE_SHARE_MIN * len(pts):
            SITE_DROP[what] = SITE_DROP.get(what, 0) + 1
            continue
        keep.append(k)
        out.append(it)
    return keep, out


def _zup(q, tin, ox, oy):
    """v1.83 (Aras 19 Nov 09:04 "roads still dissappear under ground fix that"): the built-ground height at q raised by
    the most the ground mesh can bend away from it: Archicad splits each grid square of the ground along one of its two
    diagonals, and the two choices differ by half the square's twist |z00 + z11 - z10 - z01| / 2; a road point that
    high (plus TOWN_LIFT_M) stays over the ground whichever diagonal Archicad takes (v1.78-v1.82 used 3 cm, which a
    twisted square beats on every ridge)"""
    z = _zb(q, tin, ox, oy)
    if z is None or BUILT_ZG[0] is None:
        return z
    k = (int((q[0] - TILE_G[0]) // TILE_G[2]), int((q[1] - TILE_G[1]) // TILE_G[2]))
    s_ = BUILT_PICK.get(k)
    if s_ is None:
        return z
    tw = 0.0
    for st in set((s_, GROUND_GRIDS[0])):
        for dx in (-1e-3, 1e-3):
            for dy in (-1e-3, 1e-3):
                ix = math.floor((q[0] + dx - TILE_G[0]) / st)
                iy = math.floor((q[1] + dy - TILE_G[1]) / st)
                c_ = [_zb((TILE_G[0] + (ix + a) * st, TILE_G[1] + (iy + b) * st), tin, ox, oy)
                      for a, b in ((0, 0), (1, 0), (0, 1), (1, 1))]
                if all(v is not None for v in c_):
                    tw = max(tw, abs(c_[0] + c_[3] - c_[1] - c_[2]) / 2.0)
    return z + min(tw, TOWN_TWIST_MAX_M)


TOWN_TWIST_MAX_M = 1.0                            # v1.83: m, cap on that raise (a square twisted more is a wall, FLAG-free)
TREE_GAP_M = 1.0                                  # v1.76: m, two tree trunks never closer (ASSUMED)
SNAP_M = 0.30                                     # v1.76: m, kerb / wall ends this close become one point (ASSUMED)
BLD_IX = {}                                       # v1.76: 20 m cell -> house rings (survey m) for the clash checks
BLD_SNAP = [0]                                    # v1.76: house corners moved out of a neighbour
BLD_XSKIP = [0]                                   # v1.78: corner moves not made (the outline would cross itself)
RING_MIN_M = 0.30                                 # v1.78: shortest house wall; a shorter edge is merged away


def _selfx(R):
    """v1.78: True if the closed outline R crosses itself"""
    n = len(R)
    E = [(R[i], R[(i + 1) % n]) for i in range(n)]

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    for i in range(n):
        a, b = E[i]
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            c, d = E[j]
            if max(a[0], b[0]) < min(c[0], d[0]) or max(c[0], d[0]) < min(a[0], b[0]) or \
                    max(a[1], b[1]) < min(c[1], d[1]) or max(c[1], d[1]) < min(a[1], b[1]):
                continue
            d1, d2, d3, d4 = cr(c, d, a), cr(c, d, b), cr(a, b, c), cr(a, b, d)
            if ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0)) and d1 and d2 and d3 and d4:
                return True
    return False


def _tidy_ring(R):
    """v1.78: outline without edges under RING_MIN_M and without spikes (a corner that turns back on itself), each
    merged into its neighbours, counter-clockwise; the outline as it was if too little would be left"""
    Q = clean(list(R))
    ch = True
    while ch and len(Q) > 3:
        ch = False
        for i in range(len(Q)):
            a, b, c = Q[i - 1], Q[i], Q[(i + 1) % len(Q)]
            la, lb = math.hypot(b[0] - a[0], b[1] - a[1]), math.hypot(c[0] - b[0], c[1] - b[1])
            back = la > 1e-9 and lb > 1e-9 and ((b[0] - a[0]) * (c[0] - b[0]) + (b[1] - a[1]) * (c[1] - b[1])) / (la * lb) < -0.95
            if lb < RING_MIN_M or back:
                del Q[i]
                ch = True
                break
    if len(Q) < 3 or abs(area(Q)) < 1.0:
        return list(R)
    return Q if area(Q) > 0 else Q[::-1]


def _bld_set(rings):
    """v1.76: index the house footprints for the clash checks"""
    BLD_IX.clear()
    for R in rings:
        bx = (min(q[0] for q in R), min(q[1] for q in R), max(q[0] for q in R), max(q[1] for q in R))
        for i in range(int(bx[0] // 20), int(bx[2] // 20) + 1):
            for j in range(int(bx[1] // 20), int(bx[3] // 20) + 1):
                BLD_IX.setdefault((i, j), []).append((bx, R))


def _in_bld(p, pad=0.0):
    """v1.76: True when p is inside a house footprint or within pad of its walls"""
    for bx, R in BLD_IX.get((int(p[0] // 20), int(p[1] // 20)), []):
        if bx[0] - pad <= p[0] <= bx[2] + pad and bx[1] - pad <= p[1] <= bx[3] + pad:
            if _inpoly(p, R) or (pad > 0 and min(_seg_d(p, a, b) for a, b in zip(R, R[1:] + R[:1])) < pad):
                return True
    return False


class _Spread(object):
    """v1.76: placed objects (centre, radius) on a 5 m grid: a new one may not overlap an earlier one"""
    def __init__(self):
        self.g = {}

    def free(self, c, r):
        i, j = int(c[0] // 5), int(c[1] // 5)
        for a in range(i - 1, i + 2):
            for b in range(j - 1, j + 2):
                for q, rq in self.g.get((a, b), []):
                    if math.hypot(c[0] - q[0], c[1] - q[1]) < r + rq:
                        return False
        self.g.setdefault((i, j), []).append((c, r))
        return True


LIB_PAR = [u""]                                   # v1.75: the embedded library's parent part ("" = none)
TREE_OBJ = []                                     # v1.45: (kind, centre survey m, ground z, height, crown width)
CLEANUP_FILE = os.path.join(BERGAMA_ROOT, "cached", "bergama_archicad_site", "cleanup_unlabeled.txt")   # v1.45: one-time
PARTS_FILE = os.path.join(BERGAMA_ROOT, "cached", "bergama_archicad_site", "parts.txt")   # v1.45: rebuild switch
PARTS = set()                                     # v1.45: parts to rebuild (empty = all)
PART_G = {}                                       # v1.45: guid -> part (this pass)
OWN_PART = {}                                     # v1.45: guid -> part (from the Element ID)
BGRP = {}                                         # v1.45: house index -> [guids] (one group per house)
# v1.46 (Aras 17 Nov 09:57 UTC "build everything and give me something like the unsure areas kind of different layer or
# something and build accordingly that i can check those in archicad"): his masterplan layers whose meaning Claude could
# not confirm are built with the best guess below (MP_SLABS thickness) each on its own "BGA ? unsure" layer
MP_UNSURE = {"araba_yolu": u"car road 15 cm", "doldrurma": u"fill 5 cm",   # v1.47: in his 15 Nov masterplan.svg
             "yeni": u"new surface 10 cm",                                 # v1.47: "normal" dropped (not in that file) "master": u"flat 5 cm",
             "Layer_49": u"flat 5 cm", "bina_cerceve": u"building frame as a 15 cm plinth",
             "circulation": u"paving 15 cm", "kesin_yesil": u"green 5 cm", "belki_yesil": u"maybe-green 5 cm",
             "begum_yesil": u"green 5 cm"}   # teras_-_canopy is not unsure: the canopies are built from it (CAN_KEYS)
PART_RULES = tuple((u"masterplan unsure " + k_ + u":", u"unsure_" + k_) for k_ in MP_UNSURE) + (("ground tile", "terrain"), ("ground strips", "terrain"), ("ground view", "terrain"), ("section slots", "seo_ops"), ("bank zones", "terrain"), ("river", "river"), ("water", "river"),
              ("reed", "river"), ("boulders", "river"), ("town ground", "streets"), ("pavements", "streets"),
              ("kerbs", "streets"), ("survey stairs", "stairs"), ("house frame", "structure"), ("flat roofs", "structure"),
              ("walls", "houses"), ("windows", "houses"), ("ground-floor doors", "houses"),   # v1.54: the survey
              ("balcony", "houses"), ("roofs", "houses"),   # houses stay in the site file (v1.52 sent them to "buildings")
              ("tree", "greenery"), ("survey tree", "greenery"),
              ("olive", "greenery"), ("street furniture", "furniture"), ("people", "people"), ("cars", "people"),
              ("canopy", "buildings"), ("node", "buildings"),   # v1.52: our canopies + node buildings: own file
              ("masterplan", "proposal"), ("stepped", "proposal"),   # v1.54: were inside the comment above
              ("seating", "proposal"), ("bank walls", "proposal"), ("new bridge", "proposal"), ("retaining", "proposal"),
              (u"Ulucami", "bridges"), (u"\u00dc\u00e7 Kemer", "bridges"), ("registration", "reg"))
LAYER_NAME = {"terrain": u"BGA Terrain", "river": u"BGA River + water", "streets": u"BGA Streets",
              "stairs": u"BGA Stairs * existing (survey)", "buildings": u"BGA Buildings - envelope",
              "structure": u"BGA Buildings - structure", "greenery": u"BGA Greenery", "furniture": u"BGA Street furniture",
              "people": u"BGA People + cars", "proposal": u"BGA Proposal", "bridges": u"BGA Bridges (existing)",
              "reg": u"BG reg", "other": u"BGA Other"}
LAYER_NAME["buildings"] = u"BGA Proposal - canopies + our buildings"   # v1.52 (in Bergama_buildings.pln)
LAYER_NAME["seo_ops"] = u"BGA SEO operators (hidden)"   # v1.56: hidden slabs that only cut (section slots)
LAYER_NAME["houses"] = u"BGA Buildings - envelope"   # v1.54: the survey houses' walls, roofs, windows, doors, balconies
LAYER_NAME.update((u"unsure_" + k_, u"BGA ? unsure - %s (guess: %s)" % (k_, v_)) for k_, v_ in MP_UNSURE.items())   # v1.46
LAYER_ID = {}


def part_of(what):
    """v1.45: the part (layer, rebuild switch) of an element from the label it was made with"""
    w = (what or u"").lower()
    for k, p in PART_RULES:
        if w.startswith(k.lower()):
            return p
    return "other"


ID_PREFIX = "BGA-"                                # v1.44: Element ID of every element AcBuild makes
EDIT_TOL_M = 0.02                                 # v1.44: a 3D box moved more than this = hand-edited (locked)
EDIT_TOL_WALL_M = 0.60                            # v1.79: a wall's box also changes when Archicad trims it at a junction with a
                                                  # remade neighbour (v1.78 locked 548 such walls as "hand-edited")
SURVEY_CACHE = os.path.join(BERGAMA_ROOT, "cached", "bergama_survey", "survey.json")   # v1.44: survey without Rhino
PID = [None]                                      # v1.44: guid of the Element ID property
LOCKED_BB = []                                    # v1.44: (type, plan box) of the hand-edited elements
N_LOCKSKIP = [0]
N_RAFT = [0, 0.0]                                 # v1.44: rafts made, deepest raft below the floor (m)
N_TINONLY = [0]                                   # v1.44: ground tiles filled from the triangulation only
LINK_T = set()                                    # v1.44: targets of the solid element operations made this pass
TYPE_OF = {"CreateObjects": "Object", "CreateSlabs": "Slab", "CreateWalls": "Wall", "CreateMeshes": "Mesh", "CreateColumns": "Column",
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
                                      zCoordinate=round(zs_ - z0, 3),   # v1.88: slat top on the roof underside (hung 0.15 m below it)
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
            plinths.append(dict(level=round(g + CAN_PLINTH_M + CAN_DECK_M - z0, 3), polygonCoordinates=pc,   # v1.73: one
                                **(_ccomp("floor_canopy", CAN_PLINTH_M + 0.5 + CAN_DECK_M) if "floor_canopy" in COMP_ID
                                   else dict(thickness=CAN_PLINTH_M + 0.5 + CAN_DECK_M, _mat="terrace_stone"))))   # composite
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
        made += [g for g in _reg_ops(ac.create("CreateSlabs", "slabsData", plinths,
                                               u"canopy floors (timber deck on stone plinth, one composite slab)"), plinths) if g]
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
               u"plinth %.2f m, deck %.2f m (design intent)" % (n_c, len(roofs), len(trunks), len(plinths),
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
            gl_ = [(((k + 0.5) * L / nb), L / nb, 1, hs) for k in range(nb) if k % 2]   # v1.71: glass bays
            for j_ in range(nf):                          # v1.72: one wall per side per storey
                for s in (-D / 2, D / 2):                 # v1.71: one wall per long side (was one per bay)
                    walls.append((dict(begCoordinate=xy(P(-L / 2, s)), endCoordinate=xy(P(L / 2, s)),
                                       zCoordinate=round(zp + j_ * hs - z0, 3), height=round(hs, 3), thickness=NB_WALL_M,
                                       referenceLineLocation="Center"), gl_ or None))
                for t_ in (-L / 2, L / 2):
                    walls.append((dict(begCoordinate=xy(P(t_, -D / 2)), endCoordinate=xy(P(t_, D / 2)),
                                       zCoordinate=round(zp + j_ * hs - z0, 3), height=round(hs, 3), thickness=NB_WALL_M,
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
            wins += [dict(ownerWallId={"guid": g}, width=round(max(1.0, ln - 0.8), 2),   # v1.71: each glass bay
                          height=round(hs_ - NB_GLASS_SILL_M - NB_GLASS_HEAD_M, 2),
                          sillHeight=round(j * hs_ + NB_GLASS_SILL_M, 2), centerOffset=round(co_, 2))
                     for co_, ln, nf_, hs_ in gl for j in range(nf_)]
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
            "circulation": (0.15, 0.0), "rock": (0.30, 0.0),   # v1.29: his other painted layers; rock = boulders (build_selinos)
            "araba_yolu": (0.15, 0.0), "doldrurma": (0.05, 0.0)}   # v1.47: in his 15 Nov masterplan.svg, built as unsure
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
TREE_SP = {"trees_plane": (30.0, 0.30, 0.50), "trees_ash": (15.0, 0.35, 0.40),        # (height m, crown bottom as a share
           "trees_stone_pine": (15.0, 0.60, 0.40), "trees_rosemary": (1.0, 0.0, 0.0),  # of the height, trunk m)
           "trees_olive": (5.0, 0.30, 0.30),        # v1.47: his planting olives; 5 m inside 4-8 m (RHS) / 5-10 m (vdberk), R5
           "trees_willow": (10.0, 0.25, 0.40),      # v1.47: his planting willows: height ASSUMED (no research yet), FLAG
           "trees_tamarisk": (4.0, 0.30, 0.20)}     # v1.47: his planting tamarisks: height ASSUMED (no research yet), FLAG
TREE_UNSOURCED = ("trees_willow", "trees_tamarisk", "trees_rosemary")   # v1.47: heights with no source (FLAG in the log)
# v1.46 heights = the lower end of the vdberk mature-height range (research pack v3 R5, one source for all three):
# plane 30-35 m (was 18), ash 15-20 m (15 kept), stone pine 15-25 m (was 14); other sources: plane "to c. 40 m" (TSO),
# ash 20-30 m (EUFORGEN), stone pine 25-30 m (JRC). Crown bottom shares and trunks stay ASSUMED; rosemary ASSUMED
HIST_BRIDGES = (                                     # survey bridge (pair of deck edge lines) nearest to the point
    (u"Ulucami bridge (Roman)", (29846.0, 32277.0), 2,
     u"2 arches ASSUMED: the survey length fits the 'Selinus bridge, 2 x 11.4 m' row of Wikipedia's "
     u"List of Roman bridges, but that row is not confirmed to be this bridge"),
    (u"Üç Kemer bridge", (30294.0, 31792.0), 3, u"3 arches from its name ('three arches')"))
BR_PIER_M = 1.5             # m: pier thickness between arches: ASSUMED
BR_DECK_M = 0.8             # m: deck + fill over the arch crown: ASSUMED
BR_SEG = 36                 # slabs per arch (the arch soffit in steps); v1.69: 36 (was 12, visibly stepped)
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


def _bridge_obj(ac, miss, log, made, nm_b, at, u, L, W, k, s, rise, spring, R_, top, low, xy, z0):
    """v1.75: one historic bridge as ONE GDL object: its elevation (deck, piers, true arch curves) extruded across"""
    if not GDL_OBJECTS or not LIB_PAR[0] or not ac.has("CreateLibraryParts") or "CreateObjects" in miss:
        return False
    zb = low - 1.0                                      # the pier feet (as the old pier walls)
    pts = [(0.0, top - zb), (L, top - zb)]
    for a_ in reversed(range(k)):
        ta = a_ * (s + BR_PIER_M)
        for j in range(25):                               # the soffit, right to left
            x_ = s * (1.0 - j / 24.0)
            pts.append((ta + x_, spring + math.sqrt(max(0.0, R_ * R_ - (x_ - s / 2) ** 2)) - (R_ - rise) - zb))
        if a_ > 0:                                        # the pier down to its foot
            pts += [(ta, 0.0), (ta - BR_PIER_M, 0.0)]
    cl = []
    for p in pts:                                         # no doubled points
        if not cl or math.hypot(p[0] - cl[-1][0], p[1] - cl[-1][1]) > 0.005:
            cl.append(p)
    s3 = u'MATERIAL "%s"\nADDY %.3f\nROTX 90\nPRISM_ %d, %.3f,\n%s\nDEL 2\n' % (
        MAT["bridge_stone"][0], W, len(cl), W, u",\n".join(u"%.3f, %.3f, 15" % q for q in cl))
    nm = u"BGA Bridge %s" % nm_b.split(u" ")[0]
    try:
        r_ = ac.t("CreateLibraryParts", {"libraryParts": [dict(name=nm, parentName=LIB_PAR[0], path=u"BGA/%s.gsm" % nm,
                                                               script3D=s3, script2D=GDL2D_OBJ)],
                                          "overwriteExisting": True}, 900.0)
        e = (r_.get("libraryParts") or [None])[0]
        if not isinstance(e, dict) or e.get("error"):
            log.append(u"FLAG %s: bridge object not made (%s): built from slabs + pier walls" % (nm_b, json.dumps(e)[:200]))
            return False
        o_ = at(-L / 2, -W / 2)
        g = ac.create("CreateObjects", "objectsData", [dict(libraryPartName=nm, coordinates=dict(xy(o_), z=round(zb - z0, 3)),
                      dimensions=dict(x=round(L, 3), y=round(W, 3), z=round(top - zb, 3)),
                      angle=round(math.atan2(u[1], u[0]), 5))], u"%s (one GDL object)" % nm_b)
    except Exception as ex:
        if _ac_gone(ex):
            raise
        log.append(u"FLAG %s: bridge object not made (%s): built from slabs + pier walls" % (nm_b, ex))
        return False
    if not g or not g[0]:
        return False
    made.append(g[0])
    EXTRA_OPS.append((g[0], "Subtraction", [xy(at(-L / 2, -W / 2)), xy(at(L / 2, -W / 2)), xy(at(L / 2, W / 2)),
                                            xy(at(-L / 2, W / 2))]))
    return True


def build_selinos(ac, miss, log, xy, z0, tin, ox, oy, rects, inside, contours, pts, CJ, SP):
    """v1.29: river bed mesh, water, reeds, boulders, trees, bank walls, historic bridges with arches, piers under the
    long new bridges; every size not in his drawing or the survey is ASSUMED (constants above)"""
    made = []
    del RIVER_MESH[:], WATER_OPS[:]
    gz = lambda p: tin.z(p[0] - ox, p[1] - oy)
    rings = SEL.get("river") or []
    if SITE_POLY:                                         # v1.45: site_alan only
        rings = [R for R in (clean(_clip_convex([tuple(q) for q in R], SITE_POLY)) for R in rings) if len(R) >= 3]
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
            if SITE_POLY and not _inpoly(c, SITE_POLY):
                continue
            if LIBN.get(TREE_KIND.get(sp)):              # v1.45: a GDL tree of its species
                TREE_OBJ.append((TREE_KIND[sp], c, g, H_, D))
            else:                                        # v1.68: no slab trees
                N_NOTREE[0] += 1
            continue
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
        un_ = [k for k in TREE_UNSOURCED if n_t.get(k)]
        if un_:                                          # v1.47
            log.append(u"FLAG trees: heights with no source yet (ASSUMED, check): %s" % u", ".join(
                u"%s %d x %.0f m" % (k, n_t[k], TREE_SP[k][0]) for k in un_))
    # ---- bank walls along his istinaat lines: top = the higher ground either side (+1.0 m where level), footing 0.5 m
    bw = []
    for L_ in SEL.get("istinaat") or []:
        L_ = _straighten(L_, False)                       # v1.71
        for a, b in zip(L_, L_[1:]):
            Ls = math.hypot(b[0] - a[0], b[1] - a[1])
            if Ls < 0.3:
                continue
            nx, ny = -(b[1] - a[1]) / Ls, (b[0] - a[0]) / Ls
            k_n = max(1, int(math.ceil(Ls / RET_SEG_M)))
            ch_ = []
            for k_ in range(k_n):
                p0 = (a[0] + (b[0] - a[0]) * k_ / k_n, a[1] + (b[1] - a[1]) * k_ / k_n)
                p1 = (a[0] + (b[0] - a[0]) * (k_ + 1) / k_n, a[1] + (b[1] - a[1]) * (k_ + 1) / k_n)
                m_ = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
                s1, s2 = gz((m_[0] + nx * 1.5, m_[1] + ny * 1.5)), gz((m_[0] - nx * 1.5, m_[1] - ny * 1.5))
                zs = [z for z in (s1, s2, gz(m_)) if z is not None]
                if not zs:
                    ch_.append(None)
                    continue
                hi, lo = max(zs), min(zs)
                if hi - lo < 0.3:
                    hi = hi + BANK_WALL_UP
                lo -= RET_FOOT_M
                ch_.append((p0, p1, lo, hi))
            for p0, p1, lo, hi in _merge_runs(ch_):        # v1.71: one wall per run
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
        bed_z = [z for z in (gz(at(-L / 2 + L * i / 20.0, 0)) for i in range(21)) if z is not None]   # v1.54: was "bed",
        if not ends or not bed_z:                         # which replaced bed() used by gz for the next bridge
            log.append(u"FLAG %s: outside the surveyed ground: not built" % nm_b)
            continue
        top, low = max(ends), min(bed_z)
        s = (L - (k - 1) * BR_PIER_M) / k
        rise = max(0.5, min(s / 2.0, top - BR_DECK_M - low))
        spring = top - BR_DECK_M - rise
        R_ = (s * s / 4.0 + rise * rise) / (2 * rise)
        parts, pw_ = [], []
        if _bridge_obj(ac, miss, log, made, nm_b, at, u, L, W, k, s, rise, spring, R_, top, low, xy, z0):   # v1.75
            log.append(u"%s: ONE GDL object (arches, piers, deck): survey deck %.1f x %.1f m, %d arches of %.1f m span, "
                       u"rise %.1f m, deck top %.2f m, piers %.1f m ASSUMED; %s" % (nm_b, L, W, k, s, rise, top, BR_PIER_M, why))
            continue
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
TOWN_SKIRT = "SolidBodyWithSkirt"   # v1.83 (Aras 19 Nov 09:08-09:09 "dont draw parts like this", "every thing that you
                            # draw should be realistic", "with real thickness"): roads, parks and pavements are Mesh
                            # BODIES from their top down to TOWN_UNDER_M under their lowest point (were 0-thickness skins)
TOWN_RELIEF_MAX_M = 1.5     # v1.83: m, a piece whose top rises more than this is quartered (body depth <= ~1.8 m, ASSUMED)
TOWN_MIN_M2 = 10.0          # v1.83: m2, a road / park piece smaller than this after cutting is left out
TOWN_SLIVER_M = 1.0         # v1.83: m, a road / park piece thinner than this on average (2 x area / perimeter) is left out
N_SLIVER = [0]
TOWN_CELL_SPLIT = True      # v1.83: a road / park cell Archicad refuses is made again as its four quarters
TOWN_CELL_MIN_M = 25.0      # v1.83: m, the smallest quarter tried
TOWN_CELL_M = 200.0         # v1.83: 200 (was 50; Aras 19 Nov 09:02 larger road surfaces); v1.75: 50 (was 20), the ground tile size; m: the street region / parks are built in cells this size (each with its holes)
TOWN_UNDER_M = 0.30         # m: a road / park cell reaches this far under the lowest ground in it; the terrain then
#                             shapes its top (SEO intersection), so it lies on the survey ground
TOWN_HOLE_IN = 0.01         # m: a hole cut by a cell edge is kept this far inside it (Archicad needs holes inside)
KERB_H, KERB_T = 0.15, 0.15  # m: kerb height (v1.46: inside the 3-15 cm sidewalk height, Yaya Yollari Yon. 2023 Md. 5(6), R3), thickness ASSUMED
WALL_H, WALL_T = 1.50, 0.25  # m: survey walls height (v1.46: under the 2.50 m cap, Bergama KAIP 6.5.9, R10), thickness ASSUMED
HWALL_H, HWALL_T = 4.00, 1.00  # m: survey heritage (ancient) walls; v1.46: height 4.0 = the lower end of "about 4-5 m"
                               # for the lower-town walls found in the stream works (AA 2022, press, R10; was 3.0); thickness ASSUMED
TOWN_OUTLINES = True        # v1.78: roads + parks as one Mesh per outline (50 m cells only where Archicad refuses one)
TOWN_EDGE_M = 2.0           # v1.78: m, points along a road / park outline (its edge follows the ground between them)
TOWN_PT_M = 2.5             # v1.44: m, surveyed-ground points inside each road / park mesh
PAV_MAX_M = 5.0             # v1.44: m, widest pavement strip from a kerb to a building face: ASSUMED
PAV_NEAR_M = 8.0            # v1.44: m, a kerb with no building face this close on either side gets no pavement
PAV_SKIN = True             # v1.56: pavements are skins (their flat-bottomed bodies were the "gravel boxes" in the sections)
PAV_T_M = 0.27              # v1.46: m, pavement build-up: 6 cm paver + 6 cm sand + 15 cm base (upper end of Percin's
                            # lecture-note labels 6 + 5-6 + 15 cm, SECONDARY, research pack v3 R3; was 0.30 ASSUMED)
EXTRA_LINKS = []            # v1.44: solid element operations made in the builders (road minus pavement)
LINE_RISE_M, LINE_MIN_M = 1e9, 1.0   # v1.78: off, one wall per straight run (v1.70: 0.30, was 0.10)
KERB_WALLS = False          # v1.88 (Aras 20 Nov 09:51 "you are drawing road outlines as walls"): no kerb walls on the
                            # survey road edges (the road / pavement bodies carry the kerb); True = v1.87
LINE_STEP_M = {"walls": 0.30, "heritage_walls": 0.50}   # v1.88: a survey wall steps with the slope every this much rise
                            # (v1.78-v1.87: one flat-topped wall per straight run stood metres high on a slope)
_OLD_LINE_RISE = 0.10   # v1.56: a kerb / wall piece rises at most 0.10 m along its length, but is
                                     # never shorter than 1.0 m (drawing choice: posts of at most ~0.1 m + kerb)
KERB_OPS = []               # v1.61: (guid, points) survey kerbs / walls: they cut only the section view grounds
LINE_SEG_M = 1e9            # m: walls and kerbs in pieces at most this long; v1.70: no length chopping (was 6.0)
STRAIGHT_TOL_M = 0.10       # v1.70: a survey point this close to the line between its neighbours is dropped (ASSUMED)
TOWN_LIFT_M = 0.03          # v1.56: road / park skins this far over the surveyed ground (no z-fighting with the tiles)
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
            if SITE_POLY and not _inpoly(c, SITE_POLY):      # v1.45: site_alan only
                continue
            g = tin.z(c[0] - ox, c[1] - oy)
            if g is None or any(_inpoly(c, R) for R in cell.get((int(c[0] // 20), int(c[1] // 20)), [])) or \
                    any(math.hypot(c[0] - p[0], c[1] - p[1]) < 2.0 for p in plant):
                n_skip += 1
                continue
            n_[lay] = n_.get(lay, 0) + 1
            if LIBN.get(SURVEY_KIND.get(lay)):            # v1.45: a GDL tree
                TREE_OBJ.append((SURVEY_KIND[lay], c, g, H_, D))
            else:                                        # v1.68: no slab trees
                N_NOTREE[0] += 1
            continue
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
        if L_ < 0.3 or (SITE_POLY and not _inpoly((x0, y0), SITE_POLY)):
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
        g_ = ac.create("CreateSlabs", "slabsData", tr, u"survey stairs * existing (survey): treads (Slab tool)")
        made += [g for g in g_ if g]
        EXTRA_OPS.extend((g, "Subtraction", d["polygonCoordinates"]) for g, d in zip(g_, tr) if g)
    log.append(u"survey stairs (BINA_MERDIVEN): %d flights, %d treads at their surveyed heights, down to the ground and "
               u"cutting it; %d lone step edges not built (no second edge to give the tread depth)" % (n_fl, len(tr), n_lone))
    return made


# ================================================================ v1.45: layers, GDL objects, bank zones, people + cars
TREE_KIND = {"trees_plane": "plane", "trees_ash": "ash", "trees_stone_pine": "stone_pine", "trees_rosemary": "rosemary",
             "trees_willow": "willow", "trees_olive": "olive", "trees_tamarisk": "tamarisk"}   # v1.57: own willow + tamarisk   # v1.47: his 3 other species
SURVEY_KIND = {"SEMBOL_TEK_AGAC": "deciduous", "SEMBOL_YPDKN_AGAC": "evergreen", "SEMBOL_YAP_DOKMEYEN": "evergreen"}
OLIVE_H, OLIVE_D = 5.0, 5.0                         # m: survey olive height (v1.46: inside 4-8 m RHS and 5-10 m vdberk, R5); crown ASSUMED (sources conflict 1.5-2.5 vs 8-12 m)
# survey symbol layer -> (object kind, width, depth, height m: ASSUMED, label)
FURN = {"SEMBOL_CAD_SOKAK_LAM": ("lamp", 1.2, 0.4, 6.0, u"street lamps"),
        "SEMBOL_CESME": ("fountain", 1.4, 0.7, 2.2, u"fountains"),
        "HIDRO_CESME": ("fountain", 1.4, 0.7, 2.2, u"fountains (hydro)"),
        "SEMBOL_DURAK": ("bus_stop", 3.0, 1.5, 2.6, u"bus stops"),
        "SEMBOL_HEYKEL": ("statue", 1.2, 1.2, 3.0, u"statues"),
        "SEMBOL_ABIDE": ("statue", 2.0, 2.0, 5.0, u"monuments"),
        "SEMBOL_BAYRAK_DIREGI": ("flag", 1.6, 0.2, 10.0, u"flag poles"),
        "SEMBOL_MINARE": ("minaret", 3.2, 3.2, 30.0, u"minarets")}
PERSON_H = 1.70                                     # m: ASSUMED (R5: men about 1.73 m, press citing TUIK; women NOT FOUND)
CAR_H = 1.45                                        # m: ASSUMED
BANK_PAIR_M = 20.0                                  # m: a top-of-slope point pairs with the nearest toe within this


def _tree3d(trunk, clumps, crown_cone=None, bark="Bark - Deciduous", leaf="Foliage - Leaves Tree Small", res=8):
    """GDL 3D script of a simplified tree in a unit box (A x B x ZZYZX): trunk segments (x, y, z, rotz, roty, h, r1,
    r2), leaf clumps (x, y, z, r, mulz)"""
    L = ["MUL A, B, ZZYZX", "RESOL %d" % res, 'MATERIAL "%s"' % bark]
    for x, y, z, rz, ry, h, r1, r2 in trunk:
        L += ["ADD %.3f, %.3f, %.3f" % (x, y, z), "ROTZ %.1f" % rz, "ROTY %.1f" % ry,
              "CONE %.3f, %.4f, %.4f, 90, 90" % (h, r1, r2), "DEL 3"]
    L.append('MATERIAL "%s"' % leaf)
    if crown_cone:
        z, h, r = crown_cone
        L += ["ADDZ %.3f" % z, "CONE %.3f, %.3f, 0.01, 90, 90" % (h, r), "DEL 1"]
    for x, y, z, r, mz in clumps:
        L += ["ADD %.3f, %.3f, %.3f" % (x, y, z), "MULZ %.3f" % mz, "SPHERE %.3f" % r, "DEL 2"]
    L.append("DEL 1")
    return u"\n".join(L) + u"\n"


def _ring(n, rad, z, r, mz, phase=0.0):
    return [(rad * math.cos(math.radians(phase + 360.0 * k / n)), rad * math.sin(math.radians(phase + 360.0 * k / n)),
             z, r, mz) for k in range(n)]


GDL3D = {
    "olive": _tree3d([(0, 0, 0, 0, 10, 0.25, 0.06, 0.045), (0.03, 0, 0.24, 0, -25, 0.22, 0.04, 0.025),
                      (0.02, 0, 0.24, 120, 30, 0.22, 0.035, 0.02), (0.02, 0, 0.24, 240, 28, 0.2, 0.03, 0.02)],
                     [(0.12, 0.05, 0.55, 0.22, 0.6), (-0.15, 0.1, 0.6, 0.2, 0.6), (0.05, -0.18, 0.58, 0.21, 0.6),
                      (-0.05, 0.15, 0.75, 0.2, 0.55), (0.1, -0.05, 0.78, 0.19, 0.55), (-0.12, -0.12, 0.72, 0.18, 0.55),
                      (0, 0, 0.86, 0.16, 0.5)], leaf="Foliage - Wild grapes"),
    "plane": _tree3d([(0, 0, 0, 0, 0, 0.45, 0.05, 0.035), (0, 0, 0.4, 0, 20, 0.25, 0.03, 0.02),
                      (0, 0, 0.4, 180, 20, 0.25, 0.03, 0.02)],
                     _ring(7, 0.24, 0.62, 0.21, 0.8) + [(0, 0, 0.82, 0.25, 0.7)]),
    "ash": _tree3d([(0, 0, 0, 0, 0, 0.42, 0.04, 0.03)],
                   [(0, 0, 0.55, 0.3, 0.9), (0.15, 0.1, 0.7, 0.25, 0.8), (-0.15, -0.1, 0.72, 0.25, 0.8),
                    (0, 0.15, 0.85, 0.22, 0.8), (0.05, -0.15, 0.85, 0.2, 0.8)]),
    "deciduous": _tree3d([(0, 0, 0, 0, 4, 0.4, 0.045, 0.03), (0, 0, 0.38, 60, 22, 0.2, 0.025, 0.015)],
                         _ring(5, 0.18, 0.62, 0.24, 0.85, 20) + [(0, 0, 0.8, 0.26, 0.8)]),
    "stone_pine": _tree3d([(0, 0, 0, 0, 8, 0.66, 0.04, 0.028)],
                          [(0, 0, 0.82, 0.36, 0.3)] + _ring(4, 0.2, 0.8, 0.22, 0.3, 45), bark="Bark - Deciduous"),
    "evergreen": _tree3d([(0, 0, 0, 0, 0, 0.15, 0.045, 0.035)], [(0, 0, 0.3, 0.33, 1.0)], crown_cone=(0.1, 0.9, 0.42)),
    # v1.57: weeping willow: short leaning trunk, broad dome with long hanging clumps down to near the ground
    "willow": _tree3d([(0, 0, 0, 0, 6, 0.35, 0.06, 0.045), (0, 0, 0.32, 40, 25, 0.2, 0.035, 0.02),
                       (0, 0, 0.32, 220, 25, 0.2, 0.035, 0.02)],
                      [(0, 0, 0.75, 0.3, 0.6)] + _ring(6, 0.3, 0.5, 0.16, 2.2, 15) + _ring(6, 0.18, 0.62, 0.17, 1.6, 45)),
    # v1.57: tamarisk: several thin stems from the ground, loose feathery crown of small clumps
    "tamarisk": _tree3d([(0, 0, 0, 0, 12, 0.5, 0.03, 0.02), (0, 0, 0, 120, 18, 0.45, 0.025, 0.015),
                         (0, 0, 0, 240, 15, 0.48, 0.025, 0.015)],
                        _ring(5, 0.22, 0.55, 0.16, 0.9, 10) + _ring(4, 0.12, 0.78, 0.15, 0.8, 50) + [(0, 0, 0.88, 0.13, 0.8)],
                        leaf="Foliage - Wild grapes"),
    "rosemary": _tree3d([], [(0, 0, 0.3, 0.45, 0.7), (0.2, 0.1, 0.35, 0.3, 0.8), (-0.2, -0.1, 0.35, 0.3, 0.8)],
                        leaf="Foliage - Wild grapes"),
    "lamp": u"""RESOL 12
MATERIAL "Paint - Anthracite"
CYLIND ZZYZX, 0.07
ADD 0, 0, ZZYZX - 0.08
ROTY 90
CYLIND 0.9, 0.04
DEL 2
ADD 0.65, -0.13, ZZYZX - 0.22
BLOCK 0.5, 0.26, 0.14
DEL 1
""",
    "fountain": u"""MATERIAL "Stone - Marble Carrara White"
ADD -A/2, -B/2, 0
BLOCK A, B, ZZYZX
DEL 1
ADD -A/2 - 0.1, -B/2 - 0.5, 0
BLOCK A + 0.2, 0.5, 0.45
DEL 1
MATERIAL "Water - Pond"
ADD -A/2, -B/2 - 0.45, 0.35
BLOCK A, 0.4, 0.06
DEL 1
""",
    "bus_stop": u"""RESOL 10
MATERIAL "Metal - Steel"
FOR i = 0 TO 1
FOR j = 0 TO 1
ADD -A/2 + 0.1 + i * (A - 0.2), -B/2 + 0.1 + j * (B - 0.2), 0
CYLIND ZZYZX, 0.05
DEL 1
NEXT j
NEXT i
ADD -A/2 - 0.1, -B/2 - 0.1, ZZYZX
BLOCK A + 0.2, B + 0.2, 0.08
DEL 1
MATERIAL "Glass - Clear Fast"
ADD -A/2 + 0.1, B/2 - 0.12, 0.15
BLOCK A - 0.2, 0.02, ZZYZX - 0.3
DEL 1
MATERIAL "Wood - Oak Light"
ADD -A/2 + 0.3, B/2 - 0.55, 0.45
BLOCK A - 0.6, 0.4, 0.05
DEL 1
""",
    "statue": u"""RESOL 12
MATERIAL "Stone - Granite Gray"
ADD -A/2, -B/2, 0
BLOCK A, B, ZZYZX * 0.4
DEL 1
MATERIAL "Metal - Bronze"
ADDZ ZZYZX * 0.4
CONE ZZYZX * 0.45, A * 0.18, A * 0.12, 90, 90
ADDZ ZZYZX * 0.5
SPHERE A * 0.1
DEL 2
""",
    "flag": u"""RESOL 10
MATERIAL "Metal - Aluminium"
CYLIND ZZYZX, 0.06
MATERIAL "Paint - Vermilion"
ADD 0.06, -0.005, ZZYZX - 1.2
BLOCK 1.5, 0.01, 1.0
DEL 1
""",
    "minaret": u"""RESOL 16
MATERIAL "Stone - Limestone Fine"
CYLIND ZZYZX * 0.12, A/2
ADDZ ZZYZX * 0.12
CONE ZZYZX * 0.6, A * 0.38, A * 0.33, 90, 90
ADDZ ZZYZX * 0.6
CYLIND 0.4, A/2
ADDZ 0.4
CONE ZZYZX * 0.14, A * 0.28, A * 0.26, 90, 90
ADDZ ZZYZX * 0.14
MATERIAL "Metal - Zinc"
CONE ZZYZX * 0.14 - 0.4, A * 0.3, 0.02, 90, 90
DEL 4
""",
    "person": u"""RESOL 8
MATERIAL "Paint - Light Gray"
ADD -0.08, 0, 0
CYLIND ZZYZX * 0.47, 0.06
DEL 1
ADD 0.08, 0, 0
CYLIND ZZYZX * 0.47, 0.06
DEL 1
ADDZ ZZYZX * 0.47
CONE ZZYZX * 0.35, 0.16, 0.19, 90, 90
ADDZ ZZYZX * 0.43
SPHERE 0.1
DEL 2
""",
    "car": u"""RESOL 10
MATERIAL "Paint - Light Gray"
ADD -A/2, -B/2, 0.25
BLOCK A, B, ZZYZX * 0.42
DEL 1
MATERIAL "Glass - Blue"
ADD -A * 0.22, -B/2 + 0.08, 0.25 + ZZYZX * 0.42
BLOCK A * 0.48, B - 0.16, ZZYZX * 0.38
DEL 1
MATERIAL "Paint - Anthracite"
FOR i = 0 TO 1
FOR j = 0 TO 1
ADD -A/2 + 0.75 + i * (A - 1.5), -B/2 + 0.1 + j * (B - 0.2), 0.3
ROTX 90
CYLIND 0.18, 0.3
DEL 2
NEXT j
NEXT i
""",
}
GDL2D_TREE = u"HOTSPOT2 0, 0\nCIRCLE2 0, 0, A / 2\nCIRCLE2 0, 0, A / 20\n"
GDL2D_OBJ = u"HOTSPOT2 0, 0\nPROJECT2 3, 270, 2\n"


def setup_layers(ac, log):
    """v1.45: one BGA layer per part + layer combinations"""
    LAYER_ID.clear()
    try:
        ac.t("CreateLayers", {"layerDataArray": [dict({"name": n_}, **({"isHidden": True} if p_ == "seo_ops" or p_.startswith("view_") else {}))
                                                 for p_, n_ in LAYER_NAME.items()], "overwriteExisting": False})
    except Exception as ex:
        log.append(u"layers: %s (kept the existing ones)" % ex)
    try:
        at = dict((a.get("name"), a) for a in (ac.t("GetAttributesByType", {"attributeType": "Layer"}).get("attributes") or []))
        for p, n_ in LAYER_NAME.items():
            if n_ in at:
                LAYER_ID[p] = int(at[n_]["index"])
        uns_ = set(p for p in LAYER_NAME if p.startswith(u"unsure_"))   # v1.46: the unsure masterplan layers
        combos = {u"BGA - all": set(),
                  u"BGA - existing only": {"proposal"} | uns_,
                  u"BGA ? unsure only (check)": set(p for p in LAYER_NAME if p not in uns_ and p != "terrain"),
                  u"BGA - proposal on terrain": {"buildings", "houses", "structure", "greenery", "furniture", "people", "stairs"},
                  u"BGA - terrain + water": {"streets", "stairs", "buildings", "houses", "structure", "greenery", "furniture",
                                              "people", "proposal", "bridges", "reg", "other"}}
        for p in LAYER_NAME:                               # v1.58: each section view: its own ground, no tiles
            if p.startswith("view_"):
                combos[u"BGA - section " + p[5:]] = set(q for q in LAYER_NAME if q == "terrain" or (
                    q.startswith("view_") and q != p))
        ac.t("CreateLayerCombinations", {"overwriteExisting": True, "layerCombinationDataArray": [
            dict(name=cn, layers=[dict(attributeId=at[LAYER_NAME[p]]["attributeId"], isHidden=p in hid or p == "seo_ops" or (
                                           p.startswith("view_") and not cn.startswith(u"BGA - section ")),
                                       isLocked=False)
                                  for p in LAYER_NAME if LAYER_NAME[p] in at]) for cn, hid in combos.items()]})
        log.append(u"layers (v1.45): %d BGA layers, combinations %s" % (len(LAYER_ID), u", ".join(combos)))
    except Exception as ex:
        log.append(u"FLAG layers / combinations not made (%s)" % ex)


GDL_OBJECTS = True                                # v1.68 on again (v1.63-v1.67 off)
GDL_ERR = [u""]                                   # v1.55: first reason a GDL object was not made


TREE_LIB_KEYS = {"olive": ("olive", "olea"), "plane": ("plane", "platan"), "ash": ("ash", "fraxinus"),
                 "stone_pine": ("stone pine", "pinus pinea", "pine"), "deciduous": ("deciduous", "broadleaf", "oak"),
                 "evergreen": ("evergreen", "cypress", "conifer"), "rosemary": ("rosemary", "shrub", "bush"),
                 "willow": ("willow", "salix"), "tamarisk": ("tamarisk", "tamarix", "shrub")}   # v1.78: name words
TREE_LIB_GROUP = {"olive": ("deciduous", "broadleaf", "tree"), "plane": ("deciduous", "broadleaf", "tree"),
                  "ash": ("deciduous", "broadleaf", "tree"), "deciduous": ("tree",), "willow": ("deciduous", "tree"),
                  "stone_pine": ("conifer", "tree"), "evergreen": ("conifer", "tree"),
                  "rosemary": ("bush", "plant"), "tamarisk": ("bush", "deciduous", "tree")}   # v1.79: generic fallback


# v1.83 (Aras 19 Nov 09:04 "those tree's are awful use rather high poly real 3d trees"): the real 3D tree models of the
# Archicad 30 library first (read from his library 19 Nov); v1.79 took the old symbolic "Deciduous Trees" / "Pine Trees"
# / "Shrubs" parts
TREE_LIB_EXACT = {"olive": ("Tree Model Detailed",), "plane": ("Tree Model Detailed",), "ash": ("Tree Model Detailed",),
                  "deciduous": ("Tree Model Detailed",), "willow": ("Tree Model Detailed",),
                  "tamarisk": ("Tree Model Detailed",), "stone_pine": ("Pine Tree Model", "Tree Model Detailed"),
                  "evergreen": ("Pine Tree Model", "Tree Model Detailed"),
                  "rosemary": ("Shrubs", "Tree Model Simple 1", "Tree Model Detailed")}   # v1.88: Fronded Tree variable
# was refused for all 19 rosemary on 20 Nov (Desktop log line 178)


def _lib_trees(names, log):
    """v1.78 (Aras 19 Nov "trees are really bad"): per species the loaded library part whose name holds a tree word of
    that species, preferring 'detailed' / 'realistic' / '3D' ones; the AcBuild GDL tree only where none matches"""
    # v1.79: a plant word is always needed and the species word must start a word (v1.78 let "ash" match "washbasin");
    # a species with no part of its own takes the most detailed generic tree of its group (broadleaf / conifer / shrub)
    nl = [(n_, (n_ or u"").lower()) for n_ in names if n_ and not (n_ or u"").startswith((u"BGA ", u"Bergama "))]
    nl = [(n_, l_) for n_, l_ in nl if re.search(u"(^|[^a-z])(tree|shrub|bush|plant|palm|conifer|deciduous)", l_)]
    rank = lambda x: (("detail" in x[1]) * 3 + ("realistic" in x[1]) * 2 + ("3d" in x[1]), -len(x[1]))
    pick, n_lib = {}, 0
    have_ = set(n_ for n_ in names if n_)
    for kind, keys in TREE_LIB_KEYS.items():
        best = next((n_ for n_ in TREE_LIB_EXACT.get(kind, ()) if n_ in have_), None)   # v1.83: real 3D models
        if best:
            LIBN[kind] = pick[kind] = best
            n_lib += 1
            continue
        for k_ in keys + TREE_LIB_GROUP.get(kind, ()):   # its own words first, then its group's
            c_ = [(n_, l_) for n_, l_ in nl if re.search(u"(^|[^a-z])" + re.escape(k_), l_)]
            if c_:
                best = max(c_, key=rank)[0]
                break
        if best:
            LIBN[kind] = best
            pick[kind] = best
            n_lib += 1
    log.append(u"trees (v1.83): Archicad library parts used: %s; AcBuild GDL trees kept for: %s (no library match)" % (
        u", ".join(u"%s -> %s" % kv for kv in sorted(pick.items())) or u"none",
        u", ".join(k for k in sorted(TREE_LIB_KEYS) if k not in pick) or u"none"))


LAMP_LIB = ("Street Lamp 01", "Street Lamp 02", "Street Lamp 03")   # v1.88 (Aras 20 Nov 09:50 "these lamps are wrong")
LAMP_OWN = [None]          # v1.88: AcBuild's own lamp part, the fallback
LAMP_MERGE_M = 3.2         # v1.88: survey lamp points closer than this are one lamp (the survey symbol gives 2-3 points
                           # per lamp: 79 of 101 lamps stood 1.2-2.6 m from another, 20 Nov)


def _merge_pts(P, d):
    """v1.88: points closer than d (chained) as one point at their middle, with the first one's angle"""
    out, used = [], [False] * len(P)
    for i, p in enumerate(P):
        if used[i]:
            continue
        grp, k = [i], 0
        used[i] = True
        while k < len(grp):
            q = P[grp[k]]
            for j in range(len(P)):
                if not used[j] and math.hypot(P[j][0] - q[0], P[j][1] - q[1]) < d:
                    used[j] = True
                    grp.append(j)
            k += 1
        out.append((sum(P[g][0] for g in grp) / len(grp), sum(P[g][1] for g in grp) / len(grp), P[grp[0]][2]))
    return out


def _road_angle(x, y):
    """v1.88: the angle from (x, y) to the nearest road cover piece, or None"""
    if not COVER_ON[0]:
        return None
    S_ = _shp()
    if not S_:
        return None
    sg_ = S_[1]
    rd = [p["poly"] for p in COVER_PIECES if p["mat"] == "road"]
    if not rd:
        return None
    if ROAD_TREE[0] is None:
        ROAD_TREE[0] = (S_[3].STRtree(rd), rd)
    tr, rd = ROAD_TREE[0]
    pt = sg_.Point(x, y)
    try:
        j = tr.nearest(pt)
    except Exception:
        return None
    if j is None:
        return None
    from shapely.ops import nearest_points
    q = nearest_points(rd[int(j)], pt)[0]
    if math.hypot(q.x - x, q.y - y) < 0.05 or math.hypot(q.x - x, q.y - y) > 15.0:
        return None
    return math.atan2(q.y - y, q.x - x)


ROAD_TREE = [None]


def setup_library(ac, log):
    """v1.79: AcBuild's GDL objects, then Archicad's own detailed trees per species in EVERY case (v1.78 picked them only
    when the embedded library call succeeded; it timed out on 19 Nov and all 803 trees were left out)"""
    _setup_library(ac, log)
    if GDL_OBJECTS:
        try:
            av = ac.t("GetAvailableLibraryParts", {}, 900.0).get("libraryParts") or []
            nms_ = set(p.get("documentName") or (p.get("fileName") or u"").rsplit(u".", 1)[0] for p in av)
            _lib_trees(nms_, log)
            lp_ = next((n_ for n_ in LAMP_LIB if n_ in nms_), None)
            if lp_ and "lamp" in LIBN:                     # v1.88: Archicad's own street lamp (was AcBuild's box lamp)
                LAMP_OWN[0] = LIBN["lamp"]
                LIBN["lamp"] = lp_
                log.append(u"street lamps (v1.88): Archicad library part %s (AcBuild's own lamp only where it is refused)" % lp_)
        except Exception as ex:
            if _ac_gone(ex):
                raise
            log.append(u"FLAG trees: Archicad's library parts not listed (%s)" % ex)


def _setup_library(ac, log):
    """v1.45: AcBuild's GDL objects (trees, street furniture, people, cars) in its own loaded library folder"""
    LIBN.clear()
    if not GDL_OBJECTS:                                   # v1.63 (Aras 12:11): the file is heavy enough
        log.append(u"GDL objects: off (v1.63, Aras 18 Nov): trees as trunk + crown slabs, no street furniture / people / cars")
        return
    if ac.has("CreateLibraryParts"):                      # v1.62: embedded library, scripts in the same call
        try:
            av = ac.t("GetAvailableLibraryParts", {}, 900.0).get("libraryParts") or []
            dn_ = set(p.get("documentName") for p in av)
            par = next((n_ for n_ in (u"Model Element", u"General Object") if n_ in dn_), u"Model Element")
            LIB_PAR[0] = par                              # v1.75: for the bridge objects
            kinds_, data_ = [], []
            for kind, s3 in GDL3D.items():
                nm = u"BGA %s" % kind.replace("_", " ").title()
                s2 = GDL2D_TREE if kind in ("olive", "plane", "ash", "deciduous", "stone_pine", "evergreen", "rosemary",
                                            "willow", "tamarisk") else GDL2D_OBJ
                kinds_.append(kind)
                data_.append(dict(name=nm, parentName=par, path=u"BGA/%s.gsm" % nm, script3D=s3, script2D=s2))
            import hashlib                                # v1.79: the same scripts already embedded: not sent again
            h_ = hashlib.sha1(json.dumps(data_, sort_keys=True).encode("utf-8")).hexdigest()
            hf_ = os.path.join(CACHE_DIR, "gdl_scripts.sha1")
            try:
                old_h = open(hf_).read().strip()
            except Exception:
                old_h = None
            if old_h == h_ and all(d_["name"] in dn_ for d_ in data_):
                for kind, d_ in zip(kinds_, data_):
                    LIBN[kind] = d_["name"]
                log.append(u"GDL objects (v1.79): %d embedded part(s) already in the project with the same scripts: "
                           u"not sent again" % len(LIBN))
                return
            try:                                          # written first: a call that times out may still embed them
                os.makedirs(CACHE_DIR, exist_ok=True)
                with open(hf_, "w") as f_:
                    f_.write(h_)
            except Exception:
                pass
            r_ = ac.t("CreateLibraryParts", {"libraryParts": data_, "overwriteExisting": True}, 900.0)
            for kind, d_, e in zip(kinds_, data_, r_.get("libraryParts") or []):
                if isinstance(e, dict) and not e.get("error"):
                    LIBN[kind] = d_["name"]
                elif not GDL_ERR[0]:
                    GDL_ERR[0] = u"%s: %s" % (d_["name"], json.dumps(e)[:300])
            log.append(u"GDL objects (v1.62, embedded library, parent %s): %d of %d made%s" % (
                par, len(LIBN), len(GDL3D), u"" if len(LIBN) == len(GDL3D) else u"; FLAG first reason: %s" % GDL_ERR[0]))
            if LIBN:
                return
        except Exception as ex:
            if _ac_gone(ex):
                raise
            try:                                          # v1.79: a timed-out call may have embedded them all the same
                dn2_ = set(p.get("documentName") for p in (ac.t("GetAvailableLibraryParts", {}, 900.0).get("libraryParts") or []))
                for kind in GDL3D:
                    if u"BGA %s" % kind.replace("_", " ").title() in dn2_:
                        LIBN[kind] = u"BGA %s" % kind.replace("_", " ").title()
            except Exception:
                pass
            if LIBN:
                log.append(u"FLAG GDL objects: the embedded library call failed (%s), but %d of %d parts are in the project: "
                           u"used" % (ex, len(LIBN), len(GDL3D)))
                return
            log.append(u"FLAG GDL objects in the embedded library not made (%s): trying the library folder" % ex)
    need = ("GetLibraries", "SetLibraries", "GetAvailableLibraryParts", "CreateLibraryPart", "SetLibraryPartScripts",
            "CreateObjects")
    if not all(ac.has(c) for c in need):
        log.append(u"FLAG GDL objects: Tapir lacks %s: trees stay slab trees, no street furniture" % u", ".join(
            c for c in need if not ac.has(c)))
        return
    try:
        os.makedirs(LIB_DIR, exist_ok=True)
        libs = ac.t("GetLibraries").get("libraries") or []
        loc = [l_.get("path") for l_ in libs if l_.get("path") and "local" in (l_.get("type") or u"").lower()]
        if not any(os.path.normcase(os.path.abspath(p)) == os.path.normcase(os.path.abspath(LIB_DIR)) for p in loc):
            ac.t("SetLibraries", {"libraries": [{"path": p} for p in loc + [LIB_DIR]]}, 900.0)
        av = ac.t("GetAvailableLibraryParts", {}, 900.0).get("libraryParts") or []
        fn_ = dict((p.get("fileName"), p) for p in av if p.get("fileName"))
        anc = next((n_ for n_ in ("General GDL Object.gsm", "Model Element.gsm", "Object.gsm") if n_ in fn_), None) or \
            next((n_ for n_ in fn_ if "general" in n_.lower() and "object" in n_.lower()), None)
        if not anc:
            log.append(u"FLAG GDL objects: no general object subtype found in the loaded libraries")
            return
        TODO_ = []                                        # v1.56: (kind, name, 3D, 2D) still to script
        for kind, s3 in GDL3D.items():
            nm = u"Bergama %s" % kind.replace("_", " ").title()
            path = os.path.join(LIB_DIR, nm + u".gsm")
            if not os.path.isfile(path):
                ac.t("CreateLibraryPart", {"path": path, "ancestorSubtype": anc}, 900.0)
            s2 = GDL2D_TREE if kind in ("olive", "plane", "ash", "deciduous", "stone_pine", "evergreen", "rosemary", "willow", "tamarisk") \
                else GDL2D_OBJ
            TODO_.append((kind, nm, s3, s2))              # v1.56: scripts set after one library reload (below)
        for k_try in (0, 1):                              # v1.56: the new .gsm files are loaded only after a reload
            if not TODO_:
                break
            try:
                if ac.has("ReloadLibraries"):
                    ac.t("ReloadLibraries", {}, 900.0)
                else:
                    libs = ac.t("GetLibraries").get("libraries") or []
                    loc = [l_.get("path") for l_ in libs if l_.get("path") and "local" in (l_.get("type") or u"").lower()]
                    ac.t("SetLibraries", {"libraries": [{"path": p} for p in loc]}, 900.0)
            except Exception as ex:
                GDL_ERR[0] = GDL_ERR[0] or u"library reload: %s" % ex
            left_ = []
            for kind, nm, s3, s2 in TODO_:
                r_ = ac.t("SetLibraryPartScripts", {"libraryParts": [{"name": nm + u".gsm", "scripts": {"3d": s3, "2d": s2}}]})
                if any(isinstance(e, dict) and e.get("success") for e in (r_.get("executionResults") or [])):
                    LIBN[kind] = nm
                else:
                    left_.append((kind, nm, s3, s2))
                    if k_try and not GDL_ERR[0]:          # v1.55: Archicad's reason, logged once
                        GDL_ERR[0] = u"%s: %s" % (nm, json.dumps((r_.get("executionResults") or [r_])[:1])[:300])
            TODO_[:] = left_
            if not TODO_:
                break
        log.append(u"GDL objects (v1.45, ancestor %s, in %s): %s" % (anc, LIB_DIR, u", ".join(sorted(LIBN.values()))))
        if len(LIBN) < len(GDL3D):
            log.append(u"FLAG GDL objects not made: %s (first reason: %s)" % (
                u", ".join(k for k in GDL3D if k not in LIBN), GDL_ERR[0] or u"none given"))   # v1.55
    except Exception as ex:
        log.append(u"FLAG GDL objects not made (%s): trees stay slab trees, no street furniture" % ex)
        LIBN.clear()


def _jit(x, y):
    """v1.45: a stable pseudo-random (0..1) pair from a position (the same every pass: elements are kept)"""
    a = math.sin(x * 12.9898 + y * 78.233) * 43758.5453
    b = math.sin(x * 39.3468 + y * 11.135) * 24634.6345
    return a - math.floor(a), b - math.floor(b)


def build_objects(ac, miss, log, xy, z0, tin, ox, oy, survey):
    """v1.45: every tree (his planting, the survey trees, every survey olive symbol), the survey street furniture and
    the people and cars of his assets layer as GDL objects, on the surveyed ground, inside site_alan"""
    made = []
    if N_NOTREE[0]:                                      # v1.68
        log.append(u"FLAG %d tree(s) left out: no GDL object of their kind could be made (no slab trees, Aras 18 Nov)%s"
                   % (N_NOTREE[0], (u"; first reason: " + GDL_ERR[0]) if GDL_ERR[0] else u""))
    if not LIBN or "CreateObjects" in miss:
        return made
    gz = lambda p: tin.z(p[0] - ox, p[1] - oy)
    ins = (lambda p: _inpoly(p, SITE_POLY)) if SITE_POLY else (lambda p: True)
    sym = survey.get("_sym") or {}
    trees = list(TREE_OBJ)
    for x, y, a in (sym.get("SEMBOL_ZEYTINLIK") or []):  # every survey olive symbol: one olive tree
        if ins((x, y)) and gz((x, y)) is not None:
            trees.append(("olive", (x, y), gz((x, y)), OLIVE_H, OLIVE_D))
    objs, n_k = [], {}
    SP_, n_clash = _Spread(), [0]                         # v1.76: no object on a house or on another object
    for kind, c, g, H_, D in trees:
        if kind not in LIBN:
            continue
        if _in_bld(c, 0.5) or not SP_.free(c, TREE_GAP_M / 2.0):
            n_clash[0] += 1
            continue
        j1, j2 = _jit(c[0], c[1])
        f = 0.85 + 0.3 * j1                               # +-15 % size, a turn of its own
        objs.append(dict(libraryPartName=LIBN[kind], coordinates=dict(xy(c), z=round(g - z0, 3)),
                         dimensions=dict(x=round(D * f, 2), y=round(D * f, 2), z=round(H_ * f, 2)),
                         angle=round(2 * math.pi * j2, 4)))
        n_k[kind] = n_k.get(kind, 0) + 1
    if objs:
        made += [g for g in ac.create("CreateObjects", "objectsData", objs, u"tree objects (GDL, simplified real)") if g]
    log.append(u"trees as GDL objects: %s (olive %.0f m / %.0f m crown ASSUMED, others as before; one olive per survey "
               u"symbol: the symbols mark groves)" % (u", ".join(u"%s %d" % kv for kv in sorted(n_k.items())), OLIVE_H, OLIVE_D))
    fo, n_f, fo_kind = [], {}, []
    n_lm = [0, 0]
    for lay, (kind, w, d, h, lab) in FURN.items():
        if kind not in LIBN:
            continue
        P_ = list(sym.get(lay) or [])
        if kind == "lamp":                                 # v1.88: one lamp per survey lamp, facing the road
            n_lm[0] += len(P_)
            P_ = _merge_pts(P_, LAMP_MERGE_M)
            n_lm[1] += len(P_)
        for x, y, a in P_:
            if not ins((x, y)) or gz((x, y)) is None:
                continue
            if _in_bld((x, y), max(w, d) / 2.0) or not SP_.free((x, y), max(w, d) / 2.0):   # v1.76
                n_clash[0] += 1
                continue
            ra_ = _road_angle(x, y) if kind == "lamp" else None
            o_ = dict(libraryPartName=LIBN[kind], coordinates=dict(xy((x, y)), z=round(gz((x, y)) - z0, 3)),
                      dimensions=dict(x=w, y=d, z=h), angle=round(ra_ if ra_ is not None else a, 4))
            if kind == "lamp" and LAMP_OWN[0]:
                o_.pop("dimensions")                       # v1.88: the library lamp keeps its own size
            fo.append(o_)
            fo_kind.append((kind, w, d, h))
            n_f[lab] = n_f.get(lab, 0) + 1
    if fo:
        g_ = ac.create("CreateObjects", "objectsData", fo, u"street furniture (GDL, survey symbols)")
        made += [g for g in g_ if g]
        bad_ = [dict(o_, libraryPartName=LAMP_OWN[0], dimensions=dict(x=k_[1], y=k_[2], z=k_[3]))
                for o_, k_, g in zip(fo, fo_kind, g_) if not g and k_[0] == "lamp" and LAMP_OWN[0]]
        if bad_:                                           # v1.88: AcBuild's own lamp where the library one is refused
            made += [g for g in ac.create("CreateObjects", "objectsData", bad_, u"street furniture (GDL, survey symbols)") if g]
    if n_lm[0]:
        log.append(u"street lamps (v1.88): %d survey lamp points merged to %d lamps (points within %.1f m are one lamp), "
                   u"each turned toward the nearest road (the library lamp's arm direction ASSUMED along its x axis)" % (
                       n_lm[0], n_lm[1], LAMP_MERGE_M))
    log.append(u"street furniture from the survey symbols: %s; sizes ASSUMED" % (
        u", ".join(u"%s %d" % kv for kv in sorted(n_f.items())) or u"none"))
    # pools: water skins in the survey pool outlines
    # ---- people + cars: his assets layer, shapes grouped by touch, sorted by size
    try:
        with open(MP_FILE, encoding="utf-8") as f_:
            AS = (json.load(f_).get("layers") or {}).get("assets") or []
    except Exception:
        AS = []
    pcs = []
    for pc in AS:
        R = pc[4] if len(pc) > 4 else None
        if not R or len(R) < 2:
            continue
        xs, ys = [q[0] for q in R], [q[1] for q in R]
        bx = (min(xs), min(ys), max(xs), max(ys))
        if bx[2] - bx[0] > 6.0 or bx[3] - bx[1] > 6.0 or not ins(((bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2)):
            continue
        pcs.append((bx, R))
    cell, par = {}, list(range(len(pcs)))

    def fd(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i
    for i, (bx, R) in enumerate(pcs):
        for a in range(int(bx[0] // 2), int(bx[2] // 2) + 1):
            for b in range(int(bx[1] // 2), int(bx[3] // 2) + 1):
                for j in cell.get((a, b), []):
                    bj = pcs[j][0]
                    if bx[0] <= bj[2] + 0.05 and bj[0] <= bx[2] + 0.05 and bx[1] <= bj[3] + 0.05 and bj[1] <= bx[3] + 0.05:
                        par[fd(i)] = fd(j)
                cell.setdefault((a, b), []).append(i)
    G = {}
    for i in range(len(pcs)):
        G.setdefault(fd(i), []).append(i)
    po, n_p, n_c = [], 0, 0
    for gi in G.values():
        P = [q for k in gi for q in pcs[k][1]]
        cx, cy = sum(q[0] for q in P) / len(P), sum(q[1] for q in P) / len(P)
        sxx = sum((q[0] - cx) ** 2 for q in P); syy = sum((q[1] - cy) ** 2 for q in P)
        sxy = sum((q[0] - cx) * (q[1] - cy) for q in P)
        ang = 0.5 * math.atan2(2 * sxy, sxx - syy)
        u_, v_ = (math.cos(ang), math.sin(ang)), (-math.sin(ang), math.cos(ang))
        ts = [(q[0] - cx) * u_[0] + (q[1] - cy) * u_[1] for q in P]
        ws = [(q[0] - cx) * v_[0] + (q[1] - cy) * v_[1] for q in P]
        L_, W_ = max(ts) - min(ts), max(ws) - min(ws)
        g = gz((cx, cy))
        if g is None:
            continue
        if _in_bld((cx, cy), max(L_, W_, 0.5) / 2.0) or not SP_.free((cx, cy), max(L_, W_, 0.5) / 2.0):   # v1.76
            n_clash[0] += 1
            continue
        if 3.6 <= L_ <= 5.6 and 1.5 <= W_ <= 2.4 and "car" in LIBN:
            po.append(dict(libraryPartName=LIBN["car"], coordinates=dict(xy((cx, cy)), z=round(g - z0, 3)),
                           dimensions=dict(x=round(L_, 2), y=round(W_, 2), z=CAR_H), angle=round(ang, 4)))
            n_c += 1
        elif 0.25 <= L_ <= 0.9 and W_ <= 0.9 and "person" in LIBN:
            po.append(dict(libraryPartName=LIBN["person"], coordinates=dict(xy((cx, cy)), z=round(g - z0, 3)),
                           dimensions=dict(x=0.5, y=0.3, z=PERSON_H), angle=round(ang, 4)))
            n_p += 1
    if po:
        made += [g for g in ac.create("CreateObjects", "objectsData", po, u"people + cars (his assets layer)") if g]
    log.append(u"collisions (v1.76): %d tree / furniture / person / car object(s) left out: on a house or on another "
               u"object" % n_clash[0])
    log.append(u"people + cars from his assets layer: %d shape groups in site_alan, %d people (0.25-0.9 m), %d cars "
               u"(3.6-5.6 x 1.5-2.4 m): positions his, the person / car reading by size only (DERIVED); heights ASSUMED "
               u"person %.2f m, car %.2f m; on the surveyed ground" % (len(G), n_p, n_c, PERSON_H, CAR_H))
    return made


def build_banks(ac, miss, log, xy, z0, tin, ox, oy, survey):
    """v1.45: bank zones: grass Mesh skins on the surveyed ground between each top-of-slope line (SEV_UST) and the
    toe-of-slope points (SEV_ALT) facing it, cutting the ground; none inside the river outline (the bed is there)"""
    made = []
    if "CreateMeshes" in miss or COVER_ON[0]:             # v1.88: the bank zones are ground covers
        return made
    gz = lambda p: tin.z(p[0] - ox, p[1] - oy)
    ins = (lambda p: _inpoly(p, SITE_POLY)) if SITE_POLY else (lambda p: True)
    RP = [_pip_fast(H) for _g, H in RIVER_MESH]
    toe = {}
    for pl in survey.get("SEV_ALT") or []:
        for q in pl:
            toe.setdefault((int(q[0] // 10), int(q[1] // 10)), []).append((q[0], q[1]))

    def near_toe(p):
        i, j = int(p[0] // 10), int(p[1] // 10)
        c_ = [q for a in range(i - 2, i + 3) for b in range(j - 2, j + 3) for q in toe.get((a, b), [])]
        if not c_:
            return None
        q = min(c_, key=lambda q: (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2)
        return q if math.hypot(q[0] - p[0], q[1] - p[1]) <= BANK_PAIR_M else None
    skins = []
    for pl in survey.get("SEV_UST") or []:
        S = []
        for a, b in zip(pl, pl[1:]):
            L_ = math.hypot(b[0] - a[0], b[1] - a[1])
            for k in range(max(1, int(L_ // 2.0))):
                S.append((a[0] + (b[0] - a[0]) * k / max(1, int(L_ // 2.0)), a[1] + (b[1] - a[1]) * k / max(1, int(L_ // 2.0))))
        run = []
        for p in S + [None]:
            t = near_toe(p) if p is not None and ins(p) else None
            if t is not None and math.hypot(t[0] - p[0], t[1] - p[1]) > 0.5:
                run.append((p, t))
                continue
            if len(run) >= 2:
                P = [r[0] for r in run] + [r[1] for r in reversed(run)]
                P = clean(P)
                c = (sum(q[0] for q in P) / len(P), sum(q[1] for q in P) / len(P))
                if len(P) >= 3 and abs(area(P)) > 1.0 and not any(f_(c) for f_ in RP):
                    zs = [gz(q) for q in P]
                    if all(z is not None for z in zs):
                        lo = min(zs) - 0.3
                        skins.append(dict(level=round(lo - z0, 3), skirtType="SolidBodyWithSkirt", skirtLevel=0.02,
                                          ridges="AllSmooth", polygonCoordinates=[dict(xy(q), z=round(z - lo, 3))
                                                                                  for q, z in zip(P, zs)], _mat="park"))
            run = []
    if skins:
        g_ = ac.create("CreateMeshes", "meshesData", skins, u"bank zones (grass skins, survey SEV_UST / SEV_ALT)")
        made += [g for g in g_ if g]
        EXTRA_OPS.extend((g, "Subtraction", [dict(x=q["x"], y=q["y"]) for q in d["polygonCoordinates"]])
                         for g, d in zip(g_, skins) if g)
    log.append(u"bank zones: %d grass skins between the survey top- and toe-of-slope lines (paired within %.0f m), "
               u"0.30 m deep, cutting the ground; surface grass ASSUMED" % (len(skins), BANK_PAIR_M))
    return made


def _straighten(P, closed):
    """v1.70: drop points within STRAIGHT_TOL_M of the line between their neighbours (straight runs -> one edge)"""
    P = list(P)
    ch = True
    while ch and len(P) > (3 if closed else 2):
        ch = False
        rng = range(len(P)) if closed else range(1, len(P) - 1)
        for i in rng:
            a, q, b = P[i - 1], P[i], P[(i + 1) % len(P)]
            if _seg_d(q, a, b) < STRAIGHT_TOL_M:
                del P[i]
                ch = True
                break
    return P


def _merge_runs(ch):
    """v1.71: consecutive wall test pieces (p0, p1, lo, hi) or None -> one piece per run (top within LINE_RISE_M)"""
    out, cur = [], None
    for c in ch + [None]:
        if c is not None and cur is not None and abs(c[3] - cur[3]) <= LINE_RISE_M and abs(c[3] - cur[4]) <= LINE_RISE_M:
            cur = [cur[0], c[1], min(cur[2], c[2]), max(cur[3], c[3]), cur[4]]
            continue
        if cur is not None:
            out.append(tuple(cur[:4]))
        cur = None if c is None else [c[0], c[1], c[2], c[3], c[3]]
    return out


# ================================================================ v1.88 ground covers (Aras 20 Nov 09:55-10:03 "fix roads
# and streets ... retry with a different approach"; "if you are drawing this park over landscape, just draw the landscape
# underneath it. currently you are drawing both in the same space"; "same two object shouldn't be constructed in the same
# area"; "not just in section or just in plan"; "you are mixing a lot of areas for what they are in the masterplan"):
# every surface area (his masterplan surface layers in his drawing order, the survey roads and parks, the bank zones)
# becomes ONE set of non-overlapping pieces: where two areas overlap only the one he drew on top is built. Each piece is a
# Mesh body whose top is the surveyed ground and whose flat bottom lies COVER_T under its lowest point; the ground mesh is
# lowered under every piece to just below that bottom (heights on the piece outline and a point COVER_OUT_M outside it
# pin the edge), so the ground lies UNDER the road / park / paving and never in the same space. No solid element
# operation. Needs the Python package shapely (2.x); without it v1.87's roads / parks / slabs are built and a FLAG says so.
COVER = True
COVER_LAYERS = {"kesin_yesil": "park", "belki_yesil": "park", "begum_yesil": "park", "Layer_49": "park", "master": "park",
                "normal": "pavement", "path": "pavement", "yeni": "pavement", "yol_kenar": "pavement",
                "circulation": "pavement", "araba_yolu": "road", "iskele_kenari": "quay_grey", "doldrurma": "ground"}
# his surface layer -> material: by the layer's name (yesil = green, yol = road, path / circulation = paving, iskele kenari
# = his quay paving, doldurma = fill); ASSUMED where the name does not say it (master, Layer_49 = green, yeni = paving)
COVER_SOLID = ("teras", "bina_cerceve", "begum_su_merdiven")   # his slabs on the ground: the ground goes under their bottom
COVER_T = {"road": 0.30, "pavement": 0.25, "quay_grey": 0.25, "park": 0.30, "ground": 0.20}   # m build-up: ASSUMED
COVER_BOX_M = 100.0        # m: pieces start as the areas cut by this grid ...
COVER_RELIEF_M = 1.0       # m: ... and a piece whose ground rises more than this is quartered (body at most T + 1 m deep)
COVER_MIN_M = 6.25         # m: smallest quarter (steeper ground keeps a deeper body there)
COVER_EDGE_M = 2.0         # m: height points along a piece's outline (its own mesh and the ground under it)
COVER_IN_M = 4.0           # m: height points inside a piece (its own mesh)
COVER_OUT_M = 0.05         # m: the ground point just outside an outline, at the surveyed height
COVER_GAP_M = 0.02         # m: the ground stays this much under a piece's bottom
COVER_MIN_M2 = 2.0         # m2: a smaller leftover is not built (the ground shows there, not lowered)
COVER_THIN_M = 0.5         # m: a leftover thinner than this on average (2 x area / perimeter) is not built either
COVER_PIECES = []          # dicts: mat, label, poly (shapely, survey m), low (m), plat (m), solid (bool)
COVER_IDX = [None, None]   # STRtree of the pieces grown by COVER_GAP_M, STRtree of the outline lines
COVER_TILE_PTS = {}        # (tile i, j) -> [(x, y, z)] ground heights on and just outside the outlines
COVER_ON = [False]
COVER_STAT = {}


def _shp():
    """v1.88: the shapely modules, or None"""
    try:
        import shapely
        from shapely import geometry as sg_, ops as so_, strtree as st_
        if int(shapely.__version__.split(".")[0]) < 2:
            return None
        return shapely, sg_, so_, st_
    except Exception:
        return None


def _cover_items(SP, survey, tin, ox, oy):
    """v1.88: [(order, key, mat, label, ring, holes, solid_bottom)] low to high: bank zones, survey parks, survey roads,
    then his masterplan pieces in the order of his drawing"""
    items = []
    gz = lambda p: tin.z(p[0] - ox, p[1] - oy)
    # bank zones (survey top / toe of slope), as build_banks pairs them
    toe = {}
    for pl in survey.get("SEV_ALT") or []:
        for q in pl:
            toe.setdefault((int(q[0] // 10), int(q[1] // 10)), []).append((q[0], q[1]))

    def near_toe(p):
        i, j = int(p[0] // 10), int(p[1] // 10)
        c_ = [q for a in range(i - 2, i + 3) for b in range(j - 2, j + 3) for q in toe.get((a, b), [])]
        if not c_:
            return None
        q = min(c_, key=lambda q: (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2)
        return q if math.hypot(q[0] - p[0], q[1] - p[1]) <= BANK_PAIR_M else None
    for pl in survey.get("SEV_UST") or []:
        S = []
        for a, b in zip(pl, pl[1:]):
            n_ = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) // 2.0))
            S += [(a[0] + (b[0] - a[0]) * k / n_, a[1] + (b[1] - a[1]) * k / n_) for k in range(n_)]
        run = []
        for p in S + [None]:
            t = near_toe(p) if p is not None else None
            if t is not None and math.hypot(t[0] - p[0], t[1] - p[1]) > 0.5:
                run.append((p, t))
                continue
            if len(run) >= 2:
                items.append(("bank", "park", u"bank zones (grass on the ground, v1.88)",
                              [r[0] for r in run] + [r[1] for r in reversed(run)], [], None))
            run = []
    try:
        M = read_json(MB_FILE, "MapBase", [])
    except Exception:
        M = None
    polys = (M or {}).get("polys") or {}
    for R in polys.get("parks") or []:
        if len(R) >= 3:
            items.append(("park", "park", u"town ground: parks on the ground (v1.88)", [tuple(q[:2]) for q in R], [], None))
    st = [[tuple(q[:2]) for q in R] for R in (polys.get("street_net") or []) if len(R) >= 3]
    if st:
        items.append(("road", "road", u"town ground: roads on the ground (v1.88)", None, st, None))   # even-odd rings
    for nm, R, H in SP:
        if nm in COVER_LAYERS:
            mat = PIECE_KEY.get(id(H)) or COVER_LAYERS[nm]
            lab = (u"masterplan unsure %s: best guess %s on the ground (v1.88)" % (nm, mat)) if nm in MP_UNSURE else \
                u"masterplan covers on the ground (v1.88)"
            items.append(("mp", mat, lab, list(H), [], None))
        elif nm in COVER_SOLID:
            items.append(("solid", nm, None, list(H), [], nm))
    return items


def cover_plan(log, tin, ox, oy, SP, bld, survey):
    """v1.88: COVER_PIECES (non-overlapping, his drawing order wins) + the ground heights that lower the ground under them"""
    del COVER_PIECES[:]
    COVER_IDX[:] = [None, None]
    COVER_TILE_PTS.clear()
    COVER_STAT.clear()
    COVER_ON[0] = False
    if not COVER:
        return
    S_ = _shp()
    if not S_:
        log.append(u"FLAG ground covers (v1.88) off: the Python package shapely 2.x is missing (py -3 -m pip install "
                   u"shapely): roads, parks and his areas built as in v1.87, in the same space as the ground")
        return
    shapely, sg_, so_, st_ = S_
    t0_ = time.time()

    def mk(R, holes=()):
        try:
            g = sg_.Polygon(R, [h for h in holes if len(h) >= 3]).buffer(0)
            return g if not g.is_empty and g.area > 0.01 else None
        except Exception:
            return None
    site = mk(SITE_POLY) if SITE_POLY else None
    gz = lambda p: tin.z(p[0] - ox, p[1] - oy)
    # what nothing may cover: houses (they stand on the ground) and his river (the bed and water are built there)
    nogo = [mk(b["ring"]) for b in bld if b.get("ring") and len(b["ring"]) >= 3]
    nogo += [mk(R) for R in SEL.get("river") or [] if len(R) >= 3]
    nogo = so_.unary_union([g for g in nogo if g is not None]) if any(g is not None for g in nogo) else None
    items = []
    for kind, mat, lab, R, holes, solid in _cover_items(SP, survey, tin, ox, oy):
        if kind == "road":
            g = None
            for R_ in holes:                              # even-odd: a ring inside another is a town block (a hole)
                p_ = mk(R_)
                if p_ is not None:
                    g = p_ if g is None else g.symmetric_difference(p_)
        else:
            g = mk(R)
        if g is None or g.is_empty:
            continue
        if site is not None:
            g = g.intersection(site)
        if nogo is not None:
            g = g.difference(nogo)
        if g.is_empty or g.area < COVER_MIN_M2:
            continue
        bot = None
        if solid:                                         # the bottom of his slab as build_site makes it
            gs = [z for z in (gz(q) for q in R) if z is not None]
            c = (sum(q[0] for q in R) / len(R), sum(q[1] for q in R) / len(R))
            gc = gz(c)
            if not gs:
                continue
            if solid == "begum_su_merdiven":
                bot = min(gs) - 0.40
            else:
                th, up = MP_SLABS[solid]
                bot = min((gc if gc is not None else min(gs)) + up - th, min(gs))
        items.append((len(items), kind, mat, lab, g, bot))
    if not items:
        log.append(u"ground covers (v1.88): nothing to cover (no survey roads / parks, no masterplan surface pieces)")
        return
    tree = st_.STRtree([it[4] for it in items])
    xs0, ys0, xs1, ys1 = (site.bounds if site is not None else
                          (min(it[4].bounds[0] for it in items), min(it[4].bounds[1] for it in items),
                           max(it[4].bounds[2] for it in items), max(it[4].bounds[3] for it in items)))
    pieces, n_drop = [], [0, 0]

    def relief(P):
        """lowest + highest surveyed ground over piece P (outline every 2 m + inside every 2 m)"""
        zs = []
        for ring in [P.exterior] + list(P.interiors):
            C = list(ring.coords)
            for a, b in zip(C, C[1:]):
                n_ = max(1, int(math.ceil(math.hypot(b[0] - a[0], b[1] - a[1]) / 2.0)))
                zs += [gz((a[0] + (b[0] - a[0]) * k / n_, a[1] + (b[1] - a[1]) * k / n_)) for k in range(n_)]
        bx = P.bounds
        try:
            from shapely.prepared import prep as prep_
            pr = prep_(P)
        except Exception:
            pr = None
        x = math.floor(bx[0] / 2.0) * 2.0 + 1.0
        while x < bx[2]:
            y = math.floor(bx[1] / 2.0) * 2.0 + 1.0
            while y < bx[3]:
                pt = sg_.Point(x, y)
                if (pr.contains(pt) if pr else P.contains(pt)):
                    zs.append(gz((x, y)))
                y += 2.0
            x += 2.0
        zs = [z for z in zs if z is not None]
        return (min(zs), max(zs)) if zs else (None, None)

    def add(P, it, size):
        if P.is_empty:
            return
        for Q in (list(P.geoms) if hasattr(P, "geoms") else [P]):
            if Q.geom_type != "Polygon" or Q.is_empty:
                continue
            if Q.area < COVER_MIN_M2 or 2.0 * Q.area / max(Q.length, 1e-9) < COVER_THIN_M:
                n_drop[0] += 1
                continue
            lo, hi = relief(Q)
            if lo is None:
                n_drop[1] += 1
                continue
            if it[1] != "solid" and hi - lo > COVER_RELIEF_M and size / 2.0 >= COVER_MIN_M - 1e-6:
                bx = Q.bounds
                h_ = size / 2.0
                x = math.floor(bx[0] / h_) * h_
                while x < bx[2]:
                    y = math.floor(bx[1] / h_) * h_
                    while y < bx[3]:
                        add(Q.intersection(sg_.box(x, y, x + h_, y + h_)), it, h_)
                        y += h_
                    x += h_
                continue
            from shapely.geometry.polygon import orient as orient_
            Q = Q.simplify(0.01)
            if Q.is_empty or Q.geom_type != "Polygon" or not Q.is_valid:
                n_drop[0] += 1
                continue
            Q = orient_(Q, 1.0)
            if it[1] == "solid":
                low = it[5]
            else:
                low = lo - COVER_T.get(it[2], 0.25)
            pieces.append(dict(mat=it[2], label=it[3], poly=Q, low=low, plat=low - COVER_GAP_M, solid=it[1] == "solid",
                               top=hi))
    B = COVER_BOX_M
    x = math.floor(xs0 / B) * B
    while x < xs1:
        y = math.floor(ys0 / B) * B
        while y < ys1:
            bx = sg_.box(x, y, x + B, y + B)
            ix = sorted(int(i) for i in tree.query(bx))
            above = None                                   # what lies above, top of his drawing first
            for i in reversed(ix):
                it = items[i]
                g = it[4].intersection(bx)
                if g.is_empty:
                    continue
                vis = g if above is None else g.difference(above)
                above = g if above is None else above.union(g)
                if not vis.is_empty and vis.area >= COVER_MIN_M2:
                    add(vis.buffer(0), it, B)
            y += B
        x += B
    COVER_PIECES.extend(pieces)
    if not pieces:
        log.append(u"ground covers (v1.88): no piece planned")
        return
    COVER_IDX[0] = st_.STRtree([p["poly"].buffer(COVER_GAP_M, join_style="mitre") for p in pieces])
    rings = []
    for p in pieces:
        rings += [sg_.LineString(r.coords) for r in [p["poly"].exterior] + list(p["poly"].interiors)]
    COVER_IDX[1] = (st_.STRtree(rings), rings)
    # the ground heights on every outline (every COVER_EDGE_M) and COVER_OUT_M outside it where no other piece is
    seen, pts = set(), []
    for p in pieces:
        P = p["poly"]
        for r in [P.exterior] + list(P.interiors):
            C = list(r.coords)
            for a, b in zip(C, C[1:]):
                L_ = math.hypot(b[0] - a[0], b[1] - a[1])
                if L_ < 1e-6:
                    continue
                n_ = max(1, int(math.ceil(L_ / COVER_EDGE_M)))
                nx, ny = (b[1] - a[1]) / L_, -(b[0] - a[0]) / L_
                for k in range(n_):
                    q = (a[0] + (b[0] - a[0]) * k / n_, a[1] + (b[1] - a[1]) * k / n_)
                    key = (round(q[0], 2), round(q[1], 2))
                    if key not in seen:
                        seen.add(key)
                        pts.append(q)
                    for s_ in (1.0, -1.0):                    # the side away from this piece
                        o_ = (q[0] + s_ * nx * COVER_OUT_M, q[1] + s_ * ny * COVER_OUT_M)
                        if P.contains(sg_.Point(o_)):
                            continue
                        key = (round(o_[0], 2), round(o_[1], 2))
                        if key not in seen:
                            seen.add(key)
                            pts.append(o_)
    zs = cover_z_many(pts, [gz(q) for q in pts])
    for q, z in zip(pts, zs):
        if z is not None:
            COVER_TILE_PTS.setdefault((int(q[0] // 10.0), int(q[1] // 10.0)), []).append((q[0], q[1], z))
    COVER_ON[0] = True
    by = {}
    for p in pieces:
        k = p["label"] or u"his slabs (ground under their bottom)"
        by[k] = by.get(k, 0) + 1
    COVER_STAT.update(n=len(pieces), pts=len(pts), drop=n_drop[0], noz=n_drop[1], t=time.time() - t0_)
    log.append(u"ground covers (v1.88): %d pieces with no overlap (his drawing order wins), %s; the ground lowered under "
               u"them (%d outline heights); %d leftovers under %.0f m2 or thinner than %.1f m and %d with no surveyed "
               u"ground not built; build-ups ASSUMED %s; %.1f s" % (
                   len(pieces), u", ".join(u"%s %d" % kv for kv in sorted(by.items())), len(pts), n_drop[0],
                   COVER_MIN_M2, COVER_THIN_M, n_drop[1],
                   u", ".join(u"%s %.2f m" % kv for kv in sorted(COVER_T.items())), time.time() - t0_))


def cover_z_many(qs, zs):
    """v1.88: the ground height at points qs: under a cover piece (or on its outline) its bottom less COVER_GAP_M,
    else the given height (the lowest wins where pieces meet; never higher than the given height)"""
    if not COVER_PIECES or COVER_IDX[0] is None or not qs:
        return list(zs)
    S_ = _shp()
    shapely, sg_ = S_[0], S_[1]
    out = list(zs)
    pts = [sg_.Point(q[0], q[1]) for q in qs]
    try:
        res = COVER_IDX[0].query(pts, predicate="intersects")
    except Exception:
        res = None
    if res is not None and len(res) == 2:
        for i, j in zip(res[0], res[1]):
            pl = COVER_PIECES[int(j)]["plat"]
            i = int(i)
            if out[i] is None or pl < out[i]:
                out[i] = pl
    else:                                                 # older query API: one point at a time
        for i, pt in enumerate(pts):
            for j in COVER_IDX[0].query(pt, predicate="intersects"):
                pl = COVER_PIECES[int(j)]["plat"]
                if out[i] is None or pl < out[i]:
                    out[i] = pl
    return out


def cover_edge_ts(a, b):
    """v1.88: where a tile edge a-b crosses a piece outline: params t (0..1) at the crossing and COVER_OUT_M each side"""
    if not COVER_ON[0] or COVER_IDX[1] is None:
        return []
    sg_ = _shp()[1]
    L_ = math.hypot(b[0] - a[0], b[1] - a[1])
    if L_ < 1e-6:
        return []
    seg = sg_.LineString([a, b])
    tr, rings = COVER_IDX[1]
    ts = []
    for j in tr.query(seg):
        x_ = seg.intersection(rings[int(j)])
        for g in (list(x_.geoms) if hasattr(x_, "geoms") else [x_]):
            if g.is_empty:
                continue
            for c in (list(g.coords) if g.geom_type in ("Point", "LineString") else []):
                t = ((c[0] - a[0]) * (b[0] - a[0]) + (c[1] - a[1]) * (b[1] - a[1])) / (L_ * L_)
                for d in (-COVER_OUT_M / L_, 0.0, COVER_OUT_M / L_):
                    if 0.0 < t + d < 1.0:
                        ts.append(round(t + d, 6))
    return ts


def cover_tile_pts(Pc, x0, y0, x1, y1):
    """v1.88: the outline heights inside one ground tile, at least 0.3 m from its edge"""
    out = []
    cand = [v for i in range(int(x0 // 10.0), int(x1 // 10.0) + 1) for j in range(int(y0 // 10.0), int(y1 // 10.0) + 1)
            for v in COVER_TILE_PTS.get((i, j), ())]
    for x, y, z in cand:
        if x0 < x < x1 and y0 < y < y1 and _inpoly((x, y), Pc) and \
                min(_seg_d((x, y), a_, b_) for a_, b_ in zip(Pc, Pc[1:] + Pc[:1])) >= 0.3:
            out.append((x, y, z))
    return out


def build_covers(ac, miss, log, xy, z0, tin, ox, oy):
    """v1.88: one Mesh body per cover piece: top = the surveyed ground, flat bottom COVER_T under its lowest point"""
    made = []
    if not COVER_ON[0] or "CreateMeshes" in miss:
        return made
    sg_ = _shp()[1]
    gz = lambda p: tin.z(p[0] - ox, p[1] - oy)
    by = {}
    for p in COVER_PIECES:
        if p["solid"]:
            continue
        P, low = p["poly"], p["low"]

        def ring_(r):
            C = list(r.coords)[:-1]
            out_ = []
            for a, b in zip(C, C[1:] + C[:1]):
                n_ = max(1, int(math.ceil(math.hypot(b[0] - a[0], b[1] - a[1]) / COVER_EDGE_M)))
                out_ += [(a[0] + (b[0] - a[0]) * k / n_, a[1] + (b[1] - a[1]) * k / n_) for k in range(n_)]
            return out_
        Ex = ring_(P.exterior)
        zs = [gz(q) for q in Ex]
        if any(z is None for z in zs):
            zf = min([z for z in zs if z is not None] or [low + COVER_T.get(p["mat"], 0.25)])
            zs = [z if z is not None else zf for z in zs]
        d_ = dict(level=round(low - z0, 3), skirtType=TOWN_SKIRT, skirtLevel=COVER_GAP_M / 2.0, ridges="AllSmooth",
                  polygonCoordinates=[dict(xy(q), z=round(z - low, 3)) for q, z in zip(Ex, zs)], _mat=p["mat"])
        hs = []
        for r in P.interiors:
            H = ring_(r)
            hz = [gz(q) for q in H]
            if any(z is None for z in hz):
                continue
            hs.append({"polygonCoordinates": [dict(xy(q), z=round(z - low, 3)) for q, z in zip(H, hz)]})
        if hs:
            d_["holes"] = hs
        sub = []
        bx = P.bounds
        bd = P.boundary
        x = math.floor(bx[0] / COVER_IN_M) * COVER_IN_M + COVER_IN_M / 2.0
        while x < bx[2]:
            y = math.floor(bx[1] / COVER_IN_M) * COVER_IN_M + COVER_IN_M / 2.0
            while y < bx[3]:
                pt = sg_.Point(x, y)
                if P.contains(pt) and bd.distance(pt) >= 0.3:
                    z = gz((x, y))
                    if z is not None:
                        sub.append({"coordinates": [dict(xy((x, y)), z=round(z - low, 3))]})
                y += COVER_IN_M
            x += COVER_IN_M
        if sub:
            d_["sublines"] = sub
        by.setdefault(p["label"], []).append(d_)
    n_ok = n_bad = 0
    for lab, ds in sorted(by.items()):
        g_ = ac.create("CreateMeshes", "meshesData", ds, lab)
        bad = [d for d, g in zip(ds, g_) if not g]
        made += [g for g in g_ if g]
        n_ok += sum(1 for g in g_ if g)
        if bad:                                           # again with the outline and holes only
            for d in bad:
                d.pop("sublines", None)
            g2 = ac.create("CreateMeshes", "meshesData", bad, lab)
            made += [g for g in g2 if g]
            n_ok += sum(1 for g in g2 if g)
            n_bad += sum(1 for g in g2 if not g)
    log.append(u"ground covers (v1.88): %d Mesh bodies made (top = the surveyed ground, bottom %s under its lowest "
               u"point, no solid element operation)%s" % (
                   n_ok, u"/".join(u"%.2f" % v for v in sorted(set(COVER_T.values()))),
                   (u"; FLAG %d refused by Archicad even without inner heights: the lowered ground shows there" % n_bad)
                   if n_bad else u""))
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
    gz = lambda p: _zup(p, tin, ox, oy)                   # v1.83: over the ground as built, whichever way it folds
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
    if COVER_ON[0]:                                       # v1.88: roads + parks are ground covers (build_covers)
        st, pk = [], []
    # even-odd: a street ring inside an odd number of others is a hole (a town block)
    pips = [_pip_fast(R) for R in st]
    bxs = [(min(q[0] for q in R), min(q[1] for q in R), max(q[0] for q in R), max(q[1] for q in R)) for R in st]
    hole = []
    for i, R in enumerate(st):
        p = R[0]
        d = sum(1 for j in range(len(st)) if j != i and bxs[j][0] <= p[0] <= bxs[j][2] and bxs[j][1] <= p[1] <= bxs[j][3]
                and pips[j](p))
        hole.append(d % 2 == 1)
    data, cen, kinds = [], [], []
    n_cell = n_hole = 0
    n_reg = [0, 0, 0]                                     # v1.78: road outlines, park outlines, refused
    REG_G = []
    if TOWN_OUTLINES and "CreateMeshes" not in miss:
        # v1.78 (Aras 19 Nov 07:22 "just draw them from outlines", "draw the roads properly"; 07:25 not slabs, they
        # might collide with the houses' slabs): ONE Mesh-tool skin per road / park outline (its town blocks as
        # holes), the outline itself as the edge, TOWN_LIFT_M over the ground as Archicad built it, with the same
        # heights as the ground mesh inside; no solid element operation, no slab (the street region is already
        # STREET_BLD_CLEAR 1.0 m off every footprint in MapBase)
        def dens_(R):
            out_ = []
            for a_, b_ in zip(R, R[1:] + R[:1]):
                n_ = max(1, int(math.ceil(math.hypot(b_[0] - a_[0], b_[1] - a_[1]) / TOWN_EDGE_M)))
                out_ += [(a_[0] + (b_[0] - a_[0]) * k_ / float(n_), a_[1] + (b_[1] - a_[1]) * k_ / float(n_))
                         for k_ in range(n_)]
            return out_
        g8 = GROUND_GRIDS[0]
        reg_d, reg_k, reg_r = [], [], []
        for kind, rings, hl in (("road", st, hole), ("park", pk, [False] * len(pk))):
            outs = [k for k in range(len(rings)) if not hl[k]]
            ar_ = dict((k, abs(area(rings[k]))) for k in outs)
            own_h = dict((k, []) for k in outs)
            for h_ in [k for k in range(len(rings)) if hl[k]]:
                p_ = rings[h_][0]
                par = [k for k in outs if bxs[k][0] <= p_[0] <= bxs[k][2] and bxs[k][1] <= p_[1] <= bxs[k][3] and pips[k](p_)] \
                    if kind == "road" else []
                if par:
                    own_h[min(par, key=lambda k: ar_[k])].append(h_)
            for k in outs:
                R = rings[k]
                if not any(inr(q) for q in R[::max(1, len(R) // 50)] + [R[0]]):
                    continue
                P = dens_(R)
                Hs = [dens_(rings[h_]) for h_ in own_h[k]]
                zs_ = [z for z in (gz(q) for q in P) if z is not None]
                if not zs_:
                    continue
                low = min(zs_) - TOWN_UNDER_M
                lo_z = min(zs_)
                zq = lambda q: (gz(q) if gz(q) is not None else lo_z)
                d_ = dict(level=round(low - z0 + TOWN_LIFT_M, 3), skirtType=TOWN_SKIRT, skirtLevel=0.05,
                          ridges="AllSmooth", polygonCoordinates=[dict(xy(q), z=round(zq(q) - low, 3)) for q in P],
                          _mat=kind)
                if Hs:
                    d_["holes"] = [{"polygonCoordinates": [dict(xy(q), z=round(zq(q) - low, 3)) for q in H]} for H in Hs]
                pin_ = _pip_fast(R)
                sg_ = {}                                  # edges per 2 m cell: no height point within 0.3 m of an edge
                for E_ in [P] + Hs:
                    for a_, b_ in zip(E_, E_[1:] + E_[:1]):
                        for cx_ in range(int(math.floor(min(a_[0], b_[0]) / 2.0)), int(math.floor(max(a_[0], b_[0]) / 2.0)) + 1):
                            for cy_ in range(int(math.floor(min(a_[1], b_[1]) / 2.0)), int(math.floor(max(a_[1], b_[1]) / 2.0)) + 1):
                                sg_.setdefault((cx_, cy_), []).append((a_, b_))
                near_e = lambda q: any(_seg_d(q, a_, b_) < 0.3 for di in (-1, 0, 1) for dj in (-1, 0, 1)
                                       for a_, b_ in sg_.get((int(math.floor(q[0] / 2.0)) + di, int(math.floor(q[1] / 2.0)) + dj), ()))
                hin_ = [(min(q[0] for q in H), min(q[1] for q in H), max(q[0] for q in H), max(q[1] for q in H),
                         _pip_fast(H)) for H in Hs]
                bx0, by0 = min(q[0] for q in R), min(q[1] for q in R)
                bx1, by1 = max(q[0] for q in R), max(q[1] for q in R)
                sub_ = []
                for ti in range(int((bx0 - TILE_G[0]) // TILE_G[2]), int((bx1 - TILE_G[0]) // TILE_G[2]) + 1):
                    for tj in range(int((by0 - TILE_G[1]) // TILE_G[2]), int((by1 - TILE_G[1]) // TILE_G[2]) + 1):
                        s_ = BUILT_PICK.get((ti, tj)) or TOWN_PT_M
                        tx0, ty0 = TILE_G[0] + ti * TILE_G[2], TILE_G[1] + tj * TILE_G[2]
                        nn = int(round(TILE_G[2] / s_))
                        for a_ in range(nn):
                            for b_ in range(nn):
                                q = (tx0 + a_ * s_, ty0 + b_ * s_)
                                if not (bx0 < q[0] < bx1 and by0 < q[1] < by1):
                                    continue
                                if BUILT_PICK.get((ti, tj)) and s_ < g8 and GROUND_THIN:
                                    ix_, iy_ = int(round((q[0] - TILE_G[0]) / s_)), int(round((q[1] - TILE_G[1]) / s_))
                                    on8 = abs(ix_ * s_ / g8 - round(ix_ * s_ / g8)) < 1e-6 and \
                                        abs(iy_ * s_ / g8 - round(iy_ * s_ / g8)) < 1e-6
                                    if not on8 and (s_, ix_, iy_) not in BUILT_KEPT:
                                        continue           # a height the ground does not have either
                                if not pin_(q) or any(h[0] <= q[0] <= h[2] and h[1] <= q[1] <= h[3] and h[4](q) for h in hin_):
                                    continue
                                if near_e(q):
                                    continue
                                z_ = gz(q)
                                if z_ is not None:
                                    sub_.append({"coordinates": [dict(xy(q), z=round(z_ - low, 3))]})
                if sub_:
                    d_["sublines"] = sub_
                reg_d.append(d_)
                reg_k.append(kind)
                reg_r.append((kind, k))
        g_ = ac.create("CreateMeshes", "meshesData", reg_d, u"roads + parks: one mesh per outline") if reg_d else []
        bad_r = set()
        for g, d, kind, rk in zip(g_, reg_d, reg_k, reg_r):
            if g:
                made.append(g)
                data.append(d)
                kinds.append(kind)
                if kind == "road":
                    REG_G.append((g, [(q["x"] + ox, q["y"] + oy) for q in d["polygonCoordinates"]]))
                n_reg[0 if kind == "road" else 1] += 1
            else:
                bad_r.add(rk)
                n_reg[2] += 1
        # only the outlines Archicad refused go on in 50 m cells (below), with their holes
        keep_r = set(k for kd, k in bad_r if kd == "road")
        st = [R for k, R in enumerate(st) if k in keep_r or (hole[k] and keep_r)]
        hole = [h for k, h in enumerate(hole) if k in keep_r or (h and keep_r)]
        pk = [R for k, R in enumerate(pk) if ("park", k) in bad_r]
        log.append(u"roads + parks (v1.78): %d road outline(s) and %d park outline(s) as one Mesh each on the ground as "
                   u"built (%.2f m over it, edge points every %.1f m), town blocks as holes, no slab, no SEO%s" % (
                       n_reg[0], n_reg[1], TOWN_LIFT_M, TOWN_EDGE_M,
                       u"; FLAG %d outline(s) refused: built in %.0f m cells instead" % (n_reg[2], TOWN_CELL_M) if n_reg[2] else u""))
    data_r = len(data)                                    # v1.78: the outline meshes are made already
    cell_of = []                                          # v1.83: (cell size, i, j) of each cell mesh

    def dens2_(R):                                        # v1.83: long cell edges follow the ground
        out_ = []
        for a_, b_ in zip(R, R[1:] + R[:1]):
            n_ = max(1, int(math.ceil(math.hypot(b_[0] - a_[0], b_[1] - a_[1]) / TOWN_EDGE_M)))
            out_ += [(a_[0] + (b_[0] - a_[0]) * k_ / float(n_), a_[1] + (b_[1] - a_[1]) * k_ / float(n_)) for k_ in range(n_)]
        return out_

    def kept_(bx0, by0, bx1, by1):                        # v1.83: the built ground's kept heights in a box
        g8_ = GROUND_GRIDS[0]
        for ti in range(int((bx0 - TILE_G[0]) // TILE_G[2]), int((bx1 - TILE_G[0]) // TILE_G[2]) + 1):
            for tj in range(int((by0 - TILE_G[1]) // TILE_G[2]), int((by1 - TILE_G[1]) // TILE_G[2]) + 1):
                s_ = BUILT_PICK.get((ti, tj)) or TOWN_PT_M
                tx0, ty0 = TILE_G[0] + ti * TILE_G[2], TILE_G[1] + tj * TILE_G[2]
                nn = int(round(TILE_G[2] / s_))
                for a_ in range(nn):
                    for b_ in range(nn):
                        q = (tx0 + a_ * s_, ty0 + b_ * s_)
                        if not (bx0 < q[0] < bx1 and by0 < q[1] < by1):
                            continue
                        if BUILT_PICK.get((ti, tj)) and s_ < g8_ and GROUND_THIN:
                            ix_, iy_ = int(round((q[0] - TILE_G[0]) / s_)), int(round((q[1] - TILE_G[1]) / s_))
                            on8 = abs(ix_ * s_ / g8_ - round(ix_ * s_ / g8_)) < 1e-6 and \
                                abs(iy_ * s_ / g8_ - round(iy_ * s_ / g8_)) < 1e-6
                            if not on8 and (s_, ix_, iy_) not in BUILT_KEPT:
                                continue
                        yield q

    def cells_(c, only=None):                             # v1.83: the cell loop for one cell size
        nonlocal n_hole, n_cell
        nx = int(math.ceil((X1 - X0) / c))
        ny = int(math.ceil((Y1 - Y0) / c))
        for kind, rings, hl in (("road", st, hole), ("park", pk, [False] * len(pk))):
          BO = [_bands(R, X0, X1, c) for R in rings]
          for i in range(nx):
            for j in range(ny):
                if only is not None and (kind, i // 2, j // 2) not in only:
                    continue                           # v1.83: only the halves of a refused larger cell
                x, y = X0 + i * c, Y0 + j * c
                cc = (x + c / 2, y + c / 2)
                n_s = max(2, int(round(c / 25.0)))       # v1.83: test the large cells every 25 m for the working area
                if not any(inr((x + c * a_ / n_s, y + c * b_ / n_s)) for a_ in range(n_s + 1) for b_ in range(n_s + 1)):
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
                    if len(P) >= 3 and SITE_POLY:          # v1.83: roads end at the edge of the modelled ground
                        P = clean(_clip_convex(P, SITE_POLY)) if not hl[k] else (
                            P if all(_inpoly(q, SITE_POLY) for q in P) else [])
                    if len(P) >= 3 and abs(area(P)) > 0.05:
                        (hls if hl[k] else outs).append(P)
                for P in outs:
                    H_ = [h for h in hls if all(_inpoly(q, P) for q in h[::max(1, len(h) // 12)])]   # v1.83: wholly inside
                    if abs(area(P)) - sum(abs(area(h)) for h in H_) < 1.0:
                        continue                           # a cell all town block: nothing to pave
                    per_ = sum(math.hypot(b_[0] - a_[0], b_[1] - a_[1]) for a_, b_ in zip(P, P[1:] + P[:1]))
                    if per_ > 0 and (2.0 * abs(area(P)) / per_ < TOWN_SLIVER_M or abs(area(P)) < TOWN_MIN_M2):
                        N_SLIVER[0] += 1                   # v1.83 (Aras 19 Nov 09:08 "dont draw parts like this"):
                        continue                           # no thin flaps left over from cutting a piece at an edge
                    P = dens2_(P)                          # v1.83: a point every TOWN_EDGE_M along the cell's edge
                    gs = [z for z in [gz(q) for q in P + [cc]] if z is not None]
                    if not gs:
                        continue
                    low = min(gs) - TOWN_UNDER_M         # v1.44: a mesh body on the surveyed ground
                    ti_ = [(int((q[0] - TILE_G[0]) // TILE_G[2]), int((q[1] - TILE_G[1]) // TILE_G[2])) for q in P + [cc]]
                    lift_ = TOWN_LIFT_M                    # v1.78: heights from the built ground (no tile error)
                    zq = lambda q, gs=gs: (gz(q) if gz(q) is not None else min(gs))
                    d_ = dict(level=round(low - z0 + lift_, 3), skirtType=TOWN_SKIRT, skirtLevel=0.05,   # v1.83: a body
                              ridges="AllSmooth", polygonCoordinates=[dict(xy(q), z=round(zq(q) - low, 3)) for q in P],
                              _mat=kind)
                    sub_ = []
                    # v1.83: the inner heights are the built ground's own kept heights (was every 2.5 m), so the
                    # skin follows the drawn ground and the ground cannot poke through it
                    bx0_, by0_ = min(q[0] for q in P), min(q[1] for q in P)
                    bx1_, by1_ = max(q[0] for q in P), max(q[1] for q in P)
                    for q in kept_(bx0_, by0_, bx1_, by1_):
                        if _inpoly(q, P) and not any(_inpoly(q, h) for h in H_):
                            z_ = gz(q)
                            if z_ is not None:
                                sub_.append({"coordinates": [dict(xy(q), z=round(z_ - low, 3))]})
                    if sub_:
                        d_["sublines"] = sub_
                    if H_:
                        d_["holes"] = [{"polygonCoordinates": [dict(xy(q), z=round(zq(q) - low, 3)) for q in h]} for h in H_]
                        n_hole += len(H_)
                    data.append(d_)
                    cen.append((sum(q[0] for q in P) / len(P), sum(q[1] for q in P) / len(P)))
                    kinds.append(kind)
                    zz_ = [v["z"] for v in d_["polygonCoordinates"]] + [v["coordinates"][0]["z"] for v in sub_]
                    cell_of.append((c, i, j, max(zz_) - min(zz_) > TOWN_RELIEF_MAX_M and c / 2.0 >= TOWN_CELL_MIN_M - 1e-6))
                    n_cell += 1
    cells_(TOWN_CELL_M)
    road_g = list(REG_G)                                  # v1.78: the outline meshes
    if data[data_r:] and "CreateMeshes" not in miss:    # v1.56: Mesh-tool skins ON the ground (no body, no cut)
        c = TOWN_CELL_M
        def mk_(lo, what_):                               # v1.83: a too-steep piece is not sent but quartered
            ix_ = [k for k in range(lo, len(data)) if not cell_of[k - data_r][3]]
            r_ = ac.create("CreateMeshes", "meshesData", [data[k] for k in ix_], what_) if ix_ else []
            out_ = [None] * (len(data) - lo)
            for k, g in zip(ix_, r_):
                out_[k - lo] = g
            return out_
        g_ = mk_(data_r, u"town ground: roads + parks as bodies on the ground (%.0f m cells)" % c)
        # v1.83 (Aras 19 Nov 09:02 "make the road parking surfaces larger where you can without comprimising quality"):
        # 200 m cells; a cell Archicad refuses, or whose body would be deeper than TOWN_RELIEF_MAX_M on a slope, is made
        # again as its four quarters (100, 50, 25 m), so no road goes missing and no body is metres deep in a section
        g_ = list(g_)
        while TOWN_CELL_SPLIT and c / 2.0 >= TOWN_CELL_MIN_M - 1e-6 and not all(g_):
            only = set((kinds[data_r + k], cell_of[k][1], cell_of[k][2]) for k, g in enumerate(g_) if not g)
            keep_ = [k for k, g in enumerate(g_) if g]
            data[data_r:] = [data[data_r + k] for k in keep_]
            kinds[data_r:] = [kinds[data_r + k] for k in keep_]
            cell_of[:] = [cell_of[k] for k in keep_]
            g_ = [g_[k] for k in keep_]
            n0, c = len(data), c / 2.0
            cells_(c, only)
            g_ += mk_(n0, u"town ground: refused or steep cells as %.0f m quarters" % c)
        log.append(u"town ground (v1.83): road + park cells as large as Archicad takes them: " + u", ".join(
            u"%.0f m x %d" % (cz, sum(1 for o, g in zip(cell_of, g_) if g and o[0] == cz))
            for cz in sorted(set(o[0] for o in cell_of), reverse=True)) + u"; %d refused at %.0f m; %d thin flaps left out" % (
            sum(1 for g in g_ if not g), c, N_SLIVER[0]))
        made += [g for g in g_ if g]
        road_g += [(g, [(q["x"] + ox, q["y"] + oy) for q in d["polygonCoordinates"]]) for g, d, k in
                   zip(g_, data[data_r:], kinds[data_r:]) if g and k == "road"]
        log.append(u"town ground: %d road cells (%d town blocks cut out as holes), %d park cells: Mesh bodies, top = the "
                   u"ground's own heights (not every %.1f m since v1.83), as bodies %.2f m over it reaching down under their lowest "
                   u"point (v1.83; steep pieces quartered so no body is metres deep)" % (
                       sum(1 for k in kinds[data_r:] if k == "road"), n_hole, sum(1 for k in kinds[data_r:] if k == "park"), TOWN_PT_M,
                       TOWN_LIFT_M))
    # ---- kerbs and walls (survey lines) as Walls on the ground, in pieces of at most LINE_SEG_M
    L = M.get("lines") or {}
    LN = M.get("lines_net") or {}
    walls, n_by = [], {}
    n_kc, ends_ = [0], {}                                 # v1.76

    def snap_(q):                                         # v1.76: one point for line ends within SNAP_M
        i, j = int(q[0] // 2), int(q[1] // 2)
        for a in range(i - 1, i + 2):
            for b in range(j - 1, j + 2):
                for e in ends_.get((a, b), []):
                    if math.hypot(q[0] - e[0], q[1] - e[1]) < SNAP_M:
                        return e
        ends_.setdefault((i, j), []).append(q)
        return q
    BK_ = [(a, b) for L_ in (SEL.get("istinaat") or []) for a, b in zip(L_, L_[1:])]
    SG_ = {}                                              # v1.77: every kerb / wall segment (2 m grid) for T-junctions
    LN_ = []
    for src_ in (LN.get("kerbs") or L.get("kerbs") or [], L.get("walls") or [], L.get("heritage_walls") or []):
        for pl in src_:
            P = pl[1] if (len(pl) == 2 and isinstance(pl[0], bool)) else pl
            P = _straighten([tuple(q[:2]) for q in P if isinstance(q, (list, tuple)) and len(q) >= 2], False)
            li_ = len(LN_)
            LN_.append(P)
            for a, b in zip(P, P[1:]):
                for i in range(int(min(a[0], b[0]) // 2) - 1, int(max(a[0], b[0]) // 2) + 2):
                    for j in range(int(min(a[1], b[1]) // 2) - 1, int(max(a[1], b[1]) // 2) + 2):
                        SG_.setdefault((i, j), []).append((li_, a, b))
    n_t = [0]

    def tee_(q, li_):                                     # v1.77: an end onto the nearest other line within SNAP_M
        best = None
        for lj, a, b in SG_.get((int(q[0] // 2), int(q[1] // 2)), []):
            if lj == li_:
                continue
            d_ = _seg_d(q, a, b)
            if d_ < SNAP_M and (best is None or d_ < best[0]):
                best = (d_, a, b)
        if best is None or best[0] < 1e-6:
            return q
        _d, a, b = best
        dx_, dy_ = b[0] - a[0], b[1] - a[1]
        f_ = max(0.0, min(1.0, ((q[0] - a[0]) * dx_ + (q[1] - a[1]) * dy_) / (dx_ * dx_ + dy_ * dy_ or 1e-12)))
        n_t[0] += 1
        return (a[0] + f_ * dx_, a[1] + f_ * dy_)
    li_run = [0]

    def on_bank_(p0, p1):                                 # v1.76: a kerb lying on a bank wall line
        m = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
        return any(_seg_d(m, a, b) < 0.4 and _seg_d(p0, a, b) < 0.6 and _seg_d(p1, a, b) < 0.6 for a, b in BK_)
    for key, src, h, t, mat in (("kerbs", LN.get("kerbs") or L.get("kerbs") or [], KERB_H, KERB_T, "bridge_stone"),
                                ("walls", L.get("walls") or [], WALL_H, WALL_T, "bridge_stone"),
                                ("heritage_walls", L.get("heritage_walls") or [], HWALL_H, HWALL_T, "heritage_red")):
        for pl in src:
            P = pl[1] if (len(pl) == 2 and isinstance(pl[0], bool)) else pl
            P = [tuple(q[:2]) for q in P if isinstance(q, (list, tuple)) and len(q) >= 2]
            P = _straighten(P, False)                     # v1.70: straight runs as one piece
            if key == "kerbs" and not KERB_WALLS:         # v1.88: counted for the line numbers, not built
                li_run[0] += 1
                continue
            li_ = li_run[0]                               # v1.77: this line's number (same order as LN_)
            li_run[0] += 1
            if len(P) >= 2:                               # v1.76: ends meet the other lines' ends; v1.77: or their line
                for e_ in (0, -1):
                    q0_ = P[e_]
                    q1_ = snap_(q0_)
                    P[e_] = tee_(q0_, li_) if q1_ is q0_ else q1_
            for a, b in zip(P, P[1:]):
                Ls = math.hypot(b[0] - a[0], b[1] - a[1])
                if Ls < 0.3:
                    continue
                k_n = max(1, int(math.ceil(Ls / LINE_SEG_M)))
                za_, zb_ = gz(a), gz(b)
                if za_ is not None and zb_ is not None:   # v1.56: on a slope shorter pieces (each a flat-topped wall
                    k_n = max(k_n, min(int(Ls // LINE_MIN_M) or 1,   # stood above the ground by its own rise:
                                       int(math.ceil(abs(zb_ - za_) / LINE_STEP_M.get(key, LINE_RISE_M)))))   # v1.88: stepped
                for k_ in range(k_n):
                    p0 = (a[0] + (b[0] - a[0]) * k_ / k_n, a[1] + (b[1] - a[1]) * k_ / k_n)
                    p1 = (a[0] + (b[0] - a[0]) * (k_ + 1) / k_n, a[1] + (b[1] - a[1]) * (k_ + 1) / k_n)
                    m_ = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
                    if not inr(m_):
                        continue
                    if _in_bld(m_) or on_bank_(p0, p1):     # v1.76: not through a house, not on a bank wall
                        n_kc[0] += 1
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
        KERB_OPS.extend((g, [w_["begCoordinate"], w_["endCoordinate"]]) for g, w_ in zip(gk_, walls) if g)   # v1.61
        log.append(u"SEO (v1.61): %d kerb / wall pieces cut the section view grounds only (the 3D tiles are left whole)"
                   % sum(1 for g in gk_ if g))
        # v1.32: kerbs and survey walls do not cut the ground (thousands of tiny operations stalled the publish)
    log.append(u"collisions (v1.76): %d kerb / wall piece(s) left out (through a house or on a bank wall line); line ends "
               u"within %.2f m joined; %d T-junction end(s) moved onto the other line (v1.77)" % (n_kc[0], SNAP_M, n_t[0]))
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
        lo_ = min(zs) + KERB_H - PAV_T_M                   # v1.45: a Mesh skin, kerb height over the ground
        zc_ = [((gz(q) if gz(q) is not None else min(zs)) + KERB_H) for q in P_]
        pav.append(dict(level=round(lo_ - z0, 3), skirtType=TOWN_SKIRT, skirtLevel=0.02, ridges="AllSmooth",   # v1.56
                        polygonCoordinates=[dict(xy(q), z=round(z_ - lo_, 3)) for q, z_ in zip(P_, zc_)], _mat="pavement"))
    if pav and "CreateMeshes" not in miss:
        gp_ = ac.create("CreateMeshes", "meshesData", pav, u"pavements (Mesh skins sewn to the roads at the kerb)")
        made += [g for g in gp_ if g]
        rb_ = [] if PAV_SKIN else [(g, R_, (min(q[0] for q in R_), min(q[1] for q in R_), max(q[0] for q in R_), max(q[1] for q in R_)))
               for g, R_ in road_g]
        for g, d in zip(gp_, pav):
            if not g:
                continue
            cq = (sum(q["x"] for q in d["polygonCoordinates"]) / 4.0 + ox, sum(q["y"] for q in d["polygonCoordinates"]) / 4.0 + oy)
            for rg_, R_, bx_ in rb_:
                if bx_[0] <= cq[0] <= bx_[2] and bx_[1] <= cq[1] <= bx_[3] and _inpoly(cq, R_):
                    EXTRA_LINKS.append(dict(targetId={"guid": rg_}, operatorId={"guid": g}, operation="Subtraction"))
                    OP_PTS[g] = [(q["x"] + ox, q["y"] + oy) for q in d["polygonCoordinates"]]   # v1.66
        log.append(u"pavements: %d strips from the survey kerbs to the nearest building face (at most %.1f m, ASSUMED), "
                   u"top = kerb top (%.2f m), %.2f m build-up (ASSUMED; v1.56: drawn as a skin, no body, no ground cut); %d kerb "
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
    n_hist_dk = 0                                          # v1.69
    zs_known = []
    n_cov = 0
    for nm, R, H in pieces:
        if COVER_ON[0] and nm in COVER_LAYERS:             # v1.88: built as a ground cover (build_covers)
            n_cov += 1
            continue
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
        if nm == "kopruler" and any(math.hypot(c[0] - hp[0], c[1] - hp[1]) < 30.0 for _hn, hp, _hk, _hw in HIST_BRIDGES):
            n_hist_dk += 1                                 # v1.69: the historic bridge is built with its own deck
            continue
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
    gs_ = [None] * len(data)                               # v1.46: sure pieces in one call, each unsure layer its own
    for lab_ in [None] + sorted(set(kp[0] for kp in keep if kp and kp[0] in MP_UNSURE)):
        ix_ = [i for i, kp in enumerate(keep) if (kp[0] if kp and kp[0] in MP_UNSURE else None) == lab_]
        if not ix_:
            continue
        r_ = ac.create("CreateSlabs", "slabsData", [data[i] for i in ix_],
                       u"masterplan pieces (his outlines)" if lab_ is None else
                       u"masterplan unsure %s: best guess %s" % (lab_, MP_UNSURE[lab_]))
        for i, g_ in zip(ix_, r_):
            gs_[i] = g_
    n_uns = dict((k_, sum(1 for kp, g_ in zip(keep, gs_) if g_ and kp and kp[0] == k_)) for k_ in MP_UNSURE)
    log.append(u"masterplan unsure layers (v1.46, each on its own \"BGA ? unsure\" layer, best guess built): %s" % (
        u"; ".join(u"%s %d (%s)" % (k_, n_, MP_UNSURE[k_]) for k_, n_ in sorted(n_uns.items())) or u"none"))
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
    if n_cov:
        log.append(u"masterplan (v1.88): %d surface piece(s) built as ground covers, not as flat slabs" % n_cov)
    if n_hist_dk:                                          # v1.69
        log.append(u"masterplan: %d bridge outline(s) over a historic bridge not built as a second deck (the arches carry "
                   u"their own)" % n_hist_dk)
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
def _heal(ac, log, when):
    """v1.78 (Aras 19 Nov 07:20 "many of the houses are not closed off", 07:26 "Many of those houses misses walls and
    etc."; v1.77 kept 1551 roofs but only 588 roofs were in the model after the pass): every element this pass made or
    kept is looked up in the model; any that is gone is made again (windows / doors on a remade wall follow it)"""
    live = set()
    for ty in CLEAR_TYPES:
        try:
            for e in ac.api("API.GetElementsByType", {"elementType": ty}).get("elements", []):
                if e.get("elementId"):
                    live.add(e["elementId"]["guid"])
        except Exception as ex:
            log.append(u"FLAG check %s: %s not listed (%s): vanished elements not looked for" % (when, ty, ex))
            return
    gone = [g for g in SRC_OF if g not in live]
    if not gone:
        log.append(u"check %s: all %d element(s) of this pass are in the model" % (when, len(SRC_OF)))
        return
    by_ty = {}
    for g in gone:
        by_ty[TYPE_OF.get(SRC_OF[g][0], u"?")] = by_ty.get(TYPE_OF.get(SRC_OF[g][0], u"?"), 0) + 1
    remap, n_new = {}, 0
    order = sorted(gone, key=lambda g: 1 if SRC_OF[g][0] in ("CreateWindows", "CreateDoors") else 0)
    groups = []
    for g in order:                                   # walls etc. first, then the windows / doors on them
        nm, key, it, what = SRC_OF[g]
        if groups and groups[-1][0] == (nm, key, what):
            groups[-1][1].append(g)
        else:
            groups.append(((nm, key, what), [g]))
    for (nm, key, what), gs in groups:
        its = []
        for g in gs:
            t_ = json.dumps(SRC_OF[g][2], default=str)
            for o_, n_ in remap.items():
                t_ = t_.replace(o_, n_)
            its.append(json.loads(t_))
        new = ac._create(nm, key, its, what + u" (made again: vanished)")
        for g, it, g2 in zip(gs, its, new):
            SRC_OF.pop(g, None)
            if not g2:
                continue
            remap[g] = g2
            n_new += 1
            NEW_G.add(g2)
            SRC_OF[g2] = (nm, key, it, what)
            PART_G[g2] = PART_G.get(g, part_of(what))
    for it in ITEMS:
        if it[1] in remap:
            it[1] = remap[it[1]]
    for k_, v_ in BGRP.items():
        BGRP[k_] = [remap.get(g, g) for g in v_]
    log.append(u"FLAG check %s: %d element(s) of this pass were gone from the model (%s), %d made again" % (
        when, len(gone), u", ".join(u"%s %d" % kv for kv in sorted(by_ty.items())), n_new))
    return remap


def main():
    t0 = time.time()
    SEO_OPS[:], SEO_TERR[:], CANOPY_REC[:], EXTRA_OPS[:], KERB_OPS[:] = [], [], [], [], []   # v1.27: fresh per run (a re-run in the same Rhino kept old ones)
    KEEP.clear(); ITEMS[:] = []; NEW_G.clear(); SRC_OF.clear(); BUILT_PICK.clear(); BUILT_KEPT.clear(); BUILT_ZG[0] = None; N_KEPT[0] = 0; FOUND_OWN[0] = -1
    LOCKED_BB[:] = []; EXTRA_LINKS[:] = []; TREE_OBJ[:] = []; N_NOTREE[0] = 0; PART_G.clear(); OWN_PART.clear(); BGRP.clear(); N_LOCKSKIP[0] = 0; N_TINONLY[0] = 0; N_RAFT[:] = [0, 0.0]; LINK_T.clear(); PID[0] = None             # v1.44          # v1.34: fresh per run
    log = []
    ac = AC(log)
    try:
        ver = ac.t("GetAddOnVersion").get("version", "?")
    except Exception as ex:
        raise RuntimeError(u"Archicad answers but Tapir does not (%s): install / load the Tapir add-on" % ex)
    log.insert(0, u"TAPIR OK %s (%s)" % (ver, ac.url))
    _set_scope(ac, log)                                   # v1.52: site file or buildings file (by the project name)
    try:                                                  # v1.86 (Aras 09:20 "run intersact command for every
        if ac.has("SetAutoIntersect"):                    # intersection"): Archicad's Auto-Intersection on, so walls,
            ac.t("SetAutoIntersect", {"isOn": True})      # beams and slabs that meet are joined as they are made
            log.append(u"Auto-Intersection (v1.86): on (Tapir has no command to run Intersect on chosen elements)")
        else:
            log.append(u"FLAG Tapir has no SetAutoIntersect: turn on Design > Auto-Intersection by hand")
    except Exception as ex:
        if _ac_gone(ex):
            raise
        log.append(u"FLAG Auto-Intersection not set (%s)" % ex)
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
    SITE_POLY[:] = [tuple(p[:2]) for p in (M.get("frame") or [])]          # v1.45: site_alan (MapBase frame)
    PARTS.clear()
    if os.path.isfile(PARTS_FILE):                        # v1.45: rebuild switch
        with open(PARTS_FILE, encoding="utf-8") as f_:
            PARTS.update(l_.strip() for l_ in f_ if l_.strip() and not l_.startswith("#"))
    if SCOPE[0] == "buildings":                           # v1.52: the buildings file holds only our buildings
        PARTS.clear()
        PARTS.add("buildings")
    elif SCOPE[0] == "site" and not SITE_BUILDINGS:
        PARTS.discard("buildings")
    log.append(u"site_alan: %s; parts rebuilt: %s" % (
        u" ".join(u"(%.1f, %.1f)" % q for q in SITE_POLY) or u"FLAG not in MapBase: whole survey",
        u", ".join(sorted(PARTS)) if PARTS else u"all"))
    mpb = glob.glob(os.path.join(BERGAMA_ROOT, "cached", "bergama_masterplanbase*", "*.json"))
    log.append(u"MasterplanBase: %s (proposals come in AcBuild v2)" % (mpb[0] if mpb else u"not written yet"))
    cuts = [(c["name"], tuple(c["A"]), tuple(c["B"])) for c in S["cuts"]]
    if not cuts:
        raise RuntimeError(u"sections.json holds no cut: press Sections first")
    ox = round(sum(p[0] for _, a, b in cuts for p in (a, b)) / (2 * len(cuts)), -2)
    oy = round(sum(p[1] for _, a, b in cuts for p in (a, b)) / (2 * len(cuts)), -2)
    _pj = os.path.join(CACHE_DIR, "acbuild.json")
    _sj = os.path.join(BERGAMA_ROOT, "cached", OUT_FOLDER, "acbuild.json")   # v1.52: the site file's record
    if not os.path.isfile(_pj) and SCOPE[0] == "buildings" and os.path.isfile(_sj):
        _pj = _sj                           # v1.52: the buildings file takes the site file's origin (hotlink at 0,0)
    if not os.path.isfile(_pj) and os.path.isfile(OLD_CACHE):
        _pj = OLD_CACHE                     # v1.42: the same origin as the sections project
    if os.path.isfile(_pj):                 # v1.4: one origin for the life of the Archicad project
        with open(_pj, encoding="utf-8") as f:
            _o = json.load(f).get("origin")
        if _o:
            ox, oy = float(_o[0]), float(_o[1])
    log.append(u"Archicad origin = survey (%.0f, %.0f); heights absolute (m above sea level)" % (ox, oy))
    xy = lambda p: {"x": round(p[0] - ox, 3), "y": round(p[1] - oy, 3)}
    ORIGIN[:] = [ox, oy]                                  # v1.83: for the site_alan rule in every create

    # ---- rectangles, survey, buildings
    rects = []
    for name, A, B in cuts:
        Ln, u, n = frame(A, B)
        rects.append((name, A, B, Ln, u, n))
    SEC_R[:] = [(r_[1], r_[2]) for r_ in rects]          # v1.66
    OP_PTS.clear()
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
            survey["_sym"] = SYM_READ[0] or {}
        cp_ = [p for nm_ in L_["SURVEY_LAYERS"] if nm_.startswith("EGRI") for pl in survey.get(nm_, []) for p in pl
               if p[2] > 1.0]
        box = (min(p[0] for p in cp_), min(p[1] for p in cp_), max(p[0] for p in cp_), max(p[1] for p in cp_))
        SITE_BOX[:] = list(box)
        if SITE_POLY:                                     # v1.45: only site_alan (+30 m of survey around it)
            box = (min(q[0] for q in SITE_POLY) - 30.0, min(q[1] for q in SITE_POLY) - 30.0,
                   max(q[0] for q in SITE_POLY) + 30.0, max(q[1] for q in SITE_POLY) + 30.0)
            SITE_BOX[:] = [box[0] + 30.0, box[1] + 30.0, box[2] - 30.0, box[3] - 30.0]
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
        if SITE_POLY:                                     # v1.45: site_alan only
            return _inpoly(p, SITE_POLY)
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
        ring = _straighten(clean(ring), True)            # v1.70: one wall per straight side
        if len(ring) < 3 or abs(area(ring)) < 4.0 or not any(inside(q, r) for q in ring for r in rects):
            continue
        if HOUSE_ALL_IN and SITE_POLY and not all(_inpoly(q, SITE_POLY) for q in ring):
            rc_ = clean(_clip_convex(ring, SITE_POLY))   # v1.83 (Aras 09:12 "+%90 ... draw it with the cutted plane")
            if len(rc_) < 3 or abs(area(rc_)) < SITE_SHARE_MIN * abs(area(ring)):
                N_OFFGROUND[0] += 1               # under 90 % in site_alan: not built
                continue
            ring = rc_                            # cut at the site_alan edge
        if HOUSE_ALL_IN and any(tin.z(q[0] - ox, q[1] - oy) is None for q in ring):
            N_OFFGROUND[0] += 1                   # v1.83: off the surveyed ground: not built
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
            if f > 0.0:                                  # v1.76: no overlap left: corners inside go onto its wall line
                n_touch += 1
                Rj = bld[j]["ring"]
                Rn = []
                for q in A_["ring"]:
                    if _inpoly(q, Rj):
                        e_ = min(zip(Rj, Rj[1:] + Rj[:1]), key=lambda ab: _seg_d(q, ab[0], ab[1]))
                        dx_, dy_ = e_[1][0] - e_[0][0], e_[1][1] - e_[0][1]
                        L2_ = dx_ * dx_ + dy_ * dy_ or 1e-12
                        f_ = max(0.0, min(1.0, ((q[0] - e_[0][0]) * dx_ + (q[1] - e_[0][1]) * dy_) / L2_))
                        q = (e_[0][0] + f_ * dx_, e_[0][1] + f_ * dy_)
                        BLD_SNAP[0] += 1
                    Rn.append(q)
                Rn = _tidy_ring(Rn)
                if len(Rn) >= 3 and abs(area(Rn)) > 4.0 and not _selfx(Rn):   # v1.78: never a crossed outline
                    A_["ring"] = Rn if area(Rn) > 0 else Rn[::-1]
                else:
                    BLD_XSKIP[0] += 1
        if i not in drop_:
            keep_.append(i)
    if drop_:
        bld = [b for i, b in enumerate(bld) if i not in drop_]
    n_x_ = 0
    for b in bld:                                         # v1.78: no short edge, spike or crossing left in an outline
        b["ring"] = _tidy_ring(b["ring"])
        n_x_ += 1 if _selfx(b["ring"]) else 0
    log.append(u"house outlines (v1.78): edges under %.2f m and spikes merged into their neighbours (a skipped short "
               u"edge left a gap in the walls), %d corner move(s) not made because the outline would cross itself%s" % (
                   RING_MIN_M, BLD_XSKIP[0], u"; FLAG %d outline(s) still cross themselves (Archicad may refuse their "
                   u"roof / slabs)" % n_x_ if n_x_ else u""))
    _bld_set([b["ring"] for b in bld])                   # v1.76: for the clash checks
    log.append(u"collisions (v1.76): %d house corner(s) inside a neighbouring house moved onto its wall line" % BLD_SNAP[0])
    log.append(u"collisions: %d survey building(s) overlapping the Kızıl Avlu hall by more than %.0f%% left out (the hall "
               u"stays), %d duplicate footprint(s) (more than %.0f%% inside a bigger one) left out, %d small overlap(s) "
               u"kept" % (n_hall, COL_HALL_F * 100, n_dup, COL_DUP_F * 100, n_touch))
    log.append(u"floor counts: %d buildings take the survey's floor label (YAZI_KAT_ADEDI) standing in them (%d differ "
               u"from MapBase); storeys %.1f m (civic %.1f, sacred %.1f, industry %.1f: the project rule)" % (
                   n_lab, n_labdiff, STOREY_M, STOREY["civic"], STOREY["sacred"], STOREY["industry"]))
    log.append(u"buildings in the cut rectangles: %d (%d cut by a line); %d without a floor count built as 1 floor (ASSUMED)" % (
        len(bld), sum(1 for b in bld if b["cut"]), skipped))
    log.append(u"houses under 90 %% inside site_alan or off the surveyed ground (v1.83, left out; 90 %%+ cut at the edge): %d" % N_OFFGROUND[0])

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
        if SECTION_BANDS:                                  # v1.58: one hidden ground layer per site section
            for nm_, _a, _b in cuts:
                LAYER_NAME["view_" + nm_] = u"BGA Ground view " + nm_
        setup_layers(ac, log)                              # v1.45: a layer per part + combinations
        setup_library(ac, log)                             # v1.45: GDL trees + street furniture
        setup_cut_house_override(ac, log)                  # v1.56: needs the BGA layers
    old_items = [it for it in (old.get("items") or []) if isinstance(it, list) and len(it) == 3]
    gtype, n_stray = {}, 0                                # v1.34: guid -> type of every element in the model

    def del_typed(gs, what):
        """v1.34: delete these guids, windows and doors before walls (CLEAR_TYPES order); v1.82: with Archicad's Suspend
        Groups on (v1.78 lost 3953 kept walls, 1666 windows and 26 doors when old house-group members were deleted), put
        back as it was afterwards; the groups themselves stay"""
        sg_ = None
        if gs and ac.has("SetSuspendGroupsMode"):
            try:
                sg_ = ac.t("GetSuspendGroupsMode").get("suspendGroups") if ac.has("GetSuspendGroupsMode") else None
                ac.t("SetSuspendGroupsMode", {"suspendGroups": True})
            except Exception as ex:
                log.append(u"FLAG Suspend Groups not switched on before deleting (%s)" % ex)
        try:
            return del_typed_(gs, what)
        finally:
            if gs and ac.has("SetSuspendGroupsMode") and sg_ is not True:
                try:
                    ac.t("SetSuspendGroupsMode", {"suspendGroups": bool(sg_)})
                except Exception:
                    pass

    def del_typed_(gs, what):
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
                own = dict((g, (h[:16], None, None)) for g, h in ad_)
                log.append(u"model: %d element(s) recorded by this PC's last pass given their BGA- Element ID (%d "
                           u"written)" % (len(ad_), n_ad))
            if os.path.isfile(CLEANUP_FILE):              # v1.45: one time, on Aras's word (a stopped pass's leftovers)
                stray_ = [g for g in gtype if g not in own]
                log.append(u"cleanup (one time, %s): %d element(s) without a BGA Element ID deleted (leftovers of the "
                           u"stopped v1.44 pass)" % (CLEANUP_FILE, del_typed(stray_, u"unlabelled leftovers")))
                for g in stray_:
                    gtype.pop(g, None)
                try:
                    os.remove(CLEANUP_FILE)
                except Exception:
                    pass
            bbs_ = read_bb(ac, [g for g, pr in own.items() if pr[1]]) if own else {}
            n_ed = 0
            for g, (h16, bb0, pr0) in own.items():
                OWN_PART[g] = pr0                         # v1.45
                if PARTS and pr0 and pr0 not in PARTS:    # v1.45: a part not rebuilt: kept as it is
                    continue
                bb1 = bbs_.get(g)
                tol_ = EDIT_TOL_WALL_M if gtype.get(g) == "Wall" else EDIT_TOL_M   # v1.79
                if bb0 and bb1 and max(abs(a_ - b_) for a_, b_ in zip(bb0, bb1)) > tol_:
                    LOCKED_BB.append((gtype[g], (bb1[0], bb1[1], bb1[3], bb1[4])))
                    n_ed += 1
                    continue
                KEEP.setdefault(h16, []).append(g)
            FOUND_OWN[0] = len(own) - n_ed                # v1.56: 0 = a fresh project
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
        try:                                              # v1.88: the ground covers, planned before the ground
            cover_plan(log, tin, ox, oy, SP, bld, survey)
        except Exception as ex:
            import traceback
            del COVER_PIECES[:]
            COVER_IDX[:] = [None, None]
            COVER_TILE_PTS.clear()
            COVER_ON[0] = False
            log.append(u"FLAG ground covers not planned (%s: %s) %s: roads, parks and his areas as in v1.87" % (
                type(ex).__name__, ex, traceback.format_exc()[-400:]))
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
        T0_ = SITE_TILE_M if WHOLE_SITE else GROUND_TILE_M
        pts_ix = {}                                       # v1.45: every survey height per tile (the accuracy check)
        for p in pts:
            pts_ix.setdefault((int((p[0] - gb[0]) // T0_), int((p[1] - gb[1]) // T0_)), []).append(p)
        ZG = {}                                           # v1.45: TIN heights on the global grids

        def zg(s_, ix_, iy_):
            k_ = (s_, ix_, iy_)
            if k_ not in ZG:
                ZG[k_] = tin.z(gb[0] + ix_ * s_ - ox, gb[1] + iy_ * s_ - oy)
            return ZG[k_]
        ACC = []                                          # v1.45: (grid, max deviation, tolerance) per tile
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
        TILE_SUBS = {}                                    # v1.58: (i, j) -> the tile's control heights (for the view meshes)
        THIN = [0, 0]                                     # v1.54: grid heights dropped, grid heights looked at

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
                Pc = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
                if SITE_POLY:                             # v1.45: the tile clipped to site_alan
                    Pc = clean(_clip_convex(Pc, SITE_POLY)) if any(_inpoly(q, SITE_POLY) for q in smp) or any(
                        x0 <= q[0] <= x1 and y0 <= q[1] <= y1 for q in SITE_POLY) else []
                    if len(Pc) < 3 or abs(area(Pc)) < 1.0:
                        continue
                poly = []
                for (ax, ay), (bx_, by_) in zip(Pc, Pc[1:] + Pc[:1]):
                    L_ = math.hypot(bx_ - ax, by_ - ay)
                    k_n = max(1, int(round(L_ / GROUND_EDGE_M)))
                    ts_ = [k_ / float(k_n) for k_ in range(k_n)]   # the same edge points as the neighbouring tile
                    if COVER_ON[0]:                       # v1.88: + where a cover outline crosses the edge
                        ts_ = sorted(set(ts_ + cover_edge_ts((ax, ay), (bx_, by_))))
                        ts_ = [t_ for k_, t_ in enumerate(ts_) if k_ == 0 or (t_ - ts_[k_ - 1]) * L_ > 0.002]
                    cs_ = [(ax + (bx_ - ax) * t_, ay + (by_ - ay) * t_) for t_ in ts_]
                    for c, zc_ in zip(cs_, cover_z_many(cs_, [zat(c) for c in cs_])):   # v1.88: lowered under covers
                        poly.append(dict(xy(c), z=zr(zc_)))
                if ADAPTIVE_GROUND:                       # v1.45: the coarsest grid within +-2 % of the tile's relief
                    tp_ = [p for p in pts_ix.get((i, j), []) if _inpoly(p, Pc)]
                    zs_ = [p[2] for p in tp_]
                    tol = max(GROUND_TOL_MIN, GROUND_TOL_F * (max(zs_) - min(zs_))) if zs_ else GROUND_TOL_MIN
                    pick, err_ = GROUND_GRIDS[-1], None
                    for s_ in GROUND_GRIDS:
                        e_ = 0.0
                        for p in tp_:
                            fx, fy = (p[0] - gb[0]) / s_, (p[1] - gb[1]) / s_
                            ix_, iy_ = int(fx), int(fy)
                            zc = [zg(s_, ix_, iy_), zg(s_, ix_ + 1, iy_), zg(s_, ix_, iy_ + 1), zg(s_, ix_ + 1, iy_ + 1)]
                            if any(v is None for v in zc):
                                continue
                            u_, v_ = fx - ix_, fy - iy_
                            zb_ = (zc[0] * (1 - u_) * (1 - v_) + zc[1] * u_ * (1 - v_) + zc[2] * (1 - u_) * v_ +
                                   zc[3] * u_ * v_)
                            e_ = max(e_, abs(zb_ - p[2]))
                            if e_ > tol:
                                break
                        pick, err_ = s_, e_
                        if e_ <= tol:
                            break
                    ACC.append((pick, err_ or 0.0, tol))
                    TILE_ERR[(i, j)] = max(TILE_ERR.get((i, j), 0.0), err_ or 0.0)   # v1.69
                    TILE_G[:] = [gb[0], gb[1], T]
                    BUILT_PICK[(i, j)] = pick                 # v1.78: the grid this tile was built from
                    BUILT_ZG[0] = zg
                    sub, cq_, cz_ = [], [], []
                    for ix_ in range(int((x0 - gb[0]) // pick) - 1, int((x1 - gb[0]) // pick) + 2):
                        for iy_ in range(int((y0 - gb[1]) // pick) - 1, int((y1 - gb[1]) // pick) + 2):
                            q = (gb[0] + ix_ * pick, gb[1] + iy_ * pick)
                            if not (x0 < q[0] < x1 and y0 < q[1] < y1) or not _inpoly(q, Pc):
                                continue
                            if min(_seg_d(q, a_, b_) for a_, b_ in zip(Pc, Pc[1:] + Pc[:1])) < 0.3:
                                continue
                            z_ = zg(pick, ix_, iy_)
                            if z_ is None:
                                continue
                            g8 = GROUND_GRIDS[0]
                            if GROUND_THIN and pick < g8:         # v1.54 (Desktop 3D crashed on 801,543 heights)
                                THIN[1] += 1
                                fx8, fy8 = ix_ * pick / g8, iy_ * pick / g8
                                if abs(fx8 - round(fx8)) > 1e-6 or abs(fy8 - round(fy8)) > 1e-6:   # not an 8 m node
                                    jx, jy = int(math.floor(fx8)), int(math.floor(fy8))
                                    zc8 = [zg(g8, jx, jy), zg(g8, jx + 1, jy), zg(g8, jx, jy + 1), zg(g8, jx + 1, jy + 1)]
                                    if all(v is not None for v in zc8):
                                        u8, v8 = fx8 - jx, fy8 - jy
                                        zb8 = (zc8[0] * (1 - u8) * (1 - v8) + zc8[1] * u8 * (1 - v8) +
                                               zc8[2] * (1 - u8) * v8 + zc8[3] * u8 * v8)
                                        if abs(zb8 - z_) <= tol:  # the 8 m grid gives it within the tile tolerance
                                            THIN[0] += 1
                                            continue
                            cq_.append(q)
                            cz_.append(z_)
                            BUILT_KEPT.add((pick, ix_, iy_))       # v1.78
                    sub = [{"coordinates": [dict(xy(q), z=zr(z_))]} for q, z_ in zip(cq_, cover_z_many(cq_, cz_))]
                    if COVER_ON[0]:                       # v1.88: the heights that pin the cover outlines
                        sub += [{"coordinates": [dict(xy((x_, y_)), z=zr(z_))]} for x_, y_, z_ in
                                cover_tile_pts(Pc, x0, y0, x1, y1)]
                    m = dict(level=round(base, 3), polygonCoordinates=poly, sublines=sub or [{"coordinates": [poly[0]]}],
                             skirtType="SolidBodyWithSkirt", skirtLevel=GROUND_BASE_M, ridges="AllSmooth", _mat="ground")
                    if not MESH or "CreateMeshes" in miss:
                        continue
                    TILE_SUBS[(i, j)] = sub                   # v1.58
                    PEND.append((m, sub, 0, 0, (x0, y0, x1, y1), i, j))
                    if len(PEND) >= SITE_BATCH or sum(len(t_[1]) for t_ in PEND) > 30000:
                        flush_()
                    continue
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
                TILE_SUBS[(i, j)] = sub                       # v1.58
                PEND.append((m, sub, nsc, nc, (x0, y0, x1, y1), i, j))    # v1.42: made in batches
                if len(PEND) >= (SITE_BATCH if WHOLE_SITE else 1):
                    flush_()
        flush_()
        BAND_OK.clear()
        if SECTION_BANDS and MESH and "CreateMeshes" not in miss:
            # v1.58 (Aras 18 Nov 08:44 "sections do draw each line between ground cells"): Archicad draws the outline
            # of every mesh, so 50 m tiles show as a grid in a section. One ground mesh per site section covers all it
            # sees (cut line to GROUND_BEHIND_M behind), built from the tiles' own heights; it lives on its own hidden
            # layer and only that section's view shows it (layer combination "BGA - section <name>", tiles hidden)
            n_bh = 0
            for nm_, A_, B_, Ln_, u_, n_ in rects:
                try:
                    R4 = [(A_[0] + u_[0] * s_ + n_[0] * o_, A_[1] + u_[1] * s_ + n_[1] * o_)
                          for s_, o_ in ((-1.0, -SIDE_M), (Ln_ + 1.0, -SIDE_M), (Ln_ + 1.0, GROUND_BEHIND_M),
                                         (-1.0, GROUND_BEHIND_M))]
                    if SITE_POLY:
                        R4 = clean(_clip_convex(R4, SITE_POLY))
                    if len(R4) < 3 or abs(area(R4)) < 1.0:
                        continue
                    poly, cells_ = [], set()
                    for (ax, ay), (bx_, by_) in zip(R4, R4[1:] + R4[:1]):
                        L_ = math.hypot(bx_ - ax, by_ - ay)
                        k_n = max(1, int(round(L_ / BAND_EDGE_M)))
                        for k_ in range(k_n):
                            c = (ax + (bx_ - ax) * k_ / k_n, ay + (by_ - ay) * k_ / k_n)
                            poly.append(dict(xy(c), z=zr(cover_z_many([c], [zat(c)])[0])))   # v1.88
                            cells_.add((int((c[0] - gb[0]) // T), int((c[1] - gb[1]) // T)))
                    f_in = _pip_fast(R4)
                    ed_ = list(zip(R4, R4[1:] + R4[:1]))
                    xs_, ys_ = [q[0] for q in R4], [q[1] for q in R4]
                    sub_ = []
                    for a_ in range(int((min(xs_) - gb[0]) // T), int((max(xs_) - gb[0]) // T) + 1):
                        for b_ in range(int((min(ys_) - gb[1]) // T), int((max(ys_) - gb[1]) // T) + 1):
                            for sl_ in TILE_SUBS.get((a_, b_)) or []:
                                W_ = [(c_["x"] + ox, c_["y"] + oy) for c_ in sl_["coordinates"]]
                                if all(f_in(w_) for w_ in W_) and min(_seg_d(w_, e0, e1) for w_ in W_ for e0, e1 in ed_) >= 0.3:
                                    sub_.append(sl_)
                                    cells_.add((a_, b_))
                    m_ = dict(level=round(base, 3), polygonCoordinates=poly, sublines=sub_ or [{"coordinates": [poly[0]]}],
                              skirtType="SolidBodyWithSkirt", skirtLevel=GROUND_BASE_M, ridges="AllSmooth", _mat="ground")
                    g_ = ac.create("CreateMeshes", "meshesData", [m_], u"ground view %s (%d heights)" % (nm_, len(sub_)))
                    g_ = g_[0] if g_ else None
                    if not g_:
                        continue
                    made.append(g_)
                    PART_G[g_] = "view_" + nm_                # its own layer (set in the labelling step)
                    BAND_OK[nm_] = g_
                    n_bh += len(sub_)
                    SEO_TERR.append((g_, ("tile", min(xs_), min(ys_), max(xs_), max(ys_))))
                    for c_ in cells_:                     # the same solid element operations as the tiles under it
                        TILE_IX.setdefault(c_, []).append(g_)
                except Exception as ex:
                    if _ac_gone(ex):
                        raise
                    log.append(u"FLAG ground view %s not made (%s): that section keeps the tiles" % (nm_, ex))
            log.append(u"ground views (v1.58): %d of %d section(s) got one seamless ground mesh (%d heights in all, "
                       u"the tiles' own), each on its own hidden layer; missing: %s" % (
                           len(BAND_OK), len(rects), n_bh, u", ".join(r_[0] for r_ in rects if r_[0] not in BAND_OK) or u"none"))
        if SECTION_STRIPS and MESH and "CreateMeshes" not in miss and "CreateSlabs" not in miss and \
                any(r_[0] not in BAND_OK for r_ in rects):   # v1.58: only where a view mesh is missing
            # v1.56 (Aras 18 Nov 07:58 "why do we have these kinds of stray lines"): every 50 m tile is its own mesh,
            # so each cut drew a full-height line at every tile seam. Along each section line one ground strip
            # (STRIP_W_M wide, the same heights and bottom as the tiles) takes the tiles' place: a hidden slab
            # (layer "BGA SEO operators (hidden)") cuts that slot out of the tiles, the strip fills it
            try:
                sm_, so_, sn_ = [], [], []
                for nm_, A_, B_, Ln_, u_, n_ in rects:
                    if nm_ in BAND_OK:            # v1.58: this section has its own ground mesh
                        continue
                    k_n = max(2, int(math.ceil(Ln_ / STRIP_STEP_M)))
                    cl_ = [(A_[0] + u_[0] * Ln_ * k / k_n, A_[1] + u_[1] * Ln_ * k / k_n) for k in range(k_n + 1)]
                    runs_, cur_ = [], []
                    for q in cl_:                         # only where the tiles are (site_alan)
                        if not SITE_POLY or _inpoly(q, SITE_POLY):
                            cur_.append(q)
                        elif cur_:
                            runs_.append(cur_)
                            cur_ = []
                    if cur_:
                        runs_.append(cur_)
                    for R_ in [r_ for r_ in runs_ if len(r_) >= 2]:
                        hw = STRIP_W_M / 2.0
                        Lft = [(q[0] + n_[0] * hw, q[1] + n_[1] * hw) for q in R_]
                        Rgt = [(q[0] - n_[0] * hw, q[1] - n_[1] * hw) for q in R_]
                        P_ = Lft + Rgt[::-1]
                        zs_ = [zat(q) for q in P_ + R_]
                        sm_.append(dict(level=round(base, 3), polygonCoordinates=[dict(xy(q), z=zr(zat(q))) for q in P_],
                                        sublines=[{"coordinates": [dict(xy(q), z=zr(zat(q))) for q in R_]}],
                                        skirtType="SolidBodyWithSkirt", skirtLevel=GROUND_BASE_M, ridges="AllSmooth",
                                        _mat="ground"))
                        top_ = max(zs_) - z0 + 2.0
                        bot_ = base - GROUND_BASE_M - 1.0
                        so_.append(dict(level=round(top_, 3), thickness=round(top_ - bot_, 3),
                                        polygonCoordinates=[xy(q) for q in P_]))
                        sn_.append((nm_, R_))
                gsl_ = ac.create("CreateSlabs", "slabsData", so_, u"section slots (hidden SEO operators)") if so_ else []
                made += [g for g in gsl_ if g]
                gst_ = ac.create("CreateMeshes", "meshesData", sm_, u"ground strips on the section lines") if sm_ else []
                made += [g for g in gst_ if g]
                n_sl = 0
                for (nm_, R_), gs_, gm_ in zip(sn_, gsl_, gst_):
                    if not gs_ or not gm_:
                        continue
                    cells_ = set()
                    for q in R_:
                        ci_, cj_ = int((q[0] - gb[0]) // T), int((q[1] - gb[1]) // T)
                        cells_.update((ci_ + a_, cj_ + b_) for a_ in (-1, 0, 1) for b_ in (-1, 0, 1))
                    tg_ = set(g_ for c_ in cells_ for g_ in TILE_IX.get(c_, []))
                    EXTRA_LINKS.extend(dict(targetId={"guid": t_}, operatorId={"guid": gs_}, operation="Subtraction")
                                       for t_ in tg_)
                    n_sl += len(tg_)
                    for q in R_:                          # the strip is ground too: the other operations cut it
                        c_ = (int((q[0] - gb[0]) // T), int((q[1] - gb[1]) // T))
                        if gm_ not in TILE_IX.setdefault(c_, []):
                            TILE_IX[c_].append(gm_)
                log.append(u"ground strips (v1.56): %d strip(s) %.1f m wide along the section lines (one mesh each, so the "
                           u"cut has no tile seams), %d slot cut(s) out of the tiles by hidden slabs" % (
                               sum(1 for g in gst_ if g), STRIP_W_M, n_sl))
            except Exception as ex:
                if _ac_gone(ex):
                    raise
                log.append(u"FLAG ground strips not made (%s): the tile seams stay in the sections" % ex)
        n_t, n_pts, n_ctl = CNT
        if ACC:                                           # v1.45: the accuracy reached, tile by tile
            from collections import Counter as _C
            cg_ = _C(a_[0] for a_ in ACC)
            log.append(u"ground accuracy (v1.45): %d tiles; grid %s; deviation from the survey max %.3f m, mean of the "
                       u"tile maxima %.3f m; tolerance +-%.0f %% of each tile's height range, at least %.2f m; %d tile(s) "
                       u"over it even at %.0f m (FLAG)" % (
                           len(ACC), u", ".join(u"%.0f m x %d" % (k, v) for k, v in sorted(cg_.items())),
                           max(a_[1] for a_ in ACC), sum(a_[1] for a_ in ACC) / len(ACC), GROUND_TOL_F * 100,
                           GROUND_TOL_MIN, sum(1 for a_ in ACC if a_[1] > a_[2]), GROUND_GRIDS[-1]))
        log.append(u"ground: %d tile(s) with no survey point of their own filled from the survey triangulation (no gaps)" % N_TINONLY[0])
        if THIN[1]:                                       # v1.54
            log.append(u"ground thinned (v1.54): %d of %d finer-grid heights dropped (each within its tile's tolerance "
                       u"of the 8 m grid, which is always kept); %d heights sent to Archicad" % (
                           THIN[0], THIN[1], CNT[1]))
        log.append(u"ground: %d tiles of %.0f m sharing their edge points (one surface, no gaps), %d survey heights "
                   u"(one per %.0f m), %d control points (every %.0f m where none), block %.1f m under its lowest "
                   u"point (%.1f m)" % (n_t, T, n_pts, GROUND_SPOT_M, n_ctl, GROUND_GRID_M, GROUND_BASE_M, zlo))

        # ---- walls (+ windows on the walls a cut looks at)
        walls, wmeta = [], []

        FOOT_OF = {}                                      # v1.86: house index -> its one ground-floor wall foot

        def foot_(b, a, c):                               # v1.74: ground-floor wall down over the raft edge
            zs_ = [z_ for z_ in (tin.z(q[0] - ox, q[1] - oy) for q in (a, c, ((a[0] + c[0]) / 2.0, (a[1] + c[1]) / 2.0)))
                   if z_ is not None]
            lo_ = min(zs_ + [b["z"]])
            return lo_ - 0.05 if lo_ < b["z"] - 0.01 else b["z"]
        PARTY = _party_skip(bld)                          # v1.88: a shared side gets one wall, not two
        log.append(u"house sides shared with a neighbour (v1.88, Aras 20 Nov 09:51 \"two walls in the same place\"): "
                   u"%d built once, by the taller house" % len(PARTY))
        for bi, b in enumerate(bld):
            top_extra = 0.6 if b["fl"] >= FLAT_FLOORS else 0.0
            R = b["ring"]
            Rc = _inset(R, _wt(b) / 2.0)          # v1.85: the wall centre lines, so every wall lies inside the footprint
            co_ = _core_out(b)                    # v1.87: composite: reference line on the core's outside face
            if co_ is not None:
                Rc = _inset(R, co_)
            st_ = _scr_t()                        # v1.87: screed over the floor core: wall ends at the core tops
            for ei_, ((a, c), (ac_, cc_)) in enumerate(zip(zip(R, R[1:] + R[:1]), zip(Rc, Rc[1:] + Rc[:1]))):
                ln = math.hypot(c[0] - a[0], c[1] - a[1])
                if ln < 0.3 or (bi, ei_) in PARTY:       # v1.88: the neighbour's wall stands on this side
                    continue
                on = ((c[1] - a[1]) / ln, -(c[0] - a[0]) / ln)        # outward normal (ring counter-clockwise)
                faces = b["fl"] > 0 and any(on[0] * -r[5][0] + on[1] * -r[5][1] > 0.05 for r in b["views"])
                if b["fl"] < 0:                       # the hall: one wall, into the ground
                    flr_ = [(None, b["z"] - PLINTH, b["h"] + PLINTH + top_extra)]
                else:                                 # v1.72: one wall per side per storey (Aras 13:17)
                    fh0 = b["h"] / b["fl"]
                    flr_ = [(k_, b["z"] + k_ * fh0 - (st_ if k_ else 0.0),
                             fh0 + (top_extra if k_ == b["fl"] - 1 else 0.0) + (st_ if k_ else 0.0)
                             - (st_ if k_ < b["fl"] - 1 else 0.0)) for k_ in range(b["fl"])]
                if b["fl"] > 0:                       # v1.74; v1.86: ONE foot for the whole house (Aras 09:20 "their
                    # height changes ever so slightly so intersect command doest works"): the lowest of its sides
                    if bi not in FOOT_OF:
                        FOOT_OF[bi] = min(foot_(b, a2_, c2_) for a2_, c2_ in zip(R, R[1:] + R[:1]))
                    f_ = FOOT_OF[bi]
                    flr_ = [(k_, f_, hh_ + zb_ - f_) if k_ == 0 else (k_, zb_, hh_) for k_, zb_, hh_ in flr_]
                for k_, zb_, hh_ in flr_:
                    # v1.85 (Aras 19 Nov 09:16 "something is wrong with house drawings"): centre reference lines
                    # that meet at the corners (were outside-face lines whose ends left the wall layers showing)
                    if co_ is not None and WALL_SIDE[0] is None:
                        WALL_SIDE[0] = _wall_side(ac, xy, ac_, cc_, on, b, log)
                    e0_, e1_ = (cc_, ac_) if co_ is not None and WALL_SIDE[0] == "rev" else (ac_, cc_)
                    walls.append(dict(begCoordinate=xy(e0_), endCoordinate=xy(e1_), zCoordinate=round(zb_ - z0, 3),
                                      height=round(hh_, 3), thickness=_wt(b),
                                      referenceLineLocation="CoreOutside" if co_ is not None else "Center",
                                      _mat="heritage_red" if b["fab"] in HERITAGE_FABS else None,
                                      **dict(_wcomp(b), **L("BG buildings"))))
                    wmeta.append((bi, ln, faces, a, c, on, k_))
        wg = ac.create("CreateWalls", "wallsData", walls, u"walls") if "CreateWalls" not in miss else []
        made += [g for g in wg if g]
        for g, mt in zip(wg, wmeta):                      # v1.45: the house group
            if g and bld[mt[0]]["fl"] > 0:
                BGRP.setdefault(mt[0], []).append(g)
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
            trad_ = b.get("fab") == "traditional"    # v1.46: Bergama KAIP opening sizes in the historic core (R9)
            ww_, wh_ = (WIN_W_TRAD, WIN_H_TRAD) if trad_ else (WIN_W, WIN_H)
            dw_, dh_ = (DOOR_W_TRAD, DOOR_H_TRAD) if trad_ else (DOOR_W, DOOR_H)
            nw = max(1, int((ln - 1.0) // WIN_STEP))
            x0 = (ln - (nw - 1) * WIN_STEP) / 2.0
            has_door = door_wall.get(bi, (None,))[0] == g
            if has_door:
                doors.append(dict(ownerWallId={"guid": g}, width=dw_, height=dh_, sillHeight=round(b["z"] - FOOT_OF.get(bi, b["z"]), 2),
                                  centerOffset=round(ln / 2.0, 2)))
            u_ = ((c_[0] - a_[0]) / ln, (c_[1] - a_[1]) / ln)
            for i in ([k_] if k_ is not None else range(b["fl"])):   # v1.44: this storey's wall only
                for j in range(nw):
                    xo = x0 + j * WIN_STEP
                    if i == 0 and has_door and abs(xo - ln / 2.0) < (dw_ + ww_) / 2.0 + 0.3:
                        continue                      # the door's place on the ground floor
                    wins.append(dict(ownerWallId={"guid": g}, width=ww_, height=round(min(wh_, fh * 0.5), 2),
                                     sillHeight=round((0 if k_ is not None else i * fh) + min(WIN_SILL, fh * 0.3)
                                                      + (_scr_t() if k_ else 0.0)   # v1.87: wall starts at the core top
                                                      + (b["z"] - FOOT_OF.get(bi, b["z"]) if k_ == 0 else 0.0), 2),   # v1.74; v1.86 one foot
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
                        rails.append([(p1, q1, q2, p2), lv])   # v1.83: one railing per balcony
        if wins and "CreateWindows" not in miss:
            made += [g for g in ac.create("CreateWindows", "windowsData", wins, u"windows (walls facing a cut)") if g]
        if doors and ac.has("CreateDoors"):           # v1.14
            made += [g for g in ac.create("CreateDoors", "doorsData", doors, u"ground-floor doors") if g]
        elif doors:
            log.append(u"FLAG Tapir has no CreateDoors: %d ground-floor doors not made (update Tapir)" % len(doors))
        if bals and "CreateSlabs" not in miss:
            made += [g for g in ac.create("CreateSlabs", "slabsData", bals, u"balcony slabs (blocks of %d+ floors)"
                                          % BAL_FLOORS) if g]
        if rails:                                 # v1.83 (Aras 19 Nov 09:01 "balcony rails as one railing per balcony")
            left_ = rails
            if ac.has("CreateRailings"):
                g_ = ac.create("CreateRailings", "railingsData", [dict(coordinates=[xy(q) for q in P_], floorIndex=0,
                               bottomOffset=lv_, height=RAIL_H) for P_, lv_ in rails], u"balcony railings (Railing tool)")
                made += [g for g in g_ if g]
                left_ = [r_ for r_, g in zip(rails, g_) if not g]
                if left_:
                    log.append(u"FLAG balcony railings: %d refused by Archicad, made as 3 thin walls each" % len(left_))
            else:
                log.append(u"FLAG Tapir has no CreateRailings: balcony rails made as 3 thin walls each (update Tapir)")
            if left_ and "CreateWalls" not in miss:
                made += [g for g in ac.create("CreateWalls", "wallsData", [
                    dict(begCoordinate=xy(e0), endCoordinate=xy(e1), zCoordinate=lv_, height=RAIL_H, thickness=0.05,
                         referenceLineLocation="Center", **L("BG buildings"))
                    for P_, lv_ in left_ for e0, e1 in zip(P_, P_[1:])], u"balcony rails") if g]
        log.append(u"house detail (drawing rules, not surveyed): %d doors, %d windows, %d balconies; %d houses with no "
                   u"floor count built as 1 floor (ASSUMED)" % (len(doors), len(wins), len(bals), skipped))

        # ---- roofs and slabs
        roofs, flats, slabs = [], [], []
        ground_i, flats_n = [], []                    # v1.31
        SL_BI, RO_BI = [], []                         # v1.45: house of each slab / roof (groups)
        for bi_, b in enumerate(bld):
            if b["fl"] < 0:
                continue                              # Kızıl Avlu: the roofless Roman hall
            poly = [xy(q) for q in b["ring"]]
            poly_in = [xy(q) for q in _inset(b["ring"], _wt(b))]   # v1.85: inside the walls (no slab edge on the facade)
            top = round(b["z"] + b["h"] - z0, 3)
            if b["fl"] >= FLAT_FLOORS:
                # v1.28 (Aras 20:10 "give both slabs and roofs to every building"): the flat roof is a Roof-tool
                # single-plane roof, FLAT_ROOF_DEG fall from its longest edge (a slab only if Archicad refuses it)
                R0 = _inset(b["ring"], _wt(b))      # v1.85: the flat roof sits inside the parapet walls
                ka = max(range(len(R0)), key=lambda k_: math.hypot(R0[(k_ + 1) % len(R0)][0] - R0[k_][0],
                                                                   R0[(k_ + 1) % len(R0)][1] - R0[k_][1]))
                roofs.append(dict(level=top, polygonCoordinates=poly_in, **_ccomp("roof_flat", 0.3, "Basic"),
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
                if HOUSE_CORNICE:                     # v1.85: off (a drawing-rule band that read as a loose layer)
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
                           polygonCoordinates=poly_in,   # v1.88 (Aras 20 Nov 09:53 "slab extends to the outer face of the walls"): inside the walls _mat=u"heritage_red" if b["fab"] in HERITAGE_FABS else u"rc",
                           **L("BG buildings"))]
            slabs += [dict(level=round(b["z"] + i * fh - _scr_t() - z0, 3), polygonCoordinates=poly_in,   # v1.85: inside the walls
                           **dict(_ccomp("floor_rc", 0.25), **dict(L("BG buildings"), **(   # v1.87: level = core top
                               {"referencePlaneLocation": "CoreTop"} if "floor_rc" in COMP_ID else {}))))
                       for i in range(1, b["fl"])]
            ground_i.append(len(flats_n) + len(slabs) - b["fl"])     # v1.31: index of its ground slab in slabs
            SL_BI.extend([bi_] * b["fl"])
            RO_BI.append(bi_)
        log.append(u"raft foundations: %d houses, top = ground floor (survey ground at the centroid), bottom %.2f m "
                   u"(ASSUMED) under the lowest survey ground under the footprint (deepest step %.2f m); each cuts the "
                   u"ground upwards (SEO)" % (N_RAFT[0], RAFT_T_M, N_RAFT[1]))
        if "CreateRoofs" not in miss and roofs:
            rg = ac.create("CreateRoofs", "roofsData", roofs, u"roofs (hipped + flat single-plane)")
            made += [g for g in rg if g]
            for g, bi_ in zip(rg, RO_BI):                 # v1.45: the house group
                if g:
                    BGRP.setdefault(bi_, []).append(g)
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
            for g, bi_ in zip(gsl_, SL_BI):               # v1.45: the house group
                if g:
                    BGRP.setdefault(bi_, []).append(g)
            sl_ = (flats + slabs)[len(flats):]
            EXTRA_OPS.extend((gsl_[i], "SubtractionUpwards", sl_[i]["polygonCoordinates"]) for i in ground_i
                             if 0 <= i < len(gsl_) and gsl_[i])

        # ---- v1.44 (Aras 11:18 "those rafts should connect columns and that columns should be connected by beams"):
        # a frame in every framed house: columns on the raft, beams under every floor slab and the roof
        fcols, fbeams, n_fh, n_fskip = [], [], 0, 0
        FC_BI, FB_BI = [], []                         # v1.45: house of each column / beam (groups)
        for bi_, b in enumerate(bld):
            if b["fl"] <= 0 or b["fab"] in HERITAGE_FABS or b["fab"] in FRAME_SKIP_FABS or not CONTEXT_FRAMES:
                n_fskip += 1                          # masonry: the Roman hall, sacred and monument buildings
                continue                              # v1.49: no frame in the survey (context) houses
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
                      for k_ in range(b["fl"]) for p in uq]   # v1.72: one per storey again
            FC_BI.extend([bi_] * (b["fl"] * len(uq)))
            fh_ = b["h"] / b["fl"]
            spans_ = []                               # v1.44 (Aras 11:37 "single beam travelling all across the grid"):
            for p, q in segs_:                        # every beam line split at each column on it: one beam per span
                Lq = math.hypot(q[0] - p[0], q[1] - p[1])
                if Lq < 0.3:
                    continue
                ts_ = [0.0, 1.0]                      # v1.71: one beam per grid line (was split at every column)
                ts_ = [t_ for t_ in ts_ if 0.0 <= t_ <= 1.0]
                for t0_, t1_ in zip(ts_, ts_[1:]):
                    if (t1_ - t0_) * Lq >= 0.3:
                        spans_.append(((p[0] + (q[0] - p[0]) * t0_, p[1] + (q[1] - p[1]) * t0_),
                                       (p[0] + (q[0] - p[0]) * t1_, p[1] + (q[1] - p[1]) * t1_)))
            for i in range(1, b["fl"] + 1):           # under each floor slab and under the roof
                zt_ = round(b["z"] + i * fh_ - 0.25 - z0, 3)
                fbeams += [dict(begCoordinate=xy(p), endCoordinate=xy(q), zCoordinate=zt_, width=FRAME_BEAM_W,
                                height=FRAME_BEAM_H, _mat="rc") for p, q in spans_]
                FB_BI.extend([bi_] * len(spans_))
        if fcols and "CreateColumns" not in miss:
            t_ = ac.create("CreateColumns", "columnsData", fcols[:1], u"house frame columns (square test)")
            if not t_[0]:                             # Tapir took no square column: round ones of the same width
                log.append(u"FLAG house frame: square columns refused, made round (diameter %.2f m)" % FRAME_COL_M)
                fcols = [dict(((k_, v_) for k_, v_ in c_.items() if k_ != "depth"), circleBased=True) for c_ in fcols]
                made += [g for g in ac.create("CreateColumns", "columnsData", fcols, u"house frame columns (Column tool)") if g]
            else:
                g2_ = ac.create("CreateColumns", "columnsData", fcols[1:], u"house frame columns (Column tool)")
                t_ = list(t_) + list(g2_)
                made += [g for g in t_ if g]
            for g, bi_ in zip(t_ if t_ and t_[0] else [], FC_BI):   # v1.45: the house group
                if g:
                    BGRP.setdefault(bi_, []).append(g)
        if fbeams and "CreateBeams" not in miss:
            gb_ = ac.create("CreateBeams", "beamsData", fbeams, u"house frame beams (Beam tool)")
            made += [g for g in gb_ if g]
            for g, bi_ in zip(gb_, FB_BI):                # v1.45: the house group
                if g:
                    BGRP.setdefault(bi_, []).append(g)
        log.append(u"house frames: %d houses, %d columns (%.2f m square, one per storey, slab to slab), %d beams (one per span) (%.2f x %.2f m "
                   u"under every floor slab and the roof, along the footprint and the %.1f m grid); sizes and grid ASSUMED; "
                   u"%d buildings without a frame (masonry: traditional, sacred, monument, Kizil Avlu%s)" % (
                       n_fh, len(fcols), FRAME_COL_M, len(fbeams), FRAME_BEAM_W, FRAME_BEAM_H, FRAME_SP_M, n_fskip,
                       u"" if CONTEXT_FRAMES else u"; survey houses get no frame since v1.49"))   # v1.55

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
        try:                                              # v1.45: bank zones, objects, people + cars
            made += build_banks(ac, miss, log, xy, z0, tin, ox, oy, survey)
        except Exception as ex:
            import traceback
            log.append(u"FLAG bank zones not built (%s: %s) %s" % (type(ex).__name__, ex, traceback.format_exc()[-400:]))
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
        try:                                              # v1.45: every tree + street furniture + people as objects
            made += build_objects(ac, miss, log, xy, z0, tin, ox, oy, survey)
        except Exception as ex:
            import traceback
            log.append(u"FLAG objects not built (%s: %s) %s" % (type(ex).__name__, ex, traceback.format_exc()[-400:]))
        try:                                              # v1.88: roads, parks, his areas on the lowered ground
            made += build_covers(ac, miss, log, xy, z0, tin, ox, oy)
        except Exception as ex:
            import traceback
            log.append(u"FLAG ground covers not built (%s: %s) %s" % (type(ex).__name__, ex, traceback.format_exc()[-400:]))
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
            sg_ = 1.0 if area(P) > 0 else -1.0             # v1.76: outward normals by the outline's turn
            NO_ = []
            for a, b in zip(P, P[1:] + P[:1]):
                l_ = math.hypot(b[0] - a[0], b[1] - a[1]) or 1e-9
                NO_.append((sg_ * (b[1] - a[1]) / l_, -sg_ * (b[0] - a[0]) / l_))

            def mit_(k, sh):                              # v1.76: corner k pushed out along the mitre
                n1, n2 = NO_[k - 1], NO_[k]
                d_ = 1.0 + n1[0] * n2[0] + n1[1] * n2[1]
                if d_ < 0.2:
                    return (P[k][0] + n2[0] * sh, P[k][1] + n2[1] * sh)
                return (P[k][0] + (n1[0] + n2[0]) / d_ * sh, P[k][1] + (n1[1] + n2[1]) / d_ * sh)
            for ke_, (a, b) in enumerate(zip(P, P[1:] + P[:1])):
                L_ = math.hypot(b[0] - a[0], b[1] - a[1])
                if L_ < 0.5:
                    continue
                nx, ny = NO_[ke_]
                ch_ = []
                for k_ in range(max(1, int(math.ceil(L_ / RET_SEG_M)))):
                    f0, f1 = k_ / math.ceil(L_ / RET_SEG_M), (k_ + 1) / math.ceil(L_ / RET_SEG_M)
                    p0 = (a[0] + (b[0] - a[0]) * f0, a[1] + (b[1] - a[1]) * f0)
                    p1 = (a[0] + (b[0] - a[0]) * f1, a[1] + (b[1] - a[1]) * f1)
                    o = ((p0[0] + p1[0]) / 2.0 + nx * 0.6, (p0[1] + p1[1]) / 2.0 + ny * 0.6)
                    if _in_bld(((p0[0] + p1[0]) / 2.0 + nx * RET_T_M / 2, (p0[1] + p1[1]) / 2.0 + ny * RET_T_M / 2)):
                        ch_.append(None)                   # v1.76: not through a house
                        continue
                    if any(j_ != i_ and bx[0] <= o[0] <= bx[2] and bx[1] <= o[1] <= bx[3] and _inpoly(o, OPS[j_][1])
                           for j_, bx in enumerate(boxes)):
                        ch_.append(None)
                        continue                           # another slab there, no wall
                    gz_ = tin.z(o[0] - ox, o[1] - oy)
                    if gz_ is None:
                        ch_.append(None)
                        continue
                    gz_ -= z0
                    if abs(gz_ - lv) <= RET_MIN_M:
                        ch_.append(None)
                        continue
                    ch_.append((p0, p1, min(gz_, lv) - RET_FOOT_M, max(gz_, lv)))
                for p0, p1, lo_, hi_ in _merge_runs(ch_):  # v1.71: one wall per run
                    sh = RET_T_M / 2.0
                    at_a_ = math.hypot(p0[0] - a[0], p0[1] - a[1]) < 1e-6
                    at_b_ = math.hypot(p1[0] - b[0], p1[1] - b[1]) < 1e-6
                    b0_ = mit_(ke_, sh) if at_a_ else (p0[0] + nx * sh, p0[1] + ny * sh)   # v1.76: corners meet
                    b1_ = mit_((ke_ + 1) % len(P), sh) if at_b_ else (p1[0] + nx * sh, p1[1] + ny * sh)
                    rw.append(dict(begCoordinate=xy(b0_),
                                   endCoordinate=xy(b1_), zCoordinate=round(lo_, 3),
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
        _heal(ac, log, u"after the old elements were deleted")   # v1.78

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
        bset_ = set(BAND_OK.values())                     # v1.61: kerbs / walls cut only the section view grounds
        links += [dict(targetId={"guid": tg}, operatorId={"guid": og}, operation="Subtraction")
                  for og, pa in KERB_OPS for tg in terr_at([(q["x"] + ox, q["y"] + oy) for q in pa]) if tg in bset_]
        RPIP = [(tg, _pip_fast(H)) for tg, H in RIVER_MESH]
        for wg, P in WATER_OPS:
            c = (sum(q[0] for q in P) / len(P) + ox, sum(q[1] for q in P) / len(P) + oy)
            links += [dict(targetId={"guid": wg}, operatorId={"guid": tg}, operation="Subtraction")
                      for tg in ([] if RIVER_MESH else terr_at([c]))]   # v1.44: in the channel only the bed body cuts the water
            links += [dict(targetId={"guid": wg}, operatorId={"guid": tg}, operation="Subtraction")
                      for tg, f_ in RPIP if f_(c)]
        links += EXTRA_LINKS                              # v1.44: road minus pavement
        # v1.66 (Aras 18 Nov "as little as possible"): keep only the links that show
        def _seg_box(A, B, bx):                           # segment A-B meets box (x0, y0, x1, y1)
            t0, t1 = 0.0, 1.0
            for p_, q_ in ((-(B[0] - A[0]), A[0] - bx[0]), (B[0] - A[0], bx[2] - A[0]),
                           (-(B[1] - A[1]), A[1] - bx[1]), (B[1] - A[1], bx[3] - A[1])):
                if p_ == 0:
                    if q_ < 0:
                        return False
                    continue
                r_ = q_ / p_
                if p_ < 0:
                    t0 = max(t0, r_)
                else:
                    t1 = min(t1, r_)
                if t0 > t1:
                    return False
            return True

        def _near_cut(P):
            if not P:
                return True                               # footprint unknown: kept
            bx = (min(q[0] for q in P) - SEO_CORR_M, min(q[1] for q in P) - SEO_CORR_M,
                  max(q[0] for q in P) + SEO_CORR_M, max(q[1] for q in P) + SEO_CORR_M)
            return any(_seg_box(A, B, bx) for A, B in SEC_R)
        for og, P, _lv in SEO_OPS:
            OP_PTS[og] = [(q[0] + ox, q[1] + oy) for q in P]
        for og, _op, pa in EXTRA_OPS:
            OP_PTS[og] = [(q["x"] + ox, q["y"] + oy) for q in pa]
        for og, pa in KERB_OPS:
            OP_PTS[og] = [(q["x"] + ox, q["y"] + oy) for q in pa]
        riv_ = set(g_ for g_, _H in RIVER_MESH)
        wat_ = set(g_ for g_, _P in WATER_OPS)
        links_all = [l_ for l_ in links if l_["targetId"]["guid"] and l_["operatorId"]["guid"]]
        links = [l_ for l_ in links_all if l_["operatorId"]["guid"] in riv_            # channel opening, water by its bed
                 or l_["targetId"]["guid"] in wat_
                 or (l_["operatorId"]["guid"] in OP_PTS and _near_cut(OP_PTS[l_["operatorId"]["guid"]]))
                 or l_["operatorId"]["guid"] not in OP_PTS]
        log.append(u"solid element operations (v1.66): %d of %d links kept (within %.0f m of a section line, the river "
                   u"channel, the water); the other %d are hidden inside the ground in 3D and are not made"
                   % (len(links), len(links_all), SEO_CORR_M, len(links_all) - len(links)))
        n_all = len(links)                                 # v1.34: a link between two kept elements is still there
        links = [l_ for l_ in links if l_["targetId"]["guid"] and l_["operatorId"]["guid"]]   # v1.52: both in this file
        # v1.59 (Aras 18 Nov 09:58 "solid element operations is not conducted properly"): v1.58 skipped every link
        # between two kept elements, trusting it was made before; 5,934 links failed on 18 Nov and earlier runs had
        # failures too, so those were never made again. Now only the links recorded as MADE are skipped; the first
        # v1.59 run has no record and sends them all
        want_ = set(l_["targetId"]["guid"] + u"|" + l_["operatorId"]["guid"] + u"|" + l_["operation"] for l_ in links)
        LINKS_OK.clear()
        tg_all = sorted(set(l_["targetId"]["guid"] for l_ in links_all))   # v1.66: all, so dropped ones are removed
        q_ok = True
        own_g = set(it[1] for it in ITEMS)                # v1.64: AcBuild's own elements of this pass
        stale_ = []
        for i_ in range(0, len(tg_all), 500):            # v1.59: the links already in the model, asked from Archicad
            part_t = tg_all[i_:i_ + 500]
            _progress(u"solid element operations: reading existing links %d-%d of %d targets" % (
                i_ + 1, i_ + len(part_t), len(tg_all)))
            try:
                r_ = ac.t("GetSolidElementLinks", {"elements": [{"elementId": {"guid": g}} for g in part_t]}, 900.0)
                for g, e in zip(part_t, r_.get("solidLinks") or []):
                    for lk in ((e or {}).get("solidLinksWithTheGivenTarget") or []) if isinstance(e, dict) else []:
                        k_ = g + u"|" + ((lk.get("operatorId") or {}).get("guid") or u"") + u"|" + (lk.get("operation") or u"")
                        if k_ in want_:
                            LINKS_OK.add(k_)
                        elif ((lk.get("operatorId") or {}).get("guid") or u"") in own_g:   # v1.64: ours, unwanted
                            stale_.append(dict(targetId={"guid": g}, operatorId={"guid": lk["operatorId"]["guid"]}))
            except Exception as ex:
                if _ac_gone(ex):
                    raise
                q_ok = False
                log.append(u"FLAG existing solid links not read (%s): the run's own record is used" % ex)
                break
        if not q_ok:
            LINKS_OK.update(k_ for k_ in (old.get("links_ok") or []) if k_ in want_)
        elif stale_ and ac.has("RemoveSolidElementLinks"):   # v1.64
            n_rm = 0
            for i_ in range(0, len(stale_), 500):
                _progress(u"solid element operations: removing unwanted links %d-%d of %d" % (
                    i_ + 1, min(i_ + 500, len(stale_)), len(stale_)))
                try:
                    r_ = ac.t("RemoveSolidElementLinks", {"solidLinks": stale_[i_:i_ + 500]}, 900.0)
                    n_rm += sum(1 for e in (r_.get("executionResults") or []) if isinstance(e, dict) and e.get("success"))
                except Exception as ex:
                    if _ac_gone(ex):
                        raise
                    log.append(u"FLAG unwanted solid links not removed (%s)" % ex)
                    break
            log.append(u"solid element operations (v1.64): %d of %d unwanted older link(s) removed (e.g. kerbs / walls "
                       u"cutting the 3D tiles)" % (n_rm, len(stale_)))
        links = [l_ for l_ in links if l_["targetId"]["guid"] + u"|" + l_["operatorId"]["guid"] + u"|" + l_["operation"]
                 not in LINKS_OK]
        LINK_T.update(l_["targetId"]["guid"] for l_ in links)   # v1.44: their 3D box changes: stamped again
        log.append(u"solid element operations: %d of %d needed (the others are already in the model)"
                   % (len(links), n_all))
        SEO_TODO[:] = links                                # v1.51: made after the labels + a save (below)
    if os.path.isfile(SEO_PENDING):                       # v1.51: links a stopped / crashed run did not make
        try:
            with open(SEO_PENDING, encoding="utf-8") as f_:
                pend_ = json.load(f_)
            seen_ = set((l_["targetId"]["guid"], l_["operatorId"]["guid"]) for l_ in SEO_TODO)
            add_ = [l_ for l_ in pend_ if (l_["targetId"]["guid"], l_["operatorId"]["guid"]) not in seen_]
            SEO_TODO.extend(add_)
            LINK_T.update(l_["targetId"]["guid"] for l_ in add_)
            log.append(u"solid element operations: %d left over from the last run added" % len(add_))
        except Exception as ex:
            log.append(u"FLAG %s not read (%s)" % (SEO_PENDING, ex))
    if PID[0] and not reuse:                              # v1.44: the record goes into the pln
        hm_ = dict((it[1], it[0]) for it in ITEMS)
        pr_ = [(g, hm_[g]) for g in (set(NEW_G) | LINK_T) if g in hm_]
        stamp_log(log, stamp(ac, PID[0], pr_) if pr_ else 0, len(pr_),
                  u"new / cut element(s) stamped BGA-<part>-<fingerprint>@<3D box>")    # v1.54
        # v1.45 (Aras 11:58 "group all these in a way that we can be able to edit a part of this anytime"): layers
        if LAYER_ID:
            lay_all = not old.get("layers_v145")
            gl_ = [g for g in PART_G if (lay_all or g in NEW_G)]
            n_l = 0
            for i in range(0, len(gl_), LAYER_CHUNK):
                _progress(u"layers %d-%d of %d" % (i + 1, min(i + LAYER_CHUNK, len(gl_)), len(gl_)))   # v1.57
                try:
                    r_ = ac.t("SetDetailsOfElements", {"elementsWithDetails": [
                        {"elementId": {"guid": g}, "details": {"layerIndex": LAYER_ID.get(PART_G[g], LAYER_ID.get("other"))}}
                        for g in gl_[i:i + LAYER_CHUNK]]}, 900.0)
                    n_l += sum(1 for e in (r_.get("executionResults") or []) if isinstance(e, dict) and e.get("success"))
                except Exception as ex:
                    log.append(u"FLAG layers not set on %d elements (%s)" % (len(gl_[i:i + LAYER_CHUNK]), ex))
            old["layers_v145"] = True
            log.append(u"layers: %d element(s) put on the BGA layer of their part" % n_l)
        grp_ = [gs for gs in BGRP.values() if len(gs) >= 2 and all(g in NEW_G for g in gs)]
        n_g = 0
        for i in range(0, len(grp_), 200):                # v1.45: one group per (new) house
            _progress(u"house groups %d-%d of %d" % (i + 1, min(i + 200, len(grp_)), len(grp_)))   # v1.57
            try:
                r_ = ac.t("CreateGroups", {"elementGroups": [{"elements": [{"elementId": {"guid": g}} for g in gs]}
                                                             for gs in grp_[i:i + 200]]}, 900.0)
                n_g += sum(1 for e in (r_.get("groupGuids") or []) if isinstance(e, dict) and not e.get("error"))
            except Exception as ex:
                log.append(u"FLAG house groups not made (%s)" % ex)
                break
        log.append(u"groups: %d house(s) grouped (raft, floors, walls, frame, roof; ungroup to edit one part)" % n_g)
    # v1.51: save BEFORE the solid element operations (the step that crashed Archicad on 17 Nov 15:07-15:11), then make
    # them in small batches with the RAM guard; what is not made stays in SEO_PENDING for the next run
    _save(ac, log, u"labelled model, before the solid element operations")
    if SEO_TODO:
        try:
            with open(SEO_PENDING, "w", encoding="utf-8") as f_:
                json.dump(SEO_TODO, f_)
        except Exception as ex:
            log.append(u"FLAG %s not written (%s)" % (SEO_PENDING, ex))
        try:
            ac.t("ChangeWindow", {"windowType": "FloorPlan", "storyIndex": 0})    # v1.36
        except Exception:
            pass
        n_ok, i, stop_ = 0, 0, None
        while i < len(SEO_TODO):
            part_ = SEO_TODO[i:i + SEO_CHUNK]
            try:
                fr_ = _ram_guard(u"solid element operations")
            except LowMemoryStop as ex:
                stop_ = u"%s" % ex
                break
            _progress(u"solid element operations %d-%d of %d (free RAM %s GB)" % (
                i + 1, i + len(part_), len(SEO_TODO), u"?" if fr_ is None else u"%.1f" % fr_))
            try:
                rr = ac.t("CreateSolidElementLinks", {"solidLinks": part_})
                res_ = rr.get("executionResults") or []
                n_ok += sum(1 for e in res_ if isinstance(e, dict) and e.get("success"))
                for l_, e in zip(part_, res_):            # v1.59: the record of links made
                    if isinstance(e, dict) and e.get("success"):
                        LINKS_OK.add(l_["targetId"]["guid"] + u"|" + l_["operatorId"]["guid"] + u"|" + l_["operation"])
                    elif not SEO_ERR[0]:
                        SEO_ERR[0] = json.dumps(e)[:300]
                old["links_ok"] = sorted(LINKS_OK)
            except Exception as ex:
                if _ac_gone(ex):
                    _progress(u"FLAG Archicad stopped answering during solid element operations %d-%d" % (
                        i + 1, i + len(part_)))
                    raise ArchicadGone(u"Archicad stopped answering during the solid element operations %d-%d of %d "
                                       u"(%s). The model was saved before this step: reopen the saved pln and run "
                                       u"again, the %d operations left are in %s" % (
                                           i + 1, i + len(part_), len(SEO_TODO), ex, len(SEO_TODO) - i, SEO_PENDING))
                log.append(u"FLAG solid element operations %d-%d not made (%s)" % (i + 1, i + len(part_), ex))
            i += len(part_)
            try:
                with open(SEO_PENDING, "w", encoding="utf-8") as f_:
                    json.dump(SEO_TODO[i:], f_)
            except Exception:
                pass
        if i >= len(SEO_TODO):
            try:
                os.remove(SEO_PENDING)
            except Exception:
                pass
        log.append(u"solid element operations: %d of %d (terrain + river bed cut by plinths, terraces and masterplan slabs; "
                   u"water cut by the ground; road and park cells shaped by the terrain)%s" % (
            n_ok, len(SEO_TODO), u"" if not stop_ else u"; FLAG stopped: %d left for the next run (%s)" % (
                len(SEO_TODO) - i, stop_)))
        if n_ok < i:                                      # v1.59: why Archicad refused some
            log.append(u"FLAG solid element operations: %d not made, first reason: %s (they are tried again next run)" % (
                i - n_ok, SEO_ERR[0] or u"none given"))
        if PID[0] and not reuse:                          # their 3D boxes changed: labelled again
            hm_ = dict((it[1], it[0]) for it in ITEMS)
            pr_ = [(g, hm_[g]) for g in LINK_T if g in hm_]
            stamp_log(log, stamp(ac, PID[0], pr_) if pr_ else 0, len(pr_),
                      u"cut element(s) labelled again after the operations")    # v1.54
        _save(ac, log, u"after the solid element operations")
        if stop_:
            raise LowMemoryStop(stop_ + u" (the model is saved; reopen it and run again to finish the operations)")
    if not reuse:                                         # v1.78: the end check (groups, operations)
        rm_ = _heal(ac, log, u"at the end of the model") or {}
        if rm_ and PID[0]:
            hm_ = dict((it[1], it[0]) for it in ITEMS)
            pr_ = [(g, hm_[g]) for g in rm_.values() if g in hm_]
            stamp_log(log, stamp(ac, PID[0], pr_) if pr_ else 0, len(pr_), u"element(s) made again labelled")
            _save(ac, log, u"after the end check")
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
        if have is not None and not have and secs and FOUND_OWN[0] == 0:   # v1.56: the record is another project's
            log.append(u"sections: %d recorded from another project (this file had no AcBuild element when the run "
                       u"started): record dropped, sections and View Map items made fresh" % len(secs))
            secs, old["views"], old["view_folder"] = {}, {}, None
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
                   useUncutSurfaceFill=True, modelUncutSurfaceFillType="MaterialColorShaded",   # v1.59: PenColor drew the uncut model white without outlines   # v1.57 (Aras 18 Nov screenshot): Uniform Pen - Color Fill, Non-Shaded   # v1.41: own material colour (v1.38 PenColor = white over the hills)
                   modelUncutSurfaceFillBackgroundPenIndex=-1, useOneModelPen=True, modelPenIndex=81,   # v1.44: uniform uncut pens 81   # v1.39: own pens (pen 81 hid the wall edges)
                   transparent=False, effectVectorHatch=False,   # v1.44: no surface cover fill
                   markedDistantArea=True,   # v1.44 (Aras 11:22): fade distant elements on;                     # v1.40 useUncutSurfaceFillInDistantArea=True,
                   useUncutSurfaceFillInDistantArea=True,   # v1.57: fade distant uncut fill: uniform pen colour fill, window background
                   distantAreaUncutSurfaceFillBackgroundPenIndex=-1, useOneDistantAreaPen=True, distantAreaPenIndex=102,   # v1.57: uniform pen 102   # v1.39
                  
                   boundaryDisplayMode="NoContours")
        try:
            ac.t("SetSectionsAndElevationsDetails", {"elementsWithDetails": [
                {"elementId": {"guid": g}, "details": det} for g in secs.values()]})
            log.append(u"section settings (Aras 18 Nov screenshot, v1.59 uncut fill shaded): limited depth %.0f m, cut pens 21 / 101 / transparent, "
                       u"uncut own material colour, shaded, uncut pen 81, fade distant on: uniform pen colour fill "
                       u"(window background), pen 102, no boundary contours" % BACK_M)
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
            try:                                      # v1.56: the cut-house override on every new section view
                vi_ = [x_["navigatorItemId"] for x_ in (r.get("navigatorItems") or [])
                       if isinstance(x_, dict) and x_.get("navigatorItemId")]
                if vi_:
                    ac.t("SetViewSettings", {"navigatorItemIdsWithViewSettings": [dict(
                        navigatorItemId=v_, viewSettings={"graphicOverrideCombination": SEC_COMBO}) for v_ in vi_]})
                    log.append(u"View Map: override combination \"%s\" set on %d view(s)" % (SEC_COMBO, len(vi_)))
                lc_ = [dict(navigatorItemId=v_, viewSettings={"layerCombination": u"BGA - section " + nm})
                       for nm, v_ in zip(todo, vi_) if nm in BAND_OK]   # v1.58: each section sees its own ground
                if lc_:
                    ac.t("SetViewSettings", {"navigatorItemIdsWithViewSettings": lc_})
                    log.append(u"View Map: own ground layer combination set on %d section view(s)" % len(lc_))
            except Exception as ex:
                log.append(u"FLAG override combination not set on the views (%s): in each section view's settings "
                           u"choose \"%s\" by hand" % (ex, SEC_COMBO))
            views.update(dict((nm, True) for nm in todo))
        try:                                              # v1.59: every run, every section view in the View Map
            vm_ = {}

            def walk_s(o):
                if isinstance(o, dict):
                    nm_ = o.get("name")
                    if nm_ in secs and o.get("navigatorItemId"):
                        vm_.setdefault(nm_, []).append(o["navigatorItemId"])
                    for v in o.values():
                        walk_s(v)
                elif isinstance(o, list):
                    for v in o:
                        walk_s(v)
            walk_s(ac.t("GetNavigatorItemTree", {"navigatorMapId": "PublicViewMap"}))
            st_ = [dict(navigatorItemId=v_, viewSettings=dict({"graphicOverrideCombination": SEC_COMBO}, **(
                {"layerCombination": u"BGA - section " + nm} if nm in BAND_OK else {"layerCombination": u"BGA - all"})))
                   for nm, vs_ in vm_.items() for v_ in vs_]
            if st_:
                r_ = ac.t("SetViewSettings", {"navigatorItemIdsWithViewSettings": st_})
                ok_ = sum(1 for e in (r_.get("executionResults") or []) if isinstance(e, dict) and e.get("success"))
                log.append(u"View Map (v1.59): %d of %d section view(s) set to their own ground layer combination and "
                           u"\"%s\"" % (ok_, len(st_), SEC_COMBO))
                if ok_ < len(st_):
                    log.append(u"FLAG view settings: %s" % json.dumps((r_.get("executionResults") or [r_])[:1])[:300])
        except Exception as ex:
            log.append(u"FLAG section view settings not set (%s): open each section view's View Settings and pick the "
                       u"layer combination \"BGA - section <name>\" by hand" % ex)
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
            log.append(u"not published (whole-site build; the project is saved at the end of the run)")
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

    log.append(u"site_alan rule (v1.84, %.0f %% inside or not made; the rest cut at the edge): left out %s" % (
        SITE_SHARE_MIN * 100, u", ".join(u"%s %d" % kv for kv in sorted(SITE_DROP.items())) or u"none"))
    top_ = sorted(STEP_T.items(), key=lambda kv: -kv[1])[:25]   # v1.82: where the minutes go (log only)
    log.append(u"time by step (v1.82, top %d of %d): %s" % (len(top_), len(STEP_T), u"; ".join(
        u"%s %.0f s" % kv for kv in top_)))
    _save(ac, log, u"end of the run")                    # v1.53: auto save at the end (Aras 17 Nov 12:33 UTC)
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
                       layers_v145=old.get("layers_v145", False), links_ok=old.get("links_ok") or [],   # v1.59
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
    try:                                         # v1.48: a fresh progress file per run
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f_:
            f_.write(u"%s  AcBuild %s started, free RAM %s GB\n" % (time.strftime("%H:%M:%S"), VERSION,
                                                                   u"%.1f" % (_free_gb() or 0.0)))
    except Exception:
        pass
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
