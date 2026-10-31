# p.18 where the clean water goes (split from code.py on 29 Oct 2026)
# Revision 30 Oct (T5; D2 a, D7 a, G4, M1, M9, M10): the farmland axonometric is gone; the farms are ONE field tile
# at step 6 of the flow (round 3: one olive tree on one field band beside the aquifer, see below). Each block is drawn
# at its booklet size (mm, 1:1 on A3; the size factor s that code.py's fit() hands in is not used).
# Every fact once; the shared ones (olive need, 1.25 ha, aquifer ratio, arsenic, storage) through facts.py.
# Round 3 (B4, 31 Oct; P18.1, P18.4, G3, G4, G17; booklet: p18 + p19 merged on ONE page, spec
# revision_2026-10-31_round3/handover/B4_work/spec_p18_merged.md): every block drawn at 1:1 for that page:
#   wb_farms     draw_farms_text: P18_W x P18_FLOW_H (369 x 56 mm, a white ground sets the extent): the 7-step loop on
#                the left 7 page columns, and on the right 4 columns the farms outside with the aquifer under them
#                (_p18_farms_block: ONE detailed olive tree on ONE field texture with the drip line, P18.4; groundwater
#                potential against total use as two horizontal bars with direct values). The aquifer is no longer a
#                separate part (draw_farm_picto deleted; code.py places no aquifer part).
#   wb_decision  draw_decision: the four fact boxes 2 x 2 in P18_DEC_W x P18_DEC_H (126 x 38 mm), no fill, no stroke
#                (G17); it sits beside the agriculture "stream comes first" block on the booklet page.
# Each real draw logs "FLAG overlap p18 <crop> n" (label_place.py lp_overlap_flag; code.py build_all appends
# lp_flag_lines() once).

P18_FLOW_W = grid_w(7)                           # the loop: 7 page columns (227 mm)
P18_COLS = 4                                     # step columns inside it (grid_sub)
P18_W = 369.0                                    # the whole wb_farms block: code.py's p18 cell (377) less 2 x 4 mm
P18_FARM_X = P18_W - grid_w(4)                   # the farms + aquifer block: the last 4 page columns (128 mm)
P18_FLOW_H = 56.0                                # the block's height; = half code.py's box (112): the empty aquifer
#                                                  part place() puts at the box centre then lands on the block's foot
P18_GAP_R = 3.0                                  # the least gap between the loop's two rows
P18_MK, P18_IC = 6.0, 8.0                        # step marker (icons.py ico_step) and step icon, mm
P18_FV = 4.2                                     # a box's headline value / step 7's value, mm (12 pt)
P18_BIG = grid_style("value")[0] * GRID_PT       # the aquifer ratio, the block's one headline value
P18_DEC_W, P18_DEC_H = grid_w(4) - 2.0, 38.0     # wb_decision's ground (the crop adds 1 mm a side: 4 columns)
P18_VIG_W = 34.0                                 # the farm vignette's width (one olive tree on one field band), mm
P18_BAND = 3.0                                   # the field texture band under the tree, mm (a drawing size)
P18_OLIVE_ROW_M, P18_OLIVE_TREE_M = 7.0, 5.0     # plants.py: olive 5 x 7 m (Kaya 2017 p.821), printed in cm
P18_PLANT_M3_DAY, P18_PLANT_DAYS = 14304.0, 120  # the town plant's treated water a day (p.12), summer days
P18_DEC_ICONS = [("sewage", True), ("reeds", False), ("uv", False), ("storage", False), ("stream", False),
                 ("field", False), ("not_drinkable", False)]     # (icon, crossed) for steps 1-7
P18_SRC_AQ = u"published, North Aegean drought management plan 2018 (official); " + WD
P18_SRC_NA = u"published, North Aegean water allocation plan 2025; " + REG + u" CL-21"
P18_SRC_AS = u"published, Somay & Gemici 2015; " + REG + u" EN-E3"


def _p18_put(pg, shapes):
    """icons.py / plants.py shapes onto the page (the core's sec_put)"""
    sec_put(pg, shapes)


def _p18_icon(pg, names, x, y, sz, cross=False):
    """icons.py pictogram(s) in the square (x, y - sz)-(x + sz, y): one icon fills it; a pair (the clean stream
    leaving + the field it goes to) sits on the square's diagonal, the water upper left, the field lower right"""
    if len(names) == 1:
        _p18_put(pg, ico_draw(names[0], x + sz / 2.0, y - sz / 2.0, sz))
    else:
        h = sz * 0.58
        _p18_put(pg, ico_draw(names[0], x + h / 2.0, y - h / 2.0, h))
        _p18_put(pg, ico_draw(names[1], x + sz - h / 2.0, y - sz + h / 2.0, h))
    if cross:
        _p18_put(pg, ico_cross(x + sz / 2.0, y - sz / 2.0, sz))


def _p18_real(pg):
    """True on the board's page; False on the 1 x 1 trial pages code.py's fit() draws on (no log line from those)"""
    return getattr(pg, "W", 0) > 1.0


def _p18_text_boxes(items):
    """the boxes (x0, y0, x1, y1) of the text items among items (the overlap test's label boxes)"""
    return [items_bbox([it]) for it in items if it[0] == "text"]


def _p18_ground(pg, n0, x0, y0, x1, y1):
    """the block's white ground under everything drawn since item n0 (it sets the crop's extent; no stroke, G17)"""
    tmp = Page(1, 1)
    tmp.poly([rect(x0, y0, x1, y1)], fill=COL["white"])
    pg.items.insert(n0, tmp.items[0])


def _p18_cols(x0):
    """the 4 step / box columns [(x0, x1)] of the 7-column block from x0"""
    return [(x0 + a, x0 + b) for a, b in grid_sub(P18_FLOW_W, P18_COLS)]


def _p18_steps():
    """the seven steps: (heading, value or None, line). Storage itself is p.10's fact: step 4 says only its share of
    the winter flow (live); arsenic from facts.py (printed here once)"""
    st = fact("storage_m3")
    hold = (u"storage incl. the strip: {:.1f}-{:.1f} % of the Dec-Apr flow".format(
        100.0 * st[0] / WINTER_FLOW, 100.0 * st[1] / WINTER_FLOW) if st else
        u"winter water in the ground, for the dry summer")
    return [
        (u"KEEP SEWAGE OUT", None, u"İZSU sewer"),
        (u"CLEAN AT THE UPSTREAM END", None, u"reed beds at the entry · whole reach clean"),
        (u"DISINFECT WHERE PEOPLE TOUCH IT", None, u"wetlands leave 100-100,000 CFU/100 ml · class A: 0"),
        (u"HOLD WINTER WATER", None, hold),
        (u"KEEP THE STRIP ALIVE", None, u"clean water all summer · feeds the planting"),
        (u"THEN THE FARMS", None, u"existing farmland on the slopes outside the site · reuse class B · no farm "
                                  u"channel inside"),
        (u"NOT FOR DRINKING", u"arsenic > {} µg/L".format(fact_num("arsenic_ug_l")),
         (u"groundwater · stored rain not listed for drinking · drinking needs 0 E. coli/100 ml " +
          cite(P18_SRC_AS)).strip())]


def _p18_step(pg, i, step, x0, top, cw, boxes=None):
    """step i in its column from top: the marker and the icon on one line (the icon's top on top), the heading, the
    value, the line. boxes: the icon's square is added (the overlap test's drawing boxes). Returns (bottom y, the
    marker's centre y)."""
    head, val, line = step
    ym = top - P18_IC / 2.0
    sh, (ax, ay), th, cap = ico_step(x0 + P18_MK / 2.0, ym, P18_MK, "solid")
    _p18_put(pg, sh)
    pg.text(str(i + 1), ax, ay - cap / 2.0, cap / CAP, th, bold=True, align="C")
    nm, crossed = P18_DEC_ICONS[i]
    ix = x0 + P18_MK + 1.5
    _p18_icon(pg, (nm,), ix, top, P18_IC, crossed)
    if boxes is not None:
        boxes.append((ix, top - P18_IC, ix + P18_IC, top))
    tw = cw - 2.0
    yy = para(pg, x0, top - P18_IC - 0.8, tw, head, FS_MIN, C["dark"], bold=True)
    if val:
        yy = para(pg, x0, yy - 0.6, tw, val, P18_FV, C["d3"], bold=True)
    if line:
        yy = para(pg, x0, yy - 0.6, tw, line, FS_MIN, C["ink"])
    return yy - FS_MIN * 0.3, ym


def draw_farms_text(pg, x, y, w, h, s):
    """p.18 the flow (Aras 26 Oct 07:06 and his sketch: the seven steps clockwise round a ring, 1-4 along the top,
    5-7 back along the bottom), on the 4 step columns of 7 page columns: markers and icons (icons.py) on one line, a
    heading and one line under each; the bottom row stands on the block's foot. Round 3 (B4; P18.1, G4): the block
    is P18_W x P18_FLOW_H at 1:1 (a white ground sets the crop's extent; it grows only if the text needs more); the
    farms outside and the aquifer under them sit beside the loop in the last 4 page columns (_p18_farms_block). Under
    the red closing arrow (7 -> 1: the next winter's stream, never a pump), in the empty bottom-left cell: what closes
    the loop and the one-way rule. boxed() hands x 6 mm left of the panel edge; w, h and s are not used (fixed size).
    Returns the lowest y drawn."""
    X0 = x + 6.0
    n0 = len(pg.items)
    cols = _p18_cols(X0)
    cw = cols[0][1] - cols[0][0]
    steps = _p18_steps()
    lead = FS_MIN * 1.28
    tall = [-_p18_step(Page(1, 1), i, steps[i], 0.0, 0.0, cw)[0] for i in range(4, 7)]   # row 2's heights
    foot = y - P18_FLOW_H
    dboxes = []                                      # the overlap test's drawing boxes (icons, the farm drawing)
    bots, ym = [], {}
    for i in range(4):                               # row 1: steps 1-4, left to right
        b_, ym[i] = _p18_step(pg, i, steps[i], cols[i][0], y, cw, dboxes)
        bots.append(b_)
    y1b = min(bots)
    y2 = min(foot + max(tall), y1b - P18_GAP_R)      # row 2 on the foot (never closer than the gap to row 1)
    low = foot
    for i, c in ((4, 3), (5, 2), (6, 1)):            # row 2: steps 5-7, right to left under columns 4, 3, 2
        b_, ym[i] = _p18_step(pg, i, steps[i], cols[c][0], y2, cw, dboxes)
        low = min(low, b_)
    # the arrows: along the top, down column 4, back along the bottom (water); the red closing arrow up column 1
    ia = P18_MK + 1.5 + P18_IC + 1.5                 # where an arrow leaves a step's marker line
    for i in range(3):
        arrow(pg, [(cols[i][0] + ia, ym[i]), (cols[i + 1][0] - 1.0, ym[i])], C["d2"], 0.45, 2.0)
    xd = cols[3][0] + P18_MK / 2.0
    arrow(pg, [(xd, bots[3] - 1.0), (xd, y2 + 0.3)], C["d2"], 0.45, 2.0)
    for i, (ca, cb) in ((4, (3, 2)), (5, (2, 1))):
        arrow(pg, [(cols[ca][0] - 1.0, ym[i]), (cols[cb][0] + ia, ym[i])], C["d2"], 0.45, 2.0)
    xl = X0 + P18_MK / 2.0
    arrow(pg, [(cols[1][0] - 1.0, ym[6]), (xl, ym[6]), (xl, bots[0] - 1.0)], C["acc"], 0.45, 2.0)
    # the bottom-left cell, under the red arrow's level: what closes the loop, then the one-way rule
    yy = para(pg, X0, ym[6] - 2.5, cw - 2.0, LOOP_BACK, FS_MIN, C["acc"], bold=True)
    yy = para(pg, X0, yy - 1.2, cw - 2.0, u"ONE WAY, WITH THE STREAM", FS_MIN, C["d3"], bold=True)
    low = min(low, yy - FS_MIN * 0.3)
    # the farms outside the site and the aquifer under them (the last 4 page columns, level with the loop)
    _p18_farms_block(pg, X0 + P18_FARM_X, y, grid_w(4), foot, dboxes)
    _p18_ground(pg, n0, X0, low, X0 + P18_W, y)
    if _p18_real(pg):
        if low < foot - 0.05:                        # into the label log, which build_all appends to the run log
            LP_LOG.append(u"FLAG p18 wb_farms: the loop's text runs {:.1f} mm below the block's {:.0f} mm "
                          u"(the crop grows; the booklet page has 3 mm to spare)".format(foot - low, P18_FLOW_H))
        lp_overlap_flag(u"p18 wb_farms", _p18_text_boxes(pg.items[n0:]), dboxes, (X0, low, X0 + P18_W, y))
    return low


def _p18_vignette(pg, x0, x1, gy, top, dboxes):
    """P18.4 (G9 agriculture): the farm drawn simplified, ONE field texture + ONE representative crop: a band of field
    ground (plants.py PLA_FIELD, short furrow marks in PLA_ROW, no rows) under one olive tree at print resolution
    (plants.py pla_section: the high-res silhouette where the library has it, else the vector olive with its leaf
    detail; sourced size: the lowest olive height 8 m, crown = the 5 m in-row spacing, Kaya 2017), the drip line
    along the ground. The tree is a symbol: its scale is set by the room (top - gy), not printed."""
    sh = [("poly", [(x0, gy - P18_BAND), (x1, gy - P18_BAND), (x1, gy), (x0, gy)], PLA_FIELD, None, 0.1)]
    n = int((x1 - x0) / 1.6)
    for i in range(n):                               # furrow marks: two staggered lines of short strokes (texture)
        for j, yy in enumerate((gy - 0.9, gy - 2.1)):
            px = x0 + 0.5 + i * 1.6 + (0.8 if j else 0.0) + 0.25 * ((i * 7 + j * 3) % 3)
            if px + 0.6 < x1:
                sh.append(("line", [(px, yy), (px + 0.5, yy + 0.35)], PLA_ROW, 0.08))
    _p18_put(pg, sh)
    h_m = PLA_SPECIES["olive"]["h_range"][0]
    w_m = PLA_CROPS["olive"]["plant_m"]
    k = (top - gy) / h_m
    cx = (x0 + x1) / 2.0
    _p18_put(pg, pla_section("olive", cx, gy, k, h_m=h_m, crown_m=w_m, seed=3))
    pg.line([(x0, gy + 0.3), (x1, gy + 0.3)], C["d2"], 0.3)            # the drip line on the ground
    for i in range(int((x1 - x0) / 4.0)):
        pg.circle(x0 + 2.0 + i * 4.0, gy - 0.6, 0.3, fill=C["d2"])     # its drops
    dboxes.append((x0, gy - P18_BAND, x1, top))


def _p18_farms_block(pg, x0, top, w, foot, dboxes):
    """the farms outside the site and the groundwater under them (Lower Bakırçay, AQUIFER), x0..x0 + w, top..foot:
    the title; left the farm vignette (_p18_vignette) with the olive spacing under it; right the groundwater
    potential and the total use as two horizontal bars on one scale with their values at the bars, the potential's
    length dashed across the use bar, then the ratio (facts.py, printed here once) with its two lines."""
    pg.text(u"THE FARMS OUTSIDE · GROUNDWATER, LOWER BAKIRÇAY", x0, top - CAP * FS_MIN, FS_MIN, C["dark"], bold=True)
    lead = FS_MIN * 1.28
    vx1 = x0 + P18_VIG_W
    cap = wrap(u"olives {:.0f} × {:.0f} cm · drip along every row".format(P18_OLIVE_TREE_M * 100,
                                                                           P18_OLIVE_ROW_M * 100), FS_MIN, P18_VIG_W)
    for j, ln in enumerate(cap):
        pg.text(ln, x0, foot + 0.8 + (len(cap) - 1 - j) * lead, FS_MIN, C["ink"])
    gy = foot + 0.8 + (len(cap) - 1) * lead + CAP * FS_MIN + 1.2 + P18_BAND
    _p18_vignette(pg, x0, vx1, gy, top - CAP * FS_MIN - 2.5, dboxes)
    # the two bars: label over each bar, the value after the potential's bar and inside the use bar's end
    (pot_lab, pot), (use_lab, use) = AQUIFER
    ax0, ax1 = vx1 + 6.0, x0 + w
    k = (ax1 - ax0) / max(pot, use)
    bh = 6.0
    for j, (lab, v, col) in enumerate(((pot_lab, pot, C["w3"]), (use_lab, use, C["agri"]))):
        lb = top - 11.0 - 13.0 * j                   # the label's baseline; the bar 1.5 mm under it
        pg.text(lab, ax0, lb, FS_MIN, C["ink"])
        b1 = lb - 1.5
        L = k * v
        pg.poly([rect(ax0, b1 - bh, ax0 + L, b1)], fill=col)
        t = u"{} hm³ a year".format(v)
        tb = b1 - bh / 2.0 - CAP * FS_MIN / 2.0
        if text_w(t, FS_MIN, True) + 3.0 <= L:       # inside the bar's end, white
            pg.text(t, ax0 + L - 1.5, tb, FS_MIN, COL["white"], bold=True, align="R")
        else:                                        # after the bar
            pg.text(t, ax0 + L + 1.5, tb, FS_MIN, C["ink"], bold=True)
            dboxes.append((ax0, b1 - bh, ax0 + L, b1))
        if j == 0:
            yp0, xp = b1, ax0 + k * pot
        else:
            pg.line([(xp, yp0), (xp, b1 - bh)], C["dark"], 0.3, dash=[1.0, 0.7])
    r = fact_num("aquifer_use_ratio")
    if r:
        yb = foot + 0.8 + lead
        t = r + u" ×"
        pg.text(t, ax0, yb - lead / 2.0, P18_BIG, C["acc"], bold=True)
        lx = ax0 + text_w(t, P18_BIG, True) + 3.0
        pg.text(u"total use against potential", lx, yb, FS_MIN, C["ink"])
        pg.text((u"farm water eases the aquifer " + cite(P18_SRC_AQ)).strip(), lx, yb - lead, FS_MIN, C["ink"])


def draw_decision(pg, x, y, w, h, s):
    """p.18 what the figures support: one box per fact (G4: an icon, one headline value, one line), 2 x 2 in
    P18_DEC_W x P18_DEC_H from the panel edge x, top y (round 3). The olive figures from facts.py (8,000 m³ per ha, 1.25 ha: printed
    here once); a missing live value leaves its boxes out. Returns the lowest y drawn."""
    need = fact("olive_need_m3_ha")
    items = []
    if need:
        items += [
            ("olive", fact_num("olive_need_m3_ha") + u" m³ per ha",
             (u"olives on drip, 1-in-5 dry year " + cite(fact_ref("olive_need_m3_ha")[1] or u"")).strip()),
            ("storage", fact_num("olive_ha_per_10000_m3") + u" ha", u"of olives per 10,000 m³ of stored water"),
            ("treatment", u"about {:,.0f} ha".format(round(P18_PLANT_M3_DAY * P18_PLANT_DAYS / need / 5.0) * 5),
             u"of olives from the town plant's treated water: {:.2f} million m³ in {} summer days".format(
                 P18_PLANT_M3_DAY * P18_PLANT_DAYS / 1e6, P18_PLANT_DAYS))]
    items.append(("chart", u"75 % · 29 %", (u"of farm demand met, North Aegean basin: normal year · very severe "
                                            u"drought " + cite(P18_SRC_NA)).strip()))
    # round 3 (B4; P18.1, G17): 2 x 2 boxes in P18_DEC_W (4 page columns, beside the agriculture "stream comes first"
    # block on the booklet page), separated by whitespace only: no fill, no stroke; w, h and s are not used
    n0 = len(pg.items)
    cols = [(x + a, x + b) for a, b in grid_sub(P18_DEC_W, 2)]
    ic, gap = 8.0, 3.0
    lay = []
    for j, (nm, val, line) in enumerate(items):
        c0, c1 = cols[j % 2]
        tw = c1 - c0 - ic - 2.0
        V, L = wrap(val, P18_FV, tw, True), wrap(line, FS_MIN, tw)
        lay.append((j, nm, c0, V, L, len(V) * P18_FV * 1.18 + 0.8 + len(L) * FS_MIN * 1.28))
    bh = max([t[5] for t in lay] + [ic])
    nrow = (len(lay) + 1) // 2
    tot = max(P18_DEC_H, nrow * bh + (nrow - 1) * gap)
    pg.poly([rect(x, y - tot, x + P18_DEC_W, y)], fill=COL["white"])    # the white ground sets the crop's extent
    dboxes = []
    for j, nm, c0, V, L, _ in lay:
        top = y - (j // 2) * (bh + gap)
        _p18_icon(pg, (nm,), c0, top, ic)
        dboxes.append((c0, top - ic, c0 + ic, top))
        lx, ly = c0 + ic + 2.0, top
        for ln in V:
            ly -= P18_FV * 1.18
            pg.text(ln, lx, ly, P18_FV, C["d3"], bold=True)
        ly -= 0.8
        for ln in L:
            ly -= FS_MIN * 1.28
            pg.text(ln, lx, ly, FS_MIN, C["ink"])
    if _p18_real(pg):
        lp_overlap_flag(u"p18 wb_decision", _p18_text_boxes(pg.items[n0:]), dboxes, (x, y - tot, x + P18_DEC_W, y))
    return y - tot
