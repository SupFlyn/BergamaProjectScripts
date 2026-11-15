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

VERSION = "v1.6"   # v1.6 (Aras 15 Nov 09:52-10:29 "draw our canopies much better like designed ones" / "Some closed areas underneath" / canopies in Archicad "yes please"): his master.svg canopies (kanopi layer) built as his reference: folded triangle-facet roof (meshes) with a timber louvre layer under it, Y steel columns (trunk + 2 arms) under the valleys on a 12 m bay, timber deck on a stone plinth bay by bay, a glazed room in every other bay where the floor is >= Q500 + 0.60 m, timber planters in the open bays; heights as Sections v1.28.2 (DfT 2.30 m clear, EA 0.60 m over Q500, ridge +1.8 m ASSUMED)   # v1.5 + Kızıl Avlu: the main hall outline(s) from the MasterplanBase cache (Sections library red_hall_load), roofless walls 19 m (Wikipedia, Red Basilica: "Its walls still survive up to a height of 19 metres"), no windows, no roof; v1.5 (15 Nov run 7: houses beyond the 200 m depth drawn as floating outlines): no marked distant area (only the 200 m behind each cut is drawn); publishing may take 30 min (the set grew)   # v1.4 v1.4 (15 Nov: Sections v1.18 moved the N4 lines): the Archicad origin is kept from the first run; a section whose line moved is deleted and made again on the new line (its view too), with a FLAG to refresh the publisher set   # v1.3 (run 4: houses 200 m behind stood in the sky, the hill under them was not drawn): per cut the ground behind (highest survey ground 10-200 m behind, every 2 m) written to acbuild.json for SectionsAC   # v1.2 (SectionsAC run 3: the DWGs held only the roofs = the one element type without a BG layer, so the BG layers are not shown in the views): every element on the tool default layers; registration blocks at -50 m (found by geometry); no terrain mesh (our ground is drawn instead)   # v1.1 (14 Nov run 1): mesh without layerIndex (Tapir schema), hipped roofs as one-level polyroofs, footprints cleaned (slab failures)
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
CAN_BAY_M = 12.0                                  # bay between Y columns along the canopy (design intent, ours)
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
    """[(outline ring)] per canopy from the MasterplanBase cache: the pieces of the kanopi layer grouped by touching
    boxes; the outline = the hull of the group's ring and line points simplified (his canopies are long folded strips)"""
    mp = os.path.join(BERGAMA_ROOT, "cached", "bergama_masterplanbase", "masterplan.json")
    if not os.path.isfile(mp):
        log.append(u"FLAG canopies: %s missing (press MasterplanBase): no canopies built" % mp)
        return []
    with open(mp, encoding="utf-8") as f:
        J = json.load(f)
    items = []
    for key, pieces in J.get("layers", {}).items():
        if key.split("/")[-1] not in CAN_KEYS:
            continue
        for p in pieces:
            q = [tuple(v) for v in p[4]]
            if p[0] in ("r", "l", "a") and len(q) >= 2:
                xs, ys = [v[0] for v in q], [v[1] for v in q]
                items.append([q, min(xs), max(xs), min(ys), max(ys)])
    groups = []
    for it in items:
        hit = [g for g in groups if any(it[1] <= o[2] + 3 and o[1] <= it[2] + 3 and it[3] <= o[4] + 3 and o[3] <= it[4] + 3
                                        for o in g)]
        groups = [g for g in groups if g not in hit] + [[it] + [o for g in hit for o in g]]
    out = []
    for g in groups:
        pts = sorted(set((round(v[0], 2), round(v[1], 2)) for o in g for v in o[0]))
        if len(pts) < 3:
            continue
        def cr(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        lo, hi = [], []                                        # convex hull (monotone chain)
        for p in pts:
            while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
                lo.pop()
            lo.append(p)
        for p in reversed(pts):
            while len(hi) >= 2 and cr(hi[-2], hi[-1], p) <= 0:
                hi.pop()
            hi.append(p)
        H = lo[:-1] + hi[:-1]
        if abs(area(H)) >= 20.0:
            out.append(H)
    log.append(u"canopies: %d from the masterplan kanopi layer (%d pieces), outline = hull of each group" % (
        len(out), len(items)))
    return out


def build_canopies(ac, miss, log, rects, inside, tin, ox, oy, z0, xy, q500_at, wet_at):
    """v1.6: each canopy as his reference: a folded roof of triangle facets (ridges on the long axis in the middle of
    each bay, valleys over the Y columns, the outline edges between: folds running out to the edges), a timber
    louvre layer under the skin, Y steel columns (trunk + two arms along the axis) on a regular bay under the valleys,
    a timber deck on a stone plinth, a glazed room in every other bay where the floor is >= Q500 + 0.60, a timber
    planter in the open bays. Heights: valley underside >= ground + 2.30 (DfT) and >= Q500 + 0.60 (EA); ridge +1.8 m
    (ASSUMED). Returns the new element guids."""
    made = []
    roofs, louvres, trunks, arms, plinths, decks, walls, rooms, planters = [], [], [], [], [], [], [], [], []
    n_c = 0
    for H in canopy_groups(log):
        if not any(inside(q, r) for q in H for r in rects):
            continue
        n_c += 1
        cx, cy = sum(p[0] for p in H) / len(H), sum(p[1] for p in H) / len(H)
        sxx = sum((p[0] - cx) ** 2 for p in H); syy = sum((p[1] - cy) ** 2 for p in H)
        sxy = sum((p[0] - cx) * (p[1] - cy) for p in H)
        ang = 0.5 * math.atan2(2 * sxy, sxx - syy)
        u = (math.cos(ang), math.sin(ang))
        v = (-u[1], u[0])
        T = lambda p: (p[0] - cx) * u[0] + (p[1] - cy) * u[1]
        W = lambda p: (p[0] - cx) * v[0] + (p[1] - cy) * v[1]
        ta, tb = min(T(p) for p in H), max(T(p) for p in H)
        nb = max(1, int(round((tb - ta) / CAN_BAY_M)))
        P = lambda t, w=0.0: (cx + u[0] * t + v[0] * w, cy + u[1] * t + v[1] * w)

        def mid_w(t):                                          # the axis: middle of the outline across at t
            ws = []
            for a, b in zip(H, H[1:] + H[:1]):
                ta_, tb_ = T(a), T(b)
                if (ta_ - t) * (tb_ - t) <= 0 and ta_ != tb_:
                    f = (t - ta_) / (tb_ - ta_)
                    ws.append(W(a) + (W(b) - W(a)) * f)
            return ((min(ws) + max(ws)) / 2.0, (max(ws) - min(ws)) / 2.0) if ws else (0.0, 0.0)

        q5 = q500_at(cx, cy)
        # axis points: valleys at the bay ends (the outer ones 12 % in from the tips), ridges at the bay middles
        e0, e1 = ta + 0.12 * (tb - ta), tb - 0.12 * (tb - ta)      # the end columns stand in under the roof
        ax = []
        for k in range(2 * nb + 1):
            t = e0 + (e1 - e0) * k / (2.0 * nb)
            w, hw = mid_w(t)
            p = P(t, w)
            ax.append([t, w, hw, k % 2 == 1, tin.z(p[0] - ox, p[1] - oy)])
        gs = [a_[4] for a_ in ax if a_[4] is not None]
        if not gs:
            log.append(u"canopy %d: no survey ground under it: left out" % n_c)
            continue
        for a_ in ax:
            if a_[4] is None:
                a_[4] = min(gs)
        floor0 = lambda g: g + CAN_PLINTH_M + CAN_DECK_M
        val = [max(floor0(a_[4]) + CAN_CLEAR_M, (q5 + CAN_Q500_M) if q5 is not None else -1e9) + CAN_LOUVRE_M + CAN_T
               for a_ in ax]                                   # valley top of the skin at each axis point
        zax = [val[k] + (CAN_RISE_M if ax[k][3] else 0.0) for k in range(len(ax))]
        CANOPY_REC.append(dict(ring=[[round(p[0], 2), round(p[1], 2)] for p in H], ground=round(min(gs), 3),
                               floor=round(min(floor0(a_[4]) for a_ in ax), 3),
                               under=round(min(val) - CAN_T - CAN_LOUVRE_M, 3), top=round(max(zax), 3)))

        def z_at_t(t):                                         # valley line interpolated along the axis
            if t <= ax[0][0]:
                return val[0]
            for k in range(1, len(ax)):
                if t <= ax[k][0]:
                    f = (t - ax[k - 1][0]) / max(ax[k][0] - ax[k - 1][0], 1e-6)
                    return val[k - 1] + (val[k] - val[k - 1]) * f
            return val[-1]
        # outline sides, sorted along the axis, each side triangulated as a strip against the axis chain
        i_f = max(range(len(H)), key=lambda i: math.hypot(H[i][0] - H[0][0], H[i][1] - H[0][1]))
        Hs = (_dp(H[:i_f + 1], 1.2)[:-1] + _dp(H[i_f:] + [H[0]], 1.2)[:-1]) if len(H) > 4 else H   # closed ring
        tips = [min(Hs, key=T), max(Hs, key=T)]

        def zax_t(t):                                          # the axis fold line (ridges and valleys) at t
            if t <= ax[0][0]:
                return zax[0]
            for k in range(1, len(ax)):
                if t <= ax[k][0]:
                    f = (t - ax[k - 1][0]) / max(ax[k][0] - ax[k - 1][0], 1e-6)
                    return zax[k - 1] + (zax[k] - zax[k - 1]) * f
            return zax[-1]

        def edge_z(t):                                         # the outline: 60 % of the fold, out to knife edges
            return z_at_t(t) + CAN_EAVE_F * (zax_t(t) - z_at_t(t))

        def side_w(t, sg):                                     # the outline across the axis at t, on side sg
            ws = []
            for a, b in zip(Hs, Hs[1:] + Hs[:1]):
                ta_, tb_ = T(a), T(b)
                if (ta_ - t) * (tb_ - t) <= 0 and ta_ != tb_:
                    ws.append(W(a) + (W(b) - W(a)) * (t - ta_) / (tb_ - ta_))
            return (max(ws) if sg > 0 else min(ws)) if ws else None
        side = {1: [], -1: []}
        for p in Hs:
            if p in tips:
                continue
            a_w = mid_w(T(p))[0]
            side[1 if W(p) >= a_w else -1].append(p)
        for sg in (1, -1):                                     # a point of the outline across every axis point
            for a_ in ax:
                w_ = side_w(a_[0], sg)
                if w_ is not None and all(abs(T(q) - a_[0]) > 0.8 for q in side[sg]):
                    side[sg].append(P(a_[0], w_))
        A3 = [(P(a_[0], a_[1]), zax[k]) for k, a_ in enumerate(ax)]
        tri = []
        for sg in (1, -1):
            S_ = [(tips[0], z_at_t(T(tips[0])))] + [(p, edge_z(T(p))) for p in sorted(side[sg], key=T)] + \
                 [(tips[1], z_at_t(T(tips[1])))]
            i = j = 0
            while i < len(S_) - 1 or j < len(A3) - 1:
                adv_s = j >= len(A3) - 1 or (i < len(S_) - 1 and T(S_[i + 1][0]) <= T(A3[j + 1][0]))
                if adv_s:
                    tri.append((S_[i], S_[i + 1], A3[j]))
                    i += 1
                else:
                    tri.append((S_[i], A3[j + 1], A3[j]))
                    j += 1
        for t3 in tri:
            if abs(area([p for p, z in t3])) < 0.3:
                continue
            roofs.append(dict(level=0.0, polygonCoordinates=[dict(xy(p), z=round(z - z0, 3)) for p, z in t3]))
            louvres.append(dict(level=0.0, polygonCoordinates=[dict(xy(p), z=round(z - z0 - CAN_T - CAN_LOUVRE_M, 3))
                                                               for p, z in t3]))
        # Y columns under the valleys (axis points 0, 2, 4 ...), trunk to the fork, two arms along the axis
        for k in range(0, len(ax), 2):
            t, w = ax[k][0], ax[k][1]
            base = P(t, w)
            fl = floor0(ax[k][4])
            under = val[k] - CAN_T - CAN_LOUVRE_M
            hgt = under - fl
            if hgt < 1.0:
                continue
            fork = fl + CAN_Y_FORK * hgt
            trunks.append(dict(coordinates=dict(xy(base), z=round(fl - z0, 3)), height=round(fork - fl, 3),
                               circleBased=True, width=0.30))
            for sg in (1.0, -1.0):
                tt = t + sg * min(CAN_Y_ARM_M, 0.35 * (e1 - e0) / nb)
                tt = max(e0, min(e1, tt))
                if abs(tt - t) < 0.3:
                    continue
                zz = z_at_t(tt) - CAN_T - CAN_LOUVRE_M
                end = P(tt, mid_w(tt)[0])
                run = math.hypot(end[0] - base[0], end[1] - base[1])
                arms.append(dict(begCoordinate=xy(base), endCoordinate=xy(end), zCoordinate=round(fork - z0, 3),
                                 slantAngle=round(math.atan2(zz - fork, run), 4), width=0.22, height=0.22))
        # deck on the plinth, bay by bay (follows the ground in steps); rooms and planters
        for b_ in range(nb):
            t0_, t1_ = ax[2 * b_][0], ax[2 * b_ + 2][0]
            poly = _clip([(T(p), W(p)) for p in Hs], (1.0, 0.0), t0_ - (1e9 if b_ == 0 else 0.0),
                         t1_ + (1e9 if b_ == nb - 1 else 0.0))
            if len(poly) < 3:
                continue
            gpts = [ax[2 * b_][4], ax[2 * b_ + 1][4], ax[2 * b_ + 2][4]]
            g = max(gpts)
            if wet_at(cx, cy, g):
                continue                                       # in the water: no deck (Sections: plinth only where dry)
            ring = [P(t_, w_) for t_, w_ in poly]
            if area(ring) < 0:
                ring = ring[::-1]
            pc = [xy(p) for p in clean(ring)]
            if len(pc) < 3:
                continue
            plinths.append(dict(level=round(g + CAN_PLINTH_M - z0, 3), thickness=CAN_PLINTH_M + 0.5, polygonCoordinates=pc))
            decks.append(dict(level=round(g + CAN_PLINTH_M + CAN_DECK_M - z0, 3), thickness=CAN_DECK_M, polygonCoordinates=pc))
            fl = floor0(g)
            tm, (wm, hw) = ax[2 * b_ + 1][0], mid_w(ax[2 * b_ + 1][0])
            hw = min(hw, mid_w(t0_ + 0.6)[1], mid_w(t1_ - 0.6)[1])
            if b_ % 2 == 0 and q5 is not None and fl >= q5 + CAN_Q500_M and t1_ - t0_ > 4.0 and hw > 2.0:
                r0, r1 = t0_ + 0.8, t1_ - 0.8                 # glazed room: every other bay, above Q500 + 0.60
                hr = 0.6 * hw
                C4 = [P(r0, wm - hr), P(r1, wm - hr), P(r1, wm + hr), P(r0, wm + hr)]
                top = min(val[2 * b_], val[2 * b_ + 2]) - CAN_T - CAN_LOUVRE_M - 0.05
                for a, c in zip(C4, C4[1:] + C4[:1]):
                    walls.append(dict(begCoordinate=xy(a), endCoordinate=xy(c), zCoordinate=round(fl - z0, 3),
                                      height=round(top - fl, 3), thickness=0.08, referenceLineLocation="Center"))
                    rooms.append((math.hypot(c[0] - a[0], c[1] - a[1]), top - fl))
            elif hw > 1.2:                                     # timber planter in the open bay
                L_p = min(CAN_PLANTER_M, 0.4 * (t1_ - t0_))
                C4 = [P(tm - L_p / 2, wm - 0.5), P(tm + L_p / 2, wm - 0.5), P(tm + L_p / 2, wm + 0.5), P(tm - L_p / 2, wm + 0.5)]
                planters.append(dict(level=round(fl + 0.6 - z0, 3), thickness=0.6, polygonCoordinates=[xy(p) for p in C4]))
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
               u"underside >= deck + %.2f m (DfT) and >= Q500 + %.2f m (EA), ridge + %.1f m ASSUMED; bay %.0f m, "
               u"plinth %.2f m, deck %.2f m (design intent)" % (n_c, len(roofs), len(trunks), len(decks),
                                                                 len(walls) // 4, len(planters), CAN_CLEAR_M,
                                                                 CAN_Q500_M, CAN_RISE_M, CAN_BAY_M, CAN_PLINTH_M,
                                                                 CAN_DECK_M))
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
    backs = {}
    for name, A, B, Ln, u, n in rects:                     # v1.3: the ground behind, from the same TIN
        prof, s = [], 0.0
        while s <= Ln + 1e-9:
            zs = [tin.z(A[0] + u[0] * s + n[0] * d - ox, A[1] + u[1] * s + n[1] * d - oy)
                  for d in range(10, int(BACK_M) + 1, 5)]
            zs = [z for z in zs if z is not None]
            prof.append([round(s, 2), round(max(zs), 2) if zs else None])
            s += 2.0
        backs[name] = prof
    log.append(u"ground behind: %d cut profiles (highest survey ground 10-%.0f m behind, every 2 m)" % (
        len(backs), BACK_M))

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
    L = lambda n_: {}      # v1.2: default layers (the BG layers were hidden in the section views)
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
            faces = b["fl"] > 0 and any(on[0] * -r[5][0] + on[1] * -r[5][1] > 0.2 for r in b["views"])
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
        if b["fl"] < 0:
            continue                              # Kızıl Avlu: the roofless Roman hall
        poly = [xy(q) for q in b["ring"]]
        top = round(b["z"] + b["h"] - z0, 3)
        if b["fl"] >= FLAT_FLOORS:
            flats.append(dict(level=top, thickness=0.3, polygonCoordinates=poly, **L("BG buildings")))
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
        det = dict(horizontalRange="Limited", effectVectorShadow=True, effectSunFrom3D=False, sunAzimuth=SUN[0],
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
        if PUB_SET in sets:
            os.makedirs(DWG_DIR, exist_ok=True)
            ac.t("PublishPublisherSet", {"publisherSetName": PUB_SET, "outputPath": DWG_DIR}, 1800.0)
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
                       cuts=[dict(name=nm, A=list(A), B=list(B), L=round(Ln, 3), back=backs.get(nm))
                             for nm, A, B, Ln, u, n in rects],
                       sections=secs, views=views, view_folder=old.get("view_folder"), published=published,
                       dwg_dir=DWG_DIR, layers=list(LAYERS), canopies=CANOPY_REC, elements=made), f,
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
