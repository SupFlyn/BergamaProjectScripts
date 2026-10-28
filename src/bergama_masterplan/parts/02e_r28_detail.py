# ---- MIRAQUA round 28 Oct 2026 (masterplan v27): p.24 the two 1:1,000 plans in the fade-out programme language (worker MP-detail). Shared pieces: common/r28_style.py,
# common/units.py, common/label_place.py, common/figures.py (revision_2026-10-28/PLAN.md).
# v27 (MIRAQUA 28 Oct, P24.1-P24.5, F11): the two 1:1,000 windows (crops dt_upstream, dt_k5; DT_WINDOWS, their frames,
# DT_SCALE, the scale bars and the crops kept) in the programme-diagram language of the references: p24_ref2 (faint
# grey plan, soft fields fading into each other, one big bold word per field, small grey words for the sub-spaces, a
# dot legend) and p24_ref1 (translucent overlaps that mix). Layers, bottom up: the survey as a faint grey underlay ->
# the programme fields (R28_ZONES, stepped translucent rings) -> terrace edges, canopied walk, stepping stones -> the
# water route 1-4 in one line language (line, arrowhead, numbered dot) -> study-area outline (G8) -> the levels at the
# channel cuts -> words (common/label_place, G4). Gone: the ochre programme rings and the hub and café pictograms
# (P24.3), plant codes and band letters (P24.4, F11), survey spot heights, terrace-step sketches and ramps (P24.5),
# the flood bands across the stream (F11: they read as cut lines).
# The programmes of the masterplan's data, each mapped to one R28_ZONES key (shared with the senses page, MP-senses):
#   reed      zone base WT (cleansing reed basins) and WD (spillway); the corridor's reed side arms
#   terraces  WS (dry-top retention terraces); the corridor's terrace edges on the contours (R28DT_TERR_M either side)
#   hub       the corridor's dry hub squares (K3, K4, K5, İstiklal); their programme rings (H1) are now its fade
#   subhub    the bed stations of the sub-hubs (R28DT_SUB_M[0] round the station line), fading along the amphibious
#             bed WA (tier W) within R28DT_SUB_M[1] of the station
#   demeter   DG (Demeter's Garden)
#   forest    the corridor's forest cells (FOREST), its tree-planted cells (TREES, one step lighter), GR (shaded walk,
#             raised dry top)
#   wetland   the corridor's widened stream; WA flood terrace (tier F); WP (floodable riverside planting)
#   cafe      R28DT_CAFE_M round the café points (the GR and DG zones, where v26 drew the café pictograms)
# Fields, steps and sizes are graphic (a design reading of the zones), never areas: the figures stay the zone curves'.
R28DT_STEP_M = 4.0                   # one fade step, m
R28DT_HALO, R28DT_INSET = 3, 2       # steps round a field (fading out) and inside it (denser to its core)
R28DT_A = 0.075                      # opacity of one step: they add up to about 0.37 at a field's core (G6: light)
R28DT_A_ZONE = {"forest": 0.06}      # the corridor's long background field a little lighter
R28DT_CAFE_M = 8.0                   # a café field: this far round its point, m
R28DT_SUB_M = (6.0, 60.0)            # sub-hub: this far either side of its station line; the bed within this far of it
R28DT_TERR_M = 4.0                   # terraces: this far either side of a terrace edge, m
R28DT_ARM_M = 3.0                    # reed side arm: this far either side of its line, m
R28DT_WET = ("reed", "wetland", "subhub")    # fields that may also fade over the bed (the others over open ground)
R28DT_ORDER = ("forest", "terraces", "wetland", "reed", "demeter", "hub", "subhub", "cafe")   # drawn in this order
R28DT_TS = dict(zone=4.2, place=3.5, label=2.65, small=2.47)   # mm at 1:1: 12, 10, 7.5, 7 pt (booklet type sizes)
R28DT_TITLE_MM2 = 60.0               # a field shows less than this on a window: no title there (mm², = m² at 1:1,000)
R28DT_ROUTE = dict((k_, c_) for k_, _, c_ in R28_MARKERS)["water"]   # the water route = p.23's water markers
R28DT_CODE = {("WT", None): "reed", ("WD", None): "reed", ("WS", None): "terraces", ("DG", None): "demeter",
              ("GR", None): "forest", ("WA", "F"): "wetland", ("WP", None): "wetland", ("WA", "W"): "subhub"}
# The small grey line under a field's title (P24.4, F11): plants only from p.16's list (water board SPECIES, the nine
# kept) where p.16 places them, printed as common/plant_photos.py PLANTS prints them ("English (Turkish)"); the
# forest corridor's trees (ash, poplar, oak, elm) and the cattails are not on that list: not named.
R28DT_SUB = {"reed": (u"Common reed (Kamış)", u"Water mint (Su nanesi)"),     # p.16: reed beds, upstream entry
             "terraces": (u"French lavender (Karabaş otu)",),                  # dry top, above Q500
             "hub": (u"Oriental plane (Doğu çınarı)",),                        # dry hub squares K3, K4, K5
             "demeter": (u"Olive (Zeytin)",),                                  # dry top, Demeter's Garden K5
             "wetland": (u"White willow (Ak söğüt)", u"Tamarisk (Ilgın)"),     # willow band, flood terraces
             "subhub": (u"stepping stones · closes in floods",)}


def _r28_nb(c):
    return ((1, 0, c), (-1, 0, c), (0, 1, c), (0, -1, c), (1, 1, c * 1.4142), (-1, 1, c * 1.4142),
            (1, -1, c * 1.4142), (-1, -1, c * 1.4142))


def _r28_depth(C, K, dmax):
    """{cell: m} how deep each cell of set K lies inside it (from its edge cells, c / 2), up to dmax."""
    G = C.G
    nx, ny, c = G.nx, G.ny, G.c
    d, hp = {}, []
    for n in K:
        i, j = n % nx, n // nx
        if i == 0 or j == 0 or i == nx - 1 or j == ny - 1 or (n - 1) not in K or (n + 1) not in K or \
                (n - nx) not in K or (n + nx) not in K:
            d[n] = c * 0.5
            hp.append((c * 0.5, n))
    heapq.heapify(hp)
    nb = _r28_nb(c)
    while hp:
        dd, n = heapq.heappop(hp)
        if dd > d.get(n, 1e9):
            continue
        i, j = n % nx, n // nx
        for di, dj, w in nb:
            ii, jj = i + di, j + dj
            if 0 <= ii < nx and 0 <= jj < ny:
                m = jj * nx + ii
                e = dd + w
                if e <= dmax and m in K and e < d.get(m, 1e9):
                    d[m] = e
                    heapq.heappush(hp, (e, m))
    return d


def _r28_spread(C, base, allow):
    """{cell: strength}: the strongest of base[m] less one per R28DT_STEP_M from m, over cells allow(n); kept while
    it is 1 or more (the faintest step)."""
    G = C.G
    nx, ny = G.nx, G.ny
    v = dict(base)
    hp = [(-s, n) for n, s in base.items()]
    heapq.heapify(hp)
    nb = [(di, dj, w / R28DT_STEP_M) for di, dj, w in _r28_nb(G.c)]
    while hp:
        s, n = heapq.heappop(hp)
        s = -s
        if s < v.get(n, 0.0):
            continue
        i, j = n % nx, n // nx
        for di, dj, w in nb:
            ii, jj = i + di, j + dj
            if 0 <= ii < nx and 0 <= jj < ny:
                m = jj * nx + ii
                e = s - w
                if e >= 1.0 - 1e-6 and e > v.get(m, 0.0) + 1e-9 and (m in base or allow(m)):
                    v[m] = e
                    heapq.heappush(hp, (-e, m))
    return v


def _r28_loops(C, cells):
    """Smooth survey rings (m) of a cell set: outer rings counter-clockwise, holes clockwise (fill even-odd)."""
    out = []
    for Lp in trace(C.G, set(cells)):
        Q = smooth(Lp, C.G.c * 0.5, 2)
        if len(Q) >= 3 and abs(area2(Q)) > 4.0 * C.G.c * C.G.c:
            out.append([C.V.xy(u, v) for u, v in Q])
    return out


def r28_zone_strength(C):
    """{zone key: (own cells {cell: base}, strength {cell: s})} of every R28_ZONES field over the whole frame, on the
    corridor's grid, worked out once a press (kept on C). A zone's own cells are R28DT_HALO + 1 at its edge and up to
    R28DT_INSET more inside (one per R28DT_STEP_M of depth); its lighter part (tree-planted cells, the amphibious bed
    near a sub-hub) R28DT_HALO or less; round them the strength drops by one per R28DT_STEP_M over open ground (the
    water fields also over the bed). Fade step t = the cells of strength t or more."""
    got = getattr(C, "_r28_v", None)
    if got is not None:
        return got
    G, V, F, Dst, N = C.G, C.V, C.F, C.Dst, C.N
    core = dict((k_, set()) for k_, _, _ in R28_ZONES)
    light = dict((k_, {}) for k_, _, _ in R28_ZONES)
    cells_of = lambda P: G.poly_cells([V.uv(p) for p in P])

    def along(P, r):
        out = set()
        for p in densify(P, G.c * 0.5):
            out.update(C.near_cells(p, r))
        return out
    bed, other = [], set()
    for z in C.D.zones:
        key = R28DT_CODE.get((z["code"], z["tier"])) or R28DT_CODE.get((z["code"], None))
        if key == "subhub":
            bed.append(cells_of(z["P"]))
        elif key:
            core[key].update(cells_of(z["P"]))
        else:
            other.add(z["code"] + (z["tier"] or u""))
        if z["code"] in ("GR", "DG"):
            core["cafe"].update(C.near_cells(z["q"], R28DT_CAFE_M))
    if other:
        C.warn.append(u"p.24 fields: zone codes with no programme field (R28_ZONES): " + u", ".join(sorted(other)))
    r0, reach = R28DT_SUB_M
    for h in C.hubs:
        for L_ in h.get("square") or []:
            core["hub"].update(cells_of(L_))
        s = h.get("sub_xy")
        if not s:
            continue
        a, b = s["a"], s["b"]
        for n in C.near_cells(s["c"], math.hypot(b[0] - a[0], b[1] - a[1]) / 2.0 + r0):
            x, y = C.wxy(n)
            if seg_dist(x, y, a, b) <= r0:
                core["subhub"].add(n)
        for cs in bed:                                   # the amphibious bed near the station, fading along the bed
            for n in cs:
                x, y = C.wxy(n)
                d = math.hypot(x - s["c"][0], y - s["c"][1])
                if d < reach:
                    lv = float(R28DT_HALO - int(R28DT_HALO * d / reach))
                    if lv > light["subhub"].get(n, 0.0):
                        light["subhub"][n] = lv
    for w_ in C.widen:
        core["wetland"].update(cells_of(w_["ring"]))
    for a_ in C.arms:
        core["reed"].update(along(a_["P"], R28DT_ARM_M))
    for P in C.terr:
        core["terraces"].update(along(P, R28DT_TERR_M))
    dh = C.dh
    for n in range(N):                                   # the corridor's planting rule (Corridor.planting), per cell
        if F[n] != 0 or Dst[n] > TREES[1]:
            continue
        if FOREST[0] <= Dst[n] <= FOREST[1] and dh[n] >= FOREST[2]:
            core["forest"].add(n)
        elif TREES[0] <= Dst[n] and dh[n] >= TREES[2]:
            light["forest"][n] = float(R28DT_HALO)
    out = {}
    for key, _, _ in R28_ZONES:
        K, base = core[key], {}
        if K:
            dep = _r28_depth(C, K, R28DT_INSET * R28DT_STEP_M)
            for n in K:
                base[n] = R28DT_HALO + 1.0 + min(float(R28DT_INSET), dep.get(n, 1e9) / R28DT_STEP_M)
        for n, lv in light[key].items():
            if n not in base:
                base[n] = lv
        if not base:
            continue
        if key in R28DT_WET:
            allow = lambda m: F[m] == 0 or F[m] == 3
        else:
            allow = lambda m: F[m] == 0
        out[key] = (base, _r28_spread(C, base, allow))
    C._r28_v = out
    return out


def r28_zone_fields(C):
    """[(zone key, rings)]: each R28_ZONES programme field over the whole frame (its own cells: core and lighter
    part, no fade), survey m, closed rings (fill even-odd), in R28_ZONES order; worked out once a press (kept on C).
    Shared helper: the senses page (MP-senses) builds its fade-out zones from the same fields."""
    got = getattr(C, "_r28_fields", None)
    if got is None:
        S = r28_zone_strength(C)
        got = [(k_, _r28_loops(C, list(S[k_][0]))) for k_, _, _ in R28_ZONES if k_ in S]
        got = [(k_, r_) for k_, r_ in got if r_]
        C._r28_fields = got
    return got


def _r28_cells_in(C, R, m):
    """The grid cells whose centre lies within m of the survey rectangle R = (x0, y0, x1, y1)."""
    G, V = C.G, C.V
    x0, y0, x1, y1 = R[0] - m, R[1] - m, R[2] + m, R[3] + m
    U = [V.uv(p) for p in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
    i0 = max(0, int((min(u for u, v in U) - G.x0) / G.c))
    i1 = min(G.nx - 1, int((max(u for u, v in U) - G.x0) / G.c) + 1)
    j0 = max(0, int((min(v for u, v in U) - G.y0) / G.c))
    j1 = min(G.ny - 1, int((max(v for u, v in U) - G.y0) / G.c) + 1)
    out = set()
    for j in range(j0, j1 + 1):
        for i in range(i0, i1 + 1):
            n = j * G.nx + i
            x, y = V.xy(*G.xy(n))
            if x0 <= x <= x1 and y0 <= y <= y1:
                out.add(n)
    return out


def r28_zone_levels(C, R=None, margin=10.0):
    """[(zone key, [(t, rings)])]: the fade steps of every R28_ZONES field, t = 1 (faintest, outermost) up to
    R28DT_HALO + 1 + R28DT_INSET (the core), survey m rings (fill even-odd, one step at R28DT_A over the other), in
    R28DT_ORDER (the drawing order). R = (x0, y0, x1, y1) survey m: only the cells within margin of it (a window);
    None: the whole frame (kept on C; for the senses page)."""
    if R is None and getattr(C, "_r28_levels", None) is not None:
        return C._r28_levels
    W_ = _r28_cells_in(C, R, margin) if R is not None else None
    S = r28_zone_strength(C)
    out = []
    for key in R28DT_ORDER:
        if key not in S:
            continue
        items = [(n, s) for n, s in S[key][1].items() if W_ is None or n in W_]
        lv = []
        for t in range(1, R28DT_HALO + 2 + R28DT_INSET):
            cs = [n for n, s in items if s >= t - 1e-6]
            if not cs:
                break
            rings = _r28_loops(C, cs)
            if rings:
                lv.append((t, rings))
        if lv:
            out.append((key, lv))
    if R is None:
        C._r28_levels = out
    return out


def _r28_base_cols():
    """The faint survey underlay's tones, mixed from the base map colours (COL, as load_palette set them)."""
    return {"bed": mix(COL["white"], COL["river"], 0.30), "bld": mix(COL["white"], COL["bld"], 0.60)}


def _r28_base(pg, C, T, R, segs):
    """v27 (P24.1, P24.2): the survey as a faint grey underlay: the bed, contours, stream lines, buildings (heritage
    with a thin outline), street edges; the bridges crisp (the base's only dark lines, kept free of words)."""
    cl = _r28_base_cols()
    Rm = (R[0] - 5.0, R[1] - 5.0, R[2] + 5.0, R[3] + 5.0)
    near = lambda Ls: [[T(p) for p in L_] for L_ in Ls if len(L_) >= 2 and hit(bbox(L_), Rm)]
    Ps = near(C.bed_loops)
    if Ps:
        pg.poly(Ps, fill=cl["bed"])
        leg(("r28dt", "bed"))
    for Q in near(C.contours):
        pg.line(Q, COL["contour10"], 0.12)
        leg(("r28dt", "contour"))
    for Q in near(C.streams):
        pg.line(Q, COL["river_mid"], 0.12, alpha=0.5)
    for role in ("building", "housing", "shed"):
        Ps = near(C.bld.get(role, []))
        if Ps:
            pg.poly(Ps, fill=cl["bld"])
            leg(("r28dt", "bld"))
    Ps = near(C.bld.get("heritage", []))
    if Ps:
        pg.poly(Ps, fill=cl["bld"], stroke=COL["her_edge"], lw=0.15)
        leg(("r28dt", "her"))
    Ps = near(C.built_since)
    if Ps:
        pg.poly(Ps, fill=cl["bld"], stripes=(COL["ink2"], 0.8, 0.12, 45.0))
        leg(("r28dt", "since"))
    for Q in near(C.roads):
        pg.line(Q, COL["ink2"], 0.15, alpha=0.4)
        leg(("r28dt", "street"))
    for Q in near(C.bridges):
        pg.line(Q, COL["ink"], 0.4)
        segs += list(zip(Q, Q[1:]))
        leg(("r28dt", "bridge"))


def _r28_wh(lines):
    """lines [(text, size, bold, colour)] -> (w, h), mm"""
    return max(text_w(s, sz, bd) for s, sz, bd, _ in lines), sum(sz * 1.18 for s, sz, bd, _ in lines)


def _r28_text(pg, lines, b, centre=False):
    y = b[3]
    for s, sz, bd, col in lines:
        y -= sz
        if centre:
            pg.text(s, (b[0] + b[2]) / 2.0, y, sz, col, bold=bd, align="C")
        else:
            pg.text(s, b[0], y, sz, col, bold=bd)
        y -= sz * 0.18


def _r28_free(b, taken, segs, bounds, pad):
    if not (bounds[0] <= b[0] and b[2] <= bounds[2] and bounds[1] <= b[1] and b[3] <= bounds[3]):
        return False
    return not any(lp_hit(b, t, pad) for t in taken) and not any(_lp_seg_box(p, q, b) for p, q in segs)


def _r28_spot(w, h, anchor, taken, segs, bounds, rank=0):
    """G4 (common/label_place): a free w x h box by anchor, (box, leader) or None; rank 0 always finds one."""
    got = place_labels_all([{"x": anchor[0], "y": anchor[1], "wh": lambda f: (w, h), "rank": rank}], taken, bounds,
                           segs, sizes=(1.0,), pad=0.5)
    return got[0][:2] if 0 in got else None


def _r28_label(pg, lines, anchor, taken, segs, bounds, rank=0, leader=True):
    """A word block beside its anchor, on a thin leader when it had to move off; its box or None (dropped)."""
    w, h = _r28_wh(lines)
    got = _r28_spot(w, h, anchor, taken, segs, bounds, rank)
    if got is None:
        return None
    b, far = got
    _r28_text(pg, lines, b)
    if far and leader:
        pg.line([anchor, lp_leader_end(b, anchor)], COL["ink2"], 0.15)
    return b


def _r28_title(pg, ring_, variants, taken, segs, bounds):
    """v27 (P24.1, P24.2): a field's title block, centred on the first free spot inside the field (its pole first),
    else beside the pole on a leader; the variants are tried in order (with the grey line, then without)."""
    spots = inside_spots(ring_, 12)
    for lines in variants:
        w, h = _r28_wh(lines)
        for x, y in spots:
            b = (x - w / 2.0, y - h / 2.0, x + w / 2.0, y + h / 2.0)
            if _r28_free(b, taken, segs, bounds, 0.6):
                _r28_text(pg, lines, b, True)
                taken.append(b)
                return b
    for lines in variants:
        b = _r28_label(pg, lines, spots[0], taken, segs, bounds, rank=0 if lines is variants[-1] else 1)
        if b:
            return b
    return None


def _r28_route_runs(order, L, a, b):
    """v27 (P24.2, G5): one water route step as text runs [(text, bold)]: the move, the zone in bold, its area and
    rough volume (v22-v26's figures and wording, sentence case)."""
    if order < len(ROUTE):
        words, end = ROUTE[order][1].capitalize(), ROUTE[order][2]   # "Into {}", "Back to the stream"
        z = (a, b)[end] if end is not None else None
        if z is None:
            w0, _, rest = words.partition(u" ")
            return [(w0, True), (u" " + rest, False)]
        nm = name_of(z, z.get("own", ""))
        nm = ROUTE_SHORT.get(nm, nm).lower()
        pre, _, post = words.partition(u"{}")
        runs = [(pre + u"the ", False), (nm, True)] + ([(post, False)] if post else [])
        runs.append((u" · " + u_area(z["m2"]), False))
        sv = store_m3(z)                                 # v22: rough volume, area x depth
        if sv:
            runs.append((u" · ~" + u_volume(round(sv[0], -1)) + sv[1], False))
            leg(("dt", "vol"))
        return runs
    t_ = (L["label"] or u"water").lower().replace(u"river", u"stream").capitalize()
    head, _, last = t_.rpartition(u" ")
    return [(head + u" ", False), (last, True)] if head else [(t_, True)]


def r28_window_panel(C, w, areas, missing, warn):
    """v27 (MIRAQUA 28 Oct, P24.1-P24.5, F11, G3-G5, G8, G13): a 1:1,000 window (p.24), north up, in the programme-
    diagram language (see the head of this part): faint survey, programme fields, the water route 1-4, the study
    area, the levels at the channel cuts, one title per field. The frame, scale, scale bar and crop of v26."""
    R = w["R"]
    k = 1000.0 / DT_SCALE
    dw, dh = (R[2] - R[0]) * k, (R[3] - R[1]) * k
    T = lambda p: ((p[0] - R[0]) * k, (p[1] - R[1]) * k)
    inP = lambda p: R[0] <= p[0] <= R[2] and R[1] <= p[1] <= R[3]
    on = lambda Q: hit(bbox(Q), (0.0, 0.0, dw, dh))
    _PLEG[0] = {}
    pg = Page(dw, dh)
    taken, segs, ts = [], [], R28DT_TS
    ink, ink1, ink2, white = COL["ink_dark"], COL["ink"], COL["ink2"], COL["white"]
    bounds = (1.0, 1.0, dw - 1.0, dh - 1.0)
    _r28_base(pg, C, T, R, segs)
    # ---- the programme fields: stepped translucent rings, densest at each field's core, mixing where they overlap
    tops = {}
    for key, lv in r28_zone_levels(C, R):
        hx, a_ = R28_ZONE[key][1], R28DT_A_ZONE.get(key, R28DT_A)
        seen = False
        for t, rings in lv:
            Ps = [Q for Q in ([T(p) for p in r_] for r_ in rings) if on(Q)]
            if not Ps:
                continue
            pg.poly(Ps, fill=hx, alpha=a_)
            seen = True
            if t >= R28DT_HALO:                          # the highest step that shows holds the title
                vis = [clip_ring(Q, (0.0, 0.0, dw, dh)) for Q in Ps]
                vis = [Q for Q in vis if len(Q) >= 3 and area2(Q) >= R28DT_TITLE_MM2]   # outer rings only
                if vis:
                    tops[key] = vis
        if seen:
            leg(("r28z", key))
    # ---- inside the fields: terrace edges on the contours, the canopied walk, stepping stones, footbridges, the
    # hidden-stream line (thin, in their field's colour or the base's)
    for P in C.terr:
        Q = [T(p) for p in P]
        if on(Q):
            pg.line(Q, R28_ZONE["terraces"][1], 0.3, alpha=0.8)
            leg(("r28dt", "terr"))
    canopy_at = []
    for P in C.canopy:
        Q = [T(p) for p in P]
        if on(Q):
            pg.line(Q, R28_ZONE["forest"][1], 0.3, [1.2, 0.9], cap=0, alpha=0.9)
            canopy_at += [p for p in P if inP(p)]
            leg(("r28dt", "canopy"))
    for c_ in C.cross:
        if c_["kind"] == "stepping stones" and inP(c_["xy"]):
            A_, B_ = T(c_["P"][0]), T(c_["P"][1])
            for i in range(5):
                f = (i + 0.5) / 5.0
                pg.circle(A_[0] + (B_[0] - A_[0]) * f, A_[1] + (B_[1] - A_[1]) * f, 0.8, fill=ink2, alpha=0.7)
            taken += boxes_along([A_, B_], 1.0)
            leg(("r28dt", "stones"))
        elif c_["kind"] == "footbridge":
            Q = [T(c_["P"][0]), T(c_["P"][1])]
            if on(Q):
                pg.line(Q, ink1, 0.5)
                segs.append((Q[0], Q[1]))
                leg(("r28dt", "foot"))
    for P in C.covered:
        Q = [T(p) for p in P]
        if on(Q):
            pg.line(Q, COL["river_mid"], 1.2, [1.6, 0.9], cap=0, alpha=0.7)
            leg(("r28dt", "hidden"))
    # ---- the water route (P24.2): the zone base's water links in the route's order, one line language on top
    rc = R28DT_ROUTE
    steps, shapes = [], C.D.zones + C.D.strips
    for L in C.D.links:
        if L["kind"] != "water" or len(L["P"]) < 2 or not any(inP(p) for p in L["P"]):
            continue
        a, b = link_shapes(L, shapes)
        ab = (a["code"] if a and a in C.D.zones else None, b["code"] if b and b in C.D.zones else None)
        steps.append((next((i for i, st in enumerate(ROUTE) if st[0] == ab), len(ROUTE)), L, a, b))
    steps.sort(key=lambda s_: s_[0])
    dots, key_lines = [], []
    for n_, (order, L, a, b) in enumerate(steps, 1):
        P = [T(p) for p in L["P"]]
        s = arclen(P)
        if s[-1] < 0.5:
            continue
        hl = min(1.8, s[-1] * 0.45)                      # arrowhead length, mm
        (tx, ty), (ux, uy) = at_len(P, s, s[-1])
        bx, by = tx - ux * hl, ty - uy * hl
        pg.line(sub_line(P, s, 0.0, s[-1] - hl * 0.8), rc, 0.6, cap=1)
        pg.poly([[(tx, ty), (bx - uy * hl * 0.42, by + ux * hl * 0.42), (bx + uy * hl * 0.42, by - ux * hl * 0.42)]],
                fill=rc)
        segs += list(zip(P, P[1:]))
        dots.append((n_, P[0]))
        key_lines.append((n_, _r28_route_runs(order, L, a, b)))
        leg(("r28dt", "route"))
    r_ = 1.9
    for n_, (x, y) in dots:                              # the step's number at its start, nudged off when taken
        b = (x - r_, y - r_, x + r_, y + r_)
        far = False
        if not _r28_free(b, taken, (), bounds, 0.2):
            got = label_spot(x, y, 2 * r_, 2 * r_, taken, bounds, (), 0.2)
            if got:
                b, far = got
        cx, cy = (b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0
        if far:
            pg.line([(x, y), lp_leader_end(b, (x, y))], rc, 0.2)
        pg.circle(cx, cy, r_ + 0.25, fill=white)
        pg.circle(cx, cy, r_, fill=rc)
        pg.text(str(n_), cx, cy - ts["small"] * 0.36, ts["small"], white, bold=True, align="C")
        taken.append(b)
    # ---- G8: the study area where it crosses the window
    st = R28_STUDY_LINE
    for A in (areas or {}).values():
        Q = [T(p) for p in list(A) + [A[0]]]
        if on(Q):
            pg.line(Q, st["colour"], st["width_mm"], list(st["dash_mm"]), cap=0)
            segs += list(zip(Q, Q[1:]))
            leg(("r28dt", "study"))
    # ---- P24.5: only the critical levels: bed, Q100 and Q500 at the surveyed channel cuts (CUT_AT); no flood band
    # across the stream (F11) and no survey spot heights (the survey has no point on the Üç Kemer deck)
    lev = []
    for num, nm, c, span, bed, q100, q500 in CUT_AT:
        if not inP(c):
            continue
        x, y = T(c)
        pg.line([(x - 0.8, y), (x + 0.8, y)], ink, 0.25)
        pg.line([(x, y - 0.8), (x, y + 0.8)], ink, 0.25)
        taken.append((x - 0.9, y - 0.9, x + 0.9, y + 0.9))
        lev.append(([(u"bed " + u_level(bed), ts["label"], False, ink),
                     (u"Q100 {} · Q500 {}".format(u_level(q100[0]), u_level(q500[0])), ts["label"], False, ink)],
                    (x, y)))
        leg(("r28dt", "level"))
    # ---- words (G4): levels and place names by their points, one title per field inside it, the route key, then
    # the sub-spaces (small grey, dropped where there is no room)
    for lines, anc in lev:
        if not _r28_label(pg, lines, anc, taken, segs, bounds):
            missing.append(lines[0][0])
    names = [(HUB_NAME[h["id"]], h["xy"]) for h in C.hubs] + \
        [(nm, xy) for nm, xy in BRIDGES_K if nm in (u"K1", u"K2")] + PLACES
    for nm, xy in names:
        if inP(xy) and not _r28_label(pg, [(nm, ts["place"], True, ink1)], T(xy), taken, segs, bounds):
            missing.append(nm)
    for key in R28DT_ORDER:
        if key not in tops:
            continue
        title = [(R28_ZONE[key][0], ts["zone"], True, ink)]
        sub = [(s_, ts["small"], False, ink2) for s_ in R28DT_SUB.get(key, ())]
        ring_ = max(tops[key], key=area2)
        if not _r28_title(pg, ring_, ([title + sub] if sub else []) + [title], taken, segs, bounds):
            missing.append(R28_ZONE[key][0])
    if key_lines:                                        # the route key (P24.2, G5): numbered dot, the step's words
        pitch, rr = 3.6, 1.5
        w_ = max([2 * rr + 1.2 + sum(text_w(t_, ts["label"], bd) for t_, bd in runs) for _, runs in key_lines] +
                 [text_w(u"Water route", ts["label"], True)])
        h_ = ts["label"] * 1.18 + 0.4 + pitch * len(key_lines)
        anc = (sum(p[0] for _, p in dots) / len(dots), sum(p[1] for _, p in dots) / len(dots)) if dots else \
            (dw / 2.0, dh / 2.0)
        got = _r28_spot(w_, h_, anc, taken, segs, bounds)
        if got:
            b = got[0]
            y = b[3] - ts["label"]
            pg.text(u"Water route", b[0], y, ts["label"], ink, bold=True)
            y -= ts["label"] * 0.18 + 0.4
            for n_, runs in key_lines:
                cy = y - pitch / 2.0
                pg.circle(b[0] + rr, cy, rr, fill=rc)
                pg.text(str(n_), b[0] + rr, cy - ts["small"] * 0.36, ts["small"], white, bold=True, align="C")
                x = b[0] + 2 * rr + 1.2
                for t_, bd in runs:
                    pg.text(t_, x, cy - ts["label"] * 0.36, ts["label"], ink1, bold=bd)
                    x += text_w(t_, ts["label"], bd)
                y -= pitch
        else:
            missing.append(u"water route key")
    words = []
    for z in C.D.zones:
        if z["code"] == "WD":
            words.append((u"spillway", z["q"]))
        elif z["code"] == "WT":
            words.append((u"clean-water classroom", z["q"]))   # v24's education mark: city link stop 7
    if canopy_at:
        words.append((u"canopied walk · seats", min(canopy_at, key=lambda p: (T(p)[0] - dw / 2) ** 2 +
                                                     (T(p)[1] - dh / 2) ** 2)))
    words += [(u"footbridge", c_["xy"]) for c_ in C.cross if c_["kind"] == "footbridge"]
    if C.terrace:
        words.append((u"viewing terrace", C.terrace["xy"]))
    words += [(u"step to the water", PLACES[1][1]), (u"deck on the Roman bank wall", ROMAN_WALL),
              (u"workshops", CRAFT_XY)]
    for rd in ROADS:
        if rd["change"] in ("pedestrian", "calmed", "shared"):
            P = rd["xy"]
            words.append((rd["change"] + (u" bridge" if u"Köprü" in rd["name"] else u" street"),
                          at_len(P, arclen(P), arclen(P)[-1] / 2.0)[0]))
    for s_, xy in words:
        if inP(xy) and not _r28_label(pg, [(s_, ts["small"], False, ink2)], T(xy), taken, segs, bounds, rank=1):
            missing.append(s_ + u" (no room)")
    # ---- the panel: the plan, its title (sheet only) and the north arrow and scale bar inside the crop
    M = 12.0
    W, H = M + dw + M, M + dh + 14.0
    sh = Page(W, H)
    sh.poly([rect(0, 0, W, H)], fill=COL["paper"])
    sh.clip([rect(M, M, M + dw, M + dh)])
    blit(sh, pg, M, M)
    sh.unclip()
    sh.text(w["title"] + u" · 1:1,000", M, M + dh + 5.0, 5.0, COL["ink_dark"], bold=True)
    panel_marks(sh, M, 1.5, DT_SCALE, (0.0, 10.0, 20.0, 50.0))
    sh.crop = (M, 0.5, M + dw, M + dh)
    sh.key, sh.world, sh.scale = w["key"], R, DT_SCALE
    pl = dict(_PLEG[0])
    sh.pleg, _PLEG[0] = pl, None
    sh.r28_leg = r28_crop_legend(pl)
    sh.bid = (w["id"], w["old"], w["caption"])
    return sh


def r28_crop_legend(keys):
    """v27 (P24.1 "a simple dot-and-colour legend below"): a window's booklet legend, only what it draws: a dot per
    programme field (R28_ZONES colours), the route, levels, the field details, the survey underlay, the study area."""
    cl = _r28_base_cols()
    out = [{"kind": "dot", "colour": hx, "label": lab} for key, lab, hx in R28_ZONES if ("r28z", key) in keys]
    for key, kind, colour, label in ((("r28dt", "route"), "line", R28DT_ROUTE, u"Water route · step"),
                                     (("r28dt", "level"), "dot", COL["ink_dark"], u"Level (m): bed, Q100 / Q500 flood"),
                                     (("r28dt", "terr"), "line", R28_ZONE["terraces"][1], u"Terrace edge on a contour"),
                                     (("r28dt", "canopy"), "dash", R28_ZONE["forest"][1], u"Canopied walk"),
                                     (("r28dt", "stones"), "dot", COL["ink2"], u"Stepping stones"),
                                     (("r28dt", "foot"), "line", COL["ink"], u"New footbridge"),
                                     (("r28dt", "hidden"), "dash", COL["river_mid"], u"Hidden stream line"),
                                     (("r28dt", "bed"), "fill", cl["bed"], u"Stream bed (survey)"),
                                     (("r28dt", "bld"), "fill", cl["bld"], u"Building (survey)"),
                                     (("r28dt", "study"), "dashdot", R28_STUDY_LINE["colour"], R28_STUDY_NAME)):
        if key in keys:
            out.append({"kind": kind, "colour": colour, "label": label})
    return out


def detail_legend():
    """v27 (MIRAQUA 28 Oct, P24.1; was 02b_detail.py): the detail sheet's legend groups, only what its windows draw:
    the programme fields, the water route and levels, the survey underlay and the study area (G8)."""
    cl = _r28_base_cols()
    st = R28_STUDY_LINE

    def zone_sw(hx):
        def f(pg, x, y, w, h):
            for i in range(R28DT_HALO + 1 + R28DT_INSET):
                pg.circle(x + w / 2.0, y + h / 2.0, h * 0.5 * (1.0 - 0.14 * i), fill=hx, alpha=R28DT_A)
        return f

    def line_sw(colour, lw, dash=None, alpha=None):
        def f(pg, x, y, w, h):
            pg.line([(x, y + h / 2), (x + w, y + h / 2)], colour, lw, dash, cap=0 if dash else 1, alpha=alpha)
        return f

    def route_sw(pg, x, y, w, h):
        cy = y + h / 2
        pg.line([(x + 3.8, cy), (x + w - 1.6, cy)], R28DT_ROUTE, 0.6, cap=1)
        pg.poly([[(x + w, cy), (x + w - 1.8, cy + 0.76), (x + w - 1.8, cy - 0.76)]], fill=R28DT_ROUTE)
        pg.circle(x + 1.9, cy, 1.9, fill=R28DT_ROUTE)
        pg.text(u"1", x + 1.9, cy - R28DT_TS["small"] * 0.36, R28DT_TS["small"], COL["white"], bold=True, align="C")

    def cross_sw(pg, x, y, w, h):
        cx, cy = x + w / 2, y + h / 2
        pg.line([(cx - 1.4, cy), (cx + 1.4, cy)], COL["ink_dark"], 0.3)
        pg.line([(cx, cy - 1.4), (cx, cy + 1.4)], COL["ink_dark"], 0.3)

    def stones_sw(pg, x, y, w, h):
        for i in range(5):
            pg.circle(x + w * (i + 0.5) / 5, y + h / 2, 0.8, fill=COL["ink2"], alpha=0.7)

    def none_sw(pg, x, y, w, h):
        return None
    zones = [(lab, zone_sw(hx)) for key, lab, hx in R28_ZONES if ("r28z", key) in LEG]
    water = [(nm, f) for key, nm, f in (
        (("r28dt", "route"), u"Water route · step", route_sw),
        (("r28dt", "level"), u"Level at a channel cut (m): bed, Q100, Q500", cross_sw),
        (("r28dt", "terr"), u"Terrace edge on a contour", line_sw(R28_ZONE["terraces"][1], 0.3, None, 0.8)),
        (("r28dt", "canopy"), u"Canopied walk", line_sw(R28_ZONE["forest"][1], 0.3, [1.2, 0.9], 0.9)),
        (("r28dt", "stones"), u"Stepping stones", stones_sw),
        (("r28dt", "foot"), u"New footbridge", line_sw(COL["ink"], 0.5)),
        (("r28dt", "hidden"), u"Hidden stream line", line_sw(COL["river_mid"], 1.2, [1.6, 0.9], 0.7))) if key in LEG]
    if ("dt", "vol") in LEG:                             # v22: how the rough volumes are made
        water.append((u"~ m³ = rough volume, area × depth · reed basins 0.46 m · terraces: Q100 over bed +1 m "
                      u"at the nearest cut", none_sw))   # (sentence case, as this legend's other lines)
    surv = [(nm, f) for key, nm, f in (
        (("r28dt", "bed"), u"Stream bed", _sw_fill(cl["bed"])),
        (("r28dt", "contour"), u"Contour", line_sw(COL["contour10"], 0.3)),
        (("r28dt", "bld"), u"Building", _sw_fill(cl["bld"])),
        (("r28dt", "her"), u"Heritage building", _sw_fill(cl["bld"], COL["her_edge"])),
        (("r28dt", "since"), u"Built since the survey", _sw_fill(cl["bld"], stripes=(COL["ink2"], 0.8, 0.12, 45.0))),
        (("r28dt", "street"), u"Street edge", line_sw(COL["ink2"], 0.3, None, 0.4)),
        (("r28dt", "bridge"), u"Bridge", line_sw(COL["ink"], 0.4)),
        (("r28dt", "study"), R28_STUDY_NAME, line_sw(st["colour"], st["width_mm"], list(st["dash_mm"])))) if key in LEG]
    return [(u"PROGRAMME", zones), (u"WATER · LEVELS", water), (u"SURVEY", surv)]
