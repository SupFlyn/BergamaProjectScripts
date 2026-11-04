# ---- 50_place (composer core, round 5 S1; G-R5-12 "prevent, not just detect", G-R5-2, G-R5-10, PLAN §3) -------------
# Everything that belongs to a drawing is placed by the booklet, after the drawing, in priority order: in-drawing
# labels, level column, legend, lists, notes. A label tries (1) its exported positions round its anchor, (2) nearby
# free spots on rings (text_place TP_RINGS), (3) its short forms the same way, (4) a number on the point + a row in the
# drawing's side list, (5) smaller sizes down to 4 pt; only then a WARNING and its first position. A label never
# crosses its drawing's window (G-R5-10 "no half labels"): spots that would are not taken.
#   pl_label(P, it, placed, side=None, window=None) -> TextPage item
#   pl_labels(P, placed, side=None, roles=("label", "badge")) -> n     every anchored text of the drawing, by priority
#   pl_side_rows(P, side, x, y, w, h=None) -> height                    closes the side list, sets its numbered rows
#   pl_legend(P, lg, x, y, w, h=None, max_cols=2) -> box                swatches + justified texts in columns
#   pl_list(P, ls, x, y, w, h=None) -> box                              numbered / bulleted rows
#   pl_levels(P, lc, placed, side=None) -> n                            level markers (Aras's sketch U04) beside the
#                                                                       drawing, values "+43.71"; v32: crowded values in a
#                                                                       2nd column or pushed down with a joining line
#   pl_levels_w(lc, k, e_top) -> mm                                     v32: the level column's measured width
#   pl_chain(P, fx, side=None, first=True) -> item                      v32: the one chain for every movable text
#   pl_scalebar(P, placed, x=None, y=None, max_mm=30.0) -> box           beside its drawing (default under its left end)
#   pl_inset(P, ins, parent, x, y, w, h) -> placed                      the zoom at >= 2 x the parent, framed; the
#                                                                       window drawn on the parent
#   pl_mm_drawing(P, D, texts, x, y, w, h, align="C") -> placed         a scale-free drawing (key map from the S2
#                                                                       module, diagram, chart) fitted into a box + its texts
#   pl_photo(P, ph, x, y, w, h) -> box                                  a photo kept rectangular, never stretched
# Every placed thing is a TextPage text, block or keep, so 70_check sees it.
PL_LEVEL = dict(gap=3.0, dash=(3.5, 0.8, 0.8, 0.8, 3.1), tri_w=2.2, tri_h=1.4, lw=0.5, label_gap=0.8, clear=0.8,
                ink="4A3F35")          # PLAN §3 level marker (refs/U04): mm, line width pt
PL_SW = dict(w=4.0, h=2.4, gap=1.4, row_gap=0.8)     # legend swatch (mm)


def _pl_codes(pos):
    out = []
    for c in pos or TP_POSITIONS:
        if isinstance(c, str) and c.startswith("="):
            out.append((0.0, 0.0, c[1:] or "L"))
        elif isinstance(c, (list, tuple)):
            out.append(tuple(c))
        else:
            out.append(c)
    return out


def _pl_apt(it):
    """a text item's anchor point in its drawing's units: anchor.pt (Ix) or anchor.point (key-map module, S2)"""
    a_ = it.get("anchor") or {}
    if not isinstance(a_, dict):
        return None
    p_ = a_.get("pt")
    return p_ if p_ is not None else a_.get("point")


def _pl_inside(b, win):
    return win is None or (win[0] <= b[0] + 1e-6 and b[2] <= win[2] + 1e-6 and win[1] <= b[1] + 1e-6 and
                           b[3] <= win[3] + 1e-6)


def _pl_try(P, t, anchor, codes, pt, bold, allow, win, d=0.8):
    tp = P.tp
    for code in codes:
        x, y, al = tp._at(code, t, anchor, pt, bold, d)
        b = tp._box(t, x, y, pt, bold, al, 0.0)
        if _pl_inside(b, win) and tp._free(b, allow):
            return x, y, al
    for x, y, al in tp._ring_spots(t, anchor, pt, bold, d, TP_RINGS):
        b = tp._box(t, x, y, pt, bold, al, 0.0)
        if _pl_inside(b, win) and tp._free(b, allow):
            return x, y, al
    return None


PL_FIX = ("moved", "short", "leader", "numbered", "forced")
PL_LEAD = dict(gap=1.5, col=14.0, cols=4, lw=0.3, ink="4A3F35", row_gap=0.8)    # leader lines (mm, pt)


def pl_stat(P):
    """v32: the page's label counts (log "layout <page> ... labels n (moved n, short n, leader n, numbered n)")"""
    if not hasattr(P, "fx_stat"):
        P.fx_stat = dict((k, 0) for k in ("labels",) + PL_FIX)
        P.fx_leaders = []
    return P.fx_stat


def _pl_seg_clear(P, p, q):
    """True when the leader p-q crosses no text already on the page"""
    return not any(tp_seg_box(p, q, it["box"]) for it in P.tp.items)


def _pl_leader(P, fx, t):
    """v32: a spot for text t OUTSIDE its drawing (fx["rect"]) with a leader line from its anchor: beside the drawing
    (the anchor's nearer side first, then the other, columns further out), level with the anchor or the nearest free
    row above / below. Same size, never smaller (Aras 4 Nov 19:25). -> (x, y, align, (p, q)) or None"""
    r = fx.get("rect")
    if not r:
        return None
    tp, L = P.tp, PL_LEAD
    ax, ay = fx["anchor"]
    pt, bold = fx["pt"], fx["bold"]
    a_, d_ = fm_asc_desc(pt, bold)
    step = (a_ - d_) + L["row_gap"]
    sides = ("R", "L") if ax >= (r[0] + r[2]) / 2.0 else ("L", "R")
    for j in range(L["cols"]):
        for sd in sides:
            x = (r[2] + L["gap"] + j * L["col"]) if sd == "R" else (r[0] - L["gap"] - j * L["col"])
            al = "L" if sd == "R" else "R"
            for k_ in range(0, 41):
                dy = ((k_ + 1) // 2) * step * (1.0 if k_ % 2 else -1.0)
                yc = ay + dy
                base = yc + (a_ + d_) / 2.0
                b = tp._box(t, x, base, pt, bold, al, 0.0)
                q = (x - 0.4, yc) if sd == "R" else (x + 0.4, yc)
                if tp._free(b, fx["allow"]) and _pl_seg_clear(P, (ax, ay), q):
                    return x, base, al, ((ax, ay), q)
    return None


def pl_draw_leaders(P):
    """draws the leader lines of the page's texts that kept a leader (after the fix pass, so moved ones are gone)"""
    n = 0
    for fx in P.fx_leaders:
        if fx.get("leader"):
            p, q = fx["leader"][0]
            bk_line(P, [p, q], PL_LEAD["ink"], PL_LEAD["lw"])
            n += 1
    return n


def pl_unleader(P, fx):
    """takes a text's leader (and its keep) off again before the text is placed anew"""
    ld = fx.pop("leader", None)
    if ld and ld[1] in P.tp.keeps:
        P.tp.keeps.remove(ld[1])


def pl_chain(P, fx, side=None, first=True):
    """v32 (L1, LAYOUT_PLAN §3.2-3; Aras 4 Nov 19:25 "making it smaller ... is a band-aid"): ONE chain for every
    movable text, at its own size: (1) its exported spot, (2) free spots on rings round its anchor inside its window
    (moved), (3) its short forms the same way (short), (4) OUTSIDE its drawing with a leader line, full text first
    (leader), (5) a number on the anchor + a row in the side list (numbered; side None or side_list_ok False skips
    it), (6) set at its first spot (forced: the final check names it). Never dropped, never shrunk.
    fx = dict(anchor, texts, codes, pt, lo, bold, colour, role, name, allow, win, rect, d, side_ok, owner); the text
    keeps fx in item["extra"]["fx"], so bk_fix (82_compose) can take it off and run the chain again (first=False)."""
    st = pl_stat(P)
    tp = P.tp
    anchor, texts, codes = fx["anchor"], fx["texts"], fx["codes"]
    pt0, bold, win, d = fx["pt"], fx["bold"], fx.get("win"), fx.get("d", 0.8)

    def put(t, x, y, al, kind, allow=None, **kw):
        tp.put(t, x, y, pt0, bold, al, 0.0, fx.get("name"), fx.get("role", "label"), fx.get("colour"),
               allow or fx["allow"], fx=fx, **kw)
        if kind:
            st[kind] += 1
        return tp.items[-1]
    if first:
        st["labels"] += 1
    for i, t in enumerate(texts):
        if first and i == 0 and codes:                    # its own exported spot first
            x, y, al = tp._at(codes[0], t, anchor, pt0, bold, d)
            b = tp._box(t, x, y, pt0, bold, al, 0.0)
            if _pl_inside(b, win) and tp._free(b, fx["allow"]):
                return put(t, x, y, al, None)
        got = _pl_try(P, t, anchor, codes, pt0, bold, fx["allow"], win, d)
        if got:
            return put(t, got[0], got[1], got[2], "moved" if i == 0 else "short")
    for t in texts:
        got = _pl_leader(P, fx, t)
        if got:
            nm = u"leader %s %d" % (fx.get("name"), id(fx))
            K = tp.keep([got[3][0], got[3][1]], "leader", nm, line=True)
            fx["leader"] = (got[3], K)
            if fx not in P.fx_leaders:
                P.fx_leaders.append(fx)
            return put(t, got[0], got[1], got[2], "leader", allow=tuple(fx["allow"]) + (nm, "leader"))
    if side is not None and fx.get("side_ok", True):
        tp.put(u"0", anchor[0], anchor[1], pt0, True, "MC", 0.0, fx.get("name"), "number", fx.get("colour"),
               tuple(fx["allow"]) + ("marker",))
        num = tp.items[-1]
        side.add(anchor, texts[0], num)
        if side not in tp.sides:
            tp.sides.append(side)
        st["numbered"] += 1
        return num
    x, y, al = tp._at(codes[0] if codes else "E", texts[0], anchor, pt0, bold, d)
    return put(texts[0], x, y, al, "forced", forced=True)


# ---- the label band of a section (v32, Aras 4 Nov 19:26 W1 box: labels above the section, vertical leaders) -------
def pl_band_rows(texts, xs, wmax, pt, bold=False):
    """texts at their x (mm from the drawing's left edge) set in rows ABOVE the drawing: each in the lowest row where
    it touches no neighbour and no lower-row label covers its leader; left-aligned at its x (right-aligned at its x
    when it would run past wmax). -> ([(i, x0, row, align)], n_rows)"""
    rows, out = [], []
    # v32.1 fix (kit v4.1 run: the booklet never finished): right to left, so a label's leader passes the labels set
    # before it; a label whose leader is covered by a lower label in every row used to loop for ever: on a NEW row it
    # is now set anyway (its leader crosses that label; the page check reports it)
    for i in sorted(range(len(texts)), key=lambda j: -xs[j]):
        w = fm_width(texts[i], pt, bold)
        x = xs[i]
        al = "L" if x + w <= wmax + 0.5 else "R"
        iv = (x, x + w) if al == "L" else (x - w, x)
        r = 0
        while True:
            fresh = r == len(rows)
            if fresh:
                rows.append([])
            ok = all(not (iv[0] < b_ + 1.2 and a_ < iv[1] + 1.2) for a_, b_ in rows[r])
            ok = ok and all(not (a_ - 0.4 <= x <= b_ + 0.4) for rr in rows[:r] for a_, b_ in rr)
            if ok or fresh:
                rows[r].append(iv)
                out.append((i, x, r, al))
                break
            r += 1
    return out, len(rows)


def pl_band_h(n_rows, pt):
    a_, d_ = fm_asc_desc(pt, False)
    return (n_rows * ((a_ - d_) + PL_LEAD["row_gap"]) + PL_LEAD["gap"]) if n_rows else 0.0


def pl_band_items(D):
    """the anchored labels of a section that go into its band"""
    return [it for it in ix_texts(D) if it.get("role", "label") == "label" and _pl_apt(it) is not None and
            (it.get("string") or u"")]


def pl_band_need(D, k):
    """the band height (mm) a section's labels need at k page mm per drawing unit"""
    its = pl_band_items(D)
    if not its:
        return 0.0
    pt = grid_role("label")[0]
    e0 = float(D["extent"][0])
    ew = (float(D["extent"][2]) - e0) * k
    _o, n = pl_band_rows([it["string"] for it in its], [(_pl_apt(it)[0] - e0) * k for it in its], ew, pt)
    return pl_band_h(n, pt)


def pl_band(P, placed):
    """sets a section's labels in the band above it (its top at placed rect top - band height), each with a vertical
    leader down to its point; band texts are fixed (no chain needed: the rows keep them apart). -> n"""
    D, T, r = placed["D"], placed["T"], placed["rect"]
    its = pl_band_items(D)
    if not its:
        return 0
    st = pl_stat(P)
    pt = grid_role("label")[0]
    a_, d_ = fm_asc_desc(pt, False)
    lh = (a_ - d_) + PL_LEAD["row_gap"]
    anchors = [T.pt(_pl_apt(it)[0], _pl_apt(it)[1]) for it in its]
    rows, _n = pl_band_rows([it["string"] for it in its], [a[0] - r[0] for a in anchors], r[2] - r[0], pt)
    for i, x, row, al in rows:
        it, (ax, ay) = its[i], anchors[i]
        base = r[1] - PL_LEAD["gap"] - row * lh + d_     # row 0 just above the drawing
        P.tp.put(it["string"], r[0] + x + (0.3 if al == "L" else -0.3), base, pt, bool(it.get("bold")), al, 0.0,
                 it.get("id"), "label", it.get("colour"), (placed["id"], "leader"))
        bk_line(P, [(ax, ay), (ax, base - a_ * 0.0 + 0.4)], PL_LEAD["ink"], PL_LEAD["lw"])
        st["labels"] += 1
        st["leader"] += 1
    return len(rows)


def pl_label(P, it, placed, side=None, window=None):
    """an in-drawing label (true-scale drawing): the chain, kept inside its drawing's window"""
    a_ = _pl_apt(it)
    if a_ is None:
        return None
    texts = [t for t in [it.get("string", u"")] + list(it.get("short_forms") or []) if t]
    if not texts:
        return None
    fx = dict(anchor=placed["T"].pt(a_[0], a_[1]), texts=texts, codes=_pl_codes(it.get("positions")),
              pt=float(it.get("size_pt") or grid_role(it.get("role", "label"))[0]),
              lo=max(float(it.get("min_pt") or GRID_MIN_PT), GRID_MIN_PT), bold=bool(it.get("bold")),
              colour=it.get("colour"), role=it.get("role", "label"), name=it.get("id"), allow=(placed["id"],),
              win=window or placed["rect"], rect=placed["rect"], d=0.8, side_ok=it.get("side_list_ok", True),
              owner=placed["id"])
    return pl_chain(P, fx, side)


def pl_rigid(P, placed, s, roles=None):
    """v30.3 / v32: a scale-free drawing (diagram, chart, key map, axo) or a board drawing: each text is tried FIRST at
    the spot its script set, scaled with the drawing (size x s, offsets x s); v32 (L1, Aras 4 Nov 19:17 "detect the
    collisions and fix it"): a spot that hits anything goes through the same chain as labels (pl_chain: rings, short
    forms, number, smaller), anywhere on the page, never on another drawing. Floor GRID_MIN_PT (D1)."""
    T = placed["T"]
    n = 0
    import re as _re
    stems = {}                                          # v32: lines of one multi-line label (<id>_lbl_<g>_<line>, L5)
    for it in ix_texts(placed["D"]):
        m_ = _re.match(r"^(.*_lbl_\d+)_\d+$", u"%s" % it.get("id", u""))
        if m_ and _pl_apt(it) is not None and it.get("string"):
            stems.setdefault(m_.group(1), []).append(it)
    done = set()
    for st_, its in stems.items():
        if len(its) > 1:
            n += _pl_rigid_group(P, placed, s, its)
            done.update(id(i_) for i_ in its)
    for it in sorted(ix_texts(placed["D"]), key=lambda t: t.get("priority", 5)):
        if roles and it.get("role") not in roles:
            continue
        if id(it) in done:
            continue
        a_ = _pl_apt(it)
        t = it.get("string", u"")
        if a_ is None or not t:
            continue
        pt0 = float(it.get("size_pt") or grid_role(it.get("role", "label"))[0])
        pt = max(GRID_MIN_PT, pt0 * s)
        c = (_pl_codes(it.get("positions")) or ["E"])[0]
        if not isinstance(c, str):
            c = (c[0] * s, c[1] * s, c[2])
        if it.get("role") == "badge":                  # a step / marker number stays ON its disc (never moved)
            x, y, al = P.tp._at(c, t, T.pt(a_[0], a_[1]), pt, bool(it.get("bold", True)), 0.0)
            P.tp.put(t, x, y, pt, bool(it.get("bold", True)), al, 0.0, it.get("id"), "badge", it.get("colour"),
                     (placed["id"], "marker"))
            n += 1
            continue
        texts = [x_ for x_ in [t] + list(it.get("short_forms") or []) if x_]
        fx = dict(anchor=T.pt(a_[0], a_[1]), texts=texts, codes=[c], pt=pt,
                  lo=max(float(it.get("min_pt") or GRID_MIN_PT), GRID_MIN_PT), bold=bool(it.get("bold")),
                  colour=it.get("colour"), role=it.get("role", "label"), name=it.get("id"), allow=(placed["id"],),
                  win=None, rect=placed["rect"], d=0.8 * s, side_ok=it.get("side_list_ok", True), owner=placed["id"])
        pl_chain(P, fx, getattr(P, "fx_side", None))
        n += 1
    return n


def _pl_rigid_group(P, placed, s, its):
    """v32: the lines of one multi-line label move TOGETHER: their exported spots, else one shared offset on rings
    round them (every line free), else outside the drawing in a column beside it; never split, never shrunk"""
    T, tp = placed["T"], P.tp
    allow = (placed["id"],)
    spots = []
    for it in its:
        a_ = _pl_apt(it)
        pt = max(GRID_MIN_PT, float(it.get("size_pt") or grid_role(it.get("role", "label"))[0]) * s)
        c = (_pl_codes(it.get("positions")) or ["E"])[0]
        if not isinstance(c, str):
            c = (c[0] * s, c[1] * s, c[2])
        x, y, al = tp._at(c, it["string"], T.pt(a_[0], a_[1]), pt, bool(it.get("bold")), 0.8 * s)
        spots.append((it, x, y, al, pt))

    def boxes(dx, dy):
        return [tp._box(it["string"], x + dx, y + dy, pt, bool(it.get("bold")), al, 0.0) for it, x, y, al, pt in spots]

    def ok(bs):
        g_ = []
        for b in bs:
            if not tp._free(b, allow):
                return False
            if any(tp_hit(b, c_, tp.pad) for c_ in g_):
                return False
            g_.append(b)
        return True
    import math as _m
    off = None
    st = pl_stat(P)
    if ok(boxes(0.0, 0.0)):
        off = (0.0, 0.0)
    else:
        for R_ in TP_RINGS + (8.0, 10.0, 12.0):
            for k in range(TP_RING_STEPS):
                a = 2.0 * _m.pi * k / TP_RING_STEPS
                d_ = (R_ * _m.cos(a), -R_ * _m.sin(a))
                if ok(boxes(*d_)):
                    off = d_
                    break
            if off:
                st["moved"] += 1
                break
    if off is None:
        r = placed["rect"]
        y0 = min(y for _i, _x, y, _a, _p in spots)
        x0 = min(b[0] for b in boxes(0.0, 0.0))
        for xx in (r[2] + PL_LEAD["gap"], r[0] - PL_LEAD["gap"] - max(b[2] - b[0] for b in boxes(0.0, 0.0))):
            for k in range(0, 41):
                dy = ((k + 1) // 2) * 2.5 * (1.0 if k % 2 else -1.0)
                d_ = (xx - x0, dy)
                if ok(boxes(*d_)):
                    off = d_
                    break
            if off:
                st["leader"] += 1
                ax, ay = spots[0][1], spots[0][2]
                q = (xx - 0.4 if xx > r[2] else xx + 0.4 + 0.0, y0 + d_[1])
                bk_line(P, [(ax, ay), q], PL_LEAD["ink"], PL_LEAD["lw"])
                break
    forced = off is None
    off = off or (0.0, 0.0)
    if forced:
        st["forced"] += 1
    g = tp._group()
    for it, x, y, al, pt in spots:
        tp.put(it["string"], x + off[0], y + off[1], pt, bool(it.get("bold")), al, 0.0, it.get("id"),
               it.get("role", "label"), it.get("colour"), allow, g, forced=forced)
    st["labels"] += 1
    return len(spots)


def pl_labels(P, placed, side=None, roles=("label", "badge")):
    n = 0
    for it in ix_texts(placed["D"]):
        if it.get("role") in roles and _pl_apt(it) is not None:
            if pl_label(P, it, placed, side):
                n += 1
    return n


def pl_side_rows(P, side, x, y, w, h=None):
    """closes the side list (numbers in reading order) and sets its rows "n  text" from (x, y) down"""
    rows = side.close(P.tp)
    yy = y
    for n, t in rows:
        P.tp.put(u"%d" % n, x, yy + fm_asc_desc(grid_role("list_item")[0], True)[0], grid_role("list_item")[0], True,
                 "L", 0.0, None, "list_item", None, ())
        hh, _s = st_para(P, t, x + 4.0, yy, w - 4.0, None if h is None else max(0.0, y + h - yy), "list_item")
        yy += hh + 0.8
    if h is not None and yy - y > h + 1e-6:
        wn_warn(P.pid, "overrun", u"side list %s needs %.1f mm, %.1f mm free" % (side.name, yy - y, h))
    return yy - y


def _pl_swatch(P, sw, x, y):
    """one legend swatch in the box (x, y) .. (x + w, y + h) (page mm, y down)"""
    W, H = PL_SW["w"], PL_SW["h"]
    k = (sw or {}).get("kind", "fill")
    col = sw.get("colour") or sw.get("fill") or GRID_INK["ink"]
    if k == "fill":
        bk_rect(P, (x, y, x + W, y + H), col, sw.get("stroke"), sw.get("width_pt") or 0.3)
    elif k in ("line", "dash"):
        bk_line(P, [(x, y + H / 2.0), (x + W, y + H / 2.0)], col, sw.get("width_pt") or 1.0,
                sw.get("dash_pt") or ((2.0, 1.2) if k == "dash" else None))
    elif k == "dot":
        import fitz as _fz
        sh = P.page.new_shape()
        sh.draw_circle(_fz.Point((x + W / 2.0) * BK_K, (y + H / 2.0) * BK_K), min(W, H) * 0.35 * BK_K)
        sh.finish(color=hex_rgb(sw.get("stroke")) if sw.get("stroke") else None, fill=hex_rgb(col),
                  width=sw.get("width_pt") or 0.3)
        sh.commit()
    elif k == "image" and sw.get("file"):
        import fitz as _fz
        try:
            P.page.insert_image(_fz.Rect(x * BK_K, y * BK_K, (x + W) * BK_K, (y + H) * BK_K),
                                filename=_rd_img_path(sw["file"]), keep_proportion=True)
        except Exception as ex:
            wn_warn(P.pid, "image", u"legend swatch %s: %s" % (sw.get("file"), type(ex).__name__))
    P.tp.keep((x, y, x + W, y + H), "swatch", None)


def pl_legend(P, lg, x, y, w, h=None, max_cols=2):
    """the legend in columns (filled top to bottom), one size for every entry (stepped down together)"""
    ents = [(e.get("swatch") or {}, ix_text(e.get("text"), lg.get("_folder"))) for e in lg.get("entries") or []]
    title = ix_text(lg.get("title"), lg.get("_folder")) if lg.get("title") else None
    cols = max(1, min(int(max_cols), int((w + 4.0) // 40.0) or 1))
    cw = (w - 4.0 * (cols - 1)) / float(cols)
    tw = cw - PL_SW["w"] - PL_SW["gap"]
    pt0 = grid_role("legend")[0]
    s = pt0
    while True:
        hs = [st_fit(t, tw, None, "legend", s, justify=True, page=P.pid)[3] for _sw, t in ents]
        hs = [max(hh, PL_SW["h"]) + PL_SW["row_gap"] for hh in hs]
        th = (st_fit(title, w, None, "heading", page=P.pid)[3] + 1.2) if title else 0.0
        per = -(-len(hs) // cols) if hs else 0
        colh = [sum(hs[i * per:(i + 1) * per]) for i in range(cols)]
        need = th + (max(colh) if colh else 0.0)
        if h is None or need <= h + 1e-6 or s - 0.25 < GRID_MIN_PT - 1e-6:
            break
        s -= 0.25
    if h is not None and need > h + 1e-6:
        wn_warn(P.pid, "overrun", u"legend %s needs %.1f mm at %.1f pt, %.1f mm free" % (lg.get("id"), need, s, h))
    yy = y
    if title:
        hh, _p = st_para(P, title, x, yy, w, None, "heading", page=P.pid)
        yy += hh + 1.2
    g = P.tp._group()
    for i, ((sw, t), hh) in enumerate(zip(ents, hs)):
        c = i // per if per else 0
        r0 = yy + sum(hs[c * per:i])
        cx = x + c * (cw + 4.0)
        _pl_swatch(P, sw, cx, r0)
        st_para(P, t, cx + PL_SW["w"] + PL_SW["gap"], r0, tw, None, "legend", s, group=g, page=P.pid)
    box = (x, y, x + w, y + need)
    P.tp.block(box, u"legend %s" % lg.get("id"))
    return box


def pl_list(P, ls, x, y, w, h=None):
    """numbered (or bulleted) rows; texts justified; one size for all rows"""
    rows = [ix_text(t, ls.get("_folder")) for t in ls.get("items") or []]
    numbered = ls.get("numbered", True)
    ind = 4.0
    s = grid_role("list_item")[0]
    while True:
        hs = [st_fit(t, w - ind, None, "list_item", s, page=P.pid)[3] + 0.8 for t in rows]
        if h is None or sum(hs) <= h + 1e-6 or s - 0.25 < GRID_MIN_PT - 1e-6:
            break
        s -= 0.25
    if h is not None and sum(hs) > h + 1e-6:
        wn_warn(P.pid, "overrun", u"list %s needs %.1f mm at %.1f pt, %.1f mm free" % (ls.get("id"), sum(hs), s, h))
    yy = y
    for i, (t, hh) in enumerate(zip(rows, hs)):
        mark = (u"%d" % (i + 1)) if numbered else u"•"
        mark = fm_safe(mark, True)[0]
        P.tp.put(mark, x, yy + fm_asc_desc(s, True)[0], s, True, "L", 0.0, None, "list_item", None, ())
        st_para(P, t, x + ind, yy, w - ind, None, "list_item", s, page=P.pid)
        yy += hh
    box = (x, y, x + w, yy)
    P.tp.block(box, u"list %s" % ls.get("id"))
    return box


def _pl_level_rows(lc, ry, pt):
    """v32 (L1, LAYOUT_PLAN §3.2-4): the level values in rows: [(y, lv, baseline, col)], col 0 or 1. A value that
    would crowd the one above it in column 0 takes column 1 (its dash line longer); crowded in both, it goes down in
    the freer column (a thin joining line to its level). Never dropped."""
    L = PL_LEVEL
    a_, d_ = fm_asc_desc(pt, False)
    need = (a_ - d_) + L["clear"]
    rows = sorted([(ry(lv["z"]), lv) for lv in lc.get("levels") or [] if lv.get("z") is not None], key=lambda r: r[0])
    last, out = [-1e9, -1e9], []
    for y, lv in rows:
        b = y + (a_ + d_) / 2.0
        if b - last[0] >= need:
            col = 0
        elif b - last[1] >= need:
            col = 1
        else:
            col = 0 if last[0] <= last[1] else 1
            b = last[col] + need
        last[col] = b
        out.append((y, lv, b, col))
    return out


def _pl_level_txt(lv):
    txt = u"%+.2f" % float(lv["z"])
    if lv.get("name"):
        txt += u" " + fm_safe(u"%s" % lv["name"])[0]
    return txt


def pl_levels_w(lc, k, e_top):
    """v32: the width (mm) the level column takes beside a drawing at k page mm per m (both columns measured)"""
    L = PL_LEVEL
    pt = grid_role("level_value")[0]
    rows = _pl_level_rows(lc, lambda z: (e_top - float(z)) * k, pt)
    if not rows:
        return 0.0
    w = [0.0, 0.0]
    for _y, lv, _b, col in rows:
        w[col] = max(w[col], fm_width(_pl_level_txt(lv), pt))
    base = L["gap"] + sum(L["dash"]) + L["tri_w"] / 2.0 + L["label_gap"]
    return base + w[0] + ((w[1] + L["label_gap"] + 1.5) if w[1] else 0.0)


def pl_levels(P, lc, placed, side=None):
    """level markers beside the drawing (never on it): PLAN §3 "Level marker" (refs/U04); v32 two columns + joining
    lines (_pl_level_rows), every value printed"""
    L = PL_LEVEL
    T = placed["T"]
    r = placed["rect"]
    side = (side or lc.get("side") or "R").upper()[:1]
    sg = 1.0 if side == "R" else -1.0
    length = sum(L["dash"])
    tw, th = L["tri_w"], L["tri_h"]
    pt = grid_role("level_value")[0]
    rows = _pl_level_rows(lc, T.ry, pt)
    for y, lv, _b, _c in rows:
        if not (r[1] - 1e-6 <= y <= r[3] + 1e-6):
            wn_warn(P.pid, "edge", u"level %s %+.2f of %s is outside its drawing" % (lv.get("name"), lv["z"],
                                                                                   placed["id"]))
    a_, d_ = fm_asc_desc(pt, False)
    w0 = max([fm_width(_pl_level_txt(lv), pt) for _y, lv, _b, c in rows if c == 0] or [0.0])
    off1 = w0 + L["label_gap"] + 1.5 + tw / 2.0          # column 1 starts past column 0's widest value
    edge = r[2] if side == "R" else r[0]
    n = 0
    for y, lv, base, col in rows:
        sh = off1 if col else 0.0
        x0 = edge + sg * L["gap"]                          # the dash runs outward from the drawing
        if sh:                                             # column 1: a longer line first (solid, thin)
            bk_line(P, [(x0, y), (x0 + sg * sh, y)], L["ink"], L["lw"] * 0.6)
            x0 += sg * sh
        xs, on = x0, True
        for dd in L["dash"]:
            if on:
                bk_line(P, [(xs, y), (xs + sg * dd, y)], L["ink"], L["lw"])
            xs += sg * dd
            on = not on
        xe = x0 + sg * length
        bk_poly(P, [(xe - tw / 2.0, y - th), (xe + tw / 2.0, y - th), (xe, y)], None, L["ink"], L["lw"])
        bx = (min(edge, xe - tw / 2.0), y - th, max(edge, xe + tw / 2.0), y + 0.2)
        P.tp.keep(bx, "marker", u"level %s" % lv.get("name"))
        P.ink.append(("marker", bx, lc.get("id")))
        lx = xe + sg * (tw / 2.0 + L["label_gap"])
        mid = base - (a_ + d_) / 2.0
        if abs(mid - y) > 0.3:                             # pushed off its line: a thin joining line to it
            bk_line(P, [(xe + sg * tw / 2.0, y), (lx - sg * 0.3, mid)], L["ink"], L["lw"] * 0.5)
        P.tp.put(_pl_level_txt(lv), lx, base, pt, False, "L" if side == "R" else "R", 0.0, lc.get("id"),
                 "level_value", L["ink"], ("marker",))
        n += 1
    return n


def pl_scalebar(P, placed, x=None, y=None, max_mm=30.0):
    """a scale bar for a true-scale drawing (never for key maps or diagrams): round length, 4 cells, "0", "L m",
    "1:den"; (x, y) = the bar's top-left (page mm, y down), default 2 mm under the drawing's left end"""
    T = placed["T"]
    if not T.den:
        return None
    k = T.k                                   # mm per m
    Lm = 1.0
    for c in (1, 2, 5, 10, 20, 50, 100, 200, 500, 1000):
        if c * k <= max_mm:
            Lm = float(c)
    Lw, hb = Lm * k, 1.2
    r = placed["rect"]
    x = r[0] if x is None else x
    y = r[3] + 2.0 if y is None else y
    ink = GRID_INK["ink"]
    for i in range(4):
        a, b = x + Lw * i / 4.0, x + Lw * (i + 1) / 4.0
        bk_rect(P, (a, y, b, y + hb), ink if i % 2 == 0 else "FFFFFF", ink, 0.3)
    pt = grid_role("caption")[0]
    a_, _d = fm_asc_desc(pt)
    P.tp.put(u"0", x, y + hb + 0.6 + a_, pt, False, "C", 0.0, None, "scale", ink, (), "sb_%s" % placed["id"])
    P.tp.put(u"%g m" % Lm, x + Lw, y + hb + 0.6 + a_, pt, False, "C", 0.0, None, "scale", ink, (),
             "sb_%s" % placed["id"])
    P.tp.put(u"1:{:,}".format(int(T.den)), x + Lw + 3.0, y + hb, pt, False, "L", 0.0, None, "scale", ink, (),
             "sb_%s" % placed["id"])
    box = (x, y, x + Lw + 3.0 + fm_width(u"1:{:,}".format(int(T.den)), pt), y + hb + 0.6 + a_ - _d)
    P.tp.keep((x, y, x + Lw, y + hb), "scalebar", placed["id"])
    P.ink.append(("scalebar", box, placed["id"]))
    return box


def pl_inset(P, ins, parent, x, y, w, h):
    """the zoom (child drawing) inside (x, y, w, h), centred, at its own scale (>= 2 x the parent's), framed; the
    parent shows the window it zooms into (thin dark frame)"""
    D = ix_get(ins.get("child"), ins.get("_folder"))
    if D is None:
        wn_warn(P.pid, "inset", u"inset %s: child drawing %r not exported" % (ins.get("id"), ins.get("child")))
        return None
    den = sc_inset_den(parent["den"] or 1000, D, w, h, P.pid)
    dw, dh = sc_size(D, den)
    T = BkT(D, den, x + (w - dw) / 2.0, y + (h - dh) / 2.0)
    placed = rd_drawing(P, D, T, frame=(GRID_INK["ink"], 0.5))
    wi = ins.get("window")
    if wi:
        a = parent["T"].pt(wi[0], wi[3])
        b = parent["T"].pt(wi[2], wi[1])
        bk_rect(P, (a[0], a[1], b[0], b[1]), None, GRID_INK["ink"], 0.5)
    return placed


def pl_mm_drawing(P, D, texts, x, y, w, h, align="C"):
    """a scale-free drawing fitted into the box (factor within its fit range), its texts placed round their anchors"""
    f = sc_factor(D, w, h, P.pid)
    dw, dh = sc_size(D, f)
    ox = x + ((w - dw) / 2.0 if align == "C" else (0.0 if align == "L" else w - dw))
    T = BkT(D, f, ox, y + (h - dh) / 2.0)
    placed = rd_drawing(P, D, T)
    pl_rigid(P, placed, f)                  # v30.3: texts stay where the script set them, scaled with the drawing
    return placed


def pl_photo(P, ph, x, y, w, h):
    """a photo at the largest size inside the box, its proportions kept (never stretched, G-R4-8 rectangular)"""
    import fitz as _fz
    f = _rd_img_path(ph.get("file"))
    if not f or not os.path.isfile(f):
        wn_warn(P.pid, "photo", u"photo %s missing: %s" % (ph.get("id"), f))
        return None
    try:
        pix = _fz.Pixmap(f)
        pw, phh = float(pix.width), float(pix.height)
        pix = None
    except Exception as ex:
        wn_warn(P.pid, "photo", u"photo %s unreadable (%s)" % (ph.get("id"), type(ex).__name__))
        return None
    s = min(w / pw, h / phh)
    bw, bh = pw * s, phh * s
    bx, by = x + (w - bw) / 2.0, y + (h - bh) / 2.0
    P.page.insert_image(_fz.Rect(bx * BK_K, by * BK_K, (bx + bw) * BK_K, (by + bh) * BK_K), filename=f)
    box = (bx, by, bx + bw, by + bh)
    P.tp.block(box, u"photo %s" % ph.get("id"))
    P.tp.keep(box, "photo", ph.get("id"))
    P.ink.append(("photo", box, ph.get("id")))
    return box
