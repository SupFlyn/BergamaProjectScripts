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
#                                                                       drawing, values "+43.71"; labels spread >= 0.8 mm
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


def pl_label(P, it, placed, side=None, window=None):
    a_ = _pl_apt(it)
    if a_ is None:
        return None
    T = placed["T"]
    anchor = T.pt(a_[0], a_[1])
    win = window or placed["rect"]
    allow = (placed["id"],)
    texts = [it.get("string", u"")] + list(it.get("short_forms") or [])
    texts = [t for t in texts if t]
    if not texts:
        return None
    pt0 = float(it.get("size_pt") or grid_role(it.get("role", "label"))[0])
    lo = max(float(it.get("min_pt") or GRID_MIN_PT), GRID_MIN_PT)
    bold, col, role = bool(it.get("bold")), it.get("colour"), it.get("role", "label")
    codes = _pl_codes(it.get("positions"))
    for t in texts:
        got = _pl_try(P, t, anchor, codes, pt0, bold, allow, win)
        if got:
            P.tp.put(t, got[0], got[1], pt0, bold, got[2], 0.0, it.get("id"), role, col, allow)
            return P.tp.items[-1]
    if side is not None and it.get("side_list_ok", True):
        P.tp.put(u"0", anchor[0], anchor[1], pt0, True, "MC", 0.0, it.get("id"), "number", col, allow + ("marker",))
        num = P.tp.items[-1]
        side.add(anchor, texts[0], num)
        if side not in P.tp.sides:
            P.tp.sides.append(side)
        return num
    p_ = pt0 - 0.5
    while p_ >= lo - 1e-6:
        for t in texts:
            got = _pl_try(P, t, anchor, codes, p_, bold, allow, win)
            if got:
                P.tp.put(t, got[0], got[1], p_, bold, got[2], 0.0, it.get("id"), role, col, allow)
                return P.tp.items[-1]
        p_ -= 0.5
    wn_warn(P.pid, "overlap", u"label %r of %s: no free spot inside its drawing down to %.1f pt and no side list: set at "
            u"its first position" % (texts[0], placed["id"], lo))
    x, y, al = P.tp._at(codes[0] if codes else "E", texts[-1], anchor, lo, bold, 0.8)
    P.tp.put(texts[-1], x, y, lo, bold, al, 0.0, it.get("id"), role, col, allow, forced=True)
    return P.tp.items[-1]


def pl_rigid(P, placed, s, roles=None):
    """v30.3 (2 Nov run: diagram texts on top of each other): a scale-free drawing (diagram, chart, key map, axo) keeps
    its texts exactly where its script set them, scaled WITH the drawing (size x s, offsets x s), never moved to a free
    spot or numbered into a side list: the script designed them together, so they only collide if the script's own
    design does. Floor GRID_MIN_PT (D1); below it the layout gives the drawing more room instead."""
    T = placed["T"]
    n = 0
    for it in sorted(ix_texts(placed["D"]), key=lambda t: t.get("priority", 5)):
        if roles and it.get("role") not in roles:
            continue
        a_ = _pl_apt(it)
        t = it.get("string", u"")
        if a_ is None or not t:
            continue
        anchor = T.pt(a_[0], a_[1])
        pt0 = float(it.get("size_pt") or grid_role(it.get("role", "label"))[0])
        pt = max(GRID_MIN_PT, pt0 * s)
        c = (_pl_codes(it.get("positions")) or ["E"])[0]
        if not isinstance(c, str):
            c = (c[0] * s, c[1] * s, c[2])
        x, y, al = P.tp._at(c, t, anchor, pt, bool(it.get("bold")), 0.8 * s)
        P.tp.put(t, x, y, pt, bool(it.get("bold")), al, 0.0, it.get("id"), it.get("role", "label"), it.get("colour"),
                 (placed["id"],), forced=True)
        n += 1
    return n


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


def pl_levels(P, lc, placed, side=None):
    """level markers beside the drawing (never on it): PLAN §3 "Level marker" (refs/U04)"""
    L = PL_LEVEL
    T = placed["T"]
    r = placed["rect"]
    side = (side or lc.get("side") or "R").upper()[:1]
    length = sum(L["dash"])
    tw, th = L["tri_w"], L["tri_h"]
    if side == "R":                             # marker from the drawing outward, its value after the triangle
        x0 = r[2] + L["gap"]
        xe = x0 + length
        lx, lal = xe + tw / 2.0 + L["label_gap"], "L"
    else:                                       # left side: the value left of the marker, right-aligned
        xe = r[0] - L["gap"] - tw / 2.0
        x0 = xe - length
        lx, lal = x0 - L["label_gap"], "R"
    pt = grid_role("level_value")[0]
    rows = []
    for lv in lc.get("levels") or []:
        y = T.ry(lv["z"])
        if not (r[1] - 1e-6 <= y <= r[3] + 1e-6):
            wn_warn(P.pid, "edge", u"level %s %+.2f of %s is outside its drawing" % (lv.get("name"), lv["z"],
                                                                                   placed["id"]))
        rows.append([y, lv])
    rows.sort(key=lambda a: a[0])
    a_, d_ = fm_asc_desc(pt, False)
    hgt = a_ - d_
    ly = []                                     # label baselines, spread so labels keep L["clear"] apart
    for y, lv in rows:
        b = y + (a_ + d_) / 2.0                 # the label's middle on the line
        if ly and b - ly[-1] < hgt + L["clear"]:
            b = ly[-1] + hgt + L["clear"]
        ly.append(b)
    n = 0
    for (y, lv), base in zip(rows, ly):
        xs, segs, on = x0, [], True
        for dd in L["dash"]:
            if on:
                segs.append((xs, xs + dd))
            xs += dd
            on = not on
        for a, b in segs:
            bk_line(P, [(a, y), (b, y)], L["ink"], L["lw"])
        bk_poly(P, [(xe - tw / 2.0, y - th), (xe + tw / 2.0, y - th), (xe, y)], None, L["ink"], L["lw"])
        P.tp.keep((x0, y - th, xe + tw / 2.0, y + 0.2), "marker", u"level %s" % lv.get("name"))
        P.ink.append(("marker", (x0, y - th, xe + tw / 2.0, y + 0.2), lc.get("id")))
        txt = u"%+.2f" % float(lv["z"])
        if lv.get("name"):
            txt += u" " + fm_safe(u"%s" % lv["name"])[0]
        P.tp.put(txt, lx, base, pt, False, lal, 0.0, lc.get("id"), "level_value",
                 L["ink"], ("marker",))
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
