# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE SPINE v2.46 (15 Nov 2026; v2.46 = run 31: every node "FLAG 3D: KeyError: 'axo3d_build'": the Axo library was cut at the first "AXO_LIB_END" in its docstring; now at the marker comment line; v2.45 = Aras 16:01 UTC "foreground and background is mixed still" (and 14:50 "draw these in 3D with scripts in rhino and take the drawings from rhino"): each node axonometric is now the node's piece of the slide 1 3D model (axo_model.json d3: ground, parks, streets, river, edges, walls, buildings in their area colours, trees), cut by the node's one cut, with the bus routes and the heritage loop as thin strips on the ground (a building in front hides them), built in the open Rhino and captured in the axo's own parallel view with Page01Axo v4.4's axo3d_build / capture / check (the 3dm never saved, the layer removed after), registered on the card by the cut's edge and laid under the card's vector slab faces and pins; without Rhino, or when a capture fails its check or its registration, the v2.44 2D drawing stays (FLAG); v2.44 = Aras 16:01 UTC "line is too thick and foreground and background is mixed still": in the node axonometrics the buildings and trees are painted as one list back to front (a nearer body always over a farther one), the bus routes and the heritage loop lie on the ground under them (a building in front hides them), their weights from pages_common pc_stroke_k / pc_stroke (one rule for every drawing; about 0.25 / 0.32 mm in a card); and Aras 16:00 UTC "make those gradient, like one gradient swatch should follow along the river and colors should fade in and out" / "this way it'll look a single fill": the area blobs are one fill whose colours fade into each other over about 5 mm at every area boundary (weighted mean of the area colours, the banks kept apart by the river), its edges on the river and the working area smooth; buildings keep their area colour; v2.43 = Aras 15:57 UTC "make these blue and red lines thinner like scale the lines according to the drawing size please across all drawings": in the node axonometrics the bus routes and the heritage loop take weights given for a full-width A3 drawing scaled by the drawing's width: about 0.3 / 0.4 mm in a card (were 0.6 / 0.8); v2.42 = Aras 15:22 UTC no placeholder-looking text anywhere: the building areas on the cards read "proposed" (our design proposals), not "EST."; v2.41 = run 27a FLAGs: three area names (Cultural Heritage both banks, Bazaar north bank) had no room inside their narrow strips: a name may now break into two lines (at its comma) before it shrinks to 1.3 mm; card text ran 4.6 / 6.9 / 1.4 mm below the N2 / N3 / N4 cards: axonometric 43 mm high (was 50), card text 1.7 mm (was 1.75); v2.40 = Aras 15:15 UTC "fix this area in six nodes along the spine drawing" (the east end): the area edges smoothed (each edge pixel the mean of its 5 x 5 window: no stair steps), the base map (quiet, flat river) drawn under master.svg so no part of the frame is left white where master.svg draws nothing, the mahalle boundary lines (a grey line cutting across the areas) and their legend row dropped; v2.39 = Aras 15:07 UTC "this is better however still really awful" (N1): area names smaller (2.3 mm down to 1.6), measured by the true letter widths and kept 1.5 mm inside the frame, a hairline white halo (0.09 mm, was 0.25), no leaders (a small black dot marks each node); master.svg picture tiles that have no colour of their own (the grey squares) left out; v2.38 = Aras 15:06 UTC "what is those green areas that covering areas ?" (master.svg's green picture areas, kesin_yesil / belki_yesil / bitki2, drawn over the area colours) and "just put the .svg directly into that drawing and do the colouring on most foreground layer": the map's base is master.svg as it is (every group, his existing roads and buildings included), no MapBase drawing under it; the area blobs and area-coloured buildings are drawn over it outside the working area, the working-area dashes over everything; Aras 14:56 UTC rule: every number or letter in a marker centred exactly (pages_common pc_text_c on the marker centre); N6 building ~1,560 m2 (the NODE_IDEAS.md rooms' sum); v2.37 = Aras 14:42 UTC "write the names onto the areas that have been painted BOLD BLACK in a readable way": every painted area carries its name in bold black with a thin white letter halo (no box), placed wholly inside its own colour (never across an area edge, the river or the working area), as near its node as fits, the node code in front of the areas a node stands in; the node tags with leaders are gone (a black dot marks each node, with a hairline to its name when the name sits away from it); Aras 14:42 "n2 lower and upper parts not gonna be same please show the difference on the map aswell": the two parts of Cultural Heritage (N2) on the two banks get clearly different colours (rose and brick; the hillside around Ulu Cami and the flat old town), so the map and the N2 axonometric show them apart; Aras 14:43 "the n2 lower and upper parts being different applies to all areas that have been divided": Bazaar, Settled Housing and Industrial Area get a clearly darker second colour on their other bank (Upper / Lower Neighbourhood were already sand / sage); "for that drawings basemaps use masterplan svg aswell" and 14:44 "use the masterplan svg as it is for that map": the map draws all of master.svg (MasterplanBase cache) in its own colours and lines, no longer recoloured into the accent; node axonometrics still without the masterplan (Aras 14:33); Aras 14:43-14:44 "you sure that right top area is industrial ?": no (OSM: no industrial landuse there, small buildings, farm supply shops, the district agriculture office, car dealers and vets on Adnan Menderes Bulvarı): it is now "Boulevard Trade and Services" in its own olive, and Industrial Area is the south bank alone (1. and 2. Sanayi Sitesi); Aras 14:45 "make our working area dashed line as the most foreground line": the working-area dashes drawn over every other line of the map (only the area names above them); node axonometric crash of v2.36 fixed (the cut polygon had taken the colour dict's name K); v2.36 = Aras 14:21 UTC "make those areas fit into the story ... find out what is the differences between upper side of the housings and lower side": each area's legend row carries one short line of what sets it apart, read from its calculated profile (run 25 log: MapBase fabric and shop flags, recorded floors, GLO-30 terrain, OSM heritage), each line logged with the figures behind it; Aras 14:38 UTC "dont do hatches to river" (standing rule): the river is one flat colour on the map (no hatch, no grain) and in the node axonometrics; the heritage count in the profile says when only the first 8 are listed; v2.35 = Aras 14:32 UTC "fill all the informations that are beneath those axonometric diagrams": every card now carries its idea, its story, its building (programme, areas EST.) and its links (hubs, loop stops, bus lines), all from library/node_ideas_2026-11-15/NODE_IDEAS.md (N2, N4 on Aras's marks; N1, N3, N5 stories still drafts there); v2.34 = Aras 14:31 UTC "cut the buildings in axonometric", "use single cut plane" (the orange was our masterplan: Aras 14:33 "keep the masterplan out of this axonometric diagram" for now, so the node axos drop it and its key): one cut for everything in a node axonometric = the node frame inside site_alan (the slide 1 model ends there): the ground pieces are taken back to the plan, cut by it and draped again, the slab top and its hatched faces follow its draped edge, our move, the flows and the pins end on it; in the node axonometrics every building is rebuilt from its MapBase footprint cut to the node frame and raised to the height slide 1 gave it (read back from its roof in the slide 1 model), so buildings end at the slab edge with a darker cut face; v2.33 = Aras 14:29 UTC "use masterplan over here and use the areas backreading of our working area like the place that falls out of our working area in masterplan": the areas are the back-reading of the town around our working area (the Basemap study-area cache "calisma" rings): no area colour or blob inside the working area, where the base map and the masterplan show; buildings inside it stay as the base map draws them; v2.32 = Aras 14:21 UTC "make those areas fit into the story ... find out what is the differences between upper side of the housings and lower side ... make sure that areas really cultural heritage": each area's profile calculated and logged (no drawing change): buildings, recorded floors (count, median, share of 3+), main fabric types (MapBase), shop buildings, terrain height and slope at its buildings (GLO-30 DEM), and the OpenStreetMap heritage inside it (historic / heritage / place of worship / museum / attraction, by name); v2.31 = Aras 14:17-14:19 UTC "fill the empty areas aswell", "make them look a whole", "make bazaar different colour", "divide the settled housings into two", "divide the industrial areas into two", "dont make areas to cross across river": the map is split whole among the areas (every pixel to the nearest area ring), so the areas meet edge to edge with no blank ground, the river left open; every area reaching both banks becomes two (one per bank: Cultural Heritage, Bazaar, Settled Housing, Industrial Area), slivers across the river go to that bank's areas; buildings take the area under their middle; Bazaar saffron, Archaeological Site taupe (no purple); N1 tagged as Upper and Lower Neighbourhood; v2.30 = Aras 13:34 UTC "reuse these by cutting and orienting what the previous axo have generated" and 13:41 "every 3D, 2D or whatever the drawing is should use the basemap and it's extruded version": each node axonometric is cut out of the slide 1 urban fabric axonometric (Page01Axo v3 cache axo_model.json, itself drawn from MapBase: terrain, parks, river, streets, buildings, asset trees) in that drawing's own view: its ground pieces cut to the node frame, its buildings and trees standing in the frame kept whole, the buildings recoloured by area (each face keeps its light / shade step), the node frame as a slab with soil-hatched cut faces; our move, the flows and the pins drawn on the same terrain; without the cache the v2.29 drawing stays (FLAG); v2.29 = Aras 13:44 UTC "it makes drawing too busy also dont have a opaque background for texts in any single of the drawings": the node tags on the map are bold text in the node colour with no box (the leader ends under the text), the neighbourhood fabric names dropped (the fabric reading is gone); v2.28 = Aras 13:32-13:34 UTC "every building that is for neighborhood is same colour a bit more darker shade of it blobs around those buildings and under that blob everything is same colour ... each colour is dedicated to a area", "there is a distinct difference between upper neighborhood and lower neighborhood", "every building should belong to a blob and every building should be coloured": the fabric colouring is replaced by his seven areas (his 9 Nov marked zones, Data/bergama_area_zones.json: Upper and Lower Neighbourhood, Cultural Heritage, Bazaar, Archaeological Site, Settled Housing, Industrial Area); every building on the map takes the colour of the area it stands in (outside all areas: the nearest one), each area an opaque blob a shade darker closed around its buildings (overlaps split by the nearest building), the legend lists the areas, the node axonometrics colour their buildings by area too; v2.27 = run 23 check against the liked set: the axonometrics filled about two thirds of their box (the scale assumed the tallest building at the back corner), now fitted to the real roof tops so each tile is larger and the white gap above it closes; v2.26 = Aras 12:10 UTC "compare with the examples ... bring it closer": the liked set (library/examples/liked_2026-11-12/WHY_WE_LIKED.md) keeps the context pale and quiet with colour strong only where the project acts, and its axo tiles (B08) stand on a hatched soil slab: the buildings keep their fabric colours mixed 55 % toward the paper, the slab 1.4 mm with hairline soil hatching on its cut faces; v2.25 = run 20 check (Aras 10:33 "a little bit more gentle"): the axonometric walls and outlines darkened half as much as the slide 1 steps (the dark fabrics read as black masses); v2.24 = run 18-20 check: a pin whose badge would sit on another pin's stem (N2: loop stop 4 under the K4 tile) leans 4.5 mm aside on a slanted leader; v2.23 = run 20 FLAG: a shorter legend row for the node area; v2.22 = Aras 10:33 UTC "a little bit more gentle lines": building outlines 0.06 in the lit-wall tone, slab and ground lines warm grey not black, map building edges and neighbourhood lines lighter; Aras 10:32 UTC "every single building should be attached to this reading maybe colouring buildings like in the urban fabric": on the map every building in site_alan coloured by its fabric type (MapBase FAB / FAB_COM, as the urban fabric drawings and the axonometrics), drawn over the node areas (lighter, 0.22), the neighbourhood-part tints dropped (the buildings carry the fabric now), legend rows per fabric type; Aras 10:31 UTC "these axo diagrams needs a facelift ... colourize the buildings just we have on the urban fabric axo drawing, take good care of the lines, and the thickness of the ground": buildings in the slide 1 axo's colours (roof = MapBase FAB / FAB_COM of its fabric, walls and outline darkened by that axo's own steps), outlines 0.10 in the building's dark tone, thinner flows with a narrow white casing, the slab 1.0 mm with a 0.35 base line on the slide 1 axo's paper ground; v2.21 = run 18 check: in the axonometrics the bus routes and the heritage loop drawn over the buildings (they were hidden behind them); the terrace edges in the accent (master.svg draws them olive) and the legend swatch of a masterplan group taken from an area piece first; v2.20 = run 17: the axonometric 51 mm high (N2 text ran 3.6 mm below its card); v2.19 = run 16 review: the slab's ground painted (warm grey, outlined) so nothing floats on white paper, its two cut faces darker with a 0.70 base line, shop roofs mid grey (the near-black read as holes), pins that would touch are raised in steps, the axonometric 56 mm high; v2.18 = run 16 check: the axonometrics larger (52 mm high, a flatter view turned 16 degrees, shorter pins, room above kept only for the pins a node has); v2.17 = Aras 06:41 UTC "god these diagrams are awful": the six flat strips replaced by six axonometrics of each node's own ground, from the data (node frame as a slab with its cut face; streets, stream, buildings raised by their recorded floors, shop buildings with dark roofs; our move from the masterplan in the accent; the bus routes and the heritage loop as bold flows; pins for the hub, loop stops and places), in a 3 x 2 grid of cards with one key; v2.16 = Aras 06:43 UTC "dont leave white spots that are not painted and every painting needs to be a blob without any gaps in the middle": each node area is closed wider step by step (from 12 m up to 60 m) until it is one piece, then every hole inside it is filled; v2.15 = Aras 06:19 UTC master.svg is the masterplan (MasterplanBase v1.5): its walk layer yuruyus/circulation in the accent like the other walks; v2.14 = Aras 05:53 UTC "why is buildings etc. is not showing over there": 42 of the bridges' texture pieces in the masterplan cache are picture-area outlines larger than the whole map (each about 21,000 mm2) and drew an opaque grey sheet over the buildings and streets; any masterplan piece over a quarter of the map is now dropped (logged), and the bridges get their accent colour; v2.13 = Aras 15 Nov 04:58 UTC "All defaults are fine" (default: the proposed masterplan pieces get stronger colours): the proposal on the map and its legend rows in the accent family (C07A2E, the one colour for our move), the existing fabric stays grey; v2.12 = run 10 check: the N4 tunnel mouth drawn as a portal in the bank wall (it read as a rock), the shops arrow shorter and further right so it never crosses the raised point's stems; v2.11 = run 9 review: short arrows (12 mm) from each cause toward the hub, grey where no hub exists (the accent is only our move), the hub tile on the street ground clear of the figures, the Roman bridge drawn at N2 and the tunnel mouth at N4 (the ideas name them), map places nudged off the hub tiles with a hairline leader, legend rows for the stream and the node colours, N6 says what is missing, a wider gutter after the strip; v2.10 = run 8 review: the six nodes as rows across the page (the cards were 60-75 % empty, the strips 58 x 6 mm), each strip about 140 x 29 mm with the hub as its map tile on the ground and up to 3 arrows running to it, a dashed empty footprint where there is no hub, the bus road in grey, one dome for the heritage loop, the town one continuous band; the stream line on the map; neighbourhood names placed after the node tags and kept off them; v2.9 = DIAGRAM_STYLE.md v2 refinements (ground low with ~70 % air, the cut 3 x the rest, a small accent, names on brackets under the ground, no numbers on the strip: counts as text under it); v2.8 = Aras 21:31 UTC "all the diagrams are awful": "What meets here" redrawn to library/diagram_style/DIAGRAM_STYLE.md v1 with pages_common pc_dg_kit (one cut across the stream, poché ground, context rhythm, drivers at the edges, one accent for the move, people on it, at most 4 labels, the claim as title); the card plans, tiles and hub glyph removed; v2.7 = Aras 21:21 UTC "recheck every drawing for not applied feedback": the Q500 level mark left in the hub glyph and its key removed (Aras: remove the water and level markers), card plans and their counts cut to site_alan (16:17 rule), masterplan rows say "proposed" not "masterplan" (no sources on drawings), card water textured (water rule); v2.6 = run 7 review: neighbourhood and street lines cut to their frames (a line's clip id sits at item[4]), smoother area edges (8 mask pixels a mm); v2.5 = run 6: a shorter legend row (it ran over its column); v2.4 = Aras 16:19 UTC "mark the areas properly mark the areas that are neighborhoods diversify neighborhoods according to their specialities" and 16:22 UTC on the what-meets-here diagrams "too basic ... more diagramatic more in a architectural design language way": node areas follow their blocks, not boxes; the neighbourhoods (OSM mahalle boundaries) drawn and named with their main fabric, the two neighbourhood nodes (N1, N5) coloured by it; each card's diagram is now the node's own plan (figure-ground, stream, masterplan, hub / loop stops / places at their points, bar, north) over a row of four tiles; the legend a band under the map; the frame from pages_common SiteMap; v2.3 = Aras 16:17 UTC "KEEP EVERY DRAWING STRICTLY IN SITE_ALAN" (the one exception: Plan 01, Page02): the map strip is now exactly site_alan, turned along its long side, nothing drawn outside it; v2.2 = Aras 15:3x UTC "please take these from the masterplan that i have given you anything that concerns masterplans that should use it": the proposal on the map (terraces, canopy, walks, bridges, retaining walls, cycle route, designs) now comes from the MasterplanBase cache (his B19_setB_layers259.svg), the hand-drawn spine line is gone; v2.1 = run 4 review: upper spoke names clear of their marks, the diagram taller and the cards down to the page margin (23 mm were empty)), Panel Review II slide 2: the six nodes along the streamside spine
(output/presentation/2.pdf; one script per page, Aras 14 Nov 10:46 UTC).

v2 = Aras 15:25 UTC: "dont have this like that have nodes more like pointers and give some diagrams to explain and draw it
in landscape and fit every drawing into A3's like the scale is not important"; 15:26: "maybe semi transparent area fill
would be the answer". So: A3 landscape; the map a strip across the top, turned so the stream runs left to right, at the
scale that fits; each node a semi-transparent area (a "soft" item: flat colour through an 8-bit mask, the Basemap
writer's own item) with a pointer tag N#; under the map one card per node: what meets there (a spoke diagram: hub,
heritage loop stops, bus lines, shop buildings; a missing one dashed = the weak link), the hub's levels section,
the idea (N2, N4: Aras's two marks), the project's places in it. The v1 hub cards are folded into the node cards.
Kept rules: no sources on the page (log only, Aras 15:23); no repeats (stops and lines on slide 5, shop shading on
slide 1: counts only here); never import old PDF pages (code from CityLink v13: HUBS, FUNCS, hub_glyph).
v1 history: p9 spine + hub cards without the bottom band, p8 shops folded in (Aras 12:50 UTC).

Drawn from the one MapBase (pages_common pc_mapbase, turned), nodes from Data/section_lines.json (live: if the frames
move, this page follows), hubs, stops and heritage loop from Data/bergama_access_heritage.json.
Outputs (Downloads/Bergama/output/bergama_page_spine/): Spine.pdf, Spine.svg, review/ PNGs; copy presentation/2.pdf.
Reads: Data/bergama_pages_common.py, Data/bergama_access_heritage.json, Data/section_lines.json,
Data/selinos_centreline.json, cached MapBase (press MapBase first), newest scripts/bergama_basemap_v*.py (writer).
Grasshopper: a Button on any input runs it.
"""
import os, re, time, math, zlib, json

VERSION = "v2.46"
SLIDE = 2
GH_LABEL = "PageSpine"
OUT_FOLDER = "bergama_page_spine"
LOG_NAME = "bergama_page_spine_log.txt"
GH_INPUTS = {}
COMMON = os.path.join("Data", "bergama_pages_common.py")
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
NAME = "Spine"
PAGE_W, PAGE_H, MARGIN = 420.0, 297.0, 12.0      # A3 landscape (mm)
SIDE_W = 95.0                                    # the column right of the map: title, north, scale (v2.4: legend under the map)
DEN_STEP = 500                                   # the scale is rounded up to a 1:500 step
CARD_PT = 1.7                                   # v2.35: card text size (mm; was 1.9: the cards now hold idea, story, building, links)
AXO_H = 43.0                                     # v2.17: the axonometric's height in a card (mm); v2.33: 50 (run 25: N2 text 0.9 mm over)
CARD_GAP = 6.0                                   # mm
ROW_COLS = (44.0, 140.0, 80.0)                   # v2.10 node rows: name + claim | strip | what meets (mm); the rest = idea
ROW_GAP = 4.0                                    # mm
NODE_ALPHA = 0.22                                # the node areas' opacity
EDGE_ALPHA = 0.9                                 # v2.4: their edge (one mask pixel, 0.25 mm)
MASK_PPM = 8.0                                   # v2.4: mask pixels a mm (v2.6: 8, smoother edges)
CLOSE_M, ERODE_M = 12.0, 9.0                     # v2.4: the area closes over streets up to 2 x 12 m wide, then 9 m back
NEIGH_NODES = ()                       # the nodes that are neighbourhoods (section_lines.json names:
                                                 # "Neighbourhoods (Upper + Lower)", "Settled Housing")
MIN_BLD = 15                                     # a neighbourhood with fewer buildings in site_alan gets no name
CHAR_COL = {"traditional": "B5562F", "block": "4A6A8A", "regular": "C8A03C", "selfbuilt": "6E8B5E",
            "large": "5F5F66", "monument": "A33B2B", "sacred": "A33B2B"}   # our picks; a neighbourhood's main fabric
MAH_C = "6E675E"                                 # v2.4: neighbourhood lines and names
DG = dict(ground="F4F1EA", street="FFFFFF", water="A2B6B5", bld="8E897F")   # v2.36: flat water (Aras 14:38)     # v2.4: the card plans
NODE_COL = dict(N1="70754C", N2="8B2D2D", N3="5C7A86", N4="4C2528", N5="89986A", N6="8E8F8A")   # palette colours
AREA_FILE = os.path.join("Data", "bergama_area_zones.json")   # v2.28: Aras's seven areas (9 Nov zones, survey m)
AREA_COL = {"YN": "D8C48C", "DN": "A9BC8E", "2": "D29C9A", "3": "E8B04F", "4": "B39C86", "5": "9FC7BD", "6": "B3B1AB",
            "2b": "C0674A", "3b": "A7782E", "5b": "5F8F7E", "6b": "7D7A72"}   # v2.37: each split pair clearly apart (Aras 14:43)
# v2.31: Bazaar saffron, Archaeological taupe (no purple); "b" = the part of an area on its other bank (split at the river)
SPLIT_AREAS = ("5", "6")                         # v2.31: Aras 14:18 split these two in two (at the river)
AREA_STORY = {   # v2.36: one line per area, from the area profiles (spine_run25 log, PageSpine v2.32); keyed by the map name
    u"Upper Neighbourhood": (u"highest and steepest; planned houses, no shops",
                             u"mean 103 m, slope 24 %; fabric regular 67 %; shop buildings 0"),
    u"Lower Neighbourhood": (u"lower slope, 3x the old fabric; Kozan Mescidi",
                             u"mean 90 m, slope 22 %; traditional 21 % (Upper 7 %); shop buildings 4; OSM Kozan Mescidi"),
    u"Cultural Heritage, north bank": (u"hillside around Ulu Cami, old and new mixed",
                                       u"slope 21 %; regular 52 %, traditional 31 %; OSM Bergama Ulu Cami (historic)"),
    u"Cultural Heritage, south bank": (u"flat old town, Parmaklı Mescidi and two mosques",
                                       u"slope 4 %; traditional 63 %; OSM Parmaklı Mescidi (historic), Ansarlı, Divan Hızır"),
    u"Bazaar, south bank": (u"the market: one building in six a shop",
                            u"shop buildings 39 of 245 (16 %); traditional 61 %; slope 4 %"),
    u"Bazaar, north bank": (u"historic slope: a museum, few shops",
                            u"shop buildings 11 of 247 (4 %); slope 17 %; OSM Bergamalı Kadri museum + 7 historic=building"),
    u"Archaeological Site": (u"Kızıl Avlu and Eski Kışla among old houses",
                             u"traditional 46 %, monument 8 %; OSM Kızıl Avlu (temple), Eski Kışla Binası"),
    u"Settled Housing, north bank": (u"planned houses and blocks, no shops",
                                     u"regular 79 %, block 13 %; shop buildings 0; slope 6 %"),
    u"Settled Housing, south bank": (u"older and mixed, one building in seven a shop",
                                     u"traditional 37 % (north 0 % in top 3); shop buildings 27 of 182 (15 %)"),
    u"Boulevard Trade and Services": (u"farm trade and services, two tumuli",
                                      u"OSM: farm supply shops, District Agriculture office, car dealers, vets; "
                                      u"Tumulus Tepe A, Tavşan Tepe Tümülüsü; no industrial landuse"),
    u"Industrial Area": (u"the estate: large sheds, no shops",
                                     u"large 19 %; shop buildings 0; OSM Sanayi Cami"),
}
AREA_RENAME = {   # v2.37: Aras 14:43-14:44 "you sure that right top area is industrial ?" (OSM check, 15 Nov, in site_alan)
    u"Industrial Area, north bank": (u"Boulevard Trade and Services", "8C8A4E",
                                     u"OSM in its part of site_alan: no landuse=industrial (6,282 m2 commercial only), 47 "
                                     u"buildings with median 223 m2 (south 1,143 m2); on Adnan Menderes Bulvari: farm supply "
                                     u"shops (Akguller Un-Yem sales point, Endal Tarim), the District Agriculture and Forestry "
                                     u"office, car dealers, vets, a wholesale market; the south bank holds 206,660 m2 "
                                     u"landuse=industrial and Bergama 1. and 2. Sanayi Sitesi"),
    u"Industrial Area, south bank": (u"Industrial Area", None, u"the one industrial part (see the north bank)")}
AREA_DARK = 0.15                                 # v2.28: the blob = the area colour this much toward black
AREA_PPM = 5.0                                   # v2.28: blob pixels a mm
for _k, _n in (("N2", "2"), ("N3", "3"), ("N4", "4"), ("N5", "5"), ("N6", "6")):   # v2.28: tags in their area's tone
    _c = AREA_COL[_n]
    NODE_COL[_k] = "%02X%02X%02X" % tuple(int(int(_c[i:i + 2], 16) * 0.55) for i in (0, 2, 4))
MP_ROWS = [(u"terraces (proposed)", ("teras_-_canopy/teras",)), (u"canopy (proposed)", ("teras_-_canopy/kanopi",)),
           (u"walks (proposed)", ("yuruyus",)), (u"bridges (proposed)", ("kopruler",)),
           (u"designs (proposed)", ("desings",)), (u"retaining walls (proposed)", ("istinaat",)),
           (u"cycle route (proposed)", ("bisiklet",))]   # the layer names as the nodes pages use them
MP_STYLE = {"area": {}, "fill": {}, "stroke": {}}   # v2.37: Aras 14:44 "use the masterplan svg as it is for that map"
MP_STYLE_V213 = {   # v2.13 (not used since v2.37): the proposal in the accent family (DIAGRAM_STYLE: C07A2E = our intervention); key words of the layers
    "area": {"kopruler": "A8641F", "teras": "D9A46A", "kanopi": "F2DCC0"},
    "fill": {"kopruler": "A8641F", "teras": "D9A46A", "kanopi": "F2DCC0", "iskele_kenari": "C07A2E", "normal": "C07A2E", "circulation": "C07A2E", "desings": "E6BE8E"},
    "stroke": {"teras": "A8641F", "kanopi": "C07A2E", "desings": "A8641F", "istinaat": "7A3E0C", "kopruler": "8F4E14",
               "normal": "C07A2E", "iskele_kenari": "C07A2E", "circulation": "C07A2E"}}
NODE_INFO = {   # v2.35: library/node_ideas_2026-11-15/NODE_IDEAS.md (15 Nov); areas = estimates (EST.), no source
    "N1": dict(idea=u"a neighbourhood house for both banks · a waiting room for the village buses",
               story=u"The oldest riverbank: Hellenistic embankment · Roman bank wall at Eski Kozak Cd",
               bld=u"neighbourhood house ~500 m² proposed: hall 200 · kitchen 80 · 3 workshops · children 60 · tool / seed library 40",
               links=u"Kozak Cd, Tekkeboğazı Sk stops · village lines 831-833"),
    "N2": dict(story=u"1,800 years of one crossing: Roman bridge 2nd-3rd c AD · Ulu Cami 1398-99 · Tabaklar Hamamı",
               bld=u"heritage walk point ~400 m² proposed: exhibition 250 · info 40 · café 80 · lookout",
               links=u"K4 walk hub · heritage loop stop 4 · Camikebir Cd (831-833)"),
    "N3": dict(idea=u"show the hidden stream, no opening (Roman tunnels): viewing steps at the tunnel mouth · a water line in the İstiklal paving",
               story=u"The river under the market: Tabak Köprüsü · tanneries · Hacı Hekim arasta 1513",
               bld=u"craft + produce hall ~850 m² proposed: market 600 · 3 workshops · arrival + WC 60",
               links=u"K3 walk hub · İstiklal transit hub · loop stops 3, 5 · Yıldız Garajı"),
    "N4": dict(story=u"The temple that stands on the river: Kızıl Avlu over the Selinos · Üç Kemer Roman bridge",
               bld=u"raised canopy platform on the north bank, no contact with the monument",
               links=u"Kızıl Avlu transit hub · K5 walk hub · loop stop 2 · lines 651-653, 656"),
    "N5": dict(idea=u"where the town meets the plain: courts on the dry terraces",
               story=u"Üç Kemer, the last stone bridge before the plain · 1861 ginning factory",
               bld=u"day-care + sports pavilion ~280 m² proposed: day-care 150 · changing / WC 100 · store 30",
               links=u"Üç Kemer, Akasya, Cumhuriyet Lisesi stops · lines 651-653, 656"),
    "N6": dict(idea=u"water-enrichment research + education centre, open to everyone, with DEÜ Bergama MYO",
               story=u"The gateway: industry, the plain and the school meet",
               bld=u"~1,560 m² proposed: labs 160 · pilot line 150 · canteen 200 · display hall 250 · greenhouse 400 + trial plots",
               links=u"K6 gateway hub · Bergama Sanayi, İlçe Tarım stops · lines 651-653, 656 + regional 643, 644, 836, 936")}
IDEAS = {   # Aras's two marks (thread "Develop building function ideas", 14 Nov 15:13-15:16 UTC); the others still open
    "N2": u"stepped gathering terraces into the river by the Roman bridge · a split ramp down to the water",
    "N4": u"gathering where the stream leaves the Roman tunnels · a route on top · a raised gathering point"}
MB_LAYERS = {"ground", "lc", "areas", "parks", "contours", "streets", "water", "walls", "buildings", "bridges", "trees"}
# MapBase layers: all but "veg" (the 2023 satellite cover stops inside this frame at x 29521 / y 32880: a seam; as Transit v2.5)
NODE_C = "4C2528"                    # node frames (palette 4C2528)
PLACE_C = "C07A2E"                   # the project's places (proposal orange, as the spine)
GLY = dict(structure="CFC8BA", water="A2B6B5", water_light="CFDBE4", water_deep="5C7A86", green="3C4733",
           ink2="6E675E", accent="C07A2E")
WHO = dict(L=u"residents", T=u"visitors", S=u"students")
GROWS = dict(W=u"water", E=u"stream edge", A=u"agriculture", H=u"heritage")
# CityLink v13 HUBS (L12875) and FUNCS (L686), names resolved through its names table (bergama_city_link_data.py)
HUBS = [
    dict(code="K4", pts=("K4",), kind="walk", role=u"Ulucami + Tabaklar Hamamı",
         trips=u"today 831-833 only · 2-3 trips a day each way",
         later=u"later step: a town line (e.g. 651) extended to Ulucami Önü", places=(7, 1)),
    dict(code="K3", pts=("K3",), kind="walk", role=u"the tanning reach: craft",
         trips=u"831-833 only · 2-3 trips a day each way", places=(6, 2)),
    dict(code="T", pts=("IST", "RED"), kind="hidden", role=u"the covered reach",
         trips=u"651: 54 departures a weekday, every 15-20 min", places=(3, 4)),
    dict(code="K5", pts=("K5",), kind="walk", role=u"producers' market",
         trips=u"656: 12 a weekday · 831-833: 2-3", places=(5,)),
    dict(code="K6", pts=("K6",), kind="gateway", role=u"gateway out of town",
         trips=u"643 644 651 652 653 656 836 936", places=()),
]
CH = dict(K4=467, K3=709, K5=1126, K6=1767)      # chainage m (h02 card s62, CityLink v13 L764)
PLACES = {
    1: dict(name=u"Bank bazaar", xy=(29890.4, 32243.6), who="LT", grows="HE",
            kw=(u"Ottoman bazaar on this bank: Papuçcular Arastası", u"stalls bring it back")),
    2: dict(name=u"Parchment and leather workshops", xy=(30062.0, 32106.0), who="TSL", grows="H",
            kw=(u"tanning named the stream · last master died 2026", u"teach and sell the craft")),
    3: dict(name=u"Junction square", xy=(30058.0, 32047.0), who="LTS", grows="WEH",
            kw=(u"the one place the main road meets the stream", u"a slot: view down to the water strip")),
    4: dict(name=u"Kızıl Avlu water terrace", xy=(30238.7, 31931.2), who="TL", grows="HW",
            kw=(u"Kızıl Avlu reopens: target 2026", u"its visitors step out onto the stream")),
    5: dict(name=u"Producers' market", xy=(30294.0, 31792.0), who="LT", grows="A",
            kw=(u"food from fields on our stored water · olive oil", u"Wednesdays · town producers' market: Saturdays")),
    6: dict(name=u"Study terraces", xy=(29941.0, 32200.0), who="SL", grows="EW",
            kw=(u"shaded seats by the water strip", u"for students · out of the street noise")),
    7: dict(name=u"Clean-water classroom", xy=None, ch=200, who="SL", grows="W",
            kw=(u"the cleaning basins as a lesson", u"how the stream works")),
}
KEYS = {"walk": [(u"DRY HUB", True), (u"street level", False), (u"SUB-HUB in the bed", True),
                 (u"open Jul-Sep · shut in floods", False)],
        "hidden": [(u"HIDDEN STREAM SQUARE", True), (u"water line in the paving over the culvert", False),
                   (u"KIZIL AVLU TUNNEL MOUTHS", True), (u"a viewing edge", False)],
        "gateway": [(u"GATEWAY OUT", True), (u"no hub square", False)]}
WORD = {"walk": u"walking hub", "transit": u"MAIN TRANSIT HUB", "gateway": u"gateway"}


def load_common():
    p = os.path.join(BERGAMA_ROOT, COMMON)
    if not os.path.isfile(p):
        raise RuntimeError(u"%s missing: run Bergama.bat once (the kit copies it), then press again" % p)
    ns = {"__name__": "bergama_pages_common"}
    with open(p, encoding="utf-8") as f:
        exec(compile(f.read(), p, "exec"), ns)
    return ns


def no_src(t):
    """v1.3: a legend text without its brackets (the sources) and without repeated parts"""
    out = []
    for part in t.split(u" · "):
        part = re.sub(r"\s*\([^)]*\)", u"", part).strip(u" ;,")
        if part and part.lower() not in [o.lower() for o in out]:
            out.append(part)
    return u" · ".join(out)


def pip(x, y, R):
    c = False
    for (x1, y1), (x2, y2) in zip(R, R[1:] + R[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


def soft_poly(R, colour, alpha, layer, clip, ppm=4.0):
    """a semi-transparent area: the ring R (page mm) as a flat colour through an 8-bit mask ("soft" item of the
    Basemap writer, PDF and SVG), ppm pixels a mm"""
    x0, y0 = min(p[0] for p in R), min(p[1] for p in R)
    x1, y1 = max(p[0] for p in R), max(p[1] for p in R)
    pw, ph = max(1, int(math.ceil((x1 - x0) * ppm))), max(1, int(math.ceil((y1 - y0) * ppm)))
    a = int(round(255 * alpha))
    out = bytearray()
    E = list(zip(R, R[1:] + R[:1]))
    for j in range(ph):                                  # top row first
        y = y1 - (j + 0.5) / ppm
        xs = sorted(p[0] + (y - p[1]) * (q[0] - p[0]) / (q[1] - p[1]) for p, q in E if (p[1] > y) != (q[1] > y))
        row = bytearray(pw)
        for i in range(0, len(xs) - 1, 2):
            i0 = max(0, int(round((xs[i] - x0) * ppm)))
            i1 = min(pw, int(round((xs[i + 1] - x0) * ppm)))
            row[i0:i1] = bytes([a]) * max(0, i1 - i0)
        out += row
    return ("soft", zlib.compress(bytes(out), 9), pw, ph, x0, y0, pw / ppm, ph / ppm, colour, None, layer, clip)


def mp_swatch(ns, C, prefixes):
    """the colour a masterplan group is drawn in (its first piece): ("area", fill, stroke) / ("line", stroke, None);
    v2.13: through MP_STYLE, as mp_draw draws it"""
    word = lambda key, d_: next((v for w_, v in d_.items() if w_ in key.split("/")), None)
    line_ = None
    for pre in prefixes:
        for key in ns["mp_keys"](C, pre):
            for kind, fill, stroke, w, P in C["layers"][key]:
                if kind == "a":
                    fill = word(key, MP_STYLE["area"]) or fill
                fill = word(key, MP_STYLE["fill"]) or fill
                stroke = word(key, MP_STYLE["stroke"]) or stroke
                if kind == "a" and fill:
                    return ("area", fill, None)
                if kind == "a":
                    return ("area", next((v for wd, v in ns["AREA_FILL"].items() if wd in key.split("/")),
                                         ns["AREA_DEFAULT"]), None)
                if kind == "r" and (fill or stroke):
                    return ("area", fill, stroke)
                if kind == "l" and stroke and not line_:
                    line_ = ("line", stroke, None)       # v2.21: an area piece first, a line only if none
    return line_


# ================================================================ v2.4: areas that follow the fabric, neighbourhoods
def fill_ring(g, W, H, gx0, gy1, ppm, R, val):
    """scanline fill of the ring R (page mm) into the byte grid g (W x H, row 0 at the top edge gy1)"""
    if len(R) < 3:
        return
    ys = [p[1] for p in R]
    j0, j1 = max(0, int((gy1 - max(ys)) * ppm)), min(H - 1, int((gy1 - min(ys)) * ppm) + 1)
    E = list(zip(R, R[1:] + R[:1]))
    for j in range(j0, j1 + 1):
        y = gy1 - (j + 0.5) / ppm
        xs = sorted(p[0] + (y - p[1]) * (q[0] - p[0]) / (q[1] - p[1]) for p, q in E if (p[1] > y) != (q[1] > y))
        b = j * W
        for a_ in range(0, len(xs) - 1, 2):
            i0, i1 = max(0, int(round((xs[a_] - gx0) * ppm))), min(W, int(round((xs[a_ + 1] - gx0) * ppm)))
            if i1 > i0:
                g[b + i0:b + i1] = bytes([val]) * (i1 - i0)


def dilate(g, W, H, r):
    """binary dilation by a (2r+1) square (two running sums)"""
    t = bytearray(W * H)
    for j in range(H):
        c = [0]
        for v in g[j * W:(j + 1) * W]:
            c.append(c[-1] + (1 if v else 0))
        for i in range(W):
            if c[min(W, i + r + 1)] - c[max(0, i - r)]:
                t[j * W + i] = 1
    o = bytearray(W * H)
    for i in range(W):
        c = [0]
        for j in range(H):
            c.append(c[-1] + t[j * W + i])
        for j in range(H):
            if c[min(H, j + r + 1)] - c[max(0, j - r)]:
                o[j * W + i] = 1
    return o


def comps(g, W, H, keep=False):
    """v2.16: the number of 4-connected pieces of g; keep=True: a grid of only the largest piece"""
    lab = [0] * (W * H)
    n, sizes = 0, [0]
    for s0 in range(W * H):
        if g[s0] and not lab[s0]:
            n += 1
            lab[s0], st, c = n, [s0], 0
            while st:
                i = st.pop()
                c += 1
                x, y = i % W, i // W
                for j in ((i - 1) if x > 0 else -1, (i + 1) if x < W - 1 else -1, (i - W) if y > 0 else -1,
                          (i + W) if y < H - 1 else -1):
                    if j >= 0 and g[j] and not lab[j]:
                        lab[j] = n
                        st.append(j)
            sizes.append(c)
    if not keep:
        return n
    big = max(range(1, n + 1), key=lambda m: sizes[m]) if n else 0
    return bytearray(1 if lab[i] == big and big else 0 for i in range(W * H))


def fill_holes(g, W, H):
    """v2.16: every empty pixel not reached from the grid's border becomes part of the area"""
    out = bytearray(1 for _ in range(W * H))
    st = [i for i in range(W * H) if (i % W in (0, W - 1) or i // W in (0, H - 1)) and not g[i]]
    for i in st:
        out[i] = 0
    while st:
        i = st.pop()
        x, y = i % W, i // W
        for j in ((i - 1) if x > 0 else -1, (i + 1) if x < W - 1 else -1, (i - W) if y > 0 else -1,
                  (i + W) if y < H - 1 else -1):
            if j >= 0 and out[j] and not g[j]:
                out[j] = 0
                st.append(j)
    return out


def erode(g, W, H, r):
    inv = bytearray(0 if v else 1 for v in g)
    return bytearray(0 if v else 1 for v in dilate(inv, W, H, r))


def soft_grid(vals, W, H, gx0, gy1, ppm, colour, layer, clip):
    """a byte grid of opacities (row 0 at the top) as a Basemap-writer "soft" item"""
    return ("soft", zlib.compress(bytes(vals), 9), W, H, gx0, gy1 - H / ppm, W / ppm, H / ppm, colour, None, layer, clip)


def smooth_mask(g, W, H, r=2):
    """v2.40 (Aras 15:15: the area edge stair-stepped): every pixel near an edge of the 0/255 mask becomes the mean of
    its (2r+1)^2 window, so the edge fades over about half a millimetre instead of stepping pixel by pixel"""
    near = set()
    for i in range(W * H):
        v = g[i]
        x = i % W
        if (x < W - 1 and g[i + 1] != v) or (i + W < W * H and g[i + W] != v):
            near.add(i)
    if not near:
        return g
    out = bytearray(g)
    n2 = (2 * r + 1) ** 2
    done = set()
    for i in near:
        x0, y0 = i % W, i // W
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                x, y = x0 + dx, y0 + dy
                if 0 <= x < W and 0 <= y < H:
                    j = y * W + x
                    if j in done:
                        continue
                    done.add(j)
                    t = 0
                    for ey in range(-r, r + 1):
                        yy = min(H - 1, max(0, y + ey)) * W
                        for ex in range(-r, r + 1):
                            t += g[yy + min(W - 1, max(0, x + ex))]
                    out[j] = t // n2
    return out


def area_gradient(okg, tg, order, W, H, gx0, gy1, mixh, log, F=4, R=6):
    """v2.44 (Aras 16:00 "make those gradient, like one gradient swatch should follow along the river and colors should
    fade in and out", "this way it'll look a single fill"): each area's share of every F x F pixel block, blurred (box R
    blocks, 3 passes, about 5 mm), only among the areas of the block's own bank (the river keeps the banks apart); the
    areas laid one over the other with opacity w_i / (w_1 + ... + w_i), which composites to the weighted mean of their
    colours: one fill whose colours fade into each other; its edge on the river and the working area kept (smoothed)"""
    n = len(order)
    Wl, Hl = (W + F - 1) // F, (H + F - 1) // F
    acc = [[0.0] * (Wl * Hl) for _ in range(n)]
    bk = [[0, 0] for _ in range(n)]
    for i in range(W * H):
        v = okg[i]
        if v:
            acc[v - 1][(i // W // F) * Wl + (i % W) // F] += 1.0
            bk[v - 1][tg[i]] += 1
    abank = [0 if b[0] >= b[1] else 1 for b in bk]
    lbank = bytearray(Wl * Hl)
    for j in range(Wl * Hl):
        x_, y_ = min(W - 1, (j % Wl) * F + F // 2), min(H - 1, (j // Wl) * F + F // 2)
        lbank[j] = tg[y_ * W + x_]

    def blur(a):
        for _ in range(3):
            b = [0.0] * (Wl * Hl)
            for y_ in range(Hl):
                o, s_ = y_ * Wl, 0.0
                row = a[o:o + Wl]
                for x_ in range(min(R, Wl)):
                    s_ += row[x_]
                for x_ in range(Wl):
                    if x_ + R < Wl:
                        s_ += row[x_ + R]
                    if x_ - R - 1 >= 0:
                        s_ -= row[x_ - R - 1]
                    b[o + x_] = s_
            c = [0.0] * (Wl * Hl)
            for x_ in range(Wl):
                s_ = 0.0
                for y_ in range(min(R, Hl)):
                    s_ += b[y_ * Wl + x_]
                for y_ in range(Hl):
                    if y_ + R < Hl:
                        s_ += b[(y_ + R) * Wl + x_]
                    if y_ - R - 1 >= 0:
                        s_ -= b[(y_ - R - 1) * Wl + x_]
                    c[y_ * Wl + x_] = s_
            a = c
        return a
    wts = [blur(a) if any(a) else a for a in acc]
    m = smooth_mask(bytearray(255 if v else 0 for v in okg), W, H)   # the fill's own edge, smoothed
    cum = [0.0] * (Wl * Hl)
    out = []
    for k_ in range(n):
        w = wts[k_]
        al = bytearray(W * H)
        on = 0
        for j in range(Wl * Hl):
            if w[j] <= 0.0 or lbank[j] != abank[k_]:
                continue
            cum[j] += w[j]
            a8 = w[j] / cum[j]
            x0_, y0_ = (j % Wl) * F, (j // Wl) * F
            for y_ in range(y0_, min(H, y0_ + F)):
                o = y_ * W
                for x_ in range(x0_, min(W, x0_ + F)):
                    if m[o + x_]:
                        al[o + x_] = int(m[o + x_] * a8 + 0.5)
                        on += 1
        if on:
            a_ = order[k_]
            out.append(soft_grid(al, W, H, gx0, gy1, AREA_PPM, mixh(AREA_COL.get(a_, "B3B1AB"), "000000", AREA_DARK),
                                 "area_blobs", "map"))
    log.append(u"areas: one gradient fill, %d layers (blocks %d px, blur %d blocks x 3, banks apart)" % (len(out), F, R))
    return out


def cen_of(R):
    return (sum(p[0] for p in R) / len(R), sum(p[1] for p in R) / len(R))


def read_work(G, log):
    """v2.33: our working area = the Basemap study-area cache's "calisma" rings (survey m), as pc_study draws them"""
    p = os.path.join(G["pc_root"](), G["PC_STUDY_CACHE"])
    if not os.path.isfile(p):
        return []
    with open(p, encoding="utf-8") as f:
        cal = json.load(f).get("calisma") or []
    log.append(u"areas: working area = %d study-area ring(s) from %s; the areas are drawn outside it" % (len(cal), p))
    return cal


def read_heritage_osm(lib, log):
    """v2.32: OpenStreetMap heritage of the kit's OSM file: [(x, y survey, name, what)] for historic=*, heritage=*,
    amenity=place_of_worship, tourism=museum / attraction (nodes, and ways at their mean point)"""
    import xml.etree.ElementTree as ET
    src = os.path.join(BERGAMA_ROOT, "Data", "bergama_osm.osm")
    if not os.path.isfile(src):
        log.append(u"FLAG areas: %s missing: no heritage check" % src)
        return []
    want = lambda tg: (tg.get("historic") or tg.get("heritage") or tg.get("amenity") == "place_of_worship"
                       or tg.get("tourism") in ("museum", "attraction"))
    what = lambda tg: u"/".join(v for v in (tg.get("historic") and u"historic=" + tg["historic"],
                                            tg.get("heritage") and u"heritage=" + tg["heritage"],
                                            tg.get("amenity") == "place_of_worship" and u"place of worship",
                                            tg.get("tourism") in ("museum", "attraction") and tg["tourism"]) if v)
    to_s, nodes, out = lib["to_survey"], {}, []
    for ev, el in ET.iterparse(src, events=("end",)):
        if el.tag == "node":
            try:
                ll = (float(el.get("lon")), float(el.get("lat")))
            except (TypeError, ValueError):
                el.clear()
                continue
            nodes[el.get("id")] = ll
            tg = dict((t.get("k"), t.get("v")) for t in el.findall("tag"))
            if tg and want(tg):
                out.append(to_s(*ll) + (tg.get("name") or u"(no name, node %s)" % el.get("id"), what(tg)))
            el.clear()
        elif el.tag == "way":
            tg = dict((t.get("k"), t.get("v")) for t in el.findall("tag"))
            if tg and want(tg):
                P = [to_s(*nodes[n.get("ref")]) for n in el.findall("nd") if n.get("ref") in nodes]
                if P:
                    out.append((sum(q[0] for q in P) / len(P), sum(q[1] for q in P) / len(P),
                                tg.get("name") or u"(no name, way %s)" % el.get("id"), what(tg)))
            el.clear()
    log.append(u"areas: %d OpenStreetMap heritage features read for the area check" % len(out))
    return out


def area_profile(Z, order, lab, W, H, gx0, gy1, T, M, C, area_of, inmap, her, mixh, log):
    """v2.32: what each area is, calculated (logged only): buildings, recorded floors, fabric, shops, terrain, heritage"""
    zt = None
    try:
        with open(os.path.join(BERGAMA_ROOT, DEM_FILE), encoding="utf-8") as f:
            J = json.load(f)
        nr, nc, P = int(J["rows"]), int(J["cols"]), J["pts"]
        Zg = [[q[2] for q in P[r * nc:(r + 1) * nc]] for r in range(nr)]
        g0, gdx, gdy = P[0], (P[nc - 1][0] - P[0][0]) / float(nc - 1), (P[(nr - 1) * nc][1] - P[0][1]) / float(nr - 1)

        def zt(x, y):
            fi = min(nc - 1.000001, max(0.0, (x - g0[0]) / gdx))
            fj = min(nr - 1.000001, max(0.0, (y - g0[1]) / gdy))
            i, j = int(fi), int(fj)
            a, b = fi - i, fj - j
            return (Zg[j][i] * (1 - a) + Zg[j][i + 1] * a) * (1 - b) + (Zg[j + 1][i] * (1 - a) + Zg[j + 1][i + 1] * a) * b
    except Exception as ex:
        log.append(u"areas: no terrain for the profile (%s)" % ex)
    bx = C.get("bld_x") or []
    lab_at = lambda q: lab[min(H - 1, max(0, int((gy1 - q[1]) * AREA_PPM))) * W + min(W - 1, max(0, int((q[0] - gx0) * AREA_PPM)))]
    for n_, a_ in enumerate(order):
        mine = [i for i in inmap if area_of.get(i) == a_]
        if not mine:
            continue
        fl = sorted(float(bx[i][0]) for i in mine if i < len(bx) and bx[i] and float(bx[i][0] or 0) > 0)
        fab, com = {}, 0
        for i in mine:
            fab[C["bld"][i][1]] = fab.get(C["bld"][i][1], 0) + 1
            com += 1 if C["bld"][i][2] else 0
        top2 = sorted(fab.items(), key=lambda kv: -kv[1])[:3]
        el = sl = u"-"
        if zt:
            cs = [cen_of(C["bld"][i][0]) for i in mine]
            zs = [zt(*c_) for c_ in cs]
            sls = [math.hypot(zt(c_[0] + 15.0, c_[1]) - zt(c_[0] - 15.0, c_[1]), zt(c_[0], c_[1] + 15.0) - zt(c_[0], c_[1] - 15.0))
                   / 30.0 * 100.0 for c_ in cs]
            el, sl = u"%.0f m" % (sum(zs) / len(zs)), u"%.0f %%" % (sum(sls) / len(sls))
        hh = [h for h in her if M.inside(T(h[:2])) and lab_at(T(h[:2])) == n_ + 1]
        log.append(u"area profile %s: %d buildings; floors recorded for %d (median %s, 3+ floors %s); fabric %s; shop "
                   u"buildings %d (%.0f %%); terrain at its buildings: mean %s above sea, mean slope %s (GLO-30, 15 m "
                   u"steps); OSM heritage %d%s: %s" % (
                       Z["areas"][a_]["name"], len(mine), len(fl), (u"%.0f" % fl[len(fl) // 2]) if fl else u"-",
                       (u"%.0f %%" % (100.0 * sum(1 for v in fl if v >= 3) / len(fl))) if fl else u"-",
                       u", ".join(u"%s %.0f %%" % (k_, 100.0 * v / len(mine)) for k_, v in top2), com,
                       100.0 * com / len(mine), el, sl, len(hh), u" (first 8 listed)" if len(hh) > 8 else u"",
                       u"; ".join(u"%s (%s)" % (h[2], h[3]) for h in hh[:8]) or u"none"))


def area_layer(M, T, k, C, mixh, log, sel=None, her=None, work=None):
    """v2.31 (Aras 14:17 UTC "fill the empty areas aswell", "make them look a whole"): the map split whole among
    Aras's areas: each area's ring painted, then every other map pixel given to the nearest ring (a fill outward from
    all rings at once), so the areas meet edge to edge with no blank ground; the river left open. Every building
    takes the area of the pixel under its middle (the same split, so a building never stands on another area's
    patch). Returns (blob items, building items, {building index: key}, Z)"""
    with open(os.path.join(BERGAMA_ROOT, AREA_FILE), encoding="utf-8") as f:
        Z = json.load(f)
    order = [a for a in Z["order"] if a in Z["areas"]]
    gx0, gy1 = M.box[0], M.box[3]
    W, H = int(math.ceil((M.box[2] - M.box[0]) * AREA_PPM)), int(math.ceil((M.box[3] - M.box[1]) * AREA_PPM))
    lab = bytearray(W * H)
    for n_, a_ in enumerate(order):
        fill_ring(lab, W, H, gx0, gy1, AREA_PPM, [T(tuple(p)) for p in Z["areas"][a_]["ring"]], n_ + 1)
    if not any(lab):
        log.append(u"FLAG areas: no area ring falls on the map")
        return [], [], {}, Z
    tg = bytearray(W * H)                                # v2.31: 1 = the side of the stream at the top of the page
    if sel and len(sel) > 1:
        sel = sel if sel[0][0] <= sel[-1][0] else sel[::-1]
        fill_ring(tg, W, H, gx0, gy1, AREA_PPM, [(M.box[0] - 5.0, sel[0][1])] + list(sel) + [
            (M.box[2] + 5.0, sel[-1][1]), (M.box[2] + 5.0, M.box[3] + 5.0), (M.box[0] - 5.0, M.box[3] + 5.0)], 1)
    ring_cnt = dict((n_, [0, 0]) for n_ in range(1, len(order) + 1))
    for i in range(W * H):
        if lab[i]:
            ring_cnt[lab[i]][tg[i]] += 1
    st = [i for i in range(W * H) if lab[i]]
    while st:                                            # the nearest ring, grown one pixel a step
        nx_ = []
        for i in st:
            v_, x, y = lab[i], i % W, i // W
            for j in ((i - 1) if x > 0 else -1, (i + 1) if x < W - 1 else -1, (i - W) if y > 0 else -1,
                      (i + W) if y < H - 1 else -1):
                if j >= 0 and not lab[j]:
                    lab[j] = v_
                    nx_.append(j)
        st = nx_
    if sel and len(sel) > 1:                             # v2.31 (Aras 14:18-14:19 "divide the settled housings into
        # two", "... industrial areas into two", "dont make areas to cross across river"): an area whose own ring lies
        # on both banks, and Settled Housing and Industrial Area (Aras), become two, one per bank; the others keep
        # to their ring's bank (what they reach across the river goes to that bank's areas)
        c0_, c1_ = T((30000.0, 32000.0)), T((30000.0, 32100.0))
        bank = (u"south", u"north") if c1_[1] > c0_[1] else (u"north", u"south")   # bank[tg]: survey north up the page?
        min_px = 0.01 * W * H                            # a part under 1 % of the map is a sliver: given to its bank
        for n_ in range(1, len(order) + 1):
            key = order[n_ - 1]
            cnt = [0, 0]
            for i in range(W * H):
                if lab[i] == n_:
                    cnt[tg[i]] += 1
            rc = ring_cnt[n_]
            two = key in SPLIT_AREAS or (sum(rc) and min(rc) >= 0.1 * sum(rc))
            if two and min(cnt) >= min_px:
                big = 0 if cnt[0] >= cnt[1] else 1
                nm0 = Z["areas"][key]["name"]
                order.append(key + "b")
                Z["areas"][key + "b"] = dict(Z["areas"][key], name=u"%s, %s bank" % (nm0, bank[1 - big]))
                Z["areas"][key] = dict(Z["areas"][key], name=u"%s, %s bank" % (nm0, bank[big]))
                nb_ = len(order)
                for i in range(W * H):
                    if lab[i] == n_ and tg[i] != big:
                        lab[i] = nb_
                log.append(u"areas: %s split at the Selinos (%s bank %.0f %%, %s bank %.0f %% of it)" % (
                    nm0, bank[big], 100.0 * cnt[big] / sum(cnt), bank[1 - big], 100.0 * cnt[1 - big] / sum(cnt)))
            elif min(cnt) > 0:
                sm = (0 if cnt[0] < cnt[1] else 1) if two or not sum(rc) else (0 if rc[0] < rc[1] else 1)
                for i in range(W * H):
                    if lab[i] == n_ and tg[i] == sm:
                        lab[i] = 0
                log.append(u"areas: %s's part across the Selinos (%d px) given to that bank's areas" % (
                    Z["areas"][key]["name"], cnt[sm]))
        st = [i for i in range(W * H) if lab[i]]
        while st:                                        # the slivers refilled from their own bank only
            nx_ = []
            for i in st:
                v_, x, y = lab[i], i % W, i // W
                for j in ((i - 1) if x > 0 else -1, (i + 1) if x < W - 1 else -1, (i - W) if y > 0 else -1,
                          (i + W) if y < H - 1 else -1):
                    if j >= 0 and not lab[j] and tg[j] == tg[i]:
                        lab[j] = v_
                        nx_.append(j)
            st = nx_
    Z["order"] = order
    rv = bytearray(W * H)
    for Rr in (C.get("polys") or {}).get("river", []):
        fill_ring(rv, W, H, gx0, gy1, AREA_PPM, [T(p) for p in Rr], 1)
    area_of, inmap = {}, set()
    for i, (Rb, fab_, com, src, nm) in enumerate(C["bld"]):
        if len(Rb) < 3:
            continue
        q_ = T(cen_of(Rb))
        ii, jj = int((q_[0] - gx0) * AREA_PPM), int((gy1 - q_[1]) * AREA_PPM)
        if not (M.box[0] - 30.0 <= q_[0] <= M.box[2] + 30.0 and M.box[1] - 30.0 <= q_[1] <= M.box[3] + 30.0):
            continue                                     # far off the map: not on this slide (axos sit in the map)
        ii, jj = min(W - 1, max(0, ii)), min(H - 1, max(0, jj))
        area_of[i] = order[lab[jj * W + ii] - 1]
        if M.inside(q_):
            inmap.add(i)
    area_profile(Z, order, lab, W, H, gx0, gy1, T, M, C, area_of, inmap, her or [], mixh, log)   # v2.32

    def lab_ix(i):
        q_ = T(cen_of(C["bld"][i][0]))
        return min(H - 1, max(0, int((gy1 - q_[1]) * AREA_PPM))) * W + min(W - 1, max(0, int((q_[0] - gx0) * AREA_PPM)))
    for a_ in order:                                     # v2.37: a part the data does not support under its name
        rn = AREA_RENAME.get(Z["areas"][a_]["name"])
        if rn:
            log.append(u"areas: %s renamed %s (%s)" % (Z["areas"][a_]["name"], rn[0], rn[2]))
            Z["areas"][a_] = dict(Z["areas"][a_], name=rn[0])
            if rn[1]:
                AREA_COL[a_] = rn[1]
    wk = bytearray(W * H)                                # v2.33: our working area: no area colour inside it
    for R in work or []:
        fill_ring(wk, W, H, gx0, gy1, AREA_PPM, [T(tuple(q)) for q in R], 1)
    if not work:
        log.append(u"FLAG areas: no working-area ring (study area cache): the areas cover the whole map")
    blobs, blds = [], []
    Z["cent"] = {}
    for n_, a_ in enumerate(order):
        if a_ not in AREA_COL:                           # a split part with no colour of its own: its area's, darker
            AREA_COL[a_] = mixh(AREA_COL.get(a_[:-1], "B3B1AB"), "000000", 0.22)
        g = bytearray(255 if (lab[i] == n_ + 1 and not rv[i] and not wk[i]) else 0 for i in range(W * H))
        px = [i for i in range(W * H) if g[i]]
        if px:
            Z["cent"][a_] = (gx0 + (sum(i % W for i in px) / float(len(px)) + 0.5) / AREA_PPM,
                             gy1 - (sum(i // W for i in px) / float(len(px)) + 0.5) / AREA_PPM)
        mine = [i for i in inmap if area_of[i] == a_ and not wk[lab_ix(i)]]
        if not any(g):
            log.append(u"area %s: not on the map" % Z["areas"][a_]["name"])
            continue
        col = AREA_COL.get(a_, "B3B1AB")
        for i in mine:
            blds.append(("poly", [[T(p) for p in C["bld"][i][0]]], col, mixh(col, "000000", 0.35), 0.04, None,
                         "buildings_area", 1, None, "map"))
        log.append(u"area %s: %d buildings, %.0f %% of the map" % (
            Z["areas"][a_]["name"], len(mine), 100.0 * sum(1 for v in g if v) / (W * H)))
    # v2.37: where each area is (for its name): the label at a point, and a box test against any edge (summed table)
    okg = [lab[i] if (not rv[i] and not wk[i]) else 0 for i in range(W * H)]
    edge = bytearray(W * H)
    for i in range(W * H):
        x_ = i % W
        if not okg[i] or (x_ < W - 1 and okg[i + 1] != okg[i]) or (i + W < W * H and okg[i + W] != okg[i]) or \
                (x_ > 0 and okg[i - 1] != okg[i]) or (i >= W and okg[i - W] != okg[i]):
            edge[i] = 1
    sat = [0] * ((W + 1) * (H + 1))
    for y_ in range(H):
        run, b0, b1 = 0, y_ * (W + 1), (y_ + 1) * (W + 1)
        for x_ in range(W):
            run += edge[y_ * W + x_]
            sat[b1 + x_ + 1] = sat[b0 + x_ + 1] + run
    px_ = lambda q: (int((q[0] - gx0) * AREA_PPM), int((gy1 - q[1]) * AREA_PPM))

    def key_at(q):
        c_, r_ = px_(q)
        if 0 <= c_ < W and 0 <= r_ < H and okg[r_ * W + c_]:
            return order[okg[r_ * W + c_] - 1]
        return None

    def box_clear(b):                                    # b = (x0, y0, x1, y1) page mm: no area edge inside it
        c0, r1 = px_((b[0], b[1]))
        c1, r0 = px_((b[2], b[3]))
        if c0 < 0 or r0 < 0 or c1 >= W or r1 >= H:
            return False
        return sat[(r1 + 1) * (W + 1) + c1 + 1] - sat[r0 * (W + 1) + c1 + 1] - sat[(r1 + 1) * (W + 1) + c0] + \
            sat[r0 * (W + 1) + c0] == 0
    Z["key_at"], Z["box_clear"] = key_at, box_clear
    blobs = area_gradient(okg, tg, order, W, H, gx0, gy1, mixh, log)   # v2.44: one fill, colours fading into each other
    log.append(u"areas: the whole map split among %d areas (nearest ring), the river left open; %d buildings coloured"
               % (len(blobs), len(inmap)))
    return blobs, blds, area_of, Z


def node_mask(M, T, k, C, frame, log, nk):
    """v2.4 (Aras 16:19 UTC "mark the areas properly"): the node's area follows its blocks: every building and ground
    area whose middle lies in the node frame, closed over the streets between them (CLOSE_M, then back ERODE_M), plus
    the stream inside the frame; cut to the map (site_alan). Returns (grid, W, H, gx0, gy1)"""
    R = [T(p) for p in frame]
    gx0, gy0 = max(M.box[0], min(p[0] for p in R) - 4.0), max(M.box[1], min(p[1] for p in R) - 4.0)
    gx1, gy1 = min(M.box[2], max(p[0] for p in R) + 4.0), min(M.box[3], max(p[1] for p in R) + 4.0)
    W, H = max(1, int(math.ceil((gx1 - gx0) * MASK_PPM))), max(1, int(math.ceil((gy1 - gy0) * MASK_PPM)))
    gx1, gy0 = gx0 + W / MASK_PPM, gy1 - H / MASK_PPM
    xs, ys = [p[0] for p in frame], [p[1] for p in frame]
    fb = (min(xs), min(ys), max(xs), max(ys))
    infr = lambda c: fb[0] <= c[0] <= fb[2] and fb[1] <= c[1] <= fb[3] and pip(c[0], c[1], frame)
    g = bytearray(W * H)
    nb = na = 0
    for Rb, fab_, com, src, nm in C["bld"]:
        if len(Rb) >= 3 and infr(cen_of(Rb)):
            fill_ring(g, W, H, gx0, gy1, MASK_PPM, [T(p) for p in Rb], 1)
            nb += 1
    for A in C.get("areas") or []:
        if A[1] not in ("landuse", "farm", "wood") and len(A[0]) >= 3 and infr(cen_of(A[0])):
            fill_ring(g, W, H, gx0, gy1, MASK_PPM, [T(p) for p in A[0]], 1)
            na += 1
    r1, r2 = max(1, int(round(CLOSE_M * k * MASK_PPM))), max(1, int(round(ERODE_M * k * MASK_PPM)))
    g0 = g
    g = erode(dilate(g0, W, H, r1), W, H, r2)
    rv, fm = bytearray(W * H), bytearray(W * H)
    for Rr in (C.get("polys") or {}).get("river", []):
        fill_ring(rv, W, H, gx0, gy1, MASK_PPM, [T(p) for p in Rr], 1)
    fill_ring(fm, W, H, gx0, gy1, MASK_PPM, R, 1)
    for i in range(W * H):
        if rv[i] and fm[i]:
            g[i] = 1
    cm = CLOSE_M                                         # v2.16: one blob: close wider until one piece (60 m at most)
    while comps(g, W, H) > 1 and cm < 60.0:
        cm += 8.0
        r1 = max(1, int(round(cm * k * MASK_PPM)))
        r2 = max(1, int(round((cm - (CLOSE_M - ERODE_M)) * k * MASK_PPM)))
        g = erode(dilate(g0, W, H, r1), W, H, r2)
        for i in range(W * H):
            if rv[i] and fm[i]:
                g[i] = 1
    n_ = comps(g, W, H)
    if n_ > 1:
        log.append(u"%s area: still %d pieces after closing over 60 m; the largest kept" % (nk, n_))
        g = comps(g, W, H, keep=True)
    g = fill_holes(g, W, H)
    log.append(u"%s area: one piece, closed over %.0f m, holes filled" % (nk, cm))
    log.append(u"%s area: %d buildings + %d ground areas in its frame, closed over %.0f m, back %.0f m, + the stream "
               u"in the frame; %.0f %% of the frame's own surface" % (nk, nb, na, CLOSE_M, ERODE_M,
                                                                     100.0 * sum(1 for i in range(W * H) if g[i] and fm[i]) / max(1, sum(fm))))
    return g, W, H, gx0, gy1


def read_mahalle(lib, log):
    """the neighbourhoods (mahalle = OpenStreetMap administrative boundaries, admin_level 8) of the kit's OSM file:
    [(name, [survey rings])]; a ring the file cuts off is closed straight (logged)"""
    import xml.etree.ElementTree as ET
    src = os.path.join(BERGAMA_ROOT, "Data", "bergama_osm.osm")
    if not os.path.isfile(src):
        log.append(u"FLAG: %s missing: no neighbourhoods" % src)
        return []
    nodes, ways, rels = {}, {}, []
    for ev, el in ET.iterparse(src, events=("end",)):
        if el.tag == "node":
            try:
                nodes[el.get("id")] = (float(el.get("lon")), float(el.get("lat")))
            except (TypeError, ValueError):
                pass
            el.clear()
        elif el.tag == "way":
            ways[el.get("id")] = [n.get("ref") for n in el.findall("nd")]
            el.clear()
        elif el.tag == "relation":
            tg = dict((t.get("k"), t.get("v")) for t in el.findall("tag"))
            if tg.get("boundary") == "administrative" and tg.get("admin_level") == "8" and tg.get("name"):
                rels.append((tg["name"], [m.get("ref") for m in el.findall("member")
                                          if m.get("type") == "way" and m.get("role") in ("outer", "", None)]))
            el.clear()
    to_s = lib["to_survey"]
    out = []
    for name, wids in rels:
        left = [[r for r in ways[w] if r in nodes] for w in wids if w in ways]
        left = [w for w in left if len(w) >= 2]
        rings = []
        while left:
            cur = left.pop(0)
            grown = True
            while cur[0] != cur[-1] and grown:
                grown = False
                for i, w in enumerate(left):
                    if w[0] == cur[-1]:
                        cur = cur + w[1:]
                    elif w[-1] == cur[-1]:
                        cur = cur + w[::-1][1:]
                    elif w[-1] == cur[0]:
                        cur = w[:-1] + cur
                    elif w[0] == cur[0]:
                        cur = w[::-1][:-1] + cur
                    else:
                        continue
                    left.pop(i)
                    grown = True
                    break
            P = [to_s(*nodes[r]) for r in cur]
            if cur[0] != cur[-1]:
                log.append(u"neighbourhood %s: a ring cut by the file's edge closed straight across %.0f m" % (
                    name, math.hypot(P[0][0] - P[-1][0], P[0][1] - P[-1][1])))
            else:
                P = P[:-1]
            if len(P) >= 3:
                rings.append(P)
        if rings:
            out.append((name, rings))
    log.append(u"neighbourhoods (OpenStreetMap admin_level 8): %d read" % len(out))
    return out


# ================================================================ v2.8: the diagram standard (DIAGRAM_STYLE.md v1, pages_common pc_dg_kit)
def her_kind(name):
    """the heritage loop stop's silhouette (kit kinds), from its name"""
    n = name.lower()
    return "basilica" if u"kızıl avlu" in n or u"kizil avlu" in n else "mosque" if u"cami" in n else "dome"


AXO_A = 16.0                                     # v2.17: plan turned 22 degrees, depth at 0.5, heights x 2.2 (diagram)
AXO_F, AXO_Z = 0.45, 2.2
AXO_SLAB = 1.4                                   # mm, the ground slab's cut face
AXO_STEPS = ("CCA363", "B9872F", "705426", "8F6304")   # v2.22: the slide 1 axo's residential roof, lit wall, shaded
                                                       # wall, outline: its darkening steps, used on every colour
STOREY_M = 3.0                                   # Aras 12 Nov: storey height 3.0 m
AX = dict(top="F1EEE6", street="FFFFFF", side="C9C3B7", wall_l="E4E0D8", wall_r="CBC6BC", roof="FFFFFF",
          edge="8E877C", shop="8A847A", bus="3E5C76", loop="8B2D2D", water="A2B6B5", move="C07A2E",
          move_t="DDAE76", canopy="F2DCC0")


def clip_poly(P, L1, L2):
    """Sutherland-Hodgman against the box 0..L1 x 0..L2 (local m)"""
    for ax, lim, keep_lo in ((0, 0.0, True), (0, L1, False), (1, 0.0, True), (1, L2, False)):
        if not P:
            return P
        inside = (lambda p: p[ax] >= lim) if keep_lo else (lambda p: p[ax] <= lim)
        out = []
        for i in range(len(P)):
            a, b = P[i - 1], P[i]
            ia, ib = inside(a), inside(b)
            if ia != ib:
                t = (lim - a[ax]) / ((b[ax] - a[ax]) or 1e-9)
                out.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
            if ib:
                out.append(b)
        P = out
    return P


def clip_line(P, L1, L2):
    """runs of a polyline inside the box 0..L1 x 0..L2 (Liang-Barsky per segment)"""
    runs, cur = [], []
    for a, b in zip(P, P[1:]):
        t0, t1 = 0.0, 1.0
        dx, dy = b[0] - a[0], b[1] - a[1]
        ok = True
        for p_, q_ in ((-dx, a[0]), (dx, L1 - a[0]), (-dy, a[1]), (dy, L2 - a[1])):
            if p_ == 0:
                if q_ < 0:
                    ok = False
                    break
            else:
                r = q_ / p_
                if p_ < 0:
                    t0 = max(t0, r)
                else:
                    t1 = min(t1, r)
        if not ok or t0 > t1:
            if len(cur) > 1:
                runs.append(cur)
            cur = []
            continue
        A = (a[0] + t0 * dx, a[1] + t0 * dy)
        B = (a[0] + t1 * dx, a[1] + t1 * dy)
        if not cur or abs(cur[-1][0] - A[0]) > 1e-6 or abs(cur[-1][1] - A[1]) > 1e-6:
            if len(cur) > 1:
                runs.append(cur)
            cur = [A]
        cur.append(B)
        if t1 < 1.0:
            runs.append(cur)
            cur = []
    if len(cur) > 1:
        runs.append(cur)
    return runs


AXO_MODEL = os.path.join("cached", "bergama_page01_axo", "axo_model.json")   # v2.30: slide 1's axo, cut per node
DEM_FILE = os.path.join("Data", "bergama_dem_glo30.json")


def load_axo_model(log):
    """v2.30: the slide 1 axonometric (Page01Axo v3 axo_model.json) + the terrain it is draped on (its DEM code)"""
    p = os.path.join(BERGAMA_ROOT, AXO_MODEL)
    if not os.path.exists(p):
        log.append(u"FLAG node axos: %s not found (run Page01Axo v3 once): the v2.29 axonometrics drawn" % p)
        return None
    with open(p, encoding="utf-8") as f:
        AM = json.load(f)
    if not AM.get("view") or not AM.get("shapes"):
        log.append(u"FLAG node axos: %s has no view or shapes: the v2.29 axonometrics drawn" % p)
        return None
    with open(os.path.join(BERGAMA_ROOT, DEM_FILE), encoding="utf-8") as f:
        J = json.load(f)
    nr, nc, P = int(J["rows"]), int(J["cols"]), J["pts"]
    AM["dem"] = dict(Z=[[q[2] for q in P[r * nc:(r + 1) * nc]] for r in range(nr)], nr=nr, nc=nc, gx0=P[0][0],
                     gy0=P[0][1], gdx=(P[nc - 1][0] - P[0][0]) / float(nc - 1),
                     gdy=(P[(nr - 1) * nc][1] - P[0][1]) / float(nr - 1))
    log.append(u"node axos: cut from the slide 1 axonometric (%s, %d shapes; %s)" % (AM.get("version"), len(AM["shapes"]), p))
    return AM


def load_axo3d(log):
    """v2.45: Page01Axo v4.4's 3D library (everything above its AXO_LIB_END marker) and the open Rhino document, or None
    (no Rhino here, or the script is missing): then the node axonometrics stay 2D-painted"""
    try:
        import Rhino
        doc = Rhino.RhinoDoc.ActiveDoc
        if doc is None:
            return None
    except Exception:
        return None
    import glob
    fs = glob.glob(os.path.join(BERGAMA_ROOT, "scripts", "bergama_page01_axo_v4*.py"))
    if not fs:
        log.append(u"FLAG node axos 3D: no Page01Axo v4 script in %s: 2D-painted" % os.path.join(BERGAMA_ROOT, "scripts"))
        return None
    vkey = lambda f_: [int(n_) for n_ in re.findall(r"\d+", os.path.basename(f_))]
    f = sorted(fs, key=vkey)[-1]
    with open(f, encoding="utf-8") as fh:
        src = fh.read()
    mk = re.search(r"^#[^\n]*AXO_LIB_END", src, re.M)   # v2.46: the marker comment line, not the docstring's words
    cut = mk.start() if mk else -1
    if cut < 0:
        log.append(u"FLAG node axos 3D: %s has no AXO_LIB_END: 2D-painted" % f)
        return None
    src = src[:cut]
    ns = {"__name__": "bergama_axo3d_lib"}
    exec(compile(src, f, "exec"), ns)
    log.append(u"node axos 3D: library from %s" % os.path.basename(f))
    return dict(ns=ns, doc=doc)


def node_axo_3d(G, X, nk, KC, F, D3, AM, mm_m, W, H, slab_fill, log):
    """v2.45 (Aras 16:01 "foreground and background is mixed still"; Aras 14:50 "draw these in 3D with scripts in rhino
    and take the drawings from rhino"): the node's piece of the slide 1 3D model (axo_model.json d3, cut by the node's
    cut KC), its buildings in their area colours, the bus routes and the heritage loop as thin strips on the ground,
    built in the open Rhino, captured in the axo's parallel view (Page01Axo v4.4 axo3d_*), checked, registered on the
    card by the cut's edge; returns the photo (png, x, y, w, h, True) to lie under the card's vector marks, or None"""
    A3, d3 = X.get("A3"), AM.get("d3")
    if not A3 or not d3:
        return None
    ns, doc = A3["ns"], A3["doc"]
    E = AM["dem"]

    def zdem(x, y):
        fi = min(E["nc"] - 1.000001, max(0.0, (x - E["gx0"]) / E["gdx"]))
        fj = min(E["nr"] - 1.000001, max(0.0, (y - E["gy0"]) / E["gdy"]))
        i, j = int(fi), int(fj)
        a, b = fi - i, fj - j
        Z = E["Z"]
        return (Z[j][i] * (1 - a) + Z[j][i + 1] * a) * (1 - b) + (Z[j + 1][i] * (1 - a) + Z[j + 1][i + 1] * a) * b
    mixh, aof, C, D = X["ns"]["mixh"], X.get("area_of") or {}, X["C"], X["D"]
    tup = lambda R: [tuple(q[:2]) for q in R]
    cut = lambda R: ccw(clip_convex(tup(R), KC)) if len(R) >= 3 else []
    d = dict(d3)
    d["slab"] = list(KC)
    for k_ in ("parks", "streets", "water"):
        d[k_] = [r for r in (cut(R) for R in d3.get(k_) or []) if len(r) >= 3]
    for k_ in ("street_edges", "water_edges", "walls"):
        d[k_] = [r for P in d3.get(k_) or [] for r in clip_line_convex(tup(P), KC) if len(r) >= 2]
    shp = {}
    for sh in AM["shapes"]:                              # the slide 1 colours, recoloured, by group
        g_ = sh.get("grp") or u""
        if sh.get("fill") and g_.split("/")[0] not in shp:
            shp[g_.split("/")[0]] = sh["fill"]
    d["c_slab"] = slab_fill or d3.get("c_slab")
    d["c_water"] = AX["water"]
    d["c_street"] = AX["street"]
    d["c_park"] = next((v for k_, v in shp.items() if k_.startswith(u"park")), d3.get("c_park"))
    cen_b = []                                           # buildings by their footprint middle (MapBase index)
    for i_, b_ in enumerate(C["bld"]):
        if b_ and b_[0]:
            cen_b.append((cen_of(b_[0]), i_))
    grid = {}
    for q, i_ in cen_b:
        grid.setdefault((int(q[0] // 20), int(q[1] // 20)), []).append((q, i_))

    def bld_at(q):
        best, bi = 9.0, None
        for gx in (-1, 0, 1):
            for gy in (-1, 0, 1):
                for c_, i_ in grid.get((int(q[0] // 20) + gx, int(q[1] // 20) + gy), []):
                    d2 = (c_[0] - q[0]) ** 2 + (c_[1] - q[1]) ** 2
                    if d2 < best:
                        best, bi = d2, i_
        return bi
    d["blds"], nmiss = [], 0
    for P, h, cols in d3.get("blds") or []:
        Pc = cut(P)
        if len(Pc) < 3:
            continue
        b_ = bld_at(cen_of(tup(P)))
        A_ = AREA_COL.get(aof.get(b_)) if b_ is not None else None
        if not A_:
            nmiss += 1
            A_ = "B3B1AB"
        d["blds"].append((Pc, h, (A_, mixh(A_, "000000", 0.08), mixh(A_, "000000", 0.24), mixh(A_, "000000", 0.40))))
    d["trees"] = [t for t in d3.get("trees") or [] if pip(t[0], t[1], KC)]
    k_s = G["pc_stroke_k"](W, H) if "pc_stroke_k" in G else min(1.0, W / 400.0)
    m_of = lambda mm: (G["pc_stroke"](mm, k_s) if "pc_stroke" in G else mm * k_s) / max(1e-6, mm_m)
    flows = []                                           # (plan line, width m, colour, lift m)
    seen = set()
    for r_ in (D.get("routes") or {}).values():
        for wid in r_.get("ways", []):
            if wid in seen or wid not in D.get("ways", {}):
                continue
            seen.add(wid)
            for run in clip_line_convex(tup(D["ways"][wid]), KC):
                flows += [(run, m_of(1.0), "FFFFFF", 1.0), (run, m_of(0.7), AX["bus"], 1.05)]
    Hh = sorted(D["heritage"], key=lambda h_: int(h_["n"]))
    for a, b in zip(Hh, Hh[1:]):
        Pl = [a["xy"], b["xy"]]
        if {a["key"], b["key"]} == {"tabak_koprusu", "ulucami_onu"}:
            Pl = G["pc_selinos"](a["xy"], b["xy"]) or Pl
        for run in clip_line_convex(tup(Pl), KC):
            flows += [(run, m_of(1.2), "FFFFFF", 1.1), (run, m_of(0.9), AX["loop"], 1.15)]
    guids = []
    try:
        import Rhino, System
        import Rhino.Geometry as rg
        guids, bb3 = ns["axo3d_build"](doc, d, zdem, log)
        li = doc.Layers.FindByFullPath(ns["AXO3D_LAYER"], -1)
        for run, w_, col, dz in flows:                   # thin strips on the ground: a building in front hides them
            pts = dense(run, 2.0, False)
            if len(pts) < 2:
                continue
            Ms = rg.Mesh()
            for i_, q in enumerate(pts):
                a_, b_ = pts[max(0, i_ - 1)], pts[min(len(pts) - 1, i_ + 1)]
                tx, ty = b_[0] - a_[0], b_[1] - a_[1]
                L = math.hypot(tx, ty) or 1.0
                nx, ny = -ty / L * w_ / 2.0, tx / L * w_ / 2.0
                Ms.Vertices.Add(q[0] + nx, q[1] + ny, zdem(q[0] + nx, q[1] + ny) + dz)
                Ms.Vertices.Add(q[0] - nx, q[1] - ny, zdem(q[0] - nx, q[1] - ny) + dz)
                if i_:
                    k0 = 2 * i_
                    Ms.Faces.AddFace(k0 - 2, k0 - 1, k0 + 1, k0)
            Ms.Normals.ComputeNormals()
            at = Rhino.DocObjects.ObjectAttributes()
            at.LayerIndex = li
            at.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
            at.ObjectColor = System.Drawing.Color.FromArgb(int(col[0:2], 16), int(col[2:4], 16), int(col[4:6], 16))
            g = doc.Objects.AddMesh(Ms, at)
            if g != System.Guid.Empty:
                guids.append(g)
        cam = ((d3["cam_e"][0], d3["cam_e"][1], 0.0), d3["cam_up"], d3["cam_dir"])
        reg = [(q[0], q[1], zdem(q[0], q[1])) for q in dense(KC, 10.0)]
        px_w = int(max(800, min(3000, W / 25.4 * 400)))  # about 400 ppi on the card
        cdir = os.path.join(BERGAMA_ROOT, "cached", "bergama_page_spine")
        if not os.path.isdir(cdir):
            os.makedirs(cdir)
        cap, why = None, []
        for mi_, mn_ in enumerate((ns["AXO3D_MODE"], "Shaded", "Rendered")):
            png = os.path.join(cdir, u"%s_3d%s.png" % (nk, u"" if mi_ == 0 else u"_" + mn_.lower()))
            try:
                c_ = ns["axo3d_capture"](doc, cam, reg, px_w, png, log, bb3, mn_)
            except Exception as ex:
                why.append(u"%s: %s" % (mn_, ex))
                continue
            ok_, msg_ = ns["axo3d_check"](c_, log)
            log.append(u"%s 3D check, mode %s: %s%s" % (nk, mn_, msg_, u"" if ok_ else u" (rejected)"))
            if ok_:
                cap = c_
                break
            why.append(u"%s: %s" % (mn_, msg_))
        if cap is None:
            raise RuntimeError(u"no capture passed the check (" + u"; ".join(why) + u")")
        XY = [F(D3(p_[0], p_[1])) for p_, _ in cap["px"]]
        PX = [q_ for _, q_ in cap["px"]]

        def fit1(u, v):
            n_ = float(len(u))
            mu, mv = sum(u) / n_, sum(v) / n_
            a = sum((a_ - mu) * (b_ - mv) for a_, b_ in zip(u, v)) / max(1e-12, sum((a_ - mu) ** 2 for a_ in u))
            return a, mv - a * mu
        ax_, bx_ = fit1([q_[0] for q_ in PX], [r_[0] for r_ in XY])
        ay_, by_ = fit1([q_[1] for q_ in PX], [r_[1] for r_ in XY])
        res = max(max(abs(ax_ * q_[0] + bx_ - r_[0]), abs(ay_ * q_[1] + by_ - r_[1])) for q_, r_ in zip(PX, XY))
        log.append(u"%s 3D: %d buildings (%d without an area), %d trees, %d flow strips; registered on %d edge points, "
                   u"%.2f mm off at most" % (nk, len(d["blds"]), nmiss, len(d["trees"]), len(flows), len(PX), res))
        if ax_ <= 0 or ay_ >= 0 or res > 0.6:
            raise RuntimeError(u"the capture does not register on the card (%.2f mm off, scale %.4f / %.4f)"
                               % (res, ax_, ay_))
        x0_, x1_ = bx_, ax_ * cap["w"] + bx_
        y1_, y0_ = by_, ay_ * cap["h"] + by_
        return (cap["png"], x0_, y0_, x1_ - x0_, y1_ - y0_, True)
    except Exception as ex:
        log.append(u"FLAG %s 3D: %s: %s; the 2D-painted axonometric is used" % (nk, type(ex).__name__, ex))
        return None
    finally:
        if guids:
            ns["axo3d_clear"](doc, guids, log)


def axo_D(AM):
    """v2.30: survey (x, y, h above ground) -> slide 1 drawing mm, as Page01Axo's AxoView.P (bilinear DEM, >= 0)"""
    V, E = AM["view"], AM["dem"]

    def zt(x, y):
        fi = min(E["nc"] - 1.000001, max(0.0, (x - E["gx0"]) / E["gdx"]))
        fj = min(E["nr"] - 1.000001, max(0.0, (y - E["gy0"]) / E["gdy"]))
        i, j = int(fi), int(fj)
        a, b = fi - i, fj - j
        Z = E["Z"]
        z_ = (Z[j][i] * (1 - a) + Z[j][i + 1] * a) * (1 - b) + (Z[j + 1][i] * (1 - a) + Z[j + 1][i + 1] * a) * b
        return max(0.0, z_ - V["z0"])
    D_ = lambda x, y, h=0.0: (V["c0"] + V["c1"] * x + V["c2"] * y,
                              V["oy"] + V["s"] * (-V["c2"] * x + V["c1"] * y) + V["kz"] * (zt(x, y) + h))
    D_.zt = zt
    return D_


def axo_back(AM, D3):
    """v2.34: slide 1 drawing mm on the ground -> survey (x, y): Page01Axo's AxoView.back (terrain iterated)"""
    V = AM["view"]
    inv_ = V["s"] * (V["c1"] ** 2 + V["c2"] ** 2)

    def back(X, Y):
        z = 0.0
        x = y = 0.0
        for _ in range(4):
            A, B = X - V["c0"], Y - V["oy"] - V["kz"] * z
            x = (A * V["c1"] * V["s"] - V["c2"] * B) / inv_
            y = (V["c2"] * V["s"] * A + V["c1"] * B) / inv_
            z = D3.zt(x, y)
        return x, y
    return back


def dense(P, step, closed=True):
    """v2.34: points every step (survey m) along the polygon / polyline P"""
    out = []
    E = list(zip(P, P[1:] + P[:1])) if closed else list(zip(P, P[1:]))
    for a, b in E:
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
        out += [(a[0] + (b[0] - a[0]) * t / float(n), a[1] + (b[1] - a[1]) * t / float(n)) for t in range(n)]
    if not closed and P:
        out.append(tuple(P[-1]))
    return out


def ccw(P):
    return P if sum(P[i - 1][0] * P[i][1] - P[i][0] * P[i - 1][1] for i in range(len(P))) >= 0 else P[::-1]


def clip_convex(P, Cv):
    """v2.30: Sutherland-Hodgman of polygon P against the convex ccw polygon Cv"""
    out = list(P)
    for i in range(len(Cv)):
        a, b = Cv[i - 1], Cv[i]
        side = lambda q: (b[0] - a[0]) * (q[1] - a[1]) - (b[1] - a[1]) * (q[0] - a[0])
        inp, out = out, []
        for j in range(len(inp)):
            p_, q_ = inp[j - 1], inp[j]
            sp, sq_ = side(p_), side(q_)
            if sq_ >= 0:
                if sp < 0:
                    t = sp / (sp - sq_)
                    out.append((p_[0] + (q_[0] - p_[0]) * t, p_[1] + (q_[1] - p_[1]) * t))
                out.append(q_)
            elif sp >= 0:
                t = sp / (sp - sq_)
                out.append((p_[0] + (q_[0] - p_[0]) * t, p_[1] + (q_[1] - p_[1]) * t))
        if not out:
            break
    return out


def clip_line_convex(P, Cv):
    """v2.30: the runs of polyline P inside the convex ccw polygon Cv (Cyrus-Beck per segment)"""
    runs, cur = [], []
    for a, b in zip(P, P[1:]):
        t0, t1 = 0.0, 1.0
        d = (b[0] - a[0], b[1] - a[1])
        ok = True
        for i in range(len(Cv)):
            e0, e1 = Cv[i - 1], Cv[i]
            nx, ny = -(e1[1] - e0[1]), e1[0] - e0[0]       # inward normal of a ccw edge
            num = nx * (a[0] - e0[0]) + ny * (a[1] - e0[1])
            den = nx * d[0] + ny * d[1]
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
        pa = (a[0] + d[0] * t0, a[1] + d[1] * t0)
        pb = (a[0] + d[0] * t1, a[1] + d[1] * t1)
        if cur and (abs(cur[-1][0] - pa[0]) > 1e-9 or abs(cur[-1][1] - pa[1]) > 1e-9):
            runs.append(cur)
            cur = []
        if not cur:
            cur = [pa]
        cur.append(pb)
        if t1 < 1.0:
            runs.append(cur)
            cur = []
    if len(cur) > 1:
        runs.append(cur)
    return runs


def node_axo(G, K, X, nk, info, x0, y0, W, H, log):
    """v2.17 (Aras 15 Nov 06:41 UTC "god these diagrams are awful"): the node as a small axonometric of its own ground,
    from the data: the node frame as a slab with its cut face, the streets, the stream (MapBase), our move (MasterplanBase:
    terraces, canopy, walks, bridges), the bus routes that run through it (OSM route ways) and the heritage loop's legs,
    every building in it raised by its recorded floors (MapBase; unrecorded = the median of the node's recorded ones,
    logged), shop buildings with dark roofs, and pins for the hub, the loop stops and the project's places.
    The frame's long side runs left to right, turned as the map. Returns items"""
    k_body = None                                        # v2.44: where the bodies start (cut-model branch)
    use3d = False                                        # v2.45: the Rhino 3D capture drew the ground and bodies
    P_, L_, T_, circle = G["P_"], G["L_"], G["T_"], G["circle"]
    M, C, D, H_, NODES, mpns, MPC = X["M"], X["C"], X["D"], X["H"], X["NODES"], X["mpns"], X["MPC"]
    T = M.T
    cs = NODES[nk]["corners"]
    o = cs[0]
    e1, e2 = (cs[1][0] - o[0], cs[1][1] - o[1]), (cs[3][0] - o[0], cs[3][1] - o[1])
    p1 = (T(cs[1])[0] - T(o)[0], T(cs[1])[1] - T(o)[1])
    p2 = (T(cs[3])[0] - T(o)[0], T(cs[3])[1] - T(o)[1])
    if abs(p2[0]) > abs(p1[0]):                          # u = the side that runs most left-right on the map
        e1, e2, p1, p2 = e2, e1, p2, p1
    L1, L2 = math.hypot(*e1), math.hypot(*e2)
    u1, u2 = (e1[0] / L1, e1[1] / L1), (e2[0] / L2, e2[1] / L2)
    fu, fv = (1.0 if p1[0] >= 0 else -1.0), (1.0 if p2[1] >= 0 else -1.0)

    def uv(p):
        d = (p[0] - o[0], p[1] - o[1])
        u, v = d[0] * u1[0] + d[1] * u1[1], d[0] * u2[0] + d[1] * u2[1]
        return ((u if fu > 0 else L1 - u), (v if fv > 0 else L2 - v))
    ca, sa = math.cos(math.radians(AXO_A)), math.sin(math.radians(AXO_A))
    bld = []                                             # (local ring, floors, shop, fab)
    fl_known = []
    for i, (Rb, fab_, com, src, nm) in enumerate(C["bld"]):
        if len(Rb) < 3:
            continue
        c_ = uv(cen_of(Rb))
        if not (0.0 <= c_[0] <= L1 and 0.0 <= c_[1] <= L2):
            continue
        Q = clip_poly([uv(p) for p in Rb], L1, L2)
        if len(Q) < 3:
            continue
        fl = (C.get("bld_x") or [[0]] * len(C["bld"]))[i][0] if i < len(C.get("bld_x") or []) else 0
        try:
            fl = float(fl or 0)
        except (TypeError, ValueError):
            fl = 0.0
        if fl > 0:
            fl_known.append(fl)
        bld.append([Q, fl, com, (X.get("area_of") or {}).get(i, "")])   # v2.28: the area, not the fabric
    med = sorted(fl_known)[len(fl_known) // 2] if fl_known else 2.0
    n_guess = sum(1 for b in bld if not b[1])
    for b in bld:
        b[1] = b[1] or med
    hmax = max([b[1] * STOREY_M for b in bld] + [6.0])
    log.append(u"%s diagram: %d buildings (floors recorded for %d; %d drawn at the node's median %.0f); frame %.0f x %.0f m"
               % (nk, len(bld), len(bld) - n_guess, n_guess, med, L1, L2))
    # scale to the box: the slab's corners, its cut face and the tallest building (+ pins)
    pin_mm = 7.0                                         # v2.18: the hub pin; loop stops 0.75, places 0.6 of it
    has_pin = bool(info["hubs"] or info["loop"] or info["places"])
    top_mm = (pin_mm + 4.0) if has_pin else 1.0
    lay = "cards"
    it = []
    poly = lambda Q, f, st=None, w=0.0: it.append(P_([Q], f, st, w if st else 0.0, lay))
    AM = X.get("AM")
    clipP = lambda Q: clip_poly(Q, L1, L2)               # v2.34: the cut; the node frame unless the slide 1 model
    clipL = lambda Q: clip_line(Q, L1, L2)               # sets KC (frame inside site_alan)
    inK = lambda q: 0 <= q[0] <= L1 and 0 <= q[1] <= L2

    def draw_move(Pj, poly, it):
        """our move (MasterplanBase) at ground level, cut to the frame"""
        nmove = 0
        for key, recs in MPC["layers"].items():
            if not any(key == p or key.startswith(p + "/") for _, ps in MP_ROWS for p in ps):
                continue
            w_ = key.split("/")
            for kind, fill, stroke, wd, Pp in recs:
                if kind == "s" or len(Pp) < 2:
                    continue
                Qs = [uv(p) for p in Pp]
                if kind == "a" and (max(q[0] for q in Qs) - min(q[0] for q in Qs)) * (
                        max(q[1] for q in Qs) - min(q[1] for q in Qs)) > 200000.0:
                    continue
                if kind in ("r", "a") and len(Qs) >= 3:
                    Qc = clipP(Qs)
                    if len(Qc) >= 3:
                        f_ = AX["canopy"] if "kanopi" in w_ else AX["move_t"] if "teras" in w_ else AX["move"]
                        poly([Pj(u, v) for u, v in Qc], f_, AX["move"], 0.15)
                        nmove += 1
                else:
                    for run in clipL(Qs):
                        it.append(L_([Pj(u, v) for u, v in run], AX["move"], 0.45, lay))
                        nmove += 1
        return nmove
    if AM:                                               # v2.30: cut out of the slide 1 axonometric
        D3 = axo_D(AM)
        Vw = AM["view"]

        def inv(u, v):
            uu, vv = (u if fu > 0 else L1 - u), (v if fv > 0 else L2 - v)
            return (o[0] + uu * u1[0] + vv * u2[0], o[1] + uu * u1[1] + vv * u2[1])
        corners = [inv(0, 0), inv(L1, 0), inv(L1, L2), inv(0, L2)]
        # v2.34 (Aras 14:31 "use single cut plane"): ONE cut for everything = the node frame inside site_alan (the
        # slide 1 model ends at site_alan); ground, buildings, trees, slab, move, flows and pins all end on it
        KC = ccw(clip_convex(ccw(corners), ccw([tuple(q) for q in (getattr(M, "ring", None) or corners)])))
        KC = [q for i, q in enumerate(KC) if math.hypot(q[0] - KC[i - 1][0], q[1] - KC[i - 1][1]) > 0.01] or ccw(corners)
        Ku = ccw([uv(q) for q in KC])
        clipP = lambda Q: [q for q in clip_convex(list(Q), Ku)] if len(Q) >= 3 else []
        clipL = lambda Q: clip_line_convex(list(Q), Ku)
        inK = lambda q: pip(q[0], q[1], Ku)
        back = axo_back(AM, D3)
        Qd = [D3(*q) for q in dense(KC, 5.0)]
        ground, body, slab_fill, best = [], [], None, 0.0
        for sh in AM["shapes"]:
            g_ = sh.get("grp") or u""
            if g_.startswith(u"labels") or u"hatch" in g_:
                continue
            if g_.startswith(u"water") and isinstance(sh.get("fill"), str) and sh["fill"].startswith("~"):
                sh = dict(sh, fill=sh["fill"][1:])       # v2.36 (Aras 14:38): the river one flat colour
            if g_.startswith(u"slab"):
                R0 = (sh.get("rings") or [[]])[0]
                if sh.get("fill") and len(R0) >= 3:
                    a_ = abs(sum(R0[i - 1][0] * R0[i][1] - R0[i][0] * R0[i - 1][1] for i in range(len(R0))))
                    if a_ > best:
                        best, slab_fill = a_, sh["fill"]
                continue
            anc = sh.get("anchor")
            if sh.get("bld") is not None or g_.startswith(u"trees"):
                if anc and pip(anc[0], anc[1], KC):
                    body.append(sh)
                continue
            Rs = [sh.get("pts") or []] if sh.get("t") == "line" else (sh.get("rings") or [])
            xs__ = [q[0] for R_ in Rs for q in R_]
            if not xs__ or max(xs__) < min(q[0] for q in Qd) or min(xs__) > max(q[0] for q in Qd):
                continue                                 # off this node's columns of the drawing
            if sh.get("t") == "line":                    # back to the plan, cut by KC, draped again
                runs = clip_line_convex([back(*q) for q in Rs[0]], KC)
                runs = [[D3(*q) for q in dense(r_, 5.0, False)] for r_ in runs]
                if runs:
                    ground.append((sh, runs))
            else:
                rr = [clip_convex([back(*q) for q in R_], KC) for R_ in Rs]
                rr = [[D3(*q) for q in dense(R_, 5.0)] for R_ in rr if len(R_) >= 3]
                if rr:
                    ground.append((sh, rr))
        pts_ = list(Qd) + [q for _, rr in ground for R_ in rr for q in R_] + [
            tuple(q) for sh in body for R_ in (sh.get("rings") or [sh.get("pts") or []]) for q in R_]
        mnx, mxx = min(q[0] for q in pts_), max(q[0] for q in pts_)
        mny, mxy = min(q[1] for q in pts_), max(q[1] for q in pts_)
        s = min(W / (mxx - mnx), (H - AXO_SLAB - top_mm) / (mxy - mny))
        F = lambda q: (x0 + (W - s * (mxx - mnx)) / 2.0 + s * (q[0] - mnx), y0 + AXO_SLAB + s * (q[1] - mny))
        Pj = lambda u, v, z=0.0: F(D3(*inv(u, v), h=z))
        mm_m = s * Vw["k"]
        depth = lambda Q: -max(-Vw["c2"] * inv(*q)[0] + Vw["c1"] * inv(*q)[1] for q in Q)
        wmm = lambda sh: 0.7 * 0.3528 * float(sh.get("width_pt") or 0.0)
        # the slab: the draped edge of K is the one cut; faces under the edges that face the viewer (a constant band,
        # soil hatching), then the ground (the view keeps plan ccw as screen ccw: an edge running right faces us)
        Qp = [F(q) for q in Qd]
        dz = -AXO_SLAB
        for i in range(len(KC)):
            a_, b_ = KC[i - 1], KC[i]
            top_ = [F(D3(*q)) for q in dense([a_, b_], 5.0, False)]
            if top_[-1][0] - top_[0][0] <= 1e-6:
                continue
            poly(top_ + [(q[0], q[1] + dz) for q in reversed(top_)], AX["side"], "8E877C", 0.12)
            for P0, P1 in zip(top_, top_[1:]):
                Ln = math.hypot(P1[0] - P0[0], P1[1] - P0[1])
                for j in range(0, int(Ln / 0.9)):
                    t_ = (j + 0.5) * 0.9 / Ln
                    q = (P0[0] + (P1[0] - P0[0]) * t_, P0[1] + (P1[1] - P0[1]) * t_)
                    it.append(L_([(q[0], q[1] - 0.15), (q[0] - 0.9, q[1] + dz + 0.15)], "8E877C", 0.06, lay))
            it.append(L_([(q[0], q[1] + dz) for q in top_], "6E675E", 0.3, lay))
        ph_ = node_axo_3d(G, X, nk, KC, F, D3, AM, mm_m, W, H, slab_fill, log)   # v2.45: the 3D model, captured
        if ph_:
            X.setdefault("photos", []).append(ph_)
            use3d, ground, body = True, [], []
        else:
            poly(Qp, slab_fill or AX["top"], "8E877C", 0.15)
        for sh, rr in ground:                            # parks, streets, the river, as slide 1 draws them
            if sh.get("t") == "line":
                for run in rr:
                    it.append(L_([F(q) for q in run], sh.get("stroke") or AX["street"], max(0.05, wmm(sh)), lay))
            else:
                st_ = sh.get("stroke")
                it.append(P_([[F(q) for q in R_] for R_ in rr], sh.get("fill"), st_, wmm(sh) if st_ else 0.0, lay))
        nmove = 0                                        # Aras 14:33 UTC "keep the masterplan out of this axonometric"
        # the buildings (recoloured by area, each face keeping its light / shade step) and the trees, in slide 1's order
        mixh, aof = X["ns"]["mixh"], X.get("area_of") or {}
        lum = lambda h_: 0.2126 * int(h_[0:2], 16) + 0.7152 * int(h_[2:4], 16) + 0.0722 * int(h_[4:6], 16) + 1.0
        # v2.44 (Aras 16:01 "foreground and background is mixed still"): buildings and trees as one list, back to front
        # by their plan middle (a tree by its anchor), so a nearer body always paints over a farther one
        grps, i_ = [], 0
        gkey = lambda sh: (u"b", sh.get("bld")) if sh.get("bld") is not None else (u"t", tuple(sh.get("anchor") or ()))
        while i_ < len(body):
            j_ = i_ + 1
            while j_ < len(body) and gkey(body[j_]) == gkey(body[i_]):
                j_ += 1
            grps.append(body[i_:j_])
            i_ = j_

        def back_(g_):                                   # larger = farther back (higher up the drawing)
            b0 = g_[0].get("bld")
            if b0 is not None and b0 < len(C["bld"]) and C["bld"][b0][0]:
                q = cen_of(C["bld"][b0][0])
            else:
                q = g_[0].get("anchor") or (0.0, 0.0)
            return -Vw["c2"] * q[0] + Vw["c1"] * q[1]
        grps.sort(key=back_, reverse=True)
        body = [sh for g_ in grps for sh in g_]
        k_body = len(it)                                 # the flows go in here: on the ground, under the bodies
        i_, nb_, nmiss, ncut = 0, 0, 0, 0
        steps_ = [0.5 * max(0.0, 1.0 - lum(h_) / lum(AXO_STEPS[0])) for h_ in AXO_STEPS[1:]]   # v2.25 steps
        while i_ < len(body):
            b_ = body[i_].get("bld")
            j_ = i_ + 1
            while b_ is not None and j_ < len(body) and body[j_].get("bld") == b_:
                j_ += 1
            grp_ = body[i_:j_]
            if b_ is not None:
                nb_ += 1
                if b_ not in aof:
                    nmiss += 1
                A_ = AREA_COL.get(aof.get(b_), "B3B1AB")
                # v2.34 (Aras 14:31 "cut the buildings"): rebuilt from the footprint cut to the frame, slide 1's height
                P0 = [tuple(q) for q in C["bld"][b_][0]] if b_ < len(C["bld"]) else []
                if len(P0) > 1 and P0[0] == P0[-1]:
                    P0 = P0[:-1]
                roof = next((q for q in reversed(grp_) if q.get("fill")), None)
                rr_ = (roof.get("rings") or [[]])[0] if roof else []
                if grp_[0].get("foot"):                  # Page01Axo v3.2: its own footprint (cut to site_alan) and height
                    P0 = [tuple(q) for q in grp_[0]["foot"]]
                    if len(P0) > 1 and P0[0] == P0[-1]:
                        P0 = P0[:-1]
                if grp_[0].get("h"):
                    hb = float(grp_[0]["h"])
                elif len(P0) >= 3 and rr_:
                    gY = sum(D3(*q)[1] for q in P0) / len(P0)
                    hb = max(1.0, (sum(q[1] for q in rr_) / len(rr_) - gY) / Vw["kz"])
                else:
                    hb = STOREY_M
                Pw = ccw(clip_convex(ccw(P0), KC)) if len(P0) >= 3 else []
                if len(Pw) < 3:
                    i_ = j_
                    continue

                def on_e(q):                             # on the cut (an edge of KC)
                    for e_ in range(len(KC)):
                        a_, b_ = KC[e_ - 1], KC[e_]
                        L_e = math.hypot(b_[0] - a_[0], b_[1] - a_[1]) or 1.0
                        if abs((b_[0] - a_[0]) * (q[1] - a_[1]) - (b_[1] - a_[1]) * (q[0] - a_[0])) / L_e < 0.05:
                            return True
                    return False
                Qc = Pw
                bc = [A_] + [mixh(A_, "000000", t_) for t_ in steps_]
                st_v, ct_v = Vw["c1"] / Vw["k"], -Vw["c2"] / Vw["k"]
                walls = []
                for i in range(len(Pw)):
                    p_, q_ = Pw[i - 1], Pw[i]
                    dx, dy = q_[0] - p_[0], q_[1] - p_[1]
                    Ln = math.hypot(dx, dy)
                    if Ln < 1e-6:
                        continue
                    nx, ny = dy / Ln, -dx / Ln
                    if nx * ct_v + ny * st_v < -1e-9:    # faces the viewer (slide 1's own test)
                        cut = on_e(Qc[i - 1]) and on_e(Qc[i])
                        f_ = mixh(A_, "000000", 0.42) if cut else (bc[1] if (nx * st_v - ny * ct_v) < 0 else bc[2])
                        walls.append((-Vw["c2"] * (p_[0] + q_[0]) / 2.0 + Vw["c1"] * (p_[1] + q_[1]) / 2.0,
                                      [F(D3(p_[0], p_[1])), F(D3(q_[0], q_[1])), F(D3(q_[0], q_[1], hb)),
                                       F(D3(p_[0], p_[1], hb))], f_, cut))
                        ncut += 1 if cut else 0
                for _, R_, f_, cut in sorted(walls, key=lambda w_: -w_[0]):
                    it.append(P_([R_], f_, bc[1] if not cut else mixh(A_, "000000", 0.55), 0.05, lay))
                it.append(P_([[F(D3(q[0], q[1], hb)) for q in Pw]], bc[0], bc[1], 0.05, lay))
            else:
                for sh in grp_:
                    if sh.get("t") == "line":
                        it.append(L_([F(q) for q in sh.get("pts") or []], sh.get("stroke"), max(0.04, wmm(sh)), lay))
                    else:
                        st_ = sh.get("stroke")
                        it.append(P_([[F(q) for q in R_] for R_ in sh.get("rings") or []], sh.get("fill"), st_,
                                     wmm(sh) if st_ else 0.0, lay))
            i_ = j_
        log.append(u"%s diagram: cut from slide 1's axo: %d ground pieces, %d buildings (%d with no area: grey; %d cut "
                   u"faces at the frame), %d tree / other pieces" % (nk, len(ground), nb_, nmiss, ncut,
                                                                     sum(1 for sh in body if sh.get("bld") is None)))
    else:
        xs_ = [u * ca - v * sa for u, v in ((0, 0), (L1, 0), (L1, L2), (0, L2))]
        ys_ = [(u * sa + v * ca) * AXO_F for u, v in ((0, 0), (L1, 0), (L1, L2), (0, L2))]
        # v2.27: fit to the real top of the drawing (each roof corner), not the tallest building put at the back corner
        ytop = max(ys_ + [(u * sa + v * ca) * AXO_F + b[1] * STOREY_M * AXO_Z for b in bld for u, v in b[0]])
        s = min(W / (max(xs_) - min(xs_)), (H - AXO_SLAB - top_mm) / (ytop - min(ys_)))
        ox = x0 + (W - s * (max(xs_) - min(xs_))) / 2.0 - s * min(xs_)
        oy = y0 + AXO_SLAB - s * min(ys_)
        Pj = lambda u, v, z=0.0: (ox + s * (u * ca - v * sa), oy + s * ((u * sa + v * ca) * AXO_F + z * AXO_Z))
        mm_m = s
        # ---- the slab: its two cut faces (front, right), then its top
        c4 = [(0, 0), (L1, 0), (L1, L2), (0, L2)]
        A_, B_, C_ = Pj(0, 0), Pj(L1, 0), Pj(L1, L2)
        dz = (0.0, -AXO_SLAB)
        poly([A_, B_, (B_[0], B_[1] + dz[1]), (A_[0], A_[1] + dz[1])], AX["side"], "8E877C", 0.12)
        poly([B_, C_, (C_[0], C_[1] + dz[1]), (B_[0], B_[1] + dz[1])], "B8B1A4", "8E877C", 0.12)
        for P0, P1 in ((A_, B_), (B_, C_)):                  # v2.26: soil hatching on the cut faces (B08 axo tiles)
            Ln = math.hypot(P1[0] - P0[0], P1[1] - P0[1])
            for j in range(1, int(Ln / 0.9)):
                t_ = j * 0.9 / Ln
                q = (P0[0] + (P1[0] - P0[0]) * t_, P0[1] + (P1[1] - P0[1]) * t_)
                it.append(L_([(q[0], q[1] - 0.15), (q[0] - 0.9, q[1] + dz[1] + 0.15)], "8E877C", 0.06, lay))
        it.append(L_([(A_[0], A_[1] + dz[1]), (B_[0], B_[1] + dz[1]), (C_[0], C_[1] + dz[1])], "6E675E", 0.3, lay))
        poly([Pj(u, v) for u, v in c4], AX["top"], "8E877C", 0.15)   # v2.19: the ground painted and outlined
        # ---- streets, the stream, our move (ground level)
        for key in ("street_net", "streets"):
            for Q in (C.get("polys") or {}).get(key, []):
                Qc = clip_poly([uv(p) for p in Q], L1, L2)
                if len(Qc) >= 3:
                    poly([Pj(u, v) for u, v in Qc], AX["street"])
        for Q in (C.get("polys") or {}).get("river", []):
            Qc = clip_poly([uv(p) for p in Q], L1, L2)
            if len(Qc) >= 3:
                poly([Pj(u, v) for u, v in Qc], AX["water"])
        nmove = draw_move(Pj, poly, it)
        # ---- the buildings, back to front: walls that face the viewer, then the roof
        depth = lambda Q: -max(q[0] * sa + q[1] * ca for q in Q)
        FAB_, FABC_, mixh = X["ns"]["FAB"], X["ns"]["FAB_COM"], X["ns"]["mixh"]
        lum = lambda h_: 0.2126 * int(h_[0:2], 16) + 0.7152 * int(h_[2:4], 16) + 0.0722 * int(h_[4:6], 16) + 1.0
        steps = [0.5 * max(0.0, 1.0 - lum(h_) / lum(AXO_STEPS[0])) for h_ in AXO_STEPS[1:]]   # v2.25: half as dark
        cols = {}
        for Q, fl, com, fab_ in sorted(bld, key=lambda b: depth(b[0])):
            z = fl * STOREY_M
            kc = fab_                                        # v2.28: the building's area (Aras 13:32 UTC)
            if kc not in cols:                               # v2.22: roof, lit wall, shaded wall, outline (slide 1 axo)
                r_ = AREA_COL.get(fab_, "B3B1AB")            # v2.28: the map's area colour (fab_ holds the area key)
                cols[kc] = [r_] + [mixh(r_, "000000", t_) for t_ in steps]
            bc = cols[kc]
            ar = sum(Q[i - 1][0] * Q[i][1] - Q[i][0] * Q[i - 1][1] for i in range(len(Q)))
            sg = 1.0 if ar > 0 else -1.0                     # ccw: the outward normal of an edge (dx, dy) is (dy, -dx)
            for i in range(len(Q)):
                a, b = Q[i - 1], Q[i]
                nx, ny = sg * (b[1] - a[1]), -sg * (b[0] - a[0])
                if nx * sa + ny * ca < 0:                    # faces the viewer (toward the front)
                    f_ = bc[1] if nx * ca - ny * sa < 0 else bc[2]   # v2.22: lit / shaded wall of its own colour
                    poly([Pj(*a), Pj(*b), Pj(b[0], b[1], z), Pj(a[0], a[1], z)], f_, bc[1], 0.06)
            poly([Pj(u, v, z) for u, v in Q], bc[0], bc[1], 0.06)
    # ---- the flows over the buildings (v2.21): bus routes (OSM ways), the heritage loop's legs
    seen = set()
    nbus = 0
    # v2.43 (Aras 15:57 "make these blue and red lines thinner like scale the lines according to the drawing size"):
    # a line weight is given for a full-width A3 drawing (400 mm) and scaled by this drawing's width
    if "pc_stroke_k" in G:                               # v2.44: pages_common v3.33, one rule for every drawing
        k_s = G["pc_stroke_k"](W, H, log, u"%s axonometric" % nk)
        lw = lambda b_: G["pc_stroke"](b_, k_s)
    else:
        lw = lambda b_: b_ * min(1.0, W / 400.0)
    k_f0 = len(it)
    for r_ in (D.get("routes") or {}).values():
        for wid in r_.get("ways", []):
            if wid in seen or wid not in D.get("ways", {}):
                continue
            seen.add(wid)
            for run in ([] if use3d else clipL([uv(p) for p in D["ways"][wid]])):   # v2.45: in 3D, strips
                it.append(L_([Pj(u, v) for u, v in run], "FFFFFF", lw(1.0), lay))
                it.append(L_([Pj(u, v) for u, v in run], AX["bus"], lw(0.7), lay))
                nbus += 1
    Hh = sorted(D["heritage"], key=lambda h: int(h["n"]))
    nloop = 0
    for a, b in zip(Hh, Hh[1:]):
        Pl = [a["xy"], b["xy"]]
        if {a["key"], b["key"]} == {"tabak_koprusu", "ulucami_onu"}:
            Pl = G["pc_selinos"](a["xy"], b["xy"]) or Pl
        for run in ([] if use3d else clipL([uv(p) for p in Pl])):
            it.append(L_([Pj(u, v) for u, v in run], "FFFFFF", lw(1.2), lay))
            it.append(L_([Pj(u, v) for u, v in run], AX["loop"], lw(0.9), lay))
            nloop += 1
    if k_body is not None and k_body <= k_f0:   # v2.44: the flows lie on the ground, under the bodies
        fl_ = it[k_f0:]
        del it[k_f0:]
        it[k_body:k_body] = fl_
    # ---- the pins: hub (tall), loop stops, places
    pins = []
    for hb in HUBS:
        if any(c_ == hb["code"] for c_, _k in info["hubs"]):
            for p in hb["pts"]:
                q = uv(H_[p])
                if inK(q):
                    pins.append((q, pin_mm, "hub", hb))
    for h in Hh:
        q = uv(h["xy"])
        if inK(q):
            pins.append((q, pin_mm * 0.75, "loop", h))
    for n in info["places"]:
        q = uv(PLACES[n]["xy"])
        if inK(q):
            pins.append((q, pin_mm * 0.6, "place", n))
    tips = []
    for q, ph, kd, obj in sorted(pins, key=lambda t: depth([t[0]])):
        b = Pj(*q)
        tp = (b[0], b[1] + ph)
        for _ in range(4):                               # v2.24: off another pin's stem: lean aside
            st_ = [t_ for t_ in tips if abs(tp[0] - t_[2]) < 2.6 and t_[3] - 1.0 <= tp[1] <= t_[1] + 4.0]
            if not st_:
                break
            tp = (tp[0] + (4.5 if tp[0] >= st_[0][2] else -4.5), tp[1])
        while any(abs(tp[0] - t_[0]) < 4.6 and abs(tp[1] - t_[1]) < 4.2 for t_ in tips):
            tp = (tp[0], tp[1] + 4.4)                    # v2.19: a pin that would touch another is raised
        tips.append((tp[0], tp[1], b[0], b[1]))
        it.append(P_([circle(b[0], b[1], 0.45, 12)], K["ink"], None, 0.0, lay))
        it.append(L_([b, tp], K["ink"], 0.25, lay))
        if kd == "hub":
            c_ = K["hub"]["transit" if obj["kind"] == "hidden" else obj["kind"]]
            it.append(P_([[(tp[0] - 2.0, tp[1]), (tp[0] + 2.0, tp[1]), (tp[0] + 2.0, tp[1] + 3.6),
                           (tp[0] - 2.0, tp[1] + 3.6)]], c_, "FFFFFF", 0.25, lay))
            it.append(G["pc_text_c"](obj["code"], tp[0], tp[1] + 1.8, 2.0, "FFFFFF", lay, True))
        elif kd == "loop":
            it.append(P_([circle(tp[0], tp[1] + 1.6, 1.6, 24)], AX["loop"], "FFFFFF", 0.3, lay))
            it.append(G["pc_text_c"](str(obj["n"]), tp[0], tp[1] + 1.6, 1.9, "FFFFFF", lay, True))
        else:
            it.append(P_([circle(tp[0], tp[1] + 1.5, 1.5, 24)], "FFFFFF", PLACE_C, 0.35, lay))
            it.append(G["pc_text_c"](str(obj), tp[0], tp[1] + 1.5, 1.8, PLACE_C, lay, True))
    log.append(u"%s diagram: %d bus way runs, %d loop legs, %d pieces of our move, %d pins; drawn at %.3f mm a m" % (
        nk, nbus, nloop, nmove, len(pins), mm_m))
    return it


def node_card(G, lib, K, X, nk, nd, info, x, ytop, w, h, log):
    """v2.17: one node card in the 3 x 2 grid: head (tile, name, claim), the axonometric, then two text columns:
    what meets here | idea, places, weak link. Returns (items, overflow mm)"""
    P_, T_, circle, wrap = G["P_"], G["T_"], G["circle"], G["wrap"]
    tw = lib["text_w"]
    INK = K["ink"]
    col = NODE_COL.get(nk, NODE_C)
    it = []
    low = [ytop]

    def para(s, y, size, xx, ww, c=INK, bold=False):
        for ln in wrap(s, size, ww, tw, bold):
            it.append(T_(ln, xx, y - size * 0.75, size, c, "cards", bold))
            y -= size * 1.3
        low[0] = min(low[0], y)
        return y
    it.append(P_([[(x, ytop - 1.4), (x + w, ytop - 1.4), (x + w, ytop), (x, ytop)]], col, None, 0.0, "cards"))
    tile = (8.0, 5.0)
    yh = ytop - 2.6
    it.append(P_([[(x, yh - tile[1]), (x + tile[0], yh - tile[1]), (x + tile[0], yh), (x, yh)]], col, None, 0.0, "cards"))
    it.append(G["pc_text_c"](nk, x + tile[0] / 2, yh - tile[1] / 2, 2.8, "FFFFFF", "cards", True))
    it.append(T_(nd["name"], x + tile[0] + 2.0, yh - 2.3, 2.8, INK, "cards", True))
    it.append(T_(strip_claim(nk, info), x + tile[0] + 2.0, yh - 4.9, 2.0, col, "cards", True))
    yd = yh - tile[1] - 1.5
    it += node_axo(G, K, X, nk, info, x, yd - AXO_H, w, AXO_H, log)
    y0 = yd - AXO_H - 2.0
    cw = (w - 4.0) / 2.0
    it.append(T_(u"WHAT MEETS HERE", x, y0 - 1.8, 1.9, GLY["ink2"], "cards", True))
    y = para(strip_counts(info) or u"0 bus lines · no heritage loop stop · 0 shop buildings", y0 - 3.2, CARD_PT, x, cw)
    if info["hub_kind"]:
        y -= 0.6
        for s_, b_ in KEYS[info["hub_kind"]]:
            y = para(s_, y, CARD_PT, x, cw, INK, b_)
    ni = NODE_INFO.get(nk, {})
    for head_, key_ in ((u"LINKS", "links"), (u"STORY", "story")):   # v2.35: NODE_IDEAS.md
        if ni.get(key_):
            it.append(T_(head_, x, y - 1.8 - 0.6, 1.9, GLY["ink2"], "cards", True))
            y = para(ni[key_], y - 3.8, CARD_PT, x, cw)
    xd = x + cw + 4.0
    it.append(T_(u"IDEA", xd, y0 - 1.8, 1.9, GLY["ink2"], "cards", True))
    idea_ = IDEAS.get(nk) or ni.get("idea") or u"open"
    y = para(idea_, y0 - 3.2, CARD_PT, xd, cw, col if idea_ != u"open" else GLY["ink2"], nk in IDEAS) - 0.6
    if ni.get("bld"):                                    # v2.35: the building and its programme (EST.)
        it.append(T_(u"BUILDING", xd, y - 1.8, 1.9, GLY["ink2"], "cards", True))
        y = para(ni["bld"], y - 3.2, CARD_PT, xd, cw) - 0.6
    if info["places"]:
        it.append(T_(u"PLACES", xd, y - 1.8, 1.9, GLY["ink2"], "cards", True))
        y -= 3.2
        for n in info["places"]:
            f = PLACES[n]
            it.append(P_([circle(xd + 1.3, y - 1.3, 1.3, 20)], "FFFFFF", PLACE_C, 0.3, "cards"))
            it.append(G["pc_text_c"](str(n), xd + 1.3, y - 1.3, 1.7, PLACE_C, "cards", True))
            y = para(f["name"] + u": " + f["kw"][0] + u" · " + f["kw"][1], y, CARD_PT, xd + 3.6, cw - 3.6) - 0.3
    miss = [s for s, v in ((u"no hub", info["hubs"]), (u"no heritage loop stop", info["loop"]),
                           (u"no bus line", info["bus"]), (u"no shops", info["shops"])) if not v]
    it.append(T_(u"WEAK LINK", xd, y - 1.8, 1.9, GLY["ink2"], "cards", True))
    para(u" · ".join(miss) if miss else u"none of the four missing", y - 3.2, CARD_PT, xd, cw)
    return it, max(0.0, (ytop - h) - low[0])


def strip_claim(nk, info):
    """the claim: what meets here (what is missing is the WEAK LINK line)"""
    have = [w_ for w_, v in ((u"a hub", info["hubs"]), (u"buses", info["bus"]), (u"the heritage loop", info["loop"]),
                             (u"shops", info["shops"])) if v]
    if not have:
        return u"NOTHING MEETS HERE YET"
    a = (u", ".join(have[:-1]) + u" and " + have[-1]) if len(have) > 1 else have[0]
    return (a + u" meet here" if len(have) > 1 else a + u" alone").upper()


def strip_counts(info):
    """the numbers, as text beside the strip (the strip itself carries none)"""
    out = []
    if info["bus"]:
        out.append(u"%d bus lines" % info["bus"])
    if info["loop"]:
        out.append(u"heritage loop stop " + u", ".join(u"%s %s" % (n_, nm) for n_, nm in info["loop"]))
    if info["shops"]:
        out.append(u"%d shop buildings" % info["shops"])
    return u" · ".join(out)


def main():
    t0 = time.time()
    log = []
    G = load_common()
    lib = G["pc_lib"](log)
    D = G["pc_data"](log)
    K = D["key"]
    with open(os.path.join(BERGAMA_ROOT, "Data", "section_lines.json"), encoding="utf-8") as f:
        NODES = json.load(f)["nodes"]
    dist, L_, P_, T_, circle, wrap = G["pc_dist"], G["L_"], G["P_"], G["T_"], G["circle"], G["wrap"]
    INK, tm, tw = K["ink"], K["text_mm"], lib["text_w"]
    H = D["hubs"]
    nks = sorted(NODES)
    cen = dict((k, (sum(p[0] for p in NODES[k]["corners"]) / len(NODES[k]["corners"]),
                    sum(p[1] for p in NODES[k]["corners"]) / len(NODES[k]["corners"]))) for k in nks)
    # ---- the map = site_alan (v2.4: pages_common SiteMap), across the top, scale to a 1:500 step
    mpns, MPC = G["pc_mp_data"](log)
    M = G["pc_site_map"](10000, log)
    mw_max = PAGE_W - 2 * MARGIN - 8.0 - SIDE_W
    den = int(math.ceil(M.F.w / mw_max * 1000.0 / DEN_STEP) * DEN_STEP)
    k = 1000.0 / den
    M.den, M.k = float(den), k
    M.mw, M.mh = M.F.w * k, M.F.h * k
    M.x0, M.y0 = MARGIN, PAGE_H - MARGIN - M.mh
    M.w, M.h = PAGE_W, PAGE_H
    M.box = (M.x0, M.y0, M.x0 + M.mw, M.y0 + M.mh)
    T = M.T
    log.append(u"map = site_alan %.0f x %.0f m at 1:%d = %.0f x %.0f mm" % (M.F.w, M.F.h, den, M.mw, M.mh))
    if T(cen[nks[0]])[0] > T(cen[nks[-1]])[0]:
        log.append(u"FLAG: %s sits right of %s on the map" % (nks[0], nks[-1]))

    # ---- what each node holds (calculated)
    ns, C = G["pc_mb_data"](log)
    shops = [(sum(p[0] for p in R) / len(R), sum(p[1] for p in R) / len(R)) for R, fab_, com, src, nm in C["bld"] if com]
    lines_of = G["pc_stop_lines"](D)
    info = {}
    for nk in nks:
        R = NODES[nk]["corners"]
        inn = lambda xy: pip(xy[0], xy[1], R) and M.inside(T(xy))     # v2.7: in the node frame and in site_alan
        hubs = [(hb["code"], hb["kind"]) for hb in HUBS if any(inn(H[p]) for p in hb["pts"])]
        loop = [(h["n"], h["name"]) for h in D["heritage"] if inn(h["xy"])]
        bus = set()
        for s in D["stops"]:
            if inn(s["xy"]):
                bus |= set(lines_of.get(s["name"], s["lines"]))
        info[nk] = dict(hubs=hubs, loop=loop, bus=len(bus), shops=sum(1 for s in shops if inn(s)),
                        hub_kind=hubs[0][1] if hubs else None,
                        places=[n for n, f in sorted(PLACES.items()) if f["xy"] and inn(f["xy"])])
        log.append(u"%s %s: hubs %s; loop %s; %d bus lines; %d shop buildings; places %s" % (
            nk, NODES[nk]["name"], u" ".join(c for c, _ in hubs) or u"-", u" ".join(n for n, _ in loop) or u"-",
            len(bus), info[nk]["shops"], u" ".join(str(n) for n in info[nk]["places"]) or u"-"))

    # ---- the map
    # v2.38 (Aras 15:06 "just put the .svg directly into that drawing and do the colouring on most foreground layer"):
    # the base of the map is master.svg as it is (every group, his existing roads and buildings too, its own colours),
    # the area colours over it (outside the working area), the working-area dashes over everything
    MB = G["pc_mapbase"](M, K, log, MB_LAYERS, {"lc_light": 0.8, "water_hatch": None})   # v2.40: under master.svg,
    items = [it_ for it_ in MB[0] if not (it_[0] == "line" and len(it_) > 5 and it_[5] == "water_hatch")]   # no white
    for i_, it_ in enumerate(items):                     # gaps where master.svg draws nothing; river flat (14:38)
        if it_[0] == "poly" and len(it_) > 6 and it_[6] == "water" and isinstance(it_[2], str) and it_[2].startswith("~"):
            items[i_] = tuple(it_[:2]) + (it_[2][1:],) + tuple(it_[3:])
    mp_all = set(k_.split("/")[0] for k_ in MPC["layers"])
    cnt = mpns["mp_draw"](MPC, items, T, k, M.box, "map", mp_all, MP_STYLE)
    n0 = len(items)                                      # v2.39 (Aras 15:07 "still really awful"): his picture tiles
    items = [it_ for it_ in items if not (it_[0] == "poly" and it_[2] == mpns["AREA_DEFAULT"])]   # with no colour
    log.append(u"map: %d master.svg picture tiles with no colour of their own left out (grey squares)" % (n0 - len(items)))
    log.append(u"map: master.svg as the base, %d pieces from %d groups (%s)" % (
        sum(cnt.values()), len(mp_all), u", ".join(sorted(mp_all))))
    study_its = G["pc_study"](M, K, log)                 # v2.37: drawn last of the lines (Aras 14:45), see below
    lab = G["Labels"](M, lib)
    a_blobs, a_blds, area_of, AZ = area_layer(M, T, k, C, ns["mixh"], log,
                                              [T(p) for p in G["pc_selinos_line"]()], read_heritage_osm(lib, log),
                                              read_work(G, log))   # v2.28: the areas under the proposal
    items += a_blobs + a_blds                            # v2.38: over master.svg (the colouring on top)
    mapA, drop = M.mw * M.mh, 0                          # v2.14: no sheet over the map (picture-area outlines bigger
    for i_ in range(len(items) - 1, -1, -1):             # than the frame in the cache, kopruler/texture)
        it_ = items[i_]
        if it_[0] == "poly" and str(it_[6]).startswith("mp/"):
            xs_ = [p[0] for R_ in it_[1] for p in R_]
            ys_ = [p[1] for R_ in it_[1] for p in R_]
            if (max(xs_) - min(xs_)) * (max(ys_) - min(ys_)) > 0.25 * mapA:
                del items[i_]
                drop += 1
                cnt[it_[6][3:]] = cnt.get(it_[6][3:], 1) - 1
    if drop:
        log.append(u"masterplan: %d piece(s) larger than a quarter of the map dropped (picture-area outlines)" % drop)
    log.append(u"masterplan drawn: " + (u", ".join(u"%s %d" % kv for kv in sorted(cnt.items())) or u"nothing"))
    if not cnt:
        log.append(u"FLAG: no masterplan piece inside the map strip")
    # ---- the neighbourhoods (mahalle) and their main fabric (calculated: MapBase buildings in site_alan)
    MAH = read_mahalle(lib, log)
    bld_in = [(cen_of(Rb), fab_) for Rb, fab_, com, src, nm in C["bld"] if len(Rb) >= 3 and M.inside(T(cen_of(Rb)))]
    words = ns.get("FAB_WORDS") or {}
    char = {}
    for name, rings in MAH:
        bb = [(min(p[0] for p in R_), min(p[1] for p in R_), max(p[0] for p in R_), max(p[1] for p in R_)) for R_ in rings]
        cnt_ = {}
        pts_ = []
        for c_, fab_ in bld_in:
            if any(b[0] <= c_[0] <= b[2] and b[1] <= c_[1] <= b[3] and pip(c_[0], c_[1], R_) for b, R_ in zip(bb, rings)):
                cnt_[fab_] = cnt_.get(fab_, 0) + 1
                pts_.append(c_)
        tot = sum(cnt_.values())
        if not tot:
            continue
        main_ = max((f_ for f_ in cnt_ if f_ != "construction"), key=lambda f_: cnt_[f_], default=None)
        char[name] = dict(fab=main_, n=tot, share=100.0 * cnt_.get(main_, 0) / tot, pts=pts_, rings=rings)
        log.append(u"neighbourhood %s: %d buildings in site_alan; main fabric %s %.0f %% (%s)" % (
            name, tot, main_, char[name]["share"], u", ".join(u"%s %d" % kv for kv in sorted(cnt_.items()))))
    # v2.40 (Aras 15:15 "fix this area"): the mahalle boundary lines no longer drawn (they cut across the areas)
    # v2.28: the node areas and the fabric colours gave way to the areas (area_layer, drawn under the proposal)
    sel = [T(p) for p in G["pc_selinos_line"]()]       # v2.10: the spine, the stream's line, cut to the map
    items.append(("line", sel, "3F86B8", 0.7, "map", "stream", 1))
    lab.block_line(sel, 0.6)
    inbox = lambda q, r=0.0: M.box[0] + r <= q[0] <= M.box[2] - r and M.box[1] + r <= q[1] <= M.box[3] - r
    obst = [T(H[p]) for hb in HUBS for p in hb["pts"]]
    for n, f in sorted(PLACES.items()):
        if f["xy"] and not inbox(T(f["xy"]), 1.5):
            log.append(u"place %d outside site_alan: not drawn" % n)
        elif f["xy"]:
            q0 = q = T(f["xy"])
            for _ in range(6):                           # v2.11 (run 9 review): off the hub tiles and the other places,
                near = [o for o in obst if dist(q, o) < 4.2]   # a hairline leader back to the true point
                if not near:
                    break
                o = min(near, key=lambda o_: dist(q, o_))
                d_ = dist(q, o)
                u_ = ((q[0] - o[0]) / d_, (q[1] - o[1]) / d_) if d_ > 0.05 else (0.0, 1.0)
                q = (o[0] + u_[0] * 4.4, o[1] + u_[1] * 4.4)
            if q != q0:
                items.append(L_([q0, q], PLACE_C, 0.15, "places"))
                items.append(P_([circle(q0[0], q0[1], 0.35, 12)], PLACE_C, None, 0.0, "places"))
                log.append(u"place %d moved %.1f mm off a hub tile or place, with a leader" % (n, dist(q, q0)))
            obst.append(q)
            items.append(P_([circle(q[0], q[1], 1.5, 20)], "FFFFFF", PLACE_C, 0.35, "places"))
            items.append(G["pc_text_c"](str(n), q[0], q[1], 1.8, PLACE_C, "places", True))
            lab.block_pt(q, 1.8)
    s_ = 3.6
    for hb in HUBS:
        c_ = K["hub"]["transit" if hb["kind"] == "hidden" else hb["kind"]]
        for p in hb["pts"]:
            q = T(H[p])
            if not inbox(q, s_ / 2):
                log.append(u"hub %s (%s) outside site_alan: not drawn" % (hb["code"], p))
                continue
            items.append(P_([[(q[0] - s_ / 2, q[1] - s_ / 2), (q[0] + s_ / 2, q[1] - s_ / 2), (q[0] + s_ / 2, q[1] + s_ / 2),
                              (q[0] - s_ / 2, q[1] + s_ / 2)]], c_, "FFFFFF", 0.25, "hubs"))
            items.append(G["pc_text_c"](hb["code"], q[0], q[1], 2.0, "FFFFFF", "hubs", True))
            lab.block_pt(q, s_ / 2 + 0.3)
    items += study_its                                   # v2.37 (Aras 14:45 "make our working area dashed line as
    # the most foreground line"): over every other line of the map, under the area names only
    # v2.37 (Aras 14:42 "write the names onto the areas that have been painted BOLD BLACK in a readable way"): each
    # painted area named inside its own colour, bold black on a thin white letter halo (no box), never across an edge
    nk_of = {}                                           # area key -> the node standing in it (both parts of a split area)
    for nk in nks:
        c = T(cen[nk])
        a0 = AZ["key_at"](c) if "key_at" in AZ else None
        bases = ("YN", "DN") if nk == "N1" else ((a0[:-1] if a0 and a0.endswith("b") else a0),) if a0 else ()
        for a_ in AZ["order"]:
            if a_ in bases or (a_.endswith("b") and a_[:-1] in bases):
                nk_of.setdefault(a_, nk)
        items.append(P_([circle(c[0], c[1], 0.55, 16)], "000000", "FFFFFF", 0.15, "node_pointers"))
        lab.block_pt(c, 1.0)
    placed = []
    for a_ in AZ["order"]:
        if a_ not in AZ.get("cent", {}):
            continue
        nk = nk_of.get(a_)
        txt = (u"%s %s" % (nk, AZ["areas"][a_]["name"])) if nk else AZ["areas"][a_]["name"]
        tgt = T(cen[nk]) if nk else AZ["cent"][a_]
        pts = []
        y_ = M.box[1] + 2.0
        while y_ < M.box[3] - 2.0:
            x_ = M.box[0] + 2.0
            while x_ < M.box[2] - 2.0:
                if AZ["key_at"]((x_, y_)) == a_:
                    pts.append(((x_ - tgt[0]) ** 2 + (y_ - tgt[1]) ** 2, x_, y_))
                x_ += 1.2
            y_ += 1.2
        pts.sort()
        hit = None
        mw = (lambda t_, z_: G["pc_mark_w"](t_, z_, True) * 1.08) if "pc_mark_w" in G else \
            (lambda t_, z_: tw(t_, z_, True) * 1.15)
        two = txt.split(u", ", 1) if u", " in txt else (txt.rsplit(u" ", 1) if u" " in txt else [txt])
        two = [two[0] + (u"," if u", " in txt else u"")] + two[1:]
        lays = [([txt], z_) for z_ in (2.3, 2.0, 1.8, 1.6)] + [(two, z_) for z_ in (1.8, 1.6, 1.4)] + \
            [([txt], 1.3)]                               # v2.41: two lines before the smallest single line
        for lines, sz in lays:
            w_ = max(mw(t_, sz) for t_ in lines)
            hh = sz * 1.15 * (len(lines) - 1)            # the first line's baseline is y_, the others under it
            for _, x_, y_ in pts:
                bx = (x_ - w_ / 2 - 0.4, y_ - hh - 0.3 * sz - 0.4, x_ + w_ / 2 + 0.4, y_ + 0.8 * sz + 0.4)
                if not AZ["box_clear"](bx) or bx[0] < M.box[0] + 1.5 or bx[2] > M.box[2] - 1.5 or \
                        bx[1] < M.box[1] + 1.5 or bx[3] > M.box[3] - 1.5:
                    continue
                if any(not (bx[2] < o[0] or bx[0] > o[2] or bx[3] < o[1] or bx[1] > o[3]) for o in placed + lab.boxes):
                    continue
                hit = (x_, y_, sz, bx, lines)
                break
            if hit:
                break
        if not hit:
            if not pts:
                continue
            _, x_, y_ = pts[0]
            sz, lines = 1.4, two
            w_ = max(mw(t_, sz) for t_ in lines)
            x_ = min(M.box[2] - w_ / 2 - 1.5, max(M.box[0] + w_ / 2 + 1.5, x_))
            hit = (x_, y_, sz, (x_ - w_ / 2, y_ - sz * 1.15 * (len(lines) - 1) - 0.3 * sz, x_ + w_ / 2, y_ + 0.8 * sz),
                   lines)
            log.append(u"FLAG: area name %s has no room wholly inside its colour (placed at its nearest point)" % txt)
        x_, y_, sz, bx, lines = hit
        r_ = 0.09                                        # v2.39: a hairline halo, no leaders
        for j_, t_ in enumerate(lines):
            yj = y_ - j_ * sz * 1.15
            items += [T_(t_, x_ + r_ * dx, yj + r_ * dy, sz, "FFFFFF", "area_names_halo", True, "C")
                      for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            items.append(T_(t_, x_, yj, sz, "000000", "area_names", True, "C"))
        placed.append(bx)
        lab.boxes.append(bx)
        log.append(u"area name %s: %.1f mm bold black, %d line(s)" % (txt, sz, len(lines)))
    # v2.29: the neighbourhood fabric names dropped (Aras 13:44 "too busy"; the areas carry the reading)
    items += lab.items
    items.append(P_([[(M.box[0], M.box[1]), (M.box[2], M.box[1]), (M.box[2], M.box[3]), (M.box[0], M.box[3])]], None,
                    INK, 0.25, "frame"))

    # ---- the legend: a band under the map (v2.4: the map strip is site_alan, too low for a column legend)
    sq = lambda f_, s__=3.0: (lambda xx, yy: [P_([[(xx - s__ / 2, yy - s__ / 2), (xx + s__ / 2, yy - s__ / 2),
                                                 (xx + s__ / 2, yy + s__ / 2), (xx - s__ / 2, yy + s__ / 2)]],
                                               f_, "FFFFFF", 0.25, "legend")])
    box_ = lambda xx, yy: [(xx - 4.5, yy - 1.8), (xx + 4.5, yy - 1.8), (xx + 4.5, yy + 1.8), (xx - 4.5, yy + 1.8)]
    rows, story_of = [], {}
    for a_ in AZ["order"]:                               # v2.28: one row per area: its blob with a building on it
        if not any(b == a_ for b in area_of.values()):
            continue
        c__ = AREA_COL.get(a_, "B3B1AB")
        rows.append(((lambda c_, d_: lambda xx, yy: [P_([box_(xx, yy)], d_, None, 0.0, "legend"),
                                                     P_([[(xx - 2.0, yy - 1.0), (xx + 0.5, yy - 1.0), (xx + 0.5, yy + 1.0),
                                                          (xx - 2.0, yy + 1.0)]], c_, ns["mixh"](c_, "000000", 0.35), 0.04,
                                                        "legend"),
                                                     P_([[(xx + 1.3, yy - 1.0), (xx + 3.2, yy - 1.0), (xx + 3.2, yy + 0.6),
                                                          (xx + 1.3, yy + 0.6)]], c_, ns["mixh"](c_, "000000", 0.35), 0.04,
                                                        "legend")])(c__, ns["mixh"](c__, "000000", AREA_DARK)),
                     AZ["areas"][a_]["name"]))
        st_ = AREA_STORY.get(AZ["areas"][a_]["name"])     # v2.36: what sets the area apart (Aras 14:21)
        if st_:
            story_of[AZ["areas"][a_]["name"]] = st_[0]
            log.append(u"area story %s: \"%s\" (from: %s; spine_run25 area profile, PageSpine v2.32)" % (
                AZ["areas"][a_]["name"], st_[0], st_[1]))
        else:
            log.append(u"area story %s: no line (name not in AREA_STORY)" % AZ["areas"][a_]["name"])
    rows.append((lambda xx, yy: [L_([(xx - 4.5, yy), (xx + 4.5, yy)], "3F86B8", 0.7, "legend")], u"the Selinos stream: the spine"))
    rows += [(lambda xx, yy: [P_([circle(xx, yy, 1.5, 20)], "FFFFFF", PLACE_C, 0.35, "legend")],
              u"the project's places (numbered)"),
             (sq(K["hub"]["walk"]), u"walking hub"), (sq(K["hub"]["transit"]), u"main transit hub"),
             (sq(K["hub"]["gateway"]), u"gateway out of town"),
             (lambda xx, yy: [P_([circle(xx, yy, 1.6, 20)], K["heritage"], "FFFFFF", 0.25, "legend")],
              u"heritage loop stop (cards)")]
    for txt, pres in MP_ROWS:                            # masterplan rows, in the colours the map uses
        sw = mp_swatch(mpns, MPC, pres) if any(any(c_ == p_ or c_.startswith(p_ + "/") for p_ in pres)
                                               for c_ in cnt) else None
        if not sw:
            log.append(u"legend: %s not on the map, no row" % txt)
            continue
        if sw[0] == "line":
            rows.append(((lambda c__: lambda xx, yy: [L_([(xx - 4.5, yy), (xx + 4.5, yy)], c__, 0.6, "legend")])(sw[1]),
                         txt))
        else:
            rows.append(((lambda f__, s__: lambda xx, yy: [P_([box_(xx, yy)], f__, s__, 0.2 if s__ else 0.0, "legend")])(
                sw[1], sw[2]), txt))
    ncol = 6                                             # v2.22 / v2.28: the area rows
    nrow = int(math.ceil(len(rows) / float(ncol)))
    colw, rh, ls = (PAGE_W - 2 * MARGIN) / ncol, 4.6, tm["legend"] - 0.2
    yl = M.box[1] - 5.0
    for i, (draw, txt) in enumerate(rows):
        xx, yy = MARGIN + (i // nrow) * colw, yl - (i % nrow) * rh
        items += draw(xx + 5.0, yy)
        lns = wrap(txt, ls, colw - 16.0, tw)
        if len(lns) > 1:
            log.append(u"FLAG: legend row too long for its column: %s" % txt)
        if txt in story_of:                              # v2.36: the name above, its line under it, smaller and lighter
            items.append(T_(lns[0], xx + 12.0, yy + 0.25, ls, INK, "legend"))
            ss = ls * 0.82
            sl_ = wrap(story_of[txt], ss, colw - 16.0, tw)
            if len(sl_) > 1:
                log.append(u"FLAG: area line too long for its column: %s" % story_of[txt])
            items.append(T_(sl_[0], xx + 12.0, yy - ss * 1.15, ss, ns["mixh"](INK, "FFFFFF", 0.35), "legend"))
        else:
            items.append(T_(lns[0], xx + 12.0, yy - ls * 0.38, ls, INK, "legend"))
    ylb = yl - nrow * rh

    # ---- the six nodes: a 3 x 2 grid of cards, each with its axonometric (v2.17)
    X = dict(M=M, C=C, D=D, H=H, NODES=NODES, mpns=mpns, MPC=MPC, ns=ns, area_of=area_of, AM=load_axo_model(log))
    X["A3"] = load_axo3d(log) if X["AM"] and X["AM"].get("d3") else None   # v2.45: the node axos from the 3D model
    X["photos"] = []
    yt = ylb - 6.0
    items.append(T_(u"THE SIX NODES: WHAT MEETS AT EACH, WHAT IS MISSING", MARGIN, yt + 3.0, tm["sub"], INK, "cards", True))
    xk = PAGE_W - MARGIN                                 # the one key for the six drawings, right of the heading
    keys = [(u"buildings in their area's colour (map key)", "sq", AREA_COL["YN"]),
            (u"stream", "sq", AX["water"]), (u"heritage loop", "ln", AX["loop"]), (u"bus routes", "ln", AX["bus"])]
    for txt, kd, c_ in keys:
        wt = tw(txt, 2.0) + 7.0
        xk -= wt
        if kd == "sq":
            items.append(P_([[(xk, yt + 2.6), (xk + 4.0, yt + 2.6), (xk + 4.0, yt + 5.0), (xk, yt + 5.0)]], c_, None, 0.0,
                            "cards"))
        else:
            items.append(L_([(xk, yt + 3.8), (xk + 4.0, yt + 3.8)], c_, 0.9, "cards"))
        items.append(T_(txt, xk + 5.0, yt + 3.1, 2.0, INK, "cards"))
    room = yt - 1.5 - MARGIN
    ch = (room - CARD_GAP) / 2.0
    cw = (PAGE_W - 2 * MARGIN - 2 * CARD_GAP) / 3.0
    for i, nk in enumerate(nks):
        cx, cy = MARGIN + (i % 3) * (cw + CARD_GAP), yt - 1.5 - (i // 3) * (ch + CARD_GAP)
        its_, over = node_card(G, lib, K, X, nk, NODES[nk], info[nk], cx, cy, cw, ch, log)
        items += its_
        if over > 0.1:
            log.append(u"FLAG: card %s text runs %.1f mm below its card" % (nk, over))
    log.append(u"cards: %.0f x %.0f mm, axonometrics %.0f mm high" % (cw, ch, AXO_H))

    # ---- the side column: title, north, scale
    x = M.box[2] + 8.0
    y = M.box[3] - tm["title"]
    for ln in wrap(u"THE SIX NODES ALONG THE SPINE", tm["title"], SIDE_W, tw, True):
        items.append(T_(ln, x, y, tm["title"], INK, "title", True))
        y -= tm["title"] * 1.25
    for ln in wrap(u"Where the town meets the stream, node by node", tm["sub"], SIDE_W, tw):
        items.append(T_(ln, x, y, tm["sub"], INK, "title"))
        y -= tm["sub"] * 1.4
    yb = M.box[1] + 4.0
    if y < yb + 14.0:
        log.append(u"FLAG: the title reaches the north arrow (%.1f mm)" % (y - yb - 14.0))
    items += G["pc_north_items"](x + 5.5, yb + 5.0, 4.5, M.north, INK)
    bar = 250.0 if den <= 12000 else 500.0
    Lb, xb = bar * k, x + 16.0
    for i in range(4):
        items.append(P_([[(xb + Lb * i / 4, yb), (xb + Lb * (i + 1) / 4, yb), (xb + Lb * (i + 1) / 4, yb + 1.2),
                          (xb + Lb * i / 4, yb + 1.2)]], INK if i % 2 == 0 else "FFFFFF", INK, 0.15, "north_scale"))
    items.append(T_(u"0", xb, yb - 2.8, 2.0, INK, "north_scale", False, "C"))
    items.append(T_(u"%d m" % bar, xb + Lb, yb - 2.8, 2.0, INK, "north_scale", False, "C"))
    items.append(T_(u"1:%s" % format(den, ",d"), xb, yb + 3.0, 2.8, INK, "north_scale", True))

    log.append(u"sources (log only): " + D["sources"]["osm"] + u"; hubs, places, hub sections: CityLink v13 "
               u"(SUBMISSION_SON p9); neighbourhoods: OpenStreetMap admin_level 8 (Data/bergama_osm.osm), main fabric = the most common MapBase fabric type of the buildings in site_alan; proposal: MasterplanBase (B19_setB_layers259.svg); context: MapBase; nodes: Data/section_lines.json; ideas N2, N4: Aras 14 Nov")
    orig = G["pc_frame_check"]                           # the cards and the column sit outside the map frame by design
    G["pc_frame_check"] = lambda its, box, lg, tw_=None: orig(its, box, lg, tw_, skip=G["PC_SHEET_LAYERS"] + (
        "cards", "node_pointers"))
    clips = {"map": [[[(M.box[0], M.box[1]), (M.box[2], M.box[1]), (M.box[2], M.box[3]), (M.box[0], M.box[3])]]]}
    paths = G["pc_write"](lib, M, items, OUT_DIR, NAME, u"The six nodes along the spine", log, X["photos"] or None, clips)
    pdfs = [p_ for p_ in paths if p_.lower().endswith(".pdf")]
    if pdfs:
        G["pc_present"](pdfs[0], SLIDE, log)
    flags = [l for l in log if l.startswith(u"FLAG")]
    return u"%s\n%s %s, %d FLAG line(s), %.1f s" % (u"\n".join(log), GH_LABEL, VERSION, len(flags), time.time() - t0)


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
