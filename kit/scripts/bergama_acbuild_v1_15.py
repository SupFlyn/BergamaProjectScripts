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

VERSION = "v1.15"   # v1.15 (Aras 15 Nov 17:27 UTC "draw these buildings in archicad and insert that drawing into all sections ... archicad is hella lot more detailed"): the context houses get more detail for the section elevations: a door on the ground floor of the longest wall a cut sees, windows on every wall a cut sees at any angle, balconies (slab + rail) on every other window bay of blocks of 3+ floors, a cornice band under every flat roof; a house with no recorded floor count is built as 1 floor (ASSUMED, logged) instead of left out; sizes are drawing rules, not surveyed; BUILD_SIG geometry-4 (one rebuild); v1.14 (Aras 15 Nov 17:24 UTC "any drawing that has building in it you should use the drawing that comes out of archicad"): the six node buildings built in Archicad as the node slides design them (placed by Perspectives, rooms from nodes common BUILD), each with a cut view <N>-BX and an elevation view <N>-BE in the "Bergama sections" folder (published with the sections); v1.13 = v1.13 (Aras 15 Nov 16:31-16:32 UTC "Make canopies top view match with masterplan", "Get structrual idea from the photo i have sent you and invent from there"): every canopy built on his own filled kanopi ring (no hull, no merging, outline within 0.25 m), facets by ear clipping with his fold ends on the outline, low / high vertices alternating round it, Y columns under the low vertices 1.2 m inside (4-10 m apart, arms toward the neighbouring vertices), plinth + deck bays between the columns; rooms and planters only where they fit inside; v1.12 (v1.11 publish run: 10.5 min for 13 DWGs): no vector sun shadows in the section views; a change of the view settings (SEC_SIG) publishes once even when the model is unchanged   # v1.11 (run of v1.10: the Archicad 29 API refused "CutPlane" too): sections listed through Tapir GetElementsByType (CutPlane)   # v1.10 (Aras 15 Nov 15:00 "you need to make archicad runs faster"): the model is rebuilt only when its inputs changed (buildings from MapBase, cut lines, masterplan canopies, Sections levels, BUILD_SIG) or Archicad holds other element counts; with the model and sections unchanged nothing is published either (the last DWGs are kept); model time logged; sections listed as element type CutPlane (v1.9 run: "Section" is not an API type)   # v1.9 (15 Nov: Archicad reopened from a recovery file: new GUIDs, the build doubled, 9 section views twice): the previous model is cleared by element type (windows, walls, slabs, roofs, meshes, columns, beams), not by recorded GUIDs; when the project\'s sections differ from the recorded ones, all sections and the "Bergama sections" View Map folder are made again (FLAG: refresh the publisher set)   # v1.8 (15 Nov: a refreshed publisher set held the whole project as PDF + DWG and Archicad hung an hour; the pln reopened without the build after a restart): the project is saved (Tapir SaveProject) before publishing, and only the set's items of our sections are published (selectedNavigatorItemIds); a set holding other items is not published whole   # v1.7 (Sections thread, run of v1.28.2: houses up the hill float, the survey TIN does not reach that hill): the ground behind each cut in depth bands (10-50, 50-100, 100-200, 200-400 m, 400 m to the farthest building), each the highest survey ground of the band raised to the base of every building standing in it, so every house has ground under it; written to acbuild.json cuts[].bands   # v1.6 (also: the ground-behind profile reaches 1000 m, as houses of other cuts beyond 200 m show in the sections); v1.6 (Aras 15 Nov 09:52-10:29 "draw our canopies much better like designed ones" / "Some closed areas underneath" / canopies in Archicad "yes please"): his master.svg canopies (kanopi layer) built as his reference: folded triangle-facet roof (meshes) with a timber louvre layer under it, Y steel columns (trunk + 2 arms) under the valleys on a 12 m bay, timber deck on a stone plinth bay by bay, a glazed room in every other bay where the floor is >= Q500 + 0.60 m, timber planters in the open bays; heights as Sections v1.28.2 (DfT 2.30 m clear, EA 0.60 m over Q500, ridge +1.8 m ASSUMED)   # v1.5 + Kızıl Avlu: the main hall outline(s) from the MasterplanBase cache (Sections library red_hall_load), roofless walls 19 m (Wikipedia, Red Basilica: "Its walls still survive up to a height of 19 metres"), no windows, no roof; v1.5 (15 Nov run 7: houses beyond the 200 m depth drawn as floating outlines): no marked distant area (only the 200 m behind each cut is drawn); publishing may take 30 min (the set grew)   # v1.4 v1.4 (15 Nov: Sections v1.18 moved the N4 lines): the Archicad origin is kept from the first run; a section whose line moved is deleted and made again on the new line (its view too), with a FLAG to refresh the publisher set   # v1.3 (run 4: houses 200 m behind stood in the sky, the hill under them was not drawn): per cut the ground behind (highest survey ground 10-200 m behind, every 2 m) written to acbuild.json for SectionsAC   # v1.2 (SectionsAC run 3: the DWGs held only the roofs = the one element type without a BG layer, so the BG layers are not shown in the views): every element on the tool default layers; registration blocks at -50 m (found by geometry); no terrain mesh (our ground is drawn instead)   # v1.1 (14 Nov run 1): mesh without layerIndex (Tapir schema), hipped roofs as one-level polyroofs, footprints cleaned (slab failures)
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
SEC_SIG = "sections-noshadow-1"    # v1.12: change with the section view settings (forces one publish)
BUILD_SIG = "acbuild-geometry-4"   # v1.15: house detail;   # v1.14: node buildings; v1.13 = v1.13: canopies on his outlines; v1.10: change when the element-making code changes (forces a rebuild)
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
MESH = False                       # v1.2: the terrain mesh is not built (it would cover our sky and ground behind)


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
CAN_RISE_M = 1.80      # ridge above valley: DESIGN ASSUMPTION, UNVERIFIED (Sections v1.26)
CAN_T, CAN_LOUVRE_M = 0.15, 0.30                  # skin plate, louvre depth (design intent, Sections v1.28)
CAN_Y_FORK, CAN_Y_ARM_M = 0.6, 2.5                # Y fork at 60 % of the column, arm reach (design intent, v1.28)
CAN_PLINTH_M, CAN_DECK_M = 0.45, 0.12             # stone plinth, timber deck (design intent, v1.28.2)
CAN_PLANTER_M = 2.4                               # planter length (design intent, v1.28.2)
CAN_BAY_M = 0.0                                   # v1.13: no fixed bay; the columns follow each outline (below)
CAN_OUT_TOL = 0.25                                # v1.13: m, the built outline within this of his drawn kanopi line
CAN_COL_IN = 1.2                                  # v1.13: m, a column stands this far inside the outline (ours)
CAN_COL_MIN, CAN_COL_MAX = 4.0, 10.0              # v1.13: m, columns at least / a high vertex at most this far apart
CAN_EAVE_F = 0.6                                  # outline edge at valley + 0.6 x rise: folds to knife edges (ours)
CAN_GLASS_W, CAN_GLASS_STEP = 1.4, 1.5            # glazing panes, mullion step (design intent, v1.28.2 1.5 m)
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
        CANOPY_REC.append(dict(ring=[[round(p[0], 2), round(p[1], 2)] for p in H0], ground=round(min(gs), 3),
                               floor=round(min(floor0(g) for g in gz), 3),
                               under=round(min(low) - CAN_T - CAN_LOUVRE_M, 3), top=round(max(zv), 3)))
        for t3 in _ears(H):
            P3 = [H[k] for k in t3]
            if abs(area(P3)) < 0.3:
                continue
            roofs.append(dict(level=0.0, polygonCoordinates=[dict(xy(H[k]), z=round(zv[k] - z0, 3)) for k in t3]))
            louvres.append(dict(level=0.0, polygonCoordinates=[dict(xy(H[k]), z=round(zv[k] - z0 - CAN_T - CAN_LOUVRE_M, 3))
                                                               for k in t3]))
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
    if "CreateMeshes" not in miss and roofs:
        sk = None
        for st in ("SurfaceOnlyWithoutSkirt", "SurfaceOnly", "SolidBodyWithSkirt"):
            g = ac.create("CreateMeshes", "meshesData", [dict(roofs[0], skirtType=st, skirtLevel=CAN_T)],
                          u"canopy facet test (%s)" % st)
            if g and g[0]:
                made += g
                sk = st
                break
        if sk:
            made += [g for g in ac.create("CreateMeshes", "meshesData", [dict(m, skirtType=sk, skirtLevel=CAN_T)
                                                                         for m in roofs[1:]], u"canopy roof facets") if g]
            made += [g for g in ac.create("CreateMeshes", "meshesData", [dict(m, skirtType=sk, skirtLevel=CAN_LOUVRE_M)
                                                                         for m in louvres], u"canopy louvre layer") if g]
            log.append(u"canopy facets as meshes (%s)" % sk)
        else:
            log.append(u"FLAG canopy roof facets refused by Archicad (meshes): canopies without roofs")
    if "CreateSlabs" not in miss:
        made += [g for g in ac.create("CreateSlabs", "slabsData", plinths, u"canopy stone plinths") if g]
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
        made += [g for g in ac.create("CreateSlabs", "slabsData", plin, u"node buildings: stone plinths") if g]
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
    BSECS = node_secs(NB)
    hsrc = [BUILD_SIG, MESH, [(nm, list(A), list(B)) for nm, A, B, Ln, u, n in rects], NB,
            [(b["ring"], b["fab"], b["fl"], b["h"], b["z"], b["cut"], [r[0] for r in b["views"]]) for b in bld]]
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
        if "CreateSlabs" not in miss:
            made += [g for g in ac.create("CreateSlabs", "slabsData", regs, u"registration blocks") if g]

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
                   sunAltitude=SUN[1], useUncutSurfaceFill=True, modelUncutSurfaceFillType="MaterialColorShaded",
                   markedDistantArea=False, storyHandleAppearance="None")
        try:
            ac.t("SetSectionsAndElevationsDetails", {"elementsWithDetails": [
                {"elementId": {"guid": g}, "details": det} for g in secs.values()]})
            log.append(u"section settings: limited depth %.0f m, vector sun shadows (az %.0f, alt %.0f deg), shaded "
                       u"material fills, nothing beyond the depth" % (BACK_M, SUN[0], SUN[1]))
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
        dw = [os.path.basename(x) for x in glob.glob(os.path.join(DWG_DIR, "**", "*.dwg"), recursive=True)]
        if reuse and not old.get("remade") and old.get("published") and old.get("sec_sig") == SEC_SIG and \
                all(any(x.startswith(nm + " ") or x == nm + ".dwg" for x in dw) for nm in secs):
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
                return any(re.search(u"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(nm), tx) for nm in secs)
            ours = [it for it in leaves if is_ours(it)]
            miss_b = [nm for nm, _A, _B, _d in BSECS if nm in secs and not any(
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
                                       for nm, A, B, dp in BSECS],
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
