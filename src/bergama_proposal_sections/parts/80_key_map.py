# ================================================================ v9 key map: where the four sections are cut (F4, G8)
# v9 (MIRAQUA 28 Oct, F4; P8 fault table F row 4): the page had no key map, and the K4 and K5 cuts lie downstream of
# the bridges their sketches draw behind them. The key map shows the four surveyed cuts (centres as the masterplan's
# parts/02b_detail.py CUT_AT), the two bridges (site board data/DIAG_SRC.py BRIDGES_K), the Selinos (agriculture
# data/GEO.py "selinos", survey m) and the study area (calisma_alan of Bergama_Altlik.3dm, the recorded copy the site
# board keeps as R28_STUDY_COPY) in R28_STUDY_LINE, named in the booklet legend by R28_STUDY_NAME (G8). A key map, so no
# scale bar (SCRIPT_STANDARD §8); the frame axis horizontal, upstream on the left (G7), a north arrow. It sits in the
# free band under the upstream sketch: inside ps_all, outside the single crops. The note's distances are measured
# here, every press (K4 cut 114.1 m and K5 cut 119.4 m from the bridges, both downstream along the stream line).
PS_KEY_CUTS = [("up", u"1 · UPSTREAM ENTRY", (29693.022, 32569.176)),
               ("k4", u"2 · K4 CUT", (29959.774, 32264.566)),
               ("k5", u"3 · K5 CUT", (30354.663, 31689.671)),
               ("down", u"4 · DOWNSTREAM REACH", (30991.856, 31039.404))]
PS_KEY_BRIDGES = [("k4", u"K4 bridge", (29846.40, 32277.71)),
                  ("k5", u"K5 bridge (Üç Kemer)", (30293.63, 31792.25))]
PS_KEY_STUDY = [
    [(29696.903, 32800.562), (29872.423, 32572.84), (29880.693, 32496.334), (29818.865, 32475.301), (29825.821, 32398.074),
     (29923.185, 32344.348), (29904.985, 32311.252), (29997.056, 32290.092), (30053.417, 32139.667), (30004.049, 32108.006),
     (29954.803, 32210.611), (29792.114, 32247.062), (29761.684, 32302.735), (29754.016, 32451.383), (29678.437, 32447.696),
     (29632.398, 32496.591), (29665.339, 32526.253), (29612.859, 32696.506), (29600.496, 32719.394)],
    [(30178.18, 31923.887), (30138.072, 31887.655), (30257.694, 31773.217), (30389.686, 31405.252), (30701.152, 30991.252),
     (30840.053, 31053.865), (31044.852, 30781.877), (31014.2, 30757.409), (31373.442, 30493.066), (31453.175, 30560.194),
     (31332.978, 30864.179), (31012.679, 31323.349), (30737.856, 31286.66), (30712.87, 31331.891), (30556.09, 31450.103),
     (30454.629, 31577.301), (30434.156, 31607.332), (30313.613, 31812.92)],
]
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
PS_KEY_PANEL = "up"                   # the panel whose free band under its sketch holds the key map
PS_KEY_GAP = 8.0                      # mm (sheet) between a single crop's bottom and the key map
PS_KEY_MIN_H = 60.0                   # mm (sheet): with less room there, the panel with the most room takes it (logged)
PS_KEY_PRINT = dict(cut=(6.0, 0.9), bridge=(3.2, 0.6), river=0.8, leader=0.15, arrow=4.0, pad=2.0)   # booklet print mm


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


def ps_key_note():
    """The key map's note, measured: how far (m, straight) and which way along the stream each of the K4 and K5 cuts
    lies from the bridge its sketch draws. Returns (text with **bold** runs, {key: m})."""
    at = dict((k, p) for k, _, p in PS_KEY_CUTS)
    bits, dist, ways = [], {}, set()
    for k, nm, b in PS_KEY_BRIDGES:
        c = at[k]
        dist[k] = math.hypot(c[0] - b[0], c[1] - b[1])
        way = u"downstream" if ps_key_chain(c)[0] > ps_key_chain(b)[0] else u"upstream"
        ways.add(way)
        bits.append(u"**%s cut**%s about %.0f m %s of the %s" % (k.upper(), u"" if bits else u" lies", dist[k], way, nm))
    if len(ways) == 1:                                         # today: both downstream (one short line)
        return (u"The **K4 cut** lies about %.0f m and the **K5 cut** about %.0f m %s of the bridges their sketches draw "
                u"behind them" % (dist["k4"], dist["k5"], ways.pop()), dist)
    return u"The " + u", the ".join(bits) + u": the sketches draw these bridges behind the cut", dist


def ps_key_map(pg, boxes, low, log):
    """v9 (F4): the key map in the free band under a sketch (boxes: the panels' drawing boxes; low: each sketch's
    bottom, mm on the sheet), under PS_KEY_PANEL unless it has less than PS_KEY_MIN_H there. Returns its box."""
    room = dict((k, low[k] - 3.0 - PS_KEY_GAP - boxes[k][1]) for k in low)
    key = PS_KEY_PANEL
    if room.get(key, 0.0) < PS_KEY_MIN_H:
        key = max(room, key=lambda k_: room[k_])
        log.append(u"NOTE key map: {:.0f} mm free under the {} sketch, so it sits under the {} sketch ({:.0f} mm)".format(
            room.get(PS_KEY_PANEL, 0.0), PS_KEY_PANEL, key, room[key]))
    bx = boxes[key]
    return draw_key_map(pg, (bx[0], bx[1], bx[2], bx[1] + room[key]), key, log)


def draw_key_map(pg, area, where, log):
    """v9 (F4, G4, G5, G8): the key map hung from the top of area (x0, y0, x1, y1), mm on the sheet: a frame, the
    title row with the north arrow, the map (study area, Selinos, bridges, the four cuts; labels kept apart by
    place_labels_all), the measured note. Print sizes (booklet mm, pt) are turned into sheet mm by 1 / BK_S."""
    x0, y0, x1, y1 = area
    P = dict((k, (tuple(v_ / BK_S for v_ in v) if isinstance(v, tuple) else v / BK_S)) for k, v in PS_KEY_PRINT.items())
    pad, ts, ls = P["pad"], pt_mm(7.5), pt_mm(LBL_PT)
    note, dist = ps_key_note()
    nlines = ps_rich_lines(note, ls, x1 - x0 - 2 * pad)
    note_n = len(nlines)
    title_h, note_h = ts * 1.3, ls * 1.28 * note_n
    polys = [[ps_key_turn(p) for p in R] for R in PS_KEY_STUDY]
    river = [ps_key_turn(p) for p in PS_KEY_SELINOS]
    ext = [p for R in polys for p in R] + river
    ex0, ey0 = min(p[0] for p in ext), min(p[1] for p in ext)
    ex1, ey1 = max(p[0] for p in ext), max(p[1] for p in ext)
    k = min((x1 - x0 - 2 * pad) / (ex1 - ex0), (y1 - y0 - 4 * pad - title_h - note_h) / (ey1 - ey0))
    if k <= 0:
        log.append(u"NOTE key map: no room under the {} sketch, left out".format(where))
        return None
    w, h = (ex1 - ex0) * k, (ey1 - ey0) * k
    ox, oy = x0 + pad, y1 - 2 * pad - title_h - h              # the map's lower left

    def T(q):                                                  # turned m -> sheet mm
        return (ox + (q[0] - ex0) * k, oy + (q[1] - ey0) * k)
    title = u"**KEY MAP** · where the four sections are cut, upstream to downstream"
    tw = text_w(title.replace(u"**", u""), ts, True)
    nw = max(text_w(u" ".join(t for t, _, _ in ln), ls, True) for ln in nlines)
    fx1 = min(x1, x0 + 2 * pad + max(w, tw + 3.0 * P["arrow"], nw))
    yn0 = oy - pad - ls * CAP                                  # the note's first baseline
    fy0 = max(y0, yn0 - (note_n - 1) * ls * 1.28 - 0.25 * ls - pad)
    pg.poly([rect(x0, fy0, fx1, y1)], fill=COL["white"], stroke=COL["faint"], lw=0.25)
    # title row (G5: the keyword bold) and the north arrow at its right end
    ps_rich_para(pg, x0 + pad, y1 - pad - ts * CAP + ts * 1.28, fx1 - x0, title, ts, COL["ink_dark"])
    nx, ny = ps_key_turn((0.0, 1.0))
    cx, cy = fx1 - pad - P["arrow"], y1 - pad - title_h / 2.0
    tail = (cx - nx * P["arrow"] / 2.0, cy - ny * P["arrow"] / 2.0)
    tip = (cx + nx * P["arrow"] / 2.0, cy + ny * P["arrow"] / 2.0)
    hd = 0.3 * P["arrow"]
    pg.line([tail, tip], COL["ink"], P["leader"] * 2.0)
    pg.poly([[tip, (tip[0] - nx * hd - ny * hd * 0.45, tip[1] - ny * hd + nx * hd * 0.45),
              (tip[0] - nx * hd + ny * hd * 0.45, tip[1] - ny * hd - nx * hd * 0.45)]], fill=COL["ink"])
    pg.text(u"N", tip[0] - 0.6 * ls, tip[1] - ls * CAP / 2.0, ls, COL["ink"], bold=True, align="R")
    # the map: study area (light ground + R28_STUDY_LINE), the Selinos, then the bridges and the cuts across it
    st = R28_STUDY_LINE
    for R in polys:
        pg.poly([[T(q) for q in R]], fill=COL["paper"])
    river_s = [T(q) for q in river]
    pg.line(river_s, COL["river"], P["river"])
    rings = [[T(q) for q in R] + [T(R[0])] for R in polys]
    for r_ in rings:
        pg.line(r_, st["colour"], st["width_mm"] / BK_S, dash=[d / BK_S for d in st["dash_mm"]], cap=0)
    taken, items, anchors = [], [], []

    def bar(p, L, lw, col):                                    # a short bar across the stream at survey point p
        _, (dx, dy) = ps_key_chain(p)
        tx, ty = ps_key_turn((dx, dy))
        c = T(ps_key_turn(p))
        a_, b_ = (c[0] - ty * L / 2.0, c[1] + tx * L / 2.0), (c[0] + ty * L / 2.0, c[1] - tx * L / 2.0)
        pg.line([a_, b_], col, lw, cap=0)
        taken.append((min(a_[0], b_[0]) - lw, min(a_[1], b_[1]) - lw, max(a_[0], b_[0]) + lw, max(a_[1], b_[1]) + lw))
        return c
    for key_, nm, p in PS_KEY_BRIDGES:
        c = bar(p, P["bridge"][0], P["bridge"][1], COL["ink"])
        items.append(dict(x=c[0], y=c[1], rank=0, wh=lambda f, s_=nm: (text_w(s_, ls * f), ls * f * (CAP + 0.25))))
        anchors.append((c, nm, False))
    for key_, nm, p in PS_KEY_CUTS:
        c = bar(p, P["cut"][0], P["cut"][1], COL["accent"])
        items.append(dict(x=c[0], y=c[1], rank=0, wh=lambda f, s_=nm: (text_w(s_, ls * f, True), ls * f * (CAP + 0.25))))
        anchors.append((c, nm, True))
    c = river_s[int(len(river_s) * 0.8)]                       # the stream's name, between cuts 3 and 4 (may drop)
    items.append(dict(x=c[0], y=c[1], rank=1, wh=lambda f: (text_w(u"Selinos", ls * f), ls * f * (CAP + 0.25))))
    anchors.append((c, u"Selinos", None))
    segs = list(zip(river_s[:-1], river_s[1:])) + [s_ for r_ in rings for s_ in zip(r_[:-1], r_[1:])]
    bounds = (x0 + 0.5 * pad, oy - 0.5 * pad, fx1 - 0.5 * pad, oy + h + 0.5 * pad)
    got = place_labels_all(items, taken, bounds, segs, sizes=(1.0,), pad=0.6 / BK_S)
    for i, (c, s_, bold) in enumerate(anchors):
        if i not in got:
            log.append(u"NOTE key map: label '{}' left out (no free place)".format(s_))
            continue
        b, leader, _ = got[i]
        if leader:
            pg.line([c, lp_leader_end(b, c)], COL["ink2"], P["leader"])
        col = COL["river_mid"] if bold is None else (COL["ink_dark"] if bold else COL["ink2"])
        pg.text(s_, b[0], b[1] + 0.25 * ls, ls, col, bold=bool(bold), halo=COL["white"])
    # the measured note (G5: the two cuts bold)
    ps_rich_para(pg, x0 + pad, yn0 + ls * 1.28, fx1 - x0 - 2 * pad, note, ls, COL["ink"])
    log.append(u"key map (F4): under the {} sketch, {:.0f} x {:.0f} mm on the sheet; K4 cut {:.1f} m and K5 cut {:.1f} m "
               u"from the bridges the sketches draw".format(where, fx1 - x0, y1 - fy0, dist["k4"], dist["k5"]))
    return (x0, fy0, fx1, y1)
