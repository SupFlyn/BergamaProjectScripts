

Rhino = _B19_RHINO                                   # b19_pre.py: given back after the make_board part was read

# ================================================================ B19 plan v1 (5 Nov 2026, Aras 19:51 + 20:47 + 20:59)
# A NEW standalone script: the masterplan's proposal (option A: zones, corridor, walks, hubs, trees; computed here by
# the masterplan's own code, read from the open file like the masterplan does) drawn in the drawing language of
# B19 "Greenikka" (Arkkitehdit MY, Viinikanlahti competition 2020, 3rd prize), general plan page 5
# -> library/examples/liked_2026-11-05/B19_SCRIPT_SPEC.md (targets 1-11), BRIEF.md (card).
# B19's own geometry (Tampere) is NOT copied: every drawing element of it is, on our proposal's geometry:
# dark slate water with a fine bank line, light ground over the whole project zone, white buildings with grey
# outlines, lawns and greens in light sage washes, trees as transparent sage crowns of mixed tones with a soft
# shadow, light grey paving, mauve movement lines, red facility marks, small black names beside their places,
# everything outside the project zone veiled whitish, the zone in a thin dark red line.
# Writes output/bergama_b19_plan/Bergama_B19_plan_v1.pdf (true size at 1:scale); rhino_bake = True bakes it on
# layer B19. It writes nothing another script reads (no masterplan_results.json, no booklet items).
VERSION = "bergama_b19_plan v6 (2026-11-06)"  # v6 (Aras 00:03-00:25, V6_PLAN F1-F12): every non-heritage building in the zone taken out and its ground designed; only Kozak road + Adnan Menderes kept as car roads (carriageway, pavements, direction arrows), shared streets inside; stream from the bank stations smoothed, off car roads; one continuous walk + loop-free bike lane per bank; footbridges to dry land; drawn programme pads (café, classroom, seats, decks, courts, fitness, play, lawns, allotments, meadow, bird hides), heritage trail; rain terraces, 2 m ground steps; planting by function; hedge + entrances at the edge; v5.1 (Aras 23:41-23:42): heritage never taken out; the freed Ulucami ground designed as the hub square with plane shade; v5 (Aras 23:26): planting from the asset library species (emergent edge, terraces, dry tops), names off roads and water with leaders, walks merged in two passes + loose ends joined, river rounded with a drainage wall, Ulucami buildings in the zone taken out, edge-crossing buildings outside, 10-step greenery gradient, shaded contours; v4 (Aras 22:55): the project's own walks, bike lane, roads by change, bridges with joined ends, terraces, basins, arms, garden, programme marks; OSM tracks and invented promenades/connectors gone; bike strips only beside the walk; every building whole in or out; trees off buildings and each other; v3 (Aras 22:19 "get better"): rebuilt from survey + OSM + stations: streets at survey widths with bike strips, promenades on both banks with varying width, curved connectors, footbridges with landings, ground by distance from water (wood, lawn, meadow), one continuous stream, trees by function off paving and water, names inside the zone; v2 rejected 22:18, v1 rejected 21:26
SHORT = "v6"
GH_LABEL = "B19Plan"
SETTINGS = ("rhino_bake", "scale")
OUT_FOLDER = "bergama_b19_plan"
LOG_NAME = "bergama_b19_plan_log.txt"
BAKE_ROOT = "B19"
B19_SCALE = 4000.0           # default print scale (design spec, 5 Nov 21:0x; input `scale` overrides)
B19_NAME = "Bergama_B19_plan_v6.pdf"
B19_M = 15.0                 # mm paper margin (design value)
B19_HEAD = 20.0              # mm band under the plan: title, scale bar, north arrow (design value)
B19_A1 = (841.0, 594.0)      # ISO 216 A1, mm: the log says whether the sheet fits it
B19_VEIL = 0.6               # opacity of the whitish veil outside the project zone (design value)
B19_BORDER_MM = 0.35         # project zone line, mm (design value)
B19_NAME_MM = 2.12           # place names 6 pt (booklet minimum)
B19_ZONE_MM = 1.76           # zone names 5 pt
# Colours SAMPLED from B19 page 5 (B/liked-B/B19-masterplan/B19_board01_ark-kili_5-2020_Viinikanlahti_lowres_page05.png,
# 3308 x 2339 px), 5 Nov 2026: k-means 16 colours of the project area (water, white, greens, greys) and medians of
# hue-filtered pixels for salmon, dark red, sand and mauve. Values are the page's, not our palette (spec item 4).
B19_COL = dict(water="51626C", water_edge="4B5A64", deep="3D4340", lawn="B9C4B1", green="A7AF9E", tree="94988A",
               tree_dark="798274", shadow="616758", paving="D8D9D5", ground="E4E4E0", white="FBFBFA",
               line="C9CCC4", red="EA8477", border="692F28", sand="ECCCA8", mauve="9C6D70", ink="1E1E1E")
B19_HUE = {                  # masterplan legend key -> B19 colour (keys missing here keep the masterplan's hue)
    "bld": "white", "bld_edge": "tree", "her": "red", "her_edge": "border", "since": "ground", "street": "line",
    "bridge": "tree", "road_kept": "line", "eco": "lawn", "ring": "paving", "flood_plant": "green",
    "widen": "water", "widen_edge": "deep", "reed": "green", "reed_edge": "tree_dark", "arm": "water",
    "terrace": "tree_dark", "drytop": "lawn", "drytop_edge": "tree_dark", "spill": "water", "spill_edge": "deep",
    "store": "water_edge", "cch": "deep", "hidden": "water",
    "dg": "lawn", "dg_edge": "tree_dark", "dg_gather": "paving", "dg_row": "tree_dark",
    "walk": "mauve", "walk_bed": "mauve", "bike": "mauve", "foot": "mauve", "stones": "tree", "canopy": "tree_dark",
    "road_pedestrian": "mauve", "road_calmed": "mauve", "road_shared": "mauve", "road_relocated": "line",
    "road_later": "line", "street_cut": "mauve", "square": "paving", "square_edge": "tree", "market": "red",
    "walkhub": "red", "transit": "red", "gate": "red", "sub": "red", "seat": "red", "cafe": "red", "edu": "red",
    "view": "red", "deck": "red", "sight": "tree", "left": "ground"}
B19_NOT_IN_PROPOSAL = (u"harbour piers and marina boats", u"tram line", u"red public building footprints "
                       u"(our proposal adds no buildings)", u"beach sand")   # B19 elements with no match: not drawn

_b19_h0 = pl23_h


def pl23_h(key):
    """B19: the masterplan legend key's colour from B19_COL (else the masterplan's own hue)"""
    c_ = B19_HUE.get(key)
    return B19_COL[c_] if c_ else _b19_h0(key)


def ml_study_items(rings=None, D=None):
    """B19: the shared violet study line is not drawn; b19_page draws the zone in B19's thin dark red line"""
    return []


def icon(pg, kind, x, y, s):
    """B19: every facility gets the SAME mark (spec item 7, 11): a small red block with a dark red edge"""
    h = s * 0.32
    pg.poly([rect(x - h, y - h, x + h, y + h)], fill=B19_COL["red"], stroke=B19_COL["border"], lw=0.1)


def pl23_water_draw(pg, C, T, k, on, spacing):
    """B19: the stream as one dark slate surface with a fine dark bank line; islands left open"""
    rings = []
    for R, Hs in pl23_water_groups(C):
        Q = [T(p) for p in R]
        if not on(Q):
            continue
        QH = [[T(p) for p in H] for H in Hs if len(H) >= 3]
        pg.poly([Q] + QH, fill=B19_COL["water"], stroke=B19_COL["deep"], lw=0.15)
        rings.append(Q)
        rings += QH
    return rings


_B19_PLA_ASSET = pla_plan    # v5: the plant module's own plan symbol (asset library images / species masses)


def pla_plan(key, cx, cy, k, crown_m=None, beyond=False, seed=0, distinct=True, style="b", month=None, season=None):
    """B19: a tree from above = a transparent sage crown (one of three tones by seed) over a soft shadow to the
    south-east; crown width = the species' sourced crown (plants.py PLA_SPECIES) unless crown_m is given"""
    cm = crown_m or (PLA_SPECIES.get(key) or {}).get("crown_m", 6.0)
    r = max(0.35, cm * k / 2.0)
    tone = (B19_COL["green"], B19_COL["tree"], B19_COL["tree_dark"])[seed % 3]
    ring_ = lambda ox, oy: [(cx + ox + r * math.cos(a * math.pi / 8.0), cy + oy + r * math.sin(a * math.pi / 8.0))
                            for a in range(16)]
    return [("poly", ring_(0.18 * r, -0.18 * r), B19_COL["shadow"], None, 0.0, 0.3),
            ("poly", ring_(0.0, 0.0), tone, B19_COL["tree_dark"], 0.08, 0.85)]


# ================================================================ v2 step 1 (Aras 5 Nov 22:09): the continuous network
# Order (Aras): 1 paths + roads with widths and textures (this version), 2 greenery + nature paths by ecological
# function, 3 water, 4 connections between areas; the 3 main facilities are drawn by Aras later (no footprints here).
# Widths and textures are design values (named below); geometry = the masterplan's walks, roads, bridges, hubs and
# the survey; nothing is drawn as a bare line: every route is a band with its width.
B2_PROM_W = (3.0, 8.0)       # m: promenade width, normal and at a hub / bridge end (design values)
B2_PROM_GROW_M = 45.0        # m: the promenade widens over this distance toward a hub / bridge end
B2_BIKE_W = 2.2              # m: bike lane band on the land side of the bank promenade
B2_BED_W = 1.8               # m: path down in the stream bed (gravel)
B2_CONN_W = 3.0              # m: connector from a city street to the promenade
B2_CONN_MAX = 150.0          # m: a street farther than this from the promenade gets no connector (logged)
B2_FOOT_W = 3.0              # m: footbridge deck
B2_BRIDGE_W = 7.0            # m: road bridge deck when the survey gives only its axis
B2_SHARED_W = 6.0            # m: changed street (pedestrian / calmed / shared) band
B2_JOINT_M = 3.0             # m: paving joint spacing (hard texture)
B2_FADE = ((12.0, 0.25), (28.0, 0.25), (50.0, 0.25))   # m beyond the zone line, veil opacity added (edge fades out)
B2_CONTEXT_VEIL = 0.62       # veil opacity past the last fade ring
B2_COL = dict(asphalt="BFC1BB", kerb="94988A", paving="D8D9D5", joint="BDBEB8", bike="9C6D70", gravel="E2D8C4",
              deck="FBFBFA", deck_edge="798274", lawn="B9C4B1", bld_in="FFFFFF", bld_in_edge="3D4340",
              bld_out="FBFBFA", bld_out_edge="C9CCC4", shadow="9A9C96")


def b2_band(P, widths):
    """polyline P (page mm) with one width per vertex (page mm) -> band ring (left side, then right side back)"""
    if len(P) < 2:
        return []
    L, R = [], []
    n = len(P)
    for i in range(n):
        a, b = P[max(0, i - 1)], P[min(n - 1, i + 1)]
        ux, uy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(ux, uy) or 1.0
        h = widths[i] / 2.0
        L.append((P[i][0] - uy / d * h, P[i][1] + ux / d * h))
        R.append((P[i][0] + uy / d * h, P[i][1] - ux / d * h))
    return L + R[::-1]


def b2_joints(pg, P, widths, step, col):
    """short cross lines every `step` mm along a band (paving joints = the hard-surface texture)"""
    s = arclen(P)
    t = step
    while t < s[-1]:
        (x, y), (ux, uy) = at_len(P, s, t)
        i = min(range(len(s)), key=lambda j: abs(s[j] - t))
        h = widths[i] / 2.0 * 0.92
        pg.line([(x - uy * h, y + ux * h), (x + uy * h, y - ux * h)], col, 0.05)
        t += step


def b2_seg_x(a, b, c, d):
    """intersection point of segments ab and cd, else None"""
    r = (b[0] - a[0], b[1] - a[1])
    s = (d[0] - c[0], d[1] - c[1])
    den = r[0] * s[1] - r[1] * s[0]
    if abs(den) < 1e-12:
        return None
    t = ((c[0] - a[0]) * s[1] - (c[1] - a[1]) * s[0]) / den
    u = ((c[0] - a[0]) * r[1] - (c[1] - a[1]) * r[0]) / den
    return (a[0] + t * r[0], a[1] + t * r[1]) if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0 else None


def b2_rh_pts(c, step=1.0):
    n = max(8, int(c.GetLength() / step))
    return [(c.PointAt(t).X, c.PointAt(t).Y) for t in c.DivideByCount(n, True)]


def b2_rh_curve(R):
    return rg.PolylineCurve([rg.Point3d(p[0], p[1], 0.0) for p in list(R) + [R[0]]])


def b2_union(rings, warn):
    """survey building rings merged where they overlap (one outline per block, no overlapping silhouettes); Rhino's
    boolean union; outside Rhino or on failure the rings are returned as they are (logged)"""
    if rg is None or not rings:
        return rings
    bx = [bbox(R) for R in rings]                         # only rings whose boxes touch are merged (fast)
    par = list(range(len(rings)))

    def root(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i
    order = sorted(range(len(rings)), key=lambda i: bx[i][0])
    for a_i, i in enumerate(order):
        for j in order[a_i + 1:]:
            if bx[j][0] > bx[i][2]:
                break
            if hit(bx[i], bx[j]):
                par[root(i)] = root(j)
    groups = {}
    for i in range(len(rings)):
        groups.setdefault(root(i), []).append(rings[i])
    out, failed = [], 0
    for g in groups.values():
        if len(g) == 1:
            out.append(g[0])
            continue
        try:
            res = rg.Curve.CreateBooleanUnion([b2_rh_curve(R) for R in g], 0.01)
            out += [b2_rh_pts(c, 0.5) for c in res] if res else g
            failed += 0 if res else 1
        except Exception:
            out += g
            failed += 1
    if failed:
        warn.append(u"B19 plan: {} building group(s) not merged: overlaps may show there".format(failed))
    return out


def b2_offset_out(R, d):
    """study ring R grown d m outward (Rhino offset, the larger of the two sides); None outside Rhino"""
    if rg is None:
        return None
    try:
        c = b2_rh_curve(R)
        best = None
        for s_ in (d, -d):
            o = c.Offset(rg.Plane.WorldXY, s_, 0.01, rg.CurveOffsetCornerStyle.Round)
            if o:
                P = b2_rh_pts(o[0], 1.0)
                if best is None or abs(area2(P)) > abs(area2(best)):
                    best = P
        return best
    except Exception:
        return None


# ================================================================ v3 (5 Nov 2026 22:30, Aras 22:18-22:20 "get better")
# The plan regenerated from the survey (Bergama_Altlik.3dm), OpenStreetMap street classes and the masterplan's own
# stations along the stream (C.rows: bank edge and free room each side every ~2 m), previewed offline before
# delivery (Aras 22:20, B19 script only). Every route is a band with a measured or designed width; streets keep
# their survey width (OSM centreline snapped between the survey road edges); the promenade is ONE continuous band
# per bank whose width and distance from the water follow the free room, smoothed so it never jumps; bridges land
# on paved landings that join promenade, connectors and streets; soft ground is split by purpose (bank meadow and
# reed fringe, lawn, zone surfaces of the masterplan); trees by function. Design values are named B3_*.
B3_ROAD_W = dict(trunk=14.0, trunk_link=9.0, primary=12.0, primary_link=8.0, secondary=10.0, secondary_link=7.0,
                 tertiary=8.0, unclassified=6.0, residential=6.0, living_street=5.0, service=4.0, track=3.5,
                 pedestrian=6.0, footway=2.5, path=2.0, steps=2.5, cycleway=2.5)   # m when the survey gives no width
B3_VEHICLE = ("trunk", "trunk_link", "primary", "primary_link", "secondary", "secondary_link", "tertiary",
              "unclassified", "residential", "service")
B3_SHARED = ("living_street",)
B3_PED = ("pedestrian", "footway", "path", "steps")
B3_BIKE_ON = ("trunk", "primary", "secondary")   # B19 e5: bike strips along the main roads
B3_BIKE_W = 1.8              # m bike strip (design value)
B3_SNAP_MAX = 14.0           # m: survey road edge searched this far either side of an OSM centreline
B3_PROM = dict(w_min=3.0, w_max=9.0, gap_min=1.5, gap_max=8.0, deck_free=4.5, smooth_m=40.0)   # promenade (design)
B3_CONN_MAX = 110.0          # m: a street this close to the promenade gets a connector (design value)
B3_CONN_SPACING = 70.0       # m: connectors at least this far apart along a promenade (design value)
B3_LANDING_R = 7.0           # m: paved landing at each footbridge end (design value)
B3_FOOT_W = 4.0              # m footbridge deck (design value)
B3_NECK = 9.0  # design value: half-width cap of the stream where stations are missing (m)
B3_TREE_CLEAR = 1.0          # m: a tree crown centre stays this far from paving, roads, water, buildings
B3_COL = dict(paper="FFFFFF", lawn="BCC8B0", lawn_dk="A9B79C", wood="AEBC9F", meadow="CFD7BF", reed="9FAE95", gravel="E6DCC8",
              water="51626C", water_lt="6A7B85", ripple="5E7079", asphalt="C3C5BF", kerb="8E918A",
              paving="DCDCD6", paving_edge="A9AAA3", joint="C4C5BF", bike="A0767A", deck="FAFAF7", deck_edge="5E625A",
              bld="FFFFFF", bld_edge="34383A", bld_ctx="F7F7F5", bld_ctx_edge="C8CAC4", shadow="8E928B",
              heritage="E4877A", removed_edge="8E918A", border="692F28", ink="1E1E1E", contour="9AA58E",
              tree1="8E9C82", tree2="7A8A70", tree3="A3B096", tree_edge="5F6C57", tree_sh="5A6352", tree_hi="C5CEB8",
              garden="D9CFA8", garden_row="A69A70", contour_dk="7D8A72", wall="2F3A40", prog="D9A08F",
              culture="E4877A", food="D9A55C", edu="8FA6B8", hub="9C6D70")
# v4 (Aras 22:55): the project's own elements, widths are design values (m)
B3_DROP_IN = ("track", "path", "footway", "service", "cycleway", "bridleway", "steps", "unclassified")  # not drawn in the zone
B3_WALK_W = 4.0              # riverside walk paving
B3_BED_W = 2.5               # bed walk (gravel, shut in floods)
B3_CANOPY_W = 3.5            # canopied walkway (deck)
B3_TERR_W = 3.0              # rain terrace band on its contour
B3_ARM_W = 4.0               # planted side arm, open water
B3_EMERGENT = ("soft_rush", "loosestrife", "rush")   # v5: water-edge belt (plant module species; reed + mint only in lined cells, plant module rule)
B3_ULU_XY = (29846.40, 32277.71)   # v5 (Aras 23:26): Ulucami Önü bridge (K4); every building in the zone within
B3_ULU_R = 220.0                   # this many m of it is taken out (heritage kept), design value
B3_JOIN_MAX = 30.0           # v5: a walk end looks this far for another walk / street to join (no loose ends)
B3_END_MAX = 45.0            # a bridge end looks this far for a walk to join


# ---------------------------------------------------------------- small geometry
def b3_grid(segs, cell=20.0):
    """segment index: {(i, j): [(a, b)]}"""
    G = {}
    for a, b in segs:
        x0, x1 = sorted((a[0], b[0]))
        y0, y1 = sorted((a[1], b[1]))
        for i in range(int(math.floor(x0 / cell)), int(math.floor(x1 / cell)) + 1):
            for j in range(int(math.floor(y0 / cell)), int(math.floor(y1 / cell)) + 1):
                G.setdefault((i, j), []).append((a, b))
    return G, cell


def b3_near(GI, p, r):
    G, cell = GI
    out = []
    for i in range(int(math.floor((p[0] - r) / cell)), int(math.floor((p[0] + r) / cell)) + 1):
        for j in range(int(math.floor((p[1] - r) / cell)), int(math.floor((p[1] + r) / cell)) + 1):
            out += G.get((i, j), ())
    return out


def b3_dist(GI, p, r):
    """distance from p to the nearest indexed segment within r (else r)"""
    d = r
    for a, b in b3_near(GI, p, r):
        d = min(d, seg_dist(p[0], p[1], a, b))
    return d


def b3_segs(Ps, closed=False):
    out = []
    for P in Ps:
        Q = list(P) + ([P[0]] if closed and len(P) > 2 else [])
        out += [(Q[i], Q[i + 1]) for i in range(len(Q) - 1)]
    return out


def b3_normals(P):
    out = []
    n = len(P)
    for i in range(n):
        a, b = P[max(0, i - 1)], P[min(n - 1, i + 1)]
        ux, uy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(ux, uy) or 1.0
        out.append((-uy / d, ux / d))
    return out


def b3_smooth(vals, k):
    """moving average over k samples (k odd)"""
    h = max(0, k // 2)
    out = []
    for i in range(len(vals)):
        w = vals[max(0, i - h):i + h + 1]
        out.append(sum(w) / len(w))
    return out


def b3_band(P, widths):
    """centreline P (survey m) and its widths (m) -> band ring (survey m)"""
    if len(P) < 2:
        return []
    N = b3_normals(P)
    L = [(p[0] + n[0] * w / 2.0, p[1] + n[1] * w / 2.0) for p, n, w in zip(P, N, widths)]
    R = [(p[0] - n[0] * w / 2.0, p[1] - n[1] * w / 2.0) for p, n, w in zip(P, N, widths)]
    return L + R[::-1]


def b3_circle(c, r, n=24):
    return [(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def b3_chaikin_open(P, it=2):
    for _ in range(it):
        if len(P) < 3:
            return P
        Q = [P[0]]
        for a, b in zip(P[:-1], P[1:]):
            Q += [(0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]),
                  (0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1])]
        Q.append(P[-1])
        P = Q
    return P


# ---------------------------------------------------------------- the street network (OSM classes, survey widths)
def b3_osm(box, warn):
    """[(class, is_bridge, name, [pts survey m])] of OSM highways touching box (Data/bergama_osm.osm; h01 §0
    conversion x = 30037.01 + (lon - 27.18127) x 86,361; y = 32121.57 + (lat - 39.123302) x 111,320)"""
    import xml.etree.ElementTree as _ET
    path = os.path.join(DATA_DIR, "bergama_osm.osm")
    if not os.path.isfile(path):
        warn.append(u"B19 plan: Data/bergama_osm.osm missing: street classes unknown, survey edges only")
        return []
    root = _ET.parse(path).getroot()
    N = {}
    for nd in root.iter("node"):
        N[nd.get("id")] = (30037.01 + (float(nd.get("lon")) - 27.18127) * 86361.0,
                           32121.57 + (float(nd.get("lat")) - 39.123302) * 111320.0)
    out = []
    for w in root.iter("way"):
        t = {x.get("k"): x.get("v") for x in w.findall("tag")}
        h = t.get("highway")
        if not h or h not in B3_ROAD_W:
            continue
        P = [N[x.get("ref")] for x in w.findall("nd") if x.get("ref") in N]
        if len(P) >= 2 and hit(bbox(P), box):
            out.append((h, t.get("bridge") not in (None, "no"), t.get("name", u""), P))
    return out


def b3_snap(ways, edge_idx):
    """each OSM way moved onto the middle of the survey road edges, with the survey's width (median of its
    stations); a way with no edge pair keeps its line and its class width. [(class, bridge, name, P, w, snapped)]"""
    out = []
    for h, br, nm, P in ways:
        D = densify(P, 4.0)
        N = b3_normals(D)
        shifts, widths = [], []
        for p, n in zip(D, N):
            tp, tn = None, None
            for a, b in b3_near(edge_idx, p, B3_SNAP_MAX):
                x = b2_seg_x(p, (p[0] + n[0] * B3_SNAP_MAX, p[1] + n[1] * B3_SNAP_MAX), a, b)
                if x:
                    d = math.hypot(x[0] - p[0], x[1] - p[1])
                    tp = d if tp is None or d < tp else tp
                x = b2_seg_x(p, (p[0] - n[0] * B3_SNAP_MAX, p[1] - n[1] * B3_SNAP_MAX), a, b)
                if x:
                    d = math.hypot(x[0] - p[0], x[1] - p[1])
                    tn = d if tn is None or d < tn else tn
            if tp is not None and tn is not None and 2.5 <= tp + tn <= 28.0:
                shifts.append((tp - tn) / 2.0)
                widths.append(tp + tn)
            else:
                shifts.append(None)
        ok = [s for s in shifts if s is not None]
        if len(ok) >= max(2, len(D) // 3):
            fill = sorted(ok)[len(ok) // 2]
            sh = b3_smooth([s if s is not None else fill for s in shifts], 7)
            Q = [(p[0] + n[0] * s, p[1] + n[1] * s) for p, n, s in zip(D, N, sh)]
            w = sorted(widths)[len(widths) // 2]
            out.append((h, br, nm, Q, w, True))
        else:
            out.append((h, br, nm, D, B3_ROAD_W[h], False))
    return out


# ---------------------------------------------------------------- the promenade (one band per bank, from C.rows)
def b3_promenades(C):
    """per bank: [(centre pts, widths, deck flags, inner edge pts (water side))] runs, continuous over the open
    stream; the band sits on land past a bank strip; little free room = a deck on the bank edge"""
    rows = sorted([r for r in C.rows if not r["cov"]], key=lambda r: r["ch"])
    out = {}
    for side, sg in (("NE", 1.0), ("SW", -1.0)):
        runs, cur = [], []
        last = None
        for r in rows:
            s_ = r.get(side) or {}
            if "e" not in s_:
                continue
            if last is not None and r["ch"] - last > 12.0 and cur:
                runs.append(cur)
                cur = []
            cur.append(r)
            last = r["ch"]
        if cur:
            runs.append(cur)
        res = []
        for run in runs:
            if len(run) < 6:
                continue
            free = [max(0.0, min(60.0, r[side].get("free", 0.0))) for r in run]
            gap = [min(B3_PROM["gap_max"], max(B3_PROM["gap_min"], f * 0.22)) for f in free]
            w = [min(B3_PROM["w_max"], max(B3_PROM["w_min"], (f - g) * 0.45)) for f, g in zip(free, gap)]
            deck = [f < B3_PROM["deck_free"] for f in free]
            k_ = max(3, int(B3_PROM["smooth_m"] / 2.0) | 1)
            gap, w = b3_smooth(gap, k_), b3_smooth(w, k_)
            gap = [0.0 if d else g for g, d in zip(gap, deck)]
            w = [min(wi, 3.0) if d else wi for wi, d in zip(w, deck)]
            ctr, edge = [], []
            for r, g, wi in zip(run, gap, w):
                e = r[side]["e"]
                o = e + sg * (g + wi / 2.0)
                ctr.append((r["p"][0] + r["n"][0] * o, r["p"][1] + r["n"][1] * o))
                edge.append((r["p"][0] + r["n"][0] * e, r["p"][1] + r["n"][1] * e))
            res.append((ctr, w, deck, edge, gap))
        out[side] = res
    return out


def b19_page(C, site, study, scale, warn):
    """v6 sheet (Aras 6 Nov 00:18-00:25, previews/V6_PLAN.md F1-F12): the project's own elements, each drawn as
    what it is, in B19 language. Returns (Page, log notes)."""
    t0 = time.time()
    k = 1000.0 / scale
    x0, y0, x1, y1 = bbox(site)
    dw, dh = (x1 - x0) * k, (y1 - y0) * k
    T = lambda p: ((p[0] - x0) * k, (p[1] - y0) * k)
    TL = lambda P: [T(p) for p in P]
    ins = lambda p: any(pip(p[0], p[1], R) for R in study)
    sub = Page(dw, dh)
    st = [TL(R) for R in study if len(R) >= 3]
    notes, flags, n_el, n_sp = [], [], {}, {}
    sv = C.survey if hasattr(C, "survey") else {}
    box = (x0 - 60.0, y0 - 60.0, x1 + 60.0, y1 + 60.0)
    road_names, el_names, stones = [], [], []
    cnt = lambda key, n=1: n_el.__setitem__(key, n_el.get(key, 0) + n)
    cl = pl23_prep(C)
    # ================================================================ data
    # F1 buildings: every non-heritage building touching the zone is taken out; heritage never touched
    raw = [R for role in ("building", "housing", "heritage") for R in C.bld.get(role, []) if len(R) >= 3]
    sheds = [b3_hull(R) for R in C.bld.get("shed", []) if len(R) >= 3]
    blds = b2_union(raw, warn)
    her = [R for R in C.bld.get("heritage", []) if len(R) >= 3]
    is_her = lambda R: any(pip(inner_pt(H)[0], inner_pt(H)[1], R) for H in her)
    touch = lambda R: ins(inner_pt(R)) or any(ins(q) for q in R)
    b_her = [R for R in blds if touch(R) and is_her(R)]
    b_rm = [R for R in blds + sheds if touch(R) and not is_her(R)]
    b_out = [R for R in blds + sheds if not touch(R)]
    keep_b = b_her + b_out
    kb_box = [(bbox(R), R) for R in keep_b]
    in_bld = lambda p, m=0.0: any(bb[0] - m <= p[0] <= bb[2] + m and bb[1] - m <= p[1] <= bb[3] + m and
                                  (pip(p[0], p[1], R) or (m > 0 and b3_dist_ring(R, p) < m)) for bb, R in kb_box)
    b_idx = b3_grid(b3_segs(keep_b, True))
    # streets (OSM, survey widths)
    edges = [P for role in ("road", "kerb") for P in sv.get(role, []) if hit(bbox(P), box)]
    ways = b3_snap(b3_osm(box, warn), b3_grid(b3_segs(edges), 15.0))
    PROJ_RD = [(rd, ch) for rd, ch, runs in cl["roads"]]

    def rd_of(P):
        best = None
        for rd, ch in PROJ_RD:
            xy = rd["xy"]
            n_ = sum(1 for q in P if min(seg_dist(q[0], q[1], a_, b_) for a_, b_ in zip(xy[:-1], xy[1:])) < 14.0)
            if n_ >= max(2, len(P) * 0.6) and (best is None or n_ > best[0]):
                best = (n_, rd, ch)
        return best
    vis = []
    for h, br, nm, P, w, sn in ways:
        if not hit(bbox(P), box):
            continue
        inz = sum(1 for q in P if ins(q)) >= len(P) / 2.0
        if inz and h in B3_DROP_IN:
            continue                                      # tracks, footways ... inside the zone: the walks replace them
        m = rd_of(P) if inz else None
        car = bool(m and m[1]["name"] in B6_CAR_ROADS) or (br and h in B3_VEHICLE)
        vis.append(dict(h=h, br=br, nm=nm, P=P, w=w, inz=inz, car=car, rd=m[1]["name"] if m else None))
    car_ways = [x for x in vis if x["car"]]
    # ================================================================ water (F3)
    chan_raw = b6_channel(C, car_ways)
    chan = [b3_chaikin_closed(R[::3], 2) for R in chan_raw if len(R) >= 9]   # ~6 m vertices, rounded
    chan_box = [(bbox(R), R) for R in chan]
    in_chan = lambda p: any(bb[0] <= p[0] <= bb[2] and bb[1] <= p[1] <= bb[3] and pip(p[0], p[1], R)
                            for bb, R in chan_box)
    widen = [w_["ring"] for w_ in C.widen if len(w_.get("ring") or []) >= 3]
    in_wet = lambda p: in_chan(p) or any(pip(p[0], p[1], R) for R in widen)
    hard = []                                             # (bbox, polyline, half width + clearance)
    h_idx = {}

    def add_hard(P, r):
        hard.append((bbox(P), P, r))
        bb_ = bbox(P)
        for gi in range(int(bb_[0] // 40) - 1, int(bb_[2] // 40) + 2):
            for gj in range(int(bb_[1] // 40) - 1, int(bb_[3] // 40) + 2):
                h_idx.setdefault((gi, gj), []).append(len(hard) - 1)

    def on_hard(p, r0=0.0):
        for i_ in h_idx.get((int(p[0] // 40), int(p[1] // 40)), ()):
            bb_, P, r_ = hard[i_]
            if len(P) > 3 and P[0] == P[-1] and bb_[0] <= p[0] <= bb_[2] and bb_[1] <= p[1] <= bb_[3] and \
                    pip(p[0], p[1], P):
                return True                               # inside a square or pad
            for a, b in zip(P[:-1], P[1:]):
                if seg_dist(p[0], p[1], a, b) < r_ + r0:
                    return True
        return False
    free = lambda p, r=0.0: ins(p) and not in_wet(p) and not on_hard(p, r) and not in_bld(p, r)
    # ================================================================ 1 ground: gradient, height steps, contours
    sub.clip(st)
    with mpx_grp(sub, "ground", u"open meadow"):
        sub.poly([rect(0.0, 0.0, dw, dh)], fill=B3_COL["meadow"])
        b3_dots(sub, (0.0, 0.0, dw, dh), 7.0 * k, B3_COL["lawn_dk"], st)
    eco = dict(C.eco)
    ts = sorted(eco.keys(), reverse=True)
    for i_, t_ in enumerate(ts):
        Ps = [TL(R) for R in eco[t_] if len(R) >= 3]
        if Ps:
            with mpx_grp(sub, "ground", u"planting gradient, %g m from the water" % t_):
                sub.poly(Ps, fill=b3_mix(B3_COL["meadow"], B3_COL["wood"], (i_ + 1.0) / len(ts)))
    n_lv = b6_height_steps(sub, C, T, k, ins, study)     # F8: the terraced valley, 2 m steps above the stream
    cnt("height cells", n_lv)
    with mpx_grp(sub, "ground", u"contours, shaded on the low side"):
        for P in (C.contours or []):
            if hit(bbox(P), box):
                sub.line(TL(P), B3_COL["contour"], 0.06)
                sub.line(b3_off(TL(P), 0.12), B3_COL["contour_dk"], 0.05, alpha=0.5)
    sub.unclip()
    with mpx_grp(sub, "buildings", u"buildings taken out (dashed)"):   # under everything designed after
        for R in b_rm:
            Q = TL(R)
            sub.line(Q + Q[:1], B3_COL["removed_edge"], 0.08, [0.6, 0.5], cap=0, alpha=0.6)
    # ================================================================ 2 the project's zones as surfaces
    sub.clip(st)
    for z in C.D.zones:
        if len(z["P"]) < 3:
            continue
        Q = TL(z["P"])
        c_ = z["code"]
        if c_ == "WT":
            with mpx_grp(sub, "water", u"reed basins %s" % z.get("id", u"")):
                sub.poly([Q], fill=B3_COL["reed"], stroke=B3_COL["wall"], lw=0.12)
                b3_ticks_fill(sub, Q, B3_COL["tree_edge"], 1.2)
            cnt("reed basins")
        elif c_ == "WP":
            with mpx_grp(sub, "plants", u"floodable planting"):
                sub.poly([Q], fill=B3_COL["wood"])
                b3_ticks_fill(sub, Q, B3_COL["lawn_dk"], 2.0)
        elif c_ == "WA":
            with mpx_grp(sub, "water", u"stream bed (gravel)"):
                sub.poly([Q], fill=B3_COL["bed"])
                b3_dots(sub, bbox(Q), 1.2, B3_COL["contour"], [Q])
        elif c_ in ("WS", "GR"):
            with mpx_grp(sub, "fields", u"%s terraces" % (u"dry-top" if c_ == "WS" else u"raised dry top")):
                b6_steps(sub, z["P"], T, k)
            cnt("stepped terraces")
        elif c_ == "WD":
            with mpx_grp(sub, "water", u"spillway"):
                sub.poly([Q], fill=B3_COL["water_lt"], stroke=B3_COL["wall"], lw=0.15)
                b3_ticks_line(sub, Q + Q[:1], B3_COL["deck"], 0.08, 1.0, 0.6)
    for P in C.terr:                                      # F7: rain terraces as level bands with a wall line
        if len(P) >= 2 and any(ins(q) for q in P):
            with mpx_grp(sub, "fields", u"rain terrace"):
                b6_terrace(sub, C, P, T, k)
            add_hard(P, B6_TERR_W / 2.0 - 1.0)            # (olives planted on it in 10 are exempt)
            cnt("rain terrace")
    if b6_dg(sub, C, T, add_hard):                        # F12
        cnt("Demeter's Garden")
        dq = [z["q"] for z in C.D.zones if z["code"] == "DG" and z.get("q")]
        if dq:
            el_names.append((u"Demeter's Garden, allotments", dq[0]))
    sub.unclip()
    # ================================================================ 3 water (F3)
    sub.clip(st)
    with mpx_grp(sub, "water", u"Selinos"):
        for R in chan:
            sub.poly([TL(R)], fill=B3_COL["water"])
    for R in widen:
        with mpx_grp(sub, "water", u"widened stream, wetland"):
            sub.poly([TL(R)], fill=B3_COL["water_lt"])
            b3_ticks_fill(sub, TL(R), B3_COL["reed"], 1.2)
        cnt("widened wetland")
    for a_ in C.arms:
        P = a_.get("P") or []
        if len(P) >= 2:
            with mpx_grp(sub, "water", u"planted side arm"):
                sub.poly([TL(b3_band(P, [B3_ARM_W + 3.0] * len(P)))], fill=B3_COL["reed"])
                sub.poly([TL(b3_band(P, [B3_ARM_W] * len(P)))], fill=B3_COL["water"])
            add_hard(P, B3_ARM_W / 2.0 + 1.5)
            cnt("side arm")
    sub.unclip()
    with mpx_grp(sub, "water", u"hidden stream line + grilles"):
        for P in cl["cov"]:
            if len(P) >= 2:
                sub.line(TL(P), B3_COL["water"], 0.35, [1.6, 0.9], cap=0)
                for q in b3_dense(P, 40.0)[1:-1]:
                    x_, y_ = T(q)
                    sub.poly([rect(x_ - 0.5, y_ - 0.5, x_ + 0.5, y_ + 0.5)], fill=B3_COL["deck"],
                             stroke=B3_COL["wall"], lw=0.06)
                cnt("hidden stream")
    # ================================================================ 4 streets (F2)
    n_rd = {}
    for x in vis:
        P, w, h = x["P"], x["w"], x["h"]
        if not x["br"] and any(in_chan(q) for q in P):  # nothing over the water but bridges
            pieces, cur = [], []
            for q in b3_dense(P, 4.0):
                if in_chan(q):
                    if len(cur) >= 2:
                        pieces.append(cur)
                    cur = []
                else:
                    cur.append(q)
            if len(cur) >= 2:
                pieces.append(cur)
        else:
            pieces = [P]
        for P in pieces:
            if x["car"] and x["inz"]:
                kind = "car"
            elif x["inz"]:
                kind = "shared"
            else:
                kind = "ctx"
            if kind == "ctx":                             # outside: narrowed wherever a building is near
                Pd = b3_dense(P, 4.0)
                W_ = [max(2.0, min(w, 2.0 * (b3_dist(b_idx, q, w) - 0.6))) for q in Pd]
                with mpx_grp(sub, "roads", u"street %s" % (x["nm"] or h)):
                    sub.poly([TL(b3_band(Pd, W_))], fill=B3_COL["ctx_road"])
                continue
            if x["br"]:
                with mpx_grp(sub, "roads", u"road bridge %s" % (x["nm"] or u"")):
                    sub.poly([TL(b3_band(P, [w + 1.2] * len(P)))], fill=B3_COL["deck_edge"])
                    sub.poly([TL(b3_band(P, [w] * len(P)))], fill=B3_COL["deck"])
                add_hard(P, w / 2.0 + B3_TREE_CLEAR)
                cnt("road bridge")
                continue
            if kind == "car":                              # carriageway + pavements both sides + direction arrows
                ww = w + 2.0 * B6_PAVEMENT
                with mpx_grp(sub, "roads", u"car road %s: carriageway + pavements" % x["rd"]):
                    sub.poly([TL(b3_band(P, [ww + 0.4] * len(P)))], fill=B3_COL["paving_edge"])
                    sub.poly([TL(b3_band(P, [ww] * len(P)))], fill=B3_COL["paving"])
                    sub.poly([TL(b3_band(P, [w] * len(P)))], fill=B3_COL["asphalt"], stroke=B3_COL["kerb"], lw=0.08)
                    sub.line(TL(P), "FFFFFF", 0.1, [1.2, 1.2], cap=0)
                    b6_arrows(sub, P, T, k, w)
                add_hard(P, ww / 2.0 + B3_TREE_CLEAR)
                n_rd["car (carriageway + pavements)"] = n_rd.get("car (carriageway + pavements)", 0) + 1
                road_names.append((x["rd"] + u" · cars + pedestrians", P[len(P) // 2]))
            else:
                with mpx_grp(sub, "roads", u"shared street %s" % (x["nm"] or h)):
                    sub.poly([TL(b3_band(P, [w + 0.4] * len(P)))], fill=B3_COL["paving_edge"])
                    sub.poly([TL(b3_band(P, [w] * len(P)))], fill=B3_COL["paving"])
                    b2_joints(sub, TL(P), [w * k] * len(P), 3.0 * k, B3_COL["joint"])
                add_hard(P, w / 2.0 + B3_TREE_CLEAR)
                n_rd["shared / pedestrian"] = n_rd.get("shared / pedestrian", 0) + 1
    street_pts = [q for x in vis if x["inz"] or any(ins(q) for q in x["P"]) for q in b3_dense(x["P"], 6.0)
                  if not in_chan(q)]
    # ================================================================ 5 walks + bike lane, continuous (F4)
    walks = b6_walks(C, cl, in_chan)                      # [(P, bank)] one continuous line per stretch and bank
    beds = [b3_chaikin_open(b3_dense(P, 6.0), 1) for P, bed, bank in cl["walk"] if bed and len(P) >= 2]
    canopy = []
    wp = [q for P, bank in walks for q in P]
    wp_idx = {}
    for q in wp:
        wp_idx.setdefault((int(q[0] // 10), int(q[1] // 10)), []).append(q)

    def near_pt(p, r, pts_idx):
        best = None
        for i in range(int((p[0] - r) // 10), int((p[0] + r) // 10) + 1):
            for j in range(int((p[1] - r) // 10), int((p[1] + r) // 10) + 1):
                for q in pts_idx.get((i, j), ()):
                    d = math.hypot(q[0] - p[0], q[1] - p[1])
                    if d <= r and (best is None or d < best[0]):
                        best = (d, q)
        return best
    for P in C.canopy:                                    # canopied walkway: only off the walk, long enough, tied
        piece = []
        for q in (b3_dense(P, 4.0) if len(P) >= 2 else []) + [None]:
            if q is not None and not near_pt(q, B3_WALK_W + 1.0, wp_idx) and not in_chan(q):
                piece.append(q)
                continue
            if len(piece) >= 2 and arclen(piece)[-1] >= 25.0:
                canopy.append(piece)
            piece = []
    bands = [(P, B3_WALK_W, B3_COL["paving"], u"riverside walk") for P, bank in walks]
    bands += [(P, B3_BED_W, B3_COL["gravel"], u"bed walk") for P in beds]
    bands += [(P, B3_CANOPY_W, B3_COL["paving"], u"canopied walkway") for P in canopy]
    st_idx = {}
    for q in street_pts:
        st_idx.setdefault((int(q[0] // 10), int(q[1] // 10)), []).append(q)
    links = []
    for P, w, col, nm in list(bands):                     # every end lands on a walk or a street
        if nm == u"riverside walk":
            continue
        for e in (P[0], P[-1]):
            nb = near_pt(e, B3_JOIN_MAX, wp_idx) or near_pt(e, B3_JOIN_MAX, st_idx)
            if nb and nb[0] > 0.5 and not any(in_chan(q) for q in b3_dense([e, nb[1]], 2.0)):
                links.append(([e, nb[1]], w, col))
    for P, w, col in links:
        bands.append((P, w, col, u"link"))
    for P, w, col, nm in bands:
        add_hard(P, w / 2.0 + (B3_BIKE_W + 0.3 if nm == u"riverside walk" else 0.0) + B3_TREE_CLEAR)
    cnt("riverside walk lines", len(walks))
    cnt("walk length m", int(sum(arclen(P)[-1] for P, bank in walks)))
    # ================================================================ 6 bridges (F5)
    br_bands, n_end = [], 0
    for c_ in C.cross:
        if not c_.get("P") or c_.get("kind") not in ("footbridge", "stepping stones"):
            continue
        a_, b_ = b6_to_land(c_["P"][0], c_["P"][1], in_chan), b6_to_land(c_["P"][1], c_["P"][0], in_chan)
        if not (ins(a_) or ins(b_)):
            continue
        for e in (a_, b_):
            nb = near_pt(e, B3_END_MAX, wp_idx) or near_pt(e, B3_END_MAX, st_idx)
            if nb is None:
                flags.append(u"FLAG %s: an end meets no walk or street within %.0f m" % (c_.get("name") or c_["kind"],
                                                                                        B3_END_MAX))
                continue
            if nb[0] > 0.5:
                br_bands.append(([e, nb[1]], B3_FOOT_W, B3_COL["paving"], u"bridge end path"))
            n_end += 1
        if c_["kind"] == "footbridge":
            br_bands.append(([a_, b_], B3_FOOT_W, B3_COL["deck"], u"new footbridge"))
            el_names.append((u"New footbridge", ((a_[0] + b_[0]) / 2.0, (a_[1] + b_[1]) / 2.0)))
        else:
            stones.append((a_, b_))
            el_names.append((u"Stepping stones", ((a_[0] + b_[0]) / 2.0, (a_[1] + b_[1]) / 2.0)))
    for P, w, col, nm in br_bands:
        add_hard(P, w / 2.0 + B3_TREE_CLEAR)
    # ================================================================ 7 hub squares, freed squares, programme (F6, F11)
    pads = []                                             # (kind, name, ring or centre, extra)
    for hb in C.hubs:
        for R in hb.get("square") or []:
            if len(R) >= 3 and any(ins(q) for q in R):
                pads.append(("square", None, R))
                add_hard(R + R[:1], 1.0)
    fr = [b3_hull(R) for R in b_rm if math.hypot(inner_pt(R)[0] - B3_ULU_XY[0], inner_pt(R)[1] - B3_ULU_XY[1]) < B3_ULU_R]
    pad_trees = []
    for H in fr:                                          # F11 (23:42): the freed Ulucami ground = hub square, plane shade
        pads.append(("freed", None, H))
        add_hard(H + H[:1], 3.0)
        bb = bbox(H)
        y_ = bb[1] + 4.0
        while y_ < bb[3]:
            x_ = bb[0] + 4.0
            while x_ < bb[2]:
                if pip(x_, y_, H):
                    pad_trees.append(((x_, y_), "plane", PLA_SPECIES["plane"]["crown_m"] * 0.6, u"square shade"))
                x_ += 8.0
            y_ += 8.0
    if fr:
        el_names.append((u"Ulucami Önü square: freed ground, plane shade", inner_pt(fr[0])))
        cnt("freed square pieces", len(fr))
    prog = b6_programme(C, ins)
    placed_pads = []
    for kind, nm_, p in prog:
        q = b6_free_spot(p, free, 30.0, 6.0)
        if q is None:
            flags.append(u"programme %s: no free ground within 30 m of its place" % nm_)
            continue
        R = b6_pad(kind, q, wp)
        pads.append((kind, nm_, R))
        placed_pads.append((q, kind))
        add_hard(R + R[:1], 1.5)
        if kind in ("hub_sq", "cafe"):
            a_, u_, v_, L_, W_ = b6_rect_axes(R)
            for s_ in (3.0, L_ - 3.0):
                pad_trees.append((b6_pt(a_, u_, v_, s_, W_ - 2.5), "plane", 7.0, u"square shade"))
        el_names.append((nm_, q))
        cnt(kind)
    for i_, (q, kind, nm_) in enumerate(b6_activity_spots(C, free, wp, widen, placed_pads, ins)):
        R = b6_pad(kind, q, wp)
        pads.append((kind, nm_, R))
        add_hard(R + R[:1], 1.5)
        el_names.append((nm_, q))
        cnt(kind)
        nb = near_pt(q, 120.0, wp_idx) or near_pt(q, 120.0, st_idx)
        if nb and nb[0] > 8.0:
            P = [q, nb[1]]
            if not any(in_chan(u) or in_bld(u) for u in b3_dense(P, 3.0)):
                bands.append((P, 2.0, B3_COL["gravel"], u"link"))
                add_hard(P, 1.0 + B3_TREE_CLEAR)
    # heritage trail (Q3, 00:25): the kept heritage buildings in stream order, joined along the walks, numbered
    trail = []
    for p in sorted([inner_pt(R) for R in b_her], key=lambda p: chain_at(C.ref, p)[0]):
        if all(math.hypot(p[0] - q[0], p[1] - q[1]) > 50.0 for q in trail):   # one stop per 50 m
            trail.append(p)
    # ================================================================ 8 edge threshold (F10)
    entr = b6_entrances(study, vis, ins)
    hedge, edge_trees = b6_edge(study, ins, entr)
    for c_ in entr:
        el_names.append((u"Entrance", c_))
    for P in beds:
        el_names.append((u"Bed walk, shut in floods", P[len(P) // 2]))
    for P in canopy:
        el_names.append((u"Canopied walkway", P[len(P) // 2]))
    # ================================================================ 9 draw the circulation (two passes, merged)
    allb = bands + br_bands
    with mpx_grp(sub, "paths", u"paths: edges"):
        for P, w, col, nm in allb:
            sub.poly([TL(b3_band(P, [w + 0.5] * len(P)))], fill=B3_COL["paving_edge"])
        for c_ in entr:
            sub.poly([TL(b3_circle(c_, B6_ENTRY_R + 0.4, 20))], fill=B3_COL["paving_edge"])
    with mpx_grp(sub, "paths", u"paths: surfaces"):
        for P, w, col, nm in allb:
            sub.poly([TL(b3_band(P, [w] * len(P)))], fill=col)
        for c_ in entr:
            sub.poly([TL(b3_circle(c_, B6_ENTRY_R, 20))], fill=B3_COL["paving"])
            b3_grid_fill(sub, TL(b3_circle(c_, B6_ENTRY_R, 20)), B3_COL["joint"], 2.0 * k * 4.0)
    cnt("entrances", len(entr))
    with mpx_grp(sub, "paths", u"bike lane beside the walk"):
        for P, bank in walks:
            sg = 1.0 if bank == "NE" else -1.0
            Pb = b6_clean_offset(P, sg * (B3_WALK_W / 2.0 + 0.3 + B3_BIKE_W / 2.0))
            if len(Pb) >= 2:
                sub.poly([TL(b3_band(Pb, [B3_BIKE_W] * len(Pb)))], fill=B3_COL["bike"])
                b6_bike_marks(sub, Pb, T, k)
    with mpx_grp(sub, "paths", u"joints, canopy posts, deck planks, ramps"):
        for P, w, col, nm in allb:
            if nm == u"riverside walk":
                b2_joints(sub, TL(P), [w * k] * len(P), 2.5 * k, B3_COL["joint"])
            elif nm == u"canopied walkway":
                for sg in (1.0, -1.0):
                    sub.line(b3_off(TL(P), sg * w * k / 2.0), B3_COL["deck_edge"], 0.1, [0.3, 0.9], cap=0)
            elif nm == u"new footbridge":
                sub.line(b3_off(TL(P), w * k / 2.0), B3_COL["deck_edge"], 0.1)
                sub.line(b3_off(TL(P), -w * k / 2.0), B3_COL["deck_edge"], 0.1)
        for P in beds:
            for e, nx in ((P[0], P[1]), (P[-1], P[-2])):
                b3_ramp(sub, T(e), T(nx), B3_BED_W * k, B3_COL["deck_edge"])
        for a_, b_ in stones:
            L_ = math.hypot(b_[0] - a_[0], b_[1] - a_[1])
            n_s = max(3, int(L_ / 2.2))
            for i in range(n_s):
                f = (i + 0.5) / n_s
                q = (a_[0] + (b_[0] - a_[0]) * f, a_[1] + (b_[1] - a_[1]) * f)
                sub.poly([TL(b3_circle(q, 0.7, 10))], fill=B3_COL["deck"], stroke=B3_COL["deck_edge"], lw=0.06)
    with mpx_grp(sub, "water", u"quay wall where a walk meets the water"):
        for R in chan:
            run = []
            for q in b3_dense(R + R[:1], 3.0) + [None]:
                if q is not None and ins(q) and near_pt(q, B3_WALK_W + 2.5, wp_idx):
                    run.append(q)
                    continue
                if len(run) >= 2:
                    sub.line(TL(run), B3_COL["wall"], 0.22)
                run = []
    for kind, nm_, R in pads:
        b6_draw_pad(sub, kind, R, T, k)
    with mpx_grp(sub, "annotations", u"heritage trail"):
        for P in cl["sight"]:
            if len(P) >= 2:
                sub.line(TL(P), B3_COL["ink"], 0.12, [1.4, 0.8], cap=0)
                el_names.append((u"Sightline to the Trajaneum", P[0]))
        for i_, p in enumerate(trail):
            x_, y_ = T(p)
            sub.poly([b3_circle((x_, y_), 1.2, 16)], fill=B3_COL["heritage"], stroke=B3_COL["ink"], lw=0.08)
            sub.text(u"%d" % (i_ + 1), x_, y_ - 0.55, 1.76, "FFFFFF", bold=True, align="C")
    cnt("heritage trail stops", len(trail))
    # ================================================================ 10 planting by function (F9)
    plants = pad_trees + b6_planting(C, chan, widen, walks, free, hedge, edge_trees, sv, ins)
    hedge_d = [Q for P in hedge for Q in b6_split(b3_dense(P, 3.0), lambda q: on_hard(q, 1.0) or in_wet(q) or
                                                     in_bld(q, 1.0) or not ins(q)) if arclen(Q)[-1] >= 6.0]
    with mpx_grp(sub, "plants", u"edge hedge (threshold, open at entrances)"):
        for P in hedge_d:
            sub.poly([TL(b3_band(P, [2.2] * len(P)))], fill=B3_COL["tree2"], stroke=B3_COL["tree_edge"], lw=0.06)
    for P in hedge_d:
        add_hard(P, 1.1)
    cnt("hedge m", int(sum(arclen(P)[-1] for P in hedge_d)))
    placed = []
    n_t, n_skip, n_sk = 0, 0, {}
    with mpx_grp(sub, "trees", u"planting"):
        for p, key, cr, why in plants:
            cr = cr or (PLA_SPECIES.get(key) or {}).get("crown_m") or 4.0
            if why in (u"wetland emergent",):
                ok_ = ins(p) and not in_chan(p) and not on_hard(p, 0.5)
            elif why in (u"square shade", u"terrace olives"):
                ok_ = ins(p) and not in_wet(p) and not in_bld(p, cr * 0.3)
            else:
                ok_ = free(p, min(cr * 0.3, 2.0))                # crowns may overhang a path
            if not ok_:
                n_skip += 1
                n_sk[why] = n_sk.get(why, 0) + 1
                continue
            if any(math.hypot(p[0] - q[0], p[1] - q[1]) < (cr + c2) * 0.4 for q, c2 in placed):
                n_skip += 1
                n_sk[why + u" (spacing)"] = n_sk.get(why + u" (spacing)", 0) + 1
                continue
            x_, y_ = T(p)
            sub.poly([b3_circle((x_ + 0.2 * cr * k, y_ - 0.2 * cr * k), cr * k / 2.0, 14)], fill=B3_COL["tree_sh"],
                     alpha=0.3)
            try:
                pl23_put(sub, _B19_PLA_ASSET(key, x_, y_, k, crown_m=cr, seed=n_t, distinct=True))
            except Exception:
                b3_tree(sub, (x_, y_), cr * k / 2.0, n_t, key)
            placed.append((p, cr))
            n_sp[why] = n_sp.get(why, 0) + 1
            n_t += 1
    # ================================================================ 11 fade, buildings, zone line
    with mpx_grp(sub, "ground", u"edge fade"):
        prev = st
        for d_m, a in B2_FADE:
            grown = [b2_offset_out(R, d_m) for R in study]
            if any(g is None for g in grown):
                break
            grown = b2_union(grown, warn)
            ring_s = [TL(g) for g in grown]
            sub.poly(ring_s + prev, fill="FFFFFF", alpha=a)
            prev = ring_s
        sub.poly([rect(0.0, 0.0, dw, dh)] + prev, fill="FFFFFF", alpha=B2_CONTEXT_VEIL)
    with mpx_grp(sub, "buildings", u"context buildings"):
        for R in b_out:
            sub.poly([TL(R)], fill=B3_COL["bld_ctx"], stroke=B3_COL["bld_ctx_edge"], lw=0.06)
    with mpx_grp(sub, "annotations", u"project zone"):
        for Q in st:
            sub.line(Q + Q[:1], B3_COL["border"], 0.3)
    sh = 0.9 * k
    with mpx_grp(sub, "heritage", u"heritage buildings, kept"):
        for R in b_her:
            sub.poly([[(x + sh, y - sh) for x, y in TL(R)]], fill=B3_COL["shadow"], alpha=0.45)
            sub.poly([TL(R)], fill=B3_COL["heritage"], stroke=B3_COL["bld_edge"], lw=0.13)
    # ================================================================ 12 names (beside what they name)
    taken = [b6_pbox(TL(R)) for R in keep_b if b6_pbox(TL(R))[2] - b6_pbox(TL(R))[0] > 0.6]
    labels, left = [], []
    seen = {}
    wpt = lambda bx, by: (x0 + bx / k, y0 + by / k)
    zin = lambda bx, by: ins(wpt(bx, by))

    def clear(b):
        for bx in (b[0], (b[0] + b[2]) / 2.0, b[2]):
            for by in (b[1], (b[1] + b[3]) / 2.0, b[3]):
                q = wpt(bx, by)
                if on_hard(q) or in_wet(q):
                    return False
        return True

    def name(s_, p, size, bold=False):
        if any(math.hypot(p[0] - q[0], p[1] - q[1]) < 250.0 for q in seen.get(s_, [])):
            return True
        seen.setdefault(s_, []).append(p)
        x, y = T(p)
        w_ = text_w(s_, size, bold)
        spots = [(1.2, 0.8), (-1.2 - w_, 0.8), (1.2, -size - 0.8), (-1.2 - w_, -size - 0.8), (-w_ / 2.0, 2.0),
                 (-w_ / 2.0, -size - 2.0)]
        for rr in (5.0, 8.0, 12.0, 17.0):
            for ia in range(12):
                ang = ia * math.pi / 6.0
                cx_, cy_ = rr * math.cos(ang), rr * math.sin(ang)
                spots.append((cx_ - (0.0 if cx_ >= 0 else w_), cy_ - size / 2.0))
        for strict in (True, False):
            for dx, dy in spots:
                b = (x + dx, y + dy, x + dx + w_, y + dy + size)
                if not (0 <= b[0] and b[2] <= dw and 0 <= b[1] and b[3] <= dh) or any(hit(b, o, 0.4) for o in labels):
                    continue
                if not clear(b):
                    continue
                if strict and (any(hit(b, o, 0.4) for o in taken) or not (zin(b[0], b[1]) and zin(b[2], b[3]))):
                    continue
                labels.append(b)
                sub.text(s_, b[0], b[1], size, B3_COL["ink"], bold=bold)
                tx, ty = min(max(x, b[0]), b[2]), min(max(y, b[1]), b[3])
                if math.hypot(tx - x, ty - y) > 1.2:
                    sub.line([(x, y), (tx, ty)], B3_COL["ink"], 0.08)
                return True
        return False
    for hb in C.hubs:
        if hb.get("in_study") and not name(b3_title(HUB_NAME.get(hb["id"], hb["id"])), hb["xy"], 2.12, True):
            left.append(hb["id"])
    for nm_, p in el_names:
        if not name(nm_, p, 1.76):
            left.append(nm_)
    for nm_, p in road_names:
        name(nm_, p, 1.76)
    for i_, p in enumerate(trail):
        nm_ = b6_heritage_name(p)
        name(u"%d %s" % (i_ + 1, nm_), p, 1.76)
    for z in C.D.zones:
        if z.get("label") and z.get("q") and ins(z["q"]) and z["code"] in ("WT", "WS", "GR", "WP", "DG", "WD"):
            if not name(b3_title(z["label"], first_only=True), z["q"], 1.76):
                left.append(z["label"])
    for P in C.terr[:1]:
        name(u"Rain terraces on the contours", P[len(P) // 2], 1.76)
    for P, bank in walks[:2]:
        name(u"Riverside walk + bike lane", P[len(P) // 3], 1.76)
    # ================================================================ sheet
    W, H = dw + 2 * B19_M, dh + 2 * B19_M + B19_HEAD + 22.0
    pg = Page(W, H)
    pg.poly([rect(0.0, 0.0, W, H)], fill="FFFFFF")
    oy = B19_M + B19_HEAD + 22.0
    pg.clip([rect(B19_M, oy, B19_M + dw, oy + dh)])
    blit(pg, sub, B19_M, oy)
    pg.unclip()
    lx, ly = B19_M, oy - 8.0
    for nm, col in B6_LEGEND:
        tw = text_w(nm, 2.12)
        if lx + 10.0 + tw > W - B19_M:
            lx, ly = B19_M, ly - 6.0
        pg.poly([rect(lx, ly, lx + 8.0, ly + 4.0)], fill=col, stroke=B3_COL["kerb"], lw=0.1)
        pg.text(nm, lx + 10.0, ly + 0.8, 2.12, B3_COL["ink"])
        lx += 16.0 + tw
    pg.text(u"MIRAQUA · MASTERPLAN", B19_M, B19_M + 8.0, 4.2, B3_COL["ink"], bold=True)
    pg.text(u"drawing language after Greenikka (Arkkitehdit MY, 2020)", B19_M, B19_M + 3.0, 2.12, B3_COL["ink"])
    scale_bar(pg, B19_M + 120.0, B19_M + 3.0, scale, marks=(0.0, 50.0, 100.0, 200.0))
    nx, ny, h_ = W - B19_M - 4.0, B19_M + 2.0, 12.0
    pg.poly([[(nx, ny + h_), (nx - 2.6, ny + 0.45 * h_), (nx, ny + 0.6 * h_), (nx + 2.6, ny + 0.45 * h_)]],
            fill=B3_COL["ink"])
    pg.line([(nx, ny), (nx, ny + 0.6 * h_)], B3_COL["ink"], 0.25)
    pg.text(u"N", nx, ny + h_ + 1.0, 3.0, B3_COL["ink"], bold=True, align="C")
    notes += [u"elements: " + u", ".join(u"%s %d" % kv for kv in sorted(n_el.items())),
              u"streets in the zone: " + u", ".join(u"%s %d" % kv for kv in sorted(n_rd.items())),
              u"planting by function: " + u", ".join(u"%s %d" % kv for kv in sorted(n_sp.items())) +
              u" ({} not placed: ".format(n_skip) + u", ".join(u"%s %d" % kv for kv in sorted(n_sk.items())) + u")",
              u"bridge ends on a walk or street: {}".format(n_end),
              u"buildings: {} heritage kept, {} taken out, {} context".format(len(b_her), len(b_rm), len(b_out)),
              u"names left out (no room): " + (u"; ".join(left) or u"none"), u"{:.1f} s".format(time.time() - t0)]
    return pg, notes + flags


def b3_title(s, first_only=False):
    """Turkish-safe title case (no dotted-i glitch): ÜÇ KEMER -> Üç Kemer"""
    low = lambda w: w.replace(u"I", u"ı").replace(u"İ", u"i").lower()
    ws = s.split(u" ")
    out = []
    for i, w in enumerate(ws):
        lw = low(w)
        out.append(lw[:1].upper().replace(u"i", u"İ") + lw[1:] if (i == 0 or not first_only) and lw else lw)
    return u" ".join(out)


def b3_dense(P, step):
    """the polyline with extra points every step m (so a cut at the water follows the bank)"""
    out = [P[0]]
    for a, b in zip(P[:-1], P[1:]):
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) // step))
        out += [(a[0] + (b[0] - a[0]) * i / float(n), a[1] + (b[1] - a[1]) * i / float(n)) for i in range(1, n + 1)]
    return out


def b3_channel(C):
    """the open stream as one water ring per stretch between the two bank edges of the stations; where stations
    are missing for up to 160 m the channel goes on along the corridor reference line, each side as wide as at the
    nearer station but at most B3_NECK m (no gaps, no invented wide water)"""
    rows = sorted([r for r in C.rows if not r["cov"] and "e" in (r.get("NE") or {}) and "e" in (r.get("SW") or {})],
                  key=lambda r: r["ch"])
    ref = list(C.ref)
    cum = [0.0]
    for a, b in zip(ref[:-1], ref[1:]):
        cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))

    def at(ch):
        for i in range(1, len(ref)):
            if cum[i] >= ch:
                a, b = ref[i - 1], ref[i]
                t = (ch - cum[i - 1]) / max(cum[i] - cum[i - 1], 1e-9)
                L = max(math.hypot(b[0] - a[0], b[1] - a[1]), 1e-9)
                return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), (-(b[1] - a[1]) / L, (b[0] - a[0]) / L)
        return None, None
    runs, cur, last = [], [], None
    for r in rows:
        e1, e2 = r["NE"]["e"], r["SW"]["e"]
        if last is not None and r["ch"] - last["ch"] > 12.0:
            if r["ch"] - last["ch"] > 160.0:
                runs.append(cur)
                cur = []
            else:
                ch = last["ch"] + 8.0
                while ch < r["ch"] - 4.0:
                    p, n = at(ch)
                    if p is not None:
                        if n[0] * last["n"][0] + n[1] * last["n"][1] < 0:
                            n = (-n[0], -n[1])
                        u = (ch - last["ch"]) / (r["ch"] - last["ch"])
                        a_ = min(last["NE"]["e"] * (1 - u) + e1 * u, B3_NECK)
                        b_ = max(last["SW"]["e"] * (1 - u) + e2 * u, -B3_NECK)
                        cur.append((p, n, a_, b_))
                    ch += 8.0
        cur.append((r["p"], r["n"], e1, e2))
        last = r
    if cur:
        runs.append(cur)
    out = []
    for run in runs:
        if len(run) < 3:
            continue
        A = [(p[0] + n[0] * a, p[1] + n[1] * a) for p, n, a, b in run]
        B = [(p[0] + n[0] * b, p[1] + n[1] * b) for p, n, a, b in run]
        out.append(A + B[::-1])
    return out


def b3_dots(pg, b, step, col, clip):
    """meadow texture: short strokes on a jittered grid inside the clip rings (page mm)"""
    rnd = random.Random(7)
    pg.clip(clip)
    y = b[1]
    while y < b[3]:
        x = b[0]
        while x < b[2]:
            px, py = x + rnd.uniform(0, step), y + rnd.uniform(0, step)
            if any(pip(px, py, R) for R in clip):
                pg.line([(px, py), (px + 0.25, py + 0.35)], col, 0.07)
            x += step
        y += step
    pg.unclip()


def b3_near_rings(boxes, p):
    return [R for b, R in boxes if b[0] <= p[0] <= b[2] and b[1] <= p[1] <= b[3]]


def b3_dist_ring(R, p):
    return min(seg_dist(p[0], p[1], a, b) for a, b in zip(R, R[1:] + R[:1]))


def b3_off(Q, d):
    return pl23_offset(Q, d)


B3_TREE_TONE = dict(willow="AAB59C", tamarisk="9EA394", ash="86967A", plane="6F8064")   # v4: wet edge light, dry ground dark


def b3_tree(pg, c, r, i, key=None):
    """B19 crown: cast shadow to the south-east, crown body (tone by species: willow / tamarisk light on the wet
    edge, ash / plane darker on drier ground), a lighter top lobe, a fine edge"""
    r = max(r, 0.45)
    tone = B3_TREE_TONE.get(key) or (B3_COL["tree1"], B3_COL["tree2"], B3_COL["tree3"])[i % 3]
    pg.poly([b3_circle((c[0] + 0.22 * r, c[1] - 0.22 * r), r, 16)], fill=B3_COL["tree_sh"], alpha=0.35)
    pg.poly([b3_circle(c, r, 18)], fill=tone, stroke=B3_COL["tree_edge"], lw=0.06, alpha=0.92)
    pg.poly([b3_circle((c[0] - 0.25 * r, c[1] + 0.25 * r), 0.45 * r, 12)], fill=B3_COL["tree_hi"], alpha=0.55)


def b3_ticks_fill(pg, Q, col, step):
    """reed texture: short vertical ticks on a grid inside ring Q (page mm)"""
    b = bbox(Q)
    y = b[1] + step / 2.0
    row = 0
    while y < b[3]:
        x = b[0] + (step / 2.0 if row % 2 else 0.0)
        while x < b[2]:
            if pip(x, y, Q):
                pg.line([(x, y - 0.35), (x, y + 0.35)], col, 0.07)
            x += step
        y += step * 0.8
        row += 1


def b3_ramp(pg, e, nx, w, col):
    """ramp symbol at walk end e pointing down toward nx (page mm): three chevrons across width w + a small arrow"""
    L = math.hypot(nx[0] - e[0], nx[1] - e[1])
    if L < 1e-6:
        return
    ux, uy = (nx[0] - e[0]) / L, (nx[1] - e[1]) / L
    for i in range(3):
        cx, cy = e[0] + ux * (0.5 + 0.6 * i), e[1] + uy * (0.5 + 0.6 * i)
        pg.line([(cx - uy * w / 2.0, cy + ux * w / 2.0), (cx + ux * 0.35, cy + uy * 0.35),
                 (cx + uy * w / 2.0, cy - ux * w / 2.0)], col, 0.07)


def b3_mix(a, b, f):
    """hex colour between a (f=0) and b (f=1)"""
    A, B = hex_rgb(a), hex_rgb(b)
    return u"".join(u"%02X" % int(round(255 * (x + (y - x) * f))) for x, y in zip(A, B))


def b3_chaikin_closed(R, n):
    for _ in range(n):
        Q = []
        for a, b in zip(R, R[1:] + R[:1]):
            Q += [(0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]), (0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1])]
        R = Q
    return R


def b3_hull(R):
    """convex hull of a ring (monotone chain)"""
    P = sorted(set((round(p[0], 3), round(p[1], 3)) for p in R))
    if len(P) < 3:
        return list(R)
    cr = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in P:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def b3_ticks_line(pg, Q, col, lw, step, length):
    """short ticks to one side of polyline Q every step (page mm): a terrace edge"""
    acc = 0.0
    for a, b in zip(Q[:-1], Q[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L < 1e-9:
            continue
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        t = (step - acc) if acc > 0 else 0.0
        while t <= L:
            x, y = a[0] + ux * t, a[1] + uy * t
            pg.line([(x, y), (x + uy * length, y - ux * length)], col, lw)
            t += step
        acc = (acc + L) % step


def b3_grid_fill(pg, Q, col, step):
    """paving joint grid inside ring Q (page mm)"""
    b = bbox(Q)
    pg.clip([Q])
    v = b[0] + step
    while v < b[2]:
        pg.line([(v, b[1]), (v, b[3])], col, 0.05)
        v += step
    v = b[1] + step
    while v < b[3]:
        pg.line([(b[0], v), (b[2], v)], col, 0.05)
        v += step
    pg.unclip()


def b3_rows_fill(pg, Q, col, step):
    """garden rows: parallel lines along the ring's long axis, clipped to it"""
    b = bbox(Q)
    pg.clip([Q])
    horiz = (b[2] - b[0]) >= (b[3] - b[1])
    v = (b[1] if horiz else b[0]) + step / 2.0
    while v < (b[3] if horiz else b[2]):
        pg.line([(b[0], v), (b[2], v)] if horiz else [(v, b[1]), (v, b[3])], col, 0.08)
        v += step
    pg.unclip()


def b3_reed_edge(pg, Q, col, h):
    """reed fringe along the water edge line Q (page mm): short strokes leaning off the water"""
    s = arclen(Q)
    t = 0.0
    while t < s[-1]:
        (x, y), (ux, uy) = at_len(Q, s, t)
        pg.line([(x, y), (x - uy * h + ux * h * 0.3, y + ux * h + uy * h * 0.3)], col, 0.08)
        t += 0.7


def b3_ripples(pg, C, T, k):
    """B19 water texture: short pale strokes along the flow, inside the water"""
    rnd = random.Random(19)
    rws = C.rows[::4]
    for R, Hs in pl23_water_groups(C):
        b = bbox(R)
        n = int((b[2] - b[0]) * (b[3] - b[1]) / 900.0)
        for _ in range(min(n, 900)):
            p = (rnd.uniform(b[0], b[2]), rnd.uniform(b[1], b[3]))
            if not pip(p[0], p[1], R):
                continue
            r_ = min(rws, key=lambda r: (r["p"][0] - p[0]) ** 2 + (r["p"][1] - p[1]) ** 2) if rws else None
            if r_ is None:
                continue
            ux, uy = r_["n"][1], -r_["n"][0]
            L = rnd.uniform(1.5, 4.0)
            a, b_ = T((p[0] - ux * L, p[1] - uy * L)), T((p[0] + ux * L, p[1] + uy * L))
            pg.line([a, b_], B3_COL["ripple"], 0.07)



# ================================================================ v6 (6 Nov 2026, Aras 00:03-00:25, previews/V6_PLAN.md)
# Design values (m unless noted). Car roads kept: the only two that carry cars + pedestrians (Aras 00:25 Q2).
B6_CAR_ROADS = (u"Bergama - Kozak Yolu", u"Adnan Menderes Bulvarı")
B6_PAVEMENT = 2.0            # pavement each side of a kept car road
B6_ENTRY_R = 9.0             # entrance square radius where a street meets the zone
B6_ROAD_GAP = 1.0            # the stream edge stops this short of a car road's pavement
B6_SMOOTH_M = 20.0           # stream widths averaged over this length (no necks, spikes or rectangles)
B6_STEP_Z = 2.0              # ground darkens with every 2 m above the stream bed (F8)
B6_CELL = 8.0                # height cell size
B6_TERR_W = 6.0              # rain terrace level band (F7)
B6_HEDGE_IN = 2.5            # hedge centre this far inside the zone line (F10)
B6_EDGE_TREE_IN = 7.0        # edge tree row this far inside the zone line
B6_EDGE_TREE_STEP = 18.0
B6_PAD = dict(square=(0, 0), hub_sq=(22.0, 18.0), cafe=(16.0, 10.0), classroom=(13.0, 9.0), seats=(14.0, 3.0),
              arch=(18.0, 6.0), view=(11.0, 8.0), subhub=(9.0, 7.0), court=(28.0, 15.0), fitness=(14.0, 9.0),
              play=(18.0, 14.0), event=(46.0, 30.0), picnic=(26.0, 18.0), allot=(34.0, 22.0), meadow=(54.0, 36.0),
              hide=(10.0, 3.0))
B6_ROUND = ("play", "event", "picnic", "meadow")
# the programme of the liked examples (Aras 23:45, 00:25 Q3): kind, name, how many, m from the walk (min, max)
B6_ACTIVITIES = (("court", u"Courts", 3, 20.0, 140.0), ("fitness", u"Fitness corner", 3, 6.0, 40.0),
                 ("play", u"Play, sand", 4, 6.0, 45.0), ("event", u"Event lawn", 1, 15.0, 140.0),
                 ("picnic", u"Picnic lawn", 3, 8.0, 70.0), ("allot", u"Community allotments", 2, 15.0, 160.0),
                 ("meadow", u"Pollinator meadow, mown paths", 3, 20.0, 220.0))
B6_PAD_SPACING = 60.0        # two pads at least this far apart


def b6_ccw(R):
    return area2(R) > 0


def b6_inward(R):
    """unit inward normals of ring R (per vertex)"""
    s = 1.0 if b6_ccw(R) else -1.0
    out, n = [], len(R)
    for i in range(n):
        a, b = R[i - 1], R[(i + 1) % n]
        ux, uy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(ux, uy) or 1.0
        out.append((-uy / L * s, ux / L * s))
    return out


def b6_channel(C, car_ways):
    """F3: the open stream from the stations' bank edges only (gaps up to 160 m along the reference line, as v5),
    widths averaged over B6_SMOOTH_M, each edge kept B6_ROAD_GAP short of a car road's pavement (bridges excepted).
    Returns rings (survey m)."""
    rows = sorted([r for r in C.rows if not r["cov"] and "e" in (r.get("NE") or {}) and "e" in (r.get("SW") or {})],
                  key=lambda r: r["ch"])
    ref = list(C.ref)
    cum = [0.0]
    for a, b in zip(ref[:-1], ref[1:]):
        cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))

    def at(ch):
        for i in range(1, len(ref)):
            if cum[i] >= ch:
                a, b = ref[i - 1], ref[i]
                t = (ch - cum[i - 1]) / max(cum[i] - cum[i - 1], 1e-9)
                L = max(math.hypot(b[0] - a[0], b[1] - a[1]), 1e-9)
                return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), (-(b[1] - a[1]) / L, (b[0] - a[0]) / L)
        return None, None
    runs, cur, last = [], [], None
    for r in rows:
        e1, e2 = r["NE"]["e"], r["SW"]["e"]
        if last is not None and r["ch"] - last["ch"] > 12.0:
            if r["ch"] - last["ch"] > 160.0:
                runs.append(cur)
                cur = []
            else:
                ch = last["ch"] + 8.0
                while ch < r["ch"] - 4.0:
                    p, n = at(ch)
                    if p is not None:
                        if n[0] * last["n"][0] + n[1] * last["n"][1] < 0:
                            n = (-n[0], -n[1])
                        u = (ch - last["ch"]) / (r["ch"] - last["ch"])
                        cur.append((ch, p, n, min(last["NE"]["e"] * (1 - u) + e1 * u, B3_NECK),
                                    max(last["SW"]["e"] * (1 - u) + e2 * u, -B3_NECK)))
                    ch += 8.0
        cur.append((r["ch"], r["p"], r["n"], e1, e2))
        last = r
    if cur:
        runs.append(cur)
    segs = []
    for x in car_ways:
        if x.get("br"):
            continue
        r_ = x["w"] / 2.0 + B6_PAVEMENT + B6_ROAD_GAP
        segs += [(a, b, r_) for a, b in zip(x["P"][:-1], x["P"][1:])]
    sidx = {}
    for i, (a, b, r_) in enumerate(segs):
        for gi in range(int(min(a[0], b[0]) // 30) - 1, int(max(a[0], b[0]) // 30) + 2):
            for gj in range(int(min(a[1], b[1]) // 30) - 1, int(max(a[1], b[1]) // 30) + 2):
                sidx.setdefault((gi, gj), []).append(i)

    def clash(q):
        for i in sidx.get((int(q[0] // 30), int(q[1] // 30)), ()):
            a, b, r_ = segs[i]
            if seg_dist(q[0], q[1], a, b) < r_:
                return True
        return False
    out = []
    for run in runs:
        if len(run) < 3:
            continue
        chs = [c for c, p, n, a, b in run]
        A, B = [], []
        for i, (c, p, n, a, b) in enumerate(run):
            w = [j for j in range(len(run)) if abs(chs[j] - c) <= B6_SMOOTH_M / 2.0]
            a_ = sum(run[j][3] for j in w) / len(w)
            b_ = sum(run[j][4] for j in w) / len(w)
            for side, e in ((0, a_), (1, b_)):
                f = 1.0
                q = (p[0] + n[0] * e, p[1] + n[1] * e)
                while f > 0.15 and clash(q):
                    f -= 0.1
                    q = (p[0] + n[0] * e * f, p[1] + n[1] * e * f)
                (A if side == 0 else B).append(q)
        out.append(A + B[::-1])
    return out


def b6_height_steps(sub, C, T, k, ins, study):
    """F8: the zone's ground in 2 m steps above the stream bed, from the survey's levelling points
    (NOKTA_TAKEOMETRI, 3D): bed = lowest point within 25 m of the reference line per 40 m of stream; each 8 m cell
    takes the inverse-distance height of the points within 30 m; one darker veil per step. Returns cells drawn."""
    bb = [bbox(R) for R in study]
    box = (min(b[0] for b in bb) - 30, min(b[1] for b in bb) - 30, max(b[2] for b in bb) + 30, max(b[3] for b in bb) + 30)
    sp = [(x, y, z) for x, y, z in (getattr(C, "spots", None) or []) if box[0] <= x <= box[2] and box[1] <= y <= box[3]]
    if len(sp) < 20 or len(C.ref) < 2:
        return 0
    ref = list(C.ref)
    bins, grid = {}, {}
    for x, y, z in sp:
        ch, d = chain_at(ref, (x, y))
        if d < 25.0:
            b_ = int(ch // 40)
            bins[b_] = min(bins.get(b_, 1e9), z)
        grid.setdefault((int(x // 30), int(y // 30)), []).append((x, y, z, ch))
    if not bins:
        return 0
    keys = sorted(bins)

    def bed(ch):
        b_ = ch / 40.0
        lo = [kk for kk in keys if kk <= b_]
        hi = [kk for kk in keys if kk >= b_]
        if not lo:
            return bins[hi[0]]
        if not hi:
            return bins[lo[-1]]
        a, c = lo[-1], hi[0]
        return bins[a] if a == c else bins[a] + (bins[c] - bins[a]) * (b_ - a) / float(c - a)
    lv = {}
    for R in study:
        b = bbox(R)
        y = b[1] + B6_CELL / 2.0
        while y < b[3]:
            x = b[0] + B6_CELL / 2.0
            while x < b[2]:
                if pip(x, y, R):
                    sw = sz = sc = 0.0
                    for i in (-1, 0, 1):
                        for j in (-1, 0, 1):
                            for qx, qy, qz, qc in grid.get((int(x // 30) + i, int(y // 30) + j), ()):
                                d = math.hypot(qx - x, qy - y)
                                if d <= 30.0:
                                    w = 1.0 / max(d, 1.0) ** 2
                                    sw += w
                                    sz += w * qz
                                    sc += w * qc
                    if sw > 0:
                        n_ = int(max(0.0, sz / sw - bed(sc / sw)) // B6_STEP_Z)
                        if n_ > 0:
                            h_ = B6_CELL / 2.0
                            lv.setdefault(min(n_, 8), []).append(rect(*(T((x - h_, y - h_)) + T((x + h_, y + h_)))))
                x += B6_CELL
            y += B6_CELL
    for n_ in sorted(lv):
        with mpx_grp(sub, "ground", u"ground %g-%g m above the stream bed" % (n_ * B6_STEP_Z, (n_ + 1) * B6_STEP_Z)):
            sub.poly(lv[n_], fill=B3_COL["contour_dk"], alpha=0.045 * n_)
    return sum(len(v) for v in lv.values())


def b6_steps(sub, P, T, k):
    """F6/F7: stepped terraces in a zone ring: level green with a wall line round it and a step line every 6 m"""
    Q = [T(p) for p in P]
    sub.poly([Q], fill=B3_COL["lawn_dk"], stroke=B3_COL["wall"], lw=0.1)
    b3_rows_fill(sub, Q, B3_COL["contour_dk"], B6_TERR_W * k)


def b6_terrace(sub, C, P, T, k):
    """F7: a rain terrace = a 6 m level band on its contour, a wall line on its low side (toward the stream),
    slope hatching below the wall"""
    if len(P) < 2:
        return
    m = P[len(P) // 2]
    Q = b3_off(P, 5.0)
    sg = -1.0 if chain_at(C.ref, Q[len(Q) // 2])[1] < chain_at(C.ref, m)[1] else 1.0   # +1: low side is the right
    TP = [T(p) for p in P]
    sub.poly([[T(q) for q in b3_band(P, [B6_TERR_W] * len(P))]], fill=B3_COL["lawn_dk"])
    low = b3_off(TP, -sg * B6_TERR_W * k / 2.0)
    sub.line(low, B3_COL["wall"], 0.16)
    hatch = low if sg > 0 else low[::-1]
    b3_ticks_line(sub, hatch, B3_COL["contour_dk"], 0.06, 1.0, 2.5 * k)


def b6_arrows(sub, P, T, k, w):
    """Q2: direction of travel on a kept car road: one arrow per lane every 70 m (right-hand traffic)"""
    s = arclen(P)
    t = 35.0
    while t < s[-1] - 10.0:
        (x, y), (ux, uy) = at_len(P, s, t)
        for sg in (-1.0, 1.0):                            # -1: right lane, forward; +1: left lane, backward
            cx, cy = x - uy * sg * w / 4.0, y + ux * sg * w / 4.0
            dx, dy = (ux, uy) if sg < 0 else (-ux, -uy)
            L, H = 4.0, 0.9
            tip = (cx + dx * L / 2.0, cy + dy * L / 2.0)
            bx, by = cx + dx * (L / 2.0 - 1.6), cy + dy * (L / 2.0 - 1.6)
            sub.poly([[T(tip), T((bx - dy * H, by + dx * H)), T((bx + dy * H, by - dx * H))]], fill="FFFFFF")
            sub.line([T((cx - dx * L / 2.0, cy - dy * L / 2.0)), T((bx, by))], "FFFFFF", 0.1)
        t += 70.0


def b6_split(P, bad):
    out, cur = [], []
    for q in P + [None]:
        if q is not None and not bad(q):
            cur.append(q)
            continue
        if len(cur) >= 2:
            out.append(cur)
        cur = []
    return out


def b6_walks(C, cl, in_chan):
    """F4: one continuous riverside walk per bank: the masterplan's walk pieces cut off the water, ordered along
    the stream, pieces lying on an earlier one dropped, overlaps trimmed, gaps up to 150 m closed when the join
    stays dry; then smoothed and cut off the water again. Returns [(P, bank)]."""
    ref = list(C.ref)
    by_bank = {}
    for P, bed, bank in cl["walk"]:
        if bed or not bank or len(P) < 2:
            continue
        for Q in b6_split(b3_dense(P, 4.0), in_chan):
            if arclen(Q)[-1] >= 8.0:
                by_bank.setdefault(bank, []).append(Q)
    out = []
    for bank in sorted(by_bank):
        items = []
        for P in by_bank[bank]:
            chs = [chain_at(ref, q)[0] for q in P]
            if chs[-1] < chs[0]:
                P, chs = P[::-1], chs[::-1]
            items.append([chs[0], chs[-1], P, chs])
        items.sort(key=lambda t: (t[0], -(t[1] - t[0])))
        acc = []
        for it in items:
            if acc and it[1] <= acc[-1][1] + 4.0:
                continue                                  # lies on the stretch already taken
            if acc and it[0] < acc[-1][1]:
                keep = [i for i, c in enumerate(it[3]) if c >= acc[-1][1]]
                if len(keep) < 2:
                    continue
                it = [it[3][keep[0]], it[1], it[2][keep[0]:], it[3][keep[0]:]]
            acc.append(it)
        lines, cur = [], None
        for it in acc:
            if cur is None:
                cur = list(it[2])
                continue
            e, s0 = cur[-1], it[2][0]
            gap = math.hypot(s0[0] - e[0], s0[1] - e[1])
            if gap < 150.0 and not any(in_chan(q) for q in b3_dense([e, s0], 2.0)):
                cur += list(it[2])
            else:
                lines.append(cur)
                cur = list(it[2])
        if cur:
            lines.append(cur)
        for P in lines:
            Q = [P[0]]
            for q in P[1:]:
                if math.hypot(q[0] - Q[-1][0], q[1] - Q[-1][1]) >= 2.5:
                    Q.append(q)
            Q = b3_chaikin_open(Q, 2)
            for R in b6_split(Q, in_chan):
                if arclen(R)[-1] >= 15.0:
                    out.append((R, bank))
    return out


def b6_to_land(a, b, in_chan):
    """F5: footbridge end a moved outward (away from b) until it stands 1.5 m on dry land (at most 30 m)"""
    L = math.hypot(a[0] - b[0], a[1] - b[1]) or 1.0
    ux, uy = (a[0] - b[0]) / L, (a[1] - b[1]) / L
    t = 0.0
    while t < 30.0 and in_chan((a[0] + ux * t, a[1] + uy * t)):
        t += 1.0
    return (a[0] + ux * (t + 1.5), a[1] + uy * (t + 1.5)) if t > 0 else a


def b6_programme(C, ins):
    """F6: the masterplan's named programme as drawn open-air elements (Aras draws the 3 facility buildings)"""
    out, n_ = [], {}

    def add(kind, nm, p, most):
        if p and ins(p) and n_.get(kind, 0) < most:
            n_[kind] = n_.get(kind, 0) + 1
            out.append((kind, nm, p))
    for z in C.D.zones:
        q = z.get("q")
        if z["code"] in ("GR", "DG"):
            add("cafe", u"Café terrace", q, 2)
        elif z["code"] == "WT":
            add("classroom", u"Outdoor classroom, reed basins", q, 2)
        elif z["code"] == "WS" or (z["code"] == "WA" and z.get("tier") == "F"):
            add("seats", u"Seats", q, 4)
    add("classroom", u"Craft yard (workshops)", CRAFT_XY, 3)
    add("arch", u"Archaeology deck", ROMAN_WALL, 1)
    if C.terrace:
        add("view", u"Viewing terrace", C.terrace["xy"], 1)
    for hb in C.hubs:
        if not hb.get("in_study"):
            continue
        if not hb.get("square"):
            nm = u"Transit hub" if hb["role"] == "transit" else (u"Gateway out" if hb["id"] == u"K6" else u"Walking hub")
            add("hub_sq", nm, hb["xy"], 9)
        if hb.get("sub_xy"):
            add("subhub", u"Sub-hub in the bed", hb["sub_xy"]["c"], 9)
    return out


def b6_free_spot(p, free, rmax, r):
    """the point nearest p (rings of 4 m, 12 directions) with free ground r m round it, else None"""
    if free(p, r):
        return p
    rr = 4.0
    while rr <= rmax:
        for i in range(12):
            a = i * math.pi / 6.0
            q = (p[0] + rr * math.cos(a), p[1] + rr * math.sin(a))
            if free(q, r):
                return q
        rr += 4.0
    return None


def b6_near(p, pts):
    best = None
    for q in pts:
        d = (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2
        if best is None or d < best[0]:
            best = (d, q)
    return (math.sqrt(best[0]), best[1]) if best else None


def b6_pad(kind, q, wp):
    """the pad's ring (survey m): a rectangle (or an ellipse) with its long side facing the nearest walk point; a
    bird hide is a deck from the walk side into the wetland"""
    L, W = B6_PAD.get(kind) or (12.0, 8.0)
    nb = b6_near(q, wp[::3]) if wp else None
    if nb and nb[0] > 0.5:
        vx, vy = (q[0] - nb[1][0]) / nb[0], (q[1] - nb[1][1]) / nb[0]
    else:
        vx, vy = 0.0, 1.0
    if kind == "hide":                                    # long axis toward the water
        ax, ay, bx, by = vx, vy, -vy, vx
        c = (q[0] + vx * L / 2.0 - vx * 2.0, q[1] + vy * L / 2.0 - vy * 2.0)
    else:
        ax, ay, bx, by = -vy, vx, vx, vy                  # long axis along the walk
        c = q
    if kind in B6_ROUND:
        return [(c[0] + ax * L / 2.0 * math.cos(t) + bx * W / 2.0 * math.sin(t),
                 c[1] + ay * L / 2.0 * math.cos(t) + by * W / 2.0 * math.sin(t))
                for t in [2 * math.pi * i / 28.0 for i in range(28)]]
    return [(c[0] + ax * sx * L / 2.0 + bx * sy * W / 2.0, c[1] + ay * sx * L / 2.0 + by * sy * W / 2.0)
            for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]


def b6_activity_spots(C, free, wp, widen, placed_pads, ins):
    """F11: the liked examples' programme on open ground: candidates every 20 m on free ground; each activity takes
    the candidate farthest from every pad already placed, within its distance band from the walk, its whole pad
    free; bird hides at each widened wetland, where it comes nearest the walk. Returns [(q, kind, name)]."""
    out = []
    taken = [q for q, kd in placed_pads]
    wps = wp[::2]
    widx = {}
    for q in wps:
        widx.setdefault((int(q[0] // 40), int(q[1] // 40)), []).append(q)

    def dwalk(p):
        best = 1e9
        for i in range(-6, 7):
            for j in range(-6, 7):
                for q in widx.get((int(p[0] // 40) + i, int(p[1] // 40) + j), ()):
                    best = min(best, math.hypot(q[0] - p[0], q[1] - p[1]))
        return best
    for R in widen[:4]:                                   # bird hide + deck into each widened wetland
        if not wps:
            break
        e = min(R, key=lambda q: dwalk(q))
        if not ins(e):
            continue
        cx, cy = sum(q[0] for q in R) / len(R), sum(q[1] for q in R) / len(R)
        L = math.hypot(cx - e[0], cy - e[1]) or 1.0
        out.append(((e[0] + (cx - e[0]) / L * 2.0, e[1] + (cy - e[1]) / L * 2.0), "hide", u"Bird hide, deck"))
    cand = []
    for R in C.study or []:
        b = bbox(R)
        y = b[1] + 10.0
        while y < b[3]:
            x = b[0] + 10.0
            while x < b[2]:
                if pip(x, y, R) and free((x, y), 4.0):
                    cand.append(((x, y), dwalk((x, y))))
                x += 20.0
            y += 20.0
    for kind, nm, n, dmin, dmax in B6_ACTIVITIES:
        L, W = B6_PAD[kind]
        r_ = math.hypot(L, W) / 2.0
        for _ in range(n):
            pool = []
            for q, dw_ in cand:
                if not dmin <= dw_ <= dmax:
                    continue
                dmin_t = min([math.hypot(q[0] - t[0], q[1] - t[1]) for t in taken] or [1e9])
                if dmin_t < B6_PAD_SPACING + r_:
                    continue
                pool.append((-dmin_t, q))
            pool.sort()
            hit_ = None
            for _s, q in pool[:60]:
                R = b6_pad(kind, q, wp)
                if free(q, min(W, L) / 2.0) and all(ins(c) and free(c, 0.5) for c in R[::max(1, len(R) // 8)]):
                    hit_ = q
                    break
            if hit_ is None:
                break
            taken.append(hit_)
            out.append((hit_, kind, nm))
    return out


def b6_entrances(study, vis, ins):
    """F10: where a street crosses the zone line: an entrance square (points 80 m apart at least)"""
    out = []
    for x in vis:
        if x["br"] or x["h"] in B3_DROP_IN:
            continue
        P = x["P"]
        flags_ = [ins(q) for q in P]
        if all(flags_) or not any(flags_):
            continue
        for a, b, fa, fb in zip(P[:-1], P[1:], flags_[:-1], flags_[1:]):
            if fa == fb:
                continue
            for R in study:
                for c, d in zip(R, R[1:] + R[:1]):
                    q = b2_seg_x(a, b, c, d)
                    if q and all(math.hypot(q[0] - o[0], q[1] - o[1]) > 80.0 for o in out):
                        out.append(q)
    return out


def b6_edge(study, ins, entr):
    """F10: the zone edge as a threshold: hedge lines B6_HEDGE_IN inside the zone line, open at each entrance;
    edge tree points B6_EDGE_TREE_IN inside every B6_EDGE_TREE_STEP. Returns (hedge polylines, tree points)."""
    hedge, trees = [], []
    for R in study:
        if len(R) < 3:
            continue
        Q = b3_dense(R + R[:1], 3.0)[:-1]
        N = b6_inward(Q)
        cur, acc = [], 0.0
        for i, (q, n) in enumerate(zip(Q, N)):
            near_e = any(math.hypot(q[0] - e[0], q[1] - e[1]) < B6_ENTRY_R + 4.0 for e in entr)
            h = (q[0] + n[0] * B6_HEDGE_IN, q[1] + n[1] * B6_HEDGE_IN)
            if not near_e:
                cur.append(h)
            elif len(cur) >= 2:
                hedge.append(cur)
                cur = []
            if i:
                acc += math.hypot(q[0] - Q[i - 1][0], q[1] - Q[i - 1][1])
            if acc >= B6_EDGE_TREE_STEP and not near_e:
                acc = 0.0
                t = (q[0] + n[0] * B6_EDGE_TREE_IN, q[1] + n[1] * B6_EDGE_TREE_IN)
                if ins(t):
                    trees.append(t)
        if len(cur) >= 2:
            hedge.append(cur)
    return hedge, trees


def b6_clean_offset(P, d):
    """the polyline moved d m to its left with the loops of tight bends cut out (F4: no bike-lane loops)"""
    Q = b3_off(b3_dense(P, 3.0), d)
    out = list(Q)
    i = 0
    while i < len(out) - 3:
        a, b = out[i], out[i + 1]
        cut = None
        for j in range(i + 2, min(len(out) - 1, i + 60)):
            x = b2_seg_x(a, b, out[j], out[j + 1])
            if x:
                cut = (j, x)
        if cut:
            out = out[:i + 1] + [cut[1]] + out[cut[0] + 1:]
        i += 1
    return out


def b6_bike_marks(sub, Pb, T, k):
    """bike lane: a fine white centre dash"""
    sub.line([T(p) for p in Pb], "FFFFFF", 0.05, [0.8, 1.2], cap=0)


def b6_rect_axes(R):
    a, b, d = R[0], R[1], R[3]
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    W = math.hypot(d[0] - a[0], d[1] - a[1]) or 1.0
    return a, ((b[0] - a[0]) / L, (b[1] - a[1]) / L), ((d[0] - a[0]) / W, (d[1] - a[1]) / W), L, W


def b6_pt(a, u, v, s, t):
    return (a[0] + u[0] * s + v[0] * t, a[1] + u[1] * s + v[1] * t)


def b6_draw_pad(sub, kind, R, T, k):
    """F6/F11: each programme pad drawn as what it is (open air), B19 tones"""
    Q = [T(p) for p in R]
    c = (sum(p[0] for p in R) / len(R), sum(p[1] for p in R) / len(R))
    with mpx_grp(sub, "hubs", u"programme: %s" % kind):
        if kind in ("square", "hub_sq"):
            sub.poly([Q], fill=B3_COL["paving"], stroke=B3_COL["paving_edge"], lw=0.1)
            b3_grid_fill(sub, Q, B3_COL["joint"], 3.0 * k * 4.0)
            return
        if kind == "freed":
            sub.poly([[T(q) for q in b3_band(R + R[:1], [6.5] * (len(R) + 1))]], fill=B3_COL["paving_edge"])
            sub.poly([[T(q) for q in b3_band(R + R[:1], [6.0] * (len(R) + 1))]], fill=B3_COL["paving"])
            sub.poly([Q], fill=B3_COL["paving"])
            b3_grid_fill(sub, Q, B3_COL["joint"], 3.0 * k * 4.0)
            return
        if kind in B6_ROUND:
            col = dict(play=B3_COL["sand"], event=B3_COL["lawn"], picnic=B3_COL["lawn"], meadow=B3_COL["meadow"])[kind]
            sub.poly([Q], fill=col, stroke=B3_COL["paving_edge"] if kind == "play" else B3_COL["tree_edge"], lw=0.12,
                     dash=None if kind == "play" else [0.6, 0.4])
            if kind == "play":
                b3_dots(sub, bbox(Q), 0.9, B3_COL["paving_edge"], [Q])
                for f in ((-0.2, 0.1, 0.18), (0.22, -0.1, 0.14)):
                    p = (Q[0][0] + (Q[14][0] - Q[0][0]) * (0.5 + f[0]), Q[0][1] + (Q[14][1] - Q[0][1]) * (0.5 + f[0]))
                    sub.poly([b3_circle((p[0], p[1] + f[1] * 4.0), f[2] * 10.0 * k * 4.0 / 4.0, 14)],
                             fill=B3_COL["lawn_dk"], stroke=B3_COL["tree_edge"], lw=0.06)
            elif kind == "event":
                a, b = R[0], R[14]
                st_ = (a[0] + (b[0] - a[0]) * 0.12, a[1] + (b[1] - a[1]) * 0.12)
                sub.poly([b3_circle(T(st_), 3.5 * k, 16)], fill=B3_COL["deck"], stroke=B3_COL["deck_edge"], lw=0.08)
            elif kind == "picnic":
                rnd = random.Random(int(c[0] + c[1]))
                for _ in range(7):
                    f, g = rnd.uniform(-0.3, 0.3), rnd.uniform(-0.25, 0.25)
                    p = T((c[0] + (R[0][0] - c[0]) * f + (R[7][0] - c[0]) * g, c[1] + (R[0][1] - c[1]) * f +
                           (R[7][1] - c[1]) * g))
                    sub.poly([rect(p[0] - 0.9 * k, p[1] - 0.4 * k, p[0] + 0.9 * k, p[1] + 0.4 * k)], fill=B3_COL["wood_t"])
            else:                                         # meadow: flowers + two mown paths across
                b3_dots(sub, bbox(Q), 0.8, B3_COL["culture"], [Q])
                for i, j in ((0, 14), (7, 21)):
                    sub.line([Q[i], Q[j]], B3_COL["lawn"], 2.2 * k)
            return
        a, u, v, L, W = b6_rect_axes(R)
        P_ = lambda s, t: T(b6_pt(a, u, v, s, t))
        if kind == "court":
            sub.poly([Q], fill=B3_COL["court"], stroke=B3_COL["paving_edge"], lw=0.1)
            inn = [P_(1.5, 1.5), P_(L - 1.5, 1.5), P_(L - 1.5, W - 1.5), P_(1.5, W - 1.5)]
            sub.line(inn + inn[:1], "FFFFFF", 0.08)
            sub.line([P_(L / 2.0, 1.5), P_(L / 2.0, W - 1.5)], "FFFFFF", 0.08)
            sub.poly([b3_circle(P_(L / 2.0, W / 2.0), 1.8 * k, 16)], fill=None, stroke="FFFFFF", lw=0.08)
        elif kind == "fitness":
            sub.poly([Q], fill=B3_COL["rubber"], stroke=B3_COL["paving_edge"], lw=0.1)
            for s in (2.5, 5.5, 8.5, 11.5):
                for t in (2.5, W - 2.5):
                    sub.poly([b3_circle(P_(s, t), 0.6 * k, 10)], fill=B3_COL["deck_edge"])
        elif kind == "cafe":
            sub.poly([Q], fill=B3_COL["paving"], stroke=B3_COL["paving_edge"], lw=0.1)
            s = 2.0
            while s < L - 1.0:
                t = 2.0
                while t < W - 1.0:
                    sub.poly([b3_circle(P_(s, t), 0.7 * k, 10)], fill=B3_COL["deck"], stroke=B3_COL["deck_edge"],
                             lw=0.05)
                    t += 3.0
                s += 3.0
        elif kind == "classroom":
            sub.poly([Q], fill=B3_COL["deck"], stroke=B3_COL["deck_edge"], lw=0.1)
            t = 2.0
            while t < W - 2.5:
                sub.line([P_(2.0, t), P_(L - 4.0, t)], B3_COL["wood_t"], 0.25)
                t += 1.8
            sub.line([P_(L - 2.0, 1.5), P_(L - 2.0, W - 1.5)], B3_COL["deck_edge"], 0.2)
        elif kind == "seats":
            sub.poly([Q], fill=B3_COL["paving"], stroke=B3_COL["paving_edge"], lw=0.08)
            s = 1.0
            while s < L - 1.0:
                sub.line([P_(s, W / 2.0), P_(min(s + 2.5, L - 1.0), W / 2.0)], B3_COL["wood_t"], 0.3)
                s += 3.5
        elif kind in ("arch", "view", "subhub", "hide"):
            sub.poly([Q], fill=B3_COL["deck"], stroke=B3_COL["deck_edge"], lw=0.12)
            s = 2.0
            while s < L:
                sub.line([P_(s, 0.0), P_(s, W)], B3_COL["joint"], 0.05)
                s += 2.0
            if kind == "arch":
                sub.line([P_(0.0, W / 2.0), P_(L, W / 2.0)], B3_COL["heritage"], 0.3, [0.8, 0.5], cap=0)
            elif kind == "view":
                sub.line([P_(0.0, W), P_(L, W)], B3_COL["deck_edge"], 0.25)
            elif kind == "hide":
                sub.poly([[P_(L - 3.0, -0.6), P_(L, -0.6), P_(L, W + 0.6), P_(L - 3.0, W + 0.6)]], fill=B3_COL["wood_t"],
                         stroke=B3_COL["deck_edge"], lw=0.08)
        elif kind == "allot":
            sub.poly([Q], fill=B3_COL["garden"], stroke=B3_COL["paving_edge"], lw=0.1)
            t = 2.0
            while t < W - 1.0:
                if abs(t - W / 2.0) > 1.2:
                    sub.line([P_(1.5, t), P_(L - 1.5, t)], B3_COL["garden_row"], 0.12)
                t += 1.6
            sub.poly([[P_(0.0, W / 2.0 - 0.8), P_(L, W / 2.0 - 0.8), P_(L, W / 2.0 + 0.8), P_(0.0, W / 2.0 + 0.8)]],
                     fill=B3_COL["gravel"])
        else:
            sub.poly([Q], fill=B3_COL["paving"], stroke=B3_COL["paving_edge"], lw=0.1)


def b6_planting(C, chan, widen, walks, free, hedge, edge_trees, sv, ins):
    """F9 (Aras 00:25: diverse, placed with meaning): [(p, species, crown m or None, function)] in priority order:
    survey trees kept, hub shade, riparian belt (willow / tamarisk on the wet bank), emergent clusters (rush,
    loosestrife) only in the widened wetlands and the side arms, walk allée (plane / ash on the land side), olive /
    stone pine rows on the rain terraces, rosemary / lavender beds on the dry tops, edge tree row (stone pine),
    ash / plane groups in the lawns. Reed and mint are never used (lined cells only, plant module rule)."""
    rnd = random.Random(6)
    out = [(P[0], "plane", 7.0, u"existing tree") for P in sv.get("tree", []) if P and ins(P[0])]
    out += [(p, "plane", PLA_SPECIES["plane"]["crown_m"] * 0.8, u"square shade") for p, i in pl23_hub_trees(C)]
    dgd = pl23_dg(C)
    out += [((xs, ys), key, None, u"garden shade") for key, xs, ys in ((dgd or {}).get("shade_trees") or [])
            if key in PLA_SPECIES]
    for R in chan:                                        # riparian belt
        s_ = arclen(R + R[:1])
        Q = [at_len(R + R[:1], s_, t)[0] for t in [11.0 * i for i in range(int(s_[-1] // 11.0))]]
        N = b6_inward(Q)
        for i, (q, n) in enumerate(zip(Q, N)):
            d = 5.5 + rnd.uniform(-1.0, 1.5)
            p = (q[0] - n[0] * d, q[1] - n[1] * d)        # outward = off the water
            if ins(p):
                out.append((p, ("willow", "tamarisk", "willow")[i % 3], None, u"riparian belt"))
    for R in widen:                                       # emergent clusters in the wetland
        b = bbox(R)
        for _ in range(int((b[2] - b[0]) * (b[3] - b[1]) / 140.0) + 3):
            c = (rnd.uniform(b[0], b[2]), rnd.uniform(b[1], b[3]))
            if not (pip(c[0], c[1], R) and ins(c)):
                continue
            key = B3_EMERGENT[rnd.randrange(len(B3_EMERGENT))]
            for j in range(rnd.randint(3, 6)):
                p = (c[0] + rnd.uniform(-3.0, 3.0), c[1] + rnd.uniform(-3.0, 3.0))
                if pip(p[0], p[1], R):
                    out.append((p, key, 2.4, u"wetland emergent"))
    for a_ in C.arms:
        P = a_.get("P") or []
        if len(P) >= 2:
            for sg in (1.0, -1.0):
                for i, q in enumerate(b3_dense(b3_off(P, sg * (B3_ARM_W / 2.0 + 1.0)), 4.0)):
                    if ins(q) and i % 4 != 3:
                        out.append((q, B3_EMERGENT[(i // 4) % len(B3_EMERGENT)], 2.2, u"wetland emergent"))
    for P, bank in walks:                                 # allée on the land side of the bike lane
        sg = 1.0 if bank == "NE" else -1.0
        Pa = b6_clean_offset(P, sg * (B3_WALK_W / 2.0 + 0.3 + B3_BIKE_W + 3.2))
        s = arclen(Pa)
        t = 5.0
        while t < s[-1]:
            p, _u = at_len(Pa, s, t)
            out.append((p, "plane" if int(t // 140.0) % 2 == 0 else "ash", None, u"walk allée"))
            t += 11.0
    for P in C.terr:                                      # olives on the rain terraces
        for i, q in enumerate(b3_dense(P, 9.0)[1:-1]):
            out.append((q, "stone_pine" if i % 4 == 3 else "olive", None, u"terrace olives"))
    for z in C.D.zones:                                   # rosemary / lavender beds on the dry tops
        if z["code"] in ("WS", "GR") and len(z["P"]) >= 3:
            b = bbox(z["P"])
            y = b[1] + 3.0
            while y < b[3]:
                x = b[0] + 3.0 + (3.0 if int(y // 6) % 2 else 0.0)
                while x < b[2]:
                    if pip(x, y, z["P"]) and int(x // 18 + y // 18) % 3 != 0:
                        out.append(((x, y), ("rosemary", "lavender")[int(x // 18) % 2], 2.0, u"dry-top beds"))
                    x += 6.0
                y += 6.0
    out += [(p, "stone_pine", None, u"edge tree row") for p in edge_trees]
    for R in C.study or []:                               # tree groups in the open lawns
        b = bbox(R)
        y = b[1] + 25.0
        while y < b[3]:
            x = b[0] + 25.0
            while x < b[2]:
                c = (x + rnd.uniform(-12, 12), y + rnd.uniform(-12, 12))
                if pip(c[0], c[1], R) and free(c, 10.0):
                    key = "ash" if rnd.random() < 0.5 else "plane"
                    for j in range(rnd.randint(3, 5)):
                        a = rnd.uniform(0, 2 * math.pi)
                        out.append(((c[0] + 6.0 * math.cos(a), c[1] + 6.0 * math.sin(a)), key, None, u"lawn group"))
                x += 55.0
            y += 55.0
    return out


def b6_pbox(Q):
    return bbox(Q)


def b6_heritage_name(p):
    """the place name of a kept heritage building (PLACES, within 60 m), else its tag"""
    best = None
    for nm, q in PLACES:
        d = math.hypot(q[0] - p[0], q[1] - p[1])
        if d < 60.0 and (best is None or d < best[0]):
            best = (d, nm)
    return b3_title(best[1]) if best else u"heritage, kept"


def b6_dg(sub, C, T, add_hard):
    """F12: Demeter's Garden as allotment rows in garden green, gravel paths, paved gathering places"""
    dgd = pl23_dg(C)
    if not dgd:
        return 0
    with mpx_grp(sub, "fields", u"Demeter's Garden"):
        for R in dgd.get("rings") or []:
            sub.poly([[T(p) for p in R]], fill=B3_COL["garden"], stroke=B3_COL["paving_edge"], lw=0.08)
        for P in dgd.get("rows") or []:
            sub.line([T(p) for p in P], B3_COL["garden_row"], 0.14)
        for P in (dgd.get("paths") or []) + (dgd.get("edge") or []):
            if len(P) >= 2:
                sub.poly([[T(q) for q in b3_band(P, [1.8] * len(P))]], fill=B3_COL["gravel"])
                add_hard(P, 0.9 + B3_TREE_CLEAR)
        for R in (dgd.get("gather") or []) + (dgd.get("cafe") or []):
            sub.poly([[T(p) for p in R]], fill=B3_COL["paving"], stroke=B3_COL["paving_edge"], lw=0.08)
            add_hard(R + R[:1], 1.0)
    return 1


B3_COL.update(bed="C9D0C2", ctx_road="ECECE8", sand="EDE3CC", court="C9B3A3", rubber="C7A69B", wood_t="A88E6E",
              garden="B9C49C", garden_row="8C9A72")       # v6 F12: no yellow patches (garden green, bed grey-green)
B6_LEGEND = ((u"Riverside walk", B3_COL["paving"]), (u"Bike lane", B3_COL["bike"]),
             (u"Bed walk, shut in floods", B3_COL["gravel"]), (u"Car road + pavements", B3_COL["asphalt"]),
             (u"Decks, footbridges", B3_COL["deck"]), (u"Selinos", B3_COL["water"]),
             (u"Widened stream, wetland", B3_COL["water_lt"]), (u"Reed basins", B3_COL["reed"]),
             (u"Stepped dry tops, rain terraces", B3_COL["lawn_dk"]), (u"Allotments, Demeter's Garden", B3_COL["garden"]),
             (u"Courts", B3_COL["court"]), (u"Fitness", B3_COL["rubber"]), (u"Play sand", B3_COL["sand"]),
             (u"Lawns: events, picnics", B3_COL["lawn"]), (u"Pollinator meadow", B3_COL["meadow"]),
             (u"Riparian belt: willow, tamarisk", B3_TREE_TONE["willow"]), (u"Walk allée, lawn groups: plane, ash",
                                                                          B3_TREE_TONE["plane"]),
             (u"Edge hedge + stone pine row", B3_COL["tree2"]), (u"Heritage, kept (numbered trail)", B3_COL["heritage"]),
             (u"Ground +2 m steps above the bed", b3_mix(B3_COL["meadow"], B3_COL["contour_dk"], 0.3)))


def build_all(doc, warn):
    """Read the open file, compute the proposal (masterplan code, option A), draw and write the B19 sheet.
    Returns (folder, files, log lines, pages, scale) as main() expects."""
    folder = out_folder(doc)
    os.makedirs(folder, exist_ok=True)
    wn_reset()
    mpx_start()
    del MPX_PAGES[:]
    scale = inp_num("scale", B19_SCALE, warn)
    _SCALE[0] = scale
    if doc is not None:
        load_palette([DATA_DIR] + search_dirs(doc), warn)
    areas = read_areas(doc) if doc is not None else {}
    if len(areas) < 2:
        areas = calisma_from([ring(list(P)) for P in CALISMA_COPY])
        warn.append(u"no calisma_alan outlines in the open file: the built-in copy (Bergama_Altlik.3dm, 25 Oct) "
                    u"was used")
    site, site_found = read_site(doc)
    if not site_found:
        warn.append(u"no site_alan outline in the open file: the built-in copy (Bergama_Altlik.3dm, 25 Oct) was used")
    V = View(areas, 0.0, 1000.0 / scale, frame=site)
    V.frame_P, V.study = list(site), [areas[k_] for k_ in sorted(areas)]
    bb = [bbox(A) for A in areas.values()] + [V.bb]
    R = (min(b[0] for b in bb) - RING_M - 5, min(b[1] for b in bb) - RING_M - 5,
         max(b[2] for b in bb) + RING_M + 5, max(b[3] for b in bb) + RING_M + 5)
    survey = read_survey(doc, R) if doc is not None else {}
    its = read_items(doc, "A") if doc is not None else []
    if not its:
        zb = zone_base_file(doc, warn)
        its = [i for i in zb[1] if i["layer"].startswith("Option_A::")]
        src = zb[0]
        if not its:
            its = [i for i in embedded_items() if i["layer"].startswith("Option_A::")]
            src = u"the copy of zone base v5 embedded in this script"
        warn.append(u"no Option_A::INT_ zones in the open file; {} was used".format(src))
    D = Design(its, areas, warn, "A")
    CL = city_layer("A", D, areas, survey, warn)
    spots = read_spots(doc, [V.bb]) if doc is not None else []
    t0 = time.time()
    C = Corridor(V, survey, CL, D, spots, warn)
    lines = [u"proposal computed (masterplan code, option A): zones {}, hubs {}, {:.1f} s".format(
        len(D.zones), len(C.hubs), time.time() - t0)]
    C.survey = survey
    globals()["_B19_LAST"] = dict(C=C, CL=CL, D=D, site=site, survey=survey, study=C.study or V.study)
    pg, notes = b19_page(C, site, C.study or V.study, scale, warn)
    lines += notes
    path = save(pg, folder, B19_NAME, u"MIRAQUA masterplan, B19 drawing language")
    lines.append(u"{}  {}".format(os.path.basename(path), datetime.datetime.now().strftime("%H:%M:%S")))
    return folder, [path], lines, [("A", 1, pg)], scale


if Rhino is not None:
    try:
        _txt, _files = main()
    except Exception as _ex:
        _txt, _files = u"ERROR: {}: {} ({})".format(type(_ex).__name__, _ex, VERSION), []
        gh_status(SHORT + " · ERROR")
        mem_set("ver", VERSION)
        mem_set("last", _txt)
        mem_set("status", SHORT + " · ERROR")
    log = _txt
    print(_txt)
    pdf = _files
