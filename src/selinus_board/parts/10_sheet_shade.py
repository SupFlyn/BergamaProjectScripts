def sheet_shade(S, B, X, Y, U, rects, d):
    items = shade_items(S)
    sh = S.env["shade"]
    G = sh["grid"]

    def render(it):
        n, cols, edges = shade_scale(it["daylight"])
        p = os.path.join(d, "T3_shade_%s.png" % it["key"])
        render_tech(p, S, S.F, 0.3, it["hours"], G["nx"], G["ny"], G["cell"], 0.5, lut_classes(edges, cols),
                    roof="white", season=it["season"], canopy_alpha=0.28, rkey=fp(S.env["keys"]["shade"], it["key"]))
        return p

    def side(it, x, y, w, L):
        t_title(B, x, y, it["name"], w, S.U, L)
        B.fit(it["sub"], x, y - 0.9 * S.U, 0.3 * S.U, w, T_GREY, L)
        n, cols, edges = shade_scale(it["daylight"])
        yy = tech_bands(B, x, y - 1.6 * S.U, w, cols, ["%d" % k for k in range(n)], S.U, L,
                        title="Hours in shade (from the hour shown)" + (" on the mean day" if it["key"] == "year" else ""))
        vis_tiles(B, x, yy - 0.1 * S.U, w, shade_tiles(S, it), S.U, L, h=0.9)     # v38: tiles (was a paragraph)
    tech_rows(S, B, X, Y, U, rects, "T3", "SHADE · THE KEY DAYS AND THE YEAR",
              "Hours in shade · key days + the year · sunrise to sunset [1]",
              ["Every minute the sun is up (NOAA sun position, UTC+3): the four key days of 2025, and every day of the year "
               "averaged.",
               "Casters: every building (exact footprint, roof at its surveyed floors over the surveyed ground), "
               "3D tree crowns from the 1 m canopy height map at their modelled heights (Meta/WRI, mean absolute error 2.8 m), the terrain horizon (PVGIS DEM) and "
               "the ground's own slope; obstruction found exactly for every degree of sun azimuth, {:g} m cells (v16.6; "
               "v16.5: 3 m).".format(SHADE_CELL), canopy_note(S), height_note(S)],
              "Shade", render, side, items=items)


def sheet_radiation(S, B, X, Y, U, rects, d):
    L = "LU_TECH::Solar radiation"
    B.begin("TECHNICAL T4 · Solar radiation", "LU_TECH")
    rd = S.env["rad"]
    top, bottom = tech_frame(S, B, X, Y, U, "T4", "SOLAR RADIATION · FOUR SEASONS",
                             "kWh/m² per day · ground + roofs · season means [1]",
                             ["Every hour of the PVGIS-SARAH2 typical year 2005-2020 for these coordinates, the sun at its exact "
                              "position.",
                              "Direct and circumsolar sun through the obstruction of that sun position (buildings, 3D "
                              "tree crowns by their transmission, terrain horizon, the ground's own slope), isotropic sky "
                              "(Perez 1990) through the cosine-weighted sky each cell sees (72 sectors, exact in elevation), the "
                              "Perez horizon band and ground reflection (albedo 0.2) on slopes. Ground and roofs every 1.5 m.",
                              "On open flat ground the model returns the typical year's global horizontal (within 0.1 %).",
                              "Area: " + ("the whole frame." if S.env["focus"] is S.F else "the focus area (key plan)."),
                              canopy_note(S),
                              "Classes: one scale for the four seasons, each class holding about an equal share of the "
                              "ground and roof cells."])
    x0, W = X + PM * U, (PW - 2 * PM) * U
    Fo = S.env["focus"]
    if Fo is S.F:                                     # v16.5: the whole frame, a row per season as on T5-T7
        return sheet_radiation_rows(S, B, X, Y, U, rects, d, L, top, bottom)
    kp_w = 18.0 * U
    key_plan(S, B, x0 + W - kp_w, Y - 1.9 * U, kp_w, Fo, U, L)
    cw = (W - 2.4 * U) / 2.0
    rowh = (top - bottom) / 2.0
    edges = rad_scale(S)
    cols = ramp_hex(TECH_PAL["rad"], len(edges) + 1)
    lut = lut_classes(edges, cols)
    labels = ["< %.2f" % edges[0]] + ["%.2f-%.2f" % (edges[i], edges[i + 1]) for i in range(len(edges) - 1)] + ["> %.2f" % edges[-1]]
    months = {"spring": "MARCH-MAY", "summer": "JUNE-AUGUST", "autumn": "SEPTEMBER-NOVEMBER", "winter": "DECEMBER-FEBRUARY"}
    def pic(sd):
        v = rd["seasons"][sd["key"]]["kwh"]
        gnd = np.where(rd["roof"], np.nan, v)
        roofv = np.where(rd["roof"], v, np.nan)
        p = os.path.join(d, "T4_solar_radiation_%s.png" % sd["key"])
        render_tech(p, S, Fo, 0.3, gnd, rd["nx"], rd["ny"], rd["cell"], 0.5, lut, roof="grid", roof_grid=roofv,
                    season=sd["key"], canopy_alpha=0.62, rkey=fp(S.env["keys"]["rad"], sd["key"], edges))
        return p
    ps = par_renders([(lambda sd_=sd: pic(sd_)) for sd in SEASONS])        # v18: the pictures side by side
    for k, sd in enumerate(SEASONS):
        cx = x0 + (k % 2) * (cw + 2.4 * U)
        cy = top - (k // 2) * rowh
        t_title(B, cx, cy, "{} · {} · {} DAYS".format(sd["name"], months[sd["key"]], days_in_season(sd["key"])), cw, U, L, h=0.55)
        p = ps[k]
        V, wv, hv = tech_map(S, B, Fo, p, cx, cy - 0.9 * U, cw, rowh - 5.0 * U, U, L, scale=True)
        yy = tech_bands(B, cx + 9.0 * U, cy - 0.9 * U - hv - 0.4 * U, cw - 9.0 * U, cols, labels, U, L, h=0.27,
                        title="kWh/m² per day · one scale, four seasons [6]")
        vis_tiles(B, cx, yy - 0.05 * U, cw, rad_tiles(S, sd["key"]), U, L, h=0.6)     # v38: tiles (was a line)
    rects.append(("T4 · Solar radiation", (X, Y - PH * U, X + PW * U, Y)))


def sheet_radiation_rows(S, B, X, Y, U, rects, d, L, top, bottom):
    """v16.5: T4 over the whole frame: one row per season (the map, then its classes and figures beside it), drawn on
    the sheet tech_frame already began."""
    rd = S.env["rad"]
    x0, W = X + PM * U, (PW - 2 * PM) * U
    edges = rad_scale(S)
    cols = ramp_hex(TECH_PAL["rad"], len(edges) + 1)
    lut = lut_classes(edges, cols)
    labels = ["< %.2f" % edges[0]] + ["%.2f-%.2f" % (edges[i], edges[i + 1]) for i in range(len(edges) - 1)] + ["> %.2f" % edges[-1]]
    months = {"spring": "MARCH-MAY", "summer": "JUNE-AUGUST", "autumn": "SEPTEMBER-NOVEMBER", "winter": "DECEMBER-FEBRUARY"}
    rowh = (top - bottom) / float(len(SEASONS))
    mh = rowh - 1.4 * U
    mw = min(W * 0.6, mh * S.F.w / S.F.h)
    def pic(sd):
        v = rd["seasons"][sd["key"]]["kwh"]
        gnd = np.where(rd["roof"], np.nan, v)
        roofv = np.where(rd["roof"], v, np.nan)
        p = os.path.join(d, "T4_solar_radiation_%s.png" % sd["key"])
        render_tech(p, S, S.F, 0.3, gnd, rd["nx"], rd["ny"], rd["cell"], 0.5, lut, roof="grid", roof_grid=roofv,
                    season=sd["key"], canopy_alpha=0.62, rkey=fp(S.env["keys"]["rad"], sd["key"], edges))
        return p
    ps = par_renders([(lambda sd_=sd: pic(sd_)) for sd in SEASONS])        # v18: the pictures side by side
    for k, sd in enumerate(SEASONS):
        y = top - k * rowh
        p = ps[k]
        V, wv, hv = tech_map(S, B, S.F, p, x0, y, mw, mh, U, L, scale=(k == len(SEASONS) - 1))
        sx = x0 + wv + 2.4 * U
        sw = x0 + W - sx
        t_title(B, sx, y, "{} · {} · {} DAYS".format(sd["name"], months[sd["key"]], days_in_season(sd["key"])), sw, U, L)
        yy = tech_bands(B, sx, y - 1.1 * U, sw, cols, labels, U, L, h=0.27,
                        title="kWh/m² per day · one scale, four seasons [6]")
        vis_tiles(B, sx, yy - 0.1 * U, sw, rad_tiles(S, sd["key"]), U, L, h=0.9)      # v38: tiles (was a paragraph)
    rects.append(("T4 · Solar radiation", (X, Y - PH * U, X + PW * U, Y)))


# ------------------------------------------------------------ wind, air and felt temperature: the period means
def comfort_sources(S=None):
    """v38: the climate and site sources of T5-T8 and their sections as the first five entries [1]-[5] of the sheet's
    numbered key (was one paragraph)."""
    CF = S.env.get("comfort") if S is not None else None
    lab = CF["label"] if CF else window_label()
    return ["Climate: the PVGIS typical meteorological year 2005-2020 for these coordinates (EU JRC): air temperature, "
            "humidity, 10 m wind and long-wave sky radiation from ERA5, sun from SARAH-2.",
            "Every map is the mean over " + lab + " of each season (input hours: daylight, all, or a range such as 10-17).",
            "Site: the buildings, terrain from the survey and PVGIS horizons.",
            canopy_note(S, short=True) if S is not None else "",
            height_note(S) if S is not None else ""]


def comfort_scales(S):
    """One wind scale and one temperature scale for the three sheets and their sections."""
    CF = S.env["comfort"]
    memo = env_memo(S)
    r = memo.get("comfort_scales")
    if r is not None:
        return r
    ts, ws = [], []
    for sd in SEASONS:
        c = CF["seasons"][sd["key"]]
        for k in ("ta", "utci"):
            v = c[k][np.isfinite(c[k])]
            if v.size:
                ts += [float(v.min()), float(v.max())]
        v = c["uped"][np.isfinite(c["uped"])]
        if v.size:
            ws.append(float(v.max()))
    lo, hi = 5.0 * math.floor(min(ts) / 5.0), 5.0 * math.ceil(max(ts) / 5.0)
    if hi - lo < 10.0:
        hi = lo + 10.0
    wmax = max(2.0, math.ceil(max(ws) * KT / 2.0) * 2.0 / KT) if ws else 2.0
    r = memo["comfort_scales"] = dict(t_range=(lo, hi), w_max=wmax)
    return r


def prevailing(c):
    """The sector the season's wind came from most often in the window (16 sectors) and its share of the hours."""
    tot = [sum(r) for r in c["rose"]]
    k = max(range(16), key=lambda q: tot[q])
    return k * 22.5, tot[k]


def sheet_wind(S, B, X, Y, U, rects, d):
    CF = S.env["comfort"]
    G = CF["grid"]
    wmax = comfort_scales(S)["w_max"]
    win_ = analysis_window(S, "wind")                 # v16.5: one window for the plan and every wind section
    scs = {sd["key"]: stretch_scale(WINDY_WIND, 0.0, WIND_SCALE_HI, CF["seasons"][sd["key"]]["uped"], to=WIND_STRETCH_TO,
                                    ab=win_) for sd in SEASONS}
    names = ("N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW")
    CP = Compass(S.env["E"]["location"]["lon"], S.env["E"]["location"]["lat"])

    def render(sd):
        c = CF["seasons"][sd["key"]]
        p = os.path.join(d, "T5_wind_%s.png" % sd["key"])
        dir_from, _ = prevailing(c)
        to = frame_dir(S.F, CP.vec((dir_from + 180.0) % 360.0))
        field = [[(None if not np.isfinite(v) else float(v)) for v in row] for row in c["uped"].reshape(G["ny"], G["nx"])]
        render_tech(p, S, S.F, 1.5, c["uped"], G["nx"], G["ny"], G["cell"], 0.5, scs[sd["key"]][0], roof="white",
                    season=sd["key"], canopy_alpha=0.22, relief=0.45, post=wind_streaks(S.F, 1.5, field, G["nx"], G["ny"], G["cell"], to),
                    rkey=fp(S.env["keys"]["comfort"], sd["key"], "uped", wmax))
        return p

    def side(sd, x, y, w, L):
        c = CF["seasons"][sd["key"]]
        dir_from, share = prevailing(c)
        t_title(B, x, y, "{} · MEAN OF {:,} HOURS · MOSTLY FROM {}".format(sd["name"], c["hours"], names[int(round(dir_from / 22.5)) % 16]),
                w, S.U, L)
        B.fit("{} · 10 m {:.2f} m/s ({:.2f} kt) · from {} {:.0f} % of hours [1]".format(        # v38: keywords
            CF["label_short"], c["u10_mean"], c["u10_mean"] * KT, names[int(round(dir_from / 22.5)) % 16], 100.0 * share),
            x, y - 0.9 * S.U, 0.3 * S.U, w, T_GREY, L)
        R = min(3.4 * S.U, (w - 2.0 * S.U) * 0.16)
        draw_wind_rose(B, x + R + 0.6 * S.U, y - 2.0 * S.U - R, R, c["rose"], c["calm"], page_north(S.F), S.U, L)
        tx = x + 2 * R + 2.0 * S.U
        tw_ = x + w - tx
        yb = stretch_bar(B, tx, y - 1.45 * S.U, tw_, WINDY_WIND, 0.0, WIND_SCALE_HI, scs[sd["key"]], S.U, L,
                         "kt at 1.5 m · mean · Windy colours 0-{:.0f} m/s = 0-{:.0f} kt [6]".format(
                             WIND_SCALE_HI, WIND_SCALE_HI * KT), k=KT, th=0.24, vals=c["uped"])
        vals = c["uped"][np.isfinite(c["uped"])]
        open_v = c["u10_mean"] * PED_WIND
        shel = 100.0 * float((vals < 0.5 * open_v).mean()) if vals.size else 0.0
        vis_tiles(B, tx, yb - 0.2 * S.U, tw_, [                  # v38: tiles (was a paragraph); calm stays on the rose
            ("wind", "OPEN GROUND · 1.5 m", "{:.2f} m/s · {:.2f} kt".format(open_v, open_v * KT), "[6]"),
            ("wind", "ACROSS THE SITE · MEAN", "{:.2f} m/s".format(float(vals.mean()) if vals.size else 0.0), "[6]"),
            ("build", "SHELTERED < HALF OPEN", "{:.0f} %".format(shel), "[6]")], S.U, L, h=0.9)
    tech_rows(S, B, X, Y, U, rects, "T5", "WIND · FOUR SEASONS",
              "Wind at 1.5 m · colour = speed · streaks = prevailing flow [6]",
              comfort_sources(S) + [
                  "Wind: every hour's 10 m wind (ERA5) brought to 1.5 m over open ground (log law, z0 0.1 m) "
                  "and reduced behind every building and crown upwind within 300 m (also beyond the frame) with measured "
                  "windbreak wake curves (Heisler & DeWalle 1988), for that hour's direction in 10-degree sectors; then "
                  "averaged; colours after Windy.",
                  "An estimate of shelter, not CFD: no corner jets or gusts. ERA5 wind is regional; valley "
                  "channelling is not resolved."],
              "Wind", render, side)


def draw_day_chart(B, x, ytop, w, h, series, lo, hi, U, L, window=None, bands=None, band_fill=None, unit="°C"):
    """24-hour curves by local hour. series: [(values[24] (None = no value), colour, width, label)], band_fill:
    (low[24], high[24], colour); window: the averaging window's hours, shaded."""
    X_ = lambda t: x + 1.6 * U + (w - 1.6 * U) * t / 24.0
    Y_ = lambda v: ytop - h + h * (max(lo, min(hi, v)) - lo) / (hi - lo)
    B.fill([rect(x + 1.6 * U, ytop - h, x + w, ytop)], (250, 250, 251), L, 20)
    if window is not None:
        for hh in range(24):
            if window[hh]:
                B.fill([rect(X_(max(0.0, hh - 0.5)), ytop - h, X_(min(24.0, hh + 0.5)), ytop)], (238, 238, 242), L, 20)
    for (b0, b1, col, lab) in (bands or []):
        if b1 <= lo or b0 >= hi:
            continue
        B.fill([rect(x + 1.6 * U, Y_(b0), x + w, Y_(b1))], col, L, 21)
        B.fit(lab, x + w - 0.15 * U, Y_(min(b1, hi)) - 0.3 * U, 0.2 * U, 9.0 * U, T_GREY, L, align="R")
    step = nice_step(hi - lo, 4)
    v = math.ceil(lo / step) * step
    while v <= hi + 1e-9:
        B.line([(x + 1.6 * U, Y_(v)), (x + w, Y_(v))], (214, 214, 220), L, 22, 0.02)
        B.text("%.0f" % v, x + 1.35 * U, Y_(v) - 0.1 * U, 0.24 * U, T_GREY, L, align="R")
        v += step
    for t in range(0, 25, 6):
        B.text("%02d:00" % (t % 24) if t < 24 else "24:00", X_(t), ytop - h - 0.5 * U, 0.22 * U, T_GREY, L, align="C")
    if band_fill:
        lo_v, hi_v, col = band_fill
        pts = [(X_(t), Y_(hi_v[t])) for t in range(24) if hi_v[t] is not None]          # values at the full hour
        pts += [(X_(t), Y_(lo_v[t])) for t in range(23, -1, -1) if lo_v[t] is not None]
        if len(pts) >= 3:
            B.fill([pts], col, L, 23)
    for vals, col, lw, lab in series:
        run = []
        for t in range(25):
            if t < 24 and vals[t] is not None:
                run.append((X_(t), Y_(vals[t])))
                continue
            if len(run) >= 2:
                B.line(run, col, L, 25, lw)
            run = []
    B.line(rect(x + 1.6 * U, ytop - h, x + w, ytop) + [(x + 1.6 * U, ytop - h)], T_RULE, L, 27, 0.04)
    B.text(unit, x + 1.6 * U, ytop + 0.45 * U, 0.22 * U, T_GREY, L, align="R")
    return ytop - h - 0.9 * U


def window_hours(CF):
    """Which local hours the averaging window holds (for the charts): 24 booleans."""
    kind, rng = CF["window"]
    if kind == "all":
        return [True] * 24
    if kind == "range":
        return [((hh - rng[0]) % 24) < (rng[1] - rng[0]) for hh in range(24)]
    return None


def sheet_air(S, B, X, Y, U, rects, d):
    CF = S.env["comfort"]
    G = CF["grid"]
    lo, hi = tsec_comfort_scales(S, tsec_lines(S))[1:]    # v16.5: the sections' scale, so plan and sections match
    win_ = analysis_window(S, "ta")                   # v16.5: one window for the plan and every air section
    scs = {sd["key"]: stretch_scale(WINDY_TEMP, lo, hi, CF["seasons"][sd["key"]]["ta"], ab=win_) for sd in SEASONS}

    def render(sd):
        c = CF["seasons"][sd["key"]]
        p = os.path.join(d, "T6_air_temperature_%s.png" % sd["key"])
        render_tech(p, S, S.F, 1.5, c["ta"], G["nx"], G["ny"], G["cell"], 0.5, scs[sd["key"]][0], roof="white", season=sd["key"],
                    canopy_alpha=0.22, rkey=fp(S.env["keys"]["comfort"], sd["key"], "ta", lo, hi))
        return p

    def side(sd, x, y, w, L):
        c = CF["seasons"][sd["key"]]
        t_title(B, x, y, "{} · MEAN OF {:,} HOURS · AIR {:.2f} °C · RH {:.0f} %".format(sd["name"], c["hours"], c["ta_mean"],
                                                                                     c["rh_mean"]), w, S.U, L)
        vals = c["ta"][np.isfinite(c["ta"])]
        B.fit("{} · dry bulb 2 m · only height changes it [6]".format(CF["label_short"]),          # v38: keywords
              x, y - 0.9 * S.U, 0.3 * S.U, w, T_GREY, L)
        yy = stretch_bar(B, x, y - 1.5 * S.U, w * 0.46, WINDY_TEMP, lo, hi, scs[sd["key"]], S.U, L,
                         "°C · same scale on T6 and T7", vals=c["ta"])
        day = c["day"]
        mean = [q[0] for q in day]
        p10 = [q[1] for q in day]
        p90 = [q[2] for q in day]
        vv = [v for v in p10 + p90 if v is not None]
        lo_c = math.floor(min(vv) / 5.0) * 5.0
        hi_c = math.ceil(max(vv) / 5.0) * 5.0
        draw_day_chart(B, x + w * 0.5, y - 1.95 * S.U, w * 0.5, 5.2 * S.U, [(mean, T_INK, 0.1, "mean")], lo_c, hi_c, S.U, L,
                       window=window_hours(CF), band_fill=(p10, p90, (226, 214, 190)))
        yy = vis_tiles(B, x, yy - 0.2 * S.U, w * 0.46, [          # v38: the site's range as a tile (was in a sentence)
            ("air", "ACROSS THE SITE · DRY BULB", "{:.2f}–{:.2f} °C".format(float(vals.min()), float(vals.max())), "[6]")],
            S.U, L, h=0.9)
        B.fit("chart: typical day · mean line · 80 % band [8]", x + w * 0.5 + 1.6 * S.U, y - 1.95 * S.U - 5.2 * S.U - 0.95 * S.U,
              0.22 * S.U, w * 0.5 - 1.6 * S.U, T_GREY, L)
    tech_rows(S, B, X, Y, U, rects, "T6", "AIR TEMPERATURE · DRY BULB · FOUR SEASONS",
              "Dry bulb °C · 2 m above ground · season mean · Windy [6]",
              comfort_sources(S) + [
                  "Dry bulb from the PVGIS climate data (ERA5-Land 2 m air temperature of its grid cell; "
                  "that cell's ground height is not reported), adjusted to the surveyed terrain with the standard lapse rate "
                  "(-0.65 K per 100 m) from PVGIS's point elevation ({:.0f} m), taken as its height (an assumption); colours "
                  "after Windy's scale.".format(CLIMATE["elevation"]),
                  "Street-scale air differences (shade, water, traffic) are small and are not modelled.",
                  "Chart: the season's typical day, every day of it: mean dry bulb by local hour (line) and the band holding "
                  "80 % of the hours. The air is the same across the site; how it feels is not (T7)."],
              "Air temperature", render, side)


def utci_reference_day(S, season):
    """The season's typical day by local hour for two reference spots, from every hour of it: open sun (whole sky, full
    sun, full wind) and street shade (half the sky, no direct sun, half the wind)."""
    memo = env_memo(S)
    mk = ("utci_ref", season)
    r = memo.get(mk)
    if r is not None:
        return r
    TT = S.env["TT"]
    m = TT["si"] == SEASON_INDEX[season]
    hs = np.flatnonzero(m)
    ta, rh = TT["t2m"][hs], TT["rh"][hs]
    pa = es_hpa_np(ta) * rh / 1000.0
    K = utci_K(ta, pa)
    el = TT["el"][hs]
    sun = el >= 2.0
    c1 = np.where(sun, MRT_K * proj_np(el) * TT["dni"][hs], 0.0)
    c2 = np.where(sun, MRT_K * 0.5 * F_EFF * (TT["dhi"][hs] + TT["ghi"][hs] * MRT_ALBEDO), 0.0)
    tsky = (np.maximum(1.0, TT["ir"][hs]) / (0.95 * 5.6697e-8)) ** 0.25 - 273.15
    out = {}
    for nm_, svf, T, wf in (("sun", 1.0, 1.0, 1.0), ("shade", 0.5, 0.0, 0.5)):
        D = svf * (c2 + 0.5 * (tsky - ta)) + c1 * T
        va = np.clip(TT["ws10"][hs] * wf, 0.5, 17.0)
        U_ = np.array([np.einsum("i,ij,j->", va[k] ** _P7, K[k, 0], D[k] ** _P7) for k in range(hs.size)])
        lh = TT["local"][hs]
        out[nm_] = [float(U_[lh == hh].mean()) if (lh == hh).any() else None for hh in range(24)]
    memo[mk] = out
    return out


def sheet_felt(S, B, X, Y, U, rects, d):
    CF = S.env["comfort"]
    G = CF["grid"]
    lo, hi = tsec_comfort_scales(S, tsec_lines(S))[1:]    # v16.5: the sections' scale, so plan and sections match
    win_ = analysis_window(S, "utci")                 # v16.5: one window for the plan and every felt section
    scs = {sd["key"]: stretch_scale(WINDY_TEMP, lo, hi, CF["seasons"][sd["key"]]["utci"], ab=win_) for sd in SEASONS}

    def render(sd):
        c = CF["seasons"][sd["key"]]
        p = os.path.join(d, "T7_felt_temperature_%s.png" % sd["key"])
        render_tech(p, S, S.F, 1.5, c["utci"], G["nx"], G["ny"], G["cell"], 0.5, scs[sd["key"]][0], roof="white", season=sd["key"],
                    canopy_alpha=0.22, rkey=fp(S.env["keys"]["comfort"], sd["key"], "utci", lo, hi))
        return p

    def side(sd, x, y, w, L):
        c = CF["seasons"][sd["key"]]
        vals = c["utci"][np.isfinite(c["utci"])]
        parts = []
        if c["utci_sun"] is not None:
            parts.append("{:.2f} °C IN SUN".format(c["utci_sun"]))
        if c["utci_shade"] is not None:
            parts.append("{:.2f} °C IN SHADE".format(c["utci_shade"]))
        t_title(B, x, y, "{} · MEAN FELT {:.2f} °C{}".format(sd["name"], float(vals.mean()) if vals.size else 0.0,
                                                             (" · " + " · ".join(parts)) if parts else ""), w, S.U, L)
        sv = c["sun"][np.isfinite(c["sun"])]
        B.fit("{} hours ({}) · air {:.2f} °C [1]".format("{:,}".format(c["hours"]), CF["label_short"], c["ta_mean"]),
              x, y - 0.9 * S.U, 0.3 * S.U, w, T_GREY, L)                     # v38: keywords; sun share as a tile
        sc_ = scs[sd["key"]]
        yy = stretch_bar(B, x, y - 1.5 * S.U, w * 0.46, WINDY_TEMP, lo, hi, sc_, S.U, L,
                         "UTCI °C, mean over the hours · same scale as T6", vals=c["utci"])
        yy = utci_band_marks(B, x, yy + 0.1 * S.U, w * 0.46, sc_[1], sc_[2], S.U, L)
        hist = c["hist"]
        tot = float(sum(hist)) or 1.0
        top = sorted(range(10), key=lambda k: -hist[k])[:4]
        tl = [("sun", "OPEN GROUND IN SUN · SUNNY h", "{:.0f} %".format(100.0 * float(sv.mean()) if sv.size else 0.0), "[7]")]
        tl += [("comfort" if k == 5 else "felt", (UTCI_NAMES[k] + ("" if k == 5 else " stress")).upper(),
                "{:.0f} %".format(100.0 * hist[k] / tot), "[6]") for k in sorted(top, key=lambda k: -k) if hist[k] > 0]
        vis_tiles(B, x, yy - 0.15 * S.U, w * 0.46, tl, S.U, L, cols=2, h=0.8)   # v38: every open spot, every hour (tiles)
        ref = utci_reference_day(S, sd["key"])
        site = c["by_hour"]
        vv = [v for v in ref["sun"] + ref["shade"] + site if v is not None]
        lo_c = math.floor(min(vv) / 5.0) * 5.0
        hi_c = math.ceil(max(vv) / 5.0) * 5.0
        bands = [(26.0, 32.0, (253, 236, 206), "moderate heat"), (32.0, 38.0, (250, 214, 180), "strong heat"),
                 (38.0, 46.0, (244, 186, 160), "very strong heat"), (46.0, 99.0, (232, 160, 150), "extreme heat"),
                 (0.0, 9.0, (214, 228, 240), "slight cold"), (-13.0, 0.0, (196, 214, 236), "moderate cold")]
        draw_day_chart(B, x + w * 0.5, y - 1.95 * S.U, w * 0.5, 5.2 * S.U,
                       [(ref["sun"], (200, 70, 30), 0.12, "open sun"), (ref["shade"], (40, 90, 150), 0.12, "street shade"),
                        (site, T_INK, 0.08, "site")], lo_c, hi_c, S.U, L, window=window_hours(CF), bands=bands)
        ky = y - 1.95 * S.U - 5.2 * S.U - 0.95 * S.U
        kx = x + w * 0.5 + 1.6 * S.U
        for col, lab in (((200, 70, 30), "open sun"), ((40, 90, 150), "street shade"), (T_INK, "this site's mean, window hours")):
            B.line([(kx, ky + 0.1 * S.U), (kx + 0.9 * S.U, ky + 0.1 * S.U)], col, L, 30, 0.14)
            B.text(lab, kx + 1.1 * S.U, ky, 0.22 * S.U, T_GREY, L)
            kx += 1.4 * S.U + tw(lab, 0.22 * S.U) + 0.6 * S.U
    tech_rows(S, B, X, Y, U, rects, "T7", "FELT TEMPERATURE · UTCI · FOUR SEASONS",
              "UTCI °C · air + humidity + wind + sun/shade · season [6]",
              comfort_sources(S) + [
                  "Universal Thermal Climate Index (Broede et al. 2012) every hour at every open 3 m cell, then averaged; "
                  "tiles: the share of every open spot and every hour in each stress class.",
                  "Mean radiant temperature from SolarCal (ASHRAE 55, outdoor form as in Ladybug): that hour's sun "
                  "or shade from every building, crown, the terrain and the ground's slope, the sky each spot sees, ground albedo "
                  "0.25 and the sky's long-wave radiation; that hour's wind as on T5.",
                  "Charts: the season's typical day; near "
                  "sunrise and sunset the site's mean holds only the days on which that hour is inside the window."],
              "Felt temperature", render, side)


# v33 (Aras Q12): the year in one map: the share of the window hours with no thermal stress (UTCI +9 to +26 °C,
# Blazejczyk et al. 2013, Geographia Polonica 86(1), Table 2, pp. 8-9) on every open 3 m cell, from the same hourly
# UTCI as T7 (Broede et al. 2012). Method sources: batch_2026-10-22/thread1_merge_audit/UTCI_SOURCES.md.
COMFORT_SHARE = ((0.0, (110, 44, 74)), (20.0, (190, 92, 78)), (40.0, (236, 178, 104)), (55.0, (240, 226, 170)),
                 (70.0, (170, 206, 150)), (85.0, (86, 156, 110)), (100.0, (30, 100, 80)))


def sheet_comfort_year(S, B, X, Y, U, rects, d):
    CF = S.env["comfort"]
    G = CF["grid"]
    Yr = CF["year"]
    sc = (stops_table(COMFORT_SHARE, 0.0, 100.0), 0.0, 100.0, 1.0)

    def render(sd):
        p = os.path.join(d, "T8_comfortable_hours_year.png")
        render_tech(p, S, S.F, 1.5, Yr["comfort"], G["nx"], G["ny"], G["cell"], 0.5, sc[0], roof="white",
                    canopy_alpha=0.22, rkey=fp(S.env["keys"]["comfort"], "year", "comfort9-26"))
        return p

    def side(sd, x, y, w, L):
        v = Yr["comfort"][np.isfinite(Yr["comfort"])]
        v18 = Yr["comfort18"][np.isfinite(Yr["comfort18"])]
        u = Yr["utci"][np.isfinite(Yr["utci"])]
        t_title(B, x, y, "THE YEAR · {:.0f} % OF THE {} NEITHER HOT NOR COLD".format(
            float(v.mean()) if v.size else 0.0, CF["label_short"].upper()), w, S.U, L)
        B.fit("{} · as T7 [1]".format(CF["label_short"]), x, y - 0.9 * S.U, 0.3 * S.U, w, T_GREY, L)   # v38: keywords
        yy = stretch_bar(B, x, y - 1.5 * S.U, w * 0.6, COMFORT_SHARE, 0.0, 100.0, sc, S.U, L,
                         "% of the hours with no thermal stress · UTCI 9 to 26 °C [7]", vals=Yr["comfort"], dec=0)
        yy = vis_tiles(B, x, yy - 0.15 * S.U, w * 0.6, [         # v38: the year's figures as tiles (were sentences)
            ("clock", "HOURS", "{:,}".format(Yr["hours"]), "[2]"),
            ("felt", "MEAN FELT · UTCI", "{:.2f} °C".format(float(u.mean()) if u.size else 0.0), "[6]"),
            ("comfort", "BEST SPOT", "{:.0f} %".format(float(v.max()) if v.size else 0.0), "[7]"),
            ("felt", "WORST SPOT", "{:.0f} %".format(float(v.min()) if v.size else 0.0), "[7]")], S.U, L, h=0.9)
        yy = vis_tiles(B, x, yy - 0.3 * S.U, w * 0.6, [("comfort", sd_["name"], "{:.0f} %".format(Yr["share"][sd_["key"]]), "[7]")
                                                     for sd_ in SEASONS], S.U, L, h=0.9)
        vis_tiles(B, x, yy - 0.3 * S.U, (w * 0.6 - 0.9 * S.U) / 4.0, [
            ("comfort", "18-26 °C · NEAR COMFORT", "{:.0f} %".format(float(v18.mean()) if v18.size else 0.0), "[8]")],
            S.U, L, h=0.9)
    tech_rows(S, B, X, Y, U, rects, "T8", "COMFORTABLE HOURS · UTCI · THE WHOLE YEAR",
              "% of hours neither hot nor cold · the whole year · as T7 [7]",
              comfort_sources(S) + [
                  "Universal Thermal Climate Index every hour at every open 3 m cell (Broede et al. "
                  "2012, Int J Biometeorol 56(3):481-494); the same hours, sun, shade and wind as T7.",
                  "Counted as comfortable when it lies in the index's 'no thermal "
                  "stress' band, +9 to +26 °C (Blazejczyk et al. 2013, Geographia Polonica 86(1):5-10, Table 2), for its "
                  "reference person walking at 4 km/h (same, p. 7).",
                  "The narrower 18 to 26 °C part of the band, which the UTCI's authors say may come close to a thermal "
                  "comfort zone: the share of the hours on average.",
                  "Mapping the year's share of comfortable time follows "
                  "Nazarian et al. 2019 (Building and Environment 155:145-160)."],
              "Comfortable hours", render, side, items=[dict(key="year", name="THE YEAR")])


# ------------------------------------------------------------ pages
def noise_at(nm, F, x, y, key="lden"):
    u, v = F.local(x, y)
    fi, fj = (u - F.u0) / nm["cell"], (v - F.v0) / nm["cell"]
    i0, j0 = int(math.floor(fi)), int(math.floor(fj))
    num = den = 0.0
    for di in (0, 1):
        for dj in (0, 1):
            i, j = i0 + di, j0 + dj
            if 0 <= j < nm["ny"] and 0 <= i < nm["nx"]:
                c = nm["grid"][j][i]
                if c and c.get(key) is not None:
                    w_ = (1 - abs(fi - i)) * (1 - abs(fj - j))
                    num += w_ * c[key]
                    den += w_
    return num / den if den > 0.2 else None


B_CUR = [None]


# ============================================================ TECHNICAL · top views of the 3D site, rendered to pixels
# Every analysis is shown over the same 3D map seen from above: terrain relief from the surveyed heights, buildings as
# volumes (surveyed floors x storey height) with cast shadows and drawn edges, the measured tree crowns as shaded 3D
# canopies, and the river as water. Pure python, written to PNG; placed on the technical sheets as picture frames.
import zlib as _zlib
from bisect import bisect_right as _bisect_right
import struct as _struct

TECH_LIGHT = (-0.70710678, 0.70710678)      # light from the upper left of every sheet (cartographic convention)


def tech_relief(S, frame):
    """Terrain relief of one frame: surveyed heights on a 6 m grid, smoothed twice, lit from the upper left. 1.0 on
    level ground, so the colours of an analysis stay true there; lighter on slopes facing the light, darker away.
    The same grid serves every resolution of that frame (and is kept between runs)."""
    ST = getattr(S, "store", None) or Store()
    key = fp("relief", MV["relief"], site_prints(S)["terrain"], frame.P)
    r = ST.get("relief", key)
    if r is not None:
        return r
    gc = 6.0
    gx, gy = int(math.ceil(frame.w / gc)) + 2, int(math.ceil(frame.h / gc)) + 2
    ii, jj = np.meshgrid(np.arange(gx), np.arange(gy))
    X, Y = f_world(frame, frame.u0 + (ii.ravel() - 0.5) * gc, frame.v0 + (jj.ravel() - 0.5) * gc)
    Z = z_np(S, X, Y).reshape(gy, gx)
    for _ in range(2):
        P = np.pad(Z, 1, mode="edge")
        Z = sum(P[dj:dj + gy, di:di + gx] for dj in range(3) for di in range(3)) / 9.0
    P = np.pad(Z, 1, mode="edge")
    zx = (P[1:-1, 2:] - P[1:-1, :-2]) / (2 * gc) * 1.6
    zy = (P[2:, 1:-1] - P[:-2, 1:-1]) / (2 * gc) * 1.6
    n_ = np.sqrt(zx * zx + zy * zy + 1.0)
    lit = (-zx * TECH_LIGHT[0] - zy * TECH_LIGHT[1]) / n_ * 0.7 + 1.0 / n_ * 0.7
    return ST.put("relief", key, (gc, gx, gy, (1.0 + 0.42 * (lit - 0.7)).astype(np.float32)))


def disc_pixels(cu, cv, r, u0, vtop, res, w, h):
    """Pixels (top row first) whose centres lie within each disc: (disc index, pixel index, pixel u, pixel v)."""
    e = np.zeros(0, np.int64)
    if np.size(cu) == 0:
        return e, e, np.zeros(0), np.zeros(0)
    p0 = np.clip(np.ceil((vtop - (cv + r)) / res - 0.5).astype(np.int64), 0, h)
    p1 = np.clip(np.floor((vtop - (cv - r)) / res - 0.5).astype(np.int64) + 1, 0, h)
    cnt = np.maximum(p1 - p0, 0)
    tot = int(cnt.sum())
    q = np.repeat(np.arange(cu.size), cnt)
    py = p0[q] + (np.arange(tot) - np.repeat(np.cumsum(cnt) - cnt, cnt))
    vc = vtop - (py + 0.5) * res
    hw = np.sqrt(np.maximum(r[q] ** 2 - (vc - cv[q]) ** 2, 0.0))
    a0 = np.clip(np.ceil((cu[q] - hw - u0) / res - 0.5).astype(np.int64), 0, w)
    a1 = np.clip(np.floor((cu[q] + hw - u0) / res - 0.5).astype(np.int64) + 1, 0, w)
    c = np.maximum(a1 - a0, 0)
    t2 = int(c.sum())
    rep = np.repeat(np.arange(c.size), c)
    px = a0[rep] + (np.arange(t2) - np.repeat(np.cumsum(c) - c, c))
    k = q[rep]
    pu = u0 + (px + 0.5) * res
    pv = vc[rep]
    keep = (pu - cu[k]) ** 2 + (pv - cv[k]) ** 2 <= r[k] ** 2
    return k[keep], (py[rep] * w + px)[keep], pu[keep], pv[keep]


_TECH_LOCK = _threading.RLock()     # v18: one picture thread builds the shared map layers, the others wait for them


def tech_core(S, frame, res):
    with _TECH_LOCK:
        return _tech_core(S, frame, res)


def _tech_core(S, frame, res):
    """The layers of the 3D map that do not change with the season, for one frame and resolution: buildings (index per
    pixel, courtyards open), their one-pixel edges, the tree crowns (shaded as spheres, and which kind is on top),
    water, the river outline and the terrain relief. Built once; every sheet and season shares it."""
    key = core_key(S, frame, res)
    live = tech_store(S).get(key)
    if live is not None:
        return live
    ST = getattr(S, "store", None) or Store()
    bl, gB, trees = S.env["solids"]
    port = ST.get("core", key)
    if port is not None:
        live = dict(port, cv=Canvas(frame, res), blist=[bl[i] for i in port["bl_idx"]])
        tech_store(S)[key] = live
        return live
    cv = Canvas(frame, res)
    w, h = cv.w, cv.h
    loc = frame.local
    fb = frame.bb
    fbx = (fb[0] - 120, fb[1] - 120, fb[2] + 120, fb[3] + 120)
    vtop = frame.v0 + frame.h
    vbot = vtop - h * res                                 # the pixel rows counted from the bottom start here
    blist = [b for b in bl if bb_hit(b["bb"], fbx)]
    groups = [[[loc(x, y) for x, y in b["P"]]] + [[loc(x, y) for x, y in H_] for H_ in (b.get("holes") or ())]
              for b in blist]
    bv = footprint_values(groups, np.arange(1, len(blist) + 1), frame.u0, vbot, res, w, h)
    bid = np.where(np.isfinite(bv), bv, 0.0).astype(np.int32).reshape(h, w)[::-1].copy()
    P = np.pad(bid, 1, constant_values=-1)
    edge = (bid > 0) & ((P[1:-1, :-2] != bid) | (P[1:-1, 2:] != bid) | (P[:-2, 1:-1] != bid) | (P[2:, 1:-1] != bid))
    # tree crowns lit like spheres; cwin = the kind of tree on top (1 evergreen, 2 deciduous)
    canopy = np.zeros(w * h, np.float32)
    cwin = np.zeros(w * h, np.uint8)
    tr = [t for t in trees if fbx[0] <= t["x"] <= fbx[2] and fbx[1] <= t["y"] <= fbx[3]]
    if tr:
        lc = [loc(t["x"], t["y"]) for t in tr]
        cu = np.array([p[0] for p in lc])
        cvv = np.array([p[1] for p in lc])
        rr = np.array([t["r"] for t in tr])
        ever = np.array([1 if t["kind"] in EVERGREEN else 2 for t in tr], np.uint8)
        k, pix, pu, pv = disc_pixels(cu, cvv, rr, frame.u0, vtop, res, w, h)
        nx_ = (pu - cu[k]) / rr[k]
        ny_ = (pv - cvv[k]) / rr[k]
        nz = np.sqrt(np.maximum(0.0, 1.0 - nx_ * nx_ - ny_ * ny_))
        f_ = 0.55 + 0.55 * np.maximum(0.0, 0.55 * (nx_ * TECH_LIGHT[0] + ny_ * TECH_LIGHT[1]) + 0.75 * nz)
        np.maximum.at(canopy, pix, f_.astype(np.float32))
        top = f_.astype(np.float32) >= canopy[pix]
        cwin[pix[top]] = ever[k[top]]
    # water and the river outline (water pixels outside buildings next to dry ground; the map border does not count)
    wg = [[[loc(x, y) for x, y in L_] for L_ in [wp["P"]] + list(wp.get("H", []))] for wp in S.water]
    water = (footprint_values(wg, np.ones(len(wg)), frame.u0, vbot, res, w, h) > -np.inf).reshape(h, w)[::-1].copy()
    Pw = np.pad(water, 1, constant_values=True)
    dry = ~Pw[1:-1, :-2] | ~Pw[1:-1, 2:] | ~Pw[:-2, 1:-1] | ~Pw[2:, 1:-1]
    wedge = water & (bid == 0) & dry
    # terrain relief spread to the pixels (bilinear)
    gc, gx, gy, HS = tech_relief(S, frame)
    fi = (np.arange(w) + 0.5) * res / gc + 0.5
    i0 = np.minimum(gx - 2, fi.astype(np.int64))
    ti = (fi - i0)[None, :]
    vc = vtop - (np.arange(h) + 0.5) * res
    fj = (vc - frame.v0) / gc + 0.5
    j0 = np.clip(fj.astype(np.int64), 0, gy - 2)
    tj = np.clip(fj - j0, 0.0, 1.0)[:, None]
    J0, I0 = j0[:, None], i0[None, :]
    hs = ((HS[J0, I0] * (1 - ti) + HS[J0, I0 + 1] * ti) * (1 - tj) + (HS[J0 + 1, I0] * (1 - ti) + HS[J0 + 1, I0 + 1] * ti) * tj)
    bindex = S.env.get("bindex") or dict((id(b), i) for i, b in enumerate(bl))
    port = dict(bid=bid.ravel(), bl_idx=[bindex[id(b)] for b in blist], edge=edge.ravel(), canopy=canopy, cwin=cwin,
                water=water.ravel(), wedge=wedge.ravel(), hs=hs.astype(np.float32).ravel())
    ST.put("core", key, port)
    out = dict(port, cv=cv, blist=blist)
    tech_store(S)[key] = out
    return out


def core_key(S, frame, res):
    pr = site_prints(S)
    return fp("core", MV["core"], S.env["keys"]["solids"], pr["water"], pr["terrain"], frame.P, res)


def tech_base(S, frame, res, season=None):
    """Shared layers of the 3D map for one frame and resolution; the season only decides which crowns are in leaf."""
    with _TECH_LOCK:
        return _tech_base(S, frame, res, season)


def _tech_base(S, frame, res, season=None):
    core = tech_core(S, frame, res)
    if season is None or leaf_key(season):
        ck = core.get("ck_leaf")
        if ck is None:
            ck = core["ck_leaf"] = np.where(core["cwin"] == 2, 1, core["cwin"]).astype(np.uint8)
    else:
        ck = core["cwin"]
    return dict(core, ckind=ck)


def np_grid(grid, nx, ny):
    """An analysis grid as a (ny, nx) float array, None -> NaN (lists of rows or a flat / 2D array)."""
    if isinstance(grid, np.ndarray):
        return grid.astype(float).reshape(ny, nx)
    return np.array([[(np.nan if v is None else v) for v in row] for row in grid], float).reshape(ny, nx)


def fill_nan(G, passes=12):
    """Fill empty cells (under roofs) from their neighbours so interpolation never meets a gap (as fill_none)."""
    G = G.copy()
    for _ in range(passes):
        m = np.isnan(G)
        if not m.any():
            break
        V = np.where(m, 0.0, G)
        W = (~m).astype(float)
        Vp = np.pad(V, 1)
        Wp = np.pad(W, 1)
        ny, nx = G.shape
        sv = sum(Vp[dj:dj + ny, di:di + nx] for dj in range(3) for di in range(3))
        sw = sum(Wp[dj:dj + ny, di:di + nx] for dj in range(3) for di in range(3))
        fillable = m & (sw > 0)
        if not fillable.any():
            break
        G[fillable] = sv[fillable] / sw[fillable]
    return np.where(np.isnan(G), 0.0, G)


def lut_np(colour, v):
    """The colours of a lut_ramp / lut_classes / stops_table scale for an array of values: (..., 3) floats."""
    lut = getattr(colour, "_lut", None)
    if lut is not None and lut[0] == "ramp":
        _, vmin, span, n, table = lut
        q = np.clip(((v - vmin) / span * (n - 1)).astype(np.int64), 0, n - 1)
        return np.array(table, float)[q]
    if lut is not None and lut[0] == "classes":
        _, edges, cols = lut
        q = np.minimum(np.searchsorted(np.array(edges, float), v, side="right"), len(cols) - 1)
        return np.array(cols, float)[q]
    flat = v.ravel()
    return np.array([colour(x) for x in flat], float).reshape(v.shape + (3,))


TECH_NODATA = (222, 222, 226)
SHADE_CELL = 1.0           # v16.6: m, the plan's shade grid (T3; v16.5: 3.0, shared with the comfort grid)
COMFORT_CELL = 2.0         # v16.6: m, the plan's wind, air and felt temperature grid (T5-T7; v16.5: 3.0)
TECH_TREES_UNDER = True    # v16.6: on the technical maps the tree crowns are drawn as thin outlines over the analysis
#                            colours, which show whole inside them (v16.5: a green wash of 22-62 % over the colours hid
#                            the values under the crowns). False restores the wash.


def render_tech(path, S, frame, res, grid, nx, ny, cell, off, colour, roof="white", roof_vals=None, roof_grid=None,
                season=None, canopy_alpha=0.45, water_mix=0.6, grid_frame=None, post=None, relief=1.0, rkey=None,
                nodata=None, **_):
    """Composite one analysis over the 3D map and write a PNG. grid values sit at grid_frame.u0 + (i + off) * cell
    (NaN or None: no value there, filled from the neighbours, e.g. under roofs); nodata (cells) are drawn grey: not
    computed. Roofs: white, the field lightened ("field"), one value per building ("values") or their own cells
    (roof_grid). With rkey (the fingerprint of the analysis data) an unchanged map already on disk is kept."""
    full = None
    lut_ = getattr(colour, "_lut", None)
    if rkey is not None and lut_ is not None and (post is None or getattr(post, "_key", None) is not None):
        gf_ = grid_frame or frame
        full = fp("png", MV["render"], TECH_TREES_UNDER, rkey, core_key(S, frame, res), season is None or leaf_key(season),
                  roof, None if roof_vals is None else sorted((S.env["bindex"][i_], v_) for i_, v_ in
                                                               ((id(b), roof_vals.get(id(b))) for b in S.env["solids"][0])
                                                               if v_ is not None),
                  canopy_alpha, water_mix, relief, off, cell, nx, ny, lut_, getattr(post, "_key", None), frame.P, gf_.P, res)
        d_ = os.path.dirname(path)
        e_ = maps_index(S, d_).get(os.path.basename(path))
        try:
            if e_ and e_.get("key") == full and os.path.getsize(path) == e_.get("size"):
                _rt_after(lambda: S.env.setdefault("maps_kept", []).append(os.path.basename(path)))
                return e_["w"], e_["h"]
        except Exception:
            pass
    TB = tech_base(S, frame, res, season)
    cv = TB["cv"]
    w, h = cv.w, cv.h
    gf = grid_frame or frame
    G = np_grid(grid, nx, ny)
    if gf is frame:
        fi = ((np.arange(w) + 0.5) * res) / cell - off
        i0 = np.clip(np.floor(fi).astype(np.int64), 0, nx - 2)[None, :]
        ti = np.clip(fi - i0[0], 0.0, 1.0)[None, :]
        fj = (frame.h - (np.arange(h) + 0.5) * res) / cell - off
        j0 = np.clip(np.floor(fj).astype(np.int64), 0, ny - 2)[:, None]
        tj = np.clip(fj - j0[:, 0], 0.0, 1.0)[:, None]
    else:                                                 # the grid of another frame: each pixel through world coordinates
        PU, PV = np.meshgrid(frame.u0 + (np.arange(w) + 0.5) * res, frame.v0 + frame.h - (np.arange(h) + 0.5) * res)
        gu, gv = f_local(gf, *f_world(frame, PU, PV))
        fi = (gu - gf.u0) / cell - off
        fj = (gv - gf.v0) / cell - off
        i0 = np.clip(np.floor(fi).astype(np.int64), 0, nx - 2)
        j0 = np.clip(np.floor(fj).astype(np.int64), 0, ny - 2)
        ti = np.clip(fi - i0, 0.0, 1.0)
        tj = np.clip(fj - j0, 0.0, 1.0)

    def interp(A):
        return ((A[j0, i0] * (1 - ti) + A[j0, i0 + 1] * ti) * (1 - tj) + (A[j0 + 1, i0] * (1 - ti) + A[j0 + 1, i0 + 1] * ti) * tj)
    V = interp(fill_nan(G))
    rgb = lut_np(colour, V) * (1.0 + (TB["hs"].reshape(h, w) - 1.0) * relief)[..., None]
    if nodata is not None:
        nd = interp(np.asarray(nodata, float).reshape(ny, nx)) > 0.5
        rgb[nd] = TECH_NODATA
    water = TB["water"].reshape(h, w)
    wedge = TB["wedge"].reshape(h, w)
    wm = water & ~wedge
    rgb[wm] = rgb[wm] * (1.0 - water_mix) + np.array((126.0, 168.0, 196.0)) * water_mix
    rgb[wedge] = (44.0, 92.0, 132.0)
    a = TB["canopy"].reshape(h, w).astype(float)
    ck = TB["ckind"].reshape(h, w)
    for kind, lc, al in ((1, (88.0, 128.0, 62.0), canopy_alpha), (2, (128.0, 112.0, 90.0), canopy_alpha * 0.45)):
        m = (a > 0.0) & (ck == kind)
        if not m.any():
            continue
        if TECH_TREES_UNDER:                              # v16.6: the crowns' outlines only, the analysis whole inside
            inner = m.copy()
            inner[1:, :] &= m[:-1, :]
            inner[:-1, :] &= m[1:, :]
            inner[:, 1:] &= m[:, :-1]
            inner[:, :-1] &= m[:, 1:]
            e = m & ~inner
            ao = min(0.85, 0.35 + al)
            rgb[e] = rgb[e] * (1.0 - ao) + np.array(lc) * 0.55 * ao
        else:
            rgb[m] = rgb[m] * (1.0 - al) + np.array(lc) * a[m][:, None] * al
    bid = TB["bid"].reshape(h, w)
    inb = bid > 0
    if roof == "field":
        c0 = np.floor(lut_np(colour, V[inb]))
        rgb[inb] = c0 + np.floor((255.0 - c0) / 6.0)
    elif roof == "values" and roof_vals is not None:
        cols = np.full((len(TB["blist"]) + 1, 3), 255.0)
        for k, b in enumerate(TB["blist"]):
            v_ = roof_vals.get(id(b))
            if v_ is not None:
                cols[k + 1] = colour(v_)
        rgb[inb] = cols[bid[inb]]
    elif roof == "grid" and roof_grid is not None:
        rgb[inb] = lut_np(colour, interp(fill_nan(np_grid(roof_grid, nx, ny)))[inb])
    else:
        rgb[inb] = 255.0
    rgb[TB["edge"].reshape(h, w)] = (34.0, 34.0, 38.0)
    out = np.clip(rgb, 0, 255).astype(np.uint8)
    out[0, :] = out[-1, :] = (34, 34, 38)                 # thin frame
    out[:, 0] = out[:, -1] = (34, 34, 38)
    buf = bytearray(out.tobytes())
    if post is not None:
        post(buf, w, h, TB)
    png_write(path, w, h, buf)
    if full is not None:
        def note():
            try:
                d_ = os.path.dirname(path)
                maps_index(S, d_)[os.path.basename(path)] = dict(key=full, size=os.path.getsize(path), w=w, h=h)
                maps_index_save(S, d_)
            except Exception:
                pass
        _rt_after(note)
    return w, h


_RT = _threading.local()


def _rt_after(fn):
    """v18: bookkeeping of a map picture (the index of kept maps): now, or, on a picture thread, after all pictures
    are done, in the pictures' order, so the index is written exactly as by one thread."""
    lst = getattr(_RT, "after", None)
    if lst is None:
        fn()
    else:
        lst.append(fn)


RENDER_GB = 1.5           # v18: memory one 17-megapixel map picture takes while it is made (measured peak 1.22 GB)


def par_renders(fns):
    """v18: map pictures (render_tech) on several threads at once: numpy, which does the work, runs outside Python's
    lock. Each picture is made by exactly the same code as on one thread; results come back in order and the
    bookkeeping is done afterwards in that order. As many at once as the cores and half the memory allow."""
    fns = list(fns)
    r = _ram_gb()
    n = min(len(fns), PAR_THREADS or n_cores(), 4 if r is None else max(1, int(0.5 * r / RENDER_GB)))
    if n < 2 or not PAR_JOBS:
        return [f() for f in fns]
    from concurrent.futures import ThreadPoolExecutor

    def run(f):
        _RT.after = []
        try:
            return f(), _RT.after
        finally:
            _RT.after = None
    with ThreadPoolExecutor(n) as ex:
        outs = list(ex.map(run, fns))
    res = []
    for v, after in outs:
        for a in after:
            a()
        res.append(v)
    return res


def png_write(path, w, h, rgb):
    """RGB bytes (rows from the top) to a PNG file (filter 0 on every row)."""
    a = np.frombuffer(bytes(rgb), np.uint8).reshape(h, w * 3)
    raw = np.concatenate([np.zeros((h, 1), np.uint8), a], 1).tobytes()

    def chunk(t, d):
        return _struct.pack(">I", len(d)) + t + d + _struct.pack(">I", _zlib.crc32(t + d) & 0xffffffff)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", _struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                + chunk(b"IDAT", _zlib.compress(raw, 6)) + chunk(b"IEND", b""))


class Canvas(object):
    """Pixels over a frame: column 0 at u0, row 0 at the top (v1)."""

    def __init__(self, frame, res):
        self.F, self.res = frame, res
        self.w = int(math.ceil(frame.w / res))
        self.h = int(math.ceil(frame.h / res))

    def rows(self, L_):
        """Scanline a convex polygon in frame-local coordinates: [(row, first column, end column)]."""
        n = len(L_)
        if n < 3:
            return []
        F, r = self.F, self.res
        v1 = F.v0 + F.h
        ys = [p[1] for p in L_]
        vmin, vmax = min(ys), max(ys)
        p0 = max(0, int(math.ceil((v1 - vmax) / r - 0.5)))
        p1 = min(self.h - 1, int(math.floor((v1 - vmin) / r - 0.5)))
        if p1 < p0:
            return []
        edges = []
        for k in range(n):
            (x0, y0), (x1, y1) = L_[k], L_[(k + 1) % n]
            if y0 != y1:
                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                edges.append((y0, y1, x0, (x1 - x0) / (y1 - y0)))
        out = []
        u0, W = F.u0, self.w
        ceil, floor = math.ceil, math.floor
        for py in range(p0, p1 + 1):
            vc = v1 - (py + 0.5) * r
            lo = hi = None
            for y0, y1, x0, sl in edges:
                if y0 <= vc < y1:
                    x = x0 + (vc - y0) * sl
                    if lo is None or x < lo:
                        lo = x
                    if hi is None or x > hi:
                        hi = x
            if lo is not None:
                a0 = max(0, int(ceil((lo - u0) / r - 0.5)))
                a1 = min(W, int(floor((hi - u0) / r - 0.5)) + 1)
                if a1 > a0:
                    out.append((py, a0, a1))
        return out


def tech_store(S):
    """Per-site store of the 3D map layers (kept with the environment analyses, so later bakes reuse them)."""
    st = S.env.get("tech_cache")
    if st is None:
        st = S.env["tech_cache"] = {}
    return st


# ------------------------------------------------------------ palettes (from the reference analyses)
def hexrgb(hx):
    hx = hx.lstrip("#")
    return (int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16))


TECH_PAL = {
    # shading time, after the shading-hours reference: sun (pale yellow) to deep shade (navy)
    "shade": ["FFF6B8", "FFE14A", "FDB52B", "F7832A", "EE4B3A", "E2276E", "B5279B", "7B2FBE", "3E4FD1", "1F3A93", "0B1340"],
    # road noise bands in the colour order of the Brussels noise map (green to yellow to red, then blue and violet),
    # over 11 DIN-style 5 dB classes 35-80 dB(A); not the Brussels map's 8 classes or its colours (v21, R01-17)
    "noise": ["A7D49B", "74B86A", "C9E27A", "FFE45C", "FDBA3B", "F68B2D", "E8432F", "B71F3A", "6A6FC7", "7E3FA8", "3C3C4E"],
    # v16.4 default: the same 5 dB bands as one graded run, every band darker than the one before (CIE L* 97, 93, 91,
    # 89, 83, 74, 64, 53, 41, 27, 13): the Brussels colours turn from dark red to blue and violet for the two loudest
    # bands (70-80 dB), and blue reads as quiet, so the loudest streets looked like the quietest strips of the map
    "noise_graded": ["F4F8EA", "E4F0CC", "DDEBAA", "F3E27E", "FAC659", "F5A443", "EC7D36", "DB5130", "B72A2F", "7D172E",
                     "40101F"],
    # surface temperature: the diverging red-blue of the surface temperature reference (RdBu)
    "heat": ["053061", "2166AC", "4393C3", "92C5DE", "D1E5F0", "F7F7F7", "FDDBC7", "F4A582", "D6604D", "B2182B", "67001F"],
    # incident radiation: yellow to red, after the radiation reference
    "rad": ["FFF46B", "FBD435", "F7B728", "F39A22", "EE7E21", "EA6220", "E5461D", "DF2A1A", "C21515"],
}


def lut_classes(edges, cols):
    """Banded colours: value -> class colour (edges ascending, len(cols) == len(edges) + 1)."""
    cols = [hexrgb(c) if isinstance(c, str) else c for c in cols]

    def f(v):
        k = 0
        for e in edges:
            if v >= e:
                k += 1
        return cols[min(k, len(cols) - 1)]
    if all(edges[q] <= edges[q + 1] for q in range(len(edges) - 1)):
        f._lut = ("classes", list(edges), cols)        # same answer as counting, read with a binary search
    return f


def lut_ramp(vmin, vmax, hexes, n=512):
    cols = [hexrgb(c) for c in hexes]
    table = []
    for k in range(n):
        t = k / float(n - 1) * (len(cols) - 1)
        i = min(len(cols) - 2, int(t))
        f = t - i
        table.append(tuple(int(round(cols[i][q] * (1 - f) + cols[i + 1][q] * f)) for q in range(3)))
    span = max(1e-9, vmax - vmin)

    def g(v):
        k = int((v - vmin) / span * (n - 1))
        return table[0 if k < 0 else (n - 1 if k >= n else k)]
    g._lut = ("ramp", vmin, span, n, table)
    return g


def maps_index(S, d):
    """Which map file was rendered from what (fingerprint, size, pixel size): lets a later bake keep a map whose
    inputs did not change instead of rendering it again."""
    memo = S.env.setdefault("memo", {})
    k = ("maps_index", d)
    idx = memo.get(k)
    if idx is None:
        idx = {}
        try:
            with open(os.path.join(d, ".selinus_maps_index.json"), "r", encoding="utf-8") as f:
                idx = json.load(f)
        except Exception:
            idx = {}
        memo[k] = idx
    return idx


def maps_index_save(S, d):
    try:
        with open(os.path.join(d, ".selinus_maps_index.json"), "w", encoding="utf-8") as f:
            json.dump(maps_index(S, d), f)
    except Exception:
        pass


# ============================================================ TECHNICAL SHEETS (white technical-drawing style)
import os
RUN_MODE = str(inp("mode", "") or "").strip().lower()                     # v37: was the input run
RUN_MODE = {"drawings": "board", "board": "board", "0": "board", "0.0": "board",
            "technical": "technical", "technical analysis": "technical", "analysis": "technical", "1": "technical",
            "1.0": "technical", "both": "all", "all": "all", "2": "all", "2.0": "all"}.get(RUN_MODE, "all" if (ENVIRONMENT or ENV_PATH) else "board")
if RUN_MODE == "board" and not str(inp("mode", "") or "").strip():
    LOG.append("mode: the land-use pages and drawings only; give env_path (bergama_environment.json) to bake the "
               "technical sheets with them in the same press.")
TECH_IDS = []
T_INK = (24, 24, 28)
T_GREY = (105, 105, 112)
T_RULE = (40, 40, 46)
T_BG = (255, 255, 255)


def tech_dir():
    base = SELINUS_OUT_DIR                                   # v33 24 Oct (Aras rule); was beside env_path
    d = os.path.join(base, "selinus_technical_maps")
    try:
        if not os.path.isdir(d):
            os.makedirs(d)
    except Exception:
        d = base
    return d


def t_title(B, x, y, txt, w, U, L, h=0.62):
    B.fit(txt, x, y, h * U, w, T_INK, L, font=FONT_TITLE, bold=True)


# ------------------------------------------------------------ v38 (Aras 25 Oct 17:00, visual first; SCRIPT_STANDARD 5b)
# Readings become pictogram tiles (icon, keyword, ONE big figure, [n]); method and source sentences become ONE numbered
# key in the sheet's footer (the water board v1.6 method: icon(), tiles(), cite() + SRC_KEY, adapted to the Board API).
def src_key_text(entries):
    """v38: a sheet's method and source sentences as one numbered key, "[1] ...  [2] ...". The numbers are the [n]
    marks on that sheet, so an entry keeps its place even when it is empty."""
    return u"  ".join(u"[{}] {}".format(i + 1, (e or u"-").strip()) for i, e in enumerate(entries))


BOARD_KEY = []          # v38: the drawings' numbered sources (plans 01, 02, 04-07, section key); printed by draw_footer


def bcite(src):
    """v38: the number of a source in the drawings' key (the Sources drawing), as "[n]"."""
    if src not in BOARD_KEY:
        BOARD_KEY.append(src)
    return u"[{}]".format(BOARD_KEY.index(src) + 1)


def vis_icon(B, kind, x, y, sz, L, ink, acc, order=31):
    """v38: a pictogram in the square (x, y - sz)-(x + sz, y), drawn on a 10 x 10 grid. Graphic only, no text."""
    u = sz / 10.0
    lw = 0.06 * sz

    def p(a, b):
        return (x + a * u, y - sz + b * u)

    def R(a0, b0, a1, b1):
        return [p(a0, b0), p(a1, b0), p(a1, b1), p(a0, b1)]

    def disc(a, b, r, col, n=14):
        B.fill([circle_pts(x + a * u, y - sz + b * u, r * u, n)], col, L, order)

    def ln(pts, col, w=1.0):
        B.line([p(a, b) for a, b in pts], col, L, order + 1, lw * w)

    def arc(a, b, r, a0, a1, col, w=1.0):
        n = 8
        ln([(a + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)), b + r * math.sin(math.radians(a0 + (a1 - a0) * k / n)))
            for k in range(n + 1)], col, w)

    def person(a, col):
        disc(a, 8.2, 1.1, col)
        B.fill([R(a - 1.1, 3.4, a + 1.1, 6.8)], col, L, order)
        B.fill([R(a - 1.1, 0.4, a - 0.25, 3.6), R(a + 0.25, 0.4, a + 1.1, 3.6)], col, L, order)
    if kind == "sound":
        B.fill([R(0.6, 3.6, 2.6, 6.4)], ink, L, order)
        B.fill([[p(2.6, 3.6), p(5.0, 1.4), p(5.0, 8.6), p(2.6, 6.4)]], ink, L, order)
        for r in (1.8, 3.2, 4.6):
            arc(5.0, 5.0, r, -40, 40, acc, 1.2)
    elif kind in ("heat", "air"):
        B.fill([R(4.0, 3.0, 6.0, 9.4)], (255, 255, 255), L, order)
        ln([(4.0, 3.0), (4.0, 9.4), (6.0, 9.4), (6.0, 3.0)], ink)
        disc(5.0, 2.2, 1.9, acc)
        B.fill([R(4.5, 2.2, 5.5, 7.0 if kind == "heat" else 5.4)], acc, L, order + 1)
        for b in (5.0, 6.6, 8.2):
            ln([(6.0, b), (7.2, b)], ink, 0.8)
    elif kind == "shade":
        B.fill([R(0.6, 0.6, 4.2, 7.6)], ink, L, order)
        B.fill([[p(4.2, 0.6), p(9.6, 0.6), p(9.6, 3.0), p(4.2, 7.6)]], acc, L, order)
        disc(8.2, 8.4, 1.3, ink)
    elif kind == "sun":
        disc(5.0, 5.0, 2.2, acc)
        for k in range(8):
            t = math.radians(45.0 * k)
            ln([(5.0 + 3.0 * math.cos(t), 5.0 + 3.0 * math.sin(t)), (5.0 + 4.4 * math.cos(t), 5.0 + 4.4 * math.sin(t))], ink)
    elif kind == "roof":
        B.fill([R(1.0, 0.6, 9.0, 5.4)], ink, L, order)
        B.fill([[p(0.4, 5.4), p(5.0, 7.6), p(9.6, 5.4)]], acc, L, order)
        disc(8.4, 9.0, 0.9, acc)
    elif kind == "ground":
        B.fill([R(0.4, 0.6, 9.6, 2.6)], ink, L, order)
        disc(5.0, 6.6, 1.6, acc)
        for k in (-1, 0, 1):
            ln([(5.0 + 2.2 * k, 3.4), (5.0 + 2.2 * k, 4.4)], acc)
    elif kind == "wind":
        for b, a1 in ((7.4, 7.6), (5.0, 9.4), (2.6, 6.4)):
            ln([(0.6, b), (a1, b)], ink, 1.2)
            arc(a1, b + 0.9, 0.9, -90, 120, acc, 1.2)
    elif kind == "calm":
        arc(5.0, 5.0, 4.0, 0, 360, ink)
        disc(5.0, 5.0, 1.0, acc)
    elif kind == "drop":
        B.fill([[p(5.0, 9.4), p(2.4, 4.6), p(7.6, 4.6)]], acc, L, order)
        disc(5.0, 3.8, 2.7, acc)
    elif kind in ("felt", "comfort"):
        person(3.6, ink)
        if kind == "felt":
            disc(8.0, 8.0, 1.3, acc)
        else:
            ln([(6.0, 4.8), (7.2, 3.4), (9.6, 7.4)], acc, 1.6)
    elif kind == "clock":
        arc(5.0, 5.0, 4.2, 0, 360, ink)
        ln([(5.0, 5.0), (5.0, 8.2)], ink, 1.2)
        ln([(5.0, 5.0), (7.4, 5.0)], acc, 1.2)
    elif kind == "gauge":
        arc(5.0, 3.0, 4.4, 0, 180, ink, 1.2)
        ln([(5.0, 3.0), (7.6, 6.2)], acc, 1.4)
        disc(5.0, 3.0, 0.7, ink)
    elif kind == "limit":
        for k, h_ in enumerate((3.0, 6.4, 8.6, 4.8)):
            B.fill([R(0.8 + 2.3 * k, 0.6, 2.5 + 2.3 * k, h_)], ink, L, order)
        for a in (0.2, 2.8, 5.4, 8.0):
            ln([(a, 5.6), (a + 1.6, 5.6)], acc, 1.4)
    elif kind == "build":
        B.fill([R(0.6, 0.6, 4.4, 6.0), R(5.4, 0.6, 9.4, 8.8)], ink, L, order)
        for b in (2.2, 4.4, 6.6):
            B.fill([R(6.4, b, 8.4, b + 1.0)], acc, L, order + 1)
    elif kind == "floors":
        for k in range(4):
            B.fill([R(2.4, 0.6 + 2.2 * k, 7.6, 2.4 + 2.2 * k)], ink if k else acc, L, order)
    elif kind == "green":
        B.fill([R(4.4, 0.6, 5.6, 4.0)], ink, L, order)
        disc(5.0, 6.0, 3.4, acc)
    elif kind == "field":
        B.fill([[p(0.4, 0.6), p(9.6, 0.6), p(7.6, 6.0), p(2.4, 6.0)]], acc, L, order)
        for a in (2.6, 5.0, 7.4):
            ln([(a - (a - 5.0) * 0.6, 0.6), (5.0 + (a - 5.0) * 0.55, 6.0)], ink, 0.8)
        disc(7.8, 8.4, 1.0, ink)
    elif kind == "water":
        for b in (2.4, 5.0, 7.6):
            ln([(0.4 + 1.15 * k, b + (0.7 if k % 2 else -0.7)) for k in range(9)], acc, 1.3)
    elif kind == "road":
        B.fill([[p(1.0, 0.4), p(9.0, 0.4), p(6.4, 9.6), p(3.6, 9.6)]], ink, L, order)
        for b in (1.4, 4.4, 7.4):
            B.fill([R(4.7, b, 5.3, b + 1.6)], (255, 255, 255), L, order + 1)
    elif kind == "walk":
        person(3.4, ink)
        ln([(6.0, 1.0), (7.4, 1.0)], acc, 1.4)
        ln([(8.2, 1.0), (9.6, 1.0)], acc, 1.4)
    elif kind == "shop":
        B.fill([R(1.0, 0.6, 9.0, 6.0)], ink, L, order)
        for k in range(4):
            B.fill([[p(0.6 + 2.2 * k, 6.0), p(2.8 + 2.2 * k, 6.0), p(1.7 + 2.2 * k, 8.6)]], acc, L, order)
        B.fill([R(4.0, 0.6, 6.0, 3.8)], (255, 255, 255), L, order + 1)
    elif kind == "climb":
        B.fill([[p(0.4, 0.6), p(9.6, 0.6), p(9.6, 7.4)]], ink, L, order)
        ln([(2.6, 4.0), (6.6, 7.0)], acc, 1.4)
        ln([(5.6, 7.4), (6.6, 7.0), (6.2, 6.0)], acc, 1.4)
    else:                                                 # "dot": a plain marker
        disc(5.0, 5.0, 2.4, acc)


def vis_tiles(B, x, y, w, items, U, L, cols=None, h=1.0, ink=None, grey=None, fill=None, rule=None, gap=0.3):
    """v38 (visual first): readings as pictogram tiles, the water board v1.6 tiles on this board's API. items =
    [(icon, keyword heading, ONE figure, ref "[n]" or "")], None items left out; `cols` tiles a row (all in one row by
    default). Returns the y below the last row."""
    ink, grey = ink or T_INK, grey or T_GREY
    fill = fill or (246, 246, 247)
    rule = rule or (214, 214, 220)
    items = [it for it in items if it]
    if not items:
        return y
    n = len(items)
    cols = max(1, min(n, cols or n))
    g = gap * U
    tw_ = (w - (cols - 1) * g) / float(cols)
    th, ic, pad = 1.9 * h * U, 1.25 * h * U, 0.3 * h * U
    for k, (kind, head, big, ref) in enumerate(items):
        r_, c_ = divmod(k, cols)
        tx, ty = x + c_ * (tw_ + g), y - r_ * (th + g)
        B.fill([rect(tx, ty - th, tx + tw_, ty)], fill, L, 28)
        B.line(rect(tx, ty - th, tx + tw_, ty) + [(tx, ty - th)], rule, L, 29, 0.03)
        vis_icon(B, kind, tx + pad, ty - pad, ic, L, ink, mix(ink, (200, 70, 30), 0.65))
        lx = tx + 2.0 * pad + ic
        lw = tx + tw_ - pad - lx
        B.fit(head, lx, ty - pad - 0.3 * h * U, 0.3 * h * U, lw, grey, L, font=FONT_TITLE, bold=True)
        rw = (tw(ref, 0.26 * h * U) + 0.2 * U) if ref else 0.0
        B.fit(big, lx, ty - th + pad + 0.05 * U, 0.72 * h * U, max(0.5 * U, lw - rw), ink, L, font=FONT_TITLE, bold=True)
        if ref:
            B.text(ref, tx + tw_ - pad, ty - th + pad + 0.05 * U, 0.26 * h * U, grey, L, align="R")
    nr = (n + cols - 1) // cols
    return y - nr * th - (nr - 1) * g


