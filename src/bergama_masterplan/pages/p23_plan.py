# p.23 the plan: plan_page, the pl28_* functions and draw_corridor (split from parts/02_Design.py, parts/02b_detail.py, parts/02c_corridor.py, parts/02d_r28_ground.py on 29 Oct 2026; moved unchanged)


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
            place_label(pg, [(nm, PL28_TS if fine else (PLACE_TS if k < 0.5 else PLACE_TS * 1.15), True)], T(xy),
                        taken, dw, dh, ink, d0=1.5, anywhere=False)   # v27: 7.5 pt on the 1:10,000 strip (G4)
    if C.terrace and inP(C.terrace["xy"]):
        x, y = T(C.terrace["xy"])
        p2 = (C.terrace["xy"][0] + C.terrace["dir"][0] * 120.0, C.terrace["xy"][1] + C.terrace["dir"][1] * 120.0)
        x2, y2 = T(p2)
        place_label(pg, [(u"TRAJANEUM {:,.0f} m".format(C.terrace["d"]), LAB_TS, True)],   # v26: no arrow glyph
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
        return u"Viewing terrace", u"a clear sightline to the Trajaneum, {:,.0f} m away".format(C.terrace["d"])
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
             "arm": (u"Reed side arm", u"a reed channel cleans the return water")}
    return fixed.get(k[0], (nt["text"][:1] + nt["text"][1:].lower(), u""))


def pl28_letter(i):
    return u"abcdefghijklmnopqrstuvwxyz"[i] if i < 26 else str(i + 1)


def pl28_spot(x, y, s, taken, bounds, rank):
    """G4: a free s x s box near (x, y): label_spot (common/label_place.py) on the boxes within its reach; else for a
    rank-0 marker the nearest free spot anywhere in bounds, on a leader (place_labels_all); None when there is none."""
    R = 32.0                                             # label_spot's farthest ring (24 mm) + the box + its leader
    near = [t for t in taken if t[2] > x - R and t[0] < x + R and t[3] > y - R and t[1] < y + R]
    got = label_spot(x, y, s, s, near, bounds, pad=0.3)
    if got:
        return got[0]
    if rank:
        return None
    got = place_labels_all([{"x": x, "y": y, "wh": lambda f: (s, s), "rank": 0}], list(taken), bounds, sizes=(1.0,),
                           pad=0.3).get(0)
    return got[0] if got else None


def pl28_plan_markers(sh, C, T, inP, taken, bounds):
    """P23.1 (G4): the numbered markers in their group's colour at each note's places on the strip (the first place
    must show, more places may drop), then a grey letter for each area left as it is (no intervention), on free
    spots (pl28_spot: rings round the point, a thin leader in the marker's colour when moved; the bands above and
    below the strip may hold a marker). Returns (entries, letters): [[note, group, name, line, placed]],
    [[letter, region, placed]]; a lettered region gets r_["placed"]."""
    r, rn = BADGE_R, PL28_NI_R
    mk = dict((k_, hx) for k_, lab, hx in R28_MARKERS)
    items, ents, nis = [], [], []                       # items: (x, y, radius, rank, kind, label, colour, owner)
    for nt in sorted(C.notes, key=lambda nt_: nt_["n"]):
        grp = pl28_note_group(nt)
        nm, line = pl28_note_entry(C, nt)
        ents.append([nt, grp, nm, line, False])
        first = True
        for p in nt["at"]:
            if inP(p):
                x, y = T(p)
                items.append((x, y, r, 0 if first else 1, "n", str(nt["n"]), mk[grp], ents[-1]))
                first = False
    for i, r_ in enumerate(C.nogo):
        nis.append([pl28_letter(i), r_, False])
        p = next((q for q in r_["at"] if inP(q)), None)
        if p is not None:
            x, y = T(p)
            items.append((x, y, rn, 0, "ni", nis[-1][0], COL["ink2"], nis[-1]))
    for i in sorted(range(len(items)), key=lambda i_: items[i_][3]):
        x, y, rr, rank, kind, lab, col, own = items[i]
        b = pl28_spot(x, y, 2.0 * rr, taken, bounds, rank)
        if b is None:
            continue
        taken.append(b)
        cx, cy = (b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0
        d = math.hypot(cx - x, cy - y)
        if d > rr + 0.4:                                 # the leader from the place to the marker's edge
            sh.line([(x, y), (cx - (cx - x) / d * rr, cy - (cy - y) / d * rr)], col, 0.18)
            sh.circle(x, y, 0.35, fill=col)
        if kind == "n":
            sh.circle(cx, cy, rr + 0.25, fill=COL["white"])
            sh.circle(cx, cy, rr, fill=col)
            sh.text(lab, cx, cy - BADGE_TS * 0.36, BADGE_TS, COL["white"], bold=True, align="C")
            own[4] = True
        else:
            sh.circle(cx, cy, rr, fill=COL["white"], stroke=col, lw=0.2)
            sh.text(lab, cx, cy - KEY_MIN * 0.36, KEY_MIN, col, bold=True, align="C")
            own[2] = True
            own[1]["placed"] = own[1].get("placed", 0) + 1
    return ents, nis


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


def pl28_plan_list(sh, ents, nis, y_top, warn):
    """P23.2: the list under the strip, by group in the markers' order and colours, in four columns (roads | hubs and
    transit | water and ecology | crossings, heritage and views, the areas left as they are): each entry the coloured
    number, its name in bold, one short line in a lighter grey; airy (2.6 mm between entries, 3.4 mm between
    groups)."""
    mk = dict((k_, (lab, hx)) for k_, lab, hx in R28_MARKERS)
    cols = (("roads",), ("hubs",), ("water",), ("crossings", "heritage", "nogo"))
    r = BADGE_R
    for ci, keys in enumerate(cols):
        x = PL28_COLS[ci]
        cw = (BK_W - x) if ci == len(cols) - 1 else PL28_COL_W
        tx, y = x + 2 * r + 2.2, y_top
        for key in keys:
            if key == "nogo":
                y = pl28_list_nogo(sh, nis, x, y, cw) if nis else y
                continue
            rows = [e for e in ents if e[1] == key]
            if not rows:
                continue
            lab, col = mk[key]
            y = pl28_list_head(sh, lab, col, x, y, cw)
            for nt, grp, nm, line, ok in rows:
                sh.circle(x + r, y - r, r, fill=col)
                sh.text(str(nt["n"]), x + r, y - r - BADGE_TS * 0.36, BADGE_TS, COL["white"], bold=True, align="C")
                yy = y
                for s_ in wrap(nm, PL28_HEAD_TS, cw - (tx - x), True):
                    yy -= PL28_HEAD_TS * 1.18
                    sh.text(s_, tx, yy + PL28_HEAD_TS * 0.2, PL28_HEAD_TS, COL["ink"], bold=True)
                for s_ in (wrap(line, PL28_TS, cw - (tx - x)) if line else []):
                    yy -= PL28_TS * 1.18
                    sh.text(s_, tx, yy + PL28_TS * 0.2, PL28_TS, COL["ink2"])
                y = min(yy, y - 2 * r) - 2.6
            y -= 3.4
        if y < 1.0:
            warn.append(u"masterplan list: column {} runs {:.1f} mm below the crop".format(ci + 1, 1.0 - y))


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
    """P23.2 / N2: what the list no longer prints, for the booklet's sources page, keyed by the marker numbers (and
    letters) on the masterplan page: every reason of every note, whole, with a kind hint (pl28_src_kind)."""
    return {"crop": "mp_plan", "heading": u"Masterplan: what each numbered move stands on",
            "markers": [{"n": nt["n"], "group": grp, "name": nm, "line": line,
                         "sources": [{"text": s_, "kind": pl28_src_kind(s_)} for s_ in nt["why"]]}
                        for nt, grp, nm, line, ok in ents],
            "left_as_is": [{"id": lt, "ha": round(r_["ha"], 2), "why": PL28_SRC_TAG.sub(u"", r_["why"]),
                            "sources": [PL28_SRC_NAME.get(m_, m_) for m_ in PL28_SRC_TAG.findall(r_["why"])]}
                           for lt, r_, ok in nis]}


# ---------------------------------------------------------------- the two pages
def plan_page(C, warn):
    """v27 (MIRAQUA 28 Oct, P23.1-P23.3, G4, G7, G8): the masterplan page (crop mp_plan). Top-left ONE strip of the
    whole analysis frame at 1:10,000 (284.5 x 52.9 mm, PL28_BAND above and below for markers) with every layer of the
    corridor and the study area outline; the numbered markers in their group's colour (R28_MARKERS); the scale bar
    row under the strip; the legend beside it (from COL_X, two columns); under them, from PL28_TOP, the list by group
    in four columns. The reasons and source codes go to the sources page (sh.plan_sources -> plan_sources)."""
    k = 1000.0 / MP_SCALE
    g = pl28_strip(C, k)
    T, inP, dw, dh = g["T"], g["inP"], g["dw"], g["dh"]
    W, H = BK_W, BK_H
    if dw > COL_X - 6.0 or dh > 60.0:
        warn.append(u"the analysis frame at 1:{:,.0f} ({:.0f} x {:.0f} mm) is larger than the strip's room".format(
            MP_SCALE, dw, dh))
    taken = [b for P in pl28_study(C) for b in boxes_along([T(p) for p in P + P[:1]], 1.2)]   # G4: names keep off it
    pg = Page(dw, dh)
    used, _ = draw_corridor(pg, T, k, C, inP, taken, dw, dh)
    if pl28_draw_study(pg, C, T):
        used.add("study")
    sh = Page(W, H)
    sh.poly([rect(0, 0, W, H)], fill=COL["paper"])
    x0, y0 = 0.0, H - PL28_BAND - dh
    sh.clip([rect(x0, y0, x0 + dw, y0 + dh)])
    blit(sh, pg, x0, y0)
    sh.unclip()
    sh.poly([rect(x0, y0, x0 + dw, y0 + dh)], stroke=COL["ink2"], lw=0.25, alpha=0.45)   # the strip's edge = the frame
    Ts = lambda p: (T(p)[0] + x0, T(p)[1] + y0)
    tk = [(b[0] + x0, b[1] + y0, b[2] + x0, b[3] + y0) for b in taken]
    ents, nis = pl28_plan_markers(sh, C, Ts, inP, tk, (x0, y0 - PL28_BAND, x0 + dw, y0 + dh + PL28_BAND))
    for nt, grp, nm, line, ok in ents:
        if not ok:
            warn.append(u"masterplan note {} not placed on the plan (no free spot): {}".format(nt["n"], nt["text"]))
    y_row = y0 - PL28_BAND - 10.0
    pl28_marks(sh, C, x0, y_row)
    pl28_legend(sh, [(u"EXISTING · SURVEY", [(nm, f) for key, nm, f in LEGEND_V24 if key in used and key in EXISTING]),
                     (u"PROPOSED", [(nm, f) for key, nm, f in LEGEND_V24 if key in used and key not in EXISTING])],
                COL_X, W, H, y_row, 2, warn)
    pl28_plan_list(sh, ents, nis, PL28_TOP, warn)
    sh.crop = (0.0, 0.0, W, H)
    sh.key, sh.world, sh.scale, sh.pleg = "plan", bbox(C.V.P), MP_SCALE, None
    sh.bid = ("mp_plan", "c1_s1", u"Masterplan: the ecological corridor of the whole {}".format(R28_FRAME_NAME.lower()))
    sh.plan_sources = pl28_plan_sources(ents, nis)
    C.ni_placed = sum(1 for r_ in C.nogo if r_.get("placed"))
    return sh


def pl28_chart(sh, x, y, w, head, runs, rows):
    """v27 (P21.1): one bar chart in the map's colours: head, one line (G5: bold keyword), bars [(name, m2, fill,
    stripes)] scaled to the largest, values in ha (G13); returns the y under it."""
    y -= PL28_HEAD_TS * 1.18
    sh.text(head, x, y + 0.5, PL28_HEAD_TS, COL["ink_dark"], bold=True)
    y -= PL28_TS * 1.3
    pl28_runs(sh, x, y + 0.5, runs, PL28_TS, COL["ink2"])
    y -= 1.5
    vmax = max([a for _, a, _, _ in rows] + [1.0])
    lab, room = 44.0, w - 44.0 - 20.0
    for nm, a, fill, stripes in rows:
        y -= 5.2
        sh.text(nm, x, y + 0.75, PL28_TS, COL["ink"])
        bw = max(0.3, room * a / vmax)
        sh.poly([rect(x + lab, y, x + lab + bw, y + 3.4)], fill=fill, stroke=COL["ink2"], lw=0.1, stripes=stripes)
        sh.text(u_area(a, "ha"), x + lab + bw + 1.5, y + 0.75, PL28_TS, COL["ink"], bold=True)
    return y


# ---------------------------------------------------------------- D1: the open ground for the site board
def pl28_corners(L):
    """a traced cell outline with its straight-through vertices dropped (exact: every step is axis-parallel)"""
    n = len(L)
    out = []
    for i in range(n):
        a, b, c_ = L[i - 1], L[i], L[(i + 1) % n]
        if (b[0] - a[0]) * (c_[1] - b[1]) != (b[1] - a[1]) * (c_[0] - b[0]):
            out.append(b)
    return out


def pl28_open_ground_json(C, path):
    """v27 (MIRAQUA 28 Oct, D1, G10): the masterplan's open ground for the site board's filter sheet (drw_filter; the
    site board runs after the masterplan): {frame_ha (the frame polygon), open_ha, classes {open, building, road, bed:
    {ha, rings}}, definition, cell_m, rings, source}. ha from the ONE count of pl28_frame_stats; rings = the outlines
    of each class's grid cells inside the frame (trace), straight-through vertices dropped, survey m to 0.1 m, holes
    clockwise (fill even-odd). Written compact (no indent). Returns the dict."""
    G, F, V, inF = C.G, C.F, C.V, C.inF
    sets = (set(), set(), set(), set())
    for n in range(C.N):                                 # one pass: the cells inside the frame by class
        if inF[n]:
            sets[F[n]].add(n)
    cls = {}
    for name, code in (("open", 0), ("building", 1), ("road", 2), ("bed", 3)):
        rings_ = []
        for Lp in trace(G, sets[code]):
            Q = pl28_corners(Lp)
            if len(Q) >= 4:
                rings_.append([[round(x, 1), round(y, 1)] for x, y in (V.xy(u, v) for u, v in Q)])
        cls[name] = {"ha": round(C.stats[code] / 1e4, 2), "rings": rings_}
    out = {"frame_ha": round(C.frame_m2 / 1e4, 2), "open_ha": round(C.stats[0] / 1e4, 2), "classes": cls,
           "definition": u"Open ground (masterplan) = every {:.0f} m grid cell of the analysis frame with no survey "
                         u"building, no survey road ({:.1f} m either side of a street edge) and not the stream bed; "
                         u"only cells centred inside the frame count".format(G.c, ROAD_BUF_M),
           "cell_m": round(G.c, 3), "rings": u"survey m; the outlines of each class's grid cells (holes clockwise), "
                                             u"fill even-odd",
           "source": u"{} · {}".format(VERSION, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))}
    with open(path, "w", encoding="utf-8") as f_:
        json.dump(out, f_, ensure_ascii=False, separators=(",", ":"))
    return out
