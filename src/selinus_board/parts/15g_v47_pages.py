# ============================================================ v47 (Aras 27 Oct, booklet Prompt 5, task 3a: p.22 "Which plant goes where")
# The tree-cover chart under the water board's planting panel was read as a shade diagram, but buildings and the
# terrain shade the stream too. The board's own shade engine (ShadeJob: every minute the sun is up, the surveyed
# footprints at their heights, the canopy-map crowns by what they block, the terrain horizon; 1 m grid at ground level)
# now also sums every minute of July (env16_frame: shade "july"), and draw_shade_strip lays it along the stream on the
# tree-cover chart's chainage axis: hours in shade on the mean July day, every 25 m, in three rows (left bank, bed,
# right bank). Its crop drw_shade_strip is drawn for SS_BK_W mm on the booklet page (every word 7.5 pt, sans). Without
# shade results (no bergama_environment.json, or mode "drawings") it is not drawn, no shade crop is registered and
# p.22 keeps the tree crown cover (drw_tree_cover); the log says so.
SS_BK_W = 392.0         # mm: the shade strip's width on the booklet page (p.22, the panel's full width)
SS_BANK_M = 15.0        # m: a bank row = the open ground this far beyond the channel's edge on its side
SS_BED_M = 60.0         # m: water cells farther than this from the centreline are not the Selinos's channel
SS_MIN_CELLS = 20       # a bin of a row with fewer 1 m cells is left blank (as on the tree crown cover chart)
SS_STEP = 2.0           # h: the colour steps (0-2, 2-4, 4-6, 6-8, 8-10, 10+ h)
SS_SUN = mix(C("E0B67D"), WHITE, 0.6)     # the masterplan's "centre" tone, light: in the sun ...
SS_RAMP = [mix(SS_SUN, INK, t_) for t_ in (0.0, 0.18, 0.36, 0.54, 0.72, 0.9)]   # ... to the board's ink: in shade
SS_COVER_C = MPL["water_edge"]            # the covered reaches' hatch on the bed row (the stream under the town)


def shade_july(S):
    """v47: the shade engine's July mean day (dict(hours=grid, daylight=h)), or None without the environment
    analyses (no bergama_environment.json, or mode "drawings")."""
    return ((getattr(S, "env", None) or {}).get("shade") or {}).get("july")


def shade_strip_data(S):
    """v47: shade_strip_calc once per run (kept in the environment's memo); None without July shade results, or when
    it fails (logged, and p.22 keeps the tree crown cover)."""
    if not shade_july(S):
        return None
    memo = env_memo(S)
    if "shade_strip" not in memo:
        try:
            memo["shade_strip"] = shade_strip_calc(S)
        except Exception:
            memo["shade_strip"] = None
            LOG.append("WARNING: the shade along the stream could not be computed, so booklet p.22 shows the tree crown "
                       "cover instead:\n" + traceback.format_exc())
    return memo["shade_strip"]


def shade_strip_calc(S):
    """v47: hours in shade on the mean July day along the Selinos (the shade grid's "july", 1 m cells at ground level)
    per 25 m bin of the tree crown cover chart's chainage (the data pack's OSM centreline, 0 at the upstream frame
    edge) in three rows. BED = open cells inside the stream's outline (S.water rasterised on the shade grid) within
    SS_BED_M of the centreline, except under a covered reach or a bridge (the model has no roof or deck there). LEFT and
    RIGHT BANK = open cells outside the outline within SS_BANK_M beyond the channel's edge on that side (looking
    downstream); a bin's edge on a side = the largest offset of its channel cells there, 0 where it has none. Each cell
    takes its chainage and signed offset (+ left) from the nearest centreline vertex and the line's direction there. A
    bin's value = the mean of its cells (at least SS_MIN_CELLS, else None); a row's mean = over the cells of its bins
    with a value."""
    pk = seam_pack()
    cor, sel = pk.get("corridor") or {}, pk.get("selinos") or {}
    if not cor or len(sel.get("x") or []) < 2:
        return None
    jl = shade_july(S)
    G = S.env["shade"]["grid"]
    n, bm = int(cor["n_bins"]), float(cor["bin_m"])
    hrs = np.asarray(jl["hours"], float)
    xx, yy = np.asarray(G["xx"], float), np.asarray(G["yy"], float)
    LX, LY, LC = (np.asarray(sel[k_], float) for k_ in ("x", "y", "ch"))
    R = SS_BED_M + SS_BANK_M                              # no bed or bank cell lies farther from the line
    stp = float(np.hypot(np.diff(LX), np.diff(LY)).max())
    # the cells near the line: inside its box grown by R, then within R (+ 5 vertex steps) of every 10th vertex
    near = np.flatnonzero((xx >= LX.min() - R) & (xx <= LX.max() + R) & (yy >= LY.min() - R) & (yy <= LY.max() + R))
    ci = np.unique(np.r_[np.arange(0, LX.size, 10), LX.size - 1])
    lim = (R + 1.0 + 5.0 * stp) ** 2
    keep = [np.zeros(0, np.int64)]
    for a in range(0, near.size, 20000):
        c_ = near[a:a + 20000]
        d2 = (xx[c_][:, None] - LX[ci][None, :]) ** 2 + (yy[c_][:, None] - LY[ci][None, :]) ** 2
        keep.append(c_[d2.min(axis=1) <= lim])
    cand = np.concatenate(keep)
    j = np.zeros(cand.size, np.int64)                     # each one's nearest vertex, in chunks (memory)
    for a in range(0, cand.size, 4000):
        c_ = cand[a:a + 4000]
        d2 = (xx[c_][:, None] - LX[None, :]) ** 2 + (yy[c_][:, None] - LY[None, :]) ** 2
        j[a:a + 4000] = d2.argmin(axis=1)
    TX, TY = np.gradient(LX), np.gradient(LY)             # the line's direction at each vertex (downstream)
    TL = np.hypot(TX, TY)
    TL[TL <= 0.0] = 1.0
    TX, TY = TX / TL, TY / TL
    dx, dy = xx[cand] - LX[j], yy[cand] - LY[j]
    s = LC[j] + TX[j] * dx + TY[j] * dy                   # chainage, m from the upstream frame edge
    off = TX[j] * dy - TY[j] * dx                         # offset, m: + left, - right (looking downstream)
    ok = (s >= 0.0) & (s < n * bm) & (np.abs(off) <= R)
    cand, s, off = cand[ok], s[ok], off[ok]
    bi = np.minimum(n - 1, np.floor(s / bm).astype(np.int64))
    # the stream's outline on the shade grid (cell centres inside it; the grid's own frame and cells)
    Fg = Frame(G["frame"])
    grp = [[[Fg.local(p_[0], p_[1]) for p_ in wt["P"]]] +
           [[Fg.local(p_[0], p_[1]) for p_ in h_] for h_ in (wt.get("H") or []) if len(h_) >= 3]
           for wt in S.water if len(wt.get("P") or []) >= 3]
    wet = footprint_values(grp, np.ones(len(grp)), Fg.u0, Fg.v0, float(G["cell"]), int(G["nx"]),
                           int(G["ny"])) > -np.inf
    wt_ = wet[cand]
    h = hrs[cand]
    fin = np.isfinite(h)                                  # open ground (NaN inside a footprint)
    ao = np.abs(off)
    lf = off > 0.0
    chan = wt_ & (ao <= SS_BED_M)
    edge = np.zeros((2, n))                               # the channel's edge per side (0 left, 1 right) and bin
    for k_, m_ in ((0, chan & lf), (1, chan & ~lf)):
        np.maximum.at(edge[k_], bi[m_], ao[m_])
    drop = np.zeros(s.size, bool)                         # under a covered reach or a bridge: no roof or deck modelled
    for a_, b_ in cor.get("covered_reaches", []):
        drop |= (s >= a_) & (s <= b_)
    bch = cor.get("bridges_ch", [])
    for i_ in range(0, len(bch) - 1, 2):
        drop |= (s >= bch[i_]) & (s <= bch[i_ + 1])
    eg = np.where(lf, edge[0][bi], edge[1][bi])
    bank = fin & ~wt_ & (ao > eg) & (ao <= eg + SS_BANK_M)
    rows = {}
    for key, m_ in (("left", bank & lf), ("bed", chan & fin & ~drop), ("right", bank & ~lf)):
        cnt = np.bincount(bi[m_], minlength=n)
        tot = np.bincount(bi[m_], weights=h[m_], minlength=n)
        ok_ = cnt >= SS_MIN_CELLS
        rows[key] = dict(vals=[float(tot[i] / cnt[i]) if ok_[i] else None for i in range(n)], cells=cnt.tolist(),
                         mean=float(tot[ok_].sum() / cnt[ok_].sum()) if ok_.any() else None)
    bed = [v for v in rows["bed"]["vals"] if v is not None]
    return dict(n=n, bm=bm, cor=cor, rows=rows, daylight=float(jl["daylight"]), n_bed=len(bed),
                under2=(100.0 * sum(1 for v in bed if v < SS_STEP) / len(bed)) if bed else None)


def ss_colour(v):
    """v47: the colour step of v hours in shade (SS_STEP h each, the last open-ended)."""
    return SS_RAMP[min(len(SS_RAMP) - 1, int(v // SS_STEP))]


def draw_shade_strip(S, B, x, y, w, U):
    """v47 (Prompt 5, task 3a; booklet p.22 under the water board's planting panel): SHADE ALONG THE STREAM, the mean
    July day: hours out of direct sun at ground level on the left bank, the bed and the right bank every 25 m of the
    tree crown cover chart's chainage (shade_strip_data), in steps of SS_STEP h from light (sun) to dark (shade), each
    row's mean at the right; covered reaches hatched on the bed (no value), bridges as ticks across it; no section
    markers (cuts only on the sections pages' key maps). Its own crop (drw_shade_strip) from the context line down,
    designed for SS_BK_W mm on the booklet page, every word 7.5 pt in the sans. Returns the y below; draws nothing
    without shade results (build_sheet leaves it out then)."""
    L = "LU_BOARD::ShadeStrip"
    d = shade_strip_data(S)
    if not d:
        return y
    cor, n, bm, rows = d["cor"], d["n"], d["bm"], d["rows"]
    k = w / SS_BK_W                                       # board units per booklet mm
    h75 = bk_hk(7.5, k)
    B.text(u"SHADE ALONG THE STREAM · JULY, MEAN DAY · BED AND BANKS, EVERY 25 M", x, y, 1.05 * U, INK, L,
           font=FONT_TITLE, bold=True)                    # the sheet's title, above the crop
    top = y - 0.5 * U
    f1 = lambda v: u"{:.1f}".format(v) if v is not None else u"-"
    ctx = (u"Hours out of direct sun at ground level on the stream bed and on {:.0f} m of each bank, every {:.0f} m "
           u"downstream, cast by buildings, the terrain and tree crowns. July, mean day ({} h of sun up): the bed is in "
           u"shade {} h on average, the banks {} h (left) and {} h (right)").format(
        SS_BANK_M, bm, f1(d["daylight"]), f1(rows["bed"]["mean"]), f1(rows["left"]["mean"]), f1(rows["right"]["mean"]))
    if d["under2"] is not None:
        ctx += u"; {:.0f}% of the bed's {:.0f} m bins get under {:.0f} h of shade".format(d["under2"], bm, SS_STEP)
    yt = ctx_line(B, ctx + u".", x, top - 0.8 * k - h75, w, h75, L, font=FONT_TITLE)
    lab_w = tw(u"RIGHT BANK", h75, "sans") + 2.5 * k      # the rows' names at the left
    x0 = x + lab_w
    x1 = x + w - tw(u"10.0 h", h75, "sans") - 2.5 * k     # each row's mean at the right
    cw = (x1 - x0) / float(n)

    def X(ch):
        return x0 + ch / bm * cw
    # ---- distance axis, every 500 m downstream (as on the tree crown cover chart)
    ya = yt - 1.0 * k
    gtop = ya - 1.8 * k
    B.text(u"downstream", x0 - 1.5 * k, ya, h75, INK2, L, font=FONT_TITLE, align="R")
    for m in range(0, int(n * bm) + 1, 500):
        B.line([(X(m), gtop + 0.3 * k), (X(m), gtop + 1.1 * k)], INK2, L, 6, bk_lw(0.15, k))
        B.text(u"{:,}".format(m) + (u" m" if m == 0 else u""), X(m), ya, h75, INK2, L, font=FONT_TITLE,
               align="L" if m == 0 else "C")
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
            B.fill([rect(X(i * bm), rt - rh, X((e + 1) * bm), rt)], c_, L, 3)
            i = e + 1
        B.line(rect(x0, rt - rh, x1, rt) + [(x0, rt - rh)], FAINT, L, 4, bk_lw(0.1, k))
        ym = rt - 0.5 * rh - 0.5 * h75
        B.text(nm, x0 - 1.5 * k, ym, h75, INK, L, font=FONT_TITLE, bold=True, align="R")
        if rows[key]["mean"] is not None:
            B.text(u"{:.1f} h".format(rows[key]["mean"]), x1 + 1.5 * k, ym, h75, INK, L, font=FONT_TITLE, bold=True)
    # ---- on the bed row: the covered reaches hatched (no value), the bridges as ticks across it
    bt = gtop - (rh + rg)
    for a_, b_ in cor.get("covered_reaches", []):
        cov = rect(X(a_), bt - rh, X(b_), bt)
        B.fill([cov], WHITE, L, 5)
        B.hatch([cov], SS_COVER_C, L, 6, 1.0 * k, w=bk_lw(0.15, k))
        B.line(cov + [cov[0]], SS_COVER_C, L, 6, bk_lw(0.1, k))
    bch = cor.get("bridges_ch", [])
    for i_ in range(0, len(bch) - 1, 2):
        xa, xb = X(bch[i_]), X(bch[i_ + 1])
        if xb - xa < 0.5 * k:
            xa, xb = 0.5 * (xa + xb) - 0.25 * k, 0.5 * (xa + xb) + 0.25 * k
        B.fill([rect(xa, bt - rh - 0.6 * k, xb, bt + 0.6 * k)], INK, L, 7)
    # ---- key in one row: the colour steps, a covered reach, a bridge
    ky = gtop - 3.0 * rh - 2.0 * rg - 3.0 * k             # the swatches' top
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
    B.text(u"left and right looking downstream · blank: under {} cells".format(SS_MIN_CELLS), kx, ky - sh_, h75,
           INK2, L, font=FONT_TITLE)
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
    crop_panel("shade_strip", x, low, x + w, top, u"Shade along the stream · July, mean day · bed and banks, every 25 m")
    CROP_PANELS[-1]["bk_w"] = SS_BK_W                     # its width on the booklet page, mm
    LOG.append(u"Shade along the stream (July, mean day, {} h of sun up): in shade {} h on the bed, {} h on the left "
               u"bank and {} h on the right bank on average; {} of {} bed bins under {:.0f} h; booklet crop "
               u"drw_shade_strip, {:.0f} mm wide, {:.1f} mm high.".format(
                   f1(d["daylight"]), f1(rows["bed"]["mean"]), f1(rows["left"]["mean"]), f1(rows["right"]["mean"]),
                   sum(1 for v in rows["bed"]["vals"] if v is not None and v < SS_STEP), d["n_bed"], SS_STEP, SS_BK_W,
                   (top - low) / k))
    return low - 1.0 * U
