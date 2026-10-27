# ============================================================ v46 (Aras 27 Oct 17:34, booklet Prompt 3: movement and the city)
# Theme B of the booklet (p.8 how people use it, p.10 how people will move) and the heritage loop (p.23): every map is
# the whole site frame at ONE scale, 1:10,000 on the booklet page (B_DEN), on the frame's own axes (one north), with
# the scale bar and north arrow under the map (b_foot), never on it. The base is crisp, in the masterplan's tones and
# Prompt 3's layer order (ground, green, water, buildings, bridges, roads: b_base); analysis stays crisp, a proposal
# is drawn soft: tints laid over the base by multiplying (Tint, PDF blend mode), haloes and fading fields (soft_line,
# soft_disc), no hard outline. The proposal's walkable reach is computed on the street network with the masterplan
# (mv_reach). write_city_context gives the city link's shops plan its light context: homes by the sections' building
# types, streets by class, the stream and bridges K1-K6.
B_DEN = 10000           # theme-B maps at 1:10,000 on the booklet page: the site frame is 284.5 x 52.9 mm
B_SB_M = 400.0          # m: the scale bar under each of them (four parts of 100 m)
REACH_STEP = 100.0      # m: the steps of walkable reach on the proposal map (flat-ground metres, Tobler slope)
CITY_CTX = os.path.join(SELINUS_RES_DIR, "city_context.json")    # read by bergama_city_link v2 (cached/)
CTX_HOUSING = {"traditional": u"old town", "regular": u"planned low-rise", "block": u"apartment block",
               "selfbuilt": u"small / shack"}    # a home by the sections' building types (draw_typology_key)
SHOP_AMEN = ("cafe", "restaurant", "fast_food", "bar", "pub", "ice_cream")   # with shop=*: the city link's shops


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


def soft_disc(B, x, y, r, col, L, order, n=6, t0=0.3, t1=0.94):
    """v46: a fading field round (x, y), r board units: n rings side by side (never stacked), multiplying tints of col
    from t0 at the centre to t1 at the rim."""
    for i in range(n):
        ra, rb = r * i / float(n), r * (i + 1) / float(n)
        rings = [circle_pts(x, y, rb, 40)] + ([circle_pts(x, y, ra, 40)] if ra > 0 else [])
        B.fill(rings, tint(col, t0 + (t1 - t0) * i / float(max(1, n - 1))), L, order)


def b_view(F, x, ytop, U):
    """v46: a theme-B map: the whole frame F at 1:10,000 on the booklet page, its top-left corner at (x, ytop); k =
    board units per booklet mm of a drawing 120 U wide (as draw_edge_build). Returns (View, k, board units per metre,
    the map's rectangle)."""
    k = 120.0 * U / BK_AW
    ss = 1000.0 * k / B_DEN
    return View(F, ss, x, ytop), k, ss, (x, ytop - F.h * ss, x + F.w * ss, ytop)


def b_foot(B, F, x, yb, ss, k, L):
    """v46: under a theme-B map whose bottom edge is at yb: the scale bar (0-400 m, "m" beside it) and the north
    arrow beside it, both clear of the map and of any caption. Returns the y below them."""
    low = draw_scalebar_bk(B, x, yb - 2.5 * k, ss, B_SB_M, k, L)
    ny = yb - 5.5 * k
    hw = draw_north_at(B, F, x + B_SB_M * ss + 10.0 * k, ny, 4.0, k, L)
    return min(low, ny - hw)


def b_base(S, CB, V, k, L, colfn=None):
    """v46: the base of a theme-B map through ClipB CB, crisp, in the masterplan's tones and Prompt 3's layer order:
    green (satellite trees and fields, mapped parks and woods), water (the stream, its edge, the covered course dashed;
    street surfaces under it and decks over it, as draw_eb_base), buildings (colfn, else plain and heritage), bridges,
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


def reach_t(b, nb):
    """v46: how pale reach step b of nb is (0 = the strongest, next to a hub)."""
    return 0.12 + 0.72 * b / float(max(1, nb - 1))


# ------------------------------------------------------------ p.8 walking / driving today, one map each
def draw_mv_today(S, B, x, y, U, R, MV, key, title, cap):
    """v46 (Prompt 3, p.8): walking or driving today as its own map at the theme's one scale (was a half-width inset
    at its own scale): the whole site frame at 1:10,000, the masterplan base, only the key streets in colour and named
    (draw_mv_key), the scale bar and north arrow under it. Returns the y below its crop."""
    L = "LU_BOARD::HowPeopleUseIt"
    F = S.F
    B.text(title, x, y, 0.5 * U, INK, L, font=FONT_TITLE, bold=True)
    V, k, ss, r = b_view(F, x, y - 0.8 * U, U)
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 1)
    b_base(S, CB, V, k, L)
    names_, key_ = draw_mv_key(S, CB, V, R, MV, key, F, L, bk_hk(8.0, k), r)
    b_frame(B, r, k, L)
    low = b_foot(B, F, x, r[1], ss, k, L)
    if key_:
        low = draw_label_key(B, key_, x, low - 0.8 * k, r[2] - x, bk_hk(7.5, k), L)
    crop_panel(CROP_MV.get(key, key), x - 0.5 * k, low - 0.5 * k, r[2] + 0.5 * k, r[3] + 0.5 * k,
               cap.format(len(names_)), crop_scale(ss))
    return low - 0.5 * k


# ------------------------------------------------------------ p.10 the proposal: reach on foot, soft
def draw_mv_proposal(S, B, x, y, w, U, M):
    """v46 (Prompt 3, p.10; replaces v44's): THE PROPOSAL, the whole site frame at 1:10,000 on the frame's axes, the
    base crisp and the proposal soft over it: walkable reach from the masterplan's hubs as a gradient along the
    streets, footways and new crossings (mv_reach on the board's network with the masterplan's proposal, 100 m steps
    out to the movement method's walking radius MV_OPT r_walk), the changed roads, the rerouted truck route and the
    bus routes as soft bands (later steps in soft dashes), the crossings and the hubs as fading fields; every changed
    road with its note and its walking / driving index today -> with the proposal. Returns the y below."""
    L = "LU_BOARD::Proposal"
    F = S.F
    B.text("THE PROPOSAL · REACH ON FOOT · ROADS · CROSSINGS · HUBS", x, y, 1.05 * U, INK, L, font=FONT_TITLE,
           bold=True)
    V, k, ss, r = b_view(F, x, y - 1.2 * U, U)
    h7, h9 = bk_hk(7.5, k), bk_hk(9.0, k)
    CB = ClipB(B, r)
    MR = mv_with_masterplan(S, M)
    R2 = MR.get("R") if MR else None
    B.fill([rect(*r)], WHITE, L, 1)
    b_base(S, CB, V, k, L)
    labels, taken, leg, seen = [], [], [], set()
    rw = MV_OPT["r_walk"]
    nb = max(1, int(round(rw / REACH_STEP)))
    hub_xy = [p for p in (_xy1(h.get("xy")) for h in M.get("hubs") or []) if p]
    if R2 and hub_xy:                                     # reach on foot from the hubs: the gradient
        cost = mv_reach(R2, hub_xy, rw)
        pieces = R2["pieces"]

        def band(pi):
            p = pieces[pi]
            c_ = min(cost.get(p["a"], 1e12), cost.get(p["b"], 1e12))
            return min(nb - 1, int(c_ // REACH_STEP)) if c_ <= rw else None
        km = [0.0] * nb
        for P, b_ in _runs(R2["chains"]["walk_a"], pieces, R2["xy"], band, set(R2["inside"]), F):
            soft_line(CB, V.P(P), PROP_C, k, L, 20 + nb - b_, w_mm=3.2 - 1.6 * b_ / float(max(1, nb - 1)),
                      t=reach_t(b_, nb))
            km[b_] += pl_length(P) / 1000.0
        for b_ in sorted(set((0, nb // 2 - 1, nb - 1))):
            leg.append(("thick", tint(PROP_C, reach_t(b_, nb)), u"Reach on foot · {:.0f}-{:.0f} m from a hub".format(
                b_ * REACH_STEP, (b_ + 1) * REACH_STEP)))
        LOG.append("Proposal map: walkable reach from {} hubs (Tobler, with the masterplan's crossings): {} km of "
                   "street and footway in the frame within {:.0f} m.".format(
                       len(hub_xy), " / ".join("{:.1f}".format(sum(km[:i + 1])) for i in range(nb)), rw))
    else:
        LOG.append("Proposal map: no street network with the masterplan (OSM) or no hubs, so no walkable reach drawn.")
    for rd in M.get("roads") or []:
        P = _xy_list(rd.get("xy"))
        if len(P) < 2:
            continue
        ch = rd.get("change", "kept")
        nm_, col = MP_CHANGE.get(ch, (ch, INK2))
        for run in F.clip_line(P):
            soft_line(CB, V.P(run), col, k, L, 40, w_mm=2.2, t=0.3)
        if ch not in seen:
            seen.add(ch)
            leg.append(("thick", col, u"Road " + nm_))
        idx = []
        if R2:
            for k_, lab in (("walk", u"walk"), ("car", u"car")):
                b_, a_ = mv_line_index(R2, P, k_ + "_b"), mv_line_index(R2, P, k_ + "_a")
                if b_ is not None and a_ is not None:
                    idx.append(u"{} {:.0f}→{:.0f}".format(lab, b_, a_))
        q, t = pl_point_at(P, pl_length(P) / 2.0)
        if F.inside(q[0], q[1]):
            px, py = V.p(q[0], q[1])
            labels.append(([rd.get("name", ""), rd.get("note", ""), u" · ".join(idx)], px, py, h7, INK))
    tr = M.get("truck_route")
    if tr and len(_xy_list(tr.get("xy"))) >= 2:
        P = _xy_list(tr["xy"])
        for run in F.clip_line(P):
            for d in dashes(V.P(run), 3.2 * k, 1.8 * k):
                soft_line(CB, d, INK, k, L, 41, w_mm=1.8, t=0.4)
        leg.append(("dash", INK, u"Truck route, rerouted"))
        q, t = pl_point_at(P, pl_length(P) * 0.35)
        if F.inside(q[0], q[1]):
            px, py = V.p(q[0], q[1])
            labels.append(([tr.get("name", u"truck route"), tr.get("note", "")], px, py, h7, INK))
    else:
        LOG.append("Proposal map: truck route pending in the masterplan (movement.truck_route is null).")
    for rt in M.get("routes") or []:                      # e.g. the town bus line extended to K4 as a later step
        P = _xy_list(rt.get("xy"))
        if len(P) < 2:
            continue
        later = bool(rt.get("later")) or str(rt.get("status", "")).lower() in ("later", "proposed", "future")
        for run in F.clip_line(P):
            for d in (dashes(V.P(run), 2.0 * k, 1.6 * k) if later else [V.P(run)]):
                soft_line(CB, d, TRANSIT_C, k, L, 42, w_mm=1.4, t=0.3)
        lk = u"Bus route, later step" if later else u"Bus route"
        if lk not in seen:
            seen.add(lk)
            leg.append(("dash" if later else "thick", TRANSIT_C, lk))
        q, t = pl_point_at(P, pl_length(P) / 2.0)
        if F.inside(q[0], q[1]):
            px, py = V.p(q[0], q[1])
            labels.append(([rt.get("name", ""), rt.get("note", "")], px, py, h7, TRANSIT_C))
    for c in M.get("crossings") or []:
        p = _xy1(c.get("xy"))
        if not p or not F.inside(p[0], p[1]):
            continue
        px, py = V.p(p[0], p[1])
        nrm = stream_normal(S, p[0], p[1]) or (0.0, 1.0)
        a_ = V.p(p[0] + nrm[0], p[1] + nrm[1])
        ln = math.hypot(a_[0] - px, a_[1] - py) or 1.0
        e = ((a_[0] - px) / ln * 2.4 * k, (a_[1] - py) / ln * 2.4 * k)
        kind = c.get("kind", "footbridge")
        ccol = PROP_C if kind != "bridge kept" else INK
        if kind == "stepping stones":
            for f in (-0.8, 0.0, 0.8):
                soft_disc(CB, px + e[0] * f, py + e[1] * f, 0.8 * k, ccol, L, 45, n=3, t0=0.15, t1=0.7)
        else:
            soft_line(CB, [(px - e[0], py - e[1]), (px + e[0], py + e[1])], ccol, k, L, 45, w_mm=1.6, t=0.1)
        taken.append((px - 2.4 * k, py - 2.4 * k, px + 2.4 * k, py + 2.4 * k))
        lk = u"Crossing: " + kind
        if lk not in seen:
            seen.add(lk)
            leg.append(("cdot" if kind == "stepping stones" else "ktick", ccol, lk))
        labels.append(([c.get("name", ""), c.get("note", "")], px, py, h7, INK))
    for hb in M.get("hubs") or []:                        # the role as the masterplan writes it, never assumed here
        p = _xy1(hb.get("xy"))
        if not p or not F.inside(p[0], p[1]):
            continue
        px, py = V.p(p[0], p[1])
        role = str(hb.get("role", "") or "")
        col = HUB_C.get(role, INK)
        rr = (4.4 if role == "transit" else 3.6) * k
        soft_disc(CB, px, py, rr, col, L, 50, n=6, t0=0.1, t1=0.9)
        taken.append((px - 0.5 * rr, py - 0.5 * rr, px + 0.5 * rr, py + 0.5 * rr))
        lk = u"Hub · " + (role or u"square")
        if lk not in seen:
            seen.add(lk)
            leg.append(("dot", col, lk))
        bus = u""
        if hb.get("bus_stop"):
            try:
                bus = u"bus: {} · {:.0f} m".format(hb["bus_stop"], float(hb.get("bus_stop_m")))
            except Exception:
                bus = u"bus: {}".format(hb["bus_stop"])
        labels.append(([u"{}{}".format(hb.get("name", ""), u" · " + role if role else u""),
                        u"sub-hub in the bed" if hb.get("sub_hub") else u"", bus], px, py, h7, INK))
    key = place_labels(B, labels, taken, L, bounds=r)
    b_frame(B, r, k, L)
    low = b_foot(B, F, x, r[1], ss, k, L)
    if key:
        low = draw_label_key(B, key, x, low - 0.8 * k, r[2] - x, h7, L)
    if R2 and hub_xy:
        B.text(u"reach on foot from the hubs along streets, footways and the new crossings, slope counted (Tobler) · "
               u"{:.0f} m steps to {:.0f} m · computed ".format(REACH_STEP, rw) + bcite(
                   "Reach on foot: the shortest walking cost from the nearest masterplan hub along the OSM streets and "
                   "footways and the masterplan's crossings (the board's movement network with the proposal), each "
                   "street piece timed by Tobler (1993) on the survey terrain and given as flat-ground metres, in "
                   "{:.0f} m steps to {:.0f} m, the walking radius of the movement method (bergama_movement v1). "
                   "Computed; weakest assumption: every crossing open and every footway walkable all year.".format(
                       REACH_STEP, rw)), x, low - 1.2 * k - h7, h7, INK2, L, font=FONT_TITLE)
        low -= 2.2 * k + h7
    leg += [("box", MPL["water"], u"Selinos stream"), ("box", MPL["bld"], u"Building")]
    crop_panel("proposal", x - 0.5 * k, low - 0.5 * k, r[2] + 0.5 * k, r[3] + 0.5 * k,
               u"The proposal · reach on foot from the hubs · roads, crossings, routes", crop_scale(ss), crop_legend(leg))
    ly = draw_legend_items(B, leg, x, low - 1.0 * U, r[2] - x, U, L, h=0.4)
    return ly - 0.4 * U


# ------------------------------------------------------------ p.10 the commercial spines
def draw_commercial_spines(S, B, x, y, w, U):
    """v46 (Prompt 3, p.10; v44's drawing at the theme's one scale): COMMERCIAL SPINES, the whole site frame at
    1:10,000 on the frame's axes, crisp (analysis): the masterplan base with commerce and mixed-use buildings in
    colour; the primary spines (the 2 named streets with 6+ shops within 30 m) thick, the secondary ones (next 4 with
    3+) dashed, each named with its count (build_corridors); under the map the scale bar and north arrow, then the
    caption in full (v45's bar sat on the map and over the caption). Returns the y below."""
    L = "LU_BOARD::CommercialSpines"
    F = S.F
    B.text("COMMERCIAL SPINES · SHOPS ALONG EACH STREET", x, y, 1.05 * U, INK, L, font=FONT_TITLE, bold=True)
    V, k, ss, r = b_view(F, x, y - 1.2 * U, U)
    h7, h9 = bk_hk(7.5, k), bk_hk(9.0, k)
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 1)
    b_base(S, CB, V, k, L, lambda u: CAT[u["cat"]][1] if u["cat"] in ("commercial", "mixed") else MPL["bld"])
    col = CAT["commercial"][1]
    pcol = mix(col, INK, 0.25)
    labels = []
    for grp, prim in [(g, False) for g in S.corr_secondary] + [(g, True) for g in S.corr_primary]:
        longest = None
        for P in grp["Ps"]:
            for run in F.clip_line(P):
                if prim:
                    CB.line(V.P(run), pcol, L, 15, bk_lw(0.8, k))
                else:
                    for d in dashes(V.P(run), 2.2 * k, 1.4 * k):
                        CB.line(d, col, L, 14, bk_lw(0.4, k))
                if longest is None or pl_length(run) > pl_length(longest):
                    longest = run
        if longest and grp["label"] != "an unnamed street":
            q, t = pl_point_at(longest, pl_length(longest) / 2.0)
            px, py = V.p(q[0], q[1])
            labels.append(([u"{} · {} shops".format(grp["label"], grp["n"])], px, py, h9 if prim else h7,
                           pcol if prim else INK))
    key = place_labels(B, labels, [], L, bounds=r)
    b_frame(B, r, k, L)
    low = b_foot(B, F, x, r[1], ss, k, L)
    if key:
        low = draw_label_key(B, key, x, low - 0.8 * k, r[2] - x, h7, L)
    B.text(u"shops = commerce and mixed-use buildings and shop places within 30 m of the street " + bcite(
        "Commercial spines: OSM streets grouped by name; commerce and mixed-use buildings (survey, OSM) and Overture/OSM "
        "shop places within 30 m counted per street; primary = the 2 streets with 6 or more, secondary = the next 4 "
        "with 3 or more (selinus_board build_corridors, as on the Panel Review 1 boards)."), x, low - 1.2 * k - h7, h7,
        INK2, L, font=FONT_TITLE)
    low -= 2.2 * k + h7
    leg = [("line", pcol, u"Primary commercial spine · 6+ shops"), ("dash", col, u"Secondary commercial spine · 3+ shops"),
           ("box", CAT["commercial"][1], u"Commerce"), ("box", CAT["mixed"][1], u"Mixed use"),
           ("box", MPL["water"], u"Selinos stream")]
    crop_panel("commercial_spine", x - 0.5 * k, low - 0.5 * k, r[2] + 0.5 * k, r[3] + 0.5 * k,
               u"Commercial spines · shops per street", crop_scale(ss), crop_legend(leg))
    ly = draw_legend_items(B, leg, x, low - 1.0 * U, r[2] - x, U, L, h=0.4)
    return ly - 0.4 * U


# ------------------------------------------------------------ p.23 the city heritage loop
def draw_heritage_loop(S, B, x, y, w, U):
    """v46 (Prompt 3: one scale, frame and north with the movement maps; the loop is a proposal, drawn soft): the city
    heritage loop on the whole site frame at 1:10,000: gondola valley station (to the Acropolis) -> Red Hall -> K3
    Tabakhane -> along the stream (the loop's spine) -> K4 Ulu Cami and Tabaklar Hamamı -> the bazaar axis -> Bergama
    Museum -> the Asklepieion. Stops beyond the frame are named at an arrow where the loop leaves it, each with its
    straight distance (calculated). The order of the loop, not a walked route. Returns the y below."""
    L = "LU_BOARD::HeritageLoop"
    F = S.F
    B.text("CITY HERITAGE LOOP", x, y, 1.05 * U, INK, L, font=FONT_TITLE, bold=True)
    V, k, ss, r = b_view(F, x, y - 1.2 * U, U)
    h7, h9 = bk_hk(7.5, k), bk_hk(9.0, k)
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 1)
    b_base(S, CB, V, k, L)
    acc = MARK_C
    order = [k_ for k_, nm, p, src in HER_LOOP]
    pts = dict((k_, p) for k_, nm, p, src in HER_LOOP)
    num = dict((k_, j + 1) for j, k_ in enumerate(order))
    name = dict((k_, nm) for k_, nm, p, src in HER_LOOP)
    streams = [P for P in (getattr(S, "selinus", None) or []) if len(P) >= 2]
    main = max(streams, key=pl_length) if streams else None
    walk = []
    if main:                                              # K3 -> K4 along the stream: the loop's spine
        s0, s1 = pl_chainage(main, *pts["K3"]), pl_chainage(main, *pts["K4"])
        nn = max(2, int(abs(s1 - s0) // 10.0))
        walk = [pl_point_at(main, s0 + (s1 - s0) * i / float(nn))[0] for i in range(nn + 1)]
    for a, b in zip(order[:-1], order[1:]):               # soft: dashes between the stops, a band along the stream
        if (a, b) == ("K3", "K4"):
            soft_line(CB, V.P(walk or [pts["K3"], pts["K4"]]), acc, k, L, 30, w_mm=2.6, t=0.2)
        else:
            for d in dashes(V.P([pts[a], pts[b]]), 2.0 * k, 1.3 * k):
                soft_line(CB, d, acc, k, L, 30, w_mm=1.6, t=0.3)
    ins = [F.inside(*pts[k_]) for k_ in order]
    groups, j = [], 0                                     # (the stop inside, the stops beyond it in loop order)
    while j < len(order):
        if ins[j]:
            j += 1
            continue
        j0 = j
        while j < len(order) and not ins[j]:
            j += 1
        if j0 > 0:
            groups.append((order[j0 - 1], order[j0:j]))
        elif j < len(order):
            groups.append((order[j], list(reversed(order[j0:j]))))
    labels, taken = [], []
    for k_ in order:
        if not F.inside(*pts[k_]):
            continue
        px, py = V.p(*pts[k_])
        rd = 1.7 * k
        B.fill([circle_pts(px, py, rd, 20)], acc, L, 60)
        B.text(str(num[k_]), px, py, h7, WHITE, L, order=61, font=FONT_TITLE, bold=True, align="MC")
        taken.append((px - rd, py - rd, px + rd, py + rd))
        labels.append(([name[k_]], px, py, h7, INK))
    for nm, p in HER_DOTS:
        if not F.inside(*p):
            LOG.append(u"Heritage loop: {} lies outside the site frame, so it is not on the map.".format(nm))
            continue
        px, py = V.p(*p)
        B.fill([circle_pts(px, py, 0.6 * k, 12)], INK, L, 58)
        taken.append((px - 0.6 * k, py - 0.6 * k, px + 0.6 * k, py + 0.6 * k))
        labels.append(([nm], px, py, h7, INK2))
    for a, run in groups:                                 # where the loop leaves the frame: an arrow, the stops beyond
        A_, Bp = V.p(*pts[a]), V.p(*pts[run[0]])
        cut = clip_rect_line([A_, Bp], r)
        if not cut:
            continue
        ux, uy = Bp[0] - A_[0], Bp[1] - A_[1]
        ul = math.hypot(ux, uy) or 1.0
        ux, uy = ux / ul, uy / ul
        tip = (cut[0][-1][0] - ux * 0.6 * k, cut[0][-1][1] - uy * 0.6 * k)
        ah = 2.2 * k
        B.fill([[tip, (tip[0] - ux * ah - uy * 0.45 * ah, tip[1] - uy * ah + ux * 0.45 * ah),
                 (tip[0] - ux * ah + uy * 0.45 * ah, tip[1] - uy * ah - ux * 0.45 * ah)]], tint(acc, 0.1), L, 31)
        taken.append((tip[0] - ah, tip[1] - ah, tip[0] + ah, tip[1] + ah))
        lines, prev = [], a
        for s_ in run:
            lines.append(u"{} {} · {:,.1f} km".format(num[s_], name[s_], math.hypot(
                pts[s_][0] - pts[prev][0], pts[s_][1] - pts[prev][1]) / 1000.0))
            prev = s_
            for nm, frm, p in HER_OFF:
                if frm == s_:
                    lines.append(u"then {} · {:,.1f} km".format(nm, math.hypot(p[0] - pts[s_][0],
                                                                                p[1] - pts[s_][1]) / 1000.0))
        labels.append((lines, tip[0], tip[1], h7, acc))
    key = place_labels(B, labels, taken, L, bounds=r)
    b_frame(B, r, k, L)
    low = b_foot(B, F, x, r[1], ss, k, L)
    if key:
        low = draw_label_key(B, key, x, low - 0.8 * k, r[2] - x, h7, L)
    B.text(u"order of the loop, not a route · stream walk K3-K4 = its spine · beyond the frame: at the arrow, "
           u"straight distances " + bcite(
               "Heritage loop: places from the survey labels and h01 §5 (P05, P07, P23, P24); gondola valley station, "
               "Trajaneum and Asklepieion from h03 Q3 (OSM / official coordinates) converted with h01 §0's formula, "
               "±10-30 m. Distances straight from the stop before, calculated."), x, low - 1.2 * k - h7, h7, INK2, L,
           font=FONT_TITLE)
    low -= 2.2 * k + h7
    leg = [("line", acc, u"Heritage loop, in its order"), ("dot", acc, u"Stop, numbered in loop order"),
           ("dot", INK, u"Heritage place")]
    crop_panel("heritage_loop", x - 0.5 * k, low - 0.5 * k, r[2] + 0.5 * k, r[3] + 0.5 * k, u"City heritage loop",
               crop_scale(ss), crop_legend(leg))
    return low - 1.0 * U


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
