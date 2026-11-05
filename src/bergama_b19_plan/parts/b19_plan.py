

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
VERSION = "bergama_b19_plan v4 (2026-11-05)"  # v4 (Aras 22:55): the project's own walks, bike lane, roads by change, bridges with joined ends, terraces, basins, arms, garden, programme marks; OSM tracks and invented promenades/connectors gone; bike strips only beside the walk; every building whole in or out; trees off buildings and each other; v3 (Aras 22:19 "get better"): rebuilt from survey + OSM + stations: streets at survey widths with bike strips, promenades on both banks with varying width, curved connectors, footbridges with landings, ground by distance from water (wood, lawn, meadow), one continuous stream, trees by function off paving and water, names inside the zone; v2 rejected 22:18, v1 rejected 21:26
SHORT = "v4"
GH_LABEL = "B19Plan"
SETTINGS = ("rhino_bake", "scale")
OUT_FOLDER = "bergama_b19_plan"
LOG_NAME = "bergama_b19_plan_log.txt"
BAKE_ROOT = "B19"
B19_SCALE = 4000.0           # default print scale (design spec, 5 Nov 21:0x; input `scale` overrides)
B19_NAME = "Bergama_B19_plan_v4.pdf"
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
              garden="D9CFA8", garden_row="A69A70", contour_dk="7D8A72", prog="D9A08F",
              culture="E4877A", food="D9A55C", edu="8FA6B8", hub="9C6D70")
# v4 (Aras 22:55): the project's own elements, widths are design values (m)
B3_DROP_IN = ("track", "path", "footway", "service", "cycleway", "bridleway", "steps", "unclassified")  # not drawn in the zone
B3_WALK_W = 4.0              # riverside walk paving
B3_BED_W = 2.5               # bed walk (gravel, shut in floods)
B3_CANOPY_W = 3.5            # canopied walkway (deck)
B3_TERR_W = 3.0              # rain terrace band on its contour
B3_ARM_W = 4.0               # planted side arm, open water
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
    """v3 sheet (see the note above b3_*). Returns (Page, log notes)."""
    t0 = time.time()
    k = 1000.0 / scale
    x0, y0, x1, y1 = bbox(site)
    dw, dh = (x1 - x0) * k, (y1 - y0) * k
    T = lambda p: ((p[0] - x0) * k, (p[1] - y0) * k)
    TL = lambda P: [T(p) for p in P]
    ins = lambda p: any(pip(p[0], p[1], R) for R in study)
    sub = Page(dw, dh)
    st = [TL(R) for R in study if len(R) >= 3]
    notes, flags = [], []
    sv = C.survey if hasattr(C, "survey") else {}
    box = (x0 - 60.0, y0 - 60.0, x1 + 60.0, y1 + 60.0)
    # ---- data
    water = [(R, Hs) for R, Hs in pl23_water_groups(C, warn)]
    w_idx = b3_grid(b3_segs([R for R, Hs in water], True))
    in_water = lambda p: any(pip(p[0], p[1], R) and not any(pip(p[0], p[1], H) for H in Hs) for R, Hs in water)
    raw = [R for role in ("building", "housing", "heritage") for R in C.bld.get(role, []) if len(R) >= 3]
    sheds = [b3_hull(R) for R in C.bld.get("shed", []) if len(R) >= 3]   # v4: survey X lines inside a shed gone
    blds = b2_union(raw, warn)
    b_idx = b3_grid(b3_segs(blds, True))
    in_bld = lambda p: any(pip(p[0], p[1], R) for R in b3_near_rings(blds_box, p))
    blds_box = [(bbox(R), R) for R in blds]
    rem = [z["P"] for z in C.D.removes if len(z.get("P") or []) >= 3]
    gone = lambda R: any(pip(inner_pt(R)[0], inner_pt(R)[1], Z) for Z in rem)
    her = [R for R in C.bld.get("heritage", []) if len(R) >= 3]
    is_her = lambda R: any(pip(inner_pt(H)[0], inner_pt(H)[1], R) for H in her)
    b_in = [R for R in blds if ins(inner_pt(R)) and not gone(R)]
    b_rm = [R for R in blds if ins(inner_pt(R)) and gone(R)]
    b_out = [R for R in blds if not ins(inner_pt(R))]
    edges = [P for role in ("road", "kerb") for P in sv.get(role, []) if hit(bbox(P), box)]
    e_idx = b3_grid(b3_segs(edges), 15.0)
    ways = b3_snap(b3_osm(box, warn), e_idx)
    cl = pl23_prep(C)
    road_names, el_names, n_el = [], [], {}
    # hard surfaces for the tree test: (band ring bbox, ring)
    hard = []
    # ---- 1 zone ground: lawn over the whole zone (soft), contours (shaded, topographic depth)
    sub.clip(st)
    with mpx_grp(sub, "ground", u"open meadow (beyond 62 m from the water: pollinators, flood storage)"):
        sub.poly([rect(0.0, 0.0, dw, dh)], fill=B3_COL["meadow"])
        b3_dots(sub, (0.0, 0.0, dw, dh), 7.0 * k, B3_COL["lawn_dk"], st)
    eco = dict(C.eco)
    for t_, col, nm in ((62.0, "lawn", u"lawn with tree groups (32-62 m: shade, play)"),
                        (32.0, "wood", u"riparian woodland floor (6-32 m: bank, shade, habitat)")):
        with mpx_grp(sub, "ground", nm):
            for R in eco.get(t_, []):
                if len(R) >= 3:
                    sub.poly([TL(R)], fill=B3_COL[col])
    with mpx_grp(sub, "ground", u"contours"):
        for P in (C.contours or []):
            if hit(bbox(P), box):
                sub.line(TL(P), B3_COL["contour"], 0.06)
    # ---- 2 masterplan zone surfaces (soft unless water)
    ZS = dict(WT=("reed", u"reed basins"), WP=("meadow", u"floodable planting"), WA=("gravel", u"stream bed"),
              WS=("lawn_dk", u"dry-top terraces"), GR=("lawn_dk", u"raised dry top"), DG=("garden", u"garden"),
              WD=("water_lt", u"spillway"))
    for z in C.D.zones:
        sty = ZS.get(z["code"])
        if not sty or len(z["P"]) < 3:
            continue
        with mpx_grp(sub, "fields", u"%s %s" % (z["code"], z.get("id", u""))):
            sub.poly([TL(z["P"])], fill=B3_COL[sty[0]], stroke=B3_COL["paving_edge"], lw=0.05)
            if z["code"] == "WT":
                b3_ticks_fill(sub, TL(z["P"]), B3_COL["tree_edge"], 1.2)
            if z["code"] == "DG":
                b3_rows_fill(sub, TL(z["P"]), B3_COL["garden_row"], 4.0 * k)
    sub.unclip()
    # ---- 4 water
    chan = b3_channel(C)
    with mpx_grp(sub, "water", u"Selinos"):
        for run in chan:
            sub.poly([TL(run)], fill=B3_COL["water"])
        for R, Hs in water:
            sub.poly([TL(R)] + [TL(H) for H in Hs if len(H) >= 3], fill=B3_COL["water"], stroke=B3_COL["kerb"],
                     lw=0.12)
        b3_ripples(sub, C, T, k)
    # ---- 5 streets (v4): city streets only; inside the zone no track / path / footway / service way (the
    # project's own walks replace them, Aras 22:55 "no purpose roads"); no bike strips or kerbs on streets (the bike
    # lane is the project's, beside the riverside walk); nothing over the water except bridges
    PROJ_RD = [(rd, ch) for rd, ch, runs in cl["roads"]]

    def rd_change(P):
        best = None
        for rd, ch in PROJ_RD:
            xy = rd["xy"]
            n_ = sum(1 for q in P if min(seg_dist(q[0], q[1], a_, b_) for a_, b_ in zip(xy[:-1], xy[1:])) < 14.0)
            if n_ >= max(2, len(P) * 0.6) and (best is None or n_ > best[0]):
                best = (n_, rd, ch)
        return best
    vis = []
    for x in ways:
        h, br, nm, P, w, sn = x
        if not hit(bbox(P), box):
            continue
        if h in B3_DROP_IN and any(ins(q) for q in P):
            continue
        if br or not any(pip(q[0], q[1], R) for q in P for R in chan):
            vis.append(x)
            continue
        piece = []
        for q in b3_dense(P, 4.0) + [None]:
            if q is not None and not any(pip(q[0], q[1], R) for R in chan):
                piece.append(q)
                continue
            if len(piece) >= 2:
                vis.append((h, br, nm, piece, w, sn))
            piece = []
    n_rd = {}
    for h, br, nm, P, w, sn in vis:
        if br:
            continue
        inz = sum(1 for q in P if ins(q)) >= len(P) / 2.0
        ch = rd_change(P) if inz else None
        chg = ch[2] if ch else None
        if chg in ("pedestrian", "shared"):
            col = B3_COL["paving"]
        elif h in B3_VEHICLE:
            col = B3_COL["asphalt"]
        else:
            col = B3_COL["paving"]
        with mpx_grp(sub, "roads", u"%s %s%s" % (h, nm, (u" · " + chg) if chg else u"")):
            sub.poly([TL(b3_band(P, [w] * len(P)))], fill=col, stroke=B3_COL["paving_edge"] if inz else None,
                     lw=0.05)
            Q = TL(P)
            if inz and chg == "calmed":
                b2_joints(sub, Q, [w * k] * len(Q), 6.0 * k, B3_COL["paving_edge"])
            if inz and chg in ("pedestrian", "shared"):
                b2_joints(sub, Q, [w * k] * len(Q), 3.0 * k, B3_COL["joint"])
            if inz and h in B3_VEHICLE and chg not in ("pedestrian", "shared", "calmed") and w >= 7.0:
                sub.line(Q, "FFFFFF", 0.1, [1.2, 1.2], cap=0)
        if chg:
            n_rd[chg] = n_rd.get(chg, 0) + 1
        if chg and chg != "kept":
            road_names.append((ch[1]["name"], chg, P[len(P) // 2]))
        hard.append((bbox(P), P, w / 2.0 + B3_TREE_CLEAR))
    with mpx_grp(sub, "roads", u"road bridges"):
        for h, br, nm, P, w, sn in vis:
            if br:
                sub.poly([TL(b3_band(P, [w + 1.2] * len(P)))], fill=B3_COL["deck_edge"])
                sub.poly([TL(b3_band(P, [w] * len(P)))], fill=B3_COL["deck"])
                hard.append((bbox(P), P, w / 2.0 + B3_TREE_CLEAR))
    # ---- 6 the project's ground works: rain terraces, hub squares, programme round the hubs, Demeter's Garden
    with mpx_grp(sub, "hubs", u"programme at the hubs (outer ring)"):
        if C.rings:
            r_, Ls = max(C.rings, key=lambda x: x[0])
            for L_ in Ls:
                if len(L_) >= 3:
                    Q = TL(L_)
                    sub.line(Q + Q[:1], B3_COL["prog"], 0.25, [1.0, 0.7], cap=0)
            n_el["programme ring"] = len(Ls)
    for i, P in enumerate(C.terr):
        if len(P) < 2 or not any(ins(q) for q in P):
            continue
        with mpx_grp(sub, "fields", u"rain terrace %d" % (i + 1)):
            sub.poly([TL(b3_band(P, [B3_TERR_W] * len(P)))], fill=B3_COL["lawn_dk"])
            sub.line(b3_off(TL(P), -B3_TERR_W * k / 2.0), B3_COL["contour_dk"], 0.12)
            b3_ticks_line(sub, b3_off(TL(P), -B3_TERR_W * k / 2.0), B3_COL["contour_dk"], 0.07, 1.2 * k * 4.0,
                          B3_TERR_W * k * 0.8)
        n_el["terrace"] = n_el.get("terrace", 0) + 1
    for hb in C.hubs:
        for R in hb.get("square") or []:
            if len(R) >= 3:
                with mpx_grp(sub, "hubs", u"hub square %s" % hb["id"]):
                    sub.poly([TL(R)], fill=B3_COL["paving"], stroke=B3_COL["paving_edge"], lw=0.1)
                    b3_grid_fill(sub, TL(R), B3_COL["joint"], 3.0 * k * 4.0)
                hard.append((bbox(R), R + R[:1], 1.0))
    dgd = pl23_dg(C)
    if dgd:
        with mpx_grp(sub, "fields", u"Demeter's Garden"):
            for R in dgd.get("rings") or []:
                sub.poly([TL(R)], fill=B3_COL["garden"], stroke=B3_COL["paving_edge"], lw=0.08)
            for P in dgd.get("rows") or []:
                sub.line(TL(P), B3_COL["garden_row"], 0.18)
            for R in (dgd.get("gather") or []) + (dgd.get("cafe") or []):
                sub.poly([TL(R)], fill=B3_COL["paving"], stroke=B3_COL["paving_edge"], lw=0.08)
                hard.append((bbox(R), R + R[:1], 1.0))
            for P in (dgd.get("paths") or []) + (dgd.get("edge") or []):
                if len(P) >= 2:
                    sub.poly([TL(b3_band(P, [1.8] * len(P)))], fill=B3_COL["gravel"])
                    hard.append((bbox(P), P, 0.9 + B3_TREE_CLEAR))
    # ---- 7 the project's water works: widened stream, side arms, hidden stream line
    for i, w_ in enumerate(C.widen):
        R = w_.get("ring") or []
        if len(R) >= 3:
            with mpx_grp(sub, "water", u"widened stream, wetland %d" % (i + 1)):
                sub.poly([TL(R)], fill=B3_COL["water_lt"], stroke=B3_COL["water"], lw=0.15)
                b3_ticks_fill(sub, TL(R), B3_COL["reed"], 1.2)
            n_el["widen"] = n_el.get("widen", 0) + 1
    for i, a_ in enumerate(C.arms):
        P = a_.get("P") or []
        if len(P) >= 2:
            with mpx_grp(sub, "water", u"planted side arm %d" % (i + 1)):
                sub.poly([TL(b3_band(P, [B3_ARM_W + 3.0] * len(P)))], fill=B3_COL["reed"])
                sub.poly([TL(b3_band(P, [B3_ARM_W] * len(P)))], fill=B3_COL["water"])
            hard.append((bbox(P), P, B3_ARM_W / 2.0 + 1.5))
            n_el["arm"] = n_el.get("arm", 0) + 1
    with mpx_grp(sub, "water", u"hidden stream line"):
        for P in cl["cov"]:
            if len(P) >= 2:
                sub.line(TL(P), B3_COL["water"], 0.35, [1.6, 0.9], cap=0)
                n_el["hidden"] = n_el.get("hidden", 0) + 1
    # ---- 8 the project's movement: riverside walk + its bike lane, bed walk, canopied walkway, footbridges,
    # stepping stones, sightline. Each footbridge end is joined to the nearest walk on its bank (FLAG if none).
    walk_pts = []
    for P, bed, bank in cl["walk"]:
        if len(P) < 2:
            continue
        P = b3_chaikin_open(b3_dense(P, 6.0), 1)
        if bed:
            with mpx_grp(sub, "paths", u"bed walk, shut in floods"):
                sub.poly([TL(b3_band(P, [B3_BED_W + 0.4] * len(P)))], fill=B3_COL["paving_edge"])
                sub.poly([TL(b3_band(P, [B3_BED_W] * len(P)))], fill=B3_COL["gravel"])
            hard.append((bbox(P), P, B3_BED_W / 2.0 + B3_TREE_CLEAR))
            n_el["bed"] = n_el.get("bed", 0) + 1
        else:
            sg = 1.0 if bank == "NE" else -1.0
            off = sg * (B3_WALK_W / 2.0 + 0.3 + B3_BIKE_W / 2.0)
            Pb = b3_off(P, off)
            with mpx_grp(sub, "paths", u"riverside walk %s" % bank):
                sub.poly([TL(b3_band(P, [B3_WALK_W + 0.5] * len(P)))], fill=B3_COL["paving_edge"])
                sub.poly([TL(b3_band(P, [B3_WALK_W] * len(P)))], fill=B3_COL["paving"])
                b2_joints(sub, TL(P), [B3_WALK_W * k] * len(P), 2.5 * k, B3_COL["joint"])
            with mpx_grp(sub, "paths", u"bike lane beside the walk %s" % bank):
                sub.poly([TL(b3_band(Pb, [B3_BIKE_W] * len(Pb)))], fill=B3_COL["bike"])
            hard.append((bbox(P), P, B3_WALK_W / 2.0 + B3_BIKE_W + B3_TREE_CLEAR))
            n_el["walk"] = n_el.get("walk", 0) + 1
        walk_pts += P
        el_names.append((u"Bed walk, shut in floods" if bed else u"Riverside walk + bike lane", P[len(P) // 2]))
    for P in C.canopy:
        if len(P) >= 2:
            with mpx_grp(sub, "paths", u"canopied walkway"):
                sub.poly([TL(b3_band(P, [B3_CANOPY_W] * len(P)))], fill=B3_COL["paving"])
                for sg in (1.0, -1.0):
                    sub.line(b3_off(TL(P), sg * B3_CANOPY_W * k / 2.0), B3_COL["paving_edge"], 0.08, [0.5, 0.5], cap=0)
            hard.append((bbox(P), P, B3_CANOPY_W / 2.0 + B3_TREE_CLEAR))
            walk_pts += P
            el_names.append((u"Canopied walkway", P[len(P) // 2]))
    w_idx = {}
    for q in walk_pts:
        w_idx.setdefault((int(q[0] // 20), int(q[1] // 20)), []).append(q)

    def near_walk(p, r):
        best = None
        for i in range(int((p[0] - r) // 20), int((p[0] + r) // 20) + 1):
            for j in range(int((p[1] - r) // 20), int((p[1] + r) // 20) + 1):
                for q in w_idx.get((i, j), ()):
                    d = math.hypot(q[0] - p[0], q[1] - p[1])
                    if d <= r and (best is None or d < best[0]):
                        best = (d, q)
        return best
    n_end = 0
    for c_ in C.cross:
        if not c_.get("P"):
            continue
        a_, b_ = c_["P"][0], c_["P"][1]
        if not (ins(a_) or ins(b_)):
            continue
        nm_ = c_.get("name") or c_["kind"]
        for e in (a_, b_):
            nw = near_walk(e, B3_END_MAX)
            if nw is None:
                flags.append(u"FLAG %s: an end meets no walk within %.0f m" % (nm_, B3_END_MAX))
                continue
            if nw[0] > 1.0:
                with mpx_grp(sub, "paths", u"%s end path" % nm_):
                    sub.poly([TL(b3_band([e, nw[1]], [B3_FOOT_W + 0.4] * 2))], fill=B3_COL["paving_edge"])
                    sub.poly([TL(b3_band([e, nw[1]], [B3_FOOT_W] * 2))], fill=B3_COL["paving"])
                hard.append((bbox([e, nw[1]]), [e, nw[1]], B3_FOOT_W / 2.0 + B3_TREE_CLEAR))
            n_end += 1
        if c_["kind"] == "footbridge":
            with mpx_grp(sub, "paths", u"new footbridge %s" % nm_):
                sub.poly([TL(b3_band([a_, b_], [B3_FOOT_W + 0.8] * 2))], fill=B3_COL["deck_edge"])
                sub.poly([TL(b3_band([a_, b_], [B3_FOOT_W] * 2))], fill=B3_COL["deck"])
            el_names.append((u"New footbridge", ((a_[0] + b_[0]) / 2.0, (a_[1] + b_[1]) / 2.0)))
        elif c_["kind"] == "stepping stones":
            with mpx_grp(sub, "paths", u"stepping stones %s" % nm_):
                L_ = math.hypot(b_[0] - a_[0], b_[1] - a_[1])
                n_s = max(3, int(L_ / 2.2))
                for i in range(n_s):
                    f = (i + 0.5) / n_s
                    q = (a_[0] + (b_[0] - a_[0]) * f, a_[1] + (b_[1] - a_[1]) * f)
                    sub.poly([TL(b3_circle(q, 0.7))], fill=B3_COL["deck"], stroke=B3_COL["deck_edge"], lw=0.06)
            el_names.append((u"Stepping stones", ((a_[0] + b_[0]) / 2.0, (a_[1] + b_[1]) / 2.0)))
        hard.append((bbox([a_, b_]), [a_, b_], B3_FOOT_W / 2.0 + B3_TREE_CLEAR))
    with mpx_grp(sub, "annotations", u"sightline"):
        for P in cl["sight"]:
            if len(P) >= 2:
                sub.line(TL(P), B3_COL["ink"], 0.12, [1.4, 0.8], cap=0)
                el_names.append((u"Sightline to the Trajaneum", P[0]))
    # ---- 10 trees by function (the masterplan's wet-to-dry riparian set + survey trees kept), off hard ground
    h_idx = {}
    for i_, (bb_, P, r_) in enumerate(hard):
        for gi in range(int(bb_[0] // 40) - 1, int(bb_[2] // 40) + 2):
            for gj in range(int(bb_[1] // 40) - 1, int(bb_[3] // 40) + 2):
                h_idx.setdefault((gi, gj), []).append(i_)

    def on_hard(p, cr):
        for i_ in h_idx.get((int(p[0] // 40), int(p[1] // 40)), ()):
            bb_, P, r_ = hard[i_]
            if len(P) >= 3 and P[0] == P[-1]:
                continue
            for a, b in zip(P[:-1], P[1:]):
                if seg_dist(p[0], p[1], a, b) < r_ + cr * 0.25:
                    return True
        return False
    n_t, n_skip = 0, 0
    trees = [(p, key, cr, u"riparian") for p, key, cr in pl23_tree_set(C)]
    trees += [(p, "plane", PLA_SPECIES["plane"]["crown_m"] * 0.8, u"hub shade") for p, i in pl23_hub_trees(C)]
    trees += [((xs, ys), key, PLA_SPECIES[key]["crown_m"], u"garden shade")
              for key, xs, ys in ((dgd or {}).get("shade_trees") or []) if key in PLA_SPECIES]
    trees += [(P[0], "plane", 7.0, u"existing") for P in sv.get("tree", []) if P and ins(P[0])]
    all_b = [(bbox(R), R) for R in blds + sheds]
    near_b = lambda p, r: any(bb[0] - r <= p[0] <= bb[2] + r and bb[1] - r <= p[1] <= bb[3] + r and
                              (pip(p[0], p[1], R) or b3_dist_ring(R, p) < r) for bb, R in all_b)
    placed = []
    with mpx_grp(sub, "trees", u"trees"):
        for p, key, cr, why in trees:
            if not ins(p) or in_water(p) or near_b(p, cr * 0.45) or on_hard(p, cr) or \
                    any(pip(p[0], p[1], R) for R in chan) or \
                    any(math.hypot(p[0] - q[0], p[1] - q[1]) < (cr + c2) * 0.35 for q, c2 in placed):
                n_skip += 1
                continue
            b3_tree(sub, T(p), cr * k / 2.0, n_t, key)
            placed.append((p, cr))
            n_t += 1
    # ---- 11 the edge fades out
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
    # ---- 12 the zone line under the buildings; every building whole: inside = kept (white, heritage salmon) or
    # removed (dashed), outside = pale context (Aras 22:12, 22:55)
    with mpx_grp(sub, "annotations", u"project zone"):
        for Q in st:
            sub.line(Q + Q[:1], B3_COL["border"], 0.3)
    sh = 0.9 * k
    sh_in = [R for R in sheds if ins(inner_pt(R)) and not gone(R)]
    sh_rm = [R for R in sheds if ins(inner_pt(R)) and gone(R)]
    with mpx_grp(sub, "buildings", u"context buildings"):
        for R in b_out + [R for R in sheds if not ins(inner_pt(R))]:
            sub.poly([TL(R)], fill=B3_COL["bld_ctx"], stroke=B3_COL["bld_ctx_edge"], lw=0.06)
    with mpx_grp(sub, "buildings", u"buildings in the zone, kept"):
        for R in b_in + sh_in:
            sub.poly([[(x + sh, y - sh) for x, y in TL(R)]], fill=B3_COL["shadow"], alpha=0.45)
        for R in b_in + sh_in:
            sub.poly([TL(R)], fill=B3_COL["heritage"] if is_her(R) else B3_COL["bld"], stroke=B3_COL["bld_edge"],
                     lw=0.13)
    with mpx_grp(sub, "buildings", u"buildings removed"):
        for R in b_rm + sh_rm:
            Q = TL(R)
            sub.poly([Q], fill="FFFFFF", alpha=0.5)
            sub.line(Q + Q[:1], B3_COL["removed_edge"], 0.12, [0.6, 0.5], cap=0)
    # programme points (Aras draws the facilities himself: a mark + its name, one colour per programme family)
    prog = []
    for z in C.D.zones:
        if z["code"] in ("GR", "DG") and z.get("q"):
            prog.append(("food", u"Café", z["q"]))
        if z["code"] == "WT" and z.get("q"):
            prog.append(("edu", u"Education · reed-basin classroom", z["q"]))
        if (z["code"] == "WS" or (z["code"] == "WA" and z.get("tier") == "F")) and z.get("q"):
            prog.append(("hub", u"Seats", z["q"]))
    prog += [("edu", u"Education · craft workshops", CRAFT_XY), ("culture", u"Deck, archaeology", ROMAN_WALL)]
    if C.terrace:
        prog.append(("culture", u"Viewing terrace", C.terrace["xy"]))
    for hb in C.hubs:
        if hb.get("in_study"):
            kind = u"Transit hub" if hb["role"] == "transit" else (u"Gateway out" if hb["id"] == u"K6" else u"Walking hub")
            prog.append(("hub", kind, hb["xy"]))
            if hb.get("sub_xy"):
                prog.append(("hub", u"Sub-hub in the bed", hb["sub_xy"]["c"]))
    prog = [x for x in prog if ins(x[2])]
    with mpx_grp(sub, "annotations", u"programme marks"):
        for fam, nm_, p in prog:
            x, y = T(p)
            sub.poly([[(x, y + 1.3), (x - 1.1, y - 0.6), (x + 1.1, y - 0.6)]], fill=B3_COL[fam],
                     stroke=B3_COL["ink"], lw=0.06)
    # ---- 13 names (no overlaps): zones, hubs, bridges, the promenade and main streets
    taken = []
    for R in b_in + b_out:
        Q = TL(R)
        xs, ys = [q[0] for q in Q], [q[1] for q in Q]
        if max(xs) - min(xs) > 0.6 or max(ys) - min(ys) > 0.6:
            taken.append((min(xs), min(ys), max(xs), max(ys)))
    seen, labels = {}, []
    zin = lambda bx, by: ins((x0 + bx / k, y0 + by / k))

    def name(s_, p, size, bold=False):
        if any(math.hypot(p[0] - q[0], p[1] - q[1]) < 250.0 for q in seen.get(s_, [])):
            return True
        seen.setdefault(s_, []).append(p)
        x, y = T(p)
        w_ = text_w(s_, size, bold)
        spots = [(-w_ / 2.0, -size / 2.0), (1.2, 0.8), (-1.2 - w_, 0.8), (1.2, -size - 0.8),
                 (-1.2 - w_, -size - 0.8), (-w_ / 2.0, 2.0), (-w_ / 2.0, -size - 2.0)]
        spots += [(-w_ / 2.0 + a * 4.0, -size / 2.0 + c * 3.0) for a in (-1, 0, 1) for c in (-2, -1, 1, 2)]
        for strict in (True, False):
            for dx, dy in spots:
                b = (x + dx, y + dy, x + dx + w_, y + dy + size)
                if not (0 <= b[0] and b[2] <= dw and 0 <= b[1] and b[3] <= dh):
                    continue
                if strict and (any(hit(b, o, 0.4) for o in taken) or not (zin(b[0], b[1]) and zin(b[2], b[3])
                                                                         and zin(b[0], b[3]) and zin(b[2], b[1]))):
                    continue
                if not strict and (any(hit(b, o, 0.4) for o in labels) or not zin((b[0] + b[2]) / 2.0, b[1])):
                    continue
                taken.append(b)
                labels.append(b)
                sub.text(s_, b[0], b[1], size, B3_COL["ink"], bold=bold)
                return True
        return False
    left = []
    for hb in C.hubs:
        if hb.get("in_study") and not name(b3_title(HUB_NAME.get(hb["id"], hb["id"])), hb["xy"], 2.12, True):
            left.append(hb["id"])
    for z in C.D.zones:
        if z.get("label") and z.get("q") and ins(z["q"]) and z["label"].strip().lower() != "bed":
            if not name(b3_title(z["label"], first_only=True), z["q"], 1.76):
                left.append(z["label"])
    for fam, nm_, p in prog:
        if not name(nm_, p, 1.76):
            left.append(nm_)
    for nm_, ch, p in road_names:
        name(b3_title(nm_) + u" · " + ch, p, 1.76)
    for nm_, p in el_names:
        name(nm_, p, 1.76)
    for i, w_ in enumerate(C.widen):
        if len(w_.get("ring") or []) >= 3:
            name(u"Widened · wetland, new bank", inner_pt(w_["ring"]), 1.76)
    for a_ in C.arms:
        if len(a_.get("P") or []) >= 2:
            name(u"Planted side arm", a_["P"][len(a_["P"]) // 2], 1.76)
    for P in cl["cov"]:
        if len(P) >= 2:
            name(u"Hidden stream line", P[len(P) // 2], 1.76)
    for P in C.terr[:1]:
        name(u"Rain terraces on the contours", P[len(P) // 2], 1.76)
    # ---- sheet
    W, H = dw + 2 * B19_M, dh + 2 * B19_M + B19_HEAD + 14.0
    pg = Page(W, H)
    pg.poly([rect(0.0, 0.0, W, H)], fill="FFFFFF")
    pg.clip([rect(B19_M, B19_M + B19_HEAD + 14.0, B19_M + dw, B19_M + B19_HEAD + 14.0 + dh)])
    blit(pg, sub, B19_M, B19_M + B19_HEAD + 14.0)
    pg.unclip()
    leg = [(u"street kept (car)", B3_COL["asphalt"]), (u"street calmed / shared / pedestrian", B3_COL["paving"]),
           (u"riverside walk 4 m", B3_COL["paving"]), (u"bike lane beside the walk", B3_COL["bike"]),
           (u"bed walk, shut in floods", B3_COL["gravel"]), (u"footbridge / bridge / canopied walkway", B3_COL["deck"]),
           (u"stream", B3_COL["water"]), (u"widened stream, wetland", B3_COL["water_lt"]), (u"reed basins", B3_COL["reed"]),
           (u"riparian woodland floor (6-32 m)", B3_COL["wood"]), (u"lawn with tree groups (32-62 m)", B3_COL["lawn"]),
           (u"open meadow", B3_COL["meadow"]), (u"rain terraces, dry tops", B3_COL["lawn_dk"]),
           (u"Demeter's Garden", B3_COL["garden"]), (u"willow, tamarisk: wet edge", B3_TREE_TONE["willow"]),
           (u"ash, plane: drier ground", B3_TREE_TONE["plane"]), (u"programme at the hubs (dashed ring)", B3_COL["prog"]), (u"building kept", B3_COL["bld"]), (u"heritage kept", B3_COL["heritage"]),
           (u"culture", B3_COL["culture"]), (u"food", B3_COL["food"]), (u"education", B3_COL["edu"]),
           (u"hubs, seats", B3_COL["hub"])]
    lx, ly = B19_M, B19_M + B19_HEAD + 4.0
    for nm, col in leg:
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
    notes += [u"streets: {} OSM ways, {} on survey widths".format(len(ways), sum(1 for x in ways if x[5])),
              u"project elements: " + u", ".join(u"%s %d" % kv for kv in sorted(n_el.items())) +
              u"; roads by change: " + u", ".join(u"%s %d" % kv for kv in sorted(n_rd.items())),
              u"bridge ends joined to a walk: {}; trees {} ({} not placed: on paving, water, buildings or another "
              u"crown)".format(n_end, n_t, n_skip),
              u"buildings: {} in the zone kept, {} removed, {} context".format(len(b_in), len(b_rm), len(b_out)),
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
