# p.23 the plan: plan_page, the pl28_* functions and draw_corridor (split from parts/02_Design.py, parts/02b_detail.py, parts/02c_corridor.py, parts/02d_r28_ground.py on 29 Oct 2026; moved unchanged)
# v28 (revision 29 Oct, WO-T4b-2, package H "Page 23"): the map is the page. The analysis frame at 1:5,000 in two rows
# (upstream half on top, downstream half below; PL23_OVL m either side of the match line drawn in both), every layer
# of the corridor on both, the riverside walk as one route with the bike lane beside it (PL23_BIKE); each numbered
# move a short boxed text on the map by its place, on an arrow (R13 callouts, R14 numbered boxes); a side column
# holds the small legend, the moves with no room on the map and the areas left as they are. One strip at 1:10,000
# when two rows do not fit the crop. The perspective collage of R12 is left out (a script draws no photo collage).
PL23_SCALE = 5000.0          # the two rows
PL23_FALLBACK = 10000.0      # one strip when the two rows do not fit BK_W x BK_H
PL23_OVL = 25.0              # m either side of the match line drawn in both rows
PL23_MARK_H = 9.0            # mm: north arrow, scale bar and flow note under each row
PL23_GAP = 3.0               # mm between the first row's marks and the second row
PL23_SIDE_MIN = 80.0         # mm: the side column at least this wide
PL23_SIDE_GAP = 5.0          # mm between the map and the side column
PL23_MARKS = {5000.0: (0.0, 50.0, 100.0, 250.0), 10000.0: (0.0, 100.0, 200.0, 500.0)}   # scale bar, m (50 mm)
PL23_BOX_W = 46.0            # mm: a callout box at most this wide
PL23_NAME_TS = 3.2           # mm: place names on the 1:5,000 rows (9 pt)
PL23_RINGS = (3.0, 6.0, 10.0, 15.0, 21.0, 28.0, 36.0)   # mm: callout spots round a place, nearest first
PL23_WALK_COL, PL23_BIKE_COL = "4C2528", "5C7A86"         # palette references (library/examples/palettes)
PL23_BIKE = True             # the riverside walk carries a bike lane on its land side (Aras 29 Oct 21:04, decision card)


def draw_block(pg, lines, x0, y_top, colour, halo):
    y = y_top
    for s, sz, bd in lines:
        y -= sz * 1.0
        pg.text(s, x0, y, sz, colour, bold=bd, halo=halo)
        y -= sz * 0.18


def place_label(pg, lines, anchor, taken, W, H, colour, d0=1.2, leader=True, avoid=(), more=(), anywhere=False):
    """A label block [(text, size, bold)] on a free spot round anchor (page mm, y up), off the rings in avoid, with
    a thin leader when it sits off the anchor. v22: then round each point of more (e.g. along the route), and with
    anywhere the free spot nearest anchor on the whole panel (2 mm grid). Returns its box or None."""
    w, h = block_size(lines)
    ax, ay = anchor
    on = 0.0 <= ax <= W and 0.0 <= ay <= H              # v22: the leader goes to anchor only when it is on the panel

    def free(b):
        return not (b[0] < 0.8 or b[1] < 0.8 or b[2] > W - 0.8 or b[3] > H - 0.8 or
                    any(hit(b, t, 0.4) for t in taken) or (avoid and not box_clear(b, avoid)))

    def put(b, px, py, far):
        draw_block(pg, lines, b[0], b[3], colour, None)
        taken.append(b)
        if leader and far:
            qx, qy = min(max(px, b[0]), b[2]), min(max(py, b[1]), b[3])
            pg.line([(px, py), (qx, qy)], COL["ink2"], 0.15)
        return b

    for k_, (px, py) in enumerate([anchor] + list(more)):
        for d in (d0, d0 + 2.0, d0 + 4.0, d0 + 7.0, d0 + 11.0, d0 + 16.0, 24.0, 32.0):
            for i in range(16):
                a = math.radians(i * 22.5 + 11.25)
                cx, cy = px + math.cos(a) * (d + w / 2), py + math.sin(a) * (d + h / 2)
                b = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
                if free(b):
                    return put(b, ax, ay, d > 3.0 or k_ > 0) if on or k_ == 0 else put(b, px, py, d > 3.0)
    if anywhere:                                         # v22: last, any free spot on the panel, nearest first
        cs = [(x_ * 2.0, y_ * 2.0) for x_ in range(int(W / 2.0) + 1) for y_ in range(int(H / 2.0) + 1)]
        for cx, cy in sorted(cs, key=lambda c_: (c_[0] - ax) ** 2 + (c_[1] - ay) ** 2):
            b = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
            if free(b):
                return put(b, ax, ay, True) if on else put(b, cx, cy, False)
    return None


def draw_corridor(pg, T, k, C, inP, taken, dw, dh):
    """Every layer of the corridor on plan page pg (T: world -> page mm, k: mm per m; inP: world point on this
    plan). Returns (legend keys used, note numbers placed). v27: the plan strips only (p.24's windows = 02e).
    v26 (Prompt 7 rules 1 and 5): the layers in the order water -> buildings -> bridges -> roads -> proposal ->
    labels (the paper is the ground; the planting is proposed, so it is a proposal tint); what exists (survey) is
    crisp, what we propose is soft: fading fields, haloes, translucent bands, no outlines."""
    used, placed = set(), []
    ink, ink2 = COL["ink_dark"], COL["ink2"]
    vis = lambda TPs: [Q for Q in TPs if hit(bbox(Q), (-2.0, -2.0, dw + 2.0, dh + 2.0))]
    TL = lambda Ls: vis([[T(p) for p in L_] for L_ in Ls])
    on = lambda Q: hit(bbox(Q), (0.0, 0.0, dw, dh))
    big = k >= 0.5                                       # the 1:1,000 windows
    fine = k < 0.15                                      # v27 (MIRAQUA 28 Oct, G7): the 1:10,000 strip (p.23)
    hal = 0.8 if big else 0.6                            # halo of a proposed area, mm
    # ---- water (survey): the bed between the surveyed edges, the stream lines
    Ps = TL(C.bed_loops)
    if Ps:
        pg.poly(Ps, fill=WATER_COL)
        used.add("bed")
    for P in C.streams:
        pg.line([T(p) for p in P], COL["river_mid"], 0.15)
    # v26.1 (Prompt 8): the hidden-stream line (proposal, soft) with the water, never over the buildings or bridges
    # above it; in the legend only where it is on this plan (a 1:1,000 window)
    for P in C.covered:
        Q = [T(p) for p in P]
        pg.line(Q, COL["river_mid"], 1.6 if big else 0.8, [1.6, 0.9], cap=0, alpha=0.7)
        if on(Q):
            used.add("hidden")
    # ---- buildings (survey); built on since the survey hatched (satellite check, OPEN_CHECK)
    for role, fill in (("building", COL["bld"]), ("housing", COL["bld"]), ("shed", COL["bld"]),
                       ("heritage", COL["her"])):
        Ps = TL(C.bld.get(role, []))
        if Ps:
            pg.poly(Ps, fill=fill, stroke=COL["her_edge"] if role == "heritage" else None, lw=0.1)
            used.add("bld" if role != "heritage" else "her")
    Ps = TL(C.built_since)
    if Ps:
        pg.poly(Ps, fill=COL["bld"], stripes=(ink, 0.8, 0.15, 45.0))
        used.add("since")
    # ---- bridges (survey YOL_KOPRU); a bridge of K1-K6 with no survey line within 25 m gets a mark
    for P in C.bridges:
        Q = [T(p) for p in P]
        if on(Q):
            pg.line(Q, ink, 0.5 if big else 0.3)
            used.add("bridge")
    for nm, xy in BRIDGES_K:
        if any(min(seg_dist(xy[0], xy[1], a, b) for a, b in zip(P, P[1:])) <= 25.0 for P in C.bridges):
            continue
        x, y = T(xy)
        if 0.0 <= x <= dw and 0.0 <= y <= dh:
            pg.poly([rect(x - 0.9, y - 0.9, x + 0.9, y + 0.9)], fill=ink)
            used.add("bridge")
    # ---- roads (survey street edges)
    for P in C.roads:
        Q = [T(p) for p in P]
        if on(Q):
            pg.line(Q, ROAD_TONE[1], 0.3 if big else (0.1 if fine else 0.18))   # v27: base recessive (G6)
            used.add("street")
    # ---- proposal, soft: the planting gradient from the water, the programme rings round the hubs
    for t, Ls in reversed(C.eco):
        Ps = TL(Ls)
        if Ps:
            pg.poly(Ps, fill=ECO_COL, alpha=ECO_A)
            used.add("eco")
    for r_, Ls in reversed(C.rings):
        Ps = TL(Ls)
        if Ps:
            pg.poly(Ps, fill=HUB_COL, alpha=HUB_A)
            used.add("ring")
    # ---- proposal, soft: widened stream, side arms, reed basins, Demeter's Garden, hidden-stream line
    Ps = TL([w["ring"] for w in C.widen])
    if Ps:
        soft_fill(pg, Ps, WET_COL, 0.85, hal)
        used.add("widen")
    for a in C.arms:
        Q = [T(p) for p in a["P"]]
        if on(Q):
            soft_line(pg, Q, COL["river_mid"], max(1.0, 6.0 * k), 0.6)
            used.add("arm")
    for z in C.D.zones:
        Q = [T(p) for p in z["P"]] if z["code"] in ("WT", "DG") else None
        if not Q or not on(Q):
            continue
        if z["code"] == "WT":
            soft_fill(pg, [Q], WET_COL, 0.8, hal)
            pg.poly([Q], stripes=(COL["river_dark"], 1.6 if big else 0.9, 0.15, 90.0), alpha=0.35)
            used.add("reed")
        else:
            soft_fill(pg, [Q], MP["agriculture"][2], 0.16, hal)
            used.add("dg")
    # ---- proposal, soft: terraces on the contours (upstream): edge + ticks toward the stream
    for P in C.terr:
        Q = [T(p) for p in P]
        if not on(Q):
            continue
        mid = P[len(P) // 2]
        c_, _ = chain_at(C.ref, mid)
        q, _ = at_len(C.ref, arclen(C.ref), c_)
        s = arclen(Q)
        (x, y), (ux, uy) = at_len(Q, s, s[-1] / 2.0)
        qx, qy = T(q)
        side = 1.0 if (-uy) * (qx - x) + ux * (qy - y) > 0 else -1.0
        ticks_line(pg, Q, MP["storage"][2], 0.45 if big else 0.3, 3.0 if big else 1.6, 1.2 if big else 0.6, side,
                   alpha=0.7)
        used.add("terrace")
    # ---- proposal, soft: forest corridor, tree-planted area
    for pts, a_, key in ((C.forest, 0.6, "forest"), (C.trees, 0.4, "trees")):
        r_ = 0.28 if fine else max(0.45, 2.8 * k)       # v27: 9 m apart = 0.9 mm at 1:10,000, dots stay apart
        for p in pts:
            x, y = T(p)
            if -1.0 <= x <= dw + 1.0 and -1.0 <= y <= dh + 1.0:
                pg.circle(x, y, r_, fill=COL["tree_mid"] if key == "forest" else COL["tree"], alpha=a_)
                used.add(key)
    # ---- proposal, soft: hub squares, plane trees, canopied walkway
    for h in C.hubs:
        Ps = TL(h.get("square") or [])
        if Ps:
            soft_fill(pg, Ps, SQ_EDGE, 0.22, hal)
            used.add("square")
            for p in h.get("trees", []):
                x, y = T(p)
                pg.circle(x, y, 0.4 if fine else max(0.7, 4.0 * k), fill="5E7A3A", alpha=0.6)
    for P in C.canopy:
        Q = [T(p) for p in P]
        if on(Q):
            ticks_line(pg, Q, MP["centre"][2], 0.6 if big else 0.45, 2.4 if big else 1.2, 1.0 if big else 0.5, 1.0,
                       alpha=0.6)
            used.add("canopy")
    # ---- v28 (WO-T4b-2): the riverside walk as one route (river_walks runs: bank walk and street footway solid, the
    # walk on a terrace in the bed dashed: it closes in floods), the bike lane beside it on its land side (PL23_BIKE)
    for x in (C.CL.get("W") or {}).get("runs") or []:
        Q = [T(p) for p in x.get("P") or []]
        if len(Q) < 2 or not on(Q):
            continue
        bed = x.get("cls") == "bed"
        pg.line(Q, PL23_WALK_COL, 0.8 if big else 0.5, [1.6, 0.6] if bed else None, cap=0 if bed else 1, alpha=0.85)
        used.add("walk_bed" if bed else "walk")
        if PL23_BIKE and not bed:
            ticks_line(pg, pl23_offset(Q, (1.2 if big else 0.75) * (1.0 if x.get("bank") == "NE" else -1.0)),
                       PL23_BIKE_COL, 0.25, 2.4, 0.5, 1.0 if x.get("bank") == "NE" else -1.0, alpha=0.9)
            used.add("bike")
    # ---- proposal, soft: roads changed (OSM) and the later town line
    for rd in ROADS + [TOWN_LINE]:
        Q = [T(p) for p in rd["xy"]]
        if not on(Q):
            continue
        ch = rd["change"] if rd["change"] in ROAD_CHANGE_COL else "later"
        if ch == "later":
            pg.line(Q, ROAD_CHANGE_COL["later"], 0.9 if big else 0.6, [2.0, 1.0], cap=0, alpha=0.6)
        else:
            soft_line(pg, Q, ROAD_CHANGE_COL[ch], 3.0 if big else (1.2 if fine else 1.6), 0.75)
        used.add("road_" + ch)
    # ---- proposal, soft: new crossings (footbridges, stepping stones)
    for c_ in C.cross:
        if c_["kind"] == "footbridge":
            soft_line(pg, [T(c_["P"][0]), T(c_["P"][1])], ink, 1.4 if big else 0.8, 0.8)
            used.add("foot")
        elif c_["kind"] == "stepping stones":
            A_, B_ = T(c_["P"][0]), T(c_["P"][1])
            for i in range(5):
                f = (i + 0.5) / 5.0
                pg.circle(A_[0] + (B_[0] - A_[0]) * f, A_[1] + (B_[1] - A_[1]) * f, 0.9 if big else 0.35,
                          fill=ink2, alpha=0.7)
            used.add("stones")
    s_ic = 3.0 if big else (1.8 if fine else 2.2)
    for p in C.seats:
        x, y = T(p)
        if 0.0 <= x <= dw and 0.0 <= y <= dh:
            icon(pg, "seat", x, y, s_ic * 0.8)
            used.add("seat")
    if C.terrace:                                         # the sightline toward the Trajaneum (off the plan)
        x, y = T(C.terrace["xy"])
        p2 = (C.terrace["xy"][0] + C.terrace["dir"][0] * 400.0, C.terrace["xy"][1] + C.terrace["dir"][1] * 400.0)
        x2, y2 = T(p2)
        pg.line([(x, y), (x2, y2)], COL["accent"], 0.35, [1.4, 0.8], cap=0, alpha=0.7)
        used.add("sight")
    # ---- pictograms: hubs, sub-hubs, cafes, education, viewing terrace, H4 step, H6 deck, gateway
    ic = []
    for h in C.hubs:
        ic.append(("transit" if h["role"] == "transit" else ("gate" if h["id"] == u"K6" else "walkhub"), h["xy"]))
        if h.get("sub_xy"):
            ic.append(("sub", h["sub_xy"]["c"]))
    for z in C.D.zones:
        if z["code"] in ("GR", "DG"):
            ic.append(("cafe", z["q"]))
        if z["code"] == "WT":
            ic.append(("edu", z["q"]))
        if z["code"] == "WS" or (z["code"] == "WA" and z["tier"] == "F"):
            ic.append(("seat", z["q"]))
    ic += [("edu", CRAFT_XY), ("deck", ROMAN_WALL), ("view", C.terrace["xy"]) if C.terrace else None]
    for it in [i_ for i_ in ic if i_]:
        x, y = T(it[1])
        if 0.0 <= x <= dw and 0.0 <= y <= dh:
            icon(pg, it[0], x, y, s_ic * (1.25 if it[0] in ("transit", "walkhub", "gate") else 1.0))
            taken.append((x - s_ic * 0.6, y - s_ic * 0.6, x + s_ic * 0.6, y + s_ic * 0.6))
            used.add(it[0])
    # ---- words: place names (large; v27: 7.5 pt on the 1:10,000 strip), (v27: the detail labels moved to 02e)
    names = [(HUB_NAME[h["id"]], h["xy"]) for h in C.hubs] + \
        [(nm, xy) for nm, xy in BRIDGES_K if nm in (u"K1", u"K2")] + PLACES
    for nm, xy in names:
        if inP(xy):
            place_label(pg, [(nm, PL28_TS if fine else (PL23_NAME_TS if k < 0.5 else PLACE_TS * 1.15), True)], T(xy),
                        taken, dw, dh, ink, d0=1.5, anywhere=False)   # v27: 7.5 pt on the 1:10,000 strip (G4); v28: 9 pt at 1:5,000
    if C.terrace and inP(C.terrace["xy"]):
        x, y = T(C.terrace["xy"])
        p2 = (C.terrace["xy"][0] + C.terrace["dir"][0] * 120.0, C.terrace["xy"][1] + C.terrace["dir"][1] * 120.0)
        x2, y2 = T(p2)
        place_label(pg, [(u"TRAJAN TAPINAĞI {:,.0f} m".format(C.terrace["d"]), LAB_TS, True)],   # v28: Turkish (G6)
                    (min(max(x2, 1.0), dw - 1.0), min(max(y2, 1.0), dh - 1.0)), taken, dw, dh, COL["accent"], d0=1.0)
    return used, placed                                  # v27: the detail windows' labels went (p.24 = 02e)


# ---------------------------------------------------------------- G10: one frame figure
def pl28_frame_stats(C):
    """v27 (MIRAQUA 28 Oct, G10): C.frame_m2 = the frame polygon's area (shoelace: 150.52 ha for site_alan, the figure
    the site board prints on p.02); C.inF = 1 for each grid cell whose centre lies inside the frame (the grid
    overshoots it by up to one cell on each axis, which made 151 ha); each such cell stands for frame area / cells
    inside (C.cell_m2, within 0.3 % of c x c), so C.stats {0 open, 1 building, 2 road, 3 bed: m2} adds up to the
    frame exactly. One pass over the grid (was four)."""
    G, V, F = C.G, C.V, C.F
    P = list(getattr(V, "frame_P", None) or V.P)          # build_all sets V.frame_P = site_alan
    inF = bytearray(C.N)
    for n in G.poly_cells([V.uv(p) for p in P]):
        inF[n] = 1
    C.frame_m2 = abs(area2(P))
    C.inF = inF
    C.cell_m2 = C.frame_m2 / float(inF.count(1) or 1)
    Fin = bytes(v if i else 9 for v, i in zip(F, inF))
    C.stats = dict((k_, Fin.count(k_) * C.cell_m2) for k_ in (0, 1, 2, 3))


# ---------------------------------------------------------------- G7 / G8: the strip and the study area
def pl28_strip(C, k):
    """v27 (G7): the whole analysis frame as ONE strip, the water left to right (View: the upstream end at u0): T
    (world -> strip mm, y up), inP (world point on the strip), its size dw x dh mm."""
    V = C.V

    def T(p):
        u, v = V.uv(p)
        return (u - V.u0) * k, (v - V.v0) * k

    def inP(p):
        u, v = V.uv(p)
        return V.u0 <= u <= V.u1 and V.v0 <= v <= V.v1
    return {"T": T, "inP": inP, "dw": (V.u1 - V.u0) * k, "dh": (V.v1 - V.v0) * k}


def pl28_study(C):
    """G8: the study area's outlines (calisma_alan, both parts; build_all sets V.study), survey m."""
    return [list(P) for P in (getattr(C.V, "study", None) or []) if len(P) >= 3]


def pl28_draw_study(pg, C, T):
    """G8: the study area outline in R28_STUDY_LINE (dash-dot) on a plan page; True when drawn."""
    st = R28_STUDY_LINE
    rs = pl28_study(C)
    for P in rs:
        Q = [T(p) for p in P]
        pg.line(Q + Q[:1], st["colour"], st["width_mm"], list(st["dash_mm"]), cap=0)
    return bool(rs)


def pl28_sw_study():
    """G8: the study area's legend sample."""
    return _sw_line(R28_STUDY_LINE["colour"], R28_STUDY_LINE["width_mm"], list(R28_STUDY_LINE["dash_mm"]))


def pl28_runs(sh, x, y, runs, size, colour):
    """One line of text in runs [(text, bold)] (G5: the bold keyword inside a line); returns its end x."""
    for t, bd in runs:
        if t:
            sh.text(t, x, y, size, colour, bold=bd)
            x += text_w(t, size, bd)
    return x


def pl28_marks(sh, C, x0, y0):
    """v27: the row under a strip, from (x0, y0) up (10 mm): the north arrow (survey +Y turned with the plan), the
    1:10,000 scale bar right beside it (SCRIPT_STANDARD §8: next to every orthogonal drawing) and which way the water
    flows."""
    V = C.V
    nu, nv = V.uv((V.cx, V.cy + 1.0))
    L = math.hypot(nu, nv) or 1.0
    nx_, ny_ = nu / L, nv / L
    ax, ay = x0 + 3.5, y0 + 5.0
    tip = (ax + nx_ * 3.5, ay + ny_ * 3.5)
    sh.poly([[tip, (ax - ny_ * 1.6 - nx_ * 3.0, ay + nx_ * 1.6 - ny_ * 3.0), (ax - nx_ * 1.8, ay - ny_ * 1.8)]],
            fill=COL["ink_dark"])
    sh.poly([[tip, (ax - nx_ * 1.8, ay - ny_ * 1.8), (ax + ny_ * 1.6 - nx_ * 3.0, ay - nx_ * 1.6 - ny_ * 3.0)]],
            fill=COL["white"], stroke=COL["ink_dark"], lw=0.15)
    sh.text(u"N", tip[0] + 1.2, tip[1] - 0.6, 2.6, COL["ink_dark"], bold=True)
    scale_bar(sh, x0 + 12.0, y0 + 2.0, MP_SCALE, PL28_MARKS)
    xs = x0 + 12.0 + PL28_MARKS[-1] * 1000.0 / MP_SCALE + 6.0 + text_w(u"1:{:,.0f}".format(MP_SCALE), 3.4, True) + 8.0
    pl28_runs(sh, xs, y0 + 2.0, [(u"the water flows ", False), (u"left to right", True),
                                 (u", the upstream entry at the left end", False)], PL28_TS, COL["ink2"])


def pl28_legend(sh, groups, x0, x1, y_top, y_min, ncols, warn, pitch=3.6):
    """v27: the legend in ncols columns from x0 to x1, top down from y_top to y_min: each group a bold head, then its
    drawn samples with plain names (only what the page draws); a head never ends a column; rows closer (to 3.0 mm)
    when they would not fit."""
    rows = []
    for head, items in groups:
        if items:
            rows += [(head, None)] + list(items)
    if not rows:
        return
    need = int(math.ceil(len(rows) / float(ncols))) + 1
    pitch = max(3.0, min(pitch, (y_top - y_min) / float(need)))
    R = max(2, int((y_top - y_min) / pitch))
    cols, cur = [], []
    for r_ in rows:
        if cur and (len(cur) >= R or (r_[1] is None and len(cur) >= R - 1)):
            cols.append(cur)
            cur = []
        cur.append(r_)
    cols.append(cur)
    if len(cols) > ncols:
        warn.append(u"legend: {} rows do not fit {} columns beside the strip".format(len(rows), ncols))
    cw = (x1 - x0) / float(ncols)
    for c, col in enumerate(cols):
        cx = x0 + c * cw
        for j, (nm, f) in enumerate(col):
            cy = y_top - j * pitch
            if f is None:
                sh.text(nm, cx, cy - 2.6, PL28_TS, COL["ink_dark"], bold=True)
                continue
            f(sh, cx, cy - 2.9, 6.0, 2.4)
            sh.text(nm, cx + 7.5, cy - 2.6, PL28_TS, COL["ink"])
            if text_w(nm, PL28_TS) > cw - 8.5:
                warn.append(u"legend name runs into the next column: {}".format(nm))


# ---------------------------------------------------------------- P23: markers, list, sources
def pl28_note_group(nt):
    """P23.1: the R28_MARKERS group of a numbered note: roads; hubs and transit (the later town bus line too); water
    and ecology (reed basins, terraces, hidden stream, widened stream, side arm, the edges kept); crossings
    (footbridges); heritage and views."""
    k = nt["key"]
    if k[0] == "road":
        return "hubs" if k[1] == TOWN_LINE["name"] else "roads"
    return {"hub": "hubs", "foot": "crossings", "h4": "heritage", "h6": "heritage", "view": "heritage"}.get(k[0], "water")


def pl28_note_entry(C, nt):
    """P23.2: (name, one short line) of a numbered note for the list, in plain words from the note's own data. No
    source codes: they go to the sources page with every reason, whole (pl28_plan_sources)."""
    k = nt["key"]
    less = u"less than {:.0f} m open".format(KEPT_MAX)
    if k[0] == "hub":
        h = next((h_ for h_ in C.hubs if h_["id"] == k[1]), {})
        nm = PL28_HUB.get(k[1], k[1])
        if h.get("role") == "transit":
            return nm + u" · transit hub", u"town bus lines stop here · " + (
                u"square over the culvert" if k[1] == u"İstiklal" else u"by the Red Hall tunnels")
        if k[1] == u"K6":
            return nm + u" · gateway out", u"the primary road is kept · bus stop {} {:.0f} m".format(
                h.get("stop", u""), h.get("stop_m", 0.0))
        extra = {u"K3": u" · workshops, education", u"K5": u" · Demeter's Garden"}.get(k[1], u"")
        sub = u", sub-hub in the bed" if h.get("sub_xy") else u""
        return nm + u" · walking hub", (u"dry square" if extra else u"dry square at the Roman bridge") + sub + extra
    if k[0] == "road":
        if k[1] == TOWN_LINE["name"]:
            return u"Town bus line to K4 · later step", u"on the existing streets from İstiklal to the K4 stop"
        rd = next((r_ for r_ in ROADS if r_["name"] == k[1]), None)
        if rd is not None:
            ch, _, rest = rd["note"].partition(u": ")
            return u"{}{} · {}".format(rd["name"][:1].upper(), rd["name"][1:], ch), rest
    if k[0] == "kept":
        return {"building": (u"Edge kept · buildings", u"buildings stand at the bank, " + less),
                "road": (u"Edge kept · road", u"a road runs at the bank, " + less),
                "frame": (u"Nothing placed", u"the edge of the analysis frame, " + less)}.get(
            k[1], (nt["text"][:1] + nt["text"][1:].lower(), less))
    if k[0] == "view" and C.terrace:
        return u"Viewing terrace", u"a clear sightline to Trajan Tapınağı, {:,.0f} m away".format(C.terrace["d"])
    if k[0] == "widen" and C.widen:
        lo, hi = min(w["fw"][0] for w in C.widen), max(w["fw"][1] for w in C.widen)
        return u"Stream widened", u"room for water and a wetland · {:.0f}-{:.0f} m open beside the bank".format(lo, hi)
    if k[0] == "foot":
        return u"Footbridge" + (u"s" if len(nt["at"]) > 1 else u""), \
            u"{:.0f}+ m of stream without a crossing · both landings open".format(FOOT_GAP_M)
    fixed = {"h4": (u"Step to the water", u"facing Tabaklar Hamamı, a bath ruin 1.5 m from the stream"),
             "h6": (u"Deck over the Roman bank wall", u"a Roman complex with a bank wall of about 120 m"),
             "wt": (u"Reed basins", u"the water is cleaned once · clean-water classroom"),
             "terr": (u"Rain terraces on the contours", u"they hold the rain · overflow to the reed basins"),
             "cov": (u"Hidden stream", u"nothing opened: the water line drawn in the paving"),
             "arm": (u"Side arm", u"a planted channel cleans the return water")}   # v28 (D2 a): reed only in lined basins
    return fixed.get(k[0], (nt["text"][:1] + nt["text"][1:].lower(), u""))


def pl28_letter(i):
    return u"abcdefghijklmnopqrstuvwxyz"[i] if i < 26 else str(i + 1)


def pl28_list_head(sh, lab, col, x, y, cw):
    """a group's head in the list: its name in its colour, bold, over a hairline; returns the y under it"""
    y -= PL28_HEAD_TS * 1.18
    sh.text(lab, x, y + PL28_HEAD_TS * 0.2, PL28_HEAD_TS, col, bold=True)
    y -= 1.3
    sh.line([(x, y), (x + cw, y)], col, 0.2, alpha=0.5)
    return y - 2.6


def pl28_list_nogo(sh, nis, x, y, cw):
    """the areas left as they are: grey letter, its size in ha (G13) in bold, why (its source tag goes to the
    sources page); returns the y under it"""
    y = pl28_list_head(sh, u"Left as it is · no intervention", COL["ink2"], x, y, cw)
    rn, tx = PL28_NI_R, x + 2 * BADGE_R + 2.2
    for lt, r_, ok in nis:
        sh.circle(x + BADGE_R, y - rn, rn, fill=COL["white"], stroke=COL["ink2"], lw=0.2)
        sh.text(lt, x + BADGE_R, y - rn - KEY_MIN * 0.36, KEY_MIN, COL["ink2"], bold=True, align="C")
        ha = u_area(r_["ha"] * 1e4, "ha")
        yy = y - PL28_TS * 1.18
        x1 = pl28_runs(sh, tx, yy + PL28_TS * 0.2, [(ha, True), (u" · ", False)], PL28_TS, COL["ink"])
        for i, s_ in enumerate(wrap(PL28_SRC_TAG.sub(u"", r_["why"]), PL28_TS, max(20.0, x + cw - x1))):
            if i:
                yy -= PL28_TS * 1.18
            sh.text(s_, x1, yy + PL28_TS * 0.2, PL28_TS, COL["ink2"])
        y = min(yy, y - 2 * rn) - 1.6
    return y


def pl28_src_kind(s):
    """N2 / F5 hint for the booklet's sources page: "public online" (OSM, its bus stops, ESA WorldCover, DSI, EPA),
    "project note" (history cards h01-h03, decisions D/H, register codes P/E), else "booklet analysis" (survey, open
    ground, edge plan, water board cuts, city link)."""
    if re.search(u"\\bOSM\\b|WorldCover|satellite 2021|\\bDSI\\b|\\bEPA\\b|bus stop", s):
        return u"public online"
    if re.search(u"\\b(h0\\d|H\\d|D\\d{1,2}|P\\d{2}|E\\d{2})\\b", s):
        return u"project note"
    return u"booklet analysis"


def pl28_plan_sources(ents, nis):
    """P23.2 / N2: what the page does not print, for the booklet's sources page, keyed by the marker numbers (and
    letters) on the masterplan page. v28 (revision 29 Oct, WO-T4b-2, D13): only the public sources (pl28_src_kind
    "public online"); a move or area with none keeps an empty list."""
    pub = lambda s_: pl28_src_kind(s_) == u"public online"
    return {"crop": "mp_plan", "heading": u"Masterplan: what each numbered move stands on",
            "markers": [{"n": nt["n"], "group": grp, "name": nm, "line": line,
                         "sources": [{"text": s_, "kind": u"public online"} for s_ in nt["why"] if pub(s_)]}
                        for nt, grp, nm, line, ok in ents],
            "left_as_is": [{"id": lt, "ha": round(r_["ha"], 2), "why": PL28_SRC_TAG.sub(u"", r_["why"]),
                            "sources": [n_ for n_ in (PL28_SRC_NAME.get(m_, m_)
                                                      for m_ in PL28_SRC_TAG.findall(r_["why"])) if pub(n_)]}
                           for lt, r_, ok in nis]}


# ---------------------------------------------------------------- v28 (WO-T4b-2): rows, route, callouts, side column
def pl23_offset(Q, d):
    """the polyline Q (page mm) moved d mm to its left (negative: to its right), each vertex along the normal of its
    neighbours' chord"""
    out, n = [], len(Q)
    for i in range(n):
        a, b = Q[max(0, i - 1)], Q[min(n - 1, i + 1)]
        ux, uy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(ux, uy) or 1.0
        out.append((Q[i][0] - uy / L * d, Q[i][1] + ux / L * d))
    return out


def pl23_rows(C, warn):
    """(scale, rows): two rows at PL23_SCALE when they fit the crop beside a PL23_SIDE_MIN side column, else one strip
    at PL23_FALLBACK. A row = {a, b: m from the frame's upstream end drawn; ea, eb: its own part (names, markers)}."""
    V = C.V
    L, Hm = V.u1 - V.u0, V.v1 - V.v0
    k = 1000.0 / PL23_SCALE
    w2, h2 = (L / 2.0 + PL23_OVL) * k, Hm * k
    if w2 <= BK_W - PL23_SIDE_MIN - PL23_SIDE_GAP and 2.0 * (h2 + PL23_MARK_H) + PL23_GAP <= BK_H:
        m = L / 2.0
        return PL23_SCALE, [dict(a=0.0, b=m + PL23_OVL, ea=0.0, eb=m), dict(a=m - PL23_OVL, b=L, ea=m, eb=L)]
    warn.append(u"masterplan page: two rows at 1:{:,.0f} ({:.0f} x {:.0f} mm each) do not fit the page: one strip at "
                u"1:{:,.0f}".format(PL23_SCALE, w2, h2, PL23_FALLBACK))
    return PL23_FALLBACK, [dict(a=0.0, b=L, ea=0.0, eb=L)]


def pl23_row_T(C, row, k, x0=0.0, y0=0.0):
    """(T, mine) of a row: T world -> page mm with the row's upstream end at x0 and the frame's foot at y0; mine(p) =
    the point lies in the row's own part of the frame"""
    V = C.V

    def T(p):
        u, v = V.uv(p)
        return (u - V.u0 - row["a"]) * k + x0, (v - V.v0) * k + y0

    def mine(p):
        u, v = V.uv(p)
        return V.u0 + row["ea"] <= u <= V.u0 + row["eb"] and V.v0 <= v <= V.v1
    return T, mine


def pl23_marks(sh, C, x0, y0, scale, runs):
    """the row under a map row, from (x0, y0) up: north arrow (survey +Y turned with the plan), the scale bar right
    beside it (SCRIPT_STANDARD §8) and a short note in runs [(text, bold)]"""
    V = C.V
    nu, nv = V.uv((V.cx, V.cy + 1.0))
    L = math.hypot(nu, nv) or 1.0
    nx_, ny_ = nu / L, nv / L
    ax, ay = x0 + 3.5, y0 + 5.0
    tip = (ax + nx_ * 3.5, ay + ny_ * 3.5)
    sh.poly([[tip, (ax - ny_ * 1.6 - nx_ * 3.0, ay + nx_ * 1.6 - ny_ * 3.0), (ax - nx_ * 1.8, ay - ny_ * 1.8)]],
            fill=COL["ink_dark"])
    sh.poly([[tip, (ax - nx_ * 1.8, ay - ny_ * 1.8), (ax + ny_ * 1.6 - nx_ * 3.0, ay - nx_ * 1.6 - ny_ * 3.0)]],
            fill=COL["white"], stroke=COL["ink_dark"], lw=0.15)
    sh.text(u"N", tip[0] + 1.2, tip[1] - 0.6, 2.6, COL["ink_dark"], bold=True)
    mk = PL23_MARKS.get(scale, PL28_MARKS)
    scale_bar(sh, x0 + 12.0, y0 + 2.0, scale, mk)
    xs = x0 + 12.0 + mk[-1] * 1000.0 / scale + 6.0 + text_w(u"1:{:,.0f}".format(scale), 3.4, True) + 8.0
    pl28_runs(sh, xs, y0 + 2.0, runs, PL28_TS, COL["ink2"])


def pl23_busy(C, T, half=1.4):
    """boxes (sheet mm) the callouts keep off: the stream bed edges and the proposals' lines (walk, canopy, side arms,
    roads changed, hidden stream, crossings) along their length; the small proposal areas (widened stream, reed
    basins, Demeter's Garden, hub squares) whole"""
    out = []
    lines = list(C.bed_loops) + list(C.covered) + list(C.canopy) + [a["P"] for a in C.arms] + \
        [x.get("P") or [] for x in (C.CL.get("W") or {}).get("runs") or []] + [rd["xy"] for rd in ROADS] + \
        [c_["P"] for c_ in C.cross]
    for P in lines:
        if len(P) >= 2:
            out += boxes_along([T(p) for p in P], half)
    rings = [w["ring"] for w in C.widen] + [z["P"] for z in C.D.zones if z["code"] in ("WT", "DG")] + \
        [L_ for h in C.hubs for L_ in (h.get("square") or [])]
    for R in rings:
        if len(R) >= 3:
            out.append(bbox([T(p) for p in R]))
    return out


def pl23_spot(x, y, w, h, taken, boxes, bounds, rings=PL23_RINGS):
    """a free w x h box round (x, y) inside bounds, off the taken boxes (only those within reach are tested), its
    arrow from the place never through a placed callout (boxes); the box or None"""
    R = rings[-1] + w + h
    near = [t for t in taken if t[2] > x - R and t[0] < x + R and t[3] > y - R and t[1] < y + R]
    for d in rings:
        for i in range(16):
            a = math.radians(i * 22.5 + 11.25)
            cx, cy = x + math.cos(a) * (d + w / 2.0), y + math.sin(a) * (d + h / 2.0)
            b = (cx - w / 2.0, cy - h / 2.0, cx + w / 2.0, cy + h / 2.0)
            if b[0] < bounds[0] or b[1] < bounds[1] or b[2] > bounds[2] or b[3] > bounds[3]:
                continue
            if any(lp_hit(b, t, 0.5) for t in near):
                continue
            e = lp_leader_end(b, (x, y))
            if any(_lp_seg_box((x, y), e, t) for t in boxes):
                continue
            return b
    return None


def pl23_box_lines(nm, line, w_max):
    """a callout's rows [(text, size, bold)] wrapped beside its number badge (name 7.5 pt bold, line 7 pt) and its
    box size (w, h), mm"""
    tw = w_max - 2 * BADGE_R - 2.4
    rows = [(s_, PL28_TS, True) for s_ in wrap(nm, PL28_TS, tw, True)] + \
        [(s_, KEY_MIN, False) for s_ in (wrap(line, KEY_MIN, tw) if line else [])]
    w = min(w_max, max(text_w(s_, sz, bd) for s_, sz, bd in rows) + 2 * BADGE_R + 2.4)
    h = max(2 * BADGE_R + 1.2, sum(sz * 1.18 for s_, sz, bd in rows) + 1.2)
    return rows, w, h


def pl23_badge(sh, cx, cy, n, col):
    sh.circle(cx, cy, BADGE_R + 0.25, fill=COL["white"])
    sh.circle(cx, cy, BADGE_R, fill=col)
    sh.text(str(n), cx, cy - BADGE_TS * 0.36, BADGE_TS, COL["white"], bold=True, align="C")


def pl23_box(sh, b, n, rows, col):
    """a callout: white box with a hairline in the move's group colour, the number badge top-left, the rows beside it"""
    sh.poly([rect(b[0], b[1], b[2], b[3])], fill=COL["white"], stroke=col, lw=0.25, alpha=0.94)
    pl23_badge(sh, b[0] + 0.6 + BADGE_R, b[3] - 0.6 - BADGE_R, n, col)
    x, y = b[0] + 2 * BADGE_R + 1.8, b[3] - 0.6
    for s_, sz, bd in rows:
        y -= sz
        sh.text(s_, x, y, sz, COL["ink"] if bd else COL["ink2"], bold=bd)
        y -= sz * 0.18


def pl23_arrow(sh, p, q, col):
    """an arrow from the box edge q to the place p, its small head at the place"""
    d = math.hypot(p[0] - q[0], p[1] - q[1])
    if d < 0.8:
        return
    ux, uy = (p[0] - q[0]) / d, (p[1] - q[1]) / d
    hl = min(1.3, d * 0.5)
    bx, by = p[0] - ux * hl, p[1] - uy * hl
    sh.line([q, (bx, by)], col, 0.2)
    sh.poly([[p, (bx - uy * hl * 0.4, by + ux * hl * 0.4), (bx + uy * hl * 0.4, by - ux * hl * 0.4)]], fill=col)


def pl23_callouts(sh, C, rws, taken):
    """P23.1 (R13, R14): every numbered move as a short boxed text on the map by its first place, on an arrow; its
    further places get the number badge alone. rws = [(T, mine, bounds)] per row (sheet mm). Returns (ents, nis):
    [[note, group, name, line, on the map]], [[letter, region, placed]]; moves with no room on the map are listed
    in the side column (pl23_side)."""
    mk = dict((k_, hx) for k_, lab, hx in R28_MARKERS)
    boxes, ents, nis = [], [], []
    for nt in sorted(C.notes, key=lambda nt_: nt_["n"]):
        grp = pl28_note_group(nt)
        nm, line = pl28_note_entry(C, nt)
        ent = [nt, grp, nm, line, False]
        ents.append(ent)
        col = mk[grp]
        rows, w, h = pl23_box_lines(nm, line, PL23_BOX_W)
        first = True
        for p in nt["at"]:
            rw = next((r_ for r_ in rws if r_[1](p)), None)
            if rw is None:
                continue
            T, _, bounds = rw
            x, y = T(p)
            if first:
                first = False
                b = pl23_spot(x, y, w, h, taken, boxes, bounds)
                if b is not None:
                    taken.append(b)
                    boxes.append(b)
                    pl23_box(sh, b, nt["n"], rows, col)
                    pl23_arrow(sh, (x, y), lp_leader_end(b, (x, y)), col)
                    ent[4] = True
                    continue
            s = 2 * BADGE_R + 0.5                         # a further place (or no room for the box): the badge
            b = (x - s / 2, y - s / 2, x + s / 2, y + s / 2)
            if any(lp_hit(b, t, 0.3) for t in taken if t[2] > x - 6 and t[0] < x + 6 and t[3] > y - 6 and t[1] < y + 6):
                b = pl23_spot(x, y, s, s, taken, boxes, bounds, rings=(1.0, 2.5, 5.0, 8.0))
                if b is None:
                    continue
            cx, cy = (b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0
            if math.hypot(cx - x, cy - y) > BADGE_R + 0.4:
                pl23_arrow(sh, (x, y), lp_leader_end(b, (x, y)), col)
            taken.append(b)
            pl23_badge(sh, cx, cy, nt["n"], col)
    rn = PL28_NI_R
    for i, r_ in enumerate(C.nogo):                       # the areas left as they are: a grey letter by their spot
        nis.append([pl28_letter(i), r_, False])
        for p in r_["at"]:
            rw = next((x_ for x_ in rws if x_[1](p)), None)
            if rw is None:
                continue
            T, _, bounds = rw
            x, y = T(p)
            b = pl23_spot(x, y, 2 * rn, 2 * rn, taken, boxes, bounds, rings=(0.0, 1.5, 3.5, 6.0, 9.0))
            if b is None:
                continue
            taken.append(b)
            cx, cy = (b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0
            if math.hypot(cx - x, cy - y) > rn + 0.4:
                sh.line([(x, y), lp_leader_end(b, (x, y))], COL["ink2"], 0.15)
            sh.circle(cx, cy, rn, fill=COL["white"], stroke=COL["ink2"], lw=0.2)
            sh.text(nis[-1][0], cx, cy - KEY_MIN * 0.36, KEY_MIN, COL["ink2"], bold=True, align="C")
            nis[-1][2] = True
            r_["placed"] = r_.get("placed", 0) + 1
            break
    return ents, nis


def pl23_hub_gaps(sh, C, rws, taken):
    """R14: along the walk, the distance between neighbouring bridge hubs (K4, K3, K5, K6) on the stream line, small
    and grey by the middle of the stretch; dropped where there is no room"""
    hs = [h for h in C.hubs if h["id"] in (u"K4", u"K3", u"K5", u"K6")]
    ch = sorted((chain_at(C.ref, h["xy"])[0], h["id"]) for h in hs)
    s = arclen(C.ref)
    for (c0, a), (c1, b) in zip(ch, ch[1:]):
        p = at_len(C.ref, s, (c0 + c1) / 2.0)[0]
        rw = next((r_ for r_ in rws if r_[1](p)), None)
        if rw is None:
            continue
        T, _, bounds = rw
        x, y = T(p)
        t_ = u"{} to {}: {:,.0f} m along the stream".format(a, b, c1 - c0)
        w, h = text_w(t_, KEY_MIN), KEY_MIN * 1.18
        bx = pl23_spot(x, y, w, h, taken, (), bounds, rings=(2.0, 4.0, 7.0))
        if bx is None:
            continue
        taken.append(bx)
        sh.text(t_, bx[0], bx[1] + KEY_MIN * 0.25, KEY_MIN, PL23_WALK_COL, halo=COL["white"])


def pl23_nogo_h(nis, cw):
    """the height pl28_list_nogo takes for these areas in a column cw mm wide, mm"""
    if not nis:
        return 0.0
    h = PL28_HEAD_TS * 1.18 + 1.3 + 2.6
    rn, tx = PL28_NI_R, 2 * BADGE_R + 2.2
    for lt, r_, ok in nis:
        x1 = tx + text_w(u_area(r_["ha"] * 1e4, "ha"), PL28_TS, True) + text_w(u" · ", PL28_TS)
        n = max(1, len(wrap(PL28_SRC_TAG.sub(u"", r_["why"]), PL28_TS, max(20.0, cw - x1))))
        h += max(n * PL28_TS * 1.18, 2 * rn) + 1.6
    return h


def pl23_side(sh, x0, x1, H, used, ents, nis, warn):
    """the side column from x0 to x1: on top the small legend (two columns, only what the page draws), under it the
    moves that found no room on the map (number, name, line), at its foot the areas left as they are"""
    cw = x1 - x0
    more = [e for e in ents if not e[4]]
    mk = dict((k_, hx) for k_, lab, hx in R28_MARKERS)
    lines_more = [(e,) + pl23_box_lines(e[2], e[3], cw)[:1] for e in more]
    h_more = (PL28_HEAD_TS * 1.18 + 3.9 + sum(sum(sz * 1.18 for s_, sz, bd in rows) + 1.8
                                                for e, rows in lines_more)) if more else 0.0
    h_nogo = pl23_nogo_h(nis, cw)
    leg_ = PL23_LEGEND + [(k_, nm, f) for k_, nm, f in LEGEND_V24 if k_ not in PL23_LEG_KEYS]
    groups = [(u"EXISTING · SURVEY", [(nm, f) for key, nm, f in leg_ if key in used and key in EXISTING]),
              (u"PROPOSED", [(nm, f) for key, nm, f in leg_ if key in used and key not in EXISTING])]
    n = sum(len(it) + 1 for _, it in groups if it)
    rows = int(math.ceil(n / 2.0)) + 1
    room = H - h_nogo - h_more - 4.0
    pitch = max(3.0, min(3.6, room / float(rows)))
    y_leg = H - rows * pitch
    pl28_legend(sh, groups, x0, x1, H, y_leg, 2, warn, pitch=pitch)
    y = y_leg - 2.0
    if more:
        y = pl28_list_head(sh, u"More moves", COL["ink2"], x0, y, cw)
        tx = x0 + 2 * BADGE_R + 2.2
        for e, rows_ in lines_more:
            pl23_badge(sh, x0 + BADGE_R, y - BADGE_R, e[0]["n"], mk[e[1]])
            yy = y
            for s_, sz, bd in rows_:
                yy -= sz * 1.18
                sh.text(s_, tx, yy + sz * 0.2, sz, COL["ink"] if bd else COL["ink2"], bold=bd)
            y = min(yy, y - 2 * BADGE_R) - 1.8
    if nis:
        if y < h_nogo + 1.0:
            warn.append(u"masterplan page: the side column runs {:.1f} mm over (legend, moves, areas left as they "
                        u"are)".format(h_nogo + 1.0 - y))
        pl28_list_nogo(sh, nis, x0, h_nogo + 1.0, cw)


# v28: the route's legend samples (before the core's LEGEND_V24 rows of the same key)
def _pl23_sw_bike():
    def f(pg, x, y, w, h):
        pg.line([(x, y + h * 0.3), (x + w, y + h * 0.3)], PL23_WALK_COL, 0.5, alpha=0.85)
        ticks_line(pg, [(x, y + h * 0.65), (x + w, y + h * 0.65)], PL23_BIKE_COL, 0.25, 1.6, 0.5, 1.0, alpha=0.9)
    return f


PL23_LEGEND = [("walk", u"Riverside walk", _sw_line(PL23_WALK_COL, 0.5, alpha=0.85)),
               ("walk_bed", u"Bed walk, shut in floods", _sw_line(PL23_WALK_COL, 0.5, [1.6, 0.6], 0.85)),
               ("bike", u"Bike lane beside the walk", _pl23_sw_bike()),
               ("arm", u"Planted side arm", _sw_softline(COL["river_mid"], 1.6, 0.6))]   # D2 a: not "reed"
PL23_LEG_KEYS = set(k_ for k_, _, _ in PL23_LEGEND)


# ---------------------------------------------------------------- the page
def plan_page(C, warn):
    """v28 (revision 29 Oct, WO-T4b-2, package H "Page 23"): the masterplan page (crop mp_plan, 392 x 238 mm). The
    analysis frame in two rows at 1:5,000 (pl23_rows; one 1:10,000 strip when they do not fit), upstream half on top,
    each with every layer of the corridor (draw_corridor: the walk and bike lane too), the study area outline, a
    dashed match line where the halves meet and its marks row (north arrow, scale bar, flow note). On the map: place
    names (Turkish), the numbered moves as short boxed texts on arrows and the letters of the areas left as they are
    (pl23_callouts), the distances between the bridge hubs along the walk (pl23_hub_gaps). The side column: small
    legend, moves with no room on the map, the areas left as they are (pl23_side). Public sources go to the sources
    page (sh.plan_sources -> plan_sources)."""
    scale, rows = pl23_rows(C, warn)
    k = 1000.0 / scale
    V = C.V
    W, H = BK_W, BK_H
    dh = (V.v1 - V.v0) * k
    sh = Page(W, H)
    sh.poly([rect(0, 0, W, H)], fill=COL["paper"])
    used, taken, rws, x_side = set(), [], [], 0.0
    y_top = H
    for i, row in enumerate(rows):
        dw = (row["b"] - row["a"]) * k
        x0, y0 = 0.0, y_top - dh
        T, mine = pl23_row_T(C, row, k)
        tk = [b for P in pl28_study(C) for b in boxes_along([T(p) for p in P + P[:1]], 1.2)]   # G4: names keep off it
        pg = Page(dw, dh)
        u_, _ = draw_corridor(pg, T, k, C, mine, tk, dw, dh)
        used |= u_
        if pl28_draw_study(pg, C, T):
            used.add("study")
        sh.clip([rect(x0, y0, x0 + dw, y0 + dh)])
        blit(sh, pg, x0, y0)
        sh.unclip()
        sh.poly([rect(x0, y0, x0 + dw, y0 + dh)], stroke=COL["ink2"], lw=0.25, alpha=0.45)   # the row's edge = the frame
        Ts, _ = pl23_row_T(C, row, k, x0, y0)
        taken += [(b[0] + x0, b[1] + y0, b[2] + x0, b[3] + y0) for b in tk]
        taken += [b for b in pl23_busy(C, Ts) if b[2] > x0 and b[0] < x0 + dw and b[3] > y0 and b[1] < y0 + dh]
        if len(rows) > 1:                                 # the match line where the halves meet
            xm = x0 + ((row["eb"] if i == 0 else row["ea"]) - row["a"]) * k
            sh.line([(xm, y0), (xm, y0 + dh)], COL["ink2"], 0.3, [1.6, 0.8], cap=0)
            t_ = u"match line · continues in the row below" if i == 0 else u"match line · from the row above"
            tw = text_w(t_, KEY_MIN)
            tx = xm - 1.2 - tw if i == 0 else xm + 1.2
            sh.text(t_, tx, y0 + dh - 3.4, KEY_MIN, COL["ink2"], halo=COL["white"])
            taken.append((tx, y0 + dh - 3.8, tx + tw, y0 + dh - 0.4))
            taken.append((xm - 0.8, y0, xm + 0.8, y0 + dh))
        rws.append((Ts, mine, (x0 + 0.8, y0 + 0.8, x0 + dw - 0.8, y0 + dh - 0.8)))
        if i == 0:
            runs = [(u"the water flows ", False), (u"left to right", True), (u", the upstream entry at the left end", False)]
        else:
            runs = [(u"downstream half · ", True), (u"the water flows left to right", False)]
        pl23_marks(sh, C, x0, y0 - PL23_MARK_H, scale, runs)
        x_side = max(x_side, dw)
        y_top = y0 - PL23_MARK_H - PL23_GAP
    if y_top + PL23_GAP < -0.5 or x_side > W - PL23_SIDE_MIN:
        warn.append(u"masterplan page: the map ({:.0f} x {:.0f} mm) runs over the {:.0f} x {:.0f} mm crop".format(
            x_side, H - y_top - PL23_GAP, W, H))
    ents, nis = pl23_callouts(sh, C, rws, taken)
    pl23_hub_gaps(sh, C, rws, taken)
    for nt, grp, nm, line, ok in ents:
        if not ok:
            warn.append(u"masterplan move {} has no room on the map: listed in the side column ({})".format(nt["n"], nm))
    pl23_side(sh, x_side + PL23_SIDE_GAP, W, H, used, ents, nis, warn)
    sh.crop = (0.0, 0.0, W, H)
    sh.key, sh.world, sh.scale, sh.pleg = "plan", bbox(C.V.P), scale, None
    sh.bid = ("mp_plan", "c1_s1", u"Masterplan: the ecological corridor of the whole {}".format(R28_FRAME_NAME.lower()))
    sh.plan_sources = pl28_plan_sources(ents, nis)
    C.ni_placed = sum(1 for r_ in C.nogo if r_.get("placed"))
    return sh
