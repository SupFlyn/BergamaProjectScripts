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


def _r28_base_cols():
    """The faint survey underlay's tones, mixed from the base map colours (COL, as load_palette set them)."""
    return {"bed": mix(COL["white"], COL["river"], 0.30), "bld": mix(COL["white"], COL["bld"], 0.60)}


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
