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
    bf_ = (u"%s" % (globals().get("BM_FAINT") or {}).get("bld", "D3D0CB")).lstrip(u"#").upper()
    for it in items:                                      # v61 (G6-9): each base item in its kind's group
        hx_ = (u"%s" % (it[2] if len(it) > 2 else u"")).lstrip(u"#").upper() if it[0] in ("fill", "line") else u""
        kind_ = "water" if it[0] == "water" or hx_ in _T3_WATER_HEX else (
            ("buildings" if hx_ == bf_ else "ground") if it[0] == "fill" else ("roads" if it[0] == "line" else "labels"))
        with CB.kind(kind_):
            basemap_draw([it], lambda p: V.p(p[0], p[1]), fill_fn, line_fn)
    with CB.kind("annotations", "study area"):
        draw_r28_study(S, CB, V, k, L)
    return True


_T3_WATER_HEX = ("91ADB4", "5D7F8D", "7FA4B3", "5E8494")   # v61: basemap water / edge colours (BM_COL, BM_KEY)
# v61 (round 6, G6-6, H1 p07, H2 note 1): p07's uses and services by the hue table (common/hues.py hue): buildings by
# use (commerce MOV r1, mixed MOV r2, civic PUB r2, worship as a use PUB r3), the service letters (WALK_FUN functions:
# health PUB r1, civic PUB r2 and worship PUB r3 as the buildings, education PUB r4, food & market MOV r1 as commerce,
# park GRN r2, heritage HER by place, her_rank: H3)
T3_USE_HUE = dict(commercial=("MOV", 1), mixed=("MOV", 2), institutional=("PUB", 2), religious=("PUB", 3))
T3_FUN_HUE = dict(health=("PUB", 1), civic=("PUB", 2), worship=("PUB", 3), education=("PUB", 4), market=("MOV", 1),
                  park=("GRN", 2), heritage=("HER", 3))
T3_HER_DRAWN = set()     # v61: the heritage ranks of the service letters drawn on this run (the legend row says so)


def _t3_use_col(cat):
    """v61 (G6-6): a building use's colour on p07 (T3_USE_HUE), None = not coloured"""
    cr = T3_USE_HUE.get(cat)
    return C(hue(*cr)) if cr else None


def _t3_fun_col(f, name=None):
    """v61 (G6-6): a service function's colour on p07 (T3_FUN_HUE); a heritage place by its rank (her_rank, H3)"""
    if f == "heritage" and name:
        try:
            r_ = int(her_rank(name) or 3)
            T3_HER_DRAWN.add(r_)
            return C(hue("HER", r_))
        except Exception:
            pass
    if f == "heritage":
        T3_HER_DRAWN.add(3)
    return C(hue(*T3_FUN_HUE.get(f, ("CTX", 2))))


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
        col, wl = mv_ramp(r28mv_seq(), seq_t(v, 100.0)), _t3_grad_w(v)   # v61 (G6-6): MOV ramp
        Q = V.P(P)
        B.line(Q, mix(col, WHITE, 0.6), L, order, bk_lw(2.2 * wl, k))
        B.line(Q, col, L, order + 1, bk_lw(wl, k))
    return lens


# v58 (round 3, P07.1, P07.4): r28mv_class_legend (the ramp as five booklet legend rows under the crop) is gone: the
# ramp is one graphic in the column beside the map (r28mv_ramp, parts/15i).


def _t3_bb(P):
    return (min(p[0] for p in P), min(p[1] for p in P), max(p[0] for p in P), max(p[1] for p in P))


# v58 (round 3, P07.3): _t3_rot_box, _t3_poly_hit and _t3_run_label (street names along their streets) are gone:
# the busiest streets are numbered on the map (_t3_marks) and named in the list beside it.


def _t3_marks(named, k, r, avoid=()):
    """v58 (round 3, P07.3, G3): one marker spot per street, ON its own street: named [(key, [board polylines])] in
    priority order; along each street's runs (longest first, every tenth of its length) the spot farthest from the
    markers already set (up to 12 mm counts), the middle preferred; inside the map rect r less the marker's radius.
    avoid = other symbols' points (board units) the markers keep clear of as well. Returns {key: (x, y)}."""
    R_ = R28MV_MKR * k
    inner = (r[0] + R_ + 0.5 * k, r[1] + R_ + 0.5 * k, r[2] - R_ - 0.5 * k, r[3] - R_ - 0.5 * k)
    spots, placed = {}, list(avoid)
    for key, Qs in named:
        best = None
        for Q in sorted(Qs, key=lambda q_: -pl_length(q_)):
            Lq = pl_length(Q)
            if Lq <= 0:
                continue
            for i in range(1, 10):
                p = pl_point_at(Q, Lq * i / 10.0)[0]
                if not (inner[0] <= p[0] <= inner[2] and inner[1] <= p[1] <= inner[3]):
                    continue
                d = min([math.hypot(p[0] - q[0], p[1] - q[1]) for q in placed] or [1e9])
                sc = min(d, 12.0 * k) - 0.05 * abs(i - 5) * k + 1e-6 * Lq
                if best is None or sc > best[0]:
                    best = (sc, p)
        if best is None:
            LOG.append(u"p.07: no spot on the map for the street marker of {}.".format(key))
            continue
        spots[key] = best[1]
        placed.append(best[1])
    return spots


def _t3_number(keys, spots, k):
    """v58 (G3): the markers numbered in reading order (lp_reading_order: top row first, left to right, rows 8 mm):
    [(number, key)] in number order"""
    keys = [kk for kk in keys if kk in spots]
    ro = lp_reading_order([(spots[kk][0] / k, spots[kk][1] / k) for kk in keys], y_down=False, row_mm=8.0)
    return [(n, keys[j]) for n, j in enumerate(ro, 1)]


def _t3_stage_name(nm, sh):
    """v58 (round 3, G16): a working area's printed name: the bridge it holds by its real name (bridge_name), never
    the K-code of STAGES ("K4 bridge" -> "Ulucami Önü Köprüsü")"""
    try:
        return bridge_name(sh) if sh in bridges_in_order() else nm
    except Exception:
        return nm


def _t3_top_marks(S, B, V, R, MV, F, k, r, L, avoid):
    """v58 (round 3, P07.3, G3): the streets the top map's column names, numbered ON the map (reading order): the
    primary commercial spines (S.corr_primary, their shop counts) and the busiest street on foot and by car together
    (MV rows[0], its index; merged into its spine when it is one). avoid: the map's roundels and area names (board
    points). Returns [(number, dict(name, shops, idx))] in number order; the marker boxes go to T3_P07_BOXES."""
    its, named = {}, []
    for g in getattr(S, "corr_primary", None) or []:
        if g["label"] == "an unnamed street" or g["label"] in its:
            continue
        Qs = [V.P(q) for P in g["Ps"] for q in F.clip_line(P) if len(q) >= 2]
        if Qs:
            its[g["label"]] = dict(name=g["label"], shops=g["n"], idx=None)
            named.append((g["label"], Qs))
    rows = MV.get("rows") or []
    if rows and R:
        nm = rows[0]["name"]
        if nm in its:
            its[nm]["idx"] = rows[0]["comb_b"]
        else:
            Ps = _t3_named_runs(R, F, set([nm]), "walk_b").get(nm) or _t3_named_runs(R, F, set([nm]), "car_b").get(nm)
            if Ps:
                its[nm] = dict(name=nm, shops=None, idx=rows[0]["comb_b"])
                named.append((nm, [V.P(P) for P in Ps]))
    spots = _t3_marks(named, k, r, avoid)
    out = [(n_, its[nm]) for n_, nm in _t3_number([nm for nm, _q in named], spots, k)]
    for n_, it in out:
        b_ = r28mv_marker(B, spots[it["name"]][0], spots[it["name"]][1], n_, k, L)
        T3_P07_BOXES.append(tuple(v_ / k for v_ in b_))
    return out


def draw_mv_key(S, B, V, R, MV, key, F, L, h, bounds, k):
    """v44: the key streets of the walking / driving map. v58 (round 3, P07.3, G3; A2 lp_place: no leaders; replaces
    the names along the streets and their leader fallback): the 5 busiest named streets (mv_key_rows) HIGHLIGHTED (a
    dark casing under their own colour, over every other street) and NUMBERED on their own street (_t3_marks), the
    numbers in reading order (_t3_number); their names and index go in the list beside the map (r28mv_col_today).
    Returns (their rows, {name: every point of its runs}, [(number, row)] in number order, the marker boxes)."""
    rows = mv_key_rows(MV, key)
    net = "car_b" if key.startswith("car") else "walk_b"
    runs = _t3_named_runs(R, F, set(r_["name"] for r_ in rows), net)
    pts = dict((nm, [p for P in Ps for p in P]) for nm, Ps in runs.items())
    for r_ in rows:                                       # busiest streets highlighted (P07.3)
        wl_ = _t3_grad_w(r_[key])
        col = mv_ramp(r28mv_seq(), seq_t(r_[key], 100.0))      # v61 (G6-6): MOV ramp
        for P in runs.get(r_["name"], []):
            Q = V.P(P)
            B.line(Q, INK, L, 16, bk_lw(wl_ + 0.45, k))
            B.line(Q, col, L, 17, bk_lw(wl_, k))
    named = [(r_["name"], [V.P(P) for P in runs[r_["name"]]]) for r_ in rows if runs.get(r_["name"])]
    spots = _t3_marks(named, k, bounds)
    byname = dict((r_["name"], r_) for r_ in rows)
    nums = [(n_, byname[nm]) for n_, nm in _t3_number([nm for nm, _q in named], spots, k)]
    with B.kind("labels", "street numbers"):              # v61 (G6-9)
        boxes = [r28mv_marker(B, spots[r_["name"]][0], spots[r_["name"]][1], n_, k, L) for n_, r_ in nums]
    return rows, pts, nums, boxes


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


# ------------------------------------------------------------ p.07 the columns beside the maps (P07.1-P07.4)
# v58 (round 3): r28mv_note (a text-only note) is replaced by r28mv_column (parts/15i): each map's legend right beside
# it, its numbered streets, small graphics, then the compact note. T3_P07_BOXES: every text box the p.07 maps and
# columns place (booklet mm, the board's frame / k), for the page's overlap FLAG (draw_how_people_use_it).
T3_P07_BOXES = []


def _t3_blk(head, fn, k, L):
    """v58: a column block = an optional 8 pt heading over fn's drawing (fn(B, x, ytop, w, draw) -> (h mm, boxes))"""
    def f(B, x, y, w, draw):
        hh, bx = r28mv_head(B, head, x, y, k, L, draw) if head else (0.0, [])
        hb, bx2 = fn(B, x, y - hh * k, w, draw)
        return hh + hb, bx + bx2
    return f


def r28mv_note_top(S, B, crop, k, L, MV, n_pl, leg, nums):
    """v50 (P07.2): drw_mv_note_1, beside the top map. v58 (round 3, P07.1-P07.4): its legend first (leg: rows for
    r28mv_legend, 3 columns), the street index ramp (r28mv_ramp), the numbered streets of the map (nums [(n, dict(
    name, shops, idx))]: the primary spines with their shop counts as bars, the busiest street on foot and by car with
    its index) beside the services per function as bars (n_pl; the bars' dots = the map's service dots), then the
    secondary spines, shops against walking and the civic constellations as a short note. Returns the text boxes."""
    cc = _t3_use_col("commercial")                        # v61 (G6-6): commerce MOV r1
    ramp_t = (u"**Street colour**: the share of everyday routes on foot and by car using the street (100 = the "
              u"busiest piece); **width**: the street class")
    # v61 (U19, P-8): every block in its own row (stacked in the narrower column), the legend in one column
    rows_ = [(True, [(_t3_blk(None, lambda B_, x_, y_, w_, d_: r28mv_legend(B_, leg, x_, y_, w_, k, L, 1, d_), k, L),
                      1.0)]),
             (True, [(lambda B_, x_, y_, w_, d_: r28mv_ramp(B_, x_, y_, w_, k, L, d_, ramp_t, False), 1.0)])]
    st = []
    smax = max([it["shops"] for _n, it in nums if it.get("shops")] or [1])
    out = []
    for n_, it in nums:
        if it.get("shops"):
            vt = u"{} shops".format(it["shops"])
        else:
            vt = u"index {:.0f}".format(it["idx"]) if it.get("idx") is not None else u""
        st.append(dict(n=n_, label=it["name"], value=it.get("shops"), vtext=vt, colour=cc))
        if it.get("idx") is not None:
            out.append(u"**Busiest street** on foot and by car together: {} ({} on the map), index {:.0f} (100 = the "
                       u"busiest street piece).".format(it["name"], n_, it["idx"]))
    sv = []
    for f, let, c_, lab in WALK_FUN:
        if (n_pl or {}).get(f):
            fc_ = _t3_fun_col(f)
            if f == "heritage" and min(T3_HER_DRAWN or set([3])) < 3:
                lab = u"{}, darker = listed".format(lab)   # v61 (H3): the letters by heritage rank
            sv.append(dict(dot=fc_, label=u"{} · {}".format(let, lab), value=n_pl[f], vtext=u"%d" % n_pl[f],
                           colour=fc_))
    if st:
        rows_.append((True, [(_t3_blk(u"Streets on the map " + bcite(T3_PUB_SRC),
                                      lambda B_, x_, y_, w_, d_: r28mv_bars(B_, st, x_, y_, w_, k, L, smax, d_), k, L),
                              1.0)]))
    if sv:
        tot = sum(n_pl.values())
        rows_.append((True, [(_t3_blk(u"Services on the map · {}".format(tot),
                                      lambda B_, x_, y_, w_, d_: r28mv_bars(B_, sv, x_, y_, w_, k, L,
                                                                           max(r_["value"] for r_ in sv), d_), k, L),
                              1.0)]))
    sec = getattr(S, "corr_secondary", None) or []
    if sec:
        out.append(u"**{} more street{}** with 3 or more shops: the secondary spines.".format(
            len(sec), u"" if len(sec) == 1 else u"s"))
    rho, big = (MV.get("rho") or {}).get("walk_b"), MV.get("big") or []
    if rho is not None and big:
        out.append(u"**Shops and walking**: Spearman {:.2f} over the {} named streets of 50 m or more (1 = the same "
                   u"order).".format(rho, len(big)))
    cl = [c_ for c_ in getattr(S, "clusters", None) or [] if any(S.F.inside(p[0], p[1]) for p in c_["P"])]
    if cl:
        out.append(u"**{} civic constellation{}**: 3 or more civic or sacred places, each within 100 m of the "
                   u"next.".format(len(cl), u"" if len(cl) == 1 else u"s"))
    return r28mv_column(B, crop, k, L, 1, rows_, out)


def r28mv_note_today(S, R, MV, key, rows, pts, lens):
    """v50 (P07.2): the lines of drw_mv_note_2 / _3. v58 (round 3, P07.4): what is left as words once the busiest
    streets, the index along the stream and the network length per class are graphics (r28mv_col_today): how many
    of the busiest come close to the stream, what the index counts"""
    walk = key.startswith("walk")
    out = []
    main = r28mv_main_stream(S)
    if main and rows:
        near = [r_ for r_ in rows if pts.get(r_["name"]) and
                min(pl_dist(p[0], p[1], main, False) for p in pts[r_["name"]]) <= R28MV_NEAR_M]
        out.append(u"**{} of the {}** busiest come within {:.0f} m of the stream.".format(len(near), len(rows),
                                                                                         R28MV_NEAR_M))
    if walk:
        out.append(u"**On foot**: the shortest routes up to {:.0f} m between every building and the everyday "
                   u"destinations {}.".format(MV_OPT["r_walk"], bcite(T3_PUB_SRC)))
    else:
        out.append(u"**By car**: the shortest routes up to {:.0f} min; footways and steps are not on this map "
                   u"{}.".format(MV_OPT["t_car"] / 60.0, bcite(T3_PUB_SRC)))
    return out


def r28mv_col_today(S, B, crop, k, L, R, MV, key, rows, pts, lens, nums):
    """v58 (round 3, P07.1-P07.4): the column beside the walking / driving map: the index ramp, the legend (the base,
    the highlighted busiest streets), the numbered busiest streets as index bars in number (reading) order beside
    the index along the stream against every street (bars), the network length per index class (one 100 % bar),
    then the note. Returns the text boxes."""
    walk = key.startswith("walk")
    seq = r28mv_seq()                                     # v61 (G6-6): the MOV ramp
    hi = mv_ramp(seq, seq_t(75.0, 100.0))
    leg = [("case", hi, u"Busiest named street, numbered", 0.8)] + \
        [(kd_, col_, lab_) for kd_, col_, lab_ in _t3_base_leg()]
    # v61 (U19, P-8): stacked in the narrower column: the legend in one column, each graphic in its own row
    rows_ = [(True, [(lambda B_, x_, y_, w_, d_: r28mv_ramp(B_, x_, y_, w_, k, L, d_), 1.0)]),
             (True, [(_t3_blk(None, lambda B_, x_, y_, w_, d_: r28mv_legend(B_, leg, x_, y_, w_, k, L, 1, d_), k, L),
                      1.0)])]
    st = [dict(n=n_, label=r_["name"], value=r_[key], vtext=u"{:.0f}".format(r_[key]),
               colour=mv_ramp(seq, seq_t(r_[key], 100.0))) for n_, r_ in nums]
    if st:                                                # the full width: the long street names fit their row
        rows_.append((True, [(_t3_blk(u"Busiest named streets · index",
                                      lambda B_, x_, y_, w_, d_: r28mv_bars(B_, st, x_, y_, w_, k, L, 100.0, d_), k, L),
                              1.0)]))
    em = r28mv_edge_means(S, R).get(key)
    if em and em[0] is not None and em[1] is not None:
        eb = [dict(label=u"along the stream", value=em[0],
                   vtext=u"{:.0f}".format(em[0]), colour=mv_ramp(seq, seq_t(em[0], 100.0))),
              dict(label=u"all streets", value=em[1], vtext=u"{:.0f}".format(em[1]),
                   colour=mv_ramp(seq, seq_t(em[1], 100.0)))]
        rows_.append((False, [(_t3_blk(u"Average index · stream-edge band",   # v60.2: no width; v61: own row
                                       lambda B_, x_, y_, w_, d_: r28mv_bars(B_, eb, x_, y_, w_, k, L,
                                                                            max(1.0, em[0], em[1]), d_), k, L), 1.0)]))
    tot = sum(lens)
    if tot > 0:
        labs = [None] * len(lens)
        labs[0] = u"{:.0f}% under {:.0f}".format(100.0 * lens[0] / tot, R28MV_CLS[0])
        labs[-2] = u"{:.0f}% {:.0f} or more".format(100.0 * (lens[-2] + lens[-1]) / tot, R28MV_CLS[-3])
        parts = [(l_ / tot, mv_ramp(seq, seq_t(v_, 100.0)), lb_) for l_, v_, lb_ in zip(lens, R28MV_CLS, labs)]
        rows_.append((False, [(_t3_blk(u"{} length by index".format(u"Walkable" if walk else u"Drivable"),
                                       lambda B_, x_, y_, w_, d_: r28mv_stack(B_, parts, x_, y_, w_, k, L, d_), k, L),
                               1.0)]))                    # v61: stacked under the average (was side by side)
    return r28mv_column(B, crop, k, L, R28MV_NOTE_OF[key], rows_, r28mv_note_today(S, R, MV, key, rows, pts, lens))


T3_HEAD_PT = 10.0        # pt: a p.07 map's own heading, inside its crop (T4, G1)


def _t3_map_head(B, x, y, U, head, L):
    """T4 (30 Oct, p7 G1): a p.07 map's heading at the top of its crop (y = the crop's top); returns the y of the
    map's top edge under it"""
    k0 = 120.0 * U / BK_AW
    hh = bk_hk(T3_HEAD_PT, k0)
    B.text(head, x, y - 0.5 * k0 - hh, hh, INK, L, order=66, font=FONT_TITLE, bold=True)
    return y - 0.5 * k0 - hh - 2.0 * k0


def _t3_head_box(x, y, U, head):
    """v58 (G3): the box (booklet mm) of a p.07 map's heading as _t3_map_head sets it"""
    k0 = 120.0 * U / BK_AW
    hh = bk_hk(T3_HEAD_PT, k0)
    b_ = r28mv_tbox(head, x, y - 0.5 * k0 - hh, hh, True)
    return tuple(v_ / k0 for v_ in b_)


T3_CAP_PT = 7.5          # pt: the booklet's caption size (bergama_booklet T["caption"], regular), for P07.1


def _t3_cap_fit(cap, w_mm, slug):
    """v59 (round 4, P07.1, G-R4-2 "captions never wider than their block"; round 3 open row 11): the booklet sets a
    crop's caption as ONE line at 7.5 pt under the crop, so the caption is chosen here to fit the crop's width on the
    booklet page (w_mm, booklet mm, real Arial widths): cap = a text or its alternatives, longest first; the first
    that fits is used; none fits -> RuntimeError (a caption is never cut silently). Logs the choice."""
    alts = [cap] if not isinstance(cap, (list, tuple)) else list(cap)
    alts = [a_ for a_ in alts if a_]
    if not alts:
        return u""
    for a_ in alts:
        if fm_width(a_, T3_CAP_PT, False) <= w_mm:
            if a_ != alts[0]:
                LOG.append(u"Caption {}: shortened to fit {:.0f} mm: \"{}\".".format(slug, w_mm, a_))
            return a_
    wn_warn("p07", "caption", u"{}: no form fits its {:.0f} mm crop at {} pt; the shortest is used: {}".format(
        slug, w_mm, T3_CAP_PT, u" | ".join(alts)))       # v60 (C1): warns, never stops
    return alts[-1]


def draw_mv_today(S, B, x, y, U, R, MV, key, title, cap):
    """v46 (Prompt 3, p.8): walking or driving today as its own map at the theme's one scale: the whole site frame at
    1:10,000, the masterplan base, the scale bar and north arrow under it. v50 (MIRAQUA 28 Oct, P07.3): the index on
    EVERY street piece of its network (mv_runs walk_b / car_b; walking-only pieces stay base street on the driving
    map), graded in five classes by colour and line weight (r28mv_class_streets), the classes in the crop's legend;
    the 5 busiest named streets named at 7 pt (draw_mv_key, P07.4); P07.2: its note beside it (drw_mv_note_2 / _3).
    T4 (30 Oct, p7): title = the map's own heading, inside its crop (G1); the names run along their streets (G3);
    the crop's legend (drawn by the booklet under the crop, M2) holds every symbol. Returns the y below its crop.
    v58 (round 3, P07.1-P07.4): the busiest streets highlighted and numbered on the map (draw_mv_key), no legend
    under the crop: the legend, the numbered list and the graphics stand in the column right beside the map
    (r28mv_col_today); cap = the short takeaway only (P07.2: one line inside the map's own width)."""
    L = "LU_BOARD::HowPeopleUseIt"
    F = S.F
    V, k, ss, r = b_view(F, x, _t3_map_head(B, x, y, U, title, L), U)
    T3_P07_BOXES.append(_t3_head_box(x, y, U, title))
    i0_m = sb_mark(B)                                     # v59 closing (G-R4-1): the map's own texts from here
    h = bk_hk(R28MV_LABEL_PT, k)
    CB = ClipB(B, r)
    with B.kind("ground", "paper"):
        B.fill([rect(*r)], WHITE, L, 1)
    _t3_base(S, CB, V, k, L)                              # T3a: the shared basemap, simple mode (pp.07-09)
    with B.kind("roads"):                                 # v61 (G6-9)
        lens = r28mv_class_streets(CB, V, mv_runs(S, R, key, F), k, L, 14)
        rows, pts, nums, mb = draw_mv_key(S, CB, V, R, MV, key, F, L, h, r, k)
    with B.kind("frame", "map frame"):
        b_frame(B, r, k, L)
    sb_keep(B, r, u"p07 %s map" % key, "map", i0_m)       # v59 closing (G-R4-1): its names may, no other text
    low = b_foot(B, F, x, r[1], ss, k, L)
    crop = (x - 0.5 * k, low - 0.5 * k, r[2] + 0.5 * k, y)
    cap = _t3_cap_fit(cap, (crop[2] - crop[0]) / k, CROP_MV.get(key, key))   # v59 (round 4, P07.1): width-limited
    crop_panel(CROP_MV.get(key, key), crop[0], crop[1], crop[2], crop[3], cap, crop_scale(ss), None)   # v58 (P07.1)
    bx = list(mb)
    if key in R28MV_NOTE_OF:
        bx += r28mv_col_today(S, B, crop, k, L, R, MV, key, rows, pts, lens, nums)
    T3_P07_BOXES.extend(tuple(v_ / k for v_ in b_) for b_ in bx)
    return low - 0.5 * k


# ------------------------------------------------------------ p.08 street sections (T3a, D3 b; was p.09 the proposal map)
def draw_mv_proposal(S, B, x, y, w, U, M):
    """T3a WO-T3a-5 (29 Oct 2026, D8 b, D3 b): the proposal map (drw_proposal) and the walk / car index chart
    (drw_index_change, refs S02) are gone: the masterplan's roads, crossings, hubs and the reach on foot are drawn in
    the city link's framework diagram (bergama_city_link v4, booklet p.08). The core still calls this with the
    masterplan's movement M (only when masterplan_results.json holds it), so it now draws the before / after street
    sections per road change (_t3_street_sections; v61: crops street_R1..R4 on booklet p08). Returns the y below."""
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
# (M2 Legend). v55 (Aras 31 Oct): style "a" only (cutouts placed with B.image; a missing cutout is drawn in style b).
# v61 (round 6, U18, P-9 option A; LANGUAGE: ACCURATE, r06_S03 traits): one row of four pairs at one scale, each pair
# its own crop street_R1..R4 (booklet p08); no sky, no icon badges, no numbered callouts or their key, no width or
# height texts: short labels on the drawing (_t3_label_band) and the levels at each pair's right edge
# (sf_level_marks); the existing trees the cut sees by species (_t3_trees_seen, G6-10; replaces the illustrative
# _t3_trees_behind); the key map through km_keymap (SB_KM), the legend as an item (SB_LEG); street_cuts.json.
T3_SEC_ORDER = ("kept", "calmed", "pedestrian", "shared")   # the masterplan's road changes, one section pair each
T3_SEC_DENS = (200, 250, 300, 400, 500, 600)   # v61: the scales tried, largest first: ONE row on the booklet width
T3_SEC_ROW_W = 392.0     # mm: one booklet row (BK_AW; P-9 strip x 2.3-96.5 % = 395.6 mm)
T3_SEC_GAP = 8.0         # mm between today and with the project; v61: = T3_SEC_PAIR_GAP (P-9: even gaps)
T3_SEC_PAIR_GAP = 8.0    # mm between two road types (the booklet sets the crops this far apart for even gaps)
T3_TREE_SEEN_M = 40.0    # m: v61 (G6-10): existing crowns drawn from the cut to this far along the street (drawing rule)
T3_KM_W, T3_KM_H = 102.9, 17.8   # mm: v61 (P-9 option A): the key map's frame [72,27 25x6] % of the A3 page
T3_CUTS_FILE = os.path.join(SELINUS_RES_DIR, "street_cuts.json")   # v61 (PLAN §5): read by the masterplan (S9)
T3_LV_INK = "2C2219"     # v61: level marks in the hue table's annotation ink (ANN)
T3_EL_WORD = dict(bollard=u"Bollards", lamp=u"Lamp", rack=u"Bike rack")   # v61: short labels of the street elements
T3_SEC_MATCH = 10.0      # m: an OSM street piece runs along a masterplan road when half its points lie this close
T3_SEC_REACH = 15.0      # m: a frontage (survey building) is looked for this far across, each side (as measure_widths)
T3_SEC_DEEP = 24.0       # m: a fronting building is followed this far back from its frontage (its real depth)
T3_SEC_BEYOND = (-16.0, -8.0, 8.0, 16.0)   # m along the street: where the façades behind the cut are looked for
T3_SEC_OPEN = 3.0        # m of ground drawn beyond the street edge where no building fronts it
T3_SEC_TREE_MIN = 6.0    # m: a street at least this wide (frontage to frontage) takes a tree in the proposal
T3_SEC_CAR = (1.80, 1.45)   # m: a car seen from the front (width, height), the drawing's symbol (no module draws cars)
T3_SEC_GROUND_M = 1.2    # m of cut ground drawn under the street (drawing rule)
# R2-B (31 Oct 2026, U24 "cut in half", Section checklist): the block must fit its booklet row whole
T3_SEC_SHOW_DEEP = 3.0   # m: a cut fronting building is drawn this far back from its frontage, then a break line
#                          (drawing rule: the street is the subject; the survey depth is kept in the data). v58 (round 3,
#                          P08.2): 8 -> 3 m so the four streets fit two rows at 1:200 / 1:250 (people >= 6 mm)
T3_FS = 2.3              # mm: the font size of every word in the sections (6.5 pt)
T3_COL = dict(car="A7A299", car_edge="6E675F", ink="4A3F35", ink2="7A6E60", head="8B3A3F", beyond="F2F0EC",
              beyond_edge="C9C3BA", lead="9A9086")
T3_CHANGE_TXT = dict(kept=u"kept as it is", calmed=u"calmed", pedestrian=u"made pedestrian", shared=u"shared street")
# the people of a section: footprint (m along the cut) and head height (m) of each act; who does what per street
T3_ACT = dict(adult_child=(1.0, 1.75), group=(1.8, 1.75), kerb=(0.6, 1.75), bike=(1.9, 1.80), bench=(1.0, 1.30),
              market=(2.6, 1.75), child_play=(0.8, 1.15), dog_walk=(2.4, 1.75))     # v58 (P08.2, G15): + dog walker
T3_SCRIPT = dict(today=("adult_child", "group", "kerb", "bike"),
                 calmed=("bike", "group", "bench", "adult_child", "child_play"),
                 pedestrian=("market", "bench", "group", "child_play", "adult_child"),
                 shared=("bike", "group", "bench", "adult_child", "dog_walk"))
# v58 (round 3, P08.2, G3): every activity drawn at the cut has ONE title right above it (v61: the label only; the
# icon key is unused since the badges are gone)
T3_ACT_USE = dict(group=("people", u"Meeting"), bench=("seating", u"Seating"), market=("market", u"Market stall"),
                  bike=("bike", u"Cycling"), child_play=("people", u"Play"), adult_child=("walk", u"Walking"),
                  kerb=("walk", u"Waiting to cross"), dog_walk=("walk", u"Dog walk"))
# v58 (round 3, P08.2, G15, R07): the designed zones of each street with the project, named under the section:
# (name, from, to) as shares of the street's width frontage to frontage (a design proposal, not survey data); "car"
# = the slow car lane (calmed: the surveyed carriageway when it is measured). The act -> zone it is drawn in.
T3_ZONES = dict(calmed=((u"Walking", 0.0, 0.30), (u"Slow cars, bikes", 0.30, 0.65), (u"Seats, meeting", 0.65, 1.0)),
                pedestrian=((u"Market", 0.0, 0.30), (u"Shade, seats", 0.30, 0.70), (u"Play, walking", 0.70, 1.0)),
                shared=((u"Shade, seats", 0.0, 0.45), (u"Cars at walking pace", 0.45, 0.80), (u"Walking", 0.80, 1.0)))
T3_ZONE_OF = dict(calmed=dict(adult_child=0, bike=1, group=2, bench=2, child_play=2),
                  pedestrian=dict(market=0, adult_child=0, bench=1, group=2, child_play=2),
                  shared=dict(bench=0, group=0, bike=1, adult_child=2, dog_walk=2))
T3_CAR_ZONE = dict(calmed=1, shared=1)                   # the zone the (slow) car drives in
T3_TREE_ZONE = dict(pedestrian=1, shared=0)              # the zone the project's planting group stands in
# v59 (round 4, G-R4-5.2, D7): the low layer of shrubs and flowers (plants.py PLA_LOW, dry street species only) and
# the zone of each street with the project it stands behind (drawing rule: the planting zone, else the seats)
T3_LOW_MIX = ("chaste", "rosemary", "lavender")
T3_LOW_ZONE = dict(calmed=2, pedestrian=1, shared=0)
T3_ZONE_ROW = 2.6        # mm: one line of the zone band under a section (6.5 pt text)
T3_TITLE_ROW = 2.6       # mm: one row of the label band
T3_TITLE_ROWS = 3        # rows the label band may stagger into (labels never touch)
# D4 a: the bubbles caricature the situation (an illustrative scenario, never a quote); one at most per section
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
                houses.append((min(xs_), max(xs_), float(u["h"]), u.get("floors") or None, abs(off)))   # v59: + m
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


def _t3_trees_seen(S, cut, page="p08"):
    """v61 (round 6, G6-10; replaces _t3_trees_behind, whose plane / chaste groups were not surveyed): the EXISTING
    crowns a street cut sees (crowns_near_full: CHM crowns with leaf / leaf_src), from the cut itself (a crown the
    cut passes through) to T3_TREE_SEEN_M m along the street the way the section looks (+t, as the background
    houses), whose crown lies whole inside the drawing's width; each with its species from sb_tree_species (once per
    crown, counted for the `trees <page>` line), None = the generic tree. Returns [dict(d m along, x m across, h m,
    r m, sp)], farthest first."""
    (xl, xr), _st = _t3_sec_extent(cut)
    p, t = cut["p"], cut["t"]
    R_ = T3_TREE_SEEN_M + 30.0
    out = []
    for row in crowns_near_full(S, (p[0] - R_, p[1] - R_, p[0] + R_, p[1] + R_)):
        tx, ty, r_, h_, lf, ls = row[:6]
        dn = (tx - p[0]) * t[0] + (ty - p[1]) * t[1]
        if dn < -r_ or dn > T3_TREE_SEEN_M:
            continue
        xa = (tx - p[0]) * t[1] - (ty - p[1]) * t[0]      # across: the right normal (ty, -tx), as the back houses
        if xa - r_ < xl or xa + r_ > xr:
            continue
        sp = sb_tree_species(S, tx, ty, lf, ls, r_, h_, page=page)[0]
        out.append(dict(d=max(0.0, dn), x=xa, h=float(h_), r=float(r_), sp=sp))
    out.sort(key=lambda q_: -q_["d"])
    return out


def _t3_tree_generic(x, gy, k, h, r, layer=0):
    """v61 (G6-10): an existing tree with no supported species, drawn generic (no species named): a trunk and an
    elliptic crown at its measured height and crown radius, in the context tones of the hue table (CTX r4 fill, r2
    edge), smaller and paler with depth (D9 fig_depth)."""
    sc, fade = fig_depth(layer)
    kk = k * sc
    rv = max(0.5, min(float(r), 0.45 * float(h)))
    cy = gy + (float(h) - rv) * kk
    fill = mix(C(hue("CTX", 4)), WHITE, fade)
    edge = mix(C(hue("CTX", 2)), WHITE, fade)
    return [("line", [(x, gy), (x, cy)], edge, 0.25),
            ("poly", sec_ellipse(x, cy, float(r) * kk, rv * kk, 24), fill, edge, 0.13)]


def _t3_label_band(uses, W):
    """v61 (round 6, ACCURATE language: short labels on the drawing; replaces _t3_icon_band and its badges, and the
    numbered callouts and their key): the band of short labels over one section W mm wide: each use (_, label, x mm,
    _) ONE label centred over its own x, in up to T3_TITLE_ROWS staggered rows, inside 0..W, never touching another
    label (interval test per row); a label with no free place goes right of the row that ends first (WARNING when it
    then runs past the section). Returns (shapes with the band's foot at y 0, the band's height mm, label boxes)."""
    kd = kind_of(FONT_TITLE)
    its = sorted(uses, key=lambda u_: u_[2])
    if not its:
        return [], 0.0, []
    cap = T3_FS * R28MV_CAP
    yt0 = 0.25 * cap + 0.3                                # the lowest row's baseline over the band's foot
    right = [-1e9] * T3_TITLE_ROWS
    sh, boxes, used = [], [], 0
    for _ico, lab, cx, _ty in its:
        cx = min(max(cx, 0.0), W)
        w_ = tw(lab, cap, kd)
        x0 = min(max(cx - 0.5 * w_, 0.0), max(0.0, W - w_))
        row = None
        for r in range(T3_TITLE_ROWS):
            if x0 >= right[r] + 0.8:
                row = r
                break
        if row is None:
            row = min(range(T3_TITLE_ROWS), key=lambda r_: right[r_])
            x0 = right[row] + 0.8
            if x0 + w_ > W:
                wn_warn("p08", "label", u"\"{}\" runs {:.1f} mm past its section".format(lab, x0 + w_ - W))
        right[row] = x0 + w_
        used = max(used, row + 1)
        yb = yt0 + row * T3_TITLE_ROW
        sh.append(("text", lab, x0, yb, T3_FS, T3_COL["ink"], False, "L"))
        boxes.append((x0, yb - 0.25 * cap, x0 + w_, yb + cap))
    return sh, yt0 + (used - 1) * T3_TITLE_ROW + cap + 0.4, boxes


# v61 (G6-9): a section's draw list carries one (kind, element id) per shape (wl.tg, parallel to wl.L), so every
# element is its own group on the board; shapes added without one take their layer's kind
_T3_LAYER_KIND = dict(atmosphere="other", background="buildings", ground="ground", bed="water", water="water",
                      structures="buildings", vegetation="plants", figures="people", labels="labels")


def _t3_wl_sync(wl, kind=None):
    """G6-9: pads wl.tg to wl.L (shapes a module added straight into wl: kind, else their layer's kind)"""
    if not hasattr(wl, "tg"):
        wl.tg = dict((n, []) for n in WAT_LAYERS)
    for n in WAT_LAYERS:
        miss = len(wl.L[n]) - len(wl.tg[n])
        if miss > 0:
            wl.tg[n] += [(kind or _T3_LAYER_KIND.get(n, "other"), None)] * miss


def _t3_wl_add(wl, layer, shapes, kind, eid=None, front=False):
    """G6-9: wl.add with the shapes' (kind, element id); front = in front of the layer's list (drawn first)"""
    _t3_wl_sync(wl)
    sh = list(shapes or [])
    tg = [(kind, None if eid is None else u"%s" % eid)] * len(sh)
    if front:
        wl.L[layer][:0] = sh
        wl.tg[layer][:0] = tg
    else:
        wl.add(layer, sh)
        wl.tg[layer] += tg


def _t3_put_tagged(B, PU, wl, lay, dx, dy, order):
    """G6-9: one layer of a section's draw list onto the board moved by (dx, dy) mm, each run of shapes of one
    (kind, element id) inside its own B.kind group"""
    _t3_wl_sync(wl)
    sh, tg = wl.L[lay], wl.tg[lay]
    i = 0
    while i < len(sh):
        j = i + 1
        while j < len(sh) and tg[j] == tg[i]:
            j += 1
        with B.kind(tg[i][0], tg[i][1]):
            PU.put(_t3_shift(sh[i:j], dx, dy), order)
        i = j


def _t3_shape_bb(s_):
    """the box (mm) of one house shape (poly, line, image), else None"""
    if s_[0] in ("poly", "line") and len(s_[1]) >= 2:
        return _t3_bb(s_[1])
    if s_[0] == "image":
        return (s_[1], s_[2], s_[1] + s_[3], s_[2] + s_[4])
    return None


def _t3_sec_levels(S, cut):
    """v61 (ACCURATE: levels as values with a triangle at the right edge): the levels of one street cut: the street
    at the cut point (S.z_at, m above sea; the survey terrain) and the top of each cut fronting building (street +
    its surveyed height; one value when both sides are as high). Returns ([(name, level m, height above the street
    m)], absolute): absolute False = no terrain on this run, the values are then above the street (logged)."""
    z0, ab = 0.0, False
    if getattr(S, "terrain_ok", False) and getattr(S, "z_at", None):
        try:
            z0, ab = float(S.z_at(cut["p"][0], cut["p"][1])), True
        except Exception:
            z0, ab = 0.0, False
    rows = [(u"street", z0, 0.0)]
    tops = []
    for sg, nm in ((-1, u"roof, left"), (1, u"roof, right")):
        sd = cut["side"][sg]
        if sd.get("back") and sd.get("h"):
            tops.append((nm, float(sd["h"])))
    if len(tops) == 2 and abs(tops[0][1] - tops[1][1]) < 0.005:
        tops = [(u"roofs", tops[0][1])]
    rows += [(nm, z0 + h_, h_) for nm, h_ in sorted(tops, key=lambda q_: -q_[1])]
    return rows, ab


def _t3_lv_w(cut):
    """mm: the level column right of a street pair (sf_level_marks: gap, dashes, triangle, the widest value)"""
    kd = kind_of(FONT_TITLE)
    L_ = SF_LEVEL
    return L_["gap"] + sum(L_["dashes"]) + 0.5 * L_["tri_w"] + L_["label_gap"] + 0.5 + max(
        [tw(u"%+.2f %s" % (v_, n_), L_["size"] * R28MV_CAP, kd) for n_, v_, _h in cut.get("levels") or []] or [0.0])


T3_CHANGE_HUE = dict(kept=("CTX", 2), pedestrian=("MOV", 1), calmed=("MOV", 2), shared=("MOV", 3),
                     relocated=("MOV", 2))           # v61 (G6-6, H2 note 2): road change -> hue table (relocated dashed)


def _t3_change_hex(ch):
    """v61 (G6-6): the hue-table colour (hex) of a road change"""
    code, rank = T3_CHANGE_HUE.get(ch, ("CTX", 2))
    return hue(code, rank)


def _t3_zone_band(zones, X, k, y0, W, today):
    """v58 (round 3, P08.2, G15, R07 "zones named under the section"): under the cut ground at y0 (mm): a thin rule
    with a tick at every zone edge, each zone named under its own span (6.5 pt), today with its surveyed width in cm
    on a second line; a name wider than its span goes one label row lower (never touching its neighbour). zones =
    [(name, from m, to m)]; X = m -> mm. Returns (shapes, the y below the band, the text boxes)."""
    kd = kind_of(FONT_TITLE)
    cap = T3_FS * R28MV_CAP
    ink2 = T3_COL["ink2"]
    xs = sorted(set([min(max(X(a_), 0.0), W) for _n, a_, _b in zones] + [min(max(X(b_), 0.0), W)
                                                                       for _n, _a, b_ in zones]))
    sh = [("line", [(xs[0], y0), (xs[-1], y0)], ink2, 0.15)] if xs else []
    # v60.2 (G-R5-4.6, CLOSING_CHECK §2 rows 8/13): no tick at each zone edge and no surveyed width in cm (they read
    # as a width chain); the zones keep their names only
    today = False
    nl = 1
    right, boxes, low = [-1e9, -1e9], [], y0
    for nm, a_, b_ in zones:
        xa, xb = min(max(X(a_), 0.0), W), min(max(X(b_), 0.0), W)
        lines = [nm] + ([u"{:,.0f} cm".format((b_ - a_) * 100.0)] if today else [])
        w_ = max(tw(t_, cap, kd) for t_ in lines)
        x0 = min(max(0.5 * (xa + xb) - 0.5 * w_, 0.0), max(0.0, W - w_))
        row = 0 if x0 >= right[0] + 0.8 else 1
        if row == 1 and x0 < right[1] + 0.8:
            x0 = right[1] + 0.8                           # the second row is taken too: just right of it
        right[row] = x0 + w_
        yb = y0 - 1.0 - cap - row * nl * T3_ZONE_ROW
        for j, t_ in enumerate(lines):
            sh.append(("text", t_, x0 + 0.5 * w_, yb - j * T3_ZONE_ROW, T3_FS, T3_COL["ink"] if j == 0 else ink2,
                       False, "C"))
        ybot = yb - (nl - 1) * T3_ZONE_ROW - 0.25 * cap
        boxes.append((x0, ybot, x0 + w_, yb + cap))
        low = min(low, ybot)
    return sh, low - 0.6, boxes


def _t3_sec_make(cut, after, style, k, seed, tid0=0):
    """T4: one section of cut (today, or with the project when after): page mm, its left edge at x 0, the street
    surface at y 0, k mm per m. v58 (round 3, P08.2, G15): the street in named zones (today the surveyed lanes, with
    the project T3_ZONES), each activity drawn in its zone, the project's street elements, the zones named under the
    cut ground (_t3_zone_band). v61 (round 6, U18, LANGUAGE: ACCURATE, r06_S03 traits): a thin true-scale cut on
    white (no sky), the existing trees the cut sees with their species (G6-10, _t3_trees_seen; generic where none is
    supported), small dark library figures doing the street's activities, short labels on the drawing (_t3_label_band:
    no icon badges, no numbered callouts and no key), no width or height texts (the levels go at the pair's right
    edge, _t3_sec_levels), at most one speech bubble, set only where it touches no figure, tree or plant (else left
    out, counted); every element tagged for its G6-9 group (wl.tg). tid0: the element-id offset of this drawing.
    Returns dict(wl, w = width mm, acts, low = the lowest y used, g6, tree, band = (label shapes, band height, label
    boxes), boxes = the zone-name boxes, els, low_n, bub = bubbles set, bub_drop = bubbles left out)."""
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
    _t3_wl_sync(wl)
    ad = lambda lay_, sh_, kind_, eid_=None, front=False: _t3_wl_add(wl, lay_, sh_, kind_, eid_, front)
    obs = []                                              # boxes a speech bubble keeps clear of (figures, trees, plants)
    # v61 (G6-10): the existing trees the cut sees, by species (plants.py pla_section; generic where none), D9 layers
    for i, tr in enumerate(cut.get("trees_seen") or []):
        lay_ = 0 if tr["d"] <= tr["r"] else (1 if tr["d"] < 0.5 * T3_TREE_SEEN_M else 2)
        if tr["sp"]:
            sh_ = pla_section(tr["sp"], X(tr["x"]), 0.0, k, h_m=tr["h"], crown_m=2.0 * tr["r"], layer=lay_, hires=False,
                              detail=False, style=style, seed=seed + i)
        else:
            sh_ = _t3_tree_generic(X(tr["x"]), 0.0, k, tr["h"], tr["r"], lay_)
        ad("background", sh_, "trees", u"%s %d" % (tr["sp"] or "tree", tid0 + i))
        obs += [b_ for b_ in (_t3_shape_bb(s_) for s_ in sh_) if b_]
    # R2-B (G7, G14): the buildings further along the street as elevations (sf_back_house: walls at the survey
    # height, windows per storey, hipped roof by convention), standing on the street level (flat back profile)
    hs_ = [(max(0.3 * k, X(xa_)), min(W - 0.3 * k, X(xb_)), h_, fl_, d_)
           for xa_, xb_, h_, fl_, d_ in cut.get("houses") or []]
    hs_ = [q_ for q_ in hs_ if q_[1] - q_[0] >= 1.0 * k]
    prof = sf_back_profile([(xa_, xb_, 0.0) for xa_, xb_, _h, _f, _d in hs_], 0.0, W)
    for i, (xa_, xb_, h_, fl_, d_) in enumerate(sorted(hs_, key=lambda q_: -q_[2])):
        ad("background", sf_back_house(xa_, xb_, prof or 0.0, h_, k, layer=1, floors=fl_ or None, d_m=d_),
           "buildings", u"facade %d" % (tid0 + i))
    # the ground and the lanes: carriageway and footways today, one paved level with the project
    if one or not cut["carriage"]:
        lanes = [(sl, sr, "walk")]
    else:
        c0, c1 = cut["carriage"]
        lanes = [(a_, b_, kn) for a_, b_, kn in ((sl, c0, "walk"), (c0, c1, "road"), (c1, sr, "walk")) if b_ - a_ > 0.05]
    sf_ground([(0.0, 0.0), (W, 0.0)], k, depth_m=gm, into=wl)
    _t3_wl_sync(wl, "ground")
    for i, (a_, b_, kn) in enumerate(lanes):
        ad("ground", sf_lane(X(a_), 0.0, b_ - a_, k, kind=kn), "roads" if kn == "road" else "paths",
           u"lane %d" % (tid0 + i))
    # the fronting buildings, cut (M11, survey heights); R2-B: kept inside the drawing, a break line where they go on
    bsh, brk = {-1: [], 1: []}, {}
    for it in cut["bld"]:
        if it[0] == "fill":
            for R_ in it[1]:
                sd_ = -1 if sum(m for m, _z in R_) < 0 else 1
                ring = clip_rect_poly([(X(m), z * k) for m, z in R_], (0.0, -1e6, W, 1e6))
                if len(ring) >= 3:
                    bsh[sd_].append(("poly", ring, it[2], None, 0.0))
                for m, z in R_:
                    for e_, out in ((0.0, X(m) < -0.01), (W, X(m) > W + 0.01)):
                        if out:
                            brk[e_] = max(brk.get(e_, 0.0), z * k)
        else:
            sd_ = -1 if sum(m for m, _z in it[1]) < 0 else 1
            for q_ in _t3_clip_x([(X(m), z * k) for m, z in it[1]], 0.0, W):
                bsh[sd_].append(("line", q_, it[2], it[3]) + ((it[4],) if it[4] else ()))
    for e_, ht_ in brk.items():
        bsh[-1 if e_ <= 0.0 else 1] += _t3_break(e_, 0.0, ht_, k)
    for sd_ in (-1, 1):
        ad("structures", bsh[sd_], "buildings", u"building %s %d" % ("left" if sd_ < 0 else "right", tid0))
    uses, occ, cars = [], [], []
    road, zact = [], None
    if var == "today":
        if cut["carriage"]:
            c0, c1 = cut["carriage"]
            n = max(1, min(2, int((c1 - c0) // 3.0)))
            cars = [c0 + (c1 - c0) * (j + 0.5) / n for j in range(n)]
            zones, road = [(sl, c0), (c1, sr)], [(c0, c1)]
            uses.append(("car", u"Cars", X(0.5 * (c0 + c1)), T3_SEC_CAR[1] * k))
            znames = [z_ for z_ in ((u"Footway", sl, c0), (u"Carriageway", c0, c1), (u"Footway", c1, sr))
                      if z_[2] - z_[1] > 0.05]
        else:
            zones = [(sl, sr)]
            znames = [(u"Street", sl, sr)]
    else:
        zones = [(sl, sr)]
        zd = T3_ZONES[var]                                # v58 (P08.2, G15): the designed zones, named under the cut
        cg = cut["carriage"]
        if var == "calmed" and cg and cg[0] - sl >= 1.0 and sr - cg[1] >= 1.0:
            znames = [(zd[0][0], sl, cg[0]), (zd[1][0], cg[0], cg[1]), (zd[2][0], cg[1], sr)]
        else:
            znames = [(nm_, sl + a_ * width, sl + b_ * width) for nm_, a_, b_ in zd]
        zact = T3_ZONE_OF[var]
        uses.append((None, u"One level, no kerb", X(sl + 0.15 * width), 0.0))   # v61: was callout "one level ..."
        if var in T3_CAR_ZONE:
            _nm, za_, zb_ = znames[T3_CAR_ZONE[var]]
            cars = [min(max(za_ + 1.1, za_ + (0.3 if var == "calmed" else 0.5) * (zb_ - za_)), max(za_ + 1.1, zb_ - 1.1))]
        if cars:
            uses.append(("car", u"Slow cars", X(cars[0]), T3_SEC_CAR[1] * k))
    for i, cx in enumerate(cars):
        sh_ = sf_seat(_t3_car(X(cx), 0.0, k), 0.0)        # G14: wheels on the street
        ad("figures", sh_, "roads", u"car %d" % (tid0 + i))
        obs += [b_ for b_ in (_t3_shape_bb(s_) for s_ in sh_) if b_]
        occ.append((cx - 1.1, cx + 1.1))
    # v58 (round 3, P08.2, G15 "street elements where they exist"): the project's street furniture, each named by a
    # short label on the drawing (v61; was a numbered callout with its reason); today's streets get none
    els = []
    if var == "calmed":
        _nm, za_, zb_ = znames[1]
        els += [("bollard", za_ + 0.15), ("bollard", zb_ - 0.15)]
    elif var == "pedestrian":
        _nm, za_, zb_ = znames[1]
        els.append(("lamp", za_ + 0.3))
    elif var == "shared":
        _nm, za_, zb_ = znames[0]
        els.append(("lamp", zb_ - 0.3))
    if var in ("calmed", "shared"):
        _nm, za_, zb_ = znames[2]
        if zb_ - za_ >= 1.6:
            els.append(("rack", za_ + 0.3))
    seen_el = set()
    for i, (kn_, ex_) in enumerate(els):
        if kn_ == "bollard":
            esh = sf_bollard(X(ex_), 0.0, k)
            occ.append((ex_ - 0.3, ex_ + 0.3))
        elif kn_ == "lamp":
            esh = sf_lamp(X(ex_), 0.0, k, side=1)
            occ.append((ex_ - 0.3, ex_ + 0.3))
        else:
            esh = sf_bike_rack(X(ex_), 0.0, k, side=1)
            occ.append((ex_ - 0.1, ex_ + SF_STREET["rack_l"] + 0.1))
        ad("structures", esh, "roads", u"%s %d" % (kn_, tid0 + i))   # behind the people (structures before figures)
        if kn_ not in seen_el:
            seen_el.add(kn_)
            uses.append((None, T3_EL_WORD[kn_], X(ex_ + (0.35 if kn_ == "rack" else 0.0)), 0.0))
    # R2-B (G9): the project's planting where the street leaves room: one mixed group (plants.py pla_group_section,
    # street species of the dry band), on a planting strip clear of the cars and the street elements
    tx, trees, ptags, th_ = None, [], [], 0.0
    if var in ("pedestrian", "shared") and width >= T3_SEC_TREE_MIN:
        _nm, za_, zb_ = znames[T3_TREE_ZONE[var]]        # v58 (P08.2): the planting in its own zone
        p0, p1 = za_ + 0.25, zb_ - 0.25
        sh_, placed, grp = pla_group_section(X(p0), X(p1), 0.0, k, t0=0.50, t1=0.85,
                                             mix={"plane": 1.0, "chaste": 1.0, "rosemary": 0.8,    # v58: no 20 m ash
                                                  "lavender": 0.8}, seed=seed,
                                             layers=(sf_tree_level("p08")["layer"],), style=style,   # v61: page p08
                                             density=0.8, avoid=[(X(c_ - 1.1), X(c_ + 1.1)) for c_ in cars] +
                                             [(X(ex_ - 0.5), X(ex_ + 0.5)) for _kn, ex_ in els])   # v58: + the lamp
        if placed:
            ad("vegetation", sh_, "plants", u"planting %d" % tid0)
            obs += [b_ for b_ in (_t3_shape_bb(s_) for s_ in sh_) if b_]
            trees += [q_ for q_ in placed if _pla_canopy(q_[0])]
            can = [q_ for q_ in placed if _pla_canopy(q_[0])] or placed
            tq = max(can, key=lambda q_: q_[2])
            tx = tq[1] / k + xl
            th_ = tq[2]
            for q_ in placed:
                if _pla_canopy(q_[0]):
                    occ.append((q_[1] / k + xl - 0.35, q_[1] / k + xl + 0.35))
            ptags = sorted(set(t_ for g_ in grp for t_ in g_[4]))
            uses.append((None, u"Planting for shade" if "shade" in ptags else u"Planting", X(tx), tq[2] * k))
        else:
            LOG.append(u"Street sections {}: no planting group fits the {:.1f} m strip.".format(cut["name"], p1 - p0))
    # v59 (round 4, G-R4-5.2, D7): the low layer of shrubs and flowers in every section WITH the project (plants.py
    # pla_low_section; the dry street species T3_LOW_MIX), one depth layer behind the cut, along the zone that holds
    # the planting (pedestrian, shared) or the seats (calmed). Today's streets get none (no street planting surveyed).
    low_n = 0
    if var in T3_LOW_ZONE:
        _nm, za_, zb_ = znames[T3_LOW_ZONE[var]]
        if zb_ - za_ >= 1.0:
            lsh, lpl = pla_low_section(X(za_ + 0.2), X(zb_ - 0.2), 0.0, k, t0=0.85, t1=1.0, seed=seed + 31, layer=1,
                                       density=0.8, mix=T3_LOW_MIX)
            if lpl:
                ad("background", lsh, "plants", u"low planting %d" % tid0)
                obs += [b_ for b_ in (_t3_shape_bb(s_) for s_ in lsh) if b_]
                low_n = len(lpl)
        if not low_n:
            LOG.append(u"Street sections {} ({}): no low planting fits its zone.".format(cut["name"], var))
    # walkers further along the street (D9 layers 2 and 1: smaller, paler), by what each zone is for (figures.py
    # fig_place_zones, style a cutouts only, seated: G14, G10); those who stay look at each other, walkers keep on
    zk = "market_ground" if var == "pedestrian" else "walkway"
    for lay in (2, 1):
        sh_, _pl = fig_place_zones([(zk, X(a_), X(b_)) for a_, b_ in zones if b_ - a_ >= 1.5], 0.0, k,
                                   seed=seed + 5 * lay, layer=lay, style="a", density=0.5, max_per_zone=2,
                                   focus=lambda _k, xa_, xb_: 0.5 * (xa_ + xb_))
        ad("background", sh_, "people", u"walkers %d %d" % (tid0, lay))
        obs += [b_ for b_ in (_t3_shape_bb(s_) for s_ in sh_) if b_]
    # the people at the cut (1.75 m): the street's interactions (G10)
    script = T3_SCRIPT[var]
    acts, bub = [], []
    zcount, zseen = {}, {}                                # v58 (P08.2): acts per designed zone, spread inside it
    for act in script:
        if zact and act in zact:
            zcount[zact[act]] = zcount.get(zact[act], 0) + 1
    for i, act in enumerate(script):
        f, head = T3_ACT[act]
        zs = road if (act == "bike" and var == "today") else zones
        if not zs:
            continue
        zi = zact.get(act) if zact else None
        if zi is not None:                                # v58 (P08.2, G15): the act in its own zone first
            _nm, za_, zb_ = znames[zi]
            j_ = zseen.get(zi, 0)
            zseen[zi] = j_ + 1
            prefer = za_ + (zb_ - za_) * (j_ + 0.5) / zcount[zi]
            if act == "bench" and tx is not None:
                prefer = tx + 0.4 + 0.5 * f
            zs_own = [(za_, zb_)]
        elif act == "kerb" and cut["carriage"]:
            prefer, zs_own = cut["carriage"][0] - 0.5 * f - 0.2, None
        elif act == "bench" and tx is not None:
            prefer, zs_own = tx + 0.4 + 0.5 * f, None
        elif act == "bike" and var == "today":
            prefer, zs_own = 0.5 * (zs[0][0] + zs[0][1]), None
        else:
            prefer, zs_own = sl + width * (i + 0.5) / len(script), None
        a_ = _t3_take(f, zs_own, occ, prefer) if zs_own else None
        if a_ is None:
            a_ = _t3_take(f, zs, occ, prefer)
            if a_ is not None and zs_own:
                LOG.append(u"Street sections {} ({}): {} does not fit its zone \"{}\"; drawn where the street "
                           u"leaves room.".format(cut["name"], var, act, znames[zi][0]))
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
        elif act == "market":
            xf = X(a_ + 1.45) if fac > 0 else X(a_ + f - 1.45)
            sh_ = fig_stall(xf, 0.0, k, facing=fac, style=style, seed=seed + i)
            hx = xf + fac * 0.45 * k
        else:
            sh_ = fig_side({"kerb": "watch"}.get(act, act), X(cx), 0.0, k, facing=fac, style=style, pick=seed + i)
        sh_ = sf_seat(sh_, 0.0, sink=True)                # G14: feet, stall legs, bench on the street level
        ad("figures", sh_, "people", u"%s %d" % (act, tid0 + i))
        obs += [b_ for b_ in (_t3_shape_bb(s_) for s_ in sh_) if b_]
        acts.append(act)
        bub.append((act, hx, head * k, fac))
        if act in T3_ACT_USE:
            uses.append(T3_ACT_USE[act] + (X(cx), head * k))
    # v58 (round 3, P08.2, R07): the zones named under the cut ground (v61: no width chain, no width label)
    zsh, zlow, zbox = _t3_zone_band(znames, X, k, -gm * k - 0.8, W, var == "today")
    ad("labels", zsh, "labels", u"zones %d" % tid0)
    tbox = list(zbox)
    # D4 a: one speech bubble, toward the street's middle, inside the drawing, never on a label; v61 (frames page8
    # §4): never on a figure, tree or plant either: a bubble with no clear place is left out (counted)
    wfn = lambda s, size: tw(s, size * R28MV_CAP, kd)
    boxes, n_bub, n_drop = list(tbox), 0, 0
    hit = lambda bb, Q, g: any(bb[0] < q[2] + g and q[0] < bb[2] + g and bb[1] < q[3] + g and q[1] < bb[3] + g
                               for q in Q)
    for act, hx, hy, fac in bub:
        t_ = T3_BUBBLES.get((var, act))
        if not t_ or n_bub >= 1:
            continue
        got = False
        for sd_ in (fac, -fac):
            sh_ = fig_bubble(t_, hx, hy + 0.25 * k, size=T3_FS, side=sd_, width_fn=wfn)
            bb = _t3_bb(sh_[0][1])
            if bb[0] < 0.0 or bb[2] > W or hit(bb, boxes, 0.6) or hit(bb, obs, 0.3):
                continue
            boxes.append(bb)
            n_bub += 1
            ad("labels", sh_, "labels", u"bubble %d" % tid0)
            got = True
            break
        if not got:
            n_drop += 1
    g6 = sf_assert_g6(k, trees=trees, buildings=[(u"{} side {}".format(cut["name"], sg),
                                                   cut["side"][sg]["g6"][0], cut["side"][sg]["g6"][1])
                                                  for sg in (-1, 1) if cut["side"][sg].get("g6") and
                                                  cut["side"][sg]["g6"][0] is not None], strict=False)
    # v57 (M8, D9, G14): the houses further down the street (cut["back"]), farthest first and behind everything else
    # of the background layer, as elevations standing on the street level, D9 layer 1 nearer than the band's middle,
    # else 2 (paler); a house whose roof would rise over the drawing is left out (R2-C)
    top_ = _t3_top(wl.shapes())
    dmid = 0.5 * (SF_BACK_BAND[0] + SF_BACK_BAND[1])
    bk_, nb_ = [], 0
    for xa_, xb_, h_, fl_, d_ in cut.get("back") or []:
        a_, b_ = max(0.3 * k, X(xa_)), min(W - 0.3 * k, X(xb_))
        if b_ - a_ < 2.0 * k:
            continue
        hh_ = sf_back_house(a_, b_, 0.0, h_, k, layer=1 if d_ < dmid else 2, floors=fl_, d_m=d_)   # v59 (G-R4-5.3)
        if not hh_ or _t3_top(hh_) > top_:
            continue
        bk_.append(hh_)
        nb_ += 1
    for i, hh_ in enumerate(reversed(bk_)):              # front-inserted one by one: the farthest ends up first
        ad("background", hh_, "buildings", u"back house %d" % (tid0 + i), front=True)
    if not after:
        LOG.append(u"Street sections {}: {} background houses {:.0f}-{:.0f} m down the street drawn ({} in the band; "
                   u"higher than the drawing left out).".format(cut["name"], nb_, SF_BACK_BAND[0], SF_BACK_BAND[1],
                                                                 len(cut.get("back") or [])))
    # v61 (ACCURATE): no designed sky: the cut stands on white paper (r06_S03)
    band = _t3_label_band(uses, W)                        # v61: short labels right above their elements
    return dict(wl=wl, w=W, acts=acts, low=zlow - 1.0, g6=g6, tree=tx is not None, band=band, boxes=tbox,
                els=len(els), low_n=low_n, bub=n_bub, bub_drop=n_drop)


def _t3_sec_id(i):
    """R2-B: the key map name of the i-th street cut (R1, R2 ...: R = road; the stream sections are S1-S8)"""
    return u"R%d" % (i + 1)


def _t3_sec_ends(cut):
    """R2-B (M4): the cut's two ends in survey m, end1 = the drawing's left end (left of the street's way), so the
    section looks along the street (look +1). v61: the key map (km_keymap) and street_cuts.json take these."""
    (xl, xr), _st = _t3_sec_extent(cut)
    p, nl, nr = cut["p"], cut["side"][-1]["n"], cut["side"][1]["n"]
    return (p[0] + nl[0] * -xl, p[1] + nl[1] * -xl), (p[0] + nr[0] * xr, p[1] + nr[1] * xr)


def _t3_street_sections(S, B, x, y, w, U, M):
    """T3a (D3 b, Aras 29 Oct 18:53): before / after cross-sections of one street per road change of the masterplan
    (kept, calmed, pedestrian, shared), each cut where the survey measured the street (_t3_sec_cut). A kept road is
    drawn once (no change). v61 (round 6, U18 "alttaki bunlar buyutulcek", P-9 option A; LANGUAGE: ACCURATE, r06_S03
    traits): ONE row, the four streets at ONE scale (T3_SEC_DENS: the largest whose row fills at most the booklet
    width), R label rows level, every drawing on ONE ground line, one scale bar per pair on one line, the levels at
    each pair's right edge; each pair its own crop street_R1..R4 (items sb_street_R1..R4, page p08), the strip's
    title a note (sb_street_title_n1); the legend a stand-alone item (SB_LEG sb_street_legend), the key map "Where
    each street is cut" through common/keymap.py km_keymap (SB_KM sb_street_keymap; the board drawing _t3_sec_key is
    gone); the cut ends and change classes to cached/selinus_board/street_cuts.json (the masterplan draws them).
    Returns the y below."""
    # LANGUAGE: ACCURATE (BRIEF §3, PLAN §2.3: p08 street cuts R1-R4)
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
    if not groups:                                        # missing data: never a silent empty p08
        raise RuntimeError(u"Street sections: nothing to draw (no masterplan road ({}) runs along a street the survey "
                           u"measured; roads from {})".format(len(M.get("roads") or []), M.get("source", u"?")))
    for c_ in groups:                                     # once per cut: species counted once (G6-10), the levels
        c_["trees_seen"] = _t3_trees_seen(S, c_, "p08")
        c_["levels"], c_["lv_abs"] = _t3_sec_levels(S, c_)
    ext = dict((id(c_), _t3_sec_extent(c_)[0]) for c_ in groups)
    lvw = dict((id(c_), _t3_lv_w(c_)) for c_ in groups)

    def row_w(den):
        """mm: the one row at 1:den: every pair (today + with the project), its level column, the even gaps"""
        k_ = 1000.0 / den
        tot = 0.0
        for c_ in groups:
            n = 1 if c_["change"] == "kept" else 2
            tot += n * (ext[id(c_)][1] - ext[id(c_)][0]) * k_ + (n - 1) * T3_SEC_GAP + lvw[id(c_)]
        return tot + (len(groups) - 1) * T3_SEC_PAIR_GAP
    den = next((d_ for d_ in T3_SEC_DENS if row_w(d_) <= T3_SEC_ROW_W), None)
    if den is None:
        den = T3_SEC_DENS[-1]
        wn_warn("p08", "layout", u"street cuts: one row needs {:.0f} mm at 1:{:,} (the booklet row is {:.0f} mm)".format(
            row_w(den), den, T3_SEC_ROW_W))
    k = 1000.0 / den                                      # mm per m on the booklet page
    LOG.append(u"Street sections at 1:{:,} (one scale for all {} streets, one row {:.0f} mm): ".format(
        den, len(groups), row_w(den)) + u"; ".join(
        u"{} {} ({}) {:.1f} m {}{}; buildings cut {}, behind {}".format(
            _t3_sec_id(i), c_["name"], c_["change"], c_["w"], c_["w_src"],
            u", carriageway {:.1f} m".format(c_["carriage"][1] - c_["carriage"][0]) if c_["carriage"] else u"",
            sum(1 for s_ in (-1, 1) if c_["side"][s_].get("back")), len(c_["beyond"])) for i, c_ in enumerate(groups)))
    PU = _T3Put(B, x, 0.0, kb, L)
    old_tri = sf_triangles(walls=False, aggregate=False)  # G14 / U22: no meaningless triangles in these sections
    made = []
    for gi, c_ in enumerate(groups):
        n = 1 if c_["change"] == "kept" else 2
        made.append((gi, c_, [(j, n, _t3_sec_make(c_, j == 1, "a", k, 17 * gi + j, tid0=100 * j)) for j in range(n)]))
    alls = [s_ for _g, _c, ss in made for _j, _n, s_ in ss]
    top = max([_t3_top(s_["wl"].shapes()) for s_ in alls] + [h_ * k for c_ in groups for _n, _v, h_ in c_["levels"]])
    bh = max(s_["band"][1] for s_ in alls)
    low0 = min(s_["low"] for s_ in alls)
    n_bub = sum(s_["bub"] for s_ in alls)
    ytop = y / kb                                         # mm
    # the strip's title and sub line: a text-only crop (note item sb_street_title_n1), above the pairs' crops
    with B.kind("labels", "title"):
        PU.text(u"The same surveyed width, given back to people: each street today and with the project", 0.0,
                ytop - 4.0, 11.0, T3_COL["ink"], True)
        PU.text(u"Today as surveyed, then with the project, frontage to frontage · one scale for all streets" +
                (u" · speech bubbles: {}".format(FIG_BUBBLE_TAG.lower()) if n_bub else u""), 0.0, ytop - 8.5, 7.0,
                T3_COL["ink2"], False)
    crop_panel("street_title", x, (ytop - 10.0) * kb, x + T3_SEC_ROW_W * kb, y, u"", ix_page="p08")
    yrow = ytop - 13.0                                    # the R label row, level for all four
    gy = yrow - 8.0 - bh - 1.5 - top                      # ONE ground line (street surface) for every drawing
    yb = gy + top + 1.5                                   # the foot of the label bands
    ybar = gy + low0                                      # ONE line for the scale bars
    Lm = 5.0 if den <= 250 else 10.0
    cx, g6, bot, ab_all, n_drop, used = 0.0, [], None, True, 0, []
    for gi, c_, secs in made:
        rid = _t3_sec_id(gi)
        x0p = cx
        xl_, W_ = cx, 0.0
        for j, n, sec in secs:
            sub = u"today = with the project" if n == 1 else (u"with the project" if j == 1 else u"today")
            with B.kind("labels", u"%s %s" % (rid, sub)):
                PU.text(sub, cx, yrow - 6.5, 7.0, T3_COL["ink2"], False)
            i0_s = sb_mark(B)
            for li, lay in enumerate(WAT_LAYERS):
                _t3_put_tagged(B, PU, sec["wl"], lay, cx, gy, 40 + 2 * li)
            ish, _bh, _ibox = sec["band"]
            with B.kind("labels", u"%s %s labels" % (rid, sub)):
                PU.put(_t3_shift(ish, cx, yb), 60)
            sb_keep(B, (x + cx * kb, (gy + sec["low"]) * kb, x + (cx + sec["w"]) * kb,
                        max(yb + _bh, gy + top) * kb), u"%s %s section" % (c_["name"], sub), "section", i0_s)
            g6 += sec["g6"]
            n_drop += sec["bub_drop"]
            if len(set(sec["acts"])) < 3:
                LOG.append(u"Street sections {} ({}): only {} interaction(s) fit the surveyed width: {}.".format(
                    c_["name"], sub, len(set(sec["acts"])), u", ".join(sec["acts"]) or u"none"))
            xl_, W_ = cx, sec["w"]
            cx += sec["w"] + (T3_SEC_GAP if j < n - 1 else 0.0)
        # the levels at the pair's right edge (ACCURATE): values with the triangle, spread, never stacked
        lv = [(n_, v_, h_ * k) for n_, v_, h_ in c_["levels"]]
        lsh = sf_level_marks((0.0, low0, W_, top), lv, side="R", page="p08",
                             cols=dict((n_, T3_LV_INK) for n_, _v, _h in lv))
        with B.kind("levels", u"%s levels" % rid):
            PU.put(_t3_shift(lsh, xl_, gy), 64)
        ab_all = ab_all and c_["lv_abs"]
        right = xl_ + W_ + lvw[id(c_)]
        # the R label row: the pair's heading over the pair, a rule in its road change's hue (G6-6) above it
        avail = right - x0p
        alts_ = [u"{} · {} · {}".format(rid, c_["name"], T3_CHANGE_TXT.get(c_["change"], c_["change"])),
                 u"{} · {}".format(rid, c_["name"]), rid]
        head_ = next((a_ for a_ in alts_ if fm_width(a_, 8.5, True) <= avail), None)
        if head_ is None:                                 # warns and sets the shortest form
            wn_warn("p08", "heading", u"\"{}\" ({:.0f} mm) does not fit over its street ({:.0f} mm)".format(
                alts_[-1], fm_width(alts_[-1], 8.5, True), avail))
            head_ = alts_[-1]
        elif head_ != alts_[0]:
            LOG.append(u"Street sections {}: heading shortened to fit {:.0f} mm: \"{}\".".format(rid, avail, head_))
        with B.kind("labels", u"%s heading" % rid):
            PU.text(head_, x0p, yrow - 3.0, 8.5, T3_COL["ink"], True)
        with B.kind("annotations", u"%s change" % rid):
            PU.line([(x0p, yrow - 0.3), (right, yrow - 0.3)], _t3_change_hex(c_["change"]), 0.45, order=46)
        used.append(c_["change"])
        # one scale bar per pair, all on one line, 1 mm in from the pair's left edge
        with B.kind("annotations", u"%s scale bar" % rid):
            sb = draw_scalebar_bk(B, x + (x0p + 1.0) * kb, ybar * kb, k * kb, Lm, kb, L)
        bot = sb if bot is None else min(bot, sb)
        crop_panel("street_" + rid, x + (x0p - 0.5) * kb, sb - 0.5 * kb, x + (right + 0.5) * kb, (yrow + 0.5) * kb,
                   u"", den, ix_page="p08")
        CROP_PANELS[-1]["bk_w"] = right - x0p + 1.0
        LOG.append(u"section p08 {} ACCURATE · {} ({}) · crop street_{} {:.0f} x {:.0f} mm at 1:{:,}; levels {}; "
                   u"existing trees {} ({} by species)".format(
                       rid, c_["name"], c_["change"], rid, right - x0p + 1.0, yrow + 0.5 - sb / kb + 0.5, den,
                       u", ".join(u"%s %+.2f" % (n_, v_) for n_, v_, _h in c_["levels"]),
                       len(c_["trees_seen"]), sum(1 for t_ in c_["trees_seen"] if t_["sp"])))
        cx = right + T3_SEC_PAIR_GAP
    sf_triangles(**old_tri)
    if g6:
        wn_warn("p08", "g6", u"street sections: " + u"; ".join(sorted(set(g6))))
    if cx - T3_SEC_PAIR_GAP > T3_SEC_ROW_W + 0.5:
        wn_warn("p08", "layout", u"street cuts: the row runs {:.0f} mm past the booklet width".format(
            cx - T3_SEC_PAIR_GAP - T3_SEC_ROW_W))
    if not ab_all:
        LOG.append(u"WARNING p08 levels: no survey terrain on this run: the street cuts' levels are given above the "
                   u"street (+0.00), not above sea.")
    LOG.append(u"Street sections: speech bubbles {} set, {} left out (no place clear of figures, trees and plants; "
               u"frames page8 §4).".format(n_bub, n_drop))
    LOG.append(u"Street sections: drawn {}".format(len(alls)))
    LOG.append(u"Street sections: " + fig_set_line(False))
    cl = cut_log_line()
    if cl:
        LOG.append(u"Street sections: " + cl)
    g14 = sf_g14_line()
    if g14:
        LOG.append(u"Street sections: " + g14)
    LOG.append(sb_tree_log("p08"))
    # v61 (PLAN §5): the cut ends (survey m) and change classes, as the strip draws them, for the masterplan (S9)
    try:
        out_ = {}
        for i, c_ in enumerate(groups):
            a_, b_ = _t3_sec_ends(c_)
            out_[_t3_sec_id(i)] = {"a": [round(a_[0], 2), round(a_[1], 2)], "b": [round(b_[0], 2), round(b_[1], 2)],
                                   "change": c_["change"], "street": c_["name"]}
        os.makedirs(SELINUS_RES_DIR, exist_ok=True)
        with open(T3_CUTS_FILE, "w", encoding="utf-8") as fh:
            json.dump(out_, fh, ensure_ascii=False, indent=1, sort_keys=True)
        LOG.append(u"street_cuts.json: {} cuts ({}) -> {}".format(len(out_), u", ".join(
            u"%s %s" % (k_, v_["change"]) for k_, v_ in sorted(out_.items())), T3_CUTS_FILE))
    except Exception:
        wn_warn("p08", "export", u"street_cuts.json not written: " + traceback.format_exc().strip().splitlines()[-1])
    # v61 (G6-5): the key map "Where each street is cut": THE key-map module, exported as the booklet's item
    try:
        cuts_ = []
        for i, c_ in enumerate(groups):
            a_, b_ = _t3_sec_ends(c_)
            cuts_.append((a_, b_, (_t3_sec_id(i), _t3_sec_id(i) + u"'"), 1))
        SB_KM["sb_street_keymap"] = ("p08", km_keymap("p08", cuts=cuts_, w_mm=T3_KM_W, h_mm=T3_KM_H, log=LOG))
    except Exception:
        wn_warn("p08", "keymap", u"street cuts key map not built: " + traceback.format_exc().strip().splitlines()[-1])
    # v61 (G6-6, H1 p08 / H2 note 2): the strip's legend as a stand-alone item, hue table colours only
    ents = [(dict(kind="line", colour=_t3_change_hex(ch)), T3_CHANGE_TXT[ch]) for ch in T3_SEC_ORDER if ch in used]
    ents.append((dict(kind="line", colour=T3_LV_INK), u"level, m above sea" if ab_all else u"level, m above the street"))
    SB_LEG["sb_street_legend"] = ("p08", ents)
    LOG.append(hue_log("p08"))
    return bot - 1.0 * kb


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
            col = mv_ramp(r28mv_seq(), seq_t(v, 100.0))       # v61 (G6-6): MOV ramp
        Q = V.P(P)                                        # T3a (p.07): a pale halo under each piece (smoother)
        B.line(Q, mix(col, WHITE, 0.6), L, order - 1, MV_W[cls] * scale * 2.2)
        B.line(Q, col, L, order, MV_W[cls] * scale)


def draw_how_people_use_it(S, B, x, y, w, U):
    """S2: how people move and what they reach (was 07 commercial spines, 09 civic constellations, diagrams D3, D5, D7
    and the movement script's panels). v46 (Prompt 3, p.8, analysis): the whole site frame at 1:10,000 on the frame's
    axes in the masterplan's base, the scale bar and north arrow under it; no proposed spine or stops (analysis
    only); walking and driving today as their own maps at the same scale under it (draw_mv_today). Returns the y below.
    v58 (round 3, P07.1-P07.4, G3, G16): the streets the column names (the primary spines, the busiest street) are
    numbered on the map (_t3_marks, reading order); the map's legend, the numbered list and the graphics stand in the
    column right beside it (r28mv_note_top), none under the crop; the captions are the short takeaways; the working
    areas carry the bridges' names (bridge_name), never a K-code; one overlap FLAG for the page ("p07")."""
    L = "LU_BOARD::HowPeopleUseIt"
    F = S.F
    MV = movement(S)
    del T3_P07_BOXES[:]                                   # v58 (G3): the p.07 text boxes of this run
    T3_HER_DRAWN.clear()
    R = MV.get("R")
    # T3a (package B p.07, G1): title-like captions that state the takeaway (were "How people use it / Walking today /
    # Driving today"); the top one only claims what the board's own rank correlation shows
    rho_ = (MV.get("rho") or {}).get("walk_b")
    t_top = (u"Shops line the streets people walk most" if rho_ is not None and rho_ >= 0.3 else
             u"Shops, services and everyday walks on one map")
    # T4 (30 Oct, p7 G1): the map's own heading inside its crop; the takeaway stays its caption
    V, k, ss, r = b_view(F, x, _t3_map_head(B, x, y, U, u"Shops, services and everyday walks", L), U)   # 1:10,000
    T3_P07_BOXES.append(_t3_head_box(x, y, U, u"Shops, services and everyday walks"))
    i0_m = sb_mark(B)                                     # v59 closing (G-R4-1): the map's own texts from here
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
    with B.kind("ground", "paper"):
        B.fill([rect(*r)], WHITE, L, 1)
    use_cats = ("commercial", "mixed", "institutional", "religious")
    _t3_base(S, CB, V, k, L)
    with B.kind("buildings"):                             # v61 (G6-6, G6-9): uses by the hue table, each its group
        mini_buildings(S, CB, V, L, lambda u: _t3_use_col(u["cat"]) if u["cat"] in use_cats else None, order=10)
    # commerce spines: a broad pale band in the street, under the buildings; v61 (G6-6): MOV lines, the primary
    # darker (MOV r3) than the secondary (MOV r4), both lighter than the commerce buildings (MOV r1)
    cc = _t3_use_col("commercial")
    sp1, sp2 = C(hue("MOV", 3)), C(hue("MOV", 4))
    with B.kind("roads", "commercial spines"):
        for g in S.corr_primary:
            for P in g["Ps"]:
                CB.line(V.P(P), sp1, L, 9, bk_lw(1.8, k))
        for g in S.corr_secondary:
            for P in g["Ps"]:
                for d in dashes(V.P(P), 3.0 * k, 1.8 * k):
                    CB.line(d, sp2, L, 9, bk_lw(1.1, k))
    # streets: line width = OSM class, colour = combined movement potential today
    if R:
        with B.kind("roads"):
            draw_mv_streets(CB, V, mv_runs(S, R, "comb_b", F), L, 14)
    # v46 (Prompt 3): the proposed streamside spine and its stops are no longer drawn here (an analysis map)
    # civic constellations; v61 (G6-6): civic PUB r2, dashed
    hc = C(hue("PUB", 2))
    with B.kind("annotations", "civic constellations"):
        for cl in S.clusters:
            for run in F.clip_line(cl["P"] + [cl["P"][0]]):
                for d in dashes(V.P(run), 2.0 * k, 1.4 * k):
                    CB.line(d, hc, L, 16, bk_lw(0.18, k))
    # services (Overture places, as D5) and the walks to the nearest of each function (as D7)
    fcol = dict((f, _t3_fun_col(f)) for f, let, c, lab in WALK_FUN)   # v61 (G6-6): T3_FUN_HUE
    n_pl = {}
    if ctx is not None:
        with B.kind("hubs"):                              # v61 (G6-9): every service place its own element
            for px_, py_, f, nm, conf, cat in [p[:6] for p in ctx.places]:
                if F.inside(px_, py_):
                    n_pl[f] = n_pl.get(f, 0) + 1
                    cx, cy = V.p(px_, py_)
                    CB.fill([circle_pts(cx, cy, 0.45 * k, 8)], _t3_fun_col(f, nm) if f == "heritage" else
                            fcol.get(f, INK2), L, 30)
    walk_c = C(hue("MOV", 2))                             # v61 (G6-6): walks are movement (MOV r2, dashed)
    dest, av_ = {}, []
    if D7:
        with B.kind("paths", "walks to the nearest"):
            for k_, best in D7["res"].items():
                for f, r_ in best.items():
                    if r_["pts"]:
                        for run in F.clip_line(r_["pts"]):
                            for d in dashes(V.P(run), 0.6 * k, 0.6 * k):
                                CB.line(d, walk_c, L, 32, bk_lw(0.16, k))
                    dest[(f, round(r_["x"]), round(r_["y"]))] = r_
        rr = 1.9 * k
        let_of = dict((f, let) for f, let, c, lab in WALK_FUN)
        # v59 (round 4, G-R4-1, G-R4-7): every letter by mk_marker (centred, in its function's colour); two places
        # closer than a letter: the later one beside its place (8 directions, one marker apart), never on another
        taken_ = []
        for (f, _, _), r_ in dest.items():
            if F.inside(r_["x"], r_["y"]):
                px, py = V.p(r_["x"], r_["y"])
                let_ = let_of.get(f, "?")
                d_ = 2.0 * rr + 0.6 * k
                fc_ = _t3_fun_col(f, r_.get("name") or r_.get("nm")) if f == "heritage" else fcol.get(f, INK)
                for ox, oy in [(0.0, 0.0)] + [(d_ * math.cos(j_ * math.pi / 4.0), d_ * math.sin(j_ * math.pi / 4.0))
                                              for j_ in range(8)]:
                    bx_ = mk_marker((px + ox) / k, (py + oy) / k, let_, crop_hex(fc_), size_pt=7.0,
                                    r_min=rr / k)[1]
                    if not any(tp_hit(bx_, q_, 0.6) for q_ in taken_):
                        break
                taken_.append(bx_)
                with B.kind("labels", u"service %s %d" % (let_, len(taken_))):
                    r28mv_mk(B, px + ox, py + oy, let_, fc_, k, L, order=62, size_pt=7.0, r_min=rr / k)
                av_.append((px + ox, py + oy))
        for nm, sh, a in stage_areas(S):                    # where each walk starts: a name, never an outline
            cx, cy = shoelace(a["P"])[1:]
            px, py = V.p(cx, cy)                          # v40: plain text, no white box (Aras 25 Oct 21:41)
            nm_ = _t3_stage_name(nm, sh)                  # v58 (G16): the bridge's name, never "K4"
            hn_ = bk_hk(8.0, k)                           # v59 (G-R4-1): a name clear of the letters and names
            for oy in (0.0, 1.6 * hn_, -1.6 * hn_, 3.2 * hn_, -3.2 * hn_):
                bn_ = tuple(v_ / k for v_ in r28mv_tbox(nm_, px, py + oy, hn_, True, "C"))
                if not any(tp_hit(bn_, q_, 0.6) for q_ in taken_):
                    break
            taken_.append(bn_)
            py += oy
            with B.kind("labels", nm_):
                CB.text(nm_, px, py, hn_, INK, L, order=64, font=FONT_TITLE, bold=True, align="C")
            av_.append((px, py))
            if r[0] <= px <= r[2] and r[1] <= py <= r[3]:
                T3_P07_BOXES.append(tuple(v_ / k for v_ in r28mv_tbox(nm_, px, py, bk_hk(8.0, k), True, "C")))
    with B.kind("annotations"):
        draw_map_annotations(S, B, V, U, rh=bk_hk(8.0, k))
    with B.kind("labels", "street numbers"):
        nums_top = _t3_top_marks(S, B, V, R, MV, F, k, r, L, av_)    # v58 (P07.3): the named streets numbered
    with B.kind("frame", "map frame"):
        b_frame(B, r, k, L)
    sb_keep(B, r, u"p07 movement map", "map", i0_m)       # v59 closing (G-R4-1): its names may, no other text
    foot = b_foot(B, F, x, r[1], ss, k, L)                # v46: under the map, never on it
    crop_r = (x - 0.5 * k, foot - 0.5 * k, r[2] + 0.5 * k, y)     # the booklet crop of the plan, with its heading
    # v58 (P07.1): drw_mv_note_1 (legend, numbered streets, graphics, note) is drawn once its legend rows exist (below)
    yy = foot - 3.0 * U
    # walking and driving today, only the key streets in colour and named (v44, Aras 27 Oct: "highlight only the key
    # axes and roads"); v46: each its own map at the theme's one scale, stacked under the plan
    if R:
        # v50 (MIRAQUA 28 Oct, P07.3): the index on every street piece, the busiest named (draw_mv_today, 15i)
        # T3a (package B p.07): sharper, title-like names that state what each map shows (G1)
        # T4 (30 Oct, p7 G1): each map its own heading ("Pedestrian flow", "Vehicle traffic"), the takeaway its caption
        for key_, head, lead, mode in (("walk_b", u"Pedestrian flow · where feet go", u"Where feet go", u"walking"),
                                       ("car_b", u"Vehicle traffic · where cars go", u"Where cars go", u"driving")):
            rows_k = mv_key_rows(MV, key_)
            two = _t3_names(rows_k)
            # v59 (round 4, P07.1): the caption and its shorter forms (one street, the lead), the first that fits
            title = ((u"{}: {} {} the most {} routes".format(lead, two, u"carry" if len(rows_k) >= 2 else u"carries",
                                                            mode),) if two else ()) + \
                ((u"{}: {} carries the most {} routes".format(lead, _t3_names(rows_k, 1), mode),)
                 if len(rows_k) >= 2 else ()) + (lead,)
            # v58 (P07.2): the caption is the takeaway only (one line inside the map's width); what the colours mean
            # is in the column beside the map
            yy = draw_mv_today(S, B, x, yy, U, R, MV, key_, head, title) - 2.0 * U
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
            B.text("from the " + _t3_stage_name(nm, sh), V.X0 + cw0 + j * cw, yy, h, INK2, L, bold=True)   # v58 G16
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
            leg.append(("thick", mv_ramp(r28mv_seq(), seq_t(v, 100.0)), (u"{} · the busiest street piece" if v == 100
                                                                         else u"{} of 100").format(v)))
    leg += [("hdr", None, "SHOPS AND CIVIC LIFE " + r_com),
            ("thick", sp1, "Primary commercial spine"),
            ("dash", sp2, "Secondary commercial spine")]
    leg += [("box", _t3_use_col("commercial"), "Commerce"), ("box", _t3_use_col("mixed"), "Mixed use"),
            ("box", _t3_use_col("institutional"), "Civic"), ("box", _t3_use_col("religious"), "Worship"),
            ("dash", hc, "Constellation · 3+ in 100 m")]
    if ctx is not None:
        leg += [("hdr", None, "SERVICES AND WALKS " + r_com)]
        for f, let, c, lab in WALK_FUN:
            if n_pl.get(f):                               # T4 (G1): the roundel's letter in its row
                leg.append(("dot", fcol[f], u"{} · {} · {} places".format(let, lab, n_pl[f])))
        leg.append(("dash", walk_c, "Walk to the nearest (letter at the place)"))
    ly = draw_legend_items(B, leg, x, yy - 0.4 * U, mw, U, L, h=0.4)
    # v58 (P07.1, P07.2): the takeaway as the short caption, no legend under the crop: it is the column's first block
    t_top = _t3_cap_fit(t_top, (crop_r[2] - crop_r[0]) / k, "movement")   # v59 (round 4, P07.1)
    crop_panel("movement", crop_r[0], crop_r[1], crop_r[2], crop_r[3], t_top, crop_scale(ss), None)
    # v61 (G6-6, H1 p07): grouped by category of the hue table (legend_group order: MOV, then PUB, then the base)
    leg_c = [("box", _t3_use_col("commercial"), u"Commerce"), ("box", _t3_use_col("mixed"), u"Mixed use"),
             ("thick", sp1, u"Primary commercial spine"), ("dash", sp2, u"Secondary commercial spine")]
    if ctx is not None:
        leg_c.append(("dash", walk_c, u"Walk to the nearest (letter)"))
    leg_c += [("box", _t3_use_col("institutional"), u"Civic"), ("box", _t3_use_col("religious"), u"Worship"),
              ("dash", hc, u"Constellation · 3+ in 100 m")]
    if nums_top:
        leg_c.append(("mark", None, u"Numbered street: list below"))
    leg_c += list(_t3_base_leg())
    bx_ = r28mv_note_top(S, B, crop_r, k, L, MV, n_pl, leg_c, nums_top)   # v50 P07.2; v58 P07.1-P07.4
    T3_P07_BOXES.extend(tuple(v_ / k for v_ in b_) for b_ in bx_)
    lp_overlap_flag("p07", list(T3_P07_BOXES))           # v58 (G3): once for the page; the lead logs lp_flag_lines
    LOG.append(hue_log("p07"))                            # v61 (G6-6): every p07 legend from the hue table
    LOG.append(an_log("p07", 0, 0))                       # v61 (G6-4): no cuts or levels on p07; north by an_north    # v40: the booklet crop of the plan (v46: 1:10,000);
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
