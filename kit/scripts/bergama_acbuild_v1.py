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

VERSION = "v1"
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
PUB_SET = "Bergama_Sections"       # publisher set name (made once by hand: DWG, the "Bergama sections" views)
VIEW_FOLDER = "Bergama sections"
BACK_M = 200.0                     # m behind the cut: the Sections script's BACK_M (v1.7)
SIDE_M = 10.0                      # m in front of the line still modelled (the buildings the line cuts)
STOREY = {"sacred": 5.0, "monument": 5.0, "civic": 3.5, "industry": 4.5}   # else STOREY_M
STOREY_M = 3.0
INDUSTRY_TAGS = ("industrial", "warehouse", "factory", "manufacture")
FLAT_FLOORS = 4                    # Sections FLAT_ROOF_FLOORS: from 4 floors a flat roof with a 0.6 m parapet
ROOF_DEG, EAVE_M = 30.0, 0.4       # Sections ROOF_PITCH_DEG, EAVE_M (drawing rule)
WIN_W, WIN_H, WIN_SILL, WIN_STEP = 1.2, 1.4, 0.9, 3.0   # Sections drawing rule (not surveyed)
WALL_T, PLINTH = 0.3, 1.0          # m wall thickness; m the walls start below the ground at the centroid
GRID_M = 2.0                       # m: spot heights thinned to one per cell for the terrain mesh
REG_Z = 0.0                        # m above sea level: the registration blocks sit here (below every survey height)
SUN = (135.0, 35.0)                # deg azimuth to the cut plane, altitude: the shadow light (a drawing choice)
CHUNK = 400                        # elements per Tapir call
LAYERS = ("BG terrain", "BG buildings", "BG reg")


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

    def api(self, cmd, params=None):
        b = {"command": cmd}
        if params is not None:
            b["parameters"] = params
        r = self._post(self.url, b)
        if not r.get("succeeded"):
            raise RuntimeError(u"%s failed: %s" % (cmd, json.dumps(r.get("error"))[:300]))
        return r.get("result") or {}

    def t(self, name, params=None):
        p = {"addOnCommandId": {"commandNamespace": "TapirCommand", "commandName": name}}
        if params is not None:
            p["addOnCommandParameters"] = params
        r = self.api("API.ExecuteAddOnCommand", p).get("addOnCommandResponse") or {}
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
        for i in range(0, len(items), CHUNK):
            part = items[i:i + CHUNK]
            try:
                r = self.t(name, {key: part})
                lst = r.get("elements") or r.get("elementIds") or []
            except Exception as ex:
                lst = [{"error": {"message": u"%s" % ex}}] * len(part)
            for e in lst:
                g = (e.get("elementId") or {}).get("guid") if isinstance(e, dict) else None
                out.append(g)
                if not g:
                    err.append(json.dumps(e)[:200])
        self.log.append(u"%s: %d made%s" % (what, sum(1 for g in out if g), u"" if not err else
                                                u"; FLAG %d failed, first: %s" % (len(err), err[0])))
        return out


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


# ================================================================ main
def main():
    t0 = time.time()
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
        if len(ring) < 3 or not any(inside(q, r) for q in ring for r in rects):
            continue
        fl = int(x[0] or 0)
        if fl <= 0:
            skipped += 1
            continue
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
    log.append(u"buildings in the cut rectangles: %d (%d cut by a line); %d without a floor count left out" % (
        len(bld), sum(1 for b in bld if b["cut"]), skipped))

    # ---- clear the previous run, stories, layers
    os.makedirs(CACHE_DIR, exist_ok=True)
    pj = os.path.join(CACHE_DIR, "acbuild.json")
    old = {}
    if os.path.isfile(pj):
        with open(pj, encoding="utf-8") as f:
            old = json.load(f)
    gs = old.get("elements") or []
    if gs and "DeleteElements" not in miss:
        try:
            ac.t("ChangeWindow", {"windowType": "FloorPlan", "storyIndex": 0})
        except Exception:
            pass
        for i in range(0, len(gs), CHUNK):
            try:
                ac.t("DeleteElements", {"elements": [{"elementId": {"guid": g}} for g in gs[i:i + CHUNK]]})
            except Exception as ex:
                log.append(u"FLAG previous elements not all deleted: %s" % ex)
                break
        log.append(u"previous run: %d elements deleted" % len(gs))
    z0 = 0.0
    try:
        st = ac.t("GetStories")
        z0 = next((s_["level"] for s_ in st.get("stories", []) if s_.get("index") == 0), 0.0)
    except Exception as ex:
        log.append(u"FLAG stories not read (%s): story 0 taken at 0.00" % ex)
    log.append(u"story 0 at %+.2f m: element heights are given relative to it" % z0)
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
    L = lambda n_: {"layerIndex": lay[n_]} if n_ in lay else {}
    made = []

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
                           skirtLevel=5.0, ridges="AllSmooth", **L("BG terrain")))
    if "CreateMeshes" not in miss:
        for m in meshes:
            g = ac.create("CreateMeshes", "meshesData", [m], u"terrain mesh (%d level lines)" % len(m["sublines"]))
            if not g[0]:                                          # retry with the contour lines only
                m["sublines"] = [s_ for s_ in m["sublines"] if len(s_["coordinates"]) >= 2] or m["sublines"][:1]
                g = ac.create("CreateMeshes", "meshesData", [m], u"terrain mesh, contours only")
            made += [x for x in g if x]

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
                              referenceLineLocation="Outside", **L("BG buildings")))
            on = ((c[1] - a[1]) / ln, -(c[0] - a[0]) / ln)        # outward normal (ring counter-clockwise)
            faces = any(on[0] * -r[5][0] + on[1] * -r[5][1] > 0.2 for r in b["views"])
            wmeta.append((bi, ln, faces))
    wg = ac.create("CreateWalls", "wallsData", walls, u"walls") if "CreateWalls" not in miss else []
    made += [g for g in wg if g]
    wins = []
    for g, (bi, ln, faces) in zip(wg, wmeta):
        if not g or not faces or ln < WIN_W + 1.0:
            continue
        b = bld[bi]
        fh = b["h"] / b["fl"]
        nw = max(1, int((ln - 1.0) // WIN_STEP))
        x0 = (ln - (nw - 1) * WIN_STEP) / 2.0
        for i in range(b["fl"]):
            for j in range(nw):
                wins.append(dict(ownerWallId={"guid": g}, width=WIN_W, height=round(min(WIN_H, fh * 0.5), 2),
                                 sillHeight=round(PLINTH + i * fh + min(WIN_SILL, fh * 0.3), 2),
                                 centerOffset=round(x0 + j * WIN_STEP, 2)))
    if wins and "CreateWindows" not in miss:
        made += [g for g in ac.create("CreateWindows", "windowsData", wins, u"windows (walls facing a cut)") if g]

    # ---- roofs and slabs
    roofs, flats, slabs = [], [], []
    for b in bld:
        poly = [xy(q) for q in b["ring"]]
        top = round(b["z"] + b["h"] - z0, 3)
        if b["fl"] >= FLAT_FLOORS:
            flats.append(dict(level=top, thickness=0.3, polygonCoordinates=poly, **L("BG buildings")))
        else:
            roofs.append(dict(level=top, thickness=0.25, polygonCoordinates=poly, angle=math.radians(ROOF_DEG),
                              eavesOverhang=EAVE_M))
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

    # ---- registration blocks: s = 0 (0.4 m) and s = L (0.8 m), REG_Z ... REG_Z + 0.5
    regs = []
    for name, A, B, Ln, u, n in rects:
        for s, w in ((0.0, 0.4), (Ln, 0.8)):
            c = (A[0] + u[0] * s, A[1] + u[1] * s)
            sq = [(c[0] + (u[0] * a_ + n[0] * b_) * w / 2, c[1] + (u[1] * a_ + n[1] * b_) * w / 2)
                  for a_, b_ in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            regs.append(dict(level=round(REG_Z + 0.5 - z0, 3), thickness=0.5, polygonCoordinates=[xy(q) for q in sq],
                             **L("BG reg")))
    if "CreateSlabs" not in miss:
        made += [g for g in ac.create("CreateSlabs", "slabsData", regs, u"registration blocks") if g]

    # ---- sections (kept between runs)
    secs = old.get("sections") or {}
    if "CreateSections" not in miss:
        try:
            ac.t("ChangeWindow", {"windowType": "FloorPlan", "storyIndex": 0})
        except Exception as ex:
            log.append(u"floor plan not activated (%s)" % ex)
        new = [(name, A, B) for name, A, B, Ln, u, n in rects if name not in secs]
        if new:
            gs_ = ac.create("CreateSections", "sectionsData", [
                dict(startCoordinate=xy(A), endCoordinate=xy(B), depth=BACK_M, name=name, id=name)
                for name, A, B in new], u"sections")
            secs.update(dict((nm[0], g) for nm, g in zip(new, gs_) if g))
        det = dict(horizontalRange="Limited", effectVectorShadow=True, effectSunFrom3D=False, sunAzimuth=SUN[0],
                   sunAltitude=SUN[1], useUncutSurfaceFill=True, modelUncutSurfaceFillType="MaterialColorShaded",
                   markedDistantArea=True, storyHandleAppearance="None")
        try:
            ac.t("SetSectionsAndElevationsDetails", {"elementsWithDetails": [
                {"elementId": {"guid": g}, "details": det} for g in secs.values()]})
            log.append(u"section settings: limited depth %.0f m, vector sun shadows (az %.0f, alt %.0f deg), shaded "
                       u"material fills, marked distant area" % (BACK_M, SUN[0], SUN[1]))
        except Exception as ex:
            log.append(u"FLAG section settings not set (%s): Archicad defaults used" % ex)

    # ---- View Map views + publish
    views = old.get("views") or {}
    try:
        tree = ac.t("GetNavigatorItemTree", {"navigatorMapId": "ProjectMap"})
        found = {}

        def walk(o):
            if isinstance(o, dict):
                if o.get("name") in secs and "Section" in u"%s" % o.get("type") and o.get("navigatorItemId"):
                    found[o["name"]] = o["navigatorItemId"]
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(tree)
        todo = [nm for nm in secs if nm in found and nm not in views]
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
        if PUB_SET in sets:
            os.makedirs(DWG_DIR, exist_ok=True)
            ac.t("PublishPublisherSet", {"publisherSetName": PUB_SET, "outputPath": DWG_DIR})
            published = True
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
                       cuts=[dict(name=nm, A=list(A), B=list(B), L=round(Ln, 3)) for nm, A, B, Ln, u, n in rects],
                       sections=secs, views=views, view_folder=old.get("view_folder"), published=published,
                       dwg_dir=DWG_DIR, layers=list(LAYERS), elements=made), f, ensure_ascii=False, indent=1)
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
    print(write_log(_run()))
