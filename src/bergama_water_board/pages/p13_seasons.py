# booklet p13 "Four seasons on one cut" (v16, round 6, S5 helper, 4 Nov 2026; BRIEF §6 row 13, Q2 b, PLAN P-11).
# The 28 Oct four seasons (f93d84b:src/bergama_water_board/code.py draw_seasons_panel 1550-1590, draw_s4_season
# 1436-1476, senses 1479-1488, season_tag 1491-1516, month_strip 1519-1547, subhub_words 1426, S4_SEASON, SEASON_USE,
# ACT / KERMES / TOUCH_SRC, the people pictograms of icon 2585-2606) restored on today's S4: the cut is
# p14_15_s4.py's _p14_cut (the surveyed bed, the level module's levels, the planting and people of the current
# programme), not the 28 Oct detail engine (engine_section, sky_labels, level_ladder are gone). Target =
# refs/targets/r06_S03_four_seasons_one_cut_accurate_BEST.png fitted to the frames of plan_findings/frames_p09-13.md
# "SON page15 -> new page 13": the in-bed sub-hub key and the month bar on top; per season a left column (months,
# water state, people, the in-bed hub open / closed, the season's story) and the S4 cut at 1:500 with its activities
# named on it and its levels as ▽ values at the right edge (booklet levels); FEEL · HEAR · TOUCH at the right; the
# animals on record (GBIF) as one compact column (Q2 b). Leaves the page (P-11): the upstream renders, the PLANTS /
# ZONES legends, the rain bars, the zone strips, the four 1:200 insets, the LEVELS · PLANTING BANDS block.
# Every printed value is read live: SUBHUB_OPEN (RAIN, EVAP), P15_KERMES, the level module through _p14_geo /
# _p14_level_rows, P14_PROM, STRIP_DEPTH. Values of the 28 Oct drawing with no current source are left out (handover).
# build_board: p13_page(pg, box, opt, log) in place of p14_page (same arguments, same returned crop).
# Included after pages/p14_15_s4.py (uses its _p14_* functions and P14_* / P15_* tables).

P13_TAG_W = 40.0                     # the season column at the left, mm (f93d84b TAG_W)
P13_GAP = 2.5                        # between the columns, mm (f93d84b SEASON_GAP)
P13_LEVEL_W = 24.0                   # room right of the cut for the booklet's ▽ values, mm (frames: x 61-70 of A3)
P13_FEEL_W = 42.0                    # FEEL · HEAR · TOUCH, mm (f93d84b SENSE_MIN 40)
P13_ANIM_W = 38.0                    # the animals on record, mm (frames: x 87-96.7 of A3 = 41 mm)
P13_HEAD_H = 19.0                    # the top row: sub-hub key and month bar, mm
P13_KEY = (55.0, 40.0)               # the key map's most room, mm (P-1: small, side column)
P13_LABEL_UP = 2.4                   # m over the highest ground of a zone: an activity's words (over a standing person)
P13_BAND_HUE = {"winter": ("WAT", 3), "spring": ("WAT", 2), "summer": ("WAT", 1), "autumn": ("WAT", 2)}   # G6-6:
#                                      the rule over each season's column (was BAND_BLUE)
P13_MONTH_HUE = dict(open=("PUB", 4), closed=("WAT", 2), kermes=("PUB", 1), high=("WAT", 1))   # G6-6: the month bar
#                                      (the bed open to people = public life PUB; high water = WAT)
P13_HEAD = {  # the season's state of the water store (f93d84b S4_SEASON head; design, ours)
    "winter": u"storage fills", "spring": u"storage full by end of April", "summer": u"strip runs on stored water",
    "autumn": u"storage low until the rains"}
P13_WORDS = {  # what people do, named on the cut over its zone of _p14_geo (f93d84b S4_SEASON words, our design /
    # concept v1 §10.1), moved onto today's zones; {prom} = P14_PROM over Q500, {strip} = STRIP_DEPTH, live.
    # v16 changes: "boardwalk open" -> "lower walk open" (S4 has no boardwalk now, its floodable lower walk is
    # P14_WALK); "Kermes stalls in the bed" -> "on the flood terrace" (the market ground of P14_ZONE_KEY); autumn's
    # "loosestrife heads cut" from P14_USE autumn (PLAN §8 harvest)
    "winter": [("prom_edge", u"sit at the edge · watch the floods"), ("terrace", u"terraces open between storms"),
               ("toe", u"marsh flooded · birds"), ("prom_in", u"raised walk {prom} m over Q500")],
    "spring": [("walk", u"lower walk open"), ("wade_s", u"children at the water's edge")],
    "summer": [("open_w", u"walk in the dry stream bed"), ("market", u"Kermes stalls on the flood terrace"),
               ("strip", u"feet in the strip · {strip} m")],
    "autumn": [("open_w", u"walk the gravel bed to the water"), ("strip", u"first-flush cleaning"),
               ("toe", u"loosestrife heads cut")],
}
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
                   extra=("stall", u"Kermes on the flood terrace", P13_KERMES_SRC)),
    "autumn": dict(water=("dry", u"low water"), acts=("walk", "sit"),
                   feel=("calm", u"calm, waiting for rain"), hear=("snd1", u"reeds rustle, first rain"),
                   touch=("gravel", u"gravel underfoot")),
}
P13_DROPPED = [u"p15_rain_%s", u"p15_cut_%s", u"p15_cut_%s_inset", u"p15_view_%s", u"p15_animals_%s"]   # round 5 ids


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
    if gx + 5.6 + text_w(tt, fs, True) + 1.0 > xk - 2.0 and xk + 3.4 + text_w(tk, fs, True) > gx + 5.6:
        if abs((yc - 10.3) - (yb - 5.6)) < fs * 1.2:
            wbx_warn(page, "overlap", u"p15_monthbar: \"high water ...\" and \"Kermes\" meet under the month bar")
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
    if pitch < FS_MIN * 1.1:
        wbx_warn(page, "overlap", u"p15_animals %s: %d animals in %.1f mm, names closer than their height" % (
            sea, len(sel), h))
    for i, fa in enumerate(sel):
        cy = ytop - pitch * (i + 0.5)
        with pg.g("legend", u"%s · %s" % (sea, fa["name"])):
            _p14_fauna(pg, fa["key"], x + sz / 2.0, cy, sz)
            pg.text(fa["name"], x + sz + 1.0, cy - FS_MIN * 0.35, FS_MIN, COL["ink_dark"])
        if text_w(fa["name"], FS_MIN) + sz + 1.0 > w + 0.05:
            wbx_warn(page, "edge", u"p15_animals %s: \"%s\" passes the column's edge" % (sea, fa["name"]))


def _p13_words(pg, X, Y, sea, fr, page, log=None):
    """the season's activities named on the cut (r06_S03: short words over the place, no leader lines, G3): each over
    the highest ground of its zone, P13_LABEL_UP m up, a second label that would touch one already set lifted by
    1.35 x its height (twice at most); one that still finds no room or leaves the frame = WARNING, left out"""
    G = _p14_geo()
    zn = G["zones"]
    fs = FS_MIN
    s0, s1 = P14_RANGE
    fmt = dict(prom=u"{:.2f}".format(P14_PROM - G["q500"]), strip=u"{:.2f}".format(STRIP_DEPTH))
    placed, n = [], 0
    for zone, words in P13_WORDS[sea]:
        if zone not in zn:
            wbx_warn(page, "label", u"p15_season_%s: no zone %s on S4 for \"%s\"" % (sea, zone, words))
            continue
        t = words.format(**fmt)
        a, b = max(zn[zone][0], s0), min(zn[zone][1], s1)
        zt = max(_p14_surf(a + (b - a) * j / 8.0) for j in range(9))
        w = text_w(t, fs, True)
        xa = min(max((X(a) + X(b)) / 2.0 - w / 2.0, fr[0] + 0.5), fr[2] - w - 0.5)
        y = Y(zt + P13_LABEL_UP)
        for _try in range(3):
            if not any(xa < q[2] + 1.0 and q[0] < xa + w + 1.0 and y < q[3] + 0.6 and q[1] < y + fs + 0.6
                       for q in placed):
                break
            y += 1.35 * fs
        else:
            wbx_warn(page, "overlap", u"p15_season_%s: \"%s\" finds no room clear of the other words" % (sea, t))
            continue
        if y + fs > fr[3] or xa < fr[0]:
            wbx_warn(page, "edge", u"p15_season_%s: \"%s\" would pass the drawing's frame" % (sea, t))
            continue
        placed.append((xa, y - 0.3 * fs, xa + w, y + fs))
        with pg.g("labels", t):
            pg.text(t, xa, y, fs, COL["ink_dark"], bold=True)
        n += 1
    if log is not None:
        log.append(u"p13 {}: {} activities named on the cut".format(sea, n))


def _p13_level_rows(sea):
    """the season's ▽ values (r06_S03: Q100 and Q500 only on the winter cut; each season its mean level and the bed;
    the summer strip where it is full): _p14_level_rows' [(key, m)]"""
    rows = _p14_level_rows(sea)
    if sea != "winter":
        rows = [r_ for r_ in rows if r_[0] not in ("q500", "q100")]
    return rows


def _p13_panel(pg, box, log, style):
    """booklet p13 (board page WBX_PG_SEASONS, round 6 id p13) drawn into box on the board as a recorder, every part
    handed to the booklet as its own item (crop "wb_s4_seasons"): p15_hubkey, p15_monthbar (diagrams, mm), per season
    p15_season_<season> (one row: the left column and the S4 cut at 1:500; x = m across S4 from the bed's low point,
    y = m a.s.l.; its levels as booklet levels), p15_feel and p15_animals (one column each over the four rows),
    p15_keymap (km_keymap). Returns its bbox."""
    x0, y0, x1, y1 = box
    n0 = len(pg.items)
    page = WBX_PG_SEASONS
    npg = wbx_p(page)
    crop = "wb_s4_seasons"
    G = _p14_geo(log)
    k = 1000.0 / P14_DEN
    s0, s1 = P14_RANGE
    wb = (s1 - s0) * k
    xa = x0
    xb = xa + P13_TAG_W + P13_GAP                # the cuts' band: the same x for all four (the bank lines up)
    xl = xb + wb
    xf = xl + P13_LEVEL_W                        # FEEL · HEAR · TOUCH
    xn = xf + P13_FEEL_W + P13_GAP               # the animals
    if xn + P13_ANIM_W > x1 + 0.05:
        wbx_warn(page, "edge", u"the four seasons need {:.0f} mm, the cell gives {:.0f} mm".format(
            xn + P13_ANIM_W - x0, x1 - x0))
    yt = y1 - 2.0
    yh = yt - P13_HEAD_H                         # the season rows start here
    rh = (yh - y0) / 4.0
    _P14_TREES.pop(page, None)
    _p14_keymap(page, P13_KEY, u"p15_keymap", log)
    # the top row: the in-bed sub-hub key over the left column, the month bar over the cuts
    nh = wbx_mark(pg)
    _p13_hubkey(pg, xa, yt)
    wbx_drawing(u"p15_hubkey", page, pg, _p13_bb(pg, nh), n0=nh, dkind="diagram", group=u"p15_hubkey", crop=crop)
    nm = wbx_mark(pg)
    _p13_monthbar(pg, xb, yt, wb, page)
    wbx_drawing(u"p15_monthbar", page, pg, _p13_bb(pg, nm), n0=nm, dkind="diagram", group=u"p15_monthbar",
                crop=crop)
    _p14_houses(P14_RANGE, log)                  # the houses behind the cut, logged once
    for i, sea in enumerate(SEAS):
        rt = yh - i * rh
        rbot = rt - rh
        ns = wbx_mark(pg)
        yc = _p13_tag(pg, xa, rt - 1.0, sea)
        if yc < rbot:
            wbx_warn(page, "edge", u"p15_season_%s: the season's column runs %.1f mm under its row" % (sea, rbot - yc))
        yb = rbot + 1.5
        ytc = rt - 1.0
        # ACCURATE (BRIEF §3, PLAN §2.3; target r06_S03): the S4 cut at true scale 1:500 on the surveyed bed, the
        # season's water from the level module, library people of the season's programme and the planting in the
        # season's state (plants.py images), light soil without hatch, activities named over their zones, the ▽
        # values at the right edge (booklet levels, spread); Q100 / Q500 on the winter cut only
        _p14_grp(pg, "other", u"sky · " + sea)
        shp_put(pg, sf_sky(xb, xl, yb, ytc, seed=i + 1, cid=u"S4-" + sea))
        _p14_grp(pg)
        sp = Page(0, 0)
        X, Y = _p14_cut(sp, xb, yb, k, P14_RANGE, sea, P14_SEA_MONTH[sea], style=style, ytop=ytc, page=page,
                        qlines=(sea == "winter"))
        fr = (xb, yb, xl, ytc)
        top = _p14_bb(sp.items)[3]
        if top > fr[3] + 0.05:                   # a crown taller than its row is cut at the row's top: a WARNING
            wbx_warn(page, "clipped", u"{} cut reaches {:.1f} mm over its row ({:.1f} m at 1:{:,.0f}): cut at the row "
                                      u"top".format(sea, top - fr[3], (top - fr[3]) / k, P14_DEN))
        pg.items += _p14_clip_items(sp.items, fr)
        _p13_words(pg, X, Y, sea, fr, page, log)
        did = u"p15_season_" + sea
        bbs = (xa, rbot, xl, rt)
        wbx_drawing(did, page, pg, bbs, n0=ns, den=P14_DEN, origin=(s0 - (xb - xa) / k, G["base"] + (rbot - yb) / k),
                    dkind="section", scale_pref=[int(P14_DEN)], title=sea.upper(), group=did, crop=crop)
        rows = _p13_level_rows(sea)
        _p14_levels_out(page, did, rows, S4_MONTHS[sea])
        _p14_level_spread(page, did, rows, Y, ytc, log)
        if log is not None:
            log.append(u"section {} S4 ACCURATE {} (1:{:,.0f}, r06_S03)".format(npg, sea, P14_DEN))
    # FEEL · HEAR · TOUCH and the animals: one column each, every season's part at its row's top
    nf = wbx_mark(pg)
    na = None
    for i, sea in enumerate(SEAS):
        rt = yh - i * rh
        yy = _p13_senses(pg, xf, rt - 1.0, sea, P13_FEEL_W)
        if yy < rt - rh:
            wbx_warn(page, "edge", u"p15_feel %s runs %.1f mm under its row" % (sea, rt - rh - yy))
    wbx_drawing(u"p15_feel", page, pg, (xf - 0.5, yh - 4.0 * rh, xf + P13_FEEL_W + 0.5, yh), n0=nf, dkind="diagram",
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
    wbx_text(page, u"S4–S4′, south-west to north-east: what the seasons change", "caption",
             did=u"p15_season_autumn", group=u"p15_season_autumn")
    bb = _p14_bb(pg.items[n0:])
    if log is not None:
        if G["src"] not in log:
            log.append(G["src"])
        for ln in wat_draw_order_lines(page=npg, steps=P14_STEPS_LOG):
            if ln not in log:
                log.append(ln)
        for sea in SEAS:
            for d_ in P13_DROPPED:
                log.append(u"dropped {} {} (P-11: r06_S03 layout)".format(npg, d_ % sea))
        for d_ in (u"p15_plants", u"p15_zones"):
            log.append(u"dropped {} {} (P-11: the PLANTS / ZONES legends leave the page)".format(npg, d_))
        _p14_hue_log(page, log)
        log.append(u"trees {} species={} generic=0 (proposed planting, designed species; no survey tree on the "
                   u"cut)".format(npg, _P14_TREES.get(page, 0)))
        _p14_sf_log(log, u"levels " + page)
        _p14_g6(k, P14_PLANTS, log, u"p13 cuts")
        log.append(u"p13 four seasons (r06_S03): cuts 1:{:,.0f}, rows {:.1f} mm, cut band {:.0f} mm; S4 bed {:+.2f}; "
                   u"bed open {} (SUBHUB_OPEN); people {}".format(
                       P14_DEN, rh, wb, G["bed"], _p15_open(),
                       u", ".join(u"{} {}".format(s_, len(_p14_people(s_))) for s_ in SEAS)))
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
    _p14_bridge_log(WBX_PG_SEASONS, log)
    return [("wb_s4_seasons", bb, P14_DEN)]
