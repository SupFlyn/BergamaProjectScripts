# ============================================================ v42 (Aras's deck review, 26 Oct 07:06)
# p.07 "The stream edge": a plan of what meets the water along each bank (the edge types the board already measures,
# every 4 m: build_edges), with walls, embankments, bridges, the cuts and the photo viewpoints, and the share of each
# edge type as one bar. p.09-11: every cut across the stream on ONE drawing at ONE round scale, on at most two booklet
# pages (Aras: "merge S1-S8 onto fewer pages, at a consistent scale"); a cut too long for a row is cropped to the part
# around the stream (global rule 2: crop, never stretch). Every drawing of these pages opens with a short context line
# (global rule 4: what it shows, why it is here, what to take from it).
CTX_H = 0.75            # page units: the context line's text height on a drawing about 120-140 units wide
BK_AW, BK_AH = 392.0, 238.0   # mm: the booklet's panel area on one page (bergama_booklet v4: A3 less margins, caption)
SEC_BOOK_DENS = (1000, 2000, 2500, 5000, 10000)   # the round booklet scales tried for the cuts, largest first
SEC_KEEP = 0.7          # a cut is cropped to the part around the stream only if at least this share of it stays
SEC_COL_GAP = 2.0       # page units between two cuts side by side
SEC_ROW_GAP = 1.6       # page units between rows of cuts
EDGE_PLAN_W = EDGE_W    # print weight (mm) of the edges on the edge plan


def ctx_line(B, txt, x, y, w, h, L):
    """v42: a drawing's context line (1-2 sentences) under its title, from baseline y; returns the y below it."""
    return B.para(txt, x, y, w, h, INK2, L, lead=1.45)


def edge_shares(S):
    """v42: {edge type: % of the bank length}, and the % walled and embanked (the key question's measure)."""
    tot = sum(S.edge_len.values())
    if tot <= 0:
        return {}, 0.0, 0.0, 0.0
    return (dict((k, 100.0 * v / tot) for k, v in S.edge_len.items()), 100.0 * S.walled_len / tot,
            100.0 * getattr(S, "embanked_len", 0.0) / tot, tot)


def draw_stream_edge_plan(S, B, x, y, w, U):
    """v42 (p.07): the site frame with the stream; what meets the water along each bank in the edge colours, walls
    and embankments marked on them, bridges K1-K6, the cuts S1..., the photo viewpoints by number (as under the
    photos); one bar of the edge types' shares of the bank length. Returns the y below."""
    L = "LU_BOARD::StreamEdge"
    F = S.F
    sh, wl_, em_, tot = edge_shares(S)
    B.text("WHAT MEETS THE WATER · BANK BY BANK", x, y, 1.05 * U, INK, L, font=FONT_TITLE, bold=True)
    walk = sh.get("pedestrian", 0.0)
    loose = sh.get("open", 0.0) + sh.get("parking", 0.0)
    ctx = (u"The edge along both banks, measured every 4 m on the survey: what touches the water, and where the bank "
           u"is walled or embanked. It locates the photos and cuts of these pages and shows where the stream can be "
           u"reached today ({:.0f}% of the bank walkable) and where the bank is open to change ({:.0f}% loose ground "
           u"or parking).".format(walk, loose)) if tot > 0 else \
        u"The edge along both banks, measured every 4 m on the survey: what touches the water."
    top = y - 1.5 * U
    yb = ctx_line(B, ctx, x, top, w, CTX_H * U, L)
    V, mw, mh = view_fit(F, x, yb - 0.4 * U, w, 10.0 * w)
    s = V.s
    # quiet base: paper, streets, buildings, the stream
    B.fill([V.P(F.P)], mix(PAPER, (255, 255, 255), 0.55), L, 1)
    road_lines(S, B, V, L, 3, casing=mix(INK2, PAPER, 0.7), surface=mix(ROADC, PAPER, 0.3), min_w=0.03,
               fill=mix(ROAD_FILL, PAPER, 0.55), hatch=False)
    mini_buildings(S, B, V, L, lambda u: mix(INK2, PAPER, 0.62 if not u["annex"] else 0.78), order=5)
    for wt in S.water:
        B.fill(V.Ps([wt["P"]] + wt.get("H", [])), CAT["water"][1], L, 6)
    for P in getattr(S, "covered", []):                  # the covered course, dashed over the streets
        for d in dashes(V.P(P), 0.35 * U, 0.25 * U):
            B.line(d, BLUE_D, L, 19, 0.12)
    # the edges, then walls (paper dashes) and embankments (paper dots) laid over them, as in the legend
    for typ, pts in getattr(S, "edge_runs", []):
        B.line(V.P(pts), EDGE[typ][1], L, 24, EDGE_PLAN_W)
    for pts in getattr(S, "wall_runs", []):
        for d in dashes(V.P(pts), 0.22 * U, 0.18 * U):
            B.line(d, PAPER, L, 25, EDGE_MARK_W)
    for pts in getattr(S, "bank_runs", []):
        for d in dashes(V.P(pts), 0.06 * U, 0.22 * U):
            B.line(d, PAPER, L, 25, EDGE_MARK_W)
    draw_map_annotations(S, B, V, U)                     # river name, cuts S1..., frame
    # bridges (ticks across the stream) and photo viewpoints (dots), short labels clear of each other
    photos = []
    try:
        photos = photo_files(os.path.join(pdf_folder(), "_site_photos"))
    except Exception:
        LOG.append("WARNING: the site photos could not be read for the edge plan:\n" + traceback.format_exc())
    th, kd = 0.4 * U, kind_of(FONT_TITLE)
    marks, taken = [], []
    for k, nm, bx, by in BRIDGES_K:
        if F.inside(bx, by):
            px, py = V.p(bx, by)
            n = stream_normal(S, bx, by) or (0.0, 1.0)
            a_ = V.p(bx + n[0], by + n[1])
            ln = math.hypot(a_[0] - px, a_[1] - py) or 1.0
            e = ((a_[0] - px) / ln * 0.6 * U, (a_[1] - py) / ln * 0.6 * U)
            B.line([(px - e[0], py - e[1]), (px + e[0], py + e[1])], INK, L, 62, 0.3)
            marks.append((k, px, py, INK, 0.7 * U))
    for i, (p, it) in enumerate(photos):
        if F.inside(it["x"], it["y"]):
            px, py = V.p(it["x"], it["y"])
            B.fill([circle_pts(px, py, 0.22 * U, 12)], INK, L, 64)
            B.text(str(i + 1), px, py, 0.26 * U, (255, 255, 255), L, order=65, font=FONT_TITLE, bold=True,
                   align="MC")
            taken.append((px - 0.25 * U, py - 0.25 * U, px + 0.25 * U, py + 0.25 * U))
    for t, px, py, col, d in marks:
        taken.append((px - d * 0.5, py - d * 0.5, px + d * 0.5, py + d * 0.5))
    for t, px, py, col, d in marks:
        w_ = tw(t, th, kd)
        opts = [(d, 0.2 * d), (d, -th - 0.2 * d), (-d - w_, 0.2 * d), (-d - w_, -th - 0.2 * d),
                (-0.5 * w_, d), (-0.5 * w_, -th - d)]
        for ox, oy in opts:
            bx_ = (px + ox - 0.08 * U, py + oy - 0.08 * U, px + ox + w_ + 0.08 * U, py + oy + th + 0.08 * U)
            if not any(bx_[0] < q[2] and q[0] < bx_[2] and bx_[1] < q[3] and q[1] < bx_[3] for q in taken):
                break
        else:
            ox, oy = opts[0]
            bx_ = (px + ox, py + oy, px + ox + w_, py + oy + th)
        taken.append(bx_)
        B.text(t, px + ox, py + oy, th, col, L, order=65, font=FONT_TITLE, bold=True)
    draw_north_small(B, V, mw, mh, U, L, size=0.7)
    mb = yb - 0.4 * U - mh
    draw_scalebar(B, V.X0, mb - 1.4 * U, s, nice_floor(F.w / 8.0), U, L, h=0.36)
    # one bar: each edge type's share of the bank length, figures on the bar where they fit
    yy = mb - 2.6 * U
    r_edge = bcite("Stream edges: what meets the water along each bank, sampled every 4 m along the surveyed banks "
                   "(nearest building within 8 m, walkable path or stairs, street, parking, planted ground; else "
                   "loose); walled = a surveyed wall within 3 m, embanked = only a surveyed slope line within 3 m.")
    leg = []
    if tot > 0:
        B.text(u"SHARE OF THE BANK LENGTH · {:,.1f} km {}".format(tot / 1000.0, r_edge), V.X0, yy, 0.45 * U, INK, L,
               font=FONT_TITLE, bold=True)
        bh, by0 = 1.0 * U, yy - 0.8 * U - 1.0 * U
        cx = V.X0
        for k_ in EDGE_ORDER:
            v_ = sh.get(k_, 0.0)
            if v_ <= 0:
                continue
            bw_ = mw * v_ / 100.0
            B.fill([rect(cx, by0, cx + bw_, by0 + bh)], EDGE[k_][1], L, 20)
            lab = "{:.0f}%".format(v_)
            if bw_ > tw(lab, 0.42 * U) + 0.4 * U:
                B.text(lab, cx + bw_ / 2.0, by0 + 0.3 * U, 0.42 * U,
                       (255, 255, 255) if k_ in ("building", "green", "pedestrian") else INK, L, align="C")
            cx += bw_
            leg.append(("thick", EDGE[k_][1], short(EDGE[k_][0])))
        B.line(rect(V.X0, by0, V.X0 + mw, by0 + bh) + [(V.X0, by0)], INK2, L, 21, 0.05)
        B.text(u"walled {:.0f}% · embanked {:.0f}% of the bank length".format(wl_, em_), V.X0, by0 - 0.85 * U,
               0.42 * U, INK2, L)
        yy = by0 - 1.4 * U
    leg += [("walled", INK2, "Walled bank"), ("embanked", INK2, "Embanked bank"), ("ktick", INK, "Bridges K1-K6"),
            ("pdot", INK, "Photo viewpoints (numbers as under the photos)")]
    ly = draw_legend_items(B, leg, V.X0, yy - 0.4 * U, mw, U, L, h=0.42)
    crop_panel("edge_plan", V.X0, ly + 0.2 * U, V.X0 + mw, top + CTX_H * U + 0.3 * U,
               u"What meets the water · bank by bank", crop_scale(s), crop_legend(leg))
    return ly


def sec_cropped(S, sd_, Lmax):
    """v42: the part of a cut Lmax long around the stream (centred on its water, kept inside the cut), cut again by the
    same section engine; its title says which part of the whole it is."""
    x0, y0, x1, y1, nm = sd_["line"]
    L = sd_["L"]
    if sd_["water"]:
        c = 0.5 * (min(w_[0] for w_ in sd_["water"]) + max(w_[1] for w_ in sd_["water"]))
    else:
        c = 0.5 * L
    s0 = max(0.0, min(L - Lmax, c - 0.5 * Lmax))
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    out = section_of_line(S, x0 + ux * s0, y0 + uy * s0, x0 + ux * (s0 + Lmax), y0 + uy * (s0 + Lmax), nm)
    out["crop_of"] = (L, s0)
    return out


def sections_plan(S, sw, U):
    """v42: (den, ss, pages): the largest round booklet scale 1:den at which every cut (cropped to the part around the
    stream where it is too long, keeping >= SEC_KEEP of it) fits on at most two booklet pages; pages = [[row, ...]],
    row = [(section, width)]. ss = page units per metre."""
    secs = list(S.sections)
    hmax = sw * BK_AH / BK_AW * 0.97
    best = None
    for den in SEC_BOOK_DENS:
        ss = 1000.0 * sw / (den * BK_AW)             # the drawing fills the booklet's width: 1:den on the page
        Lmax = (sw - 2.0 * SEC_END * U) / ss
        if any(sd_["L"] * SEC_KEEP > Lmax for sd_ in secs):
            continue
        cut = [sd_ if sd_["L"] <= Lmax else sec_cropped(S, sd_, Lmax) for sd_ in secs]
        items = []
        for c_ in cut:
            wi = min(sw, c_["L"] * ss + 2.0 * SEC_END * U)
            n0 = len(LOG)
            hi = -draw_section_strip(S, Board(), c_, 0.0, 0.0, wi, ss, U, dry=True)
            del LOG[n0:]
            items.append((c_, wi, hi))
        rows, cur, cw = [], [], 0.0                   # in order, side by side while they fit the width
        for it in items:
            if cur and cw + SEC_COL_GAP * U + it[1] > sw:
                rows.append(cur)
                cur, cw = [], 0.0
            cw += (SEC_COL_GAP * U if cur else 0.0) + it[1]
            cur.append(it)
        if cur:
            rows.append(cur)
        pages, ph = [[]], 4.0 * U                     # the first page also holds the context line
        for r in rows:
            rh = max(h_ for c_, w_, h_ in r) + SEC_ROW_GAP * U
            if pages[-1] and ph + rh > hmax:
                pages.append([])
                ph = 1.0 * U
            pages[-1].append(r)
            ph += rh
        best = (den, ss, [[[(c_, w_) for c_, w_, h_ in r] for r in pg] for pg in pages])
        if len(pages) <= 2 and all(max(h_ for c_, w_, h_ in r) + 5.0 * U <= hmax for r in rows):
            return best
    return best


def sections_context(S):
    """v42: the context line of the cuts, with the bed's depth below the banks over all cuts (computed)."""
    d = []
    for sd_ in S.sections:
        beds = [l for l in sd_["levels"] if l[3] == "bed"]
        banks = [l for l in sd_["levels"] if l[3] == "bank"]
        if beds and banks:
            d.append(banks[0][2] - beds[0][2])
    rng = (u" ({:.1f}-{:.1f} m)".format(min(d), max(d)) if len(d) > 1 else u" ({:.1f} m)".format(d[0])) if d else u""
    return (u"The ground as it falls to the water at {} cuts across the Selinos, all at one scale: surveyed ground, "
            u"bed, buildings at their floors and every street crossed. They show how far the bed lies below the "
            u"banks{} and what stands at each bank.".format(len(S.sections), rng))


def draw_sections_page(S, B, x, y, sw, U, plan, k):
    """v42: page k of the cuts (sections_plan): rows of whole cuts at one scale, the context line on the first page.
    Returns the y below."""
    L = "LU_BOARD::Sections"
    den, ss, pages = plan
    names = [c_["name"] for r in pages[k] for c_, w_ in r]
    B.text(u"SECTIONS ACROSS THE STREAM · {}{} · 1:{:,} ON THE A3 PAGE".format(
        names[0], "" if len(names) == 1 else "-" + names[-1], den), x, y, 0.9 * U, INK, L, font=FONT_TITLE, bold=True)
    top = y - 1.3 * U if k == 0 else y - 1.8 * U
    yy = ctx_line(B, sections_context(S), x, top, sw, CTX_H * U, L) - 0.4 * U if k == 0 else top
    low = yy
    for r in pages[k]:
        cx = x
        rl = yy
        for c_, w_ in r:
            bot = draw_section_strip(S, B, c_, cx, yy, w_, ss, U, tag="drawing",
                                     scale_txt=u"1:{:,} on the A3 booklet page".format(den))
            rl = min(rl, bot)
            cx += w_ + SEC_COL_GAP * U
        yy = rl - SEC_ROW_GAP * U
        low = rl
    crop_panel("sections_%d" % (k + 1), x, low - 0.2 * U, x + sw, (top + CTX_H * U + 0.3 * U) if k == 0 else top + 0.9 * U,
               u"Sections across the stream · {}".format(", ".join(names)), crop_scale(ss))
    return low
