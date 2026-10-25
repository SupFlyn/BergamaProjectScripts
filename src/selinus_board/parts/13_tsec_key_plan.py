def tsec_key_plan(S, B, x, ytop, w, G, lab, U, L, d):
    """Where the line runs: buildings and water (one shared picture), the frame, and the line with its ends."""
    V, mw, mh = view_fit(S.F, x, ytop, w, w * S.F.h / S.F.w)
    B.image(tsec_keyplan_png(S, d), V.X0, ytop - mh, V.X0 + mw, ytop, L, 3)
    B.line(V.P(S.F.P + [S.F.P[0]]), T_RULE, L, 6, 0.06)
    a, b = V.p(*G["a"]), V.p(*G["b"])
    B.line([a, b], (200, 30, 30), L, 7, 0.2)
    for q, t in ((a, lab), (b, lab + "'")):
        ring = circle_pts(q[0], q[1], 0.32 * U, 16)
        B.fill([ring], (255, 255, 255), L, 8)
        B.line(ring + [ring[0]], (200, 30, 30), L, 9, 0.05)
        B.text(t, q[0], q[1], 0.26 * U, T_INK, L, order=10, font=FONT_TITLE, bold=True, align="MC")
    draw_north_small(B, V, mw, mh, U, L, size=0.45)
    return ytop - mh


TSEC_GRAPH_END = 1.25    # m: v16.4: the first and last column's value reaches the section's ends (half a column at most)
TSEC_GRAPH_GAP = 6.0     # m: v16.4: a graph line runs on across a gap in its points up to this long (columns are 1-2.5 m
#                          apart, plus one just outside every cut wall); only a longer stretch with no value breaks it


def graph_runs(pts, gap=TSEC_GRAPH_GAP):
    """v16.4: the points of a graph [(s, v) or (s, v, on_roof)] as continuous runs [(points [(s, v)], on_roof)].
    Where the line passes from the open ground onto a cut building's roof (or back), the two runs meet at the middle
    of the step between their last and first points: the value steps there, with no white gap (v16.3 left a gap at
    every wall). A run breaks only where a value is missing or the points are more than `gap` metres apart."""
    out = []
    run, rf0, prev = [], False, None
    for p_ in sorted((p for p in pts if p[0] is not None), key=lambda p: p[0]):
        s_, v_ = p_[0], p_[1]
        rf = bool(p_[2]) if len(p_) > 2 else False
        if v_ is None:
            if run:
                out.append((run, rf0))
            run, prev = [], None
            continue
        if prev is not None and s_ - prev[0] > gap:
            out.append((run, rf0))
            run = []
        elif prev is not None and rf != rf0:
            m_ = 0.5 * (prev[0] + s_)                     # the step between ground and roof, at the wall
            run.append((m_, prev[1]))
            out.append((run, rf0))
            run = [(m_, v_)]
            rf0 = rf
        if not run:
            rf0 = rf
        run.append((s_, v_))
        prev = (s_, v_)
    if run:
        out.append((run, rf0))
    return out


TSEC_TREND = 10.0        # v16.6: m, the window of the running mean drawn over the solar and shade graphs
TSEC_TREND_C = (28, 58, 108)


def graph_trend(pts, win=TSEC_TREND, step=0.25, gap=TSEC_GRAPH_GAP):
    """v16.6: the running mean of a graph's values over `win` metres of line (each point the average of the line
    `win` long centred on it, the values taken every `step` m between the points), as runs [(s, v)]; it breaks where
    the graph breaks (a stretch longer than `gap` with no value). Drawn OVER the full-detail graph, never instead of
    it: the detail stays, the mean shows the trend through the walls of a densely built stretch."""
    q = sorted((p_[0], p_[1]) for p_ in pts if p_[0] is not None and p_[1] is not None)
    if len(q) < 2:
        return []
    S_ = np.array([a for a, b in q], float)
    V_ = np.array([b for a, b in q], float)
    g = np.arange(S_[0], S_[-1] + 1e-9, step)
    v = np.interp(g, S_, V_)
    k = np.searchsorted(S_, g)
    dl = np.abs(g - S_[np.clip(k - 1, 0, S_.size - 1)])
    dr = np.abs(S_[np.clip(k, 0, S_.size - 1)] - g)
    ok = (np.minimum(dl, dr) <= 0.5 * gap) | (np.maximum(dl, dr) <= gap)
    out = []
    i = 0
    n = g.size
    h = max(1, int(round(0.5 * win / step)))
    while i < n:
        if not ok[i]:
            i += 1
            continue
        j = i
        while j + 1 < n and ok[j + 1]:
            j += 1
        vv = v[i:j + 1]
        c = np.concatenate([[0.0], np.cumsum(vv)])
        idx = np.arange(vv.size)
        a = np.clip(idx - h, 0, vv.size)
        b = np.clip(idx + h + 1, 0, vv.size)
        m = (c[b] - c[a]) / (b - a)
        out.append(list(zip(g[i:j + 1].tolist(), m.tolist())))
        i = j + 1
    return out


def tsec_graph(B, x, ytop, w, h, Lm, series, lo, hi, U, L, unit, colour=None, dec=VAL_DEC, trend=None):
    """Values along the line under a section: series = [(points [(s, v)] or [(s, v, on_roof)], colour, weight)];
    a coloured ribbon under the first series when colour is given. v16.4: one continuous line along the whole section
    (graph_runs): the roof stretches (the value at the same height above the cut building's roof, as the plan shows a
    building) are dashed over a paler ribbon with a roof mark below, and join the ground stretches at the walls."""
    X_ = lambda s_: x + w * max(0.0, min(Lm, s_)) / Lm
    Y_ = lambda v_: ytop - h + h * (max(lo, min(hi, v_)) - lo) / (hi - lo)
    B.fill([rect(x, ytop - h, x + w, ytop)], (250, 250, 251), L, 20)
    step = nice_step(hi - lo, 3)
    v = math.ceil(lo / step) * step
    f_ = tick_fmt(step, dec)                          # v16.3: decimals when the range is narrow (v16.6: at least dec)
    while v <= hi + 1e-9:
        B.line([(x, Y_(v)), (x + w, Y_(v))], (218, 218, 224), L, 21, 0.02)
        B.text((f_ % v) + unit, x - 0.2 * U, Y_(v) - 0.09 * U, 0.2 * U, T_GREY, L, align="R")
        v += step
    yb_ = ytop - h
    seam = 0.015 * U                                  # each ribbon piece reaches a hair into the next: no white seams
    for si, (pts, col, lw) in enumerate(series):
        runs_ = graph_runs(pts)
        if runs_:                                     # the end columns stand for half a column each: reach the frame
            r0, rl = runs_[0][0], runs_[-1][0]
            if 0.0 < r0[0][0] <= TSEC_GRAPH_END:
                r0.insert(0, (0.0, r0[0][1]))
            if 0.0 < Lm - rl[-1][0] <= TSEC_GRAPH_END:
                rl.append((Lm, rl[-1][1]))
        for run, roof_run in runs_:
            if len(run) == 1:                             # a single point: half a column either side
                s_, v_ = run[0]
                run = [(s_ - 0.5, v_), (s_ + 0.5, v_)]
            if si == 0 and colour is not None:            # one ribbon piece per stretch of the same colour
                k0 = 0
                c0 = colour((run[0][1] + run[1][1]) / 2.0)
                for k in range(1, len(run)):
                    ck = colour((run[k][1] + run[k + 1][1]) / 2.0) if k < len(run) - 1 else None
                    if ck != c0:
                        top_ = [(X_(a_), Y_(b_)) for a_, b_ in run[k0:k + 1]]
                        cf_ = mix(c0, (255, 255, 255), 0.45) if roof_run else c0
                        xr_ = min(x + w, top_[-1][0] + seam)
                        B.fill([[(top_[0][0], yb_), (xr_, yb_), (xr_, top_[-1][1])] + top_[::-1]], cf_, L, 22)
                        k0, c0 = k, ck
            ln_ = [(X_(a_), Y_(b_)) for a_, b_ in run]
            if roof_run:
                for dd in dashes(ln_, 0.12 * U, 0.08 * U):
                    B.line(dd, col, L, 23, lw)
                x0r, x1r = X_(run[0][0]), X_(run[-1][0])
                B.fill([[(x0r, yb_), (x1r, yb_), (x1r, yb_ + 0.1 * U), (x0r, yb_ + 0.1 * U)]], (120, 120, 128), L, 24)
            else:
                B.line(ln_, col, L, 23, lw)
        # the steps at the walls: a thin vertical joining the two values, so the line reads as one
        for (ra, fa), (rb, fb) in zip(runs_, runs_[1:]):
            if fa != fb and abs(ra[-1][0] - rb[0][0]) < 1e-6:
                xs_ = X_(ra[-1][0])
                B.line([(xs_, Y_(ra[-1][1])), (xs_, Y_(rb[0][1]))], col, L, 23, lw * 0.6)
    if trend and series:                                  # v16.6: the running mean over the detail
        for run in graph_trend(series[0][0], trend):
            if len(run) >= 2:
                B.line([(X_(a_), Y_(b_)) for a_, b_ in run], (255, 255, 255), L, 25, 0.22)
                B.line([(X_(a_), Y_(b_)) for a_, b_ in run], TSEC_TREND_C, L, 26, 0.12)
    B.line(rect(x, ytop - h, x + w, ytop) + [(x, ytop - h)], T_RULE, L, 24, 0.04)
    return ytop - h


def tsec_at(fld, i, z):
    """Value of field column i at height z (linear between its heights), or None."""
    col = fld["vals"][i]
    fk = (z - fld["zlo"]) / fld["dz"] - 0.5
    k0 = int(math.floor(fk))
    if k0 < 0 or k0 >= fld["nz"] - 1:
        return None
    a, b = col[k0], col[k0 + 1]
    if a is None or b is None:
        return a if b is None else b
    return a + (b - a) * (fk - k0)


TSEC_NAMES16 = ("N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW")


# ============================================================ TECHNICAL SECTIONS v16.2: lively base + analysis wash
# Every row of a technical section is one picture: the view beyond the cut (ground, buildings, crowns at their measured
# size and leaf state, scale figures) under the analysis as a translucent wash, the surface bands on the surfaces; the
# cut itself (ground, water, cut buildings), contours, arrows and text are drawn as vectors over it.
TSEC_WASH = 0.95            # strength of the analysis colours, multiplied over the drawing
TSEC_DPI = 450.0            # pictures are made for this print resolution at the sheet's printed size (sheet_mm; v16.6: 300 -> 450)
SA_VERSION = 3              # v16.4: building types in their own tones, jetties, minarets; trees whole


def tsec_px_res(G, ss):
    """Metres per pixel for a drawing printed at ss (page units per metre): TSEC_DPI at the printed size, kept between
    0.08 and 0.6 m and at most 9000 pixels along the line (v16.6: 5000)."""
    mm_per_m = ss * MMU
    res = 25.4 / (TSEC_DPI * max(1e-6, mm_per_m))
    res = max(0.08, min(0.6, res))
    res = max(res, G["L"] / 9000.0)                   # v16.6: up to 9000 pixels along the line (v16.5: 5000)
    return round(res, 4)


def _pool_sa_base(sc, L, zlo, zhi, res, leaf, pal, ground):
    """v18: tsec_base's drawing, on a worker (the same call; sa_render does not read the site object)."""
    art, r_ = sa_render(None, sc, 0.0, L, zlo, zhi, res, SA_STYLE_TECH, leaf=leaf, season=pal, ground=ground)
    return art.to_bytes()


TSEC_PLAN = (("sound_sections", 4, 0.0), ("heat_sections", 4, 2.0), ("shade_sections", 5, 0.0),
             ("solar_sections", 4, 2.0), ("wind_sections", 4, 0.0), ("air_sections", 4, 0.0), ("felt_sections", 4, 0.0))


def tsec_seasons(S, key):
    """The leaf states (season arguments) the rows of a section sheet draw with, as the tsec_sheet_* functions pass
    them to tsec_compose."""
    if key == "sound_sections":
        return ["year"]
    if key == "shade_sections":
        return [sd["day"] for sd in SEASONS] + ["year"]
    if key == "heat_sections":
        out = []
        for sd in SEASONS:
            when = S.env["lst"].get(sd["key"], {}).get("datetime_utc", "")
            try:
                out.append((int(when[5:7]), int(when[8:10])))
            except Exception:
                out.append(sd["key"])
        return out
    return [sd["key"] for sd in SEASONS]


def tsec_prefetch(S, U):
    """v18: the drawings behind every technical section row (one per line, picture resolution and leaf state), started
    on the worker processes before the sheets are made; tsec_base takes them from there. These are the very calls
    tsec_base makes, with the same arguments; one not asked for later is only work done in vain."""
    S.env["sa_pre"] = {}
    if not pool_live():
        return 0
    lines = tsec_lines(S)
    ST = S.store
    todo = {}
    for key, nrows, gh in TSEC_PLAN:
        if key in ("wind_sections", "air_sections", "felt_sections") and not S.env.get("comfort"):
            continue
        for k, a, b in lines.get(key, []):
            G = tsec_geom(S, a, b)
            lay = tsec_layout(S, G, U, nrows, graph_h=gh * U) if gh else tsec_layout(S, G, U, nrows)
            res = tsec_px_res(G, lay["ss"])
            for season in tsec_seasons(S, key):
                leaf, tag, pal = tsec_season_tag(season)
                fk = fp("sa_base", SA_VERSION, G["key"], round(res, 4), round(leaf, 3), pal)
                if fk in todo or (ST is not None and ST.has("sa_base", fk)):
                    continue
                todo[fk] = (sa_scene(S, G["a"], G["b"]), G["L"], G["zlo"], G["zhi"], res, leaf, pal, G["ground"])
    if todo:
        job = pool_submit("_pool_sa_base", list(todo.values()), prio=8, label="section drawings")
        pre = S.env.setdefault("sa_pre", {})
        for i, fk in enumerate(todo):
            pre[fk] = (job, i)
    return len(todo)


def tsec_base(S, G, res, season):
    """The drawing behind the cut of one line for one leaf state (shared by every row and analysis using it)."""
    leaf, tag, pal = tsec_season_tag(season)
    key = fp("sa_base", SA_VERSION, G["key"], round(res, 4), round(leaf, 3), pal)
    ST = S.store
    v = ST.get("sa_base", key) if ST is not None else None
    if v is not None:
        return v
    pre = (S.env.get("sa_pre") or {}).pop(key, None)
    if pre is not None:                                  # v18: made on the worker processes (tsec_prefetch)
        v = pool_result(pre[0])[pre[1]]
    else:
        sc = sa_scene(S, G["a"], G["b"])
        art, r_ = sa_render(S, sc, 0.0, G["L"], G["zlo"], G["zhi"], res, SA_STYLE_TECH, leaf=leaf, season=pal,
                            ground=G["ground"])
        v = art.to_bytes()
    if ST is not None:
        ST.put("sa_base", key, v)
    return v


def tsec_tree_layer(S, G, res, season):
    """v16.4: the trees standing on the line, whole, as a layer (v16.6: laid UNDER the analysis colours; v16.4-v16.5 over them): the line does not cut
    them (v16.3 outlined the cut crowns with a dashed box and washed them with the field). Each tree is the same
    picture as in the base drawing (its measured height and crown, leaf type, leaf state of the row's season).
    Returns (colour premultiplied (h, w, 3) uint8, alpha (h, w) uint8) or None."""
    if not G.get("crowns"):
        return None
    leaf, tag, pal = tsec_season_tag(season)
    key = fp("sa_trees", SA_VERSION, G["key"], round(res, 4), round(leaf, 3), pal)
    ST = S.store
    v = ST.get("sa_trees", key) if ST is not None else None
    if v is not None:
        return v
    W = int(math.ceil(G["L"] / res))
    H = int(math.ceil((G["zhi"] - G["zlo"]) / res))
    Lc = np.zeros((H, W, 3), np.float32)
    La = np.zeros((H, W), np.float32)
    trees = S.env["solids"][2]
    zhi = G["zhi"]
    for sc_, hw, z0, z1, kind, ti in G["crowns"]:
        t = trees[ti]
        zg = S.z_at(t["x"], t["y"])
        sp = sa_tree(kind, sc_ / res, (zhi - zg) / res, (zhi - (zg + t["lo"])) / res, (zhi - (zg + t["hi"])) / res,
                     t["r"] / res, int(abs(t["x"] * 7.31 + t["y"] * 3.17) * 10) % 2147483647,
                     leaf=leaf if kind == "tree" else 1.0, season=pal)
        if sp is None:
            continue
        xa, ya = max(0, sp.x0), max(0, sp.y0)
        xb, yb = min(W, sp.x0 + sp.w), min(H, sp.y0 + sp.h)
        if xb <= xa or yb <= ya:
            continue
        c = sp.c[ya - sp.y0:yb - sp.y0, xa - sp.x0:xb - sp.x0] * 0.92
        a = sp.a[ya - sp.y0:yb - sp.y0, xa - sp.x0:xb - sp.x0] * 0.92
        Lc[ya:yb, xa:xb] = Lc[ya:yb, xa:xb] * (1.0 - a)[..., None] + c
        La[ya:yb, xa:xb] = La[ya:yb, xa:xb] * (1.0 - a) + a
    v = ((np.clip(Lc, 0, 1) * 255 + 0.5).astype(np.uint8), (np.clip(La, 0, 1) * 255 + 0.5).astype(np.uint8))
    if ST is not None:
        ST.put("sa_trees", key, v)
    return v


def _tsec_grid(fld, cut=None):
    """The field as an array (columns x heights, NaN where not computed) with every column's lowest value carried down
    to the ground; empty columns (not computed at all) are flagged. v16.6: with cut (G["cut"]) a column standing in a
    cut building is not carried down below its roof: the colours at a wall's foot come from the open side alone
    (v16.5 blended them with the roof's value across the wall, which drew dark or pale wedges at the feet of walls)."""
    cols = fld["vals"]
    V = np.array([[np.nan if v is None else v for v in col] for col in cols], float)
    empty = np.all(~np.isfinite(V), axis=1)
    F_ = V.copy()
    inb = np.zeros(F_.shape[0], bool)
    if cut:
        cs = np.asarray(fld["s"], float)
        for c in cut:
            inb |= (cs > c[0]) & (cs < c[1])
    for j in range(F_.shape[0]):
        if inb[j]:
            continue
        row = F_[j]
        ok = np.isfinite(row)
        if ok.any():
            k0 = int(np.argmax(ok))
            row[:k0] = row[k0]
    return V, F_, empty


def _tsec_sample(fld, F_, s_px, z_px):
    """Bilinear values of the field at pixel centres (s along the line, z height); a missing neighbour is left out."""
    cs = np.asarray(fld["s"], float)
    nc = cs.size
    j = np.searchsorted(cs, s_px)
    j0 = np.clip(j - 1, 0, nc - 1)
    j1 = np.clip(j, 0, nc - 1)
    den = np.where(j1 > j0, cs[j1] - cs[j0], 1.0)
    t = np.where(j1 > j0, np.clip((s_px - cs[j0]) / den, 0.0, 1.0), 0.0)
    fk = (z_px - fld["zlo"]) / fld["dz"] - 0.5
    k0 = np.floor(fk).astype(np.int64)
    w = fk - k0
    nz = fld["nz"]
    k0c = np.clip(k0, 0, nz - 1)
    k1c = np.clip(k0 + 1, 0, nz - 1)
    w = np.where(k0 < 0, 0.0, np.where(k0 >= nz - 1, 1.0, w))
    out = np.zeros((z_px.size, s_px.size))
    wsum = np.zeros_like(out)
    for jj, wj in ((j0, 1.0 - t), (j1, t)):
        for kk, wk in ((k0c, 1.0 - w), (k1c, w)):
            v = F_[jj[None, :], kk[:, None]]
            ww = wj[None, :] * wk[:, None]
            ok = np.isfinite(v) & (ww > 0)
            out += np.where(ok, v * ww, 0.0)
            wsum += np.where(ok, ww, 0.0)
    return np.where(wsum > 1e-9, out / np.maximum(wsum, 1e-9), np.nan)


def _lut_apply(colour, V):
    """Colours (0..1) of values through a colour table made by lut_ramp, lut_classes or stops_table."""
    lut = colour._lut
    if lut[0] == "ramp":
        _, vmin, span, n, table = lut
        q = np.clip((np.nan_to_num((V - vmin) / span, nan=0.0, posinf=1.0, neginf=0.0) * (n - 1)).astype(np.int64), 0, n - 1)
        tab = np.asarray(table, float) / 255.0
    else:
        _, edges, cols = lut
        q = np.clip(np.searchsorted(np.asarray(edges, float), V, side="right"), 0, len(cols) - 1)
        tab = np.asarray(cols, float) / 255.0
    return tab[np.where(np.isfinite(V), q, 0)]


def _ground_np(G, s_px):
    gs = np.array([p[0] for p in G["ground"]], float)
    gz = np.array([p[1] for p in G["ground"]], float)
    return np.interp(s_px, gs, gz)


def tsec_compose(path, S, G, res, season, fld=None, colour=None, bands=None, rkey=None):
    """One row's picture: the base drawing, the field as a wash over the air (hatched where it was not computed), the
    surface bands. Kept when nothing it is made from changed. Returns (path, width m, height m)."""
    W = int(math.ceil(G["L"] / res))
    H = int(math.ceil((G["zhi"] - G["zlo"]) / res))
    out = (path, W * res, H * res)
    full = None
    if rkey is not None:
        full = fp("tsec_row", SA_VERSION, "trees under, v16.6", MV["render"], MV["sec_field"], rkey, colour._lut if colour else None, res, W, H,
                  G["key"], repr(season), bands_key(bands) if bands else None, TSEC_WASH)
        d_ = os.path.dirname(path)
        e_ = maps_index(S, d_).get(os.path.basename(path))
        try:
            if e_ and e_.get("key") == full and os.path.getsize(path) == e_.get("size"):
                S.env.setdefault("maps_kept", []).append(os.path.basename(path))
                return out
        except Exception:
            pass
    base = tsec_base(S, G, res, season)
    img = base.astype(np.float32) / 255.0
    H_, W_ = img.shape[:2]
    tl = tsec_tree_layer(S, G, res, season)               # v16.6: the trees on the line, whole, UNDER the colours
    if tl is not None:                                    # (v16.4-v16.5 laid them over the analysis)
        Lc, La = tl
        hh, ww = min(H_, La.shape[0]), min(W_, La.shape[1])
        a_ = La[:hh, :ww].astype(np.float32)[..., None] / 255.0
        img[:hh, :ww] = img[:hh, :ww] * (1.0 - a_) + Lc[:hh, :ww].astype(np.float32) / 255.0
    s_px = (np.arange(W_) + 0.5) * res
    z_px = G["zhi"] - (np.arange(H_) + 0.5) * res
    if fld is not None and colour is not None:
        V, F_, empty = _tsec_grid(fld, G["cut"])
        val = _tsec_sample(fld, F_, s_px, z_px)
        gz = _ground_np(G, s_px)
        air = z_px[:, None] > gz[None, :] - 0.3
        col = _lut_apply(colour, val).astype(np.float32)
        m = (air & np.isfinite(val)).astype(np.float32)[..., None] * TSEC_WASH
        img = img * (1.0 - m + m * col)                  # multiply: the drawing stays legible under the colours
        # not computed: a light hatch over the drawing
        cs = np.asarray(fld["s"], float)
        if empty.any():
            jj = np.clip(np.searchsorted(cs, s_px) - 1, 0, cs.size - 1)
            jn = np.clip(jj + 1, 0, cs.size - 1)
            nod = empty[jj] & empty[jn]
            if nod.any():
                yy, xx = np.mgrid[0:H_, 0:W_]
                hatch = ((xx + yy) % 9 < 1.2) & nod[None, :] & air
                img[hatch] = img[hatch] * 0.55 + np.float32(0.55) * 0.45
    if bands:
        tb_cols = None
        for s0, s1, z0, z1, v in bands:
            if v is None:
                continue
            c = np.asarray(_lut_apply(colour, np.array([v], float))[0], np.float32)
            a0, a1 = max(0, int(round(s0 / res))), min(W_, int(round(s1 / res)))
            p0, p1 = max(0, int(round((G["zhi"] - z1) / res))), min(H_, int(round((G["zhi"] - z0) / res)))
            if a1 <= a0:
                a1 = min(W_, a0 + 1)
            if p1 <= p0:
                p1 = min(H_, p0 + 1)
            img[p0:p1, a0:a1] = c
    png_write_np(path, (np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8))
    if full is not None:
        try:
            d_ = os.path.dirname(path)
            maps_index(S, d_)[os.path.basename(path)] = dict(key=full, size=os.path.getsize(path), w=W_, h=H_)
            maps_index_save(S, d_)
        except Exception:
            pass
    return (path, W_ * res, H_ * res)


def png_write_np(path, a):
    """An (h, w, 3) uint8 array to PNG, each row filtered with Paeth (smaller files for drawings with soft colours)."""
    h, w = a.shape[:2]
    x = a.reshape(h, w * 3).astype(np.int16)
    left = np.zeros_like(x)
    left[:, 3:] = x[:, :-3]
    up = np.zeros_like(x)
    up[1:] = x[:-1]
    ul = np.zeros_like(x)
    ul[1:, 3:] = x[:-1, :-3]
    p = left + up - ul
    pa, pb, pc = np.abs(p - left), np.abs(p - up), np.abs(p - ul)
    pred = np.where((pa <= pb) & (pa <= pc), left, np.where(pb <= pc, up, ul))
    f = ((x - pred) & 0xFF).astype(np.uint8)
    raw = np.concatenate([np.full((h, 1), 4, np.uint8), f], 1).tobytes()

    def chunk(t, d):
        return _struct.pack(">I", len(d)) + t + d + _struct.pack(">I", _zlib.crc32(t + d) & 0xffffffff)
    with open(path, "wb") as fo:
        fo.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", _struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                 + chunk(b"IDAT", _zlib.compress(raw, 6)) + chunk(b"IEND", b""))


def tsec_season_tag(season):
    """Leaf share of deciduous crowns and the foliage palette for a row: a season key or a (month, day)."""
    if isinstance(season, tuple):
        m = season[0]
        pal = "spring" if m in (3, 4, 5) else ("autumn" if m in (9, 10, 11) else "")
        return sa_leaf_day(*season), "d%02d%02d" % season, pal
    return sa_leaf(season), str(season), (season if season in ("spring", "autumn") else "")


# ------------------------------------------------------------ contours of a field in the plane of a section
def sa_contours(fld, levels):
    """Polylines [(level, [(s, z), ...])] of the field at each level (marching squares on the computed points only)."""
    V, F_, empty = _tsec_grid(fld)
    cs = np.asarray(fld["s"], float)
    zs = fld["zlo"] + (np.arange(fld["nz"]) + 0.5) * fld["dz"]
    if V.shape[0] < 2 or V.shape[1] < 2:
        return []
    a, b, c, d = V[:-1, :-1], V[1:, :-1], V[1:, 1:], V[:-1, 1:]
    ok = np.isfinite(a) & np.isfinite(b) & np.isfinite(c) & np.isfinite(d)
    out = []
    for lev in levels:
        A, Bb, C, D = a > lev, b > lev, c > lev, d > lev
        case = (A * 1 + Bb * 2 + C * 4 + D * 8) * ok
        J, K = np.nonzero((case > 0) & (case < 15))
        if J.size == 0:
            continue
        segs = []

        def pt(edge, j, k):
            if edge == 0:            # bottom: (j, k) - (j + 1, k)
                v0, v1 = V[j, k], V[j + 1, k]
                t = (lev - v0) / (v1 - v0) if v1 != v0 else 0.5
                return ("h", j, k), (cs[j] + t * (cs[j + 1] - cs[j]), zs[k])
            if edge == 1:            # right: (j + 1, k) - (j + 1, k + 1)
                v0, v1 = V[j + 1, k], V[j + 1, k + 1]
                t = (lev - v0) / (v1 - v0) if v1 != v0 else 0.5
                return ("v", j + 1, k), (cs[j + 1], zs[k] + t * (zs[k + 1] - zs[k]))
            if edge == 2:            # top: (j, k + 1) - (j + 1, k + 1)
                v0, v1 = V[j, k + 1], V[j + 1, k + 1]
                t = (lev - v0) / (v1 - v0) if v1 != v0 else 0.5
                return ("h", j, k + 1), (cs[j] + t * (cs[j + 1] - cs[j]), zs[k + 1])
            v0, v1 = V[j, k], V[j, k + 1]                        # left
            t = (lev - v0) / (v1 - v0) if v1 != v0 else 0.5
            return ("v", j, k), (cs[j], zs[k] + t * (zs[k + 1] - zs[k]))
        TABLE = {1: ((3, 0),), 2: ((0, 1),), 3: ((3, 1),), 4: ((1, 2),), 6: ((0, 2),), 7: ((3, 2),), 8: ((2, 3),),
                 9: ((0, 2),), 11: ((1, 2),), 12: ((1, 3),), 13: ((0, 1),), 14: ((3, 0),)}
        for j, k in zip(J.tolist(), K.tolist()):
            cse = int(case[j, k])
            if cse in (5, 10):                                    # saddle: decided by the cell's mean
                mid = (V[j, k] + V[j + 1, k] + V[j + 1, k + 1] + V[j, k + 1]) / 4.0 > lev
                if cse == 5:
                    pairs = ((0, 1), (3, 2)) if mid else ((3, 0), (1, 2))
                else:
                    pairs = ((3, 0), (1, 2)) if mid else ((0, 1), (2, 3))
            else:
                pairs = TABLE[cse]
            for e0, e1 in pairs:
                segs.append((pt(e0, j, k), pt(e1, j, k)))
        # chain the segments through their shared edges
        adj = {}
        for i_, ((k0, p0), (k1, p1)) in enumerate(segs):
            adj.setdefault(k0, []).append(i_)
            adj.setdefault(k1, []).append(i_)
        used = [False] * len(segs)
        for i_ in range(len(segs)):
            if used[i_]:
                continue
            used[i_] = True
            (k0, p0), (k1, p1) = segs[i_]
            line = [p0, p1]
            for end in (1, 0):
                key = k1 if end == 1 else k0
                while True:
                    nxt = [q for q in adj.get(key, []) if not used[q]]
                    if not nxt:
                        break
                    q = nxt[0]
                    used[q] = True
                    (qa, pa), (qb, pb) = segs[q]
                    if qa == key:
                        key, p = qb, pb
                    else:
                        key, p = qa, pa
                    if end == 1:
                        line.append(p)
                    else:
                        line.insert(0, p)
            if len(line) >= 3:
                out.append((lev, line))
    return out


def _pl_len(P):
    return sum(math.hypot(P[i + 1][0] - P[i][0], P[i + 1][1] - P[i][1]) for i in range(len(P) - 1))


# ------------------------------------------------------------ the cut over the picture
TSEC_SOIL = (232, 228, 221)
TSEC_ROAD = (207, 204, 197)    # v16.7: = ROAD_FILL (v16.6: 204, 202, 198): the street surface band under the ground line of the technical sections
TSEC_WATER_LINE = (64, 120, 168)
TSEC_CONTOUR = (78, 78, 86)


def tsec_streets(S, G, step=0.25):
    """v16.6: the stretches of the line on a surveyed street surface (S.road_net, the same areas the plans hatch):
    [(s0, s1)], tested every `step` along the line. Kept per line and bake."""
    memo = env_memo(S)
    mk = ("tsec_streets", G["key"], step)
    r = memo.get(mk)
    if r is not None:
        return r
    net = getattr(S, "road_net", None) or []
    (x0, y0), ux, uy, Lm = G["a"], G["ux"], G["uy"], G["L"]
    n = int(Lm / step) + 1
    ss_ = [min(Lm, k * step) for k in range(n)]
    xs = [x0 + ux * s_ for s_ in ss_]
    ys = [y0 + uy * s_ for s_ in ss_]
    lb = (min(xs), min(ys), max(xs), max(ys))
    on = [False] * n
    for rg_ in net:
        P = rg_["P"]
        bx0, by0 = min(p[0] for p in P), min(p[1] for p in P)
        bx1, by1 = max(p[0] for p in P), max(p[1] for p in P)
        if bx1 < lb[0] or bx0 > lb[2] or by1 < lb[1] or by0 > lb[3]:
            continue
        for k in range(n):
            if on[k]:
                continue
            x_, y_ = xs[k], ys[k]
            if bx0 <= x_ <= bx1 and by0 <= y_ <= by1 and pip(x_, y_, P) and not any(pip(x_, y_, H) for H in rg_["H"]):
                on[k] = True
    out = []
    k = 0
    while k < n:
        if on[k]:
            j = k
            while j + 1 < n and on[j + 1]:
                j += 1
            out.append((max(0.0, ss_[k] - 0.5 * step), min(Lm, ss_[j] + 0.5 * step)))
            k = j + 1
        else:
            k += 1
    memo[mk] = out
    return out


def tsec_draw(S, B, G, x, ytop, ss, U, L, num, png=None, contours=None, fmt="{:g}"):
    """The cut over the row's picture: soil under the ground, the water at the bed, the cut buildings (white, a line at
    every storey), the ground line (broken inside the cut buildings), contours with their values, heights and distances.
    Returns the bottom y of the drawing."""
    zhi, zlo, Lm = G["zhi"], G["zlo"], G["L"]

    def P(s, z):
        return (x + s * ss, ytop - (zhi - z) * ss)
    ybot = P(0.0, zlo)[1]
    if png:
        B.image(png[0], x, ytop - png[2] * ss, x + png[1] * ss, ytop, L, 5)
    gp = [P(s, z) for s, z in G["ground"]]
    B.fill([gp + [P(Lm, zlo), P(0.0, zlo)]], TSEC_SOIL, L, 20)
    for a_, b_ in tsec_streets(S, G):                     # v16.6: the streets cut by the line, hatched as on the plans
        pts = [(a_, tsec_zg(G, a_))] + [(s, z) for s, z in G["ground"] if a_ < s < b_] + [(b_, tsec_zg(G, b_))]
        dd_ = max(SEC_ROAD_D, 0.2 * U / ss)               # a drawing convention, not a surveyed thickness
        band_ = [P(s, z) for s, z in pts] + [P(s, z - dd_) for s, z in reversed(pts)]
        B.fill([band_], TSEC_ROAD, L, 20)
        if not ROAD_SOLID:                                # v16.7: solid by default
            B.hatch([band_], mix(T_INK, TSEC_ROAD, 0.45), L, 21, SEC_ROAD_HATCH * U, w=0.03)
    for s0, s1, bed, lvl in G["water"]:
        # v16.5: the water hatched in blue at its depth, the channel above it in a pale wash, over the analysis
        draw_stream(B, L, P, G["ground"], s0, s1, bed, lvl, U, (226, 236, 244), (206, 224, 238), TSEC_WATER_LINE,
                    TSEC_WATER_LINE, 21, lw=0.03)
    bl = (S.env.get("solids") or ([], None, []))[0]
    spans = []
    tags_ = []
    for c in G["cut"]:
        s0, s1, base, top, bi = c[:5]
        zb = min([base] + [z for s, z in G["ground"] if s0 - 0.5 <= s <= s1 + 0.5])
        u = bl[bi]["u"] if isinstance(bi, int) and 0 <= bi < len(bl) else {}
        fl = int(u.get("floors") or 0)
        # v16.3: the generic silhouette of the building's type, faintly tinted by its use, over the white of the cut
        fab, cat_ = c[5], c[6]
        uf_ = unit_flags(u) if u else (False, False, False)
        ms_ = minaret_s(u, G["a"][0], G["a"][1], G["ux"], G["uy"], s0, s1) if (u and fab == "sacred") else None
        prof = bld_profile(fab, cat_, s0, s1, zb, base, top, fl or 1, u.get("floors_src") == "published",
                           seed=int(s0 * 7.0), ruin=uf_[2], minaret=ms_)
        tint = mix(typo_tone(fab, cat_), (255, 255, 255), 0.35)      # v16.4: the tone of its type
        lab_ = None
        tag_ = typo_label(fab, cat_, fl or 1, uf_[0], label_name(live_unit(S, u)))
        if not c[7] and (s1 - s0) * ss > 0.6 * tw(tag_, 0.17 * U):
            lab_ = tag_
        bld_draw_cut(B, L, P, prof, tint, T_INK, ss, U, order=22, roof_c=None, label=lab_, placed=tags_)
        spans.append((s0, s1))
    spans.sort()
    run = []

    def flush():
        if len(run) >= 2:
            B.line(list(run), T_INK, L, 26, 0.2)
        del run[:]
    prev_in = False
    for s, z in G["ground"]:
        sp_ = next(((a_, b_) for a_, b_ in spans if a_ < s < b_), None)
        if sp_ is not None:
            if not prev_in:
                run.append(P(sp_[0], tsec_zg(G, sp_[0])))
                flush()
            prev_in = True
            continue
        if prev_in:
            sp0 = max((b_ for a_, b_ in spans if b_ <= s), default=None)
            if sp0 is not None:
                run.append(P(sp0, tsec_zg(G, sp0)))
        prev_in = False
        run.append(P(s, z))
    flush()
    # v16.4: the trees on the line are not cut: they stand whole in the row's picture, over the analysis colours
    # (tsec_tree_layer); v16.3 outlined each cut crown with a dashed box here
    rl_ = draw_sec_roads(S, B, L, P, lambda s_: tsec_zg(G, s_), (G["a"][0], G["a"][1], G["b"][0], G["b"][1]), Lm, U,
                         order=28, w=0.4)                 # v25: the streets crossed, named over the ground
    placed_r = []
    for sm, zg_, txt in rl_:
        q = P(sm, zg_)
        half = 0.5 * tw(txt, 0.17 * U) + 0.1 * U
        tier = 0
        while any(t2 == tier and q[0] - half < r2 and l2 < q[0] + half for l2, r2, t2 in placed_r):
            tier += 1
        placed_r.append((q[0] - half, q[0] + half, tier))
        ty = q[1] + (0.55 + 0.32 * tier) * U
        B.line([(q[0], q[1] + 0.05 * U), (q[0], ty - 0.04 * U)], T_INK, L, 28, 0.03)
        B.fill([rect(q[0] - half, ty - 0.03 * U, q[0] + half, ty + 0.22 * U)], (255, 255, 255), L, 28)
        B.text(txt, q[0], ty, 0.17 * U, T_INK, L, order=29, align="C")
    if contours:
        placed = []
        for lev, line in contours:
            pts = [P(s, z) for s, z in line]
            B.line(pts, TSEC_CONTOUR, L, 24, 0.03)
            if _pl_len(line) * ss > 6.0 * U:
                k = len(pts) // 2
                px, py = pts[k]
                if all(math.hypot(px - qx, py - qy) > 3.0 * U for qx, qy in placed):
                    placed.append((px, py))
                    B.text(fmt.format(lev), px, py + 0.06 * U, 0.17 * U, (60, 60, 66), L, order=25, align="C")
    # heights on the left, distances below, the ends of the line
    step = nice_step(zhi - zlo, 4)
    zt = math.ceil(zlo / step) * step
    while zt <= zhi + 1e-9:
        q = P(0.0, zt)
        B.line([(q[0] - 0.18 * U, q[1]), (q[0] - 0.05 * U, q[1])], T_GREY, L, 29, 0.04)
        B.text("+%.0f" % zt, q[0] - 0.25 * U, q[1] - 0.09 * U, 0.2 * U, T_GREY, L, align="R")
        zt += step
    step = nice_step(Lm, 8)
    st = 0.0
    while st <= Lm + 1e-9:
        q = P(st, zlo)
        B.line([q, (q[0], q[1] - 0.15 * U)], T_GREY, L, 29, 0.04)
        B.text("%.0f" % st, q[0], q[1] - 0.48 * U, 0.2 * U, T_GREY, L, align="C")
        st += step
    for s_, lab in ((0.0, num), (Lm, num + "'")):
        q = P(s_, tsec_zg(G, s_))
        B.text(lab, q[0], q[1] + 0.55 * U, 0.34 * U, T_INK, L, font=FONT_TITLE, bold=True, align="C")
    return ybot - 0.62 * U


# ------------------------------------------------------------ the sheet: rows in one or two columns, legends under them
TSEC_ROW_TOP = 1.0       # page units above a drawing: the row's title line
TSEC_ROW_AXIS = 1.1      # under a drawing: its distances
TSEC_LEG_H = 3.2         # the legend under a row (one column: legend and note side by side; v16.3: 2.6 -> 3.2 for
                         # the shared scale drawn above a stretched bar)
TSEC_HTICK = 2.4         # left of a drawing: its heights


def tsec_layout(S, G, U, nrows, graph_h=0.0):
    """One or two columns of rows, whichever draws the line larger (one column unless two are clearly larger)."""
    W = (PW - 2 * PM) * U
    avail = (PH - 6.4 - 5.0 - 1.3) * U
    Hz = G["zhi"] - G["zlo"]
    cand = []
    for cols in (1, 2):
        rpc = (nrows + cols - 1) // cols
        cw = (W - (cols - 1) * 3.0 * U) / cols
        leg = (TSEC_LEG_H if cols == 1 else TSEC_LEG_H + 1.5) * U
        rowh = avail / rpc
        dh = rowh - (TSEC_ROW_TOP + TSEC_ROW_AXIS + 0.55) * U - leg - graph_h
        ss = min((cw - TSEC_HTICK * U) / G["L"], max(0.2 * U, dh) / Hz)
        cand.append(dict(ss=ss, cols=cols, rpc=rpc, cw=cw, rowh=rowh, leg=leg, graph_h=graph_h))
    one, two = cand
    # two columns when they draw the line clearly larger, or when one column would leave more than a third of the
    # sheet's width empty and two draw it nearly as large
    fill = (G["L"] * one["ss"] + TSEC_HTICK * U) / W
    best = two if nrows > 1 and (two["ss"] > one["ss"] * 1.12 or (fill < 0.66 and two["ss"] >= 0.9 * one["ss"])) else one
    # height a row has left once its drawing is as wide as it can be: a graph of the pedestrian level uses it
    left = best["rowh"] - (TSEC_ROW_TOP + TSEC_ROW_AXIS + 0.55) * U - best["leg"] - best["graph_h"] - Hz * best["ss"]
    if left > 1.9 * U:                                # ... no taller than the drawing above it (the drawing leads)
        best["graph_h"] += max(0.0, min(4.5 * U, left - 0.4 * U,
                                        max(2.4 * U, 1.1 * Hz * best["ss"]) - best["graph_h"]))
    return best


def tsec_profile_graph(B, G, U, L, pts, lo, hi, unit, colour, caption, dec=VAL_DEC, trend=None):
    """A row's graph: the value along the line at one height above the ground, as a coloured ribbon."""
    q = nice_step(hi - lo, 14)

    def colour_q(v):                                  # one colour per legend step: fewer, calmer ribbon pieces
        return colour(round(v / q) * q)

    def graph(x, ytop, w, h):
        if h < 1.2 * U or not any(p_[1] is not None for p_ in pts):
            return
        tsec_graph(B, x, ytop, w, h, G["L"], [(pts, T_INK, 0.06)], lo, hi, U, L, unit, colour=colour_q, dec=dec,
                   trend=trend)
        cap = caption
        if trend:
            cap += " · blue line: the mean over {:g} m of line".format(trend)
        if any(len(p_) > 2 and p_[2] for p_ in pts):    # v38: keywords (was a clause)
            cap += " · dashed on grey: same height above the cut roof"
        B.text(cap, x + w - 0.15 * U, ytop - 0.32 * U, 0.2 * U, T_GREY, L, align="R")
    return graph


def tsec_sheet(S, B, X, Y, U, rects, num, title, subtitle, sources, G, lab, rows, lay):
    """One sheet of a technical section: its rows (the periods) at one true scale, each with its title, the drawing,
    its legend and a note; key plan in the header."""
    L = "LU_TECH::Sections"
    B.begin("TECHNICAL %s · %s" % (num, title), "LU_TECH")
    ref_scale = ""
    if isinstance(sources, (list, tuple)):             # v38: the scale note joins the sheet's numbered key
        sources = list(sources) + ["True scale: heights in m above sea level; {} = start of the line, {}' = end (key "
                                   "plan, top right); trees at their modelled size and leaf state, figures for "
                                   "scale.".format(lab, lab)]
        ref_scale = " [{}]".format(len(sources))
    top, bottom = tech_frame(S, B, X, Y, U, num, title, subtitle, sources)
    x0, W = X + PM * U, (PW - 2 * PM) * U
    kpw = min(18.0 * U, 4.0 * U * S.F.w / S.F.h)
    tsec_key_plan(S, B, x0 + W - kpw, Y - 1.6 * U, kpw, G, lab, U, L, S.env["tech_dir"])
    ss = lay["ss"]
    dwm = G["L"] * ss
    for i, row in enumerate(rows):
        c, r = i % lay["cols"], i // lay["cols"]              # left to right, then down
        cx = x0 + c * (lay["cw"] + 3.0 * U)
        y = top - r * lay["rowh"]
        dx = cx + TSEC_HTICK * U
        hd = row["head"]
        h1 = 0.4 * U
        need = tw(hd, h1, kind_of(FONT_TITLE))
        B.fit(hd, cx, y, h1, lay["cw"], T_INK, L, font=FONT_TITLE, bold=True)
        if row.get("sub") and need + 1.0 * U < lay["cw"] - 4.0 * U:
            B.fit(row["sub"], cx + need + 0.8 * U, y, 0.22 * U, lay["cw"] - need - 0.8 * U, T_GREY, L)
        ytop = y - TSEC_ROW_TOP * U
        yb = tsec_draw(S, B, G, dx, ytop, ss, U, L, lab, row.get("png"), contours=row.get("contours"),
                       fmt=row.get("cfmt", "{:g}"))
        if row.get("over"):
            row["over"](dx, ytop, ss)
        yy = yb - 0.1 * U
        if lay["graph_h"] > 0.0 and row.get("graph"):
            row["graph"](dx, yy, dwm, lay["graph_h"] - 0.45 * U)
            yy -= lay["graph_h"]
        if row.get("legend"):
            yy -= 0.4 * U
            if lay["cols"] == 1:
                lw = min(40.0 * U, max(26.0 * U, 0.45 * dwm))
                ly = row["legend"](dx, yy - 0.15 * U, lw)
                if row.get("note"):
                    nx_ = dx + lw + 2.0 * U
                    if isinstance(row["note"], list):     # v38: the row's readings as tiles beside its legend
                        vis_tiles(B, nx_, yy - 0.3 * U, min(x0 + W - nx_, 12.0 * U * len(row["note"])), row["note"], U,
                                  L, h=max(0.5, min(1.0, (lay["leg"] - 0.3 * U) / (1.9 * U))))
                    else:
                        B.para_fit(row["note"] + ".", nx_, yy - 0.3 * U, x0 + W - nx_, 0.25 * U, yy - lay["leg"], T_INK, L)
            else:
                lw = lay["cw"] - TSEC_HTICK * U
                ly = row["legend"](dx, yy - 0.15 * U, lw)
                if row.get("note"):
                    if isinstance(row["note"], list):     # v38: the row's readings as tiles under its legend
                        vis_tiles(B, dx, ly - 0.08 * U, lw, row["note"], U, L,
                                  h=max(0.5, min(1.0, (ly - 0.08 * U - (yy - lay["leg"])) / (1.9 * U))))
                    else:
                        B.para_fit(row["note"] + ".", dx, ly - 0.08 * U, lw, 0.23 * U, yy - lay["leg"], T_INK, L)
    sb = nice_floor(G["L"] / 5.0)
    draw_scalebar(B, x0 + W - sb * ss - 1.2 * U, bottom + 0.05 * U, ss, sb, U, L, h=0.26)
    B.fit("TRUE SCALE · m a.s.l. · {0} start, {0}' end (key plan){1}".format(lab, ref_scale), x0, bottom + 0.15 * U,
          0.24 * U, W * 0.7, T_GREY, L)                   # v38: keywords; the sentence is in the key
    rects.append(("%s · %s" % (num, title), (X, Y - PH * U, X + PW * U, Y)))


TSEC_SLOT = 2.0          # m: a slot narrower than this between two cut buildings is bridged by the roof line (v16.3)


def tsec_at_height_all(fld, cols, h, cut=None):
    """Per column: (s, value, on_roof). Outside the cut buildings the value h metres above the ground or water; over a
    cut building the value h metres above its roof (the plan shows a building by its roof), flagged True (v16.3: the
    graph under a section no longer breaks where the line crosses a house). With cut (G["cut"]), the columns in a slot
    narrower than TSEC_SLOT between two cut buildings (party-wall gaps, light wells, which the plan's grid does not
    resolve) are left out, so the roof line runs across instead of spiking to the bottom of the slot."""
    slots = []
    if cut:
        sp = sorted((c[0], c[1]) for c in cut)
        slots = [(a[1], b[0]) for a, b in zip(sp, sp[1:]) if 0.0 < b[0] - a[1] < TSEC_SLOT]
    out = []
    for i, c in enumerate(cols):
        if c[5] is not None:
            out.append((c[0], tsec_at(fld, i, c[5] + h), True))
        elif not any(e_ <= c[0] <= b_ for e_, b_ in slots):
            out.append((c[0], tsec_at(fld, i, c[4] + h), False))
    return out


def tsec_at_height(fld, cols, h):
    """Per column outside the cut buildings: (s, value h metres above the ground or water)."""
    out = []
    for i, c in enumerate(cols):
        if c[5] is not None:
            continue
        out.append((c[0], tsec_at(fld, i, c[4] + h)))
    return out


def tsec_facades(fld, cols):
    """Values in front of the cut facades, from the ground up to the roof."""
    out = []
    for i, c in enumerate(cols):
        if c[6] is None:
            continue
        for kz, v in enumerate(fld["vals"][i]):
            z = fld["zlo"] + (kz + 0.5) * fld["dz"]
            if v is not None and z <= c[6]:
                out.append(v)
    return out


def db_rng(vals):
    """A range of levels as the plan shows them: below 35 dB(A) is "< 35"."""
    vals = [v for v in vals if v is not None]
    if not vals:
        return "-"
    lo, hi = min(vals), max(vals)
    f = lambda v: "< 35" if v < 35.0 else "{:.2f}".format(v)           # v16.6: 2 decimals
    return f(lo) if f(lo) == f(hi) else (f(lo) + "–" + f(hi))


def tsec_rng(vals, fmt="{:.2f}"):           # v16.6: 2 decimals (v16.5: 0)
    vals = [v for v in vals if v is not None]
    if not vals:
        return "-"
    lo, hi = min(vals), max(vals)
    return fmt.format(lo) if fmt.format(lo) == fmt.format(hi) else (fmt.format(lo) + "–" + fmt.format(hi))


def tsec_name(num, what):
    return "%s_%s.png" % (num.replace(".", "_"), what)


def tsec_comfort_scales(S, lines):
    """Wind and temperature scales shared by every wind, air and felt section: the plan's, widened to what the
    sections reach (the colours stay tied to the same m/s and °C as on the plan)."""
    sc_ = comfort_scales(S)
    wmax, (lo, hi) = sc_["w_max"], sc_["t_range"]
    ws, ts = [], []
    for key in ("wind_sections", "air_sections", "felt_sections"):
        for k, a, b in lines.get(key, []):
            G = tsec_geom(S, a, b)
            cf = tsec_comfort(S, G)
            for sd in SEASONS:
                c = cf["seasons"][sd["key"]]
                if key == "wind_sections":
                    ws += [v for col in c["wind"] for v in col if v is not None]
                elif key == "air_sections":
                    ts += [v for col in c["ta"] for v in col if v is not None]
                else:
                    ts += [v for col in c["utci"] for v in col if v is not None]
    if ws:
        wmax = max(wmax, math.ceil(max(ws) * KT / 2.0) * 2.0 / KT)
    if ts:
        lo, hi = min(lo, 5.0 * math.floor(min(ts) / 5.0)), max(hi, 5.0 * math.ceil(max(ts) / 5.0))
    return wmax, lo, hi


# ------------------------------------------------------------ the seven technical section sheets (v16.2 layout)
def tsec_sheet_sound(S, B, X, Y, U, rects, d, G, lab, num, ctx):
    L = "LU_TECH::Sections"
    res_ = tsec_noise(S, G)
    cols = tsec_cols(S, G, TSEC_DS_SOUND)
    edges = [35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
    lut = lut_classes(edges, noise_pal())
    labels = ["< 35"] + ["%d-%d" % (edges[k], edges[k + 1]) for k in range(len(edges) - 1)] + ["> 80"]
    nm = S.env["noise"]
    rk = fp(G["key"], S.env["keys"]["noise_raw"], nm.get("offset", 0.0), TSEC_DS_SOUND, TSEC_DZ_SOUND)
    lay = tsec_layout(S, G, U, 4)
    res = tsec_px_res(G, lay["ss"])
    rows = []
    for key, head, sub, thr in (("lden", "Lden · DAY-EVENING-NIGHT LEVEL", "the weighted 24-hour level", 53.0),
                                ("day", "Ld · DAY 06-18", "", None), ("evening", "Le · EVENING 18-22", "", None),
                                ("night", "Ln · NIGHT 22-06", "", 45.0)):
        fld = dict(res_, vals=res_["vals"][key])
        png = tsec_compose(os.path.join(d, tsec_name(num, "sound_" + key)), S, G, res, "year", fld=fld, colour=lut,
                           rkey=fp(rk, key))
        f4 = [v for s_, v in tsec_at_height(fld, cols, 4.0) if v is not None]
        fa = tsec_facades(fld, cols)
        allv = [v for col in fld["vals"] for v in col if v is not None]
        if not allv:                                      # v38: the row's readings as tiles (were a sentence)
            txt = [("sound", "NO ROAD WITHIN 300 m", "not computed", "[3]")]
        else:
            txt = [("sound", "4 m ABOVE THE GROUND", "{} dB(A)".format(db_rng(f4)), "[2]"),
                   ("build", "IN FRONT OF CUT FACADES", "{} dB(A)".format(db_rng(fa)), "[2]")]
            if thr:
                txt.append(("limit", "AIR ABOVE WHO {:.0f} dB".format(thr), "{:.0f} %".format(
                    100.0 * sum(1 for v in allv if v > thr) / max(1, len(allv))), "[6]"))
            if any(all(v is None for v in col) for col in fld["vals"]):
                txt.append(("dot", "HATCHED", "not computed", "[3]"))

        def legend(x, y, w):
            return tech_bands(B, x, y, w, noise_pal(), labels, U, L, h=0.19, title="dB(A) · the bands of the plan (T1)")
        rows.append(dict(head=head, sub=sub, png=png, legend=legend, note=txt,
                         contours=sa_contours(fld, [55.0, 65.0, 75.0]) if allv else None, cfmt="{:.0f} dB",
                         graph=tsec_profile_graph(B, G, U, L, tsec_at_height_all(fld, cols, 4.0, G["cut"]), 35.0, 80.0, "", lut,
                                                  "dB(A) at 4 m above the ground")))
    cal = ("calibrated with {} measurements ({:+.1f} dB)".format(nm["n_meas"], nm["offset"]) if nm.get("n_meas")
           else "not yet calibrated with measurements")
    tsec_sheet(S, B, X, Y, U, rects, num, "SOUND · SECTION " + lab,
               "Lden · Ld · Le · Ln dB(A) · ground to above the roofs [1]",
               ["The plan's model (T1) at every receiver of the plane: RLS-90 emission of the counted road, segment method with "
                "distance, air, ground and screening by the surveyed buildings (ISO 9613-2 path difference over the most "
                "effective roof in each of 36 directions, and round the two sides of its block).",
                "Receivers every {:.1f} m along the line and in front of every cut "
                "facade, {:.0f} m apart in height, from 0.5 m above the ground or water; above a roof that roof screens "
                "too.".format(TSEC_DS_SOUND, TSEC_DZ_SOUND),
                "Sound model {}. Cut buildings are the analysis prisms; contours at 55, 65 and 75 dB(A). Hatched: no "
                "counted road within 300 m, not computed.".format(cal),
                traffic_note(S), height_note(S),
                "WHO Environmental Noise Guidelines (2018), as on T1: 53 dB Lden, 45 dB at night."], G, lab, rows, lay)


def tsec_sheet_heat(S, B, X, Y, U, rects, d, G, lab, num, ctx):
    L = "LU_TECH::Sections"
    gh = 2.0 * U
    lay = tsec_layout(S, G, U, 4, graph_h=gh)
    ss = lay["ss"]
    res = tsec_px_res(G, ss)
    band = max(0.3 * U / ss, 2.0 * res)
    rows = []
    for sd in SEASONS:
        key = sd["key"]
        r = heat_scale(S, key)
        prof = tsec_heat(S, G, key)
        L_ = S.env["lst"].get(key, {})
        when = L_.get("datetime_utc", "")
        if not r or not prof:
            rows.append(dict(head="{} · no clear Landsat scene".format(sd["name"])))
            continue
        _, med, vmin, vmax = r
        lut = lut_ramp(vmin, vmax, TECH_PAL["heat"])
        bands = [(s_ - 0.5, s_ + 0.5, z_, z_ + band, v_) for s_, z_, v_, roof in prof]
        try:
            day = (int(when[5:7]), int(when[8:10]))
        except Exception:
            day = key
        png = tsec_compose(os.path.join(d, tsec_name(num, "surface_heat_" + key)), S, G, res, day, colour=lut,
                           bands=bands, rkey=fp(G["key"], S.env["E_fp"], key, band))
        pts = [(s_, v_) for s_, z_, v_, roof in prof]
        roofs = [v_ for s_, z_, v_, roof in prof if roof and v_ is not None]
        wat = [v_ for s_, z_, v_, roof in prof if v_ is not None and not roof and
               any(w0 <= s_ <= w1 for w0, w1, bed, lvl in G["water"])]
        grd = [v_ for s_, z_, v_, roof in prof if v_ is not None and not roof and
               not any(w0 <= s_ <= w1 for w0, w1, bed, lvl in G["water"])]
        txt = [("heat", "ALONG THE LINE", "{} °C".format(tsec_rng([v for s_, v in pts], "{:.2f}")), "[1]")]   # v38: tiles
        for ic_, nm_, vv in (("roof", "ROOFS · MEAN", roofs), ("ground", "OPEN GROUND · MEAN", grd),
                             ("water", "WATER · MEAN", wat)):
            if vv:
                txt.append((ic_, nm_, "{:.2f} °C".format(sum(vv) / len(vv)), "[1]"))

        def legend(x, y, w, vmin=vmin, vmax=vmax, med=med):
            return tech_colorbar(B, x, y, w, TECH_PAL["heat"], vmin, vmax, U, L,
                                 title="Surface temperature °C, the plan's scale (white = {:.2f} °C)".format(med))

        def graph(x, ytop, w, h, pts=pts, vmin=vmin, vmax=vmax, lut=lut):
            tsec_graph(B, x, ytop, w, h, G["L"], [(pts, T_INK, 0.06)], vmin, vmax, U, L, "°", colour=lut)
        if L_.get("n_scenes"):                       # the seasonal mean of every clear scene (as on the plan, T2)
            head = "{} · MEAN OF {} CLEAR LANDSAT SCENES".format(sd["name"], L_["n_scenes"])
            sub = "{} to {} · {} UTC · read the trend [2]".format(
                L_.get("first", ""), L_.get("last", ""), L_.get("utc_mean", ""))
        else:                                        # one scene (environment data of v1)
            head = "{} · LANDSAT {} · {}".format(sd["name"], L_.get("scene", "")[3:4], when[:10])
            sub = "scene {} UTC · read the trend [2]".format(when[11:16])
        rows.append(dict(head=head, sub=sub, png=png, legend=legend, note=txt, graph=graph))
    multi = any(v.get("n_scenes") for v in S.env["lst"].values())
    tsec_sheet(S, B, X, Y, U, rects, num, "SURFACE HEAT · SECTION " + lab,
               "LST °C · ground, roofs, water under the line · " +
               ("seasonal mean" if multi else "one scene a season") + " [1]",
               ["Landsat 8/9 Collection 2 Level-2 surface temperature (USGS), band 10, " +
                ("the seasonal means of the plan (T2): every scene of 2021-2026 with at least 95 % of the area clear, each "
                 "cell averaged over the scenes that saw it clear; " if multi else "the scenes of the plan (T2), ") +
                "sampled every metre along the line (bilinear in the 30 m grid): on the roof where the line crosses a "
                "building, else on the ground or water.",
                "The band on each surface carries its value; the graph below repeats "
                "it. Thermal pixels are 100 m: read the trend, not single roofs. Surface temperature is not air temperature.",
                ("Deciduous crowns are drawn in leaf for the share of the season's days they are in leaf." if multi else
                 "Deciduous crowns are drawn as they were on the scene's day.")], G, lab, rows, lay)


def tsec_sheet_shade(S, B, X, Y, U, rects, d, G, lab, num, ctx):
    L = "LU_TECH::Sections"
    sh = tsec_shade(S, G)
    cols = tsec_cols(S, G, TSEC_DS_SHADE)
    lay = tsec_layout(S, G, U, 5)
    res = tsec_px_res(G, lay["ss"])
    rows = []
    items = [(sd["key"], sd["event"].upper(), sh["days"][sd["key"]], sd["day"]) for sd in SEASONS]
    items.append(("year", "THE MEAN DAY OF THE YEAR · ALL 365 DAYS", sh["year"], "year"))
    for key, head, se, day in items:
        n, cols_, edges = shade_scale(se["daylight"])
        # v16.3: the plan's class colours blended continuously (each class colour at its middle hour). With hard one-hour
        # classes, the sky's terrain shade, which hovers within minutes of a whole hour along the line, jumped between
        # two classes from column to column and read as full-height stripes; the values themselves are unchanged
        stops_ = [(k + 0.5, cols_[k]) for k in range(n)]
        lut = stops_table(stops_, 0.0, float(n))
        fld = dict(zlo=sh["zlo"], dz=sh["dz"], nz=sh["nz"], s=sh["s"], vals=se["vals"])
        png = tsec_compose(os.path.join(d, tsec_name(num, "shade_" + key)), S, G, res, day, fld=fld, colour=lut,
                           rkey=fp(G["key"], S.env["keys"]["solids"], key, TSEC_DS_SHADE, TSEC_DZ_SHADE, SUN_BINS))
        g0 = [v for s_, v in tsec_at_height(fld, cols, 0.5) if v is not None]
        g10 = [v for s_, v in tsec_at_height(fld, cols, 10.0) if v is not None]
        fa = tsec_facades(fld, cols)
        txt = [("shade", "GROUND 0.5 m · MEAN SHADE", "{} h".format(fmt_h(sum(g0) / len(g0)) if g0 else "-"), "[1]"),
               ("clock", "LINE SHADED > HALF THE DAY", "{:.0f} %".format(
                   100.0 * sum(1 for v in g0 if v >= se["daylight"] / 2.0) / max(1, len(g0))), "[1]")]   # v38: tiles
        if g10:
            txt.append(("shade", "10 m UP · MEAN", "{} h".format(fmt_h(sum(g10) / len(g10))), "[1]"))
        if fa:
            txt.append(("build", "IN FRONT OF CUT FACADES", "{}-{} h".format(fmt_h(min(fa)), fmt_h(max(fa))), "[1]"))

        def legend(x, y, w, stops_=stops_, n=n, lut=lut):
            return stretch_bar(B, x, y, w, stops_, 0.0, float(n), (lut, 0.0, float(n), 1.0), U, L,
                               "Hours in shade · T3 classes, blended [3]", th=0.22, dec=0)
        if key == "year":                            # v38: keywords
            sub = "all 365 days averaged · {} h daylight on the mean day [1]".format(fmt_h(se["daylight"]))
        else:
            sub = "sun up {}-{} local · {} h · every minute [1]".format(fmt_h(se["sunrise"]), fmt_h(se["sunset"]),
                                                                       fmt_h(se["daylight"]))
        half = se["daylight"] / 2.0
        rows.append(dict(head=head, sub=sub, png=png, legend=legend, note=txt,
                         contours=sa_contours(fld, [half]), cfmt="half the daylight",
                         graph=tsec_profile_graph(B, G, U, L, tsec_at_height_all(fld, cols, 0.5, G["cut"]), 0.0, se["daylight"], " h",
                                                  lut, "hours in shade at 0.5 m above the ground", dec=0,
                                                  trend=TSEC_TREND)))
    tsec_sheet(S, B, X, Y, U, rects, num, "SHADE · SECTION " + lab,
               "Hours in shade · every point of the plane · key days + year [1]",
               ["Every minute the sun is up (NOAA sun position, UTC+3), as on the plan (T3), at every point of the plane "
                "({:g} m along the line, {:g} m in height).".format(TSEC_DS_SHADE, TSEC_DZ_SHADE),
                "Casters: the exact obstruction of each point for every degree of sun "
               "azimuth by every building (its roof over the surveyed ground, concave footprints and courtyards included), "
               "the 3D tree crowns (canopy height map, modelled heights; olives 15 %, others in leaf 3 %, bare 46 % of the sun passes; deciduous ones in leaf "
               "from {} to {}, drawn bare or in leaf as on each day), the terrain horizon (PVGIS DEM, as seen from the "
               "ground; above the ground lowered by how much the terrain's horizon falls with height: the survey terrain "
               "inside the frame and the PVGIS DEM heights of the 100 m grid out to its edge, the terrain beyond taken as "
               "far) and, near the ground, the slope's own plane. The "
               "stream channel's walls are not casters.".format(*leaf_dates()),
                "The contour marks half the day's daylight in shade. Colours: the "
                "plan's one-hour classes blended between whole hours, so minutes either side of an hour do not jump a "
                "class.", height_note(S)], G, lab, rows, lay)


def rad_graph_hi(S, edges):
    """v16.5: the top of every solar section graph: the plan's 99.9th percentile over the four seasons (kWh/m2 per day,
    rounded up to 0.5), at least the top class edge."""
    rd = S.env["rad"]
    v = np.concatenate([np.asarray(rd["seasons"][sd["key"]]["kwh"], float).ravel() for sd in SEASONS])
    v = v[np.isfinite(v)]
    top = float(np.percentile(v, 99.9)) if v.size else edges[-1]
    return math.ceil(max(top, edges[-1]) * 2.0) / 2.0


def tsec_sheet_solar(S, B, X, Y, U, rects, d, G, lab, num, ctx):
    L = "LU_TECH::Sections"
    so = tsec_solar(S, G)
    gh = 2.0 * U
    lay = tsec_layout(S, G, U, 4, graph_h=gh)
    ss = lay["ss"]
    res = tsec_px_res(G, ss)
    band = max(0.3 * U / ss, 2.0 * res)
    edges = rad_scale(S)
    cols_ = ramp_hex(TECH_PAL["rad"], len(edges) + 1)
    lut = lut_classes(edges, cols_)
    labels = ["< %.2f" % edges[0]] + ["%.2f-%.2f" % (edges[i], edges[i + 1]) for i in range(len(edges) - 1)] + ["> %.2f" % edges[-1]]
    months = {"spring": "MARCH-MAY", "summer": "JUNE-AUGUST", "autumn": "SEPTEMBER-NOVEMBER", "winter": "DECEMBER-FEBRUARY"}
    rows = []
    for sd in SEASONS:
        key = sd["key"]
        bands = [(p0, p1, z_, z_ + band, v[key]) for p0, p1, z_, v in so["ground"]]
        bands += [(a_, b_, top, top + band, v[key]) for a_, b_, top, v in so["roofs"]]
        bands += [((s_w - band, s_w) if side_ < 0 else (s_w, s_w + band)) + (z0, z1, v[key])
                  for s_w, z0, z1, side_, nrm, v in so["walls"]]
        png = tsec_compose(os.path.join(d, tsec_name(num, "solar_" + key)), S, G, res, key, colour=lut, bands=bands,
                           rkey=fp(G["key"], S.env["keys"]["solids"], key, band, edges, SUN_BINS))
        gpts = [(0.5 * (p0 + p1), v[key]) for p0, p1, z_, v in so["ground"]]
        # v16.4: the graph follows the top surface along the line, as the plan sees it: the ground where the line is in
        # the open, the roof (dashed, over a grey mark) where it crosses a cut building, joined at the walls. v16.3 drew
        # the ground alone, broken at every building, and the roofs as a separate red step line over it
        # the ground in a slot narrower than TSEC_SLOT between two cut buildings (a party-wall gap the plan's grid does not
        # resolve either) is left out of the graph, as in the other sections: the roof line runs across
        sp_ = sorted((c[0], c[1]) for c in G["cut"])
        slots_ = [(p[1], q[0]) for p, q in zip(sp_, sp_[1:]) if 0.0 < q[0] - p[1] < TSEC_SLOT]
        tpts = [(s_, v_, False) for s_, v_ in gpts if not any(e_ <= s_ <= f_ for e_, f_ in slots_)] + \
            [(0.5 * (a_ + b_), v[key], True) for a_, b_, top, v in so["roofs"]]
        gv = [v for s_, v in gpts]
        rv = [v[key] for a_, b_, top, v in so["roofs"]]
        wv = [v[key] for s_w, z0, z1, side_, nrm, v in so["walls"]]
        txt = []                                      # v38: the means as tiles, kWh/m2 per day (were a sentence)
        for ic_, nm_, vv in (("ground", "GROUND · kWh/m²·day", gv), ("roof", "ROOFS · kWh/m²·day", rv),
                             ("build", "CUT FACADES · MEAN", wv)):
            if vv:
                txt.append((ic_, nm_, "{:.2f}".format(sum(vv) / len(vv)), "[1]"))
        if wv:
            txt.append(("build", "FACADES · RANGE", "{:.2f}–{:.2f}".format(min(wv), max(wv)), "[1]"))
        # v16.5: one graph range for every solar section and season (0 to the plan's highest value), so the graphs
        # compare (v16.4: each row from its own lowest to highest value)
        lo_, hi_ = 0.0, rad_graph_hi(S, edges)

        def legend(x, y, w):
            return tech_bands(B, x, y, w, cols_, labels, U, L, h=0.17, title="kWh/m² per day · the classes of the plan (T4)")

        def graph(x, ytop, w, h, tpts=tpts, lo_=lo_, hi_=hi_):
            tsec_graph(B, x, ytop, w, h, G["L"], [(tpts, T_INK, 0.06)], lo_, hi_, U, L, "", colour=lut, trend=TSEC_TREND)
            B.text("kWh/m²·day top surface · dashed: roof · blue: {:g} m mean [2]".format(TSEC_TREND),
                   x + w - 0.15 * U, ytop - 0.32 * U, 0.2 * U, T_GREY, L, align="R")       # v38: keywords
        rows.append(dict(head="{} · {} · {} DAYS".format(sd["name"], months[key], days_in_season(key)),
                         sub="bands: ground, roofs, cut facades · graph: top surface [2]",
                         png=png, legend=legend, note=txt, graph=graph))
    tsec_sheet(S, B, X, Y, U, rects, num, "SOLAR RADIATION · SECTION " + lab,
               "kWh/m² per day · season means · ground, roofs, cut facades [1]",
               ["The plan's model (T4) at the surfaces of the section: every hour of the PVGIS-SARAH2 typical year with the "
               "sun at its exact position, each point (ground and roofs evenly every {:g} m, the ground on the surveyed "
               "slope, cut facades in bands of at most {:g} m) with its own exact 3D obstruction by buildings, crowns and terrain for "
               "every degree of sun azimuth, its cosine-weighted sky (72 sectors, its own plane hiding the sky behind it), "
               "the Perez horizon band and ground reflection (albedo 0.2).".format(TSEC_DS_SOLAR, TSEC_DZ_SOLAR),
                "Bands on the ground, the roofs and the cut facades. Graph: kWh/m² per day on the top surface along the "
                "line: the ground, and the roof where the line crosses a building (dashed over a grey mark); blue line: "
                "the mean over {:g} m of line.".format(TSEC_TREND)], G, lab, rows, lay)


