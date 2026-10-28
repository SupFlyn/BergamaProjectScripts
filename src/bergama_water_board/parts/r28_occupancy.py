# ---- v4 (MIRAQUA 28 Oct 2026): the water board's part of the round (revision_2026-10-28/PLAN.md, row WB) ----------
# Bold keywords in running text (G5), the scale bar (PLAN §2: standard scales, a bar beside every orthogonal drawing),
# the shared silhouettes of common/figures.py for the people of the S4 cuts (pp.14-15, P19.2), THE SEASON beside the
# p.14 rows (P14.2) and the p.15 occupancy diagram (P15.2). Included by code.py after the season tables (SEASON_USE),
# before the code that calls it.
BK_KEY_H = 190.0                     # the most a fixed 1:1 crop may be tall on pp.14-15: the booklet puts the S4 key map
#                                      (190 x up to 42 mm) under the title, so the rows start at y <= 78 mm (273 - 78 - 5)
R28_PART_H = BK_KEY_H - 10.0         # its panel under the context line (crop pads 2 x 1 mm, one 4.2 mm line, the 3 mm gap)
R28_SENSE_W = 72.0                   # p.14: the FEEL / HEAR / TOUCH column at most, mm (THE SEASON takes the rest)
S4_NE_POCHE = 1.0                    # p.15: soil drawn under the strip, m (the engine's 1.9): the room goes to the diagram


def r28_crop_note(log, cid):
    """the size of a fixed crop of pp.14-15 in the log, with a warning when it is taller than BK_KEY_H"""
    for c in BK_CROPS:
        if c[0] == cid:
            w, h = c[1][2] - c[1][0], c[1][3] - c[1][1]
            log.append(u"{}{}: {:.1f} x {:.1f} mm{}".format(u"WARNING: " if h > BK_KEY_H else u"", cid, w, h,
                                                            u" (more than the {:.0f} mm under the S4 key map)".format(
                                                                BK_KEY_H) if h > BK_KEY_H else u""))


# ---------------------------------------------------------------- G5: text with **bold** keywords
def r28_words(s, bold=False):
    """s with '**' switching bold on and off, as words [[(text, bold), ...]] (a word is what lies between spaces; a
    '**' inside a word splits it into pieces)"""
    words, glue = [], False
    for i, part in enumerate(s.split(u"**")):
        b = bold != (i % 2 == 1)
        for j, pc in enumerate(part.split(u" ")):
            if j:
                glue = False
            if pc:
                if glue and words:
                    words[-1].append((pc, b))
                else:
                    words.append([(pc, b)])
                glue = True
    return words


def r28_runs(words):
    """one line of words as runs [(text, bold)], neighbouring pieces of one weight joined"""
    runs = []
    for k, wd in enumerate(words):
        for j, (t, b) in enumerate(wd):
            if k and not j:
                t = u" " + t
            if runs and runs[-1][1] == b:
                runs[-1] = (runs[-1][0] + t, b)
            else:
                runs.append((t, b))
    return runs


def r28_tw(s, size, bold=False):
    """the width of one line of text with **bold** keywords, mm"""
    return sum(text_w(t, size, b) for t, b in r28_runs(r28_words(s, bold)))


def r28_draw_runs(pg, runs, x, y, size, colour, kcol=None, halo=None):
    for t, b in runs:
        pg.text(t, x, y, size, (kcol or colour) if b else colour, bold=b, halo=halo)
        x += text_w(t, size, b)
    return x


def r28_text(pg, s, x, y, size, colour, bold=False, align="L", kcol=None, halo=None):
    """one line of text with **bold** keywords (kcol: their colour); returns its width"""
    runs = r28_runs(r28_words(s, bold))
    w = sum(text_w(t, size, b) for t, b in runs)
    r28_draw_runs(pg, runs, x - {"L": 0.0, "C": w / 2.0, "R": w}[align], y, size, colour, kcol, halo)
    return w


def r28_lines(s, size, width, bold=False):
    """s wrapped to width as lines of runs"""
    out, cur, cw = [], [], 0.0
    sp = text_w(u" ", size)
    for wd in r28_words(s, bold):
        ww = sum(text_w(t, size, b) for t, b in wd)
        if cur and cw + sp + ww > width:
            out.append(r28_runs(cur))
            cur, cw = [wd], ww
        else:
            cw += (sp if cur else 0.0) + ww
            cur.append(wd)
    if cur:
        out.append(r28_runs(cur))
    return out


def r28_para(pg, x, y, w, s, size, colour, bold=False, lh=1.28, kcol=None, halo=None):
    """para() with **bold** keywords (G5): wrapped to w from the top y; returns the bottom y"""
    for runs in r28_lines(s, size, w, bold):
        y -= size * lh
        r28_draw_runs(pg, runs, x, y, size, colour, kcol, halo)
    return y


def r28_bold(s, words):
    """s with the first place of each of words marked **bold**"""
    for wd in words:
        i = s.find(wd)
        if i >= 0:
            s = s[:i] + u"**" + wd + u"**" + s[i + len(wd):]
    return s


def r28_mix(a, b, t):
    """hex colour a taken t of the way to b"""
    return u"".join(u"%02X" % int(round(int(a[i:i + 2], 16) * (1.0 - t) + int(b[i:i + 2], 16) * t)) for i in (0, 2, 4))


# ---------------------------------------------------------------- PLAN §2: the scale bar of an orthogonal drawing
R28_BAR = {200: (0, 2, 5, 10), 250: (0, 2, 5, 10), 500: (0, 5, 10, 20), 1000: (0, 10, 20, 50)}   # its marks, m


def r28_bar_box(x, y, den, fs=None, below=True):
    """the box (x0, y0, x1, y1) that r28_scale_bar takes when drawn from (x, y)"""
    fs = fs or FS_MIN
    t = R28_BAR.get(int(round(den)), (0, 5, 10, 20))
    x1 = x + t[-1] * 1000.0 / den
    lab = text_w(u"1:{:,.0f}".format(den), fs)
    if below:
        return (x - 1.0, y - fs * 1.3 - 0.2, max(x1 + 3.5, x + lab), y + 2.0 + fs * CAP + 0.2)
    return (x - 1.0, y - fs * 0.3, x1 + 4.0 + lab, y + 2.0 + fs * CAP + 0.2)


def r28_scale_bar(pg, x, y, den, fs=None, below=True, colour=None):
    """the scale bar of a drawing at 1:den from (x, y): ink and white segments 1.2 mm high, the marks in m over them,
    "1:den" under the bar (below) or after it. Returns its box."""
    fs = fs or FS_MIN
    ink = colour or COL["ink"]
    k = 1000.0 / den
    t = R28_BAR.get(int(round(den)), (0, 5, 10, 20))
    for i in range(len(t) - 1):
        pg.poly([rect(x + t[i] * k, y, x + t[i + 1] * k, y + 1.2)], fill=ink if i % 2 == 0 else COL["white"],
                stroke=ink, lw=0.12)
    for i, v in enumerate(t):
        pg.text(u"{}{}".format(v, u" m" if i == len(t) - 1 else u""), x + v * k, y + 2.0, fs, ink, align="C")
    lab = u"1:{:,.0f}".format(den)
    if below:
        pg.text(lab, x, y - fs * 1.05, fs, ink)
    else:
        pg.text(lab, x + t[-1] * k + 4.0, y, fs, ink)
    return r28_bar_box(x, y, den, fs, below)


def r28_bar_free(items, cands, den, fs=None, below=True):
    """the first spot (x, y) of cands where the scale bar lies clear of everything in items, else None"""
    boxes = [items_bbox([it]) for it in items]
    for x, y in cands:
        b = r28_bar_box(x, y, den, fs, below)
        if not any(lp_hit(b, o, 0.6) for o in boxes):
            return x, y
    return None


# ---------------------------------------------------------------- P19.2: one figure set (common/figures.py)
R28_SEAT = 0.445                     # the sit pose's seat over its feet, m (common/figures.py: thigh 0.52 less half of it)
R28_CHILD = 1.15                     # a child, m (common/figures.py)
R28_ASSET_POSE = {  # the detail engine's traced people (DETAIL_SRC FIGS) as poses of common/figures.py: (pose, extra)
    "I_walker_flood_wall": ("walk", None), "I_woman_with_bag": ("walk", None), "J_woman_walking": ("walk", None),
    "I_photographer": ("watch", None), "J_man_and_child": ("walk", "child"), "J_photographer_balcony": ("watch", None),
    "J_woman_on_steps": ("stand", None), "I_child_on_sand": ("touch", "small"), "J_person_seated": ("sit", "edge"),
    "J_person_sitting": ("sit", "stool"), "J_cyclist_cheering": ("bike", None), "I_cyclist_waving": ("bike", None)}
R28_ACT_POSE = {"sit": ("sit", 1.75), "watch": ("watch", 1.75), "walk": ("walk", 1.75), "child": ("walk", R28_CHILD),
                "wade": ("wade", 1.75)}       # p.14 season column: what people do (SEASON_USE acts) as silhouettes


def r28_fig(pg, pose, x, y, k, colour, facing=1, height=1.75, layer="people"):
    """one silhouette of common/figures.py with its feet at (x, y), k mm per m, filled in one opaque colour, no
    stroke, one poly per outline (the pages fill even-odd); on this board's Page or the detail engine's. Returns its
    box."""
    xs, ys = [], []
    for ring in fig_polys(pose, height, facing):
        pts = [(x + px * k, y + py * k) for px, py in ring]
        xs += [p[0] for p in pts]
        ys += [p[1] for p in pts]
        pg.poly([pts], fill=colour, stroke=None, layer=layer)
    return (min(xs), min(ys), max(xs), max(ys))


def r28_stall(pg, x, y, k, colour, lw=0.18):
    """a market stall in thin lines, its base centred at (x, y), k mm per m. Returns its box."""
    a, b, h = x - 1.2 * k, x + 1.2 * k, 2.0 * k
    for xx in (a, b):
        pg.line([(xx, y), (xx, y + h)], colour, lw)
    pg.line([(a - 0.25 * k, y + h), (x, y + h + 0.35 * k), (b + 0.25 * k, y + h)], colour, lw)
    pg.line([(a, y + 0.8 * k), (b, y + 0.8 * k)], colour, lw)
    return (a - 0.25 * k, y, b + 0.25 * k, y + h + 0.35 * k)


def r28_people(E):
    """the detail engine's people (draw_asset, which figure() and balcony() call) and cyclists (bike) drawn as the
    shared silhouettes, in the engine's colours and layers, at the scale it draws at (E["K"] at the call); a seated
    figure is anchored at its seat (it sits on an edge). The traced assets are no longer decoded."""
    def draw_asset(pg, key, X, Y, height_mm=None, flip=False, layer="entourage", tone=None):
        pose, extra = R28_ASSET_POSE.get(key, ("stand", None))
        k = E["K"]
        f = -1 if flip else 1
        col = tone or E["FIG"]
        if extra == "edge":
            Y -= R28_SEAT * k
        r28_fig(pg, pose, X, Y, k, col, f, R28_CHILD if extra == "small" else 1.75, layer)
        if extra == "child":
            r28_fig(pg, "walk", X + f * 0.5 * k, Y, k, col, f, R28_CHILD, layer)
        elif extra == "stool":
            for a in (-0.12, 0.2):
                pg.poly([rect(X + f * (a - 0.02) * k, Y, X + f * (a + 0.02) * k, Y + R28_SEAT * k)], fill=col,
                        stroke=None, layer=layer)
            pg.poly([rect(X - f * 0.16 * k, Y + (R28_SEAT - 0.04) * k, X + f * 0.24 * k, Y + R28_SEAT * k)], fill=col,
                    stroke=None, layer=layer)

    def bike(pg, S, s, flip):
        X, Y = S.P(s, S.surf(s))
        r28_fig(pg, "bike", X, Y, E["K"], E["FIG"], -1 if flip else 1, 1.75, "people")
    E["draw_asset"] = draw_asset
    E["bike"] = bike


# ---------------------------------------------------------------- P14.2: THE SEASON beside the p.14 rows
R28_PLANT_KEY = {"winter": (u"bare", u"evergreen"), "spring": (u"Fresh leaves", u"in flower"),
                 "summer": (u"Full leaf", u"meadow drying"), "autumn": (u"turning", u"gold")}   # G5 in SEASONS plants


def season_climate(sea):
    """the season's measured climate and its water balance as the detail engine's SEASONS texts give them (strings,
    unchanged): (rain mm, share %, rain days, mean C, rain minus evaporation mm, its words), or None if a text reads
    otherwise"""
    import re as _re
    m = _re.search(r"Rain ([\d.]+) mm \(([\d.]+) %[^)]*\), ([\d.]+) rain days, mean ([\d.]+) C", sea["climate"][0])
    b = _re.search(r"evaporation ([+-]?[\d.]+) mm[:;]?\s*(.*?)\s*\(calculated",
                   sea["climate"][1]) if len(sea["climate"]) > 1 else None
    if not m or not b:
        return None
    return m.groups() + b.groups()


def season_info(pg, x, y, key, w):
    """THE SEASON beside a p.14 row, w wide from the top y: the climate (measured) and the rain the open water loses
    (calculated), what the plants do (design) and the season's story, keywords bold (G5). Returns the bottom y."""
    fs = FS_MIN
    sea = [s for s in detail_engine()["SEASONS"] if s["key"] == key][0]
    use = SEASON_USE[key]
    cl = season_climate(sea)
    if cl:
        rain, pct, days, temp, bal, words = cl
        yy = r28_para(pg, x, y, w, u"**rain {} mm** · {} % of the year · {} rain days · mean **{} °C** {}".format(
            rain, pct, days, temp, cite(YEAR_SRC[0][1])), fs, COL["ink"])
        yy = r28_para(pg, x, yy - 0.4, w, u"rain minus open-water evaporation **{} mm**{} {}".format(
            bal, (u": " + words) if words else u"", cite(YEAR_SRC[1][1])), fs, COL["ink"])
    else:
        yy = r28_para(pg, x, y, w, u" ".join(sea["climate"]), fs, COL["ink"])
    yy = r28_para(pg, x, yy - 1.2, w, r28_bold(sea["plants"], R28_PLANT_KEY.get(key, ())), fs, C["wet"])
    if use.get("extra"):
        kind, words = use["extra"][0], use["extra"][1]
        yy -= 0.8
        if kind == "stall":
            r28_stall(pg, x + 2.3, yy - 4.4, 1.7, COL["ink"])
        else:
            icon(pg, kind, x, yy, 4.6)
        yy = min(yy - 5.2, r28_para(pg, x + 6.0, yy + fs * 0.2, w - 6.0, words, fs, MP["discharge"][2]) - 0.4)
    return yy


# ---------------------------------------------------------------- P15.2: the occupancy diagram under the p.15 cut
# Design spec (change log WB): the time axis Jan-Dec on the cut's own width (s 652 -> 588, Jan under the promenade,
# Dec under the strip; 1:250 = 21.3 mm a month); a head row (floods and Kermes; the in-bed sub-hub), the months, one
# lane a band of the cut top to bottom by level as the bank steps down, feel · hear · touch under them; the lanes'
# names and levels and a small profile of the cut (the lane's band in ink) at the left, the key at the right.
OCC_LANES = [  # (key, name, s from, s to along S4, m): the bands of the north-east bank (SECTIONS[1]), was NE_ZONES
    ("prom", u"promenade", 652.0, 638.0), ("steps", u"steps · amphitheatre", 638.0, 633.5),
    ("lower", u"lower walk", 633.5, 622.5), ("bed", u"gravel bed", 622.5, 594.0), ("strip", u"summer strip", 594.0, 590.0)]
OCC_S = (652.0, 588.0)               # the time axis spans the cut above it, s along S4
OCC_GROUPS = [  # who: (key, name, colour); locals, tourists, students as the city link's GROUP (pp.08, 10)
    ("locals", u"locals", "CC9A52"), ("tourists", u"tourists", "8B3A3F"), ("students", u"students", "5C7A86"),
    ("kermes", u"Kermes visitors", "5E4B8B")]   # new: dE00 >= 20.6 to the other three (>= 13.2 at OCC_ALPHA)
OCC_COL = dict((k_, c_) for k_, _, c_ in OCC_GROUPS)
OCC_KERMES = (5 + 28.5 / 30.0, 6 + 5.0 / 31.0)   # 29 Jun-5 Jul in months from 1 Jan (h01 §2.8, the 90th Kermes, 2026)
OCC_FLOOD = S4_MONTH_IDX["winter"]   # the months the flood reach (Q100 / Q500) is drawn, as the winter cut draws them
OCC_HUB_COL = R28_ZONE["subhub"][1]  # the in-bed sub-hub, as on the p.24 plans and the senses page
OCC_ALPHA = 0.45                     # the user bands, see-through so that the overlaps show
OCC_T = 0.6                          # a band at 3 (busy) is 0.6 of its lane tall
OCC_OFF = (0.0, 0.15, -0.15)         # the 1st, 2nd and 3rd group of a lane: its centre line off the lane's middle, x lane
OCC_FIG = 0.62                       # an adult silhouette, x lane
# DESIGN ASSUMPTION (ours, said on the diagram): how busy each band is a month (Jan-Dec, 0 nobody - 3 busy), and where
# a figure stands and what it does: (months from 1 Jan, pose or "stall", height m, keywords or None). The activities
# are the season cuts' own (S4_SEASON, the detail section's season texts, concept v1 §10.1); the Kermes visitors come
# in the Kermes week only (OCC_KERMES); none of it is a count.
OCC_USE = {
    "prom": [("locals", (2, 2, 2, 2, 3, 3, 3, 3, 3, 2, 2, 2), [(1.0, "watch", 1.75, u"watch the **floods**"),
                                                               (8.5, "walk", 1.75, u"**walk** the promenade")]),
             ("tourists", (0, 0, 1, 1, 2, 2, 2, 2, 2, 1, 0, 0), [(4.4, "walk", 1.75, None)]),
             ("kermes", None, [(6.05, "walk", 1.75, None)])],
    "steps": [("locals", (1, 1, 1, 2, 2, 2, 3, 3, 2, 2, 1, 1), [(7.0, "sit", 1.75, u"**sit** by the water")]),
              ("students", (1, 1, 2, 2, 2, 1, 0, 0, 1, 2, 2, 1), [(10.4, "sit", 1.75, u"**students** on the steps")])],
    "lower": [("locals", (1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1), [(1.2, "walk", 1.75, u"open **between storms**")]),
              ("tourists", (0, 0, 1, 1, 2, 2, 2, 2, 2, 1, 0, 0), [(3.6, "walk", 1.75, u"lower walk **open**")])],
    "bed": [("locals", (0, 0, 1, 1, 1, 2, 3, 3, 2, 1, 0, 0), [
                (3.3, "touch", R28_CHILD, u"children at the **water's edge**"),
                (8.9, "walk", 1.75, u"walk the **gravel bed**")]),
            ("tourists", (0, 0, 0, 0, 1, 1, 2, 2, 1, 0, 0, 0), []),
            ("kermes", None, [(6.05, "stall", 1.75, u"**Kermes** stalls")])],
    "strip": [("locals", (0, 0, 0, 1, 1, 2, 3, 3, 1, 0, 0, 0), [(6.9, "wade", 1.75, u"**wade** · feet in the water")]),
              ("tourists", (0, 0, 0, 0, 0, 1, 2, 2, 0, 0, 0, 0), [])],
}
OCC_NOTES = [("bed", 0.9, u"the river **takes the bed back**")]   # words on the water: (lane, months, keywords)


def occ_frac(S, a, b, z):
    """the share of this cut's ground from s a to s b that lies under the level z"""
    n = max(4, int(abs(b - a) / 0.25))
    return sum(1 for i in range(n + 1) if S.surf(a + (b - a) * i / float(n)) < z) / float(n + 1)


def occ_ease(vals, t):
    """a value a month (Jan-Dec, at the month middles) at t months from 1 Jan, cosine-eased, round the year"""
    u = t - 0.5
    i = int(math.floor(u))
    w = (1.0 - math.cos(math.pi * (u - i))) / 2.0
    return vals[i % 12] * (1.0 - w) + vals[(i + 1) % 12] * w


def occ_step(vals, t, r=0.12):
    """a value a month at t, held through each month and eased over r months at its ends"""
    m = int(math.floor(t))
    f = t - m
    if f < r:
        w = 0.5 + 0.5 * f / r
        return vals[(m - 1) % 12] * (1.0 - w) + vals[m % 12] * w
    if f > 1.0 - r:
        w = 0.5 + 0.5 * (1.0 - f) / r
        return vals[m % 12] * w + vals[(m + 1) % 12] * (1.0 - w)
    return vals[m % 12]


def occ_kermes(t, r=0.15):
    """the Kermes visitors at t: 3 in the Kermes week (OCC_KERMES), eased to nothing over r months"""
    a, b = OCC_KERMES
    d = a - t if t < a else (t - b if t > b else 0.0)
    return 3.0 * (1.0 + math.cos(math.pi * d / r)) / 2.0 if d < r else 0.0


def occ_runs(n, ok):
    """the indices 0 .. n-1 for which ok(i), in runs"""
    out, cur = [], []
    for i in range(n):
        if ok(i):
            cur.append(i)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def occ_spans(ms):
    """the months ms (0 = Jan) as spans [(first, end)] along the year: Dec-Feb gives (0, 2) and (11, 12)"""
    out, m = [], 0
    while m < 12:
        if m in ms:
            n = m
            while n + 1 < 12 and (n + 1) in ms:
                n += 1
            out.append((m, n + 1))
            m = n + 1
        else:
            m += 1
    return out


def draw_occupancy(pg, E, S, y0, h_avail, x_left, x_right):
    """THROUGH THE YEAR under the S4 north-east cut (P15.2; references p15_ref1 "Dock Square 24h": lanes, bands that
    swell with intensity, small figures in them; p15_ref2 "flexible programmes": user groups as see-through flowing
    shapes that overlap, two hatches for free time), on the cut's own width: one lane a band of the cut (OCC_LANES), the
    users in it (OCC_USE, design assumption) with silhouettes and a few words, the season's water toned and the winter
    flood reach (Q500 hatched, Q100 dashed) where this cut's ground lies under them, free time hatched (shareable;
    open to new programmes), the in-bed sub-hub and the Kermes in the head row, feel · hear · touch in a few words,
    the key at the right (x_right = the cut's right edge). Fills h_avail from y0 down. Returns the bottom y."""
    fs = FS_MIN
    XL, XR = min(S.X(OCC_S[0]), S.X(OCC_S[1])), max(S.X(OCC_S[0]), S.X(OCC_S[1]))
    mw = (XR - XL) / 12.0

    def X(t):
        return XL + t * mw
    bed, q100, q500 = E["THALWEG"][1], E["Q100"], E["Q500"]
    lev = [(None, False)] * 12                           # the season's water a month, as the season cuts draw it
    for sea in E["SEASONS"]:
        filled = [w_[0] for w_ in sea["water"] if w_[1]]
        for m in S4_MONTH_IDX[sea["key"]]:
            lev[m] = (max(filled) if filled else None, sea["strip_held"])
    segs = [("winter", 0, 2), ("spring", 2, 5), ("summer", 5, 8), ("autumn", 8, 11)]

    def sense_text(key):
        u_ = SEASON_USE[key]
        return u"**{}** · {} · {}".format(*[u_[k_][1].replace(u"**", u"") for k_ in ("feel", "hear", "touch")])
    hs = max(max(len(r28_lines(sense_text(k_), fs, (b_ - a_) * mw - 1.6)) for k_, a_, b_ in segs) * fs * 1.28 + 1.2,
             fs * 2.6 + 0.8)
    L = max(7.0, min(11.5, (h_avail - 11.0 - hs - 0.5) / len(OCC_LANES)))
    yl = y0 - 11.0                                       # the top of the lanes
    ybot = yl - L * len(OCC_LANES)
    ts = [i * 0.05 for i in range(241)]                  # 0 ... 12 months
    nt = len(ts)
    lanes = []
    for i, (key, name, a, b) in enumerate(OCC_LANES):
        cache = {}

        def fr(z, a=a, b=b, cache=cache):
            if z not in cache:
                cache[z] = occ_frac(S, a, b, z)
            return cache[z]
        top = yl - i * L
        ln = dict(key=key, name=name, a=a, b=b, top=top, bot=top - L, mid=top - L / 2.0)
        ln["back"] = [fr(lev[m][0]) if lev[m][0] is not None else 0.0 for m in range(12)]
        ln["tone"] = [max(ln["back"][m], fr(bed + 0.005) if lev[m][1] else 0.0) for m in range(12)]
        ln["f500"] = [fr(q500) if m in OCC_FLOOD else 0.0 for m in range(12)]
        ln["f100"] = [fr(q100) if m in OCC_FLOOD else 0.0 for m in range(12)]
        use = OCC_USE.get(key, [])
        ln["bands"] = []
        for j, (g, vals, marks) in enumerate(use):
            th = [(occ_kermes(t) if vals is None else occ_ease(vals, t)) / 3.0 * OCC_T * L for t in ts]
            ln["bands"].append((g, ln["mid"] + OCC_OFF[j % len(OCC_OFF)] * L, th, marks))
        ln["total"] = [sum(v[m] for _, v, _ in use if v is not None) for m in range(12)]
        lanes.append(ln)

    def env(ln, i):
        on = [(c - th[i] / 2.0, c + th[i] / 2.0) for _, c, th, _ in ln["bands"] if th[i] > 0.05]
        return (min(e[0] for e in on), max(e[1] for e in on)) if on else None

    def free(ln, m):
        """the free time of a lane in month m: "share", "open" or None (busy, the water's, or the bed closed)"""
        if ln["back"][m] >= 0.5 or ln["f500"][m] >= 0.5:
            return None
        if ln["key"] == "bed" and m not in SUBHUB_OPEN:
            return None
        return "open" if ln["total"][m] <= 1 else ("share" if ln["total"][m] <= 2 else None)
    # free time under everything: wavy lines (shareable) or dots (open to new programmes) round the bands
    pad = 0.4
    for ln in lanes:
        tone = [occ_step(ln["tone"], t) for t in ts]
        for m in range(12):
            cls = free(ln, m)
            if cls is None:
                continue
            idx = [i for i in range(nt) if m - 1e-6 <= ts[i] <= m + 1 + 1e-6]
            es = [env(ln, i) or (ln["mid"], ln["mid"]) for i in idx]
            if cls == "share":
                if all(env(ln, i) is None for i in idx):
                    regs = [rect(X(m), ln["bot"] + pad, X(m + 1), ln["top"] - pad)]
                else:
                    regs = [[(X(m), ln["top"] - pad), (X(m + 1), ln["top"] - pad)] +
                            [(X(ts[i]), min(ln["top"] - pad, e[1] + pad)) for i, e in zip(idx, es)][::-1],
                            [(X(m), ln["bot"] + pad)] +
                            [(X(ts[i]), max(ln["bot"] + pad, e[0] - pad)) for i, e in zip(idx, es)] +
                            [(X(m + 1), ln["bot"] + pad)]]
                for r_ in regs:
                    pg.poly([r_], fill=COL["white"], stripes=(COL["ink2"], 1.1, 0.12, 0.0, True))
                continue
            gx = XL + 0.75 + 1.5 * math.ceil((X(m) + 0.3 - XL - 0.75) / 1.5)
            while gx < X(m + 1) - 0.3:
                i = min(nt - 1, max(0, int(round((gx - XL) / mw / 0.05))))
                e = env(ln, i)
                gy = ln["bot"] + 0.75
                while gy < ln["top"] - 0.5:
                    if gy > ln["bot"] + tone[i] * (L - 0.2) + 0.3 and (e is None or gy > e[1] + pad or gy < e[0] - pad):
                        pg.circle(gx, gy, 0.15, fill=COL["ink2"])
                    gy += 1.5
                gx += 1.5
    # the grid: months (seasons a little darker), lanes
    for m in range(13):
        pg.line([(X(m), y0 - 7.0), (X(m), ybot)], C["structure"] if m % 3 == 2 or m in (0, 12) else COL["faint"],
                0.12 if m % 3 == 2 else 0.1)
    for i in range(len(OCC_LANES) + 1):
        pg.line([(x_left, yl - i * L), (XR, yl - i * L)], C["structure"] if i in (0, len(OCC_LANES)) else COL["faint"],
                0.15)
    # the water: the season's (tone, as the season cuts draw it), the winter flood reach (Q500 hatched, Q100 dashed)
    for ln in lanes:
        for vals, kind in ((ln["tone"], "tone"), (ln["f500"], "q500"), (ln["f100"], "q100")):
            fv = [occ_step(vals, t) for t in ts]
            for run in occ_runs(nt, lambda i: fv[i] > 0.003):
                top_ = [(X(ts[i]), ln["bot"] + fv[i] * (L - 0.2)) for i in run]
                ring = [(X(ts[run[0]]), ln["bot"])] + top_ + [(X(ts[run[-1]]), ln["bot"])]
                if kind == "tone":
                    pg.poly([ring], fill=C["w1"], alpha=0.6)
                    pg.line(top_, C["w2"], 0.2)
                elif kind == "q500":
                    pg.poly([ring], fill=None, stroke=C["w4"], lw=0.1, stripes=(C["w4"], 0.9, 0.12, 45.0))
                else:
                    pg.line(top_, C["w4"], 0.2, dash=[0.8, 0.5])
    # the in-bed sub-hub along the bed lane: solid while open, dashed while closed
    for ln in lanes:
        if ln["key"] == "bed":
            for ms, op in ((SUBHUB_OPEN, True), ([m for m in range(12) if m not in SUBHUB_OPEN], False)):
                for a_, b_ in occ_spans(ms):
                    pg.line([(X(a_), ln["top"] - 0.3), (X(b_), ln["top"] - 0.3)], OCC_HUB_COL, 0.4 if op else 0.2,
                            dash=None if op else [0.8, 0.6])
    # the users: flowing see-through bands, the silhouettes in them, their words (G4: place_labels_all)
    for ln in lanes:
        for g, c, th, marks in ln["bands"]:
            for run in occ_runs(nt, lambda i: th[i] > 0.05):
                up = [(X(ts[i]), c + th[i] / 2.0) for i in run]
                lo = [(X(ts[i]), c - th[i] / 2.0) for i in run]
                pg.poly([up + lo[::-1]], fill=OCC_COL[g], stroke=OCC_COL[g], lw=0.1, alpha=OCC_ALPHA)
    taken, says = [], []
    k = OCC_FIG * L / 1.75
    for ln in lanes:
        for g, c, th, marks in ln["bands"]:
            fc = r28_mix(OCC_COL[g], COL["ink_dark"], 0.3)
            for t, pose, h, words in marks:
                if pose == "stall":
                    bx = r28_stall(pg, X(t), c - 0.5 * OCC_FIG * L, k * 0.8, fc)
                else:
                    bx = r28_fig(pg, pose, X(t), c - 0.5 * OCC_FIG * L, k, fc, 1, h)
                taken.append(bx)
                if words:
                    says.append((ln["key"], bx[2] + 0.3, (bx[1] + bx[3]) / 2.0, words, 0))
    for key, t, words in OCC_NOTES:
        for ln in lanes:
            if ln["key"] == key:
                says.append((key, X(t), ln["bot"] + max(0.6, occ_step(ln["tone"], t) * (L - 0.2) * 0.5), words, 1))
    for ln in lanes:
        mine = [s_ for s_ in says if s_[0] == ln["key"]]
        its = [dict(x=ax, y=ay, rank=rk, wh=lambda f, s=wd: (r28_tw(s, fs * f) + 0.8, fs * f * 0.95 + 0.5))
               for _, ax, ay, wd, rk in mine]
        got = place_labels_all(its, taken, (XL + 0.3, ln["bot"] + 0.2, XR - 0.3, ln["top"] - 0.2), (), (1.0,), 0.4)
        for i, (bx, far, f) in got.items():
            if far:
                pg.line([(its[i]["x"], its[i]["y"]), lp_leader_end(bx, (its[i]["x"], its[i]["y"]))], COL["ink2"], 0.1)
            r28_text(pg, mine[i][3], bx[0] + 0.4, bx[1] + 0.25 + fs * f * 0.21, fs * f, COL["ink_dark"],
                     halo=COL["white"])
    # the head row: the floods and the Kermes (line 1), the in-bed sub-hub (line 2); the months
    y1, y2, yh = y0 - 2.4, y0 - 5.6, y0 - 6.3
    for a_, b_ in occ_spans(OCC_FLOOD):
        pg.line([(X(a_) + 0.3, y0 - 3.9), (X(a_) + 0.3, y0 - 3.2), (X(b_) - 0.3, y0 - 3.2), (X(b_) - 0.3, y0 - 3.9)],
                C["w4"], 0.35)
    wf = r28_text(pg, u"**floods** · Q100 / Q500 reach", X(0) + 0.3, y1, fs, C["w4"])
    k0, k1 = X(OCC_KERMES[0]), X(OCC_KERMES[1])
    pg.poly([rect(k0, y0 - 7.0, k1, y0 - 3.0)], fill=OCC_COL["kermes"], alpha=0.6)
    kt = u"**Kermes** · late Jun-early Jul"
    kx = k0 - 0.8 - r28_tw(kt, fs)
    if kx < X(0) + 0.3 + wf + 2.0:
        kx = k1 + 0.8
    r28_text(pg, kt, kx, y1, fs, OCC_COL["kermes"])
    for a_, b_ in occ_spans(SUBHUB_OPEN):
        pg.line([(X(a_) + 0.3, yh - 0.7), (X(a_) + 0.3, yh), (X(b_) - 0.3, yh), (X(b_) - 0.3, yh - 0.7)], OCC_HUB_COL,
                0.4)
        r28_text(pg, u"**in-bed sub-hub** open {}-{}".format(MONTHS[a_], MONTHS[b_ - 1]), X(b_) - 0.3, y2, fs,
                 COL["ink"], align="R")
    for a_, b_ in occ_spans([m for m in range(12) if m not in SUBHUB_OPEN]):
        pg.line([(X(a_) + 0.3, yh), (X(b_) - 0.3, yh)], OCC_HUB_COL, 0.2, dash=[0.8, 0.6])
        if text_w(u"closed", fs) < (b_ - a_) * mw - 2.0:
            pg.text(u"closed", (X(a_) + X(b_)) / 2.0, y2, fs, COL["ink2"], align="C")
    for m in range(12):
        pg.text(MONTHS[m], X(m + 0.5), y0 - 10.0, fs, COL["ink2"], align="C")
    # the left column: the title, the lanes' names and levels, the cut's small profile with the lane's band in ink
    pg.text(u"THROUGH THE YEAR", x_left, y0 - 3.2, 3.2, COL["ink_dark"], bold=True)
    pg.text(u"the cut's bands · Jan-Dec", x_left, y0 - 10.0, fs, COL["ink2"])
    lvs = []
    for ln in lanes:
        n = max(4, int(abs(ln["b"] - ln["a"]) / 0.25))
        zz = [S.surf(ln["a"] + (ln["b"] - ln["a"]) * i / float(n)) for i in range(n + 1)]
        if ln["key"] == "strip":
            lvs.append(u"{} · {} deep".format(u_level(min(zz)), u_height(E["STRIP"][2])))
        elif max(zz) - min(zz) < 0.02:
            lvs.append(u_level(max(zz)))
        else:
            lvs.append(u"{} to {}".format(u_level(max(zz)), u_level(min(zz))))
    tw = max(max(text_w(ln["name"], fs, True), text_w(lv, fs)) for ln, lv in zip(lanes, lvs))
    pw = 12.0
    px0 = XL - 2.5 - pw
    show = x_left + tw + 1.5 <= px0
    ps = [OCC_S[0] + (OCC_S[1] - OCC_S[0]) * i / 128.0 for i in range(129)]
    pz = [S.surf(s_) for s_ in ps]
    z0, z1 = min(pz), max(pz)
    for ln, lv in zip(lanes, lvs):
        pg.text(ln["name"], x_left, ln["top"] - 3.0, fs, COL["ink_dark"], bold=True)
        pg.text(lv, x_left, ln["top"] - 3.0 - fs * 1.2, fs, COL["ink2"])
        if show and z1 > z0:
            ph = max(1.5, min(3.0, L - 4.5))

            def pp(s_, z_, ln=ln, ph=ph):
                return (px0 + (OCC_S[0] - s_) / (OCC_S[0] - OCC_S[1]) * pw, ln["bot"] + 0.9 + (z_ - z0) / (z1 - z0) * ph)
            pg.line([pp(s_, z_) for s_, z_ in zip(ps, pz)], C["structure"], 0.12)
            pg.line([pp(s_, z_) for s_, z_ in zip(ps, pz) if ln["b"] <= s_ <= ln["a"]], COL["ink_dark"], 0.4)
    # feel · hear · touch: a few words a season (design intention), under the lanes
    ys = ybot - 0.8
    pg.text(u"FEEL · HEAR · TOUCH", x_left, ys - fs, fs, COL["ink_dark"], bold=True)
    pg.text(u"design intention, ours", x_left, ys - fs * 2.25, fs, COL["ink2"])
    for key, a_, b_ in segs:
        r28_para(pg, X(a_) + 0.8, ys + fs * 0.28, (b_ - a_) * mw - 1.6, sense_text(key), fs, COL["ink"])
    r28_para(pg, X(11) + 0.8, ys + fs * 0.28, mw - 1.6, u"**winter**: as Jan-Feb", fs, COL["ink"])   # Dec
    for m in (2, 5, 8, 11):
        pg.line([(X(m), ybot), (X(m), ybot - hs + 0.6)], C["structure"], 0.12)
    # the key at the right of the lanes
    lx = XR + 6.0
    kw_ = max(24.0, x_right - lx)                       # within the cut's own width (the panel is as wide as the cell)
    y = y0

    def head(t, y):
        pg.text(t, lx, y - fs, fs, COL["ink_dark"], bold=True)
        return y - fs * 1.55

    def entry(y, words):
        return min(y - 3.1, r28_para(pg, lx + 7.5, y + fs * 0.25, kw_ - 7.5, words, fs, COL["ink"]) - 0.5)
    y = head(u"WHO", y)
    for g, name, col in OCC_GROUPS:
        pg.poly([rect(lx, y - 2.6, lx + 6.0, y - 0.2)], fill=col, stroke=col, lw=0.1, alpha=OCC_ALPHA)
        y = entry(y, name)
    y = head(u"WATER", y - 0.8)
    pg.poly([rect(lx, y - 2.6, lx + 6.0, y - 0.2)], fill=C["w1"], alpha=0.6)
    pg.line([(lx, y - 0.2), (lx + 6.0, y - 0.2)], C["w2"], 0.2)
    y = entry(y, u"season water on this cut, **calculated**")
    pg.poly([rect(lx, y - 2.6, lx + 6.0, y - 0.2)], fill=None, stroke=C["w4"], lw=0.1,
            stripes=(C["w4"], 0.9, 0.12, 45.0))
    y = entry(y, u"**flood reach** in winter: Q500, Q100 dashed")
    y = head(u"FREE TIME", y - 0.8)
    pg.poly([rect(lx, y - 2.6, lx + 6.0, y - 0.2)], fill=COL["white"], stroke=COL["faint"], lw=0.1,
            stripes=(COL["ink2"], 1.1, 0.12, 0.0, True))
    y = entry(y, u"**shareable** time")
    pg.poly([rect(lx, y - 2.6, lx + 6.0, y - 0.2)], fill=None, stroke=COL["faint"], lw=0.1)
    for dx in (1.0, 2.5, 4.0, 5.5):
        for dy in (0.9, 2.0):
            pg.circle(lx + dx - 0.25, y - dy, 0.15, fill=COL["ink2"])
    y = entry(y, u"**open** to new programmes")
    pg.line([(lx, y - 1.0), (lx + 2.8, y - 1.0)], OCC_HUB_COL, 0.4)
    pg.line([(lx + 3.4, y - 1.0), (lx + 6.0, y - 1.0)], OCC_HUB_COL, 0.2, dash=[0.8, 0.6])
    y = entry(y - 0.8, u"in-bed **sub-hub** open · closed")
    y = r28_para(pg, lx, y - 0.6, kw_, u"band thickness = how busy: **design assumption**, ours", fs, COL["ink2"])
    return min(ybot - hs, y) - 0.5
