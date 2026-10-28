# ============================================================ v46 (Aras 27 Oct 17:34, booklet Prompt 3: movement and the city)
# Theme B of the booklet (p.8 how people use it, p.10 how people will move; v50: the heritage loop is drawn in
# 15j_r28_heritage.py, on the survey, north up): every map is
# the whole site frame at ONE scale, 1:10,000 on the booklet page (B_DEN), on the frame's own axes (one north), with
# the scale bar and north arrow under the map (b_foot), never on it. The base is crisp, in the masterplan's tones and
# Prompt 3's layer order (ground, green, water, buildings, bridges, roads: b_base); analysis stays crisp, a proposal
# is drawn soft: tints laid over the base by multiplying (Tint, PDF blend mode), haloes (soft_line), no hard outline.
# v50 (MIRAQUA 28 Oct, P07.3, P09.1, G6): the p.07 maps and the proposal are drawn crisp in
# parts/15i_r28_movement.py (draw_mv_today, draw_mv_proposal; soft_disc, reach_t and draw_commercial_spines are gone).
# The proposal's walkable reach is computed on the street network with the masterplan (mv_reach). write_city_context gives the city link's shops plan its light context: homes by the sections' building
# types, streets by class, the stream and bridges K1-K6.
B_DEN = 10000           # theme-B maps at 1:10,000 on the booklet page: the site frame is 284.5 x 52.9 mm
B_SB_M = 400.0          # m: the scale bar under each of them (four parts of 100 m)
CITY_CTX = os.path.join(SELINUS_RES_DIR, "city_context.json")    # read by bergama_city_link v2 (cached/)
CTX_HOUSING = {"traditional": u"old town", "regular": u"planned low-rise", "block": u"apartment block",
               "selfbuilt": u"small / shack"}    # a home by the sections' building types (draw_typology_key)
SHOP_AMEN = ("cafe", "restaurant", "fast_food", "bar", "pub", "ice_cream")   # with shop=*: the city link's shops
B_BASE_LEG = [("box", MPL["water"], u"Selinos stream"), ("box", MPL["bld"], u"Building"),
              ("box", MPL["her"], u"Heritage building"),
              R28_STUDY_LEG]   # v49.1 (Prompt 8): b_base's tones in every page's legend; v50 (G8): + the study area


class Tint(tuple):
    """v46: a proposal colour the PDF lays over what is under it by multiplying (blend mode Multiply, _pdf_page): the
    base shows through and overlapping fields darken. Rhino bakes it as the plain colour."""
    mul = True


def tint(c, t=0.0):
    """v46: colour c faded t of the way to white, as a multiplying Tint."""
    return Tint(mix(c, WHITE, t))


def soft_line(B, P, col, k, L, order, w_mm=2.4, t=0.5):
    """v46: a proposal line drawn soft: three multiplying strokes of col, from a pale halo w_mm wide on the booklet
    page to a narrow core (t = how pale the core is): no hard edge, no width that reads as decided."""
    for f, dt in ((1.0, 0.36), (0.6, 0.18), (0.28, 0.0)):
        B.line(P, tint(col, min(0.97, t + dt)), L, order, bk_lw(w_mm * f, k))


def b_view(F, x, ytop, U):
    """v46: a theme-B map: the whole frame F at 1:10,000 on the booklet page, its top-left corner at (x, ytop); k =
    board units per booklet mm of a drawing 120 U wide (as draw_edge_build). Returns (View, k, board units per metre,
    the map's rectangle)."""
    k = 120.0 * U / BK_AW
    ss = 1000.0 * k / B_DEN
    return View(F, ss, x, ytop), k, ss, (x, ytop - F.h * ss, x + F.w * ss, ytop)


def b_foot(B, F, x, yb, ss, k, L, Lm=B_SB_M):
    """v46: under a theme-B map whose bottom edge is at yb: the scale bar (0-Lm m, "m" beside it) and the north
    arrow beside it, both clear of the map and of any caption. Returns the y below them. v49.1 (Prompt 8): the bar
    starts 1 mm in from the map's left edge: its "0" is centred on the bar's end and the crops end 0.5 mm left of
    the map, so half the "0" was cut off; Lm (v49.1): the heritage loop's strips at 1:5,000 take 200 m."""
    x += 1.0 * k
    low = draw_scalebar_bk(B, x, yb - 2.5 * k, ss, Lm, k, L)
    ny = yb - 5.5 * k
    hw = draw_north_at(B, F, x + Lm * ss + 10.0 * k, ny, 4.0, k, L)
    return min(low, ny - hw)


def b_base(S, CB, V, k, L, colfn=None):
    """v46: the base of a theme-B map through ClipB CB, crisp, in the masterplan's tones and Prompt 3's layer order:
    green (satellite trees and fields, mapped parks and woods), water (the stream, its edge, the covered course dashed;
    street surfaces under it and decks over it, as the stream edge plan's base r28e_base), buildings (colfn, else plain and heritage), bridges,
    street edges. The ground (white) is the caller's."""
    lc = getattr(S, "lc", {}) or {}
    for key, col in (("trees", MPL["tree"]), ("farmland", MPL["field"]), ("orchard", MPL["field"])):
        rings = lc.get(key) or []
        for i in range(0, len(rings), 400):
            CB.fill(V.Ps(rings[i:i + 400]), col, L, 3)
    for z in S.zones:
        if z["kind"] in ("green", "agri"):
            CB.fill(V.Ps(z["Ps"] + z["Hs"]), MPL["field"] if z["kind"] == "agri" else (
                MPL["tree"] if z.get("sub") == "wood" else MPL["park"]), L, 4)
    for rg_ in getattr(S, "road_net", None) or []:
        CB.fill(V.Ps([rg_["P"]] + rg_["H"]), MPL["road"], L, 5)
    for wt in S.water:
        CB.fill(V.Ps([wt["P"]] + wt.get("H", [])), MPL["water"], L, 6)
    for P in getattr(S, "water_outline", []) or []:
        CB.line(V.P(P), MPL["water_edge"], L, 7, bk_lw(0.18, k))
    for q in getattr(S, "decks", []) or []:               # streets on decks over the water stay above it
        CB.fill([V.P(q)], MPL["road"], L, 8)
    for P in getattr(S, "covered", []) or []:
        for d in dashes(V.P(P), 1.6 * k, 0.9 * k):
            CB.line(d, MPL["water_edge"], L, 8, bk_lw(0.3, k))
    her = lambda u: u.get("fabric") in ("monument", "sacred")
    mini_buildings(S, CB, V, L, colfn or (lambda u: MPL["her"] if her(u) else MPL["bld"]), order=10)
    for P in getattr(S, "bridges", []) or []:
        CB.line(V.P(P), MPL["ink_dark"], L, 11, bk_lw(0.3, k))
    for P in getattr(S, "road_lines_net", []) or []:
        CB.line(V.P(P), MPL["road_edge"], L, 12, bk_lw(0.12, k))
    for r_ in S.roads:
        if not r_.get("w"):
            CB.line(V.P(r_["P"]), MPL["road_edge"], L, 12, bk_lw(0.12, k))
    draw_r28_study(S, CB, V, k, L)                        # v50 (G8): the study area's outline on every base


def b_frame(B, r, k, L):
    """v46: the site frame's line round a theme-B map (its rectangle r)."""
    B.line(rect(*r) + [(r[0], r[1])], INK, L, 70, bk_lw(0.25, k))


def mv_reach(R, starts, rmax):
    """v46: walkable reach: the walking cost (flat-ground metres; Tobler slope on the survey terrain where the network
    has heights) from the nearest start point to every node of the walking network WITH the proposal (walk_a: today's
    streets and footways and the masterplan's crossings), out to rmax; each start joins the network at its nearest
    node within MV_OPT["snap"], that distance counted. Returns {node: cost}."""
    pieces, xy = R["pieces"], R["xy"]
    z = getattr(pieces, "z", None) or {}
    adj = {}
    for p in pieces:
        if not p["walk"] or p["L"] <= 0:
            continue
        a, b = p["a"], p["b"]
        za, zb = z.get(a), z.get(b)
        g = (zb - za) / p["L"] if za is not None and zb is not None else 0.0
        adj.setdefault(a, []).append((b, p["L"] * tobler_factor(g)))
        adj.setdefault(b, []).append((a, p["L"] * tobler_factor(-g)))
    hq, cost = [], {}
    for sx, sy in starts:
        best = min(((xy[n][0] - sx) ** 2 + (xy[n][1] - sy) ** 2, n) for n in adj) if adj else None
        if best and best[0] <= MV_OPT["snap"] ** 2:
            heapq.heappush(hq, (math.sqrt(best[0]), best[1]))
    while hq:
        d, n = heapq.heappop(hq)
        if n in cost:
            continue
        cost[n] = d
        for m, c in adj[n]:
            if m not in cost and d + c <= rmax:
                heapq.heappush(hq, (d + c, m))
    return cost


# v50 (MIRAQUA 28 Oct, P07.3, P09.1): draw_mv_today and draw_mv_proposal are redrawn in parts/15i_r28_movement.py;
# reach_t, soft_disc, REACH_STEP and the commercial spines map (draw_commercial_spines, P09.3) are gone.


# ------------------------------------------------------------ the city heritage loop (booklet page "The heritage loop")
# v50 (MIRAQUA 28 Oct, P20.1-P20.3, D2): draw_heritage_loop is redrawn in parts/15j_r28_heritage.py (crops
# drw_heritage_loop and the NEW drw_heritage_key); the v46/v49.1 two-strip drawing on the site frame is gone.


# ------------------------------------------------------------ the city link's shops plan: its light context
def ctx_housing(u):
    """v46: a building's class on the city link's shops plan: a home by the sections' building types (old town,
    planned low-rise, apartment block, small / shack; mixed use = shop below, home above), else "other"."""
    if u.get("cat") == "mixed":
        return u"shop below"
    if u.get("cat") == "residential":
        return CTX_HOUSING.get(typo_kind(u.get("fabric"), u.get("cat")), u"other")
    return u"other"


def write_city_context(S):
    """v46: cached/selinus_board/city_context.json for bergama_city_link v2's shops plan (Prompt 3, p.9): the site
    frame (centre, angle, local extent) and, in metres on the frame's own axes from its lower-left corner (u - u0,
    v - v0; 0.1 m), the buildings by housing type, the streets by class (OSM highway: main, secondary, lane; footways
    = path), the water, the covered course, bridges K1-K6 (point, direction across the stream), the shops (OSM
    shop=* or a café / restaurant / bar amenity: nodes, and buildings at the mean of their corners, as the city link's
    own shop points), the tones and the walking radius of the movement method."""
    F = S.F

    def loc(P):
        out = []
        for x_, y_ in P:
            u_, v_ = F.local(x_, y_)
            out.append([round(u_ - F.u0, 1), round(v_ - F.v0, 1)])
        return out
    bld, n_ty = [], {}
    for u in S.bld:
        P0 = u["parts"][0] if u.get("parts") else None
        if not P0 or not any(F.inside(*p) for p in P0[::max(1, len(P0) // 4)]):
            continue
        ty = ctx_housing(u)
        n_ty[ty] = n_ty.get(ty, 0) + 1
        bld.append([ty, [loc(P) for P in u["parts"]], [loc(H) for H in (u.get("holes") or [])]])
    roads = [[MV_CLASS.get((r_.get("tags") or {}).get("highway"), "lane"), loc(r_["P"])] for r_ in S.roads] + \
            [["path", loc(r_["P"])] for r_ in S.paths]
    c, s = math.cos(-F.ang), math.sin(-F.ang)
    bridges = []
    for kk, nm, bx, by in BRIDGES_K:
        if F.inside(bx, by):
            n_ = stream_normal(S, bx, by) or (0.0, 1.0)
            bridges.append([kk, loc([(bx, by)])[0], [round(c * n_[0] - s * n_[1], 4), round(s * n_[0] + c * n_[1], 4)]])
    shops, osm = [], getattr(S, "osm", None)
    if osm:
        for ll, tg in osm.get("pois") or []:
            if tg.get("shop") or tg.get("amenity") in SHOP_AMEN:
                p = to_dwg(*ll)
                if F.inside(*p):
                    shops.append(loc([p])[0])
        for refs, tg in osm["ways"].values():
            if refs and (tg.get("shop") or tg.get("amenity") in SHOP_AMEN):
                P = [q for q in (osm["P"](r_) for r_ in (refs[:-1] if len(refs) > 1 and refs[0] == refs[-1] else refs))
                     if q]
                if P:
                    p = (sum(q[0] for q in P) / len(P), sum(q[1] for q in P) / len(P))
                    if F.inside(*p):
                        shops.append(loc([p])[0])
    tones = dict((CTX_HOUSING[t_], crop_hex(TYPO[t_]["tone"])) for t_ in CTX_HOUSING)
    tones[u"shop below"] = crop_hex(mix(CAT["mixed"][1], WHITE, 0.55))
    tones[u"other"] = crop_hex(mix(MPL["bld"], WHITE, 0.45))
    out = dict(script=SCRIPT_VERSION, run_time=time.strftime("%Y-%m-%d %H:%M:%S"),
               frame=dict(cx=F.cx, cy=F.cy, ang=F.ang, u0=F.u0, v0=F.v0, w=F.w, h=F.h),
               buildings=bld, roads=roads, water=[[loc(wt["P"])] + [loc(H) for H in wt.get("H", [])] for wt in S.water],
               covered=[loc(P) for P in getattr(S, "covered", []) or []], bridges=bridges,
               shops=shops if osm else None, tones=tones,
               r_walk=MV_OPT["r_walk"],
               note="metres on the site frame's axes from its lower-left corner; building types = the sections' "
                    "(typo_kind of the survey fabric), mixed use = shop below; streets by OSM highway class")
    os.makedirs(SELINUS_RES_DIR, exist_ok=True)
    with open(CITY_CTX, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, separators=(",", ":"))
    LOG.append("city_context.json: {} buildings ({}), {} streets, {} bridges, {} shops.".format(
        len(bld), ", ".join("{} {}".format(v_, k_) for k_, v_ in sorted(n_ty.items())), len(roads), len(bridges),
        len(shops) if osm else "no OSM, no"))
