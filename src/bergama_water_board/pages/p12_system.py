# p.12 the water system: chain, storage cubes and cleaning (split from code.py on 29 Oct 2026; moved unchanged)


def draw_chain(opt, W=380.0):
    """v1.14: the stream as one ribbon W mm long ending in an arrow, the elements as numbered roundels on it, a
    pictogram and the keywords under each, the three places as brackets over it. Returns a Page."""
    pg = Page(0, 0)
    rh, fs, ic = 4.2, FS_MIN, 8.0
    pg.poly([[(0.0, -rh), (W - 9.0, -rh), (W - 9.0, -rh - 2.6), (W, 0.0), (W - 9.0, rh + 2.6), (W - 9.0, rh),
              (0.0, rh)]], fill=MP["discharge"][0], stroke=MP["discharge"][1], lw=0.3)
    spans = [(0.0, 0.34), (0.34, 0.70), (0.70, 0.97)]          # share of the ribbon each place takes
    low = -rh
    for (place_, verb, els), (f0, f1) in zip(CHAIN, spans):
        x0, x1 = f0 * W, f1 * W
        pg.line([(x0 + 1.0, rh + 2.0), (x0 + 1.0, rh + 4.0), (x1 - 1.0, rh + 4.0), (x1 - 1.0, rh + 2.0)],
                COL["river_dark"], 0.35)
        pg.text(place_, x0 + 1.0, rh + 6.0, 3.6, COL["ink_dark"], bold=True)
        pg.text(verb, x0 + 2.0 + text_w(place_, 3.6, True), rh + 6.0, fs, MP["discharge"][2], bold=True)
        step = (x1 - x0) / len(els)
        for j, (n_, kind, words) in enumerate(els):
            cx = x0 + step * (j + 0.5)
            if n_:
                node(pg, cx, 0.0, n_, opt, 3.0)
            else:
                pg.circle(cx, 0.0, 1.0, fill=COL["river_dark"])
            pg.line([(cx, -rh), (cx, -rh - 1.8)], COL["river_dark"], 0.2)
            icon(pg, kind, cx - ic / 2.0, -rh - 2.2, ic)
            yb = para(pg, cx - step / 2.0 + 1.0, -rh - 3.2 - ic, step - 2.0, words, fs, COL["ink"])
            low = min(low, yb)
    pg.text(u"one way, with the stream · nothing pumped back · the stream stays above the legal minimum flow " +
            cite(CHAIN_SRC), 0.0, low - fs * 1.6, fs, MP["discharge"][2], bold=True)
    return pg


def draw_cleaning(pg, x, y, w, h, s):
    """v1.14 (p.11-14 -> 2 pages, chain and storage largest): why and how we clean as two groups of pictogram tiles
    (the removal and coliform charts became the tiles' key figures; their figures stay in results.json)."""
    def lay(p_, extra):
        p_.text(u"WHY WE CLEAN", x, y - 3.4 * s, 3.4 * s, C["dark"], bold=True)
        yy = tiles(p_, x, y - 5.2 * s, w, WHY_T, s, 2, extra) - 3.0 * s
        p_.text(u"HOW", x, yy - 3.4 * s, 3.4 * s, C["dark"], bold=True)
        return tiles(p_, x, yy - 5.2 * s, w, HOW_T, s, 2, extra)
    rows = (len(WHY_T) + 1) // 2 + (len(HOW_T) + 1) // 2       # v2: 2 x 2 + 2 x 2 since the NO DATA tiles went
    spare = lay(Page(1, 1), 0.0) - (y - h + 2.05)             # what the column has left at the bottom (fit_draw's pad
                                                              # 2.0, kept 0.05 mm clear so fit's test never flips)
    return lay(pg, spare / rows if spare > 0 and rows else 0.0)


def draw_cube(pg, V, u0, v0, e, tones, solid=True, dash=None):
    """A cube of edge e m standing at (u0, v0) in the view V: top, and the two sides facing the viewer."""
    P = lambda i, j, l: V(u0 + i * e, v0 + j * e, l * e)
    sides = [((0, -1), [(0, 0), (1, 0)]), ((1, 0), [(1, 0), (1, 1)]), ((0, 1), [(1, 1), (0, 1)]),
             ((-1, 0), [(0, 1), (0, 0)])]
    if solid:
        for (nu, nv), ((i0, j0), (i1, j1)) in sides:
            vis, lit = V.visible(nu, nv)
            if vis:
                pg.poly([[P(i0, j0, 0), P(i1, j1, 0), P(i1, j1, 1), P(i0, j0, 1)]], fill=tones[1] if lit else tones[2],
                        stroke=tones[2], lw=0.15, alpha=0.9)
        pg.poly([[P(0, 0, 1), P(1, 0, 1), P(1, 1, 1), P(0, 1, 1)]], fill=tones[0], stroke=tones[2], lw=0.15, alpha=0.9)
    else:
        for i0, j0, l0, i1, j1, l1 in ((0, 0, 0, 1, 0, 0), (1, 0, 0, 1, 1, 0), (1, 1, 0, 0, 1, 0), (0, 1, 0, 0, 0, 0),
                                       (0, 0, 1, 1, 0, 1), (1, 0, 1, 1, 1, 1), (1, 1, 1, 0, 1, 1), (0, 1, 1, 0, 0, 1),
                                       (0, 0, 0, 0, 0, 1), (1, 0, 0, 1, 0, 1), (1, 1, 0, 1, 1, 1), (0, 1, 0, 0, 1, 1)):
            pg.line([P(i0, j0, l0), P(i1, j1, l1)], tones[2], 0.25, dash=dash or [1.0, 0.7])
    pts = [P(i, j, l) for i in (0, 1) for j in (0, 1) for l in (0, 1)]
    return (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))


def draw_storage_cubes(opt, fill_h=None, gap=0.0, lift=0.0):
    """The storage the strip needs, worst case, as cubes at 1:1,000 (calculated volumes), with IN and OUT. v3.2:
    fill_h = the height the column gives it: the figures' rows then share what height is left (gap, mm between rows)
    and the cubes sit level with the middle of the list (lift, mm the list starts higher), as the cleaning tiles beside
    them share theirs; the same scale and words."""
    pg = Page(0, 0)
    k = 1000.0 / CUBE_SCALE
    V = BoxView(PSI, 0.0, k, 0.0, 0.0)
    e3, e2, e1 = VOL_UNSEALED ** (1.0 / 3.0), VOL_SEALED ** (1.0 / 3.0), VOL_FIRST ** (1.0 / 3.0)
    draw_cube(pg, V, 0, 0, e2, MP["storage"], True)
    b3 = draw_cube(pg, V, 0, 0, e3, MP["storage"], False)
    b1 = draw_cube(pg, V, e3 + 14.0, 0, e1, MP["discharge"], True)
    e4 = WB_STORE[0] ** (1.0 / 3.0)                  # v1.6: the design storage (water balance), same 1:1,000
    b4 = draw_cube(pg, V, e3 + e1 + 28.0, 0, e4, MP["discharge"], False, [1.6, 0.8])
    # v3.2 (Aras 27 Oct, Prompt 8: labels overlapping): over its cube's top (it was under the cube's lowest corner,
    # which put it on the first-fill cube in front); still under the figures' list, which starts 6 mm over that top
    pg.text(u"design storage", (b4[0] + b4[2]) / 2.0, b4[3] + 2.0, FS_MIN, COL["ink2"], align="C")
    node(pg, b3[0] + 2.0, b3[3] + 4.0, 4, opt, 2.4)
    tx = max(b3[2], b1[2], b4[2]) + 6.0
    lines = [("cube", u"{:,.0f} m³".format(VOL_SEALED), u"worst case · clay-sealed · solid cube · {:.1f} m edge".format(e2),
              u"calculated; " + RR + u" §4; 4 m strip, recirculated (one way not recalculated)"),
             ("cube", u"at least {:,.0f} m³".format(VOL_UNSEALED), u"unsealed sand bed · dashed cube · {:.1f} m edge".format(e3),
              u"calculated; " + RR + u" §4"),
             ("strip", u"{:,.0f} m³".format(VOL_FIRST), u"first fill · 2,949 x 4 x 0.30 m · small cube · {:.1f} m".format(e1),
              u"design values 2,949 m x 4 m x 0.30 m; " + CM + u" §4"),
             ("days", u"about 1 %", u"of the driest year's flow · winter fills it · seal the strip",
              u"calculated; " + CM + u" (storage row)"),
             ("rain", u"IN", u"winter water from the basins · " + ROUTE_IN[0], ROUTE_IN[1]),
             ("strip", u"OUT", u"tops up the strip · " + ROUTE_OUT[0], ROUTE_OUT[1]),
             ("cube", u"{:,.0f}-{:,.0f} m³".format(WB_STORE[0], WB_STORE[1]),
              u"design incl. strip · aquifer recharge · {:.0f}-{:.0f} % of farm need, 1-in-5 dry · {:.1f} m edge".format(
                  WB_PCT[0], WB_PCT[1], e4), WB_SRC),
             ("drop", u"about {:,.0f} m³/yr".format(WB_STRIP), u"losses only (one way, on to the farms) · evaporation + seepage "
              u"5 mm/d sealed / 25 mm/d unsealed · up to 10 x possible",
              u"calculated, sequent-peak over 2016-2021; seepage 25 mm/day = the bottom of FAO's sand range; " + RR +
              u" §4, A6; " + WB_SRC)]
    y = max(b3[3], b4[3]) + 6.0 + lift                # v1.8: each line = pictogram + big figure + keywords + [n]
    f = STORE_K                                       # v1.13: the figures and keywords read on the booklet page
    n0 = len(pg.items)
    for kind, big, t, src in lines:
        icon(pg, kind, tx, y, 5.0 * f)
        pg.text(big, tx + 6.5 * f, y - 3.6 * f, 3.0 * f, C["d3"], bold=True)
        lx = tx + 7.5 * f + text_w(big, 3.0 * f, True)
        yy = y - 1.6 * f
        for ln in wrap(t + u" " + cite(src), 1.9 * f, STORE_LIST_W - (lx - tx)):
            pg.text(ln, lx, yy, 1.9 * f, COL["ink"])
            yy -= 2.4 * f
        y = min(y - 6.6 * f, yy - 0.8 * f) - gap
    n1 = len(pg.items)
    pg.text(u"cube edges = cube root of the volume, drawn at 1:{:,.0f}".format(CUBE_SCALE), b3[0], b3[1] - 4.0 -
            FS_MIN * 1.5, FS_MIN, COL["ink2"])
    if not fill_h:
        return pg
    # v3.2 (Aras 27 Oct, Prompt 8; P4's open item "about 70 mm empty at the bottom of the cube column"): the list
    # (lb) is stretched to fill_h by equal gaps between its rows; the cubes, their number and note (cb) stay put and the
    # list is lifted so that its middle meets theirs; the whole is then exactly fill_h high
    lb, cb = items_bbox(pg.items[n0:n1]), items_bbox(pg.items[:n0] + pg.items[n1:])
    if fill_h <= max(lb[3], cb[3]) - min(lb[1], cb[1]) or len(lines) < 2:
        return pg
    return draw_storage_cubes(opt, None, (fill_h - (lb[3] - lb[1])) / (len(lines) - 1.0),
                              max(0.0, (cb[1] + cb[3] + fill_h) / 2.0 - lb[3]))
