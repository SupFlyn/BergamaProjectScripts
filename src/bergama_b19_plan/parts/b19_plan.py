

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
VERSION = "bergama_b19_plan v2 (2026-11-05)"  # v2 step 1 (Aras 22:09): continuous network as bands with widths and textures, buildings merged and whole, edge fades out, no pictograms; v1 rejected 21:26
SHORT = "v2"
GH_LABEL = "B19Plan"
SETTINGS = ("rhino_bake", "scale")
OUT_FOLDER = "bergama_b19_plan"
LOG_NAME = "bergama_b19_plan_log.txt"
BAKE_ROOT = "B19"
B19_SCALE = 4000.0           # default print scale (design spec, 5 Nov 21:0x; input `scale` overrides)
B19_NAME = "Bergama_B19_plan_v2_step1.pdf"
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


def b19_page(C, site, study, scale, warn):
    """Step 1 sheet: context, zone ground, the whole route network as bands, bridges and their ends, buildings
    (inside the zone clear and whole, outside pale), the edge fading out. Returns (Page, log notes)."""
    k = 1000.0 / scale
    x0, y0, x1, y1 = bbox(site)
    dw, dh = (x1 - x0) * k, (y1 - y0) * k
    T = lambda p: ((p[0] - x0) * k, (p[1] - y0) * k)
    TL = lambda P: [T(p) for p in P]
    ins = lambda p: any(pip(p[0], p[1], R) for R in study)
    sub = Page(dw, dh)
    st = [TL(R) for R in study if len(R) >= 3]
    notes, flags = [], []
    water = [(R, Hs) for R, Hs in pl23_water_groups(C, warn)]
    in_water = lambda p: any(pip(p[0], p[1], R) and not any(pip(p[0], p[1], H) for H in Hs) for R, Hs in water)
    # ---- buildings: merged, then each block wholly inside or wholly outside (by its centre), never cut
    raw = [R for role in ("building", "housing", "shed", "heritage") for R in C.bld.get(role, []) if len(R) >= 3]
    blds = b2_union(raw, warn)
    b_in = [R for R in blds if ins(inner_pt(R))]
    b_out = [R for R in blds if not ins(inner_pt(R))]
    # ---- 1 context (outside): pale road surfaces and pale buildings with a light shadow
    with mpx_grp(sub, "ground", u"context roads"):
        for R in C.road_loops:
            sub.poly([TL(R)], fill=B2_COL["paving"], alpha=0.6)
    sh = 0.8 * k                                          # shadow offset 0.8 m to the south-east (design value)
    with mpx_grp(sub, "buildings", u"context buildings"):
        for R in b_out:
            Q = TL(R)
            sub.poly([[(x + sh, y - sh) for x, y in Q]], fill=B2_COL["shadow"], alpha=0.25)
            sub.poly([Q], fill=B2_COL["bld_out"], stroke=B2_COL["bld_out_edge"], lw=0.08)
    # ---- 2 zone ground (soft, placeholder for step 2) and water (placeholder for step 3)
    with mpx_grp(sub, "ground", u"zone ground"):
        sub.poly(st, fill=B2_COL["lawn"])
    with mpx_grp(sub, "water", u"Selinos"):
        for R, Hs in water:
            sub.poly([TL(R)] + [TL(H) for H in Hs if len(H) >= 3], fill=B19_COL["water"], stroke=B19_COL["deep"],
                     lw=0.15)
    # ---- 3 car roads inside the zone: asphalt with kerb lines
    with mpx_grp(sub, "roads", u"car roads"):
        for R in C.road_loops:
            Q = TL(R)
            if any(ins(p) for p in R[::max(1, len(R) // 12)]):
                sub.poly([Q], fill=B2_COL["asphalt"], stroke=B2_COL["kerb"], lw=0.1)
    cl = pl23_prep(C)
    n_shared = 0
    for rd, ch, runs in cl["roads"]:                     # pedestrian / calmed / shared streets: paving bands
        if ch not in ("pedestrian", "calmed", "shared"):
            continue
        for P in runs:
            Q = TL(densify(P, 2.0))
            w = [B2_SHARED_W * k] * len(Q)
            with mpx_grp(sub, "roads", u"%s · %s" % (rd.get("name", u"street"), ch)):
                sub.poly([b2_band(Q, w)], fill=B2_COL["paving"], stroke=B2_COL["kerb"], lw=0.08)
                b2_joints(sub, Q, w, B2_JOINT_M * k, B2_COL["joint"])
                if ch != "pedestrian":                   # shared / calmed: cars still pass = dashed middle
                    sub.line(Q, B2_COL["kerb"], 0.08, [0.8, 0.8], cap=0)
            n_shared += 1
    # ---- 4 promenade (variable width) + bike lane + bed paths
    nodes = [h["xy"] for h in C.hubs if h.get("in_study")]
    ends = []                                            # bridge ends (survey m)
    for P in C.bridges:
        if len(P) >= 2:
            ends += [P[0], P[-1]]
    for c_ in C.cross:
        if c_.get("P"):
            ends += [c_["P"][0], c_["P"][1]]
    nodes += ends
    prom, prom_m = [], 0.0
    for P, bed, bank in cl["walk"]:
        D = densify(P, 2.0)
        if bed:
            Q = TL(D)
            w = [B2_BED_W * k] * len(Q)
            with mpx_grp(sub, "paths", u"bed path"):
                sub.poly([b2_band(Q, w)], fill=B2_COL["gravel"], stroke=B2_COL["kerb"], lw=0.05)
            continue
        wm = []
        for p in D:
            d = min([math.hypot(p[0] - q[0], p[1] - q[1]) for q in nodes] or [1e9])
            f = max(0.0, 1.0 - d / B2_PROM_GROW_M)
            wm.append(B2_PROM_W[0] + (B2_PROM_W[1] - B2_PROM_W[0]) * f * f * (3 - 2 * f))   # smooth step
        Q = TL(D)
        w = [x * k for x in wm]
        with mpx_grp(sub, "paths", u"promenade %s" % (bank or u"")):
            sub.poly([b2_band(Q, w)], fill=B2_COL["paving"], stroke=B2_COL["kerb"], lw=0.08)
            b2_joints(sub, Q, w, B2_JOINT_M * k, B2_COL["joint"])
            side = 1.0 if bank == "NE" else -1.0          # bike lane on the land side
            off = [side * (wi / 2.0 + B2_BIKE_W * k / 2.0) for wi in w]
            Bq = [(q[0] + (pl23_offset(Q, o)[i][0] - q[0]), q[1] + (pl23_offset(Q, o)[i][1] - q[1]))
                  for i, (q, o) in enumerate(zip(Q, off))] if len(Q) < 3 else \
                [pl23_offset(Q[max(0, i - 1):i + 2], off[i])[min(i, 1)] for i in range(len(Q))]
            sub.poly([b2_band(Bq, [B2_BIKE_W * k] * len(Bq))], fill=B2_COL["bike"], alpha=0.85)
        prom.append(D)
        prom_m += arclen(D)[-1]
    if not prom:
        flags.append(u"FLAG no promenade: the masterplan gave no riverside walk runs")

    def nearest_prom(p):
        best = None
        for D in prom:
            for q in D:
                d = math.hypot(p[0] - q[0], p[1] - q[1])
                if best is None or d < best[0]:
                    best = (d, q)
        return best

    def crosses_water(a, b):
        return any(in_water((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)) for f in (0.2, 0.4, 0.6, 0.8))

    def path_band(a, b, wm, grp):
        Q = TL(densify([a, b], 2.0))
        w = [wm * k] * len(Q)
        with mpx_grp(sub, "paths", grp):
            sub.poly([b2_band(Q, w)], fill=B2_COL["paving"], stroke=B2_COL["kerb"], lw=0.06)
            b2_joints(sub, Q, w, B2_JOINT_M * k, B2_COL["joint"])
    # ---- 5 connectors: every city street that reaches the zone line gets a path to the promenade
    hits = []
    sb = [bbox(R) for R in study]
    for P in C.roads:
        if not any(hit(bbox(P), b_, 1.0) for b_ in sb):
            continue
        for a, b in zip(P[:-1], P[1:]):
            for R in study:
                for c, d in zip(R, R[1:] + R[:1]):
                    x = b2_seg_x(a, b, c, d)
                    if x and all(math.hypot(x[0] - h[0], x[1] - h[1]) > 20.0 for h in hits):
                        hits.append(x)
    n_conn, far = 0, 0
    for x in hits:
        np_ = nearest_prom(x)
        if np_ is None or np_[0] > B2_CONN_MAX or crosses_water(x, np_[1]):
            far += 1
            continue
        if np_[0] > 2.0:
            path_band(x, np_[1], B2_CONN_W, u"connector to the city %d" % (n_conn + 1))
        n_conn += 1
    # ---- 6 bridges + footbridges (white decks), each end joined to the promenade and to a street
    def deck(P, wm, grp):
        Q = TL(densify(P, 1.0))
        closed = len(P) >= 4 and math.hypot(P[0][0] - P[-1][0], P[0][1] - P[-1][1]) < 0.5
        with mpx_grp(sub, "paths", grp):
            if closed:
                sub.poly([Q], fill=B2_COL["deck"], stroke=B2_COL["deck_edge"], lw=0.12)
            else:
                sub.poly([b2_band(Q, [wm * k] * len(Q))], fill=B2_COL["deck"], stroke=B2_COL["deck_edge"], lw=0.12)
    for i, P in enumerate(C.bridges):
        if len(P) >= 2:
            deck(P, B2_BRIDGE_W, u"bridge %d" % (i + 1))
    for i, c_ in enumerate(C.cross):
        if c_.get("P") and c_["kind"] == "footbridge":
            deck(list(c_["P"]), B2_FOOT_W, u"footbridge %d" % (i + 1))
    road_pts = [p for R in C.road_loops for p in R[::3]]
    loose = 0
    for e in ends:
        np_ = nearest_prom(e)
        joined = False
        if np_ and np_[0] <= 60.0 and not crosses_water(e, np_[1]):
            if np_[0] > 2.0:
                path_band(e, np_[1], B2_CONN_W, u"bridge end to promenade")
            joined = True
        nr = min(road_pts, key=lambda q: math.hypot(q[0] - e[0], q[1] - e[1])) if road_pts else None
        if nr and math.hypot(nr[0] - e[0], nr[1] - e[1]) <= 60.0 and not crosses_water(e, nr):
            if math.hypot(nr[0] - e[0], nr[1] - e[1]) > 2.0:
                path_band(e, nr, B2_CONN_W, u"bridge end to street")
            joined = True
        if not joined:
            loose += 1
    # ---- 7 hub squares: paving with a joint grid
    for h in C.hubs:
        for R in h.get("square") or []:
            if len(R) >= 3:
                with mpx_grp(sub, "hubs", u"square %s" % h["id"]):
                    sub.poly([TL(R)], fill=B2_COL["paving"], stroke=B2_COL["kerb"], lw=0.1)
    # ---- 8 the edge fades out: veils that grow stronger with distance from the zone line
    with mpx_grp(sub, "ground", u"edge fade"):
        prev = st
        a_sum = 0.0
        for d_m, a in B2_FADE:
            grown = [b2_offset_out(R, d_m) for R in study]
            if any(g is None for g in grown):
                break
            grown = b2_union(grown, warn)                # the grown parts merged: no even-odd holes where they meet
            ring_s = [TL(g) for g in grown]
            sub.poly(ring_s + prev, fill="FFFFFF", alpha=a)   # even-odd: the band between prev and this ring
            prev = ring_s
            a_sum += a
        sub.poly([rect(0.0, 0.0, dw, dh)] + prev, fill="FFFFFF", alpha=B2_CONTEXT_VEIL)
    # ---- 9 buildings inside the zone: whole, clear, dark outline, shadow (drawn after the veil: never faded)
    with mpx_grp(sub, "buildings", u"buildings in the zone"):
        for R in b_in:
            Q = TL(R)
            sub.poly([[(x + sh, y - sh) for x, y in Q]], fill=B2_COL["shadow"], alpha=0.35)
            sub.poly([Q], fill=B2_COL["bld_in"], stroke=B2_COL["bld_in_edge"], lw=0.15)
    with mpx_grp(sub, "annotations", u"project zone"):
        for Q in st:
            sub.line(Q + Q[:1], B19_COL["border"], B19_BORDER_MM)
    # ---- 10 names: hubs (bridges, squares) only in step 1
    taken = []
    for h in C.hubs:
        if not h.get("in_study"):
            continue
        s_ = HUB_NAME.get(h["id"], h["id"])
        x, y = T(h["xy"])
        w_ = text_w(s_, B19_NAME_MM, True)
        for dx, dy in ((1.5, 1.0), (-1.5 - w_, 1.0), (1.5, -3.2), (-1.5 - w_, -3.2)):
            b = (x + dx, y + dy, x + dx + w_, y + dy + B19_NAME_MM)
            if not any(hit(b, o) for o in taken) and 0 <= b[0] and b[2] <= dw and 0 <= b[1] and b[3] <= dh:
                taken.append(b)
                sub.text(s_, b[0], b[1], B19_NAME_MM, B19_COL["ink"], bold=True)
                break
    # ---- sheet: plan + legend band (only what step 1 draws) + scale bar + north
    W, H = dw + 2 * B19_M, dh + 2 * B19_M + B19_HEAD + 14.0
    pg = Page(W, H)
    pg.poly([rect(0.0, 0.0, W, H)], fill="FFFFFF")
    blit(pg, sub, B19_M, B19_M + B19_HEAD + 14.0)
    leg = [(u"car road (asphalt)", B2_COL["asphalt"]), (u"pedestrian / shared street", B2_COL["paving"]),
           (u"promenade (3-8 m)", B2_COL["paving"]), (u"bike lane", B2_COL["bike"]),
           (u"path in the stream bed", B2_COL["gravel"]), (u"bridge / footbridge deck", B2_COL["deck"]),
           (u"building in the zone", B2_COL["bld_in"]), (u"zone ground (step 2 designs it)", B2_COL["lawn"]),
           (u"stream (step 3 designs it)", B19_COL["water"])]
    lx, ly = B19_M, B19_M + B19_HEAD + 4.0
    for nm, col in leg:
        pg.poly([rect(lx, ly, lx + 8.0, ly + 4.0)], fill=col, stroke=B2_COL["kerb"], lw=0.1)
        pg.text(nm, lx + 10.0, ly + 0.8, 2.12, B19_COL["ink"])
        lx += 12.0 + text_w(nm, 2.12) + 6.0
    pg.text(u"MIRAQUA · MASTERPLAN · STEP 1 NETWORK", B19_M, B19_M + 8.0, 4.2, B19_COL["ink"], bold=True)
    pg.text(u"drawing language after Greenikka (Arkkitehdit MY, 2020)", B19_M, B19_M + 3.0, 2.12, B19_COL["ink"])
    scale_bar(pg, B19_M + 150.0, B19_M + 3.0, scale, marks=(0.0, 50.0, 100.0, 200.0))
    nx, ny, h_ = W - B19_M - 4.0, B19_M + 2.0, 12.0     # north arrow: survey +y = north (as the survey)
    pg.poly([[(nx, ny + h_), (nx - 2.6, ny + 0.45 * h_), (nx, ny + 0.6 * h_), (nx + 2.6, ny + 0.45 * h_)]],
            fill=B19_COL["ink"])
    pg.line([(nx, ny), (nx, ny + 0.6 * h_)], B19_COL["ink"], 0.25)
    pg.text(u"N", nx, ny + h_ + 1.0, 3.0, B19_COL["ink"], bold=True, align="C")
    fit = (W <= B19_A1[0] and H <= B19_A1[1]) or (W <= B19_A1[1] and H <= B19_A1[0])
    notes += [u"sheet {:.0f} x {:.0f} mm at 1:{:,.0f}: {}".format(W, H, scale, u"fits A1" if fit else
                                                                      u"LARGER than A1 (841 x 594)"),
              u"promenade {:.0f} m ({}-{} m wide), shared streets {}, connectors to city streets {} ({} streets "
              u"too far or across water), bridge ends {} ({} joined to nothing)".format(
                  prom_m, B2_PROM_W[0], B2_PROM_W[1], n_shared, n_conn, far, len(ends), loose),
              u"buildings: {} survey rings merged into {} blocks; {} in the zone (whole, clear), {} outside".format(
                  len(raw), len(blds), len(b_in), len(b_out))]
    if loose:
        flags.append(u"FLAG {} bridge end(s) joined to no path or street".format(loose))
    if not fit:
        warn.append(u"B19 plan: sheet {:.0f} x {:.0f} mm is larger than A1 at 1:{:,.0f}".format(W, H, scale))
    return pg, notes + flags



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
