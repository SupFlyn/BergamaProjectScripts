# p.18 the farms and the decision (split from code.py on 29 Oct 2026)
# T4a (WO-T4a-3, 29 Oct): every pictogram from icons.py (02 §2, R19 quality bar), the 1-7 flow on ico_step markers,
# the farm block redrawn per 02 §4 (plants.py rows at the published olive spacing), people through _p18_fig only.

P18_TILE_ICONS = {"out": ("stream_out", "field"), "olive": ("olive",), "plant": ("treatment",), "drought": ("chart",),
                  "nodrink": ("not_drinkable",)}
P18_DEC_ICONS = [("sewage", True), ("reeds", False), ("uv", False), ("storage", False), ("stream", False),
                 ("field", False), ("not_drinkable", False)]     # (icon, crossed) for steps 1-7
P18_INTERNAL = re.compile(u"\\s*\\((?:D\\d+|[A-Z]{2}-[A-Z]?\\d+)\\)")   # register / decision codes, never printed (D13)
P18_OLIVE_ROW_M, P18_OLIVE_TREE_M = 7.0, 5.0     # plants.py: olive 5 x 7 m (Kaya 2017 p.821), 7 m between the rows
P18_BLOCK = (8, 10)                              # rows, trees per row: one 56 x 50 m block
P18_SOIL_M = 2.0                                 # soil shown under the field, graphic only
P18_BRANCH_M = 1.90                              # the branch the picker reaches (figures.py "olive" pose)


def _p18_put(pg, shapes):
    """icons.py / plants.py shapes onto the page (the core's sec_put)"""
    sec_put(pg, shapes)


def _p18_clean(t):
    return P18_INTERNAL.sub(u"", t)


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


def _p18_tiles(pg, x, y, w, items, s, cols=2):
    """p.18's fact tiles (the core's tiles() layout) with icons.py pictograms: items = [(tile key, heading, figure or
    None, line, source)]; the source prints only its public part (cite). Returns the bottom y."""
    fh, fb, ft = 2.5 * s, 4.4 * s, 2.15 * s
    ic, pad, g = 10.0 * s, 2.2 * s, 2.4 * s
    tw = (w - (cols - 1) * g) / cols
    txw = tw - ic - 3 * pad
    lay = []
    for kind, head, big, line, src in items:
        c_ = cite(src) if src else u""
        L = (wrap(head, fh, txw, True), wrap(big, fb, txw, True) if big else [],
             wrap(_p18_clean(line) + (u" " + c_ if c_ else u""), ft, txw))
        hh = pad * 2 + len(L[0]) * fh * 1.25 + len(L[1]) * fb * 1.18 + len(L[2]) * ft * 1.28 + (fh * 0.3 if L[1] else 0)
        lay.append((kind, L, max(hh, ic + 2 * pad)))
    yy = y
    for r0 in range(0, len(lay), cols):
        row = lay[r0:r0 + cols]
        rh = max(t[2] for t in row)
        for c_, (kind, L, _) in enumerate(row):
            tx = x + c_ * (tw + g)
            pg.poly([rect(tx, yy - rh, tx + tw, yy)], fill=C["paper"], stroke=C["faint"], lw=0.2)
            _p18_icon(pg, P18_TILE_ICONS.get(kind, ("water",)), tx + pad, yy - pad, ic)
            lx, ly = tx + 2 * pad + ic, yy - pad
            for ln in L[0]:
                ly -= fh * 1.25
                pg.text(ln, lx, ly, fh, C["dark"], bold=True)
            if L[1]:
                ly -= fh * 0.3
            for ln in L[1]:
                ly -= fb * 1.18
                pg.text(ln, lx, ly, fb, C["d3"], bold=True)
            for ln in L[2]:
                ly -= ft * 1.28
                pg.text(ln, lx, ly, ft, C["ink"])
        yy -= rh + g
    return yy + g


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
              u"plan 2018 (official); " + WD))], w - 20.0, 4.0 * s, 2.6 * s, C["acc"]) - 2.8 * s * 0.8
    # v6.1: "ratio calculated" taken out of the source above (no status words)
    return _p18_tiles(pg, x + 10.0, yy, w - 20.0, GOES_T, s, 2)


def draw_decision(pg, x, y, w, h, s):
    """v1.12 (Aras 26 Oct 07:06 and his sketch): the seven steps clockwise round a rectangle, 1-4 along the top, 5-7
    back along the bottom; the closing arrow (7 -> 1) in red says what really closes the loop: the next winter's
    stream, never a pump (the water runs one way). Returns the lowest y drawn."""
    steps = [(_p18_clean(t), _p18_clean(src)) for t, src in DECISION]
    n = len(steps)
    top_n = (n + 1) // 2
    gap, vg = 16.0 * s, 24.0 * s
    bw = (w - (top_n - 1) * gap) / top_n
    bh = 0.0
    for t, src in steps:                             # one height for every box: the tallest content
        bh = max(bh, 9.0 * s + len(wrap(t, 3.2 * s, bw - 8.0, True)) * 3.2 * s * 1.28 +
                 len(wrap(src, 2.5 * s, bw - 8.0)) * 2.5 * s * 1.28 + 3.0)
    yt = y                                           # top row: its boxes' top edge
    yb = y - bh - vg                                 # bottom row
    bot_x = [x + w - bw - (w - bw) * j / (n - top_n - 1) for j in range(n - top_n)] if n - top_n > 1 else [x]
    pos = [(x + i * (bw + gap), yt) for i in range(top_n)] + [(bot_x[j], yb) for j in range(n - top_n)]
    for i, (t, src) in enumerate(steps):
        bx, by = pos[i]
        pg.poly([rect(bx, by - bh, bx + bw, by)], fill=C["white"], stroke=C["d2"], lw=0.4)
        sz = 5.6 * s                                 # the step marker (icons.py ico_step), its number written in it
        sh, (ax, ay), th, cap = ico_step(bx + 3.0 + sz / 2.0, by - 1.6 - sz / 2.0, sz, "solid")
        _p18_put(pg, sh)
        pg.text(str(i + 1), ax, ay - cap / 2.0, cap / CAP, th, bold=True, align="C")
        nm, crossed = P18_DEC_ICONS[i] if i < len(P18_DEC_ICONS) else ("water", False)
        _p18_icon(pg, (nm,), bx + bw - 3.0 - 7.0 * s, by - 1.5, 7.0 * s, crossed)
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


def _p18_fig(pg, pose, x, y, k, colour, facing=1, h_m=1.70, **params):
    """ONE place for p.18's people: the figure library (common/figures.py fig_side), feet at (x, y), k mm per m,
    in one ink; params go to the drawn pose (olive: branch_h)"""
    _p18_put(pg, fig_side(pose, x, y, k, facing, ink=colour, mm_per_m=k, h_m=h_m, **params))


def _p18_olive_spots(shapes, crown_cols):
    """the tree centres pla_crop_plan drew (the centroids of its olive crowns, merged within 1 m), so the standing
    trees sit exactly on the plan's rows"""
    pts = []
    for sh in shapes:
        if sh[0] == "poly" and sh[2] in crown_cols and len(sh[1]) > 2:
            cx = sum(p[0] for p in sh[1]) / float(len(sh[1]))
            cy = sum(p[1] for p in sh[1]) / float(len(sh[1]))
            if all(math.hypot(cx - a, cy - b) > 1.0 for a, b in pts):
                pts.append((cx, cy))
    return pts


def _p18_gap(vals):
    q = sorted(set(round(v * 2.0) / 2.0 for v in vals))
    return min([q[i + 1] - q[i] for i in range(len(q) - 1)] or [0.0])


def draw_farm_picto(opt):
    """p.18 farm block (02 §4): the existing olive grove off the site as an axonometric in true proportion. The field,
    its rows and the crowns come from plants.py pla_crop_plan at the published olive spacing (5 m in the row, 7 m
    between rows); the crowns lie on the ground as their midday shade and every tree stands on its spot as its plants.py
    section silhouette at true size; a drip line runs along every row from a header fed by the clean stream water; one
    person picks at true height. A diagram (no scale bar): place() fits it to the panel."""
    pg = Page(0, 0)
    k = 1.2
    V = BoxView(PSI, 0.0, k, 0.0, 0.0)
    nr, nt = P18_BLOCK
    a, b = nt * P18_OLIVE_TREE_M, nr * P18_OLIVE_ROW_M
    sides = [((0, -1), (0, 0), (1, 0)), ((1, 0), (1, 0), (1, 1)), ((0, 1), (1, 1), (0, 1)), ((-1, 0), (0, 1), (0, 0))]
    for (nu, nv), (i0, j0), (i1, j1) in sides:
        vis, lit = V.visible(nu, nv)
        if vis:
            pg.poly([[V(i0 * a, j0 * b, 0), V(i1 * a, j1 * b, 0), V(i1 * a, j1 * b, -P18_SOIL_M),
                      V(i0 * a, j0 * b, -P18_SOIL_M)]], fill=COL["soil"] if lit else COL["soil_dk"],
                    stroke=COL["edge3d"], lw=0.15)
    pg.poly([[V(0, 0, 0), V(a, 0, 0), V(a, b, 0), V(0, b, 0)]], fill=MP["agriculture"][0], stroke=COL["edge3d"], lw=0.15)
    # the field from plants.py, in metres (k = 1), laid on the axonometric ground
    plan = pla_crop_plan("olive", [(0.0, 0.0), (a, 0.0), (a, b), (0.0, b)], 1.0, row_spacing=P18_OLIVE_ROW_M,
                         plant_spacing=P18_OLIVE_TREE_M)
    sp = PLA_SPECIES["olive"]
    crown = set(v for kk, v in sp["colours"].items() if kk != "stem" and isinstance(v, str) and v)
    spots = _p18_olive_spots(plan, crown)
    if len(spots) < 4:                               # fallback: the same grid, half a spacing in from the edges
        spots = [((j + 0.5) * P18_OLIVE_TREE_M, (i + 0.5) * P18_OLIVE_ROW_M) for i in range(nr) for j in range(nt)]
    for sh in plan:
        pts = [V(p[0], p[1], 0.0) for p in sh[1]]
        if sh[0] != "poly":
            pg.line(pts, sh[2], sh[3])
        elif sh[2] in crown:                         # the crown's footprint = its midday shade on the ground
            pg.poly([pts], fill=COL["shade"], stroke=None, alpha=0.6)
        else:
            pg.poly([pts], fill=sh[2], stroke=sh[3], lw=sh[4])
    # drip: one line along every row, from a header on the edge where the clean stream water arrives
    along_u = _p18_gap([p[1] for p in spots]) >= _p18_gap([p[0] for p in spots])
    rows = sorted(set(round((p[1] if along_u else p[0]) * 2.0) / 2.0 for p in spots))
    for r_ in rows:
        ln = [V(0.0, r_, 0.0), V(a, r_, 0.0)] if along_u else [V(r_, 0.0, 0.0), V(r_, b, 0.0)]
        pg.line(ln, C["w3"], 0.25)
    head = [V(0.0, 0.0, 0.0), V(0.0, b, 0.0)] if along_u else [V(0.0, 0.0, 0.0), V(a, 0.0, 0.0)]
    pg.line(head, C["d3"], 0.5)
    mid = (0.0, b / 2.0) if along_u else (a / 2.0, 0.0)
    tail = (mid[0] - 14.0, mid[1]) if along_u else (mid[0], mid[1] - 14.0)
    arrow(pg, [V(tail[0], tail[1], 0.0), V(mid[0], mid[1], 0.0)], C["d2"], 0.6, 2.2)
    tx, ty = V(tail[0], tail[1], 0.0)
    pg.text(u"clean stream water", tx, ty + 1.6, FS_MIN, C["d3"], bold=True, align="C")
    # the trees standing, and one person picking, drawn back to front
    kz = k * math.cos(math.radians(PHI))             # vertical metres on this axonometric
    items = [(V(u, v, 0.0), "t", i) for i, (u, v) in enumerate(spots)]
    fu, fv = min(spots, key=lambda p: V(p[0], p[1], 0.0)[1])
    fp = V(fu + (1.4 if along_u else 0.0), fv + (0.0 if along_u else 1.4), 0.0)
    items.append((fp, "f", -1 if fp[0] > V(fu, fv, 0.0)[0] else 1))
    for (px, py), kind, i in sorted(items, key=lambda t: -t[0][1]):
        if kind == "t":
            _p18_put(pg, pla_section("olive", px, py, k, h_m=sp["h_m"] * math.cos(math.radians(PHI)),
                                     crown_m=sp["crown_m"], seed=i))
        else:
            _p18_fig(pg, "olive", px, py, kz, C["dark"], facing=i, branch_h=P18_BRANCH_M)
    bb = items_bbox(pg.items)
    node(pg, bb[0] + 3.0, bb[3] + 8.0, 11, opt, 2.6)
    pg.text(u"EXISTING FARMLAND, OFF SITE", bb[0] + 7.0, bb[3] + 7.2, FS_MIN, COL["ink"], bold=True)
    pg.text(u"olives {:.0f} x {:.0f} cm · drip along every row".format(P18_OLIVE_TREE_M * 100, P18_OLIVE_ROW_M * 100),
            bb[0] + 7.0, bb[3] + 7.2 - FS_MIN * 1.35, FS_MIN, COL["ink"])
    return pg
