

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
VERSION = "bergama_b19_plan v8.1 (2026-11-06)"  # v8.1 (Aras 12:01-12:04 TR, run over 30 min): rhino_bake False (default) skips the Rhino copy entirely, only the script's PDF is written; each step's time in the log; v8 (Aras 6 Nov 09:13-10:43 TR): 1:1,000 on one sheet = site_alan turned flat; v6 context back (streets on survey edges, else OSM width); green around the zone and existing tree cover from the Maxar 1 Mar 2023 image; Aras's painted tree + shrub set traced (131 symbols, each stored once in the PDF and as one Rhino block); his bush hatch as 5 seamless tiles filling organic bush areas and hedges; ground greens by slope (survey contours); places as numbered boxed callouts with icons, one colour per category, tied by one route with direction arrows; parent + sub groups in the PDF (Illustrator) and Rhino (layers + groups); PDF lean pass (14.4 -> 5.5 MB); data in Data/bergama_b19_plan_data.py; survey linework cleaned (duplicates, overlaps merged, corners joined at the intersection, gaps closed, undershoots extended, overshoots trimmed, strays dropped, crooked vertices straightened), one pen set for every stroke, the Rhino drawing deleted from the .3dm after Rhino writes its PDF; v7 (Aras 00:46-05:38, V7_PLAN R1-R12): every place for a reason: reaches with a theme, programme lined up along the walk, green corridor, trees by rule (rows, contour groves, square edges), open edge with screens only where needed, pure-Python fade, one road bridge deck, no ellipses or entrance circles, readable names + numbered key, new features (steps to the water, amphitheatre, boardwalk loop, skate, orchard, dog run); v6 (Aras 00:03-00:25, V6_PLAN F1-F12): every non-heritage building in the zone taken out and its ground designed; only Kozak road + Adnan Menderes kept as car roads (carriageway, pavements, direction arrows), shared streets inside; stream from the bank stations smoothed, off car roads; one continuous walk + loop-free bike lane per bank; footbridges to dry land; drawn programme pads (café, classroom, seats, decks, courts, fitness, play, lawns, allotments, meadow, bird hides), heritage trail; rain terraces, 2 m ground steps; planting by function; hedge + entrances at the edge; v5.1 (Aras 23:41-23:42): heritage never taken out; the freed Ulucami ground designed as the hub square with plane shade; v5 (Aras 23:26): planting from the asset library species (emergent edge, terraces, dry tops), names off roads and water with leaders, walks merged in two passes + loose ends joined, river rounded with a drainage wall, Ulucami buildings in the zone taken out, edge-crossing buildings outside, 10-step greenery gradient, shaded contours; v4 (Aras 22:55): the project's own walks, bike lane, roads by change, bridges with joined ends, terraces, basins, arms, garden, programme marks; OSM tracks and invented promenades/connectors gone; bike strips only beside the walk; every building whole in or out; trees off buildings and each other; v3 (Aras 22:19 "get better"): rebuilt from survey + OSM + stations: streets at survey widths with bike strips, promenades on both banks with varying width, curved connectors, footbridges with landings, ground by distance from water (wood, lawn, meadow), one continuous stream, trees by function off paving and water, names inside the zone; v2 rejected 22:18, v1 rejected 21:26
SHORT = "v7"
GH_LABEL = "B19Plan"
SETTINGS = ("rhino_bake", "scale")
OUT_FOLDER = "bergama_b19_plan"
LOG_NAME = "bergama_b19_plan_log.txt"
BAKE_ROOT = "B19"
B19_SCALE = 1000.0           # v8 (Aras 6 Nov 10:06 TR): 1:1,000 on one free-size sheet (was 1:4,000); input `scale` overrides
B19_NAME = "Bergama_B19_plan_v8.pdf"
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
# v7 (Aras 05:42-05:46, "1:1 from the .3dm"): more survey layers read by this script. Religious buildings
# (BINA_DINITESIS: Ulucami) count as heritage = kept; 1 m / 2 m contours; heritage detail lines drawn as surveyed.
ROLE_OF.update({"BINA_DINITESIS": "heritage", "BINA_DINI_TESIS": "heritage", "EGRI_1M": "contour1",
                "EGRI_2M": "contour2", "BINA_MERDIVEN": "stairs", "BINA_KAPI": "door", "BINA_TARAMA": "bhatch",
                "SEMBOL_CAMI_MESCID": "mosque_sym", "SEV_SEV": "slope"})
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


# ================================================================ v8 linework cleanup (Aras 6 Nov 09:13 TR)
# "remove stray and duplicate lines, merge overlapping or nearly-touching segments into single continuous lines,
# close small gaps and properly join corners, straighten slightly crooked lines, keep consistent line weights.
# Don't change the design itself." Survey lines only; tolerances in m, far below the survey's own accuracy at the
# printed scale (0.05 m = 0.025 mm at 1:2,000).
B8_CLEAN = {        # role: (snap, gap, extend/trim, straighten, merge with other lines of the role)
    "road": (0.10, 0.60, 0.40, 0.05, True), "kerb": (0.10, 0.60, 0.40, 0.05, True),
    "wall": (0.08, 0.40, 0.30, 0.04, True), "histwall": (0.08, 0.40, 0.30, 0.04, True),
    "slope": (0.08, 0.40, 0.30, 0.05, True),
    "stairs": (0.04, 0.15, 0.12, 0.02, True), "door": (0.03, 0.10, 0.10, 0.02, True),
    "bhatch": (0.04, 0.12, 0.10, 0.02, True), "pond": (0.04, 0.20, 0.10, 0.02, True),
    "contour1": (0.03, 0.30, 0.0, 0.05, False), "contour2": (0.03, 0.30, 0.0, 0.05, False),
    "contour": (0.03, 0.30, 0.0, 0.05, False), "contour10": (0.03, 0.30, 0.0, 0.05, False)}
B8_STRAY_M = 0.15   # a lone piece shorter than this (not joined to anything) is a stray: dropped
B8_PENS = (0.03, 0.05, 0.07, 0.1, 0.13, 0.18, 0.25, 0.35, 0.5, 0.7, 1.0)   # one pen set for the whole sheet (mm)


def b8_dp(P, tol):
    """Douglas-Peucker: drops vertices within tol of the straight run (straightens slightly crooked lines)"""
    if len(P) < 3 or tol <= 0:
        return list(P)
    keep = [False] * len(P)
    keep[0] = keep[-1] = True
    st = [(0, len(P) - 1)]
    while st:
        i, j = st.pop()
        ax, ay = P[i]
        bx, by = P[j]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy)
        best, bi = -1.0, -1
        for m in range(i + 1, j):
            px, py = P[m]
            d = abs(dx * (py - ay) - dy * (px - ax)) / L if L > 1e-9 else math.hypot(px - ax, py - ay)
            if d > best:
                best, bi = d, m
        if best > tol:
            keep[bi] = True
            st.append((i, bi))
            st.append((bi, j))
    return [p for p, k_ in zip(P, keep) if k_]


def b8_dp_closed(P, tol):
    Q = list(P[:-1]) if len(P) > 1 and P[0] == P[-1] else list(P)
    if len(Q) < 4:
        return Q + [Q[0]]
    far = max(range(len(Q)), key=lambda i: (Q[i][0] - Q[0][0]) ** 2 + (Q[i][1] - Q[0][1]) ** 2)
    a = b8_dp(Q[:far + 1], tol)
    b = b8_dp(Q[far:] + [Q[0]], tol)
    R = a[:-1] + b[:-1]
    return (R + [R[0]]) if len(R) >= 3 else Q + [Q[0]]


def _b8_seg_x(a, b, c, d):
    """intersection params (t on ab, u on cd) of two segments' lines, or None if parallel"""
    rx, ry = b[0] - a[0], b[1] - a[1]
    sx, sy = d[0] - c[0], d[1] - c[1]
    den = rx * sy - ry * sx
    if abs(den) < 1e-12:
        return None
    qx, qy = c[0] - a[0], c[1] - a[1]
    return (qx * sy - qy * sx) / den, (qx * ry - qy * rx) / den


def b8_clean_lines(Ps, snap, gap, ext, simp, merge, st):
    """one role's polylines -> cleaned polylines. st = counters dict."""
    Ps = [[(float(p[0]), float(p[1])) for p in P] for P in Ps if len(P) >= 2]
    if not Ps:
        return []
    if not merge:                                         # contours: each line kept on its own (heights differ)
        out, seen = [], set()
        for P in Ps:
            Q = [P[0]]
            for p in P[1:]:
                if math.hypot(p[0] - Q[-1][0], p[1] - Q[-1][1]) > snap:
                    Q.append(p)
            if len(Q) < 2:
                st["stray"] += 1
                continue
            key = tuple(sorted([(round(Q[0][0], 2), round(Q[0][1], 2)), (round(Q[-1][0], 2), round(Q[-1][1], 2))])
                        ) + (len(Q), round(sum(q[0] for q in Q), 1))
            if key in seen:
                st["dup"] += 1
                continue
            seen.add(key)
            out.append(Q)
        ends = {}                                         # join fragments end to end (same line broken in two)
        for i, Q in enumerate(out):
            for e in (0, 1):
                p = Q[0] if e == 0 else Q[-1]
                ends.setdefault((int(p[0] // gap), int(p[1] // gap)), []).append((i, e))
        alive = [True] * len(out)
        for i in range(len(out)):
            if not alive[i]:
                continue
            for _ in range(8):
                Q = out[i]
                if math.hypot(Q[0][0] - Q[-1][0], Q[0][1] - Q[-1][1]) <= gap:
                    if Q[0] != Q[-1]:
                        Q.append(Q[0])
                        st["closed"] += 1
                    break
                p, q = Q[-1], Q[-2]
                ux, uy = p[0] - q[0], p[1] - q[1]
                L = math.hypot(ux, uy) or 1.0
                ux, uy = ux / L, uy / L
                best = None
                cx, cy = int(p[0] // gap), int(p[1] // gap)
                for gx in (cx - 1, cx, cx + 1):
                    for gy in (cy - 1, cy, cy + 1):
                        for j, e in ends.get((gx, gy), []):
                            if j == i or not alive[j]:
                                continue
                            R = out[j]
                            s = R[0] if e == 0 else R[-1]
                            s2 = R[1] if e == 0 else R[-2]
                            d = math.hypot(s[0] - p[0], s[1] - p[1])
                            vx, vy = s2[0] - s[0], s2[1] - s[1]
                            Lv = math.hypot(vx, vy) or 1.0
                            if d <= gap and (ux * vx + uy * vy) / Lv > 0.85 and (best is None or d < best[0]):
                                best = (d, j, e)
                if best is None:
                    break
                d, j, e = best
                R = out[j] if e == 0 else out[j][::-1]
                out[i] = Q + R[1:] if d < 1e-9 else Q + R
                alive[j] = False
                st["joined"] += 1
        res = []
        for i, Q in enumerate(out):
            if not alive[i]:
                continue
            closed = len(Q) > 3 and Q[0] == Q[-1]
            n0 = len(Q)
            Q = b8_dp_closed(Q, simp) if closed else b8_dp(Q, simp)
            st["vtx"] += n0 - len(Q)
            res.append(Q)
        return res
    # ---- 1 snap every vertex onto its neighbours within `snap` (shared points become one point)
    pts = [p for P in Ps for p in P]
    par = list(range(len(pts)))

    def fnd(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i
    grid = {}
    for i, p in enumerate(pts):
        grid.setdefault((int(p[0] // snap), int(p[1] // snap)), []).append(i)
    for (gx, gy), idx in grid.items():
        for ox in (0, 1):
            for oy in (-1, 0, 1):
                if ox == 0 and oy < 0:
                    continue
                other = idx if (ox, oy) == (0, 0) else grid.get((gx + ox, gy + oy), [])
                for a_ in idx:
                    pa = pts[a_]
                    for b_ in other:
                        if b_ <= a_ and other is idx:
                            continue
                        pb = pts[b_]
                        if abs(pa[0] - pb[0]) <= snap and abs(pa[1] - pb[1]) <= snap and \
                                (pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2 <= snap * snap:
                            ra, rb = fnd(a_), fnd(b_)
                            if ra != rb:
                                par[rb] = ra
    acc = {}
    for i, p in enumerate(pts):
        r = fnd(i)
        a = acc.setdefault(r, [0.0, 0.0, 0])
        a[0] += p[0]
        a[1] += p[1]
        a[2] += 1
    node_of, nodes, k_ = {}, [], 0
    for r, a in acc.items():
        node_of[r] = len(nodes)
        nodes.append([a[0] / a[2], a[1] / a[2]])
    st["snapped"] += len(pts) - len(nodes)
    # ---- 2 segments between nodes; exact duplicates (either direction) and zero lengths dropped
    segs, seen = [], set()
    for P in Ps:
        for p, q in zip(P, P[1:]):
            k_ += 0
    i0 = 0
    for P in Ps:
        ids = [node_of[fnd(i0 + m)] for m in range(len(P))]
        i0 += len(P)
        for a, b in zip(ids, ids[1:]):
            if a == b:
                continue
            key = (a, b) if a < b else (b, a)
            if key in seen:
                st["dup"] += 1
                continue
            seen.add(key)
            segs.append(list(key))
    # ---- 3 overlapping collinear segments merged into one (the longest run of each group)
    tol_d, tol_a = max(0.02, snap * 0.5), math.radians(1.5)
    sgrid, cell = {}, max(1.0, gap * 4)

    def seg_cells(a, b):
        A, B = nodes[a], nodes[b]
        x0_, x1_ = sorted((A[0], B[0]))
        y0_, y1_ = sorted((A[1], B[1]))
        for gx in range(int(x0_ // cell), int(x1_ // cell) + 1):
            for gy in range(int(y0_ // cell), int(y1_ // cell) + 1):
                yield (gx, gy)
    for si, (a, b) in enumerate(segs):
        for c_ in seg_cells(a, b):
            sgrid.setdefault(c_, []).append(si)
    dead = [False] * len(segs)
    for si in range(len(segs)):
        if dead[si]:
            continue
        a, b = segs[si]
        A, B = nodes[a], nodes[b]
        dx, dy = B[0] - A[0], B[1] - A[1]
        L = math.hypot(dx, dy)
        if L < 1e-6:
            dead[si] = True
            continue
        ux, uy = dx / L, dy / L
        cand = set()
        for c_ in seg_cells(a, b):
            cand.update(sgrid.get(c_, ()))
        for sj in cand:
            if sj <= si or dead[sj]:
                continue
            c, d = segs[sj]
            Cc, D = nodes[c], nodes[d]
            ex, ey = D[0] - Cc[0], D[1] - Cc[1]
            Le = math.hypot(ex, ey)
            if Le < 1e-6:
                dead[sj] = True
                continue
            if abs(ux * ey - uy * ex) / Le > math.sin(tol_a):
                continue
            dc = abs(ux * (Cc[1] - A[1]) - uy * (Cc[0] - A[0]))
            dd = abs(ux * (D[1] - A[1]) - uy * (D[0] - A[0]))
            if dc > tol_d or dd > tol_d:
                continue
            tc = ux * (Cc[0] - A[0]) + uy * (Cc[1] - A[1])
            td = ux * (D[0] - A[0]) + uy * (D[1] - A[1])
            lo, hi = min(tc, td), max(tc, td)
            if hi < 0.01 or lo > L - 0.01:                # end to end only: not an overlap (chained later)
                continue
            ends = [(0.0, a), (L, b), (tc, c), (td, d)]
            ends.sort()
            segs[si] = [ends[0][1], ends[-1][1]]
            a, b = segs[si]
            A, B = nodes[a], nodes[b]
            dx, dy = B[0] - A[0], B[1] - A[1]
            L = math.hypot(dx, dy)
            ux, uy = dx / L, dy / L
            dead[sj] = True
            st["overlap"] += 1
    segs = [s for s, dd_ in zip(segs, dead) if not dd_]
    # ---- 4 free ends: corners joined at the true intersection, gaps closed, undershoots extended, overshoots trimmed
    adj = {}
    for si, (a, b) in enumerate(segs):
        adj.setdefault(a, []).append(si)
        adj.setdefault(b, []).append(si)
    other = lambda si, n: segs[si][1] if segs[si][0] == n else segs[si][0]
    free = [n for n, L_ in adj.items() if len(L_) == 1]
    fgrid, gc = {}, max(gap, 0.05)
    for n in free:
        fgrid.setdefault((int(nodes[n][0] // gc), int(nodes[n][1] // gc)), []).append(n)

    def out_dir(n):
        m = other(adj[n][0], n)
        dx, dy = nodes[n][0] - nodes[m][0], nodes[n][1] - nodes[m][1]
        L = math.hypot(dx, dy) or 1.0
        return dx / L, dy / L, m
    used = set()
    for n in free:
        if n in used or len(adj.get(n, ())) != 1:
            continue
        p = nodes[n]
        ux, uy, m = out_dir(n)
        best = None
        cx, cy = int(p[0] // gc), int(p[1] // gc)
        for gx in (cx - 1, cx, cx + 1):
            for gy in (cy - 1, cy, cy + 1):
                for q in fgrid.get((gx, gy), []):
                    if q == n or q in used or len(adj.get(q, ())) != 1 or q == m:
                        continue
                    d = math.hypot(nodes[q][0] - p[0], nodes[q][1] - p[1])
                    if d <= gap and (best is None or d < best[0]):
                        best = (d, q)
        if best is None:
            continue
        d, q = best
        vx, vy, mq = out_dir(q)
        if mq == n:
            continue
        gx_, gy_ = nodes[q][0] - p[0], nodes[q][1] - p[1]
        gl = math.hypot(gx_, gy_) or 1.0
        cos_n = (ux * gx_ + uy * gy_) / gl                # the gap continues this end
        cos_q = -(vx * gx_ + vy * gy_) / gl               # ... and the other end
        x = _b8_seg_x(nodes[m], p, nodes[mq], nodes[q])
        turn = abs(ux * vy - uy * vx)
        if x is not None and turn > 0.26:                 # a corner (> 15 deg): both ends meet at the intersection
            t, u_ = x
            X = (nodes[m][0] + t * (p[0] - nodes[m][0]), nodes[m][1] + t * (p[1] - nodes[m][1]))
            if t > 0.5 and u_ > 0.5 and math.hypot(X[0] - p[0], X[1] - p[1]) <= gap * 1.5 and \
                    math.hypot(X[0] - nodes[q][0], X[1] - nodes[q][1]) <= gap * 1.5:
                nodes[n] = [X[0], X[1]]
                for s_ in adj[q]:
                    segs[s_] = [n if v == q else v for v in segs[s_]]
                adj[n] = adj[n] + adj[q]
                adj[q] = []
                used.update((n, q))
                st["corner"] += 1
                continue
        if cos_n > 0.7 and cos_q > 0.7:                   # a straight gap: closed with a short piece
            segs.append([n, q])
            adj[n].append(len(segs) - 1)
            adj[q].append(len(segs) - 1)
            used.update((n, q))
            st["gap"] += 1
    if ext > 0:
        sgrid = {}
        for si, (a, b) in enumerate(segs):
            for c_ in seg_cells(a, b):
                sgrid.setdefault(c_, []).append(si)
        for n in free:
            if len(adj.get(n, ())) != 1:
                continue
            ux, uy, m = out_dir(n)
            p = nodes[n]
            far = (p[0] + ux * ext, p[1] + uy * ext)
            cand = set()
            for gx in range(int(min(nodes[m][0], far[0]) // cell), int(max(nodes[m][0], far[0]) // cell) + 1):
                for gy in range(int(min(nodes[m][1], far[1]) // cell), int(max(nodes[m][1], far[1]) // cell) + 1):
                    cand.update(sgrid.get((gx, gy), ()))
            own = adj[n][0]
            best = None
            seg_len = math.hypot(p[0] - nodes[m][0], p[1] - nodes[m][1]) or 1.0
            for sj in cand:
                if sj == own or n in segs[sj] or m in segs[sj]:
                    continue
                c, d = segs[sj]
                x = _b8_seg_x(nodes[m], p, nodes[c], nodes[d])
                if x is None or not (-1e-9 <= x[1] <= 1 + 1e-9):
                    continue
                over = (x[0] - 1.0) * seg_len             # > 0: undershoot (extend), < 0: overshoot (trim)
                if (0 < over <= ext) or (-ext <= over < 0 and x[0] > 0.3):
                    if best is None or abs(over) < abs(best[0]):
                        best = (over, x[0])
            if best is not None:
                t = best[1]
                nodes[n] = [nodes[m][0] + t * (p[0] - nodes[m][0]), nodes[m][1] + t * (p[1] - nodes[m][1])]
                st["extend" if best[0] > 0 else "trim"] += 1
    # ---- 5 chain the segments into continuous lines through every two-way node
    adj = {}
    for si, (a, b) in enumerate(segs):
        if a != b:
            adj.setdefault(a, []).append(si)
            adj.setdefault(b, []).append(si)
    done = [False] * len(segs)
    lines = []

    def walk(n, si):
        P = [n]
        while True:
            done[si] = True
            n2 = other(si, n)
            P.append(n2)
            nxt = [s_ for s_ in adj.get(n2, ()) if not done[s_]]
            if len(adj.get(n2, ())) != 2 or not nxt:
                return P
            n, si = n2, nxt[0]
    for n, L_ in adj.items():
        if len(L_) != 2:
            for si in L_:
                if not done[si]:
                    lines.append(walk(n, si))
    for si in range(len(segs)):
        if not done[si] and segs[si][0] != segs[si][1]:
            lines.append(walk(segs[si][0], si))           # closed loops
    res = []
    for ids in lines:
        P = [tuple(nodes[i]) for i in ids]
        closed = len(ids) > 3 and ids[0] == ids[-1]
        if not closed and len(adj.get(ids[0], ())) == 1 and len(adj.get(ids[-1], ())) == 1:
            Lp = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(P, P[1:]))
            if Lp < B8_STRAY_M:
                st["stray"] += 1
                continue
        n0 = len(P)
        P = b8_dp_closed(P, simp) if closed else b8_dp(P, simp)
        st["vtx"] += n0 - len(P)
        res.append(P)
    return res


def b8_clean_survey(sv, box, notes):
    """v8: every survey line role in B8_CLEAN cleaned (inside box + 30 m); other roles untouched. Logs one line."""
    t0 = time.time()
    out = dict(sv)
    st = dict(snapped=0, dup=0, overlap=0, corner=0, gap=0, extend=0, trim=0, joined=0, closed=0, stray=0, vtx=0)
    b = (box[0] - 30.0, box[1] - 30.0, box[2] + 30.0, box[3] + 30.0)
    n_in = n_out = 0
    for role, prm in B8_CLEAN.items():
        Ps = sv.get(role) or []
        if not Ps:
            continue
        near = [P for P in Ps if hit(bbox(P), b)]
        far = [P for P in Ps if not hit(bbox(P), b)]
        try:
            cl = b8_clean_lines(near, *(prm + (st,)))
        except Exception as ex:
            notes.append(u"v8 linework: %s not cleaned (%s: %s)" % (role, type(ex).__name__, ex))
            continue
        n_in += len(near)
        n_out += len(cl)
        out[role] = cl + far
    notes.append(u"v8 linework cleaned: %d survey lines -> %d (duplicates %d, overlaps merged %d, corners joined "
                 u"%d, gaps closed %d, ends extended %d, overshoots trimmed %d, pieces joined %d, closed %d, strays "
                 u"%d, crooked vertices dropped %d), %.1f s" % (
                     n_in, n_out, st["dup"], st["overlap"], st["corner"], st["gap"], st["extend"], st["trim"],
                     st["joined"], st["closed"], st["stray"], st["vtx"], time.time() - t0))
    return out


def b8_site_turn(site):
    """v8: the angle (rad) that turns site_alan's longest side horizontal, its eastern end to the right"""
    best = None
    for a, b in zip(site, site[1:] + site[:1]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if best is None or L > best[0]:
            best = (L, b[0] - a[0], b[1] - a[1])
    _, vx, vy = best
    if vx < 0:
        vx, vy = -vx, -vy
    return -math.atan2(vy, vx)


_B8_VEG = {}


def b8_ctx_rings(Ps, tol=0.25, min_mm2=0.8):
    """context tint rings on paper (mm): thinned to tol mm and 0.1 mm points (a light tint's edge; the imagery itself
    is good to ~5 m = 5 mm), specks under min_mm2 out"""
    out = []
    for R in Ps:
        Q = [(round(p[0], 1), round(p[1], 1)) for p in b8_dp_closed(R, tol)]
        if len(Q) >= 4 and abs(sum(Q[i][0] * Q[i - 1][1] - Q[i - 1][0] * Q[i][1] for i in range(len(Q)))) > 2.0 * min_mm2:
            out.append(Q)
    return out


def b8_veg_rings(key):
    """v8 (Aras 09:28-09:29 TR "prefer satellite imagery"): land cover traced from Esri World Imagery, Maxar Vivid
    of 1 Mar 2023 (0.31 m), in survey m (VEG_EMBED; library/satellite_2026-11-06): trees, grass, bare. [] if absent"""
    if key not in _B8_VEG:
        try:
            d = json.loads(zlib.decompress(base64.b64decode("".join(globals()["VEG_EMBED"]))).decode("utf-8"))
            _B8_VEG[key] = [r_ for r_ in d.get("rings", {}).get(key, []) if len(r_) >= 3]
        except Exception:
            _B8_VEG[key] = []
    return _B8_VEG[key]


def b8_pen(lw):
    """v8: a line weight -> the nearest pen of the one sheet-wide pen set (consistent weights)"""
    try:
        v = float(lw)
    except Exception:
        return lw
    if v <= 0:
        return lw
    return min(B8_PENS, key=lambda q: abs(q - v))


def b8_pens(pg):
    """v8: every stroke of the sheet set to its pen (B8_PENS)"""
    for i, it in enumerate(pg.items):
        kd = it[0]
        if kd == "poly" and it[4] is not None:
            pg.items[i] = it[:4] + (b8_pen(it[4]),) + it[5:]
        elif kd == "line" and it[3] is not None:
            pg.items[i] = it[:3] + (b8_pen(it[3]),) + it[4:]
        elif kd == "circle" and it[6] is not None:
            pg.items[i] = it[:6] + (b8_pen(it[6]),) + it[7:]
        elif kd == "clipline" and it[4] is not None:
            pg.items[i] = it[:4] + (b8_pen(it[4]),) + it[5:]


_B8_RGRP = []               # Rhino group indices made by the last bake (removed with it)


def b8_remove_bake(doc, warn):
    """v8 (Aras 09:16 TR: "delete afterwards because it would lag the .3dm"): every object on B7_BAKE_ROOT and its
    sub-layers deleted, then the layers themselves; no undo copies kept, so the file and memory stay light"""
    n = 0
    undo0 = doc.UndoRecordingEnabled
    try:
        doc.UndoRecordingEnabled = False
        lays = [l for l in doc.Layers if not l.IsDeleted and (l.FullPath == B7_BAKE_ROOT or
                                                               l.FullPath.startswith(B7_BAKE_ROOT + "::"))]
        lays.sort(key=lambda l: -l.FullPath.count("::"))
        for l in lays:
            for o in list(doc.Objects.FindByLayer(l) or []):
                if doc.Objects.Delete(o, True):
                    n += 1
        for d_ in list(doc.InstanceDefinitions):         # v8: the tree blocks
            try:
                if d_ is not None and not d_.IsDeleted and d_.Name.startswith(u"B19_tree_"):
                    doc.InstanceDefinitions.Delete(d_.Index, True, True)
            except Exception:
                pass
        for gi in _B8_RGRP:
            try:
                doc.Groups.Delete(gi)
            except Exception:
                pass
        del _B8_RGRP[:]
        for l in lays:
            try:
                doc.Layers.Delete(l.Index, True)
            except Exception:
                pass
        doc.Views.Redraw()
    except Exception as ex:
        warn.append(u"B19 Rhino drawing not fully removed ({}: {}); delete layer {} by hand".format(
            type(ex).__name__, ex, B7_BAKE_ROOT))
    finally:
        doc.UndoRecordingEnabled = undo0
    return n


# ================================================================ v8 tree symbols (Aras's painted set, traced) + grouped PDF
# Aras 6 Nov 10:02-10:10 TR: his own plan-view tree set (masterp_agac.svg), kept vector, best print quality at the
# smallest size; parent + sub groups in every output. A symbol = stacked tone bands (unit coords -1..1, y up), stored
# ONCE: one PDF form object per symbol (placed at every tree), one Rhino block per symbol.
_B8_SYMS = {}
B8_SPECIES_SYM = {           # species key -> Aras's traced symbols (a list = variants): SUGGESTED by look, Aras confirms
    "willow": ["S006", "S065", "S036"], "tamarisk": ["S053", "S032", "S001"], "ash": ["S056", "S081", "S014"],
    "plane": ["S047", "S027", "S045"], "olive": ["S021", "S058", "S029"],
    "stone_pine": ["S015", "S102", "S121", "S124"], "rosemary": ["S103", "S030", "S040"],
    "lavender": ["S117", "S082", "S114"], "hedge": ["S122", "S123", "S113", "S116"],
    "soft_rush": ["S130", "S070"], "rush": ["S071", "S129"], "loosestrife": ["S111", "S072"],
    "default": ["S007", "S022", "S086", "S046"]}


def b8_sym_lib():
    if "_" not in _B8_SYMS:
        _B8_SYMS["_"] = {}
        try:
            d = json.loads(zlib.decompress(base64.b64decode("".join(globals()["TREE_EMBED"]))).decode("utf-8"))
            for s_ in d.get("symbols", []):
                _B8_SYMS["_"][s_["id"]] = s_["bands"]
        except Exception:
            pass
    return _B8_SYMS["_"]


def b8_sym_for(key, seed=0):
    """the symbol id drawing species `key` (a list in B8_SPECIES_SYM = variants, picked by seed), or None"""
    lib = b8_sym_lib()
    v = B8_SPECIES_SYM.get(key) or B8_SPECIES_SYM.get("default")
    if isinstance(v, (list, tuple)):
        v = v[seed % len(v)] if v else None
    return v if v in lib else None


# v8 bush hatches (Aras 6 Nov 07:35 UTC: masterp_bush_hatch.svg, 5 styles, the top-right moss is the favourite): each
# style = one seamless tile (stacked tone bands, mm on paper, period P), stored ONCE in the PDF and repeated by a
# tiling pattern, so density stays the same in any bush size. Rhino gets the tile's mean colour (no such hatch there).
B8_BUSH_TILE = {"hedge": "H1", "rosemary": "H1", "lavender": "H4", "edge screen": "H5"}   # suggestion, Aras confirms
B8_BUSH_FN = (u"dry-top beds", u"edge screen")      # planting functions drawn as bush areas, not single symbols
B8_BUSH_CELL = 0.6           # m: grid of the bush-area field
B8_BUSH_GROW = 2.2           # x the plant's crown radius: one plant's reach; shrubs 2.5 m apart in a bed row merge
                             # into one ~2.4 m strip, rows 6 m apart stay apart (rows of planting, as designed)
B8_BUSH_WOBBLE = 0.18        # +- share of that reach, smooth random: abstract but stays where the shrubs are
_B8_TILES = {}


def b8_tiles():
    if "_" not in _B8_TILES:
        _B8_TILES["_"] = {}
        try:
            d = json.loads(zlib.decompress(base64.b64decode("".join(globals()["BUSH_EMBED"]))).decode("utf-8"))
            for t_ in d.get("tiles", []):
                _B8_TILES["_"][t_["id"]] = t_
        except Exception:
            pass
    return _B8_TILES["_"]


def b8_tile_for(key):
    t_ = B8_BUSH_TILE.get(key)
    return t_ if t_ in b8_tiles() else None


def b8_bush_rings(pts, seed):
    """b8_bush_one per cluster of touching shrubs (so the field grid stays the size of one bed, not the site)"""
    if not pts:
        return []
    reach = 2.2 * max(r for _, _, r in pts) * B8_BUSH_GROW
    par = list(range(len(pts)))

    def f_(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i
    hsh = {}
    for i, (x, y, r) in enumerate(pts):
        hsh.setdefault((int(x // reach), int(y // reach)), []).append(i)
    for (hx, hy), ids in hsh.items():
        for a_ in (hx - 1, hx, hx + 1):
            for b_ in (hy - 1, hy, hy + 1):
                for j in hsh.get((a_, b_), ()):
                    for i in ids:
                        if i < j and math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]) < reach:
                            par[f_(i)] = f_(j)
    cl = {}
    for i in range(len(pts)):
        cl.setdefault(f_(i), []).append(pts[i])
    out = []
    for n_, k_ in enumerate(sorted(cl)):
        out.append(b8_bush_one(cl[k_], seed * 1009 + n_))
    return out                                            # one list of rings per bush (cluster)


def b8_iso(F, x0, y0, c_, L, rounds=2, tol=0.08, min_area=None):
    """closed rings around the cells of grid F (F[i][j] at x0 + i c_, y0 + j c_) above level L: marching squares,
    rounded (Chaikin, `rounds`), thinned (tol m); F's border must be below L. Outer rings clockwise, holes ccw."""
    nx, ny = len(F), len(F[0])
    min_area = 2.0 * c_ * c_ if min_area is None else min_area
    segs = []

    def ip(i1, j1, i2, j2):
        a, b = F[i1][j1], F[i2][j2]
        t = 0.5 if a == b else (L - a) / (b - a)
        return (round(x0 + (i1 + (i2 - i1) * t) * c_, 4), round(y0 + (j1 + (j2 - j1) * t) * c_, 4))
    for i in range(nx - 1):
        for j in range(ny - 1):
            q = [F[i][j] > L, F[i + 1][j] > L, F[i + 1][j + 1] > L, F[i][j + 1] > L]
            if all(q) or not any(q):
                continue
            E = {0: ip(i, j, i + 1, j), 1: ip(i + 1, j, i + 1, j + 1), 2: ip(i, j + 1, i + 1, j + 1), 3: ip(i, j, i, j + 1)}
            idx = q[0] * 1 + q[1] * 2 + q[2] * 4 + q[3] * 8
            for e1, e2 in {1: ((3, 0),), 2: ((0, 1),), 3: ((3, 1),), 4: ((1, 2),), 5: ((3, 0), (1, 2)), 6: ((0, 2),),
                           7: ((3, 2),), 8: ((2, 3),), 9: ((2, 0),), 10: ((0, 1), (2, 3)), 11: ((2, 1),),
                           12: ((1, 3),), 13: ((1, 0),), 14: ((0, 3),)}[idx]:
                segs.append((E[e1], E[e2]))
    nxt = {}
    for a, b in segs:
        nxt[a] = b
    rings, seen = [], set()
    for a in list(nxt):
        if a in seen:
            continue
        ring, p_ = [], a
        while p_ in nxt and p_ not in seen:
            seen.add(p_)
            ring.append(p_)
            p_ = nxt[p_]
        if len(ring) >= 4:
            for _ in range(rounds):                            # Chaikin: soft, drawn-looking edge
                Q = []
                for k_ in range(len(ring)):
                    p1, p2 = ring[k_], ring[(k_ + 1) % len(ring)]
                    Q += [(0.75 * p1[0] + 0.25 * p2[0], 0.75 * p1[1] + 0.25 * p2[1]),
                          (0.25 * p1[0] + 0.75 * p2[0], 0.25 * p1[1] + 0.75 * p2[1])]
                ring = Q
            ring = b8_dp_closed(ring, tol)
            if len(ring) >= 3 and abs(sum(ring[k_ - 1][0] * ring[k_][1] - ring[k_][0] * ring[k_ - 1][1]
                                          for k_ in range(len(ring)))) > 2.0 * min_area:
                rings.append(ring)
    return rings


# v8 place callouts (Aras 07:42-07:43 UTC, refs "Walk by the River" Christchurch + an expo masterplan): every place a
# white box with its category's colour, an icon, a short leader to a numbered dot; one route ties them; each colour
# has ONE meaning (shown in the key).
B8_ROUTE = "C2306E"          # the connecting route: riverside walk + bike lane, both banks, footbridges
B8_CAT = {"heritage": (u"Heritage and history", "8B3A3F", "heritage"),
          "water": (u"Water and wetland ecology", "3F6E7D", "water"),
          "garden": (u"Gardens, terraces, food", "5E6B3A", "plants"),
          "meet": (u"Squares, cafés, events", "B0603A", "hub"),
          "learn": (u"Learning and culture", "7A5C78", "people"),
          "sport": (u"Play and sport", "A87A22", "people"),
          "route": (u"Route: walk + bike lane, both banks, bridges", B8_ROUTE, "walk")}
B8_CAT_WORDS = (("heritage", (u"heritage", u"ulucami", u"trajaneum", u"arch", u"mosque", u"hamam", u"bath")),
                ("route", (u"footbridge", u"stepping", u"bed walk", u"canopied", u"walkway", u"entrance")),
                ("learn", (u"classroom", u"amphi", u"school", u"museum", u"workshop", u"library")),
                ("sport", (u"court", u"fitness", u"skate", u"play", u"dog", u"pump", u"sport")),
                ("meet", (u"café", u"cafe", u"market", u"event", u"picnic")),
                ("garden", (u"garden", u"allot", u"orchard", u"terrace", u"meadow", u"dry top", u"olive")),
                ("water", (u"basin", u"wetland", u"boardwalk", u"steps down", u"hide", u"arm", u"stream", u"water",
                           u"reed")),
                ("meet", (u"café", u"cafe", u"square", u"event", u"picnic", u"hub", u"market", u"plaza", u"seat")))
B8_ICON_WORDS = (("cafe", (u"café", u"cafe")), ("viewpoint", (u"hide", u"view")), ("market", (u"market",)),
                 ("reeds", (u"basin", u"reed", u"wetland")), ("olive", (u"orchard", u"olive", u"terrace")),
                 ("heritage", (u"heritage", u"ulucami", u"trajaneum", u"arch")),
                 ("walk", (u"walk", u"steps", u"stepping", u"footbridge", u"boardwalk")),
                 ("hub", (u"square", u"hub", u"plaza")), ("plants", (u"garden", u"allot", u"meadow")),
                 ("seating", (u"picnic", u"event", u"amphi")))
B8_CALL_T, B8_CALL_S, B8_CALL_I = 2.3, 1.95, 4.4     # mm: box title, second line, icon plate


def b8_cat(nm):
    s_ = (u"%s" % nm).lower()
    for cat, ws in B8_CAT_WORDS:
        if any(w in s_ for w in ws):
            return cat
    return "meet"


def b8_icon(nm, cat):
    s_ = (u"%s" % nm).lower()
    for ic, ws in B8_ICON_WORDS:
        if any(w in s_ for w in ws):
            return ic
    return B8_CAT[cat][2]


def b8_cat_key():
    return [(B8_CAT[c][0], B8_CAT[c][1]) for c in ("route", "heritage", "water", "garden", "meet", "learn", "sport")]


B8_POLLI = "DCD8AE"          # v8: pollinator meadow pads, a dry-flower tone (the plain meadow tone now = flat ground)
B8_SLOPE = (2.0, 5.0, 10.0, 20.0, 35.0)   # % ground slope class limits (Aras 07:43 UTC: greens by steepness, quiet)
B8_SLOPE_T = (0.10, 0.20, 0.30, 0.40, 0.50)   # share mixed from the meadow tone toward green_light, per class
B8_SLOPE_CELL = 4.0          # m grid; slope = contour interval x contour length / area over 5 x 5 cells (20 m)


def b8_slope_key():
    lims = (0.0,) + B8_SLOPE
    return [(u"Ground slope 0-2 % (or no survey contours)", B3_COL["meadow"])] + [
        (u"Ground slope %g-%g %%" % (lims[i + 1], lims[i + 2]) if i + 2 < len(lims) else
         u"Ground slope over %g %%" % lims[i + 1], b8_slope_tone(i)) for i in range(len(B8_SLOPE))]


def b8_slope_tone(i):
    return b3_mix(B3_COL["meadow"], "8C9969", B8_SLOPE_T[i])


def b8_slope_rings(sv, box):
    """[(class i, rings survey m)]: mean ground slope from the survey contours by the contour-density rule
    (tan = interval x contour length / area; 1 m contours, else 2 m) over a 20 x 20 m window; cells with no contour
    within 18 m count as flat (no data). Rings = the ground steeper than each class limit, rounded."""
    I, lines = 1.0, sv.get("contour1") or []
    if len(lines) < 50:
        I, lines = 2.0, sv.get("contour2") or []
    if not lines:
        return []
    c_ = B8_SLOPE_CELL
    x0, y0 = box[0] - 2 * c_, box[1] - 2 * c_
    nx, ny = int((box[2] - box[0]) / c_) + 5, int((box[3] - box[1]) / c_) + 5
    A = [[0.0] * ny for _ in range(nx)]
    for P in lines:
        for a, b in zip(P[:-1], P[1:]):
            L_ = math.hypot(b[0] - a[0], b[1] - a[1])
            n_ = max(1, int(L_ / (c_ / 2.0)))
            for t in range(n_):
                f_ = (t + 0.5) / n_
                i, j = int((a[0] + (b[0] - a[0]) * f_ - x0) / c_), int((a[1] + (b[1] - a[1]) * f_ - y0) / c_)
                if 0 <= i < nx and 0 <= j < ny:
                    A[i][j] += L_ / n_

    def box_sum(G, w):
        H_ = [[sum(col[max(0, j - w):j + w + 1]) for j in range(ny)] for col in G]
        return [[sum(H_[k][j] for k in range(max(0, i - w), min(nx, i + w + 1))) for j in range(ny)] for i in range(nx)]
    S = box_sum(A, 2)
    has = box_sum(A, 4)
    area = (5 * c_) ** 2
    F = [[(100.0 * I * S[i][j] / area if has[i][j] > 0 else 0.0) for j in range(ny)] for i in range(nx)]
    F = box_sum(F, 1)
    F = [[v / 9.0 for v in col] for col in F]
    for i in range(nx):
        F[i][0] = F[i][-1] = 0.0
    for j in range(ny):
        F[0][j] = F[-1][j] = 0.0
    return [(i, b8_iso(F, x0, y0, c_, lim, rounds=2, tol=0.4, min_area=4 * c_ * c_)) for i, lim in enumerate(B8_SLOPE)]


def b8_bush_one(pts, seed):
    """organic bush areas around shrub points [(x, y, r m)]: a smooth field of soft discs whose reach wobbles by a
    bounded smooth noise, cut at one level (marching squares), rounded (Chaikin) -> closed rings in the same metres"""
    if not pts:
        return []
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, 6.283) for _ in range(6)]
    c_ = B8_BUSH_CELL
    R = [(x, y, r * B8_BUSH_GROW * (1.0 + B8_BUSH_WOBBLE * math.sin(x * 0.21 + ph[0]) * math.cos(y * 0.17 + ph[1])))
         for x, y, r in pts]
    rmax = max(r for _, _, r in R)
    hsh = {}
    for i, (x, y, r) in enumerate(R):
        hsh.setdefault((int(x // (2 * rmax)), int(y // (2 * rmax))), []).append(i)
    x0 = min(x - r for x, y, r in R) - 2 * c_
    y0 = min(y - r for x, y, r in R) - 2 * c_
    nx = int((max(x + r for x, y, r in R) + 2 * c_ - x0) / c_) + 2
    ny = int((max(y + r for x, y, r in R) + 2 * c_ - y0) / c_) + 2

    def fld(i, j):
        x, y = x0 + i * c_, y0 + j * c_
        w_ = 0.12 * (math.sin(x * 0.9 + ph[2]) * math.sin(y * 0.8 + ph[3]) + math.sin(x * 0.37 + y * 0.41 + ph[4]))
        v = 0.0
        hx, hy = int(x // (2 * rmax)), int(y // (2 * rmax))
        for a_ in (hx - 1, hx, hx + 1):
            for b_ in (hy - 1, hy, hy + 1):
                for k_ in hsh.get((a_, b_), ()):
                    px, py, r = R[k_]
                    d2 = ((x - px) ** 2 + (y - py) ** 2) / (r * r)
                    if d2 < 1.0:
                        v += (1.0 - d2) ** 2
        return v + w_ * min(v, 1.0)
    F = [[fld(i, j) for j in range(ny)] for i in range(nx)]
    return b8_iso(F, x0, y0, c_, 0.5)


def b8_put_tree(pg, key, x, y, r, seed, eid):
    """one tree as its own sub-group: the traced symbol if there is one, else the plant module's symbol"""
    sid = b8_sym_for(key, seed)
    pg.group("trees", eid)
    if sid:
        pg.items.append(("sym", sid, x, y, r, None))
    else:
        pl23_put(pg, _B19_PLA_ASSET(key, x, y, 1.0, crown_m=2.0 * r, seed=seed, distinct=True))
    pg.endgroup()
    return sid


_b8_blit0 = blit


def blit(dst, src, dx, dy):
    """v8: blit + the "sym" items (moved with the rest, order kept)"""
    if not any(it[0] in ("sym", "pat") for it in src.items):
        return _b8_blit0(dst, src, dx, dy)
    for it in src.items:
        if it[0] == "sym":
            dst.items.append(("sym", it[1], it[2] + dx, it[3] + dy) + tuple(it[4:]))
        elif it[0] == "pat":                              # ("pat", tile id, rings, alpha, variant)
            dst.items.append(("pat", it[1], [[(p[0] + dx, p[1] + dy) for p in r_] for r_ in it[2]]) + tuple(it[3:]))
        else:
            tmp = Page(src.W, src.H)
            tmp.items = [it]
            _b8_blit0(dst, tmp, dx, dy)


def _b8_sym_stream(bands):
    o = []
    for b_ in bands:
        r, g, b = hex_rgb(b_["fill"])
        o.append("{} {} {} rg".format(_f(r), _f(g), _f(b)))
        for R in b_["rings"]:
            if len(R) < 3:
                continue
            o.append("{} {} m".format(_f(R[0][0]), _f(R[0][1])))
            o.extend("{} {} l".format(_f(p[0]), _f(p[1])) for p in R[1:])
            o.append("h")
        o.append("f*")
    return "\n".join(o).encode("latin-1")


B8_PDF_TOL = 0.02            # mm on paper: vertices closer than this to the straight run are dropped in the PDF
                             # (a 1,200 dpi printer dot is 0.021 mm, so nothing visible changes); coordinates 0.01 mm


def _b8_r2(P):
    return [(round(p[0], 2), round(p[1], 2)) for p in P]


def _b8_lean(it):
    """the PDF copy of a drawn item: invisible vertices dropped (B8_PDF_TOL), points to 0.01 mm"""
    kd = it[0]
    if kd == "poly":
        return (kd, [_b8_r2(b8_dp_closed(r_, B8_PDF_TOL) if len(r_) > 6 else r_) for r_ in it[1]]) + tuple(it[2:])
    if kd == "line":
        return (kd, _b8_r2(b8_dp(it[1], B8_PDF_TOL) if len(it[1]) > 3 else it[1])) + tuple(it[2:])
    return it


def b8_write_pdf(pg, path, title):
    """v8 writer: kinds and elements as nested form objects (Illustrator opens them as groups: Sheet > kind >
    element), each traced tree symbol stored once and placed by reference, images embedded once. Same page, fonts,
    opacity steps (/A01../A99) and vector drawing (page_stream) as write_pdf."""
    objs = []

    def add(b):
        objs.append(b)
        return len(objs)
    font = pdf_fonts(add, ("R", "B"))
    gs = [add("<< /Type /ExtGState /ca {0} /CA {0} >>".format(_f(i / 100.0)).encode("latin-1")) for i in range(1, 100)]
    gs_res = " ".join("/A{:02d} {} 0 R".format(i + 1, o_) for i, o_ in enumerate(gs))
    pages_id = add(b"")
    xo_dict = add(b"")                                    # one shared /XObject dictionary (filled at the end)
    pat_dict = add(b"")                                   # v8: bush hatch tiling patterns (filled at the end)
    xo = []                                               # [(name, id)] images + symbols
    res = "{} 0 R".format(add("<< /Font << /F1 {} 0 R /F2 {} 0 R >> /ExtGState << {} >> /XObject {} 0 R /Pattern {} 0 R >>".format(
        font[0], font[1], gs_res, xo_dict, pat_dict).encode("latin-1")))     # one shared resource dictionary, by reference
    img_names, sym_names, tile_names, pat_names, pats = {}, {}, {}, {}, []
    lib = b8_sym_lib()
    tiles = b8_tiles()
    PTk = 2.834646
    Wp, Hp = pg.W * PTk, pg.H * PTk

    def form(stream, bbox=None):
        data = zlib.compress(stream, 6)
        bb = bbox or (0.0, 0.0, Wp, Hp)
        return add(("<< /Type /XObject /Subtype /Form /BBox [{} {} {} {}] /Resources {} /Length {} "
                    "/Filter /FlateDecode >>\nstream\n").format(_f(bb[0]), _f(bb[1]), _f(bb[2]), _f(bb[3]), res,
                                                                len(data)).encode("latin-1") + data + b"\nendstream")

    def sym_name(sid):
        if sid not in sym_names:
            oid = form(_b8_sym_stream(lib.get(sid, [])), (-1.0, -1.0, 1.0, 1.0))
            sym_names[sid] = "Sy%d" % (len(sym_names) + 1)
            xo.append((sym_names[sid], oid))
        return sym_names[sid]

    def pat_name(hid, var):
        """the tiling pattern of bush tile hid, variant var (0-3: turned 90 deg steps and shifted, so neighbouring
        bushes don't repeat the same patch); the tile itself is ONE form object shared by all four"""
        if (hid, var) not in pat_names:
            t_ = tiles[hid]
            P = float(t_["period_mm"])
            if hid not in tile_names:
                tile_names[hid] = "Ht%d" % (len(tile_names) + 1)
                xo.append((tile_names[hid], form(_b8_sym_stream(t_["bands"]), (0.0, 0.0, P, P))))
            a_ = var * math.pi / 2.0
            ca, sa = math.cos(a_) * PTk, math.sin(a_) * PTk
            body = ("q /%s Do Q" % tile_names[hid]).encode("latin-1")
            oid = add(("<< /Type /Pattern /PatternType 1 /PaintType 1 /TilingType 1 /BBox [0 0 {0} {0}] /XStep {0} "
                       "/YStep {0} /Resources {1} /Matrix [{2} {3} {4} {5} {6} {7}] /Length {8} >>\nstream\n").format(
                _f(P), res, "%.6f" % ca, "%.6f" % sa, "%.6f" % -sa, "%.6f" % ca, "%.4f" % (var * 0.37 * P * PTk), "%.4f" % (var * 0.61 * P * PTk),
                len(body)).encode("latin-1") + body + b"\nendstream")
            pat_names[(hid, var)] = "Ph%d" % (len(pat_names) + 1)
            pats.append((pat_names[(hid, var)], oid))
        return pat_names[(hid, var)]

    class _Run(object):
        pass

    def stream_of(items):
        parts, run, depth = [], [], [0]

        def flush():
            if run:
                r = _Run()
                r.W, r.H, r.items = pg.W, pg.H, [_b8_lean(i_) for i_ in run]
                parts.append(b"q\n" + page_stream(r) + b"\nQ")
                del run[:]
        for it in items:
            kd = it[0]
            if kd == "clip":                              # v8.0: clips written here, balanced q/Q, so symbols,
                flush()                                   # patterns and images placed between stay in place
                o_ = ["q"]
                for R in it[1]:
                    if len(R) >= 3:
                        o_.append("{} {} m".format(_f(R[0][0] * PTk), _f(R[0][1] * PTk)))
                        o_.extend("{} {} l".format(_f(p_[0] * PTk), _f(p_[1] * PTk)) for p_ in R[1:])
                        o_.append("h")
                o_.append("W* n")
                parts.append("\n".join(o_).encode("latin-1"))
                depth[0] += 1
            elif kd == "unclip":
                flush()
                if depth[0] > 0:
                    parts.append(b"Q")
                    depth[0] -= 1
            elif kd == "sym":
                flush()
                if it[1] not in lib:
                    continue
                g = _gs(it[5] if len(it) > 5 else None)
                parts.append(("q {0} 0 0 {0} 0 0 cm {1}{2} 0 0 {2} {3} {4} cm /{5} Do Q".format(
                    "2.834646", (g + " gs ") if g else "", _f(it[4]), _f(it[2]), _f(it[3]), sym_name(it[1]))
                              ).encode("latin-1"))
            elif kd == "pat":
                flush()
                if it[1] not in tiles:
                    continue
                g = _gs(it[3] if len(it) > 3 else None)
                o_ = ["q {0} 0 0 {0} 0 0 cm".format("2.834646")]
                if g:
                    o_.append("{} gs".format(g))
                o_.append("/Pattern cs /{} scn".format(pat_name(it[1], (it[4] if len(it) > 4 else 0) % 4)))
                for R in it[2]:
                    if len(R) >= 3:
                        R = _b8_r2(b8_dp_closed(R, B8_PDF_TOL))
                        o_.append("{} {} m".format(_f(R[0][0]), _f(R[0][1])))
                        o_.extend("{} {} l".format(_f(p_[0]), _f(p_[1])) for p_ in R[1:])
                        o_.append("h")
                o_.append("f* Q")
                parts.append("\n".join(o_).encode("latin-1"))
            elif kd == "image":
                flush()
                x, y, w, h, p = it[1:6]
                alpha = it[6] if len(it) > 6 else None
                flip = it[7] if len(it) > 7 else False
                clip = it[8] if len(it) > 8 else None
                if p not in img_names:
                    oid = _mp_image_obj(p, add)
                    img_names[p] = None if oid is None else "Im%d" % (len(img_names) + 1)
                    if oid is not None:
                        xo.append((img_names[p], oid))
                if img_names[p] is None or w <= 0 or h <= 0:
                    continue
                ops = ["q {0} 0 0 {0} 0 0 cm".format("2.834646")]
                g = _gs(alpha)
                if g:
                    ops.append("{} gs".format(g))
                if clip:
                    ops.append("{} {} {} {} re W n".format(_f(clip[0]), _f(clip[1]), _f(clip[2] - clip[0]),
                                                          _f(clip[3] - clip[1])))
                ops.append("{} 0 0 {} {} {} cm /{} Do Q".format(_f(-w if flip else w), _f(h), _f(x + w if flip else x),
                                                               _f(y), img_names[p]))
                parts.append(" ".join(ops).encode("latin-1"))
            else:
                run.append(it)
        flush()
        parts += [b"Q"] * depth[0]
        return b"\n".join(parts)
    # ---- split the items into kinds > elements (draw order kept; clips carried into every element they span)
    elems, stack, clips = [], [], []
    cur_key, cur_items, cur_pre = None, [], []

    def close_elem():
        if cur_items:
            body = list(cur_pre) + list(cur_items) + [("unclip",)] * len(clips)
            elems.append((cur_key, body))
    for it in pg.items:
        kd = it[0]
        if kd == "grp":
            if it[1] is None:
                if stack:
                    stack.pop()
            else:
                stack.append((it[1], it[2] if len(it) > 2 and it[2] else it[1]))
            key = ((stack[0][0], stack[-1][1]) if stack else ("sheet", u"sheet"))
            if key != cur_key:
                close_elem()
                cur_key, cur_items, cur_pre = key, [], [("clip", c_) for c_ in clips]
            continue
        if cur_key is None:
            cur_key, cur_items, cur_pre = ("sheet", u"sheet"), [], [("clip", c_) for c_ in clips]
        if kd == "clip":
            clips.append(it[1])
        elif kd == "unclip":
            if clips:
                clips.pop()
        cur_items.append(it)
    close_elem()
    page_parts, kind_cur, kind_buf = [], None, []

    def close_kind():
        if kind_buf:
            oid = form(b"\n".join(kind_buf))
            nm = "K%d" % (len(xo) + 1)
            xo.append((nm, oid))
            page_parts.append(b"/G69 << /Name " + pdf_str(u"%s" % kind_cur) + b" >> BDC /" + nm.encode() + b" Do EMC")
    for (kind, eid), body in elems:
        if kind != kind_cur:
            close_kind()
            kind_cur, kind_buf = kind, []
        oid = form(stream_of(body))
        nm = "E%d" % (len(xo) + 1)
        xo.append((nm, oid))
        kind_buf.append(b"/G69 << /Name " + pdf_str(u"%s" % eid) + b" >> BDC /" + nm.encode() + b" Do EMC")
    close_kind()
    objs[xo_dict - 1] = ("<< " + " ".join("/{} {} 0 R".format(n_, o_) for n_, o_ in xo) + " >>").encode("latin-1")
    objs[pat_dict - 1] = ("<< " + " ".join("/{} {} 0 R".format(n_, o_) for n_, o_ in pats) + " >>").encode("latin-1")
    data = zlib.compress(b"\n".join(page_parts), 6)
    cid = add(b"<< /Length " + str(len(data)).encode() + b" /Filter /FlateDecode >>\nstream\n" + data +
              b"\nendstream")
    kid = add("<< /Type /Page /Parent {} 0 R /MediaBox [0 0 {} {}] /Contents {} 0 R /Resources {} >>".format(
        pages_id, "%.4f" % Wp, "%.4f" % Hp, cid, res).encode("latin-1"))
    objs[pages_id - 1] = "<< /Type /Pages /Kids [{} 0 R] /Count 1 >>".format(kid).encode("latin-1")
    cat = add("<< /Type /Catalog /Pages {} 0 R >>".format(pages_id).encode("latin-1"))
    info = add(b"<< /Title " + pdf_str(title) + b" /Producer " + pdf_str(VERSION) + b" >>")
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offs = []
    for i, b in enumerate(objs):
        offs.append(len(out))
        out += "{} 0 obj\n".format(i + 1).encode() + b + b"\nendobj\n"
    x = len(out)
    out += "xref\n0 {}\n0000000000 65535 f \n".format(len(objs) + 1).encode()
    for o_ in offs:
        out += "{:010d} 00000 n \n".format(o_).encode()
    out += "trailer\n<< /Size {} /Root {} 0 R /Info {} 0 R >>\nstartxref\n{}\n%%EOF\n".format(
        len(objs) + 1, cat, info, x).encode()
    with open(path, "wb") as fh:
        fh.write(bytes(out))
    return dict(elements=len(elems), symbols=len(sym_names), images=len(img_names), tiles=len(tile_names))


def b8_save(pg, folder, name, title, notes):
    path = os.path.join(folder, name)
    try:
        st = b8_write_pdf(pg, path, title)
    except (IOError, OSError):
        path = os.path.join(folder, name.replace(".pdf", datetime.datetime.now().strftime("_%H%M%S.pdf")))
        st = b8_write_pdf(pg, path, title)
    notes.append(u"PDF groups: %d elements in their category groups; %d tree symbols + %d bush hatch tiles stored once; "
                 u"%d images; %.1f MB" % (st["elements"], st["symbols"], st["tiles"], st["images"],
                                          os.path.getsize(path) / 1048576.0))
    return path


def b19_page(C, site, study, scale, warn):
    """v6 sheet (Aras 6 Nov 00:18-00:25, previews/V6_PLAN.md F1-F12): the project's own elements, each drawn as
    what it is, in B19 language. Returns (Page, log notes)."""
    t0 = time.time()
    k = 1000.0 / scale
    # v8 (Aras 10:07 TR "keep the masterplan at site_alan"): the sheet IS the site_alan rectangle, turned so its long
    # side lies flat (upstream on the left); the north arrow turns with it
    rot = b8_site_turn(site)
    ca_, sa_ = math.cos(rot), math.sin(rot)
    ox_, oy_ = site[0][0], site[0][1]
    Rt = lambda p: (ox_ + ca_ * (p[0] - ox_) - sa_ * (p[1] - oy_), oy_ + sa_ * (p[0] - ox_) + ca_ * (p[1] - oy_))
    Ri = lambda p: (ox_ + ca_ * (p[0] - ox_) + sa_ * (p[1] - oy_), oy_ - sa_ * (p[0] - ox_) + ca_ * (p[1] - oy_))
    x0, y0, x1, y1 = bbox([Rt(p) for p in site])
    dw, dh = (x1 - x0) * k, (y1 - y0) * k

    def T(p):
        q = Rt(p)
        return ((q[0] - x0) * k, (q[1] - y0) * k)
    TL = lambda P: [T(p) for p in P]
    ins = lambda p: any(pip(p[0], p[1], R) for R in study)
    sub = Page(dw, dh)
    st = [TL(R) for R in study if len(R) >= 3]
    notes, flags, n_el, n_sp = [], [], {}, {}
    sv = C.survey if hasattr(C, "survey") else {}
    wb_ = bbox(site)                                      # world box (hit tests stay in survey m)
    box = (wb_[0] - 60.0, wb_[1] - 60.0, wb_[2] + 60.0, wb_[3] + 60.0)
    sv = b8_clean_survey(sv, box, notes)                  # v8: survey linework cleaned (design unchanged)
    road_names, el_names, stones, benches = [], [], [], []
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
    z_idx = b3_grid(b3_segs(study, True))
    for h, br, nm, P, w, sn in ways:
        if not hit(bbox(P), box):
            continue
        inz = sum(1 for q in P if ins(q)) >= len(P) / 2.0
        Pd_ = b3_dense(P, 6.0)
        if inz and sum(1 for q in Pd_ if b3_dist(z_idx, q, 12.0) < w / 2.0 + 4.0) >= 0.6 * len(Pd_):
            inz = False                                   # v7 R7: a street on the zone line stays outside
        if inz and h in B3_DROP_IN:
            continue                                      # tracks, footways ... inside the zone: the walks replace them
        m = rd_of(P) if inz else None
        car = bool(m and m[1]["name"] in B6_CAR_ROADS) or (br and h in B3_VEHICLE)
        vis.append(dict(h=h, br=br, nm=nm, P=P, w=w, inz=inz, car=car, rd=m[1]["name"] if m else None, sn=sn))
    car_ways = [x for x in vis if x["car"]]
    # ================================================================ water (F3)
    chan_raw = b6_channel(C, car_ways)
    chan = [b3_chaikin_closed(R[::2], 1) for R in chan_raw if len(R) >= 9]   # 4 m stations, corners cut < 0.5 m
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

    def on_hard(p, r0=0.0, lines_only=False):
        for i_ in h_idx.get((int(p[0] // 40), int(p[1] // 40)), ()):
            bb_, P, r_ = hard[i_]
            if lines_only and len(P) > 3 and P[0] == P[-1]:
                continue
            if len(P) > 3 and P[0] == P[-1] and bb_[0] <= p[0] <= bb_[2] and bb_[1] <= p[1] <= bb_[3] and \
                    pip(p[0], p[1], P):
                return True                               # inside a square or pad
            for a, b in zip(P[:-1], P[1:]):
                if seg_dist(p[0], p[1], a, b) < r_ + r0:
                    return True
        return False
    lc_tr = b8_veg_rings("trees") or b7_lc_rings("trees")   # v8: 2023 imagery (0.5 m) first, WorldCover 2021
    notes.append(u"tree cover: %s" % (u"traced from Maxar 2023-03-01 imagery (0.5 m)" if b8_veg_rings("trees")
                                      else u"ESA WorldCover 2021 (10 m)"))
    lc_box = [(bbox(R), R) for R in lc_tr if hit(bbox(R), box)]
    lc_idx = {}
    for i_, (bb_, R) in enumerate(lc_box):
        for gi in range(int(bb_[0] // 40), int(bb_[2] // 40) + 1):
            for gj in range(int(bb_[1] // 40), int(bb_[3] // 40) + 1):
                lc_idx.setdefault((gi, gj), []).append(i_)
    in_trees = lambda p: sum(1 for i_ in lc_idx.get((int(p[0] // 40), int(p[1] // 40)), ())
                             if lc_box[i_][0][0] <= p[0] <= lc_box[i_][0][2] and lc_box[i_][0][1] <= p[1] <= lc_box[i_][0][3]
                             and pip(p[0], p[1], lc_box[i_][1])) % 2 == 1
    free = lambda p, r=0.0: ins(p) and not in_wet(p) and not on_hard(p, r) and not in_bld(p, r) and not in_trees(p)
    with mpx_grp(sub, "trees", u"green around the zone (2023 imagery, else WorldCover 2021), light"):
        Ps = b8_ctx_rings([TL(b3_chaikin_closed(R, 2)) for R in b8_veg_rings("grass") if len(R) >= 3 and hit(bbox(R), box)])
        if Ps:                                            # v8: context tint only; inside, the zone's ground covers it
            sub.poly(Ps, fill=b3_mix(B3_COL["meadow"], "FFFFFF", 0.6))
        Ps = b8_ctx_rings([TL(b3_chaikin_closed(R, 2)) for bb_, R in lc_box if len(R) >= 3])   # v8: rounded, lean
        if Ps:
            sub.poly(Ps, fill=b3_mix(B3_COL["tree1"], "FFFFFF", 0.72))
    # ================================================================ 1 ground: gradient, height steps, contours
    sub.clip(st)
    with mpx_grp(sub, "ground", u"open meadow"):
        sub.poly([rect(0.0, 0.0, dw, dh)], fill=B3_COL["meadow"])
        b3_dots(sub, (0.0, 0.0, dw, dh), 7.0 * k, B3_COL["lawn_dk"], st)
    for i_, rings_ in b8_slope_rings(sv, box):           # v8: ground greens by slope (was: by distance to water)
        Ps = [TL(R) for R in rings_ if len(R) >= 3]
        if Ps:
            with mpx_grp(sub, "ground", u"ground slope over %g %%" % B8_SLOPE[i_]):
                sub.poly(Ps, fill=b8_slope_tone(i_))
            cnt("slope areas over %g %%" % B8_SLOPE[i_], len(Ps))
    for t_, Ls in C.eco:                                  # v7 R1: the green corridor, one band both banks
        if abs(t_ - B7_CORRIDOR_T) < 0.5:
            Ps = [TL(R) for R in Ls if len(R) >= 3]
            if Ps:
                with mpx_grp(sub, "ground", u"green corridor: open ground within %g m of the water" % t_):
                    sub.poly(Ps, fill=B3_COL["corridor"], alpha=0.55)   # v8: no ticks (v6 look)
        pass                                              # v7 (05:42): no interpolated height cells
    with mpx_grp(sub, "ground", u"survey contours 2 m / 5 m / 10 m (EGRI_2M, EGRI_5M, EGRI_10M), shaded on the low side"):
        for role, lw_, col_ in (("contour2", 0.05, B3_COL["contour"]), ("contour", 0.07, B3_COL["contour"]),
                                ("contour10", 0.09, B3_COL["contour_dk"])):   # v8: v6 look; 1 m lines left out
            for P in sv.get(role, []):                    # (0.25 mm apart at 1:4,000: they read as a dark tone)
                if len(P) >= 2 and hit(bbox(P), box):
                    sub.line(TL(P), col_, lw_)
                    sub.line(b3_off(TL(P), 0.12), B3_COL["contour_dk"], 0.05, alpha=0.4)
                    cnt("survey contour lines")
        for P in sv.get("slope", []):                     # SEV_SEV: surveyed slope lines, light (v8)
            if len(P) >= 2 and hit(bbox(P), box):
                sub.line(TL(P), B3_COL["contour"], 0.05, [0.5, 0.4], cap=0)
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
                sub.poly([TL(b3_band(P, [3.4] * len(P)))], fill=B3_COL["water_lt"], stroke=B3_COL["wall"], lw=0.08)
                sub.line(TL(P), B3_COL["water"], 0.25, [1.6, 0.9], cap=0)
                for q in b3_dense(P, 30.0)[1:-1]:
                    x_, y_ = T(q)
                    sub.poly([rect(x_ - 0.5, y_ - 0.5, x_ + 0.5, y_ + 0.5)], fill=B3_COL["deck"],
                             stroke=B3_COL["wall"], lw=0.06)
                cnt("hidden stream")
    # ================================================================ 4 streets (F2)
    n_rd = {}
    for x in vis:
        P, w, h = x["P"], x["w"], x["h"]
        if not x["br"] and not x["car"] and any(in_chan(q) for q in P):   # nothing over the water but bridges
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
            if kind == "ctx":                             # v8 (Aras 09:25 TR "recover the context"): v6 street bands,
                Pd = b3_dense(P, 4.0)                     # data first (Aras 09:27 TR): on the survey's road edges
                if x["sn"]:                               # (midline + width between them) where the .3dm has them;
                    W_ = [w] * len(Pd)                    # else OSM width, narrowed wherever a building is near
                    n_rd["context street on survey edges"] = n_rd.get("context street on survey edges", 0) + 1
                else:
                    W_ = [max(2.0, min(w, 2.0 * (b3_dist(b_idx, q, w) - 0.6))) for q in Pd]
                    n_rd["context street at OSM width (no survey edges)"] = n_rd.get(
                        "context street at OSM width (no survey edges)", 0) + 1
                with mpx_grp(sub, "roads", u"street %s" % (x["nm"] or h)):
                    sub.poly([TL(b3_band(Pd, W_))], fill=B3_COL["ctx_road"])
                continue
            if not x["sn"] and not x["br"]:               # v8: no survey edge pair: drawn at its OSM width (as v6)
                n_rd["street at OSM width (no survey edge pair)"] = n_rd.get("street at OSM width (no survey edge pair)", 0) + 1
            if x["br"]:
                continue                                  # v7 R10: drawn below, two carriageways as one deck
            if kind == "car":                              # carriageway + pavements both sides + direction arrows
                ww = w + 2.0 * B6_PAVEMENT
                with mpx_grp(sub, "roads", u"car road %s: carriageway + pavements" % x["rd"]):
                    sub.poly([TL(b3_band(P, [ww + 0.4] * len(P)))], fill=B3_COL["paving_edge"])
                    sub.poly([TL(b3_band(P, [ww] * len(P)))], fill=B3_COL["paving"])
                    sub.poly([TL(b3_band(P, [w] * len(P)))], fill=B3_COL["asphalt"], stroke=B3_COL["kerb"], lw=0.08)
                    sub.line(TL(P), "FFFFFF", 0.1, [1.2, 1.2], cap=0)
                    b6_arrows(sub, P, T, k, w)
                wet_near = lambda q: any(in_chan((q[0] + dx_, q[1] + dy_)) for dx_, dy_ in
                                         ((3.0, 0.0), (-3.0, 0.0), (0.0, 3.0), (0.0, -3.0)))
                with mpx_grp(sub, "water", u"retaining wall: car road at the water"):
                    for sg_ in (1.0, -1.0):
                        E_ = b3_off(b3_dense(P, 3.0), sg_ * (ww / 2.0 + 0.3))
                        for Q_ in b6_split(E_, lambda q: not wet_near(q)):
                            sub.line(TL(Q_), B3_COL["wall"], 0.25)
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
    for P, w in b7_merge_bridges([x for x in vis if x["br"]]):
        with mpx_grp(sub, "roads", u"road bridge"):
            sub.poly([TL(b3_band(P, [w + 1.2] * len(P)))], fill=B3_COL["deck_edge"])
            sub.poly([TL(b3_band(P, [w] * len(P)))], fill=B3_COL["deck"])
            sub.line(TL(P), B3_COL["joint"], 0.08, [1.2, 1.2], cap=0)
        add_hard(P, w / 2.0 + B3_TREE_CLEAR)
        cnt("road bridge")
    her_c = [inner_pt(H) for H in her]
    near_her = lambda P: any(math.hypot(q[0] - c_[0], q[1] - c_[1]) < 40.0 for q in P[::max(1, len(P) // 6)]
                             for c_ in her_c)
    with mpx_grp(sub, "roads", u"survey road + kerb edges outside the zone (Bergama_Altlik.3dm, as drawn)"):
        for role in ("road", "kerb"):                     # v8: inside the zone the design draws the streets; the
            for P in sv.get(role, []):                    # old edges there were the dark stray lines of v7
                if len(P) >= 2 and hit(bbox(P), box) and not any(ins(q) for q in P):
                    sub.line(TL(P), B3_COL["bld_ctx_edge"], 0.05)
    with mpx_grp(sub, "annotations", u"survey walls (SINIR_DUVAR) + historic wall (SINIR_TARIHI_SUR)"):
        for P in sv.get("wall", []):                      # v8: inside the zone only heritage courtyard walls
            if len(P) < 2 or not hit(bbox(P), box):
                continue
            if not any(ins(q) for q in P):
                sub.line(TL(P), B3_COL["bld_ctx_edge"], 0.05)
            elif near_her(P):
                sub.line(TL(P), B3_COL["wall"], 0.1)
        for P in sv.get("histwall", []):
            if len(P) >= 2 and hit(bbox(P), box):
                sub.line(TL(P), B3_COL["heritage"], 0.35, [1.2, 0.5], cap=0)
                cnt("historic wall lines")
    street_pts = [q for x in vis if x["inz"] or any(ins(q) for q in x["P"]) for q in b3_dense(x["P"], 6.0)
                  if not in_chan(q)]
    # ================================================================ 5 walks + bike lane, continuous (F4)
    walks = b6_walks(C, cl, in_chan)                      # [(P, bank)] one continuous line per stretch and bank
    walks3 = [(P, bank, [chain_at(C.ref, q)[0] for q in P]) for P, bank in walks]
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
    # v7 R6 (00:56): stepping stones where a bed walk ends at shallow water (crossing <= 14 m)
    for P in beds:
        for e in (P[0], P[-1]):
            ch_ = chain_at(C.ref, e)[0]
            s_r = arclen(C.ref)
            (rx_, ry_), (ux_, uy_) = at_len(C.ref, s_r, max(0.0, min(s_r[-1], ch_)))
            nx_, ny_ = -uy_, ux_
            if (e[0] - rx_) * nx_ + (e[1] - ry_) * ny_ > 0:
                nx_, ny_ = -nx_, -ny_                     # toward the far bank
            t_, a_, b_ = 0.0, None, None
            while t_ < 30.0:
                q_ = (e[0] + nx_ * t_, e[1] + ny_ * t_)
                if in_chan(q_) and a_ is None:
                    a_ = q_
                if a_ is not None and not in_chan(q_):
                    b_ = q_
                    break
                t_ += 0.5
            if a_ and b_ and math.hypot(b_[0] - a_[0], b_[1] - a_[1]) <= 14.0 and \
                    all(math.hypot(a_[0] - s0[0], a_[1] - s0[1]) > 40.0 for s0, s1 in stones):
                stones.append((a_, b_))
                el_names.append((u"Stepping stones", a_))
    # ================================================================ 7 hub squares, freed squares, programme (F6, F11)
    pads = []                                             # (kind, name, ring or centre, extra)
    for hb in C.hubs:
        for R in hb.get("square") or []:
            if len(R) >= 3 and any(ins(q) for q in R):
                pads.append(("square", None, R))
                add_hard(R + R[:1], 1.0)
    # v7 R7 (Aras 00:54-00:56): the freed Ulucami ground = ONE square inside the zone, shade only along its edge
    fr = [b3_hull(R) for R in b_rm if math.hypot(inner_pt(R)[0] - B3_ULU_XY[0], inner_pt(R)[1] - B3_ULU_XY[1]) < B3_ULU_R]
    fr = [H for H in fr if ins(inner_pt(H)) and not in_wet(inner_pt(H))]
    pad_trees = []
    if fr:
        sub.clip(st)
        with mpx_grp(sub, "hubs", u"Ulucami Önü square on the freed ground"):
            for H in fr:
                sub.poly([TL(b3_band(H + H[:1], [5.0] * (len(H) + 1)))], fill=B3_COL["paving"])
                sub.poly([TL(H)], fill=B3_COL["paving"])
            for H in fr:
                b3_grid_fill(sub, TL(H), B3_COL["joint"], 3.0 * k * 4.0)
        with mpx_grp(sub, "water", u"Selinos (over the square edge)"):
            sub.clip([TL(b3_band(H + H[:1], [5.2] * (len(H) + 1))) for H in fr] + [TL(H) for H in fr])
            for R in chan:
                sub.poly([TL(R)], fill=B3_COL["water"])
            sub.unclip()
        sub.unclip()
        for H in fr:
            add_hard(H + H[:1], 2.5)
        HH = b3_hull([q for H in fr for q in H])          # the square's edge: one shade row on the outline
        s_ = arclen(HH + HH[:1])
        for i_ in range(int(s_[-1] // 9.0)):
            q_, (ux_, uy_) = at_len(HH + HH[:1], s_, 9.0 * i_)
            pad_trees.append((q_, "plane", 9.0, u"square shade"))
        el_names.append((u"Ulucami Önü square", inner_pt(max(fr, key=lambda H: abs(area2(H))))))
        cnt("freed square pieces", len(fr))
    prog = [x for x in b6_programme(C, ins) if x[0] != "seats"]
    placed_pads, reach_kinds = [], {}
    reaches = b7_reaches(C, ins, [inner_pt(R) for R in b_her], widen, free)
    r_of = lambda p: next((i for i, (a, b, th) in enumerate(reaches) if a <= chain_at(C.ref, p)[0] < b), 0)
    for kind, nm_, p in prog:
        if kind == "subhub":                              # in the bed: dry ground, not the water
            q = b6_free_spot(p, lambda u, r: ins(u) and not in_chan(u) and not in_bld(u, r) and not on_hard(u, r),
                             45.0, 3.0)
        else:
            q = b6_free_spot(p, free, 40.0, 6.0)
        if q is None:
            flags.append(u"programme %s: no free ground within 40 m of its place" % nm_)
            continue
        R = b6_pad(kind, q, wp)
        pads.append((kind, nm_, R))
        placed_pads.append((q, kind))
        reach_kinds.setdefault(r_of(q), set()).add(kind)
        add_hard(R + R[:1], 1.5)
        if kind in ("hub_sq", "cafe"):
            a_, u_, v_, L_, W_ = b6_rect_axes(R)
            for s_ in (3.0, L_ - 3.0):
                pad_trees.append((b6_pt(a_, u_, v_, s_, W_ - 2.5), "plane", 7.0, u"square shade"))
        el_names.append((u"%s · %d m²" % (nm_, int(round(abs(area2(R)), -1))) if kind not in ("subhub",) else nm_, q))
        cnt(kind)
    box_ok = lambda R: True
    for i_, (a_c, b_c, th) in enumerate(reaches):        # R2 + R3: each reach's theme, lined up along the walk
        items = [it for it in B7_THEMES[th][1] if it[0] not in reach_kinds.get(i_, set())]
        for kind, nm_, R, link in b7_strip(walks3, (a_c, b_c), items, free, ins, box_ok):
            pads.append((kind, nm_, R))
            add_hard(R + R[:1], 1.5)
            bands.append((link, 2.4, B3_COL["paving"], u"link"))
            add_hard(link, 1.2 + B3_TREE_CLEAR)
            c_ = (sum(q[0] for q in R) / 4.0, sum(q[1] for q in R) / 4.0)
            el_names.append((u"%s · %d m²" % (nm_, int(round(abs(area2(R)), -1))), c_))   # real size shown
            cnt(kind)
            if kind == "orchard":
                a_, u_, v_, L_, W_ = b6_rect_axes(R)
                t_ = 4.0
                while t_ < W_ - 2.0:
                    s2 = 4.0
                    while s2 < L_ - 2.0:
                        pad_trees.append((b6_pt(a_, u_, v_, s2, t_), "olive", 5.5, u"orchard rows"))
                        s2 += 7.0
                    t_ += 7.0
    for q, kind, nm_ in [x for x in b6_activity_spots(C, free, wp, widen, placed_pads, ins) if x[1] == "hide"]:
        R = b6_pad(kind, q, wp)
        pads.append((kind, nm_, R))
        el_names.append((nm_, q))
        cnt(kind)
    # heritage trail (Q3, 00:25): the kept heritage buildings in stream order, joined along the walks, numbered
    trail = []
    for p in sorted([inner_pt(R) for R in b_her], key=lambda p: chain_at(C.ref, p)[0]):
        if all(math.hypot(p[0] - q[0], p[1] - q[1]) > 50.0 for q in trail):   # one stop per 50 m
            trail.append(p)
    # ================================================================ 8 edge threshold (F10)
    entr = b6_entrances(study, vis, ins)
    hedge, edge_trees = b6_edge(study, ins, entr)
    car_idx = b3_grid(b3_segs([x["P"] for x in vis if x["car"] and not x["inz"]]), 20.0)
    bo_idx = b3_grid(b3_segs(b_out, True), 20.0)
    need = lambda q: b3_dist(car_idx, q, B7_SCREEN_D) < B7_SCREEN_D or b3_dist(bo_idx, q, 10.0) < 10.0
    hedge = [Q for P in hedge for Q in b6_split(b3_dense(P, 3.0), lambda q: not need(q)) if arclen(Q)[-1] >= 12.0]
    screen = [p for p in edge_trees if need(p)]
    n_ent = 0
    for e in entr:                                        # R4: each street entering the zone goes on as a path
        nb = near_pt(e, 160.0, wp_idx)
        if nb and nb[0] > 3.0 and not any(in_chan(u) or in_bld(u, 1.0) for u in b3_dense([e, nb[1]], 3.0)):
            bands.append(([e, nb[1]], 3.0, B3_COL["paving"], u"entrance path"))
            add_hard([e, nb[1]], 1.5 + B3_TREE_CLEAR)
            n_ent += 1
    cnt("entrance paths", n_ent)
    her_box = [(bbox(R), R) for R in b_her]
    near_her = lambda q, r: any(bb[0] - r <= q[0] <= bb[2] + r and bb[1] - r <= q[1] <= bb[3] + r and
                                (pip(q[0], q[1], R) or b3_dist_ring(R, q) < r) for bb, R in her_box)
    aprons = [b3_hull(R) for R in b_her]                  # v7 (05:46): a stone apron round each kept heritage building
    for H in aprons:
        add_hard(H + H[:1], 3.0)
    n_door = 0
    for P in sv.get("door", []):                          # each surveyed door of a heritage building -> the walk
        m_ = P[len(P) // 2]
        if not near_her(m_, 2.0) or not ins(m_):
            continue
        nb = near_pt(m_, 90.0, wp_idx)
        if nb and nb[0] > 4.0 and not any(in_chan(u) or in_bld(u, 0.5) for u in b3_dense([m_, nb[1]], 2.0)[2:]):
            bands.append(([m_, nb[1]], 2.4, B3_COL["stone"], u"heritage door path"))
            add_hard([m_, nb[1]], 1.2 + B3_TREE_CLEAR)
            n_door += 1
    cnt("heritage door paths", n_door)
    for P, bank, chs in walks3:                           # R4: benches in a rhythm on the land edge of the walk
        sg = 1.0 if bank == "NE" else -1.0
        s_ = arclen(P)
        t_ = B7_BENCH_EVERY / 2.0
        while t_ < s_[-1]:
            (bx_, by_), (ux_, uy_) = at_len(P, s_, t_)
            benches.append(((bx_ + uy_ * sg * -(B3_WALK_W / 2.0 - 0.6), by_ - ux_ * sg * -(B3_WALK_W / 2.0 - 0.6)),
                            (ux_, uy_)))
            t_ += B7_BENCH_EVERY
    for P in beds:
        el_names.append((u"Bed walk, shut in floods", P[len(P) // 2]))
    for P in canopy:
        el_names.append((u"Canopied walkway", P[len(P) // 2]))
    # ================================================================ 9 draw the circulation (two passes, merged)
    allb = bands + br_bands
    with mpx_grp(sub, "paths", u"paths: edges (one merged outline, Rhino boolean union)"):
        rings_ = [b3_band(P, [w + 0.5] * len(P)) for P, w, col, nm in allb if len(P) >= 2]
        sub.poly([TL(R) for R in b2_union(rings_, flags)], fill=B3_COL["paving_edge"])
    with mpx_grp(sub, "paths", u"paths: surfaces (merged per surface)"):
        for col in sorted(set(c for P, w, c, nm in allb)):
            rings_ = [b3_band(P, [w] * len(P)) for P, w, c, nm in allb if c == col and len(P) >= 2]
            sub.poly([TL(R) for R in b2_union(rings_, flags)], fill=col)
    with mpx_grp(sub, "paths", u"bike lane beside the walk"):
        for P, bank in walks:
            sg = 1.0 if bank == "NE" else -1.0
            Pb = b6_clean_offset(P, sg * (B3_WALK_W / 2.0 + 0.3 + B3_BIKE_W / 2.0))
            if len(Pb) >= 2:
                sub.poly([TL(b3_band(Pb, [B3_BIKE_W] * len(Pb)))], fill=B3_COL["bike"])
                b6_bike_marks(sub, Pb, T, k)
    with mpx_grp(sub, "paths", u"joints, canopy posts, deck planks, ramps"):
        for P, w, col, nm in allb:
            if nm == u"canopied walkway":
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
        b7_draw_pad(sub, kind, R, T, k)
    with mpx_grp(sub, "paths", u"benches along the walk"):
        for (bx_, by_), (ux_, uy_) in benches:
            if free((bx_, by_), 0.0) or on_hard((bx_, by_), 0.0, lines_only=True):
                a_, b_ = T((bx_ - ux_ * 1.0, by_ - uy_ * 1.0)), T((bx_ + ux_ * 1.0, by_ + uy_ * 1.0))
                sub.line([a_, b_], B3_COL["wood_t"], 0.35, cap=0)
    cnt("benches", len(benches))
    n_steps = 0                                           # R12: steps down to the water in the heritage reach
    with mpx_grp(sub, "paths", u"steps down to the water"):
        for P, bank, chs in walks3:
            sg = -1.0 if bank == "NE" else 1.0            # water side
            for ri_, (a_c, b_c, th) in enumerate(reaches):
                if th != "heritage":
                    continue
                run = [q for q, c in zip(P, chs) if a_c <= c < b_c]
                if len(run) < 3:
                    continue
                Pd = b3_dense(run, 2.0)
                N_ = b3_normals(Pd)
                near_w = [in_chan((q[0] + n[0] * sg * (B3_WALK_W / 2.0 + 3.0), q[1] + n[1] * sg * (B3_WALK_W / 2.0 + 3.0)))
                          for q, n in zip(Pd, N_)]
                i0 = None
                for i_, f_ in enumerate(near_w + [False]):
                    if f_ and i0 is None:
                        i0 = i_
                    if not f_ and i0 is not None:
                        if i_ - i0 >= 12:                 # >= 24 m along the water
                            seg = Pd[i0:min(i_, i0 + 20)]
                            for j_ in range(1, 5):
                                off_ = sg * (B3_WALK_W / 2.0 + 0.7 * j_)
                                E_ = [q for q in b3_off(seg, off_) if not in_chan(q)]
                                if len(E_) >= 2:
                                    sub.line(TL(E_), B3_COL["deck_edge"], 0.1)
                            el_names.append((u"Steps down to the water", seg[len(seg) // 2]))
                            n_steps += 1
                            break
                        i0 = None
    cnt("steps to the water", n_steps)
    with mpx_grp(sub, "paths", u"boardwalk loop in the wetland"):
        for R in widen:
            if not any(ins(q) for q in R) or abs(area2(R)) < 2.0 * 1500.0:
                continue
            Q = b3_chaikin_closed([(q[0] + n[0] * 6.0, q[1] + n[1] * 6.0) for q, n in zip(R, b6_inward(R))], 2)
            if len(Q) >= 6 and all(pip(q[0], q[1], R) for q in Q[::3]):
                sub.poly([TL(b3_band(Q + Q[:1], [2.6] * (len(Q) + 1)))], fill=B3_COL["deck_edge"])
                sub.poly([TL(b3_band(Q + Q[:1], [2.2] * (len(Q) + 1)))], fill=B3_COL["deck"])
                el_names.append((u"Boardwalk loop", Q[len(Q) // 4]))
                cnt("boardwalk loop")
    with mpx_grp(sub, "annotations", u"sightline to the Trajaneum"):
        for P in cl["sight"]:
            if len(P) >= 2:
                a_ = P[0]
                L_ = math.hypot(P[-1][0] - a_[0], P[-1][1] - a_[1]) or 1.0
                ux_, uy_ = (P[-1][0] - a_[0]) / L_, (P[-1][1] - a_[1]) / L_
                b_ = (a_[0] + ux_ * 40.0, a_[1] + uy_ * 40.0)
                sub.line([T(a_), T(b_)], B3_COL["ink"], 0.15, [0.8, 0.5], cap=0)
                tip = T((b_[0] + ux_ * 4.0, b_[1] + uy_ * 4.0))
                sub.poly([[tip, T((b_[0] - uy_ * 1.8, b_[1] + ux_ * 1.8)), T((b_[0] + uy_ * 1.8, b_[1] - ux_ * 1.8))]],
                         fill=B3_COL["ink"])
                el_names.append((u"View to the Trajaneum", b_))
    with mpx_grp(sub, "annotations", u"heritage trail along the walks"):
        tw_ = [(q, c) for P, bank, chs in walks3 for q, c in zip(P, chs)]
        for a_, b_ in zip(trail[:-1], trail[1:]):
            ca, cb = chain_at(C.ref, a_)[0], chain_at(C.ref, b_)[0]
            ca, cb = min(ca, cb), max(ca, cb)
            seg = sorted([(c, q) for q, c in tw_ if ca <= c <= cb])
            pts = []
            for c, q in seg:
                if not pts or math.hypot(q[0] - pts[-1][0], q[1] - pts[-1][1]) < 12.0:
                    pts.append(q)
            if len(pts) >= 2:
                sub.line(TL(pts), B3_COL["heritage"], 0.35, [1.0, 0.7], cap=0)
        for p in trail:
            nb = near_pt(p, 60.0, wp_idx)
            if nb and not any(in_chan(u) for u in b3_dense([p, nb[1]], 2.0)):
                sub.line([T(p), T(nb[1])], B3_COL["heritage"], 0.25, [0.6, 0.5], cap=0)
    cnt("heritage trail stops", len(trail))
    # ================================================================ 10 planting by function (F9)
    dwat = lambda p: chain_at(C.ref, p)[1]
    plants = pad_trees + b7_planting(C, chan, widen, walks3, free, sv, ins, dwat, lambda p: False, screen)
    for bb_, R in [(bb_, R) for bb_, R in lc_box if area2(R) > 0]:   # v8 (outer rings; holes via in_trees):
        y_ = bb_[1] + 3.5                                 # tree crowns (asset library), not as dark patches;
        row = 0                                           # species not surveyed: willow near the water, ash beyond
        while y_ < bb_[3]:
            x_ = bb_[0] + (3.5 if row % 2 else 0.0)
            while x_ < bb_[2]:
                j = ((int(x_ * 7.3) ^ int(y_ * 3.1)) % 17) / 17.0 - 0.5
                p = (x_ + 2.2 * j, y_ - 1.8 * j)
                if pip(p[0], p[1], R) and in_trees(p) and ins(p):
                    plants.append((p, "willow" if dwat(p) < B7_CORRIDOR_T else "ash", 6.5, u"existing woodland"))
                x_ += 7.0
            y_ += 6.1
            row += 1
    hedge_d = [Q for P in hedge for Q in b6_split(b3_dense(P, 3.0), lambda q: on_hard(q, 1.0) or in_wet(q) or
                                                     in_bld(q, 1.0) or not ins(q)) if arclen(Q)[-1] >= 6.0]
    with mpx_grp(sub, "plants", u"edge hedge: screen to car roads and building backs only"):
        for P in hedge_d:
            hb_ = TL(b3_band(P, [2.2 + 0.5 * math.sin(i_ * 0.9 + len(P)) for i_ in range(len(P))]))
            if b8_tile_for("hedge"):                      # v8: Aras's bush hatch, soft width 1.7-2.7 m
                sub.group("plants", u"hedge %d" % len(sub.items))
                sub.items.append(("pat", b8_tile_for("hedge"), [hb_], None, len(P) % 4))
                sub.poly([hb_], stroke=B3_COL["tree_edge"], lw=0.05)
                sub.endgroup()
            else:
                sub.poly([hb_], fill=B3_COL["tree2"], stroke=B3_COL["tree_edge"], lw=0.06)
    n_hs = 0
    if b8_sym_for("hedge") and not b8_tile_for("hedge"):  # v8: Aras's shrubs along the hedge (when no hatch)
        for P in hedge_d:
            L_ = arclen(P)
            for j_ in range(int(L_[-1] // 1.6) + 1):
                q_ = at_len(P, L_, min(j_ * 1.6, L_[-1]))[0]
                x_, y_ = T(q_)
                sub.group("plants", u"hedge shrub %d" % n_hs)
                sub.items.append(("sym", b8_sym_for("hedge", n_hs), x_, y_, 1.1 * k, None))
                sub.endgroup()
                n_hs += 1
    cnt("hedge shrubs (traced symbols)", n_hs)
    for P in hedge_d:
        add_hard(P, 1.1)
    cnt("hedge m", int(sum(arclen(P)[-1] for P in hedge_d)))
    cnt("satellite tree-cover rings", len(lc_box))
    placed = []
    n_t, n_skip, n_sk, n_sym = 0, 0, {}, [0]
    bush_pts = {}                                         # v8: (tile, function) -> [(x, y, r m)] drawn as bush areas
    with mpx_grp(sub, "trees", u"planting"):
        for p, key, cr, why in plants:
            cr = cr or (PLA_SPECIES.get(key) or {}).get("crown_m") or 4.0
            if why == u"existing tree":                  # survey symbol: always drawn where it stands
                ok_ = ins(p) and not in_chan(p) and not in_bld(p)
            elif why == u"existing woodland":            # v8: satellite cover, kept where it is
                ok_ = ins(p) and not in_chan(p) and not in_bld(p, 1.0) and not on_hard(p, 1.0, lines_only=True)
            elif why in (u"wetland emergent",):
                ok_ = ins(p) and not in_chan(p) and not on_hard(p, 0.5)
            elif why in (u"square shade", u"orchard rows"):
                ok_ = ins(p) and not in_wet(p) and not in_bld(p, 1.5) and not on_hard(p, 1.0, lines_only=True)
            else:
                ok_ = free(p, min(cr * 0.3, 2.0))                # crowns may overhang a path
            if not ok_:
                n_skip += 1
                n_sk[why] = n_sk.get(why, 0) + 1
                continue
            if why != u"existing tree" and any(math.hypot(p[0] - q[0], p[1] - q[1]) < (cr + c2) * 0.4 for q, c2 in placed):
                n_skip += 1
                n_sk[why + u" (spacing)"] = n_sk.get(why + u" (spacing)", 0) + 1
                continue
            tid_ = (b8_tile_for(why) or b8_tile_for(key)) if why in B8_BUSH_FN else None
            if tid_:                                      # v8: a shrub of a bush area (Aras's hatch), drawn below
                bush_pts.setdefault((tid_, why), []).append((p[0], p[1], cr / 2.0))
                placed.append((p, cr))
                n_sp[why] = n_sp.get(why, 0) + 1
                continue
            x_, y_ = T(p)
            sub.group("trees", u"%s %d" % (key, n_t))     # v8: every tree its own sub-group (Aras 10:10 TR)
            sub.poly([b3_circle((x_ + 0.2 * cr * k, y_ - 0.2 * cr * k), cr * k / 2.0, 14)], fill=B3_COL["tree_sh"],
                     alpha=0.3)
            sid_ = b8_sym_for(key, n_t)
            if sid_:                                      # v8: Aras's traced tree, stored once, placed here
                sub.items.append(("sym", sid_, x_, y_, cr * k / 2.0, None))
                n_sym[0] += 1
            else:
                try:
                    pl23_put(sub, _B19_PLA_ASSET(key, x_, y_, k, crown_m=cr, seed=n_t, distinct=True))
                except Exception:
                    b3_tree(sub, (x_, y_), cr * k / 2.0, n_t, key)
            sub.endgroup()
            placed.append((p, cr))
            n_sp[why] = n_sp.get(why, 0) + 1
            n_t += 1
    n_bu = 0
    for (tid_, why), P_ in sorted(bush_pts.items()):      # v8: bush areas, each its own sub-group under plants
        for rings in b8_bush_rings(P_, 7 + len(why)):
            RR = [TL(R) for R in rings]
            if not RR:
                continue
            sub.group("plants", u"%s bush %d" % (why, n_bu))
            sub.poly([[(x_ + 0.35 * k, y_ - 0.35 * k) for x_, y_ in R] for R in RR], fill=B3_COL["tree_sh"], alpha=0.3)
            sub.items.append(("pat", tid_, RR, None, n_bu % 4))
            sub.poly(RR, stroke=B3_COL["tree_edge"], lw=0.05)
            sub.endgroup()
            n_bu += 1
    cnt("bush areas (Aras's hatch)", n_bu)
    notes.append(u"trees drawn with Aras's traced symbols: %d of %d%s" % (
        n_sym[0], n_t, u"" if b8_sym_lib() else u" (no traced library in this script: plant module symbols)"))
    # ================================================================ 11 fade, buildings, zone line
    with mpx_grp(sub, "ground", u"edge fade"):
        prev = st
        for d_m, a in B7_FADE:                            # v7 R7: pure Python, offline + Rhino
            ring_s = [TL(b7_grow(R, d_m)) for R in study]
            sub.poly(ring_s + prev, fill="FFFFFF", alpha=a)
            prev = ring_s
        sub.poly([rect(0.0, 0.0, dw, dh)] + prev, fill="FFFFFF", alpha=B2_CONTEXT_VEIL)
    with mpx_grp(sub, "buildings", u"context buildings"):
        for R in b_out:
            sub.poly([TL(R)], fill=B3_COL["bld_ctx"], stroke=B3_COL["bld_ctx_edge"], lw=0.06)
    with mpx_grp(sub, "annotations", u"project zone"):
        for Q in st:
            sub.line(Q + Q[:1], B3_COL["border"], 0.2)
    sh = 0.9 * k
    with mpx_grp(sub, "heritage", u"stone apron round the heritage buildings"):
        for H in aprons:
            sub.poly([TL(b3_band(H + H[:1], [6.0] * (len(H) + 1)))], fill=B3_COL["stone"], stroke=B3_COL["paving_edge"],
                     lw=0.06)
    with mpx_grp(sub, "heritage", u"heritage buildings, kept"):
        for R in b_her:
            sub.poly([[(x + sh, y - sh) for x, y in TL(R)]], fill=B3_COL["shadow"], alpha=0.45)
            sub.poly([TL(R)], fill=B3_COL["heritage"], stroke=B3_COL["bld_edge"], lw=0.13)
    with mpx_grp(sub, "heritage", u"heritage detail as surveyed: stairs, doors, hatching, walls, pool, symbol"):
        n_det = 0
        for role, col_, lw_ in (("bhatch", B3_COL["bld_edge"], 0.05), ("stairs", B3_COL["bld_edge"], 0.07),
                                ("door", B3_COL["ink"], 0.12), ("pond", B3_COL["water"], 0.1),
                                ("mosque_sym", B3_COL["ink"], 0.08)):
            for P in sv.get(role, []):
                if len(P) >= 2 and near_her(P[len(P) // 2], 12.0):
                    sub.line(TL(P), col_, lw_)
                    n_det += 1
        cnt("heritage detail lines (survey)", n_det)
    # ================================================================ 11b the route that ties every place (v8)
    with mpx_grp(sub, "annotations", u"route: riverside walk + bike lane, both banks, footbridges"):
        for P, bank, chs in walks3:
            if len(P) < 2:
                continue
            Q = TL(P if (bank == "NE") == (chs[-1] >= chs[0]) else P[::-1])   # one loop: NE downstream, SW up
            sub.line(Q, B8_ROUTE, 0.45, cap=1, alpha=0.85)
            sQ = arclen(Q)
            t_ = 30.0
            while t_ < sQ[-1] - 10.0:                    # direction arrows every 60 mm on paper
                q_, u_ = at_len(Q, sQ, t_)
                ux_, uy_ = u_ if isinstance(u_, tuple) else (1.0, 0.0)
                sub.poly([[(q_[0] + ux_ * 1.3, q_[1] + uy_ * 1.3), (q_[0] - ux_ * 0.9 - uy_ * 0.9, q_[1] - uy_ * 0.9 + ux_ * 0.9),
                           (q_[0] - ux_ * 0.9 + uy_ * 0.9, q_[1] - uy_ * 0.9 - ux_ * 0.9)]], fill=B8_ROUTE)
                t_ += 60.0
        for P, w, col, nm in br_bands:
            if nm == u"new footbridge":
                sub.line(TL(P), B8_ROUTE, 0.45, cap=1, alpha=0.85)
    # ================================================================ 12 names (beside what they name)
    taken = [b6_pbox(TL(R)) for R in keep_b if b6_pbox(TL(R))[2] - b6_pbox(TL(R))[0] > 0.6]
    labels, left = [], []
    seen = {}
    wpt = lambda bx, by: Ri((x0 + bx / k, y0 + by / k))   # v8: page -> survey m through the turn
    zin = lambda bx, by: ins(wpt(bx, by))

    def clear(b):
        for bx in (b[0], (b[0] + b[2]) / 2.0, b[2]):
            for by in (b[1], (b[1] + b[3]) / 2.0, b[3]):
                q = wpt(bx, by)
                if on_hard(q) or in_wet(q):
                    return False
        return True

    keyed = []                                            # R9: names that can't sit close -> numbered key

    def name(s_, p, size, bold=False, keyable=True, inside=False):
        if any(math.hypot(p[0] - q[0], p[1] - q[1]) < 250.0 for q in seen.get(s_, [])):
            return True
        seen.setdefault(s_, []).append(p)
        x, y = T(p)
        if not (0 <= x <= dw and 0 <= y <= dh):
            return False
        w_ = text_w(s_, size, bold)
        spots = [(-w_ / 2.0, -size / 2.0), (1.0, 0.6), (-1.0 - w_, 0.6), (1.0, -size - 0.6), (-1.0 - w_, -size - 0.6),
                 (-w_ / 2.0, 1.5), (-w_ / 2.0, -size - 1.5)]
        for rr in (3.0, 4.5, B7_LEADER_MAX):
            for ia in range(12):
                ang = ia * math.pi / 6.0
                cx_, cy_ = rr * math.cos(ang), rr * math.sin(ang)
                spots.append((cx_ - (0.0 if cx_ >= 0 else w_), cy_ - size / 2.0))
        if inside:
            spots += [(cx_ * f_ - w_ / 2.0, cy_ * f_ - size / 2.0) for f_ in (6.0, 9.0, 13.0, 18.0)
                      for cx_, cy_ in ((1, 0), (-1, 0), (0, 1), (0, -1), (0.7, 0.7), (-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7))]
        for strict in ((True,) if inside else (True, False)):
            for dx, dy in spots:
                b = (x + dx, y + dy, x + dx + w_, y + dy + size)
                if not (0.5 <= b[0] and b[2] <= dw - 0.5 and 0.5 <= b[1] and b[3] <= dh - 0.5) or \
                        any(hit(b, o, 0.5) for o in labels):
                    continue
                if not clear(b):
                    continue
                if strict and (any(hit(b, o, 0.4) for o in taken) or not (zin(b[0], b[1]) and zin(b[2], b[3]))):
                    continue
                labels.append(b)
                sub.text(s_, b[0], b[1], size, B3_COL["ink"], bold=bold)
                tx, ty = min(max(x, b[0]), b[2]), min(max(y, b[1]), b[3])
                if math.hypot(tx - x, ty - y) > 1.0:
                    sub.line([(x, y), (tx, ty)], B3_COL["ink"], 0.08)
                return True
        if not keyable:
            return False
        n_ = len(keyed) + 1                               # a numbered dot on the element, the name in the key
        b = (x - 1.3, y - 1.3, x + 1.3, y + 1.3)
        if any(hit(b, o, 0.2) for o in labels):
            return False
        labels.append(b)
        keyed.append(s_)
        sub.poly([b3_circle((x, y), 1.25, 16)], fill="FFFFFF", stroke=B3_COL["ink"], lw=0.1)
        sub.text(u"%d" % n_, x, y - 0.75, 1.76, B3_COL["ink"], bold=True, align="C")
        return True
    for a_c, b_c, th in reaches:                          # R2: reach names large along the stream
        s_r = arclen(C.ref)
        m_ = at_len(C.ref, s_r, max(0.0, min(s_r[-1], (a_c + b_c) / 2.0)))[0]
        name(B7_THEMES[th][0].upper(), m_, B7_REACH, True, keyable=False, inside=True)
    # v8 callouts: every place = a numbered dot + a boxed name with its category colour and icon (Aras 07:42 UTC)
    calls, cseen = [], {}

    def call_add(title, subt, p, cat):
        if any(math.hypot(p[0] - q[0], p[1] - q[1]) < 250.0 for q in cseen.get(title, [])):
            return
        cseen.setdefault(title, []).append(p)
        calls.append((chain_at(C.ref, p)[0], title, subt, p, cat))
    hub_words = {}
    for key_, (title_, words_) in sorted(HUB.items()):     # the project's own reading of each working area
        hid = next((w_[:2] for w_ in words_ if w_[:1] == u"K" and w_[1:2].isdigit()), None)
        if hid:
            hub_words[hid] = u" · ".join(b3_title(w_) for w_ in words_ if not w_.startswith(hid))
    for hb in C.hubs:
        if hb.get("in_study"):
            call_add(b3_title(HUB_NAME.get(hb["id"], hb["id"])), hub_words.get(hb["id"], u""), hb["xy"], "meet")
    for p in trail:
        call_add(b6_heritage_name(p), u"Heritage, kept: on the heritage trail", p, "heritage")
    for nm_, p in el_names:
        t_, _, s2 = (u"%s" % nm_).partition(u" · ")
        call_add(t_, s2, p, b8_cat(t_))
    calls.sort(key=lambda c: c[0])                        # numbered in route order, upstream to downstream
    dots = [T(c[3]) for c in calls]
    n_box = 0
    for n_, ((ch, title, subt, p, cat), (x, y)) in enumerate(zip(calls, dots), 1):
        col = B8_CAT[cat][1]
        if not (0 <= x <= dw and 0 <= y <= dh):
            continue
        TS, SS, IC = B8_CALL_T, B8_CALL_S, B8_CALL_I
        tw_ = max(text_w(title, TS, True), text_w(subt, SS) if subt else 0.0)
        bw, bh = IC + tw_ + 3.0, max(IC + 1.4, TS + (SS + 0.8 if subt else 0.0) + 1.8)
        best = None
        for rr in (7.0, 10.0, 14.0, 19.0, 25.0, 33.0, 44.0, 58.0):
            for ia in range(16):
                ang = ia * math.pi / 8.0
                cx_, cy_ = x + rr * math.cos(ang), y + rr * math.sin(ang)
                b = (cx_ - bw / 2.0, cy_ - bh / 2.0, cx_ + bw / 2.0, cy_ + bh / 2.0)
                if not (1.0 <= b[0] and b[2] <= dw - 1.0 and 1.0 <= b[1] and b[3] <= dh - 1.0):
                    continue
                if any(hit(b, o, 0.8) for o in labels) or \
                        any(b[0] - 2.0 < dx_ < b[2] + 2.0 and b[1] - 2.0 < dy_ < b[3] + 2.0 for dx_, dy_ in dots):
                    continue
                out_ = not any(zin(bx, by) for bx in (b[0], (b[0] + b[2]) / 2.0, b[2]) for by in (b[1], b[3]))
                if not out_ and not clear(b):
                    continue
                sc = rr + (0.0 if out_ else 30.0)
                if best is None or sc < best[0]:
                    best = (sc, b)
            if best is not None and best[0] <= rr:
                break
        sub.group("annotations", u"%d %s" % (n_, title))
        if best is not None:
            b = best[1]
            labels.append(b)
            tx, ty = min(max(x, b[0]), b[2]), min(max(y, b[1]), b[3])
            sub.line([(x, y), (tx, ty)], col, 0.18)
            sub.poly([rect(b[0], b[1], b[2], b[3])], fill="FFFFFF", stroke=col, lw=0.2)
            _p24_put(sub, ico_badge(b8_icon(title, cat), b[0] + 0.7 + IC / 2.0, (b[1] + b[3]) / 2.0, IC,
                                    fill="FFFFFF", edge=col, ink=col, accent=col))
            sub.text(title, b[0] + IC + 1.6, b[3] - 0.9 - TS * 0.8, TS, col, bold=True)
            if subt:
                sub.text(subt, b[0] + IC + 1.6, b[1] + 0.9, SS, B3_COL["ink"])
            n_box += 1
        else:
            keyed.append(u"%d %s" % (n_, title))         # no room: the number on the drawing, the name in the key
        labels.append((x - 1.5, y - 1.5, x + 1.5, y + 1.5))
        sub.poly([b3_circle((x, y), 1.5, 20)], fill=col, stroke="FFFFFF", lw=0.15)
        sub.text(u"%d" % n_, x, y - 0.68, 1.9, "FFFFFF", bold=True, align="C")
        sub.endgroup()
    cnt("place callouts (boxed)", n_box)
    cnt("place numbers in the key", len(calls) - n_box)
    for nm_, p in road_names:
        name(nm_, p, B7_NAME, keyable=False)
    for z in C.D.zones:
        if z.get("label") and z.get("q") and ins(z["q"]) and z["code"] in ("WT", "WS", "GR", "WP", "DG", "WD"):
            if not name(b3_title(z["label"], first_only=True), z["q"], B7_NAME, keyable=False):
                left.append(z["label"])
    # ================================================================ sheet
    key_items = [(u"%s: %s" % (B7_THEMES[th][0], B7_WHY[th]), None) for th in
                 sorted(set(th for a_c, b_c, th in reaches))] + [(s_, None) for s_ in keyed]
    n_rows = 2 + int(sum(text_w(nm, 2.12) + 16.0 for nm, c in b8_cat_key() + list(B6_LEGEND) + b8_slope_key() + key_items) //
                     max(dw - 20.0, 50.0))
    head_x = 8.0 + 6.0 * n_rows
    W, H = dw + 2 * B19_M, dh + 2 * B19_M + B19_HEAD + head_x
    pg = Page(W, H)
    pg.poly([rect(0.0, 0.0, W, H)], fill="FFFFFF")
    oy = B19_M + B19_HEAD + head_x
    pg.clip([rect(B19_M, oy, B19_M + dw, oy + dh)])
    blit(pg, sub, B19_M, oy)
    pg.unclip()
    lx, ly = B19_M, oy - 8.0
    for nm, col in b8_cat_key() + list(B6_LEGEND) + b8_slope_key() + key_items:
        tw = text_w(nm, 2.12)
        if lx + 10.0 + tw > W - B19_M:
            lx, ly = B19_M, ly - 6.0
        if col:
            pg.poly([rect(lx, ly, lx + 8.0, ly + 4.0)], fill=col, stroke=B3_COL["kerb"], lw=0.1)
            pg.text(nm, lx + 10.0, ly + 0.8, 2.12, B3_COL["ink"])
            lx += 16.0 + tw
        else:
            pg.text(nm, lx, ly + 0.8, 2.12, B3_COL["ink"])
            lx += 8.0 + tw
    pg.text(u"MIRAQUA · MASTERPLAN", B19_M, B19_M + 8.0, 4.2, B3_COL["ink"], bold=True)
    pg.text(u"drawing language after Greenikka (Arkkitehdit MY, 2020)", B19_M, B19_M + 3.0, 2.12, B3_COL["ink"])
    scale_bar(pg, B19_M + 120.0, B19_M + 3.0, scale, marks=(0.0, 50.0, 100.0, 200.0))
    nx, ny, h_ = W - B19_M - 10.0, B19_M + 8.0, 12.0     # v8: arrow turned with the sheet, centred on (nx, ny)
    NR = lambda u, v: (nx + ca_ * u - sa_ * v, ny + sa_ * u + ca_ * v)
    pg.poly([[NR(0.0, h_ / 2.0), NR(-2.6, -0.05 * h_), NR(0.0, 0.1 * h_), NR(2.6, -0.05 * h_)]], fill=B3_COL["ink"])
    pg.line([NR(0.0, -h_ / 2.0), NR(0.0, 0.1 * h_)], B3_COL["ink"], 0.25)
    tx_, ty_ = NR(0.0, h_ / 2.0 + 2.2)
    pg.text(u"N", tx_, ty_ - 1.0, 3.0, B3_COL["ink"], bold=True, align="C")
    notes += [u"elements: " + u", ".join(u"%s %d" % kv for kv in sorted(n_el.items())),
              u"streets in the zone: " + u", ".join(u"%s %d" % kv for kv in sorted(n_rd.items())),
              u"planting by function: " + u", ".join(u"%s %d" % kv for kv in sorted(n_sp.items())) +
              u" ({} not placed: ".format(n_skip) + u", ".join(u"%s %d" % kv for kv in sorted(n_sk.items())) + u")",
              u"bridge ends on a walk or street: {}".format(n_end),
              u"buildings: {} heritage kept, {} taken out, {} context".format(len(b_her), len(b_rm), len(b_out)),
              u"reaches: " + u"; ".join(u"%s %.0f-%.0f m" % (B7_THEMES[th][0], a_c, b_c) for a_c, b_c, th in reaches),
              u"names in the numbered key: %d" % len(keyed),
              u"names left out (no room): " + (u"; ".join(left) or u"none"), u"{:.1f} s".format(time.time() - t0)]
    b8_pens(pg)                                           # v8: one pen set, consistent weights
    globals()["_B7_SHEET"] = dict(pg=pg, X0=x0 - B19_M / k, Y0=y0 - oy / k, k=k, W=W, H=H)
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
B6_SMOOTH_M = 0.0            # v7 (Aras 05:42 "1:1"): each station keeps its own survey width
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
                while f > 1.0 and clash(q):                  # v7 (05:42): never squeezed, survey width as it is
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
            col = dict(play=B3_COL["sand"], event=B3_COL["lawn"], picnic=B3_COL["lawn"], meadow=B8_POLLI)[kind]
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
              garden="B9C49C", garden_row="8C9A72", corridor="A3B394", stone="E3DCCF",
              asphalt="9C9F99", paving="E9DED8", paving_edge="B5A8A2", joint="D2C6C0")
# v7 (Aras 05:51): hard vs soft at a glance: car roads dark asphalt with white marks, walks warm light paving
# (B19 mauve-pink), gravel paths sand with dots, soft ground green only       # v6 F12: no yellow patches (garden green, bed grey-green)
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


# ================================================================ v7 (6 Nov 2026, Aras 00:46-00:59, previews/V7_PLAN.md R1-R11)
# Every element placed for a stated reason: reaches with a theme (B17 p4, F07, D08), programme lined up along the walk,
# trees by rule (rows along water and walks, groves on the contours, shade at square edges), an open edge with a
# screen only where it has a job, a fade drawn in pure Python, readable names (6 pt +) with short leaders or a key.
B7_CORRIDOR_T = 25.0         # m: the green corridor = open ground within this distance of the water (C.eco band)
B7_ALLEE_OFF = 3.2           # m beyond the bike lane: walk allée line
B7_STRIP_SET = 9.0           # m beyond the bike lane: first programme row starts (past the allée)
B7_ROW_GAP = 6.0             # m between the first and the second programme row
B7_PAD_GAP = 14.0            # m between two pads in a row
B7_BENCH_EVERY = 45.0        # m: benches along the walk
B7_GROVE_STEP = 9.0          # m between grove trees on a contour
B7_GROVE_RHYTHM = (3, 5)     # trees in a grove, then gap positions (along the contour)
B7_SCREEN_D = 12.0           # m: the edge gets a hedge screen only where a car road / building back is this close
B7_LEADER_MAX = 6.0          # mm: longest leader; farther = numbered key
B7_NAME = 2.12               # mm (6 pt) element names
B7_PLACE = 2.47              # mm (7 pt) place / hub names, bold
B7_REACH = 3.6               # mm reach names, bold
B7_FADE = ((10.0, 0.22), (22.0, 0.22), (38.0, 0.22))   # m beyond the zone line, white veil added (the edge fades)
B7_THEMES = dict(            # theme -> (title, programme in row order: kind, name, row); R12 new features
    heritage=(u"Heritage reach", (("cafe", u"Café terrace", 1), ("classroom", u"Craft yard", 1),
                                  ("picnic", u"Shaded lawn", 2))),
    wetland=(u"Wetland reach", (("classroom", u"Outdoor classroom", 1), ("picnic", u"Picnic lawn", 1),
                                ("meadow", u"Pollinator meadow, mown paths", 2))),
    active=(u"Active park reach", (("play", u"Play, sand", 1), ("fitness", u"Fitness corner", 1),
                                   ("skate", u"Skate + pump track", 1), ("court", u"Courts", 2),
                                   ("event", u"Event lawn, amphitheatre steps", 2), ("picnic", u"Picnic lawn", 1),
                                   ("meadow", u"Pollinator meadow, mown paths", 2))),
    everyday=(u"Neighbourhood reach", (("play", u"Play, sand", 1), ("picnic", u"Picnic lawn", 1),
                                       ("fitness", u"Fitness corner", 1), ("dog", u"Dog run", 2))))
# (no orchard / allotments: DROPPED = farmland and orchard are not part of the site, CONTEXT §2; gardening stays in
# Demeter's Garden)
B7_WHY = dict(heritage=u"Ulucami + kept heritage: café, craft, seats", wetland=u"widened stream: learning, quiet lawns",
              active=u"largest open ground: sport, events", everyday=u"housing edge: play, picnic, fitness")


def b7_grow(R, d):
    """ring R moved d m outward along its vertex normals, rounded (pure Python: works offline and in Rhino)"""
    N = b6_inward(R)
    return b3_chaikin_closed([(p[0] - n[0] * d, p[1] - n[1] * d) for p, n in zip(R, N)], 1)


def b7_reaches(C, ins, her_pts, widen, free):
    """R2: the stream split at the hubs; each reach (ch0, ch1, theme) gets its theme from what is in it"""
    ref = list(C.ref)
    L = arclen(ref)[-1]
    cuts = sorted(set([0.0, L] + [chain_at(ref, hb["xy"])[0] for hb in C.hubs if hb.get("in_study")]))
    rs = [[a, b] for a, b in zip(cuts[:-1], cuts[1:]) if b - a > 60.0]
    if not rs:
        rs = [[0.0, L]]
    ulu = chain_at(ref, B3_ULU_XY)[0]
    wch = [chain_at(ref, (sum(q[0] for q in R) / len(R), sum(q[1] for q in R) / len(R)))[0] for R in widen if R]
    hch = [chain_at(ref, p)[0] for p in her_pts]
    opn = [0] * len(rs)
    for R in C.study or []:
        b = bbox(R)
        y = b[1] + 12.0
        while y < b[3]:
            x = b[0] + 12.0
            while x < b[2]:
                if pip(x, y, R) and free((x, y), 5.0):
                    c = chain_at(ref, (x, y))[0]
                    for i, (a, b_) in enumerate(rs):
                        if a <= c < b_:
                            opn[i] += 1
                x += 24.0
            y += 24.0
    out = []
    for i, (a, b) in enumerate(rs):
        out.append([a, b, "heritage" if a <= ulu < b else None, opn[i], sum(1 for c in wch if a <= c < b)])
    free_ = [r for r in out if r[2] is None]
    if free_:
        max(free_, key=lambda r: r[3])[2] = "active"     # the largest open ground
    for r in out:
        if r[2] is None:
            r[2] = "wetland" if r[4] >= 2 else "everyday"
    return [(a, b, th) for a, b, th, n, nw in out]


def b7_strip(walks, reach, items, free, ins, on_box_ok):
    """R3: pads of one reach in a row along the land side of the walk, parallel to it (first row past the allée,
    second row behind), each tied to the walk by a straight path at right angles. Returns
    [(kind, name, ring, link polyline)]."""
    a_ch, b_ch = reach
    out = []
    for kind, nm, row in items:
        L, W = B6_PAD[kind]
        W1 = 18.0
        done = False
        for P, bank, chs in sorted(walks, key=lambda w: -sum(1 for c in w[2] if a_ch <= c < b_ch)):
            sg = 1.0 if bank == "NE" else -1.0
            s = arclen(P)
            base = B3_WALK_W / 2.0 + 0.3 + B3_BIKE_W + B7_STRIP_SET
            d = base + (W / 2.0 if row == 1 else W1 + B7_ROW_GAP + W / 2.0)
            t = 10.0
            while t < s[-1] - 10.0 and not done:
                (x, y), (ux, uy) = at_len(P, s, t)
                i_ = min(len(chs) - 1, max(0, int(t / max(s[-1], 1e-9) * (len(chs) - 1))))
                if not a_ch <= chs[i_] < b_ch:
                    t += 8.0
                    continue
                nx, ny = -uy * sg, ux * sg                # land side
                c = (x + nx * d, y + ny * d)
                R = [(c[0] + ux * sx * L / 2.0 + nx * sy * W / 2.0, c[1] + uy * sx * L / 2.0 + ny * sy * W / 2.0)
                     for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
                ok = free(c, 2.0) and all(ins(q) and free(q, 0.5) for q in R) and on_box_ok(R) and \
                    all(free(((R[0][0] + R[1][0]) / 2.0 + (R[2][0] - R[1][0]) * f, (R[0][1] + R[1][1]) / 2.0 +
                              (R[2][1] - R[1][1]) * f), 0.5) for f in (0.0, 0.5, 1.0))
                if ok:
                    e = (x + nx * (B3_WALK_W / 2.0 + 0.3 + B3_BIKE_W), y + ny * (B3_WALK_W / 2.0 + 0.3 + B3_BIKE_W))
                    f_ = (c[0] - nx * W / 2.0, c[1] - ny * W / 2.0)
                    out.append((kind, nm, R, [e, f_]))
                    done = True
                    break
                t += 6.0
            if done:
                break
    return out


def b7_rect(c, u, L, W):
    """rectangle centred c, long side along unit u"""
    n = (-u[1], u[0])
    return [(c[0] + u[0] * sx * L / 2.0 + n[0] * sy * W / 2.0, c[1] + u[1] * sx * L / 2.0 + n[1] * sy * W / 2.0)
            for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]


def b7_species(dw, hi):
    """R11: one gradient by distance from the water (dw, m) and dry high ground (hi: True above 4 m)"""
    if dw < 14.0:
        return "willow"
    if dw < 22.0:
        return "tamarisk"
    if dw < 40.0:
        return "ash"
    if dw < 75.0 and not hi:
        return "plane"
    return "olive" if dw < 110.0 else "stone_pine"


def b7_planting(C, chan, widen, walks, free, sv, ins, dwat, high, screen):
    """R5/R11: [(p, species, crown m or None, function)] by rule only, no random groups, no grids"""
    out = [(P[0], "plane", 6.0, u"existing tree") for P in sv.get("tree", []) if P and ins(P[0])]   # survey, 1:1
    out += [(p, "plane", PLA_SPECIES["plane"]["crown_m"] * 0.8, u"square shade") for p, i in pl23_hub_trees(C)]
    dgd = pl23_dg(C)
    out += [((xs, ys), key, None, u"garden shade") for key, xs, ys in ((dgd or {}).get("shade_trees") or [])
            if key in PLA_SPECIES]
    for R in chan:                                        # riparian rows: 5.5 m off the water, every 10 m
        s_ = arclen(R + R[:1])
        RR = R + R[:1]
        for i in range(int(s_[-1] // 10.0)):
            q, (ux, uy) = at_len(RR, s_, 10.0 * i)
            n = (-uy, ux) if b6_ccw(R) else (uy, -ux)      # inward (into the water)
            p = (q[0] - n[0] * 5.5, q[1] - n[1] * 5.5)
            if ins(p):
                out.append((p, "willow" if i % 2 == 0 else "tamarisk", None, u"riparian corridor"))
    for R in widen:                                       # emergent bands round the wetland edge: 3 on, 2 off
        Q = b3_dense(R + R[:1], 3.5)[:-1]
        N = b6_inward(Q)
        for i, (q, n) in enumerate(zip(Q, N)):
            if i % 5 < 3:
                p = (q[0] + n[0] * 2.5, q[1] + n[1] * 2.5)
                if ins(p):
                    out.append((p, B3_EMERGENT[(i // 5) % len(B3_EMERGENT)], 2.4, u"wetland emergent"))
    for a_ in C.arms:
        P = a_.get("P") or []
        if len(P) >= 2:
            for sg in (1.0, -1.0):
                for i, q in enumerate(b3_dense(b3_off(P, sg * (B3_ARM_W / 2.0 + 1.0)), 4.0)):
                    if ins(q) and i % 5 < 3:
                        out.append((q, B3_EMERGENT[(i // 5) % len(B3_EMERGENT)], 2.2, u"wetland emergent"))
    for P, bank, chs in walks:                            # allée: land side, every 10 m, species by the gradient
        sg = 1.0 if bank == "NE" else -1.0
        Pa = b6_clean_offset(P, sg * (B3_WALK_W / 2.0 + 0.3 + B3_BIKE_W + B7_ALLEE_OFF))
        s = arclen(Pa)
        t = 5.0
        while t < s[-1]:
            p, _u = at_len(Pa, s, t)
            out.append((p, "ash" if dwat(p) < 40.0 else "plane", None, u"walk allée"))
            t += 10.0
    for P in C.terr:                                      # olives on the rain terraces
        for i, q in enumerate(b3_dense(P, 9.0)[1:-1]):
            out.append((q, "olive", None, u"terrace olives"))
    for z in C.D.zones:                                   # rosemary / lavender rows on the dry tops (bed rows)
        if z["code"] in ("WS", "GR") and len(z["P"]) >= 3:
            b = bbox(z["P"])
            horiz = (b[2] - b[0]) >= (b[3] - b[1])
            v = (b[1] if horiz else b[0]) + 3.0
            r = 0
            while v < (b[3] if horiz else b[2]):
                w = (b[0] if horiz else b[1]) + 2.0
                while w < (b[2] if horiz else b[3]):
                    x, y = (w, v) if horiz else (v, w)
                    if pip(x, y, z["P"]):
                        out.append(((x, y), ("rosemary", "lavender")[r % 2], 2.0, u"dry-top beds"))
                    w += 2.5
                v += 6.0
                r += 1
    zd = (getattr(C, "contours", None) or [])            # groves on the contours: 3 trees, then a 5-step gap
    for j, P in enumerate(zd):
        if j % 2 or len(P) < 2:
            continue
        s = arclen(P)
        t, k_ = 0.0, 0
        while t < s[-1]:
            p, _u = at_len(P, s, t)
            if ins(p) and free(p, 4.0) and dwat(p) > 26.0:
                if k_ % sum(B7_GROVE_RHYTHM) < B7_GROVE_RHYTHM[0]:
                    out.append((p, b7_species(dwat(p), high(p)), None, u"contour grove"))
                k_ += 1
            t += B7_GROVE_STEP
    out += [(p, "stone_pine", None, u"edge screen") for p in screen]   # only where the edge screens a road / backs
    return out


def b7_merge_bridges(br_ways):
    """R10: road bridges whose middles lie within 30 m and run the same way = one deck (OSM's two carriageways):
    [(centreline, width)]"""
    out, used = [], set()
    for i, x in enumerate(br_ways):
        if i in used:
            continue
        P = x["P"]
        grp = [x]
        for j in range(i + 1, len(br_ways)):
            y = br_ways[j]
            if j in used:
                continue
            m1, m2 = P[len(P) // 2], y["P"][len(y["P"]) // 2]
            if math.hypot(m1[0] - m2[0], m1[1] - m2[1]) < 30.0:
                grp.append(y)
                used.add(j)
        if len(grp) == 1:
            out.append((P, x["w"]))
            continue
        A = b3_dense(P, 2.0)
        B = grp[1]["P"]
        if math.hypot(B[0][0] - A[0][0], B[0][1] - A[0][1]) > math.hypot(B[-1][0] - A[0][0], B[-1][1] - A[0][1]):
            B = B[::-1]
        sB = arclen(B)
        sA = arclen(A)
        M, sep = [], 0.0
        for t, a in zip(sA, A):
            b, _u = at_len(B, sB, t / max(sA[-1], 1e-9) * sB[-1])
            M.append(((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0))
            sep = max(sep, math.hypot(a[0] - b[0], a[1] - b[1]))
        out.append((M, sep + max(g["w"] for g in grp)))
    return out


B6_PAD.update(skate=(30.0, 18.0), orchard=(42.0, 22.0), dog=(30.0, 20.0), event=(46.0, 30.0), meadow=(54.0, 30.0),
              picnic=(26.0, 16.0), play=(20.0, 14.0))


def b7_draw_pad(sub, kind, R, T, k):
    """R10/R12: pads on the strip are rectangles parallel to the walk; each type drawn as what it is"""
    if len(R) != 4 or kind not in ("play", "event", "picnic", "meadow", "skate", "orchard", "dog"):
        return b6_draw_pad(sub, kind, R, T, k)
    Q = [T(p) for p in R]
    a, u, v, L, W = b6_rect_axes(R)
    P_ = lambda s, t: T(b6_pt(a, u, v, s, t))
    with mpx_grp(sub, "hubs", u"programme: %s" % kind):
        if kind == "play":
            sub.poly([Q], fill=B3_COL["sand"], stroke=B3_COL["paving_edge"], lw=0.12)
            b3_dots(sub, bbox(Q), 0.9, B3_COL["paving_edge"], [Q])
            for s, t, r in ((L * 0.3, W * 0.45, 2.6), (L * 0.68, W * 0.6, 2.0)):
                sub.poly([b3_circle(P_(s, t), r * k, 16)], fill=B3_COL["lawn_dk"], stroke=B3_COL["tree_edge"], lw=0.06)
            sub.line([P_(L * 0.82, 2.0), P_(L * 0.82, W - 2.0)], B3_COL["deck_edge"], 0.2)   # swing frame
        elif kind == "event":
            sub.poly([Q], fill=B3_COL["lawn"], stroke=B3_COL["tree_edge"], lw=0.12)
            sub.poly([[P_(1.0, W * 0.3), P_(6.0, W * 0.3), P_(6.0, W * 0.7), P_(1.0, W * 0.7)]], fill=B3_COL["deck"],
                     stroke=B3_COL["deck_edge"], lw=0.1)                                   # stage
            for j in range(4):                                                             # amphitheatre steps
                r = 14.0 + 2.2 * j
                arc = [b6_pt(a, u, v, 3.5 + r * math.cos(t_), W / 2.0 + r * math.sin(t_))
                       for t_ in [math.radians(-50 + 5 * i) for i in range(21)]]
                arc = [q for q in arc if pip(q[0], q[1], R)]
                if len(arc) >= 2:
                    sub.line([T(q) for q in arc], B3_COL["deck_edge"], 0.12)
        elif kind == "picnic":
            sub.poly([Q], fill=B3_COL["lawn"], stroke=B3_COL["tree_edge"], lw=0.12)
            s = 4.0
            while s < L - 3.0:
                for t in (W * 0.33, W * 0.67):
                    sub.poly([[P_(s - 1.0, t - 0.4), P_(s + 1.0, t - 0.4), P_(s + 1.0, t + 0.4), P_(s - 1.0, t + 0.4)]],
                             fill=B3_COL["wood_t"])
                s += 5.0
        elif kind == "meadow":
            sub.poly([Q], fill=B3_COL["meadow"], stroke=B3_COL["tree_edge"], lw=0.12, dash=[0.6, 0.4])
            b3_dots(sub, bbox(Q), 0.8, B3_COL["culture"], [Q])
            sub.poly([[P_(0.0, W / 2.0 - 1.0), P_(L, W / 2.0 - 1.0), P_(L, W / 2.0 + 1.0), P_(0.0, W / 2.0 + 1.0)]],
                     fill=B3_COL["lawn"])
            sub.poly([[P_(L / 2.0 - 1.0, 0.0), P_(L / 2.0 + 1.0, 0.0), P_(L / 2.0 + 1.0, W), P_(L / 2.0 - 1.0, W)]],
                     fill=B3_COL["lawn"])
        elif kind == "skate":
            sub.poly([Q], fill=B3_COL["asphalt"], stroke=B3_COL["paving_edge"], lw=0.12)
            loop = [b6_pt(a, u, v, L / 2.0 + (L / 2.0 - 3.0) * math.cos(t_), W / 2.0 + (W / 2.0 - 3.0) * math.sin(t_))
                    for t_ in [2 * math.pi * i / 36.0 for i in range(36)]]
            sub.line([T(q) for q in loop + loop[:1]], "FFFFFF", 0.25)                     # pump track
            sub.poly([b3_circle(P_(L * 0.5, W * 0.5), 2.5 * k, 16)], fill=B3_COL["paving"], stroke=B3_COL["deck_edge"],
                     lw=0.08)                                                              # bowl
        elif kind == "orchard":
            sub.poly([Q], fill=B3_COL["lawn"], stroke=B3_COL["tree_edge"], lw=0.1)
            t = 4.0
            while t < W - 2.0:
                sub.line([P_(1.0, t), P_(L - 1.0, t)], B3_COL["lawn_dk"], 0.3)
                t += 7.0
        elif kind == "dog":
            sub.poly([Q], fill=B3_COL["gravel"], stroke=B3_COL["deck_edge"], lw=0.12, dash=[0.5, 0.3])   # fence
            b3_dots(sub, bbox(Q), 1.4, B3_COL["paving_edge"], [Q])
            sub.poly([b3_circle(P_(L * 0.75, W * 0.5), 2.2 * k, 14)], fill=B3_COL["lawn_dk"])


B6_LEGEND = ((u"Riverside walk", B3_COL["paving"]), (u"Bike lane", B3_COL["bike"]),
             (u"Bed walk, shut in floods", B3_COL["gravel"]), (u"Car road + pavements", B3_COL["asphalt"]),
             (u"Decks, footbridges, boardwalk", B3_COL["deck"]), (u"Selinos", B3_COL["water"]),
             (u"Widened stream, wetland", B3_COL["water_lt"]), (u"Green corridor (within 25 m of the water)",
                                                                B3_COL["corridor"]),
             (u"Reed basins", B3_COL["reed"]), (u"Stepped dry tops, rain terraces", B3_COL["lawn_dk"]),
             (u"Allotments", B3_COL["garden"]), (u"Courts", B3_COL["court"]), (u"Fitness", B3_COL["rubber"]),
             (u"Play sand", B3_COL["sand"]), (u"Lawns: events, picnics, orchard", B3_COL["lawn"]),
             (u"Pollinator meadow", B8_POLLI), (u"Skate + pump track", B3_COL["asphalt"]),
             (u"Trees by distance from the water: willow, tamarisk > ash > plane > olive, stone pine",
              B3_TREE_TONE["plane"]),
             (u"Hedge screen (roads, building backs)", B3_COL["tree2"]),
             (u"Heritage, kept + trail", B3_COL["heritage"]),
             (u"Ground +2 m steps above the bed", b3_mix(B3_COL["meadow"], B3_COL["contour_dk"], 0.3)))


_B7_LC = {}


def b7_lc_rings(key):
    """v7 (Aras 05:43, satellite merge): the ESA WorldCover 2021 rings of one class (LC_EMBED, survey m, pixel
    edges exact, holes as extra rings: fill even-odd)"""
    if key not in _B7_LC:
        try:
            d = json.loads(zlib.decompress(base64.b64decode("".join(LC_EMBED))).decode("utf-8"))
            _B7_LC[key] = [r_ for r_ in d.get("rings", {}).get(key, []) if len(r_) >= 3]
        except Exception:
            _B7_LC[key] = []
    return _B7_LC[key]


B7_BAKE_ROOT = "B19_PLAN"     # v7 (Aras 05:46 card "Rhino draws + exports PDF"): the plan drawn in the .3dm at its
B7_PATTERN = {}               # true survey coordinates (1:1 over the survey), PDF exported from Rhino. v8 (Aras 09:21
                              # TR): no Rhino pattern hatches (the "///" over the green); the sheet's own v6 fills and
                              # textures are drawn instead


def b7_pip_any(p, rings):
    return any(pip(p[0], p[1], R) for R in rings)


def b7_clip_line(pts, rings):
    """the pieces of polyline pts (page mm) inside the clip rings (even-odd), cut at the ring edges"""
    out, cur = [], []
    segs = [(a, b) for R in rings for a, b in zip(R, R[1:] + R[:1])]
    for a, b in zip(pts[:-1], pts[1:]):
        xs = [0.0, 1.0]
        bb_ = (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1]))
        for c, d in segs:
            if max(c[0], d[0]) < bb_[0] or min(c[0], d[0]) > bb_[2] or max(c[1], d[1]) < bb_[1] or \
                    min(c[1], d[1]) > bb_[3]:
                continue
            q = b2_seg_x(a, b, c, d)
            if q:
                L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
                xs.append(math.hypot(q[0] - a[0], q[1] - a[1]) / L)
        xs = sorted(set(xs))
        for t0, t1 in zip(xs[:-1], xs[1:]):
            m = (a[0] + (b[0] - a[0]) * (t0 + t1) / 2.0, a[1] + (b[1] - a[1]) * (t0 + t1) / 2.0)
            p0 = (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0)
            p1 = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
            if sum(1 for R in rings if pip(m[0], m[1], R)) % 2 == 1:
                if not cur:
                    cur = [p0]
                cur.append(p1)
            elif cur:
                out.append(cur)
                cur = []
    if len(cur) >= 2:
        out.append(cur)
    return out


def b7_bake_world(doc, sh, warn):
    """v7: the whole sheet drawn into the open .3dm under B7_BAKE_ROOT (sub-layers by element group), the plan at
    its true survey coordinates; clips applied (lines cut at the clip edge, fills intersected with Rhino's curve
    boolean), colours flattened on white, textured hatches (B7_PATTERN) over the solid fills. The last bake is
    deleted first. Returns (objects, sheet corners in model units)."""
    import rhinoscriptsyntax as rs
    import System
    pg, k = sh["pg"], sh["k"]
    try:
        u = Rhino.RhinoMath.UnitScale(Rhino.UnitSystem.Meters, doc.ModelUnitSystem)
    except Exception:
        u = 1.0
    s = u / k                                             # model units per sheet mm
    X0, Y0 = sh["X0"] * u, sh["Y0"] * u
    P3 = lambda p: rg.Point3d(X0 + p[0] * s, Y0 + p[1] * s, 0.0)
    tol = doc.ModelAbsoluteTolerance
    for lay in list(rs.LayerNames() or []):
        if lay == B7_BAKE_ROOT or lay.startswith(B7_BAKE_ROOT + "::"):
            old = rs.ObjectsByLayer(lay)
            if old:
                rs.DeleteObjects(old)
    if not rs.IsLayer(B7_BAKE_ROOT):
        rs.AddLayer(B7_BAKE_ROOT)
    lay_ix = {}

    clean_ = lambda t: u"".join(ch for ch in (t or u"other") if ch not in u"[]:;\\/").strip()[:60] or u"other"

    def layer(parts):                                     # v8 (Aras 10:10 TR): parent group = category layer,
        nm = B7_BAKE_ROOT                                 # each element its own sub-layer: ROOT::category::element
        for p_ in parts:
            nm = u"%s::%s" % (nm, clean_(p_))
            if nm not in lay_ix:
                if not rs.IsLayer(nm):
                    rs.AddLayer(nm)
                lay_ix[nm] = doc.Layers.FindByFullPath(nm, -1)
        return lay_ix[nm]
    pats = {}
    for nm_ in set(p for p, sc in B7_PATTERN.values()) | {"Solid"}:
        try:
            hp = doc.HatchPatterns.FindName(nm_)
            pats[nm_] = int(hp.Index) if hp is not None else -1
        except Exception:
            pats[nm_] = -1
    dash_lt = -1
    try:
        lt = doc.Linetypes.FindName("Dashed")
        dash_lt = int(lt.Index) if lt is not None else -1
    except Exception:
        pass
    n = [0]

    def attr(lix, colour, lw=None, dash=None):
        a = Rhino.DocObjects.ObjectAttributes()
        a.LayerIndex = lix
        try:
            a.DisplayOrder = n[0] + 1                     # v8: Rhino stacks the pieces in the sheet's order
        except Exception:
            pass
        if cur_gi[0] is not None:                         # v8: each element one Rhino group
            a.AddToGroup(cur_gi[0])
        r_, g_, b_ = _rgb(colour)
        a.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
        a.ObjectColor = System.Drawing.Color.FromArgb(r_, g_, b_)
        a.PlotColorSource = Rhino.DocObjects.ObjectPlotColorSource.PlotColorFromObject
        a.PlotColor = System.Drawing.Color.FromArgb(r_, g_, b_)
        if lw is not None:
            a.PlotWeightSource = Rhino.DocObjects.ObjectPlotWeightSource.PlotWeightFromObject
            a.PlotWeight = float(lw)
        if dash and dash_lt >= 0:
            a.LinetypeSource = Rhino.DocObjects.ObjectLinetypeSource.LinetypeFromObject
            a.LinetypeIndex = dash_lt
        return a

    def pcurve(pts, closed):
        Q = [P3(p) for p in pts]
        if closed:
            Q.append(Q[0])
        c = rg.PolylineCurve(Q)
        return c if c.IsValid else None
    clips, grps, fails = [], [], [0]
    rgrp, cur_gi, blk = {}, [None], {}
    lib = b8_sym_lib()

    def grp_add(g_):
        if cur_gi[0] is not None and g_ is not None:
            try:
                doc.Groups.AddToGroup(cur_gi[0], g_)
            except Exception:
                pass

    def block(sid):
        if sid in blk:
            return blk[sid]
        blk[sid] = None
        bands = lib.get(sid)
        if not bands:
            return None
        nm = u"B19_tree_%s" % sid
        try:
            old = doc.InstanceDefinitions.Find(nm)
            if old is not None:
                doc.InstanceDefinitions.Delete(old.Index, True, True)
            geos, atts = [], []
            for b_ in bands:
                cs = []
                for R in b_["rings"]:
                    if len(R) >= 3:
                        c = rg.PolylineCurve([rg.Point3d(p[0], p[1], 0.0) for p in R] + [rg.Point3d(R[0][0], R[0][1], 0.0)])
                        if c.IsValid:
                            cs.append(c)
                for h in (rg.Hatch.Create(cs, pats.get("Solid", 0), 0.0, 1.0, 0.0005) or []) if cs else []:
                    a = Rhino.DocObjects.ObjectAttributes()
                    r_, g2, b2 = _rgb(b_["fill"])
                    a.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
                    a.ObjectColor = System.Drawing.Color.FromArgb(r_, g2, b2)
                    a.PlotColorSource = Rhino.DocObjects.ObjectPlotColorSource.PlotColorFromObject
                    a.PlotColor = a.ObjectColor
                    geos.append(h)
                    atts.append(a)
            if geos:
                i_ = doc.InstanceDefinitions.Add(nm, u"Aras tree set, traced (v8)", rg.Point3d.Origin, geos, atts)
                blk[sid] = i_ if i_ >= 0 else None
        except Exception:
            blk[sid] = None
        return blk[sid]
    for it in pg.items:
        kd = it[0]
        if kd == "grp":
            if it[1] is None:
                if grps:
                    grps.pop()
            else:
                grps.append((it[1], it[2]))
            continue
        if kd == "clip":
            clips.append(it[1])
            continue
        if kd == "unclip":
            if clips:
                clips.pop()
            continue
        if grps:                                          # v8: ROOT::category::element type, each element
            eb_ = re.sub(r"\s*\d+$", u"", u"%s" % (grps[-1][1] or u"")) or grps[0][0]   # one Rhino group
            lix = layer([grps[0][0], eb_])
            gkey = (grps[0][0], grps[-1][1])
        else:
            lix, gkey = layer([u"sheet"]), None
        cur_gi[0] = None
        if kd == "pat":                                   # v8: bush hatch -> its tile's mean colour (Rhino has no tile)
            t_ = b8_tiles().get(it[1]) or {}
            it = ("poly", it[2], (t_.get("mean") or B3_COL["tree2"]).lstrip("#"), None, 0.0, None, None, it[3] if len(it) > 3 else None)
            kd = "poly"
        if gkey is not None:
            if gkey not in rgrp:
                try:
                    rgrp[gkey] = doc.Groups.Add(u"%s %s" % gkey)
                    _B8_RGRP.append(rgrp[gkey])
                except Exception:
                    rgrp[gkey] = -1
            cur_gi[0] = rgrp[gkey] if isinstance(rgrp[gkey], int) and rgrp[gkey] >= 0 else None
        if kd == "sym":                                   # v8: Aras's traced tree = one Rhino block, placed here
            sid, x, y, r = it[1], it[2], it[3], it[4]
            bi = block(sid)
            if bi is None:
                fails[0] += 1
                continue
            try:
                xf = rg.Transform.Multiply(rg.Transform.Translation(rg.Vector3d(P3((x, y)))),
                                           rg.Transform.Scale(rg.Point3d.Origin, r * s))
                g_ = doc.Objects.AddInstanceObject(bi, xf, attr(lix, "000000"))
                n[0] += 1
                grp_add(g_)
            except Exception:
                fails[0] += 1
            continue
        clip = clips[-1] if clips else None
        if kd == "poly":
            _, rings, fill, stroke, lw, dash, stripes, alpha = it
            cs = [pcurve(r_, True) for r_ in rings if len(r_) >= 3]
            cs = [c for c in cs if c]
            if not cs:
                continue
            if clip is not None and not all(b7_pip_any(p, clip) for r_ in rings for p in r_[::max(1, len(r_) // 12)]):
                ccs = [c for c in (pcurve(r_, True) for r_ in clip) if c]
                cut = []
                for c in cs:
                    for cc in ccs:
                        try:
                            res = rg.Curve.CreateBooleanIntersection(c, cc, tol)
                            cut += list(res or [])
                        except Exception:
                            fails[0] += 1
                cs = cut
                if not cs:
                    continue
            if fill and fill.upper() != "FFFFFF":
                col = _flat(fill, alpha)
                try:
                    for h in rg.Hatch.Create(cs, pats.get("Solid", 0), 0.0, 1.0, tol) or []:
                        doc.Objects.AddHatch(h, attr(lix, col))
                        n[0] += 1
                    pat = B7_PATTERN.get(fill.upper())
                    if pat and pats.get(pat[0], -1) >= 0:
                        for h in rg.Hatch.Create(cs, pats[pat[0]], 0.0, pat[1] * u, tol) or []:
                            doc.Objects.AddHatch(h, attr(lix, mix(col, "000000", 0.18), 0.05))
                            n[0] += 1
                except Exception:
                    fails[0] += 1
            if stroke and stroke.upper() != "FFFFFF":
                for c in cs:
                    doc.Objects.AddCurve(c, attr(lix, _flat(stroke, alpha), lw, dash))
                    n[0] += 1
        elif kd == "line":
            pts, stroke, lw, dash = it[1], it[2], it[3], it[4]
            if not stroke or stroke.upper() == "FFFFFF":
                continue
            pieces = [pts] if clip is None or all(b7_pip_any(p, clip) for p in pts) else b7_clip_line(pts, clip)
            for P in pieces:
                c = pcurve(P, False)
                if c:
                    doc.Objects.AddCurve(c, attr(lix, _flat(stroke, it[6] if len(it) > 6 else None), lw, dash))
                    n[0] += 1
        elif kd == "circle":                              # v8: circles as closed curves (seats, dots, symbols)
            _, cx, cy, r, fill, stroke, lw, alpha = (tuple(it) + (None,) * 8)[:8]
            c = pcurve([(cx + r * math.cos(a_ * math.pi / 12.0), cy + r * math.sin(a_ * math.pi / 12.0))
                        for a_ in range(24)], True)
            if c is None:
                continue
            if fill and fill.upper() != "FFFFFF":
                try:
                    for h in rg.Hatch.Create(c, pats.get("Solid", 0), 0.0, 1.0, tol) or []:
                        doc.Objects.AddHatch(h, attr(lix, _flat(fill, alpha)))
                        n[0] += 1
                except Exception:
                    fails[0] += 1
            if stroke and stroke.upper() != "FFFFFF":
                doc.Objects.AddCurve(c, attr(lix, _flat(stroke, alpha), lw))
                n[0] += 1
        elif kd == "image":                               # v8: the asset-library images (trees, plants, figures)
            _, x, y, w, h, path_, alpha, flip = (tuple(it) + (None,) * 9)[:8]
            try:
                if not path_ or not os.path.isfile(path_):
                    fails[0] += 1
                    continue
                o_ = P3((x + w, y) if flip else (x, y))
                pl = rg.Plane(o_, rg.Vector3d(-1.0 if flip else 1.0, 0.0, 0.0), rg.Vector3d(0.0, 1.0, 0.0))
                g_ = doc.Objects.AddPictureFrame(pl, path_, False, w * s, h * s, True, False)
                if g_ != System.Guid.Empty:
                    o2 = doc.Objects.FindId(g_)
                    if o2 is not None:
                        o2.Attributes.LayerIndex = lix
                        try:
                            o2.Attributes.DisplayOrder = n[0] + 1
                        except Exception:
                            pass
                        o2.CommitChanges()
                    n[0] += 1
                else:
                    fails[0] += 1
            except Exception:
                fails[0] += 1
        elif kd == "text":
            _, t, x, y, size, colour, bold, align = it[:8]
            try:
                i_ = rs.AddText(t, (P3((x, y)).X, P3((x, y)).Y, 0.0), size * s, "Arial", 1 if bold else 0,
                                {"L": 1, "C": 2, "R": 4}[align])
                if i_:
                    rs.ObjectLayer(i_, doc.Layers[lix].FullPath)
                    rs.ObjectColor(i_, _rgb(colour))
                    rs.ObjectPrintColor(i_, _rgb(colour))
                    n[0] += 1
            except Exception:
                fails[0] += 1
    if fails[0]:
        warn.append(u"B19 Rhino drawing: {} piece(s) could not be cut / hatched (left out)".format(fails[0]))
    return n[0], (rg.Point3d(X0, Y0, 0.0), rg.Point3d(X0 + sh["W"] * s, Y0 + sh["H"] * s, 0.0))


def b7_rhino_pdf(doc, corners, W_mm, H_mm, path, warn):
    """v7: the PDF written by Rhino (FilePdf, vector) from the Top view, window = the sheet, only B19_PLAN layers
    shown while it prints (the survey and everything else hidden, then restored)"""
    import System
    view = None
    for v in doc.Views:
        if v.ActiveViewport.Name == "Top":
            view = v
            break
    view = view or doc.Views.ActiveView
    vis = [(l.Index, l.IsVisible) for l in doc.Layers if not l.IsDeleted]
    try:
        for l in doc.Layers:
            if l.IsDeleted:
                continue
            on = l.FullPath == B7_BAKE_ROOT or l.FullPath.startswith(B7_BAKE_ROOT + "::")
            if l.IsVisible != on:
                l.IsVisible = on
                _b8_lmod(doc, l, l.Index)
        dpi = 300.0 if max(W_mm, H_mm) < 1200.0 else 150.0   # v8: 1:1,000 sheet ~2.3 x 2.8 m: images at 150 dpi (lines stay vector)
        size = System.Drawing.Size(int(W_mm / 25.4 * dpi), int(H_mm / 25.4 * dpi))
        st = Rhino.Display.ViewCaptureSettings(view, size, dpi)
        st.SetWindowRect(corners[0], corners[1])
        for nm_, val in (("RasterMode", False), ("DrawGrid", False), ("DrawAxis", False), ("DrawWallpaper", False),
                         ("DrawBackground", False)):
            try:
                setattr(st, nm_, val)
            except Exception:
                pass
        try:
            st.OutputColor = Rhino.Display.ViewCaptureSettings.ColorMode.DisplayColor
        except Exception:
            pass
        pdf = Rhino.FileIO.FilePdf.Create()
        pdf.AddPage(st)
        pdf.Write(path)
        return True
    except Exception as ex:
        warn.append(u"B19 Rhino PDF not written ({}: {}); the script's own PDF is the result".format(
            type(ex).__name__, ex))
        return False
    finally:
        for i_, was in vis:
            l = doc.Layers[i_]
            if l.IsVisible != was:
                l.IsVisible = was
                _b8_lmod(doc, l, i_)
        doc.Views.Redraw()


def _b8_lmod(doc, l, i_):
    """push a layer change (Rhino 8 layers are live objects; Modify only where it exists)"""
    try:
        doc.Layers.Modify(l, i_, True)
    except Exception:
        pass


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
    t_pg = time.time()
    pg, notes = b19_page(C, site, C.study or V.study, scale, warn)
    lines += notes
    lines.append(u"drawing built: {:.0f} s".format(time.time() - t_pg))
    t_pdf = time.time()
    path = b8_save(pg, folder, B19_NAME, u"MIRAQUA masterplan, B19 drawing language", lines)   # v8: grouped
    lines.append(u"{}  {}  (PDF written in {:.0f} s)".format(os.path.basename(path),
                                                         datetime.datetime.now().strftime("%H:%M:%S"), time.time() - t_pdf))
    files = [path]
    sh = globals().get("_B7_SHEET")
    rb_ = inp("rhino_bake", False)
    rb_ = rb_ is True or u"%s" % rb_ in (u"True", u"true", u"1")
    if not rb_:                                           # v8.1: the slow Rhino copy only when asked for
        lines.append(u"Rhino copy skipped (rhino_bake is False): only the script's PDF, nothing drawn in the .3dm")
    if rb_ and doc is not None and Rhino is not None and sh:      # v7 (Aras 05:46): Rhino draws it in the .3dm + exports
        t1 = time.time()
        try:
            undo0 = doc.UndoRecordingEnabled
            try:
                doc.Views.RedrawEnabled = False
                doc.UndoRecordingEnabled = False          # v8: no undo copies of the temporary drawing
                n_, corners = b7_bake_world(doc, sh, warn)
            finally:
                doc.UndoRecordingEnabled = undo0
                doc.Views.RedrawEnabled = True
            lines.append(u"Rhino: {} objects drawn under layer {} at the survey's own coordinates, {:.0f} s".format(
                n_, B7_BAKE_ROOT, time.time() - t1))
            rpath = os.path.join(folder, B19_NAME.replace(".pdf", "_rhino.pdf"))
            if b7_rhino_pdf(doc, corners, sh["W"], sh["H"], rpath, warn):
                files.insert(0, rpath)
                lines.append(u"{}  (written by Rhino)".format(os.path.basename(rpath)))
        except Exception as ex_:
            import traceback
            warn.append(u"B19 Rhino drawing NOT DONE ({}: {}); the script's own PDF is the result. {}".format(
                type(ex_).__name__, ex_, traceback.format_exc()[-300:]))
        finally:                                          # v8 (Aras 09:16 TR): drawn, exported, then deleted
            n_del = b8_remove_bake(doc, warn)
            lines.append(u"Rhino: the temporary drawing removed from the .3dm ({} objects, layer {} deleted)".format(
                n_del, B7_BAKE_ROOT))
    return folder, files, lines, [("A", 1, pg)], scale


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
