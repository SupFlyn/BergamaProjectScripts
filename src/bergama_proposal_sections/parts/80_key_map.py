# ================================================================ v10 key map strip: the four cuts of this page (WO-T3b-3)
# v10 (package C "Page 13": "today it sits inside section 1's box, so it reads as belonging to that drawing only"):
# the key map is a strip across the top of the page block, outside every section's panel, inside ps_all. It shows ONLY
# page 13's four cut lines W1-W4 (basemap_cut_items with basemap_cut_ids, D11 / brief: each key map its own cuts) on
# the shared basemap in mode "topographic", each labelled with the badge and name of its section title. A key map, so
# no scale bar (SCRIPT_STANDARD §8); the frame axis turned horizontal, upstream on the left, a north arrow. The two
# bridges (site board data/DIAG_SRC.py BRIDGES_K) name the places; PS_KEY_SELINOS (agriculture data/GEO.py
# "selinos", survey m) orients the bridge bars and is the stream when no basemap.json exists yet.
PS_KEY_BRIDGES = [("k4", u"K4 köprüsü", (29846.40, 32277.71)),
                  ("k5", u"Üç Kemer Köprüsü", (30293.63, 31792.25))]
PS_KEY_H = 46.0                       # print mm: the strip's height on the booklet page (revision 30 Oct: 46)
PS_KEY_MARGIN = (60.0, 46.0)          # m around the four cuts in the turned frame (along, across)
PS_KEY_SELINOS = [
    (29642.6, 32739.4), (29633.1, 32660.6), (29643.3, 32638.1), (29645.7, 32633.8), (29652.9, 32627.1),
    (29660.7, 32621.7), (29671.3, 32612.4), (29681.0, 32595.6), (29690.4, 32573.6), (29710.7, 32540.0),
    (29713.6, 32536.0), (29733.9, 32514.1), (29754.5, 32493.6), (29765.8, 32484.3), (29769.1, 32480.8),
    (29776.7, 32468.2), (29784.7, 32450.4), (29788.6, 32436.6), (29789.1, 32431.9), (29777.7, 32369.0),
    (29781.7, 32325.3), (29795.2, 32299.4), (29798.1, 32295.6), (29818.1, 32281.3), (29822.6, 32279.6),
    (29865.9, 32271.5), (29920.8, 32274.0), (29974.1, 32261.0), (29985.8, 32252.3), (29991.8, 32239.0),
    (30000.2, 32215.9), (30005.5, 32176.9), (30015.3, 32144.5), (30022.8, 32126.7), (30025.2, 32122.5),
    (30052.7, 32087.9), (30102.5, 32002.2), (30148.1, 31931.0), (30166.5, 31908.3), (30177.3, 31892.6),
    (30200.4, 31867.1), (30235.2, 31839.1), (30275.6, 31802.4), (30315.8, 31746.3), (30345.9, 31706.8),
    (30378.4, 31640.0), (30405.5, 31555.5), (30444.1, 31464.0), (30493.0, 31382.7), (30496.2, 31379.0),
    (30593.4, 31294.4), (30649.6, 31262.4), (30682.7, 31240.2), (30717.2, 31212.8), (30733.6, 31194.9),
    (30753.5, 31180.3), (30757.8, 31177.9), (30833.2, 31152.0), (30931.7, 31093.4), (30935.6, 31090.4),
    (30987.4, 31044.7), (31015.8, 31010.8), (31103.4, 30896.4), (31137.6, 30847.4), (31140.0, 30843.1),
    (31154.8, 30764.8), (31158.1, 30761.4), (31193.6, 30733.8), (31242.2, 30700.3), (31308.9, 30668.1),
    (31393.4, 30634.5)]
PS_KEY_TURN = 49.905                  # degrees: turns the frame axis horizontal, downstream to the right (PLAN §1, G7)


def ps_rich_lines(s, size, width):
    """v9 (MIRAQUA 28 Oct, G5): a text with **bold** runs wrapped to width (mm): lines of [(word, bold, glued)];
    glued = no space before it (punctuation right after a bold run)."""
    toks = []
    for i, part in enumerate(s.split(u"**")):
        for j, wd in enumerate(part.split()):
            toks.append((wd, i % 2 == 1, j == 0 and bool(toks) and not part[:1].isspace()))
    lines, cur, cw = [], [], 0.0
    sp = text_w(u" ", size)
    for wd, b, glued in toks:
        w = text_w(wd, size, b) + (0.0 if glued or not cur else sp)
        if cur and not glued and cw + w > width:
            lines.append(cur)
            cur, cw, w = [], 0.0, text_w(wd, size, b)
        cur.append((wd, b, glued and bool(cur)))
        cw += w
    if cur:
        lines.append(cur)
    return lines


def ps_rich_para(pg, x, y, w, s, size, colour, lh=1.28, halo=None):
    """v9 (G5): para() for a text with **bold** runs, each run one whole string; every line one baseline (size x lh)
    lower than y. Returns (the last baseline, the right end of the longest line), mm."""
    right, sp = x, text_w(u" ", size)
    for ln in ps_rich_lines(s, size, w):
        y -= size * lh
        runs = []
        for i, (wd, b, g) in enumerate(ln):
            if runs and runs[-1][1] == b:
                runs[-1][0] += (u"" if g else u" ") + wd
            else:
                runs.append([wd, b, bool(i) and not g])          # [text, bold, a space before it]
        xx = x
        for t, b, spc in runs:
            xx += sp if spc else 0.0
            pg.text(t, xx, y, size, colour, bold=b, halo=halo)
            xx += text_w(t, size, b)
        right = max(right, xx)
    return y, right


def ps_key_turn(p):
    """survey m -> key map m: turned by PS_KEY_TURN (the frame axis horizontal, downstream to the right)"""
    a = math.radians(PS_KEY_TURN)
    return (p[0] * math.cos(a) - p[1] * math.sin(a), p[0] * math.sin(a) + p[1] * math.cos(a))


def ps_key_chain(p):
    """(chainage along PS_KEY_SELINOS from its upstream end, m; the line's unit direction there) at the point of the
    line nearest p"""
    best, acc = None, 0.0
    for a, b in zip(PS_KEY_SELINOS[:-1], PS_KEY_SELINOS[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1e-9
        t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (L * L)))
        d = math.hypot(a[0] + dx * t - p[0], a[1] + dy * t - p[1])
        if best is None or d < best[0]:
            best = (d, acc + t * L, (dx / L, dy / L))
        acc += L
    return best[1], best[2]


def ps_key_unturn(q):
    """key map m -> survey m (the inverse of ps_key_turn)"""
    a = math.radians(PS_KEY_TURN)
    return (q[0] * math.cos(a) + q[1] * math.sin(a), -q[0] * math.sin(a) + q[1] * math.cos(a))


def ps_clip_ring(ring, R):
    """a ring cut to the rectangle R (x0, y0, x1, y1) (Sutherland-Hodgman); [] when nothing is left"""
    x0, y0, x1, y1 = R
    out = list(ring)
    for e in range(4):
        if not out:
            break
        inp, out = out, []
        for i in range(len(inp)):
            p, q = inp[i - 1], inp[i]
            ip = (p[0] >= x0, p[0] <= x1, p[1] >= y0, p[1] <= y1)[e]
            iq = (q[0] >= x0, q[0] <= x1, q[1] >= y0, q[1] <= y1)[e]
            if ip != iq:
                if e < 2:
                    xe = x0 if e == 0 else x1
                    out.append((xe, p[1] + (q[1] - p[1]) * (xe - p[0]) / (q[0] - p[0])))
                else:
                    ye = y0 if e == 2 else y1
                    out.append((p[0] + (q[0] - p[0]) * (ye - p[1]) / (q[1] - p[1]), ye))
            if iq:
                out.append(q)
    return out if len(out) >= 3 else []


def ps_clip_line(pts, R):
    """a polyline cut to the rectangle R: the pieces inside (Liang-Barsky per segment)"""
    x0, y0, x1, y1 = R
    runs, cur = [], []
    for p, q in zip(pts[:-1], pts[1:]):
        dx, dy = q[0] - p[0], q[1] - p[1]
        t0, t1, ok = 0.0, 1.0, True
        for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
            if pp == 0:
                if qq < 0:
                    ok = False
                    break
                continue
            t = qq / pp
            if pp < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                ok = False
                break
        if not ok:
            if cur:
                runs.append(cur)
            cur = []
            continue
        a, b = (p[0] + dx * t0, p[1] + dy * t0), (p[0] + dx * t1, p[1] + dy * t1)
        if not cur or t0 > 0.0:
            if cur:
                runs.append(cur)
            cur = [a]
        cur.append(b)
        if t1 < 1.0:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    return [r for r in runs if len(r) >= 2]


def ps_key_strip(pg, area, log):
    """v10: the key map strip in area (x0, y0, x1, y1), print mm: frame, title row with the north arrow, the
    topographic basemap cut to the map window, the bridges, page 13's four cuts W1-W4 (triangles point the way each
    section looks: downstream), each with its section's badge and name. Returns the area."""
    x0, y0, x1, y1 = area
    pad, ls, ts = 2.5, PS_LBL, PS_NOTE
    pg.poly([rect(x0, y0, x1, y1)], fill=COL["white"], stroke=COL["faint"], lw=0.25)
    pg.poly([rect(x0, y1 - 0.8, x1, y1)], fill=MP["discharge"][1])
    yt = y1 - 0.8 - 1.8 - ts * CAP
    ps_rich_para(pg, x0 + pad, yt + ts * 1.28, x1 - x0 - 20.0,
                 u"**KEY MAP** · the four cuts drawn on this page, upstream to downstream; the triangles point the "
                 u"way each section looks", ts, COL["ink_dark"])
    # north arrow at the title row's right end
    nx, ny = ps_key_turn((0.0, 1.0))
    L = 4.0
    cx, cy = x1 - pad - 3.0, yt + ts * CAP / 2.0
    tail, tip = (cx - nx * L / 2.0, cy - ny * L / 2.0), (cx + nx * L / 2.0, cy + ny * L / 2.0)
    hd = 0.3 * L
    pg.line([tail, tip], COL["ink"], 0.3)
    pg.poly([[tip, (tip[0] - nx * hd - ny * hd * 0.45, tip[1] - ny * hd + nx * hd * 0.45),
              (tip[0] - nx * hd + ny * hd * 0.45, tip[1] - ny * hd - nx * hd * 0.45)]], fill=COL["ink"])
    pg.text(u"N", tip[0] - 1.2, tip[1] - ls * CAP / 2.0, ls, COL["ink"], bold=True, align="R")
    # the map window: the four cuts in the turned frame plus PS_KEY_MARGIN, widened to fill the strip
    R = (x0 + pad, y0 + pad, x1 - pad, yt - 0.25 * ts - 1.5)
    ids = [cid for _, cid, _, _, _ in PS_CUTS]
    cuts = basemap_cut_ids(ids, looks=dict((cid, -1) for cid in ids))   # the viewer looks downstream: SW on the right
    tq = [ps_key_turn(p) for c in cuts for p in c[:2]]
    wx0, wx1 = min(q[0] for q in tq) - PS_KEY_MARGIN[0], max(q[0] for q in tq) + PS_KEY_MARGIN[0]
    wy0, wy1 = min(q[1] for q in tq) - PS_KEY_MARGIN[1], max(q[1] for q in tq) + PS_KEY_MARGIN[1]
    km = min((R[2] - R[0]) / (wx1 - wx0), (R[3] - R[1]) / (wy1 - wy0))      # print mm per m
    mx, my = (wx0 + wx1) / 2.0, (wy0 + wy1) / 2.0
    wx0, wx1 = mx - (R[2] - R[0]) / km / 2.0, mx + (R[2] - R[0]) / km / 2.0
    wy0, wy1 = my - (R[3] - R[1]) / km / 2.0, my + (R[3] - R[1]) / km / 2.0
    frame = [ps_key_unturn(q) for q in ((wx0, wy0), (wx1, wy0), (wx1, wy1), (wx0, wy1))]

    def T(p):                                                  # survey m -> print mm
        q = ps_key_turn(p)
        return (R[0] + (q[0] - wx0) * km, R[1] + (q[1] - wy0) * km)

    def fill_fn(rings, hx, alpha, nonzero):
        rr = [r_ for r_ in (ps_clip_ring(r, R) for r in rings) if r_]
        if rr:
            pg.poly(rr, fill=hx, alpha=(alpha if alpha is not None and alpha < 0.975 else None))

    def line_fn(pts, hx, w, dash, alpha):
        for piece in ps_clip_line(pts, R):
            pg.line(piece, hx, w, dash=list(dash) if dash else None)
    taken = []

    def text_fn(s, xy, size, hx, bold, align):
        w = text_w(s, size, bold)
        pg.text(s, xy[0], xy[1] - size * CAP / 2.0, size, hx, bold=bold, align="C")
        taken.append((xy[0] - w / 2.0, xy[1] - size * 0.6, xy[0] + w / 2.0, xy[1] + size * 0.6))
    bx = (min(p[0] for p in frame), min(p[1] for p in frame), max(p[0] for p in frame), max(p[1] for p in frame))
    try:                                                       # revision 30 Oct (M4): the key map base with the study
        items = keymap_items((), scale_den=1000.0 / km, box=bx, log=log)["items"]   # area; the cuts drawn below
    except Exception as ex:
        log.append(u"NOTE key map: base not drawn (%s)" % type(ex).__name__)
        items = []
    if items:
        basemap_draw(items, T, fill_fn, line_fn)
    else:                                                      # no basemap.json yet: the stream line only
        log.append(u"NOTE key map: no basemap (run the site board once); the stream line alone is drawn")
        line_fn([T(p) for p in PS_KEY_SELINOS], COL["river"], 0.8, None, 1.0)
    # the bridges: short bars across the stream, named
    lab = []
    for _, nm, p in PS_KEY_BRIDGES:
        _, (dx, dy) = ps_key_chain(p)
        tx, ty = ps_key_turn((dx, dy))
        c = T(p)
        a_, b_ = (c[0] - ty * 1.6, c[1] + tx * 1.6), (c[0] + ty * 1.6, c[1] - tx * 1.6)
        pg.line([a_, b_], COL["ink"], 0.6, cap=0)
        taken.append((min(a_[0], b_[0]) - 0.3, min(a_[1], b_[1]) - 0.3, max(a_[0], b_[0]) + 0.3, max(a_[1], b_[1]) + 0.3))
        lab.append((c, nm, False, None))
    # page 13's cuts only, then each cut's badge and name as in its section title
    ci = basemap_cut_items(cuts, 1000.0 / km, frame=frame, inset_mm=0.6, tri_mm=1.6, text_mm=ls, col=COL["accent"])
    basemap_draw(ci, T, fill_fn, line_fn, text_fn)
    segs = []
    for it in ci:
        if it[0] == "line":
            P = [T(p) for p in it[1]]
            segs += list(zip(P[:-1], P[1:]))
    for (key, cid, n, name, _), c in zip(PS_CUTS, cuts):
        m = ((c[0][0] + c[1][0]) / 2.0, (c[0][1] + c[1][1]) / 2.0)
        lab.append((T(m), u"%s · %s" % (cid, name), True, n))
    lab.append((T(PS_KEY_SELINOS[int(len(PS_KEY_SELINOS) * 0.8)]), u"Selinos", False, None))
    r = 1.6
    items_l = []
    for c, s_, bold, n in lab:
        w = text_w(s_, ls, bold) + (2 * r + 0.8 if n else 0.0)
        hb = 2 * r if n else 0.0
        items_l.append(dict(x=c[0], y=c[1], rank=0 if n else 1,
                            wh=lambda f, w_=w, h_=hb: (w_ * f, max(ls * f * (CAP + 0.25), h_))))
    got = place_labels_all(items_l, taken, R, segs, sizes=(1.0,), pad=0.6)
    for i, (c, s_, bold, n) in enumerate(lab):
        if i not in got:
            log.append(u"NOTE key map: label '{}' left out (no free place)".format(s_))
            continue
        b, leader, _ = got[i]
        if leader:
            pg.line([c, lp_leader_end(b, c)], COL["ink2"], 0.15)
        tx_ = b[0]
        if n:
            ps_badge(pg, b[0] + r, (b[1] + b[3]) / 2.0, n, r)
            tx_ += 2 * r + 0.8
        yb = (b[1] + b[3]) / 2.0 - ls * CAP / 2.0
        pg.text(s_, tx_, yb, ls, COL["ink_dark"] if bold else COL["ink2"], bold=bold)
    log.append(u"key map (v10): strip across the top of ps_all, about 1:{:,.0f}; cuts W1-W4 only".format(1000.0 / km))
    return area
