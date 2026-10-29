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


def r28_draw_runs(pg, runs, x, y, size, colour, kcol=None, halo=None):
    for t, b in runs:
        pg.text(t, x, y, size, (kcol or colour) if b else colour, bold=b, halo=halo)
        x += text_w(t, size, b)
    return x


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


