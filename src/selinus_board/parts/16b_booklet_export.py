# ============================================================ v40: A3 BOOKLET = CROPS OF THE SHEETS (CROP_SPEC)
# v60 (round 5, G-R5-12): the crops are no longer cut out of sheet PDFs: 16d_items.py hands each registered crop
# (crop_panel) to the booklet as item drawings + anchored labels (items.json). This file keeps the crop registry
# (crop_panel, crop_default, crop_scale, crop_legend), the live figures (bk_results -> results.json) and the photos.
BK_SCRIPT = "MainBoard"
BK_VERSION = "v55"
BK_LOG = []                                           # notes of the booklet step (booklet/booklet_log.txt)
CROP_PANELS = []                                      # v40: dict(slug, bb, caption, scale_den, legend, drop), board units
CROP_DIRECT = []                                      # v40: crops of pages laid out in mm (the axonometric)
SHEET_POS = []                                        # v40: (drawing name, pdf, frame, x mm, y mm, page h mm) per drawing
CROP_REF = r"^\[\d+\]$"                               # a sheet's lone [n] mark: its source key is not in the crop


def crop_panel(slug, x0, y0, x1, y1, caption="", scale_den=None, legend=None, drop=None):
    """v40: one booklet crop: a panel's rectangle in board units (any two corners), as the layout drew it. A drawing
    that calls this has no default crop (crop_default)."""
    CROP_PANELS.append(dict(slug=slug, bb=(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)), caption=caption,
                            scale_den=scale_den, legend=legend or [], drop=[CROP_REF] + list(drop or [])))


def crop_default(name, x0, y0, x1, y1, n0, slug=None, caption="", panel=None):
    """v40: a drawing that registered no crop of its own (n0 = len(CROP_PANELS) before it was drawn) gets one: the
    panel rectangle its drawer left in PANEL_RECTS[panel] when there is one, else the drawing below its title line;
    slug and caption from its name unless given ("12 Section S1" -> section_s1)."""
    if len(CROP_PANELS) != n0:
        return
    slug = slug or "_".join(w_ for w_ in "".join(c_ if c_.isalnum() else " " for c_ in name.lower()).split()[1:])
    pr = (globals().get("PANEL_RECTS") or {}).get(panel) if panel else None
    leg = []
    if panel == "riparian" and globals().get("rip_legend"):
        try:
            leg = crop_legend(globals()["rip_legend"]())
        except Exception:
            leg = []
    if pr:
        x0, y0, x1, y1 = pr[:4]
    crop_panel(slug or "panel", x0, y0, x1, y1, caption or name.split(" ", 1)[-1], legend=leg, drop=[r"^SECTION "])


def crop_scale(s):
    """The scale denominator of a plan drawn at s board units per metre, the sheet printed 1:1."""
    return int(round(PDF_SCALE / s)) if s else None


def crop_hex(c):
    return c.lstrip("#").upper() if isinstance(c, str) else "%02X%02X%02X" % tuple(int(v) for v in c[:3])


CROP_LEG_KIND = {"box": "fill", "dot": "dot", "dash": "dash", "line": "line", "thin": "line", "thick": "line",
                 "dense": "line", "street": "line", "walled": "line", "embanked": "line", "ktick": "line",
                 "cdot": "dot", "pdot": "dot", "study": "dashdot"}


def crop_legend(leg):
    """A sheet legend (draw_legend_items rows) as booklet legend entries: drawn sample + plain name, no [n] marks."""
    import re as _re
    out = []
    for kind, col, label in leg:
        if kind == "hdr" or col is None or kind not in CROP_LEG_KIND:
            continue
        t = _re.sub(r"\s*\[\d+\]", "", label).strip()
        if t:
            out.append({"kind": CROP_LEG_KIND[kind], "colour": crop_hex(col), "label": t})
    return out


def crop_sheet_key(pdf):
    """The short sheet key of a crop id: drw, sec, axo, t1 ... t8."""
    stem = os.path.splitext(os.path.basename(pdf))[0]
    if stem.startswith("Selinus_drawings"):
        return "drw" + stem[len("Selinus_drawings"):]
    if stem.startswith("Selinus_sections"):
        return "sec" + stem[len("Selinus_sections"):]
    if "axonometric" in stem:
        return "axo"
    if stem.startswith("Selinus_T") and len(stem) > 9 and stem[9].isdigit():
        return "t" + stem[9]
    return stem.lower()


def bk_results(S):
    """The figures this board computes for the booklet's A pages (plan_merged.json: values_from "none"), by key. Every
    value is computed here from the same data and with the same rule as the sheet that prints it."""
    R = {"script": SCRIPT_VERSION, "note": "figures computed by the site board for the booklet (A pages)"}
    rd = lambda v, n=1: None if v is None else round(float(v), n)
    # ---- A1 · readings and land use (draw_legend, page1_readings)
    tot = frame_total(S)
    R["frame_ha"] = rd(tot / 1e4, 2)
    R["frame_w_m"], R["frame_h_m"] = rd(S.F.w, 0), rd(S.F.h, 0)
    R["built_pct_of_frame"] = rd(100.0 * S.built_area / S.frame_area)
    R["void_pct_of_frame"] = rd(100.0 - 100.0 * S.built_area / S.frame_area)
    R["mapped_pct_of_frame"] = rd(100.0 * S.total_area / tot)
    R["homes_pct_of_mapped"] = rd(100.0 * S.area.get("residential", 0.0) / S.total_area)
    P1 = page1_readings(S)
    if P1.get("floors"):
        share, avg, peak = P1["floors"]
        R["floors_mean"] = rd(avg, 2)
        R["floors_one_pct"] = rd(share.get(1, 0.0))
        R["densest_near"] = peak
    fa = sum(S.fabric_area.values()) or 1.0
    R["old_town_pct_of_built_frame"] = rd(100.0 * S.fabric_area.get("traditional", 0.0) / fa)
    SA = getattr(S, "whole", None)
    if SA is not None and getattr(SA, "fabric_area", None):   # plan 01's tile: the whole-file map's footprint
        fa = sum(SA.fabric_area.values()) or 1.0
        R["old_town_pct_of_built_wholefile"] = rd(100.0 * SA.fabric_area.get("traditional", 0.0) / fa)
    R["green_pct_of_frame_mapped"] = rd(P1["green"][0], 2)
    R["green_pct_with_satellite"] = rd(P1["green"][2]) if P1["green"][2] is not None else None
    for k in CAT_ORDER:
        R["landuse_pct_" + k] = rd(100.0 * S.area.get(k, 0.0) / tot)
    for k_, lab, col, a in (getattr(S, "rest", None) or []):
        R["unmapped_pct_" + k_] = rd(100.0 * a / tot)
    # ---- v40: the stream bed under its banks, from the survey cuts (channel_profile; the log's channel_note)
    C_ = getattr(S, "chan", None) or {}
    if C_.get("d"):
        R["bed_below_banks_min_m"] = rd(min(C_["d"]), 1)
        R["bed_below_banks_max_m"] = rd(max(C_["d"]), 1)
        R["bed_cuts_n"] = len(C_["d"])
        R["bed_cuts_total"] = C_.get("n_cuts")
    # ---- A2 · sky view of the stream bed (stream_sky)
    sky = stream_sky(S)
    if sky:
        lows = sorted(m[2] for m in sky["marks"] if m[3] == "low")
        R["sky_bed_mean_pct"] = rd(100.0 * sky["mean"], 0)
        R["sky_most_enclosed_pct"] = rd(100.0 * lows[0], 0) if lows else None
        R["sky_enclosed_pcts"] = [rd(100.0 * v, 0) for v in lows[1:]]
        R["sky_most_open_pct"] = rd(100.0 * max(m[2] for m in sky["marks"]), 0)
    # ---- A3 · movement, services (movement(), draw_how_people_use_it)
    MV = movement(S) or {}
    if MV.get("rows"):
        R["busiest_street"] = MV["rows"][0]["name"]
        R["busiest_street_index"] = rd(MV["rows"][0]["comb_b"], 0)
    for k_, nm in (("walk_b", "walk"), ("car_b", "drive"), ("comb_b", "combined")):
        if (MV.get("rho") or {}).get(k_) is not None:
            R["spearman_shops_" + nm] = rd(MV["rho"][k_], 2)
    if MV.get("big"):
        R["streets_50m_n"] = len(MV["big"])
    try:
        DG, ctx = diagram_ctx(S)
        n_pl = {}
        for p in ctx.places:
            if S.F.inside(p[0], p[1]):
                n_pl[p[2]] = n_pl.get(p[2], 0) + 1
        for fn_, let, c, lab in WALK_FUN:
            R["places_" + fn_] = n_pl.get(fn_, 0)
    except Exception:
        BK_LOG.append("results: services not counted\n" + traceback.format_exc())
    # ---- A4 · the key question: % of bank length (key_cells)
    etot = sum(S.edge_len.values())
    if etot > 0:
        for name, val, col, phrase in key_cells(S):
            R["bank_%s_pct" % name.lower()] = rd(100.0 * val / etot, 0)
        R["bank_length_m"] = rd(etot, 0)
    env = getattr(S, "env", None) or {}
    # ---- A5 · T1 noise (sheet_sound)
    nm = env.get("noise")
    if nm:
        cells = [c for row in nm["grid"] for c in row if c and c.get("lden") is not None]
        n_out = sum(1 for row in nm["grid"] for c in row if c and c.get("out"))
        ntot = max(1, len(cells) + n_out)
        R["t1_over53_lden_pct"] = rd(100.0 * sum(1 for c in cells if c["lden"] > 53.0) / ntot, 0)
        R["t1_over45_night_pct"] = rd(100.0 * sum(1 for c in cells if c["night"] is not None and c["night"] > 45.0)
                                      / ntot, 0)
    # ---- T2 surface heat, summer (heat_scale, lst_tiles, heat_canopy_inset)
    if env.get("lst"):
        hsc = heat_scale(S, "summer")
        if hsc:
            R["t2_summer_median_c"] = rd(hsc[1], 2)
        tl = dict((t[1], t[2]) for t in lst_tiles(S, "summer"))
        if "AT THE STREAM" in tl:
            R["t2_summer_stream_vs_150m_c"] = rd(float(tl["AT THE STREAM"].split()[0]), 1)
            R["t2_summer_within50m_c"] = rd(float(tl["WITHIN 50 m OF STREAM"].split()[0]), 1)
            R["t2_summer_beyond150m_c"] = rd(float(tl["BEYOND 150 m"].split()[0]), 1)
        hs = (seam_pack().get("heat") or {}).get("seasons", {}).get("summer")
        pts = (hs or {}).get("points") or []
        if pts:
            v0 = [t for c, t in pts if c <= 0.0]
            v25 = [t for c, t in pts if 0.25 <= c < 1.01]
            R["t2_summer_no_crowns_c"] = rd(sum(v0) / len(v0), 2) if v0 else None
            R["t2_summer_dense_crowns_c"] = rd(sum(v25) / len(v25), 2) if v25 else None
    # ---- T3 shade, the mean day of the year (shade_tiles)
    if env.get("shade"):
        it = [i_ for i_ in shade_items(S) if i_["key"] == "year"][0]
        tl = dict((t[1], t[2]) for t in shade_tiles(S, it))
        R["t3_year_mean_shade_h"] = tl.get("OPEN GROUND · MEAN SHADE", "").replace(" h", "") or None
        R["t3_year_share_of_daylight_pct"] = rd(float(tl["SHARE OF THE DAYLIGHT"].split()[0]), 0) \
            if "SHARE OF THE DAYLIGHT" in tl else None
        R["t3_year_shaded_over_half_pct"] = rd(float(tl["SHADED > HALF THE DAY"].split()[0]), 0) \
            if "SHADED > HALF THE DAY" in tl else None
        R["t3_year_within30m_stream_shade_h"] = tl.get("WITHIN 30 m OF STREAM", "").replace(" h", "") or None
    # ---- T4 radiation, summer (rad_tiles)
    if env.get("rad"):
        tl = dict((t[1], t[2]) for t in rad_tiles(S, "summer"))
        for key, lab in (("roof_mean", "ROOFS · MEAN kWh/m²·day"), ("ground_mean", "GROUND · MEAN kWh/m²·day"),
                         ("ground_lowest10", "LOWEST 10 % GROUND · BELOW"), ("open_flat", "OPEN FLAT GROUND")):
            if lab in tl:
                R["t4_summer_%s_kwh" % key] = rd(float(tl[lab]), 2)
    CF = env.get("comfort")
    if CF:
        names = ("N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW")
        for sd in SEASONS:
            c = CF["seasons"][sd["key"]]
            k = sd["key"]
            # ---- T5 wind (sheet_wind)
            dir_from, share = prevailing(c)
            R["t5_%s_from" % k] = names[int(round(dir_from / 22.5)) % 16]
            R["t5_%s_from_pct" % k] = rd(100.0 * share, 0)
            vals = c["uped"][np.isfinite(c["uped"])]
            open_v = c["u10_mean"] * PED_WIND
            R["t5_%s_open_ms" % k] = rd(open_v, 2)
            R["t5_%s_site_mean_ms" % k] = rd(float(vals.mean()), 2) if vals.size else None
            R["t5_%s_sheltered_pct" % k] = rd(100.0 * float((vals < 0.5 * open_v).mean()), 0) if vals.size else None
            # ---- T6 air (sheet_air)
            ta = c["ta"][np.isfinite(c["ta"])]
            if ta.size:
                R["t6_%s_air_min_c" % k], R["t6_%s_air_max_c" % k] = rd(float(ta.min()), 2), rd(float(ta.max()), 2)
            # ---- T7 felt (sheet_felt)
            u = c["utci"][np.isfinite(c["utci"])]
            R["t7_%s_felt_mean_c" % k] = rd(float(u.mean()), 2) if u.size else None
            R["t7_%s_felt_sun_c" % k] = rd(c["utci_sun"], 2)
            R["t7_%s_felt_shade_c" % k] = rd(c["utci_shade"], 2)
        # ---- T8 comfortable hours (sheet_comfort_year)
        Yr = CF.get("year")
        if Yr:
            v = Yr["comfort"][np.isfinite(Yr["comfort"])]
            v18 = Yr["comfort18"][np.isfinite(Yr["comfort18"])]
            R["t8_year_comfortable_pct"] = rd(float(v.mean()), 0) if v.size else None
            R["t8_best_spot_pct"] = rd(float(v.max()), 0) if v.size else None
            R["t8_worst_spot_pct"] = rd(float(v.min()), 0) if v.size else None
            R["t8_near_comfort_18_26_pct"] = rd(float(v18.mean()), 0) if v18.size else None
            for sd in SEASONS:
                R["t8_%s_comfortable_pct" % sd["key"]] = rd(Yr["share"][sd["key"]], 0)
    return R


def bk_photos():
    """The site photos of the data pack (photo_files, numbered as on plan 01) as booklet_images/photo_<n>.jpg."""
    import shutil
    d = os.path.join(bg_booklet("selinus_board"), "images")        # v44 (27 Oct): cached/booklet/selinus_board/images
    shutil.rmtree(os.path.join(BERGAMA_DIR, "booklet_images"), ignore_errors=True)   # v42 and older wrote it here
    shutil.rmtree(os.path.join(BERGAMA_DIR, "cached", "booklet_images"), ignore_errors=True)   # v43 wrote it here
    if not os.path.isdir(d):
        os.makedirs(d)
    n = 0
    for i, (p, it) in enumerate(photo_files(os.path.join(SELINUS_RES_DIR, "_site_photos"))):
        shutil.copyfile(p, os.path.join(d, "photo_%d.jpg" % (i + 1)))
        n += 1
    BK_LOG.append("photos: %d copied to %s as photo_1..%d.jpg" % (n, d, n))
