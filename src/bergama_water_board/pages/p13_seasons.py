# booklet p13 "Four seasons on one cut" (v18, round 7, S4, 5 Nov 2026; BRIEF §6 row 13, PLAN §3 row 13).
# v18 (G7-1 ACCURATE, target refs/targets/r06_S03_four_seasons_one_cut_accurate_BEST.png): the cut is again the
# 28 Oct one: the detail engine's S4 south-west bank (DETAIL_SRC SECTIONS[0], s 538-598) drawn by the ported
# f93d84b engine_section / draw_s4_season / sky_labels / level_ladder (f93d84b:src/bergama_water_board/code.py
# 1260-1366, 1436-1478) at 1:500 (P14_DEN, fixed, L1), four rows stacked so the bank lines up. Every level it draws is
# today's: bed, Q100, Q500 and each season's mean from the level module (_p14_geo), the promenade P14_PROM, the strip
# depth STRIP_DEPTH; none copied from the 28 Oct drawing (BRIEF §5). Kept from v16: the left column, month bar, hub
# key, FEEL · HEAR · TOUCH, the animal column (GBIF, compact, right). Key map: km_keymap S4 at the SON page15 frame
# 94.5 x 28.4 mm, north left (G7-3). Language: ACCURATE (log `section p13 S4 ACCURATE <season>`).
# Earlier (v16, round 6): the 28 Oct column restored on p14's whole cut _p14_cut (P14_RANGE): replaced by v18.
# build_board: p13_page(pg, box, opt, log) in place of p14_page (same arguments, same returned crop).
# Included after pages/p14_15_s4.py (uses its _p14_* functions and P14_* / P15_* tables).

P13_TAG_W = 40.0                     # the season column at the left, mm (f93d84b TAG_W)
P13_GAP = 2.5                        # between the columns, mm (f93d84b SEASON_GAP)
P13_FEEL_W = 42.0                    # FEEL · HEAR · TOUCH, mm (f93d84b SENSE_MIN 40)
P13_ANIM_W = 38.0                    # the animals on record, mm (frames: x 87-96.7 of A3 = 41 mm)
P13_HEAD_H = 19.0                    # the top row: sub-hub key and month bar, mm
P13_KEY = (94.5, 28.4)               # v18 (G7-3, PLAN §3 row 13): the SON page15 key-map frame, mm (exactly)
P13_POCHE = 0.6                      # soil drawn under the strip, m (f93d84b S4_POCHE, drawing value)
P13_DROP = ("title", "callouts", "dimensions", "band", "survey", "text")   # engine layers left out (f93d84b)
P13_BAND_HUE = {"winter": ("WAT", 3), "spring": ("WAT", 2), "summer": ("WAT", 1), "autumn": ("WAT", 2)}   # G6-6:
#                                      the rule over each season's column (was BAND_BLUE)
P13_MONTH_HUE = dict(open=("PUB", 4), closed=("WAT", 2), kermes=("PUB", 1), high=("WAT", 1))   # G6-6: the month bar
#                                      (the bed open to people = public life PUB; high water = WAT)
P13_HEAD = {  # the season's state of the water store (f93d84b S4_SEASON head; design, ours)
    "winter": u"storage fills", "spring": u"storage full by end of April", "summer": u"strip runs on stored water",
    "autumn": u"storage low until the rains"}
P13_WORDS = {  # what people do, set over the place on the south-west bank (f93d84b S4_SEASON words, our design /
    # concept v1 §10.1): (s along S4 m, text) on the engine's section; {prom} = P14_PROM over Q500, {strip} =
    # STRIP_DEPTH, both live (v18: back to the 28 Oct places, the cut is the 28 Oct bank again)
    "winter": [(553.0, u"sit at the edge · watch the floods"), (563.0, u"terraces open between storms"),
               (586.0, u"marsh flooded · birds")],
    "spring": [(563.0, u"boardwalk open"), (586.5, u"children at the water's edge")],
    "summer": [(577.0, u"walk in the dry stream bed"), (583.0, u"Kermes stalls in the bed"),
               (589.85, u"feet in the strip · {strip} m")],
    "autumn": [(579.0, u"walk the gravel bed to the water"), (592.0, u"first-flush cleaning")],
}
P13_PROM_WORD = (552.5, u"raised walk {prom} m over Q500")   # winter only, at the promenade level (f93d84b)
P13_ACT_SRC = (u"concept/Selinos_riverfront_design_concept_v1.md §10.1 (design: life on the bands by season); detail "
               u"section v2 season texts")
P13_KERMES_SRC = (u"h01 §2.8: Bergama Kermesi since 1937, 90th edition 29 Jun-5 Jul 2026 (s60, s100); h03 Q5: 2024 "
                  u"concerts in Kızıl Avlu and events at the Arasta, by the stream")
P13_TOUCH_SRC = (u"history_phase1/DECISIONS.md D9: water people touch is UV-disinfected; " + REG +
                 u" EN-D3, EN-E1, EN-E2")
# FEEL / HEAR / TOUCH: what we design each season to feel, sound and touch like (design intentions, ours; no
# measurement) and the left column's pictograms (f93d84b SEASON_USE)
P13_USE = {
    "winter": dict(water=("flood", u"high water"), acts=("sit", "watch"),
                   feel=("awe", u"awe at its force"), hear=("snd3", u"rushing water"), touch=("watch", u"look, keep back"),
                   extra=("tunnel", u"the Roman tunnels at work", TUNNEL_SRC)),
    "spring": dict(water=("rain", u"water falling"), acts=("walk", "child"),
                   feel=("curious", u"curiosity, new green"), hear=("snd2", u"running water, birds"),
                   touch=("hand", u"hands at the edge")),
    "summer": dict(water=("strip", u"low water, strip"), acts=("walk", "wade", "stall"),
                   feel=("joy", u"play, cool shade"), hear=("snd1", u"trickle and voices"),
                   touch=("foot", u"feet in UV-clean water", P13_TOUCH_SRC),
                   extra=("stall", u"Kermes in the dry bed", P13_KERMES_SRC)),
    "autumn": dict(water=("dry", u"low water"), acts=("walk", "sit"),
                   feel=("calm", u"calm, waiting for rain"), hear=("snd1", u"reeds rustle, first rain"),
                   touch=("gravel", u"gravel underfoot")),
}


def _p13_icon(pg, kind, x, y, sz):
    """code.py icon(), plus the people and stall pictograms it lost after 28 Oct (f93d84b icon 2585-2606: sit, walk,
    wade, child, stall; graphic only) in the square (x, y - sz)-(x + sz, y)"""
    if kind not in ("sit", "walk", "wade", "child", "stall"):
        icon(pg, kind, x, y, sz)
        return
    u = sz / 10.0
    lw = 0.07 * sz
    ink = C["dark"]

    def P(pts):
        return [(x + a * u, y - sz + b * u) for a, b in pts]

    def R(a0, b0, a1, b1):
        return P([(a0, b0), (a1, b0), (a1, b1), (a0, b1)])
    if kind == "sit":                                       # sitting on an edge, legs over it
        pg.poly([R(0.4, 0.4, 4.6, 4.2)], fill=C["structure"])
        pg.circle(x + 4.2 * u, y - sz + 8.6 * u, 1.2 * u, fill=ink)
        pg.line(P([(4.0, 7.2), (3.6, 4.6), (6.6, 4.6), (7.0, 1.2)]), ink, lw * 1.6)
    elif kind == "stall":                                   # a festival stall (the Kermes)
        pg.poly([P([(1.0, 6.2), (5.0, 9.4), (9.0, 6.2)])], fill=hue("PUB", 1))
        pg.poly([R(1.6, 0.6, 8.4, 6.2)], fill=COL["white"], stroke=ink, lw=lw)
        pg.poly([R(3.6, 0.6, 6.4, 4.0)], fill=hue("PUB", 3))
    else:
        k_ = 0.75 if kind == "child" else 1.0
        pg.circle(x + 5.0 * u, y - sz + (1.2 + 7.4 * k_) * u, 1.2 * k_ * u, fill=ink)
        pg.line(P([(5.0, 1.2 + 6.1 * k_), (5.0, 1.2 + 3.2 * k_)]), ink, lw * 1.6)
        pg.line(P([(3.4, 1.2), (5.0, 1.2 + 3.2 * k_), (6.6, 1.2)]), ink, lw * 1.6)
        pg.line(P([(3.4, 1.2 + 4.0 * k_), (5.0, 1.2 + 5.6 * k_), (6.8, 1.2 + 4.4 * k_)]), ink, lw * 1.2)
        if kind == "wade":
            pg.poly([R(0, 0.2, 10, 2.4)], fill=hue("WAT", 3), alpha=0.85)


def _p13_hub_words(sea):
    """the in-bed sub-hub this season (f93d84b subhub_words): (pictogram, words) from SUBHUB_OPEN"""
    ms = [m for m in S4_MONTH_IDX[sea] if m in SUBHUB_OPEN]
    if not ms:
        return "hub_closed", u"in-bed hub closed"
    if len(ms) == 3:
        return "hub_open", u"in-bed hub open"
    return "hub_open", u"in-bed hub open " + u", ".join(MONTHS[m] for m in ms)


def _p13_bb(pg, n0, pad=0.6):
    """the box of pg.items[n0:] (board mm) a little wider, for wbx_drawing"""
    b = _p14_bb(pg.items[n0:])
    return (b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad)


def _p13_hubkey(pg, x, y):
    """the in-bed sub-hub key (f93d84b month_strip's left part): its pictogram, name and open months. Returns bottom"""
    fs = FS_MIN
    with pg.g("legend", u"in-bed sub-hub key"):
        _p13_icon(pg, "hub_open", x, y, 5.6)
        para(pg, x + 7.0, y + 3.2 * 0.2, P13_TAG_W - 9.0, u"IN-BED SUB-HUB", 3.2, COL["ink_dark"], bold=True)
        pg.text(u"open " + _p15_open(), x, y - 9.2, fs, COL["ink2"], bold=True)
    return y - 9.2 - fs


def _p13_monthbar(pg, gx, y, gw, page):
    """the year in 12 cells over the cut's width from gx (f93d84b month_strip): the in-bed sub-hub open (SUBHUB_OPEN:
    PUB r4) or closed (WAT r2), the Kermes week (P15_KERMES), the high-water months (the months the bed is closed)
    when the Roman tunnels carry the stream. Returns bottom y"""
    fs = FS_MIN
    cw = gw / 12.0
    yc = y - 0.5
    for m in range(12):
        op = m in SUBHUB_OPEN
        with pg.g("annotations", u"month %s · %s" % (MONTHS[m], u"bed open" if op else u"bed closed")):
            pg.poly([rect(gx + m * cw + 0.3, yc - 5.0, gx + (m + 1) * cw - 0.3, yc)],
                    fill=hue(*P13_MONTH_HUE["open" if op else "closed"]))
            pg.text(MONTHS[m], gx + (m + 0.5) * cw, yc - 3.6, fs, COL["ink_dark"] if op else COL["white"], bold=True,
                    align="C")
    xk, xk1 = gx + P15_KERMES[0] * cw, gx + P15_KERMES[1] * cw
    tk = u"Kermes " + cite(P13_KERMES_SRC)
    with pg.g("annotations", u"Kermes week"):
        pg.poly([rect(xk, yc - 6.2, xk1, yc - 5.4)], fill=hue(*P13_MONTH_HUE["kermes"]))
        _p13_icon(pg, "stall", xk - 2.0, yc - 6.8, 4.6)
        pg.text(tk, xk + 3.4, yc - 10.3, fs, hue(*P13_MONTH_HUE["kermes"]), bold=True)
    yb = yc - 6.2
    closed = [m for m in range(12) if m not in SUBHUB_OPEN]
    hc = hue(*P13_MONTH_HUE["high"])
    tt = u"high water: the Roman tunnels at work " + cite(TUNNEL_SRC)
    with pg.g("annotations", u"high water months"):
        for a_, b_ in occ_spans(closed):
            pg.line([(gx + a_ * cw + 0.5, yb), (gx + a_ * cw + 0.5, yb - 1.2), (gx + b_ * cw - 0.5, yb - 1.2),
                     (gx + b_ * cw - 0.5, yb)], hc, 0.35)
        _p13_icon(pg, "tunnel", gx, yb - 2.0, 4.6)
        pg.text(tt, gx + 5.6, yb - 5.6, fs, hc, bold=True)
    return min(yb - 8.0, y - 10.5)


def _p13_tag(pg, x, y, sea):
    """the season's column (f93d84b season_tag): the coloured rule, name, months · the store's state, the water's state,
    what people do (pictograms), the in-bed hub, and (winter, summer) the season's story. Returns bottom y"""
    fs = FS_MIN
    w = P13_TAG_W - 2.0
    use = P13_USE[sea]
    with pg.g("labels", u"%s column" % sea):
        pg.poly([rect(x, y - 1.0, x + w, y)], fill=hue(*P13_BAND_HUE[sea]))
        pg.text(sea.upper(), x, y - 6.4, 5.0, COL["ink_dark"], bold=True)
        yy = para(pg, x, y - 7.4, w, S4_MONTHS[sea] + u" · " + P13_HEAD[sea], fs, COL["ink2"], bold=True) - 1.4
        _p13_icon(pg, use["water"][0], x, yy, 5.6)
        pg.text(use["water"][1], x + 7.0, yy - 3.6, fs, hue("WAT", 1), bold=True)
        yy -= 7.2
        for j, kind in enumerate(use["acts"]):
            _p13_icon(pg, kind, x + j * 8.0, yy, 7.0)
        ca = cite(P13_ACT_SRC)
        if ca:
            pg.text(ca, x + len(use["acts"]) * 8.0 + 0.4, yy - 4.4, fs, COL["ink2"])
        yy -= 8.8
        kind, words = _p13_hub_words(sea)
        _p13_icon(pg, kind, x, yy, 5.6)
        yy = para(pg, x + 7.0, yy + fs * 0.2, w - 7.0, words, fs, COL["ink"], bold=True) - 1.6
        if use.get("extra"):
            kind, words, src = use["extra"]
            _p13_icon(pg, kind, x, yy, 5.6)
            col = hue("PUB", 1) if kind == "stall" else hue("WAT", 1)
            yy = para(pg, x + 7.0, yy + fs * 0.2, w - 7.0, (words + u" " + cite(src)).strip(), fs, col,
                      bold=True) - 1.0
    return yy


def _p13_senses(pg, x, y, sea, w):
    """FEEL / HEAR / TOUCH of one season in a column w wide (f93d84b senses): three pictograms and their words from
    the top y. Returns bottom y"""
    fs = FS_MIN
    use = P13_USE[sea]
    for slot in ("feel", "hear", "touch"):
        kind, words = use[slot][0], use[slot][1]
        with pg.g("labels", u"%s %s · %s" % (sea, slot, words)):
            _p13_icon(pg, kind, x, y, 6.4)
            t = (words + (u" " + cite(use[slot][2]) if len(use[slot]) > 2 else u"")).strip()
            yy = para(pg, x + 8.0, y + fs * 0.2, w - 8.0, t, fs, COL["ink"])
        y = min(y - 7.6, yy - 1.2)
    return y


def _p13_animals(pg, x, ytop, w, h, sea, page):
    """the animals on record this season (the GBIF list of P14_FAUNA, _p14_fauna_for): pictogram and name, one under
    the other from the band's top (round 5's _p14_animals, kept as one compact column, Q2 b)"""
    sel = _p14_fauna_for(sea)
    if not sel:
        return
    pitch = min(5.6, h / float(len(sel)))
    sz = min(4.4, pitch - 0.6)
    for i, fa in enumerate(sel):
        cy = ytop - pitch * (i + 0.5)
        with pg.g("legend", u"%s · %s" % (sea, fa["name"])):
            _p14_fauna(pg, fa["key"], x + sz / 2.0, cy, sz)
            pg.text(fa["name"], x + sz + 1.0, cy - FS_MIN * 0.35, FS_MIN, COL["ink_dark"])


def _p13_from_engine(items, sea):
    """the detail engine's Page items in this board's form (f93d84b from_engine), each tagged as one element of its
    engine layer (G6-9: trees, plants, people, water, section)"""
    kind = {"trees": "trees", "tree_shadows": "trees", "planting": "plants", "entourage": "people",
            "people": "people", "handrail": "structures", "concrete": "structures", "levels": "water",
            "water": "water"}
    out = []
    for it in items:
        k = it[0]
        if k == "poly":
            _, rings, fill, stroke, lw, dash, layer, join, stripes, alpha = it
            o = ("poly", rings, fill, stroke, lw, dash, stripes, alpha)
        elif k == "line":
            _, pts, stroke, lw, dash, layer, cap = it
            o = ("line", pts, stroke, lw, dash, cap)
        elif k == "circle":
            _, cx, cy, r, fill, stroke, lw, layer = it
            o = ("circle", cx, cy, r, fill, stroke, lw)
        else:
            continue                                  # engine texts: none kept (P13_DROP takes its text layers)
        out.append(o)
        _GRP[id(o)] = (o, u"%s/S4 %s · %s" % (kind.get(layer, "section"), sea, layer))
    return out


def _p13_engine_cut(sea, log=None):
    """one season of the S4 south-west bank by the detail engine at 1:P14_DEN (f93d84b engine_section +
    draw_s4_season), its levels set from today's data for this draw only (bed, Q100, Q500 = _p14_geo; DRY = P14_PROM;
    strip depth = STRIP_DEPTH; the season's water = its mean from the level module) and set back after.
    Returns (items at the engine's origin, S, G, E)."""
    E = detail_engine()
    prof = s4_profile(E, log)
    G = _p14_geo(log)
    d0 = E["SECTIONS"][0]
    old_dry = E["DRY"]
    d = dict(d0)                                          # the promenade surfaces on today's promenade level
    d["surfaces"] = [tuple(P14_PROM if (j_ == 2 and isinstance(v_, float) and abs(v_ - old_dry) < 1e-6) else v_
                           for j_, v_ in enumerate(srf)) if srf[0] != "steps" else srf for srf in d0["surfaces"]]
    sea0 = [x_ for x_ in E["SEASONS"] if x_["key"] == sea][0]
    sd = dict(sea0)
    sd["water"] = [(G["levels"][sea], True, u"%s mean %%+.2f" % S4_MONTHS[sea], None)]   # engine does lab % z
    keys = ("SCALE", "K", "level_line", "Q100", "Q500", "THALWEG", "DRY", "STRIP")
    keep = dict((k_, E[k_]) for k_ in keys)
    keep_sea = dict(E["SEA"])
    skip = () if sea == "winter" else (G["q100"], G["q500"])
    orig = E["level_line"]

    def ll(pg_, S_, z, label, dash, colour=E["FLOOD"]):
        if any(abs(z - q) < 1e-6 for q in skip):
            return
        orig(pg_, S_, z, label, dash, colour)
    try:
        E["SCALE"], E["K"] = P14_DEN, 1000.0 / P14_DEN
        E["level_line"] = ll
        E["Q100"], E["Q500"] = G["q100"], G["q500"]
        E["THALWEG"] = (keep["THALWEG"][0], G["bed"])
        E["DRY"] = P14_PROM
        E["STRIP"] = (keep["STRIP"][0], keep["STRIP"][1], STRIP_DEPTH)
        E["SEA"].clear()
        E["SEA"].update(E["SEASON_LOOK"][sea])
        epg = E["Page"]("s4", sea)
        S = E["Sec"](d, prof)
        S.zb = G["bed"] - STRIP_DEPTH - P13_POCHE
        E["draw_section"](epg, S, 0.0, 0.0, [], sd)
    finally:
        for k_ in keys:
            E[k_] = keep[k_]
        E["SEA"].clear()
        E["SEA"].update(keep_sea)
    k = 1000.0 / P14_DEN
    S.X = lambda s_: S.X0 + (s_ - d["s_from"]) * S.dir * k
    S.Y = lambda z_: S.Y0 + (z_ - S.zb) * k
    S.P = lambda s_, z_: (S.X(s_), S.Y(z_))
    lay = {"poly": 6, "line": 5, "circle": 7, "text": 8}
    its = [it for it in epg.items if it[lay[it[0]]] not in P13_DROP]
    return _p13_from_engine(its, sea), S, G, E


def _p13_thalweg_s():
    """s along S4 of the bed's low point in the engine (DETAIL_SRC THALWEG[0], survey), m"""
    return detail_engine()["THALWEG"][0]


def _p13_skyline(items, x0, x1, step=1.0):
    """highest drawn point (board y) in every step-wide column from x0 to x1 (f93d84b skyline; p14 has its own)"""
    n = int((x1 - x0) / step) + 2
    top = [-1e9] * n

    def put(x, y):
        i = int((x - x0) / step)
        if 0 <= i < n and y > top[i]:
            top[i] = y

    def seg(p, q):
        m = max(1, int(abs(q[0] - p[0]) / step) + 1)
        for j in range(m + 1):
            t = j / float(m)
            put(p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    for it in items:
        if it[0] == "poly":
            for r in it[1]:
                for i in range(len(r)):
                    seg(r[i], r[(i + 1) % len(r)])
        elif it[0] == "line":
            for i in range(len(it[1]) - 1):
                seg(it[1][i], it[1][i + 1])
        elif it[0] == "circle":
            put(it[1], it[2] + it[3])
    return lambda a, b: max(top[max(0, int((a - x0) / step)):max(1, int((b - x0) / step) + 1)] or [-1e9])


def _p13_sky_labels(pg, labs, items, x_lo, x_hi, y_cap, fs, boxes=None):
    """short labels in the open sky over the cut, each as low as it fits over what is drawn under it and clear of
    the others, a thin leader to its anchor (f93d84b sky_labels). labs = [(ax, ay, text, colour)]"""
    sky = _p13_skyline(items, x_lo - 60.0, x_hi + 60.0)
    boxes = boxes if boxes is not None else []
    h = fs * 1.25 * BK_GROW
    for ax, ay, t, colour in sorted(labs, key=lambda t_: t_[0]):
        w = text_w(t, fs, True) * BK_GROW + 0.8
        best = None
        for x0 in (ax - 1.0, ax - w + 1.0, ax - w / 2.0):
            x0 = max(x_lo, min(x0, x_hi - w))
            y = max(sky(x0, x0 + w) + 1.2, ay + 1.5)
            while y + h < y_cap + 30.0:
                if not any(x0 < b[2] and b[0] < x0 + w and y < b[3] and b[1] < y + h for b in boxes):
                    break
                y += 0.5
            if best is None or y < best[1]:
                best = (x0, y)
        x0, y = best
        boxes.append((x0, y, x0 + w, y + h))
        with pg.g("labels", t):
            pg.text(t, x0 + 0.4, y + h - BK_GROW * fs * 1.25 * 0.8, fs, colour, bold=True)
            lx = min(max(ax, x0 + 0.6), x0 + w - 0.6)
            pg.line([(ax, ay), (lx, y - 0.3)], COL["ink2"], 0.1)
            pg.circle(ax, ay, 0.35, fill=COL["ink"])
    return boxes


def _p13_ladder(pg, entries, x_line, x_text, fs, boxes=None, lo=None):
    """the levels at the cut's right end (f93d84b level_ladder): [(board y, text, colour, bold)], texts spread
    apart, leaders from the level's end at x_line"""
    entries = sorted(entries, key=lambda e: e[0])
    ly = spread([e[0] - fs * 0.35 for e in entries], fs * 1.25 * BK_GROW, lo=lo)
    for (y, t, colour, bold), yl in zip(entries, ly):
        with pg.g("levels", t):
            pg.line([(x_line, y), (x_text - 2.0, yl + fs * 0.35), (x_text - 0.6, yl + fs * 0.35)], colour, 0.12)
            pg.text(t, x_text, yl, fs, colour, bold=bold)
        if boxes is not None:
            boxes.append((x_text, yl - fs * 0.3, x_text + text_w(t, fs, bold) * BK_GROW, yl + fs * BK_GROW))


def _p13_season_cut(sea, log=None):
    """one season row's cut (f93d84b draw_s4_season, ACCURATE): the engine's bank and the season's water, its levels
    as values with ▽ at the right end (bed, the season's mean, the strip in summer / autumn, Q100 / Q500 in winter;
    all today's values), the season's activities set in the sky with leaders. Returns (Page, S, G)"""
    items, S, G, E = _p13_engine_cut(sea, log)
    d = S.d
    bed = G["bed"]
    fs = FS_MIN
    pg = Page(0, 0)
    pg.items = items
    xr = S.X(d["s_to"])
    bb = items_bbox(items)
    boxes = []
    fl = E["FLOOD"]
    lv = [(S.Y(bed), u"{:+.2f} bed".format(bed), COL["ink"], False),
          (S.Y(G["levels"][sea]), u"{:.2f} m {} mean".format(G["levels"][sea] - bed, S4_MONTHS[sea]), fl, True)]
    if sea in ("summer", "autumn"):
        a_, b_ = E["STRIP"][0], E["STRIP"][1]
        lv.append((S.Y(bed) + 0.01, u"strip {:.1f} x {:.2f} m".format(abs(b_ - a_), STRIP_DEPTH), fl, True))
    if sea == "winter":
        lv += [(S.Y(G["q100"]), u"{:.2f} m Q100".format(G["q100"] - bed), fl, True),
               (S.Y(G["q500"]), u"{:.2f} m Q500".format(G["q500"] - bed), fl, True)]
    _p13_ladder(pg, lv, xr + 0.5, xr + 6.0, fs, boxes, lo=bb[1] + 1.0)
    fmt = dict(prom=u"{:.2f}".format(P14_PROM - G["q500"]), strip=u"{:.2f}".format(STRIP_DEPTH))
    labs = [(S.X(s_), S.Y(S.surf(s_) + 0.05), t.format(**fmt), COL["ink_dark"]) for s_, t in P13_WORDS[sea]]
    if sea == "winter":
        labs.append((S.X(P13_PROM_WORD[0]), S.Y(P14_PROM), P13_PROM_WORD[1].format(**fmt), fl))
    _p13_sky_labels(pg, labs, items, S.X(d["s_from"]), xr + 24.0, bb[3], fs, boxes)
    if log is not None:
        log.append(u"p13 {}: {} activities named on the cut, {} levels at its right end".format(
            sea, len(labs), len(lv)))
    return pg, S, G


def _p13_panel(pg, box, log, style):
    """booklet p13 (board page WBX_PG_SEASONS, round 6 id p13) drawn into box on the board as a recorder, every part
    handed to the booklet as its own item (crop "wb_s4_seasons"): p15_hubkey, p15_monthbar (diagrams, mm), per season
    p15_season_<season> (one row: the left column and the S4 cut at 1:500; x = m across S4 from the bed's low point,
    y = m a.s.l.; v18: the 28 Oct engine's south-west bank, its levels drawn at its right end), p15_feel and p15_animals (one column each over the four rows),
    p15_keymap (km_keymap). Returns its bbox."""
    x0, y0, x1, y1 = box
    n0 = len(pg.items)
    page = WBX_PG_SEASONS
    npg = wbx_p(page)
    crop = "wb_s4_seasons"
    G = _p14_geo(log)
    k = 1000.0 / P14_DEN
    cuts = dict((sea, _p13_season_cut(sea, log)) for sea in SEAS)   # v18: the 28 Oct engine cut, today's levels
    bbs_ = [items_bbox(cuts[sea][0].items) for sea in SEAS]
    cx0, foot = min(b_[0] for b_ in bbs_), min(b_[1] for b_ in bbs_)
    wb = max(b_[2] for b_ in bbs_) - cx0         # the cut with its level values, the same for all four
    xa = x0
    xb = xa + P13_TAG_W + P13_GAP                # the cuts' band: the same x for all four (the bank lines up)
    xl = xb + wb
    xf = xl + P13_GAP                            # FEEL · HEAR · TOUCH
    xn = xf + P13_FEEL_W + P13_GAP               # the animals
    yt = y1 - 2.0
    yh = yt - P13_HEAD_H                         # the season rows start here
    rh = (yh - y0) / 4.0
    _p14_keymap(page, P13_KEY, u"p15_keymap", log)
    # the top row: the in-bed sub-hub key over the left column, the month bar over the cuts
    nh = wbx_mark(pg)
    _p13_hubkey(pg, xa, yt)
    wbx_drawing(u"p15_hubkey", page, pg, _p13_bb(pg, nh), n0=nh, dkind="diagram", group=u"p15_hubkey", crop=crop)
    nm = wbx_mark(pg)
    _p13_monthbar(pg, xb, yt, wb, page)
    wbx_drawing(u"p15_monthbar", page, pg, _p13_bb(pg, nm), n0=nm, dkind="diagram", group=u"p15_monthbar",
                crop=crop)
    for i, sea in enumerate(SEAS):
        rt = yh - i * rh
        rbot = rt - rh
        ns = wbx_mark(pg)
        yc = _p13_tag(pg, xa, rt - 1.0, sea)
        yb = rbot + 1.5
        # ACCURATE (G7-1, target r06_S03): the 28 Oct S4 south-west bank at true scale 1:500 (P14_DEN, fixed),
        # thin cut, light soil without hatch, library people (r28_people), the season's plants and water, levels as
        # values with ▽ at the right end, short activity words over their place; Q100 / Q500 on the winter cut only
        cpg, S, _G = cuts[sea]
        dx, dy = xb - cx0, yb - foot             # the cut stands on its row (all four on one x)
        pg.items += xform(cpg.items, 1.0, dx, dy)
        top = items_bbox(cpg.items)[3] + dy
        did = u"p15_season_" + sea
        ybb = min(rbot, yc - 0.5)                # v17 (L4): a season column taller than its row is exported whole
        bbs = (xa, ybb, xl, max(rt, top + 0.3))
        # origin: x = m across S4 from the bed's low point (THALWEG s), y = m a.s.l. at the box's lower left
        s_at = S.d["s_from"] + (xa - (S.X(S.d["s_from"]) + dx)) / k
        z_at = S.zb + (ybb - (S.Y0 + dy)) / k
        wbx_drawing(did, page, pg, bbs, n0=ns, den=P14_DEN, origin=(s_at - _p13_thalweg_s(), z_at),
                    dkind="section", scale_pref=[int(P14_DEN)], title=sea.upper(), group=did, crop=crop)
        if log is not None:
            log.append(u"section {} S4 ACCURATE {}".format(npg, sea))
            log.append(u"scale {} {} 1:{:.0f}".format(npg, did, P14_DEN))
    # FEEL · HEAR · TOUCH and the animals: one column each, every season's part at its row's top
    nf = wbx_mark(pg)
    na = None
    ylo = yh - 4.0 * rh
    for i, sea in enumerate(SEAS):
        rt = yh - i * rh
        yy = _p13_senses(pg, xf, rt - 1.0, sea, P13_FEEL_W)
        ylo = min(ylo, yy - 0.5)                 # v17 (L4): the column's box holds every word (none cut off)
    wbx_drawing(u"p15_feel", page, pg, (xf - 0.5, ylo, xf + P13_FEEL_W + 0.5, yh), n0=nf, dkind="diagram",
                group=u"p15_feel", crop=crop)
    na = wbx_mark(pg)
    for i, sea in enumerate(SEAS):
        rt = yh - i * rh
        _p13_animals(pg, xn, rt - 1.0, P13_ANIM_W, rh - 2.0, sea, page)
    wbx_drawing(u"p15_animals", page, pg, (xn - 0.5, yh - 4.0 * rh, xn + P13_ANIM_W + 0.5, yh), n0=na,
                dkind="diagram", group=u"p15_animals", crop=crop)
    # the page's texts (booklet texts; nothing drawn on the board)
    wbx_text(page, u"One cut through the year: the water level decides where people can be and what they do there.",
             "intro", did=u"p15_monthbar", group=u"p15_monthbar")
    wbx_text(page, u"FEEL · HEAR · TOUCH", "heading", did=u"p15_feel", group=u"p15_feel")
    wbx_text(page, u"design intention, ours", "caption", did=u"p15_feel", group=u"p15_feel")
    wbx_text(page, u"ANIMALS ON RECORD · GBIF", "heading", did=u"p15_animals", group=u"p15_animals")
    wbx_text(page, u"Animals on record: GBIF " + u"".join(cite(s_) for s_ in P14_FAUNA_SRC), "source",
             did=u"p15_animals", group=u"p15_animals")
    wbx_text(page, u"S4, south-west bank: what the seasons change · 1:500", "caption",
             did=u"p15_season_autumn", group=u"p15_season_autumn")
    bb = _p14_bb(pg.items[n0:])
    if log is not None:
        if G["src"] not in log:
            log.append(G["src"])
        _p14_hue_log(page, log)
        log.append(u"p13 four seasons (r06_S03, 28 Oct engine): S4 south-west bank s {:.0f}-{:.0f} m at 1:{:,.0f}, "
                   u"rows {:.1f} mm, cut band {:.0f} mm; bed {:+.2f}, Q100 {:+.2f}, Q500 {:+.2f}, promenade {:+.2f}; "
                   u"bed open {} (SUBHUB_OPEN)".format(
                       detail_engine()["SECTIONS"][0]["s_from"], detail_engine()["SECTIONS"][0]["s_to"], P14_DEN,
                       rh, wb, G["bed"], G["q100"], G["q500"], P14_PROM, _p15_open()))
    return bb


def p13_page(pg, box, opt, log):
    """booklet p13 "Four seasons on one cut", drawn into box (x0, y0, x1, y1), board mm, and handed to the booklet as
    items (WBX_PG_SEASONS). Returns its crop [(crop id, bbox, scale denominator)] as p14_page did (the drawings
    registered with crop="wb_s4_seasons" replace it in the export)."""
    tri = sf_triangles(walls=False, aggregate=False)          # G14 / U22: no meaningless triangles in the cuts
    try:
        bb = _p13_panel(pg, box, log, "a")   # lead: style a, as p11, p12, p17 (Aras 31 Oct 08:46)
    finally:
        sf_triangles(**tri)
    return [("wb_s4_seasons", bb, P14_DEN)]
