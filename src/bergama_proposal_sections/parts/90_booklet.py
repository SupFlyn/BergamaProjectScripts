# ================================================================ A3 booklet assets (v4, SCRIPT_STANDARD §8)
# The four sections re-laid for the booklet's wide frames (pages C4, C5: 392 x 111 mm drawing area each), drawn natively
# at that size with the same hand-sketch engine (SKETCH_SRC) as the sheet: no text in the PDFs, every word a label
# from the plan's list (booklet/content/plan_merged.json). Option A only. Q500 is a named level line, no heights
# (part B owns them), each at the sheet's level. Element numbers only where the plan asks (upstream).
BK_W, BK_H = 392.0, 116.0                      # plan frame (booklet_slots.json); drawing area = h - 5 mm caption
BK_LAB, BK_KEY = 7.5, 9.5                      # label sizes, pt (labels; key labels)
BK_LEGEND = [{"kind": "fill", "colour": "7FA7B8", "label": "winter water"},
             {"kind": "fill", "colour": "A9C3CC", "label": "summer strip"},
             {"kind": "fill", "colour": "4F9BD9", "label": "reach of the design flood (Q500)"},
             {"kind": "fill", "colour": "89986A", "label": "reeds and planting"},
             {"kind": "line", "colour": "BC6F45", "label": "walkable edge"}]
BK_GARDEN = {"kind": "fill", "colour": "C6C08D", "label": "Demeter's Garden"}
BK_SOURCES = [("rhs_lavender", u"RHS, Lavender growing guide (no soil that becomes waterlogged over winter)",
               u"https://www.rhs.org.uk/Advice/profile?pid=127"),
              ("ecocrop_olive", u"FAO Ecocrop, Olea europaea (will not tolerate waterlogged soils)",
               u"https://ecocrop.apps.fao.org/ecocrop/srv/en/cropView?id=1553")]
BK_INK, BK_INK2, BK_ROAD, BK_IDEA = "4A3F35", "847E75", "3A3A3A", "1E1E1E"
BK_WATER, BK_WATER_D, BK_ACC, BK_HER = "5C7A86", "5E8494", "BC6F45", "8B2D2D"


def _bk_tf(x0, kx, y0, ky, yb):
    """Sketch units -> frame mm (y up): the sheet's profile stretched for the wide frame (schematic, not to scale)."""
    def TX(x):
        return x0 + kx * x

    def TY(y):
        return y0 + ky * (y - yb)

    def T(x, y):
        return (TX(x), TY(y))
    return TX, TY, T


def _bk_lab(L, s, x, y, pt=BK_LAB, col=BK_INK, bold=False, anchor="L"):
    """One label (page item, size in pt, y up from the bottom; bk_take_text turns it into a blocks.json label)."""
    L.append(("text", s, x, y, pt, col, bold, anchor))


def _bk_lines(L, rows, x, y, pt=BK_LAB, col=BK_INK, bold=False, lead=None, anchor="L"):
    lead = lead or pt * PT * 1.28
    for i, s in enumerate(rows):
        _bk_lab(L, s, x, y - i * lead, pt, col, bold, anchor)


def _bk_walk(S, o, pts, dy=0.75):
    """The walkable edge (legend): a terracotta hand line just above a surface people walk on."""
    S.sketch(o, [(x, y + dy) for x, y in pts], "walkable edge", S.ACCENT, S.PEN_MED, over=0.0, retrace=False, z=S.Z_LINE)


def _bk_node(L, x, y, n, r=2.6):
    """Element number: the sheet's roundel (graphics) + its number as a label."""
    tmp = Page(0, 0)
    node(tmp, x, y, n, "A", r)
    _bk_lab(L, str(n), x, y - BK_LAB * PT * CAP / 2, BK_LAB, "FFFFFF", True, "C")
    return [it for it in tmp.items if it[0] != "text"]


def _bk_up(S, L):
    """1 · upstream entry: road and roofs -> reed-basin cascade -> regulated release into the summer strip."""
    o = (0.0, 0.0)
    TX, TY, T = _bk_tf(6.0, 1.9, 4.0, 1.25, 8.0)
    g = [T(0, 8), T(0, 64), T(34, 64), T(34, 52), T(68, 52), T(68, 40), T(102, 40), T(102, 28), T(130, 28)] + \
        S.bank(T(130, 28), T(140, 12))[1:] + [T(170, 12), T(170, 28), T(200, 28), T(200, 8)]
    basins = ((40, 52), (74, 40), (108, 28))
    gs = S.sketch_ground(o, S.notch(g, [(TX(x0), TX(x0 + 22), TY(y), 6.25) for x0, y in basins] +
                                    [(TX(150), TX(160), TY(12), 2.75)]))
    q = TY(31.5)                                      # Q500 at the sheet's level (v3): over the lowest terrace
    fl = S.under_level(gs, TX(102), TX(200), q)
    if fl:
        S.wash(o, fl, "flood", S.FLOOD_WASH, S.FLOOD_ALPHA)
    S.rain(o, 18, 62, 89, 97, 22)
    S.fill(o, rect(6, TY(64), 63, TY(64) + 1.6), "road", S.ROAD)
    S.sketch_house(o, 34, 50, TY(64) + 1.6, wall=8.0, pipe=True)
    for x0, y in basins:
        S.water_level(o, gs, TX(x0 + 11), TY(y) - 0.5, S.W_WIN)
        S.reeds(o, TX(x0 + 1), TX(x0 + 21), TY(y) - 6.25, 4.5)
    for pc in S.band(gs, TX(34), TX(130), 2.0):
        S.marker(o, pc, "terraces", S.SUN, angle=60.0, spacing=0.9, thick=0.75, alpha=0.5, base=0.0)
    S.sketch_tree(o, 132.5, TY(52), 10.0)
    S.sketch_tree(o, TX(99), TY(40), 8.5)
    S.water_level(o, gs, TX(155), TY(19), S.W_WIN, bed_hatch=True)
    S.water_level(o, gs, TX(155), TY(12), S.W_EXT, line=False)
    S.sun(o, 362, 72, 3.2)
    S.sketch_person(o, 26, TY(64) + 1.6, 6.0, kind=1)
    S.sketch_person(o, TX(70.8), TY(40), 6.0)
    S.sketch(o, gs, "ground lines", S.SKINK, S.PEN_BOLD, z=S.Z_LINE)
    for a, b, y in ((34, 40, 52), (62, 68, 52), (68, 74, 40), (96, 102, 40), (102, 108, 28)):
        _bk_walk(S, o, [T(a, y), T(b, y)])
    _bk_walk(S, o, [T(170, 28), T(200, 28)])
    S.sketch(o, [T(102, 31.5), T(200, 31.5)], "flood lines", S.HERITAGE, S.PEN_FINE, over=0.0, retrace=False,
             dashed=True, z=S.Z_LINE)
    S.level_mark(o, TX(123.8), q, S.HERITAGE, "flood lines")
    S.hand_arrow(o, (60, 92), (100, TY(52) + 3.0), S.SITE_WATER_D, width=0.8, head=3.0, bend=0.12)
    S.hand_arrow(o, (248, TY(28) + 1.0), (292, TY(12) + 2.5), S.SITE_WATER_D, width=0.8, head=3.0, bend=0.1)
    for a, b in (((64, 49), (66, 44)), ((98, 37), (100, 32)), ((130, 26), (141, 18))):
        S.hand_arrow(o, T(*a), T(*b), S.ACCENT, width=0.6, head=2.0, bend=-0.2)
    # words
    _bk_lab(L, u"ROAD", 8, TY(64) - 3.5, BK_KEY, BK_ROAD, True)
    S.cloud_rain(o, 74.5, 105.0, 1.1)
    _bk_lines(L, [u"street + roof runoff", u"reed basins clean it"], 78, 104.0)
    _bk_lines(L, [u"hold in winter", u"give back in summer"], 118, 26.0, BK_KEY, BK_IDEA)
    S.failsafe_mark(o, 11.0, 51.1, 1.8)
    _bk_lab(L, u"FAIL-SAFE", 15, 50.0, BK_KEY, BK_ACC, True)
    _bk_lines(L, [u"full basin spills to the next", u"last basin into the channel", u"floods bypass the reeds",
                  u"gravity · no pumps"], 15, 46.0, col=BK_ACC)
    S.sun(o, 334.5, 22.9, 0.9)
    _bk_lines(L, [u"continuous strip", u"regulated release", u"today: dry bed"], 338, 22.0, col=BK_WATER)
    _bk_lab(L, u"Q500 floods the lowest terrace", 333, q + 2.4, col=BK_HER)
    extra = []
    for n_, x_, y_ in ((2, TX(51), TY(56) + 3.0), (3, 126.0, TY(56) + 3.0), (4, TX(85), TY(44) + 3.0),
                       (5, TX(143) + 1.0, 20.5), (6, TX(155) + 2.5, 20.5)):
        extra += _bk_node(L, x_, y_, n_)
    return extra


def _bk_k4(S, L):
    """2 · K4: tiers 1 / 2 / 3 from the bed to the street, the Roman bridge behind, the east wall kept."""
    o = (0.0, 0.0)
    TX, TY, T = _bk_tf(6.0, 1.9, 4.0, 1.6, 8.0)
    cx, cy = 120.0, 11.9
    r = math.hypot(98 - cx, 14 - cy)
    t0, t1 = math.atan2(14 - cy, 142 - cx), math.atan2(14 - cy, 98 - cx)
    arc = [T(cx + r * math.cos(t0 + (t1 - t0) * i / 30.0), cy + r * math.sin(t0 + (t1 - t0) * i / 30.0)) for i in range(31)]
    S.sketch(o, arc, "K4 bridge (existing)", S.STONE_HATCH, S.PEN_FINE, over=0.0, retrace=False, dashed=True, z=S.Z_TREE)
    g = [T(0, 8), T(0, 62), T(40, 62), T(40, 50), T(62, 50), T(62, 40), T(84, 40), T(84, 30), T(90, 30)] + \
        S.bank(T(90, 30), T(100, 14))[1:] + [T(150, 14), T(150, 62), T(200, 62), T(200, 8)]
    gs = S.sketch_ground(o, S.notch(g, [(TX(118), TX(132), TY(14), 4.0)]))
    wall = [T(150, 14), T(154, 14), T(154, 62), T(150, 62)]
    S.marker(o, wall, "wall", S.STONE, angle=45.0, spacing=0.8, thick=0.7, alpha=0.55, base=0.35)
    q = TY(52)
    fl = S.under_level(gs, TX(40), TX(150), q)
    if fl:
        S.wash(o, fl, "flood", S.FLOOD_WASH, S.FLOOD_ALPHA)
    S.water_level(o, gs, TX(125), TY(33), S.W_WIN, bed_hatch=True)
    S.water_level(o, gs, TX(125), TY(14), S.W_EXT, line=False)
    for x0, x1 in ((0, 40), (40, 84), (84, 100)):
        for pc in S.band(gs, TX(x0), TX(x1), 2.0):
            S.marker(o, pc, "tiers", S.SUN, angle=60.0, spacing=0.9, thick=0.75, alpha=0.5, base=0.0)
    S.reeds(o, TX(102), TX(148), TY(14), 5.5)
    S.fill(o, rect(TX(0), TY(62), TX(16), TY(62) + 1.6), "road", S.ROAD)
    S.sketch_tree(o, TX(24), TY(62), 12.0)
    S.sketch_person(o, TX(31), TY(62), 6.0, kind=1)
    S.sketch_person(o, TX(35), TY(62), 6.0, kind=2, flip=True)
    S.sketch_person(o, TX(195), TY(62), 6.0)
    S.sketch(o, gs, "ground lines", S.SKINK, S.PEN_BOLD, z=S.Z_LINE)
    S.sketch(o, wall, "wall lines", S.SKINK, S.PEN_BOLD, closed=True, z=S.Z_LINE)
    for pts in ((T(16, 62), T(40, 62)), (T(40, 50), T(62, 50)), (T(62, 40), T(84, 40)), (T(154, 62), T(200, 62))):
        _bk_walk(S, o, list(pts))
    S.sketch(o, [(TX(40), q), (TX(150), q)], "flood lines", S.W_EXT, S.PEN_FINE, over=0.0, retrace=False, dashed=True,
             z=S.Z_LINE)
    S.tick_dim(o, TX(43), q, TY(62), S.SKINK)
    S.hand_arrow(o, T(138, 34.5), T(138, 50.5), S.SITE_WATER_D, width=0.7, head=2.6)
    S.level_mark(o, TX(146), q, S.W_EXT, "flood lines")
    # words
    _bk_lab(L, u"ROAD", 8, TY(62) - 5.5, BK_KEY, BK_ROAD, True)
    _bk_lab(L, u"K4 deck: traffic", 8, TY(62) - 9.1)
    _bk_lines(L, [u"dry top · in use all year", u"level 3 street: dry"], 42, TY(62) - 5.5)
    _bk_lines(L, [u"flood terraces", u"closed only in big floods", u"level 2 only in 10-year storms"], 83.5,
              TY(50) - 5.3)
    _bk_lab(L, u"level 1 floods each year", 172, TY(30) - 5.0, anchor="R")
    _bk_lab(L, u"the street stays above Q500", 200, q + 2.2, BK_KEY, BK_IDEA)
    _bk_lab(L, u"the stream may climb the steps", 200, q - 9.0, BK_KEY, BK_IDEA)
    _bk_lab(L, u"K4 Roman bridge, kept as it is", 205, TY(34) + 3.7, col=BK_INK2)
    _bk_lab(L, u"existing east wall kept", 302, TY(62) + 3.7)
    S.cloud_rain(o, 304.5, TY(33) + 0.0, 1.1)
    _bk_lab(L, u"every winter: bed under water", 308, TY(33) - 1.0, col=BK_WATER)
    S.sun(o, 304.5, TY(14) + 2.9, 0.9)
    _bk_lab(L, u"today: dry, pools", 308, TY(14) + 2.0, col=BK_WATER)
    return []


def _bk_curve(a, b, bend, n=24):
    m = ((a[0] + b[0]) / 2.0 - (b[1] - a[1]) * bend, (a[1] + b[1]) / 2.0 + (b[0] - a[0]) * bend)
    return [(a[0] * (1 - t) ** 2 + 2 * m[0] * t * (1 - t) + b[0] * t * t,
             a[1] * (1 - t) ** 2 + 2 * m[1] * t * (1 - t) + b[1] * t * t) for t in [i / float(n) for i in range(n + 1)]]


def _bk_k5(S, L):
    """3 · K5: Demeter's Garden on the south-west dry top, clean strip water lifted to it (intake dashed: not
    designed), the Üç Kemer bridge behind, kept."""
    o = (0.0, 0.0)
    TX, TY, T = _bk_tf(6.0, 1.9, 6.0, 1.6, 8.0)
    for c in (108.3, 125.0, 141.7):
        arc = [T(c + 8.0 * math.cos(math.pi * i / 20.0), 20.0 + 8.0 * math.sin(math.pi * i / 20.0)) for i in range(21)]
        S.sketch(o, arc, "K5 bridge (existing)", S.STONE_HATCH, S.PEN_FINE, over=0.0, retrace=False, dashed=True,
                 z=S.Z_TREE)
    S.sketch(o, [T(98, 36), T(156, 36)], "K5 bridge (existing)", S.STONE_HATCH, S.PEN_FINE, over=0.0, retrace=False,
             dashed=True, z=S.Z_TREE)
    g = [T(0, 8), T(0, 40), T(92, 40)] + S.bank(T(92, 40), T(104, 14))[1:] + [T(150, 14), T(160, 40), T(200, 40), T(200, 8)]
    gs = S.sketch_ground(o, S.notch(g, [(TX(56), TX(68), TY(40), 5.6), (TX(122), TX(136), TY(14), 4.0)]))
    q = TY(35)
    fl = S.under_level(gs, TX(92), TX(158), q)
    if fl:
        S.wash(o, fl, "flood", S.FLOOD_WASH, S.FLOOD_ALPHA)
    S.water_level(o, gs, TX(129), TY(22), S.W_WIN, bed_hatch=True)
    S.water_level(o, gs, TX(129), TY(14), S.W_EXT, line=False)
    S.water_level(o, gs, TX(62), TY(40) - 0.5, S.W_WIN)
    for pc in S.band(gs, TX(18), TX(92), 2.0):
        S.marker(o, pc, "garden", S.hx("C6C08D"), angle=60.0, spacing=0.9, thick=0.75, alpha=0.5, base=0.0)
    S.reeds(o, TX(104), TX(118), TY(14), 5.0)
    S.fill(o, rect(TX(0), TY(40), TX(16), TY(40) + 1.6), "road", S.ROAD)
    y0 = TY(40)
    cafe = rect(TX(72), y0, TX(86), y0 + 8.8)
    S.wash(o, cafe, "garden", S.HOUSE_WALL, 0.45)
    S.sketch(o, cafe, "garden", S.INK2, S.LW_EDGE, closed=True)
    S.sketch(o, [(TX(72) - 1.9, y0 + 8.8), (TX(86) + 1.9, y0 + 8.8), (TX(86) - 1.9, y0 + 12.0), (TX(72) + 1.9, y0 + 12.0)],
             "garden", S.INK2, S.LW_EDGE, closed=True)
    S.sketch_tree(o, TX(26), y0, 13.0)
    S.sketch_tree(o, TX(38), y0, 12.0)
    S.sketch_tree(o, TX(49), y0, 18.0)
    S.sketch_person(o, TX(89), y0, 6.0, kind=1)
    S.sketch_person(o, TX(31), y0, 6.0, kind=2, flip=True)
    S.sketch_person(o, TX(195), y0, 6.0)
    S.sketch(o, gs, "ground lines", S.SKINK, S.PEN_BOLD, z=S.Z_LINE)
    _bk_walk(S, o, [T(86, 40), T(92, 40)])
    _bk_walk(S, o, [T(160, 40), T(200, 40)])
    S.sketch(o, [T(95, 35), T(158, 35)], "flood lines", S.W_EXT, S.PEN_FINE, over=0.0, retrace=False, dashed=True, z=S.Z_LINE)
    S.level_mark(o, TX(154), q, S.W_EXT, "flood lines")
    cv = _bk_curve((TX(129), TY(14) - 1.5), (TX(62) + 6.0, y0 + 1.2), 0.08)
    S.sketch(o, cv[:-2], "intake", S.SITE_WATER_D, S.PEN_MED, over=0.0, retrace=False, dashed=True, z=S.Z_LINE)
    S.hand_arrow(o, cv[-3], cv[-1], S.SITE_WATER_D, width=0.5, head=2.6)
    # words
    _bk_lab(L, u"STREET", 8, y0 - 4.4, BK_KEY, BK_ROAD, True)
    _bk_lab(L, u"DEMETER'S GARDEN", 44, y0 - 5.6, BK_KEY, BK_INK, True)
    _bk_lines(L, [u"dry top · all year", u"no waterlogged soil {src:rhs_lavender} {src:ecocrop_olive}"], 44, y0 - 9.6)
    _bk_lines(L, [u"clean strip water", u"intake and lift: not designed"], 140, 31.5, col=BK_WATER_D)
    c2 = 47.0 + max(text_w(u"beans · tomatoes · peppers", BK_LAB * PT), text_w(u"herbs · greens · cabbages", BK_LAB * PT)) + 5.0
    S.sun(o, 43.5, 102.9, 0.9)
    _bk_lab(L, u"beans · tomatoes · peppers", 47, 102.0)
    _bk_lab(L, u"figs · grapes · quince", c2, 102.0)
    S.cloud_rain(o, 43.5, 97.8, 1.1)
    _bk_lab(L, u"herbs · greens · cabbages", 47, 96.8)
    _bk_lab(L, u"citrus", c2, 96.8)
    _bk_lab(L, u"olives", (TX(26) + TX(38)) / 2.0, y0 + 15.0, col=BK_INK2, anchor="C")
    _bk_lab(L, u"stone pine", TX(49), y0 + 19.4, col=BK_INK2, anchor="C")
    _bk_lab(L, u"cafe", (TX(72) + TX(86)) / 2.0, y0 + 14.0, col=BK_INK2, anchor="C")
    _bk_lab(L, u"basin", TX(62), y0 + 2.4, col=BK_INK2, anchor="C")
    _bk_lab(L, u"K5 Üç Kemer bridge, kept", 205, TY(36) + 4.8, col=BK_INK2)
    S.sun(o, 316.5, 20.9, 0.9)
    _bk_lab(L, u"continuous strip", 320, 20.0, col=BK_WATER)
    return []


def _bk_down(S, L):
    """4 · downstream: wide shallow banks, floodable streamside planting and boardwalk, surplus to farmland outside."""
    o = (0.0, 0.0)
    TX, TY, T = _bk_tf(6.0, 1.9, 4.0, 1.25, 8.0)
    g = [T(0, 8), T(0, 62), T(30, 62), T(46, 30), T(110, 30)] + S.bank(T(110, 30), T(120, 14))[1:] + \
        [T(165, 14), T(175, 32), T(200, 32), T(200, 8)]
    gs = S.sketch_ground(o, S.notch(g, [(TX(136), TX(150), TY(14), 2.75)]))
    q = TY(27)
    fl = S.under_level(gs, TX(110), TX(178), q)
    if fl:
        S.wash(o, fl, "flood", S.FLOOD_WASH, S.FLOOD_ALPHA)
    S.water_level(o, gs, TX(143), TY(21), S.W_WIN, bed_hatch=True)
    S.water_level(o, gs, TX(143), TY(14), S.W_EXT, line=False)
    for pc in S.band(gs, TX(46), TX(110), 2.0):
        S.marker(o, pc, "planting", S.REED, angle=60.0, spacing=0.9, thick=0.75, alpha=0.5, base=0.0)
    S.reeds(o, TX(121), TX(134), TY(14), 4.5)
    for x_, h_ in ((78, 7.5), (92, 7.0), (103, 6.3)):
        S.sketch_tree(o, TX(x_), TY(30), h_)
    deck = [T(44.5, 33.2), T(72, 33.2), T(72, 34.2), T(44.5, 34.2)]
    S.fill(o, deck, "boardwalk", S.SEC_PAVE)
    for x_ in (50, 58, 66):
        S.sketch(o, [T(x_, 33.2), T(x_, 30)], "boardwalk", S.INK2, S.LW_EDGE, over=0.0, retrace=False)
    S.sketch_person(o, TX(60), TY(34.2), 6.0, kind=1)
    S.sketch_person(o, TX(14), TY(62), 6.0)
    S.sketch(o, gs, "ground lines", S.SKINK, S.PEN_BOLD, z=S.Z_LINE)
    _bk_walk(S, o, [T(0, 62), T(30, 62)])
    _bk_walk(S, o, [T(175, 32), T(200, 32)])
    S.sketch(o, [T(112, 27), T(176, 27)], "flood lines", S.W_EXT, S.PEN_FINE, over=0.0, retrace=False, dashed=True, z=S.Z_LINE)
    S.level_mark(o, TX(170), q, S.W_EXT, "flood lines")
    S.hand_arrow(o, (TX(141), TY(16)), (TX(100), TY(31.5)), S.SITE_WATER_D, width=0.8, head=3.0, bend=0.15)
    S.hand_arrow(o, (352, 37.5), (372, 49.5), S.ACCENT, width=0.6, head=2.2, bend=-0.2)
    # words
    _bk_lines(L, [u"clean stream back", u"walkable planted edge"], 12, 102.0, BK_KEY, BK_IDEA)
    _bk_lines(L, [u"arrives clean from upstream", u"no treatment here"], 124, 102.0)
    S.failsafe_mark(o, 11.0, 61.1, 1.8)
    _bk_lab(L, u"FAIL-SAFE", 15, 60.0, BK_KEY, BK_ACC, True)
    _bk_lab(L, u"high water passes over", 15, 56.0, col=BK_ACC)
    _bk_lines(L, [u"floodable streamside planting", u"flood- and drought-tolerant", u"no farmland inside the site"],
              98, 26.2)
    _bk_lab(L, u"floodable boardwalk: open deck", 92, 46.5)
    _bk_lab(L, u"floods spread wide, shallow", 240, q + 2.5, col=BK_WATER)
    _bk_lines(L, [u"surplus to farmland outside", u"route: not designed"], 386, 58.2, col=BK_ACC, anchor="R")
    S.sun(o, 344.0, 21.9, 0.9)
    _bk_lab(L, u"regulated strip", 347.5, 21.0, col=BK_WATER)
    return []


BK_FRAMES = [("c4_s1", _bk_up, u"1 · Upstream entry: collect, clean and hold · schematic", False),
             ("c4_s2", _bk_k4, u"2 · K4 bridge: amphibious heritage threshold · schematic", False),
             ("c5_s1", _bk_k5, u"3 · K5 bridge: Demeter's Garden · schematic", True),
             ("c5_s2", _bk_down, u"4 · Downstream reach: give back · schematic", False)]


def _bk_minlw(it):
    """Line widths >= 0.1 mm in print (the sketch's hair lines are finer)."""
    if it[0] == "line" and it[3] < 0.1:
        return it[:3] + (0.1,) + it[4:]
    if it[0] == "poly" and it[3] and it[4] < 0.1:
        return it[:4] + (0.1,) + it[5:]
    if it[0] == "circle" and it[5] and it[6] < 0.1:
        return it[:6] + (0.1,)
    return it


def bk_draw(fn, W, H):
    """One frame: (graphics items, labels) drawn for W x H mm (the layout is set for BK_W x BK_H - caption; another
    slot size gets the same drawing scaled uniformly and centred, labels at their set size)."""
    E = sketch_engine()
    E["FORM"] = "A"
    del E["ZP"][:]
    E["ORDER"][0] = 0
    S = _types.SimpleNamespace(**E)
    L = []
    extra = fn(S, L)
    items = [it for _, _, it in sorted(E["ZP"], key=lambda e: (e[0], e[1]))] + extra
    del E["ZP"][:]
    H0 = BK_H - BK_CAPTION_MM
    f = min(W / BK_W, H / H0)
    if abs(f - 1.0) > 1e-6:
        dx, dy = (W - BK_W * f) / 2.0, (H - H0 * f) / 2.0
        items = xform(items, f, dx, dy)
        L = [("text", s, x * f + dx, y * f + dy, pt, c, b, a) for _, s, x, y, pt, c, b, a in L]
    keep, labels = bk_take_text(items + L, H)
    return [_bk_minlw(it) for it in keep], labels


def booklet_export(log):
    """Booklet assets (ASSET_SPEC.md): output/bergama_proposal_sections/booklet/c4_s1 ... c5_s2.pdf + blocks.json."""
    bk = BkBlocks(OUT_DIR, GH_LABEL, VERSION)
    for k, t, u in BK_SOURCES:
        bk.source(k, t, u)
    for bid, fn, cap, garden in BK_FRAMES:
        W, H = bk_frame(OUT_FOLDER + "/" + bid, BK_W, BK_H)
        if abs(W - BK_W) > 0.5 or abs(H - (BK_H - BK_CAPTION_MM)) > 0.5:
            log.append(u"booklet %s: frame is %.0f x %.0f mm, the layout is for %.0f x %.0f: scaled, re-lay it" %
                       (bid, W, H, BK_W, BK_H - BK_CAPTION_MM))
        keep, labels = bk_draw(fn, W, H)
        pg = Page(W, H)
        pg.items = keep
        name = bid + ".pdf"
        write_pdf(pg, bk.path(name), u"Bergama proposal sections {} booklet {}".format(VERSION, bid))
        bk.drawing(bid, name, labels, caption=cap, scale_den=None, legend=BK_LEGEND + ([BK_GARDEN] if garden else []))
    return bk.save()
