# p.17 the planting panel (split from code.py on 29 Oct 2026; moved unchanged)


def s4_days(E):
    """S4's days a year at or above each height (the detail section's DAYS_WET, this cut's own): [(m, days, under)],
    and the days the bed is dry."""
    import re as _re
    t = E["DAYS_WET"]
    rows = [(float(h), int(n), bool(u)) for h, u, n in _re.findall(r"(\d+\.\d+) m (under )?(\d+) d", t)]
    m = _re.search(r"about (\d+) d", t)
    return rows, (int(m.group(1)) if m else None)


def prect(pg, x, y, w, h, fill=None, stroke=None, lw=0.1):
    pg.poly([rect(x, y, x + w, y + h)], fill=fill, stroke=stroke, lw=lw)


def s4_classes(E):
    """The S4 ground split by how many days a year the water reaches it (the cut's own figures): [(h_lo, h_hi, days
    lo, days hi, label)] by height above the bed low point; the last two: up to Q500, above it."""
    rows, _dry = s4_days(E)
    bed, q500 = E["THALWEG"][1], E["Q500"]
    out, prev_h, prev_d = [], 0.0, 365.0
    for h, n, under in rows:
        lo = 0.0 if under else float(n)
        out.append((prev_h, h, lo if not under else 0.0, prev_d,
                    (u"> {} d".format(n) if not out else (u"{}-{} d".format(n, int(prev_d)) if not under else
                                                         u"< {} d".format(int(prev_d))))))
        prev_h, prev_d = h, (float(n) if not under else 1.0)
    out.append((prev_h, q500 - bed, 0.0, 1.0, u"< 1 d"))
    out.append((q500 - bed, 99.0, 0.0, 0.0, u"above Q500"))
    return out


def _bands_bar(S, xa, xb, y, h, colour):
    """A bar of the day strip or a band, filled by hand (a light wobble only: the bars are read against each other)."""
    r = S["hand_ring"]([(xa, y), (xb, y), (xb, y + h), (xa, y + h)], "bars", 0.08)
    S["fill"]((0.0, 0.0), r, "bars", S["hx"](colour), alpha=0.95, boundary=False, hand_=False)


def _bands_shrub(S, x, y, h, w):
    """Hand-drawn shrub (page mm): a dome h tall, w wide on the ground at (x, y), washes and a loose outline."""
    o = (0.0, 0.0)
    dome = [(x + w / 2.0 * math.cos(math.pi * i / 14.0), y + h * math.sin(math.pi * i / 14.0) ** 0.7) for i in range(15)]
    S["wash"](o, dome, "planting", S["SITE_TREE"][1], 0.6, z=S["Z_TREE"])
    S["wash"](o, [(x - w * 0.12 + (px - x) * 0.5, y + (py - y) * 0.55 + h * 0.3) for px, py in dome], "planting",
              S["SITE_TREE"][0], 0.5, z=S["Z_TREE"])
    S["sketch"](o, dome, "planting", S["SITE_TREE"][2], S["LW_FINE"], closed=True, over=0.0, amp=0.12, retrace=False,
                z=S["Z_TREE"])


def _bands_tufts(S, x0, x1, gy, h):
    """Meadow tufts h tall (page mm) from x0 to x1, gy(x) = ground y: three short hand strokes each."""
    o, x, i = (0.0, 0.0), x0, 0
    while x <= x1:
        g = gy(x)
        hh = h * (0.7 + 0.3 * ((i * 3) % 4) / 3.0)
        for d in (-0.4, 0.0, 0.4):
            S["sketch"](o, [(x, g), (x + d * hh * 0.6, g + hh * (1.0 - abs(d) * 0.4))], "planting", S["REED"],
                        S["LW_FINE"], over=0.0, amp=0.03, retrace=False, z=S["Z_TREE"])
        x += 1.25
        i += 1


def _bands_lavender(S, x0, x1, gy, k, h=0.5):
    """Lavender mounds about h tall (m) with flower spikes, 0.8 m apart (as sec_lavender), drawn by hand."""
    o, w = (0.0, 0.0), 0.8 * k
    x = x0 + w / 2.0
    while x <= x1 - w / 2.0 + 1e-6:
        g = gy(x)
        mound = [(x + w / 2.0 * math.cos(math.pi * i / 10.0), g + h * k * math.sin(math.pi * i / 10.0)) for i in range(11)]
        S["wash"](o, mound, "planting", S["hx"](SEC["olive"]), 0.6, z=S["Z_TREE"])
        for d in (-0.25, 0.0, 0.25):
            S["sketch"](o, [(x + d * w, g + h * k * 0.8), (x + d * w * 1.3, g + h * k * 1.4)], "planting",
                        S["hx"](SEC["lav"]), 0.3, over=0.0, amp=0.02, retrace=False, z=S["Z_TREE"])
        x += w


def _bands_chip(pg, code, x, y, fs):
    """A band's letter in its colour (x: remove), top-left at (x, y); returns its width."""
    w, h = fs * 1.7, fs * 1.3
    if code in BAND_COL:
        prect(pg, x, y - h, w, h, fill=BAND_COL[code])
        pg.text(code, x + w / 2.0, y - h + fs * 0.32, fs, "FFFFFF", bold=True, align="C")
    else:
        prect(pg, x, y - h, w, h, stroke=C_PL["accent"], lw=0.2)
        pg.text(u"x", x + w / 2.0, y - h + fs * 0.3, fs, C_PL["accent"], bold=True, align="C")
    return w


def draw_bands(opt, den=None):
    """W3b v1.12 (Aras 26 Oct: one drawing, the hand-sketched language of the upstream entry, p.23): the planting
    bands A-F on the surveyed S4 ground, where the water reaches it for that many days a year (this cut's own
    figures), drawn by the sketch engine; under it the day classes and the letters of the bands that fit each, and the
    bands' key (v1.14: the species are the photo cards of the plants panel)."""
    E = detail_engine()
    S = sketch_engine()
    del S["ZP"][:]
    S["ORDER"][0] = 0
    S["HAND"][0] = False
    o = (0.0, 0.0)
    prof = s4_profile(E)
    bed, q100, q500 = E["THALWEG"][1], E["Q100"], E["Q500"]
    den = den or BANDS_DENS[0]
    k = 1000.0 / den
    fs, fh = BANDS_FS, BANDS_HEAD
    s0, s1 = BANDS_S
    zb = bed - 1.0
    pg = Page(0, 0)

    def P(s, z):
        return ((s - s0) * k, (z - zb) * k)

    def gz(s):
        return E["prof_z"](prof, s)

    def gy_x(x):
        return P(0, gz(s0 + x / k))[1]

    def flush():
        pg.items += [it for _, _, it in sorted(S["ZP"], key=lambda e: (e[0], e[1]))]
        del S["ZP"][:]
    ss = [s0 + 0.25 * i for i in range(int((s1 - s0) / 0.25) + 1)]
    cls = s4_classes(E)

    def cl(s):
        h = gz(s) - bed
        return next(i for i, c in enumerate(cls) if h < c[1] or i == len(cls) - 1)
    runs = []
    for s in ss:
        c = cl(s)
        if runs and runs[-1][0] == c:
            runs[-1][2] = s
        else:
            runs.append([c, s, s])
    W = P(s1, 0)[0]
    # ground: the engine's poché and earth strokes on the survey every 1 m (the hand line), the day classes as a
    # marker band under the surface, the base flow (bed to the 0.10 m line) and the faint Q500 reach
    surf = [P(s0 + i, gz(s0 + i)) for i in range(int(s1 - s0) + 1)]
    gs = S["sketch_ground"](o, [(0.0, 0.0)] + surf + [(W, 0.0)], "ground")
    for c, a, b in runs:
        for pc in S["band"](gs, P(a, 0)[0], min(W, P(b + 0.25, 0)[0]), 2.4):
            S["wash"](o, pc, "days", S["hx"](DAYS_COL[c]), 0.9)
    yq5 = P(0, q500)[1]
    pc = S["under_level"](gs, 0.0, W, yq5)
    if pc:
        S["wash"](o, pc, "flood", S["FLOOD_WASH"], 0.12)
    S["water_level"](o, gs, P(E["THALWEG"][0], 0)[0], P(0, bed + cls[0][1])[1], S["W_WIN"], bed_hatch=True)
    # plants: each day class gets the band(s) whose days overlap it most (B reeds, C shrubs, D meadow, E trees, F
    # lavender), at the design's sizes on S4 (reeds 2.2 m, Tamarix / Vitex shrubs 1.9 m, plane 7.5 m)
    rd = max(r[2] for r in E["SECTIONS"][0]["reeds"]) * k
    sh_ = E["SECTIONS"][0]["shrubs"][3]
    tr = E["SECTIONS"][0]["trees"][0]
    tag = {}                                                  # band -> (x, top y) of its first plant, for its label
    for c, a, b in runs:
        xa, xb = P(a, 0)[0], P(b, 0)[0]
        if c in (0, 1) and xb - xa > 1.5:
            n = max(1, int((xb - xa - 1.2) / 4.8))
            for j in range(n):
                x0_ = xa + 0.6 + (xb - xa - 1.2) * j / n
                x1_ = xa + 0.6 + (xb - xa - 1.2) * (j + 1) / n
                S["reeds"](o, x0_, x1_, gy_x((x0_ + x1_) / 2.0) - 0.2, rd)
            if c == 0:
                tag.setdefault("B", ((xa + xb) / 2.0, gy_x((xa + xb) / 2.0) + rd))
        if c in (1, 2) and xb - xa > 6.0:
            for f in (0.3, 0.75):
                x_ = P(a + (b - a) * f, 0)[0]
                _bands_shrub(S, x_, gy_x(x_) - 0.2, sh_[1] * k, sh_[2] * k)
                tag.setdefault("C", (x_, gy_x(x_) + sh_[1] * k))
        if c == 2 and xb - xa > 2.0:
            _bands_tufts(S, xa + 0.4, xb - 0.4, gy_x, 0.35 * k)
            if xa > P(E["THALWEG"][0], 0)[0]:                 # the north-east meadow, clear of the reeds
                tag.setdefault("D", ((xa + xb) / 2.0, gy_x((xa + xb) / 2.0) + sh_[1] * k))
        if c == 3 and b - a >= 2.0:
            x_ = P((a + b) / 2.0, 0)[0]
            S["sketch_tree"](o, x_, gy_x(x_) - 0.2, tr[2] * k)
            tag.setdefault("E", (x_, gy_x(x_) + tr[2] * k * 0.96))
        if c == 4 and xb - xa > 4.0:
            _bands_lavender(S, xa + 1.0, min(xb - 1.0, xa + 6.0 * k), gy_x, k)
            tag.setdefault("F", (xa + 3.0 * k, gy_x(xa + 3.0 * k) + 0.6 * k))
    x_ = P(s0 + 2.0, 0)[0]
    S["sketch_person"](o, x_, gy_x(x_), 1.75 * k)                # scale figure on the south-west bank, above Q500
    S["sketch"](o, gs, "ground lines", S["SKINK"], S["PEN_BOLD"], z=S["Z_LINE"])   # the cut: the gesture
    flush()
    # level lines where the water stands over the ground: the day heights, Q100, Q500 (hand lines, dashed); their
    # figures in a ladder at the right
    lv = []
    for i, (hl, hh, dlo, dhi, lab) in enumerate(cls[:-2]):
        lv.append((bed + hh, u"{:.2f} m · {}".format(hh, (u"{} d".format(int(dlo)) if dlo else u"< 1 d")),
                   C["w3"], [0.6, 0.5], 0.2))
    lv += [(q100, u"Q100 · {:.2f} m".format(q100 - bed), "1B535E", [1.6, 0.6], 0.3),
           (q500, u"Q500 · {:.2f} m".format(q500 - bed), "1B535E", [2.4, 0.8], 0.3)]
    xr = W + 1.0
    ent = []
    for z, t, colr, dash, lw in lv:
        run = [s for s in ss if gz(s) < z]
        if run:
            a_, b_ = P(run[0], z), P(run[-1], z)
            pg.line(S["hand"]([a_, b_], 0.1, S["HAND_WAV"], S["_seed"](a_[0], z)), colr, lw, dash=dash)
            if b_[0] < xr - 0.5:
                pg.line([b_, (xr, b_[1])], colr, 0.08, dash=[0.3, 0.6])
            if z in (q100, q500):
                xm = P(s0 + (19.0 if z == q100 else 22.5), 0)[0]
                mk = [(xm - 1.0, b_[1] + 1.7), (xm + 1.0, b_[1] + 1.7), (xm, b_[1]), (xm - 1.0, b_[1] + 1.7)]
                pg.line(mk, colr, 0.15)
        ent.append((P(0, z)[1], t, colr, z in (q100, q500)))
    level_ladder(pg, ent, xr, xr + 5.0, fs, lo=P(0, bed)[1] - 1.0)
    # labels in the sky: the band each plant stands for, the two banks, the idea
    # v3 (Aras 27 Oct 17:34): plant names "English (Turkish)", one a line, stacked up from over the plant
    names = {"B": [plant_name("reed"), plant_name("iris")], "C": [plant_name("tamarisk"), plant_name("chaste")],
             "D": [u"meadow"], "E": [plant_name("plane")], "F": [plant_name("lavender")]}
    taken = []                                                # v3.2: the labels set so far (x0, y0, x1, y1)
    for code in sorted(tag, key=lambda c_: tag[c_][0]):       # v3.2: left to right (was A-F)
        x_, top = tag[code]
        y_ = max(top, yq5) + 2.6
        lines = names[code]
        cw_ = fs * 1.7 + 0.8 + max(text_w(t_, fs) for t_ in lines)
        x_ = min(max(x_ - cw_ / 2.0, 0.0), W - cw_)
        yt = y_ + (len(lines) - 1) * fs * 1.25
        # v3.2 (Aras 27 Oct, Prompt 8: labels overlapping): the labels under the Q500 line share one baseline, and
        # "French lavender (Karabaş otu)" ran into the tamarisk / chaste tree label; a label that would lie on one
        # set before it moves right, clear of it (same row, same words; the drawing's size is unchanged)
        for b_ in taken:
            if x_ < b_[2] + 1.5 and b_[0] < x_ + cw_ and y_ - fs * 0.3 < b_[3] and b_[1] < yt + fs * 1.05:
                x_ = b_[2] + 1.5
        x_ = min(x_, W - cw_)
        taken.append((x_, y_ - fs * 0.3, x_ + cw_, yt + fs * 1.05))
        _bands_chip(pg, code, x_, yt + fs * 1.05, fs)
        for i_, t_ in enumerate(lines):
            pg.text(t_, x_ + fs * 1.7 + 0.8, yt - i_ * fs * 1.25, fs, C_PL["ink"])
    ytop = P(0, gz(s0))[1] + 1.75 * k + 3.0
    pg.text(u"south-west bank", 0.0, ytop, fs, COL["ink2"])
    pg.text(u"north-east bank · road", W, P(0, gz(s1))[1] + 3.0 * k, fs, COL["ink2"], align="R")
    pg.text(u"the bands follow the days under water", 0.0, ytop + fh * 2.2, fh, "1E1E1E", bold=True)
    # under the cut: the day classes along the ground (one strip), then the letters of the bands whose days fit each
    # class, under it (v1.14: was one bar per band and the species list)
    y = -fs * 1.8
    pg.text(u"days a year under water on S4 " + cite(E["DAYS_WET"]), 0.0, y, fs, COL["ink2"])
    y -= 1.6 + 3.2
    for c, a, b in runs:
        xa, xb = P(a, 0)[0], P(min(s1, b + 0.25), 0)[0]
        _bands_bar(S, xa, xb, y, 3.2, DAYS_COL[c])
    flush()
    widest = {}
    for c, a, b in runs:
        xa, xb = P(a, 0)[0], P(min(s1, b + 0.25), 0)[0]
        if c not in widest or xb - xa > widest[c][1] - widest[c][0]:
            widest[c] = (xa, xb)
    yl = y - fs * 1.3
    for c, (xa, xb) in widest.items():
        codes = []
        for code, name, eco, days, depth, zone in PLANT_BANDS:
            lo_, hi_ = cls[c][2], cls[c][3]
            if code == "A":
                ok = c == 0
            elif code == "F":
                ok = c >= len(cls) - 2
            else:
                blo, bhi = BAND_DAYS[code]
                ok = lo_ < bhi and blo < hi_
            if ok:
                codes.append(code)
        lab = cls[c][4]
        need = max(text_w(lab, fs, True), len(codes) * (fs * 1.7 + 0.6))
        if xb - xa < need + 1.0:                         # too narrow for its words: the colour says it
            continue
        xm = (xa + xb) / 2.0
        pg.text(lab, xm, yl, fs, COL["ink"], bold=True, align="C")
        cx = xm - len(codes) * (fs * 1.7 + 0.6) / 2.0
        for code in codes:
            cx += _bands_chip(pg, code, cx, yl - fs * 0.6, fs) + 0.6
    y = yl - fs * 0.6 - fs * 1.3 - 2.5
    # the bands' key: letter, name and days, wrapped to the drawing's width
    x_ = 0.0
    for code, name, eco, days, depth, zone in PLANT_BANDS:
        t = u"{} · {}".format(name.split(u" (")[0].lower(), days.replace(u" d/yr", u" d").replace(u"–", u"-"))
        w_ = fs * 1.7 + 1.0 + text_w(t, fs) + 4.0
        if x_ > 0.0 and x_ + w_ > W:
            x_, y = 0.0, y - fs * 1.7
        _bands_chip(pg, code, x_, y + fs * 1.05, fs)
        pg.text(t, x_ + fs * 1.7 + 1.0, y, fs, COL["ink"])
        x_ += w_
    t = u"S4, looking upstream · bands " + cite(BAND_SOURCE)
    if x_ > 0.0 and x_ + text_w(t, fs) > W:
        x_, y = 0.0, y - fs * 1.7
    pg.text(t, x_, y, fs, COL["ink2"])
    # v4 (MIRAQUA 28 Oct, PLAN §2): the scale bar after the caption (or on a line of its own), "1:den" after it
    xb = x_ + text_w(t, fs) + 4.0
    if xb + r28_bar_box(0.0, 0.0, den, fs, False)[2] > W:
        xb, y = 0.0, y - fs * 1.7 - 1.0
    r28_scale_bar(pg, xb, y - 0.6, den, fs, False)
    return pg


def plant_card(pg, x, y, w, card, photo, photos):
    """v3: one plant: its photo PHOTO_W x PHOTO_H (every photo in the booklet the same size, cut to 4:3 about its
    centre, never stretched; none = a labelled empty frame, its JPEG listed in photos), the band letter (x = take out)
    and the name "English (Turkish)" with its sources, then its rows [(pictogram, keywords, colour, bold)]. card =
    (band, plant key, rows, source). v4 (MIRAQUA 28 Oct): P16.1 the photo from common/plant_photos.py, an empty
    frame says "no photo: " and the reason it gives; P16.2 the rows' keywords **bold**. Returns bottom y."""
    fs = FS_MIN
    band, key, rows, src = card
    path, credit, why_not = photo
    pg.poly([rect(x, y - PHOTO_H, x + PHOTO_W, y)], fill=C["paper"], stroke=C["faint"], lw=0.2)
    if path:
        photos.append((x, y - PHOTO_H, x + PHOTO_W, y, path))
    else:
        para(pg, x + 1.5, y - 4.0, PHOTO_W - 3.0, u"no photo: " + (why_not or u"not loaded"), fs, COL["ink2"])
    yy = y - PHOTO_H - 1.2
    bw = _bands_chip(pg, band, x, yy, fs) + 1.0
    yy = para(pg, x + bw, yy + fs * 0.25, w - bw, plant_name(key) + u" " + cite(src) + (cite(credit) if credit else
                                                                                         u""), fs, COL["ink_dark"],
              bold=True) - 1.0
    for kind, words, colour, bold in rows:
        icon(pg, kind, x, yy, 4.2)
        yy = min(yy - 4.6, r28_para(pg, x + 5.0, yy + fs * 0.25, w - 5.0, words, fs, colour, bold=bold) - 0.8)
    return yy


def plant_cards():
    """v3: the cards of p.22: the nine kept plants (where, why, warning) and the one to take out (Prompt 5 task 3c:
    every plant the booklet names gets its photo)."""
    out = []
    for band, key, where, why, src, flag in SPECIES:
        # v4 (MIRAQUA 28 Oct, P16.2): the where row no longer all bold; its keywords are (SPECIES **markup**)
        rows = [(where[0], where[1], COL["river_dark"], False)] + [(k_, t_, COL["ink"], False) for k_, t_ in why]
        if flag:
            hot = flag.isupper()
            rows.append(("scent" if flag in (u"aromatic", u"scent layer") else "warn", flag.lower() if hot else flag,
                         C["acc"] if hot else COL["ink2"], hot))
        out.append((band, key, rows, src))
    key, words, src = SPECIES_REMOVE
    out.append(("x", key, [("warn", words, C["acc"], False)], src))
    return out


def where_on_site(pg, x0, y, x1):
    """The stream in water order with the places and what is planted there, from the top y. Returns bottom y."""
    fs = FS_MIN
    pg.text(u"WHERE ON SITE · in water order, not to scale", x0, y - 3.2, 3.2, COL["ink_dark"], bold=True)
    y -= 3.2 + 10.5
    rh = 2.4
    pg.poly([[(x0, y), (x1 - 6.0, y), (x1 - 6.0, y + 1.6), (x1, y - rh / 2.0), (x1 - 6.0, y - rh - 1.6),
              (x1 - 6.0, y - rh), (x0, y - rh)]], fill=MP["discharge"][0], stroke=MP["discharge"][1], lw=0.25)
    sw = (x1 - x0) / len(PLANT_SITES)
    low = y
    for j, (place_, kinds, words, src) in enumerate(PLANT_SITES):
        sx = x0 + j * sw
        pg.circle(sx + 2.0, y - rh / 2.0, 1.4, fill=COL["river_dark"])
        for i, kind in enumerate(kinds):
            icon(pg, kind, sx + 4.4 + i * 6.0, y + 7.4, 5.4)
        pg.text(place_, sx + 4.4 + len(kinds) * 6.0 + 1.0, y + 3.0, fs, COL["ink_dark"], bold=True)
        low = min(low, r28_para(pg, sx, y - rh - 0.6, sw - 3.0, words + (u" " + cite(src) if src else u""), fs,
                                COL["ink"]))           # v4 (P16.2): **bold** keywords
    return low


def why_here(pg, kx, ky, kw):
    """The key at the right of the bands: why here = days a year under water on this cut, shade, cleaning.
    Returns bottom y."""
    fs = FS_MIN
    pg.text(u"WHY HERE", kx, ky - 3.2, 3.2, COL["ink_dark"], bold=True)
    ky -= 3.2 + 2.0
    pg.text(u"days a year under water", kx, ky - fs, fs, COL["ink2"])
    ky -= fs * 1.6
    for i, c in enumerate(s4_classes(detail_engine())):
        pg.poly([rect(kx, ky - fs, kx + 5.0, ky)], fill=DAYS_COL[i], stroke=C["faint"], lw=0.1)
        pg.text(c[4], kx + 6.5, ky - fs * 0.9, fs, COL["ink"])
        ky -= fs * 1.45
    ky -= 2.0
    # v3.2 (Aras 27 Oct, Prompt 8, rule 7: no "no data" rows): the row "odour: no plant measured" is left out
    for kind, words in (("tree", u"**shade**: new trees where the July shade below is shortest"),   # v4 (P16.2)
                        ("clean", u"**cleaning**: reed beds upstream")):
        icon(pg, kind, kx, ky, 4.4)
        ky = min(ky - 5.0, r28_para(pg, kx + 5.6, ky + fs * 0.25, kw - 5.6, words, fs, COL["ink"]) - 0.8)
    return ky


def draw_plants_panel(pg, box, opt, log):
    """v3 p.22 (Aras 27 Oct 17:34, Prompt 5 task 3): laid out to fill box: at the foot one photo card a plant (the
    nine kept and the one to take out, names "English (Turkish)", every photo PHOTO_W x PHOTO_H); above them the bands
    on the S4 cut at the largest round scale that fits, with the WHY HERE key at its right, and where on site under
    the bands (or beside them, where a smaller scale leaves the width empty); what height is left over is shared
    between the gaps. Returns its bbox."""
    x0, y0, x1, y1 = box
    n0 = len(pg.items)
    W = x1 - x0
    kw = 62.0                                            # the key column at the right of the cut
    room = W - kw - 4.0                                  # the width for the bands
    cards = plant_cards()
    n = len(cards)
    cw = (W - (n - 1) * CARD_GAP) / n
    state = {}
    photos = [plant_photo_of(c[1], log, state) if PHOTO_ON[0] else (None, None, u"photos switched off")   # v4 (P16.1)
              for c in cards]
    hc = max(-plant_card(Page(0, 0), 0.0, 0.0, cw, c, p, []) for c, p in zip(cards, photos))
    hw = -where_on_site(Page(0, 0), 0.0, 0.0, W)
    hk = -why_here(Page(0, 0), 0.0, 0.0, kw)
    hb = y1 - y0 - hc - 4.0                              # the height over the cards
    pick = None
    for den in BANDS_DENS:
        part = draw_bands(opt, den)
        pb = items_bbox(part.items)
        bw, bh = pb[2] - pb[0], pb[3] - pb[1]
        ws = room - bw - 6.0                             # where on site beside the bands
        if bw <= room and bh <= hb - hw - 4.0:
            pick = (den, part, None)
        elif ws >= 120.0 and max(bh, -where_on_site(Page(0, 0), 0.0, 0.0, ws)) <= hb:
            pick = (den, part, ws)
        if pick:
            break
    den, part, ws = pick or (den, part, None)
    s, bb = place(pg, part, (x0, y1 - hb, x0 + room, y1), 1.0, "TL", log, "planting bands")
    if s < 0.999:
        log.append(u"WARNING: the planting bands are printed at {:.0f} % of 1:{:,.0f}".format(100 * s, den))
    BANDS_DEN[0] = den / s
    why_here(pg, x1 - kw, y1, kw)
    top = min(bb[1], y1 - hk)                            # the foot of the bands and their key
    if ws:
        top = min(top, where_on_site(pg, bb[2] + 6.0, y1, bb[2] + 6.0 + ws))
    else:
        gap = max(4.0, (top - y0 - hc - hw) / 2.0)
        where_on_site(pg, x0, top - gap, x1)
    for i, (c, p) in enumerate(zip(cards, photos)):
        plant_card(pg, x0 + i * (cw + CARD_GAP), y0 + hc, cw, c, p, PHOTOS)
    log.append(u"p.22 plants: bands 1:{:,.0f}{}, {} cards, photos {} of {} ({})".format(
        den / s, u", where on site beside them" if ws else u"", n, len(PHOTOS), n, PLANT_PHOTO_DIR))
    return items_bbox(pg.items[n0:])
