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
            sub="dry bulb 2 m · PVGIS point elevation {:.0f} m, assumed [6]".format(CLIMATE["elevation"]),
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


def section_caption(sd_):
    g = sd_["ground"]
    base = sd_["base"]
    # v38 (visual first): keywords, " · " between them (was sentences); the figures are the same, computed live
    cap = "ground +{:.2f} to +{:.2f} · {:.0f} m".format(g[0][1] + base, g[-1][1] + base, sd_["L"])
    beds = [l for l in sd_["levels"] if l[3] == "bed"]
    banks = [l for l in sd_["levels"] if l[3] == "bank"]
    if beds and banks:
        cap += " · bed {:.1f} m below banks{}".format(banks[0][2] - beds[0][2], {   # v40: no caveat words
            "interpolated": " " + bcite("Section bed levels: interpolated along the stream from the "
                                        "surveyed depths.")}.get((sd_.get("bed_src") or ["surveyed"])[0], ""))
        types = sorted(set(short(EDGE[t][0]).lower() for s, t, wl, gz in sd_["labels"]))
        walled = [wl for s, t, wl, gz in sd_["labels"]]
        if types:
            cap += " · banks: " + ", ".join(types)
            if walled and all(w_ == 1 for w_ in walled):
                cap += " · all walled"
            elif any(w_ == 1 for w_ in walled):
                cap += " · partly walled"
            if any(w_ == 2 for w_ in walled):
                cap += " · embanked" if all(w_ == 2 for w_ in walled) else " · partly embanked"
    elif not sd_["water"]:
        cap += " · does not cross the stream"
    tot = sum(sd_["comp"].values()) or 1.0
    top = sorted(sd_["comp"].items(), key=lambda kv: -kv[1])[:3]
    cap += " · through " + ", ".join(["{} {:.0f}%".format(short(CAT[k][0]).lower(), 100.0 * v / tot)
                                      for k, v in top])
    return cap


def draw_locator(S, B, x, ytop, w, U, L, lines_):
    F = S.F
    V, mw, mh = view_fit(F, x, ytop, w, w * F.h / F.w)
    B.fill([V.P(F.P)], PAPER, L, 2)
    for wt in S.water:
        B.fill(V.Ps([wt["P"]] + wt.get("H", [])), BLUE_L, L, 8)
    mini_buildings(S, B, V, L, lambda u: FAINT)
    for (x0, y0, x1, y1, nm) in lines_:
        B.line([V.p(x0, y0), V.p(x1, y1)], INK, L, 15, 0.28)
        bx, by = V.p(x0, y0)
        B.text(nm, bx + 0.2 * U, by + 0.15 * U, 0.3 * U, INK, L, font=FONT_TITLE, bold=True)
    B.line(V.P(F.P + [F.P[0]]), INK2, L, 16, 0.06)
    draw_north_small(B, V, mw, mh, U, L, size=0.38)
    return ytop - mh


# ------------------------------------------------------------ buildings in section
# A cut building is its measured volume: footprint cut by the line, from the ground to its height, tinted by use (or
# by fabric type for monuments and mosques), with a thin line at every storey of its floor count. Nothing the survey
# does not record (roof forms, openings, balconies) is drawn.
SEC_CHANNEL = mix(CAT["water"][1], PAPER, 0.5)        # v16.4: the stream channel's ground colour in section ...
SEC_CHANNEL_HATCH = C("3E7DAE")                      # ... and its blue hatch


def channel_polys(ground, a, b, pad=4.0, top=None):
    """v16.4: the stream channel in section: the area between the cut ground (the bed, carved from the surveyed bed
    levels) and the top of the lower bank, around the water span a..b (m along the line). The bank tops are the
    ground just outside the span; where the ground rises above that level the channel ends. Returns [[(s, z)...]]."""
    gs = [p[0] for p in ground]

    def g_at(s):
        k = max(0, min(len(ground) - 1, _bisect_right(gs, s) - 1))
        k1 = min(len(ground) - 1, k + 1)
        (sa_, za), (sb_, zb) = ground[k], ground[k1]
        return za if sb_ <= sa_ else za + (zb - za) * (s - sa_) / (sb_ - sa_)
    zt = min(g_at(max(gs[0], a - 1.0)), g_at(min(gs[-1], b + 1.0)))
    if top is not None:                                   # v16.5: up to the water surface instead
        zt = min(zt, top)
    pts = [(s, z) for s, z in ground if a - pad <= s <= b + pad]
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


def draw_stream(B, L, P, ground, a, b, bed, lvl, U, wash, fill, hatch, line_c, order, lw=0.035):
    """v16.5: the stream in section: the channel from the bed to the lower bank top in a pale wash, the water from the
    bed to its surface (lvl) filled and hatched in blue, the water line on top. Without water (lvl at the bed) the
    channel itself is hatched, as in v16.4, and the bed drawn as a blue line."""
    if lvl - bed > 0.005:
        draw_channel(B, L, P, channel_polys(ground, a, b), U, wash, None, order)
        wp = channel_polys(ground, a, b, top=lvl)
        draw_channel(B, L, P, wp, U, fill, hatch, order + 1, lw=lw, spacing=0.08)
        for poly in wp:                               # the water line, over the ground line, so a thin layer still reads
            B.line([P(poly[0][0], lvl), P(poly[-1][0], lvl)], line_c, L, order + 6, 0.35)
    else:
        draw_channel(B, L, P, channel_polys(ground, a, b), U, fill, hatch, order, lw=lw)
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


def draw_section_strip(S, B, sd_, x, y, w, ss, U, dry=False, tag="page", scale_txt=None, loc=True):
    """One long section: the surveyed ground, the bed, the buildings at their heights; behind the cut a picture of what
    the section sees (buildings and ground beyond, trees at their measured size, scale figures). v45: loc=False draws
    no locator (the sections page has one key map); scale_txt="" writes no scale word (the page states one)."""
    L = "LU_BOARD::Sections"
    nm = sd_["name"]
    Lm = sd_["L"]
    pk, pn = sd_.get("part", (1, 1))
    off = sd_.get("s_off", 0.0)
    locw = min(9.0 * U, 0.22 * w) if loc else 0.0
    if pk == 1:
        # ---- header: mark, title, one or two caption lines, locator with north arrow
        mk = circle_pts(x + 0.45 * U, y + 0.22 * U, 0.45 * U, 24)
        B.fill([mk], BG, L, 40)
        B.line(mk + [mk[0]], INK, L, 41, 0.1)
        B.text(nm, x + 0.45 * U, y + 0.22 * U, 0.3 * U, INK, L, font=FONT_TITLE, bold=True, align="MC")
        tx = x + 1.2 * U
        tw_ = w - locw - 2.0 * U
        co = sd_.get("crop_of")                          # v42: a cut cropped to the part around the stream
        B.fit("SECTION {0} — {0}'  ·  THE GROUND AS IT FALLS TO THE WATER{1}".format(
            nm, ("  ·  THE {:,.0f} m AROUND THE STREAM OF {:,.0f} m".format(Lm, co[0]) if co else "") if pn == 1 else
            "  ·  IN {} PARTS".format(pn)), tx, y, 0.6 * U, tw_, INK, L, font=FONT_TITLE, bold=True)
        lines = wrap(section_caption(sd_) if pn == 1 else section_caption(sd_.get("whole", sd_)), tw_, 0.3 * U)[:3]
        cy = y - 0.95 * U
        for ln in lines:
            B.text(ln, tx, cy, 0.3 * U, INK2, L)
            cy -= 0.3 * U * 1.8
        if loc:
            lb = draw_locator(S, B, x + w - locw, y + 0.55 * U, locw, U, L, [sd_["line"]])
            top = min(cy + 0.3 * U, lb - 1.2 * U) - 0.5 * U    # v40: the end name S' clear of the locator
        else:
            top = cy + 0.3 * U - 0.5 * U
    else:
        B.fit("SECTION {0} — {0}'  ·  CONTINUED, {1:.0f}-{2:.0f} m".format(nm, off, off + Lm), x + 1.2 * U, y, 0.42 * U,
              w - 2.0 * U, INK2, L, font=FONT_TITLE, bold=True)
        top = y - 0.7 * U
    X0 = x + max(SEC_END * U, (w - Lm * ss) / 2.0)
    Y0 = top - sd_["zmax"] * ss

    def P(px, pz):
        return (X0 + px * ss, Y0 + pz * ss)

    def g_at(s):
        return sd_["ground"][max(0, min(len(sd_["ground"]) - 1, int(round(s / 0.5))))][1]
    # ---- the picture behind the cut
    if not dry:
        png = sec_art_png(S, sd_, ss, tag)
        if png:
            path, zlo_a, zhi_a = png
            base = sd_["base"]
            B.image(path, X0, Y0 + (zlo_a - base) * ss, X0 + Lm * ss, Y0 + (zhi_a - base) * ss, L, 5)
    tags_ = sec_cut(B, L, sd_, P, Lm, ss, U, dry)
    road_calls = draw_sec_roads(S, B, L, P, g_at, sd_["line"], Lm, U, off=off)   # v25: the streets crossed
    # ---- annotation: channel width (its figure goes to the callouts), end levels, end marks, callouts below
    for a, b, bed, lvl in sd_["water"]:
        zt = max(g_at(max(0.0, a - 1.0)), g_at(min(Lm, b + 1.0))) + 2.4
        q0, q1 = P(a, zt), P(b, zt)
        B.line([q0, q1], INK2, L, 35, 0.05)
        for q in (q0, q1):
            B.line([(q[0] - 0.14 * U, q[1] - 0.14 * U), (q[0] + 0.14 * U, q[1] + 0.14 * U)], INK2, L, 35, 0.06)
    for s, zl, za, kind in sd_["levels"]:
        if kind != "end":
            continue
        bx, by = P(s, zl)
        B.fill([[(bx, by), (bx - 0.22 * U, by + 0.38 * U), (bx + 0.22 * U, by + 0.38 * U)]], INK, L, 36)
        out = -1.0 if s < Lm * 0.5 else 1.0              # outside the strip, clear of the buildings at the ends
        B.text("+{:.2f}".format(za), bx + out * 0.4 * U, by + 0.08 * U, 0.26 * U, INK, L,
               align="L" if out > 0 else "R")
    g0, g1 = sd_["ground"][0], sd_["ground"][-1]
    for px_, pz_, lab, out, real in ((g0[0], g0[1], nm, -1.0, pk == 1), (g1[0], g1[1], nm + "'", 1.0, pk == pn)):
        bx, by = P(px_, pz_)
        if real:
            B.text(lab, bx + out * 0.4 * U, by + 0.62 * U, 0.42 * U, INK, L, font=FONT_TITLE, bold=True,
                   align="L" if out > 0 else "R")
        else:                                            # where the parts meet
            B.line([(bx, by - 0.9 * U), (bx, by + 1.2 * U)], INK2, L, 36, 0.05)
            B.text("continues below" if out > 0 else "continued from above", bx - out * 0.3 * U, by + 0.95 * U,
                   0.22 * U, INK2, L, align="R" if out > 0 else "L")
    # the tallest cut roof: its level, as on an architectural section
    if sd_["bld"]:
        a, b, z0, z1, cat, annex, ftype, fl, floors, fsrc = max(sd_["bld"], key=lambda t: t[3])
        lev_ = "+{:.2f}".format(z1 + sd_["base"])
        lw_ = tw(lev_, 0.22 * U)
        for side in ((1.0, -1.0) if (b - a) * ss > 0.6 * U else ()):
            bx, by = P(b if side > 0 else a, z1)         # v16.3: at the eaves beside the wall, clear of the type's tag
            bx += side * 0.4 * U
            t0, t1 = (bx - 0.16 * U, bx + 0.25 * U + lw_) if side > 0 else (bx - 0.25 * U - lw_, bx + 0.16 * U)
            if any(t0 < x1_ and x0_ < t1 and -0.35 * U < y_ - by < 0.35 * U for x0_, x1_, y_ in tags_):
                continue                                 # v40: never over a building's tag; else the other wall
            B.line([(bx - side * 0.4 * U, by), (bx + side * 0.16 * U, by)], INK, L, 36, 0.04)
            B.fill([[(bx, by), (bx - 0.16 * U, by + 0.28 * U), (bx + 0.16 * U, by + 0.28 * U)]], INK, L, 36)
            B.text(lev_, bx + side * 0.25 * U, by + 0.06 * U, 0.22 * U, INK, L, align="L" if side > 0 else "R")
            break
    # v40 (Aras 25 Oct): the words at the water in one clean band right under the cut ground, each on a short leader
    # to its bank or bed point; no word on the drawing's ink, none over another; caveats go to the log, not the page
    calls = sec_water_calls(sd_, g_at, nm, dry) + [(s, g_at(s), t) for s, t in sec_edge_calls(sd_)]
    calls += [((a + b) / 2.0, g_at((a + b) / 2.0), nm_) for a, b, nm_ in sd_.get("places", [])]   # v16.7: by name
    calls += [(s_, z_, sec_road_text(t_)) for s_, z_, t_ in road_calls]   # v25: every street crossed, its width
    calls += [(s_, g_at(s_), t_) for s_, t_ in sec_history_calls(S, sd_) if 0.0 <= s_ <= Lm]   # v44
    low = sec_callouts(B, L, P, calls, P(0, -3.0)[1] - 0.45 * U, U, xlo=x, xhi=x + w)
    # the use ribbon and the satellite rows under the callouts
    rib = low - 0.5 * U
    for a, b, cat in sd_["strip"]:
        B.fill([rect(P(a, 0)[0], rib - 0.16 * U, P(b, 0)[0], rib)], CAT[cat][1], L, 20)
    rib_low = rib - 0.16 * U
    if "_sat" not in sd_:
        sd_["_sat"] = section_sat(sd_)
    if sd_["_sat"]:                                      # v33: land cover and greenness from satellite, metre by metre
        rib_low = draw_sat_strips(B, sd_["_sat"], P, Lm, rib_low, x, U, L)
    sb = nice_floor(Lm / 4.0)
    xb = X0 + Lm * ss - sb * ss - 0.9 * U
    yb = rib_low - 1.05 * U
    draw_scalebar(B, xb, yb, ss, sb, U, L, h=0.26)
    ratio = 1000.0 / max(1e-9, ss * MMU)
    if scale_txt != "":                                  # v45: "" = the page states the one scale
        B.text(scale_txt or "1:{:,.0f} at {:.0f} mm".format(nice_ratio(ratio), SHEET_MM), X0, yb + 0.1 * U,
               0.24 * U, INK2, L)                        # v42: the cuts' common scale on the booklet page
    return yb - 0.35 * U


SEC_CALL_H = 0.6        # v40: the callouts' text height (page units): >= 7.5 pt when the booklet crops a section


def sec_water_calls(sd_, g_at, nm, dry=False):
    """v40: the stream's callouts in a section: its width and depth at the water, its bed level and depth below the
    lower bank at the bed; [(s, z, text)] (text <= 30 characters). Where a figure is interpolated or approximate the
    log says so (not the page)."""
    out, notes = [], []
    srcs = sd_.get("bed_src") or ["surveyed"] * len(sd_["water"])
    wsrc_ = sd_.get("water_src") or [WATER_SRC] * len(sd_["water"])
    banks = [l for l in sd_["levels"] if l[3] == "bank"]
    for k, ((a, b, bed, lvl), src, ws_) in enumerate(zip(sd_["water"], srcs, wsrc_)):
        dep = lvl - bed
        txt = "stream {:.0f} m wide".format(b - a)
        if dep > 0.005:
            txt += " · {:.1f} m deep".format(dep)
        elif ws_ != "approx":
            txt += " · no water"
        out.append((a + (b - a) / 3.0, lvl if dep > 0.005 else bed, txt))
        btxt = "bed +{:.2f}".format(bed + sd_["base"])
        if k < len(banks):
            btxt += " · {:.1f} m below bank".format(banks[k][2] - (bed + sd_["base"]))
        out.append((a + 2.0 * (b - a) / 3.0, bed, btxt))
        if not dry and (src != "surveyed" or ws_ in ("approx", "input")):
            notes.append("Section {}: {}{}.".format(nm, {"interpolated": "bed level interpolated along the stream from the "
                                                                      "surveyed depths", "input": "bed from the "
                                                                      "channel_depth input", "terrain": "no bed level "
                                                                      "surveyed here (terrain)"}.get(src, "bed surveyed"),
                                                   {"approx": "; water depth approximate, not measured",
                                                    "input": "; water depth from the water_depth input"}.get(ws_, "")))
    for t_ in notes:
        if t_ not in LOG:
            LOG.append(t_)
    return out


def sec_history_calls(S, sd_):
    """v44 (PHASE2_SPEC §3, p.7-8): where a cut crosses the survey's historic city wall line (layer SINIR_TARIHI_SUR,
    S.walls_hist) or the covered course of the stream (OSM tunnel / culvert, S.covered): [(s, text)] along the cut.
    Only what the data holds: the survey layer does not date the wall, so no period is named."""
    x0, y0, x1, y1, nm = sd_["line"]
    Lc = math.hypot(x1 - x0, y1 - y0)
    if Lc <= 0:
        return []
    out = []
    for key, txt in (("walls_hist", u"historic city wall"), ("covered", u"covered stream")):
        for P in getattr(S, key, None) or []:
            for a, b in zip(P[:-1], P[1:]):
                hit = seg_x((x0, y0), (x1 - x0, y1 - y0), a, (b[0] - a[0], b[1] - a[1]))
                if hit:
                    s_ = hit[0] * Lc
                    if all(abs(s_ - q) > 3.0 or t_ != txt for q, t_ in out):
                        out.append((s_, txt))
    return out


def sec_road_text(t):
    """v40: a street's callout without the caveat words: its name and the length the cut runs on it."""
    return t.replace(" · OSM line, no surveyed surface", "").replace(" m on the cut", " m")


def sec_edge_calls(sd_):
    """v40: the bank edges where the section meets the water: [(s, text)], e.g. "loose edge · embanked"."""
    return [(s, short(EDGE[typ][0]).lower() + {1: " · walled", 2: " · embanked"}.get(wl, ""))
            for s, typ, wl, gzz in sd_["labels"]]


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
    for a, b, bed, lvl in sd_["water"]:
        # v16.5: the water hatched in blue at its depth (approximate unless measured), the channel above it in a pale
        # wash (v16.4: the whole channel hatched, up to the lower bank top)
        draw_stream(B, L, P, sd_["ground"], a, b, bed, lvl, U, mix(CAT["water"][1], PAPER, 0.72), SEC_CHANNEL,
                    SEC_CHANNEL_HATCH, SEC_CHANNEL_HATCH, 22)
    for s, zb, zt in sd_.get("chwalls", []):
        r0, r1 = P(s - 0.3, zb), P(s + 0.3, zt)
        B.fill([rect(r0[0], r0[1], r1[0], r1[1])], SEC_WALL, L, 27)
    for s, zg in sd_["walls"]:                           # a surveyed wall: its place on the ground, no height
        bx, by = P(s, zg)
        B.fill([[(bx, by + 0.16 * U), (bx - 0.11 * U, by), (bx + 0.11 * U, by)]], SEC_WALL, L, 28)
    # ---- cut buildings: the volume to its height, a line at every storey
    tags_ = []
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
        lab_ = tag_ if (not annex and (b - a) * ss > 0.6 * tw(tag_, 0.17 * U)) else None
        bld_draw_cut(B, L, P, prof, room, wall_c, ss, U, order=27, label=lab_, placed=tags_)
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
                 "Section key: water, hatched blue from the surveyed bed up to its surface (approximate depth unless "
                 "measured: see the callout); the channel above it pale blue.")),
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


def draw_typology_key(S, B, x, y, w, U, ymin=None, ss=None, th=None, crop=True):
    """v16.3 · the building types as the sections draw them: one small generic section of each type found in the frame
    (types under 0.5 % of the footprint are left out, as on the fabric map; mosques and monuments always shown when
    present), with its name. Returns the y below it, or y unchanged when it would not fit above ymin. v44: with ss
    (page units per metre, a round booklet scale) and th (tag height) given, drawn at that scale under the cuts, each
    type as wide as its tag needs; draw_typology_key.last_w = the width used. v45: drawn at the cuts' own scale, so
    it writes no scale of its own (the page states the one scale)."""
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
    slot = [max(c[2] + gap, (tw(c[4], t1) + t1) / ss) if fixed else c[2] + gap for c in cand]   # m per type
    draw_typology_key.last_w = sum(slot) * ss
    ht = 1.5 * th if fixed else 0.6 * U
    B.text("BUILDING TYPES IN THE SECTIONS", x, y, ht, INK, L, font=FONT_TITLE, bold=True)
    B.fit("silhouettes · height = surveyed floors · details by type" + " " + bcite(          # v38; v45: no scale word
        "Building types: generic silhouettes of each fabric type in its own tone: the height is the surveyed floors; "
        "the roof, jetty, windows, balconies, shopfront, dome and minaret height are drawn to the type, not surveyed."),
        x, y - ht - 0.4 * t1 - t1, t1, max(w, draw_typology_key.last_w), INK2, L)
    gy = y - ht - 2.0 * t1 - 0.6 * U - hmax * ss          # the common ground line
    P = (lambda s_, z_: (x + s_ * ss, gy + z_ * ss))      # s_ in metres from x, z_ in metres above the ground line
    s0 = 0.5 * gap
    for (fab, cat, bw, fl, tag), sl in zip(cand, slot):
        s0 += 0.5 * (sl - bw - gap)
        h = fl * STOREY.get(cat, FLOOR_H)
        prof = bld_profile(fab, cat, s0, s0 + bw, 0.0, 0.0, h, fl, seed=0,
                           minaret=(s0 + bw - 0.5 * MINARET_W - 0.4) if fab == "sacred" else None)
        heritage = fab in ("monument", "sacred")
        room = mix(typo_tone(fab, cat), PAPER, 0.12)
        wall_c = mix(FABRIC[fab][2], INK, 0.45) if heritage else INK
        bld_draw_cut(B, L, P, prof, room, wall_c, ss, U, order=27)
        B.fit(tag, x + (s0 + 0.5 * bw) * ss, gy - 0.4 * t1 - t1, t1, sl * ss * 0.95, INK2, L, align="C")
        B.fit("{} fl".format(fl) if fab != "monument" else "at its height", x + (s0 + 0.5 * bw) * ss,
              gy - 0.8 * t1 - t1 - 1.45 * t2, t2, sl * ss * 0.95, INK2, L, align="C")
        s0 += bw + gap + 0.5 * (sl - bw - gap)
    B.line([P(0.0, 0.0), P(s0 - 0.5 * gap, 0.0)], INK, L, 28, 0.12)
    yb = gy - 1.2 * t1 - t1 - 1.45 * t2
    if crop:
        crop_panel("building_types", x, yb - 0.1 * U, x + w, y - 1.1 * U, u"Building types in the sections")   # v40
    return yb - 0.1 * U


BED_TAG = {"surveyed": "", "interpolated": " (INTERPOLATED)", "input": " (INPUT DEPTH)", "terrain": " (NOT SURVEYED)"}


def water_tag(depth, src):
    """v16.5: the water's callout in a section: its depth and where the depth comes from."""
    if depth <= 0.005:
        return "NO WATER" if src != "approx" else "WATER NOT SURVEYED"
    return "WATER {:.2f} M{}".format(depth, {"approx": " (APPROXIMATE, NOT MEASURED)", "input": " (WATER_DEPTH INPUT)",
                                             "measured": " (MEASURED LEVEL)"}.get(src, ""))


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
    bcite("Survey: 1/1000 survey (halihazir) of Bergama, course material; {} footprints from OpenStreetMap where the "
          "survey has none; {} surveyed floor labels whose outline the survey never closed are not drawn.".format(
              S.stats.get("osm_infill", 0) + S.stats.get("osm_fallback", 0), S.stats.get("labels_open", 0)))
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
        own = ("{:g} m (water_depth input)".format(WATER_DEPTH) if WATER_SRC == "input" else
               "an APPROXIMATE {:g} m".format(WATER_DEPTH))
        return ("water surface from {} measured level{} (water_levels input), interpolated along the stream between "
                "them; elsewhere {} above the bed".format(n, "s" if n > 1 else "", own))
    if WATER_SRC == "input":
        return "water {:g} m above the bed (water_depth input)".format(WATER_DEPTH)
    return ("water level not surveyed and no published depth found: drawn as an APPROXIMATE {:g} m over the surveyed bed "
            "(the Selinus barely flows: the Kestel dam, 1988, holds its water and much of it is led into the "
            "neighbouring catchment; DAI TransPergMikro 2024, Acik Radyo)".format(WATER_DEPTH))


def channel_note(S):
    C = getattr(S, "chan", None) or {}
    if CH_DEPTH is not None:
        return ("stream bed {:g} m below the banks where the survey has no bed level (channel_depth input); ".format(CH_DEPTH)
                + water_note(S))
    if C.get("d"):
        return ("stream bed surveyed at {} of {} cuts every 10 m along the Selinus ({:.1f}-{:.1f} m below the banks), "
                "interpolated along the stream between them; ".format(len(C["d"]), C["n_cuts"], min(C["d"]), max(C["d"]))
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


def site_crowns(S, F2):
    """Canopy-map crowns (modelled, Meta/WRI 1 m canopy height map) inside F2: [(x, y, r, h, leaf)]."""
    rows = seam_pack().get("crowns", {}).get("rows", [])
    return [(r[0], r[1], r[2], r[3], r[4]) for r in rows if F2.inside(r[0], r[1])]


def dense_outline(S, cls_min=3, min_cells=20):
    """The outline of the densest grain: groups of at least min_cells touching cells of intensity class >= cls_min
    (10 m cells, so 20 cells = 2,000 m2); single dense cells are left out (they outline one building, not an area)."""
    cells = [P for P, cls, j in getattr(S, "int_cells", []) if cls >= cls_min]
    key = lambda a, b: tuple(sorted(((round(a[0], 2), round(a[1], 2)), (round(b[0], 2), round(b[1], 2)))))
    par = list(range(len(cells)))

    def find(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i
    owner, cnt = {}, {}
    for i, P in enumerate(cells):
        for k in range(len(P)):
            e = key(P[k], P[(k + 1) % len(P)])
            cnt[e] = cnt.get(e, 0) + 1
            if e in owner:
                a, b = find(i), find(owner[e])
                if a != b:
                    par[a] = b
            else:
                owner[e] = i
    size = {}
    for i in range(len(cells)):
        r = find(i)
        size[r] = size.get(r, 0) + 1
    return [list(e) for e, c in cnt.items() if c == 1 and size[find(owner[e])] >= min_cells]


C5_XY = (30359.2, 31631.8)     # v36: centroid of the course survey's K5 working area (begum_alan, 55,525 m2)


def c5_point(S):
    if not getattr(S, "study_areas", None):
        return C5_XY
    best = None
    for a in getattr(S, "study_areas", []) or []:
        if a["name"] == "BEGUM" and (best is None or a["area"] > best["area"]):
            best = a
    if not best:
        return None
    _a, cx, cy = shoelace(best["P"])
    return (cx, cy)


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


def fabric_col(u):
    """v40: a building on plan 01 by its fabric type (the fabric map's rule: sheds and annexes paler)."""
    col = FABRIC_PLAN[u.get("fabric", "regular")]
    return mix(col, PAPER, 0.45) if u["annex"] else col


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


def draw_what_is_there(S, B, x, y, w, U):
    """S1: the site as it is on one plan, the frame and CONTEXT_M of quiet context, at the board scale. Returns the
    y below its legend."""
    L = "LU_BOARD::WhatIsThere"
    F = S.F
    RF = getattr(S, "range_F", None)                      # v36: set on the whole-file model: the analysis range
    F2 = F if RF is not None else context_frame(F)
    r_map = bcite("Plan 01: the map covers the whole survey file; the thin line is the analysis range (site_alan). Crowns "
                  "and photos exist for the site only." if RF is not None else
                  "Plan 01: context beyond the frame: survey line work only.")
    B.text("WHAT IS THERE · GROUND · BUILDINGS · GREEN · STREAM EDGE " + r_map, x, y, 1.05 * U, INK, L,
           font=FONT_TITLE, bold=True)                    # v38: keywords; the coverage note is a key entry
    # v45: plan 01 prints at 1:den_bk beside the site readings (P01_BK_W mm wide): its marks and words are sized for
    # that page (kb = board units per booklet mm; the map is as wide as w)
    den_bk = bk_std(F2.w * 1000.0 / P01_BK_W)
    kb = w / F2.w * den_bk / 1000.0
    # v42 (review rule 4): what the plan shows, why it is here, what to read from it; sized with the plan's width
    ch_ = max(CTX_H * U * max(1.0, w / (120.0 * U)), bk_hk(7.0, kb, mono=True))
    ctop = y - 0.6 * U - ch_
    ymap = ctx_line(B, u"The whole survey area as it is today, on one plan: buildings by urban fabric, ground and green, "
                       u"the Selinos with its edges, bridges and photo points. It is the base the later plans are read "
                       u"on: what the project keeps, joins and changes.", x, ctop, w, ch_, L) - 0.2 * ch_
    V, mw, mh = view_fit(F2, x, ymap, w, 10.0 * w)
    s = V.s
    # quiet context: survey line work around the frame, pale
    B.fill([V.P(F2.P)], mix(PAPER, (255, 255, 255), 0.55), L, 1)
    ctx = getattr(S, "ctx_lines", None) or {}
    for key, col, wd in (("water", mix(BLUE_D, PAPER, 0.5), 0.06), ("road", mix(INK2, PAPER, 0.62), 0.04),
                         ("bld", mix(INK2, PAPER, 0.45), 0.04)):
        for a, b in ctx.get(key, []):
            B.line([V.p(*a), V.p(*b)], col, L, 2, wd)
    # the site: land use, land cover, ground, streets, trees, buildings (homes by fabric), walls, bridges
    draw_landuse_map(S, B, V, bcol=fabric_col)            # v40: buildings by urban fabric type
    for u in S.bld:                                       # light types get a hairline so they read on paper
        if not u["annex"] and u.get("fabric") in ("selfbuilt", "large", "construction"):
            for P in u["parts"]:
                B.line(V.P(P + [P[0]]), FABRIC_EDGE, L, 15, 0.03)
    # canopy-map crowns (modelled), under the surveyed tree symbols
    crowns = [c for c in site_crowns(S, F) if F.inside(c[0], c[1])]
    for leaf in (0, 1, 2):
        pts = [circle_pts(V.p(cx, cy)[0], V.p(cx, cy)[1], max(0.06 * U, r * s), 10) for cx, cy, r, h, lf in crowns
               if lf == leaf]
        for k in range(0, len(pts), 400):
            B.fill(pts[k:k + 400], mix(LEAF_COL[leaf], PAPER, 0.25), L, 10)
    # footpaths (the open-space network's links)
    path_c = mix(CAT["green"][1], INK, 0.35)
    for p in S.paths:
        for d in dashes(V.P(p["P"]), 0.35 * U, 0.25 * U):
            B.line(d, path_c, L, 19, 0.16)
    # dense fabric (intensity): the outline of the densest floor-area class
    dens = dense_outline(S)
    dc = mix(INTENSITY[3], INK, 0.1)
    for a, b in dens:
        B.line([V.p(*a), V.p(*b)], dc, L, 23, 0.3)
    # stream thresholds, thinner, along the banks
    for typ, pts in getattr(S, "edge_runs", []):
        B.line(V.P(pts), EDGE[typ][1], L, 24, THRESH_W)
    for pts in getattr(S, "wall_runs", []):
        for d in dashes(V.P(pts), 0.16 * U, 0.14 * U):
            B.line(d, PAPER, L, 25, THRESH_W * 0.4)
    # frame, river name, section marks (shared with the section drawings)
    draw_map_annotations(S, B, V, U, rh=bk_hk(8.0, kb))  # v45: no cut lines; the stream's name 8 pt
    B.line(V.P(F.P + [F.P[0]]), INK, L, 26, 0.25)
    if RF is not None:                                    # v36: the analysis range (site_alan) on the whole-file map
        B.line(V.P(RF.P + [RF.P[0]]), INK, L, 26, 0.12)
    # bridges, conflicts, photos (v40, Aras 25 Oct 21:41: drawn marks with plain short labels, no boxes, no sentences)
    cs = list(CONFLICTS_C)
    c5 = c5_point(S)
    if c5:
        cs.append(("C5", c5[0], c5[1], C5_TEXT))
    photos = []
    try:
        photos = photo_files(os.path.join(SELINUS_RES_DIR, "_site_photos"))
    except Exception:
        LOG.append("WARNING: the site photos could not be written:\n" + traceback.format_exc())
    # v45: marks and names sized for the booklet page (K names 9 pt, C and photo numbers 7.5 pt), each name placed
    # clear of every mark and name (place_labels: on a thin leader where it must move away)
    hk, hs = bk_hk(9.0, kb), bk_hk(7.5, kb)
    taken, labs = [], []
    for k, nm, bx, by in BRIDGES_K:                       # a tick across the stream
        if F.inside(bx, by):
            px, py = V.p(bx, by)
            n = stream_normal(S, bx, by) or (0.0, 1.0)
            a_ = V.p(bx + n[0], by + n[1])
            ln = math.hypot(a_[0] - px, a_[1] - py) or 1.0
            e = ((a_[0] - px) / ln * 1.6 * kb, (a_[1] - py) / ln * 1.6 * kb)
            B.line([(px - e[0], py - e[1]), (px + e[0], py + e[1])], INK, L, 62, bk_lw(0.35, kb))
            taken.append((px - 1.6 * kb, py - 1.6 * kb, px + 1.6 * kb, py + 1.6 * kb))
            labs.append(([k], px, py, hk, INK))
    for k, cx, cy, t in cs:                               # a dot in the accent
        if F.inside(cx, cy):
            px, py = V.p(cx, cy)
            B.fill([circle_pts(px, py, 0.9 * kb, 12)], MARK_C, L, 63)
            taken.append((px - 0.9 * kb, py - 0.9 * kb, px + 0.9 * kb, py + 0.9 * kb))
            labs.append(([k], px, py, hs, MARK_C))
    for i, (p, it) in enumerate(photos):                  # a small ink dot
        px, py = V.p(it["x"], it["y"])
        B.fill([circle_pts(px, py, 0.7 * kb, 12)], INK, L, 64)
        taken.append((px - 0.7 * kb, py - 0.7 * kb, px + 0.7 * kb, py + 0.7 * kb))
        labs.append(([str(i + 1)], px, py, hs, INK))
    mb = ymap - mh
    pkey = place_labels(B, labs, taken, L, bounds=(V.X0, mb, V.X0 + mw, ymap), order=65)
    # v45: scale bar and north arrow under the map, never on it; numbers 7 pt under the bar
    sbl = nice_floor(F2.w / 8.0)
    mb_crop = min(draw_scalebar_bk(B, V.X0, mb - 3.0 * kb, s, sbl, kb, L), mb - 9.5 * kb)
    draw_north_at(B, F2, V.X0 + sbl * s + 12.0 * kb, mb - 5.0 * kb, 4.0, kb, L)
    if pkey:                                              # names with no free place: a number, the words under the bar
        mb_crop = draw_label_key(B, pkey, V.X0, mb_crop - 1.0 * kb, mw, hs, L)
    # photo strip under the map
    yy = min(mb - 2.6 * U, mb_crop - 1.0 * U)
    if photos:                                        # v44: a keyword caption under each photo, numbers 12 pt
        n = len(photos)
        g = 0.6 * U
        pw = (mw - (n - 1) * g) / n
        ph = pw * 0.75
        s_ph = bk_s(mw, ph * 1.4)                         # the strip across a booklet page (row of its own)
        hc, hn = bk_h(7.5, s_ph), bk_h(12.0, s_ph)
        bn = 1.7 * hn
        low = yy - ph
        r_ph = bcite(u"Photos: site visit 2026-10-01 (group photos, GPS within {:.0f} m); the disc marks where each "
                     u"was taken. Captions: keywords of the photo index (a visual reading); Roman bridges after h01 "
                     u"§5.".format(max(it.get("gps_err_m", 0.0) for p, it in photos)))
        for i, (p, it) in enumerate(photos):
            px = V.X0 + i * (pw + g)
            B.image(p, px, yy - ph, px + pw, yy, L, order=5)
            B.fill([rect(px, yy - bn, px + bn, yy)], INK, L, 64)
            B.text(str(i + 1), px + 0.5 * bn, yy - 0.5 * bn, hn, (255, 255, 255), L, order=65,
                   font=FONT_TITLE, bold=True, align="MC")
            cap = photo_caption(it) + (u" " + r_ph if i == n - 1 else u"")
            cy_ = yy - ph - 0.6 * hc - hc
            for ln in wrap(cap, pw, hc, "sans")[:2]:
                B.text(ln, px, cy_, hc, INK, L, font=FONT_TITLE)
                low = min(low, cy_)
                cy_ -= 1.45 * hc
        crop_panel("photos", V.X0, low - 0.5 * hc, V.X0 + mw, yy, u"Site photos · 1 Oct 2026")     # v40
        yy = low - 1.2 * U
    # legend (v38: drawn samples with short names; explanations as [n] in the Sources key)
    r_home = bcite("Urban fabric: each building's type from its survey layer, names and heritage tags, surveyed floors, "
                   "footprint size and regularity, shared walls and the grain of the 40 m around it; shares of the "
                   "built footprint.")
    r_crown = bcite("Crowns: modelled heights and leaf types (Meta/WRI 1 m canopy height map, Tolan et al. 2024; CLC+ "
                    "2021 and Sentinel-2).")
    r_edge = bcite("Stream edges: what meets the water along each bank.")
    leg = [("hdr", None, "BUILDINGS · URBAN FABRIC " + r_home)]
    ftot = sum(S.fabric_area.values()) or 1.0
    for fab in FABRIC_ORDER:                              # v40: the fabric map's types; under 0.5 % left out
        v_ = 100.0 * S.fabric_area.get(fab, 0.0) / ftot
        if round(v_) >= 1 or (fab in ("monument", "sacred") and S.fabric_area.get(fab, 0.0) > 0):
            leg.append(("box", FABRIC_PLAN[fab], u"{} · {}".format(FABRIC_SHORT[fab], "{:.0f}%".format(v_)
                                                                    if round(v_) >= 1 else "< 1%")))
    leg += [("dense", dc, "Densest grain · floor-area ratio {:.2f}+ {}".format(
                S.int_breaks[2], bcite("Densest grain: floor-area ratio on 10 m cells, areas of 2,000 m2+."))
             if getattr(S, "int_breaks", None) else "Densest grain")]
    leg += [("hdr", None, "GROUND AND GREEN")]
    for k_, lab in (("wood", "Woods"), ("park", "Parks"), ("grass", "Grass & lawns")):
        leg.append(("box", GREEN_SUB[k_], lab))
    leg += [("box", CAT["agri"][1], "Fields & orchards (survey, OSM)"), ("box", CAT["vacant"][1], "Vacant ground"),
            ("box", mix(CAT["transport"][1], PAPER, 0.3), "Parking & yards"), ("box", CAT["water"][1], "The stream")]
    for k_, lab, col in LC_CLASSES:
        if getattr(S, "lc", {}).get(k_):
            leg.append(("box", col, lab))
    for lf in (0, 1, 2):
        if any(c[4] == lf for c in crowns):
            leg.append(("dot", mix(LEAF_COL[lf], PAPER, 0.25), "Crown · " + LEAF_NAME[lf] + " " + r_crown))
    leg += [("dot", TREE_COLS["pine"], "Tree symbols of the survey"), ("dash", path_c, "Footpaths")]
    leg += [("hdr", None, "THE STREAM EDGE " + r_edge)]
    for k_ in EDGE_ORDER:
        if S.edge_len.get(k_, 0) > 0:
            leg.append(("thin", EDGE[k_][1], short(EDGE[k_][0])))
    leg += [("hdr", None, "MARKS")]
    leg += [("ktick", INK, "Bridges K1-K6")]
    leg += [("cdot", MARK_C, "{} {}".format(k, t)) for k, cx, cy, t in sorted(cs) if F.inside(cx, cy)]
    if photos:
        leg.append(("pdot", INK, "Photo viewpoints 1-{}".format(len(photos))))
    if RF is not None:
        leg.append(("thin", INK, "Analysis range (site_alan) " + r_map))
    ly = draw_legend_items(B, leg, x, yy - 1.0 * U, mw, U, L, h=0.4)
    # v45: the booklet page's legend leaves out what the site readings beside the plan already key: the ground and
    # green colours (the land-use ring's key) and the edge types (the bars); footpaths as a line
    ring_c = set(c_ for l_, c_, a_ in landuse_slices(getattr(S, "site", S))[0])
    leg_bk, grp = [], ""
    for kind, col, lab in leg:
        if kind == "hdr":
            grp = lab
        elif not ((grp == "GROUND AND GREEN" and kind == "box" and col in ring_c) or grp.startswith("THE STREAM EDGE")):
            leg_bk.append(("line" if kind == "dash" else kind, col, lab))
    crop_panel("plan01", V.X0, mb_crop - 0.5 * kb, V.X0 + mw, ctop + ch_ + 0.3 * U, u"Plan 01 · what is there today",
               crop_scale(s), crop_legend(leg_bk))        # v40; v42: from the context line down
    # v42: survey x, y of the plan's frame corners and where they sit on the sheet, so a later script (the farms map,
    # bergama_agriculture_alternatives) can place its own layer on this very plan in the booklet crop
    CROP_PANELS[-1]["geo"] = [(px_, py_) + tuple(V.p(px_, py_)) for px_, py_ in F2.P[:4]]
    tot = sum(S.fabric_area.values()) or 1.0
    # v38: the caption's two figures as tiles (were sentences); its notes are the key entries cited above
    return vis_tiles(B, x, ly - 0.3 * U, min(mw, 44.0 * U), [
        ("build", "OLD TOWN · % OF BUILT FOOTPRINT", "{:.0f}%".format(100.0 * S.fabric_area.get("traditional", 0.0) / tot),
         r_home),
        ("green", "CROWNS IN THE FRAME", "{}".format(len(crowns)), r_crown)], U, L, h=1.3, ink=INK, grey=INK2,
        fill=mix(PAPER, (255, 255, 255), 0.5), rule=FAINT)



