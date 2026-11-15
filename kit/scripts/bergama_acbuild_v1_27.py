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

VERSION = "v1.27"   # v1.27 (Aras 15 Nov 20:07 "use solid element operations where necceseary"): every canopy plinth, node plinth and masterplan slab (terraces included) cuts the terrain mesh of each cut it stands in (Tapir CreateSolidElementLinks, subtraction); (Aras 20:08 "use retaining walls where neccesery") stone retaining walls along slab edges where the ground outside differs from the slab top by more than 0.60 m (ASSUMED)   # v1.26 (Aras 15 Nov 20:06 "dont do these kinda extereme angles keep it minimal like the second image"): fold rise 0.6 m (was 1.8 m), and no facet edge steeper than 8 deg (low corners on falling ground are raised to it, so every clearance still holds)   # v1.25 (Aras 15 Nov 20:05 "draw their roofs with roof tool columns with column tool, beams with beam tool etc. so intersections would look proper"): canopy facets = single-plane Roofs (pivot line through the low corner, slope of the facet plane), louvres = timber Beams (horizontal slats every 0.6 m under each facet); columns (Column tool), arms (Beam tool), plinths/decks/planters (Slab tool), glazed rooms (Wall + Window) as before; a facet Archicad refuses as a roof falls back to a mesh (FLAG)   # v1.24 (Aras 15 Nov 20:01 "use these settings for archicad sections"): his Section Selection Settings on every section (cut elements in their pens, uncut = uniform pen colour fill + line pen 81, fade distant elements on with line pen 102, no boundary contours); publishes once for the new settings   # v1.23 (Aras 15 Nov 20:00 "archicad is missing the ground in sections ... i want real 1:1 drawing in archicad"): the survey terrain mesh is built again, one per cut rectangle (10 m in front of the line to 200 m behind, survey contours + spot heights, solid with skirt), so every Archicad section has a cut ground and the hillside under its houses   # v1.22 (Aras 15 Nov 19:48 UTC "optimize the scripts to be much much faster", item 3 "run the Rhino-only slides alongside the Archicad steps"): run from the chain (__main__), the Rhino part (survey read, TIN) runs as before, then the Archicad part (pure Python + Tapir, no Rhino call) goes on in a background thread so Rhino is free for the next page script; the log reads "RUNNING ..." until it ends (same lines as before); a file cached/_chain/acbuild_foreground.txt keeps the old one-piece run; the Grasshopper button runs in one piece as before; v1.21 (v1.18 run 15 Nov 19:23 UTC: no bridge and no stepped terrace was built: his bridge outlines (kopruler path) and stepped-terrace outlines (begum su merdiven outline) are drawn without fill): those layers are built from their closed outlines (the outermost rings only, MasterplanBase v1.9 keeps the paint-less bridge rings); a bridge as a 0.50 m stone deck whose top is the highest survey ground under its outline (the banks it spans, not the river bed); BUILD_SIG geometry-9; v1.20   # v1.20 (Aras 15 Nov 19:18: the publisher set may be PDF): published PDFs count as the kept output   # v1.19 (Aras 15 Nov 19:09-19:11 UTC "1.2meter depth is fine however think it like 15x30 steps merge into single seating", "circulation wise"): his stepped terraces (begum su merdiven, the light stone picture) built as seating tiers stepping down to the river: each tier 1.20 m deep = four 30 cm treads merged, 0.48 m high = four 12 cm risers (Aras 19:13 "make the height of the steps is 12"; the 12 x 30 stair pitch kept), tiers cut from his own outline across the direction to the nearest point of his river outline (su_outline), lowest tier on the lowest survey ground of the piece, none above the highest; the stair aisles themselves are not placed (no aisle drawn in his masterplan); materials by each layer's own picture colour: teras = wood deck ("decks are wooden"), iskele kenari = grey paving CECFCE; v1.18 (Aras 15 Nov 18:12-18:17 UTC texture legend: "this stands for regular bridges", "historic buildings are in a shade of red", "our buildings are white blues are glasses", "these are decksn", "this is shading", "these are reed beds", "this is stepped terrace that goes into the river"): Archicad surfaces + building materials named "Bergama ..." in his legend colours (median colours sampled from his legend pictures), given to the elements as they are made: bridges (kopruler pieces) stone, stepped terraces (teras, begum su merdiven) light stone, decks (iskele kenari, canopy decks, planters, louvres) timber, reed beds (su bitkii) reed green, canopy facets white, Y columns grey frame, our buildings (node buildings, glazed rooms) white, historic buildings (sacred / monument houses, Kızıl Avlu) red; every glass surface of the project in his glass blue; an element Tapir refuses with a material is made again without it (FLAG); BUILD_SIG geometry-7 (one rebuild); v1.17 (Aras 15 Nov 17:24 UTC "any drawing that has building in it you should use the drawing that comes out of archicad"): the node building FLOOR PLANS from Archicad too: one Archicad story per floor of each node building (Tapir SetStories; story 0 kept, story level lines off in the sections), so each floor plan cuts its own building; a View Map view <N>-P<floor> per story, published with the sections (one-time Organizer step again), two registration squares (1.0 m and 0.5 m) 6 m off opposite corners of the building on every floor; BUILD_SIG geometry-6 (one rebuild); v1.16 (Aras 15 Nov 17:32 UTC "make sure archicad drawing is %100 pinpoint accurate to our masterplan"): his master.svg pieces inside the working area built in Archicad on his own points (slabs per layer, on the survey ground), canopies held within 0.05 m of his kanopi line, and an accuracy check after every build: each piece read back from Archicad and compared with master.svg, any point more than 5 cm off FLAGged, report in mp_accuracy.json; BUILD_SIG geometry-5 (one rebuild); v1.15 (Aras 15 Nov 17:27 UTC "draw these buildings in archicad and insert that drawing into all sections ... archicad is hella lot more detailed"): the context houses get more detail for the section elevations: a door on the ground floor of the longest wall a cut sees, windows on every wall a cut sees at any angle, balconies (slab + rail) on every other window bay of blocks of 3+ floors, a cornice band under every flat roof; a house with no recorded floor count is built as 1 floor (ASSUMED, logged) instead of left out; sizes are drawing rules, not surveyed; BUILD_SIG geometry-4 (one rebuild); v1.14 (Aras 15 Nov 17:24 UTC "any drawing that has building in it you should use the drawing that comes out of archicad"): the six node buildings built in Archicad as the node slides design them (placed by Perspectives, rooms from nodes common BUILD), each with a cut view <N>-BX and an elevation view <N>-BE in the "Bergama sections" folder (published with the sections); v1.13 = v1.13 (Aras 15 Nov 16:31-16:32 UTC "Make canopies top view match with masterplan", "Get structrual idea from the photo i have sent you and invent from there"): every canopy built on his own filled kanopi ring (no hull, no merging, outline within 0.25 m), facets by ear clipping with his fold ends on the outline, low / high vertices alternating round it, Y columns under the low vertices 1.2 m inside (4-10 m apart, arms toward the neighbouring vertices), plinth + deck bays between the columns; rooms and planters only where they fit inside; v1.12 (v1.11 publish run: 10.5 min for 13 DWGs): no vector sun shadows in the section views; a change of the view settings (SEC_SIG) publishes once even when the model is unchanged   # v1.11 (run of v1.10: the Archicad 29 API refused "CutPlane" too): sections listed through Tapir GetElementsByType (CutPlane)   # v1.10 (Aras 15 Nov 15:00 "you need to make archicad runs faster"): the model is rebuilt only when its inputs changed (buildings from MapBase, cut lines, masterplan canopies, Sections levels, BUILD_SIG) or Archicad holds other element counts; with the model and sections unchanged nothing is published either (the last DWGs are kept); model time logged; sections listed as element type CutPlane (v1.9 run: "Section" is not an API type)   # v1.9 (15 Nov: Archicad reopened from a recovery file: new GUIDs, the build doubled, 9 section views twice): the previous model is cleared by element type (windows, walls, slabs, roofs, meshes, columns, beams), not by recorded GUIDs; when the project\'s sections differ from the recorded ones, all sections and the "Bergama sections" View Map folder are made again (FLAG: refresh the publisher set)   # v1.8 (15 Nov: a refreshed publisher set held the whole project as PDF + DWG and Archicad hung an hour; the pln reopened without the build after a restart): the project is saved (Tapir SaveProject) before publishing, and only the set's items of our sections are published (selectedNavigatorItemIds); a set holding other items is not published whole   # v1.7 (Sections thread, run of v1.28.2: houses up the hill float, the survey TIN does not reach that hill): the ground behind each cut in depth bands (10-50, 50-100, 100-200, 200-400 m, 400 m to the farthest building), each the highest survey ground of the band raised to the base of every building standing in it, so every house has ground under it; written to acbuild.json cuts[].bands   # v1.6 (also: the ground-behind profile reaches 1000 m, as houses of other cuts beyond 200 m show in the sections); v1.6 (Aras 15 Nov 09:52-10:29 "draw our canopies much better like designed ones" / "Some closed areas underneath" / canopies in Archicad "yes please"): his master.svg canopies (kanopi layer) built as his reference: folded triangle-facet roof (meshes) with a timber louvre layer under it, Y steel columns (trunk + 2 arms) under the valleys on a 12 m bay, timber deck on a stone plinth bay by bay, a glazed room in every other bay where the floor is >= Q500 + 0.60 m, timber planters in the open bays; heights as Sections v1.28.2 (DfT 2.30 m clear, EA 0.60 m over Q500, ridge +1.8 m ASSUMED)   # v1.5 + Kızıl Avlu: the main hall outline(s) from the MasterplanBase cache (Sections library red_hall_load), roofless walls 19 m (Wikipedia, Red Basilica: "Its walls still survive up to a height of 19 metres"), no windows, no roof; v1.5 (15 Nov run 7: houses beyond the 200 m depth drawn as floating outlines): no marked distant area (only the 200 m behind each cut is drawn); publishing may take 30 min (the set grew)   # v1.4 v1.4 (15 Nov: Sections v1.18 moved the N4 lines): the Archicad origin is kept from the first run; a section whose line moved is deleted and made again on the new line (its view too), with a FLAG to refresh the publisher set   # v1.3 (run 4: houses 200 m behind stood in the sky, the hill under them was not drawn): per cut the ground behind (highest survey ground 10-200 m behind, every 2 m) written to acbuild.json for SectionsAC   # v1.2 (SectionsAC run 3: the DWGs held only the roofs = the one element type without a BG layer, so the BG layers are not shown in the views): every element on the tool default layers; registration blocks at -50 m (found by geometry); no terrain mesh (our ground is drawn instead)   # v1.1 (14 Nov run 1): mesh without layerIndex (Tapir schema), hipped roofs as one-level polyroofs, footprints cleaned (slab failures)
GH_LABEL = "AcBuild"
OUT_FOLDER = "bergama_archicad"
LOG_NAME = "bergama_acbuild_log.txt"
GH_INPUTS = {}
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
CACHE_DIR = os.path.join(BERGAMA_ROOT, "cached", OUT_FOLDER)
OUT_DIR = CACHE_DIR
DWG_DIR = os.path.join(CACHE_DIR, "dwg")
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
LIB_GLOB = os.path.join(BERGAMA_ROOT, "scripts", "bergama_sections_v*.py")

PORTS = range(19723, 19744)        # Archicad's JSON API ports (the first Archicad opened takes 19723)
SHADOWS = False                    # v1.12: vector sun shadows off in the section views (publish took 10.5 min)
SEC_SIG = "sections-aras-2026-11-15"    # v1.12: change with the section view settings (forces one publish)
BUILD_SIG = "acbuild-geometry-seo-ret-1"   # v1.27: SEO terrain cuts + retaining walls; v1.26: minimal folds; v1.25: canopies with Roof/Beam tools; v1.21: bridges + stepped terraces from outlines; v1.19: seating tiers; v1.18: materials; v1.17: building stories; v1.16: masterplan pieces; v1.15: house detail;   # v1.14: node buildings; v1.13 = v1.13: canopies on his outlines; v1.10: change when the element-making code changes (forces a rebuild)
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
WALL_T, PLINTH = 0.3, 1.0          # m wall thickness; m the walls start below the ground at the centroid
GRID_M = 2.0                       # m: spot heights thinned to one per cell for the terrain mesh
REG_Z = -50.0                       # m above sea level: the registration blocks sit here (below every survey height)
SUN = (135.0, 35.0)                # deg azimuth to the cut plane, altitude: the shadow light (a drawing choice)
CHUNK = 400                        # elements per Tapir call
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
            try:
                r = self.t(name, {key: part})
                lst = r.get("elements") or r.get("elementIds") or []
            except Exception as ex:
                lst = [{"error": {"message": u"%s" % ex}}] * len(part)
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


# ================================================================ v1.18: his texture legend as Archicad materials
# (Aras 15 Nov 18:12-18:17 UTC); colours = median colour of each legend picture he sent (or of its named part), hex
MAT = {"bridge_stone": ("Bergama bridge stone", "928D8B", "Matte", 0),       # 18:12 bridges (stone paving)
       "terrace_stone": ("Bergama stepped terrace stone", "E5DFD7", "Matte", 0),   # 18:15 stepped terrace
       "timber": ("Bergama timber deck", "BAA89A", "Matte", 0),             # 18:13 decks
       "reed": ("Bergama reed bed", "707D56", "Matte", 0),                  # 18:14 reed beds (the green blades)
       "shade_white": ("Bergama shading facet white", "F4F4F4", "Matte", 0),   # 18:14 shading facets
       "frame_grey": ("Bergama shading frame grey", "818282", "Matte", 0),     # 18:14 shading frame lines
       "our_white": ("Bergama our building white", "F7F7F7", "Matte", 0),     # 18:13 our buildings
       "heritage_red": ("Bergama historic red", "B56D61", "Matte", 0),       # 18:13 historic buildings (red roof)
       "quay_grey": ("Bergama quay paving grey", "CECFCE", "Matte", 0)}     # v1.19: iskele kenari's own picture        # 18:13 historic buildings (red roof)
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


def _rgb(h):
    return {"red": int(h[0:2], 16) / 255.0, "green": int(h[2:4], 16) / 255.0, "blue": int(h[4:6], 16) / 255.0}


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
        bm = [dict(name=nm, cutSurfaceIndex=int(sf[nm]["index"])) for nm, h, ty, tr in MAT.values() if nm in sf]
        ac.t("CreateBuildingMaterials", {"overwriteExisting": True, "buildingMaterialDataArray": bm})
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


RET_MIN_M, RET_T_M, RET_FOOT_M, RET_SEG_M = 0.60, 0.30, 0.50, 4.0   # v1.27: retaining walls (threshold ASSUMED)


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


def build_nodes(ac, miss, log, xy, z0, NB):
    """the node buildings in Archicad (DESIGN, as the node slides and the perspectives): stone plinth, floor slabs,
    walls bay by bay (glazed every other bay, a window per storey), room partitions by area along the length, folded
    roof facets (meshes, as the canopies); N4 = the raised canopy platform (deck on columns, folded roof)"""
    made, plin, slabs, walls, glz, parts, facets, cols = [], [], [], [], [], [], [], []
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
            "su_bitkii": (0.05, 0.0), "su": (0.05, 0.0), "ana_su": (0.05, 0.0)}
MP_SKIP = ("kanopi", "teras_-_canopy", "desings", "existing_buildings", "builts2", "existing_roads", "heritage",
           "kizil_avlu", "PLANTING_v13_1")        # canopies + node buildings built above; context and trees not his
MP_TOL_M = 0.05                                    # FLAG a piece whose Archicad outline is further off than this
MP_MAX_M2 = 100000.0                               # his sheet / picture frames (pages common PC_MP_MAX_M2 order)
SITE_REC = []                                      # (guid, layer, ring) for the read-back


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
    for key, pieces in J.get("layers", {}).items():
        parts = key.split("/")
        if "su_outline" in parts:                          # v1.19: his river outline, for the tier direction
            for p in pieces:
                RIVER_PTS.extend(tuple(v[:2]) for v in p[4])
        nm = next((p_ for p_ in reversed(parts) if p_ in MP_SLABS), None)
        if "kopruler" in parts:
            nm = "kopruler"                                # v1.21: every bridge piece is a bridge (0.50 m)
        if nm is None:
            if not any(p_ in MP_SKIP for p_ in parts):
                n_skip[parts[-1]] = n_skip.get(parts[-1], 0) + len(pieces)
            continue
        for p in pieces:
            R = [tuple(v[:2]) for v in p[4]]
            ol_ = nm in OUTLINE_LAYERS or any(p_ in OUTLINE_LAYERS for p_ in parts)   # v1.21: outline-only layers
            if p[0] not in ("r", "a") or (not p[1] and not (ol_ and p[0] == "r")) or len(R) < 3 or \
                    abs(area(R)) < 0.5 or abs(area(R)) > MP_MAX_M2:
                continue
            if p[0] == "a" and len(R) == 4:
                continue                                   # a picture's own rectangle (nodes common v8.2)
            c = (sum(q[0] for q in R) / len(R), sum(q[1] for q in R) / len(R))
            if wa and not any(_inpoly(c, W) for W in wa):
                n_out += 1
                continue
            H = clean(R[:-1] if R[0] == R[-1] else R)
            if len(H) >= 3:
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
    gs_ = _reg_ops(ac.create("CreateSlabs", "slabsData", data, u"masterplan pieces (his outlines)"), data)
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
    SEO_OPS[:], SEO_TERR[:], CANOPY_REC[:] = [], [], []   # v1.27: fresh per run (a re-run in the same Rhino kept old ones)
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
    box = (min(p[0] for p in allp), min(p[1] for p in allp), max(p[0] for p in allp), max(p[1] for p in allp))
    survey = L_["read_survey"](box, log)
    spots = {}
    for name in L_["SURVEY_LAYERS"]:
        for pl in survey.get(name, []):
            for p in pl:
                if p[2] > 1.0:
                    spots[(int(p[0] // GRID_M), int(p[1] // GRID_M))] = p
    log.append(u"survey heights: %d (one per %.0f m cell)" % (len(spots), GRID_M))
    contours = [pl for name in L_["SURVEY_LAYERS"] if name.startswith("EGRI") for pl in survey.get(name, [])
                if len(pl) >= 2 and min(p[2] for p in pl) > 1.0]

    def inside(p, r):
        s, o = so(p, r[1], r[4], r[5])
        return -1e-6 <= s <= r[3] + 1e-6 and -SIDE_M <= o <= BACK_M
    pts = list(spots.values())
    tin = L_["Tin"]([(p[0] - ox, p[1] - oy, p[2]) for p in pts])
    zmin_all = min(p[2] for p in pts) if pts else 0.0
    bld, skipped = [], 0
    for i, (b, x) in enumerate(zip(M["bld"], M.get("bld_x") or [[0, "", ""]] * len(M["bld"]))):
        ring = [tuple(q) for q in b[0]]
        if len(ring) >= 2 and ring[0] == ring[-1]:
            ring = ring[:-1]
        ring = clean(ring)
        if len(ring) < 3 or abs(area(ring)) < 4.0 or not any(inside(q, r) for q in ring for r in rects):
            continue
        fl = int(x[0] or 0)
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
                        cut=bool(cut_by), views=[r for r in rects if any(inside(q, r) for q in ring)]))
    for x0_, y0_, x1_, y1_, ring, h_, _f in (L_["red_hall_load"](log) if "red_hall_load" in L_ else []):
        ring = clean([tuple(q) for q in ring])
        if len(ring) < 3 or not any(inside(q, r) for q in ring for r in rects):
            continue
        if area(ring) < 0:
            ring = ring[::-1]
        cx, cy = sum(q[0] for q in ring) / len(ring), sum(q[1] for q in ring) / len(ring)
        zb = tin.z(cx - ox, cy - oy)
        bld.append(dict(ring=ring, fab=u"Kızıl Avlu", fl=-1, h=h_, z=zb if zb is not None else zmin_all,
                        cut=False, views=[r for r in rects if any(inside(q, r) for q in ring)]))
        log.append(u"Kızıl Avlu hall: %d points, walls %.0f m, base z %.1f m" % (len(ring), h_, bld[-1]["z"]))
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
    NB = node_buildings(log)                              # v1.14: the node buildings (placed by Perspectives)
    SP = site_pieces(log)                                 # v1.16: his masterplan pieces in the working area
    BSECS = node_secs(NB)
    hsrc = [BUILD_SIG, MESH, [(nm, list(A), list(B)) for nm, A, B, Ln, u, n in rects], NB,
            [(b["ring"], b["fab"], b["fl"], b["h"], b["z"], b["cut"], [r[0] for r in b["views"]]) for b in bld],
            [(nm, [list(q) for q in R]) for nm, R, H in SP]]          # v1.16
    for fp in sorted(glob.glob(os.path.join(BERGAMA_ROOT, "cached", "bergama_masterplanbase*", "*.json"))) + [
            os.path.join(BERGAMA_ROOT, "cached", "bergama_sections", "cuts.json")]:
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
    if not reuse:
        # v1.9: cleared by element type, not by the GUIDs of the last run (15 Nov: Archicad reopened from a recovery
        # file with new GUIDs, and the build was doubled). Bergama_AC.pln holds only what AcBuild makes.
        if "DeleteElements" not in miss:
            try:
                ac.t("ChangeWindow", {"windowType": "FloorPlan", "storyIndex": 0})
            except Exception:
                pass
            n_del = {}
            for ty in CLEAR_TYPES:
                try:
                    gs = [e["elementId"]["guid"] for e in ac.api("API.GetElementsByType", {"elementType": ty}).get(
                        "elements", []) if e.get("elementId")]
                except Exception as ex:
                    log.append(u"FLAG %s elements not listed (%s): not cleared" % (ty, ex))
                    continue
                for i in range(0, len(gs), CHUNK):
                    try:
                        ac.t("DeleteElements", {"elements": [{"elementId": {"guid": g}} for g in gs[i:i + CHUNK]]})
                    except Exception as ex:
                        log.append(u"FLAG %s elements not all deleted: %s" % (ty, ex))
                        break
                n_del[ty] = len(gs)
            log.append(u"previous model cleared by type: %s" % u", ".join(u"%d %s" % (n_del[k], k) for k in n_del))
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
        # ---- terrain: one mesh per cut rectangle
        meshes = []
        for name, A, B, Ln, u, n in rects:
            corner = [(A[0] + n[0] * d + u[0] * s, A[1] + n[1] * d + u[1] * s)
                      for s, d in ((0.0, -SIDE_M), (Ln, -SIDE_M), (Ln, BACK_M), (0.0, BACK_M))]
            poly = []
            for c in corner:
                z = tin.z(c[0] - ox, c[1] - oy)
                if z is None:
                    q = min(pts, key=lambda p: (p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2)
                    z = q[2]
                poly.append(dict(xy(c), z=round(z - z0, 3)))
            r = (name, A, B, Ln, u, n)
            sub = [{"coordinates": [dict(xy(p), z=round(p[2] - z0, 3)) for p in pl if inside(p, r)]} for pl in contours]
            sub = [s_ for s_ in sub if len(s_["coordinates"]) >= 2]
            sub += [{"coordinates": [dict(xy(p), z=round(p[2] - z0, 3))]} for p in pts if inside(p, r)]
            meshes.append(dict(level=0.0, polygonCoordinates=poly, sublines=sub, skirtType="SolidBodyWithSkirt",
                               skirtLevel=5.0, ridges="AllSmooth"))      # CreateMeshes takes no layerIndex (run 1: 4002)
        if MESH and "CreateMeshes" not in miss:
            for m in meshes:
                g = ac.create("CreateMeshes", "meshesData", [m], u"terrain mesh (%d level lines)" % len(m["sublines"]))
                if not g[0]:                                          # retry with the contour lines only
                    m["sublines"] = [s_ for s_ in m["sublines"] if len(s_["coordinates"]) >= 2] or m["sublines"][:1]
                    g = ac.create("CreateMeshes", "meshesData", [m], u"terrain mesh, contours only")
                made += [x for x in g if x]
                SEO_TERR.extend((x, r) for x in g if x)     # v1.27

        # ---- walls (+ windows on the walls a cut looks at)
        walls, wmeta = [], []
        for bi, b in enumerate(bld):
            top_extra = 0.6 if b["fl"] >= FLAT_FLOORS else 0.0
            R = b["ring"]
            for a, c in zip(R, R[1:] + R[:1]):
                ln = math.hypot(c[0] - a[0], c[1] - a[1])
                if ln < 0.3:
                    continue
                walls.append(dict(begCoordinate=xy(a), endCoordinate=xy(c), zCoordinate=round(b["z"] - PLINTH - z0, 3),
                                  height=round(b["h"] + PLINTH + top_extra, 3), thickness=WALL_T,
                                  referenceLineLocation="Outside",
                                  _mat="heritage_red" if b["fab"] in HERITAGE_FABS else None, **L("BG buildings")))
                on = ((c[1] - a[1]) / ln, -(c[0] - a[0]) / ln)        # outward normal (ring counter-clockwise)
                faces = b["fl"] > 0 and any(on[0] * -r[5][0] + on[1] * -r[5][1] > 0.05 for r in b["views"])
                wmeta.append((bi, ln, faces, a, c, on))
        wg = ac.create("CreateWalls", "wallsData", walls, u"walls") if "CreateWalls" not in miss else []
        made += [g for g in wg if g]
        wins, doors, bals, rails = [], [], [], []
        door_wall = {}                                # v1.14: per building the longest wall a cut sees gets the door
        for g, (bi, ln, faces, a_, c_, on_) in zip(wg, wmeta):
            if g and faces and ln >= DOOR_W + 2.0 and ln > door_wall.get(bi, (None, 0.0))[1]:
                door_wall[bi] = (g, ln)
        for g, (bi, ln, faces, a_, c_, on_) in zip(wg, wmeta):
            if not g or not faces or ln < WIN_W + 1.0:
                continue
            b = bld[bi]
            fh = b["h"] / b["fl"]
            nw = max(1, int((ln - 1.0) // WIN_STEP))
            x0 = (ln - (nw - 1) * WIN_STEP) / 2.0
            has_door = door_wall.get(bi, (None,))[0] == g
            if has_door:
                doors.append(dict(ownerWallId={"guid": g}, width=DOOR_W, height=DOOR_H, sillHeight=PLINTH,
                                  centerOffset=round(ln / 2.0, 2)))
            u_ = ((c_[0] - a_[0]) / ln, (c_[1] - a_[1]) / ln)
            for i in range(b["fl"]):
                for j in range(nw):
                    xo = x0 + j * WIN_STEP
                    if i == 0 and has_door and abs(xo - ln / 2.0) < (DOOR_W + WIN_W) / 2.0 + 0.3:
                        continue                      # the door's place on the ground floor
                    wins.append(dict(ownerWallId={"guid": g}, width=WIN_W, height=round(min(WIN_H, fh * 0.5), 2),
                                     sillHeight=round(PLINTH + i * fh + min(WIN_SILL, fh * 0.3), 2),
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
        for b in bld:
            if b["fl"] < 0:
                continue                              # Kızıl Avlu: the roofless Roman hall
            poly = [xy(q) for q in b["ring"]]
            top = round(b["z"] + b["h"] - z0, 3)
            if b["fl"] >= FLAT_FLOORS:
                flats.append(dict(level=top, thickness=0.3, polygonCoordinates=poly, **L("BG buildings")))
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
                roofs.append(dict(level=top, thickness=0.25, polygonCoordinates=poly, eavesOverhang=EAVE_M,
                                  levels=[{"levelHeight": 20.0, "levelAngle": math.radians(ROOF_DEG)}]))   # polyroof (hip)
            if b["cut"]:
                fh = b["h"] / b["fl"]
                slabs += [dict(level=round(b["z"] + i * fh - z0, 3), thickness=0.25, polygonCoordinates=poly,
                               **L("BG buildings")) for i in range(b["fl"])]
        if "CreateRoofs" not in miss and roofs:
            rg = ac.create("CreateRoofs", "roofsData", roofs, u"hipped roofs")
            made += [g for g in rg if g]
            flats += [dict(level=r_["level"], thickness=0.3, polygonCoordinates=r_["polygonCoordinates"],
                           **L("BG buildings")) for r_, g in zip(roofs, rg) if not g]   # a roof Archicad refused: flat
        if "CreateSlabs" not in miss:
            made += [g for g in ac.create("CreateSlabs", "slabsData", flats + slabs, u"flat roofs + cut floor slabs") if g]

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
            made += build_site(ac, miss, log, xy, z0, tin, ox, oy, SP)
            site_accuracy(ac, log, ox, oy)                # v1.16: read back + compare, FLAG over 5 cm
        except Exception as ex:
            import traceback
            log.append(u"FLAG masterplan pieces not built (%s: %s) %s" % (type(ex).__name__, ex,
                                                                          traceback.format_exc()[-400:]))
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
    if not reuse and SEO_TERR and SEO_OPS:
        # v1.27 (Aras 15 Nov 20:07 "use solid element operations where necceseary"): every plinth, terrace and
        # masterplan slab cuts the terrain mesh it stands in (Solid Element Operation, subtraction), so the cut ground
        # in a section stops at their faces instead of running through them
        links = [dict(targetId={"guid": tg}, operatorId={"guid": og}, operation="Subtraction")
                 for tg, r in SEO_TERR for og, P, _lv in SEO_OPS
                 if P and any(inside((q[0] + ox, q[1] + oy), r) for q in P)]   # stored in Archicad coordinates
        n_ok = 0
        for i in range(0, len(links), CHUNK):
            try:
                rr = ac.t("CreateSolidElementLinks", {"solidLinks": links[i:i + CHUNK]})
                n_ok += sum(1 for e in (rr.get("executionResults") or []) if isinstance(e, dict) and e.get("success"))
            except Exception as ex:
                log.append(u"FLAG solid element operations not made (%s)" % ex)
                break
        log.append(u"solid element operations: %d of %d terrain cuts by plinths, terraces and masterplan slabs" % (
            n_ok, len(links)))
    log.append(u"model: %.0f s" % (time.time() - tp))
    # ---- sections (kept between runs)
    secs = old.get("sections") or {}
    if "CreateSections" not in miss:
        # v1.9: the sections in the project must be exactly the ones recorded; else all are made again (15 Nov:
        # after a recovery the project held 21 views with 9 names twice and none of the recorded GUIDs)
        try:
            r_ = ac.t("GetElementsByType", {"elementType": "CutPlane"})     # v1.11: Tapir's list (the AC 29 API
            have = [e["elementId"]["guid"] for e in (r_.get("elements") or [])  # refuses "Section" and "CutPlane")
                    if isinstance(e, dict) and e.get("elementId")]
        except Exception as ex:
            have = None
            log.append(u"FLAG sections not listed (%s): kept as recorded" % ex)
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
                       u"\"%s\" in (format DWG), Ctrl+S, then press AcBuild again" % (
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
                    secs.pop(k, None)
                    (old.get("views") or {}).pop(k, None)
                log.append(u"FLAG sections %s: their lines moved, made again on the new lines. In Archicad (Window > "
                           u"Palettes > Organizer): in the publisher set %s delete its folder and drag the View Map "
                           u"folder \"%s\" in again (format DWG), then press AcBuild again" % (
                               u", ".join(moved), PUB_SET, VIEW_FOLDER))
        new = [(name, A, B) for name, A, B, Ln, u, n in rects if name not in secs]
        if new:
            gs_ = ac.create("CreateSections", "sectionsData", [
                dict(startCoordinate=xy(A), endCoordinate=xy(B), depth=BACK_M, name=name, id=name)
                for name, A, B in new], u"sections")
            secs.update(dict((nm[0], g) for nm, g in zip(new, gs_) if g))
        newb = [(name, A, B, dp) for name, A, B, dp in BSECS if name not in secs]   # v1.14: the building views
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
                   useElementPens=True,
                   useUncutSurfaceFill=True, modelUncutSurfaceFillType="PenColor",
                   modelUncutSurfaceFillBackgroundPenIndex=-1, useOneModelPen=True, modelPenIndex=81, transparent=False,
                   markedDistantArea=True, useUncutSurfaceFillInDistantArea=True,
                   distantAreaUncutSurfaceFillBackgroundPenIndex=-1, useOneDistantAreaPen=True, distantAreaPenIndex=102,
                   boundaryDisplayMode="NoContours")
        try:
            ac.t("SetSectionsAndElevationsDetails", {"elementsWithDetails": [
                {"elementId": {"guid": g}, "details": det} for g in secs.values()]})
            log.append(u"section settings (Aras 15 Nov): limited depth %.0f m, uncut pen colour fill + pen 81, fade "
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
        dw = [os.path.basename(x)[:-4] + ".dwg" for e_ in ("dwg", "pdf")      # v1.20: a PDF set counts too
              for x in glob.glob(os.path.join(DWG_DIR, "**", "*." + e_), recursive=True)]
        if reuse and not old.get("remade") and old.get("published") and old.get("sec_sig") == SEC_SIG and \
                all(any(x.startswith(nm + " ") or x == nm + ".dwg" for x in dw) for nm in list(secs) + list(PVN)):
            published = True
            log.append(u"not published: model and sections unchanged, the DWGs of the last run kept")
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
                return any(re.search(u"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(nm), tx) for nm in list(secs) + list(PVN))
            ours = [it for it in leaves if is_ours(it)]
            miss_b = [nm for nm in [b_[0] for b_ in BSECS if b_[0] in secs] + sorted(PVN) if not any(
                re.search(u"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(nm),
                          u" %s %s " % (it.get("uiId") or u"", it.get("name") or u"")) for it in leaves)]
            if miss_b:                                    # v1.14: one-time Organizer step for the building views
                log.append(u"FLAG ONE-TIME STEP in Archicad (the node building views): Window > Palettes > Organizer; "
                           u"left = View Map, right = Publisher Sets > %s; drag the View Map folder \"%s\" onto the "
                           u"set again (it now also holds %s); keep format DWG; Ctrl+S; then press AcBuild again" % (
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
                               u"everything except the \"%s\" views, format DWG, Ctrl+S, then press AcBuild again" % (
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
                       u"drag the View Map folder \"%s\" into it; Publish Properties: Save files, format DWG; then "
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
                       dwg_dir=DWG_DIR, layers=list(LAYERS), canopies=CANOPY_REC, elements=made, build_sig=sig, sec_sig=SEC_SIG,
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
    print(_run_bg())                                      # v1.22: the Archicad part in the background
