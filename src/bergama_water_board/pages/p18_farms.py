# p.18 where the clean water goes (split from code.py on 29 Oct 2026)
# Revision 30 Oct (T5; D2 a, D7 a, G4, M1, M9, M10): the farmland axonometric is gone; the farms are ONE field tile
# (plants.py pla_field_tile: one texture + one olive symbol) at step 6 of the flow. Three blocks, each drawn at its
# booklet size (mm, 1:1 on A3; the size factor s that code.py's fit() hands in is not used):
#   wb_farms, left   draw_farms_text: the flow 1-7 on 4 step columns (grid_sub of 7 page columns), two rows, clockwise
#   wb_farms, right  draw_farm_picto: the aquifer, use against potential (4 page columns, as tall as code.py's box)
#   wb_decision      draw_decision: the fact boxes under the flow, on the same 4 columns (one value + one line each)
# Every fact once; the shared ones (olive need, 1.25 ha, aquifer ratio, arsenic, storage) through facts.py.

P18_FLOW_W = grid_w(7)                           # the flow and the fact boxes: 7 page columns (227 mm)
P18_COLS = 4                                     # step / box columns inside them (grid_sub)
P18_PIC_W, P18_PIC_H = grid_w(4), 112.0          # the aquifer block: 4 page columns x code.py's farm box height, so
#                                                  place() puts it at 1:1 with its top level with the flow's
P18_FLOW_H = 108.0                               # the flow block's height (code.py's box 112, fit() pad 2)
P18_GAP_R = 10.0                                 # the least gap between the flow's two rows
P18_TILE_H = 30.0                                # step 6's field tile, mm (one column wide)
P18_MK, P18_IC = 6.0, 7.0                        # step marker (icons.py ico_step) and step icon, mm
P18_FV = 4.2                                     # a box's headline value / step 7's value, mm (12 pt)
P18_BIG = grid_style("value")[0] * GRID_PT       # the aquifer ratio, the block's one headline value
P18_OLIVE_MM = 14.0                              # the field tile's olive symbol (a symbol, not to scale)
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


def _p18_step(pg, i, step, x0, top, cw):
    """step i in its column from top: the marker and the icon on one line, the heading, the value, the line.
    Returns (bottom y, the marker's centre y)."""
    head, val, line = step
    ym = top - P18_MK / 2.0
    sh, (ax, ay), th, cap = ico_step(x0 + P18_MK / 2.0, ym, P18_MK, "solid")
    _p18_put(pg, sh)
    pg.text(str(i + 1), ax, ay - cap / 2.0, cap / CAP, th, bold=True, align="C")
    nm, crossed = P18_DEC_ICONS[i]
    _p18_icon(pg, (nm,), x0 + P18_MK + 1.5, ym + P18_IC / 2.0, P18_IC, crossed)
    tw = cw - 2.0
    yy = para(pg, x0, top - P18_MK - 1.0, tw, head, FS_MIN, C["dark"], bold=True)
    if val:
        yy = para(pg, x0, yy - 0.6, tw, val, P18_FV, C["d3"], bold=True)
    if line:
        yy = para(pg, x0, yy - 0.6, tw, line, FS_MIN, C["ink"])
    return yy - FS_MIN * 0.3, ym


def draw_farms_text(pg, x, y, w, h, s):
    """p.18 the flow (Aras 26 Oct 07:06 and his sketch: the seven steps clockwise round a ring, 1-4 along the top,
    5-7 back along the bottom), on the 4 step columns of 7 page columns: markers and icons (icons.py) on one line, a
    heading and one line under each; the bottom row stands on the block's foot, so the ring is as tall as the aquifer
    block beside it. Step 6 holds the farms as ONE field tile (D2 a). Inside the ring the red closing arrow (7 -> 1):
    the next winter's stream, never a pump. boxed() hands x 6 mm left of the panel edge. Returns the lowest y drawn."""
    X0 = x + 6.0
    cols = _p18_cols(X0)
    cw = cols[0][1] - cols[0][0]
    steps = _p18_steps()
    cap = wrap(u"olives {:.0f} × {:.0f} cm · drip along every row".format(P18_OLIVE_TREE_M * 100, P18_OLIVE_ROW_M * 100),
               FS_MIN, cw - 2.0)
    lead = FS_MIN * 1.28
    tall = [-_p18_step(Page(1, 1), i, steps[i], 0.0, 0.0, cw)[0] for i in range(4, 7)]   # row 2's heights
    tall[1] += 1.5 + P18_TILE_H + 1.2 + FS_MIN * CAP + (len(cap) - 1) * lead + FS_MIN * 0.3
    foot = y - P18_FLOW_H
    bots, ym = [], {}
    for i in range(4):                               # row 1: steps 1-4, left to right
        b_, ym[i] = _p18_step(pg, i, steps[i], cols[i][0], y, cw)
        bots.append(b_)
    y1b = min(bots)
    y2 = min(foot + max(tall), y1b - P18_GAP_R)      # row 2 on the foot (never closer than the gap to row 1)
    low = y2
    b6 = y2
    for i, c in ((4, 3), (5, 2), (6, 1)):            # row 2: steps 5-7, right to left under columns 4, 3, 2
        b_, ym[i] = _p18_step(pg, i, steps[i], cols[c][0], y2, cw)
        low = min(low, b_)
        if i == 5:
            b6 = b_
    # step 6: the farms, one field tile (texture + one olive), the olive spacing under it
    t1 = b6 - 1.5
    t0 = t1 - P18_TILE_H
    tx0, tx1 = cols[2]
    _p18_put(pg, pla_field_tile((tx0, t0, tx1 - 2.0, t1), 1.0, "olive", symbol_mm=P18_OLIVE_MM))
    for j, ln in enumerate(cap):
        bl = t0 - 1.2 - FS_MIN * CAP - j * lead
        pg.text(ln, tx0, bl, FS_MIN, C["ink"])
        low = min(low, bl - FS_MIN * 0.3)
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
    # inside the ring: what closes the loop (beside the red arrow) and the one-way rule (column 3)
    lw_ = cols[1][1] - X0 - P18_MK
    nl = len(wrap(LOOP_BACK, FS_MIN, lw_, True))
    ymid = (y1b + y2) / 2.0
    para(pg, X0 + P18_MK, ymid + nl * lead / 2.0 + FS_MIN * 0.2, lw_, LOOP_BACK, FS_MIN, C["acc"], bold=True)
    pg.text(u"ONE WAY, WITH THE STREAM", (cols[2][0] + cols[2][1]) / 2.0, ymid - FS_MIN * CAP / 2.0, FS_MIN, C["d3"],
            bold=True, align="C")
    return low


def draw_farm_picto(opt):
    """p.18 the aquifer under the farms (Lower Bakırçay, AQUIFER): groundwater potential against total use as two
    bars on one scale, the potential's level dashed across the use, and the ratio (facts.py, printed here once).
    The block is P18_PIC_W x P18_PIC_H (its white ground sets the extent), so code.py's place() puts it at 1:1.
    (The name stays for code.py's call; D2 a: no farm pictogram any more.)"""
    pg = Page(0, 0)
    W, H = P18_PIC_W, P18_PIC_H
    pg.poly([rect(0.0, 0.0, W, H)], fill=COL["white"])
    pg.text(u"GROUNDWATER, LOWER BAKIRÇAY", 0.0, H - 1.0 - CAP * FS_MIN, FS_MIN, C["dark"], bold=True)
    (pot_lab, pot), (use_lab, use) = AQUIFER
    base, top = 12.0, 92.0
    k = (top - base) / max(pot, use)
    bw = 24.0
    for lab, v, col, bx in ((pot_lab, pot, C["w3"], 4.0), (use_lab, use, C["agri"], 34.0)):
        pg.poly([rect(bx, base, bx + bw, base + k * v)], fill=col)
        pg.text(u"{} hm³ a year".format(v), bx + bw / 2.0, base + k * v + 1.5, FS_MIN, C["ink"], bold=True,
                align="C")
        for j, ln in enumerate(wrap(lab, FS_MIN, bw + 4.0)):
            pg.text(ln, bx + bw / 2.0, base - 3.4 - j * FS_MIN * 1.28, FS_MIN, C["ink"], align="C")
    yp, yu = base + k * pot, base + k * use
    pg.line([(4.0, yp), (34.0 + bw + 1.0, yp)], C["dark"], 0.3, dash=[1.0, 0.7])
    xb = 34.0 + bw + 4.0
    pg.line([(xb - 1.2, yp), (xb, yp), (xb, yu), (xb - 1.2, yu)], C["acc"], 0.4)
    yv = (yp + yu) / 2.0
    pg.text(fact_num("aquifer_use_ratio") + u" ×", xb + 3.0, yv, P18_BIG, C["acc"], bold=True)
    yy = para(pg, xb + 3.0, yv - 0.6, W - xb - 3.0, u"total use against potential", FS_MIN, C["ink"])
    para(pg, xb + 3.0, yy - 0.6, W - xb - 3.0, (u"farm water eases the aquifer " + cite(P18_SRC_AQ)).strip(), FS_MIN,
         C["ink"])
    return pg


def draw_decision(pg, x, y, w, h, s):
    """p.18 what the figures support: one box per fact (G4: an icon, one headline value, one line), on the flow's
    4 step columns from the panel edge x, top y. The olive figures from facts.py (8,000 m³ per ha, 1.25 ha: printed
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
    cols = _p18_cols(x)
    pad, ic = 2.0, 8.0
    lay = []
    for (nm, val, line), (c0, c1) in zip(items, cols):
        tw = c1 - c0 - 3 * pad - ic
        V, L = wrap(val, P18_FV, tw, True), wrap(line, FS_MIN, tw)
        lay.append((nm, c0, c1, V, L, 2 * pad + len(V) * P18_FV * 1.18 + 0.8 + len(L) * FS_MIN * 1.28))
    bh = max([t[5] for t in lay] + [ic + 2 * pad])
    for nm, c0, c1, V, L, _ in lay:
        pg.poly([rect(c0, y - bh, c1, y)], fill=C["paper"], stroke=C["faint"], lw=0.2)
        _p18_icon(pg, (nm,), c0 + pad, y - pad, ic)
        lx, ly = c0 + 2 * pad + ic, y - pad
        for ln in V:
            ly -= P18_FV * 1.18
            pg.text(ln, lx, ly, P18_FV, C["d3"], bold=True)
        ly -= 0.8
        for ln in L:
            ly -= FS_MIN * 1.28
            pg.text(ln, lx, ly, FS_MIN, C["ink"])
    return y - bh
