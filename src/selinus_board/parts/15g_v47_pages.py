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
            LOG.append("WARNING: the shade along the stream could not be computed, so booklet page \"Which plant goes "
                       "where\" shows the tree crown cover instead:\n" + traceback.format_exc())   # v49.1: was "p.22"
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


# v50 (MIRAQUA 28 Oct, G7, G8): draw_shade_strip (p.16, crop drw_shade_strip: its rows along the analysis frame's
# axis at 1:10,000, the study area marked, a scale bar) is in parts/15k_r28_edge.py
