# p.18 the farms and the decision (split from code.py on 29 Oct 2026; moved unchanged)


def draw_farms_text(pg, x, y, w, h, s):
    fs = 2.6 * s
    lab_w = text_w(u"Groundwater potential", fs) + 4.0
    gx, top = x + 10.0 + lab_w, y - 4.0
    gw = w - 20.0 - lab_w - text_w(u"198.01 hm³ a year", fs, True) - 4.0
    bh = 3.6 * s
    for r, (lab, v) in enumerate(AQUIFER):
        yy = top - r * (bh + 2.4 * s)
        pg.text(lab, gx - 2.0, yy - bh * 0.5 - fs * 0.35, fs, C["ink"], align="R")
        pg.poly([rect(gx, yy - bh, gx + gw * v / 200.0, yy)], fill=C["w3"] if r == 0 else C["agri"])
        t, bw_ = u"{} hm³ a year".format(v), gw * v / 200.0
        if text_w(t, fs, True) + 3.0 <= bw_:          # v3.1 (Aras 27 Oct, Prompt 6): the value on its bar, at its end
            pg.text(t, gx + bw_ - 1.5, yy - bh * 0.5 - fs * 0.35, fs, C["white"], bold=True, align="R")
        else:
            pg.text(t, gx + bw_ + 2.0, yy - bh * 0.5 - fs * 0.35, fs, C["ink"], bold=True)
    yy = figs(pg, x + 10.0, top - 2 * (bh + 2.4 * s) - 1.0, [(u"use = {:.1f} x potential".format(198.01 / 45.4),
              u"Lower Bakırçay · farm water eases the aquifer " + cite(u"published, North Aegean drought management "
              u"plan 2018 (official); ratio calculated; " + WD))], w - 20.0, 4.0 * s, 2.6 * s, C["acc"]) - 2.8 * s * 0.8
    return tiles(pg, x + 10.0, yy, w - 20.0, GOES_T, s, 2)


def draw_decision(pg, x, y, w, h, s):
    """v1.12 (Aras 26 Oct 07:06 and his sketch): the seven steps clockwise round a rectangle, 1-4 along the top, 5-7
    back along the bottom; the closing arrow (7 -> 1) in red says what really closes the loop: the next winter's
    stream, never a pump (the water runs one way). Returns the lowest y drawn."""
    n = len(DECISION)
    top_n = (n + 1) // 2
    gap, vg = 16.0 * s, 24.0 * s
    bw = (w - (top_n - 1) * gap) / top_n
    bh = 0.0
    for t, src in DECISION:                          # one height for every box: the tallest content
        bh = max(bh, 9.0 * s + len(wrap(t, 3.2 * s, bw - 8.0, True)) * 3.2 * s * 1.28 +
                 len(wrap(src, 2.5 * s, bw - 8.0)) * 2.5 * s * 1.28 + 3.0)
    yt = y                                           # top row: its boxes' top edge
    yb = y - bh - vg                                 # bottom row
    bot_x = [x + w - bw - (w - bw) * j / (n - top_n - 1) for j in range(n - top_n)] if n - top_n > 1 else [x]
    pos = [(x + i * (bw + gap), yt) for i in range(top_n)] + [(bot_x[j], yb) for j in range(n - top_n)]
    for i, (t, src) in enumerate(DECISION):
        bx, by = pos[i]
        pg.poly([rect(bx, by - bh, bx + bw, by)], fill=C["white"], stroke=C["d2"], lw=0.4)
        pg.text(str(i + 1), bx + 3.0, by - 7.0 * s, 6.0 * s, C["d3"], bold=True)
        icon(pg, DEC_ICONS[i], bx + bw - 3.0 - 7.0 * s, by - 1.5, 7.0 * s)
        yy = para(pg, bx + 4.0, by - 8.5 * s, bw - 8.0, t, 3.2 * s, C["dark"], bold=True)
        para(pg, bx + 4.0, yy - 0.6, bw - 8.0, src, 2.5 * s, C["ink"])
    ym = yt - bh / 2.0
    for i in range(top_n - 1):                       # along the top, left to right
        hand_arrow(pg, [(pos[i][0] + bw + 2.0, ym), (pos[i + 1][0] - 2.0, ym)], small=0.7)
    xr = pos[top_n - 1][0] + bw / 2.0                # down the right side
    hand_arrow(pg, [(xr, yt - bh - 2.0), (xr, yb + 2.0)], small=0.7)
    ymb = yb - bh / 2.0
    for j in range(top_n, n - 1):                    # back along the bottom, right to left
        hand_arrow(pg, [(pos[j][0] - 2.0, ymb), (pos[j + 1][0] + bw + 2.0, ymb)], small=0.7)
    xl = pos[0][0] + bw / 2.0                        # the red closing arrow, up the left side
    hand_arrow(pg, [(xl, yb + 2.0), (xl, yt - bh - 2.0)], small=0.7, cols=(C["acc"], C["acc"]))
    para(pg, xl + 6.0, yt - bh - vg / 2.0 + 2.6 * s * 1.28, w * 0.42, LOOP_BACK, 2.6 * s, C["acc"], bold=True)
    pg.text(u"ONE WAY, WITH THE STREAM", x + w * 0.72, yt - bh - vg / 2.0 - 1.2 * s, 3.2 * s, C["d3"], bold=True,
            align="C")
    return yb - bh


def tree_at(pg, P, k, x, y, opt, style="tree", r=3.0, top=8.0, shadow=False):
    draw_tree(pg, P, k, x, y, r, top, TREE_STYLES[style], shadow=shadow)


def draw_farm_picto(opt):
    """Existing farmland off the site: a pictogram (not its shape or size), olives in rows."""
    pg = Page(0, 0)
    k = 1.0
    V = BoxView(PSI, 0.0, k, 0.0, 0.0)
    a, b = 64.0, 40.0
    sides = [((0, -1), (0, 0), (1, 0)), ((1, 0), (1, 0), (1, 1)), ((0, 1), (1, 1), (0, 1)), ((-1, 0), (0, 1), (0, 0))]
    for (nu, nv), (i0, j0), (i1, j1) in sides:
        vis, lit = V.visible(nu, nv)
        if vis:
            pg.poly([[V(i0 * a, j0 * b, 0), V(i1 * a, j1 * b, 0), V(i1 * a, j1 * b, -SLAB_T_M),
                      V(i0 * a, j0 * b, -SLAB_T_M)]], fill=COL["soil"] if lit else COL["soil_dk"], stroke=COL["edge3d"],
                    lw=0.15)
    pg.poly([[V(0, 0, 0), V(a, 0, 0), V(a, b, 0), V(0, b, 0)]], fill=MP["agriculture"][0], stroke=COL["edge3d"], lw=0.15)
    for j in range(1, 4):
        pg.line([V(2, j * b / 4.0, 0), V(a - 2, j * b / 4.0, 0)], MP["agriculture"][1], 0.15)
    for u, v in [(i * a / 6.0 + 4.0, j * b / 4.0) for j in (3, 2, 1) for i in range(6)]:
        tree_at(pg, lambda x, y, z: V(x, y, z), k, u, v, opt, "olive", 2.4, 5.0, shadow=True)
    bb = items_bbox(pg.items)
    node(pg, bb[0] + 3.0, bb[3] + 4.0, 11, opt, 2.6)
    pg.text(u"EXISTING FARMLAND, OFF SITE", bb[0] + 7.0, bb[3] + 3.2, FS_MIN, COL["ink"], bold=True)
    return pg
