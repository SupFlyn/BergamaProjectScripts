# p.17 shade strip and riparian edge (split from parts/15_ndvi_col.py, parts/15g_v47_pages.py, parts/15k_r28_edge.py on 29 Oct 2026; moved unchanged)


def rip_colour(v):
    c_ = RIP_RAMP[0][1]
    for t, cc in RIP_RAMP:
        if v >= t:
            c_ = cc
    return c_


def draw_riparian(S, B, x, y, w, U):
    """S1 companion (plant analysis panel 3): canopy cover in four bands either side of the Selinos every 25 m of
    chainage; the stream between the banks with its covered reaches and bridges. v47 (Prompt 5): named tree crown
    cover, with no claim about shade (buildings and the terrain shade the stream too: draw_shade_strip computes that)
    and no section markers (cuts only on the sections pages' key maps)."""
    L = "LU_BOARD::Riparian"
    cor = seam_pack().get("corridor", {})
    if not cor:
        return y
    B.text("TREE CROWN COVER · BANK BY BANK, EVERY 25 M", x, y, 1.05 * U, INK, L, font=FONT_TITLE, bold=True)   # v47
    n, bm = cor["n_bins"], float(cor["bin_m"])
    th = RIP_TH * U
    rh, hb, gs = 0.95 * U, 1.3 * U, 0.14 * U             # a distance band, the stream, the gap between them
    bands = ["0-15", "15-30", "30-60", "60-100"]
    col_b = tw("RIGHT", th) + 0.5 * U                     # bank names
    lab_w = col_b + tw("60-100 m", th) + 0.5 * U          # + band names
    x0 = x + lab_w
    x1 = x + w - tw("mean", th) - 0.7 * U                 # the reach's mean per band at the right
    cw = (x1 - x0) / float(n)

    def X(ch):
        return x0 + ch / bm * cw
    # v42 (review rule 4): the context line, with the cover within 15 m of the stream on each bank (the means below)
    near = [(cor["cover"].get(sd + " 0-15", {}) or {}).get("total_pct") for sd in ("left", "right")]
    ctx = u"Share of the ground under tree crowns in four bands either side of the stream, every 25 m downstream."
    if None not in near:                                  # v47: no shade claim (crowns are not all the shade there is)
        ctx += u" Within 15 m of its centre line only {:.1f}% (left) and {:.1f}% (right) is under crowns.".format(
            near[0], near[1])
    ctop = y - 1.5 * U
    ya = ctx_line(B, ctx, x, ctop, w, CTX_H * U, L) - 0.7 * U
    # ---- distance axis, every 500 m along the stream (downstream to the right)
    gtop = ya - 0.5 * U
    B.text("downstream", x0 - 0.5 * U, ya, th, INK2, L, align="R")
    for m in range(0, int(n * bm) + 1, 500):
        B.line([(X(m), gtop + 0.05 * U), (X(m), gtop + 0.3 * U)], INK2, L, 6, 0.08)
        B.text("{:,}".format(m) + (" m" if m == 0 else ""), X(m), ya, th, INK2, L, align="L" if m == 0 else "C")
    B.text("mean", x1 + 0.5 * U, ya, th, INK2, L)

    def row_top(j):                                       # rows 0-3: left bank, far to near; 4-7: right bank, near to far
        return gtop - j * rh - (hb + 2.0 * gs if j >= 4 else 0.0)
    rows = [("left", b_) for b_ in reversed(bands)] + [("right", b_) for b_ in bands]
    for j, (side, b_) in enumerate(rows):
        yy = row_top(j)
        d_ = cor["cover"].get(side + " " + b_, {})
        vals = d_.get("pct") or d_.get("cover") or []
        cells = d_.get("cells", [])
        for i in range(n):
            v = vals[i] if i < len(vals) else None
            if v is None or (i < len(cells) and cells[i] < 20):
                continue
            B.fill([rect(X(i * bm), yy - rh + 0.05 * U, X((i + 1) * bm), yy - 0.05 * U)], rip_colour(v), L, 3)
        ym = yy - 0.5 * rh - 0.5 * th
        B.text(b_ + " m", x0 - 0.5 * U, ym, th, INK, L, align="R")
        if d_.get("total_pct") is not None:
            B.text("{:.1f}%".format(d_["total_pct"]), x1 + 0.5 * U, ym, th, INK, L)
    for side, j0 in (("LEFT", 0), ("RIGHT", 4)):          # the bank's name beside its four rows
        yc = row_top(j0) - 2.0 * rh
        B.text(side, x, yc + 0.15 * U, th, INK, L, font=FONT_TITLE, bold=True)
        B.text("BANK", x, yc - 0.15 * U - th, th, INK, L, font=FONT_TITLE, bold=True)
        B.line(rect(x0, row_top(j0 + 3) - rh, x1, row_top(j0)) + [(x0, row_top(j0 + 3) - rh)], FAINT, L, 4, 0.05)
    # ---- the stream between the banks: covered reaches darker and hatched, bridges as ticks across it
    st, sb = row_top(3) - rh - gs, row_top(3) - rh - gs - hb
    B.fill([rect(x0, sb, x1, st)], CAT["water"][1], L, 3)
    B.text("STREAM", x0 - 0.5 * U, 0.5 * (st + sb) - 0.5 * th, th, BLUE_D, L, font=FONT_TITLE, bold=True, align="R")
    am = 0.5 * (st + sb)                                  # the flow, at the upstream end
    B.line([(X(10.0), am), (X(62.0), am)], BLUE_D, L, 5, 0.25)
    B.fill([[(X(88.0), am), (X(60.0), am + 0.32 * U), (X(60.0), am - 0.32 * U)]], BLUE_D, L, 5)
    for a, b in cor.get("covered_reaches", []):
        cov = rect(X(a), sb, X(b), st)
        B.fill([cov], RIP_COVERED, L, 4)
        B.hatch([cov], CAT["water"][1], L, 5, 0.3 * U, w=0.05)
    ch = cor.get("bridges_ch", [])
    for i in range(0, len(ch) - 1, 2):
        xa, xb = X(ch[i]), X(ch[i + 1])
        if xb - xa < 0.2 * U:
            xa, xb = 0.5 * (xa + xb) - 0.1 * U, 0.5 * (xa + xb) + 0.1 * U
        B.fill([rect(xa, sb - 0.08 * U, xb, st + 0.08 * U)], INK, L, 6)
    # ---- v47 (Prompt 5, Aras's rule: section cuts only on the sections pages' key maps): no section markers here
    gb = row_top(7) - rh
    yl = gb - 0.15 * U
    PANEL_RECTS["riparian"] = (x, yl - 0.25 * U, x + w, ctop + CTX_H * U + 0.3 * U)     # v42: from the context line
    # ---- key: the colour steps, the stream, a covered reach, a bridge
    yk = yl - 1.6 * U
    B.text("TREE CROWN COVER · % OF THE GROUND UNDER CROWNS", x, yk, 0.42 * U, INK, L, font=FONT_TITLE, bold=True)
    yb = yk - 1.4 * U
    bw = 2.2 * U
    for k, (t, c_) in enumerate(RIP_RAMP):
        B.fill([rect(x + k * bw, yb, x + (k + 1) * bw, yb + 0.7 * U)], c_, L, 20)
        B.text("{:g}".format(t), x + k * bw, yb - 0.25 * U - 0.42 * U, 0.42 * U, INK2, L, align="C")
    B.line(rect(x, yb, x + len(RIP_RAMP) * bw, yb + 0.7 * U) + [(x, yb)], INK2, L, 21, 0.05)
    B.text("%", x + len(RIP_RAMP) * bw, yb - 0.25 * U - 0.42 * U, 0.42 * U, INK2, L, align="C")
    kx = x + len(RIP_RAMP) * bw + 2.5 * U
    for kind, col, lab in [it for it in rip_legend() if not it[2].startswith("tree cover")]:
        sw = 2.0 * U
        B.fill([rect(kx, yb, kx + sw, yb + 0.7 * U)], CAT["water"][1] if kind == "line" else col, L, 20)
        if col is RIP_COVERED:
            B.hatch([rect(kx, yb, kx + sw, yb + 0.7 * U)], CAT["water"][1], L, 21, 0.3 * U, w=0.05)
        if kind == "line":
            B.fill([rect(kx + 0.5 * sw - 0.1 * U, yb - 0.08 * U, kx + 0.5 * sw + 0.1 * U, yb + 0.78 * U)], col, L, 22)
        B.text(lab, kx + sw + 0.4 * U, yb + 0.15 * U, 0.42 * U, INK, L)
        kx += sw + 0.4 * U + tw(lab, 0.42 * U) + 1.6 * U
    return B.para("cover = share of 1 m cells under crowns · rows by distance from the stream's centre line, left and "
                  "right looking downstream · 25 m bins · mean = the whole reach " + bcite(
        "Tree crown cover along the stream: share of the 1 m cells under crown discs (canopy map, modelled), in bands "
        "measured from the OSM centreline (so 0-15 m holds the channel); bins of 25 m of chainage from the upstream "
        "frame edge; a bin under 20 cells is left blank. Covered reaches drawn on the stream, bridges as ticks across "
        "it."),
                  x, yb - 1.8 * U, w, 0.32 * U, INK2, L)


def ss_colour(v):
    """v47: the colour step of v hours in shade (SS_STEP h each, the last open-ended)."""
    return SS_RAMP[min(len(SS_RAMP) - 1, int(v // SS_STEP))]


# ------------------------------------------------------------ p.16 the shade strip on the frame's axis
def draw_shade_strip(S, B, x, y, w, U):
    """v50 (MIRAQUA 28 Oct, G7, G8; replaces v47's chart on the chainage axis): SHADE ALONG THE STREAM, the mean July
    day (p.16, crop drw_shade_strip): hours out of direct sun at ground level on the left bank, the bed and the right
    bank in shade_strip_data's 25 m bins, each bin drawn where it lies along the analysis frame's axis at 1:10,000
    (the maps' scale and length: one strip), the study area's stretches framed in its line (G8), the stream's
    chainage as ticks every 500 m, a scale bar under the rows; covered reaches hatched on the bed (no value), bridges
    as ticks across it, each row's mean at the right; no section markers. Every word 7.5 pt in the sans, drawn for
    SS_BK_W mm. Returns the y below; draws nothing without shade results (build_sheet leaves it out then)."""
    L = "LU_BOARD::ShadeStrip"
    d = shade_strip_data(S)
    if not d:
        return y
    F = S.F
    cor, n, bm, rows = d["cor"], d["n"], d["bm"], d["rows"]
    k = w / SS_BK_W                                       # board units per booklet mm
    h75 = bk_hk(7.5, k)
    ss = 1000.0 * k / R28E_DEN                            # 1:10,000 along the frame's axis
    B.text(u"SHADE ALONG THE STREAM · JULY, MEAN DAY · BED AND BANKS, EVERY 25 M", x, y, 1.05 * U, INK, L,
           font=FONT_TITLE, bold=True)                    # the sheet's title, above the crop
    top = y - 0.5 * U
    f1 = lambda v: u"{:.1f}".format(v) if v is not None else u"-"
    ctx = (u"**Hours out of direct sun** at ground level on the stream bed and on {:.0f} m of each bank, every {:.0f} m "
           u"downstream, cast by buildings, the terrain and tree crowns. **July, mean day** ({} h of sun up): the bed "
           u"is in shade {} h on average, the banks {} h (left) and {} h (right)").format(
        SS_BANK_M, bm, f1(d["daylight"]), f1(rows["bed"]["mean"]), f1(rows["left"]["mean"]), f1(rows["right"]["mean"]))
    if d["under2"] is not None:
        ctx += u"; {:.0f}% of the bed's {:.0f} m bins get under {:.0f} h of shade".format(d["under2"], bm, SS_STEP)
    ctx += (u". Each bin is drawn where it lies along the analysis frame's axis at 1:10,000, as the maps (the rows' "
            u"height is not to scale); the ticks count metres along the stream.")
    yt = r28mv_para(B, ctx, x, top - 0.8 * k - h75, w, h75, INK2, L, order=40)
    lab_w = tw(u"RIGHT BANK", h75, "sans") + 2.5 * k      # the rows' names at the left
    x0 = x + lab_w
    x1 = x0 + F.w * ss                                    # the frame's length at 1:10,000; each row's mean beyond
    sel = seam_pack().get("selinos") or {}
    LX, LY, LC = (np.asarray(sel[k_], float) for k_ in ("x", "y", "ch"))

    def at(ch):                                           # the centreline's point at chainage ch (survey m)
        return float(np.interp(ch, LC, LX)), float(np.interp(ch, LC, LY))

    def X(ch):                                            # chainage -> page x along the frame's axis
        return x0 + min(F.w, max(0.0, F.local(*at(ch))[0] - F.u0)) * ss
    xe = [X(i * bm) for i in range(n + 1)]                # the bins' ends

    def span(i, e):                                       # bins i..e as a page x range (the stream may turn back)
        return min(xe[i:e + 2]), max(max(xe[i:e + 2]), min(xe[i:e + 2]) + 0.1 * k)
    # ---- the stream's chainage, every 500 m downstream (as on the tree crown cover chart)
    ya = yt - 1.0 * k
    gtop = ya - 1.8 * k
    B.text(u"downstream", x0 - 1.5 * k, ya, h75, INK2, L, font=FONT_TITLE, align="R")
    last = -1e30
    for m in range(0, int(n * bm) + 1, 500):
        xm = X(m)
        t_ = u"{:,}".format(m) + (u" m" if m == 0 else u"")
        tl = tw(t_, h75, "sans")
        B.line([(xm, gtop + 0.3 * k), (xm, gtop + 1.1 * k)], INK2, L, 6, bk_lw(0.15, k))
        lx_ = xm if m == 0 else xm - 0.5 * tl
        if lx_ > last + 1.0 * k:
            B.text(t_, xm, ya, h75, INK2, L, font=FONT_TITLE, align="L" if m == 0 else "C")
            last = lx_ + tl
    B.text(u"mean", x1 + 1.5 * k, ya, h75, INK2, L, font=FONT_TITLE)
    # ---- the three rows: runs of bins in one colour step as one fill, blank under SS_MIN_CELLS cells
    rh, rg = 7.0 * k, 0.9 * k                             # a row, the gap between two
    for r_, (nm, key) in enumerate(((u"LEFT BANK", "left"), (u"BED", "bed"), (u"RIGHT BANK", "right"))):
        rt = gtop - r_ * (rh + rg)
        vals = rows[key]["vals"]
        i = 0
        while i < n:
            if vals[i] is None:
                i += 1
                continue
            c_ = ss_colour(vals[i])
            e = i
            while e + 1 < n and vals[e + 1] is not None and ss_colour(vals[e + 1]) == c_:
                e += 1
            xa, xb = span(i, e)
            B.fill([rect(xa, rt - rh, xb, rt)], c_, L, 3)
            i = e + 1
        B.line(rect(x0, rt - rh, x1, rt) + [(x0, rt - rh)], FAINT, L, 4, bk_lw(0.1, k))
        ym = rt - 0.5 * rh - 0.5 * h75
        B.text(nm, x0 - 1.5 * k, ym, h75, INK, L, font=FONT_TITLE, bold=True, align="R")
        if rows[key]["mean"] is not None:
            B.text(u"{:.1f} h".format(rows[key]["mean"]), x1 + 1.5 * k, ym, h75, INK, L, font=FONT_TITLE, bold=True)
    # ---- on the bed row: the covered reaches hatched (no value), the bridges as ticks across it
    bt = gtop - (rh + rg)
    for a_, b_ in cor.get("covered_reaches", []):
        xs_ = [X(a_), X(0.5 * (a_ + b_)), X(b_)]
        cov = rect(min(xs_), bt - rh, max(xs_), bt)
        B.fill([cov], WHITE, L, 5)
        B.hatch([cov], SS_COVER_C, L, 6, 1.0 * k, w=bk_lw(0.15, k))
        B.line(cov + [cov[0]], SS_COVER_C, L, 6, bk_lw(0.1, k))
    bch = cor.get("bridges_ch", [])
    for i_ in range(0, len(bch) - 1, 2):
        xa, xb = sorted((X(bch[i_]), X(bch[i_ + 1])))
        if xb - xa < 0.5 * k:
            xa, xb = 0.5 * (xa + xb) - 0.25 * k, 0.5 * (xa + xb) + 0.25 * k
        B.fill([rect(xa, bt - rh - 0.6 * k, xb, bt + 0.6 * k)], INK, L, 7)
    # ---- G8: the stretches inside the study area, framed in its line across the three rows
    ybot = gtop - 3.0 * rh - 2.0 * rg
    st_ = R28_STUDY_LINE
    ins = [any(pip(at((i + 0.5) * bm)[0], at((i + 0.5) * bm)[1], P) for P in getattr(S, "r28_study", None) or [])
           for i in range(n)]
    i = 0
    while i < n:
        if not ins[i]:
            i += 1
            continue
        e = i
        while e + 1 < n and ins[e + 1]:
            e += 1
        xa, xb = span(i, e)
        q = rect(xa, ybot - 0.5 * k, xb, gtop + 0.2 * k)
        for dd in r28_pattern(q + [q[0]], [m_ * k for m_ in st_["dash_mm"]]):
            B.line(dd, C(st_["colour"]), L, 9, bk_lw(st_["width_mm"], k))
        i = e + 1
    # ---- the scale bar under the rows (1:10,000 along the frame's axis)
    yl0 = draw_scalebar_bk(B, x0 + 1.0 * k, ybot - 2.5 * k, ss, R28E_SB_M, k, L)
    B.text(u"1:{:,} along the frame's axis".format(R28E_DEN), x0 + 1.0 * k + R28E_SB_M * ss +
           tw(u"{:,.0f} m".format(R28E_SB_M), h75, "sans") + 3.0 * k, ybot - 2.5 * k - 1.2 * k, h75, INK2, L,
           font=FONT_TITLE)
    # ---- key in one row: the colour steps, a covered reach, a bridge, the study area
    ky = yl0 - 2.0 * k                                    # the swatches' top
    sh_ = 2.6 * k
    yl = ky - sh_ - 1.0 * k - h75                         # the steps' names under their swatches
    t_ = u"h of shade, July mean day"
    B.text(t_, x, ky - sh_, h75, INK, L, font=FONT_TITLE, bold=True)
    kx = x + tw(t_, h75, "sans") + 3.0 * k
    sw = 9.0 * k
    nr = len(SS_RAMP)
    for i, c_ in enumerate(SS_RAMP):
        B.fill([rect(kx + i * sw, ky - sh_, kx + (i + 1) * sw, ky)], c_, L, 20)
        B.text(u"{:g}-{:g}".format(i * SS_STEP, (i + 1) * SS_STEP) if i + 1 < nr else u"{:g}+".format(i * SS_STEP),
               kx + (i + 0.5) * sw, yl, h75, INK2, L, font=FONT_TITLE, align="C")
    B.line(rect(kx, ky - sh_, kx + nr * sw, ky) + [(kx, ky - sh_)], INK2, L, 21, bk_lw(0.1, k))
    B.text(u"h", kx + nr * sw + 1.0 * k, yl, h75, INK2, L, font=FONT_TITLE)
    kx += nr * sw + 6.0 * k
    sw = 6.0 * k
    cov = rect(kx, ky - sh_, kx + sw, ky)
    B.fill([cov], WHITE, L, 20)
    B.hatch([cov], SS_COVER_C, L, 21, 1.0 * k, w=bk_lw(0.15, k))
    B.line(cov + [cov[0]], SS_COVER_C, L, 22, bk_lw(0.1, k))
    t_ = u"covered: under the town, no sun"
    B.text(t_, kx + sw + 1.5 * k, ky - sh_, h75, INK, L, font=FONT_TITLE)
    kx += sw + 1.5 * k + tw(t_, h75, "sans") + 6.0 * k
    B.fill([rect(kx + 0.5 * sw - 0.3 * k, ky - sh_ - 0.6 * k, kx + 0.5 * sw + 0.3 * k, ky + 0.6 * k)], INK, L, 22)
    B.text(u"bridge", kx + sw + 1.5 * k, ky - sh_, h75, INK, L, font=FONT_TITLE)
    kx += sw + 1.5 * k + tw(u"bridge", h75, "sans") + 6.0 * k
    for dd in r28_pattern([(kx, ky - 0.5 * sh_), (kx + 8.0 * k, ky - 0.5 * sh_)], [m_ * k for m_ in st_["dash_mm"]]):
        B.line(dd, C(st_["colour"]), L, 22, bk_lw(st_["width_mm"], k))
    B.text(R28_STUDY_NAME, kx + 9.5 * k, ky - sh_, h75, INK, L, font=FONT_TITLE)
    kx += 9.5 * k + tw(R28_STUDY_NAME, h75, "sans") + 6.0 * k
    t_ = u"left and right looking downstream · blank: under {} cells".format(SS_MIN_CELLS)
    if kx + tw(t_, h75, "sans") > x + w:                  # no room left in the row: under the steps' names
        kx, yl = x, yl - 1.8 * h75
        B.text(t_, kx, yl, h75, INK2, L, font=FONT_TITLE)
    else:
        B.text(t_, kx, ky - sh_, h75, INK2, L, font=FONT_TITLE)
    # ---- the method, labelled computed; the full sentence in the drawings' source key
    src = (u"Shade along the stream (computed by this board): hours out of direct sun on the mean July day at ground "
           u"level on a 1 m grid, every minute the sun is up on all 31 days of July 2025 (NOAA / Meeus solar position, "
           u"UTC+3) summed and divided by 31. In the sun's way: every surveyed building footprint as a prism of its "
           u"height (surveyed floors x storey height, or a published height) on the surveyed ground; the tree crowns "
           u"of the canopy map (Meta / WRI 1 m canopy height, modelled), deciduous ones in leaf, counted by the light "
           u"they block; the terrain horizon (PVGIS DEM profiles every 100 m) and the ground's own slope. Not "
           u"modelled: walls, the channel's own banks, bridge decks and the roofs over the covered reaches, so where "
           u"walls or deep banks line the bed its hours are a lower bound. Bed = the 1 m cells inside the stream's "
           u"mapped outline, those under a bridge or a covered reach left out; banks = the open cells within {:.0f} m "
           u"beyond the channel's edge on each side, left and right looking downstream. Chainage along the OSM Selinos "
           u"centreline from the upstream frame edge, as on the tree crown cover chart; {:.0f} m bins, a bin under {} "
           u"cells left blank.").format(SS_BANK_M, bm, SS_MIN_CELLS)
    yb = ctx_line(B, u"computed · sun every minute of July 2025 at the site (NOAA / Meeus) · surveyed building "
                     u"footprints at their roof heights · tree crowns from the canopy map (modelled) · terrain horizon "
                     u"from the DEM (PVGIS) · 1 m grid, ground level · walls and the channel's banks not modelled " +
                  bcite(src), x, yl - 3.0 * k - h75, w, h75, L, font=FONT_TITLE)
    low = yb + 1.15 * h75 - 0.8 * k                       # under the last line's descenders
    crop_panel("shade_strip", x, low, x + w, top, u"Shade along the stream · July, mean day · bed and banks, every 25 m",
               crop_scale(ss))
    CROP_PANELS[-1]["bk_w"] = SS_BK_W                     # its width on the booklet page, mm
    LOG.append(u"Shade along the stream (July, mean day, {} h of sun up): in shade {} h on the bed, {} h on the left "
               u"bank and {} h on the right bank on average; {} of {} bed bins under {:.0f} h; {} bins in the study "
               u"area; one strip at 1:{:,} along the frame's axis; booklet crop drw_shade_strip, {:.0f} mm wide, "
               u"{:.1f} mm high.".format(
                   f1(d["daylight"]), f1(rows["bed"]["mean"]), f1(rows["left"]["mean"]), f1(rows["right"]["mean"]),
                   sum(1 for v in rows["bed"]["vals"] if v is not None and v < SS_STEP), d["n_bed"], SS_STEP,
                   sum(ins), R28E_DEN, SS_BK_W, (top - low) / k))
    return low - 1.0 * U
