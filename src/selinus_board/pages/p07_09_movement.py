# p.07-09 movement: how people use it, today and the proposal (split from parts/15_ndvi_col.py, parts/15d_v44_pages.py, parts/15f_v46_pages.py, parts/15i_r28_movement.py, parts/16_write_city_link_movement.py on 29 Oct 2026; moved unchanged)
# T3a WO-T3a-5 (29 Oct 2026, package B, D3 b, D8 b, D10 a): see the block below; the proposal map (drw_proposal) and
# the walk / car index chart (drw_index_change) are gone; draw_mv_proposal draws the street sections (drw_street_sections).


def div_t(d, dmax):
    if dmax <= 0:
        return 0.5
    s = math.sqrt(min(1.0, abs(d) / dmax))
    return 0.5 + 0.5 * s if d > 0 else 0.5 - 0.5 * s


# ============================================================ T3a WO-T3a-5 (29 Oct 2026): package B, D3 b, D8 b, D10 a
# Booklet pp.07-09 now: p07 "how people use it" (this file: drw_movement, drw_walking_today, drw_driving_today and
# their notes, all on the shared basemap in simple mode); p08 = the city link's framework diagram + who the project
# brings (bergama_city_link v4, page 1) + the before/after street sections drawn here (drw_street_sections, D3 b,
# replacing the walk / car index chart drw_index_change and the city link's "walking potential"); p09 = the city link's
# hub by hub (v4, page 2). The proposal map drw_proposal is gone: its roads, crossings, hubs and reach are in the
# framework diagram. Hand-off for the framework: movement_framework.json (_t3_write_framework, below).
T3_PUB_SRC = u"OpenStreetMap (streets, shops; extract of 28 Jul 2026); Overture Maps Foundation (places)"   # D13: public only
T3_FW_FILE = os.path.join(SELINUS_RES_DIR, "movement_framework.json")    # read by bergama_city_link v4 (framework)
T3_FW_N = 5              # the busiest named streets per mode handed to the framework (as the maps name them)


T3_BASE_DASH = []        # R2-B (31 Oct, U23): board polylines of the dashed lines _t3_base drew on the current map


def _t3_base(S, CB, V, k, L, order=2):
    """T3a (02 §1): the shared basemap in simple mode (stream, faint streets, faint buildings; basemap.py, memoised)
    through ClipB CB on the theme-B view V, then the study area's outline (G8). The same base on pp.07-09 (the city
    link draws the same items). Without basemap data (a first ever run) the board's own base, made pale, logged."""
    items = None
    del T3_BASE_DASH[:]                                   # R2-B: the dashed base lines of this map (street names avoid them)
    try:
        fr = basemap_frame()
        box = (min(p[0] for p in fr), min(p[1] for p in fr), max(p[0] for p in fr), max(p[1] for p in fr)) if fr else None
        items = basemap_items("simple", box=box)
    except Exception:
        LOG.append("WARNING: the shared basemap (simple) was not read:\n" + traceback.format_exc())
    if not items:
        LOG.append("Movement maps: no basemap data (cached/basemap/basemap.json), the board's pale base instead.")
        b_base(S, R28Pale(CB), V, k, L)
        return False

    def col_of(hx, alpha):
        a_ = 1.0 if alpha is None else max(0.0, min(1.0, float(alpha)))
        return mix(C(hx), WHITE, 1.0 - a_)

    def fill_fn(rings, hx, alpha, nonzero):
        rs = [R_ for R_ in rings if len(R_) >= 3]
        if rs:
            CB.fill(rs, col_of(hx, alpha), L, order)

    def line_fn(pts, hx, w_mm, dash_mm, alpha):
        if len(pts) < 2:
            return
        col = col_of(hx, alpha)
        if dash_mm:
            on, off = (dash_mm[0], dash_mm[1]) if isinstance(dash_mm, (list, tuple)) else (dash_mm, dash_mm)
            T3_BASE_DASH.append(list(pts))
            for d in dashes(pts, on * k, off * k):
                CB.line(d, col, L, order + 1, bk_lw(w_mm, k))
        else:
            CB.line(pts, col, L, order + 1, bk_lw(w_mm, k))
    basemap_draw(items, lambda p: V.p(p[0], p[1]), fill_fn, line_fn)
    draw_r28_study(S, CB, V, k, L)
    return True


def _t3_base_leg():
    """the simple basemap's legend rows (its own colours, basemap.py BM_COL / BM_FAINT) and the study area"""
    bc, bf = globals().get("BM_COL") or {}, globals().get("BM_FAINT") or {}
    return [("box", C(bc.get("water", "91ADB4")), u"Selinos stream"),
            ("dash", C(bc.get("water_edge", "5D7F8D")), u"Selinos stream, covered"),
            ("box", C(bf.get("bld", "D3D0CB")), u"Building"), R28_STUDY_LEG]


class _T3Put(object):
    """T3a: house shapes (page mm, y up, hex colours: icons.py, section_parts.py, plants.py, figures.py,
    section_frame.py) onto the board: board = (ox + x * kb, oy + y * kb), kb = board units per booklet mm. T4 (30
    Oct): every shape kind of the modules: ("poly", ring, fill, stroke, lw[, alpha]) (alpha = the fill mixed toward
    the white board), ("line", pts, colour, lw[, dash mm]), ("text", s, x, y, font size mm, colour, bold, align) and
    ("image", x, y, w, h, path, alpha, flip, clip) (D1 a: B.image; clip ignored); one order per call, so the shapes
    keep their own drawing order"""

    def __init__(self, B, ox, oy, kb, L):
        self.B, self.ox, self.oy, self.kb, self.L = B, ox, oy, kb, L

    def P(self, pts):
        return [(self.ox + p[0] * self.kb, self.oy + p[1] * self.kb) for p in pts]

    def put(self, shapes, order=40):
        col_ = lambda c_: C(c_) if isinstance(c_, str) else c_
        for s_ in shapes or []:
            if s_[0] == "poly":
                ring, fill, stroke, lw = s_[1], s_[2], s_[3], s_[4]
                if len(ring) < 3:
                    continue
                Q = self.P(ring)
                if fill:
                    a_ = s_[5] if len(s_) > 5 and s_[5] is not None else 1.0
                    self.B.fill([Q], mix(col_(fill), WHITE, 1.0 - max(0.0, min(1.0, a_))), self.L, order)
                if stroke and lw:
                    self.B.line(Q + [Q[0]], col_(stroke), self.L, order, bk_lw(lw, self.kb))
            elif s_[0] == "line" and len(s_[1]) >= 2:
                Q, w_ = self.P(s_[1]), bk_lw(s_[3], self.kb)
                dash = s_[4] if len(s_) > 4 else None
                for d in (dashes(Q, dash[0] * self.kb, dash[1] * self.kb) if dash else [Q]):
                    self.B.line(d, col_(s_[2]), self.L, order, w_)
            elif s_[0] == "text" and u"{}".format(s_[1]).strip():
                self.B.text(s_[1], self.ox + s_[2] * self.kb, self.oy + s_[3] * self.kb, s_[4] * R28MV_CAP * self.kb,
                            col_(s_[5]), self.L, order=order, font=FONT_TITLE, bold=bool(s_[6]) if len(s_) > 6 else False,
                            align=s_[7] if len(s_) > 7 else "L")
            elif s_[0] == "image":
                x_, y_, w_, h_ = s_[1], s_[2], s_[3], s_[4]
                self.B.image(s_[5], self.ox + x_ * self.kb, self.oy + y_ * self.kb, self.ox + (x_ + w_) * self.kb,
                             self.oy + (y_ + h_) * self.kb, self.L, order=order, alpha=s_[6] if len(s_) > 6 else None,
                             flip=bool(s_[7]) if len(s_) > 7 else False)

    def rect(self, x0, y0, x1, y1, fill, stroke=None, lw=0.15, order=40):
        self.put([("poly", [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, stroke, lw)], order)

    def line(self, pts, hx, lw, order=44):
        self.put([("line", pts, hx, lw)], order - 1)

    def text(self, s, x, y, pt, hx="4A3F35", bold=False, align="L", order=66):
        """s at (x, y) mm (baseline), pt points on the booklet page; returns its width in mm"""
        h = bk_hk(pt, self.kb)
        w_ = r28mv_tw(s, h, bold)
        X = self.ox + x * self.kb - (0.5 * w_ if align == "C" else (w_ if align == "R" else 0.0))
        self.B.text(s, X, self.oy + y * self.kb, h, C(hx), self.L, order=order, font=FONT_TITLE, bold=bold)
        return w_ / self.kb


def _t3_named_runs(R, F, names, net):
    """{street name: [polylines in the frame]} of the named streets along network net (walk_b, car_b)"""
    pieces = R["pieces"]

    def val(pi):
        nm = (pieces[pi]["tags"].get("name") or "").strip()
        return nm if nm in names else None
    out = {}
    for P, nm in _runs(R["chains"][net], pieces, R["xy"], val, set(R["inside"]), F):
        out.setdefault(nm, []).append(P)
    return out


def _t3_write_framework(S, R, MV):
    """T3a (D8 b): cached/selinus_board/movement_framework.json, the site board's half of the framework diagram that
    bergama_city_link v4 draws (it runs after the board): the T3_FW_N busiest named streets on foot (walk_b) and by
    car (car_b) with their index (100 = the busiest street piece today) and their runs in the frame, the commercial
    spines (primary and secondary, with their shop counts) and the civic constellations, survey m (0.1 m). Once per
    run (S._t3_fw)."""
    got = getattr(S, "_t3_fw", None)
    if got is not None:
        return got
    F = S.F

    def rnd(P):
        return [[round(p[0], 1), round(p[1], 1)] for p in P]
    out = dict(script=SCRIPT_VERSION, run_time=time.strftime("%Y-%m-%d %H:%M:%S"), walk=[], car=[], spines=[],
               spines_secondary=[], civic=[], r_walk=MV_OPT["r_walk"],
               note="survey m; walk / car = the busiest named streets of the movement potential today (shortest "
                    "routes between buildings and everyday destinations; 100 = the busiest street piece), not counts")
    if R:
        for key, tag in (("walk_b", "walk"), ("car_b", "car")):
            rows = mv_key_rows(MV, key, T3_FW_N)
            runs = _t3_named_runs(R, F, set(r_["name"] for r_ in rows), key)
            out[tag] = [dict(name=r_["name"], index=round(r_[key], 1), runs=[rnd(P) for P in runs[r_["name"]]])
                        for r_ in rows if runs.get(r_["name"])]
    for key, grp in (("spines", "corr_primary"), ("spines_secondary", "corr_secondary")):
        for g in getattr(S, grp, None) or []:
            runs = [q for P in g["Ps"] for q in F.clip_line(P) if len(q) >= 2]
            if runs:
                out[key].append(dict(label=g["label"], shops=g["n"], runs=[rnd(P) for P in runs]))
    for c_ in getattr(S, "clusters", None) or []:
        if len(c_["P"]) >= 3 and any(F.inside(p[0], p[1]) for p in c_["P"]):
            out["civic"].append(dict(ring=rnd(c_["P"])))
    try:
        os.makedirs(SELINUS_RES_DIR, exist_ok=True)
        with open(T3_FW_FILE, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, separators=(",", ":"))
        LOG.append(u"movement_framework.json: {} walking, {} driving streets, {} + {} commercial spines, {} civic "
                   u"constellations.".format(len(out["walk"]), len(out["car"]), len(out["spines"]),
                                             len(out["spines_secondary"]), len(out["civic"])))
    except Exception:
        LOG.append("WARNING: movement_framework.json not written (the city link's framework draws without the "
                   "board's streets):\n" + traceback.format_exc())
    S._t3_fw = out
    return out


def _t3_grad_w(v):
    """the line weight (mm) of index v, interpolated between the class weights (R28MV_CLS_W at the class tops)"""
    xs, ws = (0.0,) + tuple(R28MV_CLS), (R28MV_CLS_W[0],) + tuple(R28MV_CLS_W)
    v = max(0.0, min(xs[-1], v))
    for i in range(1, len(xs)):
        if v <= xs[i]:
            t = (v - xs[i - 1]) / max(1e-9, xs[i] - xs[i - 1])
            return ws[i - 1] + (ws[i] - ws[i - 1]) * t
    return ws[-1]


def _t3_names(rows, n=2):
    """'A and B' of the first n street names of rows"""
    nm = [r_["name"] for r_ in rows[:n]]
    return u" and ".join(nm) if nm else u""


# ============================================================ drawing (survey coordinates; baked via selinus_board helpers)
def _runs(chains, pieces, xy, value_of, inside_frame, F):
    """Polylines of equal value along every chain: [(points, value)], clipped to the frame."""
    out = []
    for ch in chains:
        run, cur = [], None
        for (pi, fw), n0, n1 in zip(ch["seq"], ch["nodes"][:-1], ch["nodes"][1:]):
            v = value_of(pi) if pi in inside_frame else None
            if v != cur or not run:
                if run and cur is not None:
                    out.append((run, cur))
                run, cur = [xy[n0]], v
            run.append(xy[n1])
        if run and cur is not None:
            out.append((run, cur))
    clipped = []
    for P, v in out:
        for q in F.clip_line(P):
            if len(q) >= 2:
                clipped.append((q, v))
    return clipped


# ------------------------------------------------------------ p.6 walking / driving today: the key streets only
def mv_key_rows(MV, key, n=MV_KEY_N):
    """v44: the n named streets (50 m+ in the frame) with the highest potential `key` today (the engine's own street
    table), highest first."""
    return [r for r in sorted(MV.get("big") or [], key=lambda r: -r[key]) if r[key] > 0][:n]


def b_view(F, x, ytop, U):
    """v46: a theme-B map: the whole frame F at 1:10,000 on the booklet page, its top-left corner at (x, ytop); k =
    board units per booklet mm of a drawing 120 U wide (as draw_edge_build). Returns (View, k, board units per metre,
    the map's rectangle)."""
    k = 120.0 * U / BK_AW
    ss = 1000.0 * k / B_DEN
    return View(F, ss, x, ytop), k, ss, (x, ytop - F.h * ss, x + F.w * ss, ytop)


# ------------------------------------------------------------ p.07 walking / driving today: every piece graded
def r28mv_class(v):
    """the index class (0-4) of value v"""
    for i, up in enumerate(R28MV_CLS):
        if v < up:
            return i
    return len(R28MV_CLS) - 1


def r28mv_class_streets(B, V, runs, k, L, order):
    """v50 (MIRAQUA 28 Oct, P07.3): every street piece of runs [(points, (OSM class, index))] (mv_runs) in its index
    class: colour (the top map's SEQ ramp at the class's upper step) and line weight (R28MV_CLS_W) by class, the
    busiest drawn last. Returns the length (m) in each class. T3a (29 Oct, package B p.07 "smoother colour
    transitions"): the colour is the continuous ramp of the top map (mv_ramp SEQ at the piece's own value) and the
    weight is interpolated between the class weights (_t3_grad_w), every piece over a pale halo of its own colour
    (order), the lines above every halo (order + 1), so neighbouring pieces blend into a gradient; the classes stay
    only for the lengths the notes count."""
    lens = [0.0] * len(R28MV_CLS)
    for P, (cls, v) in sorted(runs, key=lambda r_: r_[1][1]):
        c_ = r28mv_class(v)
        lens[c_] += pl_length(P)
        col, wl = mv_ramp(SEQ, seq_t(v, 100.0)), _t3_grad_w(v)
        Q = V.P(P)
        B.line(Q, mix(col, WHITE, 0.6), L, order, bk_lw(2.2 * wl, k))
        B.line(Q, col, L, order + 1, bk_lw(wl, k))
    return lens


def r28mv_class_legend():
    """the ramp as booklet legend rows: samples at the class tops in their colour and line weight (pt). T3a (G1):
    the term spelled out: the share of everyday routes using the street, 100 = the busiest street piece"""
    labs = [u"{:.0f}".format(v_) for v_ in R28MV_CLS]
    labs[0] = labs[0] + u" · few everyday routes use the street"
    labs[-1] = labs[-1] + u" · the busiest street piece"
    return [dict(kind="line", colour=crop_hex(mv_ramp(SEQ, seq_t(v_, 100.0))), label=lab,
                 width=round(_t3_grad_w(v_) * 72.0 / 25.4, 2)) for v_, lab in zip(R28MV_CLS, labs)]


def _t3_rot_box(cx, cy, ux, uy, a0, a1, b0, b1):
    """the corners of a rectangle round (cx, cy): a0..a1 along the unit direction (ux, uy), b0..b1 across it (to
    its left)"""
    nx, ny = -uy, ux
    return [(cx + ux * a + nx * b, cy + uy * a + ny * b) for a, b in ((a0, b0), (a1, b0), (a1, b1), (a0, b1))]


def _t3_bb(P):
    return (min(p[0] for p in P), min(p[1] for p in P), max(p[0] for p in P), max(p[1] for p in P))


def _t3_poly_hit(P, Q):
    """True when the convex polygons P and Q (a segment = a polygon of two points) touch (separating axes)"""
    for R_ in (P, Q):
        n = len(R_)
        for i in range(n):
            ex, ey = R_[(i + 1) % n][0] - R_[i][0], R_[(i + 1) % n][1] - R_[i][1]
            if abs(ex) + abs(ey) < 1e-12:
                continue
            pa = [p[0] * -ey + p[1] * ex for p in P]
            qa = [q[0] * -ey + q[1] * ex for q in Q]
            if max(pa) < min(qa) or max(qa) < min(pa):
                return False
    return True


def _t3_run_label(Qs, wt, h, half, bounds, taken, segs, others=()):
    """T4 (30 Oct, p7 G3): a spot where a street name (wt long, capital height h, board units) runs ALONG its own
    street: a straight enough stretch of one of its runs Qs (board polylines; the longest run first, its middle
    first), the name beside the line (half = half the drawn street's width) on either side, upright, inside bounds,
    clear of the names already placed (taken: rotated boxes) and of the linework segs [(a, b, bbox)]. R2-B (31 Oct,
    U23 "which name points to which street"): others = the segments of every OTHER drawn street, the stream and the
    dashed base lines; the name's box grown by a clear band (1.2 h across, 0.5 h along) must touch none of them, so
    the nearest line to every name is its own street; the side further from other lines is tried first. Returns
    (x, y of the baseline's middle, angle (radians), its box) or None."""
    pad = 0.15 * h
    for Q in sorted(Qs, key=lambda Q_: -pl_length(Q_)):
        Lq = pl_length(Q)
        if Lq < wt + 2.0 * pad:
            continue
        step, ds, d = max(0.2 * wt, 0.5 * h), [], 0.0
        while d + wt <= Lq + 1e-9:
            ds.append(d)
            d += step
        ds.sort(key=lambda d_: abs(d_ + 0.5 * wt - 0.5 * Lq))
        for d in ds:
            p0, p1 = pl_point_at(Q, d)[0], pl_point_at(Q, d + wt)[0]
            cl = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
            if cl < 0.85 * wt:
                continue
            ux, uy = (p1[0] - p0[0]) / cl, (p1[1] - p0[1]) / cl
            if ux < -1e-9 or (abs(ux) <= 1e-9 and uy < 0):
                ux, uy = -ux, -uy                         # upright: never upside down
            nx, ny = -uy, ux
            if any(abs((q[0] - p0[0]) * nx + (q[1] - p0[1]) * ny) > 0.3 * h
                   for q in (pl_point_at(Q, d + wt * i / 6.0)[0] for i in range(1, 6))):
                continue                                  # the stretch bends: the name would leave its street
            mx, my = 0.5 * (p0[0] + p1[0]), 0.5 * (p0[1] + p1[1])
            g = half + 0.3 * h
            for b0 in (g, -g - h):
                poly = _t3_rot_box(mx, my, ux, uy, -0.5 * wt - pad, 0.5 * wt + pad, b0 - pad, b0 + h + pad)
                if not all(bounds[0] <= p[0] <= bounds[2] and bounds[1] <= p[1] <= bounds[3] for p in poly):
                    continue
                if any(_t3_poly_hit(poly, t_) for t_ in taken):
                    continue
                bb = _t3_bb(poly)
                if any(sb[0] <= bb[2] and bb[0] <= sb[2] and sb[1] <= bb[3] and bb[1] <= sb[3] and
                       _t3_poly_hit([a, b], poly) for a, b, sb in segs):
                    continue
                # the clear band: away from its own line the band grows 1.2 h, along it 0.5 h (own line side: none)
                far0, far1 = (b0 - pad, b0 + h + pad + 1.2 * h) if b0 > 0 else (b0 - pad - 1.2 * h, b0 + h + pad)
                band = _t3_rot_box(mx, my, ux, uy, -0.5 * wt - pad - 0.5 * h, 0.5 * wt + pad + 0.5 * h, far0, far1)
                bb2 = _t3_bb(band)
                if any(sb[0] <= bb2[2] and bb2[0] <= sb[2] and sb[1] <= bb2[3] and bb2[1] <= sb[3] and
                       _t3_poly_hit([a, b], band) for a, b, sb in others):
                    continue
                return mx + nx * b0, my + ny * b0, math.atan2(uy, ux), poly
    return None


def draw_mv_key(S, B, V, R, MV, key, F, L, h, bounds, k):
    """v44: the key streets of the walking / driving map, named. v50 (MIRAQUA 28 Oct, P07.3, P07.4): every street
    piece is drawn graded (r28mv_class_streets), so this names the 5 busiest named streets (mv_key_rows) at h (7 pt),
    "name · index". T4 (30 Oct, p7 G3: "which name belongs to which street"): each name runs along its own street
    (_t3_run_label), clear of the other names, the study-area outline and the named streets' lines; where no
    stretch of its street holds it, M2 lp_place sets it beside the street on a short leader that touches it.
    Returns (their rows, {name: every point of its runs})."""
    rows = mv_key_rows(MV, key)
    names = set(r_["name"] for r_ in rows)
    pieces = R["pieces"]
    net = "car_b" if key.startswith("car") else "walk_b"

    def val(pi):
        nm = (pieces[pi]["tags"].get("name") or "").strip()
        return nm if nm in names else None
    runs, pts = {}, {}
    for P, nm in _runs(R["chains"][net], pieces, R["xy"], val, set(R["inside"]), F):
        pts.setdefault(nm, []).extend(P)
        runs.setdefault(nm, []).append(V.P(P))
    obst = [V.P(list(P) + [P[0]]) for P in getattr(S, "r28_study", None) or [] if len(P) >= 2]
    obst += [Q for Qs in runs.values() for Q in Qs]
    segs = [(a, b, _t3_bb([a, b])) for Q in obst for a, b in zip(Q[:-1], Q[1:])]
    # R2-B (U23): for each name, the segments of every drawn street piece that is not its own street, the stream and
    # the dashed base lines (the name keeps a clear band from them: _t3_run_label others)

    def _sk(a, b):
        return tuple(sorted(((round(a[0], 1), round(a[1], 1)), (round(b[0], 1), round(b[1], 1)))))
    own_k = {}
    for P, nm in _runs(R["chains"][net], pieces, R["xy"], val, set(R["inside"]), F):
        own_k.setdefault(nm, set()).update(_sk(a, b) for a, b in zip(P[:-1], P[1:]))
    street_s = []
    for P, v_ in mv_runs(S, R, key, F):
        Q = V.P(P)
        street_s += [(_sk(a, b), qa, qb) for (a, b), qa, qb in zip(zip(P[:-1], P[1:]), Q[:-1], Q[1:])]
    st_ = r28mv_main_stream(S)
    fixed = [(a, b, _t3_bb([a, b])) for Q in ([V.P(st_)] if st_ else []) + list(T3_BASE_DASH)
             for a, b in zip(Q[:-1], Q[1:])]

    def others_of(nm):
        mine = own_k.get(nm, set())
        return fixed + [(qa, qb, _t3_bb([qa, qb])) for sk, qa, qb in street_s if sk not in mine]
    kd = kind_of(FONT_TITLE)
    taken, rest = [], []
    for r_ in rows:
        Qs = runs.get(r_["name"])
        if not Qs:
            continue
        s = u"{} · {:.0f}".format(r_["name"], r_[key])
        wt = tw(s, h, kd)
        got = _t3_run_label(Qs, wt, h, 1.1 * _t3_grad_w(r_[key]) * k, bounds, taken, segs, others_of(r_["name"]))
        if got is None:
            rest.append((s, wt, Qs))
            continue
        x_, y_, ang, poly = got
        taken.append(poly)
        B.text(s, x_, y_, h, INK, L, order=66, font=FONT_TITLE, bold=True, align="C", angle=ang)
    if rest:                                              # M2: beside its street on a leader that touches it
        labs, q_lab = [], {}
        for s, wt, Qs in rest:
            Q = max(Qs, key=pl_length)
            q = pl_point_at(Q, pl_length(Q) / 2.0)[0]
            q_lab[s] = q
            labs.append(dict(x=q[0] / k, y=q[1] / k, w=(wt + 0.4 * h) / k, h=1.5 * h / k, rank=0, r=0.0))
        obs = [tuple(v / k for v in _t3_bb(t_)) for t_ in taken]
        res = lp_place(labs, obstacles=obs, lines=[[(p[0] / k, p[1] / k) for p in Q] for Q in obst],
                       bounds=tuple(v / k for v in bounds), max_leader=12.0)
        for (s, wt, Qs), g in zip(rest, res):
            if g is None:
                LOG.append(u"p.07 {}: no room for the street name \"{}\".".format(key, s))
                continue
            bx, f = g["box"], g["size"]
            B.text(s, bx[0] * k + 0.2 * h * f, bx[1] * k + 0.25 * h * f, h * f, INK, L, order=66, font=FONT_TITLE,
                   bold=True)
            if g["leader"]:
                (a, b) = g["leader"]
                B.line([(a[0] * k, a[1] * k), (b[0] * k, b[1] * k)], INK, L, 65, bk_lw(0.15, k))
                # R2-B (U23): a dot where the leader meets its own street (the end nearer the street's point)
                e_ = min((a, b), key=lambda q_: (q_[0] * k - q_lab[s][0]) ** 2 + (q_[1] * k - q_lab[s][1]) ** 2)
                B.fill([[(e_[0] * k + 0.45 * k * math.cos(t_ * math.pi / 4.0), e_[1] * k + 0.45 * k *
                          math.sin(t_ * math.pi / 4.0)) for t_ in range(8)]], INK, L, 66)
    return rows, pts


def r28mv_main_stream(S):
    streams = [P for P in (getattr(S, "selinus", None) or []) if len(P) >= 2]
    return max(streams, key=pl_length) if streams else None


def r28mv_edge_means(S, R):
    """v50 (P07.2): today's walking and driving index, length-weighted, on the street pieces whose middle lies within
    R28MV_EDGE_M of the main Selinos line (as city_link_movement.json "edge") and on every piece on the map:
    {"walk_b" | "car_b": (along the stream, all, m along the stream)}; once per run (S._r28mv_edge)."""
    got = getattr(S, "_r28mv_edge", None)
    if got is not None:
        return got
    out, main = {}, r28mv_main_stream(S)
    if main:
        d = R28MV_EDGE_M
        segs = list(zip(main[:-1], main[1:]))
        g = Grid(d)
        for i, (a, b) in enumerate(segs):
            g.add(i, (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])))
        pieces, xy, IDX = R["pieces"], R["xy"], R["IDX"]
        acc = {"walk_b": [0.0, 0.0, 0.0, 0.0], "car_b": [0.0, 0.0, 0.0, 0.0]}
        for i in R["inside"]:
            p = pieces[i]
            if p["prop"] or p["L"] <= 0:
                continue
            m = ((xy[p["a"]][0] + xy[p["b"]][0]) / 2.0, (xy[p["a"]][1] + xy[p["b"]][1]) / 2.0)
            near = any(seg_dist(m[0], m[1], segs[j][0][0], segs[j][0][1], segs[j][1][0], segs[j][1][1]) <= d
                       for j in g.query((m[0] - d, m[1] - d, m[0] + d, m[1] + d)))
            for key, ok in (("walk_b", p["walk"]), ("car_b", p["cf"] or p["cb"])):
                if not ok:
                    continue
                v = IDX[key].get(i, 0.0) * p["L"]
                a_ = acc[key]
                a_[0] += v
                a_[1] += p["L"]
                if near:
                    a_[2] += v
                    a_[3] += p["L"]
        out = dict((key, (a_[2] / a_[3] if a_[3] else None, a_[0] / a_[1] if a_[1] else None, a_[3]))
                   for key, a_ in acc.items())
    S._r28mv_edge = out
    return out


# ------------------------------------------------------------ p.07 the notes beside the maps (P07.2)
def r28mv_note(B, crop, k, L, num, items, head=u"Why these streets matter"):
    """v50 (MIRAQUA 28 Oct, P07.2): a short note in the empty width right of a p.07 map whose crop is `crop` (board
    units): its heading, then items (lines with one or two **bold** keywords, G5), 9 pt (8.5, 8 where the map's
    height asks for it; the last items left out, logged, where even that does not fit). Crop drw_mv_note_<num>, as
    tall as its text, its top on the map's, drawn for its width on the booklet page (bk_w): the row map + 4 mm +
    note stays within BK_AW, so the map keeps 1:10,000."""
    wmax = BK_AW - R28MV_GUT - (crop[2] - crop[0]) / k - 0.5     # mm the row leaves for the note's crop
    nw = min(R28MV_NOTE_W, wmax - 1.0)                            # mm of text
    if nw < 30.0 or not items:
        LOG.append("Note {} beside the p.07 map not drawn (no width or nothing to say).".format(num))
        return
    hmax = crop[3] - crop[1] - 1.0 * k                            # no taller than its map's crop
    x0 = crop[2] + R28MV_GUT * k
    tx, items, fit = x0 + 0.5 * k, list(items), None
    while items and fit is None:
        for pt in (9.0, 8.5, 8.0):
            h, hh = bk_hk(pt, k), bk_hk(pt + 0.5, k)
            lines = [r28mv_lines(it, nw * k, h) for it in items]
            need = 0.5 * k + hh + (R28MV_LEAD + 0.6) * h + (sum(len(l_) for l_ in lines) - 1) * R28MV_LEAD * h + \
                (len(lines) - 1) * 0.5 * h + 0.4 * h + 0.5 * k
            if need <= hmax:
                fit = (h, hh, lines)
                break
        if fit is None:
            LOG.append(u"Note {} beside the p.07 map: \"{}\" left out (no room).".format(num, items[-1]))
            items = items[:-1]
    if fit is None:
        return
    h, hh, lines = fit
    y = crop[3] - 0.5 * k - hh
    B.text(head, tx, y, hh, INK, L, order=66, font=FONT_TITLE, bold=True)
    y -= (R28MV_LEAD + 0.6) * h
    for j, item in enumerate(lines):
        for ln in item:
            r28mv_draw_line(B, ln, tx, y, h, INK, L)
            y -= R28MV_LEAD * h
        y -= 0.5 * h
    bot = y + R28MV_LEAD * h + 0.5 * h - 0.4 * h
    crop_panel("mv_note_{}".format(num), x0, bot - 0.5 * k, x0 + (nw + 1.0) * k, crop[3], u"")
    CROP_PANELS[-1]["bk_w"] = nw + 1.0


def r28mv_note_top(S, B, crop, k, L, MV, n_pl):
    """v50 (P07.2): drw_mv_note_1, beside the top map: the shops' streets, the busiest street, shops against walking,
    the civic constellations and the services, all as the board computes and prints them on the page."""
    out = []
    prim = [g for g in getattr(S, "corr_primary", None) or [] if g["label"] != "an unnamed street"]
    if prim:
        out.append(u"**Shops** line up on {}: the primary commercial spines {}.".format(
            join_names([u"{} ({} shops)".format(g["label"], g["n"]) for g in prim]), bcite(T3_PUB_SRC)))
    sec = getattr(S, "corr_secondary", None) or []
    if sec:
        out.append(u"**{} more street{}** with 3 or more shops: the secondary spines.".format(
            len(sec), u"" if len(sec) == 1 else u"s"))
    rows = MV.get("rows") or []
    if rows:
        out.append(u"**Busiest street** on foot and by car together: {}, index {:.0f} (100 = the busiest street "
                   u"piece) {}.".format(rows[0]["name"], rows[0]["comb_b"], bcite(T3_PUB_SRC)))
    rho, big = (MV.get("rho") or {}).get("walk_b"), MV.get("big") or []
    if rho is not None and big:
        out.append(u"**Shops and walking**: Spearman {:.2f} over the {} named streets of 50 m or more (1 = the same "
                   u"order).".format(rho, len(big)))
    cl = [c_ for c_ in getattr(S, "clusters", None) or [] if any(S.F.inside(p[0], p[1]) for p in c_["P"])]
    if cl:
        out.append(u"**{} civic constellation{}** on the map: 3 or more civic or sacred places, each within 100 m of "
                   u"the next.".format(len(cl), u"" if len(cl) == 1 else u"s"))
    tot = sum((n_pl or {}).values())
    if tot:
        f, n = max(n_pl.items(), key=lambda kv: kv[1])
        lab = dict((f_, lab_) for f_, let_, c_, lab_ in WALK_FUN).get(f, f)
        out.append(u"**{} services** on the map (Overture places); the most are {} ({}).".format(tot, lab.lower(), n))
    r28mv_note(B, crop, k, L, 1, out)


def r28mv_note_today(S, R, MV, key, rows, pts, lens):
    """v50 (P07.2): the lines of drw_mv_note_2 / _3: the busiest named streets, how many of them come close to the
    stream, the index along the stream against all streets, how the network length spreads over the classes, what
    the index counts"""
    walk = key.startswith("walk")
    out = []
    if rows:
        out.append(u"**Busiest**: " + u", ".join(u"{} {:.0f}".format(r_["name"], r_[key]) for r_ in rows) + u".")
    main = r28mv_main_stream(S)
    if main and rows:
        near = [r_ for r_ in rows if pts.get(r_["name"]) and
                min(pl_dist(p[0], p[1], main, False) for p in pts[r_["name"]]) <= R28MV_NEAR_M]
        out.append(u"**{} of the {}** busiest come within {:.0f} m of the stream.".format(len(near), len(rows),
                                                                                         R28MV_NEAR_M))
    em = r28mv_edge_means(S, R).get(key)
    if em and em[0] is not None and em[1] is not None:
        out.append(u"**Along the stream** (streets within {:.0f} m of it): index {:.0f} on average, all streets on the "
                   u"map {:.0f}.".format(R28MV_EDGE_M, em[0], em[1]))
    tot = sum(lens)
    if tot > 0:
        out.append(u"**{:.0f}%** of the {} street length carries index 25 or more, {:.0f}% stays under 2.".format(
            100.0 * (lens[3] + lens[4]) / tot, u"walkable" if walk else u"drivable", 100.0 * lens[0] / tot))
    if walk:
        out.append(u"**On foot**: the shortest routes up to {:.0f} m between every building and the everyday "
                   u"destinations; 100 = the busiest piece today {}.".format(MV_OPT["r_walk"], bcite(T3_PUB_SRC)))
    else:
        out.append(u"**By car**: the shortest routes up to {:.0f} min; footways and steps are not on this map "
                   u"{}.".format(MV_OPT["t_car"] / 60.0, bcite(T3_PUB_SRC)))
    return out


T3_HEAD_PT = 10.0        # pt: a p.07 map's own heading, inside its crop (T4, G1)


def _t3_map_head(B, x, y, U, head, L):
    """T4 (30 Oct, p7 G1): a p.07 map's heading at the top of its crop (y = the crop's top); returns the y of the
    map's top edge under it"""
    k0 = 120.0 * U / BK_AW
    hh = bk_hk(T3_HEAD_PT, k0)
    B.text(head, x, y - 0.5 * k0 - hh, hh, INK, L, order=66, font=FONT_TITLE, bold=True)
    return y - 0.5 * k0 - hh - 2.0 * k0


def draw_mv_today(S, B, x, y, U, R, MV, key, title, cap):
    """v46 (Prompt 3, p.8): walking or driving today as its own map at the theme's one scale: the whole site frame at
    1:10,000, the masterplan base, the scale bar and north arrow under it. v50 (MIRAQUA 28 Oct, P07.3): the index on
    EVERY street piece of its network (mv_runs walk_b / car_b; walking-only pieces stay base street on the driving
    map), graded in five classes by colour and line weight (r28mv_class_streets), the classes in the crop's legend;
    the 5 busiest named streets named at 7 pt (draw_mv_key, P07.4); P07.2: its note beside it (drw_mv_note_2 / _3).
    T4 (30 Oct, p7): title = the map's own heading, inside its crop (G1); the names run along their streets (G3);
    the crop's legend (drawn by the booklet under the crop, M2) holds every symbol. Returns the y below its crop."""
    L = "LU_BOARD::HowPeopleUseIt"
    F = S.F
    V, k, ss, r = b_view(F, x, _t3_map_head(B, x, y, U, title, L), U)
    h = bk_hk(R28MV_LABEL_PT, k)
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 1)
    _t3_base(S, CB, V, k, L)                              # T3a: the shared basemap, simple mode (pp.07-09)
    lens = r28mv_class_streets(CB, V, mv_runs(S, R, key, F), k, L, 14)
    rows, pts = draw_mv_key(S, CB, V, R, MV, key, F, L, h, r, k)
    b_frame(B, r, k, L)
    low = b_foot(B, F, x, r[1], ss, k, L)
    crop = (x - 0.5 * k, low - 0.5 * k, r[2] + 0.5 * k, y)
    crop_panel(CROP_MV.get(key, key), crop[0], crop[1], crop[2], crop[3], cap, crop_scale(ss),
               r28mv_class_legend() + crop_legend(_t3_base_leg()))     # T3a: cap is the caller's whole caption
    if key in R28MV_NOTE_OF:
        r28mv_note(B, crop, k, L, R28MV_NOTE_OF[key], r28mv_note_today(S, R, MV, key, rows, pts, lens))
    return low - 0.5 * k


# ------------------------------------------------------------ p.08 street sections (T3a, D3 b; was p.09 the proposal map)
def draw_mv_proposal(S, B, x, y, w, U, M):
    """T3a WO-T3a-5 (29 Oct 2026, D8 b, D3 b): the proposal map (drw_proposal) and the walk / car index chart
    (drw_index_change, refs S02) are gone: the masterplan's roads, crossings, hubs and the reach on foot are drawn in
    the city link's framework diagram (bergama_city_link v4, booklet p.08). The core still calls this with the
    masterplan's movement M (only when masterplan_results.json holds it), so it now draws the before / after street
    sections per road change (_t3_street_sections, crop drw_street_sections). Returns the y below."""
    return _t3_street_sections(S, B, x, y, w, U, M)

# ------------------------------------------------------------ p.08 before / after street sections per road type (D3 b)
# T4 (30 Oct 2026; PG2 ③ "just a car, a house and a person", plain rectangles, weird hatches; D1 both, D4 a, D9; G1,
# G6, G7, G10): M8 sections. The cut ground in its hatch (sf_ground) and the lanes (sf_lane); the fronting buildings as
# real profiles (M11 bld_section_items: survey height and floors, cut walls, slabs, windows, roof) and, behind them,
# the façades further along the same street (the same survey, faded); trees behind (sf_atmosphere, D9 layers 2, 1);
# people at 1.75 m doing what the street lets them do (M7 fig_side / fig_group / fig_stall, at least three
# interactions), walkers further along (D9); speech bubbles (fig_bubble) marked "illustrative scenario" (D4); icon
# labels naming each use above the section (M9, R04); numbered callouts with their reasons (SfCallouts, R07); widths
# in cm (sf_width_label); a scale bar; the G6 check (sf_assert_g6); the legend under the drawing with the hatch itself
# (M2 Legend). v55 (Aras 31 Oct): style "a" only (cutouts placed with B.image; a missing cutout is drawn in style b),
# crop drw_street_sections; the trees behind each section fitted inside its width (_t3_trees_behind).
T3_SEC_ORDER = ("kept", "calmed", "pedestrian", "shared")   # the masterplan's road changes, one section pair each
T3_SEC_DENS = (200, 250, 500)   # the standard scales tried, largest first: two rows at most on one booklet width
T3_SEC_ROW_W = 392.0     # mm: one booklet row (BK_AW)
T3_SEC_GAP = 7.0         # mm between today and with the project
T3_SEC_PAIR_GAP = 14.0   # mm between two road types
T3_SEC_MATCH = 10.0      # m: an OSM street piece runs along a masterplan road when half its points lie this close
T3_SEC_REACH = 15.0      # m: a frontage (survey building) is looked for this far across, each side (as measure_widths)
T3_SEC_DEEP = 24.0       # m: a fronting building is followed this far back from its frontage (its real depth)
T3_SEC_BEYOND = (-16.0, -8.0, 8.0, 16.0)   # m along the street: where the façades behind the cut are looked for
T3_SEC_OPEN = 3.0        # m of ground drawn beyond the street edge where no building fronts it
T3_SEC_TREE_MIN = 6.0    # m: a street at least this wide (frontage to frontage) takes a tree in the proposal
T3_SEC_CAR = (1.80, 1.45)   # m: a car seen from the front (width, height), the drawing's symbol (no module draws cars)
T3_SEC_GROUND_M = 1.2    # m of cut ground drawn under the street (drawing rule)
# R2-B (31 Oct 2026, U24 "cut in half", Section checklist): the block must fit its booklet row whole
T3_SEC_SHOW_DEEP = 8.0   # m: a cut fronting building is drawn this far back from its frontage, then a break line
#                          (drawing rule: the street is the subject; the survey depth is kept in the data)
T3_SEC_H_MAX = 110.0     # mm: the whole crop drw_street_sections at most this tall on the booklet page (p.08 has
#                          three rows; the closing thread may change it: the log prints the height drawn)
T3_SEC_KEY_W = 100.0     # mm: the key map (M4) of where each street is cut, bottom left of the block
T3_SEC_SB_H = 4.7        # mm: a scale bar's bar and numbers under a section (draw_scalebar_bk at 7 pt)
T3_FS = 2.3              # mm: the font size of every word in the sections (6.5 pt)
T3_ICO = 4.2             # mm: an icon label's badge
T3_MK = 2.6              # mm: a numbered callout (its number 6.3 pt)
T3_COL = dict(car="A7A299", car_edge="6E675F", ink="4A3F35", ink2="7A6E60", head="8B3A3F", beyond="F2F0EC",
              beyond_edge="C9C3BA", lead="9A9086")
T3_CHANGE_TXT = dict(kept=u"kept as it is", calmed=u"calmed", pedestrian=u"made pedestrian", shared=u"shared street")
# the people of a section: footprint (m along the cut) and head height (m) of each act; who does what per street
T3_ACT = dict(adult_child=(1.0, 1.75), group=(1.8, 1.75), kerb=(0.6, 1.75), bike=(1.9, 1.80), bench=(1.0, 1.30),
              market=(2.6, 1.75), child_play=(0.8, 1.15))
T3_SCRIPT = dict(today=("adult_child", "group", "kerb", "bike"),
                 calmed=("bike", "group", "bench", "adult_child", "child_play"),
                 pedestrian=("market", "bench", "group", "child_play", "adult_child"),
                 shared=("bike", "group", "bench", "adult_child"))
T3_ACT_USE = dict(group=("people", u"Meeting"), bench=("seating", u"Seating"), market=("market", u"Market stall"),
                  bike=("bike", u"Cycling"), child_play=("people", u"Play"))
# D4 a: the bubbles caricature the situation (an illustrative scenario, never a quote); three at most per section
T3_BUBBLES = {("today", "adult_child"): u"Hold my hand,\nthe cars!",
              ("today", "group"): u"Let's talk\nsomewhere quieter.",
              ("today", "kerb"): u"Still waiting\nto cross...",
              ("today", "bike"): u"Squeezed between\ncars again.",
              ("calmed", "bike"): u"Cars at my pace,\nfor once.",
              ("calmed", "group"): u"We can hear\neach other now!",
              ("calmed", "bench"): u"A seat on this\nstreet? New.",
              ("calmed", "adult_child"): u"We cross\nwhere we like.",
              ("pedestrian", "market"): u"Two kilos,\nstraight from the stall!",
              ("pedestrian", "bench"): u"Shade, a bench,\nno engines.",
              ("pedestrian", "group"): u"Same street,\nhalf the noise.",
              ("pedestrian", "child_play"): u"Race you\nto the stream!",
              ("shared", "bike"): u"Room for me\nand the car.",
              ("shared", "group"): u"Coffee\noutside today?",
              ("shared", "bench"): u"Watching the\nstreet go by."}


def _t3_ray(g, px, py, dx, dy, reach):
    """(distance m, owner) of the nearest segment of grid g along the ray from (px, py), or (None, None)"""
    ex, ey = px + dx * reach, py + dy * reach
    best = (None, None)
    for a, b, own in g.query((min(px, ex), min(py, ey), max(px, ex), max(py, ey))):
        r = seg_x((px, py), (dx * reach, dy * reach), a, (b[0] - a[0], b[1] - a[1]))
        if r is not None and r[0] * reach > 0.3 and (best[0] is None or r[0] * reach < best[0]):
            best = (r[0] * reach, own)
    return best


def _t3_sec_grids(S):
    """the surveyed road edges and the building outlines as segment grids, once per run (S._t3_secg)"""
    got = getattr(S, "_t3_secg", None)
    if got:
        return got
    ge, gb = Grid(20.0), Grid(20.0)

    def add(g, a, b, own):
        g.add((a, b, own), (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])))
    for P in getattr(S, "road_edges", None) or []:
        for a, b in zip(P[:-1], P[1:]):
            add(ge, a, b, None)
    for u in S.bld:
        for P in u["parts"]:
            for i in range(len(P)):
                add(gb, P[i], P[(i + 1) % len(P)], u)
    S._t3_secg = (ge, gb)
    return S._t3_secg


def _t3_sec_cut(S, rd):
    """T3a (D3 b): today's street along the masterplan road rd, from the survey only: of the OSM street pieces that run
    along rd (half their points within T3_SEC_MATCH of its line), the one with a measured width (measure_widths:
    road edges first, else frontages); across its middle: the carriageway between the surveyed road edges, each
    side's frontage (survey building within T3_SEC_REACH), that building and its height (the board's building
    model). T4: + the cut point p, the street's direction t, each side's normal n and building u, and the buildings
    in section (_t3_sec_bld). None when no piece along rd has a measured width."""
    Lr = _xy_list(rd.get("xy"))
    if len(Lr) < 2:
        return None
    best = None
    for r_ in list(S.roads) + list(getattr(S, "paths", []) or []):
        P = r_["P"]
        if len(P) < 2 or not r_.get("w"):
            continue
        pts = resample(P, 4.0)
        near = sum(1 for p in pts if pl_dist(p[0], p[1], Lr, False) <= T3_SEC_MATCH)
        if near < max(2, 0.5 * len(pts)):
            continue
        key = (r_.get("w_src") == "road edges", near)
        if best is None or key > best[0]:
            best = (key, r_)
    if best is None:
        return None
    r_ = best[1]
    (px, py), (tx, ty) = pl_point_at(r_["P"], pl_length(r_["P"]) / 2.0)
    ge, gb = _t3_sec_grids(S)
    side = {}
    for sg in (-1, 1):                                    # -1 = the left of the drawing (left of the street's way)
        nx, ny = (-ty, tx) if sg < 0 else (ty, -tx)
        e_ = _t3_ray(ge, px, py, nx, ny, T3_SEC_REACH)[0]
        f_, u = _t3_ray(gb, px, py, nx, ny, T3_SEC_REACH)
        if e_ is not None and f_ is not None and e_ > f_:
            e_ = None                                     # an edge behind the frontage is another street's
        side[sg] = dict(edge=e_, front=f_, h=(float(u.get("h") or 0.0) or None) if u else None,
                        u=u if f_ is not None else None, n=(nx, ny), back=None, g6=None)
    w, src = float(r_["w"]), r_.get("w_src")
    if src == "road edges":
        a_ = side[-1]["edge"] if side[-1]["edge"] and side[1]["edge"] else w / 2.0
        b_ = side[1]["edge"] if side[-1]["edge"] and side[1]["edge"] else w / 2.0
        carriage = (-a_, b_)
    else:                                                 # the width is frontage to frontage: no carriageway measured
        carriage = None
        for sg in (-1, 1):
            if side[sg]["front"] is None:
                side[sg]["front"] = w / 2.0
    name = (r_["tags"].get("name") or u"").strip() or rd.get("name", u"")
    cut = dict(name=name, change=rd.get("change", "kept"), w=w, w_src=src, carriage=carriage, side=side,
               p=(px, py), t=(tx, ty))
    _t3_sec_bld(S, cut)
    return cut


def _t3_bld_cut(q, n, front, sg, u):
    """T4 (M11, G7): survey building u cut along the ray from q (survey m) in direction n, its frontage `front` m
    away, as bld_section_items in section m: (x across the street, side sg; z m above the street). Its height and
    floors are the survey's; the roof is the module's convention (no roof survey)."""
    d0 = max(0.0, front - 0.5)
    a = (q[0] + n[0] * d0, q[1] + n[1] * d0)
    b = (q[0] + n[0] * (front + T3_SEC_DEEP), q[1] + n[1] * (front + T3_SEC_DEEP))
    out = []
    for it in bld_section_items(a, b, [u], ground=lambda x_, y_: 0.0, label=False):
        if it[0] == "fill":
            out.append(("fill", [[(sg * (d0 + s), z) for s, z in R_] for R_ in it[1]], it[2]))
        elif it[0] == "line":
            out.append(("line", [(sg * (d0 + s), z) for s, z in it[1]], it[2], it[3], it[4]))
    return out


def _t3_sec_bld(S, cut):
    """T4: the cut's buildings in section m: each side's fronting building cut (cut["bld"], its back = side "back",
    its drawn eaves against the survey height = side "g6") and the profiles of the other buildings fronting the
    street T3_SEC_BEYOND m along it, seen behind the cut (cut["beyond"]: rings), all from the survey. v57 (Aras 31 Oct
    12:01 "no background houses"; common sf_back_buildings' rule, here on the street cut, which is no registry cut):
    cut["back"] = the other survey buildings SF_BACK_BAND m along the street the way the section looks (+t, as the key
    map's triangles), projected onto the cut: [(x from, x to m across, h m, floors, m behind)], farthest first; data
    height only (a building without one is left out), none already drawn as cut or as a façade beyond"""
    gb = _t3_sec_grids(S)[1]
    p, t = cut["p"], cut["t"]
    cutb, beyond, houses = [], [], []
    drawn = set()
    for sg in (-1, 1):
        sd = cut["side"][sg]
        if sd["u"] is not None and sd["h"]:
            its = _t3_bld_cut(p, sd["n"], sd["front"], sg, sd["u"])
            xs = [abs(q[0]) for it in its if it[0] == "fill" for R_ in it[1] for q in R_]
            if xs:
                cutb += its
                sd["back"] = max(xs)
                eav = [z for it in its if it[0] == "line" and it[2] == BLD_COL["sec_line"] for _m, z in it[1]]
                sd["g6"] = (max(eav) if eav else None, sd["h"])
        seen = set([id(sd["u"])])
        drawn.add(id(sd["u"]))
        for off in T3_SEC_BEYOND:
            q = (p[0] + t[0] * off, p[1] + t[1] * off)
            f_, u = _t3_ray(gb, q[0], q[1], sd["n"][0], sd["n"][1], T3_SEC_REACH)
            if u is None or id(u) in seen or not u.get("h"):
                continue
            seen.add(id(u))
            rs_ = [R_ for it in _t3_bld_cut(q, sd["n"], f_, sg, u) if it[0] == "fill" and
                   it[2] == BLD_COL["sec_fill"] for R_ in it[1]]
            beyond += rs_
            xs_ = [q_[0] for R_ in rs_ for q_ in R_]
            if xs_:                                       # R2-B (G7, G14): drawn as an elevation (sf_back_house)
                houses.append((min(xs_), max(xs_), float(u["h"]), u.get("floors") or None))
                drawn.add(id(u))
    back = []
    for u in S.bld:                                       # v57: the houses further down the street (sf_back_buildings)
        if id(u) in drawn or not u.get("h"):
            continue
        P_ = [q_ for R_ in u["parts"] for q_ in R_]
        if len(P_) < 3:
            continue
        dn = min((q_[0] - p[0]) * t[0] + (q_[1] - p[1]) * t[1] for q_ in P_)
        if dn < SF_BACK_BAND[0] or dn > SF_BACK_BAND[1]:
            continue
        xs_ = [(q_[0] - p[0]) * t[1] - (q_[1] - p[1]) * t[0] for q_ in P_]   # across: the right normal (ty, -tx)
        back.append((min(xs_), max(xs_), float(u["h"]), u.get("floors") or None, dn))
    back.sort(key=lambda r_: -r_[4])
    cut["bld"], cut["beyond"], cut["houses"], cut["back"] = cutb, beyond, houses, back


def _t3_sec_extent(cut):
    """(left, right) m of the drawing: each side to its fronting building's back (+ 0.5 m), else the street edge +
    T3_SEC_OPEN; and (street left, street right): frontage or edge"""
    st, ex = [], []
    for sg in (-1, 1):
        sd = cut["side"][sg]
        edge = sd["front"] if sd["front"] is not None else (
            abs(cut["carriage"][0 if sg < 0 else 1]) if cut["carriage"] else cut["w"] / 2.0)
        st.append(sg * edge)
        # R2-B: a cut building to T3_SEC_SHOW_DEEP behind its frontage (then its break line), never past its back
        ex.append(sg * (min(sd["back"], sd["front"] + T3_SEC_SHOW_DEEP) + 0.5 if sd.get("back") else
                        edge + T3_SEC_OPEN))
    return tuple(ex), tuple(st)


def _t3_clip_x(pts, x0, x1):
    """R2-B: a polyline (page mm) cut to x0 <= x <= x1: [pieces]"""
    out, cur = [], []
    for a, b in zip(pts[:-1], pts[1:]):
        dx = b[0] - a[0]
        ta, tb = 0.0, 1.0
        if abs(dx) < 1e-12:
            if not (x0 <= a[0] <= x1):
                ta, tb = 1.0, 0.0
        else:
            t0_, t1_ = (x0 - a[0]) / dx, (x1 - a[0]) / dx
            ta, tb = max(0.0, min(t0_, t1_)), min(1.0, max(t0_, t1_))
        if ta > tb:
            if len(cur) >= 2:
                out.append(cur)
            cur = []
            continue
        qa = (a[0] + dx * ta, a[1] + (b[1] - a[1]) * ta)
        qb = (a[0] + dx * tb, a[1] + (b[1] - a[1]) * tb)
        if cur and abs(cur[-1][0] - qa[0]) < 1e-9 and abs(cur[-1][1] - qa[1]) < 1e-9:
            cur.append(qb)
        else:
            if len(cur) >= 2:
                out.append(cur)
            cur = [qa, qb]
    if len(cur) >= 2:
        out.append(cur)
    return out


def _t3_break(x, y0, y1, k):
    """R2-B: an architectural break line at x from y0 to y1 (page mm): the cut building continues beyond"""
    ym, a = 0.5 * (y0 + y1), 0.35 * k
    return [("line", [(x, y0), (x, ym - a), (x - 0.5 * a, ym - 0.3 * a), (x + 0.5 * a, ym + 0.3 * a), (x, ym + a),
                      (x, y1)], SEC["ink"], 0.18)]


def _t3_car(x, gy, k, facing=1):
    """a car seen from the front, the drawing's symbol (T3_SEC_CAR, true size), its middle at x, wheels on gy"""
    w_, h_ = T3_SEC_CAR
    b0, b1, c1 = gy + 0.30 * k, gy + 0.95 * k, gy + h_ * k
    body = [(x - 0.5 * w_ * k, b0), (x + 0.5 * w_ * k, b0), (x + 0.5 * w_ * k, b1), (x + 0.36 * w_ * k, c1),
            (x - 0.36 * w_ * k, c1), (x - 0.5 * w_ * k, b1)]
    out = [("poly", body, T3_COL["car"], T3_COL["car_edge"], 0.13)]
    for sx in (-0.36, 0.36):
        out.append(("poly", [(x + (sx - 0.08) * w_ * k, gy), (x + (sx + 0.08) * w_ * k, gy),
                             (x + (sx + 0.08) * w_ * k, b0), (x + (sx - 0.08) * w_ * k, b0)], T3_COL["ink"], None, 0.0))
    return out


def _t3_take(f, zones, occ, prefer):
    """the left end (m) of a free stretch f m long in zones [(a, b)], clear of occ (grows), nearest prefer"""
    cands = []
    for a, b in zones:
        x = a + 0.15
        while x + f <= b - 0.15 + 1e-9:
            cands.append(x)
            x += 0.2
    cands.sort(key=lambda c_: abs(c_ + 0.5 * f - prefer))
    for c_ in cands:
        if all(c_ + f <= o0 or c_ >= o1 for o0, o1 in occ):
            occ.append((c_ - 0.25, c_ + f + 0.25))
            return c_
    return None


def _t3_shift(shapes, dx, dy):
    """house shapes moved by (dx, dy) mm"""
    out = []
    for s_ in shapes:
        t = s_[0]
        if t in ("poly", "line"):
            out.append((t, [(p[0] + dx, p[1] + dy) for p in s_[1]]) + tuple(s_[2:]))
        elif t == "text":
            out.append((t, s_[1], s_[2] + dx, s_[3] + dy) + tuple(s_[4:]))
        elif t == "image":
            out.append((t, s_[1] + dx, s_[2] + dy) + tuple(s_[3:]))
    return out


def _t3_top(shapes):
    """the highest y (mm) the shapes reach"""
    ys = [0.0]
    for s_ in shapes:
        if s_[0] in ("poly", "line"):
            ys += [p[1] for p in s_[1]]
        elif s_[0] == "text":
            ys.append(s_[3] + s_[4])
        elif s_[0] == "image":
            ys.append(s_[2] + s_[4])
    return max(ys)


def _t3_xext(shapes):
    """(lowest x, highest x) mm the shapes reach (poly, line, image); (0, 0) for none"""
    xs = []
    for s_ in shapes:
        if s_[0] in ("poly", "line"):
            xs += [p[0] for p in s_[1]]
        elif s_[0] == "image":
            xs += [s_[1], s_[1] + s_[3]]
    return (min(xs), max(xs)) if xs else (0.0, 0.0)


def _t3_trees_behind(W, k, seed, style):
    """v55 (Aras 31 Oct, p8: trees cut off at the page edge): the depth trees behind a section, planted in a band
    narrowed until every crown lies inside 0..W mm (at most 4 tries; the last try's trees are kept). R2-B (31 Oct,
    G9, D9, Aras 11:24 colour depth): mixed groups (plants.py pla_group_section: plane, ash, chaste tree, never rows
    or one species alone) in D9 layers 2 and 1 (farther = smaller and paler), style a cutouts, each seated on the
    street level (G14). Returns the shapes."""
    a_, b_, sh = 0.0, W, []
    for _t in range(4):
        sh, _pl, _gr = pla_group_section(a_, b_, 0.0, k, t0=0.45, t1=0.60, mix={"plane": 1.0, "ash": 1.0,
                                                                                 "chaste": 0.8},
                                         seed=seed, layers=(2, 1), style=style, density=0.45, hires=False,
                                         detail=False)
        lo, hi = _t3_xext(sh)
        if not sh or (lo >= -0.05 and hi <= W + 0.05):
            break
        a_, b_ = a_ + max(0.0, -lo), b_ - max(0.0, hi - W)
        if b_ <= a_:
            return []
    return sh


def _t3_badge(ico, cx, cy, size):
    """an icon label's badge: M9 ico_badge, or the drawing's car on the same plate (icons.py has no car)"""
    if ico == "car":
        return [("poly", sec_ellipse(cx, cy, 0.5 * size, 0.5 * size, 28), ICO_PAL["paper"], None, 0.0)] + \
            _t3_car(cx, cy - 0.27 * size, 0.5 * size / T3_SEC_CAR[1])
    return ico_badge(ico, cx, cy, size)


def _t3_icon_row(uses, x0, W, yc, gy):
    """R04: the uses of one section as icon labels in a row above it (centre height yc), each named, spread so no two
    touch, each on a thin leader to its zone (target y above the ground gy). Returns (badges and names, leaders)."""
    kd = kind_of(FONT_TITLE)
    its = sorted(uses, key=lambda u_: u_[2])
    wid = [max(T3_ICO, tw(lab, T3_FS * R28MV_CAP, kd)) for _i, lab, _x, _y in its]
    xs = [x0 + u_[2] for u_ in its]
    for i in range(1, len(xs)):
        xs[i] = max(xs[i], xs[i - 1] + 0.5 * (wid[i - 1] + wid[i]) + 1.2)
    if xs and xs[-1] + 0.5 * wid[-1] > x0 + W:
        xs[-1] = x0 + W - 0.5 * wid[-1]
        for i in range(len(xs) - 2, -1, -1):
            xs[i] = min(xs[i], xs[i + 1] - 0.5 * (wid[i] + wid[i + 1]) - 1.2)
    sh, lead = [], []
    for (ico, lab, tx_, ty_), cx in zip(its, xs):
        sh += _t3_badge(ico, cx, yc, T3_ICO)
        sh.append(("text", lab, cx, yc + 0.5 * T3_ICO + 0.8, T3_FS, T3_COL["ink"], False, "C"))
        tgt = (x0 + tx_, gy + ty_ + 0.3)
        lead += [("line", [(cx, yc - 0.5 * T3_ICO), tgt], T3_COL["lead"], 0.1),
                 ("poly", sec_ellipse(tgt[0], tgt[1], 0.35, 0.35, 10), T3_COL["lead"], None, 0.0)]
    return sh, lead


def _t3_sec_make(cut, after, style, k, CO, seed):
    """T4: one section of cut (today, or with the project when after) in style "b" / "a": page mm, its left edge at
    x 0, the street surface at y 0, k mm per m. Returns dict(wl = its WaterLayers draw list, w = width mm, uses =
    [(icon, name, x, y target)], acts = the interactions drawn, low = the lowest y used, g6 = G6 messages, tree)."""
    (xl, xr), (sl, sr) = _t3_sec_extent(cut)
    X = lambda m: (m - xl) * k
    W = (xr - xl) * k
    ch = cut["change"]
    var = ch if after and ch != "kept" else "today"
    one = var in ("calmed", "pedestrian", "shared")
    width, mid = sr - sl, 0.5 * (sl + sr)
    gm = T3_SEC_GROUND_M
    kd = kind_of(FONT_TITLE)
    wl = water_layers()
    # behind the cut (D9): trees, the façades further along the street (survey), walkers further along
    wl.add("background", _t3_trees_behind(W, k, seed, style))   # v55: whole crowns inside the section width
    # R2-B (G7, G14): the buildings further along the street as elevations (sf_back_house: walls at the survey
    # height, windows per storey, hipped roof by convention), standing on the street level (flat back profile)
    hs_ = [(max(0.3 * k, X(xa_)), min(W - 0.3 * k, X(xb_)), h_, fl_) for xa_, xb_, h_, fl_ in cut.get("houses") or []]
    hs_ = [q_ for q_ in hs_ if q_[1] - q_[0] >= 1.0 * k]
    prof = sf_back_profile([(xa_, xb_, 0.0) for xa_, xb_, _h, _f in hs_], 0.0, W)
    for xa_, xb_, h_, fl_ in sorted(hs_, key=lambda q_: -q_[2]):
        wl.add("background", sf_back_house(xa_, xb_, prof or 0.0, h_, k, layer=1, floors=fl_ or None))
    # the ground and the lanes: carriageway and footways today, one paved level with the project
    if one or not cut["carriage"]:
        lanes = [(sl, sr, "walk")]
    else:
        c0, c1 = cut["carriage"]
        lanes = [(a_, b_, kn) for a_, b_, kn in ((sl, c0, "walk"), (c0, c1, "road"), (c1, sr, "walk")) if b_ - a_ > 0.05]
    sf_ground([(0.0, 0.0), (W, 0.0)], k, depth_m=gm, into=wl)
    for a_, b_, kn in lanes:
        wl.add("ground", sf_lane(X(a_), 0.0, b_ - a_, k, kind=kn))
    # the fronting buildings, cut (M11, survey heights); R2-B: kept inside the drawing, a break line where they go on
    bsh, brk = [], {}
    for it in cut["bld"]:
        if it[0] == "fill":
            for R_ in it[1]:
                ring = clip_rect_poly([(X(m), z * k) for m, z in R_], (0.0, -1e6, W, 1e6))
                if len(ring) >= 3:
                    bsh.append(("poly", ring, it[2], None, 0.0))
                for m, z in R_:
                    for e_, out in ((0.0, X(m) < -0.01), (W, X(m) > W + 0.01)):
                        if out:
                            brk[e_] = max(brk.get(e_, 0.0), z * k)
        else:
            for q_ in _t3_clip_x([(X(m), z * k) for m, z in it[1]], 0.0, W):
                bsh.append(("line", q_, it[2], it[3]) + ((it[4],) if it[4] else ()))
    for e_, ht_ in brk.items():
        bsh += _t3_break(e_, 0.0, ht_, k)
    wl.add("structures", bsh)
    marks, uses, occ, cars = [], [], [], []
    for sg in (-1, 1):
        sd = cut["side"][sg]
        if sd.get("back"):
            xm_ = min(W - 1.0, max(1.0, X(sg * 0.5 * (sd["front"] + min(sd["back"], sd["front"] + T3_SEC_SHOW_DEEP)))))
            marks.append((xm_, u"Building, cut: {} high, as surveyed".format(u_height(sd["h"])) if sd.get("h") else
                          u"Building, cut: as surveyed"))
    road = []
    if var == "today":
        if cut["carriage"]:
            c0, c1 = cut["carriage"]
            n = max(1, min(2, int((c1 - c0) // 3.0)))
            cars = [c0 + (c1 - c0) * (j + 0.5) / n for j in range(n)]
            zones, road = [(sl, c0), (c1, sr)], [(c0, c1)]
            uses.append(("car", u"Cars", X(0.5 * (c0 + c1)), T3_SEC_CAR[1] * k))
            marks.append((X(0.5 * (c0 + c1)), u"Carriageway: the middle of the street belongs to cars"))
            for a_, b_ in zones:
                if b_ - a_ >= 0.5:
                    uses.append(("walk", u"Footway", X(0.5 * (a_ + b_)), 0.0))
                    marks.append((X(0.5 * (a_ + b_)), u"Footway: what is left for people"))
        else:
            zones = [(sl, sr)]
            uses.append(("walk", u"Street", X(mid), 0.0))
    else:
        zones = [(sl, sr)]
        uses.append(("walk", u"One level for people", X(sl + 0.15 * width), 0.0))
        marks.append((X(sl + 0.15 * width), u"One level, no kerb: people cross anywhere"))
        if var == "calmed":
            c0, c1 = cut["carriage"] or (sl + 0.25 * width, sr - 0.25 * width)
            cars = [c0 + 0.3 * (c1 - c0)]
        elif var == "shared":
            cars = [sl + 0.62 * width]
        if cars:
            uses.append(("car", u"Slow cars", X(cars[0]), T3_SEC_CAR[1] * k))
            marks.append((X(cars[0]), u"Cars pass at walking pace"))
    for cx in cars:
        wl.add("figures", sf_seat(_t3_car(X(cx), 0.0, k), 0.0))   # G14: wheels on the street
        occ.append((cx - 1.1, cx + 1.1))
    # R2-B (G9): the project's planting where the street leaves room: one mixed group (plants.py pla_group_section,
    # street species of the dry band: plane, ash, chaste tree, rosemary, lavender; heights inside their sourced
    # ranges, crowns overlapping, never one species alone), on a planting strip clear of the cars; what it does from
    # the species' purpose tags (project sources only)
    tx, trees, ptags = None, [], []
    if var in ("pedestrian", "shared") and width >= T3_SEC_TREE_MIN:
        p0, p1 = (mid - 0.20 * width, mid + 0.20 * width) if var == "pedestrian" else \
            (sl + 0.08 * width, sl + 0.42 * width)
        sh_, placed, grp = pla_group_section(X(p0), X(p1), 0.0, k, t0=0.50, t1=0.85,
                                             mix={"plane": 1.0, "ash": 0.6, "chaste": 1.0, "rosemary": 0.8,
                                                  "lavender": 0.8}, seed=seed, layers=(0,), style=style,
                                             density=0.8, avoid=[(X(c_ - 1.1), X(c_ + 1.1)) for c_ in cars])
        if placed:
            wl.add("vegetation", sh_)
            trees += [q_ for q_ in placed if _pla_canopy(q_[0])]
            can = [q_ for q_ in placed if _pla_canopy(q_[0])] or placed
            tq = max(can, key=lambda q_: q_[2])
            tx = tq[1] / k + xl
            for q_ in placed:
                if _pla_canopy(q_[0]):
                    occ.append((q_[1] / k + xl - 0.35, q_[1] / k + xl + 0.35))
            ptags = sorted(set(t_ for g_ in grp for t_ in g_[4]))
            uses.append(("shade" if "shade" in ptags else "people", u"Planting", X(tx), tq[2] * k))
        else:
            LOG.append(u"Street sections {}: no planting group fits the {:.1f} m strip.".format(cut["name"], p1 - p0))
    # walkers further along the street (D9 layers 2 and 1: smaller, paler; Aras 31 Oct 11:24 colour depth by
    # distance), by what each zone is for (figures.py fig_place_zones, style a cutouts only, seated: G14, G10)
    # v57 (R2-C focus, Aras 31 Oct 12:01): those who stay look at each other (their zone's middle), walkers keep on
    zk = "market_ground" if var == "pedestrian" else "walkway"
    for lay in (2, 1):
        sh_, _pl = fig_place_zones([(zk, X(a_), X(b_)) for a_, b_ in zones if b_ - a_ >= 1.5], 0.0, k,
                                   seed=seed + 5 * lay, layer=lay, style="a", density=0.5, max_per_zone=2,
                                   focus=lambda _k, xa_, xb_: 0.5 * (xa_ + xb_))
        wl.add("background", sh_)
    # the people at the cut (1.75 m): the street's interactions (G10)
    script = T3_SCRIPT[var]
    acts, bub = [], []
    for i, act in enumerate(script):
        f, head = T3_ACT[act]
        zs = road if (act == "bike" and var == "today") else zones
        if not zs:
            continue
        if act == "kerb" and cut["carriage"]:
            prefer = cut["carriage"][0] - 0.5 * f - 0.2
        elif act == "bench" and tx is not None:
            prefer = tx + 0.4 + 0.5 * f
        elif act == "bike" and var == "today":
            prefer = 0.5 * (zs[0][0] + zs[0][1])
        else:
            prefer = sl + width * (i + 0.5) / len(script)
        a_ = _t3_take(f, zs, occ, prefer)
        if a_ is None:
            continue
        cx = a_ + 0.5 * f
        fac = 1 if cx < mid else -1
        hx = X(cx)
        if act == "group":
            sh_ = fig_group(X(cx), 0.0, k, n=3, seed=seed + i, style="a")
        elif act == "bench":
            an = fig_meta("sit_step", fac, seat_h=SF_SEAT_H)
            sh_ = sf_bench(X(cx) + float(an.get("seat_x", 0.15 * fac)) * k, 0.0, k, side=-fac) + \
                fig_side("sit_step", X(cx), 0.0, k, facing=fac, style=style, pick=seed + i, seat_h=SF_SEAT_H)
            marks.append((X(cx), u"Bench here because the planting gives shade" if tx is not None and
                          "shade" in ptags else u"Bench: a place to stop on the way"))
        elif act == "market":
            xf = X(a_ + 1.45) if fac > 0 else X(a_ + f - 1.45)
            sh_ = fig_stall(xf, 0.0, k, facing=fac, style=style, seed=seed + i)
            hx = xf + fac * 0.45 * k
            marks.append((X(cx), u"Market stall: trade moves into the street"))
        else:
            sh_ = fig_side({"kerb": "watch"}.get(act, act), X(cx), 0.0, k, facing=fac, style=style, pick=seed + i)
        wl.add("figures", sf_seat(sh_, 0.0, sink=True))   # G14: feet, stall legs, bench on the street level
        acts.append(act)
        bub.append((act, hx, head * k, fac))
        if act in T3_ACT_USE:
            uses.append(T3_ACT_USE[act] + (X(cx), head * k))
    if tx is not None:
        word = dict(shade=u"shade", corridor=u"a green link", perception=u"scent and colour", wind=u"cuts wind",
                    noise=u"cuts street noise", cleaning=u"cleans water")
        marks.append((X(tx), u"Mixed planting here because it gives {}".format(
            u", ".join(word.get(t_, t_) for t_ in ptags)) if ptags else u"Mixed planting: street greenery"))
    # D4 a: speech bubbles, toward the street's middle, never on each other or off the drawing
    wfn = lambda s, size: tw(s, size * R28MV_CAP, kd)
    boxes = []
    for act, hx, hy, fac in bub:
        t_ = T3_BUBBLES.get((var, act))
        if not t_ or len(boxes) >= 3:
            continue
        for sd_ in (fac, -fac):
            sh_ = fig_bubble(t_, hx, hy + 0.25 * k, size=T3_FS, side=sd_, width_fn=wfn)
            bb = _t3_bb(sh_[0][1])
            if bb[0] < 0.0 or bb[2] > W or any(bb[0] < q[2] and q[0] < bb[2] and bb[1] < q[3] and q[1] < bb[3]
                                               for q in boxes):
                continue
            boxes.append(bb)
            wl.add("labels", sh_)
            break
    # R07: numbered callouts in the cut ground (one number per element, its reason in the key)
    r_ = 0.75 * T3_MK
    ym = -0.55 * gm * k
    marks.sort(key=lambda m_: m_[0])
    xs = [m_[0] for m_ in marks]
    for i in range(1, len(xs)):
        xs[i] = max(xs[i], xs[i - 1] + 2.0 * r_ + 0.5)
    if xs and xs[-1] > W - r_:
        xs[-1] = W - r_
        for i in range(len(xs) - 2, -1, -1):
            xs[i] = min(xs[i], xs[i + 1] - 2.0 * r_ - 0.5)
    for (mx, txt), x_ in zip(marks, xs):
        n_ = CO.add(x_, ym, txt)
        wl.add("labels", [("poly", sec_ellipse(x_, ym, r_, r_, 20), "FFFFFF", SEC["ink"], 0.15),
                          ("text", u"%d" % n_, x_, ym - 0.36 * T3_MK, 0.85 * T3_MK, SEC["ink"], True, "C")])
    # widths in cm, as surveyed: the lanes (where the number fits), then the street frontage to frontage
    yw = -gm * k - 2.6
    rows_w = [(a_, b_) for a_, b_, _kn in lanes] if len(lanes) > 1 else []
    for a_, b_ in rows_w:
        sh_ = sf_width_label(X(a_), X(b_), yw, b_ - a_, size=T3_FS)
        if tw(sh_[-1][1], T3_FS * R28MV_CAP, kd) > (b_ - a_) * k - 0.4:
            sh_ = sh_[:-1]                                # too narrow for its number: the dimension line only
            LOG.append(u"Street sections {}: the {:,.0f} cm lane is too narrow on the page for its width; only the "
                       u"street's total is written.".format(cut["name"], (b_ - a_) * 100.0))
        wl.add("labels", sh_)
    ys = yw - (3.6 if rows_w else 0.0)
    wl.add("labels", sf_width_label(X(sl), X(sr), ys, sr - sl, size=T3_FS))
    g6 = sf_assert_g6(k, trees=trees, buildings=[(u"{} side {}".format(cut["name"], sg),
                                                   cut["side"][sg]["g6"][0], cut["side"][sg]["g6"][1])
                                                  for sg in (-1, 1) if cut["side"][sg].get("g6") and
                                                  cut["side"][sg]["g6"][0] is not None], strict=False)
    # v57 (Aras 31 Oct 12:01 "no background houses"; M8, D9, G14): the houses further down the street (cut["back"]),
    # farthest first and behind everything else of the background layer, as elevations (sf_back_house: data height,
    # windows, hipped roof by convention) standing on the street level (the flat back profile, as above), D9 layer 1
    # nearer than the band's middle, else 2 (paler); a house whose roof would rise over the drawing is left out (R2-C),
    # so the row height, the icon row and the labels stay where they were
    top_ = _t3_top(wl.shapes())
    dmid = 0.5 * (SF_BACK_BAND[0] + SF_BACK_BAND[1])
    bk_, nb_ = [], 0
    for xa_, xb_, h_, fl_, d_ in cut.get("back") or []:
        a_, b_ = max(0.3 * k, X(xa_)), min(W - 0.3 * k, X(xb_))
        if b_ - a_ < 2.0 * k:
            continue
        hh_ = sf_back_house(a_, b_, 0.0, h_, k, layer=1 if d_ < dmid else 2, floors=fl_)
        if not hh_ or _t3_top(hh_) > top_:
            continue
        bk_ += hh_
        nb_ += 1
    wl.L["background"][:0] = bk_
    if not after:
        LOG.append(u"Street sections {}: {} background houses {:.0f}-{:.0f} m down the street drawn ({} in the band; "
                   u"higher than the drawing left out).".format(cut["name"], nb_, SF_BACK_BAND[0], SF_BACK_BAND[1],
                                                                 len(cut.get("back") or [])))
    # D8 (default a: every section): the designed sky behind it, from the street level to the top of the drawing
    if SF_SKY_DEFAULT == "designed":
        wl.add("atmosphere", sf_sky(0.0, W, 0.0, _t3_top(wl.shapes()) + 1.0, seed=seed))
    return dict(wl=wl, w=W, uses=uses, acts=acts, low=ys - 1.5, g6=g6, tree=tx is not None)


def _t3_swatch(kind, b, k):
    """a legend swatch (page mm box b) drawn as the section draws it"""
    x0, y0, x1, y1 = b
    w, h, cx = x1 - x0, y1 - y0, 0.5 * (x0 + x1)
    ring = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    if kind == "road":
        return [("poly", ring, SF_LANE["road"], SCT["cut"], 0.15)]
    if kind == "walk":
        return sf_lane(x0, y1, w / k, k, kind="walk", t_m=h / k)
    if kind == "earth":
        return sct_hatch_fill(ring, "earth", k, SCT["cut"], 0.15)
    if kind == "bld":
        return [("poly", ring, BLD_COL["sec_fill"], BLD_COL["sec_cut"], BLD_LW["sec_cut"])]
    if kind == "beyond":                                  # R2-B: as the section draws them (sf_back_house)
        return sf_back_house(x0 + 0.1 * w, x1 - 0.1 * w, y0, 0.75 * h / k, k, layer=1, floors=1)
    if kind == "break":
        return _t3_break(cx, y0, y1, h / 1.2)
    if kind == "car":
        return _t3_car(cx, y0, h / T3_SEC_CAR[1])
    if kind == "person":                                  # R2-B (Aras 31 Oct 11:24): one human style, cutouts
        return fig_side("stand", cx, y0, h / FIG_ADULT_H, style="a")
    if kind == "far":
        return fig_side("stand", cx, y0, h / FIG_ADULT_H, layer=1, style="a")
    if kind == "tree":
        return pla_section("plane", cx, y0, h / float((PLA_SPECIES.get("plane") or {}).get("h_m") or 15.0),
                           hires=False, detail=False)
    if kind == "bubble":
        return [("poly", sec_ellipse(cx, 0.5 * (y0 + y1), 0.5 * w, 0.5 * h, 20), "FFFFFF", T3_COL["ink"], 0.15)]
    return []


def _t3_sec_id(i):
    """R2-B: the key map name of the i-th street cut (R1, R2 ...: R = road; the stream sections are S1-S8)"""
    return u"R%d" % (i + 1)


def _t3_sec_ends(cut):
    """R2-B (M4): the cut's two ends in survey m, end1 = the drawing's left end (left of the street's way), so the
    section looks along the street (basemap_cut_items look +1)"""
    (xl, xr), _st = _t3_sec_extent(cut)
    p, nl, nr = cut["p"], cut["side"][-1]["n"], cut["side"][1]["n"]
    return (p[0] + nl[0] * -xl, p[1] + nl[1] * -xl), (p[0] + nr[0] * xr, p[1] + nr[1] * xr)


def _t3_sec_key(S, B, x, yt, wmm, kb, groups, L):
    """R2-B (U24 "show where it is cut", M4, D11): the key map of the street sections: the site frame on the M3 key
    base (basemap keymap_items, study area always shown), ONLY these cuts (basemap_cut_items: the line, a triangle
    at each end the way the section looks, the end names R1 / R1'), names placed by M2 lp_place, a heading and the
    north arrow beside it; no scale bar (a key map). x, yt board units (top left), wmm wide. Returns its height mm."""
    F = S.F
    hh = bk_hk(7.5, kb)
    B.text(u"Where each street is cut", x, yt - hh, hh, INK, L, order=66, font=FONT_TITLE, bold=True)
    y0 = yt - hh - 1.5 * kb
    mw = (wmm - 9.0) * kb
    ssk = mw / F.w
    mh = F.h * ssk
    V = View(F, ssk, x, y0)
    r = (x, y0 - mh, x + mw, y0)
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 30)

    def col_(hx, al):
        c_ = C(hx) if isinstance(hx, str) else hx
        return mix(WHITE, c_, 1.0 if al is None else al)

    def fill_fn(rings, hx, al, nz):
        CB.fill(rings, col_(hx, al), L, 31)

    def line_fn(pts, hx, wmm_, dash, al, order=32):
        for d_ in (r28_pattern(pts, [m_ * kb for m_ in dash]) if dash else [pts]):
            CB.line(d_, col_(hx, al), L, order, bk_lw(wmm_ or 0.1, kb))
    den_k = 1000.0 * kb / ssk
    try:
        items = keymap_items((), scale_den=den_k, box=F.bb, mode="key")["items"]
    except Exception as e:
        items = None
        LOG.append(u"Street sections key map: no basemap ({}).".format(e))
    if items:
        basemap_draw(items, lambda p: V.p(p[0], p[1]), fill_fn, line_fn)
    else:
        for wt in S.water:
            CB.fill(V.Ps([wt["P"]] + wt.get("H", [])), BLUE_L, L, 31)
        draw_r28_study(S, CB, V, kb, L, order=38)
    cuts = []
    for i, c_ in enumerate(groups):
        a, b = _t3_sec_ends(c_)
        cuts.append((a, b, (_t3_sec_id(i), _t3_sec_id(i) + u"'")))
    ci = basemap_cut_items(cuts, den_k, frame=list(F.P), tri_mm=2.4, text_mm=2.8, col="4A3F35")
    basemap_draw([it for it in ci if it[0] != "text"], lambda p: V.p(p[0], p[1]),
                 lambda rings, hx, al, nz: CB.fill(rings, col_(hx, al), L, 39),
                 lambda pts, hx, wmm_, dash, al: line_fn(pts, hx, wmm_, dash, al, 39), None)
    tx_ = [it for it in ci if it[0] == "text"]
    lines_ = [[(q[0] / kb, q[1] / kb) for q in (V.p(*it[1][0]), V.p(*it[1][1]))] for it in ci if it[0] == "line"]
    obst = []
    for it in ci:
        if it[0] == "fill":
            qs = [V.p(*q) for R_ in it[1] for q in R_]
            obst.append((min(q[0] for q in qs) / kb, min(q[1] for q in qs) / kb, max(q[0] for q in qs) / kb,
                         max(q[1] for q in qs) / kb))
    labs = []
    for it in tx_:
        h_ = it[3] * 0.718 * kb
        q = V.p(*it[2])
        labs.append(dict(x=q[0] / kb, y=q[1] / kb, w=site28_tw(it[1], h_, True) / kb, h=h_ / kb, rank=0, r=0.0))
    got = lp_place(labs, obstacles=obst, lines=lines_, bounds=(r[0] / kb, r[1] / kb, r[2] / kb, r[3] / kb),
                   max_leader=6.0) if labs else []
    for it, lb, pl in zip(tx_, labs, got):
        if not pl:
            LOG.append(u"Street sections key map: no room for the end name {}.".format(it[1]))
            continue
        bx0, by0, bx1, by1 = pl["box"]
        CB.text(it[1], 0.5 * (bx0 + bx1) * kb, 0.5 * (by0 + by1) * kb, lb["h"] * pl["size"] * kb, col_(it[4], None),
                L, order=42, font=FONT_TITLE, bold=True, align="MC")
        if pl["leader"]:
            CB.line([(pl["leader"][0][0] * kb, pl["leader"][0][1] * kb),
                     (pl["leader"][1][0] * kb, pl["leader"][1][1] * kb)], col_(it[4], None), L, 42, bk_lw(0.1, kb))
    B.line(rect(*r) + [(r[0], r[1])], INK2, L, 40, bk_lw(0.15, kb))
    draw_north_at(B, F, r[2] + 4.5 * kb, y0 - 4.0 * kb, 4.0, kb, L)
    return (yt - r[1]) / kb


def _t3_sec_dry(groups, den, rows, style):
    """R2-B: the height (mm) the block takes at 1:den in these rows, made once without drawing (the section makes
    are thrown away; the log, the G14 counts and the callouts are left as they were)"""
    import copy as _cp
    k = 1000.0 / den
    n_log, g14 = len(LOG), _cp.deepcopy(SF_G14)
    h = 13.0
    try:
        for ri, row in enumerate(rows):
            tops, lows = [], []
            for gi, c_ in enumerate(row):
                for j in range(1 if c_["change"] == "kept" else 2):
                    sec = _t3_sec_make(c_, j == 1, style, k, SfCallouts(), 17 * ri + 5 * gi + j)
                    tops.append(_t3_top(sec["wl"].shapes()))
                    lows.append(sec["low"])
            h += 7.5 + T3_FS + T3_ICO + 3.0 + max(tops) - min(lows) + T3_SEC_SB_H + 4.0
    finally:
        del LOG[n_log:]
        SF_G14.clear()
        SF_G14.update(g14)
    return h


def _t3_sec_block(S, B, x, y, kb, groups, den, rows, style, L):
    """T4: every street section in style "b" or "a" from the top y (board units) down: title, rows of sections
    (heading, today / with the project, icon labels, the section, widths, scale bar), then the legend (M2) and the
    numbered callouts' key under it. R2-B (31 Oct, U24, Section checklist): the meaningless triangles off while it
    draws (sf_triangles); each pair headed with its key map name (R1 ...); under the rows one band: the key map of
    where each street is cut (_t3_sec_key), the legend in columns beside it, then the callouts' key in two columns,
    so the whole block stays short enough for its booklet row. Returns (the y below, the width used mm)."""
    k = 1000.0 / den                                      # mm per m on the booklet page
    PU = _T3Put(B, x, 0.0, kb, L)
    CO = SfCallouts()
    old_tri = sf_triangles(walls=False, aggregate=False)  # G14 / U22: no meaningless triangles in these sections
    ytop = y / kb                                         # mm
    PU.text(u"The same surveyed width, given back to people: each street today and with the project", 0.0,
            ytop - 4.0, 11.0, T3_COL["ink"], True)
    PU.text(u"Speech bubbles: {} · widths in cm as surveyed: the lanes, then the street from frontage to "
            u"frontage".format(FIG_BUBBLE_TAG.lower()), 0.0, ytop - 8.5, 7.0, T3_COL["ink2"], False)
    yrow = ytop - 13.0
    xmax, g6, tree = 0.0, [], False
    o_lead = 40 + 2 * WAT_LAYERS.index("figures") - 1     # leaders over trees and buildings, under the people
    gid = dict((id(c_), i) for i, c_ in enumerate(groups))
    for ri, row in enumerate(rows):
        made = []
        for gi, c_ in enumerate(row):
            n = 1 if c_["change"] == "kept" else 2
            for j in range(n):
                made.append((c_, j, n, _t3_sec_make(c_, j == 1, style, k, CO, 17 * ri + 5 * gi + j)))
        top = max(_t3_top(s_["wl"].shapes()) for _c, _j, _n, s_ in made)
        gy = yrow - 7.5 - (T3_FS + T3_ICO + 3.0) - top    # this row's street surface (mm)
        yc = gy + top + 2.0 + 0.5 * T3_ICO
        cx, low = 0.0, gy
        for c_, j, n, sec in made:
            if j == 0:
                PU.text(u"{} · {} · {}".format(_t3_sec_id(gid[id(c_)]), c_["name"],
                                               T3_CHANGE_TXT.get(c_["change"], c_["change"])), cx, yrow - 3.0,
                        8.5, T3_COL["head"], True)
            sub = u"today = with the project" if n == 1 else (u"with the project" if j == 1 else u"today")
            PU.text(sub, cx, yrow - 6.5, 7.0, T3_COL["ink2"], False)
            ico, lead = _t3_icon_row(sec["uses"], cx, sec["w"], yc, gy)
            for li, lay in enumerate(WAT_LAYERS):
                PU.put(_t3_shift(sec["wl"].L[lay], cx, gy), 40 + 2 * li)
            PU.put(lead, o_lead)
            PU.put(ico, 60)
            sb = draw_scalebar_bk(B, x + cx * kb, (gy + sec["low"]) * kb, k * kb, 5.0 if den <= 250 else 10.0, kb, L)
            low = min(low, sb / kb)
            g6 += sec["g6"]
            tree = tree or sec["tree"]
            if len(set(sec["acts"])) < 3:
                LOG.append(u"Street sections {} ({}): only {} interaction(s) fit the surveyed width: {}.".format(
                    c_["name"], sub, len(set(sec["acts"])), u", ".join(sec["acts"]) or u"none"))
            cx += sec["w"] + (T3_SEC_GAP if j < n - 1 else T3_SEC_PAIR_GAP)
        xmax = max(xmax, cx - T3_SEC_PAIR_GAP)
        yrow = low - 4.0
    sf_triangles(**old_tri)
    if g6:
        LOG.append(u"WARNING: street sections, G6 check: " + u"; ".join(sorted(set(g6))))
    # the band under the rows: key map | legend (M2: attached to the drawing, every symbol, the hatch itself) | key
    kd = kind_of(FONT_TITLE)
    kw = min(T3_SEC_KEY_W, max(60.0, 0.30 * xmax))
    kh = _t3_sec_key(S, B, x, (yrow + 1.0) * kb, kw, kb, groups, L)
    lx0 = kw + 6.0
    ent = []
    for n_, _x, _y, t_ in sorted(CO.items):
        if not ent or ent[-1][0] != n_:
            ent.append((n_, t_))
    cw = max([tw(t_, T3_MK * R28MV_CAP, kd) for _n, t_ in ent] or [0.0]) + 2.0 * T3_MK + 3.0
    ncol = 2 if len(ent) > 1 else 1
    lw_ = max(70.0, min(0.45 * xmax, max(xmax, T3_SEC_ROW_W) - lx0 - 6.0 - ncol * cw))
    lg = Legend((lx0, yrow + 2.0, lx0 + lw_, ytop), side="below", y_down=False, gap=2.0)
    for lab, kn in ((u"Carriageway", "road"), (u"Paving: footway, one-level street", "walk"), (u"Ground, cut", "earth"),
                    (u"Building, cut: surveyed height and floors", "bld"),
                    (u"Break line: the building goes on", "break"),
                    (u"Buildings further along the street", "beyond"), (u"Car", "car"),
                    (u"Person, 1.75 m at the cut", "person"),
                    (u"People and trees further along: smaller, paler", "far")) + \
            (((u"Mixed planting: street species", "tree"),) if tree else ()) + \
            ((u"Speech bubble: " + FIG_BUBBLE_TAG.lower(), "bubble"),):
        lg.add(lab, kn)
    lay_ = lg.layout(lambda s, pt, b: tw(s, bk_hk(pt, 1.0), kd), size_pt=7.0)
    for e in lay_["rows"]:
        PU.put(_t3_swatch(e["kind"], e["swatch"], k), 62)
        PU.text(e["label"], e["text"][0], e["text"][1], e["size_pt"], T3_COL["ink"], False)
    # the numbered callouts' key in two columns right of the legend (every number explained, G1)
    half = (len(ent) + 1) // 2 if ncol == 2 else len(ent)
    kx, ky = lx0 + lw_ + 6.0, yrow + 2.0 - 2.0
    for ci_, part in enumerate((ent[:half], ent[half:])):
        yy = ky
        for n_, t_ in part:
            x_ = kx + ci_ * cw
            PU.put([("poly", sec_ellipse(x_ + 0.75 * T3_MK, yy - 0.4 * T3_MK, 0.75 * T3_MK, 0.75 * T3_MK, 20),
                     "FFFFFF", SEC["ink"], 0.15),
                    ("text", u"%d" % n_, x_ + 0.75 * T3_MK, yy - 0.76 * T3_MK, 0.85 * T3_MK, SEC["ink"], True, "C"),
                    ("text", t_, x_ + 2.0 * T3_MK, yy - 0.76 * T3_MK, T3_MK, SEC["ink"], False, "L")], 62)
            yy -= 1.5 * T3_MK
    bot = min(lay_["box"][1], ky - half * 1.5 * T3_MK, yrow + 1.0 - kh) - 1.0
    if kx + ncol * cw > max(xmax, T3_SEC_ROW_W) + 0.5:
        LOG.append(u"WARNING: street sections: the callouts' key runs {:.0f} mm past the booklet width.".format(
            kx + ncol * cw - max(xmax, T3_SEC_ROW_W)))
    return bot * kb, max(xmax, kx + ncol * cw)


def _t3_street_sections(S, B, x, y, w, U, M):
    """T3a (D3 b, Aras 29 Oct 18:53; replaces the walk / car index chart and the city link's walking potential):
    before / after cross-sections of one street per road change of the masterplan (kept, calmed, pedestrian,
    shared), each cut where the survey measured the street (_t3_sec_cut). A kept road is drawn once (no change).
    T4 (30 Oct, PG2 ③, D1): v55 (Aras 31 Oct) style a only, drawn by _t3_sec_block, crop drw_street_sections.
    R2-B (31 Oct, U24 "cut in half": the crop is a fixed size row on p.08 and ran past the page): one standard scale
    for all (T3_SEC_DENS), the largest whose rows fit the booklet width AND whose whole block (measured: _t3_sec_dry)
    stays within T3_SEC_H_MAX; if none does, the shortest, with a WARNING naming the height. Returns the y below."""
    L = "LU_BOARD::StreetSections"
    kb = 120.0 * U / BK_AW                                # board units per booklet mm
    groups = []
    for ch in T3_SEC_ORDER:
        rds = [rd for rd in (M.get("roads") or []) if rd.get("change", "kept") == ch]
        rds.sort(key=lambda rd: (u"Kınık" not in (rd.get("name") or u""), -pl_length(_xy_list(rd.get("xy")) or [(0, 0)])))
        cut = None
        for rd in rds:
            cut = _t3_sec_cut(S, rd)
            if cut:
                break
        if cut is None:
            LOG.append(u"Street sections: no measured street along a '{}' road of the masterplan, so none drawn."
                       .format(ch))
            continue
        groups.append(cut)
    if not groups:
        LOG.append("Street sections: nothing to draw (no masterplan roads with measured widths).")
        return y - 0.4 * U
    ext = dict((id(c_), _t3_sec_extent(c_)[0]) for c_ in groups)

    def pack(den):
        k_ = 1000.0 / den
        rows, cur, cw = [], [], 0.0
        for c_ in groups:
            n = 1 if c_["change"] == "kept" else 2
            gw = n * (ext[id(c_)][1] - ext[id(c_)][0]) * k_ + (n - 1) * T3_SEC_GAP
            if cur and cw + T3_SEC_PAIR_GAP + gw > T3_SEC_ROW_W:
                rows.append(cur)
                cur, cw = [], 0.0
            cw += (T3_SEC_PAIR_GAP if cur else 0.0) + gw
            cur.append(c_)
        return rows + ([cur] if cur else [])
    band = 26.0                                           # mm: the key map / legend / key band under the rows
    best, den, rows = None, None, None
    for d_ in T3_SEC_DENS:
        rw_ = pack(d_)
        h_ = _t3_sec_dry(groups, d_, rw_, "a") + band
        if best is None or h_ < best[0]:
            best = (h_, d_, rw_)
        if h_ <= T3_SEC_H_MAX:
            best = (h_, d_, rw_)
            break
    est, den, rows = best
    if est > T3_SEC_H_MAX:
        LOG.append(u"WARNING: street sections need about {:.0f} mm at 1:{:,} (the p.08 row allows {:.0f} mm): the "
                   u"booklet must give them more height.".format(est, den, T3_SEC_H_MAX))
    LOG.append(u"Street sections at 1:{:,}: ".format(den) + u"; ".join(
        u"{} {} ({}) {:.1f} m {}{}; buildings cut {}, behind {}".format(
            _t3_sec_id(i), c_["name"], c_["change"], c_["w"], c_["w_src"],
            u", carriageway {:.1f} m".format(c_["carriage"][1] - c_["carriage"][0]) if c_["carriage"] else u"",
            sum(1 for s_ in (-1, 1) if c_["side"][s_].get("back")), len(c_["beyond"])) for i, c_ in enumerate(groups)))
    cap = u"The same surveyed width, given back to people · streets today and with the project"
    out = y
    bot, xmax = _t3_sec_block(S, B, x, out, kb, groups, den, rows, "a", L)   # v55 (Aras 31 Oct): style a only
    crop_panel("street_sections", x - 0.5 * kb, bot - 0.5 * kb, x + (xmax + 0.5) * kb, out + 0.5 * kb, cap, den)
    CROP_PANELS[-1]["bk_w"] = xmax + 1.0
    LOG.append(u"Street sections crop drw_street_sections: {:.0f} x {:.0f} mm on the booklet page.".format(
        xmax + 1.0, (out - bot) / kb + 1.0))
    out = bot - 8.0 * kb
    cl = cut_log_line()
    if cl:
        LOG.append(u"Street sections (style a): " + cl)
    g14 = sf_g14_line()
    if g14:
        LOG.append(u"Street sections: " + g14)
    return out + 7.5 * kb


def mv_runs(S, R, key, F):
    """[(points, (class, value))] of map `key` along the walking (or driving) network, clipped to F."""
    pieces, IDX = R["pieces"], R["IDX"]
    if key.endswith("_d"):
        a_, b_ = IDX[key[:-2] + "_a"], IDX[key[:-2] + "_b"]
        vals = dict((i, a_.get(i, 0.0) - b_.get(i, 0.0)) for i in R["inside"])
    else:
        vals = IDX[key]
    net = ("car" if key.startswith("car") else "walk") + ("_a" if key.endswith(("_a", "_d")) else "_b")

    def val(pi):
        return (MV_CLASS.get(pieces[pi]["tags"].get("highway"), "lane"), round(vals.get(pi, 0.0), 1))
    return _runs(R["chains"][net], pieces, R["xy"], val, set(R["inside"]), F)


def draw_mv_streets(B, V, runs, L, order, scale=1.0, div=False, dmax=1.0):
    for P, (cls, v) in sorted(runs, key=lambda r: abs(r[1][1])):
        if div:
            if abs(v) < 0.05:
                continue
            col = mv_ramp(DIV, div_t(v, dmax))
        else:
            col = mv_ramp(SEQ, seq_t(v, 100.0))
        Q = V.P(P)                                        # T3a (p.07): a pale halo under each piece (smoother)
        B.line(Q, mix(col, WHITE, 0.6), L, order - 1, MV_W[cls] * scale * 2.2)
        B.line(Q, col, L, order, MV_W[cls] * scale)


def draw_how_people_use_it(S, B, x, y, w, U):
    """S2: how people move and what they reach (was 07 commercial spines, 09 civic constellations, diagrams D3, D5, D7
    and the movement script's panels). v46 (Prompt 3, p.8, analysis): the whole site frame at 1:10,000 on the frame's
    axes in the masterplan's base, the scale bar and north arrow under it; no proposed spine or stops (analysis
    only); walking and driving today as their own maps at the same scale under it (draw_mv_today). Returns the y below."""
    L = "LU_BOARD::HowPeopleUseIt"
    F = S.F
    MV = movement(S)
    R = MV.get("R")
    # T3a (package B p.07, G1): title-like captions that state the takeaway (were "How people use it / Walking today /
    # Driving today"); the top one only claims what the board's own rank correlation shows
    rho_ = (MV.get("rho") or {}).get("walk_b")
    t_top = (u"Shops line the streets people walk most" if rho_ is not None and rho_ >= 0.3 else
             u"Shops, services and everyday walks on one map")
    # T4 (30 Oct, p7 G1): the map's own heading inside its crop; the takeaway stays its caption
    V, k, ss, r = b_view(F, x, _t3_map_head(B, x, y, U, u"Shops, services and everyday walks", L), U)   # 1:10,000
    mw = F.w * ss
    CB = ClipB(B, r)
    try:                                                  # T3a (D8 b): the framework diagram's hand-off (city link v4)
        _t3_write_framework(S, R, MV)
    except Exception:
        LOG.append("WARNING: movement_framework.json not built:\n" + traceback.format_exc())
    try:
        DG, ctx = diagram_ctx(S)
        D7 = DG["d7_links"](ctx) if ctx.areas else None
    except Exception:
        LOG.append("WARNING: services and walks not drawn:\n" + traceback.format_exc())
        DG, ctx, D7 = None, None, None
    # T3a: the shared basemap in simple mode (pp.07-09 alike), the uses in colour over its faint buildings (v46)
    B.fill([rect(*r)], WHITE, L, 1)
    use_cats = ("commercial", "mixed", "institutional", "religious")
    _t3_base(S, CB, V, k, L)
    mini_buildings(S, CB, V, L, lambda u: CAT[u["cat"]][1] if u["cat"] in use_cats else None, order=10)
    # commerce spines: a broad pale band in the street, under the buildings
    cc = CAT["commercial"][1]
    for g in S.corr_primary:
        for P in g["Ps"]:
            CB.line(V.P(P), mix(cc, WHITE, 0.45), L, 9, bk_lw(1.8, k))
    for g in S.corr_secondary:
        for P in g["Ps"]:
            for d in dashes(V.P(P), 3.0 * k, 1.8 * k):
                CB.line(d, mix(cc, WHITE, 0.45), L, 9, bk_lw(1.1, k))
    # streets: line width = OSM class, colour = combined movement potential today
    if R:
        draw_mv_streets(CB, V, mv_runs(S, R, "comb_b", F), L, 14)
    # v46 (Prompt 3): the proposed streamside spine and its stops are no longer drawn here (an analysis map)
    # civic constellations
    hc = mix(CAT["institutional"][1], INK, 0.2)
    for cl in S.clusters:
        for run in F.clip_line(cl["P"] + [cl["P"][0]]):
            for d in dashes(V.P(run), 2.0 * k, 1.4 * k):
                CB.line(d, hc, L, 16, bk_lw(0.18, k))
    # services (Overture places, as D5) and the walks to the nearest of each function (as D7)
    fcol = dict((f, hexrgb(c)) for f, let, c, lab in WALK_FUN)
    n_pl = {}
    if ctx is not None:
        for px_, py_, f, nm, conf, cat in [p[:6] for p in ctx.places]:
            if F.inside(px_, py_):
                n_pl[f] = n_pl.get(f, 0) + 1
                cx, cy = V.p(px_, py_)
                CB.fill([circle_pts(cx, cy, 0.45 * k, 8)], fcol.get(f, INK2), L, 30)
    walk_c = mix(INK, PAPER, 0.15)
    dest = {}
    if D7:
        for k_, best in D7["res"].items():
            for f, r_ in best.items():
                if r_["pts"]:
                    for run in F.clip_line(r_["pts"]):
                        for d in dashes(V.P(run), 0.6 * k, 0.6 * k):
                            CB.line(d, walk_c, L, 32, bk_lw(0.16, k))
                dest[(f, round(r_["x"]), round(r_["y"]))] = r_
        rr = 1.9 * k
        let_of = dict((f, let) for f, let, c, lab in WALK_FUN)
        for (f, _, _), r_ in dest.items():
            if F.inside(r_["x"], r_["y"]):
                px, py = V.p(r_["x"], r_["y"])
                roundel(B, px, py, rr, let_of.get(f, "?"), fcol.get(f, INK), (255, 255, 255), L, order=62)
        for nm, sh, a in stage_areas(S):                    # where each walk starts: a name, never an outline
            cx, cy = shoelace(a["P"])[1:]
            px, py = V.p(cx, cy)                          # v40: plain text, no white box (Aras 25 Oct 21:41)
            CB.text(nm, px, py, bk_hk(8.0, k), INK, L, order=64, font=FONT_TITLE, bold=True, align="C")
    draw_map_annotations(S, B, V, U, rh=bk_hk(8.0, k))
    b_frame(B, r, k, L)
    foot = b_foot(B, F, x, r[1], ss, k, L)                # v46: under the map, never on it
    crop_r = (x - 0.5 * k, foot - 0.5 * k, r[2] + 0.5 * k, y)     # the booklet crop of the plan, with its heading
    r28mv_note_top(S, B, crop_r, k, L, MV, n_pl)          # v50 (MIRAQUA 28 Oct, P07.2): drw_mv_note_1 beside the plan
    yy = foot - 3.0 * U
    # walking and driving today, only the key streets in colour and named (v44, Aras 27 Oct: "highlight only the key
    # axes and roads"); v46: each its own map at the theme's one scale, stacked under the plan
    if R:
        # v50 (MIRAQUA 28 Oct, P07.3): the index on every street piece, the busiest named (draw_mv_today, 15i)
        # T3a (package B p.07): sharper, title-like names that state what each map shows (G1)
        # T4 (30 Oct, p7 G1): each map its own heading ("Pedestrian flow", "Vehicle traffic"), the takeaway its caption
        for key_, head, lead, mode in (("walk_b", u"Pedestrian flow · where feet go", u"Where feet go", u"walking"),
                                       ("car_b", u"Vehicle traffic · where cars go", u"Where cars go", u"driving")):
            two = _t3_names(mv_key_rows(MV, key_))
            title = (u"{}: {} carry the most {} routes".format(lead, two, mode) if two else lead)
            cap = title + (u" · every street by the share of everyday {} routes that use it; the busiest named, "
                           u"with their index (100 = the busiest street piece)").format(mode)
            yy = draw_mv_today(S, B, x, yy, U, R, MV, key_, head, cap) - 2.0 * U
    # walking lengths from each working area (D7), as a small table
    if D7:
        st = [(nm, sh) for nm, sh, a in stage_areas(S) if nm in D7["res"]]
        cw0, cw = 9.0 * U, (mw - 9.0 * U) / max(1, len(st))
        h = 0.36 * U
        r_walk = bcite(T3_PUB_SRC)                        # T3a (D13): public sources only
        B.text("WALK TO THE NEAREST · m along OSM streets and footways " + r_walk, V.X0, yy, 0.42 * U, INK, L,
               font=FONT_TITLE, bold=True)
        yy -= 1.0 * U
        for j, (nm, sh) in enumerate(st):
            B.text("from the " + nm, V.X0 + cw0 + j * cw, yy, h, INK2, L, bold=True)
        yy -= 0.85 * U
        # v33 (Step 4): the climb of every walk on the survey terrain, instead of an axonometric of S2
        walks = [D7["res"].get(nm, {}).get(f) for f, let, c, lab in WALK_FUN for nm, sh in st]
        lines_ = [r["pts"] if r and r["pts"] and not r["inside"] else [] for r in walks]
        ups = DG["walk_climbs"](ctx, lines_ + [p["pts"] for p in D7["pairs"]])
        climb = dict((id(r), u_) for r, u_ in zip(walks, ups) if r)
        for f, let, c, lab in WALK_FUN:
            roundel(B, V.X0 + 0.3 * U, yy + 0.15 * U, 0.3 * U, let, fcol[f], (255, 255, 255), L, order=62)
            B.text(lab, V.X0 + 0.9 * U, yy, h, INK, L)
            for j, (nm, sh) in enumerate(st):
                r = D7["res"].get(nm, {}).get(f)
                up = climb.get(id(r)) if r else None
                t_ = "none in reach" if not r else ("inside" if r["inside"] else DG["m10"](r["L"]) + (
                    ", {} m up".format(up) if up and up >= 5 else ""))
                B.text(t_, V.X0 + cw0 + j * cw, yy, h, INK, L)
            yy -= 0.75 * U
        ups = [u_ for u_, ln in zip(ups, lines_ + [p["pts"] for p in D7["pairs"]]) if u_ is not None and ln]
        yy -= 0.4 * U
    # legend (v38: short names; the method sentences are entries of the Sources key, cited [n])
    r_mv = bcite(T3_PUB_SRC) if R else ""                 # T3a (D13): public sources only, one [n]
    r_com = bcite(T3_PUB_SRC)
    leg = [("hdr", None, "STREETS · COLOUR = SHARE OF EVERYDAY ROUTES ON FOOT AND BY CAR · WIDTH = STREET CLASS " + r_mv)]
    if R:
        for v in (2, 10, 25, 50, 100):
            leg.append(("thick", mv_ramp(SEQ, seq_t(v, 100.0)), (u"{} · the busiest street piece" if v == 100 else
                                                                 u"{} of 100").format(v)))   # T3a (G1): spelled out
    leg += [("hdr", None, "SHOPS AND CIVIC LIFE " + r_com),
            ("thick", mix(cc, WHITE, 0.45), "Primary commercial spine"),
            ("dash", mix(cc, WHITE, 0.45), "Secondary commercial spine")]
    leg += [("box", CAT["commercial"][1], "Commerce"), ("box", CAT["mixed"][1], "Mixed use"),
            ("box", CAT["institutional"][1], "Civic"), ("box", CAT["religious"][1], "Sacred"),
            ("dash", hc, "Constellation · 3+ in 100 m")]
    if ctx is not None:
        leg += [("hdr", None, "SERVICES AND WALKS " + r_com)]
        for f, let, c, lab in WALK_FUN:
            if n_pl.get(f):                               # T4 (G1): the roundel's letter in its row
                leg.append(("dot", fcol[f], u"{} · {} · {} places".format(let, lab, n_pl[f])))
        leg.append(("dash", walk_c, "Walk to the nearest (letter at the place)"))
    ly = draw_legend_items(B, leg, x, yy - 0.4 * U, mw, U, L, h=0.4)
    crop_panel("movement", crop_r[0], crop_r[1], crop_r[2], crop_r[3], t_top + u" · streets, shops, services",
               crop_scale(ss), crop_legend(leg + _t3_base_leg()))    # T3a: the takeaway as caption, the simple base    # v40: the booklet crop of the plan (v46: 1:10,000);
    #                                                       v49.1 (Prompt 8): + the base's tones, as on p.10
    # v38 (visual first): what the numbers say as a tile and two mini-charts (were caption sentences); computed above,
    # nothing measured on the street
    cy0 = ly - 0.4 * U
    low = cy0
    cx = x
    gw, gh = min(30.0 * U, (mw - 4.0 * U) / 3.0), 7.0 * U
    tfill = mix(PAPER, (255, 255, 255), 0.5)
    if R and MV.get("rows"):
        top = MV["rows"][0]
        low = min(low, vis_tiles(B, cx, cy0, gw, [
            ("road", "BUSIEST STREET · WALK + DRIVE", "{} · index {:.0f}".format(top["name"], top["comb_b"]), r_mv)],
            U, L, h=1.3, ink=INK, grey=INK2, fill=tfill, rule=FAINT))
        cx += gw + 2.0 * U
        rw = MV["rho"].get("walk_b")
        big = [r_ for r_ in (MV.get("big") or []) if r_.get("walk_b") is not None]
        if rw is not None and big:                        # scatter: shops per street against walking potential
            B.text("SHOPS vs WALKING POTENTIAL · Spearman {:.2f} {}".format(rw, r_com), cx, cy0 - 0.4 * U, 0.4 * U,
                   INK, L, font=FONT_TITLE, bold=True)
            px0, py0 = cx + 1.4 * U, cy0 - 1.0 * U - gh
            pw_ = gw - 1.4 * U
            xm = max(100.0, max(r_["walk_b"] for r_ in big))
            ym = max(1.0, max(r_["shops"] for r_ in big))
            B.fill([rect(px0, py0, px0 + pw_, py0 + gh)], tfill, L, 20)
            B.line(rect(px0, py0, px0 + pw_, py0 + gh) + [(px0, py0)], FAINT, L, 21, 0.04)
            for r_ in big:
                B.fill([circle_pts(px0 + pw_ * r_["walk_b"] / xm, py0 + gh * r_["shops"] / ym, 0.12 * U, 8)],
                       mix(CAT["commercial"][1], INK, 0.2), L, 22)
            B.text("0", px0, py0 - 0.45 * U, 0.28 * U, INK2, L, align="C")
            B.text("{:.0f}".format(xm), px0 + pw_, py0 - 0.45 * U, 0.28 * U, INK2, L, align="C")
            B.text("{:.0f}".format(ym), px0 - 0.2 * U, py0 + gh - 0.28 * U, 0.28 * U, INK2, L, align="R")
            B.text("walking index · {} streets of 50 m+".format(len(MV["big"])), px0 + pw_ / 2.0, py0 - 0.95 * U,
                   0.28 * U, INK2, L, align="C")
            B.text("shops", px0 - 0.2 * U, py0 + 0.1 * U, 0.28 * U, INK2, L, align="R")
            crop_panel("shops_vs_walking", cx - 0.6 * U, py0 - 1.3 * U, cx + gw, py0 + gh + 0.1 * U,
                       u"More walkers, more shops · Spearman {:.2f}".format(rw))    # v40
            low = min(low, py0 - 1.4 * U)
            cx += gw + 2.0 * U
    if D7 and ups:                                        # the climb of every walk, as bars
        mx = max(ups)
        r_cl = u""                                        # T3a (D13): our own computation, no source printed
        B.text("CLIMB OF THE WALKS · " + ("none 5 m or more" if mx < 5 else "most {} m up".format(mx)) + " " + r_cl,
               cx, cy0 - 0.4 * U, 0.4 * U, INK, L, font=FONT_TITLE, bold=True)
        vv = sorted(ups, reverse=True)
        bx0, by0 = cx + 1.4 * U, cy0 - 1.0 * U - gh
        bw_ = (gw - 1.4 * U) / float(len(vv))
        ym = max(5.0, float(mx))
        for i, u_ in enumerate(vv):
            B.fill([rect(bx0 + i * bw_ + 0.1 * bw_, by0, bx0 + (i + 0.9) * bw_, by0 + gh * u_ / ym)],
                   INK2 if u_ >= 5 else FAINT, L, 21)
        for dd in dashes([(bx0, by0 + gh * 5.0 / ym), (bx0 + gw - 1.4 * U, by0 + gh * 5.0 / ym)], 0.3 * U, 0.2 * U):
            B.line(dd, MARK_C, L, 22, 0.06)
        B.text("5 m", bx0 - 0.2 * U, by0 + gh * 5.0 / ym - 0.12 * U, 0.28 * U, MARK_C, L, align="R")
        B.line([(bx0, by0), (bx0 + gw - 1.4 * U, by0)], INK2, L, 22, 0.05)
        B.text("walks, steepest first · m up", bx0 + (gw - 1.4 * U) / 2.0, by0 - 0.55 * U, 0.28 * U, INK2, L, align="C")
        crop_panel("walk_climb", cx, by0 - 0.9 * U, cx + gw, by0 + gh + 0.1 * U, u"Climb of the walks")     # v40
        low = min(low, by0 - 1.0 * U)
    return low - 0.4 * U
