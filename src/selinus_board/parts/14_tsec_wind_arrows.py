def tsec_wind_arrows(B, G, x, ytop, ss, U, L, fld, cols, u_in, scale):
    """Arrows of the wind's component in the plane (length by speed) on a coarse grid of the open air."""
    zhi, Lm = G["zhi"], G["L"]
    if abs(u_in) < 0.12:
        return
    nx_ = max(4, int(Lm * ss / (3.2 * U)))
    for q in range(nx_):
        s_ = Lm * (q + 0.5) / nx_
        i = min(range(len(cols)), key=lambda j: abs(cols[j][0] - s_))
        c = cols[i]
        base = c[4] if c[5] is None else c[5]
        for hz in (2.0, 9.0, 18.0, 30.0):
            z = base + hz
            if z > zhi - 2.0:
                break
            v = tsec_at(fld, i, z)
            if v is None:
                continue
            ln = min(2.6 * U, max(0.35 * U, v * abs(u_in) * scale))
            dx = ln if u_in > 0 else -ln
            px, py = x + c[0] * ss - dx / 2.0, ytop - (zhi - z) * ss
            col = (40, 52, 78)
            B.line([(px, py), (px + dx, py)], col, L, 30, 0.07)
            hx_ = 0.2 * U * (1 if dx > 0 else -1)
            B.fill([[(px + dx, py), (px + dx - hx_, py + 0.1 * U), (px + dx - hx_ * 0.75, py), (px + dx - hx_, py - 0.1 * U)]],
                   col, L, 30)


def tsec_sheet_wind(S, B, X, Y, U, rects, d, G, lab, num, ctx):
    L = "LU_TECH::Sections"
    wmax = ctx["wmax"]
    cols = tsec_cols(S, G, TSEC_DS)
    E = S.env["E"]
    CP = Compass(E["location"]["lon"], E["location"]["lat"])
    CF = S.env["comfort"]
    cf = tsec_comfort(S, G)
    lay = tsec_layout(S, G, U, 4)
    res = tsec_px_res(G, lay["ss"])
    rows = []
    for sd in SEASONS:
        key = sd["key"]
        c = cf["seasons"][key]
        fld = dict(zlo=cf["zlo"], dz=cf["dz"], nz=cf["nz"], s=cf["s"], vals=c["wind"])
        sc = stretch_scale(WINDY_WIND, 0.0, WIND_SCALE_HI, c["wind"], to=WIND_STRETCH_TO, ab=analysis_window(S, "wind"))
        lut = sc[0]
        png = tsec_compose(os.path.join(d, tsec_name(num, "wind_" + key)), S, G, res, key, fld=fld, colour=lut,
                           rkey=fp(G["key"], S.env["keys"]["comfort"], key, "wind", TSEC_DS, TSEC_DZ, wmax))
        dir_from, share = prevailing(CF["seasons"][key])
        wv = CP.vec((dir_from + 180.0) % 360.0)            # where the prevailing wind blows to
        u_in = wv[0] * G["ux"] + wv[1] * G["uy"]
        u_x = wv[0] * (-G["uy"]) + wv[1] * G["ux"]         # + = away from the viewer (into the page)
        ang = math.degrees(math.acos(min(1.0, abs(u_in))))
        how = []
        if abs(u_in) >= 0.12:
            how.append("towards {}{}".format(lab, "'" if u_in > 0 else ""))
        if abs(u_x) >= 0.12:
            how.append("into the page" if u_x > 0 else "out of the page")
        w15 = [v for s_, v in tsec_at_height(fld, cols, 1.5) if v is not None]
        w10 = [v for s_, v in tsec_at_height(fld, cols, 10.0) if v is not None]
        open15 = (c["u10_mean"] or 0.0) * PED_WIND
        shel = 100.0 * sum(1 for v in w15 if v < 0.5 * open15) / max(1, len(w15))
        txt = [("wind", "1.5 m ABOVE THE GROUND", "{} m/s".format(tsec_rng(w15, "{:.2f}")), "[6]"),     # v38: tiles
               ("build", "SHELTERED < HALF OPEN", "{:.0f} %".format(shel), "[6]"),
               ("wind", "OPEN GROUND · 1.5 m", "{:.2f} m/s".format(open15), "[6]"),
               ("wind", "10 m UP", "{} m/s".format(tsec_rng(w10, "{:.2f}")), "[6]")]

        def legend(x, y, w, sc=sc, vv=c["wind"]):
            return stretch_bar(B, x, y, w, WINDY_WIND, 0.0, WIND_SCALE_HI, sc, U, L,
                               "kt · mean · Windy colours 0-{:.0f} m/s, as T5".format(
                                   WIND_SCALE_HI), k=KT, th=0.22, vals=vv)

        def over(x, ytop, ss, fld=fld, u_in=u_in):
            tsec_wind_arrows(B, G, x, ytop, ss, U, L, fld, cols, u_in, 0.45 * U)
        step = 0.5 if wmax <= 4.0 else 1.0
        rows.append(dict(head="{} · MEAN OF {:,} HOURS · MOSTLY FROM {} · {:.2f} m/s AT 10 m".format(
            sd["name"], c["hours"], TSEC_NAMES16[int(round(dir_from / 22.5)) % 16], c["u10_mean"] or 0.0),
            sub="wind {:.0f}° to the line · {} · {:.0f} % of hours [6]".format(ang, " and ".join(how) or "along the line",
                                                                             100.0 * share),
            png=png, legend=legend, note=txt, over=over,
            contours=sa_contours(fld, stretch_levels(sc, [step * k for k in range(1, int(wmax / step) + 1)])),
            cfmt="{:.2f} m/s",
            graph=tsec_profile_graph(B, G, U, L, tsec_at_height_all(fld, cols, 1.5, G["cut"]), sc[1], sc[2], "", lut,
                                     "m/s at 1.5 m above the ground")))
    tsec_sheet(S, B, X, Y, U, rects, num, "WIND · SECTION " + lab,
               "Wind m/s · every height · season mean · Windy [6]",
               comfort_sources(S) + [
                   "Every hour's 10 m wind brought to each height above the ground with the log law (z0 "
                   "0.1 m) and reduced behind every building and crown upwind within 300 m by the windbreak wake curves of the "
                   "plan (Heisler & DeWalle 1988), each obstacle counted with its height above that point's level (height above "
                   "ground - 1.5 m), at its exact distance along that hour's wind (10-degree sectors); then averaged. At 1.5 m "
                   "this is the plan's wind (T5). An estimate of shelter, not CFD. Colour = speed, after Windy; the prevailing "
                   "wind's angle to the line and its share of the hours; arrows: its part in the plane."], G, lab, rows, lay)


def tsec_sheet_air(S, B, X, Y, U, rects, d, G, lab, num, ctx):
    L = "LU_TECH::Sections"
    lo, hi = ctx["tlo"], ctx["thi"]
    cf = tsec_comfort(S, G)
    cols = tsec_cols(S, G, TSEC_DS)
    lay = tsec_layout(S, G, U, 4)
    res = tsec_px_res(G, lay["ss"])
    rows = []
    for sd in SEASONS:
        key = sd["key"]
        c = cf["seasons"][key]
        fld = dict(zlo=cf["zlo"], dz=cf["dz"], nz=cf["nz"], s=cf["s"], vals=c["ta"])
        sc = stretch_scale(WINDY_TEMP, lo, hi, c["ta"], ab=analysis_window(S, "ta"))
        lut = sc[0]
        png = tsec_compose(os.path.join(d, tsec_name(num, "air_temperature_" + key)), S, G, res, key, fld=fld, colour=lut,
                           rkey=fp(G["key"], S.env["keys"]["comfort"], key, "ta", TSEC_DS, TSEC_DZ, lo, hi))
        vals = [(v, fld["zlo"] + (kz + 0.5) * fld["dz"]) for col in fld["vals"] for kz, v in enumerate(col) if v is not None]
        vmin, vmax = min(vals), max(vals)
        txt = [("air", "HIGHEST POINT · +{:.0f} m".format(vmin[1]), "{:.2f} °C".format(vmin[0]), "[6]"),     # v38: tiles
               ("air", "LOWEST POINT · +{:.0f} m".format(vmax[1]), "{:.2f} °C".format(vmax[0]), "[6]")]

        def legend(x, y, w, sc=sc, vv=c["ta"]):
            return stretch_bar(B, x, y, w, WINDY_TEMP, lo, hi, sc, U, L, "°C · the scale of T6 and T7", th=0.22, vals=vv)
        lv = [round(v * 4.0) / 4.0 for v in np.arange(math.floor(vmin[0] * 4) / 4.0, vmax[0] + 0.25, 0.25)]
        lv = stretch_levels(sc, [v for v in lv if vmin[0] < v < vmax[0]][::2])
        rows.append(dict(head="{} · MEAN OF {:,} HOURS · AIR {:.2f} °C · RH {:.0f} %".format(
            sd["name"], c["hours"], c["ta_mean"] or 0.0, c["rh_mean"] or 0.0),
            sub="dry bulb 2 m · PVGIS point elevation {:.0f} m [6]".format(CLIMATE["elevation"]),
            png=png, legend=legend, note=txt, contours=sa_contours(fld, lv),
            cfmt="{:.2f} °C",
            graph=tsec_profile_graph(B, G, U, L, tsec_at_height_all(fld, cols, 2.0, G["cut"]), sc[1], sc[2], "°", lut,
                                     "°C at 2 m above the ground")))
    tsec_sheet(S, B, X, Y, U, rects, num, "AIR TEMPERATURE · SECTION " + lab,
               "Dry bulb °C · every height · season mean · Windy [6]",
               comfort_sources(S) + [
                   "Dry bulb from the PVGIS climate data (ERA5-Land 2 m air temperature of its grid cell, "
                   "whose ground height is not reported; taken at PVGIS's point elevation, {:.0f} m, an assumption), carried to every "
                   "height of the plane with the standard lapse rate (-0.65 K per 100 m), as on the plan (T6); colours after "
                   "Windy's temperature scale. The air is the same along the line, only height changes it.".format(
                       CLIMATE["elevation"]),
                   "Street-scale differences (shade, water, traffic, night inversions) are not modelled."],
               G, lab, rows, lay)


def tsec_sheet_felt(S, B, X, Y, U, rects, d, G, lab, num, ctx):
    L = "LU_TECH::Sections"
    lo, hi = ctx["tlo"], ctx["thi"]
    cols = tsec_cols(S, G, TSEC_DS)
    cf = tsec_comfort(S, G)
    lay = tsec_layout(S, G, U, 4)
    res = tsec_px_res(G, lay["ss"])
    rows = []
    for sd in SEASONS:
        key = sd["key"]
        c = cf["seasons"][key]
        fld = dict(zlo=cf["zlo"], dz=cf["dz"], nz=cf["nz"], s=cf["s"], vals=c["utci"])
        fsun = dict(fld, vals=c["sun"])
        sc = stretch_scale(WINDY_TEMP, lo, hi, c["utci"], ab=analysis_window(S, "utci"))
        lut = sc[0]
        png = tsec_compose(os.path.join(d, tsec_name(num, "felt_temperature_" + key)), S, G, res, key, fld=fld, colour=lut,
                           rkey=fp(G["key"], S.env["keys"]["comfort"], key, "utci", TSEC_DS, TSEC_DZ, lo, hi))
        u15pts = tsec_at_height(fld, cols, 1.5)
        u15 = [v for s_, v in u15pts if v is not None]
        f15 = [v for s_, v in tsec_at_height(fsun, cols, 1.5) if v is not None]
        fa = tsec_facades(fld, cols)
        txt = [("felt", "1.5 m ABOVE THE GROUND", "{} °C".format(tsec_rng(u15)), "[6]"),           # v38: tiles
               ("felt", "1.5 m · MEAN", "{:.2f} °C".format(sum(u15) / max(1, len(u15))), "[6]"),
               ("sun", "IN DIRECT SUN · SUNNY h", "{:.0f} %".format(100.0 * sum(f15) / max(1, len(f15))), "[6]")]
        if fa:
            txt.append(("build", "IN FRONT OF CUT FACADES", "{} °C".format(tsec_rng(fa)), "[6]"))

        def legend(x, y, w, sc=sc, vv=c["utci"]):
            yy = stretch_bar(B, x, y, w, WINDY_TEMP, lo, hi, sc, U, L, "UTCI °C, mean over the hours · the scale of T6 and T7", vals=vv,
                             th=0.22)
            return utci_band_marks(B, x, yy + 0.1 * U, w, sc[1], sc[2], U, L)
        thr = [t for t, nm_ in UTCI_STRESS if lo < t < hi]
        rows.append(dict(head="{} · MEAN OF {:,} HOURS · AIR {:.2f} °C".format(sd["name"], c["hours"], c["ta_mean"] or 0.0),
                         sub="air + humidity + wind + sun / shade + sky [6]",
                         png=png, legend=legend, note=txt, contours=sa_contours(fld, thr), cfmt="UTCI {:.2f} °C",
                         graph=tsec_profile_graph(B, G, U, L, tsec_at_height_all(fld, cols, 1.5, G["cut"]), sc[1], sc[2], "°", lut,
                                                  "UTCI °C at 1.5 m above the ground")))
    tsec_sheet(S, B, X, Y, U, rects, num, "FELT TEMPERATURE · SECTION " + lab,
               "UTCI °C · felt · every point of the plane · season mean [6]",
               comfort_sources(S) + ["What a person feels at each point: air, humidity, local wind, sun or shade and the sky "
               "it sees. UTCI (Broede et al. 2012) every hour at every point of the plane, then averaged: air "
               "with the lapse rate, that hour's wind as on the wind section (brought to the 10 m reference UTCI expects), "
               "mean radiant temperature from SolarCal (ASHRAE 55, outdoor form as in Ladybug) with that point's sun or "
               "shade in that hour (exact 3D obstruction) and its sky view (72 sectors through buildings, crowns and "
               "terrain), albedo 0.25 and the sky's long-wave radiation; as on the plan (T7). Contours: the UTCI stress "
               "category limits."], G, lab, rows, lay)


TSEC_SHEETS = {"sound_sections": tsec_sheet_sound, "heat_sections": tsec_sheet_heat, "shade_sections": tsec_sheet_shade,
               "solar_sections": tsec_sheet_solar, "wind_sections": tsec_sheet_wind, "air_sections": tsec_sheet_air,
               "felt_sections": tsec_sheet_felt}


def build_tech_sections(S, B, X, Y, U, rects, d):
    """Sheets of the technical sections, each under the plan sheet of its analysis (one row per line)."""
    lines = tsec_lines(S)
    if not any(lines.values()):
        return 0
    import time as _t
    t0 = _t.time()
    ctx = {}
    if S.env.get("comfort") and any(lines.get(k) for k in ("wind_sections", "air_sections", "felt_sections")):
        ctx["wmax"], ctx["tlo"], ctx["thi"] = tsec_comfort_scales(S, lines)
    step = (PW + 6.0) * U
    vstep = (PH + 6.0) * U
    made = 0
    for ci, (key, num, title) in enumerate(TSEC_DEF):
        if key in ("wind_sections", "air_sections", "felt_sections") and not S.env.get("comfort"):
            if lines.get(key):
                LOG.append("WARNING: {} need the wind and temperature analysis, which did not run.".format(key))
            continue
        for j, (k, a, b) in enumerate(lines.get(key, [])):
            G = tsec_geom(S, a, b)
            TSEC_SHEETS[key](S, B, X + ci * step, Y - (j + 1) * vstep, U, rects, d, G, str(k + 1), "%s.%d" % (num, k + 1), ctx)
            made += 1
    LOG.append("Technical sections: {} sheets (below the plan sheet of each analysis).".format(made))
    return made


def build_technical(S, B, X, Y, U, rects):
    if not getattr(S, "env", None):
        if HAVE_NP:
            LOG.append("WARNING: technical sheets need the environment data (env_path).")
        return
    d = tech_dir()
    S.env["tech_dir"] = d
    step = (PW + 6.0) * U
    try:
        tsec_noise_start(S)                              # v17: the sound sections run while the sheets are made
    except Exception as ex:
        S.env["tsec_noise_pre"] = {}
        LOG.append("Sound sections: not started early ({}); computed in turn.".format(ex))
    try:
        tsec_prefetch(S, U)                              # v18: the section drawings on the workers meanwhile
    except Exception as ex:
        S.env["sa_pre"] = {}
        LOG.append("Section drawings: not started early ({}); made in turn.".format(ex))
    sheet_sound(S, B, X, Y, U, rects, d)
    sheet_heat(S, B, X + step, Y, U, rects, d)
    sheet_shade(S, B, X + 2 * step, Y, U, rects, d)
    sheet_radiation(S, B, X + 3 * step, Y, U, rects, d)
    if S.env.get("comfort"):
        sheet_wind(S, B, X + 4 * step, Y, U, rects, d)
        sheet_air(S, B, X + 5 * step, Y, U, rects, d)
        sheet_felt(S, B, X + 6 * step, Y, U, rects, d)
        if S.env["comfort"].get("year"):
            sheet_comfort_year(S, B, X + 7 * step, Y, U, rects, d)
    try:
        S.env["n_tsec"] = build_tech_sections(S, B, X, Y, U, rects, d)
    finally:
        S.env["sa_pre"] = {}                                          # v18: none kept for a later run
        for pre in (S.env.get("tsec_noise_pre") or {}).values():      # v17: no worker left running
            if "h" in pre["job"] and "out" not in pre["job"]:
                _noise_par_stop(pre["job"]["h"])
                pre["job"]["out"] = None
    LOG.append("Technical maps written to " + d)


def tech_report(S):
    out = ["Frame {:.0f} x {:.0f} m{} - technical analyses only".format(
        S.F.w, S.F.h, "" if getattr(S, "frame_src", "survey") == "input" else " (the " + S.frame_src + ")"
        if getattr(S, "frame_src", "").startswith("analysis range") else " (the whole survey in the file)")]
    if getattr(S, "env", None):
        out.append("{} tree crowns; shade: the four key days and the mean day of the year, every minute; solar radiation: "
                   "mean kWh/m2 per day of each season from every hour of the typical year".format(len(S.env["solids"][2])))
        cf = S.env.get("comfort")
        if cf:
            out.append("Wind, air and felt temperature: means over {} of each season (input hours)".format(cf["label"]))
        if S.env.get("n_tsec"):
            out.append("Technical sections: {} sheets".format(S.env["n_tsec"]))
        out.append("Maps: " + S.env.get("tech_dir", ""))
    out.append(height_note(S))
    out.append(traffic_note(S))
    out.append(street_note(S) + " " + channel_note(S) + ".")
    return "\n".join(out)


# ============================================================ SECTION STRIPS (after the attached references)
SEC_POCHE = mix(KHAKI, PAPER, 0.62)
SEC_WALL = mix(INK, BG, 0.12)
SEC_CROWN = mix(TREE_COLS["tree"], PAPER, 0.15)       # a crown as measured on the canopy height map
SEC_PAVE = mix(C("BC6F45"), BG, 0.12)
SEC_ROAD_D = 0.6          # v16.5: depth of the street surface band under the ground line (m; v16.4: 0.4), drawing only
SEC_ROAD_HATCH = 0.07     # v16.5: its hatch, page units (U) between the lines
SURFACE = {"transport": mix(INK2, BG, 0.3), "void": mix(KHAKI, INK, 0.14), "green": CAT["green"][1],
           "agri": CAT["agri"][1], "vacant": CAT["vacant"][1]}


def fade(col, t):
    return mix(col, BG, max(0.0, min(1.0, t)))


# ------------------------------------------------------------ buildings in section
# A cut building is its measured volume: footprint cut by the line, from the ground to its height, tinted by use (or
# by fabric type for monuments and mosques), with a thin line at every storey of its floor count. Nothing the survey
# does not record (roof forms, openings, balconies) is drawn.
SEC_CHANNEL = mix(CAT["water"][1], PAPER, 0.5)        # v16.4: the stream channel's ground colour in section ...
SEC_CHANNEL_HATCH = C("3E7DAE")                      # ... and its blue hatch


def channel_polys(ground, a, b, pad=4.0, top=None, bank=None, lim=None):
    """v16.4: the stream channel in section: the area between the cut ground (the bed, carved from the surveyed bed
    levels) and the top of the lower bank, around the water span a..b (m along the line). The bank tops are the
    ground just outside the span; where the ground rises above that level the channel ends. Returns [[(s, z)...]].
    v50 (MIRAQUA 28 Oct, bank depth REPORT §4 1a): bank = the bank top given (the lower crest, or the DSİ walls'
    top) in place of the ground just outside, lim = (s0, s1) the stretch of the cut it is taken within (the crests)."""
    gs = [p[0] for p in ground]

    def g_at(s):
        k = max(0, min(len(ground) - 1, _bisect_right(gs, s) - 1))
        k1 = min(len(ground) - 1, k + 1)
        (sa_, za), (sb_, zb) = ground[k], ground[k1]
        return za if sb_ <= sa_ else za + (zb - za) * (s - sa_) / (sb_ - sa_)
    zt = min(g_at(max(gs[0], a - 1.0)), g_at(min(gs[-1], b + 1.0))) if bank is None else bank
    if top is not None:                                   # v16.5: up to the water surface instead
        zt = min(zt, top)
    lo, hi = (a - pad, b + pad) if lim is None else lim
    pts = [(s, z) for s, z in ground if lo <= s <= hi]
    out = []
    run = None
    for k, (s1, z1) in enumerate(pts):
        if z1 < zt:
            if run is None:                               # entering the channel: where the ground drops below zt
                if k == 0:
                    run = [(s1, zt)]
                else:
                    s0, z0 = pts[k - 1]
                    run = [(s0 + (s1 - s0) * (zt - z0) / (z1 - z0), zt)]
            run.append((s1, z1))
        elif run is not None:                             # leaving it
            s0, z0 = pts[k - 1]
            run.append((s0 + (s1 - s0) * (zt - z0) / (z1 - z0), zt))
            out.append(run)
            run = None
    if run is not None:
        run.append((run[-1][0], zt))
        out.append(run)
    return [p for p in out if len(p) >= 3 and p[0][0] < b and p[-1][0] > a]


def draw_channel(B, L, P, polys, U, fill, hatch, order, lw=0.035, spacing=0.16):
    """v16.4: the stream channel filled pale blue and hatched in blue (45°), in page coordinates through P; hatch None:
    the fill alone."""
    for poly in polys:
        Q = [P(s, z) for s, z in poly]
        B.fill([Q], fill, L, order)
        if hatch is not None:
            for seg in hatch_segments([Q], spacing * U, math.radians(45.0)):
                B.line(seg, hatch, L, order + 1, lw)


def draw_stream(B, L, P, ground, a, b, bed, lvl, U, wash, fill, hatch, line_c, order, lw=0.035, bank=None, lim=None):
    """v16.5: the stream in section: the channel from the bed to the lower bank top in a pale wash, the water from the
    bed to its surface (lvl) filled and hatched in blue, the water line on top. Without water (lvl at the bed) the
    channel itself is hatched, as in v16.4, and the bed drawn as a blue line. v50: bank, lim as channel_polys."""
    if lvl - bed > 0.005:
        draw_channel(B, L, P, channel_polys(ground, a, b, bank=bank, lim=lim), U, wash, None, order)
        wp = channel_polys(ground, a, b, top=lvl, bank=bank, lim=lim)
        draw_channel(B, L, P, wp, U, fill, hatch, order + 1, lw=lw, spacing=0.08)
        for poly in wp:                               # the water line, over the ground line, so a thin layer still reads
            B.line([P(poly[0][0], lvl), P(poly[-1][0], lvl)], line_c, L, order + 6, 0.35)
    else:
        draw_channel(B, L, P, channel_polys(ground, a, b, bank=bank, lim=lim), U, fill, hatch, order, lw=lw)
        B.line([P(a, bed), P(b, bed)], line_c, L, order + 5, 0.4)


def draw_crown(B, L, P, s, zg, hw, lo, hi, col, order):
    """A tree in section at its measured size: trunk to the crown base, crown from lo to hi, hw wide each side."""
    x0, y0 = P(s, zg)
    xb, yb = P(s, zg + lo)
    B.line([(x0, y0), (xb, yb)], fade(INK2, 0.25), L, order, 0.05)
    cx, cy = P(s, zg + (lo + hi) / 2.0)
    rx = abs(P(s + hw, 0)[0] - P(s, 0)[0])
    ry = abs(P(0, (hi - lo) / 2.0)[1] - P(0, 0)[1])
    if rx > 0 and ry > 0:
        B.fill([ellipse_pts(cx, cy, rx, ry, 20)], col, L, order + 1)


# ============================================================ BOARD SECTIONS v16.2: the lively drawing behind the cut
SEC_SOIL = mix(KHAKI, PAPER, 0.42)                   # the cut ground, a shade darker than the page
SA_STYLE_BOARD = dict(bg=BG, ground=mix(SEC_POCHE, BG, 0.25), ground_edge=mix(INK2, BG, 0.55), bld=FAINT,
                      bld_edge=mix(INK2, BG, 0.3), storey=mix(INK2, BG, 0.62), fade_to=BG, tree_alpha=0.88,
                      tree_wash=0.0, tree_fade0=0.04, people=mix(INK2, BG, 0.1), bridge=mix(INK2, BG, 0.35))


def sa_board_bld(bo):
    """A building beyond the cut in the tone of its type (v16.4; v16.3 tinted it by use, so the old town and the
    planned low-rise houses, both homes, looked alike)."""
    return mix(typo_tone(bo.get("fabric", "regular"), bo.get("cat", "residential")), BG, 0.32 + (0.1 if bo.get("annex") else 0.0))


def sa_env_key(S):
    E_fp = ((getattr(S, "env", None) or {}).get("E_fp"))
    if E_fp:
        return E_fp
    try:
        st = os.stat(ENV_PATH)
        return fp(os.path.basename(ENV_PATH), st.st_size, int(st.st_mtime))
    except Exception:
        return None


def sec_px_res(Lm, ss):
    """Metres per pixel for a board section drawn at ss (model units per metre): TSEC_DPI at the printed size."""
    mm_per_m = ss * MMU
    res = 25.4 / (TSEC_DPI * max(1e-6, mm_per_m))
    return round(max(0.06, min(0.6, max(res, Lm / 6000.0))), 4)


def sa_index(S, d):
    """Which section picture was drawn from what (its own index file: the board may run without the technical sheets)."""
    memo = getattr(S, "_sa_index", None)
    if memo is None:
        memo = S._sa_index = {}
    idx = memo.get(d)
    if idx is None:
        try:
            with open(os.path.join(d, ".selinus_section_art_index.json"), "r", encoding="utf-8") as f:
                idx = json.load(f)
        except Exception:
            idx = {}
        memo[d] = idx
    return idx


def sa_index_save(S, d):
    try:
        with open(os.path.join(d, ".selinus_section_art_index.json"), "w", encoding="utf-8") as f:
            json.dump(sa_index(S, d), f)
    except Exception:
        pass


def sec_art_png(S, sd_, ss, tag):
    """The picture behind a board section (or one part of it): ground, buildings and trees beyond the cut, the trees cut
    by it and scale figures, on the page's colour (white for a separate drawing). Kept when nothing it is made from
    changed. Returns (path, zlo, zhi) or None."""
    if not HAVE_NP:
        return None
    x0, y0, x1, y1, nm = sd_["line"]
    a, b = (x0, y0), (x1, y1)
    base = sd_["base"]
    Lm = sd_["L"]
    off = sd_.get("s_off", 0.0)
    k, n = sd_.get("part", (1, 1))
    zlo, zhi = base - 3.0, base + sd_["zmax"] + 1.0
    res = sec_px_res(Lm, ss)
    style = dict(SA_STYLE_BOARD)
    if tag != "page":
        style.update(bg=(255, 255, 255), fade_to=(255, 255, 255))
    d = tech_dir()
    path = os.path.join(d, "section_%s%s_%s.png" % (nm, "" if n == 1 else "_%dof%d" % (k, n), tag))
    pr = site_prints(S)
    full = fp("sec_art", SA_VERSION, a, b, off, Lm, res, round(zlo, 3), round(zhi, 3), pr["bld"], pr["terrain"],
              pr["frame"], sa_env_key(S), style["bg"])
    e_ = sa_index(S, d).get(os.path.basename(path))
    try:
        if e_ and e_.get("key") == full and os.path.getsize(path) == e_.get("size"):
            return (path, zlo, zhi)
    except Exception:
        pass
    sc = sa_scene(S, a, b)
    ground = [(s_ + off, z + base) for s_, z in sd_["ground"]]
    art, r_ = sa_render(S, sc, off, off + Lm, zlo, zhi, res, style, leaf=1.0, season="", ground=ground,
                        bld_col=sa_board_bld)
    png_write_np(path, art.to_bytes())
    try:
        sa_index(S, d)[os.path.basename(path)] = dict(key=full, size=os.path.getsize(path), w=art.W, h=art.H)
        sa_index_save(S, d)
    except Exception:
        pass
    return (path, zlo, zhi)


SEC_CALL_H = 0.6        # v40: the callouts' text height (page units): >= 7.5 pt when the booklet crops a section


def sec_callouts(B, L, P, calls, ytop, U, lh=None, xlo=None, xhi=None):
    """v40: callouts [(s, z, text)] in rows under a section from ytop down: each word on the first row where it
    clears the others (kept between xlo and xhi, still over its leader), a leader from its point on the drawing to
    its top, broken where it passes a word of a row above. Returns the lowest baseline."""
    lh = (lh or SEC_CALL_H) * U
    step = lh + 0.4 * U
    calls = sorted(calls, key=lambda c: (c[0], c[2]))
    base_y = ytop - lh
    low = base_y
    placed = []                                          # (left, right, tier) of every callout
    for s, zf, txt in calls:
        fx = P(s, zf)[0]
        half = 0.5 * tw(txt, lh)
        cx = fx
        if xlo is not None:
            cx = max(cx, min(fx + half - 0.3 * U, xlo + half))
        if xhi is not None:
            cx = min(cx, max(fx - half + 0.3 * U, xhi - half))
        tier = 0                                         # the first row where the text is clear of the others
        gap = max(0.6 * U, 2.2 * lh)                     # v44: two characters' width between words on one row
        while any(t2 == tier and cx - half < r2 + gap and l2 - gap < cx + half for l2, r2, t2 in placed):
            tier += 1
        placed.append((cx - half, cx + half, tier))
    for (s, zf, txt), (l1, r1, tier) in zip(calls, placed):
        fx, fy = P(s, zf)
        ly = base_y - tier * step
        cuts = sorted((base_y - t2 * step - 0.12 * U, base_y - t2 * step + lh + 0.12 * U)
                      for l2, r2, t2 in placed if t2 < tier and l2 - 0.15 * U < fx < r2 + 0.15 * U)
        ytop_ = fy
        for c0, c1 in reversed(cuts):
            if c1 < ytop_:
                B.line([(fx, ytop_), (fx, c1)], INK2, L, 35, 0.035)
            ytop_ = min(ytop_, c0)
        if ly + lh + 0.12 * U < ytop_:
            B.line([(fx, ytop_), (fx, ly + lh + 0.12 * U)], INK2, L, 35, 0.035)
        B.fill([circle_pts(fx, fy, 0.09 * U, 8)], INK2, L, 35)
        B.text(txt, 0.5 * (l1 + r1), ly, lh, INK, L, align="C")
        low = min(low, ly)
    return low


def sec_cut(B, L, sd_, P, Lm, ss, U, dry=False):
    """v40 (was inside draw_section_strip): what the section cuts, drawn through P (s, z) -> page: the ground in a
    light poche with its surface materials and a fine ground line, the stream, the channel walls, the surveyed walls,
    the cut buildings by type with a line at every storey; without the picture behind, the measured crowns."""
    # ---- the ground: light poche, a surface of materials, a fine ground line
    prof = [P(a, b) for a, b in sd_["ground"]]
    B.fill([prof + [P(Lm, -3.0), P(0.0, -3.0)]], SEC_SOIL, L, 20)
    wat = [(a, b) for a, b, _, _ in sd_["water"]]
    for a, b, cat in sd_["strip"]:
        col = SURFACE.get(cat)
        if col is None:
            continue
        if cat in ("transport", "void") and any(a < wb + 8.0 and b > wa - 8.0 for wa, wb in wat):
            col = SEC_PAVE
        pts = [(s, z) for s, z in sd_["ground"] if a <= s <= b]
        if len(pts) >= 2:
            band_ = [P(s, z) for s, z in pts] + [P(s, z - SEC_ROAD_D) for s, z in reversed(pts)]
            if cat == "transport" and col is not SEC_PAVE and ROAD_SOLID:
                col = ROAD_FILL                           # v16.7: the street in the plans' solid street colour
            B.fill([band_], col, L, 21)
            if cat == "transport" and col is not SEC_PAVE and not ROAD_SOLID:   # v16.5 hatch, kept as an option
                B.hatch([band_], mix(INK, col, 0.45), L, 22, SEC_ROAD_HATCH * U, w=0.03)
    spans = sorted((a, b) for a, b, z0, z1, cat, annex, ftype, fl, floors, fsrc in sd_["bld"])
    run = []
    for s, z in sd_["ground"]:                           # the ground line, broken inside the cut buildings
        if any(a_ + 0.01 < s < b_ - 0.01 for a_, b_ in spans):
            if len(run) >= 2:
                B.line(run, INK, L, 26, 0.22)
            run = []
            continue
        run.append(P(s, z))
    if len(run) >= 2:
        B.line(run, INK, L, 26, 0.22)
    bks = sd_.get("banks") or []
    for kw_, (a, b, bed, lvl) in enumerate(sd_["water"]):
        # v16.5: the water hatched in blue at its depth (approximate unless measured), the channel above it in a pale
        # wash (v16.4: the whole channel hatched, up to the lower bank top); v50 (MIRAQUA 28 Oct, bank depth REPORT
        # §4 1a-1b): up to the lower bank crest, or the DSİ walls' top in the walled town reach
        zt_, lim_ = site28_channel_top(sd_, bks[kw_] if kw_ < len(bks) else None, a, b)
        draw_stream(B, L, P, sd_["ground"], a, b, bed, lvl, U, mix(CAT["water"][1], PAPER, 0.72), SEC_CHANNEL,
                    SEC_CHANNEL_HATCH, SEC_CHANNEL_HATCH, 22, bank=zt_, lim=lim_)
    for s, zb, zt in sd_.get("chwalls", []):
        r0, r1 = P(s - 0.3, zb), P(s + 0.3, zt)
        B.fill([rect(r0[0], r0[1], r1[0], r1[1])], SEC_WALL, L, 27)
    for s, zg in sd_["walls"]:                           # a surveyed wall: its place on the ground, no height
        bx, by = P(s, zg)
        B.fill([[(bx, by + 0.16 * U), (bx - 0.11 * U, by), (bx + 0.11 * U, by)]], SEC_WALL, L, 28)
    # ---- cut buildings: the volume to its height, a line at every storey
    tags_ = []
    th_ = site28_sec_sizes(sd_, U)[2] if sd_.get("_txt") else None   # v50 (F12): the tags at the cut's minor size
    for a, b, z0, z1, cat, annex, ftype, fl, floors, fsrc in sd_["bld"]:
        r0, r1 = P(a, z0), P(b, z1)
        if b - a < 1.2:
            B.fill([rect(r0[0], r0[1], r1[0], r1[1])], SEC_WALL, L, 28)
            continue
        heritage = ftype in ("monument", "sacred")
        # v16.4: the cut building in the tone of its TYPE (old town ochre, planned low-rise pale render, blocks cool
        # grey ...); its use stays in the ribbon under the section and in its tag
        room = mix(typo_tone(ftype, cat), PAPER, 0.12 + (0.15 if annex else 0.0))
        wall_c = mix(FABRIC[ftype][2], INK, 0.45) if heritage else INK
        # the generic silhouette of the building's type over its measured volume (eaves at its height)
        prof = bld_profile(ftype, cat, a, b, z0, z0, z1, floors, fsrc == "published", seed=int(a * 7.0), ruin=fl[2],
                           minaret=fl[3] if len(fl) > 3 else None)
        tag_ = typo_label(ftype, cat, floors, fl[0], fl[4] if len(fl) > 4 else "")
        if tag_.endswith(u" fl"):                         # revision 30 Oct (G6): its height in m, never floors
            tag_ = tag_.rsplit(u" · ", 1)[0] + u" · " + u_height(z1 - z0)
        if th_ is None:
            lab_ = tag_ if (not annex and (b - a) * ss > 0.6 * tw(tag_, 0.17 * U)) else None
            bld_draw_cut(B, L, P, prof, room, wall_c, ss, U, order=27, label=lab_, placed=tags_)
            continue
        bld_draw_cut(B, L, P, prof, room, wall_c, ss, U, order=27)
        lab_ = None if annex else site28_tag_fit(tag_, (b - a) * ss, th_)   # v50: the tag, else its height alone
        if lab_:
            site28_bld_tag(B, L, P, prof, lab_, th_, wall_c, U, tags_)
    if dry or not HAVE_NP:                               # no picture: the measured crowns as before
        for s_, zg_, hw_, lo_, hi_ in sd_["trees"]:
            draw_crown(B, L, P, s_, zg_, hw_, lo_, hi_, SEC_CROWN, 30)
    return tags_


def nice_ratio(r):
    """v41 (Aras 26 Oct 06:35 "they need to be round numbers"): the first round scale at or above r (1:500, 1:1,000,
    1:2,000, 1:2,500, 1:5,000 ...)."""
    if r <= 0:
        return r
    e = 10 ** math.floor(math.log10(r))
    for m in (1.0, 2.0, 2.5, 5.0, 10.0):
        if r <= m * e * 1.0001:
            return m * e
    return 10 * e


def round_ss(ss):
    """v41: page units per metre made smaller to the nearest round printed scale (at SHEET_MM), x and y alike."""
    return 1000.0 / (nice_ratio(1000.0 / max(1e-9, ss * MMU)) * MMU)


def draw_section_key(B, x, y, w, U):
    L = "LU_BOARD::Sections"
    B.text("SECTION KEY", x, y, 0.6 * U, INK, L, font=FONT_TITLE, bold=True)
    items = [("box", SEC_PAVE, "Paving at the water"), ("box", ROAD_FILL if ROAD_SOLID else SURFACE["transport"],
                                                    "Street surface, as on the plans"),
             ("box", SURFACE["void"], "Bare and yard ground"), ("box", SURFACE["green"], "Planted ground"),
             # v38: drawn samples with short names; what each one means is an entry of the Sources key [n]
             ("box", SEC_CHANNEL, "Water · hatched from the bed " + bcite(
                 "Section key: water, hatched blue from the bed up to its surface; the channel above it pale blue.")),
             ("box", SEC_WALL, "Channel walls · triangles: surveyed, no height"),
             ("box", mix(typo_tone("traditional", "residential"), PAPER, 0.12), "Cut buildings · surveyed floors " + bcite(
                 "Section key: cut buildings at their surveyed floors, in the tone of their type (see the building "
                 "types), the far wall's windows seen through the cut; a line at every storey; use in the ribbon below.")),
             ("box", mix(typo_tone("monument", "heritage"), PAPER, 0.12), "Monuments and mosques " + bcite(
                 "Section key: monuments (stone and brick bands, arches) and mosques (dome, minaret).")),
             ("box", SEC_CROWN, "Trees · whole, never cut " + bcite(
                 "Section key: trees on and beyond the line drawn whole, never cut: their modelled height and crown "
                 "(canopy map), by leaf type.")),
             ("box", sa_board_bld(dict(cat="residential", fabric="regular")), "Beyond the cut · paler with distance " +
              bcite("Section key: beyond the cut: buildings by type, ground and trees, paler with distance (to 120 m); "
                    "figures for scale.")),
             ("hdr", None, "UNDER EACH SECTION · SATELLITE, METRE BY METRE " +
              bcite("Land cover: Copernicus CLC+ Backbone 2021, 10 m.") +
              bcite("Greenness: Sentinel-2 L2A monthly median NDVI 2019-2025, January and July."))]
    names = seam_pack().get("clc_names") or {}
    items += [("box", CLC_COL[k], "Land cover: " + names.get(str(k), str(k)).lower()) for k in sorted(CLC_COL)
              if str(k) in names and k not in (8, 11)]
    lo = None
    for t_, c_ in NDVI_STEPS:
        items.append(("box", c_, "Greenness (NDVI) " + ("under {:.2f}".format(t_) if lo is None else "{:.2f}+".format(lo)
                                                        if t_ > 1 else "{:.2f} - {:.2f}".format(lo, t_))))
        lo = t_
    return draw_legend_items(B, items, x, y - 1.0 * U, w, U, L, h=0.36)


def draw_typology_key(S, B, x, y, w, U, ymin=None, ss=None, th=None, crop=True, enl=1.0):
    """v16.3 · the building types as the sections draw them: one small generic section of each type found in the frame
    (types under 0.5 % of the footprint are left out, as on the fabric map; mosques and monuments always shown when
    present), with its name. Returns the y below it, or y unchanged when it would not fit above ymin. v44: with ss
    (page units per metre, a round booklet scale) and th (tag height) given, drawn at that scale under the cuts, each
    type as wide as its tag needs; draw_typology_key.last_w = the width used. v45: drawn at the cuts' own scale, so
    it writes no scale of its own (the page states the one scale). v50 (MIRAQUA 28 Oct, P05.1): under each type its
    floors and height, "2 fl · 6.00 m" (floors x the storey height: FLOOR_H, STOREY), the words centred by their
    real width and the subtitle's keywords in bold; enl > 1: ss is the cuts' scale x enl (sections_plan), the types
    drawn enlarged as a diagram, so said in the subtitle."""
    L = "LU_BOARD::Sections"
    draw_typology_key.last_w = 0.0
    tot = sum(S.fabric_area.values()) or 1.0
    present = set(t for t in FABRIC_ORDER if round(100.0 * S.fabric_area.get(t, 0.0) / tot) >= 1 or
                  (t in ("monument", "sacred") and S.fabric_area.get(t, 0.0) > 0))
    # (fabric type, use, width m, floors, tag)
    cand = [("traditional", "residential", 9.0, 2, "old town"),
            ("regular", "residential", 10.0, 2, "planned low-rise"),
            ("regular", "commercial", 10.0, 2, "shop below"),
            ("block", "residential", 14.0, 5, "apartment block"),
            ("selfbuilt", "residential", 6.0, 1, "small / shack"),
            ("large", "institutional", 16.0, 2, "civic hall"),
            ("large", "industrial", 18.0, 1, "industry"),
            ("sacred", "religious", 12.0, 1, "mosque"),
            ("monument", "heritage", 10.0, 3, "monument"),
            ("construction", "residential", 10.0, 3, "building site")]
    cand = [c for c in cand if c[0] in present]
    if not cand:
        return y
    gap = 3.0                                             # m between two buildings
    hmax = max(c[3] * STOREY.get(c[1], FLOOR_H) + typo_rise(c[0], c[1], c[2], c[3] * STOREY.get(c[1], FLOOR_H),
                                                            c[0] == "sacred") for c in cand)
    fixed = ss is not None
    if not fixed:
        ss = min(w / (sum(c[2] for c in cand) + gap * len(cand)), 0.3 * U)             # page units per metre
        if ymin is not None:
            ss = min(ss, (y - ymin - 2.4 * U) / hmax)
        if ss < 0.06 * U:
            return y
    t1, t2 = (th, th) if fixed else (0.2 * U, 0.17 * U)  # tag and floor-count heights
    hts = [u"at its height" if c[0] == "monument" else u"{} fl · {}".format(c[3], u_height(c[3] * STOREY.get(
        c[1], FLOOR_H))) for c in cand]                   # v50 (P05.1): floors and height
    slot = [max(c[2] + gap, (max(site28_tw(c[4], t1), site28_tw(h_, t2)) + t1) / ss) if fixed else c[2] + gap
            for c, h_ in zip(cand, hts)]                  # m per type
    ht = 1.5 * th if fixed else 0.6 * U
    draw_typology_key.last_w = max(sum(slot) * ss, site28_tw(u"BUILDING TYPES IN THE SECTIONS", ht, True) if fixed
                                   else 0.0)              # v50: the title within the width (its neighbours' room)
    B.text("BUILDING TYPES IN THE SECTIONS", x, y, ht, INK, L, font=FONT_TITLE, bold=True)
    ys_ = site28_para(B, u"generic silhouettes{} · height = **floors × storey height**: {}, civic {}, sacred {}, industry {} "
               u"· details by type ".format(u", enlarged (a diagram, not to the cuts' scale)" if enl > 1.0 else u"",
                                            u_height(FLOOR_H), u_height(STOREY["institutional"]),
                                            u_height(STOREY["religious"]), u_height(STOREY["industrial"])) + bcite(
        "Building types: generic silhouettes of each fabric type in its own tone: the height is the surveyed floors; "
        "the roof, jetty, windows, balconies, shopfront, dome and minaret height are drawn to the type, not surveyed."),
        x, y - ht - 0.4 * t1 - t1, draw_typology_key.last_w if fixed else max(w, draw_typology_key.last_w), t1, INK2,
        L, lead=1.45, bcol=INK)
    gy = ys_ + 0.85 * t1 - 0.6 * U - hmax * ss            # the common ground line (v50: under the wrapped subtitle)
    P = (lambda s_, z_: (x + s_ * ss, gy + z_ * ss))      # s_ in metres from x, z_ in metres above the ground line
    s0 = 0.5 * gap
    for (fab, cat, bw, fl, tag), sl, h_t in zip(cand, slot, hts):
        s0 += 0.5 * (sl - bw - gap)
        h = fl * STOREY.get(cat, FLOOR_H)
        prof = bld_profile(fab, cat, s0, s0 + bw, 0.0, 0.0, h, fl, seed=0,
                           minaret=(s0 + bw - 0.5 * MINARET_W - 0.4) if fab == "sacred" else None)
        heritage = fab in ("monument", "sacred")
        room = mix(typo_tone(fab, cat), PAPER, 0.12)
        wall_c = mix(FABRIC[fab][2], INK, 0.45) if heritage else INK
        bld_draw_cut(B, L, P, prof, room, wall_c, ss, U, order=27)
        site28_fit(B, tag, x + (s0 + 0.5 * bw) * ss, gy - 0.4 * t1 - t1, t1, sl * ss * 0.95, INK, L, align="C")
        site28_fit(B, h_t, x + (s0 + 0.5 * bw) * ss, gy - 0.8 * t1 - t1 - 1.45 * t2, t2, sl * ss * 0.95, INK2, L,
                   align="C")
        s0 += bw + gap + 0.5 * (sl - bw - gap)
    B.line([P(0.0, 0.0), P(s0 - 0.5 * gap, 0.0)], INK, L, 28, 0.12)
    yb = gy - 1.2 * t1 - t1 - 1.45 * t2
    if crop:
        crop_panel("building_types", x, yb - 0.1 * U, x + w, y - 1.1 * U, u"Building types in the sections")   # v40
    return yb - 0.1 * U


BED_TAG = {"surveyed": "", "interpolated": "", "input": "", "terrain": ""}   # v51: no status on any page (Aras 29 Oct)


def water_tag(depth, src):
    """v16.5: the water's callout in a section: its depth and where the depth comes from."""
    if depth <= 0.005:
        return "NO WATER" if src != "approx" else ""
    return "WATER {:.2f} M".format(depth)                 # v51: no status on any page (Aras 29 Oct 18:56)


SEC_END = 2.4           # page units kept free at both ends of a strip for the end names and levels


# ============================================================ KEY QUESTION, THRESHOLDS, PLAN, SOURCES
def key_cells(S):
    e = S.edge_len
    return [("ACCESSIBLE", e["pedestrian"], EDGE["pedestrian"][1], "walkable edges within reach"),
            ("VISIBLE", e["street"], EDGE["street"][1], "street edges, seen across the water"),
            ("PERMEABLE", e["green"], EDGE["green"][1], "planted edges that let the ground through"),
            ("ENCLOSED", e["building"], EDGE["building"][1], "backs of buildings face the bed"),
            ("DISCONNECTED", S.walled_len + getattr(S, "embanked_len", 0.0), INK2,
             "walled or embanked banks, cut off from the street"),
            ("TRANSFORMABLE", e["parking"] + e["open"], EDGE["open"][1], "parking and loose ground, open to change")]


def draw_key_question(S, B, x, y, w, U, cols=1):
    L = "LU_BOARD::KeyQuestion"
    tot = sum(S.edge_len.values())
    B.text("THE KEY QUESTION", x, y, 0.8 * U, INK, L, font=FONT_TITLE, bold=True)
    y = B.para("where is the stream ...? · % of bank length " + bcite(                                 # v38: keywords
        "Key question: where is the stream accessible, visible, permeable, enclosed, disconnected, or potentially "
        "transformable? Shares of bank length."), x, y - 1.2 * U, w, 0.34 * U, INK2, L)
    if tot <= 0:
        return y
    gap = 1.4 * U
    cw = (w - gap * (cols - 1)) / cols
    y -= 0.6 * U
    cells = key_cells(S)
    crop_panel("key_question", x, y - ((len(cells) + cols - 1) // cols) * 2.3 * U + 0.9 * U, x + w, y + 0.7 * U,
               u"Where is the stream ...? · % of bank length")     # v40: the booklet crop of the bars
    for i, (name, val, col, phrase) in enumerate(cells):
        cx = x + (i % cols) * (cw + gap)
        cy = y - (i // cols) * 2.3 * U
        pct = 100.0 * val / tot
        B.text(name, cx, cy, 0.44 * U, INK, L, font=FONT_TITLE, bold=True)
        B.text("{:.0f}%".format(pct), cx + cw, cy, 0.58 * U, INK, L, font=FONT_TITLE, align="R")
        B.fill([rect(cx, cy - 0.52 * U, cx + cw, cy - 0.3 * U)], FAINT, L, 20)
        if pct > 0:
            B.fill([rect(cx, cy - 0.52 * U, cx + cw * min(1.0, pct / 100.0), cy - 0.3 * U)], col, L, 21)
        B.fit(phrase, cx, cy - 1.08 * U, 0.3 * U, cw, INK2, L)
    return y - ((len(cells) + cols - 1) // cols) * 2.3 * U


def draw_footer(S, B, x, y, w, U, h=0.26):
    """v38: the drawings' ONE numbered source key: the entries the drawings cited as [n] (bcite), then the survey,
    height, use, street, terrain and land-cover sources (were one paragraph). Drawn last, so every [n] is in it."""
    L = "LU_BOARD::Text"
    bcite(u"Survey: 1/1000 survey (halihazır) of Bergama, course material; {} house outlines the survey closed "   # v50
          u"without a floor label ({:.0f} m² or more, not walled yards, courtyards or block insides) drawn as one "   # (P06.3)
          u"storey; {} footprints from OpenStreetMap (© OpenStreetMap contributors, ODbL) where the survey has none, "
          u"drawn with a thin outline on the stream edge plan; {} surveyed floor labels with neither a closed outline "
          u"nor an OpenStreetMap footprint are not drawn.".format(
              S.stats.get("unlabelled", 0), UNLAB_MIN_A, S.stats.get("osm_infill", 0) + S.stats.get("osm_fallback", 0),
              S.stats.get("labels_open", 0)))
    bcite(height_note(S))
    bcite("Storey heights 3.0 m; civic 3.5, sacred 5.0, industry 4.5.")
    bcite("Uses: survey layers and names, Overture Maps places (CDLA-Permissive-2.0) and OpenStreetMap contributors (ODbL).")
    bcite(street_note(S))
    bcite("Terrain: {} survey points, contours, spot heights and bank and stream lines, levels in m a.s.l.; ".format(
        S.terrain_n) + channel_note(S) + ".")
    if getattr(S, "lc", None):
        bcite(LC_CREDIT)                              # v31
    return B.para(u"Sources by number: " + src_key_text(BOARD_KEY), x, y, w, h * U, INK2, L)


def street_note(S):
    km, km_w = getattr(S, "street_km", (0.0, 0.0))
    return ("Streets: widths measured on the survey, road edge to road edge or frontage to frontage, on {:.1f} of {:.1f} km; "
            "the rest are drawn as centre lines.".format(km_w, km))


def water_note(S):
    """v16.5: where the water drawn in the sections comes from."""
    n = len(getattr(S, "water_pts", None) or [])
    if n:
        return ("water surface from {} measured level{}; elsewhere {:g} m above the bed".format(
            n, "s" if n > 1 else "", WATER_DEPTH))
    if WATER_SRC == "input":
        return "water {:g} m above the bed".format(WATER_DEPTH)
    return ("water drawn {:g} m over the bed (the Selinos barely flows: the Kestel dam, 1988, holds its water and much "
            "of it is led into the neighbouring catchment; DAI TransPergMikro 2024, Açık Radyo)".format(WATER_DEPTH))


def channel_note(S):
    C = getattr(S, "chan", None) or {}
    if CH_DEPTH is not None:
        return ("stream bed {:g} m below the banks where the survey has no bed level; ".format(CH_DEPTH)
                + water_note(S))
    if C.get("d"):
        return ("stream bed surveyed at {} of {} cuts every 10 m along the Selinos ({:.1f}-{:.1f} m below the banks); "
                .format(len(C["d"]), C["n_cuts"], min(C["d"]), max(C["d"]))
                + water_note(S))
    return "no surveyed bed levels, so stream beds stay as the terrain shows them; " + water_note(S)


# ============================================================ TWO 16:9 PAGES
PW, PH, PM, TB = 100.0, 56.25, 2.6, 6.6


# ============================================================ v33 · WHAT IS THERE: one plan instead of six
# Aras 24 Oct: any two drawings that show the same ground become one denser drawing. This plan holds what the land-use
# plan, the urban fabric, the intensity, the open-space network and the stream-thresholds maps showed, the canopy-map
# crowns and vegetation of the plant analysis (panels 1, 3, 4), the heritage of diagram D2, the bridges K1-K6, the
# conflict markers C1-C6 of pr1_drawings and the site photos as numbered viewpoints (plant analysis panel 5).
CONTEXT_M = 150.0          # m of quiet context around the site frame (Aras, batch 22 Oct, Q1)
THRESH_W = 0.45            # mm: the stream thresholds, thinner than on the old thresholds map (Aras 22 Oct)
# v40 (Aras 25 Oct 21:38-21:40: "the urban fabric layer back, informal vs planned buildings", as the v28 fabric map):
# plan 01's buildings by fabric type (fabric_types: the rules of bergama_fabric_green v10 / selinus_board v28), in the
# fabric map's lightness order (old town darkest, small irregular houses light) on palette v1.4 roles (board variant)
FABRIC_PLAN = {"monument": C("AF7474"),       # D2 historic
               "sacred": C("8B3A3F"),         # D2 sacred (accent)
               "traditional": C("4A3F35"),    # ink
               "block": C("7A6E60"),          # ink2
               "regular": C("BCB794"),        # structure
               "selfbuilt": C("DCD5C2"),      # faint
               "large": C("FAF8F1"),          # road (lightest void)
               "construction": C("E6E0C8")}   # ground
FABRIC_EDGE = mix(INK, PAPER, 0.25)           # hairline round the light types, as on the fabric map
LEAF_COL = {0: C("8FA05A"), 1: C("8A9478"), 2: C("445A3C")}             # plant analysis LEAF
LEAF_NAME = {0: "deciduous", 1: "evergreen broadleaf (mostly olive)", 2: "needle-leaved"}
# Bridges over the Selinus, survey coordinates: concept record table (CONCEPT_RECORD.md 2.1), as diagrams v1.8
BRIDGES_K = [("K1", u"side inlet crossing", 29628.35, 32630.87), ("K2", u"small crossing", 29604.93, 32622.02),
             ("K3", u"Tabakhane Köprüsü", 30037.01, 32121.57), ("K4", u"Tarihi Ulucami Önü Köprüsü", 29846.40, 32277.71),
             ("K5", u"Üçkemer Köprüsü", 30293.63, 31792.25), ("K6", u"road bridge", 30646.94, 31251.65)]
# Conflict markers of pr1_drawings v3.1 (survey coordinates); C5 sits at the centre of the larger K5 working area
CONFLICTS_C = [("C1", 29941.0, 32200.0, u"walls cut the town off"), ("C2", 30204.0, 31975.0,
                                                                       u"heritage over a hidden stream"),
               ("C3", 29846.0, 32278.0, u"K4: monument and traffic"), ("C4", 30031.6, 32119.5, u"dry bed, bad smell"),
               ("C6", 30830.0, 31160.0, u"industry at the confluence")]
C5_TEXT = u"flood against everyday life"
MARK_C = C("8B3A3F")       # palette accent: conflicts
_PACK = {}


def seam_pack():
    """v33: the plant-analysis data built into this script (SEAM_PACK, from bergama_plant_data_v1.json of
    2026-10-19): canopy-map crowns, site photos, riparian corridor, Landsat heat, section strips."""
    if not _PACK:
        import base64 as _b64
        _PACK.update(json.loads(_zlib.decompress(_b64.b64decode("".join(SEAM_PACK))).decode("utf-8")))
    return _PACK


def context_frame(F, m=CONTEXT_M):
    """The site frame grown by m on every side (a rectangle on the frame's own axes)."""
    return Frame([F.world(u, v) for u, v in ((F.u0 - m, F.v0 - m), (F.u1 + m, F.v0 - m), (F.u1 + m, F.v1 + m),
                                             (F.u0 - m, F.v1 + m))])


def context_lines(RAW, F, m=CONTEXT_M):
    """v33: the survey's buildings, streets and stream banks in the ring of m around the frame (quiet context)."""
    F2 = context_frame(F, m)
    out = {"bld": [], "road": [], "water": []}
    for key, lays in (("bld", list(DWG["bld"]) + [DWG["shed"]]), ("road", DWG["roads"]), ("water", DWG["banks"])):
        for lay in lays:
            for x0, y0, x1, y1 in RAW["lines"].get(lay, []):
                mx, my = 0.5 * (x0 + x1), 0.5 * (y0 + y1)
                if F2.inside(mx, my) and not F.inside(mx, my):
                    out[key].append(((x0, y0), (x1, y1)))
    return out


WHOLE_SKIP = ("NIRENGI", "PINDEX", "NOKTA_", "POLIGON", "SCAN", "MAH_", "YAZI_")   # v36, as fabric_green v10


def whole_frame(RAW, FR, margin=15.0):
    """v36: the whole survey file on the site frame's own axes: every survey layer this board read except the control
    and grid layers, district outlines, labels, layer 0 and the *_alan layers (fabric_green v10's rule)."""
    skip = lambda l: (not l or l.split("::")[-1] == "0" or l.split("::")[-1].upper().startswith(WHOLE_SKIP) or
                      l.lower().endswith("_alan"))
    us, vs = [], []
    for lay, lst in RAW["lines"].items():
        if not skip(lay):
            for s_ in lst:
                for x_, y_ in ((s_[0], s_[1]), (s_[2], s_[3])):
                    u_, v_ = FR.local(x_, y_)
                    us.append(u_)
                    vs.append(v_)
    for lay, lst in (RAW.get("plines") or {}).items():
        if not skip(lay):
            for P in lst:
                for q in P:
                    u_, v_ = FR.local(q[0], q[1])
                    us.append(u_)
                    vs.append(v_)
    if len(us) < 3:
        raise Exception("no survey line work for the whole-file frame")
    u0, u1, v0, v1 = min(us) - margin, max(us) + margin, min(vs) - margin, max(vs) + margin
    return Frame([FR.world(u0, v0), FR.world(u1, v0), FR.world(u1, v1), FR.world(u0, v1)])


def whole_site(RAW, OSM, PLACES, FR, S):
    """v36: the site model over the whole file, for plan 01 only (land use, fabric, land cover, density, stream
    edges); FR, the analysis range, is drawn on it. The tables keep the site frame's model S."""
    FA = whole_frame(RAW, FR)
    SA = build_site_once(RAW, OSM, PLACES, FA)
    SA.U = S.U                                           # the site's line and text sizes
    load_landcover(SA)
    SA.int_cells, SA.int_breaks, SA.int_cell, SA.int_peak, SA.int_peak_name = [], (0, 0, 0), 50.0, 0.0, ""
    SA.edge_runs, SA.wall_runs, SA.edge_samples = [], [], []
    SA.edge_len = dict((k, 0.0) for k in EDGE_ORDER)
    SA.walled_len, SA.embanked_len, SA.bank_runs = 0.0, 0.0, []
    SA.sections, SA.sec_lines, SA.observations = [], [], []
    for fn in (build_intensity, build_edges):
        try:
            fn(SA)
        except Exception:
            LOG.append("whole-file map: {} failed:\n{}".format(fn.__name__, traceback.format_exc()))
    fabric_types(SA)
    SA.ctx_lines, SA.study_areas, SA.water_pts = {}, list(S.study_areas), []
    SA.frame_src, SA.range_F, SA.rest = "whole file", FR, []
    LOG.append("Plan 01 covers the whole file: {:.0f} x {:.0f} m ({:.0f} ha); farmland {:.1f} ha and orchards {:.1f} "
               "ha in it (satellite / inferred).".format(FA.w, FA.h, FA.area / 1e4,
                                                        SA.lc_area.get("farmland", 0.0) / 1e4,
                                                        SA.lc_area.get("orchard", 0.0) / 1e4))
    return SA


C5_XY = (30359.2, 31631.8)     # v36: centroid of the course survey's K5 working area (begum_alan, 55,525 m2)


def roundel(B, x, y, r, txt, fill, ink, L, order=62, h=None):
    B.fill([circle_pts(x, y, r, 16)], fill, L, order)
    B.line(circle_pts(x, y, r, 16) + [circle_pts(x, y, r, 16)[0]], ink, L, order + 1, 0.12)
    B.text(txt, x, y, h or 0.95 * r, ink if fill == (255, 255, 255) else (255, 255, 255), L, order=order + 1,
           font=FONT_TITLE, bold=True, align="MC")


def photo_files(folder):
    """The site photos of the data pack as JPEG files in folder (written once); [(path, item)]. v45: in the order
    they were taken (the walk ran upstream to downstream), so photo 1 is the most upstream on every drawing."""
    import base64 as _b64
    out = []
    if not os.path.isdir(folder):
        os.makedirs(folder)
    for it in sorted(seam_pack().get("photos", {}).get("items", []), key=lambda i_: i_.get("taken", "")):
        p = os.path.join(folder, os.path.splitext(it["file"])[0].replace(".JPG", "") + ".jpg")
        if not os.path.isfile(p):
            with open(p, "wb") as f_:
                f_.write(_b64.b64decode(it["jpeg_b64"]))
        out.append((p, it))
    return out


def stream_normal(S, x, y):
    """v40: the unit normal to the Selinos at the stream point nearest (x, y) (survey axes), or None beyond 60 m."""
    best = None
    for P in getattr(S, "selinus", None) or []:
        for a, b in zip(P[:-1], P[1:]):
            d = seg_dist(x, y, a[0], a[1], b[0], b[1])
            if best is None or d < best[0]:
                best = (d, a, b)
    if best is None or best[0] > 60.0:
        return None
    dx, dy = best[2][0] - best[1][0], best[2][1] - best[1][1]
    n = math.hypot(dx, dy) or 1.0
    return (-dy / n, dx / n)


