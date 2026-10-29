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


def _t3_base(S, CB, V, k, L, order=2):
    """T3a (02 §1): the shared basemap in simple mode (stream, faint streets, faint buildings; basemap.py, memoised)
    through ClipB CB on the theme-B view V, then the study area's outline (G8). The same base on pp.07-09 (the city
    link draws the same items). Without basemap data (a first ever run) the board's own base, made pale, logged."""
    items = None
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


def _p07_fig(pose, x, y, k, facing=1, view="side", h_m=1.75, col="4A3F35"):
    """T3a: the ONE figure helper of this file: house shapes ("poly", ring, fill, stroke, lw), page mm, feet at (x, y),
    k mm per m. Side view = the legacy fig_polys (poses stand, walk, watch, sit, touch, wade, bike); top view = a
    minimal plan figure (shoulder ellipse + head circle, one ink weight, light flat fill).
    # swap point: figures.py fig_side/fig_top when the silhouette set arrives"""
    if view == "top":
        sh = [(x + 0.25 * k * math.cos(a_ * math.pi / 12.0), y + 0.13 * k * math.sin(a_ * math.pi / 12.0))
              for a_ in range(24)]
        hd = [(x + 0.11 * k * math.cos(a_ * math.pi / 8.0), y + 0.11 * k * math.sin(a_ * math.pi / 8.0))
              for a_ in range(16)]
        return [("poly", sh, "E2E0D4", col, 0.13), ("poly", hd, "E2E0D4", col, 0.13)]
    return [("poly", [(x + px * k, y + py * k) for px, py in R_], col, None, 0.0)
            for R_ in fig_polys(pose, h_m, facing)]


class _T3Put(object):
    """T3a: house shapes (page mm, y up, hex colours: icons.py, section_parts.py, plants.py, _p07_fig) onto the board:
    board = (ox + x * kb, oy + y * kb), kb = board units per booklet mm"""

    def __init__(self, B, ox, oy, kb, L):
        self.B, self.ox, self.oy, self.kb, self.L = B, ox, oy, kb, L

    def P(self, pts):
        return [(self.ox + p[0] * self.kb, self.oy + p[1] * self.kb) for p in pts]

    def put(self, shapes, order=40):
        for s_ in shapes or []:
            if s_[0] == "poly":
                ring, fill, stroke, lw = s_[1], s_[2], s_[3], s_[4]
                if len(ring) < 3:
                    continue
                Q = self.P(ring)
                if fill:
                    self.B.fill([Q], C(fill) if isinstance(fill, str) else fill, self.L, order)
                if stroke and lw:
                    self.B.line(Q + [Q[0]], C(stroke) if isinstance(stroke, str) else stroke, self.L, order + 1,
                                bk_lw(lw, self.kb))
            elif s_[0] == "line" and len(s_[1]) >= 2:
                col = s_[2]
                self.B.line(self.P(s_[1]), C(col) if isinstance(col, str) else col, self.L, order + 1,
                            bk_lw(s_[3], self.kb))

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


def draw_mv_key(S, B, V, R, MV, key, F, L, h, bounds):
    """v44: the key streets of the walking / driving map, named. v50 (MIRAQUA 28 Oct, P07.3, P07.4): every street
    piece is drawn graded (r28mv_class_streets), so this names the 5 busiest named streets (mv_key_rows) at h (7 pt),
    "name · index" on its longest run, placed without overlaps (place_labels). Returns (their rows, the key of the
    labels that found no place, {name: every point of its runs})."""
    rows = mv_key_rows(MV, key)
    names = set(r_["name"] for r_ in rows)
    pieces = R["pieces"]
    net = "car_b" if key.startswith("car") else "walk_b"

    def val(pi):
        nm = (pieces[pi]["tags"].get("name") or "").strip()
        return nm if nm in names else None
    best, pts = {}, {}
    for P, nm in _runs(R["chains"][net], pieces, R["xy"], val, set(R["inside"]), F):
        pts.setdefault(nm, []).extend(P)
        if nm not in best or pl_length(P) > pl_length(best[nm]):
            best[nm] = P
    labels = []
    for r_ in rows:
        P = best.get(r_["name"])
        if P:
            q, t = pl_point_at(P, pl_length(P) / 2.0)
            px, py = V.p(q[0], q[1])
            labels.append(([u"{} · {:.0f}".format(r_["name"], r_[key])], px, py, h, INK))
    return rows, place_labels(B, labels, [], L, bounds=bounds), pts


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


def draw_mv_today(S, B, x, y, U, R, MV, key, title, cap):
    """v46 (Prompt 3, p.8): walking or driving today as its own map at the theme's one scale: the whole site frame at
    1:10,000, the masterplan base, the scale bar and north arrow under it. v50 (MIRAQUA 28 Oct, P07.3): the index on
    EVERY street piece of its network (mv_runs walk_b / car_b; walking-only pieces stay base street on the driving
    map), graded in five classes by colour and line weight (r28mv_class_streets), the classes in the crop's legend;
    the 5 busiest named streets named at 7 pt (draw_mv_key, P07.4); P07.2: its note beside it (drw_mv_note_2 / _3).
    Returns the y below its crop."""
    L = "LU_BOARD::HowPeopleUseIt"
    F = S.F
    B.text(title, x, y, 0.5 * U, INK, L, font=FONT_TITLE, bold=True)
    V, k, ss, r = b_view(F, x, y - 0.8 * U, U)
    h = bk_hk(R28MV_LABEL_PT, k)
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 1)
    _t3_base(S, CB, V, k, L)                              # T3a: the shared basemap, simple mode (pp.07-09)
    lens = r28mv_class_streets(CB, V, mv_runs(S, R, key, F), k, L, 14)
    rows, key_, pts = draw_mv_key(S, CB, V, R, MV, key, F, L, h, r)
    b_frame(B, r, k, L)
    low = b_foot(B, F, x, r[1], ss, k, L)
    if key_:
        low = draw_label_key(B, key_, x, low - 0.8 * k, r[2] - x, h, L)
    crop = (x - 0.5 * k, low - 0.5 * k, r[2] + 0.5 * k, r[3] + 0.5 * k)
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
T3_SEC_ORDER = ("kept", "calmed", "pedestrian", "shared")   # the masterplan's road changes, one section pair each
T3_SEC_DENS = (200, 250, 500)   # the standard scales tried, largest first: two rows at most on one booklet width
T3_SEC_ROW_W = 392.0     # mm: one booklet row (BK_AW)
T3_SEC_GAP = 7.0         # mm between today and with the project
T3_SEC_PAIR_GAP = 14.0   # mm between two road types
T3_SEC_MATCH = 10.0      # m: an OSM street piece runs along a masterplan road when half its points lie this close
T3_SEC_REACH = 15.0      # m: a frontage (survey building) is looked for this far across, each side (as measure_widths)
T3_SEC_STUB = 4.0        # m of each fronting building drawn beyond its frontage
T3_SEC_OPEN = 3.0        # m of ground drawn beyond the street edge where no building fronts it
T3_SEC_TREE_MIN = 6.0    # m: a street at least this wide (frontage to frontage) takes a tree row in the proposal
T3_SEC_CAR = (1.80, 1.45)   # m: a car seen from the front (width, height), the drawing's symbol
T3_COL = dict(asphalt="6E675F", paving="CFC6B4", bld="E2E0D4", bld_edge="4A3F35", car="A7A299", car_edge="6E675F",
              ink="4A3F35", ink2="7A6E60", head="8B3A3F")


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
    side's frontage (survey building within T3_SEC_REACH) and that building's height (the board's building model).
    None when no piece along rd has a measured width."""
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
        side[sg] = dict(edge=e_, front=f_, h=(float(u.get("h") or 0.0) or None) if u else None)
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
    return dict(name=name, change=rd.get("change", "kept"), w=w, w_src=src, carriage=carriage, side=side)


def _t3_sec_extent(cut):
    """(left, right) m of the drawing: each side to its fronting building's back (frontage + T3_SEC_STUB), else the
    street edge + T3_SEC_OPEN; and (street left, street right): frontage or edge"""
    st, ex = [], []
    for sg in (-1, 1):
        sd = cut["side"][sg]
        edge = sd["front"] if sd["front"] is not None else (
            abs(cut["carriage"][0 if sg < 0 else 1]) if cut["carriage"] else cut["w"] / 2.0)
        st.append(sg * edge)
        ex.append(sg * (edge + (T3_SEC_STUB if sd["front"] is not None else T3_SEC_OPEN)))
    return tuple(ex), tuple(st)


def _t3_car(x, gy, k, facing=1):
    """a car seen from the front, the drawing's symbol (T3_SEC_CAR), its middle at x, wheels on gy"""
    w_, h_ = T3_SEC_CAR
    b0, b1, c1 = gy + 0.30 * k, gy + 0.95 * k, gy + h_ * k
    body = [(x - 0.5 * w_ * k, b0), (x + 0.5 * w_ * k, b0), (x + 0.5 * w_ * k, b1), (x + 0.36 * w_ * k, c1),
            (x - 0.36 * w_ * k, c1), (x - 0.5 * w_ * k, b1)]
    out = [("poly", body, T3_COL["car"], T3_COL["car_edge"], 0.13)]
    for sx in (-0.36, 0.36):
        out.append(("poly", [(x + (sx - 0.08) * w_ * k, gy), (x + (sx + 0.08) * w_ * k, gy),
                             (x + (sx + 0.08) * w_ * k, b0), (x + (sx - 0.08) * w_ * k, b0)], T3_COL["ink"], None, 0.0))
    return out


def _t3_sec_draw(PU, cut, after, x0, gy, k):
    """one section of cut (today, or with the project when after) with its left edge at x0, ground at gy (mm),
    k mm per m. Returns the mm width drawn."""
    (xl, xr), (sl, sr) = _t3_sec_extent(cut)
    X = lambda m: x0 + (m - xl) * k
    ch = cut["change"]
    sh = []
    sh += sct_ground([(X(xl), gy), (X(xr), gy)], gy - 1.0 * k, k)          # the cut ground, 1 m deep
    one_level = after and ch in ("calmed", "pedestrian", "shared")
    # surfaces: the carriageway (asphalt) and the footways (paving) today; one paved level with the project
    if one_level or not cut["carriage"]:
        sh.append(("poly", [(X(sl), gy), (X(sr), gy), (X(sr), gy + 0.15 * k), (X(sl), gy + 0.15 * k)],
                   T3_COL["paving"] if (one_level or not cut["carriage"]) else T3_COL["asphalt"], None, 0.0))
    else:
        c0, c1 = cut["carriage"]
        sh.append(("poly", [(X(c0), gy), (X(c1), gy), (X(c1), gy + 0.15 * k), (X(c0), gy + 0.15 * k)],
                   T3_COL["asphalt"], None, 0.0))
        for a_, b_ in ((sl, c0), (c1, sr)):
            if b_ - a_ > 0.05:
                sh.append(("poly", [(X(a_), gy), (X(b_), gy), (X(b_), gy + 0.15 * k), (X(a_), gy + 0.15 * k)],
                           T3_COL["paving"], None, 0.0))
    gs = gy + 0.15 * k
    # the fronting buildings, cut, at their height in the board's building model
    for sg, edge, ext in ((-1, sl, xl), (1, sr, xr)):
        sd = cut["side"][sg]
        if sd["front"] is not None and sd["h"]:
            a_, b_ = sorted((edge, ext))
            sh.append(("poly", [(X(a_), gy), (X(b_), gy), (X(b_), gy + sd["h"] * k), (X(a_), gy + sd["h"] * k)],
                       T3_COL["bld"], T3_COL["bld_edge"], 0.25))
    # trees (plants.py, D6: plane) where the proposal leaves room: pedestrian and shared streets T3_SEC_TREE_MIN wide
    width = sr - sl
    if after and ch in ("pedestrian", "shared") and width >= T3_SEC_TREE_MIN:
        tx = 0.5 * (sl + sr) if ch == "pedestrian" else sl + 0.25 * width
        cr = (PLA_SPECIES.get("plane") or {}).get("crown_m") or width     # the species' crown (plants.py), kept
        sh += pla_section("plane", X(tx), gs, k, crown_m=min(cr, width - 1.0))   # inside the street (no overlap, G5)
    # people and cars by what the street is for
    figs, cars = [], []
    if not after or ch == "kept":
        if cut["carriage"]:
            c0, c1 = cut["carriage"]
            n = max(1, min(2, int((c1 - c0) // 3.0)))
            cars = [c0 + (c1 - c0) * (j + 0.5) / n for j in range(n)]
            for a_, b_, f_ in ((sl, c0, 1), (c1, sr, -1)):
                if b_ - a_ >= 1.2:
                    figs.append(("walk", 0.5 * (a_ + b_), f_))
        else:
            figs.append(("walk", 0.5 * (sl + sr) - 0.6, 1))
    elif ch == "calmed":
        c0, c1 = cut["carriage"] or (sl + 0.25 * width, sr - 0.25 * width)
        cars = [c0 + 0.3 * (c1 - c0)]
        figs += [("walk", c0 + 0.75 * (c1 - c0), -1)]
        for a_, b_, f_ in ((sl, c0, 1), (c1, sr, -1)):
            if b_ - a_ >= 1.2:
                figs.append(("stand", 0.5 * (a_ + b_), f_))
    elif ch == "pedestrian":
        n = max(2, min(5, int(width // 2.5)))
        poses = ("walk", "stand", "walk", "sit", "walk")
        for j in range(n):
            figs.append((poses[j % len(poses)], sl + width * (j + 0.5) / n, 1 if j % 2 == 0 else -1))
    else:                                                 # shared
        cars = [sl + 0.62 * width]
        figs += [("walk", sl + 0.12 * width + 0.3, 1), ("bike", sl + 0.40 * width, 1), ("walk", sr - 0.12 * width, -1)]
    for cx in cars:
        sh += _t3_car(X(cx), gs, k)
    for pose, fx, f_ in figs:
        sh += _p07_fig(pose, X(fx), gs, k, facing=f_)
    PU.put(sh, 40)
    return (xr - xl) * k


def _t3_sec_dims(PU, cut, x0, gy, k):
    """the measured widths under a section, in cm: frontage to frontage (or the measured street width) and the
    carriageway between the surveyed road edges. Returns the lowest y used."""
    (xl, xr), (sl, sr) = _t3_sec_extent(cut)
    X = lambda m: x0 + (m - xl) * k
    rows = []
    if cut["carriage"]:
        rows.append((cut["carriage"][0], cut["carriage"][1], u"carriageway"))
    rows.append((sl, sr, u"street"))
    y = gy - 1.0 * k - 3.0
    for a_, b_, lab in rows:
        PU.line([(X(a_), y), (X(b_), y)], T3_COL["ink2"], 0.15)
        for xx in (X(a_), X(b_)):
            PU.line([(xx - 0.6, y - 0.6), (xx + 0.6, y + 0.6)], T3_COL["ink2"], 0.2)
        PU.text(u"{} {:,.0f} cm".format(lab, round((b_ - a_) * 100.0)), 0.5 * (X(a_) + X(b_)), y + 0.8, 7.0,
                T3_COL["ink"], False, "C")
        y -= 4.2
    return y + 1.5


def _t3_street_sections(S, B, x, y, w, U, M):
    """T3a (D3 b, Aras 29 Oct 18:53; replaces the walk / car index chart and the city link's walking potential):
    before / after cross-sections of one street per road change of the masterplan (kept, calmed, pedestrian,
    shared), each cut where the survey measured the street (_t3_sec_cut): carriageway and frontages as surveyed,
    buildings at the board's heights, the cut ground (section_parts.py), plane trees from plants.py where the
    proposal leaves T3_SEC_TREE_MIN, people by what the street is for (_p07_fig), cars as the drawing's symbol. A
    kept road is drawn once (no change). One standard scale for all (T3_SEC_DENS: the largest that fits two rows on
    the booklet width), a scale bar under every section (G5), widths in cm. Crop drw_street_sections. Returns the y
    below."""
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
    hmax = max([4.0] + [c_["side"][s_]["h"] or 0.0 for c_ in groups for s_ in (-1, 1)])

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
    den, rows = None, None
    for d_ in T3_SEC_DENS:
        rows = pack(d_)
        den = d_
        if len(rows) <= 2:
            break
    k = 1000.0 / den                                      # mm per m on the booklet page
    PU = _T3Put(B, x, 0.0, kb, L)
    ytop = y / kb                                         # mm
    PU.text(u"The same surveyed width, given back to people: each street today and with the project", 0.0,
            ytop - 4.0, 11.0, T3_COL["ink"], True)
    yrow = ytop - 10.0
    xmax = 0.0
    tree_h = (PLA_SPECIES.get("plane") or {}).get("h_m") or 0.0
    for row in rows:
        trees = any(c_["change"] in ("pedestrian", "shared") and _t3_sec_extent(c_)[1][1] - _t3_sec_extent(c_)[1][0]
                    >= T3_SEC_TREE_MIN for c_ in row)
        top_m = max(hmax, tree_h if trees else 0.0) + 1.0
        gy = yrow - 9.0 - top_m * k                       # the ground line of this row (mm)
        cx = 0.0
        low = gy
        for c_ in row:
            n = 1 if c_["change"] == "kept" else 2
            PU.text(u"{} · {}".format(c_["name"], c_["change"]), cx, yrow - 3.0, 8.5, T3_COL["head"], True)
            for j in range(n):
                after = j == 1
                wd = _t3_sec_draw(PU, c_, after, cx, gy, k)
                sub = u"today = with the project" if n == 1 else (u"with the project" if after else u"today")
                PU.text(sub, cx, yrow - 7.0, 7.0, T3_COL["ink2"], False)
                yd = _t3_sec_dims(PU, c_, cx, gy, k)
                sb = draw_scalebar_bk(B, x + cx * kb, yd * kb - 1.0 * kb, k * kb, 5.0 if den <= 250 else 10.0, kb, L)
                low = min(low, sb / kb)
                cx += wd + (T3_SEC_GAP if j < n - 1 else 0.0)
            cx += T3_SEC_PAIR_GAP
        xmax = max(xmax, cx - T3_SEC_PAIR_GAP)
        yrow = low - 4.0
    bot = yrow + 2.0
    LOG.append(u"Street sections at 1:{:,}: ".format(den) + u"; ".join(
        u"{} ({}) {:.1f} m {}{}".format(c_["name"], c_["change"], c_["w"], c_["w_src"],
                                       u", carriageway {:.1f} m".format(c_["carriage"][1] - c_["carriage"][0])
                                       if c_["carriage"] else u"") for c_ in groups))
    crop_panel("street_sections", x - 0.5 * kb, bot * kb - 0.5 * kb, x + (xmax + 0.5) * kb, y + 0.5 * kb,
               u"The same surveyed width, given back to people · streets today and with the project",
               den, crop_legend([("box", C(T3_COL["asphalt"]), u"Carriageway"),
                                 ("box", C(T3_COL["paving"]), u"Paving, one level"),
                                 ("box", C(T3_COL["bld"]), u"Building, cut")]))
    CROP_PANELS[-1]["bk_w"] = xmax + 1.0
    return bot * kb - 0.5 * kb


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
    B.text(t_top, x, y, 1.05 * U, INK, L, font=FONT_TITLE, bold=True)
    V, k, ss, r = b_view(F, x, y - 1.2 * U, U)            # v46: the site frame at 1:10,000, as every theme-B map
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
    crop_r = (x - 0.5 * k, foot - 0.5 * k, r[2] + 0.5 * k, r[3] + 0.5 * k)    # the booklet crop of the plan
    r28mv_note_top(S, B, crop_r, k, L, MV, n_pl)          # v50 (MIRAQUA 28 Oct, P07.2): drw_mv_note_1 beside the plan
    yy = foot - 3.0 * U
    # walking and driving today, only the key streets in colour and named (v44, Aras 27 Oct: "highlight only the key
    # axes and roads"); v46: each its own map at the theme's one scale, stacked under the plan
    if R:
        # v50 (MIRAQUA 28 Oct, P07.3): the index on every street piece, the busiest named (draw_mv_today, 15i)
        # T3a (package B p.07): sharper, title-like names that state what each map shows (G1)
        for key_, lead, mode in (("walk_b", u"Where feet go", u"walking"), ("car_b", u"Where cars go", u"driving")):
            two = _t3_names(mv_key_rows(MV, key_))
            title = (u"{}: {} carry the most {} routes".format(lead, two, mode) if two else lead)
            cap = title + u" · every street by the share of everyday {} routes that use it".format(mode)
            yy = draw_mv_today(S, B, x, yy, U, R, MV, key_, title, cap) - 2.0 * U
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
            if n_pl.get(f):
                leg.append(("dot", fcol[f], "{} · {} places".format(lab, n_pl[f])))
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
