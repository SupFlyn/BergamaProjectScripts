# ================================================================ v17 key map: this page's two cuts (G-R4-9, PLAN §4.5)
# v17 (round 4, S7): ONE key map per booklet page, in the first side column with room (ps_page): common/keymap.py
# km_map with only the page's two cuts (red R01 symbol, triangles pointing downstream: the way every section looks),
# a muted base, the study line, main street and place names (placed with the real font, clear of the cuts and the
# north arrow), the north arrow (north_items, no plate) in its top-right corner, a hairline neatline. Every text of
# it goes into the page's TextPage. The v10-v16 strip (turned frame, bridge bars, letter key) is gone.
PS_KM_PAD = 120.0                     # m round the page's cut ends in the map window (drawing rule: streets around)
PS_KM_NORTH = 5.0                     # print mm: the north arrow's height


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




def ps_key_map(pg, tp, box, cids, page, log):
    """the page's key map in box (x0, y0, x1, y1) print mm (y up); its texts registered in tp (key map names may
    sit on the map: allow = the map); the box is a drawing block of the page"""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    nm = u"%s key map" % page
    ends = [p for c in cids for p in level_ends(c)]
    bx = (min(p[0] for p in ends) - PS_KM_PAD, min(p[1] for p in ends) - PS_KM_PAD,
          max(p[0] for p in ends) + PS_KM_PAD, max(p[1] for p in ends) + PS_KM_PAD)
    na_w = 0.44 * PS_KM_NORTH + 2.0                            # the north arrow's corner, kept free of names
    try:
        km = km_map(list(cids), w, h, page=page, looks=dict((c, -1) for c in cids), box=bx, log=log,
                    legend_box=(w - na_w - 1.5, h - PS_KM_NORTH - 4.5, w, h))
    except Exception as ex:
        log.append(u"FLAG %s key map not drawn (%s: %s)" % (page, type(ex).__name__, ex))
        km = None
    pg.poly([rect(x0, y0, x1, y1)], fill=COL["white"])

    def fill_fn(rings, hx, al, nonzero=False):
        rr = [r_ for r_ in (ps_clip_ring(r, box) for r in rings) if r_]
        if rr:
            pg.poly(rr, fill=hx, alpha=(al if al is not None and al < 0.975 else None))

    def line_fn(pts, hx, w_, dash, al=None):
        for piece in ps_clip_line(pts, box):
            pg.line(piece, hx, w_ or 0.1, dash=list(dash) if dash else None)

    def text_fn(s_, xy, size, hx, bold, align):
        tp.put(s_, xy[0], xy[1], size / PT, bold, align or "L", 0.0, nm, "map", hx, (nm,))
    if km:
        km_draw(km, lambda q: (x0 + q[0], y0 + q[1]), fill_fn, line_fn, text_fn, page=page)
        for m_ in km.get("missing") or []:
            log.append(u"FLAG %s key map: %s not drawn" % (page, m_))
    basemap_draw(north_items(x1 - 0.5 * na_w - 0.5, y1 - PS_KM_NORTH - 3.2, 0.0, PS_KM_NORTH), lambda p: p,
                 fill_fn, line_fn, text_fn)
    pg.poly([rect(x0, y0, x1, y1)], stroke=COL["ink"], lw=0.088)   # the map's 0.25 pt neatline
    tp.block(box, nm)
    log.append(u"%s key map: %s, %.0f x %.0f mm, north arrow without plate" % (page, u" + ".join(cids), w, h))
